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
* **The Defense:** Valid attack; partially addressed but not fully resolved. The canonical ensemble uses a uniform ±25% deviation for all 89 EDs — it does not implement the §15(2) two-tier option. A two-tier constraint was attempted in `mcmc_ensemble.py` (`alberta_statutory_population_constraint`) but was disabled 2026-04-26 after pipeline debugging revealed the correct s15(2) interpretation (under-populated districts only) caused chain failures when the 2019 seed's pre-existing s15(2) EDs exceeded tolerance. The canonical run (`mcmc_ensemble_canonical.py`) uses the simpler uniform constraint throughout.
* **Residual defense:** The 3 s15(2) EDs in each real map are small, remote, and heavily UCP-leaning; they contribute a modest fraction of province-wide votes. The minority-majority asymmetry comparison is less sensitive to this gap than absolute percentile scores, because both maps invoke comparable s15(2) configurations. The uniform ±25% null is *stricter* than the legal possibility space, meaning the minority map must overcome a more constraining baseline to register as an outlier — the limitation is conservative in the direction of producing fewer false positives. See academic report §5.4 for the disclosed quantitative limitation.
* **EA Confirmation (2026-05-07):** Elections Alberta validated the audit's use of the 2021 Census DA baseline and statutory constraints as "reasonable and aligned with the Commission's process," though they could not provide independent population denominators.

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
* **The Defense:** Valid attack, fully addressed and resolved in the 1,010,000-plan canonical run.
* **Empirical refutation (2026-05-07, updated 2026-05-12):** The 1,010,000-plan canonical ensemble (`mcmc_ensemble_canonical.py`, 4 chains × 252,500 steps) was re-architected to generate overdispersed, purely random contiguous partitions for 3 of the 4 chains using GerryChain's `recursive_tree_part` algorithm. The chains successfully escaped the 2019 local minimum and converged on the true global phase space (GR92 R-hat 1.00179–1.01843; all pass GR92 threshold < 1.10). Against the 1M canonical ensemble on official Elections Alberta shapefiles: minority map Efficiency Gap p94.4, Mean-Median p99.98, Declination p1.21 (NDP-tail), seats@50/50 p99.99. Three of four partisan metrics individually flag above the 95th percentile; EG at p94.4 remains below the threshold and is not individually flagged. The Mahalanobis joint test (D = 5.72, p = 1.40×10⁻⁶) captures the joint extremity.

---

## Part 3: Attacks on the Partisan Metrics

### 3.1 The Uniform Swing Regional Collapse
* **The Vulnerability:** The headline `seats@50/50` metric assumes a Uniform Partisan Swing (UPS). 
* **The Attack:** "Alberta does not swing uniformly. A 5% provincial swing toward the NDP might mean a 10% swing in Calgary and a 0% swing in rural Alberta. The uniform swing creates a mathematical illusion."
* **The Defense:** Confirmed valid attack against UPS-only framing. When subjected to a Regional-Swing robustness check on the pre-canonical ensemble, the minority's extreme outlier status collapsed to p50.7. The pre-canonical §3 conclusion ("Lane 1 is officially demoted") was written on this basis.
* **Status (canonical, 2026-05-12):** Lane 1 is NOT demoted on the 1M canonical ensemble. The canonical run places the minority at MM p99.98, s50 p99.99, and Mahalanobis joint p = 1.40×10⁻⁶. The uniform-swing sensitivity is reported as a limitation (academic report §5.5), but Lane 1 contributes independently alongside Lane 2. Regional-swing recomputation against the canonical 1M ensemble is a blocker (see task list). Pre-canonical conclusion preserved for record. 

### 3.2 The "One-Metric Gerrymander" & Microtargeting (Efficiency Gap Immunity)

> **Canonical update (2026-05-12):** Pre-canonical values below are stale. Canonical 1M: EG p94.4 (unflagged), MM p99.98 (flagged), Decl p1.21 NDP-tail (flagged), s50 p99.99 (flagged). Three metrics individually flag; EG does not. Mahalanobis D = 5.72, p = 1.40×10⁻⁶. "One-metric" framing no longer applies. Pre-canonical text preserved for record.

* **The Vulnerability:** Against the pre-canonical ensemble, the minority map scored as within the normal range on the Efficiency Gap, Mean-Median, and Declination. It flagged as an outlier only on `seats@50/50`.
* **The Attack:** "A true gerrymander creates a massive efficiency gap. If the map passes the efficiency gap test, it's not a gerrymander. Furthermore, attempting to hold suburban tipping points with thin margins is a 'dummymander' that will collapse against the creators in a wave election."
* **The Defense:** In a rigid two-party system with massive geographic polarization (80-20 rural vs 80-20 urban), global metrics like the Efficiency Gap are mathematically numb. The natural packing of the province balances the global wasted-vote math. The minority map is a "Surgical Fortification"—it leaves the massive safe districts untouched and explicitly uses **microtargeting** to optimize the 5 suburban tipping-point districts. The Efficiency Gap is mathematically incapable of detecting this modern micro-targeting, whereas `seats@50/50` acts as a direct stress-test on the firewall. The "dummymander" critique is flawed because the minority map's strategy is defensive: it acts as a shock-absorbing firewall, heavily fortifying just enough suburban ridings to ensure a majority, rather than an over-extended greedy gerrymander.

