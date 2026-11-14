# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
local_targeting.py

Runs preregistration/local_targeting_2026-11-07.md: (A) were competitive majority divisions more
likely to be changed by the panel; (B) which way did changes move margins; (C) where did moved
voters' NDP votes go. All ballots primary. Unregistered. Describes, does not show intent.

Usage: python -W ignore findings/local_targeting/local_targeting.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.stats import binomtest, fisher_exact

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "findings/packing_cracking"))
from real_maps import MAPS, assign  # noqa: E402

ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
EDAY = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
NEAR = 0.10


def margins(lab, u, n):
    t = pd.DataFrame({"d": lab, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
    return (t.n - t.u) / (t.n + t.u)


def cat(m):
    return np.where(m > 0, "ndp_won", np.where(m > -NEAR, "ndp_near", "ndp_far"))


def main():
    b = gpd.read_file(EDAY).to_crs(3400)
    pts = b[["geometry"]].copy()
    pts["geometry"] = b.geometry.representative_point()
    P = assign(pts, *MAPS["panel"]).to_numpy()
    M = assign(pts, *MAPS["majority"]).to_numpy()
    v = gpd.read_file(ALL, ignore_geometry=True)
    u, n = v.va_ucp.to_numpy(float), v.va_ndp.to_numpy(float)
    pop = pd.read_csv(ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx")["pop_2021"]
    vp = pd.Series(b.index.map(pop).values).fillna(0.0).clip(lower=1.0).to_numpy()
    mM, mP = margins(M, u, n), margins(P, u, n)

    # A
    sets_P = {d: frozenset(np.where(P == d)[0]) for d in set(P)}
    same = {frozenset(np.where(M == d)[0]) for d in set(M)} & set(sets_P.values())
    changed = pd.Series({d: frozenset(np.where(M == d)[0]) not in same for d in mM.index})
    comp = mM.abs() < NEAR
    ndp = mM > 0
    A = {}
    for name, g in (("competitive_vs_safe", comp), ("ndp_won_vs_ucp_won", ndp)):
        tab = [[int((changed & g).sum()), int((~changed & g).sum())], [int((changed & ~g).sum()), int((~changed & ~g).sum())]]
        odds, p = fisher_exact(tab)
        A[name] = {"table [[changed, unchanged] in group, [changed, unchanged] outside]": tab,
                   "rate_in_group": round(tab[0][0] / sum(tab[0]), 3), "rate_outside": round(tab[1][0] / sum(tab[1]), 3),
                   "odds_ratio": None if not np.isfinite(odds) else round(float(odds), 3), "p_fisher_two_sided": round(float(p), 4)}
    A["changed_majority_divisions"] = sorted(changed[changed].index)

    # B
    pairs = []
    for d in sorted(set(P)):
        if sets_P[d] in same:
            continue
        idx = np.where(P == d)[0]
        src = pd.Series(vp[idx]).groupby(M[idx]).sum().idxmax()
        pairs.append({"panel": d, "majority_source": src, "margin_majority": round(float(mM[src]), 4),
                      "margin_panel": round(float(mP[d]), 4), "shift_toward_ndp": round(float(mP[d] - mM[src]), 4)})
    close = [q for q in pairs if abs(q["margin_majority"]) < NEAR or abs(q["margin_panel"]) < NEAR]
    to_ucp = sum(q["shift_toward_ndp"] < 0 for q in close)
    to_ndp = sum(q["shift_toward_ndp"] > 0 for q in close)
    B = {"pairs": pairs, "close_pairs": close, "toward_ucp": to_ucp, "toward_ndp": to_ndp,
         "p_sign_two_sided": round(float(binomtest(to_ucp, to_ucp + to_ndp, 0.5).pvalue), 4) if to_ucp + to_ndp else None}

    # C
    moved = P != M
    frm = cat(mM.reindex(M).to_numpy())
    to = cat(mP.reindex(P).to_numpy())
    tab = pd.crosstab(pd.Series(frm[moved], name="from (majority map)"), pd.Series(to[moved], name="to (panel map)"),
                      values=n[moved], aggfunc="sum").fillna(0).round()
    tot = float(n[moved].sum())
    cracked = float(n[moved & np.isin(frm, ["ndp_won", "ndp_near"]) & (to == "ndp_far")].sum())
    unc = float(n[moved & (frm == "ndp_far") & np.isin(to, ["ndp_won", "ndp_near"])].sum())
    C = {"ndp_votes_moved": round(tot), "transition_ndp_votes": tab.to_dict(),
         "won_or_near_to_far": round(cracked), "far_to_won_or_near": round(unc),
         "share_won_or_near_to_far": round(cracked / tot, 4), "share_far_to_won_or_near": round(unc / tot, 4),
         "ucp_votes_moved": round(float(u[moved].sum()))}
    out = {"plan": "preregistration/local_targeting_2026-11-07.md", "A": A, "B": B, "C": C}
    (HERE / "local_targeting.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf8")
    print(json.dumps({"A": {k: v for k, v in A.items() if k != "changed_majority_divisions"}, "B": {k: B[k] for k in ("toward_ucp", "toward_ndp", "p_sign_two_sided")},
                      "close": close, "C": {k: v for k, v in C.items() if k != "transition_ndp_votes"}}, indent=0))
    print(tab)


if __name__ == "__main__":
    main()
