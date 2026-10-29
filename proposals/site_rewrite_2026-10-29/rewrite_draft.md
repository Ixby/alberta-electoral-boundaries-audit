# Rewrite draft: new main page (revision 4)

**Revision 4 (2026-10-29, voice pass).** The author chose first person ("I") over "the audit" as narrator. Sentences were made plainer: no paragraph-ending punchlines, no "What X is…" openers, no repeated "pen" motif, no invented Airdrie parent-group example, and no restating of the November 2 deadline in the hero. Facts, numbers, quotes and the block structure are unchanged, so the `en.ts` keys and page markup did not move; renamed headings keep their old anchor ids (`gen_home.py` SUB_IDS). The committee is now named: the Select Special Committee on Electoral Boundaries (the name the author supplied from the Assembly's committee page). One claim was dropped rather than reworded: that a 29-member opposition would be "too small to force recorded divisions" (no source was found for it, and the Standing Orders' threshold for a recorded division has not been checked). The author's view is unchanged and awaits the author's own rewrite. The source comments below still describe revision 2's sourcing and remain valid for every fact.

Drafted 2026-10-29 against the working tree at `a5ff46e`. Status: accepted by Wuff for implementation; this is the text that ships.

Revision 2 adds:
- the finished law section, built from `legal_framework.md`;
- the committee and motion facts;
- the 1992 precedent;
- *Lalande*;
- the reframing of "gerrymander";
- X1(d) scored on evidenced consideration;
- a trimmed "How we know".

**How to read this draft.** Each paragraph is followed by an HTML comment giving a proposed `en.ts` key and the sources that every number, date, name and quote was copied from.
- "Adapted" means the wording changed and the facts did not.
- `LF` means `legal_framework.md`, by section or table row, with the status it carries there.
- `T6` marks case law on SESSION_HANDOFF's pending-counsel-review list.
- `[verify: …]` marks anything not confirmed.

**Metaphors.** There are no forensic metaphors. The 14-item list is called "the full record".

---

<!-- ==================== 0. HERO ==================== -->

# Alberta's Electoral Map, Audited
<!-- key: hero.h1 | new -->

Alberta's boundary commission split in 2026 and filed two maps. I compared both with 1.01 million neutral maps drawn by computer. The majority's map looks like them. The minority's favours the UCP more than almost all of them.
<!-- key: hero.subtitle | src: verdict.p_split, verdict.p_answer, verdict.p_howfar, top_callouts.tldr_p2 -->

The committee map that replaces both is due Monday, November 2, 2026. This page will score it within 72 hours.
<!-- key: hero.status | THE ONE SENTENCE THAT CHANGES. After scoring: "The committee's 91-seat map, released [date], [meets / fails] Recommendation 5 and [repeats / does not repeat] the minority map's pattern. [Link: The results.]" | src: LF B4 / G49 (committee report due Nov. 2, VERIFIED-SECONDARY); playbook_p2 ("within 72 hours"); weekday computed -->

