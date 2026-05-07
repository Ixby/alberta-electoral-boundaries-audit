"""
Track L - Province-wide ED drift table (DA-based, accurate aggregation).

Builds a DA-to-ED crosswalk via spatial overlay, then:
- Plan A: 2021 Census populations aggregated to each ED.
- Plan B: Plan A scaled by per-DA growth factors to a mid-2025 target.
- Per-ED deviation from provincial mean under each plan.
- Legal-window status (pass / s.15(2) / fail) under each plan.

Why DA-level aggregation:
CSD-level area-weighted aggregation fails badly in urban areas because the
Calgary or Edmonton CSD is a single polygon that crosses many small-area EDs;
area-weighting gives each ED a proportionate area share but NOT a proportionate
population share (density varies). Dissemination areas (DAs) are much smaller
(roughly 400-700 people each in urban Alberta; 6,203 DAs province-wide) and
usually fit inside a single ED. When a DA does split across two EDs, area-
weighting is a defensible approximation at that finer scale.

DAs are joined to CSDs by spatial containment (DA centroid in CSD polygon);
the CSD identity carries the per-CSD growth rate.

Outputs:
- data/province_wide_drift_2019.csv
- data/province_wide_drift_majority.csv
- data/province_wide_drift_minority.csv
"""

# Version: 0.1 series  (last updated 2026-04-26)


import os
import sys
import warnings
from pathlib import Path

import pandas as pd
import geopandas as gpd

warnings.filterwarnings("ignore")
os.environ["PYTHONIOENCODING"] = "utf-8"

ROOT = str(Path(__file__).resolve().parent.parent.parent)
DATA = os.path.join(ROOT, "data")

# Alberta TBF and StatsCan-published annual growth rates, 2021 (May census)
# to mid-2025 (Q2). Provincial reconciliation target is Q2 2025 population.
# Source: StatsCan Table 17-10-0009; Alberta TBF quarterly population reports;
# municipal census publications (Airdrie 2024, Chestermere 2025, etc.).
AB_2021_CENSUS_TOTAL = 4_262_635
AB_Q2_2025_TARGET = 5_020_000
PROVINCIAL_CUMULATIVE_GROWTH = AB_Q2_2025_TARGET / AB_2021_CENSUS_TOTAL  # roughly 1.178

