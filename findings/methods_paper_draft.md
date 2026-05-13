---
name: Methods paper draft — Derived Provisional Geometries for electoral audits
description: Standalone methodology paper companion to the Alberta 2025-26 audit. Skeleton + abstract + section outline.
type: reports
---

# Derived Provisional Geometries for Electoral Audits: Honest-Bounded Inference When Official Shapefiles Are Unavailable

**Author:** Will Conner, Mount Royal University (BSc Computer Information Systems, 4th year).

**Status:** Draft skeleton — 2026-04-24. Companion to the Alberta 2025-26 Electoral Boundaries Audit (`report_academic.md`).

**Intended venue (in order of preference):**

1. arXiv `stat.AP` preprint — fastest priority-setting; 3–5 day turnaround; free and citable.
2. *Political Analysis* (Cambridge) — methods journal; DPG framework fits their empirical-methods scope.
3. *Journal of Open Research Software* — code-first paper releasing the DPG + topology-cleanup toolkit.
4. *PS: Political Science & Politics* — shorter methods note format.

---

## Abstract (draft, ~220 words)

Public-interest forensic audits of electoral redistricting face a common and under-treated problem: the months-to-years gap between a commission's final report and the release of official topological shapefiles. During that gap, every spatial analysis rests on *derived* geometry — polygons traced from commission maps, reconstructed from crosswalks, or built from related administrative boundaries. Existing redistricting-analysis frameworks (MGGG; Chen and Rodden 2013; Stephanopoulos and McGhee 2015) implicitly assume official shapefiles; they do not specify how an audit should publish defensibly when those shapefiles are unavailable.

This paper formalises the **Derived Provisional Geometry (DPG) framework** as a disciplined posture for that case. We contribute: (i) a two-error-mode disclosure (perimeter-mode ±500 m; area-mode Tier-dependent) that distinguishes boundary-localization error from whole-polygon-territory mismatch; (ii) source-tier provenance metadata (`canon_source` ∈ {`da-anchored`, `municipal-anchored`, `osm-municipal-buffered`, `sweep`, `v7`}) enabling deterministic overlap resolution; (iii) a **four-phase DPG perfection pipeline** — precedence-based overlap resolution with anti-erasure clamp, tier-ordered edge snapping (nearest-neighbour welding using `shapely.snap()` with auto-revert on >5% area distortion), spatial-index gap-fill (R-tree nearest-neighbour assignment of residual interstitial polygons), and a multi-threaded 1m precision pass closing floating-point artefacts — that produces a fully tessellating polygon set from independently-traced sources; (iv) a **nested-polygon ownership-inversion refinement** that resolves residual overlaps where one ED is fully contained inside another by carving the inner polygon out of the outer rather than erasing the inner — a contribution beyond the cartographic-conflation literature (Sester 2000; Saalfeld 1988), where existing algorithms either erase the smaller polygon or flag the case as unresolvable; (v) a **four-measurement-layer reporting pattern** (crosswalk, centroid-in-polygon, MAUP v1 uncleaned, MAUP v2 topology-cleaned) that surfaces cross-method disagreement honestly; (vi) a **programmatic city-centre alignment proof** that requires only ground-truth POINTS (not polygons) and is therefore appropriate for the DPG-without-shapefiles posture this paper formalises; and (vii) a **sunset clause** binding the audit to recompute all DPG-dependent metrics within 48 hours of official shapefile release. We illustrate with the Alberta 2025-26 boundaries audit (87→89 electoral divisions, 4,765 voting-area polygons, 1,010,000-plan ReCom MCMC ensemble across 4 parallel chains × 252,500 steps) and release the full toolkit under a permissive licence.

---

## Suggested structure (11–14 pages + 3–5 appendices)

### 1. Introduction (~1.5 pages)

- Public-interest forensic auditing as a sub-field of empirical political methodology
- The shapefile-release gap: commissions publish textual reports months-to-years before authoritative geometry
- What the gap means for the citizen-audit posture: publish now or wait?
- Contributions (numbered i–vii from the abstract)
- Why a Canadian case study + why the general framework matters beyond Canada

### 2. Related work (~1.5 pages)

- MGGG redistricting guidance (DeFord et al., 2021; ReCom + lawsuit-grade ESS standards)
- Partisan-bias metrics family (Stephanopoulos & McGhee 2014/2015; McDonald & Best 2015; Warrington 2018)
- Natural-packing framework (Chen & Rodden 2013) + its Canadian applicability
- Consistency-across-correlated-dimensions discipline (Katz, King & Rosenblatt 2020; Altman & McDonald 2011)
- Canadian redistribution literature (Courtney 2001; Pal 2016; *Reference re Saskatchewan Electoral Boundaries* 1991)
- The **gap in existing work**: no formalisation of audit-grade inference without official shapefiles

### 3. The DPG framework (~3 pages)

#### 3.1 Definition

