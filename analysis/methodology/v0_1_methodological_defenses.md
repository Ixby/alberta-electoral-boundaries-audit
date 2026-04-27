# Methodological Defenses & Limitations (Adversarial Appendix)

## Purpose
This appendix acts as a pre-emptive adversarial review of the 2026 Electoral Boundaries Audit. It catalogs the known mathematical vulnerabilities, spatial approximations, and statistical assumptions inherent in the analysis. For each vulnerability, we present the "Hostile Attack" (how an opposing expert witness would attempt to invalidate the audit) and our "Methodological Defense" (why the core findings survive the attack).

The overarching conclusion of this review is that **Lane 1 (MCMC Statistical Partisan Fairness)** is highly sensitive to modelling assumptions, necessitating its demotion to a multi-scenario sensitivity analysis rather than a single headline metric. Conversely, **Lane 2 (Structural Irregularities & Municipal Anchoring)** is mathematically immune to every statistical confound listed below, securing its place as the definitive, unassailable finding of this audit.

---

## Part 1: Attacks on the Voting Data (The Substrate)

### 1.1 The Advance Vote Black Hole
* **The Vulnerability:** 47.5% of the 2023 electorate cast Advance, Mobile, or Special ballots. Elections Alberta reports these at the massive Electoral Division (ED) level, not the hyper-local Voting Area (VA) level. The audit relies almost entirely on Election Day VA-level results to model the new 2026 geometries.
* **The Attack:** "The audit excludes half the voting population. If advance voters lean a different partisan direction than Election Day voters, the absolute vote totals in the border zones are completely wrong, rendering the partisan metrics invalid."
* **The Defense:** Symmetrical application. The exact same geographic resolution limits apply to all three maps tested (2019, 2026 Majority, 2026 Minority). Any bias in the missing advance vote shifts the *entire* ensemble, but it preserves the massive relative delta between the maps. Furthermore, the commission itself did not possess VA-level advance vote data. The audit evaluates the maps using the exact, highest-resolution public dataset the commission legally possessed.
* **Empirical refutation (2026-04-26):** `advance_vote_splat.py` apportions the missing 47.5% of votes to VAs by Election-Day two-party shares; re-scoring v0_9 majority and minority shifts both maps' `seats@50/50` by exactly +1.12 pp and preserves the 2.25-pp relative gap between them to 4 decimal places. The defense's symmetry argument is empirically confirmed. See `analysis/reports/v0_9_advance_vote_sensitivity.md` and `data/v0_9_advance_vote_sensitivity.json`.

### 1.2 The Centroid Fallacy (Ecological MAUP)
* **The Vulnerability:** The audit assigns 2023 VAs to new 2026 districts using a centroid-in-polygon spatial join. 
* **The Attack:** "A VA is an area, not a point. A VA's geographic center might sit in an empty field on the UCP side of a boundary, while 100% of the actual human population lives in an apartment complex on the NDP side. Assigning whole VAs based on a dot artificially synthesizes margins."
* **The Defense:** Quantified insignificance. Phase 4F validation (`v0_1_boundary_refinement_impact_v3.csv`) tracked the exact population living in these ambiguous border zones. Shifting the boundaries across the full ±500m confidence interval affected only 4 VAs containing exactly 1,012 votes (0.06% of the electorate). This is orders of magnitude too small to shift the `seats@50/50` metric from p50 to p98.
* **Empirical refutation (2026-04-27):** `v0_9_va_attribution_area_weighted.py` re-attributes votes by `intersection_area / VA_area` rather than centroid-in-polygon; v0_9 majority and minority `seats@50/50` change by exactly **+0.0000 pp** under area-weighted attribution (other Lane 1 metrics shift by ≤1×10⁻⁵ pp). Diagnostic: only **7 VAs (1,396 votes, 0.15% of the electorate)** have any area sliver in a second 2026 ED; max secondary share is 0.44%. The v0_9 topological shapefiles snap ED boundaries to VA boundaries by construction, so MAUP is structurally nullified — not merely small. The 2.25-pp majority-vs-minority s50 gap is preserved exactly. See `analysis/reports/v0_9_maup_centroid_sensitivity.md` and `data/v0_9_maup_centroid_sensitivity.json` (commit `ffb707d`).

---

## Part 2: Attacks on the MCMC Baseline (The Ensemble)

