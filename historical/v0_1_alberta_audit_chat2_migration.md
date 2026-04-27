Set chat title to: Alberta Boundaries Audit — Autonomous Execution (Chat 3)

# Migration MD — Alberta Electoral Boundaries Audit

**Closing chat:** alberta-gerrymander-audit (Chat 2)
**Next session:** Claude Code execution of the v0.7 bundle
**Built:** April 22, 2026

## Where the Project Stands

Two sessions of work completed across two claude.ai chats. Tests B1 through B4 (rigorous packing/cracking analysis) are done with verified findings. The infrastructure for the remaining work — Sections A, C, D, plus Phase 4 boundary acquisition and Phase 5 MCMC — is packaged for autonomous execution in Claude Code.

**Headline finding from completed work:** Majority 2026 plan preserves the 2019 partisan baseline. Minority 2026 plan shifts it 2 to 3 percentage points toward UCP across all four canonical tests, costing NDP 3 seats in the simulated 2023 outcome. Neither map crosses the 7% efficiency-gap threshold flagged in US case law. The signal is the directional consistency and the asymmetry between the two 2026 proposals from the same commission.

| Test | 2019 | Majority 2026 | Minority 2026 |
|---|---|---|---|
| B2 — Efficiency gap | −2.64% | −0.47% | +0.30% |
| B3 — Mean-median (NDP) | −2.22 pp | −2.15 pp | −0.01 pp |
| B4 — NDP seats at 50/50 | 46 | 47 | 43 |
| Sim 2023 outcome (NDP/UCP) | 38/49 | 38/51 | 35/54 |

## The Active Deliverable

**`v0_7_alberta_audit_naive_bundle.zip`** (1.24 MB) — drop into a fresh Claude Code working directory.

**Inside:**
- `CLAUDE.md` — Claude Code reads this on session start; points at the prompt
- `v0_8_gerrymander_audit_prompt.md` — the agentic execution plan, six phases
- `setup.sh` — installs Python deps for Phases 4–5 (geopandas, geopy, osmnx, gerrychain, openpyxl, rapidfuzz, pdfplumber)
- `data/` — four verified CSVs plus the raw 2023 Statement of Vote xlsx
- `analysis/` — B1–B4 carry-forward script (verified to produce the numbers above), B1–B4 results MD, B1–B4 visual HTML, Phase 4C poll attribution skeleton (parses 1,973 polls, stages 3–7 stubbed with implementation guidance)
- `maps/`, `source_maps/` — five extracted JPGs from the official commission report

## Run Instructions

```bash
unzip v0_7_alberta_audit_naive_bundle.zip
cd alberta_audit/
bash setup.sh
claude --effort xhigh
```

Claude Code reads `CLAUDE.md` automatically. First action it should take per CLAUDE.md instructions: run `python3 analysis/v0_1_packing_cracking_analysis.py` to verify the carry-forward baseline. If output matches the table above, proceed with Phase 1.

For the hardest portions of Phase 4 reconstruction and Phase 5 MCMC, bump to `--effort max`. Auto mode (Max subscribers) reduces permission prompts during the autonomous loop. Token budget cap of 150,000 is built into the prompt with internal sub-caps (15,000 for Phase 4D OSM hybrid reconstruction).

## Phase Status (What the Next Session Does)

| Phase | Section | Status | Blocker |
|---|---|---|---|
| 1 | A — Population equality | Ready | None — data in pack |
| 2 | C — Visual spatial audit | Ready | None — maps in pack |
| 3 | D — Procedural | Ready | None — desk research |
| 4A | Direct ABEBC shapefiles | Conditional | Released yet? Check `https://www.elections.ab.ca/resources/maps/` |
| 4B | DA dissolve | Likely blocked | DAUIDs probably not in PDF text — 3-min grep check before committing |
| 4C | Poll-location attribution | Ready | Skeleton in pack, stubs labeled |
| 4D | OSM street-network | Last resort | Capped at 11 hybrids / 15K tokens |
| 5 | B5 ensemble + C1/C2 | Conditional | Requires Phase 4 producing trustworthy geometry |
| 6 | Final report compilation | Will run | Synthesizes whatever Phases 1–5 produce |

## Integrity Gates Built Into the Prompt (Don't Bypass)

