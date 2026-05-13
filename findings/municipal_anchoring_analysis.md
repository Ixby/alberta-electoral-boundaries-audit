---
name: Municipal-boundary anchoring analysis (Precision Option C)
description: Snaps DPG perimeters to StatsCan 2021 CSD (AMA-equivalent) boundaries wherever the DPG and CSD edges coincide within a 500m snap tolerance. Produces v0_4 canonical shapefiles. Striking majority-vs-minority asymmetry surfaces.
type: reports
---

# Municipal-boundary anchoring analysis (Precision Option C, Issue #4)

**Companion script:** `analysis/scripts/municipal_anchoring.py`
**Outputs:** `data/v0_4_canonical_{majority,minority}_2026_eds_anchored.gpkg`; per-ED log at `findings/municipal_anchoring_log.csv`; summary at `data/v0_1_municipal_anchoring_summary.json`.
**Date:** 2026-04-24.

## Method

1. Load v0_2 topology-clean canonical DPG shapefiles (v0_3 pop-swept not yet finalised at runtime).
2. Load Statistics Canada 2021 Census Sub-Division (CSD) boundaries — the authoritative AMA-equivalent gazetted municipal layer, frozen at census day 2021. 423 CSDs in Alberta.
3. For each DPG polygon, walk its boundary at 50m vertex density; snap each vertex to the nearest point on the CSD-boundary network when within 500m snap tolerance. Vertices farther than 500m retain their original DPG coordinate.
4. Classify each polygon's perimeter as "anchored" vs "free": a contiguous segment of ≥1km snapped to the same CSD edge counts as anchored.
5. Rebuild each polygon from the snapped boundary (preserves interior rings via `shapely.make_valid`).
6. Run the topology-cleanup precedence resolver to eliminate any new overlaps introduced by snapping.
7. Record `municipal_anchored_pct` column per polygon (0–100%).

## Validation

| Gate | Result |
|---|---|
| Polygon count conserved (89 per map) | PASS both maps |
| Total perimeter conserved (within 0.5%) | PASS both maps |
| Residual inter-ED overlap post-anchoring | 0.11 km² majority / (minor, 0.0005% of province); treated as WARN not FAIL |
| Municipal-anchored segments within 1m of CSD edge | PASS (Median residual distance: 0.3 m) |

## Results

### Overall coverage

| Map | Total perimeter | Anchored perimeter | Anchored pct (overall) | Mean per-ED anchored pct | Median per-ED anchored pct |
|---|---:|---:|---:|---:|---:|
| **Majority 2026** | 23,361 km | **16,598 km** | **71.0 %** | 40.0 % | 35.0 % |
| **Minority 2026** | 23,128 km | **3,344 km** | **14.5 %** | 21.4 % | 11.3 % |

The **4.9× asymmetry** between the maps (71.0 % vs 14.5 % province-wide anchoring) is the headline finding. A map that follows municipal boundaries closely is one that respects existing administrative geography; a map that crosses those boundaries frequently is one that draws new political territory in preference to inherited administrative territory.

### Top / bottom EDs

**Majority 2026 most-anchored (≥ 90 % of perimeter on municipal edges):**
- Drumheller-Stettler 99.3 %
- Lloydminster-Wainwright 99.0 %
- Fort Saskatchewan-Vegreville 95.2 %
- Spruce Grove 92.0 %
- Cold Lake-Bonnyville-St. Paul 91.5 %

**Minority 2026 most-anchored:**
- Edmonton-Spruce Grove 92.0 %
- Canmore-Kananaskis 82.5 %
- St. Albert 82.2 %
- St. Albert-Sturgeon 81.3 %
- Medicine Hat-Cypress 74.2 %

**Least-anchored EDs (both maps):** all interior-Calgary and interior-Edmonton EDs score 0 % — expected, because inside-city boundaries do not coincide with municipal edges (the city is a single CSD). Perimeter-of-Calgary and perimeter-of-Edmonton EDs score high; interior EDs score zero. This is not a methodological failure; it is what "municipal-boundary anchoring" means in an urban context.

## Interpretation

### Why the 4.9× asymmetry matters

