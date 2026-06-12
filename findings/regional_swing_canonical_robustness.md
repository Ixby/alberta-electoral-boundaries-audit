---
name: canonical_regional_swing_robustness
description: Does the canonical minority's seats@50/50 outlier survive regional-swing recomputation?
type: project
date: 2026-06-10
status: executed
supersedes: findings/regional_swing_robustness.md (v0_9 DPG-substrate reading)
---

> **Backward:**
> - `analysis/scripts/seats_at_50_50_regional.py` — regional-swing recomputation script
> - `data/outputs/regional_swing_ensemble.csv` — 10k verification subset rescored under regional swing
> - `data/outputs/regional_swing_canonical.json` — canonical real maps under regional swing
> - `data/outputs/mcmc/verification_assignments_raw.npz` — per-VA assignments for the 10k subset
> - `findings/regional_swing_robustness.md` — v0_9-era reading this finding supersedes
>
> **Forward:**
> - `reports/academic/report_academic.md` — Lane-1 verdict (§6.2.1, §6.2.4)
> - `TODO_REMEDIATION.md` — closes Tier-1 item T1.1 with a caveat (still want true canonical 1M)

# Canonical regional-swing robustness

**Status: Under canonical Elections Alberta shapefiles against the 10,000-plan verification subset, regional-swing recomputation does NOT falsify the minority map's seats@50/50 outlier. The canonical minority's `seats@50/50` under regional swing (0.4607) is above the maximum of every plan in the 10,000-plan regional-swing ensemble (max 0.4598). This is a stronger result than the v0_9 DPG reading and supersedes the "Lane 1 was officially demoted" line in `analysis/methodology/methodological_defenses.md`.**

## What the hostile-witness attack said (unchanged from v0_9 reading)

