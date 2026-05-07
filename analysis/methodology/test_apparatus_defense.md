---
name: Test apparatus — defense, dependency graph, and epistemological self-audit
description: Answers four framing questions about the audit's test battery — (1) are we making up metrics to have metrics or do they map real phenomena; (2) how do the tests relate to each other in a formal dependency structure; (3) what does the current structure have and what is missing; (4) can we defend the whole apparatus. Includes expanded criticism + defense for the five novel combined tests scoped in test_selection_rationale.md §6.
type: methodology
---

# Test apparatus — defense, dependency graph, and epistemological self-audit

**Companion to:** `analysis/methodology/test_selection_rationale.md` (why-these-tests-not-others) and `analysis/methodology/red_team_consolidated.md` (38+ attack record). This file answers the framing questions a reviewer asks when they step back from any individual test and interrogate the whole assemblage.

---

## 0. The four framing questions

1. **Are we making up metrics to have metrics, or do they actually map something useful?**
2. **How do all the datapoints relate to each other — can we build a graph of the tests where their relations demonstrate the presence or absence of a concern?**
3. **Does the current audit structure come close to that graph? If so, what is missing? Can we defensibly build what is missing?**
4. **Can we defend the whole apparatus?**

Answers below, grounded in the actual test set and the red-team history.

---

## 1. Are we making up metrics to have metrics?

This is the key epistemological failure mode for forensic audits and the one a hostile peer reviewer will attack first. It has a specific name in the methods literature: **metric proliferation as soft p-hacking** (Wasserman 2016; Simonsohn, Nelson, & Simmons 2014 on the "garden of forking paths"). The accusation is: the audit keeps adding metrics until some subset supports the desired conclusion, and the final claim rests on whichever metrics happened to align.

### 1.1 Diagnostic criteria (how to tell)

Five criteria separate metric proliferation from genuine convergent validity:

1. **Distinct construct.** Each metric measures a *different* aspect of the phenomenon. Redundant metrics (multiple ways of measuring the same thing) inflate apparent convergence.
2. **Prior literature support.** Each metric comes from a named literature source with citations that predate this paper. Metrics invented for this paper alone are under suspicion.
3. **Predicted correlation structure.** The relationships between metrics are *predicted* by theory before the data is consulted. Discovered post-hoc correlations can be accidental.
4. **Dis-confirming metrics reported alongside confirming.** If the audit selectively reports metrics that support its claim, it is proliferating.
5. **Concrete consequences on failure.** If a metric fails its pre-registered threshold, what finding is retracted? If the answer is "nothing," the metric is decorative.

### 1.2 Per-family audit against the criteria

**A-family (population equality — §5.1).**
- A1 MAD: literature source = US *Reynolds v. Sims* (1964) and Canadian *Reference re Saskatchewan* (1991). Predated. ✓
- A2 Calgary zone: derived from commission's own published variance tables. Two classification rules to guard against zone-definition arbitrariness. ✓
- A3 s.15(2) eligibility: statutory criteria from the Alberta Electoral Divisions Act. Predated by statute. ✓
- **Assessment: not metric proliferation.** Each A-test measures a distinct aspect of population equality (variance, regional balance, special-exception legitimacy). Literature-backed.

**B-family (partisan bias — §5.2).**
- B2 EG: Stephanopoulos & McGhee 2014. Most-cited post-2010 US test. ✓
- B3 MM: McDonald & Best 2015. Complementary measure. ✓
- B4 Seats at 50/50: Gelman & King 1994 (from Grofman 1983, King & Browning 1987). The Bayesian seat-vote tradition. ✓
- B5 MCMC ensemble: DeFord, Duchin, Solomon 2021 (MGGG). Predated. ✓
- B6 declination: Warrington 2018. Explicitly added for Katz-King-Rosenblatt 2020 consistency-across-metrics. ✓
- **Assessment: not metric proliferation.** Warrington 2019 documents that these metrics disagree on ~30 % of US plans; running them together is the *discipline*, not the padding. The paper reports the B6-vs-B2 disagreement in §5.2.4 rather than hiding it — the fourth criterion (dis-confirming metrics reported alongside) is satisfied visibly.

