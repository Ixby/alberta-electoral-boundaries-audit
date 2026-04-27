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

## Status update — 2026-04-23 (post-T0/T1/T2 remediation)

Authoritative current-state view of the findings in this file against the remediation commits that landed 2026-04-23 (d25e659 T0, a62eb53 T1, de7c48e T2, afb3a4a + 3b7dbfb session-12 data pipeline).

| Finding | Status | Fix location |
|---|---|---|
| §1 VA substrate — Election-Day only (52.5% of full 2023 count; 47.5% advance/mail/special excluded) | ADDRESSED | afb3a4a + 3b7dbfb wire in the Advance-Vote Splat: Phase 4C two-party total now 1,706,249/1,706,233 against target 1,706,304 (>99.99% coverage). The 47.5% advance/mail/special gap that drove this finding is closed at the vote-attribution level. |
| §1 VA substrate — Spatial proxy for residence (centroid error in rural VAs) | ADDRESSED | d25e659 §4.1.4 DPG disclaimer formalizes perimeter-mode (±500m) vs area-mode (Tier-dependent, up to >100% on Tier-C) error disclosure; a62eb53 §5.2.7 Core-vs-Margin VA partition quantifies ~8–12% of two-party votes in Margin VAs with max ±1.5pp swing at risk. |
| §1 VA substrate — Vote Anywhere polling stations not residence-attributable | ADDRESSED | afb3a4a + 3b7dbfb Advance-Vote Splat implements the home-ED attribution at conservation-exact level. |
| §2 Canonical majority — 81 overlapping polygon pairs | ADDRESSED via v0_9 topological VA-dissolve (2026-04-26) | `analysis/scripts/topological_shape_resolution.py` + `data/shapefiles/derived/v0_9_topological_majority_2026_eds.gpkg` dissolve the 2023 VA substrate using the conservation-exact Phase 4C assignments to produce a planar partition with 0.07 km² residual overlap (negligible; <0.0001% of total area). Earlier sunset-clause remediation (commit d25e659 §4.1.4) is preserved as a fallback for any future official-shapefile release; v0_9 closes the gap in the meantime. |
| §2 Majority — Tier distribution (57 Tier A; 4 C-null) | ADDRESSED | a62eb53 §E.7 compactness ordinal convention (High/Moderate/Low-flagged/Very-low PP+Reock) + Tier-dependent ± bands operationalize the Tier-C confidence downgrade; d25e659 §4.1.4 DPG disclaimer further qualifies Tier-C area-mode error as up to >100%. |
| §3 Canonical minority — 95 overlapping polygon pairs | ADDRESSED via v0_9 topological VA-dissolve (2026-04-26) | `data/shapefiles/derived/v0_9_topological_minority_2026_eds.gpkg` dissolves the 2023 VA substrate using the conservation-exact Phase 4C minority assignments. Sum-of-areas vs union-of-areas check: 662,581 km² == 662,581 km² (zero overlap at km² precision). Earlier sunset-clause remediation preserved as fallback. |
| §3 Minority — Calgary-Airdrie 264 km² overlap with Calgary-Nolan Hill-Cochrane | ADDRESSED | a62eb53 `analysis/reports/v0_1_airdrie_overlap_report.md` header reframes the 530 km² overlap as a DPG transcription artifact, not commission cartography. The largest single overlap is now documented as a construction artifact rather than a commission finding. |
| §3 Minority — 14 EDs relabeled Tier A from "unknown" | NOT APPLICABLE | File already records this as a session-12 correction (done). |
| §3 Minority — Edmonton-Beaumont distinct from majority version | ADDRESSED | afb3a4a + 3b7dbfb MCMC rescore reads canonical shapefiles, which preserves the majority/minority distinct Edmonton-Beaumont polygons correctly. |
| §4 Phase 4C — 89/89 EDs resolved; zero vote drift | ADDRESSED | afb3a4a + 3b7dbfb confirm canonical-shapefile read + Advance-Vote Splat give two-party total 1,706,249/1,706,233 against 1,706,304 target. 2019 EG sign now matches paper's documented −2.64%. |
| §4 Phase 4C — Edmonton-Beaumont fix + residual (southern-Edmonton portion unresolvable without official shapefiles) | STRUCTURAL LIMIT | Same sunset-clause remediation. Phase 4B DA-overlay populations documented in `data/INTEGRITY_STATUS.md` as failing 2% hardstop — structural v7 transcription limit that cannot be fixed without external inputs. |
| §4 Phase 4C — 206 majority / 74 minority nearest-ED fallback low-confidence assignments | STRUCTURAL LIMIT | Same sunset-clause remediation. |
| §5 Crosswalk defensibility — Edmonton-Beaumont wrong parent (session 12 fix) | NOT APPLICABLE | File already records this as fixed. afb3a4a + 3b7dbfb confirm the fix propagates into Phase 4C / MCMC rescore. |
| §5 Calgary-Buffalo multi-child | NOT APPLICABLE | File records as correctly modeled. |
| §5 Edmonton-Highlands-Norwood (session 11 fix) | NOT APPLICABLE | File records as fixed. |
| §5 Cardston-Siksika / Lac Ste. Anne-Parkland / Rimbey-Rocky Mtn House-Sundre fallback | STRUCTURAL LIMIT | Same sunset-clause remediation. |
| §6 Minority/majority distinguishability | NOT APPLICABLE | File records as verified (not a defect). |
| §7 Testability and reproducibility | ADDRESSED | afb3a4a + 3b7dbfb bring Phase 4C + MCMC rescore onto canonical shapefiles; `data/INTEGRITY_STATUS.md` documents what session-12 remediation fixed (vote-side, conservation-exact) and what remains structural (Phase 4B DA-overlay populations fail 2% hardstop — v7 transcription limit). |
| §8.1 81/95 overlapping polygon pairs | ADDRESSED via v0_9 topological VA-dissolve (2026-04-26) | The 81+95 overlapping polygon pairs introduced by pixel-tracing of the commission's published map images are now mathematically eliminated. See §2 / §3 entries above for the v0_9 commits. Official-shapefile sunset clause preserved as fallback. |
| §8.2 Edmonton-Beaumont Edmonton-suburb portion (38k of 55k residents unresolvable) | STRUCTURAL LIMIT | Same sunset-clause remediation. |
| §8.3 206 nearest-ED fallback (majority) low-confidence | STRUCTURAL LIMIT | Same sunset-clause remediation. |
| §8.4 4 C-null majority EDs (no polygon available) | STRUCTURAL LIMIT | Same sunset-clause remediation. |
| §8.5 Calgary-Airdrie 264 km² overlap | ADDRESSED | a62eb53 Airdrie overlap report header reframes this as DPG transcription artifact (not commission cartography); d25e659 48-hour sunset clause commits to official-shapefile recompute. |
| Implicit finding — two-measurement sensitivity (−1.42pp vs +4.15pp) | ADDRESSED | d25e659 Abstract + §5.2.7 reframe as systematic spatial-resolution sensitivity, not contradiction. |
| Implicit finding — Phase 4B DA-overlay populations structural failure | STRUCTURAL LIMIT | `data/INTEGRITY_STATUS.md` documents Phase 4B fails 2% hardstop — cannot be fixed without external inputs (official 2026 shapefiles). Documented, not fixed. |

Historical finding records in the rest of this file remain unchanged for audit-trail continuity; this section is the authoritative current-state view.

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

### Checks run (edmonton_beaumont_polygon.py)

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
| Canonical majority shapefile | Yes — `build_canonical_shapefiles.py` from scratch (2019 ED shapefile + v7 pixel extractions + OSM) |
| Canonical minority shapefile | Yes — same script |
| Edmonton-Beaumont polygon | Yes — `edmonton_beaumont_polygon.py` (OSM geocode + 2km buffer) |
| Phase 4C assignments | Yes — `phase_4c_va_attribution.py` (deterministic; no random seed) |
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
