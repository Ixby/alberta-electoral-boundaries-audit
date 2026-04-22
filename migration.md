# Migration — Alberta Boundaries Audit

**Current state:** v0.4 published. Dual-audience reports (public + academic) + accessible HTML dissemination. Submission archive verified; chair's Appendix C claim partially refuted. Structural findings robust; partisan-math findings qualified at 89% directional confidence.

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

**Working prompt for next session:** `v1_2_gerrymander_audit_prompt.md`.

## What each session completed

**Session 1 (Chat 1, prior).** Initial B1–B4 partisan-bias analysis on 2019 baseline + minority 2026 estimate. Section A population equality skeleton. Section C visual spatial audit on chair-flagged configurations.

**Session 2 (Chat 2, prior).** Section D procedural audit skeleton. Section 4 geometry provenance (blocked on shapefiles). Initial compiled report.

**Session 3 (Chat 3, current session chain).** v0.8→v0.9 prompt fortifications. Dual-audience report rewrite. Bias audit identified three class-A issues; remediated in v0.2 packing-cracking script that computes all three maps symmetrically. Monte Carlo CI + declination + 2019 cross-election stress-test pass found partisan-math claims weaker than first-draft implied.

**Session 4 (still Chat 3 thread).** Added 2015 election data. Uncertainty and shapefile-impact analysis. Design critique stress-tested methodology. Academic literature review. PDF recon confirmed Appendix B is prose-only; Appendix C hybrid crosswalk extracted. v1.1→v1.2 prompt made stress-test gates mandatory.

**Session 5 (the present).** Submission-archive sub-agent searched 1,252 of ~1,340 public submissions. **Chair's "no public support" claim partially refuted** — three of five disputed configurations have documented public support (RMH-Banff Park, Olds-Three-Hills-Didsbury, Red Deer hybrids, Chestermere partially). Public report rewritten for subject-matter-naive audience at grade 7.1. Academic report updated with APA citations. Accessible HTML dissemination built with cross-links. File structure cleaned: `deprecated/` for old scripts, `drafts/` for WIP.

## Status by phase and test

| Phase / Test | Status | Confidence |
| --- | --- | --- |
| Carry-forward B1–B4 verification | Reproducible from v0.2 script | High |
| A1 Population MAD | Complete | High (CSV-sourced) |
| A2 Calgary zone gap | Complete, two classification rules | High |
| A3 s.15(2) eligibility audit | Complete; 1/3 ridings flagged per map | Medium-low (hand-coded areas) |
| B1 Vote distribution histogram | Complete | 89% directional |
| B2 Efficiency gap | Complete; MC 95% CI crosses zero | 89% directional |
| B3 Mean-median | Complete | 89% directional |
| B4 NDP @ 50/50 | Complete | 89% directional |
| B6 Declination | Complete; **direction disagrees with B2/B3/B4** | Reported |
| C3 Visual anomalies (minority) | 3 confirmed | High |
| C3 Visual anomalies (majority) | 0 Calgary, rest not imaged | Partial |
| C4 Community splits | Complete | High |
| D Procedural | **Partially refuted** via submission search | Narrowed |
| 4A Shapefiles | Not released by ABEBC | Blocked |
| 4B DA dissolve | Infeasible (PDF has no DAUIDs) | Blocked |
| 4C VA-polygon attribution | Skeleton verified; full run not attempted | Budget-blocked |
| 4D OSM reconstruction | Not attempted | 15K token cap |
| 4E Manual digitization | Out of scope | — |
| B5 MCMC ensemble | Requires shapefiles | Blocked |
| C1 Polsby-Popper | Requires shapefiles | Blocked |
| C2 Reock | Requires shapefiles | Blocked |

## Critical sub-findings to carry forward

