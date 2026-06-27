# Truth audit — public report claims vs. primary sources (2026-06-26)

> **Resolution status (en + fr applied; 17 machine locales pending propagation):**
> A1–A3 ✅ (pre-registration wording aligned to methodology) · B4 ✅ (drain
> counts 1/2/5) · B5 ✅ (Airdrie → Olds-Three Hills-Didsbury) · B6 ✅ (defense3
> MAD wording) · B7/B8 ✅ (Motion 19 + Nov-2 committee deadline) · B9 ✅ (Lunty
> = "a UCP MLA", not "Premier-appointed") · C-Quebec ✅ (CRE finalises; no 2/3 —
> verified via Elections Québec) · C-BC ✅ (Assembly votes + enacts). OPEN:
> C-international comparators (US/UK/Australia — need primary-statute pass);
> 17-locale propagation of all the above.

Five parallel fact-checkers verified the report prose (`viewer/src/lib/i18n/locales/en.ts`)
against the canonical data outputs, shapefiles, methodology, and academic report.
Headline statistics and the core legal framing verify cleanly; the discrepancies
below are grouped by severity. No report files were edited — this is the record.

## A. Highest priority — pre-registration wording overclaims the methodology

These undercut the audit's own carefully-drawn exploratory/confirmatory line, on
which the conflict-of-interest defense depends. Fixes must align the prose to the
methodology, not the reverse.

1. **`prereg_body`**: "All five structural tests and four partisan-fairness metrics
   … were registered at OSF before any simulation was run." The methodology
   (`null_hypothesis_and_exoneration_criteria.md` L19/37) says the opposite for the
   primary tests: seeds were committed to the drand beacon before shapefile release,
   **but the test names and combination method were NOT pre-registered on OSF before
   execution** — Ch1/Ch2/Fisher are labelled *exploratory*. Overclaim.
2. **`about_me.p3`**: lists OSF:6pt83 + AsPredicted #289,469 + #289,451 all as
   "written before results were examined." True for only **#289,451**; 6pt83 was
   filed ~3h after szat.py first ran, and #289,469 is logged "results known at
   filing." Collapses the seed-committed-before / form-filed-after distinction.
3. **`conditions_intro`**: "retracted only if at least **three of the five** tests
   fail." No 3-of-5 meta-rule exists; the methodology has 3-of-6 (§7.1A) and 3-of-4
   (§7.2). Unsourced threshold.

## B. Factual errors fixable from the repo's own canonical sources

4. **Neighbour-drain counts** (`litmus.table_r8_b/c`, `closing_p2`): report says
   minority 2 / majority 6 / 2019 5. Canonical run (`findings/neighbour_drain_analysis.md`)
   gives **minority 1 / majority 2 / 2019 5** — the 2/6 are superseded DPG-era figures.
   The pre-registered PASS direction (minority < majority) still holds.
5. **Airdrie's four EDs misnamed** (`cpd.airdrie_p`, `airdrie_callout_p2`): names
   "Calgary-Nolan Hill-Cochrane" as a piece, but that ED does **not** intersect the
   Airdrie CSD. The real four (by geometry): Airdrie-East (41%), **Olds-Three Hills-
   Didsbury (27%)**, Calgary-Airdrie (19%), Calgary-Foothills-Airdrie West (13%). The
   count "4" is correct.
6. **`defense3` (§5)**: "MAD was 4,707 … placing it at the 99th percentile." 4,707 is
   the A1 MAD (deviation from the common mean); the p99 belongs to the *ensemble* MAD
   of **3,938**. Cross-wires value and percentile (both are individually correct
   elsewhere).
7. **`editorial_intro` p3 omits Motion 19**: attaches the committee structure only to
   "Government Motion 37 (April 21, 2026)". The load-bearing fact is **Motion 19
   (April 16, 2026)**, which set aside both reports and created the Lunty committee;
   Motion 37 is the later motion constituting the advisory panel. (Both are correct
   facts; the omission misleads on which created the committee.)
8. **Deadline misattribution** (`editorial_intro` p3): "the legislature must approve
   whatever the committee delivers before November 2026." Sources say the **committee
   must produce/report** its 91-seat map by **November 2, 2026** — a committee
   deadline, not a legislative-approval deadline.
9. **"Premier-appointed" Lunty** (`editorial_intro` p3 / glossary): unsupported. He is
   the UCP MLA for Leduc-Beaumont chairing a Special Select Committee of the Assembly;
   no source states the Premier personally appointed him.

## C. Comparative-law claims — likely wrong or unverifiable from the repo

The academic report itself admits Section D rests on "comparator-case general
knowledge"; `peer_review_canadian.md` already flags the Canadian comparators as
"materially mis-described." Need primary-statute checks before asserting.

10. **Quebec "two-thirds supermajority"** (`editorial_canada` p5): no repo source
    supports it; the repo describes ordinary-process amendment / refusal-to-proclaim.
    Likely inaccurate — check Quebec *Loi électorale*.
11. **BC "default-adopt rule"** (`editorial_canada` p5): repo (`procedural_analysis.md`
    L68) shows BC 2008 **required an enacting statute** (Electoral Districts Act),
    contradicting "default-adopt."
12. **International comparators** (US CA/MI/TX/NC; UK 4 commissions / ~8-yr cadence;
    Australia AEC / 7-yr trigger; federal "automatic effect") — none grounded in repo;
    each needs a primary-statute check.
13. **Rucho wording**: "outside its jurisdiction" is loose — the holding was
    non-justiciability ("political question"), not jurisdiction-stripping.
14. **"clause C(d)(ii) of Motion 37"** (glossary): the sub-clause label is not in any
    repo file.

## D. Minor / caveats

15. **2019 scorecard placement** ("0 structural tests failed", safe corner): the
    structural tests are not scored for the 87-seat 2019 map (MAD/Reock not computed;
    NW-Calgary/Airdrie/chair-flags are 2026-specific), so 2019's vertical position is
    illustrative, not computed. Worth a caveat.
16. **Commission "judges, lawyers, public members, not politicians"**: majority
    commissioner Greg Clark is a former Alberta Party MLA — loose generalization.
17. **Chair-flag count inconsistency**: `structural_results` says "seven" configurations;
    `boundary.can_3` says "three" — the academic reconciles (3 confirmed anomalies; chair
    criticism spans 7 configurations) but the two blocks state different numbers
    without that reconciliation.

## Verified clean (no action)
- 1,010,000 maps; ~66 at seats@50/50; efficiency gap p94.4 "near but below p95";
  4-of-5 minority / 0-of-5 majority structural; all partisan percentiles & p-values;
  SZAT p=0.0024→exploratory; "1 in 350,000" (conservative rounding of 357,000).
- 87 / 89 / 89 / 4,765 counts confirmed against the shapefiles.
- Rucho (holding+year+citation), Saskatchewan Reference, Charter s.3 effective
  representation, EBCA ±25% (§15(1)/§15(2)), "no legal meaning in Canada."
- All OSF IDs (w2s8k/r3zm7/qsgy8/6pt83/s58a6) and AsPredicted numbers internally
  consistent (external page contents not checkable from the repo).
