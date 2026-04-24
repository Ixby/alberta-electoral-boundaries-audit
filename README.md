# Alberta Electoral Boundary Commission 2025–26 — Comprehensive Forensic Audit

A multi-session forensic audit of Alberta's 2025–26 Electoral Boundary Commission majority and minority recommendations, evaluating each map for structural asymmetry, partisan-bias signatures, geographic coherence, and procedural fairness.

**Version:** v0.19 (monograph) — Date: 2026-04-24

---

## What the audit finds (short)

The minority 2026 recommendation shows **systematic structural asymmetry** relative to the majority recommendation across at least five non-partisan-bias dimensions:

- **Population equality** — MAD 4,707 vs 3,180 persons (A1)
- **Calgary geographic-zone asymmetry** — 12.2 % vs 0.4 % (A2)
- **Airdrie 4-way cracking** — minority splits Airdrie across four EDs; majority splits across two (§5.3.2)
- **Anchoring to reference geography** — 14.5 % / 16.5 % CSD+DA-anchored vs 71 % / 79.6 % on the majority (§5.8.5)
- **Visible cartographic anomalies** — three chair-flagged anomalies under the minority (RMH–Banff Park, Nolan Hill–Cochrane lasso, Edmonton-Windermere stepped boundary)

Partisan-bias metrics (§5.2) are **sign-dependent on vote-substrate and attribution method**; the paper reports them in full but does not lead with them. The B-family findings reinforce rather than singularly carry the headline.

**The audit does not claim the minority map is a gerrymander in the intent sense.** It claims measurable structural divergence from the majority, at magnitudes below the 7 % Efficiency Gap threshold **proposed in the academic literature** by Stephanopoulos & McGhee (2014/2015) — a threshold cited in US litigation (notably *Gill v. Whitford*, vacated on standing without a ruling) but **never adopted as a judicial standard** in the United States or in Canada. Retraction conditions are documented per finding.

---

## Core framing

> There is no correct mathematical solution. The redistricting problem is **NP-hard**; the constraint set (±25 % population deviation + contiguity + compactness + community of interest + Indigenous representation + hearing input) does not admit a unique optimum. The audit therefore does not ask "is this map wrong?" It asks: **"given that no uniquely-correct map exists, how statistically improbable is this specific map within the constraint set, and how much of the asymmetry between the two 2026 recommendations is attributable to drawing choices rather than Alberta's voter geography?"**

The audit's apparatus is deliberately over-engineered relative to the drawing process it audits. That is the point: the Commission draws with a broad brush; the auditor looks through a microscope. A microscope is what forces the distinction between an accidental brush-stroke and a systematic pattern. **Precision is armor.**

---

## How to read this repository

| File | Purpose |
|---|---|
| `report_academic.md` | The monograph. Executive summary, methods, results §§5.1–5.9, limitations, falsifiability hooks. |
| `report_public.md` | Public-audience extract with the pre-registered gerrymander checklist. |
| `analysis/methodology/v0_1_retraction_pathway.md` | **Named retraction conditions per finding.** Reviewer-usable: tells you in advance what data would break each claim. |
| `analysis/methodology/v0_1_null_hypothesis_and_exoneration_criteria.md` | Pre-committed null hypotheses + three-axis Structural/Robust/Durable classification for every finding. |
| `analysis/methodology/v0_1_test_apparatus_defense.md` | Per-test criticism + defense. Answers "are you making up metrics to have metrics?" |
| `analysis/methodology/v0_1_test_selection_rationale.md` | Why these tests, why not others. |
| `analysis/methodology/audit_dependency_graph_readme.md` | Machine-readable DAG of the apparatus: 234 nodes, 454 edges, acyclic, zero orphans. Query: `python analysis/scripts/v0_1_dependency_query.py --invalidate <node>` |

If you are reviewing hostilely, start with **retraction pathway** (what would break a finding) and the **apparatus defense** document (what each test is vulnerable to). If you are reviewing as a reader, start with the monograph's **Executive Summary** and follow the reading-guide inside.

---

## The seven measurement layers of §5.2.7

The partisan-bias direction between the two 2026 maps is reported across **seven** methodological layers, not collapsed to a single number:

1. Aggregation-based (blended crosswalk)
2. Centroid-in-polygon spatial
3. MAUP area-weighted (v0_1 substrate, artefact layer)
4. MAUP area-weighted (v0_2 topology-clean substrate, current primary)
5. v0_2 DPG-perturbation flat ±500 m CI
6. v0_2 DPG-perturbation tier-aware CI
7. v0_5 DA-anchored MAUP rerun

**The seven layers disagree on direction.** Rather than hide the disagreement behind a point estimate, the paper reports all seven and treats the cross-method disagreement itself as a finding. §4.1.4's **sunset clause** binds the audit to rerun all seven within 48 hours of Elections Alberta releasing official 2026 shapefiles.

---

## Apparatus dependency graph

234 nodes (L0 raw data 32 / L1 constructed 53 / L2 scripts 75 / L3 findings 74) across 454 edges. Acyclic, zero orphan findings. The most load-bearing L0 is the 2023 Statement of Vote: invalidating it orphans 48 / 74 (65 %) of findings. But the **26 findings that survive invalidation of the Statement of Vote** span population equality, geographic coherence, procedural, and geometry-only signature-detection — this is the structurally-independent headline core.

Query any invalidation scenario:

```bash
python analysis/scripts/v0_1_dependency_query.py --invalidate L0:data.2021_census_das
```

Outputs the cascade of orphaned findings and the surviving robust core.

---

## Pre-commitment and retraction

The audit is **pre-committed** under several disciplines before each result was read:

