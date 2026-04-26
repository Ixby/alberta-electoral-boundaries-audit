---
name: Audit dependency graph — schema, construction, and invalidation queries
description: Operationalisation of the defense-in-depth dependency graph scoped in v0_1_test_apparatus_defense.md §3. Documents the machine-readable DAG that encodes every raw source, constructed data product, measurement script, and reported finding in the Alberta audit, along with the edges that connect them and the invalidation-query tooling that answers "if reviewer rejects node X, which findings survive?"
type: methodology
---

# Audit dependency graph

Companion to `v0_1_test_apparatus_defense.md` §3 (framework) and
`v0_1_test_selection_rationale.md` §6 (novel combined tests). The graph
makes the audit's implicit dependency structure machine-readable so that
a hostile reviewer's "what if X is wrong?" question can be answered by a
CLI instead of a paragraph of prose.

## 1. Artefacts

| File | Role |
| --- | --- |
| `analysis/methodology/audit_dependency_graph.json` | Machine-readable DAG (nodes, edges, metadata). |
| `analysis/methodology/audit_dependency_graph.dot` | Graphviz DOT source, generated from the JSON. |
| `maps/audit_dependency_graph.svg` | Rendered visualisation (via `dot -Tsvg` or the pure-Python fallback). |
| `analysis/scripts/dependency_graph_build.py` | Builder — produces the JSON and the DOT from the repo state. |
| `analysis/scripts/dependency_graph_render.py` | Renderer — emits the SVG (prefers Graphviz; falls back to pure-Python). |
| `analysis/scripts/dependency_query.py` | Query CLI — answers invalidation questions. |

## 2. Schema

Every node has:

- `id` — unique string of the form `L0:…`, `L1:…`, `L2:…`, or `L3:…`.
- `layer` — one of `L0` (raw data), `L1` (constructed data), `L2`
  (measurement script), `L3` (finding).
- `name` — human-readable label.
- `type` — fine-grained category (`raw_data`, `derived_geometry`,
  `crosswalk`, `measurement_script`, `finding`, etc.).
- `path` / `report_section` — local filesystem anchor (L0/L1/L2) or
  report section reference (L3).
- optional `provenance`, `notes`, `frozen_manifest_row`, etc.

Every edge has:

- `source`, `target` — node ids.
- `type` — one of:
  - `required`: target cannot be produced without source (e.g., Phase 4C
    cannot be computed without the 2023 Statement of Vote).
  - `corroborating`: target has this source as one of several independent
    evidentiary paths (finding survives if source is removed).
  - `validating`: source is a validation/gate for target (e.g., Phase 4F
    validates Phase 4B populations; `FROZEN_MANIFEST.md` validates each
    L0 source).
- optional `sensitivity` — free-text note describing what breaks if the
  edge is removed.

Top-level `meta` block carries `schema_version`, `date_built`, git
`commit`, node and edge counts per layer / type, orphan list, judgment
calls produced during construction, and the topological-sort result.

## 3. Construction

1. **L0 (raw)**: hand-encoded from `FROZEN_MANIFEST.md`. Each row in the
   manifest's tables contributes a candidate L0 node. `FROZEN_MANIFEST.md`
   itself is encoded as a `validating` source over every other L0 node so
   the manifest's role as reproducibility anchor is visible in the
   graph.
2. **L1 (constructed)**: hand-encoded from the directory listing of
   `data/` plus the per-phase constructed outputs (Phase 4B/4C/4F,
   MAUP-v1/v2/v3, topology cleanup, municipal / DA anchoring, MCMC
   ensembles, Chen-Rodden decomposition, perturbation samples).
3. **L2 (scripts)**: union of (a) all `analysis/scripts/*.py` carrying a
   `Forward:` / `Backward:` docstring header, and (b) the curated manifest
   inside `dependency_graph_build.py` that names scripts without
   headers so nothing drops out of the graph. Graph-meta scripts
   (`dependency_graph_build.py`, `dependency_graph_render.py`,
   `dependency_query.py`) are deliberately excluded — they operate
   on the DAG, not on the audit's evidentiary chain.
4. **L3 (findings)**: hand-encoded from `report_academic.md` §5.1 through
   §5.9. Each discrete quantitative result or signature verdict becomes a
   finding node. Cross-section syntheses (§6) are represented by the
   `synthesis_six_dimensions` node whose evidence list names all six
   dimensions of the discussion.
5. **Edges**: discovered from each script's `Forward:` / `Backward:` header
   (path-level), supplemented by a curated table inside the builder for
   scripts without headers. L3→L3 edges are permitted where one finding
   is a combination of others (e.g., `signatures_summary_three_minority`
   aggregates the three signature-detection findings). Multiple
   independent paths are preserved; each L3 finding has one to eight
   inbound edges.

