---
name: Pre-registration — Alberta Electoral Boundaries Audit signature-detection checklist for the November 2026 MLA-committee 91-seat map
description: Submission-ready pre-registration document for OSF Registrations (recommended platform; see analysis/v0_1_pre_registration_platform_analysis.md). Commits the audit to a fixed 17-signal checklist, with numeric thresholds and pass/fail criteria, to be scored on the Alberta MLA-committee 91-seat map within 72 hours of its release (target date 2026-11-02). Closes D17 (self-held pre-registration vulnerability) by placing the checklist under third-party custody with a verifiable timestamp.
forward_dependencies:
  - OSF Registration submission (PO-held; see Phase 3 instructions in analysis/v0_1_pre_registration_platform_analysis.md)
  - Track C re-audit of November committee map (executed against this pre-registered checklist)
  - report_academic.md §3.11 (baseline scorecard; the November column is the outcome of this pre-registration)
backward_dependencies:
  - analysis/v0_1_track_c_checklist_baseline_scoring.md (test list, numeric thresholds, baseline scoring for majority and minority 2026 maps)
  - report_public.md §"What a gerrymander in the 91-seat map would actually look like" (plain-language checklist)
  - report_academic.md §3.7–3.10 (signature-detection methodology)
  - analysis/v0_1_red_team_round_2.md §D17 (vulnerability this closes)
  - analysis/v0_1_chair_recommendation_5_analysis.md (R5 conditions included as X1)
---

# Pre-registration — Alberta Electoral Boundaries Audit signature-detection checklist (November 2026 MLA-committee 91-seat map)

## 1. Title and metadata

**Title.** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.

**Author.** Will Conner.

**Affiliation.** Independent civic audit. Not affiliated with the Government of Alberta, the Alberta Electoral Boundaries Commission, the MLA Special Select Committee, or any political party.

**Corresponding audit.** *Alberta Redistricting Audit* (2026). Academic report (`report_academic.md`) and public report (`report_public.md`). Repository time-stamped via public git history.

**Pre-registration date.** 2026-04-22 (document draft); submission date to OSF held by the author (see submission instructions).

**Target map.** The 91-seat electoral division map to be tabled by the Alberta MLA Special Select Committee chaired by Brandon Lunty (MLA, Leduc-Beaumont). The committee was established by Alberta Legislative Assembly Motion 19, passed 44-36 on 2026-04-16, with a reporting deadline of 2026-11-02.

**Scope.** This pre-registration binds the audit to a fixed set of 17 tests (S1–S6 strong signals, W1–W3 weak signals, P1–P5 process signals, X1–X3 supplementary gates) with numeric thresholds where applicable and pass/fail criteria for each. It commits the audit to score the committee's map on these tests within 72 hours of map release, without post-hoc revision of criteria.

**Not scoped.** This pre-registration does not commit the audit to a specific rhetorical framing, a specific headline claim, or a specific conclusion about whether the November map is or is not a gerrymander. It commits the audit to the test grid and the scoring rule; the narrative is determined by the scored results.

---

## 2. Background

On 2026-04-16 the Alberta Legislative Assembly passed Motion 19 (44-36), setting aside the Alberta Electoral Boundaries Commission's 2026 majority report and establishing a Special Select Committee of five MLAs (three UCP, two NDP) chaired by Brandon Lunty to produce a 91-seat electoral boundary map by 2026-11-02. The motion was framed as partially aligned with the commission chair's Addendum Recommendation 5, which proposed, in the event the Legislature could not accept the majority's 89-seat boundaries, raising the seat count to 91 through an all-party Select Special Committee to restore two rural s.15(2) districts while maintaining the rest of the province as the majority proposed. The committee's mandate does not include public hearings on the draft map. Its advisory panel membership and terms of reference were unpublished as of 2026-04-22 (CBC Edmonton, 2026-04-16; Calgary Journal, 2026-04-21).