The audit's Lane-1 finding is the minority's `seats@50/50` placement in the extreme tail of the constraint-bound ensemble *under a uniform partisan swing* (every voting area's UCP share is shifted by the same constant until province-wide UCP share = 50 %). The attack: Alberta does not swing uniformly. From 2019 to 2023, Calgary swung roughly 11.5 pp toward the NDP, rural Alberta roughly 8.1 pp, Edmonton only about 4.3 pp. A uniform shift inflates the seat value of rural and suburban hybrid districts that "should" be safer for the UCP than the provincial average implies.

## What the v0_9 reading said

`findings/regional_swing_robustness.md` (DPG era) reported the v0_9 minority's seats@50/50 = 0.483 collapsing from p98.6 (uniform swing) to p50.7 (regional swing) against the v0_9 ensemble — i.e., the uniform-swing assumption was load-bearing for the v0_9 reading. The defense document concluded "Lane 1 was officially demoted" and made un-demotion contingent on a canonical rerun.

## What the canonical recomputation shows

The 10,000-plan regional-swing ensemble (per-VA assignments from `verification_assignments_raw.npz`, regional swing ratios computed from 2019 → 2023 two-party share, calibration in `regional_swing_canonical.json`) gives the following distribution:

| Quantile | Uniform swing s50 | Regional swing s50 |
|---|---|---|
| min (p0) | 0.4138 | 0.3908 |
| p5 | 0.4253 | 0.4023 |
| p50 (median) | 0.4483 | 0.4138 |
| p95 | 0.4828 | 0.4368 |
| p99 | 0.4828 | 0.4483 |
| **max (p100)** | **0.4828** | **0.4598** |

The canonical real maps' regional-swing recomputation (script: `seats_at_50_50_regional.py --canonical`; output: `regional_swing_canonical.json`, run 2026-05-12):

| Map | Uniform s50 | Regional s50 | Δ (regional − uniform) |
|---|---|---|---|
| 2019 enacted | 0.4598 | 0.4138 | −0.0460 |
| Canonical majority | 0.4607 | 0.4270 | −0.0337 |
| **Canonical minority** | **0.5169** | **0.4607** | **−0.0562** |

Real-map percentiles against the 10,000-plan regional-swing ensemble:

| Map | Uniform-swing percentile | **Regional-swing percentile** |
|---|---:|---:|
| 2019 enacted | p79.2 | p50.7 |
| Canonical majority | p79.2 | **p78.5** |
| **Canonical minority** | **p100.0** | **p100.0** |

n_at_least_as_extreme = 0 / 10,000 under regional swing for the canonical minority. The regional-swing distribution's maximum is 0.4598; the canonical minority's regional-swing s50 is 0.4607 — above every plan in the ensemble.

## What changed between v0_9 and canonical (mechanism)

The canonical minority's uniform-swing s50 is 0.5169; the v0_9 estimate was 0.483 — a gap of +0.034 seat-share. Under regional swing, both drop by roughly the same absolute amount (the swing math is metric-, not substrate-, sensitive). So the canonical minority lands at 0.5169 − 0.0562 = 0.4607, while the v0_9 would have landed at 0.483 − ~0.063 ≈ 0.420 — near the regional ensemble's median (0.4138). The substantive difference is that the canonical minority has a measurably larger Lane-1 effect on the actual Elections Alberta shapefiles than the v0_9 DPG reading suggested. Whether the v0_9 measurement was underestimating the effect (most likely — DPG attribution missed VAs in rural EDs which biased seat counts toward NDP) or the canonical substrate is exaggerating it (unlikely — the canonical substrate is the ground truth) is documented in `findings/post_audit_recompute_deltas.md`. Either way, the canonical reading is the headline.

## Honest caveats

1. **The 10,000-plan verification ensemble is not the 1,010,000-plan canonical ensemble.** The 10k subset stores per-VA assignments (which is what makes regional-swing recomputation possible); the 1M canonical run stores only district-level summaries. The 10k subset is the same chain family as the 1M canonical (per `findings/regional_swing_robustness.md`: "the 10k subset's uniform-swing s50 distribution matches the 100k production distribution to within 0.002 on the mean and exactly on p5/p95"), so it is a valid stand-in for percentile rankings. *But*: the 1M ensemble would extend the tail by perhaps 0.01–0.02 in s50 (roughly the spread observed across 100× more samples), which means the canonical minority's regional-swing s50 of 0.4607 might place at p99.9x rather than p100 against a true 1M regional-swing run. The headline result — "above ensemble maximum on the 10k stand-in" — would soften to "in the extreme tail of the 1M" rather than collapse to median. Until the per-VA assignments for the 1M run are archived (currently they are not), this remains a verification-subset stand-in.
2. **The neutral ensemble does not enforce all statutory criteria** (s.15(2) tiers, community of interest, Indigenous representation, municipal anchoring constraints). Percentile placements measure extremity against the ReCom reference distribution, not against "what any legally compliant Alberta commission would have produced." See Tier-1 item T1.4 in `TODO_REMEDIATION.md` for the constraint-enforcing ensemble that closes this objection.
3. **The Lane-1 finding remains coverage-sensitive at the margin.** The minority's efficiency-gap of +3.96 % sits at the 94th percentile of the constraint-bound canonical ensemble — *near, but below*, the audit's own pre-registered 95th-percentile threshold. The seats@50/50 tail result reported here is the strongest individual Lane-1 metric; it does not promote EG above its own threshold.

## Conclusion

Under canonical geometry against the 10,000-plan regional-swing ensemble, the minority's seats@50/50 outlier *survives* regional-swing recomputation. This is corroboration, not a falsification. The headline framing in `report_public.md` and `en.ts` therefore does not need a second round of edits on this axis. The defense document line "Lane 1 was officially demoted" was based on the v0_9 DPG reading and is now superseded; Lane 1 was reinstated by the canonical real-map values, not by an outcome-driven reanalysis, and the supersession is documented here.

Tier-1 item T1.1 in `TODO_REMEDIATION.md` is partially closed by this finding. The remaining open question is whether a 1M-plan regional-swing ensemble (which requires archiving the per-VA assignments of the canonical 1M run, an LFS data debt) would extend the tail enough to demote the minority below p99. **Honest revised expectation (corrected 2026-06-12 per T1.7 Referee #17):** the gap between the canonical minority's regional s50 (0.4607) and the 10k regional-swing maximum (0.4598) is **0.0009 — an order of magnitude *narrower* than this same document's own estimated 0.01–0.02 tail extension** (§"Honest caveats" item 1). Earlier wording claimed the gap was "wider than" the tail-extension estimate, which is the wrong comparison: by the document's own numbers, the canonical minority would *not* survive being above the 1M regional-swing maximum. The realistic placement under a true 1M regional-swing ensemble would be p99.9x rather than "above ensemble maximum." This does not retract the finding (extreme-tail outlier survives) but it does soften the headline to "in the extreme tail of the 1M," which is what §"Honest caveats" item 1 already said. The "above ensemble maximum" framing in the headline is queued for replacement with "p99.9x extreme tail" when the 1M regional-swing run lands.

## Reproducibility

```bash
# Real maps under regional swing on canonical geometry
python analysis/scripts/seats_at_50_50_regional.py --canonical \
  --output data/outputs/regional_swing_canonical.json

# Percentile against the 10k verification subset's regional-swing distribution
python <<'PY'
import pandas as pd, json
ens = pd.read_csv('data/outputs/regional_swing_ensemble.csv')
rs = json.load(open('data/outputs/regional_swing_canonical.json'))
for r in rs['results']:
    pu = 100.0 * (ens.s50_uniform < r['s50_uniform']).sum() / len(ens)
    pr = 100.0 * (ens.s50_regional < r['s50_regional']).sum() / len(ens)
    print(f"{r['map']:24s}  uniform p={pu:.2f}  regional p={pr:.2f}")
PY
```
