# Alberta Electoral Boundaries Audit — Naive Claude Code Bundle v0.7

A self-contained, autonomous-execution bundle for continuing the Alberta electoral boundaries forensic audit in a fresh Claude Code session.

## What's New in v0.7

- **Audit prompt v0.7** with hardened Phase 4C methodology: Vote Anywhere ballot-type handling, Zero-Sum Verification gate, landmark-dictionary geocoding strategy
- **Skeleton script** `analysis/v0_1_poll_attribution_skeleton.py` — parses the 2023 Statement of Vote into a unified poll-level dataframe (1,973 records across 87 EDs), with stub functions for the geocoding/assignment/apportionment stages
- **Raw Statement of Vote** `data/2023_results.xlsx` included so the skeleton runs offline

## How to Run

1. Unzip somewhere clean: `unzip alberta_audit.zip && cd alberta_audit/`
2. Install dependencies: `bash setup.sh`
3. Launch Claude Code: `claude --effort xhigh` (or `--effort max` for hardest phases)
4. Claude Code reads `CLAUDE.md` automatically and finds instructions in `v0_8_gerrymander_audit_prompt.md`
5. Final report appears at `alberta_redistricting_audit_final.md` when the loop completes

## What Is Already Done (Carry Forward)

- Tests B1 through B4 (rigorous packing/cracking) — completed in prior session
- Headline finding: majority preserves 2019 baseline; minority shifts it 2-3 pp toward UCP, costs NDP 3 seats in simulated 2023
- All input data extracted and verified against official totals

## What the New Session Will Do

- **Phase 1:** Section A — population equality tests
- **Phase 2:** Section C — visual spatial audit using Opus 4.7's vision on the map JPGs
- **Phase 3:** Section D — procedural audit
- **Phase 4:** Boundary geometry/attribution acquisition
  - 4A: try direct ABEBC shapefile download
  - 4B: DA dissolve (probably blocked — no DAUIDs in PDF text)
  - 4C: poll-location attribution (recommended path) — uses skeleton script as starting point
  - 4D: OSM street-network reconstruction (capped at 11 hybrids / 15K tokens)
  - 4F: validation gate (population checksum, topological audit, geometric shift log)
- **Phase 5:** MCMC ensemble (B5) and compactness (C1, C2) — only if Phase 4 produces trustworthy geometry
- **Phase 6:** Final report compilation with Technical Data Statement and LaTeX formalism

## Phase 4C Skeleton Status

The skeleton implements stages 1-2 (parse Statement of Vote, structure dataframe). Stages 3-7 are stubs with implementation guidance:

- **Stage 3:** Build alberta_landmarks.csv from school district / community center directories (faster than rate-limited geocoding)
- **Stage 4:** Geocode unmatched polls via Nominatim (1 call/sec)
- **Stage 5:** Zero-Sum Verification — check geocoded polls fall in their 2019 ED
- **Stage 6:** Vision-based assignment to 2026 hybrid EDs
- **Stage 7:** Apportion Advance/Mobile/Special votes by Election Day spatial share

Run the skeleton first to verify the parse stage:
```
python3 analysis/v0_1_poll_attribution_skeleton.py
```

Should output: `Parsed 1973 poll records across 87 EDs` with two-party total `1,706,304`.

## What Could Block the Run

- **ABEBC shapefiles still not released:** Phase 4A blocked. Phase 4C is the recommended fallback and should produce measured (not approximated) vote totals for B1–B4 refinement, even without polygon geometry.
- **Geocoding failures:** if landmark dictionary + Nominatim can't resolve >90% of poll locations, the Zero-Sum Verification will flag too many failures and Phase 4C produces unreliable output. Document the failure rate honestly.
- **Network blocks:** Phase 4 needs internet for StatsCan downloads, OSM, Nominatim. Make sure the working environment allows outbound HTTPS.
- **Token budget exhaustion:** Hard cap of 150,000 for the agentic loop. Each phase has internal caps (15K for Phase 4D OSM hybrid reconstruction).

## Output Files (After the Run)

```
alberta_redistricting_audit_final.md          # the compiled report
migration.md                                  # session summary for next chat
analysis/
├── v0_1_section_A_population_equality.md
├── v0_1_section_C_geographic_coherence.md
├── v0_1_section_D_procedural.md
├── v0_1_section_4_geometry_provenance.md     # Phase 4 results
├── v0_1_section_B5_C1_C2_geometric_tests.md  # if Phase 5 succeeds
├── geometry_shift_log.md                     # any manual adjustments
├── borderline_poll_resolution.md             # vision-resolved hybrid edge cases
├── poll_geocoding_cache.csv                  # cached Nominatim results
├── alberta_landmarks.csv                     # built landmark dictionary
├── polls_2023_unified.csv                    # parsed Statement of Vote dataframe
├── electoral_forensics_population.py
└── geometry/                                 # if Phase 4 produces polygons
```

## Versioning

This is **starter pack v0.7**. Internal:
- Audit prompt: v0.8 (Phase 4C methodology hardened with Vote Anywhere handling)
- Data files: v0.1 (unchanged)
- Carry-forward analysis: v0.1 (B1–B4 completed)
- Phase 4C skeleton: v0.1 (parse stages working, geocoding/assignment/apportionment stubs)

## License & Provenance

All input data extracted from official Elections Alberta and ABEBC sources, verified against published totals (2023: 38 NDP / 49 UCP, two-party total 1,706,304; 2019: 24 NDP / 63 UCP; majority 2026 populations sum to exact provincial total of 4,888,723). Maps are images from the publicly tabled commission report. Analysis is non-partisan and applies identical methodology symmetrically to all three maps.