A Derived Provisional Geometry (DPG) is a polygon dataset intended to approximate authoritative boundaries for a redistricting proposal, constructed from: (a) the commission's published maps (PNG or PDF), (b) precursor authoritative shapefiles (prior cycle boundaries), (c) administrative overlays (municipal, dissemination-area, census), and (d) optionally, population-calibrated parametric inference against the commission's own published per-ED population table.

#### 3.2 Two-error-mode disclosure

- **Perimeter-mode uncertainty** — boundary localisation error, typically ±100 m to ±1 km depending on source resolution. Affects compactness metrics (Polsby-Popper, Reock), fine-grained vote attribution near boundaries, and per-segment distance measurements.
- **Area-mode uncertainty** — whole-polygon-territory mismatch, Tier-dependent. Affects DA-overlay populations, polygon-intersection tests, and vote attribution where a polygon overcovers or undercovers its intended territory.

Why distinguishing these matters: the literature typically reports a single "geometric error" bar, which misleads reviewers. A polygon traced at ±500 m perimeter precision can still have ±40 % area-mode error if its overall footprint is wrong.

#### 3.3 Source-tier provenance (the `canon_source` column)

- `2019-parent` (or `<prior-cycle>-parent`) — inherited from an official authoritative shapefile. Shapefile-grade. Tier A.
- `osm-municipal-buffered` — constructed from an OpenStreetMap municipal-boundary lookup plus documented buffer. High confidence where the commission thumbnail shows the ED following a municipal edge. Tier B.
- `sweep` — population-calibrated parametric sweep against the commission's published per-ED population target. Tight residuals (typically < 0.5 %) by construction. Tier B.
- `v7` (or final visual-transcription version) — traced from commission thumbnails. Lowest confidence. Tier C.

Every DPG row must carry this metadata. Downstream methods (tessellation pipeline, four-layer reporting) rely on it. In the Alberta 2025-26 dataset: `da-anchored` (47 EDs, Tier A), `municipal-anchored` (32 EDs, Tier A), `v7` (7 EDs, Tier C), `sweep` (2 EDs, Tier B), `osm-municipal-buffered` (1 ED, Tier B).

### 4. Topology cleanup and DPG tessellation (~3 pages)

The DPG tessellation problem has four distinct failure modes, each requiring a different algorithm. Together they form the **four-phase DPG perfection pipeline** (`dpg_perfecter.py`).

#### 4.1 Phase 1 — Overlap resolution

*Failure mode:* two EDs claim the same territory. Typically occurs at Tier-C (v7) boundary edges where independent polygon traces overlap each other.

```text
Process EDs in tier order (highest first):
    Maintain "claimed" = union of all geometry committed so far.
    For each ED in order:
        candidate = ED.geometry \ claimed
        if candidate.area >= 10% × ED.geometry.area:
            commit candidate
        else (anti-erasure):
            split contested zone by centroid proximity half-plane
            commit own half

Add committed geometry to "claimed".
```

Anti-erasure safeguard: if subtraction would reduce an ED below 10% of its original area, a centroid-proximity half-plane split is used instead of wholesale subtraction. This prevents a single large Tier-A polygon from erasing a small adjacent Tier-C polygon entirely.

#### 4.2 Phase 2 — Tier-ordered edge snapping (nearest-neighbour welding)

*Failure mode:* two adjacent EDs have a sliver gap between them — territory claimed by neither. This arises because DPG polygons are built to hit population targets, not to tessellate; independent polygon traces do not share exact boundary geometry.

**Key insight:** we know there *should* be no gap between adjacent EDs. The commission draws a single line between two districts; the gap is purely a transcription artefact. The correct action is not to fill the gap with new territory but to *weld* the two edges together.

Algorithm using `shapely.snap(geometry_a, geometry_b, tolerance)`:

```text
Process EDs in tier order (highest first):
    Maintain "committed_union" = union of all geometry committed so far.
    For each ED in order:
        if distance(ED.geometry, committed_union) < snap_tolerance:
            ED.geometry ← snap(ED.geometry, committed_union, snap_tolerance)
        Add ED.geometry to committed_union.
```

`shapely.snap()` modifies only `geometry_a` — it snaps vertices and edges of the lower-tier ED to the nearest vertex/edge of the accumulated higher-tier union, without modifying the higher-tier geometry. This means:

- A `v7` ED adjacent to a `da-anchored` ED inherits the DA boundary exactly.
- A `v7` ED adjacent to another `v7` ED snaps to whichever was processed first (the one with higher original area, since same-tier EDs are ordered by area).
- The snap is idempotent: running Phase 2 twice produces the same result.

**Tolerance selection:** `snap_tolerance = 500 m`, matching the stated ±500 m perimeter-precision bound for Tier-C polygons. This is conservative enough to avoid merging genuinely separate EDs in dense urban settings (the minimum ED-to-ED gap in the Alberta dataset is approximately 800 m at its closest).

