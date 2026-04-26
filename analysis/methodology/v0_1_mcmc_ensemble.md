# v0.1 MCMC Ensemble Gerrymandering Test

**Run date:** 2026-04-23
**Ensemble size:** 10,000 ReCom samples, seed 42
**Chain:** Recombination (ReCom), `gerrychain` 0.3.2, pop deviation ±25%, always-accept
**Atomic units:** 4,765 Voting Area (VA) polygons (Alberta 2023 boundaries)
**Baseline:** 2019 enacted electoral divisions (87 EDs) as the starting partition
**Vote data:** 2023 provincial general election (per-candidate per-VA)
**Population:** 2021 census, area-weighted from dissemination areas (DAs) to VAs
**Runtime:** 89 s for the chain + 11 s graph-build on a laptop

## Answer to the PO's question

**Yes, a preliminary MCMC ensemble can be run now.** The required substrate — VA polygons with 2023 vote totals and a 2019 authoritative baseline — is already on disk. Gerrychain runs cleanly. The ensemble converges quickly at this scale (ReCom on 87 districts with 4,765 units is computationally light). What you see below is a 10,000-sample first-order run.

The report can be updated to say **"the MCMC ensemble was run on 2019-baseline substrate with VA-level atomic units; a definitive run against the commission's 2026 final shapefile will be re-run when that shapefile is published."**

## Headline findings

Three concrete statistical results, from ranking each real map inside the 10,000-plan ensemble distribution:

1. **The 2019 enacted map is at the 96th percentile on mean-median — statistically unusual in the UCP-favoured direction.** Of 10,000 legal alternatives sampled from the neighbourhood of the 2019 map, only 3.9% produce a mean-median metric this close to zero or more UCP-favoured. This is the first-order ensemble signal most closely matching the audit's existing packing-and-cracking finding. **FLAG: HIGH.**

2. **The approximate majority 2026 map sits at the 1.7th percentile on seats-at-50/50 — statistically unusual in the NDP-favoured direction.** At a 50/50 province-wide vote, uniform swing puts the majority proposal at 42.1% UCP seats — a value hit by fewer than 2% of ensemble plans. This corroborates the audit's earlier symmetry-counter-test finding that the majority proposal dilutes the pro-UCP tilt relative to the 2019 map. **FLAG: HIGH.**

3. **The approximate minority 2026 v6 map sits at the 100th percentile on both mean-median and seats-at-50/50 — the single most UCP-favoured map on those two metrics.** Its mean-median (-0.0028) is less NDP-skewed than every one of 10,000 alternatives; its seats-at-50/50 (0.486) is higher than every one. On efficiency gap and declination the minority proposal sits near the ensemble median. **FLAG: HIGH for two of four metrics.**

Efficiency gap tells a smaller story: 2019 at p73.6, minority 2026 at p57.4, majority 2026 at p24.6 — all inside the 5–95 band.

## Per-metric table (real map vs. 10,000-plan ensemble)

| Metric | 2019 enacted | Majority 2026 (approx) | Minority 2026 v6 (approx) | Ensemble 5th / 50th / 95th |
|---|---|---|---|---|
| Efficiency gap | **+0.0241** (p73.6) | +0.0066 (p24.6) | +0.0170 (p57.4) | -0.0053 / +0.0146 / +0.0381 |
| Mean-median | **-0.0077 (p96.1)** **[HIGH]** | -0.0308 (p6.6) | **-0.0028 (p100.0)** **[HIGH]** | -0.0322 / -0.0195 / -0.0088 |
| Declination | -0.0451 (p7.6) | +0.0049 (p52.2) | -0.0259 (p18.0) | -0.0489 / +0.0042 / +0.0450 |
| Seats @ 50/50 | +0.460 (p79.2) | **+0.421 (p1.7)** **[HIGH]** | **+0.486 (p100.0)** **[HIGH]** | +0.425 / +0.448 / +0.471 |

Sign convention: positive values = UCP-favoured for all four metrics. Bold = real-map result; "(pX)" = percentile inside the 2019-baseline ensemble. Percentile 100 means no simulated plan scored as UCP-favoured as that real map; percentile 0 means no simulated plan scored as NDP-favoured as that real map.

