# Migration — Alberta Boundaries Audit

**Current state:** v0.9 published. Dual-audience reports (public + academic), accessible HTML dissemination with partisan-neutral palette, SVG clipping fixes, 338Canada integration, sus/innocent-pattern framework, bias disclosure, defensibility audit gate DA1–DA7 in the prompt. Structural findings stable across multiple stress-test passes; partisan-math findings qualified at directional confidence.

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

## What each session in this chain accomplished

**Session 1 (prior chat).** B1–B4 on 2019 baseline + minority 2026 estimate. Section A skeleton. Section C visual audit of chair-flagged configurations.

**Session 2 (prior chat).** Section D procedural skeleton. Section 4 geometry provenance (shapefile-blocked). Initial compiled report.

**Session 3 (current chat, early).** v0.8 → v0.9 prompt fortifications. Dual-audience dual-report split. Bias audit found three class-A issues; remediated in symmetric v0.2 packing/cracking script. First stress-test pass (Monte Carlo CI crosses zero, declination disagrees with efficiency gap, 2019 cross-election reverses direction).

**Session 4 (current chat, middle).** Added 2015 election data. Uncertainty / shapefile-impact analysis. Design critique. Academic literature review. PDF recon confirmed Appendix B is prose-only; Appendix C majority-hybrid crosswalk extracted. v1.1 → v1.2 prompt made stress-test gates mandatory.

**Session 5 (current chat, middle-late).** Submission-archive sub-agent searched 1,252 of ~1,340 submissions. Chair's "no public support" claim partially refuted. Public report rewritten for subject-matter-naive audience. Academic APA citations. Accessible HTML dissemination built. File structure cleaned (`deprecated/`, `drafts/`).

**Session 6 (current chat, late).** Signal-strength analysis tiered the chair's refutation (precisely wrong, precisely + effectively wrong, effectively correct). Reporter + document-designer subagents rewrote public report in journalistic voice with visual hierarchy. Graphic designer redesigned palette (teal/ochre/slate/purple; no blue/orange partisan-read). SVG text clipping fixed. 338Canada integration (UCP projected blowout, reframes audit as structural/durable not 2027-specific). Bias disclosure. Sus/innocent-pattern framework. Defensibility audit gate DA1–DA7. Red-team terminology renamed to stress-test.

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
| D Procedural | Partially refuted, tiered | Narrowed |
| 4A Shapefiles | Not released by ABEBC | Blocked (external) |
| 4B DA dissolve | PDF has no DAUIDs | Blocked (structural) |
| 4C VA-polygon attribution | Substrate complete; Vision step not run | Ready-to-run |
| 4D OSM reconstruction | Not attempted | 15K token cap precluded |
| 4E Manual digitization | Out of scope | — |
| B5 MCMC ensemble | Requires shapefiles | Blocked |
| C1 Polsby-Popper | Requires shapefiles | Blocked |
| C2 Reock | Requires shapefiles | Blocked |
| 338Canada 2027 projection integration | Current snapshot cited | Useful as context |
| 91-seat proposal preliminary | Speculative with labels | LOW-SPECULATION |

---

## Critical sub-findings to carry forward

1. **Structural findings are robust.** Population MAD (3,180 vs 4,707; minority 48% wider), Calgary Zone A−B gap (0.36% vs 12.20%), community splits (Airdrie 2 vs 4), visible anomalies (0 vs 3).
2. **Partisan-math is directional, not precise.** MC 95% CI [−2.99, +0.76] pp crosses zero; 90.5% direction consistency. EG and declination disagree. 2019 cross-election flips sign.
3. **Chair's Appendix C is tiered.** 3 of 7 configurations: precisely AND effectively wrong (RMH-Banff Park, Olds-Three-Hills-Didsbury, Chestermere). 1 of 7: ambiguous (Red Deer hybrids). 3 of 7: effectively correct (Airdrie 4-way, Nolan Hill-Cochrane, St. Albert-Sturgeon minority variant). Strongest counter-example: EBC-2025-2-0619 explicitly proposes "Rocky Mountain House-Banff."
4. **Rural 3.9% mean gap is NOT partisan packing.** Both maps pack smallest rural EDs into ~68–70% UCP territory. Gap comes from differential s.15(2) usage.
5. **338Canada April 2026 snapshot shows a UCP blowout.** 52% / 38%; UCP majority odds >99%. The "close race" premise of the first draft was wrong. Audit reframed as "insurance policy" across multiple election cycles.
6. **Rural NDP baseline varies 26.47% (2019) to 35.05% (2015).** MC samples `rural_ndp_share ~ Uniform(0.26, 0.36)`.
7. **Vote Anywhere is 47.2% of 2023 valid votes.** NDP +6pp higher rate than UCP. 70/30 blend likely under-estimates the minority shift.
8. **Phase 4C substrate complete.** `data/va_polygons_with_2023_votes.gpkg` (4,765 polygons with per-party EDay totals). S3a/S3b/S3c all pass.
9. **Hybrid crosswalks acquired.** Majority via Appendix C; minority heuristic + Appendix E pp 307–308.
10. **Graphic neutrality.** Palette is teal/ochre/slate/purple; no blue/orange partisan-read. Colour-blind safe; WCAG AA; dark-mode aware.
11. **Defensibility gate DA1–DA7 in prompt.** Every number must trace to script + data; be recomputable; have characterization provenance; be labelled if speculative; cite legal authority correctly; include bias disclosure; acknowledge alternative framings.

