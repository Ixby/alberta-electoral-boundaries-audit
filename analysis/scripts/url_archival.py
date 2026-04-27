"""
v0_1_url_archival.py

Alberta Electoral Boundaries Audit — URL preservation pipeline.

Extracts every http/https URL from FROZEN_MANIFEST.md and submits each to
the Internet Archive Wayback Machine and archive.ph, recording the
permanent snapshot URLs produced.

Outputs:
  .temp/frozen_manifest_urls.txt        deduped URL list
  .temp/wayback_results.csv             Wayback submission outcomes
  .temp/archiveph_results.csv           archive.ph submission outcomes

Forward dependencies:
  - FROZEN_MANIFEST.md (input)
  - requests (HTTP)
Backward dependencies:
  - analysis/url_archival_log.md (summary consumes the CSVs)
  - FROZEN_MANIFEST.md (rewrite step consumes the CSVs)
"""
# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import csv
import os
import re
import sys
import time
from pathlib import Path

import requests

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

REPO = Path(__file__).resolve().parent.parent.parent
MANIFEST = REPO / "FROZEN_MANIFEST.md"
TEMP = REPO / ".temp"
TEMP.mkdir(exist_ok=True)

URL_LIST = TEMP / "frozen_manifest_urls.txt"
WAYBACK_CSV = TEMP / "wayback_results.csv"
ARCHIVEPH_CSV = TEMP / "archiveph_results.csv"

UA = "AlbertaBoundariesAudit/0.1 (contact: repo maintainer; academic reproducibility archival)"

URL_RE = re.compile(r"https?://[^\s\)\]\|>]+")


def extract_urls(manifest_path: Path) -> list[str]:
    text = manifest_path.read_text(encoding="utf-8")
    raw = URL_RE.findall(text)
    cleaned: list[str] = []
    for u in raw:
        u = u.rstrip(".,;:")
        # Drop manifest-internal pattern illustrations and elided example URLs.
        if "NNNN" in u:
            continue
        if "/..." in u:
            continue
        # Sample pattern rows in the manifest reference pattern segments like
        # "/NNNNe.htm (N=1001-1087)" — already filtered by NNNN check.
        cleaned.append(u)
    seen: set[str] = set()
    deduped: list[str] = []
    for u in cleaned:
        if u in seen:
            continue
        seen.add(u)
        deduped.append(u)
    # For the 338canada per-riding page pattern, add three concrete probes
    # so the Wayback save will have meaningful coverage. One concrete URL
    # is enough to demonstrate that the pattern resolves; pattern rows in
    # the manifest reference all 87 rather than any single URL.
    if "https://338canada.com/alberta/" in deduped:
        for probe in (
            "https://338canada.com/alberta/1001e.htm",
            "https://338canada.com/alberta/1044e.htm",
            "https://338canada.com/alberta/1087e.htm",
        ):
            if probe not in seen:
                deduped.append(probe)
                seen.add(probe)
    return deduped


def submit_wayback(url: str, session: requests.Session) -> dict:
    """
    Look up the most-recent existing Wayback snapshot for url.

    Queries the CDX API first (it returns exact-URL matches with better
    coverage than the availability API, including 200-status responses only).
    Falls back to the availability API if CDX is unavailable.

    As of 2026 the anonymous /save/ endpoint requires authentication. Without
    IA credentials we cannot trigger a fresh capture, so recording the most
    recent existing snapshot is the best anonymous path. Retries 3x.
    """
    last_err = None
    for attempt in range(3):
        try:
            cdx = session.get(
                "https://web.archive.org/cdx/search/cdx",
                params={
                    "url": url,
                    "limit": "-1",            # most recent
                    "output": "json",
                    "filter": "statuscode:200",
                },
                headers={"User-Agent": UA},
                timeout=45,
            )
            if cdx.status_code == 200:
                rows = cdx.json()
                # First row is the header.
                if len(rows) >= 2:
                    header, data = rows[0], rows[1]
                    d = dict(zip(header, data))
                    ts = d.get("timestamp", "")
                    orig = d.get("original", url)
                    if ts:
                        snapshot = f"https://web.archive.org/web/{ts}/{orig}"
                        return {
                            "original_url": url,
                            "wayback_snapshot_url": snapshot,
                            "timestamp": ts,
                            "status": "ok",
                            "error_message": "existing snapshot via CDX API",
                        }
                # CDX returned zero data rows — no 200-status snapshot exists.
                # Fall through to availability API as a second opinion.
            if cdx.status_code == 429 or 500 <= cdx.status_code < 600:
                last_err = f"CDX HTTP {cdx.status_code}"
                time.sleep(2 ** attempt * 5)
                continue
        except requests.RequestException as e:
            last_err = f"CDX: {e}"

        # Availability API fallback.
        try:
            avail = session.get(
                f"https://archive.org/wayback/available?url={url}",
                headers={"User-Agent": UA},
                timeout=30,
            )
            if avail.status_code == 200:
                j = avail.json()
                cs = j.get("archived_snapshots", {}).get("closest", {})
                if cs.get("available") and cs.get("url"):
                    return {
                        "original_url": url,
                        "wayback_snapshot_url": cs["url"],
                        "timestamp": cs.get("timestamp", ""),
                        "status": "ok",
                        "error_message": "existing snapshot via availability API",
                    }
                return {
                    "original_url": url,
                    "wayback_snapshot_url": "",
                    "timestamp": "",
                    "status": "unarchived",
                    "error_message": "no existing snapshot; anonymous /save/ requires auth",
                }
        except requests.RequestException as e:
            last_err = str(e)
            time.sleep(2 ** attempt * 3)
    return {
        "original_url": url,
        "wayback_snapshot_url": "",
        "timestamp": "",
        "status": "error",
        "error_message": last_err or "unknown",
    }


