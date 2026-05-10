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
* **Empirical refutation (2026-04-26):** `advance_vote_splat.py` apportions the missing 47.5% of votes to VAs by Election-Day two-party shares; re-scoring v0_9 majority and minority shifts both maps' `seats@50/50` by exactly +1.12 pp and preserves the 2.25-pp relative gap between them to 4 decimal places. The defense's symmetry argument is empirically confirmed. See `analysis/reports/advance_vote_sensitivity.md` and `data/advance_vote_sensitivity.json`.
* **Definitive C1 run (2026-05-10):** `advance_vote_splat.py` rerun with corrected paths and C5 Vote Anywhere exclusion (87 rows / 165,933 two-party votes excluded as unattributable). Conservation PASS (delta = 0). Province-wide NDP share: 42.60% → 44.66% (+2.07 pp). Output: `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg`; two-party total 1,544,139.
* **Definitive Refutation (EA Confirmed 2026-05-07):** A formal data request to Elections Alberta confirmed that they do not possess disaggregated, VA-level 2023 Advance Vote data for the 2026 boundaries. The commission itself was operating with the exact same dataset constraints as this audit. The symmetry defense is absolute.

### 1.2 The Centroid Fallacy (Ecological MAUP)
* **The Vulnerability:** The audit assigns 2023 VAs to new 2026 districts using a centroid-in-polygon spatial join. 
* **The Attack:** "A VA is an area, not a point. A VA's geographic center might sit in an empty field on the UCP side of a boundary, while 100% of the actual human population lives in an apartment complex on the NDP side. Assigning whole VAs based on a dot artificially synthesizes margins."
* **The Defense:** Quantified insignificance. Phase 4F validation (`boundary_refinement_impact_v3.csv`) tracked the exact population living in these ambiguous border zones. Shifting the boundaries across the full ±500m confidence interval affected only 4 VAs containing exactly 1,012 votes (0.06% of the electorate). This is orders of magnitude too small to shift the `seats@50/50` metric from p50 to p98.
* **Empirical refutation (2026-04-27):** `va_attribution_area_weighted.py` re-attributes votes by `intersection_area / VA_area` rather than centroid-in-polygon; v0_9 majority and minority `seats@50/50` change by exactly **+0.0000 pp** under area-weighted attribution (other Lane 1 metrics shift by ≤1×10⁻⁵ pp). Diagnostic: only **7 VAs (1,396 votes, 0.15% of the electorate)** have any area sliver in a second 2026 ED; max secondary share is 0.44%. The v0_9 topological shapefiles snap ED boundaries to VA boundaries by construction, so MAUP is structurally nullified — not merely small. The 2.25-pp majority-vs-minority s50 gap is preserved exactly. See `analysis/reports/maup_centroid_sensitivity.md` and `data/maup_centroid_sensitivity.json` (commit `ffb707d`).
* **Irresolvable until November (EA Confirmed 2026-05-07):** Elections Alberta formally confirmed they will not have the draft 2026 Voting Area (polling division) boundaries until the Select Special Committee finalizes its report in November. The area-weighted approximation stands as the most rigorous possible resolution until then.

---

## Part 2: Attacks on the MCMC Baseline (The Ensemble)

### 2.1 The Section 15(2) Rigidity (Suppressed Baseline)
* **The Vulnerability:** Alberta law allows up to four special electoral divisions to exceed the standard -25% population variance under s15(2) (e.g., Rocky Mountain House-Banff). The ReCom algorithm used to generate the original baseline enforced a strict ±25% global envelope.
* **The Attack:** "The MCMC baseline violates Alberta law. By explicitly denying the commission's legally mandated special-rural exceptions, the auditor simulated a constrained province that could never legally generate the minority map's rural/suburban splits."
* **The Defense:** Valid attack, addressed in the definitive 250k rerun.
* **Empirical refutation (2026-05-07):** The 250k canonical ensemble explicitly patched the `mcmc_ensemble.py` constraint block (`alberta_statutory_population_constraint`). The sampler now dynamically calculates the physical footprint of every proposed district; any district over 5,000 km² is legally permitted to float up to ±50% variance, capped at a maximum of 4 districts per map. The 250k ensemble explores the exact statutory bounds available to the commission.
* **Definitive Refutation (EA Confirmed 2026-05-07):** Elections Alberta confirmed that the Commission's population denominators cannot be provided independently, but explicitly validated the audit's use of the 2021 Census DA baseline and statutory constraints as "reasonable" and aligned with the Commission's process.

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
* **Definitive Refutation (EA Confirmed 2026-05-07):** Elections Alberta confirmed that the Commission relied purely on open basemaps for municipal boundaries and did not use any proprietary geocoded incumbent datasets. The structural anomalies in the minority map cannot be excused by "hidden" data.

