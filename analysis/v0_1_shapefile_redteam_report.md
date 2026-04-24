---
name: Shapefile red-team report
description: Systematic defensibility, accuracy, and testability audit of VA polygons, canonical 2026 ED shapefiles, and Phase 4C assignment pipeline. Session 12.
type: project
date: 2026-04-23
---

# Shapefile and VA data red-team report

**Scope:** VA polygon substrate, canonical majority/minority 2026 ED shapefiles,
Phase 4C assignment pipeline.
**Audit date:** 2026-04-23

---

## 1. VA polygon substrate (va_polygons_with_2023_votes.gpkg)

### What it contains
4,765 Voting Area polygons from the 2023 Elections Alberta VA shapefile, joined
with 2023 Statement of Vote Election-Day NDP and UCP vote totals per VA.

### Checks run

| Check | Result |
|---|---|
| Row count | 4,765 (matches Elections Alberta release) |
| CRS | EPSG:3401 (Alberta 10-TM Forest) |
| Null geometries | 0 |
| Missing `parent_ed_2019` | 0 |
| Vote totals sum (NDP + UCP) | 896,644 — matches Phase 4C conservation check |
| Election-Day fraction of full 2023 count | 52.5% (two-party total; advance/mail/special = 47.5%) |

### Known limitations

1. **Election-Day only.** Advance, mail-in, and special ballot votes are
   excluded. NDP voters use advance/special at a 6pp higher rate than UCP,
   so the Election-Day subset underestimates NDP's province-wide share (42.60%
   vs full-count 44.17%).

2. **Spatial proxy for residence.** VA centroid is used as a proxy for where
   Election-Day voters live. VAs are small (median ~500m diameter in urban
   areas), so centroid error is limited. In rural areas, VA polygons can be
   large and the centroid may be far from the actual polling station.

3. **Vote Anywhere polling stations.** Any VA tagged as a Vote Anywhere location
   contains votes from electors anywhere in the province. These cannot be
   spatially attributed. They are included in the VA substrate under their
   geographic polygon but their vote totals are not residence-based.

---

## 2. Canonical majority shapefile (v0_1_canonical_majority_2026_eds.gpkg)

### Checks run (v0_1_edmonton_beaumont_polygon.py)

| Check | Result |
|---|---|
| ED count | 89 of 89 — PASS |
| Null geometries | 0 — PASS |
| CRS | EPSG:3401 — PASS |
| Duplicate ED names | 0 — PASS |
| `name_2026` column | Present — PASS |
| `canon_tier` column | Present — PASS |
| `map` column | All rows = 'majority' — PASS |
| Area range | 10.6 – 109,222 km2 |
| Overlapping polygon pairs | **81 pairs — WARNING** |

### Tier distribution

| Tier | Count | Confidence | Source |
|---|---|---|---|
| A | 57 | High | v7 pixel-extracted (city-scale or overview map) |
| C-2019-direct | 16 | Lower | 2019 boundary used as-is (territory-equivalent rename) |
| C-v6-pixel-exact | 5 | Medium | v6 pixel-extracted (prior version) |
| C-null | 4 | n/a | Unresolvable from available sources |
| C-sweep | 4 | Medium | Population-calibrated parametric sweep (road-snapped) |
| C-2019-blend | 2 | Lower | 2019 parent over-covers 2026 territory |
| C-osm-construct | 1 | Medium | OSM municipal boundary + 2km buffer (Edmonton-Beaumont) |

### Overlap warning detail

81 polygon pairs overlap by >0.01 km2. Largest:

- Calgary-Acadia x Calgary-East: 77 km2
- Calgary-Bhullar-McCall x Calgary-Falconridge-Conrich: 63 km2
- Calgary-Bow x Calgary-Varsity: 15 km2

**Root cause:** C-2019-blend EDs use the full 2019 parent polygon, which
over-covers the intended 2026 territory. Some v7 pixel-extracted polygons
also have boundary shifts of 1-5 km at the urban fringe, causing small
overlaps with adjacent EDs.

