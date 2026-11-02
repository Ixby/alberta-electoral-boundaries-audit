> **Backward:**
> - `reports/academic/report_academic.md` — the monograph audited
> - `reports/academic/report_academic.pdf` — its committed print build
> - `reports/academic/data_supplement.md`, `analysis/methodology/plain_language_defense.md` — supporting documents audited
> - `analysis/scripts/build_academic_pdf.py` — PDF build audited
> - `analysis/review/swarm_audit_2026-10-29.md` — prior audit, used to avoid overlap
>
> **Forward:**
> - (leaf — review record; author decisions listed in §4)

# Monograph audit — structure, PDF, methodology and supporting documents

**Date:** 2026-10-29 21:50 MDT (Alberta time)
**Tree audited:** HEAD `231eb2fd` (clean working tree at start)
**Passes:** four. Structure and references, the PDF, methodology, and the supporting documents. A separate verifier re-checked every finding.

Line numbers below are at HEAD `231eb2fd`, before this pass's edits. In `report_academic.md` they still hold: the two new anchors sit on lines that were blank, and the line count is unchanged. Two reference entries moved within their lists. In `data_supplement.md`, HEAD lines 78–261 are now one line lower, and lines from 262 on are two lower. In `plain_language_defense.md`, HEAD lines from 1587 on are now four lines higher, because the end marker moved to the end of the file.

---

## 1. Summary counts

| | Count |
|---|---|
| Findings raised | **122** (structure 34, PDF 20, methodology 24, supporting 44) |
| Upheld by the verifier | **120** (109 confirmed, 7 likely, 4 open questions) |
| Rejected by the verifier | **2** (PDF-07, MC-C5) |
| Upheld, by severity | 15 high, 52 medium, 53 low |
| Eligible to apply (confirmed, mechanical, upheld) | 53 |
| Applied | **41** (34 in full, 7 in part) |
| Eligible but not applied | 12 (3 are code changes; 9 would change a number or a stated finding) |
| Author decisions | **26** (23 methodology items, plus 3 open questions) |

Several findings were raised twice, by two passes: S1 and PDF-03, S2 and PDF-04, S5 and PDF-08, S10–S12 and PDF-09, S12/S20 and PDF-10, S28 and PDF-01, S30 and DS-08, S31 and DS-10. Each pair is listed once below.

**The most important open items.**
1. The ensemble plans all have 87 districts. The monograph gets the cross-size caveat backwards, and its seats@50/50 "ceiling" claim compares 46/89 against an 87-seat lattice (MC-A1, MC-A5).
2. "Population MAD" names two different statistics. The ensemble MAD flag holds only under the ±12.5% proposal band (MC-C1, MC-C4).
3. The committed PDF is a June 27 build. It still prints Motion 19, five MLAs, Cassista and superseded p-values (S28, PDF-01).
4. The plain-language defense says no AI produced any number. The monograph reports LLM-classified counts (PLD-01).
5. The "Actual seats" row mixes the real 2023 result with election-day-substrate counts (MC-B1).

**Files edited (working tree only; nothing committed):**
- `reports/academic/report_academic.md`
- `reports/academic/data_supplement.md`
- `analysis/methodology/plain_language_defense.md`
- `analysis/review/monograph_audit_2026-10-30.md` (this file, new)

---

## 2. Findings that survived verification

Each entry gives the ID, severity, location, what is wrong, which pass found it, the fix, and whether the fix was applied. "Held" means the fix is mechanical but would change a number or a stated finding, so it waits for the author. "Not applied" means the fix needs judgment or touches code or the PDF.

### 2.1 High

