---
title: Test-suite mutation audit — can the tests actually fail?
date: 2026-07-09
status: complete; two suite defects found and fixed; one data finding disclosed
---

> **Backward:**
> - `tests/test_scoring.py`, `tests/test_szat.py` — the suites under audit
> - `analysis/scripts/mcmc_ensemble.py`, `analysis/utils/eg_utils.py` — mutation targets
>
> **Forward:**
> - `findings/ensemble_chain1_duplication_note.md` — the data finding this audit surfaced
> - `.github/workflows/tests.yml` — runs `test_scoring.py` on every push

# Mutation audit of the audit's test suite

**Question.** Are the tests capable of failing — do they hold the code to
independent oracles, or do they merely re-derive the code's own output?

**Method.** (1) Read every test and classify its oracle. (2) Mutation testing:
deliberately break each scoring formula and record whether the suite notices.
A surviving mutant = a bug class the suite is blind to.

## Oracle classification

| Layer | Oracle type | Honest? |
|---|---|---|
| `test_szat.py` (14 tests) | Hand-computed arithmetic, worked in comments, exact `pytest.approx` values | Yes — independent oracles throughout |
| `test_scoring.py` Layer 1 (7→10 tests) | Hand-computed synthetic maps | Yes, but pre-audit it covered EG/seats/vote-share only — **no unit oracle existed for mean-median or declination** (added in this audit) |
| `test_scoring.py` Layer 2 (3 tests) | Frozen verification subset: recompute metrics from saved assignments, compare to saved values | Honest as a *tamper/drift* oracle. Both sides share `seat_results()`, so it proves the artefact matches the code **as of today** — it detects post-hoc drift (and killed formula mutants in this audit because the baseline is frozen), but could not have detected a formula that was wrong at generation time. The pre-Amendment-10 declination sign bug is the historical instance: it was caught by referee review, not by tests. |
| `test_scoring.py` Layer 3 (3 tests) | Regression scenarios with behavioural oracles | Two honest (sjoin dedup, CRS); the state-threading test was **incapable of failing** — see below |

## Mutation kill matrix (2026-07-09)

| Mutation | What it breaks | Result |
|---|---|---|
| M1 EG numerator sign flip | efficiency gap direction | KILLED (3 tests) |
| M2 mean-median flip | MM sign convention | KILLED — but *only* by the Layer-2 frozen baseline pre-audit; now also killed at unit level by `test_mean_median_hand_oracle` |
| M3 declination θ_R−θ_D (the exact pre-Amendment-10 bug, reintroduced) | Warrington sign convention | KILLED — same story as M2; now also killed at unit level by the two declination hand oracles |
| M4 seats@50/50 tie credit 0.5→1.0 | tie fractionalization | KILLED (3 tests) |
| M5 win comparison `>`→`>=` | tie-goes-to-UCP | KILLED |
| M6 `_ed_waste` threshold /2→/3 | wasted-vote threshold | KILLED (6 tests) — a first attempt appeared to survive because the mutation hit a docstring, not code: mutation tooling must anchor on unique code |
| M7 seats@50/50 swing sign flip | uniform-swing direction | KILLED (3 tests) |
| M8 `_ed_waste` tie direction | tie waste allocation | KILLED |
| M9 threading no-op: `run_ensemble` silently rebuilds from the first-seen assignment (CRITICAL #1 regression) | chunked chain-state continuity | **SURVIVED** pre-audit; KILLED after the two fixes below |

## The two suite defects (both fixed 2026-07-09)

1. **Degenerate fixture.** The state-persistence test used a 2-district
   partition. With exactly two districts, every ReCom proposal merges the
   whole map and re-splits it from the RNG stream alone — the chain is
   *memoryless*, so threaded and restart-every-chunk runs are byte-identical
   **by construction**. Instrumented proof: per-chunk drift from the seed was
   identical (24/18/21/25) in both modes on clean code. No assertion of any
   kind could have distinguished correct threading from the CRITICAL #1 bug
   on that fixture. Fixed: 3-district fixture (one pair re-splits per step;
   the third district's boundary carries state).

2. **Soft assertion.** The test asserted `threaded_drift >= broken_drift`
   (its own comment says "strictly further"), which a threading no-op
   satisfies with equality. Fixed: deterministic no-op detector — both
   phases reseed the RNG identically, so under a threading no-op the two
   final assignments are *exactly equal*; the test now asserts they differ.

Post-fix verification: clean suite green 3× consecutively (no flakiness);
M9 now fails the suite; M2/M3 now die at unit level with the Layer-2
baseline excluded.

## Collateral finding

Reading the production runner during the audit exposed a resume-path defect
(restart-from-seed + RNG rewind), and a replay probe over the committed chain
CSVs found it had fired once: 17,500 duplicated rows in canonical chain 1.
Full disclosure and no-change sensitivity analysis:
`findings/ensemble_chain1_duplication_note.md`. The resume path now fails
loudly instead of silently corrupting.

## Honest characterization of the other gates

- **CI Tests workflow**: demonstrably capable of failing — it failed for two
  weeks (missing deps) and the provenance gate failed cross-platform until
  2026-07-09. Both were environment failures, not oracle failures.
- **Provenance gate**: real oracle (SHA-256 vs committed manifest); now
  platform-independent (LF-normalized).
- **Viewer gates** (`i18n_parity`, `no_retired_figures`): tripwire-style,
  both capable of failing (parity caught a real parse error during the
  2026-07-08 locale sweep).
- **Layer-2 frozen baseline**: powerful drift detector; not a correctness
  proof of the original generation. Original correctness rests on the hand
  oracles (now covering all four metrics) plus the referee/amendment record.
