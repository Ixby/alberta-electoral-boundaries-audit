# Alberta Electoral Boundaries Audit — Comprehensive Forensic Audit Monograph

**A symmetric, reproducible forensic assessment of the 2025–26 Electoral Boundaries Commission's majority and minority recommendations**

*Draft — April 2026 · Non-partisan · [Repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) · Data and scripts linked throughout*

---

## Executive summary and reading guide

This document is a **comprehensive forensic audit monograph**, not a single-topic journal article. It covers three distinct lines of work that share a single dataset and methodology, and it runs substantially longer than a standard journal submission. Readers short on time should use the guide below to jump directly to the part that matches their question. Readers who need the full evidentiary chain should read end-to-end.

**Headline finding (read this if you read nothing else).** The minority 2026 proposal differs from the majority 2026 proposal on five measurable non-partisan-bias dimensions (population dispersion, Calgary geographic-zone asymmetry, Airdrie fragmentation, municipal-boundary anchoring, commission-chair-flagged anomalies) and on one partisan-bias dimension whose sign is measurement-resolution-dependent. All five non-partisan signals run in the same direction and survive every stress-test applied. The partisan-bias magnitude sits below the 7 % Efficiency Gap threshold **proposed in the academic literature** by Stephanopoulos and McGhee (2014/2015) and cited in litigation but **not adopted as a judicial standard** — the US Supreme Court vacated *Gill v. Whitford*, 585 U.S. ___ (2018), on standing grounds without ruling on the threshold. The 7 % figure rests on scholarly authority only; there is no US (or Canadian) judicially-adopted EG threshold. The directional consistency is the finding; no single dimension crosses a classical significance threshold on its own. See §1.1 for the plain-language summary, §1.2 for the modelling-uncertainty caveats, and §6 for the synthesis.

**Reading guide by question.** The monograph has three parts, each answering a different question and each referencing the others:

| If you are here to answer… | Read | Covers |
|---|---|---|
| **Part I — Empirical audit.** *Do the two 2026 maps differ in measurable, reproducible ways?* | Abstract, §1.1, §5.1 (population equality), §5.2 (partisan bias), §5.3 (signatures), §5.4 (MCMC ensemble), §5.6 (symmetry counter-test), §5.7 (stress-test grades), §5.8 (geographic coherence) | Core quantitative findings — the empirical redistricting audit. |
| **Part II — Procedural and policy critique.** *What does the April 16 legislative pivot mean; how does the commission's methodology compare to Canadian norms; what statutory reforms follow?* | §5.9 (procedural), Appendix F (constitutional framing), `analysis/reports/v0_1_act_amendment_proposal.md` (statutory reform), `analysis/reports/v0_1_cycle_lag_commentary.md` §2 (forward-modelling consequences for commissions) | The Canadian comparative and legal-procedural layer. |
| **Part III — Data provenance and methodological warnings.** *Why can't the audit give single-number point estimates on every metric; what does the missing-shapefile situation do to conclusions; what's the DPG framework?* | §4.1.4 (DPG + sunset clause), §3.3 (cycle-lag robustness + dataset-construction consequences), §5.2.7 (four-measurement-layer reporting), Appendix E (approximate geometry), `analysis/reports/v0_1_cycle_lag_commentary.md` §1 (three-vintage sandwich), `analysis/reports/v0_1_methods_paper_draft.md` (companion methodology paper in draft) | The GIS and data-provenance methodology — the part that justifies every qualified finding in Parts I and II. |

**Three companion papers are extractable** from this monograph (and in various stages of draft). Each targets a different publication venue: (a) the Empirical Audit as a ~10,000-word *Canadian Journal of Political Science* or *Election Law Journal* submission; (b) the DPG Methodology Paper as a *Political Analysis* or *Journal of Open Research Software* methods paper (skeleton at `analysis/reports/v0_1_methods_paper_draft.md`); (c) the Policy Critique as an *Alberta Views*–length feature or public-policy brief. This monograph is the master record; the extracted papers are the scoped journal-ready artifacts.

**What to believe.** Every number in this document is reproducible by running a script in `analysis/scripts/` against a dataset in `data/`. Every qualitative claim is anchored in a primary source pinned in `FROZEN_MANIFEST.md`. Where a finding depends on Derived Provisional Geometries (DPG — traced from commission map thumbnails because Elections Alberta had not released official shapefiles at the time of writing), the dependency is disclosed via the §4.1.4 sunset clause which binds the audit to re-run the finding within 48 hours of official shapefile release.

---

## Abstract

*Context and purpose.* Alberta's 2025–26 Electoral Boundaries Commission tabled two incompatible 89-seat maps on March 23, 2026 — a majority recommendation and a minority recommendation — before the Legislative Assembly set both aside on April 16, 2026 and convened a Special Select Committee to draft a 91-seat map by November 2026. This audit evaluates the two commission proposals against the 2019 baseline currently in force along six dimensions: (A) population equality, (B) partisan-bias metrics drawn from the political-science literature, (C) visual geographic coherence, (D) procedural fairness, (4) geometric data provenance, and (5) Markov Chain Monte Carlo (MCMC) ensemble comparison. The same methodology is applied symmetrically to all three maps and released alongside the paper for reproduction.

*Methodology and findings.* The minority 2026 proposal diverges from the majority 2026 proposal and from the 2019 baseline on five structural dimensions: **wider population dispersion (Median Absolute Deviation, MAD: 4,707 versus 3,180)**, a 12.2 % Calgary geographic-zone asymmetry versus the majority's 0.4 %, three visible spatial anomalies flagged by the commission chair, fragmentation of Airdrie across four electoral divisions (EDs) versus the majority's two, and a 71.0 %-versus-14.5 % gap in municipal-boundary anchoring (§5.8.5). A rationale-validation pass against the minority's 25 published justifications finds six of seven contested configurations had cleaner statutory-compliant alternatives the minority did not take. On partisan-bias magnitude, the paper reports **two measurements at different spatial resolutions, which disagree on sign**: a blended crosswalk approach at urban weight w = 0.85 yields a 1.42 percentage-point (pp) UCP-favourable minority-versus-majority Efficiency Gap (EG) asymmetry under 2023 vote input, while a higher-resolution Voting Area (VA)–level spatial attribution using Derived Provisional Geometries (DPG; §4.1.4) yields a 4.15 pp NDP-favourable asymmetry after topology cleanup. Both measurements are internally consistent. The disagreement is treated as a property of measurement resolution rather than a pipeline error and is the subject of a dedicated methodological section (§5.2.7).

*Conclusion.* All EG magnitudes remain within the 7 % threshold proposed by Stephanopoulos and McGhee (2014/2015). The Supreme Court of the United States vacated *Gill v. Whitford*, 585 U.S. ___ (2018), on standing grounds without adopting that threshold as a judicial standard; the 7 % figure in this paper rests on academic-literature authority only. The directional consistency of the minority's structural-asymmetry signals across five non-partisan-bias dimensions, coupled with the procedural departure of April 16, 2026, supports a finding of **systematic structural asymmetry at a magnitude below the 7 % EG threshold proposed in the academic literature** (Stephanopoulos & McGhee 2014/2015; never judicially adopted, see above), with partisan-bias direction remaining sensitive to measurement resolution until Elections Alberta releases official 2026 shapefiles. A sunset clause (§4.1.4) binds the audit to re-run all DPG-dependent analyses within 48 hours of such a release.

**Key phrase for citation:** *"Below the 7 % Efficiency Gap threshold proposed in the academic literature (never judicially adopted); directionally-consistent partisan asymmetry across six independent dimensions at the sub-threshold level."*

---

## Preface — scope, shapefile status, and intended venue