- **Null hypotheses** for every test family (§2 of the exoneration-criteria document) — specific directional predictions from a "minority-was-drawn-against-NDP" intent hypothesis.
- **Exoneration thresholds** — numeric thresholds that, if the observed data falls inside, exonerate the minority on that test (e.g., EG difference ≤ 2 pp; coupled chain signals ratio ≤ 1.5×).
- **Retraction conditions** — for every load-bearing finding, named external data or arguments that would force retraction within 48 hours of becoming known.

The exoneration framework has already fired once: the neighbour-drain adjacency test found **zero** coupled chain signals on the minority (vs three on both the majority and 2019), which exonerates the minority on that specific test pre-commitment. The paper reports this as a §5.3.5 EXONERATION row, not as a hidden-methodology dead end.

---

## Follow-up work (open Issues)

| # | Title | Status |
|---|---|---|
| 1 | Precision Option D — FOIP request for official 2026 shapefiles | Open |
| 2 | Precision Option E — DPG-perturbation sensitivity CI on headline numbers | Resolved (v2 tier-aware committed) |
| 3 | Precision Option B — Population-calibrated parametric sweep | Resolved |
| 4 | Precision Option C — Municipal-boundary anchoring | Resolved (v0_4 + v0_5 committed) |
| 5 | Pre-registration 2h24m-separation provenance claim | PO-owned |
| 6 | Gemini Phase B.2 — E2 post-hoc reformulation disclosure | Open |
| 7 | Wayback authenticated SPN2 pass | PO-owned |
| 8 | Publication-grade MCMC — 3 chains × 150k steps | Resolved |
| 9 | Publication decision — v0.19/v0.20 public release channel | PO-owned |
| 10 | Methods paper — DPG framework companion | PO-owned |
| 11 | Empirical Audit paper — 10,000-word extract | PO-owned |
| 12 | Policy Critique paper — April 16 pivot + Act §12 reform | PO-owned |
| **13** | **Local-perturbation MCMC chain — seeded at 2019 enacted** | **Open (retraction-pathway §9 item 2)** |
| **14** | **Trade-off Frontier — counter-map challenge for §5.8.5 anchoring** | **Open (retraction-pathway §9 item 3)** |
| **15** | **Voter-elasticity model — counterfactual vote re-estimation** | **Open (retraction-pathway §9 item 4)** |
| **16** | **Alberta historical-swing EG — compute EG for 2015/2019/2023 under prior-cycle boundaries** | **Open (§5.2.8 Option C provenance; threshold_provenance.md §B.2.1.C)** |

---

## Reproducibility

- **Python 3.14** + `geopandas` + `shapely` + `gerrychain 0.3.2` + `numpy` + `pandas`.
- Setup: `bash setup.sh` installs dependencies.
- Main analyses: `analysis/scripts/v0_1_*.py` (phase pipelines) and `analysis/scripts/v0_2_*.py` (canonical-build pipelines).
- Data: `data/` contains the 2023 Statement of Vote, 2021 Census DAs and CSDs, VA-level poll assignments, canonical DPG shapefiles v0_2 through v0_5, and MCMC sample outputs.
- MCMC multi-chain run (150k × 3 chains): `python analysis/scripts/v0_1_mcmc_multichain_ensemble.py --steps 150000 --chains 3 --seed 42`. ~91 minutes on laptop.

---

## Provenance and license

- **Input data.** 2023 Statement of Vote (Elections Alberta, public); 2021 Census DAs + CSDs (Statistics Canada, Open Government Licence); Commission final report 2026 + appendices (public record). All transformations documented in `analysis/methodology/`.
- **Derived geometry.** Commission 2026 maps are published as 300-DPI rasters only; the audit reconstructs machine-readable polygons as **Derived Provisional Geometries** (DPGs) with Tier A/B/C `canon_source` classification and a §4.1.4 sunset clause tying every DPG-dependent finding to reruns against official shapefiles if released.
- **Vote verification.** 2023: 38 NDP / 49 UCP, two-party total 1,706,304. 2019: 24 NDP / 63 UCP. 2015: 40.72 % NDP / 27.79 % PC / 24.09 % WRP. Majority 2026 population sum: 4,888,723. Minority 2026 population sum: 4,888,773 (50-person rounding drift in commission figures).

The audit is non-partisan and applies identical methodology symmetrically to the majority, minority, and 2019 enacted maps. **Test-application symmetry** (same test, both maps) and **test-selection symmetry** (counter-tests §5.6) are both held as disciplines.

---

## Versioning

- **Monograph:** v0.19 (2026-04-24) — Comprehensive Forensic Audit Monograph with Executive Summary, retraction pathway, and dependency DAG.
- **Audit prompt:** v0.8 (legacy; the prompt drove the early v0.1–v0.11 phases).
- **Canonical DPG substrates:** v0_2 (topology-clean, primary) / v0_3 (population-calibrated sweep) / v0_4 (municipal-anchored) / v0_5 (DA-anchored).
- **MCMC ensemble:** 150k × 3 chains, R-hat < 1.01 strict on 3 of 4 metrics; combined ESS 643–783.

---

## How to challenge the audit

This audit welcomes adversarial review. Specifically:

1. **Read the retraction pathway.** Find a finding's named retraction condition; produce the data or argument that triggers it.
2. **Produce a counter-map** (Issue #14) that achieves the minority's COI claims with majority-comparable anchoring. A successful counter-map retracts §5.8.5.
3. **Query the DAG** (`analysis/scripts/v0_1_dependency_query.py`) to see which findings survive if you invalidate any specific L0/L1 input.
4. **Read the apparatus-defense document** for per-test criticism entries that anticipate the critiques reviewers are likely to raise.

Retraction conditions are public, concrete, and dated. The audit is falsifiable per-finding, not just per-test.
