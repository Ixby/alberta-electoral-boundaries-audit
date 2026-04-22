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
  - analysis/v0_1_url_archival_log.md (summary consumes the CSVs)
  - FROZEN_MANIFEST.md (rewrite step consumes the CSVs)
"""

from __future__ import annotations

import csv
import os
import re
import sys
import time
from pathlib import Path

import requests

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

REPO = Path(__file__).resolve().parent.parent
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
    POST to https://web.archive.org/save/<URL> and parse the returned
    Content-Location or Location header for the permanent snapshot URL.
    Retries up to 3 times with exponential backoff on 5xx or network errors.
    """
    save_url = f"https://web.archive.org/save/{url}"
    last_err = None
    for attempt in range(3):
        try:
            resp = session.get(
                save_url,
                headers={"User-Agent": UA, "Accept": "text/html"},
                timeout=60,
                allow_redirects=False,
            )
            status = resp.status_code
            # The save endpoint returns 200 on success with the snapshot path in
            # Content-Location, or a 302 to the snapshot, or a 429 when rate limited.
            loc = resp.headers.get("Content-Location") or resp.headers.get("Location") or ""
            if loc.startswith("/web/"):
                snapshot = "https://web.archive.org" + loc
                ts_match = re.search(r"/web/(\d{14})/", snapshot)
                ts = ts_match.group(1) if ts_match else ""
                return {
                    "original_url": url,
                    "wayback_snapshot_url": snapshot,
                    "timestamp": ts,
                    "status": "ok",
                    "error_message": "",
                }
            if status == 200 and "web.archive.org/web/" in resp.text:
                m = re.search(r"https://web\.archive\.org/web/(\d{14})/[^\s\"']+", resp.text)
                if m:
                    snapshot = m.group(0)
                    ts = m.group(1)
                    return {
                        "original_url": url,
                        "wayback_snapshot_url": snapshot,
                        "timestamp": ts,
                        "status": "ok",
                        "error_message": "",
                    }
            if status == 429:
                last_err = f"rate-limited (HTTP 429)"
                time.sleep(2 ** attempt * 10)
                continue
            if status in (403, 451):
                return {
                    "original_url": url,
                    "wayback_snapshot_url": "",
                    "timestamp": "",
                    "status": "blocked",
                    "error_message": f"HTTP {status}",
                }
            if 500 <= status < 600:
                last_err = f"HTTP {status}"
                time.sleep(2 ** attempt * 5)
                continue
            # Fall through: try the availability API as a fallback.
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
            last_err = f"HTTP {status}, no snapshot parsed"
            time.sleep(2 ** attempt * 3)
        except requests.RequestException as e:
            last_err = str(e)
            time.sleep(2 ** attempt * 5)
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
    Try archive.ph /submit first. If rate-limited or failing, fall back to
    /newest/<URL> which returns an existing snapshot if one exists.
    """
    # First try /newest which is faster and does not trigger a new capture.
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
        # 404 on /newest means no existing snapshot; try submit.
    except requests.RequestException as e:
        # Fall through to submit path.
        pass

    # Submit path — build a fresh snapshot.
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
        # archive.ph sometimes returns a Refresh header with the eventual URL.
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

    # Phase 2 — Wayback.
    wayback_rows: list[dict] = []
    for i, u in enumerate(urls, 1):
        print(f"[phase2 {i}/{len(urls)}] wayback: {u[:100]}")
        row = submit_wayback(u, session)
        wayback_rows.append(row)
        # ~15 req/min cap on anonymous save endpoint -> 4s spacing baseline.
        time.sleep(5)
    write_csv(
        WAYBACK_CSV,
        wayback_rows,
        ["original_url", "wayback_snapshot_url", "timestamp", "status", "error_message"],
    )
    print(f"[phase2] wrote {WAYBACK_CSV}")

    # Phase 3 — archive.ph.
    archiveph_rows: list[dict] = []
    for i, u in enumerate(urls, 1):
        print(f"[phase3 {i}/{len(urls)}] archive.ph: {u[:100]}")
        row = submit_archiveph(u, session)
        archiveph_rows.append(row)
        time.sleep(4)
    write_csv(
        ARCHIVEPH_CSV,
        archiveph_rows,
        ["original_url", "archiveph_snapshot_url", "status", "error_message"],
    )
    print(f"[phase3] wrote {ARCHIVEPH_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
