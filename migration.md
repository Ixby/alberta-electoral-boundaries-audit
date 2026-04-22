# Migration — Alberta Boundaries Audit

**Current state:** v0.13 published. Nine chat sessions in this chain. Dual-audience reports (public + academic) + accessible HTML. Formal signature detection (packing, cracking, engineered-boundary). Per-redraw seat-consequence breakdown. Alternatives-available analysis for all contested redraws. Population-math tests run against five minority justifications (all five fail). Hybrid-count vs government-rationale analysis. Pre-registered checklist for identifying a gerrymander in the November 91-seat map. Session 9 additions: 25-rationale inventory and validation with three contradicted claims (two shared-schools, one 91-seat framing); Cochrane journey-to-work from StatsCan Table 98-10-0459 (Calgary-bound 35.8% of out-commuters; within-Calgary destination not testable); CSD-level community-splits count as bounding null; 338Canada per-riding cross-validation confirming the 1-seat structural asymmetry survives both 2023 votes and April 2026 polling; close reading of Chair Miller's Recommendation 5 addendum identifying form-match / conditions-pending / intent-inverted relationship to the April 16 motion; AI-use framework for the November committee (non-partisan, five disciplines, nine-item disclosure checklist); partial OCR of the 88 non-text-layer submissions (14 recovered, 1 new hit supporting Rocky Mountain House-Banff configuration).

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

**Track G — StatsCan journey-to-work verification for Cochrane.** *Closed in session 9.* Correct table is StatsCan 98-10-0459 (98-10-0438 as listed in the v0.11 migration doc does not exist in the WDS catalogue; the correct PID was substituted on execution). Output: 49.2% of Cochrane workers work inside Cochrane, 35.8% commute to Calgary, 4.0% to Rocky View, 2.2% to Canmore, 1.5% to Airdrie. The CSD-level evidence **does not formally falsify** the minority's commuter-tie defence, contrary to the v0.11 migration doc's prediction: the 2021 public release collapses Calgary into a single CSD, so within-Calgary destination is not directly testable, and the inference that Cochrane→Calgary commuters do not target Nolan Hill rests on the separate fact that Nolan Hill is a quiet residential neighbourhood without significant employment. Verdict revised to INCONCLUSIVE at CSD resolution; prior against the minority's specific pairing but not formal refutation. Full method in `analysis/v0_1_cochrane_journey_to_work.md`.

**Track B — Phase 4C Vision-assignment execution.** *Still pending.* Substrate is ready: `data/va_polygons_with_2023_votes.gpkg` is validated (gates S3a/b/c all pass), `data/hybrid_adjacent_vas.csv` narrows the Vision work to 1,438 VAs (prioritize the 588 majority-hybrid-affected). Produces measured B1–B4 per map and collapses the Monte Carlo CI to a single value. Playbook in `analysis/phase_4c_runbook.md`. Estimated cost: ~215K tokens, 2–4 hours. **Value reassessment needed:** with the 89-seat commission proposals set aside by the April 16 motion, the precision gain on proposal-specific B1–B4 is marginal; the value of Phase 4C is now primarily cross-validation rather than primary measurement.

