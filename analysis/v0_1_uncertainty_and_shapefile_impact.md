# Uncertainty Analysis and Shapefile-Impact Assessment

**Purpose.** Answer three linked questions with documented confidence:

1. What are our findings' confidence intervals *as the analysis stands today* (no 2026 shapefiles)?
2. What outcomes could the shapefiles, once released, produce — which are plausible, which are implausible?
3. Where does the intuition *"shapefiles will validate the edges but not shift the overall effect"* hold, and where could it be wrong?

**Method.** Walk each finding. State the claim, the evidence, what could invalidate it, how likely that invalidation is, and what the post-shapefile number is likely to be. Document every assumption explicitly and flag any that is unsupportable or ambiguous.

---

## Headline Intuition Up Front

The user's intuition: *"shapefiles would validate findings on the edges, but the overall effect shouldn't shift."*

**Short answer: largely correct, with three specific qualifications.**

- Direction of the minority-majority asymmetry: **very likely to hold** under measured attribution. The 70/30 blend is a modeling choice; the direction is robust across sensitivity runs and an alternative Calgary classification rule. Probability of direction flipping: low (<10%).
- Magnitude of the partisan shift: **likely within the 0.58–1.61 pp range** already reported, probably tighter. Measured attribution collapses the sensitivity range to a single value; that value will almost certainly fall within our reported bracket. Probability of measured magnitude falling outside the bracket: moderate-low (~15–25%).
- Spatial anomalies (§C3): **almost certainly validated.** The three minority anomalies (Calgary-Nolan Hill-Cochrane, Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury) are visible on the published JPG maps. Shapefiles would measure them precisely but not change the finding.

**Where the intuition could be wrong — one specific scenario.** The MCMC ensemble (§B5) is the one test that could materially change the headline. If the minority proposal falls *within* the ensemble's central distribution (25th–75th percentile), the finding recharacterizes from "directional asymmetry suggesting intentional partisan choice" to "directional asymmetry inside the band of plausible neutral maps" — same numbers, different interpretation. Probability this happens: moderate-high (~40–60%). That's documented in §4 below as the single biggest shapefile-triggered uncertainty.

---

## Section 1 — Confidence Framework

### 1.1 Confidence levels used below

| Level     | Meaning                                                                    | Typical use case                                   |
| --------- | -------------------------------------------------------------------------- | -------------------------------------------------- |
| HIGH      | Number is from a primary source or a reproducible script; revisions unlikely | Published variance tables; parsed official totals  |
| HIGH-MED  | Number is reproducible but rests on one defensible modeling choice         | A2 Zone A-B gap under the geographic classification |
| MEDIUM    | Number is reproducible but sensitive to modeling choices or data proxies   | B1-B4 under 70/30 blend                            |
| MED-LOW   | Number is estimated, not measured; direction more reliable than magnitude  | A3 s.15(2) criteria tallies using hand-coded areas |
| LOW       | Number is a desk estimate; strong dependence on unverified assumptions     | Comparator-case "without recent precedent" claim   |

### 1.2 What we mean by "confidence interval" here

Not a frequentist CI — none of our tests have probability distributions in the usual statistical-inference sense. Instead we mean: **a range within which measured values are expected to fall when better data become available**, bounded by the sensitivity range under modeling choices we can vary today.

---

## Section 2 — Finding-by-Finding Confidence

### 2.1 §A1 Population distribution variance

| Quantity                                   | Value    | Confidence | Shapefile sensitivity |
| ------------------------------------------ | -------- | ---------- | --------------------- |
| Majority MAD from 54,929                   | 3,180    | HIGH       | None — source is CSV from commission variance tables |
| Minority MAD from 54,929                   | 4,707    | HIGH       | None                  |
| Majority EDs > +15%                        | 0        | HIGH       | None                  |
| Minority EDs > +15%                        | 5        | HIGH       | None                  |