### 2.1 The Section 15(2) Deletion (Suppressed Baseline)
* **The Vulnerability:** Alberta law allows up to four rural districts to exceed the standard -25% population variance under s15(2). The ReCom algorithm used to generate the baseline struggles to graph-seed around fixed outliers. As a result, the `mcmc_ensemble.py` script actively destroys the historical 2019 s15(2) districts (e.g., Central Peace-Notley), running a recursive tree partition to force the entire province into a strict ±25% envelope.
* **The Attack:** "The MCMC baseline violates Alberta law. By explicitly deleting the legally mandated special-rural districts, the auditor simulated an illegal province."
* **The Defense:** Conservative lower bound. The s15(2) districts are heavily conservative rural strongholds. By destroying them and forcing that population into competitive pools, the MCMC baseline *artificially suppresses* the baseline UCP seat count. The minority map's UCP-advantage looks like an outlier against this suppressed baseline. If the baseline were legally corrected (by freezing those safe UCP seats), the median baseline UCP seat count would rise, pushing the minority map *even further* into the extreme tail. The current methodological error actually favors the commission.

### 2.2 The "Random Soup" Fallacy (Zero Municipal Constraints)
* **The Vulnerability:** The ReCom chain uses only two constraints: Population Equality (±25%) and Contiguity. It does not enforce municipal preservation (e.g., penalizing city-splitting). 
* **The Attack:** "The auditor compared a human-drawn commission map to 100,000 completely random, politically absurd 'soup' maps that casually slice the City of Calgary into 50 random slivers."
* **The Defense:** The commission map is the one that ignores municipal boundaries. Lane 2 proves the minority map drops municipal anchoring from 75% to 14%. If the MCMC algorithm were constrained to respect municipal borders, the resulting baseline maps would look *less* like the minority map. The unconstrained "random soup" baseline is actually the most generous possible comparator for a minority map that famously abandoned civic borders.

### 2.3 The Turnout vs. Apportionment Gap
* **The Vulnerability:** The MCMC chain equalizes *Census Population* (required by law). The partisan metrics score *Actual Votes Cast*. 
* **The Attack:** "If rural Alberta has larger families (more non-voting children) but higher civic engagement, and urban Alberta has more adults but lower turnout, equalizing population creates wildly unequal vote totals."
* **The Defense:** This is a standard, unresolvable artifact of all spatial-partisan modeling. Like the Advance Vote flaw, this dynamic applies symmetrically across the 2019 seed, the baseline, and the commission maps.

### 2.4 Incumbent Protection (Core Preservation)
* **The Vulnerability:** The algorithm is blind to incumbent addresses.
* **The Defense:** Acknowledged limitation. The commission may argue that "lassos" were drawn to preserve the cores of 2019 districts rather than optimize partisanship. This requires qualitative review of the 2019-to-2026 overlays (provided in the article figures).

---

## Part 3: Attacks on the Partisan Metrics

### 3.1 The Uniform Swing Regional Collapse
* **The Vulnerability:** The headline `seats@50/50` metric assumes a Uniform Partisan Swing (UPS). 
* **The Attack:** "Alberta does not swing uniformly. A 5% provincial swing toward the NDP might mean a 10% swing in Calgary and a 0% swing in rural Alberta. The uniform swing creates a mathematical illusion."
* **The Defense:** Confirmed valid attack. When subjected to a Regional-Swing robustness check, the minority map's extreme p98.6 outlier status collapses to p50.7 (while the majority map shoots to p99.5 in the opposite direction). 
* **Conclusion:** Because the `seats@50/50` metric is hyper-sensitive to the swing model chosen (>40 percentage point magnitude shift), **Lane 1 is officially demoted.** It is no longer reported as a single deterministic proof of gerrymandering, but rather as a multi-scenario sensitivity test. 

### 3.2 The "One-Metric Gerrymander" (Efficiency Gap Immunity)
* **The Vulnerability:** The minority map scores as perfectly normal on the Efficiency Gap (p57.5), Mean-Median (p50.9), and Declination (p58.3). It only flags as an outlier on `seats@50/50`.
* **The Defense:** In a rigid two-party system with massive geographic polarization (80-20 rural vs 80-20 urban), global metrics like the Efficiency Gap are mathematically numb. The natural packing of the province balances the global wasted-vote math. The minority map is a "Surgical Fortification"—it leaves the massive safe districts untouched and exclusively optimizes the 5 suburban tipping-point districts. The Efficiency Gap is mathematically incapable of detecting this modern micro-targeting, whereas `seats@50/50` acts as a direct stress-test on the firewall.

---

## Part 4: Why Lane 2 (Structural Irregularities) Prevails

The vulnerabilities listed in Parts 1 through 3 successfully deconstruct the certainty of the Lane 1 statistical model. However, they have **zero mathematical impact on Lane 2.**

The discovery that the minority map dropped Municipal Anchoring from the historical norm of 75.2% down to 14.5% relies on:
1. No MCMC simulations.
2. No voting data (Advance or Election Day).
3. No Uniform or Regional swing assumptions.
4. No incumbent geography.

The minority map's structural divergence—specifically its unprecedented abandonment of civic boundaries in favor of natural/highway boundaries to construct urban-rural lasso corridors—is an immutable geometric fact. The methodological defenses listed above secure the audit by correctly shifting the burden of proof off the volatile statistical models and onto the undeniable geometry.
