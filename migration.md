# Migration — Alberta Boundaries Audit

**Current state:** v0.17 draft. Ten chat sessions in this chain. Dual-audience reports (public + academic). Formal signature detection (packing, cracking, engineered-boundary). Per-redraw seat-consequence breakdown. Alternatives-available analysis for all contested redraws. Population-math tests run against five minority justifications (all five fail). Hybrid-count vs government-rationale analysis. Pre-registered checklist for identifying a gerrymander in the November 91-seat map. Session 9 additions: 25-rationale inventory and validation with three contradicted claims (two shared-schools, one 91-seat framing); Cochrane journey-to-work from StatsCan Table 98-10-0459 (Calgary-bound 35.8% of out-commuters; within-Calgary destination not testable); CSD-level community-splits count as bounding null; 338Canada per-riding cross-validation confirming the 1-seat structural asymmetry survives both 2023 votes and April 2026 polling; close reading of Chair Miller's Recommendation 5 addendum identifying form-match / conditions-pending / intent-inverted relationship to the April 16 motion; AI-use framework for the November committee (non-partisan, five disciplines, nine-item disclosure checklist); partial OCR of the 88 non-text-layer submissions (14 recovered, 1 new hit supporting Rocky Mountain House-Banff configuration).

**Working prompt for next session:** `v1_2_gerrymander_audit_prompt.md`.

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

## Session 10 in one paragraph

