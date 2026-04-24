# Alberta Electoral Boundaries Audit — Claude Code Continuation Prompt v0.8

**System Directive (Claude Code Opus 4.7).** You are running in Claude Code at xhigh or max effort with Auto mode. You have file system access, autonomous execution, and improved vision capabilities (3x resolution over Opus 4.6). Do not output code snippets for the user to run — write the scripts to disk, execute them, read the output, debug if needed via `/ultrareview`, visually analyze the maps, and compile the final report as a markdown file. The user's role is to read the final outputs, not to run intermediate steps.

**Suggested invocation:** `claude --effort xhigh` (or `--effort max` for the hardest portions). Auto mode (Max subscribers) reduces permission prompts during the autonomous loop.

**Task Budget:** Operate within a 150,000-token budget for the full agentic loop. If the loop is unproductive (stuck in debugging, re-reading files, etc.), stop and report what you have rather than draining the budget.

**Role:** Lead quantitative political scientist running a non-partisan, evidence-based assessment of Alberta's provincial electoral redistribution. Apply identical detection methods symmetrically to all three maps. The conclusion follows from the numbers; it is not the goal of the methodology.

## Context

Alberta is in a redistribution cycle. Three maps are under evaluation:
1. **2019 boundaries** (87 EDs) — currently in force
2. **Majority recommendation** (89 EDs) — independent commission, tabled March 23, 2026
3. **Minority recommendation** (89 EDs) — government-appointed commissioners, tabled March 23, 2026

The government rejected the majority report on April 16, 2026 and created a UCP-majority MLA committee chaired by Brandon Lunty to oversee a new advisory panel reporting back November 2, 2026. Election fall 2027.

## What's Already Done (Carry Forward, Don't Redo)

The previous session completed Tests B1 through B4 (the rigorous packing/cracking analysis). The findings are in `analysis/v0_1_packing_cracking_results.md` and the visual is `analysis/v0_1_three_map_partisan_comparison.html`. Headline:

| Test | 2019 | Majority 2026 | Minority 2026 |
|---|---|---|---|
| B2 — Efficiency gap | −2.64% | −0.47% | +0.30% |
| B3 — Mean-median (NDP) | −2.22 pp | −2.15 pp | −0.01 pp |
| B4 — NDP seats at 50/50 | 46 | 47 | 43 |
| Sim 2023 outcome (NDP/UCP) | 38/49 | 38/51 | 35/54 |

Majority preserves the 2019 baseline within rounding error. Minority shifts it 2 to 3 pp toward UCP across all four tests, costing NDP 3 seats in simulated 2023. Neither map crosses the 7% efficiency-gap threshold from US case law. The signal is the directional consistency and the asymmetry between the two 2026 proposals.

**Reproducibility check (recommended first action):** Run `python3 analysis/v0_1_packing_cracking_analysis.py`. If output matches the table above, B1–B4 is verified and you can proceed to remaining work. If not, debug before continuing — the rest of the report depends on this baseline.

## Files in the Working Directory

```
data/
├── v0_1_alberta_2023_results.csv          (87 EDs, candidate-level 2023 totals — NDP 38 / UCP 49 verified)
├── v0_1_alberta_2019_results.csv          (87 EDs, 2019 baseline — NDP 24 / UCP 63 verified)
├── v0_1_majority_2026_populations.csv     (89 majority-proposed EDs, sum = 4,888,723 = exact provincial total)
└── v0_1_minority_2026_populations.csv     (89 minority-proposed EDs)

analysis/
├── v0_1_packing_cracking_analysis.py      (B1–B4 reproducible script)
├── v0_1_packing_cracking_results.md       (B1–B4 written findings)
└── v0_1_three_map_partisan_comparison.html (B1–B4 visual)

maps/
├── majority_calgary.jpg                    (Appendix A, p. 72)
└── minority_calgary.jpg                    (Appendix E, p. 74)

source_maps/
├── minority_alberta_overview.jpg           (Appendix E, p. 73)
├── minority_edmonton.jpg                   (Appendix E, p. 75)
└── minority_other_cities.jpg               (Appendix E, p. 76)
```

## Agentic Execution Plan

### Phase 1 — Population Equality (Section A)

**Action:** Create `analysis/scripts/electoral_forensics_population.py` using pandas. Compute and self-verify before moving on.

