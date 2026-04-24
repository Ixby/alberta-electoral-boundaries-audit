# Science red-team: S6 prior art, S7 data quality, S10 peer-review readiness

**Scope:** Alberta Electoral Boundaries Audit, `report_academic.md` and supporting data artifacts (as of 2026-04-23).
**Framework:** `analysis/v0_1_science_red_team_framework.md`, dimensions S6, S7, S10.
**Method:** read `report_academic.md` end-to-end; WebSearch/WebFetch every cited author-year; compute per-artifact coverage/integrity using pandas + geopandas; walk every report section against a standard IMRaD + reproducibility checklist.

---

## Summary table

| Dimension | CRITICAL | HIGH | MED | LOW | Total |
|---|---|---|---|---|---|
| S6 Prior art | 2 | 3 | 4 | 1 | 10 |
| S7 Data quality | 0 | 3 | 5 | 2 | 10 |
| S10 Peer-review readiness | 0 | 2 | 6 | 2 | 10 |
| **Total** | **2** | **8** | **15** | **5** | **30** |

**Two CRITICAL findings are both in S6**, both fabricated / mis-attributed citations (Pal 2015 with broken DOI; Pal 2019 DOI resolving to a different paper by a different author). These must be fixed before any academic submission because a reviewer will check DOIs.

**Headline reading:** S7 data-quality story is mostly good — the data artifacts are well characterised in the report and the integrity checks reproduce reported counts — with the single big exception being the 2023 VA polygons carrying only ~55 % of total 2023 two-party votes. S10 structural readiness is MED-grade: the paper has every expected section in some form but uses idiosyncratic naming ("Section A/B/C/D" / "tracks") and lacks a checklist-style data-availability block and a conflicts / funding statement. S6 prior-art engagement is the weakest dimension and the blocking one for submission.

---

## Status update — 2026-04-23 (post-T0/T1/T2 remediation)

Authoritative current-state view of the findings raised in this file against the remediation commits that landed 2026-04-23 (d25e659 T0, a62eb53 T1, de7c48e T2, afb3a4a + 3b7dbfb session-12 data pipeline).

| Finding | Status | Fix location |
|---|---|---|
| S6-01 (CRITICAL) Pal (2015) broken DOI | PARTIAL | d25e659 corrected Rizzo universally to *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27; the Pal (2015) replacement itself is not in T0/T1/T2 scope. Still open — must be replaced before submission. |
| S6-02 (CRITICAL) Pal (2019) DOI resolves to different paper | NOT ADDRESSED | No remediation commit touches the Pal (2019) entry. Still open — must be replaced before submission. |
| S6-03 (HIGH) Altman & McDonald (2011) ghost-cite | PARTIAL | de7c48e §6 Discussion explicitly invokes Altman-McDonald (2011) as authority for the multiple-comparison posture, providing one engaged use; full References entry still required. |
| S6-04 / S6-05 (HIGH) Magleby & Mosesson 22% mis-attribution | NOT ADDRESSED | No remediation commit re-sources the 22% statistic. Still open. |
| S6-06 / S6-07 / S6-08 (MED) ASA / Nosek / Munafò ghost-cites | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual cleanup for pre-submission pass. |
| S6-09 (MED) Driedger 1983 ghost-cite | NOT ADDRESSED | Not in T0/T1/T2 scope; Rizzo citation form was corrected (d25e659) but Driedger reference entry still missing. |
| S6-10 (LOW) Chen & Rodden year label | NOT APPLICABLE | File itself notes the discrepancy is in the framework prompt, not the audit. |
| S6.4 missing-citations table (Pildes, Tam Cho, Courtney engagement, DeFord/Fifield/Herschlag/Becker, Altman-McDonald-Stout, Carty year fix, Alberta-specific commentary) | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual for pre-submission pass. |
| S7-01 (HIGH) VA polygons carry only ~55% of 2023 two-party votes; MCMC ensemble substrate-dependent | ADDRESSED | afb3a4a + 3b7dbfb wire in the Advance-Vote Splat: Phase 4C two-party total now 1,706,249/1,706,233 against target 1,706,304 (>99.99% coverage); MCMC rescore reads canonical shapefiles. a62eb53 §5.4 further downgrades ESS-150 tail from p100/p1.6 to p95.35/p2.5 at chain effective precision. The VA-substrate bias S7-01 flagged is substantially closed. |
| S7-02 (HIGH) 88 missed submissions non-random | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual finding. |
| S7-03 (HIGH) 338Canada n=87 vs 2026 n=89 transparency | NOT ADDRESSED | Not in T0/T1/T2 scope (transparency fix; one-sentence disclosure still pending). |
| S7-04 (MED) MCMC partial-coverage self-consistency caveat | ADDRESSED | afb3a4a + 3b7dbfb canonical-shapefile rescore closes the partial-coverage concern by scoring against the full canonical 89-ED set; a62eb53 also adds ESS downgrade + Core-vs-Margin VA partition documenting ~8–12% of two-party votes in Margin VAs with max ±1.5pp swing. |
| S7-05 / S7-06 / S7-07 / S7-08 / S7-09 / S7-10 (MED/LOW) | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual housekeeping for pre-submission pass. |
| S10-01 (HIGH) OSF pre-registration not filed | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S10-02 (HIGH) Methods/results fragmented | NOT ADDRESSED | Structural IMRaD restructure not in T0/T1/T2 scope. |
| S10-03 through S10-10 (MED/LOW) formal captions, A/B/C/D labeling, Data-/Code-availability blocks, COI/funding/acknowledgements, figure numbering, Carty year | NOT ADDRESSED | Structural pre-submission cleanup; not in T0/T1/T2 scope. |
| Implicit finding — sign-convention ambiguity across EG / MM / declination | ADDRESSED | a62eb53 §4.3 introduces universal sign-convention glossary (negative = UCP advantage, positive = NDP advantage). |
| Implicit finding — Gill v. Whitford characterization | ADDRESSED | d25e659 corrects Gill v. Whitford language in 4 places (SCOTUS vacated/remanded on standing; did not adopt 7% threshold). |
| Implicit finding — DPG localization uncertainty disclosure | ADDRESSED | d25e659 §4.1.4 adds central DPG disclaimer (perimeter-mode ±500m vs area-mode up to >100% on Tier-C) + 48-hour sunset clause against official Elections Alberta 2026 shapefiles. |
| Implicit finding — two-measurement contradiction (−1.42pp vs +4.15pp) | ADDRESSED | d25e659 Abstract + §5.2.7 reframe as systematic spatial-resolution sensitivity, not contradiction. |

Historical finding records in the rest of this file remain unchanged for audit-trail continuity; this section is the authoritative current-state view.

---

## §S6 — Prior-art engagement

### §S6.1 Verification of audit's claimed citations

For each citation in the "audit cites…" list from the framework prompt, the target paper was fetched by WebSearch and its title / year / venue cross-checked against the characterisation in `report_academic.md`.

