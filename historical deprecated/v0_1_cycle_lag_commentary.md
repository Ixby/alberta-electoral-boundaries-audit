---
name: Census-lag commentary — dataset construction + commission growth modelling
description: Commentary on how the 2021-census / 2024-TBF / 2035-retirement cycle lag manifests in audit dataset construction and constrains commissions' ability to model forward growth. Companion to cycle_lag_analysis.md (§12 statutory-interpretation focus) and report_academic.md §3.3 (robustness focus). This file adds the construction and forward-modelling angles.
type: reports
---

# Census-lag commentary — dataset construction and commission growth modelling

**Companion to:** `analysis/cycle_lag_analysis.md` (statutory-interpretation + numerical-robustness focus), `report_academic.md §3.3` (robustness summary), and `analysis/reports/act_amendment_proposal.md` (legislative reform proposal).

**This file adds two angles that the existing material does not cover in detail:**

1. **The "three-vintage sandwich."** How the 4–14-year gap between the commission's nominal data basis and the boundaries' final retirement manifests in the *dataset-construction* work any auditor attempting to reproduce commission arithmetic has to do.
2. **The growth-modelling trap.** What a 6–14-year gap does to commissions trying to predict the electorate that will actually vote under the boundaries they are drawing — specifically for fast-growing metropolitan-fringe cities and slow-declining rural areas.

---

## 1. How the lag manifests in building the audit dataset

Any empirical audit of the 2026 proposals has to reconcile data products that sit at three different vintages simultaneously. Call this the **three-vintage sandwich**.

| Input | Vintage | Purpose in the audit | Source |
|---|---|---|---|
| 2021 Dissemination Area geometry | 2021 Q2 | The atomic spatial unit for DA-overlay population recovery (Phase 4B) | Statistics Canada `lda_000a21a_e.zip` |
| Per-DA population | 2021 Q2 census | Population attached to each DA geometry | StatsCan 98-401-X2021006 |
| Commission variance tables | July 2024 TBF estimate (Office of Statistics and Information) | The operative per-ED population against which the commission scored variance | Majority Report p. 29; Minority Report p. 296 |
| Provincial control total | Q2 2024 StatsCan postcensal (Table 17-10-0009) | The quota denominator | 4,888,723 |
| Mid-2025 TBF estimate | 2025 Q2 | Cycle-lag robustness re-run | TBF Economic Dashboard |
| 2023 Voting Area geometry | 2023 election day | VA substrate for Phase 4C spatial attribution | Elections Alberta `2023Boundaries_VAs.zip` |
| 2023 Statement of Vote | 2023 election day | Per-poll votes | Elections Alberta XLSX |

The three-vintage problem:

- **DA geometry (2021) vs ED geometry (2026) vs population mirror (2024).** A DA is a ~400-person polygon drawn for the 2021 census; a 2026 proposed ED is a polygon drawn by the commission in 2025–26. The audit overlays the former inside the latter and sums populations. The population values attached to the DAs are from 2021 — so the sum is **2021 population of 2026-shaped territory**. The commission's published value for that same ED is its **2024 estimate of 2026-shaped territory**. The ratio of these two is *not* the 14.69 % provincewide growth factor; it depends on how much of the ED's territory lies in fast-growth Calgary ring vs slow-growth rural area. **The Phase 4F hardstop failures documented in `data/INTEGRITY_STATUS.md` (81/86 majority EDs, 87/89 minority EDs) are partly a real DPG-fidelity problem, and partly a cycle-lag artifact from applying a flat growth scalar to a regionally-heterogeneous population surface.**

- **VA-geometry (2023) vs ED-geometry (2026).** Phase 4C attributes 2023 Voting Area polygons to 2026 EDs. Between 2023 and 2026 Elections Alberta updated some VAs (merges, splits, renames). The audit uses the 2023 VA polygons as the spatial substrate because they are the unit that has votes attached — but a few VAs have been restructured in the intervening ~2 years. Those changes are small but non-zero and are unrecoverable without a 2026 VA shapefile release.

- **Votes (2023) vs boundaries (drawn 2025, taking effect 2027+).** The audit's B1–B6 partisan-bias metrics apportion **2023 votes** through **2026 boundaries**. That apportionment is the best available proxy for how partisan bias would operate if 2023-era voter geography persisted, but the actual 2027 electorate is 4-6 years past the 2021 census basis. For fast-growth cities (Airdrie, Chestermere, Leduc) this gap is the difference between a district that contains the voters the commission modelled and one that contains ~30 % more voters by the first election it governs.