The *Alberta Redistricting Audit* (2026) has analysed the two 89-seat commission maps (majority and minority) using the same signature-detection methodology pre-registered below. It detected three formal gerrymander signatures under the minority map (Calgary Zone A packing, Airdrie four-way cracking, Rocky Mountain House-Banff Park engineered s.15(2) boundary) and zero under the majority. The full baseline scorecard is in `analysis/v0_1_track_c_checklist_baseline_scoring.md` (repository state as of this pre-registration's submission date). The November 91-seat map is a held-out test: the audit pre-registers here the criteria under which the committee's map will be scored on the same grid, before the map exists.

This pre-registration closes a vulnerability identified in round 2 of the audit's red-team analysis (D17, `analysis/v0_1_red_team_round_2.md`): "pre-registration as typically practised (OSF, AsPredicted) requires a third party to hold the pre-registered criteria; the audit's November checklist is self-held." Posting this document to OSF before the map lands places the checklist under third-party custody with a verifiable timestamp.

---

## 3. Pre-registered tests

All 17 tests below carry over from the calibrated checklist in `analysis/v0_1_track_c_checklist_baseline_scoring.md`. Each has a numeric threshold (where applicable) and a binary pass/fail criterion. Each test has a stated blocker condition: if the blocker applies, the test is recorded as BLOCKED (not "failed"), with the blocker reason logged. BLOCKED tests do not count toward the "triggered" tally.

### Strong signals (S1–S6)

**S1. The three minority signatures are preserved in the November map.**
- *Threshold.* A map preserves all three formal signatures detected under the minority if: (a) a Calgary zone partition exists where one zone's mean ED population exceeds the other's by ≥10% (minority baseline: 12.20%, Zone A vs Zone B); (b) the City of Airdrie is split across ≥4 EDs; (c) a s.15(2) district exists whose geographic area includes ≥20% uninhabited protected land (national park, wilderness area, or equivalent) with population-weighted centroid outside the protected area.
- *Pass.* 0 of 3 criteria met. *Fail (signature triggered).* ≥1 of 3 criteria met. Reporting also states the count (0, 1, 2, or 3).
- *Blocker.* None. All three criteria are computable from the map plus 2021 census CSD data, irrespective of 2026 shapefile release.

**S2. New signatures appear beyond the minority's set.**
- *Threshold.* Any of: (a) Edmonton zone packing ≥10% gap between any two defensible Edmonton zones (using river, ward, or municipal partition); (b) cracking (≥4 EDs) in a third Alberta city not already flagged (i.e., beyond Airdrie in S1; Lethbridge and Red Deer are already flagged as cracking candidates in the baseline and are in-scope for this test); (c) an additional engineered s.15(2) boundary beyond the one flagged in S1.
- *Pass.* 0 of 3 criteria met. *Fail.* ≥1 of 3 criteria met.
- *Blocker.* None.

**S3. Both extra rural seats have engineered boundaries.**
- *Threshold.* The committee's 91-seat map contains 2 more seats than the existing 87-seat map (2019) or 2 more than the 89-seat proposals. Identify the incremental seats by comparison. If both (or at least 2) added seats relative to the majority 89-seat baseline are rural and both invoke s.15(2) with boundaries that include ≥20% uninhabited protected land, the signal fires.
- *Pass.* 0 or 1 engineered rural additions. *Fail.* 2 engineered rural additions.
- *Blocker.* If the November map's relationship to the 89-seat majority baseline is not reconstructible (e.g., the committee publishes only the final 91-seat map with no differential trace), the audit will compare to the 2019 87-seat baseline instead. Record which baseline was used.

**S4. Efficiency gap crosses the US 7% threshold.**
- *Threshold.* Efficiency gap (Stephanopoulos and McGhee 2015) computed on 2023 provincial election votes reallocated to the November map, using the audit's pre-existing 70/30 urban/rural weighting, exceeds 7% in absolute magnitude.
- *Pass.* |EG| ≤ 7.00%. *Fail.* |EG| > 7.00%.
- *Blocker.* Requires a vote-to-ED reallocation. If 2026 shapefiles are not released, the audit will use poll-to-ED crosswalks where available, as in the baseline. If even poll-level reallocation is infeasible, the test is BLOCKED.

**S5. Ensemble outlier test.**
- *Threshold.* The November map's UCP-favourability percentile, computed against a Markov-Chain Monte Carlo ensemble of ≥10,000 rule-following alternative 91-seat maps (GerryChain, seed published), falls in the top 5% (percentile ≥ 95) of UCP-favourable plans.
- *Pass.* Percentile < 95. *Fail.* Percentile ≥ 95.
- *Blocker.* Requires 2026 shapefiles. If Elections Alberta or the committee does not release shapefiles with the map, the test is BLOCKED. The audit will not infer shapefiles from the report text; inferred ensembles are not valid substitutes.

**S6. Publicly-supported configurations dropped; unsupported ones kept.**
- *Threshold.* Using the submission-archive public-support tiers in `analysis/submission_search_findings.md`: the map drops configurations in tier "documented public support" (e.g., Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere) while keeping configurations in tier "no documented public support" (Airdrie 4-way, Nolan Hill-Cochrane). The test fires if ≥1 supported config is dropped AND ≥1 unsupported config is kept, in the same map.
- *Pass.* No inversion. *Fail.* Both conditions met.
- *Blocker.* None (submission archive is complete as of this pre-registration).

### Weak signals (W1–W3)

**W1. Two extra rural seats on their own.**
- *Threshold.* The committee adds 2 rural seats relative to the 89-seat majority baseline, regardless of whether their boundaries are engineered (if both are engineered, S3 fires instead and this test is subsumed).
- *Pass / Fail.* Fires when 2 rural seats added without engineering. On its own, this is the stated UCP position and is not a strong signal.
- *Blocker.* Requires baseline identification per S3.

**W2. Calgary zone gap similar to the minority's.**
- *Threshold.* Calgary Zone A vs Zone B mean-ED-population gap ≥ 5% (below S1's 10% strong-signal threshold but above a null baseline). Majority baseline: 0.36%; minority baseline: 12.20%.
- *Pass.* Gap < 5%. *Weak signal.* 5% ≤ gap < 10%. *Strong signal (folds into S1).* Gap ≥ 10%.
- *Blocker.* None.

**W3. Nolan Hill-Cochrane hybrid retained without stronger justification.**
- *Threshold.* The map contains an ED that pairs Cochrane with a Calgary residential neighbourhood across the city limit (the minority's Calgary-Nolan Hill-Cochrane pattern), and the committee's stated rationale does not add substantive evidence beyond commuter-tie claims already shown unsupported at CSD resolution (`analysis/v0_1_cochrane_journey_to_work.md`).
- *Pass.* No such pairing, or pairing with additional evidence. *Fail.* Pairing present with commuter-tie-only defence.
- *Blocker.* If the committee does not publish per-ED rationale text, the audit scores "ED boundaries present: yes/no" only and notes the rationale-evaluation gap.

### Process signals (P1–P5)

**P1. Committee proceedings closed to the public.**
- *Threshold.* The committee did not hold public hearings on the draft map before it was tabled.
- *Pass.* Public hearings held and transcripts published. *Fail.* No public hearings on draft map.
- *Blocker.* None.

**P2. Advisory panel members not named / terms of reference withheld.**
- *Threshold.* As of 2026-04-22, advisory panel membership and terms were unpublished. The test fires if membership and/or terms are never published prior to or with the November map release.
- *Pass.* Both published. *Fail.* Either remains unpublished at map release.
- *Blocker.* None.

**P3. Draft map not released for public comment.**
- *Threshold.* A draft of the committee's map was not released for public comment prior to the final 91-seat map.
- *Pass.* Draft released with ≥14-day public comment window. *Fail.* No draft public-comment window.
- *Blocker.* None.

**P4. Legislative adoption without amendment or published dissent.**
- *Threshold.* If the Legislature votes to adopt the committee's map, and the vote passes without amendment AND without a published dissenting opinion from any committee member.
- *Pass.* Either: the map is not yet adopted at scoring time (then record as "pending"); the map is adopted with published dissent; the map is amended during adoption. *Fail.* Adopted unanimously without amendment and without dissent.
- *Blocker.* If adoption timing falls after the 72-hour scoring window, record as "pending" and revisit once a legislative record exists.

**P5. AI tools used without disclosure.**
- *Threshold.* The committee uses AI-assisted tools in map drafting (a possibility raised by the Premier's 2026-04-16 remarks) and does not publish with the map: the prompts used, model versions, random seeds, candidate ensembles considered, and selection criteria. The audit's own AI-use framework (`analysis/v0_1_ai_use_recommendations_for_committee.md`) is the published standard against which disclosure is measured.
- *Pass.* Either: no AI tools used (with a clear committee statement); or AI tools used with full disclosure per the audit's framework. *Fail.* AI tools used with partial or no disclosure.
- *Blocker.* If the committee neither affirms nor denies AI use, record as "undetermined" and note the transparency gap separately.

### Supplementary gates (X1–X3)

**X1. Chair Miller's Recommendation 5 conditions (a)–(d) are satisfied.**
- *Threshold.* From the Chair's Addendum to the Majority Report (AEBC, 2026, pp. 66–67):
  - (a) No impact on any electoral division in Airdrie or south of it except Drumheller-Stettler.
  - (b) No impact north of Edmonton's North Saskatchewan River.
  - (c) South-of-NSR Edmonton districts revert to the interim-report map.
  - (d) A Clearwater County plus western Mountain View County s.15(2) district is restored.
- *Pass.* All four conditions met. *Fail (partial).* 1–3 conditions met (record count). *Fail (inverted).* 0 conditions met.
- *Blocker.* Condition (c) requires comparing to the interim-report Edmonton south-of-NSR districts; the interim report is public.

**X2. Rationale-against-data checks.**
- *Threshold.* For each rationale the committee states for a specific ED configuration, the audit cross-checks against the verification dataset used in the baseline scoring (Alberta Education school-division boundaries; StatsCan 2021 journey-to-work table 98-10-0459; Alberta Treasury Board 2024 population estimate; 2021 census CSD populations). A contradiction fires when a stated rationale is directly falsified by a public dataset.
- *Pass.* 0 rationale-contradictions. *Weak signal.* 1–2 contradictions. *Strong signal.* ≥3 contradictions.
- *Blocker.* If the committee does not publish per-ED rationale text, X2 is BLOCKED and noted as a transparency gap.

**X3. 338Canada (or equivalent) partisan cross-validation.**
- *Threshold.* The November map's reallocated seat count (using 338Canada poll-level projection or equivalent independent projection) shifts the UCP seat total by ≥2 relative to the majority baseline (which 338 reallocation gives as 67 UCP / 22 NDP). The test fires on UCP-favourable shifts of ≥2 seats.
- *Pass.* UCP reallocation ≤ 68. *Weak signal.* 69 ≤ UCP reallocation ≤ 70. *Strong signal.* UCP reallocation ≥ 71.
- *Blocker.* Requires 338Canada to publish a 91-seat reallocation, or the audit to compute its own via poll-to-ED crosswalks. If infeasible within the 72-hour scoring window, X3 is flagged as PENDING rather than BLOCKED, and updated when the reallocation is available.

### Scoring timing

All 17 tests will be scored within 72 hours of the November 2026 91-seat map's public release. The 72-hour window starts when the map is first publicly posted by the committee, the Legislative Assembly, or Elections Alberta — whichever is earliest. If the map is released piecemeal (e.g., overview map followed by per-ED boundaries), the 72-hour window starts at the first release that contains sufficient information for test scoring (ED names and rough boundaries are sufficient for S1-a, S1-b, S6, W2, W3, P1-P5, X1; detailed shapefiles are required for S4, S5, and X3).

---

## 4. Scoring authority

The audit's methodology is independently runnable. The scripts and data supporting each test are public in the audit's repository (see §3 test-by-test citations to files in `analysis/`). A third party can replicate the scoring by executing the same scripts against the committee's released map.

**Commitment.** The audit author will publish the per-test scorecard within 72 hours of map release, in the same structure as the baseline scorecard (`analysis/v0_1_track_c_checklist_baseline_scoring.md`), with each test's outcome recorded as PASS, FAIL (triggered), BLOCKED, PENDING, or UNDETERMINED, per the criteria in §3.

**No criteria revision.** The audit will not revise the numeric thresholds or pass/fail criteria in §3 between this pre-registration's submission and the scoring of the November map. Any discovered error in a threshold will be disclosed as an erratum but the original threshold remains in force for the November scoring. If a post-hoc methodological improvement is worth applying, it is recorded and scheduled for the next map cycle, not retrofitted into this scoring.

**Author disclosure.** The audit author is the scorer. This pre-registration does not create external scorer custody (which only a Registered Report at a peer-reviewed journal would achieve). The pre-registration creates *criteria custody*: the tests, thresholds, and pass/fail rules cannot be altered between now and the scoring, because the authoritative copy is held by OSF with a verifiable timestamp. Readers verify the author's scoring against the OSF-held criteria. This is the standard D17 fix (OSF-held pre-registration) and is the minimum methodological guarantee the audit commits to before the map lands.

---

## 5. What would falsify the audit's critique

If the November 91-seat map meets **all** of the following conditions, the audit will publish a concession statement in the November re-audit noting that its structural critique of the minority's signatures does not extend to the committee's output:

1. **S1 = 0 triggered.** Zero of three minority signatures are preserved in the November map (no Calgary zone packing ≥10%, no ≥4-way Airdrie split, no engineered s.15(2) boundary).
2. **S2 = 0 triggered.** No new signatures introduced beyond the minority's set.
3. **S6 = PASS.** No documented-public-support inversion.
4. **P1, P2, P3 all = PASS.** Committee held public hearings on the draft, named its advisory panel and published its terms, and released a draft for public comment before tabling.
5. **X2 ≤ 1 contradicted rationale.** The committee's per-ED rationales are substantially consistent with public datasets.

Additional conditions that, if met, strengthen the concession:
- S4 = PASS (efficiency gap ≤ 7%), indicating the map is not in US-court-flagged territory.
- S5 = PASS (ensemble percentile < 95) if shapefiles are released and the ensemble can run.
- X1 = all four R5 conditions met.

If all five core conditions hold and shapefiles are released allowing S5 to run and S5 passes, the audit will publicly note that **the committee's map, by the audit's own pre-registered criteria, is not a gerrymander under the methodology the audit applied to the minority map.** This is the strongest concession the pre-registered framework can produce; it is available.

Conversely, if any **four or more** of the strong-signal tests (S1 triggered, S2 triggered, S3 triggered, S4 failed, S5 failed, S6 failed) fire together with P1–P3 all failed, the audit's existing critique extends to the November map and the "sure-sign" threshold stated in the public checklist is met. Intermediate configurations (e.g., one signature triggered plus two process signals) are reported literally — not collapsed into a single "gerrymander / not gerrymander" verdict — per the audit's existing graded-evidence reporting discipline (Nosek et al. 2018; Munafò et al. 2017; ASA 2016, 2019).

---

## 6. Anticipated analyses

On the November map, the audit will compute and publish:

1. **Population equality (A-series).** MAD (mean absolute deviation), maximum deviation, distribution of per-ED population across the 91 seats, count of EDs outside the ±25% statutory window under 2021 census and 2024 TBF population estimates. Comparison against majority and minority baselines.
2. **Partisan metrics (B-series).** Efficiency gap, mean-median difference, declination, partisan bias at 50/50 vote share, using 2023 provincial vote reallocations. Comparison against baselines.
3. **Signature count (S-series).** Scored per §3.
4. **Geographic coherence (C-series).** Visual inspection of named EDs for lasso/corridor shapes, engineered statutory boundaries, and community-of-interest splits; symmetric-test-selection application of the same anomaly-scan question set used for the 89-seat maps.
5. **Process audit (D/P-series).** Inspection of the committee's public record for hearings, panel disclosure, draft-comment window, adoption vote, and AI-use disclosure.
6. **338Canada / independent reallocation (X3).** Seat-count reallocation using the same 338Canada riding-level methodology applied to the 89-seat maps (`analysis/v0_1_338canada_riding_level.md`).
7. **Ensemble percentile (S5).** GerryChain MCMC ensemble, if shapefiles are released. Seed published with results.

All seven analyses produce numeric outputs. None of the thresholds or calculation methods will be changed between this pre-registration and the November scoring.

---

## 7. Commitments not to do

The audit commits **not to** do any of the following between this pre-registration and the November scoring:

1. **No post-hoc threshold adjustment.** The numeric thresholds in §3 (10% zone gap, 4-way Airdrie split, 7% efficiency gap, top-5% ensemble percentile, 5% weak-signal zone gap, 2-seat UCP shift) are fixed. No test's threshold will be tightened or loosened between now and November scoring.
2. **No new supplementary tests invented after map release.** The test set is fixed at the 17 tests in §3. If after the map lands the audit notices a feature that would warrant a new test, that observation will be reported as a "post-hoc observation not pre-registered" and will not affect the pre-registered scorecard's totals.
3. **No cherry-picking of reportable tests.** All 17 tests will be scored and reported, including tests that PASS (no signal triggered) or that return BLOCKED for lack of shapefiles. The scorecard will report the full grid, not a subset.
4. **No headline upgrade.** The audit will not elevate a triggered weak signal to a strong-signal claim in the narrative, nor downgrade a strong-signal trigger to a weak-signal footnote. The narrative tracks the scorecard.
5. **No re-ordering of the falsification criteria.** The five conditions in §5 that would produce a concession are fixed. The audit will not add a sixth condition after the map lands to preserve a gerrymander framing.
6. **No silent revision of pre-registration.** If a correction to this document is needed post-submission, it will be posted as a new OSF version with the diff visible and a stated reason. The original OSF-held version remains the authoritative criteria set; post-dated corrections do not retroactively change what was pre-registered.
7. **No selective release timing.** The November scorecard will be published in full within 72 hours of map release, regardless of whether the map appears favourable or unfavourable to the committee.

---

## 8. Reproducibility

The scripts that compute each test's output are in the audit's public repository at `analysis/` (paths cited per-test in §3). Python dependencies are pinned in `requirements.txt`. The 2021 census CSD data, 2023 election poll data, and commission report extracts are in `data/`. A third party can clone the repository, install dependencies, and replicate the baseline scoring against the known 89-seat maps. The November scoring uses the same scripts with the November map as input; no new scripts will be introduced that are not pre-registered here.

**Repository time-stamp.** The audit's git history is public and independent of OSF; readers can verify that the scripts and thresholds referenced here existed at the OSF submission date.

---

## 9. Declarations

- **Funding.** Self-funded. No institutional, governmental, or political-party funding.
- **Conflicts of interest.** None known. The author is not a candidate, party member, or commissioner.
- **AI use disclosure.** The audit uses large-language-model tools (Anthropic Claude; OpenAI GPT-family models at various points) for analysis assistance. The reproducibility commitment in §8 is what makes the AI-assisted analyses verifiable: scripts, data, and thresholds are published; a reader can run them without an LLM in the loop. The audit's broader AI-use framework is in `analysis/v0_1_ai_use_recommendations_for_committee.md`.
- **Version.** v0.1 of the pre-registration document. Later versions, if posted to OSF, will be visible alongside v0.1 with the original v0.1 timestamp preserved.

---

## 10. References

- Alberta Electoral Boundaries Commission. (2026). *Final Report*. Edmonton: Legislative Assembly of Alberta.
- American Statistical Association. (2016). Statement on statistical significance and p-values. *The American Statistician*, 70(2), 129–133.
- American Statistical Association. (2019). Moving to a world beyond "p < 0.05." *The American Statistician*, 73(sup1), 1–19.
- CBC Edmonton. (2026, April 16). Alberta Legislature approves motion to replace boundary commission process.
- Calgary Journal. (2026, April 21). Special Select Committee on electoral boundaries — what we know and do not know.
- Munafò, M. R., et al. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1(1), 0021.
- Nosek, B. A., et al. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.
- Statistics Canada. (2021). *Journey to Work, Table 98-10-0459*. 2021 Census of Population.
- Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review*, 82, 831–900.
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

---

*End of pre-registration document.*