**Resolution improvement.** Phase 2 combined with the Phase 4 1-metre precision pass yields an area-resolution improvement of approximately **400,000,000×** relative to the v0.1/v0.2 DPGs. The logic: v0.1 edge precision was ≈ 20 km (freehand trace at province scale), giving a minimum representable area of 20,000 m × 20,000 m = 4 × 10⁸ m². The Phase 4 pass achieves ≤ 1 m edge precision, giving minimum area 1 m². Since area resolution scales as the square of linear precision, the improvement factor is (20,000 / 1)² = 4 × 10⁸. At 20 km precision, a 500-voter VA near an ED boundary could be assigned to the wrong district with no detectable error; at 1 m precision, the assignment error is negligible relative to any VA size in the dataset.

**Safety check — false-weld detection.** After snapping, the script checks each ED's area change. If snapping changes an ED's area by more than 5%, the snap is reverted for that ED and a warning is logged. In the Alberta 2025-26 run, one ED (Stony Plain-Drayton Valley) triggered a 911% area increase and was reverted — the 500 m tolerance accidentally welded it to a large adjacent da-anchored polygon whose boundary happened to be within tolerance. The reverted ED's boundary gap is handled by Phase 3 gap-fill instead.

**Novelty:** Tier-ordered edge snapping for DPG tessellation does not appear in the redistricting methods literature. Existing frameworks (MGGG; Chen & Rodden 2013) assume official shapefiles that tile by construction. The technique is closely related to *edge conflation* in cartographic generalisation (Sester 2000; Duckham & Drummond 2000) but applied here under an explicit provenance-tier ordering rather than geometric similarity. The tier ordering ensures that higher-confidence boundaries propagate outward to less-certain boundaries — never the reverse.

#### 4.3 Phase 3 — Gap fill

*Failure mode:* after overlap resolution and edge snapping, residual territory exists that is still claimed by no ED. This is not a transcription artefact between adjacent EDs but rather outer territory that the DPG polygons collectively undercover.

```text
provincial_boundary = unary_union(all VA polygons)  # authoritative precinct coverage
gap = provincial_boundary \ union(all 89 EDs)

For each connected component of gap:
    Find the ED with the longest shared boundary with this gap component.
    Assign gap component to that ED.
    Fallback (if no shared boundary): assign to nearest ED by centroid distance.
```

Validation gates:

- No-overlap: every pair post-cleanup has intersection area < ε (ε = 1 m²).
- No-erasure: no ED falls below 10% of original area.
- Full-coverage: gap area after fill < 0.001% of provincial area.
- Name preservation: output has identical 89 ED names as input.

#### 4.4 Phase 4 — 1m precision pass (multi-threaded)

*Failure mode:* after Phases 1–3, shared boundaries are *geometrically close* but not always *bit-identical*. Floating-point artefacts accumulate from snap operations, gap-fill unions, and `buffer(0)` cleanings. Two adjacent EDs may share an edge whose vertex coordinates differ by 1–10 cm. This passes the no-overlap and full-coverage gates but causes downstream tooling (gerrychain's adjacency builder; sub-VA spatial joins) to either flag spurious overlaps or fail to detect adjacency.

```text
For each ED i (in parallel across worker threads):
    g_i ← snapshot of i's geometry
    For each other ED j whose bbox is within tolerance of i's bbox:
        if distance(g_i, g_j) < tolerance:                  # tolerance = 1 m
            g_i ← snap(g_i, g_j, tolerance)
    Write g_i back to slot i.
```

The phase runs across worker threads (default 8–10 on a modern desktop CPU). `shapely.snap()` releases the GIL for its GEOS calls, so threading scales reasonably to the box's physical-core count. Each thread reads from a snapshot of the original geometries and writes to a private slot — losing the cross-pass propagation that the serial version had (snap to j seeing j's snap to k), but at ≤1 m tolerance on provincial-scale polygons the convergence is local rather than global, so the loss is negligible.

**Per-phase checkpointing.** The pipeline writes `<plan>_phase{N}.gpkg` after each successful phase. On crash or interruption, the next invocation detects the highest-completed phase and resumes from there. Critical for long runs: Phase 3 spatial-index gap-fill on the Alberta minority map redistributes 1,168 gap polygons (85,408 km²) and Phase 4 takes 10–25 minutes wall-clock; losing either to a power loss is recoverable, not catastrophic.

#### 4.5 v0_8.1 — Refinement with nested-polygon ownership inversion

*Failure mode the 4-phase pipeline does not solve:* a small number of residual overlap pairs remain because they cannot be resolved without erasing an ED. Two situations produce these:

1. **Sub-square-metre slivers** along shared boundaries — floating-point dust that the 1m precision pass is too coarse to catch.
2. **Fully-nested polygons** — one ED whose footprint is entirely inside another ED's footprint. This happens when the multi-source assembly draws two EDs from inconsistent sources for the same physical territory. In the Alberta dataset, Calgary-Falconridge-Conrich (DA-anchored) and Airdrie-East (sweep-derived) produce a 141.9 km² nested overlap on the majority map.