---

## What the next session should do (ordered by priority)

### Track A — Monitor for 2026 shapefile release
Watch `https://www.elections.ab.ca/resources/maps/`. When shapefiles release, execute Stage 2 of v1.2 (topology + population checksum) and Phase 5 (B5 GerryChain ensemble, C1 PP, C2 Reock). ~50K tokens, 1–2 hours.

### Track B — Phase 4C Vision-assignment execution
Substrate ready. Run Vision assignment for 1,438 hybrid-adjacent VAs (prioritize 588 majority-hybrid-affected). Budget ~215K tokens. See `analysis/phase_4c_runbook.md`. Produces measured B1–B4 per map; collapses MC CI to a single value.

### Track C — November 2026 committee re-audit
When the MLA committee tables its map (Nov 2, 2026), re-run the full pipeline. If the committee keeps Nolan Hill-Cochrane and Airdrie 4-way, partisan-concern extends. If it drops those and keeps publicly-supported configurations, concern weakens.

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
| 3 (current chat, v0.8→v1.0 prompts) | ~120K |
| 4 (v1.0→v1.2 + data + literature) | ~100K |
| 5 (submission search + cleanup + HTML) | ~60K |
| 6 (reporter + designer + 338 + signal-strength + sus/innocent) | ~100K |
| Background sub-agents across all sessions | ~500K |

Total approximate: ~960K tokens. Sub-agents took ~500K of that, keeping parent sessions well inside budget.

---

## Key files for the next session to read first

1. **`CLAUDE.md`** — project orientation, house voice, repository layout
2. **`v1_2_gerrymander_audit_prompt.md`** — execution prompt with stages, stress-test gates, defensibility audit gates DA1–DA7
3. **`report_public.md`** — current public findings in journalist voice
4. **`report_academic.md`** — current academic findings with APA citations
5. **`report.html`** — accessible HTML with four SVG charts and sus-dot indicators
6. **`analysis/v0_1_claim_significance_analysis.md`** — tiered chair's-claim refutation
7. **`analysis/v0_1_data_preparation.md`** — from-raw reproduction pipeline for every dataset
8. **`analysis/v0_1_uncertainty_and_shapefile_impact.md`** — what shapefile release would change
9. **`analysis/v0_1_prompt_readiness.md`** — v1.1→v1.2 readiness assessment
10. **`analysis/phase_4c_runbook.md`** — Phase 4C Vision-assignment playbook
11. **`analysis/v0_1_338canada_integration.md`** — current polling snapshot and integration rationale
12. **`analysis/v0_1_91_seat_preliminary.md`** — speculative 91-seat analysis
13. **`analysis/v0_1_marginal_seats_findings.md`** — concrete seat-level flip scenarios
14. **`analysis/v0_1_rural_gap_findings.md`** — why 3.9% rural mean is not partisan packing

---

## Open questions for the PO

1. Is v0.9 ready to share publicly, or should it hold for Track A/B/C completion?
2. If sharing now: which channel (print, social, academic submission, legal)? Each may inform a v1.0 revision.
3. Should OCR of the 88 missing submissions be prioritized, or deferred until legal use emerges?
4. After the November committee tables its map, what's the re-audit timeline?
5. Does the dual-audience model (public + academic + HTML) meet distribution needs, or is a fourth format (PDF, presentation deck, newsletter excerpt) needed?

---

## Fresh-chat instructions

1. Read `CLAUDE.md` first.
2. Read `v1_2_gerrymander_audit_prompt.md` for execution steps.
3. Run the five baseline scripts; confirm output matches documented tables.
4. Check `https://www.elections.ab.ca/resources/maps/` for 2026 shapefile release status.
5. Pick the active track from the priority list above.
6. Consult the appropriate runbook.
7. Commit intermediate work as you go; never claim "final" — everything is versioned.
8. Use sub-agents for multi-file research, parallel tasks, web fetches, validation passes, data acquisition, and anything over 15K tokens (see CLAUDE.md §"Use Sub-Agents Whenever Possible").

The repository is at v0.9. The next commit should increment the appropriate version (v0.9 → v0.10 for revisions, v0.9 → v1.0 for a locked release).

---

*Migration doc v0.9. Authored April 22, 2026. If the next session diverges materially from the documented state, update this file first before making downstream changes.*