**Track H — Community-of-interest analysis at CSD level.** *Closed in session 9.* Per-map CSD splits: 2019 66 of 191 (34.6%); Majority 2026 66 of 191 (34.6%, inferred); Minority 2026 lower-bound 54 of 191 (28.3%) to upper-bound 66. Confident-only subset (n=139, excluding uncertainties): identical 40 splits under all three maps. Conclusion: majority-minority asymmetry in §C4 operates at within-ED partition resolution, not at CSD granularity, and is not measurable without 2026 shapefiles. Full method in `analysis/v0_1_csd_community_splits.md`.

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
| 338Canada per-riding cross-validation (Track J) | Complete — r=0.960 per-riding, same 1-seat asymmetry under 2023 votes and April 2026 polling | Structural finding validated |
| 91-seat proposal | Preliminary + pre-registered November checklist | LOW-SPECULATION quantitative; checklist ready |
| Journey-to-work test (Cochrane, Track G) | Complete — Calgary direction confirmed, within-Calgary not testable at CSD resolution | INCONCLUSIVE at CSD resolution |
| CSD-level community splits (Track H) | Complete — all three maps split 34.6% of CSDs; asymmetry is within-ED, not CSD-level | Null symmetric across maps |
| Minority rationales inventory and validation (Track I) | Complete — 25 rationales, 3 contradicted (2 shared-schools, 1 chair-misattribution) | New grade of failure documented |
| Chair Miller's Recommendation 5 close reading | Complete — form-match, conditions-pending, intent-inverted | Reframes §5.2 procedural finding |
| AI-use recommendations for November committee | Complete — 5 disciplines, 9-item disclosure checklist | Non-partisan technical contribution |
| Submission OCR (Track D partial) | 14 of 88 recovered, 1 new keyword hit (Rocky Gas Co-Op supporting RMH) | Marginal update to chair's-claim refutation |

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
| 9 (tracks G/H/I/J parallel + chair R5 + AI recs) | ~100K parent |
| Background sub-agents across all sessions | ~1.0M |

Total approximate across this chat chain: ~1.7M tokens. Sub-agents absorbed ~1.0M, keeping parent sessions well inside budget.

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

The repository is at v0.13. The next commit should increment the appropriate version (v0.13 → v0.14 for revisions, v0.13 → v1.0 for a locked release).

---

*Migration doc v0.13. Authored April 22, 2026 at the close of session 9. Tracks ordered by timeliness. If the next session diverges materially from the documented state, update this file first before making downstream changes.*

**Known staleness:** `report.html` is the v0.11-state dissemination build. All session 9 additions — chair R5, Track J cross-validation, Track I shared-schools finding, Track H CSD bounding, Cochrane StatsCan refinement, Plan B compliance audit (Track K), province-wide cycle-lag analysis (Track L), legislative reform proposal (Track M), Calgary data-sources audit, red-team attack on the academic paper, baseline scorecard (Track C applied to existing maps) — are present in `report_public.md` and `report_academic.md` but not yet regenerated into HTML. A rebuild is a separate design task (SVG charts, palette, layout) and was not executed in session 9.

**v0.13 additions (session 9 close):**
- Track K: statutory compliance audit + Plan B re-run. Finding: commission used July 2024 TBF estimate (4,888,723) as primary basis despite stated methodology citing 2021 census (4,262,635). Plan B re-run leaves all five justification-test verdicts unchanged; three become more decisively "unforced" under fresher data.
- Track L: province-wide ED drift under mid-2025 populations. Majority 0 of 89 EDs shift out of ±25 % window; minority 5 of 89 (Calgary-North East, two Fort McMurray, Peace River, Lesser Slave Lake). Peak cycle lag ~14 years.
- Track M: legislative reform proposal. §12 amendment with Option A (keep census-primary, tighten supplement disclosure) and Option B (composite basis, ±2 % StatsCan tie-breaker, public-reproduction requirement). Comparative scan of federal, BC, ON, QC, SK, AB.
- Calgary data-sources audit: 16 sources catalogued. Track L's "blocked" verdict softened — ward-level modelled A2 sensitivity is feasible from public data (2021 census + StatsCan 2024 citywide + SRG forecast + communities-by-ward crosswalk + building permits).
- Track C applied to majority + minority baselines: scorecard of 18 signals per map; majority 0 triggered, minority 3 strong + 2 weak + 3 rationale-contradictions. Comparison template prepared for November map.
- Red-team attack on the academic paper: 21 attacks ranked by severity, 5 HIGH (CI crosses zero, Chen-Rodden cuts both ways, signature pre-registration unprovable, main body on commission's 2024-TBF tables, 70/30 weight selection). Fortification pass not yet commissioned.
- Open questions raised by Plan B and cycle-lag data explicitly surfaced in both reports.
- AI-use recommendations file updated with §2.5 Data currency addendum (by Track L).
- Airdrie figure reconciled: April 2025 municipal census measured 90,044; TBF 2025 estimate ≈92,500. Both are above the ±25 % ceiling; two-way split still clears.
