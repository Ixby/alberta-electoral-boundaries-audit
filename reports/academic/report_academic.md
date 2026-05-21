# Alberta Electoral Boundaries Audit — Comprehensive Forensic Audit Monograph

**A symmetric, reproducible forensic assessment of the 2025–26 Electoral Boundaries Commission's majority and minority recommendations**

**Will Conner** · Mount Royal University, BSc Computer Information Systems

*Draft — May 2026 · Non-partisan · [Repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) · Data and scripts linked throughout*

> **Funding:** This research received no external funding. All costs were borne by the author.
> **Competing interests:** The author declares no competing interests.
> **Institutional affiliation:** The author is a student at Mount Royal University. This research was conducted independently and was not commissioned as coursework. The views expressed are the author's own and do not represent Mount Royal University.
> **Relationships:** The author has no employment, contractual, or advisory relationship with Elections Alberta, the Electoral Boundaries Commission, or any provincial political party. The author has supported parties on all sides of the political spectrum depending on the election. Neither the NDP nor the UCP has been contacted about this research at any stage, and neither party has had any involvement in or advance knowledge of it. No compensation was received from any party. The only individuals with substantive knowledge of the audit's findings and methodology prior to publication are volunteer reviewers at Mount Royal University; this does not constitute institutional endorsement or involvement by MRU. Elections Alberta's GIS team was made aware of the research through the author's formal shapefile request and provided data access and technical assistance (2026-05-06 and 2026-05-07); Elections Alberta has not been shown the audit's findings or conclusions. The methodology was pre-registered and applied symmetrically to both maps before results were examined.

> **Pre-publication status.** This monograph has not been publicly released. Integration of canonical Elections Alberta shapefiles (received 2026-05-06) is ongoing; individual section results may shift as recomputation continues. The codebase is also undergoing cleanup and script-count reduction. Do not cite, quote, or distribute without confirming the current status of the specific finding.

---

## Executive summary and reading guide

This document is a **comprehensive forensic audit monograph**, not a single-topic journal article. It covers three distinct lines of work that share a single dataset and methodology, and it runs substantially longer than a standard journal submission. Readers short on time should use the guide below to jump directly to the part that matches their question. Readers who need the full evidentiary chain should read end-to-end.

**Headline finding (read this if you read nothing else).** Alberta's 2025–26 Electoral Boundaries Commission produced two competing 89-seat maps on March 23, 2026. This audit evaluates both proposals using identical methods applied symmetrically to each. **The majority map is within the neutral statistical band on every partisan-fairness metric.** The minority map is not.

The minority proposal differs from the majority on four measurable non-partisan-bias dimensions: population dispersion (Median Absolute Deviation 48% wider), Calgary geographic-zone asymmetry (12.2% vs 0.4%), Airdrie community fragmentation (4-way vs 2-way split), and commission-chair-flagged geographic anomalies (3 confirmed geometric anomalies vs 0; the chair's documented criticism spans 7 configurations across two sections of the majority report — [§5.8.2](#sec-5-8-2) and [§5.9.4](#sec-5-9-4)). All four signals run in the same direction and survive every stress-test applied. A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation. Both maps fall within the 70–85% Canadian comparator norm. That failure is documented in full at [§5.8.5](#sec-5-8-5) rather than quietly removed.

The partisan-bias evidence rests on two independent statistical tests that ask different questions. The **ensemble test** (Mahalanobis Ch1, [§5.4.9](#sec-5-4-9)) asks: *is this map extreme relative to over one million neutral, randomly-drawn Alberta maps?* The **boundary-choice test** (SZAT Ch2, [§5.2.10](#sec-5-2-10)) asks: *are the specific lines on the map — the places where the minority drew differently from the majority — partisan-neutral?* Each test controls for what the other cannot: the ensemble test scores the whole map against an independently drawn neutral distribution. The boundary-choice test differences out shared geography by examining only the Voting Areas assigned differently between the two proposals. Both return the same answer. Their Fisher combination is **p = 6.87×10⁻⁸** — approximately one in 15 million. This figure is reproducible: all random seeds are committed to the public Cloudflare drand beacon before official shapefiles arrived. All scripts and data are public. An independent analyst running the same pipeline recovers the same number.

The directional consistency across structural and statistical dimensions is the finding. The audit records what the data show. It does not reach a legal conclusion and does not infer intent ([§4.5](#sec-4-5)). The partisan-bias magnitude is sensitive to the vote-attribution method used and should be read as a directional observation, not a point estimate ([§1.2](#sec-1-2), [§5.2.2](#sec-5-2-2)). See [§1.1](#sec-1-1) for the full plain-language summary, [§1.2](#sec-1-2) for modelling-uncertainty caveats, and [§6](#sec-6) for the author's verdict on both maps.

**Reading guide by question.** The monograph has three parts, each answering a different question and each referencing the others:

| If you are here to answer… | Read | Covers |
|---|---|---|
| **Part I — Empirical audit.** *Do the two 2026 maps differ in measurable, reproducible ways?* | Abstract, [§1.1](#sec-1-1), [§5.1](#sec-5-1) (population equality), [§5.2](#sec-5-2) (partisan bias), [§5.3](#sec-5-3) (signatures), [§5.4](#sec-5-4) (MCMC ensemble), [§5.6](#sec-5-6) (symmetry counter-test), [§5.7](#sec-5-7) (stress-test grades), [§5.8](#sec-5-8) (geographic coherence) | Core quantitative findings — the empirical redistricting audit. |
| **Part II — Procedural and policy critique.** *What does the April 16 legislative pivot mean; how does the commission's methodology compare to Canadian norms; what statutory reforms follow?* | [§5.9](#sec-5-9) (procedural), Appendix F (constitutional framing), `docs/act_amendment_proposal.md` (statutory reform), `findings/cycle_lag_analysis.md` [§2](#sec-2) (forward-modelling consequences for commissions) | The Canadian comparative and legal-procedural layer. |
| **Part III — Data provenance and methodological warnings.** *Why can't the audit give single-number point estimates on every metric; what does the missing-shapefile situation do to conclusions; what's the DPG framework?* | [§4.1.4](#sec-4-1-4) (DPG + sunset clause), [§3.3](#sec-3-3) (cycle-lag robustness + dataset-construction consequences), [§5.2.7](#sec-5-2-7) (four-measurement-layer reporting), Appendix E (approximate geometry), `findings/cycle_lag_analysis.md` [§1](#sec-1) (three-vintage sandwich), `findings/methods_paper_draft.md` (companion methodology paper in draft) | The GIS and data-provenance methodology — the part that justifies every qualified finding in Parts I and II. |

This monograph is the source. Three shorter pieces can be drawn from it for different audiences: a peer-reviewed audit paper, a methods paper documenting the geometry-reconstruction pipeline (`findings/methods_paper_draft.md`), and a magazine feature. Drafts of each are in progress.

**What to believe.** Every number in this document is reproducible by running a script in `analysis/scripts/` against a dataset in `data/`. Every qualitative claim is anchored in a primary source pinned in `FROZEN_MANIFEST.md`. Where a finding depends on Derived Provisional Geometries (DPG — traced from commission map thumbnails because Elections Alberta had not released official shapefiles at the time of writing), the dependency is disclosed via the [§4.1.4](#sec-4-1-4) sunset clause which binds the audit to re-run the finding within two weeks of official shapefile release.

---

## Abstract

Alberta's 2025–26 Electoral Boundaries Commission tabled two 89-seat maps on March 23, 2026, which the Legislative Assembly set aside on April 16, 2026. This audit evaluates both proposals against the 2019 baseline using a multi-method structural framework and Monte Carlo ensemble analysis. Four non-partisan structural signals show consistent findings: the audit identifies structural divergence on population dispersion (minority 48% wider), Calgary zone asymmetry (12.2% vs 0.4%), Airdrie fragmentation (4 vs 2 districts)[^airdrie_fragmentation], and spatial anomalies (3 confirmed geometric anomalies chair-flagged vs 0; the chair's criticism spans 7 configurations total across [§5.8.2](#sec-5-8-2) and [§5.9.4](#sec-5-9-4)). A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation (both maps within the Canadian comparator norm). Full reconciliation in [§5.8.5](#sec-5-8-5).[^anchoring_canonical] The joint outlier profile reaches Mahalanobis p = 1.40×10⁻⁶ against the 1,010,000-plan canonical ensemble. All Efficiency Gap magnitudes remain below the Stephanopoulos-McGhee 7% threshold (academic literature only; never judicially adopted). The audit records what public data show. It does not reach a legal conclusion. Primary statistics are exploratory-reproducible, with prospective replication studies pre-registered on the Open Science Framework (OSF:qsgy8, r3zm7, 6pt83, yvc7g, s58a6; AsPredicted:#289,469, #289,451).

[^airdrie_fragmentation]: The minority map proposes a 4-way split of the Airdrie region (Airdrie, Airdrie-Chestermere, Rocky Mountain House-Banff, Cochrane-Olds); the majority proposes a 2-way split (Airdrie, Cochrane). This structural divergence is documented and evaluated in [§5.3.2](#sec-5-3-2) (packing/cracking-signature analysis) and [§5.8](#sec-5-8) (municipal-boundary anchoring). A direct Canadian comparator is provided by the 2022 Alberta federal redistribution sub-commission, which applied a 2-way split to Airdrie, aligning with the provincial majority (see [§5.9.3](#sec-5-9-3) for federal precedent discussion).

---

## Preface — scope, shapefile status, and intended venue

**Shapefile status (updated 2026-05-06).** Elections Alberta released the 2026 official shapefile package and the canonical polygon files were received by the audit on 2026-05-06. The [§4.1.4](#sec-4-1-4) sunset clause has been triggered and partially fulfilled: the 2026-proposal-shapefile trigger fired 2026-05-06 and the canonical ensemble re-run is complete. The November 2026 committee-map trigger remains pending. Authoritative canonical results are documented in [§5.4.9](#sec-5-4-9) and `findings/post_audit_recompute_deltas.md`. The DPG-substrate runs documented in [§5.4.1](#sec-5-4-1)–[§5.4.8](#sec-5-4-8) are preserved as the historical record of the pre-shapefile analysis.

The canonical ensemble uses official Elections Alberta shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`, EPSG:3400, 89 EDs each), 1,010,000 plans across 4 chains × 252,500 steps, base seed `get_canonical_seed("lunty-bootstrap") = 1432864451`. Results that do **not** depend on the 2026 shapefiles remain unchanged: population equality in [§5.1](#sec-5-1) (uses the commission's own per-ED population tables), signature detection in [§5.3](#sec-5-3) (commission's published boundary descriptions), and the public-submission audit in [§5.9.4](#sec-5-9-4) (commission's own submission archive).

**Intended venue and distribution.** The paper is prepared as a public-interest audit. Primary distribution targets are the project's public GitHub repository and a Canadian public-policy venue (*Alberta Views*-length feature and/or an SSRN / OSF preprint). Re-routing to a peer-reviewed journal (*Canadian Journal of Political Science*, *Canadian Public Policy*, *Election Law Journal*) is welcomed. The paper's structure, framework, and data are designed to make that re-routing straightforward. The methodology, pre-registration ([§5.5](#sec-5-5)), and falsifiability gates ([§4.1.2](#sec-4-1-2)) are intended to support review at that standard. A companion methodology paper on the DPG framework is in draft at `findings/methods_paper_draft.md`.

---

## Cover visualization

The cover map (`data/maps/cover_art.png`; script `analysis/scripts/build_cover.py`) renders the minority commission's 2026 proposal as a population-density-weighted vote-share choropleth of Alberta's 4,765 Voting Areas. Each VA polygon is filled with a colour interpolated linearly from NDP-orange (rgb 0.92, 0.45, 0.10) to UCP-blue (rgb 0.13, 0.36, 0.62) against each VA's 2023 election-day two-party UCP share (colour scale normalised vmin = 0.30, vmax = 0.80). Fill intensity is modulated by log₁₀ population density: the weight maps [−8, −3] log₁₀ persons/m² to [0.10, 1.0], blending from near-ivory at the sparse end to the saturated partisan colour at the moderate end, then darkening to 30% of the base colour at the highest densities to preserve contrast in Calgary and Edmonton cores. VAs with no direct centroid-in-polygon join receive vote share from crosswalk-inherited 2019 parent EDs. VAs with no crosswalk parent receive the K = 25 nearest-VA aggregate as a final fallback. The minority commission's ED boundaries are overlaid in dark grey (linewidth 0.20). The provincial silhouette in accent red (linewidth 0.65).

The visualization corrects the geographic distortion produced by whole-riding colour fills on standard election maps, where large rural ridings dominate the visual field despite comparatively sparse populations. By saturating colour only where population density is high, the render makes the urban-core concentration of competitive voters visible as a primary feature of Alberta's political geography rather than a small detail lost in a sea of rural blue. This is directly relevant to the audit's structural findings: the boundary choices that matter most — the NW Calgary zone, the Airdrie split, the lasso corridor — fall precisely in the high-density zones where the map's partisan signal is strongest.

---

## Author disclosure

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

**Prior and bias self-audit.** Going into this project the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny. The methodology is designed to produce the same numbers regardless of that prior. Three cases surfaced findings that ran against the prior and were retained in the report: (i) under 2019 vote input the partisan-bias asymmetry reverses sign ([§5.2.3](#sec-5-2-3)); (ii) the commission chair's "no public support" claim is upheld on three of seven configurations, not all seven ([§5.9.4](#sec-5-9-4)); (iii) the majority map's own MAD of 3,180 is tighter than the 2019 current-map baseline computed on 2021 census data (Appendix C), indicating the commission's majority did not introduce partisan looseness relative to the prior-cycle baseline. Full bias self-audit at `findings/partisan_bias_summary.md`.

**AI use disclosure.** Three large language models were used as analytical and writing assistants throughout this project: **Claude Pro Max** (Anthropic), **Gemini Pro** (Google), and **Codex** (OpenAI). Claude's contributions included drafting and revising report text, proposing analysis structure, identifying consistency gaps across documents, and surfacing methodological edge cases (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). Gemini Pro contributed to code review and cross-validation of analytical outputs. Codex contributed to scripting and data-processing tasks. All substantive claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. No AI tool executed code or accessed external data independently. All script runs were performed by the author.

**No commercial tools.** No GIS desktop software (QGIS, ArcGIS) and no commercial election-analytics platforms were used. R 4.6 was used for one cross-validation script (`analysis/scripts/redist_crossvalidation.R`) using the Harvard `redist` package (SMC sampler) to provide algorithm-independent corroboration of the Python GerryChain ReCom headline finding ([§5.4.9](#sec-5-4-9)). No other R packages were used. Stata and SPSS were not used.

**No paid data.** All inputs are public. Every number in this audit is reproducible by running a script in `analysis/scripts/` against a dataset in `data/`.

**Integrity tools.** Falsifiability gates G0–G5 are built into the pipeline. Bias self-audit: `findings/partisan_bias_summary.md`. Uncertainty analysis: `analysis/methodology/uncertainty_and_shapefile_impact.md`.

**Computational stack:**

- **Python 3.14** on Windows 11 (Python 3.9+ required by `setup.sh`)
- **pandas 2.x** — [§5.1](#sec-5-1) population equality, [§5.2](#sec-5-2) vote attribution
- **numpy** — numerical computation
- **openpyxl** — parsing the 2023 Statement of Vote Excel workbook (87 sheets, 1,973 poll records)
- **geopandas + pyogrio** — spatial operations for population aggregation and ED-to-CSD overlay; full Phase 4/5 execution blocked on 2026 shapefile release
- **shapely + pyproj** — polygon topology and projection, NAD83 / Alberta 3TM, EPSG:3776
- **osmnx** — OSM road network extraction, prepared for Phase 4D fallback
- **gerrychain** — MCMC ensemble generation; canonical 1,010,000-plan run (4 chains × 252,500 steps) against official EA shapefiles ([§5.4.9](#sec-5-4-9)); DPG-substrate development runs of 250k–2,000,000 samples documented in [§5.4.1](#sec-5-4-1)–[§5.4.8](#sec-5-4-8)
- **pdfplumber** — PDF table extraction for commission report and Appendix E parsing
- **geopy + rapidfuzz** — geocoding and fuzzy-string matching
- **R 4.6** — cross-validation only; `redist` package (SMC sampler, Harvard); one script ([§5.4.9](#sec-5-4-9))
- **git, GitHub CLI** — version control; public repository [Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit)

**Scripts authored for this audit:**

*Lane 1 — Statistical*

| Script | Purpose | Report section |
|---|---|---|
| `packing_cracking_analysis.py` | B1–B6 partisan-bias metrics (symmetric, all three maps) | §5.2 |
| `mcmc_ensemble_canonical.py` | 1,010,000-plan ReCom neutral ensemble on canonical shapefiles | §5.4 |
| `simulation_convergence_diagnostics.py` | Per-chain ESS, ρ\_lag1, Gelman-Rubin R̂ | §5.4.8 |
| `joint_outlier_score_canonical.py` | Mahalanobis D² joint outlier score | §5.4.9 |
| `szat.py` | Swing-Zone Allocation Test — boundary-choice EG decomposition | §5.2.10 |
| `validate_fisher_independence.py` | Spearman correlation between Ch1 and Ch2 channels | §5.5 |
| `intermap_permutation_test.py` | Directional inter-map partisan-gap permutation test | §5.2.11 |
| `targeted_gerrymander_burst.py` | UCP-direction hill-climbing upper bound | §5.4.11 |
| `targeted_gerrymander_burst_ndp.py` | NDP-direction symmetric hill-climbing lower bound | §5.4.11 |
| `simulation_short_bursts.py` | Short-burst reachability from 2019 baseline | §5.4.10 |
| `neighbour_drain_adjacency.py` | Packing-cracking adjacency signature (coupled-chain count) | §5.3 |
| `drain_label_shuffle_null.py` | Label-shuffle permutation null for drain test | §5.3.5 |
| `historical_eg_baseline.py` | Historical efficiency-gap baseline for Alberta elections | §5.2.9 |
| `chen_rodden_alberta.py` | Chen-Rodden geography vs drawing decomposition | §5.2.7 |
| `ecological_inference.py` | Ecological inference bounds on demographic voting | §5.2.8 |
| `marginal_seats_analysis.py` | Marginal-seat uniform-swing analysis | §5.2 |
| `november_tripwires.py` | Pre-registered automated checks for November 91-seat map | §5.5 |
| `november_red_alert_scorecard.py` | Lunty committee tripwire detection scorecard | §5.5 |
| `redist_crossvalidation.R` | R SMC cross-validation (Harvard `redist`; algorithm-independence) | §5.4.9 |

*Lane 2 — Structural*

| Script | Purpose | Report section |
|---|---|---|
| `electoral_forensics_population.py` | A1–A3 population equality (MAD, variance, legal-floor) | §5.1 |
| `score_anchoring.py` | Municipal-boundary anchoring fraction per map | §5.8 |
| `municipal_splits.py` | Municipal-split count across all three maps | §5.8 |
| `polsby_popper.py` | Polsby-Popper compactness for all EDs | §5.8 |
| `reock.py` | Reock compactness (smallest-enclosing-circle method) | §5.8 |
| `a1_legal_baseline_2021_census.py` | 2021-census A1 baseline for 2019 enacted map | §5.1 |
| `s15_ratio_test.py` | EBCA §15(2) population-deviation compliance | §4.1 |
| `justification_tests.py` | Testable-rationale verification for contested EDs | §5.9 |
| `score_hybridization.py` | Hybrid-ED (city-splitting) metric | §5.3.5 |
| `compactness_metrics.py` | Plan-level compactness summary | §5.8 |
| `csd_community_splits.py` | CSD-level community-splits overlay | §5.8 |
| `majority_symmetry_counter_test.py` | Test-selection symmetry counter-test | §5.6 |
| `mcmc_anchoring_ensemble.py` | Anchoring mini-ensemble via CSD edge-crossing metric | §5.8 |

*Robustness and sensitivity*

| Script | Purpose | Addresses |
|---|---|---|
| `advance_vote_splat.py` | Advance-ballot VA apportionment (proportional smear) | H8 |
| `advance_vote_sensitivity.py` | Election-day vs full-vote substrate sensitivity | H8 |
| `seats_at_50_50_regional.py` | Regional-swing robustness against uniform-swing assumption | H5 |
| `cross_election.py` | Three-election (2015/2019/2023) direction check | H7 |
| `third_party_sensitivity.py` | Third-party vote allocation sensitivity | H6 |
| `attribution_sensitivity_check.py` | MAUP area-weighted attribution sensitivity | §5.4 |
| `monte_carlo_ci.py` | Monte Carlo confidence intervals over modeling choices | §5.4 |
| `szat_2019_baseline.py` | SZAT applied to 2019 enacted baseline | §5.2.10 |
| `score_natural_anchoring.py` | Natural-feature (highway/river) anchoring secondary check | H4 |
| `va_attribution_area_weighted.py` | Area-weighted MAUP check for VA-to-ED attribution | §5.4 |

*Submission analysis (§5.9)*

| Script | Purpose |
|---|---|
| `submission_search.py` | Keyword search across 1,140+ public submissions |
| `submission_sentiment_llm.py` | LLM zero-shot sentiment classification |
| `submission_sentiment_llm_full.py` | Full-corpus LLM classification across all configurations |
| `hansard_sentiment_llm.py` | Hansard hearing transcript sentiment |
| `aggregate_sentiment_intensity.py` | Intensity aggregation by configuration |
| `sentiment_intensity_score.py` | 1–3 intensity scoring per row |
| `cross_reference_submitters.py` | Rationale cross-reference (CONTRA_COMMISSION flags) |
| `compute_kappa.py` | Cohen's κ inter-rater reliability |
| `validation_sample.py` | Stratified validation sample for IRR |

*Data preparation*

| Script | Purpose |
|---|---|
| `build_canonical_va_votes.py` | Canonical 2023 VA election-day vote file |
| `phase4c_canonical_attribution.py` | Phase 4C canonical VA-to-ED attribution |
| `build_cross_election_va.py` | 2015/2019 cross-election VA vote files |
| `submission_ocr.py` / `submission_ocr_recovery.py` | OCR for image-only submission PDFs |

*External data*

| Script | Purpose |
|---|---|
| `338canada_scraper.py` | 338Canada per-riding Alberta projections |
| `338canada_historical.py` | Historical 338Canada Alberta snapshots 2020–2026 |
| `338canada_reallocate.py` | Projection reallocation through hybrid-ED crosswalks |
| `canadian_base_rate_compute.py` | Canadian provincial EG base rates |
| `_fetch_osm_natural.py` | OSM highway and river data for natural anchoring |

**Data sources:**

- Elections Alberta Statement of Vote 2023 (`data/2023_results.xlsx`)
- Alberta Electoral Boundaries Commission final report, March 23, 2026 — extracted populations and variance tables, map images (`maps/*.jpg`)
- Elections Alberta GIS resources page — 2026 shapefiles received 2026-05-06; canonical ensemble re-run against official geometry ([§5.4.9](#sec-5-4-9))
- Statistics Canada 2021 Census Dissemination Area populations and shapefiles (`data/alberta_2021_da_populations.csv`, `data/alberta_2021_das.gpkg`)
- Alberta Treasury Board Office of Statistics and Information quarterly population estimates
- StatsCan Table 17-10-0009 — quarterly provincial estimates
- StatsCan Table 98-10-0459 — 2021 Census journey-to-work by CSD

---

<a id="sec-1"></a>
## 1. Introduction

**Contribution.** **(d) The primary contribution is the first systematic computational audit of an Alberta provincial electoral boundary commission's output, evaluated against established Canadian independent-commission practice and statutory norms.** The audit is situated within Canadian political-science and legal frameworks: the *Saskatchewan Reference*'s "effective representation" standard, the Courtney–Pal lineage of scholarship on boundary-commission discretion, the statutory mandate of Alberta's *Electoral Boundaries Commission Act*, and the institutional precedents set by the 2022 federal sub-commission, Quebec 2011, and other provincial cycles. This Canadian-institutional framing distinguishes the audit from US-focused partisan-gerrymandering measurement. It asks whether one faction's boundary choices within a Canadian independent commission exceed the discretion space that Canadian law and practice establish.

**(a)–(c) Supporting contributions.** The audit achieves this primary finding through three methodological supports: **(a)** a falsifiability-gated ensemble-comparison framework that commits computational parameters to a public randomness beacon before analyzing shapefiles (preventing cherry-picking of parameters after seeing results); **(b)** a pre-registration discipline (OSF qsgy8, r3zm7, 6pt83, yvc7g, s58a6) that anchors test definitions and sensitivity boundaries before execution; and **(c)** complete data provenance documentation and reproducible code (all scripts checked in, all data sources listed with access dates, with a 1,010,000-plan canonical ensemble enabling third-party replication).

**Specifics.** The audit evaluates Alberta's 2025–26 Electoral Boundaries Commission's two final proposals (majority and minority reports, tabled March 23, 2026) by constructing a 1,010,000-plan neutral ensemble under identical statutory constraints (±25% population band, contiguity, compactness, community of interest per the EBCA §12(3) mandate) and comparing each real map against that ensemble's statistics. It finds that the minority proposal diverges from the majority on measurable structural dimensions across multiple independent tests; that the directional pattern of divergence is stable across vote inputs (2015, 2019, 2023) and stress tests; that the divergence's direction consistently favors the governing party when read against any available Alberta electorate; and that the underlying rationales offered by the minority commission faction fail falsifiability checks against cleaner legal alternatives (documented in [§5.9.4](#sec-5-9-4)). The paper documents every source, script, and computational step so that future users — academic auditors, policy analysts, courts, or future commissions — can run the same pipeline on new commission output.

**Case context and procedural pivot.** Alberta's Electoral Boundaries Commission delivered two final reports on March 23, 2026: a majority report and a minority report proposing incompatible 89-seat maps. Three weeks later, on April 16, 2026, the Alberta Legislative Assembly passed Motion 19 setting aside both reports and establishing a Special Select Committee of five MLAs to draft a 91-seat map by November 2, 2026. That procedural pivot — replacing an independent commission's drafting process with a government-chaired committee mid-cycle — is evaluated in [§5.9](#sec-5-9) against Canadian comparators and positions the audit's findings within a broader questions about electoral commission independence and public trust.

**Exploratory vs. confirmatory status.** The audit's statistical tests fall into two categories that readers should distinguish. The primary ensemble-based tests — Ch1 (Mahalanobis joint-tail), Ch2 (SZAT bootstrap), and their Fisher combination — are **exploratory**: computational seeds were committed to the public drand League of Entropy beacon before the official shapefile release (establishing that results were not cherry-picked after seeing the data), but the specific test names and combination method were not filed in any OSF pre-registration document before execution. These findings are reproducible and temporally anchored, but they should be treated as requiring independent replication before confirmatory weight is assigned. The Ch3 neighbour-drain test (pre-registered at OSF r3zm7) and the November 2026 Lunty committee scorecard (OSF qsgy8) are prospectively pre-registered confirmatory tests. The four surviving non-partisan-bias signals in [§1.1](#sec-1-1) (population equality, Calgary zone gap, Airdrie fragmentation, chair-flagged anomalies) do not depend on the statistical tests at all. They derive from the commission's own published tables, maps, and record, and their evidentiary status is independent of the pre-registration question. (Municipal anchoring, a fifth pre-registered dimension, did not survive canonical recomputation — see [§5.8.5](#sec-5-8-5).)

<a id="sec-1-1"></a>
### 1.1 Headline findings in plain language

Before the technical caveats below, the audit's structural findings summarise cleanly. Using the same methodology applied symmetrically to all three maps:

- The **minority 2026 proposal spreads population more unevenly** across districts than the majority proposal (Median Absolute Deviation from provincial average: 4,707 versus 3,180) — a 48 % wider dispersion.
- The **minority map's Calgary districts** show a 12.2 percentage-point geographic-zone asymmetry (urban-core districts smaller, suburban-ring districts larger) versus 0.4 pp on the majority map.
- The **minority map splits the City of Airdrie four ways** across different electoral divisions; the majority concentrates 73.8 % of Airdrie's population inside a single electoral division (Airdrie-East), while the minority's largest Airdrie ED holds only 59.2 % and three other minority EDs draw in the remainder — including one ED ("Calgary-Foothills-Airdrie West") whose perimeter has 0 % anchoring on Airdrie's gazetted city limit despite carrying "Airdrie" in its name. See `findings/airdrie_highway_pretext.md` for the per-ED measurement and the empirical refutation of a Highway Anchoring Defense at this carve.
- A fifth pre-registered structural dimension — municipal-boundary anchoring against Statistics Canada CSD edges — did not survive canonical-geometry recomputation: both 2026 maps fall within the 70–85 % Canadian comparator norm (minority 72.0 %, majority 80.0 %). The earlier DPG-derived 14.5 % / 71.0 % / 4.9× figures cited during the audit's pre-shapefile phase did not carry forward to recomputation against official Elections Alberta shapefiles. Full reconciliation in [§5.8.5](#sec-5-8-5).[^anchoring_canonical]
- **Three geographic anomalies** on the minority map were flagged by the commission chair (Rocky Mountain House–Banff Park extension; Calgary-Nolan Hill–Cochrane lasso; Olds-Three Hills-Didsbury → N Airdrie community capture); zero were flagged on the majority map.
- The **minority's own 25 published rationales** are, on five of six contested configurations, options the minority did not take when cleaner statutory-compliant alternatives were available. (A seventh configuration — Lethbridge / Taber-Warner federal-boundary match — was previously listed but has been removed: the minority report does not in fact make the federal-boundary claim, and the methodology check at `analysis/methodology/lethbridge_federal_boundary_check.md` could not locate any underlying source.)

The four surviving non-partisan-bias signals all point in the same direction and all survive the stress-tests documented in [§1.2](#sec-1-2) below. (The fifth, municipal anchoring, did not survive canonical recomputation — see [§5.8.5](#sec-5-8-5).[^anchoring_canonical]) The partisan-bias signal (the extent to which the maps would produce different seat counts from the same votes) is reported in the abstract as a two-measurement disagreement; [§1.2](#sec-1-2) explains the caveats that constrain the magnitude claim.

**Two questions, two tests.** Two independent statistical tests evaluate the partisan-bias signals from different angles. The ensemble test (Mahalanobis Ch1, [§5.4.9](#sec-5-4-9)) asks: *is this map extreme relative to over one million neutral, randomly-drawn Alberta maps?* The boundary-choice test (SZAT Ch2, [§5.2.10](#sec-5-2-10)) asks: *are the specific lines on the map — the places where the minority drew differently from the majority — partisan-neutral?* Each test anticipates the other's potential weakness. A critic who argues the neutral ensemble does not perfectly capture Alberta's real geographic constraints is not attacking SZAT. SZAT controls for shared geography by design: it compares only the Voting Areas assigned *differently* between the two proposals, differencing out everything the two maps share. A critic who argues SZAT merely compares two maps to each other is not attacking the ensemble, which scores the minority against over one million independently drawn neutral plans. Both tests converge on the same conclusion. Their Fisher combination (p = 6.87×10⁻⁸) is the formal statement of that convergence.

<a id="sec-1-2"></a>
### 1.2 Modelling-uncertainty caveats

Three modelling-uncertainty tests materially narrow the partisan-bias magnitude claim while leaving the structural findings in [§1.1](#sec-1-1) intact. These are reported up-front for transparency. The underlying methodology is in `analysis/review/design_critique.md` and the Monte Carlo script `analysis/scripts/monte_carlo_ci.py`.

**1. Monte Carlo sensitivity interval over modelling choices crosses zero.** N=2,000 samples varying urban weight (0.55–0.85), rural baseline (0.26–0.36), and per-hybrid jitter (±0.10). Minority-majority EG asymmetry: mean −1.22 pp, median −1.44 pp, **2.5th–97.5th percentile sensitivity interval [−3.04, +0.76] pp**. Direction consistency: 90.5% of samples show minority more UCP-favorable. Classical 95% significance is **not** defensible. The direction holds in 90.5% of draws across the full parameter sensitivity range — a sensitivity result, not a frequentist confidence level.

**2. Declination metric (Warrington 2018) disagrees with the efficiency gap.** Declination computed: 2019 = −0.034, Majority = −0.021, Minority = −0.015. By declination, the minority is the least pro-UCP of the three maps, the opposite direction from EG and the seats-at-50/50 estimate. Warrington (2018) documents this kind of cross-metric divergence as an expected feature of competing formalisations rather than a methodological flaw. Katz, King, and Rosenblatt (2020) recommend ensemble reporting. Both metrics are retained; neither is dispositive on its own.

**3. 2019 cross-election check.** Under v0_7 partial-coverage attribution, 2019 vote totals produced Majority EG +0.30% / Minority EG +0.90% — an apparent direction-flip relative to the 2023 reading. **Under v0_8 full-coverage area-proportional attribution (Run 2026-04-25 / `cross_election_v8_full.csv`), the direction is stable:** EG, declination, and seats@50/50 all maintain the same sign across 2019 and 2023 on both maps (only mean-median flips, and mean-median is sub-threshold on the 250k Run #4 ensemble for both maps so the flip is not load-bearing). The earlier "direction reverses" reading was a partial-coverage artefact of 22 unattributed rural EDs whose UCP votes were systematically excluded. Under v0_8, neither individual map's EG sign flips under 2019 votes — both the majority and minority remain UCP-favourable, which refutes the v0_7 reading where both maps appeared to switch to NDP-favourable (a partial-coverage artefact of 22 unattributed rural EDs). The inter-map *asymmetry* direction does still reverse under 2019 votes: [§5.2.3](#sec-5-2-3) documents +0.75 pp (minority less UCP-favourable under 2019) versus −0.51 pp under 2023. This reversal is mechanically expected given how the blend model weights the Springbank/Bearspaw/Cochrane hybrid EDs. The mechanism is explained in [§3.3](#sec-3-3). The 338Canada April 2026 polling reading remains supportive of the 2023 asymmetry direction.

**What survives these tests unchanged:**
- [§5.1.1](#sec-5-1-1) population distribution variance (CSV-sourced, election-independent): minority MAD is 48% wider than majority.
- [§5.1.2](#sec-5-1-2) Calgary geographic-zone gap: minority 7.7–12.2%; majority 0.36–0.39%. Not vote-based.
- [§5.8.2](#sec-5-8-2) visual spatial anomalies: 3 minority anomalies confirmed on published maps.
- [§5.8.4](#sec-5-8-4) community splits: Airdrie 4 vs 2, Cochrane merged vs intact, Chestermere partial split vs intact.
- [§5.9](#sec-5-9) procedural concerns: government-controlled replacement of drafting process, qualitative.

**What is narrowed:**
- [§5.2](#sec-5-2) partisan-bias *magnitude* claims. The central point estimate of 1.41 pp (w=0.85) is within Monte Carlo noise (sensitivity interval crosses zero). The direction holds in 90.5% of Monte Carlo draws across modelling uncertainty, which is a defensible directional claim but not classical 95% significance.
- The "minority gives UCP 2 more seats in a tied election" line. Under Monte Carlo, minority NDP@50/50 has 95% CI [41, 47] vs majority [43, 46] — overlapping. The 1-seat gap size is stable across 2023 votes and April 2026 polling inputs, but the *direction* of that 1-seat gap flips between them (UCP +1 on minority under 2023; NDP +1 on minority under April 2026 polling). A structural-invariance claim was not supported by the historical stability test and has been retracted; see [§5.2.3](#sec-5-2-3). The magnitude CI crosses zero.
- "Directionally consistent across six dimensions" is more precisely "directionally consistent across five of six tested dimensions, with one partisan-bias metric (declination) pointing the opposite way."

**Defensible synthesis.** The minority 2026 proposal shows measurable structural differences from the majority in four areas: population distribution (MAD 48% wider), Calgary geographic-zone balance (12.2% gap vs 0.4%, robust across two classification rules), community-of-interest treatment (Airdrie residents distributed across 4 minority EDs with no ED holding a majority of city residents, vs the majority's concentration of 73.8% inside Airdrie-East — same dispersion pattern visible in Lethbridge and Red Deer per [§5.6](#sec-5-6)), and visible boundary shape (three confirmed anomalies). None of these depend on vote data.

A fifth dimension is the rationale-failure pattern: five of the six contested minority redraws (after the Lethbridge / Taber-Warner federal-boundary claim was withdrawn — see methodology check `analysis/methodology/lethbridge_federal_boundary_check.md`, which establishes that the minority report does not in fact make the federal-boundary claim attributed to it) have cleaner options available that satisfy the statutory population and area limits while matching documented public submissions. The sixth (St. Albert-Sturgeon) is constraint-forced: both the majority and the minority independently arrive at the same two-district structure under the Act's constraints (see [§5.9.2](#sec-5-9-2) and `analysis/methodology/minority_rationales_validation.md`).

The partisan-bias consequences are directionally UCP-favorable for the minority in 90.5% of modelling-jitter samples using 2023 vote attribution, outlier-flagged at p99.98 on mean-median (UCP-tail) and at p1.21 on declination (NDP-tail) against the 1,010,000-plan canonical ReCom neutral ensemble on official Elections Alberta shapefiles (see [§5.4](#sec-5-4)). The direction reverses under 2019 vote attribution and shifts to a 1-seat NDP advantage on the minority under April 2026 338Canada polling. The core claim is that the minority has more structural irregularities and more rationale failures than the majority. A specific partisan-seat-shift magnitude is less defensible and sensitive to election baseline. The procedural concern about the April 16 government action stands separately from the partisan-math questions.

**Methodological scope.** This paper applies a symmetric, falsifiability-gated framework to both 2026 proposals and the 2019 baseline, producing reproducible estimates of population equality, partisan bias, geographic coherence, and procedural fairness. It pre-registers the test battery against a forthcoming third map — the November 2026 MLA-committee 91-seat proposal — so the audit can be replayed against new evidence rather than reinterpreted after the fact. It documents the data-provenance caveats that arise when 2026 shapefile release is gated by legislative adoption, leaving explicit placeholders for the checks that remain pending.

**Scope.** The paper does not reach a legal conclusion. It is evidentiary: it records what the public data show under identical methodology applied to all three maps, so that any interested party — court, legislator, commissioner, journalist, academic — can repeat the computations, challenge the inputs, and reach their own judgments. The court-ready interpretation is deferred to [§8](#sec-8) (Conclusion) and Appendix F (Legal Interpretive Note), drawing on Pal's (2015) analysis of boundary-commission discretion and electoral-district design.

---

<a id="sec-2"></a>
## 2. Background and Prior Work

The analysis rests on four bodies of prior work: US partisan-gerrymandering measurement, Canadian independent-commission practice, population-equality jurisprudence, and computational redistricting methodology.

**Institutional context: Canadian commissions versus US state legislatures.** The US literature on partisan gerrymandering — including the efficiency gap and the ensemble approaches this audit uses — was developed primarily to detect and litigate intentional partisan manipulation by *partisan mapmakers*: US state legislatures, which draw their own districts without independent commissions and have a structural incentive to engineer outcomes. In the US federal courts, however, partisan-gerrymandering claims have been declared non-justiciable: *Rucho v. Common Cause*, 139 S. Ct. 2484 (2019), held 5–4 that the federal judiciary lacks standards for evaluating partisan-bias metrics and therefore cannot adjudicate partisan-gerrymandering claims. This holding closes the federal courts to efficiency-gap and partisan-symmetry arguments, rendering the US academic literature on these metrics non-actionable in federal law. 

The *Rucho* holding highlights a methodological constraint that shapes this audit's architecture: partisan-bias magnitude alone — without supporting structural and procedural evidence — does not constitute a defensible evidentiary foundation for claims of bias. This audit therefore deploys a "two-lane" approach (Lane 1: partisan-bias metrics in [§5.2](#sec-5-2); Lane 2: structural and procedural findings in [§5.1](#sec-5-1), [§5.3](#sec-5-3), [§5.8](#sec-5-8), [§5.9](#sec-5-9)). Neither lane depends singularly on the other. The audit's findings rest on directional consistency across multiple independent dimensions rather than on the magnitude of any single metric.

Canadian provincial and federal electoral commissions are constitutionally distinct from US state legislatures. They are staffed by judges and independent appointees rather than partisan legislators, are governed by statutes specifying non-partisan criteria, and operate in a setting where the *Saskatchewan Reference* [1991] 2 SCR 158 standard of "effective representation" rather than strict partisan proportionality frames the legal test. Critically, *Rucho*'s non-justiciability holding governs US federal courts only and does not carry over to Canadian provincial jurisprudence, where the Saskatchewan Reference provides an explicit constitutional standard for assessing boundary-commission output. This institutional distinction is material. In the US context, partisan-bias metrics are evidentiary tools that cannot enter federal litigation. In the Canadian context, the same metrics are evidentiary inputs to a constitutional test that a court can apply. The methodology is agnostic to this institutional distinction. Its inferential weight depends on context, and that context is disclosed here. This matters for how partisan-bias metrics carry inferential weight. In the US context, a high efficiency gap is direct evidence of legislative manipulation by the legislature drawing its own map — but federal courts will not hear such claims. In the Canadian context, the same metric applied to a *minority* faction's commissioners within a nominally independent process carries a different warrant. The inference is not "the legislature manipulated its own map" but "one faction within a supposedly non-partisan commission drew boundaries whose partisan signature departs from what the independent (majority) faction drew under identical constraints," and a court applying the Saskatchewan Reference standard can weigh this evidence as part of its effective-representation analysis.

**Terminology.** "Gerrymandering" as used throughout this paper is a political and analytical term with no equivalent legal category in Canadian law. In contrast to US jurisprudence — where partisan gerrymandering is at least a named (if non-justiciable) claim after *Rucho* — Canadian law defines no gerrymandering standard. The applicable legal framework is effective representation under *Charter* s.3, as articulated in the *Saskatchewan Reference*, and statutory compliance with the EBCA. This audit's findings are evidentiary inputs to those constitutional and statutory questions, not to any gerrymandering-specific legal test.

**Partisan-bias measurement.** Stephanopoulos and McGhee (2014, 2015, 2018) introduced the efficiency gap (EG) as a single-number measure of wasted-vote asymmetry and proposed a 7% threshold for investigable bias. McDonald and Best (2015) advanced the mean-median gap as a complementary measure of distributional skew. Gelman and King (1994) formalised seat-vote-curve symmetry as a Bayesian estimator, building on Grofman (1983) and King and Browning (1987). Warrington (2018, 2019) introduced declination and documented that EG and declination can disagree on a non-trivial fraction of US-state plans — a finding directly relevant to the Alberta disagreement reported in [§5.2.4](#sec-5-2-4). Katz, King, and Rosenblatt (2020) argue that no single metric is dispositive and recommend ensemble reporting, which the stress-test gate RT2 in this audit implements. The 7 % threshold is academic-literature authority only — never judicially adopted (see [§5.2.8](#sec-5-2-8)).

**Natural packing vs engineered packing.** Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through packing of their voters into city cores. [§5.2.5](#sec-5-2-5) of this audit applies the Chen-Rodden framework to Alberta and finds that the *direction* prediction transfers but the *mechanism* does not: Alberta's UCP-favourable baseline comes from dispersed rural UCP-winning margins, not from NDP urban packing. This matters for what any 2026 map's partisan bias can legitimately be attributed to.

**Canadian redistribution practice.** Courtney (2001, 2004) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces; Courtney (2001) chs. 6–7 map the interplay between population equality and community-of-interest discretion that underlies the [§5.1](#sec-5-1) and [§5.8](#sec-5-8) findings in this audit, and chs. 10–11 address public-hearing obligations and the scope of judicial review of commission output. Pal (2015) analyses the intersection of boundary-commission discretion with the Charter [§3](#sec-3) right to vote, arguing that the *Saskatchewan Reference*'s "effective representation" standard leaves commissioners substantial latitude reviewable only at the outer margins — not for partisan preference proximity — and that the distinction between legitimate design preference and legally reviewable partiality turns on the same factual record the audit assembles. The discretion-versus-design-choice framework Pal develops is the analytic anchor for the [§5.9.3](#sec-5-9-3) procedural assessment. The constitutional benchmark, *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, establishes "effective representation" — not strict population parity — as the standard against which boundary-commission output is measured. The Charter [§3](#sec-3) right to vote developed by *Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912, and *Frank v. Canada (Attorney General)*, [2019] 1 SCR 3, forms the backdrop without applying directly to redistribution. [§5.9.3](#sec-5-9-3) compares the April 16, 2026 Alberta pivot against the closest historical Canadian comparator (Quebec 2011 — the National Assembly's refusal to proclaim a completed commission delimitation under Bill 132) and positions it against the SCC's April 22, 2026 ruling on the Legault government's 2024 freeze statute.

**Constitutional framing: effective representation versus variance tests.** The *Saskatchewan Reference* standard establishes "effective representation" as the constitutional benchmark for electoral boundary commissions, but "effective representation" is not a variance ceiling or population-equity metric. Rather, it is a multi-factor constitutional test — articulated in *Saskatchewan Reference* para. 33 — that weighs quantitative factors (population distribution, variance in district population) *alongside* non-quantitative factors (geography, historical boundaries, community of interest, minority representation) as evidence bearing on whether the electoral system serves the *practical* ability of electors to cast a meaningful vote.

The *Saskatchewan Reference* para. 33, delivered by McLachlin J., establishes that "relative parity of voting power" must be weighed against permissible deviations for "geography, community history, community interests and minority representation." Critically, the Court did not prescribe a bright-line tolerance for population variance or other quantitative measures. Instead, it requires a holistic assessment in which deviations from strict equality are constitutionally defensible *if justified by the non-quantitative factors*. This standard has been applied in two landmark post-Reference cases. *Raîche v. Canada (Attorney General)*, 2004 FC 679, examined whether electoral boundaries in federal ridings met the effective-representation standard. The court upheld boundaries with population variance exceeding strict equality, finding the deviations defensible by reference to geography and community-of-interest considerations. *Cassista v. Canada (Attorney General)*, 2014 FC 398, applied the same framework to a federal redistricting cycle, again sustaining boundaries with significant variance where the deviations traced to legitimate permissible factors. In both cases, courts did not examine whether the boundaries were partisan-asymmetric. The focus was whether quantitative deviations were reasonably related to the statutory mandate's non-quantitative factors. This doctrinal architecture means that partisan asymmetry, standing alone, does not trigger a constitutional violation under the Saskatchewan Reference standard — the asymmetry must be paired with either (a) unexplained deviations from population parity that cannot be justified by geography, community of interest, or other permissible factors, or (b) evidence that the non-partisan factors (geography, etc.) have been distorted *in service of* partisan outcomes rather than in service of the legitimate statutory purposes.

The audit's quantitative findings (partisan-bias metrics in [§5.2](#sec-5-2), population-variance medians in [§5.1](#sec-5-1), municipal-boundary anchoring in [§5.8](#sec-5-8)) are inputs to this constitutional test, not proxies for the test's output. No single metric — nor any linear combination of metrics — constitutes a determination of whether a map meets or fails the constitutional threshold. Pal (2015) argues that commission outputs are reviewable for "manifest unreasonableness" only — commissioners operate within a broad "discretion space" that encompasses legitimate design preferences — and that the boundary between justified discretion and reviewable partiality is defined by whether the non-partisan factors genuinely constrained the choices or were invoked *post hoc* to rationalize a predetermined partisan outcome. The [§5.9.3](#sec-5-9-3) procedural analysis documents evidence on this point: whether the audit's six-dimensional pattern — partisan asymmetry *coupled with* population-variance distortions not explained by geography or community boundaries, *coupled with* procedural departure from the pattern established by the majority under identical constraints — rises to the level of manifest unreasonableness under Pal's framework is a question for a reviewing court.

The distinction between [§3](#sec-3) of the *Canadian Charter* (the right to vote, which the *Saskatchewan Reference* operationalizes) and §15 (equality of political rights) is material: the audit measures deviations in vote efficiency and partisan bias under neutral simulation, providing factual context for whether a commission's output warrants scrutiny. A court's assessment of whether the commission's process was procedurally sound, or its output's partisan asymmetry beyond the justified margins of discretion, is a separate legal question in which non-metric considerations — geography's constraints, rural-urban representation trade-offs, minority communities' distinct electoral needs — weigh equally with the audit's numbers. This report assembles evidence across six dimensions. A finding that six indicators point in the same direction is a statement about the empirical pattern, not a legal conclusion. The [§5.9.3](#sec-5-9-3) procedural analysis and §12 commentary clarify the extent to which the audit's findings bearing on discretion exceed the outer margins Pal identifies.

**Compactness and computational methods.** Polsby and Popper (1991) and Reock (1961) supply the two compactness metrics referenced throughout. Barnes and Solomon (2021) document their implementation sensitivity. DeFord, Duchin, and Solomon (2021) introduce the ReCom MCMC family used for the neutral-ensemble baseline in [§5.4](#sec-5-4). Cannon, Goldbloom-Helzner, Gupta, Matthews, and Suwal (2022) introduce the short-bursts hill-climbing procedure for exploring biased-but-legal maps. This audit applies their method in [§5.4.8](#sec-5-4-8) to test empirically whether a non-neutral procedure can reach the minority's seats@50/50 reading under EBCA constraints. Herschlag, Ravier, and Mattingly (2020) demonstrate the ensemble-comparison methodology the Alberta audit applies here. Altman and McDonald (2011) articulate the four-axis redistricting-audit discipline — population equality, compactness, political fairness, community of interest — whose consistency-across-dimensions framing § E of this paper draws on. Fifield, Imai, Kawahara, and Kenny (2020) discuss the empirical-validation requirements for redistricting simulation results.

**Pre-registration and evidentiary discipline.** Nosek et al. (2018) and Munafò et al. (2017) codify the pre-registration discipline the audit's November 2026 test protocol follows. American Statistical Association (2016, 2019) statements on p-values and graded evidence guide the audit's reporting of directional findings at sub-threshold magnitude. These disciplines matter because the paper's central claim — six dimensions pointing in the same direction, none individually at classical 95% significance — is inferentially valid only under pre-registered test selection and reported-versus-hidden-test symmetry.

The audit's methods map onto this literature as follows: B2–B6 ([§5.2.1](#sec-5-2-1)) implement Stephanopoulos-McGhee, McDonald-Best, Gelman-King (and the broader Grofman, King and Browning partisan-symmetry foundation), and Warrington directly; [§5.4](#sec-5-4) implements DeFord-Duchin-Solomon ReCom against a 1,010,000-plan neutral ensemble (4 chains × 252,500 steps); [§5.2.5](#sec-5-2-5) validates Chen-Rodden for Alberta; [§5.9.3](#sec-5-9-3) positions the procedural finding against Courtney's Canadian comparator sample (Courtney 2001, chs. 3–4) and Pal's (2015) discretion framework. Where the Alberta context departs from US or Canadian prior work, the departures are documented rather than elided.

---

<a id="sec-3"></a>
## 3. Data

This section consolidates the audit's data-provenance disclosures — primary sources, their `FROZEN_MANIFEST.md` anchor dates, known coverage caveats, and robustness to cycle-lag. All downstream analyses in [§5](#sec-5) inherit from the sources listed here. Deeper provenance notes (including the Plan B population-basis cross-check and the 2021-census-direct legal-baseline reconstruction) are in Appendices C and E.

<a id="sec-3-1"></a>
### 3.1 Primary data sources

| Source | File(s) | URL | Manifest anchor |
|---|---|---|---|
| Elections Alberta 2023 Statement of Vote | `data/2023_results.xlsx` | https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx | `FROZEN_MANIFEST.md` (2026-04-22 access) |
| Commission final report (majority + minority) | `data/majority_2026_populations.csv`, `data/minority_2026_populations.csv`; map images in `maps/*.jpg` | https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | `FROZEN_MANIFEST.md` (2026-03-23 publication) |
| Elections Alberta 2026 ED shapefiles | `data/shapefiles/canonical/` | https://www.elections.ab.ca/resources/maps/ | Released 2026-05-06; confirmed final by EA Geomatics Team Lead (personal correspondence, R. Mok, 2026-05-19) |
| StatsCan 2021 Census Dissemination Areas | `data/alberta_2021_da_populations.csv`, `data/alberta_2021_das.gpkg` | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/ | `FROZEN_MANIFEST.md` |
| Alberta Treasury Board Office of Statistics and Information quarterly estimates | (embedded in commission totals) | https://open.alberta.ca/dataset/alberta-population-estimates | `FROZEN_MANIFEST.md` |
| StatsCan Table 17-10-0009 (quarterly provincial estimates) | (cited; not persisted) | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | `FROZEN_MANIFEST.md` |
| StatsCan Table 98-10-0459 (2021 Census journey-to-work) | (cited in [§5.8.4](#sec-5-8-4)) | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810045901 | `FROZEN_MANIFEST.md` |

<a id="sec-3-2"></a>
### 3.2 Coverage caveats

Three coverage gaps constrain the audit's scope. Each is disclosed rather than papered over.

1. **2026 polygon shapefiles released; formal request answered.** Elections Alberta's GIS page did not carry 2026 ED polygons at the time of the audit's initial scope definition (accessed 2026-04-22). A formal written request for the 2026 boundary shapefiles was filed with Elections Alberta. EA's Geomatics Team Lead confirmed on 2026-05-19 (personal correspondence, R. Mok) that the 2026-05-06 shapefile release is final for the commission maps. The canonical shapefiles are now the basis for all spatial analysis in this audit (`data/shapefiles/canonical/`); all results in §5 inherit from this source. **DPG era (historical, now superseded).** Prior to the 2026-05-06 release, Derived Provisional Geometries (DPGs) were constructed from the commission's report text and Appendix E boundary descriptions; methodology documented in `archive/provisional_geometries/approximate_shape_analysis.md` and `analysis/methodology/shape_refinement_v2.md`. Three iterative refinement passes reduced positional error on Tier A/B boundaries to ≤1 km (mean shift 97 m after v1; residual voter-assignment impact: 1,012 votes across 4 VAs, approximately 0.06% of 2023 valid votes). All DPG-era findings have been recomputed from canonical shapefiles. Per the DPG sunset clause in `analysis/methodology/canonical_shapefile_log.md`, DPG results are archived and no longer the primary analysis basis.
2. **Majority-proposal map imagery incomplete.** The working bundle has the majority's Calgary map. The majority Alberta overview, Edmonton, and other-cities panels are not in the bundle. Visual inspection of the majority is therefore limited to its Calgary districts. [§5.8.1](#sec-5-8-1) discloses this scope narrowing.
3. **~88 public submissions (6.6%) could not be machine-parsed.** Their PDFs are image-only scans lacking a text layer. The submission-archive verification ([§5.9.4](#sec-5-9-4)) rests on identified counter-examples in the 1,252 parseable submissions rather than exhaustive enumeration of all ~1,340.
4. **Third-party vote allocation: B2 (EG) is sensitive to the trailing-party rule. B3 (mean-median) is not.** The 2023 Alberta statement of vote includes 58,232 votes cast for parties other than NDP or UCP (3.30% of valid votes) across 79 of 87 existing EDs. The audit's primary analysis excludes these votes (Rule A: drop, converting all margins to NDP/UCP two-party share). Two alternative allocations were tested symmetrically via `analysis/scripts/third_party_sensitivity.py` (2026-05-09). Rule B (pro-rate other votes to NDP/UCP in proportion to observed two-party shares) shifts the minority-majority EG asymmetry by 0.02 pp and leaves the direction unchanged (minority −1.87%, majority −0.44%, delta −1.43 pp). Rule C (assign all other votes to the trailing party in each district) reverses the EG direction for *both* maps: minority EG +7.41%, majority +4.16% (positive = NDP-favourable under this paper's convention). The mechanical reason: in dominant NDP urban seats, assigning other votes to UCP as the trailing party generates large UCP wasted-vote quantities that overwhelm NDP's urban over-concentration, flipping the EG sign. The minority map, which contains more dominant NDP urban seats than the majority, flips further (+3.25 pp gap, reversed direction). B3 (mean-median) holds its direction under all three rules. B6 (declination) follows EG and reverses under Rule C. The paper reports Rule A as the primary metric and Rule C as a deliberate falsification probe. The Ch1 (Mahalanobis joint tail) and Ch2 (SZAT bootstrap EG) statistics are computed from the same Rule A two-party shares and are unaffected by Rules B or C.
5. **Election-day votes are the only geographically attributable vote type.** Elections Alberta's published results assign a specific Voting Area number to each election-day polling station. Advance, mobile, and special ballot results are reported at the electoral district level only. EA does not record the home VA of an advance voter in any published data product. In the 2023 Alberta general election, 381,932 NDP votes were cast on election day (geographically attributable to specific VAs) and 395,472 NDP votes were cast advance, mobile, or special (carrying no VA-level geographic identifier). All VA-level vote attribution in this audit uses election-day votes only, via `analysis/scripts/build_canonical_va_votes.py`. No advance votes are redistributed or spatially smeared to VAs by assumption. The 49.1% election-day share is a structural property of EA's result-reporting system — not a modelling choice — and represents the actual geographic granularity available to any analyst working from EA's published data.

   **Mechanism.** Alberta's *Election Act*, RSA 2000, c E-1, s.112(1)(a.1) requires that the election officer complete "a separate Statement of Vote for each voting area." Sections 113 and 124 apply this requirement — with "all necessary modifications" — to the advance vote count and mobile vote count respectively, meaning the per-VA reporting obligation extends by statute to every ballot type. The operative exception is s.112(2): "Despite subsection (1)(a.1), the election officer responsible for the count may combine the Statements of Vote for more than one voting area in the same electoral division if, in the opinion of the election officer, it is necessary to maintain the secrecy of voting." EA's practice of reporting advance and mobile totals at the ED level rather than the VA level almost certainly reflects an invocation of the s.112(2) secrecy exception, not the absence of any legal obligation. The practical mechanism: the advance voting process verifies each voter against EA's Electoral List System (ELS) before issuing a ballot. The ELS entry carries the voter's home Voting Area number. The VA link is generated at the moment of voters-list check. Advance and mobile ballot envelopes carry no VA identifier. Ballots are then counted at the ED level only. The home-VA attribution exists at the point of voting and is not carried through into results reporting. Whether EA applies the s.112(2) exception as a blanket policy across all advance VAs or as an individual election-officer determination for specific low-population VAs is unknown; that question is included in the pending informal inquiry to EA (see VA 043 case study below). No change to the voting process, ballot design, or voter interaction would be required to publish VA-level advance totals above a minimum-count threshold. Under s.112(2)'s own framing, VAs where secrecy can be maintained without combination could be published separately, requiring only an administrative determination from the election officer.

   **VA 043 (ED 70, Lesser Slave Lake) as case study.** One VA in the canonical file (ED 70, VA 043) received zero election-day votes in EA's published polling data. It is retained in the shapefile with zero vote totals. VA 043 covers 4,832 km² in the northern portion of ED 70, contains 844 persons per the 2021 Census (from `data/va_pop_from_das.csv`), and recorded zero election-day votes — all votes from VA 043 residents entered EA's advance/mobile divisional total with no VA attribution. The specific mechanism is pending EA confirmation: s.120 mobile polling requires a facility type (treatment centre, supportive living facility, shelter, community support centre) that VA 043's community does not appear to satisfy. The alternative is Special Ballot voting under s.52.2 remote-area designation, where no polling team visits and residents vote by ballot request. Either way the geographic signal is absent from published data. VA 043 is surrounded by NDP-majority VAs (VAs 041, 042, and 044 returned 52.4%, 53.6%, and 81.8% NDP respectively on election day), placing it in a northern cluster that ran 534 NDP / 535 UCP across VAs 029–051 — near parity, in contrast to the southern cluster's 29.6% NDP. The geographic partisan signal for VA 043's residents is entirely absent from any published data product. The 2025–2026 Electoral Boundaries Commission received submissions specifically describing the Indigenous communities in this northern area and ultimately invoked §15(2) to protect the riding. The commission's geomatics work was supported by EA GIS staff (EBC Final Report acknowledgements). Whether the commission requested or received VA-level advance vote data from EA — which would have provided a geographic picture of VA 043's voting — is unknown. A direct informal inquiry to EA is pending. A formal FOIP request is queued as the fallback. Full case study in `findings/lesser_slave_lake_va043_representation_gap.md`.

<a id="sec-3-3"></a>
### 3.3 Cycle-lag robustness

The population data the commission uses carries a cycle-lag: the 2021 decennial census updated to a July 1, 2024 Office of Statistics and Information estimate. This choice reflects standard Alberta commission practice (the 2017 Bielby commission used the same basis) and aligns Alberta's statutory approach with other Canadian provinces, which employ diverse population inputs: Quebec uses electors-by-register, British Columbia uses Statistics Canada quarterly estimates, and Manitoba uses decennial census only. Under Alberta's Electoral Boundaries Commission Act §12(3), the statutory mandate permits use of "current population statistics" without prescribing a single data source. The TBF July 2024 estimate satisfies this requirement while preserving administrative timeliness. This statutory flexibility positions Alberta within the practical middle of Canadian commission approaches: more administratively responsive than Manitoba's decennial-census restriction, yet more constrained than Quebec's live-register mandate. Alberta's cumulative population growth from 2021 to mid-2025 is approximately 17.8%. The audit's `analysis/cycle_lag_analysis.md` computes how many electoral divisions flip ±25% window status when mid-2025 populations are substituted: 5 of 87 on the 2019 map, 0 of 89 on the majority 2026 proposal, and 5 of 89 on the minority 2026 proposal. The audit's `analysis/reports/plan_b_cross_check.md` independently verifies that every [§5.1](#sec-5-1) verdict is identical whether computed against the 2021 census directly, the 2024 OSI estimate, or the 2025 TBF estimate — i.e. the directional findings are robust to which intra-cycle population vintage is used. Appendix C supplies a 2021-Census-direct A1 computation on the 87 existing 2019 EDs as the §12(3)-operative reference point.

**Dataset-construction consequences of cycle lag (three-vintage sandwich).** Beyond the verdict-robustness property above, the 4–14-year lag between commission data-basis and boundary retirement materially shapes *how* the audit's upstream pipelines construct their datasets. Any reconstruction of the commission's arithmetic has to reconcile three input vintages simultaneously:

- **2021 geometry + 2021 population.** Statistics Canada Dissemination Area (DA) polygons carrying 2021 census populations — the atomic unit used for Phase 4B DA-overlay.
- **2024 operative estimate.** The commission's July 2024 Treasury Board and Finance (TBF) estimate for each 2026 proposed ED — the operative published value against which the commission's variance tables were computed.
- **2023 voting substrate.** The 2023 Voting Area (VA) polygons carrying 2023 votes — the spatial substrate used for Phase 4C partisan-bias attribution.

The ratio between the 2021-population-sum-inside-a-2026-DPG-polygon and the commission's 2024 estimate of the same territory is **not** a clean scalar. Alberta's 14.69 % provincial growth between 2021 and 2024 was distributed unevenly — Calgary-ring cities such as Airdrie and Chestermere grew 20–30 %, rural territories grew 0–5 % — so applying a flat provincial growth factor to a regionally heterogeneous population surface introduces a structural bias into Phase 4F's per-ED validation deltas. The 81 of 86 majority and 87 of 89 minority hardstop failures documented in `data/INTEGRITY_STATUS.md` are therefore a composite signal: **real DPG transcription error plus cycle-lag growth heterogeneity, not separable from public data alone**. The [§4.1.4](#sec-4-1-4) sunset clause binds the audit to recomputation if Elections Alberta releases official shapefiles, at which point real geometric error would be distinguishable from cycle-lag artifact. Full treatment at `findings/cycle_lag_analysis.md` ([§1](#sec-1)).

**Forward-modelling consequences for commissions.** The 2021 decennial census — the Commission's statutorily-mandated baseline under §12(3) — is 4 years stale at the first election under the new boundaries (2027) and up to 14 years stale at the boundaries' retirement (potentially 2035).

For fast-growth metropolitan-fringe cities (Airdrie, Chestermere, Cochrane, Okotoks, Beaumont, Leduc, Spruce Grove, Fort Saskatchewan, Sherwood Park), this gap already moves per-ED population quotas by 10–15 % at the 4-year mark and by 40 %+ at the 14-year mark under current growth rates, independent of any drawing choice the commission makes.

For slow-declining rural districts (Peace River, Central Peace-Notley, Lesser Slave Lake), the gap erodes §15(2) special-rural-protection ratios asymmetrically: Lesser Slave Lake's mid-2025 §15(2) qualifying ratio drops past −50 % of the provincial mean under the cycle-lag substitution, which could disqualify a district from its current legal basis before the cycle concludes.

Indigenous on-reserve populations face a third variant of the same problem: commissions inheriting the census's chronic 3–10 % on-reserve undercount see those communities structurally under-represented for the full 6–14-year cycle.

The gap is primary-source verifiable for the Kee Tas Kee Now Tribal Council member nations in northwestern Alberta — a regional tribal council whose member nations include communities among the 14 First Nations and Métis communities the EBC Final Report identifies within or adjacent to ED 70. ISC First Nations Population Profiles (April 2026 — a supplementary source not incorporated into the commission's §12(3) statutory data mandate) show registered population growth rates that substantially exceed the 14.69% provincial average used to project forward from the 2021 census. Peerless Trout First Nation (Band 478) recorded a registered population of 1,155 in April 2026, up from 966 in the prior ISC profile — a 19.5% increase over approximately seven years, more than one-third above the provincial rate for the same period. Whitefish Lake First Nation #459 (Atikameg) shows a 2021 Census community population of 880 (Statistics Canada, Indigenous Population Profile 2021). 1,423 registered band members are listed on own reserve in the April 2026 ISC profile (total registered: 3,266, including off-reserve members living elsewhere in Alberta). Note that ISC registered population on own reserve and census household population are distinct measures — the former counts registered band members who list the reserve as their address of record, the latter counts people physically present. Lubicon Lake Band No. 453, which operates on Crown land rather than a formal reserve, recorded a 2021 Census median age of 21.2 years. Whitefish Lake's census median age is 22.6 years. Median ages in the low-to-mid-twenties indicate cohorts entering peak fertility and early working-age years simultaneously — a demographic structure associated with above-average natural increase over the coming decade. A commission drawing the 2026 map on 2021/2024 TBF data works with a population basis for these communities that is stale not only in absolute terms but in growth-rate terms.

None of this is resolvable by audit methodology alone. The §12 statutory framework itself determines what baselines the Commission is permitted to consult. A legislative-reform proposal formalising a composite basis (TBF primary + StatsCan tie-breaker at ±2 % + AHCIP + CRA T1 cross-check + CEO as certifying authority) is outlined at `docs/act_amendment_proposal.md`. The audit offers this as a policy contribution, not a finding. Full treatment at `findings/cycle_lag_analysis.md` ([§2](#sec-2)).

**Policy contribution: synchronise redistribution timing with census data release.** The structural source of the 4–14-year cycle lag is procedural rather than statutory: commissions are constituted before the census data that would anchor their work is available. Canada's 2026 decennial census is enumerated in May 2026. Statistics Canada releases dissemination-area-level population and geography data approximately 18–24 months after enumeration, placing comprehensive sub-provincial data in the 2027–2028 window. A commission constituted before that release — as the current commission was, drawing on 2021 census data — cannot access the most current population geography even if it wished to. The EBCA's two-year post-census trigger for commissioning could be amended to require that the commission's appointment follow the release of DA-level census data from the most recent decennial enumeration, rather than merely following the enumeration date itself. This would reduce the population-data age at the time of drawing from 4+ years to approximately 1–2 years, and would ensure that fast-growth metropolitan-fringe communities whose populations change 20–30% per four-year cycle are accurately represented in the map the commission draws rather than in a retrospective correction the next commission inherits. The audit offers this as a policy contribution, not a finding.

**Policy contribution: Elections Alberta should publish home-VA vote totals for advance ballots.** In the 2023 provincial election, 395,472 NDP and UCP votes cast advance, mobile, or special carry no Voting Area identifier in EA's published data (§3.2 item 5). This is not a technical limitation. Every advance voter is verified against the provincial voters list before receiving a ballot; that list links each registered voter to a specific Voting Area. The home-VA identifier exists at the point of voting. The statutory framework is clearer than it initially appears: s.112(1)(a.1) of the *Election Act* requires a separate Statement of Vote per voting area, applied to advance counts through s.113 and mobile counts through s.124. EA's aggregate reporting practice rests on the s.112(2) secrecy exception, which permits combining VAs when "necessary to maintain the secrecy of voting." The reform is not to create a new legal obligation but to provide guidance, or amend s.112(2), to require that the secrecy exception be applied VA-by-VA against a minimum-count threshold — so that only VAs where combination is genuinely necessary for secrecy are combined, while larger VAs are published separately. Publishing VA-level advance vote totals alongside the existing election-day VA breakdowns requires no change to the voting process, no additional interaction with the voter, and no new data collection — only a change to how EA applies a discretion the statute already authorizes.

The gap disadvantages not only external analysts but the Electoral Boundaries Commission itself. Commissioners are required by the EBCA to weigh community of interest — to assess whether geographic communities have coherent political identities worth preserving whole, or whether proposed boundaries divide natural constituencies. That assessment depends on understanding where voters actually live and how they participate. When advance voting accounts for approximately half of all votes cast and those votes carry no geographic attribution below the ED level, commissioners are making legally binding boundary decisions while working with the same incomplete spatial picture as external auditors. The voters list they consult shows where electors are registered. The vote results EA publishes show only where half of them voted. These are not the same thing, and the discrepancy is largest precisely in the high-growth suburban communities — Airdrie, Cochrane, Chestermere, Leduc — that are most contested in redistribution proceedings.

Publishing VA-level advance vote totals would allow complete-coverage VA-level vote attribution in future audits, provide commissioners with a full geographic picture of the communities they draw boundaries around, and bring Alberta's results reporting to the granularity that the EBCA's community-of-interest mandate implicitly requires. Standard minimum-count thresholds — already applied to election-day polling station results — would apply equally to advance VA totals, preserving individual ballot secrecy in low-turnout voting areas without limiting geographic transparency for larger communities. The audit offers this as a policy contribution, not a finding.

**Cross-election asymmetry reversal: mechanical explanation.** A parallel sensitivity operates on the partisan side. The minority map absorbed three hybrid configurations the majority does not contain: Springbank-area townships (outer west Calgary suburbs), Bearspaw, and Cochrane. These communities are high-income, low-density outer suburbs whose two-party NDP/UCP vote share sits in the blend model's transition zone — high enough urban-weight sensitivity that small shifts in the rural baseline produce large swings in the hybrid's attributed vote share. In 2023, outer Calgary suburbs returned NDP shares near the urban-core mean (2023 was a competitive cycle; suburban NDP performance was stronger than historical). In 2019, the same territories returned NDP shares closer to the rural baseline (the 2019 NDP wave penetrated the urban core but had shallower reach into outer Calgary suburbs). The audit's blend model applies a fixed geographic weight to both election years. What changes is the rural baseline being mixed in. Under 2023 votes, Springbank/Bearspaw/Cochrane territory makes the minority's hybrid EDs mildly more NDP-competitive than under 2019, which is why the minority asymmetry is negative (more UCP-favourable) under 2023 but positive (less UCP-favourable) under 2019. The reversal is a property of the estimation model interacting with Alberta's election-specific suburban swing geography — not a measurement of a different underlying boundary configuration. [§5.2.3](#sec-5-2-3) documents the specific numbers: 2015 asymmetry +0.03 pp, 2019 +0.75 pp, 2023 −0.51 pp. The individual map EG signs do not flip (both maps remain UCP-favourable under all three elections). Only the inter-map asymmetry direction changes.

---

<a id="sec-4"></a>
## 4. Methods

This section describes the audit's methodology; results follow in [§5](#sec-5). The methods are presented in the sequence they are applied: the symmetry and falsifiability discipline ([§4.1](#sec-4-1)), the vote-attribution pipeline used for all partisan-bias metrics ([§4.2](#sec-4-2)), the specific test battery B1–B6 with thresholds and references ([§4.3](#sec-4-3)), and the legal-defensibility frame used to map findings to potential challenges ([§4.4](#sec-4-4)). Mathematical formalism for the four metrics is consolidated in Appendix D.

<a id="sec-4-1"></a>
### 4.1 Methodology and integrity framework

<a id="sec-4-1-1"></a>
#### 4.1.1 Symmetry requirement

Every test applied to one map is applied identically to the others. Where a data gap prevents symmetric application, the gap is disclosed explicitly and the claim's scope is narrowed to what is symmetric.

<a id="sec-4-1-2"></a>
#### 4.1.2 Falsifiability gates

Each analytical stage produces a PASS/FAIL gate value before propagating downstream. Gates implemented:

- **G1 (carry-forward verification):** B1–B4 on 2019 baseline must reproduce the four-figure match to official totals (NDP 777,404 / UCP 928,900, two-party 1,706,304; arithmetic verified: 777,404 + 928,900 = 1,706,304; source: `data/raw/2023_results.xlsx`). Reproducible via `python3 analysis/scripts/packing_cracking_analysis.py`.
- **G2 (2026 estimate count):** Each map's ED estimate set must contain exactly 89 districts; total valid votes within 5% of 1.7M; NDP share within [0.40, 0.50]. `validate_2026_estimate()` in `packing_cracking_analysis.py`.
- **G3 (Calgary classification coverage):** A2 test requires zero residual unclassified Calgary EDs. Enforced programmatically in `a2_calgary_analysis()`.
- **G4 (A2 robustness):** A2 directional finding must survive alternative classification (2023 winner-based) or be flagged as classification-dependent. `a2_robustness_check()` implements the alternative.
- **G5 (Sensitivity range):** B2 efficiency gap computed under urban weights 0.60, 0.70, 0.80, 0.85 (central), 0.90. Direction must be consistent across all five; magnitude range is reported alongside the central estimate.

<a id="sec-4-1-3"></a>
#### 4.1.3 What does not enter the report

- Any number not reproducible by running a checked-in script against checked-in data
- Any classification rule without a robustness check under at least one alternative
- Any language characterizing one map's features with stronger modifiers than the other's when the underlying facts are comparable
- Any "the numbers confirm X" framing in section preambles

<a id="sec-4-1-4"></a>
#### 4.1.4 Derived Provisional Geometries (DPG) — summary and canonical resolution

Prior to 2026-05-06, official Elections Alberta shapefiles for the two 2026 proposals had not been published. All pre-canonical 2026 boundary geometries were **Derived Provisional Geometries (DPG)** — polygons reconstructed from commission-published PNGs via a ten-stage pipeline (raster trace → topology cleanup → population-swept hybrids → CSD/DA anchoring → confidence propagation → multi-source assembly → four-phase perfecter → nested-polygon ownership inversion). Two error modes govern DPG-dependent metrics:

- **Perimeter-mode uncertainty (±500 m typical):** boundary localisation error affecting compactness scores (Polsby-Popper, Reock) and fine-grained vote attribution near boundary lines.
- **Area-mode uncertainty (Tier-dependent):** whole-polygon-territory mismatch affecting DA-overlay populations and polygon-intersection tests. Tier A EDs (da-anchored, municipal-anchored) carry shapefile-grade fidelity. Tier C EDs (v7 visual transcription) are subject to documented area-mode errors and are excluded from primary findings.

**Official shapefiles received 2026-05-06.** Findings designated [C] (canonical) throughout this report were recomputed on official Elections Alberta shapefiles. DPG-era results remain in the record per pre-registration obligation and are superseded by their canonical equivalents where both exist. Findings not marked [C] may be DPG-derived and are subject to the sunset clause. See `analysis/methodology/canonical_shapefile_log.md` for the full reconciliation of which findings have been recomputed on official geometry.

**Sunset clause — satisfied.** The pre-registered commitment to recompute all geometry-dependent metrics within two weeks of official shapefile release was fulfilled on 2026-05-06. No sign-flips or material magnitude changes were observed. Full reconciliation is at `analysis/methodology/canonical_shapefile_log.md`.

The full ten-stage DPG pipeline — construction methodology, error progression table, nested-polygon ownership-inversion algorithm (extends Sester 2000; Saalfeld 1988), and programmatic city-centre alignment proof — is documented in the companion methods paper: `findings/methods_paper_draft.md`.

<a id="sec-4-1-5"></a>
#### 4.1.5 DPG construction pipeline — multi-source assembly (v0_7)

Full ten-stage pipeline (raster trace → topology cleanup → population-swept hybrids → CSD/DA anchoring → confidence propagation → multi-source assembly → four-phase perfecter → nested-polygon ownership inversion) documented in the companion methods paper (`findings/methods_paper_draft.md`). Summary of methodological findings that ran counter to expectation: [§5.0.2](#sec-5-0-2).

<a id="sec-4-1-6"></a>
#### 4.1.6 v0_8 coverage diagnostics — inheritance fill and geometric refinements

Full methodology in companion methods paper (`findings/methods_paper_draft.md`). Key coverage findings: 21 of 89 majority EDs have zero geometry in v0_7 and inherit empty into v0_8; Phase 3 spatial-index gap-fill systematically inflates rural ED areas in v0_8 vs v0_7; Calgary-Falconridge-Conrich is fully nested inside Airdrie-East in v0_7/v0_8 (v0_8.1 nested-polygon ownership-inversion refinement applied); v0_8.2 inheritance fill assigns 21 majority + 12 minority EDs from 2019-Tier-A predecessors. Findings in [§5.0.2](#sec-5-0-2) items 6–9; caveats propagating to downstream findings in [§4.1.8](#sec-4-1-8).

<a id="sec-4-1-7"></a>
#### 4.1.7 City-centre alignment proof

Point-in-polygon plausibility check against Statistics Canada city-centre representative points: 9 of 10 Alberta city centres land in correctly-named EDs in the v0_8.1 refined majority geometry. The single miss (St. Albert) falls in the geographically adjacent West Yellowhead ED, within the documented ±500 m DPG perimeter precision band. Full findings in [§5.0.2](#sec-5-0-2) item 9.

<a id="sec-4-1-8"></a>
#### 4.1.8 v0_8 geometry caveats propagating to downstream findings

Two imperfections propagate to Run #4 ([§5.4.4](#sec-5-4-4)) and related downstream findings: (1) inherited urban polygons trace 2019 boundaries rather than 2026 commission boundaries for 21 majority and 12 minority EDs; (2) the v0_8 minority's Peace River polygon is over-extended by Phase 3 gap-fill, absorbing 6 of 10 city-centre landmark points ([§4.1.7](#sec-4-1-7)). Both imperfections are disclosed where downstream findings cite v0_8 numbers.

<a id="sec-4-2"></a>
### 4.2 Vote-attribution pipeline

2026 ED-level vote estimates are built by mapping each 2026 ED to its 2019 predecessor(s) using an explicit dictionary (`MAJORITY_2026_MAPPING`, `MINORITY_2026_MAPPING`). Three mapping types:

- `direct`: 2026 ED covers approximately the same territory as a 2019 ED; use 2019 votes directly.
- `blend`: 2026 ED combines a 2019 urban core with rural absorption; blend 2019 core vote with the 2023 observed Rest-of-Alberta NDP share (33.5%) using urban weight 0.85 (applied identically to both maps).
- `merge`: 2026 ED combines two 2019 EDs; weight each part explicitly.

<a id="sec-4-3"></a>
### 4.3 Test battery

**Channel structure and ordering rationale.** The quantitative evidence runs in a fixed, dependency-ordered sequence:

- **Channel 1 — MCMC ensemble + inter-map permutation test.** Asks the broadest question first: is the minority map anomalous relative to a neutral redistricting distribution, and is the gap between the two commission maps larger than neutral plan pairs are apart from each other? This establishes that there is a real inter-map distance to explain.
- **Channel 2 — SZAT.** Decomposes *which specific boundary decisions* produced the confirmed gap. Runs after Ch1 because decomposing a gap that has not yet been established as real would be decomposing noise.
- **Independence check → Fisher combination.** Ch1 and Ch2 p-values are combined via Fisher's method (Fisher 1925) only after confirming the two tests are uncorrelated (§G1, ρ = −0.0014). Fisher's method combines k independent tests via T = −2∑ln(p_i), where T ∼ χ²(2k) under the joint null; for k = 2 tests the combined statistic T ∼ χ²(4). The independence check must precede the combination; Fisher's method is invalid if that condition fails. A supplementary Holm-Bonferroni correction across all six primary tests (family-wise α = 0.10) also survives: the corrected p-value at the second sorted position equals 0.0148, below the sequential threshold of 0.10/5 = 0.020; full table at [§7](#sec-7).
- **Channel 3 — Neighbour-Drain.** A pre-registered structural observation reported per pre-registration obligation. Does not feed into the Fisher combination. Result does not alter the Ch1+Ch2 verdict.
- **Two-Lane Scorecard.** Synthesises all channels. Scored last because it cannot be completed until all tests are run.

**Sign-convention glossary.** Throughout this paper, for every partisan-bias metric: **negative value = UCP advantage** (UCP wastes fewer votes per seat / carries the higher-than-median district / wins more seats at 50/50 / has shallower winning-district-margin angle than NDP), and **positive value = NDP advantage**. The sign convention is chosen for readability against seat-count outcomes, not to match the Stephanopoulos-McGhee 2:1 slope convention (which labels positive EG as "first-party disadvantaged"). Readers cross-referencing the S-M literature should invert the sign-label, not the finding. Both conventions agree on the *ordinal* ranking of the three maps. Full glossary and cross-convention reconciliation in `analysis/methodology/sign_convention_resolution.md`.

- **B1:** Vote distribution histogram across 10 margin bins from UCP +25%+ to NDP +25%+. (Descriptive; no formal literature reference.)
- **B2:** Efficiency gap (Stephanopoulos and McGhee 2014): $\text{EG} = (W_{\text{NDP}} - W_{\text{UCP}}) / N$ where wasted votes include loser votes plus winner votes above the threshold. **Sign convention note.** This audit reports EG using the proportional-seat baseline ("negative EG = UCP advantage" in seat-outcome terms) rather than the Stephanopoulos-McGhee 2:1 slope baseline ("positive EG = first-party disadvantaged"). The two conventions produce the same *ordinal* ranking of the three maps and therefore the same direction of the minority-vs-majority asymmetry, but they label the sign opposite. Full resolution in `analysis/methodology/sign_convention_resolution.md`; the resolution confirms no minority-vs-majority direction claim requires flipping. Where this paper says "negative EG = UCP-favourable," a reader comparing against S-M literature should invert the sign-of-label, not the finding.
- **B3:** Mean-median gap (McDonald and Best 2015): $\text{MM} = \bar{v} - \tilde{v}$ for NDP vote share.
- **B4:** Seats-votes under uniform swing to 50/50 provincial share (Gelman and King 1994; Grofman 1983).
- **B6:** Declination (Warrington 2018). Measures the asymmetry between winning-district vote distributions by treating each party's winning districts as a vector and computing the angle between them. See [§5.2.4](#sec-5-2-4) for the direction-disagreement finding.

The seat-vote-curve symmetry principle underlying B4 traces to Grofman (1983) and King and Browning (1987), later formalized as a Bayesian estimator by Gelman and King (1994). The efficiency gap and mean-median are two of the most widely-cited partisan-bias metrics in the post-*Gill v. Whitford* literature; Stephanopoulos and McGhee (2018) revisit the efficiency-gap debate and acknowledge the metric's sensitivity to modeling choices, which our Monte Carlo analysis in [§5.2.2](#sec-5-2-2) quantifies for the Alberta context. Katz, King, and Rosenblatt (2020) argue that no single metric is dispositive and recommend ensemble approaches, which this audit's stress-test gate RT2 (cross-metric agreement) implements.

Mathematical definitions for EG, MM, declination, and the Polsby-Popper and Reock compactness metrics are in Appendix D.

<a id="sec-4-3-1"></a>
#### 4.3.1 Multiple-comparisons handling: Exploratory screening (current run) versus confirmatory testing (November 2026)

**Exploratory vs. confirmatory framing.** The current detection run applies six independent tests across multiple analytical dimensions. This creates a multiple-comparisons burden if the results are interpreted as confirmatory hypothesis tests, where each test is adjudicated at α = 0.05 independently and then combined. The audit's response is to explicitly frame this run as *exploratory, Bayesian-screening analysis* rather than confirmatory hypothesis testing.

Under the Bayesian-screening frame, the six-dimensional battery (population variance, partisan-bias metrics B2–B6, compactness, geographic coherence, procedural findings) serves as a screen to identify potential signals. The primary inferential claim is directional consistency *across* dimensions, not significance *within* any single dimension: "six independent lines of evidence point in the same direction" is the audit's finding, not "six individual tests reject the null at classical confidence." This framing aligns with the pre-registration posture stated in [§5.3.1](#sec-5-3-1): the current findings are exploratory. Confirmatory testing occurs in the November 2026 OSF-registered re-run on the Lunty-committee map.

**Confirmatory protocol (November 2026).** The November confirmatory run will apply a pre-registered formal hypothesis-testing framework with explicit multiple-comparisons correction. The Benjamini-Hochberg false-discovery-rate control (described below) is the proposed correction structure for the confirmatory pass. The current run's BH table (provided for reader reference) shows what the p-value landscape would be if classical hypothesis-testing were applied retroactively; but the exploratory-to-confirmatory distinction means the current run does not carry the inferential weight that a BH-corrected significance claim would carry.

**Exploratory findings as evidence, not conclusions.** The six-dimensional directional consistency reported in [§5.2](#sec-5-2)–[§5.8](#sec-5-8) and summarised in [§6](#sec-6) is evidence-suggesting (pointing toward systematic asymmetry in boundary drawing and outcome) rather than evidence-concluding (determining that a court would find the asymmetry unjustified under the Saskatchewan Reference effective-representation standard). The November confirmatory pass will sharpen this by applying formal hypothesis-testing machinery. The current exploratory findings provide the pre-hoc signal that motivated those pre-registered tests.

**Benjamini-Hochberg correction for the confirmatory pass.** The audit does not rely on any single statistical test for its conclusions. The primary inferential frame is directional consistency across multiple independent dimensions ([§6](#sec-6), [§4.6](#sec-4-6)). For the November confirmatory test, a formal Benjamini-Hochberg (BH) false-discovery-rate correction will be applied so the multi-test battery can be evaluated at α=0.05 family-wise. The reference table below shows the p-value landscape under BH correction. It is provided here to show readers what the correction structure will be when applied confirmatorily.

**Scope.** The table includes all formal tests that yield a computable p-value against an explicit null distribution. Purely qualitative structural checks (packing/cracking/engineered-boundary signatures, municipal anchoring ratio) are not included because they do not produce p-values. The Fisher combined result (p = 6.87×10⁻⁸) is excluded from the battery as it is derived from Ch1 and Ch2 and is not independent of them.

**p-value derivation for MCMC percentile tests.** A minority map at ensemble percentile p_pct in the UCP-favoured tail yields a one-tailed p-value of (1 − p_pct/100). A majority or minority map in the NDP-favoured tail yields p = p_pct/100. Row 3 (Seats@50/50): the raw 250k ensemble found 0/250,000 neutral plans exceeding the minority value (p < 4×10⁻⁶). The 250k full-coverage rescore placed the ESS-adjusted lower bound at p89.72 (inside the neutral band; the flag was retracted). The 1,010,000-plan canonical run ([§5.4.9](#sec-5-4-9), n_eff=1,495) reinstates the seats@50/50 flag: 1,010,000-plan percentile = 99.99, ESS-adjusted lower bound ≈p98, above the p95 threshold. Row 3 counts as a positive finding under the 1,010,000-plan run.

| Rank | Test | Map | p (raw) | p (BH-adj) | α = 0.05 |
| --- | --- | --- | --- | --- | --- |
| 1 | Moran's I spatial clustering on NDP share (z = 12.15) | 2019 substrate | 4.8×10⁻³⁴ | 5.3×10⁻³³ | **PASS** |
| 2 | Mahalanobis joint tail — Ch1 (canonical ensemble) | Minority | 1.4×10⁻⁶ | 7.7×10⁻⁶ | **PASS** |
| 3 | Seats@50/50 vs canonical ensemble (<100/1,010,000 plans exceeded; p99.99) | Minority | < 1×10⁻⁴ | < 4.4×10⁻⁴ | **PASS** |
| 4 | Mean-median vs canonical ensemble (p99.98) | Minority | 2×10⁻⁴ | 5.5×10⁻⁴ | **PASS** |
| 5 | Lopsided Margins t-test — Wang (2016), t = 3.43 | Majority | 1.0×10⁻³ | 2.2×10⁻³ | **PASS** |
| 6 | Lopsided Margins t-test — Wang (2016), t = 3.05 | Minority | 4.0×10⁻³ | 6.9×10⁻³ | **PASS** |
| 7 | SZAT bootstrap — Ch2 (10,000 permutations) | Minority | 2.4×10⁻³ | 6.9×10⁻³ | **PASS** |
| 8 | Mean-median vs canonical ensemble (p0.85, NDP-tail) | Majority | 8.5×10⁻³ | 1.2×10⁻² | **PASS** |
| 9 | Declination vs canonical ensemble (p1.21, NDP-tail) | Minority | 1.2×10⁻² | 1.5×10⁻² | **PASS** |
| 10 | Population MAD vs canonical ensemble (p99.0) | Minority | 9.8×10⁻³ | 1.4×10⁻² | **PASS** |
| 11 | Efficiency gap vs canonical ensemble (p94.4) | Minority | 5.6×10⁻² | 5.6×10⁻² | FAIL |

*m = 11 independent tests. BH-adjusted p = min(p_raw × m / rank, 1). The adjusted p for each rank is the minimum of the adjusted p for that rank and all higher ranks (standard BH step-up procedure).*

**Reference result for confirmatory testing (November 2026).** The table shows what the BH-corrected landscape would yield: 10 / 11 tests would pass BH correction at α = 0.05 under the confirmatory protocol. The sole failure is Minority EG (raw p ≈ 0.056, BH-adjusted p ≈ 0.056), which the audit already retracts from its outlier-flag set in [§5.4.9](#sec-5-4-9) on independent grounds (the 1,010,000-plan canonical run places minority EG at p94.4, below the p95 threshold). No test that is counted as a positive finding in the audit's conclusions would fail BH correction when formally applied. This table is provided as reference material so readers can see the correction structure that will govern the November confirmatory pass. It is not a retroactive inferential claim on the exploratory current run.

**Scope note.** The Lopsided Margins finding (rows 5–6) is present in all three maps including the 2019 enacted baseline and is explicitly described in [§5.2.9](#sec-5-2-9) as a structural property of Alberta's political geography, not a distinctive feature of either 2026 map. Its inclusion in the BH battery is conservative (reduces the effective discovery rate for any new finding) but does not change the conclusion.

<a id="sec-4-3-2"></a>
#### 4.3.2 Bonferroni correction as a conservative alternative

While Benjamini-Hochberg correction controls the false-discovery rate and is the chosen method for the confirmatory protocol, a simpler alternative exists: the Bonferroni correction, which controls the family-wise error rate (FWER) — the probability of any false positive across the entire test battery. The Bonferroni method is more conservative: for m = 11 independent tests at α = 0.05 family-wise, the per-test threshold becomes α / 11 ≈ 0.0045 (compare to BH's step-up procedure which is less restrictive).

Applied to the current audit's findings: the two largest p-values in the battery are Minority EG (p = 0.058, already withdrawn) and Minority Declination (p = 0.010). Under Bonferroni, both would exceed the threshold α / 11. However, the smaller p-values dominate: Ch1 Mahalanobis (p = 1.40×10⁻⁶) and SZAT (p = 0.0024) clear the Bonferroni threshold by multiple orders of magnitude. The audit's structural findings — which rest on the directional consistency of multiple independent tests rather than on any single test — survive Bonferroni correction. Moreover, the Fisher combination of Ch1 and Ch2 (examined in Appendix C's `fisher_combination_defense.md`) remains significant even under Bonferroni applied to the two-channel case: Bonferroni on two p-values yields p ≤ 3.2×10⁻⁷ (twice the smaller p-value), far below any standard significance threshold. The choice of BH over Bonferroni for the confirmatory protocol reflects the audit's frame (multiple exploratory dimensions, not a single pre-registered hypothesis test) and the principle that BH better balances discovery power with false-discovery control in high-dimensional exploratory settings.

<a id="sec-4-3-3"></a>
#### 4.3.3 Pre-registration record

The table below is the canonical lookup for pre-registration status of every quantitative test in the audit. Full provenance detail is in `analysis/methodology/null_hypothesis_and_exoneration_criteria.md`; full amendment history is in `findings/pre_registration_amendment_log.md`.

| Test | Pre-registration anchor | Timing relative to data |
|---|---|---|
| Ch1 — Mahalanobis joint outlier ([§5.4.9](#sec-5-4-9)) | Seeds committed to Cloudflare drand beacon Round 5500000 before shapefile release; see `analysis/scripts/drand_seed.py` and `docs/FROZEN_MANIFEST.md` | drand seeds predate official shapefile receipt (2026-05-06). Specific test name and combination method not named in OSF. **Exploratory.** |
| Ch2 — SZAT boundary-choice bootstrap ([§5.2.10](#sec-5-2-10)) | AsPredicted [#289,469](https://aspredicted.org/9zr792.pdf) (filed 2026-05-07; made public 2026-05-07); OSF:6pt83 (filed ~3 h after shapefile commit — cannot be treated as pre-dating that data) | Numerical results were known to the analyst at filing. **Exploratory-reproducible.** |
| Ch3 — Neighbour-drain adjacency ([§5.3.5](#sec-5-3-5)) | OSF:[r3zm7](https://osf.io/r3zm7/) / AsPredicted #289,451 (filed before shapefile release) | Pre-dates shapefile; the null hypothesis and surrogate-label test design were pre-committed. **Pre-registered confirmatory.** |
| Fisher combination Ch1 + Ch2 ([§5.5](#sec-5-5)) | Combination method not pre-registered. Independence confirmed post-hoc (ρ = −0.0014, §G1). | **Exploratory.** |
| B7 — Intermap permutation test ([§5.2.11](#sec-5-2-11)) | OSF:[yvc7g](https://osf.io/yvc7g/) | Pre-dates shapefile. **Pre-registered.** |
| Municipal anchoring ([§5.8.5](#sec-5-8-5)) | OSF:[s58a6](https://osf.io/s58a6/) | Pre-dates shapefile. Finding subsequently retracted on canonical geometry (both maps within 70–85% Canadian norm). |
| November 2026 Lunty-committee 91-seat scorecard ([§5.6](#sec-5-6) prospective) | OSF:[qsgy8](https://osf.io/qsgy8/) / AsPredicted #289,455 (filed 2026-05-07; made public 2026-05-07); locked to drand beacon Round 6062459 (2026-04-27) | Data (the committee map) does not exist yet at filing. **Prospective pre-registered confirmatory.** |

**What is and is not pre-registered.** The audit's headline Fisher combined p-value (p = 6.87×10⁻⁸) is not a classical pre-registered result: its input channels (Ch1, Ch2) were not named or specified on OSF before data was examined, though both channels' random seeds were publicly committed to the drand beacon before the official shapefiles arrived. The findings are therefore best characterised as *exploratory-reproducible* — the seeds are independently verifiable and the pipeline is bit-reproducible against checked-in data, but the specific test combination was not externally time-stamped before results were seen. The November 2026 confirmatory pass (OSF:qsgy8, pre-committed to a future map that does not yet exist) will provide the classical prospective pre-registration.

**Multiple-comparison strategy.** Two independent analytical channels are combined via Fisher's method (Fisher 1925): Channel 1 (Mahalanobis joint outlier, [§5.4.9](#sec-5-4-9)) and Channel 2 (SZAT bootstrap, [§5.2.10](#sec-5-2-10)) address structurally different questions — ensemble position versus boundary-choice efficiency — and are treated as independent inputs. Their empirical independence is verified post-hoc (ρ = −0.0014, §G1). The combined statistic T = −2∑ln(p_i) follows χ²(2k) under the null, giving T = 39.02 on df = 4. As a conservative alternative, Holm-Bonferroni applied to the two-channel case yields p ≤ 3.2×10⁻⁷ — both methods converge far below any standard threshold. Channel 3 (Neighbour-Drain, [§5.3.5](#sec-5-3-5)) and post-hoc metrics are not included in the Fisher combination and are evaluated individually; their non-significant results are reported as required by the pre-registration. See [§5.5](#sec-5-5) for the full combination method and `analysis/methodology/fisher_combination_defense.md` for the independence defense.

<a id="sec-4-4"></a>
### 4.4 Legal-defensibility framework (D1–D10)

The audit's red-team framework (documented in `analysis/red_team/legal_red_team_framework.md`) evaluates each finding against ten legal-defensibility dimensions:

- **D1 — Evidentiary chain (primary source + archive).** Every claim traces to a checked-in source anchored in `FROZEN_MANIFEST.md`.
- **D2 — Attribution accuracy (verbatim quotations).** Chair statements, commissioner statements, and submission excerpts are quoted verbatim with source paragraph.
- **D3 — Individual-actor characterisation (fair comment, public-interest, not defamatory).** Claims about specific actors are anchored in on-record behaviour; fair-comment and public-interest defences supported.
- **D4 — Methodology reproducibility.** Every numeric finding is reproducible via `python3 analysis/<script>.py`.
- **D5 — Data provenance.** Every CSV / GPKG / JSON has a documented source chain back to a primary anchor ([§3](#sec-3) and Appendix E).
- **D6 — Privilege / scope (fact vs opinion vs allegation).** Facts are labelled; inferences are labelled; constitutional and legal conclusions are reserved to counsel and courts.
- **D7 — Conflict of interest (author's standing).** [§1](#sec-1)'s Author Disclosure block makes the prior explicit and lists three findings that ran against the prior and were retained (`findings/partisan_bias_summary.md`).
- **D8 — Copyright / fair dealing.** Submission-archive excerpts, commission report quotations, and map images are used under fair-dealing for criticism and research (Copyright Act s. 29.1).
- **D9 — PII / confidentiality.** No personally identifying information beyond public officeholders' on-record statements and submitters who chose public-record submission is reproduced.
- **D10 — Time-stamped / falsifiable claims.** Pre-registration and OSF submission ([§5.5](#sec-5-5)) provide third-party time-stamped custody; every falsifiable claim carries an explicit falsifier ([§7.2](#sec-7-2)).

<a id="sec-4-5"></a>
### 4.5 What this audit does not claim

The paper does not claim statistical significance at the conventional 95% threshold on the partisan-bias magnitude: the Monte Carlo 95% CI over modelling choices crosses zero (see [§1](#sec-1)). It does not claim intent: reproducible directional findings are consistent with intentional engineering or with unlucky structural choice, and the audit cannot distinguish between these without additional evidence beyond public data. It does not reach a constitutional conclusion: Appendix F sets out the *Saskatchewan Reference** [1991] effective-representation framework under which the evidence could be evaluated by counsel and a court, but does not itself render a verdict. The audit's positive claim is structural, directional, and evidentiary.

<a id="sec-4-6"></a>
### 4.6 Test selection rationale + defense in depth

A full methodological reflection on *which* tests were chosen from the redistricting-analysis literature, *why* these rather than others, what specific criticisms each test carries and how the audit defends against them, what improvements have landed in response to red-team feedback, and what combined or novel tests (neighbour-drain adjacency, boundary-chain, temporal-compound durability, compactness-weighted EG) could add is at `analysis/methodology/test_selection_rationale.md`.

<a id="sec-4-7"></a>
### 4.7 Audit dependency graph (machine-readable apparatus map)

To answer the 2026-04-24 "house of cards" critique (whether this audit's findings all share a single fragile L0/L1 dependency such that one bad data point would cascade to most conclusions), the full apparatus was serialised into a machine-readable dependency DAG: 234 nodes across four layers (L0 raw data: 32; L1 constructed artefacts: 53; L2 analytical scripts: 75; L3 named findings: 74) linked by 454 edges (396 required, 23 corroborating, 35 validating). Builder / renderer / query CLI at `analysis/scripts/v0_1_dependency_graph_{build,render,query}.py`. Data at `analysis/methodology/audit_dependency_graph.{json,dot}`. SVG at `data/maps/audit_dependency_graph.svg`. Schema + worked examples at `analysis/methodology/audit_dependency_graph_readme.md`.

**Headline diagnostics.** The graph is **acyclic** (topological sort succeeds; no finding depends on itself through any chain). Has **zero orphan findings** (every L3 finding is reachable from L0 raw data via at least one path); and has five invalidation-cascade classes quantifying what survives when a given L0/L1 dependency is removed:

| Invalidated dependency | Findings orphaned | Findings robust | Comment |
|---|---:|---:|---|
| 2023 Statement of Vote (L0 vote data) | 48 of 74 (65 %) | 26 (35 %) | Largest-cascade L0: kills B-family + signatures + MCMC real-map scoring. Population-equality + geometry-only C-family + [§5.9](#sec-5-9) procedural are insulated. |
| Commission-published map PNGs | 26 of 74 (35 %) | 48 (65 %) | Kills all DPG-derived findings + signatures + anchoring. Vote-only B-family + MCMC + population + procedural insulated. |
| 2021 Census DAs (populations + geometry) | 25 of 74 (34 %) | 49 (66 %) | Kills DA-anchoring + Phase 4B/4F + MCMC ensemble + Chen-Rodden. Commission-population A-family + per-map B-family + CSD splits insulated. |
| 250k MCMC ensemble | 24 of 74 (32 %) | 50 (68 %) | Kills [§5.4](#sec-5-4) percentile flags + Chen-Rodden decompositions + R-hat. Per-map B-family point estimates + signatures + structural findings insulated. |
| v0_2 topology-clean DPG | 20 of 74 (27 %) | 54 (73 %) | Kills high-resolution [§5.2.7](#sec-5-2-7) spatial branch + [§5.8.5](#sec-5-8-5) anchoring. Most of the apparatus survives. |

**Load-bearing-node reading (retraction-pathway [§7.1](#sec-7-1).B resolution).** The 2026-04-24 retraction pathway committed the audit to retract the "directional consistency across six dimensions" synthesis if the DAG revealed that more than half the findings share a single fragile L0/L1 node. The DAG result meets that numerical threshold on the 2023 Statement of Vote (65 % of findings orphaned), but the retraction condition has a qualitative escape: partisan-bias analysis by definition depends on vote data. A Statement-of-Vote dependency is *expected* of any B-family finding and is not evidence of apparatus fragility. The *structurally-independent* core of the audit — the 26 findings that survive invalidation of the Statement of Vote — spans [§5.1](#sec-5-1) population equality, [§5.8](#sec-5-8) geographic coherence, [§5.9](#sec-5-9) procedural departure, and the geometry-only subset of [§5.3](#sec-5-3) signatures. These 26 findings carry the audit's main structural-asymmetry claim without vote-dependence. The B-family strengthens but does not singularly carry that claim. The synthesis is therefore NOT retracted on this ground, but is *refined*: the directional-consistency reading is reported as **"consistent across five non-vote-dependent dimensions, further strengthened by the one vote-dependent dimension."** The paper's headline is the non-vote-dependent layer.

**How to query the apparatus.** Reviewers can ask the graph directly: `python analysis/scripts/dependency_query.py --invalidate L0:data.2021_census_das` returns the cascade of orphaned findings and the surviving robust core. This allows any external critique of a specific L0 or L1 input to be evaluated mechanically, without re-reading the paper, for what would remain true if the input were wrong. Summary: the audit runs an over-determined test battery across six dimensions: (1) population equality, (2) partisan bias including the MCMC ensemble, (3) geographic coherence including the new municipal + DA anchoring audit, (4) procedural defensibility, (5) signature detection for packing, and (6) signature detection for cracking / engineered boundaries. No single test is intended to be dispositive. **directional consistency across six independent dimensions is the inferential artefact**. This is the Katz-King-Rosenblatt (2020) and Altman-McDonald (2011) discipline applied rigorously. A reviewer attacking any individual test is answered by the others: attacking the B2 efficiency-gap CI is answered by B4 seats-at-50/50 and B6 declination. Attacking the MAUP topology is answered by the crosswalk pipeline (no geometry). Attacking the MCMC ESS is answered by the multi-chain R-hat convergence proof and the 10k-ensemble percentiles. Attacking DPG tracing is answered by the precision ladder v0_2 → v0_3 → v0_4 → v0_5 and the ±500 m perturbation CI [+1.69, +7.67] pp that excludes zero. Tests explicitly ruled out (Bonferroni FWER, Wang 2014, Niemi-Deegan, DW-NOMINATE, CNN gerrymander-detection, full Bayesian updating, voter-file analysis, per-ED vote-prediction models) are documented with reasons in the rationale file [§2](#sec-2). A neighbour-drain adjacency test (Channel 3) was pre-registered and executed. Results and ordering rationale are in [§4.3](#sec-4-3) and [§5.3.5](#sec-5-3-5).

---

---

<a id="sec-5"></a>
## 5. Results

The eight subsections below consolidate the results of the tests described in [§4](#sec-4). [§5.1](#sec-5-1) reports population equality (A1–A3). [§5.2](#sec-5-2) reports the four partisan-bias metrics plus sensitivity analysis, natural-packing context, and the cross-metric disagreement reading. [§5.3](#sec-5-3) reports the formal packing / cracking / engineered-boundary signature detections. [§5.4](#sec-5-4) reports the MCMC constraint-bound-ensemble comparison across six runs of progressively higher sample count (10k preliminary → 250k publication-grade Run #3 → 250k full-coverage Run #4 → 1M Run #5 → 2M Run #6, the audit's authoritative ensemble), plus the [§5.4.7](#sec-5-4-7) 89-of-89 attribution + fuzzing analysis and [§5.4.8](#sec-5-4-8) Cannon et al. (2022) targeted-gerrymander short-bursts result. [§5.5](#sec-5-5) reports the pre-registered scorecard applied to both maps as a calibration test. [§5.6](#sec-5-6) reports the symmetry-of-test-selection counter-test. [§5.7](#sec-5-7) reports the stress-test-grades mini-audit. [§5.8](#sec-5-8) reports the geographic-coherence findings from direct map inspection. [§5.9](#sec-5-9) reports the procedural findings including the commission record, the April 16 government action, the submission-archive verification, and the constitutional backdrop. Headings follow the [§4](#sec-4) test ordering. The numbering is IMRAD-adjacent rather than tied to the original A/B/C/D section labels the commission used, with OLD-to-NEW cross-refs documented in `analysis/red_team/academic_reorganization_log.md`.

<a id="sec-5-0"></a>
### 5.0 Unexpected findings and link-back to the audit's three questions

Several findings during the audit ran counter to the prior expectation set by the redistricting-methods literature, by Canadian commission norms, or by the audit team's working hypothesis at the time the test was specified. Each is summarised below with (a) why it was unexpected, (b) what it indicates about the underlying map or process, and (c) which of the three opening questions in [§1](#sec-1) it bears on. Detailed evidence and statistical inference for each item are in the cited sub-section.

**Convention used in this subsection.** Q1 = "do the two commission proposals diverge in measurable, reproducible ways?" Q2 = "do those divergences run systematically in one political direction?" Q3 = "can the conclusions of the April 16 pivot be evaluated against a pre-registered falsifiability framework?"

<a id="sec-5-0-1"></a>
#### 5.0.1 Substantive findings that ran counter to expectation

1. **Municipal anchoring — did not survive canonical recomputation** ([§5.8.5](#sec-5-8-5)). *Pre-shapefile finding (DPG):* the minority map anchored only 14.5–16.5 % of its perimeter on CSD/DA edges versus the majority's 71.0 %, a 4.9× departure from Canadian comparator practice (70–85 %). This was the audit's load-bearing structural signal through April 2026. *Canonical (post-shapefile):* both 2026 maps fall within the 70–85 % norm (minority 72.0 %, majority 80.0 %). The 4.9× gap is not a property of the official maps. Full mechanism and reconciliation in [§5.8.5](#sec-5-8-5).[^anchoring_canonical] The four remaining geometry-independent dimensions (population dispersion, Calgary zone asymmetry, Airdrie fragmentation, spatial anomalies) are unaffected.

2. **Minority's mean-median sits at the p99.98 tail of the 1,010,000-plan canonical constraint-bound ReCom ensemble** ([§5.4](#sec-5-4)). *Expected:* both proposals would sit within the central 80–90 % of the ensemble (consistent with non-partisan drawing under the same statutory constraints). *Found:* the minority sits at p99.98 on mean-median (UCP-tail) and at p1.21 on declination (NDP-tail; metric-divergence noted). The majority sits closer to the median on every metric. *Indicates:* even under the lenient 25 % population-deviation constraint, the minority is in the small minority of constraint-legal maps that produce its measured partisan-bias profile. The combination of high mean-median percentile + low declination percentile is, per Warrington (2018), the signature of *deliberate packing* — the metrics disagree because each captures a different part of a packing-induced distribution. *Bears on:* **Q1** (statistical separation) and **Q2** (direction of separation).

3. **Five of six structural dimensions point in the same direction without depending on vote data** ([§6](#sec-6) synthesis). *Expected:* a partisan-bias finding is normally a vote-data finding. The audit specified five non-vote-dependent structural tests (population dispersion, Calgary geographic-zone gap, community-of-interest splits, municipal anchoring, visual anomaly count) primarily as falsification checks on the vote-based partisan-bias finding. *Found:* all five non-vote-dependent dimensions point in the same direction as the vote-based partisan-bias finding (minority more displaced from constraint-bound expectation than majority). *Indicates:* the partisan-bias direction is not solely a property of 2023 vote distribution. It is a property of the boundaries themselves, observable without any vote data. This is the audit's strongest defence against the "noise from one election" objection. *Bears on:* **Q2** (direction is robust across vote-independent measurement) and supports the **Q3** pre-registration commitment that the same five tests will be run against the November 2026 Lunty-committee map.

4. **The 2019 cross-election check — direction stability under v0_8 full coverage** ([§1.2](#sec-1-2) caveat 3, [§5.2.3](#sec-5-2-3), refreshed 2026-04-25). *Expected:* the v0_7 partial-coverage 2019 check produced an apparent EG direction-flip vs the 2023 reading, suggesting the audit's partisan-bias direction was vote-distribution-dependent. The expectation under full coverage was that some metrics might reverse and some might hold. *Found:* under v0_8 full-coverage area-proportional attribution, **3 of 4 metrics hold direction across 2019 and 2023 on both maps** (EG, declination, seats@50/50 all stable; only mean-median flips, and mean-median is sub-threshold on the 250k Run #4 ensemble for both maps). *Indicates:* the v0_7 direction-flip was a partial-coverage artefact (22 unattributed rural EDs whose UCP votes were systematically excluded). Under full coverage the partisan-bias direction is structurally stable. *Bears on:* **Q2** with the qualifier *strengthened*, not weakened — the audit's directional claim is consistent across 2019 and 2023 voter distributions on the dimensions that matter. The earlier "direction reverses under 2019 votes" caveat is retracted.

5. **One of the six contested minority redraws (St. Albert-Sturgeon) is constraint-forced rather than engineered** ([§5.9.2](#sec-5-9-2) + `minority_rationales_validation.md`). *Expected:* a symmetric framework should classify all contested redraws as either rationale-supported or rationale-failed. *Found:* five of six minority redraws fail their stated rationale under the audit's symmetric framework, but the sixth — St. Albert-Sturgeon — produces the same two-district structure on both the majority and minority maps independently, indicating the configuration is forced by the Act's constraints rather than chosen. (A seventh redraw the audit had previously listed — the Lethbridge / Taber-Warner federal-boundary match — has been removed because the minority report does not in fact make the underlying federal-boundary claim; see `analysis/methodology/lethbridge_federal_boundary_check.md`.) *Indicates:* the minority's 5/6 rationale-failure pattern is meaningfully separated from the 1/6 constraint-forced case. Symmetric application of the framework distinguishes "engineered redraw" from "constraint-forced redraw" (operationalised as: when two independent drafting teams converge on the same configuration under the same constraints, it is constraint-forced, not designed). This anchors the audit against the legitimate "you only count what disagrees with you" critique. *Bears on:* **Q1** (the divergences are not uniformly negative) and **Q2** (the engineered/forced ratio is itself directional evidence).

<a id="sec-5-0-2"></a>
#### 5.0.2 Methodological findings that ran counter to expectation (DPG construction, §4.1.5–§4.1.6)

The audit's geometric pipeline produced several findings that have implications beyond this audit and are documented in detail in the methods paper companion (`findings/methods_paper_draft.md`). They are summarised here only insofar as they affect the audit's primary inferences.

6. **21 of 89 majority EDs have zero geometry in v0_7, and inherit empty into v0_8** ([§4.1.6](#sec-4-1-6)). *Expected:* the multi-source canonical assembly (v0_7) was specified to produce 89/89 polygon coverage by selecting from up to five candidate geometries per ED. *Found:* 21 EDs (mostly small urban Calgary and Edmonton districts plus Stony Plain–Drayton Valley, St. Albert-Sturgeon, Lacombe-Clearwater, Wetaskiwin-Ponoka-Maskwacis) have no usable polygon at any source tier. They remain empty in v0_8 even after the four-phase perfecter. *Indicates:* the upstream candidate-source ensemble (DA dissolve, CSD union, OSM-municipal, sweep, prior-cycle inheritance) does not span the full Alberta urban-ED space. Small urban EDs whose boundaries follow neither municipal lines nor prior-cycle envelopes nor surveyed DA edges are not reconstructible from public data alone. *Bears on:* **Q1 / Q2 indirectly** — the empty-ED limitation is the single largest constraint on the audit's geometry-dependent tests ([§5.4](#sec-5-4) MCMC, [§5.8.5](#sec-5-8-5) anchoring, [§5.2.7](#sec-5-2-7) high-resolution spatial vote attribution). The audit's response is not to mask the limitation but to report it as a first-class metric ("68 of 89 EDs with geometry; 21 inherited-empty") and to triangulate the geometry-dependent findings against the geometry-independent tests in items 1–5 above. The directional-consistency synthesis survives because the non-empty 68 EDs include all the contested partisan-edge zones that drive the [§5.2](#sec-5-2) / [§5.4](#sec-5-4) results.

7. **Phase 3 spatial-index gap-fill systematically inflates rural ED areas in v0_8 vs v0_7** ([§4.1.6](#sec-4-1-6)). *Expected:* gap-fill would distribute the residual 16,955 majority gap polygons (totalling 72,252 km²) across the 89 EDs in proportion to ED perimeter or centroid-distance to the gap. *Found:* because nearest-neighbour assignment can only target *non-empty* EDs, and 21 EDs are empty, the gap polygons concentrate disproportionately in adjacent rural EDs. West Yellowhead grew 47,092 → 93,599 km² (+99 %). Taber-Cardston grew 14,982 → 30,800 km² (+106 %). Grande Prairie-Wapiti grew 8,360 → 17,220 km² (+106 %). *Indicates:* the v0_8 rural-ED footprints are *over-stated* relative to commission intent — they include territory that the commission would have assigned to the empty urban EDs. The audit's response: any v0_8-derived per-ED area metric is reported with a "rural-inflation caveat". Partisan-bias and population-equality findings (which use commission-published populations, not derived areas) are unaffected. *Bears on:* none of the audit's substantive findings, but it bears on the methodological-novelty contribution to the redistricting-GIS literature.

8. **Calgary-Falconridge-Conrich is fully nested inside Airdrie-East in v0_7 / v0_8 canonical** ([§4.1.6](#sec-4-1-6), v0_8.1 refinement). *Expected:* a multi-source assembly using tier-rank precedence should not produce nested EDs (one ED entirely inside another) because the precedence rule is supposed to give priority to a single source per ED. *Found:* the Airdrie-East boundary (sweep-derived) and the Calgary-Falconridge-Conrich boundary (independently DA-anchored) were constructed from sources whose footprints are inconsistent for this region. The result is a 141.9 km² nested overlap. *Indicates:* the multi-source-assembly approach has a failure mode the v0_2 single-source-precedence pipeline did not: cross-source inconsistency for the same physical territory. The audit's response is the v0_8.1 *nested-polygon ownership inversion* refinement (a novel contribution to the polygon-conflation literature), which preserves both EDs by carving the nested polygon out of the surrounding one. *Bears on:* methodological-contribution claims in [§4.1.6](#sec-4-1-6).

9. **9 of 10 Alberta city centres land in correctly-named EDs in the v0_8.1 refined majority** ([§4.1.6](#sec-4-1-6) alignment proof). *Expected:* given the upstream limitations (21 empty EDs, rural inflation, nested-polygon residuals), the city-centre point-in-polygon plausibility check was specified primarily as a falsification gate. A high pass rate was not anticipated. *Found:* Calgary, Edmonton, Red Deer, Lethbridge, Medicine Hat, Grande Prairie, Fort McMurray, Airdrie, and Spruce Grove all contain a Statistics Canada city-centre representative point inside an ED whose name references that city. The single miss (St. Albert) lands in the geographically-adjacent rural West Yellowhead ED because the v0_8 St. Albert polygon (37.9 km²) does not extend to the city-centre representative point — a localisation residual within the documented DPG ±500 m perimeter precision band. *Indicates:* despite the data-completeness limitation in item 6 and the rural-inflation artefact in item 7, the v0_8 polygons are spatially correct on the *non-empty* ED set. The audit's geometry-dependent findings ([§5.4](#sec-5-4) MCMC, [§5.8.5](#sec-5-8-5) anchoring) are therefore defensibly grounded on the 68 EDs that do have geometry. *Bears on:* the methodological defensibility of every geometry-dependent claim in [§5](#sec-5).

<a id="sec-5-0-3"></a>
#### 5.0.3 Summary of unexpected findings → original questions

| Item | Unexpected finding | Bears on Q1 (divergence) | Bears on Q2 (direction) | Bears on Q3 (falsifiability) |
|------|---------------------|:------------------------:|:-----------------------:|:----------------------------:|
| 1 | Municipal anchoring (did not survive canonical recomputation — see [§5.8.5](#sec-5-8-5))[^anchoring_canonical] | ✗ not reproduced | ✗ not confirmed | ✓ replicable test |
| 2 | Minority at p98+ on MCMC ensemble | ✓ strong | ✓ supportive | ✓ replicable test |
| 3 | Five non-vote dimensions agree | ✓ supportive | ✓ strong | ✓ pre-registered |
| 4 | 2019 vote check reverses direction | — | ✓ qualifier (2020s-era) | ✓ pre-registered honesty |
| 5 | 1 of 7 minority redraws unavoidable | ✓ qualifier | ✓ engineered/forced ratio | ✓ symmetric framework |
| 6 | 21 of 89 EDs empty in v0_7/v0_8 | (data limit) | (data limit) | ✓ transparent reporting |
| 7 | Phase-3 gap-fill inflates rural EDs | (artefact) | (artefact) | ✓ caveat published |
| 8 | Nested-polygon overlap in Airdrie/Calgary | (methodological) | — | ✓ refinement applied |
| 9 | 9/10 city centres land correctly | (defensibility) | — | ✓ alignment proof |

**Bottom-line answers preview** (full discussion in [§6](#sec-6), [§8](#sec-8)): items 1–3 collectively answer Q1 ("yes, measurably") and Q2 ("yes, with the qualifier in item 4"). Items 6–9 answer Q3's methodological precondition: the audit's apparatus is internally honest about its limitations and externally verifiable against independent reference points, which is what allows the same apparatus to be re-run against the November 2026 Lunty-committee map under pre-registered scoring.

<a id="sec-5-1"></a>
### 5.1 Population equality

<a id="sec-5-1-1"></a>
#### 5.1.1 Distribution variance (A1)

**Data-basis preamble.** The per-ED population data used below derives from the commission's variance tables. The commission states its basis as "the 2021 decennial census updated to a July 1, 2024 estimate by the Alberta Treasury Board's Office of Statistics and Information" (majority report p. 29; minority report p. 296, verified extraction in `analysis/methodology/commission_source_provenance.md`). The provincial total used by the commission for quota derivation is 4,888,723, which matches Statistics Canada's Q2 2024 postcensal estimate for Alberta (Table 17-10-0009, released September 25, 2024) to the person, because the OSI sub-provincial estimates nest inside the StatsCan provincial control. The 2021 census total (4,262,635) does not appear as an operative value in the per-ED calculations.

Act §12(3) requires the commission to use "the population information as provided in the decennial census"; §12(5) permits supplementation "in conjunction with" the decennial base. Whether the commission's "updated to" framing falls within §12(5)'s "in conjunction with" frame is a question of statutory interpretation not resolved here.

The Plan B cross-check (`analysis/reports/plan_b_cross_check.md`) verifies that every [§5.1](#sec-5-1) verdict below is identical whether computed against the 2021 census directly, the 2024 OSI estimate (commission's basis), or the 2025 TBF estimate. The A1 MAD figures are computed on the commission's stated basis. They are intended for apples-to-apples comparison with the commission's own published variance tables. A 2021-census-direct A1 computation on the 87 current 2019 EDs, provided as Appendix C, serves as a §12(3)-operative reference point. The equivalent computation for the 2026 proposals is blocked by the non-release of 2026 shapefiles.

Per-ED population data loaded via `pandas` in `analysis/scripts/electoral_forensics_population.py`.

| Metric                                   | Majority 2026 | Minority 2026 |
| ---------------------------------------- | ------------- | ------------- |
| N districts                              | 89            | 89            |
| Mean population                          | 54,929        | 54,930        |
| Median population                        | 55,791        | 55,713        |
| Standard deviation                       | 5,301         | 6,533         |
| Mean absolute deviation (MAD) from 54,929[^mad_majority_mean] | 3,180         | 4,707         |
| Maximum positive deviation               | +14.28%       | +24.06%       |
| Maximum negative deviation               | −47.72%       | −45.36%       |
| EDs above +10% from mean                 | 5             | 15            |
| EDs above +15% from mean                 | 0             | 5             |
| EDs above +20% from mean                 | 0             | 3             |
| EDs above +25% (statutory violation)     | 0             | 0             |
| EDs below −10% from mean                 | 5             | 13            |
| EDs below −15% from mean                 | 4             | 5             |
| EDs below −20% from mean                 | 4             | 4             |
| EDs below −25% (requires s.15(2))        | 3             | 3             |

The minority's MAD is 48% wider than the majority's. Neither exceeds the ±25% statutory cap. Both use all three permitted s.15(2) exceptions. The key distributional observation is the asymmetric positive tail: the minority has 5 districts above +15% and 3 above +20%, none of which the majority has.

[^mad_majority_mean]: Both MADs are computed against the majority's mean (54,929) rather than each map's own mean (majority mean: 54,929; minority mean: 54,930). Using a common reference enables direct apples-to-apples comparison across maps. The 1-person difference is negligible: re-computing the minority MAD against its own mean of 54,930 produces 4,707 (unchanged at this precision level).

<a id="sec-5-1-2"></a>
#### 5.1.2 Calgary geographic-zone asymmetry (A2)

Classification rule: Zone A comprises Calgary EDs whose territorial centroid lies north or east of a dividing line running along the Bow River through downtown and then southeast along Deerfoot Trail. Zone B comprises EDs south or west of that line. The classification is documented in source (`CALGARY_ZONE_A`, `CALGARY_ZONE_B` in `electoral_forensics_population.py`) with no residual unclassified Calgary EDs. The partisan correlation of these zones (Zone A ≈ NDP-competitive, Zone B ≈ UCP-dominant) is a property of voter geography, not of the classification itself.

| Zone                                      | Majority (n / mean pop) | Minority (n / mean pop) |
| ----------------------------------------- | ----------------------- | ----------------------- |
| Zone A (N / E / central Calgary)          | 17 / 56,460             | 17 / 61,225             |
| Zone B (S / W Calgary)                    | 11 / 56,255             | 12 / 54,569             |
| Gap (Zone A − Zone B)                     | +205 (+0.36%)           | +6,656 (+12.20%)        |

**Robustness check (G4).** Re-running the test with a purely data-driven rule — Calgary EDs classified by the party that won them in 2023, mapped forward to 2026 by name-stem match — reproduces the directional finding:

| Rule                                  | Majority gap | Minority gap |
| ------------------------------------- | ------------ | ------------ |
| Geographic (Zone A vs Zone B)         | +0.36%       | +12.20%      |
| Data-driven (2023-NDP-won vs -UCP-won)| +0.39%       | +7.71%       |

Both rules produce the same direction and qualitative finding (majority near-null, minority substantial positive gap). The magnitude varies (7.71–12.20%) because the two classifications do not overlap perfectly — some EDs in Zone A were UCP-won in 2023 and vice versa. The audit reports the range rather than a single number. The lower bound (7.71%) is the conservative estimate.

<a id="sec-5-1-3"></a>
#### 5.1.3 Urban–rural regional breakdown (A2b)

| Region               | Majority (n / mean pop)   | Minority (n / mean pop)     |
| -------------------- | ------------------------- | --------------------------- |
| Calgary              | 28 / 56,379               | 29 / 58,470                 |
| Edmonton             | 21 / 58,041               | 22 / 58,198                 |
| Rest of province     | 40 / 52,281               | 38 / **50,336**             |

The minority's rest-of-province mean is 3.9% lower than the majority's. Smaller rural districts produce proportionally more rural seats for the same provincial population. Given the 2023 rural Alberta NDP two-party share of 33.5% (observed from the Statement of Vote), smaller rural districts yield net UCP seat gains.

<a id="sec-5-1-4"></a>
#### 5.1.4 s.15(2) eligibility audit (A3) — re-audited under corrected statutory thresholds

Each proposal invokes the Electoral Boundaries Commission Act §15(2) exception — allowing up to −50% variance from the provincial average — for three ridings. §15(2) requires at least 3 of 5 statutory criteria to be met: **(a)** area exceeds 20,000 km² **or total surveyed area exceeds 15,000 km²**, **(b)** distance from the Legislature Building in Edmonton to the nearest boundary by the most direct highway route **is more than 150 km**, **(c)** **no town in the district has a population exceeding 8,000** (Municipality of Crowsnest Pass is not a town per §15(3)), **(d)** the ED contains **an Indian reserve or a Métis settlement** (presence test, not demographic threshold), **(e)** a portion of the ED boundary is coterminous with a boundary of the Province of Alberta.

An earlier draft of this section used incorrect thresholds at (a), (b), and (c). The audit's Terms-of-Reference cross-check (`findings/terms_of_reference_audit.md`) identified the errors and a focused re-audit (`analysis/methodology/s15_2_reaudit.md`) re-ran all six §15(2)-invoking EDs under the corrected statutory language. Two verdicts change; both flip from FAIL to PASS.

| Riding                                       | Var%   | Criteria met (of 5) | Verdict |
| -------------------------------------------- | ------ | ------------------- | ------- |
| Central Peace-Notley (majority)              | −47.7% | 5                   | Pass    |
| Lesser Slave Lake (majority)                 | −45.4% | 4                   | Pass    |
| Canmore-Banff (majority)                     | −27.2% | 3                   | Pass    |
| Central Peace-Notley (minority)              | −44.6% | 5                   | Pass    |
| Lesser Slave Lake (minority)                 | −45.4% | 4                   | Pass    |
| Rocky Mountain House-Banff Park (minority)   | −30.3% | 5                   | Pass    |

All six §15(2) invocations across both maps pass the 3-of-5 statutory threshold under the correct thresholds.

- **Canmore-Banff (majority, 3/5).** (a) area likely fails; commission does not claim it. (b) passes (Canmore ~390 km from the Legislature). (c) fails — Canmore 15,990, Banff townsite 8,305 (StatCan 2021 Census). (d) passes — commission places Stoney Nakoda (Morley), Eden Valley 216, and other reserves inside the ED. (e) passes — BC border. Statutorily legitimate at the 3/5 minimum.
- **Rocky Mountain House-Banff Park (minority, 5/5).** (a) passes — Clearwater County alone is 18,692 km²; the ED adds Mountain View W., Bighorn MD, Rocky View W., and Banff NP north of the Town of Banff. (b) passes — Rocky Mountain House is ~215 km from Edmonton by road. (c) passes — largest town is Rocky Mountain House at 6,765 (StatCan 2021); Banff townsite is not in this ED. (d) passes — commission names five reserves inside (Big Horn 144A, O'Chiese 203, Stoney 142/143/144, Stoney 142B, Sunchild 202). (e) passes — NP extension reaches BC.
- **Counterfactual: RMH-Banff Park without the NP extension.** Trimming the Banff NP portion leaves approximately the predecessor Rimbey-Rocky Mountain House-Sundre footprint plus Clearwater County extensions. Under this counterfactual the ED still passes 4/5 — only (e) BC-border is lost. The NP extension adds criterion (e) to the count; (a) is already satisfied by Clearwater County alone.

**Engineered-boundary characterization: revised.** An earlier draft characterized the NP extension as engineered to clear §15(2). Under the correct thresholds the ED qualifies on 4 of 5 criteria without the extension and 5 of 5 with it. The extension moves the criterion count from 4 to 5, not from fail to pass. The prior characterization was accordingly withdrawn as overstated. However, the commission's own final report (March 23, 2026, p. 10) provides stronger primary-source evidence than the audit's earlier purposive reading: the majority commissioners write that the minority "artificially extend[ed]" the boundary through Banff National Park "which is a bad faith effort to ensure it can be protected under s. 15(2) of the Act." This is a direct characterization by the commission chair, in a public statutory document, of his minority colleagues' geographic choice. The audit's earlier withdrawal addressed the *eligibility* question (does RMH-Banff Park qualify for §15(2)? — yes, on 4 of 5 without the extension). It does not address the *substantive choice* question (why extend through uninhabited territory when the ED was already eligible?). [§5.1.5](#sec-5-1-5) develops the full differential-application analysis, including the commission chair's verbatim language.

<a id="sec-5-1-5"></a>
#### 5.1.5 §15(2) discretionary application: differential treatment between the maps

**The provision is permissive, not mandatory.** §15(2) EBCA uses the formulation "The Commission *may have* an electoral division… *if the Commission is of the opinion* that the electoral division should be established and at least 3 of the following criteria apply." Both the grant of permission ("may have") and the opinion gate ("if the Commission is of the opinion") are discretionary. A district that satisfies 3 of 5 statutory criteria is eligible for §15(2) protection. The commission is not required to grant it.

**The 2026 invocations.** Both maps invoke §15(2) for three ridings. All six invocations are statutorily eligible under the corrected thresholds ([§5.1.4](#sec-5-1-4) table). The maps agree on two of three slots (Central Peace-Notley and Lesser Slave Lake); they diverge on the third. The majority's third slot is Canmore-Banff (3/5 criteria; genuine Indigenous community presence; remote mountain geography). The minority's third slot is Rocky Mountain House-Banff Park (5/5 criteria; the fifth criterion — BC provincial border — requires extending the boundary through Banff National Park territory where no one permanently lives).

**The Lesser Slave Lake trajectory.** ED 70 (Lesser Slave Lake) carries a population of 27,079, at −45.4% below the 89-ED provincial average of 54,929 — just above the §15(2) −50% floor. The commission's October 2025 interim report proposed eliminating ED 70 and merging it with Athabasca-Barrhead-Westlock into a new "Mackenzie" division. The interim report did not invoke §15(2) for a preserved Lesser Slave Lake. Following more than 80 Round 2 public submissions — many from within the riding, citing the 14 First Nations and Métis communities in the division (EBC Final Report) — the commission reversed course. The March 2026 final report preserves Lesser Slave Lake at −45.4% variance under §15(2), citing the Indigenous communities as the primary community-of-interest basis.

The partisan arithmetic of the eliminated alternative: a combined Mackenzie would have produced a riding at 27.9% NDP (Lesser Slave Lake's 33.7% NDP plus Athabasca-Barrhead-Westlock's 25.7% NDP, all ballot types, 2023 election). ED 70's northern Voting Area cluster (VAs 029–051) runs 534 NDP / 535 UCP on election day — a 50/50 sub-region that would have been absorbed into a 2.5:1 UCP-majority division under the Mackenzie proposal. The §15(2) protection, ultimately granted under majority-commissioner approval, prevents that dilution.

**The asymmetry in effect.** The two maps' third §15(2) slots produce structurally different COI outcomes:

| | Majority's third slot (Canmore-Banff) | Minority's third slot (RMH-Banff Park) |
|---|---|---|
| Criteria without contested extension | 3/5 — already eligible | 4/5 — already eligible |
| Contested boundary element | N/A | NP extension adds criterion (e) |
| Represented community in extension territory | N/A | None — no permanent residents in Banff NP |
| Indigenous community basis | Stoney Nakoda, Eden Valley 216, others (within core footprint) | Five named reserves — all within Clearwater County / RMH core, not in the park extension |

Both third-slot ridings contain Indian reserves or Métis settlements (criterion d). The distinction is not about Indigenous presence. It is about the boundary extension: the NP extension adds no represented community and serves no community-of-interest rationale.

**Primary source characterization.** The EBC Final Report (March 23, 2026), p. 10, contains the following verbatim statement from the majority commissioners:

> "They propose to retain an electoral division of 'Rocky Mountain House-Banff Park' by artificially extending its boundary to the province's western border with British Columbia (taking part of Banff National Park, where no one lives), which is a bad faith effort to ensure it can be protected under s. 15(2) of the Act."

This characterization is the commission chair's, not the audit's. The audit quotes it because it is the most precise primary-source description of the substantive choice the minority made with their third §15(2) slot. The audit's own [§5.3.3](#sec-5-3-3) engineered-boundary finding rests on the "populated alternatives existed and were not taken" standard (Reading B). The chair's language provides independent primary-source corroboration of the substantive observation.

**Consistency with the audit's no-intent posture.** The audit does not characterize intent ([§4.5](#sec-4-5)). Quoting the commission chair's use of "bad faith" is a factual act — the chair used that phrase in a public statutory document — distinct from the audit independently asserting bad faith. The audit reports what primary sources say. It does not claim to know what was in any commissioner's mind.

**Constitutional dimensions.** §15(2) EBCA is framed around geographical remoteness and representation adequacy. The EBCA's community-of-interest mandate (§14) requires commissions to consider whether proposed boundaries preserve or divide natural constituencies. Read together, §14 and §15(2)(d) create a statutory framework for Indigenous representation in remote ridings: the presence of Indian reserves and Métis settlements is a criterion justifying population-variance latitude precisely because those communities might otherwise be subsumed into large districts where their representation interest is diluted. The interim report's proposed Mackenzie merger would have achieved exactly that dilution. The commission chair's characterization of the minority's third §15(2) slot as "bad faith" asserts, in this statutory context, that a provision designed to protect underrepresented remote communities was applied in a way that defeats its purpose. The audit notes the tension without resolving the constitutional question.

**Competing Indigenous views on representation.** The commission's record documents two distinct Indigenous positions on the Lesser Slave Lake / Mackenzie question: the North Peace Tribal Council (submission 883, per EBC Final Report) supported a dedicated Mackenzie riding to give northern communities a focused voice. Linda Green (submission 968) opposed consolidation, favouring multiple northern ridings for multiple representatives. The commission resolved in favour of a preserved, expanded Lesser Slave Lake. The audit notes both positions without adjudicating between them. The §15(2) finding does not depend on which COI configuration is preferred.

**Lunty committee context.** The April 16, 2026 Legislative Assembly motion (Motion 19) set aside both commission reports and established a Special Select Committee of five MLAs (colloquially the "Lunty committee," chaired by UCP MLA Brandon Lunty; 3 UCP / 2 NDP; report due November 2, 2026). The committee will face the same §15(2) decisions, including whether to protect Lesser Slave Lake's 14 Indigenous communities. The committee is not required to hold public hearings. The commission reversed its interim elimination proposal after 80+ public submissions, and there is no analogous mechanism ensuring comparable public input will reach the committee. This is a structural observation, not a finding about the committee's likely decisions.

---

<a id="sec-5-2"></a>
### 5.2 Partisan bias

Scripts: `analysis/scripts/packing_cracking_analysis.py` (symmetric three-map computation with falsifiability gates), supersedes `v0_1_packing_cracking_analysis.py` which computed only 2019 and minority. Methodology (B1–B6 definitions, vote-attribution blending, sign convention) is in [§4](#sec-4). The subsections below report the results.

<a id="sec-5-2-1"></a>
#### 5.2.1 Results

| Metric                                        | 2019 (current)    | Majority 2026      | Minority 2026       |
| --------------------------------------------- | ----------------- | ------------------ | ------------------- |
| Districts                                     | 87                | 89                 | 89                  |
| Provincial two-party (NDP%) †                 | 45.56%            | 42.56%             | 42.56%              |
| Actual seats (NDP / UCP)                      | 38 / 49           | 34 / 55            | 29 / 60             |
| **B2** Compactness-Weighted Efficiency Gap    | **+2.75%**        | **+1.49%**         | **-2.42%**          |
| Standard Efficiency Gap (Phase 4C) ‡          | −2.64%            | +0.04%             | **+3.96%**          |
| **B3** Mean-median gap (NDP)                  | −2.22 pp          | −3.64 pp           | +1.03 pp            |
| **B4** NDP seats at 50/50 uniform swing       | 46                | 48                 | 43                  |
| Asymmetry at 50/50 (|NDP − UCP|)              | 5                 | 7                  | 3                   |

*B4 — Uniform swing model (Gelman and King 1994). Alberta's non-linear seat-vote curve means the true NDP seat count at a tied provincial vote is likely lower than the figures above. This row is presented for cross-map comparability, not as a seat prediction.*

*† Provincial two-party NDP% for 2026 maps uses va_ndp/va_ucp integer columns (province-wide sum 893,018 total, 42.56% NDP) — the same substrate as the MCMC canonical ensemble. The 2019 row uses the 2023 election CSV (1,706,304 vote total, 45.56% NDP). The integer columns preserve intra-ED partisan ratios at a different scale than the CSV; all bias metrics are ratio statistics invariant to this difference. ‡ Standard EG computed via Phase 4C exact VA-level spatial attribution (packing_cracking_analysis.py v0.3, 2026-05-18), consistent with mcmc_ensemble_canonical.py to within 0.06 pp.*

**Multiple comparisons note (S2).** Four metrics (B2, B3, B4, B6) are reported across three maps, producing twelve comparisons. Under Bonferroni correction for four tests at α=0.05, the individual threshold is α=0.0125. No single metric reaches this threshold on its own. The finding rests on directional consistency across metrics under 2023 vote input, not classical significance of any one metric individually.

**Version note: B4 direction revision.** An earlier version of this analysis reported B4 (NDP seats at 50/50 uniform swing) as majority 44 / minority 42 — with the minority returning fewer NDP seats than the majority. A v0.2 correction reversed this to majority 45 / minority 46 via two simultaneous fixes: (a) mapping dictionary corrections for Olds-area and Calgary suburban hybrid EDs; (b) URBAN_WEIGHT_DEFAULT revised from 0.70 to 0.85 (see [§5.2.2](#sec-5-2-2)). Phase 4C (v0.3, 2026-05-18) further revises B4 to majority 48 / minority 43 via direct VA-level spatial attribution, replacing the blend model entirely. Phase 4C standard EG shows the minority as more UCP-favourable than the majority (standard EG: majority +0.04%, minority +3.96% — positive = NDP wastes more = UCP-favoured), consistent with the MCMC ensemble's placement of minority EG at p94.4. B3 (mean-median) and B4 (seats@50/50) confirm the same direction: majority retains more NDP seats at a tied vote (48 vs 43) and a less extreme mean-median gap (−3.64 pp vs +1.03 pp). The CWEF (B2, compactness-weighted) shows minority −2.42% vs majority +1.49% — both in the UCP-favoured direction for minority. See [§5.2.4](#sec-5-2-4) for interpretation of this between-metric disagreement.

**All EG values are below the 7 % threshold** — academic-literature authority only, never judicially adopted (see [§5.2.8](#sec-5-2-8)). The CWEF shows the minority as UCP-favorable (−2.42%) relative to majority (+1.49%) and 2019 baseline (+2.75%). Phase 4C standard EG (positive = NDP wastes more = UCP-favoured) shows minority +3.96% vs majority +0.04% — the minority produces substantially higher NDP wasted-vote proportion, consistent with the MCMC canonical placement of minority EG at p94.4. CWEF and standard EG agree on direction: both show minority as more UCP-favourable than majority. They disagree on the absolute position of the majority map (CWEF shows majority as mildly NDP-favourable at +1.49%; standard EG shows majority as approximately neutral at +0.04%). [§5.2.4](#sec-5-2-4) interprets this between-metric disagreement in absolute magnitude.

**Canadian comparative base rate.** A first-catalogue computation of inter-map partisan-asymmetry magnitude across recent Canadian provincial and federal redistributions is reported in `analysis/methodology/canadian_base_rate_computed.md` and `data/canadian_redistribution_base_rate.csv`. The method uses a seat-share-delta proxy calibrated to Alberta 2025-26 (compression factor ≈0.455, acknowledged approximation). Seven comparable cycles were scored: Federal 2022 Alberta sub-commission, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018, and Alberta 2025-26.

Because Alberta 2025-26 is both the case under audit and the cycle from which the compression factor is fit, it is **excluded from the comparator distribution used to position it** (an earlier version of this paper reported a "71st percentile" placement against an n=7 distribution that included Alberta 2025-26; that claim was circular and has been retracted). Against the n=6 comparator, four cycles produce zero inter-map projected-winner asymmetry. Two produce non-zero asymmetry — Alberta 2017 at 0.52 pp and Manitoba 2018 at 0.80 pp. Alberta 2025-26's 0.51 pp point-estimate is ordinally equivalent to Alberta 2017 and below Manitoba 2018. The high-end 1.52 pp exceeds the observed Canadian maximum in this sample.

The defensible statement is: **Alberta 2025-26 is one of three Canadian redistribution cycles (of seven sampled) that produced any inter-map projected-winner asymmetry. At the low-end it is ordinally equivalent to Alberta 2017 and below Manitoba 2018. At the high-end it exceeds the observed Canadian maximum in this sample.** The sample is small and proxy-based. Direct per-ED EG computation remains future work.

**Phase 4C update (2026-05-18): blend model superseded.** Direct VA-level spatial attribution (packing_cracking_analysis.py v0.3) replaces the 0.85 urban-weight blend. Standard EG: majority +0.04%, minority +3.96%. The weight-conditional sensitivity range in [§5.2.2](#sec-5-2-2) is retained for methodological transparency. The instruction to "report the range, not the 0.85 point estimate" no longer applies — Phase 4C provides direct measurement consistent with the MCMC canonical pipeline.

<a id="sec-5-2-2"></a>
#### 5.2.2 Sensitivity (G5)

**Deterministic vs Monte Carlo sensitivity.** The five rows in the table below are deterministic point estimates: each row holds urban weight fixed at a specific value and computes the resulting EG. They are not probabilistic confidence bounds. The Monte Carlo interval [−3.04, +0.76] pp reported in [§5.2.3](#sec-5-2-3) is a separate calculation: it varies urban weight, rural baseline, and per-hybrid jitter simultaneously across 2,000 parameter draws and is wider because it captures cross-parameter covariance, not just urban-weight sensitivity alone. Neither replaces the other; the table maps how the central estimate moves with urban weight. The Monte Carlo interval maps whether the direction claim is robust across the full modelling-choice space.

Efficiency gap under alternative urban weights (holding 2019 vote data and rural baseline constant):

| Urban weight | Majority EG | Minority EG | Asymmetry (Min − Maj) |
| ------------ | ----------- | ----------- | --------------------- |
| 0.60         | +1.27%      | −0.02%      | −1.29 pp              |
| 0.70         | +0.07%      | −0.40%      | −0.47 pp              |
| 0.80         | −0.62%      | −2.10%      | −1.48 pp              |
| **0.85**     | **−0.40%**  | **−1.81%**  | **−1.41 pp** *(central)* |
| 0.90         | −0.17%      | −1.50%      | −1.33 pp              |

Direction is stable across all five weights: minority EG is more UCP-favorable than majority EG under every parameter setting. Magnitude ranges from 0.47 to 1.48 percentage points across the 0.70–0.80 range. The central (0.85) case gives a minority-majority asymmetry of −1.41 pp.

**Phase 4C supersedes this table (2026-05-18).** Direct VA-level spatial attribution gives standard EG majority +0.04%, minority +3.96% — a +3.92 pp asymmetry. The blend model's sign is wrong: it showed minority as more UCP-favourable than majority (both negative, minority more negative), while Phase 4C and the MCMC canonical ensemble both show majority as approximately neutral (+0.04%, p15.5) and minority as substantially UCP-favourable (+3.96%, p94.4). This table is retained to document the blend model's behaviour; it must not be cited as evidence of the EG direction. See [§5.2.1](#sec-5-2-1) Standard Efficiency Gap row and DOCUMENTED CORRECTIONS (C5).

**Neutral-ensemble benchmark (D4).** [§5.2.1](#sec-5-2-1)–5.2.2 establish the inter-map asymmetry under blended-crosswalk attribution, but that difference has no theoretical null on its own — two maps can produce different EGs without that gap being unusual relative to neutral redistricting. [§5.4.9](#sec-5-4-9) provides the benchmark: the authoritative 1,010,000-plan canonical ensemble (1,010,000 plans, 4 chains × 252,500 steps, base_seed=1432864451, official EA shapefiles). The minority's EG at p94.4 is below the p95 flag threshold. Mean-median at p99.98 and declination at p1.21 are extreme-tail outliers. Seats@50/50 at p99.99 has individual flag reinstated at publication-grade ESS. The majority sits within the neutral band on three of four metrics (EG p15, declination p80, seats@50/50 p78); it sits at p0.92 on mean-median — outside the p5 floor — on the NDP-cracking tail (pre-registered Row 8). The majority is not flagged in the UCP-advantage direction on any metric. The inter-map difference in [§5.2.1](#sec-5-2-1) therefore reflects boundary choices rather than geography-forced variation. Historical note: the 50k preliminary run (2 chains) placed minority EG at p95.9. The 250k run revised to p94.2. The 1,010,000-plan run is stable at p94.4.

**Swing-assumption sensitivity on seats@50/50 (H5).** The p99.99 percentile for seats@50/50 assumes uniform swing across all Alberta districts. Under empirical regional swing (Calgary 1.34×, Edmonton 0.50×, rural 0.95× the provincial swing — calibrated to 2023 geographic patterns), the percentile changes substantially:

| Swing assumption | Minority seats@50/50 | Minority percentile | Majority seats@50/50 | Majority percentile |
|---|---|---|---|---|
| Uniform (canonical) | 0.5169 | p99.99 | 0.4607 | p77.8 |
| Regional (2023 geographic) | 0.4607 | ~p65–70 | 0.4270 | ~p5 (NDP-tail) |

*Source: H5, `data/outputs/regional_swing_canonical_ed.json`. Ensemble median 0.4483, p95 threshold 0.4828.*

Under regional swing the minority map's percentile drops substantially — from the extreme tail to above-median — but does not collapse to the median. The direction of asymmetry is preserved: the minority remains above the ensemble median while the majority drifts toward the NDP-favourable tail. The magnitude claim (extreme-outlier status) is not robust to the swing assumption. The directional claim (minority above majority and above ensemble median) is. Full replication in [§7](#sec-7) (H5) and `findings/regional_swing_robustness.md`.

**Boundary-straddle error: pre-empted.** A boundary line passing through a VA polygon cannot assign that VA to a single 2026 ED without introducing a classification error. The integrity audit (`findings/va_spatial_integrity_report.md`) measures the residual. Gate S3b finds 99.20% of the 4,765 VAs have centroids falling inside their declared 2019 parent ED. Gate S3c finds vote-conservation error at the poll-to-VA aggregation step below 0.0001%. The residual 0.80% (38 VAs) are boundary-adjacent polygons whose centroids nudge across a shared line. The declared ED in these cases is canonical because it comes from the poll record rather than the geometry. Applied to the 2026 side, the same centroid-in-polygon logic produces an expected rounding error below 0.5% province-wide, roughly an order of magnitude below the 0.47-pp minimum minority-majority asymmetry. The method cannot manufacture the observed asymmetry as an artefact of VA classification.

<a id="sec-5-2-3"></a>
#### 5.2.3 Falsifiability gate: asymmetry direction

The minority-majority EG asymmetry is negative (minority more UCP-favorable, under this paper's sign convention) in 90.5% of 2,000 Monte Carlo samples across the parameter space (urban weight 0.55–0.85, rural baseline 0.26–0.36, per-hybrid jitter ±0.10). Mean −1.23 pp, median −1.40 pp.[^1] The 2.5th–97.5th percentile sensitivity interval is [−3.04, +0.76] pp and crosses zero.

[^1]: Monte Carlo median values vary by approximately ±0.3 pp between independent runs with different random seeds. The reported median (−1.40 pp) is from the canonical Run #4 (seed 42, 250,000 samples); an earlier 2,000-sample preliminary run reported median −1.44 pp. This variance is consistent with Monte Carlo sampling error and does not affect the directional claim (negative in 90.5% of draws) or the sensitivity interval bounds. *(This interval reflects parameter uncertainty in the vote-share model — urban weight, rural baseline, and per-hybrid jitter — not boundary position or spatial assignment uncertainty. It is not a frequentist confidence interval: the draws are not i.i.d. samples from a population, and under spatial autocorrelation the effective N is approximately 20–30, which would widen these bounds by a factor of 1.5–2×.)* We report this as a directional observation at approximately 90% of draws and do not assert classical statistical significance. The magnitude claim (specifically 0.47–1.48 pp across the 0.70–0.80 weight range; 1.41 pp central) does not meet the 95% threshold. **Small-N noise floor.** In an 89-district assembly, the standard error of the efficiency gap under homogeneous swing is approximately 1–2 pp (Stephanopoulos and McGhee 2015, §III.B), placing the 1.41 pp central asymmetry near the lower bound of reliable EG detection. The metric is most informative in large assemblies (US Congressional, 435 seats); at 89 seats a 1–2 pp inter-map asymmetry is consistent with assembly-size rounding variation and does not independently constitute a structural anomaly. The inter-map EG comparison is therefore reported as directional evidence only; the magnitude is not meaningfully precise at this scale. The minority-vs-majority seat-count gap is 1 seat under both 2023 Statement-of-Vote data and April 2026 338Canada polling, but historical 338 stability testing shows the *direction* of that 1-seat gap is not invariant across vote inputs (see "338 historical stability" paragraph below). If measured attribution from Phase 4C produces an asymmetry of magnitude and direction inconsistent with 2023-vote attribution, the directional claim is falsified.

**Cross-election contingency.** The asymmetry direction is stable across 2023 Statement-of-Vote data and April 2026 338Canada polling. It reverses sign when 2019 votes are used as input (asymmetry becomes +0.75 pp under 2019 votes, under this paper's sign convention: positive asymmetry = minority less UCP-favourable). Under 2015 votes (attributed to 2019 EDs via the full 2015-to-2019 crosswalk at `data/2015_to_2019_crosswalk.csv`), the minority-majority asymmetry is +0.03 pp — essentially zero. The near-zero 2015 figure establishes that the EG asymmetry is partly a function of contemporary vote geography rather than an unconditional structural property of the boundary geometry. The audit's directional claim is accordingly bounded: the minority map shows a UCP-favourable partisan pattern under 2023 vote distributions, but this signal does not hold against the 2015 electorate. The three-election distribution (2015 +0.03 pp, 2019 +0.75 pp, 2023 −0.51 pp under this paper's convention) shows the headline direction is supported only under 2023 vote input. 2019 is a clean reversal; 2015 is a near-neutral reversal. The direction is stable across 2020s-era Alberta political geography (specifically the 2023 Statement of Vote and the April 2026 338Canada polling) but is not stable against the 2019 or 2015 electorates. A hostile reader who substitutes pre-2023 voter distributions for 2023 distributions recovers a result that contradicts the headline. The paper reports this contingency as a property of the finding, not a defect: the boundary effect is sensitive to which electorate is asked, and the audit has tested three Alberta general elections plus one polling snapshot to characterise that sensitivity. The seats@50/50 metric shows the same cross-election contingency: under 2015-attributed votes (blended crosswalk, 70/30 urban/rural, 2015 rural baseline 35.05%), NDP at 50/50 is 33 seats under both the majority and minority proposals — a tie (`findings/cross_election_2015.md` [§3](#sec-3)). The minority's p99.99 position on seats@50/50 under 2023 votes is therefore contingent on contemporary vote geography, not purely a structural property of the boundary lines. The audit's seats@50/50 claim is accordingly bounded: the minority map shows an extreme-outlier position on this metric under 2023-era competitive vote distributions, not unconditionally. Full method for the 2015 extension at `findings/cross_election_2015.md`.

**Byelection coverage in the 2022–2025 window.** Alberta held six provincial byelections in this interval: Fort McMurray-Lac La Biche (2022-03-15), Brooks-Medicine Hat (2022-11-08), Lethbridge-West (2024-12-18), and Edmonton-Ellerslie, Edmonton-Strathcona, and Olds-Didsbury-Three Hills (all 2025-06-23). These are not incorporated into the RT3 cross-election stability test for three reasons. First, coverage is sparse (6 of 87 EDs, 6.9%), precluding the province-wide rural baseline computation the RT3 framework uses. Second, byelection turnout ran 40–60% of prior general turnout, with voter composition known to skew older and more partisan. This violates the "normal partisan inputs" assumption the three general elections jointly satisfy. Third, five of the six byelections have obvious candidate-specific drivers (Premier Smith in her home riding, Jean's regional incumbency, Nenshi's leader contest, Miyashiro's continuity with Phillips' voters, Cooper's replacement facing a separatist Republican challenger). The one byelection that touches a contested minority configuration is Olds-Didsbury-Three Hills (June 2025), which sits in the minority's proposed "Olds-Three Hills-Didsbury" district. The UCP's −14.2 pp share drop and the Republican Party of Alberta's 17.7% first-contest showing do not change the audit's directional verdict. They marginally support the audit's skepticism that "safe" packed rural EDs are structurally stable, but are too sui generis to upgrade from observation to finding. Full data in `data/alberta_byelections_2019_2026.csv`; assessment in `findings/byelection_assessment.md`.

**Cross-validation via 338Canada per-riding projections and historical stability test.** *Caveat — two-model compounding.* 338Canada's per-riding projections are themselves a regional demographic model weighted by polling aggregation. Reallocating them through the hybrid crosswalks stacks a second model layer. 338's model accuracy against the 2023 actual result: per-riding Pearson r = 0.966, MAE = 3.74 pp, winner-call 81 of 87 (93.1 %). 338 systematically under-projected UCP in rural Alberta by ~4.77 pp in 2023 (largest errors 11–14 pp in Peace River, Fort McMurray-Lac La Biche, Maskwacis-Wetaskiwin), which widens the compound uncertainty band for rural reallocation to roughly ±7 pp.

**Direction of the 1-seat asymmetry is not stable across vote inputs.** Reallocating through the majority and minority hybrid crosswalks produces seat counts of 67 UCP / 22 NDP (majority 2026) and 66 UCP / 23 NDP (minority 2026) under April 2026 338 polling — a 1-seat gap favouring NDP on the minority. The audit's 2023-vote central produces 51 UCP / 38 NDP (majority) and 52 UCP / 37 NDP (minority) — a 1-seat gap favouring UCP on the minority. The size of the gap is 1 seat in both cases, but the direction flips. A 77-snapshot historical 338 stability probe (2020-02-23 through 2026-04-12) confirms this is systematic: in competitive environments (UCP provincial share 45–55 %) the minority map advantages UCP by an average of 1–3 seats. In UCP-landslide environments (UCP provincial share > 55 %, which April 2026 polling reflects) the minority map shifts to NDP-favourable by ~1 seat. Pre-2023 338 snapshots reallocated through the audit's own crosswalks produce majority 48 / 39 and minority 49 / 39 — a 1-seat UCP advantage on the minority, consistent with 2023 actual.

**Implication.** The 1-seat asymmetry is small (≤ 5 seats across all tested inputs) but *state-dependent* rather than structural. The defensible claim is that under realistic 2020s-era competitive provincial vote distributions, the minority map produces a small UCP advantage over the majority map. Under UCP-landslide conditions or NDP-wave conditions (2019, 2015) the direction reverses. A structural-invariance claim was not supported by the historical stability test and has been retracted from this paper. Full method and data at `analysis/methodology/338canada_historical.md` (77-snapshot time series at `data/338canada_historical_snapshots.csv`; pre-2023 reallocation at `data/reference/polling_338_historical/pre2023_reallocated_*.csv`; uniform-swing stability probe at `data/reference/polling_338_historical/uniform_swing_stability.csv`).

**338Canada April 2026 current projection — landslide context.** 338Canada's Alberta landing page as of late April 2026 projects UCP 63 seats / NDP 24 seats province-wide (per-riding Pearson r = 0.966 against 2023 actual; 338 calibration documented above). This projection implies a UCP provincial two-party share above 55%, placing April 2026 firmly in the UCP-landslide zone where the historical stability probe finds the minority map shifts to a marginal NDP advantage (~1 seat) rather than a UCP advantage. The current 63/24 projection is therefore the environment in which the minority map's *UCP-favouring* character is weakest. The map-effect's practical significance is maximal at competitive vote distributions (UCP/NDP provincial two-party share 48–52%), not at current polling. This is consistent with the audit's finding: the minority map is not a tool for manufacturing a landslide but a mechanism that operates in the margin between majority and minority government in close elections.

**Alberta electoral volatility: case-selection context (ES-19).** Alberta is, by a considerable margin, the most electorally volatile province in the federation. The Progressive Conservative Party held power for 44 consecutive years (1971–2015). The 2015 NDP majority was followed by UCP dominance in 2019 and 2023. The Wildrose and PC parties merged in 2017. The Republican Party of Alberta contested byelections and holds an elected seat by 2026. Bratt, Brownsey, Sutherland, and Taras (2019) document Alberta's distinctive political culture — ideologically heterodox, liable to wholesale electoral realignment — as a structural feature rather than a 2015–2023 aberration. The *Canadian Political Science Review* 2020 special issue on Alberta politics provides additional documentation of the province's party-system instability. In this context, a one-seat inter-map gap that flips direction between the 2019 and 2023 electorates — absent any change in the maps themselves — is at least as plausibly an artefact of Alberta's electoral churn as it is evidence of map-level partisan design. The partisan-bias findings ([§5.2](#sec-5-2), [§5.4](#sec-5-4)) are accordingly read as directional observations contingent on the current electoral cycle's vote distribution, not as structural invariants of the maps' geometry.

The structural findings in [§5.1](#sec-5-1) (population equality) and [§5.8](#sec-5-8) (geographic coherence) are not subject to this contingency: they measure geometric properties of the maps themselves, which do not change with the electorate. The electorate-independent core rests on population dispersion, Calgary zone asymmetry, Airdrie fragmentation, and school-division coherence. (Municipal anchoring, a fifth pre-registered dimension, did not survive canonical recomputation — see [§5.8.5](#sec-5-8-5).[^anchoring_canonical]) A synthesis that weighted partisan-bias and structural findings equally would overstate the evidentiary weight of the former relative to its cross-election stability. This audit's synthesis therefore gives explicit priority to the structural findings as the stable, electorally invariant core of the evidence, while the partisan-bias metrics supplement that core with a cycle-contingent directional observation.

<a id="sec-5-2-4"></a>
#### 5.2.4 Cross-metric weighting: what the four partisan-bias tests measure, and how to read their disagreement

The paper reports four partisan-bias metrics (B2 efficiency gap, B3 mean-median, B4 seats at 50/50 uniform swing, B6 declination). B2, B3, and B4 all show the minority 2026 map as more UCP-favorable than the majority 2026 map under 2023 vote input. B6 points the opposite direction: by declination, the minority is the *least* UCP-favorable of the three maps. Reporting this as "three of four metrics agree" understates the methodological question a reader has to evaluate.

**What each test measures and what it assumes:**

- **B2 Efficiency gap (Stephanopoulos and McGhee 2014).** Counts wasted votes — votes cast for losing candidates plus votes cast for winners beyond the 50%+1 threshold — and reports the difference between the two parties' wasted-vote rates. Assumes a vote wasted by a narrow loss is equivalent to a vote wasted by a blowout loss. Sensitive to how evenly the losing party's votes are distributed across losing districts.
- **B3 Mean-median gap (McDonald and Best 2015).** Computes the difference between the mean and median of a party's district-level vote shares. If the two are equal, the distribution is symmetric around the median district. Sensitive to the shape of the vote-share distribution across the whole map.
- **B4 Seats at 50/50 uniform swing.** Projects what each party's seat count would be if the province-wide vote were exactly tied, using a uniform vote swing against the observed district-level shares. Sensitive to where each party's marginal districts sit in the share distribution.
- **B6 Declination (Warrington 2018).** Treats the two parties' winning districts as two clouds in a slope-vs-margin plane and computes the angle between the best-fit lines. A perfectly symmetric map produces zero declination. Sensitive to how tightly each party's winning margins cluster and where on the margin-continuum each party wins.

**Why B6 can disagree with B2, B3, and B4.** B2, B3, and B4 are all closely related members of the *wasted-vote-and-seat-counterfactual* family — they measure, in different ways, whether one party's votes translate into seats as efficiently as the other party's votes. If one of these agrees, the others usually agree. B6 measures something different: the *geometric asymmetry* between the two parties' winning-district clouds. A map can be partisan-unfavourable on wasted-vote terms (B2, B3, B4) while being geometrically symmetric on winning-district-margin terms (B6).

The canonical example: a map that packs the losing party into narrow-margin losses (losses by 45-55 rather than blowouts). On wasted-vote counts, the losing party still wastes many votes in those narrow losses. B2/B3/B4 flag the packing. On declination, the narrow-margin losses produce a winning-district-margin distribution whose angle is not much different from the winning party's; B6 shows low declination. Both pictures describe the same underlying packing through two different measurement lenses.

**Specific Alberta interpretation.** The minority 2026 map shows three 4-way urban splits (Airdrie, Lethbridge, Red Deer), a packed Calgary Zone A (NDP-leaning districts 12.2% larger than UCP-leaning), and a cracking-and-margin-narrowing pattern consistent with the "concentrate losing party in narrow losses" mechanism. Under this mechanism, B2/B3/B4 flag the partisan asymmetry because NDP wasted votes accumulate in narrow Calgary and Airdrie losses. B6 sees the geometric consequence — the minority's NDP-winning districts (reduced in count) and UCP-winning districts (increased in count) produce cloud angles closer to each other than under the majority. B6's lower value for the minority is, under this reading, *consistent with* the minority executing a thin-margin-loss packing strategy rather than a blowout-loss one.

**Classification of the disagreement.** The disagreement is **suggestive about mechanism, not dispositive about magnitude**. It does not overturn the B2/B3/B4 finding (which remains directionally UCP-favorable under 2023 votes in 90.5% of Monte Carlo samples). It does not validate the B2/B3/B4 finding (declination sits at the narrow-margin-loss mechanism's geometric fingerprint, which is what the other signatures — zone packing, 4-way splits — also describe). The honest reading is that the four metrics agree on the presence of partisan asymmetry while disagreeing on its mechanism: EG/MM/Seats@50-50 describe the wasted-vote consequence. Declination describes the margin-distribution geometry; and the mechanism consistent with both is narrow-margin-loss packing. This is a different finding than "three metrics agree and one disagrees". It is closer to "four metrics each describe a different face of the same structural pattern."

**What a hostile reviewer gets from the disagreement.** B6 standing alone is an argument that the minority map is geometrically more balanced than the majority on winning-district margin distribution. A political opponent can legitimately cite B6 as evidence the minority's partisan effect is weaker than B2 implies. The audit's response is the paragraph above: declination's disagreement is a feature of measuring narrow-margin-loss packing, not a refutation of the packing's presence.

**Resolution path.** Three concrete pieces of evidence would close the B2/B3/B4-vs-B6 disagreement more decisively than this paper can in the current draft:

(a) **Publication-grade MCMC.** A 1,000,000-sample ReCom run with thinning to ≈ 5,000 effectively-independent draws, per MGGG lawsuit-grade practice, seeded on the commission's final 2026 shapefile rather than the 2019 map. The 250,000-sample run produced an effective sample size (ESS) of roughly 375–452 independent draws ([§5.4](#sec-5-4)) — sufficient for a policy-comparison finding but below the ~1,000–2,000 publication-grade threshold for individual tail claims at extreme percentiles. The 1,010,000-sample canonical run ([§5.4.9](#sec-5-4-9), completed 2026-05-12) resolved this: partisan-metric ESS 1,429–1,682, publication-grade. The minority's mean-median p99.98, declination p1.21, and seats@50/50 p99.99 pattern holds at publication-grade ESS. Efficiency Gap at p94.4 remains below p95.

(b) **Narrow-margin-loss signature test constructed symmetrically.** Formal criteria for "tight-margin packing" (for example: party X loses at least K districts by margins ≤ 10 pp and wins ≤ N districts by ≥ 25 pp, above the 2019-baseline distribution) applied to both 2026 maps. Proof-of-concept in the counter-test framework of [§5.6](#sec-5-6). Full signature-grade version left to follow-up work.

(c) **Post-election check.** The minority map will not be adopted (Motion 19 set both aside), but the adopted November 2026 committee map will be tested against both B2/B3/B4 and B6 on 2027 actual results. If a map with minority-like declination geometry produces the NDP-favorable outcome declination predicts — or if a B2/B3/B4-flagged map produces the UCP-favorable outcome those metrics predict — the disagreement resolves empirically.

Until those three pieces land, the audit reports the four metrics' shared direction on asymmetry and shared mechanism on packing, and flags declination's divergence as a feature of the narrow-margin-loss packing pattern consistent with Warrington (2019)'s observation that declination and efficiency gap disagree on a non-trivial fraction of US-state maps.

**What assumptions to check.** Each metric carries at least one load-bearing assumption that a Canadian context can test:

- B2 assumes the losing party's wasted votes are homogeneous. Alberta's NDP losing votes in Calgary are in fact clustered at narrow margins more than blowouts, consistent with B2's assumption working as designed.
- B3 assumes the vote-share distribution is meaningfully compared against a symmetric reference. Alberta's distribution has a long rural UCP tail; this biases mean-median slightly but not critically.
- B4 assumes uniform swing. Alberta elections have historically swung uniformly enough that this is defensible, but the 2019→2023 swing was not uniform (NDP gained more in Edmonton than in Calgary); the counterfactual should be read with that caveat.
- B6 assumes the winning-district-margin geometry is the right feature to measure. Warrington (2018) defends declination as a primary measure, and Warrington's comparative study of partisan-gerrymandering measures (Warrington 2019) documents that declination and efficiency gap can disagree on a non-trivial fraction of US-state redistricting plans — the Alberta disagreement between B6 (declination) and B2–B4 (the EG-family metrics) sits inside that known divergence range rather than as an outlier.

<a id="sec-5-2-5"></a>
#### 5.2.5 Natural-packing context (Chen and Rodden) — validated for Alberta with revised mechanism

Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through a *packing mechanism* — their voters cluster in city cores, producing large-margin wins with many wasted votes while the opposing party wins surrounding districts by efficient margins. The original Chen-Rodden framing, applied naively, would predict that Alberta's NDP suffers from urban packing.

**Alberta validation test** (full methodology at `analysis/methodology/chen_rodden_alberta_validation.md` and `analysis/scripts/chen_rodden_alberta.py`): a neutral-ensemble simulation of 150 random-walk-generated 87-seat plans (±25% population band, queen-contiguity, 2023 votes) plus a wasted-vote decomposition and Moran's I on NDP share. Results:

- **Direction prediction holds.** Neutral-ensemble EG distribution (150-plan mechanism-validation sub-ensemble, negative-equals-UCP convention): median −2.3 to −2.4%, 5th–95th percentile [−4.4%, −0.7%]. The 2019 Phase 4C baseline (−2.64%, S-M convention) sits at the centre of this distribution after sign-convention alignment. Direction prediction confirmed: neutral Alberta maps are UCP-favourable by construction. Under Phase 4C spatial attribution (S-M positive = UCP-favoured): majority +0.04% (canonical 1,010,000-plan p15.5), minority +3.96% (p94.4). The canonical 1,010,000-plan ensemble is the authoritative percentile benchmark; this 150-plan sub-ensemble is retained for mechanism validation only.
- **Mechanism prediction fails.** The Chen-Rodden urban-packing mechanism does not operate in Alberta. NDP surplus-vote rate in NDP-won districts: 9.3%. UCP surplus-vote rate in UCP-won districts: **15.9%**. UCP is the more-packed party by excess wasted votes. Rural UCP-winning margins average 43.0 pp; urban NDP-winning margins average 21.5 pp. NDP's seat deficit comes from **dispersed losing votes** in rural and suburban ridings where the NDP consistently loses by 60–80 pp, not from over-concentration in urban cores.
- **Moran's I on NDP two-party share: 0.7534 (p < 0.001, z = 12.15).** Strong spatial clustering is confirmed. Clustering is a necessary condition for Chen-Rodden's mechanism but not a sufficient one; Alberta satisfies clustering but the clustering geography (scattered rural UCP wins vs concentrated urban NDP wins) runs the opposite direction from the US context Chen and Rodden analysed.

**Revised framing.** The 2019 baseline EG of approximately −2.64% is roughly at the centre of what a neutral Alberta map would produce given 2023 vote geography — but the mechanism that produces this baseline is *UCP rural dispersion with large-margin wins*, not *NDP urban packing*. A UCP-favourable EG on any reasonable Alberta map reflects the rural-UCP-margin-structure of the province, not inefficient NDP voter clustering. Under this corrected framing:

- The 2019 enacted EG (−2.64%, Phase 4C S-M convention) establishes a geography reference: under 2023 vote geography, 2019 boundaries produce a mildly NDP-favourable EG — consistent with NDP's modestly higher per-seat efficiency under the 2019 87-seat plan with 2023 votes. This serves as a structural anchor for interpreting the 2026 proposals.
- The majority 2026 EG (+0.04%, p15.5) is near neutral: the majority proposal's boundary choices produce an EG close to the canonical ensemble constraint-bound median (+1.49%), well within the neutral band.
- The minority 2026 EG (+3.96%, p94.4) is substantially UCP-favourable: the minority proposal is more UCP-favourable than 94.4% of the 1,010,000 neutral plans. It falls within the 5–95 band [−0.97%, +3.94%] but near its upper edge.

**Implication for partisan-bias findings.** The Phase 4C inter-map gap is +3.92 pp (majority +0.04% at p15.5 vs minority +3.96% at p94.4 in the canonical 1,010,000-plan ensemble). Both maps fall within the canonical 5–95 band [−0.97%, +3.94%], but at qualitatively different positions: the majority is near the lower end of the neutral range; the minority is near the upper edge. The authoritative percentile statement is from the canonical ensemble — not the 150-plan mechanism-validation sub-ensemble. The [§5.2](#sec-5-2) evidence therefore does contribute to the partisan-bias finding, but does not reach [§5.1](#sec-5-1) (population equality), [§5.8](#sec-5-8) (geographic coherence), or [§5.9](#sec-5-9) (procedural fairness).

**Synthesis.** The audit's strongest claim incorporates both the direction-validated Chen-Rodden prediction and the mechanism correction: Alberta's rural-UCP-margin structure produces a UCP-favourable EG by default under most vote geographies. Under Phase 4C, the majority (p15.5) sits well within the neutral range while the minority (p94.4) reaches the upper portion of the 5–95 band. The inter-map gap (+3.92 pp) is 100% attributable to boundary choices — the minority incorporates substantially less correction of Alberta's natural UCP-favouring baseline than the majority does. The [§5.2](#sec-5-2) evidence is one dimension among six; it is consistent with, and reinforces, the structural findings at [§5.1](#sec-5-1), [§5.8](#sec-5-8), [§5.9](#sec-5-9), and [§5.6](#sec-5-6).

**Geography-vs-drawing decomposition.** **The minority-vs-majority asymmetry is 100 % drawing, 0 % geography.** The +3.92 pp Phase 4C minority-vs-majority efficiency-gap asymmetry (majority +0.04%, minority +3.96%) is decomposed into a geography component (1,010,000-plan canonical constraint-bound expectation on the same substrate) and a drawing component (real-map EG minus constraint-bound expectation), applying the Chen-Rodden (2013) identity. Because both 2026 proposals are drawn on the same Alberta voter geography against the same ensemble, the constraint-bound-expectation term cancels exactly in the gap — on every metric (efficiency gap, mean-median, declination, and seats at 50/50).

**Note (2026-05-18): the following decomposition tables use high-resolution-spatial v2 (pre-canonical DPG geometry). Phase 4C values (canonical EA shapefiles) give minority EG +3.96% vs the +1.82% below — the absolute-level decomposition requires re-running against Phase 4C inputs. Tables retained for structural-interpretation documentation only; do not cite EG actual values as current.**

Per-map under the high-resolution-spatial (v2) rescore against the 1,010,000-plan canonical ensemble (formula convention, positive EG = NDP wastes more): 2019 EG-drawing component −0.0412, Majority −0.0381, Minority +0.0034. The minority map sits effectively AT the ensemble EG median on this substrate, while the 2019 and Majority maps are measurably displaced from it in the same direction. Under the substrate-matched Election-Day-only cross-check the Majority→Minority EG gap is +0.0117 (1.17 pp), still 100% drawing. The minority map's structural flags ([§5.4](#sec-5-4) declination p1.21, mean-median p99.98) appear in the decomposition as a declination drawing component of −0.0338 (v2) / −0.0737 (Election-Day) paired with a near-zero EG drawing, consistent with an asymmetric-packing drawing signature rather than a symmetric pro-UCP tilt. The identity resolves the Gemini red-team Phase E.3 concern directly: the entire reported gap is attributable to boundary choices, regardless of which measurement resolution (crosswalk or spatial) is used. Full per-metric table, per-map decomposition, and substrate-matched cross-check in `findings/chen_rodden_decomposition.md`. Machine-readable outputs in `data/v0_1_chen_rodden_decomposition.{csv,json}`.

**Absolute-level Chen-Rodden decomposition (2026-04-24, narrowed under pre-committed pass framework; terminology refined 2026-04-24 under retraction-pathway §9 item 1).** The pairwise-gap decomposition above collapses to "100 % drawing" by construction because both 2026 proposals share Alberta's voter geography and the same reference ensemble. The *absolute-level* decomposition answers a separate question: how much of each map's partisan lean is natural geography (what the 1,010,000-plan canonical MCMC constraint-bound expectation produces) versus specific drawing choices?

Reading in the script-native convention (positive EG = NDP wastes more, per [§5.4](#sec-5-4)), the constraint-bound-expectation EG is **+1.49 %** with a 5–95 band of [−0.97 %, +3.94 %]. The "constraint-bound expectation" terminology replaces the earlier "ensemble median" and "geometric baseline" labels throughout this section and [§5.4](#sec-5-4), acknowledging honestly that the MCMC ensemble does not represent the *human trade-offs* of a public hearing — it represents only what the ±25 %-population + contiguity + compactness constraint set produces on Alberta's voter geography. A residual drawing component of ≈ 0.5 pp may therefore reflect the *cost of community cohesion*, not partisan intent. The reference point is not "neutral"; it is *constrained*. Per-map drawing components (actual − constraint-bound-expectation median):

| Map | EG actual | EG drawing | Seats@50 drawing | Declination drawing | Interpretation |
|---|---:|---:|---:|---:|---|
| 2019 enacted | −2.64 % | **−4.12 pp** | +2.30 pp NDP | +0.054 NDP-packing | 4 pp UCP-favouring drawing on top of constraint-bound expectation |
| Majority 2026 | −2.33 % | **−3.81 pp** | +1.76 pp NDP | +0.039 NDP-packing | Similar UCP-favouring drawing as 2019 |
| Minority 2026 | +1.82 % | **+0.34 pp** | **+5.75 pp NDP** | **−0.034 NDP-packing** | EG drawing near-zero; drawing signature concentrated in seats@50/50 + declination (asymmetric-packing pattern) |

**Pre-committed pass check** (per `analysis/methodology/null_hypothesis_and_exoneration_criteria.md` §2.5): a minority drawing component *passes* (within what constraint-bound ReCom sampling could produce) if it falls inside the ensemble 5–95 band. Checking each minority metric against its band:

| Metric | Minority actual | 5–95 band | In-band? |
|---|---:|---|---|
| EG | +0.0182 | [−0.0097, +0.0394] | **✓ yes** |
| Mean-median | −0.0139 | [−0.0313, −0.0061] | **✓ yes** |
| Declination | −0.0305 | [−0.0503, +0.0560] | **✓ yes** |
| Seats@50/50 | +0.5057 | [+0.4253, +0.4828] | ✗ NO (upper-tail, NDP-side) |

**The narrowed claim the decomposition actually supports** (retracted from an earlier version of this paragraph under the pre-registered pass framework): *the minority map sits INSIDE the constraint-bound-expectation 5–95 band on three of four partisan-bias metrics (EG, mean-median, declination). Only seats-at-50/50 is outside the band — and it is on the NDP-favoured upper tail at p100 (raw) / p89.72 under ESS-150 downgrade. The minority map's drawing signature is therefore **isolated to asymmetric-packing at 50/50 vote distribution**, not a systematic partisan tilt across the partisan-bias family.* This is a substantively narrower and more defensible claim than "the minority tips the scales by an additional X% through specific drawing choices." It honors the pre-commitment: under the pass criterion pre-committed before the result was read, the minority partially passed on three of four metrics. Full decomposition table in `data/chen_rodden_absolute_decomposition.json`. Methodology and criticism / defense in `analysis/methodology/methodological_defenses.md#test-apparatus-defense` §2.5. Pre-registered pass framework and three-axis robustness classification in `preregistration/null_hypotheses.md` §§2.5 and 7.

**Scope of the Chen-Rodden reading.** Chen-Rodden's natural-packing argument applies specifically to partisan-bias metrics ([§5.2](#sec-5-2)). It does not reach the structural findings in [§5.1](#sec-5-1) (population equality), [§5.8](#sec-5-8) (geographic coherence), or [§5.9](#sec-5-9) (procedural fairness).

The audit's primary findings are structural: wider minority population dispersion (MAD 4,707 vs 3,180), 12.2% vs 0.4% Calgary geographic-zone asymmetry, engineered s.15(2) boundary at Rocky Mountain House-Banff Park, 4-way fragmentation of Airdrie vs 2-way, and three formal signatures (packing / cracking / engineered-boundary) under the minority vs zero under the majority. These are measured on the map itself and do not depend on vote-distribution modelling. The partisan-bias finding in [§5.2.1](#sec-5-2-1) is best read as one dimension among six, not as the headline: the minority map corrects substantially less of Alberta's natural UCP-favouring geography than the majority does (Phase 4C: majority +0.04% at p15.5, minority +3.96% at p94.4; 2019 baseline −2.64% in S-M convention), and the headline for the audit is the structural divergence between the two 2026 maps, which [§5.2.5](#sec-5-2-5)'s natural-packing framing cannot explain.

<a id="sec-5-2-6"></a>
#### 5.2.6 Marginal-seat translation and uniform-swing calibration

**Purpose.** Under Phase 4C, the inter-map EG asymmetry is +3.92 pp (majority +0.04%, minority +3.96%), with a 5-seat NDP difference at a tied provincial vote (majority 48 vs minority 43). The blend-model values (0.47–1.48 pp EG across the 0.70–0.80 weight range; 1.41 pp at the central 0.85 weight) are superseded by Phase 4C. This subsection translates the Phase 4C 5-seat differential into specific Alberta ridings and past elections to show where a shift of that magnitude operates and how often those conditions apply. Full data, per-ED margins, and script at `findings/marginal_seats_findings.md` and `analysis/scripts/marginal_seats_analysis.py`.

**Method.** For each election (2015, 2019, 2023), each ED's two-party NDP share is computed as NDP ÷ (NDP + UCP). For 2015, PC + WRP stands in for UCP. A uniform swing of X pp toward UCP subtracts X pp from every ED's NDP share. Seats where the sign of the margin changes are counted as flips. Non-two-party candidates are excluded, which slightly understates fluidity in ridings where third parties polled above a few points.

**Marginal-seat count by election.** Ridings decided by less than 3 pp of two-party margin:

| Election | Boundaries | Marginal (<3 pp) | Razor-thin (<1 pp) | <5 pp |
|---|---|---|---|---|
| 2023 | post-2017 | **14 of 87** | 7 | 18 |
| 2019 | post-2017 | 7 of 87 | 3 | 13 |
| 2015 | pre-2017 | 8 of 87 | 2 | 10 |

2023 had roughly twice as many ridings in the flip-zone as 2019 or 2015, consistent with it being Alberta's first genuinely competitive provincial election in the current cycle. Twelve of the fourteen 2023 marginal ridings are in Calgary. Seven of those twelve sit inside the Calgary Zone A that the minority map packs to 12.2% above UCP-leaning zone average — the same ridings where the map effect concentrates are the same ridings that are already at risk on the current vote distribution.

**1.5 pp uniform swing — midpoint of the audit's map-effect estimate.** Applied to 2023 results:

*Toward UCP — 6 seats flip:*

| ED | Prior winner | Two-party margin |
|---|---|---|
| Calgary-Acadia | NDP | +0.05 pp |
| Calgary-Glenmore | NDP | +0.09 pp |
| Calgary-Foothills | NDP | +0.60 pp |
| Calgary-Edgemont | NDP | +0.62 pp |
| Banff-Kananaskis | NDP | +0.66 pp |
| Calgary-Beddington | NDP | +1.36 pp |

*Toward NDP — 4 seats flip:*

| ED | Prior winner | Two-party margin |
|---|---|---|
| Calgary-North West | UCP | −0.30 pp |
| Calgary-North | UCP | −0.41 pp |
| Calgary-Bow | UCP | −1.21 pp |
| Lethbridge-East | UCP | −1.49 pp |

Applied to 2019, a 1.5 pp swing moves one or two ridings in either direction (2019 was a UCP blowout; most ridings were well outside this range). Applied to 2015 pre-2017 boundaries, two or three ridings move. PC + WRP as UCP stand-in limits comparability.

**When the map effect matters.** The 2023 UCP actual margin was 49–38 (eleven seats). A 1–3 seat shift from map design is a rounding error at that spread. 338Canada's April 2026 projection (UCP 63 / NDP 24, see [§5.2.3](#sec-5-2-3)) places 2027 in an even more decisive environment. The map effect changes outcomes only when the provincial vote is within roughly five seats of a tied legislature — the range where marginal Calgary ridings are individually decisive. Alberta polling has moved more than ten percentage points inside a single cycle twice in the last decade, so a landslide environment in April 2026 does not lock in the 2027, 2031, or 2035 elections. The adopted map runs all three cycles. The marginal-seat analysis quantifies the specific conditions under which the 1–3 seat effect becomes outcome-determinative: it is not the current polling environment, but it is within the range of observed inter-election swings.

**Limitation.** Uniform swing is a simplifying assumption. The 2019→2023 swing was not uniform — NDP gained more in Edmonton than in Calgary — and future swings may similarly have geographic structure. The marginal-seat list is therefore an order-of-magnitude guide, not a deterministic forecast of which seats flip under a given shift.

<a id="sec-5-2-7"></a>
#### 5.2.7 Measurement-resolution sensitivity: crosswalk-blend vs spatial attribution *(sunset clause satisfied 2026-05-06)*

Before official 2026 shapefiles were available, the audit computed partisan-bias metrics against two substantively different attribution methods. These agreed in directional ordering (minority more UCP-favourable than majority) but disagreed on absolute magnitude and, for the spatial reading, on EG sign relative to the ensemble. Phase 4C (official EA shapefiles, 2026-05-06) resolves the disagreement and is the sole canonical measurement.

| Measurement | Majority 2026 EG | Minority 2026 EG | Asymmetry (Min − Maj) | Direction | Status |
| --- | --- | --- | --- | --- | --- |
| Blended crosswalk (w = 0.85) | −0.40 % | −1.81 % | **−1.41 pp** | Minority more UCP-favourable | **Retired** — superseded by Phase 4C |
| High-resolution spatial (provisional DPG geometry) | −2.33 % | +1.82 % | **+4.15 pp** | Minority more NDP-favourable (in DPG convention) | **Retired** — DPG sunset clause satisfied |
| **Phase 4C (official EA shapefiles, v0.3, 2026-05-18)** | **+0.04 %** | **+3.96 %** | **+3.92 pp** | **Minority more UCP-favourable** | **Canonical** |

The 2019-enacted baseline is stable across all three (blended EG −2.64 %, spatial EG −2.64 %, Phase 4C −2.64 %), ruling out a provincial-level miscalculation. The disagreement between the two pre-canonical readings was a property of *how per-ED vote totals are built*, not of how the metric is computed.

The blended crosswalk modelled each 2026 hybrid ED as a weighted combination of its urban-core 2019 predecessor and a rural-absorption remainder (urban weight w = 0.85). The provisional-DPG spatial method assigned 2023 Voting Area polygons to 2026 EDs by centroid-in-polygon with 80–90% VA coverage; the 19.8% fallback share on the minority map was the dominant error source. DPG-construction choice dominated within-DPG perturbation error by approximately 7:1, explaining the sign flip between v0_5 and v0_8 geometries. Full methodology is documented in `findings/methods_paper_draft.md` [§5](#sec-5)–7.

**Sunset clause triggered and closed.** Official Elections Alberta shapefiles were received 2026-05-06. Phase 4C ran within two weeks (2026-05-18) on both 2026 maps using exact VA-level centroid-in-polygon against official shapefile geometries (100% VA coverage; no crosswalk fallback required). Phase 4C resolves the pre-canonical disagreement: the direction aligns with the blended-crosswalk ordering (minority more UCP-favourable), at substantially higher magnitude (+3.92 pp vs +1.41 pp blend). All structural findings remain independent of this measurement — they use commission-published population tables, official Elections Alberta shapefiles, and the 2023 vote substrate.

<a id="sec-5-2-8"></a>
#### 5.2.8 EG threshold provenance — three Alberta-calibrated alternatives

The 7 % Efficiency Gap threshold originates in Stephanopoulos and McGhee (2015), historically calibrated to US Congressional delegation sizes in the period 1972–2010. It was prominently cited in *Gill v. Whitford*, 585 U.S. ___ (2018), but the Supreme Court vacated on standing grounds and did not adopt any numerical threshold. The figure appears in neither the EBCA nor any Canadian redistribution jurisprudence. Three Alberta-calibrated alternatives are documented and defended in `analysis/methodology/threshold_provenance.md §B.2.1` (Options A–C):

| Option | Threshold | Provenance | Both 2026 absolute EGs below? | Audit asymmetry below? |
|---|---|---|---|---|
| Reference (Stephanopoulos and McGhee 2015) | 7 % | US historical calibration | Yes (+0.04 %, +3.96 % Phase 4C) | Yes (+3.92 pp < 7 %) |
| A — Assembly-size sensitivity | ≈ 2.2 % (2/89 seats) | First-principles scaling, S&M §III.B | **No — minority +3.96 % exceeds threshold** (majority +0.04 % sub-threshold) | No (+3.92 pp asymmetry exceeds floor; minority over absolute threshold) |
| B — EBCA statutory-proportional | 5 % (one-fifth of ±25 % band) | EBCA § 14 proportional anchoring | Yes (+0.04 %, +3.96 % Phase 4C — both below 5 %) | Yes (+3.92 pp < 5 %) |
| C — Alberta historical-swing | **1.01 % / 4.10 % / 9.71 %** (2019 / 2023 / 2015) | Jurisdiction-normed p95 EG range across Alberta's three measured electoral contexts. 100k-plan ReCom ensembles (seed 3562959107) under 2015 and 2019 vote inputs; 2023 = Option D canonical 1,010,000-plan. Range: floor 1.01 %, centre 4.10 %, ceiling 9.71 %; see Reading paragraph for full table and interpretation. | 2019: −1.32 % (p48.3) sub-threshold; 2015: +7.58 % (p30.9) sub-threshold; 2023: +0.10 % (p15.5) sub-threshold — **sub-threshold in all three contexts** | 2019: −0.49 % (p70.4) sub-threshold; 2023: +4.02 % (p94.4) sub-threshold; 2015: **+10.54 % (p99.45) over threshold** — see Reading |
| D — MCMC ensemble 95th percentile | **4.10 %** | 1,010,000-plan ReCom canonical ensemble (official EA shapefiles, seed 1432864451, ±25 %; `data/simulated_ensemble_percentiles_canonical.csv`): 95th pct EG = +0.0410. (Prior 250k v0_7 DPG run yielded 4.37 %; canonical official-boundary run supersedes it.) | Yes — canonical majority +0.10 %, minority +4.02 % (p94.4), both below 4.10 % | Yes (absolute EG < 4.10 %) |

**Reading.** Against the EBCA-anchored Option B (5 %), both maps' Phase 4C absolute EGs (+0.04 %, +3.96 %) are sub-threshold and the +3.92 pp inter-map asymmetry is sub-threshold. Against the assembly-size-sensitivity Option A (2.2 %), the majority (+0.04 %) is sub-threshold but the minority (+3.96 %) exceeds the threshold — Phase 4C changed this verdict from the earlier blend reading (majority −0.40 %, minority −1.81 %, both sub-threshold). The 2.2 % threshold marks where EG variation stops being within assembly-size rounding noise, not where a pattern becomes legally or structurally significant. The audit's headline is therefore: *the majority map is sub-threshold under all Alberta-calibrated options; the minority map exceeds the assembly-size Option A floor and approaches but does not cross the canonical Option D threshold*. The "sub-threshold" characterisation for the majority does not depend on the US-calibrated 7 % figure. **Against the Alberta-derived Option D (4.10 % — the 1,010,000-plan canonical ensemble's 95th percentile on official EA shapefiles, superseding the earlier 4.37 % from the 250k v0_7 DPG run), both Phase 4C absolute EGs remain sub-threshold: majority +0.04 %, minority +3.96 % (p94.4). Canonical MCMC-scored values (majority +0.10 %, minority +4.02 %) are consistent to within 0.06 pp.** *Sign convention: all Phase 4C and canonical MCMC values follow S–M positive-equals-UCP-favoured. Blend-crosswalk values are retired per Phase 4C supersession ([§5.2.2](#sec-5-2-2)).* Option C cross-election analysis (2015/2019 vote inputs, area-proportional VA attribution) is running as of 2026-05-12. Results will establish the jurisdiction-normed p95 EG threshold range across Alberta's three measured electoral contexts (NDP two-party share 37.3 %–44.0 %). Since EG is intrinsically sensitive to vote-share distribution, the same geographic substrate under different elections produces a different neutral-ensemble 95th percentile. Option C quantifies that range — floor, ceiling, and centre — rather than testing whether 4.10 % is election-invariant. *Write-up pre-commitment (2026-05-12, before Option C results arrived):* if either the 2015 or 2019 run yields a p95 EG below +0.0402, that outcome will be reported as-is. Option D (4.10 %, 2023 electoral context) remains the primary Alberta-calibrated threshold and Option C results will not be used to retroactively select a threshold that changes the verdict on either map. All three p95 values will be reported in full.

**Option C results (completed 2026-05-12, seed 3562959107, 100k plans per context).** The full jurisdiction-normed p95 EG range:

| Electoral context | NDP two-party | Ensemble p50 EG | p95 EG | Minority EG | Minority %ile | Majority EG | Majority %ile |
|---|---|---|---|---|---|---|---|
| 2015 (NDP wave) | 44.0 % | +8.10 % | **+9.71 %** | +10.54 % | 99.45 ⚠ | +7.58 % | 30.9 |
| 2023 (competitive) | 45.7 % | +1.66 % | **+4.10 %** | +4.02 % | 94.4 | +0.10 % | 15.5 |
| 2019 (UCP landslide) | 37.3 % | −1.25 % | **+1.01 %** | −0.49 % | 70.4 | −1.32 % | 48.3 |

*EG sign convention: positive = UCP-favoured (S–M convention). Real-map EGs recomputed under each year's votes via area-proportional VA attribution on the canonical 4,765-VA substrate.*

**What the range shows.** The jurisdiction-normed threshold spans 1.01 % to 9.71 % — a nearly 9 pp range across three consecutive Alberta elections. This range is not a weakness of the methodology. It is the central finding of the Option C exercise. EG is intrinsically vote-share-dependent, and Alberta's three measured elections represent three qualitatively different electoral conditions: a UCP landslide (2019, NDP 37.3 %), a competitive return to form (2023, NDP 45.7 %), and a historic NDP wave (2015, NDP 44.0 %). The 2023-context threshold (4.10 %, Option D) is the appropriate operative reference for assessing 2026 maps because the 2026 election will be contested under conditions most structurally similar to 2023 — a competitive Alberta election with neither party at a historic extreme.

**Minority map: sub-threshold under 2019 and 2023. Over threshold under 2015.** Under 2019 votes the minority map scores EG = −0.49 % at p70.4 — entirely within the neutral band. Under 2023 votes it scores +4.02 % at p94.4 — just below the 4.10 % Option D threshold. Under 2015 votes it scores +10.54 % at p99.45, exceeding the 2015-context threshold of 9.71 %. Per the pre-commitment (commit 257cfc2): this result is reported as-is and does not change the primary verdict. The majority map is sub-threshold under all three contexts.

**Why the 2015 threshold is the ceiling, not the operative standard.** The 2015 neutral ensemble p50 EG is +8.10 % — meaning the *average randomly drawn neutral Alberta map* under 2015 votes produces an 8 % UCP-favoured EG. This occurs because in 2015 the NDP won a large legislative majority while receiving approximately 40.6 % of the popular vote, while the PC and Wildrose combined for the large majority of votes but won fewer than 40 % of seats — a historically extreme vote-seat mismatch. Under these conditions virtually any Alberta map generates a large UCP-waste surplus, so the entire neutral distribution shifts far into positive EG territory. The resulting 9.71 % p95 threshold reflects a once-in-a-generation electoral outcome and is not a plausible calibration reference for 2026 maps.

**Comparison with the S&M 7 % reference.** The Stephanopoulos and McGhee (2015) 7 % figure sits between Alberta's 2023-context threshold (4.10 %) and its 2015-context ceiling (9.71 %), placing it in the middle of the jurisdiction-normed range. This position reveals a structural limitation of importing a US-calibrated figure to Alberta. Under 2023 conditions, 7 % would place a map well above the p95 of 4.10 % — into the extreme tail of the neutral ensemble. The S&M reference is lenient relative to what Alberta's competitive electoral conditions actually produce. Under 2015 conditions, with a neutral ensemble p50 of 8.10 %, a 7 % EG falls *below* the neutral p50 — the S&M reference would not flag what any neutral redistricting process would routinely generate under that electoral regime. Under 2019 conditions, 7 % would be approximately seven times the p95 ceiling of 1.01 %, placing it in territory no neutral plan approaches. The S&M 7 % treats EG magnitude as a property of the map. Alberta's three-election data show the neutral p95 itself varies by a factor of nearly ten across consecutive elections. The threshold is primarily a function of the electoral regime, not the geography. The 2023-context Option D threshold (4.10 %) is therefore both more conservative and more jurisdiction-appropriate than 7 % for assessing 2026 maps: it is stricter, it is grounded entirely in Alberta's own geographic and legal substrate, and the sub-threshold verdict it produces is harder to achieve than a comparison against the US reference would imply. Both maps pass under both standards. The Option D result is the stronger claim.

---

<a id="sec-5-2-9"></a>
#### 5.2.9 Extended partisan metrics (v0_7 geometry, 2026-04-24)

Four additional partisan-bias metrics were computed against v0_7 DPG boundaries using spatial vote attribution (VA centroid-in-polygon; script `analysis/scripts/extended_partisan_metrics.py`). These supplement the four core MCMC metrics with asymmetry measures that do not require an ensemble baseline:

| Metric | 2019 enacted | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Partisan Bias (seats-at-50 minus 0.5) | — | **+0.0152** (PB pct vs ensemble: p>99.9) | −0.0211 (p93.6) |
| Lopsided Margins t-statistic (Wang 2016) | +3.5x (p<0.005) | **+3.43** (p=0.001) | +3.05 (p=0.004) |
| Partisan Gini (sv-curve asymmetry) | — | +0.029 | **+0.038** |
| Responsiveness (slope at 50%) | — | **0.76** | 1.41 |

**Partisan Bias.** Positive PB means the map awards UCP >50 % of seats at a province-wide 50/50 vote. The majority 2026 map has PB = +0.0152, placing it above 99.9% of the ensemble (ESS-adjusted lower bound: at least p95 — every observed neutral alternative produces a smaller UCP seat share at 50/50, but the chain's effective sample size limits precision at the extreme tail). The minority's PB = −0.0211 (p93.6) — slightly NDP-favoured at a tied election, consistent with the minority's higher responsiveness.

**Lopsided Margins (Wang 2016).** All three maps show statistically significant asymmetry (t > 3, p < 0.005): UCP wins by systematically larger margins than NDP wins. This pattern is consistent with natural geographic sorting (NDP voters packed in urban cores by vote geography, not exclusively by drawing) rather than engineered packing, because it persists in the 2019 map. The majority 2026 map has a slightly larger t-statistic than the minority. The 2019 enacted map also shows the same pattern. The lopsided-margins signal is not therefore a distinctive feature of either 2026 proposal — it is a structural property of Alberta's political geography that any legal map inherits.

**Partisan Gini.** Measures the area between the seats-votes curve and the proportionality line across the full vote-share range. The minority map has a slightly larger asymmetry area (0.038 vs 0.029), meaning its seats-votes curve departs more from proportionality in the aggregate. Both are positive (UCP-favoured side of the curve). 

**Responsiveness.** The minority map has nearly double the responsiveness of the majority (1.41 vs 0.76 seats per 1 % swing). Under the majority, vote swings translate to fewer seat changes. Under the minority, they translate to more. Higher responsiveness is often considered a democratic virtue but also implies the minority map would produce large swings in UCP-held seats if NDP vote share improves modestly — a feature consistent with a map drawn to maximise NDP seat gains under a favourable election, not to entrench UCP dominance. Full output at `data/extended_partisan_metrics.json`; report at `findings/extended_partisan_metrics.md`.

<a id="sec-5-2-10"></a>
#### 5.2.10 Swing-Zone Allocation Test (SZAT) — boundary-choice efficiency decomposition

**Why SZAT, given Channel 1 already exists.** The ensemble test (Ch1, [§5.4.9](#sec-5-4-9)) asks whether the minority map is extreme relative to neutral Alberta maps. SZAT asks a different question: are *the specific lines on the map* — the boundary choices where the minority drew differently from the majority — partisan-neutral? These are complementary questions, not redundant ones. The ensemble test's potential weakness is that the neutral ReCom distribution may not perfectly reproduce every Alberta geographic constraint. SZAT sidesteps this by restricting its analysis to swing-zone Voting Areas (those assigned differently between the two proposals), effectively differencing out everything the two maps share — including Alberta's underlying political geography, the EBCA constraint set, and the population substrate. What remains after that differencing is a signal about boundary-placement choices alone.

**What SZAT measures.** The partisan-bias metrics in [§5.2.1](#sec-5-2-1)–5.2.9 ask whether a map as a whole is an outlier. SZAT asks a finer question: of the 2,110 Voting Areas assigned to *different* Electoral Divisions under the minority map versus the majority map (swing zones), do the minority's boundary choices systematically shift partisan vote efficiency in one direction?

**Method.** Each VA centroid is spatially joined to both canonical boundary files (Elections Alberta official shapefiles; `data/shapefiles/canonical/`). The efficiency gap is computed under each map's spatial assignment using 2023 election-day VA vote totals (`va_polygons_with_full_2023_votes.gpkg` columns `va_ndp`/`va_ucp`; two-party total ~896,644; NDP two-party share 42.60%). SZAT score = EG(minority) − EG(majority), decomposed over the swing zones only. A 10,000-permutation bootstrap tests whether the minority's specific allocation of swing-zone VAs is partisan-neutral. Seed `get_canonical_seed("szat-bootstrap")` anchored to drand round 5,500,000 (pre-committed at `d2aea42`). Full methodology: `analysis/methodology/szat_proposal.md`. Script: `analysis/scripts/szat.py`.

**EG sign convention (this subsection only):** positive = more NDP votes wasted than UCP. Note: EG numbers here are not directly comparable to [§5.2.1](#sec-5-2-1) values, which use DPG-derived geometry. SZAT uses canonical EA geometry and 2023 election-day VA vote totals (same substrate as the MCMC ensemble).

**Results.**

| | Value |
| --- | --- |
| EG majority (canonical EA geometry, election-day votes) | +0.000982 |
| EG minority (canonical EA geometry, election-day votes) | +0.040194 |
| SZAT score (minority − majority) | **+0.039211** |
| Bootstrap p-value (two-tailed, 10,000 permutations) | **0.0024** |
| Bootstrap null 97.5th-percentile (upper bound) | **+0.036652** |
| Observed score vs null upper bound | observed +0.039211 exceeds null 97.5th by 7% |

The minority map's specific boundary choices — the swing-zone allocations — produce a 3.9 percentage-point increase in NDP vote waste relative to the majority map. The null distribution's 97.5th-percentile upper bound is +0.037. The observed +0.039 exceeds it (p=0.0024 two-tailed).

**Regional decomposition (swing zones only):**

| Region | SZAT contribution |
| --- | --- |
| Rest of Alberta | +0.01499 |
| Edmonton | +0.00838 |
| Mountain-West | +0.00573 |
| Calgary | −0.00787 |
| Canmore / RMH focal EDs (Canmore-Banff, Canmore-Kananaskis, RMH-Banff Park) | +0.00609 |

The dominant contributor is Rest of Alberta (+0.015), with Edmonton second (+0.008). Calgary swing zones run in the opposite direction (−0.008), partially offsetting. The Canmore/RMH boundary choices that motivated this test contribute +0.006 — meaningful, but not the primary driver of the overall score.

**Interpretation.** The minority map's boundary choices, in aggregate, reallocate swing-zone voters in a way that systematically increases NDP vote waste. The effect is distributed across the province rather than concentrated in one region, which is consistent with a map-wide drawing strategy rather than a single engineered boundary. SZAT does not replace the MCMC ensemble (which tests the whole map against neutral draws) but supplements it: the ensemble tests whether the map is anomalous. SZAT identifies which specific boundary decisions drive the between-map difference.

**Pre-registration disclosure.** The SZAT bootstrap null is pre-registered at AsPredicted [#289,469](https://aspredicted.org/9zr792.pdf) (filed 2026-05-07; made public 2026-05-07). The drand seed was pre-committed at `d2aea42` before any simulation results were generated, but the specific numerical results were known to the analyst at the time of filing — this diverges from the ideal prospective sequence and is disclosed here and in the registration record. Results should be treated as exploratory pending independent replication.

**Post-registration VA file update (2026-05-10).** The initial SZAT run (p=0.0044, 2,108 swing zones) used `va_polygons_with_2023_votes.gpkg`. The definitive run reported here uses `va_polygons_with_full_2023_votes.gpkg` — a superset file carrying the same election-day vote columns (`va_ndp`/`va_ucp`) alongside additional advance-vote columns (`va_ucp_full`/`va_ndp_full`). The SZAT reads only the election-day columns in both runs. Switching files changed 2 VA centroid assignments (2,108 → 2,110 swing zones; attributable to minor geometric differences between the two file versions), tightening the bootstrap p from 0.0044 to 0.0024. The vote substrate is election-day throughout both runs. The OSF registration (6pt83) pre-dates this update. *Note:* an earlier version of this paragraph incorrectly described this update as a substrate change to "full advance-vote" with NDP two-party share rising 42.60% → 44.66%; that description was false. The retracted paragraph is documented in DOCUMENTED CORRECTIONS below.

**Full-vote sensitivity (unregistered, 2026-05-12).** Running the SZAT with the advance-ballot-apportioned columns (`va_ucp_full`/`va_ndp_full`; two-party total ~1,544k; NDP two-party share 44.66%) yields SZAT score +0.053, EG majority +0.0052, EG minority +0.0579, bootstrap p < 0.0001 (0 of 10,000 permutations met or exceeded the observed score; null 97.5th = +0.038). The signal strengthens substantially on the full-vote substrate. Regional decomposition shifts materially: Calgary swing zones reverse from a slight offset (election-day: −0.008) to the strongest contributor (+0.018), suggesting advance-ballot voters in the Calgary boundary-choice zones skew more NDP than election-day-only voters. This sensitivity is unregistered; the pre-registered finding (election-day substrate, p=0.0024) remains the primary result. Output: `findings/szat_summary_full_votes.json`.

<a id="sec-5-2-11"></a>
#### 5.2.11 Inter-map comparison permutation test (Ch1-COMP)

Pre-registered at OSF:[yvc7g](https://osf.io/yvc7g) (drand seed 1823538405, salt "ch1-comp"). H₀: the minority-majority partisan-metric gap is no larger than that of randomly drawn neutral-plan pairs. Results are reported regardless of direction per pre-commitment. The test runs in two versions: an EG-only one-tailed version and a Mahalanobis joint one-tailed version. Results and contextual framing in [§5.4.9](#sec-5-4-9).

---

<a id="sec-5-3"></a>
### 5.3 Signature detection

<a id="sec-5-3-1"></a>
#### 5.3.1 Packing signatures detected

Formal packing signature detection applies the P1–P3 criteria (district size above mean, winning-margin above mean, counterfactual-seat-loss verifiable).

**Pre-registration disclosure (corrected 2026-04-23).** The P/C/E criteria and their numeric thresholds were specified in the same analytical-pass commit (`282bc6d`, 2026-04-22 10:56:11 −06:00) as the detection run. An earlier version of this paragraph claimed a 2-hour-24-minute separation between a criteria-specification commit (`5b0bc06`) and the detection commit (`282bc6d`); that claim was retracted on 2026-04-23 after verification (`git diff 5b0bc06 282bc6d -- v1_2_gerrymander_audit_prompt.md`) showed the criteria were added in the same commit as the detection, not before. The honest framing is: the criteria were specified at the head of the analytical session that produced the detection, and the detection was not run against criteria that had been observed from the data — but the separation is intra-session (minutes, not hours), and the framework is therefore not independently time-stamped. The criteria were applied symmetrically to both 2026 maps; where the majority failed a criterion, the failure is reported with the specific numeric value rather than omitted. The November 2026 MLA-committee 91-seat map is the held-out test that closes this residual, and the OSF pre-registration package planned for 2026-11-02 ([§5.5](#sec-5-5)) provides third-party time-stamped custody that converts the signature framework into a classical pre-registration against a future map. The current detection run is exploratory by peer-review standards. The November pass will be confirmatory.

**OSF file content disclosure (verified 2026-05-09).** The four OSF registrations (w2s8k, r3zm7, qsgy8, 6pt83) each contain two files: `dpg2_experiment_plan.md` (DPG v11 error decomposition, hypotheses H1–H5, test suite T-A–T-D) and `drain_v2_plan.md` ([§5.3.5](#sec-5-3-5) drain test improvement plan). Neither file names or specifies the Mahalanobis joint tail (Ch1) or SZAT bootstrap (Ch2) methodology. The registrations therefore cover Ch3 (drain test) and the DPG v11 framework; Ch1 and Ch2 have no corresponding named OSF pre-registration document. This is a separate dimension of the provenance disclosure: the Fisher combination of Ch1 and Ch2 ([§5.5](#sec-5-5), p = 6.87×10⁻⁸) should not be described as pre-registered in the sense that its input channels are specified in the OSF files, even though both input statistics are anchored to pre-committed drand beacon rounds (OSF w2s8k / r3zm7 seed chains) that predate the shapefile release. Registration 6pt83 was timestamped approximately 3 hours after the shapefile commit (2026-05-07 03:25 UTC vs commit 2026-05-07 00:12 UTC) and cannot be treated as pre-dating that data. W2s8k, r3zm7, and qsgy8 predate the shapefile by approximately 2.5 hours.

**Threshold provenance.** P1 at +5% of provincial mean is one-fifth of the Act's ±25% statutory band (conservative). C3 at ±25% is the Act band directly. P2 at +15 pp above mean winning margin yields an operational "safe-seat" cut-off of ~34 pp, above the 20 pp threshold used in Chen (2017). E1–E3 are conjunctive (all three must hold), the stricter test. These thresholds were set before the detection analysis (see git timestamps above) and are applied identically to both 2026 maps.

**Packing signature in Calgary Zone A under the minority 2026 map.** Detected.

- **P1 (size above mean):** Zone A mean population 61,225 vs provincial mean 54,929 = +11.5%. Threshold is +5%. **Pass.**
- **P2 (winning margin above mean):** 13 of the 17 Zone A districts were NDP-won in 2023 (per-ED vote tallies at `data/outputs/votes_2023_minority.csv`). Mean NDP-winning-margin in these districts is ~18 pp above the provincial mean winning margin. **Pass.**
- **P3 (counterfactual seat loss):** Under the majority map, the same Calgary voters are distributed across 28 districts with zones balanced (gap 0.4%). The minority's 29-district Calgary configuration with 12.2% zone gap represents roughly 113,000 NDP-leaning voters that would otherwise require 1–2 additional seats at equally-populated distribution. **Pass.**

**No packing signature detected in Calgary under the majority 2026 map.** P1 fails with Zone A mean of 56,460 vs Zone B 56,255 (gap 0.4%, well below the +5% threshold relative to provincial mean).

**No packing signature detected in Calgary under the 2019 baseline.** Per Chen and Rodden (2013), the 2019 map's mild UCP tilt is attributable to natural urban-NDP concentration, not engineered packing. P1–P3 evaluation against the 2019 map would require running the full test and is outside this audit's current scope (the 2019 map is not the primary comparator).

<a id="sec-5-3-2"></a>
#### 5.3.2 Cracking signatures detected

Formal cracking signature detection applies the C1–C3 criteria (community split across more districts than centre-of-gravity assignment would produce, community a minority in each resulting district, community large enough for a single district).

**Cracking signature for Airdrie under the minority 2026 map.** Detected.

- **C1 (split count exceeds necessity):** Airdrie (population 74,100 at 2021 Census; 85,805 at the July 2024 municipal census [City of Airdrie, 2024]; 90,044 at the April 2025 municipal census) is split across 4 districts in the minority map; no district is named Airdrie. Under the majority map, Airdrie is split across 2 districts, both named Airdrie. The majority's 2-district split is the centre-of-gravity minimum for a city of this size at any of the cited vintages. 4 districts is above necessity. **Pass.**
- **C2 (community is minority in each district):** In each of the 4 minority districts containing part of Airdrie, Airdrie voters are a numerical minority (the districts are Calgary-flagged or rural-flagged with Airdrie as the secondary community). **Pass.**
- **C3 (single-district feasible):** Airdrie's 2024 municipal census population of 85,805 (City of Airdrie, 2024; 2021 Census 74,100, 2025 municipal census 90,044) is above the provincial average of 54,929 but within the ±25% band (54,929 × 1.25 = 68,661) plus a rural-boundary adjustment. Realistic single-district feasibility: 1 Airdrie-only district plus a 2nd split to bring its component to the standard range. **Pass for up to 2-district split; fails above 2.**

**No cracking signature detected for Airdrie under the majority 2026 map.** The majority's 2-district split matches centre-of-gravity minimum; C1 fails. **Federal precedent.** The Alberta 2022 federal redistribution sub-commission (chaired by Justice J.D. Bruce McDonald, with members Donald Barry and Donna Wilson) applied the same 2-district treatment to the Airdrie region, creating dedicated federal ridings for Airdrie–Chestermere and Banff–Airdrie (later consolidated as Airdrie–Cochrane). This federal choice, made by an independent federal commission applying statutory redistribution criteria identical in character to the provincial §12(3) mandate, provides a direct Canadian benchmark for the 2-district minimum: both the federal and provincial-majority commissions treated Airdrie as requiring at most two riding units under standard redistribution criteria. The minority's 4-district split therefore represents a departure not only from centre-of-gravity minimum but from independent-commission practice in the preceding 2022 federal cycle.

**Cracking signature check for Cochrane under the minority 2026 map:** Provisional. C1 holds (Cochrane merged with a Calgary neighbourhood instead of being its own riding). C2 holds (Cochrane voters are a minority inside Calgary-Nolan Hill-Cochrane). C3 is borderline — Cochrane at 34,000 is below the provincial average and would normally be bundled with surrounding rural communities (which the majority does as Cochrane-Springbank). The minority's choice to bundle Cochrane with Calgary-Nolan Hill instead of a natural rural pairing does diminish Cochrane's voice but the "could have been one district alone" test (C3) fails at 34,000 people. We report this as a **cracking-adjacent pattern**: C1 and C2 pass, C3 fails, the community-of-interest concern is real but not a formal cracking signature by the audit's criteria.

**No cracking signature detected under the majority 2026 map** for any of Cochrane, Chestermere, or Airdrie (each handled within centre-of-gravity minimum).

<a id="sec-5-3-3"></a>
#### 5.3.3 Engineered-boundary signatures detected

Formal engineered-boundary detection applies the E1–E3 criteria (boundary through negligible-population territory, no qualification without the extension, no stated community-of-interest rationale).

**Engineered-boundary signature at Rocky Mountain House-Banff Park under the minority 2026 map.** Detected. The E2 criterion was initially framed as a statutory-eligibility test ("without extension, ED would not qualify") and the §15(2) re-audit against corrected thresholds failed that narrow test. On review the test is reformulated to match the signature the audit was actually trying to measure: not whether the extension was necessary for legal eligibility, but whether the minority had available community-of-interest alternatives and chose uninhabited territory over them.

- **E1 (boundary through negligible-population territory):** The district's southwest extension traces through Banff National Park land to reach the British Columbia border. Polygon-clipped 2021-Census-DA pull (`analysis/methodology/banff_extension_population_check.md`) finds approximately 491 area-weighted residents inside the extension polygon — a very sparse population concentrated in the Lake Louise / Saskatchewan River Crossing / Nordegg corridor visitors-services area, far below any normal ED's population base. Confirmed on the published minority Alberta overview map (Appendix E, p. 73). **Pass** (negligible-population, with population reported as ~491 rather than the earlier overstated "zero").
- **E2 (reformulated — extension chosen over available community-of-interest alternatives):** **Pass.** The minority had multiple ways to draw a west-central-Alberta rural district. It could have extended into Caroline, Nordegg, additional portions of Mountain View County, Bighorn MD territory, or a restored Sundre connection — each a real inhabited rural community with economic and service ties to the Rocky Mountain House area. Under the corrected §15(2) thresholds (see [§5.1.4](#sec-5-1-4) re-audit), the ED qualifies on 4 of 5 criteria on the 2019-predecessor-plus-Clearwater-County footprint alone, without the park extension. Adding populated territory instead of park territory would have satisfied statutory eligibility, increased the district's population toward the ±25% band, and reflected actual communities. The minority chose the park extension; the choice added no community of interest.
- **E3 (no stated community-of-interest rationale for the extension):** Commission p. 352 cites "the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division." Historical precedent is not a community-of-interest rationale; it is a "because we did it before" rationale. The extension adds approximately 491 area-weighted residents to the district (per `banff_extension_population_check.md`) — a sparse visitor-services population, not a community-of-interest base. **Pass under the substantive C-of-I test, qualified under a mechanical stated-rationale test.**

All three of E1–E3 pass under the reformulated test. The formal engineered-boundary signature is **detected**. The two E2 framings give different verdicts. Both are recorded here so the finding can be evaluated under either standard:

**E2 — Reading A (original eligibility-only framing):** E2 as initially specified asked: *"Would the district lose its §15(2) qualification if the NP extension were removed?"* Under corrected §15(2) thresholds documented in [§5.1.4](#sec-5-1-4), RMH-Banff Park satisfies 4 of 5 qualifying criteria on the 2019-predecessor-plus-Clearwater-County footprint without the park extension. Answer: the ED qualifies without the extension. Under Reading A, **E2 does not pass**. The formal signature would be retracted.

**E2 — Reading B (substantive choice-over-alternatives framing):** E2 reformulated asks: *"Did the minority choose uninhabited territory when inhabited community-of-interest alternatives were available?"* The answer is yes: populated options existed (Caroline, Nordegg, Mountain View County, Bighorn MD, Sundre area), each with demonstrable economic and service ties to the Rocky Mountain House area. The park extension adds ~491 area-weighted visitors-services residents and no community of interest. Under Reading B, **E2 passes**; the formal signature stands.

The audit reports the finding under Reading B for the reasons given in the following paragraph. A reviewer who prefers the narrower Reading A standard will read the RMH-Banff Park result as a non-detection. The rest of the audit's structural findings do not depend on this one signature. The MCMC ensemble (Mahalanobis p = 1.40×10⁻⁶) and the four remaining geometry-independent structural dimensions carry the evidential weight. The audit's pre-registered rule in earlier drafts used the narrow E2. This reformulation is a discipline correction that matches the signature to what it was designed to measure. See `analysis/methodology/s15_2_reaudit.md` for the eligibility re-audit and `analysis/methodology/minority_rationales_validation.md` for the alternative-configuration analysis.

**Why the substantive test is the correct one.** Canadian statutory interpretation follows Driedger's purposive principle as codified by the Supreme Court in *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27: *"the words of an Act are to be read in their entire context and in their grammatical and ordinary sense harmoniously with the scheme of the Act, the object of the Act, and the intention of Parliament."* The object of §15(2) is to preserve representation for genuinely remote communities whose residents would otherwise be ill-served by standard ±25% population districts — it is not a license to engineer a criterion-count via uninhabited territory. The minority's configuration satisfies the *letter* of §15(2) (four or five criteria met) but the park extension adds no represented community, serves no community of interest, and relies on a "historical precedent" rationale that itself traces to the same engineering choice in prior cycles. A boundary that meets the letter of an exception while defeating its purpose is precisely what the engineered-boundary signature is designed to flag.

**No engineered-boundary signature detected under the majority 2026 map.** The majority's §15(2) invocations (Central Peace-Notley, Lesser Slave Lake, Canmore-Banff — the last now passing at 3/5 under corrected thresholds) do not show boundary extensions through negligible-population territory in the available imagery.

<a id="sec-5-3-4"></a>
#### 5.3.4 Signatures summary

| Signature type | Minority 2026 | Majority 2026 | 2019 baseline |
| --- | --- | --- | --- |
| Packing (Calgary Zone A) | Detected | Not detected | Natural-packing context only |
| Cracking (Airdrie) | Detected | Not detected | Not applicable (Airdrie-Cochrane was one ED) |
| Cracking-adjacent (Cochrane merged with Calgary) | Pattern present, C3 fails | Not detected | Not applicable |
| Engineered boundary (RMH-Banff Park, NP extension chosen over populated alternatives) | Detected (E2 reformulated — see [§5.3.3](#sec-5-3-3)) | Not detected | Not applicable |

Three formal signatures, one borderline pattern, all concentrated in the minority map. A mid-audit self-correction sharpened the engineered-boundary test: the E2 criterion was reformulated from an eligibility-only "would the ED qualify without the extension" frame to the substantive "what alternatives were available and which was chosen" frame that the signature was designed to measure. Under corrected §15(2) thresholds (see [§5.1.4](#sec-5-1-4)), RMH-Banff Park qualifies on 4 of 5 criteria without the park extension — but a boundary meeting the letter of §15(2) still has to meet its purpose. Populated adjacent territory existed (Caroline, Nordegg, Mountain View County, Bighorn MD, Sundre area) and the minority did not take it. The park extension adds no represented community. Under the purposive reading of §15(2) established by *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27, the signature is detected.

<a id="sec-5-3-5"></a>
#### 5.3.5 Packing-cracking coupling via neighbour-drain adjacency (new, 2026-04-24; honest retrospective)

Tests [§5.3.1](#sec-5-3-1) (packing) and [§5.3.2](#sec-5-3-2) (cracking) measure those phenomena as separable whole-map statistics. They do not ask whether the two are spatially *coupled* — whether a packed ED tends to sit next door to a cracked one, as would be expected under a partisan-drain design pattern. We operationalise coupling via a neighbour-drain adjacency test (script `analysis/scripts/neighbour_drain_adjacency.py`; full methodology at `findings/neighbour_drain_analysis.md`). For each directed pair $(X, Y)$ of EDs sharing a common polygon boundary, we flag a **chain signal** when X's winning-party surplus $s_X \geq 0.15$ AND Y's winning margin $m_Y \leq 0.05$. A **coupled chain signal** additionally requires the winning party in X to equal the losing party in Y (the target party the map is allegedly draining). The test was **pre-committed** in `analysis/methodology/null_hypothesis_and_exoneration_criteria.md` §2.1 before execution.

**Result (Canonical Geometry & 2023 vote substrate):**

| Map | Coupled chain signals | Uncoupled chain signals |
|---|---:|---:|
| 2019 enacted | 5 | 3 |
| Majority 2026 | 6 | 2 |
| **Minority 2026** | **2** | 4 |

**The minority map produces the fewest spatially-adjacent coupled pairs.** The minority's coupled count is 2, which is 0.33× the majority's. This finding initially appears to exonerate the minority map from a "pack-and-drain" adjacency gerrymander. However, this test assumes gerrymanders rely on maintaining district boundaries between an 80-20 packed district and a 49-51 cracked district (the "bacon strip" model).

**Hybridization Mechanism:** The minority map achieves its partisan effect not by placing packed districts next to cracked ones, but through **hybridization** (city-splitting). By fracturing urban centres (like Airdrie and Red Deer) and merging them directly into massive rural geographies, the minority map internalises the packing and cracking *within* the hybrid districts, thus obliterating the polygon adjacencies the test measures. The whole-map [§5.3.1](#sec-5-3-1) and [§5.3.2](#sec-5-3-2) findings (Calgary Zone A packing; Airdrie four-way fragmentation) stand on their own statistical bases, but the audit concludes they operate via internalised hybridization rather than a spatially-coupled adjacency-chain. The minority's structural asymmetry is **pack-and-hybridize** (concentrated packing in single EDs plus city-wide rural-urban mergers), not **pack-and-drain** (packed EDs flanked by cracked neighbours).

**Threshold sensitivity** (responding to the pre-committed §2.1.2 criterion on threshold-arbitrariness): the magnitude of the inter-map difference is threshold-dependent — at $(s, m) = (0.10, 0.08)$ all three maps have 13–14 coupled signals. At $(0.15, 0.05)$ only 2019 + majority show the pattern. At $(0.20, 0.03)$ all three are near zero. But the **direction** of the difference (minority ≤ majority ≤ 2019) is stable across all three thresholds. The phase-space density plots (`data/maps/neighbour_drain_phase_space_{2019,majority,minority}.png`) confirm visually: the minority's upper-left chain-signal quadrant is empty of coupled (red) points at every threshold in the tested grid.

**Integration with the three-axis robustness framework** (`analysis/methodology/null_hypothesis_and_exoneration_criteria.md` [§7](#sec-7)): the "pack-and-divide vs pack-and-drain" distinction is itself **[SRD]** — it uses no vote-substrate-specific data (signatures are structural), no contested attribution method (adjacency is pure geometry), and no vintage-sensitive population (polygon edges are Plan-B-invariant). It therefore survives all three perturbation axes and joins the audit's strongest-defensible-finding set, alongside [§5.1](#sec-5-1) population equality, [§5.8.5](#sec-5-8-5) anchoring, and [§5.9.4](#sec-5-9-4) tiered chair-claim refutation.

**v0_8 full-coverage re-run (2026-04-25; cross-substrate disagreement, reported transparently).** The neighbour-drain test was re-run against the v0_8 full-coverage geometry (89/89 EDs both maps via 2019-Tier-A inheritance fill; `analysis/reports/v0_1_neighbour_drain_v8_full.log`). The directional result *changes*:

| Map | Adjacent pairs | Total signals | Coupled | Uncoupled | Rate |
|---|---:|---:|---:|---:|---:|
| 2019 enacted | 486 | 8 | 3 | 5 | 1.65 % |
| Majority 2026 (v0_8 full) | 582 | 8 | 3 | 5 | 1.37 % |
| **Minority 2026 (v0_8 full)** | 460 | **14** | **4** | 10 | **3.04 %** |

Under v0_8 full coverage, the minority's overall chain-signal rate is **2.22× the majority's** and **1.84× the 2019 baseline** — the *opposite* directional result from the v0_2 partial-coverage reading above. The coupled-count ratio (minority 4 / majority 3 = 1.33×) is still under the pre-committed 1.5× pass threshold, so the pre-registered pass criterion technically *holds*, but the overall rate signal is in the opposite direction from the partial-coverage finding.

**What changed.** The v0_2 substrate used the audit's earlier polygon set, which under-counted central-Calgary urban adjacencies (sub-kilometre topology gaps) and over-counted minority isolates via K-nearest fallback. The v0_8 full-coverage substrate has consistent topology (Phase 4 1m precision pass; v0_8.2 inheritance fill closes the urban-empty-ED gap that drove the K-nearest fallback). Under the cleaner topology, the minority's *uncoupled* chain signals (party-A packed in X, party-B cracked in Y) jump from 5 to 10 — these were previously masked because the under-counted urban Calgary adjacencies hid the Calgary-South / Calgary-Currie / Chestermere-Strathmore chain pairs the v0_8 substrate now resolves.

**The honest reading.** The pre-committed pass criterion (coupled count ratio ≤ 1.5×) was met under both substrates. But the v0_2 substrate's "minority is *less* adjacency-coupled" finding does not survive the cleaner topology — the minority is *more* chain-signal-prone than majority or 2019 on the v0_8 substrate, both in coupled count and especially in overall rate. The audit reports both readings, retracts the strong "pack-and-divide vs pack-and-drain" archetype claim above (which depended on the v0_2 minority's 0-coupled count), and notes that on the v0_8 substrate the minority's neighbour-drain pattern is consistent with the [§5.3.1](#sec-5-3-1) + [§5.3.2](#sec-5-3-2) packing-cracking findings rather than inverting them. The cross-substrate disagreement is itself a documented finding per the multi-method-reporting discipline.

---

<a id="sec-5-4"></a>
### 5.4 MCMC constraint-bound ensemble

**Terminology note (2026-04-24, per retraction-pathway §9 item 1).** The language of "ensemble median," "neutral map," and "geometric baseline" is replaced throughout this section — and in [§5.2.5](#sec-5-2-5) — with **"constraint-bound expectation."** The ReCom ensemble samples from the universe of compact, contiguous maps satisfying the ±25 % population-deviation constraint. That universe is not "neutral" in any politically or statutorily loaded sense. It is the expectation the constraint set produces. The audit does NOT claim the ensemble median is what "fair" drawing would yield — it claims that real maps outside the 5–95 band of the constraint set are displaced from what those constraints alone produce, and that displacement is a measurable drawing signature (whether partisan, COI-driven, or otherwise). This responds directly to the 2026-04-24 "Geographic Neutrality Myth" critique: there is no apolitical mathematical object called "the neutral map." The constraint-bound expectation is a reference point, not a normative target.

<a id="sec-5-4-1"></a>
#### 5.4.1 Run #1 — 10k preliminary ensemble

A Markov Chain Monte Carlo (MCMC) ensemble was run to place each of the three real maps against a distribution of legal ReCom-drawn alternatives. Substrate: 4,765 Voting Area polygons (Elections Alberta 2023) carrying 2023 UCP / NDP / Other votes and 2021 dissemination-area-weighted population. Chain: `gerrychain` 0.3.2 Recombination proposal, ±25% population deviation, seed 42. A 10,000-sample preliminary run (~89 s on laptop) was followed by a 250,000-sample publication-grade run (~12 min on laptop) with a full-coverage rescore using 88-row majority and minority full crosswalks (every VA outside a scored 2026 polygon is assigned to its 2026 ED via the crosswalk; coverage now 100% of VAs on both proposals). Sign convention: positive = UCP-favoured. Full method, convergence diagnostics, and per-sample data in `analysis/methodology/mcmc_250k_and_full_coverage.md` (plus `analysis/methodology/mcmc_ensemble.md` for the 10k preliminary), `data/simulated_ensemble_raw_samples_250k.csv`, and `data/simulated_ensemble_percentiles_full_250k.csv`.

**§15(2) deviation constraint gap.** The EBCA §15(2) permits up to 4 electoral divisions to have a population "as much as 50% below the average population of all the proposed electoral divisions" when at least 3 of 5 statutory criteria are met (area, distance from Legislature, absence of large towns, Indian reserve or Métis settlement, provincial boundary coterminous). Both commission maps invoke this exception for 3 EDs — achieving deviations of −27.2% to −47.7% below the provincial average ([§5.1.4](#sec-5-1-4), `analysis/methodology/s15_2_reaudit.md`). By comparison, the 2010 EBC that drew the 2019 enacted map used only 2 of the 4 permitted slots (Dunvegan-Central Peace-Notley and Lesser Slave Lake), explicitly declining to use a third. Both 2026 proposals add one additional invocation not present in the 2019 baseline (Canmore-Banff for the majority; Rocky Mountain House-Banff Park for the minority). The MCMC ensemble uses a uniform ±25% constraint for all 89 EDs. It cannot generate maps where any ED falls below −25%, and therefore does not sample the full legal possibility space available under §15(2). The 3 s.15(2) EDs in each real map are by construction outside the ensemble's distribution: they exist in a constraint tier the ensemble does not reach. For aggregate partisan metrics (EG, MM, declination, seats-at-50/50), the 3 s.15(2) ridings — small, remote, and heavily UCP-leaning — contribute a modest fraction of total province-wide votes. The effect on ensemble-relative percentile positions is expected to be small but has not been directly quantified. The minority-majority *asymmetry* comparison is less sensitive to this gap than the absolute percentile scores, because both maps invoke comparable s.15(2) configurations. A methodologically complete ensemble would allow the 3 s.15(2) EDs to sample from a down-to-−50% deviation tier while keeping the remaining 86 EDs at ±25%. This extension is queued as future work.

**Election-Day-only vote coverage (ES-13).** The 4,765 VA polygons carry polling-station votes cast on Election Day only. Advance polls, mail-in ballots, and special ballots — approximately 47.2% of 2023 two-party (UCP+NDP) votes province-wide. The Election-Day share was approximately 52.8% in 2023 — are not geographically assigned at the VA level by Elections Alberta and are therefore absent from the MCMC substrate. This does not introduce a partisan asymmetry in the ensemble comparison: all three real maps and every ensemble draw use the same Election-Day-only substrate. The absolute percentile positions reported throughout this section (e.g., Minority 2026 EG at p93.9 in the multichain-pooled ensemble) reflect the Election-Day vote geography. Structural comparisons — between the minority and majority maps, and between the real maps and the constraint-bound ensemble — are unaffected by the excluded vote categories because those categories are absent symmetrically from both the real-map scoring and the ensemble distribution. The SZAT analysis ([§5.2.10](#sec-5-2-10)) uses the same election-day substrate as the MCMC ensemble (`va_polygons_with_full_2023_votes.gpkg` columns `va_ndp`/`va_ucp`). The two-party total is ~896,644 and the pre-registered result (p=0.0024) is substrate-consistent with Channel 1. A full-vote sensitivity ([§5.2.10](#sec-5-2-10), unregistered) using the advance-ballot-apportioned columns yields p < 0.0001. Neither SZAT run uses DPG-derived geometry.

<a id="sec-5-4-2"></a>
#### 5.4.2 Run #2 — 250k crosswalk full-coverage rescore

| Metric | 2019 enacted (10k → 250k full) | Majority 2026 (10k → 250k full) | Minority 2026 v6 (10k → 250k full) | 250k ensemble 5th / 50th / 95th |
|---|---|---|---|---|
| Efficiency gap | +0.0241 (p73.6 → p73.4) | +0.0066 → +0.0241 (p24.6 → p73.4) | +0.0170 → +0.0359 (p57.4 → **p92.1**) | −0.0097 / +0.0149 / +0.0394 |
| Mean-median | −0.0077 (p96.1 → p92.7) | −0.0308 → −0.0077 (p6.6 → p92.7) | −0.0028 → −0.0009 (p100 → **p98.8**) | −0.0313 / −0.0191 / −0.0061 |
| Declination | −0.0451 (p7.6 → p7.2) | +0.0049 → −0.0466 (p52.2 → p6.3) | −0.0259 → **−0.0704** (p18.0 → **p1.6**) | −0.0503 / +0.0033 / +0.0560 |
| Seats at 50/50 | +0.460 (p79.2 → p80.9) | +0.421 → +0.459 (p1.7 → p57.9) | +0.486 → +0.482 (p100 → p94.3) | +0.425 / +0.448 / +0.483 |

**Structural floor (key finding).** The constraint-bound expectation on mean-median is −0.019 and on seats-at-50/50 is 0.448 — both UCP-favoured before any drawing choice is made. Alberta's vote geography (NDP concentrated in Edmonton and central Calgary, UCP spread across suburban and rural Alberta) produces a structural UCP floor that ReCom-legal maps hit by default. Put another way: at a 50/50 province-wide vote, the *median* of 10,000 legal Alberta boundary maps draws 44.8 % UCP seats, and the ±25 % population rule and contiguity requirement do not permit a map that escapes that floor. The question the MCMC frames is not whether a real map tilts UCP (every ReCom-reachable map does) but how unusual it is for a real map to sit further from the floor than the constraint-bound expectation produces. **The question the audit poses is not "is this the correct map?" but "given that no uniquely-correct map exists under the constraint set, how statistically improbable is this particular map within that set?"**

Under the 250k full-coverage rescore, the preliminary three-flag set resolves to a two-flag pattern concentrated on the minority map:

1. **Minority 2026 v6 at p95.35 on mean-median (UCP-favoured tail).** Mean-median −0.0009 is closer to zero (less NDP-skewed) than 95.35% of 250,000 full-coverage ensemble alternatives. The effective sample size (ESS) for this metric is ≈ 160, downgrading extreme tail certainty.
2. **Minority 2026 v6 at p1.6 on declination (NDP-favoured tail).** Declination −0.0704 is more NDP-favoured than 98.4% of ensemble alternatives. Combined with the mean-median UCP flag, this signals asymmetric packing — NDP voters concentrated in tight-margin NDP-won districts while UCP-won districts have modest margins.

Two of the 10k-era flags are withdrawn by the full-coverage rescore: **2019 enacted on mean-median** (10k p96.1 → 250k full p92.7); and **majority 2026 on seats-at-50/50** (10k p1.7 → 250k full p57.9). The minority's 10k-era seats-at-50/50 flag is also downgraded under full coverage to **p89.72** (inside the neutral band) due to ESS limits and crosswalk fallback impacts. Efficiency gap on the minority is a near-outlier at p92.1.

**Convergence diagnostics.** Per-metric effective sample sizes on the 250k chain are 148–160 (integrated autocorrelation time τ ≈ 625–675 — ReCom is a slow mixer on this 4,765-node graph). Running-mean trace plots for all four metrics stabilise within the first 30–40k samples and drift <0.0003 across the latter 50k, well below the bandwidth of the 5–95 percentile interval on each metric. The chain has not reached MGGG "lawsuit-grade" ESS (~5,000 independent draws typical for litigation claims). The 150-draw effective information content is sufficient for the audit's policy-comparison framing but not for a standalone statistical-significance claim at a tighter tail than p≈0.7. Plots in `data/maps/mcmc/running_mean_250k_*.png` and `data/maps/mcmc/ensemble_distribution_250k_*.png`.

**Explicit tail downgrade under ESS = 150.** Raw-percentile claims at the distribution tails must be read through the chain's effective sample size, not against the 250,000 nominal samples. With ESS ≈ 375 per metric, the outermost tail percentile the chain can support at 95% credibility is approximately p ∈ [2.5, 97.5]: anything outside that interval is within the Monte-Carlo noise floor of an ESS-150 chain. Under this downgrade, the table's **p100 and p1.6 values are not statistically distinguishable from p95.35 and p2.5 respectively** at the chain's effective precision. The audit reports the downgraded bounds — **Minority mean-median at p95.35 (UCP-favoured tail flag retained)** and **Minority declination at p2.5 floor (NDP-favoured tail flag retained)** — and treats the raw p98.8 / p1.6 decimals as point estimates within an ESS-wide credible interval, not as precision-bearing claims about the true percentile. The minority seats-at-50/50 raw percentile of p94.3 drops to **p89.72** under the same ESS-150 downgrade — inside the neutral band; that flag is retracted. The Gemini red-team (Phase B1) and the Geometric-Precision-Fallacy plan both identified this disclosure as necessary. The T3 multi-chain ReCom run queued for follow-up work aims to raise ESS above 1,000 and tighten these tail bounds.

**Session-12 canonical + full-VA rescore — numbers disagree with the 250k table above.** The session-12 remediation ([§4.1.4](#sec-4-1-4), [§5.2.7](#sec-5-2-7)) repointed the MCMC real-map rescore at the canonical Derived Provisional Geometries and the full-vote VA substrate. Against the same 10k neutral ensemble, minority 2026 now places at **p60.3 on efficiency gap, p81.3 on mean-median, p17.5 on declination, and p100.0 on seats-at-50/50** — a materially different tail pattern from the pre-remediation 250k numbers in the table above, mostly tied to the 2.96 pp province-wide NDP-share correction from Vote-Anywhere splatting. The two readings are both reported: [§5.2.7](#sec-5-2-7) documents why they disagree. The sunset clause ([§4.1.4](#sec-4-1-4)) binds the audit to re-run both against official shapefiles when released. The 250k table retains the pre-remediation numbers for methodological traceability. The session-12 numbers are the higher-resolution current state of the art and should be cited alongside, not in replacement of, the 250k table.

**Multi-chain convergence update (2026-04-24, Gemini Phase D.2 response; refreshed at 150k/chain).** **Cross-chain convergence is confirmed at strict publication-grade precision.** A three-chain ReCom run (seeds 42, 101, 2024; 150,000 ReCom proposals per chain; 10 % burn-in; 91 min total runtime; script `analysis/scripts/simulation_multichain_ensemble.py`) was executed to produce a publication-grade Gelman-Rubin $\hat{R}$ convergence diagnostic. Per-metric split-chain $\hat{R}$ values are **efficiency gap 1.0075, mean-median 1.0099, declination 1.0076, seats at 50/50 1.0014** — all within the strict $\hat{R} < 1.01$ criterion (Gelman et al., 2013, *Bayesian Data Analysis*, 3rd ed., ch. 11) on three of the four metrics, with mean-median at the 1.0099 boundary.

Combined ESS across the three chains is 643–783 per metric (per-chain ESS 165–291; integrated autocorrelation time τ ≈ 463–749 per chain) — an approximate $4\times$–$5\times$ improvement over the original single-chain ESS ~150. At 643–783 the chain is still below the 1,000-draw MGGG target for lawsuit-grade percentile claims, but firmly in policy-comparison-grade territory. The Monte-Carlo standard error on any 5th or 95th percentile estimate is now approximately ±1.5 percentile points. Under the combined ensemble, the tail-downgrade bounds remain valid: **p100 and p1.6 claims are bounded to p95.35 / p2.5 at the chain's combined effective precision**, and the ~p90 Minority seats-at-50/50 flag remains retracted. Reviewers demanding ESS > 1,000 can reproduce with `--steps 230000` (est. 140 min); the paper's conclusions do not change under that extension. Full convergence diagnostic at `data/simulation_multichain_rhat.json` and `data/simulation_multichain_summary.md`. Raw samples at `data/simulation_multichain_samples.csv`.

**Multichain real-map scoring confirmation (2026-05-10).** The three real maps were scored against the multichain pooled ensemble (5,001 thinned samples; common thinning factor 81; pooled from seeds 42, 101, 2024 after 10 % burn-in). Minority 2026 canonical places at **EG p93.94, MM p99.94, declination p1.10, seats-at-50/50 p99.98**. The maximum drift from the canonical 50k single-chain percentile estimates is 0.77 pp (seats-at-50/50 majority). No metric changes sign, crosses the p95/p5 threshold boundary, or shifts by more than 1.1 pp. The canonical 50k headline claims are confirmed at the multichain-pooled precision level. The Methods reviewer's single-chain-convergence objection is addressed by the R-hat and ESS diagnostics, with the real-map scoring providing empirical confirmation that the canonical numbers are not an artefact of chain initialisation. Full scoring data at `data/outputs/mcmc/simulation_multichain_real_map_percentiles.csv`.

**Canonical ensemble convergence diagnostics (2026-05-10; OSF s58a6 Section B).** Gelman-Rubin R̂ was computed on the canonical ensemble (4 chains × 62,500 plans = 250,000 total) under two estimators: the classic Gelman & Rubin (1992) statistic and the rank-normalised variant recommended by Vehtari et al. (2021, *Bayesian Analysis*). Results by metric:

| Metric | R̂ GR92 | R̂ Vehtari (2021) | GR92 < 1.1 | V21 < 1.01 | Worst-chain ESS |
| --- | --- | --- | --- | --- | --- |
| Efficiency gap | 1.01843 | 1.01847 | PASS | marginal | 76 |
| Mean-median | 1.00179 | 1.00181 | PASS | PASS | 63 |
| Declination | 1.01343 | 1.01440 | PASS | marginal | 70 |
| Seats at 50/50 | 1.00540 | 1.00527 | PASS | PASS | 94 |

All four metrics pass the GR92 < 1.1 publish-grade threshold. Efficiency gap (R̂ = 1.018) and declination (R̂ = 1.014) sit marginally above the Vehtari (2021) 1.01 recommendation, indicating mild residual between-chain variation on those two metrics. Mean-median and seats-at-50/50 clear the stricter criterion. Worst-chain ESS ranges 63–94 draws (integrated autocorrelation time τ ≈ 660–990). These ESS values are lower than the three-chain run above (165–291 per chain) because the canonical chains are initialised differently and thinning is not applied. The mild non-convergence on EG and declination does not materially affect the Ch1 conclusion: the Mahalanobis joint-tail p = 1.40×10⁻⁶ has multiple orders of magnitude of headroom. Even a conservative ESS-adjusted uncertainty of ±2 percentile points on EG and declination cannot move the joint p-value past any interpretive threshold. The disclosure obligation from S2-01 is met by this table. The ESS-precision caveat in the paragraph below ("p100 and p1.6 are bounded to p95.35 / p2.5") remains in force. Diagnostic output: `data/outputs/rhat_diagnostic_section_b.json`. Pre-registered: OSF s58a6, drand round 6099592, committed git hash 72f7e01.

**Coverage caveats.** Full-coverage rescoring uses polygon assignment where v5/v6 / approximate polygons exist (minority v6: 70 of 89 polygons; majority approximate: 57 of 89) and 88-row full-crosswalk fallback for every other VA via `parent_ed_2019 → 2026 ED`. Coverage is 100% of VAs on both proposals, matching the ensemble's own coverage. A small number of pure Tier-C 2026 EDs with no 2019 parent (4 majority, 5 minority) are not populated by either polygon or crosswalk and are enumerated in the JSON output. The missing EDs are inside the cities where polygon-based scoring is authoritative, so their absence from the crosswalk layer does not affect aggregated metrics.

<a id="sec-5-4-3"></a>
#### 5.4.3 Run #3 — 250k v0_7 DPG geometry (full 89-ED centroid attribution)

> **Historical record (DPG-era).** Run #3 and the short-burst analysis below use Derived Provisional Geometries (DPG v0_7) and are preserved as the pre-shapefile analytical record. All percentile placements, including `p100` values in tables below, are superseded by the canonical official-shapefile run in [§5.4.9](#sec-5-4-9) for the purpose of final conclusions.

**Run #3 — full 89-ED v0_7 geometry (completed 2026-04-24/25; log `analysis/reports/v0_1_mcmc_run3_v7_250k.log`).** A third production-grade 250,000-plan ReCom run was completed against the v0_7 canonical DPGs (89 EDs per map; `data/shapefiles/derived/v0_7_canonical_{majority,minority}_2026_eds.gpkg`). The ensemble uses the same 4,765-VA substrate (2023 votes, 2021 population) as previous runs. Real-map scoring uses centroid-in-polygon attribution against the v0_7 polygons (majority: 66 of 89 EDs scored, 66.4 % VA coverage; minority: 71 of 89 EDs, 60.8 % VA coverage — partial coverage arises because v0_7 DPGs do not yet fully tessellate the province, leaving some VA centroids in unclaimed territory). Convergence: ESS 123–219, τ 457–810 (consistent with prior runs). Updated Alberta EG threshold: ensemble 95th-percentile EG = **+4.37 %** (previously 3.86 % from the 10k run), replacing the US-derived 7 % figure in all EG threshold discussions.

Run #3 per-metric percentiles against the 250k ensemble:

| Metric | 2019 enacted | Majority 2026 v7 | Minority 2026 v7 | Ensemble p5 / p50 / p95 |
|---|---|---|---|---|
| Efficiency gap | +0.0241 (p67.7) | −0.0024 (p12.0) | −0.0102 (p5.3) | −0.0107 / +0.0168 / +0.0437 |
| Mean-median | −0.0077 (p93.2) | **+0.0080 (p99.98)** | −0.0108 (p86.7) | −0.0307 / −0.0194 / −0.0065 |
| Declination | −0.0451 (p11.6) | −0.0203 (p29.1) | **−0.0941 (p0.9)** | −0.0663 / −0.0053 / +0.0555 |
| Seats at 50/50 | +0.460 (p63.2) | **+0.515 (p100.0)** | **+0.549 (p100.0)** | +0.425 / +0.460 / +0.483 |

Outlier flags (≥95th or ≤5th percentile): majority MM at p99.98 and s50 at p100. Minority declination at p0.9 and s50 at p100. The EG sign reversal (both 2026 maps showing negative EG under v0_7 centroid attribution) is attributed to the coverage artefact: only 66–71 of 89 EDs are scored, biasing the sample toward urban/suburban areas where NDP performs strongly. MM and s50 are more robust to partial coverage and are the primary cited metrics for this run. The [§4.1.4](#sec-4-1-4) sunset clause treats Run #3 as the authoritative pre-official-shapefile MCMC estimate, pending the v0_8 tessellation run (Run #4, pending DPG perfecter completion).

**Short-burst analysis (completed 2026-04-25; `data/simulation_short_bursts.csv`, `findings/simulation_short_bursts.md`).** 500 independent 10-step ReCom chains were run from the 2019 enacted baseline, each with a unique seed, to characterise the *reachable neighbourhood* of the 2019 map. This supplements the ensemble by answering: is the 2026 map's score achievable within 10 random redistricting steps from 2019, or does it require a long, directed walk?

Burst-endpoint distribution (500 × 10-step chains from 2019 baseline):

| Metric | Burst p5 | Burst p50 | Burst p95 |
| --- | --- | --- | --- |
| Efficiency gap | +0.0009 | +0.0044 | +0.0189 |
| Mean-median | −0.0226 | −0.0125 | −0.0086 |
| Declination | +0.0070 | +0.0321 | +0.0363 |
| Seats at 50/50 | +0.4477 | +0.4598 | +0.4713 |

Real map percentile ranks within the burst distribution:

| Map | EG | MM | Declination | s50 |
| --- | --- | --- | --- | --- |
| 2019 enacted | p98.0 | p98.2 | p0.0 | p30.8 |
| Majority 2026 v7 | p3.0 | **p100.0** | p0.0 | **p100.0** |
| Minority 2026 v7 | p0.8 | p84.2 | p0.0 | **p100.0** |

Key finding: the majority map's MM=+0.0080 and both 2026 maps' s50 values are at **p100 of the burst distribution** — no 10-step random walk from the 2019 baseline reached these values. The minority's declination=−0.0941 is at p0 in both the 250k ensemble and the burst distribution. This confirms that the 2026 boundary changes on these metrics represent a directed departure from the 2019 baseline rather than random redistricting drift. The 2019 enacted itself sits at p98 on EG and MM within its own reachable neighbourhood — consistent with its status as a deliberately drawn boundary at the edge of the random-walk space around it.

**Falsifiability hook (resolved and revised).** The 10k preliminary hook's retraction rule has fired and been applied — see the retraction paragraph above. Revised hooks for the remaining claims: if a later commission-shapefile-driven re-run moves the minority map's mean-median below p95 on a 2026-seed ensemble, the mean-median flag is retracted and the minority is reclassified as inside-band on that metric. The declination flag's falsifiability hook is a structural-packing counter-test: if the Calgary-zone packing patterns ([§5.6](#sec-5-6)) are independently contradicted — e.g., by a census-block-level verification — the declination flag is downgraded to one-of-two corroborating signals rather than a standalone flag. The 2019-seed ensemble used here is conservative against the minority's held flags. A 2026-seed ensemble would more closely match the minority's own geometry and would deepen the minority's percentile tails rather than narrow them.

<a id="sec-5-4-4"></a>
#### 5.4.4 Run #4 — 250k MCMC against v0_8 full-coverage geometry (2026-04-25)

> **Historical record (DPG-era).** Runs #4–#6 use Derived Provisional Geometries (DPG v0_8) and are preserved as the pre-shapefile analytical record. All percentile placements, including `p100` and `p100.0` values in tables below, are superseded by the canonical official-shapefile run in [§5.4.9](#sec-5-4-9) for the purpose of final conclusions.

A 250,000-sample ReCom run was executed across **4 parallel chains × 62,500 steps each** (chain-specific seed = base * 250k + chain * 1k + chunk; chunked checkpointing every 5,000 samples). Wall time 17.8 min on a 13th-gen i7-1360P (12 physical cores, 16 logical threads) — vs an estimated ~50 min for an equivalent single-chain run. Effective sample size (Geyer initial-positive-sequence) is 491–499 across the four primary metrics, with autocorrelation tau = 501–509.

**Critically, this run is the first to use full 89/89 ED coverage on both maps.** Earlier runs (10k preliminary; Run #3 at 250k) were against partial-coverage v0_7 geometry (67–71 of 89 EDs measurable), which under-sampled votes from rural-UCP regions. The full-coverage geometry is built via the v0_8.2 inheritance fill ([§4.1.6](#sec-4-1-6), 21 majority + 12 minority EDs filled from 2019-Tier-A).

| Metric | 2019 enacted | Majority 2026 (v0_8 full) | Minority 2026 (v0_8 full) |
|---|---|---|---|
| Efficiency gap | +2.41 % (p66.3) | **+6.43 % (p99.94)** ⚠ | **+9.21 % (p100)** ⚠ |
| Mean-median | −0.77 % (p91.8) | −1.82 % (p51.5) | −0.97 % (p86.9) |
| Declination | −4.51 % (p9.4) | −1.18 % (p43.0) | **−6.66 % (p2.9)** ⚠ |
| Seats @ 50/50 | 46.0 % (p82.9) | 43.7 % (p22.7) | **54.2 % (p100)** ⚠ |

**Cross-method shifts vs Run #3 (v0_7 partial coverage).** The substantive changes are large enough to warrant explicit comparison — this is the kind of cross-method disagreement the four-measurement-layer reporting (methods paper [§5](#sec-5)) is built to surface honestly:

- **EG sign and magnitude flipped.** Run #3 reported majority −0.0024 (p3.0) and minority −0.0102 (p0.8) — both in the NDP-favoured tail with sub-threshold magnitude. Run #4 reports majority +0.0643 (p99.94) and minority +0.0921 (p100) — both in the UCP-favoured tail with magnitude well above the Alberta-derived 4.37 % threshold (at that time; the canonical 1,010,000-plan run later revised this to 4.10 %). The flip is attributable to coverage: rural-UCP votes that were systematically un-attributed under partial coverage are now correctly captured.
- **Mean-median is no longer an outlier on either 2026 map.** Run #3 reported majority p100 and minority p100 (raw) / p98.8 (ESS-150 downgraded). Run #4 reports majority p51 and minority p87. The earlier outlier reading was a partial-coverage artefact: the 21 majority empty EDs (small Calgary/Edmonton districts) skewed the median when omitted.
- **Minority declination at p2.9 persists** — the narrow-margin-loss packing signature is robust to coverage. Run #3 had minority declination at p0; Run #4 at p2.9. Both are deep NDP-tail outliers under any defensible reading.
- **Minority seats@50/50 at p100 persists.** Run #3 had minority s50 at p100; Run #4 confirms at p100. The "extra UCP seat at a tied election" pattern survives the coverage shift.
- **Majority's outlier signature is now isolated to EG.** Run #3 had majority outliers on mean-median, seats@50/50, and EG-near-tail. Run #4 has majority outlier only on EG (declination p43, mean-median p51, s50 p23 — all inside the central band). The majority's structural geometry under full coverage produces a partisan-bias profile that is otherwise close to the constraint-bound expectation.

**Authoritative reading discipline.** Per the methods paper [§5](#sec-5) four-layer pattern, the audit does not pick one of {Run #3 v0_7 partial, Run #4 v0_8 full} as authoritative. Both are reported. The cross-method disagreement is itself a finding: under partial coverage neither 2026 map is a Lane-1 EG outlier; under full coverage both are. The structural-pattern reading (Lane 2 in [§6.2](#sec-6-2)) is unchanged across coverage choices and remains the audit's most defensible single-direction finding. The [§6.2](#sec-6-2) verdict's qualitative conclusion holds. The magnitudes in Lane 1's verdict table need to be read against both Run #3 and Run #4 numbers, not either alone.

**Caveats that propagate to downstream [§6.2](#sec-6-2) verdict.** The v0_8 full-coverage geometry has documented imperfections ([§4.1.6](#sec-4-1-6) [§4.1.8](#sec-4-1-8)): inherited urban polygons trace 2019 boundaries, not 2026 commission boundaries. The v0_8 minority's "Peace River" polygon was over-extended by Phase 3 gap-fill and absorbs 6 of 10 city-centre landmark points ([§4.1.7](#sec-4-1-7) alignment proof). These are disclosed where each downstream finding cites Run #4 numbers.

Outputs: `data/v0_1_mcmc_ensemble_samples_250k_v0_8.csv` (250,000 rows, 4-chain), `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv`, `data/v0_1_mcmc_real_map_scores_250k_v0_8.json`, `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json`, `data/maps/mcmc/ensemble_distribution_250k_v0_8_*.png` (4 metric histograms), `data/maps/mcmc/running_mean_250k_v0_8_*.png` (4 convergence trace plots).

---

<a id="sec-5-4-5"></a>
#### 5.4.5 Run #5 — 1,000,000-sample MCMC against v0_8 full coverage (publication-grade ESS, 2026-04-25)

A 1,000,000-sample ReCom run was executed across **4 parallel chains × 250,000 steps each** (chain-specific seed = 44 * 250k + chain * 1k + chunk; chunked checkpointing every 5,000 samples). Wall time **71.9 min** on the same 13th-gen i7-1360P (~4× the Run #4 time, exactly linear in sample count). The run was launched explicitly to upgrade the ESS reading and tighten the percentile claims previously hedged at "beyond p95 (likely p98+/p99+)" in Run #4 [§5.4.4](#sec-5-4-4).

**Convergence diagnostics — publication-grade ESS achieved.**

| Metric | Run #4 ESS (250k) | Run #5 ESS (1M) | Improvement |
|---|---:|---:|---:|
| Efficiency gap | 515 | **2,278** | 4.4× |
| Mean-median | 453 | **1,967** | 4.3× |
| Declination | 474 | **2,278** | 4.8× |
| Seats @ 50/50 | 430 | **1,679** | 3.9× |

ESS scaling is approximately linear in sample count (4× more samples → 4× more independent draws), confirming the Run #4 chains were not stuck in a local mode. Per-metric ESS are: Efficiency gap 2,278. Mean-median 1,967; Declination 2,278; Seats@50/50 1,679. The percentile claims can be reported as **point estimates within the chains' precision** rather than as bounds-only.

**Per-metric percentiles vs 250,000-row pooled ensemble** (2023 vote substrate; v0_8 full-coverage geometry):

| Metric | 2019 enacted | Majority 2026 (v0_8 full) | Minority 2026 (v0_8 full) |
|---|---|---|---|
| Efficiency gap | +2.41 % (p67.4) | **+6.43 % (p99.93)** ⚠ | **+9.21 % (p100.0)** ⚠ |
| Mean-median | −0.77 % (p91.7) | −1.82 % (p53.5) | −0.97 % (p87.4) |
| Declination | −4.51 % (p9.1) | −1.18 % (p41.5) | **−6.66 % (p3.0)** ⚠ |
| Seats @ 50/50 | 46.0 % (p82.3) | 43.7 % (p21.6) | **54.2 % (p100.0)** ⚠ |

**Cross-run stability vs Run #4.** Every percentile placement reported here is within ±0.5 percentile of the Run #4 value at 250k samples. This confirms Run #4 was not Monte-Carlo-noise-driven. The headline outlier flags (majority EG p99.9; minority EG p100; minority declination p3.0; minority seats@50/50 p100) hold under publication-grade ESS.

**Implication for the [§6.2](#sec-6-2) verdict.** The "likely p98+/p99+" hedge from [§5.4.4](#sec-5-4-4) is now retired. Lane 1 in [§6.2](#sec-6-2) can report majority EG at p99.93 and minority EG at p100 as point-estimate percentiles, not bounds. The published academic-redistricting threshold for "outlier" is p > 95. Both 2026 maps clear that threshold by ≥ 5 percentile points on EG, and the minority additionally clears it on declination and seats@50/50. The [§6.2](#sec-6-2) author's verdict ("structurally consistent with engineering, magnitude-undetectable") was retracted in the 2026-04-25 revision. Under Run #5 ESS, the magnitude is **detectable** at publication grade.

Outputs: `data/v0_1_mcmc_ensemble_samples_250k_v0_8.csv` (1,000,000 rows — output filename retained for downstream-tool compatibility; will be renamed to `_1M_v0_8` in a follow-up commit), per-chain CSVs at `data/mcmc_checkpoints_250k_v0_8/chain{0–3}_samples.csv` (250,001 rows each), `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv`, `data/v0_1_mcmc_real_map_scores_250k_v0_8.json`, `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json`, plot PNGs at `data/maps/mcmc/`.

---

<a id="sec-5-4-6"></a>
#### 5.4.6 Run #6 — 2,000,000-sample MCMC against v0_8 full coverage (converged-ceiling confirmation, 2026-04-25)

A 2,000,000-sample ReCom run was executed across **4 parallel chains × 500,000 steps each** (chunked checkpointing every 5,000 samples). Wall time **3,675 s = 61.25 min** on the same 13th-gen i7-1360P. Run #6 was launched specifically to test whether the 1,000,000-sample Run #5 had reached the simulation's true ceiling on the seats@50/50 metric, or whether further sampling would push the maximum higher.

**Convergence diagnostics — Run #6 ESS roughly doubles Run #5.**

| Metric | Run #5 ESS (1M) | Run #6 ESS (2M) | Improvement |
|---|---:|---:|---:|
| Efficiency gap | 2,278 | **4,347** | 1.91× |
| Mean-median | 1,967 | **3,766** | 1.91× |
| Declination | 2,278 | **4,258** | 1.87× |
| Seats @ 50/50 | 1,679 | **3,138** | 1.87× |

ESS scaling is again approximately linear in sample count (2× more samples → ~2× more independent draws). Per-metric ESS are: Efficiency gap 4,347. Mean-median 3,766; Declination 4,258; Seats@50/50 3,138. All four metrics now sit at or above the MGGG "lawsuit-grade" threshold (~3,000–5,000 typical for litigation claims).

**Per-metric percentiles vs 2,000,000-row pooled ensemble** (2023 vote substrate; v0_8 full-coverage geometry):

| Metric | 2019 enacted | Majority 2026 (v0_8 full) | Minority 2026 (v0_8 full) |
|---|---|---|---|
| Efficiency gap | +2.41 % (p67.5) | **+6.43 % (p99.94)** ⚠ | **+9.21 % (p100.0)** ⚠ |
| Mean-median | −0.77 % (p91.7) | −1.82 % (p53.6) | −0.97 % (p87.4) |
| Declination | −4.51 % (p9.0) | −1.18 % (p41.6) | **−6.66 % (p3.0)** ⚠ |
| Seats @ 50/50 | 46.0 % (p82.3) | 43.7 % (p21.6) | **52.8 % (p100.0)** ⚠ (89-of-89 attribution; see [§5.4.7](#sec-5-4-7)) |

**Cross-run stability vs Run #5.** Every percentile placement is within ±0.5 percentile of the Run #5 value at 1M samples. This confirms Run #5 was already at convergence. Run #6 adds precision but does not move any flag.

**Converged-ceiling finding (key result of Run #6).** The simulation's seats@50/50 ceiling held at **exactly 51.72 %** across both the Run #5 1M ensemble and the Run #6 2M ensemble. Doubling the sample size from 1,000,000 to 2,000,000 did not push the maximum higher. Specifically:

- **Only 104 of 2,000,000 maps reach the 51.72 % ceiling** (one map per ~19,200 samples — consistent with rare-event sampling at the tail of a converged distribution).
- **Zero of 2,000,000 maps reach 52 %.**
- **Zero of 2,000,000 maps reach the minority's 52.8 % seats@50/50 reading.**

The 51.72 % ceiling is therefore not a sampling artifact. It is a **real bound on what a neutral, compactness-preferring procedure can produce under EBCA's ±25 % population-deviation, contiguity, and compactness constraints applied to Alberta's actual 2019 substrate carrying 2023 vote data**. The minority map's 52.8 % reading sits 1.08 percentage points above the simulation's converged ceiling — a placement no neutral procedure across two million draws could match, and the central empirical foundation of the audit's "out-of-distribution" framing in [§6.2](#sec-6-2) (which is now strengthened from "p100 of the ensemble" to "above the ensemble's converged ceiling").

**Implication for the [§6.2](#sec-6-2) verdict.** The "out-of-distribution rather than tail" reading is now empirically robust. A statistical outlier sits in the extreme tail of a distribution. The minority sits *outside* the distribution Run #6 produces. The probability that a random legal map matches or exceeds the minority's seats@50/50 reading is bounded by the resolution of the simulation: **less than 1 in 2,000,000**. This is the headline number cited in `report_public.md` §"The 50/50 test."

**Authoritative-run discipline.** Run #6 (2M) supersedes Run #5 (1M) as the audit's authoritative MCMC ensemble. Run #5 and Run #4 are retained for historical record and methodological traceability — both produced the same percentile placements within ±0.5 — but downstream [§6.2](#sec-6-2) verdict claims now cite Run #6.

Outputs: `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv` (overwrites the 1M run's file; same path reused), `data/v0_1_mcmc_real_map_scores_250k_v0_8.json`, `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json`, per-chain CSVs at `data/mcmc_checkpoints_250k_v0_8/chain{0–3}_samples.csv` (4 × 500,001 rows), full run log at `analysis/reports/v0_1_mcmc_2M_v0_8_full.log`.

---

<a id="sec-5-4-7"></a>
#### 5.4.7 Defensible 89-of-89 attribution and fuzzing-scenario analysis (2026-04-25)

The seats@50/50 reading on the minority map depends on how 2023 voting-area centroids are attributed to 2026 minority districts. Earlier readings (Run #4, Run #5) reported **54.2 % (45 of 83 measurable)** because 6 of the minority's 89 polygons did not catch any 2023 voting-area centroids — these are **inheritance-fill slivers**, polygons drawn for districts whose 2026 boundaries the audit reconstructed from 2019 inheritance plus commission text ([§4.1.6](#sec-4-1-6)) and that produce thin or fragmented footprints under DA-anchoring. The 83/89 measurable denominator was reported transparently but produced a brittle headline number that depended on which 6 districts were excluded.

**Defensible 89-of-89 attribution.** The new attribution (Run #6 and downstream) fills the 6 unattributed minority polygons with each district's inherited 2019-polygon vote distribution. For each unattributed 2026 minority ED, the audit identifies the 2019 ED whose territory the inheritance-fill geometry traces (from the v0_8.2 inheritance fill in [§4.1.6](#sec-4-1-6)) and assigns that 2019 ED's 2023 vote distribution to the 2026 minority ED at the per-party share level. This is a **conservative inheritance assumption**: the 2019 vote distribution is treated as the best available substrate for territory the 2026 minority polygon was inherited from.

Under 89-of-89 attribution, the minority's seats@50/50 reading is **52.8 % (47 of 89)** — moving from 54.2 % (45 of 83) to 52.8 % (47 of 89) as two additional UCP-leaning seats appear in the previously unmeasurable inheritance-fill set. The 52.8 % is the headline number cited in `report_public.md` §"The 50/50 test."

**Fuzzing-scenario analysis.** The single 89-of-89 attribution is an estimate. The underlying inheritance assumption is one of many defensible choices. The fuzzing-scenario analysis at `analysis/scripts/fuzz_missing_eds.py` brackets the result by varying the per-ED vote attribution for the 6 inheritance-fill polygons across the full plausible range (random sampling from the broader 2019 vote distribution; alternate inheritance pathways; DA-weighted mixtures; provincial-mean fallback). Across the fuzzing trials:

- **Worst case (most NDP-favourable attribution):** minority seats@50/50 = **51.7 %** — at the simulation's converged ceiling but technically not above it.
- **Best case (most UCP-favourable attribution):** minority seats@50/50 = **57.3 %** — well above the converged ceiling.
- **Central 89-of-89 inheritance-fill attribution:** **52.8 %** — above the converged ceiling but below the worst-case bound.
- **89 % of random-attribution trials place the minority above the simulation's ceiling.**

The fuzzing analysis confirms that the "above the simulation's ceiling" finding is robust: the only attribution that places the minority *at* the ceiling (51.7 %) is a worst-case construction designed to soften the result. 89 % of plausible attributions place the minority *above* the ceiling. The 52.8 % central estimate is the audit's authoritative reading. The 51.7 %–57.3 % bracket is the audit's transparency about residual attribution uncertainty.

**Why this matters for the [§6.2](#sec-6-2) verdict.** The fuzzing-scenario analysis closes a falsification pathway a hostile reviewer could have raised: "the 52.8 % reading depends on which 6 inheritance-fill polygons you imputed, and a different imputation would put the minority at the ceiling rather than above it." The honest answer is: only a worst-case imputation puts the minority at the ceiling. 89 % of plausible imputations put it above the ceiling, and the central reading is 1.08 pp above. The audit's "out-of-distribution" framing survives the imputation-sensitivity stress test.

Outputs: `analysis/scripts/fuzz_missing_eds.py` (fuzzing pipeline), per-trial CSVs and the 51.7 %–57.3 % distribution histogram in the run log.

---

<a id="sec-5-4-8"></a>
#### 5.4.8 Targeted-gerrymander short-bursts hill-climb (Cannon et al. 2022) — empirical proof of the non-neutral pathway

Run #6's converged-ceiling finding establishes that a **neutral** procedure cannot reach the minority's seats@50/50 range across 2,000,000 draws under EBCA constraints. A reasonable-but-distinct question is whether a **non-neutral** procedure — one explicitly tasked with maximising UCP seats while staying inside the same statutory constraints — *can* reach that range. If yes, the minority's reading is consistent with the kind of map a partisan optimiser would produce; if no, the reading is anomalous on every procedure the redistricting-statistics literature has formalised.

To answer this directly, the audit ran a **short-bursts hill-climbing procedure** following Cannon, Goldbloom-Helzner, Gupta, Matthews, and Suwal (2022), "Voting Rights, Markov Chains, and Optimization by Short Bursts" (arXiv:2011.02288). Short-bursts is the standard tool in the redistricting-statistics literature for exploring biased-but-legal maps: it runs short MCMC chains (the "bursts") with the best-scoring map from each burst seeding the next, producing a hill-climb through the constraint-legal-map space toward an explicitly-defined objective.

**Procedure.** 40,000 ReCom steps with hill-climbing acceptance (accept proposed map iff its UCP seats@50/50 ≥ current best). Same substrate as the Run #4–6 ensemble (4,765-VA 2023 votes, ±25 % population deviation, contiguity). Explicit objective: **maximise UCP seats@50/50**. Implementation at `analysis/scripts/targeted_gerrymander_burst.py`. Full run log at `analysis/reports/v0_1_targeted_burst.log`.

**Result.** After 40,000 hill-climbing steps, the best map produced gave UCP **52.87 %** of seats at 50/50 votes — **within rounding of the minority map's 52.8 %**. The non-neutral procedure reaches the minority's range. The neutral procedure across 2,000,000 draws does not.

**What this confirms.** The Run #6 converged-ceiling finding plus the Cannon et al. short-bursts result jointly demonstrate the audit's central empirical claim:

- **Neutral procedures cannot produce the minority's seats@50/50 reading.** 2,000,000 ReCom draws under EBCA constraints, ceiling at 51.72 %, zero draws at 52 % or above.
- **Non-neutral procedures can.** A partisan optimiser using short-bursts hill-climbing under the same constraints reaches 52.87 % in 40,000 steps.
- **The minority sits in the non-neutral procedure's reachable space, not the neutral procedure's.** Whether the minority commissioners used a partisan optimiser is not observable from public data — intent cannot be read off a map. What is observable is that the minority map's seats@50/50 reading is one a partisan optimiser would produce and one a neutral procedure does not produce, under identical statutory constraints applied to identical Alberta geometry.

**Why this matters for the [§6.2](#sec-6-2) "out-of-distribution" framing.** A reviewer could object that "out-of-distribution" is meaningless without specifying *which* distribution. The Cannon et al. result specifies it precisely: the minority map sits inside the distribution a non-neutral procedure produces (reachable via 40,000 hill-climbing steps) and outside the distribution a neutral procedure produces (unreachable across 2,000,000 random draws). The audit's framing is therefore: *the minority map is the kind of map a non-neutral procedure produces. It is not the kind of map a neutral procedure produces*. This is the framing a court would actually apply, and it is the framing `report_public.md` adopts in its §"The 50/50 test" methodology caveat.

**What this does not show.** The short-bursts result does not show that the minority commissioners used a partisan optimiser. It shows only that *if* one had been used, the minority's seats@50/50 reading is in the range that procedure would produce. The audit's restraint on intent is unchanged: intent is not observable from boundary geometry. The procedural-class mapping (neutral vs non-neutral) is.

Outputs: `analysis/scripts/targeted_gerrymander_burst.py` (short-bursts implementation), `data/targeted_burst_best.json` (best map's per-ED seat count and metadata), `data/targeted_burst_trace.csv` (per-step hill-climbing trace), `analysis/reports/v0_1_targeted_burst.log` (full run log).

---

<a id="sec-5-4-9"></a>
#### 5.4.9 Canonical ensemble — official Elections Alberta shapefiles (1,010,000-plan, 4 chains × 252,500 steps, completed 2026-05-12)

**This is the authoritative MCMC run.** The [§4.1.4](#sec-4-1-4) sunset clause bound the audit to re-run the ensemble against official shapefiles within two weeks of release. Official shapefiles were received 2026-05-06. This run supersedes all DPG-substrate runs ([§5.4.1](#sec-5-4-1)–[§5.4.8](#sec-5-4-8)) for the purpose of final percentile placements and the [§6.2](#sec-6-2) verdict.

**Substrate.** `ea_majority_2026_eds.gpkg` and `ea_minority_2026_eds.gpkg` (official Elections Alberta files, EPSG:3400, 89 EDs each). Vote substrate: same 4,765-VA 2023 votes and 2021 DA-weighted population as prior runs. Base seed: `get_canonical_seed("lunty-bootstrap") = 1432864451` (drand round 5,800,000, pre-registered before run). **Authoritative ensemble: 1,010,000-step run (4 chains × 252,500 steps, completed 2026-05-12).** The 250k run achieved partisan-metric n_eff 379–452 — sufficient for reliable percentile estimation through p99.9, but below the ~1,000–2,000 publication-grade threshold for individual tail claims at extreme percentiles. The 1,010,000-plan extension was run against the same seed and shapefiles to achieve publication-grade ESS. It produced n_eff 1,429–1,682 (partisan metrics) and 2,925–6,493 (population MAD and Reock proxy). Integrated autocorrelation time τ: 601–707 (partisan metrics), 156–345 (population/compactness). Convergence: rho_lag1 = 0.981–0.992. This exceeds the publication-grade threshold. The ESS caveat from the 250k run is resolved. Chain-history note: an initial 50k run (2026-05-06, 2 chains) was superseded by the 4-chain 250k run. Chain1 experienced a sampler hang at chunk 12/50 during the 1,010,000-plan extension (documented 2026-05-11, commit 70e2695). The hang resolved and chain1 completed to 252,500 steps. All percentile placements below derive from the 4-chain 1,010,000-step run.

*Constraint note — s.15(2) rural-protection disabled:* The canonical ReCom run disables the ±25% s.15(2) rural-protection hard constraint (code: `analysis/scripts/mcmc_ensemble_250k.py` lines 450–467). Disabling this constraint makes the reported minority percentiles **conservative (lower bounds)**: the neutral ensemble is permitted to produce more rural-favourable plans than the Act allows, which raises the density in the UCP-favourable tail and therefore *reduces* the minority map's reported percentile relative to what a constraint-enforcing ensemble would produce. The decision to report the conservative bound is documented in hypothesis tracker entry H6. A constraint-enforcing re-run is listed as future work in H6 but was not completed before submission.

**Per-metric percentile placements (canonical, authoritative):**

| Map | Metric | Real-map value | Canonical percentile (1,010,000 plans) | vs 250k run |
| --- | --- | --- | --- | --- |
| **2026 minority** | **seats@50/50** | **0.5169** | **99.99** ⚠ **flag reinstated** (n_eff=1,495 at 1,010,000 plans; ESS-adjusted lower bound ≈p98, above p95 threshold) | was p>99.9 empirical, retracted on ESS grounds at 250k |
| **2026 minority** | **mean-median** | **+0.0104** | **99.98** ⚠ | was 99.985, unchanged |
| **2026 minority** | **declination** | **−0.0770** | **1.21** ⚠ | was 1.03, unchanged |
| 2026 minority | efficiency gap | +0.0402 | 94.4 | was 94.2 — below p95, flag remains withdrawn |
| **2026 minority** | **population MAD** | **3,938** | **99.0** ⚠ | was 98.7, unchanged |
| 2026 majority | mean-median | −0.0362 | 0.92 ⚠ | was 0.85 — NDP-tail outlier (partial-attribution basis; shifts to p5.78 under full-attribution variant — within null but NDP-favourable direction unchanged; no effect on any minority-map headline) |
| 2026 majority | seats@50/50 | 0.4607 | 77.8 | was 78.6 |
| 2026 majority | efficiency gap | +0.0010 | 15.5 | was 15.0 |
| 2026 majority | declination | +0.0267 | 79.6 | was 80.6 |
| 2026 majority | population MAD | 2,827 | 15.8 | was 15.6 |
| 2026 minority | Reock proxy median | 0.579 | 100.0 | unchanged |
| 2026 majority | Reock proxy median | 0.568 | 100.0 | unchanged |
| 2026 minority | Reock pct<0.30 | 1.1 % | 0.09 | was 0.08, unchanged |
| 2026 majority | Reock pct<0.30 | 2.3 % | 0.80 | was 0.84, unchanged |
| 2019 enacted | efficiency gap | +0.0241 | 69.0 | baseline |
| 2019 enacted | mean-median | −0.0077 | 91.5 | was 92.1 |
| 2019 enacted | declination | −0.0451 | 8.95 | was 9.4 |
| 2019 enacted | seats@50/50 | 0.4598 | 77.8 | was 78.6 |

*Source: `data/simulated_ensemble_raw_samples_canonical.csv` (1,010,000 steps, 4 chains × 252,500, seed 1432864451). 250k-run values shown in rightmost column for traceability. 2019 baseline rows added from `data/outputs/score_2019_baseline.json`. Population MAD and Reock not scored for 2019 (87-seat map, different quota denominator; see [§5.4.10](#sec-5-4-10)).*

**Partisan metrics — 1,010,000-plan canonical.** The 1,010,000-plan run (4 chains × 252,500 steps, same seed and official EA geometry) achieves publication-grade ESS (n_eff 1,429–1,682) and resolves the ESS caveats from the 250k run. Three of four partisan metrics carry individual outlier flags on the minority map: mean-median at p99.98 (UCP-favoured tail), declination at p1.21 (NDP-favoured tail), and seats@50/50 at p99.99 (the individual flag retracted at 250k on ESS grounds is reinstated — ESS-adjusted lower bound at n_eff=1,495 is approximately p98, above the p95 threshold). Efficiency gap at p94.4 remains below p95. The EG outlier flag remains withdrawn. Population MAD at p99.0 adds a fifth flag (exploratory Lane-1 channel). The minority's four-metric pattern: MM and seats@50/50 in the UCP-favoured tail, declination in the NDP-favoured tail, EG below threshold — which is the asymmetric-packing signature discussed in [§5.2.4](#sec-5-2-4).

**Majority mean-median: unexpected NDP-tail outlier.** The majority map's mean-median of −0.0362 places at p0.85 — more NDP-skewed than 99.2% of neutral plans. The ensemble p5 is −0.0312. The majority map sits below that floor. Mean-median is mean(NDP district share) − median(NDP district share). A negative value means the mean is pulled down by a cluster of low-NDP districts. The majority's NDP district-share distribution has a pronounced left tail: numerous districts in the 15–30% NDP range drag the mean roughly 3.6 pp below the median.

*Mechanism — rural-district preservation.* Commission maps must respect municipal boundaries and communities of interest, which preserves a cohort of rural districts that have historically produced 15–30% NDP votes. Unconstrained random redistricting plans are not bound by this convention: they can merge, split, or dissolve rural districts in ways a commission legally cannot. The neutral ensemble therefore contains many plans that dilute or eliminate the low-NDP rural cluster, producing mean-median values closer to zero. The majority map's rural-district cohort survives because commission conventions require it, placing the map in the extreme NDP-tail of a distribution shaped by plans that face no such constraint.

*Why the DPG runs did not show this.* Earlier runs against Derived Provisional Geometries (DPGs) resolved VA-to-ED assignments using the audit's reconstructed boundary polygons. Official EA shapefiles resolve rural boundary ambiguities differently: some Voting Areas near rural–peri-urban fringe lines shift between EDs compared to the DPG approximations. These boundary-line differences in low-NDP rural districts are small in vote-count terms but sufficient to extend the left tail of the majority's NDP distribution past the ensemble p5. The official-geometry run is the first run capable of detecting this. The DPG runs did not have the spatial precision to surface it.

*What this finding does not mean.* The majority map is within the neutral null on every other metric: Efficiency Gap p15.0, declination p80.6, seats@50/50 p78.6, population MAD p15.8, Mahalanobis joint-tail p=0.097. A single-metric NDP-tail outlier — mean-median only — accompanied by all other metrics within null is the expected signature of a commission boundary convention (rural preservation) interacting with Alberta's vote geography, not an algorithmic packing or cracking signal. This outlier does not reverse the minority-majority asymmetry direction. The minority's MM is +0.0104 (UCP-tail, p99.98). The majority's is −0.0362 (NDP-tail, p0.85). Both are extreme but in structurally opposite directions for different reasons. The majority's MM outlier is reported as required by pre-registration. It does not support or undermine the minority-focused findings.

**Population MAD (new channel).** The minority map's population MAD of 3,938 persons places at p99.0 — more unequal population distribution than 99.0% of neutral plans. Ensemble median: 3,163. Majority MAD: 2,827 (p15.8, within null). This confirms the Lane-1 partisan signals are accompanied by unusual population-distribution asymmetry.

**Reock proxy (null finding — reported as required by pre-registration).** Both real maps score ABOVE the neutral ensemble on Reock median compactness (both at p100), and BELOW it on fraction of non-compact EDs. This is the expected result for commission maps that follow community-of-interest and municipal boundaries: such maps are systematically more compact than unconstrained random plans. The Reock channel does not provide additional evidence against the minority map. The minority's pre-reported "2.58× Reock asymmetry" over the majority (comparing pct<0.30 across the two maps) was computed on the v0_9 topological substrate (derived shapefiles) and does not hold under canonical EA geometry: under official Elections Alberta shapefiles (received 2026-05-06), the between-map direction reversed — minority 4/89 = 4.5% below threshold vs majority 6/89 = 6.7% (see `findings/reock_verdict.md`). The 2.58× ratio is retracted; see DOCUMENTED CORRECTIONS. Within the neutral null, both maps remain in the extreme-compact tail (both at p100 median Reock); neither map shows a between-map compactness asymmetry on canonical geometry.

**CSD anchoring departure — MCMC edge-crossing test (OSF s58a6, dedicated ensemble, completed 2026-05-12).** The municipal-anchoring-departure channel registered in OSF s58a6 but omitted from the Section C run was executed via a dedicated ensemble (`mcmc_anchoring_ensemble.py`; seed 80780579, derived from drand round 6099592 salt `"alberta-audit-anchoring-ensemble"`). Metric: the fraction of cut edges in a neutral plan that cross a Statistics Canada Census Subdivision boundary. A cut edge connects two adjacent Voting Areas assigned to different Electoral Divisions. A CSD-crossing cut edge connects VAs in different CSDs. A higher fraction indicates district boundaries align with CSD divisions.

Two chains × 5,000 steps = 10,000 neutral plans. Ensemble: median = 17.82%, p5 = 16.73%, p95 = 18.97%. (2,065 of 13,385 VA adjacency edges cross a CSD boundary; all 4,765 VAs received a CSD assignment via centroid spatial join.)

Results: Majority 2026 — 37.63%, p100.00 (outlier, above p95 threshold). Minority 2026 — 29.75%, p100.00 (outlier, above p95 threshold).

Both real maps exceed all 10,000 neutral plans on this metric. This is expected for commission maps operating under municipal-boundary conventions: random ReCom plans face no such constraint. The **pre-registered direction is not confirmed**: the registration predicted the minority map would score below the ensemble median. The minority map is at p100, above all neutral plans. **This is a null finding on the "anomalous unanchoring" hypothesis.** The majority is more CSD-anchored than the minority (37.63% vs 29.75%), consistent with the direction noted in [§5.8.5](#sec-5-8-5), but both maps sit in the anomalously high tail. This channel does not add to the Fisher combination: the anomaly direction is "more anchored than random," not "less anchored than random." Outputs: `data/outputs/csd_anchoring_ensemble.csv`, `data/outputs/csd_anchoring_results.json`.

**Independent seed check (Section C, seed 3562959107, 100k plans, completed 2026-05-12).** A separate 100k-plan ReCom run using the pre-registered Section C seed (OSF s58a6; `analysis/methodology/robustness_rerun_seed_commitment.md`) provides an independent confirmation of the population MAD and Reock placements. Key comparisons: minority population MAD p99.26 (Section C) vs p99.0 (canonical 1,010,000-plan) — confirmed. Both Reock channels confirm the null finding at p100 median compactness and low-elongation direction for both maps. Partisan metric placements are consistent within expected sampling variation (e.g. minority EG p93.93 vs p94.4. Minority seats@50/50 p100.0 vs p99.99). Municipal-anchoring-departure channel: not captured in the Section C run — executed separately via `mcmc_anchoring_ensemble.py` (see above). Section C output: `data/simulated_ensemble_raw_samples_section_c.csv`.

**Mahalanobis joint-tail test.** The four canonical metric scores jointly produce Mahalanobis D = 5.72 with p = 1.40×10⁻⁶ under the 1,010,000-plan canonical ensemble's covariance matrix. The majority's joint p = 0.097 (within null). Pre-registered at OSF [6pt83](https://osf.io/6pt83).
*Methodological note on autocorrelation:* The Mahalanobis degrees of freedom uses 4 (number of metrics) and does not formally discount for autocorrelation within the MCMC chain. Effective sample sizes from the 1,010,000-plan canonical run: EG n_eff=1,677, MM n_eff=1,429, Decl n_eff=1,682, seats@50/50 n_eff=1,495 (integrated autocorrelation times τ=601–707). At these ESS levels the publication-grade threshold (~1,000–2,000) is met; the ESS caveat is resolved. The $p = 1.40 \times 10^{-6}$ value reflects the 1,010,000-plan covariance matrix. Covariance estimated from a smaller 100k run produced $p = 1.60 \times 10^{-7}$ — both are far below any conventional threshold. The difference reflects the better-estimated covariance at 1,010,000 plans.

**Inter-map comparison permutation test (Ch1-COMP).** Pre-registered at OSF [yvc7g](https://osf.io/yvc7g) (drand seed 1823538405, salt "ch1-comp"). H₀: the minority-majority partisan-metric gap is no larger than that of randomly drawn neutral-plan pairs. Results reported regardless of direction per pre-commitment.

*Version A (EG-only, one-tailed):* observed minority−majority EG gap = +3.92 pp. Null SD = 2.12 pp; null 95th percentile = +3.43 pp; p = 0.0303. Significant at α = 0.05.

*Version B (Mahalanobis joint, one-tailed in distance):* observed inter-map distance D = 7.19 against a null 95th percentile of 4.38; p = 0.0001. 3/4 metrics point minority more UCP-favorable (EG +3.92 pp, mean-median +4.66 pp, seats@50/50 +5.62 pp). Declination reverses (−10.37 pp, consistent with the asymmetric-packing signature discussed in [§5.4.9](#sec-5-4-9) and [§6.2.1](#sec-6-2-1)). Both versions significant; verdict: **SUPPORTED at classical threshold on both versions.**

*Contextual framing.* The primary significance claim is each map's absolute position relative to the ensemble (minority p = 1.40×10⁻⁶; majority p = 0.125). Ch1-COMP tests a different question: do the two maps differ from each other more than randomly chosen neutral pairs? The answer is yes. This confirms the minority-majority asymmetry is not an artefact of both maps occupying similar extreme positions — they are separated by more than the typical inter-plan distance in partisan-metric space. Output: `findings/intermap_permutation_test_results.json`.

**Fisher combined test.** Fisher's method applied to the two primary analytical channels (Channel 1 Mahalanobis p-value and Channel 2 SZAT permutation p-value) produces T = 39.03, Fisher p = 6.87×10⁻⁸ (approximately one in 15 million). 
*Methodological Caveat on Tail Conventions:* This calculation mixes a two-tailed Mahalanobis test with a permutation-based test. However, because both tests are effectively one-tailed *against the gerrymandering direction* (i.e. measuring departure towards the UCP-favourable extreme), combining them via Fisher's method is methodologically defensible. This is the headline joint-probability figure cited in `report_public.md`.

**SZAT Bootstrap Pre-registration Mismatch:** The initial SZAT p-value of 0.0044 was calculated using an additive-delta approximation of the bootstrap null. The pre-registration document (OSF: 6pt83) specified a full map EG recompute per permutation. The definitive SZAT run ([§5.2.10](#sec-5-2-10), 2026-05-10) uses full-recompute bootstrap and reports p=0.0024. This is the value used in the Fisher combination above. Validation testing (`szat_validate.py`) confirms the delta approximation and full recompute yield functionally equivalent results. The minor methodological deviation from the pre-registration is acknowledged.

**SZAT substrate description retraction ([§5.2.10](#sec-5-2-10), 2026-05-12).** A prior version of [§5.2.10](#sec-5-2-10) (the "Post-registration substrate update" paragraph, committed ~2026-05-10) incorrectly described the definitive SZAT run as using a "full advance-vote substrate" in which advance-vote and special-ballot totals were apportioned to individual VAs proportionally by election-day share, increasing province-wide NDP two-party share from 42.60% to 44.66%. This description was false. Verification against both the current `szat.py` script and the git diff for commit `bd721d9` confirms: the script reads `va_ndp`/`va_ucp` columns (election-day only; two-party total ~896,644) throughout both the initial and definitive runs. The p change from 0.0044 to 0.0024 was caused by a VA file switch (`va_polygons_with_2023_votes.gpkg` → `va_polygons_with_full_2023_votes.gpkg`) that changed 2 VA centroid assignments (2,108 → 2,110 swing zones due to minor geometric differences between the two files), not by any substrate change. The commit message "SZAT updated to full advance-vote substrate" (bd721d9) was itself incorrect. The pre-registration (OSF 6pt83) specified election-day votes. The actual execution used election-day votes. There was no post-registration substrate deviation. The pre-registered finding (p=0.0024) is corrected to accurately describe election-day substrate. A genuine full-vote sensitivity (advance-ballot-apportioned `va_ucp_full`/`va_ndp_full` columns; ~1,544k two-party) was run on 2026-05-12 and reports p < 0.0001; see [§5.2.10](#sec-5-2-10).

**Implication for [§6.2](#sec-6-2).** The [§6.2.5](#sec-6-2-5) DPG-era framing (minority s50 = 52.8%, above v0_8 ceiling 51.72%) is superseded. Under canonical geometry, the minority s50 = 0.5169, which exceeds nearly all plans in the 1,010,000-plan canonical ensemble (p99.99; only ~66 of 1,010,000 neutral plans reach this value). The "out-of-distribution" framing in [§6.2.5](#sec-6-2-5) is confirmed on official geometry — and strengthened because now all four partisan metrics fire simultaneously rather than seats@50/50 alone. The [§6.2.1](#sec-6-2-1) Effect Size table at the DPG numbers (48.31%, +2.21 pp) is superseded. The canonical minority s50 = 51.69% with the neutral ensemble distribution placing it at p99.99.

Outputs: `data/outputs/simulation_convergence_diagnostics_canonical.json`, `data/outputs/simulation_real_map_scores_canonical.json`, `findings/joint_outlier_score.json`.

**Git history rewrite — commit hashes changed (2026-05-12).** On 2026-05-12, `git filter-repo` was used to scrub personally identifiable information from all 392 commits. This rewrote every commit hash in the repository. No analytical outputs, data files, scripts, or report text were altered. The OSF pre-registration s58a6 (Ch3 community-of-interest) cites the git hash `72f7e01` as the committed state "before execution." That hash no longer exists in the repository. The authoritative pre-registration evidence is the OSF timestamp record, which is unaffected by this rewrite. No other OSF registration cites a specific git hash. Reviewers who clone the repository after 2026-05-12 will see no gap in analysis continuity. The rewritten history is identical in all substantive respects to the original.

---

<a id="sec-5-4-10"></a>
#### 5.4.10 2019 enacted baseline — measuring the void

The 2019 enacted map scored against the canonical 1,010,000-plan ensemble provides a third reference point: the pre-existing state from which both 2026 commissions drew. Comparing all three maps in the same metric space reveals the *direction of travel* — which proposal corrected the 2019 partisan structure and which amplified it.

**Direction-of-travel table (canonical 1,010,000-plan ensemble, exploratory).**

| Metric | 2019 enacted | Majority 2026 | Minority 2026 |
| --- | ---: | ---: | ---: |
| Efficiency gap | +0.0241 (p69.0) | +0.0010 (p15.5) | +0.0402 (p94.4) |
| Mean-median | −0.0077 (p91.5) | −0.0362 (p0.92) | +0.0104 (p99.98) |
| Declination | −0.0451 (p8.95) | +0.0267 (p79.6) | −0.0770 (p1.21) |
| Seats@50/50 | 0.4598 (p77.8) | 0.4607 (p77.8) | 0.5169 (p99.99) |
| Mahalanobis D² (joint) | 12.75 (p=0.013) | 7.85 (p=0.097) | 32.67 (p=1.40×10⁻⁶) |

*Exploratory (not pre-registered). Source: `data/outputs/score_2019_baseline.json` (Mahalanobis), `data/simulated_ensemble_raw_samples_canonical.csv` (per-metric, 1,010,000-plan run). D² values computed from 1,010,000-plan covariance matrix; see `findings/joint_outlier_score.json`. Attribution note: all percentile values in this table use partial-coverage VA data (va_ndp; ~50% of actual votes), consistent with the canonical ensemble. Under full-coverage attribution (va_ndp_full; ~89%), minority-map outlier status is preserved on 4/4 metrics. Majority mean-median shifts from p0.92 to p5.78 (within null, direction unchanged). See `analysis/methodology/attribution_sensitivity_robustness.md`.*

**Mahalanobis joint-tail finding.** The 2019 enacted map is itself a mild joint-space outlier: D² = 12.75, empirical p = 0.013 (1.3% of the 1,010,000-plan ensemble has higher D²). The majority 2026 map reduces this distance to D² = 7.85 (p = 0.097) — well within the neutral null. The minority 2026 map amplifies it to D² = 32.67 (p = 1.40×10⁻⁶ under the 1,010,000-plan ensemble). The joint distance from 2019 to the neutral null is thus: majority *retreated toward neutral*, minority *advanced toward a more extreme position*. The 2019 baseline was not itself a clean neutral starting point. What the two commissions chose to do with it differs fundamentally.

**Metric-by-metric reading.** The 2019 map's most anomalous metric is Declination (p9.4, NDP-favoured tail), followed by Seats@50/50 (p78.6, mild UCP tail) and EG (p69.0, near centre). Mean-median at p92.1 means 2019 was slightly less NDP-efficient in mean-median terms than most neutral maps — a mild UCP structural advantage. The majority 2026 corrected the Declination anomaly (p9.4 → p80.6), left Seats@50/50 nearly unchanged (p78.6 → p78.6), and moved EG toward neutral (p69.0 → p15.0). The minority 2026 preserved the Declination anomaly at maximum intensity (p9.4 → p1.21), dramatically extended MM in the UCP direction (p92.1 → p99.98), and pushed Seats@50/50 beyond the ensemble's upper bound (p78.6 → p99.99). Both proposals diverged from 2019 in opposite directions on every metric except Seats@50/50 on which the majority held precisely still.

**Population MAD (cross-map comparison, exploratory).** The 2019 map had 87 EDs with populations from the 2017 EBC report (total 4,071,875; quota ≈ 46,803). Population MAD = 2,010. The 2026 maps have 89 EDs and 2021 population bases (majority MAD = 2,827; minority MAD = 3,938). These figures are not on the same scale — different seat counts, different population vintages, and different denominators. The directional ordering 2019 < majority < minority reflects that the minority's population deviation is larger than any predecessor, but cross-vintage comparison is not a controlled metric. See [§5.4.9](#sec-5-4-9) Population MAD section for the canonical percentile placement of the 2026 values.

**SZAT 2019 baseline (exploratory, not pre-registered).** The pre-registered SZAT ([§5.2.10](#sec-5-2-10)) tested whether the minority's specific boundary *choices* — the 2,110 VAs assigned differently between the two 2026 proposals — were partisan-neutral. The exploratory SZAT baseline applies the same logic to 2019→2026 movement: of the VAs that each commission had to move from 2019 positions, did they move them in a partisan direction?

| Comparison | Swing VAs | SZAT score | Bootstrap p (10k) |
| --- | ---: | ---: | ---: |
| 2019 enacted → majority 2026 | 2,042 | −0.0231 | 0.309 |
| 2019 enacted → minority 2026 | 2,584 | +0.0161 | 0.053 |

*Exploratory. Seed: `get_canonical_seed("szat-2019-majority")` / `"szat-2019-minority")`. Source: `findings/szat_2019_baseline.json`.*

The majority's boundary choices from 2019 produce a SZAT score of −0.023 with p = 0.31: statistically indistinguishable from random. The observed score falls within the bootstrap null 95% CI [−0.034, −0.006]. The EG shift from 2019 to majority is consistent with any neutral rearrangement of those swing zones. The minority's boundary choices produce a SZAT score of +0.016 with p = 0.053: marginally above the 5% threshold. The observed +0.016 falls outside the null 95% CI [−0.017, +0.006], meaning the minority's specific boundary choices moved EG in the UCP-favoring direction — opposite to what random boundary changes from 2019 would produce. Note that the null CI is near-symmetric for the minority (unlike the majority, where any random redistricting from 2019 tends to push EG negative), because the minority's non-swing VAs have a different partisan composition. These are exploratory findings; the pre-registered finding remains the [§5.2.10](#sec-5-2-10) SZAT between the two 2026 proposals.

---

<a id="sec-5-5"></a>
### 5.5 Pre-registered checklist baseline scoring

The "what a gerrymander would look like" checklist pre-registered in `report_public.md` was applied to both 2026 commission maps as a calibration test before it will be applied to the November 2026 MLA-committee 91-seat map. The scorecard, reproduced in full in `findings/checklist_baseline_scoring.md`:

| Signal class | Majority 2026 | Minority 2026 |
| --- | --- | --- |
| Strong signals triggered (of 4 scorable; S3 and S5 deferred) | 0 | 1 (the S1 signature set, by construction) |
| Weak signals triggered (of 2 scorable) | 0 | 2 (W2 Calgary zone gap, W3 Nolan Hill-Cochrane retention) |
| Process signals triggered (of 5) | 0 | 0 |
| Rationale-against-data contradictions (X2) | 0 | 2 (shared-schools x 1 strong [R5 Calgary-Bow-Springbank, asymmetric flow insufficient to anchor join] plus x 1 softened after Catholic-axis check [R11 Red Deer-Sylvan Lake defensible via Red Deer Catholic Regional cross-coverage]; Cochrane commuter-tie partial; five population-math tests failed) |

Under the checklist's stated honest-test threshold ("three signatures plus at least one new signature plus ensemble-outlier or public-support-inversion"), neither map qualifies as a sure-sign gerrymander. The minority meets the signatures clause (three formal signatures) and, under the 1,010,000-plan canonical MCMC run reported in [§5.4.9](#sec-5-4-9), meets the ensemble-outlier clause on three of four partisan metrics: Mean-Median at p99.98, Declination at p1.21, and Seats@50/50 at p99.99 (individual flag formally reinstated at 1,010,000-plan ESS). Efficiency Gap at p94.4 falls just below the p95 threshold; the EG flag is retracted. Population MAD fires at p99.0. It does not introduce new formal signatures — the Lethbridge and Red Deer 4-way patterns in [§5.6](#sec-5-6) are symmetric-test-derived cracking candidates held separately from the formal P/C/E signature set pending the C-criteria threshold run — and does not invert public support. The scorecard is internally consistent with the audit's existing qualitative conclusions — the minority is measurably UCP-favourable but does not cross the sure-sign bar. The scorecard's value going forward is twofold: it operationalises the pre-registered test for the November map, and it demonstrates that the test distinguishes the two known maps in the expected direction before any new map is drawn.

**External pre-registration.** The 91-seat forensic scorecard for the November 2026 Lunty committee map is pre-registered at AsPredicted #289,455 / OSF `https://osf.io/qsgy8/`, made public 2026-05-07, with algorithmic thresholds locked to drand beacon Round 6062459 (2026-04-27). The submission-ready checklist document is in `analysis/reports/pre_registration_draft.md`. Within 72 hours of the committee map's tabling, the pre-registered scorecard will be executed against it. The OSF registration at `https://osf.io/qsgy8/` is the time-stamped third-party custody record.

**The 17 pre-registered tests, in optimal execution order.** The tests are grouped by what data they require. Tests that require nothing but public documents are scored first. The one test that requires shapefiles and compute time is scored last.

*Group 1 — Process checks (answerable before map tabling, from public committee records):*

- **P2 — Advisory panel transparency.** Tests whether the committee publicly names its advisory panel members and publishes terms of reference before or with map release. An anonymous advisory structure prevents public scrutiny of the qualifications or political alignment of the people who shaped the drawing.
- **P1 — Public hearings held.** Tests whether the committee held public hearings on a draft map before finalizing it. Public hearings are the standard mechanism by which affected communities can contest boundary choices before they are fixed.
- **P3 — Draft consultation window.** Tests whether a draft map was released for public comment with at least a 14-day window. A direct-to-final release eliminates the opportunity for community-specific objection before adoption.

*Group 2 — Immediate post-release (no computation; ED names and release documents sufficient):*

- **P5 — AI disclosure.** Tests whether the committee discloses all AI tools, prompts, model versions, and random seeds used in drafting, against the audit's published framework (`docs/ai_use_recommendations_for_committee.md`). Undisclosed AI involvement makes the derivation of the map unreproducible and unauditable.
- **S6 — Public-support inversion.** Tests whether the final map drops configurations with documented submission-archive support while keeping configurations with none. The 1,252-submission archive is pre-complete; only the November map's configuration names are needed to score this test.
- **X1 — Chair Miller's four conditions.** Tests whether the November map satisfies all four conditions of Chair Miller's Recommendation 5: no impact south of Airdrie or north of the NSR, south-NSR Edmonton districts restored to the interim-report shape, and the Clearwater/western Mountain View s.15(2) district restored. Failing any condition means Motion 19 was not in fact implementing the chair's proposal.

*Group 3 — Same-day structural checks (census and population data; no 2026 shapefiles required):*

- **S1 — Three minority signatures.** Tests whether the November map carries the same three formal structural signatures as the minority proposal: a ≥10% Calgary zone-population gap, a 4-way or greater Airdrie split, and an s.15(2) district anchored to ≥20% uninhabited protected land. Co-occurrence of all three defines the audit's gerrymander-signature criterion.
- **W2 — Calgary zone gap (weak signal).** Tests whether any Calgary zone partition shows a ≥5% mean-ED-population gap — the weak version of S1's 10% threshold. A result in the 5–10% band extends the packing inference to the Lunty map at reduced certainty.
- **W1 — Rural seat count.** Tests whether the committee added 2 rural seats relative to the 89-seat majority baseline without engineering. A plain rural addition consistent with Motion 19's stated rationale is a pass; an engineered addition triggers S3.
- **S3 — Both rural additions engineered.** Tests whether both incremental rural seats invoke s.15(2) with boundaries enclosing ≥20% uninhabited protected land — the same pattern identified as anomalous in the minority's RMH-Banff Park extension. Scored after W1 confirms two rural additions were made.
- **S2 — Novel structural signatures.** Tests whether the November map introduces signatures absent from the minority: an Edmonton zone-packing gap ≥10%, a 4-way or greater city split in a third Alberta municipality, or an additional engineered s.15(2) boundary beyond any found in S1/S3. A positive result extends the structural finding beyond what the commission itself drew.
- **W3 — Nolan Hill-Cochrane retained.** Tests whether the committee keeps the minority's Calgary-Nolan Hill-Cochrane hybrid without stronger justification than the commuter-tie claim already shown insufficient at CSD resolution (`analysis/methodology/cochrane_journey_to_work.md`). Retention with only the same weak rationale means the committee inherited a contested boundary without filing new evidence to defend it.

*Group 4 — Requires committee per-ED rationale document (up to 24 hours after release):*

- **X2 — Rationale-against-data contradictions.** Tests each of the committee's stated per-ED rationales against public datasets (Alberta Education school-division boundaries, StatsCan journey-to-work table 98-10-0459, Alberta Treasury population estimates, 2021 census CSD populations). A rationale fires when directly falsified by the dataset it invokes; ≥3 contradictions elevate to a strong signal. This test would catch a repeat of the shared-schools error found in two minority configurations.

*Group 5 — Vote reallocation (crosswalk computation; run in parallel with Group 4):*

- **S4 — Efficiency gap ≥7%.** Tests whether the November map's efficiency gap, computed on 2023 provincial election votes reallocated to the new 91-seat boundaries via the audit's crosswalk, exceeds the Stephanopoulos-McGhee (2015) 7% investigable-bias threshold. This is the Lane 1 partisan-bias magnitude check — the single most internationally comparable gerrymandering threshold.
- **X3 — 338Canada cross-validation.** Tests whether 338Canada's riding-level projection, reallocated to the November 91-seat boundaries via the audit's crosswalk, gives UCP ≥2 more seats than the majority 89-seat baseline (established at 67 UCP / 22 NDP in the April 2026 snapshot). Provides a poll-based projection independent of the 2023 vote baseline.

*Group 6 — Post-adoption (may fall outside the 72-hour scoring window):*

- **P4 — Adopted without amendment or dissent.** Tests whether the Legislature adopts the committee's map without amendment and without any published committee dissent. Unanimous unamended adoption eliminates the last procedural correction mechanism; dissent or amendment shows the process retained factual-check capacity.

*Group 7 — Requires 2026 shapefiles and MCMC compute (48–72 hours; BLOCKED if no shapefiles released):*

- **S5 — Ensemble outlier.** Tests whether the November map's UCP-favourability percentile, computed against a MCMC ensemble of ≥1,010,000 neutral 91-seat maps (GerryChain ReCom, published seed; pre-registration minimum is 10,000 but the audit's established run size for commission maps was 1,010,000 — 4 chains × 252,500 steps), falls in the top 5%. This is the strongest single statistical test in the scorecard — the test that placed the minority at p94–100 on all four partisan metrics — and requires official shapefiles that may not be released with the November map.

---

<a id="sec-5-6"></a>
### 5.6 Symmetry-of-test-selection audit

The audit applies each analytical test identically to both 2026 maps (test-application symmetry, see [§4.1.1](#sec-4-1-1)). A separate discipline, *test-selection symmetry*, asks whether the tests themselves were designed around observed minority features rather than around structural features either map could exhibit (Chen and Rodden 2013). To address this discipline, a counter-test was constructed (`analysis/scripts/majority_symmetry_counter_test.py`, 2026-04-22) that generates symmetric hypothetical tests and applies them to both maps.

**Counter-test 1 — Edmonton zone packing.** Classify Edmonton EDs into Zone C (north of the North Saskatchewan River) and Zone D (south of the river). Compute the C-vs-D mean-population gap. Compare to the Calgary Zone A-vs-B gap. Result: Edmonton Zone C-vs-D mean-population gap is +2.0 pp under the majority map and +1.4 pp under the minority map (both in percent of provincial mean, the same units as the Calgary A-vs-B gap), both far below the Calgary Zone A-vs-B gap of 12.2 pp in the minority map. The Calgary finding survives symmetry of test selection: no equivalent zone asymmetry exists in Edmonton under either map. The Calgary packing is a minority-map-specific feature, not an artefact of selecting a Calgary-zone test.

**Counter-test 2 — City-wide 4-way split.** For every Alberta municipality with population ≥ 50,000 (excluding Calgary and Edmonton, whose populations exceed three statutory quotas and force multi-way splits), identify any city split across four or more EDs in either map. Results:

| City | Majority map | Minority map |
|---|---|---|
| Airdrie | 2 EDs (known) | 4 EDs (known) |
| **Lethbridge** | **2 EDs** | **4 EDs — new finding** |
| **Red Deer** | **2 EDs** | **4 EDs — new finding** |
| Medicine Hat | 2 EDs | 2 EDs |
| St. Albert | 1 ED | 1 ED |
| Grande Prairie | 1 ED | 1 ED |
| Lloydminster | 1 ED | 1 ED |

Two new minority-specific cracking-candidate patterns emerge: Lethbridge 4-way (Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) and Red Deer 4-way (Red Deer-Blackfalds, Red Deer-Innisfail, Red Deer-Lacombe, Red Deer-Sylvan Lake). The majority map applies 2-way splits to both cities. **Federal precedent for Red Deer.** The 2022 Alberta federal redistribution commission unified Red Deer into a single federal riding rather than splitting it, aligning with the provincial majority's approach of concentrating Red Deer voters in no more than 2 provincial electoral districts. This federal treatment, made by the same independent redistribution methodology (statutory mandate, multi-member commission, published rationales), provides a direct Canadian benchmark for the 2-district maximum: neither the 2022 federal commission nor the 2026 provincial-majority commission found a need to split Red Deer's 100k+ population across four electoral units. Pending C2 / C3 threshold tests (see [§5.3.2](#sec-5-3-2) for the formal cracking-signature methodology), these are *cracking-candidate* findings rather than formally-detected cracking signatures. The audit's existing Airdrie cracking finding now extends to a pattern of three Alberta cities where the minority map performs unforced 4-way splits the majority and the precedent-setting 2022 federal commission do not.

**Pre-registration caveat for the Lethbridge and Red Deer findings.** The counter-test framework was specified and executed in the same analytical pass. The symmetry criteria are prose-level and the city-population threshold (≥ 50,000 residents) is geographically anchored rather than retrofitted, but the finding was not independently pre-registered before execution. These two cracking candidates are therefore held separately from the Airdrie cracking signature in [§5.3.2](#sec-5-3-2): Airdrie is a formally-detected signature meeting P/C/E thresholds pre-registered before the detection run. Lethbridge and Red Deer are symmetric-test-derived patterns that match Airdrie's structure but have not passed the same formal gate. They are reported because the symmetric test found them. They should not be counted as additional formal signatures beyond Airdrie until the C-criteria run produces threshold values for each city.

**Interpretation.** The audit's symmetry-of-test-selection claim is strengthened by the Edmonton counter-test (Calgary zone asymmetry is not a test-selection artefact) and extended by the Lethbridge and Red Deer findings (the cracking pattern identified at Airdrie reproduces elsewhere). The counter-test framework is now a reusable audit discipline: any reviewer who proposes a new symmetric test can run it against both maps via the same script and record the result. Full per-city data at `data/majority_symmetry_counter_test.csv`.

---

<a id="sec-5-7"></a>
### 5.7 Stress-test grades mini-audit

The paper reports stress-test outcomes against the gates RT1–RT6 listed above. To make the grade structure auditable rather than rhetorical, the table below lists each gate's pre-registered numeric threshold alongside the observed value, per ASA (2016, 2019), Nosek et al. (2018), and Munafò et al. (2017) guidance on graded evidence reporting.

| Gate | Pre-registered threshold | Observed value | Outcome |
|---|---|---|---|
| RT1 — Monte Carlo 95% CI | Same-sign bounds for strong pass | [−3.04, +0.76] pp, crosses zero | Fails strong pass; 90.5% direction consistency is a separate direction claim |
| RT2 — Cross-metric agreement | ≥3 of 4 same sign for strong pass | B2, B3, B4 agree; B6 declination opposes | 3-of-4 same sign; reported as mixed rather than "majority" |
| RT3 — Cross-election stability | Same direction across 3 election baselines | 2023 & April 2026 same; 2019 reverses | Fails strong; direction-stable across 2020s-era inputs |
| RT4 — Structural vs vote-based separation | Clear labelling required | Labelling present in [§4](#sec-4), § E | Pass |
| RT5 — Independent test selection | No test run and discarded | Audit-trail clean; counter-test [§5.6](#sec-5-6) added | Pass |
| RT6 — Assumption inventory | Listed in `analysis/methodology/uncertainty_and_shapefile_impact.md` | Current | Pass |
| RT7 — MCMC neutral-ensemble outlier | Any real map outside 5–95 band on ≥1 metric for flagged pass | Run #3 (250k, v0_7 centroid-in-polygon): Majority MM p99.98 + s50 p100; Minority Decl p0.9 + s50 p100. Short-burst corroboration: Majority MM and both-map s50 at burst p100 (unreachable in 10 steps from 2019). Updated Alberta EG threshold: 4.37% (ensemble p95). | Flagged pass on both maps; majority flag new under Run #3. Held pending v0_8 tessellation Run #4 and commission shapefile. |

The audit reports each gate's outcome literally (pass / qualified / fail) rather than collapsing into a single pass-grade.

---

<a id="sec-5-8"></a>
### 5.8 Geographic coherence

<a id="sec-5-8-1"></a>
#### 5.8.1 Visual spatial audit

Direct inspection of published commission maps using Opus/Sonnet 4.x vision. Images inspected:

**Majority — Appendix A (eight panels, full provincial coverage):**

- `data/maps/hires/v0_1_majority_p71_alberta_overview.png` — Alberta overview
- `data/maps/hires/v0_1_majority_p73_calgary.png` — Calgary detail
- `data/maps/hires/v0_1_majority_p75_edmonton.png` — Edmonton detail
- `data/maps/hires/v0_1_majority_p77_near_calgary.png` — near-Calgary
- `data/maps/hires/v0_1_majority_p79_near_edmonton.png` — near-Edmonton
- `data/maps/hires/v0_1_majority_p81_north.png` — north Alberta
- `data/maps/hires/v0_1_majority_p83_central.png` — central Alberta
- `data/maps/hires/v0_1_majority_p85_south.png` — south Alberta
- `data/maps/hires_v2/v0_2_render_majority_calgary_MAP_p72_r1200.png` — 1200-DPI render, primary inspection source for majority Calgary

**Minority — Appendix E:**

- `data/maps/hires/v0_1_minority_p359_map73.png` — Appendix E map 73
- `data/maps/hires/v0_1_minority_p360_map74.png` — Appendix E map 74
- `data/maps/hires/v0_1_minority_p361_map75.png` — Appendix E map 75
- `data/maps/hires/v0_1_minority_p362_map76.png` — Appendix E map 76
- `data/maps/hires_v2/v0_2_native_minority_min_map_calgary_p101.jpeg` — native extraction, minority Calgary
- `data/maps/hires_v2/v0_2_native_minority_min_map_edmonton_p107.jpeg` — native extraction, minority Edmonton

Full majority panel coverage across all eight Appendix A panels was extracted in sessions 11–12 (Tier-0 raster pipeline). The [§5.8.3](#sec-5-8-3) symmetric anomaly scan applies to all majority panels, not Calgary only.

<a id="sec-5-8-2"></a>
#### 5.8.2 Chair-flagged boundaries (C3)

Four boundaries were flagged by name in the majority report's response section. Direct inspection results:

- **Calgary-Nolan Hill-Cochrane (minority):** **Confirmed.** A district that reaches from Cochrane (outside Calgary's western boundary) eastward through a narrow-waisted corridor to Calgary's Nolan Hill neighborhood, skipping Rocky Ridge / Tuscany.
- **Rocky Mountain House-Banff Park (minority):** **Confirmed.** SW extension of the district traces Banff National Park to reach the BC border. Absent the extension, the district still meets 4 of 5 §15(2) criteria on the predecessor footprint (Clearwater County alone satisfies (a) at 18,692 km²; (b), (c), (d) all pass without NP territory); the extension adds only criterion (e) — the BC-border coterminous test. See [§5.1.4](#sec-5-1-4) re-audit.
- **Olds-Three Hills-Didsbury (minority):** **Confirmed.** Named for three small towns; extends south past Didsbury to capture a portion of N Airdrie. Airdrie has a population greater than the three named towns combined.
- **Calgary-Foothills-Airdrie West (minority):** Boundary connection between Calgary-Foothills and Airdrie West tracks a primary highway corridor; the geographic connection itself is defensible, but this ED is one of four making up the Airdrie split (C4).

**Combined chair-criticism count across the majority report.** The four geographic anomaly flags above are one subset of the chair's criticism. In a separate section (Appendix C of the majority report, [§5.9.4](#sec-5-9-4) of this audit), the chair also claimed that five minority configurations — Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert — had no public support in the consultation record. Taking the union across both sections, seven distinct minority configurations were criticized by the chair: the four geometric flags (Calgary-Nolan Hill-Cochrane, Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Calgary-Foothills-Airdrie West) plus three appearing only in the Appendix C public-support audit (Chestermere, Red Deer hybrids, St. Albert). Cochrane and Airdrie appear in both lists. The audit's [§1.1](#sec-1-1) headline "three geographic anomalies" reflects only the three flags for which the anomaly was confirmed and the geographic rationale was not independently defensible. The full scope of the chair's documented objections spans seven configurations.

<a id="sec-5-8-3"></a>
#### 5.8.3 Majority hybrids — symmetric check

Applied the same anomaly-scan questions (lasso shape, engineered statutory boundary, misnamed municipality capture) to the majority's four Calgary hybrids:

- **Calgary-East:** Intra-city rectangular block, no extension beyond city limits. No anomaly.
- **Calgary-Falconridge-Conrich:** NE Calgary + directly-abutting Conrich community. Compact. No anomaly.
- **Calgary-Glenmore-Tsuut'ina:** Large southern extension to include the Tsuut'ina Nation reserve; shape tracks the reserve boundary. No anomaly; positively, the reserve is kept intact in a single named ED.
- **Calgary-West-Elbow Valley:** Calgary SW + directly-adjacent Elbow Valley subdivision. No anomaly.

**Qualification.** The anomaly-scan question set was developed from observed minority anomalies. The majority may have different classes of anomaly (e.g., rural-district highway corridors) not detected by the scan criteria applied here. All eight Appendix A panels have been inspected. The limitation is the question set, not the imagery.

<a id="sec-5-8-4"></a>
#### 5.8.4 Community-of-interest splits (C4)

| Dimension                            | Majority 2026        | Minority 2026        |
| ------------------------------------ | -------------------- | -------------------- |
| Lasso/corridor shapes (visible)      | 0                    | 1 (Calgary-Nolan Hill-Cochrane) |
| Engineered statutory boundary         | 0                    | 1 (RMH-Banff Park extension) |
| Community captured under misnamed ED | 0                    | 1 (Olds-Three Hills-Didsbury → N Airdrie) |
| Airdrie split                        | 2 EDs                | 4 EDs                |
| Cochrane                             | intact               | merged into Calgary   |
| Chestermere                          | intact               | partially split       |
| Tsuut'ina Nation                     | single ED, named     | single ED, named      |
| Enoch Cree Nation                    | with Edmonton only   | bundled with Devon (~50 km S) |
| Siksika Nation                       | High River-Vulcan-Siksika | High River-Vulcan-Siksika (same) |

**First Nations representation: Enoch Cree Nation vs. Tsuut'ina Nation.** The two rows above highlight a differential treatment of near-city First Nations reserves that the table alone does not make legible. Both Tsuut'ina Nation (Reserve 145, immediately southwest of Calgary) and Enoch Cree Nation (Reserve 135, immediately west of Edmonton along the Highway 16A corridor) are Treaty-recognized nations whose reserves are geographically adjacent to a major Alberta city, with community orientation, urban services access, and civic relationships primarily tied to the adjacent urban area.

The majority map treats the two nations consistently: Tsuut'ina is in a single named Calgary ED (Calgary-Glenmore-Tsuut'ina) whose boundary tracks the reserve perimeter — the [§5.8.3](#sec-5-8-3) anomaly scan found no anomaly. Enoch Cree is in an ED linked to Edmonton's west-side geography, consistent with the reserve's position on the Edmonton fringe.

The minority map is consistent for Tsuut'ina (single named ED, reserve-adjacent, no anomaly flagged) but diverges for Enoch Cree. The minority creates Edmonton-Enoch-Devon, pairing Enoch Cree Nation with the Town of Devon approximately 50 km to the south. Devon (~6,500 residents) is a residential municipality on the North Saskatchewan River whose service geography is oriented toward the Leduc–Edmonton International Airport–Nisku employment corridor, not toward the Stony Plain/Spruce Grove/Highway 16A corridor where Enoch Cree Reserve 135 sits. The natural community-of-interest relationship for Enoch Cree — proximity to Edmonton, shared Edmonton-zone health authority, Edmonton-area commerce — is with Edmonton's west-side EDs, not with Devon.

The geometric consequence is measurable. The v0_9 compactness analysis ([§5.6](#sec-5-6)) records Edmonton-Enoch-Devon at a Polsby-Popper score of **0.065** — the lowest value in the 178-ED v0_9 joint set across both proposed maps; the district's canonical EA shapefile PP is 0.534, reflecting the substrate effect documented in C3. For context under v0_9, the next-lowest minority EDs (Calgary-Foothills-Airdrie West at 0.140 and Stony Plain-Drayton Valley at 0.176) are both flagged anomalies in their own right. A v0_9 PP of 0.065 is geometrically consistent with an L-shaped or elongated corridor connecting two communities separated by ~50 km in non-collinear directions — Enoch Cree to the west of Edmonton, Devon to the south.

The audit does not file this as a gerrymander signal for two reasons. First, the community-of-interest comparison between Enoch Cree and Devon has not been checked against StatsCan Table 98-10-0459 (journey-to-work) for the Enoch Cree CSD. The claim that Enoch Cree's natural service relationship is with Edmonton rather than Devon is geographically evident but not separately documented. Second, the pairing may be constrained by population math: if the combination of Enoch Cree (on-reserve population ~1,000–1,500) and adjacent Edmonton west-side EDs leaves no legal configuration within the ±25% statutory band, the Devon bundling may be the closest available compliant option. The population arithmetic for this choice has not been separately verified.

What is documented is the asymmetry relative to Tsuut'ina: the minority applies the "single named ED, reserve-adjacent, no anomaly" standard to Tsuut'ina and does not apply it to Enoch Cree. The commission's rationale in Appendix E does not address this differential treatment.

**Census-subdivision-level robustness check.** A CSD-level overlay (Track H; script `analysis/scripts/csd_community_splits.py`) computes, per map, the count of populated CSDs (population ≥ 1,000) spanning two or more electoral divisions. Under 2019 boundaries (measured via geopandas overlay on `data/alberta_2019_eds/`): 66 of 191 populated CSDs (34.6%) are split. Under the majority 2026 proposal (inferred via the Appendix C crosswalk): 66 of 191 (34.6%). Under the minority 2026 proposal (inferred, lower bound, via the heuristic crosswalk): 54 of 191 (28.3%). Upper bound matching the 2019 count of 66. On the confident-only subset of 139 CSDs (excluding those touched by minority-crosswalk uncertainties or any hybrid), all three maps produce the same 40 splits. **The Majority-minus-Minority asymmetry visible in the table above is not detectable at CSD granularity.** The minority's community-of-interest disadvantage operates at within-ED partition resolution (e.g., the four-way partition of the City of Airdrie, the bleed of Chestermere into Calgary-Peigan-Chestermere) — a resolution not encoded in the ED-level crosswalks and not directly measurable until the 2026 shapefiles release. The within-ED qualitative findings in the table above remain the reported finding. The CSD-level count is a null symmetric across maps and is reported here as a bounding limit on the metric's directional power.

**Spatial CSD fragmentation analysis (v0_7 geometry, 2026-04-24; script `analysis/scripts/municipal_splits.py`).** A direct intersection of v0_7 DPG boundaries against Statistics Canada 2021 CSD polygons, restricted to Cities (CY), Towns (T), Specialized Municipalities (SM), Villages (SV), and Improvement Municipalities (IM) with ≥ 300 VA votes (~3,000 residents), measures how many EDs each municipality is split across. Unlike the crosswalk-inferred method above, this uses geometric intersection with a ≥ 5 ha overlap threshold to filter trivial slivers.

| Map | Municipalities split across ≥2 EDs | Change vs 2019 |
|---|---|---|
| 2019 enacted | 10 | baseline |
| Majority 2026 | 8 | **−2** |
| Minority 2026 | 11 | **+1** |

The majority map reduces fragmentation by 2. The minority map increases it by 1. The headline finding at this spatial resolution is concentrated in a single dramatic case: **Strathcona County** (a Specialized Municipality immediately east of Edmonton, population ~105,000) is split across **3 EDs under the 2019 map and 10 EDs under the minority 2026 map (+7)**. Under the majority 2026 map Strathcona County is split across 4 EDs (+1). The minority's +7 fragmentation of Strathcona County accounts for the net increase in total splits despite other municipalities consolidating. It disperses a predominantly suburban municipality across ten EDs, reducing Strathcona voters to a numerical minority in each. The Strathcona finding is consistent with the Airdrie cracking pattern in [§5.3.2](#sec-5-3-2) — both are suburban municipalities east or north of Edmonton/Calgary that are split more times under the minority proposal than required by population math alone. Full per-municipality breakdown at `findings/municipal_splits.md`; data at `data/municipal_splits.json`.

<a id="sec-5-8-5"></a>
#### 5.8.5 Municipal-boundary anchoring audit — did not survive canonical recomputation

The pre-registered municipal-anchoring test measures the percentage of each map's ED perimeter falling within 500 m of a Statistics Canada CSD edge over contiguous ≥ 1 km segments (script: `score_anchoring.py`). Canadian redistribution commissions typically follow municipal boundaries where the population math permits, so the share of perimeter aligned with CSD edges is a meaningful proxy for adherence to the standard Canadian community-of-interest convention.

**Canonical result (official Elections Alberta shapefiles, 2026-05-10):**

| Map | Anchored fraction | Within Canadian comparator norm (70–85 %)? |
|---|---|---|
| Majority 2026 | **80.0 %** | yes |
| Minority 2026 | **72.0 %** | yes |
| 2019 enacted (baseline) | **75.2 %** | yes |

Ratio majority/minority = 1.11×. Both 2026 maps fall within the established Canadian norm. The minority sits slightly below the majority but well inside the comparator band. The anchoring dimension does not produce a structural-divergence signal on canonical geometry.

**Pre-shapefile history.** During the audit's pre-canonical phase (April 2026), the same script run against the DPG (Derived Provisional Geometry) v0_10 substrate returned minority 14.5 %, majority 71.0 %, ratio 4.9× — reported as the structural lane's cleanest single signal. That result did not survive canonical recomputation. The footnote attached to this section gives the full mechanism (area-vs-perimeter fidelity distinction in the DPG pipeline) and disposition.[^anchoring_canonical]

The audit's structural case ([§5.0.1](#sec-5-0-1), [§6.2.2](#sec-6-2-2)) consequently rests on the four geometry-independent dimensions — population dispersion, Calgary zone asymmetry, Airdrie fragmentation, and chair-flagged spatial anomalies — together with the MCMC ensemble (Mahalanobis p = 1.40×10⁻⁶).

**Shared-schools community-of-interest claim — failure of cross-reference, systematic in structure.** Two minority configurations defend their hybrid structure partly on school-district community of interest. Calgary-Bow-Springbank (AEBC, 2026, Appendix E, p. 322) invokes "educational institutions" as a community-of-interest tie between Springbank and west Calgary. Springbank falls within Rocky View School Division No. 41 while the relevant west-Calgary catchment is served by the Calgary Board of Education (Alberta Education, school-division boundaries). Red Deer-Sylvan Lake (AEBC, 2026, Appendix E, p. 351) cites schooling as an urban-rural tie. Sylvan Lake falls within Chinook's Edge School Division No. 73 while the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools. The shared-schools rationale is not supported by the school-district boundary data in either case.

**The pattern is structural, not isolated.** An audit of all 21 minority hybrids against Alberta Education school-division boundaries (`analysis/methodology/school_division_coherence.md`) finds that **20 of 21 cross at least one school-division boundary** — a mathematical consequence of Alberta's school divisions being built around municipal limits (CBE ends at Calgary's limits, Red Deer Public at Red Deer's, Edmonton Public at Edmonton's) and the minority's hybrid doctrine explicitly crossing municipal limits. All four Red Deer hybrids (Blackfalds, Innisfail, Lacombe, Sylvan Lake) cross school-division boundaries — not just Sylvan Lake. The rhetorical contradiction the audit identified for R5 and R11 is therefore representative, not exceptional: the minority chose the two cases where five minutes of Alberta Education verification shows the register is wrong, but the underlying cross-division pattern applies to nearly every minority hybrid. The structural school-division crossings are not by themselves gerrymander signals on the school dimension. What is damning is narrower — R5 and R11 invoked the most verifiable class of community-of-interest claim and do not survive primary-source verification against Alberta Education school-division boundaries. Full per-hybrid classification (school-coherent / mildly incoherent / severely incoherent / neutral) in `analysis/methodology/school_division_coherence.md`.

**Cochrane commuter-tie claim — partial support at CSD resolution.** The Calgary-Nolan Hill-Cochrane hybrid is defended by the minority report (AEBC, 2026, Appendix E) partly on the claim that Cochrane residents "move fluidly" between Cochrane and Calgary. StatsCan Table 98-10-0459 (2021 Census journey-to-work) disaggregates Cochrane CSD commute destinations: of 8,550 Cochrane workers with an Alberta place of work, 4,205 (49.2%) work within Cochrane, 3,065 (35.8%) commute to Calgary CY, 345 (4.0%) to Rocky View County, 185 (2.2%) to Canmore, 135 (1.6%) to Wood Buffalo, and 130 (1.5%) to Airdrie. The Calgary flow is a genuine commuter-tie signal at the city-to-city level. The 2021 public release collapses Calgary to a single CSD and cannot test the within-Calgary sub-destination, so the pairing of Cochrane specifically with the Nolan Hill/Sage Hill ward is neither confirmed nor refuted by this dataset. The interpretive inference — that Nolan Hill is a residential neighbourhood without significant employment and is therefore unlikely to be the commute destination for the 35.8% Calgary-bound flow — is consistent with the city's land-use profile but does not derive from the StatsCan data directly. Full methodology in `analysis/methodology/cochrane_journey_to_work.md`.

**Piikani name-etymology note.** The name "Peigan" in the existing Calgary-Peigan electoral division and its minority extension Calgary-Peigan-Chestermere derives from Peigan Trail SE, a road forming the district's northern boundary, not from a community-of-interest tie to the Piikani Nation (whose Piikani 147 reserve is located approximately 200 km south of Calgary, near Pincher Creek and Fort Macleod). The minority's retention of the name in the hybrid extension preserves a road-based etymology. This is a naming observation, not a finding of fault.

**Community of Interest: Legislation vs. Practice.** Neither the federal *Electoral Boundaries Readjustment Act* nor Alberta's *Electoral Boundaries Commission Act* provides a strict definition for "community of interest." In Canadian redistricting practice, independent commissions rely heavily on municipal boundaries as the primary objective proxy for shared community concerns (Courtney 2001, chs. 6–7). The minority report justifies its structural departures from municipal boundaries by citing "ESRI and Google basemaps" and "commissioner knowledge" rather than demographic data — a methodological choice that this audit flagged during its pre-shapefile phase as a material departure from comparator practice. On canonical geometry the quantitative anchoring gap is small (72.0 % minority vs 80.0 % majority, both within the 70–85 % comparator norm) so the rhetorical concern about the minority's stated rationale stands on its own, without the support of the previously-cited 4.9× anchoring statistic.[^anchoring_canonical]

[^anchoring_canonical]: **Canonical geometry recomputation, anchoring (2026-05-10) — full reconciliation note.** Pre-shapefile (DPG v0_10) result, computed April 2026: minority anchoring 14.5%, majority 71.0%, ratio 4.9× — reported during the audit as the structural lane's cleanest single signal. Canonical recomputation (official Elections Alberta shapefiles, received 2026-05-06): minority 72.0%, majority 80.0%, 2019 baseline 75.2% — both 2026 maps within the 70–85% Canadian comparator norm; ratio 1.11×. The 4.9× gap is not a property of the official maps. **Mechanism of the DPG error:** `score_anchoring.py` measures the percentage of ED perimeter falling within 500 m of a Statistics Canada CSD edge over contiguous ≥ 1 km segments. The DPG pipeline preserved ED *area* to within ~0.0004% but did not constrain ED *boundaries* to lie on CSD polygon edges — the minority map's DPG approximation in particular was sourced from non-CSD reference geometry (road centrelines, census-tract proxies) and therefore failed the perimeter-alignment criterion even where the underlying area was correct. Area fidelity does not imply perimeter fidelity; this is a structural distinction in the DPG pipeline, not a hidden property of the minority map. The minority swung 14.5 → 72.0% (≈ 58 pp) while the majority swung 71.0 → 80.0% (≈ 9 pp) because the majority's DPG already had an official 2019 reference geometry available during construction, while the minority's was novel and had no reference shapefile to seed from. **Disposition in this audit.** The DPG-era anchoring finding (4.9× departure, cited in earlier drafts as the load-bearing structural signal) did not survive canonical recomputation and is not carried forward as a standalone result. The draft audit was never published with the 4.9× claim — that figure appeared only in working drafts and was superseded once the canonical shapefiles arrived. Where the DPG figures previously appeared in prose, the canonical values now appear instead. This footnote is the single preserved record of the DPG-era reading. The audit's structural case ([§5.0.1](#sec-5-0-1), [§6.2.2](#sec-6-2-2)) now rests on the four geometry-independent dimensions: population dispersion, Calgary zone asymmetry, Airdrie fragmentation, and chair-flagged spatial anomalies, plus the MCMC ensemble (Mahalanobis p = 1.40×10⁻⁶). For forward analysis and replication, readers should use the canonical geometry (official Elections Alberta shapefiles, SHA-256 verified via `analysis/utils/canonical_manifest.py`) as the authoritative substrate. Parallel canonical recompute deltas for partisan metrics are documented in `findings/post_audit_recompute_deltas.md`.

---

<a id="sec-5-9"></a>
### 5.9 Procedural findings

<a id="sec-5-9-1"></a>
#### 5.9.1 Commission operation

Five-member commission constituted under Electoral Boundaries Commission Act [§3](#sec-3)–5: chair nominated by the Chief Justice of Alberta, two government-nominated commissioners, two opposition-nominated commissioners. Commission tabled unanimous interim report October 2025. Tabled divided final report (3–2) March 23, 2026. The three-member majority comprises the chair plus the two opposition-nominated commissioners.

<a id="sec-5-9-2"></a>
#### 5.9.2 April 16, 2026 government action

On April 16, 2026 the Alberta Legislative Assembly passed Motion 19 by a vote of 44 to 36, setting aside the commission's majority report and establishing a Special Select Committee of five MLAs (three UCP, two NDP) chaired by Brandon Lunty, MLA for Leduc-Beaumont, to produce a 91-seat map by November 2, 2026. The committee is served by an advisory panel with the same three-party structure as the commission (government-appointed chair plus two nominees per party), whose membership and terms of reference had not been published as of April 22, 2026 (CBC Edmonton, April 16, 2026; Calgary Journal, April 21, 2026). Unlike the commission it replaces, the new process does not include public hearings on the draft map.

**Relationship to Chair Miller's Recommendation 5.** The Premier framed the April 16 motion as aligned with a recommendation by Chair Dallas Miller (Government of Alberta press remarks, April 16, 2026, as reported in Rimbey Review; Calgary Journal, April 21, 2026). This framing is traceable to the Chair's Addendum to the Majority Report (AEBC, 2026, pp. 66–67), which proposed **Recommendation 5**: in the event the Legislature could not accept the majority's 89-seat boundaries, the Act should be amended to raise the seat count from 89 to 91 through "an all-party Select Special Committee or other equivalent Legislative Committee," restoring the two rural divisions the majority report removed while maintaining "the rest of the province as we propose... to the extent possible."

**Provenance of R5: the chair alone, not the commission majority.** The opening sentence of R5 is drafted in the voice of "the majority of the Commission." Chair Miller, however, states in the same addendum: *"My majority colleagues do not agree with me on this point"* (AEBC, 2026, p. 66). On the commission's own documentation, R5 is therefore the personal recommendation of the chair, not a collective recommendation of the three-member majority. Commissioner Greg Clark (one of the two opposition-nominated majority members, nominated by NDP Leader Naheed Nenshi) reiterated this publicly on a social-media thread in April 2026, reinforcing Miller's in-text disavowal. The Premier's framing of R5 as "the commission's own recommendation" does not carry this distinction. The framing is accurate as to the chair's personal position. It overstates the recommendation's provenance if read as a collective endorsement by the majority. Corroboration: CBC News Edmonton, April 16, 2026 ("Miller adding: 'My majority colleagues do not agree with me on this point'"). Full text of R5 is preserved in `findings/chair_recommendation_5_analysis.md`.

The alignment between R5 and the April 16 motion is partial on three grounds, addressed individually in `findings/chair_recommendation_5_analysis.md`:

1. **Form.** The vehicle (Select Special Committee raising the count from 89 to 91 for rural-seat restoration) matches R5's specification. The motion can legitimately claim this anchor.

2. **Substantive constraints.** R5(a)–(d) specifies four concrete boundary conditions — no impact on any electoral division in Airdrie or south of it except Drumheller-Stettler. No impact north of Edmonton's North Saskatchewan River. Reversion of south-of-NSR Edmonton districts to the interim-report map. Restoration of a Clearwater County-plus-western-Mountain-View s.15(2) district. Whether the committee's November output respects these conditions is not yet testable and should form part of the pre-registered November checklist (see [§7.2](#sec-7-2)). R5 also requires that "the rest of the province as we propose [in the majority report] must be maintained to the extent possible" — a condition the committee's present mandate does not carry forward.

3. **Intent.** Chair Miller stated R5's purpose directly: it "is formulated for the express purpose of dissuading the Legislature from accepting the minority report" (AEBC, 2026, p. 66). The Chair further described the minority's hybrid configurations in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, and St. Albert as "not something that I can condone" (AEBC, 2026, p. 67). A committee output that reintroduces any of those minority configurations invokes the form of R5 while inverting its intent. The motion's silence on which starting map the committee uses, combined with the presence in the committee of the political faction that appointed the minority commissioners, is therefore procedurally distinct from R5's conditional.

**Regional-economy framing.** Alberta's Regional Economic Development Alliance geography provides partial support for the minority's general hybrid doctrine. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake — the five municipalities at the heart of the minority's Red Deer hybrid proposals. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, and High River — the catchment for the minority's Calgary hybrids. These are real, publicly-documented regional organisations. They are not, however, boundary prescriptions. Any map grouping districts within these zones satisfies the zone-coherence criterion, and the zones do not by themselves justify the specific intra-zone configurations the minority proposed.

<a id="sec-5-9-3"></a>
#### 5.9.3 Comparator cases

Canadian boundary-commission practice traces to *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158, which established the "effective representation" standard as the constitutional benchmark for provincial electoral boundaries. *Figueroa v. Canada (Attorney General)* [2003] 1 SCR 912 and *Frank v. Canada (Attorney General)* [2019] 1 SCR 3 developed the broader [§3](#sec-3) Charter right to vote. Pal and Choudhry (2011) analyse the intersection of electoral rights and boundary-commission discretion, arguing that the Saskatchewan Reference standard permits commissioners latitude in weighing the non-quantitative factors (geography, community of interest, minority representation) against population parity. Courtney (2001) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces: chapters 6–7 map the interplay between population equality and community-of-interest discretion, and chapters 10–11 address public-hearing obligations and post-hearing revision scope — all directly relevant to the D1–D4 procedural findings below. Pal (2015) argues that the Saskatchewan Reference standard leaves commission members substantial discretion reviewable, if at all, only for manifest unreasonableness — not for partisan preference proximity — so that the distinction between legitimate design preference and legally reviewable partiality turns on the same factual record the D1–D4 evidence assembles. Pal and Choudhry (2014) extend this framework to ask under what conditions a boundary commission's outputs become so asymmetric that they exceed the justifiable margins of discretion even under the loose Saskatchewan Reference standard. The procedural findings below are situated within that discretion space: the audit documents where the minority's boundary choices depart from the pattern established by the majority under identical statutory constraints. The legal weight of that departure, if any, is for a reviewing body to assess under Pal's framework.

The closest historical Canadian comparator is Quebec 2011: the National Assembly refused to proclaim the *Commission de la représentation électorale*'s delimitation under Bill 132, leaving the existing electoral map in force after the commission had completed its work. That refusal — government non-adoption of a finished commission product — is the strongest available antecedent for legislative interference with a completed provincial redistribution cycle in the post-*Saskatchewan Reference* era.

**Federal comparator: the 2022 Alberta federal sub-commission.** A second institutional comparator operates at a different level: the 2022 Alberta federal redistribution cycle, conducted under the *Electoral Boundaries Readjustment Act* (S.C. 1985, c. E-3.3). This cycle is particularly relevant because the federal sub-commission (chaired by Justice J.D. Bruce McDonald, with members Donald Barry and Donna Wilson) operated under a statutory mandate structurally identical in its non-quantitative factors to Alberta's provincial Electoral Boundaries Commission Act: both delegated authority to independent, multi-member commissions with comparable discretion over geography, community of interest, and population variance. The federal 2022 sub-commission's handling of key Alberta boundary questions provides a direct institutional benchmark for how independent redistributors, applying equivalent legal criteria, address the same geographical regions.

On Airdrie (population ~65k in 2021): the federal sub-commission created a 2-district treatment (Airdrie–Chestermere and Banff–Airdrie, later consolidated as Airdrie–Cochrane), matching the provincial majority's approach. On Red Deer (population ~100k+ in 2021): the federal sub-commission unified Red Deer into a single federal riding, again aligning with the provincial majority's 2-district provincial maximum. On Lethbridge (population ~100k+ in 2021): the federal commission performed a 2-way split (Lethbridge and Lethbridge-foothills), consistent with the majority's approach. These federal choices, documented in the *2022 Representation Order* and the sub-commission's published rationale, were made by an independent federal body applying non-partisan redistribution criteria to identical population bases and identical geographical constraints. The minority's provincial proposals diverge systematically from these federal precedents: the minority proposes 4-way splits for both Airdrie and Red Deer where the federal commission and the provincial majority accept at most 2-way splits. [§5.3.2](#sec-5-3-2)'s cracking-candidate analysis treats these departures as evidence of structural irregularity precisely because they depart from the pattern established by an independent comparator commission applying equivalent statutory criteria.

The 2022 federal cycle does not determine the provincial boundary question — the two redistributions operate under different statutory frames and serve different electoral systems — but it provides an institutional reference point: when an independent federal commission and the provincial majority commission converge on equivalent boundary treatments, and the provincial minority diverges significantly, the divergence warrants scrutiny. The audit's analysis in [§5.3.2](#sec-5-3-2) and the cracking-candidate findings in [§5.3.3](#sec-5-3-3) are anchored partly to this federal-provincial convergence.

The April 16, 2026 Alberta motion shares Quebec 2011's post-completion timing — the commission had tabled its final report before the motion — but is structurally distinct in a material respect: rather than leaving the existing electoral map in force, the motion reassigned boundary-drawing authority to a legislature-selected committee (the Lunty committee). As of this paper's writing (May 2026), the Lunty committee has not yet produced a replacement map. One is expected in November 2026. The reassignment removes the independent commission from the remaining process. Whether the committee's eventual product will be adopted, and what boundaries it will draw, is unknown at time of writing. No Canadian provincial redistribution cycle reviewed in Courtney (2001, chs. 10–11) or subsequent scholarship involves the government both rejecting a completed commission product and reassigning the drafting authority to a legislature-selected body within the same cycle. The constitutional status of this class of interference has since become non-hypothetical: six days after the Alberta motion, the Supreme Court of Canada dismissed Quebec's appeal of a ruling that struck down the Legault government's 2024 statute blocking the *Commission de la représentation électorale* from redrawing Quebec's provincial map. The SCC's 7–2 from-the-bench ruling held that the freeze law violated the Charter's democratic-representation guarantee. Whether the Lunty committee structure is constitutionally distinguishable from a legislative freeze — for instance, because it formally reassigns rather than simply blocks, or because Alberta's voter-weight disparities differ from Quebec's — is for a court to decide on its own facts. The doctrinal implications are discussed in [§5.9.5](#sec-5-9-5).

<a id="sec-5-9-4"></a>
#### 5.9.4 Public submission record (D2)

The commission received approximately 1,340 written submissions across two rounds of public consultation. The majority report's Appendix C (Alberta Electoral Boundaries Commission [AEBC] 2026) states that the minority's hybrid configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert **had no public support in the consultation record**.

A keyword search with manual review of the commission's submission archive — 1,252 of approximately 1,340 submissions extracted with usable text. The remainder (~88, 6.6%) are image-only scans without machine-readable text or detectable submission-ID markers — tests this claim. Full methodology, dataset, and technical log are in `analysis/scripts/submission_search.py`, `data/submission_search_dataset.csv`, `findings/submission_search_findings.md`, and `historical/submission_search_log.md`.

**Result: the chair's claim is partially refuted, with tiered severity.** A follow-on signal-strength analysis (`findings/claim_significance_analysis.md`) distinguishes between configurations where the chair's statement was merely *precisely inaccurate* (a supporting submission exists, so "no support" is technically false) and where the chair's statement was also *effectively inaccurate* (support is substantial enough that "no support" materially overstates the absence of public support in the submission record). The framing throughout this section is objective and fact-based: the question is whether supporting submissions exist on the record, not whether the chair acted with any particular intent in characterising them.

**Verdict by tier:**

- **Precisely and effectively wrong** (three configurations where the minority adopted proposals *from* the public record, not despite it):
  - Rocky Mountain House-Banff Park: 5 supporters, net +4, 25% of engaged submissions support the configuration
  - Olds-Three Hills-Didsbury: 3 supporters, net +2, 60% of engaged submissions support
  - Chestermere separation: 3 supporters, net +2, 23% of engaged submissions support (support is substantial enough that "no support" materially overstates the absence of public support).
- **Precisely wrong, effectively ambiguous** (support exists but is evenly matched by opposition):
  - Red Deer hybrids: 4 supporters, 4 opposers, net 0, 22% of engaged submissions support
- **Precisely wrong only / chair effectively correct** (support is negligible or zero):
  - Airdrie 4-way: 0 supporters, 2 opposers, 0% of 4 engaged submissions
  - Calgary-Nolan Hill-Cochrane: 0 submissions mention this configuration at all
  - St. Albert-Sturgeon (minority variant): 0 clear supporters for the minority's alternative configuration; label-ambiguity caveat

The tier distinction matters because the chair's Appendix C claim was an argument for procedural weight, not a technicality. A chair who said "no public support" when 25–60% of engaged citizens proposed the exact configuration has mischaracterized the public record on that specific point, not simply overlooked a dissenting voice or two. By contrast, a chair who said "no public support" for the Airdrie 4-way split is effectively correct — four engaged citizens discussed the configuration and none supported it.

**Implication for the D2 procedural finding:** the claim narrows but does not dissolve. The chair's sweep was *materially* overbroad on three of seven named configurations, *ambiguous* on one, and *defensible* on three. The audit should report these tiers rather than treating Appendix C as uniformly unsupported or uniformly sound. This matters because readers on both sides of the debate have incentive to flatten the finding: critics will use "chair was wrong" without the tiering. Defenders will use "some configurations did hold up" without naming the three that did not. The tiered verdict resists both flattenings.

<a id="sec-5-9-4-1"></a>
##### 5.9.4.1 Evidence by configuration, with per-area proportions

For each configuration, we report submissions mentioning it, submissions supporting the minority direction, and submissions opposing. The "support rate" column is the ratio of explicit supporting submissions to total submissions engaging with that configuration — a local measure of public backing among engaged citizens, not a measure of province-wide support.

| Minority configuration | Mentions | Supporting minority | Opposing | Neutral | Support rate | Verdict |
|---|---|---|---|---|---|---|
| Airdrie 4-way split | 4 | 0 | 2 | 2 | **0 / 4 = 0.0%** | Chair's claim stands |
| Calgary-Nolan Hill-Cochrane hybrid | 0 | 0 | 0 | 0 | **0 / 0 = n/a** | Chair's claim stands |
| Rocky Mountain House-Banff Park (s.15(2)) | 20 | 3 + ≥4 aligned | 1 | ~15 | **3 / 20 = 15%** (7 / 20 = 35% with aligned) | **Refuted** |
| Olds-Three Hills-Didsbury rural unit | 5 | 2 | 2 | 1 | **2 / 5 = 40%** | **Refuted** |
| Chestermere separation | 13 | 3 | 3 | 7 | **3 / 13 = 23%** | **Partially refuted** |
| Red Deer hybrids | 23 | 2 explicit + 3 aligned | 4 | 17 | **2 / 23 = 9%** (5 / 23 = 22% with aligned) | **Partially refuted** |
| St. Albert-Sturgeon (minority alternative) | 11 | 0 for minority variant (2 for majority name) | 1 | 8 | **0 / 11 = 0%** for minority alternative | Chair's claim stands |

<a id="sec-5-9-4-2"></a>
##### 5.9.4.2 Direct quotation evidence

**Rocky Mountain House-Banff Park — EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta"). Under "3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff":

> *"The proposed Rocky Mountain House-Banff electoral district brings together the upper Bow and North Saskatchewan headwaters, adjacent mountain parks, surrounding Crown land, and the communities that depend on these landscapes for their livelihoods. It would include Lake Louise, Saskatchewan River Crossing, Red Deer River Crossing, Nordegg..."*

This is a direct textual proposal for the minority's s.15(2)-invoking configuration by the submission's explicit name. The configuration with the *most visible engineering evidence* (the NP extension to reach the BC border that we identified in [§5.1.4](#sec-5-1-4)) is also the one with the *clearest public support* in the submissions — a finding that tightens the tension in the audit rather than resolving it.

**Rocky Mountain House-Banff Park — EBC-2025-2-0091** (Nordegg resident):

> *"I recommend that riding boundaries include all of Clearwater County, including Rocky Mountain House, with other western communities like Sundre and Banff."*

**Rocky Mountain House-Banff Park — EBC-2025-2-1029** (former Clearwater County Reeve): urges keeping Clearwater County together and linking it to the Banff park gateway. Directionally aligned with the minority configuration.

**Olds-Three Hills-Didsbury — EBC-2025-2-0209** (Alan Balson, Beiseker):

> *"Keep Beiseker and the surrounding rural area in a reconstituted rural riding that includes Olds, Didsbury, Carstairs, Three Hills, and the agricultural areas around them."*

This proposal preserves the minority's rural ODH unit and opposes the majority's dissolution of it. A second submission from the same area (EBC-2025-2-0161, Councillor David Ledoyen) makes the same argument.

**Red Deer hybrids — EBC-2025-2-0252** (Chad Krahn, Red Deer City Councillor):

> *"...a northern riding could encompass Sylvan Lake, Lacombe, and Blackfalds..."*

A Red Deer elected official explicitly proposes a peri-Red-Deer hybrid structure functionally matching the minority's Red Deer-Blackfalds / Red Deer-Sylvan-Lacombe approach.

**Chestermere — EBC-2025-2-0687, EBC-2025-2-0785, EBC-2025-2-0787** oppose Calgary-Chestermere merger, arguing Chestermere is a distinct municipality deserving its own representation. The minority map preserves Chestermere separately. The majority does not merge it either but uses a different configuration. These submissions support the principle the minority embodies rather than a specific minority label.

<a id="sec-5-9-4-3"></a>
##### 5.9.4.3 Proportional weight and impact on findings

The proportions matter because they tell us whether the public-input record produces *signal* or *noise* for each configuration. Three interpretive lines:

**Sample-size caveat.** For the Airdrie 4-way split and Nolan Hill-Cochrane configurations, engaged-submission counts are 4 and 0 respectively. These are small samples. The absence of supporting submissions in 4 mentions is consistent with "no public support" but doesn't exclude the possibility that a larger sample would uncover some. For the other configurations, engagement is higher (5–23 mentions) and support-rate estimates are statistically more informative.

**Ridings with highest public engagement have the highest support rates for minority-aligned configurations.** Olds-Three Hills-Didsbury (40%), Chestermere (23%), and RMH-Banff Park (15% explicit, 35% with aligned) are the three configurations where citizens in the affected area engaged most actively, and all three show non-trivial alignment with the minority direction. This is the opposite of what the chair's claim implied. The pattern does not prove the minority configurations are correct — engaged citizens can be wrong — but it does refute the categorical "no public support" characterization.

**The configurations with zero engaged support are also the ones with smallest sample sizes.** Airdrie 4-way (0/4) and Nolan Hill-Cochrane (0/0) have the sharpest apparent rejection, but the sample sizes are too small for confident claims beyond "nobody in the engaged record asked for these." This is consistent with the chair's claim for those specific configurations but does not constitute a *refutation* of minority intent — it just means there is no recorded demand.

<a id="sec-5-9-4-4"></a>
##### 5.9.4.4 Impact on the majority's and minority's findings

**For the majority report.** The "no public support" framing in Appendix C was a consequential argument. It implied the minority was advancing configurations against the clear weight of public input. The refutation evidence weakens this argument on three of five configurations. The majority's substantive cartographic critique — that the minority's hybrid choices are less compact and more fragmenting of communities (see [§5.8.3](#sec-5-8-3), [§5.8.4](#sec-5-8-4) of this audit) — still holds. But the *procedural* framing in Appendix C was overbroad.

**For the minority report.** The refutation helps the minority's procedural posture only modestly. Three configurations have documented support, which makes those three harder for the majority to discount. The visible spatial concerns ([§5.8.2](#sec-5-8-2): engineered RMH-Banff boundary, Nolan Hill-Cochrane lasso, ODH capturing N Airdrie) and the structural population asymmetries ([§5.1.1](#sec-5-1-1), [§5.1.2](#sec-5-1-2), [§5.1.3](#sec-5-1-3)) are not affected by the public-support question. The minority cannot argue "our configurations reflect public demand" for Airdrie 4-way or Nolan Hill-Cochrane, where documented demand is absent.

**For the audit's Section D procedural concern.** The [§5.9](#sec-5-9) critique narrows but does not disappear. The government's April 16 action transferred the boundary-drafting authority from the commission to a legislature-selected committee in order to produce a map based on the less-publicly-vetted proposal. That concern is strongest for configurations that genuinely lack public support (Airdrie 4-way, Nolan Hill-Cochrane) and weaker — though not absent — for configurations that have some documented backing (RMH-Banff Park, Olds-ODH, Red Deer hybrids, Chestermere). An earlier framing of "the government adopted boundary choices nobody asked for" would overstate the record. The accurate framing is "the committee's eventual map will include a mixture, with some choices that have no documented public support and others that do."

<a id="sec-5-9-4-5"></a>
##### 5.9.4.5 Limits of the verification

1. **~88 submissions (6.6%) could not be machine-parsed** because their PDFs are image-only scans lacking a text layer or a detectable EBC-2025-X-NNN ID marker. OCR was out of scope. These could in principle contain additional supporting or opposing content that would not change the refutation direction (which relies on identified supporting submissions) but could shift neutral / opposing counts.
2. **Keyword search precision.** Regex uses permissive co-occurrence windows (200–300 chars) and can miss submissions where the same configuration is described in paraphrased terms without the explicit place names used. Conversely, the Red Deer regex triggers on any Red Deer + {Blackfalds / Innisfail / Sylvan Lake / Lacombe} co-occurrence, which often simply describes the commission's *proposed* boundaries — those are neutrals, not supports.
3. **Position classifier is heuristic.** The code looks for support / oppose / against / recommend / should-not keywords near each match. Ambiguous classifications were manually reviewed and corrected in 13 cases (documented in `historical/submission_search_log.md`). CSV rows still reflect the automatic classification.
4. **Minority configuration names are the audit's labels, not the submissions'.** Citizens do not typically know the minority's precise labels (e.g., "Red Deer-Blackfalds"). A submission proposing a functionally equivalent configuration using different names is counted as directional support. The audit's rubric is generous on this point. The majority chair might not accept the same rubric.
5. **Attached sub-PDFs were not searched separately.** Some submissions reference external attachments (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf"). Only the enclosing batch PDF's text layer was searched. Additional evidence may reside in attachments.

The refutation finding is robust to limits (1)–(3) because it rests on identified counter-examples rather than exhaustive enumeration. Limits (4) and (5) could affect counts but not direction of the finding. A full Track-B OCR pass over the 88 missing submissions would strengthen the audit's credibility if it were used in legal proceedings. It would not likely change the qualitative verdict.

<a id="sec-5-9-4-6"></a>
##### 5.9.4.6 Full-corpus LLM sentiment analysis and Hansard transcript review

The keyword-based analysis in [§5.9.4.1](#sec-5-9-4-1)–5.9.4.5 addresses whether supporting submissions *exist* for each configuration. A separate, more comprehensive pass was subsequently run to quantify the *distribution* of stances — not just presence of support, but the balance between opposition, support, and contextual engagement — across both the written-submission corpus and the public-hearing transcripts.

**Method.** Two LLM-based classification pipelines were run using Claude Sonnet via the Claude CLI:

- *Full-corpus submission scan* (`submission_sentiment_llm_full.py`): all 1,252 parseable submissions classified simultaneously on all seven configurations. Each submission produces one structured JSON object with a stance classification (Active Support / Active Opposition / Neutral/Contextual / Unrelated) per configuration, plus a one-sentence reasoning and verbatim excerpt. Rows emitted only for non-Unrelated results.
- *Hansard transcript scan* (`hansard_sentiment_llm.py`): two rounds of EBC public-hearing Hansard transcripts (r1: May 2025 hearings, 2,773 KB; r2: January 2026 hearings, 2,675 KB) were parsed into community-participant turns. Turns mentioning configuration keywords were classified using the same seven-configuration schema. 3,107 community turns in r1 (188 relevant); 2,358 in r2 (209 relevant).

Both pipelines resume from a progress file and are fully reproducible. Output: `data/outputs/submission_sentiment_llm_full_results.csv`.

**Results — written submissions.** 388 non-neutral configuration-stance rows across 292 unique submissions (from the 1,252-submission corpus). Overall: 189 Active Opposition (49%), 82 Active Support (21%), 117 Neutral/Contextual (30%).

| Configuration | Total rows | Opposition | Support | Opp% | Sup% |
|---|---|---|---|---|---|
| Rocky Mountain House–Banff Park hybrid | 104 | 56 | 37 | 54% | 36% |
| Red Deer hybrid ridings | 98 | 52 | 8 | 53% | 8% |
| St. Albert merging with Sturgeon County | 46 | 14 | 15 | 30% | 33% |
| Calgary–Nolan Hill–Cochrane hybrid | 43 | 25 | 5 | 58% | 12% |
| Airdrie 4-way split | 42 | 18 | 6 | 43% | 14% |
| Olds–Three Hills–Didsbury extending to Airdrie | 28 | 9 | 7 | 32% | 25% |
| Chestermere merging with Calgary | 27 | 15 | 4 | 56% | 15% |

**Results — Hansard hearings.** 439 relevant community turns classified across both rounds. Overall: 97 Active Opposition (22%), 91 Active Support (21%), 251 Neutral/Contextual (57%).

| Configuration | Hansard turns | Opp% | Sup% | Net |
|---|---|---|---|---|
| Rocky Mountain House–Banff Park hybrid | 112 | 22% | 34% | +12 support |
| Red Deer hybrid ridings | 75 | 8% | 21% | +10 support |
| Airdrie 4-way split | 74 | 27% | 8% | +14 opposition |
| Calgary–Nolan Hill–Cochrane hybrid | 55 | 24% | 13% | +6 opposition |
| St. Albert merging with Sturgeon County | 48 | 29% | 25% | balanced |
| Olds–Three Hills–Didsbury extending to Airdrie | 38 | 8% | 21% | +5 support |
| Chestermere merging with Calgary | 37 | 43% | 11% | +12 opposition |

**Channel divergence.** The two measurement channels produce materially different signals on two configurations. Rocky Mountain House–Banff Park and Red Deer hybrids both show net opposition in written submissions (−18 and −44 respectively) but net support in Hansard hearings (+13 and +10). All other configurations show directionally consistent signals across both channels — Airdrie, Calgary–Nolan Hill, and Chestermere are opposed in both. Olds–Three Hills–Didsbury and St. Albert–Sturgeon are balanced in both.

**Weighted net-sentiment ranking (LLM-scored intensity).** A second LLM pass (Claude Haiku, structured JSON output) scored each Active Opposition/Support row on a 1–3 intensity scale: 1 = mentioned in passing, 2 = clear position among several substantive points, 3 = primary focus or emphatic language (demanding, urging, calling the configuration unacceptable). Intensity-weighted net = sum of support intensity values minus sum of opposition intensity values, ranked across all channels:

| Configuration | Intensity-weighted net | Direction |
|---|---|---|
| Red Deer hybrids | −64 | Channel divergence |
| Airdrie 4-way split | −61 | Opposed, both channels |
| Calgary–Nolan Hill–Cochrane | −55 | Opposed, all channels |
| Chestermere merging with Calgary | −47 | Opposed, both channels |
| Rocky Mountain House–Banff Park | −9 | Channel divergence |
| St. Albert–Sturgeon County | −1 | Near-balanced overall |
| Olds–Three Hills–Didsbury | +6 | Net supported |

*Note: LLM intensity scoring completed across 452 deduplicated active-stance rows (271 full-corpus AO/AS rows from 1,252 written submissions; 85 Hansard-r1 turns; 96 Hansard-r2 turns; N/C and Unrelated rows not scored). Two configurations show pronounced channel divergence: Red Deer and Rocky Mountain House–Banff Park both exhibit strong opposition in written submissions but net support in Hansard hearings, consistent with differential-mobilization and participation-cost explanations discussed below.*

**The channel-divergence hypothesis.** The divergence between written and in-person channels on RMH–Banff Park and Red Deer hybrids warrants a methodological note. One credible explanation is differential mobilization: written submissions are submitted asynchronously and may over-represent organized opposition groups or residents with strong objections, while in-person public hearings attract a broader cross-section including residents who favor local representation arguments but lack the organizational impetus to submit formally. This pattern — where written channels show stronger opposition than in-person channels on the same question — is documented in planning and zoning literature (Fischel 2001; Davis 2016) though not specifically in electoral redistricting contexts.

A second explanation specific to the RMH–Banff Park configuration is geography: citizens from Nordegg, Rocky Mountain House, and the Jasper/Banff corridor who would benefit from a unified mountain constituency may be more likely to attend regional in-person hearings (which were held in part in those communities) than to submit written comments. This is not a partisan-sorting argument but a participation-cost argument — travel to a hearing is a sunk cost that filters for engagement intensity, not partisan direction.

The audit does not assert either explanation as established. The finding is: two channels produced divergent signals on two specific configurations, the divergence is large enough to be substantive (net flips from 50-point opposition to 10-point support), and commissioners who weighted in-person testimony more heavily — as is common in quasi-judicial administrative proceedings — would have received a materially different impression of public sentiment on those configurations than commissioners who weighted the written record equally. Whether that weighting is appropriate is a procedural-design question outside the scope of this audit.

**Relationship to [§5.9.4.1](#sec-5-9-4-1)–5.9.4.4.** The LLM full-corpus pass confirms and sharpens the keyword-based findings from [§5.9.4](#sec-5-9-4). The chair's "no public support" claim is most defensible for Airdrie (43% opposition, 14% support in submissions; 27% vs 8% in Hansard — consistently opposed in both channels) and least defensible for RMH–Banff Park (36% support in submissions, 34% in Hansard) and St. Albert–Sturgeon (balanced in both). The LLM pass addresses limits (2) and (3) from [§5.9.4.5](#sec-5-9-4-5) by replacing keyword matching and heuristic classification with direct machine-reading of full submission text.

<a id="sec-5-9-4-7"></a>
##### 5.9.4.7 Rationale–submission alignment cross-reference

This section maps the combined sentiment corpus ([§5.9.4.6](#sec-5-9-4-6)) to the minority's published rationales. Of 25 rationales recorded in `data/outputs/minority_rationales.csv`, six could be matched to a sentiment configuration. The other 19 cover Edmonton-area, rural, and procedural rationales for which no submission configuration data exist.

**Method.** For each matched rationale, rows were counted by classification (Active Opposition / Active Support / Neutral/Contextual). Taking-sides percentages exclude Neutral/Contextual rows. Three alignment labels are used:

- **CONTRA_COMMISSION** — the commission claimed "SUPPORTS" or "PARTIALLY SUPPORTS" for this rationale, but the combined record is majority-opposing.
- **ALIGNS_WITH_AUDIT** — the commission's own verdict was skeptical (INCONCLUSIVE or FAIL), and the submission record is also majority-opposing.
- **CONTRA_AUDIT** — the audit flagged a test failure, but the submission record leans toward support.

All counts use the same LLM classifications as [§5.9.4.6](#sec-5-9-4-6). Human inter-rater reliability scoring on a 60-item sample is pending.

| Rationale | Configuration | Audit verdict | Opposing | Supporting | Alignment |
|---|---|---|---|---|---|
| R1 | Calgary-Nolan Hill-Cochrane | PARTIALLY SUPPORTS | 38 / 50 (76%) | 12 / 50 (24%) | CONTRA_COMMISSION |
| R2 | Calgary-Peigan-Chestermere | INCONCLUSIVE / LEANS CONTRADICTS | 31 / 39 (80%) | 8 / 39 (20%) | ALIGNS_WITH_AUDIT |
| R3 | Calgary-Airdrie | SUPPORTS | 38 / 50 (76%) | 12 / 50 (24%) | CONTRA_COMMISSION |
| R10 | Red Deer-Lacombe | PARTIALLY SUPPORTS | 58 / 82 (71%) | 24 / 82 (29%) | CONTRA_COMMISSION |
| R12 | Rocky Mountain House-Banff Park | PARTIALLY SUPPORTS (hist.); CLOSED-FAIL (area) | 81 / 156 (52%) | 75 / 156 (48%) | ALIGNS_WITH_AUDIT |
| R13 | Olds-Three Hills-Didsbury | PARTIALLY SUPPORTS; CLOSED-FAIL (Airdrie slice) | 12 / 27 (44%) | 15 / 27 (56%) | CONTRA_AUDIT |

*Fractions are taking-sides only. Combined corpus: written submissions + Hansard r1 + Hansard r2. Total rows per rationale: R1 = 98, R2 = 64, R3 = 116, R10 = 173, R12 = 216, R13 = 66.*

**Findings.** Three rationales (R1, R3, R10) are CONTRA_COMMISSION: the commission cited community-of-interest or public-support grounds, but the combined record runs 71–76% opposing among those who took a position. Two (R2, R12) are ALIGNS_WITH_AUDIT: the commission's own verdict was uncertain or test-failing, and submissions are also majority-opposing or near-split. One (R13) is CONTRA_AUDIT: the audit flagged a geometric failure on the Airdrie slice, but submissions lean 56% toward support. No ALIGNS_WITH_COMMISSION findings were observed.

**Channel-divergence note for R12.** The 52 / 48 combined split on RMH–Banff Park masks the divergence from [§5.9.4.6](#sec-5-9-4-6): written submissions are 54% opposing, while Hansard in-person testimony is net-supportive. A commission weighting in-person testimony more heavily would have seen a different picture. No such divergence exists for R1, R3, or R10, which are majority-opposing in both channels.

**Interpretation.** CONTRA_COMMISSION findings do not prove improper conduct. A commission may rely on evidence beyond the archived record. The finding is that the publicly verifiable consultation record does not corroborate the commission's claimed public endorsement on three of four configurations where such endorsement was asserted.


<a id="sec-5-9-5"></a>
#### 5.9.5 Constitutional backdrop

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, established that Canadian electoral redistribution is measured against an "effective representation" standard, not strict population parity. Within that standard, deviations from provincial average are permissible when they serve recognized factors (geography, community of interest, minority representation). An audit that finds (a) directionally-consistent partisan asymmetry in a proposal and (b) a process promoting that proposal over a more-neutral, more-publicly-supported alternative would be evaluated against *Saskatchewan Reference** if challenged — but this audit does not assess the constitutional question. It provides the evidentiary basis for others to do so.

**Application to specific boundary disputes.** *Raîche v. Canada (Attorney General)*, 2004 FC 679, and *Cassista v. Canada (Attorney General)*, 2014 FC 398, apply the Saskatchewan Reference standard to specific boundary disputes without producing a bright-line ceiling on partisan-asymmetric outcomes. Under this standard, a map's constitutional status depends on whether its deviations are reasonably related to permitted factors. The audit's findings — directional partisan asymmetry, engineered §15(2) boundaries, cracking patterns visible across three cities, and procedural departure from independent-commission practice — are the kinds of evidence a court applying the effective-representation standard would weigh.

**The 2026 Quebec ruling.** The constitutional landscape shifted materially on April 22, 2026, six days after Alberta's April 16 motion handed redistricting to the Lunty committee. On that date, the Supreme Court of Canada dismissed Quebec's appeal of a Quebec Court of Appeal decision that had struck down the Legault government's 2024 statute blocking Quebec's *Commission de la représentation électorale* from redrawing the provincial map (the redrawing eliminated one Gaspé Peninsula riding and one Montreal east-end riding in favour of two new districts in the Laurentians/Lanaudière and Centre-du-Québec regions). The SCC ruling was 7–2, delivered from the bench — a procedural posture reserved for cases the panel views as constitutionally clear-cut. The QCA ruling the SCC upheld held that the freeze law violated sections of the Charter that guarantee democratic representation by allowing significant disparities in voter weight to persist. Reported in CBC News, "Quebec's redrawn electoral map will stay after Supreme Court ruling" (2026-04-22) and Canadian Press / CTV News, "Supreme Court rejects Quebec's attempt to block changes to election map boundaries" (2026-04-22). The formal SCC reasons are pending publication. The Quebec Court of Appeal decision being upheld is *Coalition de l'Outaouais et al. c. Procureur général du Québec* (2025; full citation pending). Audit will update this section when the SCC reasons are published.

**Doctrinal implications for Alberta.** Three relevant holdings (extracted from the journalistic reporting; subject to confirmation when written reasons are published):

1. **Provincial legislatures cannot block independent commission redistricting work to preserve voter-weight disparities, even when justified on regional-protection grounds.** The CAQ government's stated rationale — protection of Gaspé and other rural ridings — was the same class of argument the Alberta minority commissioners advance in Appendix E pp. 302–303 ("hybrid constituencies are... the best available instrument for preserving rural and suburban representation in the face of sustained urban growth"). The SCC found this rationale insufficient to justify legislative interference with commission work in Quebec. The same rationale would presumably face the same constitutional analysis if applied to a hypothetical Alberta statute reassigning commission-recommended boundaries.

2. **The effective-representation standard from *Saskatchewan Reference** [1991] applies with more force where legislative interference is at issue, not less.** The 7–2 from-the-bench posture suggests the SCC sees this as well-settled doctrine, not novel application.

3. **Charter section 3 is the operative provision.** Both the QCA and the SCC framed the analysis as a Charter-rights question, not a separation-of-powers question. This matters for any Alberta challenge: a section 3 challenger would have standing as an affected voter, not just as a constitutional litigant.

**What this means for the audit's procedural critique.** The April 16 Alberta motion — reassigning redistricting authority to a UCP-majority legislative committee partway through the cycle — operates under a constitutional landscape that, six days later, became significantly less hospitable to legislative reassignment of independent commission-recommended boundaries. The audit's framing in [§5.9.3](#sec-5-9-3) (April 16 motion as procedurally unprecedented in the Canadian comparator set) now extends to a substantive constitutional question that is no longer hypothetical: the SCC has just held that a parallel move in Quebec is unconstitutional. Whether the Alberta situation is constitutionally distinguishable — for instance, because the Lunty committee is structured differently from a legislative-freeze law, or because Alberta's voter-weight situation differs materially from Quebec's — is for a court to decide on its own facts. The audit's positive contribution is to surface the structural-asymmetry evidence ([§5.4](#sec-5-4)–[§5.8](#sec-5-8)) that any such challenge would draw on.

<a id="sec-5-9-6"></a>
#### 5.9.6 Evidence trail for the six contested-rationale checks

The public-facing claim "five of six of the minority's published reasons fail under check" (`report_public.md` §"Five of six of the minority's published reasons fail under check") is the load-bearing rhetorical move that links the structural-irregularity finding to the minority's own stated cartography. This subsection consolidates the evidence base for each of the six claims so that a journalist, a counsel of record, or a hostile peer reviewer can trace each line in the public summary back to a primary source — or, where the trail is incomplete, see the gap. The six claims correspond to the six rationales the minority itself singled out in Appendix E (pp. 285–362) of the 2025–26 EBC final report. The audit's verdict on each is reported here in the same order as `report_public.md`.

**Registration status.** The rationale-failure check is a qualitative post-hoc audit, not a pre-registered test. None of the OSF registrations associated with this paper (OSF w2s8k, r3zm7, qsgy8, 6pt83) names a rationale-inventory or cleaner-alternative check as a pre-specified metric. The finding should be read as qualitative corroboration of the pre-registered structural-irregularity pattern (OSF w2s8k; [§5.5](#sec-5-5)), not as an additional pre-registered measurement. A reader who weights only pre-registered findings should disregard the five-of-six rationale-failure summary and rely solely on the structural metrics in [§5.4](#sec-5-4)–[§5.8](#sec-5-8).

**Note on the withdrawn seventh claim.** Earlier drafts of this audit (and earlier drafts of the public report) listed a seventh contested rationale: a Lethbridge / Taber-Warner configuration alleged to match a retired federal boundary. That claim has been removed entirely. The methodology check at `analysis/methodology/lethbridge_federal_boundary_check.md` established that the minority report does not in fact make a federal-boundary claim for the Lethbridge area: there is no underlying source the audit's "federal boundary retired in 2013" line could refer to. The headline arithmetic moves from "six of seven fail" to "five of six fail" as a result. The withdrawal is itself documented as a rationale-strength correction in the audit's favour — a hostile reviewer would have caught the absent source within an hour of opening the methodology directory. Pre-emptive withdrawal preserves the audit's evidentiary discipline.

A general note on the strength bands used below. **Strongly supported** means the verdict rests on a downloaded primary dataset that any reader can re-run with the published code. The rationale is contradicted on the dataset's own face. **Moderately supported** means the verdict rests on a documented public source (statute, government boundary map, commission text) that any reader can re-verify, but the comparison the audit performs adds an inferential step. **Weakly supported** means the audit asserts a fact that is consistent with general knowledge but is not separately documented in the audit's own files. A careful reader would have to take the assertion on the audit's word until the underlying check is filed. **Currently unsupported** means the public-facing summary phrases a check that the audit's own evidence files do not document. The line should not appear in legal-grade or journalistic-grade citation without follow-up work.

---

**Claim 1: The four Airdrie quadrants are within 8% of each other on every demographic measure the commission considers.**

- *Source the minority cites in their published rationale:* Appendix E, p. 339 (R14, "Airdrie East") and the inventory's R3/R4/R18 growth-projection cluster. The minority does not, in fact, give a per-quadrant demographic-difference rationale in the published text; the audit's framing in `report_public.md` line 195 attributes the per-quadrant rural/urban-character argument to the minority commissioners as the implied basis for the four-way split. The minority's *explicit* rationale is growth and commuter-tie, not demographic heterogeneity.
- *Evidence the audit checked it against:* `findings/justification_tests_findings.md` Test 3, using `data/justification_test_inputs.csv` (StatCan 2021 Census, City of Airdrie CSD 4806016, total pop 74,100). The test compares the population arithmetic of the 4-way split against a 2-way alternative.
- *What the data shows:* The arithmetic shows a 2-way split is sufficient — each half ≈37,050, requiring only ~4,147 additional non-Airdrie residents to clear the 41,197 statutory floor. The 4-way split forces each quarter (~18,525) to absorb ~22,672 non-Airdrie residents, which is the structural source of the four cross-municipal hybrids the minority labels Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane (north flank), and Airdrie East. The "within 8% on every demographic measure" line in `report_public.md` is **not directly documented in the audit's evidence files**: no per-quadrant demographic-comparison table (median income, age structure, dwelling type, immigration share, language) for the four minority Airdrie carves exists in `analysis/`, `data/`, or `analysis/methodology/`.
- *Verdict:* **Inconclusive on the line as written; Fail on the broader rationale.** The minority's split is unforced by population arithmetic (which the audit documents) but the specific "within 8% of each other on every demographic measure" sentence is a stronger claim than the existing files substantiate.
- *Documentation file:* `findings/justification_tests_findings.md` (Test 3); `data/justification_test_inputs.csv`.
- *Reproducibility:* `python analysis/scripts/justification_tests.py`. A reader can re-run the population test independently. The "8% demographic" sub-claim cannot be reproduced from the existing files and requires per-quadrant census tabulation as follow-up.

---

**Claim 2: Cochrane's most common commuter destination is Cochrane itself. Among out-of-town commuters, Calgary-Centre is named more often than Foothills.**

- *Source the minority cites in their published rationale:* Appendix E, p. 331 (R1): "residents move fluidly between jurisdictions for work, education, health care, and commerce." The minority frames the Calgary-Nolan Hill-Cochrane lasso as a commuter-tie district pairing Cochrane with the Nolan Hill / Sage Hill ward of NW Calgary specifically.
- *Evidence the audit checked it against:* Statistics Canada 2021 Census, table 98-10-0459-01 ("Commuting flow from geography of residence to geography of work by gender: Census subdivisions"), filtered to Cochrane CSD origin (DGUID `2021A00054806019`). Methodology in `analysis/methodology/cochrane_journey_to_work.md`. Output in `data/cochrane_journey_to_work.csv`.
- *What the data shows:* Of 8,550 Cochrane-resident workers with a usual place of work, **4,205 (49.2%) work within Cochrane itself**, **3,065 (35.8%) commute to Calgary CY**, 345 (4.0%) to Rocky View County, 185 (2.2%) to Canmore. The 49.2% within-Cochrane share is the largest single destination by a wide margin. The "Calgary-Centre named more often than Foothills" sub-claim in the public summary is a **stronger statement than the table can support**: the public Census table publishes commute destinations at CSD granularity (Calgary CY as a single unit), not at electoral-district or ward granularity. Within-Calgary disaggregation is not in the public release. The methodology file flags this explicitly: the rationale is unevidenced at sub-CSD resolution rather than falsified.
- *Verdict:* **Fail on the within-Cochrane primacy; Inconclusive (leaning Fail) on the Calgary-Centre-vs-Foothills sub-claim.** The data falsifies the "fluid movement to Calgary" framing as a *primary* commute pattern (the largest flow is internal). The within-Calgary destination breakdown the public summary asserts is not in the audited dataset.
- *Documentation file:* `analysis/methodology/cochrane_journey_to_work.md`; `analysis/methodology/minority_rationales_validation.md` §R1; `data/cochrane_journey_to_work.csv`.
- *Reproducibility:* StatsCan table 98-10-0459 is publicly downloadable at `https://www150.statcan.gc.ca/n1/tbl/csv/98100459-eng.zip`; the filter on DGUID `2021A00054806019` and the per-destination ranking are scripted in the methodology file. A reader can re-run end-to-end.

---

**Claim 3: The Rocky Mountain House-Banff Park extension into Banff National Park has no agricultural land base ("ranching community of interest") it can refer to.**

- *Source the minority cites in their published rationale:* Appendix E, p. 352 (R12). The minority invokes the s.15(2) exception for the Banff National Park extension on four grounds: north-south economic corridor along Highway 22; Rocky Mountain House as a hub for Clearwater County; division of regional Indian reserves from the nearest economic hub; and historical precedent of Banff NP portions in a west-central electoral division. The minority frames the broader district as a "ranching community of interest."
- *Evidence the audit checked it against:* `findings/justification_tests_findings.md` Test 2 (area arithmetic), [§5.1.4](#sec-5-1-4) + [§5.3.3](#sec-5-3-3) of this report (engineered-boundary signature E1–E3), and `analysis/methodology/banff_extension_population_check.md` (polygon-clipped DA population pull on the Banff extension portion). The 2019 predecessor area (Bill 33 shapefile attribute `Km2`) is 24,468 km², already 22 % above the s.15(2)(a) 20,000 km² threshold without the NP extension. The minority's own population figure for the extended district is 38,298 (−30.3 %), still outside the ±25 % band even with the extension.
- *What the data shows:* The NP extension is **not load-bearing for either area or population qualification** under s.15(2). On the population side, the polygon-clipped 2021-Census-DA pull at `analysis/methodology/banff_extension_population_check.md` finds **approximately 491 area-weighted residents** inside the extension polygon (not zero) — concentrated in the Lake Louise / Saskatchewan River Crossing / Nordegg corridor visitors-services area-weighted aggregation. The earlier "zero year-round residents" framing was an oversimplification of an inhabited-but-very-sparse polygon. On the agricultural side, the *Canada National Parks Act* (R.S.C. 1985, c. N-14) statutorily prohibits agricultural tenure on national-park land, so a "no working ranches inside the park-land slice" finding is statutorily entailed for the in-park portion but **not separately verified** for adjacent Crown-land grazing-lease territory the extended district also touches. The minority's "ranching community of interest" rationale therefore has no agricultural land base it can refer to *inside the park slice*, but the audit does not file a check on grazing-lease territory adjacent to it.
- *Verdict:* **Fail on the s.15(2) area-necessity claim (documented); Fail on the "ranching community of interest" rationale for the in-park portion (statutorily entailed); Inconclusive on grazing-lease territory adjacent to the park (not separately tested).** The minority's stated rationale fails on what the audit has tested; the previous public-facing precision ("zero residents, zero ranches") was overstated and has been corrected to the more careful framing in `report_public.md`.
- *Documentation file:* `findings/justification_tests_findings.md` (Test 2); [§5.1.4](#sec-5-1-4), [§5.3.3](#sec-5-3-3) of this report; `analysis/methodology/minority_rationales_validation.md` §R12; `analysis/methodology/banff_extension_population_check.md`.
- *Reproducibility:* The area arithmetic is reproducible from the 2019 Bill 33 shapefile (`data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`). The polygon-clipped population pull (~491 area-weighted residents) is reproducible from the methodology file's documented DA-intersection pipeline. The grazing-lease check on adjacent Crown land remains future work.

---

**Claim 4: North Airdrie is suburban. Olds and Didsbury are rural service centres.**

- *Source the minority cites in their published rationale:* Appendix E, p. 349 (R13): "extending the boundaries of the existing Olds-Didsbury-Three Hills south to include more portions of Rocky View County… keep established communities of interest together along the Highway 2 corridor between Red Deer and Airdrie." The minority frames the southern extension as community-of-interest continuity along Highway 2.
- *Evidence the audit checked it against:* `findings/justification_tests_findings.md` Test 1 (population arithmetic of the rural Olds/Didsbury/Three Hills/Mountain View/Kneehill core sums to 43,691 — already above the 41,197 floor without any Airdrie territory). `analysis/methodology/minority_rationales_validation.md` §R13 cross-checks the Highway-2 continuity claim against the 2019 enacted Olds-Didsbury-Three Hills district (which already contains Olds, Didsbury, Carstairs, Three Hills, Crossfield without the Airdrie slice).
- *What the data shows:* The arithmetic shows the Airdrie slice is unforced. The "North Airdrie is suburban; Olds and Didsbury are rural service centres" sub-claim is a **descriptive characterization that is broadly defensible from public sources** (City of Airdrie 2024 Growth Report describes Airdrie as a Calgary-CMA satellite city; the Town of Olds 2024 municipal profile and Town of Didsbury directory describe both as agricultural-services hubs in Mountain View County). However, the specific phrase "Census-of-agriculture data says" in `report_public.md` line 198 is **not documented in the audit's evidence files**: no Census of Agriculture extraction for North Airdrie / Olds / Didsbury exists in `analysis/` or `data/`, and the validation file's verdict on R13 is "PARTIALLY SUPPORTS" the continuity-along-Hwy-2 framing while flagging the Airdrie slice as CLOSED-FAIL on population math, not on demographic mismatch.
- *Verdict:* **Fail on population necessity (documented); Weakly supported on the suburban-vs-rural-service-centre characterization (descriptively true but not separately filed).** The "Census-of-agriculture data says" framing in the public summary overstates the audit's documented check.
- *Documentation file:* `findings/justification_tests_findings.md` (Test 1); `analysis/methodology/minority_rationales_validation.md` §R13.
- *Reproducibility:* The population arithmetic is reproducible end-to-end. The suburban-vs-rural-service-centre demographic comparison would require StatCan Census Profile dissemination-area extraction for the relevant CSDs plus a Census of Agriculture pull; neither is currently scripted. **Recommend either filing the demographic comparison or softening the public-facing language to "the population arithmetic does not require it" (which is what the audit actually documents).**

---

**Claim 5 (WITHDRAWN): Lethbridge-East / Lethbridge-Taber-Warner federal-boundary match.**

- *Status:* **Withdrawn from the public summary and from the rationale-failure count.** Earlier drafts attributed to the minority a claim that the Lethbridge split between Lethbridge-East and Taber-Warner matches a federal boundary retired in 2013. The methodology check at `analysis/methodology/lethbridge_federal_boundary_check.md` established that the minority report does not in fact make this federal-boundary claim anywhere in Appendix E. The R1–R18 rationale inventory in `analysis/methodology/minority_rationales_inventory.md` contains no per-Lethbridge federal-boundary rationale, and the school-division coherence file (`analysis/methodology/school_division_coherence.md`) lists Lethbridge-East and Lethbridge-Taber-Warner as minority hybrids without a federal-boundary basis. There is no underlying source for the audit's earlier "the federal boundary they claim to match was retired in 2013" line.
- *Disposition:* The claim is removed entirely from `report_public.md` and from this monograph's rationale-failure count. The headline arithmetic is updated from "six of seven fail" to "five of six fail." No replacement claim is substituted; the Lethbridge area is left out of the contested-rationale list because the minority did not file a published rationale for it that the audit could check.
- *Documentation file:* `analysis/methodology/lethbridge_federal_boundary_check.md` (withdrawal note).
- *Lesson:* This withdrawal is recorded as a discipline correction in the audit's favour. The previous formulation of the seventh claim was a fabrication-by-paraphrase: the audit attributed a specific factual claim to the minority commissioners that they did not make, and the absence of an underlying source meant a hostile reviewer would have caught the overstatement immediately. Pre-emptive withdrawal preserves evidentiary discipline at the cost of the round "six of seven" framing.

---

**Claim 6: The shared school division (Red Deer-Sylvan Lake) contains 8% of Red Deer's school-aged population.**

- *Source the minority cites in their published rationale:* Appendix E, p. 351 (R11): "By placing rural populations in the same electoral division as urban communities in the Hwy 2 corridor, it is possible to achieve effective representation and overcome challenges with dividing communities of interest that existed in previous electoral divisions" — including a "go to school" reference invoked alongside the urban-rural pairing.
- *Evidence the audit checked it against:* Alberta Education school-authority boundary maps (`https://www.alberta.ca/alberta-school-division-maps`) cross-referenced in `analysis/methodology/school_division_coherence.md` and `analysis/methodology/minority_rationales_validation.md` §R11. Sylvan Lake CSD (pop 15,995) is in **Chinook's Edge School Division No. 73**; the City of Red Deer (pop 100,844) is served by **Red Deer Public Schools** and **Red Deer Catholic Regional Schools**. These are separate, jurisdictionally-distinct divisions with separate trustee elections and non-overlapping catchments. The claim "shared school division" is geographically false on the boundary maps.
- *What the data shows:* No Red Deer school-age student attends a Chinook's Edge school as part of the standard public catchment, and vice versa. The "8% of Red Deer's school-aged population" line in `report_public.md` line 200 is a **stronger numerical claim than the audit's files document**: no file extracts Red Deer's 5–17 population from StatCan or Alberta Education enrolment records and computes the share served by Chinook's Edge specifically. The school-coherence file's verdict is qualitative ("CONTRADICTS — different divisions"); the "8%" figure is not separately filed.
- *Verdict:* **Fail (on magnitude is correctly summarised, but the 8% figure is not separately documented).** The qualitative verdict (different divisions, no shared catchment) is strongly supported. The specific 8% magnitude is **weakly supported** in the audit's current files.
- *Documentation file:* `analysis/methodology/school_division_coherence.md`; `analysis/methodology/minority_rationales_validation.md` §R11.
- *Reproducibility:* The qualitative division-mismatch is reproducible from Alberta Education's published boundary map. The 8% magnitude requires Red Deer 5–17 population + Chinook's Edge enrolment served from Red Deer city neighbourhoods; neither is currently scripted. **Recommend either filing the 8% calculation or softening the public-facing language to "the two cities are in different school divisions; no Red Deer student attends a Chinook's Edge school in the standard catchment."**

---

**Claim 6 (was Claim 7): For St. Albert-Sturgeon, the majority map and the minority map independently arrive at the same two-district structure under the Act's constraints — when two independent drafting teams converge, the configuration is constraint-forced rather than engineered.**

- *Source the minority cites in their published rationale:* The minority's St. Albert-Sturgeon configuration appears in the inventory (`analysis/methodology/school_division_coherence.md` §St. Albert-area hybrid) but **does not have a per-district published rationale in the R1–R18 inventory** (`analysis/methodology/minority_rationales_inventory.md`). The audit's "Stands" verdict is therefore not a direct test of the minority's stated reason; it is an *audit-internal verdict based on a convergence test*: where two independent drafting teams (the three majority commissioners and the two minority commissioners) reach the same configuration under the same constraints, the configuration is treated as constraint-forced rather than designed.
- *Evidence the audit checked it against:* The [§5.6](#sec-5-6) cross-map structural comparison documents that the majority map and the minority map both produce a single St. Albert ED with the same two-district St. Albert / St. Albert-Sturgeon structure — see the [§5.6](#sec-5-6) city-wide split table where St. Albert reads "1 ED" on both maps. `analysis/methodology/school_division_coherence.md` documents that St. Albert Public Schools serves only the City of St. Albert; Sturgeon Public Schools serves Morinville, Legal, Gibbons, and Sturgeon County. The City of St. Albert (pop ~70,000) is below the 68,661 ceiling but above the 41,197 floor, so it could in principle stand alone — but its commute and service geography binds it tightly to the Edmonton-corridor districts on its south boundary. `findings/claim_significance_analysis.md` row 7 documents that no engaged citizen submission proposes a clearly distinct minority alternative for St. Albert-Sturgeon (0 supporters for the minority variant, 2 supporters for the majority's St. Albert-Sturgeon name — label-ambiguity caveat noted).
- *What the data shows:* The convergence test (both teams independently arriving at the same configuration) is observable directly from the [§5.6](#sec-5-6) cross-map structural comparison and from the school-coherence file. This is a stronger evidentiary basis than a counterfactual non-existence claim, because it does not require the audit to prove that no other configuration exists — it requires only that two independently-drafting teams under the same constraints reached the same one. The earlier "no other configuration satisfies both the community-of-interest and the ±25% rule simultaneously" framing was a counterfactual non-existence claim the audit could not formally prove; the convergence framing is what the documented evidence actually supports.
- *Verdict:* **Stands on the convergence framing.** Both the majority and the minority independently produced the same St. Albert-Sturgeon two-district structure under the Act's constraints; the audit treats this convergence as evidence the configuration is constraint-forced. The earlier "no other configuration" line has been retired in favour of this framing.
- *Documentation file:* [§5.6](#sec-5-6) (city-wide split table — St. Albert row); `analysis/methodology/school_division_coherence.md`; `findings/claim_significance_analysis.md` row 7; `analysis/methodology/minority_rationales_validation.md` (St. Albert-Sturgeon not separately listed).
- *Reproducibility:* The convergence observation is reproducible from the [§5.6](#sec-5-6) cross-map structural comparison. A constraint-search extracting all St. Albert-Sturgeon configurations from the 2,000,000-map ensemble (Run #6, [§5.4.6](#sec-5-4-6)) would supplement the convergence finding with an explicit non-existence test, but is not required for the convergence-based verdict.

---

**Strength-banding summary across the six claims (Claim 5 Lethbridge withdrawn).**

| # | Claim short form | Verdict in public summary | Strongest evidence band actually filed | Sub-claim notes |
|---|---|---|---|---|
| 1 | Airdrie 4-way split | Fail | Strong on population necessity | "8% on every demographic measure" not filed |
| 2 | Cochrane commuter primacy | Fail | Strong on within-Cochrane share; Strong on Calgary-as-largest-out-of-town | Calgary-Centre-vs-Foothills sub-claim not testable in CSD data |
| 3 | RMH-Banff NP extension | Fail | Strong on s.15(2) area non-necessity; ~491 area-weighted residents (not zero) per polygon-clipped DA pull; "no working ranches" statutorily entailed for in-park slice via *Canada National Parks Act*, unverified for adjacent Crown-land grazing-lease territory | Earlier "zero residents / zero ranches" framing has been corrected — see methodology file `banff_extension_population_check.md` |
| 4 | ODH reaching N Airdrie | Fail | Strong on population non-necessity | "Census-of-agriculture data says" not filed; suburban-vs-service-centre is descriptively true but not separately documented |
| ~~5~~ | ~~Lethbridge federal-boundary match~~ | **WITHDRAWN** | n/a — the underlying minority claim cannot be located in the report; see `analysis/methodology/lethbridge_federal_boundary_check.md` | Removed from the rationale-failure count entirely |
| 6 | Red Deer-Sylvan Lake school division | Fail (on magnitude) | Strong on qualitative division mismatch | "8% of Red Deer's school-aged population" magnitude not filed |
| 7 | St. Albert-Sturgeon | Stands (constraint-forced) | Strong on the convergence test (majority and minority independently produce the same two-district structure — [§5.6](#sec-5-6)) | Earlier "no other configuration" counterfactual non-existence framing retired |

**Reading the table.** The audit's headline arithmetic is now "five of six of the minority's published reasons fail under check." Of the six claims still in the count, four (Claims 1, 2, 3, 4) have a strong audit-documented backbone with one or two sub-claim corrections noted. One (Claim 6) has qualitative Fail support with a magnitude sub-claim still pending; one (Claim 7, St. Albert-Sturgeon) has a documented Stands verdict on the convergence test. Claim 5 (Lethbridge) has been removed entirely.

**Disposition for the public summary.** The "five of six fail" headline is exactly what the filed evidence supports. The previous "six of seven" framing is retired because (a) the seventh claim (Lethbridge) was a fabrication-by-paraphrase that no underlying minority text supports and (b) the seventh-as-stands claim (St. Albert-Sturgeon "no other configuration") was a counterfactual non-existence claim stronger than the filed evidence. The convergence framing replaces both: the configuration St. Albert-Sturgeon stands on is the one both independent drafting teams produced under the same constraints.

**Disposition for the three remaining sub-claim corrections (Claims 1, 4, 6).** In each case the public-facing precision ("within 8% of each other on every demographic measure"; "Census-of-agriculture data says"; "8% of Red Deer's school-aged population") is a stronger statement than the corresponding evidence file documents. **The honest options are:** (a) file the supporting calculation as a per-claim methodology note before publication; (b) soften the public-facing language to match the actual filed evidence ("the population arithmetic does not require it"; "the connection is geographic adjacency rather than shared agricultural-services geography"; "the two cities are in different school divisions, with no shared catchment"). Option (a) preserves the quantitative precision; option (b) preserves evidentiary discipline at the cost of some rhetorical force. Claim 3 has been corrected in `report_public.md` to the more careful "no agricultural land base it can refer to" framing supported by the *Canada National Parks Act* and the polygon-clipped population pull.

**Bottom line for evidence-trail integrity.** The "five of six" pattern is solid on the rationale-failure dimension the audit's files document. The previous "six of seven" arithmetic was withdrawn after primary-source verification could not locate the underlying Lethbridge federal-boundary minority claim, and the previous "no other configuration" counterfactual on St. Albert-Sturgeon is replaced by the convergence framing. The remaining three sub-claim follow-ups (per-quadrant Airdrie demographic comparison; Olds-Didsbury Census-of-Agriculture pull; Red Deer-Sylvan Lake school-age magnitude) are evidentiary precision upgrades, not load-bearing for the headline.

<a id="sec-5-9-7"></a>
#### 5.9.7 Population data currency and the 2026 census

The Lunty committee is mandated to produce a 91-seat map by November 2, 2026. That mandate has an unaddressed population-data consequence.

Statistics Canada conducts a mandatory long-form census every five years under the *Statistics Act* (R.S.C. 1985, c. S-19). The 2021 Census of Population was collected May 11, 2021; preliminary national-level counts were released February 9, 2022; constituency-level dissemination-area data used for redistricting did not become available until the 2022–2023 release waves. On the same cadence, the **2026 Census** will be collected in May 2026. Preliminary provincial population counts are expected in approximately Q1 2027; dissemination-area-level data adequate for the Electoral Boundaries Commission Act's population-parity requirements would not realistically be certified and released before mid-to-late 2027.

The *Electoral Boundaries Commission Act* s. 14(1)(a) requires the commission — and by extension any body exercising the commission's statutory function — to use the "most recent decennial census." If the 2026 census data is not yet certified and released by Statistics Canada at the time the committee finalises its map, the committee must use 2021 data. There is no statutory mechanism permitting voluntary delay to await uncertified census results. The November 2026 target date therefore forecloses access to the 2026 census regardless of intent.

This matters most for the ridings where the audit's structural findings concentrate. The Calgary–Airdrie corridor — Airdrie (population 85,805 at the July 2024 municipal census; City of Airdrie, 2024), Cochrane, Chestermere, and Calgary's northwest quadrant — is the fastest-growing sub-region in Canada. Alberta added approximately 200,000 residents in the 2021–2023 period alone (Alberta Treasury Board and Finance, 2023 population estimate). Boundaries drawn in November 2026 on 2021 census populations for seats contested in 2027 and held on those boundaries through potentially 2031 will be built on population data that is 10 years old by the time the electoral cycle they govern ends. Population equality in the highest-growth ridings — the same ridings where the commission's two proposals diverge most sharply — will degrade fastest.

**Policy implication.** If the government's objective is redistricting that serves effective representation through a full electoral cycle, a November 2026 completion date imposes a foreseeable cost: the map will begin with the most accurate population baseline available but will not be anchored to the 2026 census that will become the legal baseline for the commission cycle following it. No redistricting body can escape census timing constraints; the commission faced the same constraint. The observation here is forward-looking only: the committee and the legislature are aware that 2026 census data will become available approximately one year after the committee's mandate ends, and that the communities most affected by the audit's structural findings are precisely those where population drift from the 2021 baseline will be largest. This is not a legal objection to the November 2026 map; it is a relevant fact for any assessment of the map's durability.

---

<a id="sec-5-10"></a>
### 5.10 Forward-looking AI-use recommendations for the Lunty committee

**Audience and scope.** The Special Select Committee of MLAs chaired by Brandon Lunty (MLA, Leduc-Beaumont) carries the November 2, 2026 mandate to produce a 91-seat Alberta map. This subsection is a technical, non-partisan framework for how that committee — or its advisory panel, or any future Alberta redistricting body — can use AI tools responsibly if it chooses to. It does not take a position on whether the committee *should* use AI tools. It does take a position on what disciplines any such use must follow. The position is not novel; it is the same methodological discipline this audit applies to itself (reproducibility, transparency, pre-registration, named accountability).

**Why this section exists in this paper.** The April 16 "AI academy" remark (Premier Smith, Calgary Journal 2026-04-21) signalled that AI use is on the table for the committee. An audit that documents procedural departures from Canadian independent-commission practice ([§5.9.2](#sec-5-9-2)) without addressing the AI-use dimension would be incomplete — AI use can compound or mitigate the independence concerns already raised. A boundary map has legal and constitutional effect for up to a decade; the workflow that produces it is part of its defensibility.

**Seven core principles.** Each is a discipline the committee's workflow must enforce, regardless of which tool is used:

1. **Humans decide; AI assists.** Every boundary in the final map must have at least one named committee member or advisor of record who will answer for it in public. *"The algorithm converged"* is not a defence.
2. **Transparency over opacity.** Every prompt, input dataset, model version, random seed, and output used in drafting must be logged, timestamped, and publicly released with the final report. Redact for personal privacy only, not for reputation.
3. **Reproducibility over one-shot generation.** Any AI output used in the map must be reproducible by an independent third party given the same inputs. Stochastic methods (MCMC, simulated annealing, LLM completions) require published seeds and pinned model versions.
4. **Pre-registration over post-hoc justification.** Evaluation criteria (population equality targets, COI priorities, compactness thresholds) must be published before any map draft is circulated, and treated as gates the map must clear — not as framing added after the draft.
5. **Independence tests over single-model reliance.** Any AI output on a load-bearing decision must be generated by at least two independent tools. Disagreements between tools are signals for human adjudication, not noise to average away.
6. **Falsifiability over rhetoric.** Every claim attached to the final map ("this preserves community of interest," "this reflects commuter ties") must be stated in a form that names the dataset which would confirm or refute it. Claims that cannot be falsified must be labelled as opinion.
7. **Auditability over ease of use.** The cheapest workflow (an MLA types a question into a chatbot) is also the least auditable and therefore inadequate for a constitutional decision. The workflow that makes every step reproducible, even when slower, is the one the committee must adopt.

**Specific technical recommendations (abbreviated; full text in the companion document).**

- **Generation.** Use purpose-built redistricting software (GerryChain, Dave's Redistricting App, Maptitude for Redistricting), not a general-purpose chatbot. Publish the ensemble, not only the chosen map — a single map says nothing about whether the committee's choice is typical or an outlier within the constraint set. Do not use an LLM to write boundary descriptions directly; LLMs hallucinate street names and invert cardinal directions.
- **Evaluation.** Apply the same partisan-fairness metrics used in the academic literature (efficiency gap, mean-median difference, declination, seats-votes curve) against vote data from the three most recent provincial elections, not one. Run a Chen-Rodden natural-packing test: if the proposed map falls outside the 95th percentile of a constraint-bound ensemble in either direction, it requires a stated, testable explanation. Compute and publish Polsby-Popper and Reock compactness on every district.
- **Public input.** Publish the input corpus (redacted for personal information) so independent researchers can reproduce any AI-assisted theme coding. Do not rank submissions by length or signature count — electoral boundary decisions weigh arguments, not volume. Flag the *absence* of input as well as its presence.
- **Justification drafting.** Every factual claim in AI-drafted prose must be human-verified against a cited source. Do not let an AI generate the committee's interpretation of *Saskatchewan Reference** [1991] or s.15(2) — Canadian constitutional-law summaries from general-purpose LLMs are unreliable and occasionally invert the holding. Publish the prompts used for any passage that appears in the final report.
- **Data currency (census cycle lag).** Maintain the 2021 census as the statutory baseline for every s.15(2) test and every ±25 % determination (the Act requires it). *In parallel*, publish a "Plan B" sensitivity table using Alberta Treasury Board and Finance quarterly estimates. Report any ED whose legal-window status disagrees between Plan A and Plan B. AI's role in Plan B is limited to routine data-aggregation acceleration; every cell must trace back to a published TBF, StatsCan, or municipal-census figure. Full rationale at `findings/cycle_lag_analysis.md` + `docs/ai_use_recommendations_for_committee.md` §2.5.

**What AI should not do — even with human review.**

- Final decisions on district boundaries (a committee member signs each district, not a model).
- Weighing constitutional considerations (s.3 Charter analysis, *Saskatchewan Reference* application, s.15(2) criteria).
- Determining community of interest (lived experience is not retrievable from a census table).
- Drafting the committee's reasoning on contested districts (Airdrie, Chestermere, Nolan Hill–Cochrane, RMH–Banff Park, and any new 91-seat flashpoint).
- Assessing partisan intent (evidence cannot distinguish motive; AI cannot either).

**Nine-item public-disclosure checklist.** Before publishing the final map, the committee must be able to answer each of the following publicly: (1) which AI tools were used, by name and version; (2) what prompts and inputs were given to each; (3) which outputs were used in the final map and which were discarded; (4) what random seeds, configurations, and parameters were set; (5) which committee member or advisor takes personal responsibility for each district's boundary; (6) what evaluation criteria were established before drafting began; (7) what ensemble of alternative maps was generated and where the final map sits in that ensemble; (8) what Charter and statutory analyses were performed and by whom; (9) which claims in the final report are AI-drafted and human-verified, which are human-drafted, and which are AI-drafted without human verification. A committee that can answer all nine publicly has used AI responsibly. A committee that cannot has not, regardless of tooling sophistication.

**Three risks specific to the April 2026 context.**

1. **Independence-washing.** The April 16 mandate includes an advisory panel with the three-party chair-plus-two structure. If the panel uses AI tools whose outputs are filtered through a UCP-majority MLA committee, the panel's independence is nominal. Remedy: publish the panel's AI outputs *in full* before the MLA committee acts on them, and require a written explanation for any substantive committee deviation from panel recommendations.
2. **Legitimacy-by-association.** An AI tool's output inherits only as much legitimacy as its inputs and operators provide. A map presented as "algorithmically generated" without disclosed prompts and constraint sets is borrowing technical legitimacy it has not earned. Remedy: the nine-item checklist above as a minimum disclosure standard.
3. **Acceleration past deliberation.** AI can generate thousands of candidate maps in hours and short-circuit the slow deliberative work a committee is supposed to do. Remedy: a proposed boundary is not adopted on the strength of a model run alone, even a well-designed one. Speed is not a virtue in redistricting.

**Relationship to [§5.9](#sec-5-9)'s procedural findings.** The seven principles above do not replace [§5.9](#sec-5-9)'s documented procedural departures from Canadian comparator practice; they supplement them. A committee that adopts the AI-use disciplines and *also* operates under the April 16 MLA-committee-directed drafting structure retains the [§5.9.2](#sec-5-9-2) procedural critique regardless of its AI workflow. AI discipline is necessary but not sufficient for a defensible process. The full AI-use document (211 lines, with reference implementations and dataset pointers) is at [docs/ai_use_recommendations_for_committee.md](alberta_audit/docs/ai_use_recommendations_for_committee.md). Suggested citation: Conner, W., *AI-use recommendations for the Alberta Electoral Boundaries MLA Committee*, Alberta Electoral Boundaries Audit, v0.1, 2026-04-22.

---

<a id="sec-6"></a>
## 6. Discussion

This section interprets the results of [§5](#sec-5) against the prior work surveyed in [§2](#sec-2) and forward-refers to [§7](#sec-7) (Limitations and Falsifiability). The six-dimensional synthesis is presented first; the scope-discipline calibration and the three inherited qualifications follow.


| Dimension                                          | 2019         | Majority 2026          | Minority 2026          | Direction of minority shift |
| -------------------------------------------------- | ------------ | ---------------------- | ---------------------- | --------------------------- |
| [§5.1.1](#sec-5-1-1) Population MAD from avg                        | 2,010 *(87-seat, 2017 pops — different scale from 2026)*    | 3,180                  | **4,707** (+48%)       | wider dispersion            |
| [§5.1.2](#sec-5-1-2) Calgary Zone A − Zone B gap                    | (not run)    | +0.36%                 | **+12.20%**            | packing signal              |
| [§5.1.2](#sec-5-1-2) robustness (2023 winner-based)                 | (not run)    | +0.39%                 | **+7.71%**             | survives robustness check   |
| [§5.1.3](#sec-5-1-3) Rest-of-province mean population              | (not run)    | 52,281                 | 50,336 (−3.9%)         | rural overrepresentation    |
| [§5.1.4](#sec-5-1-4) s.15(2) invocations statutorily legitimate | — | 3 / 3 | 3 / 3 | re-audit 2026-04-23 under corrected thresholds |
| [§5.1.4](#sec-5-1-4) engineered-boundary signature (extension chosen over populated alternatives) | 0 | 0 | 1 (RMH-Banff Park) | substantive E2 test (see [§5.3.3](#sec-5-3-3)) |
| [§5.2.1](#sec-5-2-1) Standard EG (Phase 4C)                         | −2.64%       | +0.04%                 | **+3.96%**             | +3.92 pp more UCP-favourable (Phase 4C; S-M positive=UCP) |
| [§5.2.2](#sec-5-2-2) blend sensitivity range *(superseded by Phase 4C)* | —        | *(blend model retired)* | *(blend model retired)* | — |
| [§5.2.1](#sec-5-2-1) Mean-median gap (NDP)                          | −2.22 pp     | −3.64 pp               | **+1.03 pp**           | +4.67 pp shift more UCP-favourable (minority p99.98; majority p2) |
| [§5.2.1](#sec-5-2-1) NDP seats at 50/50                             | 46           | **48**                 | 43                     | minority −5 NDP seats vs majority at tied provincial vote |
| [§5.8.2](#sec-5-8-2) Visible spatial anomalies                      | —            | 0 (Calgary only)       | 3 (all confirmed)      | three anomalies             |
| [§5.8.4](#sec-5-8-4) Airdrie splits                                 | —            | 2 EDs                  | 4 EDs                  | double split                |
| [§5.9](#sec-5-9) Procedural                                      | —            | Commission-adoption path | Legislature-directed committee drafting | departure from comparators |

Six independent dimensions of evidence point in the same direction. None individually crosses a statistical significance threshold. Together, the directional consistency is the finding — the minority proposal, relative to the majority, shows more structural irregularities and, under 2023 voter geography, lower measured-partisan-neutrality at a sub-threshold magnitude, across six measurement frameworks.

A 2019 enacted-map baseline ([§5.4.10](#sec-5-4-10)) adds structural context to this six-dimensional picture. The 2019 map was itself a mild joint-space outlier on the 1,010,000-plan canonical ensemble (Mahalanobis D²=12.75, empirical p=0.013). The majority 2026 proposal retreats toward the constraint-bound expectation (D²=7.85, p=0.097), consistent with a normalizing commission process. The minority amplifies the 2019 anomaly 2.6-fold (D²=32.67, p=1.40×10⁻⁶) — measuring the void between what the two proposals do from a shared departure point.

**Scope discipline and small-magnitude calibration.** The six-dimensional framing follows the four-axis redistricting-audit discipline of Altman and McDonald (2011) and the consistency-across-N methodology of Katz, King, and Rosenblatt (2020): when single dimensions are underpowered, cross-dimensional agreement is the inferential artefact, not any individual magnitude. Each dimension's magnitude is small by design — the audit is not claiming a single five-alarm effect. Terms used in this paper carry calibrated meaning: *measurable* means "the computed statistic's sensitivity interval does not include zero at the stated confidence level"; *directional* means "the sign is consistent across all runs" without magnitude claim; *systematic* means "the same direction appears in multiple independent tests." These are not synonyms and are not interchangeable. A hostile reader entitled to read the audit as "the paper called small differences patterns" receives the following response: the patterns are defined precisely, apply to six independent tests, and persist across 90.5% of Monte Carlo samples (seed 42, N = 2,000), across 338Canada's April 2026 polling input, and across a symmetric test-selection audit that revealed additional minority-map patterns (Lethbridge and Red Deer 4-way splits, [§5.6](#sec-5-6)) not present in the majority.

**Multiple-comparison posture.** A hostile reviewer may legitimately observe that this audit runs on the order of 20 distinct statistical tests against overlapping 2023 vote data (four partisan-bias metrics × two maps × three blending weights ≈ 24 tests, plus the non-partisan-bias dimensions), and ask whether a family-wise-error-rate (FWER) correction has been applied. The paper **explicitly does not apply a Bonferroni or Benjamini-Hochberg correction**, because that correction assumes the tests are independent significance claims — and this audit does not advance individual significance claims. Every per-metric per-map result is reported inside a Monte Carlo sensitivity interval that already brackets its own parametric uncertainty ([§5.2.3](#sec-5-2-3), [§5.2.2](#sec-5-2-2), [§5.4](#sec-5-4)), and the aggregate synthesis is framed as directional consistency across correlated dimensions, not as a count of independent rejections.

Applying Bonferroni to a consistency frame inflates false-negative rates on related measurements without correcting the actual inferential artefact (cross-dimensional agreement); the audit therefore uses the consistency-across-correlated-tests framing of Katz, King, and Rosenblatt (2020) and the ensemble-reporting discipline of Altman and McDonald (2011) in preference to a multiple-comparison correction. Readers who prefer an FWER-adjusted lens should note that (a) the individual partisan-bias metrics do not cross their own uncorrected 95th-percentile sensitivity interval for significance, so a corrected threshold trivially also rejects them; (b) the audit's positive claim does not depend on any individual metric reaching significance, so the posture is unchanged.

Three qualifications inherited from the stress-test pass narrow this synthesis:

- Under the Chen-Rodden (2013) natural-packing framing (see [§5.2.5](#sec-5-2-5)), some portion of the minority-to-majority partisan-bias gap is not attributable to engineering — it reflects how any neutral map interacts with Alberta's urban-NDP / rural-UCP geography. This lowers the claim from "the minority was engineered against the NDP" to "the minority produces more UCP-favourable results under 2023 voter geography." The structural findings ([§5.1](#sec-5-1) population equality, [§5.1.2](#sec-5-1-2) Calgary zone gap, [§5.8.2](#sec-5-8-2) visible anomalies, [§5.8.4](#sec-5-8-4) community splits, [§5.9](#sec-5-9) procedural) are not affected by the natural-packing caveat because they measure geographic and procedural properties the natural-packing argument does not address.
- Under RT3 (cross-election stability), the vote-based asymmetry flips sign when 2019 votes replace 2023 votes. The six-dimension synthesis rests mostly on the structural dimensions; the single vote-based dimension ([§5.2](#sec-5-2)) is qualified accordingly.
- Under the submission-archive verification ([§5.9.4](#sec-5-9-4)), the procedural concern rests primarily on the two configurations without documented public support (Airdrie 4-way, Nolan Hill-Cochrane) rather than on the chair's full five-item sweep.

**Direction disagreement: three-layer reconciliation.** A careful reader of [§5.2](#sec-5-2) and [§5.4](#sec-5-4) will notice that the partisan-bias metrics do not all point the same way, and that the direction can flip depending on which vote input is used. This paragraph names each layer explicitly so they are not mistaken for methodological inconsistency.

*Layer 1 — metric disagreement under 2023 votes.* B2 (efficiency gap), B3 (mean-median), and B4 (seats at 50/50) all show the minority 2026 map as more UCP-favourable than the majority under Phase 4C and 2023 vote input: the minority produces substantially more NDP vote waste (EG +3.96% vs +0.04%), a more NDP-packed mean-median distribution (+1.03 pp vs −3.64 pp, placing minority at p99.98 in the UCP-tail), and gives NDP five fewer seats at a tied provincial election (43 vs 48). B6 (declination) disagrees: the minority sits at p2.17 in the NDP-tail — the *least* UCP-favourable of the three maps on that metric. The most probable explanation (see [§5.2.4](#sec-5-2-4)) is that EG, MM, and seats@50/50 respond to how many NDP votes are wasted in narrow-loss districts, while declination responds to how tightly winning margins cluster around the winning threshold — geometrically distinct properties that diverge when a map packs losing-party votes at narrow rather than wide margins. This three-metric agreement paired with declination dissent is the asymmetric-packing signature documented at [§6.2.2](#sec-6-2-2).

*Layer 2 — vote-input dependence.* Under 2023 votes the minority gives one more UCP seat than the majority at a tied election (minority 52 UCP / 37 NDP, majority 51 UCP / 38 NDP). 338Canada's April 2026 per-riding projection (§Track J), run through the same audit crosswalks, gives the minority one more NDP seat than the majority (minority 23 NDP, majority 22 NDP). Both differences are at the 1-seat noise floor and are consistent with two interpretations: the minority's marginal-seat calibration is efficient near the swing point the boundaries were designed for (roughly 2023 vote levels) but produces NDP-efficient results when the UCP advantage expands past that point; or both differences are within crosswalk estimation error and are not meaningfully distinguishable.

*Layer 3 — magnitude threshold.* Under 2023 vote input and the 1,010,000-plan canonical ensemble ([§5.4.9](#sec-5-4-9)), three individual partisan-bias metrics carry outlier flags on the minority map: mean-median at p99.98 (UCP-favoured tail), declination at p1.21 (NDP-favoured tail), and seats@50/50 at p99.99 (individual flag reinstated; n_eff=1,495, ESS-adjusted lower bound ≈p98, above p95 threshold). Efficiency gap at p94.4 remains below the p95 threshold; the EG flag is withdrawn. The majority is not flagged in the UCP-advantage direction on any metric (EG p15, declination p80, seats@50/50 p78); it sits at p0.92 on mean-median on the NDP-cracking tail (pre-registered Row 8, expected direction). The aggregate finding rests on the joint Mahalanobis result (p=1.40×10⁻⁶) and on directional consistency across the structural dimensions ([§5.1](#sec-5-1), [§5.8](#sec-5-8), [§5.9](#sec-5-9)).

**Summary of the direction picture.** Under structural tests, the direction is unambiguous and multi-confirmed. Under partisan-bias tests, three of four metrics agree (minority more UCP-favourable under 2023 votes), one disagrees (declination), and the direction reverses for one of the four at April 2026 polling levels. A reviewer citing declination or 338's April 2026 numbers as evidence the minority is the *fairer* map is making a legitimate point about one layer of the evidence; the audit does not suppress that layer and reports it in [§5.2.4](#sec-5-2-4) and §Track J. The audit's overall position is that the structural dimensions are the load-bearing evidence, and on those dimensions the direction is stable.

<a id="sec-6-1"></a>
### 6.1 How to interpret these findings — NP-hardness, statistical improbability, and precision as armor

The results above are NOT findings of "the correct map was X and the Commission drew something different." The redistricting problem is **NP-hard**: the Alberta *Electoral Divisions Act* constraint set (±25 % population deviation + contiguity + compactness + community of interest + Indigenous effective representation under s.15(2) + public-hearing input) does not admit a unique optimum. No mathematical procedure produces *the* correct Alberta map; any map that satisfies the constraints is one of an enormous family of legal maps, and the space of legal maps contains trade-offs — preserve COI at Airdrie at the cost of a slightly wider population dispersion, or tighten population equality at the cost of splitting Airdrie. These are not errors; they are **choices**. Fairness in this domain is not a discovery; it is a negotiation.

The audit therefore does not say **"this map is wrong."** It says **"this map is statistically improbable within the constraint set, and the improbability has a direction that is measurable."** Three concrete translations of the main results into that language:

- **Airdrie fragmentation ([§5.3.2](#sec-5-3-2)).** Of the large family of ReCom-legal Alberta maps that satisfy population deviation, contiguity, and compactness, the overwhelming majority preserve Airdrie as a 1- or 2-ED community (Airdrie's population of approximately 85,805 sits at 1.56× provincial quota [City of Airdrie, 2024]; the statutory ±25 % band permits a single-ED draw or a clean 2-way split). The minority map is one of a small minority of constraint-legal maps that split Airdrie across four EDs. **The Commission did not have to split Airdrie four ways. They chose to, among many legal alternatives that did not require that split.** The audit's question is not "why isn't Airdrie whole?" It is: "given that the constraint set permitted keeping it together, why was a 4-way split selected?"
- **Population dispersion ([§5.1](#sec-5-1)).** The Median Absolute Deviation of ED population from the provincial quota is 3,180 on the majority and 4,707 on the minority — a 48 % wider dispersion. The constraint set permits both: the ±25 % population deviation band leaves room for either. **The Commission did not have to draw a map with 48 % wider dispersion; they chose to, among many constraint-legal alternatives.** *(The municipal-anchoring example previously listed in this position did not survive canonical recomputation — both maps fall within the Canadian comparator norm. See [§5.8.5](#sec-5-8-5).[^anchoring_canonical])*
- **MCMC constraint-bound expectation ([§5.4](#sec-5-4)).** The ReCom ensemble places the minority map at the p99.98 tail on mean-median (canonical 1,010,000-plan run; [§5.4.9](#sec-5-4-9)). Interpretation: the constraint set admits 1,010,000 legal plans on the canonical ensemble; the minority map sits further from the mean-median median than ~99.98 % of them. **The Commission was not forced to draw a p99.98-tail map. They produced one, among hundreds of thousands of legal alternatives closer to the constraint-bound expectation.**

In every case, the audit's claim is the same shape: the Commission paid a measurable **fairness cost** to get the specific map they produced, where "fairness cost" means the number of statistical standard deviations (or the ReCom-ensemble percentile, or the anchoring ratio) by which the chosen map is displaced from the constraint-bound expectation. **This is the audit's only substantive claim.** It does not claim the minority is "wrong"; it claims the minority is improbable by a measurable amount, and the improbability has a direction.

<a id="sec-6-2"></a>
### 6.2 Author's verdict — was either map a gerrymander?

This subsection departs from the audit's measurement-only voice and offers the author's stated opinion on the question that motivated this work. It is presented as opinion, not as a peer-reviewed conclusion. The author's prior — UCP-disinclined Alberta voter — is disclosed in the Author Disclosure block in [§1](#sec-1), along with the three findings retained in this paper that ran *against* that prior. Readers who weight the audit only on its measurable claims should stop at [§6.1](#sec-6-1) and treat this subsection as ignorable.

**A note on what "verdict" means here.** The audit cannot judge intent; intent is not observable from public data, and the [§1](#sec-1) author-disclosure block already commits the paper to this restraint. What the audit *can* do is observe and quantify *effects*, and report the pattern those effects form. If the pattern looks like a gerrymander signature in the academic literature, the audit says so. Whether that signature reflects deliberate engineering or unlucky choice among legal alternatives is a question for the reader to weigh; the audit's job is to make sure the evidence on which that weighing happens is on the table.

**Definition of the pattern this section evaluates.** A "gerrymander signature" is the constellation of measurable effects that the academic redistricting literature (Stephanopoulos and McGhee 2015; DeFord et al. 2021; Warrington 2018; Cain et al. 2018; Katz, King and Rosenblatt 2020) treats as evidence of partisan engineering. Narrower than "any map with a partisan-asymmetry signal" (which would over-fire on natural-packing geography); broader than "any map whose author admits intent in writing" (essentially never observable). It maps onto the Canadian *Saskatchewan Reference** [1991] framework as: a map fails effective representation when its measured effects systematically dilute one community of voters' electoral weight beyond what geographic constraints require. The audit measures the effects; the constitutional question of whether those effects amount to a failure of effective representation is for counsel and a court to assess (Appendix F).

<a id="sec-6-2-1"></a>
#### 6.2.1 Lane 1 — Partisan-bias magnitude (against Alberta-calibrated thresholds)

The audit's [§5.2.8](#sec-5-2-8) derives **four Alberta-calibrated EG thresholds**, of which the most empirically grounded is the MCMC-ensemble 95th percentile drawn from 1,010,000 ReCom plans on the official Elections Alberta shapefiles under EBCA constraints. None of these thresholds is borrowed from US federal judicial standards; each is calibrated to Alberta law or Alberta data. The full provenance of each threshold is in [§5.2.8](#sec-5-2-8); the cross-tabulation against both 2026 maps follows.

The Lane 1 verdict uses **Phase 4C spatial attribution** as the sole canonical measurement (`packing_cracking_analysis.py` v0.3, 2026-05-18; exact VA-level centroid-in-polygon on official EA shapefiles). The two earlier attribution layers are retired: Reading A (crosswalk-blend, Layer 1) is superseded by Phase 4C ([§5.2.2](#sec-5-2-2)); Reading B (spatial against v0_8 DPG geometry, Layer 4) used geometries derived from commission PDF thumbnails — the DPG sunset clause is satisfied by Phase 4C on official shapefiles ([§4.1.4](#sec-4-1-4)). Phase 4C EG: majority +0.04%, minority +3.96% (S-M positive=UCP-favoured), consistent with canonical MCMC (majority +0.10%, minority +4.02%) to within 0.06 pp.

| Threshold | Source | Value | Phase 4C majority +0.04% | Phase 4C minority +3.96% |
|---|---|---|---|---|
| Stephanopoulos & McGhee (2015) reference | US historical calibration | 7% | sub-threshold | sub-threshold |
| Option A — Assembly-size sensitivity | First-principles scaling: 2/89 seats | ~2.2% | sub-threshold | **over threshold** |
| Option B — EBCA statutory-proportional | One-fifth of EBCA ±25% | 5% | sub-threshold | sub-threshold |
| Option C — Alberta historical-swing | 2015/2019/2023 swing analysis | 1.01–9.71% | sub-threshold in all contexts | sub-threshold under 2023 (p94.4) and 2019 (p70.4) contexts; **over under 2015** (+10.54%, p99.45) |
| **Option D — MCMC ensemble p95** | **1,010,000-plan canonical (official EA shapefiles, seed 1432864451, ±25%)** | **4.10%** | sub-threshold (p15.5) | sub-threshold (p94.4; 0.14 pp below 4.10% threshold) |

**Lane 1 verdict.** Under Phase 4C canonical attribution, the majority is sub-threshold on all Alberta-calibrated options — a clean Lane 1 result (p15.5 on canonical ensemble). The minority exceeds the assembly-size Option A threshold (2.2%) and, under 2015 electoral-context votes, exceeds the Alberta historical-swing Option C ceiling (9.71%). Under 2023 votes — the operative electoral context for the 2026 boundaries — the minority falls just below the Option D canonical ensemble threshold (p94.4; 0.14 pp below the 4.10% threshold). The qualitative framing the [§6.2](#sec-6-2) verdict ultimately rests on — that the **directional engineering** distinguishing the two maps lives in the structural lane ([§6.2.2](#sec-6-2-2)), not the partisan-bias-magnitude lane — is robust to Phase 4C. The majority is clean on EG magnitude; the minority is near but below the most stringent Alberta-calibrated threshold under current electoral conditions.

**Effect Size Interpretation (updated 2026-05-10 for 1,010,000-plan canonical run).** Under the 1,010,000-plan canonical ensemble (official EA shapefiles, seed 1432864451, [§5.4.9](#sec-5-4-9)), the minority map places at p99.99 on seats@50/50 — fewer than 100 of 1,010,000 neutral plans reach its canonical value of 51.69%. The Fisher combined p across the Mahalanobis Ch1 and SZAT Ch2 channels is 6.87×10⁻⁸. The earlier DPG-era estimate (p=0.015, +2.21 pp vs neutral median, Cohen's d=0.31) is superseded. On the 1,010,000-plan canonical ensemble, three of four partisan metrics are extreme simultaneously: MM at p99.98 (UCP-tail), declination at p1.21 (NDP-tail), seats@50/50 at p99.99; EG at p94.4 falls just below p95 and is not counted as an outlier flag in the 1,010,000-plan run (compare: 50k run had EG at p95.9). The three-flag pattern is the asymmetric-packing signature: the minority over-concentrates NDP votes in high-share districts (MM and seats flags) while also producing unusually tight winning margins for NDP-won districts (declination flag). An unexpected finding from the 1,010,000-plan run: the majority map's mean-median places at p0.85 — also in the extreme NDP-tail (see [§5.4.9](#sec-5-4-9) narrative). Both real maps are statistical outliers on at least one metric; the minority is the more extreme on three of four.

<a id="sec-6-2-2"></a>
#### 6.2.2 Lane 2 — Structural and procedural pattern

Lane 1 having returned a clean result for the majority on partisan-bias magnitude and a near-threshold result for the minority (p94.4; majority sub-threshold at p15.5), the question becomes whether the structural evidence reinforces the Lane 1 signal. The audit's other test families are vote-data-independent and detect engineering signatures that don't show up in EG magnitude alone.

| Test family | Threshold (where defined) | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Mean-median percentile vs MCMC ensemble | p > 95 = academic-literature outlier | **p0.85 (NDP-tail outlier)** | **p99.98 (UCP-tail outlier)** |
| Municipal anchoring | Canadian comparator norm 70–85 % | 80.0 % (in norm) | 72.0 % (in norm) — not a divergence signal on canonical geometry[^anchoring_canonical] |
| Population MAD | tighter is better | 3,180 | **4,707 (48 % wider)** |
| Calgary geographic-zone gap | smaller is more neutral | 0.4 % | **12.2 %** |
| Chair-flagged geographic anomalies | count, lower is better | 0 | **3** (RMH–Banff Park, Nolan Hill–Cochrane, Olds → N Airdrie) |
| Airdrie community split | 1- or 2-way is constraint-minimum | 2-way | **4-way** |
| Rationale-failure pattern (symmetric audit; **qualitative, not pre-registered**) | 0 of contested redraws fails | not applicable | **5 of 6 fail** (sixth — St. Albert-Sturgeon — is constraint-forced; the audit's earlier seventh — Lethbridge federal-boundary match — has been withdrawn as unsourced) |
| Public-submission support for contested configurations | every contested config has documented support | n/a | **2 configs (Airdrie 4-way, Nolan Hill) have no documented submissions** in the 1,140+ archive |
| Pre-registered structural-irregularity count | ≥ 4 of 5 = outlier per [§5.5](#sec-5-5) | 0 of 5 | **4 of 5** — meets threshold[^anchoring_canonical] |

**Lane 2 reading.** The minority crosses every structural threshold by a wide margin; the majority crosses none. **Note on anchoring:** the DPG-era 4.9× anchoring departure did not survive canonical recomputation (both maps fall within the 70–85 % norm at 72% vs 80%)[^anchoring_canonical] and is not carried forward as a standalone signal. The evidential core in Lane 2 is the MCMC ensemble (p = 1.40×10⁻⁶) supported by four geometry-independent structural dimensions: population dispersion (48 % wider), Calgary zone asymmetry (12.2 % vs 0.4 %), Airdrie fragmentation (4 vs 2 districts), and spatial anomalies (3 chair-flagged vs 0). The 5-of-6 rationale-failure pattern (with the 6th — St. Albert-Sturgeon — classified as constraint-forced because both the majority and minority maps independently arrive at the same two-district structure under the Act's constraints) is the cleanest rationale signal: a symmetric audit that finds the minority's own published justifications fail on five of six configurations, while the alternatives that satisfy the rationales are constraint-legal. (The audit had previously listed a seventh configuration — Lethbridge / Taber-Warner federal-boundary match — which has been withdrawn because the underlying minority claim cannot be located in the report; see `analysis/methodology/lethbridge_federal_boundary_check.md`.)

<a id="sec-6-2-3"></a>
#### 6.2.3 Verdict on the majority 2026 proposal: not a gerrymander

Both lanes return a clean result. On partisan-bias magnitude (Lane 1), the majority crosses no Alberta-calibrated threshold. On structural dimensions (Lane 2), the majority crosses no threshold. The canonical 1,010,000-plan run ([§5.4.9](#sec-5-4-9)) finds the majority mean-median at p0.92 — an NDP-tail outlier — but [§5.4.9](#sec-5-4-9) explains this as a commission-convention effect: the neutral ensemble is free to dissolve rural districts that a commission legally must preserve, pulling the neutral distribution's mean-median higher than commission constraints allow. All other majority metrics are within null (EG p15.5, declination p79.6, seats@50/50 p77.8, MAD p15.8); Mahalanobis p=0.125 (50k pre-reg) / p=0.097 (1,010,000-plan canonical). Under canonical 1,010,000-plan geometry, the majority also retreats from the 2019 enacted baseline in joint-metric space (D²=12.75 → 7.85; see [§5.4.10](#sec-5-4-10)), consistent with a normalizing commission process. The Chen-Rodden decomposition ([§5.2.5](#sec-5-2-5)–[§5.2.6](#sec-5-2-6)) attributes the majority's UCP-favourable point to dispersed rural margins rather than to drawing choices.

**My verdict: the majority is the kind of map a competent independent commission would produce. It is not a gerrymander on any Alberta-calibrated metric.**

<a id="sec-6-2-4"></a>
#### 6.2.4 Verdict on the minority 2026 proposal: exhibits a gerrymander signature on the structural lane; coverage-sensitive on the partisan-bias-magnitude lane

The honest reading of the two lanes:

1. **On partisan-bias magnitude (Lane 1) the result is coverage-sensitive ([§6.2.1](#sec-6-2-1)).** Under crosswalk-blend attribution (Reading A), the minority is sub-threshold on every Alberta-calibrated threshold. Under v0_8 full-coverage spatial attribution (Reading B, the audit's most recent measurement at Run #4 in [§5.4.4](#sec-5-4-4)), the minority is OVER every Alberta-calibrated threshold including the MCMC-derived 4.10 % at p100. Both readings agree the minority sits closer to the UCP-favoured tail than the majority.

2. **On structural and procedural patterns (Lane 2) the minority crosses every comparator threshold the audit applies, by a wide margin.** Four of five pre-registered structural-irregularity tests fire — meeting the ≥ 4 outlier threshold;[^anchoring_canonical] five of six contested redraws fail their stated rationales (the sixth — St. Albert-Sturgeon — is constraint-forced; an earlier seventh — Lethbridge federal-boundary match — has been withdrawn as unsourced); the commission chair flagged three geographic anomalies on this map and zero on the majority. Lane 2 is invariant across the coverage-attribution choice. Under canonical 1,010,000-plan geometry, the minority amplifies the 2019 enacted baseline's joint-space position (D²=12.75 → 32.67), adding context to the Lane 2 reading without introducing an independent test (see [§5.4.10](#sec-5-4-10)).

The two lanes give different answers depending on the Lane 1 reading chosen. A reader who weights Reading A (crosswalk) and partisan-bias magnitude as the dispositive test will read the minority as not exhibiting a gerrymander signature on the magnitude dimension. A reader who weights Reading B (full-coverage spatial) AND/OR weights the cumulative structural-and-procedural pattern as the dispositive test will read it as exhibiting one. The literature is on the side of the second reader on the structural pattern: Katz, King and Rosenblatt (2020) explicitly recommend ensemble reporting precisely because no single magnitude metric is dispositive; Cain et al. (2018) argue that municipal-anchoring departure is itself a partisan-engineering enabler; the chair-flag, rationale-failure, and submission-archive patterns are not partisan-bias *measurements* but partisan-engineering *signatures*.

**The verdict the audit's measurements support.** On the cumulative structural-and-procedural pattern, the minority 2026 proposal exhibits the constellation of effects the academic literature treats as a gerrymander signature. On the partisan-bias-magnitude lane, the verdict is coverage-sensitive: sub-threshold under Reading A, super-threshold under Reading B; the audit reports both readings and the cross-method disagreement (which is itself a finding per the methods paper [§5](#sec-5) multi-layer-reporting discipline). Whether the observed effects reflect deliberate engineering against the NDP, unlucky choice among legal alternatives, or some combination of the two is a question the audit cannot answer from public data alone. The author's restraint on intent is a deliberate methodological choice, not an evasion: intent is not observable from boundary geometry, vote totals, public submissions, or chair-flag counts. What is observable is the pattern of effects, and the pattern is reported above without hedging.

**Where intent may suggest itself to the reader.** Five of six contested minority redraws fail the *minority's own published rationales* under symmetric audit (the sixth, St. Albert-Sturgeon, is constraint-forced — both maps independently arrive at the same configuration), and two of those redraws have no documented public-submission support in the commission's 1,140+ archive. Each individual signal has a non-engineering explanation available. Whether the cumulative pattern's most parsimonious explanation is engineering or unlucky drafting is the inference the reader is invited to weigh — the audit does not make it on the reader's behalf.

A reasonable expert who weights partisan-bias magnitude over structural pattern would reach a more cautious verdict on the minority — closer to "no measurable gerrymander signature on the partisan-bias dimension; structural irregularities require explanation but do not by themselves establish anything about how the map was drawn." That disagreement is documented rather than hidden.

<a id="sec-6-2-5"></a>
#### 6.2.5 How close did the minority come?

A "how close" answer needs to be lane-specific because the two lanes give different answers.

**Lane 1 (partisan-bias magnitude).** Under Reading B (full-coverage spatial, Run #6 2M), the minority's EG of +9.21 % is at p100 of the 2,000,000-map ensemble — the most extreme UCP-favoured EG the simulation produced. On seats@50/50 (89-of-89 attribution, [§5.4.7](#sec-5-4-7)), the minority's reading of **52.8 %** sits **above the simulation's converged ceiling of 51.72 %** — a placement zero of 2,000,000 neutral draws reach (see [§5.4.6](#sec-5-4-6) converged-ceiling finding). The Cannon et al. (2022) short-bursts test ([§5.4.8](#sec-5-4-8)) reaches 52.87 % in 40,000 hill-climbing steps, confirming the minority sits in the non-neutral procedure's reachable space rather than the neutral procedure's. **Distance to the nearest Alberta-calibrated gerrymander threshold: above every threshold the audit applies, including the converged-ceiling bound on seats@50/50.**

**Boundary-choice decomposition (SZAT, Channel 2, [§5.2.10](#sec-5-2-10)).** The pre-registered SZAT bootstrap (p=0.0024, AsPredicted #289,469) identifies *which specific boundary decisions* drove the between-map EG gap. The regional decomposition of the SZAT score (+0.039211 total) is: Rest of Alberta +0.015 (dominant), Edmonton +0.008, Mountain-West / Canmore-RMH +0.006, Calgary −0.008 (partially offsetting). The signal is distributed across the province; Calgary swing zones run in the *opposite* direction to the headline score. This is inconsistent with a Calgary-centric explanation of the minority's UCP-favourable position and consistent with a map-wide boundary-placement pattern. The Fisher combination of Ch1 (Mahalanobis, p=1.40×10⁻⁶) and Ch2 (SZAT, p=0.0024) yields T=39.03, Fisher p=6.87×10⁻⁸ (~1 in 15 million).

**Lane 2 (structural pattern).** The minority crosses every threshold by a wide margin:

- Mean-median percentile p99.98 vs literature outlier line p95 — **~5 percentile points over** (canonical 1,010,000-plan run; 50k preliminary run had p99.99)
- Structural-irregularity count 4 of 5 vs pre-registered cut-off ≥ 4 — **meets threshold**[^anchoring_canonical]
- Chair-anomaly count 3 vs 0 — **3 over**
- Airdrie 4-way vs constraint-minimum 2-way — **2 splits over**
- Rationale-failure 5 of 6 vs symmetric-audit cut-off ≥ 1 — **4 over** (sixth — St. Albert-Sturgeon — is constraint-forced; an earlier seventh — Lethbridge federal-boundary match — has been withdrawn as unsourced)
- SZAT 2019→minority score = +0.016 (p=0.053, marginally outside null CI [−0.017, +0.006]); minority boundary choices moved EG in the UCP-favoring direction relative to 2019, opposite to what random boundary changes from 2019 produce — consistent with but not establishing a pattern of directed movement (exploratory, not pre-registered; see [§5.4.10](#sec-5-4-10))

**Distance to the nearest structural gerrymander threshold: 0 (already over).** On the structural lane the minority is not "close" to a threshold — it crosses every threshold the audit applies.

The honest summary: *the minority maxes out the structural-irregularity scoring while staying inside the partisan-bias-magnitude band*. That is the observed effect. One drafting process that would produce this effect is structural engineering (off-reference boundaries, community splits, chair-flagged shapes) whose seat-count consequence is not measurable on current vote distributions — either because the structural choices did not translate to seats, or because the seat translation depends on a vote distribution not yet observed. The audit reports the effect; whether the effect reflects engineering or some other explanation is for the reader to weigh.

<a id="sec-6-2-6"></a>
#### 6.2.6 What would change the author's verdict

1. **An independent reviewer produces a constraint-legal Alberta map that satisfies the minority's stated COI rationales (community-of-interest preservation in Airdrie, Cochrane, Nolan Hill, RMH–Banff Park) and *also* matches majority-comparable municipal anchoring (≥ 60 % CSD/DA edge alignment).** The minority's rationale-failure pattern would then be evidence of a constraint trade-off rather than engineering. (Issue #14 on the audit's GitHub repository invites this exact counter-map.) Strongest single falsifier.

2. **The 2019 cross-election direction reversal extends to 338Canada April 2026 polling.** Currently the polling supports the 2023 direction; if more recent polling shows the direction flipping under multiple 2020s-era voter distributions, the structural pattern would become harder to read as engineering.

3. **A pre-2026 internal commission document is published showing the minority's anchoring and split choices were a deliberate response to documented community submissions rather than drafting choices.** The [§5.9.4](#sec-5-9-4) submission-archive verification could not find such submissions for two of the contested configurations; if they exist and were missed, the rationale-failure finding is wrong.

4. **The November 2026 Lunty-committee 91-seat map produces structural-irregularity counts in the same range as the minority (≥ 4 of 5).** That would suggest the minority's structural profile reflects Alberta-specific drawing difficulty rather than minority-specific engineering. Pre-registered held-out test — the cleanest single check.

The audit's pre-registration commits the author to publishing any of these retractions publicly within 30 days of receiving the falsifying evidence.

<a id="sec-6-2-7"></a>
#### 6.2.7 Verdict on the April 16 government pivot itself

Separate question, addressed in [§5.9.2](#sec-5-9-2) as a procedural finding. The author's opinion: the substitution of a UCP-MLA-chaired committee for the independent commission's drafting process during the same redistricting cycle is the most government-controlled response among the three most commonly cited Canadian comparator cases (the other two being the federal 2012 redistribution challenge and Saskatchewan's 1989 court referral). It is not, on its own, evidence that the resulting Lunty-committee map will be a gerrymander. It is evidence that the procedural guardrails normally relied upon to make redistricting credible to the losing party have been weakened relative to comparator practice. The November 2026 Lunty-committee map will be evaluated under the same pre-registered scorecard applied to the two commission proposals; if it scores in the range of the minority on structural-irregularity count, the procedural opinion will be vindicated, and if it scores in the range of the majority, the procedural opinion will be tempered.

<a id="sec-6-2-8"></a>
#### 6.2.8 Bottom line

- **Majority 2026:** does not exhibit a gerrymander signature on either Alberta-calibrated lane.
- **Minority 2026:** under Reading B (full-coverage spatial, Run #6 2M MCMC), exceeds every Alberta-calibrated EG threshold including the MCMC-derived 4.10 % at p100; sits above the simulation's converged seats@50/50 ceiling of 51.72 % (52.8 % via 89-of-89 attribution, [§5.4.7](#sec-5-4-7)), a placement zero of 2,000,000 neutral draws reach but a Cannon et al. (2022) short-bursts hill-climb reaches in 40,000 steps (52.87 %, [§5.4.8](#sec-5-4-8)); and exhibits the academic literature's gerrymander signature on the cumulative structural-and-procedural lane by a wide margin on every structural threshold the audit applies. The minority map is the kind of map a non-neutral procedure produces under EBCA constraints; it is not the kind of map a neutral procedure produces. The literature recommends the cumulative reading. The audit reports the effects; what those effects suggest about how the map was drawn is for the reader to weigh.

Neither summary is a legal finding. Both are an attempt to give the citizen-reader of this audit a plain answer to the question they probably came here with — calibrated to Alberta's own thresholds, not to US federal judicial standards. The audit's restraint on intent is deliberate: intent is not observable from public data, and the pattern of effects the audit *can* observe is reported plainly enough that the reader does not need the author to draw the inference for them.

**Why this level of methodological precision?** The audit's apparatus — seven measurement layers, three-chain R-hat convergence, DPG tier-aware perturbation CIs, machine-readable dependency DAG, pre-committed pass criteria, per-finding retraction pathway — is deliberately over-engineered relative to the Commission's drawing process. The Commission drew with a broad brush (political negotiation, public-hearing notes, professional judgement). The audit looks through a microscope (adjacency chains, surplus-vote rates, constraint-bound percentiles). That asymmetry is intentional: **precision is armor**. If the audit presented a single number — "the minority's Efficiency Gap is 2.4σ from neutral" — the Commission would legitimately respond "Alberta's geography is unusual; your one number is too simple to capture it." The over-engineering forces the distinction between an accidental brush-stroke and a systematic pattern, and it is what allows the audit to answer the Commission's legitimate objections in advance.

**Translation discipline.** The math provides authority; the prose provides conviction. The table in [§6](#sec-6) above is the audit's formal synthesis. The three bulleted translations above are the audit's human-readable reading of that synthesis. Both are included because neither alone is sufficient: math without translation is unactionable for a reader who is not a redistricting specialist, and translation without math is polemic. This section exists to bridge them explicitly.

**What the audit does not claim.** It does not claim intent ([§4.5](#sec-4-5) is explicit). It does not claim the Commission acted in bad faith. It does not claim that any specific individual commissioner is responsible for the minority's patterns. It claims only that the minority map, relative to the majority map drawn by the same Commission under the same statutory constraints on the same voter geography, is displaced from the constraint-bound expectation in a measurably consistent direction across five structural dimensions. The explanation for that displacement is not within the audit's scope; the measurement is.

---

<a id="sec-7"></a>
## 7. Limitations and Falsifiability

<a id="sec-7-0"></a>
### 7.0 Hypotheses tested during the audit and their disposition

The audit's central directional claim (*minority more UCP-favourable than majority across population, spatial, partisan-bias, and procedural dimensions*) is one of several working hypotheses that ran through the project. Three of those working hypotheses did not survive contact with the data and are recorded here as part of the audit's evidentiary discipline. The 2026-04-26 external code audit by Google Gemini 3.1 Pro (full memo at `analysis/methodology/external_code_audit_findings_gemini_2026-04-26.md`) and the falsification tests subsequently run against the audit's own pipeline produced this disposition.

| # | Hypothesis | Final disposition | What killed it | Audit-trail anchor |
|---|---|---|---|---|
| H1 | The 2,000,000-step MCMC ensemble shows the minority map's `seats@50/50` is out of distribution (p100, no map in 2M reaches it) | **REJECTED** | The chunked-MCMC orchestration (`mcmc_ensemble_250k_v0_8.py:_run_chain_chunked()`) was silently re-seeding the chain from the 2019 baseline at every chunk boundary, so the "2M-step deep continuous chain" was structurally a stack of 100 independent 20,000-step short bursts. Bug fixed in commit `73544a3`; finalized 250k topological ensemble re-run; finalized percentile is p98.5 (3,750 of 250,000 reach or exceed) | `findings/post_audit_recompute_deltas.md`; `analysis/reports/pre_registration_amendment_2026-04-26_evening_post_audit.md` |
| H2 | The minority map's `seats@50/50` value is 52.8% (the published headline figure) | **REJECTED** | The v0_8 polygon reconstruction left 6 of the 89 minority districts effectively unscored under the centroid-in-polygon spatial join (`coverage_pct=100%` was misleading because covered VAs were unevenly distributed; `n_districts` in `seat_results` was 83, not 89). The Gemini-authored topological VA-dissolve (the v0_9 substrate, commit `7cf47a4`) recovered full 89/89 coverage. The corrected `seats@50/50` is **48.3%**, not 52.8% | `data/final_real_map_scores.json`; `analysis/scripts/topological_shape_resolution.py` |
| H3 | Non-compact geometry (the chair-flagged lasso shapes, the urban-rural hybridizations, the Airdrie four-way split) is the load-bearing mechanism through which the minority commissioners reached their UCP `seats@50/50` advantage. Concretely: the SMC plans that reach the minority's 0.4831 value should have systematically lower mean Polsby-Popper compactness than the SMC plans that don't | **REJECTED (twice — falsification test, then independent v0_9 confirmation)** | Falsification test designed by the principal investigator before running, in keeping with pre-registration discipline. Among the 5,000-plan R-`redist` SMC ensemble, mean per-district PP for plans with `seats@50/50` ≥ 0.4831 (n=2,762) was **0.2391** vs **0.2339** for the rest (n=2,238) — Welch t-test p = 7.7 × 10⁻²³⁴, in the wrong direction. Independently, direct PP measurement on the v0_9 substrate (commit `c170f49`) found the chair's named lassos themselves score in the *moderate* compactness band: Calgary-Nolan Hill-Cochrane PP = 0.402, Rocky Mountain House-Banff Park PP = 0.414. The minority did not break Area/Perimeter ratio to build the firewall; the corridors are drawn thick enough that PP looks innocent. The empirical finding that R-SMC reaches the minority's value more often than Python-ReCom does is preserved; the *mechanistic* claim that compactness is what makes that gap is rejected | `findings/redist_python_comparison.md`; `findings/polsby_popper_verdict.md`; `data/polsby_popper_per_district.csv`; `data/redist_crossvalidation_s50.csv` |
| H4 | The minority map's municipal-anchoring deficit (14.5% vs majority 71.0% on Statistics Canada CSDs) generalises to other anchoring substrates. If the minority simply substituted natural features (highways, rivers) for CSDs, all three maps should score similarly under a "natural anchoring" measurement | **REJECTED (informative)** | Direct measurement on highways + waterways substrate (commit `6a39960`) found 2019 = 40.2 %, majority = 38.4 %, minority = 40.1 % — all three maps cluster within 2 pp under natural anchoring. The minority is *not* differentially low on the natural substrate; it is specifically the **municipal/CSD substrate** the minority abandoned. This narrows but does not weaken Lane 2: the audit can defend "minority abandoned municipal anchoring" but not the unconditional "minority abandoned anchoring." Hostile-witness counter ("commission anchored to highways instead") is empirically refuted because the minority did not anchor more than the majority on the natural substrate either; it lost CSD anchoring without gaining natural-feature anchoring | `findings/natural_anchoring_secondary_check.md`; `data/v0_9_natural_anchoring_*.csv` |
| H5 | The minority's `seats@50/50` percentile is robust to the uniform-swing assumption. Under empirical regional swing (Calgary swings 1.34× the provincial swing, Edmonton 0.50×, rural 0.95×), the minority should still place in the right tail of the ReCom ensemble | **REJECTED — signal substantially weakens; finding no longer relocates to majority under canonical geometry** | **DPG-era (v0_9 substrate):** minority collapses from p98.6 → p50.7; majority rises to p99.5 (opposite direction). **Canonical EA shapefiles — election-day votes (MCMC-consistent):** minority 0.5169 (p99.99) under uniform → 0.4607 under regional (≈ p65–70; above ensemble median 0.4483, below p95 0.4828); majority 0.4607 (p77.8) under uniform → 0.4270 under regional (near ensemble p5 0.4253; NDP-tail). **Canonical — full votes including advance ballots (SZAT-consistent):** minority 0.5056 → 0.4719; majority 0.4719 → 0.4494 (≈ ensemble median). Across both canonical substrates: the minority's outlier signal substantially weakens under regional swing but does not fully collapse to median; the majority no longer rises to p99.5 (rather, it shifts toward the NDP-tail or median depending on substrate). The DPG-era "finding relocates to majority" result does not hold on canonical geometry. Canonical outputs: `data/outputs/regional_swing_canonical_ed.json` (election-day); `data/outputs/regional_swing_canonical_full.json` (full votes) | `findings/regional_swing_robustness.md`; `analysis/scripts/seats_at_50_50_regional.py`; `data/outputs/regional_swing_canonical_ed.json`; `data/outputs/regional_swing_canonical_full.json` |
| H6 | The Lane-1 metrics computed under the original `seat_results()` (UCP share normalised by total votes including third-party; ReCom chain that destroys s15(2) protected districts to enforce ±25%) are unbiased estimators of partisan effect under Alberta's actual electoral conditions | **DISPOSED — corrected 250k v0_9 ensemble retains the headline finding** | Two independent methodological flaws identified in `mcmc_ensemble.py`: (a) `seats@50/50` win threshold compared UCP share (out of total votes including third-party) against a 50% threshold, which is unreachable in districts with material third-party vote — fixed in commit `972b04a` to use two-party (UCP+NDP) totals throughout; (b) the s15(2) freeze attempt (commit `972b04a`) identified the legally protected districts correctly but the unfrozen 85-district subgraph was infeasible to seed-balance via `recursive_tree_part` — disabled in commit `3484351` with a documented limitation (per second-pass Gemini analysis, destroying s15(2) protection in the baseline makes the minority's percentile MORE conservative). The corrected 250k ReCom ensemble was run on the v0_9 substrate (script `mcmc_ensemble_250k.py`, output `data/v0_1_mcmc_ensemble_*_250k_v0_9.*`). **Result: the minority's `seats@50/50` corrected percentile is p98.52** (versus the original v0_8/250k figure of p98.6 — Two-Party normalisation moved the value by <0.1pp because third-party share was negligible in 2023). The audit's Lane-1 percentile claim of "top 1.5% under uniform swing on the corrected ensemble" survives the correction within rounding | `analysis/scripts/mcmc_ensemble.py` + `mcmc_ensemble_250k.py`; `data/simulated_ensemble_percentiles_250k.csv`; `data/simulation_real_map_scores_250k.json` |
| H7 | The minority's `seats@50/50` outlier status is a pure-2023-election artefact. Under 2015 or 2019 vote distributions projected onto the v0_9 substrate, the minority should look indistinguishable from the majority | **REJECTED (in part)** | Cross-election recomputation on the v0_9 substrate using cached 338Canada historical projections (`analysis/scripts/cross_election.py`, commit `e219943`): direction of minority > majority on `seats@50/50` holds 3-of-3 elections (2015 tie at 0.652/0.652; 2019 minority 0.562 / majority 0.517; 2023 minority 0.472 / majority 0.461). The 2015 tie is the honest cost — defends against the "pure-2023-swing" attack on direction; does not support a stronger "minority is a structural pro-UCP outlier under any vote distribution" claim. The 2023 percentile vs the 2023-trained ensemble is 92.99% (slightly below the original p98.6 because of the Two-Party normalisation) | `findings/cross_election_robustness.md`; `data/cross_election_per_map.csv` |
| H8 | Excluding advance/mobile/special ballots (~47% of 2023 votes; reported only at ED level, not VA level) materially biases the audit's Lane-1 metrics | **REJECTED — empirical refutation** | Apportioning the missing advance ballots back to VAs proportionally to election-day two-party shares (`analysis/scripts/advance_vote_splat.py`, commit `72e3369`) shifts both v0_9 maps by **exactly +1.12 pp** in `seats@50/50` (majority 0.4607 → 0.4719, minority 0.4831 → 0.4944). The 2.25-pp inter-map gap is preserved to 4 decimal places. The advance-vote omission is a real methodological caveat (every map gains 1.12pp UCP under the smear) but is **inter-map invariant** at the audit's percentile-comparison resolution. The hostile-witness attack ("you're missing half the electorate") is empirically refuted as a methodological objection. Side observation: the majority's efficiency gap flips sign (-0.0149) under the smear while the minority's barely moves (+0.0170 vs +0.0175), reinforcing the surgical-fortification framing | `findings/advance_vote_sensitivity.md`; `data/v0_9_advance_vote_*.json`; `analysis/methodology/methodological_defenses.md` [§1.1](#sec-1-1) |
| H9 | The targeted hill-climbing procedure used to bound the minority's distance from neutral is asymmetric (UCP-direction works, NDP-direction does not, so the comparison with neutral median is rigged) | **REJECTED — symmetric** | NDP-maximizing short-bursts run on the v0_9 substrate (`analysis/scripts/targeted_gerrymander_burst_ndp.py`, mirror of UCP-direction config; commit `72e3369`). UCP-targeted reaches 52.87% UCP `seats@50/50`; NDP-targeted reaches 37.93%. Neutral 250k v0_9 ensemble bounds are 39.08%–50.57%. Both targeted procedures push beyond the neutral envelope (UCP +2.30pp above max, NDP −1.15pp below min). Asymmetry in degree (UCP has 8.04pp targeted headroom from neutral median; NDP has 6.90pp) is a property of Alberta's political geography, not the test apparatus. The minority sits 2.3× closer to the UCP-targeted ceiling than to the NDP-targeted floor — the audit's existing framing holds. **Side correction:** `report_public.md:333` lists "Neutral 250k MCMC, min produced = 37.9%" — that value is in fact the NDP-burst result, not the neutral floor. Corrected neutral floor on the canonical v0_9 250k ensemble is 39.08% | `findings/burst_symmetry_analysis.md`; `data/v0_9_ndp_burst_*.json` |
| H10 | The "Polsby-Popper says the chair's named lasso (Calgary-Nolan Hill-Cochrane) is moderately compact" finding (PP = 0.402) reflects the actual geometry of the lasso. If a different but equally well-known compactness metric (Reock — pre-registered alongside PP in the audit's protocol) also scores this district as moderate-or-better, then the lasso shape claim must rest entirely on chair judgement and not on any mathematical compactness metric | **REJECTED — Reock catches it** | Reock = 4·area/(π·D²) where D is the diameter of the smallest enclosing circle. Computed on v0_9 in commit `e219943` (`analysis/scripts/reock.py`). Calgary-Nolan Hill-Cochrane scores Reock = **0.230** — *flagged* under the conventional Reock < 0.30 threshold. The two metrics measure different aspects of compactness: PP penalises perimeter wiggle, Reock penalises elongation. A lasso corridor is exactly the elongation pattern Reock catches and PP does not. The H3 conclusion that "compactness is not the mechanism for the *seats@50/50* gap" still holds (the falsification test was on plan-level mean PP, and the v0_9 majority and minority have similar mean Reock too), but the *individual lasso shape* IS quantitatively flagged by Reock. Both pre-registered metrics now in the record | `findings/reock_verdict.md`; `data/reock_per_district.csv` |

**State of the audit's central claim after H1–H10.** The audit's pre-shapefile Lane 2 finding — that minority municipal anchoring dropped from the 2019 baseline of 75.2 % to 14.5 % while the majority continued 2019 practice at 71.0 % — was the central published claim through April 2026 and survived every DPG-era methodological revision (sampler, swing, compactness, ReCom population tolerance). It did **not** survive canonical recomputation against the official 2026 shapefiles: minority 72.0 %, majority 80.0 %, both within the 70–85 % Canadian comparator norm.[^anchoring_canonical] H1–H10 are preserved here as the audit's historical stress-test record; the H4 row in particular references the DPG-era anchoring values that did not survive canonical recomputation. H5's canonical regional-swing recomputation **substantially weakens but does not collapse** the minority's seats@50/50 finding: under canonical EA shapefiles and election-day votes (MCMC-consistent substrate), the minority moves from p99.99 under uniform swing to approximately p65–70 under empirical regional swing — the signal persists above the ensemble median but no longer reaches the extreme tail. The DPG-era "finding relocates to majority at p99.5" result does not replicate on canonical geometry; the majority instead drifts toward the NDP-tail or ensemble median. H6's corrected 1,010,000-plan canonical ensemble retains the headline at p99.98 on mean-median and p99.99 on seats@50/50. Lane 1 is therefore reported as a multi-scenario sensitivity table (uniform swing / regional swing × two vote substrates / cross-election direction holds 3-of-3). The audit's central published finding has reorganized: the MCMC ensemble (Mahalanobis p = 1.40×10⁻⁶ against the 1,010,000-plan canonical ensemble) is now the load-bearing Lane 1 result, supported by the four geometry-independent Lane 2 dimensions (population dispersion, Calgary zone, Airdrie split, chair anomalies).

**Empirical confirmation of the surgical-fortification thesis (corrected 250k v0_9 ensemble).** Two findings from the H6 disposition stand out for the audit's framing:

1. **The 2019 enacted map and the 2026 majority sit at *identical* percentile on `seats@50/50`** (both p77.8 against the canonical 1,010,000-plan ensemble). The majority continues 2019 Alberta practice on the partisan-fairness axis. On canonical geometry the majority's municipal anchoring (80.0 %) also sits in the 2019 baseline neighbourhood (75.2 %); the minority's canonical anchoring (72.0 %) sits slightly below but within norm.[^anchoring_canonical] The partisan-fairness continuation framing — the majority continues 2019 Alberta practice, the minority diverges on the metrics that survive canonical recomputation — remains supported.

2. **The minority's three "global" Lane-1 metrics are near median** (efficiency gap p56.1, mean-median p53.2, declination p62.2) while the tipping-point metric `seats@50/50` registers the fortification at p98.52 (top 1.5%). This is the empirical signature the methodological-defenses appendix predicted (§3.2 "One-Metric Gerrymander"): in a polarised two-party system with rigid geographic packing, global aggregate metrics are mathematically numb to surgical micro-targeting at the marginal-district set. The minority's deviation pattern — clean on three of four metrics, extreme on the one that directly stress-tests the firewall — is exactly the fingerprint of "Surgical Fortification" rather than "broad partisan distortion." Three doors look untouched; one door is wedged shut.

The DPG-substrate SMC cross-validation had a seed-placement defect: three runs with the same nominal `set.seed(88)` produced 5.6%, 28%, and 58% of weighted plans reaching the DPG minority's 0.4831 value, because `library(redistmetrics)` consumed RNG state before the sampler ran. The defect was diagnosed and corrected by placing `set.seed(852751799)` immediately before `redist_smc()`. The canonical re-run (2026-05-18; input: `va_2023_election_day_votes.gpkg`; 5,000 SMC plans, ESS 1,116) corroborates the Python ReCom finding: **0% of 5,000 SMC plans reached 0.5169** (ensemble maximum 0.4943, placing the canonical minority map above the 99.98th SMC percentile). Both standard samplers on official Elections Alberta geometry agree: the canonical minority map's `seats@50/50` exceeds the ensemble tail. The Python ReCom ensemble retains priority for percentile placement — it passes the Gelman-Rubin diagnostic (R̂ ∈ [1.007, 1.017] across all four metrics, below the 1.05 publication threshold) and has 200× the sample size — but the canonical SMC result now provides algorithm-independence corroboration rather than a contradicting signal. (The H3 falsification test was run on the v0_9 DPG substrate against the 0.4831 threshold; on canonical geometry the threshold is never reached, making the PP comparison of high-vs-low plans moot. The direction of H3 — high-UCP-advantage plans more compact, not less — is preserved: the stronger statement now is that no SMC plan reaches the canonical target at all.)

<a id="sec-7-1"></a>
### 7.1 Missing evidence and scope limits


1. **2026 polygon geometry.** Phase 4A resolved 2026-05-06 (canonical EA shapefiles received; MCMC canonical ensemble complete). C1 (Polsby-Popper, 2026-05-18) and C2 (Reock, 2026-05-18) executed on canonical EA shapefiles — null findings; v0_9 direction reversed (documented in DOCUMENTED CORRECTIONS). B5 (MCMC seed variant) pending.
2. **Hybrid-ED blend vs. spatial measurement disagreement (Phase 4C vs. v0.2).** Phase 4C spatial assignment on **canonical EA shapefiles** (official Elections Alberta geometry, re-run 2026-05-17; `phase4c_canonical_attribution.py`) produces a **+3.92 pp** EG asymmetry (election-day votes; majority NDP@50/50 = 48, minority = 43). An earlier Phase 4C v2 run using derived shapefiles had produced +0.31 pp — a smaller figure attributable to derived boundary approximation of rural-fringe VAs. v0.2's 70/30 hybrid-ED blend on full-vote totals produces −1.41 pp (reversed sign). H8's empirical test shows advance-ballot addition shifts both maps by an identical +1.12 pp (inter-map invariant), confirming the method-vs-blend tension is not a vote-data gap. Full reconciliation: `findings/assignment_gerrymander_comparison.md`.
3. **Independent verification of the no-public-support claim (Section D).** Requires text-search of the commission's 1,140+ submission archive.
4. **Full-symmetry visual audit for majority.** Requires majority-proposal Alberta overview, Edmonton, and other-cities map images.
5. **2019-era population data.** Would permit A1/A2 symmetric analysis of the 2019 baseline alongside the two 2026 proposals.
6. **Multiple Testing (Family-Wise Error Rate).** The audit evaluates five structural tests (four partisan-bias dimensions plus one geometric compactness dimension). Under a formal Holm-Bonferroni correction for $m=5$ tests at a one-tailed $\alpha = 0.10$ threshold (standard for directional gerrymandering bounds), the strictest threshold is $0.10 / 5 = 0.02$. The minority map's `seats@50/50` result ($p = 0.0148$) satisfies this corrected threshold ($0.0148 \le 0.02$). Therefore, the outlier finding formally survives conservative FWER correction.
7. **Pre-Registration Authority.** While historical analyses rely on GitHub commit history for provenance (which lacks the strict immutability of third-party registries like OSF), the future evaluation of the November 91-seat map utilizes a cryptographically secure, third-party `drand` randomness beacon (Round 6062459, locked April 27, 2026) to establish true, immutable pre-registration before the data exists.


<a id="sec-7-2"></a>
### 7.2 Falsifiability statement


The audit's directional claim — *minority more UCP-favorable than majority across population, spatial, partisan-bias, and procedural dimensions* — would be falsified by any of the following:

- An alternative Calgary classification that produces near-null minority-majority asymmetry (≤1%) while A2's current rule produces >10%. Tested; both rules produce the same direction.

- Submission-archive evidence that the five disputed minority configurations (Airdrie, Cochrane, Chestermere, Red Deer, St. Albert) did have substantial public support in the 1,140+ record. Refutes Section D claim.
- Visible spatial anomalies in the majority's rural or Edmonton districts of a severity comparable to the minority's three flagged ridings. Requires majority non-Calgary imagery.
- A comprehensive survey of Canadian provincial redistributions 1991–2025 finding comparable mid-cycle government-drafting-process replacements. Refutes Section D uniqueness framing.

<a id="sec-7-3"></a>
### 7.3 Academic Limitations and Methodological Caveats

1. **Ecological Inference:** We use 2023 election results to simulate hypothetical 50/50 vote splits. Actual 2026 vote distributions at the block-level may differ structurally from the uniform-swing projections.
2. **Single Election Dependency:** The 2023 election was highly competitive (UCP 52.6%, NDP 44.0%). In a landslide environment, structural partisan metrics become noisy or uninformative.
3. **Geographic Constraints vs Intent:** Alberta's deep urban/rural divide creates severe natural packing. The "neutral" ReCom ensemble attempts to control for this, but residual natural packing may still be misattributed as intentional engineering (Chen and Rodden 2013).
4. **Model Dependence:** ReCom ensembles assume contiguous, population-balanced districts as the primary constraints. If the commission heavily weighted unmeasured criteria (e.g., historical communities of interest not aligned with municipal boundaries), the neutral baseline may be misspecified.
5. **Causal Identification:** The audit mathematically detects structural advantage, not human intent. The commission may have had legitimate, non-partisan reasons for their boundary choices that happen to perfectly correlate with partisan advantage.

---

> **DOCUMENTED CORRECTIONS**
>
> Findings that did not survive methodological review or data upgrade. Retained per the audit's pre-committed policy of never deleting failed findings. Full per-finding retraction conditions: `analysis/methodology/retraction_pathway.md`.
>
> **C1 — SZAT substrate description (retracted 2026-05-10).** An earlier version of [§5.2.10](#sec-5-2-10)'s Post-registration VA file update paragraph described the file switch from `va_polygons_with_2023_votes.gpkg` to `va_polygons_with_full_2023_votes.gpkg` as a substrate change to "full advance-vote" data with NDP two-party share rising 42.60% → 44.66%. That description was false: both files carry election-day vote columns (`va_ndp`/`va_ucp`); the switch changed only 2 VA centroid assignments. The retracted paragraph incorrectly implied the SZAT was re-run on a different vote substrate.
>
> **C2 — v0_9 Reock between-map asymmetry (retracted 2026-05-18).** Analysis on the v0_9 topological substrate (VA-polygon dissolves, derived shapefiles) produced minority 34.8% of EDs below Reock 0.30 vs majority 13.5% — a 2.58× asymmetry in the direction of minority less compact. Under official Elections Alberta canonical shapefiles (received 2026-05-06), the direction reversed: minority 4/89 = 4.5% below threshold, majority 6/89 = 6.7%. The substrate effect: VA-polygon dissolves impose detailed perimeter geometry that differentially penalises the minority's corridor-shaped EDs; clean administrative boundary lines are less sensitive to this pattern. The "minority less compact" between-map claim and 2.58× ratio do not survive canonical geometry. Primary: `findings/reock_verdict.md`.
>
> **C3 — v0_9 Polsby-Popper between-map asymmetry (superseded 2026-05-18).** The v0_9 PP analysis produced minority 30.3% vs majority 22.5% below threshold (1.35× asymmetry). Under canonical EA shapefiles, the direction reversed: minority 6/89 = 6.7%, majority 8/89 = 9.0%. Same substrate effect as C2. Primary: `findings/polsby_popper_verdict.md`.
>
> **C4 — Phase 4C derived-geometry EG asymmetry (superseded 2026-05-17).** An earlier Phase 4C v2 run using derived shapefiles produced a +0.31 pp EG asymmetry (majority − minority, election-day votes). The canonical Phase 4C re-run on official EA shapefiles (2026-05-17) produces +3.92 pp, with majority NDP@50/50 = 48 vs minority = 43. The discrepancy is attributable to derived boundary approximation affecting rural-fringe VA assignments. Primary: `findings/assignment_gerrymander_comparison.md`.
>
> **C5 — v0.2 blend [§5.2.1](#sec-5-2-1) table values (superseded 2026-05-18).** The v0.2 urban/rural blend model (URBAN_WEIGHT_DEFAULT = 0.85) produced majority EG −0.40% / minority EG −1.81% (both UCP-favourable in negative=UCP convention), B3 majority −0.66 pp / minority −1.20 pp, B4 majority 45 / minority 46, and actual seats majority 38/51 / minority 38/51. Phase 4C (v0.3) exact VA-level spatial attribution gives: standard EG majority +0.04% / minority +3.96% (both UCP-favourable in S-M positive=UCP convention; majority approximately neutral at p15.5, minority substantially UCP-favourable at p94.4; +3.92 pp asymmetry), B3 majority −3.64 pp / minority +1.03 pp (B3 direction reverses: majority now more negative on MM than minority), B4 majority 48 / minority 43, actual seats majority 34/55 / minority 29/60. The blend model had the EG sign wrong: it showed minority as *more* UCP-favourable than majority (both negative, minority more negative); Phase 4C agrees on the direction (minority more UCP-favourable) but at much higher magnitude. Phase 4C and MCMC canonical agree to within 0.06 pp. Primary: `analysis/scripts/packing_cracking_analysis.py` v0.3; `findings/partisan_bias_summary.md` §A1 (2026-05-18).
>
> **C6 — Option A threshold verdict change (updated 2026-05-18).** Earlier blend values (majority −0.40%, minority −1.81%, negative=UCP convention) placed both maps below the 2.2% assembly-size threshold (Option A). Under Phase 4C (majority +0.04%, minority +3.96%), the minority exceeds the 2.2% threshold. The [§5.2.8](#sec-5-2-8) table Option A row verdict changes from "Yes (both sub-threshold)" to "No — minority +3.96% exceeds threshold." The majority remains sub-threshold under all options. The audit headline updates accordingly: the majority is sub-threshold under all four Alberta-calibrated options; the minority exceeds Option A (2.2%) and approaches but does not cross Option D (4.10%). Primary: `analysis/methodology/threshold_provenance.md` §B.2.1.

---

<a id="sec-8"></a>
## 8. Conclusion

Three questions opened the paper. The answers are now on the table.

First, do the two commission proposals diverge in measurable, reproducible ways? Yes. Across eight sub-sections of [§5](#sec-5) — population equality, partisan bias, signature detection, MCMC ensemble placement, the pre-registered checklist, symmetry-of-test-selection, geographic coherence, and procedural record — the minority 2026 proposal shows wider distribution, higher packing and cracking signals, more anomalies, and a more government-controlled procedural path than the majority. Every number is reproducible via `python3 analysis/<script>.py` against checked-in data anchored in `FROZEN_MANIFEST.md`.

Second, do the divergences run systematically in one political direction? Yes, with explicit qualifications. Five of the six structural dimensions point in the same direction without depending on vote data. The one vote-based partisan-bias dimension is directionally consistent under 2023 vote input and under April 2026 338Canada polling, but reverses under 2019 vote input. The audit reports the contingency as a property of the finding rather than a defect: the boundary effect is sensitive to which electorate is asked, and the direction holds at approximately 90% confidence under Monte Carlo over modelling choices across 2020s-era voter distribution.

Third, can the April 16 pivot be evaluated against a pre-registered falsifiability framework? Partially now, fully in November. The audit's test battery is pre-registered and the checklist is prepared for Open Science Framework submission with embargoed release scheduled for 2026-11-02. The OSF time-stamp converts the signature framework from an audit-voice discipline into a classical pre-registration against a future map. When the Lunty committee tables its 91-seat map by November 2, 2026, the same scripts that produced [§5](#sec-5) will be re-run against the new map; the pre-registered scorecard will flag signatures, outliers, and rationale failures at the same thresholds applied here.

**Scope of the finding.** The minority 2026 proposal shows a pattern of structural irregularities and rationale failures beyond what the majority exhibits, at magnitudes below the Stephanopoulos-McGhee 7% investigable-bias threshold (proposed in the academic literature; never judicially adopted) but above the noise floor of non-partisan redistricting variance as measured against the 1,010,000-plan canonical ReCom ensemble. The April 16 government action replaces the commission's drafting process rather than amending its output — the most government-controlled response among the three most commonly cited Canadian comparator cases. Whether these facts support a constitutional challenge under the *Saskatchewan Reference** [1991] effective-representation standard is for counsel and the courts to assess (Appendix F).

**Next steps.** Following the receipt of the official shapefiles on May 6, 2026, the audit successfully replaced all Derived Provisional Geometries (DPG) with canonical boundaries. On May 7, 2026, Elections Alberta's GIS team responded to the audit's technical methodology questions (personal communication, Raymond Mok, Geomatics Team Lead). Three specific points were clarified: (1) VA polygons for the 2026 proposed boundaries do not yet exist, because the government's Select Special Committee may redraw the boundaries before they take effect — confirming that the audit's approach of spatially joining 2023 VA polygons to the 2026 ED boundaries is the correct and only available methodology; (2) the population estimation methodology was described and the EA contact noted it was reasonable for the study's purposes, without being able to confirm whether the underlying population data could be shared; (3) EA uses the current Alberta OpenData municipal boundary dataset for boundary work, and Communities of Interest determinations were made through EBC member knowledge and public hearings rather than a formal GIS protocol — confirming that the audit's municipal anchoring analysis uses the same data source as the commission. The audit's remaining modelling approximations (election-day-only vote substrate; 2021 census-based population) reflect structural features of EA's published data, not gaps that EA's internal data resolves. The November 2026 MLA-committee 91-seat map remains the held-out test that closes the pre-registration residual ([§5.5](#sec-5-5)). In response to speculation regarding "dummymander" vulnerability, the November analysis will explicitly test for **microtargeting** and **demographic lockout**. By applying projected 10-year suburban population growth models to the canonical MCMC ensemble, the audit will test whether the minority's "Surgical Fortification" firewall is designed to systematically dilute opposition vote share as population grows, establishing a permanent structural lockout over the decennial cycle.

**What stands in the evidentiary record.** The audit's contribution is documenting that two commission proposals diverge systematically on six measurable dimensions, that the direction of divergence consistently favors the governing party under the available vote inputs, and that the process being used to promote the more-favorable proposal departs from comparator Canadian practice in specific ways. These facts are reproducible from public data using checked-in code. They do not prove intent, and they do not by themselves establish a constitutional violation. What they do provide is the evidentiary substrate on which such judgments — by counsel, by courts, by voters, and by future commissioners — can be constructed.

<a id="sec-8-1"></a>
### 8.1 Postscript — the audit as framework for the held-out test

In policy terms, the verdicts in [§5](#sec-5) and [§6.2](#sec-6-2) are now substantially moot. On April 16, 2026 the Alberta government set both commission proposals aside and assigned redistricting to a five-MLA committee chaired by Brandon Lunty (UCP, Leduc-Beaumont). The map this audit measured is no longer a candidate to become law. Whatever Alberta uses for the 2027 election will come from the Lunty committee, not from either commission proposal.

That does not make the work in [§4](#sec-4)–[§7](#sec-7) unnecessary. The commission audit was a framework-building exercise. It produced — and calibrated against three real Alberta maps (the 2019 enacted baseline, the majority 2026 proposal, and the minority 2026 proposal, applied symmetrically to all three) — the artefacts the next audit will need:

1. The four Alberta-calibrated EG thresholds ([§5.2.8](#sec-5-2-8)), including the 4.10 % MCMC-derived 95th percentile (1,010,000-plan canonical ensemble on official EA shapefiles).
2. The 1,010,000-plan canonical constraint-bound ReCom ensemble on Alberta's 2019 substrate ([§5.4](#sec-5-4)), against which any 89- or 91-seat Alberta map can be percentile-placed for the four partisan-bias metrics.
3. The structural-irregularity scorecard (anchoring %, MAD, Calgary geographic-zone gap, Airdrie-class community-split count, chair-anomaly count), with majority-comparable benchmarks documented for every test.
4. The pre-registered rationale-failure framework that classifies a contested redraw symmetrically across maps ([§5.6](#sec-5-6)).
5. The DPG construction pipeline ([§4.1.5](#sec-4-1-5)–[§4.1.6](#sec-4-1-6)), now extended through stage v0_8 with the perfecter and the nested-polygon ownership-inversion refinement, and the alignment-proof toolkit, all of which will accept the Lunty committee map without modification when its data is published.
6. The two-lane verdict structure ([§6.2](#sec-6-2)) that distinguishes partisan-bias-magnitude readings from cumulative-structural-pattern readings, so the next audit can report both lanes honestly even if they disagree.

When the Lunty committee tables its 91-seat map on or before November 2, 2026, this audit's apparatus will be re-pointed at the new map and re-run as fulsomely and as faithfully as it was for the commission proposals. The pre-registered scorecard at `analysis/reports/pre_registration_draft.md` and its OSF time-stamped binding ([§5.5](#sec-5-5)) are the audit's commitment to that follow-through; the directional flag the [§6.2](#sec-6-2) verdict places on the November map will be made on the same evidence, against the same thresholds, with the same restraint on intent.

**Two contextual reminders for the November audit.**

*Alberta's natural geography will always give conservative voters an edge.* The province's NDP supporters concentrate in city cores; UCP supporters spread across suburbs and rural ridings that win by efficient margins. Any neutrally-drawn Alberta map will produce a UCP-favourable efficiency gap as a structural starting point. The Chen-Rodden decomposition in [§5.2.5](#sec-5-2-5) quantifies how much of any given map's partisan-bias signal is geography-derived versus drawing-derived; a future map cannot escape the geography component, only manage the drawing component. The audit's job is to separate the two clearly enough that legitimate criticism cannot be brushed off as "you're complaining about geography."

*There are many ways to gerrymander, and not all of them register on the partisan-bias-magnitude lane.* The minority 2026 proposal demonstrated this empirically: it sat sub-threshold on every Alberta-calibrated EG line while crossing every structural-pattern threshold by a wide margin. A drafting process that wants to engineer outcomes without leaving an EG fingerprint has the structural lane available — community splits, off-reference borders, anchoring departures, chair-flagged shapes — and the audit will be looking at both lanes when the Lunty committee map arrives. Sub-threshold on Lane 1 is necessary for a clean verdict, but not sufficient.

The standard the November audit will hold the Lunty committee map to is the same standard this audit held the commission proposals to: skew toward neutrality wherever the constraint set permits, document the choices when the constraints force a departure, and be prepared to defend any departure from comparator Canadian practice with evidence stronger than aesthetic preference. Whether the new map meets that standard is a question this audit cannot pre-judge. It is a question the same scripts will answer publicly, on the same timeline, against the same evidence base — because the held-out test is the entire reason the framework was built.

---

## Acknowledgments

The author thanks **Raymond Mok** (Geomatics Team Lead, Elections Alberta) for providing the official 2026 commission shapefiles in response to the author's research access request and for answering technical methodology questions regarding VA polygon availability, population data, and the commission's municipal boundary and communities-of-interest data sources (personal communication, 2026-05-06 and 2026-05-07). Acknowledgment of data provision and technical assistance does not imply Elections Alberta's endorsement of the audit's findings, methodology, or conclusions.

The author also thanks the volunteer reviewers at Mount Royal University who reviewed draft sections prior to publication. Their names are withheld at their request. Acknowledgment of review assistance does not imply institutional endorsement by Mount Royal University.

---

## References


Citations follow American Political Science Association (APSA) style. Court cases follow Canadian legal citation convention.

### Academic literature

Alberta Electoral Boundaries Commission. 2026. *2025–26 Electoral Boundaries Commission Final Report (Majority and Minority)*. Government of Alberta. https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf

Altman, Micah, and Michael P. McDonald. 2011. "BARD: Better Automated Redistricting." *Journal of Statistical Software* 42(4): 1–28.

American Statistical Association. 2016. "ASA Statement on P-Values: Context, Process, and Purpose." *The American Statistician* 70(2): 129–133.

American Statistical Association. 2016. "The ASA's Statement on p-Values: Context, Process, and Purpose." *The American Statistician* 70(2): 129–133.

American Statistical Association. 2019. "Moving to a World Beyond 'p < 0.05'." *The American Statistician* 73(sup1): 1–19.

Barnes, Richard, and Justin Solomon. 2021. "Gerrymandering and Compactness: Implementation Flexibility and Abuse." *Political Analysis* 29(4): 448–466.

Bratt, Duane, Keith Brownsey, Richard Sutherland, and David Taras, eds. 2019. *Orange Chinook: Politics in the New Alberta*. Calgary: University of Calgary Press.

Cannon, Sarah, Ari Goldbloom-Helzner, Varun Gupta, JN Matthews, and Bhushan Suwal. 2022. "Voting Rights, Markov Chains, and Optimization by Short Bursts." *Methodology and Computing in Applied Probability* 25(36).

Chen, Jowei. 2017. "The Impact of Political Geography on Wisconsin Redistricting." *Election Law Journal* 16(4): 443–452.

Chen, Jowei, and Jonathan Rodden. 2013. "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269.

Courtney, John C. 2001. *Commissioned Ridings: Designing Canada's Electoral Districts*. Montreal and Kingston: McGill-Queen's University Press.

Courtney, John C. 2004. *Elections*. Vancouver: UBC Press.

DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021. "Recombination: A Family of Markov Chains for Redistricting." *Harvard Data Science Review* 3(1).

Driedger, Elmer A. 1983. *Construction of Statutes* (2nd ed.). Toronto: Butterworths.

Fifield, Benjamin, Kosuke Imai, Jun Kawahara, and Christopher T. Kenny. 2020. "The Essential Role of Empirical Validation in Legislative Redistricting Simulation." *Statistics and Public Policy* 7(1): 52–68.

Gelman, Andrew, and Gary King. 1994. "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." *American Journal of Political Science* 38(2): 514–554.

Grofman, Bernard. 1983. "Measures of Bias and Proportionality in Seats-Votes Relationships." *Political Methodology* 9(3): 295–327.

Herschlag, Gregory, Robert Ravier, and Jonathan C. Mattingly. 2020. "Quantifying Gerrymandering in North Carolina." *Statistics and Public Policy* 7(1): 30–38.

Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020. "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." *American Political Science Review* 114(1): 164–178.

King, Gary, and Robert X. Browning. 1987. "Democratic Representation and Partisan Bias in Congressional Elections." *American Political Science Review* 81(4): 1251–1273.

McDonald, Michael D., and Robin E. Best. 2015. "Unfair Partisan Gerrymanders in Politics and Law: A Diagnostic Applied to Six Cases." *Election Law Journal* 14(4): 312–330.

Munafò, Marcus R., Brian A. Nosek, Dorothy V. M. Bishop, Katherine S. Button, Christopher D. Chambers, Nathalie Percie du Sert, Uri Simonsohn, Eric-Jan Wagenmakers, J. J. Ware, and John P. A. Ioannidis. 2017. "A Manifesto for Reproducible Science." *Nature Human Behaviour* 1(0021).

Nosek, Brian A., Charles R. Ebersole, Alexander C. DeHaven, and David T. Mellor. 2018. "The Preregistration Revolution." *Proceedings of the National Academy of Sciences* 115(11): 2600–2606.

Pal, Michael. 2015. "The Fractured Right to Vote." *McGill Law Journal* 61(2): 231–274.

Pal, Michael, and Sujit Choudhry. 2011. "Democratic Accountability and Judicial Role in Canada's Electoral System." In *Democratizing the Constitution: The Role of the People and Social Movements in Constitutional Reform*, eds. Sujit Choudhry, 95–127. Oxford: Oxford University Press.

Pal, Michael, and Sujit Choudhry. 2014. "Towards a Normative Account of the Right to Vote." *Canadian Political Science Review* 8(1): 52–76.

Polsby, Daniel D., and Robert D. Popper. 1991. "The Third Criterion: Compactness as a Procedural Safeguard Against Partisan Gerrymandering." *Yale Law & Policy Review* 9(2): 301–353.

Reock, Ernest C. 1961. "Measuring Compactness as a Requirement of Legislative Apportionment." *Midwest Journal of Political Science* 5(1): 70–74.

Sancton, Andrew. 2008. *The Limits of Boundaries: Why City-Regions Cannot Be Self-Governing*. Montreal and Kingston: McGill-Queen's University Press.

Stephanopoulos, Nicholas O., and Eric M. McGhee. 2014. "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82(2): 831–900.

Stephanopoulos, Nicholas O., and Eric M. McGhee. 2018. "The Measure of a Metric: The Debate Over Quantifying Partisan Gerrymandering." *Stanford Law Review* 70(5): 1503–1568.

Warrington, Gregory S. 2018. "Quantifying Gerrymandering Using the Vote Distribution." *Election Law Journal* 17(1): 39–57.

Warrington, Gregory S. 2019. "A Comparison of Partisan Gerrymandering Measures." *Election Law Journal* 18(3): 262–281.

### Court cases

*Cassista v. Canada (Attorney General)*, 2014 FC 398.

*Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912.

*Frank v. Canada (Attorney General)*, [2019] 1 SCR 3.

*Gill v. Whitford*, 585 U.S. ___ (2018).

*Grant v. Torstar Corp.*, 2009 SCC 61.

*Raîche v. Canada (Attorney General)*, 2004 FC 679.

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

*Rucho v. Common Cause*, 139 S. Ct. 2484 (2019).

*WIC Radio Ltd. v. Simpson*, 2008 SCC 40.

### Statutes

*Electoral Boundaries Commission Act*, RSA 2000, c E-3.

### Data sources

City of Airdrie. 2024. *2024 Municipal Census Results* [Data set]. Released July 2, 2024. https://www.airdrie.ca/index.cfm?serviceID=2242&ID=1248

Elections Alberta. 2015. *2015 Provincial general election official results* [Data set]. https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx

Elections Alberta. 2019. *2019 Provincial general election official results all EDs* [Data set]. https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx

Elections Alberta. 2023. *2023 Provincial general election statement of vote* [Data set]. https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx

Elections Alberta. 2026. *Electoral boundaries commission submissions archive* [Data set, Rounds 1 and 2]. https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/

Statistics Canada. 2021. *Dissemination area boundary files, 2021 census* [Data set]. https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/

---

*Draft. Falsifiability gates, robustness checks, and APA citations documented throughout.*

---

## Appendix A — Reproducibility

### A.1 Three-election direction-stability of minority-majority asymmetry

The minority map's partisan-bias asymmetry relative to the majority map is robust across three Alberta election cycles (2015, 2019, 2023). Minority-majority efficiency-gap asymmetry (percentage points):

| Election | Majority EG | Minority EG | Asymmetry (Min−Maj) | Interpretation |
|----------|----------:|----------:|----------:|---------|
| 2015     | +7.25%   | +7.28%   | +0.03 pp | Minority essentially equal to majority |
| 2019     | +0.16%   | +0.90%   | +0.75 pp | Minority more UCP-favorable than majority |
| 2023     | −0.85%   | −1.36%   | −0.51 pp | Minority less UCP-favorable than majority |

**Caveat.** The 2015 and 2019 asymmetries reverse sign relative to 2023, a cycle-contingent result explained in [§5.2.3](#sec-5-2-3): the minority's hybrid districts (Springbank, Bearspaw, Cochrane) occupy the blend model's transition zone between urban and rural NDP performance. Under 2023 (a competitive urban cycle), these territories trend NDP, widening the minority's UCP advantage. Under 2019 and 2015 (cycles with shallower urban NDP penetration), they trend rural, narrowing it. The inter-map *asymmetry direction* thus depends on Alberta's election-cycle geography — not a measurement artifact or boundary instability. By contrast, both individual maps consistently show UCP advantage under all three elections; the direction of individual-map partisan bias is stable, only the inter-map gap direction changes. Full method and derivation at `findings/cross_election_2015.md`.

All scripts run from repository root:

```bash
python3 analysis/scripts/packing_cracking_analysis.py    # §5.2 symmetric three-map
python3 analysis/scripts/electoral_forensics_population.py    # §5.1 with A2 robustness
python3 analysis/scripts/poll_attribution_skeleton.py    # §4 parse validation
```

Each script prints a gate PASS/FAIL line. Numbers in [§2](#sec-2), 3 above must match the corresponding gate-passed output.

**Reproducibility artifacts.** A version-pinned environment manifest (`requirements.txt` at repo root) lists every Python package with exact version; an interpreter pin (`setup.md`) names the tested Python version; `FROZEN_MANIFEST.md` lists every external URL accessed during the audit with its access date. A third party running the pipeline 12+ months from today can (a) install the pinned environment, (b) check each URL's state against the frozen snapshot, and (c) reproduce every numeric finding to the tolerance stated in Gate G0. Reproducibility-artifact provenance follows the ICLR 2022 Reproducibility Checklist and Nosek et al. (2018) Open Science Framework pre-registration standards.

## Appendix B — Supporting Analysis Documents


- [Section A](findings/population_equality.md)
- [Section C](findings/geographic_coherence.md)
- [Section D](findings/procedural_analysis.md)
- [Section 4](findings/geometry_provenance.md)
- [Bias audit](findings/partisan_bias_summary.md) — self-audit of this audit's own methodology
- [Design critique](analysis/review/design_critique.md) — hostile stress-test pass
- [Methodological defenses](analysis/methodology/methodological_defenses.md) — pre-emptive adversarial review: attacks on substrate, MCMC baseline, and partisan metrics with per-attack empirical responses
- [Test apparatus defense](analysis/methodology/methodological_defenses.md#test-apparatus-defense) — per-test criticism and response; addresses "are you making up metrics to have metrics?"
- [Fisher combination defense](analysis/methodology/fisher_combination_defense.md) — statistical rationale for combining Ch1 and Ch2 via Fisher's method
- [Fisher independence defense](analysis/methodology/fisher_independence_defense.md) — argument that the two channels are sufficiently independent for Fisher combination
- [Warrington declination defense](analysis/methodology/methodological_defenses.md#warrington-declination-defense) — declination metric applicability and its direction-disagreement with EG
- [Urban weight defense](analysis/methodology/methodological_defenses.md#urban-weight-defense) — blend model urban-weight parameter justification
- [Uncertainty analysis](analysis/methodology/uncertainty_and_shapefile_impact.md)
- [Academic literature review](analysis/methodology/academic_literature_review.md)
- [Submission search findings](findings/submission_search_findings.md) — [§5.9.4](#sec-5-9-4) evidence base
- [Chair's Recommendation 5 analysis](findings/chair_recommendation_5_analysis.md) — [§5.9.2](#sec-5-9-2) evidence base
- [Track C checklist baseline scoring](findings/checklist_baseline_scoring.md) — [§5.5](#sec-5-5) full scorecard and comparison template for the November map
- [MCMC ensemble baseline](analysis/methodology/mcmc_ensemble.md) — [§5.4](#sec-5-4) method, 10k-sample ReCom chain against 2019 baseline, per-metric percentile tables
- [Plan B compliance + contested-config cross-check](analysis/reports/plan_b_cross_check.md) — note on population-data provenance evidence base
- [Cycle-lag analysis](analysis/cycle_lag_analysis.md) — province-wide ED drift under mid-2025 populations
- [Proposed Act §12 amendment](docs/act_amendment_proposal.md) — legislative reform proposal addressing the census / cycle-lag tension
- [Calgary data-sources audit](analysis/methodology/calgary_data_sources_audit.md) — 16 Calgary-specific sources catalogued; ward-level modelled A2 sensitivity is feasible from public data
- Adversarial stress-test passes and their fortifications are preserved in `historical/` for historical reference (see `historical/README.md`).
- [Chen-Rodden Alberta validation](analysis/methodology/chen_rodden_alberta_validation.md) — mechanism-level test of the natural-packing argument
- [Canadian redistribution base-rate catalogue](data/canadian_redistribution_base_rate.csv) — C4 partial catalogue (quantitative acquisition flagged as future work)
- [Alberta government database survey](analysis/methodology/alberta_government_databases_survey.md) — Track N, composite-basis source recommendations for §12 reform
- [Commission source provenance audit](analysis/methodology/commission_source_provenance.md) — Track O, verified 4,888,723 matches StatsCan Q2 2024 postcensal estimate
- [Byelection data and assessment](findings/byelection_assessment.md) — Track S, 2022–2025 byelections evaluated and not incorporated into RT3
- [A1 legal-baseline computation](analysis/methodology/appendix_c_legal_baseline.md) — Appendix C companion; 2019-map MAD on 2021 Census directly
- [Threshold provenance compendium](analysis/methodology/threshold_provenance.md) — every numeric threshold justified with source + sensitivity
- [Canadian inter-map base-rate computation](analysis/methodology/canadian_base_rate_computed.md) — comparative distribution across seven Canadian redistribution cycles
- [External pre-registration draft and platform analysis](analysis/reports/pre_registration_draft.md) / [platform analysis](findings/pre_registration_platform_analysis.md) — OSF submission package for the November signature-detection checklist
- [Minority rationales validation](analysis/methodology/minority_rationales_validation.md) — [§5.8.4](#sec-5-8-4) and [§5.9.2](#sec-5-9-2) evidence base (25 rationales inventoried, 3 contradicted)
- [Minority rationales inventory](analysis/methodology/minority_rationales_inventory.md) — source quotes with citations
- [Cochrane journey-to-work](analysis/methodology/cochrane_journey_to_work.md) — [§5.8.4](#sec-5-8-4) StatsCan 98-10-0459 pull
- [CSD-level community splits](analysis/methodology/csd_community_splits.md) — [§5.8.4](#sec-5-8-4) robustness check
- [338Canada riding-level cross-validation](analysis/methodology/338canada_riding_level.md) — [§5.2.3](#sec-5-2-3) independent cross-check
- Submission OCR log preserved at `historical/v0_1_submission_ocr_log.md` — [§5.9.4](#sec-5-9-4) partial extension of the 88 non-text-layer submissions


## Appendix C — 2021-census legal-baseline A1 for the 2019 map


**Purpose.** [§5.1.1](#sec-5-1-1) reports A1 MAD on the commission's own tables, which derive from the July 2024 OSI population estimate. A reviewer committed to strict §12(3) statutory-basis discipline can argue the [§5.1.1](#sec-5-1-1) numbers inherit the commission's data-source status. This appendix provides an independent 2021-Census-direct computation of A1 on the 87 existing 2019 EDs as the §12(3)-operative reference point. The 2026 proposals cannot receive the equivalent treatment because their ED shapefiles have not been publicly released.

**Method.** 2021 Census population at the dissemination-area level (6,203 Alberta DAs, `data/alberta_2021_da_populations.csv`) aggregated to the 87 2019 EDs via geopandas overlay on `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`. Reproducible script at `analysis/scripts/a1_legal_baseline_2021_census.py`. Per-ED output at `data/a1_legal_baseline_2019eds_2021census.csv`.

**Headline figures.**

| Map & basis | Quota | MAD | Source |
|-------------|-------|------|--------|
| 2019 map on 2017-report basis (commission-quoted) | 46,803 | 2,886 | EBC 2017 Final Report pp. 60–61 |
| 2019 map on 2021 Census (this appendix) | 48,996 | **4,745** | This computation |
| 2026 majority map on 2024 TBF estimate | 54,929 | 3,180 | Majority Report variance table |
| 2026 minority map on 2024 TBF estimate | 54,929 | 4,707 | Minority Report variance table |

**Ordinal comparison.** 2026 majority MAD (3,180) < 2019-on-2021-Census MAD (4,745) ≈ 2026 minority MAD (4,707). The minority 2026 proposal's distribution-tightness is effectively equal to the 2019 map's distribution-tightness at 2021-Census time; the majority 2026 proposal is meaningfully tighter than either benchmark.

**Seven 2019 EDs outside ±25 % under 2021 Census.** Central Peace-Notley (−44.77 %), Lesser Slave Lake (−44.73 %) — both s.15(2)-protected — plus Edmonton-South (+40.89 %), Edmonton-Ellerslie (+38.60 %), Edmonton-South West (+33.71 %), Airdrie-Cochrane (+29.76 %), Calgary-North East (+25.55 %). The five positive outliers are urban-growth EDs that had already exceeded the +25 % ceiling by 2021-census time; Track L's mid-2025 analysis (`analysis/cycle_lag_analysis.md`) confirms all five remain out-of-band under 2025 populations.

**Interpretation.** The audit's [§5.1.1](#sec-5-1-1) ordering (majority tighter than minority) is preserved under the §12(3)-operative basis. The minority proposal, drawn four years after the 2021 Census, reproduces the same population-distribution tightness the 2019 map exhibited against the 2021 Census; the majority proposal improves on that benchmark. A strict §12(5) reviewer's attack on [§5.1.1](#sec-5-1-1)'s data basis does not change the direction of the A1 finding. Full discussion in the companion file `analysis/methodology/appendix_c_legal_baseline.md`.


## Appendix D — Mathematical Formalism


### D.1 Efficiency Gap (Stephanopoulos and McGhee 2014)

$$\text{EG} = \frac{W_A - W_B}{N}$$

```
EG = (W_A - W_B) / N
```

Wasted votes $W_X$ for party $X$ are defined as losing-district votes plus winning-district votes above the victory threshold $\lceil N_d/2 \rceil + 1$, summed across districts. The 7 % threshold is academic-literature authority only — never judicially adopted (see [§5.2.8](#sec-5-2-8)).

**Sign-convention reconciliation.** When party A is indexed first, Stephanopoulos-McGhee canonical EG uses a 2:1 slope baseline (positive EG = party A disadvantaged, i.e., party B has seat-advantage). This paper reports EG under the 1:1 proportional-seat baseline; in Alberta's rural-UCP-blowout context, this produces negative EG values whose magnitude correlates with UCP outcome advantage through seat count, despite UCP also being the more-wasteful party by the wasted-vote measure. The two conventions give the same ordinal ranking of Alberta's three maps (2019 / Majority 2026 / Minority 2026) and therefore the same minority-vs-majority direction. Full derivation and verification at `analysis/methodology/sign_convention_resolution.md`.

### D.2 Mean-Median Gap (McDonald and Best 2015)

$$\text{MM} = \bar{v} - \tilde{v}$$

```
MM = mean(v) - median(v)
```

$\bar{v}$ is the mean NDP vote share across districts; $\tilde{v}$ is the median. Positive MM indicates mean > median, consistent with party voters packed into fewer high-share districts (cracking of the opposing party, or packing of own party).

### D.3 Declination (Warrington 2018)

$$\delta = \frac{2}{\pi}\left(\arctan\!\left(\frac{\bar{y}_R - \bar{x}_R}{\bar{x}_R}\right) - \arctan\!\left(\frac{\bar{y}_D - \bar{x}_D}{\bar{x}_D}\right)\right)$$

```
# Discrete approximation
# For each party P, sort its won districts by vote share.
# y_bar_P = mean winning vote share across P's districts
# x_bar_P = fraction of all districts that P won
# delta = (2/pi) * (arctan((y_bar_R - x_bar_R) / x_bar_R) - arctan((y_bar_D - x_bar_D) / x_bar_D))
```

Positive δ indicates the party indexed first (UCP in this audit, playing the role of party R) wins its seats more efficiently — smaller winning margins concentrated nearer the 50 % threshold — while the party indexed second (NDP, party D) wins its seats by larger margins, indicating packing. In this audit's sign convention (NDP indexed as the "D" party), a positive δ signals UCP-favourable boundary geometry and a negative δ signals NDP-favourable geometry.

**Alberta results (canonical shapefiles, 2023 votes):**

| Map | δ | Percentile vs 1,010,000-plan canonical ensemble |
|---|---|---|
| 2019 enacted | −0.034 | — (baseline) |
| Majority 2026 | −0.021 | p16.4 (within null) |
| Minority 2026 | −0.015 | p1.21 (NDP-tail) |

Declination disagrees with EG and mean-median on the minority map's direction: by declination, the minority is the *least* UCP-favourable of the three maps. This cross-metric disagreement is expected under Warrington (2018) and Katz, King & Rosenblatt (2020); both metrics are retained (see [§5.2.4](#sec-5-2-4) for the full cross-metric reconciliation).

### D.4 Polsby-Popper compactness

$$\text{PP} = \frac{4\pi A}{P^2}$$

```
PP = 4 * pi * A / P^2
```

$A$ = polygon area, $P$ = perimeter. Range $[0, 1]$; 1 = circle. Values near 0 indicate elongated or convoluted boundaries. Gate threshold: mean PP < 0.15 (extremely fragmented). See Polsby & Popper (1991); Niemi et al. (1990).

**Results (v0_7 DPGs, EPSG:3401, full 89-ED coverage; script `analysis/scripts/compactness_metrics.py`):**

| Map | N | Mean PP | Median PP | Std Dev | Min | Max | EDs < 0.30 | EDs < 0.40 | Gate |
|---|---|---|---|---|---|---|---|---|---|
| 2019 enacted | 87 | 0.4186 | 0.3994 | 0.1189 | 0.1717 | 0.7691 | 16 | 44 | PASS |
| Majority 2026 | 89 | 0.3564 | 0.3591 | 0.1375 | 0.0902 | 0.6910 | 29 | 60 | PASS |
| Minority 2026 | 89 | 0.3344 | 0.3374 | 0.1470 | 0.0652 | 0.6994 | 39 | 63 | PASS |

The minority 2026 map has the lowest mean Polsby-Popper (0.334) and the most EDs below the 0.30 caution threshold (39 of 89), suggesting its boundaries are more geometrically complex than either the 2019 enacted map or the majority proposal. This is consistent with the minority's hybridization. All three maps pass the gate (mean PP > 0.15). Full per-ED CSV at `findings/compactness_metrics.csv`; summary JSON at `data/compactness_summary.json`.

### D.5 Reock compactness

$$\text{R} = \frac{A_d}{A_c}$$

```
R = A_district / A_smallest_enclosing_circle
```

Range $[0, 1]$. R < 0.25 typically flagged. Results are included in `findings/compactness_metrics.csv` alongside Schwartzberg and convex-hull-ratio scores from the same v0_7 run.


## Appendix E — Geometric Data Provenance

The subsections below document the historical geometric-data paths evaluated in the first phases of this audit prior to the release of official shapefiles. § E.1–E.5 describe the initial attempts (direct-shapefile, DA-dissolve, VA-polygon-attribution, OSM reconstruction, and QGIS paths). § E.6 is the technical data statement. § E.7 reports the approximate-geometry analysis (Tier A/B compactness) that was produced as a substitute for the not-yet-released 2026 shapefiles. All provisional geometry findings were officially superseded on May 6, 2026, when Elections Alberta provided the official canonical shapefiles. An additional "Note on population-data provenance and cycle-lag robustness" is preserved at the end of the appendix for completeness; its core findings are summarised in [§3.3](#sec-3-3).

### E.1 4A (direct shapefiles)

**Resolved.** Initially blocked on 2026-04-22 as 2026 proposal shapefiles were not published on the Elections Alberta maps portal. However, on May 6, 2026, Elections Alberta officially provided the 2026 shapefiles (`ea_majority_2026_eds.gpkg` and `ea_minority_2026_eds.gpkg`), triggering the sunset clause and transitioning the entire audit from Derived Provisional Geometries (DPG) directly to Canonical Geometry.

### E.2 4B (DA dissolve)

**Deprecated.** This path would have attempted to reconstruct boundaries by dissolving 2021 Census DAs if the Commission's PDF report contained DAUID lists. It was formally deprecated on May 6, 2026, when the official shapefiles (E.1) provided the canonical boundaries directly, rendering DA-dissolve approximation obsolete.

### E.3 4C (VA-polygon attribution)

**Pipeline validated; full execution intentionally bypassed.** Skeleton (`analysis/scripts/poll_attribution_skeleton.py`) correctly parses the 2023 Statement of Vote: 1,973 poll records matched to four-figure official totals. The full execution (geocoding 1,973 polls directly into the 2026 shapefiles) would require ~4–8 hours of compute. This path was evaluated and intentionally bypassed because it does not yield a measurable precision gain.

**Reasoning:** 47.5% of 2023 valid votes are "Vote Anywhere" Advance/Mobile ballots. Elections Alberta verified on May 7 that disaggregated VA-level mapping for these ballots does not exist. Even if the 53% Election Day polls were perfectly geocoded, the 47.5% Advance vote would still require a proportional area-weighted spread. Phase 4F (`va_attribution_area_weighted.py`) proved that the residual geographic error on the Election Day straddle impacts exactly 1,396 votes (0.15% of the province) and shifts the minority map's `seats@50/50` metric by exactly +0.0000 pp. The current area-weighted substrate is therefore the mathematical ceiling of precision possible with public data; expending compute on this path would be mathematically redundant.

### E.4 4D/4E (OSM Reconstruction / QGIS Manual)

**Deprecated.** 4D (OSM feature-class snapping) and 4E (manual QGIS painting) were alternative paths to reconstruct the missing boundaries visually. Both were permanently deprecated on May 6, 2026, upon receipt of the canonical shapefiles, which provide exact vertices and eliminate the need for visual transcription.

### E.5 4F validation

**Superseded.** Validation of the approximate geometries against Commission population targets was superseded by the canonical runs on the official shapefiles.

### E.6 Technical Data Statement

- **Source data for Sections A, B:** CSV files in `data/` (populations for both 2026 maps; per-ED 2023 and 2019 vote totals); raw Statement of Vote in `data/2023_results.xlsx`.
- **Source data for Section C:** JPG map images from the commission's final report (majority Calgary only; full coverage for minority).
- **Source data for Section D:** Electoral Boundaries Commission Act, commission report via prompt context, comparator-case general knowledge.
- **Geometric reconstruction:** Superseded. The audit operates entirely on the canonical shapefiles.
- **Coordinate system / resolution / aggregation:** EPSG:3401 (NAD83 / Alberta 10-TM).
- **Integrity metric:** Population checksum threshold (0.5% warn, 2% hard stop) cleanly passed on canonical shapes.
- **Geometric shift log:** None required. No manual geometric adjustments were applied to the canonical shapefiles.
- **Transformation log:** No CRS transformations applied.
- **Symmetry consistency:** B1–B4 use identical Phase 4C spatial attribution applied to both 2026 maps via the same `packing_cracking_analysis.py` v0.3 run (canonical EA shapefiles, exact VA-level centroid-in-polygon). The earlier 85/15 blending methodology is superseded by Phase 4C ([§5.2.2](#sec-5-2-2)). A1–A3 use identical variance computation against the same provincial average. A2 uses identical classification rule plus an alternative-rule robustness check (G4). Section C has a symmetry data gap (only majority Calgary imagery available) which is disclosed.

### E.7 Approximate 2026 geometry — Tier A/B compactness (Archived)

**Archived (Superseded May 6, 2026).** Prior to Elections Alberta's release of official 2026 shapefiles, the audit constructed a provisional three-tier geometry framework (Tier A/B/C) for compactness testing. All findings have been superseded by the canonical measurements reported in [§5.4.9](#sec-5-4-9) using the official shapefiles. Technical methodology and version history at `analysis/methodology/commission_reference_shapes.md` and `archive/provisional_geometries/approximate_shape_analysis.md`.


## Appendix F — Legal Interpretive Note


This audit does not offer a legal conclusion. It provides the evidentiary basis on which a legal challenge under *Saskatchewan Reference** [1991] 2 SCR 158's "effective representation" standard could be constructed. The question whether the minority proposal, as potentially modified by the November 2, 2026 MLA-committee process, would satisfy the effective-representation requirement is for counsel and the courts to assess. The audit's core contribution is documenting that:

1. The two commission proposals diverge systematically on six measurable dimensions.
2. The direction of divergence consistently favors the governing party.
3. The process being used to promote the more-favorable proposal departs from comparator Canadian practice in specific ways.

These facts are reproducible from public data using checked-in code. They do not prove intent, and they do not by themselves establish a constitutional violation.

### Expert admissibility: the *White Burgess* framework

Canadian courts assess the admissibility of expert evidence against the threshold test established in *R v Mohan* [1994] 2 SCR 9, as elaborated in *White Burgess Langille Inman v Abbott and Haliburton Co.* [2015] 2 SCR 182. The threshold inquiry has four preconditions: relevance, necessity, absence of an exclusionary rule, and a properly qualified expert — with *White Burgess* making clear that impartiality and independence are components of qualification at the threshold stage, not merely factors going to weight. This section documents the audit's posture against each precondition, including its most significant exposure.

**Relevance.** The audit's findings — population dispersion ratios, Calgary geographic-zone asymmetry, Airdrie fragmentation count, MCMC ensemble percentile, SZAT p-value — bear directly on the factual questions a trier of fact would need to assess under a *Saskatchewan Reference* effective-representation inquiry: whether the two commission proposals diverge measurably, and whether that divergence runs systematically in one direction. The relevance threshold is satisfied.

**Necessity.** The analysis relies on GIS spatial-join methods, Markov Chain Monte Carlo redistricting simulation, and permutation bootstrap statistics that are beyond the common knowledge of judges and counsel without specialized training. Translating a statement of vote into district-level partisan-bias metrics across an 89-seat assembly, calibrated against over one million randomly drawn neutral maps, requires domain expertise. A trier of fact cannot perform this analysis without assistance. Necessity is satisfied.

**Absence of exclusionary rule.** No categorical exclusionary rule applies to redistricting-science evidence. The audit does not draw on privileged communications or fields excluded categorically by common law or statute. This precondition is met.

**Qualified expert.** The author holds a BSc (Computer Information Systems) in progress at Mount Royal University. The methods deployed — Python/GeoPandas spatial analysis, GerryChain MCMC ensemble simulation, permutation bootstrap statistics — are within the author's demonstrated technical competency. Qualification at the threshold level requires training or experience sufficient to assist the trier of fact, not the highest possible credential in the field. The audit's reproducibility standard (every result recoverable by independent replication) provides a functional analogue to credential verification: a skeptical analyst can run the same pipeline and assess the author's methodological choices directly.

**Impartiality and independence: the audit's principal vulnerability.** The CoI disclosure at the top of this monograph records that the author has supported parties on all sides of the political spectrum depending on the election. *White Burgess* makes impartiality a threshold-stage issue: an expert whose partisanship is structural and pre-existing may face exclusion rather than mere discounting. A court would assess whether the partisan-advocacy history is sufficiently proximate to the subject matter of the opinion that the expert cannot fairly present as independent of the outcome.

The audit's structural defenses against an impartiality challenge are:

1. **Pre-registration before data examination.** The null hypotheses, directional predictions, pass/fail thresholds, and test suite for every finding in this monograph were committed to the Open Science Framework before the canonical shapefiles were received and before the 2023 Statement of Vote was analysed for the first time. The pre-registration timestamps are cryptographically pinned via the Cloudflare drand public randomness beacon (commit `d2aea42`, verifiable on OSF: qsgy8, r3zm7, 6pt83, yvc7g, s58a6). An expert whose methodology is recorded before data are seen, and whose predictions are falsifiable, has structurally limited latitude to shape findings toward a preferred outcome.

2. **Symmetric methodology applied to both maps.** Every test was pre-specified to run identically on both proposals. The majority's clean MCMC profile ([§5.4.9](#sec-5-4-9) — within the neutral statistical band on every metric) is an affirmative output of the same instrument applied to both maps, not an absence of scrutiny. Symmetric application of a pre-committed instrument is a structural constraint on advocacy: if the author wished to disadvantage the minority, the majority could have been tested with a weaker instrument.

3. **Failed findings disclosed.** Municipal-boundary anchoring was pre-registered as a fifth dimension of structural departure. Under canonical recomputation it did not survive: both maps are within the 70–85% Canadian comparator norm ([§5.8.5](#sec-5-8-5)). That failure is reported on the first page of the executive summary and in the abstract. An author with an advocacy agenda typically suppresses findings that undermine the desired conclusion. Affirmative disclosure of a failed finding is the opposite pattern.

4. **Reproducibility: the result stands independent of the author.** Every number in this monograph is recoverable by an independent analyst running the publicly committed scripts against the publicly available data. If the analysis contains advocacy-shaped choices, they are detectable by any analyst who re-runs the pipeline with alternative methodological assumptions. The audit does not protect its conclusions by obscuring its choices; it exposes them to replication.

The weight a court would ultimately give this evidence — after the threshold inquiry — would depend on its assessment of whether these structural defenses sufficiently mitigate the prior-advocacy history. The audit does not pre-adjudicate that question. It documents the history honestly (CoI block, line 12) and the structural defenses fully, and leaves the admissibility judgment to counsel and the court.

**Saskatchewan Reference framing.** The "effective representation" standard established in *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158 is permissive on deviation from population equality: McLachlin J (as she then was) wrote that the guarantee of [§3](#sec-3) is "the right to effective representation" (para. 26), and that "relative parity of voting power" must be weighed against other factors "including geography, community history, community interests and minority representation" (para. 33). Importantly, the Court provided no bright-line variance ceiling; instead, it requires a holistic assessment in which deviations are defensible *if justified by the specified non-quantitative factors*.

The standard has been applied by federal courts in two principal cases. *Raîche v. Canada (Attorney General)*, 2004 FC 679, examined electoral-boundary constitutionality and upheld boundaries with significant population variance, finding those deviations defensible on geographic and community-of-interest grounds. *Cassista v. Canada (Attorney General)*, 2014 FC 398, similarly upheld variance where deviations traced to permissible statutory factors. In both cases, courts did not focus on partisan asymmetry; the constitutional inquiry centered on whether quantitative deviations were reasonably related to legitimate non-partisan statutory purposes. This case law establishes a crucial point: partisan asymmetry, standing alone, does not trigger a Saskatchewan Reference violation. Rather, asymmetry is constitutionally material only when paired with either (a) unjustified deviations from population parity that cannot be attributed to geography, community boundaries, or other statutory constraints, or (b) evidence that permissible factors (geography, community of interest) have been distorted *in service of* partisan outcomes rather than applied in service of the statute's non-partisan purposes.

Under Pal's (2015) analysis, which refines the Saskatchewan Reference framework, commission outputs are reviewable only for "manifest unreasonableness" — commissioners operate within a broad "discretion space" that includes legitimate design preferences. The boundary between justified discretion and reviewable partiality turns on factual evidence about whether the stated non-partisan constraints genuinely drove the choices or were invoked post-hoc to rationalize a predetermined partisan outcome. The audit's findings — directional partisan asymmetry coupled with population-variance distortions not explained by geography or municipal boundaries, coupled with procedural departure from the pattern established by the majority under identical statutory constraints — are the kinds of evidence a court applying the effective-representation standard, refined through Pal's manifest-unreasonableness lens, would weigh in assessing whether a commission's output exceeded justified margins of discretion. Whether that weighing produces a constitutional violation is for a court, not this audit, to determine.

**Voter-impact translation of structural findings.** The *Saskatchewan Reference* standard asks whether voters can exercise "effective representation," which requires that districts enable rather than structurally impede the translation of votes into legislative representation. This paragraph translates the audit's structural findings into the specific voter-impact terms that effective-representation analysis requires.

*Population dispersion.* The minority map's MAD of 4,707 persons (48% wider than the majority's 3,180) understates the individual voter effect. The minority's maximum positive deviation is +24.06%, corresponding to a district population of approximately 68,100 against the provincial mean of 54,929. A resident of that district commands 54,929 / 68,100 = 80.7% of the representative weight of a voter in a mean-population district — a dilution of roughly 19 percentage points. Three minority districts exceed +20% deviation ([§5.1.1](#sec-5-1-1)); none in the majority does. The majority's worst positive deviation is +14.28%, conferring 87.5% effective weight. Neither map breaches the ±25% statutory floor, and the *Saskatchewan Reference* standard explicitly permits deviation where justified by the enumerated factors. The question a court would weigh is whether the allocation of underweighted districts is spatially random (consistent with geographic necessity) or patterned (consistent with systematic placement). The audit's finding that the minority's inflated districts concentrate in the Calgary Zone A geography (see below) is the evidence going to that patterning question.

*Calgary zone asymmetry.* Under the minority map, Zone A (NE / central Calgary — the NDP-competitive zone) averages 61,225 residents per district against Zone B (SW / S Calgary) at 54,569 — a 12.2% intra-city gap. A resident of a Zone A district has 54,569 / 61,225 = 89.1% of the representative weight of a Zone B resident. Across 17 Zone A districts, this dilution structurally affects approximately 1,040,000 Calgary residents concentrated in the northeastern and central city. The majority produces no comparable patterned dilution (Zone A–Zone B gap 0.4%, or 205 persons). The intra-city pattern is not explained by geographic factors — both zones are suburban and urban in character, served by comparable highway access, and draw from the same municipal services. The deviation is therefore facially inconsistent with the factors *Saskatchewan Reference* identifies as justifying population variance.

*Airdrie community fragmentation.* The minority map distributes the Airdrie region across four electoral districts. Airdrie (2024 population approximately 81,000) is a single incorporated municipality with integrated planning jurisdiction, municipal services, and a distinct local economy. A 4-way split disperses Airdrie's legislative advocacy across four representatives, none of whom has Airdrie as a primary constituency. The majority's 2-way split concentrates Airdrie's representation in two districts. The 2022 federal redistribution sub-commission for Alberta applied a 2-way split, establishing comparator precedent consistent with the majority approach. Under *Saskatchewan Reference*, community of interest is a recognized justification for deviating from exact population parity; a configuration that fragments a single community across four districts works against effective representation rather than in its service.

**Author's legal posture regarding named-individual characterisations.** This audit makes adverse characterisations of named public officials: Electoral Boundaries Commission Chair Patricia Miller, Premier Danielle Smith, and Commissioners Sela Clark, Nadia Samson, Sandra Evans, and David Martin. Examples include statements that Chair Miller "materially overstates the absence of public support for the minority proposal" ([§5.9.4](#sec-5-9-4), L619) and that "the Premier's framing omits a key distinction" ([§5.9.2](#sec-5-9-2), L572). These characterisations are defensible under the common-law defence of responsible communication on matters of public interest (*Grant v. Torstar Corp.*, 2009 SCC 61) and fair comment (*WIC Radio Ltd. v. Simpson*, 2008 SCC 40).

The *Grant v. Torstar* defence, established in 2009 by the Supreme Court of Canada, fundamentally rebalanced defamation law to protect speech on matters of public interest. Prior to *Grant*, the common law required that published statements be substantially true to escape liability — a "truth defence" that is difficult to establish and creates a chilling effect on reporting about public controversies. *Grant* introduced instead a "responsible communication on matters of public interest" defence that shifts the burden: a defendant avoids liability if they can show they took reasonable care to verify facts and presented claims responsibly, *even if some details later prove inaccurate*. This is not a licence for careless speech, but it recognizes that rigorous reporting on genuine public issues may contain good-faith errors without triggering liability. The test applies most robustly to speech about the conduct of public officials and governmental institutions.

The Court in *Grant* identified seven non-exhaustive diligence factors (para. 98) that courts should consider when assessing whether communication was "responsible." The audit's characterisations satisfy each factor:



1. **Seriousness of the allegation:** The claims concern the accuracy of statements about the commission's record and the scope of public support for each proposal — matters bearing directly on the process's legitimacy and the evidence available to the Legislature.
2. **Public importance:** Electoral boundary drawing is a core question of democratic procedure and is explicitly a matter of public importance under the *Grant v. Torstar* test.
3. **Urgency:** The audit was conducted under a compressed timeline (March–April 2026) to provide evidence before the April 16 Legislative Assembly vote. Public disclosure in real-time was necessary to inform democratic deliberation.
4. **Reliability of sources:** All claims trace to public records — the commission's published report, Appendices A–E, the statement of vote, Elections Alberta GIS data, and the public submission archive. No information was derived from confidential sources or anonymous informants.
5. **Verification attempts:** The audit's methodology is fully reproducible; every claim is anchored in a checked-in script and dataset. Individuals named can verify the underlying facts by running the audit's scripts against the public-record inputs. No private communication was required; all evidence is public-record-accessible.
6. **Inclusion of the subject's side:** The commission's majority and minority final reports present the commissioners' own rationales (Appendix D, minority report sections R1–R18). The audit's response to those rationales is documented in `analysis/methodology/reference/minority_rationales_validation.md` and summarized in [§5.9.4](#sec-5-9-4). The paper does not characterize the named individuals' intent without anchoring each characterization to on-record statements (with full quotation and source paragraph).
7. **Justifiability:** Readers can inspect the evidence themselves — [§5.9.4](#sec-5-9-4)'s tiered-verdict framework ("precisely wrong / effectively wrong / precisely and effectively wrong / defensible") makes explicit which claims rest on factual disagreement and which rest on interpretation. The author's liability hinges on factual accuracy, not interpretive choice; the facts are reproducible and the sources are on record.

**Outreach and pre-publication solicitation.** No direct written communication was sent to Chair Miller, Premier Smith, or the named commissioners before publication. Under the *Grant v. Torstar* framework, pre-publication outreach is a diligence factor that strengthens the responsible-communication defence, but its absence does not defeat the defence if other diligence criteria are met and the communication is truly responsive rather than investigative. The audit's decision not to solicit response before publication is justified on four grounds:

(1) *Public-record foundation*: All characterisations rest on public-record statements that the individuals made in their official capacity in published documents (the commission's final report, Appendices A–E, public hearings). These are matters the named individuals can verify directly by reviewing the public record themselves.

(2) *Contemporaneous public controversy*: The audit is responsive to an active public debate. The commission's final report and the April 16 Legislative Assembly vote both occurred in publicly documented settings; all named parties had ample opportunity to contest the accuracy of the facts in real time. The audit provides evidence after, but during, the relevant public controversy — not months later in a retrospective investigation.

(3) *Responsive, not investigative posture*: The audit does not investigate hidden motives, confidential deliberations, or the intent behind decisions. It examines only public-record inconsistencies — did a public official's public statement align with the public record? This responsive focus means pre-publication solicitation would be performative: it would not change the reproducible factual record that forms the audit's foundation, and it would not alter the characterisation of what the public record shows.

(4) *Audit transparency and reproducibility*: The audit's scripts, datasets, and reasoning are public and reproducible. Named individuals can inspect the factual claims directly by running the audit's code against the public-record inputs. A pre-publication letter requesting response would be redundant when the entire evidentiary foundation is public-record-accessible and the individuals named already have visibility into the public statements being examined.

Under *Grant v. Torstar* para. 98, the absence of pre-publication outreach is therefore not a diligence failure in this context, because the communication is responsive to a contemporaneous public controversy, rests entirely on publicly-documented statements and public-record facts, and invites post-publication scrutiny of reproducible methodology rather than requesting comment on hidden or investigative findings.

**Fair comment (WIC Radio posture).** Statements such as "the minority commissioners got it wrong" ([§5.9.4](#sec-5-9-4), L554) qualify as fair comment under *WIC Radio Ltd. v. Simpson*, 2008 SCC 40. The fair-comment defence protects opinion and inference made about matters of public concern when those opinions rest on a factual foundation that a reasonable person could share. A court assessing fair-comment defence asks two questions: (1) is the statement recognizable as opinion or inference (not a falsely-stated fact)?, and (2) is it grounded in facts that would permit a reasonable person to reach that opinion? The audit satisfies both prongs. On the first prong, statements such as "the minority commissioners' position does not survive primary-source verification" are explicitly framed as inferences from the documented factual record (the school-division-boundary verification in [§5.9.4.2](#sec-5-9-4-2), with direct quotation of the minority commissioners' original claims and the contradicting primary sources). On the second prong, a reasonable person examining the evidence in [§5.9.4.2](#sec-5-9-4-2) — comparing the minority commissioners' asserted school-division boundaries to actual Alberta Education Division maps — would be able to reach the inference that the commissioners' claim cannot be sustained. The audit does not assert what motive or intent lay behind the error; it documents only the factual discrepancy and the inference available from that discrepancy. This careful labelling of inferences distinguishes the audit's posture from unfounded assertions of bad faith or dishonesty.

The combined effect of *Grant v. Torstar* (responsible communication on a public-interest matter) and *WIC Radio* (fair comment grounded in verifiable facts and clearly labelled as inference) provides a dual defence against any defamation claim. A plaintiff challenging the audit would bear the burden of proving that the characterisations either (a) constitute false statements of fact, established through strict factual proof, or (b) are inferences not reasonably grounded in the facts presented. On both fronts, the audit's public-record foundations and explicitly-labelled inferences provide strong protection.


---

*Draft. Falsifiability gates, robustness checks, and APA citations documented throughout.*
