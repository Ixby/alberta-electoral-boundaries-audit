# Legal red-team — `report_academic.md`

**Standard:** defensible under hostile cross-examination in a court of law.
**Framework:** `analysis/red_team/v0_1_legal_red_team_framework.md` (ten dimensions D1–D10).
**Reference pass:** `analysis/red_team/v0_1_legal_red_team_report_public.md` (same template).
**Date:** 2026-04-23
**Scope:** `report_academic.md`, 1,049 lines, draft dated April 2026. Extends —
does not duplicate — the assertions / references / conclusions / latent-bias /
code red-team passes already on file. Focus of this pass: legal-standard
defensibility of the academic paper's statistical chain, external-literature
attributions, named-actor characterisations, and falsifiability hooks, above
and beyond what the earlier passes already flagged.

---

## Summary table

| # | Severity | Dimension | Region | One-line |
|---|---|---|---|---|
| ACA-01 | CRITICAL | D2 | L92, L243, L794, L840 | "7% efficiency-gap threshold used in *Gill v. Whitford* (2018)" — four occurrences; SCOTUS never adopted the 7% threshold, it vacated on standing. Extends references-pass CRIT-01 to the academic paper's own citations and synthesis. |
| ACA-02 | CRITICAL | D1, D4 | L82 vs L92 vs L243/257 vs L764 | Internal magnitude inconsistency: Abstract says "0.6–1.6 pp" range; Stress-Test Preamble calls the point estimate "0.58 pp"; §3.4 table and text give the 0.70-central as "−0.51 pp"; §7 Synthesis table row labels B2 as "+0.58 pp more UCP-favorable". The arithmetic (−1.36 − (−0.85) = −0.51) favours §3.4. The headline number is therefore wrong in three of four places or right in only one of four. |
| ACA-03 | HIGH | D2 | L774 | "Altman and McDonald (2011) … four-axis redistricting-audit discipline" cited in-text; no Altman entry in References list. Framework-citation ghost. |
| ACA-04 | HIGH | D2 | L299 | "Magleby and Mosesson (2018) document a ~22% US-state disagreement rate between declination and EG" cited; not in References. |
| ACA-05 | HIGH | D2 | L450 | "per ASA (2016, 2019), Nosek et al. (2018), and Munafò et al. (2017) guidance on graded evidence reporting" — three citation anchors, none in References. |
| ACA-06 | HIGH | D2 | L369, L382 | *Rizzo v. Rizzo Shoes* (1998) — correct case is *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 SCR 27 (no opposing party; bankruptcy re-reference). Also absent from court-cases section at L1019–1029. Extends references-pass HIGH-04 to the academic edition. |
| ACA-07 | HIGH | D3, D6 | L367, L382 | Engineered-boundary signature reinstated after its narrow E2 test failed, by reformulating E2 to a "choice over populated alternatives" test. Ad-hoc-rescue exposure. Pre-registration timestamp L327 ("5b0bc06 at 2026-04-22 08:32:20") is 2h24m before detection run; the reformulation occurred *after* the §2.4 retraction. Already flagged in conclusions-pass CRIT-02; residual HIGH here because the academic paper at L367 labels the retraction and rescue in the same section but does not acknowledge that E2 was rewritten post-failure. |
| ACA-08 | HIGH | D3, D6 | L568 | "the chair's claim is partially refuted" … "materially misrepresents the submission record" — this is an adverse characterisation of a sitting judge's reasoning in a public document. Defensible under fair comment if (a) grounded in reproducible submission-search data (it is: §5.4.1 table) and (b) labelled as the audit's finding, not the chair's position (it is). HIGH rather than CRITICAL because the tiered verdict at L570–583 is precise: three tiers, specific counts, submission IDs cited. A hostile reader will still test whether "materially misrepresents" is a fact-claim (requires proof the chair knew) or an opinion-claim (defensible without intent). Recommend reframing "materially misrepresents" → "materially overbroad" or "substantively overbroad" to stay clearly on the fact/effect side rather than the intent side. |
| ACA-09 | HIGH | D3, D6 | L538 | "the Premier's framing of R5 as 'the commission's own recommendation' elides this distinction" — "elides" is a verb of selective concealment and a hostile reader can construe it as imputing deceptive intent to the Premier. The academic paper's surrounding sentences are careful ("accurate as to the chair's personal position; overstates the recommendation's provenance if read as a collective endorsement"). Recommend swapping "elides" for "does not carry" or "omits" to stay on the fact/effect side. |
| ACA-10 | HIGH | D1, D5 | L92 Abstract | "fragmentation of Airdrie across four electoral divisions vs the majority's two" — Abstract asserts as fact; Airdrie population at three different vintages (74,100 / ~84,000 / 90,044) is cited at §3.8 L347 with StatCan and municipal-census anchors. Abstract itself has no inline cite. Standard D1 fix: footnote anchor to §3.8 or to `data/alberta_2021_da_populations.csv`. |
| ACA-11 | HIGH | D1, D5 | L267 | "338's model accuracy against the 2023 actual result: per-riding Pearson r = 0.966, MAE = 3.74 pp, winner-call 81 of 87 (93.1 %)" — four specific statistics presented without inline link to the analysis doc. Paper references `analysis/methodology/v0_1_338canada_historical.md` at L271 but the numbers at L267 are quoted without a per-statistic anchor. Third-party reproducer cannot confirm without the anchor. |
| ACA-12 | HIGH | D1, D5 | L267, L269 | "338 systematically under-projected UCP in rural Alberta by ~4.77 pp in 2023 (largest errors 11–14 pp in Peace River, Fort McMurray-Lac La Biche, Maskwacis-Wetaskiwin)" — three named ridings with specific error magnitudes. Adverse claim about a public-facing polling aggregator with a commercial reputation. Needs inline cite to the per-riding comparison artifact in the repo. If the artifact does not yet exist, the claim is D1 unsourced. |
| ACA-13 | HIGH | D1 | L245 | "Canadian comparative base rate … n=7 including the Alberta 2025-26 anchor: Federal 2022 Alberta sub-commission, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018, Alberta 2025-26. Distribution: mean proxy ΔEG 0.262 pp, median 0.000 pp, maximum 0.798 pp (Manitoba 2018)." — Seven-cycle composite statistical claim. Paper flags the proxy limitation. The D1 question is whether each of the seven cycles' inputs traces to archived primary sources. Pass label cites `data/v0_1_canadian_redistribution_base_rate.csv` and the `.md` computation. Third-party reproducer needs FROZEN_MANIFEST entries for each of seven commission reports + vote data sets. |
| ACA-14 | HIGH | D1, D5 | L386, L388–L393 | MCMC percentile table cites "4,765 Voting Area polygons (Elections Alberta 2023)", "10,000 samples", seed 42, 89 s runtime. Per-map percentiles (p96.1 / p6.6 / p100 / p24.6 / p57.4 / p1.7) are the load-bearing number for three of the paper's most consequential claims (structural floor; majority NDP tail; minority UCP tail). D4 reproducibility gate: the MCMC script must produce *these exact percentiles* on a fresh run. `data/v0_1_mcmc_ensemble_percentiles.csv` is the claimed artifact; needs author-verified reproduction check before release. Also: §3.11 acknowledges partial-coverage (57 / 70 / 87 districts) which means the majority p1.7 and minority p100 are NOT evaluated on identical substrate as the ensemble distribution. A hostile cross-examiner will ask why a p100 result against 87-district ensemble distributions is treated as comparable to a real map evaluated on a 70-district subset. The paper flags this but does not adjust the percentile label. |
| ACA-15 | HIGH | D1, D5 | L270 | "A 77-snapshot historical 338 stability probe (2020-02-23 through 2026-04-12)" — source URLs for 77 snapshots not in FROZEN_MANIFEST. 338Canada's archive pages' retention policy is unknown; this is a D1 archive risk analogous to the X-post risk (PUB-08 in the public-report pass). |
| ACA-16 | MED | D2 | L202 | "Rocky Mountain House at 6,765 (StatCan 2021)" — StatCan 2021 Census figure; a hostile checker will want the specific table (97-10-X or equivalent CSD-level). MED not HIGH because the number is readily verifiable and the paper already cites StatCan 2021 Census as the general source. |
| ACA-17 | MED | D2 | L536 | "CBC Edmonton, April 16, 2026; Calgary Journal, April 21, 2026" — two news citations without URLs. Academic-paper edition should include URL + archive snapshot per D1 standard. |
| ACA-18 | MED | D2 | L538 | "Corroboration: CBC News Edmonton, April 16, 2026 ('Miller adding: \"My majority colleagues do not agree with me on this point\"')" — nested quote attributed to CBC reporting; no URL. The underlying Miller quote is verified verbatim in references-pass; the CBC's reproduction of it is secondary. Needs URL + archive. |
| ACA-19 | MED | D1 | L264 | "the full 2015-to-2019 crosswalk at `data/v0_1_2015_to_2019_crosswalk.csv`" — file exists in repo per framework file-inventory; 2015 vote attribution is a load-bearing input to the 2015 cross-election asymmetry (+0.03 pp). The crosswalk's construction methodology (per-precinct mapping, vote-share interpolation rules) needs a documented methodology trace. If the crosswalk file's header lacks provenance, D5. |
| ACA-20 | MED | D2 | L303 | "Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through a *packing mechanism*" — paraphrase of the Chen-Rodden thesis. The DOI citation at L971 is verified (references-pass INFO); the paraphrase direction is correct. MED because the paraphrase is defensible; a more-exact summary would say Chen-Rodden argue residential segregation produces this effect for Democrats in US urban contexts, and the transfer to Canadian / NDP context is the audit's own empirical question. The paper does clarify this at §3.6 L311, so the MED is downgraded to a style note. |
| ACA-21 | MED | D2 | L229 | "Stephanopoulos and McGhee (2018) revisit the efficiency-gap debate and acknowledge the metric's sensitivity to modeling choices" — this citation supports the audit's Monte Carlo framing; the 2018 Stanford Law Review piece is in References at L1009. Check whether S&M 2018 specifically "acknowledges sensitivity to modeling choices" as the audit claims, or whether they defend the metric against critics. MED because the citation is real and broadly consistent; precision on what S&M 2018 actually argue would tighten the chain. |
| ACA-22 | MED | D3, D6 | L568–L583 | "tiered verdict" on the chair's "no public support" claim — the tier labels *precisely wrong* / *effectively wrong* / *precisely and effectively wrong* / *defensible* are novel coinages. Defensible as the audit's own analytic framework, but a hostile reader will test whether the coinage was pre-registered or invented during analysis. Recommend adding a line: "These tier labels were specified in `analysis/reports/v0_1_claim_significance_analysis.md` before running the search" (if true); or label as "post-hoc analytic categorisation" (if not). |
| ACA-23 | MED | D1 | L514 | "A CSD-level overlay (Track H; script `analysis/scripts/csd_community_splits.py`) computes, per map, the count of populated CSDs (population ≥ 1,000) spanning two or more electoral divisions" — script exists per file inventory; results (66/191, 66/191, 54/191 lower bound) are load-bearing for a "metric is a null symmetric" finding that constrains the C-section claim. D4 reproducibility check needed. |
| ACA-24 | MED | D1 | L520 | "StatsCan Table 98-10-0459 (2021 Census journey-to-work) disaggregates Cochrane CSD commute destinations: of 8,550 Cochrane workers with an Alberta place of work, 4,205 (49.2%) work within Cochrane, 3,065 (35.8%) commute to Calgary CY" — specific numbers from StatsCan table. Table reference is named; specific number extraction needs artifact link (`analysis/methodology/v0_1_cochrane_journey_to_work.md`; the paper does reference this file). MED because the cite chain exists but the journey-to-work doc itself should be verified to carry the same numbers. |
| ACA-25 | MED | D1, D6 | L518 | "20 of 21 cross at least one school-division boundary" — adverse finding against the minority report's school-district rationales. Anchors to `analysis/methodology/v0_1_school_division_coherence.md`. Load-bearing for the paper's "structural school-district crossings" claim. D1 passes if the school-division-coherence analysis file enumerates the 21 hybrids + their boundary crossings with Alberta Education primary-source link. |
| ACA-26 | MED | D4 | L305 | "a neutral-ensemble simulation of 150 random-walk-generated 87-seat plans (±25% population band, queen-contiguity, 2023 votes) plus a wasted-vote decomposition and Moran's I on NDP share" — N=150 is below DeFord, Duchin & Solomon (2021) recommended minimum for stable CI. Paper anticipates this concern at L317 ("A full GerryChain ReCom ensemble … would produce a tighter CI"). MED because the paper is self-aware of the limit. |
| ACA-27 | MED | D6 | L520 | "The interpretive inference — that Nolan Hill is a residential neighbourhood without significant employment and is therefore unlikely to be the commute destination for the 35.8% Calgary-bound flow — is consistent with the city's land-use profile but does not derive from the StatsCan data directly" — good fact/opinion labelling in the paper. MED is not a finding so much as a note that the self-label format (inference → opinion, data → fact) should be applied throughout §4–§5. |
| ACA-28 | MED | D3, D6 | L518 | "R5 and R11 invoked the most verifiable class of community-of-interest claim and got it wrong" — adverse characterisation of minority-report reasoning. Fact-vs-opinion boundary is sharp here: "invoked" is factual; "got it wrong" is a conclusion that rests on the school-division-boundary data. Defensible if the school-division analysis file supports. Paper does the anchor work. MED only because "got it wrong" is punchy rhetoric in an academic register; an academic-edition alternative: "do not survive primary-source verification against Alberta Education school-division boundaries." |
| ACA-29 | MED | D2 | L858 | "McLachlin J (as she then was) wrote that the guarantee of §3 is 'the right to effective representation' (para. 26), and that 'relative parity of voting power' must be weighed against other factors 'including geography, community history, community interests and minority representation' (para. 33)." — two verbatim quotations from *Reference re Saskatchewan* [1991] 2 SCR 158. Quotation accuracy verified by references-pass INFO (L334). Paragraph references given. Pass for verbatim accuracy; MED because an academic-edition citation should include the reporter page number or pin-cite form, not just the paragraph. |
| ACA-30 | MED | D1 | L539 | "Alberta's Regional Economic Development Alliance geography provides partial support for the minority's general hybrid doctrine. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake — the five municipalities at the heart of the minority's Red Deer hybrid proposals. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, and High River" — REDA catchment claims need URL + archive. D1 standard: every substantive factual claim traces. |
| ACA-31 | MED | D1, D5 | L867 | "2026 minority, 5 of 89 (Calgary-North East, Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo, Peace River all pass → fail; Lesser Slave Lake's s.15(2) ratio to the updated mean drops past −50 %)" — named-riding statutory-compliance claim under mid-2025 populations. Anchors to `analysis/v0_1_cycle_lag_analysis.md`. D4 reproducibility gate: the overlay script must produce exactly this 0/0/5 split on a fresh run. |
| ACA-32 | MED | D3 | L124 | "Going into this project, the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny." — author's D7 disclosure. Better than the public report (which has no disclosure). Partial: names the prior direction and names three findings that ran against it. Does not disclose party-donation history, prior commission or election-administration involvement, or any consulting work related to Alberta redistricting. Recommend expanding §1.4 with the D7 checklist: (a) political-party donation history, (b) prior employment related to electoral administration, (c) any party or commission member consulted during the audit, (d) whether the author is a current candidate for any office, (e) academic-supervisor affiliation if any. |
| ACA-33 | MED | D10 | L407 | "If the 100k-sample full-coverage rescore, or a later commission-shapefile-driven re-run, moves either 2026 map off its p ≥ 95 or p ≤ 5 tail on the flagged metric, the claim for that map is retracted and the map is reclassified as inside-band." — concrete falsifiability hook. PASS by D10 standard. MED is note-only: name a date by which the 100k run will be reported (the paper says "in progress") so that the hook is time-stamped, not open-ended. |
| ACA-34 | MED | D10 | L422 | "the checklist is prepared for submission to the Open Science Framework Registrations platform (`https://osf.io`) with embargoed release scheduled for 2026-11-02" — concrete date. PASS by D10 standard. MED is note-only: update status (submitted / DOI assigned / embargoed) when achieved. |
| ACA-35 | MED | D2 | L369 | "Canadian statutory interpretation follows Driedger's purposive principle" — "Driedger" is the scholarly short-form for Elmer Driedger, whose 1983 *The Construction of Statutes* is the primary-source textbook. The purposive principle's Driedger attribution is standard; the paper does not cite the textbook. A hostile academic reviewer will expect Driedger (1983) in References. |
| ACA-36 | MED | D2 | L550 | "Canadian boundary-commission practice traces to *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158, which established the 'effective representation' standard" — Saskatchewan Reference is correctly cited; para numbers at L858 are in the style academic readers expect. MED because the audit's at-a-glance claim that commissions "trace to" 1991 SCC is loose — Canadian redistribution commissions pre-date the case; the case established the *constitutional standard* for evaluating their work. Tightening: "Canadian boundary-commission jurisprudence traces to…" or "the constitutional standard evaluating Canadian boundary commissions traces to…". |
| ACA-37 | MED | D2 | L552 | "*Figueroa v. Canada (Attorney General)* [2003] 1 SCR 912 and *Frank v. Canada (Attorney General)* [2019] 1 SCR 3 developed the broader §3 Charter right to vote but did not directly apply the effective-representation standard to redistribution; they are listed in the References as context for the Charter jurisprudence surrounding electoral rights, not as authorities on boundary drawing." — accurate characterisation. Figueroa was about political-party registration thresholds; Frank was about expatriate voting. Both §3 cases, neither boundary-drawing cases. PASS. |
| ACA-38 | MED | D2 | L552 | "Courtney (2001) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces. Pal (2019) applies contemporary quantitative gerrymandering analysis to Canadian boundary cases within the Charter framework." — Courtney and Pal are both in References. Characterisation of each work as "authoritative" and "applies contemporary quantitative" is an editorial claim. MED because the characterisation is defensible; academic readers may want pin-cites to specific claims. |
| ACA-39 | MED | D1 | L870–L878 | "Open questions raised by the data" (numbered 1–6 under §11 appendix) — each raises genuine interpretive questions. Question 2 ("Operative force of §12(3)") describes the statutory-interpretation question well but stops short of a legal conclusion ("The question is for counsel and, if litigated, for courts"). PASS for the fact/opinion labelling. MED is a note: question 1 ("Current-map statutory status. Observed: 5 of 87 EDs sit outside the window under DA-level aggregation of mid-2025 populations") is a load-bearing fact claim requiring verifiable DA-level aggregation artifact — needs inline link to `analysis/v0_1_cycle_lag_analysis.md`. |
| ACA-40 | MED | D1, D5 | L893 | Appendix C table "2019 map on 2021 Census (this appendix) \| 48,996 \| **4,745** \| This computation" — new number (4,745) introduced in Appendix C, differing from the 2026 minority MAD of 4,707 by only 38 (0.8%). The closeness of these two numbers is the backbone of the appendix's "minority reproduces 2019-on-2021-Census distribution-tightness" argument. D4: the Appendix C computation script must be reproducible from `analysis/scripts/a1_legal_baseline_2021_census.py` plus the named inputs. |
| ACA-41 | LOW | D7 | L7 | "Author and audit design: Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student)" — better than the public report (which has no author bio). The degree + institution affiliation is stated. D7 is partially closed. See ACA-32 for the expansion recommendation. |
| ACA-42 | LOW | D8 | L24–L31 | Data-sources list includes several URLs (Elections Alberta Statement of Vote, Treasury Board estimates, StatsCan tables). All appear to be public-domain government data. Fair-dealing risk is minimal. PASS. |
| ACA-43 | LOW | D8 | L473–L477 | Map images (`maps/majority_calgary.jpg`, `maps/minority_*.jpg`) are "published commission maps" — reproduction for research and criticism is defensible under s.29 fair dealing provided source is attributed. Paper attributes to Appendix E pages. PASS. |
| ACA-44 | LOW | D9 | Throughout | No PII in the academic paper. Named actors are public figures (MLAs, commissioners, councillor Chad Krahn, former reeve cited in EBC-2025-2-1029, etc.). Alan Balson at L615 is a public-submission author, which is a public-record disclosure made by Balson himself. SAFE. |
| ACA-45 | LOW | D10 | L842–L846 | Falsifiability Statement — five enumerated conditions, each concrete. The A2 alternative-classification test was already run (L842 says so). The Phase 4C condition is specific on sign + threshold. The submission-archive condition is specific on the five named configurations. PASS. |
| ACA-46 | LOW | D10 | L838 | "time-stamped pending" and the Track O, Track L, Track H, Track N, Track Y-prime-prime-prime references — these internal track labels are opaque to an outside reader. Cosmetic; academic-edition should swap for section/file anchors. |
| ACA-47 | LOW | D4 | L908–L912 | "All scripts run from repository root" + three enumerated scripts. Minimal reproducibility appendix. `requirements.txt` and `setup.md` are referenced at L916. PASS for minimal D4; see D4 discussion below for the fuller reproducibility gap. |
| ACA-48 | LOW | D4 | L916 | "A version-pinned environment manifest (`requirements.txt` at repo root) lists every Python package with exact version; an interpreter pin (`setup.md`) names the tested Python version" — PASS as claim; triaged for later confirmation against the actual `requirements.txt` and `setup.md` content (framework parallel-agent assignment). |

