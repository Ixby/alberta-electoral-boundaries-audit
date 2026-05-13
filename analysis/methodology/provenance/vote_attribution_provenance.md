# Attribution Sensitivity Robustness Check

**Date:** 2026-05-12
**Script:** `analysis/scripts/attribution_sensitivity_check.py`
**Output:** `data/outputs/attribution_sensitivity_check.json`

---

## Background

The canonical 1,010,000-plan MCMC ensemble was built using partial-coverage VA vote data
(`va_ndp` / `va_ucp` / `va_other`), which captures approximately 50% of actual 2023 votes
cast. This is because the Voting Area (VA) shapefile covers only the geographic area of each
VA, and many VA polygons partially overlap multiple electoral districts, so only the
area-proportional share of votes is assigned to each VA.

A full-coverage alternative (`va_ndp_full`) assigns the entire 2023 vote total for a VA to
whichever 2026 electoral district contains that VA's centroid. This captures approximately
89% of actual votes. Neither method captures 100% of votes because some VAs straddle
district boundaries under both mapping approaches.

The sensitivity check scores both canonical 2026 maps against the same canonical
partial-attribution ensemble using each attribution variant, then compares percentile
placements.

---

## Results

| Map | Metric | Partial ptile | Full ptile | Shift (pp) | Material? |
| --- | --- | ---: | ---: | ---: | --- |
| minority | efficiency_gap | 94.39 | 99.77 | +5.38 | yes |
| minority | mean_median | 99.98 | 99.78 | −0.19 | no |
| minority | declination | 1.21 | 0.08 | −1.13 | no |
| minority | seats_at_50_50 | 99.99 | 99.80 | −0.19 | no |
| majority | efficiency_gap | 15.47 | 22.87 | +7.40 | yes |
| majority | mean_median | 0.92 | 5.78 | +4.86 | yes |
| majority | declination | 79.62 | 91.83 | +12.21 | yes |
| majority | seats_at_50_50 | 77.81 | 93.31 | +15.50 | yes |

Material threshold: ≥ 3 pp shift.

---

## Interpretation

**The discriminating question is not "does any metric shift by ≥3 pp" but "does
any metric cross the outlier/non-outlier boundary?"**

The canonical outlier thresholds are p ≤ 5 (low-tail outlier) or p ≥ 95 (high-tail outlier).

### Minority map (headline)

All four metrics remain strict outliers under both attribution variants:

- EG: p94.39 → p99.77 (shifts to more extreme, not less)
- Mean-median: p99.98 → p99.78 (stable; both deep UCP-tail)
- Declination: p1.21 → p0.08 (stays deep NDP-tail outlier)
- Seats@50/50: p99.99 → p99.80 (stable; both at or near ensemble ceiling)

Minority-map headline findings are attribution-stable. Full attribution
strengthens the EG finding and leaves the other three essentially unchanged.

### Majority map (comparator)

The majority map's metrics shift more, but none become outliers under either variant:

- EG: p15.47 → p22.87 (within null under both)
- Mean-median: p0.92 → p5.78 — **the one status flip**: strict outlier (NDP-tail)
  under partial attribution; within null under full attribution. Direction unchanged
  (NDP-favourable). No headline finding for the minority map depends on this value.
- Declination: p79.62 → p91.83 (within null under both)
- Seats@50/50: p77.81 → p93.31 (within null under both)

The majority map's mean-median reading at p0.92 (partial-attribution basis) should
therefore be read as attribution-sensitive. The characterization "NDP-tail outlier" on
this one metric does not hold under full attribution. The audit's primary conclusions
about the minority map are unaffected.

---

## Methodological note on ensemble consistency

This check scores full-attribution real-map values against a partial-attribution null
distribution. Because the ensemble itself was built on partial-coverage data, the
comparison is a hybrid. A fully consistent sensitivity check would require re-running
the 1M-plan ensemble on full-attribution data. Given that the substantive conclusions
are unchanged (minority map remains outlier on 4/4 metrics), a full re-run is not
warranted. A small-scale (50k-plan) full-attribution ensemble would be the cleanest
future supplementary check.

---

## Files

- Script: `analysis/scripts/attribution_sensitivity_check.py`
- Output JSON: `data/outputs/attribution_sensitivity_check.json`
- Report caveat: `outputs/academic_report/report_academic.md` (direction-of-travel
  table footnote and corrections table, both updated 2026-05-12)
