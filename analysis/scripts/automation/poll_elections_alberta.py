"""Backstop poller for Elections Alberta shapefile releases.

Runs on a weekly schedule (Sunday 06:00 UTC) via the GitHub Actions
workflow `.github/workflows/recompute-on-shapefile-release.yml`. The
ChangeDetection.io watcher (set up per `analysis/automation/
changedetection_setup.md`) is the primary detector; this poller is the
safety net in case the watcher misses a release or is offline.

Behaviour:
  - Fetches the audit's tracked Elections Alberta release pages
  - Hashes each one against the last seen hash (stored in
    .temp/automation_state/last_hashes.json)
  - If any page changed since the last poll: download any .gpkg/.zip
    links found on the page into the output directory and exit 0
  - If no page changed: exit 1 (signals the GitHub workflow's backstop
    branch to skip the recompute)

Usage:
    python analysis/scripts/automation/poll_elections_alberta.py \
        --output-dir .temp/inbound

Watched pages (update this list when the audit identifies new tracking
endpoints, or when Elections Alberta restructures their site):
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path

WATCHED_PAGES = [
    # Primary GIS data landing page
    "https://www.elections.ab.ca/resource-centre/maps-data/",
    # 2026 boundary commission redistricting page (if it exists)
    "https://www.abebc.ca/",
    # Direct GIS resources page
    "https://www.elections.ab.ca/resources/maps-and-gis-data/",
]

# File-extension patterns we care about
SHAPEFILE_PATTERN = re.compile(
    r'href=["\']([^"\']+\.(?:gpkg|zip|shp))["\']',
    re.IGNORECASE
)

USER_AGENT = (
    "Mozilla/5.0 (compatible; AlbertaElectoralBoundariesAudit/0.1; "
    "+https://github.com/Ixby/alberta-electoral-boundaries-audit)"
)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_state(state_path: Path) -> dict:
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text())


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2))


def discover_shapefile_links(html: bytes, base_url: str) -> list[str]:
    text = html.decode("utf-8", errors="replace")
    matches = SHAPEFILE_PATTERN.findall(text)
    resolved = []
    for href in matches:
        resolved.append(urllib.parse.urljoin(base_url, href))
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--state-file", default=Path(".temp/automation_state/last_hashes.json"),
                        type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    state = load_state(args.state_file)
    new_state = {}
    any_changed = False
    discovered_files: list[str] = []

    for page_url in WATCHED_PAGES:
        try:
            html = fetch(page_url)
        except Exception as e:
            print(f"WARN: could not fetch {page_url}: {e}", file=sys.stderr)
            continue

        h = hash_bytes(html)
        new_state[page_url] = h
        if state.get(page_url) != h:
            any_changed = True
            print(f"CHANGED: {page_url}")
            for link in discover_shapefile_links(html, page_url):
                print(f"  found: {link}")
                discovered_files.append(link)
        else:
            print(f"unchanged: {page_url}")

    save_state(args.state_file, new_state)

    if not any_changed:
        print("\nNo watched page changed since last poll. Exiting 1 to signal no recompute needed.")
        return 1

    if not discovered_files:
        print("\nWatched page(s) changed but no shapefile links discovered. "
              "Maintainer should investigate manually.")
        return 1

    # Download discovered files
    for url in discovered_files:
        fname = Path(urllib.parse.urlparse(url).path).name
        out_path = args.output_dir / fname
        print(f"Downloading {url} -> {out_path}")
        try:
            data = fetch(url)
            out_path.write_bytes(data)
            print(f"  wrote {out_path} ({len(data)/1024/1024:.1f} MB)")
        except Exception as e:
            print(f"  WARN: download failed: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
