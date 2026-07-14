# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Rural-division count and succession test — the minority's charge, executed.

MOTIVATION. The minority report charges the majority map with "an inclination
to delete or mangle rural electoral divisions and, in effect, reduce effective
rural representation" (commission final report, minority report p. 356) and
with "insistence on eliminating and amalgamating certain rural divisions"
(ibid.). Surfacing that charge into the audit record (2026-07-14) without
testing it would repeat the one-way-evidence pattern the audit discounts
elsewhere. This script tests it now, symmetrically, on canonical shapefiles.

STATUS: EXPLORATORY. Written and executed in-session on data that already
exists and has been partially examined in adjacent analyses. It is labelled
exploratory under the audit's own §4.3.1 standard and can never be promoted.

HYPOTHESES — FROZEN IN THIS HEADER BEFORE FIRST EXECUTION (2026-07-14):
  H-charge (the minority's prediction): the majority map has FEWER
    rural-anchored divisions than the minority map, and more 2019
    rural-anchored divisions lose their rural anchor under the majority
    (absorbed into urban-anchored successors, or amalgamated together)
    than under the minority.
  H-null: the two 2026 maps treat rural divisions alike (counts and
    successions within ±1 of each other).
  No numeric pass/fail threshold is declared — the output is a descriptive
  count-and-name comparison, reported whichever way it cuts.

METHOD.
  Classifier: the audit's established rural/urban name rule (identical to
  T3.2, Amendment-corrected): an ED is rural-anchored iff its name does not
  start with any of the URBAN_PREFIXES below. Known limitation, inherited
  from T3.2 and disclosed there: name-based classification is inferior to a
  CSD-overlap rule (hybrid ridings carrying a city name classify urban even
  where they absorb large rural territory, and vice versa for rural-named
  hybrids); the same rule is applied to all three maps, so the comparison is
  symmetric even where the rule is coarse.
  Succession: all layers reprojected to EPSG:3400; each 2019 ED's successor
  under each 2026 map is the ED with the largest intersection area.
    - A 2019 rural ED is ABSORBED if its successor is urban-anchored.
    - Two or more 2019 rural EDs are AMALGAMATED if they share one
      rural-anchored successor.
    - A 2026 rural ED is NEW if it is no 2019 rural ED's successor.

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
  analysis/scripts/t3_2_majority_rural_isolation.py — classifier provenance
Forward:
  findings/rural_division_count.md
  findings/rural_division_count.json
