# Assertions red team — findings

**Audit date:** 2026-04-23
**Scope:** `report_public.md` and `report_academic.md` at repo root, checked against scripts in `analysis/`, data in `data/`, commission PDF in `.temp/commission_report.pdf`, and cited URLs.
**Method:** Every numeric claim, every named-speaker direct quote, and every statute-section reference was reproduced from its declared source (script, data file, URL, PDF page). Where the primary source was inaccessible (Hansard 403, paywalled), claims are marked "needs manual verification." This file documents findings; it does not propose edits to the reports.

---

## Executive summary

- **CRITICAL:** 3 (claims that are factually wrong by the audit's own internal sources)
- **HIGH:** 5 (claims overstated relative to evidence or internally inconsistent)
- **MEDIUM:** 7 (technically correct but misleading / partial)
- **LOW:** 4 (phrasing / style / punctuation)
- **INFO:** 5 (observations that do not rise to findings)
- **Total flagged claims:** 24
- **Needs manual verification:** 3 (Hansard-sourced and X-post quotes)

Overall posture: the two reports are substantially reproducible from the checked-in pipeline. The structural findings (MAD, Calgary zone gap, Airdrie 4-way, RMH-Banff extension) hold exactly as stated when the scripts are rerun. The issues are concentrated in three areas: (a) the §3.4 sensitivity-table values in `report_academic.md` do not match the script's current output at two of three weight points; (b) `report_public.md` still attributes "+0.7 of a seat" to the RMH-Banff §15(2) invocation after that attribution was retracted in `analysis/methodology/v0_1_s15_2_reaudit.md` §5.3; (c) direct-quotation wording is imprecise in several places (Nenshi quote stitched from two places in the source; Notley paraphrase presented as a direct quote).

---

## Critical findings

### CRIT-01. Academic §3.4 sensitivity table disagrees with its own script on 2 of 3 rows
**Claim (verbatim):** "| 0.60 | +1.58% | +0.22% | **−1.36 pp** | / | 0.70 | −0.85% | −1.36% | −0.51 pp | / | 0.80 | −1.43% | −3.04% | **−1.61 pp** |" — `report_academic.md` lines 253–255
**Stated values:**
- 0.60 urban-weight: Majority EG +1.58%, Asymmetry −1.36 pp
- 0.80 urban-weight: Majority EG −1.43%, Asymmetry −1.61 pp

**Verified values (from `PYTHONIOENCODING=utf-8 python analysis/scripts/v0_2_packing_cracking_analysis.py` run on 2026-04-23):**
- 0.60: Majority EG **+1.53%**, Minority EG +0.22%, Asymmetry **−1.31 pp**
- 0.70: Majority EG −0.85%, Minority EG −1.36%, Asymmetry −0.51 pp (matches)
- 0.80: Majority EG **−1.52%**, Minority EG −3.04%, Asymmetry **−1.52 pp**

**Source of truth:** `v0_2_packing_cracking_analysis.py` lines 573–586 (the `for w in [0.60, 0.70, 0.80]:` sensitivity loop).
**Delta:** +0.05 pp on the 0.60 Majority EG; +0.09 pp on the 0.80 Majority EG. Both rows' asymmetry columns drift correspondingly.
**Downstream impact:** The §3.3 headline "Magnitude ranges from 0.58 to 1.61 percentage points" is derived from the overstated table. Using the script's actual output, the range is 0.51 to 1.52 pp. The §7 row "§B2 sensitivity range (urban weights 0.60–0.80)" table also carries the stale numbers ("[+1.58% to −1.43%]" vs actual [+1.53% to −1.52%]).
**Recommendation:** Rerun the sensitivity loop and update Table 3.4, §7, and the text "0.58 to 1.61 percentage points" to match the script.

### CRIT-02. `report_public.md` still attributes "+0.7 of a seat" to RMH-Banff Park after the internal re-audit retracted the attribution
**Claim (verbatim):** "The extra rural seat at Rocky Mountain House-Banff Park accounts for roughly 0.7 of the one-to-three-seat gap between the two maps." — `report_public.md` line 140
**Stated value:** +0.7 seat attributable to the RMH-Banff §15(2) invocation.
**Source of truth:** `analysis/methodology/v0_1_s15_2_reaudit.md` §5.3, which concludes: *"The +0.7 seat attribution collapses. The rural-seat gap must be re-attributed to other features of the two maps (e.g., Canmore-Banff adding a rural seat the minority does not create, Lesser Slave Lake's specific boundary, or — more likely — the minority's rest-of-province mean being 3.9% lower than the majority's via other EDs)."* The re-audit is explicit that the engineered-boundary-qualification theory that underwrote the attribution is factually wrong (RMH-Banff passes 4/5 §15(2) criteria without the NP extension; the extension is not load-bearing).
**Delta:** The public report retains a number the internal audit says it must drop. The §3.10 academic signatures summary was revised to show RMH-Banff as "retracted under corrected §15(2) thresholds" in §5.2 of the re-audit, but the public report's seat-attribution line was not carried forward.
**Recommendation:** Either delete the "+0.7" line from `report_public.md`, or reframe as "the rest-of-province average population gap (3.9%) accounts for most of the 1–3 seat gap between the two maps." Noting: `report_public.md` lines 136–138 already reflect the re-audit qualitatively — they acknowledge the test "was tempting to retract" — but the numeric attribution two lines later is stale.

### CRIT-03. The "materially wrong on three of them" framing in `report_public.md` misrepresents the scope
**Claim (verbatim):** "the chair's own claim that five minority configurations had 'no public support' turned out to be materially wrong on three of them" — `report_public.md` line 25
**Stated value:** 3 of 5 Miller-named configurations were materially wrong.
**Source of truth:** `analysis/reports/submission_search_findings.md` and `analysis/reports/v0_1_claim_significance_analysis.md` identify three configurations as "precisely and effectively wrong": Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, and Chestermere. Miller's Appendix C-quoted list in the same documents is: **Airdrie, Cochrane, Chestermere, Red Deer, St. Albert**. Of those five, only Chestermere appears on the "materially wrong" list. RMH-Banff and Olds-ODH were not among Miller's original five — the audit added them as extensions to test.
**Delta:** The public report's intro promises "three of five" but the support refutation actually hits one of Miller's five (Chestermere) plus two configurations Miller did not specifically disavow in Appendix C. The in-body Table 2 (line 147–154) lists all seven correctly, but the intro's phrasing inflates the hit rate against what Miller specifically claimed.
**Recommendation:** Tighten the intro to "the chair's own claim that five minority configurations had no public support turned out to be materially wrong on Chestermere, and his broader 'no public support' framing mischaracterized the record on two additional configurations the minority adopted from the submissions." Or equivalent.

---

## High findings

### HIGH-01. 2019 cross-election asymmetry: academic preamble says +0.60 pp, §3.5 and script say +0.75 pp
**Claim (verbatim):** "Running identical methodology with 2019 vote totals (instead of 2023) produces Majority EG +0.30%, Minority EG +0.90%, asymmetry **+0.60 pp**" — `report_academic.md` line 72 (stress-test preamble)
**Stated values:** Majority +0.30%, Asymmetry +0.60 pp
**Verified values (from `python analysis/scripts/v0_3_monte_carlo_ci.py` cross-election cross-check and `python analysis/scripts/2015_cross_election.py`):**
- Majority 2026 under 2019 votes: EG **+0.16%** (v0_3) / +0.16% (v0_1_2015 script)
- Minority 2026 under 2019 votes: EG +0.90%
- Asymmetry **+0.75 pp** (reported identically in `report_academic.md` §3.5 line 263)
**Delta:** 0.14 pp on the Majority EG; 0.15 pp on the asymmetry.
**Recommendation:** Reconcile the preamble with §3.5 and the script — the preamble is stale.

### HIGH-02. Monte Carlo median asymmetry: academic says −1.44, script says −1.40
**Claim (verbatim):** "Minority-majority EG asymmetry: mean −1.22 pp, median **−1.44 pp**, **95% CI [−3.04, +0.76] pp**. Direction consistency: 90.5% of samples" — `report_academic.md` lines 68
**Stated value:** Mean −1.22, median −1.44
**Verified values (from `python analysis/scripts/v0_3_monte_carlo_ci.py` run, seed=42 N=2000):**
- Mean: **−1.233** (rounds to −1.23, not −1.22)
- Median: **−1.401** (rounds to −1.40, not −1.44)
- 95% CI: [−3.038, +0.764] (matches academic's [−3.04, +0.76])
- Direction consistency: **90.5%** (matches)
**Source of truth:** Full script output at /analysis/scripts/v0_3_monte_carlo_ci.py with hard-coded seed=42, n_samples=2000 in the `run_monte_carlo()` function (line 94).
**Delta:** Median off by 0.04 pp; mean off by 0.01 pp.
**Recommendation:** Update the preamble from "−1.22 pp" / "−1.44 pp" to "−1.23 pp" / "−1.40 pp". The 95% CI and the 90.5% directional consistency are already correct.

### HIGH-03. "1,345 submissions" in public report differs from every internal source ("~1,340" / "approximately 1,340")
**Claim (verbatim):** "The commission took 1,345 written submissions across two rounds of hearings. I was able to keyword-search 1,252 of them." — `report_public.md` line 144
**Stated value:** 1,345
**Verified value:**
- `analysis/reports/submission_search_findings.md` line 3: "~1,340 public submissions"
- `analysis/reports/submission_search_findings.md` line 7: "1,252 of ~1,340 (93.4%)"
- `report_academic.md` line 538: "approximately 1,340"
**Source of truth:** No source in the repo gives 1,345; every internal reference uses "~1,340" or "approximately 1,340."
**Recommendation:** Change "1,345" to "approximately 1,340" in `report_public.md` to match the academic report and the submission search findings, or cite the specific source if 1,345 is the actual commission-reported count.

### HIGH-04. Jared Wesley "chaired the 2018 Edmonton commission" — wrong year, unclear which commission
**Claim (verbatim):** "Jared Wesley, the University of Alberta political scientist who chaired the 2018 Edmonton commission, said any casual observer could see it for what it was." — `report_public.md` line 19
**Stated value:** 2018 Edmonton commission, Wesley as chair.
**Verified value:** Per https://jaredwesley.ca/service and https://www.edmonton.ca/city_government/city_organization/ward-boundary-commission, Wesley chaired the **Edmonton Ward Boundary Commission**, established by City of Edmonton Bylaw 18893 in **June 2019**, with its Final Report published in **May 2020**. The commission was never titled "Edmonton commission" and never operated in 2018. It redrew **municipal** ward boundaries, not provincial electoral boundaries.
**Delta:** Year is off by 1 year (2018 → 2019 for establishment, 2020 for report); the body is misidentified by generic name ("Edmonton commission" is ambiguous — readers may think Wesley chaired the provincial Alberta Electoral Boundaries Commission, which he did not).
**Recommendation:** Correct to "Jared Wesley, the University of Alberta political scientist who chaired Edmonton's 2019–2020 Ward Boundary Commission..." or similar. Note that Wesley's expertise in municipal-level boundary commissions supports his quoted opinion on provincial boundary practice, but the factual attribution as written is inaccurate.

### HIGH-05. The Nenshi quote in `report_public.md` line 17 is stitched from two separated parts of the source interview
**Claim (verbatim):** "'Let's be clear,' he said. 'Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and, in fact, not adopting the report is a full-on assault on our democracy.'" — `report_public.md` line 17
**Stated value:** Presented as a single continuous Nenshi utterance.
**Verified value (from WebFetch of https://www.discoverairdrie.com/articles/alberta-introduces-motion-to-review-electoral-boundaries-as-parties-dispute-commission-findings, retrieved 2026-04-23):**
- The clause "Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and in fact not adopting the report is a full-on assault on our democracy" **is verbatim** in the source article.
- The phrase "Let's be clear" **also appears** in the source article attributed to Nenshi, but in a different paragraph discussing the procedural provenance of Recommendation 5 (context: "To set the record straight, that is incorrect. The commission report had one recommendation from the majority..."). The two passages are not adjacent in the source.
- The "Let's be clear" in the source precedes the "To set the record straight..." sentence, not the "cheating/gerrymandering/full-on assault" sentence.
**Delta:** The "Let's be clear" and the cheating/gerrymandering passages are both genuine Nenshi quotes, but the two are stitched together in the report in a way that does not match the source's flow. Minor punctuation ("and in fact" vs "and, in fact,") also reads as a direct quote.
**Recommendation:** Either replace "Let's be clear" with ellipsis-cued stitching ("…Not adopting the commission's report is cheating…"), or drop the "Let's be clear" prefix. Alternatively, cite the Hansard record if available rather than the DiscoverAirdrie paraphrase.

---

## Medium findings

### MED-01. Notley "never even casually considered abusing my power" — paraphrase presented as a direct quote
**Claim (verbatim):** "wrote in a Globe op-ed a few days later that she 'never even casually considered abusing my power.'" — `report_public.md` line 19
**Verified value (from WebFetch of https://www.theglobeandmail.com/opinion/article-possible-changes-to-alberta-electoral-map-put-democracy-at-risk/, retrieved 2026-04-23):** The actual sentence in the op-ed is: *"at no time did I even casually consider abusing my power as Premier or our legislative majority to reverse the work of the boundaries commission."*
**Delta:** The semantic meaning is the same, but the quotation marks in the report imply word-for-word reproduction of "never even casually considered." The source says "at no time did I even casually consider." The transposition ("never" for "at no time") is minor but falls outside the convention for direct quotation.
**Recommendation:** Change to indirect phrasing ("wrote that she had at no time even casually considered abusing her power") or use the verbatim clause.

### MED-02. "I've been asking every member to look at page 66 of the report and the judge's addendum to the majority report" — no accessible source in repo or web
**Claim (verbatim):** "'I've been asking every member to look at page 66 of the report and the judge's addendum to the majority report,' she said." — `report_public.md` line 39
**Verified source:** Attempted fetches of multiple April 17, 2026 articles about Smith's Question Period remarks. Parliamentum.org (2026-04-21) and albertacounselnews.com both paraphrase Smith but do not reproduce the "I've been asking every member..." verbatim line. The Alberta Hansard direct-transcript site returned 403 on attempted WebFetch per `analysis/methodology/v0_1_minority_rationales_inventory.md` line 276. The public report cites "Premier Smith's April 17 legislature statement" in its "source trail" (line 348) without a URL anchor.
**Delta:** The quote is plausible and consistent with every paraphrased summary of Smith's Question Period statements, but I cannot reproduce the exact words from any accessible source.
**Recommendation:** Mark as "needs manual verification" against Hansard for April 17, 2026 Day 17 sitting; supply a URL if Hansard is indexed and accessible.

### MED-03. Greg Clark "In Canada, we don't want elected officials drawing their own election maps" — not verified from X
**Claim (verbatim):** "Commissioner Greg Clark, one of the two opposition-nominated majority members — Clark had been nominated by NDP leader Naheed Nenshi — posted on X after the report dropped. 'In Canada,' he wrote, 'we don't want elected officials drawing their own election maps.'" — `report_public.md` line 230
**Verified source:** `analysis/reports/v0_1_chair_recommendation_5_analysis.md` line 48 acknowledges: *"Commissioner Greg Clark, one of the two opposition-nominated majority commissioners... posted a thread on X / social media after the final report's tabling in April 2026 clarifying that the 91-seat call came from the chair alone, not from the majority commissioners. Clark's thread was referenced by multiple outlets (rabble.ca, albertapolitics.substack.com). **Full citation pending direct archival retrieval** at @GregClarkAB; the substance is already established by Miller's own in-text admission above."*
**Delta:** The direction of Clark's view is internally corroborated (Miller's own text in the PDF disavows majority endorsement of R5). The specific "In Canada, we don't want..." wording is not archival-verified in the repo.
**Recommendation:** Mark as "needs manual verification" against the X thread (Wayback capture or direct archive URL).

### MED-04. "five Indian reserves are inside it — Big Horn 144A, O'Chiese, three Stoney reserves, Sunchild"
**Claim (verbatim):** "Five named Indian reserves are inside it — Big Horn 144A, O'Chiese, three Stoney reserves, Sunchild." — `report_public.md` line 126
**Verified source:** `analysis/methodology/v0_1_s15_2_reaudit.md` §3.4 and commission PDF p. 352 list the reserves as: "Big Horn No. 144A, O'Chiese No. 203, Stoney nos. 142, 143, 144, Stoney No. 142B and Sunchild No. 202" — that is **four** Stoney reserves (142, 143, 144, plus 142B), not three.
**Delta:** The public report says "three Stoney reserves"; the commission and the re-audit both enumerate four. Counting five distinct named reserves (Big Horn, O'Chiese, 142-143-144 as a block, 142B, Sunchild) yields five if 142/143/144 are grouped as "the three numbered Stoney" plus 142B. But the commission's list as written distinguishes "Stoney nos. 142, 143, 144" and "Stoney No. 142B" as separate entries.
**Recommendation:** Either "four Stoney reserves" or "the numbered Stoney Nakoda reserves" would be accurate.

### MED-05. Academic Abstract and §7 claim "directional consistency across six independent dimensions" while §Stress-Test Preamble qualifies it as 5 of 6
**Claim (verbatim):** Abstract line 92: "The directional consistency of the minority's shift across six independent analytical dimensions..." and §7 line 746: "Six independent dimensions of evidence point in the same direction." vs Stress-Test Preamble line 85: "**'Directionally consistent across six dimensions' is more precisely 'directionally consistent across five of six tested dimensions, with one partisan-bias metric (declination) pointing the opposite way.'**"
**Verified source:** The declination result (−0.034 / −0.021 / −0.015 for 2019/Majority/Minority) has the minority-to-majority magnitude decreasing (Minority declination is **closer to zero** than Majority), so by declination the minority looks less UCP-biased, not more. Script confirms this (see §3.4 of academic paper).
**Delta:** The Abstract and §7 row do not surface the declination inversion; the stress-test preamble does. Some readers will see the Abstract's "six independent dimensions" without reading far enough to hit the 5-of-6 qualifier.
**Recommendation:** Amend the Abstract to "across five of six independent analytical dimensions (with declination pointing opposite)" or move the qualifier up-front.

### MED-06. Submission-table numbers in `report_public.md` line 147–154 do not match the audit's own per-configuration counts
**Claim (verbatim):** Table 2 in `report_public.md`:
| Configuration | Public submissions |
| --- | --- |
| Rocky Mountain House-Banff Park | 5 support, 1 oppose |
| Olds-Three Hills-Didsbury rural unit | 3 support, 1 oppose |
| Chestermere as its own unit | 3 support, 1 oppose |
| Red Deer hybrids | 4 support, 4 oppose, 15 neutral |

**Verified value (from `analysis/reports/submission_search_findings.md` and `report_academic.md` §5.4.1):**
- RMH-Banff Park: **3 explicit supporters + ≥4 aligned = 7 total leaning-support**, 1 oppose, ~15 neutral (20 total mentions)
- ODH: **2 supporters**, 2 opposers, 1 neutral (5 total mentions)
- Chestermere: 3 supporters, **3 opposers** (not 1), 7 neutral (13 total)
- Red Deer: **2 explicit + 3 aligned = 5**, 4 oppose, 17 neutral (23 total — not 4+4+15=23 as the public table suggests)
**Delta:**
- RMH: public "5 support" does not match "3 explicit / 7 with aligned"; the 5 may be a split between these numbers.
- ODH: public "3 support" vs findings "2 support"; public "1 oppose" vs findings "2 oppose."
- Chestermere: public "1 oppose" vs findings "3 oppose."
- Red Deer: public "4 support" vs findings "2 explicit, or 5 with aligned."
**Recommendation:** Reconcile the public-report table to match either `submission_search_findings.md` or `report_academic.md` §5.4.1; currently it disagrees with both. If the public-report numbers derive from a separate manual re-tag that superseded the CSV, that document should be named in the footnote.

### MED-07. "four of five criteria pass without the park" in `report_public.md` line 126 — audit says (b) is "qualified" pass
**Claim (verbatim):** "Four of the Act's five criteria pass without the park." — `report_public.md` line 126
**Verified source:** `analysis/methodology/v0_1_s15_2_reaudit.md` §3.5 counterfactual: 4/5 pass without NP extension, but criterion (b) is qualified with: *"Rimbey ~143 km from Edmonton (Wikipedia); Rocky Mountain House ~215 km (rome2rio, ViaMichelin). On a 'nearest boundary' conservative reading this is borderline."* §7 open question 1 reiterates: "Criterion (b) for RMH-Banff Park is borderline. Rimbey sits at ~143 km from the Edmonton Legislature by road; the NE corner of Clearwater County may be marginally closer to 150 km."
**Delta:** The 4/5 pass claim depends on (b) being credited; the internal re-audit flags (b) as "qualified pass" and notes that under a strict reading (b) may fail, in which case without the NP extension the district passes only 3/5. The 3/5 still clears the statutory threshold, but the public report's "four of five" is the upper-bound reading, not the conservative one.
**Recommendation:** Soften to "four of the Act's five criteria pass without the park (three cleanly, one borderline)" to match the re-audit's own qualifier.

---

## Low findings

### LOW-01. "1,345 submissions" vs "~1,340" — minor figure drift (covered in HIGH-03)

### LOW-02. "and in fact" vs "and, in fact," comma insertion in the Nenshi quote
**Claim (verbatim):** Direct quotation inserts two commas not present in the DiscoverAirdrie source ("and in fact" → "and, in fact,"). — `report_public.md` line 17
**Recommendation:** Preserve source punctuation inside direct quotation marks.

### LOW-03. Metis settlement spelling — statute uses "Metis" without accent; audit text sometimes uses "Métis"
**Claim (verbatim):** `report_public.md` line 57 uses "Métis settlements" (with accent); the statute text quoted verbatim in `analysis/methodology/v0_1_s15_2_reaudit.md` §1 uses "Metis settlement" (no accent).
**Delta:** Stylistic. Both are accepted. Match source if quoting verbatim.

### LOW-04. Seven reserves in RMH enumerated as "five named" — covered in MED-04

---

## Info-level observations

### INFO-01. 2015 cross-election +0.03 pp asymmetry is not headlined
Script output confirms 2015 EG asymmetry is +0.03 pp (essentially zero). This is reported in academic §3.5 but is not in the Abstract or §7 six-dimensions table.

### INFO-02. Three comparator cases (Quebec 1992, Ontario 1996, BC 2008) are internally documented but without academic citation
`analysis/methodology/v0_1_academic_literature_review.md` line 38 acknowledges: "Comparator cases: Quebec 1992, Ontario 1996, BC 2008. — cited but without academic sources backing the comparisons." `analysis/reports/v0_1_bias_audit.md` line 125–127 acknowledges the uniqueness framing is overbroad and recommends softening. The claim "None of the three dissolved the commission mid-cycle and installed a legislative committee in its place" (`report_public.md` line 35) is internally supported by the `v0_1_section_D_procedural.md` comparators but could use a cited academic source.

### INFO-03. "1.5-point swing" as "the middle of the map-effect estimate" (public report line 270)
The Monte Carlo mean is −1.23 pp; the median is −1.40 pp; the sensitivity range is 0.51 to 1.52 pp. 1.5 pp is at the upper end of the range, not the middle (which is closer to 1.0 pp). "Midpoint of 1.0 to 1.5" would be technically more accurate; "middle of the estimate" reads like a point-estimate midpoint.

### INFO-04. Siksika Nation / High River-Vulcan-Siksika claim
`report_academic.md` §4.4 table shows "Siksika Nation | High River-Vulcan-Siksika | High River-Vulcan-Siksika (same)." The academic check is internally consistent; this is not a finding but a data point.

### INFO-05. Script output discrepancy for the 0.60 row is small but non-trivial because the public report doesn't repeat these numbers
The 0.05 pp drift at 0.60 and 0.09 pp at 0.80 (CRIT-01) only appears in the academic report. The public-report magnitude claim "one-fifth of the seven-percent threshold" is stated on the 0.70 central value (−1.36% is 19% of 7%), which is correct under either the old or current script output.

---

## Needs manual verification

### NM-01. Premier Smith's April 17 "page 66" verbatim quote
**Location:** `report_public.md` line 39
**Claim:** "'I've been asking every member to look at page 66 of the report and the judge's addendum to the majority report,' she said."
**Procedure:** Pull Alberta Hansard for 2026-04-17, Day 17 of the First Session of the 31st Legislature, Premier's Question Period exchange. Check the committee-sitting stenograph for verbatim reproduction. Secondary-source paraphrases corroborate the substance (page 66 reference) but not the exact words.

### NM-02. Greg Clark X-thread exact wording
**Location:** `report_public.md` line 230
**Claim:** "'In Canada,' he wrote, 'we don't want elected officials drawing their own election maps.'"
**Procedure:** Wayback Machine capture of @GregClarkAB for the April 2026 thread, or direct retrieval from X (Twitter) using an authenticated client. The substance is corroborated by Miller's in-text disavowal of majority endorsement of R5 (`.temp/commission_report.pdf` p. 66), so the general point holds. The verbatim words are archival-unverified.

### NM-03. DiscoverAirdrie article durability
**Location:** All Nenshi and Pancholi quotes in `report_public.md`
**Claim:** DiscoverAirdrie April 17, 2026 article is the source. A Wayback-captured snapshot would close the citation durability gap.
**Procedure:** Submit the DiscoverAirdrie URL to web.archive.org/save/; add the snapshot URL to the bibliography / FROZEN_MANIFEST.

---

## What I verified and is correct

- Monte Carlo parameters (seed=42, N=2,000, urban-weight 0.55–0.85, rural baseline 0.26–0.36, jitter ±0.10) — verified from `analysis/scripts/v0_3_monte_carlo_ci.py` lines 11–17, 94.
- 90.5% directional consistency — reproduced exactly from script.
- 95% CI [−3.04, +0.76] pp — reproduced exactly from script.
- Calgary Zone A mean 61,225 / Zone B mean 54,569 / gap +12.20% under the minority — `analysis/scripts/electoral_forensics_population.py` output.
- Calgary Zone gap under the majority (+0.36%) — `electoral_forensics_population.py` output.
- A1 MAD: Majority 3,180 / Minority 4,707 — `electoral_forensics_population.py`.
- 113,000 voters excess ≈ 17 × (61,225 − 54,569) = 113,152, matches public-report rounding.
- Efficiency gaps: 2019 −2.64%, Majority −0.85%, Minority −1.36% — `v0_2_packing_cracking_analysis.py` at urban weight 0.70.
- Declination: 2019 −0.0341, Majority −0.0210, Minority −0.0150 — `v0_2_packing_cracking_analysis.py`.
- NDP seats @ 50/50: 2019 46, Majority 44, Minority 42 — `v0_2_packing_cracking_analysis.py`.
- Mean-median gap: 2019 −2.22 pp, Majority −0.18 pp, Minority −0.33 pp — `v0_2_packing_cracking_analysis.py`. (Academic report §3.3 shows Majority −0.16 pp, which is a minor rounding drift to note but within one-digit precision.)
- 2023 outcome UCP 49 / NDP 38 — Statement of Vote.
- 338Canada April 2026 snapshot: UCP 63 / NDP 24 — `data/v0_1_338canada_historical_snapshots.csv` row 2026-04-12.
- Airdrie 2021 population 74,100; 2025 municipal census 90,044 — consistent across all audit references, StatCan CY census tables.
- Red Deer 2021 population 100,844 — StatCan Census table, CSD 4808011.
- RMH-Banff Park population 38,298 (−30.3% variance) — Minority report p. 358, reproduced in `data/v0_1_minority_2026_populations.csv`.
- Provincial total 4,888,723 — Majority/Minority report tables, equals StatsCan Q2 2024 postcensal estimate for Alberta.
- Commission tabled March 23, 2026 — verified across multiple internal docs.
- April 16 motion passed 44–36, Brandon Lunty (Leduc-Beaumont) chair, November 2, 2026 deadline — verified from CBC and DiscoverAirdrie.
- Nenshi quote clauses "cheating / gerrymandering / full-on assault on our democracy" — verbatim in DiscoverAirdrie source.
- Miller's Addendum text on p. 66, including "My majority colleagues do not agree with me on this point" and "This fifth recommendation is formulated for the express purpose of dissuading the Legislature from accepting the minority report" — verified from commission PDF p. 66 via pdfplumber.
- "historical precedent of portions of Banff National Park" on p. 352 — verified from commission PDF p. 352.
- Clearwater County area 18,692 km² — Wikipedia, matches audit claim.
- Rocky Mountain House town 6,765 (2021 census) and Canmore 15,990 / Banff 8,305 — StatCan profiles.
- 12 of 14 marginal 2023 ridings are in Calgary — verified from `marginal_seats_analysis.py` output (Calgary-Acadia, -Glenmore, -North West, -North, -Foothills, -Edgemont, -Bow, -Beddington, -Elbow, -Cross, -Klein, -East = 12 Calgary + Banff-Kananaskis + Lethbridge-East = 14).
- Calgary-Acadia 0.05 pp margin in 2023 and Calgary-North West UCP 0.30 pp — verified.
- 1.5 pp UCP-swing flips 6 (5 Calgary + Banff-Kananaskis); 1.5 pp NDP-swing flips 4 (Calgary-Bow, Calgary-North, Calgary-North West, Lethbridge-East) — verified.
- RMH-Banff Park §15(2) re-audit: 5/5 as drawn, 4/5 without NP extension; Canmore-Banff 3/5 under corrected thresholds — verified from `v0_1_s15_2_reaudit.md` against commission PDF pages 212, 236, 248, 341, 345, 352.
- Shared-schools claims (Rocky View Schools vs CBE for Bow-Springbank; Chinook's Edge vs Red Deer Public for Red Deer-Sylvan Lake) — verified against Alberta Education school-division boundaries.
- Three intro-promised counterexamples are surfaced: (i) majority's Canmore-Banff flips FAIL→PASS under corrected thresholds (verified); (ii) 2019-vote direction reversal (verified at +0.75 pp, modulo the stale preamble figure); (iii) chair's "no public support" materially wrong on Chestermere + two added configurations (verified, modulo the CRIT-03 scope reframing).

---

## Methodology notes

- All scripts run with `PYTHONIOENCODING=utf-8` on Python 3.14 (Windows).
- PDF text extraction via `pdfplumber`. Page indexing is 0-based in the Python API; report citations are 1-based (p. 66 = `pages[65]`).
- Webfetches on 2026-04-23; URLs preserved in `FROZEN_MANIFEST.md` where present. Hansard direct access blocked (403); secondary-source paraphrase carried forward.
- No edits were made to either report. All findings are documented for the next reviewer.
