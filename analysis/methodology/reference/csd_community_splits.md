# CSD-level Community-Splits Count, Per Map (Track H)

Status: v0.1 — revisable. This is a companion analysis to §C4 in `section_C_geographic_coherence.md`. It supplies verifiable per-CSD counts for the community-of-interest claim that the §C4 narrative rests on.

## Method

### Inputs

- `data/alberta_2021_csds.gpkg` — 423 Statistics Canada 2021 Census Subdivision polygons for Alberta.
- `data/alberta_2021_csd_populations.csv` — 2021 populations by CSDUID.
- `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp` — 87 Elections Alberta 2019 Electoral Division polygons (currently in force).
- `data/majority_hybrid_crosswalk.csv` — 19 rows from Appendix C, covering the majority commission's hybrid and renaming changes.
- `data/minority_hybrid_crosswalk.csv` — 103 rows, heuristically assembled from Appendix E with a `jaccard` match score; includes 14 rows where a 2019 ED has no clean 2026 successor and is recorded as `(MERGED/ABSORBED)`.

### Population filter

CSDs with 2021 population below 1,000 are excluded. This removes unpopulated reserves, small villages, and Improvement Districts whose presence in multiple EDs is a cartographic artifact rather than a community-of-interest concern. One exception is retained: Improvement District No. 9 (Banff), included by name in §C4's focus list even though its 2021 population is 1,004. It clears the threshold.

191 populated CSDs are analysed.

### 2019 splits (measured)

Computed by spatial overlay of the projected CSD polygons onto the 2019 ED polygons (CRS `EPSG:3401`). A CSD is counted as "present in" a 2019 ED only if the intersection meets either of:

- ≥ 2 percent of the CSD's own area, or
- ≥ 1 km² in absolute terms.

Both conditions filter sliver artifacts arising from minor geometry mismatch between the StatsCan CSD layer and the Elections Alberta ED layer without suppressing genuine partial containment. The resulting per-CSD count is the number of 2019 EDs the CSD spans.

### 2026 splits (estimated, crosswalk-based)

No 2026 shapefiles exist. Splits under the two 2026 proposals are inferred by taking each CSD's 2019-ED membership set and mapping it through the relevant crosswalk:

- If a 2019 ED appears in the crosswalk with a single 2026 successor, the CSD's membership in that 2019 ED contributes one 2026 ED.
- If a 2019 ED appears in the crosswalk with multiple 2026 successors (a hybrid that was split), the CSD's membership contributes all listed successors. The CSD is flagged `uncertain` because without the 2026 shapefile we cannot determine which side of the new internal boundary the CSD actually sits on — it may sit entirely in one successor, or it may straddle both.
- If a 2019 ED is not in the crosswalk at all, the majority's 19-row crosswalk only covers hybrid changes; unlisted EDs are assumed to carry forward as a single 2026 successor with the same name. This is the intended reading of Appendix C.
- In the minority crosswalk specifically, 14 rows list `(MERGED/ABSORBED)` as the successor — the 2019 ED was fully dissolved into adjacent 2026 EDs without a single named heir. These rows are skipped in the lower-bound count and added back one-to-one in the upper-bound count. Any CSD that intersects such a 2019 ED is flagged `uncertain`.

Because this approach operates at ED granularity, it does not capture CSD-level splits that occur entirely within a 2019 ED when that 2019 ED is carved into two 2026 EDs. A hybrid 2019 ED can split a CSD that the 2019 map kept whole; the crosswalk tells us that a split may have occurred but not which CSD it bisected. This is the core structural limitation of the method, and it is why CSDs with `majority_uncertain = True` or `minority_uncertain = True` are called out in the per-CSD summary.

### Top-line caveat

The strongest claim this analysis supports is at the level of the confident subset — CSDs whose 2019-ED containment maps cleanly through both crosswalks. On the full 191-CSD sample, minority-vs-majority comparisons are partly driven by crosswalk gaps rather than boundary substance.

## Results

### Per-map summary

All 191 populated CSDs (pop ≥ 1,000):

| Metric                                     | 2019  | Majority 2026 (est) | Minority 2026 (lower) | Minority 2026 (upper) |
|--------------------------------------------|-------|---------------------|-----------------------|-----------------------|
| CSDs split across ≥ 2 districts            | 66    | 66                  | 54                    | 66                    |
| % of populated CSDs split                  | 34.6% | 34.6%               | 28.3%                 | 34.6%                 |
| Mean districts per CSD                     | 1.83  | 1.83                | 1.49                  | 1.83                  |
| Median districts per CSD                   | 1.0   | 1.0                 | 1.0                   | 1.0                   |

Confident-only subset (`uncertain = False` in both crosswalks, n = 139):

| Metric                                     | 2019  | Majority 2026 (est) | Minority 2026 (est)   |
|--------------------------------------------|-------|---------------------|-----------------------|
| CSDs split across ≥ 2 districts            | 40    | 40                  | 40                    |

