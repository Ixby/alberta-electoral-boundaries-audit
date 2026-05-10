# Six Thinking Hats Analysis — Alberta Electoral Boundary Audit
## Pass 1: Project Integrity and Evidentiary Weight

*Framework: Edward de Bono's Six Thinking Hats. Each hat examines the Alberta Electoral Boundary Audit from a single disciplined perspective. Pass 1 focuses on what the project has established, where it holds, and where it strains.*

---

## WHITE HAT — Facts, Data, and Known Information

### What the project is
An independent forensic audit of Alberta's 2025–26 Electoral Boundaries Commission process, comparing two competing 89-seat maps (majority recommendation and minority recommendation) against the 2019 87-seat baseline. Author: Will Conner, 4th-year BCIS student at Mount Royal University. No political party affiliation declared.

### Timeline of events (verified)
- October 2025: Interim commission report — unanimous among all five commissioners
- March 23, 2026: Final report tabled — split 3–2 (chair + 2 opposition forming majority; 2 government commissioners forming minority)
- April 16, 2026: Government rejected majority report, established MLA Special Select Committee chaired by Brandon Lunty (government-controlled)
- April 2026: Audit released publicly on GitHub (Ixby/alberta-electoral-boundaries-audit)
- April 23, 2026: Will Conner sent outreach emails to Elections Alberta (shapefile request) and Duane Bratt (academic)
- May 6, 2026: Elections Alberta released official shapefiles, triggering pre-committed sunset clause recomputation
- November 2, 2026: Scheduled date for Lunty committee map release; re-audit pre-registered

### Data sources (all public record)
- Elections Alberta 2023 Statement of Vote: 1,973 polls, 87 ridings
- Electoral Boundaries Commission Final Report (March 23, 2026)
- Statistics Canada 2021 Census Dissemination Area populations and shapefiles
- Elections Alberta official 2026 shapefiles (received May 6, 2026)
- Alberta public submission archive: 1,252 of approximately 1,340 machine-parseable (93.4%)
- 338Canada riding-level projections: April 2026 snapshot; 77-snapshot historical series
- 2018 and 2019 Alberta electoral data for cross-election validation

### Statistical results (exact figures)

**Vote-independent structural findings:**

| Metric | Majority | Minority |
|--------|----------|----------|
| Mean Absolute Deviation (MAD) from provincial average (54,929) | 3,180 persons | 4,707 persons (+48%) |
| Ridings >+10% deviation | 5 | 15 |
| Ridings >+15% deviation | 0 | 5 |
| Maximum positive deviation | +14.28% | +24.06% |
| Calgary NE/central vs S/W zone gap | +0.36% | +12.20% |
| Airdrie municipal splits | 2 EDs | 4 EDs |
| Municipal boundary anchoring (perimeter %) | 71.0% | 14.5% |
| Municipal + DA boundary anchoring | 79.6% | 16.5% |
| Cartographic anomalies flagged by commission chair | 0 | 3 |

**Vote-dependent partisan bias findings (crosswalk-blended, w=0.85):**

| Metric | Majority | Minority | Asymmetry |
|--------|----------|----------|-----------|
| Efficiency Gap (EG) | −0.40% | −1.81% | −1.41 pp |
| Mean-Median Gap | 2.1% | 3.5% | — |
| Seats@50/50 (CI) | 43–46 | 41–47 | CIs overlap |
| Declination | −0.021 | −0.015 | Opposite direction to EG |
| MCMC minority EG p-rank (ESS-adjusted) | p92.66 | p98.76 | — |
| 338Canada April 2026 projection | — | +1 NDP seat | Direction reversal |

**Sensitivity range (EG asymmetry, urban weight w=0.60–0.90):** −0.51 pp to −1.52 pp

**Monte Carlo directional confidence (N=2,000, parameter jitter):** 90.5% of samples show minority more UCP-favorable than majority; 95% CI on asymmetry: [−3.04, +0.76] pp (crosses zero).

