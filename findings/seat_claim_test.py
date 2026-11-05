# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
seat_claim_test.py
------------------

Runs the test in preregistration/seat_claim_test_2026-11-04.md (committed at da21f14b, before any
computation): do 2023's votes on the panel's 91 districts elect 50 UCP and 41 NDP?

  map        the panel's map as assembled by the registered Amendment 10 run
             (findings/a10_stepb_run/va_assignment_real_map.csv; every VA in one district)
  votes      A: all ballots (election day plus advance, mobile and special spread to VAs by election-day
                share: va_*_full); B: election-day ballots only (va_*)
  seats      most votes wins; va_other is all other parties combined, so a district where it leads is
             flagged rather than given to a party
  check      the same code on the 2019 map (parent_ed_2019) must give 49 UCP / 38 NDP on substrate A
  C (added after A failed the check, a disclosed deviation): A rescaled party by party within each 2019
             district so that district totals equal the official 2023 results, which makes the check exact
  undecided  a district whose margin is smaller than the votes in its cut VAs (cut by one of its changed
             lines), or whose winner changes when any one of its cut VAs with at least FLIP_MIN of its
             area on the other side is moved to its largest partner; the seat count is given as a range

Usage: python -W ignore findings/seat_claim_test.py OUT_JSON
"""
import json
import sys

import geopandas as gpd
import pandas as pd

ASSIGN = "findings/a10_stepb_run/va_assignment_real_map.csv"
REPORT = "findings/a10_stepb_run/report_real_map.json"
VOTES = "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg"
OFFICIAL = "data/reference/alberta_2023_results.csv"
FLIP_MIN = 0.10
CLOSE_PTS = 2.0


def tally(v, key, cols):
    t = v.groupby(key)[cols].sum()
    t.columns = ["ucp", "ndp", "oth"]
    t["winner"] = t[["ucp", "ndp", "oth"]].idxmax(axis=1)
    tot = t[["ucp", "ndp", "oth"]].sum(axis=1)
    top2 = t[["ucp", "ndp", "oth"]].apply(lambda r: sorted(r, reverse=True)[:2], axis=1)
    t["margin_votes"] = top2.map(lambda x: x[0] - x[1])
    t["margin_pts"] = 100 * t.margin_votes / tot
    return t


def seats(t):
    return {"UCP": int((t.winner == "ucp").sum()), "NDP": int((t.winner == "ndp").sum()), "other_combined": int((t.winner == "oth").sum())}


def partners(s):
    if not isinstance(s, str) or not s:
        return {}
    out = {}
    for part in s.split(";"):
        n, x = part.rsplit(":", 1)
        out[n] = float(x)
    return out


def main():
    out = sys.argv[1]
    v = gpd.read_file(VOTES, ignore_geometry=True)
    a = pd.read_csv(ASSIGN)
    assert len(v) == len(a) and (v.OBJECTID.values == a.OBJECTID.values).all()
    v["district"] = a.district.values
    v["cut"] = a.cut.astype(str).str.lower().eq("true").values
    v["partners"] = a.cut_partners.map(partners).values
    with open(REPORT, encoding="utf-8") as f:
        src = {r["district"]: r["source"] for r in json.load(f)["districts"]}
    # Substrate C (added after the step-4 method check failed on A; see the result file): A rescaled, party
    # by party within each 2019 district, so every district's totals equal the official 2023 results.
    off = pd.read_csv(OFFICIAL).set_index("ed_name")
    def party(row, p):
        for i in range(1, 7):
            c = row.get(f"cand_{i}")
            if isinstance(c, str) and c.endswith(f"({p})"):
                return row[f"votes_{i}"]
        return 0
    off["UCP"] = off.apply(lambda r: party(r, "UCP"), axis=1)
    off["NDP"] = off.apply(lambda r: party(r, "NDP"), axis=1)
    off["OTH"] = off.total_valid_votes - off.UCP - off.NDP
    sub = v.groupby("parent_ed_2019")[["va_ucp_full", "va_ndp_full", "va_other_full"]].sum()
    for c, o in (("va_ucp_full", "UCP"), ("va_ndp_full", "NDP"), ("va_other_full", "OTH")):
        f = (off[o] / sub[c]).fillna(0.0)
        v[c.replace("_full", "_cal")] = v[c] * v.parent_ed_2019.map(f).fillna(0.0)
    res = {"test_plan": "preregistration/seat_claim_test_2026-11-04.md (da21f14b)", "claim": {"UCP": 50, "NDP": 41},
           "substrate_A_coverage": {"ucp_votes": float(sub.va_ucp_full.sum()), "official_ucp": float(off.UCP.sum()),
                                    "ndp_votes": float(sub.va_ndp_full.sum()), "official_ndp": float(off.NDP.sum())}}
    for tag, cols in (("A_all_ballots", ["va_ucp_full", "va_ndp_full", "va_other_full"]),
                      ("B_election_day", ["va_ucp", "va_ndp", "va_other"]),
                      ("C_all_ballots_scaled_to_official", ["va_ucp_cal", "va_ndp_cal", "va_other_cal"])):
        chk = seats(tally(v, "parent_ed_2019", cols))
        t = tally(v, "district", cols)
        base = seats(t)
        # undecided districts
        und = {}
        cutvotes = v[v.cut].assign(tot=v[v.cut][cols].sum(axis=1))
        changed = {d for d, s in src.items() if s != "known"}
        for i, r in cutvotes.iterrows():
            for n, sh in r.partners.items():
                if r.district not in changed and n not in changed:
                    continue  # a cut between two known districts is the official map's own line
                for d in (r.district, n):
                    und.setdefault(d, {"cut_votes": 0.0, "flips": []})
                und[r.district]["cut_votes"] += r.tot
                if sh >= FLIP_MIN:
                    dist2 = v.district.copy()
                    dist2.loc[i] = n
                    t2 = tally(v.assign(district=dist2), "district", cols)
                    for d in (r.district, n):
                        if t2.loc[d, "winner"] != t.loc[d, "winner"]:
                            und[d]["flips"].append(int(r.OBJECTID))
        undecided = sorted(d for d, u in und.items()
                           if d in t.index and (u["cut_votes"] > t.loc[d, "margin_votes"] or u["flips"]))
        lo = {"UCP": base["UCP"] - sum(t.loc[d, "winner"] == "ucp" for d in undecided),
              "NDP": base["NDP"] - sum(t.loc[d, "winner"] == "ndp" for d in undecided)}
        rng = {"UCP": [lo["UCP"], lo["UCP"] + len(undecided)], "NDP": [lo["NDP"], lo["NDP"] + len(undecided)]}
        close = t[t.margin_pts < CLOSE_PTS].sort_values("margin_pts")
        res[tag] = {
            "method_check_2019_map": chk, "method_check_passes": chk["UCP"] == 49 and chk["NDP"] == 38,
            "seats": base, "matches_claim": base["UCP"] == 50 and base["NDP"] == 41,
            "undecided_by_reconstruction": [{"district": d, "winner": t.loc[d, "winner"], "margin_votes": round(float(t.loc[d, "margin_votes"]), 1),
                                             "margin_pts": round(float(t.loc[d, "margin_pts"]), 2), "cut_votes": round(und[d]["cut_votes"], 1),
                                             "flip_vas": und[d]["flips"]} for d in undecided],
            "seat_range_over_undecided": rng,
            "close_districts_under_2pts": [{"district": d, "winner": r.winner, "margin_pts": round(float(r.margin_pts), 2),
                                            "source": src.get(d)} for d, r in close.iterrows()],
            "districts": {d: {"winner": r.winner, "ucp": round(float(r.ucp), 1), "ndp": round(float(r.ndp), 1),
                              "other": round(float(r.oth), 1), "margin_pts": round(float(r.margin_pts), 2), "source": src.get(d)}
                          for d, r in t.iterrows()},
        }
        print(tag, "2019 check", chk, "| panel map", base, "| matches claim", res[tag]["matches_claim"],
              "| undecided", len(undecided), rng)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
