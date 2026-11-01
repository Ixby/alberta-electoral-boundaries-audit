<!--
© Will Conner 2026 | CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
Data: Elections Alberta (public domain) | https://ixby.github.io
-->
> **Backward:**
> - `reports/academic/report_academic.md` — full monograph from which headline findings are summarised
> - `reports/public/report_public.md` — plain-language report cross-referenced in the deeper-reading list
> - `docs/FINDINGS_BRIEF.md` — one-page brief linked as the fastest entry point
> - `findings/population_equality.md` — source of population MAD A1 numbers
> - `findings/partisan_bias_summary.md` — source of partisan-metric headline values (+3.92 pp EG, +4.66 pp mean-median, +5.62 pp seats@50/50)
> - `findings/intermap_permutation_test_results.md` — source of the Ch1-COMP inter-map test results
> - `findings/joint_outlier_score_summary.md` — Mahalanobis joint outlier (Ch1) numbers
> - `findings/airdrie_overlap_report.md` — Airdrie four-way split documentation
> - `analysis/methodology/retraction_pathway.md` — named retraction conditions referenced throughout
> - `analysis/methodology/null_hypothesis_and_exoneration_criteria.md` — pre-committed pass thresholds
> - `analysis/methodology/threshold_provenance.md` — threshold derivations cited (EG, anchoring)
> - `analysis/methodology/audit_dependency_graph_readme.md` — 279-node DAG referenced in "apparatus" section
> - `docs/act_amendment_proposal.md` — §12 amendment policy recommendation
> - `docs/ai_use_recommendations_for_committee.md` — AI-use disciplines for Lunty committee
>
> **Forward:**
> - (leaf — repository landing page; reviewer-facing and external-citation surface)

# Alberta Electoral Boundaries Commission 2025–26 — Forensic Audit

*One commission, two recommendations, and the structural distance between them.*

## Public Summary

**https://ixby.github.io/alberta-electoral-boundaries-audit/**

---

Every so often Alberta redraws its electoral divisions (EDs), the districts that each elect a Member of the Legislative Assembly (MLA). The lines decide who represents you and which neighbourhoods are grouped with yours. Where they fall can decide who wins.

The 2025–26 Alberta Electoral Boundaries Commission produced two competing recommendations: a majority, backed by most of the commissioners, and a minority. Both comply with the *Electoral Boundaries Commission Act*, and the Act treats the majority's as the commission's report (s.9). This audit measures the structural distance between the two maps, on dimensions that have nothing to do with which party benefits.

**Airdrie.** The City of Airdrie has approximately 85,805 residents (City of Airdrie 2024 municipal census, July 2, 2024). That is above the statutory ceiling for a single electoral division under the Act's ±25% population band, the room the Act allows above or below the provincial average. So the city has to be split. The majority recommendation splits it across two electoral divisions. The minority splits it across four, placing more than half the city in Airdrie East and nearly all the rest in two divisions where Calgary residents outnumber Airdrie's. Both maps stay inside the Act's population band; the majority argued the minority map would likely fail a Charter challenge (final report, p. 10). Neither is required to use four instead of two. That is a drawing choice.

**Chair-flagged boundaries.** When the commission's majority (the chair and two commissioners) names a specific boundary in the final report, that signal comes straight from the primary source, and it takes no vote data to read. The majority report's written responses flag four minority boundaries as calling for explanation. Among them are these three: a lasso-shaped corridor linking Nolan Hill to Cochrane; an extension through Banff National Park, a stretch the majority described as a place "where no one lives" (audit estimate: a few hundred residents); and a district named for three small towns that reaches south to take in about 350 residents of north Airdrie. Zero boundaries in the majority recommendation drew comment of that kind from the majority.

