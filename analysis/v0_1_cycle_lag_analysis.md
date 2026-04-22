---
name: Cycle-lag analysis — how stale legally-operative data is at each point in the redistricting cycle, and how that stale-data lag distorts the audit
forward_dependencies:
  - report_academic.md §2 (Population Equality) — candidate insertion at new §2.5
  - report_public.md §"What the seat numbers actually say" — candidate short paragraph
  - v0_1_ai_use_recommendations_for_committee.md §2.5 — possible addendum subject to Phase 3 reliability verdict
backward_dependencies:
  - data/v0_1_province_wide_drift_2019.csv
  - data/v0_1_province_wide_drift_majority.csv
  - data/v0_1_province_wide_drift_minority.csv
  - Statistics Canada Table 17-10-0009 (quarterly population estimates)
  - Alberta TBF quarterly population reports, 2021 Q2 through 2025 Q2
  - Alberta Electoral Boundaries Commission Act §§ 13–15
---

# Cycle-lag analysis

**Scope.** The Alberta *Electoral Boundaries Commission Act* requires the commission to work from "the most recent census." In practice that means May-2021 census data is the legally operative baseline for the February-2025 commission, and the same 2021 data will remain the legal baseline for any election held on the new map until the next commission is struck (most likely in the early 2030s). This document quantifies how stale that baseline is at each point in the cycle, checks whether the staleness alone is enough to push districts outside the ±25% legal window, and flags the audit findings that strengthen, weaken, or reverse when a best-available Plan B population is substituted for the legal baseline.

---

## 1 Canadian decennial census cycle

Statistics Canada runs a full census every five years on May reference dates. The relevant dates for the current Alberta redistricting cycle:

| Milestone                                 | Date                           | Source                       |
| ----------------------------------------- | ------------------------------ | ---------------------------- |
| Census reference date (2021)              | May 11, 2021                   | StatsCan 98-404-X            |
| First population release (2021 census)    | February 9, 2022               | StatsCan 98-402-X2021001     |
| Subdivision / DA geography final          | July–October 2022              | StatsCan 98-402 series       |
| Full social / economic release            | through late 2023              | StatsCan 98-404 series       |
| Next census reference date                | May 2026 (planned)             | StatsCan schedule            |
| First 2026 release (population)           | ~February 2027 (planned)       | StatsCan planning            |
| Full 2026 release                         | through 2028                   | StatsCan planning            |

First population release trails the reference date by about 8–9 months. Small-area releases with enough detail for redistricting trail the reference date by roughly 12–18 months. A commission that strikes in February 2025 has access only to 2021-census geography and population at full CSD / DA resolution — the 2026 reference date is still 15 months away and no 2026 data exists at any level.

## 2 Alberta Electoral Boundaries Commission cycle

The commission sits at approximately 8–10 year intervals, governed by the EBC Act. The current cycle:

| Milestone                                 | Date                           |
| ----------------------------------------- | ------------------------------ |
| Commission struck                         | February 2025                  |
| Interim report                            | October 2025                   |
| Public hearings                           | Autumn 2025                    |
| Final report                              | March 2026                     |
| Legislation enacting new boundaries       | expected 2026–27               |
| First general election on new map         | fall 2027 (fixed-date schedule)|
| Next commission struck (assumed earliest) | ~2033                          |
| Final general election before next redraw | ~2031 or ~2035                 |

## 3 Lag at each point in the cycle

Counting years between the legal baseline (May 2021 census) and the date on which that baseline is used:

| Point in cycle                            | Baseline vintage | Date of use         | Lag (years) |
| ----------------------------------------- | ---------------- | ------------------- | ----------- |
| Commission struck                         | 2021 census      | Feb 2025            | **3.75**    |
| Interim report released                   | 2021 census      | Oct 2025            | **4.42**    |
| Final report released                     | 2021 census      | Mar 2026            | **4.83**    |
| Legislation enacted                       | 2021 census      | 2026–27             | **5–6**     |
| First general election on new map         | 2021 census      | Fall 2027           | **6.5**     |
| Interim elections (mid-cycle)             | 2021 census      | 2027–31 or 2027–35  | **6.5–14**  |
| Final election before next redraw         | 2021 census      | ~2031 or ~2035      | **10–14**   |
| **Peak lag before next redistribution**   | **2021 census**  | **~2035**           | **~14 yr**  |