### Pre-registration record
- OSF registrations: w2s8k, r3zm7, qsgy8, 6pt83
- AsPredicted: #289449, #289451, #289455
- 17-test prospective scoring grid committed for November 2026 Lunty committee map
- 72-hour scoring window from map release

### Code audit findings (Gemini 3.1 Pro, April 26, 2026)
- 1 CRITICAL bug fixed: dict iteration order in `targeted_gerrymander_burst.py` (vote array misalignment)
- 1 HIGH bug fixed: missing deduplication in `fuzz_missing_eds.py` (slivers double-counting)
- 1 MEDIUM noted: PRNG per-chunk reseeding in MCMC script (low practical impact)
- 1 LOW noted: float boundary drift at 0.5 ties

### Red-team findings summary
- 4 CRITICAL science issues identified; all addressed (retracted, ESS-adjusted, or recomputed)
- 8 HIGH issues; documented, not blocking, disclosure in-paper
- 5 MEDIUM, 1 LOW

### What is not known
- Whether the Lunty committee map will show any of the same patterns
- Whether the 7% EG threshold (Stephanopoulos-McGhee 2014/2015) is an appropriate benchmark for Alberta (never judicially adopted in Canada)
- Actual partisan intent behind the minority commission positions
- How the approximately 88 image-only submissions (6.6%) would have changed public input tallies
- Whether the audit will receive academic peer review before the November 2026 committee map release

---

## RED HAT — Feelings, Intuitions, and Gut Reactions

### On the project's ambition
There is something genuinely impressive about a fourth-year undergraduate producing a 234-node dependency DAG with pre-registered falsifiability gates, a six-stage geometry pipeline, and a science red-team framework. The ambition here exceeds the institutional context. This feels like a project that outgrew its container.

### On the April 16 pivot
The gut reaction to a government rejecting an independent commission's majority recommendation and substituting a government-controlled MLA committee is alarm. It doesn't feel right, regardless of which party is doing it. The commission existed precisely to remove this kind of decision from political hands. The pivot feels like a democratic norm being tested in real time.

### On the minority map
Looking at the Airdrie 4-way split, the lasso-shaped corridor in Calgary-Nolan Hill-Cochrane, and the Rocky Mountain House-Banff Park extension through uninhabited national park, something feels engineered. Whether or not statistics confirm it, the visual anomalies alone produce a visceral reaction in any person familiar with basic geographic common sense. Boundaries don't need to do these things to serve communities.

### On the efficiency gap numbers
A 1.41 percentage point asymmetry feels simultaneously meaningful and modest. It's not nothing — it's a consistent directional signal across multiple methods. But it also doesn't feel like the smoking gun the public debate might expect. There's a tension between "this is statistically interesting" and "this will move people."

### On the author's situation
There is something lonely about one person, working without institutional support, building a system this complex while also completing a university degree. The project carries the weight of civic urgency — a commission report that may determine Alberta's electoral map for a decade — and the author is a student. That deserves acknowledgment.

### On the 338Canada reversal
The fact that the April 2026 polling substrate shows a +1 NDP seat advantage on the minority map — the opposite direction from every structural finding — produces genuine unease. It suggests the project is sitting at a methodological inflection point. The finding isn't wrong, but it should make anyone cautious about strong directional claims.

### On the red-team process
The willingness to commission a red-team that found CRITICAL flaws and then address them publicly rather than quietly burying them feels honest. This produces trust. It's rare.

---

## BLACK HAT — Caution, Risk, and Critical Thinking

### The efficiency gap threshold problem
The 7% EG threshold (Stephanopoulos-McGhee) has never been judicially adopted in Canada or the United States. Alberta's 2026 magnitudes (−1.4 pp to +0.4 pp) sit far below it. The audit documents this clearly, but anyone misreading the headline EG numbers as evidence of legal gerrymandering will be incorrect. The academic literature on what EG magnitude constitutes actionable gerrymandering is unsettled even in the US context, where courts have explicitly declined to adopt it.

