"""
v0_1_approximate_shape_analysis.py

Track X: Construct approximate 2026 ED shapefiles from the published 2019
shapefile + commission crosswalks, then run Polsby-Popper and Reock
compactness.

Dependencies
  Forward  : data/alberta_2019_eds/*.shp (authoritative 2019 87-ED polygons)
             data/v0_1_majority_2026_populations.csv (89 majority 2026 ED list)
             data/v0_1_minority_hybrid_crosswalk.csv (minority crosswalk)
             data/v0_1_minority_hybrid_crosswalk_appendixE.csv (Calgary/minority)
             data/v0_1_majority_hybrid_crosswalk.csv (partial majority renames)
  Backward : analysis/v0_1_approximate_shape_analysis.md (method + results)
             data/v0_1_approximate_majority_2026_eds.gpkg (if Tier C attempted)
             data/v0_1_approximate_minority_2026_eds.gpkg (if Tier C attempted)
             data/v0_1_compactness_scores.csv (per-ED compactness for all maps)

Approach
  Tier A (exact rename) : 2026 ED == single 2019 ED with same or renamed boundary.
                          Use 2019 polygon directly.
  Tier B (merge)        : 2026 ED == union of 2+ full 2019 EDs. Union the polygons.
  Tier C (hybrid)       : 2026 ED splits one or more 2019 EDs across multiple
                          2026 EDs. NOT ATTEMPTED IN THIS SESSION -- visual
                          transcription from the commission JPGs cannot be
                          done reliably in the budget without fabricating
                          coordinates. Flagged as not_computed; audit per
                          Section 4 provenance document and uncertainty rules.

Math
  Polsby-Popper = 4 * pi * A / P^2     in [0, 1], higher = more compact
  Reock         = A / (pi * r_mbc^2)    in [0, 1], r_mbc = min bounding circle radius

Coordinate system
  Input CRS is EPSG:3401 (NAD83 / Alberta 10-TM Forest) -- projected, metres.
  Areas and perimeters are computed directly in this CRS, no reprojection
  needed. All compactness metrics are scale-invariant but we still use the
  projected CRS to avoid lat/lon distortion in area/perimeter.

Author: sub-agent, Track X, 2026-04-22
"""
from __future__ import annotations

import csv
import math
import os
import sys
from dataclasses import dataclass

import geopandas as gpd
import pandas as pd
from shapely import minimum_bounding_radius
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

# ---------------------------------------------------------------------------
# Paths

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = r"C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit"
SHP_2019 = os.path.join(ROOT, "data", "alberta_2019_eds", "EDS_ENACTED_BILL33_15DEC2017.shp")
MAJ_POP_CSV = os.path.join(ROOT, "data", "v0_1_majority_2026_populations.csv")
MIN_CROSSWALK_CSV = os.path.join(ROOT, "data", "v0_1_minority_hybrid_crosswalk.csv")
MIN_APPENDIX_E = os.path.join(ROOT, "data", "v0_1_minority_hybrid_crosswalk_appendixE.csv")
MAJ_CROSSWALK_CSV = os.path.join(ROOT, "data", "v0_1_majority_hybrid_crosswalk.csv")

OUT_MAJ_GPKG = os.path.join(ROOT, "data", "v0_1_approximate_majority_2026_eds.gpkg")
OUT_MIN_GPKG = os.path.join(ROOT, "data", "v0_1_approximate_minority_2026_eds.gpkg")
OUT_CSV = os.path.join(ROOT, "data", "v0_1_compactness_scores.csv")


# ---------------------------------------------------------------------------
# Compactness metrics

def polsby_popper(geom) -> float:
    """4*pi*A / P^2."""
    if geom is None or geom.is_empty:
        return float("nan")
    area = geom.area
    perim = geom.length
    if perim == 0:
        return float("nan")
    return (4.0 * math.pi * area) / (perim * perim)