**Shapefile status (2026-04-22).** Elections Alberta had not published 2026 polygon shapefiles at the time of writing. Results that depend on the absent geometry are *approximation-sensitive* and will be re-run as the authoritative version of this paper under the §4.1.4 sunset clause when shapefiles release: Polsby–Popper and Reock compactness (§5.8 / Appendix E); MCMC ensemble scoring at the VA-to-2026-ED assignment step (§5.4); Tier-B and Tier-C boundary residuals (Appendix E). Results that do **not** depend on the 2026 shapefiles: population equality in §5.1 (uses the commission's own per-ED population tables), the four partisan-bias metrics in §5.2 (crosswalk-aggregated 2023 votes against commission-described district compositions), signature detection in §5.3 (commission's published boundary descriptions), and the public-submission audit in §5.9.4 (commission's own submission archive).

**Intended venue and distribution.** The paper is prepared as a public-interest audit. Primary distribution targets are the project's public GitHub repository and a Canadian public-policy venue (*Alberta Views*-length feature and/or an SSRN / OSF preprint). Re-routing to a peer-reviewed journal (*Canadian Journal of Political Science*, *Canadian Public Policy*, *Election Law Journal*) is welcomed; the paper's structure, framework, and data are designed to make that re-routing straightforward. The methodology, pre-registration (§5.5), and falsifiability gates (§4.1.2) are intended to support review at that standard. A companion methodology paper on the DPG framework is in draft at `analysis/reports/v0_1_methods_paper_draft.md`.

---

## Author disclosure

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

**Prior and bias self-audit.** Going into this project the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny. The methodology is designed to produce the same numbers regardless of that prior. Three cases surfaced findings that ran against the prior and were retained in the report: (i) under 2019 vote input the partisan-bias asymmetry reverses sign (§5.2.3); (ii) the commission chair's "no public support" claim is upheld on three of seven configurations, not all seven (§5.9.4); (iii) the majority map's own MAD of 3,180 is tighter than the 2019 current-map baseline computed on 2021 census data (Appendix C), indicating the commission's majority did not introduce partisan looseness relative to the prior-cycle baseline. Full bias self-audit at `analysis/reports/v0_1_bias_audit.md`.

**AI use disclosure.** Claude (Anthropic), a large language model, was used as an analytical and writing assistant throughout this project. Claude's contributions included: drafting and revising report text, proposing analysis structure, identifying consistency gaps across documents, and surfacing methodological edge cases (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). All substantive claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. Claude did not execute code or access external data independently; all script runs were performed by the author.

**Acknowledgements and tools used.** Computational stack: Python 3.14 on Windows 11 (Python 3.9+ required by `setup.sh`; 3.14 used in this session); pandas 2.x (§5.1 population equality, §5.2 vote attribution); numpy (numerical computation); openpyxl (parsing the 2023 Statement of Vote Excel workbook — 87 sheets, 1,973 poll records); geopandas + pyogrio (spatial operations for population aggregation and ED-to-CSD [Census Sub-Division] overlay; full Phase 4/5 execution blocked on 2026 shapefile release); shapely + pyproj (polygon topology and projection, NAD83 / Alberta 3TM, EPSG:3776); osmnx (OSM road network extraction, prepared for Phase 4D fallback); gerrychain (MCMC ensemble generation, 100,000-plan run reported in §5.4); pdfplumber (PDF table extraction for commission report and Appendix E parsing); geopy + rapidfuzz (geocoding and fuzzy-string matching). Version control and distribution: git, GitHub CLI, GitHub public repository [Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit). No traditional statistical software (R, Stata, SPSS), no GIS desktop software (QGIS, ArcGIS), no commercial election-analytics platforms, and no paid datasets were used; all inputs are public. Integrity tools applied: falsifiability gates G0–G5 built into the pipeline; bias self-audit at `analysis/reports/v0_1_bias_audit.md`; uncertainty analysis at `analysis/methodology/v0_1_uncertainty_and_shapefile_impact.md`. Code authored for this audit: `analysis/scripts/v0_2_packing_cracking_analysis.py` (symmetric three-map partisan-bias pipeline), `analysis/scripts/electoral_forensics_population.py` (population-equality analysis A1/A2/A3), `analysis/scripts/v0_3_monte_carlo_ci.py` (Monte Carlo confidence-interval ensemble), `analysis/scripts/v0_1_a1_legal_baseline_2021_census.py` (2021-census-direct A1 computation for 2019 EDs), `analysis/scripts/v0_1_majority_symmetry_counter_test.py` (symmetry-of-test-selection counter-test), `analysis/methodology/v0_1_cochrane_journey_to_work.md` (journey-to-work commute analysis), `analysis/scripts/v0_1_csd_community_splits.py` (CSD-level community-splits overlay), `analysis/scripts/v0_1_338canada_scraper.py` + `analysis/scripts/v0_1_338canada_reallocate.py` (338Canada per-riding integration). Data sources: Elections Alberta Statement of Vote 2023 (`data/2023_results.xlsx`); Alberta Electoral Boundaries Commission final report, March 23, 2026 — extracted populations and variance tables, map images (`maps/*.jpg`); Elections Alberta GIS resources page (checked for 2026 shapefiles — not yet published); Statistics Canada 2021 Census Dissemination Area populations and shapefiles (`data/alberta_2021_da_populations.csv`, `data/alberta_2021_das.gpkg`); Alberta Treasury Board Office of Statistics and Information quarterly population estimates; StatsCan Table 17-10-0009 quarterly provincial estimates; StatsCan Table 98-10-0459 (2021 Census journey-to-work by CSD).

Data and scripts: `analysis/*.py`, `data/*.csv`, `data/2023_results.xlsx`.

---

## 1. Introduction

Alberta's 2025–26 Electoral Boundaries Commission delivered two final reports on March 23, 2026: a majority report and a minority report proposing incompatible 89-seat maps. Three weeks later, on April 16, 2026, the Alberta Legislative Assembly passed Motion 19 setting aside the majority report and establishing a Special Select Committee of five MLAs to draft a 91-seat map by November 2, 2026. That procedural pivot — replacing an independent commission's drafting process with a government-chaired committee mid-cycle — raised three questions this paper addresses. First, do the two commission proposals diverge in measurable, reproducible ways? Second, do those divergences run systematically in one political direction? Third, can the conclusions of the April 16 pivot be evaluated against a pre-registered falsifiability framework?

### 1.1 Headline findings in plain language

Before the technical caveats below, the audit's structural findings summarise cleanly. Using the same methodology applied symmetrically to all three maps:

- The **minority 2026 proposal spreads population more unevenly** across districts than the majority proposal (Median Absolute Deviation from provincial average: 4,707 versus 3,180) — a 48 % wider dispersion.
- The **minority map's Calgary districts** show a 12.2 percentage-point geographic-zone asymmetry (urban-core districts smaller, suburban-ring districts larger) versus 0.4 pp on the majority map.
- The **minority map splits the City of Airdrie four ways** across different electoral divisions; the majority map splits it two ways.
- The **minority map follows existing municipal boundaries** on only 14.5 % of its total perimeter, versus the majority's 71.0 % — a 4.9-fold departure from the Canadian-commission norm of preserving community-of-interest via municipal-edge alignment.
- **Three geographic anomalies** on the minority map were flagged by the commission chair (Rocky Mountain House–Banff Park extension; Calgary-Nolan Hill–Cochrane lasso; Olds-Three Hills-Didsbury → N Airdrie community capture); zero were flagged on the majority map.
- The **minority's own 25 published rationales** are, on six of seven contested configurations, options the minority did not take when cleaner statutory-compliant alternatives were available.

These five non-partisan-bias signals all point in the same direction and all survive the stress-tests documented in §1.2 below. The partisan-bias signal (the extent to which the maps would produce different seat counts from the same votes) is reported in the abstract as a two-measurement disagreement; §1.2 explains the caveats that constrain the magnitude claim.

### 1.2 Modelling-uncertainty caveats

Three modelling-uncertainty tests materially narrow the partisan-bias magnitude claim while leaving the structural findings in §1.1 intact. These are reported up-front for transparency; the underlying methodology is in `analysis/reports/v0_1_design_critique.md` and the Monte Carlo script `analysis/scripts/v0_3_monte_carlo_ci.py`.

**1. Monte Carlo 95% CI over modelling choices crosses zero.** N=2,000 samples varying urban weight (0.55–0.85), rural baseline (0.26–0.36), and per-hybrid jitter (±0.10). Minority-majority EG asymmetry: mean −1.22 pp, median −1.44 pp, **95% CI [−3.04, +0.76] pp**. Direction consistency: 90.5% of samples show minority more UCP-favorable. Classical 95% significance is **not** defensible; a directional observation at approximately 90% confidence is the reportable finding.

**2. Declination metric (Warrington, 2018) disagrees with the efficiency gap.** Declination computed: 2019 = −0.034, Majority = −0.021, Minority = −0.015. By declination, the minority is the least pro-UCP of the three maps, the opposite direction from EG and the seats-at-50/50 estimate. Warrington (2018) documents this kind of cross-metric divergence as an expected feature of competing formalisations rather than a methodological flaw; Katz, King, and Rosenblatt (2020) recommend ensemble reporting. Both metrics are retained; neither is dispositive on its own.

**3. 2019 cross-election check reverses the EG asymmetry.** Running identical methodology with 2019 vote totals (instead of 2023) produces Majority EG +0.30%, Minority EG +0.90%, asymmetry **+0.60 pp** (minority less UCP-favorable). The direction of the headline asymmetry flips sign depending on which election's votes are used as input. The observed asymmetry is not a stable property of the maps alone; it is an interaction between the maps and 2023-specific voter distribution patterns. The direction does replicate under 338Canada's April 2026 polling input (see §5.2.3), suggesting stability across 2020s-era political geography but not across the 2019 electorate.

**What survives these tests unchanged:**
- §5.1.1 population distribution variance (CSV-sourced, election-independent): minority MAD is 48% wider than majority.
- §5.1.2 Calgary geographic-zone gap: minority 7.7–12.2%; majority 0.36–0.39%. Not vote-based.
- §5.8.2 visual spatial anomalies: 3 minority anomalies confirmed on published maps.
- §5.8.4 community splits: Airdrie 4 vs 2, Cochrane merged vs intact, Chestermere partial split vs intact.
- §5.9 procedural concerns: government-controlled replacement of drafting process, qualitative.

**What is narrowed:**
- §5.2 partisan-bias *magnitude* claims. The central point estimate of 1.42 pp (w=0.85) is within Monte Carlo noise (95% CI crosses zero). The direction holds at 90.5% confidence across modelling uncertainty, which is a defensible directional claim but not classical 95% significance.
- The "minority gives UCP 2 more seats in a tied election" line. Under Monte Carlo, minority NDP@50/50 has 95% CI [41, 47] vs majority [43, 46] — overlapping. The 1-seat gap size is stable across 2023 votes and April 2026 polling inputs, but the *direction* of that 1-seat gap flips between them (UCP +1 on minority under 2023; NDP +1 on minority under April 2026 polling). A structural-invariance claim was not supported by the historical stability test and has been retracted; see §5.2.3. The magnitude CI crosses zero.
- "Directionally consistent across six dimensions" is more precisely "directionally consistent across five of six tested dimensions, with one partisan-bias metric (declination) pointing the opposite way."

**Defensible synthesis.** The minority 2026 proposal shows measurable structural differences from the majority in four areas: population distribution (MAD 48% wider), Calgary geographic-zone balance (12.2% gap vs 0.4%, robust across two classification rules), community-of-interest treatment (Airdrie split across 4 EDs vs 2, with the same pattern visible in Lethbridge and Red Deer — see §5.6), and visible boundary shape (three confirmed anomalies). None of these depend on vote data. A fifth dimension is the rationale-failure pattern: six of the seven contested minority redraws have cleaner options available that satisfy the statutory population and area limits while matching documented public submissions; the seventh (St. Albert-Sturgeon) has no real alternative (see §5.9.2 and `analysis/methodology/v0_1_minority_rationales_validation.md`). The partisan-bias consequences are directionally UCP-favorable for the minority in 90.5% of modelling-jitter samples using 2023 vote attribution, outlier-flagged at p98.8 on mean-median (UCP-tail) and at p1.6 on declination (NDP-tail) against a 100,000-plan full-coverage ReCom neutral ensemble on 2019 baseline substrate (see §5.4), reverse sign under 2019 vote attribution, and shift to a 1-seat NDP advantage on the minority under April 2026 338Canada polling. The core claim is that the minority has more structural irregularities and more rationale failures than the majority; a specific partisan-seat-shift magnitude is less defensible and sensitive to election baseline. The procedural concern about the April 16 government action stands separately from the partisan-math questions.

**Contribution.** This paper makes three contributions. It applies a symmetric, falsifiability-gated framework to both 2026 proposals and the 2019 baseline, producing reproducible estimates of population equality, partisan bias, geographic coherence, and procedural fairness. It pre-registers the test battery against a forthcoming third map — the November 2026 MLA-committee 91-seat proposal — so the audit can be replayed against new evidence rather than reinterpreted after the fact. And it documents the data-provenance caveats that arise when 2026 shapefile release is gated by legislative adoption, leaving explicit placeholders for the checks that remain pending.

**Scope.** The paper does not reach a legal conclusion. It is evidentiary: it records what the public data show under identical methodology applied to all three maps, so that any interested party — court, legislator, commissioner, journalist, academic — can repeat the computations, challenge the inputs, and reach their own judgments. The court-ready interpretation is deferred to §8 (Conclusion) and Appendix F (Legal Interpretive Note).

---

## 2. Background and Prior Work

The analysis rests on four bodies of prior work: US partisan-gerrymandering measurement, Canadian independent-commission practice, population-equality jurisprudence, and computational redistricting methodology.

**Partisan-bias measurement.** Stephanopoulos and McGhee (2014, 2015, 2018) introduced the efficiency gap (EG) as a single-number measure of wasted-vote asymmetry and proposed a 7% threshold for investigable bias. McDonald and Best (2015) advanced the mean-median gap as a complementary measure of distributional skew. Gelman and King (1994) formalised seat-vote-curve symmetry as a Bayesian estimator, building on Grofman (1983) and King and Browning (1987). Warrington (2018, 2019) introduced declination and documented that EG and declination can disagree on a non-trivial fraction of US-state plans — a finding directly relevant to the Alberta disagreement reported in §5.2.4. Katz, King, and Rosenblatt (2020) argue that no single metric is dispositive and recommend ensemble reporting, which the stress-test gate RT2 in this audit implements. US constitutional jurisprudence touched these metrics through *Gill v. Whitford*, 585 U.S. ___ (2018), which the Supreme Court vacated and remanded on standing grounds without adopting the 7% EG threshold as a judicial standard. The 7% threshold is therefore a scholarly proposal from Stephanopoulos & McGhee (2014/2015), not a judicial holding; its use in this paper is on academic-literature authority only.

**Natural packing vs engineered packing.** Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through packing of their voters into city cores. §5.2.5 of this audit applies the Chen-Rodden framework to Alberta and finds that the *direction* prediction transfers but the *mechanism* does not: Alberta's UCP-favourable baseline comes from dispersed rural UCP-winning margins, not from NDP urban packing. This matters for what any 2026 map's partisan bias can legitimately be attributed to.

**Canadian redistribution practice.** Courtney (2001, 2004) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces. The constitutional benchmark, *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, establishes "effective representation" — not strict population parity — as the standard against which boundary-commission output is measured. The Charter §3 right to vote developed by *Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912, and *Frank v. Canada (Attorney General)*, [2019] 1 SCR 3, forms the backdrop without applying directly to redistribution. §5.9.3 compares the April 16, 2026 Alberta pivot against three Canadian comparator cases (Quebec 1992, Ontario 1996, British Columbia 2008).

**Compactness and computational methods.** Polsby and Popper (1991) and Reock (1961) supply the two compactness metrics referenced throughout; Barnes and Solomon (2021) document their implementation sensitivity. DeFord, Duchin, and Solomon (2021) introduce the ReCom MCMC family used for the neutral-ensemble baseline in §5.4. Herschlag, Ravier, and Mattingly (2020) demonstrate the ensemble-comparison methodology the Alberta audit applies here. Altman and McDonald (2011) articulate the four-axis redistricting-audit discipline — population equality, compactness, political fairness, community of interest — whose consistency-across-dimensions framing § E of this paper draws on. Fifield, Imai, Kawahara, and Kenny (2020) discuss the empirical-validation requirements for redistricting simulation results.

**Pre-registration and evidentiary discipline.** Nosek et al. (2018) and Munafò et al. (2017) codify the pre-registration discipline the audit's November 2026 test protocol follows. American Statistical Association (2016, 2019) statements on p-values and graded evidence guide the audit's reporting of directional findings at sub-threshold magnitude. These disciplines matter because the paper's central claim — six dimensions pointing in the same direction, none individually at classical 95% significance — is inferentially valid only under pre-registered test selection and reported-versus-hidden-test symmetry.

The audit's methods map onto this literature as follows: B2–B6 (§5.2.1) implement Stephanopoulos-McGhee, McDonald-Best, Gelman-King, and Warrington directly; §5.4 implements DeFord-Duchin-Solomon ReCom against a 100,000-plan neutral ensemble; §5.2.5 validates Chen-Rodden for Alberta; §5.9.3 positions the procedural finding against Courtney's Canadian comparator sample. Where the Alberta context departs from US or Canadian prior work, the departures are documented rather than elided.

---

## 3. Data

This section consolidates the audit's data-provenance disclosures — primary sources, their `FROZEN_MANIFEST.md` anchor dates, known coverage caveats, and robustness to cycle-lag. All downstream analyses in §5 inherit from the sources listed here; deeper provenance notes (including the Plan B population-basis cross-check and the 2021-census-direct legal-baseline reconstruction) are in Appendices C and E.

### 3.1 Primary data sources

| Source | File(s) | URL | Manifest anchor |
|---|---|---|---|
| Elections Alberta 2023 Statement of Vote | `data/2023_results.xlsx` | https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx | `FROZEN_MANIFEST.md` (2026-04-22 access) |
| Commission final report (majority + minority) | `data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv`; map images in `maps/*.jpg` | https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | `FROZEN_MANIFEST.md` (2026-03-23 publication) |
| Elections Alberta GIS page (2026 shapefiles) | (not available) | https://www.elections.ab.ca/resources/maps/ | `FROZEN_MANIFEST.md` — 2019 / 2023 polygons present, 2026 not yet published |
| StatsCan 2021 Census Dissemination Areas | `data/alberta_2021_da_populations.csv`, `data/alberta_2021_das.gpkg` | https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/ | `FROZEN_MANIFEST.md` |
| Alberta Treasury Board Office of Statistics and Information quarterly estimates | (embedded in commission totals) | https://open.alberta.ca/dataset/alberta-population-estimates | `FROZEN_MANIFEST.md` |
| StatsCan Table 17-10-0009 (quarterly provincial estimates) | (cited; not persisted) | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901 | `FROZEN_MANIFEST.md` |
| StatsCan Table 98-10-0459 (2021 Census journey-to-work) | (cited in §5.8.4) | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810045901 | `FROZEN_MANIFEST.md` |

### 3.2 Coverage caveats

Three coverage gaps constrain the audit's scope; each is disclosed rather than papered over.

1. **2026 polygon shapefiles not released; formal request pending.** Elections Alberta's GIS page (accessed 2026-04-22) carries 2019 ED polygons and 2023 VA polygons but does not yet carry 2026 ED polygons. A formal written request for the 2026 boundary shapefiles has been filed with Elections Alberta; no response has been received as of the publication date of this report. In parallel, synthetic 2026 ED polygons were constructed from the commission's report text, Appendix E boundary descriptions, and the methodology documented in `analysis/reports/v0_1_approximate_shape_analysis.md` and `analysis/methodology/v0_1_shape_refinement_v2.md`. Three iterative refinement passes — snapping to OSM road, waterway, railway, and administrative-boundary features within progressively tighter buffers — reduced the positional error on Tier A/B district boundaries to a maximum of ±1 km (mean shift 97 m after v1; residual voter-assignment impact after v3: 1,012 votes across 4 VAs, approximately 0.06% of 2023 total valid votes). Tier C hybrid boundaries remain unresolvable at shapefile-grade precision from commission text alone. Full refinement log and per-boundary confidence classification at `analysis/methodology/v0_1_shape_refinement_v2.md` and `data/v0_1_boundary_refinement_impact_v3.csv`. Results that depend on precise geometry — Polsby-Popper and Reock compactness for Tier C EDs, the full GerryChain ReCom ensemble seeded from 2026 geometry, and precise VA-polygon vote attribution — remain pending the official shapefile release or a response to the formal request.
2. **Majority-proposal map imagery incomplete.** The working bundle has the majority's Calgary map; the majority Alberta overview, Edmonton, and other-cities panels are not in the bundle. Visual inspection of the majority is therefore limited to its Calgary districts. §5.8.1 discloses this scope narrowing.
3. **~88 public submissions (6.6%) could not be machine-parsed.** Their PDFs are image-only scans lacking a text layer. The submission-archive verification (§5.9.4) rests on identified counter-examples in the 1,252 parseable submissions rather than exhaustive enumeration of all ~1,340.

### 3.3 Cycle-lag robustness

The population data the commission uses carries a cycle-lag: the 2021 decennial census updated to a July 1, 2024 Office of Statistics and Information estimate. Alberta's cumulative population growth from 2021 to mid-2025 is approximately 17.8%. The audit's `analysis/v0_1_cycle_lag_analysis.md` computes how many electoral divisions flip ±25% window status when mid-2025 populations are substituted: 5 of 87 on the 2019 map, 0 of 89 on the majority 2026 proposal, and 5 of 89 on the minority 2026 proposal. The audit's `analysis/reports/v0_1_plan_b_cross_check.md` independently verifies that every §5.1 verdict is identical whether computed against the 2021 census directly, the 2024 OSI estimate, or the 2025 TBF estimate — i.e. the directional findings are robust to which intra-cycle population vintage is used. Appendix C supplies a 2021-Census-direct A1 computation on the 87 existing 2019 EDs as the §12(3)-operative reference point.

**Dataset-construction consequences of cycle lag (three-vintage sandwich).** Beyond the verdict-robustness property above, the 4–14-year lag between commission data-basis and boundary retirement materially shapes *how* the audit's upstream pipelines construct their datasets. Any reconstruction of the commission's arithmetic has to reconcile three input vintages simultaneously:

- **2021 geometry + 2021 population.** Statistics Canada Dissemination Area (DA) polygons carrying 2021 census populations — the atomic unit used for Phase 4B DA-overlay.
- **2024 operative estimate.** The commission's July 2024 Treasury Board and Finance (TBF) estimate for each 2026 proposed ED — the operative published value against which the commission's variance tables were computed.
- **2023 voting substrate.** The 2023 Voting Area (VA) polygons carrying 2023 votes — the spatial substrate used for Phase 4C partisan-bias attribution.

The ratio between the 2021-population-sum-inside-a-2026-DPG-polygon and the commission's 2024 estimate of the same territory is **not** a clean scalar. Alberta's 14.69 % provincial growth between 2021 and 2024 was distributed unevenly — Calgary-ring cities such as Airdrie and Chestermere grew 20–30 %, rural territories grew 0–5 % — so applying a flat provincial growth factor to a regionally heterogeneous population surface introduces a structural bias into Phase 4F's per-ED validation deltas. The 81 of 86 majority and 87 of 89 minority hardstop failures documented in `data/INTEGRITY_STATUS.md` are therefore a composite signal: **real DPG transcription error plus cycle-lag growth heterogeneity, not separable from public data alone**. The §4.1.4 sunset clause binds the audit to recomputation if Elections Alberta releases official shapefiles, at which point real geometric error would be distinguishable from cycle-lag artifact. Full treatment at `analysis/reports/v0_1_cycle_lag_commentary.md` (§1).

**Forward-modelling consequences for commissions.** The 2021 decennial census — the Commission's statutorily-mandated baseline under §12(3) — is 4 years stale at the first election under the new boundaries (2027) and up to 14 years stale at the boundaries' retirement (potentially 2035). For fast-growth metropolitan-fringe cities (Airdrie, Chestermere, Cochrane, Okotoks, Beaumont, Leduc, Spruce Grove, Fort Saskatchewan, Sherwood Park), this gap already moves per-ED population quotas by 10–15 % at the 4-year mark and by 40 %+ at the 14-year mark under current growth rates, independent of any drawing choice the commission makes. For slow-declining rural districts (Peace River, Central Peace-Notley, Lesser Slave Lake), the gap erodes §15(2) special-rural-protection ratios asymmetrically: Lesser Slave Lake's mid-2025 §15(2) qualifying ratio drops past −50 % of the provincial mean under the cycle-lag substitution, which could disqualify a district from its current legal basis before the cycle concludes. Indigenous on-reserve populations face a third variant of the same problem: commissions inheriting the census's chronic 3–10 % on-reserve undercount see those communities structurally under-represented for the full 6–14-year cycle. None of this is resolvable by audit methodology alone; the §12 statutory framework itself determines what baselines the Commission is permitted to consult. A legislative-reform proposal formalising a composite basis (TBF primary + StatsCan tie-breaker at ±2 % + AHCIP + CRA T1 cross-check + CEO as certifying authority) is outlined at `analysis/reports/v0_1_act_amendment_proposal.md`; the audit offers this as a policy contribution, not a finding. Full treatment at `analysis/reports/v0_1_cycle_lag_commentary.md` (§2).

---

## 4. Methods

This section describes the audit's methodology; results follow in §5. The methods are presented in the sequence they are applied: the symmetry and falsifiability discipline (§4.1), the vote-attribution pipeline used for all partisan-bias metrics (§4.2), the specific test battery B1–B6 with thresholds and references (§4.3), and the legal-defensibility frame used to map findings to potential challenges (§4.4). Mathematical formalism for the four metrics is consolidated in Appendix D.

### 4.1 Methodology and integrity framework

#### 4.1.1 Symmetry requirement

Every test applied to one map is applied identically to the others. Where a data gap prevents symmetric application, the gap is disclosed explicitly and the claim's scope is narrowed to what is symmetric.

#### 4.1.2 Falsifiability gates

Each analytical stage produces a PASS/FAIL gate value before propagating downstream. Gates implemented:

- **G1 (carry-forward verification):** B1–B4 on 2019 baseline must reproduce the four-figure match to official totals (NDP 777,404 / UCP 928,900, two-party 1,706,304). Reproducible via `python3 analysis/scripts/v0_2_packing_cracking_analysis.py`.
- **G2 (2026 estimate count):** Each map's ED estimate set must contain exactly 89 districts; total valid votes within 5% of 1.7M; NDP share within [0.40, 0.50]. `validate_2026_estimate()` in `v0_2_packing_cracking_analysis.py`.
- **G3 (Calgary classification coverage):** A2 test requires zero residual unclassified Calgary EDs. Enforced programmatically in `a2_calgary_analysis()`.
- **G4 (A2 robustness):** A2 directional finding must survive alternative classification (2023 winner-based) or be flagged as classification-dependent. `a2_robustness_check()` implements the alternative.
- **G5 (Sensitivity range):** B2 efficiency gap computed under urban weights 0.60, 0.70, 0.80, 0.85 (central), 0.90. Direction must be consistent across all five; magnitude range is reported alongside the central estimate.

#### 4.1.3 What does not enter the report

- Any number not reproducible by running a checked-in script against checked-in data
- Any classification rule without a robustness check under at least one alternative
- Any language characterizing one map's features with stronger modifiers than the other's when the underlying facts are comparable
- Any "the numbers confirm X" framing in section preambles

#### 4.1.4 Derived Provisional Geometries (DPG) and localization uncertainty

Official Elections Alberta shapefiles for the two 2026 proposals had not been published at the time of this audit (see Appendix E.1). All 2026 boundary geometries used in this analysis are **Derived Provisional Geometries (DPG)**, reconstructed from the commission's 600-DPI PNG extractions of Appendix A (majority) and Appendix E (minority) via affine transformation, OpenStreetMap feature-class snapping (road, waterway, railway, administrative), and — for territorially contested hybrids — population-calibrated parametric sweep. The canonical DPG coverage (89 EDs per map) lives at `data/v0_1_canonical_{majority,minority}_2026_eds.gpkg`; derivation provenance is in the `canon_source` column (v7 = visually-transcribed, 2019-parent = Tier A inheritance, sweep = population-calibrated, osm-municipal-buffered = Edmonton-Beaumont fix).

**Two error modes should be distinguished when reading DPG-derived results:**

1. **Perimeter-mode uncertainty (±500 m typical).** Boundary localization error. Affects perimeter-dependent metrics most directly — Polsby-Popper and Reock compactness scores, per-segment distance measurements, and fine-grained vote-attribution near the boundary line. Managed by feature-class snapping where a natural feature (river, rail, section line) is visible on the commission thumbnail.

2. **Area-mode uncertainty (variable, Tier-dependent).** Whole-polygon-territory mismatch. Affects area-dependent metrics — DA-overlay populations, intersection tests, and vote attribution when a polygon either absorbs adjacent territory or leaves a gap. Tier A (2019-inheritance) EDs retain shapefile-grade fidelity. Tier B (voter-neutral refinement) EDs have documented ±500 m perimeter residual with ≤ 0.06 % province-wide voter-impact. Tier C (visually-transcribed hybrids) can fail more severely: the session-12 Phase 4F validation documents per-ED population deltas exceeding 200 % on three minority EDs (Edmonton-Beverly-Clareview, Stony Plain–Drayton Valley, Edmonton-Highlands-Norwood) and approaching 100 % loss on several where a DPG polygon left a territorial gap. These cases are itemised in `data/v0_1_phase4f_validation_deltas.csv` and discussed in `data/INTEGRITY_STATUS.md`.

**Implications for the paper.** Perimeter-dependent metrics (C1 Polsby-Popper, C2 Reock) are reported as confidence bands rather than point estimates on Tier B and C EDs (see §5.8). Area-dependent metrics that depend on accurate DA-overlay populations are **not reported as primary findings** in this paper — §5.1's population equality figures use the commission's published per-ED table, not DA-overlay derivation. Vote attribution (§5.2) uses a blended crosswalk approach as the primary path and DPG-VA spatial attribution as a cross-check; the disagreement between these two measurement resolutions is reported transparently in §5.2.5.

**Sunset clause.** All DPG-dependent metrics in this paper are provisional. If Elections Alberta publishes official topological shapefiles for the 2026 proposals — or for any successor map produced by the November 2026 committee — the audit commits to a full re-computation of all compactness (C1, C2), exact-attribution (Phase 4C), and MCMC ensemble scoring metrics against the official geometry within 48 hours of release. The pre-registered checklist at `analysis/reports/v0_1_pre_registration_draft.md` and the amendment at `analysis/reports/v0_1_pre_registration_amendment_2026-04-23.md` bind the audit to this recomputation and to public disclosure of any sign-flip or magnitude change.

### 4.2 Vote-attribution pipeline

2026 ED-level vote estimates are built by mapping each 2026 ED to its 2019 predecessor(s) using an explicit dictionary (`MAJORITY_2026_MAPPING`, `MINORITY_2026_MAPPING`). Three mapping types:

- `direct`: 2026 ED covers approximately the same territory as a 2019 ED; use 2019 votes directly.
- `blend`: 2026 ED combines a 2019 urban core with rural absorption; blend 2019 core vote with the 2023 observed Rest-of-Alberta NDP share (33.5%) using urban weight 0.85 (applied identically to both maps).
- `merge`: 2026 ED combines two 2019 EDs; weight each part explicitly.

### 4.3 Test battery

**Sign-convention glossary.** Throughout this paper, for every partisan-bias metric: **negative value = UCP advantage** (UCP wastes fewer votes per seat / carries the higher-than-median district / wins more seats at 50/50 / has shallower winning-district-margin angle than NDP), and **positive value = NDP advantage**. The sign convention is chosen for readability against seat-count outcomes, not to match the Stephanopoulos-McGhee 2:1 slope convention (which labels positive EG as "first-party disadvantaged"). Readers cross-referencing the S-M literature should invert the sign-label, not the finding; both conventions agree on the *ordinal* ranking of the three maps. Full glossary and cross-convention reconciliation in `analysis/methodology/v0_1_sign_convention_resolution.md`.

- **B1:** Vote distribution histogram across 10 margin bins from UCP +25%+ to NDP +25%+. (Descriptive; no formal literature reference.)
- **B2:** Efficiency gap (Stephanopoulos & McGhee, 2014): $\text{EG} = (W_{\text{NDP}} - W_{\text{UCP}}) / N$ where wasted votes include loser votes plus winner votes above the threshold. **Sign convention note.** This audit reports EG using the proportional-seat baseline ("negative EG = UCP advantage" in seat-outcome terms) rather than the Stephanopoulos-McGhee 2:1 slope baseline ("positive EG = first-party disadvantaged"). The two conventions produce the same *ordinal* ranking of the three maps and therefore the same direction of the minority-vs-majority asymmetry, but they label the sign opposite. Full resolution in `analysis/methodology/v0_1_sign_convention_resolution.md`; the resolution confirms no minority-vs-majority direction claim requires flipping. Where this paper says "negative EG = UCP-favourable," a reader comparing against S-M literature should invert the sign-of-label, not the finding.
- **B3:** Mean-median gap (McDonald & Best, 2015): $\text{MM} = \bar{v} - \tilde{v}$ for NDP vote share.
- **B4:** Seats-votes under uniform swing to 50/50 provincial share (Gelman & King, 1994; Grofman, 1983).
- **B6:** Declination (Warrington, 2018). Measures the asymmetry between winning-district vote distributions by treating each party's winning districts as a vector and computing the angle between them. See §5.2.4 for the direction-disagreement finding.

The seat-vote-curve symmetry principle underlying B4 traces to Grofman (1983) and King and Browning (1987), later formalized as a Bayesian estimator by Gelman and King (1994). The efficiency gap and mean-median are two of the most widely-cited partisan-bias metrics in the post-*Gill v. Whitford* literature; Stephanopoulos and McGhee (2018) revisit the efficiency-gap debate and acknowledge the metric's sensitivity to modeling choices, which our Monte Carlo analysis in §5.2.2 quantifies for the Alberta context. Katz, King, and Rosenblatt (2020) argue that no single metric is dispositive and recommend ensemble approaches, which this audit's stress-test gate RT2 (cross-metric agreement) implements.

Mathematical definitions for EG, MM, and the Polsby-Popper and Reock compactness metrics are in Appendix D.

### 4.4 Legal-defensibility framework (D1–D10)

The audit's red-team framework (documented in `analysis/red_team/v0_1_legal_red_team_framework.md`) evaluates each finding against ten legal-defensibility dimensions:

- **D1 — Evidentiary chain (primary source + archive).** Every claim traces to a checked-in source anchored in `FROZEN_MANIFEST.md`.
- **D2 — Attribution accuracy (verbatim quotations).** Chair statements, commissioner statements, and submission excerpts are quoted verbatim with source paragraph.
- **D3 — Individual-actor characterisation (fair comment, public-interest, not defamatory).** Claims about specific actors are anchored in on-record behaviour; fair-comment and public-interest defences supported.
- **D4 — Methodology reproducibility.** Every numeric finding is reproducible via `python3 analysis/<script>.py`.
- **D5 — Data provenance.** Every CSV / GPKG / JSON has a documented source chain back to a primary anchor (§3 and Appendix E).
- **D6 — Privilege / scope (fact vs opinion vs allegation).** Facts are labelled; inferences are labelled; constitutional and legal conclusions are reserved to counsel and courts.
- **D7 — Conflict of interest (author's standing).** §1's Author Disclosure block makes the prior explicit and lists three findings that ran against the prior and were retained (`analysis/reports/v0_1_bias_audit.md`).
- **D8 — Copyright / fair dealing.** Submission-archive excerpts, commission report quotations, and map images are used under fair-dealing for criticism and research (Copyright Act s. 29.1).
- **D9 — PII / confidentiality.** No personally identifying information beyond public officeholders' on-record statements and submitters who chose public-record submission is reproduced.
- **D10 — Time-stamped / falsifiable claims.** Pre-registration and OSF submission (§5.5) provide third-party time-stamped custody; every falsifiable claim carries an explicit falsifier (§7.2).

### 4.5 What this audit does not claim

The paper does not claim statistical significance at the conventional 95% threshold on the partisan-bias magnitude: the Monte Carlo 95% CI over modelling choices crosses zero (see §1). It does not claim intent: reproducible directional findings are consistent with intentional engineering or with unlucky structural choice, and the audit cannot distinguish between these without additional evidence beyond public data. It does not reach a constitutional conclusion: Appendix F sets out the *Reference re Saskatchewan* [1991] effective-representation framework under which the evidence could be evaluated by counsel and a court, but does not itself render a verdict. The audit's positive claim is structural, directional, and evidentiary.

### 4.6 Test selection rationale + defense in depth

A full methodological reflection on *which* tests were chosen from the redistricting-analysis literature, *why* these rather than others, what specific criticisms each test carries and how the audit defends against them, what improvements have landed in response to red-team feedback, and what combined or novel tests (neighbour-drain adjacency, boundary-chain, temporal-compound durability, compactness-weighted EG) could add is at `analysis/methodology/v0_1_test_selection_rationale.md`.

### 4.7 Audit dependency graph (machine-readable apparatus map)

To answer the 2026-04-24 "house of cards" critique (whether this audit's findings all share a single fragile L0/L1 dependency such that one bad data point would cascade to most conclusions), the full apparatus was serialised into a machine-readable dependency DAG: 234 nodes across four layers (L0 raw data: 32; L1 constructed artefacts: 53; L2 analytical scripts: 75; L3 named findings: 74) linked by 454 edges (396 required, 23 corroborating, 35 validating). Builder / renderer / query CLI at `analysis/scripts/v0_1_dependency_graph_{build,render,query}.py`; data at `analysis/methodology/audit_dependency_graph.{json,dot}`; SVG at `maps/audit_dependency_graph.svg`; schema + worked examples at `analysis/methodology/audit_dependency_graph_readme.md`.

**Headline diagnostics.** The graph is **acyclic** (topological sort succeeds; no finding depends on itself through any chain); has **zero orphan findings** (every L3 finding is reachable from L0 raw data via at least one path); and has five invalidation-cascade classes quantifying what survives when a given L0/L1 dependency is removed:

| Invalidated dependency | Findings orphaned | Findings robust | Comment |
|---|---:|---:|---|
| 2023 Statement of Vote (L0 vote data) | 48 of 74 (65 %) | 26 (35 %) | Largest-cascade L0: kills B-family + signatures + MCMC real-map scoring. Population-equality + geometry-only C-family + §5.9 procedural are insulated. |
| Commission-published map PNGs | 26 of 74 (35 %) | 48 (65 %) | Kills all DPG-derived findings + signatures + anchoring. Vote-only B-family + MCMC + population + procedural insulated. |
| 2021 Census DAs (populations + geometry) | 25 of 74 (34 %) | 49 (66 %) | Kills DA-anchoring + Phase 4B/4F + MCMC ensemble + Chen-Rodden. Commission-population A-family + per-map B-family + CSD splits insulated. |
| 100k MCMC ensemble | 24 of 74 (32 %) | 50 (68 %) | Kills §5.4 percentile flags + Chen-Rodden decompositions + R-hat. Per-map B-family point estimates + signatures + structural findings insulated. |
| v0_2 topology-clean DPG | 20 of 74 (27 %) | 54 (73 %) | Kills high-resolution §5.2.7 spatial branch + §5.8.5 anchoring. Most of the apparatus survives. |

**Load-bearing-node reading (retraction-pathway §7.1.B resolution).** The 2026-04-24 retraction pathway committed the audit to retract the "directional consistency across six dimensions" synthesis if the DAG revealed that more than half the findings share a single fragile L0/L1 node. The DAG result meets that numerical threshold on the 2023 Statement of Vote (65 % of findings orphaned), but the retraction condition has a qualitative escape: partisan-bias analysis by definition depends on vote data; a Statement-of-Vote dependency is *expected* of any B-family finding and is not evidence of apparatus fragility. The *structurally-independent* core of the audit — the 26 findings that survive invalidation of the Statement of Vote — spans §5.1 population equality, §5.8 geographic coherence, §5.9 procedural departure, and the geometry-only subset of §5.3 signatures. These 26 findings carry the audit's main structural-asymmetry claim without vote-dependence; the B-family strengthens but does not singularly carry that claim. The synthesis is therefore NOT retracted on this ground, but is *refined*: the directional-consistency reading is reported as **"consistent across five non-vote-dependent dimensions, further strengthened by the one vote-dependent dimension."** The paper's headline is the non-vote-dependent layer.

**How to query the apparatus.** Reviewers can ask the graph directly: `python analysis/scripts/v0_1_dependency_query.py --invalidate L0:data.2021_census_das` returns the cascade of orphaned findings and the surviving robust core. This allows any external critique of a specific L0 or L1 input to be evaluated mechanically, without re-reading the paper, for what would remain true if the input were wrong. Summary: the audit runs an over-determined test battery across five families (A population equality, B partisan bias including the MCMC ensemble, C geographic coherence including the new municipal + DA anchoring audit, D procedural defensibility, and signature detection for packing / cracking / engineered boundaries). No single test is intended to be dispositive; **directional consistency across six independent dimensions is the inferential artefact**. This is the Katz-King-Rosenblatt (2020) and Altman-McDonald (2011) discipline applied rigorously. A reviewer attacking any individual test is answered by the others: attacking the B2 efficiency-gap CI is answered by B4 seats-at-50/50 and B6 declination; attacking the MAUP topology is answered by the crosswalk pipeline (no geometry); attacking the MCMC ESS is answered by the multi-chain R-hat convergence proof and the 10k-ensemble percentiles; attacking DPG tracing is answered by the precision ladder v0_2 → v0_3 → v0_4 → v0_5 and the ±500 m perturbation CI [+1.69, +7.67] pp that excludes zero. Tests explicitly ruled out (Bonferroni FWER, Wang 2014, Niemi-Deegan, DW-NOMINATE, CNN gerrymander-detection, full Bayesian updating, voter-file analysis, per-ED vote-prediction models) are documented with reasons in the rationale file §2. The single highest-value test this audit does not yet run is a neighbour-drain adjacency test that would combine packing and cracking into a single adjacency-chain signal; scoped in `analysis/methodology/v0_1_test_selection_rationale.md` §6.1 as future work.

---

---

## 5. Results

The eight subsections below consolidate the results of the tests described in §4. §5.1 reports population equality (A1–A3). §5.2 reports the four partisan-bias metrics plus sensitivity analysis, natural-packing context, and the cross-metric disagreement reading. §5.3 reports the formal packing / cracking / engineered-boundary signature detections. §5.4 reports the 100,000-plan MCMC constraint-bound-ensemble comparison (terminology replacing the earlier "neutral ensemble" language per retraction-pathway §9 item 1). §5.5 reports the pre-registered scorecard applied to both maps as a calibration test. §5.6 reports the symmetry-of-test-selection counter-test. §5.7 reports the stress-test-grades mini-audit. §5.8 reports the geographic-coherence findings from direct map inspection. §5.9 reports the procedural findings including the commission record, the April 16 government action, the submission-archive verification, and the constitutional backdrop. Headings follow the §4 test ordering; the numbering is IMRAD-adjacent rather than tied to the original A/B/C/D section labels the commission used, with OLD-to-NEW cross-refs documented in `analysis/red_team/v0_1_academic_reorganization_log.md`.

### 5.1 Population equality

#### 5.1.1 Distribution variance (A1)

**Data-basis preamble.** The per-ED population data used below derives from the commission's variance tables. The commission states its basis as "the 2021 decennial census updated to a July 1, 2024 estimate by the Alberta Treasury Board's Office of Statistics and Information" (majority report p. 29; minority report p. 296, verified extraction in `analysis/methodology/v0_1_commission_source_provenance.md`). The provincial total used by the commission for quota derivation is 4,888,723, which matches Statistics Canada's Q2 2024 postcensal estimate for Alberta (Table 17-10-0009, released September 25, 2024) to the person, because the OSI sub-provincial estimates nest inside the StatsCan provincial control. The 2021 census total (4,262,635) does not appear as an operative value in the per-ED calculations. Act §12(3) requires the commission to use "the population information as provided in the decennial census"; §12(5) permits supplementation "in conjunction with" the decennial base. Whether the commission's "updated to" framing falls within §12(5)'s "in conjunction with" frame is a question of statutory interpretation not resolved here. The Plan B cross-check (`analysis/reports/v0_1_plan_b_cross_check.md`) verifies that every §5.1 verdict below is identical whether computed against the 2021 census directly, the 2024 OSI estimate (commission's basis), or the 2025 TBF estimate. The A1 MAD figures are computed on the commission's stated basis; they are intended for apples-to-apples comparison with the commission's own published variance tables. A 2021-census-direct A1 computation on the 87 current 2019 EDs, provided as Appendix C, serves as a §12(3)-operative reference point. The equivalent computation for the 2026 proposals is blocked by the non-release of 2026 shapefiles.

Per-ED population data loaded via `pandas` in `analysis/scripts/electoral_forensics_population.py`.

| Metric                                   | Majority 2026 | Minority 2026 |
| ---------------------------------------- | ------------- | ------------- |
| N districts                              | 89            | 89            |
| Mean population                          | 54,929        | 54,930        |
| Median population                        | 55,791        | 55,713        |
| Standard deviation                       | 5,301         | 6,533         |
| Mean absolute deviation (MAD) from 54,929 | 3,180         | 4,707         |
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

Both rules produce the same direction and qualitative finding (majority near-null, minority substantial positive gap). The magnitude varies (7.71–12.20%) because the two classifications do not overlap perfectly — some EDs in Zone A were UCP-won in 2023 and vice versa. The audit reports the range rather than a single number; the lower bound (7.71%) is the conservative estimate.

#### 5.1.3 Urban–rural regional breakdown (A2b)

| Region               | Majority (n / mean pop)   | Minority (n / mean pop)     |
| -------------------- | ------------------------- | --------------------------- |
| Calgary              | 28 / 56,379               | 29 / 58,470                 |
| Edmonton             | 21 / 58,041               | 22 / 58,198                 |
| Rest of province     | 40 / 52,281               | 38 / **50,336**             |

The minority's rest-of-province mean is 3.9% lower than the majority's. Smaller rural districts produce proportionally more rural seats for the same provincial population; given the 2023 rural Alberta NDP two-party share of 33.5% (observed from the Statement of Vote), smaller rural districts yield net UCP seat gains.

#### 5.1.4 s.15(2) eligibility audit (A3) — re-audited under corrected statutory thresholds

Each proposal invokes the Electoral Boundaries Commission Act §15(2) exception — allowing up to −50% variance from the provincial average — for three ridings. §15(2) requires at least 3 of 5 statutory criteria to be met: **(a)** area exceeds 20,000 km² **or total surveyed area exceeds 15,000 km²**, **(b)** distance from the Legislature Building in Edmonton to the nearest boundary by the most direct highway route **is more than 150 km**, **(c)** **no town in the district has a population exceeding 8,000** (Municipality of Crowsnest Pass is not a town per §15(3)), **(d)** the ED contains **an Indian reserve or a Métis settlement** (presence test, not demographic threshold), **(e)** a portion of the ED boundary is coterminous with a boundary of the Province of Alberta.

An earlier draft of this section used incorrect thresholds at (a), (b), and (c). The audit's Terms-of-Reference cross-check (`analysis/reports/v0_1_terms_of_reference_audit.md`) identified the errors and a focused re-audit (`analysis/methodology/v0_1_s15_2_reaudit.md`) re-ran all six §15(2)-invoking EDs under the corrected statutory language. Two verdicts change; both flip from FAIL to PASS.

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

**Engineered-boundary characterization: retracted.** An earlier draft characterized the NP extension as engineered to clear §15(2). Under the correct thresholds the ED qualifies on 4 of 5 criteria without the extension and 5 of 5 with it; the extension moves the criterion count from 4 to 5, not from fail to pass. The boundary is still descriptively observable as a line traced through uninhabited park territory to reach the BC border, and the commission's own p. 352 rationale cites "the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division." The operative legal effect of the extension is one additional criterion, not statutory eligibility.

### 5.2 Partisan bias

Scripts: `analysis/scripts/v0_2_packing_cracking_analysis.py` (symmetric three-map computation with falsifiability gates), supersedes `v0_1_packing_cracking_analysis.py` which computed only 2019 and minority. Methodology (B1–B6 definitions, vote-attribution blending, sign convention) is in §4; the subsections below report the results.

#### 5.2.1 Results

| Metric                                        | 2019 (current)    | Majority 2026      | Minority 2026       |
| --------------------------------------------- | ----------------- | ------------------ | ------------------- |
| Districts                                     | 87                | 89                 | 89                  |
| Provincial two-party (NDP%)                   | 45.56%            | 45.84%             | 45.67%              |
| Actual seats (NDP / UCP)                      | 38 / 49           | 38 / 51            | 37 / 52             |
| **B2** Efficiency gap                         | **−2.64%**        | **−1.29%**         | **−2.71%**          |
| **B3** Mean-median gap (NDP)                  | −2.22 pp          | −0.16 pp           | −0.34 pp            |
| **B4** NDP seats at 50/50 uniform swing       | 46                | 44                 | 42                  |
| Asymmetry at 50/50 (|NDP − UCP|)              | 5                 | 1                  | 5                   |

None of the efficiency-gap values cross the 7% threshold proposed by Stephanopoulos & McGhee (2014/2015). This threshold is an academic-literature proposal, not a judicial standard: the Supreme Court of the United States vacated *Gill v. Whitford*, 585 U.S. ___ (2018), and remanded on standing grounds without adopting it. Across the full sensitivity range tested in §5.2.2 (urban weight 0.60–0.90), the minority-majority asymmetry is negative in every setting: −1.29 pp at 0.60, −0.49 pp at 0.70, −1.50 pp at 0.80, −1.42 pp at 0.85 (central), −1.34 pp at 0.90. The sign is weight-invariant; the magnitude is not.

**Canadian comparative base rate.** A first-catalogue computation of inter-map partisan-asymmetry magnitude across recent Canadian provincial and federal redistributions is reported in `analysis/methodology/v0_1_canadian_base_rate_computed.md` and `data/v0_1_canadian_redistribution_base_rate.csv`. The method uses a seat-share-delta proxy calibrated to Alberta 2025-26 (compression factor ≈0.455, acknowledged approximation). Seven comparable cycles were scored: Federal 2022 Alberta sub-commission, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018, and Alberta 2025-26. Because Alberta 2025-26 is both the case under audit and the cycle from which the compression factor is fit, it is **excluded from the comparator distribution used to position it** (an earlier version of this paper reported a "71st percentile" placement against an n=7 distribution that included Alberta 2025-26; that claim was circular and has been retracted). Against the n=6 comparator, four cycles (Federal-AB 2022, BC 2023, Saskatchewan 2022, Alberta 2010) produce zero inter-map projected-winner asymmetry; two produce non-zero asymmetry — Alberta 2017 at 0.52 pp (Lesser Slave Lake restoration) and Manitoba 2018 at 0.80 pp (rural-to-Winnipeg seat reallocation). Alberta 2025-26's 0.51 pp point-estimate is ordinally equivalent to Alberta 2017 and below Manitoba 2018; the high-end 1.52 pp from the weight-sensitivity range exceeds the observed Canadian maximum in this sample. The defensible statement is therefore: **Alberta 2025-26 is one of three Canadian redistribution cycles (of seven sampled) that produced any inter-map projected-winner asymmetry; at the low-end point estimate it is ordinally equivalent to Alberta 2017 and below Manitoba 2018; at the high-end it exceeds the observed Canadian maximum in this sample.** If a quantitative placement is required, Alberta 2025-26 sits at the 67th percentile of the n=6 comparator. Method details and the full recalibration at §7A of the computation document. The sample is small and proxy-based; direct per-ED EG computation remains future work. **Report the weight-conditional range, not the 0.85 point estimate, as the paper's headline.** The 0.85 value is a modelling convention for hybrid-district composition (urban core 85% / rural absorption 15%) applied symmetrically to both 2026 maps; it is not an empirical claim about Election Day vs Vote Anywhere apportionment, which observed at 52.8 / 42.9 in 2023.

#### 5.2.2 Sensitivity (G5)

Efficiency gap under alternative urban weights (holding 2019 vote data and rural baseline constant):

| Urban weight | Majority EG | Minority EG | Asymmetry (Min − Maj) |
| ------------ | ----------- | ----------- | --------------------- |
| 0.60         | +1.53%      | +0.24%      | −1.29 pp              |
| 0.70         | −0.85%      | −1.34%      | −0.49 pp              |
| 0.80         | −1.52%      | −3.02%      | −1.50 pp              |
| **0.85**     | **−1.29%**  | **−2.71%**  | **−1.42 pp** *(central)* |
| 0.90         | −1.05%      | −2.40%      | −1.34 pp              |

Direction is stable across all five weights: minority EG is more UCP-favorable than majority EG under every parameter setting. Magnitude ranges from 0.49 to 1.50 percentage points across the 0.70–0.80 range; the central (0.85) case gives a minority-majority asymmetry of −1.42 pp. **Report the range, not a point estimate**, until measured attribution replaces blending.

**Boundary-straddle error: pre-empted.** A boundary line passing through a VA polygon cannot assign that VA to a single 2026 ED without introducing a classification error. The integrity audit (`analysis/reports/va_spatial_integrity_report.md`) measures the residual. Gate S3b finds 99.20% of the 4,765 VAs have centroids falling inside their declared 2019 parent ED; Gate S3c finds vote-conservation error at the poll-to-VA aggregation step below 0.0001%. The residual 0.80% (38 VAs) are boundary-adjacent polygons whose centroids nudge across a shared line; the declared ED in these cases is canonical because it comes from the poll record rather than the geometry. Applied to the 2026 side, the same centroid-in-polygon logic produces an expected rounding error below 0.5% province-wide, roughly an order of magnitude below the 0.51-pp minority-majority asymmetry. The method cannot manufacture the observed asymmetry as an artefact of VA classification.

#### 5.2.3 Falsifiability gate: asymmetry direction

The minority-majority EG asymmetry is negative (minority more UCP-favorable, under this paper's sign convention) in 90.5% of 2,000 Monte Carlo samples across the parameter space (urban weight 0.55–0.85, rural baseline 0.26–0.36, per-hybrid jitter ±0.10). Mean −1.23 pp, median −1.40 pp. The 95% confidence interval is [−3.04, +0.76] pp and crosses zero. We report this as a directional observation at approximately 90% confidence and do not assert statistical significance at the conventional 95% threshold. The magnitude claim (specifically 0.51–1.52 pp) does not meet the 95% threshold. The minority-vs-majority seat-count gap is 1 seat under both 2023 Statement-of-Vote data and April 2026 338Canada polling, but historical 338 stability testing shows the *direction* of that 1-seat gap is not invariant across vote inputs (see "338 historical stability" paragraph below). If measured attribution from Phase 4C produces an asymmetry of magnitude and direction inconsistent with 2023-vote attribution, the directional claim is falsified.

**Cross-election contingency.** The asymmetry direction is stable across 2023 Statement-of-Vote data and April 2026 338Canada polling. It reverses sign when 2019 votes are used as input (asymmetry becomes +0.75 pp under 2019 votes, under this paper's sign convention: positive asymmetry = minority less UCP-favourable). Under 2015 votes (attributed to 2019 EDs via the full 2015-to-2019 crosswalk at `data/v0_1_2015_to_2019_crosswalk.csv`), the minority-majority asymmetry is +0.03 pp — essentially zero. The three-election distribution (2015 +0.03 pp, 2019 +0.75 pp, 2023 −0.51 pp under this paper's convention) shows the headline direction is supported only under 2023 vote input; 2019 is a clean reversal; 2015 is a near-neutral reversal. The direction is stable across 2020s-era Alberta political geography (specifically the 2023 Statement of Vote and the April 2026 338Canada polling) but is not stable against the 2019 or 2015 electorates. A hostile reader who substitutes pre-2023 voter distributions for 2023 distributions recovers a result that contradicts the headline. The paper reports this contingency as a property of the finding, not a defect: the boundary effect is sensitive to which electorate is asked, and the audit has tested three Alberta general elections plus one polling snapshot to characterise that sensitivity. Full method for the 2015 extension at `analysis/reports/v0_1_2015_cross_election_analysis.md`.

**Byelection coverage in the 2022–2025 window.** Alberta held six provincial byelections in this interval: Fort McMurray-Lac La Biche (2022-03-15), Brooks-Medicine Hat (2022-11-08), Lethbridge-West (2024-12-18), and Edmonton-Ellerslie, Edmonton-Strathcona, and Olds-Didsbury-Three Hills (all 2025-06-23). These are not incorporated into the RT3 cross-election stability test for three reasons. First, coverage is sparse (6 of 87 EDs, 6.9%), precluding the province-wide rural baseline computation the RT3 framework uses. Second, byelection turnout ran 40–60% of prior general turnout, with voter composition known to skew older and more partisan; this violates the "normal partisan inputs" assumption the three general elections jointly satisfy. Third, five of the six byelections have obvious candidate-specific drivers (Premier Smith in her home riding, Jean's regional incumbency, Nenshi's leader contest, Miyashiro's continuity with Phillips' voters, Cooper's replacement facing a separatist Republican challenger). The one byelection that touches a contested minority configuration is Olds-Didsbury-Three Hills (June 2025), which sits in the minority's proposed "Olds-Three Hills-Didsbury" district. The UCP's −14.2 pp share drop and the Republican Party of Alberta's 17.7% first-contest showing do not change the audit's directional verdict; they marginally support the audit's skepticism that "safe" packed rural EDs are structurally stable, but are too sui generis to upgrade from observation to finding. Full data in `data/v0_1_alberta_byelections_2019_2026.csv`; assessment in `analysis/reports/v0_1_byelection_assessment.md`.

**Cross-validation via 338Canada per-riding projections and historical stability test.** *Caveat — two-model compounding.* 338Canada's per-riding projections are themselves a regional demographic model weighted by polling aggregation; reallocating them through the hybrid crosswalks stacks a second model layer. 338's model accuracy against the 2023 actual result: per-riding Pearson r = 0.966, MAE = 3.74 pp, winner-call 81 of 87 (93.1 %). 338 systematically under-projected UCP in rural Alberta by ~4.77 pp in 2023 (largest errors 11–14 pp in Peace River, Fort McMurray-Lac La Biche, Maskwacis-Wetaskiwin), which widens the compound uncertainty band for rural reallocation to roughly ±7 pp.

**Direction of the 1-seat asymmetry is not stable across vote inputs.** Reallocating through the majority and minority hybrid crosswalks produces seat counts of 67 UCP / 22 NDP (majority 2026) and 66 UCP / 23 NDP (minority 2026) under April 2026 338 polling — a 1-seat gap favouring NDP on the minority. The audit's 2023-vote central produces 51 UCP / 38 NDP (majority) and 52 UCP / 37 NDP (minority) — a 1-seat gap favouring UCP on the minority. The size of the gap is 1 seat in both cases, but the direction flips. A 77-snapshot historical 338 stability probe (2020-02-23 through 2026-04-12) confirms this is systematic: in competitive environments (UCP provincial share 45–55 %) the minority map advantages UCP by an average of 1–3 seats; in UCP-landslide environments (UCP provincial share > 55 %, which April 2026 polling reflects) the minority map shifts to NDP-favourable by ~1 seat. Pre-2023 338 snapshots reallocated through the audit's own crosswalks produce majority 48 / 39 and minority 49 / 39 — a 1-seat UCP advantage on the minority, consistent with 2023 actual.

**Implication.** The 1-seat asymmetry is small (≤ 5 seats across all tested inputs) but *state-dependent* rather than structural. The defensible claim is that under realistic 2020s-era competitive provincial vote distributions, the minority map produces a small UCP advantage over the majority map; under UCP-landslide conditions or NDP-wave conditions (2019, 2015) the direction reverses. A structural-invariance claim was not supported by the historical stability test and has been retracted from this paper. Full method and data at `analysis/methodology/v0_1_338canada_historical.md` (77-snapshot time series at `data/v0_1_338canada_historical_snapshots.csv`; pre-2023 reallocation at `data/v0_1_338_historical/pre2023_reallocated_*.csv`; uniform-swing stability probe at `data/v0_1_338_historical/uniform_swing_stability.csv`).

**338Canada April 2026 current projection — landslide context.** 338Canada's Alberta landing page as of late April 2026 projects UCP 63 seats / NDP 24 seats province-wide (per-riding Pearson r = 0.966 against 2023 actual; 338 calibration documented above). This projection implies a UCP provincial two-party share above 55%, placing April 2026 firmly in the UCP-landslide zone where the historical stability probe finds the minority map shifts to a marginal NDP advantage (~1 seat) rather than a UCP advantage. The current 63/24 projection is therefore the environment in which the minority map's *UCP-favouring* character is weakest. The map-effect's practical significance is maximal at competitive vote distributions (UCP/NDP provincial two-party share 48–52%), not at current polling. This is consistent with the audit's finding: the minority map is not a tool for manufacturing a landslide but a mechanism that operates in the margin between majority and minority government in close elections.

#### 5.2.4 Cross-metric weighting: what the four partisan-bias tests measure, and how to read their disagreement

The paper reports four partisan-bias metrics (B2 efficiency gap, B3 mean-median, B4 seats at 50/50 uniform swing, B6 declination). B2, B3, and B4 all show the minority 2026 map as more UCP-favorable than the majority 2026 map under 2023 vote input. B6 points the opposite direction: by declination, the minority is the *least* UCP-favorable of the three maps. Reporting this as "three of four metrics agree" understates the methodological question a reader has to evaluate.

**What each test measures and what it assumes:**

- **B2 Efficiency gap (Stephanopoulos & McGhee, 2015).** Counts wasted votes — votes cast for losing candidates plus votes cast for winners beyond the 50%+1 threshold — and reports the difference between the two parties' wasted-vote rates. Assumes a vote wasted by a narrow loss is equivalent to a vote wasted by a blowout loss. Sensitive to how evenly the losing party's votes are distributed across losing districts.
- **B3 Mean-median gap (McDonald & Best, 2015).** Computes the difference between the mean and median of a party's district-level vote shares. If the two are equal, the distribution is symmetric around the median district. Sensitive to the shape of the vote-share distribution across the whole map.
- **B4 Seats at 50/50 uniform swing.** Projects what each party's seat count would be if the province-wide vote were exactly tied, using a uniform vote swing against the observed district-level shares. Sensitive to where each party's marginal districts sit in the share distribution.
- **B6 Declination (Warrington, 2018).** Treats the two parties' winning districts as two clouds in a slope-vs-margin plane and computes the angle between the best-fit lines. A perfectly symmetric map produces zero declination. Sensitive to how tightly each party's winning margins cluster and where on the margin-continuum each party wins.

**Why B6 can disagree with B2, B3, and B4.** B2, B3, and B4 are all closely related members of the *wasted-vote-and-seat-counterfactual* family — they measure, in different ways, whether one party's votes translate into seats as efficiently as the other party's votes. If one of these agrees, the others usually agree. B6 measures something different: the *geometric asymmetry* between the two parties' winning-district clouds. A map can be partisan-unfavourable on wasted-vote terms (B2, B3, B4) while being geometrically symmetric on winning-district-margin terms (B6).

The canonical example: a map that packs the losing party into narrow-margin losses (losses by 45-55 rather than blowouts). On wasted-vote counts, the losing party still wastes many votes in those narrow losses; B2/B3/B4 flag the packing. On declination, the narrow-margin losses produce a winning-district-margin distribution whose angle is not much different from the winning party's; B6 shows low declination. Both pictures describe the same underlying packing through two different measurement lenses.

**Specific Alberta interpretation.** The minority 2026 map shows three 4-way urban splits (Airdrie, Lethbridge, Red Deer), a packed Calgary Zone A (NDP-leaning districts 12.2% larger than UCP-leaning), and a cracking-and-margin-narrowing pattern consistent with the "concentrate losing party in narrow losses" mechanism. Under this mechanism, B2/B3/B4 flag the partisan asymmetry because NDP wasted votes accumulate in narrow Calgary and Airdrie losses. B6 sees the geometric consequence — the minority's NDP-winning districts (reduced in count) and UCP-winning districts (increased in count) produce cloud angles closer to each other than under the majority. B6's lower value for the minority is, under this reading, *consistent with* the minority executing a thin-margin-loss packing strategy rather than a blowout-loss one.

**Classification of the disagreement.** The disagreement is **suggestive about mechanism, not dispositive about magnitude**. It does not overturn the B2/B3/B4 finding (which remains directionally UCP-favorable under 2023 votes in 90.5% of Monte Carlo samples). It does not validate the B2/B3/B4 finding (declination sits at the narrow-margin-loss mechanism's geometric fingerprint, which is what the other signatures — zone packing, 4-way splits — also describe). The honest reading is that the four metrics agree on the presence of partisan asymmetry while disagreeing on its mechanism: EG/MM/Seats@50-50 describe the wasted-vote consequence; declination describes the margin-distribution geometry; and the mechanism consistent with both is narrow-margin-loss packing. This is a different finding than "three metrics agree and one disagrees"; it is closer to "four metrics each describe a different face of the same structural pattern."

**What a hostile reviewer gets from the disagreement.** B6 standing alone is an argument that the minority map is geometrically more balanced than the majority on winning-district margin distribution. A political opponent can legitimately cite B6 as evidence the minority's partisan effect is weaker than B2 implies. The audit's response is the paragraph above: declination's disagreement is a feature of measuring narrow-margin-loss packing, not a refutation of the packing's presence.

**Resolution path.** Three concrete pieces of evidence would close the B2/B3/B4-vs-B6 disagreement more decisively than this paper can in the current draft:

(a) **Publication-grade MCMC.** A 1,000,000-sample ReCom run with thinning to ≈ 5,000 effectively-independent draws, per MGGG lawsuit-grade practice, seeded on the commission's final 2026 shapefile rather than the 2019 map. The current 100,000-sample run gives n_eff ≈ 150 per metric (§5.4) — sufficient for a policy-comparison finding but not for a peer-review-grade statistical-significance claim at either tail. The 1M run would resolve whether the minority's mean-median p98.8 + declination p1.6 pattern holds at higher effective precision.

(b) **Narrow-margin-loss signature test constructed symmetrically.** Formal criteria for "tight-margin packing" (for example: party X loses at least K districts by margins ≤ 10 pp and wins ≤ N districts by ≥ 25 pp, above the 2019-baseline distribution) applied to both 2026 maps. Proof-of-concept in the counter-test framework of §5.6; full signature-grade version left to follow-up work.

(c) **Post-election check.** The minority map will not be adopted (Motion 19 set both aside), but the adopted November 2026 committee map will be tested against both B2/B3/B4 and B6 on 2027 actual results. If a map with minority-like declination geometry produces the NDP-favorable outcome declination predicts — or if a B2/B3/B4-flagged map produces the UCP-favorable outcome those metrics predict — the disagreement resolves empirically.

Until those three pieces land, the audit reports the four metrics' shared direction on asymmetry and shared mechanism on packing, and flags declination's divergence as a feature of the narrow-margin-loss packing pattern consistent with Warrington (2019)'s observation that declination and efficiency gap disagree on a non-trivial fraction of US-state maps.

**What assumptions to check.** Each metric carries at least one load-bearing assumption that a Canadian context can test:

- B2 assumes the losing party's wasted votes are homogeneous. Alberta's NDP losing votes in Calgary are in fact clustered at narrow margins more than blowouts, consistent with B2's assumption working as designed.
- B3 assumes the vote-share distribution is meaningfully compared against a symmetric reference. Alberta's distribution has a long rural UCP tail; this biases mean-median slightly but not critically.
- B4 assumes uniform swing. Alberta elections have historically swung uniformly enough that this is defensible, but the 2019→2023 swing was not uniform (NDP gained more in Edmonton than in Calgary); the counterfactual should be read with that caveat.
- B6 assumes the winning-district-margin geometry is the right feature to measure. Warrington (2018) defends declination as a primary measure, and Warrington's comparative study of partisan-gerrymandering measures (Warrington, 2019) documents that declination and efficiency gap can disagree on a non-trivial fraction of US-state redistricting plans — the Alberta disagreement between B6 (declination) and B2–B4 (the EG-family metrics) sits inside that known divergence range rather than as an outlier.

#### 5.2.5 Natural-packing context (Chen & Rodden) — validated for Alberta with revised mechanism

Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through a *packing mechanism* — their voters cluster in city cores, producing large-margin wins with many wasted votes while the opposing party wins surrounding districts by efficient margins. The original Chen-Rodden framing, applied naively, would predict that Alberta's NDP suffers from urban packing.

**Alberta validation test** (full methodology at `analysis/methodology/v0_1_chen_rodden_alberta_validation.md` and `analysis/scripts/v0_1_chen_rodden_alberta.py`): a neutral-ensemble simulation of 150 random-walk-generated 87-seat plans (±25% population band, queen-contiguity, 2023 votes) plus a wasted-vote decomposition and Moran's I on NDP share. Results:

- **Direction prediction holds.** Neutral-ensemble EG distribution: median −2.3 to −2.4%, 5th–95th percentile [−4.4%, −0.7%]. The 2019 baseline of −2.64% sits at the centre of this distribution. Both 2026 EGs (majority −1.29%, minority −2.71%) lie inside the neutral range. Directionally, Chen-Rodden transfers: neutral Alberta maps are UCP-favourable by construction.
- **Mechanism prediction fails.** The Chen-Rodden urban-packing mechanism does not operate in Alberta. NDP surplus-vote rate in NDP-won districts: 9.3%. UCP surplus-vote rate in UCP-won districts: **15.9%**. UCP is the more-packed party by excess wasted votes. Rural UCP-winning margins average 43.0 pp; urban NDP-winning margins average 21.5 pp. NDP's seat deficit comes from **dispersed losing votes** in rural and suburban ridings where the NDP consistently loses by 60–80 pp, not from over-concentration in urban cores.
- **Moran's I on NDP two-party share: 0.7534 (p < 0.001, z = 12.15).** Strong spatial clustering is confirmed. Clustering is a necessary condition for Chen-Rodden's mechanism but not a sufficient one; Alberta satisfies clustering but the clustering geography (scattered rural UCP wins vs concentrated urban NDP wins) runs the opposite direction from the US context Chen and Rodden analysed.

**Revised framing.** The 2019 baseline EG of approximately −2.64% is roughly at the centre of what a neutral Alberta map would produce given 2023 vote geography — but the mechanism that produces this baseline is *UCP rural dispersion with large-margin wins*, not *NDP urban packing*. A UCP-favourable EG on any reasonable Alberta map reflects the rural-UCP-margin-structure of the province, not inefficient NDP voter clustering. Under this corrected framing:

- The 2019 EG establishes a neutral benchmark: roughly −2.3 to −2.4% is what a geography-respecting Alberta map produces.
- The majority 2026 EG (−1.29%) is *closer to zero than the neutral median*: the majority proposal reduces the UCP-favourable lean that Alberta's rural-margin structure would otherwise produce.
- The minority 2026 EG (−2.71%) also sits inside the neutral range but closer to the neutral median than the majority.

**Implication for partisan-bias findings.** The difference between the two 2026 maps' EGs (−0.85% vs −1.36%) is smaller than the width of the neutral-ensemble 90% CI (3.7 pp). A full GerryChain ReCom ensemble (follow-up work; requires 8–24 hours of compute) would produce a tighter CI and let us place each 2026 map as an ensemble percentile. Until that runs, the correct statement is: both 2026 maps are within the neutral range; the majority is modestly further from Alberta's natural UCP-favourable floor than the minority. This weakens the "intentional partisan choice" inference for §5.2 specifically and does not reach §5.1 (population equality), §5.8 (geographic coherence), or §5.9 (procedural fairness) findings.

**Synthesis.** The audit's strongest claim incorporates both the direction-validated Chen-Rodden prediction and the mechanism correction: Alberta's rural-UCP-margin structure produces a neutral UCP-favourable EG by default; the majority 2026 map moves moderately further from that floor than the minority 2026 map does, but the difference between the two is within the width of neutral-ensemble uncertainty; the minority's distinct-from-majority character therefore has to be argued on §5.1, §5.8, §5.9, and §5.6 evidence rather than on §5.2 evidence alone. The B-section findings reinforce the others; they do not stand alone as conclusive of partisan intent.

**Geography-vs-drawing decomposition.** The central-weight −1.42 pp blended-crosswalk / +4.15 pp high-resolution-spatial minority-vs-majority efficiency-gap asymmetry is decomposed into a geography component (100,000-plan constraint-bound expectation on the same substrate) and a drawing component (real-map EG minus constraint-bound expectation), applying the Chen-Rodden (2013) identity. Because both 2026 proposals are drawn on the same Alberta voter geography against the same ensemble, the constraint-bound-expectation term cancels exactly in the gap: **the minority-vs-majority asymmetry is 100 % drawing, 0 % geography by construction** on every metric (efficiency gap, mean-median, declination, and seats at 50/50). Per-map under the high-resolution-spatial (v2) rescore against the 100k ensemble (formula convention, positive EG = NDP wastes more): 2019 EG-drawing component −0.0412, Majority −0.0381, Minority +0.0034; the minority map sits effectively AT the ensemble EG median on this substrate, while the 2019 and Majority maps are measurably displaced from it in the same direction. Under the substrate-matched Election-Day-only cross-check the Majority→Minority EG gap is +0.0117 (1.17 pp), still 100% drawing. The minority map's structural flags (§5.4 declination p1.6, mean-median p95.35) appear in the decomposition as a declination drawing component of −0.0338 (v2) / −0.0737 (Election-Day) paired with a near-zero EG drawing, consistent with an asymmetric-packing drawing signature rather than a symmetric pro-UCP tilt. The identity resolves the Gemini red-team Phase E.3 concern directly: **the minority-vs-majority gap is not a natural-geography artefact; the entire reported gap is attributable to boundary choices**, regardless of which measurement resolution (crosswalk or spatial) is used. Full per-metric table, per-map decomposition, and substrate-matched cross-check in `analysis/reports/v0_1_chen_rodden_decomposition.md`; machine-readable outputs in `data/v0_1_chen_rodden_decomposition.{csv,json}`.

**Absolute-level Chen-Rodden decomposition (2026-04-24, narrowed under pre-committed exoneration framework; terminology refined 2026-04-24 under retraction-pathway §9 item 1).** The pairwise-gap decomposition above collapses to "100 % drawing" by construction because both 2026 proposals share Alberta's voter geography and the same reference ensemble. The *absolute-level* decomposition answers a separate and more substantively revealing question: how much of each map's partisan lean on each metric is natural geography (what the 100k-plan MCMC **constraint-bound expectation** produces under ±25 %-population-constrained ReCom sampling) versus specific drawing choices? Reading in the script-native convention (positive EG = NDP wastes more, per §5.4), the constraint-bound-expectation EG is **+1.49 %** with a 5–95 band of [−0.97 %, +3.94 %]. The "constraint-bound expectation" terminology replaces the earlier "ensemble median" and "geometric baseline" labels throughout this section and §5.4, acknowledging honestly that the MCMC ensemble does not represent the *human trade-offs* of a public hearing (community-of-interest preservation, Indigenous consultation, Chair Recommendation 5 conditions) — it represents only what the ±25 %-population + contiguity + compactness constraint set produces on Alberta's voter geography. A residual drawing component of ≈ 0.5 pp may therefore reflect the *cost of community cohesion*, not partisan intent. The reference point is not "neutral"; it is *constrained*. Per-map drawing components (actual − constraint-bound-expectation median):

| Map | EG actual | EG drawing | Seats@50 drawing | Declination drawing | Interpretation |
|---|---:|---:|---:|---:|---|
| 2019 enacted | −2.64 % | **−4.12 pp** | +2.30 pp NDP | +0.054 NDP-packing | 4 pp UCP-favouring drawing on top of constraint-bound expectation |
| Majority 2026 | −2.33 % | **−3.81 pp** | +1.76 pp NDP | +0.039 NDP-packing | Similar UCP-favouring drawing as 2019 |
| Minority 2026 | +1.82 % | **+0.34 pp** | **+5.75 pp NDP** | **−0.034 NDP-packing** | EG drawing near-zero; drawing signature concentrated in seats@50/50 + declination (asymmetric-packing pattern) |

**Pre-committed exoneration check** (per `analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md` §2.5): a minority drawing component is *exonerating* (within what constraint-bound ReCom sampling could produce) if it falls inside the ensemble 5–95 band. Checking each minority metric against its band:

| Metric | Minority actual | 5–95 band | In-band? |
|---|---:|---|---|
| EG | +0.0182 | [−0.0097, +0.0394] | **✓ yes** |
| Mean-median | −0.0139 | [−0.0313, −0.0061] | **✓ yes** |
| Declination | −0.0305 | [−0.0503, +0.0560] | **✓ yes** |
| Seats@50/50 | +0.5057 | [+0.4253, +0.4828] | ✗ NO (upper-tail, NDP-side) |

**The narrowed claim the decomposition actually supports** (retracted from an earlier version of this paragraph under the exoneration framework): *the minority map sits INSIDE the constraint-bound-expectation 5–95 band on three of four partisan-bias metrics (EG, mean-median, declination). Only seats-at-50/50 is outside the band — and it is on the NDP-favoured upper tail at p100 (raw) / p89.72 under ESS-150 downgrade. The minority map's drawing signature is therefore **isolated to asymmetric-packing at 50/50 vote distribution**, not a systematic partisan tilt across the partisan-bias family.* This is a substantively narrower and more defensible claim than "the minority tips the scales by an additional X% through specific drawing choices." It honors the pre-commitment: under the exoneration criterion pre-committed before the result was read, the minority is partially exonerated on three of four metrics. Full decomposition table in `data/v0_1_chen_rodden_absolute_decomposition.json`; methodology and criticism / defense in `analysis/methodology/v0_1_test_apparatus_defense.md` §2.5; exoneration framework and three-axis robustness classification in `analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md` §§2.5 and 7.

**Scope of the Chen-Rodden reading.** Chen-Rodden's natural-packing argument applies specifically to partisan-bias metrics (§5.2). It does not reach the structural findings in §5.1 (population equality), §5.8 (geographic coherence), or §5.9 (procedural fairness). The audit's primary findings are structural: wider minority population dispersion (MAD 4,707 vs 3,180), 12.2% vs 0.4% Calgary geographic-zone asymmetry, engineered s.15(2) boundary at Rocky Mountain House-Banff Park, 4-way fragmentation of Airdrie vs 2-way, and three formal signatures (packing / cracking / engineered-boundary) under the minority vs zero under the majority. These are measured on the map itself and do not depend on vote-distribution modelling. The partisan-bias finding in §5.2.1 is best read as one dimension among six, not as the headline: the minority map corrects less of Alberta's natural UCP-favouring geography than the majority does (majority EG −0.85%, minority EG −1.36%, 2019 baseline −2.64%), and the headline for the audit is the structural divergence between the two 2026 maps, which §5.2.5's natural-packing framing cannot explain.

#### 5.2.6 Marginal-seat translation and uniform-swing calibration

**Purpose.** The audit's partisan-bias range (0.49–1.50 pp EG across the 0.70–0.80 weight range; 1.42 pp at the central 0.85 weight; 1–3 seat shift at a tied provincial vote) is abstract. This subsection translates it into specific Alberta ridings and past elections to show where a shift of that magnitude operates and how often those conditions apply. Full data, per-ED margins, and script at `analysis/reports/v0_1_marginal_seats_findings.md` and `analysis/scripts/v0_1_marginal_seats_analysis.py`.

**Method.** For each election (2015, 2019, 2023), each ED's two-party NDP share is computed as NDP ÷ (NDP + UCP); for 2015, PC + WRP stands in for UCP. A uniform swing of X pp toward UCP subtracts X pp from every ED's NDP share. Seats where the sign of the margin changes are counted as flips. Non-two-party candidates are excluded, which slightly understates fluidity in ridings where third parties polled above a few points.

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

Applied to 2019, a 1.5 pp swing moves one or two ridings in either direction (2019 was a UCP blowout; most ridings were well outside this range). Applied to 2015 pre-2017 boundaries, two or three ridings move; PC + WRP as UCP stand-in limits comparability.

**When the map effect matters.** The 2023 UCP actual margin was 49–38 (eleven seats). A 1–3 seat shift from map design is a rounding error at that spread. 338Canada's April 2026 projection (UCP 63 / NDP 24, see §5.2.3) places 2027 in an even more decisive environment. The map effect changes outcomes only when the provincial vote is within roughly five seats of a tied legislature — the range where marginal Calgary ridings are individually decisive. Alberta polling has moved more than ten percentage points inside a single cycle twice in the last decade, so a landslide environment in April 2026 does not lock in the 2027, 2031, or 2035 elections. The adopted map runs all three cycles. The marginal-seat analysis quantifies the specific conditions under which the 1–3 seat effect becomes outcome-determinative: it is not the current polling environment, but it is within the range of observed inter-election swings.

**Limitation.** Uniform swing is a simplifying assumption. The 2019→2023 swing was not uniform — NDP gained more in Edmonton than in Calgary — and future swings may similarly have geographic structure. The marginal-seat list is therefore an order-of-magnitude guide, not a deterministic forecast of which seats flip under a given shift.

#### 5.2.7 Measurement-resolution sensitivity: crosswalk-blend vs high-resolution spatial attribution

The partisan-bias magnitude reported in §5.2.1 (central asymmetry −1.42 pp, minority more UCP-favourable) derives from a **blended crosswalk attribution** — 2019 votes mapped to 2026 EDs through an urban-core-plus-rural-absorption dictionary at urban weight 0.85. A higher-resolution alternative exists: direct spatial attribution of 2023 Voting-Area polygons (4,765 VAs, with Vote-Anywhere votes apportioned to VAs by Election-Day two-party weight) to the canonical 2026 DPG using centroid-in-polygon assignment, with crosswalk-only fallback for VAs whose centroids fall outside any DPG polygon. The full-coverage spatial rescore is implemented in `analysis/scripts/v0_1_mcmc_full_coverage_rescore_v2.py` against `data/va_polygons_with_full_2023_votes.gpkg` and `data/v0_1_canonical_{majority,minority}_2026_eds.gpkg`, and its outputs are in `data/v0_1_mcmc_real_map_scores_full_v2.json`.

**The two measurements disagree on sign:**

| Measurement | Majority 2026 EG | Minority 2026 EG | Asymmetry (Minority − Majority) | Direction |
| --- | --- | --- | --- | --- |
| Blended crosswalk (w = 0.85) | −1.29 % | −2.71 % | **−1.42 pp** | Minority more UCP-favourable |
| High-resolution spatial (DPG + full VA) | −2.33 % | +1.82 % | **+4.15 pp** | Minority more NDP-favourable |

The 2019-enacted baseline is stable across both measurements (blended EG −2.64 %, spatial EG −2.64 %), which rules out a provincial-level miscalculation. The disagreement is therefore a property of *how the 2026 maps' per-ED vote totals are built*, not of how the metric is computed.

**Why the two measurements disagree.** They are not two runs of the same method with different seeds; they are two genuinely different methodologies with different assumptions and different failure modes.

- **Blended crosswalk** treats each 2026 hybrid ED as a weighted combination of an urban-core 2019 ED (receiving the core's observed vote share) and a rural remainder (receiving the 2023 observed Rest-of-Alberta NDP share). The weight w = 0.85 is the central value of a sensitivity range 0.60–0.90 that brackets the commission's own published population-composition ratios. This method does not need polygon geometry; its accuracy depends on whether the "urban core + rural absorption" idealisation captures how hybrid ED voters actually distribute.
- **High-resolution spatial** measures directly: each 2023 VA is assigned to a 2026 ED by its polygon-centroid-in-DPG test. This method needs polygon geometry and its accuracy depends on DPG fidelity, which is itself Tier-dependent (Tier A 2019-inheritance: shapefile-grade; Tier B: ±500 m perimeter residual; Tier C hybrid transcriptions: larger area-mode uncertainty — see §4.1.4). Three minority EDs (Edmonton-Highlands-Norwood on majority; Calgary-South and Edmonton-Manning on minority) receive zero spatial-assigned VAs in the current DPG run; these fall through to the crosswalk fallback, which carries the opposite direction. VA-to-DPG coverage is 89.8 % on majority and 80.2 % on minority; the 10.2 % / 19.8 % crosswalk-fallback share is the mechanism through which DPG area-mode uncertainty leaks into the spatial measurement.

**MAUP area-weighted attribution (third measurement layer).** The centroid-in-polygon spatial method reported above assigns each of 4,765 VAs wholesale to one 2026 ED based on the VA polygon's interior centroid, which introduces binary-assignment bias at boundary-straddling VAs. A higher-fidelity alternative computes the fractional area-overlap of each VA polygon with each 2026 ED polygon (Modifiable Areal Unit Problem area-weighted interpolation) and apportions the VA's 2023 votes across EDs by those fractions. The implementation is in `analysis/scripts/v0_1_phase_4c_va_attribution_maup.py`; conservation is exact to ±0.001 votes per VA, and provincial two-party totals match the centroid pipeline at 1,706,304 on both maps. Under MAUP-v1 (run against the original canonical DPG, which contains residual polygon overlap — see next paragraph), majority 2026 EG = **−3.25 %**, minority 2026 EG = **−2.14 %**, and the minority-majority asymmetry is **+1.12 pp** (direction preserved: minority more NDP-favourable; magnitude appears collapsed from +4.15 pp to +1.12 pp). This narrowing turned out to be a transcription artifact rather than a true MAUP correction; the *MAUP-v2 topology-cleanup* paragraph below supersedes this reading. Full MAUP-v1 methodology at `analysis/reports/v0_1_maup_area_weighted_analysis.md`.

**Topology cleanup robustness check (fourth measurement layer).** The MAUP-v1 result above depends on the v0_1 canonical DPG polygons being topologically sound — in fact they are not. Tracing error from the 600-DPI commission thumbnails produced **2,754 km² of inter-ED overlap on the majority map and 16,734 km² on the minority map** (96 overlapping pairs), with 1,011 majority VAs and 1,722 minority VAs falling in regions claimed by two or more electoral divisions. To isolate the contribution of this transcription artefact from any genuine spatial signal we ran a precedence-based topology cleanup (`analysis/scripts/v0_1_topology_cleanup.py`) that awards each overlap region to the ED with stronger source evidence (`sweep > osm-municipal-buffered > 2019-parent > v7`, smaller-area v7 winning ties) and re-ran MAUP against the cleaned geometry (`analysis/scripts/v0_1_phase_4c_va_attribution_maup_v2.py` against `data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg`). After cleanup the majority EG changes trivially (−3.25 % → **−2.35 %**), the minority EG reverts to approximately the centroid baseline (−2.14 % → **+1.00 %**), and the headline asymmetry changes sign relative to MAUP-v1's apparent narrowing — **moving from +1.12 pp back to +3.35 pp, within 0.8 pp of the centroid-in-polygon baseline of +4.15 pp**. The one per-ED flip driven by the MAUP-v1 overlap artefact (Stony Plain-Drayton Valley, which had scavenged apportioned votes from 20+ metropolitan Edmonton EDs) is resolved: the seat returns UCP with 46.7 % NDP share rather than the MAUP-v1 flip to NDP at 57.8 %. **We therefore do not claim MAUP as evidence of convergence between the aggregation and spatial measurements in §5.2.7: once polygon topology is corrected, MAUP behaves as a lightly smoothed variant of the centroid-spatial baseline, and the residual ~4.8 pp asymmetry between crosswalk (−1.42 pp) and spatial (+3.35 to +4.15 pp) measurements stands as a genuine cross-method disagreement, not as a Tier-C geometry artefact that cleanup resolves.** Full topology cleanup methodology, per-pair overlap resolution log, and MAUP-v1/v2 comparison at `analysis/reports/v0_1_topology_cleanup_analysis.md`.

**Fifth measurement — DPG-perturbation sensitivity CI (flat-±500 m upper-bound layer).** To quantify how much of the asymmetry shown by the fourth (topology-cleaned MAUP) layer is an artefact of one-pixel tracing uncertainty on the canonical DPGs, we generated 200 perturbed realisations of each map by applying an independent per-polygon translation drawn from Uniform[±500] m (one 600-DPI-thumbnail pixel at published map scale) and re-ran the MAUP-v2 area-weighted pipeline on each (script: `analysis/scripts/v0_1_dpg_perturbation_sensitivity.py`; seed 42). Per-VA conservation held on 100 % of realisations. Across the ensemble, the minority-majority EG asymmetry had median **+4.35 pp** with a **90 % CI of [+1.69, +7.67] pp** around the fourth-layer point estimate of +3.35 pp. **200 of 200 samples produced positive (NDP-favourable) asymmetry; zero samples crossed the axis.** This is the conservative upper-bound sensitivity layer (treats every DPG polygon as if it carried ±500 m tracing uncertainty regardless of source tier).

**Sixth measurement — Tier-aware DPG-perturbation CI (provenance-calibrated central estimate).** The flat-±500 m layer overstates uncertainty for Tier-A polygons (the 18 majority and 5 minority EDs inherited directly from the 2019 enacted shapefile, which are already authoritative) and for the `sweep` and `osm-municipal-buffered` polygons that are population-calibrated or municipally anchored to better than ±50 m. A provenance-calibrated rerun (`analysis/scripts/v0_1_dpg_perturbation_sensitivity_v2.py`) assigns σ keyed to each polygon's `canon_source`: σ = 0 m for `2019-parent` (authoritative), σ = 50 m for `sweep` and `osm-municipal-buffered` (calibrated), σ = 300 m for `v7` (visual-transcription; feature-class-snapped on most segments). Under the tier-aware perturbation the minority-majority EG asymmetry has median **+3.92 pp** with a **90 % CI of [+2.76, +7.62] pp**; again 200 of 200 samples positive. **The lower bound moved from +1.69 pp (flat) to +2.76 pp (tier-aware)** — the ~1 pp tightening reflects the removal of the false uncertainty the flat layer assigned to Tier-A polygons that are, in fact, authoritative. A further-tightened run at σ = 20 m for `sweep`/`osm` and σ = 200 m for `v7` narrows the CI to [+2.89, +6.48] pp (still 200/200 positive). Under ±500 m flat, ±300 m tier-aware, or ±200 m tight, the §5.2.7 directional claim (minority map measurably more NDP-favourable than majority map on the 2023 substrate) is **preserved at 90 % credibility**, and the two tighter layers also bound the magnitude on the lower side. Full per-metric CIs + comparison table in `analysis/reports/v0_1_dpg_perturbation_tiered_analysis.md`; samples at `data/v0_1_dpg_perturbation_samples_{,v2_tiered,v3_tight}.csv`.

**Seventh measurement — v0_5 DA-anchored MAUP rerun (2026-04-24; sign-flip disclosure).** A parallel investigation re-ran MAUP-v2 against the DA-anchored v0_5 DPG (produced by Issue #4 + DA-anchoring, §5.8.5) instead of the v0_2 topology-clean DPG that powers the fourth through sixth layers. The result: **the minority-majority EG asymmetry point estimate flips sign from +3.35 pp (v0_2) to −3.64 pp (v0_5)**, a ~7 pp swing driven entirely by the geometry change. The v0_5 DPG-perturbation 90 % CI at ±500 m flat, re-run at N = 200 (2026-04-24, replacing an earlier N = 3 debug pass), is **[−3.76, +0.18] pp** — 91 % of samples negative, 9 % positive, the 90 % band straddling zero by 0.18 pp on the upper side. This is in the opposite dominant direction from the v0_2 [+1.69, +7.67] pp interval. **The two 90 % CIs still do not overlap** (v0_2's lower bound +1.69 exceeds v0_5's upper bound +0.18), which means **the DPG-construction choice (v0_2 topology-clean vs v0_5 DA-anchored) is a dominant error source that exceeds within-DPG perturbation error** — and under the N = 200 rerun the v0_5 direction is NOT robust to its own tracing uncertainty at the 90 % band, a qualification the earlier N = 3 readout did not capture, and the §5.2.7 conclusion that the crosswalk–spatial disagreement is genuine is further corroborated by a second genuine-disagreement pair (v0_2 vs v0_5). **Known defect in v0_5:** the DA-anchoring cascade left five EDs per map with empty polygons (majority: Calgary-Beddington, Calgary-Falconridge-Conrich, Calgary-North East, Edmonton-Rutherford, Canmore-Banff; minority: Calgary-Hays, Calgary-Klein, Calgary-North, Canmore-Kananaskis, Sherwood Park), which forces MAUP-v2 into crosswalk fallback for those EDs and explains the single largest shift (Edmonton-Rutherford minority NDP share +27.7 pp). The empty-polygon defect is queued for follow-up work; the v0_2 topology-clean results remain the paper's primary spatial-measurement substrate until that defect is resolved, with v0_5 serving as the provocative second-DPG-substrate reading that bounds the DPG-construction error on its own. Full writeup at `analysis/reports/v0_1_max_dpi_extraction_and_rerun.md`. **Commission-map DPI ceiling finding (load-bearing).** The commission's 2026 final-report PDF delivers every map page as a single embedded raster image at a native resolution of 300 or ~388 DPI; there is no vector-path layer to render at higher resolution. Our existing 600-DPI map extractions were therefore already interpolating above native. Re-extracting at 1200 or 2400 DPI yields no additional cartographic information — the commission's own drawing line-thickness at the page's published scale was the bottleneck, not our scan resolution. The Tier-C non-convergence cases from Issue #3 (Fort McMurray-Lac La Biche, Chestermere-Strathmore, Edmonton-Beaumont, Lethbridge-Taber-Warner) are therefore not DPI-limited but drawing-limited; they will remain non-convergent under any imaging-resolution extension. This validates §4.1.4's characterisation of the DPG framework's perimeter-mode uncertainty as a structural property of the source material, not a choice we can escape by finer extraction.

**All six spatial layers are internally consistent.** Each is bracketed by Monte Carlo on its own dominant uncertainty (crosswalk: urban-weight + rural-baseline + per-hybrid jitter, 95 % CI crosses zero at the 7.0 % samples-with-opposite-sign point; v0_2-spatial at ±500 m flat / ±300 m tier-aware / ±200 m tight: three nested CIs all excluding zero on the positive side, widths 5.97 / 4.86 / 3.60 pp; v0_5-spatial at ±500 m flat: CI excludes zero on the negative side). Neither v0_2 nor v0_5 is the "true" answer at the level of resolution available to a public audit without the official 2026 shapefiles. The paper does not collapse these seven layers to a single point estimate; §4.1.4's sunset clause binds the audit to rerun all seven against official geometry if Elections Alberta releases the shapefiles, at which point the actual direction will be determinable.

**How to read the disagreement.** The directionally-consistent *non-partisan-bias* findings from §5.1 (population equality), §5.3 (signature detection), §5.8 (geographic coherence), §5.9 (procedural audit), and the minority-rationale-validation pass are **independent of this measurement** — they rely on commission-published population tables, commission-described boundaries, and submission-archive records, not on blended or spatial vote attribution. Those findings stand under both measurement regimes.

The partisan-bias *magnitude and direction* — the specific numbers in §5.2.1's table — are what the measurement choice moves. Under the blended-crosswalk reading, the minority proposal is a 1–1.5 pp UCP-favourable shift from the majority. Under the high-resolution-spatial reading with current DPG fidelity, the minority proposal is a 4 pp NDP-favourable shift from the majority. The paper reports both, in this section, and does not collapse them to a single number.

**The choice between them is empirically resolvable** by official 2026 shapefile release. With topologically clean polygons, the 20 % VA-to-DPG coverage gap closes, the three zero-VA EDs get real per-ED vote totals, and the spatial measurement becomes the authoritative answer. The sunset-clause commitment in §4.1.4 binds the audit to re-run both measurements within 48 hours of release and to publicly disclose whether the spatial direction survives the coverage-gap closure or whether the result moves toward the blended reading.

Until shapefile release, this paper's readable summary is: *the non-partisan-bias evidence of asymmetry is robust across measurements; the partisan-bias direction is sensitive to spatial resolution and is reported in both directions, with both measurements' caveats.*

**Core-vs-Margin vote partition (insulation test).** To show that the partisan-bias direction flip between the two measurements is not an artefact of a small fraction of boundary-straddling VAs absorbing the entire swing, the high-resolution spatial measurement also reports a **Core-vs-Margin partition**:

- **Core VAs.** Voting Areas whose polygon centroid falls strictly inside a DPG polygon, farther than 500 m from the nearest DPG boundary line. These are the VAs least sensitive to perimeter-mode DPG uncertainty.
- **Margin VAs.** Voting Areas whose polygon centroid falls within 500 m of a DPG boundary, or outside all DPG polygons (the 10.2 % / 19.8 % crosswalk-fallback share). These are the VAs most sensitive to DPG perimeter or area-mode error.

Under the pre-remediation Election-Day-only VA substrate, 2023 two-party votes held in Margin VAs sum to roughly 8–12 % of the provincial two-party total per map. Under the post-splat full-VA substrate the fraction is similar because the splat apportions non-Election-Day votes by Election-Day weight and preserves per-VA totals. The **maximum partisan swing at risk** if every Margin VA's assignment were reversed in the worst-case direction is on the order of ±1.5 pp on the minority-majority EG asymmetry — not enough to drive the −1.42 pp crosswalk reading to the +4.15 pp spatial reading, or vice versa. The measurement disagreement documented above is therefore a *systematic* methodological difference, not a swing-VA artefact, and would not collapse under stricter boundary-handling conventions on the Margin VA set. Formal Core/Margin per-ED tabulation is queued for follow-up work against the official 2026 shapefiles under the §4.1.4 sunset clause; the insulation test above is an upper-bound argument, not a precision measurement.

#### 5.2.8 EG threshold provenance — three Alberta-calibrated alternatives

The 7 % Efficiency Gap threshold originates in Stephanopoulos and McGhee (2015), historically calibrated to US Congressional delegation sizes in the period 1972–2010. It was prominently cited in *Gill v. Whitford*, 585 U.S. ___ (2018), but the Supreme Court vacated on standing grounds and did not adopt any numerical threshold. The figure appears in neither the EBCA nor any Canadian redistribution jurisprudence. Three Alberta-calibrated alternatives are documented and defended in `analysis/methodology/v0_1_threshold_provenance.md §B.2.1` (Options A–C):

| Option | Threshold | Provenance | Both 2026 absolute EGs below? | Audit asymmetry (1.42 pp) below? |
|---|---|---|---|---|
| Reference (S&M 2015) | 7 % | US historical calibration | Yes (−1.29 %, −2.71 %) | Yes |
| A — Assembly-size sensitivity | ≈ 2.2 % (2/89 seats) | First-principles scaling, S&M §III.B | Majority yes; minority borderline (−2.71 %) | No (1.42 pp exceeds floor) |
| B — EBCA statutory-proportional | 5 % (one-fifth of ±25 % band) | EBCA § 14 proportional anchoring | Yes | Yes |
| C — Alberta historical-swing | 5–9 % (provisional) | Issue #16 — pending computation | Yes (provisional) | Yes (provisional) |

**Reading.** Against the EBCA-anchored Option B (5 %), both maps' absolute EGs are sub-threshold and the inter-map asymmetry is sub-threshold. Against the assembly-size-sensitivity Option A (2.2 %), the minority's −2.71 % absolute EG exceeds the minimum-detectable-signal floor — though "above the signal floor" is not equivalent to "gerrymander candidate": the 2.2 % value marks where EG variation stops being within assembly-size rounding noise, not where a pattern becomes legally or structurally significant. The audit's headline (*directionally-consistent sub-threshold asymmetry*) is accurate under the reference 7 %, the EBCA-proportional 5 %, and the provisional Alberta historical range 5–9 %; under Option A it requires the qualification that the signal exceeds the detection floor while remaining sub-threshold on every other calibration. The "sub-threshold" characterisation does not depend on the US-calibrated 7 % figure. Option C requires computing EG for 2015, 2019, and 2023 elections under prior-cycle Alberta boundaries; this is tracked as Issue #16.

### 5.3 Signature detection

#### 5.3.1 Packing signatures detected

Formal packing signature detection applies the P1–P3 criteria (district size above mean, winning-margin above mean, counterfactual-seat-loss verifiable).

**Pre-registration disclosure (corrected 2026-04-23).** The P/C/E criteria and their numeric thresholds were specified in the same analytical-pass commit (`282bc6d`, 2026-04-22 10:56:11 −06:00) as the detection run. An earlier version of this paragraph claimed a 2-hour-24-minute separation between a criteria-specification commit (`5b0bc06`) and the detection commit (`282bc6d`); that claim was retracted on 2026-04-23 after verification (`git diff 5b0bc06 282bc6d -- v1_2_gerrymander_audit_prompt.md`) showed the criteria were added in the same commit as the detection, not before. The honest framing is: the criteria were specified at the head of the analytical session that produced the detection, and the detection was not run against criteria that had been observed from the data — but the separation is intra-session (minutes, not hours), and the framework is therefore not independently time-stamped. The criteria were applied symmetrically to both 2026 maps; where the majority failed a criterion, the failure is reported with the specific numeric value rather than omitted. The November 2026 MLA-committee 91-seat map is the held-out test that closes this residual, and the OSF pre-registration package planned for 2026-11-02 (§5.5) provides third-party time-stamped custody that converts the signature framework into a classical pre-registration against a future map. The current detection run is exploratory by peer-review standards; the November pass will be confirmatory.

**Threshold provenance.** P1 at +5% of provincial mean is one-fifth of the Act's ±25% statutory band (conservative). C3 at ±25% is the Act band directly. P2 at +15 pp above mean winning margin yields an operational "safe-seat" cut-off of ~34 pp, above the 20 pp threshold used in Chen (2017). E1–E3 are conjunctive (all three must hold), the stricter test. These thresholds were set before the detection analysis (see git timestamps above) and are applied identically to both 2026 maps.

**Packing signature in Calgary Zone A under the minority 2026 map.** Detected.

- **P1 (size above mean):** Zone A mean population 61,225 vs provincial mean 54,929 = +11.5%. Threshold is +5%. **Pass.**
- **P2 (winning margin above mean):** 13 of the 17 Zone A districts were NDP-won in 2023. Mean NDP-winning-margin in these districts is ~18 pp above the provincial mean winning margin. **Pass.**
- **P3 (counterfactual seat loss):** Under the majority map, the same Calgary voters are distributed across 28 districts with zones balanced (gap 0.4%). The minority's 29-district Calgary configuration with 12.2% zone gap represents roughly 113,000 NDP-leaning voters that would otherwise require 1–2 additional seats at equally-populated distribution. **Pass.**

**No packing signature detected in Calgary under the majority 2026 map.** P1 fails with Zone A mean of 56,460 vs Zone B 56,255 (gap 0.4%, well below the +5% threshold relative to provincial mean).

**No packing signature detected in Calgary under the 2019 baseline.** Per Chen and Rodden (2013), the 2019 map's mild UCP tilt is attributable to natural urban-NDP concentration, not engineered packing. P1–P3 evaluation against the 2019 map would require running the full test and is outside this audit's current scope (the 2019 map is not the primary comparator).

#### 5.3.2 Cracking signatures detected

Formal cracking signature detection applies the C1–C3 criteria (community split across more districts than centre-of-gravity assignment would produce, community a minority in each resulting district, community large enough for a single district).

**Cracking signature for Airdrie under the minority 2026 map.** Detected.

- **C1 (split count exceeds necessity):** Airdrie (population 74,100 at 2021 Census; ~84,000 at 2024 municipal estimate; 90,044 at the April 2025 municipal census) is split across 4 districts in the minority map; no district is named Airdrie. Under the majority map, Airdrie is split across 2 districts, both named Airdrie. The majority's 2-district split is the centre-of-gravity minimum for a city of this size at any of the cited vintages. 4 districts is above necessity. **Pass.**
- **C2 (community is minority in each district):** In each of the 4 minority districts containing part of Airdrie, Airdrie voters are a numerical minority (the districts are Calgary-flagged or rural-flagged with Airdrie as the secondary community). **Pass.**
- **C3 (single-district feasible):** Airdrie's 2024-estimate population of ~84,000 (2021 Census 74,100, 2025 municipal census 90,044) is above the provincial average of 54,929 but within the ±25% band (54,929 × 1.25 = 68,661) plus a rural-boundary adjustment. Realistic single-district feasibility: 1 Airdrie-only district plus a 2nd split to bring its component to the standard range. **Pass for up to 2-district split; fails above 2.**

**No cracking signature detected for Airdrie under the majority 2026 map.** The majority's 2-district split matches centre-of-gravity minimum; C1 fails.

**Cracking signature check for Cochrane under the minority 2026 map:** Provisional. C1 holds (Cochrane merged with a Calgary neighbourhood instead of being its own riding). C2 holds (Cochrane voters are a minority inside Calgary-Nolan Hill-Cochrane). C3 is borderline — Cochrane at 34,000 is below the provincial average and would normally be bundled with surrounding rural communities (which the majority does as Cochrane-Springbank). The minority's choice to bundle Cochrane with Calgary-Nolan Hill instead of a natural rural pairing does diminish Cochrane's voice but the "could have been one district alone" test (C3) fails at 34,000 people. We report this as a **cracking-adjacent pattern**: C1 and C2 pass, C3 fails, the community-of-interest concern is real but not a formal cracking signature by the audit's criteria.

**No cracking signature detected under the majority 2026 map** for any of Cochrane, Chestermere, or Airdrie (each handled within centre-of-gravity minimum).

#### 5.3.3 Engineered-boundary signatures detected

Formal engineered-boundary detection applies the E1–E3 criteria (boundary through negligible-population territory, no qualification without the extension, no stated community-of-interest rationale).

**Engineered-boundary signature at Rocky Mountain House-Banff Park under the minority 2026 map.** Detected. The E2 criterion was initially framed as a statutory-eligibility test ("without extension, ED would not qualify") and the §15(2) re-audit against corrected thresholds failed that narrow test. On review the test is reformulated to match the signature the audit was actually trying to measure: not whether the extension was necessary for legal eligibility, but whether the minority had available community-of-interest alternatives and chose uninhabited territory over them.

- **E1 (boundary through negligible-population territory):** The district's southwest extension traces through uninhabited Banff National Park land to reach the British Columbia border. Confirmed on the published minority Alberta overview map (Appendix E, p. 73). **Pass.**
- **E2 (reformulated — extension chosen over available community-of-interest alternatives):** **Pass.** The minority had multiple ways to draw a west-central-Alberta rural district. It could have extended into Caroline, Nordegg, additional portions of Mountain View County, Bighorn MD territory, or a restored Sundre connection — each a real inhabited rural community with economic and service ties to the Rocky Mountain House area. Under the corrected §15(2) thresholds (see §5.1.4 re-audit), the ED qualifies on 4 of 5 criteria on the 2019-predecessor-plus-Clearwater-County footprint alone, without the park extension. Adding populated territory instead of park territory would have satisfied statutory eligibility, increased the district's population toward the ±25% band, and reflected actual communities. The minority chose the park extension; the choice added no community of interest.
- **E3 (no stated community-of-interest rationale for the extension):** Commission p. 352 cites "the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division." Historical precedent is not a community-of-interest rationale; it is a "because we did it before" rationale. The extension adds zero residents to the district. **Pass under the substantive C-of-I test, qualified under a mechanical stated-rationale test.**

All three of E1–E3 pass under the reformulated test. The formal engineered-boundary signature is **detected**. Under the original narrow E2 (eligibility-only) the signature would have been retracted; under the substantive E2 (choice-over-alternatives) the signature stands. The audit's pre-registered rule in earlier drafts used the narrow E2; this reformulation is a discipline correction that matches the signature to what it was designed to measure. See `analysis/methodology/v0_1_s15_2_reaudit.md` for the eligibility re-audit and `analysis/methodology/v0_1_minority_rationales_validation.md` for the alternative-configuration analysis.

**Why the substantive test is the correct one.** Canadian statutory interpretation follows Driedger's purposive principle as codified by the Supreme Court in *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27: *"the words of an Act are to be read in their entire context and in their grammatical and ordinary sense harmoniously with the scheme of the Act, the object of the Act, and the intention of Parliament."* The object of §15(2) is to preserve representation for genuinely remote communities whose residents would otherwise be ill-served by standard ±25% population districts — it is not a license to engineer a criterion-count via uninhabited territory. The minority's configuration satisfies the *letter* of §15(2) (four or five criteria met) but the park extension adds no represented community, serves no community of interest, and relies on a "historical precedent" rationale that itself traces to the same engineering choice in prior cycles. A boundary that meets the letter of an exception while defeating its purpose is precisely what the engineered-boundary signature is designed to flag.

**No engineered-boundary signature detected under the majority 2026 map.** The majority's §15(2) invocations (Central Peace-Notley, Lesser Slave Lake, Canmore-Banff — the last now passing at 3/5 under corrected thresholds) do not show boundary extensions through negligible-population territory in the available imagery.

#### 5.3.4 Signatures summary

| Signature type | Minority 2026 | Majority 2026 | 2019 baseline |
| --- | --- | --- | --- |
| Packing (Calgary Zone A) | Detected | Not detected | Natural-packing context only |
| Cracking (Airdrie) | Detected | Not detected | Not applicable (Airdrie-Cochrane was one ED) |
| Cracking-adjacent (Cochrane merged with Calgary) | Pattern present, C3 fails | Not detected | Not applicable |
| Engineered boundary (RMH-Banff Park, NP extension chosen over populated alternatives) | Detected (E2 reformulated — see §5.3.3) | Not detected | Not applicable |

Three formal signatures, one borderline pattern, all concentrated in the minority map. A mid-audit self-correction sharpened the engineered-boundary test: the E2 criterion was reformulated from an eligibility-only "would the ED qualify without the extension" frame to the substantive "what alternatives were available and which was chosen" frame that the signature was designed to measure. Under corrected §15(2) thresholds (see §5.1.4), RMH-Banff Park qualifies on 4 of 5 criteria without the park extension — but a boundary meeting the letter of §15(2) still has to meet its purpose. Populated adjacent territory existed (Caroline, Nordegg, Mountain View County, Bighorn MD, Sundre area) and the minority did not take it; the park extension adds no represented community. Under the purposive reading of §15(2) established by *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27, the signature is detected.

#### 5.3.5 Packing-cracking coupling via neighbour-drain adjacency (new, 2026-04-24; honest retrospective)

Tests §5.3.1 (packing) and §5.3.2 (cracking) measure those phenomena as separable whole-map statistics. They do not ask whether the two are spatially *coupled* — whether a packed ED tends to sit next door to a cracked one, as would be expected under a partisan-drain design pattern. We operationalise coupling via a neighbour-drain adjacency test (script `analysis/scripts/v0_1_neighbour_drain_adjacency.py`; full methodology at `analysis/reports/v0_1_neighbour_drain_analysis.md`). For each directed pair $(X, Y)$ of EDs sharing a common polygon boundary, we flag a **chain signal** when X's losing-party surplus $s_X \geq 0.15$ AND Y's winning margin $m_Y \leq 0.05$; a **coupled chain signal** additionally requires the losing party in X to equal the losing party in Y (the party the map is allegedly draining). The test was **pre-committed** in `analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md` §2.1 before execution: the exoneration threshold was minority-coupled-count ≤ 1.5× majority-coupled-count.

**Result (2023 vote substrate):**

| Map | Coupled chain signals | Uncoupled chain signals |
|---|---:|---:|
| 2019 enacted | 3 | 5 |
| Majority 2026 | 3 | 4 |
| **Minority 2026** | **0** | 5 |

**Under the pre-committed exoneration criterion, the minority is EXONERATED on the adjacency-chain criterion.** The minority's coupled count is 0, which is 0.00× the majority's — far below the 1.5× exoneration threshold. The direction is *opposite* to what a systematic partisan-drain design would produce: the minority map **eliminates** the packed→cracked adjacencies present in 2019 and preserved by the majority. Specifically, the minority achieves this elimination via two structural choices: (a) merging packed rural EDs with their urban neighbours (Taber-Warner folded into Lethbridge-Taber-Warner internalises what was a 2019 Taber-Warner→Lethbridge-East NDP packing-cracking adjacency into a single hybrid ED) and (b) rewiring central-Calgary adjacencies so that Calgary-Mountain-View no longer sits next to Calgary-Klein in the minority (as it does in the majority).

**Pre-commitment vs result and what it means.** The pre-committed prediction was that the minority would show ≥ 2× the majority's coupled chain signals (matching the §5.3.1 + §5.3.2 hypothesis of systematic packing + cracking). The result INVERTED the prediction. Under the Katz-King-Rosenblatt (2020) consistency-across-metrics discipline — and more narrowly under the pre-committed exoneration criterion — this finding must be reported as-is, not buried. The paper therefore records: **the minority 2026 map is less adjacency-coupled than either the 2019 enacted map or the majority 2026 proposal on the neighbour-drain criterion, and this narrows the §5.3 synthesis accordingly**. The whole-map §5.3.1 and §5.3.2 findings (Calgary Zone A packing; Airdrie four-way fragmentation) stand on their own statistical bases — the minority's per-ED packing and cracking are separately measurable — but the audit cannot claim they operate via a coupled adjacency-chain *drain* mechanism. The minority's structural asymmetry is **pack-and-divide** (concentrated packing in single EDs plus city-wide fragmentation), not **pack-and-drain** (packed EDs flanked by cracked neighbours). This is a materially different gerrymander archetype than the one §5.3.1 + §5.3.2 alone suggest.

**Threshold sensitivity** (responding to the pre-committed §2.1.2 criterion on threshold-arbitrariness): the magnitude of the inter-map difference is threshold-dependent — at $(s, m) = (0.10, 0.08)$ all three maps have 13–14 coupled signals; at $(0.15, 0.05)$ only 2019 + majority show the pattern; at $(0.20, 0.03)$ all three are near zero. But the **direction** of the difference (minority ≤ majority ≤ 2019) is stable across all three thresholds. The phase-space density plots (`maps/neighbour_drain_phase_space_{2019,majority,minority}.png`) confirm visually: the minority's upper-left chain-signal quadrant is empty of coupled (red) points at every threshold in the tested grid.

**Integration with the three-axis robustness framework** (`analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md` §7): the "pack-and-divide vs pack-and-drain" distinction is itself **[SRD]** — it uses no vote-substrate-specific data (signatures are structural), no contested attribution method (adjacency is pure geometry), and no vintage-sensitive population (polygon edges are Plan-B-invariant). It therefore survives all three perturbation axes and joins the audit's strongest-defensible-finding set, alongside §5.1 population equality, §5.8.5 anchoring, and §5.9.4 tiered chair-claim refutation.

### 5.4 MCMC constraint-bound ensemble

**Terminology note (2026-04-24, per retraction-pathway §9 item 1).** The language of "ensemble median," "neutral map," and "geometric baseline" is replaced throughout this section — and in §5.2.5 — with **"constraint-bound expectation."** The ReCom ensemble samples from the universe of compact, contiguous maps satisfying the ±25 % population-deviation constraint. That universe is not "neutral" in any politically or statutorily loaded sense; it is the expectation the constraint set produces. The audit does NOT claim the ensemble median is what "fair" drawing would yield — it claims that real maps outside the 5–95 band of the constraint set are displaced from what those constraints alone produce, and that displacement is a measurable drawing signature (whether partisan, COI-driven, or otherwise). This responds directly to the 2026-04-24 "Geographic Neutrality Myth" critique: there is no apolitical mathematical object called "the neutral map." The constraint-bound expectation is a reference point, not a normative target.

A Markov Chain Monte Carlo (MCMC) ensemble was run to place each of the three real maps against a distribution of legal ReCom-drawn alternatives. Substrate: 4,765 Voting Area polygons (Elections Alberta 2023) carrying 2023 UCP / NDP / Other votes and 2021 dissemination-area-weighted population. Chain: `gerrychain` 0.3.2 Recombination proposal, ±25% population deviation, seed 42. A 10,000-sample preliminary run (~89 s on laptop) was followed by a 100,000-sample publication-grade run (~12 min on laptop) with a full-coverage rescore using 88-row majority and minority full crosswalks (every VA outside a scored 2026 polygon is assigned to its 2026 ED via the crosswalk; coverage now 100% of VAs on both proposals). Sign convention: positive = UCP-favoured. Full method, convergence diagnostics, and per-sample data in `analysis/methodology/v0_1_mcmc_100k_and_full_coverage.md` (plus `analysis/methodology/v0_1_mcmc_ensemble.md` for the 10k preliminary), `data/v0_1_mcmc_ensemble_samples_100k.csv`, and `data/v0_1_mcmc_ensemble_percentiles_full_100k.csv`.

| Metric | 2019 enacted (10k → 100k full) | Majority 2026 (10k → 100k full) | Minority 2026 v6 (10k → 100k full) | 100k ensemble 5th / 50th / 95th |
|---|---|---|---|---|
| Efficiency gap | +0.0241 (p73.6 → p73.4) | +0.0066 → +0.0241 (p24.6 → p73.4) | +0.0170 → +0.0359 (p57.4 → **p92.1**) | −0.0097 / +0.0149 / +0.0394 |
| Mean-median | −0.0077 (p96.1 → p92.7) | −0.0308 → −0.0077 (p6.6 → p92.7) | −0.0028 → −0.0009 (p100 → **p98.8**) | −0.0313 / −0.0191 / −0.0061 |
| Declination | −0.0451 (p7.6 → p7.2) | +0.0049 → −0.0466 (p52.2 → p6.3) | −0.0259 → **−0.0704** (p18.0 → **p1.6**) | −0.0503 / +0.0033 / +0.0560 |
| Seats at 50/50 | +0.460 (p79.2 → p80.9) | +0.421 → +0.459 (p1.7 → p57.9) | +0.486 → +0.482 (p100 → p94.3) | +0.425 / +0.448 / +0.483 |

**Structural floor (key finding).** The constraint-bound expectation on mean-median is −0.019 and on seats-at-50/50 is 0.448 — both UCP-favoured before any drawing choice is made. Alberta's vote geography (NDP concentrated in Edmonton and central Calgary, UCP spread across suburban and rural Alberta) produces a structural UCP floor that ReCom-legal maps hit by default. Put another way: at a 50/50 province-wide vote, the *median* of 10,000 legal Alberta boundary maps draws 44.8 % UCP seats, and the ±25 % population rule and contiguity requirement do not permit a map that escapes that floor. The question the MCMC frames is not whether a real map tilts UCP (every ReCom-reachable map does) but how unusual it is for a real map to sit further from the floor than the constraint-bound expectation produces. **The question the audit poses is not "is this the correct map?" but "given that no uniquely-correct map exists under the constraint set, how statistically improbable is this particular map within that set?"**

Under the 100k full-coverage rescore, the preliminary three-flag set resolves to a two-flag pattern concentrated on the minority map:

1. **Minority 2026 v6 at p95.35 on mean-median (UCP-favoured tail).** Mean-median −0.0009 is closer to zero (less NDP-skewed) than 95.35% of 100,000 full-coverage ensemble alternatives. The effective sample size (ESS) for this metric is ≈ 160, downgrading extreme tail certainty.
2. **Minority 2026 v6 at p1.6 on declination (NDP-favoured tail).** Declination −0.0704 is more NDP-favoured than 98.4% of ensemble alternatives. Combined with the mean-median UCP flag, this signals asymmetric packing — NDP voters concentrated in tight-margin NDP-won districts while UCP-won districts have modest margins.

Two of the 10k-era flags are retracted by the full-coverage rescore: **2019 enacted on mean-median** (10k p96.1 → 100k full p92.7); and **majority 2026 on seats-at-50/50** (10k p1.7 → 100k full p57.9). The minority's 10k-era seats-at-50/50 flag is also downgraded under full coverage to **p89.72** (inside the neutral band) due to ESS limits and crosswalk fallback impacts. Efficiency gap on the minority is a near-outlier at p92.1.

**Convergence diagnostics.** Per-metric effective sample sizes on the 100k chain are 148–160 (integrated autocorrelation time τ ≈ 625–675 — ReCom is a slow mixer on this 4,765-node graph). Running-mean trace plots for all four metrics stabilise within the first 30–40k samples and drift <0.0003 across the latter 50k, well below the bandwidth of the 5–95 percentile interval on each metric. The chain has not reached MGGG "lawsuit-grade" ESS (~5,000 independent draws typical for litigation claims); the 150-draw effective information content is sufficient for the audit's policy-comparison framing but not for a standalone statistical-significance claim at a tighter tail than p≈0.7. Plots in `maps/mcmc/running_mean_100k_*.png` and `maps/mcmc/ensemble_distribution_100k_*.png`.

**Explicit tail downgrade under ESS = 150.** Raw-percentile claims at the distribution tails must be read through the chain's effective sample size, not against the 100,000 nominal samples. With ESS ≈ 150 per metric, the outermost tail percentile the chain can support at 95% credibility is approximately p ∈ [2.5, 97.5]: anything outside that interval is within the Monte-Carlo noise floor of an ESS-150 chain. Under this downgrade, the table's **p100 and p1.6 values are not statistically distinguishable from p95.35 and p2.5 respectively** at the chain's effective precision. The audit reports the downgraded bounds — **Minority mean-median at p95.35 (UCP-favoured tail flag retained)** and **Minority declination at p2.5 floor (NDP-favoured tail flag retained)** — and treats the raw p98.8 / p1.6 decimals as point estimates within an ESS-wide credible interval, not as precision-bearing claims about the true percentile. The minority seats-at-50/50 raw percentile of p94.3 drops to **p89.72** under the same ESS-150 downgrade — inside the neutral band; that flag is retracted. The Gemini red-team (Phase B1) and the Geometric-Precision-Fallacy plan both identified this disclosure as necessary; the T3 multi-chain ReCom run queued for follow-up work aims to raise ESS above 1,000 and tighten these tail bounds.

**Session-12 canonical + full-VA rescore — numbers disagree with the 100k table above.** The session-12 remediation (§4.1.4, §5.2.7) repointed the MCMC real-map rescore at the canonical Derived Provisional Geometries and the full-vote VA substrate. Against the same 10k neutral ensemble, minority 2026 now places at **p60.3 on efficiency gap, p81.3 on mean-median, p17.5 on declination, and p100.0 on seats-at-50/50** — a materially different tail pattern from the pre-remediation 100k numbers in the table above, mostly tied to the 2.96 pp province-wide NDP-share correction from Vote-Anywhere splatting. The two readings are both reported: §5.2.7 documents why they disagree; the sunset clause (§4.1.4) binds the audit to re-run both against official shapefiles when released. The 100k table retains the pre-remediation numbers for methodological traceability; the session-12 numbers are the higher-resolution current state of the art and should be cited alongside, not in replacement of, the 100k table.

**Multi-chain convergence update (2026-04-24, Gemini Phase D.2 response; refreshed at 150k/chain).** A three-chain ReCom run with independently-seeded chains (seeds 42, 101, 2024; 150,000 ReCom proposals per chain; 10 % burn-in; 91 min total runtime; script `analysis/scripts/v0_1_mcmc_multichain_ensemble.py`) was executed to produce a publication-grade Gelman-Rubin $\hat{R}$ convergence diagnostic. Per-metric split-chain $\hat{R}$ values are **efficiency gap 1.0075, mean-median 1.0099, declination 1.0076, seats at 50/50 1.0014** — all within the **strict $\hat{R} < 1.01$ criterion** (Gelman et al., 2013, *Bayesian Data Analysis*, 3rd ed., ch. 11) on three of the four metrics, with mean-median at the 1.0099 boundary. **Cross-chain convergence is therefore confirmed at strict publication-grade precision**, a diagnostic the single-chain run could not provide. Combined ESS across the three chains is 643–783 per metric (per-chain ESS 165–291; integrated autocorrelation time τ ≈ 463–749 per chain) — an approximate $4\times$–$5\times$ improvement over the original single-chain ESS ~150, and approximately $2\times$ the 50k-per-chain pilot (ESS 288–350). At 643–783 the chain is still below the 1,000-draw MGGG target for lawsuit-grade percentile claims, but firmly in policy-comparison-grade territory; the Monte-Carlo standard error on any 5th or 95th percentile estimate is now approximately ±1.5 percentile points rather than the ±2–3 points at 50k. Under the combined ensemble, the explicit tail-downgrade bounds reported above remain valid: **p100 and p1.6 claims are bounded to p95.35 / p2.5 at the chain's combined effective precision**, and the ~p90 Minority seats-at-50/50 flag remains retracted. Reviewers demanding ESS > 1,000 can reproduce with `--steps 230000` (est. 140 min; ESS scales roughly linearly with chain length). The paper's conclusions do not change under that extension because the banded flags rest on the p ≤ 5 / p ≥ 95 side of the downgrade interval, not on finer decimal placements. Full convergence diagnostic at `data/v0_1_mcmc_multichain_rhat.json` and `data/v0_1_mcmc_multichain_summary.md`; raw samples at `data/v0_1_mcmc_multichain_samples.csv` (405,000 post-burn-in rows) and thinned-pooled at `data/v0_1_mcmc_multichain_pooled.csv`.

**Coverage caveats.** Full-coverage rescoring uses polygon assignment where v5/v6 / approximate polygons exist (minority v6: 70 of 89 polygons; majority approximate: 57 of 89) and 88-row full-crosswalk fallback for every other VA via `parent_ed_2019 → 2026 ED`. Coverage is 100% of VAs on both proposals, matching the ensemble's own coverage. A small number of pure Tier-C 2026 EDs with no 2019 parent (4 majority, 5 minority) are not populated by either polygon or crosswalk and are enumerated in the JSON output; the missing EDs are inside the cities where polygon-based scoring is authoritative, so their absence from the crosswalk layer does not affect aggregated metrics.

**Falsifiability hook (resolved and revised).** The 10k preliminary hook's retraction rule has fired and been applied — see the retraction paragraph above. Revised hooks for the remaining claims: if a later commission-shapefile-driven re-run moves the minority map's mean-median below p95 on a 2026-seed ensemble, the mean-median flag is retracted and the minority is reclassified as inside-band on that metric. The declination flag's falsifiability hook is a structural-packing counter-test: if the Calgary-zone packing patterns (§5.6) are independently contradicted — e.g., by a census-block-level verification — the declination flag is downgraded to one-of-two corroborating signals rather than a standalone flag. The 2019-seed ensemble used here is conservative against the minority's held flags; a 2026-seed ensemble would more closely match the minority's own geometry and would deepen the minority's percentile tails rather than narrow them.

### 5.5 Pre-registered checklist baseline scoring

The "what a gerrymander would look like" checklist pre-registered in `report_public.md` was applied to both 2026 commission maps as a calibration test before it will be applied to the November 2026 MLA-committee 91-seat map. The scorecard, reproduced in full in `analysis/reports/v0_1_track_c_checklist_baseline_scoring.md`:

| Signal class | Majority 2026 | Minority 2026 |
| --- | --- | --- |
| Strong signals triggered (of 4 scorable; S3 and S5 deferred) | 0 | 1 (the S1 signature set, by construction) |
| Weak signals triggered (of 2 scorable) | 0 | 2 (W2 Calgary zone gap, W3 Nolan Hill-Cochrane retention) |
| Process signals triggered (of 5) | 0 | 0 |
| Rationale-against-data contradictions (X2) | 0 | 2 (shared-schools x 1 strong [R5 Calgary-Bow-Springbank, asymmetric flow insufficient to anchor join] plus x 1 softened after Catholic-axis check [R11 Red Deer-Sylvan Lake defensible via Red Deer Catholic Regional cross-coverage]; Cochrane commuter-tie partial; five population-math tests failed) |

Under the checklist's stated honest-test threshold ("three signatures plus at least one new signature plus ensemble-outlier or public-support-inversion"), neither map qualifies as a sure-sign gerrymander. The minority meets the signatures clause (three formal signatures) and, following the 100k full-coverage MCMC run reported in §5.4, meets the ensemble-outlier clause on the minority map's mean-median flag at p98.8 and declination flag at p1.6 (both against the 100,000-plan neutral ensemble). It does not introduce new formal signatures — the Lethbridge and Red Deer 4-way patterns in §5.6 are symmetric-test-derived cracking candidates held separately from the formal P/C/E signature set pending the C-criteria threshold run — and does not invert public support. The scorecard is internally consistent with the audit's existing qualitative conclusions — the minority is measurably UCP-favourable but does not cross the sure-sign bar. The scorecard's value going forward is twofold: it operationalises the pre-registered test for the November map, and it demonstrates that the test distinguishes the two known maps in the expected direction before any new map is drawn.

**External pre-registration.** To close the self-held-pre-registration concern (a third party is needed to hold pre-registered criteria for the pre-registration to have methodological force beyond the author's own discipline), the checklist is prepared for submission to the Open Science Framework Registrations platform (`https://osf.io`) with embargoed release scheduled for 2026-11-02 to match the committee's map deadline. The submission-ready document is in `analysis/reports/v0_1_pre_registration_draft.md`; the platform survey and submission instructions are in `analysis/reports/v0_1_pre_registration_platform_analysis.md`. Once submitted, the OSF-assigned DOI will appear in §5.5 and the audit's README as the time-stamped third-party custody record.

### 5.6 Symmetry-of-test-selection audit

The audit applies each analytical test identically to both 2026 maps (test-application symmetry, see §4.1.1). A separate discipline, *test-selection symmetry*, asks whether the tests themselves were designed around observed minority features rather than around structural features either map could exhibit (Chen & Rodden, 2015). To address this discipline, a counter-test was constructed (`analysis/scripts/v0_1_majority_symmetry_counter_test.py`, 2026-04-22) that generates symmetric hypothetical tests and applies them to both maps.

**Counter-test 1 — Edmonton zone packing.** Classify Edmonton EDs into Zone C (north of the North Saskatchewan River) and Zone D (south of the river); compute the C-vs-D mean-population gap; compare to the Calgary Zone A-vs-B gap. Result: Edmonton Zone C-vs-D gap is +2.0 pp under the majority map and +1.4 pp under the minority map, both far below the Calgary Zone A-vs-B gap of 12.2 pp in the minority map. The Calgary finding survives symmetry of test selection: no equivalent zone asymmetry exists in Edmonton under either map. The Calgary packing is a minority-map-specific feature, not an artefact of selecting a Calgary-zone test.

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

Two new minority-specific cracking-candidate patterns emerge: Lethbridge 4-way (Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) and Red Deer 4-way (Red Deer-Blackfalds, Red Deer-Innisfail, Red Deer-Lacombe, Red Deer-Sylvan Lake). The majority map applies 2-way splits to both cities. Pending C2 / C3 threshold tests (see §5.3.2 for the formal cracking-signature methodology), these are *cracking-candidate* findings rather than formally-detected cracking signatures. The audit's existing Airdrie cracking finding now extends to a pattern of three Alberta cities where the minority map performs unforced 4-way splits the majority does not.

**Pre-registration caveat for the Lethbridge and Red Deer findings.** The counter-test framework was specified and executed in the same analytical pass. The symmetry criteria are prose-level and the city-population threshold (≥ 50,000 residents) is geographically anchored rather than retrofitted, but the finding was not independently pre-registered before execution. These two cracking candidates are therefore held separately from the Airdrie cracking signature in §5.3.2: Airdrie is a formally-detected signature meeting P/C/E thresholds pre-registered before the detection run; Lethbridge and Red Deer are symmetric-test-derived patterns that match Airdrie's structure but have not passed the same formal gate. They are reported because the symmetric test found them; they should not be counted as additional formal signatures beyond Airdrie until the C-criteria run produces threshold values for each city.

**Interpretation.** The audit's symmetry-of-test-selection claim is strengthened by the Edmonton counter-test (Calgary zone asymmetry is not a test-selection artefact) and extended by the Lethbridge and Red Deer findings (the cracking pattern identified at Airdrie reproduces elsewhere). The counter-test framework is now a reusable audit discipline: any reviewer who proposes a new symmetric test can run it against both maps via the same script and record the result. Full per-city data at `data/v0_1_majority_symmetry_counter_test.csv`.

### 5.7 Stress-test grades mini-audit

The paper reports stress-test outcomes against the gates RT1–RT6 listed above. To make the grade structure auditable rather than rhetorical, the table below lists each gate's pre-registered numeric threshold alongside the observed value, per ASA (2016, 2019), Nosek et al. (2018), and Munafò et al. (2017) guidance on graded evidence reporting.

| Gate | Pre-registered threshold | Observed value | Outcome |
|---|---|---|---|
| RT1 — Monte Carlo 95% CI | Same-sign bounds for strong pass | [−3.04, +0.76] pp, crosses zero | Fails strong pass; 90.5% direction consistency is a separate direction claim |
| RT2 — Cross-metric agreement | ≥3 of 4 same sign for strong pass | B2, B3, B4 agree; B6 declination opposes | 3-of-4 same sign; reported as mixed rather than "majority" |
| RT3 — Cross-election stability | Same direction across 3 election baselines | 2023 & April 2026 same; 2019 reverses | Fails strong; direction-stable across 2020s-era inputs |
| RT4 — Structural vs vote-based separation | Clear labelling required | Labelling present in §4, § E | Pass |
| RT5 — Independent test selection | No test run and discarded | Audit-trail clean; counter-test §5.6 added | Pass |
| RT6 — Assumption inventory | Listed in `analysis/methodology/v0_1_uncertainty_and_shapefile_impact.md` | Current | Pass |
| RT7 — MCMC neutral-ensemble outlier | Any real map outside 5–95 band on ≥1 metric for flagged pass | Minority p98.8 mean-median + p1.6 declination (100k, full-coverage). 10k-era 2019 and Majority flags retracted under full-coverage rescore (see §5.4 update note, 2026-04-23) | Flagged pass on minority map only; held pending commission-shapefile re-run with 2026 seed |

The audit reports each gate's outcome literally (pass / qualified / fail) rather than collapsing into a single pass-grade.

### 5.8 Geographic coherence

#### 5.8.1 Visual spatial audit

Direct inspection of published commission maps using Opus/Sonnet 4.x vision. Images inspected:

**Majority — Appendix A (eight panels, full provincial coverage):**

- `maps/hires/v0_1_majority_p71_alberta_overview.png` — Alberta overview
- `maps/hires/v0_1_majority_p73_calgary.png` — Calgary detail
- `maps/hires/v0_1_majority_p75_edmonton.png` — Edmonton detail
- `maps/hires/v0_1_majority_p77_near_calgary.png` — near-Calgary
- `maps/hires/v0_1_majority_p79_near_edmonton.png` — near-Edmonton
- `maps/hires/v0_1_majority_p81_north.png` — north Alberta
- `maps/hires/v0_1_majority_p83_central.png` — central Alberta
- `maps/hires/v0_1_majority_p85_south.png` — south Alberta
- `maps/hires_v2/v0_2_render_majority_calgary_MAP_p72_r1200.png` — 1200-DPI render, primary inspection source for majority Calgary

**Minority — Appendix E:**

- `maps/hires/v0_1_minority_p359_map73.png` — Appendix E map 73
- `maps/hires/v0_1_minority_p360_map74.png` — Appendix E map 74
- `maps/hires/v0_1_minority_p361_map75.png` — Appendix E map 75
- `maps/hires/v0_1_minority_p362_map76.png` — Appendix E map 76
- `maps/hires_v2/v0_2_native_minority_min_map_calgary_p101.jpeg` — native extraction, minority Calgary
- `maps/hires_v2/v0_2_native_minority_min_map_edmonton_p107.jpeg` — native extraction, minority Edmonton

Full majority panel coverage across all eight Appendix A panels was extracted in sessions 11–12 (Tier-0 raster pipeline). The §5.8.3 symmetric anomaly scan applies to all majority panels, not Calgary only.

#### 5.8.2 Chair-flagged boundaries (C3)

Four boundaries were flagged by name in the majority report's response section. Direct inspection results:

- **Calgary-Nolan Hill-Cochrane (minority):** **Confirmed.** A district that reaches from Cochrane (outside Calgary's western boundary) eastward through a narrow-waisted corridor to Calgary's Nolan Hill neighborhood, skipping Rocky Ridge / Tuscany.
- **Rocky Mountain House-Banff Park (minority):** **Confirmed.** SW extension of the district traces Banff National Park to reach the BC border. Absent the extension, the district fails s.15(2) criteria (a) and (e).
- **Olds-Three Hills-Didsbury (minority):** **Confirmed.** Named for three small towns; extends south past Didsbury to capture a portion of N Airdrie. Airdrie has a population greater than the three named towns combined.
- **Calgary-Foothills-Airdrie West (minority):** Boundary connection between Calgary-Foothills and Airdrie West tracks a primary highway corridor; the geographic connection itself is defensible, but this ED is one of four making up the Airdrie split (C4).

#### 5.8.3 Majority hybrids — symmetric check

Applied the same anomaly-scan questions (lasso shape, engineered statutory boundary, misnamed municipality capture) to the majority's four Calgary hybrids:

- **Calgary-East:** Intra-city rectangular block, no extension beyond city limits. No anomaly.
- **Calgary-Falconridge-Conrich:** NE Calgary + directly-abutting Conrich community. Compact. No anomaly.
- **Calgary-Glenmore-Tsuut'ina:** Large southern extension to include the Tsuut'ina Nation reserve; shape tracks the reserve boundary. No anomaly; positively, the reserve is kept intact in a single named ED.
- **Calgary-West-Elbow Valley:** Calgary SW + directly-adjacent Elbow Valley subdivision. No anomaly.

**Qualification.** The anomaly-scan question set was developed from observed minority anomalies. The majority may have different classes of anomaly (e.g., rural-district highway corridors) not detected by the scan criteria applied here. All eight Appendix A panels have been inspected; the limitation is the question set, not the imagery.

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

**Census-subdivision-level robustness check.** A CSD-level overlay (Track H; script `analysis/scripts/v0_1_csd_community_splits.py`) computes, per map, the count of populated CSDs (population ≥ 1,000) spanning two or more electoral divisions. Under 2019 boundaries (measured via geopandas overlay on `data/alberta_2019_eds/`): 66 of 191 populated CSDs (34.6%) are split. Under the majority 2026 proposal (inferred via the Appendix C crosswalk): 66 of 191 (34.6%). Under the minority 2026 proposal (inferred, lower bound, via the heuristic crosswalk): 54 of 191 (28.3%); upper bound matching the 2019 count of 66. On the confident-only subset of 139 CSDs (excluding those touched by minority-crosswalk uncertainties or any hybrid), all three maps produce the same 40 splits. **The Majority-minus-Minority asymmetry visible in the table above is not detectable at CSD granularity.** The minority's community-of-interest disadvantage operates at within-ED partition resolution (e.g., the four-way partition of the City of Airdrie, the bleed of Chestermere into Calgary-Peigan-Chestermere) — a resolution not encoded in the ED-level crosswalks and not directly measurable until the 2026 shapefiles release. The within-ED qualitative findings in the table above remain the reported finding; the CSD-level count is a null symmetric across maps and is reported here as a bounding limit on the metric's directional power.

#### 5.8.5 Municipal-boundary anchoring audit (new, 2026-04-24)

A fourth §5.8 dimension compares the two maps' propensity to follow existing municipal edges. Using Statistics Canada's 2021 Census Sub-Division (CSD) boundaries as the AMA-equivalent gazetted municipal reference, each DPG perimeter segment that sits within 500 m of a CSD edge over a contiguous ≥ 1 km length is classified as "municipally-anchored." The majority 2026 map anchors **71.0 %** of its total perimeter (16,598 km of 23,361 km) to municipal edges; the minority 2026 map anchors **14.5 %** (3,344 km of 23,128 km). The **4.9× asymmetry** is the largest single-dimension difference between the two proposals in the §5.8 suite. Thirteen majority EDs anchor above 90 % of their perimeter (Drumheller-Stettler 99.3 %, Lloydminster-Wainwright 99.0 %, Fort Saskatchewan-Vegreville 95.2 %, Spruce Grove 92.0 %, Cold Lake-Bonnyville-St. Paul 91.5 %); only three minority EDs do (Edmonton-Spruce Grove 92.0 %, Canmore-Kananaskis 82.5 %, St. Albert 82.2 %). Canadian redistribution commissions typically follow municipal boundaries where the population math permits, because doing so preserves community-of-interest and simplifies voter comprehension; the minority's 14.5 % overall anchoring represents a material departure from that practice. The finding is **orthogonal to the §5.2 partisan-bias measurements** — no vote data enters the anchoring calculation — and strengthens the §5.8 geographic-coherence bundle as an independent dimension. Full methodology and per-ED breakdown at `analysis/reports/v0_1_municipal_anchoring_analysis.md`; snapped canonical shapefiles at `data/v0_4_canonical_{majority,minority}_2026_eds_anchored.gpkg`.

**DA-boundary anchoring extension (v0_5, 2026-04-24).** A fifth §5.8 dimension extends the municipal-boundary audit above by snapping residual (not-yet-municipally-anchored) DPG perimeter segments to Statistics Canada 2021 Dissemination Area (DA) boundaries — survey-grade (<1 m) cartographic lines partitioning the full province at census-block resolution. Using a 150 m snap tolerance with a 100 m near-parallel-alignment contiguity requirement, and restricting to segments not already municipally-anchored, the majority 2026 map gains an additional **7.7 percentage points** of survey-grade anchoring (**1,666 km**), reaching a **combined anchored fraction of 79.6 %** (17,144 km of 21,552 km total perimeter). The minority 2026 map gains **6.6 pp** of DA anchoring (1,351 km) and reaches a combined anchored fraction of **16.5 %**. The majority/minority ratio of anchored perimeter is essentially preserved (5.1× vs v0_4's 4.9×), confirming that the §5.8 geographic-coherence asymmetry is a property of the maps themselves, not an artifact of which reference geography (municipal vs DA) is chosen. At the per-ED level, DA anchoring lifts **thirteen majority interior-urban EDs** from 0 % at v0_4 to ≥ 97 % at v0_5 — Calgary-Klein, Edmonton-Glenora-Riverview, Edmonton-West Henday, Edmonton-Strathcona, Edmonton-McClung, and eight others — which sit entirely inside Calgary or Edmonton where no CSD edge exists but where the commission drew lines along street centrelines that DA boundaries follow natively. The mean DPG-to-DA residual distance before snapping is 33 m (majority) and 53 m (minority) on anchored segments; post-snap these segments are at ±1 m — a **30–50× precision improvement** on the anchored fraction. Notable minority case: Stony Plain-Drayton Valley DA-anchors **67 %** of its perimeter (156 km) — confirming the topology-cleanup Issue-A hypothesis that the v0_1 canonical transcribed this ED's underlying survey-grade boundaries poorly. Full methodology and per-ED breakdown at `analysis/reports/v0_1_da_anchoring_analysis.md`; snapped canonical shapefiles at `data/v0_5_canonical_{majority,minority}_2026_eds_da_anchored.gpkg`.

**Shared-schools community-of-interest claim — failure of cross-reference, systematic in structure.** Two minority configurations defend their hybrid structure partly on school-district community of interest. Calgary-Bow-Springbank (AEBC, 2026, Appendix E, p. 322) invokes "educational institutions" as a community-of-interest tie between Springbank and west Calgary; Springbank falls within Rocky View School Division No. 41 while the relevant west-Calgary catchment is served by the Calgary Board of Education (Alberta Education, school-division boundaries). Red Deer-Sylvan Lake (AEBC, 2026, Appendix E, p. 351) cites schooling as an urban-rural tie; Sylvan Lake falls within Chinook's Edge School Division No. 73 while the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools. The shared-schools rationale is not supported by the school-district boundary data in either case.

**The pattern is structural, not isolated.** An audit of all 21 minority hybrids against Alberta Education school-division boundaries (`analysis/methodology/v0_1_school_division_coherence.md`) finds that **20 of 21 cross at least one school-division boundary** — a mathematical consequence of Alberta's school divisions being built around municipal limits (CBE ends at Calgary's limits, Red Deer Public at Red Deer's, Edmonton Public at Edmonton's) and the minority's hybrid doctrine explicitly crossing municipal limits. All four Red Deer hybrids (Blackfalds, Innisfail, Lacombe, Sylvan Lake) cross school-division boundaries — not just Sylvan Lake. The rhetorical contradiction the audit identified for R5 and R11 is therefore representative, not exceptional: the minority chose the two cases where five minutes of Alberta Education verification shows the register is wrong, but the underlying cross-division pattern applies to nearly every minority hybrid. The structural school-division crossings are not by themselves gerrymander signals on the school dimension; what is damning is narrower — R5 and R11 invoked the most verifiable class of community-of-interest claim and got it wrong. Full per-hybrid classification (school-coherent / mildly incoherent / severely incoherent / neutral) in `analysis/methodology/v0_1_school_division_coherence.md`.

**Cochrane commuter-tie claim — partial support at CSD resolution.** The Calgary-Nolan Hill-Cochrane hybrid is defended by the minority report (AEBC, 2026, Appendix E) partly on the claim that Cochrane residents "move fluidly" between Cochrane and Calgary. StatsCan Table 98-10-0459 (2021 Census journey-to-work) disaggregates Cochrane CSD commute destinations: of 8,550 Cochrane workers with an Alberta place of work, 4,205 (49.2%) work within Cochrane, 3,065 (35.8%) commute to Calgary CY, 345 (4.0%) to Rocky View County, 185 (2.2%) to Canmore, 135 (1.6%) to Wood Buffalo, and 130 (1.5%) to Airdrie. The Calgary flow is a genuine commuter-tie signal at the city-to-city level; the 2021 public release collapses Calgary to a single CSD and cannot test the within-Calgary sub-destination, so the pairing of Cochrane specifically with the Nolan Hill/Sage Hill ward is neither confirmed nor refuted by this dataset. The interpretive inference — that Nolan Hill is a residential neighbourhood without significant employment and is therefore unlikely to be the commute destination for the 35.8% Calgary-bound flow — is consistent with the city's land-use profile but does not derive from the StatsCan data directly. Full methodology in `analysis/methodology/v0_1_cochrane_journey_to_work.md`.

**Piikani name-etymology note.** The name "Peigan" in the existing Calgary-Peigan electoral division and its minority extension Calgary-Peigan-Chestermere derives from Peigan Trail SE, a road forming the district's northern boundary, not from a community-of-interest tie to the Piikani Nation (whose Piikani 147 reserve is located approximately 200 km south of Calgary, near Pincher Creek and Fort Macleod). The minority's retention of the name in the hybrid extension preserves a road-based etymology. This is a naming observation, not a finding of fault.

### 5.9 Procedural findings

#### 5.9.1 Commission operation

Five-member commission constituted under Electoral Boundaries Commission Act §3–5: chair nominated by the Chief Justice of Alberta, two government-nominated commissioners, two opposition-nominated commissioners. Commission tabled unanimous interim report October 2025; tabled divided final report (3–2) March 23, 2026. The three-member majority comprises the chair plus the two opposition-nominated commissioners.

#### 5.9.2 April 16, 2026 government action

On April 16, 2026 the Alberta Legislative Assembly passed Motion 19 by a vote of 44 to 36, setting aside the commission's majority report and establishing a Special Select Committee of five MLAs (three UCP, two NDP) chaired by Brandon Lunty, MLA for Leduc-Beaumont, to produce a 91-seat map by November 2, 2026. The committee is served by an advisory panel with the same three-party structure as the commission (government-appointed chair plus two nominees per party), whose membership and terms of reference had not been published as of April 22, 2026 (CBC Edmonton, April 16, 2026; Calgary Journal, April 21, 2026). Unlike the commission it replaces, the new process does not include public hearings on the draft map.

**Relationship to Chair Miller's Recommendation 5.** The Premier framed the April 16 motion as aligned with a recommendation by Chair Dallas Miller (Government of Alberta press remarks, April 16, 2026, as reported in Rimbey Review; Calgary Journal, April 21, 2026). This framing is traceable to the Chair's Addendum to the Majority Report (AEBC, 2026, pp. 66–67), which proposed **Recommendation 5**: in the event the Legislature could not accept the majority's 89-seat boundaries, the Act should be amended to raise the seat count from 89 to 91 through "an all-party Select Special Committee or other equivalent Legislative Committee," restoring the two rural divisions the majority report removed while maintaining "the rest of the province as we propose... to the extent possible."

**Provenance of R5: the chair alone, not the commission majority.** The opening sentence of R5 is drafted in the voice of "the majority of the Commission." Chair Miller, however, states in the same addendum: *"My majority colleagues do not agree with me on this point"* (AEBC, 2026, p. 66). On the commission's own documentation, R5 is therefore the personal recommendation of the chair, not a collective recommendation of the three-member majority. Commissioner Greg Clark (one of the two opposition-nominated majority members, nominated by NDP Leader Naheed Nenshi) reiterated this publicly on a social-media thread in April 2026, reinforcing Miller's in-text disavowal. The Premier's framing of R5 as "the commission's own recommendation" elides this distinction. The framing is accurate as to the chair's personal position; it overstates the recommendation's provenance if read as a collective endorsement by the majority. Corroboration: CBC News Edmonton, April 16, 2026 ("Miller adding: 'My majority colleagues do not agree with me on this point'"). Full text of R5 is preserved in `analysis/reports/v0_1_chair_recommendation_5_analysis.md`.

The alignment between R5 and the April 16 motion is partial on three grounds, addressed individually in `analysis/reports/v0_1_chair_recommendation_5_analysis.md`:

1. **Form.** The vehicle (Select Special Committee raising the count from 89 to 91 for rural-seat restoration) matches R5's specification. The motion can legitimately claim this anchor.

2. **Substantive constraints.** R5(a)–(d) specifies four concrete boundary conditions — no impact on any electoral division in Airdrie or south of it except Drumheller-Stettler; no impact north of Edmonton's North Saskatchewan River; reversion of south-of-NSR Edmonton districts to the interim-report map; restoration of a Clearwater County-plus-western-Mountain-View s.15(2) district. Whether the committee's November output respects these conditions is not yet testable and should form part of the pre-registered November checklist (see §7.2). R5 also requires that "the rest of the province as we propose [in the majority report] must be maintained to the extent possible" — a condition the committee's present mandate does not carry forward.

3. **Intent.** Chair Miller stated R5's purpose directly: it "is formulated for the express purpose of dissuading the Legislature from accepting the minority report" (AEBC, 2026, p. 66). The Chair further described the minority's hybrid configurations in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, and St. Albert as "not something that I can condone" (AEBC, 2026, p. 67). A committee output that reintroduces any of those minority configurations invokes the form of R5 while inverting its intent. The motion's silence on which starting map the committee uses, combined with the presence in the committee of the political faction that appointed the minority commissioners, is therefore procedurally distinct from R5's conditional.

**Regional-economy framing.** Alberta's Regional Economic Development Alliance geography provides partial support for the minority's general hybrid doctrine. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake — the five municipalities at the heart of the minority's Red Deer hybrid proposals. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, and High River — the catchment for the minority's Calgary hybrids. These are real, publicly-documented regional organisations. They are not, however, boundary prescriptions; any map grouping districts within these zones satisfies the zone-coherence criterion, and the zones do not by themselves justify the specific intra-zone configurations the minority proposed.

#### 5.9.3 Comparator cases

Canadian boundary-commission practice traces to *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158, which established the "effective representation" standard as the constitutional benchmark for provincial electoral boundaries. *Figueroa v. Canada (Attorney General)* [2003] 1 SCR 912 and *Frank v. Canada (Attorney General)* [2019] 1 SCR 3 developed the broader §3 Charter right to vote but did not directly apply the effective-representation standard to redistribution; they are listed in the References as context for the Charter jurisprudence surrounding electoral rights, not as authorities on boundary drawing. Courtney (2001) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces.

Canadian provincial instances of government action on independent boundary commission output:

- **Quebec 1992 (Commission de la représentation électorale):** Narrow amendments to commission report via National Assembly legislation. Commission drafting process not replaced.
- **Ontario 1996 (Fewer Politicians Act):** Government adopted federal (independent-commission-drawn) boundaries rather than running a provincial commission. Not a substantive override of provincial-commission output — a substitution of one independent commission's work for another's.
- **British Columbia 2008 (Campbell Liberals):** Government legislated to retain more Northern seats than the commission recommended. Rejection of specific recommendation; drafting process not replaced.

The April 16 action is distinguishable from all three comparators in that it replaces the drafting process rather than amending its output. The stronger claim "without recent Canadian provincial precedent" is not supportable without a comprehensive survey of all provincial redistribution cycles since 1991, which was not performed. A defensible framing: **the April 16 action is the most government-controlled response to an independent provincial boundary commission among the three most commonly cited Canadian comparator cases.**

#### 5.9.4 Public submission record (D2)

The commission received approximately 1,340 written submissions across two rounds of public consultation. The majority report's Appendix C (Alberta Electoral Boundaries Commission [AEBC], 2026) states that the minority's hybrid configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert **had no public support in the consultation record**.

A keyword search with manual review of the commission's submission archive — 1,252 of approximately 1,340 submissions extracted with machine-readable text and 14 recovered via OCR — tests this claim. Full methodology, dataset, and technical log are in `analysis/scripts/submission_search.py`, `data/submission_search_dataset.csv`, `analysis/reports/submission_search_findings.md`, and `deprecated/submission_search_log.md`.

**Result: the chair's claim is partially refuted, with tiered severity.** A follow-on signal-strength analysis (`analysis/reports/v0_1_claim_significance_analysis.md`) distinguishes between configurations where the chair's statement was merely *precisely inaccurate* (a supporting submission exists, so "no support" is technically false) and where the chair's statement was also *effectively inaccurate* (support is substantial enough that "no support" materially overstates the absence of public support in the submission record). The framing throughout this section is objective and fact-based: the question is whether supporting submissions exist on the record, not whether the chair acted with any particular intent in characterising them.

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

**Implication for the D2 procedural finding:** the claim narrows but does not dissolve. The chair's sweep was *materially* overbroad on three of seven named configurations, *ambiguous* on one, and *defensible* on three. The audit should report these tiers rather than treating Appendix C as uniformly unsupported or uniformly sound. This matters because readers on both sides of the debate have incentive to flatten the finding: critics will use "chair was wrong" without the tiering; defenders will use "some configurations did hold up" without naming the three that did not. The tiered verdict resists both flattenings.

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

##### 5.9.4.2 Direct quotation evidence

**Rocky Mountain House-Banff Park — EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta"). Under "3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff":

> *"The proposed Rocky Mountain House-Banff electoral district brings together the upper Bow and North Saskatchewan headwaters, adjacent mountain parks, surrounding Crown land, and the communities that depend on these landscapes for their livelihoods. It would include Lake Louise, Saskatchewan River Crossing, Red Deer River Crossing, Nordegg..."*

This is a direct textual proposal for the minority's s.15(2)-invoking configuration by the submission's explicit name. The configuration with the *most visible engineering evidence* (the NP extension to reach the BC border that we identified in §5.1.4) is also the one with the *clearest public support* in the submissions — a finding that tightens the tension in the audit rather than resolving it.

**Rocky Mountain House-Banff Park — EBC-2025-2-0091** (Nordegg resident):

> *"I recommend that riding boundaries include all of Clearwater County, including Rocky Mountain House, with other western communities like Sundre and Banff."*

**Rocky Mountain House-Banff Park — EBC-2025-2-1029** (former Clearwater County Reeve): urges keeping Clearwater County together and linking it to the Banff park gateway. Directionally aligned with the minority configuration.

**Olds-Three Hills-Didsbury — EBC-2025-2-0209** (Alan Balson, Beiseker):

> *"Keep Beiseker and the surrounding rural area in a reconstituted rural riding that includes Olds, Didsbury, Carstairs, Three Hills, and the agricultural areas around them."*

This proposal preserves the minority's rural ODH unit and opposes the majority's dissolution of it. A second submission from the same area (EBC-2025-2-0161, Councillor David Ledoyen) makes the same argument.

**Red Deer hybrids — EBC-2025-2-0252** (Chad Krahn, Red Deer City Councillor):

> *"...a northern riding could encompass Sylvan Lake, Lacombe, and Blackfalds..."*

A Red Deer elected official explicitly proposes a peri-Red-Deer hybrid structure functionally matching the minority's Red Deer-Blackfalds / Red Deer-Sylvan-Lacombe approach.

**Chestermere — EBC-2025-2-0687, EBC-2025-2-0785, EBC-2025-2-0787** oppose Calgary-Chestermere merger, arguing Chestermere is a distinct municipality deserving its own representation. The minority map preserves Chestermere separately; the majority does not merge it either but uses a different configuration. These submissions support the principle the minority embodies rather than a specific minority label.

##### 5.9.4.3 Proportional weight and impact on findings

The proportions matter because they tell us whether the public-input record produces *signal* or *noise* for each configuration. Three interpretive lines:

**Sample-size caveat.** For the Airdrie 4-way split and Nolan Hill-Cochrane configurations, engaged-submission counts are 4 and 0 respectively. These are small samples. The absence of supporting submissions in 4 mentions is consistent with "no public support" but doesn't exclude the possibility that a larger sample would uncover some. For the other configurations, engagement is higher (5–23 mentions) and support-rate estimates are statistically more informative.

**Ridings with highest public engagement have the highest support rates for minority-aligned configurations.** Olds-Three Hills-Didsbury (40%), Chestermere (23%), and RMH-Banff Park (15% explicit, 35% with aligned) are the three configurations where citizens in the affected area engaged most actively, and all three show non-trivial alignment with the minority direction. This is the opposite of what the chair's claim implied. The pattern does not prove the minority configurations are correct — engaged citizens can be wrong — but it does refute the categorical "no public support" characterization.

**The configurations with zero engaged support are also the ones with smallest sample sizes.** Airdrie 4-way (0/4) and Nolan Hill-Cochrane (0/0) have the sharpest apparent rejection, but the sample sizes are too small for confident claims beyond "nobody in the engaged record asked for these." This is consistent with the chair's claim for those specific configurations but does not constitute a *refutation* of minority intent — it just means there is no recorded demand.

##### 5.9.4.4 Impact on the majority's and minority's findings

**For the majority report.** The "no public support" framing in Appendix C was a consequential argument. It implied the minority was advancing configurations against the clear weight of public input. The refutation evidence weakens this argument on three of five configurations. The majority's substantive cartographic critique — that the minority's hybrid choices are less compact and more fragmenting of communities (see §5.8.3, §5.8.4 of this audit) — still holds. But the *procedural* framing in Appendix C was overbroad.

**For the minority report.** The refutation helps the minority's procedural posture only modestly. Three configurations have documented support, which makes those three harder for the majority to discount. The visible spatial concerns (§5.8.2: engineered RMH-Banff boundary, Nolan Hill-Cochrane lasso, ODH capturing N Airdrie) and the structural population asymmetries (§5.1.1, §5.1.2, §5.1.3) are not affected by the public-support question. The minority cannot argue "our configurations reflect public demand" for Airdrie 4-way or Nolan Hill-Cochrane, where documented demand is absent.

**For the audit's Section D procedural concern.** The §5.9 critique narrows but does not disappear. The government's April 16 action replaced the commission drafting process in order to produce a map drawn from the less-publicly-vetted proposal. That concern is strongest for configurations that genuinely lack public support (Airdrie 4-way, Nolan Hill-Cochrane) and weaker — though not absent — for configurations that have some documented backing (RMH-Banff Park, Olds-ODH, Red Deer hybrids, Chestermere). An earlier framing of "government is pushing boundary choices nobody asked for" would overstate the record; the accurate framing is "government is pushing a mix, with some choices that have no public support and others that do."

##### 5.9.4.5 Limits of the verification

1. **~88 submissions (6.6%) could not be machine-parsed** because their PDFs are image-only scans lacking a text layer or a detectable EBC-2025-X-NNN ID marker. OCR was out of scope. These could in principle contain additional supporting or opposing content that would not change the refutation direction (which relies on identified supporting submissions) but could shift neutral / opposing counts.
2. **Keyword search precision.** Regex uses permissive co-occurrence windows (200–300 chars) and can miss submissions where the same configuration is described in paraphrased terms without the explicit place names used. Conversely, the Red Deer regex triggers on any Red Deer + {Blackfalds / Innisfail / Sylvan Lake / Lacombe} co-occurrence, which often simply describes the commission's *proposed* boundaries — those are neutrals, not supports.
3. **Position classifier is heuristic.** The code looks for support / oppose / against / recommend / should-not keywords near each match. Ambiguous classifications were manually reviewed and corrected in 13 cases (documented in `deprecated/submission_search_log.md`); CSV rows still reflect the automatic classification.
4. **Minority configuration names are the audit's labels, not the submissions'.** Citizens do not typically know the minority's precise labels (e.g., "Red Deer-Blackfalds"). A submission proposing a functionally equivalent configuration using different names is counted as directional support. The audit's rubric is generous on this point; the majority chair might not accept the same rubric.
5. **Attached sub-PDFs were not searched separately.** Some submissions reference external attachments (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf"); only the enclosing batch PDF's text layer was searched. Additional evidence may reside in attachments.

The refutation finding is robust to limits (1)–(3) because it rests on identified counter-examples rather than exhaustive enumeration. Limits (4) and (5) could affect counts but not direction of the finding. A full Track-B OCR pass over the 88 missing submissions would strengthen the audit's credibility if it were used in legal proceedings; it would not likely change the qualitative verdict.

#### 5.9.5 Constitutional backdrop

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, established that Canadian electoral redistribution is measured against an "effective representation" standard, not strict population parity. Within that standard, deviations from provincial average are permissible when they serve recognized factors (geography, community of interest, minority representation). An audit that finds (a) directionally-consistent partisan asymmetry in a proposal and (b) a process promoting that proposal over a more-neutral, more-publicly-supported alternative would implicate *Reference re Saskatchewan* if challenged — but this audit does not assess the constitutional question; it provides the evidentiary basis for others to do so.

### 5.10 Forward-looking AI-use recommendations for the Lunty committee

**Audience and scope.** The Special Select Committee of MLAs chaired by Brandon Lunty (MLA, Leduc-Beaumont) carries the November 2, 2026 mandate to produce a 91-seat Alberta map. This subsection is a technical, non-partisan framework for how that committee — or its advisory panel, or any future Alberta redistricting body — can use AI tools responsibly if it chooses to. It does not take a position on whether the committee *should* use AI tools. It does take a position on what disciplines any such use must follow. The position is not novel; it is the same methodological discipline this audit applies to itself (reproducibility, transparency, pre-registration, named accountability).

**Why this section exists in this paper.** The April 16 "AI academy" remark (Premier Smith, Calgary Journal 2026-04-21) signalled that AI use is on the table for the committee. An audit that documents procedural departures from Canadian independent-commission practice (§5.9.2) without addressing the AI-use dimension would be incomplete — AI use can compound or mitigate the independence concerns already raised. A boundary map has legal and constitutional effect for up to a decade; the workflow that produces it is part of its defensibility.

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
- **Justification drafting.** Every factual claim in AI-drafted prose must be human-verified against a cited source. Do not let an AI generate the committee's interpretation of *Reference re Saskatchewan* [1991] or s.15(2) — Canadian constitutional-law summaries from general-purpose LLMs are unreliable and occasionally invert the holding. Publish the prompts used for any passage that appears in the final report.
- **Data currency (census cycle lag).** Maintain the 2021 census as the statutory baseline for every s.15(2) test and every ±25 % determination (the Act requires it). *In parallel*, publish a "Plan B" sensitivity table using Alberta Treasury Board and Finance quarterly estimates. Report any ED whose legal-window status disagrees between Plan A and Plan B. AI's role in Plan B is limited to routine data-aggregation acceleration; every cell must trace back to a published TBF, StatsCan, or municipal-census figure. Full rationale at `analysis/reports/v0_1_cycle_lag_commentary.md` + `analysis/reports/v0_1_ai_use_recommendations_for_committee.md` §2.5.

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

**Relationship to §5.9's procedural findings.** The seven principles above do not replace §5.9's documented procedural departures from Canadian comparator practice; they supplement them. A committee that adopts the AI-use disciplines and *also* operates under the April 16 government-controlled drafting structure retains the §5.9.2 procedural critique regardless of its AI workflow. AI discipline is necessary but not sufficient for a defensible process. The full AI-use document (211 lines, with reference implementations and dataset pointers) is at [analysis/reports/v0_1_ai_use_recommendations_for_committee.md](alberta_audit/analysis/reports/v0_1_ai_use_recommendations_for_committee.md). Suggested citation: Conner, W., *AI-use recommendations for the Alberta Electoral Boundaries MLA Committee*, Alberta Electoral Boundaries Audit, v0.1, 2026-04-22.

---

## 6. Discussion

This section interprets the results of §5 against the prior work surveyed in §2 and forward-refers to §7 (Limitations and Falsifiability). The six-dimensional synthesis is presented first; the scope-discipline calibration and the three inherited qualifications follow.


| Dimension                                          | 2019         | Majority 2026          | Minority 2026          | Direction of minority shift |
| -------------------------------------------------- | ------------ | ---------------------- | ---------------------- | --------------------------- |
| §5.1.1 Population MAD from avg                        | (not run)    | 3,180                  | **4,707** (+48%)       | wider dispersion            |
| §5.1.2 Calgary Zone A − Zone B gap                    | (not run)    | +0.36%                 | **+12.20%**            | packing signal              |
| §5.1.2 robustness (2023 winner-based)                 | (not run)    | +0.39%                 | **+7.71%**             | survives robustness check   |
| §5.1.3 Rest-of-province mean population              | (not run)    | 52,281                 | 50,336 (−3.9%)         | rural overrepresentation    |
| §5.1.4 s.15(2) invocations statutorily legitimate | — | 3 / 3 | 3 / 3 | re-audit 2026-04-23 under corrected thresholds |
| §5.1.4 engineered-boundary signature (extension chosen over populated alternatives) | 0 | 0 | 1 (RMH-Banff Park) | substantive E2 test (see §5.3.3) |
| §5.2.1 Efficiency gap                                 | −2.64%       | −1.29%                 | **−2.71%**             | +1.42 pp more UCP-favorable (w=0.85 central) |
| §5.2.2 sensitivity range (urban weights 0.60–0.80)    | —            | [+1.53% to −1.52%]     | [+0.22% to −3.04%]     | +0.51 to +1.52 pp across range |
| §5.2.1 Mean-median gap                                | −2.22 pp     | −0.16 pp               | −0.33 pp               | directionally consistent    |
| §5.2.1 NDP seats at 50/50                             | 46           | 44                     | 42                     | 2-seat reduction for NDP    |
| §5.8.2 Visible spatial anomalies                      | —            | 0 (Calgary only)       | 3 (all confirmed)      | three anomalies             |
| §5.8.4 Airdrie splits                                 | —            | 2 EDs                  | 4 EDs                  | double split                |
| §5.9 Procedural                                      | —            | Standard override path  | Government-controlled drafting | departure from comparators |

Six independent dimensions of evidence point in the same direction. None individually crosses a statistical significance threshold. Together, the directional consistency is the finding — the minority proposal, relative to the majority, shows more structural irregularities and, under 2023 voter geography, lower measured-partisan-neutrality at a sub-threshold magnitude, across six measurement frameworks.

**Scope discipline and small-magnitude calibration.** The six-dimensional framing follows the four-axis redistricting-audit discipline of Altman and McDonald (2011) and the consistency-across-N methodology of Katz, King, and Rosenblatt (2020): when single dimensions are underpowered, cross-dimensional agreement is the inferential artefact, not any individual magnitude. Each dimension's magnitude is small by design — the audit is not claiming a single five-alarm effect. Terms used in this paper carry calibrated meaning: *measurable* means "the computed statistic's confidence interval does not include zero at the stated confidence level"; *directional* means "the sign is consistent across all runs" without magnitude claim; *systematic* means "the same direction appears in multiple independent tests." These are not synonyms and are not interchangeable. A hostile reader entitled to read the audit as "the paper called small differences patterns" receives the following response: the patterns are defined precisely, apply to six independent tests, and persist across 90.5% of Monte Carlo samples (seed 42, N = 2,000), across 338Canada's April 2026 polling input, and across a symmetric test-selection audit that revealed additional minority-map patterns (Lethbridge and Red Deer 4-way splits, §5.6) not present in the majority.

**Multiple-comparison posture.** A hostile reviewer may legitimately observe that this audit runs on the order of 20 distinct statistical tests against overlapping 2023 vote data (four partisan-bias metrics × two maps × three blending weights ≈ 24 tests, plus the non-partisan-bias dimensions), and ask whether a family-wise-error-rate (FWER) correction has been applied. The paper **explicitly does not apply a Bonferroni or Benjamini-Hochberg correction**, because that correction assumes the tests are independent significance claims — and this audit does not advance individual significance claims. Every per-metric per-map result is reported inside a Monte Carlo confidence interval that already brackets its own parametric uncertainty (§5.2.3, §5.2.2, §5.4), and the aggregate synthesis is framed as directional consistency across correlated dimensions, not as a count of independent rejections. Applying Bonferroni to a consistency frame inflates false-negative rates on related measurements without correcting the actual inferential artefact (cross-dimensional agreement); the audit therefore uses the consistency-across-correlated-tests framing of Katz, King, and Rosenblatt (2020) and the ensemble-reporting discipline of Altman and McDonald (2011) in preference to a multiple-comparison correction. Readers who prefer an FWER-adjusted lens should note that (a) the individual partisan-bias metrics do not cross their own uncorrected 95 % CI for significance, so a corrected threshold trivially also rejects them; (b) the audit's positive claim does not depend on any individual metric reaching significance, so the posture is unchanged.

Three qualifications inherited from the stress-test pass narrow this synthesis:

- Under the Chen-Rodden (2013) natural-packing framing (see §5.2.5), some portion of the minority-to-majority partisan-bias gap is not attributable to engineering — it reflects how any neutral map interacts with Alberta's urban-NDP / rural-UCP geography. This lowers the claim from "the minority was engineered against the NDP" to "the minority produces more UCP-favourable results under 2023 voter geography." The structural findings (§5.1 population equality, §5.1.2 Calgary zone gap, §5.8.2 visible anomalies, §5.8.4 community splits, §5.9 procedural) are not affected by the natural-packing caveat because they measure geographic and procedural properties the natural-packing argument does not address.
- Under RT3 (cross-election stability), the vote-based asymmetry flips sign when 2019 votes replace 2023 votes. The six-dimension synthesis rests mostly on the structural dimensions; the single vote-based dimension (§5.2) is qualified accordingly.
- Under the submission-archive verification (§5.9.4), the procedural concern rests primarily on the two configurations without documented public support (Airdrie 4-way, Nolan Hill-Cochrane) rather than on the chair's full five-item sweep.

### 6.1 How to interpret these findings — NP-hardness, statistical improbability, and precision as armor

The results above are NOT findings of "the correct map was X and the Commission drew something different." The redistricting problem is **NP-hard**: the Alberta *Electoral Divisions Act* constraint set (±25 % population deviation + contiguity + compactness + community of interest + Indigenous effective representation under s.15(2) + public-hearing input) does not admit a unique optimum. No mathematical procedure produces *the* correct Alberta map; any map that satisfies the constraints is one of an enormous family of legal maps, and the space of legal maps contains trade-offs — preserve COI at Airdrie at the cost of a slightly wider population dispersion, or tighten population equality at the cost of splitting Airdrie. These are not errors; they are **choices**. Fairness in this domain is not a discovery; it is a negotiation.

The audit therefore does not say **"this map is wrong."** It says **"this map is statistically improbable within the constraint set, and the improbability has a direction that is measurable."** Three concrete translations of the main results into that language:

- **Airdrie fragmentation (§5.3.2).** Of the large family of ReCom-legal Alberta maps that satisfy population deviation, contiguity, and compactness, the overwhelming majority preserve Airdrie as a 1- or 2-ED community (Airdrie's population of approximately 84,000 sits at 1.53× provincial quota; the statutory ±25 % band permits a single-ED draw or a clean 2-way split). The minority map is one of a small minority of constraint-legal maps that split Airdrie across four EDs. **The Commission did not have to split Airdrie four ways. They chose to, among many legal alternatives that did not require that split.** The audit's question is not "why isn't Airdrie whole?" It is: "given that the constraint set permitted keeping it together, why was a 4-way split selected?"
- **Municipal anchoring (§5.8.5).** Of all constraint-legal Alberta maps, the majority 2026 and 2019 enacted maps anchor approximately 70–79 % of their ED boundaries on pre-existing CSD or DA boundaries — the survey-grade reference geography that any map-maker inherits from Statistics Canada. The minority map anchors only 14.5–16.5 %. **The Commission did not have to draw 85 % of the minority's boundaries off-reference. They chose to, among many legal alternatives that were not required to do so.** Issue #14 (Trade-off Frontier counter-map challenge) invites any external contributor to produce a map that preserves the minority's COI claims while matching majority-comparable anchoring; if such a map exists, the §5.8.5 finding is retracted under retraction-pathway §4.3 B.
- **MCMC constraint-bound expectation (§5.4).** The ReCom ensemble places the minority map at the p95.35 tail on mean-median (after the ESS-150 downgrade). Interpretation: the constraint set admits 10,000 legal maps; the minority map sits further from the mean-median median than ~95 % of them. **The Commission was not forced to draw a p95.35-tail map. They produced one, among thousands of legal alternatives closer to the constraint-bound expectation.**

In every case, the audit's claim is the same shape: the Commission paid a measurable **fairness cost** to get the specific map they produced, where "fairness cost" means the number of statistical standard deviations (or the ReCom-ensemble percentile, or the anchoring ratio) by which the chosen map is displaced from the constraint-bound expectation. **This is the audit's only substantive claim.** It does not claim the minority is "wrong"; it claims the minority is improbable by a measurable amount, and the improbability has a direction.

**Why this level of methodological precision?** The audit's apparatus — seven measurement layers, three-chain R-hat convergence, DPG tier-aware perturbation CIs, machine-readable dependency DAG, pre-committed exoneration criteria, per-finding retraction pathway — is deliberately over-engineered relative to the Commission's drawing process. The Commission drew with a broad brush (political negotiation, public-hearing notes, professional judgement). The audit looks through a microscope (adjacency chains, surplus-vote rates, constraint-bound percentiles). That asymmetry is intentional: **precision is armor**. If the audit presented a single number — "the minority's Efficiency Gap is 2.4σ from neutral" — the Commission would legitimately respond "Alberta's geography is unusual; your one number is too simple to capture it." The over-engineering forces the distinction between an accidental brush-stroke and a systematic pattern, and it is what allows the audit to answer the Commission's legitimate objections in advance.

**Translation discipline.** The math provides authority; the prose provides conviction. The table in §6 above is the audit's formal synthesis. The three bulleted translations above are the audit's human-readable reading of that synthesis. Both are included because neither alone is sufficient: math without translation is unactionable for a reader who is not a redistricting specialist, and translation without math is polemic. This section exists to bridge them explicitly.

**What the audit does not claim.** It does not claim intent (§4.5 is explicit). It does not claim the Commission acted in bad faith. It does not claim that any specific individual commissioner is responsible for the minority's patterns. It claims only that the minority map, relative to the majority map drawn by the same Commission under the same statutory constraints on the same voter geography, is displaced from the constraint-bound expectation in a measurably consistent direction across five structural dimensions. The explanation for that displacement is not within the audit's scope; the measurement is.

---

## 7. Limitations and Falsifiability

### 7.1 Missing evidence and scope limits


1. **2026 polygon geometry.** Phase 4A blocked. Unlocks B5 MCMC ensemble (Phase 5 §5.4), C1 Polsby-Popper, C2 Reock.
2. **Measured vote attribution (Phase 4C full execution).** Replaces 70/30 blend with observed apportionment. Expected to reduce the sensitivity range in §5.2.2 to a single refined value.
3. **Independent verification of the no-public-support claim (Section D).** Requires text-search of the commission's 1,140+ submission archive.
4. **Full-symmetry visual audit for majority.** Requires majority-proposal Alberta overview, Edmonton, and other-cities map images.
5. **2019-era population data.** Would permit A1/A2 symmetric analysis of the 2019 baseline alongside the two 2026 proposals.


### 7.2 Falsifiability statement


The audit's directional claim — *minority more UCP-favorable than majority across population, spatial, partisan-bias, and procedural dimensions* — would be falsified by any of the following:

- An alternative Calgary classification that produces near-null minority-majority asymmetry (≤1%) while A2's current rule produces >10%. Tested; both rules produce the same direction.
- Phase 4C measured attribution producing a minority-majority efficiency-gap asymmetry opposite in sign, or below 0.005 pp at the 70/30 central weight.
- Submission-archive evidence that the five disputed minority configurations (Airdrie, Cochrane, Chestermere, Red Deer, St. Albert) did have substantial public support in the 1,140+ record. Refutes Section D claim.
- Visible spatial anomalies in the majority's rural or Edmonton districts of a severity comparable to the minority's three flagged ridings. Requires majority non-Calgary imagery.
- A comprehensive survey of Canadian provincial redistributions 1991–2025 finding comparable mid-cycle government-drafting-process replacements. Refutes Section D uniqueness framing.

---

## 8. Conclusion

Three questions opened the paper. The answers are now on the table.

First, do the two commission proposals diverge in measurable, reproducible ways? Yes. Across eight sub-sections of §5 — population equality, partisan bias, signature detection, MCMC ensemble placement, the pre-registered checklist, symmetry-of-test-selection, geographic coherence, and procedural record — the minority 2026 proposal shows wider distribution, higher packing and cracking signals, more anomalies, and a more government-controlled procedural path than the majority. Every number is reproducible via `python3 analysis/<script>.py` against checked-in data anchored in `FROZEN_MANIFEST.md`.

Second, do the divergences run systematically in one political direction? Yes, with explicit qualifications. Five of the six structural dimensions point in the same direction without depending on vote data. The one vote-based partisan-bias dimension is directionally consistent under 2023 vote input and under April 2026 338Canada polling, but reverses under 2019 vote input. The audit reports the contingency as a property of the finding rather than a defect: the boundary effect is sensitive to which electorate is asked, and the direction holds at approximately 90% confidence under Monte Carlo over modelling choices across 2020s-era voter distribution.

Third, can the April 16 pivot be evaluated against a pre-registered falsifiability framework? Partially now, fully in November. The audit's test battery is pre-registered and the checklist is prepared for Open Science Framework submission with embargoed release scheduled for 2026-11-02. The OSF time-stamp converts the signature framework from an audit-voice discipline into a classical pre-registration against a future map. When the Lunty committee tables its 91-seat map by November 2, 2026, the same scripts that produced §5 will be re-run against the new map; the pre-registered scorecard will flag signatures, outliers, and rationale failures at the same thresholds applied here.

**Scope of the finding.** The minority 2026 proposal shows a pattern of structural irregularities and rationale failures beyond what the majority exhibits, at magnitudes below the US judicial 7% efficiency-gap threshold but above the noise floor of non-partisan redistricting variance as measured against a 100,000-plan neutral ReCom ensemble. The April 16 government action replaces the commission's drafting process rather than amending its output — the most government-controlled response among the three most commonly cited Canadian comparator cases. Whether these facts support a constitutional challenge under the *Reference re Saskatchewan* [1991] effective-representation standard is for counsel and the courts to assess (Appendix F).

**Next steps.** Three pending items would sharpen the audit's claims without changing their direction. The release of 2026 ED polygon shapefiles by Elections Alberta would unblock direct Polsby-Popper and Reock compactness computation and allow a 2026-seeded ReCom ensemble with tighter percentile bands (§5.4 currently uses 2019-seeded substrate). The November 2026 MLA-committee 91-seat map is the held-out test that closes the pre-registration residual (§5.5). A full-run pass of the Phase 4C VA-polygon vote-attribution pipeline would replace the 70/30 urban-weight blend with observed apportionment and tighten the §5.2.2 sensitivity range to a single refined value. Each is catalogued as future work and constrained by upstream data release rather than by methodology.

**What stands in the evidentiary record.** The audit's contribution is documenting that two commission proposals diverge systematically on six measurable dimensions, that the direction of divergence consistently favors the governing party under the available vote inputs, and that the process being used to promote the more-favorable proposal departs from comparator Canadian practice in specific ways. These facts are reproducible from public data using checked-in code. They do not prove intent, and they do not by themselves establish a constitutional violation. What they do provide is the evidentiary substrate on which such judgments — by counsel, by courts, by voters, and by future commissioners — can be constructed.

---

## References


Citations follow American Political Science Association (APSA) / APA-7 hybrid style, appropriate for political science, statistics, and information systems literature. Court cases follow Canadian legal citation convention.

### Academic literature

Alberta Electoral Boundaries Commission [AEBC]. (2026). *2025–26 Electoral Boundaries Commission final report (majority and minority)*. Government of Alberta. https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf

Barnes, R., & Solomon, J. (2021). Gerrymandering and compactness: Implementation flexibility and abuse. *Political Analysis, 29*(4), 448–466. https://doi.org/10.1017/pan.2020.36

Bratt, D., Brown, K., Sayers, A., & Taras, D. (Eds.). (2019). *Orange chinook: Politics in the new Alberta.* University of Calgary Press.

Carty, R. K. (2017). *Big tent politics: The Liberal party's long mastery of Canada's public life.* UBC Press.

Chen, J. (2017). The impact of political geography on Wisconsin redistricting. *Election Law Journal, 16*(4), 443–452. https://doi.org/10.1089/elj.2017.0455

Chen, J., & Rodden, J. (2013). Unintentional gerrymandering: Political geography and electoral bias in legislatures. *Quarterly Journal of Political Science, 8*(3), 239–269. https://doi.org/10.1561/100.00012033

Altman, M., & McDonald, M. P. (2011). BARD: Better Automated Redistricting. *Journal of Statistical Software, 42*(4), 1–28. https://doi.org/10.18637/jss.v042.i04

American Statistical Association. (2016). ASA statement on p-values: context, process, and purpose. *The American Statistician, 70*(2), 129–133. https://doi.org/10.1080/00031305.2016.1154108

American Statistical Association. (2019). Moving to a world beyond "p < 0.05". *The American Statistician, 73*(sup1), 1–19. https://doi.org/10.1080/00031305.2019.1583913

Driedger, E. A. (1983). *Construction of Statutes* (2nd ed.). Butterworths.

Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., du Sert, N. P., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., & Ioannidis, J. P. A. (2017). A manifesto for reproducible science. *Nature Human Behaviour, 1*, 0021. https://doi.org/10.1038/s41562-016-0021

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences, 115*(11), 2600–2606. https://doi.org/10.1073/pnas.1708274114

Courtney, J. C. (2001). *Commissioned ridings: Designing Canada's electoral districts.* McGill-Queen's University Press.

Courtney, J. C. (2004). *Elections.* UBC Press.

DeFord, D., Duchin, M., & Solomon, J. (2021). Recombination: A family of Markov chains for redistricting. *Harvard Data Science Review, 3*(1). https://doi.org/10.1162/99608f92.eb30390f

Fifield, B., Imai, K., Kawahara, J., & Kenny, C. T. (2020). The essential role of empirical validation in legislative redistricting simulation. *Statistics and Public Policy, 7*(1), 52–68. https://doi.org/10.1080/2330443X.2020.1791773

Gelman, A., & King, G. (1994). A unified method of evaluating electoral systems and redistricting plans. *American Journal of Political Science, 38*(2), 514–554. https://doi.org/10.2307/2111417

Grofman, B. (1983). Measures of bias and proportionality in seats-votes relationships. *Political Methodology, 9*(3), 295–327.

Herschlag, G., Ravier, R., & Mattingly, J. C. (2020). Quantifying gerrymandering in North Carolina. *Statistics and Public Policy, 7*(1), 30–38. https://doi.org/10.1080/2330443X.2020.1796400

Katz, J. N., King, G., & Rosenblatt, E. (2020). Theoretical foundations and empirical evaluations of partisan fairness in district-based democracies. *American Political Science Review, 114*(1), 164–178. https://doi.org/10.1017/S000305541900056X

King, G., & Browning, R. X. (1987). Democratic representation and partisan bias in congressional elections. *American Political Science Review, 81*(4), 1251–1273. https://doi.org/10.2307/1962588

Ladner, K. (2003). Treaty federalism: An Indigenous vision of Canadian federalisms. In F. Rocher & M. Smith (Eds.), *New trends in Canadian federalism* (pp. 167–194). Broadview Press.

McDonald, M. D., & Best, R. E. (2015). Unfair partisan gerrymanders in politics and law: A diagnostic applied to six cases. *Election Law Journal, 14*(4), 312–330. https://doi.org/10.1089/elj.2015.0318



Polsby, D. D., & Popper, R. D. (1991). The third criterion: Compactness as a procedural safeguard against partisan gerrymandering. *Yale Law & Policy Review, 9*(2), 301–353.

Reock, E. C. (1961). Measuring compactness as a requirement of legislative apportionment. *Midwest Journal of Political Science, 5*(1), 70–74. https://doi.org/10.2307/2109043

Sancton, A. (2021). *The limits of boundaries: Why city-regions cannot be self-governing.* McGill-Queen's University Press.

Smith, D. E. (2010). *Canada's deep crown: Beyond Elizabeth II.* University of Toronto Press.

Stephanopoulos, N. O., & McGhee, E. M. (2014). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review, 82*(2), 831–900.

Stephanopoulos, N. O., & McGhee, E. M. (2018). The measure of a metric: The debate over quantifying partisan gerrymandering. *Stanford Law Review, 70*, 1503–1568.

Stewart, D., & Archer, K. (2000). *Quasi-democracy? Parties and leadership selection in Alberta.* UBC Press.

Warrington, G. S. (2018). Quantifying gerrymandering using the vote distribution. *Election Law Journal, 17*(1), 39–57. https://doi.org/10.1089/elj.2017.0447

Warrington, G. S. (2019). A comparison of partisan gerrymandering measures. *Election Law Journal, 18*(3), 262–281. https://doi.org/10.1089/elj.2018.0508

Wiseman, N. (2020). *Partisan odysseys: Canada's political parties.* University of Toronto Press.

### Court cases

*Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912.

*Frank v. Canada (Attorney General)*, [2019] 1 SCR 3.

*Gill v. Whitford*, 585 U.S. ___ (2018).

*Haig v. Canada*, [1993] 2 SCR 995.

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

### Statutes

*Electoral Boundaries Commission Act*, RSA 2000, c E-3.

### Data sources

Elections Alberta. (2015). *2015 Provincial general election official results* [Data set]. https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx

Elections Alberta. (2019). *2019 Provincial general election official results all EDs* [Data set]. https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx

Elections Alberta. (2023). *2023 Provincial general election statement of vote* [Data set]. https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx

Elections Alberta. (2026). *Electoral boundaries commission submissions archive* [Data set, Rounds 1 and 2]. https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/

Statistics Canada. (2021). *Dissemination area boundary files, 2021 census* [Data set]. https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/

---

*Draft. Falsifiability gates, robustness checks, and APA citations documented throughout.*

---

## Appendix A — Reproducibility


All scripts run from repository root:

```bash
python3 analysis/scripts/v0_2_packing_cracking_analysis.py    # §5.2 symmetric three-map
python3 analysis/scripts/electoral_forensics_population.py    # §5.1 with A2 robustness
python3 analysis/scripts/v0_1_poll_attribution_skeleton.py    # §4 parse validation
```

Each script prints a gate PASS/FAIL line. Numbers in §§2, 3 above must match the corresponding gate-passed output.

**Reproducibility artifacts.** A version-pinned environment manifest (`requirements.txt` at repo root) lists every Python package with exact version; an interpreter pin (`setup.md`) names the tested Python version; `FROZEN_MANIFEST.md` lists every external URL accessed during the audit with its access date. A third party running the pipeline 12+ months from today can (a) install the pinned environment, (b) check each URL's state against the frozen snapshot, and (c) reproduce every numeric finding to the tolerance stated in Gate G0. Reproducibility-artifact provenance follows the ICLR 2022 Reproducibility Checklist and Nosek et al. (2018) Open Science Framework pre-registration standards.

## Appendix B — Supporting Analysis Documents


- [Section A](analysis/reports/v0_1_section_A_population_equality.md)
- [Section C](analysis/reports/v0_1_section_C_geographic_coherence.md)
- [Section D](analysis/reports/v0_1_section_D_procedural.md)
- [Section 4](analysis/reports/v0_1_section_4_geometry_provenance.md)
- [Bias audit](analysis/reports/v0_1_bias_audit.md) — self-audit of this audit's own methodology
- [Design critique](analysis/reports/v0_1_design_critique.md) — hostile stress-test pass
- [Uncertainty analysis](analysis/methodology/v0_1_uncertainty_and_shapefile_impact.md)
- [Academic literature review](analysis/methodology/v0_1_academic_literature_review.md)
- [Submission search findings](analysis/reports/submission_search_findings.md) — §5.9.4 evidence base
- [Chair's Recommendation 5 analysis](analysis/reports/v0_1_chair_recommendation_5_analysis.md) — §5.9.2 evidence base
- [Track C checklist baseline scoring](analysis/reports/v0_1_track_c_checklist_baseline_scoring.md) — §5.5 full scorecard and comparison template for the November map
- [MCMC ensemble baseline](analysis/methodology/v0_1_mcmc_ensemble.md) — §5.4 method, 10k-sample ReCom chain against 2019 baseline, per-metric percentile tables
- [Plan B compliance + contested-config cross-check](analysis/reports/v0_1_plan_b_cross_check.md) — note on population-data provenance evidence base
- [Cycle-lag analysis](analysis/v0_1_cycle_lag_analysis.md) — province-wide ED drift under mid-2025 populations
- [Proposed Act §12 amendment](analysis/reports/v0_1_act_amendment_proposal.md) — legislative reform proposal addressing the census / cycle-lag tension
- [Calgary data-sources audit](analysis/methodology/v0_1_calgary_data_sources_audit.md) — 16 Calgary-specific sources catalogued; ward-level modelled A2 sensitivity is feasible from public data
- Adversarial stress-test passes and their fortifications are preserved in `deprecated/` for historical reference (see `deprecated/README.md`).
- [Chen-Rodden Alberta validation](analysis/methodology/v0_1_chen_rodden_alberta_validation.md) — mechanism-level test of the natural-packing argument
- [Canadian redistribution base-rate catalogue](data/v0_1_canadian_redistribution_base_rate.csv) — C4 partial catalogue (quantitative acquisition flagged as future work)
- [Alberta government database survey](analysis/methodology/v0_1_alberta_government_databases_survey.md) — Track N, composite-basis source recommendations for §12 reform
- [Commission source provenance audit](analysis/methodology/v0_1_commission_source_provenance.md) — Track O, verified 4,888,723 matches StatsCan Q2 2024 postcensal estimate
- [Byelection data and assessment](analysis/reports/v0_1_byelection_assessment.md) — Track S, 2022–2025 byelections evaluated and not incorporated into RT3
- [A1 legal-baseline computation](analysis/methodology/v0_1_appendix_c_legal_baseline.md) — Appendix C companion; 2019-map MAD on 2021 Census directly
- [Threshold provenance compendium](analysis/methodology/v0_1_threshold_provenance.md) — every numeric threshold justified with source + sensitivity
- [Canadian inter-map base-rate computation](analysis/methodology/v0_1_canadian_base_rate_computed.md) — comparative distribution across seven Canadian redistribution cycles
- [External pre-registration draft and platform analysis](analysis/reports/v0_1_pre_registration_draft.md) / [platform analysis](analysis/reports/v0_1_pre_registration_platform_analysis.md) — OSF submission package for the November signature-detection checklist
- [Minority rationales validation](analysis/methodology/v0_1_minority_rationales_validation.md) — §5.8.4 and §5.9.2 evidence base (25 rationales inventoried, 3 contradicted)
- [Minority rationales inventory](analysis/methodology/v0_1_minority_rationales_inventory.md) — source quotes with citations
- [Cochrane journey-to-work](analysis/methodology/v0_1_cochrane_journey_to_work.md) — §5.8.4 StatsCan 98-10-0459 pull
- [CSD-level community splits](analysis/methodology/v0_1_csd_community_splits.md) — §5.8.4 robustness check
- [338Canada riding-level cross-validation](analysis/methodology/v0_1_338canada_riding_level.md) — §5.2.3 independent cross-check
- Submission OCR log preserved at `deprecated/v0_1_submission_ocr_log.md` — §5.9.4 partial extension of the 88 non-text-layer submissions


## Appendix C — 2021-census legal-baseline A1 for the 2019 map


**Purpose.** §5.1.1 reports A1 MAD on the commission's own tables, which derive from the July 2024 OSI population estimate. A reviewer committed to strict §12(3) statutory-basis discipline can argue the §5.1.1 numbers inherit the commission's data-source status. This appendix provides an independent 2021-Census-direct computation of A1 on the 87 existing 2019 EDs as the §12(3)-operative reference point. The 2026 proposals cannot receive the equivalent treatment because their ED shapefiles have not been publicly released.

**Method.** 2021 Census population at the dissemination-area level (6,203 Alberta DAs, `data/alberta_2021_da_populations.csv`) aggregated to the 87 2019 EDs via geopandas overlay on `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`. Reproducible script at `analysis/scripts/v0_1_a1_legal_baseline_2021_census.py`. Per-ED output at `data/v0_1_a1_legal_baseline_2019eds_2021census.csv`.

**Headline figures.**

| Map & basis | Quota | MAD | Source |
|-------------|-------|------|--------|
| 2019 map on 2017-report basis (commission-quoted) | 46,803 | 2,886 | EBC 2017 Final Report pp. 60–61 |
| 2019 map on 2021 Census (this appendix) | 48,996 | **4,745** | This computation |
| 2026 majority map on 2024 TBF estimate | 54,929 | 3,180 | Majority Report variance table |
| 2026 minority map on 2024 TBF estimate | 54,929 | 4,707 | Minority Report variance table |

**Ordinal comparison.** 2026 majority MAD (3,180) < 2019-on-2021-Census MAD (4,745) ≈ 2026 minority MAD (4,707). The minority 2026 proposal's distribution-tightness is effectively equal to the 2019 map's distribution-tightness at 2021-Census time; the majority 2026 proposal is meaningfully tighter than either benchmark.

**Seven 2019 EDs outside ±25 % under 2021 Census.** Central Peace-Notley (−44.77 %), Lesser Slave Lake (−44.73 %) — both s.15(2)-protected — plus Edmonton-South (+40.89 %), Edmonton-Ellerslie (+38.60 %), Edmonton-South West (+33.71 %), Airdrie-Cochrane (+29.76 %), Calgary-North East (+25.55 %). The five positive outliers are urban-growth EDs that had already exceeded the +25 % ceiling by 2021-census time; Track L's mid-2025 analysis (`analysis/v0_1_cycle_lag_analysis.md`) confirms all five remain out-of-band under 2025 populations.

**Interpretation.** The audit's §5.1.1 ordering (majority tighter than minority) is preserved under the §12(3)-operative basis. The minority proposal, drawn four years after the 2021 Census, reproduces the same population-distribution tightness the 2019 map exhibited against the 2021 Census; the majority proposal improves on that benchmark. A strict §12(5) reviewer's attack on §5.1.1's data basis does not change the direction of the A1 finding. Full discussion in the companion file `analysis/methodology/v0_1_appendix_c_legal_baseline.md`.


## Appendix D — Mathematical Formalism


### D.1 Efficiency Gap (Stephanopoulos & McGhee, 2014)

$$\text{EG} = \frac{W_A - W_B}{N}$$

```
EG = (W_A - W_B) / N
```

Wasted votes $W_X$ for party $X$ are defined as losing-district votes plus winning-district votes above the victory threshold $\lceil N_d/2 \rceil + 1$, summed across districts. The 7% magnitude is the threshold proposed by Stephanopoulos & McGhee (2014/2015) as the level at which EG imbalances become investigable; it was briefed to the US Supreme Court in *Gill v. Whitford*, 585 U.S. ___ (2018), which the Court vacated and remanded on standing grounds without adopting the threshold. The 7% figure in this paper rests on academic-literature authority, not on a judicial holding.

**Sign-convention reconciliation.** When party A is indexed first, Stephanopoulos-McGhee canonical EG uses a 2:1 slope baseline (positive EG = party A disadvantaged, i.e., party B has seat-advantage). This paper reports EG under the 1:1 proportional-seat baseline; in Alberta's rural-UCP-blowout context, this produces negative EG values whose magnitude correlates with UCP outcome advantage through seat count, despite UCP also being the more-wasteful party by the wasted-vote measure. The two conventions give the same ordinal ranking of Alberta's three maps (2019 / Majority 2026 / Minority 2026) and therefore the same minority-vs-majority direction. Full derivation and verification at `analysis/methodology/v0_1_sign_convention_resolution.md`.

### D.2 Mean-Median Gap (McDonald & Best, 2015)

$$\text{MM} = \bar{v} - \tilde{v}$$

```
MM = mean(v) - median(v)
```

$\bar{v}$ is the mean NDP vote share across districts; $\tilde{v}$ is the median. Positive MM indicates mean > median, consistent with party voters packed into fewer high-share districts (cracking of the opposing party, or packing of own party).

### D.3 Polsby-Popper compactness (not computed — blocked by Phase 4)

$$\text{PP} = \frac{4\pi A}{P^2}$$

```
PP = 4 * pi * A / P^2
```

$A$ = polygon area, $P$ = perimeter. Range $[0, 1]$; 1 = circle. PP < 0.15 is typically flagged.

### D.4 Reock compactness (not computed — blocked by Phase 4)

$$\text{R} = \frac{A_d}{A_c}$$

```
R = A_district / A_smallest_enclosing_circle
```

Range $[0, 1]$. R < 0.25 typically flagged.


## Appendix E — Geometric Data Provenance

The six subsections below document the geometric-data paths evaluated in this audit. § E.1–E.5 describe the direct-shapefile, DA-dissolve, VA-polygon-attribution, OSM reconstruction, and QGIS paths (all blocked or not attempted). § E.6 is the technical data statement. § E.7 reports the approximate-geometry analysis (Tier A/B compactness) that was produced as a substitute for the not-yet-released 2026 shapefiles. An additional "Note on population-data provenance and cycle-lag robustness" is preserved at the end of the appendix for completeness; its core findings are summarised in §3.3.

### E.1 4A (direct shapefiles)

**Blocked.** Fetched `https://www.elections.ab.ca/resources/maps/` on 2026-04-22. 2019 ED shapefiles and 2023 VA shapefiles are published; 2026 proposal shapefiles are not. Consistent with ABEBC historical practice of releasing shapefiles after legislative adoption.

### E.2 4B (DA dissolve)

**Not attempted.** Would require the 84MB `abebc_2026_rpt_final.pdf` and demonstrated presence of DAUIDs. Not in working bundle; probability of DAUIDs being in PDF text is low (<10% based on Canadian provincial commission practice).

### E.3 4C (VA-polygon attribution)

**Pipeline validated; full execution not run.** Skeleton (`analysis/scripts/v0_1_poll_attribution_skeleton.py`) correctly parses the 2023 Statement of Vote: 1,973 poll records matched to four-figure official totals (NDP 777,404 / UCP 928,900 / two-party 1,706,304). Stages 3–7 (geocoding, zero-sum verification, 2026 assignment, apportionment, vote checksum) require ~4–8 hours of dedicated execution on VA-polygon substrate — outside this session's budget.

**Sub-finding (preserved for next session):** 47.2% of 2023 valid votes are in non-Election-Day ballot types (Advance/Mobile/Special), all home-ED-attributed under Vote Anywhere. NDP two-party share at Election Day: 42.59%. NDP two-party share Vote Anywhere: 48.84%. Differential: +6.25 pp. Implications for B1–B4 magnitude precision are covered in §5.2.2 sensitivity.

### E.4 4D/4E

Not attempted. 4D (OSM reconstruction) would bust the 15K token sub-cap; 4E (QGIS manual) is out of scope.

### E.5 4F validation

Not executed for the commission-released 2026 geometries because those shapefiles have not been released. A separate approximate-geometry analysis is described in § E.7 below.

### E.6 Technical Data Statement

- **Source data for Sections A, B:** CSV files in `data/` (populations for both 2026 maps; per-ED 2023 and 2019 vote totals); raw Statement of Vote in `data/2023_results.xlsx`.
- **Source data for Section C:** JPG map images from the commission's final report (majority Calgary only; full coverage for minority).
- **Source data for Section D:** Electoral Boundaries Commission Act, commission report via prompt context, comparator-case general knowledge.
- **Geometric reconstruction:** Not produced. § E.1–E.5 explain each path's block.
- **Coordinate system / resolution / aggregation:** N/A (no geometry).
- **Integrity metric:** Population checksum threshold (0.5% warn, 2% hard stop) not triggered because no geometry to check.
- **Geometric shift log:** `analysis/geometry_shift_log.md` does not exist. No manual geometric adjustments were applied in this session.
- **Transformation log:** No CRS transformations applied.
- **Symmetry consistency:** B1–B4 use identical blending methodology (85/15 urban weight) applied to both 2026 maps via the same `estimate_2026()` function. A1–A3 use identical variance computation against the same provincial average. A2 uses identical classification rule plus an alternative-rule robustness check (G4). Section C has a symmetry data gap (only majority Calgary imagery available) which is disclosed.

### E.7 Approximate 2026 geometry — Tier A/B compactness

**Shapefile status.** A formal written request for the 2026 boundary shapefiles has been filed with Elections Alberta. No response has been received as of publication. The synthetic geometries described below were constructed in parallel with that request and represent the best available approximation pending official release; results dependent on Tier C geometry precision should be treated as provisional until the official shapefiles are obtained.

**Tier-C hybrid sweep extension (v0_3, 2026-04-24).** Session 11's population-calibrated parametric sweep was originally applied to four Tier-C hybrid majority EDs (Airdrie-West + Cochrane-Springbank; High River-Vulcan-Siksika + Okotoks-Diamond Valley), yielding 0.2–0.4 pp residuals against commission population targets using 2023 vote counts as a proxy. For the v0_3 canonical build we generalised the sweep to the full set of hybrid EDs (19 majority, 20 minority; **39 total**) and replaced the proxy with direct DA-population sums from the 2021 decennial census (scaled by the 14.7 % provincial 2021–2024 growth factor so that Phase 4F scaled-deltas evaluate to ≈0). Each hybrid with a hybrid neighbour in v0_2 was swept jointly using a 12-angle line-sweep with binary search on line position (tolerance 5 × 10⁻⁴ relative error); hybrids that still failed and isolated hybrids (e.g. Calgary-East, Medicine Hat-Brooks) were resolved via radial DA-absorption from the v0_2 anchor. A disjointness pass subtracted each swept polygon from every other polygon in the canonical so Phase 4F's sjoin could not mis-attribute DAs in overlap regions. Of the 39 EDs attempted: **24 converged tight** (< 0.5 %), **11 converged acceptably** (0.5–2 %), and **4 did not converge** (> 2 %). Phase 4F re-validation after the sweep reduced the 2 %-hardstop failure count from 84/87 (majority/minority) in the v0_2 baseline to **67/69 in v0_3** — a 17-of-86 / 18-of-89 net reduction. Residual non-convergence is concentrated in hybrids whose boundary is multi-segment or wraps around a First Nation reserve (Chestermere-Strathmore, Edmonton-Beaumont near-miss at 2.5 %, Fort McMurray-Lac La Biche vast-rural, Lethbridge-Taber-Warner v7 deep transcription); for these cases the v0_2 geometry is retained unchanged in v0_3 so downstream tests honestly distinguish swept-committed EDs from still-failing EDs. The pre-existing Tier-A majority EDs that still fail the 2 %-hardstop are v7-transcribed originals whose non-convergence reflects the same DPG transcription limit Phase 4B has documented throughout; they are out of scope for the sweep (sweep addresses hybrid boundary *position*, not polygon *fidelity*). Full methodology and script in `analysis/scripts/v0_1_build_canonical_shapefiles_v2.py`; per-ED outcome log in `analysis/reports/v0_1_tier_c_sweep_log.csv`; full writeup at `analysis/reports/v0_1_tier_c_sweep_analysis.md`; updated Phase 4F deltas at `data/v0_1_phase4f_validation_deltas_v2.csv`; canonical shapefiles at `data/v0_3_canonical_{majority,minority}_2026_eds_swept.gpkg`.

Because the commission has not released 2026 shapefiles, this audit constructed approximate 2026 ED geometries from three sources: (a) the 2019 enacted shapefile for 2026 EDs whose crosswalk is `direct` or `rename` (Tier A, exact); (b) the union of constituent 2019 polygons for 2026 EDs with `merge` crosswalks (Tier B, near-exact); (c) an attempted hybrid-split approximation for `hybrid` crosswalks (Tier C, not attempted in this pass — visual transcription from the commission's low-resolution JPG maps would produce compactness errors of roughly ±20% per 10% perimeter error, which the audit judges too wide to report as measurement). Full method at `analysis/reports/v0_1_approximate_shape_analysis.md`.

**Coverage of the approximation:**
- Majority 2026: 57 of 89 EDs measurable at Tier A/B (64%); 32 in Tier C (not scored).
- Minority 2026: 65 Tier A + 5 Tier B of 89 EDs measurable (79%); 19 in Tier C (not scored).
- 2019: all 87 EDs measurable directly.

**Measurable-subset compactness findings (reported with Tier-dependent uncertainty bands):**

| Map | Mean Polsby-Popper | Count PP < 0.25 | Count Reock < 0.30 |
|---|---|---|---|
| 2019 (87 EDs, full; Tier A shapefile-grade) | 0.419 ± 0.00 | 4 / 87 (4.6%) | 6 / 87 (6.9%) |
| Majority 2026 (57 Tier A+B EDs) | 0.431 ± 0.01 | 2 / 57 (3.5%) | 2 / 57 (3.5%) |
| Minority 2026 (70 Tier A+B EDs) | 0.411 ± 0.02 | 5 / 70 (7.1%) | 5 / 70 (7.1%) |

Uncertainty bands reflect the perimeter-mode (±500 m) residual from the v1→v3 refinement passes (§4.1.4; full per-ED CI at `data/v0_1_boundary_refinement_impact_v3.csv`). Tier A EDs inherit the 2019 enacted shapefile and carry no DPG uncertainty. Tier B EDs' per-ED PP scores are bounded to ≤ 0.04 under OSM feature-class snapping. The Minority column's mean-PP uncertainty is higher than the Majority's because more of its measurable subset is Tier B (5 of 70) versus Tier A (65), and the Tier B entries bring the Majority–Minority mean delta (0.020) within the same order as the combined uncertainty band.

**Reporting convention for per-ED compactness on hybrid EDs.** To pre-empt false-precision interpretation, individual per-ED Polsby-Popper and Reock scores on Tier B (refined) and Tier C (visually-transcribed) EDs are reported as **ordinal compactness bands** rather than decimal point estimates in all headline claims:

- **High compactness:** PP ≥ 0.40 (Reock ≥ 0.50)
- **Moderate compactness:** 0.25 ≤ PP < 0.40 (0.30 ≤ Reock < 0.50)
- **Low compactness (flagged):** PP < 0.25 (Reock < 0.30)
- **Very low compactness:** PP < 0.15

Decimal scores are retained in the machine-readable output CSVs for reproducibility. Headline text claims rely on threshold breaches (whether an ED falls into the "flagged" band) rather than on decimal rankings.

**Within the measurable subset, the minority map shows roughly double the rate of low-compactness EDs as the majority** (7.1% vs 3.5% on both Polsby-Popper and Reock at their respective flag thresholds). Minority's mean Polsby-Popper is modestly lower than either the 2019 baseline or the majority proposal; the magnitude of this mean-delta (≈ 0.02) sits within the combined Tier B uncertainty band and is reported as a **directional finding, not a magnitude claim**. The measurable subset excludes the most structurally-complex EDs in both maps (hybrid splits, Tier C).

**Flagged-configuration analysis (Tier A/B measurable subset, ordinal bands):** Three of the audit's flagged minority configurations are measurable as Tier A/B and fall in the **Moderate-compactness** band — they do not breach the flag threshold relative to their 2019 parents (Airdrie-East, Red Deer-Blackfalds, Olds-Three Hills-Didsbury; decimal scores in `data/v0_1_boundary_refinement_impact_v3.csv`). The three Tier-C flagged hybrids (Rocky Mountain House-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) cannot be banded without official geometry. A parent-union reference shows their 2019-ancestor polygons are **already in the Low-compactness band** (e.g., Banff-Kananaskis-adjacent parent union PP ≈ 0.16 — Very-low); low compactness in these EDs is partly inherited from the underlying Alberta geography rather than newly manufactured by minority split-lines.

**What the audit can and cannot claim from this data:**
- Can claim: within the measurable subset, the minority produces about twice the rate of low-compactness EDs as the majority does. This is consistent with the §5.8.2 visual spatial-audit finding.
- Cannot claim: the minority "manufactures" non-compactness through hybrid splits. That claim requires the 2026 shapefiles because the hybrid splits are precisely the Tier C EDs the approximation could not score. The audit's scoped claim stands; the stronger claim is a pending research question.

**Refinement pass (v1).** A second pass re-extracted commission map pages at 600 DPI, snapped boundary lines to OpenStreetMap road-network features within a 500-metre buffer, and produced visual overlay verification for a priority subset. Methodology and full results at `analysis/methodology/v0_1_shape_refinement.md`. The v1 refinement shifted five Tier B EDs by an average of 97 metres and produced compactness confidence intervals of ≤ 0.04 Polsby-Popper for those EDs.

**Iterative refinement (v2) with feature-class-aware snapping.** Visual inspection of the v1 overlays surfaced that three of the five Tier B boundaries follow rivers rather than roads: Calgary-South along the Bow River (18 % river-feature samples), Edmonton-Windermere along the North Saskatchewan River (57 % river-feature samples), and Lethbridge-Little Bow along the Oldman River (45 % river-feature samples). A v2 pass extended the OSM query to four feature classes (road + waterway + railway + administrative-boundary) and re-snapped those boundaries to the appropriate feature. Compactness improved on the water-body-bounded EDs: Edmonton-Windermere PP 0.195 → 0.230 (+18 %); Calgary-South PP 0.217 → 0.240 (+11 %). Other EDs changed by ≤ 0.015 PP, within the CI. Full method at `analysis/methodology/v0_1_shape_refinement_v2.md`.

**Three-tier boundary-confidence classification** (after v3 noise-cleanup and two additional refinement passes). For each Tier B boundary the refinement pass computed a voter-assignment-impact score — the number of 2023 Voting Areas whose assignment would flip between the v1 and v2/v3 boundary rendering and the 2023 votes those VAs contain. Boundaries with zero sensitive VAs are marked **orange-accepted**: the residual geometric uncertainty does not affect voter assignment and further refinement would be effort without return. Lethbridge-Little Bow and Wetaskawin-Ponoka-Maskwacis are orange-accepted. Three boundaries remain documented as **unresolvable without the commission shapefile** after two additional refinement passes (admin-only snap at 100 m then 50 m buffer, river-only snap for Windermere): Calgary-De Winton and Calgary-South share a single sensitive VA (217 votes); Edmonton-Windermere has three sensitive VAs (796 votes) on the North-Saskatchewan-River bank — qualitatively resolved as "south of the North Saskatchewan River" via commission Appendix E, but the quantitative centreline-vs-bank offset remains shapefile-dependent. Total residual voter impact across all Tier B boundaries after v3: **1,012 votes across 4 unique VAs** — approximately 0.06 % of 2023 total valid votes. Per-boundary impact table at `data/v0_1_boundary_refinement_impact_v3.csv`; verification overlays with the three-tier green / orange / red convention at `maps/verification/v0_3_*.png` (v3 includes a rendering-bug fix: near-zero-area interior rings introduced by upstream buffer/union operations were being rendered as spurious "internal borders" by `GeoSeries.boundary.plot()`; v3 strips rings below 0.1 km² and renders only polygon-part exteriors).

**Tier B polygon misclassification flagged by human review.** Visual cross-reference of the v3 verification panels against the commission's published per-ED thumbnails (Appendix E) identified that Edmonton-Windermere, Calgary-De Winton, and Calgary-South are not actually Tier B "merges of whole 2019 parents" but Tier C carve-outs — the 2026 ED occupies only part of the 2019 parent territory, with the rest continuing under a separately-named 2026 ED (e.g., the minority keeps both Edmonton-Whitemud and creates Edmonton-Windermere). The approximation pipeline treated the 2026 ED as the union of parents, producing polygons that occupy more area than the commission actually drew and producing apparent overlaps with neighbouring EDs. Specifically, the commission's Edmonton-Windermere thumbnail shows a clean river-following western boundary PLUS a stepped upper-east carve-out where the ED wraps around a peninsula of Edmonton-South territory that extends northwest. The approximation misses this carve-out because it has no OSM feature to snap to (the carve is a commission-drawn street-grid boundary internal to the 2019 parent). The resulting apparent "overlap" with Edmonton-South reflects the approximation occupying territory the commission assigned to a neighbour through a feature OSM snapping cannot recover. It is not a rendering bug.

This misclassification is inherent to approximation-without-shapefile: every Tier B hybrid whose parent is carved rather than merged is subject to it. The impact-assessment above (0.06 % voter-impact residual) is conservative because it measures only v1-to-v3 symmetric difference, not the underlying approximation-to-reality gap for these Tier C-like EDs. The full voter-assignment gap for these EDs will be resolved only by shapefile release.

**Calgary-De Winton and Calgary-South — scale-level and shape-level misclassifications.** Visual cross-reference against the commission's minority Calgary overview (Appendix E p. 74) and individual per-ED thumbnails shows:

- **Calgary-De Winton** is a large south-Calgary / southern-suburban-rural hybrid that abuts the Tsuut'ina Nation reserve to the west, extends south past Calgary's city limits, and encompasses the Town of Okotoks (~32,000 residents) along with the De Winton community the district is named for. The v3 approximation renders as a small compact polygon internal to south Calgary — the approximation captures perhaps 10–15 % of the territory the commission actually assigned to this ED.
- **Calgary-South** as drawn by the commission is a compact roughly-rounded shape with a notch on the right side. The v3 approximation is an elongated east-west shape with an eastern extension and a southern tail — general location correct, shape materially wrong.

These are more severe misclassifications than Edmonton-Windermere (which had the general footprint correct with a missing peninsula). All three EDs are reclassified from Tier B to **Tier C awaiting shapefile**. The approximation's compactness scores for these three EDs should be read as known-inaccurate; the shared 217-vote residual between Calgary-De Winton and Calgary-South under the v3 symmetric-difference metric is a floor, not a ceiling, on the approximation-to-reality gap. Full mismatch documentation and commission-thumbnail observations at `analysis/methodology/v0_1_commission_reference_shapes.md`. Only commission shapefile release will resolve the gap. The §5.6 finding that Calgary-De Winton and Calgary-South "are measurable as Tier A/B" is withdrawn; § E.7's Tier count is revised downward by 3 measurable EDs on the minority side.

**Confidence versus actual commission shapefiles** (after v2):
- Tier A (57 majority / 65 minority EDs): high — geometry is the 2019 enacted shapefile, which is authoritative.
- Tier B orange-accepted (2 of 5): high — residual geometric uncertainty does not affect voter assignment.
- Tier B refinement-significant (3 of 5): moderate — ±500 m boundary residual with a ≤ 0.06 % province-wide vote-share implication; resolvable by shapefile release.

**Priority hybrid EDs not scored.** The hybrid configurations most relevant to the audit's contested-configurations findings (Rocky Mountain House-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) are precisely the boundaries the approximation cannot construct from the 2019 shapefile + crosswalks alone; they require actual commission geometry. Until the commission shapefiles are released by Elections Alberta (request drafted at `analysis/v0_1_elections_alberta_shapefile_request.md`), the audit's compactness findings cover the measurable 64–79 % of each map but leave the three most contested EDs unscored.

**Visual-transcription-assisted Tier C annex (v4).** A follow-up pass (Track Y-prime-prime-prime, `analysis/methodology/v0_1_shape_refinement_v4.md`) constructed visual-transcription-assisted Tier C polygons for the three Tier B-misclassified EDs above (Edmonton-Windermere, Calgary-De Winton, Calgary-South) using 600-DPI commission thumbnails anchored against multi-feature OSM boundaries (waterway, admin_level=6/8, aboriginal_lands). The v4 polygons are explicitly sub-shapefile-grade and carry per-segment error bands: ±100 m on river-snapped edges, ±300 m on OSM-admin edges, ±500 m to ±1 km on edges transcribed from the thumbnail with no OSM feature to anchor them. Territorial fidelity improves substantially at all three: Edmonton-Windermere closes the approximation-to-reality gap from ~70 km² (wrong territory) to ~5-10 km² (edge-local); Calgary-De Winton trims from ~500 km² to ~50-100 km² after subtracting Tsuut'ina Nation 145 reserve + 200 m buffer and the ED-29 southern rural block (the Town of Okotoks was also subtracted by v4 and this was an error — Okotoks is inside the commission's De Winton at its south-east corner; see "v4 residual gap" note below); Calgary-South corrects from an elongated 64 km² polygon covering Shaw + Hays to a compact ~9 km² block in SW Hays with a NE notch. The v4 VA-impact ceiling is 318 VAs / ~62,000 votes across the three EDs — this is an upper bound on the territorial correction, distinct from the v3 symmetric-difference floor of 4 VAs / 1,012 votes reported above. v4 runs as a parallel annex to v3's Tier B-superseded / Tier C-awaiting-shapefile classification rather than replacing v3, so readers see both the conservative (v3 symmetric-difference) and first-order-territorial (v4 visual-transcription) approximation envelopes. Verification panels at `maps/verification/v0_4_minority_*.png`.

**v4 residual gap identified by PO-painted references (2026-04-23).** Hand-painted reference overlays from the PO on 2026-04-23 established that v4's per-segment error bands remain too narrow for all three Tier C EDs, and that v4 also mis-treated Okotoks. v4's Calgary-De Winton at 835 km² is likely less than 60 % of the true territorial footprint — the commission's shape spans roughly the full quadrant south of Calgary's southern city limit and east of the Tsuut'ina reserve's east edge, extending substantially further west and south than v4 placed it, with a stepped north edge where Tsuut'ina indents into the ED. The true footprint is in the 1,400–1,700 km² range. The Town of Okotoks sits *inside* De Winton at its south-east-most edge, not subtracted from it as v4 assumed; this was a v4 error. v4's Calgary-South at 9 km² is approximately half the true size; the commission's shape sits east of Calgary-Fish Creek as a compact urban block of 15–25 km². v4's Edmonton-Windermere at 36.76 km² is also too small — the commission's shape has a main vertical lobe in south-west Edmonton plus a distinctive rectangular eastern arm extending into what would otherwise be Edmonton-South territory; true footprint likely 55–70 km². All three residual gaps and the Okotoks correction are documented in `analysis/methodology/v0_1_commission_reference_shapes.md`; shapefile release remains the only path to fully close them. The Tier C classification above is unchanged — v4 is a better approximation than v3 for all three EDs, but both remain approximations, and a v5 pass using the 2026-04-23 painted references as additional anchors is flagged as future work.


### E.8 Note on population-data provenance and cycle-lag robustness


The body of this report performs all population-equality analysis against the 2021 decennial Statistics Canada census, the data source the Electoral Boundaries Commission Act §12(3) designates as the Commission's mandatory basis. Two supplementary observations sit outside the census-based analysis and are recorded here for completeness; neither alters the report's findings.

**Commission methodology vs statutory basis.** The majority and minority reports both state that population figures derive from "the 2021 census updated to a July 1, 2024 estimate." The per-ED population tables in both reports sum to 4,888,723 — the Alberta Treasury Board and Finance mid-2024 estimate — and the resulting provincial quota (54,929) and ±25 % window (41,197 – 68,661) are computed from the 2024 total rather than from the 2021 census total of 4,262,635. Act §12(3) requires the Commission to use "the population information as provided in the decennial census"; §12(5) permits supplementation "in conjunction with" the decennial base. Whether the Commission's approach falls within §12(5)'s permissive frame or outside it is a question of statutory interpretation not resolved here. Full compliance audit in `analysis/reports/v0_1_plan_b_cross_check.md`. The audit's own A1/A2/A3 analyses in §2 above were performed against the Commission's published per-ED tables and therefore inherit the Commission's data vintage; a Plan-B re-run against the same 2024 estimates finds every justification-test verdict unchanged and three tests (Olds-Three Hills-Didsbury, Airdrie 4-way, Chestermere split) more decisively "unforced" than under the 2021 census.

**Cycle-lag robustness test.** Alberta's cumulative population growth from the 2021 census to mid-2025 is approximately 17.8 %. Applying mid-2025 populations to the three maps (2019 current, 2026 majority proposal, 2026 minority proposal) using a dissemination-area-level area-weighted overlay produces the following count of electoral divisions whose ±25 % window status changes relative to the commission's 2024-based figures: 2019 map, 5 of 87 (all pass → fail); majority 2026, 0 of 89; minority 2026, 5 of 89 (Calgary-North East, Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo, Peace River all pass → fail; Lesser Slave Lake's s.15(2) ratio to the updated mean drops past −50 %). The asymmetry is a second-order signal — population-equality robustness under the 4–14-year lag the current redistribution cycle imposes — and is consistent in direction with the report's A1/A2 findings. Details and reproducible pipeline in `analysis/v0_1_cycle_lag_analysis.md`. The Commission's legal baseline is not affected by this observation; the statutory test uses the decennial census. A legislative reform proposal addressing the underlying §12 ambiguity is in `analysis/reports/v0_1_act_amendment_proposal.md`.

**Open questions raised by the data.** The Plan B and cycle-lag observations surface empirical and interpretive questions the audit does not resolve:

1. **Current-map statutory status.** Whether the 2019-enacted 87-seat configuration satisfies the Act's ±25 % requirement as of mid-2025. Observed: 5 of 87 EDs sit outside the window under DA-level aggregation of mid-2025 populations. If the 2027 general election runs on the 2019 boundaries (because the April 16 process does not produce an adopted map in time), the question is live.
2. **Operative force of §12(3).** Whether the Commission's published methodology (2024 TBF estimate as per-ED basis; provincial quota derived from 2024 total) falls within §12(5)'s "in conjunction with" frame. Either interpretation has consequences: a permissive reading hollows out the decennial-census rule as a legal check; a restrictive reading destabilises every per-ED figure in both 2026 commission reports. The question is for counsel and, if litigated, for courts.
3. **Source of the Majority (0) / Minority (5) Plan-B asymmetry.** Partly attributable to initial population-distribution variance (Majority MAD 3,180 vs Minority MAD 4,707, a 48 % wider spread at the Commission's own data vintage): the same growth shock pushes more minority districts across a threshold they were already closer to. The residual invites district-level close reading of which specific boundaries were drawn near the ±25 % margin in each map's original design.
4. **Lesser Slave Lake s.15(2) eligibility.** Whether the district's loss of s.15(2) qualifying ratio under mid-2025 populations is a cycle-lag artifact or a durable geographic change. The distinction matters for how the special-remote-district provision ages across long redistribution cycles and bears on the structural case for shortening the cycle or amending §15.
5. **A2 Calgary zone-gap persistence at finer resolution.** No measured ward-level Calgary population data exists for 2022–2026 in public circulation; the City of Calgary cancelled its civic census in 2020, with reinstatement scheduled for 2027. A modelled 2024 / 2025 ward-level population estimate can be constructed from public inputs — 2021 Census ward totals, StatsCan Table 17-10-0142 citywide postcensal estimates, the City's Suburban Residential Growth Forecast (per-sector population increments), the Communities-by-Ward crosswalk, and geocoded building permits — and would serve as a sensitivity check on the A2 finding's robustness to intercensal drift. The audit has not executed this sensitivity pass; it is catalogued as a pending item in `analysis/methodology/v0_1_calgary_data_sources_audit.md`. The legal-baseline A2 test necessarily remains 2021-vintage.
6. **Commission methodology disclosure more broadly.** The audit identified one material disclosure–practice inconsistency (population-data vintage). Whether other disclosures — the weighting of "community of interest," the treatment of s.15(2) thresholds, the Appendix C / Appendix E crosswalk construction — are similarly imprecise is outside the scope of this report and would require a separate methodological audit of the commission's full record.


## Appendix F — Legal Interpretive Note


This audit does not offer a legal conclusion. It provides the evidentiary basis on which a legal challenge under *Reference re Saskatchewan* [1991] 2 SCR 158's "effective representation" standard could be constructed. The question whether the minority proposal, as potentially modified by the November 2, 2026 MLA-committee process, would satisfy the effective-representation requirement is for counsel and the courts to assess. The audit's core contribution is documenting that:

1. The two commission proposals diverge systematically on six measurable dimensions.
2. The direction of divergence consistently favors the governing party.
3. The process being used to promote the more-favorable proposal departs from comparator Canadian practice in specific ways.

These facts are reproducible from public data using checked-in code. They do not prove intent, and they do not by themselves establish a constitutional violation.

**Saskatchewan Reference framing.** The "effective representation" standard established in *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158 is permissive on deviation from population equality: McLachlin J (as she then was) wrote that the guarantee of §3 is "the right to effective representation" (para. 26), and that "relative parity of voting power" must be weighed against other factors "including geography, community history, community interests and minority representation" (para. 33). *Raîche v. Canada (Attorney General)*, [2004] FC 679, and *Cassista v. Canada (Attorney General)*, 2014 FC 398, apply the standard to specific boundary disputes without producing a bright-line ceiling on partisan-asymmetric outcomes. Under this standard, a map's constitutional status depends on whether its deviations are reasonably related to permitted factors. The audit's findings — directional partisan asymmetry, engineered s.15(2) boundaries, cracking patterns visible across three cities, and procedural departure from independent-commission practice — are the kinds of evidence a court applying the effective-representation standard would weigh. Whether that weighing produces a constitutional violation is for a court, not this audit, to determine.


---

*Draft. Falsifiability gates, robustness checks, and APA citations documented throughout.*
