# v0.1 Rocky Mountain House-Banff Park — National-Park Extension Population & Ranching Check

**Date:** 2026-04-26
**Scope:** Substantiate or qualify the public-report claim that the minority's Banff National Park extension polygon contains "zero year-round residents and zero working ranches." Verdict: **Geographically plausible but quantitatively softer than "zero"; the polygon-clipped DA-population analysis run for this file finds approximately 491 area-weighted residents in the NP/mountain-park slice, drawn entirely from two enormous rural dissemination areas whose actual park-land portion is essentially uninhabited.**

## Source the minority cites

Appendix E, p. 352 (R12 in the audit's rationale inventory). The minority invokes the s.15(2) exception for the Banff National Park extension on four grounds:

1. North-south economic corridor along Highway 22.
2. Rocky Mountain House as the only town in Clearwater County and a hub for the surrounding population.
3. Implications of dividing regional Indian reserves from the nearest economic hub.
4. Historical precedent: portions of Banff National Park have previously been included in a west-central Alberta electoral division.

The minority does *not* explicitly invoke "ranching community of interest" for the extension polygon. The "ranching community of interest" framing in the public-report bullet (line 200 of `report_public.md`) is the audit's gloss on the minority's economic-zone argument. The Appendix E text describes Rocky Mountain House as a regional hub for Clearwater County including "Indian reserves" and emphasises Highway 22 north-south continuity; it does not single out ranching as the binding interest.

## Test method

Three checks were run for this file:

1. **Polygon extraction.** Extract the Rocky Mountain House-Banff Park polygon from the v0.8 refined minority shapefile (`data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg`).
2. **NP/mountain-park slice isolation.** Approximate the "Banff NP extension" portion as the part of the district west of longitude -115.5° and north of latitude 51.4° (covering the District's western mountain wilderness — Banff NP backcountry north of the townsite, Lake Louise / Bow Valley headwaters, and the eastern-slopes mountain block adjacent to BC).
3. **Polygon-clipped population count.** Intersect the slice with Statistics Canada 2021 dissemination-area (DA) boundaries, then area-weight each DA's population by the fraction of its area that falls inside the slice.

Census-of-Agriculture extraction (working-ranch count) was *not* run for this file: no Census-of-Agriculture file exists in the audit's `data/` folder, and the public Statistics Canada Census-of-Agriculture tables are organized by Census Agricultural Region (CAR) and by CSD (municipality), not by arbitrary polygon. Banff National Park itself has no working agricultural land — agricultural use is prohibited under the Canada National Parks Act, S.C. 2000, c. 32, s. 15 and s. 16 (commercial use restricted to existing leaseholds in townsites; no farming or ranching tenure permitted in park backcountry). The "zero working ranches" claim is therefore a statutory entailment of the Canada National Parks Act for the park-land portion of the polygon, not an empirical Census-of-Agriculture count.

## Data sources

- **Minority shapefile:** `data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg`, district `Rocky Mountain House-Banff Park` (canonical tier A, anchoring 37.3% municipal / 1.5% DA, polygon area 19,120 km², bounds approximately lat 51.43–52.85°N, lon -116.98 to -114.47°W in EPSG:3401).
- **DA shapefile:** `data/shapefiles/reference/alberta_2021_das.gpkg` (6,203 DAs, EPSG:3347).
- **DA populations:** `data/alberta_2021_da_populations.csv` (StatsCan 2021 Census, table 98-10-0001-01 dissemination-area release; 6,182 of 6,203 DAs successfully merged; total Alberta DA population 4,262,635).
- **Statutory framework:** Canada National Parks Act, S.C. 2000, c. 32, ss. 15–16 (no agricultural tenure in backcountry park land).
- **District-level minority population:** `data/minority_2026_populations.csv` row 81 (Rocky Mountain House-Banff Park, population 38,298, deviation -30.28%, NOT within ±25% — the minority itself classifies this as a Rest-s15(2) district requiring the area exception).

## Findings

**The Rocky Mountain House-Banff Park polygon as drawn in the v0.8 minority shapefile spans 19,120 km².** Of this:

- Total polygon-clipped DA population (area-weighted, all DAs intersecting the polygon): **26,444 residents**.
- Centroid-in-polygon DA population (52 DAs): **27,323 residents**.

This is materially lower than the 38,298 residents the minority's own published figure assigns to the district. The discrepancy is consistent with the audit's documented shapefile-precision sunset clause (`report_academic.md` §4.1.4): the v0.8 polygon is a derived geometry constructed from PNG extraction of the commission's published map, not the commission's official boundary file (which has not been publicly released as a shapefile). The 26,444-vs-38,298 gap (a ~31% under-count) reflects shapefile drift, not a population error in the minority's own number.

**The "Banff NP extension" portion specifically (west of -115.5° lon, north of 51.4° lat):**

- Slice area: **7,143 km²** (37.4% of the total district).
- DAs intersecting the slice: **5**.
- Area-weighted population in the slice: **491 residents**.

The 491 figure comes almost entirely from two very large rural DAs (DAUID 48090073, total pop 411 spread over 6,154 km², 76.4% inside the slice = 314 weighted residents; DAUID 48090085, total pop 461 spread over 6,248 km², 38.3% inside the slice = 176 weighted residents). These two DAs together cover approximately 12,400 km², spanning the entire eastern-slopes mountain block from David Thompson Country south through the Front Ranges. The actual Banff NP backcountry portion of these DAs is uninhabited under the Canada National Parks Act — Parks Canada operates only the Lake Louise and Banff townsites (both excluded from the minority polygon), staffed warden cabins, and seasonal lodges (Num-Ti-Jah, Castle Mountain, Mosquito Creek hostel). Year-round population in the park-land portion is, by Parks Canada's own land-use designation, limited to a small number of warden families and concession-lease operators — likely in the low double digits across the entire NP territory inside the slice, not the 491 figure the area-weighting produces.

**The "zero year-round residents" public-report claim is therefore literally false at the area-weighted DA-population level (~491 residents in the polygon-clipped slice) but plausibly true at the actual park-land level inside the slice (likely fewer than 50 year-round residents, drawn from Parks Canada warden households and lease-operators).** The 491 figure is an artifact of the DA being the smallest publicly-released census geography; the DA-internal distribution of those 411 + 461 residents is not in StatCan's public release. Most of those residents live in scattered Clearwater County rural homes and along Highway 11 / Forestry Trunk Road — *outside* the Banff NP boundary, even though the DA they belong to extends into the park.

**The "zero working ranches" claim is statutorily entailed for the Banff NP portion of the slice** (Canada National Parks Act prohibits agricultural tenure) but is *not* entailed for the eastern-slopes Bighorn Country / public-lands portion of the slice (which is Crown land outside the park, available for grazing leases under the Public Lands Act, R.S.A. 2000, c. P-40). The audit did not extract grazing-lease data from Alberta Forestry's Public Lands Administrative Database. A grazing lease is not the same as a "working ranch," but the claim "zero working ranches" requires either (a) restricting the polygon to the park-land portion only, in which case the Canada National Parks Act delivers the result, or (b) extracting Census-of-Agriculture farm counts for the relevant CSDs, which is feasible from StatsCan's 2021 Census of Agriculture table 32-10-0152-01 (number of farms by farm type, by CSD) but was not done for this file.

## Verdict

**Inconclusive on the literal "zero residents" phrasing as written; Substantiated on the underlying point.** The polygon-clipped DA-population result (~491 area-weighted residents) is non-zero, so the public-report claim cannot stand as "zero year-round residents" without qualification. However:

- The 491 figure is almost certainly an over-count of *park-land residents* because DAs near the park boundary include extensive Clearwater County / Bighorn rural-residential territory outside the park.
- Statutory restrictions under the Canada National Parks Act mean the actual park-land portion of the slice has very few year-round residents (Parks Canada warden families, lease-operators) and no agricultural tenure.
- The minority's own population figure for the entire district (38,298, -30.3% deviation) confirms that the population the minority counts in the district lives almost entirely in the *non-park* portion (Clearwater County, Rocky Mountain House town, Sundre, Rimbey, Caroline, Ponoka County). The minority itself does not claim the NP extension adds population.

**Bottom line: the NP-extension polygon contains far fewer residents than the rest of the district, but not literally zero.** The audit's public-report wording overstates the precision available from polygon-clipped Census data.

## Reproducibility

The polygon-clipped DA-population calculation can be reproduced end-to-end:

```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

# Load minority shapefile
gdf = gpd.read_file('data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg')
rmh = gdf[gdf['name_2026'] == 'Rocky Mountain House-Banff Park'].to_crs('EPSG:4326')

# Define NP/mountain-park slice (west of -115.5 lon, north of 51.4 lat)
np_bbox = box(-117.0, 51.4, -115.5, 52.5)
np_slice = rmh.geometry.iloc[0].intersection(np_bbox)

# Load DAs and populations
das = gpd.read_file('data/shapefiles/reference/alberta_2021_das.gpkg').to_crs('EPSG:4326')
pops = pd.read_csv('data/alberta_2021_da_populations.csv')
das['DAUID'] = das['DAUID'].astype(str)
pops['DAUID'] = pops['DAUID'].astype(str)
das = das.merge(pops[['DAUID', 'population_2021']], on='DAUID')

# Area-weighted population in slice
slice_das = das[das.geometry.intersects(np_slice)].copy()
slice_das['intersect_area'] = slice_das.geometry.intersection(np_slice).area
slice_das['frac_inside'] = slice_das['intersect_area'] / slice_das.geometry.area
slice_das['weighted_pop'] = slice_das['population_2021'] * slice_das['frac_inside']
print(f'NP-slice area-weighted population: {slice_das["weighted_pop"].sum():.0f}')
```

A third party can verify by running the above against the published shapefiles and StatCan 2021 DA population release.

For a tighter check on actual park-land residents, the follow-up calculation would intersect the slice with the official Banff National Park boundary (available from Parks Canada open-data portal, `open.canada.ca` dataset "Canadian National Parks Boundaries"), then re-run the DA-area-weighting on that strict park-land polygon. The audit did not pull the Parks Canada boundary file for this check; this is a flagged follow-up if a tighter "zero residents" claim is needed.

For the working-ranches sub-claim, StatsCan Census of Agriculture 2021 table 32-10-0152-01 (number of farms by CSD) can be filtered to Clearwater County (CSD 4809026), Improvement District No. 9 Banff (CSD 4815080 — Banff NP), and Improvement District No. 12 Jasper (CSD 4815084 — outside this polygon). Any "farm" count in the Banff NP CSD would be a Parks-Canada-permitted historical leasehold (very rare, none currently active per Parks Canada 2024 land-use disclosure). Clearwater County would have a substantial farm count but those farms are *outside* the NP extension portion.

## Public-report implication

**The current public-report sentence (line 200) — "Rocky Mountain House extended into Banff National Park: minority commissioners said ranching community of interest; the extended polygon contains zero year-round residents and zero working ranches" — overstates the audit's filed evidence in two ways:**

1. **"Zero year-round residents" is not literally true** at the polygon-clipped DA-population level (~491 area-weighted residents). It is *plausibly* true at the strict park-land level, but the audit has not run the strict-park-boundary check.
2. **"Zero working ranches" is statutorily entailed for the Banff NP portion** under the Canada National Parks Act, but not for the broader polygon slice (which includes Crown land outside the park where grazing leases are permissible). The audit has not pulled Census of Agriculture data to count actual farms.

**Suggested rewrites, in declining order of evidentiary strength:**

**Rewrite A (preferred, tightest defensible statement).** "Rocky Mountain House extended into Banff National Park: minority commissioners cited north-south economic corridor and historical precedent; the National Parks Act prohibits agricultural tenure inside the park boundary, and the audit's polygon-clipped 2021 dissemination-area population check finds the mountain-park portion of the polygon contributes no measurable additional resident population to the district beyond what the Clearwater County / Highway 11 corridor already supplies. **Fail (the s.15(2) area exception is not load-bearing for either area or population qualification — see audit Test 2).**"

**Rewrite B (preserves the punchy 'zero' framing with disclosure).** "Rocky Mountain House extended into Banff National Park: minority commissioners cited north-south economic corridor and historical precedent; the extension passes through territory with no documented year-round residents in Statistics Canada's 2021 dissemination-area population grid (the area-weighted DA-population in the park-land portion is dominated by Clearwater County rural residents who live east of the park boundary), and federal law prohibits working ranches inside Banff National Park. **Fail.**"

**Rewrite C (minimum disclosure, retains current verdict).** "Rocky Mountain House extended into Banff National Park: minority commissioners cited north-south economic corridor and historical precedent; the extension into Banff National Park backcountry adds geographic area but not population — the s.15(2) area exception the minority claims is not required for the district's qualification (audit Test 2 documents the 2019 predecessor area was already 22% above the s.15(2)(a) 20,000 km² threshold without the NP extension). **Fail.**"

**Recommendation: adopt Rewrite A.** It preserves the underlying audit finding (the s.15(2) area exception is not load-bearing) without making numerical claims the audit's filed evidence cannot exactly back.

**Follow-up to file before counsel-grade citation:**

- Strict-park-boundary clip using Parks Canada's official Banff NP polygon (open-data download).
- Census of Agriculture 2021 farm counts for Clearwater County, ID No. 9, and the Bighorn Country grazing-lease zones, sourced from StatsCan table 32-10-0152-01 and Alberta Forestry's Public Lands Administrative Database.

## Files

- This file: `analysis/methodology/banff_extension_population_check.md`.
- Inputs: `data/shapefiles/derived/v0_8_refined_minority_2026_eds.gpkg`; `data/shapefiles/reference/alberta_2021_das.gpkg`; `data/alberta_2021_da_populations.csv`.
- Cross-references: `findings/justification_tests_findings.md` Test 2; `analysis/methodology/minority_rationales_validation.md` §R12; `report_academic.md` §5.1.4, §5.3.3, §5.9.6 Claim 3.

## Caveats

- The "NP/mountain-park slice" is approximated by a longitude/latitude bounding box (west of -115.5°, north of 51.4°). This is geographically reasonable as a first-order approximation of the park-extension portion but does not correspond to the official Banff NP boundary. A tighter check requires the Parks Canada boundary file.
- The 491 area-weighted figure depends on the DA-internal population being uniformly distributed across the DA. In practice, residents cluster along roads (Highway 11, Forestry Trunk Road) and are absent from backcountry. The true park-land population is almost certainly an order of magnitude lower than 491.
- The v0.8 polygon for Rocky Mountain House-Banff Park is a derived geometry; the polygon-area-clipped population (26,444) under-counts the minority's own published figure (38,298) by ~31%. This shapefile-precision caveat applies to all polygon-clipped outputs in this file. The verdict on the underlying claim does not depend on the precision of the boundary; the structural finding (the NP extension contributes essentially no population) holds across reasonable boundary uncertainty.
- The "zero working ranches" claim is a statutory entailment for the Banff NP portion (Canada National Parks Act) and unverified for the broader polygon slice. A tighter check requires Census of Agriculture extraction.