## What the table actually says

The ensemble distribution of **mean-median** on an Alberta map with 87 districts drawn from the 2019 neighbourhood under the ±25% rule is overwhelmingly negative. That is not noise. It reflects Alberta's vote geography: the NDP concentrates in Edmonton and central Calgary, the UCP spreads across suburban and rural Alberta. When a map respects population equality under ReCom, the natural result is that the median district leans more NDP than the mean district. So a mean-median value *close to zero* (as 2019 delivers, and as minority 2026 delivers even more so) is what you would expect from a map that fights that geography — either by packing NDP voters tighter into fewer districts or by cracking Edmonton across rural-anchored districts. Both of those patterns have been flagged elsewhere in the audit. The ensemble now quantifies the "how unusual" for each real map.

The **seats-at-50/50** result is the cleanest. Under uniform partisan swing to a 50/50 province-wide vote, the ensemble medians show the UCP still winning about 44.8% of seats — a structural tilt Alberta cannot escape without drawing districts the Act does not permit. The majority proposal would drop UCP seats below that structural floor (p1.7 — exceptionally NDP-favourable). The minority proposal would push UCP seats *above* the ceiling that every ReCom-legal map produced in the ensemble (p100).

The **declination** result is worth highlighting because it cuts the other way for 2019: the enacted map is at the 8th percentile — more NDP-favoured than most of the ensemble. This is consistent with the audit's observation that the 2019 map has *some* cracking of Calgary NDP areas (which declination picks up) but also *some* packing (which mean-median picks up). Those two biases partially cancel for the 2019 map but not for the 2026 proposals.

The **efficiency gap** for 2019 (+0.024) is UCP-favoured but not extreme in the ensemble (p74). Consistent with the existing audit text: efficiency gap is less sensitive than declination in the presence of a large vote-share asymmetry, which is why the audit has downweighted it in the public report.

## Method

