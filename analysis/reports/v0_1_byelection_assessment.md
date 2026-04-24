---
name: Alberta provincial byelection assessment (2019-2026) — Track S
description: Acquires every Alberta provincial byelection held 2019-01-01 to 2026-04-22, assesses methodological usefulness for the boundaries audit, and judges whether incorporating byelection data strengthens any existing finding. Honest verdict: the 2022-2025 byelections are not a usefully additive cross-election baseline for the audit's RT3 stability test, and only one (Olds-Didsbury-Three Hills, June 2025) is materially informative for a contested-configuration finding.
forward_dependencies:
  - report_academic.md — §3.5 cross-election paragraph (proposed footnote-grade insertion)
  - report_public.md — no change recommended
backward_dependencies:
  - data/v0_1_alberta_byelections_2019_2026.csv — byelection vote data
  - analysis/scripts/v0_3_monte_carlo_ci.py — RT3 framework this assessment tests against
  - analysis/scripts/v0_1_cross_election_rural_baseline.py — 2015/2019/2023 rural baseline
  - analysis/v0_1_fortification_a1_a5.md §A1 — the CI-crosses-zero concern this track was to address
---

# Byelection assessment

## Phase 1 — What was acquired

Six byelections held between 2019-01-01 and 2026-04-22, covering six distinct 2019-boundaries electoral divisions. Data saved to `data/v0_1_alberta_byelections_2019_2026.csv`.

| Date | Riding | Reason | Winner | UCP share | NDP share | Turnout |
|---|---|---|---|---|---|---|
| 2022-03-15 | Fort McMurray-Lac La Biche | Goodridge resigned to run federally | Brian Jean (UCP) | 63.64% | 18.51% | 23.99% |
| 2022-11-08 | Brooks-Medicine Hat | Frey resigned to seat Premier Smith | Danielle Smith (UCP) | 54.51% | 26.74% | 35.51% |
| 2024-12-18 | Lethbridge-West | Phillips resigned (personal) | Rob Miyashiro (NDP) | 44.91% | 53.35% | 36.06% |
| 2025-06-23 | Edmonton-Ellerslie | Loyola resigned to run federally | Gurtej Singh Brar (NDP) | 38.06% | 50.84% | 24.50% |
| 2025-06-23 | Edmonton-Strathcona | Notley stepped down | Naheed Nenshi (NDP) | 13.60% | 82.28% | 32.00% |
| 2025-06-23 | Olds-Didsbury-Three Hills | Cooper left for Washington role | Tara Sawyer (UCP) | 61.12% | 19.98% | 38.80% |

No other byelections were held in the window. Calgary-Elbow, vacated by Schweitzer in August 2022, was left unfilled through the 2023 general — Smith declined to call it. No Chestermere-Strathmore byelection was held. No post-2025 byelections have been scheduled as of 2026-04-22.

**Sources:** Elections Alberta byelection reports for the 2022 pair and 2024 Lethbridge-West; Wikipedia pages for each byelection (cross-checked). Full 2025 vote counts are from Wikipedia's per-byelection pages; Elections Alberta had not yet posted the 2025 report as of the acquisition date.

## Phase 2 — Methodological assessment

### Signal strength (turnout ratio)

| Riding | Byelection turnout | General turnout | Ratio |
|---|---|---|---|
| Fort McMurray-Lac La Biche | 23.99% | 58.25% (2019) | 0.41 |
| Brooks-Medicine Hat | 35.51% | 65.78% (2019) | 0.54 |
| Lethbridge-West | 36.06% | 61.77% (2023) | 0.58 |
| Edmonton-Ellerslie | 24.50% | 56.24% (2023) | 0.44 |
| Edmonton-Strathcona | 32.00% | ~63% (2023, imputed) | 0.51 |
| Olds-Didsbury-Three Hills | 38.80% | 64.17% (2023) | 0.60 |

Every byelection drew less than 60% of the prior general turnout. Fort McMurray-Lac La Biche and Edmonton-Ellerslie dropped to roughly two-fifths. A Monte Carlo that weighted byelection votes equally with general-election votes would overweight the preferences of the one-in-three voters who bothered to show up. Any honest integration has to discount byelection weight by the turnout ratio, and even then the composition of who turns out is itself a selection effect.

### Anomaly flags

**Fort McMurray-Lac La Biche (2022)** — Brian Jean is a former Wildrose leader and long-standing regional figure. The -2.7 pp UCP dip and -6.0 pp NDP dip both reflect a low-information midterm with a returning local name. Not generalizable as a partisan signal.

