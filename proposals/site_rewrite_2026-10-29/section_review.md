# Section-by-section prose review

Reviewed 2026-10-29 against the working tree at `a5ff46e` (this includes the coordinator's new `finding3` and the `november.r5_*` block).

**How words were counted.** I resolved every `t(lang.current, '…')` key in render order, stripped HTML, and split on whitespace. Nav and `*_aria` strings are excluded; a repeated label counts every time it renders. The main page totals **17,222 words**. Sub-page counts strip script, style and comment blocks from the `.svelte` source, so they are approximate (±5%).

## The two meta-narratives

**Current.** "You came looking for proof of a gerrymander. Canadian law makes proof impossible, so here is the next best thing: fourteen pieces of evidence, each real, each ending with the legal reason it falls short. Add them up and the minority map is extreme, and the process that should have caught it was replaced. The system as written lets all of it through. November is the next test." The page's thesis is the gap between evidence and proof. Its unit is the evidence item, and its refrain is the negative ("a casing, not a gun", 15 times).

**Proposed.** "One of the two commission maps does what a gerrymander does, and the government's nominees drew it. When the commission would not adopt it, the pen moved to a committee the government controls. The law requires little of either step. Here is how we know, and where we were wrong. This week the committee's map is scored against tests locked before it existed, starting with the recommendation the government itself cited." The thesis is the effect, plus the test that could overturn the claim. The unit is the reader's question: what happened, how, what the law asks, how we know, what next.

**Where they diverge.**
1. **What comes first.** The current page leads with what cannot be proven (`frame_p1`, word ~250). The proposed page leads with what the map does.
2. **How the law is handled.** The current page threads eight legal lessons through fifteen evidence items. The proposed page gives the law its own section ("What the law requires, and what it doesn't") so it explains the system instead of deflating each finding.
3. **Where the climax sits.** The current page climaxes philosophically ("the gap the law chose to leave open", `rev_gun`) and treats November as an epilogue at word ~12,470. The proposed page makes November the climax and the place the claim can fail.

---

## Main page, in render order

### hero (98 words)
- **What it says.** A title ("Laws, Norms, & Statistics: An Audit of…") and a subtitle asking whether the two maps "treat voters the same way".
- **Current job.** Introduce three lenses and one neutral question.
- **How well.** Academic and finding-free. The subtitle asks a question the page takes ~1,000 words to answer: "do they treat voters the same way?"
- **Proposed job.** State the finding plus the date of the test, and carry the one sentence that changes after the scoring.
- **Verdict: CHANGE.** The best plain lead already exists unrendered in `verdict.p_answer`: "One of the two is. The other looks normal."

### epigraph (151 words)
- **What it says.** A reader objects that the colouring makes rural land look big. The author explains that the colour depth follows population.
- **Current job.** Pre-empt a cartographic objection before the argument starts.
- **How well.** Good prose in the wrong place: "It is blank precisely because land doesn't vote." It puts a map-reading lesson ahead of the reason anyone came.
- **Proposed job.** Caption block under the cover map.
- **Verdict: MOVE.** Into the map caption, merged with `the_map.p2`.

### the-smoking-gun (806 words)
- **What it says.** There is no smoking gun and there cannot be one. Here are fourteen "casings", the five-question template, the author's prior, two ways in, a legal-terminology note, and the can/can't box.
- **Current job.** Thesis statement and reading instructions for the whole page.
- **How well.** It argues the negative before any positive has been stated: "You came here looking for a smoking gun. This report does not have one." Two of its internal counts are wrong: "five legal reasons" against eight lessons, and "Two casings … point the wrong way" against five adverse results. `frame_p1b` (138 words) is the only paragraph that tells the story.
- **Proposed job.** `frame_p1b` becomes the core of the lead. The can/can't box stays under it.
- **Verdict: CUT the frame (`frame_p1`, `p2`–`p5`, the beat legend, `frame_routes`). CHANGE and keep `frame_p1b`, the verdict box and `frame_coi` (moved to "Who did this").** The metaphor is retired entirely.

### the-picture (366 words)
- **What it says.** A scatter plot of both lanes, then a TL;DR of the whole finding.
- **Current job.** "The picture, before the proof": show the conclusion, defer the argument.
- **How well.** The TL;DR (`tldr_p2`) is the clearest summary on the page. `picture.lead` spends 79 words saying the picture can't yet be judged: "right now you have no way to judge whether it means anything."
- **Proposed job.** The TL;DR content folds into the lead. The figure appears once, in "How we know".
- **Verdict: MOVE (the figure), MERGE (the TL;DR into the lead), CUT `picture.lead`.**

### the-map (307 words)
- **What it says.** How to read the cover map: voting areas, colour by vote, saturation by population.
- **Current job.** Make the stakes visible.
- **How well.** `p2`–`p3` are clear. `p5` overclaims: "most of the people live in areas that vote the other way". That is unsupported, and from memory (not checked here) the UCP won the 2023 province-wide vote.
- **Proposed job.** The map caption.
- **Verdict: MOVE `p2`–`p4` into the caption; CUT `p1` and `p5`.**

### act-1 intro (80 words)
- **What it says.** Act I uses geometry only. The two drafts came from the same room and the same rules.
- **Current job.** Introduce the evidence class.
- **How well.** Fine, but it only exists to serve the act structure: "Act I walks the lines themselves."
- **Proposed job.** None. "Same room, same rules" moves into the minority-map section opener.
- **Verdict: CUT** (one clause reused).

### casing-1, Airdrie (508 words)
- **What it says.** The minority splits Airdrie (85,805) four ways, each piece a minority; the majority splits it two ways.
- **Current job.** The first piece of evidence, plus legal lesson 1 (factors are discretionary).
- **How well.** `c1_found` is strong and concrete. `c1_show` adds a vivid PTA example. `c1_experts` is unsourced: "one of the primary red flags in the redistricting literature". `c1_found` also carries an unverified claim: "the largest Alberta city without its own MLA".
- **Proposed job.** The lead example of cracking.
- **Verdict: CHANGE.** Keep the facts at ~110 words. The legal lesson moves to the law section, and the "largest city" claim is dropped until verified.

### casing-2, the chair's three flags (453 words)
- **What it says.** The chair flagged three minority boundaries, called the park extension "a bad faith effort", and the audit's blind tests confirmed three of his four geometric flags.
- **Current job.** Insider evidence, plus lesson 2 (reports bind no one).
- **How well.** Admirably fair about the Banff townsite (`c2_experts`), but it runs as one 169-word sentence chain: "…(the fourth, Calgary-Foothills-Airdrie West, did not meet the audit's confirmation threshold; his published criticism covers seven boundary configurations in total)."
- **Proposed job.** The "odd shapes" item in the minority-map section, carrying the ledger's "undercut" verdict on "bad faith".
- **Verdict: CHANGE** (compress to ~120 words, keep the Banff fairness note).

### casing-3, Calgary (298 words)
- **What it says.** NE/central Calgary districts average 11.5% above the provincial mean on the minority map, against 2.8% on the majority.
- **Current job.** The packing evidence, plus lesson 3 (partisan effect is not a legal harm).
- **How well.** Crisp, but the title claim is unsupported: "One zone of Calgary, drawn a quarter too big". 61,225 against a majority-implied ~56,467 is about 8.5% larger, not 25%.
- **Proposed job.** The packing item.
- **Verdict: CHANGE** (drop "a quarter").

### casing-4, population spread (304 words)
- **What it says.** The minority's population spread is 48% wider, at the 99th percentile of neutral maps.
- **Current job.** "Worse at the one thing the law measures", plus lesson 4.
- **How well.** A good argument: "the minority map is worse at population equality than the majority drawn beside it." But it gives two figure pairs (3,938/2,827 and 4,707/3,180) without saying why.
- **Proposed job.** "The cost: vote equality."
- **Verdict: CHANGE** (explain the two measurements in one clause).

### casing-5, the retracted anchoring test (302 words)
- **What it says.** An early 15% anchoring figure was an artefact. On official files both maps sit inside the norm.
- **Current job.** Show the audit admits error.
- **How well.** Honest, and it adds a narrower surviving claim. The template forces empty beats: "Nothing — no Canadian statute or practice guide requires any particular anchoring rate."
- **Proposed job.** One bullet in "Where the audit lost".
- **Verdict: MOVE** (compress to ~45 words; full text to `/evidence`).

### act-1-picture (439 words)
- **What it says.** A bar chart and a six-row table of the structural tests.
- **Current job.** Summarise Act I.
- **How well.** The table is useful. The figure's alt text (130 words) and caption (127) nearly duplicate each other, and the close says "four of four" where the table says "4 of 5".
- **Proposed job.** Merged into the single results table.
- **Verdict: MERGE** (deduplicate the alt and caption; fix the count).

### what-this-means (1,011 words)
- **What it says.** An interlude at five scales (you, community, municipality, region, province) on why the lines matter.
- **Current job.** Bring the stakes to the reader's street.
- **How well.** Warm, but the questions it promises are never measured: "Where does your MLA live?" `municipality_p` overclaims: "the four statistical measures flag the same districts the structural tests flag". `province_p` contradicts Casing 6 on whether the 60-seat outcome was tested.
- **Proposed job.** Two lines in the minority-map section ("rural ridings with urban centres") plus the explorer link.
- **Verdict: CUT most.** Keep `region_p2` (rural Alberta does not have too many seats) and `region_p3` (urban heads, rural tails) in condensed form.

### history-of-gerrymandering (374 words)
- **What it says.** The 1812 origin of the word, then the US, UK and Australia.
- **Current job.** Context.
- **How well.** Clean and readable: "The cartoonist's pun, *Gerry-mander*, stuck." But it sits mid-argument.
- **Proposed job.** `/law` or a "where the word comes from" sidebar. One link from the main page.
- **Verdict: MOVE.**

### canada-is-different (561 words)
- **What it says.** Canada's test is effective representation, not one person, one vote. Other provinces insulate commissions; Alberta is the exception.
- **Current job.** Legal context.
- **How well.** Good comparative content. `p6` is factually wrong: the committee was created "to choose between them". It is drawing a new 91-seat map. `p7` points to a references section that does not hold what it promises.
- **Proposed job.** Seed content for "What the law requires, and what it doesn't".
- **Verdict: MOVE** (into the law section and `/law`; fix `p6`).

### act-2 intro (375 words)
- **What it says.** How the 1,010,000-map ensemble works, pre-registration, and why neutral in Alberta is 44.8%, not 50%.
- **Current job.** Method primer.
- **How well.** `act2_intro_p2` (neutral is not 50/50) is essential and well written. `p1` buries the idea under parameters: "(4 independent chains × 252,500 steps, base seed from the Cloudflare drand public randomness beacon, pre-registered at OSF before execution)".
- **Proposed job.** "The what-if machine" in "How we know".
- **Verdict: CHANGE** (parameters go to `/methods`).

### casing-6, the tied-vote seats (1,123 words)
- **What it says.** At 50/50, only 69 of 1,010,000 neutral maps exceed the minority's 51.69%. That is 60 of 89 seats on 2023 votes, a majority down to a 49.7% vote share, plus the supermajority discussion.
- **Current job.** The headline statistic, plus lesson 5.
- **How well.** The core numbers are the strongest on the site. The supermajority block sets up a stake ("a two-thirds supermajority requires exactly 60 seats") and then dismantles it ("no two-thirds threshold that unlocks special powers"). It is the longest item on the page.
- **Proposed job.** "What it buys" in the minority-map section, plus the results table.
- **Verdict: CHANGE** (about 1,123 → 220 words).

### casing-7, the efficiency-gap miss (375 words)
- **What it says.** The efficiency gap is +4.0%, the 94th percentile, under the pre-set 95th-percentile line. It is a miss.
- **Current job.** Show honest counting.
- **How well.** The figure caption is good. The beats pad it: "Nothing — no Canadian body uses the efficiency gap at all."
- **Proposed job.** One bullet in "Where the audit lost", plus a table row.
- **Verdict: MOVE.**

### casing-8, the 1-in-568,000 figure (492 words)
- **What it says.** The combined profile is at most 1 in 568,000 under neutral drawing. Why it was doubled, why it isn't the probability of innocence, and the retired 1-in-15-million figure.
- **Current job.** Explain and defuse the big number.
- **How well.** The content is right. The prose is the densest on the page: "The doubling holds no matter how the two channels relate — the exact objection that killed the old figure — and the four measures inside the simulation count as one look, not four…"
- **Proposed job.** "What 1 in 568,000 means." The retired figure goes to "Where the audit lost".
- **Verdict: CHANGE** (about 492 → 110 words).

### casing-9, attacks on the result (323 words)
- **What it says.** The sampler swap held, the software swap was moot, and the mechanism test failed.
- **Current job.** Robustness, plus an admitted failure.
- **How well.** Honest, but the robust result and the failure are tangled in one 181-word string: "Third, the mechanism test, which the audit's claim failed…"
- **Proposed job.** Split: the robustness result goes to "Did it survive attack?" and the failure to "Where the audit lost".
- **Verdict: CHANGE / SPLIT.**

### casing-10, signals the other way (533 words)
- **What it says.** The minority passed neighbour-drain. SZAT was retired after a spatial correction. The Fisher combination was retired.
- **Current job.** Adverse results.
- **How well.** Fair, but it uses a forensic metaphor ("it is a fingerprint"), and the SZAT box (136 words) is methods-page material.
- **Proposed job.** Bullets in "Where the audit lost".
- **Verdict: MOVE** (SZAT box to `/methods`).

### act-3 intro (45 words)
- **What it says.** Act III reads conduct, where intent is usually decided.
- **Current job.** Introduce the conduct evidence.
- **How well.** It teases a reveal that never comes: "Watch what happens to it here."
- **Proposed job.** None.
- **Verdict: CUT.**

### casing-11, the minority's reasons (494 words)
- **What it says.** Five of six of the minority's published rationales fail independent checks (Cochrane commuting, Chestermere, Red Deer–Sylvan Lake schools).
- **Current job.** Pretext evidence, plus lesson 6.
- **How well.** A careful, fair framing: "in most of these cases the general claim is true, and a boundary honouring it could have been drawn." At 247 words in `c11_found` it reads like a list without breaks.
- **Proposed job.** "Both sides tested": two sentences and a link.
- **Verdict: CHANGE** (compress; the symmetry note `c11_note` stays).

### casing-12, the split commission (608 words)
- **What it says.** Who nominated whom. The chair's "no public support" claim was right on only three of seven. The minority's two charges against the majority: one reversed, one supported.
- **Current job.** Institutional evidence and even-handedness.
- **How well.** The best fairness work on the site, buried in a 417-word single string: "Tested together, the two charges describe two design philosophies, not one vice."
- **Proposed job.** Who drew it goes to the lead (with the `c12_gun` caveat). The charges go to "Both sides tested".
- **Verdict: CHANGE / SPLIT.**

### ledger (379 words)
- **What it says.** A seven-row table of every written accusation, each tested.
- **Current job.** Symmetry.
- **How well.** The clearest table on the page. The intro over-explains: "This ledger is not a scorecard. Nothing in it gets added up…"
- **Proposed job.** "Both sides tested."
- **Verdict: KEEP** (intro trimmed to two sentences).

### casing-13, the commission replaced (476 words)
- **What it says.** The commission worked in public. Motion 19 (44–36) replaced it with a five-MLA committee: no hearings on the map, no draft, the panel advises and the MLAs decide.
- **Current job.** Process evidence, plus lesson 7.
- **How well.** Strong facts and quotes, but one 259-word string. Its claim that the committee will "draft a 91-seat map" conflicts with `november.intro` ("The committee itself does not draw the map").
- **Proposed job.** "The pen moved", in the system section.
- **Verdict: CHANGE** (fix the drafter wording).

### casing-14, the norm set aside (335 words)
- **What it says.** Sixty years of independent commissions, no reviewed precedent (Bratt), and conventions are unenforceable.
- **Current job.** Norm evidence, plus lesson 8.
- **How well.** `c14_show` has the page's best line on stakes: "Nothing prevents the next government, of any party, from citing this cycle as precedent." It also carries an abstraction: "the demonstration that the guardrail was a convention."
- **Proposed job.** The system section, with the precedent claim stated once.
- **Verdict: CHANGE.**

### the-scorecard (855 words before the playbook)
- **What it says.** "Fourteen casings. No gun." The scatter plot again, a summary table, a technical detail block, and the scorecard run through the five questions.
- **Current job.** The synthesis.
- **How well.** It restates rather than synthesises: "Now go back to the picture from the top of this page — you can read it now." The figure renders twice on the page, and the five-question litany is self-referential.
- **Proposed job.** The table merges into the results table, the figure appears once, and `details2_p` goes to `/methods`.
- **Verdict: CUT / MERGE.**

### playbook (278 words)
- **What it says.** The November test is registered (OSF qsgy8), has process and outcome halves, is scored within 72 hours, and both outcomes are stated.
- **Current job.** The epilogue.
- **How well.** Some of the clearest commitment language on the site: "the reader will not have to trust this audit's judgment — only its arithmetic." It is buried at word ~12,470.
- **Proposed job.** The core of "The November test", which becomes the climax.
- **Verdict: MOVE up and EXPAND.**

### section-7 intro + finding3 (265 words)
- **What it says.** A "context" label, the committee's structure, and the new `finding3`: no reviewed precedent, Alberta's reversed default, Motion 19, and the R5 justification.
- **Current job.** Process context.
- **How well.** The new `finding3` is accurate and tight: "A commission report here changes nothing until the legislature passes a separate *Electoral Divisions Act*." But the "CONTEXT … not part of the statistical findings" label tells readers to skip the section that matters this week.
- **Proposed job.** "The pen moved" and "Why the government's choice was lawful", in the system section.
- **Verdict: KEEP `finding3`, CUT the context label, MOVE.**

### section-7, R5 block (486 words)
- **What it says.** R5 in plain words: chair alone, its stated purpose, the trigger, 89→91, the four conditions with district counts, what they close off, and how X1 scores it.
- **Current job.** The yardstick for November.
- **How well.** The most useful new text on the site, plain and checkable: "A map that reopens Airdrie or Calgary may still be lawful. It is not the map Recommendation 5 describes."
- **Proposed job.** "Recommendation 5: the yardstick the government chose", in the system section, with X1 repeated in the November test.
- **Verdict: KEEP** (tightened about 15%; facts unchanged).

### section-7, framework (505 words)
- **What it says.** Section 3, the Saskatchewan Reference, *Raîche v. Canada*, and whether the committee could survive a s.3 challenge.
- **Current job.** Legal context.
- **How well.** Clear but lawyerly. `framework_p2` claims the audit's findings "are the evidentiary record a s.3 applicant would need to assemble". That is a legal judgement the site elsewhere says it doesn't make.
- **Proposed job.** Seed for "What the law requires, and what it doesn't".
- **Verdict: MOVE** (to the law section, pending the legal research; soften `p2`).

### authors-view (993 words)
- **What it says.** A signed opinion: the facts strain innocent readings; the guardrail was habit, not law; a pattern of norm-spending; 60 seats is insulation; terms for being wrong.
- **Current job.** Severable opinion.
- **How well.** The best-written section on the page, short sentences that land: "That is the difference between an opinion and an accusation. An opinion tells you what would change it." `p5` says "the map they draw", which conflicts with the panel-drafts account. `p10` re-lists the November checks.
- **Proposed job.** The same, after the November test.
- **Verdict: KEEP, TRIM** (to ~500 words; fix `p5`; cut the `p10` checklist).

### section-8, suggestions (1,265 words)
- **What it says.** Advance votes aren't mapped. Lesser Slave Lake and s.15(2). Banff. Wait for the 2026 census.
- **Current job.** Housekeeping and reforms.
- **How well.** Good material with an unfair passage: `banff_p` says "through Banff National Park, where no one lives" and repeats "bad faith" without the ledger's "undercut" verdict.
- **Proposed job.** A `/fixes` sub-page, with a 60-word teaser.
- **Verdict: MOVE** (fix `banff_p`).

### retractions (525 words)
- **What it says.** Five falsification conditions and a corrections pointer.
- **Current job.** Accountability.
- **How well.** Clear conditions, with two pointer errors: "six independent structural dimensions" (the page says five tests), and condition 5 points to a Quebec argument that lives on `/norms`.
- **Proposed job.** Becomes "What would change our mind", in plain language, with the formal conditions kept.
- **Verdict: CHANGE.**

### references, resources, contact, about-translation (434 words combined)
- **What it says.** Citations, links to reports, about the author, and the AI-translation notice.
- **Current job.** Back matter.
- **How well.** `about_me.p1` contradicts `frame_coi`: "no connection to … any political party" against having volunteered for the NDP. "Technical Appendix" mislabels a list that includes plain-language reports.
- **Proposed job.** Back matter.
- **Verdict: KEEP, CHANGE** (fix `about_me.p1`; rename "Technical Appendix").

---

## Sub-pages

### /norms (~2,100 words)
- **What it says.** It cross-examines the sixty-year norm: what it bought this cycle, the departure, the government's case at full strength, where that case bends, and the process scorecard.
- **Current job.** The norms lens.
- **How well.** Strong. It steel-mans: "An audit that only rehearses one side's outrage is not checking anything." It updates R5 accurately. It describes Airdrie and Calgary as locked under R5, so it agrees with the new `r5_a`.
- **Proposed job.** Unchanged, with the C13/C14 depth living here.
- **Verdict: KEEP** (light trim of material duplicated from the main page).

### /law (~1,450 words)
- **What it says.** Why the audit never rules "gerrymander", the Charter test, and the EBCA.
- **Current job.** The law lens.
- **How well.** Plain and exact: "A map cannot be found guilty of a category that does not exist."
- **Proposed job.** The deep version of the new law section. The legal research fills both.
- **Verdict: KEEP, EXPAND** (absorb `history-of-gerrymandering`, `canada-is-different` and `framework_p1`–`p3`).

### /methods (~2,000 words)
- **What it says.** The what-if machine, percentiles, the structural tests, the fairness measures, the odds, the tests that died, robustness and pre-registration.
- **Current job.** The statistics lens.
- **How well.** The best plain-language writing on the site: "If you can read a weather forecast, you can read this."
- **Proposed job.** It receives the ensemble parameters, the SZAT box and `details2_p`.
- **Verdict: KEEP.**

### /explainers (~3,050 words)
- **What it says.** Fourteen one-concept appendices (A–N), each with a confusion, a toy example and a limit.
- **Current job.** Teaching companions, one per casing.
- **How well.** Excellent pedagogy (Appendix A's town-of-40,000 example), but every appendix links back with casing language: "Now re-read Casing 1".
- **Proposed job.** Unchanged teaching. Back-links point to the new `/evidence` items.
- **Verdict: CHANGE** (rename the back-links; drop "casing").