For each of the three maps:
- **A1. Variance distribution.** Mean absolute deviation from 54,929 provincial average. Standard deviation. Maximum positive and negative deviation. Count of EDs above +10%, +15%, +20%, +25% and below the same negative thresholds. The ±25% line is the statutory limit; s.15(2) protected ridings can go to −50%.
- **A2. Geographic asymmetry.** Group EDs by region (Calgary, Edmonton, rural). Within Calgary specifically, partition NE/central from S/W and compute mean populations for each. Test the hypothesis that NDP-leaning Calgary regions are systematically larger (a packing signal) under each map.
- **A3. s.15(2) eligibility audit.** For the three protected ridings each map proposes — majority: Central Peace-Notley (−47.7%), Lesser Slave Lake (−45.4%), Canmore-Banff (−27.2%); minority: Central Peace-Notley (−44.6%), Lesser Slave Lake (−45.4%), Rocky Mountain House-Banff Park (−30.3%) — verify at least 3 of 5 statutory criteria are met independently of the boundary drawing: (a) area >20,000 km², (b) >100 km from major centre, (c) no town with 4,000+ population, (d) significant Indigenous population/reserves, (e) shared border with another province or US. Flag any riding whose boundary appears drawn into existence to qualify.

**Output:** Write results to `analysis/reports/v0_1_section_A_population_equality.md` with comparison tables and the symmetric assessment.

### Phase 2 — Visual Spatial Audit (Section C, partial)

**Action:** Use Opus 4.7's improved vision to directly read the map JPGs. The maps are dense, so use full resolution.

- **C3. Disconnected community check.** Open `maps/minority_calgary.jpg` and `source_maps/minority_other_cities.jpg`. Examine the four moves the chair flagged by name in the majority report's response section:
  1. Calgary-Nolan Hill-Cochrane — does Nolan Hill connect to Cochrane only by skipping Rocky Ridge/Tuscany?
  2. Rocky Mountain House-Banff Park — does the boundary extend through uninhabited Banff National Park to reach the BC border?
  3. Olds-Three Hills-Didsbury — does it include a portion of Airdrie not justified in text?
  4. Calgary-Foothills-Airdrie West — does the Airdrie West portion connect naturally to Calgary-Foothills?
  
  Document visual findings: lasso shapes, disconnected nodes, geographic anomalies. Open `maps/majority_calgary.jpg` and apply the same scrutiny to the majority's four hybrids — Calgary-East, Calgary-Falconridge-Conrich, Calgary-Glenmore-Tsuut'ina, Calgary-West-Elbow Valley. Symmetry discipline applies.

- **C4. Community of interest splits.** Count for each map: municipalities split across two or more EDs (the minority is reported to split Airdrie across 4 ridings; verify), First Nations reserves split or moved between EDs, school divisions split. The majority report names Tsuut'ina, Enoch, and Siksika specifically — check both maps' treatment.

**Output:** Write findings to `analysis/reports/v0_1_section_C_geographic_coherence.md`.

### Phase 3 — Procedural Audit (Section D)

**Action:** Pure desk research. No code execution needed unless you choose to web-fetch comparative cases.

- **D1.** Independence of the drawing process. Original commission was independent (members chosen via judiciary and Lt-Gov in council). The April 16 government action — rejecting the majority report and creating a government-majority MLA committee under Lunty — departs from this. Compare to standard practice across Canadian provinces (BC, Ontario, Quebec, Manitoba, Saskatchewan all use independent commissions).
- **D2.** Public input alignment. The commission received 1,140+ written submissions. The majority report claims (verifiable in Appendix C of the final report PDF) the minority's hybrid configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had no public support. Sample to verify or refute.
- **D3.** Procedural fairness. Did either proposal radically depart from the unanimous interim report (October 2025) without public notice? Trace interim → final.
- **D4.** Override mechanism comparisons. When have other Canadian provincial governments overridden independent boundary commission reports? Quebec 1992, Ontario 1998, BC 2008 are useful comparators.

**Output:** Write findings to `analysis/reports/v0_1_section_D_procedural.md`.

### Phase 4 — Boundary Geometry & Attribution Acquisition (PRECONDITION FOR B5/C1/C2)

This phase produces the spatial data needed for the rigorous compactness tests (C1 Polsby-Popper, C2 Reock) and the MCMC ensemble (B5), and/or the precise vote attribution needed to replace the current B1–B4 approximation with measured values.

#### 4A. Direct shapefile attempt (try first, fastest path)

Check `https://www.elections.ab.ca/resources/maps/` for ABEBC's published shapefiles for the proposed 89-ED maps. If available, download them directly. Skip to 4F (validation) and then Phase 5.

