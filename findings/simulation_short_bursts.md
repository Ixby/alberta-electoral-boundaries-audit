---
status: SUPERSEDED — DPG v0_7 / pre-shapefile substrate; canonical rerun pending (TODO_REMEDIATION T1.5)
superseded_date: 2026-06-13
note: |
  The burst-endpoint distribution below was computed on the DPG v0_7 pre-shapefile substrate
  (seed 42, 500×10 ReCom bursts). The report (§5.4.8 / §5.4.10) preserves these as the
  historical pre-shapefile analytical record; final percentile placements are the canonical
  official-shapefile run (§5.4.9). The canonical-substrate short-bursts rerun is queued at
  T1.5 (script repaired and ready; needs a dedicated compute window). Methodology is sound;
  only the substrate-specific numerical values are stale.
---

> [SUPERSEDED 2026-06-13] — DPG v0_7 pre-shapefile substrate; canonical rerun pending (T1.5).

> **Backward:**
> - `analysis/scripts/simulation_short_bursts.py` — companion script that runs the short-burst MCMC chains
> - `data/outputs/` ensemble outputs from the burst run
>
> **Forward:**
> - `reports/academic/report_academic.md` — incorporates the burst percentile-rank findings
> - `findings/README.md` — indexes this finding
> - `findings/burst_symmetry_analysis.md` — related burst-based analysis

# MCMC Short-Burst Analysis — Alberta 2026 Electoral Maps

**Config:** 500 bursts × 10 steps each; pop deviation ±25%; seed 42.
Starting point: 2019 enacted assignment. Each burst is an independent ReCom chain with a unique seed.

## Burst-endpoint distribution

| Metric | Mean | p5 | p50 | p95 | Min | Max |
|---|---|---|---|---|---|---|
| efficiency_gap | +0.0070 | +0.0009 | +0.0044 | +0.0189 | -0.0125 | +0.0292 |
| mean_median | -0.0132 | -0.0226 | -0.0125 | -0.0086 | -0.0337 | +0.0003 |
| declination | +0.0264 | +0.0070 | +0.0321 | +0.0363 | -0.0187 | +0.0587 |
| seats_at_50_50 | +0.4569 | +0.4477 | +0.4598 | +0.4713 | +0.4253 | +0.4828 |

## Real map percentile ranks within burst distribution

A high rank means the real map score is more extreme than most 10-step neighbourhood walks can reach from the 2019 starting point.

| Map | Metric | Value | Burst pct rank |
|---|---|---|---|
| 2019_enacted | efficiency_gap | +0.0241 | 98.0 |
| 2019_enacted | mean_median | -0.0077 | 98.2 |
| 2019_enacted | declination | -0.0451 | 0.0 |
| 2019_enacted | seats_at_50_50 | +0.4598 | 30.8 |
| majority_2026_v7 | efficiency_gap | -0.0024 | 3.0 |
| majority_2026_v7 | mean_median | +0.0080 | 100.0 |
| majority_2026_v7 | declination | -0.0203 | 0.0 |
| majority_2026_v7 | seats_at_50_50 | +0.5152 | 100.0 |
| minority_2026_v7 | efficiency_gap | -0.0102 | 0.8 |
| minority_2026_v7 | mean_median | -0.0108 | 84.2 |
| minority_2026_v7 | declination | -0.0941 | 0.0 |
| minority_2026_v7 | seats_at_50_50 | +0.5493 | 100.0 |

_Generated 2026-04-25 00:06 — elapsed 4181s_