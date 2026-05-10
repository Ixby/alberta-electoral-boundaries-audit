# Six Thinking Hats Analysis — Alberta Electoral Boundary Audit
## Pass 2: Scientific Validity and Methodological Trustworthiness

*Framework: Edward de Bono's Six Thinking Hats. Pass 2 focuses specifically on the scientific credibility of the audit — what the methodology can and cannot support, where the red-team findings land, and what a peer reviewer would say.*

---

## WHITE HAT — The Methodological Record

### Geometry pipeline (eight stages)

The audit's geometry is derived from a multi-stage pipeline because no official shapefiles were available at time of initial analysis. The pipeline:

**v0_1:** Initial canonical from Commission PDF maps. Perimeter error ±500 m–1 km.
**v0_2:** Topology cleanup. Majority had 2,754 km² overlap; minority had 16,734 km² — six times more.
**v0_3:** Population-swept hybrids (Census DA populations allocated proportionally).
**v0_4:** Municipal anchoring — CSD boundary snap at 500 m tolerance.
**v0_5:** DA extension — 150 m tolerance, ±1–5 m accuracy on anchored segments.
**v0_6:** Inter-ED confidence propagation.
**v0_7 (post-May-6):** Multi-source assembly with per-ED provenance tracking using official shapefiles.
**v0_8:** DPG perfecter — four-phase topology resolution, gap-fill, precision pass.
**v0_8.1:** Nested-polygon ownership inversion for residual overlaps.
**v0_8.2:** 2019-Tier-A inheritance fill: 21 majority EDs, 12 minority EDs had zero geometry and inherited from 2019 enactment boundaries.

**Coverage achieved:** 89/89 EDs at 100% coverage for both maps after v0_8.2.

**Sunset clause triggered:** May 6, 2026, when Elections Alberta released official shapefiles. Canonical ensemble re-run completed.

### MCMC ensemble specifications

- **Platform:** GerryChain
- **Runs reported:** 10,000 plans (2023 substrate)
- **Effective Sample Size (ESS):** ~148–160 per metric (autocorrelation time τ = 624–674)
- **ESS implication:** Tail percentile precision far lower than raw run count implies
- **Minority EG p-rank (ESS-adjusted):** p98.76 (previously reported as p100 — CRITICAL error, corrected)
- **Majority EG p-rank (ESS-adjusted):** p92.66
- **2M run ensemble:** Core findings trusted; critical dict-iteration bug already fixed before primary run

### Vote attribution methods tested

**Rule A:** Drop third-party votes (58,232 votes, 3.30% excluded)
**Rule B:** Allocate proportionally to two-party vote
**Rule C:** Allocate to nearest major-party winner
**Crosswalk-blended:** Urban weight w ranging 0.60–0.90 (primary: w=0.85)

All methods tested; directional findings documented across all.

### Pre-registration architecture

**What was pre-registered before analysis:**
- Population equality thresholds (A1)
- Zone classification criteria (A2)
- s.15(2) eligibility criteria (A3)
- Municipal anchoring methodology
- The 17-test scoring grid for the November 2026 Lunty committee map

**What was not pre-registered (disclosed):**
- P/C/E signature detection framework — criteria committed in same analytical pass as detection ("retrospectively-defined," not pre-registered)
- E2 reformulation — criterion changed mid-audit after initial formulation failed detection
- Keyword list for submission analysis — pre-dates formal checklist (researcher degrees of freedom)

### Red-team taxonomy and resolution status

**CRITICAL (4 identified, 4 addressed):**
- S1-01: "2h 24m separation" between P/C/E specification and detection run was false (same commit). **Retracted; retrospectively-defined label applied.**
- S2-01: MCMC ESS ≈150 — p100 claim overstated. **ESS-150 tail downgrade; p100 → p95.35/p2.5.**
- S2-02: 100k full-coverage rescore contradicted §3.11 headline. **Canonical shapefiles recompute; Phase 4C + MCMC rewired.**
- S9-01: "p100" / "every one of 10,000" over-claims. **ESS-adjusted language; two-measurement reframing.**

**HIGH (8 identified, disclosed but not all corrected):**
- S1-02: Submission keyword list pre-dates checklist (researcher DoF)
- S1-03: E2 reformulation fits optional-stopping pattern
- S1-04: Counter-tests caveat not fully propagated through paper
- S2-03: No family-wise error-rate control across 21 tests (Bonferroni per-test α = 0.0024)
- S2-04: B4 uniform-swing violation not quantified
- S2-05: Canadian base-rate "71st percentile" claim is circular
- S9-02: "Three formal signatures" tighter than evidence supports
- S9-03: "Six dimensions" collapses to four analytical families

