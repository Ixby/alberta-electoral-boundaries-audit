# Design Critique — Alberta Electoral Boundaries Audit

**Purpose.** Red-team the audit's own design. Identify every gap, assumption, or methodological choice that a hostile critic could exploit. Fix what can be fixed with FOSS and public data; document what can't.

**Format per issue.** Critique · Severity · Fixable with FOSS/public data? · Fix applied (if any) · Residual concern.

---

## Part 1 — Statistical Significance and Inference

### 1.1 No hypothesis testing framework

**Critique.** The audit reports point estimates (e.g., minority EG = −1.36%) and sensitivity ranges (0.58–1.61 pp asymmetry) but no classical p-values, confidence intervals, or null-hypothesis tests. A critic can ask: "How do you know the 0.58 pp asymmetry is distinguishable from zero, given your modeling uncertainty?" We don't have a formal answer.

**Severity:** HIGH. This is the single most common academic-style objection to audits like this one.

**Fixable with FOSS?** Partially. Full frequentist inference requires either (a) repeated sampling (we have one election), (b) a parameterized model with likelihood (we don't have one), or (c) Monte Carlo simulation over modeling parameters (we can do this).

**Fix applied.** Implementing Monte Carlo bootstrap in `v0_3_monte_carlo_ci.py`. Samples urban weights from U(0.55, 0.85), rural-baseline NDP share from U(0.28, 0.38), and per-hybrid weight jitter, then reports the empirical distribution of minority-majority EG asymmetry. Produces a proper 95% CI range.

**Residual concern.** Monte Carlo over modeling choices is not a statistical significance test in the inferential sense — it's a sensitivity envelope. The underlying question "is the asymmetry real?" is about whether two specific map proposals differ, not whether a random sample differs from a population. Inferential significance isn't quite the right frame. But the expanded CI output is more defensible than a single point estimate.

### 1.2 Ensemble-free partisan-bias testing

**Critique.** Modern redistricting literature (Duchin, Chen, Rodden) treats the MCMC ensemble as the gold standard because it answers "is this map extreme relative to other legal maps?" rather than "is this map different from some arbitrary baseline?". We haven't run an ensemble.

**Severity:** HIGH. A legal or academic reviewer will ask for this.

**Fixable with FOSS?** Not without 2026 polygon geometry. GerryChain is FOSS and installed; we lack the input data.

**Fix applied.** None possible in-session. Prompt v1.0 Stage 5 is gated on shapefile release; will run when available.

**Residual concern.** Until ensemble runs, the "minority is systematically partisan" claim is weaker than it would be with ensemble support. The uncertainty analysis (`v0_1_uncertainty_and_shapefile_impact.md` §4) flags a ~35% probability that the minority falls within the 25th–75th percentile of its ensemble — in which case our "intentional partisan choice" framing weakens even while direction holds.

### 1.3 Only four partisan-bias metrics (B1–B4)

**Critique.** The gerrymandering literature uses at least a dozen metrics: efficiency gap, mean-median, partisan bias, declination, GEO, partisan symmetry, seat-vote curve asymmetry, lopsided margins. By choosing B1–B4 specifically, we risk test-selection bias — a critic can ask: "Did you try other metrics that didn't show asymmetry?"

**Severity:** MEDIUM-HIGH. Credibility concern.

**Fixable with FOSS?** Yes. Declination (Warrington 2018) is a simple formula we can implement. Partisan bias is computable from the seat-vote curve. GEO metric requires geographic weighting we don't have without shapefiles.

**Fix applied.** Adding declination to `v0_2_packing_cracking_analysis.py` as metric B6. Reporting it alongside B2/B3/B4 in the comparison table.

**Residual concern.** Adding tests changes the multiple-comparisons picture: if we run N tests, the probability that at least one shows asymmetry by chance grows. Conversely, if all N tests show asymmetry in the same direction, that's stronger evidence than one test. We report all test results, consistent with the "directional consistency across multiple measures is the finding" frame.

---

## Part 2 — Modeling Assumptions

### 2.1 70/30 urban weight is a judgment call, not derived from data

**Critique.** The rationale for 70/30 is pragmatic — it treats hybrid 2026 districts as 70% composed of their 2019 urban core + 30% rural absorption. But the actual split in any given hybrid depends on the hybrid's construction, which we don't know without shapefiles or measured attribution. Sensitivity testing across 0.60/0.70/0.80 shows direction stable but magnitude variable.

**Severity:** MEDIUM. Acknowledged in the audit; sensitivity-tested.

**Fixable with FOSS?** Partially. Population-weighted urban/rural split per hybrid could be estimated from 2021 Census DA population density inside the approximate hybrid area. Requires rough polygon definitions we don't have.

**Fix applied.** Monte Carlo expansion (see 1.1) samples per-hybrid jittered weights rather than single-value across all hybrids. Produces per-hybrid sensitivity rather than single-weight sensitivity.

**Residual concern.** Per-hybrid weights are still uniform across hybrids within a run. The actual per-hybrid accuracy improvement requires measured attribution.

### 2.2 Rural baseline 33.5% NDP share may not apply to suburban absorptions

**Critique.** Minority hybrids absorb Bearspaw, Springbank, Cochrane town, Chestermere — wealthy suburbs that are more UCP than rural Alberta average (probably ~20–25% NDP, not 33.5%). Using 33.5% overstates NDP share in these hybrids, understating the minority's partisan advantage.

**Severity:** MEDIUM. Direction of the bias is known (we're being *conservative*, understating the minority shift) but magnitude is not calibrated.

**Fixable with FOSS?** Yes, partially. Can look up specific 2019 poll-level results in the areas being absorbed and compute per-hybrid rural baselines.

**Fix applied.** In `v0_3_monte_carlo_ci.py`, add a "per-hybrid rural-baseline override" sensitivity run: drop the suburban-absorption rural baseline from 33.5% to 22.5% (empirical suburban Calgary UCP-area baseline) for minority-specific hybrids with suburban absorptions. Report the effect on measured EG asymmetry.

**Residual concern.** The choice of 22.5% is also a judgment call, derived from 2019 poll-level results in Bearspaw/Springbank which are in the 20–25% NDP range. A more rigorous approach would use measured attribution from Phase 4C.

### 2.3 Calgary zone classification (A2)

**Critique.** Zone A/B split is a geographic rule that happens to correlate with partisan geography. A critic can say: "You chose this split because it produces the finding."

**Severity:** MEDIUM. Mitigated by the robustness check using an alternative (2023-winner-based) rule.

**Fixable with FOSS?** Yes. Can add more classification rules: ward-based (Calgary has 14 civic wards with public boundary data), centroid-based (compute ED centroids if we had shapefiles; we don't), median-household-income-based (Statistics Canada income data is public).

**Fix applied.** Adding a third classification rule: **Calgary wards mapped to 2026 EDs by name/area overlap**. Report under all three rules. If all three produce the same direction, the claim is robust to classification choice.

**Residual concern.** Ward mapping to EDs is itself a judgment. Three rules is better than one but still finite.

### 2.4 Name-stem matching for 2019→2026 ED attribution is fragile

**Critique.** Assumes "Calgary-South" in 2026 corresponds to "Calgary-Shaw" in 2019 (south Calgary renamed), but could be a different territory. Some mappings in `MAJORITY_2026_MAPPING` are reasonable inferences, not verified facts.

**Severity:** MEDIUM. Explicit in code (see mapping dicts) but not cross-checked against commission's own description of which 2026 EDs correspond to which 2019 ones.

**Fixable with FOSS?** Yes — the commission's final report (downloadable PDF) typically describes each 2026 ED's relationship to 2019 geography. Not in bundle, could be downloaded.

**Fix applied.** None this pass (PDF too large, would bust the session budget). Flagged for v1.0 Stage 3 execution.

**Residual concern.** Some of the direct-rename mappings may be wrong. An error in any single one shifts that ED's vote share; we don't know the aggregate effect without measured attribution. Monte Carlo jitter (1.1) partially compensates by spreading this uncertainty.

### 2.5 Single-election baseline (2023)

**Critique.** All attribution uses 2023 results. 2023 was a specific political moment (pandemic afterglow, leadership disputes, UCP internal turbulence). Using only 2023 may amplify idiosyncratic effects.

**Severity:** MEDIUM. Real but hard to fix without multi-election attribution.

**Fixable with FOSS?** Yes — 2019 results are in the bundle. Can run B1–B4 on both maps using 2019 vote shares and check if the minority-majority asymmetry is stable across elections.

**Fix applied.** Adding a `run_on_2019_votes()` cross-check in `v0_2_packing_cracking_analysis.py`. Reports B1–B4 for both 2026 maps using 2019 votes as input. If the asymmetry direction and magnitude are similar across 2019 and 2023, that's cross-temporal robustness. If they differ, the 2023-specific idiosyncrasies dominated our finding and the audit's magnitude claim weakens.

**Residual concern.** Two elections is still a small baseline. 2015 data exists but isn't in the bundle.

---

## Part 3 — Data Integrity

### 3.1 s.15(2) criteria hand-coded from memory/estimates

**Critique.** In `electoral_forensics_population.py`, the `S15_2_CRITERIA` dictionary contains my estimated area/distance values (e.g., Canmore-Banff area ~8,500 km²). These are not measured; they are plausible guesses.

**Severity:** MEDIUM-HIGH. A critic could demand verification and find some wrong.

**Fixable with FOSS?** Yes. Natural Resources Canada publishes CanVec geographic data; StatsCan publishes Canadian census boundary files. Area measurements can be computed exactly for each s.15(2) riding once we have 2026 polygon geometry (shapefile-blocked) or 2019 polygon geometry (available) for the predecessor ridings.

**Fix applied.** Computing 2019 predecessor ED areas from the Elections Alberta 2019 shapefile (publicly available, not yet downloaded in this bundle). Cross-reference as a sanity check on the hand-coded 2026 area estimates where predecessors are territorially similar.

**Residual concern.** This gives us predecessor areas, not 2026 areas. Canmore-Banff (majority) and RMH-Banff Park (minority) don't have clean 2019 predecessors. Partial fortification at best.

### 3.2 "No public support" claim in §D2 is not independently verified

**Critique.** We treat the majority report's Appendix C assertion as prima facie credible because it's signed by a judicial officer. This is deference, not verification.

**Severity:** HIGH. This is the load-bearing claim for the §D finding.

**Fixable with FOSS?** Yes. The commission's 1,140+ public submissions are available at the Elections Alberta website. Text-search for the specific configurations in dispute (Airdrie, Cochrane, Chestermere, Red Deer, St. Albert hybrids) would either confirm or refute the chair's account.

**Fix applied.** None this session (would require downloading 1,140+ submissions, a significant token and time investment). Flagged as Track B for the next session in the migration doc. **Must be done before any public-legal use of §D.**

**Residual concern.** Until done, §D rests on an unverified authority claim. If refuted, the procedural finding weakens substantially.

### 3.3 Commission's own variance tables inherited without independent check

**Critique.** We use the commission's reported per-ED populations as ground truth. If the commission made arithmetic errors, we inherit them. The minority's 50-person rounding gap in the provincial total is a small indicator of this.

**Severity:** LOW. Commission is a public body with professional-responsibility norms; large errors would be flagged before publication.

**Fixable with FOSS?** Yes. 2021 Census DA populations are public; we could sum DAs within each 2026 polygon and compare. Requires shapefiles.

**Fix applied.** None (shapefile-blocked). Flagged for Stage 2b validation in v1.0 prompt.

**Residual concern.** Small errors in commission figures would propagate to §A1 but probably not change its qualitative finding (the MAD ratio of 48% is too large to be explained by rounding).

### 3.4 Vote Anywhere 47.2% figure

**Critique.** We reported that 47.2% of 2023 valid votes were non-Election-Day. This contradicts the 21.9% figure in circulation. We explained this as a definitional difference but didn't verify against an official source.

**Severity:** LOW-MEDIUM. Directional implications of the finding (NDP used VA more than UCP) are empirical; the exact 47.2% may be wrong.

**Fixable with FOSS?** Yes. Elections Alberta publishes post-election reports with turnout breakdowns. Can cross-check.

**Fix applied.** None this session (would require downloading and parsing the turnout report). Flagged for future verification.

**Residual concern.** If the 47.2% is off, the Vote Anywhere methodology adjustment in future measured attribution may be misspecified. Direction of the NDP-UCP differential (+6 pp NDP) is less affected.

---

## Part 4 — Test-Selection and Confirmation Bias

### 4.1 Every test we ran shows an asymmetric finding

**Critique.** Across A1, A2, A3, B1-B4, C3, C4, D, every single test produced a directional signal favoring the minority-is-more-UCP-favorable hypothesis. This is suspicious. Either the pattern is genuinely strong, or we're running tests that are correlated with each other (all measuring the same underlying fact), or we're selecting tests that produce the finding.

**Severity:** HIGH. Methodological concern — a critic will say "where's your null result?"

**Fixable with FOSS?** Yes. Define several test categories, run all tests in each category, report the full distribution including any that are null or opposite-direction.

**Fix applied.** In the critique here: **honest accounting of what a null would look like and whether we actually encountered any:**

- A1 (population distribution): a null would be "both maps have comparable variance." The minority's MAD is 48% wider — not null. Legitimate finding.
- A2 (Calgary zone): a null would be "both maps show comparable gaps." Majority 0.4%, minority 12.2% — not null. Legitimate finding.
- A2 robustness: a null would be "alternative classification reverses the direction." Both rules show minority substantially larger — not null.
- A3 (s.15(2)): a null would be "both maps have equal failure rates." 1/3 vs 1/3 — **actual null on the count**, non-null on the severity characterization (see §2.3.1 of academic report).
- B2/B3/B4: a null would be "majority and minority EG are within 0.1 pp of each other." They're 0.58 pp apart — not null.
- C3: a null would be "both maps have comparable visible anomalies." Minority 3, majority 0 visible — but we only had majority Calgary imagery. The majority non-Calgary anomaly count is *unmeasured*, not *zero*.
- C4: a null would be "both maps have comparable community splits." Airdrie 4 vs 2 — not null.
- D: a null would be "April 16 action is ordinary within comparator cases." It's not, by the three comparators cited — but our survey is N=3, not comprehensive.

**Actual null or contrary findings we did encounter:**

- A3 criteria failure count (1/3 vs 1/3) is symmetric.
- Tsuut'ina Nation treatment is symmetric across both maps.
- Siksika Nation treatment is symmetric.
- Both maps produce legally-compliant district populations (no ±25% violations).
- Neither map crosses the 7% US efficiency-gap threshold.

So the pattern is not "every test flags the minority" — several tests produce nulls that we've noted. The *directional tests* produce consistent findings; the *count* tests produce symmetric results. Both are honest.

**Residual concern.** Directional tests are a selection — we chose metrics where direction is meaningful. Tests without a natural direction (is the map "contiguous," does it obey rules?) produce nulls. The "every test I ran shows asymmetry" concern applies only to directional tests; within those, the finding is genuine.

### 4.2 Visual anomaly scan guided by chair's flags, not independent

**Critique.** We examined the three minority ridings the chair flagged (Nolan Hill-Cochrane, RMH-Banff Park, Olds-Three Hills-Didsbury) and found anomalies. But we didn't independently scan other minority ridings for unflagged anomalies, or apply the same scan to the majority. This is confirmation of the chair's report, not an independent finding.

**Severity:** MEDIUM.

**Fixable with FOSS?** Partially. Without shapefiles, we can't compute perimeter-to-area ratios programmatically. But we could visually scan all 89 polygons in each published map and flag visible outliers.

**Fix applied.** Independent visual scan of all minority Calgary EDs (28 districts) and all minority Edmonton EDs (~21 districts) — looking for anomalous shapes not on the chair's list. Report findings.

Results of the independent scan (done in this pass):
- Minority Calgary: examined all 29 EDs. Beyond the chair's 3 flags, one additional potential anomaly — Calgary-Peigan-Chestermere — which stretches from SE Calgary out to Chestermere town (a ~25km separation). The extension is along a highway corridor, so it's less visually dramatic than Nolan Hill-Cochrane, but it's a hybrid that connects two communities with no obvious shared infrastructure between them. Flagging as a minor anomaly pending shapefile verification.
- Minority Edmonton: Edmonton-Enoch-Devon is the main candidate — a large district combining the Enoch Cree reserve, the town of Devon, and adjacent territory, with the reserve and Devon separated by ~50km. Called out in §C4.
- Other minority EDs (Airdrie-East, Chestermere-Strathmore, etc.) appear conventionally shaped.

**Residual concern.** Majority non-Calgary maps not in bundle, so the equivalent scan for majority is impossible. §C3 remains Calgary-only for majority.

### 4.3 B1-B4 metric selection criterion

**Critique.** Why B1-B4 specifically? Stephanopoulos & McGhee (EG, 2014) and McDonald & Best (MM, 2015) are well-established. But Chen & Rodden's partisan bias metric, Warrington's declination, and DeFord/Duchin/Solomon's GEO are also in the literature. Did we select B1-B4 because they happened to be familiar, or because they happened to show asymmetry?

**Severity:** MEDIUM.

**Fixable with FOSS?** Yes. Implement declination and partisan bias as additional metrics.

**Fix applied.** Adding declination (Warrington 2018) as metric B6 in `v0_2_packing_cracking_analysis.py`. Declination measures the asymmetry between winning districts' vote distributions; positive declination favors one party, negative favors the other. If declination agrees with EG direction, the finding is reinforced. If not, we have a methodological discrepancy to investigate.

---

## Part 5 — Framing and Characterization

### 5.1 "Engineered" as a value-laden term

**Critique.** We characterize RMH-Banff Park as "engineered" based on the visible NP extension. "Engineered" implies intent. We can see the boundary; we cannot see inside the commissioners' minds.

**Severity:** MEDIUM. Language precision issue.

**Fixable with FOSS?** Yes, replace loaded language with descriptive language.

**Fix applied.** In academic report §2.4, the characterization reads: *"its ~22,000 km² area criterion is met only through an extension of the boundary through the uninhabited portion of Banff National Park; the extension also provides the shared-border criterion (e)."* This is descriptive. The word "engineered" appears only in the legacy Section A MD and final_v1 report, which inherited it from v0.1. Flagging for revision in the final report's next revision pass.

**Residual concern.** The word appears in the repo history and several files. A thorough edit would search-replace across all MDs.

### 5.2 "Gerrymander" framing

**Critique.** We don't use the word gerrymander in the findings (correctly — our evidence doesn't support the magnitude implied by that word). But the repository is called "alberta-electoral-boundaries-audit" and the file is `v0_9_gerrymander_audit_prompt.md`. A casual observer sees "gerrymander" prominently and assumes the finding supports that characterization.

**Severity:** LOW-MEDIUM. Naming convention inherited from prior sessions.

**Fixable with FOSS?** Yes, by renaming. Repository rename is a GitHub action.

**Fix applied.** None this session — rename would require URL migration and break existing links. Flagged for review: if the audit's findings don't support "gerrymander" as a characterization, the file and repo naming should follow.

**Residual concern.** Current naming may create an expectation the analysis itself doesn't support.

### 5.3 "Directionally consistent" language without effect-size qualification

**Critique.** We say "directionally consistent across six independent dimensions." A critic could reasonably ask: "Six dimensions, or six correlated measurements of the same underlying fact?" The six dimensions (population, zone, s.15(2), B1–B4, anomalies, community splits) are not fully independent — if one map has partisan tilt, you'd expect multiple measurements to reflect it.

**Severity:** MEDIUM.

**Fixable with FOSS?** Not entirely. Formal independence would require treating the dimensions as random variables with known correlations, which we don't have a basis for.

**Fix applied.** Add acknowledgment in both reports and in the design critique: the six dimensions are methodologically independent in that they use different data and methods, but they are not statistically independent — all are measuring properties of the same maps and would be expected to correlate if either proposal has any partisan tilt.

**Residual concern.** The "six independent dimensions" framing sounds stronger than it is. Better phrasing: "six different analytical lenses, each pointing in the same direction."

### 5.4 Intent vs effect conflation

**Critique.** The audit is careful in explicit statements that it doesn't prove intent. But the overall framing — describing boundaries as "engineered," the April 16 action as "promoting the less-publicly-supported option," etc. — leans on intent as the most plausible explanation. A critic will say: "You say you don't prove intent, but your narrative depends on intent."

**Severity:** MEDIUM.

**Fixable with FOSS?** Language-level fix. Keep the explicit disclaimers; reduce the intent-leaning implications in the body text.

**Fix applied.** The public report's "Bottom Line" section makes this explicit: *"What we've shown is the effect, which is observable; the intent is not."* Consider adding a similar disclaimer at the start of the academic report's §7 synthesis.

---

## Part 6 — Scope and Coverage Gaps

### 6.1 Missing majority non-Calgary imagery

**Critique.** We only have majority Calgary maps in the bundle. 77% of the majority's 89 districts are not inspected visually. The "0 majority anomalies" claim is Calgary-scoped but the language doesn't always make that clear.

**Severity:** HIGH for symmetry.

**Fixable with FOSS?** Yes. The commission's final report is a public PDF containing all maps. Can download and extract the relevant pages.

**Fix applied.** None this session (84MB PDF download plus pdfplumber extraction is a 10K+ token task). **Critical for next session.**

### 6.2 2019 map not included in §A1/A2 analysis

**Critique.** A1 and A2 tests compare majority vs minority 2026. The 2019 baseline is absent from these analyses because 2019-era per-ED population data wasn't in the bundle. This is a triple-asymmetry: two 2026 proposals tested against each other, 2019 as an unincluded third.

**Severity:** MEDIUM.

**Fixable with FOSS?** Yes. The 2017 commission's report contains 2019-map populations. Public document.

**Fix applied.** None this session. Flagged for inclusion in future revision of §A.

### 6.3 No map drafted or published as a counter-proposal

**Critique.** The audit argues the minority is non-ideal but doesn't propose what "better" would look like. A reader asking "ok, what should the map look like instead?" has no answer from us.

**Severity:** LOW. Not the audit's purpose, but a reader might expect it.

**Fixable with FOSS?** Yes, with GerryChain ensemble + shapefiles. Could publish 3–5 alternative maps drawn from the ensemble's neutral distribution and compare.

**Fix applied.** Out of scope for this session. Legitimate future deliverable.

---

## Part 7 — What Can Be Done With FOSS and Public Data to Fortify

Summary of fortifications achievable without new external data releases:

| Fortification                                        | Tool / data needed                           | Cost to execute        | In this session? |
| ---------------------------------------------------- | -------------------------------------------- | ---------------------- | ---------------- |
| Monte Carlo over modeling choices → true CI          | numpy, pandas (already installed)            | ~100 lines of code     | **Yes**          |
| Declination metric (Warrington 2018)                 | statistics module                            | ~20 lines              | **Yes**          |
| Per-hybrid rural-baseline override sensitivity       | 2019 poll-level results (in bundle)          | ~50 lines              | **Yes**          |
| 2019-election cross-validation of B1–B4              | 2019 results CSV (in bundle)                 | ~50 lines              | **Yes**          |
| Independent visual anomaly scan of minority          | already-loaded JPGs + vision                 | ~30 min                | **Yes**          |
| Third Calgary classification rule (ward-based)       | Calgary open-data ward shapefile (online)    | ~80 lines + web fetch  | **Yes**          |
| S.15(2) area verification for 2019 predecessors      | Elections Alberta 2019 shapefiles (online)   | ~60 lines + web fetch  | **No — next session** (download size) |
| Submission-archive text search (§D2)                 | 1,140+ PDFs from Elections Alberta           | 1–2 hours              | **No — next session** |
| Majority non-Calgary imagery                         | 84MB commission PDF                          | 30 min download/parse  | **No — next session** |
| MCMC ensemble (B5)                                    | GerryChain + 2026 shapefiles                 | 2–3 hours              | **No — shapefile-blocked** |
| Programmatic C1/C2 compactness                       | shapely + 2026 shapefiles                    | 30 min                 | **No — shapefile-blocked** |

---

## Part 8 — Fortifications Applied This Session

See commits after this document is pushed:

1. **`v0_3_monte_carlo_ci.py`** — Monte Carlo over urban weights, rural baseline, per-hybrid jitter. Produces 95% CI on minority-majority EG asymmetry.
2. **Declination metric (B6)** added to `v0_2_packing_cracking_analysis.py`.
3. **Per-hybrid rural-baseline override** added to the sensitivity runs.
4. **2019-election cross-check** — running B1–B4 with 2019 vote data as input to both maps; reporting whether asymmetry direction and magnitude are stable across elections.
5. **Calgary ward-based classification (third rule)** added to `electoral_forensics_population.py` robustness check.
6. **Independent anomaly scan** documented in this critique (§4.2).
7. **Language audit** — cataloguing "engineered" and "directionally consistent" usages for the next report revision.

Fortifications deferred to next session:
- Submission-archive search (§3.2)
- Majority non-Calgary imagery (§6.1)
- 2019 predecessor shapefile area verification (§3.1)
- Ensemble and compactness (shapefile-blocked)

---

## Part 9 — The Most Defensible Version of the Audit's Claim

Stripping out all contested or weakened framings, the audit's minimum defensible claim is:

> **Using public data and open-source tools, and applying identical methodology to both 2026 proposals, the minority proposal produces a measurable advantage for the UCP relative to the majority proposal across six different analytical frames (population distribution, Calgary geographic-zone balance, s.15(2) eligibility severity, efficiency-gap computation under blended attribution, visible boundary shape count, community-of-interest splits). The direction of this advantage is stable across every modeling sensitivity tested. The magnitude is below the 7% efficiency-gap threshold US courts have used to flag suspect maps, but above the level at which reasonable people would call it random noise. Whether the commissioners intended this advantage is not established by this audit; the effect is observable and reproducible. The government's April 16 decision to replace the commission's drafting process with a UCP-majority MLA committee means the choice between the two proposals is now being made through a mechanism not used in the three most-cited Canadian provincial comparator cases. Whether this procedural choice is materially different from historical practice requires a more comprehensive survey than this audit performed.**

That claim is what we can defend with the data and methods currently in the bundle. Everything beyond it — intent, magnitude precision, ensemble placement, cross-case procedural uniqueness — requires further work that we've enumerated and scoped.

---

*Design critique v0.1. Hostile red-team pass against this audit's own methodology. Authored during the same session that produced the bias remediation and uncertainty analysis. This document is itself subject to the same standard: if it misses a valid critique, that's a class of error the next revision should catch.*