**Counts:** 2 CRITICAL, 13 HIGH, 25 MEDIUM, 8 LOW (total 48).

## Discussion per dimension

### D1 Evidentiary chain

The largest finding class. The academic paper's statistical chain is generally defensible — most numbers are anchored to named scripts and CSVs — but four seams remain.

1. **Load-bearing MCMC percentiles** (ACA-14): the p100 / p1.7 flags at L393 are the structural-floor finding's teeth. Partial-coverage (57 / 70 / 87 districts) mixing in one table is a hostile-cross-examination target; the paper discloses it but does not propagate the uncertainty into the percentile labels.
2. **338Canada source URLs** (ACA-11, ACA-12, ACA-15): 77 historical snapshots plus per-riding 2023 error statistics all need FROZEN_MANIFEST entries. 338Canada archives' retention is not guaranteed, analogous to the X-post risk the public-report pass flagged.
3. **Canadian base-rate sample** (ACA-13): the seven-cycle sample's input data (seven separate commission reports + vote datasets + crosswalks) needs full manifest coverage. Paper acknowledges the proxy limitation but not the archival status of the underlying inputs.
4. **Abstract-level claims without inline anchors** (ACA-10): the Abstract asserts structural facts ("fragmentation of Airdrie across four EDs") as if established. Academic convention expects either inline §-reference footnotes or a self-containment rule (Abstract states; body proves). The paper mixes both. Fix: either footnote-anchor each Abstract claim to its §3.x / §4.x home, or move the claim's cite into the body only.

