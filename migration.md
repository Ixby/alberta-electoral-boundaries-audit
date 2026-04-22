# Migration — Alberta Boundaries Audit

**Current state:** v0.11 published. Eight chat sessions in this chain. Dual-audience reports (public + academic) + accessible HTML. Formal signature detection (packing, cracking, engineered-boundary). Per-redraw seat-consequence breakdown. Alternatives-available analysis for all contested redraws. Population-math tests run against five minority justifications (all five fail). Hybrid-count vs government-rationale analysis. Pre-registered checklist for identifying a gerrymander in the November 91-seat map.

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
PYTHONIOENCODING=utf-8 python3 analysis/v0_1_justification_tests.py
python3 analysis/check_voice_and_readability.py
```

If all six scripts produce output matching the documented tables, the environment is good. The v1.2 prompt then takes over.

---

## Tracks, ordered by timeliness

Tracks are ordered by what can start first. Immediate tracks need no external data release or time gate. Time-bounded tracks decay if deferred. Date-gated tracks must wait.

### Immediate — can start today

Order these by the next session's priorities.

**Track G — StatsCan journey-to-work verification for Cochrane.** Highest value for cost. Download StatsCan table 98-10-0438 (journey-to-work flows by census subdivision) and compute Cochrane→central Calgary versus Cochrane→Nolan Hill/NW suburbs flows. If central Calgary dominates (expected), the commuter defence for the Nolan Hill-Cochrane minority hybrid is formally falsified. Estimated cost: ~25K tokens, 30 minutes. No dependencies.

**Track B — Phase 4C Vision-assignment execution.** Substrate is ready: `data/va_polygons_with_2023_votes.gpkg` is validated (gates S3a/b/c all pass), `data/hybrid_adjacent_vas.csv` narrows the Vision work to 1,438 VAs (prioritize the 588 majority-hybrid-affected). Produces measured B1–B4 per map and collapses the Monte Carlo CI to a single value. Playbook in `analysis/phase_4c_runbook.md`. Estimated cost: ~215K tokens, 2–4 hours.

**Track H — Community-of-interest analysis at CSD level.** New. Use `data/alberta_2021_csds.gpkg` + `data/alberta_2021_csd_populations.csv` + hybrid crosswalks to compute, per map, how many census subdivisions are split across multiple districts versus kept whole. Formalizes the community-of-interest discussion currently in §C4 with verifiable counts. Estimated cost: ~20K tokens, 30 minutes.

**Track D — OCR the 88 missing submissions.** Only do this if the audit is headed toward legal proceedings or a journal submission. The main findings do not depend on it; the chair's claim refutation rests on identified counter-examples. Estimated cost: ~30K tokens, 1 hour.

**Track F — Deeper academic citations.** Only if submitting to a journal. Expand APA references per `analysis/v0_1_academic_literature_review.md` with the full Chen-Rodden, Courtney, Pal, Stephanopoulos-McGhee set. Estimated cost: ~15K tokens, 45 minutes. Pure writing, no analysis.

### Time-bounded — refresh before staleness

**Track E — 338Canada refresh.** The April 12, 2026 snapshot in the current public report becomes stale within 60–90 days. Re-check `https://338canada.com/alberta/` at the start of any session after June 2026. If the projection has moved materially, update the public report's Section "Why 2027 is where this actually lands." Estimated cost: ~10K tokens, 15 minutes. Recurring.

### Date-gated — wait for external events

**Track A — 2026 shapefile release.** Watch `https://www.elections.ab.ca/resources/maps/` at the start of every session. Historical Elections Alberta practice releases shapefiles after a map is legislatively adopted. Probable release window: late 2026 to early 2027, possibly after the November committee tables its map. When shapefiles release, execute Stage 2 of v1.2 (topology + population checksum) and Phase 5 (B5 GerryChain ensemble, C1 Polsby-Popper, C2 Reock). Unblocks: measured attribution, proper compactness scores, ensemble-outlier test. Estimated cost: ~50K tokens, 1–2 hours.

**Track C — November 2026 committee re-audit.** The UCP-majority MLA committee chaired by Brandon Lunty is due to report November 2, 2026 with a 91-seat map. When the map is tabled:

1. **Run the pre-registered signature-detection checklist** from `report_public.md` §"What a gerrymander in the 91-seat map would actually look like." Count Calgary hybrids (minority: 7, majority: 4). Check for the three minority signatures (Nolan Hill-Cochrane lasso, Airdrie 4-way, RMH-Banff Park engineered boundary) surviving into the new map.
2. **Apply the alternatives-available lens** to every new contested configuration.
3. **Re-run the population-math tests** from `analysis/v0_1_justification_tests.py` against the committee's stated rationales.
4. **Compare hybrid concentration** against the government's "rural preservation" stated reason.
5. If shapefiles are released for the new map, run Phase 5 ensemble.

