"""w01: all-ballots equivalent of data/outputs/iap_assembled_phase4c.json.
The election-day file came from analysis/scripts/phase4c_canonical_attribution.py --majority ... --map-key iap_2026_assembled,
whose score_candidate() calls me.build_va_graph(verbose=False) (election-day file) and me.score_exogenous_map.
This wrapper does the same with the all-ballots VA file. Rehearsal, provisional, not a registered result."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402

me = _a12.default_va_to_all_ballots()
va, _ = me.build_va_graph(verbose=False)
m = me.score_exogenous_map(va, _a12.MAP, id_col="EDName2025")
if m["coverage_pct"] < 0.98:
    sys.exit(f"coverage {m['coverage_pct']:.2%} below 98%")
out = {"iap_2026_assembled": m, "iap_2026_assembled_source": _a12.MAP.name, "name_col": "EDName2025",
       "scorer": "mcmc_ensemble.score_exogenous_map (canonical ensemble conventions), all-ballots VA file",
       "va_file": _a12.VA_ALL.name, "va_file_sha256": _a12.VA_ALL_SHA}
(_a12.OUT / "iap_assembled_phase4c_allballots.json").write_text(json.dumps(out, indent=2, default=float), encoding="utf-8")
print(f"{m['n_districts']} districts, coverage {m['coverage_pct']:.2%}; EG={m['efficiency_gap']:+.5f} "
      f"MM={m['mean_median']:+.5f} decl={m['declination']:+.5f} s50={m['seats_at_50_50']:.5f} ucp_seats={m.get('ucp_seats')}")