**Population concentration.** In north, east and central Calgary, across 17 districts that include the Airdrie and Cochrane hybrids (the audit's Zone A; `findings/population_equality.md` §A2), the minority map's districts hold, on average, 11.5% more people than the provincial average. That is above the audit's +5% line. The majority's matching zone sits 2.8% above average, inside it. The difference is 8.7 percentage points. The +5% line is the audit's choice, one-fifth of the Act's ±25% band.

These are three of four structural dimensions where the audit finds the minority recommendation pulling away from the majority in directions that are consistent and measurable. In none of the three cases is the divergence legally prohibited. In none of the three cases does the measure depend on partisan vote data. And in none of the three cases is the divergence explained by Alberta's geography: both maps were drawn on the same geography, under the same provincial constraints. What these measures show is distance between the two maps, not distance from neutral. Legal maps drawn at random by computer would be flagged by the audit's structural battery more than nine times in ten, because both commission maps follow municipal lines and balance populations more tightly than random maps do (`findings/structural_lane_calibration_2026-10-31.md`). The evidence that the minority departs from neutral is partisan, below.

This audit was produced as a personal research project by Will Conner, a Mount Royal University student, following Government Motion 37 (introduced April 16, passed April 21, 2026), which referred the commission's work to a Select Special Committee of MLAs. It is not affiliated with any political party, campaign, or advocacy organization. The author has worked as a contract election officer for Elections Alberta for about 27 years, election by election, administering the vote on election day; nothing in this audit comes from that work, and every input is public. All code, data, and methodology are published here in reproducible form. The audit applies identical methodology to both maps.

> **New here?** The quickest ways in:
> - **[One-page brief](docs/FINDINGS_BRIEF.md)** — seat counts, wasted votes, plain English, no background needed.
> - **[Web summary](https://ixby.github.io/alberta-electoral-boundaries-audit/)** — the same findings with the key chart, made for sharing.
> - **[Public report](reports/public/report_public.md)** — the longer plain-language story, with maps and figures.
> - **[Technical monograph](reports/academic/report_academic.md)** — full methods, citations, and pre-registration IDs.

---

## Reading guide

The audit's **live claims and current methodology** sit in this README and in `findings/`, `reports/`, `analysis/methodology/`, and `preregistration/`. Everything in those directories is computed on the canonical Elections Alberta shapefiles, the official digital boundary files, and kept current through the academic report's DOCUMENTED CORRECTIONS. Every number in a file should check out against the on-disk data named in that file's `Backward:` block.

Two top-level directories are **not** part of the live audit:

- `archive/` holds analyses that were superseded or replaced, kept whole so the trail of work stays in view. The anchoring analysis on those provisional geometries lives there, along with the sampler comparison run before the canonical files. DPG stands for Derived Provisional Geometries: boundaries the audit rebuilt from the commission's published images before the official files existed. **Skip unless** you are tracing how the draft analysis changed or following the methods-paper case study (see `archive/dpg_era/README.md`).
- `proposals/` holds future work that is still speculative: not authorized, not pre-registered in final form, not run. **Skip unless** you want to know what might be done next (see `proposals/README.md`).

Every script and document in the repository names, in its own header, what it reads from and what reads from it (`Backward:` / `Forward:` block). The convention is set out in `DEPENDENCY_CONVENTION.md`. There is no central dependency map. To walk the chain either way from any file, grep that file's header.

---

## Cover map

The cover art (`data/maps/cover_art.png`, regenerated by `python analysis/scripts/build_cover.py`) shows Alberta's 4,765 Voting Areas, each coloured by its 2023 UCP–NDP two-party election-day vote share: orange where it leaned NDP, blue where it leaned UCP. How strongly the colour runs depends on population density, on a log scale. Sparse rural Voting Areas come out near-ivory. Dense urban areas are fully saturated, and darker still in the Calgary and Edmonton cores. Over the top, in thin boundary lines, sits the minority commission's 89-district proposal.

The result is Alberta weighted by where people live, not by how much land there is. A standard election map fills each riding with the winning party's colour, and the big rural ridings take over the picture. This render works at the level of the Voting Area and lets density set the colour, so population becomes visible. Colour deepens only where people gather. What appears is a population that sits heavily in the cities, in a picture that looks nothing like the usual election-night map of the province.

---

## Repository Architecture

The repository keeps each kind of material strictly in its own place, so an independent auditor can tell what they are looking at. **Live tier** (the audit's current claims):

* **`findings/`** — Analyses, test by test; one file per substantive finding. Each names its `Backward:` / `Forward:` dependencies in its own header.
* **`reports/`** — `reports/academic/report_academic.md` is the full technical monograph; `reports/public/report_public.md` is the plain-language report.
* **`analysis/`** — The code that runs (`scripts/`), the reasoning behind the live methods (`methodology/`), and review records (`review/`). Diagnostic logs live in `data/logs/`.
* **`data/`** — Source material, unaltered; fixed reference standards (`reference/`); boundary files (`shapefiles/`); and every computed metric and MCMC simulation distribution (`outputs/`). Code never lives here. The `data/maps/` subdirectory holds the cover art and generated plots.
* **`preregistration/`** — Null hypotheses committed in advance, drand-beacon seed commitments, retraction conditions, and the amendment log.
* **`docs/`** — Instructions for reproducing the work (`docs/REPRODUCING.md`), the one-page brief (`docs/FINDINGS_BRIEF.md`), policy proposals, and the rendered HTML for GitHub Pages.
* **`notebooks/`** — An exploratory notebook, ready for Colab (`notebooks/alberta_audit_explorer.ipynb`).
* **`tests/`** — The Pytest suite, which enforces byte-for-byte integrity and checks the mathematical proofs.
* **`viewer/`** — Svelte source for the public web summary (built and deployed via `docs/`).

**Out-of-band tiers** (clearly labelled, see the Reading guide above):

* **`archive/`** — Superseded or replaced analyses, kept whole so the trail of work stays in view. Each subdirectory has its own README saying what is there and why.
* **`proposals/`** — Speculative future work, not yet authorized or run. Each proposal has its own README with the plan and the authorization gate it waits on.

---

## Quickstart

To reproduce the core findings or run your own analysis, you can have the environment running in three steps. (Requires Python 3.11+).

```bash
# 1. Clone the repository
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit

# 1b. Pull Git LFS files (MCMC checkpoints, ~1 GB — required for ensemble re-runs)
git lfs install && git lfs pull

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify the installation by running the baseline packing/cracking script
python3 analysis/scripts/packing_cracking_analysis.py
```
For step-by-step instructions on recreating the derived shapefiles or running the MCMC ensemble, see [`docs/REPRODUCING.md`](docs/REPRODUCING.md).

---

## What the audit finds

The findings start with those that need only the lines and population counts, then bring in votes.

**Population equality (A1).** Each district should hold about the same number of people. The measure here is the mean absolute deviation from the provincial quota: on average, how far a district's population sits from the ideal size. Majority: 3,180 persons. Minority: 4,707 persons, on the commission's July 2024 population tables (provincial mean: 54,929; source: `findings/population_equality.md`). Both maps comply with the law. On those tables the minority's wider spread comes from drawing choices, not from where people live; on 2021 census counts the two maps come out almost level (4,847 against 4,871).

**Geographic-zone asymmetry (A2).** In the minority map, the northeast/central Calgary zone sits 11.5% above the provincial mean population (zone mean: 61,225; provincial mean: 54,929). That crosses the +5% line, the first test (P1) of the audit's packing signature. The majority's matching zone sits 2.8% above average, inside it. The +5% line is the audit's choice, one-fifth of the Act's band. The packing signature itself is not detected on the official maps. Its second test (P2) needs the NDP to win this zone's districts by margins at least 15 points above the provincial average. On the official vote attribution the NDP wins 8 of the 17, by margins 12.6 points below it (`data/outputs/packing_signature_rescore_2026-11-01.json`). The test was exploratory: it was written in the same commit as its first run. What stands is a population-equality finding.

**Community fragmentation (§5.3.2).** The minority recommendation cuts Airdrie into four separate electoral divisions. The majority uses two. Both satisfy the Act's population band. Under the minority's choice, voters in the same city are represented across four separate legislative constituencies, three of them tied mainly to a community outside Airdrie.

**Boundary anchoring (§5.8.5) — the maps look alike.** Anchoring is how closely a map's boundaries follow existing municipal lines. On the official Elections Alberta shapefiles (received 2026-05-06), majority 80.0%, minority 71.8%. The 2019 map, drawn by the last commission, scores 75.1% on the same measure (`data/outputs/municipal_anchoring_canonical.json`). The measure does not separate the maps, so the audit makes no anchoring claim. The three chair-flagged cartographic anomalies (§5.8.2) are a separate test.

**Cartographic anomalies (§5.8.2).** The majority report's own response text names four boundaries. The audit inspected the four and confirmed three; a check of the majority's four Calgary hybrids, with questions built from the minority's anomalies, found none (§5.8.3). All three sit in the minority recommendation: a lasso-shaped corridor district (Nolan Hill–Cochrane); a boundary extension through Banff National Park, which has few residents (Rocky Mountain House–Banff Park); and a district named for three towns that reaches south to take in about 350 residents of north Airdrie. The majority map has none.

**Partisan-bias metrics (§5.2).** These measures use votes. The efficiency gap compares the votes each party wastes. The mean-median difference is the gap between a party's average vote share across districts and its median. Declination measures how lopsidedly each party wins its seats. Each is set against a 1 million-plan MCMC neutral ensemble: legal maps drawn at random by computer, with no stake in who wins (official Elections Alberta shapefiles, canonical run). With the 2023 election-day votes attributed to the new districts, and with the correction to the declination sign convention (2026-06-12; Amendment 5, Part 9), the minority map favours the UCP more than the majority does on all four metrics: mean-median +4.66 pp, seats@50/50 +5.62 pp, efficiency gap +3.92 pp, declination the same way (UCP-tail, p98.79). Here pp means percentage points, the seats figure is the seat share at a tied vote, and a figure like p98.79 gives the map's percentile among the neutral maps. The majority map sits inside the neutral null on three of four metrics. Its mean-median is a 1st-percentile (p0.99) outlier leaning NDP, the wrong direction to help the UCP.

**MCMC neutral-ensemble outlier test (§5.4, Ch1).** Take the minority map's four partisan metrics together, and ask how far the map sits from the centre of the neutral maps. The joint answer is a Mahalanobis distance: D = 5.80 against the canonical ensemble covariance (p = 8.80×10⁻⁷ parametric χ²₄; see referee #1 finding on the ESS-bounded empirical alternative). No sampled plan reaches that distance, so the p-value is a model-based approximation, not a measured frequency, and it compares 89-district maps with 87-district plans; a size-matched joint test is pending. Taken singly against the 1 million-plan canonical ensemble (n_eff 1,413–1,522), three of four metrics pass the 95th percentile: mean-median at p99.97, **declination at p98.79 (UCP-tail under the sign-convention correction of 2026-06-12, Amendment 5, Part 9)**, and seats@50/50 at p99.99 (ESS-adjusted lower bound ≈p98, above p95). The efficiency gap, at p94.54, stays below the threshold and is not flagged. The four single-metric readings agree on direction. The majority sits at p0.99 on mean-median (NDP-tail) and inside the neutral null on the other three metrics.

**Combined-channel result (§5.4).** The audit examined two channels: Ch1 (Mahalanobis, p = 8.80×10⁻⁷) and Ch2 (SZAT swing-zone bootstrap, p = 0.0024). The headline combines them under the **Bonferroni dependence-robust upper bound p ≤ 1.76×10⁻⁶ (≈ 1 in 568,000)**. That bound holds under any dependence between the channels. A Fisher combination (p = 4.61×10⁻⁸) is anti-conservative under positive dependence (Brown 1975): when the channels move together, it overstates the evidence. It appears in the methods section only as the dependence-naive value. Both channels' seeds are derived from a published drand League of Entropy beacon value plus a label, so anyone can reproduce them; the beacon value was public long before the labels were set, so this alone does not rule out seed choice. Ch2's p = 0.0024 is the i.i.d.-flip value, and it does not survive a block-permutation null that respects contiguity (p = 0.1947, variance inflation 5.79×; see `findings/szat_block_permutation.md`), so SZAT is exploratory, not confirmatory. Ch1 is the binding term in the bound.

**Inter-map comparison test (§5.4, Ch1-COMP).** Registered at OSF yvc7g (filed 2026-05-10, after the shapefiles arrived on 2026-05-06 but before the test ran; the drand seed derives from beacon round 5500000, public since October 2025, plus a label — see `analysis/methodology/intermap_permutation_design.md` §AV6). The question: is the gap between the minority and majority maps bigger than the distance between pairs of neutral plans chosen at random? Version A (EG-only): p = 0.0348 against the canonical 1.01M ensemble. Version B (Mahalanobis joint): p = 0.0002. Both significant. The prediction written before the run said Version A would likely fail. It passed. The distance between the maps (Mahalanobis D = 7.20) is larger than either map's own distance from the centre of the ensemble (minority D = 5.80, majority D = 2.78). That confirms the maps sit on opposite flanks of partisan-metric space, not side by side. (Canonical values per report_academic.md §5.4.9 and findings/joint_outlier_score.json.)

**Direction-of-travel (§5.4.10).** Where did each map move from? The 2019 enacted baseline sits at the statistical edge of neutral redistricting practice: Mahalanobis D²=13.16 against the canonical 1 million-plan ensemble (p=0.0105). The majority 2026 map pulls back toward the middle of the ensemble (D²=7.74, p=0.102 — inside the null). The minority 2026 map pushes further out (D²=33.64, p=8.80×10⁻⁷). SZAT boundary-choice tests, exploratory because their null ignores spatial clustering, point the same way: the step from 2019 to the majority map is consistent with neutral redistricting (p=0.309); the step from 2019 to the minority map is marginally outside the null's confidence interval (p=0.053). The same five-member commission produced both 2026 proposals from the same 2019 baseline. They moved in measurably opposite directions on the partisan-metric axes the ensemble measures.

**One pre-registered pass (§5.3.5) — canonical.** Packing crowds a party's voters into a few districts it wins overwhelmingly. Cracking splits them across many districts so they never reach a majority in any. The neighbour-drain adjacency test asks whether packed and cracked districts of the same party sit next to each other. On the canonical Elections Alberta shapefiles it finds **1 coupled chain signal under the minority map, compared to 2 under the majority and 5 under the 2019 enacted map** (`findings/neighbour_drain_analysis.md`, run 2026-05-23). The minority's coupled count (1) is 0.50× the majority's, well below the pre-registered pass threshold of 1.5×. The pre-registered PASS criterion is met. The canonical run used clean topology (zero K-nearest fallback for any of the three maps). §5.3.5 sets out the substantive explanation. The minority gets its partisan effect through **hybridization** (city-splitting that internalises packing and cracking within single EDs), not through the adjacency-chain packing model this test measures.

The audit does not claim the minority map is a gerrymander in the intent sense. It claims a measurable divergence from the majority: structural on the measures above, and partisan, of a size that the constraint set alone is unlikely to explain: the ±25% population band, contiguity (every district in a single piece), and compactness.

---

## Forward-looking recommendations

The findings come with two policy recommendations.

**Act §12 amendment.** Section 12 of the *Electoral Boundaries Commission Act* sets the population data the commission uses: the most recent decennial census (or a newer province-wide census), with more recent information allowed "in conjunction with" it. The audit proposes amending §12 in one of two ways. The minimum option keeps the census as the legal basis and requires paired population tables, showing the 2021-census figures beside any newer Treasury Board estimates, with a statement of each source used and why. The structural option makes Treasury Board quarterly estimates, checked against Statistics Canada's, the legal basis, still published beside a census table, and requires the commission to explain its choice wherever the two bases would put a district on different sides of the legal limits. The proposal is in `docs/act_amendment_proposal.md`.

**AI-use discipline for the Lunty committee.** The Select Special Committee on Electoral Boundaries, chaired by Brandon Lunty, MLA for Leduc-Beaumont, oversaw an independent advisory panel that drew the new map and delivered it on October 22, 2026. On October 28 the committee voted 3–2 to end its review without adding observations, and the panel's report was due before the Assembly by November 2 (`evidence/legislature/ceb_transcript_2026-10-28.pdf`, pp. CEB-65, CEB-72 and CEB-73). For any redistricting body that uses AI tools, the audit proposes seven disciplines. Humans decide, not algorithms. Every prompt is logged and published. Evaluation criteria are registered before drafting begins. At least two independent tools run side by side. Every boundary has a named human of record. Every factual claim in AI-drafted text is checked by a human. And the body publishes a 9-item public disclosure checklist alongside the final map. The proposal is in `docs/ai_use_recommendations_for_committee.md`, summarised at §5.10 of the monograph.

---

## The structural cost

Both maps satisfy the law. The table below sets out the structural distance between them: five measures of geometry and population (one, anchoring, does not separate the maps on canonical geometry) and two measures that depend on votes, in the same units, applied the same way to both.

| Dimension | Majority 2026 | Minority 2026 | Gap |
|---|---|---|---|
| Population MAD (persons) | 3,180 | 4,707 | Minority 48% wider spread (commission's July 2024 tables) |
| Calgary NE/central zone population excess | +2.8% above mean | +11.5% above mean | 8.7 pp gap; minority 2.3× the +5% threshold, majority below it |
| Airdrie partition count | 2 EDs | 4 EDs by territory; 3 by people (≥2%) | Minority 2× more fragments by territory, 1.5× by people |
| Municipal-boundary anchoring *(does not separate the maps — canonical)* | 80.0% of perimeter | 71.8% of perimeter | Both close to the 2019 map's 75.1% |
| Chair-flagged cartographic anomalies | 0 | 3 | — |
| Efficiency gap (canonical ensemble scoring, official EA shapefiles) | +0.10% | +4.02% | Both below 7% reference on 2023 votes; minority about 3.9 points more UCP-structural than majority (positive = UCP structural advantage) |
| Coupled packing-cracking adjacencies (canonical EA shapefiles, 2026-05-23 run) | 2 | 1 | Pre-registered PASS for the minority on canonical geometry: 0.50× ratio, well below the 1.5× threshold. Clean topology (zero K-nearest fallback). §5.3.5 explains the hybridization mechanism, which is the substantive claim. |

The first five rows do not use votes. They can be measured against public official records, and they do not move if the partisan substrate changes. On canonical geometry the municipal-anchoring row does not separate the maps (both close to the 2019 map). The last two rows depend on vote data. The sixth row's direction holds under all three spatial-attribution methods the audit tested. The seventh row is a finding in favour of the minority map.

A map that splits a city of 85,805 into four divisions, three of them identified mainly with a community outside the city, puts a navigational cost on the people of that city. A two-division split does not. The three confirmed flagged boundaries (Cartographic anomalies, above) impose interpretive costs of the same kind. Neither cost is counted in dollars. Both are structural costs to effective representation as the *Saskatchewan Reference* [1991] sets it out. Effective representation is the standard Canadian courts apply to electoral boundaries.

Not auditing has a cost too. The alternative is to accept or reject either recommendation on commentary and intuition instead of measurement.

---

## What makes this different

**The record says which predictions came before the results.** Not every test family was committed before its results were read. The drain test (Ch3) is pre-registered and confirmatory: its null hypothesis and pass threshold were committed before its result was read. The inter-map comparison test was registered after the official shapefiles arrived but before it ran. The pass criteria for the population, partisan-bias, geographic and procedural families were committed after the commission reported and after some results were in, but before the final ensemble ran. The MCMC joint test (Ch1), the SZAT bootstrap (Ch2) and their combination are exploratory: Ch1's test and the combination were not named in any registration, and SZAT was registered after its results were known. For the MCMC ensemble (Ch1), SZAT bootstrap (Ch2), drain test (Ch3), and inter-map comparison test (Ch1-COMP, OSF yvc7g), the results follow deterministically from seeds derived from a published drand beacon value plus a label. Same seed, same result: that makes the runs reproducible, though it does not by itself rule out seed choice. For the P/C/E signature framework, the detection criteria were written in the same analytical commit as the detection run, a separation within a single session that §5.3.1 of the academic report discloses in full. Ch1-COMP is the sharpest example of committing in advance. The prediction written before the run said Version A (EG-only) would likely *not* reach significance. It did (p = 0.0348). The audit reports that whether or not it helps. That is what pre-registration is for. A method that finds only what it was looking for, after it looked, is not a method. It is a justification after the fact. Pre-registration prevents that.

**Each finding has a named retraction condition.** For every finding the audit leans on, it writes down what data or argument would force a retraction within 48 hours of that evidence becoming available (an operating rule kept in the repository, not pre-registered outside it; see methods-paper §6 for the full provenance). The conditions are in `analysis/methodology/retraction_pathway.md`. A reviewer who objects to a specific finding does not have to argue in the abstract. They can look up that finding's retraction condition and bring the evidence that triggers it. A separate two-week sunset-clause window covers the recompute from DPG to canonical geometry (originally 48 hours; relaxed on 2026-04-26, Amendment 5, Part 2). It is documented at `findings/methods_paper_draft.md` §6 + §7.1 Stages 11–12, including the observed 12-day headline turnaround and the 17-day overshoot to full integration on the Alberta 2025-26 case.

**The pre-registered passes are reported as prominently as the findings.** The neighbour-drain PASS for the minority (One pre-registered pass, above) sits among the headline findings, not in a supplementary table, with §5.3.5's explanation beside it: the minority gets its partisan effect through hybridization, which this adjacency test cannot see. An audit that hides its non-findings is not an audit.

**The same tests run on both maps.** Every metric applied to the minority recommendation is applied in the same way to the majority and to the 2019 enacted map. No test in this audit runs only on the minority. The paper's name for this discipline is test-application symmetry.

**The apparatus has a dependency graph.** 279 analytical nodes, 410 directed edges, no cycles. Invalidate any dataset and the cascade of orphaned findings can be computed on the spot: `python analysis/scripts/dependency_query.py --invalidate L0:data.2023_statement_of_vote`. Invalidate the entire 2023 vote dataset and the population-equality, Calgary zone, Airdrie fragmentation, and chair-flagged anomaly findings still stand. If the partisan-vote data is challenged, the structural differences still stand, but the departure from neutral rests on the vote data.

---

## Open questions

This audit is not finished. These questions are still open.

**Official geometry (Issue #1 — resolved 2026-05-06).** Elections Alberta released official vector shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`) on May 6, 2026 (commit `873f4d0`). The canonical boundaries have replaced every Derived Provisional Geometry. §5.2.7's direction claim rests on the official Elections Alberta shapefiles. The DPG reconstruction pipeline stays documented, so the work can be reproduced.

**1 million-plan MCMC ensemble — complete.** The authoritative ensemble is 1,010,000 plans (4 chains × 252,500 steps, seed 1432864451, official shapefiles), regenerated clean on 2026-07-12 (DOCUMENTED CORRECTIONS C10). Maps next to each other in a chain resemble each other, so the effective sample size (ESS) counts how many independent draws the chain is worth. Partisan-metric ESS is 1,413–1,522. The ESS-adjusted lower bound for the seats@50/50 flag is ≈p98, above p95. All headline p-values and percentile placements in §5.4.9 reflect this ensemble. An independent seed check (Section C, seed 3562959107, 100k plans) replicated the population MedAD and Reock placements under the same ±12.5% proposal band; the partisan metrics agree within sampling variation.

**The 2019-seeded MCMC ensemble (Issue #13).** The constraint-bound ensemble in §5.4 starts from a random seed, not from the 2019 enacted map. A chain that started from the 2019 enacted geometry would model a commission's incremental redrawing more directly, and might place both 2026 recommendations differently within the ensemble distribution. It would need a relaxed start: on 2021 population, 7 of the 2019 map's 87 districts fall outside ±25%.

**Submission sentiment (§5.9.4) — coverage gap.** LLM intensity scoring of the public submissions is complete. It reached the 1,252 submissions with machine-readable text, about 93% of the roughly 1,340 the audit searched. The rest are scanned images with no text layer, so the §5.9.4 weighted-net sentiment results leave them out.

**Alberta's historical efficiency-gap baseline (Issue #16) — resolved 2026-05-12.** The 7% EG reference threshold comes from US state-legislative cases. To get p95 EG thresholds fitted to Alberta, the same neutral ensemble was run under 2019 and 2015 vote shares (100k plans each, seeds from drand round 6099592): **2019 p95 = 1.01 %** (UCP landslide), **2023 p95 = 4.10 %** (competitive — canonical operative threshold), **2015 p95 = 9.71 %** (2015 votes, with the PC and Wildrose votes merged into one UCP-equivalent at 56.0 % of the two-party vote). The jurisdiction-normed range is 1.01 %–9.71 %. The minority map is under the threshold in 2019 and 2023 conditions, and over it only in 2015 conditions. That result is reported as committed, with no re-selection of the threshold. The majority map is under the threshold in all three contexts. The Stephanopoulos-McGhee 7 % reference sits between the 2023 and 2015 values. On 2023 votes both maps sit below both lines; on 2015 votes both exceed 7 % (majority +7.58 %, minority +10.54 %). Full results and methodology in §5.2.8 and `analysis/methodology/threshold_provenance.md` B.2.1.C.

---

## What to do with this

**Challenge the audit.** Read `analysis/methodology/retraction_pathway.md`. Pick a specific finding and its named retraction condition. Bring the data or argument that triggers it. The retraction conditions are public, concrete, and dated.

**Ask about the panel's process.** Some questions worth putting to the Lunty committee and its advisory panel: What evaluation criteria were set before the panel began drawing? Will the prompts and inputs to any AI tools used in the process be published? Will an ensemble of alternative maps be generated and published alongside the final map?

**Share the public-audience report.** [`reports/public/report_public.md`](reports/public/report_public.md) is written for a general audience. It covers fourteen pieces of evidence, what each can and cannot prove under Canadian law, and what Government Motion 37 means. It asks for no background in electoral systems or statistics.

The audit is a measurement, not an advocacy document. It does not argue for adopting either recommendation. The panel the Lunty committee oversaw drew an entirely new map; the Assembly decides what is enacted. The audit's job is to record what the commission's two proposals look like when they are measured systematically.

---

## Feedback and engagement

This is a working document. It gets better the more people engage with it.

**Issues** — use the [Issues tab](../../issues) for a specific objection to the method, a data correction, or evidence that triggers a retraction condition. Include the finding number (e.g., A1, §5.8.5) and the specific claim at issue.

**Discussions** — use the [Discussions tab](../../discussions) for the broader design questions: Is the constraint-bound ensemble the right comparator? Should the municipal-anchoring metric weight urban and rural EDs differently? Is a 7% EG reference appropriate for a Canadian provincial legislature at all?

**Pull requests** — fixes to data files, script bugs, and documentation errors are welcome. A PR that proposes a new finding or test should include a pre-registration artifact (null hypothesis, threshold, prediction direction) in its description.

The most useful challenges come from people with expertise in electoral geography, Canadian constitutional law, redistricting statistics, and GIS. Supporters of either recommendation are welcome to engage. The retraction conditions exist to give hostile reviewers a structured path that never requires arguing about intent.

---

## Deeper reading

- **[docs/FINDINGS_BRIEF.md](docs/FINDINGS_BRIEF.md)** — **Quickest entry.** One-page plain-language brief: riding boundaries explained from scratch, seat-gap and wasted-vote findings, what the audit does not claim, conflict-of-interest disclosure.
- **[Web summary](https://ixby.github.io/alberta-electoral-boundaries-audit/)** — The brief on GitHub Pages, with the key chart built in; made for sharing with people new to the topic.
- **[report_public.md](reports/public/report_public.md)** — Plain-language narrative for a general audience: fourteen pieces of evidence, each with its legal limits, and what Government Motion 37 means.
- **[report_academic.md](reports/academic/report_academic.md)** — The full monograph (pre-publication, continuously updated): executive summary, methods, §§5.1–5.10 results, seven measurement layers, dependency DAG, limitations, and falsifiability hooks. Start here to challenge a specific finding.
- **[analysis/methodology/retraction_pathway.md](analysis/methodology/retraction_pathway.md)** — The named retraction condition for each finding. The fastest way either to retract a claim or to confirm it holds.
- **[analysis/methodology/null_hypothesis_and_exoneration_criteria.md](analysis/methodology/null_hypothesis_and_exoneration_criteria.md)** — Null hypotheses and pass thresholds committed in advance, and the Structural/Robust/Durable classification of every finding.
- **[analysis/methodology/plain_language_defense.md](analysis/methodology/plain_language_defense.md)** — The full defense, entry by entry: 215 assertion/why/answer entries covering every substantive claim in the monograph, written for a reader with no background in GIS, statistics, or political science.
- **[analysis/methodology/methodological_defenses.md#test-apparatus-defense](analysis/methodology/methodological_defenses.md#test-apparatus-defense)** — Criticism and response, test by test. Answers "are you making up metrics to have metrics?"
- **[analysis/methodology/threshold_provenance.md](analysis/methodology/threshold_provenance.md)** — Every numeric threshold traced to a statutory source, a literature citation, or a first-principles derivation. 41 thresholds catalogued, including three Alberta-calibrated EG alternatives (jurisdiction-normed range 1.01 %–9.71 %).
- **[analysis/methodology/audit_dependency_graph_readme.md](analysis/methodology/audit_dependency_graph_readme.md)** — The 279-node, 410-edge dependency graph: schema, worked examples, and the `--invalidate` query CLI.
- **[docs/ai_use_recommendations_for_committee.md](docs/ai_use_recommendations_for_committee.md)** — AI-use recommendations for the Lunty committee: seven principles, technical guidance by task type, and a 9-item public disclosure checklist.

---

## Acknowledgements

The author thanks the following for their willingness to engage with a pre-publication draft and provide independent methodological perspective:

- **Raymond Mok** (Elections Alberta) — for releasing the official 2026 electoral-division shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`) on 2026-05-06, which the audit's canonical recomputation depends on entirely. The Derived Provisional Geometry framework was a holding posture until those shapefiles arrived; the live structural-distance numbers in this README are all computed against the authoritative geometry Mr. Mok provided.
- **Duane Bratt** (Mount Royal University, Department of Economics, Justice, and Policy Studies; co-editor, *Orange Chinook: Politics in the New Alberta*) — political science and Alberta electoral systems review.
- **Lan Nguyen** (Mount Royal University, Department of Geography and Environmental Studies) — spatial methodology review.
- **Lynn Moorman** (Mount Royal University, Department of Geography and Environmental Studies) — GIS methodology review.

Pre-publication review is ongoing. Reviewers and data contributors are acknowledged for their time and assistance; findings and conclusions remain the sole responsibility of the author.

---

## Licensing and reuse

Input data is public-record material: Elections Alberta's 2023 Statement of Vote, Statistics Canada's 2021 Census (Open Government Licence — Canada), and the Electoral Boundaries Commission's 2026 final report and appendices. Derived code and analysis are released under the MIT License. The Derived Provisional Geometries (DPGs) are original work produced by reconstructing machine-readable polygons from the commission's raster-only published maps; they carry the §4.1.4 sunset clause and should not be cited as authoritative electoral geography without reference to that clause and its rerun commitment.