### The 90.5% directional confidence is not 95%
The Monte Carlo confidence interval on the EG asymmetry crosses zero ([−3.04, +0.76] pp). This means at classical significance thresholds, the directional claim fails. The audit re-labels this a "sensitivity interval" rather than a confidence interval, which is methodologically honest — but the 90.5% figure will be interpreted by non-statisticians as near-certainty when it is not.

### The family-wise error rate problem (HIGH, unresolved)
21 statistical tests are conducted without Bonferroni or other family-wise error rate correction (per-test α at Bonferroni: 0.0024). This is disclosed in the paper but not corrected. Several individual test results that appear significant at conventional α=0.05 would not survive correction. The audit's conclusion that multiple dimensions show consistent direction partially compensates for this, but the unadjusted individual test statistics remain in the paper.

### The E2 reformulation is a documented optional-stopping risk
The engineered boundary criterion (E2) was reformulated mid-audit — from a "narrow eligibility" test to a "substantive choice-over-alternatives" test — after the initial narrow formulation failed to detect the Rocky Mountain House-Banff Park anomaly. The audit discloses this as an optional-stopping risk, but disclosure does not eliminate the problem. This is the most significant methodological weakness in the P/C/E framework.

### The P/C/E signatures are retrospective, not pre-registered
The criteria for the P/C/E signature framework were committed in the same analytical pass as the detection run. The audit describes them as "retrospectively-defined signatures" rather than pre-registered tests. This is the right labeling, but it means the three formal signatures cannot carry the evidentiary weight of a true pre-registration. Critics will note this.

### The MCMC effective sample size issue
The MCMC ensemble reported 10,000 runs but the effective sample size (ESS) due to autocorrelation is approximately 148–160. This means the tail percentiles are far less precise than the raw run count implies. The ESS adjustment was a CRITICAL red-team finding; it is now addressed in the text, but the underlying precision limitation remains.

### The declination metric contradicts EG direction
Declination (Warrington 2018) shows the minority map as *least* UCP-favorable of the three maps — the opposite direction from EG and Mean-Median. The audit documents this as a property of the metrics, not a suppressed finding, which is correct. But it complicates any simple directional narrative. Two of four partisan-bias metrics point one way; one points the other way; one (Seats@50/50) has overlapping CIs. The honest characterization is "directionally mixed with majority of metrics showing one pattern."

### Solo author, no institutional validation
The audit has not undergone peer review. The code audit was performed by an external AI (Gemini 3.1 Pro), not a human academic statistician. The geometry pipeline (eight stages) is complex enough that undetected bugs could affect results in ways not caught by the automated audit. The dependency DAG with 234 nodes and 454 edges is self-generated. The project's reproducibility claim rests on public code that has not been independently re-run by a third party as of writing.

### The 338Canada direction reversal is not explained
Under April 2026 polling projections, the minority map produces +1 NDP seat — the opposite of the structural efficiency gap findings. The audit notes this reversal but does not fully explain the mechanism. If partisan bias is a function of vote distribution rather than structural invariant (as the result implies), the magnitude of the structural EG finding is partially contingent on the 2023 election result being representative of future elections — a strong assumption given Alberta's historical vote volatility.

### Public input finding is partial
The audit recovered 14 submissions supporting at least one minority-contested configuration, partially refuting the chair's "no public support" claim. But "at least one contested configuration" is not "support for the full minority map." The recovery is meaningful but overstated if used to argue the minority map had broad public support.

---

## YELLOW HAT — Optimism, Value, and Benefits

### The vote-independent findings are genuinely strong
The structural findings — population variance (48% wider MAD), Calgary zone gap (12.2% vs 0.36%), Airdrie fragmentation (4 vs 2 splits), municipal boundary anchoring (14.5% vs 71%) — do not depend on vote attribution method, election baseline, urban weight parameter, or any other analytical choice. They are direct comparisons of the maps as drawn against each other and against publicly stated commission methodology. These findings are the project's strongest contribution and survive all stress tests.

