# v0.1 St. Albert-Sturgeon — Counterfactual Non-Existence Constraint-Search Check

**Date:** 2026-04-26
**Scope:** Substantiate or revise the public-report verdict that the St. Albert-Sturgeon hybrid "stands" because "no other configuration satisfies both the community-of-interest and the ±25% rule simultaneously." Verdict: **The 'Stands' verdict is defensible but the 'no other configuration' framing is an unproven counterfactual; the strongest defensible reading is that the minority's St. Albert-Sturgeon configuration is the one configuration where the minority and the majority independently arrived at the same answer.**

## Source the minority cites

**The minority commissioners do not, in fact, publish a per-district rationale for St. Albert-Sturgeon in Appendix E of the 2025–26 EBC final report.** The audit's own rationale inventory (`analysis/methodology/v0_1_minority_rationales_inventory.md`) lists 18 minority district-specific rationales (R1–R18); none of them covers a St. Albert-area district. The school-division coherence file (`analysis/methodology/v0_1_school_division_coherence.md`, "St. Albert-area hybrid" subsection) explicitly notes: "no explicit minority rationale in the R1–R18 inventory names this district."

The "population balancing on Edmonton-corridor constraints" framing in the public-report bullet (line 201 of `report_public.md`) is the audit's gloss, not a direct quotation from the minority. The minority simply *includes* a St. Albert-Sturgeon hybrid in its proposed map; it does not separately defend the configuration in Appendix E.

This is structurally important: Claims 5 (Lethbridge) and 7 (St. Albert-Sturgeon) in the public report's "six of seven" framing are both checked against rationales that the minority did not actually publish in Appendix E. Both are characterised as audit-internal verdicts about what the minority *would have* argued or what configuration *constraints permit*, rather than tests of stated minority claims against primary-source data.

## Test method

The "no other configuration satisfies both the community-of-interest and the ±25% rule simultaneously" claim is a counterfactual non-existence claim. To formally test it, one would need to enumerate all electoral-district configurations for the St. Albert area that:

(a) keep the City of St. Albert as a coherent community of interest,
(b) keep Sturgeon County (or its constituent municipalities) as a coherent community of interest, and
(c) achieve population per district within ±25% of the provincial quota (41,197–68,661 for 89 seats).

Three approaches were considered for this check:

1. **MCMC-ensemble query.** The audit ran a 250,000-step Monte Carlo Markov Chain ReCom ensemble (4 chains × 250k = 1,000,000 maps) at v0.8, stored in `data/mcmc_checkpoints_250k_v0_8/`. In principle, one could query the ensemble to count how many simulated maps produce a St. Albert-Sturgeon-like configuration that satisfies both rules.
2. **Closed-form arithmetic check.** The City of St. Albert (CSD 4811062) has a 2021 Census population of **68,232**, which is below the 68,661 statutory ceiling and above the 41,197 floor. Sturgeon County (CSD 4811059) has a population of 20,061, plus Morinville (CSD 4811068) at 10,385, Legal, Gibbons, and assorted smaller communities. The relevant question is whether St. Albert can stand as a single ED.
3. **Majority-map comparison.** Whether the majority's St. Albert configuration is structurally identical to the minority's, or whether the majority finds a clean distinct alternative.

Approach 1 is **not feasible from the audit's filed data.** The MCMC ensemble samples (`chain0_samples.csv` through `chain3_samples.csv`) store only ten aggregate metrics per step: `efficiency_gap, mean_median, declination, seats_at_50_50, ucp_seats, n_districts, ucp_vote_share, step, chain, chunk`. **Per-district assignments are not stored in the checkpoint files.** The audit's MCMC pipeline computes summary statistics on the fly without persisting district memberships. To answer "how many ensemble maps produce a viable St. Albert-Sturgeon configuration," the ensemble would need to be re-run with per-step district-assignment serialization — a non-trivial engineering task, not a query on existing data.

Approach 2 *was* run for this file. Approach 3 *was* run for this file. Findings below.

## Data sources

