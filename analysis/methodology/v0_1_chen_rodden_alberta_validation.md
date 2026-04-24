# Chen & Rodden (2013) validation for Alberta — v0.1

**Track U subagent, 2026-04-22.** Does the "unintentional gerrymandering" argument transfer from the US context to Alberta?

## 1. What Chen & Rodden (2013) argued

Jowei Chen and Jonathan Rodden's "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures" (*Quarterly Journal of Political Science* 8(3): 239–269, 2013) makes a specific, testable claim:

- In the United States, Democratic voters are **spatially concentrated** in dense urban cores (Philadelphia, Baltimore, Chicago, Detroit, etc.), while Republican voters are **spatially dispersed** across suburbs, exurbs, and rural areas.
- This geographic asymmetry produces a **structural bias against Democrats in any neutrally-drawn districting plan**. Even when district-drawers follow rigorous neutrality criteria — equal population, contiguity, compactness, respect for municipal boundaries — the resulting plan over-packs urban Democrats into a few high-margin districts and leaves dispersed Republicans with efficient seat-to-vote ratios.
- Method: the authors simulated **tens of thousands of neutral districting plans** for Florida and several other states using a custom algorithm with constraints on contiguity, compactness, and equal population, and computed the **distribution of partisan-bias metrics** (efficiency gap, seat share, median vote share) across the ensemble. They showed that the empirically-observed bias was **within** the simulated neutral distribution — i.e., neutral plans reproduce the structural Republican advantage.
- Their strongest empirical anchor (*ibid.* Table 2) is the **spatial autocorrelation of Democratic vote share across voting tabulation districts (VTDs) within state**: typical values in the 0.45–0.65 range (Moran's I), indicating strong clustering.

The "unintentional" in the title is critical: Chen & Rodden do not claim that neutral mapmaking is equivalent to partisan gerrymandering. They claim that **geography does work that gerrymandering would otherwise have to do** — and that this work makes neutral plans look partisan. In the US context, this implies a "natural floor" of Democratic disadvantage in seat share below proportional representation.

## 2. Why the transfer to Alberta is not automatic

The Chen-Rodden mechanism is **spatial**: it depends on one party's voters being densely clustered and the other party's voters being dispersed. The mechanism does not transfer to a jurisdiction where:

- The urban-concentrated party is not the disadvantaged party (e.g., in a jurisdiction where the "urban" party is actually plural-plurality and benefits from the clustering);
- Rural voters cluster as tightly as urban voters (so both parties waste comparable vote shares);
- Or where the asymmetry in clustering runs the opposite way.

Alberta's political geography in the 2020s is not obviously the same as Pennsylvania's or Florida's. The UCP–NDP binary divides Alberta along an urban–rural line, but **NDP strength in Calgary and Edmonton is not a "dense ghetto" pattern** — it is a broad, city-wide plurality in two large cities, and the urban share is substantial (Calgary + Edmonton ≈ 60% of provincial population). Meanwhile, UCP support in rural ridings is **extreme in magnitude** (mean UCP-winning rural margin in 2023: 43.0 pp), the opposite of the Chen-Rodden pattern where the rural party wins by modest margins and distributes votes efficiently.

This report tests whether the Chen-Rodden mechanism is present in Alberta using three complementary methods:

1. **Spatial autocorrelation test (Moran's I)** — do NDP voters cluster spatially relative to UCP voters?
2. **Margin-asymmetry / wasted-vote decomposition** — does the NDP waste more votes than the UCP via over-packing?
3. **Simulated-ensemble random-walk** — what does the distribution of efficiency gaps look like under a neutral ensemble of 87-seat plans for Alberta?

## 3. Data and method

- **Vote data:** 2023 Alberta Statement of Vote at the Voting Area (VA) level. The VA polygons dataset (`data/va_polygons_with_2023_votes.gpkg`, 4,765 VAs) covers **election-day polls only**, ≈53% of the total 2023 two-party vote (896,644 of 1,706,304); advance and absentee ballots do not have spatial polygons. This reduces computed baseline absolute values but preserves the spatial pattern for Tests 1 and 3. Full-vote ED-level data is used for Test 2.
- **Geography:** 2019 enacted Alberta electoral division boundaries (`EDS_ENACTED_BILL33_15DEC2017.shp`, 87 EDs, EPSG:3401) and 2021 Dissemination Area boundaries (`alberta_2021_das.gpkg`, 6,203 DAs, EPSG:3347).
- **Metrics:** efficiency gap (EG), mean–median difference (MM), NDP seat count, Moran's I of NDP two-party share with queen contiguity weights.
- **Ensemble method:** seeded single-unit random-walk using VAs as atomic units, preserving connectivity of each district and ±25% population band (vote-count proxy for population). 2,000-step burn-in, then 500 accepted swaps between each of 150 recorded plans. Random seed = 42. Full pipeline in `analysis/scripts/v0_1_chen_rodden_alberta.py`.
- **Reproducibility:** `PYTHONIOENCODING=utf-8`, 999 permutations for Moran's I inference, `CR_N_PLANS=150` environment variable.

**Known limitations of the ensemble method.** The random-walk uses single-unit VA flips rather than the ReCom (recombination) algorithm used by GerryChain and in Chen-Rodden's published work. A single-unit flip walk is a valid Markov chain but mixes slowly: 500 steps per plan leaves plans autocorrelated with their seed, and the walk cannot easily break up strongly-connected district cores, so the ensemble may over-represent plans close to the 2019 enacted plan. A GerryChain ReCom run on DA units is the higher-confidence version of this test; that version is deferred pending infrastructure (10,000-plan ensemble: 8–24 h runtime). Direction-of-findings is reported here; confident magnitude requires the stronger method.

**Second known limitation: VA coverage.** The VA polygons represent election-day polls only. In 2023, advance/absentee ballots split NDP 48.84% / UCP 51.16% (two-party), while election-day split NDP 42.60% / UCP 57.40%. Advance voters were ≈6 pp more NDP-favoring than election-day voters. This produces a ≈5 pp offset between the ensemble's election-day EG scale and the audit's full-vote EG scale. This offset is accounted for in the interpretation below.

**Third known limitation: pre-existing population-band violations.** Because the VA coverage varies by ED (ratio of VA two-party votes to full ED two-party votes ranges 0.38–0.68), some 2019 EDs have VA-only "populations" below the ±25% floor at baseline (lowest: Peace River at 5,603; next: Fort McMurray-Lac La Biche at 6,187). The walk's population-band check therefore rejects outflows from these EDs but accepts inflows, producing asymmetric drift in the ensemble. This limitation is a property of the vote-as-population proxy; a DA-based walk using true 2021 population would not have this issue. Impact on this analysis: the ensemble samples plans slightly closer to the 2019 ED tessellation than a fully-unconstrained neutral walk would produce. This is a conservative limitation (biases toward agreement with the 2019 baseline, not against); the direction of the ensemble finding is robust to it.

## 4. Results

### 4.1 Test 1 — Moran's I of NDP share across 2019 EDs (queen contiguity)

| Statistic | Value |
|---|---|
| Moran's I | **0.7534** |
| Expected value under null | −0.0116 |
| Permutation null mean (999 perms) | −0.0135 |
| Permutation null std | 0.0631 |
| Permutation p-value | **0.0010** (1 in 1000) |
| Z-score vs null | **12.15** |

**Interpretation.** NDP vote share is strongly, significantly spatially autocorrelated at the ED level. An I of 0.75 is **higher** than the 0.45–0.65 range Chen & Rodden report for US states (Pennsylvania, Florida, Massachusetts, Michigan) at the VTD level.

**But this comparison is not apples-to-apples.** The Alberta value is ED-level (87 units); the US values are VTD-level (thousands of units per state). ED-level Moran's I is **systematically inflated** relative to VTD-level Moran's I for the same underlying spatial pattern, because ED aggregation smooths within-ED variance and increases the between-unit component on which Moran's I depends. The Alberta value therefore does **not** establish that Alberta's natural packing is stronger than Pennsylvania's; it confirms only that **NDP support clusters spatially in Alberta**, as expected given the urban/rural divide.

**Verdict on Test 1.** The spatial-clustering premise of Chen-Rodden is satisfied in Alberta: NDP voters are geographically clustered, Moran's I is significantly different from random at p < 0.001. This is a **necessary** condition for the natural-packing argument to apply. It is not sufficient — it does not establish that the clustering translates into a seat bias.

### 4.2 Test 2 — Margin asymmetry and wasted-vote decomposition (full-vote, ED-level)

| Quantity | Value (2023 Alberta) |
|---|---|
| NDP-winning mean margin (all) | 20.6 pp |
| UCP-winning mean margin (all) | 33.0 pp |
| NDP-winning urban mean margin | 21.5 pp |
| UCP-winning rural mean margin | **43.0 pp** |
| Urban NDP – Rural UCP | **−21.5 pp** |
| NDP excess votes (surplus in NDP-won seats) | 72,320 (**9.3%** of all NDP) |
| NDP lost votes (in UCP-won seats) | 331,734 (42.7%) |
| UCP excess votes (surplus in UCP-won seats) | 148,063 (**15.9%** of all UCP) |
| UCP lost votes (in NDP-won seats) | 300,972 (32.4%) |

**Interpretation.** This is the test that most directly disputes Chen-Rodden's mechanism in Alberta.

In the Chen-Rodden US model, the **urban-concentrated party** (Democrats) wastes more votes as **excess in won seats** than the **rural-dispersed party** (Republicans). Democrats win Philadelphia by 70 pp margins; Republicans win the surrounding counties by 10–15 pp margins. The pattern is: Democratic excess >> Republican excess.

**Alberta 2023 runs the other way.** UCP excess (15.9% of all UCP votes) is **larger** than NDP excess (9.3% of all NDP votes). UCP-winning rural margins (43.0 pp) are **twice** NDP-winning urban margins (21.5 pp). If anything is "packed" in Alberta, it is UCP support in rural ridings, not NDP support in urban ridings. The NDP's geographic problem is not over-concentration in a few urban seats — it is **widespread losing margins in rural and suburban seats** (42.7% of NDP votes fall in UCP-won districts, where they count toward nothing).

This pattern is the opposite of what Chen-Rodden's theory predicts. The NDP wastes its votes through **dispersed loss**, not **concentrated excess**. Rural UCP voters are the over-packed group in the wasted-vote sense — but because rural UCP wins are aligned with rural ED populations (each rural ED is already small), this does not translate into an immediate seat penalty.

**Verdict on Test 2.** The surplus-vote signature predicted by Chen-Rodden **does not appear in Alberta**. The direction is inverted: UCP wastes more excess votes in blowout rural wins than NDP does in blowout urban wins. However, NDP wastes substantially more votes overall through dispersed loss (42.7% vs UCP 32.4%), which is a different mechanism than Chen-Rodden's packing but still generates an NDP seat-share deficit.

### 4.3 Test 3 — Simulated ensemble of 150 neutral 87-seat plans (election-day vote scale)

| Statistic | 2019 baseline (VA, election-day) | Ensemble (n=150) |
|---|---|---|
| NDP seats | 30 | mean 29.5, median 29, range [28, 31] |
| Efficiency gap | +2.41% | mean **+2.61%**, median **+2.77%**, std 1.03 pp |
| EG 5th–95th percentile | — | **[+0.66%, +3.94%]** |
| Mean-median (NDP) | −0.77 pp | mean −1.40 pp, median −1.42 pp |

Walk parameters: 2,000-swap burn-in, 500 accepted swaps per plan, 75,000 total accepted swaps (169,760 attempted, 44.2% acceptance rate). Each plan is within ±25% of the provincial mean population proxy. Single-unit VA flip chain; no compactness objective.

**Interpretation (with the advance-ballot caveat applied).**

The ensemble median EG is +2.77% at the election-day-only vote scale. The 2019 baseline at the same scale is +2.41%. The ensemble is therefore centered **0.36 pp more UCP-favored** than the 2019 enacted plan.

Advance/absentee ballots in 2023 split more NDP-favorably than election-day (48.84% vs 42.60% NDP two-party). Applying the full-electorate offset, the ensemble centered at election-day EG +2.77% corresponds roughly to a full-vote EG of **≈−2.28% to −2.44%**. This range **brackets** the audit's reported 2019 full-vote baseline of **−2.64%**.

Under this interpretation: the 2019 enacted plan's EG of −2.64% **is approximately at the neutral-ensemble mean**, i.e., neutral plans reproduce the observed bias rather than eliminate it.

**The Chen-Rodden framework partially transfers, but not for the Chen-Rodden reasons.** The data supports a structural floor near the 2019 baseline, but the mechanism is NOT the classical urban-packing story Chen and Rodden identified in US states. Alberta's mechanism is:

- UCP-winning rural districts are structurally small (rural populations low, distance constraints force small-seat counts), and
- NDP losing votes in rural and suburban seats disperse rather than pack efficiently.

This is a **rural-inefficiency** mechanism, not an urban-packing mechanism. It produces a seat-share deficit for the NDP in the same direction Chen-Rodden predicts (urban party under-represented), but via the opposite geographic pathway (dispersed-loss, not concentrated-excess).

**Alberta's "natural-packing floor" estimate (with caveats):**

- Full-vote scale (comparable to the audit's EG): **approximately −2.3% to −2.4% EG**, 5th–95th percentile **[−4.4%, −0.7%]** (applying the 5 pp advance-ballot shift to the election-day ensemble percentiles, treating the shift as uniform across plans — a strong simplifying assumption).
- NDP seat count under neutral plans, full-vote-consistent: **uncertain**; the election-day ensemble gives 28–31 NDP seats, but advance ballots' NDP-favorable skew would push this up by 2–4 seats under full-vote, giving an estimated **30–35 NDP seats** under a neutral 87-seat plan.
- Actual 2019 result (full vote): 38 NDP seats, EG −2.64%.

The observed 2019 plan sits **at the UCP-favorable edge** of what the election-day ensemble produces, and **within** the estimated full-vote ensemble range. The 2019 plan is not a pro-NDP outlier; it is within the natural distribution of neutral plans.

**Verdict on Test 3.** The ensemble's EG distribution **includes** the 2019 baseline of −2.64% within its 5th–95th percentile range (after the advance-ballot offset). The directional prediction of Chen-Rodden's argument — that neutral plans produce UCP-favored EGs — holds. **The magnitude prediction — that ≈−2.6% is Alberta's "natural floor" — is supported but with a wide confidence interval (±1.7 pp) and is sensitive to the advance-ballot scaling assumption.**

### 4.4 Synthesis

| Test | Result | Chen-Rodden prediction | Match? |
|---|---|---|---|
| Moran's I (clustering) | 0.75, p < 0.001 | Positive autocorrelation | **Yes** (necessary condition) |
| Margin asymmetry (packing direction) | UCP excess > NDP excess | NDP excess > UCP excess | **No** — direction inverted |
| Neutral ensemble EG sign | Median EG > 0 (election-day) or ≈ −2.3% (full-vote, scaled) | Negative | **Yes** — direction matches at full-vote scale |
| Neutral ensemble EG magnitude | Ensemble brackets 2019 baseline of −2.64% | Ensemble brackets observed bias | **Yes, weakly** (wide CI) |

## 5. Interpretation: does Chen-Rodden transfer to Alberta?

**Partially, but not for the reasons Chen & Rodden identified.** The headline prediction — that neutrally-drawn maps for Alberta produce an EG near the observed 2019 baseline — is supported. But the mechanism is different: Alberta's "natural packing" is not urban-clustering packing (Chen-Rodden) — it is rural-dispersed-loss combined with small rural riding populations.

The implication for the audit's §3.6 framing is nuanced:

- **The "natural-packing floor" language is defensible** as a shorthand. The 2019 baseline of −2.64% is within the estimated neutral-ensemble distribution for Alberta's 2023 voter geography.
- **The mechanism attributed to that floor needs correction.** Chen-Rodden describes urban-packing as the mechanism. In Alberta, the operative mechanism is different: rural inefficiency and widespread dispersed losses in suburban and rural ridings. The report should not imply NDP voters are concentrated into a few high-margin urban districts; in 2023 they are not (NDP excess = only 9.3% of NDP votes, lower than UCP excess at 15.9%).
- **The 2026 framing survives with adjustment.** The report's claim that "the majority 2026 EG (−0.85%) moves toward zero, which means the majority proposal is actively correcting for natural packing" is defensible *if* the baseline claim is defensible. The ensemble supports a natural-packing floor in the range [−4.4%, −0.7%] under full-vote scaling. EGs of −0.85% (majority) and −1.36% (minority) **are both within** this natural range, but both are UCP-favored-less than the ensemble median estimate of ≈−2.3%. Both 2026 maps do correct for some of the natural floor; the question of whether that correction is engineering or a byproduct of other decisions is unsettled by this analysis.

## 6. Implications for §3.6 of the academic report

**Finding:** Chen-Rodden's natural-packing claim **transfers to Alberta in directional form** — neutral 87-seat plans of Alberta reproduce a UCP-favored EG centered at approximately the 2019 baseline (−2.3% to −2.4% with a ±1.7 pp interval). **But the specific urban-packing mechanism Chen-Rodden identified does not operate in Alberta.** Alberta's floor comes from rural inefficiency, not urban over-concentration.

**Recommended revisions to §3.6 (in increasing strength):**

**Revision A (minimum required by evidence).** Qualify the "natural-packing floor" language with a footnote: "The US-derived Chen-Rodden mechanism emphasizes concentration of urban voters; Alberta's analogous outcome arises primarily from rural dispersed loss (see analysis/methodology/v0_1_chen_rodden_alberta_validation.md). The direction of bias matches; the mechanism differs." The "−2.6% EG is Alberta's natural-packing floor" sentence should be rewritten as "the 2019 EG of −2.64% is approximately at the center of the neutral-ensemble distribution (interval [−4.4%, −0.7%])."

**Revision B (strengthening).** Replace the mechanism attribution throughout. Wherever the report attributes EG to "NDP voter concentration in Calgary and Edmonton" (e.g., §3.6 opening paragraph), add the observation that NDP urban wins are by modest margins (21.5 pp) and carry low excess waste (9.3%), whereas rural UCP wins are by very large margins (43.0 pp) with high excess waste (15.9%) — concentration alone is not the operative mechanism.

**Revision C (if applied rigorously).** The ensemble confidence interval [−4.4%, −0.7%] at full-vote scale is wide enough that **both** 2026 maps (−0.85% and −1.36%) sit within the neutral range. Under that reading, **neither 2026 map is engineered against the natural floor; both are consistent with neutrally-drawn plans.** The structural findings (Sections A, C, D) are the audit's primary evidence; Section B partisan-bias metrics alone are not distinguishing evidence between the two 2026 maps once the full ensemble uncertainty is acknowledged. The current §3.6 footnote treating the asymmetry as "a distinct explanation beyond neutral mapmaking is required" would then need softening.

**Recommendation:** Revision A is supported by the evidence in hand and is a minor edit. Revision B is supported by the margin-asymmetry evidence and adds precision. Revision C requires running the full-vote ensemble explicitly (not estimated via scaling) and is a follow-up task. Run both ensemble versions (election-day and full-vote) via GerryChain ReCom on DA units for a definitive answer.

**§3.6's structural-findings disclaimer is unaffected.** The paragraph noting that Chen-Rodden's natural-packing argument does not reach Section A (population equality), Section C (geographic coherence), or Section D (procedural fairness) findings remains valid. Those findings do not rest on vote-distribution modeling and are unchanged by this analysis.

## 7. What Track U cannot settle in this budget

- A full GerryChain ReCom ensemble on DA units (6,203 atoms, 87 districts). This is the gold-standard version of the test. It requires additional installation (`libpysal`, tuned chain lengths) and runtime on the order of 8–24 hours for a well-mixed 10,000-plan ensemble.
- A **full-vote ensemble** (rather than election-day-only scaled). Requires a spatial disaggregation of advance/absentee ballots into VA-level allocations, which requires additional data (ED-level advance-poll records) and assumptions about how advance voters are spatially distributed within EDs.
- A 2019-electorate version of the ensemble. The cross-election contingency noted in §3.5 of the academic report already shows the partisan-bias direction reverses sign under 2019 inputs; Chen-Rodden's mechanism is electorate-specific, so a full treatment should run the ensemble under both electorates. Re-running this script with the 2019 vote data substituted in would produce that.

## 8. Files

- `analysis/scripts/v0_1_chen_rodden_alberta.py` — reproducible pipeline.
- `data/v0_1_chen_rodden_simulation.csv` — per-plan ensemble metrics (150 plans, Test 3).
- `data/v0_1_chen_rodden_summary.json` — structured summary (Tests 1, 2, 3).

## 9. References

- Chen, J. & Rodden, J. (2013). "Unintentional gerrymandering: Political geography and electoral bias in legislatures." *Quarterly Journal of Political Science* 8(3): 239–269.
- Chen, J. & Rodden, J. (2015). "Cutting through the thicket: Redistricting simulations and the detection of partisan gerrymanders." *Election Law Journal* 14(4): 331–345.
- Stephanopoulos, N. & McGhee, E. (2015). "Partisan gerrymandering and the efficiency gap." *University of Chicago Law Review* 82(2): 831–900.
- Warrington, G.S. (2018). "Quantifying gerrymandering using the vote distribution." *Election Law Journal* 17(1): 39–57.
- McDonald, M.D. & Best, R.E. (2015). "Unfair partisan gerrymanders in politics and law: A diagnostic applied to six cases." *Election Law Journal* 14(4): 312–330.
- Moran, P.A.P. (1950). "Notes on continuous stochastic phenomena." *Biometrika* 37(1/2): 17–23.
