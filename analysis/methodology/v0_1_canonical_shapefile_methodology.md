---
title: Derived boundary construction — methodology for §6.8
section: 6.8
type: methodology
version: 0.1
date: 2026-04-23
---

# §6.8 Derived boundary construction

## 6.8.1 Problem statement

Elections Alberta had not published official digital boundary files for the 2026
proposed electoral districts at the time of this analysis. The commission's
report contains printed cartographic maps at roughly 1:1,000,000 scale for the
full province and 1:200,000 for Calgary and Edmonton. No machine-readable polygon
data accompanied these maps.

Without official shapefiles, spatial analysis of the 2026 proposals depends on
derived approximations. This section documents the construction of the canonical
derived shapefile set used in all spatial tests (Phase 4C and the parametric
boundary sensitivity analysis).

The objective was to produce the most accurate approximation achievable from
available public data while maintaining explicit, auditable provenance for every
district boundary.

## 6.8.2 Source hierarchy

Four source types are available for constructing 2026 district boundaries:

**v7 pixel-extracted polygons.** A prior phase of this audit applied flood-fill
pixel extraction to the commission's cartographic maps. This produced boundary
polygons for 67 of 89 majority and 84 of 89 minority districts. Where pixel
extraction succeeded, the resulting polygon is treated as a direct measurement of
the commission's intended boundary, subject to the resolution limitations of the
printed map (approximately ±500m at 1:200,000 scale; ±5,000m at 1:1,000,000
scale).

**2019 parent polygons.** Elections Alberta publishes official shapefiles for
the 2019 boundaries (the districts currently in force). The commission's report
includes a district-to-district crosswalk mapping each 2026 district to one or
more 2019 predecessors. Where a 2026 district is either a direct rename of a
2019 district (territory largely unchanged) or occupies a well-defined subset of
a 2019 parent, the 2019 polygon serves as a documented approximation.

**Population-calibrated parametric sweep.** Four majority districts required a
novel approach: Airdrie-West and Cochrane-Springbank were both carved from the
single 2019 district of Airdrie-Cochrane, and High River–Vulcan–Siksika and
Okotoks–Diamond Valley were both carved from the single district of Highwood. In
both cases, the commission published population targets for each 2026 district,
allowing the boundary position to be calibrated against published data.

**OSM municipal polygons.** As a last resort for districts where no other source
was usable, OpenStreetMap municipal boundary polygons were used to construct
approximate territories. No majority districts reached this fallback in the final
canonical file; it was considered but superseded by the parametric sweep.

## 6.8.3 Tier classification

Every district in the canonical file carries a `canon_tier` label indicating
confidence in the boundary approximation.

| Tier | Meaning | Error estimate | Count (maj) | Count (min) |
|---|---|---|---|---|
| A | v7 pixel-extracted, city-scale or overview map | ±500m – ±5km | 57 | 65 |
| B | v7 pixel-extracted, matched against OSM refinement | ±250m | 0 | 2 |
| C-pixel | v6 pixel-extracted (prior version, validated) | ±500m | 6 | 3 |
| C-sweep | Population-calibrated parametric sweep | ±2–5km | 4 | 0 |
| C-2019-direct | 2019 territory-equivalent rename | ±0km (same territory) | 16 | 1 |
| C-2019-blend | 2019 parent over-covers 2026 territory | ±5–30km | 2 | 3 |
| C-null | Unresolvable (no v7, no 2019 match) | n/a | 4 | 0 |

Tiers A, B, and C-pixel together cover 63 of 89 majority districts (71%) and
70 of 89 minority districts (79%). The remaining majority districts are all in
the C-series and carry explicit documentation of their approximation type and
error direction.

## 6.8.4 Population-calibrated parametric sweep

### Motivation

Four majority districts share parent polygons: the Airdrie-Cochrane 2019
boundary (754 km²) contained both Airdrie-West and Cochrane-Springbank, and
the Highwood 2019 boundary (1,343 km²) contained both High River–Vulcan–Siksika
and Okotoks–Diamond Valley. Without a boundary between the two 2026 districts
within each parent, any spatial assignment algorithm would produce centroid
ambiguity: a Voting Area centroid inside Airdrie-Cochrane could be validly
assigned to either 2026 district.

The commission's published population targets resolve this ambiguity: they
constrain where the boundary must fall, because the vote (population) proxy is
observable at Voting Area granularity.

### Algorithm

For each overlap pair, the algorithm operates as follows:

1. **Extract the Voting Area subset.** All VA polygons whose centroids fall inside
   the parent 2019 polygon are extracted as the candidate population.

2. **Define the split line family.** A split line is parameterised by two values:
   angle θ ∈ {0°, 15°, 30°, 45°, 60°, 75°, 90°, 105°, 120°, 135°, 150°, 165°}
   and position t ∈ [0.15, 0.85] (fraction of the bounding-box extent along the
   perpendicular axis). The full search space is 12 × 50 = 600 candidate lines.

