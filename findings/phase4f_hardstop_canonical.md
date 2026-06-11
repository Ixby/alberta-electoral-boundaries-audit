---
name: phase4f_hardstop_canonical
date: 2026-06-11
substrate: canonical (ea_*_2026_eds.gpkg + StatsCan 2021 DAs)
script_commit: 2c3b9ce0f276f10c0749d50b26e09ece2792236a
supersedes: findings/phase4f_summary.json (v0_5 DPG substrate)
---

> **Backward:**
> - `analysis/scripts/phase4f_hardstop_canonical.py` — this analysis
> - `findings/phase4f_summary.json` — superseded v0_5 predecessor
> - `findings/dpg_legacy_audit.md` §"phase4f_summary.json" — documented the supersession requirement
>
> **Forward:**
> - `reports/academic/report_academic.md` §3.3 — canonical numbers now anchor the hardstop reading

# Phase 4F population-hardstop validation — CANONICAL substrate

## Method

Area-weighted aggregation of Statistics Canada 2021 dissemination-area (DA) populations into each commission ED polygon via `geopandas.overlay(...).area / DA_area × pop_2021`. Result compared to the commission-published population; hardstop fails iff `|delta| > 2 %`.

## Results — canonical substrate vs v0_5 DPG predecessor

| Map | n EDs | warn (0.5 %) | hardstop (2 %) | median |Δ%| | max |Δ%| | v0_5 hardstop count |
|---|---:|---:|---:|---:|---:|---:|
| majority_2026 | 89 | 89 | **89** | 9.60 % | 47.02 % | 81 of 86 (v0_5 DPG) |
| minority_2026 | 89 | 89 | **89** | 10.21 % | 41.92 % | 87 of 89 (v0_5 DPG) |

## Top 5 hardstops per map (canonical)

### majority_2026

| ED | published pop | DA-derived pop | Δ% |
|---|---:|---:|---:|
| Calgary-North East | 54,541 | 28,894 | -47.02 % |
| Edmonton-Windermere | 56,944 | 36,138 | -36.54 % |
| Calgary-Shaw | 58,171 | 38,536 | -33.75 % |
| Calgary-South East | 53,551 | 35,769 | -33.21 % |
| Edmonton-South | 60,775 | 41,167 | -32.26 % |

### minority_2026

| ED | published pop | DA-derived pop | Δ% |
|---|---:|---:|---:|
| Calgary-North East | 68,145 | 39,579 | -41.92 % |
| Edmonton-Windermere | 56,944 | 36,138 | -36.54 % |
| Calgary-South East | 54,045 | 36,186 | -33.04 % |
| Edmonton-South | 60,775 | 41,167 | -32.26 % |
| Calgary-Buffalo | 66,801 | 45,376 | -32.07 % |

## Interpretation

The v0_5 DPG hardstop counts (81 / 86 majority; 87 / 89 minority) reflected a composite signal — real population displacement between 2021 census and 2026 commission *plus* DPG transcription error from the v0_5 substrate's incomplete polygon set. On the canonical substrate (official Elections Alberta shapefiles + canonical DA aggregation), the hardstop counts above measure pure 2021-to-2026 cycle-lag growth heterogeneity. The v0_5 framing in monograph §3.3 was honestly disclosed as a composite signal; this canonical recompute replaces the composite with the clean cycle-lag measurement.

## Reproducibility

```bash
python analysis/scripts/phase4f_hardstop_canonical.py
```

Script commit: `2c3b9ce0f276f10c0749d50b26e09ece2792236a`
