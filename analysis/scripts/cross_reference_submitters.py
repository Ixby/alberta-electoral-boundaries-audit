"""
cross_reference_submitters.py
------------------------------
Cross-reference public submission sentiment against the minority commission's
stated rationales for contested boundary decisions (minority_rationales.csv).

For each rationale (R1–R17 or similar), this script:
  1. Maps the rationale to the sentiment configurations that bear on it
  2. Reports the distribution of submission sentiment (oppose/support/neutral)
  3. Computes a "submission alignment score" — fraction of taking-sides submissions
     that align with the commission's claimed public sentiment direction
  4. Flags rationales where submission sentiment contradicts the commission's claims

Input:
    data/outputs/quotes_verified.csv  (or fallback: submission_sentiment_llm_full_results.csv)
    data/outputs/minority_rationales.csv

Output:
    data/outputs/cross_reference_results.csv
    data/outputs/cross_reference_summary.json

Usage:
    python analysis/scripts/cross_reference_submitters.py

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SENTIMENT_CSV = ROOT / "data/outputs/quotes_verified.csv"
FALLBACK_SENTIMENT = ROOT / "data/outputs/submission_sentiment_llm_full_results.csv"
RATIONALES_CSV = ROOT / "data" / "reference" / "minority_rationales.csv"
OUTPUT_CSV = ROOT / "data/outputs/cross_reference_results.csv"
SUMMARY_JSON = ROOT / "data/outputs/cross_reference_summary.json"

# Map minority_rationales 'district' values to sentiment 'configuration' values.
# District names in rationales often match configuration names (or a substring).
RATIONALE_TO_CONFIG: dict[str, list[str]] = {
    "Calgary-Nolan Hill-Cochrane": ["Calgary-Nolan Hill-Cochrane hybrid"],
    "Calgary-Peigan-Chestermere": ["Chestermere merging with Calgary"],
    "Calgary-Airdrie": ["Airdrie 4-way split"],
    "Rocky Mountain House-Banff": ["Rocky Mountain House-Banff Park hybrid"],
    "Red Deer-Lacombe-Sylvan Lake": [
        "Red Deer hybrid ridings (Blackfalds, Sylvan Lake, Innisfail)"
    ],
    "Cochrane-Springbank": ["Calgary-Nolan Hill-Cochrane hybrid"],
}

SUPPORT_LABEL = "Active Support"
OPPOSE_LABEL = "Active Opposition"
NEUTRAL_LABEL = "Neutral/Contextual"


def classify_alignment(submission_sentiment: str, rationale_verdict: str) -> str:
    """Return alignment between submission and commission rationale verdict.

    A commission rationale marked 'SUPPORTS' or 'PARTIALLY SUPPORTS' implies
    the commission claimed public support for that boundary choice. A submission
    classifying as Active Support would ALIGN; Active Opposition would CONTRADICT.
    """
    verdict_upper = str(rationale_verdict).upper()
    if "CONTRADICT" in verdict_upper or "FAIL" in verdict_upper:
        # Commission itself said the rationale contradicts the claimed COI —
        # so Active Opposition from public aligns with the audit's finding.
        if submission_sentiment == OPPOSE_LABEL:
            return "ALIGNS_WITH_AUDIT"
        elif submission_sentiment == SUPPORT_LABEL:
            return "CONTRA_AUDIT"
        else:
            return "NEUTRAL"
    elif "SUPPORT" in verdict_upper:
        # Commission claims public/evidence support: Active Support from public aligns.
        if submission_sentiment == SUPPORT_LABEL:
            return "ALIGNS_WITH_COMMISSION"
        elif submission_sentiment == OPPOSE_LABEL:
            return "CONTRA_COMMISSION"
        else:
            return "NEUTRAL"
    else:
        return "INCONCLUSIVE"


def main():
    # Load sentiment data
    sentiment_path = SENTIMENT_CSV if SENTIMENT_CSV.exists() else FALLBACK_SENTIMENT
    print(f"Loading sentiment from {sentiment_path.name}...")
    sent_df = pd.read_csv(sentiment_path, on_bad_lines="skip")
    print(f"  {len(sent_df)} rows.")

    # Load rationales
    print(f"Loading rationales from {RATIONALES_CSV.name}...")
    rat_df = pd.read_csv(RATIONALES_CSV)
    print(f"  {len(rat_df)} rationales.")

    results = []
    for _, rat in rat_df.iterrows():
        rationale_id = rat["rationale_id"]
        district = str(rat["district"])
        verdict = str(rat["verdict"])

        # Find matching configurations for this district
        configs = []
        for key, val_configs in RATIONALE_TO_CONFIG.items():
            if key.lower() in district.lower() or district.lower() in key.lower():
                configs.extend(val_configs)

        if not configs:
            # Fuzzy match: check if any config name appears in the district string
            for config in sent_df["configuration"].unique():
                config_core = config.split("(")[0].strip().lower()
                if config_core in district.lower() or district.lower() in config_core:
                    configs.append(config)

        if not configs:
            results.append({
                "rationale_id": rationale_id,
                "district": district,
                "verdict": verdict,
                "configs_matched": None,
                "n_oppose": 0,
                "n_support": 0,
                "n_neutral": 0,
                "n_total": 0,
                "oppose_pct": None,
                "support_pct": None,
                "alignment_summary": "NO_CONFIG_MATCH",
            })
            continue

        config_sent = sent_df[sent_df["configuration"].isin(configs)]
        n_oppose = (config_sent["classification"] == OPPOSE_LABEL).sum()
        n_support = (config_sent["classification"] == SUPPORT_LABEL).sum()
        n_neutral = (config_sent["classification"] == NEUTRAL_LABEL).sum()
        n_total = len(config_sent)
        n_taking_sides = n_oppose + n_support

        oppose_pct = round(n_oppose / n_taking_sides * 100, 1) if n_taking_sides > 0 else None
        support_pct = round(n_support / n_taking_sides * 100, 1) if n_taking_sides > 0 else None

        # Alignment: majority taking-sides direction vs. commission verdict
        if n_taking_sides == 0:
            alignment = "NO_TAKING_SIDES"
        elif n_oppose > n_support:
            alignment = classify_alignment(OPPOSE_LABEL, verdict)
        elif n_support > n_oppose:
            alignment = classify_alignment(SUPPORT_LABEL, verdict)
        else:
            alignment = "TIED"

        results.append({
            "rationale_id": rationale_id,
            "district": district,
            "verdict": verdict,
            "configs_matched": "; ".join(configs),
            "n_oppose": int(n_oppose),
            "n_support": int(n_support),
            "n_neutral": int(n_neutral),
            "n_total": int(n_total),
            "oppose_pct": oppose_pct,
            "support_pct": support_pct,
            "alignment_summary": alignment,
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)

    # Summary statistics
    matched = out_df[out_df["alignment_summary"] != "NO_CONFIG_MATCH"]
    contra_commission = (out_df["alignment_summary"] == "CONTRA_COMMISSION").sum()
    contra_audit = (out_df["alignment_summary"] == "CONTRA_AUDIT").sum()
    aligns_commission = (out_df["alignment_summary"] == "ALIGNS_WITH_COMMISSION").sum()
    aligns_audit = (out_df["alignment_summary"] == "ALIGNS_WITH_AUDIT").sum()

    summary = {
        "total_rationales": len(rat_df),
        "rationales_with_config_match": int(len(matched)),
        "aligns_with_commission": int(aligns_commission),
        "contra_commission": int(contra_commission),
        "aligns_with_audit_finding": int(aligns_audit),
        "contra_audit": int(contra_audit),
        "no_taking_sides": int((out_df["alignment_summary"] == "NO_TAKING_SIDES").sum()),
        "top_opposed_configs": (
            out_df.assign(n_taking_sides=lambda x: x["n_oppose"] + x["n_support"])
            .pipe(lambda x: x[x["n_taking_sides"] > 0])
            .nlargest(5, "n_oppose")[["district", "n_oppose", "oppose_pct", "verdict"]]
            .to_dict(orient="records")
            if "n_oppose" in out_df.columns else []
        ),
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2)

    print("\nCross-reference results:")
    print(f"  Rationales with config match: {len(matched)}/{len(rat_df)}")
    print(f"  Submission sentiment aligns with commission: {aligns_commission}")
    print(f"  Submission sentiment contradicts commission: {contra_commission}")
    print(f"  Submission sentiment aligns with audit finding: {aligns_audit}")

    print("\nPer-rationale results:")
    for _, row in out_df.iterrows():
        print(
            f"  {row['rationale_id']:4s} {row['district'][:30]:<30} "
            f"oppose={row['n_oppose']:3d} support={row['n_support']:3d} "
            f"| {row['alignment_summary']}"
        )

    print(f"\nOutput: {OUTPUT_CSV.relative_to(ROOT)}")
    print(f"Summary: {SUMMARY_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
