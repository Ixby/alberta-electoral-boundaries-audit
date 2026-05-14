#!/usr/bin/env python
"""
Synthetic Gerrymander Detection (Implementation)
Extracts extreme outliers from the 100k simulated maps to act as synthetic "known bads"
and passes them through the test battery to prove it triggers the alarm.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_SAMPLES = DATA_DIR / "simulated_ensemble_raw_samples_100k.csv"

def main():
    raise NotImplementedError(
        "STUB — DO NOT RUN. This script is self-validating by design: it uses the "
        "ensemble's own min/max EG values as test inputs, so the alarm will always "
        "trigger (ensemble extremes are guaranteed outliers). The meaningful test is "
        "whether the *actual proposed maps* (majority_2026, minority_2026) trigger the "
        "detection threshold, not whether constructed extremes do. Additionally, the "
        "baseline expected median is hardcoded as -0.02, but the canonical 2019 enacted "
        "EG is +0.0241 (from simulation_real_map_scores_canonical.json). The script "
        "needs a complete redesign to load proposed-map EG values from the canonical "
        "JSON and test those against ensemble percentile thresholds."
    )
    if not RAW_SAMPLES.exists():
        print(f"WARNING: Simulated raw samples not found at {RAW_SAMPLES.name}")
        print("Gracefully degrading: Simulating extreme map generation.")
        synthetic_ucp_eg = -0.15
        synthetic_ndp_eg = 0.10
    else:
        print(f"Loading MCMC raw samples from {RAW_SAMPLES.name}...")
        df = pd.read_csv(RAW_SAMPLES)
        synthetic_ucp_eg = df['efficiency_gap'].min()
        synthetic_ndp_eg = df['efficiency_gap'].max()

    print(f"\nExtracted Synthetic Extreme Maps:")
    print(f"  Max UCP Gerrymander EG: {synthetic_ucp_eg:+.4f}")
    print(f"  Max NDP Gerrymander EG: {synthetic_ndp_eg:+.4f}")

    print("\nRunning test battery against Synthetic Extremes...")
    # Baseline expected median is ~-0.02
    threshold = 0.05
    if synthetic_ucp_eg < -0.02 - threshold:
        print(f"  ✓ Battery correctly flagged Max UCP Map as GERRYMANDER_UCP")
    if synthetic_ndp_eg > -0.02 + threshold:
        print(f"  ✓ Battery correctly flagged Max NDP Map as GERRYMANDER_NDP")

if __name__ == "__main__":
    main()
