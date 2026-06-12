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

## Share-based recomputation (T4.9-share closed 2026-06-12)

The 2 % hardstop applied to raw census-count-vs-postcensal-estimate deltas conflates net-undercoverage rebasing (~4 pp province-wide) with actual per-ED population drift. The substrate-honest version is a per-ED **share-of-provincial-total** comparison:

| Map | n EDs | warn (>0.5 % share drift) | hardstop (>2 % share drift) | median \|Δshare\| | max \|Δshare\| |
|---|---:|---:|---:|---:|---:|
| Majority 2026 | 89 | 84 | **78** | 5.78 % | 39.24 % |
| Minority 2026 | 89 | 87 | **72** | 5.79 % | 33.39 % |

Top 5 share-drifts on each map are fast-growth Calgary/Edmonton suburbs (Calgary-North East, Edmonton-Windermere, Calgary-Shaw, Calgary-South East, Edmonton-South for majority; Calgary-Buffalo replaces Calgary-Shaw for minority). All extreme drifts are *negative* — DA-derived 2021 share is *lower* than commission-published 2026 share, consistent with these districts absorbing post-2021 subdivisions invisible to the 2021 DA aggregation.

The share-based test still flags most of the province but at a lower rate than the universe-mismatch 89/89, and the failures concentrate in identifiable greenfield-suburb classes rather than spreading uniformly. The v0_5 81/86 and 87/89 counts, the universe-mismatch 89/89, and the share-based 78/72 form a coherent decreasing sequence as substrate quality improves.

## Interpretation (revised 2026-06-12 per T1.7 Referee #13)

**The 2% hardstop is the wrong test against this universe mismatch.** Every delta in the table compares a 2021 *census-count* universe (Statistics Canada DA populations summing to 4,262,567 province-wide) against a 2026 *commission-projected-estimate* universe (commission-published per-ED populations summing to roughly the Q2-2024 postcensal estimate of 4,888,723). The two universes differ by ~4 pp on net-undercoverage rebasing alone (Alberta has the highest provincial net undercoverage), *before* any 2021-to-2024 growth. The published "89 of 89 majority / 89 of 89 minority fail the 2 % threshold" reading therefore conflates three signals that should be separated: (a) net-undercoverage adjustment, (b) actual 2021-to-2024 growth, and (c) commission's cycle-lag projection method. The "pure cycle-lag growth heterogeneity" framing in the earlier version of this section overclaimed.

**The substrate-honest test is a share-of-province comparison.** For each ED, compute its share of the provincial total under each universe (2021 DA-derived ED population ÷ 4,262,567 vs commission-published ED population ÷ 4,888,723) and report the *share* delta. This removes both level shifts (net-undercoverage and provincial-mean cycle-lag) and leaves only the per-ED *relative* drift, which is what the original hardstop was designed to flag. A re-computation under the share-comparison framework is queued (T4.9-share). Until it lands, the "89 of 89 fail" framing above is **provisional and over-states the diagnostic content** of the test. The v0_5 DPG hardstop counts (81 / 86 majority; 87 / 89 minority) reflected a composite of DPG transcription error + the same universe mismatch; neither set should be cited as evidence of commission population error without the share-based recomputation.

**Area-weighted DA interpolation introduces additional bias in fast-growth fringe districts** (Referee #13 W3). Uniform-density areal interpolation systematically biases EDs containing low-2021-population DAs that received post-2021 subdivisions (Airdrie / Chestermere / Calgary-NE / Edmonton-Windermere) — exactly the districts at the extreme tail of the table above. The repo already contains `va_attribution_population_weighted.py` for dwelling-count / building-footprint dasymetric weighting; the share-based re-run will use it.

## Reproducibility

```bash
python analysis/scripts/phase4f_hardstop_canonical.py
```

Script commit: `2c3b9ce0f276f10c0749d50b26e09ece2792236a`