def reock(geom) -> float:
    """A / (pi * r_mbc^2)."""
    if geom is None or geom.is_empty:
        return float("nan")
    r = minimum_bounding_radius(geom)
    if r == 0:
        return float("nan")
    circle_area = math.pi * (r * r)
    return geom.area / circle_area


# ---------------------------------------------------------------------------
# 2019 ED polygon lookup

def load_2019_eds() -> dict[str, any]:
    """Return dict keyed by 2019 ED name -> shapely geometry."""
    gdf = gpd.read_file(SHP_2019)
    # sanity
    assert len(gdf) == 87, f"Expected 87 2019 EDs, got {len(gdf)}"
    assert gdf.crs.to_epsg() == 3401, f"Expected EPSG:3401, got {gdf.crs}"
    return dict(zip(gdf["EDName2017"], gdf.geometry))


# ---------------------------------------------------------------------------
# Crosswalk construction
#
# We build crosswalks as a dict:
#     proposed_2026_name -> (tier, [list_of_2019_names], confidence, note)
#
# tier in {"A", "B", "C"}; C entries have [] for 2019 list when truly new EDs.

# Naming-pattern map from 2019 -> canonical (used for fuzzy matching)

@dataclass
class CrosswalkEntry:
    name_2026: str
    tier: str
    parents_2019: list[str]
    confidence: str
    note: str


# ---- MAJORITY 2026 (89 EDs) ----
#
# Based on data/v0_1_majority_2026_populations.csv (which lists all 89 EDs)
# cross-referenced with the partial rename crosswalk at
# data/v0_1_majority_hybrid_crosswalk.csv.
#
# Tier A (direct or rename, single 2019 parent):
#   rename pairs where the 2026 name differs only in ordering or minor edit.
# Tier B (merge -- union of 2+ full 2019 EDs):
#   Athabasca-Barrhead-Westlock is the province's Athabasca-Barrhead absorbing
#   Westlock-ward area, but in the 2019 map there is no "Westlock" ED and this
#   is a clean renaming of the 2019 "Athabasca-Barrhead" so treated as A.
# Tier C (hybrid, split): the commission's is_hybrid flag in the 2026 population
#   CSV marks these; we cannot reconstruct split boundaries from the JPGs in
#   this session's budget.

# Build majority crosswalk from the population CSV (which has is_hybrid).
# Rule set (documented):
#
#   1. If the 2026 ED name exactly equals a 2019 ED name AND is_hybrid is False,
#      -> Tier A (identity).
#   2. If the majority crosswalk file has a rename mapping AND is_hybrid is
#      False, -> Tier A (rename).
#   3. If is_hybrid is False but neither an identity match nor explicit rename
#      is found -> attempt fuzzy match by name tokens; otherwise Tier C with
#      parents=[] (truly new ED).
#   4. If is_hybrid is True -> Tier C. Parents identified by token overlap
#      where possible; not used for geometry (Tier C not computed).

MAJORITY_HYBRID_PARENTS: dict[str, list[str]] = {
    # Names from the majority 2026 population CSV that are hybrid, mapped to
    # approximate 2019 parents by name stem / contextual reading of the
    # commission's chapter on rural boundary changes. These are used for
    # reporting only; geometry is NOT reconstructed.
    "Calgary-East": ["Calgary-East"],
    "Calgary-Falconridge-Conrich": ["Calgary-Falconridge", "Chestermere-Strathmore"],
    "Calgary-Glenmore-Tsuut'ina": ["Calgary-Glenmore", "Calgary-West"],
    "Calgary-West-Elbow Valley": ["Calgary-West", "Banff-Kananaskis"],
    "Edmonton-Beaumont": ["Edmonton-Ellerslie", "Leduc-Beaumont"],
    "Edmonton-Enoch": ["Edmonton-West Henday", "Lac Ste. Anne-Parkland"],
    "Airdrie-East": ["Airdrie-East"],
    "Airdrie-West": ["Airdrie-Cochrane"],
    "Chestermere-Strathmore": ["Chestermere-Strathmore"],
    "Cochrane-Springbank": ["Airdrie-Cochrane", "Banff-Kananaskis"],
    "Cold Lake-Bonnyville-St. Paul": ["Bonnyville-Cold Lake-St. Paul"],
    "Fort McMurray-Lac La Biche": ["Fort McMurray-Lac La Biche"],
    "High River-Vulcan-Siksika": ["Highwood", "Cardston-Siksika", "Livingstone-Macleod"],
    "Leduc-Devon": ["Leduc-Beaumont", "Drayton Valley-Devon"],
    "Lethbridge-East": ["Lethbridge-East"],
    "Lethbridge-West": ["Lethbridge-West"],
    "Medicine Hat-Brooks": ["Brooks-Medicine Hat"],
    "Okotoks-Diamond Valley": ["Highwood", "Livingstone-Macleod"],
    "St. Albert-Sturgeon": ["Morinville-St. Albert"],
}


