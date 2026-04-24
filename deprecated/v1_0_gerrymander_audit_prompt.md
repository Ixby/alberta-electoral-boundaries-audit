# Alberta Electoral Boundaries Audit — Claude Code Continuation Prompt v1.0

**Opus 4.7 1M context. 450,000 token budget. 4-hour wall-clock budget.**

**System Directive.** You are running in Claude Code at xhigh or max effort with Auto mode. You have file system access, autonomous execution, vision, and web fetch. Do not output code snippets for the user to run — write scripts to disk, execute them, read outputs, compile results. The user reads the final report, not the intermediate steps.

**Role.** Lead quantitative political scientist running a non-partisan, evidence-based assessment. Apply identical detection methods symmetrically to all three maps. **No number enters the final report without passing a stage-based falsifiability gate.**

---

## The Gate Discipline

This is the core of v1.0. The v0.8 audit produced a directional finding that survived a bias audit, but one central number (majority B1–B4) was not reproducible from checked-in code because no intermediate stage enforced reproducibility before downstream stages used it.

Every stage below ends in a **GATE** check. A stage's output cannot propagate to downstream stages until the gate passes. If a gate fails, the stage halts and reports the failure explicitly rather than publishing the unreproduced number.

A gate has four parts:

1. **Check statement:** the specific numeric or structural property that must hold.
2. **Pass condition:** the exact threshold or equality.
3. **Fail behavior:** halt; write `analysis/gate_failures.md` with the failure; do not run downstream stages that consume this stage's output.
4. **Documentation:** the gate status appears in the final report's falsifiability section.

The user's rule: **"Nothing should move between steps without being provable."** This prompt makes that rule operational.

---

## Prior Work and Its Integrity Status

Prior sessions produced:

### Integrity-verified outputs (carry forward unchanged)
- `analysis/scripts/v0_2_packing_cracking_analysis.py` — symmetric three-map B1–B4 with gates G1, G2, G5
- `analysis/scripts/electoral_forensics_population.py` — A1/A2/A3 with gate G3 (no unclassified EDs) and G4 (A2 robustness via alternative classification)
- `analysis/scripts/v0_1_poll_attribution_skeleton.py` — Phase 4C skeleton with parse-stage gate
- `analysis/reports/v0_1_bias_audit.md` — self-audit of the audit

### Carry-forward headline numbers (all reproducible)
From `v0_2_packing_cracking_analysis.py` under gate G2 (estimate validation) and G5 (sensitivity):

| Metric               | 2019     | Majority 2026 | Minority 2026 | Asymmetry (Min − Maj) |
| -------------------- | -------- | ------------- | ------------- | --------------------- |
| Districts            | 87       | 89            | 89            | —                     |
| B2 Efficiency gap    | −2.64%   | −0.78%        | −1.36%        | −0.58 pp              |
| B3 Mean-median       | −2.22 pp | −0.16 pp      | −0.33 pp      | −0.17 pp              |
| B4 NDP @ 50/50       | 46       | 44            | 42            | −2 seats              |
| Seats simulated 2023 | 38/49    | 38/51         | 37/52         | −1 seat               |

From `electoral_forensics_population.py` under gate G3:

| Metric                  | Majority 2026 | Minority 2026 | Asymmetry             |
| ----------------------- | ------------- | ------------- | --------------------- |
| A1 MAD from avg         | 3,180         | 4,707         | minority +48% wider   |
| A2 Calgary Zone A−B gap | +0.36%        | +12.20%       | minority much larger  |
| A2 robustness (2023 winner rule) | +0.39% | +7.71%       | same direction        |
| A3 s.15(2) failures     | 1/3 (Canmore) | 1/3 (RMH-BP)  | equal count           |

### Carry-forward superseded (do not cite)
- v0.1 packing_cracking_analysis.py majority claims (−0.47% EG, −2.15pp MM, 47 NDP@50/50). Not reproducible. Use v0.2 numbers above.
- v0.8 prompt's carry-forward table. Superseded by v0.2 symmetric output.

