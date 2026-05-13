---
name: Phase 4C vs v0.2 comparison
description: Compares VA-resolution measured results against the v0.2 proportional-estimate (70/30 blend) approach. Documents what Phase 4C resolves, what it cannot, and why the results differ from v0.2.
---

# Phase 4C vs v0.2 gerrymander-metric comparison

## Summary

Phase 4C assigns 4,765 VA polygons to their 2026 EDs using spatial
containment (centroid-in-polygon). It resolves 86 of 89 expected EDs
for both maps, with perfect vote conservation. However, it does NOT
reproduce the v0.2 asymmetry finding, for reasons explained below.

## Results side-by-side

### v0.2 (proportional-estimate, w=0.70 urban blend, full 2023 vote)

| Metric | 2019 | Majority | Minority |
|---|---|---|---|
| Districts | 87 | 89 | 89 |
| Seats NDP/UCP | 38/49 | 38/51 | 37/52 |
| B2 Efficiency gap | -2.64% | -0.85% | -1.36% |
| B3 Mean-median | -2.22pp | -0.18pp | -0.34pp |
| B4 NDP @ 50/50 | 46 | 44 | 42 |
| B6 Declination | -0.0341 | -0.0210 | -0.0150 |
| **Min-Maj asymmetry (EG)** | | | **-0.51pp** |

### v0.2 (proportional-estimate, w=0.85 urban blend, full 2023 vote) — preferred

Urban weight updated from 0.70 to 0.85 to reflect commission population targets
(majority hybrid mean: 0.876; minority hybrid mean: 0.830). Alberta 2023
turnout confirms urban ≈ rural (0.597 vs 0.600), so the population-based weight
is equivalent to a vote-weighted fraction of 0.849 — a 0.1pp difference that
does not materially affect results. See `analysis/methodology/canonical_shapefile_methodology.md`
§6.8.4 for the full derivation.

| Metric | 2019 | Majority | Minority |
|---|---|---|---|
| Districts | 87 | 89 | 89 |
| B2 Efficiency gap (point est.) | -2.64% | -0.40% | -1.81% |
| B2 EG mean (MC, N=2,000) | | -0.33% | -1.57% |
| B2 EG 95% CI | | [-1.97%, +1.49%] | [-3.43%, +0.24%] |
| **Min-Maj asymmetry (point est.)** | | | **-1.41pp** |
| **Min-Maj asymmetry (MC mean)** | | | **-1.23pp** |
| **Min-Maj asymmetry 95% CI** | | | **[-3.04pp, +0.76pp]** |
| Direction consistency | | 59.7% | 94.2% |
| Asymmetry direction consistency | | | **90.5%** |

MC samples: urban_weight ~ Uniform(0.55, 0.85), rural_ndp ~ Uniform(0.26, 0.36),
per-hybrid jitter ~ Uniform(-0.10, +0.10). N=2,000, seed=42.

The direction of the asymmetry (minority map more pro-UCP than majority) holds
in 90.5% of draws. The 95% CI crosses zero (+0.76pp upper bound). Per the
audit's pre-specified reporting discipline: directional claim at 90% confidence,
not 95% significance. CI disclosed in full. Cross-election inconsistency
(direction reverses under 2019 vote inputs) also disclosed.

### Phase 4C v2 — 89/89 resolution (final, session 12)

All 89 EDs fully resolved in both maps after:
- Edmonton-Beaumont crosswalk corrected (Leduc-Beaumont as 2019 parent,
  not Edmonton-South)
- Edmonton-Beaumont canonical polygon rebuilt from OSM City of Beaumont
  + 2km edge buffer (76.6 km²; captures 21 Beaumont-area VAs / 4,621
  Election-Day votes)
- Crosswalk-leak nearest-ED fallback covers 206 majority / 74 minority
  VAs whose 2019 parent ED name is absent from the 2026 reverse map

| Metric | 2019 | Majority | Minority |
|---|---|---|---|
| Districts | 87 | 89 | 89 |
| Seats NDP/UCP | 30/57 | 31/58 | 31/58 |
| B2 Efficiency gap | +2.41% | +1.44% | +1.75% |
| B3 Mean-median | -0.77pp | -0.79pp | -1.79pp |
| B4 NDP @ 50/50 | 47 | 48 | 46 |
| B6 Declination | +0.0270 | +0.0167 | -0.0061 |
| **Min-Maj asymmetry (EG)** | | | **+0.31pp** |

Note: +EG = minority map is *less* pro-UCP than majority on this metric;
B3 and B6 tell the opposite story (minority mean-median -1.79pp vs -0.79pp
and negative declination signal pro-UCP lean). No single-metric conclusion
is warranted from Phase 4C alone.

### Monte Carlo 95% CIs (Phase 4C v2, 2,000 draws)

| Metric | Majority CI | Minority CI |
|---|---|---|
| EG | [-6.03%, +4.51%] | [-3.57%, +5.03%] |
| EG median | +0.16% | +1.50% |
| Mean-median | [-2.58pp, +0.58pp] | [-3.21pp, -0.31pp] |
| NDP @ 50/50 | [44, 50] | [45, 50] |
| Declination | [-0.0552, +0.0543] | [-0.0611, +0.0679] |
| EG negative (pro-UCP) | 48.4% | 23.9% |