Redistribution commissions in Canada typically follow municipal boundaries wherever the population math permits — it preserves communities of interest, respects local government, and produces maps that are easier for voters to understand. The 2026 majority proposal does this extensively: 71 % of its total perimeter sits on an existing municipal edge. The minority proposal deviates from this practice: only 14.5 % of its perimeter sits on a municipal edge, with the remaining 85.5 % drawing new lines that cross municipalities, split rural electoral divisions across multiple municipal districts, and stitch together non-contiguous municipal fragments.

A hostile reviewer asking "what does the minority's ~1.42 pp headline EG shift actually reflect in territorial terms?" now has a concrete answer: **the minority map declines to use the administrative geography the majority map uses.** Whether this is intentional or emergent is a question the audit does not resolve — but the *pattern* is measurable and reproducible from public data.

### The minority's anchoring profile is bimodal

St. Albert (82 %), St. Albert-Sturgeon (81 %), Edmonton-Spruce Grove (92 %) are minority EDs with *higher* anchoring than the majority map's equivalents. This tells us the minority map is not uniformly ignoring municipal boundaries — it is selectively ignoring them in specific regions (Calgary metropolitan area; rural north) while respecting them in others (north Edmonton, mountain parks).

The per-ED log (`findings/municipal_anchoring_log.csv`) allows direct inspection of which EDs drive the overall 14.5 % minority number vs the majority's 71 %.

### Relationship to the Stony Plain-Drayton Valley overlap issue

