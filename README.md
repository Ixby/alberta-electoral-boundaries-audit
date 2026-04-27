# Alberta Electoral Boundary Commission 2025–26 — Forensic Audit

*Two recommendations, one commission: measuring the structural distance between them.*

---

The 2025–26 Alberta Electoral Boundary Commission produced two competing recommendations — a majority and a minority — both legally compliant with the *Electoral Boundaries Commission Act*. The Act does not resolve between them. This audit measures the structural distance between the two maps on dimensions that have nothing to do with which party benefits.

**Airdrie.** The City of Airdrie has a population of approximately 84,000 residents — above the statutory ceiling for a single electoral division under the Act's ±25% population band. The majority recommendation splits it across two electoral divisions. The minority recommendation splits it across four, placing each quarter of the city into a division anchored in a different surrounding region. Both maps satisfy the law. Neither is required to use four instead of two. That is a drawing choice.

**Municipal boundaries.** When an electoral boundary follows an existing city or town limit, it produces a line that voters already know — from their school division, their property tax notice, their local ballot. The majority recommendation follows municipal edges on 71% of its total perimeter. The minority recommendation follows them on 14.5%. This 4.9× gap appears on a measure with no vote data in it: it is calculated from polygon geometry against Statistics Canada's 2021 Census sub-division boundaries.

**Population concentration.** In northwest Calgary, the minority map's electoral zone has a mean population 11.5% above the provincial average — above the threshold derived from the Act's own ±25% band. The majority's equivalent zone sits 2.8% above average, inside the threshold. The difference is 8.7 percentage points on a metric whose threshold is anchored to the statute, not to any academic benchmark.

These are three of five structural dimensions where the audit finds the minority recommendation diverges from the majority in consistent and measurable directions. In none of the three cases is the divergence legally prohibited. In none of the three cases does the measure depend on partisan vote data. And in none of the three cases is the divergence explained by Alberta's geography: the same provincial constraint set produces it on both maps, and a 100,000-plan MCMC ensemble confirms that the minority's values sit further from the constraint-bound expectation than the majority's.

This audit was produced as a personal research project by Will Conner, a Mount Royal University student, following the April 16, 2026 government decision to refer the commission's work to a Special Select Committee of MLAs. It is not affiliated with any political party, campaign, or advocacy organization. All code, data, and methodology are published here in reproducible form. The audit applies identical methodology to both maps.

> **New here? Start with the public report — [PDF](report_public.pdf) · [Web](report_public.md)** — a plain-language summary covering the five findings, the gerrymander checklist, and what you can do. The full technical monograph is [`report_academic.md`](report_academic.md).

---

## Quickstart

To reproduce the core findings or run your own analysis, you can get the environment running in three steps. (Requires Python 3.11+).

```bash
# 1. Clone the repository
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit

# 2. Run the idempotent setup script to install all dependencies
./setup.sh

# 3. Verify the installation by running the baseline packing/cracking script
python3 analysis/scripts/v0_2_packing_cracking_analysis.py
```
For detailed instructions on recreating the derived shapefiles or running the MCMC ensemble, see [`REPRODUCING.md`](REPRODUCING.md).

---

## What the audit finds

**Population equality (A1).** Mean absolute deviation from provincial quota: 3,180 persons (majority) vs 4,707 persons (minority). Both maps are legally compliant; the minority's higher variance is a property of drawing choices, not demographic geography.

**Geographic-zone asymmetry (A2).** The minority map's northwest Calgary zone sits 11.5% above the provincial mean population, exceeding the packing threshold (≥ +5% of provincial mean) anchored to the Act. The majority's equivalent zone sits 2.8% above average, inside the threshold. The threshold is derived from EBCA § 14, not from any partisan estimate.

**Community fragmentation (§5.3.2).** The minority recommendation partitions Airdrie into four separate electoral divisions. The majority uses two. Both satisfy the Act's population band. The minority's choice requires voters in the same city to be represented across four separate legislative constituencies, each primarily identified with a different surrounding community.

**Boundary anchoring (§5.8.5).** The majority recommendation anchors 71.0% of its perimeter to existing municipal edges; adding Statistics Canada dissemination-area boundaries brings the combined figure to 79.6%. The minority anchors 14.5% (municipal) and 16.5% (municipal + DA). The gap is 4.9× on the municipal measure, 4.8× combined.

