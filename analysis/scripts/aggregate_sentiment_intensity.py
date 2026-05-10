"""
aggregate_sentiment_intensity.py

Aggregates sentiment intensity scores by configuration to compute
the weighted-net intensity metrics for §5.9.4.6.

Input: data/outputs/sentiment_intensity_scores.csv (from sentiment_intensity_score.py)
Output: data/outputs/intensity_summary_table.csv + display to stdout
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = ROOT / "data"
INPUT_CSV = DATA_DIR / "outputs" / "sentiment_intensity_scores.csv"
OUTPUT_CSV = DATA_DIR / "outputs" / "intensity_summary_table.csv"

def main():
    if not INPUT_CSV.exists():
        print(f"ERROR: {INPUT_CSV} not found")
        sys.exit(1)
    
    by_config = defaultdict(lambda: {
        "opposition_sum": 0,
        "support_sum": 0,
        "opposition_count": 0,
        "support_count": 0,
    })
    
    with INPUT_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("classification") or not row.get("intensity"):
                continue

            config = row["configuration"]
            try:
                intensity = int(row["intensity"])
            except (ValueError, TypeError):
                continue
            classification = row["classification"]

            if classification == "Active Opposition":
                by_config[config]["opposition_sum"] += intensity
                by_config[config]["opposition_count"] += 1
            elif classification == "Active Support":
                by_config[config]["support_sum"] += intensity
                by_config[config]["support_count"] += 1
    
    # Compute weighted-net and sort
    results = []
    for config, stats in by_config.items():
        opp_sum = stats["opposition_sum"]
        sup_sum = stats["support_sum"]
        total_count = stats["opposition_count"] + stats["support_count"]
        
        # Weighted net: (support_sum - opposition_sum)
        weighted_net = sup_sum - opp_sum
        
        # Direction: which dominates
        if sup_sum > opp_sum:
            direction = "Net supported"
        elif opp_sum > sup_sum:
            direction = "Opposed"
        else:
            direction = "Balanced"
        
        results.append({
            "configuration": config,
            "opposition_count": stats["opposition_count"],
            "support_count": stats["support_count"],
            "opposition_sum": opp_sum,
            "support_sum": sup_sum,
            "total_count": total_count,
            "weighted_net": weighted_net,
            "direction": direction,
        })
    
    # Sort by weighted_net ascending (most opposed first)
    results.sort(key=lambda x: x["weighted_net"])
    
    # Display
    print(f"\n=== Intensity-Weighted Summary ({len(results)} configurations) ===\n")
    print(f"{'Configuration':<50} {'Opp':>3} {'Sup':>3} {'Weighted-Net':>12} {'Direction':<20}")
    print("-" * 90)
    
    for r in results:
        config_short = r["configuration"][:48]
        print(f"{config_short:<50} {r['opposition_count']:>3} {r['support_count']:>3} "
              f"{r['weighted_net']:>12} {r['direction']:<20}")
    
    # Write output CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "configuration", "opposition_count", "support_count", "total_count",
            "opposition_sum", "support_sum", "weighted_net", "direction"
        ])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nOutput written to: {OUTPUT_CSV}")
    print(f"Processed {len(results)} configurations across {sum(r['total_count'] for r in results)} rows.")

if __name__ == "__main__":
    main()
