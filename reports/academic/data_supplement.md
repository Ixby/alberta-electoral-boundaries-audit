# Data Supplement — Alberta Electoral Boundaries Audit (Phase 1)

**Document type:** Peer-review navigation aid  
**Companion report:** `outputs/academic_report/report_academic.md`  
**Repository HEAD at time of submission:** `7b7b2fe`  
**Date:** 2026-05-12

---

This supplement is not a second manuscript. It is a structured index for external verifiers: where to find primary outputs, how to reproduce the key computations, the exact headline numbers for cross-checking, and the pre-registration record with timing disclosures. All findings, interpretation, and methodology are in the academic report.

---

## §D1 — Repository Layout

```
alberta_audit/
├── analysis/
│   ├── scripts/          # 95 single-responsibility analysis scripts
│   ├── reports/          # intermediate JSON outputs (joint_outlier_score, szat_summary, etc.)
│   └── methodology/      # test protocols, pre-analysis plans
├── data/
│   ├── shapefiles/
│   │   ├── canonical/    # authoritative Elections Alberta shapefiles (ground truth)
│   │   ├── derived/      # VA polygons with 2023 vote attribution
│   │   └── reference/    # 2019 enacted baseline
│   └── outputs/          # 99 CSV + 45 JSON script outputs (committed for reproducibility)
├── outputs/
│   ├── academic_report/  # report_academic.md, figures, this supplement
│   └── public_report/    # report_public.md
├── tests/                # pytest suite
├── config.yaml           # all path configuration (never hardcode shapefile paths)
├── requirements.txt      # pinned Python dependencies
└── CLAUDE.md             # session-bootstrap and contributor conventions
```

Three files are script outputs committed to git and **must not be hand-edited**:
- `data/outputs/simulation_real_map_scores_canonical.json`
- `data/outputs/simulated_ensemble_percentiles_canonical.csv`
- `data/outputs/simulation_convergence_diagnostics_canonical.json`

If any of these are absent, re-run the generating script (`mcmc_ensemble_canonical.py`) before reproducing headline results.

**DPG sunset clause.** Files in `data/shapefiles/derived/` generated from Derived Provisional Geometries (traced from commission PDF thumbnails) are deprecated. Files labelled `v0_8` or `v0_9` in `data/outputs/` retain DPG-era provenance and are kept for audit trail transparency only. All active analysis uses canonical Elections Alberta shapefiles.

---

## §D2 — Software Environment

**Python version:** 3.11 (Windows 11 Education 10.0.26100; Python 3.14 also verified)

| Package | Pinned version | Role |
|---|---|---|
| gerrychain | 0.3.2 | MCMC neutral ensemble (canonical 1M-plan run) |
| networkx | 3.6.1 | gerrychain dependency — graph iteration semantics are version-sensitive |
| geopandas | 1.1.3 | shapefile I/O and spatial joins |
| pyogrio | 0.12.1 | fast shapefile driver for geopandas |
| shapely | 2.1.2 | geometry operations |
| pyproj | 3.7.2 | CRS transformations |
| pandas | 2.2.2 | tabular data processing |
| numpy | 1.26.4 | numerical operations |
| textstat | 0.7.13 | Flesch-Kincaid readability gate |
| matplotlib | 3.9.2 | figures |

**Install and verify:**

```bash
python -m pip install -r requirements.txt
python -c "import pandas, numpy, geopandas, shapely, pyproj; print('OK')"
python -m pytest tests/ -v
```

**Random seed protocol.** All random seeds are derived from Cloudflare drand beacon values: `seed = int(SHA-256("salt:randomness_hex"), 16) % (2**32)`. Beacon rounds and salts are documented per-script in OSF registrations and in the methodology directory.

---

## §D3 — Primary Data Sources