Estimated cost: ~80K tokens, 1–2 hours for the baseline re-audit; ~50K more if ensemble runs.

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
| Formal signature detection (P/C/E) | 3 detected under minority, 0 under majority | Criteria-driven |
| D Procedural | Tiered refutation | Narrowed |
| Per-redraw seat breakdown | Complete | Mechanism-level |
| Alternatives-available table | 6 of 7 contested redraws had cleaner options | Geographic reasoning |
| **Population-math tests (5 tested)** | **All 5 FAIL — minority configurations not forced by math** | **Quantitative, CSD-sourced** |
| Hybrid concentration analysis | Minority packs hybrids in Calgary/Red Deer | Contradicts government rationale |
| 4A Shapefiles | Not released by ABEBC | Blocked (external) |
| 4B DA dissolve | PDF has no DAUIDs | Blocked (structural) |
| 4C VA-polygon attribution | Substrate complete; Vision step not run | Ready-to-run |
| 4D OSM reconstruction | Not attempted | 15K token cap precluded |
| 4E Manual digitization | Out of scope | — |
| B5 MCMC ensemble | Requires shapefiles | Blocked |
| C1 Polsby-Popper | Requires shapefiles | Blocked |
| C2 Reock | Requires shapefiles | Blocked |
| 338Canada 2027 projection | Current snapshot cited (UCP blowout); refresh every 60-90 days | Useful as context |
| 91-seat proposal | Preliminary + pre-registered November checklist | LOW-SPECULATION quantitative; checklist ready |
| Journey-to-work test (Nolan Hill-Cochrane) | Not yet run (Track G) | Ready to run |
| CSD-level community splits (Track H) | Not yet run | Ready to run |

---

## Critical sub-findings to carry forward

1. **Structural findings are robust.** Population MAD (3,180 vs 4,707), Calgary Zone A−B gap (0.36% vs 12.20%), community splits, visible anomalies.
2. **Partisan-math is directional, not precise.** MC 95% CI [−2.99, +0.76] pp crosses zero; 90.5% direction consistency.
3. **Chair's Appendix C is tiered.** 3 of 7 configurations precisely + effectively wrong, 1 ambiguous, 3 effectively correct.
4. **Rural 3.9% mean gap is not partisan packing.** Differential s.15(2) usage.
5. **338Canada April 2026: UCP blowout projected.** Audit reframed as "insurance policy," not 2027-specific.
6. **Three formal signatures detected under minority, zero under majority.** Packing (Calgary Zone A), cracking (Airdrie), engineered boundary (RMH-Banff Park).
7. **Six of seven contested redraws had cleaner alternatives.** Only St. Albert-Sturgeon had none.
8. **Five minority justifications tested against population math. All five failed.** None of the contested configurations were required by population or area rules.
9. **Hybrid concentration contradicts government's rural-preservation rationale.** Minority packs hybrids in Calgary (7) and Red Deer (4), diluting rural voices into urban majorities.
10. **Commuter-tie defence for Nolan Hill-Cochrane is geographically weak.** Cochrane commuters travel to central Calgary, not a NW residential suburb. StatsCan 98-10-0438 would formally falsify if Track G runs.
11. **Rural NDP baseline varies 26.47% (2019) to 35.05% (2015).** MC uses Uniform(0.26, 0.36).
12. **Vote Anywhere is 47.2% of 2023 valid votes.** NDP +6pp higher rate than UCP.
13. **Phase 4C substrate complete.** Gates S3a/b/c pass.
14. **Graphic neutrality.** Teal / ochre / slate / purple palette.
15. **Defensibility gate DA1–DA7 in prompt.** Every number must trace, recomputable, label speculation.
16. **Pre-registered checklist for November 91-seat map.** Strong signals vs weak vs process signals.
17. **Airdrie 2021 population is 74,100, not 84,000.** Commission data correction noted.

---

## Token spend across the chain

| Session | Approximate tokens |
| --- | --- |
| 1–2 (prior chats) | ~80K |
| 3 (v0.8 → v1.0 prompts) | ~120K |
| 4 (v1.0 → v1.2 + data + literature) | ~100K |
| 5 (submission search + cleanup + HTML) | ~60K |
| 6 (reporter + designer + 338 + signal-strength + sus/innocent) | ~100K |
| 7 (seat-consequences + signatures + alternatives + hybrid analysis) | ~70K |
| 8 (commuter examination + population-math tests) | ~50K |
| Background sub-agents across all sessions | ~600K |

Total approximate across this chat chain: ~1.18M tokens. Sub-agents absorbed ~600K, keeping parent sessions well inside budget.

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
15. `analysis/v0_1_justification_tests_findings.md` — five minority justifications tested; all failed

---

## Open questions for the PO

1. Is v0.11 ready to share publicly, or should it hold for Track B/G/H completion? (Tracks A and C are external/date-gated.)
2. If sharing now: which channel (print, social, academic submission, legal)? Each may inform a v1.0 revision.
3. Should OCR of the 88 missing submissions be prioritized (Track D), or deferred until legal use emerges?
4. Does the dual-audience model (public + academic + HTML) meet distribution needs, or is a fourth format needed?
5. After Nov 2, 2026 is the committee's 91-seat map tabled? If yes, Track C is the top priority. If no, Track B or G.

---

## Fresh-chat instructions

1. Read `CLAUDE.md` first.
2. Read `v1_2_gerrymander_audit_prompt.md` for execution steps.
3. Run the six baseline scripts; confirm output matches documented tables.
4. Check `https://www.elections.ab.ca/resources/maps/` for 2026 shapefile release status.
5. Check whether the November committee has tabled its 91-seat map (news search or direct URL at the commission's page).
6. Pick the active track from the timeliness-ordered list above.
7. Consult the appropriate runbook (`phase_4c_runbook.md` for Track B; re-audit playbook in `report_public.md` §"What a gerrymander..." for Track C).
8. Use sub-agents for multi-file research, parallel tasks, web fetches, validation passes, data acquisition, and anything over 15K tokens. See CLAUDE.md §"Use Sub-Agents Whenever Possible."
9. Commit intermediate work as you go; never claim "final" — everything is versioned.

The repository is at v0.11. The next commit should increment the appropriate version (v0.11 → v0.12 for revisions, v0.11 → v1.0 for a locked release).

---

*Migration doc v0.11. Authored April 22, 2026 at the close of session 8. Tracks ordered by timeliness. If the next session diverges materially from the documented state, update this file first before making downstream changes.*