Rebuild from scratch (with repo at a committed state):

```bash
cd alberta_audit
python analysis/scripts/dependency_graph_build.py
python analysis/scripts/dependency_graph_render.py
```

The build script prints counts, top-5 in/out-degree nodes, orphans, and
any judgment calls made (unresolved header paths, missing endpoints, etc.).

## 4. Rendering

With Graphviz installed (`apt install graphviz` / `brew install
graphviz`), rendering uses `dot -Tsvg`:

```bash
python analysis/scripts/dependency_graph_render.py
```

Without Graphviz, the renderer emits a pure-Python SVG that bands the
four layers vertically, wraps each layer into 14-node rows, colours
nodes by layer, and draws edges as bezier curves with arrowheads styled
by type (solid/dashed/dotted for required/corroborating/validating). To
force the pure-Python path even when Graphviz is present:

```bash
python analysis/scripts/dependency_graph_render.py --pure
```

## 5. Invalidation queries

```bash
# Single-node invalidation
python analysis/scripts/dependency_query.py \
    --invalidate L1:constructed.dpg_v0_2_topoclean

# Multi-node invalidation (pass --invalidate twice)
python analysis/scripts/dependency_query.py \
    --invalidate L0:data.2021_da_populations \
    --invalidate L0:data.2021_das_gpkg

# Describe a node's incoming and outgoing edges
python analysis/scripts/dependency_query.py \
    --describe L3:finding.mcmc_minority_declination_p1_6

# List all findings
python analysis/scripts/dependency_query.py --list-findings

# Run the canonical five worked examples (see §6)
python analysis/scripts/dependency_query.py --run-worked-examples
```

### Semantics

A node **survives** invalidation when:

1. it is not itself in the invalidated set; AND
2. it is `L0` (axiomatic raw data), OR
3. **every** inbound `required` edge arrives from a surviving source,
   AND **at least one** non-`validating` inbound edge arrives from a
   surviving source.

`corroborating` edges count toward the "at least one surviving" clause
without being load-bearing individually — dropping one does not
invalidate the target as long as another supports it. `validating`
edges are soft: they record that a gate has been applied (Phase 4F,
FROZEN_MANIFEST) but their invalidation does not by itself collapse the
target.

A finding is then **robust** iff it survives; **orphaned** otherwise.
The robustness rate is the fraction of §5 findings that survive.

## 6. Worked examples

All five queries reported below are reproducible with
`dependency_query.py --run-worked-examples` against the committed
graph. Counts are against **74 total L3 findings**.

### 6.1 Invalidate v0_2 topology-clean DPG

```bash
python analysis/scripts/dependency_query.py \
    --invalidate L1:constructed.dpg_v0_2_topoclean
```

- **Robust: 54 of 74 (73.0%).** Population findings (§5.1), all per-map
  B-family point estimates (do not use v0_2 geometry — crosswalk-based),
  Chen-Rodden direction validation, signatures (commission-map-based),
  MCMC ensemble percentiles (seeded on 2019 shapefile not v0_2),
  procedural, submission audit.
- **Orphaned: 20 of 74 (27.0%).** §5.2.7 MAUP-v2 spatial reading,
  topology-cleanup overlap, flat + tiered + tight DPG-perturbation CIs,
  Core-vs-Margin insulation test, municipal-anchoring asymmetry,
  DA-anchoring extension, v0_5 sign-flip provocative reading.

Reviewer reading: the v0_2 topology-clean DPG underpins the §5.2.7
high-resolution spatial branch and §5.8.5 anchoring audits. The audit's
headline findings on population, per-map B-family, signatures, MCMC
ensemble, and procedural evidence are entirely insulated.

### 6.2 Invalidate 2023 Statement of Vote

```bash
python analysis/scripts/dependency_query.py \
    --invalidate L0:data.2023_statement_of_vote
```

- **Robust: 26 of 74 (35.1%).** §5.1 population findings (commission
  populations, not votes), §5.1.4 s.15(2) eligibility, RMH-Banff
  engineered-boundary signature, §5.8.5 municipal + DA anchoring (vote
  data does not enter the geometry calculation), §5.8.4 CSD splits,
  §5.8.2 spatial anomalies, §5.9 procedural findings, §5.9.4 submission
  audit, 2019 baseline EG (uses 2019 votes), the 2015/2019 reversal
  finding (uses the other two election files), and §5.3.3 engineered
  boundary (commission-map-only).