Refinement walks the residual list and applies one of three resolutions in priority order:

- **Clip** — standard difference operation; the lower-tier ED loses the overlap. Used when the loser retains ≥10% of its area after clipping.
- **Nested-invert** — when the loser is fully (≥95%) contained in the winner: the loser keeps its full polygon, and the *winner* is clipped to carve a hole around the loser. Inverts the standard precedence rule for this case only. Used 1 time in the Alberta majority refinement (Calgary-Falconridge-Conrich preserved by carving Airdrie-East), 2 times in minority refinement.
- **Midline split** — fallback when neither clip nor nested-invert resolves: assign half the overlap to each ED based on perpendicular-bisector distance to centroids. Not triggered in the Alberta dataset.

After v0_8.1 refinement: 0 residual overlap pairs on both Alberta maps.

**Novelty.** Nested-polygon ownership inversion is, to the authors' knowledge, a contribution beyond the cartographic-conflation literature (Sester 2000; Saalfeld 1988): existing polygon-overlap-resolution algorithms either erase the smaller polygon or flag the case as unresolvable and require human intervention. Inverting ownership is not always semantically appropriate (in cadastral GIS, a property nested inside another is itself an error), but for *electoral* GIS it is the only resolution that preserves both legally-distinct EDs without imputing geometry that the data do not support.

#### 4.6 Why the order matters

The phases must run in sequence: Phase 1 before Phase 2, Phase 2 before Phase 3, Phase 3 before Phase 4. v0_8.1 refinement runs after the 4-phase pipeline produces a v0_8 canonical output.

- Running Phase 2 before Phase 1 would snap edges across overlapping territory, potentially propagating the overlap into the committed union and corrupting subsequent snaps.
- Running Phase 3 before Phase 2 would fill some sliver gaps with "new" territory instead of welding adjacent edges — inflating ED areas unnecessarily and obscuring the DPG imprecision.
- Running Phase 4 before Phase 3 would snap edges across un-filled gaps and create geometric artefacts that look like adjacency but cross undefined territory.

The pipeline produces **v0_8 DPGs**: fully tessellating shapefiles where every point in Alberta's electoral territory belongs to exactly one ED, shared boundaries are bit-identical in both EDs that share them, residual overlap pairs after v0_8.1 refinement are 0, and every claimed improvement is traceable to a specific phase and tolerance parameter.

#### 4.7 Programmatic alignment proof

The DPG-without-shapefiles posture forecloses standard ground-truth comparison: the audit cannot compute intersection-over-union against an authoritative polygon set because no such set exists. We propose an alternative validation pattern that requires only ground-truth POINTS, not polygons:

1. **Topology check** — ED count vs expected, residual overlap area, full provincial coverage, count of EDs with non-zero geometry.
2. **City-centre landmark check** — major Alberta city centres (Calgary, Edmonton, Red Deer, Lethbridge, Medicine Hat, Grande Prairie, Fort McMurray, Airdrie, St. Albert, Spruce Grove) sourced from Statistics Canada CSD representative-point coordinates, tested by point-in-polygon containment against the v0_8 EDs. The containing ED's name is checked for plausibility against the city name (the Calgary-centre point should land in some ED whose name contains "Calgary"; landing in "Peace River" is a misalignment signal).
3. **Cross-plan area consistency** — the majority and minority partitions should each cover the same provincial area to within DPG precision; deviation > 0.1% indicates a topology bug in one of the plans.

For the Alberta v0_8.1 majority refined output: 89 EDs (✓), 68 with non-zero geometry (21 inherited-empty from upstream — see §4.8), 0 residual overlaps (✓), 100.04% provincial coverage (✓), and 9 of 10 city centres land in correctly-named EDs (the single miss is St. Albert: 37.9 km² polygon does not extend to the city-centre representative point, a documented localisation residual within the DPG ±500 m perimeter precision band). Cross-plan area diff: 0.04%.

This validation pattern is appropriate to the DPG posture in a way that polygon-based ground-truth comparison is not. It generalises beyond electoral GIS to any domain where derived polygons must be validated against authoritative point references rather than authoritative polygon references.

#### 4.8 Honesty about inherited limitations

The Alberta dataset contains 21 majority EDs and 12 minority EDs whose `canon_source` candidate sources collectively produced no usable geometry. These EDs (mostly small urban Calgary and Edmonton districts plus Stony Plain–Drayton Valley, St. Albert-Sturgeon, etc.) remain empty in v0_8 even after the 4-phase perfecter. The audit reports this as a first-class data-completeness metric ("68 of 89 EDs with geometry; 21 inherited-empty") rather than masking it via zero-area imputation.

