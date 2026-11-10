"""Headline numbers on all 2023 ballots under each allocation rule (exploratory, not registered).

Maps: 2019 (in force), commission majority (89), commission minority (89),
      panel reconstruction v3 (91), para 167 map (91).
Rules: M0 (current), M1 (party-specific), M2 (turnout gap, half lean),
       R = G(beta, lam) with beta and lam taken from the federal test
       (outputs/federal_gradient.json, mean of 2019 and 2021),
       a grid over G, and a Monte Carlo that lets beta and lam differ by
       division as much as they differ between federal ridings (seed 20261109).

Metrics come from analysis/scripts/mcmc_ensemble.seat_results (the audit's own
formulas); "close" uses the rule in close_seats_ensemble.py (two-party margin
of 4 points or less).

Checks: every rule returns each division's official two-party totals, and the
2019 map gives 49 UCP, 38 NDP under every rule.

Writes outputs/headline_table.csv, outputs/headline.json,
       outputs/turnout_plausibility.json, outputs/va_allocations.csv

Usage: python findings/advance_vote_profile/05_models_headlines.py
"""
import contextlib
import io
import json
import sys

import geopandas as gpd
import numpy as np
import pandas as pd

import _models as M
from _common import DATA_ROOT, HERE, OUT, ROOT, build_va_table, division_totals, load_2023_rows, load_va

sys.path.insert(0, str(ROOT / "analysis/scripts"))
with contextlib.redirect_stdout(io.StringIO()):
    import mcmc_ensemble as me

SEED = 20261109
N_DRAWS = 1000
MAPS = {"majority_89": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "minority_89": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
        "panel_v3_91": ("data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district"),
        "para167_91": ("findings/iap_para167/para167_map.gpkg", "district")}


def src(rel):
    p = ROOT / rel
    return p if p.exists() and p.stat().st_size > 10_000 else DATA_ROOT / rel


