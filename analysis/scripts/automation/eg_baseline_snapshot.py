"""
eg_baseline_snapshot.py — Record EG values from callable implementations before extraction.

Run once before Step 1.1 is finalized. Saves results to eg_baseline_values.json.
mcmc_ensemble.py is handled via manual inspection (EG is inline, no callable function).
Delete this file after Step 1.1 verification passes.

EXECUTOR: verify ED_VOTES_PATH against a1_legal_baseline_2021_census.py / data_loader.py.
It must be the file with per-ED ndp and ucp vote columns, NOT the ensemble CSV.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

# EXECUTOR: substitute the correct path before running.
# Must have per-ED 'ndp' and 'ucp' columns (actual election results, not MCMC draws).
ED_VOTES_PATH = Path("data/...")  # fill in before running

ed_votes = pd.read_csv(ED_VOTES_PATH)
assert "ndp" in ed_votes.columns and "ucp" in ed_votes.columns, (
    f"Wrong file — ndp/ucp columns not found. Got: {list(ed_votes.columns)}"
)

results: dict[str, float] = {}

# Append scripts dir to path so direct imports work
_scripts = Path(__file__).resolve().parent.parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

import szat  # noqa: E402
results["szat"] = szat.compute_eg(ed_votes)

import szat_validate  # noqa: E402
results["szat_validate"] = szat_validate.compute_eg(ed_votes)

# NOTE: overlap_zone_diagnostic, chen_rodden_alberta, historical_eg_baseline
# use different threshold variants (see REMEDIATION_LOG.md 2026-05-09) and are
# NOT included in the snapshot — their local implementations are intentionally different.

# mcmc_ensemble.py: EG is inline in seat_results() — no callable function exists.
# Manual check required: read seat_results(), verify the inline formula matches
# eg_utils._ed_waste by inspection. Record result in REMEDIATION_LOG.md.
print("NOTE: mcmc_ensemble.py requires manual inspection — see REMEDIATION_LOG.md")

print(json.dumps(results, indent=2))
Path("eg_baseline_values.json").write_text(json.dumps(results, indent=2))

values = list(results.values())
if len(values) >= 2:
    max_diff = max(abs(a - b) for a in values for b in values)
    if max_diff > 1e-9:
        print(f"\nWARNING: implementations disagree — max diff = {max_diff:.2e}")
        print("Record in REMEDIATION_LOG.md before committing eg_utils.py.")
        sys.exit(1)
    print(f"\n{len(values)} callable implementations agree (max diff = {max_diff:.2e}). Safe to extract.")