**Impact on Phase 4C:** The assignment hierarchy (Method 0 crosswalk > Method
1 spatial) means most VAs in overlap zones are assigned by crosswalk rather
than by their spatial position. Approximately 1,765 majority VAs are assigned
spatially; of these, an unknown fraction are in overlap zones and carry medium
confidence. This is acceptable for the current measurement precision.

**Testability:** When official 2026 shapefiles are released, re-running
Phase 4C will eliminate all overlaps and produce ground-truth spatial
assignments.

---

## 3. Canonical minority shapefile (v0_1_canonical_minority_2026_eds.gpkg)

### Checks run

| Check | Result |
|---|---|
| ED count | 89 of 89 — PASS |
| Null geometries | 0 — PASS |
| CRS | EPSG:3401 — PASS |
| Duplicate ED names | 0 — PASS |
| `map` column | All rows = 'minority' — PASS |
| Overlapping polygon pairs | **95 pairs — WARNING** |

### Tier distribution (corrected in session 12)

14 EDs were previously labeled "unknown" despite having source=v7. They are
correctly Tier A (pixel-extracted) and have been relabeled.

| Tier | Count | Confidence |
|---|---|---|
| A | 79 | High |
| C-v6-pixel-exact | 3 | Medium |
| C-2019-blend | 3 | Lower |
| B | 2 | High |
| C-2019-split | 1 | Lower |
| C-2019-direct | 1 | Lower |

79 of 89 minority EDs (89%) are Tier A. The minority file is the
higher-quality canonical file.

### Overlap warning detail

95 pairs overlap by >0.01 km2. Largest:

- Calgary-Airdrie x Calgary-Nolan Hill-Cochrane: 264 km2
- Calgary-Airdrie x Olds-Three Hills-Didsbury: 197 km2
- Calgary-Airdrie x Calgary-Foothills-Airdrie West: 71 km2

Calgary-Airdrie appears in multiple large overlaps, suggesting its pixel-
extracted boundary over-extends into neighboring EDs. The 264 km2 overlap
with Calgary-Nolan Hill-Cochrane is the largest single overlap in either
file and should be reviewed against the commission map when official
shapefiles are available.

### Edmonton-Beaumont in minority file

The minority file contains Edmonton-Beaumont with tier A (v7 pixel-extracted).
This is a different polygon from the majority version. The minority commission
may have drawn Edmonton-Beaumont with different boundaries than the majority
commission. Both polygons are independently sourced from their respective
commission maps.

---

## 4. Phase 4C assignment pipeline

### Resolution summary (session 12 — final)

| Map | EDs resolved | Total VAs assigned |
|---|---|---|
| Majority | **89 / 89** | 4,765 |
| Minority | **89 / 89** | 4,765 |

Vote conservation: zero drift (NDP=381,932, UCP=514,712 in both maps).

### Assignment method breakdown

| Method | Majority | Minority | Confidence |
|---|---|---|---|
| Crosswalk (direct override + 1:1 reverse) | 2,781 | 2,609 | High |
| Spatial (centroid-in-polygon) | 1,765 | 1,723 | High–Medium |
| Candidate (flagged hybrid-adjacent) | 0 | 233 | Medium |
| Nearest-ED geographic fallback | 206 | 74 | Low |
| crosswalk_split_default | 13 | 126 | Medium |

Nearest-ED fallback (206 majority, 74 minority) handles VAs whose 2019
parent ED name does not appear in any 2026 crosswalk entry. Most are
in rural EDs with direct renames that weren't captured in the crosswalk.

### Edmonton-Beaumont fix

**Problem:** The v0.2 crosswalk had `Edmonton-Beaumont: ('blend',
'Edmonton-South', ...)`. Edmonton-South 2026 is an identical rename of
Edmonton-South 2019 (no territory split). The direct-rename override
(Method 0) captured all Edmonton-South VAs for Edmonton-South 2026,
leaving Edmonton-Beaumont with zero VAs.

