# Repository Tree

*Annotated directory map. Updated 2026-05-12 to reflect post-reorganisation layout.*
*Verified against `git ls-files` output. Gitignored paths documented at bottom.*

---

## Root

```
alberta_audit/
├── CONTRIBUTING.md            PR workflow, coding standards, AI attribution policy
├── README.md                  Public-facing overview — findings, quickstart, citation
├── TODO.md                    Outstanding tasks — M1/M2/M3 milestones, blockers, deferred items
├── TREE.md                    This file
│
├── config.yaml                Master configuration — all shapefile paths, column renames, thresholds
├── pyproject.toml             Python project metadata and tool configuration (ruff, mypy)
├── requirements.txt           Pinned Python dependencies — gerrychain==0.3.2 is load-bearing
│
├── run_audit.py               Shapefile integrity audit — 10 checks; run before any analysis
└── run_master_qa.py           Full QA sweep — invokes all scripts in dependency order
```

---

## docs/

Project-level documentation that does not need to live at root.

```
docs/
├── COMPLETED_LOG.md           Finished-task log — every completed item with date and outcome
├── FROZEN_MANIFEST.md         Canonical file manifest — hashes of every committed output
├── REPRODUCING.md             Step-by-step instructions to re-run every quantitative claim
├── data_sources.md            Primary data sources with URLs, access dates, and licence information
└── setup.md                   Environment setup notes (Python 3.11+, dependency pinning)
```

---

## analysis/

The analysis engine. Code, methodology docs, and all human-readable analytical outputs.

```
analysis/
├── __init__.py
│
├── methodology/            ~70 .md files — analytical decisions, threshold derivations, provenance
│   ├── README.md               Index of methodology documents
│   ├── retraction_pathway.md   Named retraction conditions per finding
│   ├── null_hypothesis_and_exoneration_criteria.md   Pre-committed null hypotheses
│   ├── threshold_provenance.md 41 numeric thresholds traced to statute or literature
│   ├── test_apparatus_defense.md     Per-test criticism and response
│   ├── methodological_defenses.md    Responses to anticipated objections
│   ├── plain_language_defense.md     215-entry Q&A; §0 = six-objection quick reference
│   ├── minority_rationales_validation.md    Scientific findings on Proposals A–F
│   ├── minority_rationales_inventory.md     Exhaustive commission rationale inventory
│   ├── canonical_shapefile_log.md    Per-finding delta log when DPG → official shapefiles changed values
│   ├── canonical_shapefile_methodology.md   How official shapefiles were integrated
│   ├── mcmc_ensemble.md              MCMC design — constraint choices, seed provenance
│   ├── s15_2_reaudit.md              s.15(2) EBCA two-tier deviation reaudit
│   ├── szat_methodology.md           SZAT design, method, and AsPredicted pre-registration text
│   ├── fisher_combination_defense.md Defense of Fisher's method for Ch1 + Ch2
│   ├── fisher_independence_defense.md Independence argument for the two test channels
│   ├── changedetection_setup.md      ChangeDetection.io + GitHub Actions shapefile monitoring
│   ├── audit_dependency_graph.json   234-node, 454-edge DAG (machine-readable)
│   ├── audit_dependency_graph.dot    Graphviz DOT source for the DAG
│   ├── audit_dependency_graph_readme.md   DAG schema and --invalidate query usage
│   ├── scripts_inventory.md          Maps all analysis scripts to findings
│   └── ...                           (~54 more: source-check logs, sensitivity analyses,
│                                      editorial passes, attribution trails)
│
├── red_team/           ~26 .md files — red team reports, peer reviews, legal analysis
│   ├── red_team_consolidated.md      Red team summary and verdict
│   ├── red_team_assertions.md        Full assertion inventory
│   ├── red_team_code_fixes.md        Deferred HIGH/MEDIUM code-level findings
│   ├── red_team_latent_bias.md       Latent-bias analysis of the analytical framework
│   ├── science_red_team_*.md         Science red team reports
│   ├── legal_red_team_*.md           Legal red team reports
│   ├── peer_review_*.md              Peer review documents
│   └── external_code_audit_findings_gemini_2026-04-26.md
│
├── reports/            ~70+ data and .md files — per-finding results and logs
│   ├── pre_registration_amendment_log.md     Consolidated pre-registration amendment record
│   │                                          (4 dated amendments, 2026-04-23 through 2026-04-27)
│   ├── act_amendment_proposal.md             Proposed EBCA §12 amendment text
│   ├── ai_use_recommendations_for_committee.md   7 AI-use principles for the Lunty committee
│   ├── joint_outlier_score.json              Mahalanobis D² joint outlier result (Ch1) — canonical
│   ├── szat_summary.json                     SZAT bootstrap summary — canonical
│   ├── szat_summary_full_votes.json          SZAT full-vote sensitivity run
│   ├── szat_2019_baseline.json               SZAT 2019 baseline
│   ├── intermap_permutation_test_results.json   Ch1-COMP inter-map permutation test
│   ├── neighbour_drain_analysis.md           Ch3 neighbour-drain test (pre-registered pass)
│   ├── municipal_anchoring_analysis.md       §5.8.5 anchoring (retracted on canonical geometry)
│   ├── da_anchoring_analysis.md              DA-level anchoring secondary check
│   ├── sensitivity_report.md                 Multi-parameter sensitivity analysis
│   ├── cross_election_robustness.md          Cross-election EG robustness
│   ├── methods_paper_draft.md                Draft standalone methods paper
│   └── ...
│
└── scripts/            ~95 Python scripts — the executable analysis pipeline
    ├── packing_cracking_analysis.py        B1–B6 partisan bias; symmetric, all three maps
    ├── electoral_forensics_population.py   A1/A2/A3 population equality tests
    ├── mcmc_ensemble_canonical.py          Canonical 1,010,000-plan ReCom neutral ensemble
    ├── mcmc_ensemble.py                    MCMC core library (chain runner, constraint functions)
    ├── mcmc_anchoring_ensemble.py          CSD edge-crossing anchoring ensemble (OSF s58a6; 10k plans)
    ├── szat.py                             Swing-Zone Allocation Test (Ch2)
    ├── joint_outlier_score_canonical.py    Mahalanobis D² joint outlier (Ch1)
    ├── score_anchoring.py                  Municipal-boundary anchoring fractions (§5.8.5)
    ├── simulation_convergence_diagnostics.py   ESS, rho_lag1, Gelman-Rubin per chain
    ├── validate_fisher_independence.py     Ch1 × Ch2 independence test (ρ test)
    ├── build_pdf.py / build_academic_pdf.py    Pandoc-based PDF generation
    ├── canonical_paths.py                  Map-path resolver — never hardcode shapefile paths
    ├── dependency_query.py                 DAG --invalidate query CLI
    ├── quote_verify_and_clean.py           Submission quote verification + deduplication
    ├── validation_sample.py                Stratified IRR validation sample (60 rows)
    ├── compute_kappa.py                    Cohen's kappa for LLM vs human sentiment labels
    ├── utils/
    │   ├── data_loader.py                  config.yaml reader — all path resolution goes here
    │   └── ...
    └── ...                                 (~70 more: compactness, topological alignment, SZAT,
                                             cross-election, submission search, VA assignment, builds)
```