| Audit cites | Verified paper | Characterisation match? |
|---|---|---|
| Stephanopoulos & McGhee (2014/2015) — EG | "Partisan Gerrymandering and the Efficiency Gap", *U Chicago Law Review* 82(2), 2015 (2014 in working-paper form, 2015 in print) | **Yes.** Audit's description of wasted-vote definition and seat-based EG is consistent with the paper. The audit cites "Stephanopoulos & McGhee, 2014" in `3.2` and 2018 in `3.2`; both years exist as distinct publications, and the paper uses the 2015 print version's math. Sign-convention discrepancy disclosed openly (§3.2, §8.1). |
| Warrington (2018) — declination | "Quantifying Gerrymandering Using the Vote Distribution", *Election Law Journal* 17(1), 2018 | **Yes.** Audit's description of declination as "angle between the best-fit lines" across each party's winning-district clouds matches Warrington's formulation. |
| McDonald & Best (2015) — MM | "Unfair Partisan Gerrymanders in Politics and Law: A Diagnostic Applied to Six Cases", *ELJ* 14(4), 2015 | **Yes.** MM = mean − median NDP share matches the paper's diagnostic. |
| Chen & Rodden (2013) — natural-packing | "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures", *QJPS* 8(3), 2013 | **Yes.** Audit uses 2013 QJPS version; §3.6 engages the natural-packing argument and correctly notes Alberta's *mechanism* differs from the US case (rural dispersion, not urban packing). The framework's citation as "Chen & Rodden (2015)" is a minor inconsistency — the 2015 *Election Law Journal* paper exists ("Cutting through the Thicket") but the audit's arguments engage the 2013 paper. |
| Altman & McDonald (2011) — redistricting audit discipline | Likely Altman & McDonald (2011), "BARD: Better Automated Redistricting", *J Statistical Software* 42(4) | **Partial.** BARD is a software tool, not an audit-discipline paper per se. The framing "four-axis redistricting-audit discipline of Altman and McDonald (2011)" (L774) is a simplification; the "four axes" framing is not a direct quote from BARD. **The bibliographic entry is missing from the References list** — see S6.3. |
| Gelman & King (1994) — seats-votes partisan symmetry | "A Unified Method of Evaluating Electoral Systems and Redistricting Plans", *AJPS* 38(2), 1994 | **Yes.** JudgeIt predecessor. |
| Tufte (1973) — seats-votes curve | "The Relationship Between Seats and Votes in Two-Party Systems", *APSR* 67(2):540–554, 1973 | **Yes.** Audit's B4 uniform-swing 50/50 projection is a simplified version of Tufte-Gelman-King seats-votes methodology. Tufte (1973) is referenced in the text but not included in the References list — MED S6 citation ghost. |
| Katz, King & Rosenblatt (2020) — consistency-across-N | "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies", *APSR* 114(1), 2020 | **Yes.** Audit's use in "when single dimensions are underpowered, cross-dimensional agreement is the inferential artefact" is a reasonable paraphrase of the paper's argument that multiple statistical measures should agree on the same theoretical quantity. |
| Grant v. Torstar (2009 SCC) — responsible-communication | 2009 SCC 61, [2009] 3 SCR 640 | **Yes** (case real and cited correctly in the legal-red-team report). Does NOT appear in `report_academic.md` — only in `report_public.md` and legal-red-team files. Confirm scope: the academic paper relies on *Rizzo* for purposive interpretation of §15(2), not *Grant* for responsible-communication defence. |
| Rizzo v. Rizzo Shoes (1998 SCC) — purposive interpretation | *Re Rizzo & Rizzo Shoes Ltd* [1998] 1 SCR 27 | **Yes.** §3.9 (L369) uses Rizzo's purposive-interpretation Driedger quote correctly. **Driedger 1983** is cited in legal red-team docs but not in References — MED S6 citation ghost. |

### §S6.2 CRITICAL — two likely-fabricated citations

**S6-01 (CRITICAL). Pal (2015) "The fragmentation of party politics and the rise of political fixers"**
- **Claim:** `report_academic.md` L995 lists Pal, M. (2015). *University of Toronto Law Journal* 65(3): 293–324. DOI 10.3138/utlj.2767.
- **Evidence:** The DOI `10.3138/utlj.2767` returns HTTP 404. Targeted WebSearch for the exact title + author produces no matches. Pal has publications in this period (*McGill Law Journal*, various SSRN working papers, "Evaluating Bill C-76" in *Journal of Parliamentary and Political Law* 2019) but no paper with this title, pagination, and DOI appears in any WorldCat, SSRN, or journal-index match.
- **Reviewer objection:** A reviewer who click-tests the first Pal entry encounters a broken DOI. This is one of the two most-damaging findings in a peer-review triage — fabricated citations disqualify a paper on sight.
- **Status:** Highly suspected fabrication or transcription error from a similar paper. Needs author verification and replacement with a real Pal source.
- **Recommendation:** **Before submission**, either (a) obtain Pal's CV and confirm the 2015 title or (b) replace with a verifiable Pal source. Candidate replacements: Pal, M. (2016). "Fair Representation in the House of Commons?" SSRN 2705498; Pal, M. (2017). "Canadian Electoral Boundaries and the Courts". *McGill Law Journal*.

**S6-02 (CRITICAL). Pal (2019) "The Charter and the constitutionality of electoral boundaries"**
- **Claim:** `report_academic.md` L997 lists Pal, M. (2019). *Canadian Journal of Law and Jurisprudence* 32(2): 323–346. DOI 10.1017/cjlj.2019.16.
- **Evidence:** The DOI `10.1017/cjlj.2019.16` resolves (via Cambridge Core) to "Retributivism and the Use of Imprisonment as the Ultimate Back-up Sanction" by William Bülow, published *CJLJ* 32(2), 2019. Not a Pal paper and unrelated topic. Pal's 2019 publications in this space are in *McGill Law Journal* (unwritten-principle-of-democracy) and *J Parliamentary & Political Law* (Bill C-76), not *CJLJ*.
- **Reviewer objection:** The DOI resolves to a different paper by a different author on an unrelated topic. This is the canonical "hallucinated citation" signature.
- **Recommendation:** **Before submission**, replace with a real Pal Charter-and-boundaries source. Candidate: Pal, M. (2016). "The Fractured Right to Vote", *McGill Law Journal* 62(1):171–212 (exists and is on-topic).

### §S6.3 HIGH / MED — Citation ghosts (in-text cites with no References entry)

Identified by audit's own `v0_1_red_team_references.md` and independently reproduced here. Each needs a References entry before submission.

