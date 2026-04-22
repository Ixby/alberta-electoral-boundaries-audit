# Alberta Electoral Boundaries Audit — Project Root

You are a fresh Claude Code instance arriving at a partially-completed multi-session audit. **Your full instructions are in `v0_8_gerrymander_audit_prompt.md`. Read that file first, then execute the agentic plan it contains.**

## Quick Orientation

**What this project is.** A non-partisan, evidence-based forensic audit of Alberta's 2025–26 Electoral Boundaries Commission proposals. Three maps under evaluation: the 2019 boundaries (in force), the independent commission's majority recommendation, and the government appointees' minority recommendation.

**What's done.** A previous session completed Tests B1 through B4 (efficiency gap, mean-median, seats-votes, vote distribution histogram). All input data is extracted and verified against official totals. Findings: majority preserves the 2019 partisan baseline; minority shifts it 2 to 3 percentage points toward UCP across all four tests.

**What you are doing.** Phases 1–6 in the prompt. The most important addition in v0.7: **Phase 4C poll-location attribution** is now the recommended fallback for boundary acquisition. It uses the 2023 Statement of Vote's ~5,000 polling stations, geocodes them, validates against 2019 ED membership (Zero-Sum Verification gate), then uses Opus 4.7 vision to assign Election Day polls to new 2026 boundaries. Apportions Advance/Mobile/Special votes by Election Day spatial share to handle Vote Anywhere correctly.

**Skeleton script provided.** `analysis/v0_1_poll_attribution_skeleton.py` does the data loading and dataframe structuring. Stages 3-7 are stubs with implementation guidance — start there rather than from scratch.

## Repository Layout

```
.
├── CLAUDE.md                                  # this file
├── README.md                                  # human-facing setup notes
├── v0_8_gerrymander_audit_prompt.md           # YOUR INSTRUCTIONS — READ FIRST
├── setup.sh                                   # installs Python deps for Phases 4–5
├── data/
│   ├── v0_1_alberta_2023_results.csv          # 87 EDs, candidate-level 2023 totals
│   ├── v0_1_alberta_2019_results.csv          # 87 EDs, 2019 baseline
│   ├── v0_1_majority_2026_populations.csv     # 89 majority-proposed EDs
│   ├── v0_1_minority_2026_populations.csv     # 89 minority-proposed EDs
│   └── 2023_results.xlsx                      # raw Statement of Vote (87 sheets, poll-level)
├── analysis/
│   ├── v0_1_packing_cracking_analysis.py      # B1–B4 reproducible (RUN FIRST to verify)
│   ├── v0_1_packing_cracking_results.md       # B1–B4 written findings
│   ├── v0_1_three_map_partisan_comparison.html  # B1–B4 visual
│   └── v0_1_poll_attribution_skeleton.py      # Phase 4C starting framework (NEW in v0.6)
├── maps/
│   ├── majority_calgary.jpg                   # Appendix A, p. 72 of final report
│   └── minority_calgary.jpg                   # Appendix E, p. 74
└── source_maps/
    ├── minority_alberta_overview.jpg          # Appendix E, p. 73
    ├── minority_edmonton.jpg                  # Appendix E, p. 75
    └── minority_other_cities.jpg              # Appendix E, p. 76
```

## First Action (Verify the Baseline)

Run `python3 analysis/v0_1_packing_cracking_analysis.py` and confirm the output matches:

```
2019 BOUNDARIES (CURRENT) under 2023 vote shares
  Districts: 87, NDP 38, UCP 49
  B2 Efficiency gap: -2.64%
  B3 Mean-median (NDP): -2.22 pp
  B4 NDP at 50/50: 46

MINORITY 2026 PROPOSAL (estimated) under 2023 vote shares
  Districts: 89
  B2 Efficiency gap: +0.30%
  B3 Mean-median (NDP): -0.01 pp
  B4 NDP at 50/50: 43
```

If the output matches, the carry-forward state is verified.

## Second Action (Verify the Skeleton)

Run `python3 analysis/v0_1_poll_attribution_skeleton.py` and confirm it parses 1973 poll records (1216 Election Day, 341 Advance, 242 Mobile, 174 Special Ballot) with two-party total 1,706,304. The stubs will print `[STUB] ... implement before running` — that's expected. Implement them as you proceed through Phase 4C.

## Dependencies

Carry-forward script: standard library only.

Phase 4C skeleton parsing: needs `openpyxl` (run `bash setup.sh` to install).

Phase 4C full pipeline + Phase 5: needs `geopandas`, `geopy`, `osmnx`, `gerrychain` etc. — also installed by `setup.sh`.

## Critical Discipline Reminders

- **Symmetry.** Every test, every map. If you flag a packing/cracking signal in the minority plan, check whether the equivalent move appears in the majority plan and the 2019 baseline.
- **Vote Anywhere handling.** Only Election Day polls are spatially valid. Advance/Mobile/Special votes are home-ED-attributed regardless of physical location and must be apportioned by Election Day spatial share, not direct geocoding.
- **Zero-Sum Verification gate.** Every geocoded poll must fall within its known 2019 ED before propagating to 2026 attribution. If "Acadia Community Hall" geocodes to Edmonton, the geocoder is wrong — discard or re-geocode.
- **Geometric shift logging.** Any manual adjustment to make a checksum pass goes in `analysis/geometry_shift_log.md` with delta and justification. No silent transformations.
- **Honest blocking.** If Phase 4 fails the population checksum (variance >2%), do not proceed to Phase 5 with bad geometry. Report the block cleanly.

## Style Notes for the Project Owner (Wuff / Will Conner)

- Plain, grounded, conversational prose. No mirrored "not X — Y" reversals. No templated triads. No emoji. No editorializing reactions.
- Versioning convention: `major.minor`. `x.0` is locked, `x.1+` is revisions. Files use the version as a filename prefix (`v0_1_filename.ext`). Paired files share version. Never describe anything as "final."
- When you finish, write outputs as markdown files into `analysis/`. The compiled report goes to project root as `alberta_redistricting_audit_final.md`.

## When You Are Done

Write a brief migration MD at project root named `migration.md` containing: phases completed, phases blocked (with reason), token spend, and recommended next session topic. Title format: `Set chat title to: Alberta Boundaries Audit — [Phase] (Chat N)` where N increments from previous sessions (this is at minimum Chat 5 if continuing the lineage).
