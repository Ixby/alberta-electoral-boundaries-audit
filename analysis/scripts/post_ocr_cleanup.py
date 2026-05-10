"""
post_ocr_cleanup.py

Run AFTER submission_sentiment_llm_full.py completes AND after OCR recovery.

Removes the 10 OCR-recovered submissions that were classified on boilerplate text
from the progress CSV and results CSV, then prints a reminder to re-run the
full-corpus scan (which will only classify the newly-recovered submissions).

The 23 OCR IDs:
  - 17 Round 1 (10 already processed on boilerplate; 7 will be processed later)
  - 6 Round 2 (not yet processed — will be handled in the normal run)

Only the 10 already-processed R1 IDs need cleanup.

Usage:
    python analysis/scripts/post_ocr_cleanup.py [--dry-run]
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

try:
    sys.path.insert(0, str(ROOT / "analysis" / "utils"))
    import data_loader
    DATA_DIR = data_loader._resolve_path("data")
except Exception:
    DATA_DIR = ROOT / "data"

PROGRESS_CSV = DATA_DIR / "outputs" / "submission_sentiment_llm_full_progress.csv"
RESULTS_CSV  = DATA_DIR / "outputs" / "submission_sentiment_llm_full_results.csv"

# The 10 R1 IDs classified on boilerplate before OCR recovery ran
STALE_IDS = {
    "EBC-2025-1-0011",
    "EBC-2025-1-0013",
    "EBC-2025-1-0015",
    "EBC-2025-1-0016",
    "EBC-2025-1-0018",
    "EBC-2025-1-0020",
    "EBC-2025-1-0065",
    "EBC-2025-1-0082",
    "EBC-2025-1-0086",
    "EBC-2025-1-0097",
}


def main(dry_run: bool = False) -> None:
    # ── Progress CSV ──────────────────────────────────────────────────────────
    if not PROGRESS_CSV.exists():
        print(f"ERROR: progress CSV not found at {PROGRESS_CSV}")
        sys.exit(1)

    with PROGRESS_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)

    kept_progress = [r for r in rows if r["submission_id"] not in STALE_IDS]
    removed_progress = len(rows) - len(kept_progress)
    print(f"Progress CSV: {len(rows)} rows -> removing {removed_progress} stale IDs -> {len(kept_progress)} kept")

    if not dry_run:
        with PROGRESS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(kept_progress)

    # ── Results CSV ───────────────────────────────────────────────────────────
    if not RESULTS_CSV.exists():
        print(f"Results CSV not found — nothing to clean there.")
    else:
        with RESULTS_CSV.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fields_r = reader.fieldnames or []
            rows_r = list(reader)

        kept_results = [r for r in rows_r if r.get("submission_id") not in STALE_IDS]
        removed_results = len(rows_r) - len(kept_results)
        print(f"Results CSV:  {len(rows_r)} rows -> removing {removed_results} stale rows -> {len(kept_results)} kept")

        if not dry_run:
            with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields_r)
                writer.writeheader()
                writer.writerows(kept_results)

    if dry_run:
        print("\n[dry-run] No files written.")
    else:
        print("\nDone. Now re-run:")
        print("  python analysis/scripts/submission_sentiment_llm_full.py")
        print("It will classify only the purged IDs (all others are still in progress CSV).")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN -- no files will be modified")
    main(dry_run=dry_run)
