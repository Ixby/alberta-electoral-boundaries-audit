"""Measure how non-election-day ballots differ from election-day ballots (exploratory, not registered).

2023: data/raw/2023_results.xlsx, every poll row in all 87 divisions.
2015: data/raw/2015_results.xlsx, every poll row in all 87 divisions
      (NDP against PC + Wildrose, the two parties that later merged into the UCP).
2019 poll-level results are not in the repository, so 2019 is not measured here.

Writes outputs/skew_2023_by_division.csv, outputs/skew_2015_by_division.csv,
       outputs/skew_summary.json

Usage: python findings/advance_vote_profile/01_measure_skew.py
"""
import json
import re

import numpy as np
import pandas as pd
from scipy import stats

from _common import OUT, VA_EDAY, WORKBOOK_2015, WORKBOOK_2023, load_2023_rows, load_va, logit, region_of, write_csv, write_json


def wls_slope(x, y, w):
    x, y, w = map(np.asarray, (x, y, w))
    xm, ym = np.average(x, weights=w), np.average(y, weights=w)
    b = np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2)
    a = ym - b * xm
    res = y - a - b * x
    n = len(x)
    se = np.sqrt(np.sum(w * res ** 2) / (n - 2) / np.sum(w * (x - xm) ** 2))  # weighted least squares, classical SE
    return float(a), float(b), float(se)


def summarise(div, kinds, label):
    """div: one row per division with columns {kind}_ndp, {kind}_ucp, region, electors."""
    out = {"label": label, "province": {}, "by_region": [], "by_competitiveness": [], "cross_division": {}}
    ed_share = div.eday_ndp / (div.eday_ndp + div.eday_ucp)
    div["eday_share"] = ed_share
    div["eday_margin_pts"] = 100 * (2 * ed_share - 1).abs()
    div["comp"] = pd.cut(div.eday_margin_pts, [-1, 10, 30, 101], labels=["close (under 10 pts)", "10 to 30 pts", "safe (over 30 pts)"])
    P = lambda n, u: float(n / (n + u))
    for k in ["eday"] + kinds:
        n, u = div[f"{k}_ndp"].sum(), div[f"{k}_ucp"].sum()
        out["province"][k] = {"ndp": int(n), "ucp_bloc": int(u), "two_party": int(n + u), "ndp_share_pct": round(100 * P(n, u), 2),
                              "minus_eday_pts": round(100 * (P(n, u) - P(div.eday_ndp.sum(), div.eday_ucp.sum())), 2)}
    allk = kinds
    div["non_ndp"] = sum(div[f"{k}_ndp"] for k in allk)
    div["non_ucp"] = sum(div[f"{k}_ucp"] for k in allk)
    n, u = div.non_ndp.sum(), div.non_ucp.sum()
    out["province"]["all_non_election_day"] = {"ndp": int(n), "ucp_bloc": int(u), "two_party": int(n + u), "ndp_share_pct": round(100 * P(n, u), 2),
                                               "minus_eday_pts": round(100 * (P(n, u) - P(div.eday_ndp.sum(), div.eday_ucp.sum())), 2),
                                               "share_of_all_two_party_pct": round(100 * (n + u) / (n + u + div.eday_ndp.sum() + div.eday_ucp.sum()), 2)}
    div["non_share"] = div.non_ndp / (div.non_ndp + div.non_ucp)
    div["skew_pts"] = 100 * (div.non_share - div.eday_share)
    div["skew_logit"] = logit(div.non_share) - logit(div.eday_share)
    div["non_frac_of_votes"] = (div.non_ndp + div.non_ucp) / (div.non_ndp + div.non_ucp + div.eday_ndp + div.eday_ucp)
    for k in kinds:
        s = div[f"{k}_ndp"] / (div[f"{k}_ndp"] + div[f"{k}_ucp"]).replace(0, np.nan)
        div[f"{k}_skew_pts"] = 100 * (s - div.eday_share)
    d = div.skew_pts
    out["per_division_skew_pts"] = {"mean": round(d.mean(), 2), "median": round(d.median(), 2), "sd": round(d.std(), 2), "min": round(d.min(), 2),
                                    "max": round(d.max(), 2), "divisions_ndp_better_off_election_day": int((d > 0).sum()), "n": int(len(d)),
                                    "mean_logit_shift": round(div.skew_logit.mean(), 3), "sd_logit_shift": round(div.skew_logit.std(), 3)}
    for col, key in (("region", "by_region"), ("comp", "by_competitiveness")):
        for name, g in div.groupby(col, observed=True):
            e, a = P(g.eday_ndp.sum(), g.eday_ucp.sum()), P(g.non_ndp.sum(), g.non_ucp.sum())
            out[key].append({"group": str(name), "divisions": int(len(g)), "eday_ndp_pct": round(100 * e, 2), "non_eday_ndp_pct": round(100 * a, 2),
                                   "skew_pts": round(100 * (a - e), 2), "mean_division_skew_pts": round(g.skew_pts.mean(), 2),
                                   "mean_logit_shift": round(g.skew_logit.mean(), 3),
                                   "non_eday_share_of_votes_pct": round(100 * (g.non_ndp.sum() + g.non_ucp.sum()) / (g.non_ndp.sum() + g.non_ucp.sum() + g.eday_ndp.sum() + g.eday_ucp.sum()), 1)})
    # Across divisions: does the non-election-day vote follow the election-day vote one for one?
    w = (div.non_ndp + div.non_ucp).values
    a, b, se = wls_slope(logit(div.eday_share), logit(div.non_share), w)
    out["cross_division"]["logit_non_eday_on_logit_eday"] = {"intercept": round(a, 3), "slope": round(b, 3), "se": round(se, 3),
                                                            "corr": round(float(np.corrcoef(logit(div.eday_share), logit(div.non_share))[0, 1]), 4)}
    for k in kinds:
        ok = (div[f"{k}_ndp"] + div[f"{k}_ucp"]) > 50
        s = div.loc[ok, f"{k}_ndp"] / (div.loc[ok, f"{k}_ndp"] + div.loc[ok, f"{k}_ucp"])
        a, b, se = wls_slope(logit(div.eday_share[ok]), logit(s), (div.loc[ok, f"{k}_ndp"] + div.loc[ok, f"{k}_ucp"]).values)
        out["cross_division"][f"{k}_slope"] = {"intercept": round(a, 3), "slope": round(b, 3), "se": round(se, 3), "n": int(ok.sum())}
    r, p = stats.spearmanr(div.eday_share, div.skew_pts)
    out["cross_division"]["skew_pts_vs_eday_ndp_share_spearman"] = {"rho": round(float(r), 3), "p": float(p)}
    r, p = stats.spearmanr(div.eday_margin_pts, div.skew_pts)
    out["cross_division"]["skew_pts_vs_eday_margin_spearman"] = {"rho": round(float(r), 3), "p": float(p)}
    if "electors" in div and div.electors.notna().all():
        div["eday_rate"] = div.eday_valid / div.electors
        div["non_rate"] = div.non_valid / div.electors
        r, p = stats.pearsonr(div.eday_rate, div.non_rate)
        a, b, se = wls_slope(div.eday_rate, div.non_rate, div.electors.values)
        out["cross_division"]["non_eday_ballots_per_elector_vs_eday_ballots_per_elector"] = {
            "pearson_r": round(float(r), 3), "p": float(p), "slope": round(b, 3), "se": round(se, 3),
            "reading": "M0 weighting implies a positive slope through zero; a pure turnout-gap rule implies a negative slope"}
    return out