- **CSD populations:** `data/alberta_2021_csd_populations.csv` — City of St. Albert (DGUID 2021A00054811062) population **68,232**; Sturgeon County (DGUID 2021A00054811059) **20,061**; Morinville (DGUID 2021A00054811068) **10,385**.
- **Minority district populations:** `data/v0_1_minority_2026_populations.csv` — St. Albert (single district, row 83) **54,589** (-0.62%, within ±25%); St. Albert-Sturgeon (hybrid, row 84) **52,334** (-4.72%, within ±25%).
- **Majority district populations:** `data/v0_1_majority_2026_populations.csv` — St. Albert (row 82) **59,935** (+9.11%); St. Albert-Sturgeon (row 83, hybrid) **54,214** (-1.30%).
- **MCMC ensemble (header only, no per-district assignments):** `data/mcmc_checkpoints_250k_v0_8/chain{0,1,2,3}_samples.csv` (4 chains, 250k samples each, ~30MB per file).
- **School-division geometry:** `analysis/methodology/v0_1_school_division_coherence.md` — St. Albert Public Schools serves City of St. Albert only; Sturgeon Public Schools serves Morinville/Legal/Gibbons/Sturgeon County (not the City of St. Albert).
- **Public-submission inventory:** `analysis/reports/v0_1_claim_significance_analysis.md` row 7 — zero engaged-citizen submissions propose a clearly distinct minority alternative for St. Albert-Sturgeon.

## Findings

**Finding 1: A stand-alone St. Albert is mathematically permitted.** The City of St. Albert's 2021 population (68,232) is just below the ±25% statutory ceiling (68,661 for 89 seats). A stand-alone "St. Albert" district at 68,232 sits at +24.2% deviation — within the ±25% rule by 429 residents. This means the audit's "no other configuration satisfies the ±25% rule" framing is **not strictly correct**. A configuration of "City of St. Albert as a single district + Sturgeon County paired with Edmonton-corridor or Morinville-Legal-Gibbons hybrid neighbours" is mathematically feasible.

**Finding 2: Both the majority and the minority chose a 'St. Albert + St. Albert-Sturgeon' two-district pairing.** This is the load-bearing observation for the public-report 'Stands' verdict. The audit's filed evidence shows:

- **Minority map:** "St. Albert" (54,589) + "St. Albert-Sturgeon" (52,334). Both within ±25%.
- **Majority map:** "St. Albert" (59,935) + "St. Albert-Sturgeon" (54,214). Both within ±25%.

The two maps disagree on the exact slice between the two districts (the minority pulls more population into St. Albert proper; the majority pushes more into the Sturgeon hybrid) but agree on the structural choice of *two* districts, one named "St. Albert" and one named "St. Albert-Sturgeon." Both maps avoid the alternative of (a) a single 68,232-resident stand-alone St. Albert, or (b) a single ED that combines St. Albert with significant Edmonton territory.

**Finding 3: The school-division geometry of the area is constrained.** From `v0_1_school_division_coherence.md`: St. Albert Public Schools serves only the City of St. Albert; Sturgeon Public Schools serves Morinville/Legal/Gibbons/Sturgeon County rural. Greater St. Albert Roman Catholic serves a larger footprint covering both. The City of St. Albert is bordered by City of Edmonton on three sides (south, southeast, southwest) and by Sturgeon County on the north. Any cross-municipal hybrid that pairs St. Albert with Edmonton territory crosses a major school-division boundary (St. Albert Public ↔ Edmonton Public). The minority's chosen configuration (St. Albert ↔ Sturgeon Public via the St. Albert-Sturgeon hybrid) crosses a less-load-bearing division boundary — the school-coherence file classifies it "School-incoherent (mild)" rather than severe, in part because the Greater St. Albert Catholic catchment overlaps both sides.

**Finding 4: The MCMC ensemble cannot directly test the counterfactual.** The audit's 1,000,000-step ensemble would in principle answer "what fraction of maps produce a different St. Albert-Sturgeon configuration?" But the checkpoint files do not store per-district assignments, only ten aggregate metrics. Re-running the ensemble with per-step district-membership serialization is feasible but has not been done. The audit therefore cannot deliver the formal counterfactual non-existence proof the public-report wording implies.