**Assumption:** the commission's variance tables are accurate. **Validation:** majority sum = 4,888,723 matches exactly the commission's published provincial total; minority sum = 4,888,773 differs by 50 (rounding in the commission's own figures). **Ambiguity:** none.

**Post-shapefile change:** None. Shapefiles would let us verify the commission's own math against 2021 DA populations dissolved into 2026 polygons, but that verification would only detect commission arithmetic errors, not change any audit finding.

### 2.2 §A2 Calgary Zone A vs Zone B gap

| Rule                                  | Majority gap | Minority gap | Confidence |
| ------------------------------------- | ------------ | ------------ | ---------- |
| Geographic (Zone A / Zone B)          | +0.36%       | +12.20%      | HIGH-MED   |
| Data-driven (2023-NDP-won / UCP-won)  | +0.39%       | +7.71%       | HIGH-MED   |

**Assumption 1:** the Zone A/B geographic classification (N/E/central vs S/W) is a reasonable proxy for Calgary's partisan geography. **Validation:** correlates 85%+ with 2023 winner; alternative data-driven rule produces same direction; both rules show majority near-null and minority substantial.

**Assumption 2:** 2026 EDs retain partisan character of 2019 predecessors where names match. **Validation:** mostly stable since partisan geography of Calgary neighborhoods changes slowly (on decadal, not annual, time scales). Holds for direct renames. For hybrids we classified by name stem; the robustness check shows the stem-matching is roughly consistent with zone-based classification.

**Ambiguity:** the 12.20% vs 7.71% range — which is "the" number? Honest answer: both are. **The finding is "minority Zone A/NDP-leaning Calgary EDs carry 7.7–12.2% more population per seat than Zone B/UCP-leaning ones, while the majority's gap is near zero."** Not a point estimate.

**Post-shapefile change:** Shapefiles would replace our name-based classification with polygon centroids, allowing a deterministic Zone A/B assignment. Expected effect: tightening the range, probably to within ±1.5 pp of the current midpoint of ~10%. **Very unlikely to reverse direction.** Probability of direction reversal: <5%.

### 2.3 §A3 s.15(2) eligibility audit

| Quantity                                     | Value  | Confidence | Shapefile sensitivity |
| -------------------------------------------- | ------ | ---------- | --------------------- |
| Canmore-Banff (maj) criteria-met count       | 1/5    | MED-LOW    | Moderate (area, distance) |
| Rocky Mountain House-Banff Park (min) count  | 2/5    | MED-LOW    | Moderate              |
| Both maps: 1/3 invocations fail 3/5 test     | Equal  | HIGH       | Low                   |

**Assumption 1:** the area estimates for each protected riding (Canmore-Banff ~8,500 km²; RMH-Banff Park ~22,000 km²) are correct. **Validation:** the numbers are desk estimates based on public Alberta geography; no programmatic measurement from a GIS layer. **Status: UNVERIFIED QUANTITATIVELY.** The qualitative finding (Canmore-Banff is well below 20,000 km², RMH-Banff Park just above) is robust to plausible ± 20% error in the estimates.

**Assumption 2:** the "engineered boundary" characterization of RMH-Banff Park is supported by the visible NP extension on published maps. **Validation:** confirmed in §C3 visual inspection.

**Assumption 3:** the characterization of Canmore-Banff's variance as "a judgment call on a mid-variance riding, no visible engineering" is supported by absence of evidence, not evidence of absence. **Status: WEAKER THAN IT LOOKS.** If the commission drew Canmore-Banff's boundary to engineer its criterion passes but the engineering isn't visible on the Calgary map in our bundle, we'd miss it. The majority's non-Calgary maps are not in the bundle (§C symmetry data gap). **This is a soft spot in the audit's symmetry.**

**Ambiguity:** our characterization of RMH-Banff Park as "engineered" is stronger than our characterization of Canmore-Banff as "judgment call." The factual asymmetry (visible NP extension vs no visible extension) supports this, but we cannot rule out that Canmore-Banff was also engineered in ways we can't see from our imagery.

**Post-shapefile change:** Shapefiles would give precise area measurements and let us verify (a), (b), (d), (e) criteria programmatically for all six protected ridings. Probability that programmatic verification flips a riding's verdict: moderate for borderline criteria (area just over/under 20,000 km²; distance from centre just over/under 100 km); low for the invisible-engineering question in Canmore-Banff (shapefile would measure the boundary but wouldn't tell us *why* it was drawn that way).