| Finding | In-text cite | References entry? | Severity |
|---|---|---|---|
| S6-03 (HIGH) | Altman & McDonald (2011) — L774 "four-axis redistricting-audit discipline" | Missing | Add Altman, M., & McDonald, M. P. (2011). BARD. *J Statistical Software* 42(4). Before submission. |
| S6-04 (HIGH) | Magleby & Mosesson (2018) — L299 "~22% US-state disagreement rate between declination and EG" | Missing + possible mis-attribution (see S6-05) | Before submission. |
| S6-05 (HIGH) | The claim that Magleby & Mosesson (2018) "document a ~22% disagreement rate" | Magleby & Mosesson (2018) is **"A New Approach for Developing Neutral Redistricting Plans"** in *Political Analysis* 26(2) — an **algorithm** paper, NOT a cross-metric disagreement-rate paper | Finding is at best a mis-attribution; at worst a fabricated statistic. The ~22% figure may come from Warrington (2019) *ELJ* "A Comparison of Partisan-Gerrymandering Measures" but was not verified in this pass. **Re-source the 22% number or remove the claim.** |
| S6-06 (MED) | ASA (2016, 2019) — L450 "ASA guidance on graded evidence reporting" | Missing | Likely refers to Wasserstein & Lazar (2016) "The ASA's statement on p-values" and Wasserstein, Schirm & Lazar (2019) "Moving to a world beyond p < 0.05". Add both to References. |
| S6-07 (MED) | Nosek et al. (2018) — L450 + L916 | Missing | Likely Nosek, B. A. et al. (2018). "The preregistration revolution". *PNAS* 115(11):2600–2606. Add to References. |
| S6-08 (MED) | Munafò et al. (2017) — L450 | Missing | Likely Munafò, M. R. et al. (2017). "A manifesto for reproducible science". *Nature Human Behaviour* 1:0021. Add to References. |
| S6-09 (MED) | Driedger's purposive principle — L369 | Missing | Driedger, E. A. (1983). *Construction of Statutes* (2d ed., Butterworths). Canonical source for the purposive-interpretation rule *Rizzo* adopted. Add to References (under "Legal and statutory"). |
| S6-10 (LOW) | Chen (2017), Chen & Rodden framework-year mismatch (framework says "2015"; audit uses 2013) | 2013 is correctly listed in References | Inconsequential; framework's listing is the discrepancy, not the audit's. |

### §S6.4 Missing citations (works the audit should cite but doesn't)

A peer reviewer in *Election Law Journal* or *Statistics and Public Policy* would flag the following omissions. Each should be **added** to the References and engaged in the relevant section. The most important five are flagged with the section they best fit.

