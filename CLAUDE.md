# Alberta Electoral Boundaries Audit — Project Root

You are a fresh Claude Code instance arriving at a partially-completed multi-session audit. **Your full instructions are in `v1_2_gerrymander_audit_prompt.md`. Read that file first, then execute the staged pipeline it contains.**

## Quick Orientation

**What this project is.** A non-partisan, evidence-based forensic audit of Alberta's 2025–26 Electoral Boundaries Commission proposals. Three maps under evaluation: the 2019 boundaries currently in force, the independent commission's majority recommendation, and the government-appointed commissioners' minority recommendation.

**Project owner.** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student). All published outputs credit Will Conner as author and audit designer.

**What's done.** Sessions 1–4 produced: symmetric B1–B6 partisan-bias analysis across all three maps with Monte Carlo CI and cross-election robustness; Section A population equality with Calgary zone-gap analysis under two classification rules; Section C visual spatial audit of chair-flagged and independently-scanned configurations; Section D procedural audit with sub-agent-verified submission archive search (1,252 of ~1,340 submissions) that partially refuted the chair's "no public support" claim; bias audit; design critique; uncertainty and shapefile-impact analysis; academic literature review; dual-audience reports (public + academic); v1.2 pipeline prompt with integrity and red-team gates.

**What's next.** The two external unknowns that are still outstanding: 2026 boundary shapefiles (not yet released by Elections Alberta) and full measured vote attribution via Phase 4C execution. Both would improve precision. Neither is required for the headline findings.

## House voice (for any new writing)

- Plain, grounded, conversational prose.
- No mirrored "not X — Y" reversals. No templated triads. No emoji. No editorializing reactions.
- Versioning: `major.minor`. `x.0` is locked, `x.1+` is revisions. Files use the version as a filename prefix (`v0_1_filename.ext`). Never describe anything as "final."
- Public outputs target Flesch-Kincaid grade 9 or lower. Academic outputs target grade 13 or lower. The `analysis/check_voice_and_readability.py` script is a publication gate.

## Repository Layout (v1.2)

```
.
├── CLAUDE.md                                       # this file
├── README.md                                       # human-facing setup notes
├── report_public.md                                # dual-audience primary (grade 9, subject-matter-naive)
├── report_academic.md                              # dual-audience secondary (technical, legal framing, APA)
├── report.html                                     # accessible HTML dissemination build
├── migration.md                                    # handoff log for next session
├── v1_2_gerrymander_audit_prompt.md                # current execution prompt
├── alberta_redistricting_audit_final.md            # redirect pointer to the two reports
├── setup.sh                                        # installs Python deps (incl. textstat, pyogrio)
├── data/
│   ├── v0_1_alberta_2015_results.csv               # parsed 2015 election per-ED totals
│   ├── v0_1_alberta_2019_results.csv               # 87 EDs, 2019 candidate-level
│   ├── v0_1_alberta_2023_results.csv               # 87 EDs, 2023 candidate-level
│   ├── v0_1_alberta_2019_populations.csv           # 87 EDs, 2019-baseline populations (from 2017 EBC report)
│   ├── v0_1_majority_2026_populations.csv          # 89 majority-proposed EDs
│   ├── v0_1_minority_2026_populations.csv          # 89 minority-proposed EDs
│   ├── v0_1_minority_2026_populations_appendixE.csv # corroborating parse from Appendix E
│   ├── v0_1_majority_hybrid_crosswalk.csv          # Appendix C extracted crosswalk
│   ├── v0_1_minority_hybrid_crosswalk.csv          # heuristic minority crosswalk (2019->2026)
│   ├── submission_search_dataset.csv               # per-submission keyword hit dataset
│   ├── 2015_results.xlsx                           # raw 2015 Statement of Vote
│   ├── 2023_results.xlsx                           # raw 2023 Statement of Vote
│   ├── alberta_2019_eds/                           # Elections Alberta 2019 ED shapefile (87 polygons)
│   ├── alberta_2023_vas/                           # Elections Alberta 2023 Voting Area shapefile (4,765 polygons)
│   ├── alberta_2021_das.gpkg                       # StatsCan 2021 DA geometry filtered to Alberta (6,203 polygons)
│   ├── calgary_wards.geojson                       # City of Calgary ward shapefile (14 wards)
│   ├── alberta_shapefiles_README.md                # shapefile integrity summary
│   └── data_acquisition_manifest.md                # acquisition log and source URLs
├── analysis/
│   ├── v0_2_packing_cracking_analysis.py           # symmetric three-map B1–B6 (current)
│   ├── v0_3_monte_carlo_ci.py                      # Monte Carlo CI + cross-election
│   ├── electoral_forensics_population.py           # A1/A2/A3 + robustness
│   ├── parse_2015_results.py                       # 2015 election parser
│   ├── submission_search.py                        # submission archive keyword search
│   ├── v0_1_poll_attribution_skeleton.py           # Phase 4C skeleton
│   ├── v0_1_cross_election_rural_baseline.py       # 2015/2019/2023 rural baseline check
│   ├── check_voice_and_readability.py              # PR1/PR2 publication gate
│   ├── v0_1_section_A_population_equality.md       # §A writeup
│   ├── v0_1_section_C_geographic_coherence.md      # §C writeup
│   ├── v0_1_section_D_procedural.md                # §D writeup
│   ├── v0_1_section_4_geometry_provenance.md       # §4 writeup
│   ├── v0_1_bias_audit.md                          # self-audit of v0.1 methodology
│   ├── v0_1_design_critique.md                     # hostile red-team pass
│   ├── v0_1_uncertainty_and_shapefile_impact.md    # confidence intervals + shapefile scenarios
│   ├── v0_1_prompt_readiness.md                    # v1.1→v1.2 execution-readiness assessment
│   ├── v0_1_academic_literature_review.md          # literature gap analysis
│   ├── submission_search_findings.md               # refutation verdict write-up
│   ├── submission_search_log.md                    # submission-search technical log
│   ├── data_acquisition_log.md                     # data-acquisition subagent log
│   ├── appendix_e_recon_log.md                     # Appendix E PDF recon log
│   ├── v0_1_reproducibility_verification.md        # clean-room pipeline verification
│   ├── v0_2_final_redteam.md                       # final red-team pass on design + prompt
│   ├── v0_1_three_map_partisan_comparison.html     # B1–B4 visual from first session
│   └── polls_2023_unified.csv                      # parsed Statement of Vote output
├── maps/
│   ├── majority_calgary.jpg                        # Appendix A, p. 72
│   └── minority_calgary.jpg                        # Appendix E, p. 74
├── source_maps/
│   ├── minority_alberta_overview.jpg               # Appendix E, p. 73
│   ├── minority_edmonton.jpg                       # Appendix E, p. 75
│   └── minority_other_cities.jpg                   # Appendix E, p. 76
├── deprecated/                                     # prior-version scripts + prompts retained for audit trail
│   └── README.md                                   # explains each file
├── drafts/                                         # work-in-progress (typically empty)
│   └── README.md
└── .temp/                                          # gitignored; large downloads go here
```