### D2 Attribution accuracy

Seven distinct external-citation gaps raise the academic edition's exposure higher than the public edition's.

1. **Citation ghosts** (ACA-03, ACA-04, ACA-05, ACA-35): Altman & McDonald (2011), Magleby & Mosesson (2018), ASA (2016, 2019), Nosek et al. (2018), Munafò et al. (2017), Driedger (1983) — six in-text citations that do not appear in References. Each is an academic reader's first-click failure.
2. **Gill v. Whitford 7% threshold** (ACA-01): four occurrences, misattribution of a Stephanopoulos-McGhee threshold to a SCOTUS decision that vacated on standing. Extends references-pass CRIT-01. Cross-examination target.
3. **Case-name formatting** (ACA-06): *Rizzo v. Rizzo Shoes* should be *Rizzo & Rizzo Shoes Ltd. (Re)*. Absent from References. Extends references-pass HIGH-04.
4. **News and academic citations without URLs** (ACA-17, ACA-18, ACA-30): multiple references with no link. Academic edition should cite with URL + archive per D1 standard.

### D3 Individual-actor characterisation

The academic paper uses stronger verbs than the public report in a few places. Each is defensible but each is worth tightening.

1. **"materially misrepresents the submission record"** (L568, ACA-08) about the chair's "no public support" claim. "Misrepresents" carries an imputation of misrepresentation-qua-falsehood that a hostile reader may construe as intent-claim. Recommend "materially overbroad" / "substantively overbroad" as fact-side alternatives. The tiered verdict at L570–583 is well-constructed; the "materially misrepresents" framing at L568 is the load-bearing adjective above the tiers.
2. **"elides this distinction"** (L538, ACA-09) about the Premier's framing of R5. "Elides" carries selective-concealment connotation. Recommend "does not carry" or "omits" for neutrality.
3. **"got it wrong"** (L518, ACA-28) about R5 and R11's school-district claims. Punchy in an academic register; L518's alternative "do not survive primary-source verification against Alberta Education school-division boundaries" is the academic-edition form.
4. **Chair-alone vs majority-consensus distinction** (cross-ref to references-pass MED-03) is handled correctly in §5.2 L538 "personal recommendation of the chair, not a collective recommendation of the three-member majority" and in L544 "the committee's present mandate does not carry forward." Academic-edition precision is high here.

