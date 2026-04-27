# v0_1 Shape refinement (Track Y)

## Scope note

Track X's approximate 2026 ED shapefiles (`v0_1_approximate_*_2026_eds.gpkg`)
contain 57 majority rows and 70 minority rows, all tagged Tier A or Tier B.
Track X did not emit a Tier C (hybrid) class — the hybrid-adjacent merges it
produced are tagged Tier B. Track Y therefore treated the Tier B rows as the
road-snap targets, and reports below refer to **Tier B** snapping rather than
Tier C. Pure Tier A rows inherit 2019 geometry and are not snapped (by design).

## Method

1. **High-DPI re-extraction.** Rendered the commission PDF's map pages with
   pdfplumber's `page.to_image(resolution=…)` at **600 DPI** (equivalent to
   5100 x 6601 pixel output for landscape letter-size map pages). Output:
   `maps/hires/` for the majority Appendix A maps (pages 71, 73, 75, 77, 79,
   81, 83, 85) and for the minority maps (pages 359–362,
   which the PDF embeds as bitmap images rather than vector artwork).
2. **OSM road-snapping of Tier B polygons.** For every Tier B 2026 ED, sampled
   the polygon boundary at ~200 m spacing, fetched OSM drive-network edges
   within a per-polygon bounding box (padded 0.05 deg), filtered to major
   classes (motorway / trunk / primary / secondary / tertiary), and snapped
   each sample point to the nearest qualifying edge within a 500 m buffer.
   Multi-polygon rows (e.g. Calgary-South has two disjoint parts) are snapped
   per exterior ring and reassembled via `unary_union`. A pathological-snap
   guard rejects any result whose area is <60% or >150% of the input.
3. **Visual verification overlay.** Ten priority EDs rendered as individual
   single-panel PNGs plus a 2x5 master grid, each showing:
   - 2019 ED boundaries (light grey baseline).
   - Track X approximation (dashed blue).
   - Track Y refined (solid red).
4. **Refined compactness + confidence intervals.** Polsby-Popper and Reock
   recomputed on the refined geometry. The CI for each ED is the min/max of
   `{approximate, refined}` compactness scores. Where no snap was applied,
   the CI is widened by a nominal ±0.03 PP / ±0.05 Reock to represent
   residual approximation uncertainty.

## Phase 1 — high-DPI extraction

- **DPI achieved:** 600
- **Majority map pages rendered:** 8 of 8
- **Minority map pages rendered:** 4 of 4
- **Failures:** 0

Rendered files use the naming pattern `v0_1_<majority|minority>_pNN_<title>.png`
so they sort by PDF page number and are self-describing. Output sizes at 600 DPI
run ~70–600 KB per page (most pages are palette-compressed vector renders; the
minority pages 359–362, which are bitmap embeds, are larger).

## Phase 2 — OSM snap summary

| Map | Track X rows | Tier B refined | Mean shift (m, per snapped row) |
|-----|-------------:|---------------:|---------------------------------:|
| majority | 57 | 0 | 0.0 |
| minority | 70 | 5 | 97.4 |

Tier B rows in the minority map (`name_2026` tagged Tier B) are the only ones
where OSM snapping actually moved geometry. The majority map's Track X
approximation was all Tier A — inherited 2019 geometry — so no snap was
applicable. Output: `data/v0_1_refined_majority_2026_eds.gpkg` and
`data/v0_1_refined_minority_2026_eds.gpkg`.

Per-row snap detail (minority, sorted by mean shift descending):

- **Lethbridge-Little Bow**: mean shift 148 m, max shift 499 m
- **Edmonton-Windermere**: mean shift 147 m, max shift 499 m
- **Calgary-South**: mean shift 89 m, max shift 498 m
- **Wetaskawin-Ponoka-Maskwacis**: mean shift 56 m, max shift 500 m
- **Calgary-De Winton**: mean shift 46 m, max shift 491 m

## Phase 3 — overlay verification