Session 10 was the defensibility pass. Round-1 red-team (21 attacks) and round-2 red-team (17 attacks) were run, fortified, and closed. The Chen-Rodden framing was re-tested and found to transfer directionally but fail on mechanism (UCP is the more-packed party in Alberta, not NDP; minority is rural-dispersed-loss, not urban-packed). A full Canadian comparator base rate was computed (median Canadian inter-map asymmetry = 0). The 2015 election was added as a third cross-election input via a completed 87-of-87 crosswalk. A 77-snapshot 338Canada historical stability test was run and uncovered a UCP/NDP column inversion in the earlier §3 cross-validation table; the "1-seat structural asymmetry" claim was retracted in favour of a state-dependent characterisation. Shape refinement went through four passes (road snap → feature-class snap → noise-cleanup + orange-accepted tier → visual-transcription-assisted Tier C annex for the 3 misclassified EDs) with 0.06% residual voter impact documented at v3 and ~90% of the thumbnail-legible territorial gap closed at v4. All 38 red-team attacks are answered in the paper. The sign-convention question Track Z raised was resolved by a consistency audit: both conventions are mathematically valid, produce the same ordinal ranking, and no direction claim needed flipping. The bottom-line summary was extended from three to four sentences to add the rationale-failure finding (six of seven minority redraws had cleaner options the minority didn't take). The HTML dissemination build was removed from the repository at PO direction; the two markdown reports are canonical. AI-provenance manifest and version labels were scrubbed from the reports per PO direction. Repository housekeeping moved draft-process artefacts to `deprecated/`, merged `source_maps/` into `maps/`, and untracked sub-agent cache. URL archival reached 70% coverage; the remaining 8 URLs need an authenticated Internet Archive SPN2 token to close. Outreach drafts (Elections Alberta, Duane Bratt) are ready for PO send. OSF pre-registration is submission-ready. The paper is defensibly drafted; remaining analytical gaps are either shapefile-dependent (Phase 5 ensemble, Polsby-Popper / Reock precision on the 3 visually-transcribed EDs) or date-gated (November 91-seat map).

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

**Track D — OCR the 88 missing submissions.** *Partial — session 9 recovered 14 of 88, 1 new support-configuration hit (RMH-Rocky Gas Co-Op).* Only extend further if legal proceedings or journal submission demands comprehensive coverage. Full methodology at `deprecated/v0_1_submission_ocr_log.md`.

**Track F — Deeper academic citations.** Only if submitting to a journal. Expand APA references per `analysis/v0_1_academic_literature_review.md` with the full Chen-Rodden, Courtney, Pal, Stephanopoulos-McGhee, Magleby-Mosesson, Katz-King-Rosenblatt, Altman-McDonald set. Estimated cost: ~15K tokens, 45 minutes. Pure writing, no analysis.

**Track T — Threshold provenance compendium.** *Closed in session 10.* 37 thresholds catalogued with statutory/literature/first-principles/modelling-convention provenance; ±20% sensitivity analysis confirms no finding direction flips at any threshold perturbation. Full file at `analysis/v0_1_threshold_provenance.md`.

**Track U — Chen-Rodden Alberta validation.** *Closed in session 10.* Direction prediction holds: neutral-ensemble EG [−4.4%, −0.7%] brackets the 2019 baseline of −2.64%. Mechanism prediction fails: UCP is the more-packed party in Alberta (surplus-vote rate 15.9% vs NDP 9.3%; rural UCP wins at 43 pp vs urban NDP wins at 21.5 pp). NDP seat deficit comes from dispersed rural losses, not urban concentration. Moran's I = 0.7534, p<0.001. §3.6 revised to reflect the mechanism correction. Full method at `analysis/v0_1_chen_rodden_alberta_validation.md`.

**Track V — Canadian comparator base rate.** *Closed in session 10, partial.* Proxy-based computation across 6 Canadian cycles + Alberta 2025-26 anchor (Federal 2022, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018). Median inter-map asymmetry = 0.000 pp; more than half of sampled Canadian cycles produce zero projected-winner flip between interim and final. Alberta 2025-26's 0.51 pp sits at 71st percentile; high-end 1.60 pp exceeds the observed Canadian maximum. Direct per-ED EG computation across all cycles (4–8 hours per cycle) flagged as future work. Full write-up at `analysis/v0_1_canadian_base_rate_computed.md`.

**Track W — OSF pre-registration draft.** *Closed in session 10, submission-ready.* Platform survey recommended OSF (free, timestamped, embargoable). Submission-ready document at `analysis/v0_1_pre_registration_draft.md`; step-by-step PO instructions at `analysis/v0_1_pre_registration_platform_analysis.md`. PO action: OSF account signup + upload + embargo to 2026-11-02 (≈30–45 min). DOI will become the time-stamped third-party custody record for the November checklist.

**Track X — Approximate 2026 shapefiles + compactness.** *Closed in session 10, with Tier C declined.* Tier A (exact 2019 inheritance): 57 majority EDs, 65 minority EDs measurable. Tier B (merged parents): 0 majority, 5 minority. Tier C (hybrid approximation from JPGs): not attempted — visual-transcription error of ±20% on compactness per 10% perimeter error was judged too wide. Within the measurable 64–79% of each map, minority shows ~2× the rate of low-compactness EDs as majority (PP<0.25: 7.1% vs 3.5%).

**Track Y — Iterative shape refinement (v1 → v2 → v3).** *Closed in session 10.* Three passes: v1 OSM road snap (mean shift 97 m); v2 feature-class-aware snap including waterway/railway/admin (Edmonton-Windermere PP 0.195→0.230 via North Saskatchewan River; Calgary-South PP 0.217→0.240 via Bow River); v3 noise-cleanup (strips near-zero-area interior rings that the boundary.plot renderer was drawing as spurious "internal borders"). Three-tier classification: green (Tier A exact), orange (Tier B voter-neutral, 2 EDs orange-accepted), red (refinement-unresolvable without shapefile, 3 EDs / 1,012 residual voter impact / 0.06% province-wide). See §6.7 of the academic report plus `analysis/v0_1_shape_refinement_v3.md`.

**Track Y-prime-prime-prime — Visual-transcription-assisted Tier C annex (v4).** *Closed in session 10.* Follow-up pass for the three EDs whose v3 approximations were structurally wrong (Edmonton-Windermere, Calgary-De Winton, Calgary-South). Used 600-DPI commission thumbnails anchored against multi-feature OSM boundaries (waterway + admin L6/L8 + aboriginal_lands). Polygons are explicitly sub-shapefile-grade with per-segment error bands (±100 m river snap, ±300 m OSM admin, ±500 m to ±1 km visually-transcribed). Territorial gap closed ~90 % at all three: Windermere 70 km² → ~5-10 km² edge-local; De Winton 500 km² → 50-100 km² after subtracting Tsuut'ina + ED-29 south + Okotoks; Calgary-South elongated 64 km² → compact ~9 km² with NE notch. VA-impact ceiling 318 VAs / ~62k votes (v3 → v4 reassignment, a correction of v3's territorial error). v4 runs as parallel annex to v3, not replacement. Full method at `analysis/v0_1_shape_refinement_v4.md`; verification panels at `maps/verification/v0_4_minority_*.png`.

**Track Z — 2015 cross-election extension.** *Closed in session 10.* Full 2015→2019 crosswalk built (87 of 87 mapped, 127 links, confidence ≥ medium) at `data/v0_1_2015_to_2019_crosswalk.csv`. Three-election asymmetry distribution under paper's sign convention: 2015 +0.03 pp (near-neutral reversal), 2019 +0.75 pp (clean reversal), 2023 −0.51 pp (supports headline). Headline direction supported under 2023 vote input; reversed under 2015 and 2019 pre-UCP-era electorates. See §3.5 of the academic report plus `analysis/v0_1_2015_cross_election_analysis.md`.

