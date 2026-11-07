# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada 2021 Census Profile (Open Government Licence - Canada) | Elections Alberta (public domain)
"""
census_eligibility.py

Runs preregistration/census_eligibility_check_2026-11-07.md: how much of a division's low elector count
does the 2021 census eligible share (Canadian citizens 18 and over) explain? Unregistered. Applies no
legal test. Eligibility is never inferred from ancestry; visible minority shares are description only.

Reads   data/census_2021/alberta_da_profile.csv (built by --build from the API extracts)
        data/shapefiles/reference/alberta_2021_das.gpkg, findings/referendum_electors/division_table.csv
        data/shapefiles/canonical/ea_majority_2026_eds.gpkg, data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg
Writes  findings/referendum_electors/census_eligibility.json, census_division_table.csv

Usage: python -W ignore findings/referendum_electors/census_eligibility.py [--build DIR]
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROFILE = ROOT / "data/census_2021/alberta_da_profile.csv"
DAS = ROOT / "data/shapefiles/reference/alberta_2021_das.gpkg"
MAPS = {"majority": (ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "panel": (ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district")}
FIELDS = {1: "pop_2021", 8: "age_total", 9: "age_0_14", 1508: "citizenship_total", 1511: "citizens_18_plus", 1512: "not_citizens",
          1513: "immigrant_status_total", 1515: "immigrants", 1523: "non_permanent_residents", 1669: "vismin_total",
          1670: "visible_minority", 1671: "south_asian", 1672: "chinese", 1674: "filipino"}
NAMED = ["Calgary-North East", "Calgary-Bhullar-McCall", "Calgary-Falconridge-Conrich"]
PROVINCE_ELECTORS = 3286778
PROVINCE_STATED = 4888723
MAX_SUPPRESSED = 0.05


def build(src):
    out = None
    for c, name in FIELDS.items():
        d = pd.read_csv(Path(src) / f"c{c}.csv", usecols=["ALT_GEO_CODE", "OBS_VALUE"], dtype={"ALT_GEO_CODE": str})
        d = d.rename(columns={"ALT_GEO_CODE": "DAUID", "OBS_VALUE": name})
        out = d if out is None else out.merge(d, on="DAUID", how="outer")
    PROFILE.parent.mkdir(exist_ok=True)
    out.sort_values("DAUID").to_csv(PROFILE, index=False)
    print("built", PROFILE, out.shape)


def miss(actual, predicted):
    return round(100 * float((actual / predicted - 1).abs().mean()), 1)


def main():
    if "--build" in sys.argv:
        build(sys.argv[sys.argv.index("--build") + 1])
    p = pd.read_csv(PROFILE, dtype={"DAUID": str})
    da = gpd.read_file(DAS).to_crs(3400)
    print("DA columns", list(da.columns)[:8], len(da))
    key = next(c for c in da.columns if c.upper() == "DAUID")
    da[key] = da[key].astype(str)
    pts = da[[key, "geometry"]].copy()
    pts["geometry"] = da.geometry.representative_point()
    missing = p.citizens_18_plus.isna() | p.citizenship_total.isna() | (p.citizenship_total == 0)
    total = p.pop_2021.sum()
    out = {"plan": "preregistration/census_eligibility_check_2026-11-07.md",
           "coverage": {"das_in_profile": int(len(p)), "das_in_polygons": int(len(da)), "pop_2021_total": float(total),
                        "share_pop_without_eligibility_figure": round(float(p.pop_2021[missing].sum() / total), 4),
                        "province_eligible_share": round(float(p.citizens_18_plus.sum() / p.citizenship_total.sum()), 4)}}
    print(out["coverage"])
    out["reliable"] = out["coverage"]["share_pop_without_eligibility_figure"] <= MAX_SUPPRESSED

    t = pd.read_csv(HERE / "division_table.csv")
    rows = []
    for k, (f, col) in MAPS.items():
        eds = gpd.read_file(f).to_crs(3400)[[col, "geometry"]]
        j = gpd.sjoin(pts, eds, how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].rename(columns={col: "division"})[[key, "division"]]
        m = p.merge(j, left_on="DAUID", right_on=key, how="left")
        unplaced = float(m.pop_2021[m.division.isna()].sum())
        g = m.groupby("division")[list(FIELDS.values())].sum()
        x = t[t["map"] == k].set_index("division")
        g = g.reindex(x.index)
        share = g.citizens_18_plus / g.citizenship_total
        raw = share * x.stated_pop
        scale = x.electors_2026.sum() / raw.sum()
        expected = raw * scale
        plain = x.stated_pop * (x.electors_2026.sum() / x.stated_pop.sum())
        ratio = x.electors_2026 / x.stated_pop
        prov = PROVINCE_ELECTORS / PROVINCE_STATED
        adj_ratio = expected / x.stated_pop
        explained = (prov - adj_ratio) / (prov - ratio)
        urban = x.index.str.startswith(("Calgary-", "Edmonton-"))
        tab = pd.DataFrame({"map": k, "electors_2026": x.electors_2026, "stated_pop": x.stated_pop, "overlay_2021": x.overlay_2021,
                            "census_route_pop_2021": g.pop_2021.round(), "electors_per_stated": ratio.round(3),
                            "eligible_share_2021": share.round(3), "citizens_18_plus_2021": g.citizens_18_plus.round(),
                            "expected_electors": expected.round(), "left_over": (x.electors_2026 / expected).round(3),
                            "share_of_gap_explained": explained.round(3),
                            "under_15_share": (g.age_0_14 / g.age_total).round(3), "not_citizen_share": (g.not_citizens / g.citizenship_total).round(3),
                            "immigrant_share": (g.immigrants / g.immigrant_status_total).round(3),
                            "non_permanent_share": (g.non_permanent_residents / g.immigrant_status_total).round(3),
                            "visible_minority_share": (g.visible_minority / g.vismin_total).round(3),
                            "south_asian_share": (g.south_asian / g.vismin_total).round(3), "chinese_share": (g.chinese / g.vismin_total).round(3),
                            "filipino_share": (g.filipino / g.vismin_total).round(3)})
        rows.append(tab.reset_index())
        low = tab[tab.electors_per_stated < prov].sort_values("electors_per_stated")
        out[k] = {"scale_factor": round(float(scale), 4), "pop_2021_unplaced": unplaced,
                  "census_route_vs_overlay_mean_abs_pct": miss(g.pop_2021, x.overlay_2021),
                  "miss_vs_electors": {"stated_only": {"all": miss(x.electors_2026, plain), "cities": miss(x.electors_2026[urban], plain[urban]), "rest": miss(x.electors_2026[~urban], plain[~urban])},
                                       "with_census_eligibility": {"all": miss(x.electors_2026, expected), "cities": miss(x.electors_2026[urban], expected[urban]), "rest": miss(x.electors_2026[~urban], expected[~urban])}},
                  "named": tab.loc[[n for n in NAMED if n in tab.index]].drop(columns="map").to_dict("index"),
                  "lowest_ratio": low.head(12)[["electors_2026", "stated_pop", "electors_per_stated", "eligible_share_2021", "left_over", "share_of_gap_explained", "not_citizen_share", "non_permanent_share", "visible_minority_share"]].to_dict("index"),
                  "lowest_left_over": tab.sort_values("left_over").head(10)[["electors_per_stated", "eligible_share_2021", "left_over", "not_citizen_share"]].to_dict("index"),
                  "highest_left_over": tab.sort_values("left_over").tail(6)[["electors_per_stated", "eligible_share_2021", "left_over"]].to_dict("index"),
                  "highest_visible_minority": tab.sort_values("visible_minority_share").tail(8)[["visible_minority_share", "south_asian_share", "chinese_share", "filipino_share", "electors_per_stated"]].to_dict("index")}
    pd.concat(rows).to_csv(HERE / "census_division_table.csv", index=False)
    (HERE / "census_eligibility.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf8")
    print(json.dumps(out, indent=0, default=float)[:9000])


if __name__ == "__main__":
    main()
