# v0.1 Airdrie Four-Quadrant Demographic Comparison Check

**Date:** 2026-04-26
**Scope:** Substantiate or revise the public-report claim that the four Airdrie minority quadrants are "within 8% of each other on every demographic measure the commission considers." Verdict: **Unsubstantiated as filed; the audit's own files document a different (and stronger) finding — that the four-way split is unforced by population arithmetic, regardless of demographic homogeneity.**

## Source the minority cites

**The minority commissioners do not, in fact, publish a per-quadrant demographic-difference rationale for the four-way Airdrie split in Appendix E.** The R3 (Calgary-Airdrie), R4 (Calgary-Foothills-Airdrie West), R14 (Airdrie East), and R18 (general growth-projection) entries in `analysis/methodology/minority_rationales_inventory.md` defend the configuration on grounds of:

- Growth projection (Airdrie 2025 population reported at 90,044 with 4.9% annual growth; projected 128,470 by 2033).
- Commuter ties (Airdrie is in the Calgary CMA above the 50%-flow CMA-membership threshold).
- Shared infrastructure (rapidly developing neighbourhoods north of Stoney Trail share infrastructure and commuting patterns with south Airdrie).

The minority does *not* publish a "rural and urban character differs across the quadrants" argument. The public-report bullet (line 199 of `report_public.md`) attributes such an argument to the minority as the implied basis for the four-way split, then refutes it with a "within 8% on every demographic measure" sub-claim. Both the implied minority claim and the refutation are audit-internal framings; neither is a primary-source extraction the audit has filed.

This is the same structural pattern documented for Claims 5 (Lethbridge) and 7 (St. Albert-Sturgeon) in `report_academic.md` §5.9.6: the public report's bullet structure invokes a minority claim that the source text does not quite contain, then evaluates it against a sub-claim the audit's own files do not quite document.

## Test method

A formal Airdrie-quadrant demographic comparison would require:

1. **Per-quadrant resident assignment.** Identify which Statistics Canada dissemination areas (DAs) fall inside each of the four minority Airdrie quadrants:
   - Calgary-Airdrie (south Airdrie, north Calgary across Stoney Trail).
   - Calgary-Foothills-Airdrie West (west Airdrie, plus NW Calgary along the Hwy 2 / Hwy 1A corridor).
   - Calgary-Nolan Hill-Cochrane (north flank of Airdrie, plus Cochrane and NW Calgary).
   - Airdrie East (east Airdrie + rural Rocky View / Beiseker / Irricana).
2. **Per-DA demographic extraction.** Pull StatsCan 2021 Census Profile (table 98-10-0019-01 and the broader 98-10-0019 series) at DA level for: median age, median household income, dwelling-type mix, mother-tongue distribution, immigrant-status mix.
3. **Quadrant aggregation.** Population-weight the DA values into a quadrant aggregate for each of the five demographic measures × four quadrants = 20 aggregate values.
4. **Pairwise comparison.** Compute the maximum spread between quadrants for each measure, and report whether that spread is within 8%.

**None of steps 2–4 can be run from the audit's filed data.** The audit's `data/` folder contains DA-level *population totals* (`alberta_2021_da_populations.csv`) but no DA-level demographic detail. A grep for "income," "age," "median," "demographic," "dwelling," "tongue," or "immigrant" across all CSV headers in `data/` returns zero matches.

For *step 1* (per-quadrant DA assignment), the audit *does* have the v0.8 minority shapefile (`data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg`) and the DA shapefile (`data/shapefiles/reference/alberta_2021_das.gpkg`). A spatial intersection identifies which DAs fall in each quadrant. This was *not* run for this file because steps 2–4 cannot proceed without demographic data; running step 1 alone produces no usable output for the demographic claim.

A sanity check on the spatial structure was run: the v0.8 Airdrie polygons are subject to a documented overlap problem (`analysis/reports/airdrie_overlap_report.md`). The "Calgary-Airdrie" polygon overlaps its three neighbours by a combined 532 km² (70.6% of its 754 km² footprint). This is a pixel-extraction artifact, not commission cartography. The overlap means a per-quadrant DA assignment from the v0.8 shapefile would be ambiguous for ~60 voting areas in the contested zone (per `airdrie_overlap_report.md` Table 2). A rigorous quadrant-comparison would need either (a) the official commission boundary shapefile (not publicly released), or (b) a documented disambiguation rule (e.g., `parent_ed_2019` crosswalk fallback as currently used).

## Data sources

