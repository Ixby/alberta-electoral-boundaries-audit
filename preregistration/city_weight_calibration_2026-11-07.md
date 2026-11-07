# How much do Alberta's boundary drawers weigh city boundaries? Calibrating the municipal weight on past maps (written before any new computation)

> Written 2026-11-07, about 9:20 AM Alberta Time (UTC−6), after downloading the historical maps and before computing anything on them. Unregistered and not blind: the split ratios of the 2019, majority and minority maps (Amendment 17 run log, §6) and every Lethbridge result today are known. Requested by the author on 2026-11-07 ("can we calibrate that?"). GitHub only; no OSF filing. Nothing here says whether any map is a gerrymander.

## The question

The municipality-aware redraws use a city-boundary weight W, which was set at 0.5 by matching the 2019 map. Here W is inferred separately for every human-drawn Alberta map available. That gives the range of weight Alberta's drawers have actually applied, and the Lethbridge regional test is then rerun across that range.

## Maps

| Map | Divisions | Source |
|---|---|---|
| 2003 commission (in force 2004-2008) | 83 | Government of Alberta GIS layer "Provincial Electoral Division - Historical 2003", 84 features |
| 2010 commission (in force 2012-2015) | 87 | Government of Alberta GIS layer "Historical 2010"; Elections Alberta's `EDs_Act2010_FINAL.zip` as a cross-check |
| 2017 commission (in force 2019-2023) | 87 | the 2019 boundaries already in the audit (`parent_ed_2019`) |
| 2026 commission majority and minority | 89 | official |
| 2026 panel | 91 | v3 |
| ¶167 | 91 | reconstruction |

Older maps (1996 and before) were not found as GIS files and are out of scope.

Layers were fetched from `geospatial.alberta.ca/titan/rest/services/boundary/goa_administrative_area/MapServer/{3,4,5}` on 2026-11-07 at about 9:16 AM Alberta Time. SHA-256: layer 3 (2017) `071e27fc…bc78`, layer 4 (2010) `ac5ef3f5…f8`, layer 5 (2003) `580a12ec…e21`, `EDs_Act2010_FINAL.zip` `4101a10c…26`.

## The measure

**R** is the share of the 169 municipalities split into more pieces than their population requires. It uses the definition from Amendment 17, §6:
- **Which municipalities:** 2021 municipalities other than Calgary and Edmonton that span at least 2 voting areas.
- **A piece:** at least 2% of the municipality's 2021 population.
- **Needed pieces:** ceil(population / (1.25 × average)).

Voting areas are placed by representative point.

**Limit, fixed now:** older maps are measured on 2021 municipalities and 2021 population, not on the boundaries and populations their commissions used. Cities have since annexed land and grown, so older maps' R is approximate.

## Calibration

The calibration chains use the tool that set W = 0.5 (`amendment17_chain_runs/tools/muni_calib.py`), unchanged: proposal epsilon 0.25, the surcharge W, 10,000 steps, and R as the mean over the second half.

| Districts | W values |
|---|---|
| 83, 87 | 0, 0.25, 0.5, 0.75, 1.0 |
| 89 | 0, 0.25, 0.75, 1.0, added to the existing 0.45, 0.55, 0.65 |
| 91 | existing 0, 0.10, 0.25, 0.45, 0.5, 0.55, 0.6, 0.7, 1.0 |

New calibration chains use indices 280-299, which are unused.

**Inference:** each map's implied W is read by linear interpolation on the curve for its number of districts. A map whose R is outside the curve's range is reported as below 0 or above 1, not extrapolated.

## Use

Rerun the Lethbridge regional city-aware redraw (`findings/hybrid_regions/regional_redraw.py`, same region, chains and reading rule) at the lowest and highest implied W among the commission-drawn maps: 2003, 2010, 2017 and the 2026 majority. The 2026 minority, the panel and ¶167 are not commission-adopted maps, so they are reported but do not set the range.

Report the panel's Lethbridge percentile at each W. Whichever W is used, the reading rule is the one in `preregistration/hybrid_regions_2026-11-07.md`, with the literature grounding in `findings/hybrid_regions/threshold_grounding.md` reported beside it.

**Signed:** Claude (acting as session agent), directed by Will Conner
