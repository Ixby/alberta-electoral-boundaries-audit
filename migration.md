# Migration — Alberta Boundaries Audit

**Current state:** v0.10 published. Seven chat sessions in this chain. Dual-audience reports (public + academic) + accessible HTML, formal packing / cracking / engineered-boundary signature detection, per-redraw seat-consequence breakdown, alternatives-available analysis for all contested redraws, hybrid-count analysis vs government rationale, pre-registered checklist for identifying a gerrymander in the November 91-seat map.

**Working prompt for next session:** `v1_2_gerrymander_audit_prompt.md`.

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

---

## Quick start for a fresh Claude Code session

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit
cd alberta-electoral-boundaries-audit
bash setup.sh

# Verify the carry-forward baseline (Gate G0)
PYTHONIOENCODING=utf-8 python3 analysis/v0_2_packing_cracking_analysis.py
PYTHONIOENCODING=utf-8 python3 analysis/electoral_forensics_population.py
PYTHONIOENCODING=utf-8 python3 analysis/v0_3_monte_carlo_ci.py
PYTHONIOENCODING=utf-8 python3 analysis/v0_1_cross_election_rural_baseline.py
python3 analysis/check_voice_and_readability.py
```

If all five scripts produce output matching the tables in `report_academic.md` §3 and §A, the environment is good. The v1.2 prompt at project root then takes over.

---

## What each session accomplished

**Session 1 (prior chat).** B1–B4 on 2019 baseline + minority 2026 estimate. Section A skeleton. Section C visual audit of chair-flagged configurations.

**Session 2 (prior chat).** Section D procedural skeleton. Section 4 geometry provenance (shapefile-blocked). Initial compiled report.

**Session 3 (this chat, early).** v0.8 → v0.9 prompt fortifications. Dual-audience dual-report split. Bias audit found three class-A issues; remediated in symmetric v0.2 packing/cracking script. First stress-test pass (Monte Carlo CI crosses zero, declination disagrees, 2019 cross-election reverses).

**Session 4 (this chat, middle).** 2015 election data. Uncertainty / shapefile-impact analysis. Design critique. Academic literature review. PDF recon confirmed Appendix B prose-only; Appendix C majority-hybrid crosswalk extracted. v1.1 → v1.2 prompt made stress-test gates mandatory.

**Session 5 (this chat, middle-late).** Submission archive searched by sub-agent (1,252 of ~1,340). Chair's "no public support" claim partially refuted. Public report rewrite for subject-matter-naive audience. Academic APA citations. Accessible HTML dissemination. File structure cleaned (`deprecated/`, `drafts/`).

**Session 6 (this chat, late).** Signal-strength tiering of chair's refutation (3 of 7 precisely + effectively wrong). Reporter + document-designer subagents rewrote public report. Graphic designer redesigned palette (teal / ochre / slate / purple — no partisan colour read). SVG text clipping fixed. 338Canada integration (UCP projected blowout, audit reframed as structural/durable not 2027-specific). Bias disclosure. Sus/innocent-pattern framework. Defensibility audit gate DA1–DA7. Red-team renamed to stress-test.

**Session 7 (this chat, final).**
- **Per-redraw seat-consequence breakdown** in public report. Only two contested redraws move seat math materially: RMH-Banff Park s.15(2) (~+0.7 UCP seat) and Calgary Zone A packing (~1-2 NDP seats lost). Others affect representation quality, not seat count.
- **Formal packing / cracking / engineered-boundary signature detection** added to v1.2 prompt (P1–P3, C1–C3, E1–E3 criteria) and to both reports. Three signatures detected under minority, zero under majority.
- **Alternatives-available analysis** for all seven contested redraws. Six of seven had cleaner geographic alternatives that the minority did not take.
- **"What would a gerrymander in the 91-seat map actually look like"** pre-registered checklist in public report. Distinguishes strong signals (three minority signatures preserved + new patterns + ensemble-outlier or public-support inversion) from weak signals and process signals.
- **Hybrid-count analysis** vs government's stated rationale. Total hybrid count roughly constant (19/19/20). What changed is location: minority concentrates hybrids in Calgary (7 vs 4 majority) and Red Deer (4 vs 0 majority), with rural/small-town communities becoming numerical minorities inside Calgary-dominated hybrids. This is the reverse of the government's stated "preserve rural ridings" rationale. November 91-seat map choice between these two patterns is an explicit honesty test of the government's stated reason.

---

## Status by phase and test

| Phase / Test | Status | Confidence |
| --- | --- | --- |
| Carry-forward B1–B4 verification | Reproducible from v0.2 script | High |
| A1 Population MAD | Complete | High (CSV-sourced) |
| A2 Calgary zone gap | Complete, two classification rules | High |
| A2b Rural mean | Complete; refined interpretation | High structural; interpretation narrowed |
| A3 s.15(2) eligibility audit | Complete; 1/3 ridings flagged per map | Medium-low (hand-coded areas) |
| B1 Vote distribution histogram | Complete | 90% directional |
| B2 Efficiency gap | MC 95% CI crosses zero | 90% directional, qualified |
| B3 Mean-median | Complete | 90% directional, qualified |
| B4 NDP @ 50/50 | Complete | 90% directional, qualified |
| B6 Declination | Direction disagrees with B2/B3/B4 | Reported as disagreement |
| C3 Visual anomalies (minority) | 3 confirmed | High |
| C3 Visual anomalies (majority) | 0 Calgary; non-Calgary unimaged | Partial |
| C4 Community splits | Complete | High |
| **Formal signature detection (P/C/E)** | **3 detected under minority, 0 under majority** | **Criteria-driven, not inferential** |
| D Procedural | Tiered refutation | Narrowed |
| **Per-redraw seat breakdown** | **Complete** | **Mechanism-level, aggregate matches B4** |
| **Alternatives-available table** | **6 of 7 contested redraws had cleaner options** | **Geographic reasoning, case-by-case** |
| **Hybrid concentration analysis** | **Minority packs hybrids in Calgary/Red Deer** | **Contradicts government's stated rationale** |
| 4A Shapefiles | Not released by ABEBC | Blocked (external) |
| 4B DA dissolve | PDF has no DAUIDs | Blocked (structural) |
| 4C VA-polygon attribution | Substrate complete; Vision step not run | Ready-to-run |
| 4D OSM reconstruction | Not attempted | 15K token cap precluded |
| 4E Manual digitization | Out of scope | — |
| B5 MCMC ensemble | Requires shapefiles | Blocked |
| C1 Polsby-Popper | Requires shapefiles | Blocked |
| C2 Reock | Requires shapefiles | Blocked |
| 338Canada 2027 projection | Current snapshot cited (UCP blowout) | Useful as context |
| 91-seat proposal | Preliminary + November test checklist | LOW-SPECULATION on quantitative; pre-registered checklist on qualitative |

---

## Critical sub-findings to carry forward

1. **Structural findings are robust.** Population MAD (3,180 vs 4,707; minority 48% wider), Calgary Zone A−B gap (0.36% vs 12.20%), community splits, visible anomalies.
2. **Partisan-math is directional, not precise.** MC 95% CI [−2.99, +0.76] pp crosses zero; 90.5% direction. EG and declination disagree. 2019 cross-election flips sign.
3. **Chair's Appendix C is tiered.** 3 of 7 configurations: precisely AND effectively wrong (RMH-Banff Park, Olds-Three-Hills-Didsbury, Chestermere). 1 ambiguous (Red Deer). 3 effectively correct (Airdrie 4-way, Nolan Hill-Cochrane, St. Albert-Sturgeon minority variant).
4. **Rural 3.9% mean gap is not partisan packing.** Differential s.15(2) usage, not packing signature.
5. **338Canada April 2026 shows UCP blowout.** Audit reframed as "insurance policy" across multiple cycles, not 2027-specific.
6. **Three formal signatures detected under minority, zero under majority.** Packing (Calgary Zone A), cracking (Airdrie), engineered boundary (RMH-Banff Park). Criteria-driven detection.
7. **Six of seven contested redraws had cleaner alternatives.** Cochrane, Airdrie, RMH-Banff Park, Olds-3H-Didsbury, Chestermere, Red Deer all had natural non-Calgary / non-split options the minority did not take. Only St. Albert-Sturgeon had no meaningful alternative.
8. **Hybrid concentration contradicts government's rationale.** Total hybrids roughly constant (19/19/20) but minority concentrates them in Calgary (7 vs 4) and Red Deer (4 vs 0), making rural voters a minority in Calgary-dominated hybrids. This is the reverse of "preserve rural ridings."
9. **Rural NDP baseline varies 26.47% (2019) to 35.05% (2015).** MC uses Uniform(0.26, 0.36).
10. **Vote Anywhere is 47.2% of 2023 valid votes.** NDP +6pp higher rate than UCP.
11. **Phase 4C substrate complete.** VA polygons with attached votes; S3a/b/c all pass.
12. **Graphic neutrality.** Teal / ochre / slate / purple palette. Colour-blind safe; WCAG AA.
13. **Defensibility gate DA1–DA7 in prompt.**
14. **Pre-registered checklist for November 91-seat map.** Strong gerrymander signals vs weak vs process signals vs things-that-look-bad-but-aren't. Readers can apply this cold when the committee tables its map.

---

## What the next session should do (ordered by priority)

### Track A — Monitor for 2026 shapefile release
Watch `https://www.elections.ab.ca/resources/maps/`. When shapefiles release, execute Stage 2 of v1.2 (topology + population checksum) and Phase 5 (B5 GerryChain ensemble, C1 PP, C2 Reock). ~50K tokens, 1–2 hours.

