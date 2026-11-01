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

# Alberta Electoral Boundary Commission 2025–26 — Forensic Audit

*One commission, two recommendations, and the structural distance between them.*

## Public Summary

**https://ixby.github.io/alberta-electoral-boundaries-audit/**

---

Every so often Alberta redraws its electoral divisions (EDs), the districts that each elect a Member of the Legislative Assembly (MLA). The lines decide who represents you and which neighbourhoods are grouped with yours. Where they fall can decide who wins.

The 2025–26 Alberta Electoral Boundary Commission produced two competing recommendations: a majority, backed by most of the commissioners, and a minority. Both comply with the *Electoral Boundaries Commission Act*. The Act does not choose between them. This audit measures the structural distance between the two maps, on dimensions that have nothing to do with which party benefits.

**Airdrie.** The City of Airdrie has approximately 85,805 residents (City of Airdrie 2024 municipal census, July 2, 2024). That is above the statutory ceiling for a single electoral division under the Act's ±25% population band, the room the Act allows above or below the provincial average. So the city has to be split. The majority recommendation splits it across two electoral divisions. The minority splits it across four, placing more than half the city in Airdrie East and nearly all the rest in two divisions where Calgary residents outnumber Airdrie's. Both maps satisfy the law. Neither is required to use four instead of two. That is a drawing choice.

**Chair-flagged boundaries.** When the commission's chair names a specific boundary in the official hearing record, that signal comes straight from the primary source, and it takes no vote data to read. The majority report's written responses flag four minority boundaries as calling for explanation. Among them are these three: a lasso-shaped corridor linking Nolan Hill to Cochrane; an extension through uninhabited Banff National Park; and a district whose name points to three smaller towns while its largest population centre goes unnamed. Zero boundaries in the majority recommendation drew comment of that kind from the chair.

