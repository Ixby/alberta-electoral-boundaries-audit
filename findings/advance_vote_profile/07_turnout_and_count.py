"""Turnout cannot pass 100% of the list: the constraint, the evidence, and the count side of P
(exploratory, not registered). Provincial data only.

1. What "Names on List" counts. The 2023 workbook's station counts are summed per division and compared
   with Appendix D of Elections Alberta's 2023 report (the Post Election Day List of Electors), copied into
   inputs/ea_2023_report_appendix_c_d.csv. What the report says the list includes is recorded with page numbers.
2. Station turnout, (election-day ballots + placed early ballots) / names on list, for election day alone,
   M0 and P: percentiles, counts in 5-point bins, and the stations over 100%.
3. The hard check: under P no station passes 100% unless it already does on election day.
4. P's count assumption: within a division, the share of election-day non-voters who voted early is the
   same at every station. Two provincial looks: across the 87 divisions, and inside divisions at the
   located advance polls (outputs/advance_locations_2023.csv).

Placed early ballots: every non-election-day ballot of the division (valid, declined and rejected).
P places them by electors who did not vote on election day; M0 places them like election-day two-party votes.
Turnout under P does not depend on beta.

Writes outputs/turnout.json, outputs/turnout_stations.csv, outputs/division_takeup.csv
Usage: python findings/advance_vote_profile/07_turnout_and_count.py
"""
import json

import numpy as np
import pandas as pd
from scipy import stats

import _models as M
from _common import INPUTS, OUT, VA_EDAY, WORKBOOK_2023, build_va_table, division_totals, load_2023_rows, load_va, write_csv, write_json

REPORT = {"title": "Elections Alberta, 2023 Provincial General Election Report",
          "url": "https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Report.pdf",
          "sha256_of_pdf_fetched_2026_11_10": "51e9771b61bcd05a066b23f733efd563fd36f8ee14f42c309682bf8ebaf31993",
          "statements": [
              {"page": 61, "text": "248,688 electors registered to vote at their advance or Election Day voting location, representing 14% of voters"},
              {"page": 61, "text": "Electors who were not registered or had not updated their information after the close of the revision period were required to complete their registration at their voting location prior to being issued their ballot."},
              {"page": 62, "text": "Following the close of voting, returning offices package all election supplies and materials including declaration forms to return to Elections Alberta. From here, Elections Alberta reviews all voting records, declarations, and oaths to update the Register of Electors."},
              {"page": 62, "text": "The Post Election Day List of Electors is compiled following these updates and represents a snapshot of voters as of March 26, 2024."},
              {"page": 131, "text": "voter turnout is recalculated using the Post Election Day List of Electors ... it accounts for changes to the List of Electors received during the election period that were processed during post-election data entry. This ensures that electors who have moved are not double counted in the List ..., electors who are deceased or moved are removed from the list, and new electors are reflected in the correct electoral division and voting area."},
              {"page": 131, "text": "Table 29, 2023: Ballots Cast 1,777,315; Names on List 2,939,762; Voter Turnout 60.5%"}]}
BINS = list(range(0, 105, 5))


def dist(x):
    x = np.asarray(x, float)
    q = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]
    b = pd.cut(100 * x, bins=[-0.001] + BINS[1:] + [np.inf], right=True)
    counts = pd.Series(b).value_counts(sort=False)
    labels = [f"{lo}_to_{lo + 5}" for lo in BINS[:-1]] + ["over_100"]
    return {"stations": int(len(x)), "percentiles_pct": [{"percentile": p, "turnout_pct": round(float(v), 2)} for p, v in zip(q, np.percentile(100 * x, q))],
            "bins_5pt": [{"bin": lab, "stations": int(c)} for lab, c in zip(labels, counts.values)],
            "at_or_over_100": int((x >= 1 - 1e-12).sum()), "over_100": int((x > 1 + 1e-12).sum()),
            "over_95": int((x > 0.95).sum()), "under_30": int((x < 0.30).sum())}


