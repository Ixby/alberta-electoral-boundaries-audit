# Repository Tree

*Complete annotated directory map. Updated 2026-05-12.*
*Source of truth: `git ls-files` on commit f3cd32f. Gitignored paths are excluded.*

---

## Root

```
alberta_audit/
|
|-- CLAUDE.md                  Guidance for Claude Code sessions — architecture rules, grounding standard
|-- COMPLETED_LOG.md           Completed work log — every finished task with date and outcome
|-- CONTRIBUTING.md            Contribution guide — PR workflow, coding standards, AI attribution policy
|-- README.md                  Public-facing overview — findings, open questions, quickstart
|-- REPRODUCING.md             Step-by-step instructions to re-run every quantitative claim
|-- TODO.md                    Outstanding tasks — M1/M2/M3 milestones, blockers, deferred items
|-- TREE.md                    This file — annotated directory map
|
|-- config.yaml                Master configuration — all shapefile paths, column renames, thresholds
|-- pyproject.toml             Python project metadata and tool configuration (ruff, mypy)
|-- requirements.txt           Pinned Python dependencies (gerrychain==0.3.2 is load-bearing)
|
|-- run_audit.py               Shapefile integrity audit — 10 checks; run before any analysis
|-- run_master_qa.py           Full QA sweep — invokes all scripts in dependency order
```

---

## analysis/

The analysis engine. Code, methodology, and all human-readable analytical work.

