"""
Track H — CSD-level community-splits count, per map.

Computes, per populated CSD:
- Number of 2019 EDs the CSD spans (spatial intersection).
- Approximate number of majority-2026 EDs (via hybrid crosswalk).
- Approximate number of minority-2026 EDs (via hybrid crosswalk).

Outputs:
- data/v0_1_csd_splits_summary.csv
- Console summary consumed by the markdown writer.

Dependencies (backward): alberta_2021_csds.gpkg, alberta_2021_csd_populations.csv,
alberta_2019_eds/*.shp, v0_1_majority_hybrid_crosswalk.csv,
v0_1_minority_hybrid_crosswalk.csv
Dependencies (forward): analysis/methodology/v0_1_csd_community_splits.md
"""
# Version: 0.1 series  (last updated 2026-04-26)


import os
import sys
from pathlib import Path

import pandas as pd
import geopandas as gpd

os.environ["PYTHONIOENCODING"] = "utf-8"

ROOT = str(Path(__file__).resolve().parent.parent.parent)
DATA = os.path.join(ROOT, "data")

POP_THRESHOLD = 1000
# A CSD is counted as present in an ED only if the intersection is at least
# this fraction of the CSD's own area, OR at least 1 km^2 in absolute terms.
# This filters the overlay slivers caused by minor geometry mismatches between
# the StatsCan CSD layer and the Elections Alberta ED layer.
INTERSECT_PCT_THRESHOLD = 0.02      # 2% of CSD area
INTERSECT_ABS_THRESHOLD_M2 = 1_000_000  # 1 km^2