"""
from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent

URBAN_PREFIXES: tuple[str, ...] = (
    "Calgary-", "Edmonton-", "Airdrie", "Lethbridge-", "Red Deer-",
    "Medicine Hat-", "St. Albert-", "Sherwood Park-",
    "Fort McMurray-", "Grande Prairie-", "Spruce Grove-",
)

CANONICAL_CRS = "EPSG:3400"

MAPS = {
    "majority_2026": {
        "path": ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
        "name_col": "EDName2025",
    },
    "minority_2026": {
        "path": ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
        "name_col": "EDName2025",
    },
    "enacted_2019": {
        "path": ROOT / "data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp",
        "name_col": "EDName2017",
    },
}


def is_rural(name: str) -> bool:
    return not any(name.startswith(p) for p in URBAN_PREFIXES)


# SENSITIVITY RULE (added after first execution, disclosed in the findings
# file): inspection of the frozen rule's output found the same hyphen-
# sensitivity artifact the T3.2 Amendment fixed for "Airdrie" — bare city
# names ("St. Albert", "Sherwood Park", "Grande Prairie", "Spruce Grove")
# do not match the hyphen-suffixed prefixes and classify rural. The
# corrected rule treats a name as urban if it equals a city name or starts
# with it followed by a hyphen or space. Reported alongside the frozen rule,
# never in place of it.
CITY_NAMES: tuple[str, ...] = (
    "Calgary", "Edmonton", "Airdrie", "Lethbridge", "Red Deer",
    "Medicine Hat", "St. Albert", "St Albert",  # minority map omits the period
    "Sherwood Park", "Fort McMurray", "Grande Prairie", "Spruce Grove",
)


def is_rural_corrected(name: str) -> bool:
    for c in CITY_NAMES:
        if name == c or name.startswith(c + "-") or name.startswith(c + " "):
            return False
    return True


def load(key: str, rule=is_rural) -> gpd.GeoDataFrame:
    spec = MAPS[key]
    gdf = gpd.read_file(spec["path"]).to_crs(CANONICAL_CRS)
    gdf = gdf.rename(columns={spec["name_col"]: "name"})[["name", "geometry"]]
    gdf["rural"] = gdf["name"].map(rule)
    return gdf


def successions(base: gpd.GeoDataFrame, target: gpd.GeoDataFrame) -> dict[str, str]:
    """Max-area-overlap successor in `target` for each ED in `base`."""
    out: dict[str, str] = {}
    sindex = target.sindex
    for _, row in base.iterrows():
        cands = target.iloc[list(sindex.intersection(row.geometry.bounds))]
        best, best_a = None, 0.0
        for _, t in cands.iterrows():
            a = row.geometry.intersection(t.geometry).area
            if a > best_a:
                best, best_a = t["name"], a
        out[row["name"]] = best
    return out


def analyse(map_key: str, g2019: gpd.GeoDataFrame, rule=is_rural) -> dict:
    g = load(map_key, rule)
    succ = successions(g2019, g)
    rural_2019 = [n for n in succ if rule(n)]
    urban_lookup = dict(zip(g["name"], g["rural"]))

    absorbed = sorted(n for n in rural_2019 if not urban_lookup.get(succ[n], True))
    # amalgamation: rural successors shared by >=2 rural 2019 EDs
    shared: dict[str, list[str]] = {}
    for n in rural_2019:
        s = succ[n]
        if urban_lookup.get(s, False):
            shared.setdefault(s, []).append(n)
    amalgams = {s: sorted(v) for s, v in shared.items() if len(v) >= 2}
    rural_names = sorted(g.loc[g["rural"], "name"])
    succ_rural_targets = {succ[n] for n in rural_2019}
    new_rural = sorted(n for n in rural_names if n not in succ_rural_targets)
    return {
        "total_eds": int(len(g)),
        "rural_count": int(g["rural"].sum()),
        "rural_share": round(float(g["rural"].mean()), 4),
        "rural_names": rural_names,
        "rural_2019_absorbed_into_urban_successor": absorbed,
        "amalgamations_rural_2019_sharing_one_rural_successor": amalgams,
        "new_rural_divisions_no_2019_rural_predecessor": new_rural,
    }


def run(rule) -> dict:
    g2019 = load("enacted_2019", rule)
    return {
        "enacted_2019": {
            "total_eds": int(len(g2019)),
            "rural_count": int(g2019["rural"].sum()),
            "rural_share": round(float(g2019["rural"].mean()), 4),
            "rural_names": sorted(g2019.loc[g2019["rural"], "name"]),
        },
        "majority_2026": analyse("majority_2026", g2019, rule),
        "minority_2026": analyse("minority_2026", g2019, rule),
    }


def main() -> None:
    result = {
        "frozen_rule": run(is_rural),
        "corrected_rule_sensitivity": run(is_rural_corrected),
        "classifier": "frozen = T3.2 name-prefix rule; corrected = hyphen/space/bare-name robust variant (see header)",
        "status": "exploratory — hypotheses frozen in script header before execution; corrected rule added post-inspection as a disclosed sensitivity",
    }
    out = ROOT / "findings" / "rural_division_count.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    for rule_key in ("frozen_rule", "corrected_rule_sensitivity"):
        print(f"==== {rule_key} ====")
        block = result[rule_key]
        for k in ("enacted_2019", "majority_2026", "minority_2026"):
            r = block[k]
            print(f"{k}: {r['rural_count']} rural of {r['total_eds']} "
                  f"({100*r['rural_share']:.1f}%)")
        for k in ("majority_2026", "minority_2026"):
            r = block[k]
            print(f"{k} — absorbed({len(r['rural_2019_absorbed_into_urban_successor'])}): "
                  f"{r['rural_2019_absorbed_into_urban_successor']}")
            print(f"{k} — amalgamations: {r['amalgamations_rural_2019_sharing_one_rural_successor']}")
            print(f"{k} — new rural: {r['new_rural_divisions_no_2019_rural_predecessor']}")
        print()
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