| Source | Description | Location |
|---|---|---|
| Elections Alberta canonical shapefiles | Authoritative 2026 boundary geometries for both commission proposals | `data/shapefiles/canonical/ea_minority_2026_eds.gpkg`, `ea_majority_2026_eds.gpkg` |
| 2019 enacted boundaries | Pre-redistribution baseline for all comparisons | `data/shapefiles/reference/` |
| VA polygons with 2023 vote attribution | Voting areas with election-day NDP/UCP tallies attributed to 2026 boundaries | `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg` |
| 2023 Alberta general election results | Official tally (NDP 777,404 + UCP 928,900 province-wide) | source documented in `analysis/methodology/` |
| Statistics Canada Census Subdivision boundaries | CSD polygons used for municipal anchoring edge-crossing test | `data/shapefiles/reference/` |
| Written public submissions (1,252) | Full-corpus sentiment and cross-reference analysis | `data/submissions/` |
| Hansard transcripts | Round 1 (188 turns, May 2025), Round 2 (209 turns, Jan 2026) | `data/hansard/` |

**Vote substrate note.** The SZAT channel (Ch2) uses election-day two-party totals (~896,644 combined) from the VA polygon attribution layer, not province-wide election totals. The 1,706,304 two-party figure in Alberta's 2023 results is not the VA-level denominator. This distinction is documented in §5.2.10 DOCUMENTED CORRECTIONS of the academic report.

---

## §D4 — Key Output Files

| Output file | Generating script | Report section |
|---|---|---|
| `findings/joint_outlier_score.json` | `joint_outlier_score_canonical.py` | §5.2 (Ch1 Mahalanobis) |
| `findings/szat_summary.json` | `szat.py` | §5.3 (Ch2 SZAT) |
| `data/outputs/rhat_diagnostic_section_b.json` | `simulation_convergence_diagnostics.py` | §5.4 (convergence) |
| `data/outputs/szat_robustness_section_a.json` | `szat.py` (10-seed replay) | §5.2.10 (robustness) |
| `data/outputs/csd_anchoring_results.json` | `mcmc_anchoring_ensemble.py` | §5.4.9 (anchoring) |
| `data/outputs/csd_anchoring_ensemble.csv` | `mcmc_anchoring_ensemble.py` | §5.4.9 |
| `data/outputs/sentiment_intensity_scores.csv` | `submission_sentiment_llm_full.py` | §5.9.4.6 |
| `data/outputs/quotes_verified.csv` | `quote_verify_and_clean.py` | §5.9.4.7 |
| `data/outputs/cross_reference_summary.json` | `cross_reference_submitters.py` | §5.9.4.7 |
| `data/outputs/irr_validation_sample.csv` | `validation_sample.py` | §5.9 (IRR gate — pending) |

**Ensemble checkpoints** are in `data/simulation_checkpoints_canonical/` and are excluded from the git repository (`.gitignore`). The canonical ensemble can be reproduced from scratch with `python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 252500`.

---

## §D5 — Headline Results

All values below are drawn from committed output files at HEAD `7b7b2fe`. File paths given for verification.

### Ch1 — Partisan Joint Outlier (Mahalanobis)

Ensemble: 1,010,000 neutral plans, 4 chains × 252,500 steps, ReCom algorithm, base_seed=1432864451. Covariance matrix estimated from the full 1M ensemble. Source: `findings/joint_outlier_score.json`.

| Map | D | D² | Joint p |
|---|---|---|---|
| Minority (March 2026) | 5.716 | 32.67 | 1.40 × 10⁻⁶ |
| Majority (March 2026) | 2.802 | 7.85 | 0.097 (within null) |
| Enacted 2019 (baseline) | — | — | 0.013 |

The four component metrics (efficiency gap, mean-median, declination, seats at 50/50) are available in `findings/joint_outlier_score.json`.

**Pre-registration status:** Ch1 was not pre-registered before execution. See §D7 for the timing disclosure.

### Ch2 — Swing Zone Allocation Test (SZAT)

Source: `findings/szat_summary.json`.

| Parameter | Value |
|---|---|
| SZAT score (minority − majority EG, swing VAs only) | +0.039211 |
| Null 97.5th percentile (bootstrap) | +0.036652 |
| Bootstrap p-value | 0.0024 |
| Bootstrap N | 10,000 |
| Bootstrap seed | 23,687,475 (drand-derived) |
| Vote substrate | Election-day (~896k two-party) |
| Swing zones used | 2,110 of 4,765 VAs |
| Bootstrap 95% CI | [0.0097, 0.0367] |

**Pre-registration:** OSF 6pt83, AsPredicted #289469, submitted 2026-05-07.

### Fisher Combination (Ch1 × Ch2)