### 3.3 Durability & Demographic Lockout (10-Year Trend)
* **The Speculation:** "Are the UCP trying to stack the deck to ensure a permanent lead as population grows on trend over the next ten years? Are these maps designed to lockout opposition permanently?"
* **The Test:** This speculation is addressed by incorporating a longitudinal demographic projection model into the audit. By applying 10-year projected population growth trends (specifically the rapid expansion of the Calgary-Edmonton suburban corridors) to the MCMC ensemble, we test whether the minority map's firewall gains or loses efficacy over the decennial cycle. 
* **The Defense:** The November 2026 Lunty Committee map evaluation will explicitly incorporate demographic swing tests. If the map is structured such that projected suburban growth systematically dilutes opposition vote share rather than augmenting it (a "demographic lockout"), the metric will flag. The audit limits its conclusion to measuring structural *effects* rather than establishing *intent*, rendering the finding academically defensible regardless of motive.

---

## Part 4: Lane 1 and Lane 2 — Independent, Converging Contributions

The Parts 1–3 attacks identify real limitations in specific statistical claims. They do not undermine the audit's headline conclusions because those conclusions rest on **two independent lines of evidence** — one statistical, one structural — that converge on the same map, the same direction, and the same communities.

### Lane 1 (statistical) — canonical status

The 1,010,000-plan canonical ensemble reinstates all four partisan-fairness flags. Against official Elections Alberta shapefiles: EG p94.4 (below the 95th-percentile individual threshold, but contributes to joint test), MM p99.98 (flagged), Declination p1.21 NDP-tail (flagged), seats@50/50 p99.99 (flagged). The Mahalanobis joint test (D = 5.72, p = 1.40×10⁻⁶) captures the joint extremity; the Fisher combination with Ch2 SZAT (p = 0.0024) yields p = 6.87×10⁻⁸.

The "Lane 1 officially demoted" conclusion in §3.1 was written on the pre-canonical DPG-era ensemble, where a regional-swing robustness check collapsed the minority's outlier status. That pre-canonical result does not survive the canonical run. The uniform-swing sensitivity is documented as a disclosed limitation (§5.5 of the academic report) but is not load-bearing against the canonical 1M finding — three metrics individually flag above the 95th percentile without any swing-model assumption. Lane 1 is not demoted; both lanes contribute independently.

### Lane 2 (structural) — surviving canonical findings

The statistical confounds in Parts 1–3 are ensemble-specific and vote-data-specific. They have **zero impact** on the following four Lane 2 findings, which require no MCMC ensemble, no vote data, no swing assumptions, and no incumbent geography:

* **Population spread (MAD).** Minority Population MAD = 4,707; majority = 3,180 — a 48% wider dispersion. Derived directly from the commission's own published per-ED population tables. No statistical model involved.
* **Airdrie fragmentation.** Minority splits the City of Airdrie into 4 electoral divisions; majority uses 2. An immutable geometric count, applied symmetrically to both maps.
* **Chair-flagged anomalies.** The commission's own chair flagged 3 minority boundaries as geometrically anomalous (Rocky Mountain House–Banff Park extension; Calgary-Nolan Hill–Cochrane lasso; Olds-Three Hills-Didsbury → N Airdrie community capture). Zero majority boundaries were flagged. This finding derives from the chair's own majority report and cannot be attacked without attacking the commission's internal process.
* **NW Calgary population asymmetry.** The minority's NW Calgary geographic zone averages 11.5% above provincial population mean; the majority's same zone shows 2.8%. Measured from commission-published per-ED population targets, not from vote data.

### The anchoring finding is retracted

The discovery that the minority map dropped Municipal Anchoring from the historical norm of 75.2% down to 14.5% **[RETRACTED — DPG-era value; did not survive canonical recomputation]** was previously cited as the Lane 2 anchor. On official Elections Alberta shapefiles, both maps fall within the 70–85% Canadian comparator norm (majority 80.0%, minority 72.0%, 2019 enacted 75.2%). The "4.9× below norm" characterisation is retracted per the failed-findings policy; see academic report §5.8.5 and public report Documented Corrections. The four surviving Lane 2 findings above do not depend on anchoring.

### Summary

The Parts 1–3 statistical confounds affect Lane 1 magnitude claims at the margins; they do not reach Lane 1's canonical joint p-value (p = 6.87×10⁻⁸) and they do not reach any Lane 2 finding. Four Lane 2 structural findings survive canonical recomputation: population MAD 48% wider, Airdrie 4-way split, 3 chair-flagged anomalies, and NW Calgary population asymmetry. All four pre-registered tests fire for the minority; none fire for the majority. This structural pattern is not affected by any confound in Parts 1–3.