- **Symmetry discipline.** Same tests, same standards, every map.
- **Zero-Sum Verification (Phase 4C step 4).** Every geocoded poll must fall within its known 2019 ED before propagating to 2026 attribution.
- **Population Checksum (Phase 4F).** Reconstructed geometry's census population must be within 0.5% of official. Hard stop at 2%.
- **Geometric shift logging (Phase 4F).** Any manual adjustment goes in `geometry_shift_log.md` with delta and justification.
- **Total Vote Checksum (Phase 4C step 10).** Reconstructed votes must sum to NDP 777,404 / UCP 928,900 within 0.1% tolerance. Hard stop at 1%.
- **Honest blocking.** If geometry isn't trusted, do not fabricate B5/C1/C2 results. Report the block.

## Vote Anywhere Methodology Reminder

Of the 1,973 poll records in the 2023 Statement of Vote, only the 1,216 Election Day records are spatially valid as proxies for where voters live. The 757 Advance/Mobile/Special records are home-ED-attributed (voters could vote anywhere under the 2023 Vote Anywhere policy) and must be apportioned by Election Day spatial share, not directly geocoded. This is documented in Phase 4C steps 6–8 of the prompt.

## What This Audit Cannot Establish (And Why)

Even with everything in the bundle, two things remain out of reach until ABEBC releases proposed boundary shapefiles:
- **B5 (MCMC ensemble).** Generating 10,000+ alternative maps that meet the same legal criteria requires the actual proposed polygons. The strongest possible evidence for or against intentional gerrymandering remains pending.
- **C1, C2 (compactness).** Polsby-Popper and Reock scores need polygon geometry. Phase 4D OSM reconstruction can produce approximate polygons but not at the fidelity required for defensible scores.

If the audit's final form needs these tests, the next session after Claude Code execution should monitor `https://www.elections.ab.ca/resources/maps/` and run B5/C1/C2 when shapefiles drop. ABEBC has historically released them within weeks of tabling final reports.

## Lineage of Files Already in Outputs

For reference, these are the prior deliverables shipped to `/mnt/user-data/outputs/` in this chat lineage. Most are superseded by the v0.7 bundle — listed for completeness:

- `v0_1_alberta_minority_gerrymander_visual.html` — Calgary-only first visual (superseded but useful as a visual reference)
- `v0_1_alberta_gerrymander_migration.md` — earlier migration doc
- `v0_1_gerrymander_audit_starter_pack.zip` — superseded by v0.7
- `v0_2_gerrymander_audit_starter_pack.zip` — superseded
- `v0_3_gerrymander_audit_starter_pack.zip` — superseded
- `v0_4_alberta_audit_naive_bundle.zip` — superseded
- `v0_5_alberta_audit_naive_bundle.zip` — superseded
- `v0_6_alberta_audit_naive_bundle.zip` — superseded
- **`v0_7_alberta_audit_naive_bundle.zip`** — **CURRENT, USE THIS**
- Various `v0_X_gerrymander_audit_prompt.md` files — `v0_8` is current
- `v0_1_packing_cracking_analysis.py` — also bundled inside v0.7
- `v0_1_packing_cracking_results.md` — also bundled
- `v0_1_three_map_partisan_comparison.html` — also bundled
- `v0_1_majority_2026_populations.csv` — also bundled
- `build_three_map_visual.py` — script that built the comparison visual

## When the Claude Code Run Completes

The next-next session (Chat 4 of the lineage) will receive `alberta_redistricting_audit_final.md` and should:
1. Read the report
2. Verify the integrity-gate results (population checksum, vote checksum, geometric shift log entries)
3. Decide whether to publish, iterate, or wait for shapefiles
4. If publishing: convert to PDF for distribution, build any final visuals, draft outreach if relevant

## Discipline Reminders Worth Carrying Forward

These came up enough times in the prompt-iteration loop that they're worth restating:
- The signal is **directional consistency across multiple tests**, not extreme magnitude in any single one. Neither 2026 map crosses the US case-law gerrymandering threshold; the case rests on the asymmetry between two proposals from the same commission with the same data.
- The procedural question (commission rejected, MLA committee created) is **separate from but related to** the cartographic question. Treat in its own Section D, don't mix.
- "Final" is not a word that appears anywhere yet. The bundle is shippable; nothing is locked.
