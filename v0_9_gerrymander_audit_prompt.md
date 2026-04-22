# Alberta Electoral Boundaries Audit — Claude Code Continuation Prompt v0.9

**System Directive (Claude Code Opus 4.7 with 1M context).** You are running in Claude Code at xhigh or max effort with Auto mode. You have file system access, autonomous execution, and improved vision capabilities (3x resolution over Opus 4.6). Do not output code snippets for the user to run — write the scripts to disk, execute them, read the output, debug if needed via `/ultrareview`, visually analyze the maps, and compile the final report as a markdown file. The user's role is to read the final outputs, not to run intermediate steps.

**Suggested invocation:** `claude --effort xhigh` (or `--effort max` for the hardest portions). Auto mode (Max subscribers) reduces permission prompts during the autonomous loop.

**Task Budget.** Operate within:
- **Token ceiling: 500,000 tokens** for the full agentic loop (raised from 150K in v0.8 to match Opus 4.7's 1M context — the old ceiling was writing for 200K-context models and was leaving roughly 350K of productive budget on the table).
- **Wall-clock ceiling: 4 hours.** The real runaway guard is time, not tokens. Many Phase 4 sub-steps (Nominatim rate-limiting at 1 call/sec, HTTP downloads, polygon operations) consume clock but not context; they bust the audit's total cost while looking fine on a token counter.
- **Per-phase sub-caps unchanged from v0.8** as sanity fuses: Phase 4D capped at 15K tokens for OSM reconstruction, Phase 5 ensemble capped at 100K tokens regardless of overall budget.
- If either ceiling is exceeded **or** the loop is unproductive (same error >3 times, single phase >80K tokens), stop and report partial results rather than draining the budget. The audit is stronger with an honest "blocked at step X" than with results computed on rushed/bad geometry.

**Role:** Lead quantitative political scientist running a non-partisan, evidence-based assessment of Alberta's provincial electoral redistribution. Apply identical detection methods symmetrically to all three maps. The conclusion follows from the numbers; it is not the goal of the methodology.

## Context

Alberta is in a redistribution cycle. Three maps are under evaluation:

1. **2019 boundaries** (87 EDs) — currently in force
2. **Majority recommendation** (89 EDs) — independent commission, tabled March 23, 2026
3. **Minority recommendation** (89 EDs) — government-appointed commissioners, tabled March 23, 2026

The government rejected the majority report on April 16, 2026 and created a UCP-majority MLA committee chaired by Brandon Lunty to oversee a new advisory panel reporting back November 2, 2026. Election fall 2027.

## What's Already Done (Carry Forward, Don't Redo)

The previous sessions completed Tests B1 through B4 (the rigorous packing/cracking analysis) **and** Sections A, C, D, plus methodology-validated Phase 4C skeleton. The findings are in:

- `analysis/v0_1_packing_cracking_results.md` — B1–B4 written findings
- `analysis/v0_1_three_map_partisan_comparison.html` — B1–B4 visual
- `analysis/v0_1_section_A_population_equality.md` — Section A (Population Equality)
- `analysis/v0_1_section_C_geographic_coherence.md` — Section C (Visual Spatial Audit)
- `analysis/v0_1_section_D_procedural.md` — Section D (Procedural)
- `analysis/v0_1_section_4_geometry_provenance.md` — Section 4 (Geometry provenance + Phase 5 block)
- `alberta_redistricting_audit_final.md` — compiled audit report at project root

**Headline table (B1–B4 + key A/C results):**

| Test                       | 2019     | Majority 2026 | Minority 2026 |
| -------------------------- | -------- | ------------- | ------------- |
| B2 — Efficiency gap        | −2.64%   | −0.47%        | +0.30%        |
| B3 — Mean-median (NDP)     | −2.22 pp | −2.15 pp      | −0.01 pp      |
| B4 — NDP seats at 50/50    | 46       | 47            | 43            |
| Sim 2023 outcome (NDP/UCP) | 38/49    | 38/51         | 35/54         |
| A1 MAD from avg            | —        | 3,180         | **4,707**     |
| A2 Calgary NE/SW gap       | —        | +0.4%         | **+12.2%**    |
| C3 Named visual anomalies  | —        | 0             | **3**         |
| C4 Airdrie split           | —        | 2 EDs         | **4 EDs**     |

Majority preserves the 2019 baseline within rounding error. Minority shifts it 2 to 3 pp toward UCP across all four tests, costs NDP 3 seats in simulated 2023, and shows measurable correlates at the population, spatial, and procedural levels. Neither map crosses the 7% efficiency-gap threshold from US case law. **The signal is the directional consistency and the asymmetry between the two 2026 proposals.**

**Reproducibility check (first action for any re-run):**
1. `python3 analysis/v0_1_packing_cracking_analysis.py` — must reproduce the B1–B4 table above
2. `python3 analysis/electoral_forensics_population.py` — must reproduce A1/A2/A3 numbers

If either check fails, debug before trusting downstream work — the rest of the report depends on this baseline.

## Critical Sub-Findings From Prior Sessions (Don't Re-derive)

These came out of v0.8 execution and materially affect methodology. Don't re-derive:

1. **Vote Anywhere is 47.2%, not 21.9%.** Of 1,764,915 total 2023 valid votes, only **52.8% were cast on Election Day** (spatially valid). The 21.9% figure in circulation refers to something narrower. Phase 4C full execution must apportion nearly half the votes by Election Day spatial share, not a fifth.

2. **NDP voters used Vote Anywhere at +6 pp higher rate than UCP.**
   - Election Day two-party: NDP 42.59% / UCP 57.41%
   - Advance/Mobile/Special two-party: NDP 48.84% / UCP 51.16%
   - This means the 70/30 urban/rural B1–B4 approximation *underestimates* urban NDP concentration, which *underestimates* the minority's partisan shift. A correctly-executed Phase 4C is expected to produce a **larger** minority shift than B1–B4's 2–3 pp, not a smaller one.

3. **2023 Voting Area (VA) shapefiles are published.** At `https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip`. These provide pre-computed polygon geometry for every voting area in the province. **Use VA polygons as the spatial unit for Phase 4C**, not per-poll geocoding — this collapses stages 3–5 of the old 4C plan into a single spatial join, saves ~70% of execution cost, and eliminates the Nominatim rate-limit bottleneck entirely.

4. **Calgary classification requires full coverage (no residuals).** The A2 Calgary NE/central vs S/W test is sensitive to residual (unclassified) EDs. v0.8's first-pass classification left 8 minority EDs unclassified and understated the gap at +9.8%. Full classification (all 57 Calgary EDs across both maps) produced the correct +12.2% gap. Any re-run must classify every Calgary ED with a reasonable geographic rule.

5. **2026 shapefiles not released by ABEBC as of 2026-04-22.** Check `https://www.elections.ab.ca/resources/maps/` at the start of any new session — if `2026*.zip` appears alongside `2019Boundaries_ED-Shapefiles.zip`, Phase 4A unblocks and priorities change.

## Files in the Working Directory

```
data/
├── v0_1_alberta_2023_results.csv          (87 EDs, candidate-level 2023 totals — NDP 38 / UCP 49 verified)
├── v0_1_alberta_2019_results.csv          (87 EDs, 2019 baseline — NDP 24 / UCP 63 verified)
├── v0_1_majority_2026_populations.csv     (89 majority-proposed EDs, sum = 4,888,723)
├── v0_1_minority_2026_populations.csv     (89 minority-proposed EDs)
└── 2023_results.xlsx                       (raw Statement of Vote, 87 sheets, poll-level)

analysis/
├── v0_1_packing_cracking_analysis.py      (B1–B4 reproducible)
├── v0_1_packing_cracking_results.md       (B1–B4 written findings)
├── v0_1_three_map_partisan_comparison.html (B1–B4 visual)
├── electoral_forensics_population.py      (A1–A3 reproducible)
├── v0_1_section_A_population_equality.md  (Section A written findings)
├── v0_1_section_C_geographic_coherence.md (Section C written findings)
├── v0_1_section_D_procedural.md           (Section D written findings)
├── v0_1_section_4_geometry_provenance.md  (Phase 4 block documentation)
├── v0_1_poll_attribution_skeleton.py      (Phase 4C skeleton — stages 1-2 live, 3-7 stubbed)
└── polls_2023_unified.csv                 (parsed Statement of Vote — 1,973 rows, 4-figure match to official totals)

maps/
├── majority_calgary.jpg                    (Appendix A, p. 72)
└── minority_calgary.jpg                    (Appendix E, p. 74)

source_maps/
├── minority_alberta_overview.jpg           (Appendix E, p. 73)
├── minority_edmonton.jpg                   (Appendix E, p. 75)
└── minority_other_cities.jpg               (Appendix E, p. 76)

alberta_redistricting_audit_final.md        (compiled audit — current v0.1 published)
```

## Agentic Execution Plan

Phases 1–3 and 6 are complete. Phases 4 and 5 are the active work. If ABEBC has released 2026 shapefiles, Phase 4 unblocks entirely and Phase 5 runs clean. If not, Phase 4C via VA polygons is the recommended path.

### Phase 4 — Boundary Geometry & Attribution

#### 4A. Direct shapefile attempt (first action — check on every re-run)

Fetch `https://www.elections.ab.ca/resources/maps/`. If `2026*` shapefiles are present, download them. Skip to 4F (validation) then Phase 5.

#### 4B. Boundary reconstruction via dissemination area dissolve

**Feasibility note.** Boundary commission reports almost never contain DAUIDs. Run a check first:

- Download `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf` (84 MB)
- `pdftotext abebc_2026_rpt_final.pdf - | grep -E "[0-9]{10}" | head -20`

If DAUIDs not present (likely): skip to 4C.

If DAUIDs ARE present:

1. Build `analysis/da_mapping_lookup.csv`. Columns: `DAUID`, `Riding_Name`, `Proposal_Type` (Majority/Minority).
2. Download 2021 Alberta DA shapefiles from StatsCan.
3. `geopandas.dissolve(by='Riding_Name', aggfunc='sum')`.
4. Project to NAD83 / Alberta 3TM (EPSG:3776).

#### 4C. VA-polygon vote attribution (RECOMMENDED PATH — revised from v0.8)

**Change from v0.8:** use the published 2023 VA shapefiles as the spatial substrate instead of per-poll geocoding. This eliminates stages 3–5 (landmark dictionary + Nominatim + Zero-Sum Verification) because VA polygons are pre-built by Elections Alberta with known lat/lon bounds.

**Pipeline:**

1. **Download VA shapefiles.** `curl -O https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip && unzip 2023Boundaries_VAs.zip -d data/va_2023/`. Load via `geopandas.read_file()`. Each VA polygon has attributes including parent ED, VA number, and geometry.

2. **Attach 2023 vote data to VA polygons.** The Statement of Vote records polls per VA number (e.g., "001,002,003" in the voting_areas field of `analysis/polls_2023_unified.csv`). Aggregate Election Day votes by VA number, attach to the VA polygon geometry. This produces `va_polygons_with_votes.geojson` — every VA polygon has NDP/UCP/other Election Day totals.

3. **Assign each VA polygon to a 2026 ED** (majority and minority separately). Two sub-paths:

   **3a. Crosswalk-from-PDF path.** Extract from `abebc_2026_rpt_final.pdf` Appendix B (which lists VAs per 2026 ED for both maps, if formatted similarly to prior Alberta boundary reports). Use `pdfplumber` to parse tables. If present, this is a machine-readable crosswalk and requires no vision.

   **3b. Vision-on-VA-polygons path.** For each VA polygon centroid, overlay on `maps/majority_calgary.jpg` / `source_maps/minority_*.jpg` and use Opus 4.7 vision to determine which 2026 ED contains the centroid. Each VA is ~40-60 per ED (vs ~200+ polls) — order of magnitude cheaper than per-poll Vision assignment.

4. **Apportion Advance/Mobile/Special votes.** For each 2019 ED: compute what fraction of its Election Day VA polygons were assigned to each 2026 ED. Apportion the 2019 ED's non-ED vote totals by that fraction.

5. **Total Vote Checksum (vote conservation gate).** Sum every NDP and UCP vote across the 89 reconstructed 2026 EDs for both maps. Compare to **NDP 777,404 / UCP 928,900 / two-party 1,706,304**.

   - **Tolerance: 0.1%** (~1,700 votes) for apportionment rounding drift
   - **Hard stop: 1%** — if variance exceeds this, pipeline is leaking votes. Investigate before continuing.

6. **Re-run B1–B4 on measured attribution.** Expected outcome: minority shift larger than 2–3 pp (see sub-finding #2 above).

#### 4D. OSM street-network reconstruction (last resort)

If 4A blocked and 4C insufficient for polygon-geometry tests: same as v0.8, capped at 15K tokens for the 15 hybrid ridings.

#### 4E. Manual digitization (out of scope)

#### 4F. Validation routine

**Population checksum.** Sum 2021 census population within each reconstructed polygon. Compare to official Commission totals. Tolerance: 0.5% warning, 2% hard stop.

**Topological audit.** 89 distinct contiguous polygons (allowing legitimate island ridings for s.15(2)). Slivers and overlaps.

**Geometric shift logging.** If you applied any manual geometric adjustment to make a checksum pass, log in `analysis/geometry_shift_log.md` with: polygon, change, population delta, justification. **If the log is empty at end of Phase 4, explicitly state "no manual geometric adjustments were applied" in the Technical Data Statement.**

**Symmetry consistency.** Apply the same method to majority and minority. Document the method.

### Phase 5 — MCMC Ensemble & Compactness (B5, C1, C2)

**Conditional on Phase 4 producing trustworthy geometry (population variance <0.5%).**

- **C1, C2.** Polsby-Popper and Reock for every ED in both maps. Flag PP<0.15 or Reock<0.25.
- **B5.** GerryChain ensemble, 10,000+ maps meeting ±25% + contiguity + s.15(2) protections. Each real map's partisan metrics vs ensemble distribution. >95th percentile = statistically inconsistent with neutral redistricting.
- **Phase 5 token sub-cap: 100K** (separate from overall 500K ceiling). Gerrychain runs can balloon — the sub-cap forces early stopping if the ensemble is slow.

If geometry not trustworthy: state explicitly "B5/C1/C2 blocked by Phase 4." Do not fabricate.

### Phase 6 — Final Report Update

Update `alberta_redistricting_audit_final.md` at project root (**not** a new file — edit the existing v0.1). Replace the "blocked" entries in the summary table with computed values. Update the Technical Data Statement. Add a "Changelog from v0.1" section documenting what was filled in.

Required additions to summary table (v0.9 deliverables):

| Test                                 | 2019                         | Majority 2026   | Minority 2026   |
| ------------------------------------ | ---------------------------- | --------------- | --------------- |
| **B5 ensemble percentile**            | [computed]                   | [computed]      | [computed]      |
| **C1 min Polsby-Popper**              | [computed]                   | [computed]      | [computed]      |
| **C2 min Reock**                      | [computed]                   | [computed]      | [computed]      |
| **B1–B4 from measured attribution**   | unchanged                    | [refined]       | [refined]       |

Mathematical formalism, missing evidence, and "what would change the headline finding" sections are already in v0.1 — update only if new tests invalidate or materially refine them.

## Symmetry Discipline (Non-Negotiable)

Before publishing any conclusion, verify:

- Did you apply the same test to every proposal?
- If you flagged a move as a packing/cracking signal in one, did you check the equivalent in others?
- Magnitude language proportionate to effect size — no adjective inflation?
- Same benefit of the doubt given to all proposals?
- Same reconstruction algorithm (Phase 4) applied identically to both 2026 maps?

## Self-Verification Loop

- After each metric, print intermediates and verify (no negative populations, totals match, shares <100%).
- Each section MD opens with a sanity-check paragraph: what should the numbers look like, do they?
- On surprising results, `/ultrareview` the script before trusting output.
- **Population Checksum in Phase 4F is the strongest integrity test.** Do not paper over a failure — report the block honestly.
- **Geometric shift logging is non-negotiable.** Any boundary adjustment that moves population gets logged with delta + justification. Empty log = explicit "none applied" statement.
- **Total Vote Checksum at 4C step 5.** Missing votes = real pipeline leak, not rounding. Investigate, don't paper over.
- Data conflicts with the prompt? Prefer the data. Flag the conflict in the report.

## Sources to Fetch as Needed

- **Final report PDF** (84 MB): `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`
- **2023 poll-by-poll xlsx** (462 KB, 87 sheets): `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx` *(already in `data/2023_results.xlsx`)*
- **2023 Voting Area shapefiles (NEW PRIORITY):** `https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip`
- **2019 ED shapefiles:** `https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip`
- **2019 poll-by-poll xlsx:** `https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx`
- **Electoral Boundaries Commission Act:** `https://www.qp.alberta.ca/documents/Acts/E03.pdf` (s.13–15)
- **Reference re Provincial Electoral Boundaries (Saskatchewan),** [1991] 2 SCR 158
- **2021 Census DA shapefiles (Alberta):** `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm`
- **2021 Census population by DA:** `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/index-eng.cfm` (table 98-401-X2021006)
- **Watch for 2026 shapefiles:** `https://www.elections.ab.ca/resources/maps/`

## Trigger

Begin at Phase 4A. If shapefiles are released, skip straight to 4F/5. If not, execute Phase 4C via the VA-polygon path (revised). Continue through Phase 6, updating the existing `alberta_redistricting_audit_final.md` rather than creating a new file. Stop when all phases are complete, when the token ceiling (500K) is exceeded, or when the wall-clock ceiling (4 hours) is exceeded — whichever comes first. Report token spend, wall-clock spend, and any ceiling trips at completion.

If the loop becomes unproductive (same error >3 attempts, single phase >80K tokens), stop and report partial results.

---

*Prompt v0.9. Changes from v0.8:*

- *Token ceiling raised 150K → 500K for Opus 4.7 1M context*
- *Added 4-hour wall-clock ceiling as the actual runaway guard*
- *Phase 4C pipeline revised to use 2023 VA shapefiles as spatial substrate (removes Nominatim geocoding, Zero-Sum Verification, landmark dictionary stages)*
- *Vote Anywhere correction: 47.2% not 21.9%; apportion nearly half the votes*
- *Sub-finding added: NDP +6 pp higher Vote Anywhere rate → 70/30 underestimates minority shift*
- *Calgary classification completeness requirement (no residuals) for A2 sensitivity*
- *Carry-forward table expanded to include Sections A, C findings alongside B1–B4*
- *Per-phase sub-caps retained as sanity fuses (4D=15K, Phase 5=100K)*
- *Phase 6 reframed as update-in-place on existing `alberta_redistricting_audit_final.md`, not a new file*

*Optimized for Claude Code Opus 4.7 1M context with xhigh/max effort and Auto mode. Previous session (Chat 3, v0.8) executed Phases 1–3 and 6 to completion; Phase 4 structurally blocked on 2026 shapefile release. This revision prepares the prompt for the next-session attempt once shapefiles arrive or when the VA-polygon substrate approach is ready to execute.*