The core test for each characterisation is whether the underlying fact-anchor is reproducible. For the chair's claim (§5.4), the fact-anchor is the submission-search dataset; for R5's provenance (§5.2), the anchor is the commission PDF p. 66; for school-district crossings (§4.4), the anchor is Alberta Education's school-division boundary data. Each is either referenced to or embedded in the repo. Defamation-defence in Canadian common law (truth / fair comment / *Grant v. Torstar* responsible communication on matters of public interest) is well-supported for all three, provided the underlying artifacts survive the D1 / D4 checks.

### D4 Methodology reproducibility

Three load-bearing reproducibility gates need author-verified reproduction before the academic edition is tendered in evidence.

1. **MCMC percentiles** (ACA-14) — §3.11's p-values. The `mcmc_ensemble.py` script plus `gerrychain 0.3.2` plus seed 42 plus 10,000 samples plus the voting-area GPKG must produce these exact percentiles on a fresh run.
2. **Chen-Rodden validation** (ACA-26) — 150 random-walk plans + Moran's I z=12.15 + median −2.3 to −2.4% EG + 9.3% / 15.9% surplus rates. `analysis/scripts/chen_rodden_alberta.py` must reproduce.
3. **Appendix C legal baseline** (ACA-40) — 4,745 MAD on 87 2019 EDs × 2021 DA populations × geopandas overlay. `analysis/scripts/a1_legal_baseline_2021_census.py` must reproduce.

