---
name: drain_label_shuffle_null_canonical
date: 2026-06-11
substrate: canonical (ea_*_2026_eds.gpkg + va_2023_election_day_votes.gpkg)
script_commit: 2c3b9ce0f276f10c0749d50b26e09ece2792236a
salt: drain-label-shuffle-canonical-2026-06-11
n_permutations: 10000
supersedes: findings/drain_label_shuffle_null.md (DPG-era / blended-vote substrate)
---

> **Backward:**
> - `analysis/scripts/drain_phase_b_canonical.py` — this analysis
> - `findings/drain_label_shuffle_null.md` — superseded predecessor (DPG / blended substrate)
> - `findings/drain_metric_validation.md` — the substrate-staleness discovery that motivated this re-run
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.3.5 — canonical numbers now anchor the §5.3.5 continuous-score reading
> - `findings/joint_outlier_score.json` — `neighbour_drain` block can drop its SUBSTRATE_STATUS retraction now this rerun is published

# Drain Phase B label-shuffle null — CANONICAL substrate

## Method (unchanged from original Phase B)

Continuous `drain_score = Σ intensity(X, Y)` over coupled directed adjacent pairs where

```
intensity(X, Y) = max(0, s_X − 0.15) × max(0, 0.05 − m_Y)
coupled iff losing_party(X) == losing_party(Y)
```

Null: 10,000 label-shuffle permutations — (NDP, UCP) vote vectors randomly reassigned across EDs; adjacency graph fixed.

## Substrate (this is the canonical version)

- Shapefiles: `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` + `ea_minority_2026_eds.gpkg` + 2019 enacted reference.
- VA vote layer: `data/shapefiles/canonical/va_2023_election_day_votes.gpkg`, integer columns `va_ndp` / `va_ucp` (mirrors `mcmc_ensemble_canonical.py`).
- Attribution: `representative_point()` centroid-in-polygon spatial join.
- Adjacency: queen-contiguity via `neighbour_drain_adjacency.build_adjacency` (600 m half-buffer, K-nearest fallback for isolates).

## Results

| Map | observed drain_score | null mean | null std | z-score | percentile rank | p (two-tailed) |
|---|---:|---:|---:|---:|---:|---:|
| majority_2026 | 0.007213 | 0.049257 | 0.013251 | -3.173 | 0.01% | 0.0002 |
| minority_2026 | 0.000591 | 0.028057 | 0.009987 | -2.750 | 0.01% | 0.0002 |
| enacted_2019 | 0.001530 | 0.052987 | 0.014618 | -3.520 | 0.00% | 0.0000 |

## Pre-registered Prediction A revisited

- Prediction A (drain(majority) > drain(minority)): CONFIRMED on canonical substrate.
- Observed: majority = 0.007213, minority = 0.000591.
- The original Phase B numbers (majority = 0.000179, minority = 0.006176; majority z = −2.915 "anomalously low") were computed on a DPG-era / blended-vote substrate. They are now superseded by this canonical run.

## Reproducibility

```bash
python analysis/scripts/drain_phase_b_canonical.py
```

Script commit: `2c3b9ce0f276f10c0749d50b26e09ece2792236a`
