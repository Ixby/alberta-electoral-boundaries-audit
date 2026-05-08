"""Build full 2019 -> 2026 crosswalks for majority and minority maps.

The 10k MCMC rescore used a hybrid crosswalk that covered only the
19 explicit majority renames and 103 minority rows. For full 89-district
coverage we need a row for every 2019 ED mapping to its primary 2026
successor under each map.

Sources of truth (priority order):
  1. `parents_2019` column in the 2026 gpkg (when 2026 ED exists there)
  2. Explicit `data/majority_hybrid_crosswalk.csv` / `_minority_hybrid_crosswalk.csv`
  3. 338canada reallocation files (`data/v0_1_338canada_reallocated_*.csv`)
     which map every 2026 ED back to its 2019 source (primary) — reverse
     this for unique 2019->2026 assignment; for 2019 EDs that appear as
     source to multiple 2026 EDs (Calgary gets +2 seats), prefer the one
     keeping the 2019 name exactly, else the most populous successor.
  4. Manual commission-report splits fallback.

Outputs:
  - data/majority_full_crosswalk.csv
  - data/minority_full_crosswalk.csv

Each file has columns: current_2019, proposed_2026, type, source
where type in {hybrid, rename, identity, split_primary, merge, absorb}.

Forward: analysis/scripts/v0_1_mcmc_full_coverage_rescore_100k.py
Backward:
  data/majority_2026_populations.csv
  data/minority_2026_populations.csv
  data/majority_hybrid_crosswalk.csv
  data/minority_hybrid_crosswalk.csv
  data/338canada_reallocated_majority.csv
  data/338canada_reallocated_minority.csv
  data/v0_1_approximate_majority_2026_eds_full.gpkg
  data/v0_1_refined_v6_minority_2026_eds_full.gpkg
  data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from __future__ import annotations
import pandas as pd
import geopandas as gpd
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")


def norm(s: str) -> str:
    """Normalise whitespace + Tsuut'ina apostrophe variants."""
    if s is None:
        return ""
    s = str(s).strip()
    # Replace curly apostrophes with straight
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    # Unicode normalise
    s = unicodedata.normalize("NFC", s)
    return s


