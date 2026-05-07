# Novel Methodological Contributions — Alberta 2025-26 Electoral Boundaries Audit

**Status:** Active reference. Updated 2026-05-07.
**Scope:** Three methodological contributions introduced by this audit that, to the authors' knowledge, have no direct precedent in the redistricting or forensic-audit literature.

Cross-ref: `analysis/reports/methods_paper_draft.md` (DPG standalone paper skeleton), `analysis/methodology/academic_literature_review.md` §9–9b (prior-art placement), `dpg_validation/dpg2_worklog.md` (pre-registration chain).

---

## 1. Derived Provisional Geometry (DPG) Framework

### What it is

A disciplined methodology for constructing, validating, and reporting electoral boundary analyses when official topological shapefiles have not been released. A DPG is a polygon dataset that approximates authoritative boundaries from: (a) commission-published maps (PNG/PDF), (b) prior-cycle authoritative shapefiles, (c) administrative overlays (municipal, dissemination-area, census), and (d) population-calibrated parametric inference against the commission's published per-ED population table.

### The problem it solves

Existing redistricting-analysis frameworks (MGGG, Chen & Rodden 2013, Stephanopoulos & McGhee 2015) assume official shapefiles as input. They do not specify how an audit should publish defensibly when those shapefiles are unavailable. The gap between a commission's final report and release of authoritative geometry is months to years in most Canadian jurisdictions. No prior methodology formalises this case.

### The specific contributions

**i. Two-error-mode disclosure.** The DPG framework separates *perimeter-mode uncertainty* (boundary localisation error, ±100 m–1 km depending on source; affects compactness and fine-grained vote attribution) from *area-mode uncertainty* (whole-polygon-territory mismatch, Tier-dependent; affects population overlays and area-weighted vote attribution). The existing literature reports a single "geometric error" bar that conflates these two structurally different failure modes.

**ii. Source-tier provenance.** Each DPG row carries a `canon_source` value from a defined hierarchy: `da-anchored` / `municipal-anchored` (Tier A, shapefile-grade accuracy), `osm-municipal-buffered` / `sweep` (Tier B, high confidence), `v7` (Tier C, visually transcribed). Downstream algorithms — overlap resolution, edge snapping, four-layer reporting — consume this metadata deterministically.

**iii. Four-phase DPG tessellation pipeline.** Independently-traced polygon sources do not tile; they overlap and leave gaps. The pipeline resolves this in four phases: (1) precedence-based overlap resolution with anti-erasure clamp; (2) tier-ordered edge snapping using `shapely.snap()` with auto-revert on >5% area distortion; (3) spatial-index gap-fill assigning residual territory to the longest-shared-boundary neighbour; (4) 1 m precision pass closing floating-point artefacts via multi-threaded snapping. Phase order is fixed; running them out of order propagates errors into the committed union. Code: `analysis/scripts/dpg_perfecter.py`.

**iv. Nested-polygon ownership inversion.** Standard polygon-overlap-resolution algorithms either erase the smaller polygon or flag the case as unresolvable. For electoral GIS, erasing a legally distinct ED is not acceptable. When the overlap-resolution pass finds that one ED is ≥95% contained inside another, ownership inversion preserves the inner polygon by carving a hole in the outer ED rather than deleting the inner. The cartographic-conflation literature (Sester 2000; Saalfeld 1988) does not treat this case. In the Alberta dataset this resolves the Calgary-Falconridge-Conrich / Airdrie-East 141.9 km² nested overlap on the majority map.

**v. Programmatic alignment proof without reference polygons.** Standard ground-truth validation (intersection-over-union against an authoritative polygon set) is unavailable in the DPG posture. The audit introduces a point-based validation substitute: topology checks (ED count, residual overlap, coverage), city-centre landmark containment tests against Statistics Canada CSD representative points, and cross-plan area consistency. This validates that derived polygons are in the right place without requiring authoritative polygons to compare against.

**vi. Sunset clause as pre-registration commitment.** All DPG-dependent findings are published with a timestamped public obligation to re-run every analysis against official geometry within 48 hours of its release and to disclose any sign-flip or material magnitude change. This inverts the usual "caveated-final" posture into a falsifiable commitment. If the authors fail to honour it, that failure is itself publicly documented.

### Claim to novelty