**C-family (geographic coherence — §5.8).**
- C1/C2 compactness: Polsby & Popper 1991, Reock 1961. Predated. ✓
- C3 visual anomalies: chair's own published list from minority report. Not audit-invented. ✓
- C4 CSD splits: Alberta Municipal Government Act boundaries + 2021 census geography. ✓
- C5 municipal/DA anchoring: novel to this audit, but the underlying construct (preservation of community-of-interest via administrative boundaries) is a standard Canadian-commission norm documented in Courtney 2001 and the 2017 Alberta commission's own rationale text. ✓
- **Assessment: C5 is novel but well-anchored.** Would strengthen if cited in the methods paper (Issue #10) with explicit Courtney 2001 linkage.

**D-family (procedural — §5.9 / D1–D10).**
- Legal-defensibility dimensions from *Grant v. Torstar* (responsible communication) and *Reference re Saskatchewan* 1991 effective-representation doctrine. Pre-existing legal framework. ✓

**Signature tests (§5.3).**
- Packing, cracking: Cox & Mair 1985; Gelman & King 1994. ✓
- Engineered boundary (E2): Altman & McDonald 2011 formulation, re-adapted for Alberta §15(2). The reformulation is specifically disclosed in §5.3.3 as post-hoc (Gemini Phase B.2). ✓

### 1.3 Where we are most exposed

Three places where the accusation could stick:

1. **Four-measurement-layer reporting in §5.2.7.** We report four substrates (crosswalk, centroid, MAUP-v1 overlap-contaminated, MAUP-v2 topology-clean) plus now a fifth (DPG-perturbation CI) and sixth (tier-aware perturbation CI) and seventh (v0_5 DA-anchored rerun). That is seven layers. A hostile reviewer could say: "you kept running layers until you found a story."
   - **Defense**: each layer was added *before* its result was computed, each layer measures a structurally different thing (binary-assignment bias, DPG transcription artifact, DPG-construction error, perimeter uncertainty), and the disagreement between layers is *itself* the reported finding — not the agreement. We are explicit that *the paper does not pick a winner*. This is the opposite of p-hacking, which would be picking the layer that supports the conclusion.

2. **The `canon_source` precedence rules.** We assign source tiers (v7 < 2019-parent < osm-municipal-buffered < sweep) to resolve overlaps in topology cleanup and to key tier-aware perturbation sigmas. A reviewer could say: "you chose a precedence that makes your preferred direction survive."
   - **Defense**: the precedence is theoretically motivated (authoritativeness of the source, not the direction of the resulting finding). The ordering is derivable from external criteria (2019 shapefile is government-published; sweep is population-calibrated; OSM-municipal is survey-grade) without consulting the partisan output. The commit message for the topology cleanup (452f841) documents the rule ex ante and the anti-erasure safeguards.

3. **Novel combined tests in `test_selection_rationale.md` §6** (the five this document expands). These are proposed but not yet executed. Each is worth executing or dropping explicitly; leaving them as "planned but never run" creates a soft-proliferation trap.
   - **Defense**: executed tests that fail are reported (B6 declination is the worked example). Proposed tests that are never executed should be dropped from the record or executed. This document is the place to make that commitment per-test.

### 1.4 Verdict

**The audit passes the metric-proliferation test on all five criteria for the five core families.** The §5.2.7 four-seven-layer framing is the single most-exposed area and it passes under the specific defense that the layers are *predicted disagreements*, not curated confirmations. The novel combined tests in §3 below are individually defensible; each must be executed or retracted to stay defensible at the set level.

---

## 2. Per-test expansion of the five combined tests

This section documents each test in the depth needed for execution or formal retraction. Each subsection follows the same template: definition, phenomenon mapped, literature basis, five criticisms, five defenses, discriminant-validity argument, implementation cost, status.

### 2.1 Neighbour-drain adjacency test

**Definition.** For each pair of adjacent EDs $(X, Y)$ on the same map under the 2023 Statement-of-Vote substrate, compute:

$$s_X = \frac{\max(V_A^X, V_B^X) - \lceil N_X/2 \rceil - 1}{N_X} \quad \text{(losing party surplus rate in X)}$$

$$m_Y = \left| V_A^Y - V_B^Y \right| / N_Y \quad \text{(margin in Y)}$$

Define $(X, Y)$ as an **adjacency-chain signal** if $s_X \geq 0.15$ (X is packed against the losing party) AND $m_Y \leq 0.05$ (Y is cracked: losing party within 5 pp of the winning threshold). Count chain signals per map.

**Phenomenon mapped.** The mechanical coupling between packing and cracking. In a genuine gerrymander, packing concentrates a losing party's votes in a few districts; the drained adjacent areas become low-margin losses for the same party. A chain count distinguishes *coupled* packing-cracking (cartographic choice) from *incidental* packing + incidental cracking (geographic accident).

**Literature basis.** Stephanopoulos & McGhee (2015, pp. 848–851) describe the packing-cracking mechanism but do not operationalise the adjacency coupling. Chen & Rodden (2013) demonstrate that natural packing without cracking can produce apparent partisan bias without intent; the adjacency test is the inverse discriminator that isolates the intent-signal from the natural-geography signal. DeFord, Duchin, and Solomon (2021) treat adjacency as a graph property of the underlying ReCom process but do not use it as a gerrymander-detection statistic.

**Five criticisms + defenses.**

1. **"The 15 % surplus-rate threshold is arbitrary."**
   - **Defense:** Sensitivity-test across $s_X \in [0.10, 0.20]$ and report chain-count for each threshold. A signal that is robust to the threshold is a real coupling; a signal that disappears below 0.15 is an artifact of the threshold. The paper reports both the primary threshold and the sensitivity band.

2. **"Adjacency in Alberta is mostly rural-to-urban, so chain signals will always accumulate at city boundaries."**
   - **Defense:** Restrict the chain test to same-category adjacencies (urban-urban and rural-rural separately), documented per category. The minority's four-way Airdrie split would still generate chain signals under the urban-urban restriction; the majority's two-way split would generate fewer.

3. **"Alberta has few cities, so the chain count is dominated by 3–4 specific municipalities (Calgary, Edmonton, Red Deer, Lethbridge) and doesn't generalise."**
   - **Defense:** Report chain count both as a raw count and as a per-urban-municipality rate (chain-count / number-of-urban-EDs-in-that-city). The per-rate version normalises for Alberta's urban structure.

4. **"This is just a re-labelling of the §5.3.1 packing + §5.3.2 cracking findings and isn't genuinely new."**
   - **Defense:** The chain count specifically measures the *coupling*. The existing §5.3.1 and §5.3.2 are independent observations: Zone-A packing, four-way Airdrie cracking. The adjacency test asks whether they are causally coupled. A gerrymanderer who packs without cracking leaves voters with representation elsewhere; a gerrymanderer who pairs packing with cracking deprives them of representation anywhere. The coupling test therefore measures *intent-to-disenfranchise*, which the separate tests do not.

5. **"This is ex post facto. You designed the test after seeing the 2026 maps."**
   - **Defense:** The test is pre-registered in `analysis/methodology/test_selection_rationale.md` §6.1 at its current publication version. Its application to the 2026 November committee's 91-seat map when that map tables will be a genuine out-of-sample test. Until then, document the test and its threshold sensitivity explicitly; do not count the Alberta 2026 proposal results against this test's pre-registration credibility.

**Discriminant validity.** Not redundant with §5.3.1 (packing alone), §5.3.2 (cracking alone), B2 EG (whole-map wasted-vote asymmetry), or C4 CSD splits (within-municipality partition). Correlation with each is limited by construction: the chain test requires BOTH packing AND cracking in adjacent EDs, a conjunction the other tests do not capture.

**Implementation.** `geopandas.sjoin(predicate='touches')` for adjacency; per-ED vote totals from 2023 Statement of Vote (already in the repo at `data/alberta_2023_results.csv`); threshold loop + chain-count aggregation. ~200 lines of Python. Runtime negligible. **Effort: 2 days** including writeup + sensitivity table.

**Status.** Scoped, not executed. **Recommendation: execute** — the highest value-to-effort test in the battery.

### 2.2 Boundary-chain test (systemic vs ad-hoc)

**Definition.** A **boundary chain** is a sequence of 3 or more consecutive ED-to-ED boundaries passing through a single municipality or adjacent municipal area. For each chain, compute:

$$\text{ChainOutcome}_{\text{actual}} = \sum_{i \in \text{chain}} \mathbb{1}[V_A^i > V_B^i] \quad \text{(seats party A wins from the chain's EDs under 2023 votes)}$$

Compute the same under a reference partition (2019 boundaries or the opposite 2026 proposal, applied to the same territory). The **chain-asymmetry** = actual − reference, in expected seats per party.

**Phenomenon mapped.** Systematic versus ad-hoc partitioning. Per-boundary defensibility (each boundary follows a visible feature) can coexist with a systematic chain effect (the cumulative choice of boundaries produces a politically skewed partition). The individual-boundary B-family tests and the whole-map A-family tests cannot detect patterns that only emerge at 3+-boundary scale.

**Literature basis.** The concept of "contiguity-preserving gerrymander" in Altman and McDonald (2011) and the "incremental unfairness" doctrine in Davis v. Bandemer (1986) both rely on the idea that cumulative small decisions can produce large partisan outcomes. The chain test operationalises that concept quantitatively.

**Five criticisms + defenses.**

1. **"What counts as a 'chain' is subjective."**
   - **Defense:** Use the commission's own descriptive text in Appendix E to identify chains: a chain is a sequence of boundaries the commission describes in the same paragraph or the same ED-description as sharing a purpose (e.g., "the four boundaries partitioning Airdrie"). This ties the identification to commission-authored text rather than analyst judgment.

2. **"Which reference partition is the right one?"**
   - **Defense:** Report chain-asymmetry against three references: (a) 2019 enacted, (b) the opposite 2026 proposal, (c) a neutral MCMC draw from the ensemble. Consistency across all three is the reportable finding; if only one reference produces the finding, the test fails and is reported as such.

3. **"Canadian redistribution norms permit chain decisions."**
   - **Defense:** Not in dispute. The chain test asks whether the chain produces a systematic partisan outcome; it does not ask whether the chain is permitted. Permissible systematic partisan partitions are still partisan, which is the §5.2 finding. The chain test adds evidence at a different resolution.

4. **"Alberta's geography forces chain decisions (Calgary is a big city)."**
   - **Defense:** Compare chain-asymmetry across Canadian commissions. If chain-asymmetry in Alberta 2026 is comparable to BC 2023 or Saskatchewan 2022, the finding is a geographic artifact; if Alberta 2026 exceeds other commissions by a wide margin, the finding is cartographic choice. (This links to the `canadian_base_rate_computed.md` comparator.)

5. **"You designed the chain criterion to catch Airdrie."**
   - **Defense:** Airdrie is one of several chains on the minority map; the same criterion applies to Lethbridge, Red Deer, and the Calgary metropolitan ring. The §5.6 symmetry-counter-test already flags these as additional minority-only chains; the boundary-chain test quantifies their cumulative partisan effect.

**Discriminant validity.** Not redundant with B-family (whole-map) or §5.3 (per-district-signature). The chain test measures an intermediate scale — multi-district cumulative partition — that neither current test covers.

**Implementation.** Manual chain identification from commission text (~1 hour); compute per-ED 2023 seat outcomes under three references (existing script reuse); aggregate. **Effort: 4–6 days** including inter-reference comparison + commission-text parsing + writeup.

**Status.** Scoped, not executed. **Recommendation: execute after Neighbour-drain** — high value, more effort, more subjective. Worth doing but requires careful specification.

### 2.3 Temporal-compound durability test

**Definition.** For each map $M$ and each provincial-vote scenario $v \in \{0.40, 0.42, \ldots, 0.60\}$ (UCP two-party share — an 11-point grid covering the plausible 2027–2035 swing window):

1. Apply a uniform swing to 2023 baseline to reach $v$.
2. Recompute EG, MM, Seats at 50/50, Decl on the swung distribution.
3. Record the minority-majority EG asymmetry.

Report the **maximum-over-scenarios asymmetry**, the **mean-across-scenarios**, and the **cross-scenario sign-consistency** (fraction of scenarios with the same sign as the 2023 point estimate).

**Phenomenon mapped.** Durability of the partisan effect across the boundaries' operative window. A map that is neutral at 2023 votes but becomes gerrymanderous in a competitive 2031 election is still a gerrymander during the half of the cycle it governs competitive elections. The §5.2.3 cross-election robustness test covers only three observed elections (2015, 2019, 2023) plus April 2026 polling; the durability test covers the full plausible swing space.

**Literature basis.** Stephanopoulos and McGhee (2018, §IV) acknowledge that EG is sensitive to the vote-share distribution and recommend scenario sweeps. Gelman and King (1994, §V) advocate testing seat-vote curves across the full domain. The test implements both.

**Five criticisms + defenses.**

1. **"Uniform-swing is a known bad assumption; Alberta's 2019→2023 swing was not uniform."**
   - **Defense:** Report two versions — uniform swing (simple baseline) and geographically-heterogeneous swing (parametrised on 2015→2019→2023 observed regional-swing differentials). Alberta's geographic-swing patterns are themselves stable (urban NDP swings larger than rural UCP swings), so the heterogeneous-swing version extends rather than replaces the uniform version.

2. **"The 0.40–0.60 vote-share range is arbitrary."**
   - **Defense:** 338Canada's Alberta model has produced values in this range in every poll since 2019; values outside are extrapolations. Report the sensitivity separately if reviewers want extrapolation.

3. **"The future is uncertain, so durability testing is speculation."**
   - **Defense:** Durability is the statutory question. Commissions draw boundaries for the *future* cycle; the test asks whether the drawings are partisan-neutral under *any plausible future*, not whether they predict the future. The §4.1.4 sunset clause does not apply — this is not a DPG-dependent test.

4. **"This is just iterating §5.2.3 through more elections."**
   - **Defense:** §5.2.3 uses three elections + one poll (four empirical points). Durability uses 11 synthetic points spanning the plausible range. The synthetic points probe specifically the interactions between map design and the intermediate vote shares the empirical points don't cover (0.45, 0.47, 0.51, 0.53) — the most politically relevant range.

5. **"If the asymmetry is stable across the full range, that means the map is partisan in the strongest sense, but if it varies, your finding is noise."**
   - **Defense:** Both outcomes are legitimate findings. A cross-scenario-stable asymmetry is evidence of a durable partisan structure. A swing-dependent asymmetry is evidence that the partisan effect is *scenario-contingent* — which the paper would report as such. Either way, the durability test adds information.

**Discriminant validity.** Not redundant with §5.2.3 (empirical cross-election). Not redundant with §5.2.6 marginal-seats (which names specific EDs without aggregating across the swing space).

**Implementation.** Reuse `packing_cracking_analysis.py` machinery; loop over 11 scenarios. **Effort: 3 days** (most code exists).

**Status.** Scoped, not executed. **Recommendation: queue after #2.1 and #2.2** — lower value than the coupling test because the existing §5.2.3 cross-election test covers most of the defensibility need. Execute if a reviewer specifically asks for durability.

### 2.4 Compactness-weighted partisan bias

**Definition.** Given per-ED Polsby-Popper compactness $PP_i$, define per-ED weight

$$w_i = \max\left(0, 1 - \frac{PP_i}{\text{median}(PP_{\text{all EDs}})}\right)$$

(so below-median-compactness districts get weight in [0, 1]; above-median get weight 0). Compactness-weighted efficiency gap:

$$\text{EG}_{cw} = \frac{\sum_i w_i \cdot (W_i^{\text{NDP}} - W_i^{\text{UCP}})}{\sum_i w_i \cdot N_i}$$

Compare to the unweighted EG. Report the ratio $\text{EG}_{cw} / \text{EG}$ — if > 1, the partisan effect is concentrated in irregular districts; if ≈ 1, it is distributed uniformly; if < 1, it is concentrated in regular districts.

**Phenomenon mapped.** Localisation of the partisan effect. A map with a small overall EG but a large $\text{EG}_{cw}$ has its partisan asymmetry concentrated in the few low-compactness EDs — the districts where commissioner drawing discretion is highest. This is specifically targeted at distinguishing drawing-attributable partisan effect from whole-map geographic-structure effect.

**Literature basis.** Polsby & Popper (1991) introduce compactness as a proxy for drawing discretion. Chen & Rodden (2013) establish that compactness correlates with partisan-bias-attributable-to-drawing. Barnes and Solomon (2021) caution that naive compactness measures can be gamed; the weighting scheme here uses a relative (within-map) comparison that resists gaming.

**Five criticisms + defenses.**

1. **"Weighting scheme is arbitrary (why median, why linear)."**
   - **Defense:** Report sensitivity to weight choice. Report variants: quartile-based weights, decile-based weights, continuous weights. Consistency across schemes is the reportable finding.

2. **"Compactness is perimeter-dependent and the paper admits ±500m tracing uncertainty on Tier C."**
   - **Defense:** Restrict the test to Tier A/B EDs where compactness is shapefile-grade or OSM-snap precision. A Tier-C-inclusive version waits on official disclosure / official shapefiles.

3. **"This favours the majority by construction (its hybrids are swept-calibrated)."**
   - **Defense:** The weighting uses *within-map median*, not a fixed threshold. Both maps have their own Tier-C-dominated tail; the within-map relative weighting is symmetric.

4. **"Low-compactness can be natural (rural districts are large and non-compact by necessity)."**
   - **Defense:** Separate rural vs urban EDs; apply the weighting within each class. A cross-class finding is what the test is designed to detect (a city ED with unusually low compactness flags a drawing choice, not geography).

5. **"Correlation ≠ causation. Compact districts can be gerrymandered too."**
   - **Defense:** The test is not a claim that low compactness = gerrymander. It is a claim that the *partisan signal* concentrated in low-compactness districts is evidence the drawing was what produced the signal. A high $\text{EG}_{cw} / \text{EG}$ ratio is compatible with: (a) drawing-attributable partisan effect, (b) natural clustering of low-compactness + heterogeneous-voters districts, (c) random noise. Chen-Rodden decomposition (test #5) helps separate (a) from (b).

**Discriminant validity.** Not redundant with C1/C2 compactness (which reports compactness per se, not partisan weighting) or B2 EG (which is uniform-weighted). The weighted version specifically identifies whether the partisan signal is localised.

**Implementation.** Requires per-ED PP (blocked on Tier-C; Tier A/B available now). Weight computation + weighted-EG aggregation ~100 lines. **Effort: 2 days** for the Tier A/B version.

**Status.** Scoped, not executed (blocked partially on official disclosure for full coverage). **Recommendation: execute Tier A/B version** as a partial test now; queue full version for post-official disclosure.

### 2.5 Absolute-level Chen-Rodden decomposition

**Definition.** For each map $M \in \{2019, \text{Majority 2026}, \text{Minority 2026}\}$:

$$\text{Draw}_M = \text{EG}_M^{\text{actual}} - \text{EG}_{\text{neutral}}^{\text{median}}$$

where $\text{EG}_{\text{neutral}}^{\text{median}}$ is the median EG of the 100k-plan MCMC ensemble on the same Alberta substrate. $\text{Draw}_M$ is the *drawing-attributable* partisan effect; the ensemble median captures the *geography-attributable* effect.

Report $\text{Draw}$ for each map as a point estimate alongside the ensemble 5th/95th percentiles for the Draw distribution; then compare the *absolute* drawing contributions, not just the inter-map gap.

**Phenomenon mapped.** How much of each map's partisan lean is Alberta's geography versus its drawing? §5.2.5 answers this for the minority-vs-majority *gap* (100 % drawing, 0 % geography by construction). The absolute version answers it for each map separately.

**Literature basis.** Chen and Rodden (2013) introduce the geography-vs-drawing decomposition. Herschlag, Ravier, and Mattingly (2020) implement it for US states. This is a direct Canadian adaptation.

**Five criticisms + defenses.**

1. **"The ensemble-median baseline isn't privileged."**
   - **Defense:** Report the Draw value with the ensemble 5th/95th percentiles as error bars. A map's drawing component is in the tail if Draw sits outside the ensemble 5–95 range. Transparent about what the baseline means.

2. **"The MCMC ensemble is constrained (pop ±25 %, contiguity, ReCom). The 'geography' component reflects those constraints, not natural geography."**
   - **Defense:** Absolutely. The Draw component is *drawing beyond what the constraints force*. This is precisely what the decomposition measures. A cleaner name would be `Draw_unforced`.

3. **"The 100k ensemble has ESS 288–350 (now 648–783 with the 150k run, Issue #8). Not enough for a decimal percentile claim."**
   - **Defense:** Report Draw as a range (ensemble 5th–95th) rather than a point (ensemble median). The range is robust to the ESS downgrade already documented in §5.4.

4. **"This is Post-hoc — you computed the ensemble and then decomposed."**
   - **Defense:** The decomposition is pre-registered in the methods section; it would have been applied regardless of its numerical outcome. Chen-Rodden is a specific adaptation of an established framework, not a novel decomposition invented for this finding.

5. **"Either Draw_maj and Draw_min are both close to zero (no drawing effect, just natural geography) or they're both large (both maps are gerrymandered in different directions). The binary interpretation limits usefulness."**
   - **Defense:** Report three cases honestly. If both are close to zero, the minority-vs-majority gap in §5.2.5 is the only finding (the absolute level is structural). If Majority is close to zero and Minority is non-trivially displaced, that's the "minority is drawing beyond neutral" finding. If both are non-trivially displaced, that's "both are drawing in different ways" — a richer finding than the current paper's.

**Discriminant validity.** Explicitly complements §5.2.5's pairwise gap decomposition. Absolute-level is a distinct question that the pairwise version can't answer.

**Implementation.** Pure post-processing of `data/v0_1_mcmc_ensemble_percentiles_full_*.csv` and `data/v0_1_mcmc_real_map_scores_*.json`. ~50 lines. **Effort: 1 day.**

**Status.** Scoped, not executed. **Recommendation: execute next.** Highest value-to-effort ratio of the five; no new infrastructure needed; no dependencies on external data.

---

## 3. The dependency graph — does the structure already exist?

### 3.1 The claim the graph is trying to capture

A defensible audit is one where **every finding at the top has multiple independent evidential paths from the raw data at the bottom**. A graph representation exposes exactly where a finding survives a specific attack and where it has a single point of failure.

### 3.2 Does the current structure do this?

**Partially.** The audit has an implicit graph structure that can be read out of the existing artifacts:

- **Layer 0 (raw data).** `FROZEN_MANIFEST.md` enumerates every primary source.
- **Layer 1 (constructed data).** `data/*.csv`, `data/*.gpkg`, MCMC sample files.
- **Layer 2 (per-ED metrics).** Scripts in `analysis/scripts/`, results in per-ED CSV.
- **Layer 3 (synthesis).** §5.1 through §5.9 of the monograph.
- **Layer 4 (defensibility).** §6 discussion + §4.1 integrity framework.

Each layer has a **forward/backward dependency header** in many analysis scripts. Examples in the repo: the script `phase_4bcdef_execution.py` lists its backward dependencies (input data paths) and forward dependencies (downstream writeups) explicitly.

But the dependency structure is not **machine-readable as a whole**. You can grep a script to see what it depends on; you cannot easily ask the repo "if `2023_results.xlsx` is questioned, what findings survive?" or "which findings share a dependency on the v0_2 DPG specifically?"

### 3.3 What's missing

A **formal DAG** of the whole audit as a single machine-readable artifact. Concretely:

1. **Nodes**: every raw-data source, every constructed data product, every test script, every reported finding.
2. **Edges**: directed dependency from source to consumer. Attributes: "required" (finding fails if edge breaks) vs "corroborating" (finding weakens but survives).
3. **Metadata per node**: test name, literature source, current robustness verdict, commits that landed it.
4. **Metadata per edge**: sensitivity (e.g., "survives ±500m DPG perturbation per §5.2.7 fifth layer").
5. **Queries**: "if node X is invalidated, which findings are affected?" "Which findings have only a single path from the raw data?" "Which findings have redundant paths?"

### 3.4 What's buildable

All of the above. Concretely:

1. A `analysis/methodology/audit_dependency_graph.json` file with nodes + edges + metadata. ~600 lines of JSON; derivable semi-automatically from the existing script headers + the 87 findings in the monograph.
2. A Graphviz DOT render (`.dot` file) produced by a small script that reads the JSON. Visualisation goes in `maps/dependency_graph.svg`.
3. A query script `analysis/scripts/dependency_query.py` that answers: "if I invalidate X, list all consequences."
4. An appendix in the methods paper (Issue #10) describing the DAG framework as a genuine novel contribution (I don't know of another public-interest audit that has published this).

**Effort**: 1–2 weeks of focused work to enumerate all nodes + edges carefully and build the query tooling. Not blocked on any external data. Good work for a follow-up contract or a graduate student.

### 3.5 Defensibility of the graph itself

A DAG representation is itself attackable. Three criticisms:

1. **"The graph is constructed by the same team that made the claims, so it's not an independent check."**
   - **Defense:** The graph exposes structure, not verdicts. A reviewer can inspect the graph and disagree with its edges; the graph makes that disagreement concrete. The current monograph buries dependencies in prose, making disagreement harder.

2. **"The graph's edges have subjective 'required vs corroborating' labels."**
   - **Defense:** Every edge carries a test — what happens to the downstream finding if the upstream node is deleted? The test is objective; the labelling reflects the test result.

3. **"Adding the graph is itself metric proliferation — yet another artifact to bless the audit."**
   - **Defense:** The graph is explanatory, not evaluative. It does not produce new numbers. It organises existing evidence.

### 3.6 Starter graph — the seven-layer §5.2.7 structure

Before the full DAG, the paper's §5.2.7 already implicitly encodes a mini-graph for the partisan-bias measurement:

```
Raw data: 2023 Statement of Vote + 2019 ED shapefile + commission populations + commission map PNGs
    ↓
Derived: crosswalks + DPG (v0_2 → v0_3 → v0_4 → v0_5)
    ↓
Attribution: crosswalk blending | centroid-in-polygon | MAUP-v1 | MAUP-v2 | DPG-perturbation | tier-aware perturbation | v0_5 MAUP rerun
    ↓
Metric: EG per map + asymmetry
    ↓
Synthesis: §5.2.7 conclusion = "cross-method disagreement, direction measurement-resolution-dependent, sunset-clause bound"
```

A reviewer attacking the crosswalk approach is answered by the spatial approach; attacking the spatial approach is answered by the DPG-perturbation CI; attacking the DPG is answered by the v0_5 second-substrate reading; attacking the whole apparatus is answered by the sunset clause. **This is the DAG structure the broader audit needs.**

---

## 4. Can we defend the whole apparatus?

### 4.1 The four kinds of validity

Measurement validity in quantitative social science has four canonical forms (Messick 1989; Clark and Watson 2019):

1. **Content validity.** The tests cover the construct's full domain.
2. **Convergent validity.** Independent measures of the same construct correlate.
3. **Discriminant validity.** Measures of different constructs don't correlate spuriously.
4. **Predictive / criterion validity.** The measures predict out-of-sample outcomes.

**The audit's posture on each:**

- **Content validity.** The six-dimension framing (A population + B partisan bias + C geographic + D procedural + signatures + cycle-lag) covers the canonical domains of redistricting audits per Altman-McDonald 2011. Three specific gaps: (a) community-of-interest at sub-CSD resolution (blocked on shapefiles), (b) racial/ethnic equity analysis (Canadian charter frames this differently and the audit defers to *Reference re Saskatchewan*), (c) incumbent-protection audit (not attempted).

- **Convergent validity.** Within the B-family, five metrics (EG/MM/Seats/Declination/MCMC-percentile) plus the four-seven spatial layers in §5.2.7 all measure partisan bias. They agree directionally in 90.5 % of Monte Carlo samples (§5.2.3) and disagree on mechanism (§5.2.4). The disagreement is *reported*, making convergent validity visible and auditable.

- **Discriminant validity.** The A-family and B-family and C-family measure distinct constructs; their findings can diverge (§5.1 population equality is UCP-favourable across all maps; §5.2 partisan bias is measurement-resolution-dependent; §5.8 geographic coherence has the 4.9× anchoring asymmetry). The audit does not claim these three findings collapse into one meta-finding.

- **Predictive / criterion validity.** The November 2026 committee's 91-seat map is the out-of-sample test the audit explicitly pre-registers against (Track C in `migration.md` / private `live_tasks.md`). Until that map is tabled, criterion validity is pending.

### 4.2 Defense in depth as the integrative strategy

The audit's defense is **not a single test carrying the weight**. It is:

- **Six independent dimensions** of evidence (§6 Discussion synthesis)
- **Multiple measurements per dimension** (seven layers for §5.2 alone)
- **Multiple references per measurement** (three elections + one poll for cross-vote robustness)
- **Explicit dis-confirming results reported** (2019 vote flips B2 sign; B6 declination disagrees with B2-B4; the §5.2.7 cross-method disagreement is itself reported)
- **Pre-registered falsifiability gates G0–G5** (§4.1.2) — named conditions for retraction
- **Sunset clause §4.1.4** — binding recompute commitment

A reviewer attacking any single test is answered by the others. The edifice is *over-determined on the structural-asymmetry finding* by design.

### 4.3 The honest limits

What the audit cannot defend:

- **Court-grade precision on polygon-derived metrics.** Without official shapefiles, compactness and DA-population overlays are structurally limited. The §4.1.4 sunset clause binds future recomputation.
- **Classical statistical significance on B-family magnitudes.** The 95 % CI crosses zero (§5.2.3). The reportable finding is directional at ~93 % confidence, not magnitude at 95 %.
- **Intent.** The audit documents structural asymmetry; it does not prove intent. `report_academic.md` §4.5 is explicit: structural findings are consistent with both intentional engineering and unlucky structural choice.
- **Constitutional conclusions.** The *Reference re Saskatchewan* 1991 effective-representation framework (Appendix F) is set out but not applied as a verdict. That is for counsel and courts.

### 4.4 The strongest single defensive argument

If we had to pick one: **the cross-method disagreement in §5.2.7 is itself the audit's most defensible finding**. We report that under different measurement resolutions the partisan-bias direction changes — and we do not collapse this disagreement into a false consensus. The disagreement is evidence that the audit is not cherry-picking; it is evidence that the available public data does not yet resolve the question, and the paper names what would resolve it (official disclosure, Issue #1).

A forensic audit that honestly reports "we don't yet know the direction with certainty, here are the boundaries of what we can say, here's what would resolve it" is stronger, not weaker, than an audit that picks a side.

---

## 5. Action items derivable from this reflection

| # | Action | Effort | Rationale |
|---|---|---|---|
| 1 | Execute absolute-level Chen-Rodden (§2.5) | 1 day | Highest value-to-effort; no dependencies |
| 2 | Execute neighbour-drain adjacency test (§2.1) | 2 days | Couples §5.3 packing + cracking findings |
| 3 | Execute compactness-weighted EG, Tier A/B only (§2.4) | 2 days | Partial test; strengthens §5.2 drawing attribution |
| 4 | Build the audit dependency DAG (§3.3–3.4) | 1–2 weeks | Genuine novel contribution; fits the methods paper (Issue #10) |
| 5 | Queue boundary-chain test (§2.2) | 4–6 days | Execute if a reviewer requests systematic-vs-ad-hoc evidence |
| 6 | Queue temporal-compound durability (§2.3) | 3 days | Lower priority; §5.2.3 already covers most of this |
| 7 | Retract unscoped-and-unexecuted tests from §6 of `test_selection_rationale.md` | 0.5 day | Remove soft-proliferation risk |
| 8 | File an Issue explicitly tracking each of items 1–4 | 0.5 day | Make the proposed tests accountable or droppable |

Items 1, 2, and 3 could be executed in one batch — combined effort ~5 days. Item 4 is the big investment that would strengthen the methods paper significantly.

---

## 6. Bottom line

**The apparatus is defensible as it stands.** It meets the five criteria separating genuine convergent validity from metric proliferation. Its weakest exposure (§5.2.7 multi-layer reporting) is defended by the explicit disclosure that the layers disagree by design.

**The apparatus can be strengthened further.** The five combined tests in §2 above each carry their own defense; at least three should be executed as planned to close the soft-proliferation gap. The DAG framework in §3 is a novel contribution that fits the methods paper well.

**The apparatus cannot be defended against its true structural limit** — the absence of official 2026 shapefiles. That limit is honestly reported via the §4.1.4 sunset clause and the data request in Issue #1. No internal methodology can substitute for authoritative data; what the audit can do is make its dependencies visible enough that the limit is the *only* thing a reviewer can attack.

That is the strongest position a public-interest audit can occupy.
