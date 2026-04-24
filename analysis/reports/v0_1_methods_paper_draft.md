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

This paper formalises the **Derived Provisional Geometry (DPG) framework** as a disciplined posture for that case. We contribute: (i) a two-error-mode disclosure (perimeter-mode ±500 m; area-mode Tier-dependent) that distinguishes boundary-localization error from whole-polygon-territory mismatch; (ii) source-tier provenance metadata (`canon_source` ∈ {`sweep`, `osm-municipal-buffered`, `2019-parent`, `v7`}) enabling deterministic overlap resolution; (iii) a precedence-based topology cleanup algorithm with anti-erasure safeguards; (iv) a **four-measurement-layer reporting pattern** (crosswalk, centroid-in-polygon, MAUP v1 uncleaned, MAUP v2 topology-cleaned) that surfaces cross-method disagreement honestly rather than hiding it behind a single point estimate; and (v) a **sunset clause** binding the audit to recompute all DPG-dependent metrics within 48 hours of official shapefile release. We illustrate with the Alberta 2025-26 boundaries audit (87→89 electoral divisions, 4,765 voting-area polygons, 100,000-plan ReCom MCMC) and release the full toolkit under a permissive licence.

---

## Suggested structure (11–14 pages + 3–5 appendices)

### 1. Introduction (~1.5 pages)

- Public-interest forensic auditing as a sub-field of empirical political methodology
- The shapefile-release gap: commissions publish textual reports months-to-years before authoritative geometry
- What the gap means for the citizen-audit posture: publish now or wait?
- Contributions (numbered i–v from the abstract)
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

Every DPG row must carry this metadata. Downstream methods (topology cleanup, four-layer reporting) rely on it.

### 4. Topology cleanup (~2 pages)

Algorithm:

```
For each pair of 2026 EDs (A, B) with non-zero intersection:
    overlap = A ∩ B
    precedence(A) = precedence rank of canon_source[A]
    precedence(B) = precedence rank of canon_source[B]

    if precedence(A) > precedence(B):    overlap → A, B ← B \ overlap
    elif precedence(B) > precedence(A):  overlap → B, A ← A \ overlap
    else (v7 vs v7):                     overlap → smaller-area ED (more concentrated = more trustworthy)

    Anti-erasure safeguard: if resulting B_area < 10 % × original_B_area, split overlap proportionally by centroid proximity instead of wholesale reassignment.

Final pass: any residual overlap goes to the larger polygon (topological closure).
```

Validation gates:
- No-overlap gate: every pair post-cleanup has intersection area < ε (ε = 1 m²).
- No-erased gate: no ED falls below 10 % × original area.
- Area-conservation gate: provincial union area matches source to within 0.001 %.

### 5. Four-measurement-layer reporting (~2 pages)

When multiple vote-attribution methodologies are available, the paper **does not pick one** — it reports all four:

| Layer | Method | Failure mode it exposes |
|---|---|---|
| 1 | Crosswalk blending (no geometry) | Calibration of urban/rural weights |
| 2 | Centroid-in-polygon spatial attribution | Binary assignment bias at boundary-straddling VAs |
| 3 | MAUP area-weighted against raw DPG | Reveals transcription-overlap artefacts |
| 4 | MAUP area-weighted against topology-clean DPG | Authoritative spatial measurement given available DPG fidelity |

Each layer's failure mode is different. A reviewer attacking layer 2 gets answered by layer 1 or layer 4; a reviewer attacking layer 4 gets answered by layer 3's diagnostic. **No single measurement is the headline.** The reader sees all four and their residual disagreement.

Illustrative case study: Alberta 2025-26 minority vs majority asymmetry reads −1.42 pp (layer 1), +4.15 pp (layer 2), +1.12 pp (layer 3, misleading), +3.35 pp (layer 4). Residual cross-method gap: ~4.8 pp. The layer 3→4 comparison isolates the transcription-overlap artefact explicitly.

### 6. Sunset clause as pre-registration commitment (~1 page)

Every DPG-dependent claim is published with a dated, public commitment:

> *All DPG-dependent metrics are provisional. Within 48 hours of the relevant authority publishing official topological shapefiles, the audit commits to: (1) re-running every DPG-dependent analysis against the official geometry, (2) publicly disclosing in a dated amendment any sign-flip or material magnitude change (> threshold), and (3) treating the official-shapefile recomputation as the authoritative result.*

This is a novel defensibility mechanism: it inverts the usual peer-review posture ("we have no shapefiles, so our numbers are final-but-caveated") into a *timestamped obligation*. If the paper authors fail to honour the recompute within 48 h of shapefile release, the commitment is itself falsifiable.

### 7. Case study — Alberta 2025-26 (~1.5 pages, condensed)

Brief summary referencing the main audit paper. Focus on methodological lessons:

- 21 Tier-C hybrid EDs required visual transcription from 600-DPI PNG extractions
- Topology cleanup resolved 19,487 km² of transcription overlap
- Multi-chain ReCom MCMC achieved R-hat 1.013–1.017 on the 4,765-VA graph
- Headline finding: residual 4.8 pp cross-method asymmetry disagreement stands as a *genuine* cross-method property, not a geometry artefact

### 8. Open-source release (~0.5 pages)

Scripts released under [LICENSE TBD] at `github.com/Ixby/alberta-electoral-boundaries-audit`:
- `v0_1_topology_cleanup.py` — precedence-based overlap resolver
- `v0_1_phase_4c_va_attribution_maup_v2.py` — MAUP area-weighting with conservation gate
- `v0_1_build_canonical_shapefiles.py` — population-calibrated parametric sweep
- `v0_1_mcmc_multichain_ensemble.py` — multi-chain ReCom with split-chain R-hat

### 9. Limitations (~1 page)

- The DPG framework is a **second-best** method; it does not substitute for official shapefiles. Option D (FOIP requests in jurisdictions with FOI legislation) remains the only path to court-grade precision.
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
|---|---|---|
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