### Reproducibility check (first action)
```bash
python3 analysis/scripts/v0_2_packing_cracking_analysis.py
python3 analysis/scripts/electoral_forensics_population.py
```
Output must match the tables above. **Gate G0:** if either mismatches, halt — downstream stages are working against a changed baseline.

---

## Stage-Based Pipeline

Each stage below has inputs, a process, a gate, and outputs. The gate's pass condition is what "nothing moves without being provable" operationalizes.

### Stage 0 — Environment Setup

**Inputs:** repository fresh clone, Python 3.11+ with scientific stack.

**Process:** `bash setup.sh`. Confirm imports of geopandas, pyogrio, osmnx, gerrychain succeed.

**Gate S0:**
- [ ] All 10 library imports succeed in `python3 -c "import ..."`
- [ ] `python3 analysis/scripts/v0_2_packing_cracking_analysis.py` reproduces carry-forward table above
- [ ] `python3 analysis/scripts/electoral_forensics_population.py` reproduces carry-forward A-series table
- [ ] FAIL ACTION: If numbers differ, do not proceed. Report environmental or data drift.

**Outputs:** reproducibility verified.

---

### Stage 1 — Shapefile Status Check

**Inputs:** `https://www.elections.ab.ca/resources/maps/`

**Process:** `curl -s https://www.elections.ab.ca/resources/maps/ | grep -E "2026|proposed"`

**Gate S1:**
- [ ] Output contains a match for 2026 boundary files? → Go to Stage 2 (shapefile path).
- [ ] No match? → Go to Stage 3 (VA-polygon fallback). Document the check date in `analysis/shapefile_watch_log.md`.

**Outputs:** shapefile availability status determined; downstream path selected.

---

### Stage 2 — Shapefile Path (4A/4F fast lane)

**Condition to enter:** Gate S1 shapefile-present branch.

**Inputs:** ABEBC 2026 shapefile ZIPs (both majority and minority).

**Process:**
1. Download, unzip, load via `geopandas.read_file()`.
2. Confirm 89 distinct polygons in each map.
3. Project to NAD83/Alberta 3TM (EPSG:3776).

**Gate S2a — topological integrity:**
- [ ] Each map: exactly 89 polygons
- [ ] No self-intersecting geometries
- [ ] Total area within 0.1% of Alberta's land area (640,081 km²)
- [ ] No two polygons share interior (spatial disjoint except at boundaries)
- [ ] FAIL ACTION: write `analysis/topology_failures.md` with the specific failing polygon(s); do not proceed to Stage 2b.

**Gate S2b — population checksum:**
- [ ] For each map: sum of 2021 DA populations within each polygon, compared to ABEBC reported population per ED.
- [ ] Per-ED variance ≤ 0.5%: **PASS**; compute and proceed.
- [ ] Per-ED variance in (0.5%, 2.0%]: **WARN**; log in `analysis/geometry_shift_log.md` with per-ED delta. May proceed to Phase 5 with qualification.
- [ ] Per-ED variance > 2.0%: **FAIL**; do not run Phase 5 on this map. The polygon does not faithfully represent the commission's population count.

**Outputs:** `analysis/geometry/majority_2026.gpkg`, `analysis/geometry/minority_2026.gpkg`, `analysis/geometry/2019.gpkg`.

---

### Stage 3 — VA-Polygon Attribution (4C fallback)

**Condition to enter:** Gate S1 shapefile-not-present branch.

**Inputs:** `2023Boundaries_VAs.zip` from Elections Alberta (published); 2023 Statement of Vote already parsed in `analysis/polls_2023_unified.csv`; commission maps `maps/*.jpg`, `source_maps/*.jpg`.

**Process:**
1. Download VA shapefile, load as GeoDataFrame.
2. Aggregate per-VA 2023 Election Day votes from `polls_2023_unified.csv` (group by `voting_areas` field, split comma-separated VA numbers).
3. For each VA polygon: assign to majority 2026 ED and minority 2026 ED via (a) PDF Appendix B crosswalk if extractable via `pdfplumber`, else (b) centroid-in-polygon test if 2026 shapefiles became available mid-session, else (c) Vision assignment using the map JPGs.
4. Apportion Advance/Mobile/Special votes by Election Day spatial share per 2019 ED.

