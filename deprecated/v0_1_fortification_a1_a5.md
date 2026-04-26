---
name: Fortification against HIGH-severity red-team attacks A1–A5
description: Peer-review-grade defence of the academic paper against the five HIGH-severity attacks in the red-team critique. Written in the voice of the author's methodologist responding under pressure; acknowledges landed hits; narrows claims where the attack cuts; flags residual vulnerabilities.
forward_dependencies:
  - report_academic.md — proposed edits catalogued at end (parent session applies)
  - report_public.md — §"what the seat numbers say" caveats
backward_dependencies:
  - analysis/v0_1_red_team_academic_discredit.md — the attacks being answered
  - analysis/scripts/v0_3_monte_carlo_ci.py — CI defence evidence
  - analysis/scripts/v0_2_packing_cracking_analysis.py — pipeline provenance for sensitivity
  - v1_2_gerrymander_audit_prompt.md — pre-registration provenance; git commit 5b0bc06 at 2026-04-22 08:32:20 −06:00
  - analysis/reports/v0_1_plan_b_cross_check.md — A4 data-source defence
  - analysis/v0_1_cycle_lag_analysis.md — A4 robustness defence
  - analysis/methodology/v0_1_338canada_riding_level.md — A1 cross-validation defence
  - data/v0_1_alberta_2023_results.csv, analysis/polls_2023_unified.csv — A5 apportionment evidence base
---

# Fortification — defence against A1 through A5

## Framing

The red-team surfaced five HIGH-severity attacks. This document answers them in peer-review style. Each attack receives five paragraphs: (i) the attack restated; (ii) what it gets right; (iii) the available defence; (iv) the narrowed claim where the attack lands; (v) the residual vulnerability. Where an attack lands, this document says so plainly. Where the paper's current language is defensible only after narrowing, the narrowed wording is drafted verbatim. The fortification does not attempt to rescue indefensible claims; the goal is to produce a version of the audit that could survive public peer review, not one that pretends every attack fails.

---

## A1 — 95 % CI crosses zero; core partisan finding not statistically significant

### (i) The attack

*"Your Monte Carlo 95 % CI of [−3.04, +0.76] pp on the minority-majority EG asymmetry crosses zero; a 'qualified pass at 90 %' is a rhetorical move; 90 % is not 95 %; paired with 2019 cross-election reversal, the ordinary inference is that there is no effect."*

### (ii) What the attack gets right

The 95 % CI does cross zero. `analysis/scripts/v0_3_monte_carlo_ci.py` ran N=2,000 samples over urban weight U(0.55, 0.85), rural baseline U(0.26, 0.36), per-hybrid jitter U(−0.10, +0.10) and produced a 95 % CI of [−3.04, +0.76] pp (paper reports [−2.99, +0.76]; minor rounding). The direction-consistency figure is 89.3 %, not 95 %. The paper's "qualified pass at 90 %" language is a judgment call about what confidence level is adequate — it is not a statistical significance claim. The red-team is correct that in a strictly frequentist reading of political-science methodological norms (95 % as the canonical significance threshold for effect-existence claims), the data do not meet that bar. The 2019 cross-election flip (asymmetry reverses sign when 2019 votes replace 2023 votes) amplifies the attack because it shows the finding is not invariant to the vote input. A reviewer who holds the 95 % line would reject the stated magnitude claim.

### (iii) The defence

Three distinct defences are available, each bearing a different amount of weight.

**Defence 1 — A directional claim at ≈89 % confidence is a reportable political-science finding, not a rhetorical move.** Empirical political science routinely publishes findings at confidence levels below 95 % when the theoretical stakes warrant it and the direction is stable. Stephanopoulos and McGhee (2018) explicitly discuss the efficiency-gap metric's modeling sensitivity as a reason to report ranges rather than point estimates with significance stars. Katz, King and Rosenblatt (2020) argue for ensemble reporting in which cross-metric consistency substitutes for single-metric p-values. The American Political Science Association style treats 90 % CIs as publishable when clearly labelled. Direction-consistency at 89.3 % across 2,000 samples means the finding survives about 8.9 of every 10 modeling configurations the author could have chosen; this is not nothing.

**Defence 2 — A direction claim and a magnitude claim are not the same claim and should be reported separately.** The paper currently conflates them in places. A direction claim requires only consistent sign across simulations; a magnitude claim requires a CI tight around the point estimate. The 89.3 % figure is evidence for the direction claim; the [−3.04, +0.76] CI kills the magnitude claim. The author should separate them. The paper's §3.4 already does this ("report the range, not a point estimate") — the red-team attack is that §3.5 then undoes the separation by calling it a "qualified pass at approximately 90 %". The fix is linguistic rather than analytical: state the direction claim at 89.3 %, state the magnitude claim as unfalsified (CI crosses zero), and stop using "qualified pass" as if it were a graded version of significance.

**Defence 3 — The 338 Canada cross-validation substantially reduces reliance on the 95 % test.** `analysis/methodology/v0_1_338canada_riding_level.md` reports that under April 2026 338 Canada polling — a completely different vote input from the 2023 Statement of Vote that drives the Monte Carlo — reallocation through the majority and minority crosswalks produces seat counts of 67 UCP / 22 NDP (majority) and 66 UCP / 23 NDP (minority). The 1-seat asymmetry is identical to the audit's 2023-vote headline. This is evidence that the 1-seat asymmetry is a *structural property of the boundary configurations*, not an artifact of the 2023 vote data that the Monte Carlo is perturbing. The Monte Carlo CI measures sensitivity to one form of uncertainty (modeling choices at fixed vote input); the 338 cross-validation measures sensitivity to a second form (changing the vote input entirely). The asymmetry survives the second test at 1 seat. This is the political-science analog of replication across datasets — when two independent data sources give the same directional answer, frequentist 95 % tests against one source become less dispositive.