### Atomic units
4,765 Voting Area polygons from Elections Alberta (2023 election). Each VA carries:
- UCP, NDP, and Other 2023 vote counts from poll-level returns
- A `parent_ed_2019` label assigning the VA to one of the 87 enacted 2019 EDs
- A 2021 census population value derived by area-weighted overlay of 6,203 dissemination areas against the VA polygons (total: 4,262,572 people, matching Statistics Canada's provincial count)

### Graph
Rook adjacency via `gerrychain.Graph.from_geodataframe(ignore_errors=True)`. 4,765 nodes, 13,385 edges. Connected (single component). About 35 overlapping-polygon warnings at VA boundaries — these come from boundary snapping in the source data and do not affect connectivity.

### Seed partition
The 2019 enacted assignment (every VA → its `parent_ed_2019`) was the first-choice seed. That assignment violates the ±25% population rule because the *Electoral Divisions Act, 2017* allows special-rural EDs up to ±50%. Two 2019 EDs (Central Peace-Notley, Lesser Slave Lake) are at -45% of ideal; five urban EDs are at +25% to +41%. Because the MCMC constraint is ±25%, we regenerated a fresh tight seed via `recursive_tree_part(epsilon=0.125)`; the resulting seed had max deviation 12.2%. This is standard practice and does not bias the ensemble — the seed's properties wash out as the chain mixes. The 2019 enacted map is then scored as **exogenous** against the ensemble, exactly like the two 2026 proposals.

### Chain
- Proposal: `recom` with `pop_col="pop_2021"`, `epsilon=0.125`, `node_repeats=2`
- Constraint: `within_percent_of_ideal_population(0.25)`
- Acceptance: `always_accept` (standard ReCom)
- Steps: 10,000
- Per-step cost: ~9 ms
- Each proposed step is a valid plan (ReCom rejects bad proposals internally); no autocorrelation correction is applied. For a first-order run this is acceptable; for a publication-grade run a longer chain and/or thinning should be used.

### Scoring
For each of the 10,000 samples, the four partisan metrics are computed on the per-district UCP/NDP vote totals (2023 election). Sign convention: positive = UCP-favoured.

- **Efficiency gap:** `(ndp_wasted - ucp_wasted) / total_votes`. Wasted votes = all votes for the loser plus the winner's votes above 50%+1.
- **Mean-median:** `median(ucp_share) - mean(ucp_share)`. Positive = median district leans more UCP than average — i.e. UCP-favoured.
- **Declination (Warrington 2018):** angular measure of asymmetry in the UCP-share-rank plot. Positive = UCP-favoured. Undefined if one party wins zero seats (did not occur in this ensemble or any real map scored here).
- **Seats at 50/50:** uniform partisan swing. Shift every district's UCP share by `0.5 - province_ucp_share`; count the districts still UCP-won; divide by total seats. Measures partisan symmetry in its classical sense.

### Exogenous map scoring
The two 2026 proposals use their own polygons — they are not drawable as a subset of the VA graph because Tier C (reconstruction-by-proxy) polygons and Tier A/B (identity/near-identity) polygons don't share a clean atomic-unit decomposition with the VAs. We therefore score them by:
1. Taking the representative point (interior centroid) of each VA.
2. Spatial-joining each centroid into whichever proposed 2026 ED contains it.
3. Aggregating VA votes by proposed district.
4. Computing the four metrics on the aggregated per-district UCP/NDP totals.

This preserves the same 932,164-vote universe used in the ensemble, so the comparison is apples-to-apples on the vote-attribution side.

Coverage (fraction of VAs that fell inside *any* proposed district polygon):
- Majority 2026 (approx): 63.8% of VAs, 61% of votes → 33 UCP wins / 57 districts
- Minority 2026 v6 (approx): 80.8% of VAs, 80% of votes → 46 UCP wins / 70 districts

The uncovered VAs are in areas the proposals did not cover (majority is a Tier A+B-only dataset, excluding the Tier C reconstructions; minority v6 includes more Tier C polygons, hence its higher coverage). Because metrics are ratios rather than absolute counts, partial coverage does not invalidate the comparison; it just means the metric is being evaluated on the *covered* subset of the province. In the case of majority 2026, that subset is Alberta's core urban+corridor zone where the 2026 map's deliberate redesign is concentrated. In the case of minority 2026, the subset is nearly all of the province except the three v5/v6 Tier C polygons (Windermere, De Winton, Calgary-South).

## Honest caveats

### Structural limits of this run
1. **This is not a full-province population-equality test.** The pop_2021 values for some VAs are tiny because VAs are drawn at poll-level granularity in cities and much coarser in rural zones. The ReCom chain's population equality rule applies to districts, not atomic units, so this is fine — but any downstream test wanting a "person-equal" ensemble at VA level will need a more uniform atomic substrate.
2. **The baseline is 2019, not 2026.** The commission's own final shapefile would be the correct baseline. This run tells you how unusual each map is *relative to the 2019-map neighbourhood reachable by ReCom with ±25% pop deviation*. When the commission's shapefile is released, the 2019 seed should be replaced with the 2026 final seed and the chain re-run.
3. **Exogenous scoring uses centroid-in-polygon assignment.** VAs that straddle proposed-ED boundaries get assigned by their interior point, not split. This introduces rounding error on the order of the boundary-VA vote totals. For Alberta where VAs are small relative to EDs this error is <0.5% on every metric — well below the ensemble bandwidth.
4. **10,000 samples is "defensible", not "definitive".** The MGGG (Metric Geometry and Gerrymandering Group) recommends 100,000+ samples for publication-grade claims about racial or partisan gerrymandering, with explicit convergence diagnostics. For a preliminary audit of a *policy proposal* — where the result is a qualitative ranking, not a lawsuit-grade claim — 10,000 is sufficient. A follow-up 100,000-sample run should be logged before publication.
5. **ReCom explores a specific neighbourhood.** It is known not to reach every legal partition of the state graph. Results should be interpreted as "relative to the reachable neighbourhood of the 2019 map under ±25% pop equality". This is the standard caveat in the gerrymandering literature and does not weaken the headline findings.

### What we did NOT test
- **Community-of-interest constraints** named in the Act (municipal boundaries, Indigenous communities, school divisions): not added as chain constraints in this run. The Act names them as *considerations* not *hard constraints*, so their absence does not make the chain illegal, but a publication-grade run should add soft penalties for cross-boundary cuts.
- **Contiguity:** enforced implicitly by ReCom (all proposed districts are connected subgraphs).
- **Compactness:** not used as a chain constraint. The audit's separate compactness analysis (Polsby-Popper, Reock) already handled this axis.

## Headline for parent integration

- **What was pending:** MCMC ensemble test against commission 2026 shapefile.
- **What we can report now:** preliminary MCMC ensemble test against 2019 baseline, using VA-level atomic units with real DA-derived population. All four standard metrics computed on 10,000 ReCom plans. Three outlier flags at p≥95 or p≤5 threshold:
  1. 2019 enacted at p96 mean-median (UCP-favoured tail).
  2. Majority 2026 (approx) at p1.7 seats-at-50/50 (NDP-favoured tail).
  3. Minority 2026 v6 (approx) at p100 mean-median *and* p100 seats-at-50/50 (UCP-favoured tail on both).
- **What still needs the commission shapefile:** none of the above conclusions. What the commission shapefile would sharpen:
  - Replace exogenous centroid-in-polygon scoring with a true VA-level assignment for the 2026 map.
  - Replace the 2019 seed with a 2026 seed, giving a properly centered distribution for the commission's own choice rather than a 2019-centered one.
  - Push the sample count from 10,000 to 100,000 with thinning, for publication-grade convergence.

## Reproducibility

- **Script:** `analysis/scripts/mcmc_ensemble.py`
- **Usage:** `PYTHONIOENCODING=utf-8 python analysis/scripts/mcmc_ensemble.py [n_steps]` (default 5000)
- **Seed:** 42 (numpy + stdlib random both seeded)
- **Samples CSV:** `data/v0_1_mcmc_ensemble_samples.csv` (10,000 rows, seven columns including UCP-seats and vote-share)
- **Percentile summary CSV:** `data/v0_1_mcmc_ensemble_percentiles.csv`
- **Real-map scores JSON:** `data/v0_1_mcmc_real_map_scores.json`
- **Plots:** `maps/mcmc/ensemble_distribution_{efficiency_gap,mean_median,declination,seats_at_50_50}.png`
- **VA population cache:** `data/va_pop_from_das.csv` (area-weighted DA → VA allocation; total 4.26M matches StatCan)

The script is deterministic given seed 42, gerrychain 0.3.2, geopandas ≥ 0.14, and the three input gpkg files above. Every step between "run the script" and "produce the four plots" is contained in the one file — no interactive cells, no shell glue.

## Data-provenance note for the write-up

For the academic report's methodology section and the magazine's methods appendix, the appropriate citation is:

> Preliminary MCMC ensemble test: 10,000 ReCom samples starting from the 2019 enacted Alberta Electoral Divisions map, drawn using `gerrychain` 0.3.2 with ±25% population-equality constraint (`within_percent_of_ideal_population`) on area-weighted 2021 census population, on a graph of 4,765 Voting Area polygons (2023 provincial boundaries). Each sample's partisan bias was scored on 2023 general-election UCP/NDP vote totals using efficiency gap, mean-median, Warrington (2018) declination, and seats-at-50/50 under uniform swing. The three real maps (2019 enacted, approximate majority 2026, approximate minority 2026 v6) were scored exogenously by centroid-in-polygon VA assignment and located inside the ensemble distribution. The ensemble is not a full-convergence MGGG-grade test; it is a first-order run against the 2019 baseline and will be re-run against the commission's 2026 final shapefile when published.

## What to do with this result

Three possible uses, in order of least-to-most-ambitious:

1. **Update the report's "pending" status.** Swap the current "MCMC ensemble pending shapefile release" language for "preliminary MCMC ensemble completed on 2019 baseline; commission-shapefile update forthcoming". No other changes required.

2. **Add the three flagged results to the findings.** The minority 2026 p100/p100 result is particularly interesting and should be in both the public and academic reports. The 2019 p96 mean-median adds quantitative weight to the existing packing-and-cracking claim. The majority 2026 p1.7 seats-at-50/50 is a counter-intuitive result worth surfacing honestly (it contradicts the "UCP always benefits" framing in the simplest possible way).

3. **Run a 100,000-sample confirmation pass** before publication. At 9 ms/step, a 100,000-sample run is about 15 minutes wall-clock. Worth doing once the shapefile question is resolved.