def main():
    raw = load_2023_rows()
    g = load_va()
    t = build_va_table(g, raw)
    tot = division_totals(raw)
    ed_rows = raw[raw.kind == "Election Day"].copy()
    ed_rows["station"] = ed_rows.ed + ed_rows.letter.astype(str)

    # 1. Names on List against the report
    ap = pd.read_csv(INPUTS / "ea_2023_report_appendix_c_d.csv", dtype={"ed": str})
    wb = ed_rows.groupby("ed").electors.sum()
    cmp_ = ap.set_index("ed").post_election_list_of_electors
    eq = (wb.reindex(cmp_.index) == cmp_)
    missing = sorted(set(wb.index) - set(cmp_.index))
    names = {"workbook_names_on_list_total": int(wb.sum()), "report_table_29_names_on_list": 2939762,
             "workbook_equals_table_29": bool(int(wb.sum()) == 2939762),
             "appendix_d_divisions_read": int(len(cmp_)), "appendix_d_divisions_equal_to_workbook": int(eq.sum()),
             "appendix_d_divisions_missing_from_text_extraction": missing,
             "missing_division_equals_table_29_remainder": bool(all(int(wb[m]) == 2939762 - int(cmp_.sum()) for m in missing)) if len(missing) == 1 else None,
             "registered_at_voting_place_appendix_c_total_read": int(ap.registered_total.sum()),
             "finding": ("The workbook's Names on List is the Post Election Day List of Electors (it equals Appendix D in every division "
                         "read and Table 29 in total). The report says that list was updated from the voting records and declaration "
                         "forms and places new electors in their correct division and voting area, so electors who registered at a "
                         "voting place, on election day or in advance, are most likely counted, in the voting area where they live. That reading "
                         "rests on the report's general description; the report does not say so station by station, and it gives no "
                         "count of poll registrants per station."),
             "report": REPORT}

    # 2-3. station turnout
    gap = np.nan_to_num(t.gap.values.astype(float), nan=0.0)
    placed_p = np.zeros(len(t)); placed_m0 = np.zeros(len(t))
    e_two = t.e_n.values + t.e_u.values
    for ed, ix in t.groupby("ed").indices.items():
        placed_p[ix] = float(tot.total[ed]) * M.count_weights_p(gap[ix])
        placed_m0[ix] = float(tot.total[ed]) * e_two[ix] / e_two[ix].sum()
    st = pd.DataFrame({"station": t.station, "ed": t.ed, "electors": t.electors, "eday_ballots": t.eday_total,
                       "placed_m0": placed_m0, "placed_p": placed_p}).groupby(["station", "ed"], as_index=False).sum()
    st = st.merge(ed_rows[["station", "name", "vas"]], on="station", how="left")
    st["turnout_eday_only"] = st.eday_ballots / st.electors
    st["turnout_m0"] = (st.eday_ballots + st.placed_m0) / st.electors
    st["turnout_p"] = (st.eday_ballots + st.placed_p) / st.electors
    assert len(st) == 1216 and st.electors.gt(0).all()
    G = pd.Series(gap.clip(0)).groupby(t.ed.values).sum()
    take = tot.total / G
    over_eday = st[st.turnout_eday_only > 1]
    new_over_p = st[(st.turnout_p > 1 + 1e-9) & ~(st.turnout_eday_only > 1)]
    explain = {
        "04H": ("Calgary Drop In Centre, a homeless shelter. Most plausibly electors with no fixed address voted there and were registered "
                "at the shelter, while the list as of March 2024 counts only those still listed there. Not established from the data."),
        "61C": ("Remote Area - Fort Fitzgerald, a remote poll with 2 names on the list. Most plausibly people who live or work in the "
                "area but are listed elsewhere, or were registered at the poll and placed in another voting area. Cannot tell from the data.")}
    over_list = [{"station": r.station, "division": r.ed, "name": r.name, "voting_areas": r.vas, "names_on_list": int(r.electors),
                  "election_day_ballots": int(r.eday_ballots), "turnout_pct": round(100 * r.turnout_eday_only, 1),
                  "turnout_p_pct": round(100 * r.turnout_p, 1), "turnout_m0_pct": round(100 * r.turnout_m0, 1),
                  "plausible_explanation": explain.get(r.station, "Cannot tell from the data.")} for r in over_eday.itertuples()]
    hard = {"divisions": 87, "largest_division_takeup": round(float(take.max()), 4),
            "every_division_has_fewer_early_ballots_than_election_day_non_voters": bool((tot.total <= G).all()),
            "stations_over_100_on_election_day_alone": int(len(over_eday)),
            "stations_over_100_under_p_not_already_over": int(len(new_over_p)),
            "stations_at_exactly_100_under_p": int((np.abs(st.turnout_p - 1) < 1e-9).sum()),
            "passed": bool(len(new_over_p) == 0 and (tot.total <= G).all()),
            "why_it_holds": ("Under P a station's turnout is 1 - (non-voters / list) x (1 - division take-up). Take-up is below 1 in every "
                             "division, so turnout stays below 100% wherever any listed elector did not vote on election day. Stations "
                             "already over 100% get no early ballots under P and stay where election day put them.")}
    print("hard check", json.dumps(hard), flush=True)
    m0_over = st[st.turnout_m0 > 1].sort_values("turnout_m0", ascending=False)

    # 4. count assumption
    dv = pd.DataFrame({"electors": st.groupby("ed").electors.sum(), "eday_ballots": st.groupby("ed").eday_ballots.sum(),
                       "early_ballots": tot.total, "non_voters_eday": G})
    dv["eday_turnout"] = dv.eday_ballots / dv.electors
    dv["takeup"] = dv.early_ballots / dv.non_voters_eday
    dv["total_turnout"] = (dv.eday_ballots + dv.early_ballots) / dv.electors
    names_ = g.drop_duplicates("ed").set_index("ed").parent_ed_2019
    from _common import region_of
    dv["division"] = names_.reindex(dv.index)
    dv["region"] = dv.division.map(region_of)
    r_p, p_p = stats.pearsonr(dv.eday_turnout, dv.takeup)
    r_s, p_s = stats.spearmanr(dv.eday_turnout, dv.takeup)
    sl = stats.linregress(dv.eday_turnout, dv.takeup)
    by_reg = []
    for reg, d in dv.groupby("region"):
        rr = stats.spearmanr(d.eday_turnout, d.takeup)
        by_reg.append({"region": reg, "divisions": int(len(d)), "spearman_rho": round(float(rr[0]), 3), "p_value": round(float(rr[1]), 4),
                       "median_takeup": round(float(d.takeup.median()), 3)})
    across = {"divisions": 87, "takeup_median": round(float(dv.takeup.median()), 3), "takeup_min": round(float(dv.takeup.min()), 3),
              "takeup_max": round(float(dv.takeup.max()), 3),
              "pearson_r_takeup_vs_eday_turnout": round(float(r_p), 3), "pearson_p": float(p_p),
              "spearman_rho": round(float(r_s), 3), "spearman_p": float(p_s),
              "slope_takeup_per_point_of_eday_turnout": round(float(sl.slope), 3), "slope_se": round(float(sl.stderr), 3),
              "by_region": by_reg}
    # inside divisions, at the located advance polls
    L = pd.read_csv(OUT / "advance_locations_2023.csv", dtype={"ed": str})
    L = L[L.groupby("ed").ed.transform("size") >= 2].copy()
    # catchment electors and election-day ballots, from the voting-area table
    c = pd.read_csv(OUT / "advance_catchments_2023.csv", dtype={"ed": str})
    c = c.merge(pd.DataFrame({"va_row_idx": np.arange(len(t)), "electors": t.electors.values, "eday_ballots": t.eday_total.values,
                              "non_voters": gap.clip(0)}), on="va_row_idx")
    cc = c.groupby(["ed", "location"], as_index=False)[["electors", "eday_ballots", "non_voters"]].sum().rename(columns={"location": "name"})
    L = L.merge(cc, on=["ed", "name"], how="inner")
    L["a_two"] = L.a_ndp + L.a_ucp
    L = L[(L.non_voters > 0) & (L.groupby("ed").ed.transform("size") >= 2)]
    L["y"] = np.log(L.a_two / L.non_voters)   # log of early two-party ballots per election-day non-voter in the catchment
    L["x"] = L.eday_ballots / L.electors       # catchment election-day turnout
    xd = L.x - L.groupby("ed").x.transform("mean")
    yd = L.y - L.groupby("ed").y.transform("mean")
    b = float(np.sum(xd * yd) / np.sum(xd * xd))
    cl = (xd * (yd - b * xd)).groupby(L.ed).sum()
    se = float(np.sqrt((cl ** 2).sum()) / np.sum(xd * xd))
    within = {"polls": int(len(L)), "divisions": int(L.ed.nunique()),
              "slope_log_takeup_per_unit_eday_turnout": round(b, 3), "se_clustered": round(se, 3),
              "corr_within": round(float(np.corrcoef(xd, yd)[0, 1]), 3),
              "reading": ("P predicts a slope of 0: within a division, take-up among election-day non-voters does not depend on "
                          "the area's election-day turnout. A positive slope means early ballots are more concentrated where "
                          "election-day turnout was high than P puts them.")}
    count = {"assumption": "Within a division, the share of election-day non-voters who voted early is the same at every station.",
             "across_divisions": across, "within_divisions_located_polls": within,
             "cannot_say": ["Who voted early at any station: no provincial source counts early ballots below the division except the "
                            "254 named advance polls, and an elector may use any advance poll.",
                            "Whether the across-division pattern holds inside divisions: divisions differ in poll siting, hours, "
                            "distance and campaign, so a cross-division link is not a within-division one.",
                            "The located-poll catchments are nearest-poll guesses, and a poll's volume depends on its size and hours. "
                            "Vote Anywhere, special and mobile ballots (about 29% of early two-party ballots) are not covered."]}
    print("count assumption", json.dumps(count, indent=1, default=float), flush=True)

    out = {"names_on_list": names,
           "turnout_distribution": {"election_day_alone": dist(st.turnout_eday_only), "m0": dist(st.turnout_m0), "p": dist(st.turnout_p)},
           "within_division_sd_pts_median": {k: round(float(100 * st.groupby("ed")[c_].std().median()), 2)
                                              for k, c_ in (("election_day_alone", "turnout_eday_only"), ("m0", "turnout_m0"), ("p", "turnout_p"))},
           "stations_over_100_election_day_alone": over_list,
           "m0_stations_over_100": int(len(m0_over)), "m0_top10_over_100": [
               {"station": r.station, "name": r.name, "names_on_list": int(r.electors), "turnout_m0_pct": round(100 * r.turnout_m0, 1)}
               for r in m0_over.head(10).itertuples()],
           "hard_check_p": hard, "count_assumption": count}
    st_out = st[["station", "ed", "name", "electors", "eday_ballots", "placed_m0", "placed_p", "turnout_eday_only", "turnout_m0", "turnout_p"]].copy()
    st_out = st_out.rename(columns={"name": "station_name", "electors": "names_on_list"})
    for c_ in ("placed_m0", "placed_p"):
        st_out[c_] = st_out[c_].round(2)
    for c_ in ("turnout_eday_only", "turnout_m0", "turnout_p"):
        st_out[c_] = st_out[c_].round(5)
    write_csv(st_out, "turnout_stations.csv")
    dv_out = dv.reset_index().rename(columns={"index": "ed"})[["ed", "division", "region", "electors", "eday_ballots", "early_ballots",
                                                               "non_voters_eday", "eday_turnout", "takeup", "total_turnout"]].round(5)
    write_csv(dv_out, "division_takeup.csv")
    write_json("turnout.json", out, __file__, [WORKBOOK_2023, VA_EDAY, INPUTS / "ea_2023_report_appendix_c_d.csv",
                                              OUT / "advance_locations_2023.csv", OUT / "advance_catchments_2023.csv"])
    print(json.dumps({k: out[k] for k in ("names_on_list", "turnout_distribution", "within_division_sd_pts_median")}, indent=1, default=float)[:6000])
    if not hard["passed"]:
        raise SystemExit("hard check failed")


if __name__ == "__main__":
    main()
