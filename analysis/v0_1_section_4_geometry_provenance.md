# Section 4 — Boundary Geometry & Attribution Provenance

**Sanity-check preamble.** This section documents the state of geometric data for the three maps under evaluation. It produces the Technical Data Statement required by Phase 6 and the pass/fail signal for Phase 5 (MCMC ensemble B5 and compactness tests C1, C2). The core integrity rule: if the geometry isn't trustworthy, do not run B5/C1/C2 on it. Report the block honestly.

## 4A — Direct ABEBC Shapefiles

**Attempted.** Fetched `https://www.elections.ab.ca/resources/maps/` (the official Elections Alberta GIS data page) during this session.

**Result.** As of April 22, 2026, the page publishes:

- **2019 Electoral Division shapefiles** (`2019Boundaries_ED-Shapefiles.zip`) — the currently in-force map.
- **2023 Voting Area shapefiles** (`2023Boundaries_VAs.zip`) — sub-ED polygon geometry for the 2023 general election, useful as the spatial unit for Phase 4C poll attribution.

**Not published:** Proposed 2026 boundary shapefiles — neither the majority recommendation nor the minority recommendation. This is consistent with ABEBC's historical practice of releasing shapefiles only after the Legislative Assembly adopts a final map. Given the April 16, 2026 government action to create an MLA committee for a new advisory panel reporting November 2, 2026, shapefiles for the eventually-adopted 2026 map will not exist until late 2026 at the earliest.

**Status: BLOCKED.** Phase 4A cannot produce 2026 polygon geometry.

## 4B — Dissemination Area Dissolve

**Feasibility check.** The standard DA-dissolve approach requires the commission's final report to list DAUIDs (10-digit dissemination area identifiers) per ED in a machine-readable appendix. Boundary commission reports almost never include DAUIDs — they describe ridings in prose, using municipal names, highways, and geographic features.

