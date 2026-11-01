# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
airdrie_split_shares.py
-----------------------

How each 2026 commission map divides the City of Airdrie, counted by people.

For the majority and minority maps (Elections Alberta's official 2026
boundaries), 2021 census dissemination areas (DAs) are laid over the
districts. A DA belongs to Airdrie when its representative point lies in the
Airdrie census subdivision (CSDUID 4806021, 2021 limits). Where a district
line cuts a DA, the DA's people are shared out by area (people assumed spread
evenly inside the DA).

Per district holding any Airdrie residents it reports:
  district_pop_2021_da      the district's 2021 population from the DA overlay
  district_pop_official     the PopCensus field on the official boundary file
                            (the commission's own figure, 2024 basis)
  airdrie_residents         Airdrie's 2021 residents in the district
  share_of_district_airdrie airdrie_residents / district_pop_2021_da
  share_of_airdrie_held     airdrie_residents / Airdrie's 2021 total
  airdrie_from_whole_das    part of airdrie_residents from DAs lying (>= 99%
                            of their area) in this district
  airdrie_from_cut_das      part from DAs that a district line cuts (no
                            district holds 99% of the DA's area)
  rests_only_on_cut_das     true when airdrie_from_whole_das is 0, i.e. the
                            district's Airdrie count is area sharing alone
  piece_2pct                true when the district holds >= 2% of Airdrie's
                            people (Amendment 17's piece rule)
  airdrie_land_km2          square kilometres of Airdrie (2021 CSD limits) in the district
  residents_by_csd_top3     the district's three largest 2021 CSDs by residents
                            (who outnumbers whom)
A second assignment, every DA whole to the district holding its
representative point, is reported beside it as a check.

Backward: data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg,
  data/shapefiles/reference/alberta_2021_das.gpkg,
  data/shapefiles/reference/alberta_2021_csds.gpkg,
  data/reference/alberta_2021_da_populations.csv,
  data/reference/alberta_2021_csd_populations.csv
Forward: data/outputs/airdrie_split_shares_2026-10-31.json

Usage
  python analysis/scripts/airdrie_split_shares.py [--out PATH]
"""
import argparse
import json
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
MAPS = {
    "majority": "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
    "minority": "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
}
NAME = "EDName2025"
AIRDRIE_CSDUID = "4806021"
WHOLE = 0.99  # a DA is whole when one district holds at least this share of its area
PIECE = 0.02  # Amendment 17's piece rule
DEFAULT_OUT = REPO / "data/outputs/airdrie_split_shares_2026-10-31.json"


def load_das(crs):
    da = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_das.gpkg").to_crs(crs)
    pops = pd.read_csv(REPO / "data/reference/alberta_2021_da_populations.csv").set_index("DGUID")
    da["pop"] = da["DGUID"].map(pops["population_2021"]).fillna(0.0)
    csd = gpd.read_file(REPO / "data/shapefiles/reference/alberta_2021_csds.gpkg").to_crs(crs)
    airdrie = csd[csd["CSDUID"].astype(str) == AIRDRIE_CSDUID]
    assert len(airdrie) == 1, "Airdrie CSD not found"
    pt = da[["DGUID", "geometry"]].copy()
    pt["geometry"] = da.geometry.representative_point()
    inside = gpd.sjoin(pt, airdrie[["geometry"]], how="inner", predicate="within")["DGUID"]
    da["airdrie"] = da["DGUID"].isin(set(inside))
    j = gpd.sjoin(pt, csd[["CSDNAME", "geometry"]], how="left", predicate="within")
    da["csd"] = da["DGUID"].map(j.drop_duplicates("DGUID").set_index("DGUID")["CSDNAME"]).fillna("(none)")
    return da, pt, airdrie.geometry.iloc[0]


def split_map(da, pt, eds, airdrie_shape):
    o = gpd.overlay(da[["DGUID", "pop", "airdrie", "csd", "geometry"]], eds[[NAME, "geometry"]],
                    how="intersection", keep_geom_type=True)
    o["a"] = o.area
    o["w"] = o["a"] / o.groupby("DGUID")["a"].transform("sum")
    o["p"] = o["pop"] * o["w"]
    o["whole"] = o.groupby("DGUID")["w"].transform("max") >= WHOLE
    o["main"] = o["w"] == o.groupby("DGUID")["w"].transform("max")

    # check: whole-DA assignment by representative point
    rp = gpd.sjoin(pt, eds[[NAME, "geometry"]], how="left", predicate="within")
    rp = rp.drop_duplicates("DGUID").set_index("DGUID")[NAME]
    da_rp = da.assign(ed=da["DGUID"].map(rp))

    air = o[o["airdrie"]]
    air_total = float(da.loc[da["airdrie"], "pop"].sum())
    district_pop = o.groupby(NAME)["p"].sum()
    official = eds.set_index(NAME)["PopCensus"]
    rp_air = da_rp[da_rp["airdrie"]].groupby("ed")["pop"].sum()
    rp_all = da_rp.groupby("ed")["pop"].sum()
    by_csd = o.groupby([NAME, "csd"])["p"].sum()
    land = eds.set_index(NAME).geometry.intersection(airdrie_shape).area / 1e6

    rows = []
    for ed, g in air.groupby(NAME):
        res = float(g["p"].sum())
        whole_main = float(g.loc[g["whole"] & g["main"], "p"].sum())
        cut = float(g.loc[~g["whole"], "p"].sum())
        sliver = float(g.loc[g["whole"] & ~g["main"], "p"].sum())
        rows.append({
            "district": ed,
            "district_pop_2021_da": round(float(district_pop[ed])),
            "district_pop_official": int(official[ed]),
            "airdrie_residents": round(res),
            "share_of_district_airdrie": round(res / float(district_pop[ed]), 4),
            "share_of_airdrie_held": round(res / air_total, 4),
            "airdrie_from_whole_das": round(whole_main),
            "airdrie_from_cut_das": round(cut),
            "airdrie_from_slivers_of_whole_das": round(sliver, 1),
            "rests_only_on_cut_das": whole_main == 0,
            "piece_2pct": res / air_total >= PIECE,
            "check_rep_point_airdrie_residents": int(rp_air.get(ed, 0)),
            "check_rep_point_share_of_district_airdrie":
                round(float(rp_air.get(ed, 0)) / float(rp_all[ed]), 4) if ed in rp_all else None,
            "airdrie_land_km2": round(float(land[ed]), 2),
            "residents_by_csd_top3": {k: round(float(v)) for k, v in
                                      by_csd[ed].sort_values(ascending=False).head(3).items()},
        })
    rows.sort(key=lambda r: -r["airdrie_residents"])
    material = [r for r in rows if r["airdrie_residents"] >= 1]
    n_cut = int(air.loc[~air["whole"], "DGUID"].nunique())
    return {
        "airdrie_total_2021_da": round(air_total),
        "airdrie_das": int(da["airdrie"].sum()),
        "airdrie_das_cut_by_a_district_line": n_cut,
        "districts_with_any_airdrie_residents": len(material),
        "districts_holding_2pct_or_more": sum(r["piece_2pct"] for r in rows),
        "districts_where_airdrie_is_a_majority": [r["district"] for r in material
                                                  if r["share_of_district_airdrie"] > 0.5],
        "districts": material,
        "below_one_resident": [r["district"] for r in rows if r["airdrie_residents"] < 1],
    }


def main(out):
    warnings.filterwarnings("ignore")
    result = {
        "script": "analysis/scripts/airdrie_split_shares.py",
        "method": ("2021 census DAs over Elections Alberta's official 2026 boundaries; a DA is in "
                   "Airdrie when its representative point lies in CSD 4806021; DAs cut by a "
                   "district line shared out by area; a DA is whole when one district holds "
                   f">= {WHOLE:.0%} of its area; piece rule = >= {PIECE:.0%} of Airdrie's people "
                   "(Amendment 17)."),
        "airdrie_2021_census_csd": int(pd.read_csv(REPO / "data/reference/alberta_2021_csd_populations.csv")
                                       .set_index("ALT_GEO_CODE").loc[int(AIRDRIE_CSDUID), "population_2021"]),
        "maps": {},
    }
    da = pt = shape = None
    for plan, path in MAPS.items():
        eds = gpd.read_file(REPO / path)
        if da is None:
            da, pt, shape = load_das(eds.crs)
        result["maps"][plan] = split_map(da, pt, eds, shape)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    for plan, m in result["maps"].items():
        print(f"\n{plan}: Airdrie 2021 (DA sum) {m['airdrie_total_2021_da']:,} "
              f"in {m['airdrie_das']} DAs, {m['airdrie_das_cut_by_a_district_line']} cut")
        print(f"  {'district':34s} {'dist pop':>9s} {'official':>9s} {'Airdrie':>8s} "
              f"{'% dist':>7s} {'% city':>7s} {'whole':>7s} {'cut':>6s}  only-cut  rep-pt")
        for r in m["districts"]:
            print(f"  {r['district']:34s} {r['district_pop_2021_da']:9,} {r['district_pop_official']:9,} "
                  f"{r['airdrie_residents']:8,} {r['share_of_district_airdrie']:7.1%} "
                  f"{r['share_of_airdrie_held']:7.1%} {r['airdrie_from_whole_das']:7,} "
                  f"{r['airdrie_from_cut_das']:6,}  {str(r['rests_only_on_cut_das']):8s}  "
                  f"{r['check_rep_point_airdrie_residents']:,}")
    print(f"\nwrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    main(ap.parse_args().out)
