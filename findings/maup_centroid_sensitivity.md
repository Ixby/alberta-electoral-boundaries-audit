---
name: v0_9 MAUP centroid-vs-area-weighted sensitivity — does the audit's centroid pipeline survive the Modifiable Areal Unit Problem attack?
description: Empirical refutation of the "Centroid Fallacy" hostile attack vector (methodological-defenses §1.2). Re-attributes 2023 VA votes to v0_9 majority and minority 2026 EDs under area-weighted intersection (each VA's UCP/NDP/other votes split by % of area inside each overlapping ED) and re-scores Lane 1 metrics with the corrected `seat_results()` from `mcmc_ensemble.py` (post-commit 5cc7e5c, two-party math). Reports the 4-row delta table and the implication for the audit's defensibility.
type: project
forward_dependencies:
  - analysis/methodology/methodological_defenses.md §1.2 "The Centroid Fallacy (Ecological MAUP)" — quantified-insignificance line for insertion
backward_dependencies:
  - analysis/scripts/va_attribution_area_weighted.py — area-weighted apportionment by intersection_area / VA_area
  - analysis/scripts/_v0_9_maup_compare.py — re-scoring driver (centroid vs area-weighted, both maps)
  - analysis/scripts/mcmc_ensemble.py — `seat_results()` and `score_exogenous_map()` (corrected two-party math, commit 5cc7e5c)
  - analysis/scripts/assignment_va_attribution.py — original centroid-based attribution
  - analysis/scripts/assignment_va_attribution_maup.py — prior MAUP work (full-vote variant)
  - data/shapefiles/derived/va_polygons_with_2023_votes.gpkg — Election-Day VA substrate
  - data/shapefiles/derived/v0_10_topological_majority_2026_eds.gpkg
  - data/shapefiles/derived/v0_10_topological_minority_2026_eds.gpkg
  - data/votes_2023_majority_area_weighted.csv
  - data/votes_2023_minority_area_weighted.csv
  - data/maup_centroid_sensitivity.json — full output
---

# v0_9 MAUP centroid-vs-area-weighted sensitivity — verdict

## The attack vector

The audit assigns 2023 votes to 2026 EDs by spatial-joining each VA's centroid into a single 2026 ED polygon. A hostile reviewer will object: "A VA is an area, not a point. If the centroid lands on the UCP side of a boundary while half the population lives on the NDP side, the audit synthesizes an artificial margin." The textbook fix is **area-weighted attribution**: intersect each VA polygon with every overlapping ED, compute fractional weights `intersection_area / VA_area`, and apportion each party's votes proportionally. That removes the all-or-nothing artefact at the cost of one extra spatial-overlay pass.

## Method

`analysis/scripts/va_attribution_area_weighted.py` performs the overlay (`gpd.overlay` with `how="intersection"`), normalises per-VA weights to sum to 1.0, and apportions the per-VA UCP/NDP/other vote totals into per-ED CSVs. A nearest-ED fallback is applied to the 5 VAs whose polygons fall entirely outside the v0_9 ED union (lakes, edge-of-province slivers) — this matches the centroid pipeline's own `nearest_ed` fallback in `assignment_va_attribution.py`, ensuring like-for-like vote conservation. `analysis/scripts/_v0_9_maup_compare.py` then re-runs `seat_results()` (corrected two-party math, commit 5cc7e5c) on both attribution flavours and emits the comparison.

## Result — 4-number delta table (s50 is the audit's headline metric)

| map           | metric         | centroid  | area-weighted | Δ            |
|---------------|----------------|----------:|--------------:|-------------:|
| majority_2026 | seats@50/50    | 46.067 %  | 46.067 %      | **+0.0000 pp** |
| majority_2026 | efficiency_gap | +1.4362 % | +1.4362 %     | +7.7e-7 pp |
| majority_2026 | mean_median    | -0.7855 % | -0.7855 %     | -2.3e-5 pp |
| majority_2026 | declination    | -0.02823  | -0.02823      | +5.3e-7    |
| minority_2026 | seats@50/50    | 48.315 %  | 48.315 %      | **+0.0000 pp** |
| minority_2026 | efficiency_gap | +1.7456 % | +1.7456 %     | -1.8e-7 pp |
| minority_2026 | mean_median    | -1.7938 % | -1.7938 %     | -2.4e-8 pp |
| minority_2026 | declination    | +0.01051  | +0.01051      | +2.4e-9    |

The centroid scores reproduce `data/simulation_real_map_scores_250k.json` to all reported decimals — confirming the `seat_results()` baseline. The area-weighted scores diverge only at the 7th–10th decimal place. This is floating-point noise, not signal.

## Why so small? — boundaries snap to VAs

A diagnostic pass shows **only 7 VAs (carrying 1,396 votes, 0.15 % of the electorate) have a >0.01 % area sliver in a second 2026 ED, and only 3 VAs (632 votes) have a >0.1 % secondary share.** The maximum secondary share for any VA is 0.44 %. The v0_9 topological shapefiles were constructed by snapping ED boundaries to existing VA boundaries, so MAUP is not "small" — it is structurally **nullified by construction**. There is essentially nothing for area-weighted attribution to redistribute.

## Verdict

**The audit's centroid pipeline survives the MAUP attack.** Both maps' `seats@50/50` change by 0.0000 pp under area-weighted attribution — three orders of magnitude inside the 1-pp defensibility threshold. The other three Lane 1 metrics shift by floating-point noise. The 2.25-pp majority-vs-minority `s50` gap is preserved exactly. Defenders may cite this as quantified, not qualitative, refutation.

## One-liner for `methodological_defenses.md` §1.2

> **Empirical refutation (2026-04-26):** `va_attribution_area_weighted.py` re-attributes votes by `intersection_area / VA_area` instead of centroid-in-polygon; v0_9 majority and minority `seats@50/50` change by exactly +0.0000 pp under area-weighted attribution (other Lane 1 metrics shift by ≤1e-5 pp). Diagnostic: only 7 VAs have a >0.01 % area sliver in a second 2026 ED. The v0_9 topological shapefiles snap ED boundaries to VA boundaries, so MAUP is structurally nullified. See `findings/maup_centroid_sensitivity.md` and `data/maup_centroid_sensitivity.json`.