### Track B — Phase 4C Vision-assignment execution
Substrate ready. Run Vision for 1,438 hybrid-adjacent VAs (prioritize 588 majority-hybrid-affected). Budget ~215K tokens. See `analysis/phase_4c_runbook.md`. Produces measured B1–B4 per map; collapses MC CI to a single value.

### Track C — November 2026 committee re-audit
When the MLA committee tables its 91-seat map (due Nov 2, 2026), re-run the full pipeline. Apply the pre-registered checklist in `report_public.md` §"What a gerrymander in the 91-seat map would actually look like." Apply the "alternatives-available" lens to each contested configuration. Count the Calgary and Red Deer hybrids; compare to the government's stated rural-preservation rationale.

### Track D — OCR the ~88 missing submissions
For legal-proceedings use only. ~30K tokens, 1 hour. Findings do not currently depend on this.

### Track E — 338Canada refresh
April 12 snapshot becomes stale within 60–90 days. Re-check and update public-report cite if projection has materially moved.

### Track F — Deeper academic citations
If submitting to a journal or legal proceedings, expand APA references per `analysis/v0_1_academic_literature_review.md`.

---

## Token spend across the chain

| Session | Approximate tokens |
| --- | --- |
| 1–2 (prior chats) | ~80K |
| 3 (v0.8 → v1.0 prompts) | ~120K |
| 4 (v1.0 → v1.2 + data + literature) | ~100K |
| 5 (submission search + cleanup + HTML) | ~60K |
| 6 (reporter + designer + 338 + signal-strength + sus/innocent) | ~100K |
| 7 (seat-consequences + signatures + alternatives + hybrid analysis + November checklist) | ~70K |
| Background sub-agents across all sessions | ~550K |

