"""
compute_kappa.py
-----------------
Compute Cohen's kappa between LLM classifications and human annotations
for inter-rater reliability (IRR).

Requires:
    data/outputs/irr_validation_sample.csv  -- with human_label column filled in
    (output of validation_sample.py after human annotation)

Outputs:
    data/outputs/irr_kappa_results.json  -- kappa, confusion matrix, per-class stats

Usage:
    python analysis/scripts/compute_kappa.py [--input PATH]

Interpretation thresholds (Landis & Koch 1977):
    kappa < 0.20 = Slight
    0.20 – 0.40 = Fair
    0.40 – 0.60 = Moderate
    0.60 – 0.80 = Substantial
    0.80 – 1.00 = Almost perfect

Acceptable for publication: kappa >= 0.60 (Substantial or better).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "data/outputs/irr_validation_sample.csv"
OUTPUT_JSON = ROOT / "data/outputs/irr_kappa_results.json"

LABELS = ["Active Opposition", "Active Support", "Neutral/Contextual"]
LABEL_MAP = {
    "active opposition": "Active Opposition",
    "active support": "Active Support",
    "neutral/contextual": "Neutral/Contextual",
    "neutral": "Neutral/Contextual",
    "contextual": "Neutral/Contextual",
}


def normalize_label(label: str) -> str | None:
    """Normalize label spelling variations."""
    if not isinstance(label, str):
        return None
    cleaned = label.strip().lower()
    return LABEL_MAP.get(cleaned, label.strip())


def cohen_kappa(y1: list[str], y2: list[str], labels: list[str]) -> dict:
    """Compute Cohen's kappa and return detailed statistics."""
    n = len(y1)
    label_index = {l: i for i, l in enumerate(labels)}
    k = len(labels)

    # Build confusion matrix
    conf = np.zeros((k, k), dtype=int)
    for a, b in zip(y1, y2):
        i = label_index.get(a)
        j = label_index.get(b)
        if i is not None and j is not None:
            conf[i, j] += 1

    po = np.trace(conf) / n  # observed agreement

    # Expected agreement
    row_marginals = conf.sum(axis=1) / n
    col_marginals = conf.sum(axis=0) / n
    pe = float(np.dot(row_marginals, col_marginals))

    kappa = (po - pe) / (1 - pe) if pe < 1 else 0.0

    # Per-class precision/recall
    per_class = {}
    for label in labels:
        i = label_index[label]
        tp = conf[i, i]
        fp = conf[:, i].sum() - tp
        fn = conf[i, :].sum() - tp
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        per_class[label] = {
            "precision": round(float(precision), 3),
            "recall": round(float(recall), 3),
            "f1": round(2 * precision * recall / max(precision + recall, 1e-9), 3),
            "support": int(conf[i, :].sum()),
        }

    return {
        "kappa": round(float(kappa), 4),
        "po": round(float(po), 4),
        "pe": round(float(pe), 4),
        "n_items": n,
        "confusion_matrix": conf.tolist(),
        "labels": labels,
        "per_class": per_class,
    }


def interpret_kappa(kappa: float) -> str:
    if kappa < 0.20:
        return "Slight"
    elif kappa < 0.40:
        return "Fair"
    elif kappa < 0.60:
        return "Moderate"
    elif kappa < 0.80:
        return "Substantial"
    else:
        return "Almost perfect"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT),
                        help="Path to annotated IRR sample CSV")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} not found.")
        print("Run validation_sample.py first, annotate the output, then re-run.")
        return

    print(f"Loading annotated sample from {input_path.name}...")
    df = pd.read_csv(input_path)

    # Check for required columns
    if "human_label" not in df.columns:
        print("ERROR: 'human_label' column not found. Please annotate the sample first.")
        return

    # Filter to rows with human labels
    annotated = df[df["human_label"].notna() & (df["human_label"].str.strip() != "")]
    n_annotated = len(annotated)
    n_total = len(df)
    print(f"  {n_annotated}/{n_total} items annotated.")

    if n_annotated == 0:
        print("ERROR: No annotations found. Please fill in the 'human_label' column.")
        return

    if n_annotated < 20:
        print(f"WARNING: Only {n_annotated} items annotated. Kappa may be unreliable "
              f"(recommend >= 30 items).")

    # Normalize labels
    llm_labels = annotated["classification"].apply(normalize_label).tolist()
    human_labels = annotated["human_label"].apply(normalize_label).tolist()

    # Filter to valid label pairs (exclude Unrelated or unknown labels)
    valid_pairs = [
        (l, h) for l, h in zip(llm_labels, human_labels)
        if l in LABELS and h in LABELS
    ]
    if len(valid_pairs) < n_annotated:
        excluded = n_annotated - len(valid_pairs)
        print(f"  {excluded} items excluded (Unrelated or unknown label).")

    if not valid_pairs:
        print("ERROR: No valid label pairs found.")
        return

    y_llm, y_human = zip(*valid_pairs)
    print(f"\nComputing kappa on {len(valid_pairs)} items...")

    stats = cohen_kappa(list(y_llm), list(y_human), LABELS)
    stats["interpretation"] = interpret_kappa(stats["kappa"])
    stats["acceptable_for_publication"] = stats["kappa"] >= 0.60

    print(f"\nCohen's kappa: {stats['kappa']:.4f} ({stats['interpretation']})")
    print(f"Observed agreement (po): {stats['po']:.4f}")
    print(f"Expected agreement (pe): {stats['pe']:.4f}")
    print(f"Acceptable for publication (kappa >= 0.60): "
          f"{'YES' if stats['acceptable_for_publication'] else 'NO — review needed'}")

    print("\nPer-class statistics:")
    for label, pcs in stats["per_class"].items():
        print(f"  {label[:25]:<25} precision={pcs['precision']:.3f} "
              f"recall={pcs['recall']:.3f} f1={pcs['f1']:.3f} n={pcs['support']}")

    with open(OUTPUT_JSON, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"\nResults: {OUTPUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