3. **Score each candidate.** For each candidate split line, the VA set is
   partitioned into two subsets based on which side each VA centroid falls.
   The population proxy for each subset is the Election Day vote total for
   that VA. The score is:

       score = |achieved_ratio − target_ratio|

   where `target_ratio = pop(A) / (pop(A) + pop(B))` from the commission's
   published data and `achieved_ratio` is the Election Day vote fraction for the
   subset designated as district A.

4. **Select the best-fit split.** The 600-candidate sweep selects the line with
   the minimum score. If the minimum score exceeds 0.10 (10 percentage points),
   the result is flagged as low-confidence.

5. **Compute the sensitivity envelope.** All candidate splits within ±5
   percentage points of the target ratio are retained. The envelope reports the
   number of qualifying splits, the range of achieved ratios, and the range of
   VA-vote totals that result from the full envelope. This envelope characterises
   how much the B1–B6 metrics would move if the commission's actual boundary
   differs from the best-fit line.

### Results

**Airdrie-Cochrane → Airdrie-West / Cochrane-Springbank**

Commission population targets: Airdrie-West 48,145 (46.0%) /
Cochrane-Springbank 56,487 (54.0%). Total parent: 104,632.

- VA set: 82 Voting Areas
- Best-fit: angle 75°, position 0.36
- Achieved ratio: 0.462 (target: 0.460; residual: 0.2pp)
- Sensitivity envelope: 7 splits within ±5pp; ratio range 0.435–0.500
- Boundary orientation: NE-SW, consistent with Airdrie being NE of the split
  axis and Cochrane/Springbank to the NW

**Highwood → High River–Vulcan–Siksika / Okotoks–Diamond Valley**

Commission population targets: High River–Vulcan–Siksika 53,351 (49.1%) /
Okotoks–Diamond Valley 55,284 (50.9%). Total parent: 108,635.

- VA set: 71 Voting Areas
- Town-cluster approach attempted first (classify each VA by nearest named town);
  rejected — achieved ratio 0.681 vs target 0.491, too far from target
- Sweep best-fit: angle 165°, position 0.48
- Achieved ratio: 0.495 (target: 0.491; residual: 0.4pp)
- Sensitivity envelope: 2 splits within ±5pp; ratio range 0.450–0.526
- Boundary orientation: nearly E-W with slight tilt, separating the
  Okotoks/Diamond Valley cluster (north) from High River/Vulcan/Siksika (south)

Both sweeps achieve residuals below 0.5pp, which is within the uncertainty of
using Election Day votes as a population proxy.

### Validity of the vote-count proxy

The sweep uses Election Day VA vote totals as a proxy for residential population.
This is valid to the extent that Election Day voter turnout is uniform within
each parent polygon. If, for example, urban Airdrie voters turned out at a
substantially higher rate than rural voters in the Cochrane portion, the vote-
count ratio would overstate the Airdrie fraction of the parent's population, and
the calibrated split line would be drawn too far into Airdrie's territory.

**Turnout check (2023 Alberta general election).** To test this assumption,
the 2023 Statement of Vote was used to compute Election Day turnout by ED class:

| Class | n | Mean turnout | Std dev |
|---|---|---|---|
| Calgary core | 26 | 0.620 | 0.066 |
| Edmonton core | 20 | 0.574 | 0.057 |
| Urban (Cgy + Edm combined) | 46 | 0.597 | 0.065 |
| Rural (pure rural EDs) | 27 | 0.600 | 0.060 |
| Turnout ratio (urban/rural) | | **0.9949** | |

The urban-rural turnout differential in the 2023 Alberta election is 0.3pp
(urban slightly lower). This is negligible. At a population weight of p = 0.85,
the corresponding vote-fraction is:

    vote_frac = (p × t_u) / (p × t_u + (1−p) × t_r)
              = (0.85 × 0.597) / (0.85 × 0.597 + 0.15 × 0.600)
              = 0.8494

The difference between the population weight (0.850) and the vote-fraction
(0.849) is 0.1pp. Alberta's near-uniform turnout means the VA vote count is a
reliable proxy for population distribution, and the parametric sweep's
calibration against commission population targets is not materially distorted
by differential turnout.

**Province-wide consistency.** Alberta's 2023 province-wide turnout was 60.4%.
By class: Calgary 62.0%, Edmonton 57.4%, rest of province 60.5% (weighted
average of 41 EDs ranging from 42% in Fort McMurray–Wood Buffalo to 70% in
Sherwood Park). The absence of a consistent urban-direction bias in turnout
is consistent with prior Alberta elections: the 2019 election (province-wide
71.2%) also showed no systematic urban-rural gap, though at a higher overall
level driven by the NDP-UCP competitive dynamic.

This finding does not mean turnout is constant across EDs. The range within
the Calgary urban class alone is 0.452 (Calgary-East) to 0.713 (Calgary-Varsity)
— a spread of 26pp. The relevant question for the parametric sweep is whether
this variation has a systematic geographic pattern within the small 2019 parent
polygons (Airdrie-Cochrane 754 km², Highwood 1,343 km²). Within those compact,
homogeneous parent territories, there is no reason to expect a large systematic
bias in the intra-parent turnout distribution.