```
analysis/
|-- __init__.py
|
|-- automation/
|   +-- changedetection_setup.md    Instruction for ChangeDetection.io + GitHub Actions shapefile monitoring
|
|-- meta/
|   |-- FROZEN_MANIFEST.md          Canonical file manifest — hashes of every committed output; update on change
|   |-- PRIVATE_FILES.md            Documents what is in private_workspace/ and why it is excluded from git
|   +-- setup.md                    Environment setup notes
|
|-- methodology/            70 .md files documenting analytical decisions, threshold derivations, provenance
|   |-- README.md               Index of methodology documents
|   |-- retraction_pathway.md   Named retraction conditions per finding — the fastest path to a challenge
|   |-- null_hypothesis_and_exoneration_criteria.md   Pre-committed null hypotheses for every finding
|   |-- threshold_provenance.md 41 numeric thresholds traced to statutory source or literature
|   |-- test_apparatus_defense.md   Per-test criticism and response
|   |-- methodological_defenses.md  Responses to anticipated methodological objections
|   |-- minority_rationales_validation.md   Scientific findings on Proposals A–F (Airdrie, RMH-Banff, etc.)
|   |-- minority_rationales_inventory.md    Exhaustive inventory of commission rationale claims
|   |-- canonical_shapefile_log.md  Per-finding delta log when DPG → official EA shapefiles changed values
|   |-- canonical_shapefile_methodology.md  How the official shapefiles were integrated
|   |-- mcmc_ensemble.md            MCMC design document — constraint choices, seed provenance
|   |-- s15_2_reaudit.md            s.15(2) EBCA two-tier deviation reaudit (all 6 EDs pass corrected threshold)
|   |-- szat_proposal.md            SZAT (Swing-Zone Allocation Test) pre-registration proposal
|   |-- szat_prereg_draft.md        SZAT pre-registration draft submitted to OSF
|   |-- fisher_combination_defense.md   Defense of Fisher's method for combining Ch1 + Ch2
|   |-- fisher_independence_defense.md  Independence argument for the two test channels
|   |-- audit_dependency_graph.json     234-node, 454-edge DAG in JSON (machine-readable)
|   |-- audit_dependency_graph.dot      Graphviz DOT source for the DAG
|   |-- audit_dependency_graph_readme.md   DAG schema and --invalidate query usage
|   |-- scripts_inventory.md        Inventory mapping all 87 analysis scripts to findings
|   |-- restructure_inventory.md    Phase A–D directory restructure plan (PO-approved; awaiting trigger)
|   |-- ...                         (remaining 54 documents: source-check logs, data surveys,
|                                    editorial pass logs, sensitivity analyses, attribution trails)
|
|-- red_team/               26 .md files — red team reports, peer reviews, legal analysis
|   |-- red_team_assertions.md       Full assertion inventory — keep until referee response
|   |-- red_team_code_fixes.md       Deferred HIGH/MEDIUM code-level findings with rationale
|   |-- red_team_conclusions.md      Red team summary and verdict
|   |-- red_team_latent_bias.md      Latent-bias analysis of the analytical framework
|   |-- science_red_team_*.md        Science red team reports (design, reproducibility, peer review)
|   |-- legal_red_team_*.md          Legal red team reports (framework, report review, data artifacts)
|   |-- peer_review_*.md             Peer review documents (Canadian context, legal, methods)
|   |-- external_code_audit_findings_gemini_2026-04-26.md   Gemini external code audit (9 findings)
|   +-- ...
|
|-- reports/                70+ .md and data files — per-finding analysis results and logs
|   |-- act_amendment_proposal.md       Proposed EBCA §12 amendment text
|   |-- ai_use_recommendations_for_committee.md   7 AI-use principles for the Lunty committee
|   |-- retraction_pathway.md  →  see analysis/methodology/retraction_pathway.md (canonical)
|   |-- pre_registration_*.md        Pre-registration drafts and amendments (2026-04-23 through 04-27)
|   |-- joint_outlier_score.json     Mahalanobis D² joint outlier result (Ch1)
|   |-- intermap_permutation_test_results.json   Ch1-COMP inter-map permutation test (OSF yvc7g)
|   |-- szat_results.csv / szat_summary.json     SZAT bootstrap results (Ch2, OSF 6pt83)
|   |-- neighbour_drain_analysis.md  Ch3 neighbour-drain test (pre-registered pass)
|   |-- municipal_anchoring_analysis.md   §5.8.5 anchoring (retracted on canonical geometry)
|   |-- da_anchoring_analysis.md     DA-level anchoring secondary check
|   |-- sensitivity_report.md        Multi-parameter sensitivity analysis
|   |-- cross_election_robustness.md Cross-election EG robustness (2015, 2019, 2023)
|   |-- claim_significance_analysis.md   MED-A: plurality-of-Albertans claim significance test
|   |-- methods_paper_draft.md       Draft standalone methods paper
|   |-- v0_1_mcmc_*.log              MCMC run logs (1M, 250k, 2019-seeded, etc.)
|   +-- ...
|
+-- scripts/                87 Python scripts — the executable analysis pipeline
    |-- packing_cracking_analysis.py        B1–B6 partisan bias; symmetric, all three maps
    |-- electoral_forensics_population.py   A1/A2/A3 population equality tests
    |-- mcmc_ensemble_canonical.py          Canonical 1M ReCom neutral ensemble (4 chains × 252,500)
    |-- mcmc_ensemble.py                    MCMC core library (chain runner, constraint functions)
    |-- szat.py                             Swing-Zone Allocation Test (Ch2)
    |-- joint_outlier_score_canonical.py    Mahalanobis D² joint outlier (Ch1)
    |-- score_anchoring.py                  Municipal-boundary anchoring fractions
    |-- simulation_convergence_diagnostics.py  ESS, rho_lag1, Gelman-Rubin per chain
    |-- build_pdf.py                        Pandoc-based public report PDF build
    |-- build_academic_pdf.py               Pandoc-based academic report PDF build
    |-- dependency_query.py                 DAG --invalidate query CLI
    |-- canonical_paths.py                  Map-path resolver; never hardcode shapefile paths
    |-- check_voice_and_readability.py      Flesch-Kincaid readability check (run before commit)
    |-- claim_significance_analysis.py      MED-A plurality claim significance test
    |-- sentiment_intensity_score.py        LLM intensity scoring for public submissions
    |-- quote_verify_and_clean.py           Submission quote verification pipeline
    |-- monte_carlo_ci.py                   Monte Carlo confidence intervals for Stage 5 data
    |-- 338canada_reallocate.py             338Canada polling sensitivity (Track E)
    |-- generate_infographic_v3.py          Infographic generator (v3)
    |-- sentiment_monitoring.py             Sentiment pipeline monitoring utility
    |-- utils/
    |   |-- data_loader.py                  config.yaml reader — all path resolution goes here
    |   +-- ...
    |-- automation/
    |   |-- eg_baseline_snapshot.py         EG baseline snapshot for historical calibration
    |   +-- poll_elections_alberta.py       Elections Alberta polling monitor
    +-- ...                                 (remaining ~65 scripts covering compactness,
                                             topological alignment, SZAT, cross-election,
                                             submission search, VA assignment, and build tools)
```