**Finding 5: The public-submission record contains no clearly distinct minority alternative.** From `v0_1_claim_significance_analysis.md` row 7: zero submissions propose a different St. Albert-Sturgeon configuration. This is consistent with — but not proof of — a constraint-forced configuration. It could equally indicate that the public did not engage with this district.

## Verdict

**Stands on the underlying observation; Weakly supported on the 'no other configuration' framing.**

The qualitative reading — "this is the one contested configuration where minority and majority independently agree on the structural answer" — is strongly supported by the side-by-side population CSV comparison. Both maps choose the same two-district structure (one stand-alone-ish St. Albert, one Sturgeon hybrid) despite drawing the inter-district line differently. That convergence is consistent with the geometry constraining the answer — but it is not proof of non-existence of alternatives.

A stand-alone St. Albert at 68,232 (+24.2%) is mathematically possible but sits at the very edge of the ±25% rule, leaving no headroom for the Sturgeon County remainder to be cleanly attached to anything compact. The remainder (Sturgeon County 20,061 + Morinville 10,385 + Legal + Gibbons + smaller ≈ 35,000) is below the 41,197 floor and would need to be paired with either Edmonton-corridor neighbours (Spruce Grove, Beaumont) or an Edmonton hybrid (which crosses the heavier Edmonton Public ↔ Sturgeon Public school-division boundary). Both the majority and the minority concluded that the cleanest answer was a St. Albert + St. Albert-Sturgeon pairing, with the inter-district line drawn through the south-northern St. Albert / Sturgeon County interface.

The "no other configuration satisfies both rules" line in the public report overstates this finding. A truthful version would be: "Both the minority and majority maps converge on this two-district structure; no other configuration in the audit's documented review satisfies both the population-deviation rule and the school-catchment / commute-corridor coherence simultaneously without crossing a more load-bearing institutional boundary." That statement is defensible from the audit's filed evidence; the bald "no other configuration" is not.

## Reproducibility

To formally test the counterfactual non-existence claim, a third party would need to:

1. Re-run the audit's MCMC ensemble with per-step district-assignment serialization. This is a one-line modification to the audit's `mcmc_runner.py` (currently in `analysis/scripts/`, not directly read for this file but inferred from the metric-only checkpoint format). Output would be a per-step CSV mapping each of the ~6,000 voting areas to a district number.
2. For each of the 1,000,000 maps, identify the "St. Albert area" by intersecting the City of St. Albert CSD boundary with each map's district assignments. Count the number of districts touching the city.
3. For maps with two St. Albert-area districts, classify each as "St. Albert + St. Albert-Sturgeon" structure or as a "stand-alone St. Albert + Sturgeon-Edmonton hybrid" structure or as "St. Albert + Edmonton-hybrid" structure. Count each class.
4. Report the share of ensemble maps in each structural class.

Approximate compute cost: re-running the ensemble at v0.8 takes approximately 24 hours on the audit's reference hardware (per `v0_1_mcmc_ensemble.md` if available; estimated based on the 250k step counts). Adding per-district serialization adds ~10 GB of disk output and ~20% wall-time overhead.

The simpler closed-form check above (Findings 1–5) is reproducible immediately:

```python
import pandas as pd
csds = pd.read_csv('data/alberta_2021_csd_populations.csv')
st_albert = csds[csds['GEO_NAME'].str.contains('St. Albert')]
sturgeon = csds[csds['GEO_NAME'].str.contains('Sturgeon')]
# Verify St. Albert pop = 68,232; check ±25% rule
quota_max = 68661
print(f'St. Albert pop {st_albert.iloc[0]["population_2021"]:,.0f} vs quota max {quota_max}')
# Confirm a stand-alone St. Albert is permitted (just barely)
```

## Public-report implication

**The current public-report sentence (line 201) — "St. Albert-Sturgeon: minority commissioners said population balancing on Edmonton-corridor constraints; the constraint check confirms with the population-deviation rule and the Edmonton-corridor commute geography, no other configuration satisfies both the community-of-interest and the ±25% rule simultaneously. **Stands.**" — overstates the audit's filed evidence and misattributes to the minority a rationale they did not publish.**