| Author (year) | Title | Why it must be cited | Severity (if omitted) | Section to engage |
|---|---|---|---|---|
| Pildes, R. H. (2016) | "Political Fragmentation in Democracies of the West", *Journal of Political Philosophy* OR the efficiency-gap critique in the 2017–18 *Gill v. Whitford* amicus literature | The 7 % EG threshold the audit relies on (abstract; §3.3; §B2) has been the subject of a sustained critique Pildes and others lead. Any EG-based argument must acknowledge the critique. | HIGH | §3.2, §3.3, §8.1 |
| Persily, N.; Pildes, R. H. (~2017) | *Brennan Center* / *Stanford Law Review* exchange on the efficiency-gap debate | Same reason as above; round out the EG-threshold critique. | MED | §3.2, §3.3 |
| Magleby, D. B., & Mosesson, D. B. (2018) | "A New Approach for Developing Neutral Redistricting Plans", *Political Analysis* 26(2):147–167 | This is the paper the audit actually cites at L299 — but the audit's current claim (22 % disagreement rate) is NOT in this paper; this paper is a redistricting-algorithm paper, not a cross-metric disagreement paper. Correctly citing or re-sourcing this is both HIGH (the claim) and MED (completeness). | HIGH | §3.5.1 |
| Warrington, G. S. (2019) | "A Comparison of Partisan-Gerrymandering Measures", *ELJ* 18(3) | Already in References. But the 22 % disagreement-rate statistic may actually come from this paper, not from Magleby & Mosesson. **Cross-reference and re-attribute**. | HIGH (also resolves S6-05) | §3.5.1 |
| Tam Cho, W. K., & Liu, Y. Y. (2016/2018) | "Toward a Talismanic Redistricting Tool" or "A Massively Parallel Evolutionary Markov Chain Monte Carlo Algorithm for Sampling Contiguous Redistricting Plans", *Operations Research Letters* | The audit's MCMC §3.11 uses GerryChain's ReCom sampler; Tam Cho's super-computer ensemble work is the necessary prior on the scaling properties of ensemble-sampling redistricting. A reviewer in *Statistics and Public Policy* or *Election Law Journal* will flag its absence. | HIGH | §3.11 |
| DeFord, Duchin, Solomon (2021) | Already in References — "Recombination: A family of Markov chains for redistricting", *HDSR* 3(1) | In References (L977) but never *cited in the body*. Engage in §3.11 to justify the ReCom chain's theoretical properties (reversibility, mixing time, bias/variance tradeoff). Currently orphan-cited. | MED | §3.11 |
| Fifield, Imai, Kawahara, Kenny (2020) | Already in References — "Essential role of empirical validation", *Statistics and Public Policy* 7(1) | Same — orphan-cited. Use to justify the audit's convergence-diagnostics plans (ESS, trace plots) and to frame the 57 / 70-polygon partial-coverage caveat. | MED | §3.11 |
| Herschlag, Ravier, Mattingly (2020) | Already in References — "Quantifying gerrymandering in North Carolina", *SPP* 7(1) | Orphan-cited. Engage in §3.11 as the methodological precedent for placing an enacted map against an ensemble on multiple metrics. | MED | §3.11 |
| Becker, Duchin, Gold, Hirsch (2021) | "Computational Redistricting and the Voting Rights Act", *ELJ* 20(4) | For VRA-adjacent measurement-literature — if the audit ever touches Indigenous-representation arguments (it does: Enoch Cree, Tsuut'ina, Siksika, Piikani name-etymology in §4.4) it should ground the Indigenous-EDs analysis in this paper's framework. | MED | §4.4, §5.5 |
| Courtney, J. C. (2001) | Already in References — *Commissioned Ridings* | In References but not *engaged* in §5 procedural audit. The audit's claim that "the April 16 action is the most government-controlled response…among the three most commonly cited Canadian comparator cases" explicitly needs Courtney's full provincial / federal survey to be either confirmed or bounded. | HIGH | §5.3 |
| Pal, M. (real citations; see S6-01, S6-02) | Verifiable Pal work on Canadian electoral boundaries | The audit leans on Pal twice (likely-fabricated). A real Pal citation on boundaries must replace them. | CRITICAL (S6-01, S6-02) | §5.3, §5.5 |
| Carty, R. K. (2015) | *Big Tent Politics* | In References but not engaged. A reviewer would expect at least one sentence drawing on Carty's brokerage-model argument for why Canadian independent commissions produce different partisan-bias patterns from US map-drawers. Note: audit says 2017; UBC Press lists 2015. Fix year. | MED | §5.3 |
| Altman, McDonald, Stout (2017) | "A Public Transparency Framework for the Evaluation of Election Administration", *PS: Political Science & Politics* 50(3) | Audit's `analysis/v0_1_fortification_c1_c10.md` references this explicitly as the extension of the Altman-McDonald 2011 framework. It's the direct source of the "four-axis" framing. | MED | §7 |
| Alberta-specific post-2020 redistribution commentary | E.g., media commentary from Duane Bratt, Melanee Thomas, Lisa Young on 2025–26 Alberta redistribution | The audit's §1.4 author-disclosure notes Bratt as an outreach contact (`analysis/v0_1_duane_bratt_outreach_email.md`); but no academic commentary by Bratt or Thomas on the 2025–26 cycle is cited. A reviewer would expect at least one Alberta-political-science citation contextualising the 2025–26 cycle. | MED | §1.4, §5.2 |

**Missing-citations count: 14** (of which 2 CRITICAL S6-01/S6-02 = must-replace; 6 HIGH = must-add-or-re-attribute; 6 MED = should-add-for-scholarly-completeness).

---

## §S7 — Data quality (coverage, selection bias, measurement error, time-stamp currency)

### §S7.0 Integrity check summary (performed in this pass)

| Artifact | Expected | Observed | Status |
|---|---|---|---|
| `data/v0_1_alberta_2023_results.csv` | 87 rows (2019 EDs), two-party total 1,706,304 | 87 rows, `total_valid_votes` sum matches when including all parties | PASS |
| `data/v0_1_alberta_2015_results.csv` | 87 rows | 87 rows, total votes 1,433,745; NDP 583,892 | PASS |
| `data/alberta_2021_da_populations.csv` | 6,203 DAs summing to 4,262,635 | 6,203 DAs, sum = 4,262,635 | PASS (exact match to StatsCan Alberta 2021 count) |
| `data/alberta_2021_csd_populations.csv` | ~421 CSDs summing to 4,262,635 | 423 CSDs, sum = 4,262,635 | PASS |
| `data/va_polygons_with_2023_votes.gpkg` | 4,765 polygons, all 2023 votes | 4,765 polygons, 87 unique EDs, zero null geometries, zero duplicates on (ED_NUM, VA_NUMBER) | PASS on polygon count; **FAIL on vote coverage** — see S7-01. |
| `data/submission_search_dataset.csv` | per `submission_search_findings.md`, 1,252 of ~1,340 submissions searched | 71 rows in CSV (= subset with at least one configuration hit); 70 with ≥1 hit. Per-configuration counts (Airdrie 4, RMH 20, ODH 5, Chestermere 13, Red Deer 23, St. Albert 11, Nolan Hill-Cochrane 0) exactly match `submission_search_findings.md`. | PASS — the CSV is the hits-only subset, which is the correct representation; the 1,252 figure is the denominator, not the CSV row count. |
| `data/v0_1_338canada_per_riding_87seat.csv` | 87 rows (2019 EDs) | 87 rows; UCP mean share 52.4 % (consistent with April 2026 snapshot in §3.5) | PASS |

### §S7.1 HIGH — VA polygon vote coverage

**S7-01 (HIGH). 2023 VA polygons carry ~55 % of 2023 total votes.**
- **Observed:** `va_polygons_with_2023_votes.gpkg` per-VA UCP + NDP + Other votes sum to: NDP 381,932; UCP 514,712; Other 35,520; **two-party 896,644; total 932,164**.
- **Report claim:** Audit's §6.3 states 1,973 polls summing to NDP 777,404 / UCP 928,900 / two-party 1,706,304.
- **Gap:** Two-party total in VA polygons (896,644) is 52.5 % of the reported 2023 two-party total (1,706,304). The remaining ~48 % consists of Advance, Mobile, and Special / Vote-Anywhere ballots, which §6.3 notes are "home-ED-attributed under Vote Anywhere" — i.e., not reflected at the VA level. The report acknowledges this at §6.3 ("47.2 % of 2023 valid votes are in non-Election-Day ballot types… all home-ED-attributed under Vote Anywhere"), but the impact on the MCMC ensemble (§3.11) is under-disclosed.
- **Reviewer objection:** The MCMC ensemble in §3.11 scores each real map against 10,000 ReCom-drawn alternatives using VA-polygon votes. If Election-Day votes differ systematically from Vote-Anywhere votes (§6.3 observes +6.25 pp NDP share under Vote-Anywhere), then every ensemble percentile computed on VA polygons carries a systematic ~6 pp skew against NDP outcomes. The MCMC percentiles in §3.11 (minority p100 mean-median / seats-at-50/50) may move once Vote-Anywhere votes are merged in.
- **Severity:** HIGH. The audit's single strongest quantitative finding (minority at p100 on two metrics) is potentially VA-polygon-substrate-dependent.
- **Recommendation:** Add an explicit coverage statement to §3.11 reading something like: "The MCMC ensemble is computed on Election-Day VA-polygon votes, which constitute 52.5 % of 2023 two-party votes. The remaining 47.5 % (Advance / Mobile / Special) are home-ED-attributed and, per §6.3, differ from Election-Day votes by +6.25 pp in NDP share. This means the ensemble percentiles in §3.11 have a systematic bias against NDP outcomes that would tighten toward NDP if Vote-Anywhere votes were apportioned. Pending Phase 4C completion (§6.3), the p100 verdicts are upper bounds; true ensemble percentiles may be closer to the ensemble interior."

### §S7.2 HIGH — submission-search coverage non-uniform

**S7-02 (HIGH). The 93 missed submissions are not randomly distributed.**
- **Observed:** 1,252 of 1,345 (93.4 %) searched; 88 (6.6 %) are image-only scans with no text layer and no EBC-ID marker. The audit's §5.4.5 limits list this but does not characterise the *content* of the 88.
- **Reviewer objection:** If the 88 are concentrated in one geographic / configuration area (e.g., all handwritten RMH-area submissions, or all city-of-Airdrie feedback attachments), the per-configuration support-rate columns in §5.4.1 shift. The audit's Rocky Mountain House-Banff Park refutation rests on 3 explicit supporting submissions out of 20 mentions; if 10 additional RMH submissions are in the OCR-missed 88, the 15 % explicit-support rate could move either direction by 5–10 percentage points.
- **Severity:** HIGH.
- **Recommendation:** (a) Sample 20 of the 88 missed submissions manually, classify each by likely configuration based on source-file batch number and submitting party, and report whether the missing ones are geographically concentrated. (b) If concentrated, apply a sensitivity band around the §5.4.1 per-configuration verdicts (e.g., "Rocky Mountain House-Banff Park: 15–25 % explicit support rate under the worst-case 88-missed assumption"). (c) If the OCR backfill in `deprecated/v0_1_submission_ocr_log.md` has already recovered some of the 88, incorporate those into the main dataset. 14 were already recovered per `submission_search_findings.md` L7.

### §S7.3 HIGH — 338Canada per-riding projection cross-check vs 2019 ED count

**S7-03 (HIGH). Audit uses 87 rows for 338Canada; this is the *2019* ED count, not the *2026* proposal count (89 each).**
- **Observed:** `data/v0_1_338canada_per_riding_87seat.csv` has 87 rows.
- **Reviewer objection:** 338Canada projections for Alberta publish at the 2019-boundary level because the 2026 proposals have no 338-model history. The audit's Phase 4C design attempts to reallocate these to 2026 via hybrid crosswalks. A reviewer checking that 338 gave 87 projections, not 89, is correct; but the audit needs to say so explicitly where it cites 338 projections.
- **Severity:** HIGH for transparency; LOW for correctness (the audit's reallocation math is on the right side of the issue per §3.5's 67/22 and 66/23 seat counts — 89 seats post-reallocation — but the disclosure is implicit).
- **Recommendation:** Add one sentence to §3.5 stating "338Canada projects at the 2019-ED level (n=87); the 67/22 and 66/23 counts in this paragraph reflect reallocation through the majority and minority hybrid crosswalks, producing 89-seat outputs."

### §S7.4 Per-artifact coverage table (completeness map)

| Artifact | Coverage % | Selection-bias assessment | Measurement-error magnitude | Time-stamp currency |
|---|---|---|---|---|
| 2023 Statement of Vote (`data/2023_results.xlsx`, `data/v0_1_alberta_2023_results.csv`) | 100 % of cast ballots (Elections Alberta publishes official SoV) | None — universal enumeration. Spoiled and rejected ballots reported separately per §B1 structure; audit uses valid votes only. | Near-zero for aggregate vote counts (official count); ~0.1 % rounding / party-name-mapping error in crosstabs. | 2023-05-29 (election day); 2023-06-21 (official return). 3-year currency window; not a concern. |
| 2015 Statement of Vote (`data/2015_results.xlsx`, `data/v0_1_alberta_2015_results.csv`) | 100 % of cast ballots | None | Same as 2023; additional crosswalk-transformation error into 2019 EDs is tracked at `data/v0_1_2015_to_2019_crosswalk.csv` (partial rows also captured). | 2015-05-05 (election day). 11-year-old data used for cross-election stability probe; currency is a *feature* of the test, not a defect. |
| 2021 Census DA populations (`data/alberta_2021_da_populations.csv`) | 100 % of DAs (6,203 in Alberta matches StatsCan count); total pop 4,262,635 matches StatsCan provincial count to the person | Small-area data is subject to StatsCan random-rounding and area-suppression for DAs under 40 residents; minimal impact on aggregate. | ±5 per DA (random rounding); aggregate error <0.1 % at ED level. | 2021-05-11 (census day); 5-year-old data is §12(3)-operative. |
| 2021 Census CSD populations (`data/alberta_2021_csd_populations.csv`) | 100 % of CSDs (423) | None | Negligible | 2021-05-11 |
| 4,765 VA polygons with 2023 votes (`data/va_polygons_with_2023_votes.gpkg`) | **100 % of Elections Alberta's published 2023 VA list** (confirmed: 87 unique EDs; no null geometries; no duplicates on (ED_NUM, VA_NUMBER)) — but only **52.5 % of total 2023 two-party votes** because Advance/Mobile/Special ballots are home-ED-attributed at the EA-published-SoV level, not attributable to VAs. See S7-01. | Election Day voters only; systematically skewed against Advance / Mobile / Special voters. Per §6.3 those voter populations differ by +6.25 pp NDP share. | Polygon assignment: ~0.5 % of VAs near ED borders have centroid-in-polygon mismatch (audit's §3.6 notes the issue and flags it as acceptable). Vote attribution: 0 % measurement error for the 52.5 % captured; the remaining 47.5 % is systematically excluded, which is a coverage issue rather than a measurement-error issue. | 2023-05-29 |
| Submission search dataset (`data/submission_search_dataset.csv`) | **93.4 % (1,252 of ~1,340 submissions searched, OCR-recovered 14 of the initial 88 missed).** The 71-row CSV = hit subset; per-configuration counts reproduce `submission_search_findings.md` exactly. | **Probable non-uniformity.** The 88 image-only scans are systematically over-represented by handwritten and unstructured submissions, which may correlate with older or rural submitters. See S7-02. | Regex keyword match rate is high-precision; position classifier (support/oppose/neutral) has ~10 % residual classification error per `deprecated/submission_search_log.md` (13 of 71 manual corrections). | 2025-05 (Round 1), 2025-10 (Round 2). Current. |
| 338Canada per-riding projections (`data/v0_1_338canada_per_riding_87seat.csv`) | 100 % of 2019 EDs (87 rows); **matches 2019 ED count, not 2026** — see S7-03. | 338 model has documented +4.77 pp UCP-underprediction bias in rural Alberta (§3.5); audit applies a +7 pp compound-uncertainty band to rural reallocation. | MAE 3.74 pp per-riding (2023 validation); winner-call 81/87 (93.1 %). | 2026-04-12 (latest snapshot); 2020-02-23 (oldest in 77-snapshot series). Current. |
| MCMC ensemble (approx majority 57/89; minority v6 70/89) | **63.8 % and 80.8 % of VA-polygon coverage respectively** (explicitly flagged in §3.11 and the full-coverage rescore is in progress). | Incomplete-coverage bias: the scored subset may be systematically different (Tier A unchanged EDs vs Tier B/C) from the full 89-ED set. §3.11's "ratios not counts" defence is correct but partial — see S7-04. | ReCom sampler is documented (`gerrychain` 0.3.2, seed 42); ensemble CI is computed at each percentile. | 2026-04 (the 10k run); the 100k run and full-coverage rescore are committed-to-be-completed before publication per §3.11. |
| Commission-map approximations (v5, v6, v7-pending) | Tier A (majority 57; minority 65): exact. Tier B (majority 0 additional; minority 5): ±500 m boundary residual → ≤0.06 % vote-share residual per §6.7 v3 refinement. Tier C (majority 32; minority 19): NOT scored (commission shapefiles unreleased). | The priority hybrid EDs (RMH-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) are all Tier C. Audit correctly flags this at §6.7. | v4 residual gap identified by PO-painted references 2026-04-23: Calgary-De Winton approximation at 60 % of true territorial footprint; Calgary-South at ~50 %; Edmonton-Windermere too small. Quantitative boundary-residual-to-vote-residual: at v4, ~318 VAs / ~62,000 votes. See §6.7 v4 residual gap discussion. | 2026-04-23 (hand-painted references; documented in §6.7). |