- **City of Airdrie population:** `data/justification_test_inputs.csv` row T3 — 2021 population **74,100** (StatsCan CSD 4806016).
- **DA shapefile:** `data/shapefiles/reference/alberta_2021_das.gpkg`. Spatial intersection with an Airdrie city bounding box (lat 51.24–51.36°N, lon -114.10 to -113.95°W) identifies **89 DAs** with centroids inside the city, totalling **74,100** population — exact match with the StatsCan CSD figure.
- **Minority quadrant shapefile:** `data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg`, four polygons: Airdrie East (canonical tier A); Calgary-Airdrie (tier C-2019-split, with 70.6% overlap problem documented in `airdrie_overlap_report.md`); Calgary-Foothills-Airdrie West (tier A); Calgary-Nolan Hill-Cochrane (tier A).
- **Population test outcome:** `analysis/reports/justification_tests_findings.md` Test 3, which finds the 4-way split is unforced by population arithmetic — each Airdrie quarter is ~18,525, requiring 22,672 non-Airdrie residents per quarter to reach the 41,197 floor; a 2-way split (37,050 per half, requiring only 4,147 non-Airdrie residents per half) is comfortably within bounds.
- **Demographic data:** *Not in the audit*. Required source would be StatsCan 2021 Census Profile DA-level extraction (table 98-10-0019 series), available via the StatsCan Web Data Service or via custom DA-level census-profile pulls.

## Findings

**The "within 8% of each other on every demographic measure" claim cannot be substantiated from any file in the audit.** The audit's data infrastructure does not include DA-level or CSD-level demographic detail beyond population totals. The five plausible demographic measures the public-report wording implies (median age, median household income, dwelling-type mix, mother-tongue distribution, immigrant-status mix) have not been extracted, computed, or filed.

**However: the audit has documented a stronger and adjacent finding** in `analysis/reports/justification_tests_findings.md` Test 3. The four-way split is unforced by population arithmetic. A two-way split is sufficient. This is the load-bearing audit finding on the Airdrie configuration — it does not depend on demographic homogeneity at all. Whether the four quadrants are demographically similar or different is *irrelevant* to the population-arithmetic argument: the math says the city does not need to be split four ways regardless of who lives in each quadrant.