**Gate S3a — VA parse integrity:**
- [ ] Count of unique VA numbers in the shapefile matches count of distinct VA numbers referenced in `polls_2023_unified.csv`.
- [ ] Every VA in the shapefile has a matching vote total from the poll parse (or explicit "no Election Day polls" for uncontested VAs).
- [ ] FAIL ACTION: list mismatches in `analysis/va_parse_failures.md`; do not proceed.

**Gate S3b — Zero-sum verification per 2019 ED:**
- [ ] Sum of VA polygon centroids by 2019 ED matches the known 2019 ED boundaries (every VA falls inside its claimed 2019 parent ED).
- [ ] ≥95% pass rate: WARN on failures, proceed.
- [ ] <95% pass rate: FAIL; write `analysis/zero_sum_failures.md`.

**Gate S3c — Total Vote Checksum:**
- [ ] After full apportionment to 2026 EDs (both maps): sum NDP votes across all 89 EDs.
- [ ] |sum_NDP − 777,404| / 777,404 ≤ 0.1%: PASS.
- [ ] Same check for UCP (target 928,900): PASS.
- [ ] Variance in (0.1%, 1.0%]: WARN; diagnose rounding drift.
- [ ] Variance > 1.0%: FAIL; vote pipeline leaking. Do not use outputs.

**Outputs:** `analysis/va_polygons_with_votes_2026.geojson` (both maps); `analysis/attribution_2026.csv`.

---

### Stage 4 — Refined B1–B4 (measured, not blended)

**Condition to enter:** Gate S2b or S3c passed.

**Inputs:** measured attribution from Stage 2 or Stage 3.

**Process:** run the same metrics as v0.2 but on measured (not blended) vote totals per 2026 ED.

**Gate S4 — sensitivity collapse:**
- [ ] Measured B2 efficiency gap per map
- [ ] |measured − blended (70/30)| ≤ 1.0 pp: blend was within noise of measurement; report measured as primary, blended as prior estimate.
- [ ] |measured − blended| > 1.0 pp: methodology matters. Report measured and explain why blending was misleading (likely urban turnout differential or Vote Anywhere concentration).

**Outputs:** updated Section B with measured numbers; v0.2 blended numbers preserved for audit trail.

---

### Stage 5 — MCMC Ensemble (B5) and Compactness (C1, C2)

**Condition to enter:** Stage 2 passed (polygon geometry required). Cannot run from Stage 3 outputs alone.

**Inputs:** polygon geometry for both 2026 maps; 2021 census DAs for ensemble constraints.

**Process:**
1. Build dual graph of 2026 polygons per map.
2. Configure GerryChain constraints: ±25% population, contiguity, s.15(2) protections.
3. Generate 10,000 alternative maps per real map.
4. Compute B2, B3 for each ensemble map.
5. Locate each real map in its ensemble distribution.

**Gate S5a — ensemble diversity:**
- [ ] At least 1,000 distinct plans in ensemble (not stuck in local minimum).
- [ ] Std deviation of ensemble efficiency gap ≥ 0.5 pp.
- [ ] FAIL ACTION: increase chain length, decrease burn-in, or flag ensemble as non-representative.

**Gate S5b — compactness computation:**
- [ ] Polsby-Popper computed for all 89 polygons each map.
- [ ] Reock computed for all 89 polygons each map.
- [ ] All values ∈ [0, 1].
- [ ] FAIL ACTION: geometric defect; log in `analysis/compactness_failures.md`.

**Outputs:** ensemble percentiles, compactness scores for both 2026 maps.

---

### Stage 6 — Final Report Update

**Condition to enter:** Stages 0–5 all passed (or explicitly blocked with documented reason).

**Inputs:** Sections A, C, D (already complete); Stage 4 measured B1–B4; Stage 5 B5/C1/C2; geometric shift log; all gate logs.

**Process:** update `report_academic.md` and `report_public.md` at project root. For each updated number, include:
- Which stage produced it
- Which gate(s) it passed
- If blocked: which gate it could not pass and why