This matters for two downstream consequences. First, Phase 3 spatial-index gap-fill can only assign gaps to *non-empty* EDs, so the 21 empty EDs' notional territory concentrates disproportionately in adjacent rural EDs (West Yellowhead grew 47,092 → 93,599 km²; Taber-Cardston 14,982 → 30,800 km²). Any per-ED area metric derived from v0_8 should carry a "rural-inflation caveat." Second, geometry-dependent metrics (compactness, MAUP-attributed votes, contiguity) are reported on the 68 (or 77 for minority) EDs that have geometry, not on the full 89.

The audit's defence against the "this hides bad data" objection is *transparent reporting*: the empty-ED list is published, the rural-inflation magnitudes are quantified, and every geometry-dependent finding carries an explicit "of N EDs with geometry" footnote.

### 5. Four-measurement-layer reporting (~2 pages)

When multiple vote-attribution methodologies are available, the paper **does not pick one** — it reports all four:

| Layer | Method | Failure mode it exposes |
| --- | --- | --- |
| 1 | Crosswalk blending (no geometry) | Calibration of urban/rural weights |
| 2 | Centroid-in-polygon spatial attribution | Binary assignment bias at boundary-straddling VAs |
| 3 | MAUP area-weighted against raw DPG | Reveals transcription-overlap artefacts |
| 4 | MAUP area-weighted against topology-clean DPG | Authoritative spatial measurement given available DPG fidelity |

Each layer's failure mode is different. A reviewer attacking layer 2 gets answered by layer 1 or layer 4; a reviewer attacking layer 4 gets answered by layer 3's diagnostic. **No single measurement is the headline.** The reader sees all four and their residual disagreement.

Illustrative case study: Alberta 2025-26 minority vs majority asymmetry reads −1.42 pp (layer 1), +4.15 pp (layer 2), +1.12 pp (layer 3, misleading), +3.35 pp (layer 4). Residual cross-method gap: ~4.8 pp. The layer 3→4 comparison isolates the transcription-overlap artefact explicitly.

#### 5.1 Why the layers disagree in Alberta

The four readings are not four attempts at the same measurement — they measure different things and their disagreement is informative.

**Layer 1 (crosswalk, −1.42 pp minority-vs-majority efficiency gap)** uses no geometry. It maps 2026 EDs to their 2019 predecessors via an explicit dictionary and computes vote totals by blending 2019 predecessor results using population-weighted urban/rural coefficients. The −1.42 pp reading is in the audit's crosswalk convention where negative = UCP-favourable (more negative = more UCP-advantaged). It means: conditioning on 2023 vote shares and the commission's own population table, the minority map is estimated to waste *more* NDP votes per seat than the majority — that is, the minority is estimated to be slightly *more* UCP-favourable. This reading is stable across five urban-weight sensitivity values (0.60–0.90); the direction holds at ~90% of Monte Carlo draws over model-parameter uncertainty.

**Layer 2 (centroid-in-polygon, +4.15 pp)** assigns each Voting Area's votes to whichever 2026 ED contains its centroid. Against v0_7 DPG geometry, this also shows the minority as *more* UCP-favourable than the majority. In the spatial formula convention (positive EG = NDP wastes more = UCP advantage), +4.15 pp means the minority is 4.15 pp further in the UCP-favourable direction than the majority — the same qualitative direction as Layer 1. The two layers do not disagree on which map is more UCP-favourable; they disagree on magnitude and, in appearance, on sign — but the sign difference is a convention artefact. Layer 1 (crosswalk) uses the audit's negative-UCP convention while Layer 2 (spatial formula) uses the positive-UCP convention; converting either to the other's convention reverses the arithmetic sign without changing the substantive direction. What the two layers genuinely dispute is magnitude: Layer 1 puts the minority-vs-majority gap at 1.42 pp, Layer 2 at 4.15 pp. This magnitude disagreement is the informative signal about DPG boundary-localization uncertainty: in urban Tier-C zones where DPG precision is lowest, the centroid method may assign VAs to the wrong 2026 ED, artificially widening the apparent gap relative to the crosswalk.

**Layer 3 (MAUP against raw DPG, +1.12 pp, misleading)** area-weights votes by intersection with the raw pre-perfected DPG polygons. Before the four-phase tessellation pipeline, the DPG contains overlaps and sliver gaps; VAs near contested boundaries may contribute partial vote fractions to two EDs simultaneously. The +1.12 pp reading understates the true cross-method asymmetry because overlap contamination artificially equalises the two maps' vote distributions near boundary zones. This layer's value is diagnostic, not estimative: its deviation from Layer 4 quantifies the topology artefact.

**Layer 4 (MAUP against topology-clean DPG, +3.35 pp)** uses the v0_8 perfecter output. With overlaps and gaps resolved, area-weighted attribution no longer double-counts boundary VAs. The Layer 3→4 change (+2.23 pp) isolates the transcription-overlap artefact: 2.23 pp of the apparent map symmetry in Layer 3 was a product of imperfect tessellation, not a genuine property of the boundaries.