On the confident subset the three maps are identical. The 12-CSD gap between minority-lower (54) and minority-upper (66) is the crosswalk-gap band; it reflects the 14 `(MERGED/ABSORBED)` rows in the minority crosswalk, not known unity.

The honest headline: at CSD granularity, with only ED-level crosswalks available, the three maps are not distinguishable on this metric. That is different from saying they produce the same community-of-interest outcome. It says we cannot see a difference at this resolution.

### Top-10 most-split CSDs

Under 2019 (measured by spatial overlay):

| CSD                                       | Pop. 2021 | EDs spanned |
|-------------------------------------------|-----------|-------------|
| Calgary, City (CY)                        | 1,306,784 | 27          |
| Edmonton, City (CY)                       | 1,010,899 | 20          |
| Rocky View County, MD                     | 41,028    | 5           |
| Yellowhead County, MD                     | 10,426    | 5           |
| Wheatland County, MD                      | 8,738     | 5           |
| Greenview No. 16, MD                      | 8,584     | 5           |
| Clearwater County, MD                     | 11,865    | 4           |
| Ponoka County, MD                         | 9,998     | 4           |
| Camrose County, MD                        | 8,504     | 4           |
| Cypress County, MD                        | 7,524     | 4           |

Under majority 2026 (estimated via crosswalk): identical to the 2019 list at these magnitudes. The majority crosswalk's 19 rows only touch hybrid or renamed EDs, and none of the hybrids consolidate these large rural CSDs into fewer successor EDs.

Under minority 2026 (estimated via crosswalk, lower bound):

| CSD                                       | Pop. 2021 | EDs spanned (lower) | Flag        |
|-------------------------------------------|-----------|---------------------|-------------|
| Calgary, City (CY)                        | 1,306,784 | 26                  | uncertain   |
| Edmonton, City (CY)                       | 1,010,899 | 17                  | uncertain   |
| Yellowhead County, MD                     | 10,426    | 5                   | —           |
| Greenview No. 16, MD                      | 8,584     | 5                   | —           |
| Wheatland County, MD                      | 8,738     | 4                   | —           |
| Cypress County, MD                        | 7,524     | 4                   | —           |
| Big Lakes County, MD                      | 4,986     | 4                   | —           |
| Woodlands County, MD                      | 4,558     | 4                   | —           |
| Smoky Lake County, MD                     | 3,874     | 4                   | —           |
| Rocky View County, MD                     | 41,028    | 3                   | uncertain   |

Calgary at 26 (vs 27 under 2019) and Edmonton at 17 (vs 20) reflect the minority crosswalk's hybrid moves and `(MERGED/ABSORBED)` gaps; both cities would still be the two most-split CSDs under any reading.

### Focus CSDs (contested configurations)

| CSD                                        | Pop.    | 2019 | Majority | Minority (lower) | Notes                                          |
|--------------------------------------------|---------|------|----------|------------------|------------------------------------------------|
| Calgary, City (CY)                         | 1,306,784 | 27   | 27       | 26               | Always split; structural, not a finding.       |
| Edmonton, City (CY)                        | 1,010,899 | 20   | 20       | 17               | Always split; structural.                      |
| Airdrie, City (CY)                         | 74,100   | 2    | 2        | 1*               | *Minority figure depressed by `Airdrie-Cochrane` being MERGED/ABSORBED; the §C4 narrative text says minority splits Airdrie into 4 EDs via hybrid absorption into Calgary-Foothills and Olds-Three Hills, which this crosswalk method cannot verify without the 2026 shapefile. |
| St. Albert, City (CY)                      | 68,232   | 2    | 2        | 2                | Both maps split it into the city ED and the surrounding ED.  |
| Cochrane, Town (T)                         | 32,199   | 1    | 1        | 0*               | *Minority = 0 is an artifact of `Airdrie-Cochrane` being MERGED in the crosswalk. The §C4 narrative says the minority places Cochrane inside `Calgary-Nolan Hill-Cochrane`, which is a 1-ED placement but inside a Calgary-named district. The split-count metric does not detect this framing concern.  |
| Chestermere, City (CY)                     | 22,163   | 1    | 1        | 1                | §C4 flags `Calgary-Peigan-Chestermere` as a partial inclusion; under a 2-percent area threshold the Calgary intersection does not meet the cutoff, so Chestermere reads as single-ED here. Revisit if 2026 shapefiles release. |
| Red Deer, City (CY)                        | 100,844  | 2    | 2        | 2                | Consistent with §C4's observation that both maps split Red Deer; only the naming of successor EDs differs (`Red Deer-North/South` in the majority reading, `Red Deer-Blackfalds/Innisfail` under minority). |
| Red Deer County, MD                        | 19,933   | 2    | 2        | 2                | Surrounding rural CSD, structurally split.     |
| Town of Banff                              | 8,305    | 1    | 1        | 0*               | *Minority = 0 is a `Banff-Kananaskis` → MERGED/ABSORBED artifact. Cannot verify without 2026 shapefile. |
| Improvement District No. 9 (Banff)         | 1,004    | 3    | 3        | 2                | The ID's three 2019 EDs collapse to two under the minority (one absorbed). Low-population, structural.  |
| Rocky Mountain House, Town (T)             | 6,765    | 1    | 1        | 1                | Unsplit in all three. §A3 concern is with the ED shape surrounding it (`Rimbey-Rocky Mountain House-Sundre`), not with the CSD being divided. |