Independence test: Pearson ρ = −0.0014, p = 0.888 (|ρ| < 0.30 threshold — PASS). Channels treated as empirically near-independent. Source: `findings/joint_outlier_score.json`.

| Statistic | Value |
|---|---|
| Fisher T | 39.028 |
| Degrees of freedom | 4 |
| Combined p | 6.87 × 10⁻⁸ |

### Ch3 — Neighbour-Drain Label Shuffle

Source: `findings/intermap_permutation_test_results.json`. **Not included in Fisher combination.**

| Map | p | Result |
|---|---|---|
| Minority | 0.134 | Within null |
| Majority | (anomalously clean — z = −2.92) | Reported as anomaly |

**Pre-registration:** OSF r3zm7, AsPredicted #289451, submitted 2026-05-06.

### Supporting Channels (§s58a6-C, all complete)

| Channel | Minority result | Majority result | Status |
|---|---|---|---|
| Population MAD (canonical ensemble) | p ≈ 0.0098 (p99.0 — outlier) | p15.8 (within null) | DONE 2026-05-12 |
| Reock median compactness | p100 (anomalously compact) | p100 (anomalously compact) | Null finding |
| CSD anchoring edge-crossing (MCMC, 10,000 plans) | 29.75% → p100 | 37.63% → p100 | Null finding (see note) |
| Justification tests 1–5 (population/area law) | All 5 FAIL | — | DONE |

**CSD anchoring note.** Both maps exceed all 10,000 neutral plans on CSD boundary-following (ensemble median 17.82%, 95% interval [16.73%, 18.97%]). This indicates both commission maps are more anchored to municipal divisions than random plans — the expected direction for commission work. The pre-registered alternative direction (minority < ensemble median) is not confirmed. This channel does not add to the Fisher combination. Source: `data/outputs/csd_anchoring_results.json`.

### SZAT Robustness (§s58a6-A)

Ten pre-committed seeds derived from drand round 6099592. Source: `data/outputs/szat_robustness_section_a.json`.

| Statistic | Value |
|---|---|
| Primary p (registered seed) | 0.0024 |
| Range across 10 seeds | [0.0025, 0.0043] |
| Median across 10 seeds | 0.0031 |
| All seeds p < 0.05 | Yes |

### Submission Sentiment Cross-Reference (§5.9.4.7)

1,252 written submissions + 397 Hansard turns (full combined corpus). Source: `data/outputs/cross_reference_summary.json`.

| Metric | Value |
|---|---|
| Total rationales reviewed | 25 |
| Rationales matched to named configurations | 6 |
| CONTRA_COMMISSION (public opposed, commission supportive) | 3 (R1, R3, R10) |
| ALIGNS_WITH_AUDIT_FINDING | 2 (R2, R12) |
| CONTRA_AUDIT | 1 (R13) |
| ALIGNS_WITH_COMMISSION | 0 |

**IRR gate status:** Pending. 60-row human annotation sample is in `data/outputs/irr_validation_sample.csv`. Run `python analysis/scripts/compute_kappa.py` after filling the `human_label` column. Threshold: Cohen's κ ≥ 0.60.

---

## §D6 — MCMC Convergence Diagnostics

4-chain ensemble, 252,500 steps per chain. Gelman-Rubin R̂ computed per metric. Pre-registered criterion: GR92 R̂ < 1.1. Source: `data/outputs/rhat_diagnostic_section_b.json`.

| Metric | R̂ (GR92) | R̂ (Vehtari 2021) | GR92 < 1.1 | V21 < 1.01 | Worst-chain ESS |
|---|---|---|---|---|---|
| Efficiency gap | 1.01843 | 1.01847 | **PASS** | marginal | 76 |
| Mean-median | 1.00179 | 1.00181 | **PASS** | **PASS** | 63 |
| Declination | 1.01343 | 1.01440 | **PASS** | marginal | 70 |
| Seats at 50/50 | 1.00540 | 1.00527 | **PASS** | **PASS** | 94 |

All four metrics satisfy the registered GR92 < 1.1 criterion. Efficiency gap and declination marginally exceed the stricter Vehtari (2021) 1.01 recommendation; this is disclosed in §5.4 of the academic report with a note on headroom relative to Ch1 scores.

---

## §D7 — Pre-Registration Record

