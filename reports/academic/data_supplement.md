<!--
© Will Conner 2026 | CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
Data: Elections Alberta (public domain) | https://ixby.github.io
-->
> **Backward:**
> - `reports/academic/report_academic.md` — the manuscript this supplement indexes
> - `analysis/scripts/` — primary outputs referenced for verification
> - `preregistration/` — pre-registration record cited
>
> **Forward:**
> - (leaf — peer-review navigation aid; reviewer-facing only)

# Data Supplement — Alberta Electoral Boundaries Audit (Phase 1)

**Document type:** Peer-review navigation aid  
**Companion report:** `reports/academic/report_academic.md`  
**Repository HEAD at time of submission:** `7b7b2fe`  
**Date:** first generated 2026-05-12; figures current to 2026-11-10 (repository layout and counts in [§D1](#d1--repository-layout) refreshed 2026-07-13 — the `outputs/academic_report/` and `outputs/public_report/` paths below were retired when reports moved to `reports/academic/` and `reports/public/`)

---

This supplement is not a second manuscript. It is a structured index for external verifiers: where to find primary outputs, how to reproduce the key computations, the exact headline numbers for cross-checking, and the pre-registration record with timing disclosures. All findings, interpretation, and methodology are in the academic report.

---

## §D1 — Repository Layout

```
alberta_audit/
├── analysis/
│   ├── scripts/          # 133 single-responsibility Python analysis scripts (incl. 2 in automation/) and 1 R script
│   ├── methodology/      # test protocols, pre-analysis plans, defense docs
│   └── review/           # peer-review and red-team artifacts
├── data/
│   ├── shapefiles/
│   │   ├── canonical/    # authoritative Elections Alberta shapefiles (ground truth)
│   │   ├── derived/      # VA polygons with vote attribution (2015/2019/2023)
│   │   └── reference/    # 2019 enacted baseline
│   └── outputs/          # 103 CSV + 49 JSON script outputs at top level, 124 CSV + 63 JSON with subfolders (committed for reproducibility)
├── reports/
│   ├── academic/         # report_academic.md, this supplement
│   └── public/           # report_public.md
├── findings/             # per-topic result writeups referenced throughout the reports
├── preregistration/      # pre-registration record: specs, amendment drafts, run sheets; only part is filed on OSF (osf_ledger.json)
├── tests/                # pytest suite
├── config.yaml           # all path configuration (never hardcode shapefile paths)
├── requirements.txt      # pinned Python dependencies
└── CLAUDE.md             # session-bootstrap and contributor conventions (gitignored)
```

Three files are script outputs committed to git and **must not be hand-edited**:
- `data/outputs/simulation_real_map_scores_canonical.json`
- `data/outputs/simulated_ensemble_percentiles_canonical.csv`
- `data/outputs/simulation_convergence_diagnostics_canonical.json`

If any of these are absent, re-run the generating script (`mcmc_ensemble_canonical.py`) before reproducing headline results.

**DPG sunset clause.** Files generated from Derived Provisional Geometries (traced from commission PDF thumbnails) are deprecated and archived under `archive/`. The `va_polygons_*` files in `data/shapefiles/derived/` are live inputs. Files labelled `v0_8` or `v0_9` in `data/outputs/` retain DPG-era provenance and are kept for audit trail transparency only. All active analysis uses canonical Elections Alberta shapefiles.

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
| redist (R 4.6) | not pinned | SMC cross-validation only (`analysis/scripts/redist_crossvalidation.R`) |

**Install and verify:**

```bash
python -m pip install -r requirements.txt
python -c "import pandas, numpy, geopandas, shapely, pyproj; print('OK')"
python -m pytest tests/ -v
```

**Random seed protocol.** All random seeds are derived from Cloudflare drand beacon values, by one of two derivations. Round 5,500,000 (`analysis/scripts/drand_seed.py`): the first 4 bytes, big-endian, of `SHA-256(randomness_hex + salt)`, with no separator. Round 6,099,592 (s58a6): `int(SHA-256(f"{salt}:{randomness_hex}").hexdigest()[:8], 16)`. Beacon rounds and salts are documented per script in the repository; which of them are also on OSF, and from when, is set out in §D7.

---

## §D3 — Primary Data Sources

| Source | Description | Location |
|---|---|---|
| Elections Alberta canonical shapefiles | Authoritative 2026 boundary geometries for both commission proposals; provided by Elections Alberta on request and republished here (not posted on its maps page) | `data/shapefiles/canonical/ea_minority_2026_eds.gpkg`, `ea_majority_2026_eds.gpkg` |
| 2019 enacted boundaries | Pre-redistribution baseline for all comparisons | `data/shapefiles/reference/` |
| VA polygons with 2023 vote attribution | Voting areas with 2023 election-day NDP/UCP tallies and their 2019 parent ED; 2026 assignment by centroid join at run time | `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg` |
| 2023 Alberta general election results | Official tally (NDP 777,404 + UCP 928,900 province-wide) | `data/reference/alberta_2023_results.csv` |
| Statistics Canada Census Subdivision boundaries | CSD polygons used for municipal anchoring edge-crossing test | `data/shapefiles/reference/` |
| Written public submissions (1,339 posted, all read whole; the commission counts 1,345 received) and 349 hearing presentations | Full read of every record (§5.9.4, `findings/submissions_recode/`); the LLM stance analysis of §5.9.4.6–§5.9.4.7 is withdrawn | `.temp/submissions/text/` (gitignored raw text; see `findings/submission_search_findings.md` for the processed dataset) |
| Hansard transcripts | Round 1 (188 configuration-relevant turns, May 2025), Round 2 (209 configuration-relevant turns, Jan 2026) | Not committed: the text is rebuilt from the two Elections Alberta hearing-transcript PDFs (2025-2026-EBC-Public-Meeting-Hansard-Round-1.pdf and -Round-2.pdf) by `findings/submissions_recode/scripts/03_hansard.py` |

**Vote substrate note.** The SZAT channel (Ch2) uses election-day two-party totals (~896,644 combined) from the VA polygon attribution layer, not province-wide election totals. The 1,706,304 two-party figure in Alberta's 2023 results is not the VA-level denominator. This distinction is documented in §5.2.10 (post-registration VA-file note) and in DOCUMENTED CORRECTIONS C1 (§7.3) of the academic report.

---

## §D4 — Key Output Files

| Output file | Generating script | Report section |
|---|---|---|
| `findings/joint_outlier_score.json` | `joint_outlier_score_canonical.py` | §5.4.9 (Ch1 Mahalanobis) |
| `findings/szat_summary.json` | `szat.py` | §5.2.10 (Ch2 SZAT) |
| `findings/joint_empirical_bound_verification.json` | `verify_joint_empirical_bound.py` | §5.4.2 (full-run R̂, 2026-07-12) |
| `data/outputs/rhat_diagnostic_section_b.json` | committed output (`1dd5e91b`); generating code not in repo | s58a6-B R̂ at 4 × 62,500 draws (2026-05-10); superseded by the full-run R̂ |
| `data/outputs/szat_robustness_section_a.json` | committed output (`1dd5e91b`); generating code not in repo | §5.2.10 (robustness) |
| `data/outputs/csd_anchoring_results.json` | `mcmc_anchoring_ensemble.py` | §5.4.9 (anchoring) |
| `data/outputs/csd_anchoring_ensemble.csv` | `mcmc_anchoring_ensemble.py` | §5.4.9 |
| `data/outputs/sentiment_intensity_scores.csv` | `sentiment_intensity_score.py` | §5.9.4.6 (stance results withdrawn; recode pending) |
| `data/outputs/quotes_verified.csv` | `quote_verify_and_clean.py` | §5.9.4.7 (withdrawn) |
| `data/outputs/cross_reference_summary.json` | `cross_reference_submitters.py` | §5.9.4.7 (withdrawn) |
| `data/outputs/irr_validation_sample.csv` | `validation_sample.py` | §5.9.4.7 (withdrawn; the sample has not been scored) |

**Ensemble checkpoints** are in `data/simulation_checkpoints_canonical/` and are excluded from the git repository (`.gitignore`). The canonical ensemble can be reproduced from scratch with `python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 1010000` (corrected 2026-07-13: `--n-steps` is the *total* across all 4 chains, not per-chain; the previously-documented `--n-steps 252500` silently produces a quarter-scale run — see CLAUDE.md's caution note on this exact command).

---

## §D5 — Headline Results

All values below are drawn from committed output files as of the 2026-07-12 clean rerun (DOCUMENTED CORRECTIONS C10) and later corrections. File paths given for verification.

*(Note: the Ch3 block below was corrected 2026-07-08 against the canonical committed outputs `findings/drain_label_shuffle_null_canonical.json` and `findings/neighbour_drain_analysis.md`.)*

### Ch1 — Partisan Joint Outlier (Mahalanobis)

Ensemble: 1,010,000 neutral plans, 4 chains × 252,500 steps, ReCom algorithm, base_seed=1432864451. Covariance matrix estimated from the full 1M ensemble. Source: `findings/joint_outlier_score.json`.

| Map | D | D² | Joint p |
|---|---|---|---|
| Minority (March 2026) | 5.80 | 33.64 | 8.84 × 10⁻⁷ (published χ²(4) model; one estimate among several, see below) |
| Majority (March 2026) | 2.78 | 7.74 | 0.102 (within null) |
| Enacted 2019 (baseline) | 3.63 | 13.16 | 0.0105 |

The four component metrics (efficiency gap, mean-median, declination, seats at 50/50) are available in `findings/joint_outlier_score.json`. They are scored on 2023 election-day votes, the registered Phase 1 substrate.

**What the minority's p is.** It is one model's estimate, on election-day ballots only. No sampled plan reaches the minority's D² on the published measure (the ensemble maximum is 28.43), so 8.84 × 10⁻⁷ is a parametric χ²(4) extrapolation, not a measured frequency. Doubled as a conservative allowance, the estimate runs from about 1 in 20,000 to about 1 in 570,000 under other defensible modelling choices (`findings/audit_2026-11-10/joint_sensitivity.json`; exploratory):

| Version (doubled) | Chance |
|---|---:|
| Published (four measures, χ²(4)) | 1 in 565,691 |
| Hotelling T², n_eff 1,413 (covariance-estimation error only) | 1 in 449,368 |
| Rank-based (normal scores) | 1 in 238,414 |
| Drop declination (r = 0.973 with the efficiency gap) | 1 in 97,426 |
| Second sampler (Forest-ReCom, 80,000 plans) | 1 in 20,341 |

The map is far out in the tail on every version. On the rank-based version seven sampled plans are at least as extreme as the map; on the published one, none. No all-ballots version exists, because the all-ballots chains are not in the repository. The doubling was set for two channels; with Ch2 retired it corresponds to no stated family of tests. Counting sampled plans alone, the chains' autocorrelation leaves a pooled effective sample of about 4,372 for the D² series, and zero exceedances then support only p below about 3 / n_eff ≈ 0.0007 (`findings/joint_empirical_bound_verification.json`).

**Pre-registration status:** Ch1 was not pre-registered before execution. See §D7 for the timing disclosure.

### Ch2 — Swing Zone Allocation Test (SZAT)

Source: `findings/szat_summary.json`.

| Parameter | Value |
|---|---|
| SZAT score (minority − majority EG, swing VAs only) | +0.039211 |
| Null 97.5th percentile (bootstrap) | +0.036652 |
| Bootstrap p-value (i.i.d.-flip null; in effect one-tailed) | 0.0024 |
| Bootstrap N | 10,000 |
| Bootstrap seed | 23,687,475 (drand-derived) |
| Vote substrate | Election-day (~896k two-party) |
| Swing zones used | 2,110 of 4,765 VAs |
| Bootstrap 95% CI | [0.0097, 0.0367] |

**Registration:** OSF 6pt83, AsPredicted #289469, filed 2026-05-06 at 21:25 MDT (2026-05-07 UTC), after the test's first results were known. The seed's salt (`szat-bootstrap`) was committed together with the test's code and first results (2026-05-06, 18:11 MDT); no record fixes it earlier.

**Status (added 2026-07-08).** The i.i.d.-flip null is invalid, because neighbouring voting areas vote alike. Under a contiguity-respecting block-permutation null the SZAT p-value is 0.1947 (variance inflation 5.79× vs. the i.i.d.-flip null; `findings/szat_block_permutation.md`), but that test has one effective block (2,086 of the 2,110 swing-zone voting areas form a single connected component) and cannot reject for any data. SZAT is unresolved and is not used. Channel 2 is retired as a confirmatory channel; the p = 0.0024 above is retained as exploratory context. Per `report_academic.md` §4.3.3, OSF 6pt83 was filed ~3 h after the shapefile commit — the channel is classified "Exploratory-reproducible," not prospectively pre-registered.

**Artifact provenance and estimator note (2026-07-08).** The committed `findings/szat_summary.json` was overwritten on 2026-06-13 by a T1.10b block-permutation *smoke test* (n = 100, p = 0.0198; commit `cc1b290` — the commit message says "smoke test") and sat in that state until today. It was restored from the pre-smoke-test commit and then verified by a full first-principles re-run (same drand seed 23,687,475, i.i.d. null, 10,000 permutations), which reproduced **exactly 24/10,000 exceedances**, the identical SZAT score (+0.039211) and the identical null CI. The registered figure 0.0024 is the raw exceedance ratio 24/10,000; the regenerated file reports the same run as p = 0.0025 under the (b+1)/(B+1) estimator adopted per T1.10 (`bootstrap_b_extreme: 24` is recorded in the file). Both conventions describe the same permutation result. `szat.py` now diverts any non-registered configuration to `*_exploratory` output paths so a smoke test can no longer overwrite the registered artifact.

### Fisher Combination (Ch1 × Ch2)

**[SUPERSEDED 2026-06-10 — see `reports/academic/report_academic.md` §4.3.3 and §5.4.9.]** The Fisher combination of Ch1 and Ch2 (T = 39.87, p ≈ 4.61×10⁻⁸, recomputed on the clean rerun; the table below gives the figures as published on 2026-06-10) is retired: it assumed channel independence the two channels do not have (they share the 2023 vote substrate; Brown 1975), and Ch2 (SZAT) rests on an invalid i.i.d. null and is unresolved (the block-permutation test, p ≈ 0.19, cannot reject by design). The operative joint headline is Ch1 alone (published model, Mahalanobis p = 8.84×10⁻⁷). Doubled as a conservative allowance, that is p ≈ 1.77×10⁻⁶, about 1 in 566,000: one model's estimate on election-day ballots, not a measured bound, and the top of a range that runs down to about 1 in 20,000 under other defensible modelling choices (see Ch1 above). The figure here is preserved as historical record.

Historical (retired): Independence test: Pearson ρ = −0.0014, p = 0.888 (|ρ| < 0.30 threshold — PASS). Channels treated as empirically near-independent. Source: `findings/joint_outlier_score.json`. The check correlated unpaired Monte Carlo streams, not the two test statistics, so it could not show that the channels are independent; it was dropped with the Fisher combination (`report_academic.md` §4.3.3).

| Statistic (as published 2026-06-10) | Value |
|---|---|
| Fisher T | 39.028 |
| Degrees of freedom | 4 |
| Combined p | 6.87 × 10⁻⁸ |

### Ch3 — Neighbour-Drain Label Shuffle

Source: `findings/drain_label_shuffle_null_canonical.json` (label-shuffle null, 10,000 permutations, seed 460508741; the script's default seed is now beacon-derived, so reproducing the committed file needs `--seed 460508741`) and `findings/neighbour_drain_analysis.md` (coupled chain-signal counts, canonical 2026-05-23 run). **Not included in Fisher combination.**

| Map | z | p (two-tailed) | Result |
|---|---|---|---|
| Minority (2026) | −2.750 | 0.0002 | Anomalously low vs. label-shuffle null |
| Majority (2026) | −3.173 | 0.0002 | Anomalously low vs. label-shuffle null |
| Enacted 2019 (baseline) | −3.520 | 0.0 | Anomalously low vs. label-shuffle null (most anomalous of the three) |

All three maps score anomalously low against their own label-shuffle nulls, with the 2019 enacted baseline the most anomalous (z = −3.520). Shuffling district vote totals removes the spatial clustering of the vote that any real map has, so a low score against this null is expected for any real map. The p-values are b/B without the +1 correction, so 0.0 means that no permutation was as extreme. Prediction A is directionally confirmed (`prediction_A_confirmed: true` in the source JSON).

Coupled chain-signal counts (adjacency test): minority 1, majority 2, 2019 enacted 5 (ratio 0.50×, minority/majority) — a pre-registered PASS at the 1.5× threshold. Source: `findings/neighbour_drain_analysis.md`.

**Pre-registration:** OSF r3zm7, AsPredicted #289451, submitted 2026-05-06.

*(Corrected 2026-07-08: this block previously cited `findings/intermap_permutation_test_results.json` as the source — the Ch1-COMP output, not a Ch3 source — and reported superseded DPG-era values (minority p = 0.134, "within null"; majority z = −2.92, "reported as anomaly"). The canonical label-shuffle results above are from `findings/drain_label_shuffle_null_canonical.json`, which explicitly supersedes the earlier DPG/blended-substrate null.)*

### Supporting Channels (§s58a6-C, all complete)

| Channel | Minority result | Majority result | Status |
|---|---|---|---|
| Population MedAD (median absolute deviation from the median district; canonical ensemble, ±12.5% proposal band) | p99.13 (outlier under this band only); p0.013 under the ±25% statute band | p15.87 (within null); p0.0 under the ±25% statute band | DONE 2026-05-12 |
| Proxy Reock median (bounding-box diagonal) | p100 (anomalously compact) | p100 (anomalously compact) | Null finding |
| CSD anchoring edge-crossing (MCMC, 10,000 plans) | 29.75% → p100 | 37.63% → p100 | Null finding (see note) |
| Justification tests 1–5 (population or area necessity: was the line forced?) | All 5 fail on necessity; the minority did not claim necessity. On its stated reasons none of the six contested redraws fails (§5.9.6) | — | DONE |

**MedAD note.** This channel is not the 3,180 / 4,707 MAD headline, which is the mean absolute deviation on the commission's tables. It compares the 89-district commission maps with 87-district plans. Measured as a share of each map's own quota, the canonical-band placements are p99.6 (minority) and p21.0 (majority). Sources: `data/simulation_checkpoints_canonical/chain*_samples.csv` and `data/outputs/simulated_ensemble_percentiles_eps_full.csv`.

**CSD anchoring note.** Both maps exceed all 10,000 neutral plans on CSD boundary-following (ensemble median 17.82%, 5th–95th percentile range [16.73%, 18.97%]). This indicates both commission maps are more anchored to municipal divisions than random plans — the expected direction for commission work. The pre-registered alternative direction (minority < ensemble median) is not confirmed. This channel does not add to the Fisher combination. Source: `data/outputs/csd_anchoring_results.json`.

### SZAT Robustness (§s58a6-A)

Ten pre-committed seeds derived from drand round 6099592. Source: `data/outputs/szat_robustness_section_a.json`.

| Statistic | Value |
|---|---|
| Primary p (registered seed) | 0.0024 |
| Range across 10 seeds | [0.0025, 0.0043] |
| Median across 10 seeds | 0.0031 |
| All seeds p < 0.05 | Yes |

### Submission Sentiment Cross-Reference (§5.9.4.7)

**Withdrawn.** The support/oppose labels behind this cross-reference are unreliable: in a random sample read in full, 26 of 31 stance labels were wrong for the configuration they were attached to (`findings/audit_2026-11-10/submissions_sample48_judgements.csv`). A full read of every submission and hearing presentation (`findings/submissions_recode/`) replaces those labels; it counts requests by place, and no alignment counts against the minority's rationales have been rebuilt from it. The committed outputs (`data/outputs/cross_reference_summary.json`, `data/outputs/submission_sentiment_llm_full_results.csv`) are kept for the record and should not be cited. The 60-row human annotation sample (`data/outputs/irr_validation_sample.csv`) has not been scored.

---

## §D6 — MCMC Convergence Diagnostics

4-chain ensemble, 252,500 steps per chain (1,010,000 plans; the 2026-07-12 clean rerun). Gelman-Rubin R̂ computed per metric on the full run. Pre-registered criterion: GR92 R̂ < 1.1. Sources: `findings/joint_empirical_bound_verification.json` (R̂) and `data/outputs/simulation_convergence_diagnostics_canonical.json` (n_eff).

| Metric | R̂ (GR92) | GR92 < 1.1 | V21 < 1.01 | n_eff (pooled, lag-capped) | n_eff (pooled, uncapped) |
|---|---|---|---|---|---|
| Efficiency gap | 1.00011 | **PASS** | **PASS** | 1,522 | 1,037 |
| Mean-median | 1.00205 | **PASS** | **PASS** | 1,448 | 1,250 |
| Declination | 1.00016 | **PASS** | **PASS** | 1,513 | 1,039 |
| Seats at 50/50 | 1.00149 | **PASS** | **PASS** | 1,413 | 894 |

The pipeline's n_eff stops the autocorrelation sum at lag 2,000, where the autocorrelation is still 0.05 to 0.07, so the capped figures are upper bounds. Uncapped, the million plans are worth about 1,000 independent draws, roughly 900 to 1,300 depending on the measure and the estimator (`findings/audit_2026-11-10/ess_uncapped.json`). Seats at 50/50 is just under the report's 1,000 floor on the pooled estimate.

All four metrics satisfy the registered GR92 < 1.1 criterion and the stricter Vehtari (2021) 1.01 recommendation. The rank-normalized split R̂ was recomputed from the four chain files in `data/simulation_checkpoints_canonical/`. The registered s58a6-B diagnostic (`data/outputs/rhat_diagnostic_section_b.json`) was computed on 2026-05-10, at 4 × 62,500 draws. At that stage all four metrics passed GR92 < 1.1, and efficiency gap and declination sat just above the Vehtari 1.01 line. The academic report gives the full-run table in §5.4.2.

---

## §D7 — Pre-Registration Record

Not all registrations preceded their data. Every OSF entry was filed after the official shapefiles arrived on 2026-05-06 at 09:51 MDT, and 6pt83 was filed after its test's first results were known; filing times relative to each channel's data are in the academic report's §4.3.3. Dates below are Alberta time. Registration links are listed in the academic report's §4.3.3 table and in `preregistration/seed_commitments.md`.

| OSF ID | AsPredicted ID | Submitted | Covers |
|---|---|---|---|
| w2s8k | #289449 | 2026-05-06 | DPG v11 geometry validation (S2-01 / shapefile integrity); holds no seed |
| r3zm7 | #289451 | 2026-05-06 | Ch3: Neighbour-Drain label shuffle |
| qsgy8 | #289452 (Part A: the 89-seat comparison); #289455 (the 91-seat scorecard) | 2026-05-06 | Phase 2 comparison (predictions H2 and H3, both failed) and four tripwires for the November map, reported beside the November verdict |
| 6pt83 | #289469 | 2026-05-06, 21:25 MDT (2026-05-07 UTC) | Ch2: SZAT bootstrap null test; filed after its first results were known |
| 9wp5y | — | 2026-05-06, 22:27 MDT (2026-05-07 UTC) | 17-test November checklist; scored on the panel's map on 2026-11-09 (`findings/checklist_9wp5y_panel_map.md`); Amendments 5 onward are filed as its updates |
| s58a6 | — | 2026-05-10 | §s58a6-A SZAT robustness (10 seeds); §s58a6-B R-hat diagnostics; §s58a6-C Section C channels (population MAD, Reock, anchoring) |
| yvc7g | — | 2026-05-10 | B7 inter-map permutation test (Ch1-COMP); filed after shapefile receipt and after both maps' scores existed |
| he53s | — | 2026-07-09, 23:42 MDT (2026-07-10 UTC) | Forest-ReCom Phase A sampler-robustness check (filed before the registered run; a 500-step software test preceded it; registered rule met on all four metrics, inconclusive at pooled n_eff 61–124) |
| u47bq | — | 2026-07-14 | Lane 3 process scorecard — nine protective process features; prospective for the November committee process, retrospective/descriptive for the commission process |

### Timing Disclosure — Ch1 (Mahalanobis Joint Outlier)

The canonical Mahalanobis joint outlier test (Ch1) was not pre-registered. Neither the joint metric nor the combination method was named or specified on OSF before the data were examined, so Ch1 and the combined figure are exploratory. Ch1's seeds derive from a published drand beacon value plus a label, which makes the run reproducible but does not by itself rule out seed choice.

This is disclosed as a limitation of the audit's pre-registration architecture. Ch2 cannot stand in for it: OSF 6pt83 was filed after its first results were known, its i.i.d. null is invalid, and the block-permutation test (p ≈ 0.19; §D5) cannot reject by design, so SZAT is unresolved. The Fisher combination of the two is retired (§D5). This is discussed in §4.3.3 of the academic report.

### drand Beacon Record

All random seeds are derived from Cloudflare drand (league/default, chain `8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce`). Derivation for round 6,099,592: the first 8 hex digits of `SHA-256("salt:beacon_randomness_hex")`, read as a 32-bit unsigned integer. Round-5,500,000 seeds use `analysis/scripts/drand_seed.py` (first 4 bytes of `SHA-256(randomness_hex + salt)`).

| Registration | drand round | Salt | Derived seed |
|---|---|---|---|
| Ch2 primary (6pt83) | 5,500,000 | `szat-bootstrap` (`drand_seed.py`); first committed with the test's code and first results, 2026-05-06 18:11 MDT | 23,687,475 |
| s58a6 Section A (SZAT robustness) | 6,099,592 | `alberta-audit-robustness-szat-seed-{0..9}` | 10 seeds (see `preregistration/seed_robustness_rerun.md`) |
| s58a6 Section C rerun | 6,099,592 | `alberta-audit-mcmc-rerun-base` | 3,562,959,107 |
| s58a6 anchoring ensemble | 6,099,592 | `alberta-audit-anchoring-ensemble` (recorded in `mcmc_anchoring_ensemble.py`, not in the registration) | 80,780,579 |
| Canonical ensemble base seed (not registered: w2s8k holds no seed) | 5,500,000 | `mcmc_ensemble_250k` (`drand_seed.py`); in code 2026-04-27 by the git record; on OSF from Amendment 5 (2026-11-01) | 1,432,864,451 |

s58a6 Section B (R̂ diagnostics) draws no random numbers, so it has no seed.

---

## §D8 — Key Scripts by Function

For reviewers who wish to trace a specific result to its source code:

| Result | Script |
|---|---|
| Ch1 Mahalanobis joint outlier | `analysis/scripts/joint_outlier_score_canonical.py` |
| Ch2 SZAT bootstrap | `analysis/scripts/szat.py` |
| Ch3 Neighbour-Drain | `analysis/scripts/neighbour_drain_adjacency.py` (coupled counts), `drain_phase_b_canonical.py` (canonical label-shuffle null) |
| Canonical MCMC ensemble (1M plans) | `analysis/scripts/mcmc_ensemble_canonical.py` |
| Population MAD (commission tables) and MedAD (ensemble) | `electoral_forensics_population.py` (commission-table MAD, the mean absolute deviation); `analysis/scripts/mcmc_ensemble_canonical.py` (per-plan MedAD), `joint_outlier_score_canonical.py` (percentiles) |
| Reock compactness | `analysis/scripts/mcmc_ensemble_canonical.py` (proxy Reock per plan), `joint_outlier_score_canonical.py` (percentiles); `reock.py` (true Reock, DPG-era substrate only) |
| CSD anchoring MCMC (10,000 plans) | `analysis/scripts/mcmc_anchoring_ensemble.py` |
| Justification tests 1–5 | `analysis/scripts/justification_tests.py` |
| SZAT robustness (§s58a6-A) | committed output (`1dd5e91b`); generating code not in repo |
| R-hat convergence (§s58a6-B) | committed output (`1dd5e91b`); generating code not in repo |
| Sentiment intensity scoring | `analysis/scripts/submission_sentiment_llm_full.py` (classification), `sentiment_intensity_score.py` (intensity) |
| Quote verification and cross-reference | `analysis/scripts/quote_verify_and_clean.py`, `cross_reference_submitters.py` |
| IRR validation sample | `analysis/scripts/validation_sample.py` |
| Cohen's κ computation | `analysis/scripts/compute_kappa.py` |

---

*This supplement was first generated 2026-05-12 at repository HEAD `7b7b2fe`; its figures are current to 2026-11-10. It is a machine-readable navigation document; the definitive record is the academic report and the committed output files.*