**Population concentration.** In north, east and central Calgary (the audit's Zone A; earlier text here said "northwest" — corrected 2026-07-08 per `findings/population_equality.md` §A2), the districts in the minority map's zone hold, on average, 11.5% more people than the provincial average. That is above the threshold drawn from the Act's own ±25% band. The majority's matching zone sits 2.8% above average, inside the threshold. The difference is 8.7 percentage points, on a measure whose threshold is anchored to the statute, not to any academic benchmark.

These are three of four structural dimensions, still standing, where the audit finds the minority recommendation pulling away from the majority in directions that are consistent and measurable. In none of the three cases is the divergence legally prohibited. In none of the three cases does the measure depend on partisan vote data. And in none of the three cases is the divergence explained by Alberta's geography. Both maps were drawn under the same provincial constraints, and a 1 million-plan MCMC ensemble (a large set of legal maps drawn at random by computer) confirms that the minority's values sit further than the majority's from what those constraints would lead you to expect.

This audit was produced as a personal research project by Will Conner, a Mount Royal University student, following the April 16, 2026 government decision to refer the commission's work to a Select Special Committee of MLAs. It is not affiliated with any political party, campaign, or advocacy organization. The author has worked as a contract election officer for Elections Alberta for about 27 years, election by election, administering the vote on election day; nothing in this audit comes from that work, and every input is public. All code, data, and methodology are published here in reproducible form. The audit applies identical methodology to both maps.

> **New here?** The quickest ways in:
> - **[One-page brief](docs/FINDINGS_BRIEF.md)** — seat counts, wasted votes, plain English, no background needed.
> - **[Web summary](https://ixby.github.io/alberta-electoral-boundaries-audit/)** — the same findings with the key chart, made for sharing.
> - **[Public report](reports/public/report_public.md)** — the longer plain-language story, with maps and figures.
> - **[Technical monograph](reports/academic/report_academic.md)** — full methods, citations, and pre-registration IDs.

---

## Reading guide

The audit's **live claims and current methodology** sit in this README and in `findings/`, `reports/`, `analysis/methodology/`, and `preregistration/`. Everything in those directories is current as of the recomputation (2026-05-12) on the canonical Elections Alberta shapefiles, the official digital boundary files. Every number in a file should check out against the on-disk data named in that file's `Backward:` block.

Two top-level directories are **not** part of the live audit:

- `archive/` holds analyses that were superseded or replaced, kept whole so the trail of work stays in view. The DPG-era anchoring findings (majority 71.0% / minority 14.5% / 4.9× asymmetry) live there, along with the sampler-disagreement framing from before the canonical files. DPG stands for Derived Provisional Geometries: boundaries the audit rebuilt from the commission's published images before the official files existed. **Skip unless** you are auditing the retraction history or following the methods-paper case study (see `archive/dpg_era/README.md`).
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

**Population equality (A1).** Each district should hold about the same number of people. The measure here is the mean absolute deviation from the provincial quota: on average, how far a district's population sits from the ideal size. Majority: 3,180 persons. Minority: 4,707 persons (provincial mean: 54,929; source: `findings/population_equality.md`). Both maps comply with the law. The minority's wider spread comes from drawing choices, not from where people live.

**Geographic-zone asymmetry (A2).** In the minority map, the northeast/central Calgary zone sits 11.5% above the provincial mean population (zone mean: 61,225; provincial mean: 54,929). That crosses the packing threshold (≥ +5% of provincial mean), which is anchored to the Act. The majority's matching zone sits 2.8% above average, inside the threshold. The threshold comes from EBCA § 15(1), not from any partisan estimate.

**Community fragmentation (§5.3.2).** The minority recommendation cuts Airdrie into four separate electoral divisions. The majority uses two. Both satisfy the Act's population band. Under the minority's choice, voters in the same city are represented across four separate legislative constituencies, three of them tied mainly to a community outside Airdrie.

**Boundary anchoring (§5.8.5) — both maps within the norm on canonical geometry.** Anchoring is how closely a map's boundaries follow existing municipal lines. Before the official shapefiles arrived, analysis on the Derived Provisional Geometries had the majority anchoring 71.0% of its perimeter to municipal edges and the minority 14.5%, a 4.9× gap. On the official Elections Alberta shapefiles (received 2026-05-06), both maps fall within the 70–85% Canadian comparator norm: majority 80.0%, minority 71.8%. The DPG-era values did not survive recomputation on the canonical files, so the audit makes no anchoring claim. The three chair-flagged cartographic anomalies (§5.8.2) are untouched by this correction.

**Cartographic anomalies (§5.8.2).** The majority report's own response text names four boundaries. The audit's blind tests, run without knowing which boundaries the chair had named, confirmed three. All three sit in the minority recommendation: a lasso-shaped corridor district (Nolan Hill–Cochrane); a boundary extension through uninhabited Banff National Park (Rocky Mountain House–Banff Park); and a district named for three towns whose population is smaller than the fourth community the district takes in. Under the majority, zero chair-flagged anomalies.

**Partisan-bias metrics (§5.2).** These measures use votes. The efficiency gap compares the votes each party wastes. The mean-median difference is the gap between a party's average vote share across districts and its median. Declination measures how lopsidedly each party wins its seats. Each is set against a 1 million-plan MCMC neutral ensemble: legal maps drawn at random by computer, with no stake in who wins (official Elections Alberta shapefiles, canonical run). With the 2023 votes attributed to the new districts, and with the Amendment 10 correction to the declination sign convention (2026-06-12), the minority map favours the UCP more than the majority does on all four metrics: mean-median +4.66 pp, seats@50/50 +5.62 pp, efficiency gap +3.92 pp, declination the same way (UCP-tail, p98.79). Here pp means percentage points, the seats figure is the seat share at a tied vote, and a figure like p98.79 gives the map's percentile among the neutral maps. The majority map sits inside the neutral null on three of four metrics. Its mean-median is a 1st-percentile (p0.99) outlier leaning NDP, the wrong direction to help the UCP.

**MCMC neutral-ensemble outlier test (§5.4, Ch1).** Take the minority map's four partisan metrics together, and ask how far the map sits from the centre of the neutral maps. The joint answer is a Mahalanobis distance: D = 5.80 against the canonical ensemble covariance (p = 8.80×10⁻⁷ parametric χ²₄; see referee #1 finding on the ESS-bounded empirical alternative). Taken singly against the 1 million-plan canonical ensemble (n_eff 1,413–1,522), three of four metrics pass the 95th percentile: mean-median at p99.97, **declination at p98.79 (UCP-tail under the Amendment 10 sign-convention correction, 2026-06-12)**, and seats@50/50 at p99.99 (ESS-adjusted lower bound ≈p98, above p95 — flag reinstated). The efficiency gap, at p94.54, stays below the threshold and is not flagged. The joint Mahalanobis result stands. With the declination sign corrected, the four single-metric readings now agree on direction. The majority sits at p0.99 on mean-median (NDP-tail) and inside the neutral null on the other three metrics.

**Combined-channel result (§5.4, headline = Bonferroni 2026-06-10, updated 2026-07-12 per a clean ensemble rerun — DOCUMENTED CORRECTIONS C10).** Ch1 (Mahalanobis, p = 8.80×10⁻⁷) and Ch2 (SZAT swing-zone bootstrap, p = 0.0024) are combined under the **Bonferroni dependence-robust upper bound p ≤ 1.76×10⁻⁶ (≈ 1 in 568,000)**. That bound holds under any dependence between the channels. The earlier Fisher combination (p = 4.61×10⁻⁸) is anti-conservative under positive dependence (Brown 1975): when the channels move together, it overstates the evidence. It is retired as the headline figure, and appears in the methods section as the dependence-naive value, for completeness. Both channels are seeded from publicly-verifiable drand League of Entropy beacon rounds that predate the shapefile release. (Updated 2026-07-08: Ch2's p = 0.0024 is the i.i.d.-flip value, and it does not survive a block-permutation null that respects contiguity — p = 0.1947, variance inflation 5.79×; see `findings/szat_block_permutation.md`. SZAT is retired as a confirmatory channel. The joint headline rests on Ch1 alone. The Bonferroni bound moved with Ch1's 2026-07-12 update, above, because Ch1 is the binding term throughout.)

**Inter-map comparison test (§5.4, Ch1-COMP).** Registered at OSF yvc7g (filed 2026-05-10, after the shapefiles arrived on 2026-05-06 but before the test ran; the drand seed derives from beacon round 5500000, which predates the shapefiles — see `analysis/methodology/intermap_permutation_design.md` §AV6). The question: is the gap between the minority and majority maps bigger than the distance between pairs of neutral plans chosen at random? Version A (EG-only): p = 0.0348 against the canonical 1.01M ensemble (round-1 published p = 0.0303 against the 250k v0_9 ensemble). Version B (Mahalanobis joint): p = 0.0002. Both significant. The prediction written before the run said Version A would likely fail. It passed. The distance between the maps (Mahalanobis D = 7.20) is larger than either map's own distance from the centre of the ensemble (minority D = 5.80, majority D = 2.78). That confirms the maps sit on opposite flanks of partisan-metric space, not side by side. (Corrected 2026-07-08: this paragraph previously carried the pre-rescore values D = 7.19 / 5.71 / 2.79 and p = 0.0303; canonical values per report_academic.md §5.4.9 and findings/joint_outlier_score.json.)

**Direction-of-travel (§5.4.10).** Where did each map move from? The 2019 enacted baseline sits at the statistical edge of neutral redistricting practice: Mahalanobis D²=13.16 against the canonical 1 million-plan ensemble (p=0.0105). The majority 2026 map pulls back toward the middle of the ensemble (D²=7.74, p=0.102 — inside the null). The minority 2026 map pushes further out (D²=33.64, p=8.80×10⁻⁷). SZAT boundary-choice tests confirm the pattern: the step from 2019 to the majority map is consistent with neutral redistricting (p=0.309); the step from 2019 to the minority map is marginally outside the null's confidence interval (p=0.053). The same five-member commission produced both 2026 proposals from the same 2019 baseline. They moved in measurably opposite directions on the partisan-metric axes the ensemble measures.

**One pre-registered pass (§5.3.5) — canonical.** Packing crowds a party's voters into a few districts it wins overwhelmingly. Cracking splits them across many districts so they never reach a majority in any. The neighbour-drain adjacency test asks whether packed and cracked districts of the same party sit next to each other. On the canonical Elections Alberta shapefiles it finds **1 coupled chain signal under the minority map, compared to 2 under the majority and 5 under the 2019 enacted map** (`findings/neighbour_drain_analysis.md`, run 2026-05-23). The minority's coupled count (1) is 0.50× the majority's, well below the pre-registered pass threshold of 1.5×. The pre-registered PASS criterion is met. The canonical run used clean topology (zero K-nearest fallback for any of the three maps). The result holds against the DPG-era substrate-sensitivity that had earlier produced different numbers on v0_2 (2/6, ratio 0.33×) and v0_8 (4/3, ratio 1.33× — direction reversed but still passing). §5.3.5 sets out the substantive explanation. The minority gets its partisan effect through **hybridization** (city-splitting that internalises packing and cracking within single EDs), not through the adjacency-chain packing model this test measures.

The audit does not claim the minority map is a gerrymander in the intent sense. It claims a measurable structural divergence from the majority, of a size that the constraint set alone is unlikely to explain: the ±25% population band, contiguity (every district in a single piece), and compactness.

---

## Forward-looking recommendations

The findings come with two policy recommendations.

**Act §12 amendment.** Section 12 of the *Electoral Boundaries Commission Act* sets the population data the commission uses: the most recent decennial census (or a newer province-wide census), with more recent information allowed "in conjunction with" it. The audit proposes amending §12 in one of two ways. The minimum option keeps the census as the legal basis and requires paired population tables, showing the 2021-census figures beside any newer Treasury Board estimates, with a statement of each source used and why. The structural option makes Treasury Board quarterly estimates, checked against Statistics Canada's, the legal basis, still published beside a census table, and requires the commission to explain its choice wherever the two bases would put a district on different sides of the legal limits. The proposal is in `docs/act_amendment_proposal.md`.

**AI-use discipline for the Lunty committee.** The Select Special Committee on Electoral Boundaries, chaired by Brandon Lunty, MLA for Leduc-Beaumont, is due to report by November 2, 2026. If the committee uses AI tools in its work, the audit proposes seven disciplines. Humans decide, not algorithms. Every prompt is logged and published. Evaluation criteria are registered before drafting begins. At least two independent tools run side by side. Every boundary has a named human of record. Every factual claim in AI-drafted text is checked by a human. And the committee publishes a 9-item public disclosure checklist alongside the final map. The proposal is in `docs/ai_use_recommendations_for_committee.md`, summarised at §5.10 of the monograph.

---

## The structural cost

Both maps satisfy the law. The table below sets out the structural distance between them: five measures of geometry and population (one, anchoring, does not separate the maps on canonical geometry) and two measures that depend on votes, in the same units, applied the same way to both.

| Dimension | Majority 2026 | Minority 2026 | Gap |
|---|---|---|---|
| Population MAD (persons) | 3,180 | 4,707 | Minority 48% higher variance |
| Calgary NE/central zone population excess | +2.8% above mean | +11.5% above mean | 8.7 pp gap; minority 2.3× the +5% threshold, majority below it |
| Airdrie partition count | 2 EDs | 4 EDs by territory; 3 by people (≥2%) | Minority 2× more fragments by territory, 1.5× by people |
| Municipal-boundary anchoring *(does not separate the maps — canonical)* | 80.0% of perimeter | 71.8% of perimeter | Both within 70–85% Canadian norm; DPG-era values 71%/14.5%/4.9× did not survive shapefile recomputation |
| Chair-flagged cartographic anomalies | 0 | 3 | — |
| Efficiency gap (Phase 4C, canonical EA shapefiles) | +0.10% | +4.02% | Both below 7% reference; minority 40× more UCP-structural than majority (positive = UCP structural advantage) |
| Coupled packing-cracking adjacencies (canonical EA shapefiles, 2026-05-23 run) | 2 | 1 | Pre-registered PASS for the minority on canonical geometry: 0.50× ratio, well below the 1.5× threshold. Clean topology (zero K-nearest fallback). DPG-era runs (v0_2: 2/6, ratio 0.33×; v0_8: 4/3, ratio 1.33×) are superseded by this canonical run. §5.3.5 explains the hybridization mechanism, which is the substantive claim. |

The first five rows do not use votes. They can be measured against public official records, and they do not move if the partisan substrate changes. On canonical geometry the municipal-anchoring row does not separate the maps (both within norm). The last two rows depend on vote data. The sixth row's direction holds under all three spatial-attribution methods the audit tested. The seventh row is a finding in favour of the minority map.

A map that splits a city of 85,805 into four divisions, three of them identified mainly with a community outside the city, puts a navigational cost on the people of that city. A two-division split does not. Three of the four boundaries the commission chair flagged in the official hearing record impose interpretive costs of the same kind: a corridor district whose narrow waist links Nolan Hill to Cochrane; an extension running through uninhabited Banff National Park; and a district named for three smaller towns, whose population is dwarfed by the fourth community the district captures. Neither cost is counted in dollars. Both are structural costs to effective representation as the *Saskatchewan Reference* [1991] sets it out. Effective representation is the standard Canadian courts apply to electoral boundaries.

Not auditing has a cost too. The alternative is to accept or reject either recommendation on commentary and intuition instead of measurement.

---

## What makes this different

**The record says which predictions came before the results.** Not every test family was committed before its results were read. The drain test (Ch3) is pre-registered and confirmatory: its null hypothesis and pass threshold were committed before its result was read. The inter-map comparison test was registered after the official shapefiles arrived but before it ran. The pass criteria for the population, partisan-bias, geographic and procedural families were committed after the commission reported and after some results were in, but before the final ensemble ran. The MCMC joint test (Ch1), the SZAT bootstrap (Ch2) and their combination are exploratory: Ch1's test and the combination were not named in any registration, and SZAT was registered after its results were known. For the MCMC ensemble (Ch1), SZAT bootstrap (Ch2), drain test (Ch3), and inter-map comparison test (Ch1-COMP, OSF yvc7g), the results follow deterministically from seeds anchored to publicly-verifiable drand beacon rounds that predate the commission's shapefile release. Same seed, same result. For the P/C/E signature framework, the detection criteria were written in the same analytical commit as the detection run, a separation within a single session that §5.3.1 of the academic report discloses in full. Ch1-COMP is the sharpest example of committing in advance. The prediction written before the run said Version A (EG-only) would likely *not* reach significance. It did (p = 0.0348). The audit reports that whether or not it helps. That is what pre-registration is for. A method that finds only what it was looking for, after it looked, is not a method. It is a justification after the fact. Pre-registration prevents that.

**Each finding has a named retraction condition.** For every finding the audit leans on, it writes down what data or argument would force a retraction within 48 hours of that evidence becoming available (an operating rule kept in the repository, not pre-registered outside it; see methods-paper §6 for the full provenance). The conditions are in `analysis/methodology/retraction_pathway.md`. A reviewer who objects to a specific finding does not have to argue in the abstract. They can look up that finding's retraction condition and bring the evidence that triggers it. A separate two-week sunset-clause window covers the recompute from DPG to canonical geometry (originally 48 hours; relaxed in Amendment 2 Change 11 on 2026-04-26). It is documented at `findings/methods_paper_draft.md` §6 + §7.1 Stages 11–12, including the observed 12-day headline turnaround and the 17-day overshoot to full integration on the Alberta 2025-26 case.

**The pre-registered passes are reported as prominently as the findings.** The neighbour-drain result (1 coupled chain signal under the minority, 2 under the majority, 5 under the 2019 enacted map, on canonical Elections Alberta shapefiles, run 2026-05-23) is reported as a §5.3.5 PASS (ratio 0.50×, threshold ≤ 1.5×). It is not buried in a supplementary table. The minority's low adjacency-chain count does not clear it. §5.3.5 establishes that the minority gets its partisan effect through hybridization (city-splitting that internalises packing and cracking within single EDs), not through the classic adjacency-drain model this test measures. An audit that hides its non-findings is not an audit. The DPG-era substrate-sensitivity that produced different numbers on v0_2 and v0_8 is documented in the same finding file and in the commit history. The canonical run is now the authoritative result.

**The same tests run on both maps.** Every metric applied to the minority recommendation is applied in the same way to the majority and to the 2019 enacted map. No test in this audit runs only on the minority. The paper's name for this discipline is test-application symmetry.

**The apparatus has a dependency graph.** 279 analytical nodes, 410 directed edges, no cycles. Invalidate any dataset and the cascade of orphaned findings can be computed on the spot: `python analysis/scripts/dependency_query.py --invalidate L0:data.2023_statement_of_vote`. Invalidate the entire 2023 vote dataset and the population-equality, Calgary zone, Airdrie fragmentation, and chair-flagged anomaly findings still stand. If the partisan-vote data is challenged, the audit's headline does not collapse.

---

## Open questions

This audit is not finished. These questions are still open.

**Official geometry (Issue #1 — resolved 2026-05-06).** Elections Alberta released official vector shapefiles (`ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`) on May 6, 2026 (commit `873f4d0`). The canonical boundaries have replaced every Derived Provisional Geometry. §5.2.7's direction claim now rests on the official Elections Alberta shapefiles, and the method-sensitivity noted in earlier versions of this section no longer applies. The DPG reconstruction pipeline stays documented, so the work can be reproduced.

**The counter-map challenge (Issue #14) — moot on canonical geometry.** The §5.8.5 anchoring finding's original retraction condition was this: produce a map that meets the minority's stated community-of-interest goals while anchoring to municipal boundaries about as well as the majority does. On canonical Elections Alberta shapefiles, both 2026 maps already fall within the 70–85% Canadian comparator norm (majority 80.0%, minority 71.8%). The DPG-era 4.9× anchoring asymmetry the challenge was built to falsify no longer exists. The audit makes no §5.8.5 anchoring claim, so in its original form the challenge is moot. The audit's live claim about structural coherence now rests on urban hybridization (§5.3.2), the splitting of Airdrie, and the chair-flagged cartographic anomalies (§5.8.2). Each carries its own named retraction condition in `analysis/methodology/retraction_pathway.md`.

**1 million-plan MCMC ESS-upgrade run — complete (2026-05-12).** The authoritative ensemble is 1 million plans (4 chains × 252,500 steps, same seed and shapefiles as the initial 250k run). Maps next to each other in a chain resemble each other, so the effective sample size (ESS) counts how many independent draws the chain is worth. Partisan-metric ESS is 1,413–1,522. The ESS-adjusted lower bound for the seats@50/50 flag rose from p89.72 (below p95 at 250k) to ≈p98 (above p95 at 1 million plans), and the flag is reinstated. All headline p-values and percentile placements in §5.4.9 reflect the 1 million-plan ensemble. An independent seed check (Section C, seed 3562959107, 100k plans) confirmed the population MAD and Reock null findings; the partisan metrics agree within sampling variation.

*Note on why the 1 million-plan Ch1 p-value is less extreme than the 100k run:* as the ensemble grew from 100k to 1 million plans (n_eff 379 → 1,413 for the minimum metric), the Mahalanobis covariance matrix was estimated more precisely. That better-calibrated covariance shows the minority map is somewhat less extreme than the noisier 100k estimate suggested: Ch1 p moved from 1.60×10⁻⁷ to 8.80×10⁻⁷ (the 1M figure itself further updated 2026-07-12 after a clean ensemble rerun; see DOCUMENTED CORRECTIONS C10 in the academic report). This is a calibration effect, not a weakening of the finding. The dependence-naive Fisher combined p (4.61×10⁻⁸) is kept so the methods are complete, but it is not the headline. The operative value is the Bonferroni-bounded headline (p ≤ 1.76×10⁻⁶). The individual metric percentiles (mean-median p99.97, seats@50/50 p99.99) are stronger, not weaker, in the 1 million-plan run.

**The 2019-seeded MCMC ensemble (Issue #13).** The constraint-bound ensemble in §5.4 starts from a random seed, not from the 2019 enacted map. A chain that started from the 2019 enacted geometry would model a commission's incremental redrawing more directly, and might place both 2026 recommendations differently within the ensemble distribution.

**Submission sentiment (§5.9.4) — coverage gap.** LLM intensity scoring of the public submissions is complete. It reached the 1,252 submissions with machine-readable text, about 93% of the roughly 1,340 the audit searched. The rest are scanned images with no text layer, so the §5.9.4 weighted-net sentiment results leave them out.

**Alberta's historical efficiency-gap baseline (Issue #16) — resolved 2026-05-12.** The 7% EG reference threshold is calibrated to US Congressional elections. To get p95 EG thresholds fitted to Alberta, the same neutral ensemble was run under 2019 and 2015 vote shares (100k plans each, seeds from drand round 6099592): **2019 p95 = 1.01 %** (UCP landslide), **2023 p95 = 4.10 %** (competitive — canonical operative threshold), **2015 p95 = 9.71 %** (NDP wave). The jurisdiction-normed range is 1.01 %–9.71 %. The minority map is under the threshold in 2019 and 2023 conditions, and over it only in 2015 conditions. That result is reported as committed, with no re-selection of the threshold. The majority map is under the threshold in all three contexts. The Stephanopoulos-McGhee 7 % reference sits between the 2023 and 2015 values; both maps pass under both standards. Full results and methodology in §5.2.8 and `analysis/methodology/threshold_provenance.md` B.2.1.C.

---

## What to do with this

**Challenge the audit.** Read `analysis/methodology/retraction_pathway.md`. Pick a specific finding and its named retraction condition. Bring the data or argument that triggers it. The retraction conditions are public, concrete, and dated.

**Ask the Lunty committee about its process.** The Select Special Committee is due to report by November 2, 2026. Some questions worth putting to it: What evaluation criteria were set before the committee began drawing? Will the prompts and inputs to any AI tools used in the process be published? Will an ensemble of alternative maps be generated and published alongside the final map?

**Share the public-audience report.** [`reports/public/report_public.md`](reports/public/report_public.md) is written for a general audience. It covers the structural findings that survived, the gerrymander checklist, and what the April 16 pivot means. It asks for no background in electoral systems or statistics.

The audit is a measurement, not an advocacy document. It does not argue for adopting either recommendation. The Lunty committee has the authority to produce an entirely new map. The audit's job is to record what the commission's two proposals look like when they are measured systematically.

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
- **[report_public.md](reports/public/report_public.md)** — Plain-language narrative for a general audience: the five findings, the gerrymander checklist, what the April 16 pivot means, and what you can do.
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

Input data is public-record material: Elections Alberta's 2023 Statement of Vote, Statistics Canada's 2021 Census (Open Government Licence — Canada), and the Electoral Boundary Commission's 2026 final report and appendices. Derived code and analysis are released under the MIT License. The Derived Provisional Geometries (DPGs) are original work produced by reconstructing machine-readable polygons from the commission's raster-only published maps; they carry the §4.1.4 sunset clause and should not be cited as authoritative electoral geography without reference to that clause and its rerun commitment.