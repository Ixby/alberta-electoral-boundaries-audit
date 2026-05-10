"""
quote_verify_and_clean.py

Post-process sentiment results CSV to ensure every exact_quote is a verbatim
substring of its source document. Forensic integrity layer.

Usage:
    python quote_verify_and_clean.py [--input path] [--output path] [--dry-run]
"""

import argparse
import csv
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from sentiment_config import DATA_DIR, TEXT_DIR, OUTPUTS_DIR, CONFIGS, STANCE_ENUM
from source_loader import SourceLoader
from quote_verifier import verify_quote, VerificationResult, PRIMARY_STATUSES, STATUS_HALLUCINATED, STATUS_MISSING, STATUS_NA, STATUS_WEAK

loader = SourceLoader()

DEFAULT_INPUT  = OUTPUTS_DIR / "submission_sentiment_llm_full_results.csv"
DEFAULT_OUTPUT = OUTPUTS_DIR / "submission_sentiment_llm_full_results_clean.csv"


# ---------------------------------------------------------------------------
# Classification downgrade helper
# ---------------------------------------------------------------------------
def _maybe_downgrade(row: dict) -> None:
    """Append visibility tag to Active Support/Opposition classifications."""
    cls = row.get("classification", "")
    active_classes = {"active support", "active opposition"}
    if cls.strip().lower() in active_classes:
        row["classification"] = cls + " (Quote Unverifiable)"


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------
def process(input_path: Path, output_path: Path, dry_run: bool) -> None:
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not rows:
        print("No rows found in input CSV.")
        return

    # Ensure original_quote column exists in output
    out_fields = list(fieldnames)
    if "quote_verified" not in out_fields:
        out_fields.append("quote_verified")
    if "original_quote" not in out_fields:
        out_fields.append("original_quote")

    # Counters
    counts: dict[str, int] = {}
    downgraded = 0
    source_missing = 0

    processed_rows = []

    for row in rows:
        submission_id = row.get("submission_id", "").strip()

        text, found = loader.get_text(submission_id)

        if not found:
            row["original_quote"] = row.get("exact_quote", "")
            row["quote_verified"] = STATUS_MISSING
            counts[STATUS_MISSING] = counts.get(STATUS_MISSING, 0) + 1
            processed_rows.append(row)
            source_missing += 1
            continue

        classification = row.get("classification", "")
        exact_quote = row.get("exact_quote", "").strip()

        # Preserve original LLM quote for audit trail
        row["original_quote"] = exact_quote

        # Neutral/Contextual or Unrelated — skip quote verification
        neutral_classes = {"neutral/contextual", "unrelated"}
        if classification.strip().lower() in neutral_classes:
            row["exact_quote"] = ""
            row["quote_verified"] = STATUS_NA
            counts[STATUS_NA] = counts.get(STATUS_NA, 0) + 1
            processed_rows.append(row)
            continue

        sentences = loader.get_sentences(submission_id)
        vr = verify_quote(exact_quote, text, reasoning=row.get("reasoning", ""), sentences=sentences)

        cls_before = classification
        row["exact_quote"] = vr.quote
        row["quote_verified"] = vr.status

        if vr.downgrade:
            _maybe_downgrade(row)

        cls_after = row.get("classification", "")
        if cls_after != cls_before:
            downgraded += 1

        counts[vr.status] = counts.get(vr.status, 0) + 1
        processed_rows.append(row)

    # Print summary
    print()
    print("=== Quote Verification Summary ===")
    for code, count in sorted(counts.items()):
        print(f"  {code}: {count}")

    primary = sum(counts.get(s, 0) for s in PRIMARY_STATUSES)
    hallucinated = counts.get(STATUS_HALLUCINATED, 0)

    print()
    print(f"Primary count (True+Normalized+Extracted): {primary}")
    print(f"Excluded (Hallucinated): {hallucinated}")
    print(f"Classifications downgraded: {downgraded}")
    if source_missing:
        print(f"Source files missing: {source_missing}")
    print()

    if dry_run:
        print("[Dry run] No output written.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(processed_rows)

    print(f"Cleaned CSV written to: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify and clean exact_quote columns against source documents."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Input CSV path (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without writing output file.",
    )
    args = parser.parse_args()
    process(args.input, args.output, args.dry_run)


if __name__ == "__main__":
    main()