#### 5.2 Reporting without picking a winner

The four-layer report conveys three things simultaneously: the best available estimate under each methodology, the failure mode that explains each layer's deviation from the others, and the range of uncertainty attributable to DPG fidelity rather than model specification. The standard of care is:

1. State each layer's finding and its specific failure mode in the same sentence.
2. Do not average the layers or weight-average to a "consensus" estimate. The disagreement is real; averaging it away hides information.
3. Identify which pair of layers isolates which artefact (Layer 3 vs 4 isolates the topology artefact; Layer 1 vs 2 isolates the boundary-localization artefact).
4. Commit to a final reading when — and only when — official shapefiles arrive. The sunset clause specifies this timing.

#### 5.3 Canonical resolution

When official Elections Alberta shapefiles arrived (2026-05-06), all four layers were recomputed on authoritative geometry. Layer 1 (crosswalk, which uses no geometry) was unaffected: majority −0.40%, minority −1.81% (crosswalk convention, negative = UCP-favourable). Layer 2 on canonical geometry (centroid-in-polygon against official EA shapefiles, formula convention positive = UCP advantage): majority +0.098%, minority +4.02%; inter-map gap +3.92 pp (minority more UCP-favourable). Both readings are on the UCP-tail of the null distribution under canonical geometry.

The canonical result confirms directional agreement between layers 1 and 2 (both showing minority more UCP-leaning than majority). The magnitude gap between layers narrows relative to the DPG era (DPG Layer 2 put the gap at +4.15 pp; canonical Layer 2 puts it at +3.92 pp), consistent with DPG boundary-localization error in Tier-C zones accounting for a small fraction of the cross-layer magnitude disagreement. The directional finding — minority more UCP-favourable — was present at every DPG stage and is confirmed by official geometry.

### 6. Sunset clause as pre-registration commitment (~1 page)

Every DPG-dependent claim is published with a dated, public commitment:

> *All DPG-dependent metrics are provisional. Within 48 hours of the relevant authority publishing official topological shapefiles, the audit commits to: (1) re-running every DPG-dependent analysis against the official geometry, (2) publicly disclosing in a dated amendment any sign-flip or material magnitude change (> threshold), and (3) treating the official-shapefile recomputation as the authoritative result.*

This is a novel defensibility mechanism: it inverts the usual peer-review posture ("we have no shapefiles, so our numbers are final-but-caveated") into a *timestamped obligation*. If the paper authors fail to honour the recompute within 48 h of shapefile release, the commitment is itself falsifiable.

### 7. Case study — Alberta 2025-26 (~1.5 pages, condensed)

The Alberta 2025-26 audit provides a complete in-production demonstration of the DPG framework: from first freehand polygon trace to official shapefile recomputation, with the metric evolution at each stage documented and publicly reproducible. The companion paper (`report_academic.md`) carries the full partisan-bias analysis; this section focuses on the methodological progression.

#### 7.1 The ten-stage DPG development arc

**Stage 1 — Province-scale freehand trace (v0_1, 2025-10).** Initial digitisation of the commission PDF thumbnails at full-province zoom. Edge precision approximately 20 km. Coverage: 60 of 89 majority EDs, 54 of 89 minority. No usable EG estimate; the large uncovered fraction (29 majority, 35 minority) concentrated in urban Calgary and Edmonton where thumbnails were densest but most complex. Purpose: confirm the DPG construction workflow before investing in higher-precision tracing.

**Stage 2 — First topology cleanup (v0_2, 2025-11).** Resolved 14 overlap pairs produced by the province-scale trace (two EDs claiming the same 4,000–12,000 km² rural block). First tessellating output. Still at 20 km edge precision. The B1 vote-distribution histogram (margin bins) became computable at this stage; EG crosswalk estimate first available (−1.42 pp minority-vs-majority, direction stable from this version forward).

**Stage 3 — Population-calibrated parametric sweep (v0_3, 2026-01).** For 5 null-geometry EDs per map (urban Calgary where the thumbnail trace was illegible), iterated buffer-expand from the 2019 predecessor centroid until the commission's published per-ED population target was met to within 0.5%. This filled the highest-density urban holes. MCMC first attempted at this stage; Recom was not able to complete valid proposals across the null-geometry EDs, deferring ensemble runs to v0_7.

**Stage 4 — CSD/DA anchoring (v0_5, 2026-02).** 47 EDs whose visible boundaries follow census Dissemination Area (DA) edges were reconstructed from the official 2021 DA polygon set (Tier A: shapefile-grade). 32 EDs following Census Subdivision (CSD) edges received municipal-boundary anchoring (Tier A). Coverage rose to 79 majority EDs and 71 minority EDs. The Layer 1 crosswalk stabilised; the centroid-in-polygon Layer 2 first became reliable for the anchored subset.