### §S7.5 Additional S7 findings

**S7-04 (MED). MCMC partial-coverage self-consistency caveat.**
- The §3.11 "ratios not counts" defence ("partial coverage does not invalidate the comparison — each map is evaluated on its own covered subset") is correct only if Tier A / Tier B / Tier C EDs are demographically exchangeable. They are not: Tier A excludes 2019-unchanged districts, which are disproportionately rural UCP strongholds; Tier B/C is disproportionately the hybrid configurations we are interested in. The minority's p100 on mean-median may be an artefact of scoring a non-random 80.8 % slice.
- **Recommendation:** Report the 100k-sample full-coverage rescore results as soon as available and include a sensitivity-test variant where the ensemble is restricted to the same 57 and 70 polygons for apples-to-apples percentile computation.

**S7-05 (MED). 2023 results file uses 2019 EDs (n=87) — not 2026 (n=89). Consistent with the mapping methodology but should be said out loud in §3.1.**

**S7-06 (MED). 338Canada per-riding n=87 matches 2019 ED count. Stated implicitly throughout §3.5; made explicit is a one-sentence fix. See S7-03.**

**S7-07 (MED). 2015 results crosswalk to 2019 EDs is "full" per `data/v0_1_2015_to_2019_crosswalk.csv`; "partial" at `…_crosswalk_partial.csv`. Audit uses the full crosswalk in §3.5 for the 2015 reversal test. The partial version is deprecated — confirm via file size / row count and remove the partial file to avoid two-file confusion.**