def y2023():
    raw = load_2023_rows()
    g = load_va()
    names = g.drop_duplicates("ed").set_index("ed").parent_ed_2019
    raw["k"] = raw.kind.map({"Election Day": "eday", "Advance": "advance", "Vote Anywhere": "vote_anywhere", "Mobile": "mobile", "Special Ballot": "special"})
    piv = raw.pivot_table(index="ed", columns="k", values=["ndp", "ucp", "valid"], aggfunc="sum").fillna(0)
    div = pd.DataFrame({f"{k}_{p}": piv[(p, k)] for p in ("ndp", "ucp", "valid") for k in piv["ndp"].columns})
    div["electors"] = raw[raw.kind == "Election Day"].groupby("ed").electors.sum()
    div["eday_valid"] = div["eday_valid"]
    div["non_valid"] = div[[c for c in div if c.endswith("_valid") and not c.startswith("eday")]].sum(axis=1)
    div["name"] = names
    div["region"] = div.name.map(region_of)
    kinds = ["advance", "vote_anywhere", "mobile", "special"]
    out = summarise(div, kinds, "2023, NDP share of NDP+UCP")
    # Named advance locations inside a division: do they all show the same party mix?
    adv = raw[raw.kind == "Advance"]
    chi, dof, ndiv, sig = 0.0, 0, 0, 0
    spread = []
    for ed, a in adv.groupby("ed"):
        a = a[(a.ndp + a.ucp) >= 30]
        if len(a) < 2:
            continue
        c, p, d, _ = stats.chi2_contingency(a[["ndp", "ucp"]].values, correction=False)
        chi += c; dof += d; ndiv += 1; sig += p < 0.05
        s = a.ndp / (a.ndp + a.ucp)
        spread.append(100 * (s.max() - s.min()))
    out["advance_locations_within_division"] = {
        "advance_location_rows": int(len(adv)), "divisions_with_2plus_locations": ndiv, "pooled_chi2": round(chi, 1), "dof": dof,
        "p_value": float(stats.chi2.sf(chi, dof)), "divisions_rejecting_same_mix_at_5pct": int(sig),
        "median_gap_between_most_and_least_ndp_location_pts": round(float(np.median(spread)), 1),
        "max_gap_pts": round(float(np.max(spread)), 1),
        "reading": "M0 says every advance voter group in a division has one party mix; a large chi-square rejects that"}
    # the same statistic for election-day stations, to scale the advance-location spread
    ed_ = raw[raw.kind == "Election Day"]
    sp2 = []
    for ed, a in ed_.groupby("ed"):
        a = a[(a.ndp + a.ucp) > 0]
        s = a.ndp / (a.ndp + a.ucp)
        sp2.append(100 * np.sqrt(np.average((s - np.average(s, weights=a.ndp + a.ucp)) ** 2, weights=a.ndp + a.ucp)))
    sp3 = []
    for ed, a in adv.groupby("ed"):
        if len(a) < 2:
            continue
        s = a.ndp / (a.ndp + a.ucp)
        sp3.append((ed, 100 * np.sqrt(np.average((s - np.average(s, weights=a.ndp + a.ucp)) ** 2, weights=a.ndp + a.ucp))))
    sp2 = pd.Series(sp2, index=sorted(ed_.ed.unique()))
    sp3 = pd.Series(dict(sp3))
    out["advance_locations_within_division"]["median_weighted_sd_pts_election_day_stations"] = round(float(sp2.median()), 2)
    out["advance_locations_within_division"]["median_weighted_sd_pts_advance_locations"] = round(float(sp3.median()), 2)
    r, p = stats.spearmanr(sp2.reindex(sp3.index), sp3)
    out["advance_locations_within_division"]["spearman_sd_advance_vs_sd_election_day"] = {"rho": round(float(r), 3), "p": float(p)}
    write_csv(div, "skew_2023_by_division.csv", index=True)
    return out