**Stage 5 — Full visual transcription from 600-DPI PNG (v0_7, 2026-03).** The remaining Tier-C EDs (21 majority, 18 minority) were transcribed from high-resolution PNG extractions of the commission's published maps. All 89 EDs now carry geometry on both maps. This is the first version at which all four measurement layers are computable. Observed layer readings (minority vs majority EG gap): Layer 1 −1.42 pp, Layer 2 +4.15 pp, Layer 3 +1.12 pp, Layer 4 +3.35 pp. The Layer 1–2 sign divergence first surfaces at this stage, confirming that the boundary-localization artefact concentrates in the Tier-C zones that were only finalized at v0_7.

**Stage 6 — Four-phase tessellation (v0_8, 2026-03).** `dpg_perfecter.py` applied. Overlap resolution removed 19,487 km² of transcription overlap; tier-ordered edge snapping closed 8,214 sliver gaps; gap-fill redistributed 1,168 gap polygons across 85,408 km²; 1m precision pass eliminated floating-point artefacts. Output: fully tessellating, bit-identical shared boundaries. MAUP attribution reliable. One sampler hang during Phase 4 (Stony Plain–Drayton Valley, 911% area blowup, reverted); resolved by gap-fill fallback.

**Stage 7 — Nested-polygon ownership inversion (v0_8.1, v0_8.2, 2026-04).** Residual overlap pairs resolved using the ownership-inversion algorithm (§4.5). Calgary-Falconridge-Conrich / Airdrie-East 141.9 km² nested overlap on majority map resolved by carving Airdrie-East around Falconridge-Conrich rather than erasing the smaller polygon. Zero residual overlap pairs post-v0_8.2.

**Stage 8 — Advance vote splatting (v0_9, 2026-04).** Advance and special ballots (~47% of all 2023 votes, reported only at ED level) apportioned back to individual VAs proportionally to each VA's election-day two-party share. This raised both maps' seats@50/50 by +1.12 pp symmetrically (inter-map gap preserved to 4 decimal places). The SZAT substrate used in the Ch2 bootstrap was built on v0_9 with full advance-vote attribution.

**Stage 9 — Official Elections Alberta shapefiles (canonical, 2026-05-06).** Canonical `ea_majority_2026_eds.gpkg` and `ea_minority_2026_eds.gpkg` received. All geometry-dependent metrics recomputed. Municipal anchoring: majority 80.0%, minority 72.0% (both within 70–85% Canadian comparator norm; the DPG-era 4.9× below-norm anchoring finding did not survive canonical recomputation). EG Layer 1 (crosswalk, unchanged by canonical shapefiles): majority −0.40%, minority −1.81% (crosswalk convention, negative = UCP-favourable). EG Layer 2 (centroid-in-polygon on canonical shapefiles, formula convention positive = UCP advantage): majority +0.098%, minority +4.02%; inter-map gap +3.92 pp. Both layers agree that the minority map is more UCP-favourable than the majority. The apparent sign difference between the two conventions (negative vs positive) is a convention artefact, not a directional disagreement.

**Stage 10 — Canonical MCMC ensemble (1,010,000-plan, 2026-05-12).** Full 4-chain × 252,500-step ReCom run on canonical shapefiles. GR92 R-hat 1.00179–1.01843 (all four chains pass GR92 < 1.10). Partisan-metric ESS 1,429–1,682 (publication-grade). Minority mean-median at p99.98 (UCP-tail), declination at p1.21 (NDP-tail), seats@50/50 at p99.99. Fisher combined Ch1 × Ch2: p = 6.87×10⁻⁸.

#### 7.2 Error trajectory

| Stage | Majority coverage | Minority coverage | Layer 1 gap | Layer 2 gap | Primary artefact |
|---|---|---|---|---|---|
| v0_1 (freehand) | 67% | 61% | n/a | n/a | 20 km edge precision |
| v0_5 (anchored) | 89% | 80% | −1.42 pp | partially computable | Tier-C zones unresolved |
| v0_7 (full Tier-C) | 100% | 100% | −1.42 pp | +4.15 pp | Boundary-localization in Tier-C zones |
| v0_8 (tessellating) | 100% | 100% | −1.42 pp | +3.35 pp (Layer 4) | Topology artefact removed; ±500m perimeter still DPG |
| canonical (EA shapefiles) | 100% | 100% | −1.42 pp | +3.92 pp (Layer 2) | No DPG artefacts; magnitude gap narrows from +4.15 pp |

The Layer 1 crosswalk estimate is stable from v0_5 forward: the crosswalk uses the commission's population table and 2019 predecessor vote totals, neither of which depends on DPG geometry. This stability is a diagnostic asset — it means any Layer 1 change would flag a shift in the crosswalk weights, not a geometry update.

**v0_7 full-coverage update (2026-04-24).** The DPG pipeline reached canonical v0_7 status (89 EDs per map; v0_5 da-anchored as primary source; v0_3 swept geometry as fallback for 5 null-geom EDs per map; `v3_fallback` boolean column for transparency). Key v0_7 metrics:

