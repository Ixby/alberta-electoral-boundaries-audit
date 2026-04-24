# v0_1 Shape refinement v2 (Track Y-prime)

## Purpose

Second pass over Track Y's shape-refinement output. The PO flagged two concerns
with Track Y's v1 result:

1. The OSM snap ran against roads only, but the commission plainly drew several
   boundary segments along rivers, not roads. River-boundary segments in
   Track Y v1 are visibly wrong — they zigzag between residential streets
   because no road parallels the river closely enough.
2. The v1 writeup reported compactness movement but did not test whether any
   of the reported geometric shifts actually changed voter assignment. A
   boundary that moves 500 m through open prairie has no voter-assignment
   impact; a boundary that moves 100 m through dense suburbia can flip
   dozens of VAs. The audit should prioritise refinement effort by
   voter-assignment impact, not by geometric magnitude.

This writeup reports what Track Y-prime did and what it found.

## Phase 1 — commission-PNG transcription

Each of the five Tier B minority EDs was transcribed segment-by-segment from
the 600-DPI commission PNG (`maps/hires/v0_1_minority_p35[9-60-61-62]_*.png`).
Full transcription lives at `analysis/methodology/v0_1_boundary_transcription.md`. Summary:

| ED | Water-body segment | Dominant feature class(es) | Priority |
|---|---|---|---|
| Calgary-De Winton | None | road + admin (township) | Low |
| Calgary-South | Bow River (east protrusion) | road + **river** + admin | **High** |
| Edmonton-Windermere | North Saskatchewan River (east) | road + **river** + admin | **High** |
| Lethbridge-Little Bow | Oldman River (north) | **river** + admin | **High** |
| Wetaskawin-Ponoka-Maskwacis | Battle River (short, south) | admin + road + river | Low |

Three of the five Tier B EDs have material river-boundary segments. These
were the re-snap priority.

### Triple-check

Transcription was cross-checked three ways:

1. **Commission PNG visual inspection** at 600 DPI — identified blue river
   symbols and red ED boundary overlay.
2. **2019 ED shapefile cross-reference** — the Bow River, North Saskatchewan,
   and Oldman already serve as boundaries between adjacent 2019 EDs in the
   `alberta_2019_eds/` shapefile, so OSM river tagging is pre-validated.
3. **OSM tag scan** of `waterway=river` features within each ED's bbox —
   confirmed each named river is tagged and returned multi-kilometre line
   geometries from Overpass (Bow River 541 river features, North Saskatchewan
   758, Oldman 5846, Battle 20465 within padded bounding boxes).

## Phase 2 — feature-class-aware re-snap

Extended Track Y's road-only pipeline to fetch four feature classes per ED:

- `highway=motorway|trunk|primary|secondary|tertiary` (road)
- `waterway=river|stream` + `natural=water` (river / lake)
- `railway=rail|light_rail` (rail)
- `boundary=administrative` (admin / municipal / jurisdictional)

For each sample point on the polygon boundary (200 m spacing, 500 m buffer),
the snap picks the **closest feature across all four classes**, with a
priority order biased by the Phase 1 transcription. High-priority (water)
EDs use priority `[river, admin, road, rail]`; low-priority EDs use
`[admin, road, river, rail]`. The priority only matters when two features
are within buffer at similar distance; otherwise the literal nearest feature
wins.

**Per-ED snap class distribution (v2 pass 1, 500 m buffer, 200 m spacing):**

| ED | River hits | Admin hits | Road hits | Rail hits | None | Total |
|---|---:|---:|---:|---:|---:|---:|
| Calgary-De Winton | 164 | 940 | 473 | 9 | 122 | 1708 |
| Calgary-South | 53 | 188 | 52 | 0 | 0 | 293 |
| Edmonton-Windermere | 243 | 124 | 58 | 0 | 0 | 425 |
| Lethbridge-Little Bow | 1443 | 1236 | 93 | 4 | 454 | 3230 |
| Wetaskawin-Ponoka-Maskwacis | 698 | 710 | 781 | 42 | 406 | 2637 |

Interpretation:
- Edmonton-Windermere lands 57% of samples on river — the north-saskatchewan
  east-bank segment is doing exactly what the transcription required.
- Lethbridge-Little Bow lands 45% of samples on river — matches the Oldman
  River north boundary.
- Calgary-South lands 18% on river — lower ratio because the river segment
  is only one of four edges (east exurban limb); the other three edges are
  road or admin.
- Calgary-De Winton lands 10% on river — expected, since Phase 1 said the
  ED has no water-body boundary. The 164 river hits are spurious (a nearby
  creek was closer than the township line at a handful of samples).