The audit's published numbers therefore carry a compounded vintage disclosure: *2021 census geometry × 2023 voter distribution × 2024 population estimate × 2025 growth extrapolation*. The §3.3 cycle-lag robustness test re-runs the key counts under a mid-2025 TBF substitution and finds the directional verdicts stable, but the absolute magnitudes move by low-single-digit percentage points on some EDs and more than 50 % on a handful of fast-growth special cases.

**Practical consequence for reproduction:** an auditor rerunning this audit in 2028 against the 2026 census (when released, ~2028 Q3) will get noticeably different per-ED population deltas than the 2021-based pipeline produces today, even if the DPG geometry is unchanged. That is not a bug; it is a property of the underlying statutory framework that mandates a decennial census while allowing mid-cycle estimates for variance measurement.

## 2. What a 6–14-year lag does to commissions trying to model forward growth

Alberta's redistribution cycle, counted from most-stale input to boundary-retirement date:

| Event | Date | Years from 2021 census |
|---|---|---|
| 2021 decennial census (Commission's statutorily-mandated baseline) | 2021 Q2 | 0 |
| Commission formed | 2025 Q1 | ~4 |
| Commission tables final report | March 2026 | ~5 |
| Boundaries take effect (first election under the new map) | 2027 general | ~6 |
| Mid-cycle election | 2031 general (if called on schedule) | ~10 |
| Boundaries retire (next commission tabled, typical 7-year cycle) | 2033–34 | ~12 |
| Last election under the boundaries (if cycle runs long) | 2035 general | ~14 |

**The statutorily mandated data basis (the decennial census) is thus between 4 and 14 years stale for every election actually governed by the boundaries it informed.** The mid-cycle estimates commissions use to partially correct this (Alberta's OSI uses TBF estimates for the post-2021 years) are themselves re-basings of the 2021 anchor using birth / death / migration records, not independent counts — they drift from the true population at rates that depend on model quality and on whether inter-provincial migration is being handled well.

### Where the lag hits hardest

**Fast-growth metropolitan-fringe cities.** Airdrie grew from 74,100 (2021 census) to 92,500 (TBF 2025) to somewhere above 100,000 by the time the 2026 boundaries take effect in 2027. The commission's minority map splits Airdrie four ways to "absorb growth"; the majority map splits it two ways and lets those districts become oversized. Neither approach is wrong on its face — they're different bets about the growth trajectory. But **both bets were placed using 2024 population data on a boundary that will govern elections through at least 2031**, and the doubling-in-a-decade rate observed in the Calgary ring means any 2024-basis district in this zone will be ±30 % of its quota by cycle end.

The same story applies at smaller scale to Chestermere, Cochrane, Okotoks, Beaumont, Leduc, Spruce Grove, Fort Saskatchewan, and Sherwood Park — a ring of high-growth municipalities around Calgary and Edmonton where the 4-year gap between commission data basis and first-election date already moves the quota by 10–15 %, and the 14-year gap to boundary retirement moves it by 40 %+ on current rates.

**Slow-decline rural areas.** The mirror-image problem. Peace River, Central Peace-Notley, Lesser Slave Lake, and several northern constituencies have essentially flat or slightly declining populations. Commissions invoke §15(2) (the ±25 % special-rural exception) to keep these districts viable. The §15(2) eligibility ratio the commission computes against 2024 population shifts under mid-2025 data — `analysis/cycle_lag_analysis.md` documents Lesser Slave Lake's s.15(2) qualifying ratio dropping past −50 % of provincial mean under the mid-2025 substitution. If the ratio drift persists into 2028–30, a §15(2) protection established under 2024 data may be unavailable by the time the boundary is litigated — a commission has locked in a legal basis for the district that does not survive its own cycle.

**Indigenous communities and on-reserve populations.** The decennial census chronically under-counts on-reserve populations (undercount estimates in the 3–10 % range per cycle). A commission using the raw census as its basis treats these communities as smaller than they actually are for district-sizing purposes; a commission using TBF estimates inherits the TBF's own treatment of reserves (which varies). The 6–14-year lag amplifies this: a reserve that grew 20 % between 2021 and 2031 but was counted 10 % short at the 2021 anchor spends its entire cycle under-represented relative to its true population.

### Modelling options commissions have — and don't have

Commissions can choose:

1. **Census-only (the statutory baseline).** Maximally conservative, most legally defensible, most stale.
2. **Census-plus-estimate blend (Alberta 2026 approach).** Less stale but introduces a statutory-interpretation question about the §12(5) "in conjunction with" clause. Creates a legal attack vector.
3. **Projection-based ("mid-cycle midpoint").** Choose the projected population at the midpoint of the boundaries' effective window. Statistically sound (minimises mean squared deviation from actual populations across the cycle) but not permitted under current Act §12.
4. **Composite basis with published provenance.** `analysis/reports/act_amendment_proposal.md` proposes this: TBF primary + StatsCan tie-breaker at ±2 % + AHCIP + CRA T1 cross-check + CEO as certifying authority. Would require Act amendment.

No Canadian commission currently uses option 3. BC (2023), Saskatchewan (2022), and Federal (2022) used option 1. Alberta 2026 used option 2.

**The audit's position on this is deliberately narrow:** we do not argue the commission's choice was wrong, because it is a policy choice the Act permits. We do document (1) that the choice has real numerical consequences for which districts drift out of ±25 % during the cycle, (2) that the statutory question about §12(5) is unresolved, and (3) that a future amendment to §12 formalising a composite basis would reduce the attack surface on both sides. See §3.3, Appendix E.8, and `analysis/reports/act_amendment_proposal.md`.

## 3. Proposed paper insertions

### Candidate expansion of `report_academic.md §3.3`

The existing §3.3 treats cycle-lag as a robustness-of-verdict property. The additional angle this commentary develops — that the three-vintage sandwich materially affects the Phase 4B pop-overlay pipeline itself, not just the robustness post-processing — is worth a paragraph:

> **Dataset-construction consequences of cycle lag.** The Phase 4B DA-overlay pipeline sums 2021 census populations inside 2026 DPG polygons. The commission's published per-ED populations are 2024 TBF estimates for the same 2026 territory. The ratio of these two values is *not* a clean scalar: Alberta's 14.69 % provincial growth between 2021 and 2024 was distributed unevenly (Calgary ring grew faster than average; some rural areas slower), so flat-scalar adjustments introduce a structural bias into Phase 4B's per-ED validation deltas. The 81/86 majority and 87/89 minority hardstop failures documented in `data/INTEGRITY_STATUS.md` are therefore a composite signal: real DPG transcription error plus cycle-lag growth heterogeneity. Disentangling the two without official 2026 shapefiles is not tractable from public data; the §4.1.4 sunset clause binds the audit to recomputation if shapefiles release, at which point real geometry error would be distinguishable from cycle-lag artifact.

### New subsection for `report_academic.md §9` (procedural) — "§9.X Cycle-lag as a structural audit-policy question"

> **Cycle-lag as a policy question beyond the audit's scope.** The commission operates under Act §12, which mandates a decennial-census baseline. The boundaries the commission draws will govern elections 4–14 years after that baseline. For fast-growth municipalities around Calgary and Edmonton this lag moves per-ED quotas by 10–40 % during the cycle; for slow-declining rural districts it erodes §15(2) protection ratios. The audit's verdicts are robust to the choice within the current Act (§3.3 cycle-lag robustness test); the audit does not, however, resolve whether §12 itself should be amended to allow a composite basis that reduces the attack surface. The legislative-reform proposal in `analysis/reports/act_amendment_proposal.md` sets out one possible composite-basis amendment. That proposal is offered as a policy contribution, not a finding.

## 4. References

- Existing cycle-lag analysis: `analysis/cycle_lag_analysis.md`
- §3.3 robustness summary in `report_academic.md`
- Appendix E.8 in `report_academic.md`
- Plan B cross-check: `analysis/reports/plan_b_cross_check.md`
- Act §12 amendment proposal: `analysis/reports/act_amendment_proposal.md`
- Commission source provenance: `analysis/methodology/commission_source_provenance.md`
- Phase 4F validation: `data/v0_1_validation_deltas.csv` + `data/INTEGRITY_STATUS.md`
