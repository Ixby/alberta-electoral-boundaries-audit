# Plan: does the neutral maps' population basis matter? (2026-11-07)

**Unregistered. Written before computing.** Not blind: the persistent misses it asks about (for example Calgary-Airdrie) are already known.

**Question.** The neutral maps balance districts on 2021 census population. The panel and the commission balanced on the province's 2024 estimates. If some regions grew faster than others between 2021 and 2024, a neutral map drawn on 2021 figures gives those regions fewer seats than one drawn on 2024 figures. Then some gaps between the real maps and the neutral maps would come from the population basis, not from where the lines were drawn.

**Data.**
- 2021 census population by voting area (`pop_2021` on the voting-area graph; the ensembles' basis).
- The Office of Statistics and Information's July 2024 municipal estimates (`data/osi/`), by 2021 census subdivision (CSD).
- The panel's published division populations (`data/iap/iap_app7_populations.csv`), used for the validation check.

**Method: a municipal-growth basis.** Each voting area's 2021 population is multiplied by its CSD's growth factor (2024 estimate ÷ 2021 census). A voting area in a CSD with no usable estimate gets its census division's rural growth factor. If that is not available either, it gets the province's factor.

This is the same municipal-level information the failed small-area rebuild used. That rebuild failed only at the scale of single divisions inside cities (`findings/osi_rebuild/`). Here the factor is used only at the regional level, where uniform growth inside a city is a smaller error. The plan says so, and reports the validation below rather than assuming it.

**Measures:**
1. **Seat entitlement by region, on each basis:** the region's population share × 91. Regions:
   - Calgary;
   - Edmonton;
   - the Calgary ring (Airdrie, Chestermere, Cochrane, Okotoks, Rocky View County, Foothills County);
   - the Edmonton ring (St. Albert, Sherwood Park/Strathcona County, Spruce Grove, Stony Plain, Leduc, Beaumont, Fort Saskatchewan, Parkland County, Sturgeon County, Leduc County);
   - other cities of 20,000 or more;
   - everything else.

   The entitlement shift is the 2024 figure minus the 2021 figure.
2. **Validation:** the growth basis's total for each of the panel's divisions (reconstruction v3), against the panel's App. 7 figure. Report the mean and largest absolute error. This shows how far the basis can be trusted at division level. It is a check on the basis, not a pass/fail gate for measure 1.
3. **Real maps on both bases:** for the majority, minority and panel maps, report the population MAD and the largest deviation on 2021 and on the growth basis. Also report how many divisions are outside ±25% on each.
4. **Is the shift in the right places?** Correlate each region's entitlement shift with the gap between the panel's seat count there and the neutral maps' median count (set D, 91 districts). Report this only if the region-level seat counts can be computed from committed outputs. Otherwise state that they cannot.

**Decision rule, fixed now:**
- If no region's entitlement shift reaches 0.5 seats, the population basis cannot account for a whole-seat difference in any region, and the neutral maps' 2021 basis stands as is.
- If one or more regions shift by 0.5 seats or more, the result is reported as a limit on every comparison in that region. A rerun of set D on the growth basis is then proposed (not launched here: it needs a new chain set, and memory is committed to the Amendment 12 replays).

**Outputs:** `findings/population_basis/` (script, JSON, README).

**Wording:** nothing here says whether any map is a gerrymander. A basis difference explains where the neutral maps differ, not why a line was drawn.