def build_majority_crosswalk() -> pd.DataFrame:
    eds_2019 = gpd.read_file(
        DATA
        / "shapefiles"
        / "reference"
        / "alberta_2019_eds"
        / "EDS_ENACTED_BILL33_15DEC2017.shp"
    )
    eds_2019_set = set(norm(n) for n in eds_2019["EDName2017"].unique())

    maj_pops = pd.read_csv(DATA / "majority_2026_populations.csv")
    maj_2026_set = set(norm(n) for n in maj_pops["ed_name"])
    # Population lookup for tiebreak
    maj_pop_by_name = {
        norm(r["ed_name"]): int(r["population"]) for _, r in maj_pops.iterrows()
    }

    gpkg = gpd.read_file(
        DATA / "shapefiles" / "derived" / "v0_1_approximate_majority_2026_eds_full.gpkg"
    )
    hyb = pd.read_csv(DATA / "majority_hybrid_crosswalk.csv")
    reall = pd.read_csv(DATA / "338canada_reallocated_majority.csv")

    # map 2019 -> list of candidate 2026 assignments with priority/type
    candidates: dict[str, list[tuple[int, str, str]]] = {n: [] for n in eds_2019_set}

    # Priority 1: parents_2019 in gpkg (highest confidence)
    for _, r in gpkg.iterrows():
        parents = norm(r.get("parents_2019") or "")
        if not parents:
            continue
        name_2026 = norm(r["name_2026"])
        for p in parents.split(";"):
            p = norm(p)
            if p in eds_2019_set:
                tp = "rename" if p != name_2026 else "identity"
                candidates[p].append((1, name_2026, f"gpkg_parents ({tp})"))

    # Priority 2: explicit hybrid crosswalk
    for _, r in hyb.iterrows():
        cur = norm(r["current_2019"])
        prop = norm(r["proposed_2026"])
        if cur in eds_2019_set:
            tp = (
                "hybrid"
                if "-" in prop and prop != cur
                else ("rename" if prop != cur else "identity")
            )
            candidates[cur].append((2, prop, f"hybrid_xwalk ({tp})"))

    # Priority 3: 338canada reallocation reversed
    # Each row: 2026_ed <- sources (2019 ED). Reverse: 2019 source ED -> 2026 ed.
    # Several 2026 EDs can share a 2019 source (split). Track them all.
    rev: dict[str, list[str]] = {}
    for _, r in reall.iterrows():
        name_2026 = norm(r["ed"])
        srcs = norm(r["sources"])
        if not srcs:
            continue
        # sources can be 'a|b' for merges (forward: 2026 has multiple sources)
        for src in srcs.split("|"):
            src = norm(src)
            if not src:
                continue
            rev.setdefault(src, []).append(name_2026)

    for src_2019, successors in rev.items():
        if src_2019 not in eds_2019_set:
            continue
        # Prefer a successor whose name matches exactly (identity), else most populous
        if len(successors) == 1:
            sel = successors[0]
            tp = "identity" if sel == src_2019 else "rename_or_split_primary"
            candidates[src_2019].append((3, sel, f"reall_single ({tp})"))
        else:
            # Tie-break: prefer identical-name successor, else largest population
            identical = [s for s in successors if s == src_2019]
            if identical:
                sel = identical[0]
                tp = "split_primary_keeps_name"
            else:
                # Also prefer successor whose name CONTAINS the 2019 name prefix (e.g. "Calgary-Foothills" -> "Calgary-Foothills-Airdrie West")
                contains = [
                    s
                    for s in successors
                    if src_2019.lower() in s.lower() or s.lower() in src_2019.lower()
                ]
                if contains:
                    # pick most populous among contains
                    sel = max(contains, key=lambda s: maj_pop_by_name.get(s, 0))
                    tp = "split_primary_substring"
                else:
                    sel = max(successors, key=lambda s: maj_pop_by_name.get(s, 0))
                    tp = "split_primary_largest"
            candidates[src_2019].append(
                (3, sel, f"reall_multi ({tp}, opts={len(successors)})")
            )

    # Manual commission-report fallbacks — 2019 EDs that may still be unassigned
    # or need explicit overrides due to known majority restructuring.
    # Based on analysis/reports/91_seat_preliminary.md F6: Calgary +2 (Nose Creek, Confluence, McKenzie; Peigan eliminated)
    # Peigan 2019 was absorbed; the 2026 area is split between Calgary-Peigan-adjacent EDs.
    manual = {
        # 2019 -> (2026 successor, note)
        "Calgary-Peigan": (
            "Calgary-McKenzie",
            "manual: Peigan eliminated in majority; McKenzie covers S. Calgary Peigan territory",
        ),
        "Calgary-Foothills": (
            "Calgary-Nose Creek",
            "manual: Foothills restructured; Nose Creek absorbs north-Calgary territory",
        ),
        "Calgary-McCall": (
            "Calgary-Bhullar-McCall",
            "manual: McCall renamed to Bhullar-McCall",
        ),
        "Calgary-West": (
            "Calgary-West-Elbow Valley",
            "manual: West restructured with Elbow Valley addition",
        ),
        "Calgary-Glenmore": (
            "Calgary-Glenmore-Tsuut'ina",
            "manual: Glenmore + Tsuut'ina addition",
        ),
        "Calgary-Falconridge": (
            "Calgary-Falconridge-Conrich",
            "manual: Falconridge + Conrich addition",
        ),
        "Banff-Kananaskis": (
            "Canmore-Banff",
            "manual: Banff-Kananaskis renamed/relocated under majority",
        ),
        "Cardston-Siksika": (
            "High River-Vulcan-Siksika",
            "manual: Siksika territory absorbed into High River-Vulcan-Siksika",
        ),
        "Highwood": (
            "Okotoks-Diamond Valley",
            "manual: Highwood restructured -> Okotoks-Diamond Valley",
        ),
        "Drayton Valley-Devon": (
            "Stony Plain-Drayton Valley",
            "manual: Drayton Valley-Devon renamed Stony Plain-Drayton Valley",
        ),
        "Edmonton-Glenora": (
            "Edmonton-Glenora-Riverview",
            "manual: Edmonton-Glenora merged with Riverview",
        ),
        "Edmonton-Riverview": (
            "Edmonton-Glenora-Riverview",
            "manual: Edmonton-Riverview merged with Glenora",
        ),
        "Edmonton-South West": (
            "Edmonton-Windermere",
            "manual: Edmonton-South West absorbed into Edmonton-Windermere",
        ),
        "Innisfail-Sylvan Lake": ("Sylvan Lake-Innisfail", "manual: renamed"),
        "Lac Ste. Anne-Parkland": (
            "Edmonton-Enoch",
            "manual: LSA-Parkland absorbed into Edmonton-Enoch (majority)",
        ),
        "Olds-Didsbury-Three Hills": (
            "Mountain View-Kneehill",
            "manual: Olds-Didsbury-Three Hills restructured as Mountain View-Kneehill (majority)",
        ),
        "Rimbey-Rocky Mountain House-Sundre": (
            "Lacombe-Clearwater",
            "manual: RMH-Sundre restructured into Lacombe-Clearwater under majority",
        ),
        "Taber-Warner": (
            "Taber-Cardston",
            "manual: Taber-Warner merged with Cardston portion to form Taber-Cardston (majority)",
        ),
        "Athabasca-Barrhead-Westlock": (
            "Barrhead-Westlock-Athabasca",
            "manual: reorder rename",
        ),
        "Airdrie-Cochrane": (
            "Airdrie-West",
            "manual: Airdrie-Cochrane restructured to Airdrie-West",
        ),
    }
    for k, (v, note) in manual.items():
        k_n = norm(k)
        v_n = norm(v)
        if k_n in eds_2019_set and v_n in maj_2026_set:
            candidates[k_n].append((4, v_n, f"manual ({note})"))

    # Resolve: take lowest priority-number candidate per 2019 ED
    rows = []
    for k in sorted(eds_2019_set):
        if not candidates[k]:
            rows.append(
                {
                    "current_2019": k,
                    "proposed_2026": k,
                    "type": "identity_fallback",
                    "source": "no_mapping_found",
                }
            )
            continue
        candidates[k].sort(key=lambda t: (t[0], t[1]))  # stable
        pri, sel, src = candidates[k][0]
        # Validate sel is in 2026 set
        if sel not in maj_2026_set:
            # pick next candidate whose target is in maj_2026_set
            picked = None
            for p2, s2, src2 in candidates[k]:
                if s2 in maj_2026_set:
                    picked = (p2, s2, src2)
                    break
            if picked:
                pri, sel, src = picked
            else:
                sel, src = k, f"forced_identity_fallback (orig={sel})"
        tp = (
            "identity"
            if sel == k
            else (
                "rename"
                if any(s in src for s in ["rename", "hybrid"])
                else "split_primary"
            )
        )
        rows.append(
            {"current_2019": k, "proposed_2026": sel, "type": tp, "source": src}
        )

    df = pd.DataFrame(rows)
    return df