**S7-08 (MED). Alberta Treasury Board 2024 quarterly population estimate (4,888,723): verified at `analysis/methodology/v0_1_commission_source_provenance.md` (per L866 audit) against StatsCan Table 17-10-0009 Q2 2024 postcensal. Integrity passes.**

**S7-09 (LOW). Submission dataset columns include `round` with value 0 for one row — likely a data-entry artefact since rounds are 1 and 2. Clean up or document.**

**S7-10 (LOW). 6,203 DAs: the audit loads this at `data/alberta_2021_da_populations.csv` and uses it in Appendix C. The one-row-per-DA convention is consistent throughout. LOW note: the `DAUID` column is a pure string ID; casting to numeric would break. Script `v0_1_a1_legal_baseline_2021_census.py` appears to preserve string typing (not verified in this pass).**

---

## §S10 — Peer-review readiness

### §S10.1 Structural checklist

| Element (journal-standard) | Present? | Location | Notes |
|---|---|---|---|
| Title | Yes | L1 | Clear; specifies "symmetric, reproducible forensic assessment" scoping. |
| Author and affiliation | Yes | L7 | "Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student)." Undergraduate status disclosed — reviewer will note; not disqualifying for methods paper. |
| Abstract | Yes | L90 | Single-paragraph structured abstract covering dimensions A–D, key findings, caveats. Length (~300 words) is appropriate for a methods paper. |
| Data | Yes | L22, L742 ("Technical Data Statement" section) | Data sources are listed in the "Tools Used in the Academic Analysis" opening section (L22–L30) and re-stated in §6.6. Good redundancy. |
| Methods | Yes, but fragmented | §1, §2, §3, §4, §5, §6 | Methods are embedded per-section rather than in a single Methods chapter. This is the primary S10 structural departure from IMRaD. A reviewer used to IMRaD will have to reassemble the methods from 6 places. |
| Results | Yes, but fragmented | §2 (A), §3 (B), §4 (C), §5 (D), §6 (geometry), §7 (synthesis) | Same structural issue — results are per-section. |
| Discussion | Partial | §7 synthesis + §3.6 (Chen-Rodden revised framing) + §3.14 stress-test grades | No single "Discussion" section, but substantive discussion threads are present. Reviewer-navigable. |
| Limitations | Yes | §9 (Missing Evidence and Scope Limits), §10 (Falsifiability Statement), §5.4.5 (submission-search limits), §7 qualifications | Limitations are well-distributed and honest. Strong. |
| Conclusion | Partial | §7, §11 (Legal Interpretive Note) | Conclusion is threaded through §7 synthesis + §11. A single 1-paragraph "Conclusion" header would tighten the close. |
| References | Yes | L955–L1044 | 26 academic entries + 5 court cases + 1 statute + 4 data sources. **Missing 6 ghost citations (S6-03 through S6-09)**. |
| Data-availability statement | Partial | Embedded at L22 (GitHub link) + §4 ("checked-in scripts") + Appendix A reproducibility + `FROZEN_MANIFEST.md` | **No dedicated data-availability section header.** Journals increasingly require a block titled "Data Availability" with specific archive DOIs and license terms. Currently the information is correct but not checklist-discoverable. |
| Code-availability statement | Partial (same as above) | Repository URL + Appendix A | Same — no formal "Code Availability" block. |
| Pre-registration statement | Partial | §3.12 ("prepared for submission to the Open Science Framework… embargoed release scheduled for 2026-11-02") | **Pre-registration is not yet filed.** The audit plans OSF registration on 2026-11-02. Until the DOI is in the paper, pre-registration cannot be cited as a defence against post-hoc charges. HIGH S10 until filed (see S10-01). |
| Conflict of interest | **No** | — | Standard academic submissions require a COI statement. **Absent.** The audit's §1.4 author disclosure covers author priors, which is useful but not a formal COI. |
| Funding acknowledgement | **No** | — | Standard journal requirement. Absent. |
| Acknowledgements | **No** | — | Optional but expected. The audit mentions a "PO" (Wuff) in CLAUDE.md and conductor interactions; none of this is in the paper, correctly. But acknowledgement of outreach contacts (e.g., Duane Bratt per `analysis/v0_1_duane_bratt_outreach_email.md`) would be conventional. |
| Pre-submission statistical checklist | **No** | — | Election-science papers are not typically required to attach one. *Statistics and Public Policy* expects authors to have completed one internally (e.g., STROBE-adapted for observational work). Not a blocker. MED. |
| Figure / table captions complete | Partial | See §S10.3 | Most tables have implied captions (the preceding paragraph explains the source); no table has a formal `Table X: source · method · N · date` caption. Same for tables in §2.2, §3.3, §3.11, §5.4.1. |

### §S10.2 HIGH S10 findings

**S10-01 (HIGH). Pre-registration is not yet filed.**
- **Claim:** §3.12 says "submission-ready document is in `analysis/reports/v0_1_pre_registration_draft.md`; the platform survey and submission instructions are in `analysis/reports/v0_1_pre_registration_platform_analysis.md`. Once submitted, the OSF-assigned DOI will appear in §3.12 and the audit's README as the time-stamped third-party custody record." Embargoed release scheduled for 2026-11-02.
- **Reviewer objection:** A methods paper claiming pre-registration protection for P/C/E signature thresholds cannot cite an OSF DOI that doesn't exist yet. Intra-session git-timestamp provenance (§3.7 at "2 hours 24 minutes before the detection runs") is weaker than third-party OSF custody; a reviewer will ask where the DOI is.
- **Recommendation:** **File the OSF pre-registration before submission** (embargoed or not). Backdate the claim in §3.12 to cite the actual DOI. If OSF filing is genuinely tied to 2026-11-02 deadline, either (a) submit the paper after 2026-11-02 or (b) file without embargo now and simply note "embargoed for 2026-11-02 map release" is not necessary for the paper's pre-registration protection — you just need the DOI.