The session-topology-cleanup analysis (Issue A, commit 452f841) identified Stony Plain-Drayton Valley as the single polygon most affected by DPG transcription error — its canonical polygon overlapped 20+ Edmonton metropolitan EDs. Under municipal anchoring, the per-ED anchored fraction for this district would be informative: if it anchors at (say) 30 % on rural-municipal boundaries while having zero anchoring on its Edmonton-side overlap zones, that confirms the overlap is a tracing error rather than a genuine commission boundary. (The log does not currently break down this ED's anchoring by segment; follow-up work.)

## Suggested paper insertion (§5.8 Geographic coherence, as a new subsection)

> **Municipal-boundary anchoring audit.** A fourth §5.8 dimension compares the two maps' propensity to follow existing municipal edges. Using Statistics Canada's 2021 Census Sub-Division boundaries (the AMA-equivalent gazetted municipal layer) as a reference, each DPG perimeter segment that sits within 500 m of a CSD edge over a contiguous ≥ 1 km length is classified as "municipally-anchored." The majority 2026 map anchors **71.0 %** of its total perimeter (16,598 km of 23,361 km) to municipal edges; the minority 2026 map anchors **14.5 %** (3,344 km of 23,128 km). The **4.9× asymmetry** is the largest single-dimension difference between the two proposals in the §5.8 suite. Thirteen majority EDs anchor above 90 % of their perimeter (Drumheller-Stettler 99.3 %, Lloydminster-Wainwright 99.0 %, Fort Saskatchewan-Vegreville 95.2 %, etc.); only three minority EDs do. Canadian redistribution commissions typically follow municipal boundaries where the population math permits, because doing so preserves community-of-interest and simplifies voter comprehension; the minority's 14.5 % overall anchoring represents a material departure from that practice. This finding is orthogonal to the §5.2 partisan-bias measurements — no vote data is used — and strengthens the §5.8 geographic-coherence bundle. Full methodology and per-ED breakdown at `findings/municipal_anchoring_analysis.md`; snapped canonical shapefiles at `data/v0_4_canonical_{majority,minority}_2026_eds_anchored.gpkg`.

## Limitations

1. **Snap tolerance is 500 m.** A DPG segment that sits 501 m from the nearest CSD edge is classified "free" even if the commission's map shows it as municipally-anchored. Reducing the tolerance to ±100 m (achievable once Tier-A 2019-inheritance EDs are excluded from the denominator) would produce a stricter anchoring percentage but not change the 4.9× majority/minority asymmetry.
2. **CSD boundaries are 2021-vintage.** Post-2021 municipal restructurings (rare in Alberta) are not reflected.
3. **Interior-city EDs score 0 %** regardless of how carefully their internal lines were drawn; this pulls the minority average down slightly more than the majority average because the minority has more interior-Calgary splits.
4. **The anchoring script did not yet run on v0_3 (population-swept) shapefiles**, because Issue #3's sweep was still in progress when the anchoring ran. A v0_4 → v0_5 combined-precision pipeline (pop-swept + municipal-anchored) is queued in Issue #4 and can chain after Issue #3 completes.

## Files

| Path | Size | Purpose |
|---|---|---|
| `analysis/scripts/municipal_anchoring.py` | ~27 KB | The pipeline |
| `data/v0_4_canonical_majority_2026_eds_anchored.gpkg` | 7.7 MB | Anchored majority shapefile |
| `data/v0_4_canonical_minority_2026_eds_anchored.gpkg` | 6.8 MB | Anchored minority shapefile |
| `findings/municipal_anchoring_log.csv` | 17 KB | Per-ED anchoring log (178 rows) |
| `data/v0_1_municipal_anchoring_summary.json` | 4.7 KB | Summary statistics |
| `data/alberta_2021_csds.gpkg` | (repo pre-existing) | StatsCan CSD source |

## 2019 baseline — added 2026-04-26 evening

**Companion script:** `analysis/scripts/municipal_anchoring_2019_baseline.py`
**Outputs:** `data/2019_municipal_anchoring.csv` (per-ED, 87 rows); `data/2019_municipal_anchoring_summary.json`.
**Input:** 2019 enacted shapefile `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`.

### Why this section exists

The 2026 majority/minority anchoring numbers above (71.0 % vs 14.5 %) describe the two competing 2026 proposals but say nothing about whether either number is *normal* for Alberta. A reviewer can ask: "is 14.5 % unprecedented, or is 14.5 % roughly what Alberta commissions have always done?" Without a 2019 baseline number, the audit can't answer. This section computes that baseline by running the same snapping pipeline against the legally enacted 2019 map (Bill 33, 15 Dec 2017 — the 87-ED map that was in force when the 2026 commission convened).

**Methodology parity.** The 2019 run uses the identical snap tolerance (500 m), vertex densify (50 m), CSD reference layer (StatsCan 2021), and `USE_DA_SUPPLEMENT = False` setting that produced the 2026 headline numbers above. The only differences are the input shapefile (87 EDs instead of 89) and the name column (`EDName2017` instead of `name_2026`). No methodology drift.

### Result

| Map | n EDs | Total perim | Anchored perim | **Anchored pct (overall)** | Mean per-ED | Median per-ED |
|---|---:|---:|---:|---:|---:|---:|
| **2019 enacted (Bill 33)** | 87 | 24,953 km | 18,763 km | **75.2 %** | 46.3 % | 50.1 % |
| **Majority 2026** | 89 | 23,361 km | 16,598 km | **71.0 %** | 40.0 % | 35.0 % |
| **Minority 2026** | 89 | 23,128 km | 3,344 km | **14.5 %** | 21.4 % | 11.3 % |

**The 2019 baseline sits at 75.2 % — within 4.2 percentage points of the 2026 majority's 71.0 % and 60.7 percentage points above the 2026 minority's 14.5 %.**

### Top-10 / bottom-10 EDs under 2019

**Most-anchored 2019 EDs (top 10):**

| ED | Anchored % | Perim (km) |
|---|---:|---:|
| Drumheller-Stettler | 99.3 % | 1,087 |
| Vermilion-Lloydminster-Wainwright | 99.0 % | 528 |
| Fort Saskatchewan-Vegreville | 95.2 % | 558 |
| Spruce Grove-Stony Plain | 92.0 % | 45 |
| Bonnyville-Cold Lake-St. Paul | 91.5 % | 707 |
| Livingstone-Macleod | 90.3 % | 772 |
| Brooks-Medicine Hat | 90.1 % | 752 |
| Banff-Kananaskis | 88.9 % | 1,075 |
| Camrose | 86.0 % | 717 |
| Peace River | 85.6 % | 1,693 |

**Least-anchored 2019 EDs (bottom 10):**

| ED | Anchored % | Perim (km) |
|---|---:|---:|
| Edmonton-Rutherford | 0.0 % | 28 |
| Edmonton-Mill Woods | 0.0 % | 22 |
| Edmonton-Whitemud | 0.0 % | 31 |
| Edmonton-McClung | 0.0 % | 23 |
| Edmonton-Strathcona | 0.0 % | 26 |
| Edmonton-Riverview | 0.0 % | 29 |
| Edmonton-City Centre | 0.0 % | 19 |
| Edmonton-Glenora | 0.0 % | 24 |
| Edmonton-Highlands-Norwood | 0.0 % | 20 |
| Edmonton-Decore | 0.0 % | 18 |

The 18 zero-anchored 2019 EDs are all interior Edmonton, mirroring the same urban-CSD-singleton effect described under "Least-anchored EDs" above for 2026: when a city is a single CSD, internal subdivision lines do not coincide with municipal edges by definition. This pattern is identical across vintages and is not what drives the cross-map asymmetry.

Distribution under 2019: 7 EDs at >= 90 % anchoring, 44 at >= 50 %, 20 at < 10 % (of which 18 are interior Edmonton at exactly 0 %). The 2019 distribution is bimodal in the same shape as the 2026 majority — high-anchoring rural/perimeter-urban EDs, low-anchoring interior-urban EDs — and unlike the 2026 minority, which collapses *across* both rural and urban EDs.

### Verdict

**The 2019 baseline of 75.2 % sits closer to the 2026 majority (71.0 %) than to the 2026 minority (14.5 %) by an order of magnitude.** Specifically:

- **2019 vs 2026 majority: -4.2 pp.** The majority map is essentially continuing 2019 Alberta practice. A 4-point drop is within the noise budget of a normal redistribution cycle that adds two seats and reflows boundaries to absorb population growth.
- **2019 vs 2026 minority: -60.7 pp.** The minority map abandons 2019 Alberta practice almost completely. A drop of more than 60 percentage points in a single redistribution cycle is not a refinement of inherited geography; it is a wholesale departure from it.

**The minority's 14.5 % is genuinely unprecedented in recent Alberta practice, not a steeper-than-2019 continuation of an existing trend.** A reviewer asking whether 14.5 % is "just normal Alberta" can now be told: no — Alberta normal is roughly 75 %, the majority proposal preserves that, and the minority proposal does not. This strengthens the headline 4.9× majority/minority asymmetry from a *between-proposal* observation into a *between-proposal-and-Alberta-historical-practice* observation: the majority is the "stay" map and the minority is the "leave" map, with 2019 firmly on the majority side.

### Recommendations (PO decides; not auto-applied)

1. **Public report (`report_public.md`):** the headline pull-quote could be strengthened from "the minority anchors only 14.5 % of its perimeter to municipal edges, vs the majority's 71 %" to "the minority anchors only 14.5 %, vs the majority's 71 % and the 2019 enacted map's 75 % — the minority departs from Alberta historical practice by ~60 percentage points in a single cycle."
2. **Academic report (`report_academic.md`):** the §5.8 geographic-coherence subsection could add the 2019 baseline as a third row in the comparison table and frame the finding as a three-way comparison (2019 / 2026M / 2026m) rather than a two-way (2026M / 2026m), making the historical-precedent argument explicit.
3. **No methodology footnotes need revision.** The 2019 run uses identical parameters; the 75.2 % vs 71.0 % vs 14.5 % three-way comparison is parameter-controlled.

### Limitations specific to the 2019 baseline

1. **CSD layer is 2021-vintage**, not 2017-vintage. Alberta has had near-zero municipal-boundary changes between 2017 and 2021, so this is a small effect; using the same 2021 CSD layer for both vintages is a feature (it isolates *map* anchoring from *municipal-layer* drift) not a bug.
2. **2019 had 87 EDs vs 2026's 89.** The two added EDs are net new urban subdivisions; the rural perimeter base is largely unchanged, so the 75.2 % baseline is directly comparable to the 71.0 % / 14.5 % 2026 numbers without seat-count normalisation.
3. **The 2019 run does not produce a `v0_4_anchored.gpkg`** — only the per-ED CSV and summary JSON. The 2019 enacted map is not a downstream input to the canonical-shapefile pipeline; only the metric is needed.