---

## data/

All data. Code never lives here. Output CSVs/JSONs are script-generated; never edit by hand.

```
data/
|-- INTEGRITY_STATUS.md         Integrity check results (run_audit.py output)
|-- data_acquisition_manifest.md  Sources, download dates, and checksums for all input data
|-- provenance_manifest.json    Machine-readable provenance record for all data files
|-- input_hashes.json           SHA-256 hashes of all input data files (verified pre-run)
|
|-- shapefiles/
|   |-- canonical/                   Official Elections Alberta shapefiles (received 2026-05-06)
|   |   |-- ea_majority_2026_eds.gpkg    Majority recommendation — 89 EDs (ground truth)
|   |   +-- ea_minority_2026_eds.gpkg    Minority recommendation — 89 EDs (ground truth)
|   |-- derived/                     Computed from canonical shapefiles
|   |   |-- README.md                    DPG sunset clause documentation
|   |   |-- va_polygons_with_2023_votes.gpkg      VA polygons with crosswalk vote attribution
|   |   +-- va_polygons_with_full_2023_votes.gpkg  VA polygons with full 2023 vote set
|   +-- reference/                   Immutable reference boundaries
|       |-- alberta_2019_eds/         2019 enacted boundaries (EDS_ENACTED_BILL33_15DEC2017.shp)
|       |-- alberta_2021_csds.gpkg    2021 Census Subdivision boundaries
|       |-- alberta_2021_das.gpkg     2021 Dissemination Area boundaries
|       +-- alberta_2023_vas/         2023 Voting Area boundaries (EA_Voting_Area_Boundaries_2023.shp)
|
|-- simulation_checkpoints_canonical/   1M canonical MCMC ensemble (Git LFS, ~1 GB)
|   |-- chain0_samples.csv   252,500 rows — chain 0 (seed: drand round, salt "mcmc_ensemble_250k")
|   |-- chain1_samples.csv   252,500 rows — chain 1
|   |-- chain2_samples.csv   252,500 rows — chain 2
|   +-- chain3_samples.csv   252,500 rows — chain 3
|   (columns: efficiency_gap, mean_median, declination, seats_at_50_50, chain, compactness proxies)
|
|-- outputs/                91 CSVs and 37 JSONs — all script-generated metrics
|   |-- simulation_real_map_scores_canonical.json     Per-map metric values (3 maps × 4 metrics)
|   |-- simulated_ensemble_percentiles_canonical.csv  Per-map percentile placements against 1M ensemble
|   |-- simulation_convergence_diagnostics_canonical.json  ESS, rho_lag1, Gelman-Rubin (4 chains)
|   |-- sentiment_intensity_scores.csv                452 scored public submissions (LLM intensity)
|   +-- ...                                           (remaining ~120 files: compactness, anchoring,
|                                                      population, SZAT, drain, crosswalk metrics)
|
|-- maps/
|   |-- mcmc/                        Ensemble distribution plots (4 PNG figures, report-ready)
|   |   |-- ensemble_distribution_efficiency_gap.png
|   |   |-- ensemble_distribution_mean_median.png
|   |   |-- ensemble_distribution_declination.png
|   |   +-- ensemble_distribution_seats_at_50_50.png
|   |-- hires/                       High-resolution map exports (v0_1 series)
|   |-- hires_v2/                    High-resolution map exports (v0_2 series, 600/1200 dpi)
|   +-- *.jpg                        Overview and regional maps (minority/majority Alberta, Calgary, Edmonton)
|   (data/maps/verification/ — gitignored; QA workflow snapshots, not canonical)
|   (data/maps/pdf_previews/ — gitignored; regenerated on PDF build)
|
|-- raw/                     Raw census data (large files gitignored; metadata tracked)
|-- osm/                     OpenStreetMap data (JSON gitignored; GPKG tracked)
|-- reference/               Static reference tables (338Canada CSVs, StatsCan journey-to-work, etc.)
|
|-- submission_sentiment_llm_results.csv  LLM sentiment classification (452 deduped submissions)
|-- submission_search_dataset.csv         All 614 public submissions with metadata
|-- va_pop_from_das.csv                   VA-level 2021 population from DA crosswalk
|-- szat_bootstrap_eg_samples.npy         SZAT bootstrap samples (Ch2; numpy binary)
|-- simulation_real_map_scores_canonical.json → also in data/outputs/
|-- topology_alignment_proof.md           Formal proof that VA graph topology is planar + connected
+-- ...
```