### Urban weight in v0.2 hybrid ED estimation

The v0.2 packing-cracking script models hybrid EDs (those that combine urban
core vote shares with rural baseline vote shares) using a blended estimate:

    hybrid_estimate = w × urban_share + (1−w) × rural_baseline

The weight w (URBAN_WEIGHT_DEFAULT) was updated from 0.70 to 0.85. This value
is derived from the commission's own population data: the population-weighted
average of the urban fraction across all hybrid EDs is 0.876 for the majority
map and 0.830 for the minority map. The flat value 0.85 falls between these and
is the best single-parameter estimate available without per-ED turnout data at
VA resolution.

Given Alberta's near-uniform turnout (urban/rural ratio = 0.9949), the
population-based weight 0.85 is equivalent to a vote-weighted fraction of 0.849.
Sensitivity analysis across the range [0.60, 0.70, 0.80, 0.85, 0.90] shows that
the qualitative finding (minority EG more negative than majority) is consistent
across the full range. The magnitude of the asymmetry increases monotonically
with w, from -0.3pp at w=0.60 to -1.7pp at w=0.90, with -1.42pp at the
preferred w=0.85.

## 6.8.5 Post-sweep validation

After constructing the canonical files, two geometric checks confirm that the
overlap-pair resolution succeeded:

1. Zero null geometries in the canonical file (both majority and minority).
2. All six pairwise polygon intersections among the four sweep-resolved districts
   (Airdrie-West, Cochrane-Springbank, High River–Vulcan–Siksika,
   Okotoks–Diamond Valley) measure 0.00 km², confirming the split is clean.

The full build log, including sweep parameters, sensitivity envelopes, and all
tier assignments for all 89 districts, is in
`analysis/methodology/v0_1_canonical_shapefile_log.md`.

## 6.8.6 Comparison to alternative approaches

**Geometric midpoint.** Using the bounding-box midpoint of the parent polygon
as the split line is simple but ignores population distribution. For the Highwood
parent (an elongated N-S irregular polygon), the midpoint would place the
boundary roughly at the geometric centre, which does not correspond to the
population distribution of the parent territory.

**OSM municipal boundary union.** Constructing district boundaries from
OpenStreetMap municipal polygons is straightforward for named municipalities but
fails at rural fringe areas. Sturgeon County, for example, covers 2,380 km² —
far larger than the territory of St. Albert–Sturgeon warrants — and using the
full county polygon would substantially over-cover the intended district.

**No split (shared parent polygon).** Using the parent polygon for both 2026
districts produces centroid ambiguity: a VA centroid inside the parent can be
assigned to either district, which is arbitrary. The parametric sweep eliminates
this ambiguity by committing to a specific, calibrated boundary.

The parametric sweep approach is preferred because it uses the commission's own
published population targets as the calibration constraint. The derived boundary
is consistent with the commission's stated population allocation, even if the
exact spatial path of the boundary cannot be verified without official shapefiles.

## 6.8.7 Known limitations

1. **C-sweep tier error bound.** The four sweep-resolved districts are
   road-snapped: the best-fit parametric split line is snapped to the nearest
   OSM road within a 5 km buffer (Airdrie-Cochrane: road at 720 m;
   Highwood: road at 475 m). This reduces the boundary error from the
   parametric-only estimate of ±5–10 km to approximately ±1–2 km, consistent
   with the precision of OSM rural road mapping. The sensitivity envelope
   reports B1–B6 across all plausible splits (within ±5pp of target ratio).
   Results reported for these four districts should be read with this error
   band in mind.

2. **C-2019-blend over-coverage.** Two majority and three minority districts use
   a 2019 parent polygon that over-covers the 2026 territory. Spatial assignment
   of VAs to these districts may include VAs that actually belong to adjacent
   districts. This error is documented per district in the canonical file's
   `canon_note` field.

3. **C-null districts.** Four majority districts could not be resolved from
   available sources. These districts contribute zero VAs in Phase 4C and are
   excluded from spatial tests.

4. **No official verification.** This file is a derived approximation. When
   Elections Alberta publishes official 2026 shapefiles, the spatial tests should
   be re-run against those files. The v0.2 proportional-estimate results do not
   depend on the derived shapefiles and remain unaffected.

## 6.8.8 File outputs

| File | Contents |
|---|---|
| `data/v0_1_canonical_majority_2026_eds.gpkg` | 89 majority district polygons, EPSG:3401, with tier metadata |
| `data/v0_1_canonical_minority_2026_eds.gpkg` | 89 minority district polygons, EPSG:3401, with tier metadata |
| `analysis/methodology/v0_1_canonical_shapefile_log.md` | Full build log with per-district provenance |
| `analysis/scripts/build_canonical_shapefiles.py` | Reproducible construction script |