**Cartographic anomalies (§5.8.2).** Three boundaries were flagged by name in the majority report's own response text. All three appear under the minority recommendation: a lasso-shaped corridor district (Nolan Hill–Cochrane), a boundary extension through uninhabited Banff National Park (Rocky Mountain House–Banff Park), and a district named for three towns whose population is smaller than the fourth community the district captures. Zero chair-flagged anomalies appear under the majority.

**Partisan-bias metrics (§5.2).** Efficiency gap, mean-median difference, and declination are measured across seven methodological layers and disagree on direction depending on the spatial-attribution method. The crosswalk-blended layer shows the minority 1.42 percentage points more UCP-favourable than the majority; the spatial-attribution layers show the minority 3–4 pp more NDP-favourable. Both directions are below the 7% efficiency-gap threshold proposed in the academic literature — a threshold that has never been adopted as a judicial standard in any Canadian or US court. The audit reports all seven layers and treats the method-disagreement itself as a finding.

**One pre-registered pass (§5.3.5).** The neighbour-drain adjacency test — which asks whether packed and cracked districts of the same party sit next to each other — finds zero coupled chain signals under the minority map, compared to three under both the majority and the 2019 enacted map. This is a pre-registered pass of the minority on that specific test. It appears in the paper as a result.

The audit does not claim the minority map is a gerrymander in the intent sense. It claims measurable structural divergence from the majority, at magnitudes that are unlikely to be explained by the ±25% population + contiguity + compactness constraint set alone.

---

## Forward-looking recommendations

Two policy recommendations attach to the audit findings.

**Act §12 amendment.** Section 12 of the *Electoral Boundaries Commission Act* permits referral of commission recommendations to a legislative committee with no statutory minimum notice or public-comment period. The audit proposes amending §12 to require: a 90-day minimum public-comment period before any referral, paired population tables showing both the statutory 2021-census baseline and an advisory Treasury Board quarterly-estimate sensitivity analysis, and a written explanation for any substantive deviation from commission recommendations. The proposal is in `analysis/reports/v0_1_act_amendment_proposal.md`.

**AI-use discipline for the Lunty committee.** The Special Select Committee chaired by Brandon Lunty, MLA for Leduc-Beaumont, is due to report by November 2, 2026. If the committee uses AI tools in its work, the audit proposes seven disciplines: humans decide (not algorithms), every prompt is logged and published, evaluation criteria are registered before drafting begins, at least two independent tools are run in parallel, every boundary has a named human of record, every factual claim in AI-drafted text is human-verified, and the committee publishes a 9-item public disclosure checklist alongside the final map. The proposal is in `analysis/reports/v0_1_ai_use_recommendations_for_committee.md` and summarised at §5.10 of the monograph.

---

## The structural cost

Both maps satisfy the law. The table below states the structural distance between them on six geometry-and-population measures and two vote-dependent measures, in the same units, applied identically to both.

| Dimension | Majority 2026 | Minority 2026 | Gap |
|---|---|---|---|
| Population MAD (persons) | 3,180 | 4,707 | Minority 48% higher variance |
| Calgary NW zone population excess | +2.8% above mean | +11.5% above mean | Minority 4.1× the threshold value |
| Airdrie partition count | 2 EDs | 4 EDs | Minority 2× more fragments |
| Municipal-boundary anchoring | 71.0% of perimeter | 14.5% of perimeter | 4.9× majority advantage |
| CSD + DA combined anchoring | 79.6% | 16.5% | 4.8× majority advantage |
| Chair-flagged cartographic anomalies | 0 | 3 | — |
| Efficiency gap (crosswalk method) | −1.29% | −2.71% | Both below 7% reference; direction method-sensitive |
| Coupled packing-cracking adjacencies | 3 (matches 2019 baseline) | 0 (pre-registered pass) | Minority eliminates the signature |

The first six rows are vote-independent. They are measurable against public official records and do not change if the partisan substrate changes. The last two rows depend on vote data; the seventh row's direction is not robust to the choice of spatial-attribution method; the eighth row is a finding in favour of the minority map.