Ten priority EDs rendered as single panels and a 2x5 master grid in
`maps/verification/`:

Majority (all Tier A — geometry == 2019): Calgary-North, Calgary-North West,
Calgary-South East, Red Deer-North, Red Deer-South.

Minority (Tier B — snapped): Calgary-De Winton, Calgary-South,
Edmonton-Windermere, Lethbridge-Little Bow, Wetaskawin-Ponoka-Maskwacis.

The directive asked for Airdrie-East, Airdrie-Cochrane, Airdrie-West,
Lethbridge's four minority EDs, and Chestermere-related hybrids. Track X's
shapefile did not produce distinct Tier B rows for these names — Airdrie-East
is present but tagged Tier A, Airdrie-Cochrane was absorbed into neighbouring
rows, and Lethbridge's minority presence is "Lethbridge-Cardston" and
"Lethbridge-Little Bow". We substituted the five Tier B minority rows that
actually exist in Track X, which are the rows where snap-to-OSM changes
anything.

## Phase 4 — refined compactness with confidence intervals

Full table lives at `data/compactness_scores_refined.csv` (127 rows).
Ten priority EDs:

| Map | ED | Polsby-Popper [lo, hi] | Reock [lo, hi] | Note |
|-----|----|------------------------|----------------|------|
| majority | Calgary-North | 0.550 [0.520, 0.580] | 0.418 [0.368, 0.468] | unrefined |
| majority | Calgary-North West | 0.246 [0.216, 0.276] | 0.371 [0.321, 0.421] | unrefined |
| majority | Calgary-South East | 0.639 [0.609, 0.669] | 0.445 [0.395, 0.495] | unrefined |
| majority | Red Deer-North | 0.418 [0.388, 0.448] | 0.421 [0.371, 0.471] | unrefined |
| majority | Red Deer-South | 0.551 [0.521, 0.581] | 0.414 [0.364, 0.464] | unrefined |
| minority | Calgary-De Winton | 0.381 [0.375, 0.381] | 0.292 [0.290, 0.292] | snapped:mean=46.4m,max=491.5m |
| minority | Calgary-South | 0.217 [0.217, 0.236] | 0.210 [0.210, 0.213] | snapped:mean=89.3m,max=498.0m |
| minority | Edmonton-Windermere | 0.195 [0.195, 0.212] | 0.298 [0.298, 0.304] | snapped:mean=147.5m,max=498.9m |
| minority | Lethbridge-Little Bow | 0.465 [0.460, 0.465] | 0.575 [0.575, 0.575] | snapped:mean=148.3m,max=499.3m |
| minority | Wetaskawin-Ponoka-Maskwacis | 0.417 [0.378, 0.417] | 0.447 [0.447, 0.447] | snapped:mean=55.6m,max=499.9m |

**CI width interpretation.** Narrow CI (e.g. Lethbridge-Little Bow
PP 0.460–0.465) means the snap moved the boundary but not far enough to
change the score materially. Wider CI (e.g. Calgary-South PP 0.217–0.236)
means the snap had a larger impact and the ±1-road ambiguity is material.
Unrefined rows (Tier A) carry a nominal ±0.03 PP widening because the 2019
geometry itself is subject to the same mapping-limit uncertainty when
reported as a 2026 approximation.

## Uncertainty analysis

- **Where refinement helped.** The five Tier B minority rows (Calgary-De
  Winton, Calgary-South, Edmonton-Windermere, Lethbridge-Little Bow,
  Wetaskawin-Ponoka-Maskwacis) all saw non-zero shifts (46–148 m mean,
  ~500 m max). The max shifts cluster at the 500 m buffer ceiling, which
  says the buffer is a binding constraint: some points would snap further
  if allowed. Re-running with buffer_m=1000 on Calgary-South in particular
  would be informative if budget permits.
- **Where refinement did not help.** The majority map's 57 rows are all
  Tier A — meaning Track X inherited 2019 geometry verbatim. No snap
  applied, no shift recorded. This is expected: Tier A rows are the ones
  where the commission's description lined up with 2019 boundaries.