1. **Structural findings are robust.** Population MAD, Calgary zone gap, community splits, visible anomalies survive all three stress-test gates.
2. **Partisan-math findings are directional at 89% confidence, not 95% significance.** Monte Carlo CI on majority-minority EG asymmetry is [−2.99, +0.76] pp and crosses zero. Two literature-standard metrics (EG and declination) disagree. Under 2019 vote data the asymmetry flips sign.
3. **Chair's Appendix C claim is overbroad.** Three of five disputed configurations have public support. Strongest counter-example: EBC-2025-2-0619 explicitly proposes "Rocky Mountain House-Banff" as an electoral district amendment.
4. **Strongest remaining procedural case:** Airdrie 4-way split (0/1,252 supporting submissions) and Calgary-Nolan Hill-Cochrane (0/1,252 supporting).
5. **Rural NDP baseline varies across elections:** 26.47% (2019) to 35.05% (2015). Monte Carlo samples rural_ndp_share ~ Uniform(0.26, 0.36).
6. **Vote Anywhere is 47.2% of 2023 valid votes.** NDP voters used Vote Anywhere at +6 pp higher rate than UCP, meaning the 70/30 urban/rural blend likely *under*-estimates the minority partisan shift — if a shift exists.
7. **Hybrid crosswalk from Appendix C verified two hand-coded mapping errors** (Airdrie-East, Medicine Hat-Brooks) that have been corrected.

## What the next session should do

In priority order:

**Track A (monitoring).** Watch `https://www.elections.ab.ca/resources/maps/` for 2026 shapefile release. When available:
- Run Stage 2 pipeline (shapefile integrity + population checksum)
- Run Phase 5 ensemble (GerryChain 10K+ maps) and compactness (C1 PP, C2 Reock)
- Refine B1–B4 with measured attribution replacing 70/30 blend
- Estimated cost: ~50K tokens, 1–2 hours wall-clock

**Track B (OCR completion).** The submission search missed ~88 image-only submissions (6.6%). If the audit will be used in legal proceedings, OCR'ing these would close the coverage gap. Estimated cost: ~30K tokens, 1 hour.

**Track C (Appendix E recon).** Extract minority report's hybrid crosswalk if one exists in a table format. Currently only the majority's Appendix C crosswalk is machine-extracted.

**Track D (full measured attribution).** Execute the Phase 4C pipeline against 2023 VA shapefiles even without 2026 polygons. Uses the commission's Appendix B prose descriptions + Vision assignment for hybrid-adjacent VAs. Collapses the Monte Carlo CI to a single point estimate. Estimated cost: ~300K tokens, 3–4 hours.

## Token spend across the session chain

Rough totals by phase:

| Session | Token spend |
| --- | --- |
| 1–2 (prior chats) | ~80K |
| 3 (current chat, v0.8→v0.9→v1.0) | ~120K |
| 4 (v1.0→v1.2 + data + literature) | ~100K |
| 5 (submission search + cleanup + HTML) | ~60K |
| Background sub-agents (submission search + data acquisition) | ~200K |

Total approximate spend in this chat: ~580K tokens. Sub-agents took ~200K of that.

## How to produce the reports from a clean checkout

Fresh Claude Code session, fresh clone of the repository:

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit
cd alberta-electoral-boundaries-audit
bash setup.sh
PYTHONIOENCODING=utf-8 python3 analysis/v0_2_packing_cracking_analysis.py
PYTHONIOENCODING=utf-8 python3 analysis/electoral_forensics_population.py
PYTHONIOENCODING=utf-8 python3 analysis/v0_3_monte_carlo_ci.py
PYTHONIOENCODING=utf-8 python3 analysis/v0_1_cross_election_rural_baseline.py
python3 analysis/check_voice_and_readability.py
```

If all five scripts complete without errors and their outputs match the tables in the academic report, the environment is ready. The reports themselves (`report_public.md`, `report_academic.md`, `report.html`) are checked-in artifacts — regenerating them requires running the pipeline through the v1.2 prompt in Claude Code.

## Open questions for the PO

- Is the current v0.4 output ready to share publicly? (Both reports pass their gates; HTML dissemination build includes accessibility features.)
- Should OCR of the ~88 missing submissions be prioritized, or deferred until the audit is used in legal proceedings?
- When should Track A execute? (Shapefile release is external.)
- Does the dual-audience model (public / academic / HTML) meet distribution needs, or are additional formats required (PDF, print, presentation)?

---

*Migration doc v0.4. Authored April 22, 2026 during the post-submission-search consolidation pass.*