> The DPG framework is, to the authors' knowledge, the first formalisation of forensic electoral auditing under geometry uncertainty. Specific novel elements: the two-error-mode distinction, tier-ordered edge snapping for electoral polygon tessellation, nested-polygon ownership inversion for electoral GIS, and the sunset clause as a pre-registration-style commitment applied to derived geometry rather than statistical analysis.

### Prior art this builds on

- MGGG redistricting tools (DeFord et al. 2021) — assume official shapefiles
- Chen & Rodden (2013) — simulation-based; assume official shapefiles
- Sester (2000); Saalfeld (1988) — cartographic conflation; do not address electoral polygon ownership inversion
- Duckham & Drummond (2000) — edge conflation; related but not tiered by provenance

### Pre-registration / documentation

- AsPredicted #289,449 — DPG v11 validation (thresholds pre-registered)
- Full paper skeleton: `analysis/reports/methods_paper_draft.md`

---

## 2. Neighbour-Drain

### What it is

A local pack-crack adjacency metric. An ED pair constitutes a Neighbour-Drain when: (a) one ED is *packed* — the losing party's share exceeds the winning margin by ≥ 15 pp — and (b) the adjacent ED is *cracked* — the winning party's margin is ≤ 5 pp — and (c) the losing party is the same in both. The packed ED drains the losing party's concentrated votes away from the cracked ED next door, where those votes could have been electorally decisive. A continuous intensity measure ΔPPS (packed-pair surplus) quantifies how much losing-party concentration the coupled pair represents.

### The problem it solves

Pack-and-crack has been described qualitatively since at least the 2010s and appears in the US redistricting litigation record (see *Gill v. Whitford*, 585 U.S. 2018; *Rucho v. Common Cause*, 588 U.S. 2019). The existing literature operationalises it at the map level (ensemble-based; e.g., Chen & Rodden 2013) or as a categorical description of specific EDs. No prior metric quantifies the *coupling* between adjacent packed and cracked EDs as a measurable, named signal at the ED-pair level.

### The specific contribution

Neighbour-Drain operationalises pack-and-crack as a local, paired, directional adjacency metric rather than a map-level count. It is:

- **Local** — computed on ED pairs, not map-wide; reveals which specific adjacencies drive the ensemble signal
- **Directional** — the drain flows from the packed ED (surplus concentration) to the cracked ED (margin suppression); the direction is identifiable from the data
- **Testable** — pre-registered null: if Neighbour-Drain is a real signal and not a labelling artefact, its intensity should not survive a label-shuffle permutation test on a neutral ensemble map set

Applied to Alberta 2026: the minority map produces 50% more Neighbour-Drain-eligible ED pairs than the majority under identical population constraints, concentrated in the Calgary suburban ring.

### Claim to novelty