### The pre-registration for the Lunty map is valuable regardless of what the map shows
Whether the November 2026 committee map shows evidence of manipulation or not, a pre-registered 17-test audit conducted within 72 hours of map release is a civic contribution. If the map is clean, the audit will demonstrate that. If it is not, the finding will have pre-registered credibility. Either outcome serves the public interest.

### The dependency DAG is a methodological innovation
Publishing a 234-node, 454-edge directed acyclic graph of analytical dependencies — showing exactly which findings orphan if any dataset is invalidated — is an unusually rigorous approach for any audit, let alone an independent one. It gives critics a precise map of where to attack and readers a precise map of how findings connect. This is a genuine contribution to transparent civic analysis.

### The retraction pathways are intellectually honest
Every major finding has a named retraction condition. This is rare in public-interest research. It communicates that the author's commitment is to accuracy rather than to a predetermined conclusion, and it gives future analysts a clear roadmap for updating the record.

### The public report and academic report are correctly separated
Producing both a plain-language public report and a technical academic monograph shows awareness that these audiences require different documents. The public report states findings without requiring readers to understand MCMC or DPG pipelines. The academic report is fully specified for replication.

### The April 16 procedural finding is the most legally and politically durable
Regardless of EG magnitudes, the observation that the government substituted a government-controlled MLA committee for an independent commission recommendation — for the first time in recent Canadian history (compared to BC 2008, Quebec 1992, Ontario 1996) — is a factual, durable, politically significant finding that requires no statistical interpretation. It stands on its own.

### The Enoch Cree Nation bundling observation matters
The observation that the minority map pairs Enoch Cree Nation with distant Devon rather than adjacent Edmonton, while the majority map pairs it with adjacent Edmonton, is a meaningful community-of-interest finding with Indigenous rights implications. This dimension is underdeveloped in the current report and deserves expansion.

### The Act amendment proposal is constructive
The proposal in `act_amendment_proposal.md` — requiring 90-day minimum public-comment periods before referral, paired population tables, and written explanation for substantive deviations from commission recommendations — translates the audit findings into specific, achievable legislative fixes. It demonstrates that the project is aimed at improving the process, not just documenting a problem.

### Open-source reproducibility is a genuine strength
All code, data, and methodology are public. Any researcher, journalist, or rival partisan can verify or attack the findings using the same tools. This is the appropriate standard for civic research and it distinguishes the audit from internal party analyses.

---

## GREEN HAT — Creativity, Alternatives, and New Possibilities

### The counter-map challenge (Issue #14) is unfinished and valuable
The audit commits to producing an alternative map achieving the minority's stated objectives with majority-level municipal anchoring. This is the most powerful possible response to "the minority map was necessary to achieve certain objectives." If a counter-map can be produced showing it was not necessary, the unavoidability defense collapses. This should be the highest-priority open item.

### The 2019-seeded MCMC ensemble (Issue #13) could shift the baseline conversation
Running the MCMC ensemble seeded from the 2019 enacted map would allow comparison of how far the 2026 proposals deviate from the historically-enacted baseline, rather than from an arbitrary random-draw ensemble. This would be a more legally grounded null hypothesis than "any redistricting plan."

### The methods paper could become the primary academic contribution
The DPG framework documentation (`methods_paper_draft.md`) may ultimately be the most academically original contribution of this project — the eight-stage pipeline for constructing provisional electoral geometries from mismatched census and electoral data is a solved problem that has wide applicability beyond Alberta. Publishing this as a standalone methods paper would reach a different audience than the audit itself.

### The public submissions analysis could be deeper
Of 1,252 machine-parseable submissions, only a keyword extraction and frequency analysis was conducted for D2. A full topic-model or sentiment analysis of the submissions, combined with geographic clustering (which submissions came from which ridings, and what did those riders think about their proposed new boundaries), could yield a much richer picture of public input alignment.