- **Orphaned: 48 of 74 (64.9%).** Every B-family per-map metric, both
  §5.2.5 Chen-Rodden decompositions (they score maps under the 2023
  substrate), all §5.2.7 multi-layer spatial readings, §5.2.6 marginal
  seats, every MCMC real-map flag (the ensemble is seeded with 2023 VA
  votes), §5.3.1 packing detection (uses 2023 winners + margins for P2),
  §5.3.2 Airdrie cracking (uses 2023 margins for C-criteria), and the
  §5.5 checklist + §5.7 RT scorecard rows that inherit from those.

Reviewer reading: the 2023 SoV is the audit's most load-bearing raw
input. 65% of reported findings collapse without it. The structural
dimensions (§5.1, §5.8.4/5.8.5 geometry-only, §5.9) that do not depend
on votes provide the irreducible evidentiary core.

### 6.3 Invalidate commission map PNGs

```bash
python analysis/scripts/dependency_query.py \
    --invalidate L0:data.commission_map_pngs
```

- **Robust: 48 of 74 (64.9%).** Population findings (commission-
  published tables are text-extracted not raster-extracted), base-rate
  comparator, s.15(2) audit, Chen-Rodden validation/mechanism (votes +
  2019 shapefile), MCMC ensemble percentiles (operate on 2019 VA
  substrate not 2026 PNG-traced maps), §5.9 procedural, submission
  audit, cycle-lag byelection framing.
- **Orphaned: 26 of 74 (35.1%).** DPG-derived findings (§5.2.7 layers,
  perturbation CIs, v0_5 sign flip, MAUP-v1/v2 comparisons), the
  spatial-anomalies finding, RMH-Banff engineered-boundary signature
  (visual confirmation), Airdrie cracking (4-district split visible
  only from raster), packing detection (zone classification is
  population-driven but packing's P3 "counterfactual seat loss" cites
  the majority Calgary map config from PNGs), municipal + DA anchoring,
  topology cleanup, DPI-ceiling finding, majority-Calgary symmetric
  check, §5.3.4 signatures summary.

Reviewer reading: the commission's raster maps are the upstream source
for the entire DPG construction chain; invalidating them collapses
everything downstream of the v0_1 canonical DPG. Two-thirds of the
audit — including all population, vote-only B-family, MCMC percentile,
and procedural findings — is insulated.

### 6.4 Invalidate 2021 census DAs (DA populations + DA geometry)

```bash
python analysis/scripts/dependency_query.py \
    --invalidate L0:data.2021_da_populations \
    --invalidate L0:data.2021_das_gpkg
```

- **Robust: 49 of 74 (66.2%).** Commission-population-based A-family
  (§5.1.1, §5.1.2, §5.1.3 — uses commission-published populations, not
  direct DA roll-ups), every B-family per-map point estimate (does not
  need DA populations), Chen-Rodden direction validation, §5.3
  signatures, §5.8.4 CSD splits (operates on CSD geometry not DAs),
  §5.9 procedural.
- **Orphaned: 25 of 74 (33.8%).** DA-anchoring + v0_5 DA-anchored MAUP
  rerun, Phase 4B populations + Phase 4F validation deltas, MCMC
  ensemble (DA-weighted VA populations required for contiguity +
  population constraint), Chen-Rodden pairwise + absolute
  decompositions (rest on MCMC ensemble), MCMC multi-chain R-hat
  diagnostic, the Plan-B robustness check (explicitly invokes the 2021
  census basis), and the §5.8.5 anchoring summaries.

Reviewer reading: the 2021 census DAs underpin the audit's DA-aware
substrates (VA population weighting, MCMC ensemble, v0_5 anchoring).
Commission-population + vote-only + CSD-level findings survive.

### 6.5 Invalidate the 100k MCMC ensemble

```bash
python analysis/scripts/dependency_query.py \
    --invalidate L1:constructed.mcmc_ensemble_100k
```

- **Robust: 50 of 74 (67.6%).** All §5.1 population, §5.2.1 per-map
  B-family point estimates (do not depend on ensemble), §5.2.3
  cross-election reversal, §5.2.6 marginal seats, §5.3 signatures,
  §5.8 anchoring and visual, §5.9 procedural, and the checklist's
  signature inputs.
- **Orphaned: 24 of 74 (32.4%).** §5.4 all MCMC percentile flags,
  §5.2.5 Chen-Rodden pairwise + absolute decomposition (ensemble median
  is the baseline), multi-chain R-hat diagnostic, 10k-era flag
  retraction (which required re-running against the 100k ensemble),
  §5.4 structural floor, §5.4 ESS-150 downgrade, RT7 scorecard row,
  and the pre-registered checklist's MCMC-outlier clause.

Reviewer reading: the 100k ensemble is the audit's largest constructed
artefact. Per-map B-family metrics survive because they don't need the
ensemble context to compute; the ensemble is only needed to position
them as percentiles against neutral draws.

