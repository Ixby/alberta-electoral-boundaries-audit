---
name: extended_partisan_metrics_canonical
date: 2026-06-11
substrate: canonical (ea_*_2026_eds.gpkg + va_2023_election_day_votes.gpkg + 1.01M ReCom)
script_commit: 2c3b9ce0f276f10c0749d50b26e09ece2792236a
supersedes: findings/extended_partisan_metrics.md (v0_7 DPG substrate + 10k ReCom)
---

> **Backward:**
> - `analysis/scripts/extended_partisan_metrics_canonical.py` — this analysis
> - `findings/extended_partisan_metrics.md` — superseded predecessor (v0_7 substrate)
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.2.9 — canonical numbers now anchor the §5.2.9 reading
> - `reports/academic/report_academic.md` §1.1 BH-table rows 5–6 (Lopsided Margins) — t-values to refresh

# Extended Partisan Metrics — CANONICAL substrate (Alberta 2026)

Substrate: official Elections Alberta shapefiles + canonical VA centroid-in-polygon spatial join + 1,010,000-plan canonical ReCom ensemble (4 chains × 252,500, base_seed=1432864451).

## Results

| Map | N EDs | UCP wins | Partisan Bias | PB ensemble pct | Lopsided-t | Lopsided-p | Proportionality Deviation | Responsiveness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| majority_2026 | 89 | 55 | -0.0281 | 93.31 | +3.800 | 0.0003 | +0.0237 | 1.12 |
| minority_2026 | 89 | 60 | +0.0169 | 99.99 | +3.169 | 0.0022 | +0.0271 | 1.69 |
| enacted_2019 | 87 | 57 | -0.0057 | 99.22 | +3.070 | 0.0029 | +0.0252 | 2.87 |

## Provenance compared to v0_7 predecessor

| Metric | v0_7 majority | canonical majority | v0_7 minority | canonical minority |
|---|---:|---:|---:|---:|
| Partisan Bias | −0.0402 | -0.0281 | −0.0422 | +0.0169 |
| Lopsided-t | +3.158 | +3.800 | +3.491 | +3.169 |
| Responsiveness | 1.15 | 1.12 | 2.41 | 1.69 |

## §1.1 BH-table refresh (Lopsided Margins rows 5-6)

- Row 5 (Majority Lopsided-t = 3.43 → **+3.800** on canonical substrate, p = 0.0003)
- Row 6 (Minority Lopsided-t = 3.05 → **+3.169** on canonical substrate, p = 0.0022)

The Lopsided Margins finding remains a structural property of Alberta's political geography present on the 2019 enacted baseline (Lopsided-t = +3.070) and on both 2026 commission proposals.

## Reproducibility

```bash
python analysis/scripts/extended_partisan_metrics_canonical.py
```

Script commit: `2c3b9ce0f276f10c0749d50b26e09ece2792236a`