### Dependency graph
- 234 analytical nodes
- 454 directed edges
- Tracks all finding cascades and orphaning relationships
- Allows precise identification of which findings survive any given dataset invalidation

---

## RED HAT — Emotional and Intuitive Responses to the Methodology

### On the red-team process itself
It is genuinely unusual and admirable that a solo researcher commissioned a structured red-team of their own work, published the findings in full, and addressed the critical issues publicly. The instinct is to respect this. Most research — academic, government, or private — does not do this.

### On the CRITICAL errors
Learning that the audit initially reported p100 (every one of 10,000 plans) for the minority EG percentile when the ESS-corrected figure is p98.76 produces real discomfort. That's not a rounding error — it's a qualitative claim difference. p100 means "more extreme than every plan in the ensemble." p98.76 means "more extreme than 98.76% of plans." These are different sentences. The correction is the right call. But the initial overclaim was significant.

Similarly, learning that the "2 hours 24 minutes separation" between specification and detection was false produces a jarring reaction. A reader who encountered that specific framing would have concluded the P/C/E analysis was prospectively specified. It was not. The retraction is correct, but the original framing was misleading.

### On the E2 reformulation
There is something uncomfortable about a criterion being reformulated after the initial version fails to detect the target. Even with full disclosure, the reformulation process produces the feeling that the framework was adjusted to find what the researcher suspected was there. This feeling does not mean the finding is wrong — the RMH-Banff Park boundary extension through uninhabited national park is visually anomalous regardless of what the criterion says. But the feeling is real and should be taken seriously.

### On the ESS of 148–160
Running 10,000 MCMC plans and getting an effective sample size of 148 due to autocorrelation is humbling. It means the ensemble is much less informative about the tails than the headline number suggests. The reaction is not that the result is wrong — p98.76 is still a meaningful outlier — but that the precision of the claim is much lower than the run count implies.

### On the 21 unadjusted tests
Knowing that 21 statistical tests were conducted without family-wise error rate correction produces unease. Some of what appears significant at α=0.05 would not survive Bonferroni correction at α=0.0024. The audit discloses this but does not correct it. The feeling is that individual test statistics in the paper should be read with caution.

### On the overall scientific posture
The honest answer to "how scientifically trustworthy is this?" is: trustworthy on the structural findings, appropriately cautious on the partisan-bias findings, and correctly positioned on what it claims versus what it does not claim. The emotional read is that the author has been doing the right things, caught real problems, and fixed them. That deserves credit.

---

## BLACK HAT — Scientific Risks and Critical Assessment

### Problem 1: The family-wise error rate is the most persistent methodological flaw
21 statistical tests. No correction. At Bonferroni α=0.0024, multiple results that appear individually significant at α=0.05 would not survive. The paper discloses this as HIGH issue S2-03 but does not apply the correction. The defense — that the finding rests on directional consistency across multiple dimensions, not on any individual test crossing a threshold — is the right scientific posture, but individual test statistics in the paper remain potentially misleading to readers who will take them at face value.

### Problem 2: The P/C/E framework cannot carry formal evidentiary weight
Three issues compound here:
(a) Criteria were committed in the same analytical pass as detection — same commit, same session. This is disclosed and relabeled, but disclosure does not fix the researcher degrees-of-freedom problem.
(b) E2 was reformulated mid-audit after the initial version failed detection. This is disclosed as an optional-stopping risk, which is the correct label. But the E2 criterion as published is the one that detects the anomaly, not the original one.
(c) Counter-tests (Lethbridge and Red Deer 4-way splits) were detected in the same pass and held from formal count. The rationale for holding them is documented, but the researcher has selectively reported signatures, not all detected patterns.

Together, these three issues mean the P/C/E framework's three signatures cannot be treated as the results of a pre-registered confirmatory analysis. They are exploratory findings, correctly labeled as such, but structurally equivalent to data-dredging with subsequent rationalization. This is not fatal — exploratory analyses are scientifically legitimate — but they carry appropriately lower evidential weight.

### Problem 3: The declination metric's direction disagreement is not resolved, only acknowledged
Declination (Warrington 2018) shows the minority map as *least* UCP-favorable of the three maps. EG and Mean-Median show the minority map as most UCP-favorable. These metrics are designed to capture different aspects of partisan geometry. But the directional disagreement is not resolved by acknowledging it — it is a substantive scientific problem. Two metrics pointing one way and one pointing the other way means the researcher's choice of primary metric materially determines the conclusion. The paper correctly does not suppress the disagreement, but it also does not provide a principled basis for preferring EG/MM over Declination.

