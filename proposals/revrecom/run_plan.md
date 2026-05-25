---
name: Reversible ReCom (RevReCom / Forest-ReCom) — run plan
description: "Ready-to-execute plan for a Reversible-ReCom robustness check against the canonical 1.01M-plan ReCom and 5,000-plan SMC ensembles. Status PREP COMPLETE — explicit principal-investigator authorization required before running. Includes parameter pre-commitment, expected-output schema, write-up scaffold, and publish-regardless commitment language so the run cannot be reframed post-hoc as p-hacking."
type: methodology
---

> **Backward:**
> - `findings/redist_python_comparison.md` — current dual-sampler cross-validation (ReCom + SMC) this plan would extend with a third sampler
> - `proposals/revrecom/pre_registration_amendment_DRAFT.md` — pre-registration amendment draft (must be signed and locked before the run)
> - `analysis/scripts/mcmc_ensemble_canonical.py` — the existing ReCom pipeline that built the 1.01M-plan canonical ensemble; this run reuses its graph, constraints, and scorer
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — canonical VA adjacency substrate (4,765 nodes / 13,385 edges)
> - external tools (not yet installed): `frcw.rs` Rust binary (https://github.com/mggg/frcw.rs) or `gerrytools.mgrp` Docker wrapper
> - cited references: Cannon, Goldbloom-Helzner, Gupta, Matthews, Suwal 2022 — "Spanning Trees and Redistricting", arXiv:2210.01401; Chen 2025 — "Balanced Spanning Tree Distributions Have Separation Fairness", arXiv:2509.15137
>
> **Forward:**
> - `proposals/revrecom/pre_registration_amendment_DRAFT.md` — pre-reg amendment, must be locked before run
> - `findings/redist_python_comparison.md` — would gain a third column (RevReCom percentile) and a tri-sampler reconciliation paragraph if executed
> - `reports/academic/report_academic.md` §5.4 — would incorporate the RevReCom result into the joint outlier analysis
> - `TODO.md` — flags this plan as ready-to-run pending PI authorization

# Reversible ReCom (RevReCom / Forest-ReCom) — run plan

**Status as of 2026-05-23: PREP COMPLETE, NOT RUN.** This file is a ready-to-execute plan. The principal investigator (Will Conner) must explicitly authorize the run, lock the pre-registration amendment (`proposals/revrecom/pre_registration_amendment_DRAFT.md`), and confirm the compute environment before any chain is started. Until that point no graph export, no Rust build, no chain proposals — no compute consumed beyond what produced this file.

## Why this would be run

The current canonical sampler cross-validation rests on Python `gerrychain` ReCom (1.01M plans) and R `redist` SMC (5,000 plans, ESS 1,116). Both agree on canonical EA geometry. A reviewer raised the specific objection that ReCom has no writable stationary distribution — you cannot point at "this is what ReCom is sampling from" and write it down. **RevReCom (Cannon et al. 2022) is the direct fix:** it is a reversible variant whose stationary distribution is the spanning-tree distribution (plan probability ∝ ∏ τ(district_i), where τ counts spanning trees of district_i). Running RevReCom on the same canonical inputs and showing it reproduces the qualitative finding (minority `seats@50/50` in the extreme upper tail) is the targeted methodological inoculation for that specific objection.

Note that RevReCom does **not** fix ReCom's spanning-tree compactness bias — it makes the bias explicit by design (the spanning-tree distribution is exactly the compactness-biased target). The SMC cross-check is the relevant counter to that separate critique. RevReCom and SMC therefore answer different objections; running RevReCom is not redundant with SMC.

## Parameters — pre-committed before run

These values are pinned here so the run cannot be tuned post-hoc to produce a desired result.

| Parameter | Value | Source / justification |
|---|---|---|
| Sampler | `frcw --variant reversible` (RevReCom) | Cannon et al. 2022; MGGG-canonical Rust implementation |
| Graph | Canonical VA adjacency (4,765 nodes / 13,385 edges) | Bit-identical to the graph used by ReCom 1.01M and SMC 5k runs |
| Seed partition | 2019 enacted Bill 33 (87 districts) | Same seed as the ReCom canonical ensemble |
| `--n-steps` | 1,010,000 | Match the ReCom canonical ensemble exactly |
| `--n-threads` | (machine-dependent, set at run time; record in log) | Throughput only; not result-affecting |
| `--pop-col` | `pop_2021` (or vote-totals proxy if integer constraint requires it — match SMC adapter) | Same as ReCom canonical |
| `--tol` | `0.25` | EBCA ±25% population band; same as ReCom canonical |
| `--batch-size` | `64` | Standard frcw value |
| `--rng-seed` | A drand-beacon round whose round-number is below the run start time and whose round-number is recorded in this file BEFORE the run | Public verifiable randomness, prevents seed-shopping |
| `--variant` | `reversible` | The RevReCom flag; without this, frcw runs vanilla ReCom |
| Burn-in | First 10% of samples discarded (consistent with ReCom canonical convention) | Same as ReCom canonical |
| Convergence diagnostic threshold | GR92 R-hat < 1.10 (publishable); R-hat < 1.05 (preferred) | Same threshold used for ReCom canonical |

**RNG seed will be filled in at authorization time, sourced from a single drand beacon round, and recorded in this file before the run begins.** No re-rolls; the first beacon round above the authorization timestamp is the seed.

## What I will report

A pre-committed list. The run produces these outputs regardless of which way the result lands.

1. **Headline minority percentile.** Where does the canonical minority's `seats@50/50` (0.5169) sit in the RevReCom ensemble distribution? Report the percentile and the number of plans equal-or-exceeding the value out of 1,010,000.
2. **Headline majority percentile.** Same for the canonical majority's value (0.4607).
3. **Convergence diagnostics.** GR92 R-hat for the partisan metrics (EG, mean-median, declination, seats@50/50). ESS per metric. Pass/fail against the R-hat < 1.10 publishable threshold.
4. **Tri-sampler reconciliation table.** Side-by-side ReCom / SMC / RevReCom for both maps with percentiles and (for RevReCom and ReCom) tail-plan counts. To be added to `findings/redist_python_comparison.md` §"Canonical ReCom ensemble — minority placement."
5. **Compactness check.** Mean and median Polsby-Popper across the RevReCom ensemble. Compare against ReCom mean PP and SMC mean PP. Direction of difference will be reported regardless of sign.
6. **Mahalanobis joint outlier.** Recompute the four-metric joint distance for both maps under the RevReCom covariance. Compare D² and the chi-squared p-value to the existing ReCom-derived D² (5.72 minority, 1.67 majority).
7. **Joint-distribution comparison plot.** Overlay RevReCom and ReCom seats@50/50 distributions on a single histogram with the real-map markers.

**Publish-regardless commitment.** Every item above will be published in `findings/redist_python_comparison.md` and in `reports/academic/report_academic.md` §5.4 within 7 days of the run completing, regardless of whether the result confirms, partly confirms, or contradicts the existing ReCom + SMC finding. If the result contradicts the headline (minority not in the extreme upper tail under RevReCom), `findings/redist_python_comparison.md` will be updated to lead with that contradiction and the audit's central claim will be re-framed accordingly. The pre-registration amendment at `proposals/revrecom/pre_registration_amendment_DRAFT.md` is the binding instrument; the principal investigator must sign and lock it before authorizing the run.

## Implementation steps

When authorized, the run sequence is:

1. **Lock pre-reg.** Sign `proposals/revrecom/pre_registration_amendment_DRAFT.md` (rename to drop `_DRAFT`), include drand round number, commit and push.
2. **Build `frcw.rs`.** Clone https://github.com/mggg/frcw.rs into `/opt/` or equivalent. `RUSTFLAGS="-C target-cpu=native" cargo build --release`. ~5–15 min if Rust toolchain is pre-installed; longer if not.
3. **Write graph adapter.** New script `analysis/scripts/export_graph_to_frcw_json.py` reads the canonical 2023 VA gpkg and writes a frcw-format JSON. Schema: `{"nodes": [...], "edges": [...], "node_attrs": {"pop_2021": [...], "assignment_2019": [...]}}`. ~30–60 min coding + verification against a known-good frcw example.
4. **Sanity run.** Run frcw with `--n-steps 10000 --variant reversible` on the exported graph. Verify it produces a JSONL output and parses cleanly. ~5–10 min.
5. **Full run.** Run with `--n-steps 1010000 --variant reversible`. Wall time on local hardware: estimated 1–2 hours (Rust binary, multi-threaded; the existing 1M ReCom run on this user's machine was ~30 min in Python with gerrychain — frcw is faster than gerrychain, but RevReCom is 1.5–2× slower than vanilla ReCom because of the reversibility correction). Total: probably similar wall time to the existing ReCom run.
6. **Parse and score.** New script `analysis/scripts/score_revrecom_ensemble.py` consumes the JSONL, applies the same metric pipeline as `mcmc_ensemble_canonical.py` (efficiency_gap, mean_median, declination, seats_at_50_50), and writes `data/outputs/revrecom_canonical_raw_samples.csv` and `data/outputs/revrecom_canonical_percentiles.csv`. Convergence diagnostics into `data/outputs/revrecom_canonical_convergence.json`. ~1–2 hours coding + run.
7. **Write up.** Add the tri-sampler reconciliation table to `findings/redist_python_comparison.md`. Update `reports/academic/report_academic.md` §5.4. ~2 hours.

Total clock from authorization to published write-up, on a working machine: **6–10 hours**, dominated by the full chain run wall time. If the remote container is the compute target, the chain run may be slower; in that case the sanity run runs in the container and the full run goes to the user's local machine.

## Environment requirements

- **Rust toolchain** (`rustc`, `cargo`) installed and on PATH.
- **Python 3.11+** with `gerrychain`, `geopandas`, `pandas`, `numpy`, `pyyaml` (already in `requirements.txt`).
- **Disk space:** approximately 2–4 GB for the JSONL chain output. Will be LFS-tracked or compressed before commit.
- **Memory:** the existing 1M ReCom run uses a few GB; RevReCom is comparable.

## What this prep does NOT include

- The graph adapter is **not written**. Implementing it would consume some hours of coding and is conditional on the authorization.
- The Rust toolchain is **not installed**. `cargo build --release` is **not run**.
- No chain proposals have been made. The RevReCom ensemble does not exist.
- The pre-reg amendment file (`proposals/revrecom/pre_registration_amendment_DRAFT.md`) is created in DRAFT form but contains a placeholder for the drand seed round number; it must be filled in and signed at authorization time.

## How to authorize

To go from PREP COMPLETE to RUNNING, the principal investigator must:

1. Open `proposals/revrecom/pre_registration_amendment_DRAFT.md`, fill in the drand round number (the first drand-beacon round above the current wall-clock minute) and the date, then save and commit (renaming to drop `_DRAFT`).
2. Confirm the parameters in this file (§"Parameters — pre-committed before run") are accepted as-is, or amend them in this file before running.
3. Instruct Claude (or self-execute) to begin step 2 of §"Implementation steps."

Until those three actions are taken, this file is documentation only.