def build_majority_crosswalk() -> list[CrosswalkEntry]:
    # Load 2019 ED names
    gdf_2019 = gpd.read_file(SHP_2019)
    names_2019 = set(gdf_2019["EDName2017"])

    # Load explicit rename map
    renames: dict[str, str] = {}
    with open(MAJ_CROSSWALK_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            renames[row["proposed_2026"]] = row["current_2019"]

    # Load majority 2026 ED list + is_hybrid
    df = pd.read_csv(MAJ_POP_CSV)
    out: list[CrosswalkEntry] = []
    for _, row in df.iterrows():
        name26 = row["ed_name"]
        is_hybrid = bool(row["is_hybrid"])

        if not is_hybrid:
            # Tier A candidate
            if name26 in names_2019:
                out.append(CrosswalkEntry(name26, "A", [name26], "high", "identity"))
                continue
            if name26 in renames and renames[name26] in names_2019:
                out.append(CrosswalkEntry(name26, "A", [renames[name26]], "high", f"rename from {renames[name26]}"))
                continue
            # Check MAJORITY_HYBRID_PARENTS (which also handles a few
            # non-hybrid renames we know about).
            parents = MAJORITY_HYBRID_PARENTS.get(name26, [])
            parents = [p for p in parents if p in names_2019]
            if len(parents) == 1:
                out.append(CrosswalkEntry(name26, "A", parents, "medium", "documented rename"))
                continue
            if len(parents) >= 2:
                out.append(CrosswalkEntry(name26, "B", parents, "medium", "documented merge (non-hybrid-flagged)"))
                continue
            # Unknown
            out.append(CrosswalkEntry(name26, "C", [], "low", "unidentified parent(s)"))
        else:
            # is_hybrid=True -> Tier C
            parents = MAJORITY_HYBRID_PARENTS.get(name26, [])
            parents = [p for p in parents if p in names_2019]
            out.append(CrosswalkEntry(name26, "C", parents, "low", "hybrid split -- geometry not reconstructed"))

    return out


# ---- MINORITY 2026 (89 EDs) ----
# The minority crosswalk CSV is more comprehensive (89 rows including
# unmapped merges). is_hybrid yes => Tier C; is_hybrid no + exact/jaccard=1
# => Tier A; jaccard<1 => Tier A (rename) if single parent, Tier B if merged
# naming.
MINORITY_NEW_PARENTS: dict[str, list[str]] = {
    # NEW 2026 EDs with approximate parents for reporting (not used for geom).
    "Calgary-Airdrie": ["Calgary-Foothills", "Airdrie-Cochrane"],
    "Calgary-De Winton": ["Calgary-Shaw", "Highwood"],
    "Calgary-Nolan Hill-Cochrane": ["Calgary-Foothills", "Airdrie-Cochrane"],
    "Calgary-South": ["Calgary-Shaw", "Calgary-Hays"],
    "Canmore-Kananaskis": ["Banff-Kananaskis"],
    "Edmonton-Beaumont": ["Edmonton-Ellerslie", "Leduc-Beaumont"],
    "Edmonton-Castledowns": ["Edmonton-Castle Downs"],
    "Edmonton-Enoch-Devon": ["Edmonton-West Henday", "Drayton Valley-Devon"],
    "Edmonton-Windermere": ["Edmonton-Whitemud", "Edmonton-South West"],
    "Highwood": ["Highwood"],
    "Lethbridge-Cardston": ["Cardston-Siksika"],
    "Lethbridge-Fort MacLeod-Crowsnest Pass": ["Lethbridge-West", "Livingstone-Macleod"],
    "Lethbridge-Little Bow": ["Lethbridge-East", "Taber-Warner"],
    "Lloydminster-Wainwright": ["Vermilion-Lloydminster-Wainwright"],
    "Red Deer-Lacombe": ["Lacombe-Ponoka"],
    "Wetaskawin-Ponoka-Maskwacis": ["Maskwacis-Wetaskiwin", "Lacombe-Ponoka"],
    # hybrid-flagged but single/double clear parents
    "Calgary-Bow-Springbank": ["Calgary-Bow", "Banff-Kananaskis"],
    "Calgary-Foothills-Airdrie West": ["Calgary-Foothills", "Airdrie-Cochrane"],
    "Calgary-McCall-Bhullar": ["Calgary-McCall"],
    "Calgary-North West-Bearspaw": ["Calgary-North West", "Airdrie-Cochrane"],
    "Calgary-Peigan-Chestermere": ["Calgary-Peigan", "Chestermere-Strathmore"],
    "Calgary-West-Tsuut\u2019ina": ["Calgary-West"],
    "Calgary-West-Tsuut'ina": ["Calgary-West"],
    "Edmonton-Beverly-Clareview": ["Edmonton-Beverly-Clareview"],
    "Edmonton-Glenora-Riverview": ["Edmonton-Glenora", "Edmonton-Riverview"],
    "Edmonton-Highlands-Norwood": ["Edmonton-Highlands-Norwood"],
    "St. Albert-Sturgeon": ["Morinville-St. Albert"],
    "Lethbridge-Taber-Warner": ["Taber-Warner"],
}


def build_minority_crosswalk() -> list[CrosswalkEntry]:
    gdf_2019 = gpd.read_file(SHP_2019)
    names_2019 = set(gdf_2019["EDName2017"])

    df = pd.read_csv(MIN_CROSSWALK_CSV)
    out: list[CrosswalkEntry] = []
    seen_names: set[str] = set()

    for _, row in df.iterrows():
        name26 = row["proposed_2026"]
        cur19 = row["current_2019"]
        is_hybrid = str(row.get("is_hybrid", "no")).lower() == "yes"
        match_type = str(row.get("match_type", ""))

        if name26 == "(MERGED/ABSORBED)":
            # 2019 ED that was absorbed; skip -- not a 2026 ED.
            continue
        if name26 in seen_names:
            continue
        seen_names.add(name26)

        if cur19 == "(NEW)":
            # Truly new 2026 ED; check parent hints
            parents = MINORITY_NEW_PARENTS.get(name26, [])
            parents = [p for p in parents if p in names_2019]
            if len(parents) == 1 and not is_hybrid:
                out.append(CrosswalkEntry(name26, "A", parents, "medium", "NEW ED, single approx parent"))
            elif len(parents) >= 2 and not is_hybrid:
                out.append(CrosswalkEntry(name26, "B", parents, "medium", "NEW ED, merge of approx parents"))
            else:
                out.append(CrosswalkEntry(name26, "C", parents, "low", "NEW hybrid -- geometry not reconstructed"))
            continue

        # Existing 2019 parent
        if is_hybrid:
            # Tier C. Parents from MINORITY_NEW_PARENTS if available,
            # else default to the listed current_2019.
            parents = MINORITY_NEW_PARENTS.get(name26, [cur19 if cur19 in names_2019 else ""])
            parents = [p for p in parents if p in names_2019]
            out.append(CrosswalkEntry(name26, "C", parents, "low", "hybrid split -- geometry not reconstructed"))
            continue

        # Not hybrid, not new
        if match_type.startswith("exact") or match_type == "jaccard=1.00":
            # Tier A: identity or clean rename of single 2019 parent
            if cur19 in names_2019:
                out.append(CrosswalkEntry(name26, "A", [cur19], "high", match_type))
            else:
                out.append(CrosswalkEntry(name26, "C", [], "low", f"cur19 '{cur19}' not in 2019 shapefile"))
        else:
            # jaccard < 1: rename / partial absorption of single parent.
            # Treat as Tier A (approximation) if we can map to a single 2019 parent,
            # else Tier C.
            parents = MINORITY_NEW_PARENTS.get(name26, [cur19])
            parents = [p for p in parents if p in names_2019]
            if len(parents) == 1:
                out.append(CrosswalkEntry(name26, "A", parents, "medium", f"rename with {match_type}"))
            elif len(parents) >= 2:
                out.append(CrosswalkEntry(name26, "B", parents, "medium", f"merge approx, {match_type}"))
            else:
                out.append(CrosswalkEntry(name26, "C", [], "low", f"{match_type} unmatched"))

    return out


# ---------------------------------------------------------------------------
# Geometry assembly

def geom_for_entry(entry: CrosswalkEntry, eds_2019: dict[str, any]):
    if entry.tier == "A":
        p = entry.parents_2019[0]
        return eds_2019[p] if p in eds_2019 else None
    if entry.tier == "B":
        geoms = [eds_2019[p] for p in entry.parents_2019 if p in eds_2019]
        if not geoms:
            return None
        return unary_union(geoms)
    # Tier C: not computed in this session.
    return None


def assemble_map(entries: list[CrosswalkEntry], eds_2019: dict[str, any]) -> gpd.GeoDataFrame:
    records = []
    for e in entries:
        geom = geom_for_entry(e, eds_2019)
        records.append({
            "name_2026": e.name_2026,
            "tier": e.tier,
            "confidence": e.confidence,
            "parents_2019": ";".join(e.parents_2019),
            "note": e.note,
            "geometry": geom,
        })
    gdf = gpd.GeoDataFrame(records, crs="EPSG:3401")
    return gdf


# ---------------------------------------------------------------------------
# Compactness scoring

def compactness_for_gdf(gdf: gpd.GeoDataFrame, name_col: str, map_label: str) -> pd.DataFrame:
    rows = []
    for _, r in gdf.iterrows():
        g = r.geometry
        if g is None or (isinstance(g, float) and pd.isna(g)) or (hasattr(g, "is_empty") and g.is_empty):
            rows.append({
                "map": map_label,
                "name": r[name_col],
                "tier": r.get("tier", "A"),
                "confidence": r.get("confidence", "high"),
                "area_km2": None,
                "perimeter_km": None,
                "polsby_popper": None,
                "reock": None,
            })
            continue
        pp = polsby_popper(g)
        rk = reock(g)
        area_km2 = g.area / 1e6
        perim_km = g.length / 1e3
        rows.append({
            "map": map_label,
            "name": r[name_col],
            "tier": r.get("tier", "A"),
            "confidence": r.get("confidence", "high"),
            "area_km2": area_km2,
            "perimeter_km": perim_km,
            "polsby_popper": pp,
            "reock": rk,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main

def main():
    print("Loading 2019 ED shapefile...", flush=True)
    eds_2019 = load_2019_eds()
    print(f"  Loaded {len(eds_2019)} 2019 EDs (CRS EPSG:3401)")

    # 2019 baseline compactness
    print("\nComputing 2019 baseline compactness...", flush=True)
    gdf_2019 = gpd.read_file(SHP_2019)
    gdf_2019 = gdf_2019.rename(columns={"EDName2017": "name_2026"})
    gdf_2019["tier"] = "A"
    gdf_2019["confidence"] = "high"
    df_2019 = compactness_for_gdf(gdf_2019, "name_2026", "2019")

    # Build crosswalks
    print("\nBuilding majority crosswalk...", flush=True)
    maj_entries = build_majority_crosswalk()
    maj_tiers = {"A": 0, "B": 0, "C": 0}
    for e in maj_entries:
        maj_tiers[e.tier] += 1
    print(f"  Majority tiers: A={maj_tiers['A']} B={maj_tiers['B']} C={maj_tiers['C']}  (total {len(maj_entries)})")

    print("\nBuilding minority crosswalk...", flush=True)
    min_entries = build_minority_crosswalk()
    min_tiers = {"A": 0, "B": 0, "C": 0}
    for e in min_entries:
        min_tiers[e.tier] += 1
    print(f"  Minority tiers: A={min_tiers['A']} B={min_tiers['B']} C={min_tiers['C']}  (total {len(min_entries)})")

    # Assemble approximate shapefiles (Tier A + B only; Tier C geometry = None).
    print("\nAssembling majority approximate shapefile...", flush=True)
    gdf_maj = assemble_map(maj_entries, eds_2019)
    # Keep only entries with valid geometry for file output
    gdf_maj_save = gdf_maj[gdf_maj.geometry.notna()].copy()
    gdf_maj_save.to_file(OUT_MAJ_GPKG, driver="GPKG", layer="approximate_2026_majority")
    print(f"  Wrote {OUT_MAJ_GPKG} ({len(gdf_maj_save)} features)")

    print("\nAssembling minority approximate shapefile...", flush=True)
    gdf_min = assemble_map(min_entries, eds_2019)
    gdf_min_save = gdf_min[gdf_min.geometry.notna()].copy()
    gdf_min_save.to_file(OUT_MIN_GPKG, driver="GPKG", layer="approximate_2026_minority")
    print(f"  Wrote {OUT_MIN_GPKG} ({len(gdf_min_save)} features)")

    # Compactness
    print("\nComputing majority compactness...", flush=True)
    df_maj = compactness_for_gdf(gdf_maj, "name_2026", "majority_2026_approx")

    print("Computing minority compactness...", flush=True)
    df_min = compactness_for_gdf(gdf_min, "name_2026", "minority_2026_approx")

    # Combine
    df_all = pd.concat([df_2019, df_maj, df_min], ignore_index=True)
    df_all.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV} ({len(df_all)} rows)")

    # Summary stats
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    for label, df in [("2019", df_2019), ("majority 2026 approx (A+B only)", df_maj),
                      ("minority 2026 approx (A+B only)", df_min)]:
        d = df.dropna(subset=["polsby_popper"])
        if len(d) == 0:
            print(f"\n{label}: no polygons computed")
            continue
        pp = d["polsby_popper"]
        rk = d["reock"]
        print(f"\n{label} ({len(d)} polygons, {df['polsby_popper'].isna().sum()} Tier-C/not-computed)")
        print(f"  Polsby-Popper  mean={pp.mean():.3f}  median={pp.median():.3f}  "
              f"<0.25: {(pp < 0.25).sum()}/{len(pp)}")
        print(f"  Reock          mean={rk.mean():.3f}  median={rk.median():.3f}  "
              f"<0.30: {(rk < 0.30).sum()}/{len(rk)}")

    # Flagged minority configurations
    print("\n" + "=" * 72)
    print("FLAGGED MINORITY CONFIGURATIONS vs MAJORITY EQUIVALENT")
    print("=" * 72)
    # Flagged minority configurations to compare vs majority equivalent.
    # Majority name is the closest majority 2026 ED that covers the same
    # geography; if the majority kept the 2019 shape, we use the 2019 ED
    # so we still get a baseline number.
    flagged = [
        ("RMH-Banff Park (minority)",       "Rocky Mountain House-Banff Park",
                                            "Banff-Kananaskis",    "maj uses Banff-Kananaskis; 2019"),
        ("Calgary-Nolan Hill-Cochrane",      "Calgary-Nolan Hill-Cochrane",
                                             "Cochrane-Springbank", "maj uses Cochrane-Springbank"),
        ("Airdrie E (min Tier A / maj C)",   "Airdrie East",
                                             "Airdrie-East",        "maj hybrid, min identity"),
        ("Lethbridge-Little Bow (min)",      "Lethbridge-Little Bow",
                                             "Lethbridge-East",     "maj Lethbridge-East (hybrid)"),
        ("Red Deer-Blackfalds (min)",        "Red Deer-Blackfalds",
                                             "Red Deer-North",      "maj kept Red Deer-North single"),
        ("Chestermere split (min)",          "Calgary-Peigan-Chestermere",
                                             "Calgary-Falconridge-Conrich", "maj absorbs Chestermere"),
        ("Calgary-Peigan-Chestermere (min)", "Calgary-Peigan-Chestermere",
                                             "Calgary-Peigan",      "maj kept Calgary-Peigan (A)"),
        ("Olds-Three Hills-Didsbury (min)",  "Olds-Three Hills-Didsbury",
                                             "Olds-Didsbury-Three Hills", "maj identical-name rename"),
    ]
    # Also grab 2019 reference compactness for each comparator
    for label, min_name, maj_name, note in flagged:
        minrow = df_min[df_min["name"] == min_name]
        majrow = df_maj[df_maj["name"] == maj_name] if maj_name else pd.DataFrame()
        ref2019 = df_2019[df_2019["name"] == maj_name] if maj_name else pd.DataFrame()

        def row_fmt(row):
            if not len(row):
                return "not found"
            pp = row["polsby_popper"].iloc[0]
            rk = row["reock"].iloc[0]
            tier = row["tier"].iloc[0]
            if pp is None or (isinstance(pp, float) and math.isnan(pp)):
                return f"tier={tier}  PP=NA  Reock=NA"
            return f"tier={tier}  PP={pp:.3f}  Reock={rk:.3f}"

        print(f"\n  {label} -- {note}")
        print(f"    min({min_name}): {row_fmt(minrow)}")
        print(f"    maj({maj_name}): {row_fmt(majrow)}")
        print(f"    2019({maj_name}): {row_fmt(ref2019)}")

    # Tier C uncertainty band: if we approximate Tier C by the UNION of
    # parent 2019 polygons (treating the 2026 ED as contained within that
    # union), compute PP for the parent union as an upper-bound reference.
    # The true hybrid boundary is a subset of the union, so its Polsby-Popper
    # is usually LOWER than the parent union's (more perimeter per unit
    # area after cutting). We report this as a sensitivity illustration,
    # explicitly NOT as the estimated value for the 2026 ED.
    print("\n" + "=" * 72)
    print("TIER C PARENT-UNION COMPACTNESS (sensitivity reference only, NOT estimate)")
    print("=" * 72)
    tierC_rows = []
    for e in maj_entries + min_entries:
        if e.tier != "C":
            continue
        geoms = [eds_2019[p] for p in e.parents_2019 if p in eds_2019]
        if not geoms:
            continue
        union = unary_union(geoms) if len(geoms) > 1 else geoms[0]
        pp = polsby_popper(union)
        rk = reock(union)
        tierC_rows.append({
            "ed_2026": e.name_2026,
            "parents": ";".join(e.parents_2019),
            "n_parents": len(e.parents_2019),
            "parent_union_PP": pp,
            "parent_union_Reock": rk,
            "pp_minus10pct_perim": (4 * math.pi * union.area) / ((union.length * 0.9) ** 2),
            "pp_plus10pct_perim": (4 * math.pi * union.area) / ((union.length * 1.1) ** 2),
        })
    tc_df = pd.DataFrame(tierC_rows)
    tc_csv = os.path.join(ROOT, "data", "v0_1_tierC_parent_union_reference.csv")
    tc_df.to_csv(tc_csv, index=False)
    print(f"  Wrote {tc_csv} ({len(tc_df)} Tier-C EDs with at least one identified parent)")
    print("\nDone.")


if __name__ == "__main__":
    main()
