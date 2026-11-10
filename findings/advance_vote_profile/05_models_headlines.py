"""Results on all 2023 ballots under M0 (the registered rule) and P, on every map (exploratory, not registered).

Maps: 2019 (in force, 87), commission majority (89), commission minority (89),
      panel reconstruction v3 (91), para 167 reconstruction (91).
Rules: M0  read from the registered Amendment 12 file (va_polygons_all_2023_ballots_primary.gpkg,
           SHA-256 checked), and rebuilt here as a check;
       P   rule_p in _models.py: lam = 1, beta = 1.0, and the same rule across the provincial
           range of beta (the 95% cluster-bootstrap range of the 2023 located-poll slope, from
           outputs/robustness.json). No federal number is used.

Metrics: analysis/scripts/mcmc_ensemble.seat_results (the audit's own formulas). Close seat:
two-party margin of 4 points or less. Voting areas go to districts by representative point.

Checks (printed; the script stops if any fails):
  1. every division's official NDP, UCP and other totals are returned exactly, under M0 and every P;
  2. the 2019 map gives 49 UCP, 38 NDP under M0 and every P;
  3. no election-day station is over 100% of its list under P, except those already over on election day;
  4. the rebuilt M0 equals the registered file.

Writes outputs/headline.json, outputs/headline_table.csv, outputs/district_margins.csv,
       outputs/va_allocations.csv

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
from _common import (DATA_ROOT, M0_SHA256, OUT, ROOT, VA_EDAY, VA_M0, WORKBOOK_2023, build_va_table,
                     division_totals, load_2023_rows, load_va, sha256, write_csv, write_json)

sys.path.insert(0, str(ROOT / "analysis/scripts"))
with contextlib.redirect_stdout(io.StringIO()):
    import mcmc_ensemble as me

MAPS = {"majority_89": ("data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "minority_89": ("data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
        "panel_v3_91": ("data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district"),
        "para167_91": ("findings/iap_para167/para167_map.gpkg", "district")}
MAP_LABEL = {"enacted_2019_87": "2019 map (87)", "majority_89": "Commission majority (89)",
             "minority_89": "Commission minority (89)", "panel_v3_91": "Panel reconstruction v3 (91)",
             "para167_91": "Paragraph 167 reconstruction (91)"}


def src(rel):
    p = ROOT / rel
    return p if p.exists() and p.stat().st_size > 10_000 else DATA_ROOT / rel


def assignments(g):
    lab = {"enacted_2019_87": g.parent_ed_2019.values}
    pts = g[["geometry"]].copy()
    pts["geometry"] = g.geometry.representative_point()
    for k, (f, col) in MAPS.items():
        eds = gpd.read_file(src(f)).to_crs(pts.crs)
        j = gpd.sjoin(pts, eds[[col, "geometry"]], how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")][col].reindex(pts.index)
        assert j.notna().all(), k
        lab[k] = j.values
    return lab


def metrics(n, u, labels):
    d = pd.DataFrame({"d": labels, "u": u, "n": n}).groupby("d")[["u", "n"]].sum()
    s = me.seat_results(d.u.values, d.n.values)
    share = (d.u - d.n) / (d.u + d.n)
    k = len(d)
    return {"ucp_seats": int(s["ucp_seats"]), "ndp_seats": int(k - s["ucp_seats"]),
            "efficiency_gap_pct": round(100 * s["efficiency_gap"], 3), "mean_median_pct": round(100 * s["mean_median"], 3),
            "declination": round(s["declination"], 4), "ucp_seats_at_tied_vote": round(s["seats_at_50_50"] * k, 1),
            "close_seats_4pts": int((share.abs() <= 0.04).sum()), "n_districts": k}, d


def station_turnout(t, placed):
    """Per election-day station: (election-day ballots + placed early ballots) / names on list."""
    s = pd.DataFrame({"station": t.station.values, "electors": t.electors.values, "eday_total": t.eday_total.values,
                      "placed": placed}).groupby("station").sum()
    return s, (s.eday_total + s.placed) / s.electors


def beta_evidence():
    loc = json.loads((OUT / "provincial_location_tests.json").read_text())
    rob = json.loads((OUT / "robustness.json").read_text())
    a = loc["located_polls_2023"]["slope_all"]
    b = loc["town_polls_2015"]["slope"]
    lo, hi = rob["located_polls_2023"]["cluster_bootstrap_95pct"]
    return {"estimate_2023_located_polls": a["beta"], "se_2023_located_polls": a["se_clustered"],
            "estimate_2015_town_polls": b["beta"], "se_2015_town_polls": b["se_clustered"],
            "unweighted_2023": rob["located_polls_2023"]["log_odds_unweighted"][0],
            "without_two_mountain_divisions_2023": rob["located_polls_2023"]["drop_top2"][0],
            "range_used": [lo, hi], "range_source": "95% cluster bootstrap of the 2023 located-poll slope (robustness.json)",
            "value_used": M.BETA_P}


def main():
    raw = load_2023_rows()
    g = load_va()
    t = build_va_table(g, raw)
    tot = division_totals(raw)
    lab = assignments(g.to_crs(3400))
    official = raw.groupby("ed")[["ndp", "ucp", "other"]].sum()
    ev = beta_evidence()
    lo, hi = ev["range_used"]
    assert lo <= M.BETA_P <= hi, "value used lies outside the provincial range"
    betas = sorted({round(lo, 2), 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, round(hi, 2)})
    checks = []

    def check(name, ok, detail):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + name + ": " + detail, flush=True)

    # M0: the registered file itself
    assert sha256(VA_M0) == M0_SHA256, "registered all-ballots file changed"
    gm = gpd.read_file(VA_M0)
    assert (gm.OBJECTID.values == g.OBJECTID.values).all()
    store = {"m0": {"ndp": gm.va_ndp.values.astype(float), "ucp": gm.va_ucp.values.astype(float), "other": gm.va_other.values.astype(float)}}
    # M0 rebuilt (two-party), to show the rule implemented here is the registered one
    n0, u0 = t.e_n.values.copy(), t.e_u.values.copy()
    for ed, ix in t.groupby("ed").indices.items():
        a, b = M.m0(t.e_n.values[ix], t.e_u.values[ix], t.gap.values[ix], float(tot.ndp[ed]), float(tot.ucp[ed]))
        n0[ix] += a; u0[ix] += b
    d0 = float(max(np.abs(n0 - store["m0"]["ndp"]).max(), np.abs(u0 - store["m0"]["ucp"]).max()))
    check("rebuilt M0 equals the registered file", d0 < 1e-6, f"largest difference per voting area {d0:.2e} votes")
    e_two = t.e_n.values + t.e_u.values
    m0_share = np.zeros(len(t))
    for ed, ix in t.groupby("ed").indices.items():
        m0_share[ix] = e_two[ix] / e_two[ix].sum()
    store["m0"]["placed_ballots"] = t.ed.map(tot.total).values * m0_share

    for b in betas:
        store[f"p_beta_{b:.2f}".replace(".", "_")] = M.allocate_p(t, tot, b)
    pkey = "p_beta_1_00"

    worst = 0.0
    for k, a in store.items():
        c = pd.DataFrame({"ed": t.ed, "ndp": a["ndp"], "ucp": a["ucp"], "other": a["other"]}).groupby("ed").sum()
        worst = max(worst, float((c - official.loc[c.index]).abs().max().max()))
    check("every division's official NDP, UCP and other totals returned", worst < 1e-6 and len(official) == 87,
          f"87 divisions, {len(store)} allocations, largest difference {worst:.2e} votes")

    rows, dist = [], {}
    for k, a in store.items():
        for mp, labels in lab.items():
            m, d = metrics(a["ndp"], a["ucp"], labels)
            rows.append({"map": mp, "rule": "m0" if k == "m0" else "p", "beta": None if k == "m0" else float(k[7:].replace("_", ".")), **m})
            dist[(mp, k)] = d
    T = pd.DataFrame(rows)
    e19 = T[T["map"] == "enacted_2019_87"]
    check("2019 map gives 49-38 under M0 and every P", ((e19.ucp_seats == 49) & (e19.ndp_seats == 38)).all(),
          ", ".join(f"{r.rule}{'' if r.beta is None or np.isnan(r.beta) else ' beta ' + format(r.beta, '.2f')}: {r.ucp_seats}-{r.ndp_seats}" for r in e19.itertuples()))

    # turnout hard check
    _, to_ed = station_turnout(t, np.zeros(len(t)))
    over_ed = set(to_ed.index[to_ed > 1])
    bad = []
    for k, a in store.items():
        if k == "m0":
            continue
        _, to = station_turnout(t, a["placed_ballots"])
        bad += [(k, s, round(100 * float(to[s]), 1)) for s in to.index[to > 1 + 1e-9] if s not in over_ed]
    check("no station over 100% under P beyond those already over on election day", not bad,
          f"over on election day alone: {sorted(over_ed)}; new under any P: {len(bad)}")
    _, to_m0 = station_turnout(t, store["m0"]["placed_ballots"])

    # ranges and seat changes
    P = T[T.rule == "p"]
    summary = []
    for mp in lab:
        r0 = T[(T["map"] == mp) & (T.rule == "m0")].iloc[0]
        rp = P[(P["map"] == mp) & (P.beta == M.BETA_P)].iloc[0]
        s = P[P["map"] == mp]
        rec = {"map": mp, "label": MAP_LABEL[mp], "n_districts": int(r0.n_districts),
               "m0": {c: r0[c] for c in ("ucp_seats", "ndp_seats", "efficiency_gap_pct", "mean_median_pct", "declination", "ucp_seats_at_tied_vote", "close_seats_4pts")},
               "p_beta_1": {c: rp[c] for c in ("ucp_seats", "ndp_seats", "efficiency_gap_pct", "mean_median_pct", "declination", "ucp_seats_at_tied_vote", "close_seats_4pts")},
               "p_range_over_beta": {c: [s[c].min(), s[c].max()] for c in ("ucp_seats", "efficiency_gap_pct", "mean_median_pct", "declination", "ucp_seats_at_tied_vote", "close_seats_4pts")}}
        d0m, d1 = dist[(mp, "m0")], dist[(mp, pkey)]
        mar = {k: (dist[(mp, k)].u - dist[(mp, k)].n) for k in store}
        pm = pd.concat([mar[k] for k in store if k != "m0"], axis=1)
        changed = []
        for x in d0m.index:
            w0, w1 = mar["m0"][x] > 0, mar[pkey][x] > 0
            flips_in_range = bool(((pm.loc[x] > 0) != w0).any())
            if w0 != w1 or flips_in_range:
                changed.append({"district": x, "m0_ucp_margin_votes": round(float(mar["m0"][x])), "p_ucp_margin_votes": round(float(mar[pkey][x])),
                                "p_ucp_margin_range_votes": [round(float(pm.loc[x].min())), round(float(pm.loc[x].max()))],
                                "winner_m0": "UCP" if w0 else "NDP", "winner_p": "UCP" if w1 else "NDP",
                                "changes_at_beta_1": bool(w0 != w1)})
        rec["seats_that_change"] = changed
        rec["thinnest_p_margins"] = [{"district": x, "p_ucp_margin_votes": round(float(mar[pkey][x]))} for x in mar[pkey].abs().sort_values().index[:4]]
        summary.append(rec)
    # one row per district per map
    dm = []
    for mp in lab:
        idx = dist[(mp, "m0")].index
        for x in idx:
            dd0, dd1 = dist[(mp, "m0")].loc[x], dist[(mp, pkey)].loc[x]
            pm = [float(dist[(mp, k)].loc[x].u - dist[(mp, k)].loc[x].n) for k in store if k != "m0"]
            dm.append({"map": mp, "district": x, "m0_ucp": round(dd0.u, 1), "m0_ndp": round(dd0.n, 1), "m0_ucp_margin": round(dd0.u - dd0.n, 1),
                       "p_ucp": round(dd1.u, 1), "p_ndp": round(dd1.n, 1), "p_ucp_margin": round(dd1.u - dd1.n, 1),
                       "p_ucp_margin_min_over_beta": round(min(pm), 1), "p_ucp_margin_max_over_beta": round(max(pm), 1),
                       "winner_m0": "UCP" if dd0.u > dd0.n else "NDP", "winner_p": "UCP" if dd1.u > dd1.n else "NDP"})
    write_csv(pd.DataFrame(dm), "district_margins.csv")
    write_csv(T, "headline_table.csv")
    va = pd.DataFrame({"va_row_idx": np.arange(len(t)), "ed": t.ed, "va": t.v, "station": t.station,
                       "eday_ndp": t.e_n.round(3), "eday_ucp": t.e_u.round(3), "eday_other": t.e_o.round(3),
                       "electors": t.electors.round(3), "eday_ballots": t.eday_total.round(3),
                       "m0_ndp": store["m0"]["ndp"].round(3), "m0_ucp": store["m0"]["ucp"].round(3), "m0_other": store["m0"]["other"].round(3),
                       "p_ndp": store[pkey]["ndp"].round(3), "p_ucp": store[pkey]["ucp"].round(3), "p_other": store[pkey]["other"].round(3),
                       "p_placed_ballots": store[pkey]["placed_ballots"].round(3)})
    write_csv(va, "va_allocations.csv")
    over = []
    for s in sorted(over_ed):
        r = raw[(raw.kind == "Election Day") & ((raw.ed + raw.letter.astype(str)) == s)].iloc[0]
        over.append({"station": s, "division": r.ed, "name": r["name"], "voting_areas": r.vas, "names_on_list": int(r.electors),
                     "election_day_ballots": int(r.total), "turnout_pct": round(100 * r.total / r.electors, 1)})
    out = {"rule_p": {"lam": M.LAM_P, "beta": ev, "shrink_pseudo_count": M.SHRINK_K,
                      "betas_run": betas, "federal_numbers_used": False},
           "checks": checks, "all_checks_passed": all(c["passed"] for c in checks),
           "stations_over_100pct_on_election_day": over,
           "stations_over_100pct_m0": int((to_m0 > 1).sum()),
           "maps": summary}
    write_json("headline.json", out, __file__, [WORKBOOK_2023, VA_EDAY, VA_M0, OUT / "provincial_location_tests.json", OUT / "robustness.json"]
               + [src(f) for f, _ in MAPS.values()])
    pd.set_option("display.width", 250)
    print(T[(T.rule == "m0") | (T.beta == M.BETA_P)].to_string(index=False))
    print(json.dumps(summary, indent=1, default=float))
    if not out["all_checks_passed"]:
        sys.exit("a check failed")


if __name__ == "__main__":
    main()