### Problem 4: The 338Canada direction reversal is unexplained
Under April 2026 polling, the minority map yields +1 NDP seat. This is the opposite direction from the EG finding under 2023 election results. The audit notes this reversal but attributes it to vote-distribution dependence without quantifying the mechanism. The critical question — which election environment is more representative of future Alberta elections — is not addressed. If the minority map yields NDP-favorable seat outcomes under most plausible future vote shares, the entire framing of the partisan-bias section requires revision.

### Problem 5: No independent replication
The audit has not been independently re-run by a third party. The code audit was by AI (Gemini 3.1 Pro), not a human academic statistician. The geometry pipeline is eight stages of custom code. An undetected bug at any stage could propagate through all downstream findings in ways the dependency DAG does not catch if the bug is in a foundational assumption rather than an individual script.

### Problem 6: The Canadian base-rate "71st percentile" is circular (HIGH, S2-05)
The claim that the minority map is at the "71st percentile" of Canadian redistricting processes appears to use Alberta's own commission methodology as part of the benchmark. This is circular — using the standard being evaluated to construct the reference distribution. The audit flags this as a HIGH issue but has not corrected it.

### Problem 7: The uniform-swing B4 violation is documented but not quantified (HIGH, S2-04)
The Seats-at-50/50 metric assumes uniform swing across ridings — an assumption acknowledged to be violated for Alberta, where urban NDP margins and rural UCP margins behave very differently. The CI overlap (43–46 vs 41–47) is the published finding. But the degree to which the uniform-swing assumption inflates or deflates the CI is not quantified. The finding could be artifactual.

### Problem 8: The "six dimensions" collapse to four families (HIGH, S9-03)
The paper presents findings as six independent dimensions. The red-team identifies that these collapse to four analytical families (structural population, geographic-zone symmetry, boundary coherence, and partisan bias). The "six dimensions" framing may overstate independence.

---

## YELLOW HAT — What the Methodology Gets Genuinely Right

### The structural findings require no vote data and cannot be questioned on partisan-bias grounds
The MAD comparison, the Calgary zone gap, the Airdrie split count, and the municipal anchoring percentage are direct measurements from the commission's own maps. They do not depend on vote attribution, election baseline, or partisan-bias metric choice. They cannot be reversed by choosing a different electoral substrate. This is the correct foundation for any redistricting audit.

### The DPG pipeline is the right engineering response to missing official data
Before May 6, 2026, no official shapefiles existed. Building a provisional geometry pipeline from published commission materials, census DA data, and municipal boundaries was the only scientifically defensible approach. The eight-stage pipeline, with documented uncertainty ranges at each stage, is correctly engineered. The sunset clause automatically triggering recomputation on official shapefile receipt is the correct scientific commitment.

### The falsifiability gates are genuinely rigorous
G1–G5 provide specific, testable conditions that would invalidate each class of finding. This is the correct scientific structure. Having retraction conditions documented before any attack on the findings is the right order of operations. It makes the project's epistemological commitments explicit rather than reactive.

### ESS disclosure and correction is the right scientific behavior
The correction from p100 to p98.76 — while substantively important — demonstrates that the red-team process is working as intended. Most research does not catch and correct this kind of tail-precision error before publication. The audit caught it, corrected it, and documented the correction. This is exemplary scientific behavior.

### The distinction between structural and vote-dependent findings is correctly maintained throughout
The paper consistently separates vote-independent structural findings (which are strong) from vote-dependent partisan-bias findings (which are consistent but sub-threshold). This distinction is the scientifically correct framing. A less rigorous analysis would collapse them.

### The pre-registration for the Lunty map is prospective and unimpeachable
The 17-test scoring grid for the November 2026 committee map was committed before the map exists. The 72-hour scoring window is specified. Numeric thresholds are fixed. This is exactly what pre-registration is for — it eliminates researcher degrees of freedom for the prospective audit entirely. If the committee map shows evidence of manipulation, the pre-registered finding will carry significantly higher evidential weight than anything in the retrospective audit.

### The dependency DAG is a genuinely novel contribution to open civic analysis
No Canadian electoral boundary audit (and few in other jurisdictions) has published a directed acyclic graph of analytical dependencies with explicit orphaning conditions. This makes the audit uniquely interrogable. Any critic can trace exactly how a finding would propagate downstream if their objection is valid.

---

## GREEN HAT — Scientific Improvements and Alternative Approaches