#### 4B. Boundary reconstruction via dissemination area dissolve

**Feasibility note before starting:** Boundary commission reports almost never contain DAUIDs. Run a 3-minute check first:

- `pdftotext final_report.pdf - | grep -E "[0-9]{10}" | head -20`

If DAUIDs are not present (likely outcome), do not commit tokens to this path. Skip to 4C or 4D.

If DAUIDs ARE present:
1. Build `analysis/da_mapping_lookup.csv`. Columns: `DAUID`, `Riding_Name`, `Proposal_Type` (Majority/Minority).
2. Download 2021 Alberta DA shapefiles from StatsCan.
3. `geopandas.dissolve(by='Riding_Name', aggfunc='sum')`.
4. Project to NAD83 / Alberta 3TM (EPSG:3776).

#### 4C. Poll-location-based vote attribution (cheap, accurate, recommended fallback)

**Cheaper than OSM reconstruction. Produces measured vote totals per proposed ED rather than approximated ones. Cannot produce polygon geometry — so does not enable C1/C2 compactness or B5 ensemble.**

The 2023 Statement of Vote (`https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx`) names every polling station in every ED with full address. Total ~5,000 polling places.

**Critical methodology note: Vote Anywhere (2023).** 21.9% of 2023 voters used Vote Anywhere — they cast ballots at any advance/special/mobile location regardless of home ED. Votes are attributed to the voter's home ED, not the physical location. **This means only Election Day polls are spatially valid as proxies for where voters live.** Advance, Mobile, and Special Ballot rows in the Statement of Vote do not have meaningful geographic interpretation.

**Implementation:**

1. **Parse the Statement of Vote.** For each of the 87 sheets, extract all polls with their type (Election Day / Advance / Mobile / Special Ballot), location name, address (where present in the location name), and per-candidate vote totals. Store as a dataframe with columns: `ed_2019`, `poll_letter`, `poll_name`, `ballot_type`, `ndp_votes`, `ucp_votes`, `other_votes`, `valid_votes`.

2. **Build a landmark dictionary first (faster than rate-limited geocoding).** Most poll locations are schools, community halls, churches, libraries with predictable name patterns. Build `analysis/alberta_landmarks.csv` from public sources:
   - Alberta school district lists (CBE, EPSB, Catholic boards) — most polls are schools
   - Municipal community center directories
   - Church directories (United Church of Canada, Catholic dioceses)
   
   Match poll names against this dictionary first. Falls back to Nominatim only for residual misses (saves the rate-limit budget).

3. **Geocode the misses.** Use `geopy.geocoders.Nominatim` with 1-call-per-second compliance for unmatched poll locations. Append "Calgary, AB, Canada" or appropriate locality to disambiguate. Cache results to `analysis/poll_geocoding_cache.csv`.

4. **Zero-Sum Verification gate (do not skip).** For each geocoded poll, check that the lat/lon falls within its known 2019 ED boundary. If "Acadia Community Hall" geocodes to Edmonton, the geocoder is wrong — flag the row, do not propagate. State the flag rate: *"Of [N] geocoded polls, [M] failed the within-2019-ED check. These were re-geocoded manually / discarded / flagged for review."*

5. **Spatial assignment via Vision.** For each Election Day poll that passed step 4: open the corresponding 2026 proposed map JPG (`maps/majority_calgary.jpg`, `maps/minority_calgary.jpg`, etc.). Use Opus 4.7 vision to determine which new 2026 ED contains the poll's lat/lon. The 11 minority hybrids and 4 majority hybrids are the only attribution challenges; everywhere else the existing 2019 ED maps to the new ED via 1:1 rename or trivial split.
   
   For polls within ~500m of a hybrid boundary: treat as borderline, resolve by careful vision inspection of the polygon edge. Document the resolution in `analysis/borderline_poll_resolution.md`.

6. **Aggregate Election Day votes by new ED.** Sum the per-poll Election Day NDP/UCP/other totals into the new 2026 ED.

7. **Apportion Advance/Mobile/Special votes by Election Day spatial share.** For each 2019 ED, compute what fraction of its Election Day votes were assigned to each new 2026 ED. Use that fraction to distribute the 2019 ED's Advance/Mobile/Special vote totals to the same new EDs. Example: if 60% of Calgary-Bow's Election Day polls fell within the new Calgary-Bow-Springbank hybrid, then 60% of Calgary-Bow's advance/special votes go there too.

