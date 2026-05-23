> **Backward:**
> - `reports/academic/report_academic.md` — full monograph from which headline findings are summarised
> - `reports/public/report_public.md` — plain-language report cross-referenced in the deeper-reading list
> - `docs/FINDINGS_BRIEF.md` — one-page brief linked as the fastest entry point
> - `findings/population_equality.md` — source of population MAD A1 numbers
> - `findings/partisan_bias_summary.md` — source of partisan-metric headline values (+3.92 pp EG, +4.66 pp mean-median, +5.62 pp seats@50/50)
> - `findings/intermap_permutation_test_results.md` — source of the Ch1-COMP inter-map test results
> - `findings/joint_outlier_score_summary.md` — Mahalanobis joint outlier (Ch1) numbers
> - `findings/airdrie_overlap_report.md` — Airdrie four-way split documentation
> - `analysis/methodology/retraction_pathway.md` — named retraction conditions referenced throughout
> - `analysis/methodology/null_hypothesis_and_exoneration_criteria.md` — pre-committed pass thresholds
> - `analysis/methodology/threshold_provenance.md` — threshold derivations cited (EG, anchoring)
> - `analysis/methodology/audit_dependency_graph_readme.md` — 234-node DAG referenced in "apparatus" section
> - `docs/act_amendment_proposal.md` — §12 amendment policy recommendation
> - `docs/ai_use_recommendations_for_committee.md` — AI-use disciplines for Lunty committee
>
> **Forward:**
> - (leaf — repository landing page; reviewer-facing and external-citation surface)

# Alberta Electoral Boundary Commission 2025–26 — Forensic Audit

*Two recommendations, one commission: measuring the structural distance between them.*

## Public Summary

**https://ixby.github.io/alberta-electoral-boundaries-audit/**

---

## Reading guide

The audit's **live claims and current methodology** are in this README and in `findings/`, `reports/`, `analysis/methodology/`, and `preregistration/`. Everything in those directories is current as of the canonical Elections Alberta shapefile recomputation (2026-05-12); numbers in any individual file should be cross-checkable against the on-disk data referenced in that file's `Backward:` block.

Two top-level directories are **not** part of the live audit:

- `archive/` holds retracted or superseded analyses, kept intact for trail-of-work transparency. The DPG-era anchoring findings (majority 71.0% / minority 14.5% / 4.9× asymmetry) live there along with the pre-canonical sampler-disagreement framing. **Skip unless** you are auditing the retraction history or following the methods-paper case study (see `archive/dpg_era/README.md`).
- `proposals/` holds speculative future work that has not been authorized, has not been pre-registered in non-draft form, and has not been run. **Skip unless** you want to know what work might be done next (see `proposals/README.md`).

Every script and document in the repository declares its upstream and downstream dependencies in its own header (`Backward:` / `Forward:` block); the convention is documented in `DEPENDENCY_CONVENTION.md`. There is no central dependency map — to walk the chain in either direction from any file, grep that file's header.

---

The 2025–26 Alberta Electoral Boundary Commission produced two competing recommendations — a majority and a minority — both legally compliant with the *Electoral Boundaries Commission Act*. The Act does not resolve between them. This audit measures the structural distance between the two maps on dimensions that have nothing to do with which party benefits.

**Airdrie.** The City of Airdrie has a population of approximately 85,805 residents (City of Airdrie 2024 municipal census, July 2, 2024) — above the statutory ceiling for a single electoral division under the Act's ±25% population band. The majority recommendation splits it across two electoral divisions. The minority recommendation splits it across four, placing each quarter of the city into a division anchored in a different surrounding region. Both maps satisfy the law. Neither is required to use four instead of two. That is a drawing choice.

**Chair-flagged boundaries.** When the commission chair singles out a specific boundary by name in the official hearing record, that is a primary-source signal requiring no vote data to interpret. The majority report's written responses flag three minority boundaries as warranting explanation: a lasso-shaped corridor linking Nolan Hill to Cochrane, an extension through uninhabited Banff National Park, and a district whose name references three smaller towns while its largest population centre goes unnamed. Zero boundaries in the majority recommendation attracted equivalent chair-level commentary.