- **MC-A1** · `report_academic.md:1722` · methodology. The cross-size declination caveat has the sizes backwards. All 1,010,000 canonical plans have 87 districts, seeded from the 2019 map's count. So the 2019 map is the same-size comparison, and both 2026 maps are cross-size. The ln(87)/ln(89) bound still holds for δ. The PDF has the same text. Fix: rewrite the caveat. **Not applied: author decision A1.**
- **MC-A5** · `report_academic.md:1593` (also 1579, 1584, 1691, 2550, 2589; BH row 3 at 532) · methodology. Seats@50/50 is compared across two lattices. The 87-district ensemble can only produce k/87. The minority's 46/89 = 51.69% sits just below the ensemble's 45/87 = 51.72% maximum, and all 69 "reaching" plans exceed it. "The DPG-era ceiling figures above therefore survive" does not hold. Fix: see decision A5. **Not applied: author decision A5.**
- **MC-B1** · `report_academic.md:829` (also `findings/partisan_bias_summary.md:220`) · methodology. The "Actual seats" row puts the real 2023 result (38/49) in the 2019 column, and election-day-substrate counts in the 2026 columns. On the same substrate, 2019 gives NDP 30 / UCP 57. As labelled, the row overstates the UCP gain under both 2026 maps. **Not applied: author decision B1.**
- **MC-C1** · `report_academic.md:1658` (also 54, 254, 538, 708, 1619, 1629, 1634, 1646, 1670, 2469, 2511, 3148; `data_supplement.md:201`) · methodology. Two statistics share the name "population MAD". The 3,180 / 4,707 headline is the mean absolute deviation from the 54,929 average, on the commission's tables. The ensemble channel (2,827 / 3,938) is the median absolute deviation from the median, on 2021 DA population. **Not applied: author decision C1.**
- **MC-C4** · `report_academic.md:1646` (also 538 row 9, 1658; `data_supplement.md:201`) · methodology. The ensemble MAD "fifth flag" exists only under the ±12.5% proposal band. Under the statute band (±25%) the minority sits at p0.013 and the majority at p0.0. Both are more equal than almost every neutral plan. **Not applied: author decision C4.**
- **S1** (duplicate: PDF-03) · `report_academic.md:2919` (also 2409, 2708, 2919–2955) · structure and PDF. All 38 relative links were written from the repo root. GitHub and the PDF resolve them from `reports/academic/`, so every one broke. Fix: prefix `../../`, after the S2 moves. **Applied.** All 38 now resolve from `reports/academic/`.
- **S28** (duplicate: PDF-01) · `reports/academic/report_academic.pdf` · structure and PDF. The committed PDF is a 2026-06-27 Windows build, 215 pages. The markdown has had 28 commits since. The PDF still prints Motion 19 and five MLAs, the Cassista citation, Ch1 p ≈ 1.40×10⁻⁶, "Median Absolute Deviation", ledger entries only to C7, and the old disclosure wording. Fix: rebuild after S1–S3 and the PDF-02/05/06/12 build fixes, or remove it. Stamp the source commit in the PDF. **Not applied** (the PDF and build code are out of scope). The markdown header now marks the PDF "not current; rebuild pending" (PDF-19).
- **PLD-01** · `plain_language_defense.md:37` (also 163) · supporting. Says no AI tool "produced any number that appears in the report". The monograph says two Claude pipelines classified submissions and Hansard turns (§5.9.4.6, :2140). Those counts are reported (:2147). A vision model screened the maps (:1859), and Codex did scripting (:108). The human IRR check has 0 of 60 labels filled. Fix: rewrite Quick Ref #5 and :161–163 to match the monograph, and say the IRR gate is pending. **Not applied** (rewrite needs judgment).
- **PLD-02** · `plain_language_defense.md:71` (also 892, 1528) · supporting. Says the majority is in the neutral band on every metric. Its mean-median is p0.99, and the same file says so at :844. Fix: "within the null on three of four metrics and jointly (p = 0.102); its mean-median is a p0.99 outlier leaning NDP." **Held** (changes a stated finding).
- **PLD-03** · `plain_language_defense.md:1000` (also 141, 1007, 1372) · supporting. Cites "Motion 19", "five MLAs", "Special Select Committee", and a governing-party-only committee. The monograph gives Government Motion 37 (introduced April 16, passed April 21), six MLAs (four UCP, two NDP), and "Select Special Committee". Fix text in the finding. **Held** (changes numbers).
- **PLD-04** · `plain_language_defense.md:984` (also 986, 990) · supporting. The PLD says the chair was "nominated by the Chief Justice", calls the interim report "unanimous", and says the government accepted the minority map. All three are wrong. The chair was appointed by the Lieutenant Governor in Council under s.2(1), and the interim report was tabled October 28, 2025. Unanimity is unverified. GM37 set both reports aside. **Not applied** (factual rewrite).
- **PLD-05** · `plain_language_defense.md:278` (also 526–528, 580–582, 1617–1619) · supporting. Repeats the retracted v0_8 "no flip" claim and blend-era asymmetries, and reads −0.51 in opposite directions at :528 and :1619. Fix: use the verifier's corrected text. Both maps' EGs turn NDP-favourable under 2019. The minority stays the more UCP-favourable map in every election tested (+2.96, +0.83, +3.92 pp). Do not write that the asymmetry reverses. **Not applied.** The same check found that the monograph's own "reverses under 2019" statements need reconciling (§1.2 item 3 :274, :291, :404, :654, RT3 :1843, :2723, :2902; PLD :25, :155).
- **PLD-06** · `plain_language_defense.md:25` (also 41, 107, 201–203, 360, 856, 862, 870–872, 1198, 1530) · supporting. Says every test was registered on OSF before the data were examined. §4.3.3 says Ch1 is exploratory, 6pt83 was filed about 3 h after the shapefile commit, and yvc7g and s58a6 post-date the shapefiles. Eight registrations exist, not five. **Not applied.**
- **PLD-07** · `plain_language_defense.md:426` (also 652–654, 862, 1250) · supporting. Presents SZAT p = 0.0024 with no caveat and gives it primary weight. SZAT is retired: block-permuted p ≈ 0.19, with 5.79× variance inflation. **Not applied.**

### 2.2 Medium

