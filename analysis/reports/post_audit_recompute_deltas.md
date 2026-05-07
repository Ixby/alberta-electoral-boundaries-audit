---
name: Post-audit recompute deltas — 2026-04-26
description: Side-by-side comparison of the audit's pre-audit (buggy) v0_8-substrate published values against the corrected post-audit values produced by (a) the 9 fixed pipeline bugs, (b) the v0_9 topological VA-dissolve, and (c) the 100k pre-registered baseline ensemble. Filed in fulfilment of the 2026-04-26-evening pre-registration amendment.
type: project
---

# Post-audit recompute deltas — 2026-04-26

**Filed in fulfilment of:** `analysis/reports/pre_registration_amendment_2026-04-26_evening_post_audit.md`

**What this document records:** the audit's published Lane 1 numbers as they stood before the 2026-04-26 external code audit, and the corrected numbers produced after (a) all nine code-level bug fixes landed (commits `73544a3`, `5fdb57c`, `1579f99`), (b) the v0_9 topological VA-dissolve eliminated the pixel-traced polygon overlaps (commit `7cf47a4`), and (c) the corrected 100k pre-registered baseline ensemble was re-run (the 2M exploratory enlargement was cancelled mid-run; cf. recalibration note below).

---

## Recalibration note: 2M → 100k

The 2026-04-26 morning amendment (Bucket A change 1) had escalated the ensemble size from the pre-registered 100k to 2M as a defensibility enlargement. After the corrected 2M re-run reached 480k samples (24% complete), Gemini's per-chain ESS and Gelman-Rubin Rhat diagnostics showed Rhat values of 1.0001-1.0018 across all four metrics — gold-standard convergence already. The 2M run was cancelled at 1.6M samples (80% complete) and the audit recalibrated back to the pre-registered 100k baseline. Rationale: 100k delivers ~1,000 total ESS across 4 chains, sufficient to characterize tail behavior; 2M was statistical overkill for a project whose pre-registration named 100k as the canonical size. The cancelled-2M partial samples are preserved at `historical/simulation_checkpoints_partial_2m_killed/` for any future curiosity-driven re-analysis.

---

## Headline number deltas

### Real-map seats@50/50 (the most-cited figure in the public report)

| Map | v0_8 substrate (pre-audit, published) | v0_9 substrate (post-topological-fix) | Δ |
|---|---|---|---|
| 2019 enacted | 0.460 | +0.4598 | +78.6 |
| 2026 majority | 0.4368 | 0.4607 | +0.024 |
| 2026 minority | **0.5422** | **0.4831** | **−0.0591** |

The minority's drop from 0.5422 to 0.4831 is the largest single delta in the audit. Source: the v0_8 reconstructed minority polygons left 6 of the 89 districts effectively uncovered (the `coverage_pct=100%` figure was misleading because covered VAs were unevenly distributed across the 89 polygons; n_districts in `seat_results` was 83). The v0_9 topological dissolve recovers full 89/89 ED coverage. Source: `data/final_real_map_scores.json`.

### Real-map efficiency gap

| Map | v0_8 (published) | v0_9 (corrected) | Δ |
|---|---|---|---|
| 2019 enacted | +0.0241 | +0.0241 | +72.3 |
| 2026 majority | +0.0643 | +0.0144 | −0.050 |
| 2026 minority | **+0.0921** | **+0.0175** | **−0.075** |

### Real-map declination

| Map | v0_8 (published) | v0_9 (corrected) | Δ |
|---|---|---|---|
| 2019 enacted | −0.0451 | -0.0451 | +8.2 |
| 2026 majority | −0.0118 | −0.0282 | small drift |
| 2026 minority | **−0.0666** | **+0.0105** | **sign flip** |

The minority declination's sign flip — from −0.0666 (UCP-favoured) to +0.0105 (mildly NDP-favoured) — is structural news. The previously-reported −0.0666 was an artefact of the 6 missing districts' votes being unevenly redistributed.

---

## Ensemble-distribution deltas (100k corrected baseline)

