---
name: Test selection rationale — why these tests, not others; criticisms + defenses; improvements made + still possible
description: A methodological reflection on the audit's test battery. Answers: why these specific tests, what their criticisms are, how we defend against them, what we've already improved, and what combined or novel tests (drain effects, boundary-chain analyses) could add. Companion to the empirical paper extraction (Issue #11).
type: methodology
---

# Test selection rationale — why these tests, not others

**Purpose.** This file is a methodological reflection on the audit's test battery. It is written for reviewers asking why the audit chose the specific tests it ran rather than others, how those choices defend against standard criticisms, what improvements have already landed in response to red-team feedback, and what combined or novel tests could strengthen future work. It is NOT a new empirical result; it reorganises material that is scattered across §§2, 4, 5, 6 of the monograph and the analysis/red_team/ subfolder.

## 1. What the test battery actually is

Five families of tests, each answering a different question. The ladder below shows what the audit reports and where each test sits in the code.

### A-family — Population equality (§5.1)

| Test | What it measures | Source | Script |
|---|---|---|---|
| A1 | Median Absolute Deviation (MAD) from provincial quota | commission per-ED populations | `electoral_forensics_population.py` |
| A2 | Calgary geographic-zone asymmetry (urban-core vs suburban-ring) | two classification rules | same |
| A2b | Urban-rural regional breakdown (Calgary / Edmonton / Rest) | commission per-ED populations | same |
| A3 | s.15(2) special-rural eligibility audit | Act §15(2) criteria | same |

### B-family — Partisan bias (§5.2)

| Test | What it measures | Source | Script |
|---|---|---|---|
| B1 | Vote-distribution histogram across 10 margin bins | descriptive | `v0_2_packing_cracking_analysis.py` |
| B2 | Efficiency Gap (EG) — wasted-vote asymmetry | Stephanopoulos & McGhee 2014, 2015 | same |
| B3 | Mean-median gap — distributional skew | McDonald & Best 2015 | same |
| B4 | Seats-at-50/50 under uniform swing | Gelman & King 1994 (via Grofman 1983) | same |
| B5 | MCMC neutral-ensemble outlier percentile | ReCom (DeFord, Duchin, Solomon 2021) | `v0_1_mcmc_ensemble.py`, `_100k`, `_multichain_ensemble.py` |
| B6 | Declination — winning-district-margin angle | Warrington 2018, 2019 | embedded in `v0_2_packing_cracking_analysis.py` |

### C-family — Geographic coherence (§5.8)

| Test | What it measures | Source | Script |
|---|---|---|---|
| C1 | Polsby-Popper compactness | Polsby & Popper 1991 | `v0_1_approximate_shape_analysis.py` (Tier A/B only; Tier C blocked) |
| C2 | Reock compactness | Reock 1961 | same |
| C3 | Visual anomalies (chair-flagged) | commission chair's own §5 | visual inspection + Appendix E parse |
| C4 | Community-of-interest splits (CSD overlay) | Track H | `v0_1_csd_community_splits.py` |
| C5 | Municipal-boundary anchoring (v0_4) + DA-boundary anchoring (v0_5) | StatsCan CSDs + DAs | `v0_1_municipal_anchoring.py`, `v0_1_da_boundary_anchoring.py` |

### D-family — Procedural / legal defensibility (§5.9 + D1–D10)

| Test | What it measures | Source |
|---|---|---|
| D1 | Evidentiary chain (primary source + archive) | `FROZEN_MANIFEST.md` |
| D2 | Attribution accuracy (verbatim quotations) | commission text |
| D3 | Individual-actor characterisation (fair comment) | *Grant v. Torstar*; *WIC Radio* |
| D4 | Methodology reproducibility | every script has `python -c` one-line rerun |
| D5 | Data provenance | `FROZEN_MANIFEST.md` + `analysis/methodology/v0_1_commission_source_provenance.md` |
| D6 | Privilege / scope (fact vs opinion vs allegation) | labelled throughout |
| D7 | Conflict of interest (author standing) | Author Disclosure + `analysis/reports/v0_1_bias_audit.md` |
| D8 | Copyright / fair dealing | Copyright Act s. 29.1 |
| D9 | PII / confidentiality | no PII |
| D10 | Time-stamped falsifiable claims | OSF pre-registration + git log |

### Signature tests (§5.3)

| Test | What it detects | Criterion |
|---|---|---|
| Packing (P) | Disproportionate losing-party voter concentration | Calgary Zone A/B gap ≥ 10 % |
| Cracking (C) | Disproportionate losing-party fragmentation | Target city split across ≥ 4 EDs |
| Engineered boundary (E) | Statutory threshold met via uninhabited territory | s.15(2) criterion satisfied only via park/reserve extension |

## 2. Why these tests and not others

### Why the B-family: the EG-centric tradition

**Stephanopoulos & McGhee 2014/2015 on the Efficiency Gap** is the most-cited single test in the post-2010 US redistricting-law literature. It was briefed to the Supreme Court in *Gill v. Whitford* (vacated on standing, 2018). Using it makes the audit directly comparable to roughly a decade of US peer-reviewed work and to *Reference re Saskatchewan* (1991) -era Canadian frameworks that absorb the same concepts through comparative law.

**McDonald & Best 2015 on mean-median** is the natural complement: where EG measures wasted-vote asymmetry, MM measures distributional skew. Together they catch different gerrymander patterns (blowouts vs many-narrow-losses).

**Gelman & King 1994 (via B4 seats-at-50/50)** adds the Bayesian symmetry tradition, which is specifically the test used in *Davis v. Bandemer* (1986) and is the test most courts have found comprehensible.

**Warrington 2018 on declination** was added specifically because Warrington (2019) documents that declination and EG disagree on a non-trivial fraction of US-state plans. Running both is the Katz-King-Rosenblatt 2020 "consistency across metrics" discipline applied to this audit.

**DeFord-Duchin-Solomon 2021 (B5 MCMC)** is the MGGG lawsuit-grade standard. Without an MCMC baseline, there is no way to distinguish "unusual map" from "unusual-for-Alberta-geography map" (the Chen-Rodden natural-packing issue).

### Why the A-family: the Canadian-charter tradition

*Reference re Saskatchewan* (1991) establishes that effective representation under s.3 of the Charter requires more than pure population equality — it requires attention to "community of interest," "community of identity," and "geography" (the famous Lamer formulation). The A-family tests translate this principle into measurable quantities: A1 is the US-style dispersion measure; A2 operationalises Calgary-zone-equality (the most contested Canadian-specific claim); A3 is the statutory §15(2) exception test.

### Why C4 + C5 (community-of-interest and boundary anchoring) specifically

Community-of-interest is the hardest Canadian-charter criterion to operationalise. Pure perimeter-anchoring (C5 municipal+DA) is the cleanest measurable proxy: Canadian commissions have historically preserved community-of-interest by snapping boundaries to municipal edges where population allows. A map that anchors 71 % to municipal edges is doing what commissions have historically done; a map that anchors 14.5 % is not.

### Tests we did NOT run, and why

| Test considered | Why not run |
|---|---|
| **Bonferroni / Benjamini-Hochberg FWER correction** | The audit frame is "consistency across correlated dimensions" (Katz-King-Rosenblatt 2020), not "count of independent significance claims." Applying FWER to a correlated-dimension frame over-corrects on the null side. Documented in §6 Discussion. |
| **Wang 2014 partisan-symmetry test** | Overlaps substantially with B4 seats-at-50/50. Including it would be double-counting under Altman-McDonald 2011's consistency discipline. |
| **Niemi-Deegan structural measures** | Mostly superseded by the EG-family + MCMC ensembles. Not widely cited in post-2010 literature. |
| **DW-NOMINATE / ideological-polarisation measures** | Applies to members' voting behaviour, not map-partisan-effect. Out of scope. |
| **CNN / gerrymander-detection deep-learning models** | Would require Canadian-specific training data that does not exist at scale. Would introduce unaudible black-box decisions. |
| **Bayesian posterior updating** (hierarchical model on districts) | Would require specifying priors. The audit's approach is frequentist-adjacent (consistency-across-metrics) + pre-registered, which is more legally defensible than a Bayesian frame where the prior itself is contestable. |
| **Per-ED vote-prediction models** (Random Forest on demographic covariates) | Overfits on n=87 districts. Would introduce predictions as data into a prediction-based assessment — circular. |
| **Redistricting-alternatives MCMC at 2026 seed** (seeded on the commission's own geometry rather than 2019) | Blocked on official 2026 shapefiles. Once Option D FOIP responds, this is the single most-requested follow-up. |
| **Natural-language sentiment analysis on public submissions** | Out of scope for the empirical audit; potentially a follow-up for the policy paper (Issue #12). |
| **Voter-file-level analysis** (individual voter records) | Not publicly available in Canada; privacy-blocked. |
| **Historical comparison with 2010, 2017 Alberta commission maps** | Tier-B comparison structurally (different statutory bases, different data vintages). Cross-election rural baseline (§3.3) is the reduced-form version. |

## 3. Criticisms of the chosen tests + defenses

For each B-family test a hostile reviewer can mount a specific attack. Each has a specific counter.

### B2 Efficiency Gap

- **Attack A.** "Your 95 % CI crosses zero (−2.74 to +0.60 pp)." Classical significance not defensible.
- **Defense A.** Acknowledged in §5.2.3. Directional consistency is the reportable finding at 93 % confidence; magnitude is the separate weaker claim.

- **Attack B.** "The 7 % EG threshold from Stephanopoulos-McGhee is not a court standard. SCOTUS vacated *Gill v. Whitford*."
- **Defense B.** Explicitly acknowledged in the abstract, §2, §5.2.1, and Appendix D.1 (T0 legal fix). The threshold is cited as an academic-literature proposal, not a judicial holding.

- **Attack C.** "EG is sensitive to boundary choices about what counts as a 'wasted' vote."
- **Defense C.** Our B4 seats-at-50/50 test uses a different wasted-vote convention, and B6 declination uses none at all. Convergence across the three is the reportable finding; disagreement on one metric triggers the §5.2.4 cross-metric analysis.

### B3 Mean-median

- **Attack.** "Mean-median assumes a symmetric reference distribution. Alberta's distribution has a long rural UCP tail."
- **Defense.** The asymmetry is acknowledged in §4.3 and is exactly the Chen-Rodden natural-packing mechanism the audit validates. Under the mechanism correction (§5.2.5), MM's sign matches B2; B2 itself is not dispositive of the audit's headline.

### B4 Seats-at-50/50 uniform swing

- **Attack.** "Uniform swing assumption fails when regional swings differ. The 2019→2023 Alberta swing was not uniform."
- **Defense.** Documented as a limitation in §4.3. The marginal-seats analysis (§5.2.6) uses the same assumption because it is the only tractable counterfactual; its result is reported as order-of-magnitude, not deterministic.

### B5 MCMC ensemble

- **Attack.** "Your 100k single-chain has n_eff ≈ 150. That's not enough for a p100 tail claim."
- **Defense.** T1 remediation landed the explicit ESS tail-downgrade: p100 claims are bounded to p95.35 at the chain's effective precision. T3.1 multi-chain ReCom (50k × 3 seeds) delivered R-hat 1.013–1.017 (strict convergence) with combined ESS 288–350 (still under 1000 MGGG target; 150k × 3 run in flight at Issue #8).

### B6 Declination

- **Attack.** "Declination disagrees with EG — you can't have it both ways."
- **Defense.** Warrington 2019 documents this kind of disagreement as expected on roughly a third of US-state plans. §5.2.4 reads the disagreement as consistent with a narrow-margin-loss packing pattern (our signal for tight-packing gerrymanders), not as metric failure. All four metrics agree on the presence of asymmetry; they disagree on its mechanism.

### MAUP area-weighted attribution

- **Attack.** "Area-weighting introduces MAUP artifacts because the base grid is arbitrary."
- **Defense.** The conservation gate on each perturbation realisation ensures per-VA vote totals are preserved. The four-layer reporting pattern (§5.2.7) surfaces cross-method disagreement rather than hiding it; MAUP-v1 vs MAUP-v2 specifically isolates transcription-overlap artifacts from genuine signal.

### DPG perimeter tracing

- **Attack.** "You traced the commission's maps from 600-DPI thumbnails. Your polygons are wrong."
- **Defense.** Precision ladder: v0_2 topology-clean → v0_3 pop-calibrated sweep → v0_4 municipal-anchored → v0_5 DA-anchored. The §5.8.5 audit shows 79.6 % of majority perimeter now sits at ±1 m on DA / municipal edges. The DPG-perturbation CI (±500 m flat, N=200) has 90 % CI [+1.69, +7.67] pp on asymmetry with zero samples crossing zero — the spatial direction is robust at the conservative ceiling; tier-aware (Issue #2 v2) will narrow this further.

### Cross-election sign reversal

- **Attack.** "Under 2019 votes, your asymmetry flips. Your finding is not about the maps, it's about 2023 votes."
- **Defense.** Reported as a property of the finding, not a defect. The boundary effect is a voter-geography interaction; we document that interaction across 2015, 2019, 2023 + April 2026 polling. §3.5 characterises when the direction holds (2020s-era political geography) and when it doesn't (pre-UCP-era electorates). This is more honest than a single-election claim.

## 4. Improvements already landed in this cycle

Counted by commit hash on `master`:

- **T0 (d25e659)** — DPG framework + sunset clause + Phase-A legal fixes (Gill, Rizzo, chair softening)
- **T1 (a62eb53)** — compactness uncertainty bands + MCMC ESS downgrade + Core/Margin VA partition + sign-convention glossary + Airdrie pixel-extraction reframe
- **T2 (de7c48e)** — multiple-comparison posture paragraph + int()/hashlib verified
- **T3.1 MCMC multi-chain (054ec00)** — R-hat 1.013–1.017 convergence proof; combined ESS 288–350
- **T3.2 Chen-Rodden decomposition (3c7385f)** — formal 100 %-drawing, 0 %-geography identity for the minority-majority gap
- **T3.3 Canadian base-rate recalibration (same)** — removed Alberta 2026 anchor circularity; ordinal ranking + p67 (n=6)
- **Topology cleanup (452f841, Issue A)** — resolved 19,487 km² of inter-ED polygon overlap; MAUP-v2 run on clean geometry
- **Municipal anchoring (2e6c351, Issue #4)** — 71.0 % maj / 14.5 % min to CSD edges; 4.9× asymmetry as independent §5.8 dimension
- **DA-boundary anchoring (f319960)** — +7.7 pp maj / +6.6 pp min to DA edges; 5.1× asymmetry ratio preserved
- **DPG-perturbation CI (21df0af, Issue #2)** — 90 % CI [+1.69, +7.67] pp, 200 of 200 samples positive
- **Pop-calibrated sweep on 39 hybrids (bf6edf2, Issue #3)** — 35 of 39 converged; Phase 4F fails 84/87 → 67/69
- **Cycle-lag commentary (a85308a)** — three-vintage sandwich + forward-modelling commentary

## 5. Improvements we can still make

Ordered by value / effort:

1. **Combined test: adjacency-chain packing + cracking.** *See §6 below.* The single highest-value novel test we haven't run.

2. **Multi-chain MCMC at ESS > 1000** (Issue #8, in flight). When the 150k × 3 run completes, the tail-percentile claims move from "policy-comparison grade" to "MGGG lawsuit grade."

3. **Tier-aware DPG-perturbation CI** (Issue #2 v2 subagent, in flight). σ per-polygon by `canon_source` — expect tighter than the flat-±500m v1 CI.

4. **Bayesian falsifiability hooks** on each headline number. The sunset clause handles DPG-dependent claims; a complementary Bayesian-update hook would state "if official shapefiles produce X direction, the finding is retracted" explicitly per metric.

5. **Synthetic-gerrymander simulation studies.** Generate Alberta-geography synthetic plans with known partisan properties; run the full test battery. Validate that the battery detects the synthetic gerrymanders at the expected signal strength and rejects neutral maps.

6. **Sub-ED clustering analysis.** Are the minority's 21 Tier-C hybrids clustered in specific regions (Calgary metropolitan? Edmonton ring?), or distributed? Pattern suggests whether the hybridisation is systematic or ad-hoc.

7. **Cross-commissioner attribution.** The commission had two dissenting commissioners (chair Miller and one other who signed the minority report). Can we identify which Tier-C hybrids came from which commissioner? If the minority's 4-way Airdrie split was authored by a single commissioner, that's a different story than if it emerged from consensus.

8. **Boundary-chain test** (see §6).

9. **Federal-boundary correlation.** Canadian federal ridings in Alberta redistribute on a different cycle; they provide an independent baseline. If the minority's ED boundaries are anti-correlated with federal riding boundaries (i.e., split where federal boundaries don't), that's structural evidence the minority is drawing *against* a natural partition.

10. **Full 338Canada back-test across 2020-2026.** The current 77-snapshot historical stability probe (§5.2.3) tests direction-robustness. A tighter test: refit the minority → 2026 crosswalk each month and measure how the asymmetry number drifts with changing voter geography.

11. **Formal falsifiability registration at OSF amendment.** Each headline number gets a named falsifier on OSF, dated. Current pre-registration has this at the dimension level but not per-metric.

## 6. Combined tests (novel)

This is the single most-requested item from the methodological reflection, and where the audit could add genuine value to the literature.

### 6.1 Neighbour-drain adjacency test (the user's example)

**Motivation.** Packing concentrates a losing party into a few districts; cracking distributes the losing party's votes thinly enough that it loses each of many districts. These work together: a "packed" district drains adjacent areas, and the drained areas become "cracked." Existing tests catch packing (§5.3.1 Calgary Zone A) and cracking (§5.3.2 Airdrie four-way) as separate findings. A combined test would measure the **adjacency-chain pattern**: if ED X is packed (party Y surplus-vote rate ≥ threshold), are X's adjacent EDs cracked (party Y margin ≤ threshold, despite X being right next door)?

**Operational definition.** For each ED X, compute surplus-vote rate for the losing party. For each adjacent ED Y, compute party-Y margin. Define the pair (X, Y) as an **adjacency-chain signal** if X's surplus rate ≥ 15 % AND Y's party-Y share is within 5 pp of the losing threshold. Count such (X, Y) pairs per map. Higher count = more systematic packing-cracking coupling.

**Refinement (PO critique 2026-04-24).** Rather than single-point threshold counts, **visualise the full 2D phase space**: x-axis = $s_X$ (losing party surplus rate in X), y-axis = $m_Y$ (losing party margin in Y). Plot every adjacent pair as a point, coloured by map (majority vs minority). A neutral map produces a uniform-random scatter; a gerrymandered map produces a hot spot in the upper-left quadrant ($s_X > 0.15$, $m_Y < 0.05$). This pre-empts the "arbitrary threshold" critique because the heat-map shows whether *any* threshold separates the two maps, not just the specific $0.15 / 0.05$ chosen in the definition. The "so-what" framing for the paper: the chain signature proves the Airdrie four-way split is not an isolated incident but a repeatable *design pattern* applied across the minority map.

**Status.** Not yet implemented. Straightforward; ~2 days of work including the 2D heat-map visualisation. Would strengthen the §5.3 signature analysis significantly.

### 6.2 Boundary-chain test (systemic vs ad-hoc)

**Motivation.** Individual boundaries can look defensible on their own ("this river is the natural boundary") while the chain of adjacent boundaries systematically favours one party. If the minority's four Airdrie boundaries each look defensible, but the four together partition Airdrie in a way that every piece lands in a larger UCP-leaning rural ED, that's a boundary-chain signature.

**Operational definition.** Identify all boundary chains of 3+ consecutive ED boundaries passing through a single city or municipal area. For each chain, compute the partisan outcome (NDP seats won) under 2023 votes + an alternative partition (same city, different commissioner-proposed split). If the minority's chain systematically produces NDP-disadvantageous outcomes across 3+ chains, that's a pattern, not an accident.

**Refinement (PO critique 2026-04-24).** Use the 2019 partition as the null-hypothesis baseline as planned, but **control for population growth**: if a chain boundary shifted significantly because a Calgary-ring suburb grew 20 % since 2021, the shift is demographic necessity rather than partisan choice. Operational control: for each chain boundary that moved relative to 2019, compute the population the new boundary would have under the 2019 partition shape versus the commission's new partition; if the 2019 shape exceeds the ±25 % quota band for either side at 2024 population, the boundary was *forced* to move, and the chain-asymmetry contribution is flagged as demographic-compelled rather than partisan-chosen. **Visualisation:** a "Chain Map" overlay showing the minority's chain boundaries in red, the majority's in orange, and the 2019 boundaries in blue would be the single most impactful graphic in the paper — readers can see the chain pattern at a glance.

**Status.** Not yet implemented. ~4–6 days including population-growth controls and chain-map visualisation. Would catch systematic gerrymander patterns that per-boundary tests miss.

### 6.3 Temporal-compound durability test

**Motivation.** A map can be neutral under 2023 votes but become gerrymanderous under realistic 5-year swings. Durability testing: run the full B-family against each projected swing scenario for 2027, 2031, 2035; report the worst-case asymmetry across the cycle.

**Operational definition.** Use 338Canada's uniform-swing model to project provincial vote shares for scenarios spanning UCP 40/60 to 60/40. For each scenario, recompute B2-B4 asymmetry. Report the maximum-over-scenarios asymmetry.

**Refinement (PO critique 2026-04-24) — pivot to geographic-heterogeneous swing as PRIMARY.** Alberta's swings are demonstrably non-uniform; the "Donut" effect (urban NDP vs rural UCP) means a 5 pp provincial swing historically manifests as ~10 pp in Calgary and ~1 pp in rural south. Use the 2015→2019→2023 observed regional-swing pattern to parametrise a *geographically-heterogeneous* swing function, then sweep the provincial aggregate across the 0.40–0.60 range with the regional structure preserved at each point. **The specific finding to watch for is a "responsiveness gerrymander"**: a map that remains neutral-to-UCP-favourable at UCP-plus-10 leads but becomes a "fortress" (unresponsive to additional swing, NDP cannot gain seats through extra votes) once the NDP crosses ~48 %. A responsiveness gerrymander is constitutionally suspect under *Reference re Saskatchewan* (1991) because it breaks the seat-vote responsiveness that effective representation requires. Uniform-swing results kept as a robustness baseline; heterogeneous-swing is the primary.

**Status.** Partial — §5.2.6 already has a marginal-seat analysis. The systematic durability test would extend that to the full B-family and aggregate over the whole swing space, with geographic heterogeneity as primary.

### 6.4 Compactness-weighted partisan bias

**Motivation.** Low-compactness EDs are more likely to be gerrymandered. Weighting each ED's contribution to the map's EG by its Polsby-Popper distance from the map median gives a "compactness-weighted EG" that isolates the partisan effect in irregular EDs from the partisan effect in regular ones.

**Operational definition.** $\text{EG}_{cw} = \sum_i w_i \cdot \text{EG}_i$ where $w_i = (1 - PP_i / \text{median}(PP))$, bounded to [0, 1]. High $\text{EG}_{cw}$ means the partisan asymmetry is concentrated in the map's least-compact districts.

**Refinement (PO critique 2026-04-24).** Tier-C Polsby-Popper is blocked on FOIP, but **convex-hull ratio and Reock scores are both computable from the vertex data we already have** in the v0_2 / v0_3 / v0_4 / v0_5 canonical shapefiles. Use these as Tier-C proxies while waiting for FOIP: $\text{Reock}_i = \text{area}(i) / \text{area}(\text{min-enclosing-circle}(i))$; $\text{ConvexHull}_i = \text{area}(i) / \text{area}(\text{convex-hull}(i))$. A compactness-weighted EG using Reock or convex-hull ratios is partially defensible now and fully defensible once Polsby-Popper becomes available. **Framing for the paper**: "The bias is not coming from the districts that look like squares; it is coming from the districts that look like dragons." That one sentence is the most difficult argument for a commission to defend, because the commission's own drawing discretion is proportional to polygon irregularity.

**Status.** Reock / convex-hull version implementable now. Polsby-Popper version blocked on Tier-C shapefiles (FOIP, Issue #1). Queued; executable under the refinement.

### 6.5 Combined Chen-Rodden + drawing decomposition (absolute-level)

**Motivation.** §5.2.5 validates Chen-Rodden direction + mechanism correction. §5.2.5 geography-vs-drawing decomposition shows the minority-vs-majority gap is 100 % drawing. Combining these: what fraction of the *absolute* minority partisan lean is natural-geography vs drawing? (Not the gap — the level.) Answer would calibrate the minority's gerrymander-relative-to-neutral-drawing claim.

**Operational definition.** $\text{Draw}_{min} = \text{EG}_{min, \text{actual}} - \text{EG}_{neutral, \text{median}}$. Similarly for the majority. Report both as "drawing-attributable" EG. If Majority drawing-attributable EG is 0 and Minority drawing-attributable EG is +2 pp, that's a clean story.

**Refinement (PO critique 2026-04-24) — this is the audit's most honest metric.** Acknowledging the ~−2.2 % structural EG floor that any Alberta map produces under 2023 votes *gains massive credibility*. It stops the audit from sounding partisan and starts making it sound like a geographer. **The intended headline**: *"The minority map does not just reflect Alberta's lopsided geography; it actively tips the scales by an additional 0.7 % through specific drawing choices."* That framing converts the decomposition from a technical result into a clear causal argument that reviewers can inspect and disagree with on specific grounds (the ensemble median, the substrate, the 90 % band) rather than on genre (is the audit partisan).

**Status.** Absolute-level version is a ~50-line extension of the existing `v0_1_chen_rodden_decomposition.py` script. **Recommendation: execute first among the five combined tests.** Highest value-to-effort ratio; no dependencies; produces a headline-grade result.

## 7. Defense-in-depth framing

The audit's overall epistemic posture is **defense in depth**: no single test is intended to be dispositive. Directional consistency across six independent dimensions is the inferential artefact. This is the Katz-King-Rosenblatt 2020 + Altman-McDonald 2011 discipline applied rigorously.

A reviewer attacking any individual test gets answered by the others:

- Attack B2's CI → B4's direction consistency and B6's mechanism-corroboration answer back
- Attack MAUP's topology → the crosswalk approach (no geometry) answers back
- Attack the MCMC's ESS → the multi-chain R-hat and the 10k-ensemble percentiles answer back
- Attack the DPG tracing → the population-calibrated sweep and municipal + DA anchoring answer back
- Attack the 2023 vote substrate → the cross-election 2019 + 2015 tests answer back (though they flip sign, which is reported)

This is the framing §6 Discussion documents and the §7 Limitations section hedges. The test battery is intentionally over-determined on the structural-asymmetry finding so that no reviewer can take out the whole edifice by attacking one pillar.

## 8. Relationship to other documents

- `report_academic.md §4` — the methods section that this reflection hangs off
- `report_academic.md §6` — the discussion where the multi-dimensional synthesis is argued
- `analysis/methodology/red_team_consolidated.md` — the 23-document red-team record this reflection inherits from
- `analysis/reports/v0_1_methods_paper_draft.md` — the companion methodology paper (Issue #10) that would formalise §§3-5 of this file for publication