Mean-median CI for minority does not cross zero ([-3.21pp, -0.31pp]),
indicating a statistically consistent pro-UCP lean on that metric under
Election-Day vote distribution. All other CIs cross zero.

## Why the results differ

### 1. Different vote populations

The v0.2 script uses full 2023 per-ED vote totals (all ballot types,
two-party total 1,706,304). Phase 4C uses the VA substrate, which
contains only Election Day spatially-assigned votes (two-party total
896,644 — 52.5% of the full count).

Election Day votes skew UCP relative to the full count because NDP
voters use advance/mail/special ballots at a 6pp higher rate (NDP
advance share ~51% vs UCP ~45%). The Phase 4C NDP province-wide share
is 42.60% vs the full-count 44.66%.

This explains the sign flip in EG: the NDP seat count drops from 38 to
30 under the Election Day subset because marginal NDP seats are won on
advance/special votes that aren't in the VA substrate.

### 2. Spatial assignment mostly relabels 2019 EDs

The approximate 2026 shapefiles are Tier A (inherited 2019 geometry) for
57 of 57 majority EDs and 65 of 70 minority EDs. A VA whose centroid
falls inside a Tier A polygon is assigned to the 2026 ED that occupies
the same territory as the parent 2019 ED. This is effectively a rename
operation — the vote totals don't change.

The v0.2 blending rule, by contrast, models how hybrid EDs incorporate
rural votes: a 70% urban-core, 30% rural-baseline blend shifts the NDP
share in every hybrid ED. Since the minority map has 7 Calgary hybrids
(vs majority's 4), the blending produces a larger net shift under the
minority map, which is the source of the -0.51pp asymmetry.

Phase 4C's spatial approach CANNOT reproduce this effect because it
doesn't model the rural-vote absorption. It assigns existing VA votes
to the 2026 ED that contains them, but the rural areas absorbed by the
hybrids have no VA-level data (their polls use different VA polygons
than the urban core).

### 3. Resolution gaps (v2 — 89/89 both maps)

Phase 4C v2 fully resolves all 89 EDs in both maps. The assignment
method breakdown:

| Method | Majority | Minority |
|---|---|---|
| Crosswalk (direct rename / 1:1 reverse map) | 2,781 | 2,609 |
| Spatial (centroid-in-polygon) | 1,765 | 1,723 |
| Candidate (flagged hybrid-adjacent) | 0 | 233 |
| Nearest-ED geographic fallback | 206 | 74 |
| Unresolved (crosswalk_split_default) | 13 | 126 |
| **Total** | **4,765** | **4,765** |

"Unresolved" rows are assigned via crosswalk_split_default (first-listed
2026 target for a multi-child 2019 parent). They are assigned, not
missing — the label reflects medium confidence, not a gap.

The nearest-ED fallback (206 majority, 74 minority) handles VAs whose
2019 parent ED name does not appear in any 2026 crosswalk entry. These
are low-confidence assignments that should be reviewed when official
shapefiles are released.

### 4. Shapefile overlap warning

The canonical derived shapefiles contain overlapping polygons: 81 pairs
in the majority file, 95 in the minority file. Overlaps arise from
C-2019-blend EDs (where the full 2019 parent polygon over-covers the
intended 2026 territory) and from pixel-extraction boundary shifts that
push one polygon into an adjacent ED's area. The largest overlaps:

- Majority: Calgary-Bhullar-McCall x Calgary-Falconridge-Conrich (63 km²),
  Calgary-Acadia x Calgary-East (77 km²)
- Minority: Calgary-Airdrie x Calgary-Nolan Hill-Cochrane (264 km²),
  Calgary-Airdrie x Olds-Three Hills-Didsbury (197 km²)

Phase 4C handles overlaps via the assignment hierarchy: Method 0
(direct-rename override) and Method 3 (crosswalk) take priority over
Method 1 (spatial), so most VAs in overlap zones are assigned by
crosswalk rather than by spatial position. The remaining spatial
assignments in overlap zones carry medium confidence. This is documented
in `edmonton_beaumont_log.md`.

## Conclusion

Phase 4C v2 confirms vote conservation (zero drift) and fully resolves
all 89 EDs in both maps. It provides a measured Election-Day-only
baseline and demonstrates that the VA-level spatial distribution does
not reproduce the v0.2 modeled asymmetry.

The v0.2 finding of -0.51pp minority-majority EG asymmetry is a
modeled effect — it reflects the differential impact of the blending
rule on the two maps' different numbers of hybrid EDs. This is not
wrong; it is a legitimate estimate of what rural absorption does to
the vote profile. But it is an estimate, not a measurement.

To resolve this:

1. **2026 shapefiles** (from Elections Alberta) would allow full spatial
   assignment of all 4,765 VAs to all 89 EDs, eliminating both the
   split-ED gaps and the blending approximation.
2. **Full-vote VA attribution** (Phase 4C Stages 5-7 per the runbook)
   would apportion advance/mobile/special votes by Election Day spatial
   share, bringing the two-party total back to 1,706,304 and making the
   Phase 4C results directly comparable to v0.2.

Neither is blocked by anything other than the shapefile release (Track A).

## File outputs

- `assignment_va_to_2026_assignments.csv` — 4,765 rows, per-VA assignment
- `assignment_2026_synthetic_totals.csv` — per-ED vote totals (both maps)
- `assignment_va_attribution.py` — execution script