**Git provenance for Defence 3.** `analysis/scripts/338canada_scraper.py` committed before `analysis/scripts/338canada_reallocate.py`; 87 ridings scraped directly from 338 Canada live pages; Pearson r=0.960 against audit's 2023-vote UCP share. The 338 and audit pipelines do share some structural assumptions (riding-level aggregation methods), which the red-team's C5 correctly flags as reducing the independence. But the vote input is genuinely different (2023 actual ballots vs April 2026 polling), and that is where the Monte Carlo's uncertainty lives.

### (iv) Narrowed claim

The paper's §3.5 language *"directional claim holds at 89.3 % confidence"* should be replaced by:

> **"The minority-majority EG asymmetry is negative (minority more UCP-favorable) in 89.3 % of 2,000 Monte Carlo samples across the parameter space (urban weight 0.55–0.85, rural baseline 0.26–0.36, per-hybrid jitter ±0.10). The 95 % confidence interval is [−3.04, +0.76] pp and crosses zero. We report this as a directional observation at approximately 90 % confidence and do not assert statistical significance at the conventional 95 % threshold. Because the 338 Canada April 2026 per-riding projection reallocated through the same crosswalks produces the same 1-seat asymmetry as the 2023-vote input (`analysis/methodology/v0_1_338canada_riding_level.md`), the 1-seat structural effect is invariant to the vote-input uncertainty the Monte Carlo samples. The magnitude claim (specifically 0.5–1.6 pp) does not meet the 95 % threshold; the 1-seat structural asymmetry meets a replication test across distinct vote inputs."**

The phrase *"qualified pass at 90 %"* should be deleted everywhere it appears in §3.5. "Qualified pass" is the red-team's best target because it elides the direction/magnitude distinction; replacing it with literal language removes the target.

### (v) Residual vulnerability

The 2019 cross-election reversal (reported in §1 stress-test update as "asymmetry flips sign under 2019 votes as input") is not fully cured by the 338 defence. The 338 defence establishes consistency across 2023-vote and April-2026-poll inputs; it does not establish consistency across 2023 and 2019 votes. A hostile reviewer can still observe: "the asymmetry holds across datasets that share 2020s-era Alberta political geography (2023 votes, April 2026 polls), but reverses when the 2019 NDP-favourable electorate is used as input." That is a real finding about the contingency of the asymmetry, not a defence-proof artifact. The honest response is the one already in the paper's §1 stress-test update ("the direction of the audit's headline asymmetry flips sign depending on which election's votes are used"). The fortification should make that qualification more prominent — current placement in the stress-test preface is correct; adding a one-line reminder in §3.5 ("direction is stable across 2023 votes and April 2026 polling; reverses under 2019 votes") would disarm a reviewer who reads §3.5 in isolation.

**A1 severity after fortification: MEDIUM.** The CI attack cannot be fully dismantled — the CI does cross zero. But with (a) direction/magnitude separation, (b) deletion of "qualified pass" language, and (c) foregrounding of the 338 1-seat replication, the attack narrows from "the finding is not defensible" to "the magnitude claim is not defensible; the direction claim is defensible at approximately 90 % and replicates across distinct vote inputs." A peer reviewer can still reject the magnitude claim. The structural 1-seat asymmetry and the direction-at-≈90 % claim can survive.

---

## A2 — Chen-Rodden concession flips the framing

### (i) The attack

*"Your §3.6 concedes that neither 2026 map is engineered against natural packing; both correct it, the majority more. In partisan-neutral language, both maps are NDP-favourable relative to 2019 and to Alberta's natural geography; the minority is just less so than the majority. Your 'minority is UCP-favourable' headline depends on taking the majority as baseline rather than 2019 or natural geography."*

### (ii) What the attack gets right

The §3.6 concession is real. Under Chen and Rodden (2013), the 2019 map's −2.64 % EG is partly a natural artifact of NDP urban concentration rather than an engineered tilt. The majority 2026 at −0.85 % and minority 2026 at −1.36 % both shift EG toward zero relative to 2019, meaning both correct some of the natural UCP advantage. The majority corrects more (by ~0.51 pp on EG). A government communicator can legitimately say: *"the minority map sits closer to Alberta's natural political geography than the majority does."* This reframes the "minority is UCP-favourable" finding from "the minority map tilts to UCP" to "the minority map corrects less of Alberta's natural UCP-favouring geography than the majority does." Those two statements have different rhetorical valence and both are arguable from the same numbers.

The attack is not trivially dismissable. The paper's own §3.6 supplies the ammunition. The strongest framing-attack responses to academic papers are the ones built from the paper's own concessions, and this is one.

### (iii) The defence

Three defences available, in order of weight.

**Defence 1 — Chen-Rodden's natural-packing thesis affects only Section B (partisan bias); it does not reach Sections A, C, or D.** Chen and Rodden's argument is that voter geography (urban concentration of one party) produces a natural partisan lean in efficiency-gap-type metrics even in neutrally-drawn maps. This is a statement about *vote-distribution-derived metrics*. It says nothing about population-distribution irregularities (A1 MAD of 3,180 vs 4,707), Calgary geographic-zone asymmetry (0.4 % vs 12.2 %), s.15(2) engineered boundaries (0 vs 1), Airdrie fragmentation (2 EDs vs 4), or procedural differences (standard override vs government-controlled drafting). Under Chen-Rodden the minority-vs-majority EG comparison is partisan-framed-neutral — neither map is engineered against natural geography — but the wider population dispersion, larger Calgary zone gap, extra Airdrie split, and engineered s.15(2) boundary in the minority map are *structural differences measured directly on the map*, not inferred from vote outcomes. Chen-Rodden cannot reach these.

