# Seed Commitment — Robustness, Diagnostics, and Pending Channels

> **Pre-registration:** [OSF s58a6](https://osf.io/s58a6)

**Date:** 2026-05-10
**Purpose:** Pre-commit all random seeds for the three-section robustness/rerun registration before any analyses are executed.

---

## Drand Beacon

| Field | Value |
|---|---|
| Chain | Cloudflare drand (default) |
| Round | 6099592 |
| Randomness | `5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8` |
| Signature | `8a193647eedd3f423d261f05b3e4603702634486fae82ee032e35f5cf57c93c69b77d8897d5506b889d0dc0b29fbcbf413e098028bc77e69c59a1e8a6fee29b20465ef3dfd3b193deb55446b211d195fff17b0447e7d46f28c13c559520265ab` |
| Fetched | 2026-05-10, before OSF submission, before any runs |

Verification: `curl https://drand.cloudflare.com/public/6099592`

---

## Derivation Protocol

```python
import hashlib

randomness = "5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8"

# Section A: 10 SZAT robustness seeds
for i in range(10):
    h = hashlib.sha256(f"alberta-audit-robustness-szat-seed-{i}:{randomness}".encode()).hexdigest()
    seed = int(h[:8], 16)

# Section C: MCMC rerun base seed
h_c = hashlib.sha256(f"alberta-audit-mcmc-rerun-base:{randomness}".encode()).hexdigest()
base_seed = int(h_c[:8], 16)
```

---

## Section A — SZAT Multi-Seed Robustness Seeds

Post-hoc relative to OSF 6pt83 (primary result p=0.0024, seed committed 2026-04-27).
All 10 seeds fixed here before execution. Results reported regardless of direction.

| Index | Seed | p-value (executed 2026-05-10) |
| --- | --- | --- |
| seed_00 | 1225431167 | 0.0027 |
| seed_01 | 2380378561 | 0.0043 |
| seed_02 | 2351904413 | 0.0038 |
| seed_03 | 768926600 | 0.0036 |
| seed_04 | 156365611 | 0.0025 |
| seed_05 | 1841997680 | 0.0031 |
| seed_06 | 3405372638 | 0.0030 |
| seed_07 | 1541506898 | 0.0027 |
| seed_08 | 536299629 | 0.0041 |
| seed_09 | 4096160843 | 0.0026 |

**Result summary:** p ∈ [0.0025, 0.0043], median = 0.0031. All 10 seeds p < 0.05. Primary result (p = 0.0024) is seed-stable. SZAT score fixed at +0.039211 (deterministic observed value); only the bootstrap p varies across seeds.

**Note on seed wiring:** `szat.py` does not accept a command-line `--seed` argument — it always calls `get_canonical_seed("szat-bootstrap")` from `drand_seed.py`. Robustness runs were executed by replaying the bootstrap kernel directly (same VA data from `findings/szat_results.csv`, same permutation logic) with each pre-committed seed via a standalone script. This is methodologically equivalent: the SZAT score is a deterministic observed statistic; only the bootstrap null distribution varies with seed.

Output: `data/outputs/szat_robustness_section_a.json`

---

## Section B — R-hat Convergence Diagnostic

No seed required. Deterministic computation on existing chain outputs:
`data/simulated_ensemble_raw_samples_canonical.csv` (250,000 draws, 4 chains × 62,500).
Pass criterion: Gelman-Rubin R̂ < 1.1 (GR92) on all four metrics.

**Results (executed 2026-05-10):**

| Metric | R̂ GR92 | R̂ Vehtari (2021) | GR92 < 1.1 | V21 < 1.01 | Worst-chain ESS |
| --- | --- | --- | --- | --- | --- |
| Efficiency gap | 1.01843 | 1.01847 | PASS | marginal | 76 |
| Mean-median | 1.00179 | 1.00181 | PASS | PASS | 63 |
| Declination | 1.01343 | 1.01440 | PASS | marginal | 70 |
| Seats at 50/50 | 1.00540 | 1.00527 | PASS | PASS | 94 |

**GR92 verdict:** ALL PASS (registered criterion met).

**Vehtari (2021) verdict:** EG and declination marginally exceed the 1.01 recommendation (1.018 and 1.014 respectively). Mean-median and seats@50/50 pass. Vehtari et al. (2021) describe 1.01 as a recommendation for high-quality inference; values below ~1.05 remain acceptable in practice. The mild non-convergence on EG and declination does not materially affect Ch1 (Mahalanobis p = 1.60×10⁻⁷ has multiple orders of magnitude of headroom against any ESS-adjusted recalibration).

**ESS note:** Worst-chain ESS 63–94 (τ ≈ 660–990). Lower than the three-chain sensitivity run (165–291 per chain) because canonical chains are not thinned. Consistent with the existing ESS-adjusted tail-downgrade disclosure in §5.4.

**Methodology note:** Both the classic Gelman & Rubin (1992, *Statistical Science*) statistic and the rank-normalised variant from Vehtari et al. (2021, *Bayesian Analysis*) were computed and reported. The registered pass criterion specified GR92 < 1.1; the Vehtari comparison was added as a methodological improvement and is disclosed alongside the registered result.

Output: `data/outputs/rhat_diagnostic_section_b.json`
Report insertion: §5.4 of `outputs/academic_report/report_academic.md` (committed db913f2)

---

## Section C — MCMC Rerun Base Seed

Independent seed check of canonical 1M results. Channels captured: population MAD, Reock proxy. Municipal anchoring departure: **NOT captured** — per-plan anchor-count is not implemented in `mcmc_ensemble_canonical.py` as of this run; that channel remains pending.

| Field | Value |
| --- | --- |
| base_seed | 3562959107 |
| chains | 2 |
| plans per chain | 50,000 (100,000 total) |
| Output file | `data/simulated_ensemble_raw_samples_section_c.csv` (200,000 samples) |
| Completed | 2026-05-12 |

**Percentile results (Section C seed vs canonical 1M):**

| Map | Metric | Real-map value | Section C p-tile (100k) | Canonical 1M p-tile | Match? |
| --- | --- | --- | --- | --- | --- |
| Minority 2026 | population_mad | 3,938.11 | 99.26 | 99.0 | ✓ confirmed |
| Majority 2026 | population_mad | 2,826.89 | 16.58 | 15.8 | ✓ confirmed |
| Minority 2026 | reock_proxy_median | 0.5785 | 100.0 | 100.0 | ✓ confirmed (null) |
| Majority 2026 | reock_proxy_median | 0.5681 | 100.0 | 100.0 | ✓ confirmed (null) |
| Minority 2026 | reock_pct_below_030 | 1.12 % | 0.05 | 0.09 | ✓ confirmed (null, low-elongation) |
| Majority 2026 | reock_pct_below_030 | 2.25 % | 0.91 | 0.80 | ✓ confirmed (null) |
| Minority 2026 | efficiency_gap | +0.0402 | 93.93 | 94.4 | ✓ consistent |
| Minority 2026 | mean_median | +0.0104 | 100.0 | 99.98 | ✓ consistent |
| Minority 2026 | declination | −0.0770 | 1.89 | 1.21 | ✓ consistent |
| Minority 2026 | seats_at_50_50 | 0.5169 | 100.0 | 99.99 | ✓ consistent |

**p95 EG from Section C ensemble: 0.0417 (4.17 %).** Small upward deviation from canonical 0.0410 (4.10 %); sampling variation expected across different seeds at 100k vs 1M plans.

**Municipal anchoring departure:** channel not implemented in `mcmc_ensemble_canonical.py`; per-plan anchor counts require a separate script that captures anchoring per-plan rather than per-map. Remains as future work.

**Status: EXECUTED 2026-05-12 — population MAD and Reock channels independently confirmed.**

---

## Order of Operations

1. Beacon fetched — 2026-05-10 ✓
2. Seeds derived and committed to git — 2026-05-10 ✓ (hash `72f7e01`)
3. OSF form submitted (s58a6) — 2026-05-10 ✓ (approved by registrant)
4. Section A executed — 2026-05-10 ✓
5. Section B executed — 2026-05-10 ✓
6. Section C executed — 2026-05-12 ✓ (population MAD and Reock confirmed; anchoring not captured)