def assignments(g):
    lab = {"enacted_2019_87": g.parent_ed_2019.values}
    pts = g[["geometry"]].copy()
    pts["geometry"] = g.geometry.representative_point()
    for k, (f, col) in MAPS.items():
        if not src(f).exists():
            continue
        eds = gpd.read_file(src(f)).to_crs(pts.crs)
        j = gpd.sjoin(pts, eds[[col, "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")][col].reindex(pts.index)
        assert j.notna().all(), k
        lab[k] = j.values
    return lab


def metrics(n, u, labels):
    d = pd.DataFrame({"d": labels, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
    s = me.seat_results(d.u.values, d.n.values)
    gap = (d.u - d.n) / (d.u + d.n)
    nseats = len(d)
    return {"ucp_seats": int(s["ucp_seats"]), "ndp_seats": int(nseats - s["ucp_seats"]), "efficiency_gap_pct": round(100 * s["efficiency_gap"], 3),
            "mean_median_pct": round(100 * s["mean_median"], 3), "seats_at_tied_vote": round(s["seats_at_50_50"] * nseats, 1),
            "close_under_4pts": int((gap.abs() <= 0.04).sum()), "n_districts": nseats}, d


def main():
    raw = load_2023_rows()
    g = load_va()
    t = build_va_table(g, raw)
    t["gap"] = t.gap.fillna(0).clip(lower=0)
    tot = division_totals(raw)
    lab = assignments(g.to_crs(3400))
    fed = json.loads((OUT / "federal_gradient.json").read_text())
    yrs = [y for y in fed if fed[y].get("available")]
    BETA = round(float(np.mean([fed[y]["within_riding_slope_beta"]["beta"] for y in yrs])), 2)
    LAM = round(float(np.mean([fed[y]["volume_lambda"]["lambda"] for y in yrs])), 2)
    SD_B = float(np.mean([fed[y]["within_riding_slope_beta"]["per_riding_sd"] for y in yrs]))
    SD_L = float(np.mean([fed[y]["volume_lambda"]["per_riding_sd"] for y in yrs]))
    idx = {ed: np.where(t.ed.values == ed)[0] for ed in sorted(t.ed.unique())}

    def alloc(rule):
        n, u = t.e_n.values.copy(), t.e_u.values.copy()
        for ed, ix in idx.items():
            a_n, a_u = rule(t.e_n.values[ix], t.e_u.values[ix], t.gap.values[ix], float(tot.ndp[ed]), float(tot.ucp[ed]), ed)
            n[ix] += a_n; u[ix] += a_u
        return n, u

    G = lambda b, l: (lambda en, eu, gp, An, Au, ed: M.general(en, eu, gp, An, Au, b, l, shrink_k=10))
    rules = {"M0 current rule": lambda en, eu, gp, An, Au, ed: M.m0(en, eu, gp, An, Au),
             "M1 party-specific": lambda en, eu, gp, An, Au, ed: M.m1(en, eu, gp, An, Au),
             "M2 turnout gap, half lean": lambda en, eu, gp, An, Au, ed: M.m2(en, eu, gp, An, Au),
             f"R recommended G(beta={BETA}, lam={LAM})": G(BETA, LAM)}
    grid_b, grid_l = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25], [0.0, 0.5, 1.0]
    for b in grid_b:
        for l in grid_l:
            rules[f"G({b},{l})"] = G(b, l)

    # recommended rule applied to each ballot type on its own, then added
    kinds = {k: division_totals(raw, (k,)) for k in ("Advance", "Vote Anywhere", "Mobile", "Special Ballot")}

    official = raw.groupby("ed")[["ndp", "ucp"]].sum()
    rows, alloc_store, dist_store = [], {}, {}
    for name, rule in rules.items():
        n, u = alloc(rule)
        chk = pd.DataFrame({"ed": t.ed, "n": n, "u": u}).groupby("ed").sum()
        assert np.abs(chk.n - official.ndp).max() < 1e-6 and np.abs(chk.u - official.ucp).max() < 1e-6, name
        alloc_store[name] = (n, u)
        for mp, labels in lab.items():
            m, d = metrics(n, u, labels)
            if mp == "enacted_2019_87":
                assert (m["ucp_seats"], m["ndp_seats"]) == (49, 38), (name, m)
            rows.append({"map": mp, "rule": name, **m})
            dist_store[(mp, name)] = d
    # by-kind variant of R
    n, u = t.e_n.values.copy(), t.e_u.values.copy()
    for k, tk in kinds.items():
        for ed, ix in idx.items():
            if ed in tk.index:
                a_n, a_u = M.general(t.e_n.values[ix], t.e_u.values[ix], t.gap.values[ix], float(tk.ndp[ed]), float(tk.ucp[ed]), BETA, LAM, shrink_k=10)
                n[ix] += a_n; u[ix] += a_u
    for mp, labels in lab.items():
        m, _ = metrics(n, u, labels)
        rows.append({"map": mp, "rule": "R applied to each ballot type separately", **m})
    # M3: location-informed. Where two or more of a division's named advance polls were geocoded, each such
    # poll's ballots go only to the voting areas nearest to it (R inside that catchment); everything else follows R.
    cf = OUT / "advance_catchments_2023.csv"
    if cf.exists():
        c = pd.read_csv(cf, dtype={"ed": str})
        n, u = t.e_n.values.copy(), t.e_u.values.copy()
        used_n, used_u = pd.Series(0.0, index=tot.index), pd.Series(0.0, index=tot.index)
        for (ed, loc), cc in c.groupby(["ed", "location"]):
            ix = cc.va_row_idx.values
            if t.e_n.values[ix].sum() + t.e_u.values[ix].sum() <= 0:
                continue
            a_n, a_u = M.general(t.e_n.values[ix], t.e_u.values[ix], t.gap.values[ix], float(cc.loc_ndp.iloc[0]), float(cc.loc_ucp.iloc[0]), BETA, LAM, shrink_k=10)
            n[ix] += a_n; u[ix] += a_u
            used_n[ed] += cc.loc_ndp.iloc[0]; used_u[ed] += cc.loc_ucp.iloc[0]
        for ed, ix in idx.items():
            a_n, a_u = M.general(t.e_n.values[ix], t.e_u.values[ix], t.gap.values[ix], float(tot.ndp[ed] - used_n[ed]), float(tot.ucp[ed] - used_u[ed]), BETA, LAM, shrink_k=10)
            n[ix] += a_n; u[ix] += a_u
        chk = pd.DataFrame({"ed": t.ed, "n": n, "u": u}).groupby("ed").sum()
        assert np.abs(chk.n - official.ndp).max() < 1e-6 and np.abs(chk.u - official.ucp).max() < 1e-6
        m3name = f"M3 location-informed ({c.ed.nunique()} divisions, {int(used_n.sum() + used_u.sum()):,} ballots placed by poll)"
        alloc_store[m3name] = (n, u)
        for mp, labels in lab.items():
            m, d = metrics(n, u, labels)
            if mp == "enacted_2019_87":
                assert (m["ucp_seats"], m["ndp_seats"]) == (49, 38)
            rows.append({"map": mp, "rule": m3name, **m})
    T = pd.DataFrame(rows)
    T.to_csv(OUT / "headline_table.csv", index=False)

    # Monte Carlo: beta and lam differ by division as much as they differ between federal ridings
    rng = np.random.default_rng(SEED)
    mc = {mp: [] for mp in lab}
    for _ in range(N_DRAWS):
        bd = {ed: max(0.0, rng.normal(BETA, SD_B)) for ed in idx}
        ld = {ed: float(np.clip(rng.normal(LAM, SD_L), 0, 1)) for ed in idx}
        n, u = alloc(lambda en, eu, gp, An, Au, ed: M.general(en, eu, gp, An, Au, bd[ed], ld[ed], shrink_k=10))
        for mp, labels in lab.items():
            m, _ = metrics(n, u, labels)
            mc[mp].append((m["ucp_seats"], m["efficiency_gap_pct"], m["mean_median_pct"], m["seats_at_tied_vote"], m["close_under_4pts"]))
    mc_out = {}
    for mp, v in mc.items():
        a = np.array(v)
        seats = pd.Series(a[:, 0]).value_counts(normalize=True).sort_index()
        mc_out[mp] = {"ucp_seats_distribution": {int(k): round(float(x), 3) for k, x in seats.items()},
                      "efficiency_gap_pct_p5_p50_p95": [round(float(q), 2) for q in np.percentile(a[:, 1], [5, 50, 95])],
                      "mean_median_pct_p5_p50_p95": [round(float(q), 2) for q in np.percentile(a[:, 2], [5, 50, 95])],
                      "seats_at_tied_vote_distribution": {str(k): round(float(x), 3) for k, x in pd.Series(a[:, 3]).value_counts(normalize=True).sort_index().items()},
                      "close_under_4pts_min_max": [int(a[:, 4].min()), int(a[:, 4].max())]}

    rname = [k for k in rules if k.startswith("R ")][0]
    supported = [k for k in rules if k.startswith("G(") and float(k[2:].split(",")[0]) >= 0.75] + ["M1 party-specific", rname]
    rng_out = {}
    for mp in lab:
        s = T[(T["map"] == mp) & T.rule.isin(supported)]
        rng_out[mp] = {"ucp_seats": [int(s.ucp_seats.min()), int(s.ucp_seats.max())],
                       "efficiency_gap_pct": [float(s.efficiency_gap_pct.min()), float(s.efficiency_gap_pct.max())],
                       "mean_median_pct": [float(s.mean_median_pct.min()), float(s.mean_median_pct.max())],
                       "seats_at_tied_vote": [float(s.seats_at_tied_vote.min()), float(s.seats_at_tied_vote.max())],
                       "close_under_4pts": [int(s.close_under_4pts.min()), int(s.close_under_4pts.max())]}
    # districts that change hands between M0 and R, and R's thinnest margins
    flips = {}
    for mp in lab:
        d0, d1 = dist_store[(mp, "M0 current rule")], dist_store[(mp, rname)]
        ch = d0.index[(d0.u > d0.n) != (d1.u > d1.n)]
        flips[mp] = {"changed_winner": {x: {"M0_ucp_margin_votes": round(float(d0.u[x] - d0.n[x]), 1), "R_ucp_margin_votes": round(float(d1.u[x] - d1.n[x]), 1)} for x in ch},
                     "R_three_thinnest": {x: round(float(d1.u[x] - d1.n[x]), 1) for x in (d1.u - d1.n).abs().sort_values().index[:3]},
                     "M0_three_thinnest": {x: round(float(d0.u[x] - d0.n[x]), 1) for x in (d0.u - d0.n).abs().sort_values().index[:3]},
                     "largest_district_share_shift_pts": round(float(100 * ((d1.n / (d1.n + d1.u)) - (d0.n / (d0.n + d0.u))).abs().max()), 2)}

    # turnout plausibility per election-day station: (election-day ballots + allocated ballots) / names on list
    st_el = t.groupby("station").electors.sum()
    st_ev = t.groupby("station").eday_valid.sum()
    non_valid = raw[raw.kind != "Election Day"].groupby("ed").valid.sum()
    scale = (non_valid / (tot.ndp + tot.ucp))  # all-party ballots per two-party ballot, by division
    plaus = {}
    for name in ["M0 current rule", "M1 party-specific", "M2 turnout gap, half lean", rname]:
        n, u = alloc_store[name]
        add = pd.Series((n - t.e_n.values + u - t.e_u.values) * t.ed.map(scale).values).groupby(t.station.values).sum()
        to = ((st_ev + add) / st_el).replace([np.inf, -np.inf], np.nan).dropna()
        sd_within = to.groupby(to.index.str[:2]).std().median()
        plaus[name] = {"stations": int(len(to)), "over_100pct": int((to > 1).sum()), "over_90pct": int((to > 0.9).sum()), "under_30pct": int((to < 0.3).sum()),
                       "max_pct": round(100 * float(to.max()), 1), "min_pct": round(100 * float(to.min()), 1), "median_pct": round(100 * float(to.median()), 1),
                       "median_within_division_sd_pts": round(100 * float(sd_within), 2)}
    plaus["election_day_only"] = {"max_pct": round(100 * float((st_ev / st_el).max()), 1), "median_pct": round(100 * float((st_ev / st_el).median()), 1),
                                  "median_within_division_sd_pts": round(100 * float((st_ev / st_el).groupby(st_el.index.str[:2]).std().median()), 2)}
    (OUT / "turnout_plausibility.json").write_text(json.dumps(plaus, indent=1))

    out = {"status": "exploratory, not registered", "recommended": {"rule": rname, "beta": BETA, "lam": LAM, "source": "mean of federal 2019 and 2021 Alberta estimates"},
           "monte_carlo": {"seed": SEED, "draws": N_DRAWS, "beta_sd_between_divisions": round(SD_B, 3), "lam_sd_between_divisions": round(SD_L, 3), "results": mc_out},
           "supported_range_rules": supported, "supported_range": rng_out, "M0_vs_R": flips,
           "checks": {"division_totals_match_official_under_every_rule": True, "2019_map_49_38_under_every_rule": True}}
    (OUT / "headline.json").write_text(json.dumps(out, indent=1))
    va = pd.DataFrame({"va_row_idx": np.arange(len(t)), "ed": t.ed, "va": t.v, "eday_ndp": t.e_n.round(3), "eday_ucp": t.e_u.round(3)})
    for name, key in (("M0 current rule", "M0"), ("M1 party-specific", "M1"), ("M2 turnout gap, half lean", "M2"), (rname, "R")):
        va[f"{key}_ndp"], va[f"{key}_ucp"] = alloc_store[name][0].round(3), alloc_store[name][1].round(3)
    va.to_csv(OUT / "va_allocations.csv", index=False)

    pd.set_option("display.width", 250)
    show = T[~T.rule.str.startswith("G(")]
    print(show.to_string(index=False))
    print(T[T.rule.str.startswith("G(") & T["map"].isin(["minority_89", "majority_89"])].to_string(index=False))
    print(json.dumps(out["monte_carlo"], indent=1)); print(json.dumps(rng_out, indent=1)); print(json.dumps(flips, indent=1)); print(json.dumps(plaus, indent=1))


if __name__ == "__main__":
    main()