A map with 4.9× lower municipal-boundary anchoring produces electoral divisions that are harder for voters to connect to their lived experience of municipal geography. A map that splits a city of 84,000 into four divisions — each identified with a different surrounding community — imposes a navigational cost on residents of that city that a two-division split does not. Neither cost is measured in dollars; both are structural costs to effective representation as the *Saskatchewan Reference* [1991] articulates it.

The status quo cost — of not auditing — is the alternative: accepting or rejecting either recommendation on the basis of commentary and intuition rather than measurement.

---

## What makes this different

**The predictions came before the results.** Every test family in the audit was committed with a directional null hypothesis and a pre-specified pass threshold before the results were read. The commit timestamp separating the pre-registration from the first detection run is 2 hours and 24 minutes. A methodology that only finds what it was looking for, after it looked, is not a methodology — it is a post-hoc justification. Pre-registration prevents that.

**Each finding has a named retraction condition.** For every load-bearing finding, the audit documents what data or argument would force a retraction within 48 hours of it becoming available. The conditions are in `analysis/methodology/v0_1_retraction_pathway.md`. A reviewer who objects to a specific finding does not need to argue in the abstract — they can find that finding's retraction condition and produce the triggering evidence.

**The pre-registered passes are reported as prominently as the findings.** The neighbour-drain test result — zero coupled adjacencies under the minority, where three exist under both the majority and 2019 — is reported as a §5.3.5 PASS, not buried in a supplementary table. An audit that hides its non-findings is not an audit.

**The same tests run on both maps.** Every metric applied to the minority recommendation is applied identically to the majority and to the 2019 enacted map. There is no test in this audit that runs only on the minority. This is the discipline the paper calls test-application symmetry.

**The apparatus has a dependency graph.** 234 analytical nodes across 454 directed edges — acyclic, zero orphan findings. Any dataset can be invalidated and the cascade of orphaned findings is computable in real time: `python analysis/scripts/dependency_query.py --invalidate L0:data.2023_statement_of_vote`. Invalidating the entire 2023 vote dataset orphans 48 of 74 findings — but leaves 26 that span population, geography, procedural, and geometry-only dimensions. The audit's headline does not collapse if the partisan-vote data is challenged.

---

## Open questions

This audit is not finished. The following are genuinely unresolved.