---

## data/

All data. Code never lives here. Script-generated outputs are committed for reproducibility; never edit by hand.

```
data/
│
├── [large flat files — script-read/write paths; do not move]
│   ├── simulated_ensemble_raw_samples_canonical.csv        1,010,000-row canonical ensemble
│   ├── simulated_ensemble_raw_samples_section_c.csv        Section C ensemble (seed 3562959107)
│   ├── simulated_ensemble_raw_samples_threshold_2015.csv   2015-vote-substrate sensitivity
│   ├── simulated_ensemble_raw_samples_threshold_2019.csv   2019-vote-substrate sensitivity
│   ├── simulated_ensemble_percentiles_canonical.csv        Per-map percentile placements (canonical)
│   ├── simulated_ensemble_percentiles_section_c.csv
│   ├── simulated_ensemble_percentiles_threshold_2015.csv
│   ├── simulated_ensemble_percentiles_threshold_2019.csv
│   ├── simulation_real_map_scores_canonical.json           Per-map metric values (3 maps × 4 metrics)
│   ├── simulation_real_map_scores_{section_c,threshold_2015,threshold_2019}.json
│   ├── simulation_convergence_diagnostics_canonical.json   ESS, rho_lag1, Gelman-Rubin (4 chains)
│   ├── simulation_convergence_diagnostics_per_chain.json
│   ├── simulation_convergence_diagnostics_{section_c,threshold_2015,threshold_2019}.json
│   ├── drain_label_shuffle_null.json                       Ch3 label-shuffle null result
│   ├── neighbour_drain_summary.json                        Neighbour-drain aggregate stats
│   ├── submission_search_dataset.csv                       614 public submissions with metadata
│   ├── submission_sentiment_llm_results.csv                LLM sentiment (452 deduped submissions)
│   ├── szat_bootstrap_eg_samples.npy                       SZAT bootstrap samples (numpy binary)
│   └── va_pop_from_das.csv                                 VA-level 2021 population from DA crosswalk
│
├── logs/                       Run logs from long-running canonical-era scripts (4 files)
│   ├── isr_run1.log
│   ├── mcmc_100k_post_audit_rerun.log
│   ├── python_compactness_run.log
│   └── redist_crossvalidation_run.log
│
├── meta/                       Provenance, integrity, and documentation (not read by scripts)
│   ├── data_acquisition_manifest.md    Sources, download dates, checksums for all input data
│   ├── INTEGRITY_STATUS.md             Integrity check results (run_audit.py output)
│   ├── provenance_manifest.json        Machine-readable provenance record
│   ├── input_hashes.json               SHA-256 hashes of all input data files
│   └── topology_alignment_proof.md     Formal proof that VA graph topology is planar + connected
│
├── scratch/                    Issue-specific investigation artefacts (not canonical)
│   ├── issue14_feasibility_qgis.gpkg
│   └── issue14_optimization_results.csv
│
├── shapefiles/
│   ├── canonical/                   Official Elections Alberta shapefiles (received 2026-05-06)
│   │   ├── ea_majority_2026_eds.gpkg    Majority — 89 EDs (ground truth)
│   │   └── ea_minority_2026_eds.gpkg    Minority — 89 EDs (ground truth)
│   ├── derived/                     Computed from canonical shapefiles
│   │   ├── README.md                    DPG sunset clause documentation
│   │   ├── va_polygons_with_2023_votes.gpkg      VA polygons — crosswalk vote attribution
│   │   └── va_polygons_with_full_2023_votes.gpkg VA polygons — full 2023 vote set (authoritative)
│   └── reference/                   Immutable reference boundaries
│       ├── alberta_2019_eds/            2019 enacted (EDS_ENACTED_BILL33_15DEC2017.shp)
│       ├── alberta_2021_csds.gpkg       2021 Census Subdivision boundaries
│       ├── alberta_2021_das.gpkg        2021 Dissemination Area boundaries
│       └── alberta_2023_vas/            2023 Voting Area boundaries
│
├── simulation_checkpoints_canonical/   1,010,000-plan canonical MCMC ensemble (Git LFS, ~1 GB)
│   ├── chain0_samples.csv  252,500 rows
│   ├── chain1_samples.csv
│   ├── chain2_samples.csv
│   └── chain3_samples.csv
│
├── simulation_checkpoints_section_c/   Section C re-run (seed 3562959107)
├── simulation_checkpoints_threshold_2015/
├── simulation_checkpoints_threshold_2019/
│
├── outputs/                ~150 CSVs + JSONs — all script-generated metrics
│   ├── csd_anchoring_ensemble.csv                    10,000-plan CSD edge-crossing ensemble (s58a6)
│   ├── csd_anchoring_results.json                    Anchoring percentile results — both maps p100
│   ├── szat_robustness_section_a.json                SZAT 10-seed robustness range (s58a6-A)
│   ├── sentiment_intensity_scores.csv                452 LLM-scored intensity rows (deduped)
│   ├── quotes_verified.csv                           827 verified quotes (submissions + Hansard)
│   ├── irr_validation_sample.csv                     60-row IRR sample (human annotation pending)
│   ├── assignment_va_to_2026_canonical.csv           4,765 VA → 2026 ED canonical spatial join
│   ├── cross_reference_results.csv                   25-rationale submission cross-reference
│   └── ...                                           (~140 more: compactness, anchoring, population,
│                                                      SZAT, drain, crosswalk, cross-election metrics)
│
├── maps/
│   ├── mcmc/                     Ensemble distribution plots (4 PNG figures, report-ready)
│   ├── hires/ hires_v2/          High-resolution map exports
│   └── *.jpg                     Overview and regional maps
│
├── osm/                          OpenStreetMap data (JSON gitignored; GPKG tracked)
├── raw/                          Raw census data (large files gitignored; metadata tracked)
├── processed/                    Intermediate processed data
└── reference/                    Static reference tables (338Canada CSVs, journey-to-work, etc.)
```