- Wetaskawin-Ponoka-Maskwacis lands 26% on river — consistent with the
  partial Battle River segment plus lake-edge fragments.

Outputs:
- `data/v0_1_refined_v2_majority_2026_eds.gpkg` (pass-through; majority is
  all Tier A).
- `data/v0_1_refined_v2_minority_2026_eds.gpkg` (five Tier B rows re-snapped;
  all other rows carried over from Track Y v1).

## Phase 3 — voter-assignment impact assessment

For each Tier B boundary the difference between Track Y v1 (road-only snap)
and v2 (feature-class snap) was measured as the symmetric-difference region
between the two polygons. VAs whose centroid falls inside the symmetric-
difference region are "boundary-sensitive": their ED assignment would flip
depending on which boundary version is used. 2023 vote totals (NDP + UCP +
other) for those VAs were summed.

**Classification rule:**
- Any single boundary-sensitive VA with > 50 votes OR aggregate > 500 votes
  across all sensitive VAs → `refinement-significant` (further effort
  warranted).
- All sensitive VAs ≤ 50 votes AND aggregate ≤ 500 → `refinement-negligible`
  (**orange-accepted**).
- Commission PNG ambiguous and no clear feature match → `boundary-unresolvable`
  (red flag).

### Results

| ED | v1-v2 shift (m) | Sensitive VAs | Sensitive votes | Classification |
|---|---:|---:|---:|---|
| Calgary-De Winton | 13.7 | 1 | 216.6 | **refinement-significant** |
| Calgary-South | 36.9 | 1 | 216.6 | **refinement-significant** |
| Edmonton-Windermere | 54.9 | 3 | 795.8 | **refinement-significant** |
| Lethbridge-Little Bow | 59.2 | 0 | 0 | refinement-negligible (orange) |
| Wetaskawin-Ponoka-Maskwacis | 30.5 | 0 | 0 | refinement-negligible (orange) |

**Total boundary-sensitive votes across all v1→v2 transitions: 1,229.**

Full CSV: `data/v0_1_boundary_refinement_impact.csv`.

**Important observation.** Calgary-De Winton and Calgary-South each list the
same 1 sensitive VA with 216.6 votes — these two EDs share a boundary
segment, so the same VA is sensitive to both. The actual unique
boundary-sensitive VAs across all five Tier B EDs is 4, with 1,012.4 total
votes (216.6 Calgary-DW ∩ Calgary-South shared VA + 795.8 Edmonton-Windermere
river-bank VAs).

## Phase 4 — iterative refinement log

Only the three refinement-significant EDs were iterated.

### Calgary-De Winton (2 passes)

- Pass 1 (baseline): buffer 500 m, spacing 200 m → 11.1 m mean shift, 164
  spurious river hits.
- Pass 2: buffer 300 m, spacing 150 m (tighter) → 8.7 m mean shift. Still
  217 spurious river hits; the narrower buffer did not eliminate them. No
  pass 3 needed — the ED is admin-dominated and the 1 sensitive VA is
  on the road/admin-only edge, not the spurious river corner.
- **Result after pass 2: refinement-significant remains — but the residual
  216.6-vote sensitive VA is at a road-vs-admin boundary point where the
  commission's actual choice is genuinely ambiguous without the shapefile.**

### Calgary-South (3 passes)

- Pass 1: 500 m / 200 m → 11.2 m mean shift, 53 river hits (18%).
- Pass 2: 300 m / 150 m → 9.7 m mean shift, 59 river hits (15%).
- Pass 3: 400 m / 100 m, river-forced priority → 11.4 m mean shift, 92 river
  hits (16%). The extra river hits come from denser sampling picking up more
  river-proximal points; it did not change the VA-sensitivity outcome
  because the 216-vote sensitive VA is located on the shared Calgary-DW /
  Calgary-South boundary segment rather than the river segment.
- **Result after pass 3: refinement-significant remains on the shared-boundary
  VA, but the river segment is well-resolved.**

### Edmonton-Windermere (3 passes)

- Pass 1: 500 m / 200 m → 7.1 m mean shift, 243 river hits (57%).
- Pass 2: 300 m / 150 m → 7.3 m mean shift, 319 river hits (59%).
- Pass 3: 400 m / 100 m, river-forced → 7.2 m mean shift, 475 river hits
  (57%). The finer spacing preserves the river-dominance.
- **Result after pass 3: refinement-significant remains; 3 VAs totalling
  795.8 votes sit in the symmetric-difference region. These VAs are
  physically near the river-bank, where the commission's exact line
  (river-centreline vs left-bank vs right-bank) is unresolvable from the PNG
  alone.**

### Why passes 2–3 did not flip refinement-significant to orange