def availability_only(url: str, session: requests.Session) -> dict:
    """Fallback: look up the closest existing Wayback snapshot without submitting."""
    try:
        avail = session.get(
            f"https://archive.org/wayback/available?url={url}",
            headers={"User-Agent": UA},
            timeout=30,
        )
        if avail.status_code == 200:
            j = avail.json()
            cs = j.get("archived_snapshots", {}).get("closest", {})
            if cs.get("available") and cs.get("url"):
                return {
                    "original_url": url,
                    "wayback_snapshot_url": cs["url"],
                    "timestamp": cs.get("timestamp", ""),
                    "status": "ok",
                    "error_message": "existing snapshot via availability API",
                }
        return {
            "original_url": url,
            "wayback_snapshot_url": "",
            "timestamp": "",
            "status": "error",
            "error_message": "no existing snapshot",
        }
    except requests.RequestException as e:
        return {
            "original_url": url,
            "wayback_snapshot_url": "",
            "timestamp": "",
            "status": "error",
            "error_message": str(e),
        }


def submit_archiveph(url: str, session: requests.Session) -> dict:
    """
    Query archive.ph /newest/<URL> for an existing snapshot. Retry with
    exponential backoff on HTTP 429 rate-limit. If /newest returns no
    snapshot, fall through to /submit/ (which may also be rate-limited).
    """
    # /newest — look up an existing snapshot. Retries on 429.
    for attempt in range(4):
        try:
            r = session.get(
                f"https://archive.ph/newest/{url}",
                headers={"User-Agent": UA},
                timeout=30,
                allow_redirects=False,
            )
            if r.status_code in (301, 302, 303, 307, 308):
                loc = r.headers.get("Location", "")
                if loc and "archive.ph/" in loc and "/newest/" not in loc:
                    return {
                        "original_url": url,
                        "archiveph_snapshot_url": loc,
                        "status": "ok",
                        "error_message": "existing snapshot via /newest",
                    }
            if r.status_code == 200 and "archive.ph" in r.url and "/newest/" not in r.url:
                return {
                    "original_url": url,
                    "archiveph_snapshot_url": r.url,
                    "status": "ok",
                    "error_message": "existing snapshot via /newest",
                }
            if r.status_code == 404:
                # No existing snapshot. Break to /submit path.
                break
            if r.status_code == 429:
                time.sleep(15 + 10 * attempt)
                continue
            # Other non-terminal: break to /submit.
            break
        except requests.RequestException:
            time.sleep(5 + 5 * attempt)
            continue

    # /submit — fresh capture request. Usually heavily rate-limited.
    try:
        r = session.post(
            "https://archive.ph/submit/",
            data={"url": url},
            headers={"User-Agent": UA},
            timeout=90,
            allow_redirects=False,
        )
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location", "")
            if loc.startswith("http") and "archive.ph/" in loc:
                return {
                    "original_url": url,
                    "archiveph_snapshot_url": loc,
                    "status": "ok",
                    "error_message": "fresh submission",
                }
        refresh = r.headers.get("Refresh", "")
        m = re.search(r"url=(https?://archive\.ph/\S+)", refresh, re.IGNORECASE)
        if m:
            return {
                "original_url": url,
                "archiveph_snapshot_url": m.group(1),
                "status": "ok",
                "error_message": "fresh submission via Refresh header",
            }
        return {
            "original_url": url,
            "archiveph_snapshot_url": "",
            "status": "error",
            "error_message": f"HTTP {r.status_code}; no snapshot URL in response",
        }
    except requests.RequestException as e:
        return {
            "original_url": url,
            "archiveph_snapshot_url": "",
            "status": "error",
            "error_message": str(e),
        }


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    urls = extract_urls(MANIFEST)
    URL_LIST.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"[phase1] extracted {len(urls)} unique URLs -> {URL_LIST}")

    session = requests.Session()

    # Phase 2 — Wayback availability lookups. The anonymous /save/ endpoint
    # now requires authentication; the availability API remains public and
    # returns the closest existing snapshot.
    wayback_rows: list[dict] = []
    for i, u in enumerate(urls, 1):
        print(f"[phase2 {i}/{len(urls)}] wayback: {u[:100]}")
        row = submit_wayback(u, session)
        wayback_rows.append(row)
        time.sleep(2)
    write_csv(
        WAYBACK_CSV,
        wayback_rows,
        ["original_url", "wayback_snapshot_url", "timestamp", "status", "error_message"],
    )
    print(f"[phase2] wrote {WAYBACK_CSV}")

    # Phase 3 — archive.ph /newest with retries. Longer per-URL spacing to
    # avoid the aggressive 429 rate-limit we hit on the first pass.
    archiveph_rows: list[dict] = []
    for i, u in enumerate(urls, 1):
        print(f"[phase3 {i}/{len(urls)}] archive.ph: {u[:100]}")
        row = submit_archiveph(u, session)
        archiveph_rows.append(row)
        time.sleep(8)
    write_csv(
        ARCHIVEPH_CSV,
        archiveph_rows,
        ["original_url", "archiveph_snapshot_url", "status", "error_message"],
    )
    print(f"[phase3] wrote {ARCHIVEPH_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