---

## outputs/

Published report artefacts. PDFs are the deliverable; Markdown is the source.

```
outputs/
|-- academic_report/
|   |-- report_academic.md    Full technical monograph (continuously updated; do not hand-edit numbers)
|   +-- report_academic.pdf   Compiled PDF (rebuilt via build_academic_pdf.py)
|-- public_report/
|   |-- report_public.md      Grade-9 reading level summary for a general audience
|   +-- report_public.pdf     Compiled PDF (rebuilt via build_pdf.py)
+-- assets/                   (gitignored — infographic PNGs distributed in supplemental zip)
```

---

## tests/

32 pytest files. Run with `python -m pytest tests/`. All tests must pass before any report commit.

```
tests/
|-- conftest.py               Shared fixtures and test configuration
|-- pipeline_schemas.py       Data schema validators for pipeline outputs
|-- test_packing_cracking.py  B1–B6 partisan bias tests
|-- test_neighbour_drain.py   Ch3 drain test regression
|-- test_szat.py              Ch2 SZAT bootstrap tests
|-- test_population_consistency.py  A1/A2/A3 population equality
|-- test_canonical_manifest.py      FROZEN_MANIFEST integrity verification
|-- test_drand_and_canonical.py     Seed provenance verification (drand beacon)
|-- test_tripwires.py         Anti-regression tripwires for headline numbers
|-- test_synthetic_gerrymander.py   Synthetic gerrymander detection validation
+-- ...                       (remaining 22 files covering compactness, municipal splits,
                               cross-election, ecological inference, marginal seats, etc.)
```

---

## interactive_proofs/

Vite + React + TypeScript web application for interactive map and methodology visualization.
Source is tracked; `node_modules/` and `dist/` are gitignored (distribute built app in supplemental zip).

```
interactive_proofs/
|-- index.html
|-- src/                 React components and visualization logic
|-- public/              Static assets
|-- package.json
|-- vite.config.ts
|-- tailwind.config.js
|-- tsconfig*.json
+-- README.md
```

---

## docs/

```
docs/
+-- data_sources.md      Primary data sources with URLs, access dates, and licence information
```

---

## .github/

```
.github/
+-- workflows/
    |-- tests.yml                          CI: run pytest on every push + PR
    +-- recompute-on-shapefile-release.yml  CI: trigger recompute pipeline on EA shapefile update
```

---

## Key forward and back dependencies

Files that feed or are fed by multiple other files. Read this when deciding what to update after a change.

### Data pipeline (forward flow — upstream → downstream)