All three refinement-significant cases have a residual disagreement that is
**not** between two snap strategies — it is between the snap result (any
version) and the commission's actual chosen polyline. The v1 vs v2 difference
is a proxy for "Track Y's snap precision"; the boundary-sensitive VAs in that
difference are a lower bound on the VAs that would differ between the snap
and the real commission shapefile. Iterating snap parameters does not shrink
this — it just exchanges one approximation for another. The residual
materiality is a function of the intrinsic ambiguity, not of insufficient
iteration.

**Conclusion for Phase 4:** three passes is sufficient. No pass 4/5 would
help without the commission shapefile.

## Phase 5 — orange-tier visualization

Re-rendered the 10 priority verification panels with a three-tier colour
convention:

- **Green (solid, 2.2 px):** Tier A (exact 2019 inheritance, high fidelity).
- **Orange (solid, 2.2 px):** Tier B, refinement-negligible — accepted as
  "good enough for voter assignment".
- **Red (dashed, 2.2 px):** Tier B, refinement-significant — residual
  disagreement affects voter assignment, awaits commission shapefile.

Colour-blind fallback: the dash pattern distinguishes red from orange even
for protanopic / deuteranopic readers.

Panels at `maps/verification/v0_2_<majority|minority>_<ed-slug>.png` plus a
2×5 grid at `maps/verification/v0_2_priority_grid.png`.

### Legend contents

| Glyph | Meaning |
|---|---|
| Green solid | Tier A — 2019 inheritance, PP point score |
| Orange solid | Tier B — refinement-negligible, orange-accepted |
| Red dashed | Tier B — refinement-significant, awaits shapefile |
| Grey dotted | v1 (Track Y road-only) boundary, for reference |

## Final compactness scores with three-tier confidence

Full table: `data/v0_1_compactness_scores_refined.csv` (carried over from
Track Y v1) + a v2 column for the five snapped Tier B rows.

### Tier B comparison, v1 vs v2

| ED | v1 PP | v2 PP | v1 Reock | v2 Reock | Tier |
|---|---:|---:|---:|---:|---|
| Calgary-De Winton | 0.381 | 0.387 | 0.292 | 0.291 | red (significant) |
| Calgary-South | 0.217 | 0.240 | 0.210 | 0.214 | red (significant) |
| Edmonton-Windermere | 0.195 | 0.230 | 0.298 | 0.304 | red (significant) |
| Lethbridge-Little Bow | 0.465 | 0.452 | 0.575 | 0.574 | **orange** |
| Wetaskawin-Ponoka-Maskwacis | 0.417 | 0.406 | 0.447 | 0.448 | **orange** |

Edmonton-Windermere's PP improvement (0.195 → 0.230, +18%) is the biggest
visible win: removing spurious road-snap zigzags along the North Saskatchewan
bank straightened the east edge to follow the river's natural meander only.

### Three-tier confidence classification, final roll-up

- **Green (Tier A, high confidence):** all 57 majority + 60 minority =
  117 EDs. PP point score is the 2019 geometry's score, CI ±0.03 nominal.
- **Orange (Tier B, accepted for voter assignment):** 2 minority EDs
  (Lethbridge-Little Bow, Wetaskawin-Ponoka-Maskwacis). PP CI is the v1–v2
  range (≤0.02 PP width), voter-assignment impact zero.
- **Red (Tier B, significant residual, awaits shapefile):** 3 minority EDs
  (Calgary-De Winton, Calgary-South, Edmonton-Windermere). PP CI is the
  v1–v2 range (up to 0.035 PP width), voter-assignment impact 4 unique
  sensitive VAs with 1,012 total 2023 votes.

Total: 117 + 2 + 3 = 122 rows classified; 5 remaining unaccounted-for rows
in the minority shapefile (rows that are Tier A but that Track X may have
approximated with non-trivial uncertainty; these inherit the ±0.03 nominal
widening and are implicitly green).

## Proposed §6.7 revision for the academic report

