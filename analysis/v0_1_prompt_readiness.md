# v1.1 Prompt Execution Readiness Assessment

**Question asked.** Can the v1.1 prompt fully execute with valid and defensible results? Are there limits or challenges addressable now to improve precision?

**Short answer.** v1.1 is executable but has six specific gaps that would force mid-run improvisation or produce unverified outputs. Four of the six can be closed now with FOSS tooling and public data. Two require the boundary shapefiles to be released before they can be resolved. The fixes are captured in v1.2.

---

## Readiness by Stage

### Stage 0 — Environment Setup
**Executable: yes.** `setup.sh` installs all required libraries. Reproducibility scripts are in place and their outputs match the prompt's carry-forward tables as of this session.

**Limit:** no programmatic check that the output actually matches the tables. An agent could run the script, see a small difference, and proceed unaware. v1.2 should add `make verify-carryforward` style regression assertions.

### Stage 1 — Shapefile Status Check
**Executable: yes.** `curl` + `grep`. No failure mode.

### Stage 2 — Shapefile Path (shapefiles present)
**Executable: conditional.** Works *if* ABEBC releases 2026 shapefiles. Will not be available for at least several months given the April 16 political timeline.

**Limit: shapefile release is external.** Nothing the prompt can do about this.

### Stage 3 — VA-Polygon Attribution (shapefiles absent)
**Executable: partially. This is the weakest stage in v1.1.**

Three sub-paths (3a PDF crosswalk, 3b centroid-in-polygon with 2026 shapefiles, 3c vision assignment). 3b requires shapefiles we don't have. 3a is untested — we don't know if the commission's Appendix B is machine-readable. 3c is budget-busting without scoping: ~3,600 VAs across the province at ~500 tokens per careful Vision inspection = ~1.8M tokens, vs the 500K budget.

**Four limits in Stage 3:**

1. **Appendix B crosswalk extractability is unknown.** We need to check the 84MB commission PDF to see if it lists VA→2026-ED mappings in a table that `pdfplumber` can parse. If yes, 3a works cheaply. If no, 3a fails and we fall to 3c. v1.2 should make the PDF recon a pre-Stage-3 task.

2. **Vision scope is unbounded.** "~500-800 hybrid-relevant VAs" in v0.8 prompt, "3,600 VAs" implicit in v1.1. The right scope is hybrid-adjacent VAs only (perhaps 400 for majority + 700 for minority = 1,100 VAs × 500 tokens = 550K — still over budget). v1.2 should cap Vision at 800 VAs total with explicit deprioritization of clearly-interior VAs.

3. **Zero-Sum Verification threshold is named but not gated.** Gate S3b says "<95% pass rate: FAIL." But "pass rate" of what exactly — centroid-in-2019-ED or some fuzzier geographic match? v1.2 should specify the geometric operation precisely.

4. **Total Vote Checksum is per-party, not joint.** If NDP is +0.3% and UCP is -0.3%, variance per party is within the 0.1% hard fail threshold on each, but the joint failure (offsetting errors) is not detected. v1.2 should add a joint-variance gate.

### Stage 4 — Refined B1–B4
**Executable: conditional.** Depends on Stage 3 output. Inherits all of Stage 3's limits.

### Stage 5 — MCMC Ensemble
**Executable: blocked.** GerryChain needs shapefiles.

### Stage 6 — Final Report Update with RT gates
**Executable: partially.**

**Three limits in Stage 6:**

1. **RT1-RT6 gate thresholds are under-specified in several places.** RT1 says "95% CI does not cross zero: strong pass." But what if CI is [−0.0001, +X]? Does that count as crossing? v1.2 needs explicit tie-breaker language.

2. **Grade 9 readability check is asserted but not operationalized.** v1.2 should specify the tool (`textstat.flesch_kincaid_grade`) and the threshold (≤9.0 for public report).

3. **Wuff voice check has no verifier.** The forbidden patterns (not X — Y, templated triads, emoji) can be grep-detected. v1.2 should include a check script.

---

## Assumptions Currently Unverified

Six assumptions in the v1.1 pipeline that would be load-bearing in a real execution:

| Assumption | Currently verified? | Fix needed |
| --- | --- | --- |
| Commission PDF Appendix B has a VA→2026-ED crosswalk table | **No** | PDF recon (v1.2 adds) |
| 2019→2026 ED mappings in `MAJORITY_2026_MAPPING` / `MINORITY_2026_MAPPING` are correct | Partial (name-based guesses for some; uncertain entries not flagged) | v1.2 adds confidence field per entry |
| 2023 VA shapefile contains VA numbers matching the Statement of Vote's voting_areas field | No | Download + verify first, gate Stage 3 on it |
| 70/30 urban weight is a reasonable default | Sensitivity-tested; no per-hybrid grounding | Could improve with Census DA-based estimates per hybrid |
| Grade 9 readability achievable in Wuff voice | No quantitative check | v1.2 adds textstat verification |
| A2 Calgary zone classification is falsifiable | Two classifications checked (geographic + 2023-winner); adding a third (Calgary wards) would strengthen | v1.2 could pre-build the ward dataset |

