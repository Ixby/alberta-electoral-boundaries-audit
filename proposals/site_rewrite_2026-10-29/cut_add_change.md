# Cut, add, change

Written 2026-10-29 against the working tree at `a5ff46e`. These lists go with `rewrite_draft.md`, which is the accepted text. Each item is one line, with its key or section reference. Where a caveat leaves the main page, its new home is named.

## CUT

1. **The whole smoking-gun frame** (`body.casings.frame_p1`, `frame_p2`, `frame_p3`, `frame_p4`, `frame_p5`, `beat_*_d`). It argues the negative first. The no-proof point survives in the verdict box (`box_cant_*`) and on `/law`.
2. **All 15 refrains** (`refrain`, `refrain_not_even`, `c2_refrain` … `c14_refrain`, `rev_refrain`). Pure repetition (497 words of scaffold with the beat labels). Nothing load-bearing is lost.
3. **The five beat labels** (`beat_found`, `beat_show`, `beat_experts`, `beat_canada`, `beat_gun`) from the main page. The template survives on `/evidence` under plain names.
4. **`frame_routes`.** The nav does this job.
5. **`picture.lead`.** It spends 79 words saying the picture can't be judged yet.
6. **The duplicate stakes figure** in `#the-scorecard` (`body.clean.stakes_fig_*`). The figure appears once, in "How we know".
7. **`the_map.p1`.** Filler.
8. **`the_map.p5`.** Unsupported claim (fix #15).
9. **`act1_intro`, `act2_intro_p1` (its first sentence), `act3_intro`, and the `act*_h` act headings.** The act structure is gone. "Same room, same rules" is reused in "What happened".
10. **`editorial_reflect.intro_p1`, `intro_q1`–`q3`, `intro_p2`.** They promise questions the audit never measures ("Where does your MLA live?").
11. **`editorial_reflect.you_p`, `community_p`.** Replaced by one explorer link and the Airdrie school example.
12. **`editorial_reflect.municipality_p`.** Overclaim; contradicts `c9_found` (fix #7).
13. **`editorial_reflect.province_p`.** Contradicts `c6_found` on the 60 seats (fix #2). The margin point lives in "What it buys".
14. **`body.casings.rev_p1`, `rev_p2`, `rev_litany_intro`, `rev_found` … `rev_gun`.** The scorecard re-run through five questions only restates. `rev_gun`'s "sample size of one" caveat moves to `/methods` [verify it is there; add if not].
15. **`body.clean.super_lead`'s supermajority framing.** It sets up a stake that `super_body` then dismantles. Its "the structural evidence carries most of the weight" caveat moves to "What the machine can't see".
16. **`body.casings.c1_experts` … `c14_experts` and `rev_experts`** from the main page. 14 of 15 cite no source. Keep them on `/evidence` only if each gets a citation; otherwise cut.
17. **The `c*_canada` beats that say "Nothing", "None" or "Not applicable"** (`c5`, `c7`, `c9`, `c10`, `rev`). Empty by construction.
18. **`november.context_label` + `context_body`.** "Not part of the statistical findings" tells readers to skip the section that matters this week.
19. **`authors_view.p10`'s checklist sentences.** Duplicates "The November test"; its last three sentences stay.
20. **`body.casings.c10_experts`'s "it is a fingerprint".** Forensic metaphor.
21. **`c1_found`'s "the largest Alberta city without its own MLA"**, until verified against the 2019 map (fix #16).
22. **`c3_title` / `c3_found`'s "a quarter too big / a quarter larger".** Unsupported by the stated numbers (fix #8).
23. **`c6_found2`'s "the UCP could lose the popular vote by 0.3 points".** Ambiguous arithmetic. The 49.7% vote share it rests on stays.
24. **Dead strings, after a dynamic-key check** (about 9,500 `en.ts` words are referenced by no literal key; upper bound). Examples: `verdict.headline`, `verdict.p_*` (now reused), `why_redrawn.*`, `stakes.q1`–`q3`, `editorial_intro.*`, `body.cpd.*` (most), `body.litmus.*` (most), `commission_split.intro`/`finding1`/`finding2`/`finding4`/`closing`, `november.anomalous_p1`–`p2`. Cutting them shrinks what translators are asked to translate.

## ADD

1. **"What the law requires, and what it doesn't"** (main page, about 600 words, plus `/law` depth). The skeleton is in `rewrite_draft.md` §3; the coordinator fills it from the legal research.
2. **"What would change our mind"** as a plain-language section title over the retraction conditions (`retractions.*`). It turns the conditions into reader-facing terms.
3. **"The results" slot** (`results.*`), hidden until the scoring. It holds: the release date; the X1 verdict for each of (a)–(d); the process checks; the committee map as a third column in the results table; and a link to the scoring file.
4. **`hero.status`.** The one lead sentence that changes after scoring, with its replacement template written in advance.
5. **`week.strip`.** A "This week" line under the hero, removed or rewritten after the scoring.
6. **A can't-say row from `c12_gun`:** "That the government directed its nominees. The audit found no evidence of coordination." The lead now names who nominated whom, so this caveat must sit right beside it.
7. **A `/evidence` page.** The 14 findings in full, renamed to plain headings, with the §5 fixes applied. Keep `#casing-N` anchors there, plus a hash redirect from `/#casing-N`, so shared links survive.
8. **A `/fixes` page.** The current `section-8` in full: advance votes, Lesser Slave Lake, census timing, and `banff_p` fixed. The main page keeps a 60-word teaser.
9. **The results table: one table, both maps, both kinds of test**, built from `impact.table_*`, `t5_*`, `c6_found`, `c7_found` and `c8_found`. It replaces three overlapping tables.
10. **"Where the audit lost":** one box listing every adverse result, from `c5`, `c7`, the `c9` mechanism test, `c10` and the `c8` Fisher retirement.
11. **One clause explaining 1,147 against ~1,340 submissions** (fix #13). [verify which universe each number covers]
12. **The Banff "undercut" verdict next to the chair's "bad faith" quote**, wherever the quote appears (`ledger_r3_c` into `c2` and `banff_p`).
13. **`explainers` back-links renamed** from "Re-read Casing N" to the new `/evidence` headings.
14. **Optional, Wuff's call:** name the minority-report authors. `commission_split.intro` (unrendered) names Dr. Julian Martin and John D. Evans. The rewrite uses roles only.

## CHANGE

1. **`hero.h1`, `hero.subtitle`.** Academic title out; finding plus date in (rewrite §0).
2. **`verdict.box_cant_2`.** Absorbs `legal_body` in one line ("Canadian law has no such category…").
3. **`frame_p1b` → "What happened".** Rebuilt with the TL;DR facts from `tldr_p1`–`p3`.
4. **`epigraph.*` + `the_map.p2`–`p4` → one map caption** under the cover image.
5. **`c1_found`, `c3_found`, `c4_found`, `c2_found` → shorter "What the minority map does" items.** Every figure is kept.
6. **`c6_found`, `c6_found2`, `super_body` → "What it buys"** (~200 words, down from 1,123).
7. **`c8_*` → "What 1 in 568,000 means"** (~110 words, down from 492).
8. **`c9_found` → split.** Robustness goes to "Did the result survive attack?"; the failed mechanism test goes to "Where the audit lost".
9. **`c11_found`, `c12_found`, `ledger_intro` → "Both sides tested".** The ledger table stays verbatim.
10. **`c13_found` + `november.intro` + `intro_b` → "How it got here".** One account of who chairs the panel and who drafts the map (fixes #3, #4).
11. **`glossary.advisory-panel`.** Replace "A fifth seat … went unfilled" with `intro_b`'s account: the judge was declined, and O'Ferrall was appointed chair later (fix #3).
12. **`editorial_canada.p6`.** "To choose between them" is wrong; the committee is drafting a new 91-seat map (fix #5). The text moves to `/law`.
13. **`editorial_history.*`, `editorial_canada.*`, `november.framework_p1`–`p3` → `/law`.** Soften `framework_p2`'s "the evidentiary record a s.3 applicant would need to assemble".
14. **`november.r5_*`.** Kept, with light tightening of `r5_p1`, `r5_c` and `r5_p3`. It also moves from section-7 to "How it got here", keeping its anchor `#recommendation-5`.
15. **`playbook_p1`, `playbook_p2`, `process_scorecard`, `r5_test` → "The November test".** It moves up from word ~12,470 and becomes the climax.
16. **`authors_view.*`.** Trimmed from 993 to about 500 words. `p5`'s "the map they draw" becomes "the map they approve" (fix #4).
17. **`about_me.p1`–`p2`.** Uses Wuff's disclosure ("voted for and donated to both conservative and progressive provincial parties in Alberta as an adult") and keeps the NDP volunteering from `frame_coi` [Wuff to confirm]. It replaces `p2`'s "wrote down my predictions before looking at the results", which overstates the record against `about_me.p3`.
18. **`retractions.conditions_intro`.** Reconcile "three of the six independent structural dimensions" with the five structural tests named everywhere else (fix #11). [verify against `analysis/methodology/retraction_pathway.md`]
19. **`retractions.c5_what`.** Point to `/norms`, where the Quebec argument actually lives (fix #17).
20. **Structural count wording** (`tldr_p2`, `act1_table_close`, `t5_r2_b`, `details2_p`, `framework_p2`). One phrasing everywhere: "4 of 5; the fifth, anchoring, is neutral for both maps" (fix #11).
21. **The 69-map wording.** Use "exceed" everywhere (`tldr_p2` "award as many", `super_lead`/`t5_r2_c` "reach") (fix #12). [verify ≥ vs > against the chain CSV]
22. **The efficiency-gap percentile.** "94th" everywhere (`details2_p` says 94.5th) (fix #19).
23. **`suggestions.banff_p`.** Drop "where no one lives"; add the ledger's "undercut" verdict (fix #14).
24. **`body.resources.heading`.** Rename "Technical Appendix" to "Reports and code".
25. **The `SECTIONS` array and analytics ids in `+page.svelte`.** Must change with the new structure; `observeSections` keys follow.
26. **Every non-English locale.** Each is keyed to `en.ts`, so the rewrite invalidates them. Out of scope now; flagged once.
