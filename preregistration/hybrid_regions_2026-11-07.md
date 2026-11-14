# Neutral regional redraws wherever the panel's map has hybrid ridings, city-blind and municipality-aware (written before any computation)

> Written 2026-11-07, about 6:50 AM Alberta Time (UTC−6), before any chain below has been run. Unregistered and **not blind**: signal F's city-blind result for the south is known (`findings/six_signals/README.md`). Requested by the author on 2026-11-07 ("run it, and any where there's hybrid ridings"). GitHub only; no OSF filing. Nothing here is a finding on whether any map is a gerrymander.

## Ballots

**All ballots are the primary figures here** (`va_polygons_all_2023_ballots_primary.gpkg`, which matches the official 2023 results). The author's view (2026-11-07) is that election-day-only figures are noise. They miss about half of 2023's ballots and turn 49 UCP / 38 NDP into 57 / 30 on the 2019 map. Election-day figures are kept in the output files for completeness and are not used in any reading below. This applies to this plan only. The registered steps still use election-day ballots, and changing that would be an OSF amendment, which is the author's call.

## Hybrid ridings

A division on the panel's map is a hybrid if 5% to 95% of its 2021 population lives in one city of 20,000 or more (a CSD of type CY), the rest outside it. Found before this plan:
- Airdrie-East
- Calgary-Bow-Springbank
- Calgary-West-Springbank
- Chestermere-Strathmore
- Edmonton-Enoch
- Edmonton-Nisku
- Fort Saskatchewan-Vegreville
- Grande Prairie-Wapiti
- Leduc-Beaumont
- Lethbridge-Cardston
- Lethbridge-Little Bow
- Lethbridge-Taber-Warner
- Medicine Hat-Brooks
- Medicine Hat-Cypress
- Morinville-Sturgeon
- Spruce Grove

## Regions

One region per city with a hybrid:

| Region | Rule |
|---|---|
| Lethbridge | the panel's southern group, as in signal F |
| Calgary and Edmonton | the city's hybrid divisions, plus every panel division sharing a boundary with one |
| Each other city: Airdrie, Chestermere, Fort Saskatchewan, Grande Prairie, Leduc and Beaumont together (one division holds both), Medicine Hat, St. Albert, Spruce Grove | every panel division holding 2% or more of the city, plus every division sharing a boundary with one of its hybrids |

Every other division is held fixed.

## Chains

The same as signal F: ReCom on the region's voting-area graph, 2021 population, ±25% of the region's mean, a random starting plan within the band, the first 1,000 steps discarded, and drand seeds (salt `regional_<region>_<variant>_<chain>`). Detached pieces of the region are held with their nearest region area.

| Region | Chains |
|---|---|
| Lethbridge | 4 × 50,000 steps, municipality-aware only (the city-blind run is signal F) |
| Every other region | 2 × 25,000 steps for each variant |

**The variants:**
- **City-blind:** population and contiguity only.
- **Municipality-aware:** ReCom's region surcharge on 2021 CSDs at weight 0.5, the audit's set C setting. Spanning trees cross municipal boundaries last, and cuts prefer them.

## What is recorded and compared

For every plan:
- **Where the city's NDP voters land:** the share in seats the NDP wins, in seats it loses by under 10 points, and in seats it loses by more.
- **How many pieces:** the number of districts holding at least 2% of the city.
- **NDP seats** in the region.

The panel's configuration is placed against each variant as percentiles. So is the commission majority's, where its divisions cover exactly the same voting areas as the region.

**Reading:**
- A configuration is unusual for a variant if it lies beyond the 95th percentile, or below the 5th, on the share of the city's NDP votes in seats lost by 10 points or more, on all ballots.
- The municipality-aware variant is the closer match to the Act's s.14(b), so where the two variants disagree, both are reported and the difference is the finding.

**Signed:** Claude (acting as session agent), directed by Will Conner