# Per-CSD cumulative 2021->mid-2025 growth factors.
# Urban high-growth: from published municipal census or Alberta Regional
# Dashboard. Resource-dependent: near-flat. Remote/Indigenous: conservative.
CSD_GROWTH_FACTORS = {
    # Calgary CMA core and ring
    "Calgary, City (CY)": 1.195,
    "Airdrie, City (CY)": 1.310,
    "Chestermere, City (CY)": 1.352,
    "Cochrane, Town (T)": 1.205,
    "Okotoks, Town (T)": 1.155,
    "High River, Town (T)": 1.105,
    "Rocky View County, Municipal district (MD)": 1.165,
    "Foothills County, Municipal district (MD)": 1.105,
    "Strathmore, Town (T)": 1.145,
    "Canmore, Town (T)": 1.095,
    "Banff, Town (T)": 1.075,
    "Crossfield, Town (T)": 1.115,
    # Edmonton CMA
    "Edmonton, City (CY)": 1.205,
    "St. Albert, City (CY)": 1.105,
    "Sherwood Park, Urban service area (USA)": 1.110,
    "Strathcona County, Specialized municipality (SM)": 1.110,
    "Fort Saskatchewan, City (CY)": 1.150,
    "Sturgeon County, Municipal district (MD)": 1.105,
    "Leduc, City (CY)": 1.175,
    "Leduc County, Municipal district (MD)": 1.125,
    "Beaumont, City (CY)": 1.225,
    "Spruce Grove, City (CY)": 1.150,
    "Stony Plain, Town (T)": 1.145,
    "Parkland County, Municipal district (MD)": 1.105,
    "Devon, Town (T)": 1.095,
    "Morinville, Town (T)": 1.115,
    "Bon Accord, Town (T)": 1.075,
    "Gibbons, Town (T)": 1.075,
    "Redwater, Town (T)": 1.065,
    "Thorsby, Town (T)": 1.065,
    "Calmar, Town (T)": 1.075,
    "Warburg, Village (VL)": 1.055,
    # Red Deer CMA
    "Red Deer, City (CY)": 1.100,
    "Red Deer County, Municipal district (MD)": 1.105,
    "Lacombe, City (CY)": 1.105,
    "Lacombe County, Municipal district (MD)": 1.085,
    "Blackfalds, Town (T)": 1.165,
    "Innisfail, Town (T)": 1.095,
    "Sylvan Lake, Town (T)": 1.125,
    "Rimbey, Town (T)": 1.055,
    "Ponoka, Town (T)": 1.085,
    "Ponoka County, Municipal district (MD)": 1.065,
    # Lethbridge CMA
    "Lethbridge, City (CY)": 1.110,
    "Lethbridge County, Municipal district (MD)": 1.085,
    "Coaldale, Town (T)": 1.115,
    "Cardston, Town (T)": 1.065,
    "Cardston County, Municipal district (MD)": 1.065,
    "Taber, Town (T)": 1.095,
    "Taber, Municipal district (MD)": 1.075,
    # Medicine Hat
    "Medicine Hat, City (CY)": 1.080,
    "Cypress County, Municipal district (MD)": 1.065,
    "Brooks, City (CY)": 1.095,
    "Newell County, Municipal district (MD)": 1.075,
    # Other larger centres
    "Grande Prairie, City (CY)": 1.065,
    "Grande Prairie County No. 1, Municipal district (MD)": 1.065,
    "Wood Buffalo, Specialized municipality (SM)": 0.990,
    "Cold Lake, City (CY)": 1.045,
    "Lac La Biche County, Specialized municipality (SM)": 1.045,
    "St. Paul, Town (T)": 1.055,
    "St. Paul County No. 19, Municipal district (MD)": 1.045,
    "Bonnyville, Town (T)": 1.045,
    "Camrose, City (CY)": 1.075,
    "Camrose County, Municipal district (MD)": 1.055,
    "Wetaskiwin, City (CY)": 1.085,
    "Vegreville, Town (T)": 1.045,
    "Drayton Valley, Town (T)": 1.045,
    "Drumheller, Town (T)": 1.035,
    "Stettler, Town (T)": 1.045,
    "Olds, Town (T)": 1.085,
    "Didsbury, Town (T)": 1.075,
    "Peace River, Town (T)": 1.045,
    "Hinton, Town (T)": 1.045,
    "Edson, Town (T)": 1.045,
    "Jasper, Specialized municipality (SM)": 1.015,
    "Rocky Mountain House, Town (T)": 1.045,
    "Whitecourt, Town (T)": 1.045,
    "Slave Lake, Town (T)": 1.035,
    "High Level, Town (T)": 1.015,
    "Barrhead, Town (T)": 1.045,
    "Mayerthorpe, Town (T)": 1.035,
    "Athabasca, Town (T)": 1.045,
    "Westlock, Town (T)": 1.045,
    "Fort Macleod, Town (T)": 1.055,
    "Pincher Creek, Town (T)": 1.045,
    "Claresholm, Town (T)": 1.055,
    "Vulcan, Town (T)": 1.045,
    "Three Hills, Town (T)": 1.045,
    "Vermilion, Town (T)": 1.045,
    "Wainwright, Town (T)": 1.055,
    "Lloydminster, City (CY)": 1.065,
}

DEFAULT_GROWTH = {
    "urban_high": 1.160,
    "rural_md": 1.070,
    "rural_town": 1.065,
    "first_nation": 1.040,
    "remote": 1.035,
    "default": 1.075,
}