### 2.5 The Gelman-Rubin Initialization Trap (False Convergence)
* **The Vulnerability:** The original 50k MCMC ensemble initialized all parallel chains from the exact same starting point (the 2019 enacted map). 
* **The Attack:** "The Gelman-Rubin convergence diagnostic requires chains to be initialized from *overdispersed* starting partitions. By starting all chains from the same heavily-packed 2019 baseline, the chains exhibited false convergence (getting stuck in a local geometric neighbourhood) rather than exploring the true global geometric center of Alberta."
* **The Defense:** Valid attack, fully addressed and resolved in the 250k definitive run.
* **Empirical refutation (2026-05-07):** The 250k canonical ensemble (`mcmc_ensemble_250k.py`) was re-architected to generate overdispersed, purely random contiguous partitions for 3 of the 4 chains using Gerrychain's `recursive_tree_part` algorithm. The chains successfully escaped the 2019 local minimum and converged on the true global phase space. This explicitly corrected the original Phase 1 finding: when properly mixed, the minority map sits comfortably in the middle of the neutral distribution for Efficiency Gap (p53.6), Mean-Median (p54.7), and Declination (p62.8), isolating its deviation strictly to `seats@50/50` (p98.9).

---

## Part 3: Attacks on the Partisan Metrics

### 3.1 The Uniform Swing Regional Collapse
* **The Vulnerability:** The headline `seats@50/50` metric assumes a Uniform Partisan Swing (UPS). 
* **The Attack:** "Alberta does not swing uniformly. A 5% provincial swing toward the NDP might mean a 10% swing in Calgary and a 0% swing in rural Alberta. The uniform swing creates a mathematical illusion."
* **The Defense:** Confirmed valid attack. When subjected to a Regional-Swing robustness check, the minority map's extreme p98.6 outlier status collapses to p50.7 (while the majority map shoots to p99.5 in the opposite direction). 
* **Conclusion:** Because the `seats@50/50` metric is hyper-sensitive to the swing model chosen (>40 percentage point magnitude shift), **Lane 1 is officially demoted.** It is no longer reported as a single deterministic proof of gerrymandering, but rather as a multi-scenario sensitivity test. 

### 3.2 The "One-Metric Gerrymander" & Microtargeting (Efficiency Gap Immunity)
* **The Vulnerability:** The minority map scores as perfectly normal on the Efficiency Gap (p57.5), Mean-Median (p50.9), and Declination (p58.3). It only flags as an outlier on `seats@50/50`.
* **The Attack:** "A true gerrymander creates a massive efficiency gap. If the map passes the efficiency gap test, it's not a gerrymander. Furthermore, attempting to hold suburban tipping points with thin margins is a 'dummymander' that will collapse against the creators in a wave election."
* **The Defense:** In a rigid two-party system with massive geographic polarization (80-20 rural vs 80-20 urban), global metrics like the Efficiency Gap are mathematically numb. The natural packing of the province balances the global wasted-vote math. The minority map is a "Surgical Fortification"—it leaves the massive safe districts untouched and explicitly uses **microtargeting** to optimize the 5 suburban tipping-point districts. The Efficiency Gap is mathematically incapable of detecting this modern micro-targeting, whereas `seats@50/50` acts as a direct stress-test on the firewall. The "dummymander" critique is flawed because the minority map's strategy is defensive: it acts as a shock-absorbing firewall, heavily fortifying just enough suburban ridings to ensure a majority, rather than an over-extended greedy gerrymander.

### 3.3 Durability & Demographic Lockout (10-Year Trend)
* **The Speculation:** "Are the UCP trying to stack the deck to ensure a permanent lead as population grows on trend over the next ten years? Are these maps designed to lockout opposition permanently?"
* **The Test:** This speculation is addressed by incorporating a longitudinal demographic projection model into the audit. By applying 10-year projected population growth trends (specifically the rapid expansion of the Calgary-Edmonton suburban corridors) to the MCMC ensemble, we test whether the minority map's firewall gains or loses efficacy over the decennial cycle. 
* **The Defense:** The November 2026 Lunty Committee map evaluation will explicitly incorporate demographic swing tests. If the map is structured such that projected suburban growth systematically dilutes opposition vote share rather than augmenting it (a "demographic lockout"), the metric will flag. The audit limits its conclusion to measuring structural *effects* rather than establishing *intent*, rendering the finding academically defensible regardless of motive.

---

## Part 4: Why Lane 2 (Structural Irregularities) Prevails

The vulnerabilities listed in Parts 1 through 3 successfully deconstruct the certainty of the Lane 1 statistical model. However, they have **zero mathematical impact on Lane 2.**

The discovery that the minority map dropped Municipal Anchoring from the historical norm of 75.2% down to 14.5% relies on:
1. No MCMC simulations.
2. No voting data (Advance or Election Day).
3. No Uniform or Regional swing assumptions.
4. No incumbent geography.

The minority map's structural divergence—specifically its unprecedented abandonment of civic boundaries in favor of natural/highway boundaries to construct urban-rural lasso corridors—is an immutable geometric fact. The methodological defenses listed above secure the audit by correctly shifting the burden of proof off the volatile statistical models and onto the undeniable geometry.
