# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
vote_anywhere_splat.py
----------------------

Adds the 2023 "Vote Anywhere (Out of ED)" advance ballots to the all-ballots VA substrate.

advance_vote_splat.py excludes them (its step C5) because a Vote Anywhere ballot is not cast at
a poll tied to particular VAs. Elections Alberta still reports each one under the voter's own 2019
district, so it can be spread over that district's VAs by the same rule the other non-election-day
ballots use: each VA's share of the district's election-day two-party vote (equal shares if the
district has none). Without them the substrate holds 854,502 UCP and 689,637 NDP votes against the
official 928,900 and 777,404; the missing ballots lean NDP, so the shortfall is not neutral.

Reads   data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg (left unchanged)
        data/outputs/polls_2023_unified.csv
        data/reference/alberta_2023_results.csv (check only)
Writes  data/shapefiles/derived/va_polygons_with_all_2023_ballots.gpkg
        (va_*_full as in the input; va_*_all = va_*_full + Vote Anywhere share)
        with --primary: also data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg, the
        election-day file (va_polygons_with_2023_votes.gpkg, same rows and geometry) with va_ndp, va_ucp
        and va_other replaced by the all-ballots values, for scripts that read only those columns
        (e.g. mcmc_ensemble_canonical.py --va-file)

Exits non-zero unless every 2019 district's UCP, NDP and other totals equal the official results.

Usage: python -W ignore analysis/scripts/vote_anywhere_splat.py [--primary]
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
VA_IN = ROOT / "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg"
POLLS = ROOT / "data/outputs/polls_2023_unified.csv"
OFFICIAL = ROOT / "data/reference/alberta_2023_results.csv"
VA_OUT = ROOT / "data/shapefiles/derived/va_polygons_with_all_2023_ballots.gpkg"
VA_ED = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
VA_PRIMARY = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
PARTIES = (("ucp", "ucp_votes"), ("ndp", "ndp_votes"), ("other", "other_votes"))


def official_totals():
    off = pd.read_csv(OFFICIAL).set_index("ed_name")

    def party(row, p):
        for i in range(1, 7):
            c = row.get(f"cand_{i}")
            if isinstance(c, str) and c.endswith(f"({p})"):
                return row[f"votes_{i}"]
        return 0

    out = pd.DataFrame(index=off.index)
    out["ucp"] = off.apply(lambda r: party(r, "UCP"), axis=1)
    out["ndp"] = off.apply(lambda r: party(r, "NDP"), axis=1)
    out["other"] = off.total_valid_votes - out.ucp - out.ndp
    return out


def main():
    va = gpd.read_file(VA_IN)
    polls = pd.read_csv(POLLS, dtype={"sheet_num": str, "voting_areas": str}, encoding="cp1252")
    for _, col in PARTIES:
        polls[col] = pd.to_numeric(polls[col], errors="coerce").fillna(0)
    anywhere = polls[polls.poll_name.str.contains("Vote Anywhere", na=False, case=False)]
    add = anywhere.groupby("ed_2019")[[c for _, c in PARTIES]].sum()
    missing = set(add.index) - set(va.parent_ed_2019)
    if missing:
        sys.exit(f"Vote Anywhere districts not in the substrate: {sorted(missing)}")

    w = va.va_ucp + va.va_ndp
    tot = w.groupby(va.parent_ed_2019).transform("sum")
    n = va.groupby("parent_ed_2019").va_ucp.transform("size")
    share = (w / tot).where(tot > 0, 1.0 / n)
    for p, col in PARTIES:
        va[f"va_{p}_all"] = va[f"va_{p}_full"] + share * va.parent_ed_2019.map(add[col]).fillna(0.0)

    got = va.groupby("parent_ed_2019")[[f"va_{p}_all" for p, _ in PARTIES]].sum()
    got.columns = [p for p, _ in PARTIES]
    off = official_totals().reindex(got.index)
    diff = (got - off).abs()
    print(f"Vote Anywhere added: UCP {add.ucp_votes.sum():,.0f}  NDP {add.ndp_votes.sum():,.0f}  "
          f"other {add.other_votes.sum():,.0f} across {len(add)} districts")
    print(f"Province: UCP {got.ucp.sum():,.1f} (official {off.ucp.sum():,})  NDP {got.ndp.sum():,.1f} "
          f"(official {off.ndp.sum():,})  other {got.other.sum():,.1f} (official {off.other.sum():,})")
    bad = diff[(diff > 0.5).any(axis=1)]
    if len(bad):
        print(f"FAIL: {len(bad)} districts differ from the official results by more than half a vote:")
        print(pd.concat([got.loc[bad.index], off.loc[bad.index]], axis=1, keys=["substrate", "official"]).to_string())
        sys.exit(1)
    va.to_file(VA_OUT, driver="GPKG")
    print(f"PASS: all {len(got)} districts equal the official results; wrote {VA_OUT.relative_to(ROOT)}")
    if "--primary" in sys.argv:
        ed = gpd.read_file(VA_ED)
        if not (ed.OBJECTID.values == va.OBJECTID.values).all():
            sys.exit("election-day file rows do not match")
        for p, _ in PARTIES:
            ed[f"va_{p}"] = va[f"va_{p}_all"].values
        ed.to_file(VA_PRIMARY, driver="GPKG")
        print(f"wrote {VA_PRIMARY.relative_to(ROOT)} (va_ndp/va_ucp/va_other = all ballots)")


if __name__ == "__main__":
    main()