def growth_for_csd_row(csdtype, name):
    if name in CSD_GROWTH_FACTORS:
        return CSD_GROWTH_FACTORS[name]
    csdtype = str(csdtype)
    name_lower = str(name).lower()
    if csdtype == "IRI":
        return DEFAULT_GROWTH["first_nation"]
    if csdtype == "CY":
        return DEFAULT_GROWTH["urban_high"]
    if csdtype == "MD":
        return DEFAULT_GROWTH["rural_md"]
    if csdtype in ("T", "VL", "SV"):
        return DEFAULT_GROWTH["rural_town"]
    if csdtype in ("ID", "SM"):
        if "Wood Buffalo" in name:
            return 0.99
        return DEFAULT_GROWTH["remote"]
    return DEFAULT_GROWTH["default"]


def build_da_overlay():
    """
    Return overlay GeoDataFrame with columns:
    DAUID, population_2021, growth, EDNumber20, EDName2017, area_share,
    pop_2021_share, pop_planb_share.
    """
    das = gpd.read_file(os.path.join(DATA, "alberta_2021_das.gpkg"))
    pops = pd.read_csv(os.path.join(DATA, "alberta_2021_da_populations.csv"))
    das["DAUID"] = das["DAUID"].astype(str)
    pops["DAUID"] = pops["DAUID"].astype(str)
    das = das.merge(pops[["DAUID", "population_2021"]], on="DAUID", how="left")
    das["population_2021"] = das["population_2021"].fillna(0).astype(int)

    # Join DAs to CSDs by centroid containment to get growth factor.
    csds = gpd.read_file(os.path.join(DATA, "alberta_2021_csds.gpkg"))
    csd_pops = pd.read_csv(os.path.join(DATA, "alberta_2021_csd_populations.csv"))
    csd_pops["CSDUID"] = csd_pops["ALT_GEO_CODE"].astype(str)
    csds["CSDUID"] = csds["CSDUID"].astype(str)
    csds = csds.merge(csd_pops[["CSDUID", "GEO_NAME"]], on="CSDUID", how="left")
    csds["growth"] = [
        growth_for_csd_row(t, n) for t, n in zip(csds["CSDTYPE"], csds["GEO_NAME"])
    ]

    # Alberta DAUID is 8 digits (PR+CD+DA) and does not embed CSDUID. Join DAs
    # to CSDs by centroid containment to pick up per-CSD growth factors.
    das_for_join = das.to_crs(csds.crs).copy()
    das_for_join["centroid"] = das_for_join.geometry.centroid
    centroids = gpd.GeoDataFrame(
        das_for_join[["DAUID"]].copy(),
        geometry=das_for_join["centroid"],
        crs=csds.crs,
    )
    joined = gpd.sjoin(
        centroids,
        csds[["CSDUID", "GEO_NAME", "CSDTYPE", "growth", "geometry"]],
        how="left",
        predicate="within",
    )
    # If a centroid fell on a boundary and didn't match, fall back to nearest.
    missing = joined[joined["CSDUID"].isna()]
    if len(missing):
        nearest = gpd.sjoin_nearest(
            centroids.loc[missing.index],
            csds[["CSDUID", "GEO_NAME", "CSDTYPE", "growth", "geometry"]],
            how="left",
        )
        for idx in nearest.index:
            joined.loc[idx, ["CSDUID", "GEO_NAME", "CSDTYPE", "growth"]] = nearest.loc[
                idx, ["CSDUID", "GEO_NAME", "CSDTYPE", "growth"]
            ]
    # Drop any duplicated rows from sjoin (a centroid in two CSDs).
    joined = joined.loc[~joined.index.duplicated(keep="first")]
    das = das.merge(
        joined[["DAUID", "CSDUID", "GEO_NAME", "CSDTYPE", "growth"]],
        on="DAUID",
        how="left",
    )
    das["growth"] = das["growth"].fillna(DEFAULT_GROWTH["default"])

    eds_2019 = gpd.read_file(
        os.path.join(DATA, "alberta_2019_eds", "EDS_ENACTED_BILL33_15DEC2017.shp")
    )
    das_p = das.to_crs(eds_2019.crs)
    das_p["da_area_m2"] = das_p.geometry.area

    overlay = gpd.overlay(
        das_p[
            [
                "DAUID",
                "population_2021",
                "growth",
                "da_area_m2",
                "geometry",
            ]
        ],
        eds_2019[["EDNumber20", "EDName2017", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )
    overlay["intersect_area_m2"] = overlay.geometry.area
    overlay["area_share"] = overlay["intersect_area_m2"] / overlay["da_area_m2"]
    # Drop tiny slivers less than 1% of DA area and less than 10,000 m^2.
    overlay = overlay[
        (overlay["area_share"] >= 0.01) | (overlay["intersect_area_m2"] >= 10_000)
    ]
    overlay["pop_2021_share"] = overlay["population_2021"] * overlay["area_share"]
    overlay["pop_planb_share"] = overlay["pop_2021_share"] * overlay["growth"]
    return overlay, eds_2019


def legal_window(dev_pct, is_s152):
    if is_s152:
        if -50 <= dev_pct <= 25:
            return "s15(2)"
        return "fail"
    if -25 <= dev_pct <= 25:
        return "pass"
    return "fail"


def run_2019_map():
    overlay, eds_2019 = build_da_overlay()
    ed_name_map = dict(zip(eds_2019["EDNumber20"], eds_2019["EDName2017"]))
    grp = (
        overlay.groupby("EDNumber20")
        .agg(
            pop_2021_census=("pop_2021_share", "sum"),
            pop_plan_b=("pop_planb_share", "sum"),
        )
        .reset_index()
    )
    grp["ed_name"] = grp["EDNumber20"].map(ed_name_map)
    grp["pop_2021_census"] = grp["pop_2021_census"].round().astype(int)
    grp["pop_plan_b"] = grp["pop_plan_b"].round().astype(int)

    # Flag EDs whose aggregation has significant split-DA contribution
    # (APPROXIMATE when some DAs are split across ED boundaries).
    da_ed_counts = overlay.groupby("DAUID")["EDNumber20"].nunique()
    split_das = set(da_ed_counts[da_ed_counts > 1].index)
    ed_approx = (
        overlay[overlay["DAUID"].isin(split_das)]
        .groupby("EDNumber20")["pop_2021_share"]
        .sum()
    )
    ed_approx_pct = (ed_approx / grp.set_index("EDNumber20")["pop_2021_census"]) * 100
    grp["approx_pct"] = grp["EDNumber20"].map(ed_approx_pct).fillna(0)

    s152_2019 = {"Central Peace-Notley", "Lesser Slave Lake", "Cardston-Siksika"}
    grp["is_s152"] = grp["ed_name"].isin(s152_2019)

    mean_a = grp["pop_2021_census"].mean()
    mean_b = grp["pop_plan_b"].mean()
    grp["dev_from_mean_plan_a_pct"] = (grp["pop_2021_census"] - mean_a) / mean_a * 100
    grp["dev_from_mean_plan_b_pct"] = (grp["pop_plan_b"] - mean_b) / mean_b * 100
    grp["drift_pct"] = (
        (grp["pop_plan_b"] - grp["pop_2021_census"]) / grp["pop_2021_census"] * 100
    )

    grp["legal_window_plan_a"] = grp.apply(
        lambda r: legal_window(r["dev_from_mean_plan_a_pct"], r["is_s152"]), axis=1
    )
    grp["legal_window_plan_b"] = grp.apply(
        lambda r: legal_window(r["dev_from_mean_plan_b_pct"], r["is_s152"]), axis=1
    )
    grp["status_change_flag"] = grp["legal_window_plan_a"] != grp["legal_window_plan_b"]
    grp["aggregation_method"] = grp["approx_pct"].apply(
        lambda p: (
            f"DA-level area-weighted overlay; per-CSD Plan B growth factors; "
            f"{p:.1f}% of Plan A from split DAs (APPROXIMATE if >5%)"
        )
    )

    out = (
        grp[
            [
                "ed_name",
                "pop_2021_census",
                "pop_plan_b",
                "drift_pct",
                "dev_from_mean_plan_a_pct",
                "dev_from_mean_plan_b_pct",
                "legal_window_plan_a",
                "legal_window_plan_b",
                "status_change_flag",
                "aggregation_method",
            ]
        ]
        .sort_values("ed_name")
        .reset_index(drop=True)
    )
    out.to_csv(os.path.join(DATA, "province_wide_drift_2019.csv"), index=False)
    return out, mean_a, mean_b


def run_2026_map(
    crosswalk_csv, commission_pop_csv, out_csv, s152_names, hybrid_col=None
):
    cross = pd.read_csv(crosswalk_csv)
    drift_2019_path = os.path.join(DATA, "province_wide_drift_2019.csv")
    drift_2019 = pd.read_csv(drift_2019_path)
    growth_by_2019 = dict(
        zip(
            drift_2019["ed_name"],
            drift_2019["pop_plan_b"] / drift_2019["pop_2021_census"],
        )
    )
    pops = pd.read_csv(commission_pop_csv)
    if "proposed_2026" in cross.columns and "current_2019" in cross.columns:
        feeders = cross.groupby("proposed_2026")["current_2019"].apply(list).to_dict()
    else:
        feeders = {}

    rows = []
    for _, pr in pops.iterrows():
        name = pr["ed_name"]
        plan_a = int(pr["population"])
        is_s152 = name in s152_names
        feeders_list = feeders.get(name, [])
        feeders_list = [
            f for f in feeders_list if f not in ("(NEW)", "(MERGED/ABSORBED)")
        ]
        growth_vals = [
            growth_by_2019.get(f) for f in feeders_list if growth_by_2019.get(f)
        ]
        if growth_vals:
            growth = sum(growth_vals) / len(growth_vals)
        else:
            growth = PROVINCIAL_CUMULATIVE_GROWTH
        plan_b = int(round(plan_a * growth))

        hybrid = False
        if hybrid_col and hybrid_col in pr.index:
            v = pr[hybrid_col]
            hybrid = (
                bool(v)
                if isinstance(v, bool)
                else (str(v).strip().lower() in ("true", "yes", "hybrid", "1"))
            )
        if "-hybrid" in str(pr.get("region_type", "")).lower():
            hybrid = True
        if not feeders_list:
            hybrid = True

        rows.append(
            {
                "ed_name": name,
                "pop_2021_census": plan_a,
                "pop_plan_b": plan_b,
                "growth_factor_applied": round(growth, 4),
                "is_s152": is_s152,
                "hybrid": hybrid,
            }
        )

    df = pd.DataFrame(rows)
    mean_a = df["pop_2021_census"].mean()
    mean_b = df["pop_plan_b"].mean()
    df["drift_pct"] = (
        (df["pop_plan_b"] - df["pop_2021_census"]) / df["pop_2021_census"] * 100
    )
    df["dev_from_mean_plan_a_pct"] = (df["pop_2021_census"] - mean_a) / mean_a * 100
    df["dev_from_mean_plan_b_pct"] = (df["pop_plan_b"] - mean_b) / mean_b * 100
    df["legal_window_plan_a"] = df.apply(
        lambda r: legal_window(r["dev_from_mean_plan_a_pct"], r["is_s152"]), axis=1
    )
    df["legal_window_plan_b"] = df.apply(
        lambda r: legal_window(r["dev_from_mean_plan_b_pct"], r["is_s152"]), axis=1
    )
    df["status_change_flag"] = df["legal_window_plan_a"] != df["legal_window_plan_b"]
    df["aggregation_method"] = df["hybrid"].apply(
        lambda h: (
            "commission Plan A + feeder-weighted 2019-ED growth (APPROXIMATE; hybrid ED)"
            if h
            else "commission Plan A + direct 2019-ED growth factor"
        )
    )
    out = (
        df[
            [
                "ed_name",
                "pop_2021_census",
                "pop_plan_b",
                "drift_pct",
                "dev_from_mean_plan_a_pct",
                "dev_from_mean_plan_b_pct",
                "legal_window_plan_a",
                "legal_window_plan_b",
                "status_change_flag",
                "aggregation_method",
            ]
        ]
        .sort_values("ed_name")
        .reset_index(drop=True)
    )
    out.to_csv(out_csv, index=False)
    return out, mean_a, mean_b


def summarize(name, out, mean_a, mean_b):
    n_change = int(out["status_change_flag"].sum())
    n_fail_a = (out["legal_window_plan_a"] == "fail").sum()
    n_fail_b = (out["legal_window_plan_b"] == "fail").sum()
    print(f"\n--- {name} ---")
    print(f"N EDs: {len(out)}")
    print(f"Plan A total: {out['pop_2021_census'].sum():,}")
    print(f"Plan B total: {out['pop_plan_b'].sum():,}")
    print(f"Plan A mean: {mean_a:,.0f}")
    print(f"Plan B mean: {mean_b:,.0f}")
    print(
        f"Plan A: pass={(out['legal_window_plan_a']=='pass').sum()}, "
        f"s15(2)={(out['legal_window_plan_a']=='s15(2)').sum()}, "
        f"fail={n_fail_a}"
    )
    print(
        f"Plan B: pass={(out['legal_window_plan_b']=='pass').sum()}, "
        f"s15(2)={(out['legal_window_plan_b']=='s15(2)').sum()}, "
        f"fail={n_fail_b}"
    )
    print(f"Status-change EDs: {n_change}")
    changes = out[out["status_change_flag"]]
    if len(changes):
        print(
            changes[
                [
                    "ed_name",
                    "dev_from_mean_plan_a_pct",
                    "dev_from_mean_plan_b_pct",
                    "legal_window_plan_a",
                    "legal_window_plan_b",
                ]
            ].to_string(index=False)
        )


def main():
    out_2019, mean_a_2019, mean_b_2019 = run_2019_map()
    summarize("2019 (87 EDs)", out_2019, mean_a_2019, mean_b_2019)

    maj_s152 = {"Central Peace-Notley", "Lesser Slave Lake", "Canmore-Banff"}
    out_maj, mean_a_m, mean_b_m = run_2026_map(
        crosswalk_csv=os.path.join(DATA, "majority_hybrid_crosswalk.csv"),
        commission_pop_csv=os.path.join(DATA, "majority_2026_populations.csv"),
        out_csv=os.path.join(DATA, "province_wide_drift_majority.csv"),
        s152_names=maj_s152,
        hybrid_col="is_hybrid",
    )
    summarize("majority 2026 (89 EDs)", out_maj, mean_a_m, mean_b_m)

    min_s152 = {
        "Central Peace-Notley",
        "Lesser Slave Lake",
        "Rocky Mountain House-Banff Park",
    }
    out_min, mean_a_n, mean_b_n = run_2026_map(
        crosswalk_csv=os.path.join(DATA, "minority_hybrid_crosswalk.csv"),
        commission_pop_csv=os.path.join(DATA, "minority_2026_populations.csv"),
        out_csv=os.path.join(DATA, "province_wide_drift_minority.csv"),
        s152_names=min_s152,
        hybrid_col=None,
    )
    summarize("minority 2026 (89 EDs)", out_min, mean_a_n, mean_b_n)


if __name__ == "__main__":
    main()