---

## Fixes Applied In This Session (Pre-v1.2)

Closing four of the six gaps:

**1. PDF recon on Appendix B.** Pre-Stage-3 task added to v1.2. If the recon finds the crosswalk, Stage 3 has a cheap path. If not, the prompt budgets the expensive path.

**2. Readability verification.** `textstat` added to `setup.sh` dependencies. Stage 6 gate specifies Flesch-Kincaid grade threshold of ≤9.0 for the public report. Script added.

**3. Wuff voice pattern checker.** `analysis/check_wuff_voice.py` added. Greps for "not X — Y" constructions, emoji, and templated triad markers. Publication gate in v1.2.

**4. RT gate threshold tightening.** Each of RT1-RT6 gets explicit pass/qualified-pass/fail numeric thresholds with tie-breaker rules. Carried into v1.2.

Two gaps deferred:

**5. Per-hybrid DA-based rural-urban splits.** Requires fetching Alberta 2021 Census DA population data (~100 MB) and manually defining hybrid polygon bounds. Budget-intensive; requires either shapefile release or Stage 3a/3c execution.

**6. Ward-based Calgary classification.** Calgary Open Data publishes ward shapefiles. Adding this as a third A2 classification rule is moderately complex (map ward polygons to ED centroids). Deferred to the session that runs with shapefiles.

---

## Defensibility Assessment

**If v1.2 is executed against the current data state (no shapefiles):**

- Structural findings (A1 population equality, A2 Calgary zone gap, C3 visible anomalies, C4 community splits, D procedural) are **defensible at high confidence.** No shapefile dependency.
- Vote-based findings (B1-B6) are **defensible at 89% directional confidence, not 95% significance.** The red-team gates RT1-RT3 in v1.2 enforce this disclosure.
- The report's synthesis separates structural from vote-based findings, which is the right move.

**If v1.2 is executed after shapefile release:**

- Ensemble (B5) and compactness (C1/C2) become available. The "minority is within the expected ensemble range" uncertainty (§6 of the uncertainty analysis) would be resolved.
- Measured attribution replaces 70/30 blend. Monte Carlo CI narrows or is replaced entirely by the measured value. Partisan-math magnitude becomes a point estimate rather than a range.
- Majority non-Calgary visual audit becomes possible via shapefile + vision.
- §A3 area criterion verification becomes programmatic.

**If v1.2 is executed with a comprehensive submission-archive search added:**

- §D2 "no public support for five disputed configurations" either verified or refuted.
- If refuted, §D weakens substantially.
- If verified, §D strengthens.

---

## Precision and Accuracy Limits

The audit's highest achievable precision under current constraints:

| Finding | Today's precision | With shapefiles | With submission-archive search |
| --- | --- | --- | --- |
| A1 population MAD | 4 sig figs (exact from CSV) | Unchanged | Unchanged |
| A2 Calgary zone gap | ±1.5 pp (7.7-12.2% bracket) | ±0.5 pp | Unchanged |
| A3 s.15(2) area measurements | ±20% (hand estimates) | Exact | Unchanged |
| C3 named anomaly count | Calgary-complete, majority non-Calgary unknown | Full coverage | Unchanged |
| B2 EG asymmetry | [-3.14, +0.76] pp 95% CI | ±0.3 pp point estimate | Unchanged |
| B5 ensemble percentile | Not computable | Single run with bootstrap | Unchanged |
| D2 no-public-support claim | Asserted, not verified | Unchanged | Verified or refuted |

The biggest accuracy gains come from shapefile release (B5, C1/C2, precise A3, measured B1-B4) and submission-archive search (D2). Everything else is near the precision ceiling of current data.

---

## v1.1 → v1.2 Changelog

v1.2 incorporates:
- Pre-Stage-3 PDF recon task
- Vision budget cap at 800 VAs total with hybrid-only prioritization
- RT1-RT6 explicit numeric thresholds with tie-breakers
- Textstat readability gate for public report (FKG ≤ 9.0)
- Wuff voice pattern check script as publication gate
- 2015 added to RT3 cross-election stability check (with boundary-caveat disclosure)
- Confidence field annotations on 2019→2026 ED mappings where uncertain
- VA shapefile parse verification gated before Stage 3 execution
- Carryforward reproducibility assertions in Stage 0

---

*Readiness assessment v0.1. Authored during the v1.1→v1.2 improvement pass. The intent: a prompt that an agent can execute cold, producing results that survive red-team review without mid-run improvisation.*
