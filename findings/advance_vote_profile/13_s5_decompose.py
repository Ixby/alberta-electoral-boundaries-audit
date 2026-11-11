"""Break the S5 neighbour-drain score into the district pairs it is made of.

The drain score (analysis/scripts/drain_label_shuffle_null.drain_score) is a sum over pairs of
neighbouring districts X -> Y that the same party lost:
    max(0, s_X - 0.15) * max(0, 0.05 - m_Y)
where s_X is X's surplus-vote rate and m_Y is Y's winning margin. This script lists every pair
with a non-zero term, for each map on each vote file, and checks that the terms add up to the
score the registered compute_S5_drain returns. It changes no registered result.

Vote files: election day; all ballots under Amendment 12's rule; all ballots under rule P.
Output: outputs/s5_decomposition.json
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # works under python -I
import warnings

import geopandas as gpd

from _common import ROOT, VA_M0, VA_P, write_json

warnings.filterwarnings("ignore")
_sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
import run_structural_battery as rsb  # noqa: E402
from neighbour_drain_adjacency import (  # noqa: E402
    S_THRESHOLD, M_THRESHOLD, _score_canonical_map_strict, build_adjacency, compute_ed_metrics,
    detect_chain_signals,
)

VA_ED = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"
VOTES = {"election_day": VA_ED, "all_ballots_amendment_12": VA_M0, "all_ballots_rule_p": VA_P}
SHP = {
    "majority_89": ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
    "minority_89": ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
    "panel_v3_91": ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg",
    "para167_91": ROOT / "findings/iap_para167/para167_map.gpkg",
}


def decompose(shp, va):
    votes, col = _score_canonical_map_strict(va, shp, label="candidate")
    ed = compute_ed_metrics(votes)
    und, _, _ = build_adjacency(gpd.read_file(shp), col)
    pairs = detect_chain_signals(ed, und)
    look = ed.set_index("ed").to_dict("index")
    terms = []
    for _, r in pairs.iterrows():
        x, y = look[r["X"]], look[r["Y"]]
        if x["losing_party"] != y["losing_party"]:
            continue
        t = max(0.0, x["s"] - S_THRESHOLD) * max(0.0, M_THRESHOLD - y["m"])
        if t > 0:
            terms.append({"packed": r["X"], "close": r["Y"], "term": t,
                          "surplus_rate_packed": float(x["s"]), "margin_close": float(y["m"])})
    terms.sort(key=lambda t: -t["term"])
    total = sum(t["term"] for t in terms)
    for t in terms:
        t["share_of_score"] = t["term"] / total if total else None
    return {"drain_score": total, "pairs_with_nonzero_term": len(terms),
            "close_districts": sorted({t["close"] for t in terms}), "terms": terms}


def main():
    out = {"maps": {}}
    for m, shp in SHP.items():
        out["maps"][m] = {}
        for rule, path in VOTES.items():
            va = gpd.read_file(path)
            d = decompose(shp, va)
            reg = rsb.compute_S5_drain(shp, path)["drain_score"]
            assert reg is not None and abs(reg - d["drain_score"]) < 1e-12, (m, rule, reg, d["drain_score"])
            out["maps"][m][rule] = d
    order = {rule: ("majority_higher" if out["maps"]["majority_89"][rule]["drain_score"] >
                    out["maps"]["minority_89"][rule]["drain_score"] else "minority_higher") for rule in VOTES}
    out["commission_maps_order_by_vote_file"] = order
    write_json("s5_decomposition.json", out, __file__, list(VOTES.values()) + list(SHP.values()),
               extra={"thresholds": {"surplus_rate": S_THRESHOLD, "margin": M_THRESHOLD},
                      "check": "each map's terms sum to compute_S5_drain's score to 1e-12"})
    for m in out["maps"]:
        for rule in VOTES:
            d = out["maps"][m][rule]
            top = d["terms"][0] if d["terms"] else None
            print(m, rule, round(d["drain_score"], 5), d["pairs_with_nonzero_term"], "pairs",
                  (top["packed"], top["close"], round(top["share_of_score"], 2), round(top["margin_close"], 4)) if top else "")
    print(order)


if __name__ == "__main__":
    main()