---

## dpg/

DPG-era artifacts archived here. DPG = Derived Provisional Geometries — boundary tracings
made from PDF thumbnails before Elections Alberta released official shapefiles (2026-05-06).
These files are a historical record; no active analysis uses them.

```
dpg/
├── analysis/
│   └── dpg_perturbation_consolidated.md   v1 / v2 / v3 perturbation CI analysis (consolidated)
│                                           Upper-bound (v1, ±500m) + tier-aware (v2/v3) layers
├── logs/                      29 DPG-era run logs — perfecter runs 1–9, MCMC runs, burst tests
├── outputs/
│   ├── dpg_perturbation_samples_v3_tight.csv
│   └── dpg_perturbation_summary_v3_tight.json
└── verification/              106 DPG-era QA map snapshots (PNG)
```

---

## outputs/

Published report artefacts. PDFs are the deliverable; Markdown is the source of truth.

```
outputs/
├── academic_report/
│   ├── report_academic.md      Full technical monograph — do not hand-edit numbers
│   ├── data_supplement.md      Peer-review navigation aid
│   └── report_academic.pdf     Compiled PDF (rebuilt via build_academic_pdf.py)
├── public_report/
│   ├── report_public.md        Grade-9 reading level summary for general audience
│   └── report_public.pdf       Compiled PDF (rebuilt via build_pdf.py)
└── assets/                     Infographic PNGs (gitignored — in supplemental zip)
```