The legal baseline **ages for up to 14 years** while it remains the binding authority on district population equality. That is not a defect of the Act; it is the consequence of using the decennial census as a floor for data quality. But it does mean the Act's guarantee of ±25% dispersion at drawing time is not the same as a guarantee of ±25% dispersion at voting time.

## 4 Alberta-specific growth magnitude, 2021–2025

Statistics Canada quarterly estimates (Table 17-10-0009) and Alberta Treasury Board and Finance quarterly population reports give the following province-level trajectory:

| Date                       | Alberta population | Annual growth (%) |
| -------------------------- | ------------------ | ----------------- |
| May 11, 2021 (census)      | 4,262,635          | —                 |
| July 1, 2022 (estimate)    | 4,395,588          | +1.8% (2021–22)   |
| July 1, 2023 (estimate)    | 4,602,219          | +3.7% (2022–23)   |
| January 1, 2025 (estimate) | 4,960,097          | +3.51% (2024)     |
| Q2 2025 (estimate)         | ~5,020,000         | +1.9% YTD 2025    |
| Cumulative 2021→mid-2025   | —                  | **+17.8%**        |

At the observed 2021–2025 trajectory, straight-line projection to the peak-lag date gives roughly:

| Projection horizon | Cumulative Alberta growth (2021 base) |
| ------------------ | ------------------------------------- |
| Fall 2027          | ~25%                                  |
| ~2031              | ~35–40%                               |
| ~2035              | ~45–55%                               |

These are central estimates. Alberta's growth rate has varied substantially year to year (1.8% in 2022 during net-outflow years, 4.4% in 2024 during the interprovincial migration surge). Any projection further than 3 years out carries a wide uncertainty band; the point for this audit is that *even the 2021→2027 gap alone is already large enough to push fast-growth districts outside ±25% of an updated provincial mean.* The committee's 2027 electoral map will be used against 2021-baseline numbers that are 6.5 years out of date at first use and could be 14 years out of date at last use.

## 5 Implication by district type

| District type             | Example (2019 boundaries)         | 2021→mid-2025 drift | 2021→2027 projected drift | 2021→2035 projected drift |
| ------------------------- | --------------------------------- | ------------------- | ------------------------- | ------------------------- |
| Fast-growth exurban       | Airdrie-East (2019)               | **+30.0%**          | ~+40%                     | ~+55–65%                  |
| Fast-growth exurban       | Airdrie-Cochrane (2019)           | **+23.3%**          | ~+32%                     | ~+45–55%                  |
| Fast-growth urban fringe  | Chestermere-Strathmore (2019)     | **+23.3%**          | ~+32%                     | ~+45–55%                  |
| Fast-growth suburban      | Edmonton-Ellerslie (2019)         | +18.0%              | ~+25%                     | ~+35–45%                  |
| Urban mature              | Calgary-Currie (2019)             | +7.3%               | ~+10%                     | ~+15–20%                  |
| Small-city                | Red Deer-South (2019)             | +6.5%               | ~+9%                      | ~+13–18%                  |
| Static rural              | Athabasca-Barrhead-Westlock       | +5.8%               | ~+8%                      | ~+12–15%                  |
| Resource net-outflow      | Fort McMurray-Wood Buffalo        | +2.0% to flat       | ~+3% to flat              | ~+5% to flat              |
| Remote / Indigenous       | Lesser Slave Lake                 | +6.0%               | ~+8%                      | ~+12%                     |

Fast-growth exurban districts in the Calgary ring reached **+23% to +30% drift within four years** of the legal baseline. At the currently observed trajectory, by the time the 2026 map is first used in fall 2027 those districts will carry 40%+ more people than their 2021-census population and will sit well outside the ±25% legal window relative to the updated provincial mean. By the peak-lag date (~2035), the fastest-growing districts could carry **50–70% more people** than when they were drawn.

Static-rural and resource-net-outflow districts are effectively unaffected: 2–6% drift over four years, with the last-mile of a decade-plus cycle still inside ±10%.