### Apply Bonferroni correction or report Benjamini-Hochberg FDR
The most straightforward fix for the family-wise error rate problem is to apply correction and report both corrected and uncorrected p-values, noting which findings survive correction and which do not. Benjamin-Hochberg false discovery rate control is a less conservative alternative to Bonferroni that would preserve more findings while still controlling error. This is a single analytical pass.

### Run the analysis on all 77 338Canada polling snapshots
The historical series already exists. Running EG and MM calculations across all 77 snapshots would produce a distribution of EG asymmetry values across plausible vote environments. If the asymmetry is consistently directional across most snapshots, the vote-distribution-dependence concern is substantially reduced. If it reverses in many snapshots, the finding is fragile and should be relabeled accordingly.

### Implement the 2019-seeded MCMC ensemble (Issue #13)
The current MCMC ensemble uses a random-draw null. The 2019-seeded ensemble would use the enacted map as the seed, producing a reference distribution centered on what was actually implemented previously. This is arguably a more legally relevant null hypothesis — it asks "how far does this proposal deviate from what Alberta voters have already lived under?" rather than "how does this compare to an arbitrary random map?"

### Attempt to recruit one independent academic replication
Even a single academic re-run of the core MCMC ensemble — not the full pipeline, just the vote-attribution-to-ensemble-comparison chain — would substantially strengthen the audit's scientific credibility. A single email to a Canadian political science or statistics department with the GitHub link asking for independent verification would be the right move before the November 2026 deadline.

### Write the methods paper for the DPG framework before November 2026
The eight-stage geometry pipeline is an original methodological contribution that has broad applicability beyond Alberta. Writing it as a standalone paper — "Constructing Electoral Geometries from Non-Shapefile Sources: A Staged Provisional Approach" — would allow it to be cited independently of the partisan-bias findings. A methods paper with no partisan stakes is easier to get into peer review quickly.

### Separate the D2 public submission analysis from the main audit
The public submission analysis currently appears as one section of a large audit. Expanded and published separately, it could be a standalone contribution to the literature on public engagement in redistricting processes. The 1,252 machine-parseable submissions represent a substantial dataset with research value beyond the Alberta case.

### Explicitly model the uniform-swing violation in B4
Rather than noting the uniform-swing assumption is violated and leaving it, the analysis could model a non-uniform swing — applying different regional swing rates to urban, suburban, and rural ridings based on historical Alberta variability. This would yield a Seats@50/50 estimate that doesn't depend on the violated assumption. The finding might not change, but the scientific defensibility would improve significantly.

---

## BLUE HAT — Scientific Process Assessment

### What this pass has established about the methodology

The White Hat found a technically sophisticated, well-documented methodology with genuine innovations (DPG pipeline, dependency DAG, falsifiability gates) and significant disclosed limitations (FWER, E2 reformulation, ESS, MCMC assumptions).

The Red Hat surfaced appropriate discomfort with the corrected CRITICAL errors — p100 → p98.76 and the P/C/E specification timing — while affirming that the correction process is itself evidence of scientific honesty.

The Black Hat identified eight specific methodological vulnerabilities, of which three are most significant: the family-wise error rate, the E2 reformulation as optional-stopping risk, and the 338Canada direction reversal. These set firm limits on what the partisan-bias findings can claim.

The Yellow Hat established that the structural findings are methodologically clean and the pre-registration for the Lunty map is the project's most scientifically credible contribution.

The Green Hat proposed seven specific methodological improvements, prioritized by feasibility before November 2026.

### The scientific defensibility assessment

**High confidence:** All structural findings (A1, A2, A3, C). These use publicly available data, require no vote attribution, and have been cross-validated against commission's own methodology.

**Moderate confidence:** Partisan-bias directional findings (EG and MM direction, MCMC percentile rank). These are consistent across methods and election cycles but sub-threshold and reversed under one polling substrate.

**Low confidence as formally pre-registered findings:** P/C/E signatures. These are exploratory findings correctly labeled as retrospective but carrying only exploratory evidential weight.

**Not established:** Intentionality of any map departure from neutrality. The audit correctly does not claim this.

### Scientific priority list for November 2026 deadline

1. Bonferroni/BH correction applied and reported (1–2 days work)
2. 338Canada 77-snapshot sensitivity (automated once pipeline is built, ~3–5 days)
3. 2019-seeded MCMC ensemble (1–2 weeks)
4. Recruit one independent academic re-run (outreach, unpredictable timeline)
5. Methods paper draft (ongoing, submit before November)

---

*End of Pass 2*