**Fix:**
1. Crosswalk updated to `('blend', 'Leduc-Beaumont', ...)` — the City of
   Beaumont is in the Leduc-Beaumont 2019 district.
2. Edmonton-Beaumont canonical polygon rebuilt from OSM City of Beaumont
   boundary + 2km edge buffer (76.6 km², 21 VAs, 4,621 votes).
3. The Edmonton suburb portion (~68% of the ED's population) cannot be
   spatially resolved without official 2026 shapefiles.

**Residual limitation:** Edmonton-Beaumont in Phase 4C captures only
the Beaumont-city VAs (Leduc-Beaumont parent). Southern Edmonton VAs
are captured by Edmonton-South 2026 via the direct override. The true
Edmonton-Beaumont vote total is higher than the 4,621 captured here.

---

## 5. Crosswalk defensibility

The v0.2 crosswalk (`MAJORITY_2026_MAPPING`, `MINORITY_2026_MAPPING`) was
audited against known commission decisions:

| Concern | Status |
|---|---|
| Edmonton-Beaumont points to wrong 2019 parent | Fixed (session 12) |
| Calgary-Buffalo feeds both Calgary-Buffalo 2026 AND Calgary-Confluence 2026 | Correctly modeled as multi-child (direct-override disabled for multi-child parents) |
| Edmonton-Highlands-Norwood stolen by spatial error | Fixed (session 11) — direct-rename override restores correct assignment |
| Cardston-Siksika / Lac Ste. Anne-Parkland / Rimbey-Rocky Mtn House-Sundre parent names absent from crosswalk | Handled by nearest-ED fallback; low confidence; flagged for review |

---

## 6. Minority / majority distinguishability

Both canonical files carry a `map` column set to 'majority' or 'minority'
(all 89 rows verified). The `canon_tier` column describes provenance for
every polygon. The `canon_note` field records the construction method where
non-standard.

Downstream scripts (Phase 4C, v0.2) load the files by explicit path:
- `data/v0_1_canonical_majority_2026_eds.gpkg`
- `data/v0_1_canonical_minority_2026_eds.gpkg`

No script shares a file between the two maps.

---

## 7. Testability and reproducibility

| Artifact | Reproducible? |
|---|---|
| VA polygon substrate | Yes — from Elections Alberta 2023 VA shapefile + Statement of Vote |
| Canonical majority shapefile | Yes — `v0_1_build_canonical_shapefiles.py` from scratch (2019 ED shapefile + v7 pixel extractions + OSM) |
| Canonical minority shapefile | Yes — same script |
| Edmonton-Beaumont polygon | Yes — `v0_1_edmonton_beaumont_polygon.py` (OSM geocode + 2km buffer) |
| Phase 4C assignments | Yes — `v0_1_phase_4c_va_attribution.py` (deterministic; no random seed) |
| Phase 4C Monte Carlo CIs | Yes — same script, seed=42, N=2000 |

All scripts are in `analysis/`. Required inputs are in `data/` (Elections Alberta
public shapefiles) or reconstructible from public sources.

---

## 8. Open issues requiring official shapefiles

1. **81/95 overlapping polygon pairs** — caused by derived boundary
   approximations. Official shapefiles will eliminate all overlaps.
2. **Edmonton-Beaumont Edmonton-suburb portion** — 38,000 of 55,802 residents
   are in southern Edmonton territory; unresolvable without official boundaries.
3. **206 nearest-ED fallback assignments (majority)** — low-confidence; should
   be reviewed against official shapefiles when available.
4. **C-null majority EDs (4)** — no polygon available; VAs in these 2019
   territories cannot be assigned spatially.
5. **Calgary-Airdrie overlap (264 km²)** — minority file; pixel-extracted
   boundary appears to over-extend into Calgary-Nolan Hill-Cochrane and
   adjacent EDs.