> **§6.7 Geometry approximation, refinement, and orange-tier acceptance.** The
> 2026 electoral division shapes used in this audit are not the commission's
> published shapefiles, which were not available to the audit team. They
> are reconstructions built from the 2019 ED geometry as a seed and the
> Appendix A / Appendix E textual descriptions as a name crosswalk. For the
> subset of 2026 divisions that merge pieces of two or more 2019 parents
> (tagged Tier B), an OpenStreetMap feature-snapping procedure was applied
> in two rounds:
>
> - **Round 1 (Track Y, 2026-04-21).** Snap-to-nearest-road with priority
>   motorway → trunk → primary → secondary → tertiary, 500 m buffer, 200 m
>   spacing.
> - **Round 2 (Track Y-prime, 2026-04-22).** Transcribed each commission
>   PNG for the five Tier B EDs; found three have water-body boundary
>   segments (Bow River for Calgary-South, North Saskatchewan River for
>   Edmonton-Windermere, Oldman River for Lethbridge-Little Bow). Re-snapped
>   those three plus two admin-dominated Tier B EDs using four OSM feature
>   classes simultaneously (road, waterway, railway, administrative) with
>   transcription-derived priority ordering.
>
> The post-Round 2 geometry is evaluated for **voter-assignment impact**:
> VAs whose centroid falls in the v1–v2 symmetric-difference region are
> boundary-sensitive, and their 2023 vote totals are summed. Four unique
> VAs totalling 1,012 votes are sensitive to the v1→v2 transition across
> the three water-body Tier B EDs. Two of the five Tier B EDs have zero
> boundary-sensitive VAs and are classified **orange-accepted** (geometric
> residual exists but does not affect voter assignment). The remaining three
> are flagged red pending release of the commission's shapefile.
>
> Compactness scores (Polsby-Popper, Reock) reported in §5 are accompanied
> by the [v1, v2] range as the CI for Tier B rows, and ±0.03 nominal for
> Tier A rows. Any §5 threshold test that depends on a Tier B compactness
> being above or below a nominal value should be read against this CI and
> the corresponding tier label (green / orange / red).

## Per-boundary classification list

### Refinement-negligible (orange-accepted)
- **Lethbridge-Little Bow** — north edge follows Oldman River (v2 captures
  this correctly); south / east / west follow township lines (v2 admin-snap
  captures these). 0 boundary-sensitive VAs.
- **Wetaskawin-Ponoka-Maskwacis** — north / east / west follow township
  lines; south partially follows Hwy 53 and Battle River. 0 boundary-sensitive
  VAs. Snap disagreements are in rural / reserve territory with no VAs at
  stake.

### Refinement-significant (continued refinement warranted)
- **Calgary-De Winton** — 1 boundary-sensitive VA (216.6 votes). Ambiguity
  is on the shared boundary with Calgary-South, not on a river segment.
- **Calgary-South** — 1 boundary-sensitive VA (216.6 votes, same VA as
  Calgary-DW). Ambiguity is on the DW-South shared boundary, east-protrusion
  river edge is well-resolved (53–92 river hits across three passes).
- **Edmonton-Windermere** — 3 boundary-sensitive VAs (795.8 votes). Residual
  disagreement is on the bank-centreline choice along the North Saskatchewan;
  the river itself is correctly identified as the boundary feature, but
  which side of the river is in which ED cannot be resolved without the
  commission shapefile.

### Boundary-unresolvable (red flag — needs actual shapefile)
- None of the five Tier B EDs hits this. The commission PNG is legible
  enough for feature-class identification in all five cases. The three
  refinement-significant EDs have an identifiable feature (river + admin)
  and a known impact (4 unique VAs, 1,012 votes) — they are *refinable once
  the shapefile arrives*, not categorically unresolvable.

## Reproducibility

Pipeline: `analysis/scripts/v0_1_shape_refinement_v2.py`.

Dependencies (same as Track Y v1 plus no new additions):
- `osmnx ≥ 2.0` with `features_from_bbox` helper.
- `geopandas`, `shapely ≥ 2.0`, `pyproj`, `numpy`, `pandas`, `matplotlib`.

Network access to the Overpass API required. Cache lives in
`cache/` under the OSMnx default path. Typical run time on a developer
laptop: 2-3 minutes (cached) / 8-10 minutes (cold Overpass).

Phases 2b / 3b / 4b / 5b can be run independently: pass the phases to skip
as CLI args (e.g. `python analysis/scripts/v0_1_shape_refinement_v2.py phase4 phase5`
to run only phase 2b and 3b).

## Summary: what Track Y-prime changed

- **Transcribed** each Tier B ED boundary from the commission PNG
  (`analysis/methodology/v0_1_boundary_transcription.md`).
- **Re-snapped** 3 of 5 Tier B EDs that have water-body segments using
  multi-feature OSM priority queries; 2 of 5 admin-dominated EDs also
  re-snapped for consistency.
- **Introduced orange-tier acceptance:** 2 of 5 Tier B EDs are classified
  refinement-negligible (0 boundary-sensitive VAs each).
- **Identified** the residual risk: 4 unique VAs, 1,012 total 2023 votes,
  located on river-bank / shared-boundary segments of 3 Tier B EDs in
  Calgary / Edmonton. These are the only boundaries where the commission
  shapefile would materially change the VA-to-ED assignment.
- **Rendered** v0_2 verification panels with three-tier colour convention
  (`maps/verification/v0_2_*.png`).