## First Action (Verify the Baseline)

Run these five scripts. All must produce outputs matching the tables in `v1_2_gerrymander_audit_prompt.md`:

```bash
python3 analysis/v0_2_packing_cracking_analysis.py
python3 analysis/electoral_forensics_population.py
python3 analysis/v0_3_monte_carlo_ci.py
python3 analysis/v0_1_cross_election_rural_baseline.py
python3 analysis/check_voice_and_readability.py
```

If any output differs by more than 0.05 pp or one seat from the expected values, do not proceed — investigate the drift first.

## Dependencies

See `setup.sh`. Python 3.11+ required. Installs pandas, numpy, openpyxl, geopandas+pyogrio, shapely, pyproj, osmnx, gerrychain, pdfplumber, geopy, rapidfuzz, textstat.

## Use Sub-Agents Whenever Possible

Prefer spawning sub-agents (via the `Agent` tool) over direct work for anything that fits one of these patterns:

- **Multi-file research or scans.** Reading through many files to find a pattern, survey the codebase, or verify consistency — a sub-agent absorbs the file-read context cost while the parent session retains its room to plan.
- **Web fetches that take unknown time.** Downloading PDFs, shapefiles, scraping archives. Sub-agents run in the background; the parent keeps working.
- **Parallel independent tasks.** Two or more tasks that don't depend on each other — spawn them in the same message so they run concurrently.
- **Fresh-eyes red-team passes.** A sub-agent hasn't seen the authoring reasoning and will catch framing bias the author misses.
- **Validation passes on existing code or reports.** Clean-room reproducibility, citation spot-checks, cross-document consistency checks.
- **Data-acquisition tasks.** Downloading, parsing, and filtering multi-source data into `data/`.
- **OCR or text-extraction at scale.** Long PDFs, image-layer scans, submission archives.
- **Any task likely to exceed 15K tokens.** Better to isolate in a sub-agent transcript than to consume the parent's main context window.

When spawning sub-agents:

- Write prompts that stand alone. The sub-agent has no memory of this conversation.
- Include the working directory path explicitly.
- Give a clear output contract (named files, specific formats).
- Set a token budget and wall-clock budget inside the prompt.
- Tell the sub-agent not to make git commits — the parent session commits.
- For background agents, send them off and continue other work; don't poll.
- Multiple independent sub-agents should be spawned in a single message for concurrency.

Precedent sub-agents used in this audit chain:
- Submission-archive keyword search (1,252 submissions searched)
- Shapefile and census data acquisition
- Clean-room reproducibility verification
- Final red-team pass on design and prompt
- Historical marginal-seat analysis
- Phase 4C preparation (VA-polygon validation, hybrid-adjacent VA identification)
- Data-closeout web fetches

## Critical Discipline Reminders

- **Symmetry.** Every test, every map. If a pattern is flagged in one proposal, check the equivalent in others.
- **Vote Anywhere handling.** Only Election Day polls are spatially valid as proxies for where voters live. 2023 non-Election-Day votes make up 47.2% of total and must be apportioned by Election Day spatial share.
- **Structural findings vs vote-based findings.** Report them separately. Structural findings (A1, A2, C3, C4, D) survive all three red-team tests (Monte Carlo CI, cross-metric agreement, cross-election stability). Vote-based findings (B1–B6) have 89% directional confidence, not 95% significance, and require explicit disclosure of Monte Carlo CI bounds, declination disagreement, and 2019 direction flip.
- **Honest blocking.** If a stage fails a gate, stop and report. Fabricated results from a failed gate are worse than a documented block.
- **No "final" in filenames or claims.** Everything is a revision.

## Output Audiences

- **Public/Media:** grade-9 reading level, subject-matter-naive. Primary audience for the audit.
- **Academic/Legal:** full technical detail, APA citations, falsifiability statements, constitutional framing under *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991].

## When You Are Done

Update `migration.md` at project root with: phases completed, phases blocked (with reason), token spend, and recommended next session topic. Do not rename or delete files without updating this CLAUDE.md and the `deprecated/README.md`.