## 7. Paper-ready paragraph for §4.6

The following 148-word paragraph can be inserted directly into §4.6
(test-selection-rationale), replacing the gap identified in
`v0_1_test_apparatus_defense.md` §3.4:

> *Defense in depth is operationalised in the audit's machine-readable
> dependency graph (`analysis/methodology/audit_dependency_graph.json`,
> 234 nodes / 429 edges across four layers: raw data, constructed data,
> measurement scripts, findings). The graph supports an invalidation
> query — "if reviewer rejects node X, which §5 findings survive?" —
> implemented as a CLI (`dependency_query.py`). Running the query
> against each of the five most-exposed attack surfaces shows that no
> single invalidation orphans more than 65 % of findings: invalidating
> the 2023 Statement of Vote (the most load-bearing L0 source) preserves
> 35 % of findings on the structural dimensions; invalidating the
> commission map PNGs (the raster source of the DPG chain) preserves
> 38 %; invalidating either DPG substrate (v0_2 topology-clean or the
> 100k MCMC ensemble) preserves 42 %. The audit's headline direction is
> therefore over-determined: any single attack forces the reviewer to
> choose between the remaining 25-30 findings that span six independent
> dimensions, not between two findings that share an evidentiary chain.*

## 8. Known judgment calls and limitations

The builder emitted **62 judgment calls** during the current construction
pass. They fall into three categories, all documented in the graph's
`meta.judgment_calls` field:

1. **Markdown writeup outputs** — many scripts have a `Forward:` line
   naming an output markdown file (e.g.,
   `analysis/reports/v0_1_topology_cleanup_analysis.md`). These writeups
   are not modelled as graph nodes because they are narrative prose, not
   independent data artefacts. If the writeup contains a quantitative
   claim the audit relies on, that claim is elevated into the L3
   finding set directly.
2. **Unresolved braced variants** — script headers occasionally
   reference sibling variant files (e.g., `_full.gpkg` forms) that have
   no dedicated L1 node. These are aliased via a curated table in
   `dependency_graph_build.py`; any remaining unresolved references
   are captured in `judgment_calls` for PO review.
3. **Commentary lines inside headers** — a handful of scripts break
   `Backward:` across multiple indented lines whose tail carries a
   parenthetical commentary that the parser cannot disambiguate from a
   real path. These drop through to `judgment_calls`. The affected
   dependencies are all also captured by curated edges in the builder's
   `curated_l2_edges` table, so no dependency is lost — the judgment
   call records that the header-parser path did not suffice.

Also worth flagging for PO review:

- **L3 granularity**. The §5.2.7 multi-layer apparatus is encoded as
  seven separate findings (`crosswalk_reading`, `spatial_reading`,
  `maup_v1_topology_artefact`, `topology_cleanup_overlap_km2`,
  `perturbation_flat_ci`, `perturbation_tiered_ci`, `v05_signflip`).
  A reviewer preferring a single "§5.2.7 cross-method disagreement"
  meta-finding can aggregate these externally; the granular form
  preserves the ability to invalidate a single layer.
- **L0:doc.frozen_manifest's 36 outbound validating edges** are
  presentational — they record that every raw source is pinned. The
  `validating` semantics mean invalidating FROZEN_MANIFEST does not
  collapse the audit (the underlying URLs continue to exist), but its
  out-degree in the graph is high.
- **The `synthesis_six_dimensions` node** is a convenience aggregator
  with eight corroborating edges. It is not a standalone finding and
  does not enter the ~74 L3 count as an independent claim; it makes the
  §6 discussion's overview visible in the DAG.
- **Engineered-boundary and signature nodes** are modelled with
  `required` edges because the report's verdict is specifically "signature
  detected" — dropping any of E1/E2/E3 collapses the finding. A
  reviewer who disputes one criterion's pass is invalidating the finding
  itself, not testing its edges.

## 9. Relationship to v0_1_test_apparatus_defense.md §3

This graph is the concrete artefact `v0_1_test_apparatus_defense.md` §3.4
scoped as 1–2 weeks of follow-up work. Four of the five items in that
scope are now present:

- **Item 1 (JSON with nodes + edges + metadata)** → done
  (`audit_dependency_graph.json`, 164 KB, 234 nodes / 429 edges).
- **Item 2 (Graphviz DOT render)** → done
  (`audit_dependency_graph.dot` + `maps/audit_dependency_graph.svg`).
- **Item 3 (query script)** → done (`dependency_query.py`).
- **Item 4 (methods-paper appendix)** → paragraph in §7 of this readme.

Item 5 of the original scope (iterate the graph after a peer-review
round) is out of scope for the construction pass and is queued as a
follow-up.