**Suggested rewrites, in declining order of evidentiary strength:**

**Rewrite A (preferred, matches filed evidence exactly).** "St. Albert-Sturgeon: this is the one contested configuration where the minority and majority maps independently converge on the same two-district structure (St. Albert + St. Albert-Sturgeon, both within ±25%). The minority does not publish a per-district rationale for this pairing in Appendix E; the audit's own school-division and population-arithmetic checks find no cleaner alternative that satisfies both the population-deviation rule and the city/county school-catchment boundary without crossing a more load-bearing institutional line. **Stands.**"

**Rewrite B (preserves the punchier framing with disclosure).** "St. Albert-Sturgeon: the minority's two-district configuration (St. Albert + St. Albert-Sturgeon hybrid) is the only contested redraw the audit cannot improve on — both the minority map and the majority map independently arrive at this two-district structure, and no documented alternative in the audit's review satisfies both the ±25% rule and the city/county community-of-interest boundary simultaneously without splitting either St. Albert or Sturgeon County across an Edmonton hybrid. **Stands.**"

**Rewrite C (only if the MCMC re-run is performed before publication).** Substantively equivalent to the current public-report bullet, but with a methodology note documenting the ensemble-based counterfactual extraction. Required engineering: re-run the v0.8 ensemble with per-district serialization (~24h compute + 10GB output); query for St. Albert-area district structures; report the share of maps with each structure.

**Recommendation: adopt Rewrite A.** It removes the misattribution to the minority (who did not actually publish this rationale), preserves the underlying 'Stands' verdict, and acknowledges the convergence-of-maps as the load-bearing evidence rather than an unproven counterfactual non-existence.

The 'Stands' verdict itself is robust under all three rewrites. The substantive finding — that this is the configuration where the audit cannot substitute a cleaner alternative — is what makes the "six of seven" pattern asymmetric and non-trivial. The exact phrasing of the *reason* this configuration stands is what needs softening.

## Files

- This file: `analysis/methodology/v0_1_st_albert_sturgeon_constraint_search.md`.
- Cross-references: `analysis/methodology/v0_1_school_division_coherence.md` (St. Albert-area subsection); `analysis/methodology/v0_1_minority_rationales_validation.md` (St. Albert-Sturgeon not separately listed); `analysis/reports/v0_1_claim_significance_analysis.md` row 7; `report_academic.md` §5.9.6 Claim 7.
- Inputs used: `data/alberta_2021_csd_populations.csv`; `data/v0_1_minority_2026_populations.csv`; `data/v0_1_majority_2026_populations.csv`.
- *Not* used (because not feasible from filed data): `data/mcmc_checkpoints_250k_v0_8/chain*_samples.csv` — the ensemble checkpoints store only aggregate per-step metrics, not per-district assignments.

## Caveats

- The "no cleaner alternative" finding rests on the closed-form arithmetic and the side-by-side comparison of the two filed maps. It does not formally enumerate all configurations the ensemble produced. A formal enumeration requires re-running the ensemble.
- The St. Albert population of 68,232 is *just* under the ±25% ceiling (68,661). If StatsCan's 2026 inter-census estimate or the OSI population estimate the EBC used in 2025 differs by even 500 residents from the 2021 Census figure, a stand-alone St. Albert could fall on either side of the ceiling. The audit uses the 2021 Census figure throughout; a different population data source could change the verdict at the margin.
- The "school-catchment community of interest" assumption used here is that crossing a school-division boundary degrades community-of-interest coherence. This is the same assumption the audit applies in `v0_1_school_division_coherence.md` to all 21 minority hybrids. It is defensible but not the only possible community-of-interest dimension.
- The 1,000,000-map ensemble is at v0.8; the audit's pre-registration uses the v0.8 boundaries as the ground-truth reference, but the ensemble construction does not constrain the St. Albert-area on community-of-interest grounds (it constrains on contiguity, population-equality, and compactness). The ensemble can therefore produce many maps with implausible St. Albert configurations; the relevant counterfactual count would need a community-of-interest filter applied post-hoc.