Stars mark counts that are depressed by `(MERGED/ABSORBED)` entries in the minority crosswalk rather than by observed consolidation.

### What this does and does not say

This analysis verifies, with 2019 measured and both 2026 proposals estimated:

- Calgary and Edmonton are split across ~20+ EDs under all three maps. That is dictated by population; both cities exceed any feasible single-ED quotient.
- Mid-size cities (Red Deer, St. Albert) are split across 2 EDs under all three maps.
- Large rural MDs (Rocky View, Yellowhead, Wheatland, Greenview, Foothills) are split across 4–5 EDs under all three maps. These are also structural — the counties are physically larger than a single rural ED quotient.

It does not verify the §C4 qualitative claims that turn on how a community is named or paired with adjacent communities:

- The Airdrie 4-way split claim (minority) relies on hybrids that absorb parts of Airdrie into Calgary-Foothills-Airdrie West and Olds-Three Hills. The CSD-level count sees Airdrie inside the Airdrie-Cochrane and Airdrie-East 2019 EDs and cannot see the within-ED partition that creates the 4-way split.
- The Chestermere-into-Calgary concern (`Calgary-Peigan-Chestermere` in the minority) depends on a partial inclusion that falls below the 2 percent overlay threshold used here. It reads as single-ED under this metric.
- The Cochrane-merged-with-Calgary concern is about which district name a town sits in, not whether the town itself is divided.

These three qualitative concerns are real and independently supported by the Appendix E text. The CSD split-count metric is not the right instrument for them.

## Interpretation

### Against §C4's existing claim

§C4 currently states, in its summary table: minority is Airdrie-split-4 vs majority's Airdrie-split-2, minority is Chestermere-partial vs majority's Chestermere-intact, minority systematically chose the more split or more irregular option across every divergent configuration.

This CSD-level count neither refutes nor strongly confirms that claim. On the narrow question "how many CSDs are split across multiple districts under each map":

- The confident-subset answer is identical for all three maps (40 of 139).
- The full-sample answer, taken literally, is 66 under 2019, 66 under majority, 54–66 under minority depending on whether crosswalk gaps are counted as unity or as unity-with-unknown-split. No reading supports a statement that the minority is worse than the majority on this specific metric.

What the metric can say about systematic difference is limited to what visible at ED granularity. The §C4 claim's strongest evidence is at within-ED granularity — how the minority partitions Airdrie between Airdrie-East and Calgary-Foothills-Airdrie West, how it slides part of Chestermere into Calgary-Peigan-Chestermere. Without 2026 shapefiles, those partitions are visible in the Appendix E maps and text but not in the crosswalk, and not in CSD overlay counts.

### Recommendation for the §C4 narrative

The existing §C4 text should be preserved, but the summary table currently reads as if the community-of-interest advantage is a count-of-splits advantage. It is not. It is an advantage at within-ED granularity that a CSD-level count cannot see. Two low-cost updates would tighten the claim:

1. Add a row or footnote to the §C3+C4 summary table noting that at CSD granularity the three maps split the same count of municipalities across multiple districts, and that the minority's community-of-interest disadvantage is within-ED (how a named municipality is carved between adjacent EDs), not across-ED.
2. Cite Track H as the verification attempt, note the shapefile-gap limitation, and mark the within-ED partition question as "unmeasurable until 2026 shapefiles release."

This revises §C4's implicit framing without changing its overall direction.

### Headline sentence for downstream documents

At the CSD level, all three maps split the same roughly one-third of populated census subdivisions across multiple EDs, driven by CSD size against the per-district population quotient. The minority's community-of-interest concerns operate within 2019-ED boundaries and are not visible at CSD-overlay granularity; they require 2026 shapefiles or close reading of the Appendix E maps to verify.

## Files

- Script: `analysis/scripts/csd_community_splits.py`
- Per-CSD detail: `data/csd_splits_summary.csv`
- Section under revision: `analysis/reports/section_C_geographic_coherence.md` §C4
- Academic report section potentially affected: `report_academic.md` §3 (community of interest) — flag, do not edit.

## Dependencies header

Backward: `alberta_2021_csds.gpkg`, `alberta_2021_csd_populations.csv`, `alberta_2019_eds/*.shp`, `majority_hybrid_crosswalk.csv`, `minority_hybrid_crosswalk.csv`.
Forward: section C revision, academic report community-of-interest paragraph.