**Population concentration.** In northwest Calgary, the minority map's electoral zone has a mean population 11.5% above the provincial average — above the threshold derived from the Act's own ±25% band. The majority's equivalent zone sits 2.8% above average, inside the threshold. The difference is 8.7 percentage points on a metric whose threshold is anchored to the statute, not to any academic benchmark.

These are three of four surviving structural dimensions where the audit finds the minority recommendation diverges from the majority in consistent and measurable directions. In none of the three cases is the divergence legally prohibited. In none of the three cases does the measure depend on partisan vote data. And in none of the three cases is the divergence explained by Alberta's geography: the same provincial constraint set produces it on both maps, and a 1 million-plan MCMC ensemble confirms that the minority's values sit further from the constraint-bound expectation than the majority's.

This audit was produced as a personal research project by Will Conner, a Mount Royal University student, following the April 16, 2026 government decision to refer the commission's work to a Special Select Committee of MLAs. It is not affiliated with any political party, campaign, or advocacy organization. All code, data, and methodology are published here in reproducible form. The audit applies identical methodology to both maps.

> **New here?** The fastest entry points:
> - **[One-page brief](docs/FINDINGS_BRIEF.md)** — seat counts, wasted votes, plain English, no background needed. Print-ready PDF version: [`docs/FINDINGS_BRIEF.html`](docs/FINDINGS_BRIEF.html) (open in Chrome → File → Print → Save as PDF).
> - **[Web summary](https://ixby.github.io/alberta-electoral-boundaries-audit/)** — same findings with the key chart, designed for sharing.
> - **[Public report](reports/public/report_public.md)** — longer plain-language narrative with maps and figures.
> - **[Technical monograph](reports/academic/report_academic.md)** — full methods, citations, and pre-registration IDs.

---

## Cover map

The cover art (`data/maps/cover_art.png`, regenerated by `python analysis/scripts/build_cover.py`) shows Alberta's 4,765 Voting Areas coloured by 2023 UCP–NDP two-party election-day vote share — orange for NDP-leaning, blue for UCP-leaning — with colour intensity modulated by log-scale population density. Sparse rural Voting Areas appear near-ivory; dense urban areas are fully saturated, darkening further in the Calgary and Edmonton cores. The minority commission's 89-district proposal is overlaid as thin boundary lines.

The result shows Alberta weighted by where people live rather than by land area. Standard election maps fill each riding with the winning party's colour, producing a picture dominated by large rural ridings. The VA-level density-modulated render makes population visible: colour saturates only where people are concentrated, revealing an urban-heavy population distribution that looks nothing like the typical election-night map of the province.

---

## Repository Architecture

This repository is structured to enforce a strict separation of concerns for independent auditors. **Live tier** (the audit's current claims):

* **`findings/`** — Per-test analyses; one file per substantive finding. Each declares its `Backward:` / `Forward:` dependencies in its own header.
* **`reports/`** — `reports/academic/report_academic.md` is the full technical monograph; `reports/public/report_public.md` is the plain-language report.
* **`analysis/`** — Execution code (`scripts/`), live methodology rationale (`methodology/`), and review records (`review/`). Diagnostic logs live in `data/logs/`.
* **`data/`** — Unaltered source material, immutable standards (`reference/`), geospatial boundaries (`shapefiles/`), and all computed metrics and MCMC simulation distributions (`outputs/`). Code never lives here. The `data/maps/` subdirectory holds cover art and generated visual plots.
* **`preregistration/`** — Pre-committed null hypotheses, drand-beacon seed commitments, retraction conditions, and amendment log.
* **`docs/`** — Reproducer instructions (`docs/REPRODUCING.md`), one-page brief (`docs/FINDINGS_BRIEF.md`), policy proposals, and rendered HTML for GitHub Pages.
* **`notebooks/`** — Colab-ready exploratory notebook (`notebooks/alberta_audit_explorer.ipynb`).
* **`tests/`** — The Pytest suite enforcing byte-for-byte integrity and mathematical proofs.
* **`viewer/`** — Svelte source for the public web summary (built and deployed via `docs/`).

**Out-of-band tiers** (clearly labelled, see the Reading guide above):

* **`archive/`** — Retracted or superseded analyses, kept intact for trail-of-work transparency. Each subdirectory has its own README explaining what's there and why.
* **`proposals/`** — Speculative future work not yet authorized or run. Each proposal has its own README documenting the plan and the authorization gate.

---

## Quickstart

To reproduce the core findings or run your own analysis, you can get the environment running in three steps. (Requires Python 3.11+).

```bash
# 1. Clone the repository
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit

# 1b. Pull Git LFS files (MCMC checkpoints, ~1 GB — required for ensemble re-runs)
git lfs install && git lfs pull

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify the installation by running the baseline packing/cracking script
python3 analysis/scripts/packing_cracking_analysis.py
```
For detailed instructions on recreating the derived shapefiles or running the MCMC ensemble, see [`docs/REPRODUCING.md`](docs/REPRODUCING.md).

---

## What the audit finds

**Population equality (A1).** Mean absolute deviation from provincial quota: 3,180 persons (majority) vs 4,707 persons (minority) (provincial mean: 54,929; source: `findings/population_equality.md`). Both maps are legally compliant; the minority's higher variance is a property of drawing choices, not demographic geography.

**Geographic-zone asymmetry (A2).** The minority map's northeast/central Calgary zone sits 11.5% above the provincial mean population (zone mean: 61,225; provincial mean: 54,929), exceeding the packing threshold (≥ +5% of provincial mean) anchored to the Act. The majority's equivalent zone sits 2.8% above average, inside the threshold. The threshold is derived from EBCA § 14, not from any partisan estimate.

**Community fragmentation (§5.3.2).** The minority recommendation partitions Airdrie into four separate electoral divisions. The majority uses two. Both satisfy the Act's population band. The minority's choice requires voters in the same city to be represented across four separate legislative constituencies, each primarily identified with a different surrounding community.

**Boundary anchoring (§5.8.5) — retracted on canonical geometry.** Pre-shapefile analysis (Derived Provisional Geometries) showed the majority anchoring 71.0% of its perimeter to municipal edges, the minority 14.5% — a 4.9× gap. On official Elections Alberta shapefiles (received 2026-05-06), both maps fall within the 70–85% Canadian comparator norm: majority 80.0%, minority 72.0%. The DPG-era values did not survive canonical recomputation and the finding is retracted. The three chair-flagged cartographic anomalies (§5.8.2) are unaffected by this correction.

**Cartographic anomalies (§5.8.2).** Three boundaries were flagged by name in the majority report's own response text. All three appear under the minority recommendation: a lasso-shaped corridor district (Nolan Hill–Cochrane), a boundary extension through uninhabited Banff National Park (Rocky Mountain House–Banff Park), and a district named for three towns whose population is smaller than the fourth community the district captures. Zero chair-flagged anomalies appear under the majority.

**Partisan-bias metrics (§5.2).** Efficiency gap, mean-median difference, and declination are measured against a 1 million-plan MCMC neutral ensemble (official Elections Alberta shapefiles, canonical run). Under 2023 vote attribution, the minority map is more UCP-favourable than the majority on three of four metrics: mean-median +4.66 pp, seats@50/50 +5.62 pp, efficiency gap +3.92 pp. Declination reverses direction — consistent with asymmetric-packing geometry where NDP votes are concentrated in fewer, safer districts. The majority map is within the neutral null on all four metrics.

**MCMC neutral-ensemble outlier test (§5.4, Ch1).** The minority map's four partisan metrics jointly produce Mahalanobis D = 5.72 against the canonical ensemble covariance (p = 1.40×10⁻⁶). Against the 1 million-plan canonical ensemble (n_eff 1,429–1,682), three of four metrics individually exceed the 95th percentile: mean-median at p99.98, declination at p1.21 (NDP-tail), and seats@50/50 at p99.99 (ESS-adjusted lower bound ≈p98, above p95 — flag reinstated). Efficiency gap at p94.4 remains below the threshold and is not flagged. The joint Mahalanobis result stands. The majority sits at p0.92 — within the neutral null on all metrics.

**Fisher combined test (§5.4).** Fisher's method applied to Ch1 (Mahalanobis, p = 1.40×10⁻⁶) and Ch2 (SZAT swing-zone bootstrap, p = 0.0024) yields a joint p = 6.87×10⁻⁸ — approximately one in 14.5 million neutral draws. Both channels are seeded from publicly-verifiable drand League of Entropy beacon rounds predating the shapefile release. The combined finding is robust across Fisher, Stouffer, and Cauchy combination methods.

**Inter-map comparison test (§5.4, Ch1-COMP).** Pre-registered at OSF yvc7g. Does the minority-majority gap exceed the distance between randomly chosen neutral-plan pairs? Version A (EG-only): p = 0.0303. Version B (Mahalanobis joint): p = 0.0001. Both significant. The written prediction before running was that Version A would likely fail — it passed. The inter-map Mahalanobis distance (D = 7.19) exceeds each map's individual distance from the ensemble centroid (minority D = 5.71, majority D = 2.79), confirming the maps are positioned on opposite flanks of partisan-metric space rather than being co-located.

**Direction-of-travel (§5.4.10).** The 2019 enacted baseline sits at the statistical edge of neutral redistricting practice — Mahalanobis D²=12.75 against the canonical 1 million-plan ensemble (p=0.013). The majority 2026 map retreats toward the ensemble interior (D²=7.85, p=0.097 — inside the null). The minority 2026 map amplifies away from it (D²=32.67, p=1.40×10⁻⁶). SZAT boundary-choice tests confirm the pattern: the 2019→majority transition is consistent with neutral redistricting (p=0.309); the 2019→minority transition is marginally outside the null CI (p=0.053). Both 2026 proposals were drawn by the same five commissioners from the same 2019 baseline; they moved in measurably opposite directions on the partisan-metric axes the ensemble measures.

**One pre-registered pass (§5.3.5) — canonical.** The neighbour-drain adjacency test — which asks whether packed and cracked districts of the same party sit next to each other — finds, on the canonical Elections Alberta shapefiles, **1 coupled chain signal under the minority map, compared to 2 under the majority and 5 under the 2019 enacted map** (`findings/neighbour_drain_analysis.md`, run 2026-05-23). The minority's coupled count (1) is 0.50× the majority's — well below the pre-registered pass threshold of 1.5×; the pre-registered PASS criterion is met. The canonical run used clean topology (zero K-nearest fallback for any of the three maps); the result is robust against the DPG-era substrate-sensitivity that had previously produced different numbers on v0_2 (2/6, ratio 0.33×) and v0_8 (4/3, ratio 1.33× — direction reversed but still passing). §5.3.5 establishes the substantive explanation: the minority achieves its partisan effect via **hybridization** (city-splitting that internalises packing and cracking within single EDs), not the adjacency-chain packing model this test measures.

The audit does not claim the minority map is a gerrymander in the intent sense. It claims measurable structural divergence from the majority, at magnitudes that are unlikely to be explained by the ±25% population + contiguity + compactness constraint set alone.

---

## Forward-looking recommendations

Two policy recommendations attach to the audit findings.

**Act §12 amendment.** Section 12 of the *Electoral Boundaries Commission Act* permits referral of commission recommendations to a legislative committee with no statutory minimum notice or public-comment period. The audit proposes amending §12 to require: a 90-day minimum public-comment period before any referral, paired population tables showing both the statutory 2021-census baseline and an advisory Treasury Board quarterly-estimate sensitivity analysis, and a written explanation for any substantive deviation from commission recommendations. The proposal is in `docs/act_amendment_proposal.md`.

**AI-use discipline for the Lunty committee.** The Special Select Committee chaired by Brandon Lunty, MLA for Leduc-Beaumont, is due to report by November 2, 2026. If the committee uses AI tools in its work, the audit proposes seven disciplines: humans decide (not algorithms), every prompt is logged and published, evaluation criteria are registered before drafting begins, at least two independent tools are run in parallel, every boundary has a named human of record, every factual claim in AI-drafted text is human-verified, and the committee publishes a 9-item public disclosure checklist alongside the final map. The proposal is in `docs/ai_use_recommendations_for_committee.md` and summarised at §5.10 of the monograph.

---

## The structural cost

Both maps satisfy the law. The table below states the structural distance between them on five geometry-and-population measures (one retracted on canonical geometry) and two vote-dependent measures, in the same units, applied identically to both.

| Dimension | Majority 2026 | Minority 2026 | Gap |
|---|---|---|---|
| Population MAD (persons) | 3,180 | 4,707 | Minority 48% higher variance |
| Calgary NW zone population excess | +2.8% above mean | +11.5% above mean | 8.7 pp gap; minority 2.3× the +5% threshold, majority below it |
| Airdrie partition count | 2 EDs | 4 EDs | Minority 2× more fragments |
| Municipal-boundary anchoring *(retracted — canonical)* | 80.0% of perimeter | 72.0% of perimeter | Both within 70–85% Canadian norm; DPG-era values 71%/14.5%/4.9× did not survive shapefile recomputation |
| Chair-flagged cartographic anomalies | 0 | 3 | — |
| Efficiency gap (Phase 4C, canonical EA shapefiles) | +0.10% | +4.02% | Both below 7% reference; minority 40× more UCP-structural than majority (positive = UCP structural advantage) |
| Coupled packing-cracking adjacencies (canonical EA shapefiles, 2026-05-23 run) | 2 | 1 | Pre-registered PASS for the minority on canonical geometry: 0.50× ratio, well below the 1.5× threshold. Clean topology (zero K-nearest fallback). DPG-era runs (v0_2: 2/6, ratio 0.33×; v0_8: 4/3, ratio 1.33×) are superseded by this canonical run. §5.3.5 explains the hybridization mechanism, which is the substantive claim. |

The first five rows are vote-independent. They are measurable against public official records and do not change if the partisan substrate changes; the municipal-anchoring row is retracted on canonical geometry (both maps within norm). The last two rows depend on vote data; the sixth row's direction is not robust to the choice of spatial-attribution method; the seventh row is a finding in favour of the minority map.

A map that splits a city of 85,805 into four divisions — each identified with a different surrounding community — imposes a navigational cost on residents of that city that a two-division split does not. Three boundaries flagged by the commission chair in the official hearing record impose interpretive costs of the same kind — a corridor district whose narrow waist links Nolan Hill to Cochrane, an extension running through uninhabited Banff National Park, and a district named for three smaller towns whose population is dwarfed by the fourth community the district captures. Neither cost is measured in dollars; both are structural costs to effective representation as the *Saskatchewan Reference* [1991] articulates it.

The status quo cost — of not auditing — is the alternative: accepting or rejecting either recommendation on the basis of commentary and intuition rather than measurement.

---

## What makes this different

**The predictions came before the results.** Every test family in the audit was committed with a directional null hypothesis and a pre-specified pass threshold before the results were read. For the MCMC ensemble (Ch1), SZAT bootstrap (Ch2), drain test (Ch3), and inter-map comparison test (Ch1-COMP, OSF yvc7g), results are deterministic from seeds anchored to publicly-verifiable drand beacon rounds predating the commission's shapefile release. For the P/C/E signature framework, the detection criteria were specified in the same analytical commit as the detection run — an intra-session separation disclosed in full in §5.3.1 of the academic report. Ch1-COMP is the sharpest example of pre-commitment discipline: the written prediction before running was that Version A (EG-only) would likely *not* reach significance. It did (p = 0.0303). The audit reports this whether or not it helps — that is what pre-registration is for. A methodology that only finds what it was looking for, after it looked, is not a methodology — it is a post-hoc justification. Pre-registration prevents that.

**Each finding has a named retraction condition.** For every load-bearing finding, the audit documents what data or argument would force a retraction within 48 hours of it becoming available (in-repo operational discipline, not externally pre-registered; see methods-paper §6 for the full provenance). The conditions are in `analysis/methodology/retraction_pathway.md`. A reviewer who objects to a specific finding does not need to argue in the abstract — they can find that finding's retraction condition and produce the triggering evidence. The separate two-week sunset-clause window for DPG-to-canonical recompute (originally 48 hours; relaxed in Amendment 2 Change 11 on 2026-04-26) is documented at `findings/methods_paper_draft.md` §6 + §7.1 Stages 11–12, including the observed 12-day headline turnaround and 17-day full-integration overshoot on the Alberta 2025-26 case.

**The pre-registered passes are reported as prominently as the findings.** The neighbour-drain test result — 1 coupled chain signal under the minority, 2 under the majority, 5 under the 2019 enacted map on canonical Elections Alberta shapefiles (run 2026-05-23) — is reported as a §5.3.5 PASS (ratio 0.50×, threshold ≤ 1.5×), not buried in a supplementary table. The minority's low adjacency-chain count does not exonerate it; §5.3.5 establishes that the minority achieves its partisan effect via hybridization (city-splitting that internalises packing and cracking within single EDs), not via the classic adjacency-drain model this test measures. An audit that hides its non-findings is not an audit. The DPG-era substrate-sensitivity that produced different numbers on v0_2 and v0_8 is documented in the same finding file and in commit history; the canonical run is now the authoritative result.

**The same tests run on both maps.** Every metric applied to the minority recommendation is applied identically to the majority and to the 2019 enacted map. There is no test in this audit that runs only on the minority. This is the discipline the paper calls test-application symmetry.

**The apparatus has a dependency graph.** 263 analytical nodes across 413 directed edges — acyclic, zero orphan findings. Any dataset can be invalidated and the cascade of orphaned findings is computable in real time: `python analysis/scripts/dependency_query.py --invalidate L0:data.2023_statement_of_vote`. Invalidating the entire 2023 vote dataset still leaves the population-equality, Calgary zone, Airdrie fragmentation, and chair-flagged anomaly findings standing — the audit's headline does not collapse if the partisan-vote data is challenged.

---

## Open questions

This audit is not finished. The following are genuinely unresolved.

**Official geometry (Issue #1 — resolved 2026-05-06).** Elections Alberta released official vector shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`) on May 6, 2026 (commit `873f4d0`). All Derived Provisional Geometries have been replaced by the canonical boundaries; §5.2.7's direction claim is now anchored to official Elections Alberta shapefiles and the method-sensitivity noted in earlier versions of this section no longer applies. The DPG reconstruction pipeline remains documented for reproducibility.

**The counter-map challenge (Issue #14) — moot on canonical geometry.** The §5.8.5 anchoring finding's original retraction condition was: produce a map that achieves the minority's stated community-of-interest objectives with majority-comparable municipal-boundary anchoring. On canonical Elections Alberta shapefiles, both 2026 maps already fall within the 70–85% Canadian comparator norm (majority 80.0%, minority 72.0%), so the DPG-era 4.9× anchoring asymmetry the challenge was designed to falsify no longer exists. The §5.8.5 anchoring claim is retracted; the challenge is moot in its original form. The audit's live structural-coherence claim now rests on urban hybridization (§5.3.2), Airdrie city-splitting, and the chair-flagged cartographic anomalies (§5.8.2) — each of which carries its own named retraction condition in `analysis/methodology/retraction_pathway.md`.

**1 million-plan MCMC ESS-upgrade run — complete (2026-05-12).** The authoritative ensemble is 1 million plans (4 chains × 252,500 steps, same seed and shapefiles as the initial 250k run). Partisan-metric ESS is 1,429–1,682. The ESS-adjusted lower bound for the seats@50/50 flag rose from p89.72 (below p95 at 250k) to ≈p98 (above p95 at 1 million plans), reinstating the flag. All headline p-values and percentile placements in §5.4.9 reflect the 1 million-plan ensemble. An independent seed check (Section C, seed 3562959107, 100k plans) confirmed the population MAD and Reock null findings; partisan metrics are consistent within sampling variation.

*Note on why the 1 million-plan Ch1 p-value is less extreme than the 100k run:* as the ensemble grew from 100k to 1 million plans (n_eff 379 → 1,429 for the minimum metric), the Mahalanobis covariance matrix was estimated more precisely. The better-calibrated covariance shows the minority map is somewhat less extreme than the noisier 100k estimate suggested — Ch1 p moved from 1.60×10⁻⁷ to 1.40×10⁻⁶. This is a calibration effect, not a weakening of the finding. The Fisher combined p (6.87×10⁻⁸) remains overwhelming; the individual metric percentiles (mean-median p99.98, seats@50/50 p99.99) are stronger, not weaker, in the 1 million-plan run.

**The 2019-seeded MCMC ensemble (Issue #13).** The constraint-bound ensemble in §5.4 starts from a random seed, not from the 2019 enacted map. A chain seeded at the 2019 enacted geometry would more directly model incremental commission drawing and might place both 2026 recommendations differently within the ensemble distribution.

**Submission sentiment (§5.9.4) — coverage gap.** LLM intensity scoring of public submissions is complete. However, only 14.5% of the commission's published submission archive could be processed; the remaining 85.5% are absent from the public record. Findings from the scored subset are indicative, not representative, and §5.9.4 weighted-net sentiment results carry this caveat.

**Alberta's historical efficiency-gap baseline (Issue #16) — resolved 2026-05-12.** The 7% EG reference threshold is calibrated to US Congressional elections. Alberta-specific p95 EG thresholds were computed by running the same neutral ensemble under 2019 and 2015 vote shares (100k plans each, seeds from drand round 6099592): **2019 p95 = 1.01 %** (UCP landslide), **2023 p95 = 4.10 %** (competitive — canonical operative threshold), **2015 p95 = 9.71 %** (NDP wave). The jurisdiction-normed range is 1.01 %–9.71 %. The minority map is sub-threshold under 2019 and 2023 conditions and over-threshold only under 2015 conditions — a result reported per pre-commitment without threshold re-selection. The majority map is sub-threshold in all three contexts. The Stephanopoulos-McGhee 7 % reference sits between the 2023 and 2015 values; both maps pass under both standards. Full results and methodology in §5.2.8 and `analysis/methodology/threshold_provenance.md` B.2.1.C.

---

## What to do with this

**Challenge the audit.** Read `analysis/methodology/retraction_pathway.md`. Find a specific finding and its named retraction condition. Produce the data or argument that triggers it. The retraction conditions are public, concrete, and dated.

**Ask the Lunty committee about its process.** The Special Select Committee is due to report by November 2, 2026. Specific questions worth asking: What evaluation criteria were established before the committee began drawing? Will prompts and inputs to any AI tools used in the process be published? Will an ensemble of alternative maps be generated and published alongside the final map?

**Share the public-audience report.** [`reports/public/report_public.md`](reports/public/report_public.md) is written for a general audience. It covers the surviving structural findings, the gerrymander checklist, and what the April 16 pivot means — without requiring any background in electoral systems or statistics.

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

- **[docs/FINDINGS_BRIEF.md](docs/FINDINGS_BRIEF.md)** — **Quickest entry.** One-page plain-language brief: riding boundaries explained from scratch, seat-gap and wasted-vote findings, what the audit does not claim, CoI disclosure. Print-ready HTML version at [`docs/FINDINGS_BRIEF.html`](docs/FINDINGS_BRIEF.html).
- **[Web summary](https://ixby.github.io/alberta-electoral-boundaries-audit/)** — GitHub Pages version of the brief with the key chart embedded; designed for sharing with people unfamiliar with the topic.
- **[report_public.md](reports/public/report_public.md)** — Plain-language narrative for a general audience: the five findings, the gerrymander checklist, what the April 16 pivot means, and what you can do.
- **[report_academic.md](reports/academic/report_academic.md)** — The full monograph (pre-publication, continuously updated): executive summary, methods, §§5.1–5.10 results, seven measurement layers, dependency DAG, limitations, and falsifiability hooks. Start here to challenge a specific finding.
- **[analysis/methodology/retraction_pathway.md](analysis/methodology/retraction_pathway.md)** — Named retraction conditions per finding. The fastest path to either retracting a claim or confirming it holds.
- **[analysis/methodology/null_hypothesis_and_exoneration_criteria.md](analysis/methodology/null_hypothesis_and_exoneration_criteria.md)** — Pre-committed null hypotheses, pass thresholds, and Structural/Robust/Durable classification for every finding.
- **[analysis/methodology/plain_language_defense.md](analysis/methodology/plain_language_defense.md)** — Full entry-by-entry defense: 215 assertion/why/answer entries covering every substantive claim in the monograph, written for a reader with no background in GIS, statistics, or political science.
- **[analysis/methodology/methodological_defenses.md#test-apparatus-defense](analysis/methodology/methodological_defenses.md#test-apparatus-defense)** — Per-test criticism and response. Answers "are you making up metrics to have metrics?"
- **[analysis/methodology/threshold_provenance.md](analysis/methodology/threshold_provenance.md)** — Every numeric threshold traced to a statutory source, a literature citation, or a first-principles derivation. 41 thresholds catalogued, including three Alberta-calibrated EG alternatives (jurisdiction-normed range 1.01 %–9.71 %).
- **[analysis/methodology/audit_dependency_graph_readme.md](analysis/methodology/audit_dependency_graph_readme.md)** — The 234-node, 454-edge dependency graph: schema, worked examples, and the `--invalidate` query CLI.
- **[docs/ai_use_recommendations_for_committee.md](docs/ai_use_recommendations_for_committee.md)** — AI-use recommendations for the Lunty committee: seven principles, technical guidance by task type, and a 9-item public disclosure checklist.

---

## Acknowledgements

The author thanks the following for their willingness to engage with a pre-publication draft and provide independent methodological perspective:

- **Raymond Mok** (Elections Alberta) — for releasing the official 2026 electoral-division shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`) on 2026-05-06, which the audit's canonical recomputation depends on entirely. The Derived Provisional Geometry framework was a holding posture until those shapefiles arrived; the live structural-distance numbers in this README are all computed against the authoritative geometry Mr. Mok provided.
- **Duane Bratt** (Mount Royal University, Department of Economics, Justice, and Policy Studies; co-editor, *Orange Chinook: Politics in the New Alberta*) — political science and Alberta electoral systems review.
- **Lan Nguyen** (Mount Royal University, Department of Geography and Environmental Studies) — spatial methodology review.
- **Lynn Moorman** (Mount Royal University, Department of Geography and Environmental Studies) — GIS methodology review.

Pre-publication review is ongoing. Reviewers and data contributors are acknowledged for their time and assistance; findings and conclusions remain the sole responsibility of the author.

---

## Licensing and reuse

Input data is public-record material: Elections Alberta's 2023 Statement of Vote, Statistics Canada's 2021 Census (Open Government Licence — Canada), and the Electoral Boundary Commission's 2026 final report and appendices. Derived code and analysis are released under the MIT License. The Derived Provisional Geometries (DPGs) are original work produced by reconstructing machine-readable polygons from the commission's raster-only published maps; they carry the §4.1.4 sunset clause and should not be cited as authoritative electoral geography without reference to that clause and its rerun commitment.