8. **Re-run B1–B4 metrics** on the measured (rather than approximated) attribution. Report any deltas from the carry-forward baseline. The expected outcome: similar direction of shift, possibly larger magnitude (since the 70/30 blend was conservative).

9. **Confidence statement.** Required output: *"Of [N] total Election Day polls, [G] were successfully geocoded ([G/N]%), [V] were resolved by vision for borderline cases ([V/N]%), [R] could not be assigned and were distributed by neighborhood-weighted average ([R/N]%). Advance/Mobile/Special vote portion ([X]% of total) was apportioned by Election Day spatial share."*

10. **Total Vote Checksum (vote conservation gate).** After all assignment and apportionment, sum every NDP and UCP vote across the 89 reconstructed 2026 EDs (both maps). Compare to the official province-wide totals from the Statement of Vote: **NDP 777,404 / UCP 928,900 / two-party total 1,706,304** (verified in this prompt's carry-forward analysis). State the result: *"Total reconstructed NDP votes: [X], variance from official: [0.0x]%. Total reconstructed UCP votes: [Y], variance from official: [0.0x]%."*

    - **Tolerance threshold: 0.1%** (about 1,700 votes). Integer rounding in proportional apportionment routinely produces drift of a few hundred votes; 0.1% accommodates that without permitting actual data loss.
    - If variance exceeds 0.1%: there's a real leak in the pipeline (votes dropped, double-counted, or polls assigned to no ED). Investigate before continuing.
    - If variance exceeds 1%: do not proceed. The apportionment isn't trustworthy.

**Skeleton script available:** `analysis/scripts/v0_1_poll_attribution_skeleton.py` provides the data loading and dataframe structure as a starting point. Modify rather than rewrite from scratch.

#### 4D. Street-network reconstruction (last resort, expensive)

If 4A blocked, 4B infeasible, and 4C insufficient (or you want geometry for B5/C1/C2):

1. Pull OpenStreetMap road network for Alberta via `osmnx`.
2. Parse street/highway names from each ED's text description in the report.
3. Use them as cutting edges. Spatially join each DA to whichever ED's polygon contains its centroid.
4. **Token budget gate:** Prioritize the 11 minority Calgary/Edmonton hybrid ridings + 4 majority hybrids first. Do not attempt to reconstruct all 89 ridings via street-network unless the first 15 hybrids are completed within 15,000 tokens. If the 15K threshold is exceeded, stop and report partial geometry.

#### 4E. Manual digitization fallback (only if Wuff's MRU lab time is available)

If 4A–4D all fail or are insufficient: report the failure cleanly. Do not fabricate geometry. The fallback is human work in QGIS using MRU lab software — out of scope for this autonomous loop, but a clean handoff item for Wuff.

#### 4F. Validation routine (run regardless of which path produced the geometry/attribution)

- **Population checksum.** Sum the 2021 census population within each generated polygon (or sum the polling-station catchment populations if 4C was used). Compare to the official population from the variance tables (majority p. 44–45 of report, minority p. 71 of Appendix E). State the result: *"The total population captured in the generated geometry is [X], a [0.00x]% variance from the official Commission total of [Y]."* If variance is >0.5%, re-examine the mapping. If >2%, do not proceed to B5 — the geometry isn't trustworthy.
- **Topological audit.** Check for slivers (unintentional gaps between polygons) and overlaps. Verify 89 distinct contiguous polygons (allowing for the legitimate s.15(2) island ridings if any). State: *"Verified [N] polygons, [M] contiguity exceptions accounted for, [K] sliver/overlap defects detected."*
- **Geometric shift logging.** **CRITICAL.** If you applied any manual geometric adjustment to make the population checksum pass — moving a boundary, snapping endpoints, removing a sliver, dissolving a stray polygon — log it in `analysis/geometry_shift_log.md` with: which polygon, what you changed, the population delta the change produced, and why you believe the change is justified. Do not apply silent adjustments. The reader needs to know what's measured vs what's reconstructed.
- **Symmetry consistency.** Whatever method was used, apply it identically to majority and minority proposals to eliminate algorithmic bias in the comparison. Document the method in plain prose.

**Output:** Write geometry files to `analysis/geometry/` (if produced) and the validation report to `analysis/reports/v0_1_section_4_geometry_provenance.md` containing the Technical Data Statement.

### Phase 5 — MCMC Ensemble & Compactness (B5, C1, C2)

**Conditional on Phase 4 producing trustworthy geometry (population variance <0.5%).**

If geometry trustworthy:
- **C1, C2.** Compute Polsby-Popper (`4π × area / perimeter²`) and Reock (district area / smallest enclosing circle area) for every proposed ED in both maps. Flag any ED with Polsby-Popper <0.15 or Reock <0.25.
- **B5.** Install GerryChain (`pip install gerrychain`). Generate 10,000+ alternative maps that meet the same legal criteria (population ±25%, contiguity, the s.15(2) protections). For each of the three real maps, compute partisan metrics and locate in the distribution. A proposal beyond the 95th percentile is statistically inconsistent with neutral redistricting.

If geometry not trustworthy or Phase 4 was skipped: state explicitly in the final report that B5/C1/C2 are blocked. Do not fabricate ensemble results or compactness scores.

**Output:** Write findings to `analysis/v0_1_section_B5_C1_C2_geometric_tests.md`.

### Phase 6 — Final Report Compilation

**Action:** Write `alberta_redistricting_audit_final.md` synthesizing all completed sections.

The markdown file MUST include:

1. **Headline finding** carrying forward the B1–B4 results plus whatever the new sections established.

2. **Summary scoring table.** Build out from the existing B1–B4 table to include all completed tests:

   | Test | 2019 | Majority 2026 | Minority 2026 |
   |---|---|---|---|
   | A1: Mean absolute deviation | [computed] | [computed] | [computed] |
   | A1: EDs above +20% | [count] | [count] | [count] |
   | A2: Calgary NE-vs-S/W population gap | [computed] | [computed] | [computed] |
   | A3: s.15(2) eligibility | [pass/conditional/fail per riding] | [same] | [same] |
   | B2: Efficiency gap | −2.64% | −0.47% | +0.30% |
   | B3: Mean-median gap | −2.22 pp | −2.15 pp | −0.01 pp |
   | B4: NDP seats at 50/50 | 46 | 47 | 43 |
   | B5: Ensemble percentile | [from Phase 5 or "blocked"] | [same] | [same] |
   | C1: Min Polsby-Popper | [computed or "blocked"] | [same] | [same] |
   | C3: Named visual anomalies | [count + named] | [count + named] | [count + named] |
   | C4: Municipalities split | [count] | [count] | [count] |

3. **Written assessment per map.** Distinguish structural advantage that *could be* incidental (e.g., natural rural geography) from patterns that *can't be explained* by non-partisan criteria (deliberate packing/cracking confirmed across multiple tests).

4. **Procedural assessment.** Distinct section covering Section D findings. Treated separately from the cartographic question because the procedural fairness analysis is on different evidence.

5. **Technical Data Statement** (from Phase 4 validation). This is the data-provenance section that proves the geometric reconstruction is a faithful digital twin of the commission's legal text. Structure:
   - **Source geometry:** What input data (StatsCan 2021 DA shapefiles, ABEBC shapefiles, OSM-based reconstruction, or polling-station attribution per Phase 4C)
   - **Resolution:** Source scale and granularity (e.g., 2021 StatsCan DA at 1:50,000 vs 2023 Elections Alberta poll divisions)
   - **Coordinate system:** Used (e.g., NAD83 / Alberta 3TM, EPSG:3776). Note any reprojection (e.g., from EPSG:4326 input).
   - **Aggregation logic:** Dissolve method, mapping dictionary provenance, attribution rule for polls in hybrid EDs
   - **Integrity metric:** The tolerance threshold used as the pass/fail gate (e.g., 0.5% population variance from Commission totals)
   - **Population checksum results:** Per map, with computed variance vs official total
   - **Topological audit results:** Polygon count, contiguity exceptions, sliver/overlap defects
   - **Geometric shift log reference:** If `analysis/geometry_shift_log.md` exists, summarize what was logged. If empty, state explicitly: "No manual geometric adjustments were applied."
   - **Transformation log:** Any CRS transformations applied during the pipeline
   - **Symmetry consistency statement:** Confirm the same algorithm was applied identically to both 2026 maps

6. **Mathematical formalism for the academic record.** When defining the partisan-bias metrics in the report, include the formal mathematical notation. Use LaTeX inline (`$...$`) and display (`$$...$$`) syntax. Because plain markdown viewers don't render LaTeX, also include each formula as a plain-text code block immediately below for portability. Required formulas:

   - Efficiency Gap (Stephanopoulos & McGhee 2014):
     - LaTeX: `$$\text{EG} = \frac{W_A - W_B}{N}$$` where $W_X$ = wasted votes for party $X$ (loser votes + winner votes above $\lceil N_d/2 \rceil + 1$ summed across districts), and $N$ = total two-party votes
     - Plain: `EG = (W_A - W_B) / N`
   - Mean-Median Difference (McDonald & Best 2015):
     - LaTeX: `$$\text{MM} = \bar{v} - \tilde{v}$$` where $\bar{v}$ = mean district vote share for the party, $\tilde{v}$ = median district vote share
     - Plain: `MM = mean(v) - median(v)`
   - Polsby-Popper compactness:
     - LaTeX: `$$\text{PP} = \frac{4\pi A}{P^2}$$` where $A$ = polygon area, $P$ = perimeter; range [0, 1] with 1 = circle
     - Plain: `PP = 4*pi*A / P^2`

7. **Missing evidence.** Specify exactly what data would close remaining forensic gaps.

8. **What would change the headline finding.** In either direction. Be specific.

## Symmetry Discipline (Non-Negotiable)

Before publishing any conclusion, verify:
- Did you apply the same test to every proposal?
- If you flagged a move as a packing/cracking signal in one proposal, did you check whether the equivalent move appears in others?
- Is your magnitude language proportionate to the effect size, or is it adjective inflation?
- Did you give the same benefit of the doubt to all three proposals when evaluating procedural fairness, community of interest, and rural representation?
- Did you apply the same reconstruction algorithm (Phase 4) identically to both 2026 maps? Differences in algorithm = software-induced bias, not real bias.

The B1–B4 finding (majority preserves baseline, minority shifts it) emerged from symmetric testing. Do not abandon that discipline now that the direction is established.

## Self-Verification Loop

Opus 4.7 follows instructions more literally than 4.6. Use that:
- After computing each metric, print intermediate values and verify they make physical sense (no negative populations, totals match official records, party shares sum to <100%).
- After each phase, write a brief sanity-check paragraph at the top of the section MD explaining what you'd expect the numbers to look like and whether they do.
- If a result is surprising, run `/ultrareview` on the script before trusting the output. Three free runs available per Pro/Max account, expiring May 5, 2026.
- The Population Checksum in Phase 4F is the strongest integrity test in this audit. If it fails, do not paper over it — the report is more useful with an honest "geometry not trusted, B5/C1/C2 blocked" than with results computed on bad geometry.
- **Geometric shift logging is non-negotiable.** Auto mode reduces permission prompts but it does not give you license to silently transform data to make a checksum pass. Any boundary snap, sliver removal, or polygon dissolve that produces a measurable population delta gets logged in `analysis/geometry_shift_log.md` with the delta and a written justification. If the log is empty at the end of Phase 4, state so explicitly in the Technical Data Statement.
- If anything in this prompt conflicts with what the data shows, prefer the data and flag the conflict in the final report.

## Sources to Fetch as Needed

- **Final report PDF** (84 MB): `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`
- **2023 poll-by-poll xlsx** (462 KB, 87 sheets): `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx`
- **2019 poll-by-poll xlsx**: `https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx`
- **Electoral Boundaries Commission Act**: `https://www.qp.alberta.ca/documents/Acts/E03.pdf` (s.13–15)
- **Reference re Provincial Electoral Boundaries (Saskatchewan)**, [1991] 2 SCR 158
- **2021 Census Dissemination Area shapefiles (Alberta)**: `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm`
- **2021 Census population by DA**: `https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/index-eng.cfm` (table 98-401-X2021006)
- **Proposed boundary shapefiles** — watch `https://www.elections.ab.ca/resources/maps/`

## Trigger

Begin Phase 1 immediately. Write the script, execute, verify, move to Phase 2. Continue through all phases. Stop only when `alberta_redistricting_audit_final.md` is successfully written and all section MDs are saved to `analysis/`. Report token spend at completion.

If the loop becomes unproductive (stuck on the same error for >3 attempts, or any single phase consumes >40K tokens), stop and report partial results rather than draining the budget.

---

*Prompt v0.8. Carries forward B1–B4 from prior session. Phase 4C poll-location attribution methodology hardened with Vote Anywhere handling, Zero-Sum Verification gate, Total Vote Checksum (0.1% tolerance), and landmark-dictionary geocoding strategy. Phase 6 Technical Data Statement formalized with LaTeX + plain-text math. Optimized for Claude Code Opus 4.7 with xhigh/max effort and Auto mode.*
