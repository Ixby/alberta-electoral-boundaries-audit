"""
compute_kappa.py

Compute Cohen's kappa between LLM and human classifications from the
validation sample CSV produced by validation_sample.py.

Usage:
    python compute_kappa.py [--input path]

Output:
    Prints report to stdout.
    Writes DATA_DIR / "outputs" / "kappa_report.txt"
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from sentiment_config import DATA_DIR, TEXT_DIR, OUTPUTS_DIR, CONFIGS, STANCE_ENUM
from source_loader import SourceLoader
from quote_verifier import verify_quote, VerificationResult, PRIMARY_STATUSES, STATUS_HALLUCINATED, STATUS_MISSING, STATUS_NA, STATUS_WEAK

DEFAULT_INPUT  = OUTPUTS_DIR / "validation_sample_for_review.csv"
DEFAULT_REPORT = OUTPUTS_DIR / "kappa_report.txt"

MIN_ROWS_FOR_CONFIG_KAPPA = 5

# ---------------------------------------------------------------------------
# Kappa helpers
# ---------------------------------------------------------------------------

def _kappa_from_lists(y_llm: list[str], y_human: list[str]) -> float | None:
    """
    Compute Cohen's kappa between two equal-length label lists.
    Returns None if computation is impossible (e.g. only one class, n=0).
    """
    n = len(y_llm)
    if n == 0:
        return None

    # Try sklearn first
    try:
        from sklearn.metrics import cohen_kappa_score
        return float(cohen_kappa_score(y_llm, y_human))
    except ImportError:
        pass
    except Exception:
        pass

    # Manual computation
    labels = sorted(set(y_llm) | set(y_human))
    if len(labels) < 2:
        # Perfect agreement (or degenerate)
        return 1.0 if y_llm == y_human else None

    # Confusion matrix: conf[llm_label][human_label] = count
    conf: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for ll, hu in zip(y_llm, y_human):
        conf[ll][hu] += 1

    # p_o = observed agreement
    p_o = sum(conf[lb][lb] for lb in labels) / n

    # Marginals
    row_totals = {lb: sum(conf[lb].values()) for lb in labels}
    col_totals: dict[str, int] = defaultdict(int)
    for lb_r in labels:
        for lb_c in labels:
            col_totals[lb_c] += conf[lb_r][lb_c]

    # p_e = expected agreement by chance
    p_e = sum((row_totals[lb] / n) * (col_totals[lb] / n) for lb in labels)

    if abs(1.0 - p_e) < 1e-12:
        return 1.0

    return (p_o - p_e) / (1.0 - p_e)


def interpret_kappa(k: float) -> str:
    if k < 0.2:
        return "poor"
    if k < 0.4:
        return "fair"
    if k < 0.6:
        return "moderate"
    if k < 0.8:
        return "substantial"
    return "almost perfect"


# ---------------------------------------------------------------------------
# Confusion matrix renderer
# ---------------------------------------------------------------------------

def _format_confusion_matrix(
    y_llm: list[str],
    y_human: list[str],
    labels: list[str],
) -> list[str]:
    """Return lines of a plain-text confusion matrix."""
    conf: dict[str, dict[str, int]] = {
        lb: {lb2: 0 for lb2 in labels} for lb in labels
    }
    for ll, hu in zip(y_llm, y_human):
        if ll in conf and hu in conf[ll]:
            conf[ll][hu] += 1

    col_w = max(len(lb) for lb in labels) + 2
    row_label_w = max(len(lb) for lb in labels) + 2

    lines: list[str] = []
    header = " " * row_label_w + "".join(lb.ljust(col_w) for lb in labels)
    lines.append("  LLM (rows) x Human (columns)")
    lines.append("  " + header)
    lines.append("  " + "-" * len(header))
    for lb_r in labels:
        row_str = lb_r.ljust(row_label_w)
        for lb_c in labels:
            row_str += str(conf[lb_r][lb_c]).ljust(col_w)
        lines.append("  " + row_str)
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute Cohen's kappa from the completed validation sample."
    )
    parser.add_argument("--input", default=None, help="Path to validation sample CSV.")
    args = parser.parse_args()

    input_path = Path(args.input) if args.input else DEFAULT_INPUT
    if not input_path.is_absolute() and args.input:
        input_path = Path.cwd() / input_path

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        print("Run validation_sample.py first and fill in human_classification.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Load rows
    # ------------------------------------------------------------------
    all_rows: list[dict] = []
    with open(input_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            all_rows.append(row)

    # Filter to rows with a human classification
    reviewed: list[dict] = [
        r for r in all_rows
        if r.get("human_classification", "").strip()
    ]

    total_in_file = len(all_rows)
    total_reviewed = len(reviewed)

    if total_reviewed == 0:
        print(
            "No rows with human_classification found.\n"
            "Open the validation sample CSV, fill in human_classification,"
            " then re-run this script."
        )
        sys.exit(0)

    # ------------------------------------------------------------------
    # Gather paired labels
    # ------------------------------------------------------------------
    y_llm   = [r["classification"].strip() for r in reviewed]
    y_human = [r["human_classification"].strip() for r in reviewed]

    all_labels = sorted(set(y_llm) | set(y_human))

    # ------------------------------------------------------------------
    # Build report lines
    # ------------------------------------------------------------------
    lines: list[str] = []

    lines.append("=" * 66)
    lines.append("INTER-RATER RELIABILITY REPORT")
    lines.append("=" * 66)
    lines.append(f"  Input:            {input_path}")
    lines.append(f"  Rows in file:     {total_in_file}")
    lines.append(f"  Rows reviewed:    {total_reviewed}")
    lines.append("")

    # Overall kappa
    kappa = _kappa_from_lists(y_llm, y_human)
    if kappa is None:
        lines.append("  Overall kappa: could not be computed (degenerate input).")
    else:
        interp = interpret_kappa(kappa)
        lines.append(f"  Overall Cohen's kappa: {kappa:.4f}  ({interp})")
        lines.append("")
        lines.append("  Kappa scale:")
        lines.append("    < 0.20  poor")
        lines.append("    0.20-0.40  fair")
        lines.append("    0.40-0.60  moderate")
        lines.append("    0.60-0.80  substantial")
        lines.append("    > 0.80  almost perfect")

    lines.append("")
    lines.append("-" * 66)
    lines.append("CONFUSION MATRIX")
    lines.append("-" * 66)
    lines.extend(_format_confusion_matrix(y_llm, y_human, all_labels))

    # ------------------------------------------------------------------
    # Per-configuration kappa
    # ------------------------------------------------------------------
    config_groups: dict[str, tuple[list[str], list[str]]] = defaultdict(
        lambda: ([], [])
    )
    for row, ll, hu in zip(reviewed, y_llm, y_human):
        config = row.get("configuration", "(unknown)").strip()
        config_groups[config][0].append(ll)
        config_groups[config][1].append(hu)

    lines.append("")
    lines.append("-" * 66)
    lines.append("PER-CONFIGURATION KAPPA")
    lines.append("-" * 66)

    for config in sorted(config_groups.keys()):
        ll_list, hu_list = config_groups[config]
        n = len(ll_list)
        if n < MIN_ROWS_FOR_CONFIG_KAPPA:
            lines.append(
                f"  {config}: n={n} (skipped — fewer than {MIN_ROWS_FOR_CONFIG_KAPPA} rows)"
            )
            continue
        k = _kappa_from_lists(ll_list, hu_list)
        if k is None:
            lines.append(f"  {config}: n={n}, kappa=N/A (degenerate)")
        else:
            lines.append(f"  {config}: n={n}, kappa={k:.4f} ({interpret_kappa(k)})")

    # ------------------------------------------------------------------
    # Disagreements
    # ------------------------------------------------------------------
    disagreements = [
        (row, ll, hu)
        for row, ll, hu in zip(reviewed, y_llm, y_human)
        if ll != hu
    ]

    lines.append("")
    lines.append("-" * 66)
    lines.append(f"DISAGREEMENTS ({len(disagreements)} of {total_reviewed} rows)")
    lines.append("-" * 66)

    if not disagreements:
        lines.append("  No disagreements found.")
    else:
        lines.append(
            f"  {'submission_id':<30} {'configuration':<30} {'LLM':<24} {'Human':<24}"
        )
        lines.append("  " + "-" * 110)
        for row, ll, hu in disagreements:
            sid    = row.get("submission_id", "").strip()[:29]
            config = row.get("configuration", "").strip()[:29]
            lines.append(f"  {sid:<30} {config:<30} {ll:<24} {hu:<24}")

    lines.append("")
    lines.append("=" * 66)

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    report_text = "\n".join(lines)
    print(report_text)

    DEFAULT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(DEFAULT_REPORT, "w", encoding="utf-8") as fh:
        fh.write(report_text)
        fh.write("\n")

    print(f"\nReport written: {DEFAULT_REPORT}")


if __name__ == "__main__":
    main()