### The 338Canada series could be used for retrospective sensitivity
The 77-snapshot historical 338Canada series is noted but not fully exploited. Running the EG calculation against each historical polling snapshot would show whether the EG asymmetry has been stable across different hypothetical election environments or whether it depends on the specific polling moment of April 2026. This would directly address the vote-distribution-dependence concern.

### The Indigenous dimension deserves dedicated analysis
The Enoch Cree Nation finding, the s.15(2) remote-district provisions, and potential other First Nations communities affected by boundary changes deserve a dedicated analytical section. Engaging an Indigenous legal or political scholar as co-reviewer would strengthen this dimension significantly.

### An automated boundary monitoring tool could be the project's legacy
The DPG pipeline and the pre-registration grid, once proven on the Alberta case, could form the basis of a generalized electoral boundary monitoring toolkit applicable to any Canadian province's redistricting cycle. The next provincial redistricting in any province could be audited using the same framework in a fraction of the time it took to develop it for Alberta.

### The Lunty committee map could be pre-analyzed
Before the committee map is released, the pre-registration criteria are fixed. But the model inputs — the 2023 vote substrate, the census geometry, the DPG pipeline — are already built. The instant the map is released as a shapefile, the entire analytical chain can run in automated sequence. Pre-building the analysis pipeline to run on input is the right approach.

---

## BLUE HAT — Process Control and Meta-Thinking

### What the six hats have surfaced in this pass

The White Hat established that the project has produced real, reproducible, publicly documented findings on both structural and partisan-bias dimensions. The data is all public record. The analysis chain is available for independent replication.

The Red Hat surfaced appropriate emotional investment in the civic stakes — the April 16 pivot is genuinely alarming as a democratic norm question — while also flagging the discomfort produced by the 338Canada direction reversal. The emotional read is: "this matters, but be careful."

The Black Hat identified the primary vulnerabilities: the family-wise error rate problem, the E2 optional-stopping risk, the ESS limitation, the declination metric direction disagreement, and the absence of institutional peer review. None of these individually collapses the project, but they set limits on how strong the partisan-bias claims can responsibly be stated.

The Yellow Hat established that the vote-independent structural findings are the strongest part of the project and the April 16 procedural finding is the most durable. The pre-registration for the Lunty map is the project's most forward-looking contribution.

The Green Hat identified the counter-map challenge as the highest-priority unfinished item and pointed toward the methods paper as a potentially more academically significant output than the audit itself.

### What the project has and has not established

**Has established:** Measurable, reproducible structural differences between the two maps across five vote-independent dimensions. Consistent directional pattern in partisan-bias metrics (with documented exceptions). A pre-registered audit framework ready for the November 2026 committee map.

**Has not established:** Intentional partisan manipulation. Statistical significance at classical thresholds on the directional partisan-bias claim. A finding that would compel judicial relief under any Canadian legal standard.

### Process recommendations

1. Priority 1: Complete the counter-map challenge (Issue #14). This is the most powerful single piece of evidence available.
2. Priority 2: Propagate the family-wise error rate disclosure to every section containing unadjusted individual test statistics.
3. Priority 3: Expand the Enoch Cree Nation and Indigenous dimension analysis.
4. Priority 4: Run the 338Canada 77-snapshot sensitivity to quantify vote-distribution dependence.
5. Priority 5: Seek a single independent academic re-run of the core MCMC ensemble before November 2026.

### The right claim level for public communication

The project's findings support this claim: *"The minority map departs from the majority map on five structural dimensions independent of vote data, and shows a consistent directional pattern on partisan-bias metrics that are at sub-threshold magnitude but consistent across analytical methods and election cycles. The April 16 government decision to replace the independent commission with a government-controlled committee is without recent Canadian precedent."*

The project's findings do not support: *"The minority map is gerrymandered."* The audit correctly does not make this claim.

---

*End of Pass 1*