All three are self-contained within the repo + public datasets. The framework's script-reproducibility parallel agent (parallel assignment 3 per framework.md L125) is the correct venue. Fail on any of the three is CRITICAL; the academic paper's synthesis section hinges on each.

### D5 Data provenance

Most CSVs and GPKGs cited by name in the academic paper have a documented path: `data/v0_1_mcmc_ensemble_samples.csv`, `data/v0_1_mcmc_ensemble_percentiles.csv`, `data/v0_1_338canada_historical_snapshots.csv`, `data/v0_1_alberta_byelections_2019_2026.csv`, `data/alberta_2021_da_populations.csv`, etc. Each needs a provenance header pointing at FROZEN_MANIFEST per the framework standard. The D5 parallel-agent pass (framework.md L124) is the correct venue.

Two artifact-names in the academic paper do not appear in the current data inventory from this pass's file listing:
- `data/v0_1_canadian_redistribution_base_rate.csv` (ACA-13) — needed for the seven-cycle base-rate claim
- `data/v0_1_2015_to_2019_crosswalk.csv` (ACA-19) — needed for 2015 cross-election attribution

Both should be confirmed present + documented in the D5 parallel pass.

### D6 Privilege / scope (fact vs opinion vs allegation)

Academic paper's fact/opinion labelling is generally crisp. §3.6 "Revised framing" L311–L321 is a model of self-aware scope setting — it says what the data supports, what the mechanism does, what the corrected framing is, and where the finding is weakened by the correction. The stress-test preamble at L64–L86 is similarly disciplined.