**S10-02 (HIGH). Methods and results are fragmented, making reviewer-linear reading hard.**
- **Observed:** Methods for §A population appear in §2.1's data-basis preamble; methods for §B partisan bias in §3.1–§3.2 mixed with results; methods for §3.11 MCMC are in a subsection of §3; methods for §6.7 compactness are embedded in §6.7.
- **Reviewer objection:** A *Statistics and Public Policy* reviewer will want a single Methods section covering: (1) data sources; (2) population-equality test; (3) partisan-bias metrics; (4) MCMC ensemble; (5) compactness; (6) symmetry-counter-tests; (7) submission-search regex. Currently these are scattered across §2, §3, §4, §5, §6.
- **Severity:** HIGH (because it takes a reviewer ~60 minutes extra to reconstruct) but **NOT CRITICAL** (the methods *are* present and reproducible, just not IMRaD-arranged).
- **Recommendation:** Either (a) add a brief "Methods summary" appendix pointing at each per-section methods fragment, or (b) restructure into formal IMRaD with a single Methods chapter before §A. Option (a) is cheaper; option (b) is the journal-conventional fix.

### §S10.3 MED S10 findings — structure + captions

**S10-03 (MED). Tables lack formal captions.**
- Every table in §2.1, §2.2, §2.3, §2.4, §3.3, §3.4, §3.10, §3.11, §3.13, §4.4, §5.4.1, §6.7, §7, Appendix C has an implicit caption (the preceding paragraph explains it) but no `Table N: [source] · [method] · [N] · [date]` header line.
- **Recommendation:** Add a one-line formal caption above each table. Required by most journals.

**S10-04 (MED). "Sections A/B/C/D" naming is idiosyncratic.**
- The audit's six dimensions (A population, B partisan bias, C geographic coherence, D procedural, §4 geometry, §5 MCMC — except the numbering in §3.11 is called "Section 5") use inconsistent top-level labels. §2 / §3 / §4 / §5 / §6 / §7 work as section numbers but the content-label letters A–D cross-reference everything.
- **Recommendation:** Either drop the A/B/C/D letter labels from the abstract and §7 synthesis table, or footnote the mapping A=§2, B=§3, C=§4, D=§5 early in the paper. Current state forces the reader to infer the mapping.

**S10-05 (MED). Data-availability block is missing.**
- Add a formal block before References:
  ```
  Data Availability
  All data used in this analysis are publicly available. Elections Alberta
  Statement of Vote files (2015, 2019, 2023) are at https://www.elections.ab.ca/.
  Statistics Canada 2021 Census dissemination-area data are at
  https://www12.statcan.gc.ca/census-recensement/2021/. Derived datasets used
  in this analysis are in the repository at
  https://github.com/Ixby/alberta-electoral-boundaries-audit under CC-BY-4.0.
  ```
- **Recommendation:** Add. 5 minutes of work.

**S10-06 (MED). Code-availability block is missing.**
- Same template as above but for scripts. Reference Appendix A's reproducibility block and `FROZEN_MANIFEST.md`.

**S10-07 (MED). Conflict-of-interest / funding / acknowledgements block is missing.**
- Add a standard block:
  ```
  Conflict of Interest
  The author declares no financial conflict of interest. The author's political
  prior is disclosed in §1.4.

  Funding
  This research received no external funding.

  Acknowledgements
  The author thanks [outreach contacts if any — Duane Bratt, etc.] for feedback.
  ```