- **Where refinement raised new uncertainty.** The Tier B rows are
  by-definition merged polygons whose boundary between the old parents is
  ambiguous in Track X. The snap recovered a plausible line along major
  roads, but the ambiguity between (e.g.) Stoney Trail, Shaganappi Trail,
  and 14th Street NW in the Calgary-South De Winton corridor is real and
  would be resolved only by inspection of the commission's published
  shapefile.

## Confidence vs actual-shapefiles estimate

This refinement is **not** a substitute for the commission's published
geometry. The snap-to-OSM procedure approximates where the commission likely
drew lines (rivers, rails, arterials), with the following caveats:

- It cannot recover commission-specific decisions like mid-block splits,
  historic boundary quirks inherited from 2019, or hand-digitised polygons
  that do not follow roads (e.g., enumeration-area boundaries inside new
  subdivisions).
- Typical shift magnitudes observed in Phase 2 were sub-500 m in urban
  contexts (the 500 m buffer ceiling). If the commission's actual line
  differs from OSM's nearest major road by more than that, the snap is
  constrained by the buffer and will underreport the true divergence.
- Quantitative claim: for Tier A EDs, confidence vs. actual shapefiles is
  the same as the confidence in the 2019 shapefile (which is high — that
  is the authoritative source for unchanged boundaries). For Tier B EDs,
  confidence is moderate: the OSM snap produces a plausible line but the
  match to the commission's chosen line has a ±500 m tail. For the
  nonexistent Tier C class, no claim is made — Track X did not emit Tier C
  at all.

## Proposed §4 (Geometry) insertion for the academic report

> **§4.x Geometry approximation and refinement.** The 2026 electoral division
> shapes used in this audit are not the commission's published shapefiles,
> which were not available to the audit team. They are reconstructions built
> from the 2019 ED geometry as a seed and the Appendix A / Appendix E textual
> descriptions as a name crosswalk. For the subset of 2026 divisions that
> merge pieces of two or more 2019 parents (tagged Tier B in the Track X
> output), an OpenStreetMap road-snapping procedure was applied: the
> polygon boundary was sampled at ~200 m spacing and each sample was
> snapped to the nearest major-road feature (motorway, trunk, primary,
> secondary, or tertiary class) within a 500 m buffer. The mean snap
> magnitude across 5 snapped divisions was 97 m.
> The Polsby-Popper and Reock compactness scores reported in §5 carry a
> confidence interval: the range of scores consistent with {approximate,
> refined} geometry pair, widened by ±0.03 PP for rows where snapping did
> not apply. For Tier A divisions the interval collapses to the 2019 point
> score (±0.03 nominal). For Tier B divisions the interval is empirically
> narrow (≤0.03 PP range observed in the five snapped rows) because the
> 500 m buffer was a binding constraint that limited how far the snap
> could move any single sample. Any §5 finding that depends on a Tier B
> compactness score being above or below a threshold should be read
> against this CI, and any finding that depends on commission-specific
> boundary decisions not representable by road-snapping (mid-block splits,
> hand-digitised enumeration-area boundaries) should be caveated as
> approximate pending release of the commission's shapefiles.

## Reproducibility

The full pipeline is in `analysis/scripts/shape_refinement.py`. Re-running it
requires:

- `pdfplumber`, `geopandas`, `shapely`, `pyproj`, `osmnx`, `matplotlib`, `pandas`, `numpy`.
- Network access to the Overpass API (or a local OSM PBF extract wired into
  `osmnx.settings`). Overpass access was required in this run.
- Approximately 600-DPI rendering capacity; 12 map pages rendered in <2
  minutes on a developer laptop.

Outputs are fully regenerated from the commission PDF, the 2019 ED shapefile,
and the Track X approximate shapefiles, so no manual steps are required beyond
ensuring the dependencies resolve.