Three places where the fact/opinion line is less crisp (each HIGH or MED above): "materially misrepresents" (L568), "elides this distinction" (L538), "got it wrong" (L518). The paper does not hide these as opinions dressed as facts — each is tied to a primary-source or analytic anchor — but the verb choice invites hostile re-characterisation.

The E2-reformulation move (L367, ACA-07) is the remaining D6 residual. The paper discloses the reformulation and argues for its purposive-interpretation grounding under *Rizzo*. A hostile reviewer will still read it as ad-hoc rescue. The academic edition's advantage here is that it *names* the reformulation as such and defends it; the public edition does not. Fix: explicitly label the E2 reformulation as "post-test reformulation on purposive-interpretation grounds; declared; not pre-registered in the narrow form" rather than letting "reformulated" carry the full weight. This is a one-sentence insertion at L361.

### D7 Conflict of interest

L7 names author and institution; L121–L124 discloses prior + three findings that ran against it. That is further than the public report (zero disclosure). Residual: party-donation history, prior election-admin involvement, current candidacy status, academic-supervisor affiliation. See ACA-32 for the checklist.

### D8 Copyright / fair dealing

Low risk. Data-sources list (L24–L31) is public-domain government. Map images are s.29 criticism/research defensible with attribution (paper provides). No problematic quotations exceeding fair-dealing length. PASS.

