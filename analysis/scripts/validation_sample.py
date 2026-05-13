"""
validation_sample.py
---------------------
Draw a stratified random sample from the classified submissions for human
inter-rater reliability (IRR) testing.

Stratification: sample proportionally across {configuration × classification}
cells to ensure coverage of all 7 configurations and all 3 classification
labels (Active Opposition, Active Support, Neutral/Contextual).

Output format is structured for direct human annotation: one row per item,
with the submission text excerpt and a blank column for the human rater's label.

Seed derivation (same drand beacon as other audit analyses):
  randomness: 5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8
  salt: "alberta-audit-irr-sample"
  seed: derived

Usage:
    python analysis/scripts/validation_sample.py [--n 60]

Outputs:
    data/outputs/irr_validation_sample.csv  -- sample for human annotation
    data/outputs/irr_sampling_report.json   -- stratification details

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_CSV = ROOT / "data/outputs/quotes_verified.csv"
FALLBACK_CSV = ROOT / "data/outputs/submission_sentiment_llm_full_results.csv"
TEXT_DIR = ROOT / ".temp" / "submissions" / "text"
OUTPUT_CSV = ROOT / "data/outputs/irr_validation_sample.csv"
REPORT_JSON = ROOT / "data/outputs/irr_sampling_report.json"

# Derive seed from drand beacon (round 6099592, same as robustness runs)
_RANDOMNESS = "5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8"
_h = hashlib.sha256(f"alberta-audit-irr-sample:{_RANDOMNESS}".encode()).hexdigest()
SEED = int(_h[:8], 16)

LABELS = ["Active Opposition", "Active Support", "Neutral/Contextual"]
ANNOTATION_PROMPT = (
    "Based on the text excerpt below, classify this submission's stance on the "
    "named boundary configuration. Choose one of: Active Opposition / Active Support / "
    "Neutral/Contextual / Unrelated."
)


def load_source_excerpt(submission_id: str, max_chars: int = 600) -> str:
    """Return the first max_chars characters of the source text, stripped."""
    path = TEXT_DIR / f"{submission_id}.txt"
    if not path.exists():
        return "[source text not available]"
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return text[:max_chars].strip()
    except Exception:
        return "[source text read error]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=60,
                        help="Total sample size (default 60)")
    args = parser.parse_args()

    # Load input
    input_path = INPUT_CSV if INPUT_CSV.exists() else FALLBACK_CSV
    print(f"Loading from {input_path.name}...")
    df = pd.read_csv(input_path, on_bad_lines="skip")

    # Filter to classified rows (exclude Neutral if needed; keep all three labels)
    classified = df[df["classification"].isin(LABELS)].copy()
    print(f"  {len(classified)} classified rows across "
          f"{classified['configuration'].nunique()} configurations.")

    # Stratified sampling: proportional within each config × classification cell
    rng = np.random.default_rng(SEED)
    strata = classified.groupby(["configuration", "classification"])

    cell_counts = strata.size().reset_index(name="cell_n")
    total_classified = len(classified)
    cell_counts["target_n"] = (
        (cell_counts["cell_n"] / total_classified * args.n)
        .apply(np.floor).astype(int).clip(lower=1)
    )
    # Distribute remaining slots to largest cells
    allocated = cell_counts["target_n"].sum()
    remainder = args.n - allocated
    if remainder > 0:
        top_cells = cell_counts.nlargest(remainder, "cell_n").index
        cell_counts.loc[top_cells, "target_n"] += 1

    sampled_rows = []
    for _, cell_info in cell_counts.iterrows():
        config = cell_info["configuration"]
        label = cell_info["classification"]
        n_draw = int(min(cell_info["target_n"], cell_info["cell_n"]))
        cell_df = classified[
            (classified["configuration"] == config)
            & (classified["classification"] == label)
        ]
        draw = cell_df.sample(n=n_draw, random_state=int(rng.integers(0, 2**31)))
        sampled_rows.append(draw)

    sample = pd.concat(sampled_rows, ignore_index=True).sample(
        frac=1, random_state=SEED
    )  # shuffle to remove ordering bias

    # Attach source text excerpt
    print("Attaching source text excerpts...")
    sample["source_excerpt"] = sample["submission_id"].apply(load_source_excerpt)

    # Build annotation-ready output
    annotation_df = sample[[
        "submission_id", "configuration", "classification",
        "exact_quote", "source_excerpt", "reasoning",
    ]].copy()
    annotation_df.insert(0, "item_id", range(1, len(annotation_df) + 1))
    annotation_df["human_label"] = ""  # blank for annotator
    annotation_df["annotator_notes"] = ""
    annotation_df["annotation_prompt"] = ANNOTATION_PROMPT

    annotation_df.to_csv(OUTPUT_CSV, index=False)

    # Sampling report
    report = {
        "seed": SEED,
        "seed_salt": "alberta-audit-irr-sample",
        "drand_round": 6099592,
        "total_sample_n": len(annotation_df),
        "input_file": input_path.name,
        "total_classified_rows": total_classified,
        "stratification": cell_counts.to_dict(orient="records"),
        "annotation_prompt": ANNOTATION_PROMPT,
        "instructions": (
            "Fill in 'human_label' for each row. Valid values: "
            "Active Opposition, Active Support, Neutral/Contextual, Unrelated. "
            "After annotation, run compute_kappa.py against this file."
        ),
    }
    with open(REPORT_JSON, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nSample drawn: {len(annotation_df)} items "
          f"(target={args.n}, seed={SEED})")
    print(f"Output: {OUTPUT_CSV.relative_to(ROOT)}")
    print(f"Report: {REPORT_JSON.relative_to(ROOT)}")
    print("\nNext step: open irr_validation_sample.csv and fill in the 'human_label' "
          "column for each row, then run compute_kappa.py.")


if __name__ == "__main__":
    main()