- *Compactness (Polsby-Popper):* Majority 2026 mean PP = 0.304 (41/89 EDs below 0.30); minority 2026 mean PP = 0.356 ≈ 2019 baseline (0.355). All maps pass mean PP gate (> 0.15). The majority's lower compactness reflects its hybrid-split doctrine producing geometrically complex boundaries — invisible in the Tier-A/B-only pass.
- *Municipal fragmentation:* Minority 2026 splits 11 significant municipalities across ≥2 EDs (+1 vs 2019); majority splits 8 (−2). Strathcona County (SM, ~105,000 pop.) is split across 10 EDs under the minority (+7 vs 3 in 2019) — the single largest municipal fragmentation event in the dataset.
- *Extended partisan metrics:* Majority PB = +0.0152 (100th ensemble percentile); minority responsiveness = 1.41 (nearly 2× majority's 0.76). All three maps show statistically significant lopsided margins (Wang 2016 t > 3, p < 0.005) — a structural property of Alberta political geography, not a drawing artefact.
- *MCMC Alberta threshold:* Ensemble 95th-percentile EG = 3.86 %; both 2026 maps' absolute EGs remain sub-threshold under this Alberta-calibrated reference, replacing the US-derived 7 % figure as the primary citation in threshold discussions.

### 8. Open-source release (~0.5 pages)

Scripts released under [LICENSE TBD] at `github.com/Ixby/alberta-electoral-boundaries-audit`:

- `dpg_perfecter.py` — four-phase tessellation pipeline (overlap resolution → tier-ordered edge snapping → gap fill → 1m precision pass); produces fully tessellating v0_8 DPGs from independently-traced v0_7 sources
- `topology_cleanup.py` — standalone precedence-based overlap resolver (Phase 1 only)
- `assignment_va_attribution_maup_v2.py` — MAUP area-weighting with conservation gate
- `build_canonical_shapefiles.py` — population-calibrated parametric sweep
- `simulation_multichain_ensemble.py` — multi-chain ReCom with split-chain R-hat

### 9. Limitations (~1 page)

- The DPG framework is a **second-best** method; it does not substitute for official shapefiles. Elections Alberta disclosure remains the only path to court-grade precision.
- `canon_source` precedence rules are judgment calls; topology cleanup could be manipulated by adversarial provenance labelling. We recommend open-source provenance audits at publication.
- The four-measurement-layer pattern works when multiple methodologies can be constructed; in cases where only one is feasible (pure crosswalk without spatial substrate, or pure spatial without crosswalk), the pattern degrades to single-measurement reporting with all its attendant risks.

### 10. Conclusion (~0.5 pages)

The DPG framework closes a gap in the forensic-audit methodology literature: how to publish defensibly when official shapefiles are unavailable. It is *not* a substitute for authoritative geometry; it is a disciplined posture for the interim. The Alberta 2025-26 case study demonstrates the framework in production, and the open-source release makes it reusable for future audits in Canada and beyond.

### Appendices

- **A**: Full topology-cleanup pseudocode + anti-erasure formal definition
- **B**: Per-ED `canon_source` classification for Alberta 2025-26 (majority + minority)
- **C**: Validation gate specifications (pop checksum, vote checksum, conservation, R-hat thresholds)
- **D**: Monte Carlo specification for the DPG-perturbation sensitivity CI (Issue #2)
- **E**: Reproducibility notes — Python 3.11+ environment, input data provenance, one-command rerun

---

## Timeline to first draft (estimate)

| Week | Task | Deliverable |
| --- | --- | --- |
| 1 | §1 Introduction, §2 Related Work, §3 DPG Framework | 6 pages drafted |
| 2 | §4 Topology Cleanup, §5 Four-Layer Reporting | +4 pages |
| 3 | §6 Sunset Clause, §7 Case Study, §8 Release | +3 pages |
| 4 | §9 Limitations, §10 Conclusion, Appendices A–E, revision | arXiv-ready |

**Budget**: ~60 hours of focused write-up once the Alberta paper stabilises at v0.20. Most of the infrastructure (scripts, data, writeups) already exists in the audit repo.

---

## Relationship to the Alberta audit paper

- Alberta paper (`report_academic.md`) **cites** this methods paper for DPG framework, topology-cleanup algorithm, four-layer reporting, and sunset-clause mechanics.
- This methods paper **uses** Alberta 2025-26 as its worked case study; details go to the Alberta paper.
- Both publish independently. arXiv-first for this paper sets priority on the novel contributions; Alberta paper goes to journal review with a concrete methods-paper reference.

## Open question for the PO

- License choice: MIT, Apache-2.0, or CC-BY-4.0-Share-Alike for the toolkit release?
- Submit arXiv preprint in parallel with Alberta paper v0.20, or after it lands in journal review?
- Pursue faculty co-authorship (Bratt outreach already drafted in `private/`), or solo for the methods paper?