**Structure and references**
- **S2** (duplicate: PDF-04) · `report_academic.md:2931` (also 2409, 2932, 2938, 2941–2955) · 14 link targets were missing even from the repo root. Thirteen had moved; one (`pre_registration_draft.md`) was deleted. `historical/` no longer exists. **Applied** with the corrected fix. All 13 moved paths now point at their current locations. Line 2950 now links `preregistration/november_2026_scoring_spec.md`. Line 2941 now says the stress-test passes are in git history under `historical/` before `e4c32e89` (not `archive/`, which does not hold them).
- **S3** · `report_academic.md:226` (about 37 paths; also 72, 114, 229, 259, 289, 339, 346–352, 374, 382, 452, 587, 589, 656, 694, 846, 896, 898, 962, 1003, 1088, 1234, 1283, 1322, 1380, 1542, 1577, 1591, 1644, 1714, 1774, 1820, 1846, 1935, 1978–1980, 2039, 2129, 2252–2341, 2519, 2612, 2616, 2721, 2914, 2964, 2977, 2979, 3105) · Backticked paths still named pre-restructure locations. **Applied.** Each old path now names its current location, checked against `git ls-files`.
- **S4** · `report_academic.md:2909` (also 7, 118, 359, 546, 636, 820, 1140, 1322, 1326, 1402, 1466, 1499, 1542, 1555, 1566, 1615, 1617, 2607, 2611, 2612, 2616, 2956, 3091) · About 25 paths name files that are not in the repo. Several are cited as provenance for reported numbers. The Appendix A run line names a script that is gone. Fix: cite the corrected provenance (see the verifier's list in §3). Replace or drop the Appendix A run line. Drop or retarget the never-tracked files. **Not applied** (each needs a choice).
- **S5** (duplicate: PDF-08) · `report_academic.md:316` (also 67, 68, 326, 382, 394, 625, 627, 896, 1069, 1281, 1454, 1462, 2022, 2618, 3140) · 17 section numbers that belong to other documents or to the Charter were linked to the monograph's own anchors. **Applied.** The link markup is gone. Charter cites now read "s. 3". Line 896 names the "Three-map metrics under 2015 votes" table.
- **S6** · `report_academic.md:1265` (also 994, 1279, 1281) · "Pre-committed" tests were cited to §2.1 / §2.5 / §7 of a file with no numbered sections. **Applied.** They now cite `preregistration/null_hypotheses.md`. Line 1279 names §2.1 criterion 2 (ratio stability).
- **S8** · `report_academic.md:573` (also 142, 495 ×2, 580, 582, 1196) · Seven pointers sent readers to §5.5 for the Fisher/Bonferroni method. §5.5 never mentions either. **Applied.** All seven now point to §5.4.9.
- **S9** · `report_academic.md:78` · The Abstract pointed to §4.3.2 and §5.5 for the OSF disclosure. **Applied.** It now points to §4.3.3 and §5.3.1.
- **S24** · `report_academic.md:2772` · About 17 works cited by author and year have no reference entry (Brown 1975, Gelman–Rubin 1992, Vehtari 2021, Benjamini–Hochberg 1995, Liu–Xie 2020 and others). Fix: add verified APSA entries, or drop citations that cannot be verified. **Not applied** (each entry needs source checking).
- **S25** · `report_academic.md:2846` · About ten cases cited in the text are missing from Court cases (Vavilov, League of Women Voters, Dixon, Rizzo, Mohan, White Burgess, Haida, Taku River, Lalande, Whitford W.D. Wis.). Fix: add each with its neutral citation and existing status flags. **Not applied.**
- **S29** · `report_academic.md:2670` · Ledger entries C16 and C17 were removed in `cb6b1895`. `swarm_audit_2026-10-29.md` cites C16/:2714 on 164 lines. `proposals/site_rewrite_2026-10-29/rewrite_draft.md:222` cites "academic report C17". **Not applied: author decision Q2.**
- **S30** (duplicate: DS-08) · `data_supplement.md:292` (also 294, 295, 101) · §D8 named three scripts that never existed. **Applied** with a merged mapping. Ch3: `neighbour_drain_adjacency.py` (coupled counts) and `drain_phase_b_canonical.py` (canonical label-shuffle null; this script writes `findings/drain_label_shuffle_null_canonical.json`). MAD: `mcmc_ensemble_canonical.py` and `joint_outlier_score_canonical.py`, plus `electoral_forensics_population.py` for the commission-table MAD. Reock: the same two canonical scripts, with `reock.py` marked DPG-era only. **The Hansard source was not changed**: no tracked raw Hansard text exists (the only tracked derivative is a progress log). Counted as applied in part.

**PDF and build**
- **PDF-02** · `analysis/scripts/build_academic_pdf.py:941` · The build turns relative links into `file://` URLs. The committed PDF has 38 dead links, and they expose a local Windows username and folder path. Fix: rewrite relative hrefs to GitHub URLs in `post_process_html`, then rebuild. **Not applied** (code).
- **PDF-05** · `build_academic_pdf.py:858` · The DOCUMENTED CORRECTIONS ledger (3,667 words) is styled as a 30%-wide floated sidebar. It prints as a narrow column across many pages, with a blank page before it. Fix: exclude it from the sidebar rule, or only treat titles starting "SIDEBAR" as sidebars. **Not applied** (code).
- **PDF-06** · `report_academic.md:2609` (also 344 and the other wide tables and code blocks) · Wide tables and code blocks run off the A5 page. Whole columns are missing from the print ("Audit-trail anchor", "Manifest anchor"). Fix: wrapping CSS, plus landscape pages or footnoted URL columns. **Not applied** (code and layout).

**Methodology** (all author decisions; see §4)
- **MC-A2** · `report_academic.md:88` (also 1602; `plain_language_defense.md:690`) · "Canonical ensemble uses official shapefiles … 89 EDs each" reads as if the neutral plans have 89 districts. The 89-ED shapefiles only score the two commission maps. **Decision A2.**
- **MC-A3** · `report_academic.md:1328` (also `methodological_defenses.md:45`, `plain_language_defense.md:738`, `preregistration/thresholds.md:138`) · "±25% constraint for all 89 EDs". The ensemble applies it to 87 districts around a quota of total/87. **Decision A3.**
- **MC-A4** · `report_academic.md:1644` · The reason given for not scoring 2019 MAD/Reock is inverted. The real obstacle is that 2019 breaks ±25% on 2021 population (7 of 87 districts). **Decision A4.**
- **MC-A6** · `report_academic.md:1718` (also 1642, 1711) · The 2019 seats@50/50 percentile of p78.54 is a floating-point tie artefact. With a tolerance it is about p65.4. The majority's identical p78.54 is the upper edge of the 40/87 block. **Decision A6.**
- **MC-A7** · `report_academic.md:1415` (also 2741; `mcmc_ensemble.py:752`; `mcmc_ensemble.md:56`) · The ensemble is described as the neighbourhood of the 2019 map. Chains start from a fresh 87-part seed, and 2019 supplies only the count. **Decision A7.**
- **MC-A8** · `report_academic.md:2741` · The 87-district ensemble is offered for "any 89- or 91-seat map" with no size caveat. **Decision A8.**
- **MC-A9** · `report_academic.md:1791` · S5 is described as tested against "≥1,010,000 neutral 91-seat maps". The registered reference is the fixed 87-district canonical run. **Decision A9.**
- **MC-A10** (likely) · `report_academic.md:538` (also 1629, 1634, 1658; `data_supplement.md:201`) · MAD percentiles compare 89-district maps with 87-district plans. The cross-size effect understates both maps' percentiles by a few points. **Decision A10.**
- **MC-A11** (question) · `report_academic.md:1672` (also 56, 78) · The headline D² = 33.64, p = 8.80×10⁻⁷ is against 87-district plans, with no size caveat. The effect of a size-matched null is unknown. **Decision A11.**
- **MC-B2** · `report_academic.md:2430` (also 833, 834) · B4 takes 2019 from the full statement of vote (46) and the 2026 values from the substrate. On the substrate, 2019 is 47 NDP / 40 UCP, and the asymmetry is 7, not 5. **Decision B2.**
- **MC-B3** · `analysis/methodology/methodological_defenses.md:55` · "The partisan metrics score Actual Votes Cast." They score election-day votes only. **Decision B3.**
- **MC-B4** · `report_academic.md:1052` · "A 1–3 seat shift … is a rounding error." The canonical gap is 5 seats (substrate and at a tie), and about 9 at the real 2023 level. **Decision B4.**
- **MC-B5** · `report_academic.md:363` · §3.2 does not disclose that election-day voters were about 3 points more UCP than the electorate (57.4% vs 54.4%). **Decision B5.**
- **MC-C2** · `report_academic.md:2421` (also 1720) · The 2019 "MAD from avg" of 2,010 is a median. The other cells are means; the mean for 2019 is 2,886, as Appendix C uses. **Decision C2.**
- **MC-C3** · `plain_language_defense.md:474` · Defines the 3,180 / 4,707 figure as a median. It is a mean (the medians are 2,015 / 3,153). **Decision C3.**
- **MC-C6** · `report_academic.md:2975` (also 2962) · Appendix C compares mean deviations across different quotas and bases. Its reason for not using the 2026 maps (shapefiles unreleased) is stale. **Decision C6.**
- **MC-P1** · `report_academic.md:1617` · The monograph never mentions Amendment 5, Parts 14–17. Line 1617 says a constraint-enforcing re-run "was not completed", which contradicts §5.4.1 (:1330). **Decision P1.**

**Supporting documents**
- **DS-01** · `data_supplement.md:238` (also 113, 247) · The §D6 R̂ table is the 2026-05-10 run (4 × 62,500), labelled as 4 × 252,500. The clean-rerun values are 1.00011 / 1.00205 / 1.00016 / 1.00149, all passing. **Held** (changes numbers).
- **DS-03** · `data_supplement.md:269` · Tells strict reviewers to treat the Fisher result as driven by the "registered" Ch2. Fisher is retired, and Ch2 is not prospectively registered. Fix: the replacement paragraph in the finding. **Not applied.** The section pointer in the same paragraph was corrected (DS-10).
- **DS-04** · `data_supplement.md:253` · "All registrations were submitted before examining the test data." 6pt83, yvc7g and s58a6 post-date the shapefiles, and u47bq is retrospective for the commission. **Not applied.**
- **DS-06** · `data_supplement.md:277` (also 278) · drand record rows. Row 277 lists the 6pt83 seed under an s58a6 salt. Row 278's salt was wrong. **Applied in part**: the row 278 salt is now `alberta-audit-mcmc-rerun-base`, which reproduces its seed. Row 277 is **held** (it changes the listed seed).
- **PLD-08** · `plain_language_defense.md:257` (also 520, 558–560, 564, 1464, 1549–1551) · The retired blend-model Monte Carlo is still defended as current. Line 1464 misdescribes what the interval measured. **Not applied.**
- **PLD-09** · `plain_language_defense.md:536` (also 502, 538, 548, 614, 632, 634, 832) · Stale §5.2.1 values (B3, B4 45/46, EG p94.4, 4.10% as the canonical p95). **Held** (numbers).
- **PLD-10** · `plain_language_defense.md:1689` · Declination values from before Amendment 5, Part 9, with no banner. **Held** (numbers).
- **PLD-11** · `plain_language_defense.md:410` (also 1276, 1282, 1288, 1677) · Uses the retired "negative = UCP" sign convention, and misreads Reading B as NDP-favourable. **Not applied.**
- **PLD-12** · `plain_language_defense.md:1274` (also 1334, 1344–1346) · Presents the retired Readings A and B as the verdict basis. "52.8% → 48.3%" mixes UCP and NDP fractions. **Not applied.**
- **PLD-13** · `plain_language_defense.md:1406` (also 792–800, 1344, 1412–1432) · Misstates hypotheses H1–H4 and keeps the retired "lawsuit-grade" 2M-draw ceiling. **Not applied.**
- **PLD-14** · `plain_language_defense.md:113` (also 91, 712, 1314) · Reads 8.80×10⁻⁷ as an observed frequency, and inverts what p = 0.102 means for the majority. **Not applied.**
- **PLD-15** (likely) · `plain_language_defense.md:726` (also 604, 722, 1212, 1597–1599) · "Gives the NDP 44.8% of seats" should be UCP. The "structural UCP floor" framing (also monograph :1363) conflicts with the s50 definition and the C13 glossary. **Not applied.**
- **PLD-16** · `plain_language_defense.md:1118` (also 288–290, 1605) · Says the Lalande reasons are pending, cites the withdrawn Cassista case, and puts the ±25% band at s.14. **Applied in part**: s.14 → s.15(1) at 288 and 290, and Cassista dropped at 1605. **Held**: the Lalande publication status at 1118, and the "SCC has not revisited since 1991" sentence at 1605.
- **PLD-17** · `plain_language_defense.md:1244` · Says a single Airdrie district is legal (85,805 exceeds the 68,661 cap), and makes an unsourced claim about "a million maps". **Not applied.**
- **PLD-18** · `plain_language_defense.md:1162` (also 89, 1250, 1545, 1741) · Calls the tests "independent". The monograph says they are correlated. **Not applied.**
- **PLD-19** · `plain_language_defense.md:346` (also 1188) · Says "all three vote inputs point the same direction". The two 338Canada probes disagree (C7). **Not applied.**
- **PLD-21** · `plain_language_defense.md:832` (also 388, 396, 510, 514, 698, 816, 822, 860, 1168) · Stale seed round, R̂, ESS and percentiles; "Cannon et al. 2022"; "1 in 15 million". **Applied in part**: Cannon et al. 2022 → 2023 at 816 and 822. The rest is **held** (numbers).

### 2.3 Low

**Structure and references**
- **S7** · `report_academic.md:1080` (also 784, 984, 1317, 2682) · Three cross-document citations named the wrong file or section. **Applied** with the corrected fix: `preregistration/thresholds.md` §B.2.1; `population_deviation_reaudit.md` §3.4 criterion (b) and §7 item 1; `preregistration/retraction_conditions.md` §9 item 1.
- **S10** (with S11, S12; duplicate: PDF-09) · `report_academic.md:1328` (also 1349) · Two malformed anchors. **Applied**: `#sec-5-1-4` and `#sec-5-2-10`.
- **S11** · `report_academic.md:1384` · `#documented-corrections-c10` did not exist. **Applied**: anchors added for the ledger and for C10. The C10 anchor sits inline on the C10 line, so it adds no empty paragraph.
- **S12** (duplicate: part of PDF-10) · `report_academic.md:2692` (also 582, 1684) · References to §10 and §10.2, which do not exist. **Applied**: 2692 → §4.3.1; 582 and 1684 now read "is left as future work".
- **S13** · `report_academic.md:576` · The November scorecard row pointed to §5.6. **Applied**: §5.5.
- **S14** · `report_academic.md:56` (also 2435) · "See §1.2 for the exploratory/confirmatory distinction." §1.2 does not discuss it. **Applied**: now §1 and §4.3.1.
- **S15** · `report_academic.md:144` (also 139, 145, 146, 150) · Script-table section numbers, one of which did not exist. **Applied**: §5.4.9, §5.4.8 ×3, §5.2.5.
- **S16** (question) · `report_academic.md:151` · Six scripts in the table are never cited in the body. `ecological_inference.py` is a stub, and no reported number depends on it. **Not applied: author decision Q3.**
- **S17** · `report_academic.md:495` (also 573, 582) · "§G1" does not exist. **Applied**: now cites `analysis/methodology/fisher_independence_defense.md`.
- **S18** · `report_academic.md:2914` (also 114) · Gate G0 is cited, but §4.1.2 defines only G1–G5. Fix: define G0, or cite G1–G5 and G1. **Not applied.**
- **S19** · `report_academic.md:392` · "The §5.1.1 correction note above" points forward to a section with no such note. The note is in §3.3 at :382. Fix: point to §3.3. **Not applied** (marked non-mechanical, although the corrected fix is a one-pointer change).
- **S20** (duplicate: part of PDF-10) · `report_academic.md:2912` (also 326, 328, 1844, 3105–3107) · Pointers left over from an older numbering scheme. **Applied**: 2912 → §5.1 and §5.2; "§ E" → §6.2 at 328 and 1844 (the two-lane verdict, which is the best fit; the author may prefer §6.2.2); "§12 commentary" dropped at 326; E.6 Sections A–D → §5.1/§5.2, §5.8, §5.9.
- **S21** · `report_academic.md:3079` (also 339) · Appendix E promises a closing note that is not there. Line 339 points to a Plan B cross-check that line 374 says was never produced. **Not applied.**
- **S22** · `report_academic.md:3142` · The Cassista sentence pointed to a §2 discussion that is gone. **Applied**: the parenthetical was removed. The rest of the sentence ("cited in earlier drafts … withdrawn") is left for the author (see Q2).
- **S23** · `report_academic.md:1384` · The canonical R̂ paragraph and table sit inside the DPG-era §5.4.2. Fix: move them to §5.4.9. **Not applied.**
- **S26** · `report_academic.md:2866` · Statutes lists only the EBCA. At least six other enactments are cited. **Not applied.**
- **S27** · `report_academic.md:2790` (also 2832, 2848, 2886) · Uncited entries, ordering errors and an "APA" label. **Applied in part**: McCartan and Imai 2023 is now cited at :110 and sits after King and Browning. Alphabetically it comes before McDonald, so the finding's "after McDonald" placement was not used. The 1993 Reference re entry now sits beside the other Reference re entry. "APA" → "APSA" at both footers. **Held**: Sancton 2008, which is never cited; drop it unless a citing passage is intended.
- **S31** (duplicate: DS-10) · `data_supplement.md:111` (also 112, 169) · §D4 section column errors. **Applied** (see DS-10).
- **S32** (likely) · `report_academic.md:1234` (also 1800, 1935, 2056, 2058, 2118) · "Appendix C" and "Appendix E" are used for both the monograph's and the commission's appendices. Fix: qualify each commission appendix. At 1234 write "minority report Appendix E, map 73 (p. 359)". **Not applied** (not confirmed).
- **S33** (likely) · `report_academic.md:3056` · D.4 sends readers to §5.6 for Polsby-Popper figures that are not there. Fix: point to `findings/polsby_popper_verdict.md` and C3. **Not applied** (not confirmed).
- **S34** · `report_academic.md:54` (also 80, 306) · Three imprecise pointers. **Applied**: 54 now reads "analysed in this audit's §5.8.2 and §5.9.4"; the footnote at 80 now points to §5.8.4 (community-of-interest splits); the §2 self-reference at 306 now reads "see Appendix F".

**PDF and build**
- **PDF-11** · `report_academic.md:595` (also 2477, 2479) · Three links said the Author disclosure is in §1. **Applied**: an `author-disclosure` anchor was added, and the three links now use it.
- **PDF-12** · `build_academic_pdf.py:936` · No math renderer, so LaTeX prints raw, and `\!` is mangled. **Not applied** (code).
- **PDF-13** · `build_academic_pdf.py:848` · The provenance blockquote prints as a boxed "deck" above the title. Fix in the build only; DEPENDENCY_CONVENTION.md requires the blockquote in the markdown. **Not applied** (code).
- **PDF-14** · `build_academic_pdf.py:71` · The Google Fonts URL asks for an axis Playfair Display lacks, so the display font silently falls back. **Not applied** (code; mechanical, a one-line fix).
- **PDF-15** · `build_academic_pdf.py:827` · The PDF title metadata is a retired title, "The Quiet Part". **Not applied** (code; mechanical).
- **PDF-16** · `build_academic_pdf.py:48` · The build only finds Chrome/Edge at Windows paths, and its output depends on the platform. Fix: CHROME_PATH or a PATH lookup, pinned fonts, and the browser version in the metadata. **Not applied** (code).
- **PDF-17** · `build_academic_pdf.py:947` · No PDF bookmarks. Fix: add `--generate-pdf-document-outline`. **Not applied** (code; mechanical).
- **PDF-18** · `build_academic_pdf.py:907` · The drop-cap class lands on an empty anchor paragraph, so the adjacent-element CSS never matches. **Not applied** (code).
- **PDF-19** · `report_academic.md:37` (also 25) · Title block said "Draft — June 2026", and the header called the PDF print-ready. **Applied**: "Draft — October 2026"; the PDF is marked "not current; rebuild pending".
- **PDF-20** (question) · `report_academic.md:42` · The site dropped the NDP-volunteering clause (`390afa8d`). The monograph and public report keep it, and the PDF has a third wording. **Not applied: author decision Q1.**

**Methodology**
- **MC-B6** · `report_academic.md:1334` (also 1177, H8 at 2618) · The "full-vote" substrate still undercounts two-party votes by about 9.5% (unattributable Vote Anywhere ballots), and is more UCP than the actual result. **Decision B6.**

**Supporting documents**
- **PLD-20** · `plain_language_defense.md:642` · v0_7 DPG values in the §5.2.9 entry. **Held** (numbers).
- **PLD-22** · `plain_language_defense.md:167` · Said R was not used. The monograph says R 4.6 with `redist` was used for one script. **Applied**, and the answer at :169 was adjusted to match.
- **PLD-23** · `plain_language_defense.md:336` · Mixes up the 2,110 SZAT swing-zone VAs with the Vote Anywhere problem. **Not applied.**
- **PLD-24** · `plain_language_defense.md:740` (also 838–840) · Calls the constraint-enforcing run "future work", though it ran on 2026-06-13. The mechanism at :840 is backwards. **Not applied.**
- **PLD-25** (likely) · `plain_language_defense.md:1468` (also monograph :2641) · Holm p = 0.0148 is from an older run; the canonical tail p is about 6.8×10⁻⁵. **Not applied** (not confirmed; it also changes a number).
- **PLD-26** (likely) · `plain_language_defense.md:33` · "Both maps pass" the 7% line holds only for 2023 and 2019 votes. Under 2015 votes both exceed it. **Not applied.**
- **PLD-27** · `plain_language_defense.md:1296` (also 45, 452, 590, 1026, 1112, 1464, 1583) · Mechanical defects. **Applied in part**: the path at :45, "§914" → §5.2.4 at :590, the §5.8.2/§5.9.4 wording at :1026, "§1706 entry" → "Appendix E Phase 4C entry" at :1464, and the end marker moved to the end of the file. **Held**: 1,140 vs ~1,340 at :1298 (number), the GM37 date wording at :1112, and "calibrated to Chen" → "stricter than Chen" at :452 (claim).
- **DS-02** · `data_supplement.md:169` (also 175) · Pairs Fisher T = 39.0 with the recomputed p. **Held** (numbers).
- **DS-05** · `data_supplement.md:253` · Said OSF links are archived in `FROZEN_MANIFEST.md`, which holds none. The table omitted yvc7g. **Applied**: the pointer now names §4.3.3 and `preregistration/seed_commitments.md`, and a yvc7g row was added (filed 2026-05-10, as in monograph :574).
- **DS-07** · `data_supplement.md:87` (also 273) · The documented seed formula matched neither derivation in use. **Applied**: both derivations are documented exactly.
- **DS-09** · `data_supplement.md:117` (also 113, 114, 298, 299) · Wrong generating scripts. **Applied**: `sentiment_intensity_score.py`; the two s58a6 JSONs are marked "committed output (`1dd5e91b`); generating code not in repo". The same mislabel at §D8 :300 was fixed to name both pipeline stages.
- **DS-10** · `data_supplement.md:112` (also 103, 111, 120, 269) · Wrong report-section pointers. **Applied** with the corrected fix: §5.4.9, §5.2.10, §5.9.4.7, "§5.2.10 and DOCUMENTED CORRECTIONS C1 (§7.3)", §4.3.3.
- **DS-11** · `data_supplement.md:201` · MAD tail p and percentiles slightly off (p99.1 / p15.9). **Held** (numbers).
- **DS-12** · `data_supplement.md:206` · A 5th–95th range was labelled a 95% interval. **Applied**.
- **DS-13** · `data_supplement.md:202` · "Reock median" is proxy Reock. **Applied**: relabelled.
- **DS-14** · `data_supplement.md:31` (also 39) · Stale file counts. **Held** (numbers; trivial).
- **DS-15** · `data_supplement.md:128` · "Values at HEAD 7b7b2fe" cannot be right; the values come from the 2026-07-12 rerun. **Applied in part**: :128 now says so. No commit hash was recorded, because nothing is committed yet; :17 (submission HEAD) was left as a historical record.
- **DS-16** · `data_supplement.md:97` (also 58, 98) · Wrong description of the VA file, a missing source path for the 2023 totals, and a stale DPG sunset note. **Applied**.
- **DS-17** · `data_supplement.md:101` (also 221, §D2) · The Hansard counts are configuration-relevant subsets, not the corpus, and §D2 omitted R. **Applied**: relabelled without adding new numbers; R row added (`redist`, R 4.6, not pinned).

---

## 3. Findings the verifier rejected

Rejected outright:
- **PDF-07** — The C16/C17 removal was deliberate (`9280fbf8`, the author's no-change-notes rule). They were factual and citation corrections, not failed findings, so the never-delete policy does not cover them. The open part stays as S29 / Q2.
- **MC-C5** — The finding's own numbers contradict it. The median statistic separates the maps more than the mean (2.17× vs 1.48×). On the 2021 overlay, the mean deviations are almost equal (10.12% vs 10.17% of quota). The valid part is covered by MC-C1.

Parts of upheld findings the verifier rejected or corrected:
- **S2** — "historical/ → archive/" was wrong; the tracked `archive/` does not hold the stress-test passes.
- **S4** — Several provenance details were wrong (moves recorded as deletions, wrong commits, "never in git" for two tracked files).
- **S7** — The ~143 km figure is in §7 item 1, not only §3.4.
- **S16** — "Ecological inference" does appear, at :2660, as a limitation label.
- **S19** — "The ~10% figure is documented nowhere" was false; it is at :382.
- **S28** — "p ≤ 2.80" does appear once in the markdown, as the superseded value in C10.
- **S30** — Parts of the mapping were wrong. The verifier's own Ch3 pick (`drain_label_shuffle_null.py`) is the stale-substrate original; `drain_phase_b_canonical.py` writes the canonical JSON, as DS-08 said.
- **S32** — "Appendix C crosswalk" at :1935 is a correct pointer to the majority report's appendix; the suggested file was wrong.
- **PDF-01** — Minor: the PDF also cites Amendment 11, and the markdown still has "p94.4" twice.
- **PDF-04** — The verifier said 4 files were gone. `git show -M aecc6f06` shows 3 of them as R100 renames, so 13 moved and 1 was deleted, as S2 said.
- **PDF-13** — Moving the provenance block into the HTML comment conflicts with DEPENDENCY_CONVENTION.md; fix it in the build only.
- **PDF-16** — The Windows-only requirement is documented (reports/README.md:26). The issue is portability.
- **MC-B6** — The suggested H8 note was wrong; advance ballots keep their real party split per poll group.
- **MC-C6** — The fix should warn that the 2021-basis ordering will probably not hold.
- **PLD-05** — The proposed fix copied the monograph's sign-order error; the minority stays more UCP-favourable in all three elections.
- **PLD-19** — Basing the fix on a "2019 reversal" is doubtful; base it on the 338Canada probe disagreement.
- **DS-10** — "The monograph never mentions an IRR gate" was false (§5.9.4.7, :2206).

---

## 4. The author's decisions

### 4.1 Methodology (23 items)

- **A1** (MC-A1, high). Rewrite the :1722 caveat. Canonical plans have 87 districts, so 2019 is same-size and both 2026 maps are cross-size. Keep the ln(87)/ln(89) bound for δ, and say it does not cover seats@50/50 or MAD. *Recommend: accept.*
- **A2** (MC-A2). At :88, :1602 and PLD :690, say the neutral plans are 87-district ReCom partitions, and that the 89-ED shapefiles only score the commission maps. *Recommend: accept. This is the likely root of A1, A3 and A9.*
- **A3** (MC-A3). Change "all 89 EDs" to "all 87 districts of each neutral plan (quota = 2021 population / 87)" at :1328, `methodological_defenses.md:45`, PLD :738 and `preregistration/thresholds.md:138`. *Recommend: accept. thresholds.md is under preregistration/, so decide whether this needs an amendment entry.*
- **A4** (MC-A4). At :1644, give the real reason: 2019 breaks ±25% on 2021 population (7 of 87). Mark the 2026 MAD and Reock rows cross-size. *Recommend: state the reason, and optionally report 2019 MAD (~3,085, ~p41) with the caveat.*
- **A5** (MC-A5, high). Drop "ceiling figures survive" at :1593. Say the minority (46/89 = 51.69%) lies just below the 87-district maximum (45/87 = 51.72%, 69 plans). Change "reach this value" to "exceed it (all at 45/87)" at :1691, :2550 and :2589. Give hill-climb and minority results as seat counts on their own denominators. *Recommend: accept. p99.99 still stands as a percentile.*
- **A6** (MC-A6). Recompute the 2019 seats@50/50 percentile with a tolerance (about p65.4) at :1642, :1711 and :1718. Describe the majority's p78.54 as the upper edge of the 40/87 block, and cite the 89-district values (p51–57). *Recommend: change the text now. Make `pct_rank` tie-tolerant only through an amendment, because the scoring spec pins the code.*
- **A7** (MC-A7). Add one sentence in §5.4.9: chains start from a recursive_tree_part 87-part seed, because 2019 breaks ±25% on 2021 population. Adjust :1415, the plot title in `mcmc_ensemble.py:752` (a code change), and `findings/simulation_short_bursts.md:4`. *Recommend: accept. ":2741 2019 substrate" can stay.*
- **A8** (MC-A8). At :2741, say 89- and 91-seat maps are placed against the 87-district set as a cross-size headline, with the Amendment 5, Part 14 size-matched sets beside it. *Recommend: accept.*
- **A9** (MC-A9). At :1791, say S5 uses the fixed 87-district canonical ensemble as the headline, with the Amendment 5, Part 14 sets beside it, final at n_eff ≥ 400 (Amendment 5, Part 16). *Recommend: accept.*
- **A10** (MC-A10). Either report MAD as a percentage of quota, or say the cross-size comparison understates both maps' percentiles by a few points. *Recommend: note it, and handle it together with C4. The effect strengthens the minority flag, so it is a disclosure issue.*
- **A11** (MC-A11). Add a sentence beside the headline: the joint p is against 87-district plans; per-metric tails hold on the 89-district constrained null (:1330); a size-matched D² will follow from the Amendment 5, Part 14 chains once n_eff ≥ 400. *Recommend: add the sentence. Compute the size-matched D² before November if time allows.*
- **B1** (MC-B1, high). Relabel the :829 row as UCP seats on the 2023 election-day substrate (UCP 57.4%). Put 2019 on the same substrate (30 / 57), and add the real 2023 result (38 / 49) as its own row. Optionally add a 54.4% row (46 / 44 / 53). Same change at `partisan_bias_summary.md:220`. *Recommend: accept.*
- **B2** (MC-B2). Use the substrate value for 2019 in B4 (47 NDP / 40 UCP; asymmetry 7), or footnote B4 and the asymmetry row as mixed-substrate. *Recommend: use the substrate value.*
- **B3** (MC-B3). At `methodological_defenses.md:55`, say "election-day votes (896,644 of 1,706,304 two-party; UCP 57.4% against 54.4%)". *Recommend: accept (low stakes; the same file already says so at §1.1).*
- **B4** (MC-B4). At :1052, replace "1–3 seat" with 5 seats on the substrate and at a tie, and about 9 at the real 2023 level, judged against the 11-seat actual spread. *Recommend: accept.*
- **B5** (MC-B5). Add to §3.2 item 5 that election-day voters were more UCP (57.4% vs 54.4%), so substrate seat counts are not actual seats; s50 and mean-median remove most of this; raw seats and EG do not. *Recommend: accept.*
- **B6** (MC-B6). Rename "full-vote" at :1177, :1334 and H8 to "election-day plus apportioned advance/special ballots (1.54M of 1.71M; Vote Anywhere excluded; UCP 55.3%)". Use the verifier's corrected H8 wording. *Recommend: accept the corrected version.*
- **C1** (MC-C1, high). Keep "MAD" for one statistic and rename the other everywhere. Add a sentence in §5.1.1 and §5.4.9 saying the p99.1 placement uses a different statistic and base from the 48% headline. *Recommend: accept. Decide this first, because C2, C3, C4 and A10 depend on it.*
- **C2** (MC-C2). At :2421, use 2,886 (mean, as in Appendix C). At :1720, compare like statistics or say the three figures use three statistics. *Recommend: accept after C1.*
- **C3** (MC-C3). At PLD :474, define it as the mean absolute deviation, and retitle :472. *Recommend: accept.*
- **C4** (MC-C4, high). Label every ensemble-MAD placement as conditional on the ±12.5% proposal band. Report the statute-band placement (p0.0 / p0.013) beside it. Restate "fifth flag" and "confirms" as conditional, citing Amendment 5, Part 14, set B. *Recommend: accept. The 48% commission-table comparison can stay as the population headline.*
- **C6** (MC-C6). Compute all three maps on the same 2021 VA overlay, give each as a percentage of its quota, and replace the stale shapefile sentence at :2962. Expect 2019 9.7%, majority 10.1%, minority 10.2%. *Recommend: accept, and rewrite the Interpretation paragraph. The majority's tighter spread then appears only on the 2024-estimate tables. Add the cycle-lag caveat.*
- **P1** (MC-P1). Add a short paragraph in §5.4.9 or §5.4.10 on the Amendment 5, Parts 14–16 sets (size-matched 89/91, statute band, municipality-aware, s.15(2); final at n_eff ≥ 400). Fix :1617, which contradicts :1330. *Recommend: accept. This also gives A8, A9 and A11 somewhere to point.*

### 4.2 Open questions (3 items)

- **Q1** (PDF-20). Which disclosure wording is authoritative? The site drops the NDP-volunteering clause. Monograph :42, `report_public.md:47`, `conflict_of_interest.md:20` and `evaluation_symmetry_matrix.md:12` keep it, and the PDF has a third wording. *Recommend: pick one wording and apply it to all five places before any PDF rebuild. Resolve it together with swarm #454, #487, #488 and #616.*
- **Q2** (S29). C16 and C17 were removed from the ledger. *Recommend: keep them removed. This matches the `9280fbf8` rule, and the header's never-delete promise covers failed findings only. Then (a) repoint `rewrite_draft.md:222` from "academic report C17" to the amendment log or legal_framework.md, (b) leave the swarm audit as a dated record, and (c) remove Appendix F's "was cited in earlier drafts … withdrawn" Cassista sentence (:3142) under the same rule.*
- **Q3** (S16). Six scripts in the Author-disclosure table are never cited in the body. *Recommend: cite each where its result appears, or mark it "supporting". Drop the `ecological_inference.py` row, because it is a stub and no reported number depends on it.*

### 4.3 Mechanical edits held for approval

These are ready to apply as written in each finding. They wait only because they change a number or a stated claim: PLD-02, PLD-03, PLD-09, PLD-10, PLD-20, DS-01, DS-02, DS-11, DS-14, plus the held parts of PLD-16 (:1118, :1605), PLD-21, PLD-27 (:1298, :1112, :452), DS-06 (:277) and S27 (Sancton). *Recommend: approve PLD-03 and DS-01 first. Both are high-visibility stale facts.*

---

## 5. Coverage notes

**Structure pass.** Scripted checks over the whole monograph: all 110 anchors, every internal link, all 747 plain § references against the heading list, footnotes, appendix letters, all 38 relative links, every backticked path (against `git ls-files` and history), external-file § references, the script-table section column, above/below direction, and author-year, case and statute citations in both directions. Read in full: front matter (1–340), 1263–1317, 1370–1396, 2655–2758, References and Appendices A–G. Also checked: `data_supplement.md` section references and paths, and the PDF via pdfinfo and pdftotext.

**PDF pass.** The current markdown was rebuilt into a scratch PDF without touching the repo (229 pages vs 215 committed). Checks: link annotations, named destinations, fonts, images, a sentence-level text diff, layout overflow at A5 width, and rendered pages. The monograph has no embedded images.

**Methodology pass.** All four canonical chain CSVs (1,010,000 rows) were checked, along with the real-map scores, the percentile CSVs, the commission population tables (all three MAD definitions recomputed), the VA gpkg, uniform swing to 54.44%, Amendment 5, Parts 12–17, 19–21 and 26, and the scoring spec. The exploratory 89-district chain 100 was used only for its own distribution.

**Supporting pass.** `data_supplement.md` and `plain_language_defense.md` were read in full and checked against the monograph, data, code and drand derivations.

**This pass's checks after editing.** Every link and anchor in the monograph resolves. Every backticked path was re-scanned. The paths still missing are the S4 items, `plan_b_cross_check.md` (described as never produced), `pre_registration_draft.md` at :1752 and :2750 (a swarm-audit item, not edited here), and the `historical/` mention in the new :2941 text. The monograph line count is unchanged.

**Disagreements between passes, settled here.**
- PDF-04 vs S2: `git show -M aecc6f06` shows R100 renames, so S2 is right.
- S30 vs DS-08: `drain_phase_b_canonical.py` writes the canonical label-shuffle JSON, so DS-08 is right.
- S27: McCartan was placed alphabetically, not "after McDonald".
- S20: "§ E" became §6.2 (best fit; the author may prefer §6.2.2).

**Audits and updates (the user asked that these not be forgotten).**
- `analysis/review/swarm_audit_2026-10-29.md` was used to avoid overlap, and was not edited. Its 164 lines citing C16 / :2714 now point at removed text (Q2). Swarm items that touch this pass and are still open: `pre_registration_draft.md` at §5.5 and §8.1, the OSF dates in data-supplement §D7, and the disclosure questions #454, #487, #488 and #616 (Q1).
- `findings/pre_registration_amendment_log.md` and `preregistration/november_2026_scoring_spec.md` were not edited (by rule). Amendment 5, Parts 14–17 exist, but the monograph never mentions them (P1).
- The site update in `390afa8d` (disclosure wording) has not reached the monograph, the public report or two methodology files (Q1).
- `proposals/site_rewrite_2026-10-29/rewrite_draft.md:222` still cites "academic report C17" (Q2).
- The other review records in `analysis/review/` (truth_audit_2026-06-26, project_assessment_2026-06-27, report_skeptic_review_2026-06-27, the legal, science and peer reviews, the external audits, and others) were not re-read in this pass.

**Not checked.**
- The semantic fit of the ~700 internal § references beyond labelled ones and a sample.
- External URLs (no web fetches).
- § references inside `preregistration/*.md` and `findings/*.md`, beyond those the monograph cites.
- Numbers in the current markdown against `data/outputs` (the swarm audit's job).
- `reports/public/` (only incidental hits).
- OSF records, the raw Hansard text (gitignored), the LFS raw samples, and the legal content of the Grant v. Torstar factors.
- Every PDF page by eye.
- The exact markdown commit the committed PDF was built from.
- A size-matched joint D² (A11) and exact size-matched MAD percentiles (A10).
- No new ensemble was run.

**Seen in passing (not filed as findings).**
- Monograph :110 says "No other R packages were used", but `redist_crossvalidation.R` loads redistmetrics, sf and dplyr.
- `maps/*.jpg` at :227 and :347 should be `data/maps/*.jpg`.
- The DOCUMENTED CORRECTIONS ledger breaks into separate blockquotes at blank lines 2693, 2695 and 2697 (C11–C14).
- :1393 cites `simulation_convergence_diagnostics_canonical.json` for R̂, but the file has none.
- :1363's "structural UCP floor" conflicts with the s50 definition.
- :404 keeps the old +0.03/+0.75/−0.51 asymmetry.
- :2641 Holm p is stale (see PLD-25).
- Appendix B still lists the Fisher defenses as current.
- `robustness_rerun_seed_commitment.md:46` calls a seed irreproducible, but it reproduces.
- A tracked `report_public.pdf` sits at the repo root, although reports/README.md says it was retired.