**Official geometry (Issue #1).** The commission published its 2026 maps as 300-DPI rasters only; no vector shapefiles have been released. The audit's partisan-bias direction in §5.2.7 is sensitive to which reconstructed geometry substrate is used, and the two substrates currently disagree on direction. Elections Alberta was contacted on April 23, 2026 with a request for the official shapefiles. An FOIP request would accelerate this. Until official shapefiles are available, §5.2.7's direction claim remains method-sensitive and is reported in both directions.

**The counter-map challenge (Issue #14).** The §5.8.5 anchoring finding has a retraction condition: produce a map that achieves the minority's stated community-of-interest objectives with majority-comparable municipal-boundary anchoring. Producing that map requires the commission's drawing tools and the official 2026 shapefiles. No counter-map has been produced. If one is, §5.8.5 retracts.

**The 2019-seeded MCMC ensemble (Issue #13).** The constraint-bound ensemble in §5.4 starts from a random seed, not from the 2019 enacted map. A chain seeded at the 2019 enacted geometry would more directly model incremental commission drawing and might place both 2026 recommendations differently within the ensemble distribution.

**Alberta's historical efficiency-gap baseline (Issue #16).** The 7% EG reference threshold is calibrated to US Congressional elections. An Alberta-specific threshold requires computing EG for the 2015, 2019, and 2023 elections under prior-cycle boundaries — work not yet done. The provisional range is 5–9%; see §5.2.8 Option C.

---

## What to do with this

**Challenge the audit.** Read `analysis/methodology/v0_1_retraction_pathway.md`. Find a specific finding and its named retraction condition. Produce the data or argument that triggers it. The retraction conditions are public, concrete, and dated.

**Ask the Lunty committee about its process.** The Special Select Committee is due to report by November 2, 2026. Specific questions worth asking: What evaluation criteria were established before the committee began drawing? Will prompts and inputs to any AI tools used in the process be published? Will an ensemble of alternative maps be generated and published alongside the final map?

**Request the official shapefiles.** File a Freedom of Information and Protection of Privacy Act request with Elections Alberta for the official 2026 electoral division shapefiles. This is the single piece of external data that would resolve the §5.2.7 method-sensitivity disagreement and allow the audit's sunset-clause reruns.

**Share the public-audience report.** [`report_public.md`](report_public.md) is written for a general audience. It covers the five findings, the gerrymander checklist, and what the April 16 pivot means — without requiring any background in electoral systems or statistics.

The audit is a measurement, not an advocacy document. It does not argue for either recommendation to be adopted. The Lunty committee has the authority to produce a new map entirely; the audit's job is to document what the commission's two proposals look like under systematic measurement.

---

## Feedback and engagement

This is a working document that gets better with engagement.

**Issues** — use the [Issues tab](../../issues) for specific methodological objections, data corrections, or retraction-condition triggers. Include the finding number (e.g., A1, §5.8.5) and the specific claim at issue.

**Discussions** — use the [Discussions tab](../../discussions) for broader design questions: Is the constraint-bound ensemble the right comparator? Should the municipal-anchoring metric weight urban and rural EDs differently? Is a 7% EG reference appropriate for a Canadian provincial legislature at all?

**Pull requests** — corrections to data files, script bugs, and documentation errors are welcome. PRs proposing new findings or tests should include a pre-registration artifact (null hypothesis, threshold, prediction direction) in the PR description.

The audit is most usefully challenged by people with expertise in electoral geography, Canadian constitutional law, redistricting statistics, and GIS. Engagement from supporters of either recommendation is welcome; the retraction conditions exist to give hostile reviewers a structured path that doesn't require arguing about intent.

---

## Deeper reading

- **[report_public.md](report_public.md)** — **Start here.** Plain-language summary for a general audience: the five findings, the gerrymander checklist, what the April 16 pivot means, and what you can do. No prior knowledge required.
- **[report_academic.md](report_academic.md)** — The full monograph (v0.19, 2026-04-24): executive summary, methods, §§5.1–5.10 results, seven measurement layers, dependency DAG, limitations, and falsifiability hooks. Start here to challenge a specific finding.
- **[analysis/methodology/v0_1_retraction_pathway.md](analysis/methodology/v0_1_retraction_pathway.md)** — Named retraction conditions per finding. The fastest path to either retracting a claim or confirming it holds.
- **[analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md](analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md)** — Pre-committed null hypotheses, pass thresholds, and Structural/Robust/Durable classification for every finding.
- **[analysis/methodology/v0_1_test_apparatus_defense.md](analysis/methodology/v0_1_test_apparatus_defense.md)** — Per-test criticism and response. Answers "are you making up metrics to have metrics?"
- **[analysis/methodology/v0_1_threshold_provenance.md](analysis/methodology/v0_1_threshold_provenance.md)** — Every numeric threshold traced to a statutory source, a literature citation, or a first-principles derivation. 41 thresholds catalogued, including three Alberta-calibrated EG alternatives.
- **[analysis/methodology/audit_dependency_graph_readme.md](analysis/methodology/audit_dependency_graph_readme.md)** — The 234-node, 454-edge dependency graph: schema, worked examples, and the `--invalidate` query CLI.
- **[analysis/reports/v0_1_ai_use_recommendations_for_committee.md](analysis/reports/v0_1_ai_use_recommendations_for_committee.md)** — AI-use recommendations for the Lunty committee: seven principles, technical guidance by task type, and a 9-item public disclosure checklist.

---

## Licensing and reuse

Input data is public-record material: Elections Alberta's 2023 Statement of Vote, Statistics Canada's 2021 Census (Open Government Licence — Canada), and the Electoral Boundary Commission's 2026 final report and appendices. Derived code and analysis are released under the MIT License. The Derived Provisional Geometries (DPGs) are original work produced by reconstructing machine-readable polygons from the commission's raster-only published maps; they carry the §4.1.4 sunset clause and should not be cited as authoritative electoral geography without reference to that clause and its rerun commitment.