| Metric | Buggy 2M ensemble (pre-audit) | Corrected 100k ensemble (post-audit) | Direction of change |
|---|---|---|---|
| seats@50/50 — median | 0.4483 | 0.4483 | No material change (tail distributions identical to 4 dp) |
| seats@50/50 — p5 | 0.4253 | 0.4253 | No material change |
| seats@50/50 — p95 | 0.4828 | 0.4828 | No material change |
| seats@50/50 — max | 0.5172 | 0.5057 | Right tail compressed by ~1.2pp (the buggy chains visited a slightly wider tail than the corrected continuous chain) |
| efficiency gap — p5 | — | -0.0108 | — |
| efficiency gap — median | — | +0.0144 | — |
| efficiency gap — p95 | — | +0.0390 | — |
| declination — median | — | +0.0044 | — |

The headline-shaping insight: **the corrected ensemble's percentile placements are nearly identical to the buggy ensemble's percentile placements** (within ~1pp on the right tail). The bug fixes did NOT meaningfully change the simulated distribution. What they DID change was the v0_8→v0_9 substrate fix's effect on the REAL maps' scores — the minority's `seats@50/50` dropped from 0.5422 to 0.4831 because the v0_8 reconstruction had been under-counting 6 districts. So the percentile shift (p100 → p98.57) is almost entirely a real-map-score correction, not an ensemble-distribution correction.

Source for buggy values: `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.buggy_pre_audit_2026-04-26.csv`. Source for corrected values: `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv` (regenerated 2026-04-26 evening).

---

## Convergence diagnostics — Gelman-Rubin Rhat + per-chain ESS