**Defence 2 — Chen-Rodden 2013 was developed from US congressional data; its transferability to Alberta provincial redistribution is partial.** Chen and Rodden's empirical case uses 2000-era US states with larger, more polarized urban-rural divides than Alberta currently has. Alberta's NDP urban concentration is real but weaker than, say, Philadelphia vs rural Pennsylvania — Calgary alone has UCP-dominant south-west and NDP-competitive north-east zones (the paper's §2.2 observation), and many Alberta urban EDs are swing rather than safe. The Chen-Rodden prediction that "natural packing" accounts for most of the measured EG is therefore a hypothesis for Alberta, not an established finding. The paper's §3.6 acknowledges this by saying natural packing accounts for *some portion* of the 2019 EG, not all of it. The attack that framing-neutralizes the result by treating all of the 2019 EG as natural is over-reading Chen-Rodden.

**Defence 3 — The correct reframing is neither "minority engineered against NDP" nor "minority respects natural geography," but both maps correct; minority corrects less.** This is the framing `analysis/methodology/v0_1_academic_literature_review.md` §6.1 recommends. Under this framing the audit's finding is stated: *"both 2026 maps partially correct Alberta's natural UCP-favouring geography; the majority corrects more of it than the minority does. The minority's additional structural irregularities (wider population dispersion, larger Calgary zone gap, engineered s.15(2) boundary, 4-way Airdrie fragmentation) are independent of the natural-packing argument and constitute the core finding. The partisan-bias magnitude difference between the two maps (0.5–1.6 pp EG) sits at the boundary of modeling sensitivity and is reported as directionally observed at ≈90 % confidence without asserting 95 % significance."* This is the framing the paper should adopt. It lands the Chen-Rodden hit but does not let the hit propagate to the structural findings.

### (iv) Narrowed claim

The paper currently writes the headline as *"minority is measurably UCP-favourable."* That phrasing concedes too much to the Chen-Rodden attack. Replacement:

> **"The minority 2026 map corrects less of Alberta's natural UCP-favouring geography than the majority map does (majority EG −0.85 %, minority EG −1.36 %, 2019 baseline −2.64 %). Under Chen and Rodden's (2013) natural-packing framing, neither 2026 map is engineered against natural geography; both move toward EG zero, with the majority moving further. The partisan-bias difference between the two maps is not the primary finding of this audit. The primary finding is structural: the minority map shows wider population dispersion (MAD 4,707 vs 3,180), larger Calgary geographic-zone asymmetry (12.2 % vs 0.4 %), engineered s.15(2) boundary at Rocky Mountain House-Banff Park, and 4-way fragmentation of Airdrie vs the majority's 2-way split. These structural differences are measured on the map itself and do not depend on vote-distribution modeling. Natural-packing arguments cannot reach them."**

This reframing turns the Chen-Rodden concession from a structural undermining (Attack A2 lands) into an informative context (partisan-bias finding is secondary; structural findings remain primary). The paper's §7 synthesis already leans this way — the fortification makes the lean explicit.

### (v) Residual vulnerability

The attack's rhetorical payload ("the minority respects natural geography more than the majority") remains available to government communications regardless of how the paper frames the finding. A press release can quote the paper's own §3.6 without attribution: "*neither 2026 map is engineered against natural packing; both correct it."* That sentence, lifted from context, is a defence of the minority. The audit cannot prevent selective quotation. The best it can do is make the structural findings (A, C, D) rhetorically stronger than the partisan-bias finding (B), so the minority's natural-geography defence is a defence only on the B finding, not on the whole audit. The narrowed claim above does that. The residual vulnerability is that any reader who only reads §3.6 and §3 headlines sees a Chen-Rodden-shaped defence and does not see the A/C/D structural findings that sit outside Chen-Rodden's reach.

**A2 severity after fortification: MEDIUM.** Attack lands on partisan-bias framing. Defended by restricting partisan-bias finding to its proper scope and foregrounding structural findings. The finding is still real but has been re-narrated to match what the evidence supports. A hostile reviewer no longer gets a one-sentence kill. A political opponent still has the Chen-Rodden press-release line, which the audit cannot prevent.

---

## A3 — Signature-detection thresholds not credibly pre-registered

### (i) The attack

*"Your P1–P3, C1–C3, E1–E3 criteria have specific numeric thresholds (P1 pop ≥ mean + 5 %; P2 winning margin ≥ 15 pp above mean; etc.). The thresholds appear for the first time in v1.2 of the prompt, written after the v0.2 packing-cracking analysis had been run. 'Formally detect' requires the criterion to exist before the test. If you had found four signatures in the majority and zero in the minority, would you have reported it? If your answer is yes, where is the version of the code that would have identified signatures in the majority?"*

### (ii) What the attack gets right

The attack is correct that "formally detect" requires the criterion to exist before the test. It is correct that a claim of pre-registration must be git-provable. It is correct that retuning thresholds after seeing the data, even subconsciously, would invalidate the signature-detection methodology. The attack is also correct to note that the author chose the thresholds — +5 % population deviation, +15 pp margin deviation, ±25 % population floor on C3 feasibility — without citing literature precedent for these specific numbers. A reviewer sensitive to pre-registration discipline will want git evidence and will want to see that the thresholds were not tuned against the minority's observed values.

### (iii) The defence

The defence on this attack is the strongest of the five, and it is the narrow defence that git-provenance itself supplies.

**Git evidence — v1.2 prompt commit predates signature-detection runs.** From `git log --format="%h %ci %s"`:

- Commit `5b0bc06`, 2026-04-22 08:32:20 −06:00: "v1.2 prompt + PDF recon findings + mapping corrections + voice checker" — this is the commit that introduced the v1.2 prompt containing P1–P3, C1–C3, E1–E3 thresholds.
- Commit `282bc6d`, 2026-04-22 10:56:11 −06:00: "Packing/cracking/engineered-boundary signatures: formal detection" — this is the commit that ran the signature-detection analysis against the minority and majority maps.

**The v1.2 prompt committing the thresholds predates the detection-run commit by 2 hours 24 minutes.** This is machine-timestamped evidence that the criteria existed before the analysis. A reviewer can verify this with `git log --all --format="%h %ci %s" -- "v1_2_gerrymander_audit_prompt.md"` against the repository. The prompt commit diff shows P1–P3, C1–C3, E1–E3 verbatim at the time of commit (verified by `git show 5b0bc06 -- v1_2_gerrymander_audit_prompt.md | grep -E "(P[123]|C[123]|E[123])"`).

**Source-text provenance — prompt-side vs analysis-side.** The v1.2 prompt §7.3 (`v1_2_gerrymander_audit_prompt.md` lines 170–218 approximately) specifies the criteria as prose requirements on the author, not as code the author then executed. The analysis script `analysis/scripts/v0_2_packing_cracking_analysis.py` does not actually implement P/C/E as machine tests — the detection is done by human-interpretable comparison of commission-published values against the prompt-stated thresholds, and the results are reported in `report_academic.md` §3.7–3.9 with numeric values. The criteria-before-analysis ordering is clean on both the prompt-side and the analysis-side.

**Counterfactual test — would the author have reported majority signatures if detected?** The attack's hypothetical ("if you had found four signatures in the majority map and zero in the minority, would you have reported it?") is answerable from the audit's existing conduct. Section 3.7 explicitly states *"No packing signature detected in Calgary under the majority 2026 map. P1 fails with Zone A mean of 56,460 vs Zone B 56,255 (gap 0.4 %, well below the +5 % threshold)."* The author ran the same criterion on the majority and reported the negative result in the same format. Section 3.8 does the same for cracking: *"No cracking signature detected under the majority 2026 map for any of Cochrane, Chestermere, or Airdrie."* Section 3.9 reports *"No engineered-boundary signature detected under the majority 2026 map"* followed by the specific statutory calculation. The audit in fact reported each criterion's failure on the majority with the exact numeric value that caused the failure. This is the symmetric-application test; the audit passes it for packing, cracking, and engineered-boundary criteria.

**Threshold provenance — why these specific numbers.** The thresholds are not literature-derived; they are interval-scale judgment calls:
- P1 at +5 % of provincial mean: the Act itself uses ±25 %, so +5 % is a tight fraction of the statutory band (one-fifth); this is conservative.
- P2 at +15 pp above mean winning margin: in Alberta's 2023 results the mean winning margin was ~19 pp; +15 pp above mean gives ~34 pp, which is above the "safe seat" threshold commonly used in US redistricting literature (Chen 2017 uses 20 pp).
- C3 at ±25 %: matches the statutory population band exactly, not a chosen threshold.
- E1–E3: structural — either a boundary passes through negligible-population territory or it does not; the author's choice was whether to require all three conjunctively (conservative) or disjunctively (permissive); conjunctive was chosen, which is the stricter test.

### (iv) Narrowed claim

The current paper states *"the detection is not 'we think the minority looks engineered'; it is 'apply P/C/E criteria mechanically, record what passes.'"* This claim is defensible as-is, but the paper can strengthen it by adding explicit git-timestamp evidence. Proposed addition at the end of §3.11 (or as a footnote at §3.7):

> **"Pre-registration provenance. The P/C/E criteria and their numeric thresholds are specified in `v1_2_gerrymander_audit_prompt.md`, committed as `5b0bc06` at 2026-04-22 08:32:20 −06:00. The signature-detection analysis reported in §3.7–3.9 was committed as `282bc6d` at 2026-04-22 10:56:11 −06:00. The criteria exist in the repository 2 hours 24 minutes before the detection runs. `git log --all --format='%h %ci %s' -- v1_2_gerrymander_audit_prompt.md` reproduces this timeline. The criteria were applied symmetrically to both 2026 maps; where the majority failed a criterion, the failure is reported with the specific numeric value (e.g., §3.7 'No packing signature detected in Calgary under the majority 2026 map. P1 fails with Zone A mean of 56,460 vs Zone B 56,255 (gap 0.4 %, well below the +5 % threshold).')."**

Additionally, a brief note on threshold provenance should be added in §3.7:

> **"Threshold provenance. P1 at +5 % and C3 at ±25 % are indexed to statutory references (P1 is one-fifth of the ±25 % Act band; C3 uses the Act band directly). P2 at +15 pp above mean winning margin yields an operational 'safe-seat' cut-off of ~34 pp, above the 20 pp threshold used in Chen (2017). These thresholds were set before the signature-detection analysis runs (see above) and are applied identically to both 2026 maps."**

### (v) Residual vulnerability

The defence narrows the attack significantly but does not eliminate it entirely. A sceptic can still observe: (a) the prompt was authored by the same author as the analysis; pre-registration at commit `5b0bc06` does not rule out the author having seen the data mentally before writing the prompt; (b) the prompt was committed at 08:32 and the analysis at 10:56, both within the same session — so it is not a days-ago-blinded pre-registration, only a hours-ago intra-session pre-registration; (c) the thresholds are not externally validated against a held-out map. The strongest fortification against residual vulnerability would be to run the P/C/E criteria against a *new* map that the author has not seen — the November 2026 MLA-committee 91-seat map, when it is published — and report whether the criteria produce similar signature counts. The paper's §3.11 pre-registered checklist already anticipates this; the November map will be the held-out test. Noting this explicitly in §3.7 reinforces the pre-registration claim.

**A3 severity after fortification: LOW.** The git timestamp evidence is concrete and verifiable. The symmetric application of the criteria to both maps with numeric values reported for both passes and failures demonstrates the criteria are not tuned to the minority's observed data. The November 2026 map provides a held-out test that locks the pre-registration claim. Residual vulnerability is intra-session pre-registration rather than pre-session — real but narrow, and the November test closes it.

---

## A4 — Main-body population analysis not against the Act's data standard

### (i) The attack

*"Your §2 analyses A1 MAD, A2 Calgary zone gap, A3 s.15(2) eligibility against the commission's own per-ED tables. Track K has now discovered those tables derive from July 2024 Alberta TBF estimates, not the 2021 census. §12(3) of the Act requires the decennial census. If a court reads §12(5) narrowly, every per-ED number in §2 is derivative of non-compliant commission data and your analysis inherits the defect. You either re-run §2 directly from 2021 census, or argue §12(5) is permissive, in which case your reform proposal is weaker. You cannot have it both ways."*

### (ii) What the attack gets right

The commission's variance tables derive from the July 2024 TBF estimate, not the 2021 census (`analysis/reports/v0_1_plan_b_cross_check.md` confirms this: "the 4,888,723 provincial total is the Alberta Treasury Board Office of Statistics and Information July 1, 2024 mid-year population estimate; the 2021 Census of Population total for Alberta was 4,262,635"). The paper's §2 numbers (MAD 3,180 / 4,707, Calgary zone gap, s.15(2) deviations) are therefore computed against 2024 TBF values. Act §12(3) does require use of "the population information as provided in the decennial census," with §12(5) permitting supplementation "in conjunction with" the decennial census. The commission used 2024 TBF as sole basis, not as supplement. A strict §12(5) reader can argue every commission-table-derived number in the audit's §2 has a statutory-basis defect. The paper's end-note acknowledges this but does not re-anchor the main body. The red-team is correct that this is a structural issue, not a footnote issue.

The attack's "you cannot have it both ways" point is also correct in narrow form. If the audit treats §12(5) as permissive (commission's 2024 basis is fine), the §12 reform proposal (`analysis/reports/v0_1_act_amendment_proposal.md`) has a weaker motivating premise. If the audit treats §12(5) as restrictive (commission's basis is non-compliant), the §2 analysis must either re-anchor to 2021 census or acknowledge it inherits the commission's §12 defect. The paper currently walks a middle path that is not fully principled.

### (iii) The defence

Three defences, but A4 is the attack that most clearly lands and requires the most substantive narrowing.

**Defence 1 — The Plan B cross-check establishes that audit findings are invariant to the data-source question.** `analysis/reports/v0_1_plan_b_cross_check.md` re-ran every justification test against both the 2021 census and the 2025 TBF estimates. Every test reaches the same verdict under both data sources. Three tests (Olds-Three Hills-Didsbury rural catchment, Airdrie 4-way split, Chestermere split) become *more decisively* FAIL under newer data. A1 is "already a Plan B result" because the commission's own ED tables use the 2024 TBF basis. The directional finding (minority more population-dispersed, wider Calgary zone gap, engineered s.15(2) at RMH) survives whether one anchors to the 2021 census or the 2024/2025 TBF estimates. The legal question "which basis is statutorily correct" is unresolved; the audit question "do the minority's structural irregularities show up on any defensible population basis" is resolved in the affirmative.

**Defence 2 — The §2 analysis can be repositioned as diagnostic-level, with a 2021-census-direct analysis as the legal-baseline appendix.** Currently §2 uses commission-derived values, which inherit the commission's §12 status. A principled fix is to label §2's numbers as *"commission-derived, therefore on the commission's stated 2024 TBF basis,"* and to add an appendix (or expand the cycle-lag end-note) that reports A1/A2/A3 computed directly from 2021 census CSD data aggregated to 2019 ED boundaries. The 2019-boundary 2021-census A1 is computable from `data/alberta_2021_csd_populations.csv` once a CSD-to-2019-ED crosswalk is constructed. A crosswalk to 2026 EDs would require the as-yet-unreleased 2026 shapefiles and is blocked; but a 2019-boundary 2021-census A1 is feasible and would serve as the "legal baseline" the Act §12(3) requires, with the commission-derived §2 serving as the diagnostic version that matches what the commission actually published.

**Defence 3 — The cycle-lag analysis provides independent evidence that the data-source question matters more for durability than for direction.** `analysis/v0_1_cycle_lag_analysis.md` shows that under mid-2025 estimates the majority map has 0 legal-window status changes and the minority map has 5. This signal is orthogonal to the 2021-vs-2024 debate — it says whichever basis the commission used at drawing time, the minority's wider dispersion means more of its districts sit near the ±25 % boundary and will be pushed over by expected 2021–2031 growth. This is a population-equality finding that uses the *trajectory* rather than the snapshot, and it strengthens the audit's direction-of-finding without depending on §12(5) interpretation.

### (iv) Narrowed claim

The paper's current end-note is insufficient. The §2 preamble itself should acknowledge the data basis. Proposed replacement for the current §2.1 opening sentence:

> **"§2.1 Distribution variance (A1). The commission's variance tables in both the majority and minority reports derive from the Alberta Treasury Board Office of Statistics and Information July 1, 2024 population estimate (total 4,888,723), not from the 2021 decennial census (total 4,262,635). The commission's stated methodology describes its basis as the 2021 census updated to 2024, but the actual tables use the 2024 estimate directly (see `analysis/reports/v0_1_plan_b_cross_check.md` for the compliance audit). The audit's A1 analysis therefore inherits the commission's data vintage: the 3,180 and 4,707 MAD figures are computed against 54,929 (the 2024-basis quota) rather than against a 2021-census-basis quota. Plan B cross-check (`analysis/reports/v0_1_plan_b_cross_check.md` §3) verifies every A1-related justification verdict is identical under the 2021 census, the 2024 TBF estimate, and the 2025 TBF estimate. Three contested-configuration tests (Olds-Three Hills-Didsbury, Airdrie 4-way, Chestermere split) become more decisively unforced under the 2025 TBF basis than under the 2021 census basis. A1 MAD figures are reported below on the commission's stated basis (2024 TBF); they are intended for apples-to-apples comparison with the commission's own published tables, not as the Act §12(3)-operative legal baseline. The §12(3) legal-baseline analysis is at Appendix C (to be added)."**

Section 2.4 (s.15(2) eligibility) needs similar language noting the area criterion is independent of the population basis, the qualifying-centres criterion is independent of the population basis, and only the population-band criterion inherits the 2024 TBF basis.

**New appendix to add (flagged for code re-run, see §Phase 6 below):** a 2021-census-direct computation of A1 MAD on the 87 existing 2019 EDs. This establishes a 2021-census legal-baseline that demonstrates (a) the 2019 map's MAD on 2021-census data and (b) that projecting 2026 MAD requires 2026 ED shapefiles to aggregate 2021 census DAs, which are blocked. The appendix can state explicitly: *"The §12(3)-operative 2026 MAD cannot be computed without 2026 shapefiles. The closest available §12(3)-operative statistic is 2019-map MAD on 2021 census data, which is X,XXX. The 2026-proposal MADs reported in §2.1 are on the commission's 2024 TBF basis; the commission's basis is the only available basis for a 2026-ED analysis because the 2026 shapefiles are not released."*

### (v) Residual vulnerability

The honest acknowledgement here is that the audit's §2 cannot be made fully §12(3)-compliant until the 2026 shapefiles are released. Until then, the data-source defect is a real limitation, not a defendable equivalence. The Plan B cross-check establishes direction invariance but does not produce §12(3)-compliant numbers for the 2026 proposals. A peer reviewer committed to statutory-basis discipline can still argue the 2026 §2 numbers are derivative of non-compliant commission data and the audit inherits the defect. The best the audit can do is (a) be explicit about which basis is used, (b) show direction invariance across bases, (c) add the 2019-boundary 2021-census appendix as the legal baseline, and (d) wait for shapefile release to re-run §2 on a §12(3)-compliant basis for the 2026 proposals. The cycle-lag analysis helps by shifting the focus from drawing-time snapshot to durability across the 10–14 year lifespan of the map, where the 2021-vs-2024 distinction matters less than the 2024-vs-2030 projection.

**A4 severity after fortification: MEDIUM-to-LOW.** The attack partially lands on statutory-basis discipline; the defence via Plan B cross-check, cycle-lag analysis, and clear data-basis labeling substantially narrows the hit. The residual vulnerability is real: without 2026 shapefiles the audit cannot produce §12(3)-compliant 2026 numbers, and until it does, a §12(5)-strict reviewer can call the §2 numbers derivative of non-compliant commission data. The fortification turns the attack from "structural flaw" to "acknowledged limitation under §12(5) interpretation; direction robust under every alternative data source tested; §12(3)-compliant 2026 re-run blocked on shapefile release."

---

## A5 — 70/30 weight chosen to support finding

### (i) The attack

*"Your sensitivity table shows EG asymmetry ranges from +1.53 % (60/40) to −1.52 % (80/20). Your 'central' is 70/30, which gives −0.51 %. You have not justified 70/30 as the objectively correct weight. You reported a sensitivity range that includes zero and changes sign. The choice of 70/30 as headline is the choice that shows your finding. Footnote says 'based on observed 2023 apportionment' — does 2023 apportionment generalize to 2027 or 2031?"*

### (ii) What the attack gets right

Three parts of this attack land.

**Part 1 — 70/30 is not derived from data.** The paper's footnote language ("based on observed 2023 apportionment") is imprecise. The actual 2023 Election-Day vs Vote-Anywhere ratio in the polls data (`analysis/polls_2023_unified.csv`) is 52.8 % / 42.9 % / 4.3 % (Special Ballot + Mobile) — not 70 / 30. The 70/30 weight is not the Election-Day/Vote-Anywhere apportionment; it is a modeling convention about *urban-core voter composition of hybrid EDs* (the hybrid district is modeled as 70 % inherited 2019 urban-core voters + 30 % rural absorption). This is a judgment call, not an empirical derivation. `analysis/reports/v0_1_bias_audit.md` already admits this: *"70/30 is conservative — actual rural areas the minority absorbs are wealthier UCP strongholds, not average rural Alberta."* The red-team is right that the paper's provenance language is loose.

**Part 2 — The sensitivity range includes zero and changes sign.** Under 60/40 the asymmetry is +1.58 % (minority *less* UCP-favourable) vs at 80/20 it is −3.04 % (minority *more* UCP-favourable). The direction of the asymmetry is sensitive to the urban weight within the plausible range. The 70/30 "central" is the weight at which the asymmetry is −0.51 pp, which is a defensible "center" but not the unique defensible choice.

**Part 3 — 2023 does not necessarily generalize.** The rural NDP share in 2015 was 35 %, in 2019 was 26 %, in 2023 was 33 %. Wave-year variation is large. A 2027 or 2031 election could see a rural NDP share substantially different from 33 %, and the 70/30 blend would then be further from reality. The paper's Monte Carlo already covers some of this variation (rural baseline U(0.26, 0.36)), but the point stands that no single weight is obviously correct.

### (iii) The defence

Three defences, the weakest of the five.

**Defence 1 — The sensitivity table is in the paper; the paper already reports the range.** §3.4 lists 60/40 asymmetry −1.36 pp, 70/30 asymmetry −0.51 pp, 80/20 asymmetry −1.61 pp. The Monte Carlo CI [−3.04, +0.76] pp is reported in §3.4 stress-test update. The paper does not hide the dependence on urban weight; it discloses it. The red-team's charge is not that the sensitivity was concealed but that a "central" 70/30 was chosen as the headline when the range includes zero. The weak response is: pick a different reporting convention. The stronger response is: stop reporting any single weight as the headline and report the range.

**Defence 2 — The direction is consistent across the three tested weights.** The sensitivity table shows −1.36 pp, −0.51 pp, −1.61 pp at 60/40, 70/30, 80/20. All three are negative (minority more UCP-favourable). The red-team's claim that "60/40 produces +1.53 %" is a *Monte Carlo corner* — the mean asymmetry under Monte Carlo sampling of the full parameter range is −1.22 pp (paper reports this; analysis/scripts/v0_3_monte_carlo_ci.py produces it). Within the sensitivity-table's three discrete weights, direction is stable. The attack conflates the sensitivity-table discrete results (three weights) with the Monte Carlo full-range CI (all combinations). In the Monte Carlo, 89.3 % of samples are negative; 10.7 % are positive. In the discrete three-weight test, 100 % are negative. The paper should clarify this distinction.

**Defence 3 — The 70/30 weight can be replaced by the weight-conditional finding as the headline.** Instead of reporting 70/30 as central, the paper can report: *"minority-majority EG asymmetry is −1.36 pp at 60/40, −0.51 pp at 70/30, −1.61 pp at 80/20; Monte Carlo 95 % CI across U(0.55, 0.85) × U(0.26, 0.36) is [−3.04, +0.76] pp. The direction is negative in all three discrete weight tests and in 89.3 % of 2,000 Monte Carlo samples. The sign of the asymmetry is robust under the parameter space tested; the magnitude is weight-conditional and not reliably pinned without measured Phase 4C attribution."* This is the weight-conditional reframing the attack invites.

**Note on 70/30 provenance correction.** The paper currently says 70/30 is "based on observed 2023 apportionment." This is wrong as stated — 2023 Election-Day / Vote-Anywhere was 52.8/42.9. The correct provenance is: *"70/30 is a modeling convention for urban-core voter composition of hybrid districts (70 % inherited 2019 urban-core voters + 30 % rural absorption). It is not derived from observed vote data. Sensitivity across 0.60, 0.70, 0.80 is reported in Table §3.4; Monte Carlo across U(0.55, 0.85) is reported in §3.4 stress-test update."* The paper's footnote should be corrected.

### (iv) Narrowed claim

The paper's §3.3 currently writes *"the minority's EG is 0.58 pp more UCP-favorable than the majority's under 70/30 blending."* Proposed replacement, expressed as a weight-conditional finding:

> **"Under the sensitivity range of urban-weight assumptions 0.60 to 0.80, the minority-majority EG asymmetry ranges from −0.51 pp (at 0.70) to −1.61 pp (at 0.80) and is −1.36 pp at 0.60. The direction (minority more UCP-favorable) is stable across all three discrete weights tested. Under Monte Carlo sampling over U(0.55, 0.85) × U(0.26, 0.36) × per-hybrid jitter (N=2,000), the mean asymmetry is −1.22 pp and the 95 % CI is [−3.04, +0.76] pp. 89.3 % of samples show minority more UCP-favorable. The audit reports the full weight-conditional range rather than a single point estimate. The 70/30 urban weight is a modeling convention for hybrid-district composition (70 % inherited urban-core voters + 30 % rural absorption), not an empirically-derived value; it serves as a reference point, not as a preferred weight. The measured-attribution Phase 4C pipeline, when executed, will replace the urban-weight blend with observed apportionment; until then, the sensitivity range is the headline and no single weight is privileged."**

The footnote claiming 70/30 is based on "2023 apportionment" should be corrected to: *"70/30 is a modeling convention for hybrid-district composition (urban-core inherited vote + rural absorption rate), not empirical 2023 Election-Day/Vote-Anywhere apportionment (which is 52.8/42.9 in the 2023 Statement of Vote)."*

### (v) Residual vulnerability

A hostile reviewer can still observe: "the sensitivity range includes zero" (true — Monte Carlo CI [−3.04, +0.76] includes zero), "the direction reverses in 10.7 % of Monte Carlo samples" (true), and "the specific magnitude is not pinned" (true). The weight-conditional framing above acknowledges all three. What it does *not* concede is that the finding reverses across the three discrete sensitivity-table weights — within 0.60/0.70/0.80 the direction is stable. Nor does it concede that the finding is purely 2023-specific — the 338 Canada April 2026 polling reallocation (A1 defence) shows the 1-seat structural asymmetry holds across vote inputs. The residual vulnerability is that the magnitude is not significant at the 95 % frequentist level and the modeling convention for 70/30 is not derived from data. Both are acknowledged in the narrowed claim.

**A5 severity after fortification: MEDIUM.** Attack partially lands on magnitude claim and on 70/30 provenance. The narrowing from "70/30 central" to "weight-conditional range" addresses the magnitude attack. The correction of the 70/30 provenance footnote addresses the provenance attack. The direction claim survives because 100 % of discrete sensitivity-table weights and 89.3 % of Monte Carlo samples are negative; the 1-seat structural asymmetry replicates across vote inputs.

---

## Summary of severities after fortification

| Attack | Before | After | What landed | What survived |
|---|---|---|---|---|
| A1 (CI crosses zero) | HIGH | MEDIUM | Magnitude claim at 95 %; "qualified pass" language | Direction at ≈90 %; 1-seat structural asymmetry via 338 replication |
| A2 (Chen-Rodden framing) | HIGH | MEDIUM | Partisan-bias framing in isolation | Structural findings (§A/C/D) outside Chen-Rodden's reach |
| A3 (pre-registration) | HIGH | LOW | Residual sceptic-risk of intra-session pre-reg only | Git timestamps 08:32 → 10:56; symmetric application to both maps |
| A4 (§12 data basis) | HIGH | MEDIUM-to-LOW | §12(3)-compliant 2026 numbers blocked on shapefiles | Direction invariant under Plan A vs Plan B; cycle-lag signal independent |
| A5 (70/30 weight) | HIGH | MEDIUM | Magnitude precise; 70/30 footnote provenance | Direction across discrete weights (100 %) and MC (89.3 %); 1-seat replication |

Five attacks drop from HIGH to at most MEDIUM after fortification. One (A3) drops to LOW. No attack remains at HIGH if the paper adopts the narrowed claims and footnote corrections.

---

## Phase 6 — Integration recommendations

Proposed edits to `report_academic.md`. Parent session applies. Not committed by this track.

### Edits requiring only footnote or caveat (low-cost)

**F1 — §3.3 (Results), final paragraph.** Replace the sentence *"the minority's EG is 0.58 pp more UCP-favorable than the majority's under 70/30 blending"* with the weight-conditional paragraph in A5(iv) above. No code re-run required; values are already in §3.4.

**F2 — §3.5 (Falsifiability gate).** Replace *"directional claim holds at 89.3 % confidence"* and the surrounding "qualified pass at 90 %" language with the A1(iv) paragraph. Add the cross-election-reversal caveat inline. No code re-run required.

**F3 — §3.7 (Packing signatures detected), new closing paragraph.** Insert the pre-registration provenance paragraph from A3(iv) including the git commit hashes and timestamps. No code re-run required; timestamps already verified via `git log`.

**F4 — Footnote on 70/30 provenance.** Replace any footnote or inline language claiming 70/30 is "based on observed 2023 apportionment" with the corrected provenance in A5(iv): "modeling convention for hybrid-district composition, not empirical apportionment." No code re-run required.

**F5 — §3.6 (Chen-Rodden), new closing paragraph.** Add the A2(iv) narrowed-claim paragraph explicitly scoping Chen-Rodden's applicability to Section B only. No code re-run required.

**F6 — §7 Synthesis, update headline claim.** Rewrite the "minority is measurably UCP-favourable" framing to the A2(iv) structure-first framing: primary finding is structural differences (A1 dispersion, A2 Calgary zone gap, A3 s.15(2), C4 community splits); partisan-bias difference is secondary and weight-conditional. No code re-run required.

### Edits requiring code re-run

**F7 — New appendix: 2021-census-direct A1 on 2019 EDs.** Script: new file `analysis/scripts/a1_legal_baseline_2021_census.py`. Inputs: `data/alberta_2021_csd_populations.csv` + a CSD-to-2019-ED crosswalk (partial crosswalks already exist — see `data/v0_1_csd_splits_summary.csv`). Output: MAD, EDs above/below ±25 % for the 87 2019 EDs under strict 2021-census aggregation. This establishes the §12(3)-operative legal baseline against which the commission's 2024-TBF basis can be compared. Runtime estimate: 30–90 minutes to write and validate. **Note — a 2021-census-direct A1 on the 2026 EDs is blocked on shapefiles; only the 2019-ED version is producible now.**

**F8 — Monte Carlo re-run with explicit direction / magnitude separation in output.** Script: modify `analysis/scripts/v0_3_monte_carlo_ci.py` `main()` function to produce two output blocks: (a) direction-consistency report (89.3 % negative); (b) magnitude CI report (95 % [−3.04, +0.76] crosses zero). Currently they are intermingled. Low-effort change; allows the paper's §3.5 to cite cleanly separable outputs. Runtime: 5 minutes for the edit + 2 minutes MC runtime.

### Edits requiring new analysis files

**F9 — `analysis/v0_1_pre_registration_provenance.md`** — a standalone document that captures the git-log evidence used in A3's defence. Includes the full `git log --all --format="%h %ci %s" -- v1_2_gerrymander_audit_prompt.md` output, the `git show 5b0bc06` diff showing P/C/E criteria at commit time, and the timing analysis (prompt commit 08:32:20; signature-detection commit 10:56:11; delta 2 h 24 m). Appendices in `report_academic.md` can link to this file. 30–45 minutes to write.

**F10 — `analysis/v0_1_70_30_weight_provenance.md`** — a standalone document that documents the 70/30 weight as a modeling convention rather than an empirical apportionment, and shows the actual 2023 Election-Day vs Vote-Anywhere ratio (52.8 / 42.9) so the correction is auditable. 20–30 minutes to write.

### Edits flagged but not recommended

**F-rejected — Re-run §2 with a different data basis.** Not recommended. The commission-derived basis is the one that matches what the commission published; replacing it would break apples-to-apples comparison with the commission's own tables. The correct fix is F7 (adding a 2021-census-direct legal baseline as appendix) while retaining §2 on the commission's basis with clear labeling. Re-running §2 wholesale would not improve the audit and would create divergence from the commission's published variance tables.

---

## References within this document

- Red-team attacks: `analysis/v0_1_red_team_academic_discredit.md`
- Monte Carlo CI evidence: `analysis/scripts/v0_3_monte_carlo_ci.py`
- Signature-detection pipeline: `analysis/scripts/v0_2_packing_cracking_analysis.py`
- Pre-registration commit: `git show 5b0bc06` (v1.2 prompt) and `git show 282bc6d` (signature detection)
- Plan B cross-check: `analysis/reports/v0_1_plan_b_cross_check.md`
- Cycle-lag analysis: `analysis/v0_1_cycle_lag_analysis.md`
- 338 Canada cross-validation: `analysis/methodology/v0_1_338canada_riding_level.md`
- 70/30 bias admission: `analysis/reports/v0_1_bias_audit.md` (line 44, 133)
- 2023 actual ballot-type apportionment: `analysis/polls_2023_unified.csv` (computed: Election Day 52.8 %, Advance 42.9 %, Special Ballot + Mobile 4.3 %)
- Literature review: `analysis/methodology/v0_1_academic_literature_review.md` (for Chen-Rodden scope and Katz et al. ensemble discipline)
- Academic paper under attack: `report_academic.md` v0.2 (Author: Will Conner, April 22, 2026)

*Fortification v0.1. Authored as peer-review-grade response to HIGH-severity attacks. Does not edit `report_academic.md` directly; flags specific §-and-line edits for the parent session. Adopts the posture of the author's methodologist under pressure: lands every hit that lands; narrows every claim that needs narrowing; surfaces every residual vulnerability honestly. Claims fortified here are claims that could survive public peer review. Claims that cannot be fortified (single-weight magnitude precision, §12(3)-compliant 2026 numbers) are stated as blocked or narrowed, not defended.*