def main():
    # Load CSDs with geometry
    csds = gpd.read_file(os.path.join(DATA, "alberta_2021_csds.gpkg"))
    pops = pd.read_csv(os.path.join(DATA, "alberta_2021_csd_populations.csv"))
    pops["CSDUID"] = pops["ALT_GEO_CODE"].astype(str)
    csds["CSDUID"] = csds["CSDUID"].astype(str)

    csds = csds.merge(
        pops[["CSDUID", "population_2021", "GEO_NAME"]],
        on="CSDUID",
        how="left",
    )
    csds["name"] = csds["GEO_NAME"].fillna(csds["CSDNAME"])

    # Load 2019 EDs, project CSDs to ED CRS
    eds_2019 = gpd.read_file(
        os.path.join(DATA, "alberta_2019_eds", "EDS_ENACTED_BILL33_15DEC2017.shp")
    )
    csds_p = csds.to_crs(eds_2019.crs)

    # Spatial join overlay to count how many EDs each CSD intersects
    # Use overlay intersection and filter slivers by area.
    csds_p["csd_area_m2"] = csds_p.geometry.area
    overlay = gpd.overlay(
        csds_p[["CSDUID", "name", "population_2021", "CSDTYPE",
                "csd_area_m2", "geometry"]],
        eds_2019[["EDNumber20", "EDName2017", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )
    overlay["intersect_area_m2"] = overlay.geometry.area
    overlay["pct_of_csd"] = overlay["intersect_area_m2"] / overlay["csd_area_m2"]
    overlay = overlay[
        (overlay["pct_of_csd"] >= INTERSECT_PCT_THRESHOLD)
        | (overlay["intersect_area_m2"] >= INTERSECT_ABS_THRESHOLD_M2)
    ]

    # For each CSD, collect the set of 2019 EDs it spans
    ed_sets_2019 = (
        overlay.groupby("CSDUID")["EDName2017"]
        .apply(lambda s: sorted(set(s)))
        .to_dict()
    )

    # Load crosswalks
    maj = pd.read_csv(os.path.join(DATA, "v0_1_majority_hybrid_crosswalk.csv"))
    mnr = pd.read_csv(os.path.join(DATA, "v0_1_minority_hybrid_crosswalk.csv"))

    # Build 2019->set-of-2026 maps. If a 2019 ED appears twice (hybrid splitting
    # into multiple 2026 EDs), include both 2026 EDs.
    def build_map(df, src_col, dst_col):
        m = {}
        for _, row in df.iterrows():
            src = str(row[src_col]).strip()
            dst = str(row[dst_col]).strip()
            if dst.upper().startswith("(MERGED") or dst.upper() == "NAN":
                # 2019 ED was absorbed into adjacent 2026 EDs without a
                # single successor named; treat as unmapped (skip).
                continue
            m.setdefault(src, set()).add(dst)
        return m

    maj_map = build_map(maj, "current_2019", "proposed_2026")
    mnr_map = build_map(mnr, "current_2019", "proposed_2026")

    # Track 2019 EDs that appear in the minority crosswalk but have no clean
    # successor. These contribute uncertainty to any CSD that intersects them.
    mnr_unmapped = set()
    for _, row in mnr.iterrows():
        dst = str(row["proposed_2026"]).strip()
        if dst.upper().startswith("(MERGED") or dst.upper() == "NAN":
            mnr_unmapped.add(str(row["current_2019"]).strip())

    # IMPORTANT NOTE on majority crosswalk: only 19 rows. This captures
    # hybrid / renaming changes; 2019 EDs not listed are assumed to carry
    # forward into a single 2026 ED that shares (or closely shares) the name.
    # For the splits estimation, any 2019 ED NOT in the crosswalk is assumed
    # to map to exactly one 2026 ED (unsplit at the 2019-ED level).

    def count_2026_eds(ed2019_set, cross_map, unmapped_set=None):
        """Return (count, sorted_list, uncertain_flag).

        A 2019 ED that appears in the crosswalk but has no clean successor
        (MERGED/ABSORBED in minority crosswalk) contributes uncertainty: we
        do not know whether the CSD sitting in it ends up in one or several
        2026 EDs. We do not add a phantom district in the count; we flag the
        CSD as uncertain.
        """
        proposed = set()
        uncertain = False
        for e in ed2019_set:
            if unmapped_set is not None and e in unmapped_set:
                uncertain = True
                continue
            if e in cross_map:
                proposed.update(cross_map[e])
            else:
                # not in crosswalk -> inherit a single unchanged proposed ED
                proposed.add(e)
        return len(proposed), sorted(proposed), uncertain

    # Build per-CSD summary
    rows = []
    for _, r in csds_p.iterrows():
        pop = r.get("population_2021")
        if pd.isna(pop):
            pop = 0
        pop = int(pop)
        if pop < POP_THRESHOLD:
            continue

        ed2019 = ed_sets_2019.get(r["CSDUID"], [])
        n_2019 = len(ed2019)
        if n_2019 == 0:
            # No spatial intersection (shouldn't happen for populated AB CSDs)
            continue

        n_maj, maj_eds, _ = count_2026_eds(ed2019, maj_map)
        n_mnr, mnr_eds, mnr_uncertain = count_2026_eds(
            ed2019, mnr_map, unmapped_set=mnr_unmapped
        )
        # Upper-bound for minority: assume each unmapped 2019 ED contributes
        # one distinct 2026 ED (conservative against over-claiming minority
        # unity). Adds 1 per unmapped parent 2019 ED hit by this CSD.
        unmapped_hits = sum(1 for e in ed2019 if e in mnr_unmapped)
        n_mnr_upper = n_mnr + unmapped_hits

        # Hybrid-boundary uncertainty: if any of the CSD's 2019 EDs split
        # into multiple 2026 EDs in the crosswalk, the CSD may be split
        # at a point not captured by the ED-level join.
        maj_hybrid_hit = any(
            e in maj_map and len(maj_map[e]) >= 2 for e in ed2019
        )
        mnr_hybrid_hit = any(
            e in mnr_map and len(mnr_map[e]) >= 2 for e in ed2019
        )

        rows.append(
            {
                "csduid": r["CSDUID"],
                "csd_name": r["name"],
                "csd_type": r.get("CSDTYPE", ""),
                "population_2021": pop,
                "splits_2019": n_2019,
                "splits_majority_2026_est": n_maj,
                "splits_minority_2026_est": n_mnr,
                "splits_minority_2026_upper": n_mnr_upper,
                "majority_uncertain": maj_hybrid_hit,
                "minority_uncertain": (mnr_uncertain or mnr_hybrid_hit),
                "eds_2019": "; ".join(ed2019),
                "eds_majority_2026_est": "; ".join(maj_eds),
                "eds_minority_2026_est": "; ".join(mnr_eds),
            }
        )

    out = pd.DataFrame(rows).sort_values(
        ["splits_2019", "population_2021"], ascending=[False, False]
    )
    out_path = os.path.join(DATA, "v0_1_csd_splits_summary.csv")
    out.to_csv(out_path, index=False, encoding="utf-8")

    # Console summary
    total_csds = len(out)
    split_2019 = int((out["splits_2019"] >= 2).sum())
    split_maj = int((out["splits_majority_2026_est"] >= 2).sum())
    split_mnr = int((out["splits_minority_2026_est"] >= 2).sum())

    print(f"Populated CSDs analysed (pop >= {POP_THRESHOLD}): {total_csds}")
    print(
        f"Split under 2019: {split_2019} "
        f"({split_2019/total_csds*100:.1f}%)  "
        f"mean {out['splits_2019'].mean():.2f}  median {out['splits_2019'].median():.1f}"
    )
    print(
        f"Split under majority 2026 (est): {split_maj} "
        f"({split_maj/total_csds*100:.1f}%)  "
        f"mean {out['splits_majority_2026_est'].mean():.2f}  "
        f"median {out['splits_majority_2026_est'].median():.1f}"
    )
    print(
        f"Split under minority 2026 (est lower): {split_mnr} "
        f"({split_mnr/total_csds*100:.1f}%)  "
        f"mean {out['splits_minority_2026_est'].mean():.2f}  "
        f"median {out['splits_minority_2026_est'].median():.1f}"
    )
    split_mnr_u = int((out["splits_minority_2026_upper"] >= 2).sum())
    print(
        f"Split under minority 2026 (upper): {split_mnr_u} "
        f"({split_mnr_u/total_csds*100:.1f}%)  "
        f"mean {out['splits_minority_2026_upper'].mean():.2f}  "
        f"median {out['splits_minority_2026_upper'].median():.1f}"
    )

    # Confident-only subset (minority hybrids and MERGED entries excluded)
    confident = out[~out["minority_uncertain"]]
    c_split_mnr = int((confident["splits_minority_2026_est"] >= 2).sum())
    c_split_2019 = int((confident["splits_2019"] >= 2).sum())
    c_split_maj = int((confident["splits_majority_2026_est"] >= 2).sum())
    print(
        f"\nConfident-only subset (n={len(confident)}): "
        f"2019={c_split_2019}  majority={c_split_maj}  minority={c_split_mnr}"
    )

    print("\nTop-10 most-split CSDs under 2019:")
    print(
        out.nlargest(10, "splits_2019")[
            ["csd_name", "population_2021", "splits_2019"]
        ].to_string(index=False)
    )

    print("\nTop-10 most-split CSDs under majority 2026 (est):")
    print(
        out.nlargest(10, "splits_majority_2026_est")[
            ["csd_name", "population_2021", "splits_majority_2026_est"]
        ].to_string(index=False)
    )

    print("\nTop-10 most-split CSDs under minority 2026 (est):")
    print(
        out.nlargest(10, "splits_minority_2026_est")[
            ["csd_name", "population_2021", "splits_minority_2026_est"]
        ].to_string(index=False)
    )

    # Focused CSDs
    focus_names = [
        "Airdrie",
        "Calgary",
        "Red Deer",
        "Cochrane",
        "Chestermere",
        "St. Albert",
        "Banff",
        "Improvement District No. 9",
        "Rocky Mountain House",
    ]
    print("\nContested / focus configurations:")
    for needle in focus_names:
        mask = out["csd_name"].str.contains(needle, case=False, regex=False)
        sub = out[mask]
        for _, r in sub.iterrows():
            print(
                f"  {r['csd_name']:<55} pop={r['population_2021']:>8}  "
                f"2019={r['splits_2019']}  maj={r['splits_majority_2026_est']}  "
                f"min={r['splits_minority_2026_est']}"
            )

    return out


if __name__ == "__main__":
    main()