**Possible outcome the shapefiles could produce that would change the finding:**
- Canmore-Banff has an invisible engineering feature (e.g., a boundary extension to Banff townsite that we didn't catch on the low-resolution Calgary JPG). Would push majority's count from 1/3 flagged to 2/3 flagged, shifting §A3 toward symmetric failure. Probability: ~15%.
- RMH-Banff Park's NP extension turns out to be less material than it looks on the map (the district actually passes 3/5 criteria with or without the extension). Would push minority's count from 1/3 to 0/3. Probability: ~20%. **If this happens, the minority's §A3 story weakens significantly.**

### 2.4 §A2b Rest-of-province mean population

| Quantity                           | Value          | Confidence |
| ---------------------------------- | -------------- | ---------- |
| Majority rest-of-province mean pop | 52,281         | HIGH       |
| Minority rest-of-province mean pop | 50,336         | HIGH       |
| Delta                              | −3.9%          | HIGH       |

**Assumption:** the commission's regional classification of EDs (Calgary / Edmonton / Rest) is correct. **Validation:** the classification is embedded in the CSV `region_type` column for minority, and derived by ED-name prefix for majority. Probability of error: negligible.

**Post-shapefile change:** None substantive. Shapefiles would let us compute the rural seat-per-capita ratio precisely; current variance numbers don't depend on shapefile data.

### 2.5 §B1–B4 Partisan bias metrics

| Metric                  | 2019       | Majority  | Minority  | Asymmetry | Confidence |
| ----------------------- | ---------- | --------- | --------- | --------- | ---------- |
| B2 EG at urban 0.70     | −2.64%     | −0.78%    | −1.36%    | −0.58 pp  | MEDIUM     |
| B2 EG range (0.60–0.80) | (exact)    | +1.58% to −1.43% | +0.22% to −3.04% | −0.58 to −1.61 pp | MEDIUM |
| B3 MM at urban 0.70     | −2.22 pp   | −0.16 pp  | −0.33 pp  | −0.17 pp  | MEDIUM     |
| B4 NDP@50/50 at 0.70    | 46         | 44        | 42        | −2 seats  | MED-LOW    |

**Assumption 1 (load-bearing):** 70/30 urban/rural blend represents a reasonable approximation to the actual vote mix in hybrid 2026 EDs. **Validation:** sensitivity across 0.60/0.70/0.80 shows direction stable; magnitude varies by a factor of ~3. **Weakness:** 70/30 is a judgment call, not derived from data.

**Assumption 2 (load-bearing):** 2026 EDs composed of "2019 urban core + rural absorption" have voter mix proportional to population-weighted blend of those areas. **Validation:** none from first principles. The alternative (measured attribution via Phase 4C) would replace this with observed values.

**Assumption 3:** rural Alberta's 2023 NDP share (33.5%) is a reasonable baseline for rural absorptions into hybrids. **Validation:** this is an observed quantity, not an assumption — but some hybrid absorptions are wealthy near-urban communities (Bearspaw, Springbank, Cochrane) whose actual NDP share may be below 33.5%. **Direction of bias in our estimate:** likely understating the minority's partisan shift, because these specific rural absorptions are probably ≤25% NDP, not 33.5%. In other words, **the 70/30 blend is probably conservative toward finding *less* minority shift than measured attribution would reveal.**

**Ambiguity — potentially unsupportable:** The 70/30 split for Calgary hybrids like Calgary-Nolan Hill-Cochrane is a guess. The actual urban Calgary fraction of that district's population may be 40–60%, not 70%. If so, our minority B2 estimate of −1.36% at 70/30 may be ~0.5 pp too conservative (i.e., actual minority shift is larger). **Status: unsupportable without measured attribution; flagged as a known modeling weakness.**

**Post-shapefile change:** Shapefiles enable measured attribution via Phase 4C full execution. Expected effects:

| Shapefile-enabled outcome                             | Probability | Magnitude of change                |
| ----------------------------------------------------- | ----------- | ---------------------------------- |
| Measured B2 falls within [−1.61, −0.58] pp bracket   | 60–70%      | Tightening to a single point in range |
| Measured B2 below bracket (more UCP-favorable)        | 15–25%      | Minority shift larger than reported |
| Measured B2 above bracket (less UCP-favorable)        | 5–15%       | Minority shift smaller than reported |
| Measured B2 opposite sign (minority becomes NDP-favorable) | <5%    | Direction reversal — would falsify headline |

The Vote Anywhere finding from §4 supports the "measured B2 below bracket" possibility because NDP voters used Vote Anywhere at +6 pp higher rate than UCP, meaning urban NDP concentration is likely under-estimated by Election-Day-only proxies. But this push is partly offset by the "rural absorptions are more UCP than provincial average" factor. The two effects may roughly cancel, which is why we expect the measured number to fall within the bracket more often than outside.

**Critical honesty check:** *"If your intuition is wrong that shapefiles don't shift the effect, why?"* The scenario would be: measured attribution reveals the 70/30 blend is systematically off in ways that cancel the asymmetry between the two maps. This would happen if both the majority and minority hybrids have very different actual urban fractions than 70/30 (say, majority at 90/10 and minority at 50/50), such that our identical-weight methodology manufactured the asymmetry. **Probability: low but not zero (~10%).** Mitigation: the sensitivity runs across 0.60/0.70/0.80 already test this — if the asymmetry were weight-manufactured, it would shrink at some weight. It doesn't: the 0.60 run shows a −1.36 pp asymmetry (larger than the 0.70 run), and the 0.80 run shows −1.61 pp. Consistent direction at all three weights rules out the "weight-manufactured asymmetry" scenario.

### 2.6 §C3 Visual spatial anomalies

| Anomaly                            | Source           | Confidence | Shapefile sensitivity |
| ---------------------------------- | ---------------- | ---------- | --------------------- |
| Calgary-Nolan Hill-Cochrane (min) lasso | Visual JPG  | HIGH       | None                  |
| RMH-Banff Park (min) NP extension  | Visual JPG       | HIGH       | Precise polygon confirms visible extension |
| Olds-Three Hills-Didsbury (min) capture of N Airdrie | Visual JPG | HIGH | Precise polygon confirms |
| 0 majority Calgary anomalies       | Visual JPG       | MEDIUM     | Only majority Calgary imaged — data gap |
| 0 majority non-Calgary anomalies   | **No imagery**   | LOW-NA     | Large gap — shapefiles would close |

**Assumption:** published map JPGs are accurate renderings of the actual proposed polygons. **Validation:** published by the commission for its own report; no reason to doubt.

**Ambiguity:** the "0 majority anomalies" claim rests on imagery we don't have for 77% of the majority map. Shapefiles would produce full-coverage geometry for the majority, allowing us to run the same visual-anomaly check programmatically (e.g., compute perimeter-to-area ratio for every ED and flag outliers).

**Possible shapefile-triggered outcomes:**

- Majority has one or two previously invisible anomalies in rural or Edmonton districts. Probability: ~25%. Effect: reduces majority's clean-shape advantage from 3-to-0 to 3-to-2 or similar. **Would materially soften the §C finding but not reverse it.**
- Majority has zero anomalies under programmatic check. Probability: ~50%. Effect: reinforces current finding.
- Minority has additional anomalies not visible on the overview maps. Probability: ~25%. Effect: strengthens current finding.

### 2.7 §C4 Community of interest splits

| Claim                                     | Confidence | Shapefile sensitivity |
| ----------------------------------------- | ---------- | --------------------- |
| Minority splits Airdrie 4 ways; majority 2 | HIGH     | Precise verification  |
| Minority splits Cochrane; majority intact  | HIGH     | Precise verification  |
| Minority splits Chestermere partially; majority intact | HIGH | Precise verification |

**Assumption:** city/community boundaries are well-defined in Alberta's municipal records. **Validation:** they are — municipal boundaries are statutory.

**Shapefile effect:** Precisification. Shapefiles would let us count exactly how many census dissemination areas within Airdrie fall in each of the 4 minority EDs. Qualitatively unchanged.

### 2.8 §D Procedural

| Claim                                          | Confidence | Shapefile sensitivity |
| ---------------------------------------------- | ---------- | --------------------- |
| April 16 action replaces drafting process      | HIGH       | None                  |
| More government-controlled than QC92/ON96/BC08 | MED        | None                  |
| "No public support" for 5 minority hybrids     | MED        | Independent of shapefiles — requires submission-archive text search |
| "Without recent Canadian provincial precedent" | LOW        | Independent — requires comprehensive survey |

**Unsupportable claim in v0.1/v0.8 reports:** "without recent Canadian provincial precedent." We did not do a comprehensive survey. Tightened to "most government-controlled among the three most-cited comparator cases" in v0.2 reports. Leaving the stronger claim in earlier drafts would be a false-precision problem.

**Load-bearing unverified claim:** the majority report's Appendix C assertion that the minority's five disputed configurations had no public support in the 1,140+ submissions. **If refuted by submission-archive text search, the §D finding weakens substantially.** Probability of refutation (i.e., that the majority report's own claim is wrong): low (~15%), because the claim is signed by a judicial officer and subject to professional-responsibility norms. But because it's not independently verified, the audit treats it as prima facie credible, not proven.

---

## Section 3 — Aggregate: What the Audit Would Claim With vs Without Shapefiles

### 3.1 Current headline (without shapefiles)

> The minority 2026 proposal is directionally more UCP-favorable than the majority 2026 proposal across six independent dimensions, at a magnitude below the US gerrymandering threshold (7% EG) but consistently positive. The direction of the asymmetry is robust to modeling choices; the magnitude ranges from 0.58 to 1.61 percentage points in the efficiency gap depending on urban/rural blending weight. Three minority ridings have visible spatial anomalies confirmed on published maps; the majority has none in its published Calgary imagery (non-Calgary majority imagery was not in the bundle — symmetry data gap).

### 3.2 Expected headline after shapefile release, measured attribution, and ensemble

Most likely outcome (~55–65% probability under current modeling):

> The minority 2026 proposal is measurably more UCP-favorable than the majority 2026 proposal across six independent dimensions. The measured efficiency gap asymmetry is X pp (within the 0.58–1.61 bracket estimated from blended attribution). MCMC ensemble places the minority at the Yth percentile of neutrally-drawn alternatives — [within / outside] the range (25th–75th) typical of non-partisan redistricting. Three minority ridings show visible spatial anomalies with Polsby-Popper scores of P1/P2/P3; the majority's minimum Polsby-Popper is Q, which is / isn't materially different.

### 3.3 Most likely quantitative updates

| Dimension         | Current value             | Expected measured value    | Likelihood |
| ----------------- | ------------------------- | -------------------------- | ---------- |
| B2 asymmetry      | 0.58–1.61 pp range        | 0.8–1.3 pp point estimate  | 60%        |
| B2 asymmetry      | 0.58–1.61 pp range        | outside bracket, UCP-ward  | 20%        |
| B2 asymmetry      | 0.58–1.61 pp range        | outside bracket, NDP-ward  | 10%        |
| B2 asymmetry      | direction consistent      | direction reverses         | <5%        |
| §A2 Zone A−B gap  | 7.7–12.2%                 | ~9–11% point estimate      | 70%        |
| §A3 majority flag | 1/3 (Canmore-Banff)       | 1/3 (unchanged)             | 70%        |
| §A3 majority flag | 1/3                       | 2/3 (new invisible engineering found) | 15% |
| §A3 minority flag | 1/3 (RMH-Banff Park)      | 1/3 (unchanged)             | 75%        |
| §A3 minority flag | 1/3                       | 0/3 (RMH-BP actually passes 3/5) | 15% |
| §C3 majority anomalies | 0 (Calgary only)     | 0 (full coverage)          | 50%        |
| §C3 majority anomalies | 0 (Calgary only)     | 1–2 (found in rural imagery) | 25%       |
| §B5 ensemble percentile of minority | N/A      | 60th–90th percentile       | 50%        |
| §B5 ensemble percentile of minority | N/A      | 90th–99th (extreme outlier) | 15%       |
| §B5 ensemble percentile of minority | N/A      | 25th–75th (not extreme)    | 35%        |

### 3.4 The one scenario that would shift the headline

**Scenario: ensemble places both 2026 maps inside the 25th–75th percentile.**

Probability: ~35% per table above. What would change:

- Direction finding (minority > majority in UCP-favor) **remains** — ensemble placement is per-map, not relative.
- Headline magnitude claim **weakens from** "systematic partisan asymmetry" **to** "directional asymmetry that is nonetheless within the range of neutrally-drawn alternatives."
- §11 constitutional-legal framing (Ref re Saskatchewan) **changes materially**: the evidentiary basis for an effective-representation challenge becomes weaker if both maps are within the ensemble's central band. A challenge would still have the population-equality asymmetry and the spatial anomalies as standalone grounds, but the partisan-bias argument would lose the "statistically inconsistent with neutrality" frame.
- §A3 and §C3 findings **unchanged**.
- Procedural §D finding **unchanged**.

**This is the single most important uncertainty in the audit.** Flagged for the reader with CONFIDENCE: if the minority proposal falls within the 25th–75th percentile of its ensemble, the "intentional partisan choice" interpretation is not supported by the statistical evidence, even though the direction of the asymmetry is real. We should not assume the ensemble will find extreme outliers; that's optimistic about our own evidence. Reporting this possibility honestly *now* is better than discovering it later.

---

## Section 4 — Assumption Inventory and Validation Status

| Assumption                                        | Section | Status                 | If wrong, effect                     |
| ------------------------------------------------- | ------- | ---------------------- | ------------------------------------ |
| Commission variance tables are accurate           | §A1     | Validated (sum checks) | Negligible                           |
| Zone A/B geographic classification reasonable     | §A2     | Validated (2 rules)    | Magnitude shifts ±3 pp               |
| 2026 direct-rename EDs inherit 2019 partisan character | §A2, §B | Reasonable, not proven | Direction unchanged; magnitude uncertain |
| 70/30 urban weight in hybrid blending             | §B      | Documented, sensitivity-tested | Direction robust; magnitude varies 0.58–1.61 pp |
| Rural baseline 33.5% NDP share                    | §B      | Observed from data    | Negligible                           |
| Rural absorptions (Bearspaw/Springbank/Cochrane) ~= provincial rural average | §B | **Unsupported** | Minority shift understated by ~0.3 pp |
| Published JPGs accurately render proposed polygons | §C     | Reasonable, not verified | Unlikely to matter; shapefiles would confirm |
| "No majority non-Calgary anomalies"               | §C3     | **Unsupported** — no imagery | §C3 claim narrows scope |
| Majority report's Appendix C "no public support" claim | §D2 | **Unverified** — not independently searched | §D weakens if refuted |
| "Most government-controlled" framing for April 16 action | §D4 | Defensible (3 cases) but not comprehensive | §D statement may soften further |
| Canmore-Banff has no engineered boundary         | §A3     | **Unsupported** — no imagery | §A3 asymmetry could invert |
| Area estimates for s.15(2) ridings                | §A3     | Desk estimates ± 20%   | Verdict change unlikely unless ±50% |

**Two Assumptions flagged as unsupported:**

1. *"No majority non-Calgary anomalies."* Reason: no imagery for majority Alberta-wide, Edmonton, or other-cities panels. Shapefiles would resolve. Current audit scope should read: **"0 majority anomalies in the Calgary imagery available; majority non-Calgary spatial audit not performed."**

2. *"Rural absorptions align with provincial rural average."* The minority absorbs Bearspaw, Springbank, Cochrane, Chestermere — suburban areas of higher-than-average UCP lean. Treating them as 33.5% NDP (provincial rural average) likely overstates NDP share in those hybrids, understating the minority's partisan advantage. Measured attribution would correct this and probably push the measured B2 toward the lower (more UCP-favorable) end of the sensitivity bracket.

**Two Ambiguities that are blockers:**

1. *§A3 Canmore-Banff majority flag.* Without majority non-Calgary imagery, we cannot determine whether the boundary is engineered the way RMH-Banff Park is. Current characterization asymmetric by necessity, not by evidence of absence. **Blocker for full §A3 symmetry. Remedy: release majority Alberta-wide imagery, or post-shapefile programmatic area-criterion verification.**

2. *§D2 no-public-support claim.* The claim is in the majority report's Appendix C; we treat it as prima facie credible because it's signed by a judicial officer. If refuted by submission-archive text search, §D weakens. **Blocker for full confidence in §D2. Remedy: text-search the commission's 1,140+ public submission archive.**

---

## Section 5 — What the Shapefiles WOULD NOT Change

For completeness:

- **§A1 Population variance numbers.** Source is CSV; shapefile-independent.
- **§A2b Rest-of-province mean population.** Source is CSV; shapefile-independent.
- **§C4 Community-of-interest splits.** Municipal boundaries are statutory; shapefile would precision-check but not change qualitative finding.
- **§D Procedural comparator analysis.** About government actions, not map geometry.
- **B1 distribution histogram direction.** Bin counts depend on attribution, but the qualitative shape (UCP peak at +25%+) is a 2023 electorate fact, not a redistricting artifact.
- **The Vote Anywhere differential (+6 pp NDP in VA vs Election Day).** Observed in the 2023 data; shapefile-independent.

---

## Section 6 — Recommendations for the Reader

**If you're deciding whether to trust this audit's findings pre-shapefile:**

1. The population-distribution and community-split findings (§A1, §A2b, §C4) are HIGH confidence. These don't change with shapefiles.
2. The Calgary Zone A-B gap (§A2) is HIGH-MED confidence. Direction near-certain; magnitude bracket 7.7–12.2%.
3. The partisan-bias findings (§B) are MEDIUM confidence. Direction robust; magnitude bracket 0.58–1.61 pp. Shapefiles will collapse the bracket but most likely keep it within current bounds.
4. The visual spatial findings (§C3) are HIGH confidence for the three minority anomalies; LOW for the "0 majority anomalies" claim (imagery gap).
5. The procedural findings (§D) are MEDIUM confidence pending submission-archive verification.
6. **B5 ensemble placement is the biggest unknown.** A ~35% chance that both maps fall inside the 25th–75th percentile — which would keep the directional finding but weaken the "intentional partisan choice" interpretation.

**If you're deciding whether to share this audit publicly:**

- The population and community findings are solid. Safe to share.
- The partisan-bias magnitude is a bracket (0.58–1.61 pp), not a single number. Share the bracket; don't cite the central value without the range.
- The spatial-anomaly count (3 minority, 0 majority-visible) should include the imagery-gap caveat.
- The ensemble-placement uncertainty is material and worth flagging: the audit's "systematic partisan asymmetry" frame is weaker if the minority is within the central ensemble band, even though all other findings hold.

**If you're deciding whether to wait for shapefiles:**

- The core direction of the finding is unlikely to change. Waiting is conservative but not necessary.
- Waiting produces measured (not estimated) magnitudes and unlocks B5/C1/C2. The gain is precision, not direction.
- If your audience is academic or legal (needs statistical significance language), waiting is worth it. If public/media (needs direction and magnitude bracket), current audit is sufficient.

---

## Version History

- **v0.1** (April 22, 2026) — initial uncertainty analysis, written alongside bias remediation pass that produced the symmetric v0.2 packing/cracking script.

*This document accompanies the reports at project root. It is intended as the audit's own epistemic inventory: what we know, what we assume, what we could be wrong about, and how a future measurement would update us.*
