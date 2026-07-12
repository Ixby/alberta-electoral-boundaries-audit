---
title: Forest-ReCom sampler robustness check — Phase A results
date: 2026-07-10
osf: he53s
status: executed as registered; joint verdict ROBUST on all four metrics
---

> **Backward:**
> - `preregistration/osf_forest_recom_robustness.md` — binding spec (commit 264afc5b)
> - OSF registration [he53s](https://osf.io/he53s/) — filed 2026-07-10, public, pre-execution
> - `analysis/scripts/forest_recom_ensemble.py` — sampler + harness
> - `data/outputs/forest_recom_*_phaseA.*` — the four pre-committed output artifacts
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.2.7 (update owed within 30 days per prereg §8.3)
> - viewer public copy (update owed within 14 days per prereg §8.2)

# Forest-ReCom robustness check — Phase A results (as pre-registered)

## Chain of custody

- Pre-registration document committed 2026-06-10 (`264afc5b`), script scaffold same day.
- OSF registration **he53s** filed public 2026-07-10, **before any Forest-ReCom
  sample existed**; the execution gate in the script verifiably refused to run
  without a registration ID.
- Seed 949257740 derived from drand beacon round 5,500,000, salt
  `"forest_recom_robustness"`; chain seeds from the pre-registered per-chain
  salts (`_chain_0` … `_chain_3`). Anyone can recompute all five from the
  public beacon.
- Executed 2026-07-10 immediately after filing: 4 chains × 25,000 steps,
  5,000-step burn-in per chain, substrate and constraints identical to the
  canonical run, proposal method swapped to the two-root Wilson
  spanning-forest sampler (the only difference, threaded through
  `run_ensemble(proposal_method=...)`).

## Pre-registered decision rule — outcome

|p_canonical(m) − p_forest(m)| per metric; <2 pp Robust, 2–5 pp Borderline, ≥5 pp material shift:

| Metric | Canonical (1.01M ReCom) | Forest Phase A (80k reporting) | \|Δ\| | Verdict |
|---|---|---|---|---|
| Efficiency gap | p94.39 | p93.58 | 0.81 pp | **Robust** |
| Mean–median | p99.98 | p99.64 | 0.34 pp | **Robust** |
| Declination | p98.79 | p98.83 | 0.04 pp | **Robust** |
| Seats @ 50/50 | p99.99 | p99.88 | 0.11 pp | **Robust** |

**Joint verdict (prereg §7): the canonical claim survives.** Per the
pre-committed language: *"Forest-ReCom Phase A (100 k) yields percentile ranks
within ±5 pp of canonical ReCom on every partisan metric."* No metric came
within an order of magnitude of the 5-pp qualification threshold.

## Diagnostics (prereg §6.6)

| Metric | R̂ (GR92, 4 chains) | τ | n_eff (pooled, post burn-in) |
|---|---|---|---|
| Efficiency gap | 1.01161 | 688 | 116 |
| Mean–median | 1.05181 | 1,163 | 69 |
| Declination | 1.00708 | 646 | 124 |
| Seats @ 50/50 | 1.03491 | 1,301 | 61 |

Trace plot: `data/maps/mcmc/forest_recom_phaseA_traces.png`.
Forest-proposal acceptance: 99,980 accepted / 100,079 proposal calls /
99 pair-reselections across all chains (per-proposal forest redraws for
population balance averaged ~7).

## Honest limitations — reported, not hidden

1. **The prereg's ESS target is not met.** §6.4 targeted ≥200 effective
   samples per metric per chain; the run delivered pooled n_eff of 61–124.
   The forest proposal mixes more slowly than spanning-tree ReCom on this
   substrate (τ up to ~1,300 vs the canonical ~600–700). Consequence: the
   Monte Carlo error on the Phase A percentiles is larger than the observed
   deltas for the two slow metrics (at n_eff≈116, the SE on the minority's EG
   percentile is roughly ±2 pp). The **verdicts under the pre-registered rule
   stand as computed**, but the honest reading of the 0.04–0.81 pp deltas is
   "indistinguishable from zero at this run size," not "measured tiny shifts."
   A Phase B at 1M samples (with dispersed starts) would resolve the deltas to
   ~±0.3 pp; per the prereg, Phase B is optional after a clean Phase A and
   would be filed as its own registration before execution.
2. **R̂ on the two slow metrics (1.052, 1.035) exceeds the strict 1.01
   recommendation** though both pass the registered GR92 < 1.1 criterion —
   consistent with the low ESS, same cause, same Phase B remedy.
3. **Same-start chains.** All four chains start from the 2019-derived seed
   partition (the prereg pinned this design). Between-chain agreement is
   therefore weaker evidence of mixing than dispersed starts would give.
4. The canonical comparison percentiles are those of the 1.01M ensemble as
   regenerated clean on 2026-07-12 (`findings/ensemble_chain1_duplication_note.md`;
   the prior ensemble contained a disclosed chain-1 duplication that was corrected
   before this Phase A execution. Sensitivity analysis showed the duplication
   affected no percentile by more than 0.07 pp, far below all deltas here).

## What this does and does not show

It shows the minority map's tail position is **not an artifact of
spanning-tree compactness weighting** — swap the proposal's spanning
structure and the percentiles barely move. It does not address constraint
realism (the s.15(2)-pinned companion remains future work), sample-size
resolution (Phase B), or anything about intent.

## Post-registration code changes (Amendment 13)

The execution harness was wired *after* OSF he53s was filed (the registered
scaffold's sampler was complete but its `main()` was gated), one import-error
crash was fixed between execution attempts (attempt 1 died before drawing any
sample), and the prereg's "Aldous-Broder" naming was resolved to the
implemented multi-root Wilson sampler (distribution-identical; the document's
own citations are the LERW literature). Full detail, and why the chain of
custody survives (no sample predates either the registration or the final
harness), at `findings/pre_registration_amendment_log.md` Amendment 13 —
flagged by the author on execution day.