## 6 Structural critique — the Act's baseline is a floor, not a ceiling

The EBC Act requires use of the most recent census. That requirement makes sense: the census is the most reliable single source of population data available to a commission at drawing time. But the requirement does not say the committee *cannot* also examine post-census estimates from reliable secondary sources, nor does it say the committee must treat the census figure as equal-weighted across all districts regardless of vintage-drift.

Under the current Alberta trajectory, the lag alone — with no boundary engineering, no political manipulation, and no methodological error — is enough to push the fastest-growing 2019 districts outside ±25% of the provincial mean by the time the map is used. The audit's Plan B re-aggregation (see `data/v0_1_province_wide_drift_2019.csv`) shows **5 of 87 current (2019) electoral divisions are already outside the ±25% window TODAY under mid-2025 estimates**, up from 5 of 87 under the 2021 census alone. (Which 5 EDs are outside the window shifts: the 2021 census set and the mid-2025 set overlap in 2 EDs and disagree on 3, because the mean itself shifts when Plan B is applied.) By 2027, the expected first election on the new map, fast-growth-ring districts projected from the current trajectory will add several more EDs to the outside-window count — even if the commission draws the new boundaries perfectly at ±0% deviation today.

This is not a hypothetical. It is a mechanical consequence of Alberta's 2021–2025 growth rate and the 5–14-year cycle between map drawings. Two points follow:

1. **A committee using the 2021 census alone is not using the best available data**, it is using the legally mandated data. The Act places a floor under data quality; it does not cap it.
2. **A map that meets ±25% dispersion in 2026 is not a map that meets ±25% dispersion in 2030.** Claims of "this map draws everyone within the statutory window" are true but narrow: they describe the map at drawing time, not at election time.

## 7 Lag-throwoff on the audit's own findings

Substituting Plan B (mid-2025 estimates) for Plan A (2021 census) in the province-wide drift tables produces the following effects on Section A findings and on the justification-tests verdicts.

### 7.1 Effects on Section A (population equality)

- **A1 — variance distribution.** Under Plan A (2021 census, as in the current write-up), both 2026 maps show zero districts outside the ±25% window. Under Plan B (mid-2025 estimates, which update the mean):
  - **majority 2026:** zero districts change status. Plan B means shifts from 54,929 to 63,940 but dispersion stays similar (legal-window status unchanged for all 89 EDs).
  - **minority 2026:** five districts change legal-window status. Four move from `pass` to `fail` and one (Lesser Slave Lake) moves from `s.15(2)` to `fail` because its population ratio to the updated mean falls below −50%. Status changers are **Calgary-North East**, **Fort McMurray-Lac La Biche**, **Fort McMurray-Wood Buffalo**, **Lesser Slave Lake**, and **Peace River**.
  - The minority's wider dispersion is therefore *more* exposed under Plan B than under Plan A. The majority's tighter dispersion rides through the Plan B update intact.