**Brooks-Medicine Hat (2022)** — Premier Smith's home riding within a week of her swearing-in. A party leader running in a safe seat draws unique candidate-specific swings; the +9.6 pp Alberta Party surge (Barry Morishita is the former Brooks mayor) and the +8.9 pp NDP gain are personality-driven, not structural. Not generalizable.

**Lethbridge-West (2024)** — Miyashiro held the seat for the NDP with near-identical share (-0.6 pp). John Middleton-Hope is the former Lethbridge police chief and former city councillor, which inflates UCP share locally. The closest thing to a "normal" byelection in the set, but still candidate-driven.

**Edmonton-Ellerslie (2025)** — NDP share collapsed -10.9 pp without a party-leader candidate. The Liberal and Alberta Party got a combined 7.2%, suggesting a fragmented non-UCP vote and possibly voter reaction to Loyola's federal move. Not structural.

**Edmonton-Strathcona (2025)** — Leader's seat contest; Nenshi gained +2.6 pp on Notley's +80% share. UCP ran Darby-Rae Crouch without significant investment (13.6%, down from 17.3%). Very clearly anomalous: this is a performative byelection where the UCP did not contest seriously.

**Olds-Didsbury-Three Hills (2025)** — Most interesting case. UCP share fell -14.2 pp (75.3% → 61.1%). The separatist Republican Party of Alberta took 17.7% at first contest. This is either a signal of genuine UCP erosion in rural Alberta, or a safe-seat byelection protest vote. Without a subsequent general election, we cannot distinguish.

### Overlap with contested 2026 configurations

Six byelections, mapped to the minority 2026 configurations flagged in v0_2_packing_cracking_analysis.py:

- **Fort McMurray-Lac La Biche** → minority preserves this as a direct rename. Not in the audit's contested-configuration list (the Fort McMurray area is not flagged as packed/cracked in either proposal).
- **Brooks-Medicine Hat** → minority renames to "Medicine Hat-Brooks". Not in contested list.
- **Lethbridge-West** → minority absorbs part of Lethbridge-West into three new EDs: Lethbridge-Fort MacLeod-Crowsnest Pass (blend), Lethbridge-Cardston (blend), Lethbridge-East (blend with Lethbridge-East). The minority Lethbridge reconfiguration is NOT in the audit's packing/cracking signature list but is a significant boundary change.
- **Edmonton-Ellerslie** → preserved as direct in both proposals. Not contested.
- **Edmonton-Strathcona** → preserved as direct in both proposals. Not contested.
- **Olds-Didsbury-Three Hills** → minority renames to "Olds-Three Hills-Didsbury". **This is a flagged minority configuration** in the audit (the minority map includes it in its s.15(2) rural-catchment rationales; it appears in `v0_1_justification_test_inputs.csv` and is on the audit's minority-contested-configuration list).

**One of six** (Olds-Didsbury-Three Hills) sits in contested-configuration territory. Zero of six sit inside the Airdrie/Cochrane/Chestermere/Red Deer/St. Albert/Rocky Mountain House-Banff Park minority configurations. The byelection coverage of the audit's specific contested geographies is very thin.

## Phase 3 — Impact on existing findings

### Per-riding partisan shift vs 2023 general

| Riding | UCP delta | NDP delta | Direction |
|---|---|---|---|
| Fort McMurray-Lac La Biche | -2.7 pp | -6.0 pp | Both down, Other up |
| Brooks-Medicine Hat | -6.2 pp | +8.9 pp | NDP gain, UCP loss |
| Lethbridge-West | +2.4 pp | -0.6 pp | Stable (small UCP gain) |
| Edmonton-Ellerslie | +1.2 pp | -10.9 pp | UCP gain, NDP collapse |
| Edmonton-Strathcona | -3.7 pp | +2.6 pp | NDP gain |
| Olds-Didsbury-Three Hills | -14.2 pp | +1.2 pp | UCP collapse to Republican |

Three ridings show UCP erosion (Brooks-MH, Strathcona, ODTH); two show NDP erosion (FMLLB, Ellerslie); one is stable (Lethbridge-West). No directionally consistent partisan shift across the byelection set.

### Aggregate effect on minority-majority asymmetry

The audit's 2023-based minority-majority EG asymmetry is -0.58 pp at 70/30 urban weight (minority more UCP-favorable). The 338 Canada April 2026 polling replication produces the same 1-seat structural asymmetry (v0_1_338canada_riding_level.md). If byelection data replaced 2023 votes in the six byelection ridings:

- **Fort McMurray-Lac La Biche** is safe UCP under both 2023 and the 2022 byelection; swap does not flip the seat or meaningfully change EG contribution.
- **Brooks-Medicine Hat** (mapped to Medicine Hat-Brooks in minority) is safe UCP under both; no seat flip.
- **Lethbridge-West** is safe NDP under both 2023 and the 2024 byelection; under minority's Lethbridge reconfiguration the blend uses Lethbridge-West as input, but the byelection reinforces the 2023 NDP-safe verdict (same direction, same magnitude within 1 pp).
- **Edmonton-Ellerslie** — NDP share dropped to 50.8% from 61.8%. Still NDP-safe, no flip. UCP contribution to EG would move slightly.
- **Edmonton-Strathcona** — NDP super-safe under both. Slight increase in wasted NDP votes (packing further), which would widen the 2019-map EG slightly but leave both 2026 maps unchanged.
- **Olds-Didsbury-Three Hills** — UCP dropped from 75.3% to 61.1%. Still UCP-safe (margin 41 pp over NDP, 44 pp over Republican). No flip under any 2026 configuration.

**Zero seat flips** under either proposal if byelection votes replaced 2023 votes in these six ridings. The asymmetry change would be on the order of 0.05-0.15 pp — well below the Monte Carlo CI width of ±2 pp and swamped by modeling uncertainty.

### Would byelections tighten the A1 CI?

The v0_3 Monte Carlo CI of [-3.04, +0.76] pp crosses zero because modeling choices (urban weight, rural baseline, per-hybrid jitter) generate 2-3 pp of asymmetry spread. Byelection data does not address any of these three sources of uncertainty:
- Urban weight applies to hybrid districts; none of the six byelection ridings are hybrid in either 2026 map (Lethbridge-West is absorbed into three new minority EDs, but the 2023 vote data for Lethbridge-West already feeds the blend).
- Rural baseline applies to the ex-rural portions of hybrid districts; byelections provide per-riding signal, not a rural NDP share.
- Per-hybrid jitter is a structural modeling choice independent of any vote input.

**Verdict: byelections do not tighten the A1 CI.** The CI-crossing-zero is a modeling-uncertainty problem, not a vote-input-uncertainty problem.

### Would byelections serve as a third RT3 cross-election baseline?

The audit's RT3 cross-election stability test uses 2015, 2019, 2023 provincial general elections. These three elections share:
- Full provincial turnout (56-66% each).
- All 87 EDs contested by both UCP (or PC+WRP equivalents) and NDP.
- Boundaries-stable pairing for 2019/2023 (pre-2017-commission 2015 boundaries are harmonized by ED-name heuristic).

The six 2022-2025 byelections fail three of the RT3 preconditions:
1. **Coverage.** Only 6 of 87 EDs (6.9%) have byelection data. The audit's RT3 framework uses province-wide rural NDP share, which a 6-riding subset cannot produce.
2. **Turnout representativeness.** Byelection turnout runs 40-60% of general turnout, with different composition (older, more partisan voters). Treating a byelection as a third baseline alongside two general elections is apples-to-oranges.
3. **Candidate-specific anomalies.** Five of six byelections have obvious candidate-specific drivers (Smith, Jean, Nenshi, Miyashiro, Cooper's Republican challenger). Cross-election stability tests assume "normal" partisan inputs; byelections systematically violate this.

**Verdict: byelections are too sui generis to count as a third RT3 baseline.** A hostile reviewer would rightly reject a three-baseline RT3 that mixed general elections with byelections.

## Phase 4 — Recommendation

### On incorporation as a third RT3 baseline

**No.** Byelection data does not satisfy the coverage, turnout-representativeness, or candidate-normalcy preconditions that the 2015/2019/2023 triad satisfies. Adding byelections as a third RT3 cross-election dimension would weaken the audit by substituting a sparse, candidate-driven, low-turnout dataset for the rigor of the general-election baseline. The honest move is to not incorporate.

### On specific contested-configuration findings

**Olds-Didsbury-Three Hills (June 2025 byelection) is the only byelection that lives in contested-configuration territory.** The minority 2026 proposal's "Olds-Three Hills-Didsbury" is on the audit's flagged list. The June 2025 result (UCP -14.2 pp, Republican +17.7%, turnout 38.8%) does not contradict the audit's finding about the minority's justification for this configuration. If anything, it marginally supports the audit's skepticism about rural-catchment justifications: a "safe" rural UCP seat can show 14 pp swings in a single byelection cycle, which cuts against the minority's argument that packed rural EDs are structurally stable enough to warrant their boundary choices. But this is a soft observation, not a finding-strengthening signal. A footnote in §3.5 or §3.9 (rural catchment rationale) is the right level of coverage. Not a dedicated section.

**No other byelection materially informs any contested-configuration finding.** Fort McMurray-Lac La Biche, Brooks-Medicine Hat, Edmonton-Ellerslie, Edmonton-Strathcona, and Lethbridge-West all sit outside the flagged minority configurations.

### On 338-validation extension

The 338 Canada pipeline validates the audit by reallocating April 2026 per-riding projections through the majority and minority crosswalks. A similar reconciliation could use byelection actuals as a model-accuracy check: did the 338 April 2026 snapshot match the June 2025 byelection actuals in Olds-Didsbury-Three Hills, Edmonton-Ellerslie, Edmonton-Strathcona? This is a narrow, mechanical accuracy check — not a boundary-audit finding. It would strengthen the 338 validation pipeline's confidence in polling-based per-riding projections, which is downstream of the audit's main claims. Recommend: **flag as a side-project, not integrate into the audit.** A sub-agent can compute 338-vs-byelection Pearson r in about 30 minutes against `data/v0_1_338canada_per_riding_87seat.csv` and the byelection CSV.

### On integration level

**Recommended: footnote in §3.5 of `report_academic.md`.** No change to §1, no change to `report_public.md`, no new RT baseline, no §3 rewrite.

## Proposed insertion — `report_academic.md` §3.5

Drafted as a footnote-grade paragraph for the §3.5 cross-election stability discussion. Parent session applies.

> **Byelection coverage in the 2022-2025 window.** Alberta held six provincial byelections between the 2019 and 2023 general elections and in the 2023-2026 interval: Fort McMurray-Lac La Biche (2022-03-15), Brooks-Medicine Hat (2022-11-08), Lethbridge-West (2024-12-18), and Edmonton-Ellerslie, Edmonton-Strathcona, and Olds-Didsbury-Three Hills (all 2025-06-23). These byelections are not incorporated into the audit's RT3 cross-election stability test for three reasons. First, their coverage is sparse (6 of 87 EDs, 6.9%), which precludes the province-wide rural baseline computation the RT3 framework uses. Second, byelection turnout ran 40-60% of prior general turnout, and byelection voter composition is known to skew older and more partisan; this violates the "normal partisan inputs" assumption the three general elections jointly satisfy. Third, five of the six byelections have obvious candidate-specific drivers (Premier Smith in her home riding, Jean's regional incumbency, Nenshi's leader contest, Miyashiro's continuity with Phillips' voters, Cooper's replacement facing a separatist Republican challenger), which cross-election stability tests presume absent. The one byelection that touches a contested minority configuration is Olds-Didsbury-Three Hills (June 2025), which sits in the minority's proposed "Olds-Three Hills-Didsbury" district. The UCP's -14.2 pp share drop and the Republican Party of Alberta's 17.7% first-contest showing do not change the audit's directional verdict on rural-catchment configurations; they marginally support the audit's skepticism that "safe" packed rural EDs are structurally stable enough to justify the minority's boundary choices, but the byelection is too sui generis to upgrade this from an observation to a finding. Full data: `data/v0_1_alberta_byelections_2019_2026.csv`; assessment: `analysis/reports/v0_1_byelection_assessment.md`.

## Proposed insertion — `report_public.md`

**None.** The public reader's intuition does not change if byelection data is mentioned. The audit's headline claims (structural differences in A1/A2/A3, C4 community splits) are not affected by byelection evidence. A public-reader paragraph would add complexity without changing the takeaway. Recommend: no insertion in the public report.

## Honesty check

Track S was set up with an explicit honesty clause ("if byelection data is not a usefully additive source, say so"). Byelection data is *not* a usefully additive source for the audit's main findings. The Olds-Didsbury-Three Hills byelection is the only data point that touches contested territory, and even its signal is candidate-contingent (Cameron Davies is a known separatist figure; his 17.7% is an issue-specific protest vote, not a partisan baseline shift). The audit's A1 CI-crosses-zero concern is a modeling-uncertainty problem that byelections cannot address. The correct recommendation is a §3.5 footnote — nothing more.

## Summary for parent

- **Byelection count:** 6. Fort McMurray-Lac La Biche (2022), Brooks-Medicine Hat (2022), Lethbridge-West (2024), Edmonton-Ellerslie (2025), Edmonton-Strathcona (2025), Olds-Didsbury-Three Hills (2025).
- **Contested-configuration overlap:** 1 of 6 (Olds-Didsbury-Three Hills, sits in minority's flagged Olds-Three Hills-Didsbury configuration).
- **RT3 strengthening verdict:** No. Byelections fail coverage, turnout, and candidate-normalcy preconditions for cross-election baseline inclusion.
- **A1 CI tightening potential:** None. The CI-crosses-zero issue is a modeling-uncertainty problem (urban weight, rural baseline, per-hybrid jitter), not a vote-input problem. Byelections cannot address any of the three sources.
- **Recommended integration:** Footnote in `report_academic.md` §3.5 only. No new RT baseline, no public-report change, no new analysis section. Data and assessment saved for audit-trail completeness.