**Track AA — 338Canada historical stability.** *Closed in session 10.* 77-snapshot aggregate time series (2020-02-23 through 2026-04-12). 87 pre-2023 per-riding Wayback snapshots retrieved (mixed March/May 2023 coverage). Pre-2023 validation against 2023 actual: Pearson r = 0.966, MAE = 3.74 pp, winner-call 81/87 (93.1%). **Material correction:** uncovered UCP/NDP column inversion in the previous §3 cross-validation table. The 1-seat "structural asymmetry" claim was retracted — 338's uniform-swing probe shows the direction of the minority-vs-majority gap flips between UCP-competitive environments (UCP +1 on minority) and UCP-landslide environments (NDP +1 on minority). §3.5 of the academic report rewritten accordingly. Full methodology at `analysis/v0_1_338canada_historical.md`.

**School-division coherence check.** *Closed in session 10.* All 21 minority hybrids audited against Alberta Education school-division boundaries. 20 of 21 cross at least one school-division boundary — structurally systematic (a mathematical consequence of hybrid crossings + division-is-municipal mapping). The two explicit shared-schools claims Track I identified (R5 Bow-Springbank, R11 Red Deer-Sylvan Lake) are representative of the pattern, not exceptional. All four Red Deer hybrids cross a school-division boundary, not just Sylvan Lake. §5.4 extended. Full method at `analysis/v0_1_school_division_coherence.md`.

