"""
validation_sample.py

Generate a stratified random sample of classified rows for human inter-rater
reliability review. Samples 5% of rows per (configuration x classification)
cell, minimum 1 per non-empty cell, maximum 20.

Usage:
    python validation_sample.py [--input path]

Output:
    DATA_DIR / "outputs" / "validation_sample_for_review.csv"
"""

from __future__ import annotations

import argparse
import csv
import math
import random
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

DEFAULT_INPUT_CLEAN = OUTPUTS_DIR / "submission_sentiment_llm_full_results_clean.csv"
DEFAULT_INPUT_RAW   = OUTPUTS_DIR / "submission_sentiment_llm_full_results.csv"
DEFAULT_OUTPUT      = OUTPUTS_DIR / "validation_sample_for_review.csv"

# Classifications to include in the sample (exclude Unrelated and
# unverifiable-suffix variants)
VALID_CLASSIFICATIONS = {
    "Active Support",
    "Active Opposition",
    "Neutral/Contextual",
}

# Unverifiable suffixes to exclude
UNVERIFIABLE_SUFFIXES = ("(Quote Unverifiable)", "(Unverifiable)")

SOURCE_EXCERPT_CHARS = 400

def source_excerpt(submission_id: str) -> str:
    """Return the first SOURCE_EXCERPT_CHARS characters of the source document."""
    text, _ = loader.get_text(submission_id)
    if not text:
        return ""
    return text[:SOURCE_EXCERPT_CHARS].replace("\n", " ").replace("\r", " ")


# ---------------------------------------------------------------------------
# Classification filter helpers
# ---------------------------------------------------------------------------

def is_valid_classification(classification: str) -> bool:
    """Return True if this row should be included in sampling."""
    if not classification:
        return False
    stripped = classification.strip()
    # Exclude unverifiable suffixes
    for suffix in UNVERIFIABLE_SUFFIXES:
        if suffix in stripped:
            return False
    return stripped in VALID_CLASSIFICATIONS


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def resolve_input(explicit_path: str | None) -> Path:
    if explicit_path:
        p = Path(explicit_path)
        if not p.is_absolute():
            p = Path.cwd() / p
        return p
    if DEFAULT_INPUT_CLEAN.exists():
        return DEFAULT_INPUT_CLEAN
    return DEFAULT_INPUT_RAW


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate stratified validation sample for inter-rater reliability."
    )
    parser.add_argument("--input", default=None, help="Path to results CSV (optional).")
    args = parser.parse_args()

    input_path = resolve_input(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    print(f"Reading: {input_path}")

    # ------------------------------------------------------------------
    # Load all rows and group by (configuration, classification)
    # ------------------------------------------------------------------
    random.seed(42)

    all_rows: list[dict] = []
    groups: dict[tuple[str, str], list[dict]] = {}

    with open(input_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        for row in reader:
            all_rows.append(row)
            config = row.get("configuration", "").strip()
            classification = row.get("classification", "").strip()
            if not is_valid_classification(classification):
                continue
            key = (config, classification)
            groups.setdefault(key, []).append(row)

    total_rows = len(all_rows)
    print(f"Total rows in dataset: {total_rows}")

    # ------------------------------------------------------------------
    # Stratified sample
    # ------------------------------------------------------------------
    sampled_rows: list[dict] = []

    for (config, classification), cell_rows in sorted(groups.items()):
        n = len(cell_rows)
        k = min(max(math.ceil(n * 0.05), 1), 20)
        chosen = random.sample(cell_rows, k)
        sampled_rows.extend(chosen)

    total_sampled = len(sampled_rows)
    print(f"Rows sampled: {total_sampled}")

    # ------------------------------------------------------------------
    # Add source_excerpt + blank reviewer columns; write output
    # ------------------------------------------------------------------
    output_fieldnames = fieldnames + [
        "human_classification",
        "human_notes",
        "source_excerpt",
    ]

    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(DEFAULT_OUTPUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=output_fieldnames)
        writer.writeheader()
        for row in sampled_rows:
            out_row = dict(row)
            out_row["human_classification"] = ""
            out_row["human_notes"] = ""
            out_row["source_excerpt"] = source_excerpt(
                row.get("submission_id", "")
            )
            writer.writerow(out_row)

    print(f"Output written: {DEFAULT_OUTPUT}")

    # ------------------------------------------------------------------
    # Per-configuration breakdown
    # ------------------------------------------------------------------
    config_counts: dict[str, int] = {}
    for row in sampled_rows:
        c = row.get("configuration", "(unknown)").strip()
        config_counts[c] = config_counts.get(c, 0) + 1

    print("\nSampled rows per configuration:")
    for config, count in sorted(config_counts.items()):
        print(f"  {config}: {count}")

    # ------------------------------------------------------------------
    # Reviewer instructions
    # ------------------------------------------------------------------
    print(
        "\n------------------------------------------------------------------"
        "\nREVIEWER INSTRUCTIONS"
        "\n------------------------------------------------------------------"
        "\nOpen the output CSV and fill in the 'human_classification' column"
        "\nfor each row using exactly one of the following labels:"
        "\n"
        "\n    Active Support"
        "\n    Active Opposition"
        "\n    Neutral/Contextual"
        "\n    Unrelated"
        "\n"
        "\nUse 'human_notes' for any comments about a difficult or borderline case."
        "\nThe 'source_excerpt' column shows the first 400 characters of the"
        "\nsource document to help orient your review."
        "\n"
        "\nWhen done, save the file and run:"
        "\n    python compute_kappa.py"
        "\n------------------------------------------------------------------"
    )


if __name__ == "__main__":
    main()