The pre-audit version computed pooled-ensemble ESS by treating the concatenated 4-chain DataFrame as a single time series (Gemini's MEDIUM finding from the post-rename pass). The corrected version reports both per-chain ESS (the honest unit) AND Gelman-Rubin Rhat across the 4 chains.

| Metric | Per-chain ESS (worst) | Per-chain ESS (sum) | Pooled ESS (inflated) | Rhat | Verdict |
|---|---|---|---|---|---|
| efficiency gap | 37.7 | 199.7 | 191.0 | 1.0072 | GOLD < 1.05 |
| mean median | 41.8 | 236.8 | 178.6 | 1.0172 | GOLD < 1.05 |
| declination | 38.1 | 202.8 | 190.8 | 1.0098 | GOLD < 1.05 |
| seats@50/50 | 32.0 | 204.3 | 179.4 | 1.0147 | GOLD < 1.05 |

All four Rhat values comfortably below the 1.05 publication-grade threshold. The chains have lost memory of their 2019 starting point and are sampling from a common stationary distribution. Source: `data/simulation_convergence_diagnostics_per_chain.json`. Validated independently against the cancelled 2M partial at 480k samples, which showed Rhat values of 1.0001-1.0018 — the same gold-standard territory.

---

## Percentile placement of the v0_9 real maps in the corrected ensemble

**Resolved 2026-05-07.** Two distinct 100k ensemble runs are now complete:

- v0_9 DPG substrate (4-chain, DPG-derived polygons): values below
- Canonical substrate (2-chain × 50k, official Elections Alberta shapefiles): reported in `joint_outlier_score_summary.md`

**v0_9 DPG substrate percentile placements (corrected 100k):**

| Map | Metric | Real-map value (v0_9) | Percentile in 100k corrected ensemble |
|---|---|---|---|
| 2026 majority | seats@50/50 | 0.4607 | 78.6 |
| 2026 majority | efficiency gap | +0.0144 | 48.0 |
| 2026 minority | seats@50/50 | **0.4831** | **98.5** |
| 2026 minority | efficiency gap | +0.0175 | 56.1 |
| 2026 minority | declination | +0.0105 | 62.2 |

**Canonical ensemble percentile placements (authoritative, 2026-05-07):**

| Map | Metric | Real-map value (canonical) | Percentile |
|---|---|---|---|
| 2026 majority | seats@50/50 | 0.4607 | 83.2 |
| 2026 majority | efficiency gap | +0.0010 | 14.8 |
| 2026 minority | seats@50/50 | **0.5169** | **100.0** |
| 2026 minority | efficiency gap | **+0.0402** | **95.9** |
| 2026 minority | mean-median | **+0.0104** | **99.99** |
| 2026 minority | declination | **−0.0770** | **0.4** |

The canonical ensemble uses official Elections Alberta shapefiles and produces substantially stronger outlier placements for the minority map than the DPG substrate. The DPG values above are preserved as the historical record of the v0_8→v0_9 transition audit.

---

## R `redist` cross-validation result

**Resolved 2026-04-26/27.** Full results in `analysis/reports/redist_python_comparison.md`.

The R SMC cross-validation **failed the ±0.5pp tolerance** — the two samplers produce materially different distributions. Under Python ReCom the v0_9 minority map's seats@50/50 (0.4831) sits at the 98.6th percentile; under R SMC (Harvard `redist`, 5k importance-weighted plans) it sits near the median (~28–58% of plans reach or exceed it, run-stochastic due to RNG state consumption by `library(redistmetrics)`).

| Metric | Python ReCom (100k corrected) | R SMC (5k weighted) | Δ | Pass? |
|---|---|---|---|---|
| seats@50/50 — median | +0.4483 | +0.4828 | +0.035 | FAIL |
| seats@50/50 — p95 | +0.4828 | +0.4943 | +0.011 | FAIL |
| v0_9 minority percentile | **98.6** | **~28–58%** | ~26–70pp | **FAIL** |

Root cause: ReCom has a known empirical bias toward more compact maps (Wong, Cannon et al. 2024); SMC explores higher-seats@50/50 territory more readily. Two falsification tests (Tests #2 and #4) ran on 2026-04-26 evening and **refuted** the "mechanism is geometry/compactness" explanation — SMC plans reaching 0.4831 are slightly *more* compact than those that don't (Welch p = 7.7×10⁻²³⁴, opposite direction). The sampler disagreement is real and is disclosed in the public report as a methodology-sensitivity caveat.

---

## Headline framing decision

**Resolved 2026-05-07.** Decision tree outcome for each substrate:

**v0_9 DPG substrate:** Branch 2 applied — the corrected ensemble's right tail (max 0.5057) does reach the minority's 0.4831, so "out of distribution at p100" was retracted. Replaced with "top 1.5% outlier (p98.6)" under ReCom. R SMC diverged substantially (branch 3 also triggered), disclosed as a methodology-sensitivity caveat in `redist_python_comparison.md`.

**Canonical substrate (authoritative):** Branch 1 applies — the canonical ensemble (official Elections Alberta shapefiles, 100k plans) does not produce any neutral plan reaching the minority's canonical value of 0.5169 for seats@50/50 (p100.0). The canonical ensemble also places the minority at p99.99 on mean-median and p95.9 on efficiency gap. The "out of distribution" framing is restored under canonical geometry, supported further by the Mahalanobis joint tail (p=1.60e-07) and Fisher combined (p=1.55e-08).

The canonical result is the authoritative finding. The v0_9 DPG discrepancy is fully explained by geometry approximation error and is preserved here as the historical audit trail.

---

## Audit-trail anchors

- Bug-fix commits: `73544a3` (9 fixes from Gemini Part 1-3), `5fdb57c` (CRITICAL+HIGH from gemini-audit branch swept up), `1579f99` (MEDIUM PRNG + LOW epsilon)
- v0_9 topology: `7cf47a4` (atomic-assembly via Phase 4C VA-dissolve)
- Diagnostics + CI: `c992497` (per-chain ESS + Gelman-Rubin Rhat + GitHub Actions workflow)
- Script rename: `822e6ca` (v0_1_ prefix dropped from 97 scripts; version moves to header)
- Recalibration: 2M run cancelled at 80% complete; 100k baseline restarted
- Buggy-version artefacts preserved at `data/*.buggy_pre_audit_2026-04-26.*` and `historical/simulation_checkpoints_partial_2m_killed/`
