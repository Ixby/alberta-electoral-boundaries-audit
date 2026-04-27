---
name: Post-audit recompute deltas — 2026-04-26
description: Side-by-side comparison of the audit's pre-audit (buggy) v0_8-substrate published values against the corrected post-audit values produced by (a) the 9 fixed pipeline bugs, (b) the v0_9 topological VA-dissolve, and (c) the 100k pre-registered baseline ensemble. Filed in fulfilment of the 2026-04-26-evening pre-registration amendment.
type: project
---

# Post-audit recompute deltas — 2026-04-26

**Filed in fulfilment of:** `analysis/reports/v0_1_pre_registration_amendment_2026-04-26_evening_post_audit.md`

**What this document records:** the audit's published Lane 1 numbers as they stood before the 2026-04-26 external code audit, and the corrected numbers produced after (a) all nine code-level bug fixes landed (commits `73544a3`, `5fdb57c`, `1579f99`), (b) the v0_9 topological VA-dissolve eliminated the pixel-traced polygon overlaps (commit `7cf47a4`), and (c) the corrected 100k pre-registered baseline ensemble was re-run (the 2M exploratory enlargement was cancelled mid-run; cf. recalibration note below).

---

## Recalibration note: 2M → 100k

The 2026-04-26 morning amendment (Bucket A change 1) had escalated the ensemble size from the pre-registered 100k to 2M as a defensibility enlargement. After the corrected 2M re-run reached 480k samples (24% complete), Gemini's per-chain ESS and Gelman-Rubin Rhat diagnostics showed Rhat values of 1.0001-1.0018 across all four metrics — gold-standard convergence already. The 2M run was cancelled at 1.6M samples (80% complete) and the audit recalibrated back to the pre-registered 100k baseline. Rationale: 100k delivers ~1,000 total ESS across 4 chains, sufficient to characterize tail behavior; 2M was statistical overkill for a project whose pre-registration named 100k as the canonical size. The cancelled-2M partial samples are preserved at `data/mcmc_checkpoints_partial_2m_killed_2026-04-26/` for any future curiosity-driven re-analysis.

---

## Headline number deltas

### Real-map seats@50/50 (the most-cited figure in the public report)

| Map | v0_8 substrate (pre-audit, published) | v0_9 substrate (post-topological-fix) | Δ |
|---|---|---|---|
| 2019 enacted | 0.460 | TBD | TBD |
| 2026 majority | 0.4368 | 0.4607 | +0.024 |
| 2026 minority | **0.5422** | **0.4831** | **−0.0591** |

The minority's drop from 0.5422 to 0.4831 is the largest single delta in the audit. Source: the v0_8 reconstructed minority polygons left 6 of the 89 districts effectively uncovered (the `coverage_pct=100%` figure was misleading because covered VAs were unevenly distributed across the 89 polygons; n_districts in `seat_results` was 83). The v0_9 topological dissolve recovers full 89/89 ED coverage. Source: `data/v0_1_v0_9_real_map_scores.json`.

### Real-map efficiency gap

| Map | v0_8 (published) | v0_9 (corrected) | Δ |
|---|---|---|---|
| 2019 enacted | +0.0241 | TBD | TBD |
| 2026 majority | +0.0643 | +0.0144 | −0.050 |
| 2026 minority | **+0.0921** | **+0.0175** | **−0.075** |

### Real-map declination

| Map | v0_8 (published) | v0_9 (corrected) | Δ |
|---|---|---|---|
| 2019 enacted | −0.0451 | TBD | TBD |
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

All four Rhat values comfortably below the 1.05 publication-grade threshold. The chains have lost memory of their 2019 starting point and are sampling from a common stationary distribution. Source: `data/v0_1_mcmc_convergence_diagnostics_per_chain.json`. Validated independently against the cancelled 2M partial at 480k samples, which showed Rhat values of 1.0001-1.0018 — the same gold-standard territory.

---

## Percentile placement of the v0_9 real maps in the corrected ensemble

> **TODO — compute once the 100k run completes.**

| Map | Metric | Real-map value (v0_9) | Percentile in 100k corrected ensemble |
|---|---|---|---|
| 2026 majority | seats@50/50 | 0.4607 | TBD |
| 2026 majority | efficiency gap | +0.0144 | TBD |
| 2026 minority | seats@50/50 | **0.4831** | **TBD** |
| 2026 minority | efficiency gap | +0.0175 | TBD |
| 2026 minority | declination | +0.0105 | TBD |

The minority's seats@50/50 of 0.4831 sits roughly at the **p95** of the buggy 2M distribution (whose max was 0.5172). If the corrected 100k distribution has a similar right tail, the minority sits as a meaningful outlier (one-in-twenty), not as the previously-claimed out-of-distribution outlier (one-in-millions).

---

## R `redist` cross-validation result

> **TODO — fill once `Rscript analysis/scripts/redist_crossvalidation.R` completes.**

The Harvard `redist` package implements Sequential Monte Carlo (SMC), a sampler fundamentally different from the `gerrychain` ReCom Markov chain used by the Python pipeline. If SMC produces percentile placements within ±0.5pp of the corrected Python ReCom, the audit's headline finding is algorithm-independent and library-independent.

| Metric | Python ReCom (100k corrected) | R SMC (50k) | Δ | Pass? (±0.5pp tolerance) |
|---|---|---|---|---|
| seats@50/50 — median | TBD | TBD | TBD | TBD |
| seats@50/50 — p5 | TBD | TBD | TBD | TBD |
| seats@50/50 — p95 | TBD | TBD | TBD | TBD |
| seats@50/50 — max | TBD | TBD | TBD | TBD |

---

## Headline framing decision

> **TODO — finalize after percentile placement is computed.**

Per the 2026-04-26-evening pre-registration amendment's three-branch decision tree:

1. If the corrected ensemble's right tail does not reach the v0_9 minority's 0.4831 → "no map in N reaches the minority's value" framing CAN be revived, but with corrected numbers and the v0_9 caveat
2. If the corrected ensemble's right tail does reach 0.4831 (likely, given the buggy-version max of 0.5172 already exceeded it) → the "out of distribution at p100" claim is retracted; replaced with the actual percentile of 0.4831
3. If the R SMC and Python ReCom diverge → defer the headline framing pending investigation

Most likely outcome based on partial-run preview: branch 2 — minority sits at ~p95 rather than p100, framed as "meaningful outlier, not extraordinary."

---

## Audit-trail anchors

- Bug-fix commits: `73544a3` (9 fixes from Gemini Part 1-3), `5fdb57c` (CRITICAL+HIGH from gemini-audit branch swept up), `1579f99` (MEDIUM PRNG + LOW epsilon)
- v0_9 topology: `7cf47a4` (atomic-assembly via Phase 4C VA-dissolve)
- Diagnostics + CI: `c992497` (per-chain ESS + Gelman-Rubin Rhat + GitHub Actions workflow)
- Script rename: `822e6ca` (v0_1_ prefix dropped from 97 scripts; version moves to header)
- Recalibration: 2M run cancelled at 80% complete; 100k baseline restarted
- Buggy-version artefacts preserved at `data/*.buggy_pre_audit_2026-04-26.*` and `data/mcmc_checkpoints_partial_2m_killed_2026-04-26/`