Total approximate across this chat chain: ~1.08M tokens. Sub-agents absorbed ~550K, keeping parent sessions well inside budget.

---

## Key files for the next session to read first

1. `CLAUDE.md` — project orientation, house voice, repository layout, sub-agent-use guidance
2. `v1_2_gerrymander_audit_prompt.md` — execution prompt with stages, stress-test gates, defensibility audit gates DA1–DA7, signature-detection criteria
3. `report_public.md` — current public findings in journalist voice (grade 9.4)
4. `report_academic.md` — current academic findings with APA citations, signatures §3.7–3.10 (grade 12.8)
5. `report.html` — accessible HTML with four SVG charts, sus-dot indicators, partisan-neutral palette
6. `analysis/v0_1_claim_significance_analysis.md` — tiered chair's-claim refutation
7. `analysis/v0_1_data_preparation.md` — from-raw reproduction pipeline for every dataset
8. `analysis/v0_1_uncertainty_and_shapefile_impact.md` — what shapefile release would change
9. `analysis/v0_1_prompt_readiness.md` — v1.1→v1.2 readiness assessment
10. `analysis/phase_4c_runbook.md` — Phase 4C Vision-assignment playbook
11. `analysis/v0_1_338canada_integration.md` — polling-snapshot integration
12. `analysis/v0_1_91_seat_preliminary.md` — speculative 91-seat analysis
13. `analysis/v0_1_marginal_seats_findings.md` — concrete seat-level flip scenarios
14. `analysis/v0_1_rural_gap_findings.md` — why 3.9% rural mean is not partisan packing

---

## Open questions for the PO

1. Is v0.10 ready to share publicly, or should it hold for Track A/B/C completion?
2. If sharing now: which channel (print, social, academic submission, legal)? Each may inform a v1.0 revision.
3. Should OCR of the 88 missing submissions be prioritized, or deferred until legal use emerges?
4. After the November committee tables its map, what is the re-audit timeline? (The checklist is pre-registered; the data substrate is ready.)
5. Does the dual-audience model (public + academic + HTML) meet distribution needs, or is a fourth format (PDF, presentation deck, newsletter excerpt) needed?

---

## Fresh-chat instructions

1. Read `CLAUDE.md` first.
2. Read `v1_2_gerrymander_audit_prompt.md` for execution steps.
3. Run the five baseline scripts; confirm output matches documented tables.
4. Check `https://www.elections.ab.ca/resources/maps/` for 2026 shapefile release status.
5. Check if the November committee has tabled its 91-seat map yet. If yes, Track C is the top priority. If no, Track B.
6. Pick the active track from the priority list above.
7. Consult the appropriate runbook (`phase_4c_runbook.md` for Track B; re-audit playbook in `report_public.md` §"What a gerrymander..." for Track C).
8. Use sub-agents for multi-file research, parallel tasks, web fetches, validation passes, data acquisition, and anything over 15K tokens. See CLAUDE.md §"Use Sub-Agents Whenever Possible."
9. Commit intermediate work as you go; never claim "final" — everything is versioned.

The repository is at v0.10. The next commit should increment the appropriate version (v0.10 → v0.11 for revisions, v0.10 → v1.0 for a locked release).

---

*Migration doc v0.10. Authored April 22, 2026 at the close of session 7. If the next session diverges materially from the documented state, update this file first before making downstream changes.*