```
config.yaml
  → analysis/scripts/utils/data_loader.py          [reads config; all scripts import this]
  → analysis/scripts/canonical_paths.py             [map-path resolution layer]

data/shapefiles/canonical/*.gpkg                   [official EA shapefiles; received 2026-05-06]
  → analysis/scripts/packing_cracking_analysis.py  [computes B1–B6 partisan bias]
  → analysis/scripts/electoral_forensics_population.py  [computes A1/A2/A3 MAD, NW Calgary]
  → analysis/scripts/score_anchoring.py            [computes §5.8.5 anchoring fractions]
  → analysis/scripts/szat.py                        [computes Ch2 SZAT bootstrap]
  → analysis/scripts/mcmc_ensemble_canonical.py    [builds neutral ensemble]

data/shapefiles/derived/va_polygons_with_2023_votes.gpkg   [2023 votes on VA polygons]
  → analysis/scripts/packing_cracking_analysis.py  [vote attribution for B1–B6]
  → analysis/scripts/szat.py                        [swing-zone assignment]

analysis/scripts/mcmc_ensemble_canonical.py
  → data/simulation_checkpoints_canonical/chain{0..3}_samples.csv  [1M MCMC plans]
  → data/outputs/simulated_ensemble_percentiles_canonical.csv       [percentile placements]
  → data/outputs/simulation_convergence_diagnostics_canonical.json  [ESS, Gelman-Rubin]

analysis/scripts/joint_outlier_score_canonical.py
  → data/outputs/simulation_real_map_scores_canonical.json  [metric values for 3 maps]
  → analysis/reports/joint_outlier_score.json               [D², Fisher combination]

data/outputs/simulated_ensemble_percentiles_canonical.csv   [percentile placements]
  → outputs/academic_report/report_academic.md              [§5.4.9 table]
  → outputs/public_report/report_public.md                  [summary findings]
  → README.md                                               [findings section]
```

### Report pipeline (what each report file depends on)

```
outputs/academic_report/report_academic.md
  ← data/outputs/simulated_ensemble_percentiles_canonical.csv  [§5.4.9 percentiles]
  ← data/outputs/simulation_real_map_scores_canonical.json     [metric values]
  ← analysis/reports/joint_outlier_score.json                  [Ch1 D², Fisher p]
  ← analysis/reports/intermap_permutation_test_results.json    [Ch1-COMP p-values]
  ← data/submission_sentiment_llm_results.csv                  [§5.9.4 sentiment]
  ← analysis/methodology/retraction_pathway.md                 [retraction conditions]

README.md
  ← data/simulation_real_map_scores_canonical.json             [MAD, EG values]
  ← analysis/reports/joint_outlier_score.json                  [Ch1, SZAT, Fisher]
  ← analysis/reports/intermap_permutation_test_results.json    [Ch1-COMP]
  ← analysis/methodology/audit_dependency_graph.json           [234 nodes, 454 edges]
```

### Integrity chain (files that must be updated together)

| When you change... | Also update... |
|---|---|
| Any script output CSV/JSON | `analysis/meta/FROZEN_MANIFEST.md` (hash) |
| Any report finding | `analysis/methodology/retraction_pathway.md` (retraction condition) |
| Any percentile / p-value | `outputs/academic_report/report_academic.md` → `README.md` |
| `config.yaml` | Run `run_audit.py` to verify nothing breaks |
| Any pre-registration amendment | `analysis/reports/pre_registration_amendment_*.md` |
| `data/simulation_checkpoints_canonical/` | `data/outputs/simulation_convergence_diagnostics_canonical.json` |

---

## Gitignored paths (not in repo, documented here for reference)

| Path | Contents | Disposition |
|---|---|---|
| `private_workspace/` | Credentials, personal notes, OSF scripts, draft emails, live task logs | Never commit |
| `analysis/ops/` | Operational scripts (watchdog, poller, pipeline runners) | Never commit |
| `analysis/tools/` | One-off build helpers and refactor scripts | Never commit |
| `interactive_proofs/node_modules/` | npm dependencies | Regenerate: `npm install` |
| `interactive_proofs/dist/` | Built app output | Distribute in supplemental zip |
| `data/maps/verification/` | QA workflow map snapshots (versioned PNGs) | Distribute in supplemental zip |
| `data/reference/polling_338_historical/` | Raw scraped 338Canada HTML | Regenerated by scraper |
| `outputs/assets/` | Draft infographic PNGs | Distribute in supplemental zip |
| `data/outputs/checkpoints/` | Intermediate computation checkpoints | Local only |
| `data/simulation_checkpoints_canonical/` *(except chain*.csv)* | MCMC chunk files | chain*.csv tracked via LFS |
| `private_workspace/osf_token.txt` | OSF credentials | Never commit |
| `*.bak` | Backup files | Local only |