All registrations were submitted before examining the test data for that channel. Links are archived in `analysis/meta/FROZEN_MANIFEST.md`.

| OSF ID | AsPredicted ID | Submitted | Covers |
|---|---|---|---|
| w2s8k | — | 2026-05-06 | DPG v11 geometry validation (S2-01 / shapefile integrity) |
| r3zm7 | #289451 | 2026-05-06 | Ch3: Neighbour-Drain label shuffle |
| qsgy8 | #289455 | 2026-05-06 | Phase 2: Lunty 91-seat scorecard (pending Nov 2026 map) |
| 6pt83 | #289469 | 2026-05-07 | Ch2: SZAT bootstrap null test |
| s58a6 | — | 2026-05-10 | §s58a6-A SZAT robustness (10 seeds); §s58a6-B R-hat diagnostics; §s58a6-C Section C channels (population MAD, Reock, anchoring) |

### Timing Disclosure — Ch1 (Mahalanobis Joint Outlier)

The canonical Mahalanobis joint outlier test (Ch1) was not filed as a stand-alone OSF pre-registration before execution. The test null hypothesis, the four component metrics, the covariance estimation method, and the rejection threshold were specified in the pre-analysis plan documented in `analysis/methodology/` prior to running the ensemble, but no OSF registration exists for this specific channel.

This is disclosed as a limitation of the audit's pre-registration architecture. The Ch1 result should be read with the same evidential weight as a hypothesis-consistent finding where the hypothesis is documented but the registration is absent. The Fisher combination includes Ch1; reviewers who apply a stricter pre-registration standard may wish to treat the Fisher result as primarily driven by Ch2 (OSF 6pt83, p = 0.0024), which is registered. This is discussed in §5.2.10 DOCUMENTED CORRECTIONS of the academic report.

### drand Beacon Record

All random seeds are derived from Cloudflare drand (league/default, chain `8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce`). Derivation: `SHA-256("salt:beacon_randomness_hex")` truncated to 32-bit unsigned integer.

| Registration | drand round | Salt | Derived seed |
|---|---|---|---|
| s58a6 primary (SZAT robustness + R-hat) | 6,099,592 | `alberta-audit-szat-robustness` | 23,687,475 |
| s58a6 Section C rerun | 6,099,592 | `alberta-audit-section-c-rerun` | 3,562,959,107 |
| s58a6 anchoring ensemble | 6,099,592 | `alberta-audit-anchoring-ensemble` | 80,780,579 |
| Canonical ensemble base seed | — | (pre-registered in w2s8k) | 1,432,864,451 |

---

## §D8 — Key Scripts by Function

For reviewers who wish to trace a specific result to its source code:

| Result | Script |
|---|---|
| Ch1 Mahalanobis joint outlier | `analysis/scripts/joint_outlier_score_canonical.py` |
| Ch2 SZAT bootstrap | `analysis/scripts/szat.py` |
| Ch3 Neighbour-Drain | `analysis/scripts/neighbour_drain_test.py` |
| Canonical MCMC ensemble (1M plans) | `analysis/scripts/mcmc_ensemble_canonical.py` |
| Population MAD ratio | `analysis/scripts/population_mad_ratio.py` |
| Reock compactness | `analysis/scripts/reock_asymmetry.py` |
| CSD anchoring MCMC (10,000 plans) | `analysis/scripts/mcmc_anchoring_ensemble.py` |
| Justification tests 1–5 | `analysis/scripts/justification_tests.py` |
| SZAT robustness (§s58a6-A) | `analysis/scripts/szat.py` (10-seed replay) |
| R-hat convergence (§s58a6-B) | `analysis/scripts/simulation_convergence_diagnostics.py` |
| Sentiment intensity scoring | `analysis/scripts/submission_sentiment_llm_full.py` |
| Quote verification and cross-reference | `analysis/scripts/quote_verify_and_clean.py`, `cross_reference_submitters.py` |
| IRR validation sample | `analysis/scripts/validation_sample.py` |
| Cohen's κ computation | `analysis/scripts/compute_kappa.py` |

---

*This supplement was generated 2026-05-12 at repository HEAD `7b7b2fe`. It is a machine-readable navigation document; the definitive record is the academic report and the committed output files.*