**S10-08 (MED). Figure references (maps/*.jpg) have no on-paper figure numbers.**
- §4 ("Geographic Coherence") references `maps/majority_calgary.jpg`, `maps/minority_calgary.jpg`, etc., without formal Figure 1 / Figure 2 numbering. A print-ready submission needs each figure to have a number, caption, and in-text reference.
- **Recommendation:** Number and caption each figure. 30 minutes.

### §S10.4 LOW S10 findings

**S10-09 (LOW). Some references have bare URLs that render as live hyperlinks (Alberta EBC L961, Elections Alberta 2015/19/23 L1037–1041). Journal style (APA-7 / APSA) prefers DOIs over live URLs where both exist; the data-source URLs are appropriate given no DOI exists. Acceptable as-is.**

**S10-10 (LOW). Carty (2017) year mismatch — UBC Press lists 2015 publication. Small fix.**

---

## Missing-citations table (§S6.4 consolidated) — recommendations for academic paper

| Priority | Add citation | Section | Why |
|---|---|---|---|
| **CRITICAL** | Replace Pal (2015) — L995 — with a verifiable Pal paper | References + §5.3 | Broken DOI 10.3138/utlj.2767 |
| **CRITICAL** | Replace Pal (2019) — L997 — with a real Pal boundary paper | References + §5.3 / §5.5 | DOI resolves to a different author / topic |
| HIGH | Altman & McDonald (2011) "BARD" *J Stat Software* 42(4) | References + §7 | Currently ghost-cited |
| HIGH | Magleby & Mosesson (2018) "A New Approach for Developing Neutral Redistricting Plans" *Political Analysis* 26(2) | References + §3.5.1 | Currently ghost-cited and likely mis-attributed (the 22 % claim is not in this paper) |
| HIGH | Re-source the 22 % declination-EG disagreement-rate claim (likely Warrington 2019) | §3.5.1 | Statistic needs a verifiable source |
| HIGH | Pildes (2016) or the Pildes / Persily efficiency-gap critique | §3.2, §3.3 | 7 % EG threshold critique is canonical prior art |
| HIGH | Tam Cho & Liu (2016 / 2018) | §3.11 | Ensemble-sampling prior for MCMC §3.11 |
| HIGH | Courtney (2001) — engage in §5.3 rather than orphan-cite | §5.3 | Provides the Canadian provincial comparator survey |
| MED | ASA (2016, 2019) on p-values | References | Ghost-cited L450 |
| MED | Nosek et al. (2018) preregistration | References + §3.12 | Ghost-cited L450/L916 |
| MED | Munafò et al. (2017) reproducibility | References + §3.12 | Ghost-cited L450 |
| MED | Driedger (1983) *Construction of Statutes* | References | Ghost-cited L369 |
| MED | DeFord, Duchin, Solomon (2021) — engage in-text | §3.11 | Orphan-cited |
| MED | Fifield, Imai, Kawahara, Kenny (2020) — engage in-text | §3.11 | Orphan-cited |
| MED | Herschlag, Ravier, Mattingly (2020) — engage in-text | §3.11 | Orphan-cited |
| MED | Becker, Duchin, Gold, Hirsch (2021) VRA-ensembles | §4.4, §5.5 | Indigenous-ED framework |
| MED | Altman, McDonald, Stout (2017) transparency framework | §7 | Direct source of "four-axis" framing |
| MED | Fix Carty (2015 not 2017) year; engage in §5.3 | L967 + §5.3 | Currently orphan-cited with wrong year |
| MED | At least one Alberta-specific political-science citation (Bratt / Thomas / Young) on 2025–26 redistribution | §1.4, §5.2 | Local political-science context |

**Total missing-citations count: 19** (2 CRITICAL replacements; 6 HIGH additions / re-attributions; 11 MED).

---

## Peer-review-readiness checklist (§S10 consolidated) — pass/fail on each structural element

| Element | Pass/Fail |
|---|---|
| Title | PASS |
| Author + affiliation | PASS |
| Abstract (under 300 words, structured) | PASS |
| Data (source and location) | PASS (embedded; formal block missing — see Data-availability) |
| Methods | PARTIAL — fragmented across sections (S10-02) |
| Results | PARTIAL — fragmented across sections (S10-02) |
| Discussion | PARTIAL — threaded; no single section |
| Limitations | PASS |
| Conclusion | PARTIAL — threaded through §7 + §11 |
| References (complete, no bare-URL entries where DOIs exist, every in-text cite resolves to an entry) | **FAIL** — 6 ghost citations (S6-03 through S6-09); 2 fabricated DOIs (S6-01, S6-02) |
| Data-availability block | **FAIL** — implicit, not a dedicated block (S10-05) |
| Code-availability block | **FAIL** — implicit, not a dedicated block (S10-06) |
| Pre-registration DOI | **FAIL** — planned 2026-11-02, not yet filed (S10-01) |
| Conflict-of-interest block | **FAIL** — absent (S10-07) |
| Funding block | **FAIL** — absent (S10-07) |
| Acknowledgements block | **FAIL** — absent (S10-07) |
| Tables have formal captions (Table N: source · method · N · date) | **FAIL** — implicit captions only (S10-03) |
| Figures have formal captions and numbers | **FAIL** — figures reference raw JPG paths (S10-08) |
| Section naming follows IMRaD or journal convention | **PARTIAL** — A/B/C/D letter labels are idiosyncratic (S10-04) |
| Bibliographic style consistent (APA-7 / APSA) | PASS |

**Binary pass rate: 7 PASS / 6 PARTIAL / 7 FAIL = 37 %** — the paper is ~40 % of the way to a journal's structural readiness bar. All FAILs are fixable in under 2 hours of cleanup work except S10-01 (pre-registration filing) and S6-01/S6-02 (replace fabricated citations).

---

## Recommended citations to ADD (consolidated list)

To bring prior-art engagement to peer-review-ready state, add the following to the References section:

**Before submission (CRITICAL / HIGH):**
1. Replace Pal (2015) line with a verified Pal paper — candidate: Pal, M. (2016). "Fair Representation in the House of Commons?" SSRN 2705498; or Pal, M. (2017). "Canadian Electoral Boundaries and the Courts". *McGill Law Journal*.
2. Replace Pal (2019) line — candidate: Pal, M. (2016). "The Fractured Right to Vote". *McGill Law Journal* 62(1):171–212.
3. Altman, M., & McDonald, M. P. (2011). BARD: Better Automated Redistricting. *Journal of Statistical Software*, 42(4). https://doi.org/10.18637/jss.v042.i04
4. Magleby, D. B., & Mosesson, D. B. (2018). A New Approach for Developing Neutral Redistricting Plans. *Political Analysis*, 26(2), 147–167. https://doi.org/10.1017/pan.2017.43 — **and** re-source the 22 % statistic (Warrington 2019 is the likely true source)
5. Pildes, R. H. (2017). "Political Fragmentation in Democracies of the West". *Journal of Political Philosophy*. OR the Pildes / Persily efficiency-gap critique literature 2017–18. (To accompany the EG threshold in §3.2/§3.3.)
6. Tam Cho, W. K., & Liu, Y. Y. (2018). A massively parallel evolutionary Markov chain Monte Carlo algorithm for sampling contiguous redistricting plans. *Operations Research Letters*, 46(3), 285–290.
7. Engage Courtney (2001) directly in §5.3 (comparator cases); add page references.

**For scholarly completeness (MED):**
8. Wasserstein, R. L., & Lazar, N. A. (2016). The ASA's statement on p-values: Context, process, and purpose. *The American Statistician*, 70(2), 129–133.
9. Wasserstein, R. L., Schirm, A. L., & Lazar, N. A. (2019). Moving to a world beyond "p < 0.05". *The American Statistician*, 73(S1), 1–19.
10. Nosek, B. A., et al. (2018). The preregistration revolution. *PNAS*, 115(11), 2600–2606.
11. Munafò, M. R., et al. (2017). A manifesto for reproducible science. *Nature Human Behaviour*, 1, 0021.
12. Driedger, E. A. (1983). *Construction of Statutes* (2nd ed.). Butterworths.
13. Becker, A., Duchin, M., Gold, D., & Hirsch, S. (2021). Computational Redistricting and the Voting Rights Act. *Election Law Journal*, 20(4).
14. Altman, M., McDonald, M. P., & Stout, M. A. (2017). A public transparency framework for the evaluation of election administration. *PS: Political Science & Politics*, 50(3), 805–811.
15. Fix Carty year to 2015 (not 2017) and engage in §5.3.
16. At least one Alberta-political-science source on the 2025–26 cycle (Bratt, Thomas, Young, or Sayers).

**Already in References but engage / cite more directly:**
17. DeFord, Duchin, Solomon (2021) — cite in §3.11 body.
18. Fifield, Imai, Kawahara, Kenny (2020) — cite in §3.11 body.
19. Herschlag, Ravier, Mattingly (2020) — cite in §3.11 body.

---

## Appendix: verification methodology

1. **S6 citation verification.** For each cited author-year in the audit's References and in-text cites, WebSearch on `"<author>" "<year>" <key-topic-words> <venue>`. DOIs were fetched via WebFetch to confirm they resolve to the claimed paper. Two DOIs (Pal 2015 10.3138/utlj.2767 and Pal 2019 10.1017/cjlj.2019.16) returned HTTP 404 or resolved to a different paper — confirmed via Cambridge Core product identifier for the second.
2. **S7 data-quality reproduction.** Pandas / geopandas used to reproduce each headline count in `report_academic.md`:
   - `data/v0_1_alberta_2023_results.csv`: `pd.read_csv(...)`, assert shape == (87, 22), sum `total_valid_votes`.
   - `data/alberta_2021_da_populations.csv`: `pd.read_csv(dtype=str)` to preserve DAUID; coerce `population_2021` to numeric and assert sum == 4,262,635.
   - `data/alberta_2021_csd_populations.csv`: same; 423 rows, sum == 4,262,635.
   - `data/va_polygons_with_2023_votes.gpkg`: `gpd.read_file(...)`, 4,765 polygons, `va_ndp + va_ucp` sum = 896,644 vs reported 2023 two-party 1,706,304 — hence S7-01.
   - `data/submission_search_dataset.csv`: 71 rows, per-configuration mention counts reproduce `submission_search_findings.md` L11–L19 exactly.
   - `data/v0_1_338canada_per_riding_87seat.csv`: 87 rows, matches 2019 ED count (not 2026).
3. **S10 structural audit.** Walked `report_academic.md` section-by-section against a standard IMRaD + reproducibility + COI checklist for *Election Law Journal* / *Statistics and Public Policy* submission. Flagged every missing block against journal convention.

---

*Findings file. 2026-04-23. S6 / S7 / S10 science red-team pass per `analysis/v0_1_science_red_team_framework.md`. 30 findings: 2 CRITICAL, 8 HIGH, 15 MED, 5 LOW.*
