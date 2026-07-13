> **Backward:**
> - `analysis/scripts/attribution_sensitivity_check.py` — produces the sensitivity comparison
> - `analysis/scripts/va_attribution_area_weighted.py`, `phase4c_canonical_attribution.py` — attribution implementations
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — VA polygons with vote totals
>
> **Forward:**
> - `data/outputs/attribution_sensitivity_check.json` — output consumed by methodology defenses
> - `analysis/methodology/methodological_defenses.md` Part 1 — companion centroid-fallacy defense
> - `reports/academic/report_academic.md` §6 — cites attribution provenance

# Attribution Sensitivity Robustness Check

**Date:** 2026-05-12; rerun 2026-07-12 against the clean canonical ensemble
(DOCUMENTED CORRECTIONS C10) with the Amendment-10 declination sign
convention. The 2026-05-12 figures were both pre-rerun and pre-Amendment-10
(declination reported NDP-tail-signed); this page reflects the 2026-07-12
rerun throughout.
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
| minority | efficiency_gap | 94.54 | 99.77 | +5.23 | yes |
| minority | mean_median | 99.97 | 99.79 | −0.18 | no |
| minority | declination | 98.79 | 99.91 | +1.12 | no |
| minority | seats_at_50_50 | 99.99 | 99.81 | −0.19 | no |
| majority | efficiency_gap | 16.52 | 24.19 | +7.67 | yes |
| majority | mean_median | 0.99 | 5.74 | +4.75 | yes |
| majority | declination | 21.85 | 9.22 | −12.63 | yes |
| majority | seats_at_50_50 | 78.54 | 93.73 | +15.19 | yes |

Material threshold: ≥ 3 pp shift.

---

## Interpretation

**The discriminating question is not "does any metric shift by ≥3 pp" but "does
any metric cross the outlier/non-outlier boundary?"**

The canonical outlier thresholds are p ≤ 5 (low-tail outlier) or p ≥ 95 (high-tail outlier).

### Minority map (headline)

All four metrics remain strict outliers under both attribution variants:

- EG: p94.54 → p99.77 (shifts to more extreme, not less; sub-threshold under
  partial attribution, crosses p95 under full attribution)
- Mean-median: p99.97 → p99.79 (stable; both deep UCP-tail)
- Declination (Warrington, post-Amendment-10 sign): p98.79 → p99.91 (stays
  deep UCP-tail outlier)
- Seats@50/50: p99.99 → p99.81 (stable; both at or near ensemble ceiling)

Minority-map headline findings are attribution-stable. Full attribution
strengthens the EG finding and leaves the other three essentially unchanged.

### Majority map (comparator)

The majority map's metrics shift more, but none become outliers under either variant:

- EG: p16.52 → p24.19 (within null under both)
- Mean-median: p0.99 → p5.74 — **the one status flip**: strict outlier (NDP-tail)
  under partial attribution; within null under full attribution (barely — p5.74
  sits just outside the p5 floor). Direction unchanged (NDP-favourable). No
  headline finding for the minority map depends on this value.
- Declination (post-Amendment-10 sign): p21.85 → p9.22 (within null under
  both, on the low-tail/NDP side; moves toward but does not cross p5)
- Seats@50/50: p78.54 → p93.73 (within null under both; moves toward but does
  not cross p95)

The majority map's mean-median reading at p0.99 (partial-attribution basis) should
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
- Report caveat: `reports/academic/report_academic.md` (direction-of-travel
  table footnote and corrections table; rerun 2026-07-12 per DOCUMENTED
  CORRECTIONS C10)