**Track M — Act §12 reform proposal + Track N + Track O.** *Closed in session 9, reaffirmed session 10 under full integration.* Proposed amendment text with Option A (minor reform) and Option B (composite basis, author recommendation); Track N concrete composite-basis source specification (TBF primary; StatsCan 17-10-0009 tie-breaker at ±2%; AHCIP + CRA T1 cross-check; Chief Electoral Officer as certifying authority); Track O provenance audit (commission's 4,888,723 provincial total verified as StatsCan Q2 2024 postcensal estimate). Standalone file at `analysis/v0_1_act_amendment_proposal.md`.

**URL archival (CDX + Chrome).** *Partial.* 19 of 27 critical URLs preserved via Wayback or archive.ph. 8 URLs remain unarchived because Wayback's anonymous Save-Page-Now endpoint requires authentication (daily IP quota on SPN reached during Chrome-based retry). Path forward: authenticated IA account with SPN2 Bearer token. Full log at `analysis/v0_1_url_archival_log.md`.

**Consistency audit (session 10 final-pass).** *Closed.* Confirmed both sign conventions (paper's 1:1 proportional-seat / Stephanopoulos-McGhee 2:1 slope) are mathematically valid and produce the same ordinal ranking; sign-convention glossary footnote added at §3.2 and §8.1. 6 numerical drift corrections (89.3%→90.5% MC direction-consistency across 7 locations, Airdrie / Red Deer population vintage tags, Calgary-Airdrie type tag). 5 broken references fixed (source_maps/ → maps/ folder merge follow-up). Full audit at `analysis/v0_1_consistency_audit.md` plus `analysis/v0_1_sign_convention_resolution.md`.

**Outreach drafts.** Two drafted but not yet sent (PO owns the send decision):
- `analysis/v0_1_elections_alberta_shapefile_request.md` — research-access request to Elections Alberta GIS team + Chief Electoral Officer Gordon McClure for 2026 shapefiles.
- `analysis/v0_1_duane_bratt_outreach_email.md` — collegial same-institution outreach to Prof. Bratt at Mount Royal asking for (i) 30-min methodological review, (ii) possible Elections Alberta introduction.

**Red-team passes.** Round 1 (21 attacks) and Round 2 (17 attacks) on the paper committed to `deprecated/` along with the three fortification files (A1–A5, B1–B6, C1–C10). All 38 attacks addressed in-paper or conceded with explicit scope narrowing. See `deprecated/README.md`.

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
| 10 (defensibility pass + red-team + Y-prime-prime + shape refinement + 2015 + 338 historical + school coherence + consistency audit) | ~400K parent |
| Background sub-agents across all sessions | ~2.5M |

Total approximate across this chat chain: ~3.5M tokens. Sub-agents absorbed ~2.5M; parent-session consumption kept inside budget across all ten sessions. The 1M-context model accommodated the concurrent-sub-agent pattern used heavily in session 10.

---

## Key files for the next session to read first

1. `CLAUDE.md` — project orientation, house voice, repository layout, sub-agent-use guidance
2. `v1_2_gerrymander_audit_prompt.md` — execution prompt with stages, stress-test gates, defensibility audit gates DA1–DA7, signature-detection criteria
3. `report_public.md` — current public findings in journalist voice (grade 9.4)
4. `report_academic.md` — current academic findings with APA citations, signatures §3.7–3.10 (grade 12.8)
5. `analysis/v0_1_claim_significance_analysis.md` — tiered chair's-claim refutation
6. `analysis/v0_1_data_preparation.md` — from-raw reproduction pipeline for every dataset
7. `analysis/v0_1_uncertainty_and_shapefile_impact.md` — what shapefile release would change
8. `analysis/v0_1_prompt_readiness.md` — v1.1→v1.2 readiness assessment
9. `analysis/phase_4c_runbook.md` — Phase 4C Vision-assignment playbook
10. `analysis/v0_1_338canada_integration.md` — polling-snapshot integration
11. `analysis/v0_1_91_seat_preliminary.md` — speculative 91-seat analysis
12. `analysis/v0_1_marginal_seats_findings.md` — concrete seat-level flip scenarios
13. `analysis/v0_1_rural_gap_findings.md` — why 3.9% rural mean is not partisan packing
14. `analysis/v0_1_justification_tests_findings.md` — five minority justifications tested; all failed

---

## Open questions for the PO (handoff to session 11)

**PO-owned decisions.** These are waiting on the PO, not on more analysis.

1. **Share v0.17 draft publicly — yes / no / after what changes?** The paper is defensibly drafted after a 38-attack red-team + full fortification pass. Remaining gaps are either date-gated (November committee) or shapefile-gated (Elections Alberta release).
2. **If sharing:** which channel (print media, social media, academic submission to *Election Law Journal* or *Canadian Journal of Political Science*, legal counsel, or a combination)?
3. **Send the Elections Alberta shapefile-request email?** Drafted at `analysis/v0_1_elections_alberta_shapefile_request.md`. PO sends from personal or institutional email.
4. **Send the Duane Bratt outreach email?** Drafted at `analysis/v0_1_duane_bratt_outreach_email.md`. Collegial same-institution ask. PO sends from Mount Royal email.
5. **Submit the OSF pre-registration?** Submission-ready at `analysis/v0_1_pre_registration_draft.md` with instructions at `analysis/v0_1_pre_registration_platform_analysis.md`. ~30–45 min of PO time. Embargo to 2026-11-02 matches the committee's deadline.
6. **Commission an authenticated Wayback archival pass for the 6 remaining URLs?** Requires IA account with SPN2 Bearer token. 8 URLs currently unarchived; 19 of 27 preserved.
7. **Resume Phase 4C VA-polygon vote attribution?** ~215K tokens, 2–4 hours. Value is now primarily cross-validation rather than primary measurement, since commission maps have been set aside. Possibly deferred until the November committee's map lands.
8. **After Nov 2, 2026** — is the committee's 91-seat map tabled? If yes, Track C (re-audit) becomes top priority. The pre-registered checklist, the R5 conditions, the symmetric counter-test framework, and the baseline scorecard are all ready.

---

## Fresh-chat instructions (session 11 kickoff)

1. Read `CLAUDE.md` first.
2. Read this migration doc.
3. Read `analysis/v0_1_live_tasks.md` — check for any sub-agent entries under "Currently live tasks" (these are handoffs from prior sessions that terminated before completion). Integrate or re-spawn as documented.
4. Read `v1_2_gerrymander_audit_prompt.md` for execution steps.
5. Run the five baseline scripts; confirm output matches documented tables to within the 0.05 pp / 1 seat tolerance.
6. Check `https://www.elections.ab.ca/resources/maps/` for 2026 shapefile release status.
7. Check whether the November committee has tabled its 91-seat map.
8. Pick the active track from the Open Questions above.
9. Consult the appropriate runbook.
10. Use sub-agents for multi-file research, parallel tasks, web fetches, validation passes, data acquisition, and anything over 15K tokens. See CLAUDE.md §"Use Sub-Agents Whenever Possible."
11. **When spawning any sub-agent that might not finish before the session hits a usage limit, add an entry to `analysis/v0_1_live_tasks.md`** under "Currently live tasks" with the full re-spawn prompt. This preserves the task for a future session to resume.
12. Commit intermediate work as you go; never claim "final" — everything is versioned.

The repository is at v0.17 draft. Next commit should increment to v0.18 for revisions, or v1.0 for a locked release.

---

*Migration doc v0.17. Authored April 22, 2026 at the close of session 10. Tracks ordered by timeliness. All 38 red-team attacks addressed; sign-convention resolved; full cross-election coverage (2015, 2019, 2023, April 2026 polling) integrated; shape refinement classified into three confidence tiers with 0.06 % residual voter impact documented; URL archival at 70 % coverage with path forward named. If the next session diverges materially from the documented state, update this file first before making downstream changes.*

**HTML dissemination build removed in session 10.** `report.html` was removed from the repository at PO direction. The two canonical reports (`report_public.md`, `report_academic.md`) carry all current findings. If an HTML dissemination build is wanted later, it is a separate design task (SVG charts, palette, layout) to be spec'd against the then-current markdown.

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

**v0.14 additions (session 9 continuation — full defensibility pass):**
- Track N: Alberta government database survey. Top-3 sources of truth: TBF Quarterly Population Estimate (primary), StatsCan Table 17-10-0009 (±2% tie-breaker), AHCIP + CRA T1 (cross-check). Constitutional verdict: census-based redistribution is NOT constitutionally required for provincial elections; data-source choice is a policy question. Certifying authority: Chief Electoral Officer.
- Track O: Commission source provenance audit. Commission's 4,888,723 provincial total verified as StatsCan Q2 2024 postcensal estimate (identical to OSI; OSI nests in StatsCan by construction). Zero Major / 4 Material / 3 Minor inconsistencies — all prose-level, not arithmetic. A1/A2/A3/B1–B6 findings unchanged.
- Track P: Fortification A1–A5 HIGH-severity attacks. All drop to MEDIUM or lower after narrowed claims + git-timestamp pre-registration evidence + Plan B invariance + §2.1 preamble + Appendix C 2021-census legal baseline (new 2019-map MAD = 4,745 ≈ minority 4,707; majority 3,180 materially tighter).
- A4 cascade: New script `analysis/v0_1_a1_legal_baseline_2021_census.py` computes A1 on 2019 EDs direct from 2021 census via DA-level overlay. 7 of 87 EDs outside ±25% at 2021-census time (5 urban-growth, 2 s.15(2) rurals). Audit §2.1 ordering preserved: majority (3,180) < 2019-on-2021 (4,745) ≈ minority (4,707).
- Track S: Byelection data 2022–2025. Six byelections inventoried; only Olds-Didsbury-Three Hills (June 2025) sits in contested territory. Verdict: byelection data not usefully additive. §3.5 footnote only.
- Track Q: Fortification B1–B6 MEDIUM-severity attacks. **Material new finding via symmetry counter-test**: Lethbridge 4-way and Red Deer 4-way cracking candidates in minority (majority is 2-way). Airdrie pattern now documented at 3 cities. §3.12 and §3.13 added to academic report.
- Track R: Fortification C1–C10 LOW-severity attacks. 9 at LOW, 1 (C9 reproducibility) DEFENDED. Reproducibility artifacts added at repo root: `requirements.txt`, `setup.md`, `FROZEN_MANIFEST.md`. Sub-agent prompts archive at `analysis/v0_1_subagent_prompts_appendix.md`. Canadian redistribution base-rate catalogue at `data/v0_1_canadian_redistribution_base_rate.csv` (partial; per-cycle quantification flagged as future work).
- Track M reform proposal: updated with Track N + Track O concrete addendum specifying composite-basis sources (TBF primary, StatsCan tie-breaker ±2%, AHCIP + CRA cross-check, CEO certifying authority) and §12(6)–(8) disclosure-requirement clauses.
- Academic report edits applied: F1 through F16 (F11–F16 from Track Q; F1–F10 from Track P). New §3.12 Symmetry-of-test-selection audit; new §3.13 Stress-test grades mini-audit; §1.4 AI-provenance manifest; §7 scope discipline paragraph; §3.5 byelection footnote + 338 two-model caveat; §3.3 base-rate acknowledgement; §11 Saskatchewan Reference two-way reading; Appendix A reproducibility artifacts note; Appendix B expanded linkset.
- Public report: "A pattern, not a one-off" paragraph surfacing Lethbridge 4-way as a material new finding.
- Red-team fortification summary: all 21 attacks now have specific responses. No attack remains at HIGH after fortification. Paper is fully defensible under peer-review-grade scrutiny.
