---
title: Constraint-enforcing ReCom ensemble — first run (T1.4 partial + T1.11)
date: 2026-06-13
status: executed; substantive finding
script: analysis/scripts/constraint_enforcing_ensemble.py
seed: drand-anchored salt "constraint-ensemble-v1" → 192903772
n_steps: 100,000 (single chain; ESS caveat below)
---

> **Backward:**
> - `analysis/scripts/constraint_enforcing_ensemble.py` — this run
> - `analysis/scripts/mcmc_ensemble.py` — canonical sampler (post-Amendment-10 seat_results)
> - `data/shapefiles/reference/alberta_2021_csds.gpkg` — municipal-split tally layer
> - TODO_REMEDIATION T1.4 (constraint-enforcing ensemble) + T1.11 (ε rerun)
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.4 — incorporates this result
> - `findings/pre_registration_amendment_log.md` Amendment 9 addendum — S2 specificity

# Constraint-enforcing ReCom ensemble — first run

## What this run adds over the canonical 1.01M ensemble

| Gap in canonical run | Adaptation here |
|---|---|
| Proposal ε was ±12.5% (half the documented ±25%) | **Full ε = 0.25** in the ReCom proposal (T1.11 fix) |
| s.15(2) tier (≤4 districts to −50%) unreachable; H6 freeze attempt failed at seeding | **Freeze-from-real-seed**: seed from the majority canonical map via spatial join; freeze the 5 districts below 75% of ideal on the 2021 substrate; ReCom redraws the remaining 84. Frozen votes re-attached as constants per plan → every sample is a complete 89-district plan |
| No commission-convention measurement (municipal preservation) | **Per-plan municipal-split tally** over 170 multi-VA CSDs |

**Frozen districts** (below 75% of ideal on the 2021-DA substrate): Central Peace-Notley (−43.5%), Calgary-North East (−39.7%), Lesser Slave Lake (−38.4%), Canmore-Banff (−33.7%), Calgary-South East (−25.5%). Three are the statutory s.15(2) invocations; the two Calgary suburbs are cycle-lag artifacts (legal under the commission's 2024 estimates, under-populated only on the audit's 2021 substrate — the same districts at the top of the Phase 4F share-drift table). Freezing them prevents ReCom from "fixing" districts that are not actually broken.

## Result 1 — Minority's EG flag FIRES under the constrained null

| Map | Metric | Value | Unconstrained 1.01M percentile | **Constrained 100k percentile** |
|---|---|---:|---:|---:|
| Minority | efficiency_gap | +0.0402 | p94.4 (flag withdrawn) | **p97.24 (flag fires)** |
| Minority | mean_median | +0.0104 | p99.98 | p99.99 |
| Minority | declination (Warrington) | +0.0770 | p98.79 | p99.64 |
| Minority | seats_at_50_50 | 0.5169 | p99.99 | p99.99 |
| Majority | efficiency_gap | +0.0010 | p15.5 | p28.63 |
| Majority | mean_median | −0.0362 | p0.92 | p1.33 |
| Majority | declination | −0.0267 | p20.36 | p34.45 |
| Majority | seats_at_50_50 | 0.4607 | p78 | **p57.06** |

Under the more legally faithful null, **the minority becomes more extreme on every metric (4-of-4 tail flags at ≥p95) while the majority becomes more normal on every metric** (s50 p78 → p57; declination p20 → p34; MM p0.92 → p1.33). This is the directional prediction of the §5.4.9 severity-audit paragraph confirmed empirically: constraint-respecting nulls discount tails symmetrically, and the minority's displacement survives because it lives in the drawing, not in the constraint set.

The EG flag — withdrawn at p94.4 under the unconstrained ensemble, the audit's most prominently disclosed near-miss — **crosses p95 under the constrained null** (and recall the ES-13 full-vote sensitivity independently pushed EG to +5.79%, also above threshold). The "EG sub-threshold" caveat the audit carried is now bracketed on both sides: it holds only under the specific combination of unconstrained null + election-day-only substrate.

## Result 2 — The commission-convention auxiliary is now measured, symmetrically

ReCom plans split **55–67 multi-VA municipalities (median 61, min 25, max 75)**. The real maps split **23 (majority) / 30 (minority)** under the structural battery's CY/T/SM count. Both real maps sit at ≈ **p0.00–p0.02** — far below anything the unconstrained sampler produces.

- This **empirically validates** the "commission convention" explanation for the majority's MM p0.92 NDP-tail outlier (§5.4.9): real commissions preserve municipalities at rates ReCom never reaches, and that preservation mechanically shapes partisan-metric distributions.
- It applies the auxiliary **symmetrically** (the T1.17 severity requirement): both maps are convention-compliant; the minority's partisan-metric extremity is *not* explained by convention compliance, because the majority is equally convention-compliant and sits mid-band.
- It supplies the **S2 specificity rate** the Amendment 9 addendum flagged as missing: Pr(splits ≤ 30 | ReCom plan) ≈ 0.0002. (Definition caveat: the per-plan tally uses 170 multi-VA CSDs; the battery's 23/30 counts use the CY/T/SM filter — close but not identical universes, so the percentile is indicative rather than exact. A like-for-like recount is queued.)

## Honest caveats

1. **100,000 steps, single chain.** At ~85 steps/s wall clock this is a 20-minute run, not the 1.01M-publication-grade run. Integrated autocorrelation on ReCom chains of this graph runs τ ≈ 500–800, so ESS here is roughly 125–200. Percentile claims beyond ≈ p[1, 99] are not precision-bearing; **p97.24 on the minority's EG is within resolution; the p99.99 values should be read as "extreme tail" not as precise decimals.** A 1.01M-scale constrained run (T1.4-full) is the publication-grade follow-on (≈ 3.5 h at this rate, parallelizable).
2. **Freeze set is majority-derived.** The s.15(2)+cycle-lag districts were identified from the majority seed. A minority-seeded run (freezing the minority's Rocky Mountain House-Banff Park instead of Canmore-Banff) is the symmetric robustness check (T1.4-minority-seed, queued).
3. **The constraint floor includes +0.01 slack** above the worst seed deviation (25.3% — one unfrozen district slightly exceeds ±25% on the 2021 substrate due to the same cycle-lag).
4. **Municipal splits recorded, not constrained.** Constraining splits to ≤30 would concentrate the null on convention-compliant plans — the full T1.4 vision. The recorded tally shows that would discard ≈ 99.98 % of ReCom proposals, so a split-constrained chain needs either a much longer run or a penalized-acceptance (soft constraint) design.

## Reproducibility

```bash
python analysis/scripts/constraint_enforcing_ensemble.py --steps 100000 --out-prefix constraint_enforcing_100k
```

Outputs: `data/outputs/constraint_enforcing_100k_samples.csv` (100,000 rows, %.17g lossless floats, Warrington-signed declination) + `constraint_enforcing_100k_summary.json`. Wall clock ≈ 20 min single-core.
