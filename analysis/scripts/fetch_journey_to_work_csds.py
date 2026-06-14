# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
"""
fetch_journey_to_work_csds.py

Stream-download StatsCan 98-10-0459-01 (2021 CSD-level commuter flows) and
extract origin-CSD tables for Airdrie, Chestermere, Sylvan Lake, Innisfail,
and Red Deer, Alberta.

Run:
    python analysis/scripts/fetch_journey_to_work_csds.py

Outputs: data/outputs/{csd_slug}_journey_to_work.csv (one file per city)
Reference: analysis/methodology/reference/cochrane_journey_to_work.md
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
OUT  = ROOT / "data" / "outputs"
TEMP = ROOT / ".temp"
TEMP.mkdir(exist_ok=True)

# StatsCan 2021 Census commuter flow table
TABLE_URL = "https://www150.statcan.gc.ca/n1/tbl/csv/98100459-eng.zip"
ZIP_PATH  = TEMP / "statscan_98-10-0459.zip"

# Target CSD slugs → (DGUID, human-readable name for output)
# DGUIDs verified from 98100459.csv column scan 2026-06-13.
TARGETS = {
    "airdrie":    ("2021A00054806021", "Airdrie (CY), Alta."),
    "chestermere":("2021A00054806017", "Chestermere (CY), Alta."),
    "red_deer":   ("2021A00054808011", "Red Deer (CY), Alta."),
    "sylvan_lake":("2021A00054808012", "Sylvan Lake (T), Alta."),
    "innisfail":  ("2021A00054808008", "Innisfail (T), Alta."),
}

OUTPUT_COLS = [
    "origin_csd", "origin_dguid", "origin_csd_code",
    "dest_csd", "workers_total", "workers_men", "workers_women",
    "pct_all_workers", "pct_out_commuters",
]


def _download() -> None:
    """Stream-download ZIP to .temp/ (resume-safe: skip if already complete)."""
    import requests

    if ZIP_PATH.exists():
        remote_size = None
        try:
            r = requests.head(TABLE_URL, timeout=30)
            remote_size = int(r.headers.get("Content-Length", 0))
        except Exception:
            pass
        if remote_size and ZIP_PATH.stat().st_size == remote_size:
            print(f"[fetch] ZIP already downloaded ({ZIP_PATH.stat().st_size // 1_000_000} MB), skipping.")
            return
        elif ZIP_PATH.stat().st_size > 100_000_000:
            print(f"[fetch] ZIP present ({ZIP_PATH.stat().st_size // 1_000_000} MB), assuming complete.")
            return

    print(f"[fetch] Downloading {TABLE_URL}")
    print("        This is ~2.2 GB uncompressed; expect 5–20 minutes.")

    import requests
    with requests.get(TABLE_URL, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0))
        written = 0
        with open(ZIP_PATH, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 20):
                fh.write(chunk)
                written += len(chunk)
                if total:
                    pct = written / total * 100
                    print(f"\r  {written // 1_000_000} MB / {total // 1_000_000} MB  ({pct:.1f}%)",
                          end="", flush=True)
    print(f"\n[fetch] Saved to {ZIP_PATH}")


def _extract_targets() -> dict[str, list[dict]]:
    """Stream the CSV inside the ZIP and collect rows for target DGUIDs."""
    target_dguids = {dguid: slug for slug, (dguid, _) in TARGETS.items()}
    rows: dict[str, list[dict]] = {slug: [] for slug in TARGETS}

    print(f"[extract] Opening {ZIP_PATH} …")
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        # The archive usually contains one CSV named like 98100459.csv
        csv_names = [n for n in zf.namelist() if n.endswith(".csv") and "Meta" not in n]
        if not csv_names:
            raise RuntimeError(f"No data CSV found in ZIP. Contents: {zf.namelist()}")
        csv_name = csv_names[0]
        print(f"[extract] Reading {csv_name} …")

        with zf.open(csv_name) as raw:
            # StatsCan CSVs can be large; use io.TextIOWrapper for UTF-8 streaming
            text = io.TextIOWrapper(raw, encoding="utf-8-sig")
            reader = csv.DictReader(text)

            # Print actual column names to diagnose header variation
            print(f"[extract] Columns: {reader.fieldnames[:8]} …")

            # StatsCan 98-10-0459 columns (2021 release):
            # GEO_CODE (ORG), GEO_LEVEL (ORG), GEO_NAME (ORG), GNR, GNR_LNG,
            # DATA_QUALITY_FLAG, DGUID (ORG), Symbol,
            # GEO_CODE (DES), GEO_LEVEL (DES), GEO_NAME (DES), DGUID (DES),
            # GNR_DES, GNR_LNG_DES, ...
            # Then: Total - Gender, Men+, Women+, ...

            for i, row in enumerate(reader):
                if i % 2_000_000 == 0 and i > 0:
                    print(f"  … {i // 1_000_000}M rows scanned …", flush=True)
                org_dguid = row.get("DGUID") or ""
                if org_dguid in target_dguids:
                    rows[target_dguids[org_dguid]].append(row)

    return rows


def _to_output(slug: str, dguid: str, human: str, raw_rows: list[dict]) -> None:
    """Convert raw StatsCan rows to the cochrane_journey_to_work.csv schema."""
    if not raw_rows:
        print(f"[warn] No rows found for {human} (DGUID {dguid})")
        return

    # Introspect column names from first row
    sample = raw_rows[0]
    keys = list(sample.keys())

    def _col(*candidates: str) -> str:
        for c in candidates:
            if c in sample:
                return c
        return ""

    # Actual columns from 98100459.csv (2021 Census release)
    col_org_name  = _col("GEO", "GEO_NAME (ORG)", "GEO_NAME_ORG")
    col_org_dguid = _col("DGUID", "DGUID (ORG)", "DGUID_ORG")
    col_org_code  = _col("Coordinate", "GEO_CODE (ORG)", "GEO_CODE_ORG")
    col_des_name  = _col("Place of work", "GEO_NAME (DES)", "GEO_NAME_DES")
    col_total     = _col("Gender (3):Total - Gender[1]", "Total - Gender", "Total")
    col_men       = _col("Gender (3):Men+[2]", "Men+", "Men")
    col_women     = _col("Gender (3):Women+[3]", "Women+", "Women")

    # Filter: only rows where Total is numeric (exclude header/symbol rows)
    def _safe_int(v: str) -> int | None:
        try:
            return int(str(v).replace(",", "").strip())
        except (ValueError, AttributeError):
            return None

    clean_rows = []
    for row in raw_rows:
        total = _safe_int(row.get(col_total, ""))
        if total is None or total == 0:
            continue
        clean_rows.append({
            "origin_csd":  row.get(col_org_name, ""),
            "origin_dguid":row.get(col_org_dguid, ""),
            "origin_csd_code": row.get(col_org_code, ""),
            "dest_csd":    row.get(col_des_name, ""),
            "workers_total": total,
            "workers_men":   _safe_int(row.get(col_men, "")) or 0,
            "workers_women": _safe_int(row.get(col_women, "")) or 0,
        })

    if not clean_rows:
        print(f"[warn] All rows for {human} had non-numeric totals — check column names.")
        print(f"       Sample keys: {keys[:12]}")
        return

    # Sort by workers_total descending
    clean_rows.sort(key=lambda r: r["workers_total"], reverse=True)

    # Compute self (work-in-CSD) and out-commuters
    self_workers = next(
        (r["workers_total"] for r in clean_rows if human.lower() in r["dest_csd"].lower()),
        0,
    )
    all_workers  = sum(r["workers_total"] for r in clean_rows)
    out_workers  = all_workers - self_workers

    out_path = OUT / f"{slug}_journey_to_work.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUTPUT_COLS)
        writer.writeheader()
        for r in clean_rows:
            is_self = human.lower() in r["dest_csd"].lower()
            pct_all = r["workers_total"] / all_workers * 100 if all_workers else 0
            pct_out = r["workers_total"] / out_workers * 100 if (out_workers and not is_self) else None
            writer.writerow({
                **r,
                "pct_all_workers":   f"{pct_all:.2f}",
                "pct_out_commuters": f"{pct_out:.2f}" if pct_out is not None else "",
            })

    print(f"[out] {out_path.name}  ({len(clean_rows)} destinations, {all_workers:,} workers)")


def main() -> int:
    _download()
    raw = _extract_targets()
    for slug, (dguid, human) in TARGETS.items():
        _to_output(slug, dguid, human, raw[slug])
    print("[fetch_journey_to_work_csds] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