**The "within 8%" rhetoric is a different and more contestable argument.** It implicitly assumes that demographic homogeneity is a *reason* against splitting (i.e., "you don't need to split because the people are all the same"). This is a weak version of the stronger argument the audit actually makes (the population math doesn't require splitting at all). The "within 8%" framing also exposes the audit to a hostile-reviewer attack: a defender of the four-way split could argue that even within an 8% demographic envelope, the four quadrants have *different* commuter destinations, *different* school catchments, or *different* growth trajectories that justify separate representation. None of those defenses contradict an 8%-demographic-homogeneity finding.

**Order-of-magnitude observation:** Airdrie is a relatively young, middle-income, English-mother-tongue, owner-occupied-dwelling city across all four quadrants. The 2021 Census Profile for the City of Airdrie CSD as a whole (publicly accessible, not currently filed) shows: median age ~33 years; median total household income ~$110,000; ~85% English mother tongue; ~75% owned dwellings; ~20% immigrant population. There is no obvious reason to expect within-city heterogeneity to exceed 8% on these measures — Airdrie is not a city with sharp socio-economic gradients. But the audit cannot file this as audit-grade evidence without doing the DA-level extraction.

## Verdict

**Unsubstantiated on the "within 8% of each other on every demographic measure" claim as filed.** The audit's own data does not allow the calculation. The stronger underlying finding — that the four-way split is unforced by population arithmetic — is **strongly supported** by `justification_tests_findings.md` Test 3 and is the verdict the public-report bullet should rely on.

The "within 8%" framing should be removed or replaced. The "**Fail**" verdict on the four-way Airdrie split is robust and should be preserved, but on the population-arithmetic ground rather than the unfiled demographic-homogeneity ground.

## Reproducibility

The Airdrie-quadrant demographic comparison can be substantiated, but the audit has not done it. A third party would need to:

1. **Pull StatsCan 2021 Census Profile DA-level data** for the 89 DAs inside Airdrie city limits. The Census Profile DA-level release is StatsCan table 98-10-0019-01 (and related sub-tables for income, dwelling, language, immigration). Bulk download via `https://www150.statcan.gc.ca/n1/en/catalogue/98-10-0019-01` or via the StatsCan Web Data Service.
2. **Assign each DA to a minority quadrant** via spatial intersection with the v0.8 minority shapefile. Use centroid-in-polygon for unambiguous DAs; use the documented `parent_ed_2019` fallback for the ~60 voting areas in the Calgary-Airdrie overlap zone (per `airdrie_overlap_report.md`).
3. **Population-weight the DA values into quadrant aggregates** for median age, median household income, dwelling-type mix, mother-tongue distribution, immigrant-status mix.
4. **Compute the max-min spread per measure** and report whether each falls within ±8% of the four-quadrant mean.

A starter Python skeleton:

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

# Step 1 - load Airdrie DAs
das = gpd.read_file('data/shapefiles/reference/alberta_2021_das.gpkg').to_crs('EPSG:4326')
airdrie_bbox = box(-114.10, 51.24, -113.95, 51.36)
airdrie_das = das[das.geometry.centroid.within(airdrie_bbox)]
# 89 DAs, total pop 74,100

# Step 2 - assign to quadrants via spatial join with minority shapefile
mins = gpd.read_file('data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg').to_crs('EPSG:4326')
airdrie_quadrants = mins[mins['name_2026'].isin([
    'Airdrie East',
    'Calgary-Airdrie',
    'Calgary-Foothills-Airdrie West',
    'Calgary-Nolan Hill-Cochrane'
])]
# Then sjoin airdrie_das with airdrie_quadrants by centroid

# Step 3 - merge with StatsCan DA-level census profile (NOT YET DOWNLOADED)
# census_profile = pd.read_csv('data/statscan_98_10_0019_da_alberta.csv')  # FILE DOES NOT EXIST

# Step 4 - aggregate and compare
```

The data download in step 3 is the missing input. StatsCan's DA-level census-profile bulk file is large (~5GB compressed) and requires filtering to Alberta DAs before quadrant-aggregation. Approximate time to complete: 4–6 hours of data engineering plus ~2 hours of analysis.

## Public-report implication

**The current public-report sentence (line 199) — "Airdrie split four ways: minority commissioners said rural and urban character differs across Airdrie's quadrants; Statistics Canada says the four quadrants are within 8% of each other on every demographic measure the commission considers. **Fail.**" — overstates the audit's filed evidence and misattributes a rationale to the minority.**

**Suggested rewrites, in declining order of evidentiary strength:**

**Rewrite A (preferred, matches filed evidence exactly).** "Airdrie split four ways: minority commissioners cited population growth and Calgary-CMA commuter ties; the audit's population arithmetic finds the four-way split is unforced — a two-way split (each half ~37,050 + ~4,147 from Rocky View / Cochrane) sits comfortably within the ±25% rule, while the four-way split forces each quarter (~18,525) to absorb 22,672 non-Airdrie residents, manufacturing the four cross-municipal hybrids that span Calgary, Cochrane, Foothills, and rural Rocky View. **Fail.**"

**Rewrite B (preserves demographic-homogeneity framing as a secondary observation).** "Airdrie split four ways: minority commissioners cited population growth and Calgary-CMA commuter ties; the audit's population arithmetic finds the four-way split is unforced (a two-way split is sufficient under the ±25% rule), and Airdrie's city-wide demographic profile (a young, middle-income, predominantly owner-occupied, predominantly English-mother-tongue Calgary-CMA satellite) does not exhibit within-city heterogeneity that would justify dividing residents across four electoral districts. **Fail.**"

**Rewrite C (only if the DA-level extraction is performed before publication).** Substantively equivalent to the current public-report bullet, but with a methodology file documenting per-quadrant median age / income / dwelling / language / immigration aggregates from StatsCan DA-level data and confirming the 8% ceiling. Required work: ~6–8 hours of data engineering and analysis as outlined in the Reproducibility section.

**Recommendation: adopt Rewrite A.** It removes the unsubstantiated "8% on every demographic measure" claim, removes the misattribution to the minority of an argument they did not publish, and replaces both with the audit's strongly-documented population-arithmetic finding. The **Fail** verdict on the rationale is preserved on stronger ground.

The "Airdrie split four ways" finding is one of the audit's most robust per-district verdicts (Test 3 in `justification_tests_findings.md` is closed and reproducible end-to-end). The public-report bullet should not weaken its own evidentiary position by leaning on an unfiled demographic comparison when the population-arithmetic case is already strong.

## Files

- This file: `analysis/methodology/airdrie_quadrant_demographic_comparison.md`.
- Cross-references: `analysis/reports/justification_tests_findings.md` Test 3; `analysis/reports/airdrie_overlap_report.md`; `analysis/methodology/minority_rationales_inventory.md` R3/R4/R14/R18; `analysis/methodology/minority_rationales_validation.md` §R3/R4/R18; `report_academic.md` §5.9.6 Claim 1.
- Source files that *would need to be added* to substantiate the 8% figure: a StatsCan 2021 Census Profile DA-level extraction (table 98-10-0019 series) for the 89 DAs inside Airdrie city limits; a documented spatial-join from those DAs to the four minority quadrants (with the v0.8 overlap-zone disambiguation rule).

## Caveats

- The 89 Airdrie DAs identified by spatial intersection with the city bounding box (lat 51.24–51.36°N, lon -114.10 to -113.95°W) total 74,100 population, exactly matching the StatsCan CSD-level 2021 figure. The DA list is therefore complete.
- The v0.8 Calgary-Airdrie polygon has a documented 70.6% overlap problem with neighbouring polygons (`airdrie_overlap_report.md`). Any per-quadrant DA assignment must use the documented `parent_ed_2019` crosswalk fallback for ~60 ambiguous voting areas. This adds uncertainty to the quadrant-assignment step but does not block the demographic comparison once Census Profile data is in hand.
- The "8% within" claim, even if substantiated, would not by itself refute the minority's stated rationales (which are growth and commuter ties, not demographic heterogeneity). The public-report wording sets up a refutation of an argument the minority did not actually make. The demographic comparison would be ancillary to — not a substitute for — the population-arithmetic finding the audit already documents.
- "Every demographic measure the commission considers" is an unbounded set unless the commission's published methodology specifies which measures it weighed. Appendix E of the EBC 2025–26 Final Report references population, geography, communities of interest, and historical patterns but does not enumerate "demographic measures" in a closed list. The "8% on every measure" phrasing is therefore literally untestable without additional commission documentation. The audit should either name the specific measures it claims fall within 8% (median age, household income, dwelling type, language, immigration) or drop the universal "every measure" framing.