> "Neighbour-Drain" is coined in this audit (AsPredicted #289,451, 2026-05-06). A targeted search of the redistricting literature found no established named measure for the specific adjacency coupling described above. The term and its continuous intensity variant (ΔPPS) are proposed as a contribution to the pack-crack operationalisation literature, pending fuller prior-art review.

### Prior art this builds on

- Informal "pack-and-crack" terminology in US litigation and commentary
- "Pizza-slice" / "hub-and-spoke" urban district descriptions (Rodden 2019; Chen & Rodden 2013)
- McGhee (2014/2015) efficiency gap — map-level complement to the pair-level Neighbour-Drain
- Urban Hybridization count (this audit) — map-level predecessor to the pair-level metric

### Pre-registration

- AsPredicted #289,451 — Neighbour-Drain label-shuffle null (pending execution)
- OSF: [r3zm7](https://osf.io/r3zm7/)

---

## 3. Swing-Zone Allocation Test (SZAT)

### What it is

A paired-map decomposition of the efficiency-gap difference that attributes the between-map partisan gap to specific boundary choices. A *swing zone* is any Voting Area whose centroid falls in a different Electoral Division under Map A than under Map B. Only swing zones carry the between-map difference; non-swing VAs produce identical EG contributions under both maps. SZAT score = Σ ΔEG(VA) across all swing zones, where ΔEG(VA) is the change in EG contribution produced by assigning that VA to the minority-map ED rather than the majority-map ED. Significance is tested against a permutation null in which each swing zone is independently assigned to either map's configuration with probability 0.5.

### The problem it solves

Existing ensemble methods (Chen & Rodden 2013; MGGG ReCom) answer: *is this map anomalous compared to neutral random draws?* Map-level EG (Stephanopoulos & McGhee 2015) answers: *how much partisan waste asymmetry does this map produce?* Neither answers: *which specific boundary decisions, between two real proposed maps, are responsible for the difference?* When a commission produces two competing proposals, the policy-relevant question is not just whether either map is anomalous, but whether the minority's specific deviations from the majority map serve a partisan purpose.

### The specific contribution

SZAT isolates the *causal boundary choices* — the swing zones — and tests whether their allocation is partisan-neutral under a well-specified null. It is:

- **Decomposable** — produces both a map-wide SZAT score and a VA-level delta that can be mapped spatially and summed by region or ED
- **Paired** — uses a real alternative map as its counterfactual, not an ensemble median; the counterfactual is therefore politically meaningful, not a neutral geometric average
- **Generalizable** — any two maps covering the same territory (majority vs minority; proposed vs enacted; proposed vs prior cycle) can be compared via SZAT; the proposed-vs-2019-baseline variant requires only one new spatial join

Applied to Alberta 2026: SZAT score = +0.039165 (p < 0.0001, two-tailed bootstrap N = 10,000, seed pre-committed at git hash d2aea42). The minority map's boundary choices increase NDP vote waste by 3.9 pp relative to the majority, with dominant contribution from Rest of Alberta (+0.015) and Edmonton (+0.008). The Canmore/RMH focal EDs — which motivated the test — contribute +0.006291, a meaningful share of the total given their geographic scale.

### Claim to novelty

> "Swing-Zone Allocation Test" and the term "swing zone" in this paired-map sense are introduced in this audit (AsPredicted #289,469, 2026-05-07). The decomposition of between-map EG differences to individual Voting Area boundary choices, and its permutation test, are novel to this audit. The closest prior work (Chen & Rodden 2013) decomposes EG into geography-versus-drawing components using an ensemble median as counterfactual; SZAT uses a specific alternative real map, producing a directional boundary-choice attribution rather than a geography-partitioned variance explanation.

### Prior art this builds on

- Stephanopoulos & McGhee (2015) — EG formula, sign convention, wasted-vote accounting
- Chen & Rodden (2013) — geography-vs-drawing decomposition (SZAT is the boundary-choice-level complement)
- Altman & McDonald (2011) — multi-criteria consistent-signals discipline (the approach SZAT uses when combining with ensemble results)
- The paired-comparison design is a standard statistical construct; SZAT applies it to the EG decomposition setting

### Pre-registration

- AsPredicted #289,469 — SZAT bootstrap null (filed 2026-05-07; results known at filing; seed pre-committed at d2aea42)

---

## 4. Two-Lane Forensic Scorecard

### What it is

A structured reporting framework that evaluates a proposed electoral map on two explicitly separated evidence tracks and requires both to be reported honestly even when they disagree:

- **Lane 1 — Partisan-bias magnitude.** Quantitative vote-data-dependent metrics: efficiency gap, partisan bias index, seats@50/50 simulation, MCMC ensemble percentile placement. Threshold calibrated to the jurisdiction's own electoral geography via neutral-draw ensemble rather than borrowed from US litigation defaults.
- **Lane 2 — Structural and procedural pattern.** Vote-data-independent signals: population distribution (MAD), municipal-boundary anchoring departure, community-of-interest treatment (city splits), geometric anomalies, commission-chair flags, rationale-failure analysis. These signals register engineering intent even when the EG magnitude remains sub-threshold.

The scorecard is pre-registered before any new map is drawn, applied to known-outcome maps as a calibration test, then re-applied prospectively to the target map without modification.

### The problem it solves

US redistricting litigation post-*Rucho v. Common Cause* (588 U.S. 684, 2019) demonstrated that partisan-bias magnitude alone — EG, partisan bias index, seats-votes responsiveness — is not a judicially manageable standard. Courts and commissions need a framework that can surface gerrymander signals even when the EG magnitude is sub-threshold, and that distinguishes intent signals from magnitude signals explicitly so that a sub-threshold Lane 1 result cannot be used to foreclose a Lane 2 finding.

Existing audit frameworks (MGGG redistricting tools; Chen & Rodden 2013; Stephanopoulos & McGhee 2015) are single-lane: they produce partisan-bias metrics or structural metrics, not an integrated two-lane verdict with explicit rules for how the lanes interact. No prior published audit framework specifies:

- that Lane 2 findings can stand as independent gerrymander evidence when Lane 1 is sub-threshold
- that sub-threshold Lane 1 is necessary but not sufficient for a clean verdict
- a pre-registered scorecard applied prospectively to a future map with a published null hypothesis

### Two-lane specific contributions

**i. Explicit lane separation with interaction rules.** The framework specifies in advance that Lane 1 and Lane 2 are independent evidentiary tracks. A Lane 1 sub-threshold result does not resolve Lane 2; a Lane 2 clean result does not resolve Lane 1. When the lanes disagree (as they do in the Alberta minority map — sub-threshold on crosswalk Lane 1, above-threshold on every Lane 2 signal), the framework requires reporting the disagreement honestly rather than selecting the more convenient lane.

**ii. Jurisdiction-calibrated Lane 1 thresholds.** Rather than applying the Stephanopoulos-McGhee 7% EG threshold (derived from US elections data, never judicially adopted), the framework derives its Lane 1 thresholds from the jurisdiction's own neutral-draw MCMC ensemble. The Alberta-calibrated 95th-percentile EG is 3.86% — nearly half the US-derived figure — and is the operative threshold for this audit's Lane 1 verdict.

**iii. Pre-registered prospective scorecard.** The "what a gerrymander would look like" checklist is published and OSF-time-stamped *before* the Lunty committee's 91-seat map is produced (embargo release 2026-11-02). When the map is tabled, the same scripts and thresholds applied in §5 of this audit are re-run without modification. The pre-registration converts the framework from an audit-voice opinion into a classical hypothesis test against a future observable. Code: `analysis/scripts/november_red_alert_scorecard.py`.

**iv. Signature threshold with explicit cross-evidence requirement.** The checklist's "sure-sign" verdict requires three formal signatures *plus* at least one new signature *plus* either ensemble-outlier placement or public-support-inversion. This multi-criteria threshold is explicitly borrowed from the multi-criteria discipline in Katz, King & Rosenblatt (2020) and Altman & McDonald (2011) — no single metric is dispositive, but directional consistency across independent metrics is. The audit applies this discipline to both lanes simultaneously.

### Two-lane claim to novelty

> The two-lane scorecard architecture — separating partisan-bias magnitude (Lane 1) from structural-and-procedural pattern (Lane 2) with explicit interaction rules, jurisdiction-calibrated Lane 1 thresholds, and a pre-registered prospective application to a future map — is, to the authors' knowledge, novel as a unified forensic audit framework. Individual components (EG, MCMC ensemble, municipal anchoring) have prior art; their integration under an explicit two-lane verdict structure with pre-specified interaction rules does not.

### Two-lane prior art

- Stephanopoulos & McGhee (2015) — EG formula, Lane 1 core metric
- Chen & Rodden (2013) — MCMC ensemble null, natural-packing controls
- Katz, King & Rosenblatt (2020) — explicit multi-criteria consistency discipline
- Altman & McDonald (2011) — no single metric is dispositive; consistent-signals approach
- *Rucho v. Common Cause*, 588 U.S. 684 (2019) — negative prior art; defines the problem the two-lane architecture is designed to address in the Canadian context
- *Reference re Saskatchewan Electoral Boundaries*, [1991] 2 SCR 158 — Canadian statutory framework the Lane 2 signals map onto

### Two-lane pre-registration

- AsPredicted #289,455 — Lunty 91-seat forensic scorecard (prospective; pending November map)
- OSF embargo release: 2026-11-02
- Checklist: `analysis/reports/track_c_checklist_baseline_scoring.md`
- Script: `analysis/scripts/november_red_alert_scorecard.py`

---

## Summary table

| Contribution | Claim | Pre-reg | Status |
| --- | --- | --- | --- |
| DPG Framework | First formalised audit methodology for the no-official-shapefiles case; nested-polygon ownership inversion and sunset clause are novel sub-contributions | #289,449 (validation) | Methods paper draft at `analysis/reports/methods_paper_draft.md` |
| Neighbour-Drain | First named, pre-registered ED-pair-level pack-crack adjacency metric with directional intensity measure | #289,451 (label-shuffle null) | Null pending execution |
| SZAT | First decomposition of between-map EG differences to individual VA boundary choices with permutation null using a real alternative map as counterfactual | #289,469 (bootstrap null) | Results: `analysis/reports/szat_summary.json` |
| Two-Lane Scorecard | First integrated two-lane forensic audit framework with explicit lane-interaction rules, jurisdiction-calibrated thresholds, and pre-registered prospective application | #289,455 (Lunty scorecard) | Prospective; November 2026 map pending |

---

*Document version 1.1 — 2026-05-07*