---

## tests/

32 pytest files. Run with `python -m pytest tests/`. All must pass before any report commit.

```
tests/
├── conftest.py               Shared fixtures and test configuration
├── pipeline_schemas.py       Data schema validators
├── test_packing_cracking.py  B1–B6 partisan bias
├── test_neighbour_drain.py   Ch3 drain test regression
├── test_szat.py              Ch2 SZAT bootstrap
├── test_population_consistency.py  A1/A2/A3 population equality
├── test_canonical_manifest.py      FROZEN_MANIFEST integrity
├── test_drand_and_canonical.py     Seed provenance (drand beacon)
├── test_tripwires.py         Anti-regression tripwires for headline numbers
├── test_synthetic_gerrymander.py   Synthetic detection validation
└── ...                       (22 more: compactness, municipal splits, cross-election,
                               ecological inference, marginal seats, MAUP sensitivity)
```

---

## interactive_proofs/

Vite + React + TypeScript web app for interactive map and methodology visualization.
`node_modules/` and `dist/` are gitignored; distribute built app in supplemental zip.

---

## Data pipeline (key forward dependencies)

```
config.yaml
  → analysis/scripts/utils/data_loader.py          [reads config; all scripts import this]
  → analysis/scripts/canonical_paths.py             [map-path resolution layer]

data/shapefiles/canonical/*.gpkg                   [official EA shapefiles; received 2026-05-06]
  → analysis/scripts/mcmc_ensemble_canonical.py    [builds neutral ensemble → data/ flat files]
  → analysis/scripts/packing_cracking_analysis.py  [computes B1–B6 partisan bias]
  → analysis/scripts/szat.py                        [Ch2 SZAT bootstrap]
  → analysis/scripts/mcmc_anchoring_ensemble.py    [CSD anchoring ensemble]

analysis/scripts/mcmc_ensemble_canonical.py
  → data/simulation_checkpoints_canonical/chain{0..3}_samples.csv
  → data/simulated_ensemble_percentiles_canonical.csv       [percentile placements]
  → data/simulation_convergence_diagnostics_canonical.json  [ESS, Gelman-Rubin]
  → data/simulation_real_map_scores_canonical.json          [metric values]

analysis/scripts/joint_outlier_score_canonical.py
  → analysis/reports/joint_outlier_score.json       [D², Fisher combination — authoritative Ch1 result]

data/simulated_ensemble_percentiles_canonical.csv
  → outputs/academic_report/report_academic.md      [§5.4.9 table]
  → outputs/public_report/report_public.md          [summary findings]
  → README.md                                        [findings section]
```

### Report dependencies

```
outputs/academic_report/report_academic.md
  ← data/simulated_ensemble_percentiles_canonical.csv
  ← data/simulation_real_map_scores_canonical.json
  ← analysis/reports/joint_outlier_score.json        [Ch1 D², Fisher p]
  ← analysis/reports/szat_summary.json               [Ch2 SZAT p, score]
  ← data/submission_sentiment_llm_results.csv         [§5.9.4 sentiment]
  ← analysis/methodology/retraction_pathway.md        [retraction conditions]
```

### Integrity chain

| When you change… | Also update… |
|---|---|
| Any script output CSV/JSON | `docs/FROZEN_MANIFEST.md` (hash) |
| Any report finding | `analysis/methodology/retraction_pathway.md` |
| Any percentile / p-value | `report_academic.md` → `README.md` |
| `config.yaml` | Run `run_audit.py` to verify nothing breaks |
| Pre-registration methodology | `analysis/reports/pre_registration_amendment_log.md` |
| MCMC checkpoints | `data/simulation_convergence_diagnostics_canonical.json` |

---

## Gitignored paths

| Path | Contents | Disposition |
|---|---|---|
| `private_workspace/` | Credentials, emails, notes, live task logs | Never commit |
| `analysis/ops/` | Operational scripts (watchdog, poller) | Never commit |
| `analysis/tools/` | One-off build helpers | Never commit |
| `interactive_proofs/node_modules/` | npm deps | Regenerate: `npm install` |
| `interactive_proofs/dist/` | Built app | Supplemental zip |
| `data/simulation_checkpoints_*/` (non-chain*.csv) | MCMC chunk files | chain*.csv tracked via LFS |
| `outputs/assets/` | Draft infographic PNGs | Supplemental zip |
| `data/outputs/checkpoints/` | Intermediate checkpoints | Local only |
| `CLAUDE.md` | AI session bootstrap | Never commit |
| `*.bak` | Backup files | Local only |