### D9 PII / confidentiality

Low risk. No PII. Named submitters (Alan Balson, Chad Krahn, former reeve cited by EBC ID) are public-record identifications they themselves made by submitting to the commission. SAFE.

### D10 Time-stamped / falsifiable claims

Strong. Three explicit falsifiability hooks are concretely specified:
- L407 (ACA-33): 100k-sample full-coverage rescore hook — named, awaiting.
- L422 (ACA-34): OSF pre-registration with 2026-11-02 embargoed release — named date.
- L842–L846 (ACA-45): five enumerated falsification conditions — each with a concrete threshold.

Plus the §3.5 cross-election contingency disclosure at L261–L271 (asymmetry reverses under 2019 and 2015 votes) is itself a falsification-on-open-terms move. D10 PASS with minor tightening (ACA-33 should time-stamp the 100k rescore's expected release date).

## Cross-consistency with earlier red-team passes

This pass extends, not duplicates, earlier passes.

- **References red-team** (`v0_1_red_team_references.md`, dated 2026-04-23): its CRIT-01 (Gill v. Whitford 7%) extends to the academic paper at ACA-01. Its HIGH-04 (Rizzo case-name) extends to ACA-06. Its HIGH-03 (submission total count) is an internal inconsistency between reports — academic paper uses 1,340 at L564 and 1,140+ at L846, which is internal to the academic paper. Framework-level fix (pick one number and use consistently).
- **Conclusions red-team** (`v0_1_red_team_conclusions.md`): its CRIT-02 (engineered-boundary retract-and-rescue) informs ACA-07. Its CRIT-01 (2019 direction-reversal internal contradiction) is a public-report framing concern; academic paper handles the same issue more carefully at §3.5 L261 and §7 L778–L780 but still carries the Abstract's "directionally-consistent across six dimensions" claim, which should be footnoted to name the two conditions under which the direction reverses.
- **Latent-bias red-team** (`v0_1_red_team_latent_bias.md`): CRIT-01 (mis-counting Miller among "NDP-nominated") is a public-report concern; academic paper's §5.2 at L538 handles the distinction correctly. Academic paper does not have the same bias.
- **Assertions red-team** and **Code red-team** (not read in this pass) should be cross-checked for residuals before release.

## Recommended next actions

1. **Fix ACA-01 (Gill v. Whitford 7% threshold)** at all four L-sites. One-sentence edit per site. Before release.
2. **Resolve ACA-02 (0.58 / 0.51 / 0.6–1.6 inconsistency)**. Pick one headline framing; update Abstract, Stress-Test Preamble, §3.4, and §7 synthesis table to match. Twenty-minute edit. Before release.
3. **Add References entries for Altman & McDonald (2011), Magleby & Mosesson (2018), ASA (2016/2019), Nosek et al. (2018), Munafò et al. (2017), Driedger (1983)** — ACA-03, ACA-04, ACA-05, ACA-35. Six entries. Before release.
4. **Fix Rizzo case-name** at L369, L382, and add to court-cases section. ACA-06. Before release.
5. **Tighten three verbs**: "materially misrepresents" → "materially overbroad" (L568); "elides this distinction" → "does not carry / omits" (L538); "got it wrong" → "do not survive primary-source verification" (L518). ACA-08, ACA-09, ACA-28. Before release.
6. **Label E2 reformulation** explicitly at L361 as "post-test reformulation on purposive-interpretation grounds; declared; not pre-registered in narrow form." ACA-07. Before release.
7. **Queue the script-reproducibility agent (framework.md L125)** to run `mcmc_ensemble.py` + `chen_rodden_alberta.py` + `a1_legal_baseline_2021_census.py` and verify ACA-14 / ACA-26 / ACA-40 percentiles and MADs reproduce exactly. Block release on any divergence.
8. **Queue the data-provenance agent (framework.md L124)** to confirm ACA-13 and ACA-19 artifacts exist with documented provenance.
9. **Expand §1.4 author disclosure** per ACA-32 checklist (party donation / prior election-admin / current candidacy / supervisor affiliation).
10. **Time-stamp the MCMC 100k rescore** at L407 (ACA-33) — name the expected report date.
11. **Harmonise submission count** (1,340 vs 1,140+ vs 1,252) across the paper, using round-1 vs round-2 labelling consistently; extends references-pass HIGH-03.

## Not-yet-reviewed in this pass

- **Per-script reproducibility** — the ten named scripts under §3–§6 each need a fresh-run verification to confirm they produce the numbers cited. Framework parallel-agent assignment 3.
- **Per-artifact D5 provenance** for the 15+ CSV / GPKG files the paper cites by name — framework parallel-agent assignment 2.
- **Per-URL D1 archive verification** for the 30+ external URLs in the paper's Data Sources and inline mentions — framework parallel-agent assignment equivalent (URL-by-URL WebFetch).
- **Appendix E and commission-PDF page-cite verification** (L201, L205, L352 references, L363, L383) — framework's Quote-Verification parallel agent (assignment 1) covers this.
- **Supplementary analysis-doc assertions** — 25+ `analysis/v0_1_*.md` files underpin specific paper claims; each should be spot-checked that its own headline matches what the paper attributes to it. Framework parallel-agent assignment 4 (academic-report pass) overlaps with framework.md assignment 3 (analysis-docs pass).
- **Draft vs final numbers** — paper is labelled "Draft — April 2026"; the published-release version should re-confirm every numeric against a final frozen snapshot.

## Parallel-agent assignment (for framework.md L125 restart)

When rate limits reset, four agents run in parallel:

1. **Quote verification** — verify every in-text citation (see D2 discussion). Produces `analysis/red_team/v0_1_quote_verification_log.md`.
2. **Data provenance** — confirm every `data/*.csv|gpkg|json` artifact has a documented provenance chain per D5. Produces `analysis/red_team/v0_1_legal_red_team_data_artifacts.md`.
3. **Script reproducibility** — re-run `v0_2_packing_cracking_analysis.py`, `v0_3_monte_carlo_ci.py`, `mcmc_ensemble.py`, `chen_rodden_alberta.py`, `a1_legal_baseline_2021_census.py`, `338canada_reallocate.py`, `csd_community_splits.py`, `v0_1_cochrane_journey_to_work.py` (if exists), and confirm numbers match the paper. Produces `analysis/red_team/v0_1_legal_red_team_scripts.md`.
4. **Analysis-doc consistency** — for each of the ~25 `analysis/v0_1_*.md` files cited by name in the academic paper, spot-check that the file's own headline or findings match what the paper attributes. Produces `analysis/red_team/v0_1_legal_red_team_analysis_docs.md` (framework assignment 3 overlaps).

The conductor consolidation (framework.md L123 "seventh agent") should apply a blocking rule: any CRITICAL across the six findings files blocks release; any HIGH count above an agreed threshold (framework does not specify; suggest 15 aggregate across the six files) triggers a second editing pass before release.

---

*End of legal red-team findings for `report_academic.md`.*
