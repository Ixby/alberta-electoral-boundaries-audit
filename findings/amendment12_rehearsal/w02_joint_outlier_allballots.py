"""w02: joint_outlier_score_canonical.run_candidate against the all-ballots canonical ensemble.
Overrides ENSEMBLE_CSV and CONVERGENCE_JSON (and recomputes N_EFF_CONSERVATIVE from the latter). Rehearsal, provisional."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402
import joint_outlier_score_canonical as j  # noqa: E402

D = _a12.ROOT / "data/outputs"
j.ENSEMBLE_CSV = D / "simulated_ensemble_raw_samples_allballots.csv"
j.CONVERGENCE_JSON = D / "simulation_convergence_diagnostics_allballots.json"
j.N_EFF_CONSERVATIVE = j._load_n_eff_conservative()
# mahalanobis_pvalue_neff_adjusted binds n_eff as a default argument at import (the election-day value);
# run_candidate relies on that default, so rebind it or the F-test silently uses the old n_eff.
j.mahalanobis_pvalue_neff_adjusted.__defaults__ = (j.N_EFF_CONSERVATIVE,)
_a12.noop_logger(j)
print("n_eff used:", j.N_EFF_CONSERVATIVE, "| ensemble:", j.ENSEMBLE_CSV.name)
j.run_candidate(_a12.OUT / "iap_assembled_phase4c_allballots.json", "iap_2026_assembled",
                _a12.OUT / "joint_outlier_allballots.json")
