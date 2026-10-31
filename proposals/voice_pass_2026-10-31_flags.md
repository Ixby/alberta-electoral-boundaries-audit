# Possible factual problems found during the 2026-10-31 voice pass

**Written:** 2026-10-31 15:45 MDT. **Status:** unverified leads, not findings. The voice pass changed no fact; each writer listed what looked wrong and left it alone. Each item needs checking against its source before anything is corrected, and every correction gets a DOCUMENTED CORRECTIONS entry.

Items already corrected are marked done. Line numbers are as the writers reported them and may have shifted.

## voice-body (251adbd8)
1. en.ts cpd.airdrie_callout_p1: Airdrie 85,805 "bigger than Red Deer" (Red Deer ~100k)
2. suggestions.lesser_slave_p1: 4,832 km2 "larger than PEI" (PEI ~5,660 km2)
3. suggestions.census_p1: "census every ten years" (five); "spring 2026" stale
4. cpd.packing_p: 11.5% vs 2.8% called "a quarter larger" (~8.5%); "province-wide population" -> average?
5. impact.summary_p: minority "crosses every one" vs 4 of 5 elsewhere
6. impact.chair_appendix_p: "~1,340 public submissions" vs 1,147
7. litmus.table_intro: "last two rows depend on votes" but vote rows are r6-r7; r8 is neighbour drain
8. suggestions.rationale_p2 "objective fact, not a judgment call" vs ebca_body "must judge"
## voice-home (54dc99c1)
- Done: happened.p2 "filed two maps" restored
1. glossary riding/electoral-district: "provincial term" claims; statute says "electoral division"
2. hero.cover_note "all three boundary proposals" — one is the 2019 enacted map
3. does.p9 "three boundaries" vs p10 "three of his four geometric flags" — confusing
4. know.p12 disclosure beat lacks Elections Alberta work; points to About me (confirm intended)
## i18n-committee-fix (65e781d6)
- 3 keys missing in all translations (english shows): november.r5_test, casings.frame_cast, authors_view.p5
- crk c5_cond phrase uncertain ("six days after"?) — needs native check
- FOLLOW-UP: glossary.lunty-committee.definition in all 18 locales still says five MLAs/Motion 19/April 16 -> retranslate from English
- Done (C37): English authors_view.p5 "five votes"
## voice-routes (efce7457)
- Done (C37): norms "the five MLA votes decide"
1. norms table count row "1 Yes · 2 Partial · 4 No · 2 Pending" vs cells 1 Partial, 5 No
2. norms ~l.281 "four of the committee's No cells" includes responsiveness marked Pending
3. explainers F "66 matches in 1,010,000" stale (C10) — methods says 69
4. explainers G "94th percentile" vs methods "94.5th"
5. explainers H DNA analogy: "90% chance someone else matches too" is wrong framing
6. law "some jurisdictions" vs norms "most provinces" (commission map default); explainers "almost no constraints" vs law "nothing governs"; "rewritten" vs "amended" 1995; glossary "electoral district" vs pages "riding"
## voice-pld1 (64a3df4f)
1. PLD l.25 majority tighter spread than 2019 vs l.163 / §5.1 l.494 "Not on this evidence"
2. PLD l.25 "every test declared publicly in advance" vs l.217 Ch1/Ch2 exploratory; l.668 cites "SZAT pre-registration"
3. 2019-vote direction: l.288 stable/artifact vs ll.25,273,536,590 reverses; l.273 "above" should be below; l.356 all three agree
4. l.338 maps designed from 2021 Census vs l.494 2024 estimates
5. l.344 2,110 VAs tied to Vote Anywhere vs elsewhere SZAT swing zones
6. l.612 neutral maps favour UCP because it wastes excess votes — looks backwards vs l.690
7. ll.29,205 drand beacon "Cloudflare's" vs League of Entropy
8. l.282 Warrington (2018) vs note l.280 (2019)
9. SZAT l.436 "partisan intent" wording; ll.436,662 p=0.0024 without l.93 caveat (Ch2 fails stricter spatial check)
10. l.404 "1,000,000 total steps" vs 1,010,000
11. l.33 "2023 election produced these maps"; "that range" around 7% unclear
## voice-casings (c5c6ca4f)
- Done (C37): casings.frame_p1b "Three weeks later"
- CHECK agent wording fixes: c3_found ("province-wide population" -> "provincial average"); c12_found ("that count" -> "we counted the rural divisions themselves")
1. frame_p1b "without precedent in the sixty years" vs c14_found says wrong because of 1992
2. c3_found "a quarter larger" vs 11.5% vs 2.8% (~8.5%)
3. c6_found2 majority 46.1% "sits at the neutral median" (median 44.8%; 46.1% = p78)
4. c12_found "~1,340 submissions" vs 1,147; rural arithmetic 31-3-3=25 not 28; 31-7=24 not 23
5. c2_found chair "flagged three boundaries" vs "four geometric flags"
6. frame_p4 promises "five legal reasons" but lessons run 1-8
7. rev_p2 calls EG "Act II's headline number" vs Casing 6 (seats 50/50 headline), Casing 7 (EG a miss)
## voice-readme (39ee8a64)
- STRUCTURE: README narrative block (orig 47-63) moved above Reading guide (headings/anchors unchanged)
- CHECK wording: "the same provincial constraint set produces it on both maps" -> "Both maps were drawn under the same provincial constraints."
1. Brief Finding 4 "Northwest Calgary" vs README corrected 2026-07-08 to north/east/central
2. Brief threshold section puts Finding 2 (votes-based) under Lane 2 (structural)
3. Brief supermajority: 60+ seats change electoral rules w/o opposition vs en.ts stakes.q3 no two-thirds rule
4. Brief Cochrane "75 km from Nolan Hill" (~20 km)
5. README dependency graph 263/413 vs 234/454
6. README Ch2 p=0.0025 then 0.0024
7. README Version A p=0.0303 (round 1) vs current 0.0348
8. README "every test committed before results" vs brief: partisan channels exploratory, SZAT registered after results
9. README sixth row direction depends on attribution vs Open questions says no longer applies
10. chair flagged four boundaries (README) vs "7 configurations" (brief)
11. EG "41x" (brief) vs "40x" (README); Airdrie "about 85,000" vs 85,805
12. Brief calls gerrymander "unconstitutional" under US law vs Rucho
## voice-pld2 (1d22781e)
1. §6.1 Airdrie 85,805 = 1.56x average (over +25%) yet single district "legally valid"
2. §6.2.3 p=0.102 "more extreme than about 10%" -> ~90%; "close to the center"
3. §6.2.1 "positive = NDP advantage" vs sign convention (positive = UCP)
4. §6.2.5/H2 48.3% called UCP seat share at p99.99; Phase 4C 0.4831 = NDP fraction (UCP 0.5169)
5. §5.4.4 Run #4 rural-UCP missing vs Run #3 urban/suburban missing
6. §5.4.9 "s.15(2) disabled... EDs fall below -25%" vs §5.4.2 uniform ±25%
7. §5.9.1 "the proposal the government ultimately accepted — the minority map" vs GM37 set both aside
8. §5.9.4.3 Olds (5) "high-engagement"; Red Deer (23) omitted
9. §5.9.4.5 "all five listed limitations" vs four
10. §5.9.4.6 "388 non-neutral rows" vs "30% neutral/contextual"
11. §6.2.6 falsifier logic inverted
12. Directional Pattern: declination "disagrees with other three" — stale after A10
13. §8 "~90% confidence" Monte Carlo relies on retired blend-model check
14. §5.9.7 EBCA "decennial census" vs 2026 census as next baseline — check
15. §5.4.1 "median of 10,000 legal maps" vs 1,010,000
- §7 first entry last sentence "The audit does (a) correctly" looks erroneous