def y2015():
    import openpyxl
    wb = openpyxl.load_workbook(WORKBOOK_2015, read_only=True, data_only=True)
    rows = []
    for sn in wb.sheetnames:
        it = list(wb[sn].iter_rows(values_only=True))
        title = str(it[0][0]).replace("Summary Of Results By Poll -", "").strip()
        hdr = it[1]
        vcol = [i for i, h in enumerate(hdr) if h == "V"][0]
        party = {i: str(hdr[i]).split("\n")[-1].strip() for i in range(4, vcol)}
        for r in it[2:]:
            if not isinstance(r[0], (int, float)) or r[2] is None:
                continue
            nm = str(r[2]).strip()
            kind = "advance" if nm.upper().startswith("ADVANCE") else "mobile" if nm.upper().startswith("MOBILE") else \
                "special" if nm.upper().startswith("SPECIAL") else "eday"
            v = {p: 0 for p in ("NDP", "PC", "WRP")}
            for i, p in party.items():
                if p in v:
                    v[p] += r[i] or 0
            rows.append(dict(ed=sn, name=title, poll=nm, k=kind, ndp=v["NDP"], ucp=v["PC"] + v["WRP"], valid=r[vcol] or 0, electors=r[3]))
    raw = pd.DataFrame(rows)
    write_csv(raw, "polls_2015_parsed.csv")
    piv = raw.pivot_table(index="ed", columns="k", values=["ndp", "ucp", "valid"], aggfunc="sum").fillna(0)
    div = pd.DataFrame({f"{k}_{p}": piv[(p, k)] for p in ("ndp", "ucp", "valid") for k in piv["ndp"].columns})
    div["electors"] = raw[raw.k == "eday"].groupby("ed").electors.sum()
    div["non_valid"] = div[[c for c in div if c.endswith("_valid") and not c.startswith("eday")]].sum(axis=1)
    div["name"] = raw.drop_duplicates("ed").set_index("ed").name
    div["region"] = div.name.map(region_of)
    out = summarise(div, ["advance", "mobile", "special"], "2015, NDP share of NDP+PC+Wildrose")
    write_csv(div, "skew_2015_by_division.csv", index=True)
    return out


def main():
    res = {"y2023": y2023(), "y2015": y2015(),
           "note_2019": "No 2019 poll-level workbook is in the repository (only division totals in data/reference), so 2019 is not measured."}
    write_json("skew_summary.json", res, __file__, [WORKBOOK_2023, WORKBOOK_2015, VA_EDAY])
    for y in ("y2023", "y2015"):
        r = res[y]
        print("==", r["label"])
        for k, v in r["province"].items():
            print(f"  {k:22s} two-party {v['two_party']:>9,}  NDP {v['ndp_share_pct']:6.2f}%  vs election day {v['minus_eday_pts']:+.2f}")
        print("  per division:", r["per_division_skew_pts"])
        for k in ("by_region", "by_competitiveness"):
            for v in r[k]:
                print("  ", v)
        print("  cross:", json.dumps(r["cross_division"]))
        if "advance_locations_within_division" in r:
            print("  locations:", json.dumps(r["advance_locations_within_division"]))


if __name__ == "__main__":
    main()