**Gate S6 — publication readiness:**
- [ ] Every number in the final report traceable to a script + data file.
- [ ] Every claim of "significantly different" or "directionally consistent" backed by a sensitivity range or robustness check.
- [ ] No "adjective inflation": modifiers proportionate to effect sizes measured, not to narrative arc.
- [ ] Falsifiability section states exactly what evidence would invalidate the headline finding.
- [ ] If audience is unstated, default to producing **both** Public/Media and Academic/Legal versions.

**Outputs:** two updated final reports (Public/Media and Academic/Legal); `migration.md` for the next chat.

---

## Symmetry Discipline (Enforced at Every Gate)

Before any stage's gate can pass:

- [ ] Was the test applied identically to both 2026 proposals?
- [ ] If data was available for only one (e.g., majority non-Calgary imagery), is the scope narrowed explicitly, not overreached?
- [ ] Were characterizations (adjectives, severity language) proportionate to measured effect size on both sides?
- [ ] If a flagged pattern was found in one, was the equivalent checked in the other?

---

## Negative-Finding Discipline

The audit must publish at least one null or contrary finding per session. Candidates:

- Stage 2 topology integrity: if both maps produce clean polygons with <0.5% population variance, both pass. Not every stage produces asymmetric findings.
- Stage 3 zero-sum: if ≥99% of VAs pass the 2019-ED membership check, that's a methodology validation, not a discriminating signal.
- Stage 5 B5: if both real maps fall within the 25th–75th percentile of their ensembles, neither is extreme; report that honestly rather than only reporting the asymmetry.

If every stage in a session produces a pattern confirming the prior, flag that in the bias-audit update: either the methodology is exceptionally well-tuned to this dataset, or the stage definitions are selecting confirming tests. Both possibilities warrant review.

---

## Ceilings and Abort Conditions

- **Token ceiling: 450,000 tokens.** Opus 4.7 1M context allows this without context eviction.
- **Wall-clock ceiling: 4 hours.** The actual runaway guard — Nominatim rate-limits, HTTP downloads, polygon ops burn clock but not context.
- **Per-phase sub-caps:** Stage 5 ensemble ≤ 100K tokens.
- **Abort if:** same error >3 times; single stage >80K tokens; wall-clock >4 hours; user-visible exception in gate check.

On abort: write `analysis/abort_report.md` with the last-completed stage, the failing gate, the partial outputs, and the recommended next action.

---

## Sources

- **2026 shapefiles watch:** `https://www.elections.ab.ca/resources/maps/`
- **Final report PDF (84 MB):** `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`
- **2023 Statement of Vote:** already in `data/2023_results.xlsx`
- **2023 Voting Area shapefiles:** `https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip`
- **2019 ED shapefiles:** `https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip`
- **Electoral Boundaries Commission Act:** `https://www.qp.alberta.ca/documents/Acts/E03.pdf`
- **Reference re Provincial Electoral Boundaries (Saskatchewan)**, [1991] 2 SCR 158
- **2021 Census DAs:** `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm`

---

## Trigger

Execute Stages 0 through 6 sequentially. Stop at any FAIL gate and report. Complete both `report_academic.md` and `report_public.md` in Stage 6 unless the user has specified otherwise.

Report at completion:
- Wall-clock spend
- Token spend
- Every gate's PASS/WARN/FAIL status
- Any stage that halted with its reason
- Files updated or created

---

*Prompt v1.0. Changes from v0.9:*
- *Stage-based falsifiability gates at every transition (S0–S6) — no number moves downstream unless provable*
- *Dual-audience final report (Public/Media + Academic/Legal) as the default Stage 6 deliverable*
- *Negative-finding discipline formalized as an explicit check, not aspirational*
- *Carry-forward table now cites the symmetric v0.2 numbers (−0.78% / −1.36% EG), replacing the unreproducible v0.1 values*
- *Gate definitions include explicit pass/fail/warn thresholds with named output files for each failure mode*
- *Symmetry discipline enforced at every gate, not just globally*

*Optimized for Opus 4.7 1M context with a 450K token budget and 4-hour wall-clock budget. Prior session (v0.9, Chat 3–4) completed Phases 1–3, 6; Phases 4–5 blocked on shapefile release. v1.0 assumes that same starting state and gates every forward step.*