def build_minority_crosswalk() -> pd.DataFrame:
    eds_2019 = gpd.read_file(
        DATA
        / "shapefiles"
        / "reference"
        / "alberta_2019_eds"
        / "EDS_ENACTED_BILL33_15DEC2017.shp"
    )
    eds_2019_set = set(norm(n) for n in eds_2019["EDName2017"].unique())

    min_pops = pd.read_csv(DATA / "minority_2026_populations.csv")
    min_2026_set = set(norm(n) for n in min_pops["ed_name"])
    min_pop_by_name = {
        norm(r["ed_name"]): int(r["population"]) for _, r in min_pops.iterrows()
    }

    gpkg = gpd.read_file(
        DATA / "shapefiles" / "derived" / "v0_1_refined_v6_minority_2026_eds_full.gpkg"
    )
    hyb = pd.read_csv(DATA / "minority_hybrid_crosswalk.csv")
    reall = pd.read_csv(DATA / "338canada_reallocated_minority.csv")

    candidates: dict[str, list[tuple[int, str, str]]] = {n: [] for n in eds_2019_set}

    # P1: gpkg parents_2019
    for _, r in gpkg.iterrows():
        parents = norm(r.get("parents_2019") or "")
        if not parents:
            continue
        name_2026 = norm(r["name_2026"])
        for p in parents.split(";"):
            p = norm(p)
            if p in eds_2019_set:
                tp = "rename" if p != name_2026 else "identity"
                candidates[p].append((1, name_2026, f"gpkg_parents ({tp})"))

    # P2: hybrid crosswalk, skipping MERGED/ABSORBED placeholders
    # (these are marked with proposed_2026 = "(MERGED/ABSORBED)")
    for _, r in hyb.iterrows():
        cur = norm(r["current_2019"])
        prop = norm(r["proposed_2026"])
        if (
            cur in eds_2019_set
            and prop
            and "MERGED" not in prop.upper()
            and "ABSORBED" not in prop.upper()
        ):
            tp = (
                "hybrid"
                if r.get("is_hybrid") == "yes"
                else ("rename" if prop != cur else "identity")
            )
            candidates[cur].append((2, prop, f"hybrid_xwalk ({tp})"))

    # P3: 338canada reallocation reversed
    rev: dict[str, list[str]] = {}
    for _, r in reall.iterrows():
        name_2026 = norm(r["ed"])
        srcs = norm(r["sources"])
        if not srcs:
            continue
        for src in srcs.split("|"):
            src = norm(src)
            if not src:
                continue
            rev.setdefault(src, []).append(name_2026)

    for src_2019, successors in rev.items():
        if src_2019 not in eds_2019_set:
            continue
        if len(successors) == 1:
            sel = successors[0]
            tp = "identity" if sel == src_2019 else "rename_or_split_primary"
            candidates[src_2019].append((3, sel, f"reall_single ({tp})"))
        else:
            identical = [s for s in successors if s == src_2019]
            if identical:
                sel = identical[0]
                tp = "split_primary_keeps_name"
            else:
                contains = [
                    s
                    for s in successors
                    if src_2019.lower() in s.lower() or s.lower() in src_2019.lower()
                ]
                if contains:
                    sel = max(contains, key=lambda s: min_pop_by_name.get(s, 0))
                    tp = "split_primary_substring"
                else:
                    sel = max(successors, key=lambda s: min_pop_by_name.get(s, 0))
                    tp = "split_primary_largest"
            candidates[src_2019].append(
                (3, sel, f"reall_multi ({tp}, opts={len(successors)})")
            )

    # P4: manual overrides for MERGED/ABSORBED rows, using the absorbing-ED's parents_2019
    # Read the gpkg's parents_2019 to figure out which 2026 ED each absorbed 2019 ED went into
    # (some of the merged/absorbed 2019 EDs are already handled by the 338 reallocation; this catches the rest).
    absorbed_in_hyb = set()
    for _, r in hyb.iterrows():
        cur = norm(r["current_2019"])
        prop = norm(r["proposed_2026"])
        if "MERGED" in prop.upper() or "ABSORBED" in prop.upper():
            absorbed_in_hyb.add(cur)

    manual = {
        # absorbed 2019 ED -> 2026 ED inferred from commission report / majority restructure
        "Airdrie-Cochrane": (
            "Calgary-Nolan Hill-Cochrane",
            "manual: Airdrie-Cochrane absorbed -> Nolan Hill-Cochrane",
        ),
        "Banff-Kananaskis": (
            "Canmore-Kananaskis",
            "manual: Banff-Kananaskis -> Canmore-Kananaskis (rename)",
        ),
        "Calgary-Shaw": (
            "Calgary-South",
            "manual: Calgary-Shaw split between De Winton and South; South is primary",
        ),
        "Cardston-Siksika": (
            "Lethbridge-Cardston",
            "manual: Cardston-Siksika absorbed -> Lethbridge-Cardston",
        ),
        "Edmonton-Castle Downs": ("Edmonton-Castledowns", "manual: renamed"),
        "Edmonton-Riverview": (
            "Edmonton-Glenora-Riverview",
            "manual: merged into Glenora-Riverview",
        ),
        "Edmonton-South West": (
            "Edmonton-Windermere",
            "manual: absorbed into Edmonton-Windermere",
        ),
        "Lacombe-Ponoka": (
            "Red Deer-Lacombe",
            "manual: Lacombe-Ponoka absorbed -> Red Deer-Lacombe",
        ),
        "Lethbridge-East": (
            "Lethbridge-Taber-Warner",
            "manual: Lethbridge-East absorbed -> Lethbridge-Taber-Warner (primary)",
        ),
        "Lethbridge-West": (
            "Lethbridge-Fort MacLeod-Crowsnest Pass",
            "manual: Lethbridge-West absorbed -> Lethbridge-Ft MacLeod",
        ),
        "Livingstone-Macleod": (
            "Lethbridge-Fort MacLeod-Crowsnest Pass",
            "manual: Livingstone-Macleod absorbed -> Lethbridge-Ft MacLeod",
        ),
        "Maskwacis-Wetaskiwin": (
            "Wetaskawin-Ponoka-Maskwacis",
            "manual: renamed+consolidated",
        ),
        "Okotoks-Sheep River": (
            "Highwood",
            "manual: Okotoks-Sheep River absorbed -> Highwood",
        ),
        "Vermilion-Wainwright": (
            "Lloydminster-Wainwright",
            "manual: Vermilion-Wainwright absorbed -> Lloydminster-Wainwright",
        ),
        # Also fill any 2019 EDs not in candidates yet
        "Rimbey-Rocky Mountain House-Sundre": (
            "Rocky Mountain House-Banff Park",
            "manual: RMH-Sundre -> RMH-Banff Park",
        ),
        "Calgary-Foothills": (
            "Calgary-Foothills-Airdrie West",
            "manual: Foothills extends to Airdrie West",
        ),
        "Calgary-Peigan": (
            "Calgary-Peigan-Chestermere",
            "manual: Peigan + Chestermere hybrid",
        ),
        "Calgary-McCall": ("Calgary-McCall-Bhullar", "manual: McCall renamed/hybrid"),
        "Calgary-West": ("Calgary-West-Tsuut'ina", "manual: West extends to Tsuut'ina"),
        "Calgary-North West": ("Calgary-North West-Bearspaw", "manual: NW hybrid"),
        "Calgary-Bow": ("Calgary-Bow-Springbank", "manual: Bow + Springbank hybrid"),
        "Taber-Warner": (
            "Lethbridge-Taber-Warner",
            "manual: Taber-Warner absorbed into Lethbridge-Taber-Warner",
        ),
        "Morinville-St. Albert": (
            "St. Albert-Sturgeon",
            "manual: renamed St. Albert-Sturgeon",
        ),
        "Spruce Grove-Stony Plain": (
            "Edmonton-Spruce Grove",
            "manual: renamed Edmonton-Spruce Grove",
        ),
        "Cold Lake-St. Paul": ("Cold Lake-Bonnyville-St. Paul", "manual: consolidated"),
        "Bonnyville-Cold Lake-St. Paul": (
            "Cold Lake-Bonnyville-St. Paul",
            "manual: consolidated (reorder)",
        ),
        "Olds-Didsbury-Three Hills": (
            "Olds-Three Hills-Didsbury",
            "manual: reorder rename",
        ),
        "Drayton Valley-Devon": (
            "Stony Plain-Drayton Valley",
            "manual: DV-Devon -> Stony Plain-DV",
        ),
        "Leduc-Beaumont": (
            "Leduc",
            "manual: Leduc-Beaumont -> Leduc (Beaumont split to Edmonton-Beaumont)",
        ),
        "Innisfail-Sylvan Lake": ("Red Deer-Sylvan Lake", "manual: renamed"),
        "Red Deer-North": (
            "Red Deer-Innisfail",
            "manual: split primary (also Red Deer-Lacombe); Red Deer-Innisfail primary",
        ),
        "Red Deer-South": ("Red Deer-Blackfalds", "manual: renamed/hybrid"),
        "Cypress-Medicine Hat": ("Medicine Hat-Cypress", "manual: reorder rename"),
        "Brooks-Medicine Hat": ("Medicine Hat-Brooks", "manual: reorder rename"),
        "Vermilion-Lloydminster-Wainwright": (
            "Lloydminster-Wainwright",
            "manual: Vermilion split out",
        ),
        "Athabasca-Barrhead-Westlock": (
            "Barrhead-Westlock-Athabasca",
            "manual: reorder rename",
        ),
        "Airdrie-East": (
            "Airdrie East",
            "manual: Airdrie-East -> Airdrie East (no hyphen)",
        ),
    }
    for k, (v, note) in manual.items():
        k_n = norm(k)
        v_n = norm(v)
        if k_n in eds_2019_set and v_n in min_2026_set:
            candidates[k_n].append((4, v_n, f"manual ({note})"))

    # Resolve
    rows = []
    for k in sorted(eds_2019_set):
        if not candidates[k]:
            # Fall back to identity only if k is in 2026 set; else flag
            if k in min_2026_set:
                rows.append(
                    {
                        "current_2019": k,
                        "proposed_2026": k,
                        "type": "identity",
                        "source": "identity_found_in_2026",
                    }
                )
            else:
                rows.append(
                    {
                        "current_2019": k,
                        "proposed_2026": k,
                        "type": "identity_fallback_missing",
                        "source": "no_mapping_found_and_not_in_2026",
                    }
                )
            continue
        candidates[k].sort(key=lambda t: (t[0], t[1]))
        pri, sel, src = candidates[k][0]
        if sel not in min_2026_set:
            picked = None
            for p2, s2, src2 in candidates[k]:
                if s2 in min_2026_set:
                    picked = (p2, s2, src2)
                    break
            if picked:
                pri, sel, src = picked
            else:
                sel, src = k, f"forced_identity_fallback (orig={sel})"
        tp = (
            "identity"
            if sel == k
            else (
                "rename"
                if any(s in src for s in ["rename", "hybrid"])
                else "split_primary"
            )
        )
        rows.append(
            {"current_2019": k, "proposed_2026": sel, "type": tp, "source": src}
        )

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    print("Building full majority crosswalk...")
    maj_df = build_majority_crosswalk()
    out_maj = DATA / "majority_full_crosswalk.csv"
    maj_df.to_csv(out_maj, index=False)
    print(f"  wrote {out_maj} ({len(maj_df)} rows)")
    print("  type counts:", maj_df["type"].value_counts().to_dict())

    print("\nBuilding full minority crosswalk...")
    min_df = build_minority_crosswalk()
    out_min = DATA / "minority_full_crosswalk.csv"
    min_df.to_csv(out_min, index=False)
    print(f"  wrote {out_min} ({len(min_df)} rows)")
    print("  type counts:", min_df["type"].value_counts().to_dict())

    # Audit: any rows whose 2026 target is NOT in the populations list?
    maj_pops = pd.read_csv(DATA / "majority_2026_populations.csv")
    maj_set = set(maj_pops["ed_name"].astype(str).str.strip())
    bad_maj = maj_df[~maj_df["proposed_2026"].isin(maj_set)]
    if len(bad_maj):
        print(
            "\nMAJORITY: 2019 rows mapping to non-2026 ED names (", len(bad_maj), "):"
        )
        print(bad_maj.to_string(index=False))

    min_pops = pd.read_csv(DATA / "minority_2026_populations.csv")
    min_set = set(norm(n) for n in min_pops["ed_name"])
    bad_min = min_df[~min_df["proposed_2026"].apply(lambda x: norm(x) in min_set)]
    if len(bad_min):
        print(
            "\nMINORITY: 2019 rows mapping to non-2026 ED names (", len(bad_min), "):"
        )
        print(bad_min.to_string(index=False))