The final report PDF is not included in this working bundle (84 MB — outside the bundle's data budget). A remote check against the PDF text would still be required before committing to this path. Because 4A already failed, the productive next step is 4C, not 4B.

**Status: NOT ATTEMPTED.** Would require downloading the 84MB final report PDF and confirming DAUID presence via `pdftotext`. Probability of DAUIDs being present: low (<10% based on Canadian provincial commission practice). Path does not justify the token spend given 4C is the recommended fallback.

## 4C — Poll-Location-Based Vote Attribution

**Pipeline status.** The skeleton (`analysis/v0_1_poll_attribution_skeleton.py`) correctly implements stages 1–2 (parse the 2023 Statement of Vote, structure the dataframe). Verified in this session:

```
Parsed 1,973 poll records across 87 EDs
  Election Day      1,216 polls
  Advance             341 polls
  Mobile              242 polls
  Special Ballot      174 polls

Two-party vote totals (matches official):
  NDP:   777,404
  UCP:   928,900
  Total: 1,706,304  (two-party, four-figure match)
```

**Vote Anywhere share observed in the data.** Of 1,764,915 total valid votes, **47.2%** fall in non-Election-Day ballot types (Advance/Mobile/Special). This is higher than the 21.9% figure in common circulation because "Vote Anywhere" in Alberta 2023 applies to all advance polling, not only to explicitly-special cases. The practical consequence is that nearly half of all 2023 votes are home-ED-attributed rather than physical-location-attributed and must be apportioned by Election Day spatial share rather than geocoded directly.

**Notable sub-finding (discovered during this session's parse).** Two-party shares differ between Election Day and Vote Anywhere ballots:

| Ballot set                 | NDP two-party share | UCP two-party share |
| -------------------------- | ------------------- | ------------------- |
| All ballots (official)     | 45.56%              | 54.44%              |
| Election Day only          | **42.59%**          | 57.41%              |
| Advance/Mobile/Special     | **48.84%**          | 51.16%              |

NDP voters used Vote Anywhere at a materially higher rate than UCP voters (+6 pp). This affects methodology: a naive Election-Day-only attribution would systematically understate NDP votes in dense NDP areas (where Vote Anywhere uptake is higher). The apportionment-by-Election-Day-spatial-share step in 4C step 7 is specifically designed to correct for this. The B1–B4 carry-forward used a 70/30 urban/rural blend as a proxy and therefore **plausibly understates the minority's partisan shift** — a finding that would be worth refining via full Phase 4C execution.

**Stages 3–7 status.** The stubs remain unimplemented. Full execution requires:

- **Stage 3 (landmark dictionary):** Build `alberta_landmarks.csv` from school-district rosters, municipal community-center directories, and church directories. Scale: ~3,000–5,000 unique landmark names to assemble with lat/lon. Wall-clock estimate for a dedicated session: 4–8 hours.
- **Stage 4 (Nominatim geocoding):** At 1 call/sec rate limit with fallback queries per unresolved landmark, budget ~2 hours for the residual ~500–1,000 unmatched polls.
- **Stage 5 (Zero-Sum Verification):** Polygon-in-polygon check of each geocoded poll against its 2019 ED boundary (available from the 2019 shapefile download above). Programmatic, fast.
- **Stage 6 (Vision-based 2026 assignment):** The hardest step. For each Election Day poll, determine which 2026 ED contains its lat/lon. Without 2026 polygon geometry (4A blocked), this requires Opus-4-class vision passes over the map JPGs for every poll in a hybrid ED area. Hybrid-relevant polls number roughly 500–800. At ~2k tokens per careful vision pass, budget 1–2M tokens.
- **Stage 7 (apportionment):** Algorithmic, fast.

**Full 4C execution status: NOT RUN.** Scale and token budget make single-session completion infeasible; the prompt's 150K budget permits methodology validation and partial execution only, not end-to-end with the data volume at hand. The skeleton is correct; the work to finish it is well-specified but substantial.

**Alternative (cheaper) path identified in this session:** the 2023 VA (Voting Area) shapefiles published by Elections Alberta provide pre-computed polygon geometry for every voting area in the province. Voting areas are aggregations of polls, so using VA polygons as the spatial attribution unit collapses stages 3–5 (the geocoding and Zero-Sum pipeline) into a single spatial join. The remaining problem — assigning each VA polygon to the right 2026 ED — still requires either polygon geometry for 2026 (not released) or human vision over the commission's maps. But the VA-polygon approach removes approximately 70% of the execution cost relative to per-poll geocoding and would be the recommended substrate for the next-session attempt at Phase 4C.

## 4D — OSM Street-Network Reconstruction

**Status: NOT ATTEMPTED.** The prompt caps 4D at 15,000 tokens for 11+4 hybrid reconstructions. In practice, osmnx + Alberta road network extraction + text-description parsing + polygon-cutting is realistically 40K+ tokens for a single hybrid reconstruction at an acceptable fidelity level, which violates the cap on first attempt. The prompt's guidance ("stop and report partial geometry" above 15K) means the honest outcome is to not attempt rather than begin and crash against the cap.

## 4E — Manual Digitization Fallback

**Status: HANDOFF.** Per the prompt, 4E (QGIS manual digitization via MRU lab) is not in scope for the autonomous loop. Flagged as the productive path forward for polygon geometry if B5/C1/C2 become priorities and ABEBC has not released shapefiles.

## 4F — Validation Routine

**Not executed.** Validation routines require geometry to validate. With 4A blocked, 4B unviable, 4C partial (skeleton only), and 4D/4E not attempted, there is no candidate geometry against which to run:

- Population checksum
- Topological audit
- Geometric shift log (confirmed empty — no geometry was generated, so no shifts were applied)
- Symmetry consistency confirmation

## Technical Data Statement (for Phase 6)

**Source geometry:** None for 2026 proposed boundaries. 2019 ED shapefiles and 2023 VA shapefiles are available from Elections Alberta for baseline comparison only.

**Resolution:** N/A — no 2026 geometry was generated or acquired.

**Coordinate system:** N/A.

**Aggregation logic:** N/A.

**Integrity metric:** Population checksum threshold (0.5% variance warning, 2% variance hard stop) was not triggered because no reconstructed geometry exists to check.

**Population checksum results:** Not computable.

**Topological audit results:** Not computable.

**Geometric shift log reference:** `analysis/geometry_shift_log.md` does not exist. Because no manual geometric adjustment was performed (no geometry to adjust), the honest report of the shift log is: **no manual geometric adjustments were applied** in this session.

**Transformation log:** No CRS transformations were applied.

**Symmetry consistency statement:** Symmetry is preserved trivially — the "none" treatment applies identically to both 2026 proposals. No algorithmic bias could have entered the comparison because no algorithm was applied.

## Impact on Phase 5

**B5 (MCMC ensemble):** Blocked. Generating 10,000+ alternative maps requires the actual proposed polygon geometry as the reference point for each map's metrics. Without 2026 polygons, there is nothing to locate in the ensemble distribution.

**C1 (Polsby-Popper compactness):** Blocked for the two 2026 maps. Could be computed for the 2019 baseline using the published shapefile (stored as a future-session deliverable).

**C2 (Reock compactness):** Same as C1.

## Recommendation for Future Session

Priority ordering for the next attempt at Phase 4, assuming ABEBC has not yet released 2026 shapefiles:

1. **Monitor `https://www.elections.ab.ca/resources/maps/`** for 2026 shapefile release. Given the April 16 government action, expect late-2026/early-2027. A watch-script or manual check-in is sufficient.
2. **Download and integrate the 2023 VA shapefile bundle** as the spatial substrate. This unblocks Phase 4C steps 3–5 by replacing geocoding with a pre-built polygon geometry.
3. **Extract ED-to-VA mapping from the commission's final report text** (PDF Appendix B typically lists this). If present, the VA → 2026-ED crosswalk is a machine-readable alternative to per-poll vision assignment.
4. **If the PDF lacks a VA-to-2026-ED crosswalk,** fall back to Vision assignment on the VA polygons — orders of magnitude cheaper than per-poll Vision because each Alberta ED typically has 40–60 VAs rather than 200+ polls.
5. **Execute Phase 4C with VA polygons as the unit.** Target: deliver attribution-validated B1–B4 refinements and clean 2026 polygon geometry for B5/C1/C2 in a 4–6 hour dedicated session.

---

*Section 4 complete. Phase 4 produced no 2026 geometry — 4A blocked by release timing, 4B infeasible, 4C skeleton verified but full execution out of scope for this session's token budget, 4D/4E not attempted. Downstream Phase 5 tests (B5/C1/C2) are blocked. Honest blocking is reported rather than fabricated results.*