**This week.** I registered the November tests before the committee's map existed (OSF registration qsgy8), and I'll publish the scores whichever way they point. The first check is the one the government picked: [Recommendation 5](#recommendation-5).
<!-- key: week.strip | src: playbook_p1, playbook_p2, r5_p1, r5_h. After scoring: "This week: the results are in. [link]" -->

---

<!-- ==================== 1. WHAT HAPPENED ==================== -->

## What happened

Every so often Alberta redraws its ridings, the districts that each elect one MLA. Where the lines go can decide which party wins a seat.
<!-- key: happened.p1 | src: verdict.p_what, frame_p1b -->

On March 23, 2026 the independent commission doing the redraw split three to two and filed two maps. Both are legal under the Act. The chair and the two commissioners nominated by the opposition wrote the majority map. The two commissioners nominated by the government wrote the minority map. Both worked from the same rules, data and 1,147 public submissions.
<!-- key: happened.p2 | src: frame_p1b, commission_split.intro, c12_found, act1_intro -->

The majority map looks like the maps a neutral process draws. The minority map doesn't:
- It splits Airdrie, a city of 85,805, into four districts, and leaves its residents a minority in every one.
- In north-east and central Calgary, where the NDP won thirteen of seventeen seats in 2023, it draws districts 11.5% above the provincial average.
- At a perfectly tied vote it gives the UCP 51.7% of the seats. Only 69 of 1,010,000 neutral maps give more.
- On 2023's actual votes it yields 60 of 89 seats for the UCP, against 55 on the majority map.
<!-- key: happened.p3 | src: tldr_p2, c1_found, c3_found, c6_found -->

The Assembly adopted neither map. On April 21 it passed Government Motion 37, which handed the job to the Select Special Committee on Electoral Boundaries: six MLAs, four UCP and two NDP, chaired by UCP MLA Brandon Lunty. The committee's 91-seat map is due November 2. CBC has reported that there will be no public hearings on it, and no draft released for the public to comment on first.
<!-- key: happened.p4 | src: LF B4, G43, G46 (GM37 passed April 21; six members; VERIFIED-SECONDARY via the Assembly committee page); november.intro ("Neither commission map is in force"); c13_found (CBC). "Motion 19 … 44 to 36" removed (LF G45, UNVERIFIED). -->

### What I can say, and what I can't

I can say:
- The minority map falls outside what 1.01 million neutral maps produce, in the UCP's favour.
- All four partisan-fairness measures lean the same way.
<!-- src: verdict.box_can_1, verdict.box_can_2 -->

I can't say:
- That any commissioner meant to do this. My tests measure what a map does, and they can't show motive.
- That the government directed its nominees. I found no evidence of coordination, and appointing someone is not evidence of it.
- That the pattern will happen again. The map that has it was never enacted. November will show whether it comes back.
- How a court would rule, or what the committee will choose.
<!-- src: verdict.box_cant_1, c12_gun, playbook_p2 ("one map that was never enacted"), verdict.box_cant_3. box_cant_2 ("isn't a category Canadian law recognizes") removed per Wuff's framing instruction; see "On the word". -->

**On the word.** Gerrymandering means drawing lines for partisan advantage. You recognise it by what a map does and by what is known about how it was drawn. Canadian law has no offence by that name, so a court won't rule on gerrymandering as such, but that doesn't mean it can't happen here. The closest legal test is effective representation under section 3 of the Charter, covered below.
<!-- key: verdict.on_the_word | src: Wuff's framing instruction via coordinator 2026-10-29; body.clean.legal_body ("everyday political sense — manipulating electoral boundaries for partisan advantage"); LF D10 (no gerrymandering test; s.3 effective representation) -->

**Reading the cover map.** The cover colours Alberta's 4,765 voting areas by how people in each one voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are. The colour only deepens where lots of people live, so a voting area covering hundreds of square kilometres of parkland stays pale. The land west of Ponoka is pure white because it has no polling station and nobody was recorded living or voting there. The lines on top are the minority map's 89 proposed districts. [Open the map explorer](/explorer) to switch between all three maps.
<!-- key: map.caption | src: the_map.p2, the_map.p4, epigraph.author_p1, epigraph.author_p2, hero.cover_note -->

---

<!-- ==================== 2. WHAT THE MINORITY MAP DOES ==================== -->

## What the minority map does

The two maps agree on most of Alberta. Where they differ, here is what the minority map chose and what each choice does.
<!-- key: does.intro | src: act1_intro -->

### One city, four districts

Airdrie has 85,805 people (2024 municipal census), one city council and one school division. The law caps each district at one-and-a-quarter times the provincial average, so Airdrie needs at least two districts. The majority map gives it two.

The minority map gives it four: north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie. Each piece is joined to a different rural or Calgary-edge district, and Airdrie's residents are a minority in all four. The split meets every criterion of my pre-registered cracking test. The majority's two-way split meets none.
<!-- key: does.airdrie_p1 | src: c1_found -->

Splitting a community so thinly that it can't decide any of its seats is called cracking. Airdrie would have four MLAs, and most of the voters who elect each one live outside Airdrie.
<!-- key: does.airdrie_p2 | src: c1_show (adapted), c3_show -->

### Bigger districts where the NDP is strongest

In Calgary's north-east and central districts, where the NDP won thirteen of seventeen seats in 2023, the minority map's districts average 11.5% above the provincial average population. The majority's average 2.8%. A bigger district means each vote in it counts for less. Putting one party's voters into fewer, larger districts is called packing, and this pattern meets my pre-registered packing test.
<!-- key: does.calgary_p | src: c3_found, c3_show -->

### Unequal district sizes

Equal district populations are the one value Alberta's law puts a number on. By the commission's own population tables, the minority map's districts are off the ideal size by 4,707 people on average, compared with 3,180 on the majority map, a spread 48% wider. My own measurement on the official map files shows the same thing (3,938 against 2,827), and only about 1 in 100 neutral maps spreads its populations wider. So the usual defence of odd lines, that they were needed to balance populations, doesn't work here.
<!-- key: does.spread_p | src: c4_found, c4_show -->

### Rural tails on urban districts

I'm not saying rural Alberta has too many seats. The Act lets district populations vary by up to 25%, so one rural MLA doesn't have to cover an area the size of southern France. Both maps use that room.

But in several places the minority map attaches rural communities to a district whose population centre is in a city. Each of Airdrie's four pieces runs out into a different stretch of countryside, and in every one the district's population centre falls in the urban part. That happens on the minority map in places where it doesn't on the majority.
<!-- key: does.rural_p | src: editorial_reflect.region_p2, editorial_reflect.region_p3 -->

### Three boundaries the chair called out

The commission's chair flagged three of the minority's boundaries as geographically anomalous:
- the Rocky Mountain House–Banff Park extension into uninhabited national-park land;
- the lasso-shaped corridor of Calgary-Nolan Hill–Cochrane;
- the reach of Olds–Three Hills–Didsbury into north Airdrie.

The chair signed the majority report, so you would expect him to criticise only the minority. But my geometry tests, which were run without knowing which boundaries he had flagged, independently confirmed three of his four geometric flags.
<!-- key: does.chair_p1 | src: c2_found, ledger_r1_c -->

He called the park extension "a bad faith effort" to claim a population protection, section 15(2), that is written for remote communities where people actually live. My check undercuts that charge, because the division qualifies under s.15(2) even without the extension. Putting the Banff townsite with Canmore makes sense as a community of interest, because the town sits inside a national park it can't grow into. His objection to the empty-park extension still stands, and the townsite's placement doesn't affect it.
<!-- key: does.chair_p2 | src: c2_found, ledger_r3_c, c2_experts -->

### The seat advantage

At a perfectly tied province-wide vote, this is the UCP's share of seats on each map:
- the median neutral map gives 44.8%;
- the majority map gives 46.1%, the 78th percentile;
- the minority map gives 51.7%, the 99.99th percentile, and only 69 of 1,010,000 neutral maps exceed it.

On the minority map the UCP keeps the 45 seats it needs for a majority even if its vote share falls to about 49.7%. On the majority map it would need to win the popular vote by about 4 points. On 2023's actual votes the minority map yields 60 of 89 seats, against 55.
<!-- key: does.buys_p1 | src: c6_found, c6_found2, act2_intro_p2 -->

Sixty seats is a two-thirds majority, but in Alberta that doesn't unlock any special power. A simple majority can already pass laws and budgets, invoke closure, change the rules of the House and set every committee's membership. Sixty seats would give the government a cushion. A few floor-crossings couldn't threaten it, and a smaller opposition would have fewer members to keep up committee scrutiny.
<!-- key: does.buys_p2 | src: body.clean.super_lead, body.clean.super_body -->

None of these choices breaks Alberta's law. The Act allows splitting cities, and every district on both maps is inside the ±25% band. Canadian law has no rule against partisan advantage as such. Its test is whether voters get effective representation.
<!-- key: does.legal | src: c1_gun, c3_gun, c4_gun; LF D10. Reworded so that "lawful" does not read as "not a gerrymander" (Wuff's framing instruction). -->

---

<!-- ==================== 3. WHAT THE LAW REQUIRES ==================== -->

## What the law requires, and what it doesn't

### The Constitution

Section 3 of the Charter gives every citizen the right to vote, which the Supreme Court of Canada reads as a right to effective representation. Roughly equal voting power is the starting point, a "prime condition", though strict equality isn't required. A district can be bigger or smaller for a real reason, such as geography, community history, shared local interests or a minority community's voice, but the difference has to be justified.
<!-- key: law.charter_p1 | src: LF A1 (Charter s.3 text VERIFIED-PRIMARY via repo; Reference re Prov. Electoral Boundaries (Sask.) [1991] 2 SCR 158, effective representation, "prime condition", factors: VERIFIED-SECONDARY); T6 (Saskatchewan Reference pinpoints pending; no pinpoint used) -->

Courts give legislatures a lot of room here. They ask whether reasonable people, applying those principles, could have drawn the lines this way. No government can switch the right off, because the notwithstanding clause doesn't apply to section 3.
<!-- key: law.charter_p2 | src: LF A1 (Raîche, 2004 FC 679, summarising Carter: VERIFIED-SECONDARY; s.33 per Justice Canada and Ontario (AG) v. Working Families, 2025 SCC 5: VERIFIED-SECONDARY); T6 (Carter) -->

Courts have also looked at how a map gets made. In 2017 Nova Scotia's Court of Appeal found the province's map violated section 3, because the government had directed its independent commission to change course and the final map didn't reflect the commission's own view. The court added that a legislature may still draw a map itself.

In 2026 the Supreme Court of Canada struck down a Quebec law that paused Quebec's commission to protect ridings in the Gaspésie (*Quebec (AG) v. Lalande*, 2026 SCC 13, 7–2, reasons May 1). Quebec could have protected them more narrowly, and the fact that the law passed unanimously didn't save it. On June 12, 2026 Quebec's National Assembly passed its own 127-seat map.
<!-- key: law.process_p | src: LF A2, C5, C8, G22 (2017 NSCA 10), G26 (Lalande), G27 (Quebec act of June 12, 2026): all VERIFIED-SECONDARY; judgments not read -->

### Alberta's statute

The *Electoral Boundaries Commission Act* sets the commission's rules:
- **Who sits.** A chair appointed by cabinet from eligible roles that include judges. Four non-MLA members, two nominated by the Premier and two by the Opposition, appointed by the Speaker.
- **Hearings.** Public hearings before and after its draft map.
- **Deadlines.** A draft within seven months, and a final report within five months after that.
- **Seats.** 89. Bill 32, introduced April 23, 2026, would make it 91. [verify: passage and assent not found]
- **Population.** Every division within 25% of the average. Up to four remote divisions may go as low as 50% below, if the commission finds at least three of five criteria met.
- **Factors.** The commission must consider effective representation, and may weigh growth, communities of interest, geography and other factors.

Both commission maps fit inside these rules.
<!-- key: law.statute | src: LF B1, B2 (EBCA ss.2(1), 6(1), 7(1), 8(1), 13, 14, 15(1)–(2): VERIFIED-PRIMARY via repo); LF B3, G42 (Bill 32 introduced April 23, 2026: VERIFIED-SECONDARY; passage UNVERIFIED); c1_gun, c4_gun -->

### What the law doesn't require

Most of that rulebook is addressed to "the Commission". Read plainly, it doesn't bind the Legislature or a committee of MLAs unless the committee's motion adopts it. Whether Government Motion 37 does isn't public.
- The Legislature doesn't have to adopt a commission's map. A report becomes law only if MLAs pass a bill.
- I found no provision that requires a committee of MLAs to hold hearings, be independent, publish a draft or explain its choices. Government Motion 37 reportedly says the review is expedited and does not require public hearings.
- Recommendation 5, which the government cited, binds no one.
- Elections Alberta says it needs at least a year and a half to prepare new ridings. That's a planning need, and no law makes it a deadline.
- Courts don't review a law while it's being made. A challenge can only come after a boundaries law passes.
<!-- key: law.not_required | src: LF §0 item 6, B4 (rules addressed to "the Commission": VERIFIED-PRIMARY text; the reading is the memo's analysis; GM37 full text not seen); LF D1, D3, D4, D7, D8, D9, D11; G43 (GM37 "expedited", "would not require public hearings", via search summary: [verify against the motion text]); G50 (Elections Alberta "at least 1 1/2 years": VERIFIED-SECONDARY); G30 (Mikisew Cree, 2018 SCC 40: VERIFIED-SECONDARY, applied by analogy) -->

### It has happened here before

In 1992 Alberta's commission deadlocked over mixed urban–rural ridings. On July 2, 1992 the Assembly passed Motion 24, handing the work to a Select Special Committee of MLAs chaired by Bob Bogle. The Opposition refused to appoint members, so four Progressive Conservative MLAs drew the map. It was used in the 1993 election.

In 1994 the Court of Appeal upheld that map under the Charter but criticised how it was made. The committee's members couldn't explain several of its boundaries and district populations, and one of the smallest districts was Bogle's own. The court said a proper review was needed before the Legislature's term ran out. In 1995 the Legislature rewrote the Act and created the commission model used ever since, which is the model set aside in 2026.
<!-- key: law.precedent | src: LF §0 item 1, C2, G16, G19, G21 (VERIFIED-SECONDARY; the 1994 details are weak: Wikipedia and Alberta Views; the 1994 judgment was not read); coordinator fact note 2026-10-29. Four PC MLAs (Bogle, Stockwell Day, Pat Nelson, Mike Cardinal) per the search summary of the 1993 election page; LF G19's 'seven-MLA' is the committee's size with the Opposition's seats unfilled [verify]. Bill 20 (1995) per LF C2 'Aftermath' (VERIFIED-SECONDARY). -->

### What this means in November

The committee's map can still be challenged in court. It faces the same test as any map: effective representation, with every population gap justified. Reasons matter, and Alberta's Court of Appeal criticised the last committee-drawn map for not giving them. I'm scoring the map and the process. Whether it's constitutional is up to a court.
<!-- key: law.november | src: LF §F ("What this means in November"), C2 (VERIFIED-SECONDARY, weak) -->

---

<!-- ==================== 4. HOW IT GOT HERE ==================== -->

## How the committee got the job

The commission did its work in public. It held hearings in sixteen communities, received 1,147 written submissions, and reversed its own interim proposal based on more than 80 of them.
<!-- key: system.p1 | src: c13_found -->

Four weeks after the split, Government Motion 37 (introduced April 16, passed April 21, 2026) created the Select Special Committee on Electoral Boundaries, with six MLAs:
- four UCP: Brandon Lunty (chair), de Jonge, Sawyer and Wiebe;
- two NDP: Ganley and Gray.

The committee oversees an Independent Advisory Panel, which drafts the 91-seat proposal. In June the committee appointed four panel members: the Hon. Monte Solberg and Darwin Durnie, nominated by the Premier, and Dr. Gerard Kennedy and Brent Robinson, nominated by the Opposition.

Alberta's acting chief justice declined the committee's request to help find a judge to chair the panel, citing "the irregularity of this process". The Alberta branch of the Canadian Bar Association and the Law Society of Alberta also declined to take part. Retired Court of Appeal justice Brian O'Ferrall was later named chair. The panel's role is advisory, and the decisions belong to the committee's MLAs. The committee's UCP members also declined to release the submissions the committee received, citing privileged information. An NDP amendment to release them with privileged material removed was defeated 3–2 [cite: video of the committee's October 28, 2026 meeting, Rocky Mountain Room, 10:29 a.m. to 12:15 p.m., supplied by the author; transcript pending]. The panel was due to report to the committee by October 22. Its report is now before the committee, but its map has not been made public.
<!-- key: system.p2 | additions: the submissions vote per Wuff via coordinator 2026-10-29 [cite: CEB transcript, date]; the Oct. 22 panel deadline per LF B4, G49 (VERIFIED-SECONDARY) and the coordinator's search (no public sign of delivery as of Oct. 29). The contacts-disclosure motion is left out for word budget. | src: LF B4, G43, G46, G47, G48 (all VERIFIED-SECONDARY: Assembly committee page and transcripts; Assembly news release of June 9, 2026; Bow Island Commentator; CTV); november.intro, intro_b (panel members); c13_found ("the panel advises … decide"). Applies coordinator fix 2: "Motion 19" and "five MLAs, three UCP" removed. -->

In May, Duane Bratt, Professor of Political Science at Mount Royal University, described the process to me as without precedent in Canada, and I repeated that on this site. That was wrong. Alberta did it in 1992, when a deadlocked commission's work went to a committee of MLAs, PC members alone drew the map after the Opposition refused to take part, and the Court of Appeal later criticised the result. My mistake was the scope of my review, which never looked at Alberta's own 1992 cycle.

2026 differs from 1992 in one important way. The commission didn't deadlock. A majority signed a report, and under the Act a majority report is the commission's report. Government Motion 37 set it aside anyway.
<!-- key: system.p3 | Nenshi quote REMOVED 2026-10-29 (academic report C17): search coverage of the Lethbridge Herald, Apr. 1, 2026, ties "never been done before in Alberta history" to the government-nominated commissioners' minority report, two weeks before Government Motion 37, so it is not a claim about the committee route and 1992 does not answer it; no Hansard instance found. src: Bratt: consented in May 2026 to be named and quoted for "described the process as without precedent in Canada" (said in a conversation with the author; his title per his email signature); EBCA s.9 (VERIFIED-PRIMARY via repo); LF §0 item 1, C2 (VERIFIED-SECONDARY, weak). Per Wuff 2026-10-29: refute both claims. Courtesy: tell Bratt before publishing. The finding3 point that a commission report "changes nothing until the legislature passes a separate Electoral Divisions Act" now lives in law.not_required. Replaces finding3's "without precedent" sentence and the Bratt attribution (coordinator fix 3; see fixes table #22). -->

On the floor, the government presented its route as following the commission: "We are adopting the recommendations from the report" (Government House Leader, Hansard, April 16, 2026). The opposition called it "retaliation against the independent Electoral [Boundaries Commission]." The report itself doesn't fully support the government's claim. The majority asked the Legislature to adopt its 89-seat map, and the one recommendation that proposed 91 seats came from the chair alone.
<!-- key: system.p4 | src: c13_found, c14_show. [verify: the Hansard quote is the repo's own transcription, findings/hansard_april16_motion19.md; LF flags that file's motion number as unverified, not the quote] -->

Every step was lawful. But this time the MLAs who approve the map will also run in it, and nothing stops a future government of any party from citing this cycle as precedent.
<!-- key: system.p5 | src: c13_gun, authors_view.p5 (adapted), c14_show -->

### Recommendation 5: what the government cited
<!-- key: november.r5_h | anchor: #recommendation-5 -->

The government's justification for handing the job to a committee was one recommendation in the commission's report, so it's the first thing to check when the committee's map comes out. The chair, Justice Dallas Miller, wrote Recommendation 5 alone, in an addendum to the majority report: "My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation" (final report, p. 66). He also stated its purpose: it "is formulated for the express purpose of dissuading the Legislature from accepting the minority report."
<!-- key: november.r5_p1 | src: r5_p1 -->

It's a fallback, and a specific one. If the Legislature wouldn't accept the majority's choice to remove two divisions outside Edmonton and Calgary, the chair asked it to amend the *Electoral Divisions Act* from 89 seats to 91, restore those two divisions, and keep "the rest of the province as we propose" (the majority map) "to the extent possible." Restoring the two divisions should:
<!-- key: november.r5_p2 | src: r5_p2 -->

- **(a) Leave Airdrie and the south alone.** No change to any division in Airdrie, or with any land south of Airdrie's southern city limit, except Drumheller-Stettler. On the majority map that is 41 divisions: both Airdrie seats, all 28 Calgary seats, and the 11 divisions around and south of Calgary.
- **(b) Leave north Edmonton alone.** No change to any Edmonton division north of the North Saskatchewan River: 11 divisions on the majority map.
- **(c) Put south Edmonton back.** Every Edmonton division south of the river returns to the commission's October 2025 interim map, the draft it published for comment before the final split. The committee may add Nisku to Edmonton-South East if it wants Leduc and Beaumont back in one division. That is 10 divisions.
- **(d) Consider a Clearwater seat.** Consider restoring a division made mostly of Clearwater County and western Mountain View County, with s.15(2) status. This is the only restored seat the recommendation places. It names no place for the second.
<!-- key: november.r5_a–r5_d | src: r5_a, r5_b, r5_c, r5_d -->

Together, the conditions rule out most of the ground the commission split over. Airdrie, Calgary, Cochrane and Chestermere, where the four-way Airdrie split and the Calgary-edge hybrids are, all fall under condition (a). Red Deer and St. Albert are covered only by the softer clause, "to the extent possible." A map that reopens Airdrie or Calgary may still be lawful, but it isn't the map Recommendation 5 describes. Government Motion 37 itself reportedly lets the panel apply the recommendation "subject to any modifications the independent advisory panel considers necessary." The [map explorer](/explorer) shades the two areas Recommendation 5 changes and draws a dashed line around the two it leaves alone.
<!-- key: november.r5_p3 | src: r5_p3; LF B4, G44 (GM37 "subject to any modifications…": VERIFIED-SECONDARY from a partisan source; exact motion text not seen [verify]) -->

---

<!-- ==================== 5. HOW WE KNOW ==================== -->

## How we know

### How the neutral maps were drawn

A computer drew 1,010,000 legal Alberta maps from the official Elections Alberta files, each with its districts inside the population band and in one piece. The method, ReCom, is the standard one in this field. It merges two neighbouring districts, splits the result at random into two new legal ones, and repeats. The computer never sees a vote. Where a real map's numbers fall among the million shows how unusual it is.
<!-- key: know.machine_p1 | src: act2_intro_p1, body.clean.howmcmc_mcmc, body.clean.howmcmc_recom -->

My commitments are filed on the Open Science Framework. The random seeds were locked to a public beacon before the official map files existed, and [the Methods page](/methods) labels each finding pre-registered or exploratory.
<!-- key: know.machine_p2 | src: body.clean.prereg_body (trimmed) -->

### In Alberta, neutral is not 50/50

Rural UCP voters win their ridings by wide margins, like 60-40, which wastes a lot of extra votes. Urban NDP voters win theirs by closer margins, like 51-49. So at a perfectly tied vote, the median neutral map gives the UCP only 44.8% of seats. Both maps are measured against that baseline.
<!-- key: know.baseline_p | src: act2_intro_p2 -->

### The results, side by side

| Test | Majority map | Minority map |
|---|---|---|
| Follows municipal lines (Canadian norm 70–85%) | 80%: within norm | 72%: within norm |
| Population spread from ideal size (commission tables) | 3,180 | 4,707: 48% wider |
| NE/central Calgary districts above provincial average | 2.8% | 11.5% |
| Boundaries flagged by the commission's chair | 0 | 3 |
| Airdrie split (legal minimum: 2) | 2 pieces | 4 pieces |
| **Pre-registered structural summary** (4 of 5 or more = outlier) | **0 of 5** | **4 of 5** (the fifth, anchoring, is neutral for both maps) |
| UCP seat share at a tied vote (neutral median 44.8%) | 46.1% (78th percentile) | 51.7% (99.99th percentile; 69 of 1,010,000 exceed it) |
| Mean-median gap | 1st percentile: an outlier, but leaning the NDP's way, the wrong direction to help the UCP | deeper in the tail than 99.97% of neutral maps, leaning the UCP's way |
| Declination (a second lopsidedness measure) | 22nd percentile: inside the normal range | deeper in the tail than 98.8%, leaning the UCP's way |
| Efficiency gap (pre-set line about +4.1%) | +0.1% (16th percentile) | +4.0% (94.5th percentile): a miss |
| UCP seats on 2023 votes | 55 of 89 | 60 of 89 |
| Odds of this profile under neutral drawing | n/a | at most about 1 in 568,000 |
<!-- key: know.table_* | src: body.impact.table_r1–r6, t5_r2_b, c6_found, c8_found; fairness-measure rows and percentiles from reports/public/report_public.md table (l.358–366), which carries the majority's 1st-percentile mean-median outlier that t5_r1_c ('inside the normal range on every measure') omits -->

The structural tests use geometry only, and all five were pre-registered on April 24, 2026, before the final simulation results were compiled. The 2019 enacted map sits beside the majority, at a 46.0% tied-vote seat share (78th percentile).
<!-- key: know.table_note | src: act1_table_close, details2_p, c6_found -->

*[Figure: stakes_quadrant, shown once.]* Partisan skew runs left to right, and failed structural tests run bottom to top. The 2019 map and the 2026 majority map sit in the safe corner. The minority map sits by itself in the outlier region.
<!-- key: know.fig_caption | src: stakes.scorecard_fig_caption (trimmed); alt: stakes.scorecard_fig_alt -->

### What "1 in 568,000" means

The chance that a neutral process produces the minority map's combined profile across the four fairness measures is at most about 1 in 568,000 (p ≤ 1.76×10⁻⁶, a Bonferroni-corrected, dependence-robust upper bound). I doubled the raw figure because I looked in two places, so the real chance is at most this, and probably smaller.

That figure isn't the probability that the map is innocent. Treating it that way is the prosecutor's fallacy. A map this rare can still come from unusual but honest judgment. My claim is only that ordinary drafting variation isn't a plausible explanation.
<!-- key: know.odds | src: c8_found, c8_experts, c8_gun -->

### Checking with a second method

I swapped the simulation's engine for a structurally different one, a spanning-forest sampler registered in advance at OSF (he53s) and run on 2026-07-10. Every metric's percentile moved by less than one point. A separate implementation, the R redist package, also found zero plans reaching the minority's value.
<!-- key: know.robust | src: c9_found -->

### Limits of the simulation

The simulation enforces population and contiguity, but not every rule the commission weighed (s.15(2), community of interest, municipal anchoring). It's a strong outside check rather than a list of every map a lawful commission might draw, so the geometry tests, which don't use the simulation, carry most of the weight. The tied-vote test isolates what a map contributes on its own. A big enough swing in a real election can still outweigh any map's lean.
<!-- key: know.limits | src: c6_gun, body.clean.super_lead -->

### What didn't hold up

Some tests came back against my findings. They stay on the page.
- **The anchoring test came back neutral.** The minority map follows municipal lines 72% of the time and the majority 80%, and both are inside the 70–85% Canadian norm.
- **The efficiency gap missed.** The minority came in at +4.0%, the 94.5th percentile. The pre-registered line was the 95th (about +4.1%), so I report it as a miss.
- **The mechanism test failed.** I tested whether the flagged shapes produce the seat advantage, and on my test they don't. The shapes and the seat numbers point at the same map, but the link between them didn't hold up.
- **The minority passed one test outright.** On neighbour-drain, which looks for packed districts next to thin-margin ones, it shows 1 coupled signal, against the majority's 2 and the 2019 map's 5.
- **I retired two statistics.** The Swing-Zone Allocation Test fell from p = 0.0024 to p ≈ 0.19 once corrected for neighbouring areas voting alike, and I retired it on 2026-06-13. The one-in-fifteen-million headline combined two channels that weren't independent, and I retired it on 2026-06-10.
<!-- key: lost.items | src: c5_found, c7_found, c9_found, c10_found, c8_found -->

### Both sides tested

I ran every written accusation from either side through the same tests. None of these checks was set up in advance, so they carry less weight than the five structural tests. Every number behind them is public.
<!-- key: sides.intro | src: ledger_intro (trimmed) -->

| The accusation | Who made it | What I found |
|---|---|---|
| Three of the minority's boundaries are geometrically anomalous | The chair (majority report) | Largely confirmed: my blind tests independently confirmed three of the chair's four geometric flags; the fourth fell below threshold |
| The minority's seven contested configurations had "no public support" | The chair (Appendix C) | Overbroad: right on three of seven, wrong on three, partially wrong on one |
| The park extension was "a bad faith effort" to claim s.15(2) protection | The chair (final report, p. 10) | Undercut: the division qualifies under s.15(2) even without the flagged extension |
| The majority "delete[s] or mangle[s] rural electoral divisions" | The minority (p. 356) | Reversed: the minority keeps fewer rural-anchored divisions (23 vs 28, against 2019's 31) and absorbs more into city-named districts (7 vs 3) |
| The majority "decline[d] to use" the ±25% flexibility in rural Alberta | The minority (p. 356) | Supported: majority rural divisions average −6.0% deviation (4 below −10%); the minority's average −12.2% (11 below −10%) |
| "Substantial and consistent testimony" for hybrids was ignored | The minority (p. 356) | Overbroad: support was configuration-specific, documented for three of seven hybrid configurations and absent for three |
| The majority's rural districts are engineered corridors of isolation | My own counter-hypothesis (T3.2) | Not supported: the geographic explanation held, and the majority cleared |
<!-- key: sides.table | src: ledger_r1–r7 (verbatim) -->

The minority's published reasons for its contested lines mostly fail on public data: five of six don't survive an independent check. Usually the general claim is true and the specific line isn't. About a third of Cochrane's workers commute somewhere in Calgary, but that says nothing about the Nolan Hill neighbourhood the corridor reaches. The majority published no such list, so this check only runs one way. Taken together, the minority's two charges against the majority describe two different approaches: more but fuller rural divisions on the majority map, and fewer but lighter ones on the minority map.
<!-- key: sides.p | src: c11_found, c11_note, c12_found. The chair's "no public support" result sits in the table row; its archive size (~1,340) is moved to /evidence pending fix #13. -->

### Who did this

I'm the only author, a self-funded student at Mount Royal University, and I've voted for and donated to both conservative and progressive provincial parties (more under About me). Findings that went against what I expected stay on the record, and every number can be reproduced from public code, public data and random seeds committed in public before the analysis ran.
<!-- key: who.p | src: author's disclosure via coordinator 2026-10-29; frame_coi (NDP volunteering; reproducibility). [confirm with Wuff: NDP volunteering] -->

### The full record

All fourteen findings are on [the full record](/evidence), each with its numbers, what it could show, what Canadian practice expects and what the law does with it. Each one links to a short explainer on [the explainers page](/explainers).
<!-- key: record.p | src: body.casings.appendices_note (adapted). "Why it falls short of legal proof" removed per Wuff's framing instruction. -->

---

<!-- ==================== 6. THE NOVEMBER TEST ==================== -->

## The November test

The committee's 91-seat map is due November 2, 2026. I registered the November tests (OSF registration qsgy8) before the committee's map existed. I'll publish the scores within 72 hours of the map's release, whichever way they point.
<!-- key: test.p1 | src: playbook_p1, playbook_p2; LF G49 (Nov. 2) -->

**The process.** Were public hearings held? Was a draft released? Are the advisory panel's members and terms of reference published? Is the record behind the map public? The committee has kept its submissions private, so I can only score the reasons for its lines from what its report publishes. The process also gets its own nine-feature scorecard, published in draft on [the norms page](/norms#measurable). Four of the committee's failing cells are features it can still add before it reports.
<!-- key: test.process | src: playbook_p1, process_scorecard. [verify: the panel's four members are already public (Assembly release of June 9, LF G47); mark that part of the check as met if so] -->

**Recommendation 5.** Test X1 scores the committee's map against the chair's four conditions, one at a time:
- (a), (b) and (c) pass if the map leaves those divisions as described.
- (d) asks only that a Clearwater seat be considered, so it's scored on evidenced consideration. It passes if the map contains the division, or if the committee's published report names the option and gives a reason for adopting or declining it. With the submissions withheld, the report is the only record that counts. Silence or boilerplate fails.

X1 passes only if all four do. I'll also report a strict reading, which fails (d) unless the seat exists. Recommendation 5 binds no one in law, so X1 tests whether the committee delivered what the government cited.
<!-- key: test.r5 | src: r5_test (adapted); LF §H3–H4 (recommended rule: ADOPTED / CONSIDERED-WITH-REASONS / NOT SHOWN, strict reading as a sensitivity line), LF D8; coordinator instruction 6. [process: log this scoring rule as a dated entry in findings/pre_registration_amendment_log.md BEFORE the map lands, per SESSION_HANDOFF] -->

**The map.** Where does it land on every measure on this page, against the same million-map distribution and under the same pre-registered thresholds?
<!-- key: test.map | src: playbook_p1 -->

**What each outcome means.** If the committee's map repeats the minority map's pattern, drawn by different people under different constraints on a different timeline, the structural finding becomes confirmatory. If it lands inside the neutral bands, the finding stays an isolated observation about one map that was never enacted, and I'll say so here. Either way, the arithmetic is public and you can check it yourself.
<!-- key: test.outcomes | src: playbook_p2 -->

### The results
<!-- key: results.* | SLOT, hidden until scoring: release date; X1 verdict for each of (a)–(d), with (d) as ADOPTED / CONSIDERED-WITH-REASONS / NOT SHOWN, plus the strict-reading line; process checks; the committee map as a third column in the results table; link to the scoring file. Then update hero.status and week.strip. -->

---

<!-- ==================== 7. WHAT WOULD CHANGE OUR MIND ==================== -->

## What would change my mind

Every finding has a condition, written in advance, that would retract it. If one is met, I'll publish the retraction within 30 days.
- **Someone draws a better-justified map.** If anyone produces a legal Alberta map that satisfies the minority's own stated reasons for Airdrie, Cochrane, Nolan Hill and Rocky Mountain House–Banff Park, and follows municipal lines about as often as the majority's, I'll retract the finding that those boundaries can't be explained by their stated reasons. The challenge is open at [Issue #14](https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14).
- **A document shows the reasons came first.** If an internal commission document, dated before the minority's final choices, shows those choices were driven by community submissions I haven't seen, I'll retract the inference that they were drafting decisions.
- **The neighbour-drain pass turns out to be an artefact.** If the continuous version of that score falls in the extreme upper tail (p < 0.05) of random permutations, I'll withdraw the minority's pass.
- **An election contradicts the simulation.** If the 2027 election is fought on either commission map and the actual seat split contradicts the projection from 2023 votes, I'll revisit the simulation's percentile findings against the actual results.
- **A court distinguishes *Lalande*.** In *Quebec (AG) v. Lalande*, 2026 SCC 13, the Supreme Court struck down Quebec's law pausing its commission, and Quebec then legislated its own map. If a court reviewing Alberta's route finds it constitutionally different, for example because handing a finished commission's work to an MLA committee isn't the same as freezing a commission mid-process, I'll retract the argument on [the norms page](/norms) that the two belong in the same class.
<!-- key: mind.items | src: retractions.conditions_intro, retractions.c1–c5; LF G26, G27 (Lalande, the June 12 act: VERIFIED-SECONDARY). Condition 5 updated for the decided case (coordinator fix 4). [verify: the norms page's Quebec contrast (quebec_p1/p2) is now outdated per LF E; update it in step] -->

The November map can also weaken the overall conclusion, as described above. I correct mistakes in public and don't delete them. Every correction is listed in the [academic report's Documented Corrections section](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md).
<!-- key: mind.close | src: playbook_p2, retractions.corr_light_intro. The compound "three of six dimensions" condition is held back pending fix #11. -->

---

<!-- ==================== 8. THE AUTHOR'S VIEW ==================== -->

## The author's view

Everything above is the audit. Delete this section and not one number changes. This section is an opinion, signed, severable and mine.
<!-- key: authors_view.preamble (trimmed) -->

Start with the two facts I cannot make innocent. Government-nominated commissioners drew a map that neutral map-drawing almost never produces: fewer than a hundred matches in a million draws. And when the commission split rather than endorse it, the government did not ask why. It took the pen.
<!-- key: authors_view.p2 -->

Each fact has an innocent reading. A commissioner can be eccentric in good faith. A legislature can lose patience with deadlock. But put the facts in sequence and the innocent readings strain. A government wanted a certain kind of map. The independent route did not deliver one. A route was found that would.
<!-- key: authors_view.p3 -->

Here is what alarms me. No law was broken; I checked, and that checking is most of what this audit is. The statute makes the commission's report advisory. It sets no notice period. It requires no draft, no hearings, no consultation. The guardrail was never law. It was a habit, and habits only bind governments that choose to keep them. Alberta learned that once, in 1992, and rebuilt the guardrail in 1995.
<!-- key: authors_view.p4 (trimmed; last sentence added from LF C2, G21: VERIFIED-SECONDARY) -->

The committee that replaced the commission is six MLAs: four government, two opposition, and a government chair. There is an advisory panel, chaired by a retired judge, after the province's acting chief justice declined to help find one. But advisers advise. The votes belong to the MLAs, and the map they approve is the map they will run in. It will face no public hearing. It arrives finished.
<!-- key: authors_view.p5 (facts updated: six MLAs, four UCP, per LF G46; the acting chief justice, per LF G48; "draw" → "approve"). [confirm with Wuff: factual edits inside the signed opinion] -->

And this government has been here before. Its first bill, as written, would have let cabinet rewrite laws without the legislature; that power was stripped after the outcry, not before. Its own ethics commissioner found the Premier breached the conflicts law by pressing her attorney general about a criminal case. It passed a law letting cabinet repeal local bylaws and trigger the removal of elected councillors. And when a court paused one of its laws in December 2025, it invoked the notwithstanding clause. Every one of those moves was lawful. Every one spent a norm to get past an independent check.
<!-- key: authors_view.p6 (trimmed; authors_view.sources unchanged) -->

I worry about what the map buys. On recent voting patterns, the minority map's geometry yields sixty seats of eighty-nine. That is not a mandate. It is insulation: from floor-crossings, from committees, from any opposition large enough to sustain scrutiny. I would worry about that insulation in any hands.
<!-- key: authors_view.p9 (trimmed) -->

I could be wrong. Unlike most opinions about this government, mine ships with the terms of its own destruction. The committee's map is due November 2, and the tests were locked before it existed. If it lands inside the neutral bands, my suspicion took real damage, and this site will say so within seventy-two hours, because I committed to that before I knew the answer. That is the difference between an opinion and an accusation. An opinion tells you what would change it.
<!-- key: authors_view.p10 (checklist removed) -->

— Will Conner
<!-- key: authors_view.signed; authors_view.sources unchanged, plus the 1992 sources from LF G19 and G21 if p4's last sentence stays -->

---

<!-- ==================== 9. BACK MATTER ==================== -->

## Fixes for next time

Two problems make every audit of Alberta's maps harder than it needs to be. About half of all votes now come in before election day, and Elections Alberta reports them by division rather than by voting area, so roughly 395,000 NDP and UCP votes cast in 2023 can't be placed on a map. Commissions also draw from census data that's already years old by the time a map takes effect. Both problems can be fixed, and [the proposals page](/fixes) explains how.
<!-- key: fixes.teaser | src: suggestions.intro, suggestions.advance_p1, suggestions.census_p1 -->

## About me

I'm a student at Mount Royal University. I did this research on my own: it was not assigned as coursework, and the university did not commission it. My views are my own and do not represent the university. I have no connection to Elections Alberta or the commission. I've voted for and donated to both conservative and progressive provincial parties in Alberta as an adult.

My political history could affect how I look at this issue, and the main protection against that is the method. I tested both maps the same way, registered my tests in public, time-stamped records, labelled every finding pre-registered or exploratory, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I want to know.
<!-- key: body.about_me.p1–p2 | src: about_me.p1, about_me.p2, author's disclosure via coordinator 2026-10-29, frame_coi (NDP volunteering), body.clean.prereg_body. [confirm with Wuff: NDP volunteering] -->

<!-- Unchanged: about_me.p3–p4, references.*, resources.* (heading renamed "Reports and code"), translation_about.* -->

---

## Fixes applied

| # | Fix | Where |
|---|---|---|
| 1 | Party disclosure in Wuff's own words. The NDP volunteering is kept from `frame_coi`; **Wuff to confirm** | "Who did this", "About me" |
| 2 | 60 of 89 stated as tested on 2023 votes | "What it buys" |
| 3 | One account of the panel chair (acting chief justice declined; O'Ferrall named later) | "How it got here" |
| 4 | The panel produces the proposal and the MLAs decide; "draw" → "approve" | "How it got here", "The author's view" |
| 5 | "To choose between them" not carried over | (absent) |
| 6 | `finding3` facts reused, minus its precedent sentence (see #22) | "How it got here" |
| 7 | `municipality_p` overclaim cut | (absent) |
| 8 | "A quarter too big" dropped | Calgary section |
| 9 | "Five legal reasons" gone; the law section replaces the eight scattered lessons | Law section |
| 10 | Adverse results listed, not counted | "Where the audit lost", "Who did this" |
| 11 | One structural count ("4 of 5, anchoring neutral"); the "six dimensions" compound condition held back pending a check | Results table, "What would change our mind" |
| 12 | "Exceed" used for the 69 maps | Lead, "What it buys", table |
| 13 | ~1,340-submission archive size moved off the main page pending a check; 1,147 kept | "Both sides tested" |
| 14 | Banff: "undercut" verdict included | "Three boundaries the chair called out" |
| 15 | `the_map.p5` dropped | Map caption |
| 16 | "Largest city without its own MLA" dropped | Airdrie section |
| 17 | Quebec condition points to /norms | "What would change our mind" |
| 18 | Broken references pointer not carried over | (absent) |
| 19 | Efficiency gap at the 94.5th percentile throughout (the public and academic reports' p94.54), majority at the 16th | Table, "Where the audit lost" |
| 20 | T6 marked on Saskatchewan Reference sentences; *Cassista* not used | Law section comments |
| 21 | **Committee facts (coordinator fix 2).** Six members (four UCP, two NDP, named), created by GM37, introduced April 16 and passed April 21, 2026. "Motion 19", "44 to 36" and "five MLAs / three UCP" are removed everywhere, including the author's view | "What happened", "How it got here", "The author's view" |
| 22 | **Precedent (coordinator fix 3).** "No precedent" replaced by "It has happened once before, here", with the 1992 committee and the 1994 Court of Appeal criticism. **The Bratt attribution is dropped.** The site attributes to him an assessment that the move is "without precedent among the Canadian redistribution cycles this audit reviewed", and Alberta 1992 contradicts that. Re-scoping it to "other provinces" would change what he is quoted as saying without his confirmation. Restore a scoped version only if Wuff re-confirms the wording with him | Law section, "How it got here", "The author's view" p4 |
| 23 | **Quebec (coordinator fix 4).** *Lalande*, 2026 SCC 13 (7–2, reasons May 1) and Quebec's June 12 127-seat act added. The contrast now cuts both ways (a legislature can't derail a commission disproportionately; it may still legislate a map). Retraction condition 5 is rewritten for the decided case. The /norms Quebec contrast is flagged as outdated | Law section, "What would change our mind" |
| 24 | **Framing (coordinator fix 5).** Removed `box_cant_2` ("isn't a category Canadian law recognizes") from the can't-say list. Added "On the word": a practice identified by effects and evidence; the missing legal category limits what a court will call it, not whether it happened. "Every one of these choices is legal … partisan effect is not a harm" reworded to "none breaks the statute … the law's test is effective representation". "Why it falls short of legal proof" removed from "The full record". The stop condition is kept and now rests on the real limits (effects not intent; never enacted; November tests recurrence), stated as a new can't-say row | Verdict box, "On the word", "What the minority map does", "The full record" |
| 25 | **X1(d) (coordinator instruction 6).** Scored on evidenced consideration (adopted, or named with a reason; silence or boilerplate fails), reported per condition, with the strict reading alongside; R5 described as a fidelity test, not law. **Needs a dated entry in `findings/pre_registration_amendment_log.md` before the map lands** | "The November test", "The results" slot |
| 26 | GM37's reported "subject to any modifications the independent advisory panel considers necessary" added, so the yardstick is described fairly [verify: motion text] | Recommendation 5 |
| 27 | **Submissions withheld.** The committee's UCP members declined to release the submissions, and an NDP amendment to release them with privileged material removed was defeated 3–2 [cite: video of the committee's October 28, 2026 meeting, Rocky Mountain Room, 10:29 a.m. to 12:15 p.m., supplied by the author; transcript pending]. Used in "How it got here" and in the November test's process half and X1(d) rule. The voting rule is not asserted: "six members (four UCP, two NDP)" only. The panel's Oct. 22 deadline is added; the contacts-disclosure motion is left out for word budget | "How it got here", "The November test" |

**Count note.** Visible words: comments, headings and markdown are stripped; table cells are counted.

| Section | Words |
|---|---:|
| Hero + "This week" | 94 |
| What happened | 516 |
| What the minority map does | 774 |
| What the law requires, and what it doesn't | 674 |
| How it got here: the pen moved | 794 |
| How we know | 1238 |
| The November test | 348 |
| What would change our mind | 302 |
| The author's view | 498 |
| Fixes for next time | 76 |
| About me | 140 |
| **Total** | **5454** |
