"""Threshold lines under rule P, for Amendment 14, Part 3 (exploratory, not registered).

P1's line is the 95th percentile of the canonical ensemble's efficiency gap, taken from the replayed
canonical chains on the P file that passed their check (replay_check_p.json). The rule is the same
as Amendment 12, Part 3, which set +1.394% from the M0 replay; this script reproduces that value first
as a check of the rule. The same percentile is given for mean-median, declination and seats at 50/50,
with the count of plans whose efficiency gap is at or above the minority map's P value.

S5's line is the midpoint of the two commission maps' drain scores, computed by run_structural_battery's
own compute_S5_drain (imported, not edited) with the vote file swapped to P. The S5 drain is a score of
each real map, not a column of the ensemble chains, so it is not part of the replay. The script first
reproduces Amendment 12's all-ballots midpoint (0.0019398) from the M0 file.

Writes outputs/thresholds_p.json. Run from the repository root:
  python -I findings/advance_vote_profile/11_thresholds_p.py
Needs STAMP_MODEL and STAMP_EFFORT in the environment (read by _common.stamp()).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd

from _common import OUT, ROOT, VA_M0, VA_P, rel, write_json


STATS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
CHECK = OUT / "replay_check_p.json"
RANKS = OUT / "ensemble_ranks_p.json"
M0_P1 = 0.01394   # Amendment 12, Part 3
M0_S5 = 0.0019398  # Amendment 12, Part 3


def chains(folder, idx):
    return pd.concat([pd.read_csv(ROOT / folder / f"chain{i}_samples.csv", usecols=STATS) for i in idx], ignore_index=True)


def main():
    check = json.loads(CHECK.read_text(encoding="utf-8"))
    passed = sorted(r["chain"] for r in check["chains"] if r["set"] == "canonical" and r["status"] == "match")
    assert passed == [0, 1, 2, 3], passed

    m0 = chains("data/simulation_checkpoints_allballots", range(4))
    m0_p1 = float(np.percentile(m0["efficiency_gap"], 95))
    assert round(m0_p1, 5) == M0_P1, m0_p1

    p = chains("data/simulation_checkpoints_allballots_p", passed)
    assert len(p) == 1_010_000, len(p)
    p95 = {s: float(np.percentile(p[s], 95)) for s in STATS}

    ranks = json.loads(RANKS.read_text(encoding="utf-8"))
    canon = next(s for s in ranks["sets"] if s["set"] == "canonical")
    k = "ranks" if "ranks" in canon else "results"
    minority_eg = next(x["value_p"] for x in canon[k] if x["map"] == "minority_89" and x["statistic"] == "efficiency_gap")
    exceed = int((p["efficiency_gap"] >= minority_eg).sum())

    sys.path.insert(0, str(ROOT / "analysis/scripts"))
    import run_structural_battery as rsb
    shp = {m: ROOT / f"data/shapefiles/canonical/ea_{m}_2026_eds.gpkg" for m in ("majority", "minority")}
    d_m0 = {m: rsb.compute_S5_drain(f, VA_M0)["drain_score"] for m, f in shp.items()}
    m0_mid = (d_m0["majority"] + d_m0["minority"]) / 2
    assert round(m0_mid, 7) == M0_S5, m0_mid
    d_p = {m: rsb.compute_S5_drain(f, VA_P)["drain_score"] for m, f in shp.items()}
    p_mid = (d_p["majority"] + d_p["minority"]) / 2

    payload = {
        "p1_line": {"rule": "95th percentile (numpy default, linear) of the canonical ensemble's efficiency gap",
                    "chains": passed, "plans": len(p), "value": p95["efficiency_gap"],
                    "check_m0_reproduced": m0_p1},
        "canonical_p95": p95,
        "minority_exceedance": {"minority_efficiency_gap_p": minority_eg, "rule": "plans with efficiency_gap >= minority value",
                                "count": exceed, "of": len(p)},
        "s5_line": {"rule": "midpoint of the commission maps' drain scores (Amendment 5, Part 7), compute_S5_drain with the P vote file",
                    "majority_drain": d_p["majority"], "minority_drain": d_p["minority"], "value": p_mid,
                    "flag_fires": "below the line",
                    "check_m0_reproduced": {"majority_drain": d_m0["majority"], "minority_drain": d_m0["minority"], "midpoint": m0_mid},
                    "note": "drain is a score of each real map, not a column of the ensemble chains; it is not part of the replay"},
    }
    inputs = [CHECK, RANKS, VA_P, VA_M0, *shp.values(),
              *[ROOT / f"data/simulation_checkpoints_allballots_p/chain{i}_samples.csv" for i in passed]]
    write_json("thresholds_p.json", payload, __file__, inputs)
    print(json.dumps(payload, indent=1))


if __name__ == "__main__":
    main()