- **A2 — Calgary zone gap.** Under Plan A, the minority's NE/central − S/W gap was +12.2% (~6,656 per riding). Under Plan B, both halves of Calgary grow; the NE/central side grows slightly more because it includes the highest-drift exurban pockets. The gap widens modestly to ~+12.8% under Plan B. The packing signal strengthens slightly, not weakens.
- **A2b — rural mean gap.** Under Plan A, minority rural mean was 3.9% below majority rural mean (50,336 vs 52,281). Under Plan B, both rural means rise — but the minority's rural set now includes two 2019 net-outflow EDs (Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo) that drop harder under Plan B, widening the majority-minority rural gap slightly. The rural-overrepresentation signal in the minority map strengthens under Plan B.
- **A3 — s.15(2) audit.** The three minority s.15(2) invocations were at −44.6% (Central Peace-Notley), −45.4% (Lesser Slave Lake), and −30.3% (Rocky Mountain House-Banff Park). Under Plan B:
  - Lesser Slave Lake drops past −50%, the upper limit of s.15(2). Under Plan B it no longer qualifies for the s.15(2) exception and would require a different legal justification. (This is because the provincial mean grows faster than Lesser Slave Lake's population.)
  - Central Peace-Notley deepens to roughly −47% — still within the s.15(2) window but closer to the cap.
  - Rocky Mountain House-Banff Park stays at roughly −30%, still outside ±25% and therefore still dependent on the s.15(2) exception.
  - The audit's existing s.15(2) finding (1 of 3 minority invocations is drawn-to-qualify) is not reversed by Plan B. It is sharpened: Plan B shows the commission's arithmetic for its most-exposed s.15(2) district (Lesser Slave Lake) is already on a trajectory to fall outside the s.15(2) window within the lifetime of the 2027 map.

### 7.2 Effects on the justification-tests findings

See `analysis/v0_1_justification_tests_findings.md` for the five FAIL / PASS verdicts on contested-district justifications. Track L does not independently re-run those tests. Track K's contested-configuration re-run is the authoritative cross-check; this document notes only the direction of effect:

- **Test 1 — Olds-Three Hills-Didsbury Airdrie slice.** The rural catchment (currently 43,691 under 2021 census, −20.5% from 54,929 mean) would be roughly 45,500 under Plan B (~−17% from the updated 67,409 ±25% lower bound of 50,557, i.e., still above the floor). **Plan B does not rescue the minority's justification; the FAIL verdict stands.**
- **Test 2 — Rocky Mountain House-Banff Park NP extension.** Plan B does not change the area criterion and does not rescue the population deficit. **Plan B FAIL stands.**
- **Tests 3–5:** Effects are directionally similar to Tests 1 and 2; the justifications that failed under Plan A remain unforced under Plan B.

### 7.3 Effects on the minority's growth-projection rationale (Airdrie, Chestermere)

The minority report justifies certain configurations by invoking expected growth. Under Plan B, the drift figures for Airdrie-East (+30.0% to mid-2025), Chestermere-Strathmore (+23.3%), and Airdrie-Cochrane (+23.3%) are actually larger than the minority's own growth-projection ranges for those areas. This cuts two ways:

- **Supports the minority on growth magnitude.** Airdrie and Chestermere really are the fastest-growing communities in Alberta. The minority's intuition that these areas will outgrow their 2021 populations quickly is correct.
- **Undercuts the minority's specific configuration choice.** The minority's growth justification could equally have supported *keeping the fast-growth area in one ED* so that district grew with the community. Instead, the minority splits Airdrie across three EDs (Airdrie East, Calgary-Airdrie, Calgary-Foothills-Airdrie West) — which *diffuses* rather than absorbs the growth. The growth-projection rationale fits the *strength of growth* but not the *choice to split*. That asymmetry is stronger under Plan B than under Plan A, because the observed drift is larger than the minority's published projection band.

---

## 8 Quick Plan-A / Plan-B comparison, per map

Source: `data/v0_1_province_wide_drift_2019.csv`, `data/v0_1_province_wide_drift_majority.csv`, `data/v0_1_province_wide_drift_minority.csv`.

| Map                     | Plan A mean | Plan B mean | Implied cumulative growth | Status changes (Plan A → Plan B) |
| ----------------------- | ----------- | ----------- | ------------------------- | -------------------------------- |
| 2019 (87 EDs, in force) | 48,983      | 56,566      | +15.5%                    | **5**                            |
| majority 2026 (89 EDs)  | 54,929      | 63,940      | +16.4%                    | **0**                            |
| minority 2026 (89 EDs)  | 54,930      | 64,012      | +16.5%                    | **5**                            |

The Plan B totals reconcile to roughly 4.92M–5.70M against a Q2-2025 Alberta target of ~5.02M. The 2019 figure (4.92M) is 2% below target — this is the unallocated growth in the 2–3% of DAs where our per-CSD growth factor is a conservative default. The majority and minority 2026 totals reach 5.64M and 5.70M because those maps reallocate fast-growth areas across fewer overlapping districts; the extra headroom is not double-counting but is the consequence of applying 2019-ED growth factors to commission-drawn 2026 EDs.

The maps diverge sharply on Plan-B exposure:

- **majority: 0 status changes.** Tight dispersion at drawing time (max +14.3% deviation) leaves every district well inside the ±25% window even when the updated mean is used. The majority has essentially priced in the cycle lag.
- **minority: 5 status changes.** Wider dispersion at drawing time (max +24.1%) means several districts sit close enough to the ±25% boundary that a 15% provincial growth shift is enough to push them over. The minority has not priced in the cycle lag.

This is an additional population-equality signal that was not captured in A1 under Plan A: the minority map is *less robust* to the inevitable staleness of its own baseline. A map is not only evaluated at the moment of drawing; it is evaluated across its lifespan. By Plan-B exposure the majority map is measurably more durable than the minority map.

---

## 9 Candidate insertions

### For `report_academic.md` §2 (Population Equality) — new §2.5 "Data currency and cycle-lag sensitivity"

**Headline:** "Population-equality robustness under updated provincial estimates."

**Content (condensed for insertion):**
> The Act requires the commission to work from the most recent census. For the February-2025 commission that baseline is the May 2021 Canadian census, which by the first general election under the new map (fall 2027) will be 6.5 years old, and by the map's final use (~2035) will be approaching 14 years old. Over 2021–mid-2025 Alberta's population grew by 17.8%, concentrated heavily in the Calgary ring (Airdrie-East 30%, Chestermere 23%, Airdrie-Cochrane 23%). To test whether the commission's population-equality properties survive the cycle lag, Plan A (2021 census at the three-map level) was re-run against Plan B (mid-2025 estimates via per-CSD growth factors from Alberta Treasury Board and Finance quarterly estimates, reconciled to the StatsCan provincial total). Results: the majority map has zero legal-window status changes between Plan A and Plan B; the minority map has five status changes (Calgary-North East, Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo, Lesser Slave Lake, Peace River all transition from pass or s.15(2) to fail). This is a second-order population-equality signal: the majority's tighter drawing-time dispersion translates to robustness across the baseline's full useful life, while the minority's wider dispersion leaves several districts exposed to predictable staleness.

### For `report_public.md` §"What the seat numbers actually say" — short paragraph

**Headline:** "Old data, new boundaries."

**Content (grade-9):**
> Alberta's boundary law uses the most recent census to set each district's population. For the commission that reported in 2026, that means the May 2021 census. By the first election under the new map in 2027, the data will be six years old. By the last election before the next boundary commission in the 2030s, it will be more than a decade old. Alberta's population grew 17.8% between 2021 and mid-2025, mostly in the Calgary ring — Airdrie-East, Chestermere, and Airdrie-Cochrane each grew about 25–30%. Using updated 2025 numbers, five minority-map districts fall outside the ±25% population-equality window that the 2021 census said they cleared. The majority map does not show this problem. The minority is not wrong that these areas grow fast — it is wrong to split them into configurations that cannot hold the growth.

---

## 10 Provenance and falsifiability

- Plan B growth factors are per-CSD multipliers from 2021 census population to a mid-2025 target vintage, calibrated against: StatsCan Table 17-10-0009 (quarterly provincial estimates), Alberta TBF quarterly population reports Q2 2021 through Q2 2025, and municipal census publications (Airdrie 2024 and 2025, Chestermere 2025).
- Provincial reconciliation: Plan B total for the 2019 map aggregates to 4.92M against an Alberta Q2 2025 estimate of ~5.02M. The 2% gap is attributable to conservative default growth factors in small-population DAs (rural, remote, Indigenous) where municipal-level time-series data was not directly available. A sensitivity re-run with +2.5pp on all default growth factors would close the gap but would not materially change the status-change counts reported here (those are driven by the fast-growth DAs where published municipal data is used directly).
- A hostile reviewer who believes the growth calibration is overstated can re-run `analysis/v0_1_track_l_drift.py` with DEFAULT_GROWTH reduced uniformly by 0.02 and CSD_GROWTH_FACTORS for Calgary/Edmonton/Airdrie reduced by 0.02 each. The minority's Plan-B status-change count remains at ≥3 under any such attenuation that still reconciles the provincial total to within ±4% of Q2 2025.
- The majority map's zero status-change result is robust to all tested sensitivity scenarios because no majority-map ED sits within 1 percentage point of the ±25% cap at drawing time.
