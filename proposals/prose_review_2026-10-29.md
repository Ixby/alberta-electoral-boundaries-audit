# English prose review: restructure around what's happening, how, and how we know

**Status:** Proposal — pending the author's call on §0 and the restructure
**Date:** 2026-10-29 14:00 MDT
**Scope:** English copy only (`viewer/src/lib/i18n/locales/en.ts` in render order, plus inline English on `/norms`, `/law`, `/methods`, `/explainers`). Translations ignored.
**Direction from the author:** good prose and storytelling outrank preserving the current section structure.

> **Spot-checked before filing (2026-10-29).** Confirmed against `en.ts` or the shapefiles: the
> `about_me.p1` / `frame_coi` contradiction; `province_p` "not yet directly tested" vs `c6_found`
> "60 of 89"; "thirteen of seventeen"; "55 on the majority map"; "49.7%" and "by about 4 points";
> "a quarter larger" in `c3_*`; the glossary's unfilled panel chair vs O'Ferrall as chair; and the
> 2019 map's **Airdrie-East** district (so #16 below is real). Edit 2's "69 … give the UCP more"
> inherits the reach/exceed ambiguity in #12; settle #12 before shipping it.
>
> **Already done in the same PR as this file:** the Recommendation 5 problems listed in §4 were
> fixed in `commission_split.finding3`, the new `november.r5_*` block, `/norms`, and the explorer
> (see §4's update note).

**How I counted words.** For the main page I resolved every `t(lang.current, '…')` key in render order, stripped HTML tags and entities, and split on whitespace. Nav labels and `*_aria` strings are excluded. A repeated label (the five beat headings, for example) counts each time it renders. For the sub-pages I stripped script, style and tags from the `.svelte` source, so those counts are approximate (±5%). Reading times assume 238 words per minute. That is a commonly cited adult average for non-fiction, quoted from memory rather than looked up this session, so read the minutes as rough.

---

## 0. Stop condition: the spine as stated overclaims

You asked for a site that shows "gerrymandering, how it's happening, and how we know." The evidence supports a narrower present tense than "is happening":

- The minority map carries a gerrymander's **effect signature**, but it was never enacted. Neither commission map is law (`top_callouts.tldr_p1`).
- The audit measures outcomes, not intent (`verdict.box_cant_1`).
- The audit's own pre-registered fallback, frozen before the November map existed, says: "If it lands inside the neutral bands, the finding stands as an isolated observation about one map that was never enacted" (`body.casings.playbook_p2`). A headline saying "gerrymandering is happening" would contradict the audit's registration in the very week that registration gets tested.

**The spine I recommend, which is still blunt:**

1. **What's happening.** The government's nominees drew a map with a gerrymander's signature. When the commission would not sign it, the pen moved to a committee the government controls. Its map lands November 2.
2. **How it works.** Cracking, packing, lopsided district sizes, and a legal system with eight gaps that let all of it through.
3. **How we know.** 1,010,000 neutral maps, tests locked in advance, and every place the audit lost.

If the November map repeats the signature, the present tense is earned: the audit's own rule gives the finding "confirmatory status" (`playbook_p2`). Write the lead so that one sentence changes on November 5, not the whole page.

---

## 1. Diagnosis

### D1. The page argues the wrong thesis first

The first sentence of the body is `body.casings.frame_p1`: "You came here looking for a smoking gun. This report does not have one." It sits about 250 words into the page. The first statement of an actual finding is `verdict.box_can_1`, at roughly word 1,000. The headline number ("1 in 568,000", `top_callouts.tldr_p2`) first appears at word 1,271, about 5 minutes in.

From there the structure keeps arguing a negative. Fifteen sections (14 casings plus the scorecard) each end on a "not a gun" refrain. "Gun" appears 35 times on the page and "casing" 64 times. The legal impossibility of proof is a real finding, but it is the fourth thing a reader needs, and the page makes it the first.

### D2. The template outweighs the evidence

The main page runs about **16,900 words** (about 71 minutes at 238 wpm). The four sub-pages add about 8,900 more (`/norms` ~2,200, `/law` ~1,500, `/methods` ~2,100, `/explainers` ~3,100).

Every casing is forced through the same five questions. Beat labels, refrains and "Know more" stubs alone come to **497 words** of repetition. The template also manufactures empty beats:

- "What the experts say" names an expert or source in **1 of 15** instances. Only `c13_experts` cites anyone (CCLA). The others are unattributed assertions under a label that promises attribution. Example, `c1_experts`: "Community splitting is one of the primary red flags in the redistricting literature". No literature is named.
- "What Canadian practice expects" is effectively empty in **7 of 15** instances: `c5_canada` "Nothing —", `c7_canada` "Nothing —", `c9_canada` "None of this is required by anyone", `c10_canada` "Not applicable", `rev_canada` "Nothing —", and `c6_canada` and `c8_canada` both open "No Canadian…".

### D3. The urgent content is buried and split four ways

The November test is the reason Recommendation 5 matters this week. Its details first appear at **word ~12,470** (`body.casings.playbook_p1`, roughly 52 minutes in). Recommendation 5 first appears at **word ~12,860** (`body.commission_split.finding3`). The test is described in four places:

- `playbook_p1`/`p2`, inside the scorecard section;
- section-7 "The Lunty Committee", which labels itself "CONTEXT … not part of the statistical findings" (`november.context_body`);
- `november.process_scorecard`, which points to `/norms`;
- `authors_view.p10`, which re-lists the checks inside the signed opinion.

A reader who stops at 10 minutes never learns that the map lands this week.

### D4. The same facts are restated three to five times

- The stakes scatter plot renders twice (`#the-picture` and `#the-scorecard`), with two different alt texts and two captions totalling 174 words.
- The "4 of 5 structural / 69 of 1,010,000 / 1 in 568,000" triple is restated in `tldr_p2`, `act1_table_close`, `t5_r2_b`/`t5_r2_c`, `details2_p`, `rev_p2`, `rev_found` and `framework_p2`.
- "Sixteen communities / 1,147 submissions / 80-plus" appears in `c13_found`, `authors_view.p5` and `/norms`.
- The "no precedent" claim with the Bratt attribution appears in `c14_found`, `finding3` and `/norms`. "Sixty years" appears in `frame_p1b`, `c14_title`, `c14_found`, `authors_view.p8` and `/norms`.

### D5. The sentences are built to defend rather than to tell

- Single strings run very long: `c12_found` is 417 words, `finding3` 287, `c13_found` 259, `c11_found` 247, `c8_found` 218.
- Asides nest inside asides, as in `c8_found`: "…so the odds are multiplied by two before being quoted. The doubling holds no matter how the two channels relate — the exact objection that killed the old figure — and the four measures inside the simulation count as one look, not four…"
- "Not X, it's Y" reversals do the heavy lifting: "What it found is not a gun. It is casings" (`frame_p2`); "That gap … is not a loophole the audit failed to close. In Canada, it is the system as written" (`frame_p2`); "It is not that a law was broken" (`authors_view.p4`); "That is not a mandate. It is insulation" (`authors_view.p9`).
- Abstract nouns do the work of verbs: "the demonstration that the guardrail was a convention" (`c14_show`).

The sub-pages are better written. `/methods` opens: "If you can read a weather forecast, you can read this." The main page duplicates their content in a heavier voice.

### D6. Internal contradictions undercut a site that sells self-correction

There are 20 of these, listed in §5. The worst four would each hand a hostile reader a quote:

- `body.about_me.p1`: "I have no connection to … any political party". `body.casings.frame_coi`: "He has donated to the NDP and volunteered for the party."
- `editorial_reflect.province_p`: whether the map pushes past 60 seats at real vote shares "is a question this audit has not yet directly tested". `c6_found`: "On the actual 2023 voting patterns, the minority map's geometry awards the UCP 60 of 89 seats." `authors_view.p9` says the same.
- `editorial_reflect.municipality_p`: "the four statistical measures flag the same districts the structural tests flag". The four measures are whole-map numbers and flag no districts. Separately, `c9_found` reports that the geometry-is-the-mechanism test failed.
- `commission_split.finding3`: "The process now promoting the minority map". That asserts the outcome the November test exists to measure.

### D7. Each casing mixes all three lenses

Each casing runs law, norms and statistics at once. Readers cannot follow one thread, and the legal thread (eight numbered "Legal lessons" scattered across fifteen sections) is the best idea on the page. Collected in one place it becomes the "how it's happening" layer you want: how a map can do all of this and break no rule. `frame_p4` even miscounts the thread: "Each of the five legal reasons is different", but the casings number eight.

### D8. The lead strings already exist and nothing renders them

`verdict.headline`, `p_what`, `p_split`, `p_question`, `p_answer` and `p_howfar` are referenced nowhere in `viewer/src`. `p_answer` reads: "One of the two is. The other looks normal." That is the strongest plain-language line in `en.ts`, and it is dead.

More broadly, about **9,500 of 28,158 `en.ts` words** are never referenced by a literal key. That is an upper bound: some keys are built dynamically, such as `glossary.${key}` (excluded from the count) and possibly `explorer.flags`. Out of scope here, but every dead word is still a word translators are asked to translate.

---

## 2. Proposed restructure, written from scratch

**Target:** about 5,000–5,500 words on the main page, roughly 22 minutes, down from about 71. Depth moves to sub-pages that already exist and to one new one, `/evidence`, which holds the full 14-casing log verbatim (with the §5 fixes). That guarantees every disclosure keeps a home.

### First screen
- **H1:** "Alberta's Electoral Map, Audited".
- **Subtitle:** the finding in two sentences, from Edit 1.
- **A "This week" strip:** "The committee's map is due November 2. We score it within 72 hours, against tests locked before it existed."
- **The cover map,** with the button to the explorer.

### First 60 seconds (about 240 words)
Edit 2, then the existing "What we can and can't say" box. By the end of that, a reader knows four things: what the minority map does, who drew it, where the pen went, and what happens this week.

### New order

| # | New section | Draws on | ~Words |
|---|---|---|---|
| 0 | Hero + "This week" strip | `hero.*`, `verdict.p_answer` | 70 |
| 1 | **What's happening** | `frame_p1b`, `tldr_p1`–`p3`, `c1`/`c3`/`c6` headlines, `c12` (who drew it), `c13` (the move), verdict box | 700 |
| 1a | How to read the cover map (caption block under the map) | `the_map.p2`–`p4`, `epigraph.*` | 150 |
| 2 | **How it works on the map:** cracking (Airdrie); packing (NE/central Calgary); the cost in vote equality; urban heads and rural tails; the odd shapes the chair flagged, with Banff credited; what 60 of 89 buys | `c1`, `c3`, `c4`, `c2` + `c2_experts` fairness, `region_p2`–`p4`, `c6_found2`, `super_*` | 1,100 |
| 2b | **How it works in the system:** the pen moved (Motion 19, the committee, no hearings, the precedent); why every step is legal (eight one-line lessons); what the government cited (R5, one paragraph) | `c13`, `c14`, `november.intro`, the eight `*_gun` lessons, `editorial_canada.p5`–`p6` | 600 |
| 3 | **How we know:** the what-if machine; in Alberta neutral is not 50/50; one results table for both maps and both lanes; the figure once; what 1 in 568,000 means and doesn't; what the machine can't see; both sides tested (ledger table); where the audit lost; who did this | `act2_intro_p1`/`p2`, `c6`, `c8`, `c9`, Act I table + `t5` merged, `stakes` figure, `ledger_*`, `c11`/`c12` (condensed), `c5`/`c7`/`c10` + Fisher, `frame_coi` | 1,500 |
| 4 | **This week: the November test.** The process checks, the R5 conditions, the structural and outcome checks, the 72-hour commitment and both outcomes; becomes "The results" after Nov 5 | `playbook_p1`/`p2`, `process_scorecard`, `authors_view.p10` (its checklist half), R5 (your rewrite) | 500 |
| 5 | The author's view (signed, severable) | `authors_view.*`, trimmed and fixed | 500 |
| 6 | Retractions and corrections | `retractions.*`, compacted and fixed | 250 |
| 7 | Back matter: fixes for next time (teaser), references, resources, about me, about this translation | `suggestions` teaser, `references.*`, `resources.*`, `about_me.*`, `translation_about.*` | 400 |

### Where every current section goes

| Current id | Fate | Essential content now lives… |
|---|---|---|
| hero | Rewrite | §0. The academic title moves to `/methods` or the PDF. |
| epigraph | Move | Caption block §1a. The reader-and-author exchange is good, but it is about cartography, and it sits before the argument. |
| the-smoking-gun | Split / cut | `frame_p1b` → §1. `frame_p1`, `p2`–`p4` and the beat legend → `/evidence` intro only. `frame_p5` → §3 "Where the audit lost". `frame_coi` → §3 "Who did this". `frame_routes` → cut (nav does this). `legal_body` → one line in the verdict box; full text on `/law` (already there). Verdict box → §1, kept. |
| the-picture | Merge | Figure → §3 (once). `picture.lead` → cut. `tldr_*` → §1. `tldr_footer` link → §6. |
| the-map | Move / cut | `p2`–`p4` → caption §1a. `p1` → cut. `p5` → cut: unsupported claim (§5 #15). |
| act-1 | Split | C1, C3, C4 → §2. C2 → §2, with the `c2_experts` Banff fairness note kept. C5 → §3 "Where the audit lost". Act I table + lane2 figure → §3 merged table. Each `*_gun` lesson → §2b list. Full casings → `/evidence`. |
| what-this-means | Mostly cut | `you_p` → one line plus the explorer link in §2. `region_p2`–`p4` → §2 "rural tails" (keep `region_p2`'s caveat that rural Alberta does not have too many seats). `community_p` → merged into the Airdrie item. `municipality_p` → cut (overclaim, §5 #7). `province_p` → seat-margin point merged into §2 "what it buys", with the contradiction fixed. The intro questions ("Where does your MLA live?") → cut: the audit never measures MLA residence. |
| history-of-gerrymandering | Move | `/law`, as a "Where the word comes from" section. Main page gets one link line. |
| canada-is-different | Move | `/law` (most of it duplicates `/law` already). `p5`–`p6` → one sentence in §2b. `p6`'s "to choose between them" fixed (§5 #5). |
| act-2 | Split | Intro → §3, short. Chains, steps and drand → `/methods` (already there). `howmcmc_*`, the prereg box and the SZAT box → `/methods`. C6 → §1 headline + §2 "what it buys" + §3 table. Hill-climb → §3. `super_*` → §2. C7 → §3 "Where the audit lost". C8 → §3; the Fisher history goes to "Where the audit lost". C9 → §3 (sampler swap) and "Where the audit lost" (mechanism test). C10 → "Where the audit lost". |
| act-3 | Split | C11 → §3 "Both sides tested", two sentences plus a link to `/evidence`. C12 → §1 (who drew it) and §3 (chair overbroad; the minority's charges). Ledger → §3, table kept, intro trimmed. C13, C14 → §2b. C13/C14 depth → `/norms` (already largely there). |
| the-scorecard | Cut / merge | Figure → §3 (once). `t5` table merged into the §3 table. `details2_p` → `/methods`. `rev_*` litany → cut: it restates. `playbook_*` → §4. `appendices_*` → a §3 link to `/explainers`. |
| section-7 | Split | `intro` → §2b. `finding3`: precedent → §2b; R5 → §4 (yours); its overclaims fixed (§5 #6). `framework_p1`–`p3` → `/law`. `process_scorecard` → §4. Drop the "CONTEXT … not part of the findings" label, which tells readers to skip the section that matters this week. |
| authors-view | Keep, trim | §5. Cut `p10`'s re-listed checklist (now in §4) and keep its last three sentences. Fix `p5` ("the map they draw", §5 #4). |
| section-8 | Move | New `/fixes` sub-page: advance votes, Lesser Slave Lake and s.15(2), census timing. 60-word teaser in §7. `banff_p` fixed (§5 #14) and moved to `/fixes` or §2. |
| retractions | Keep, compact | §6. Fix the "six dimensions" count and the condition-5 pointer (§5 #11, #17). |
| references, resources, contact, about-translation | Keep | §7. Fix `about_me.p1` (§5 #1). Rename "Technical Appendix", since it lists plain-language reports too. |
| (new) /evidence | New sub-page | The full 14-casing log with the five-question format intact: the home for every casing-level caveat. Keep the `#casing-N` anchors there, and add a small hash redirect from `/#casing-N` → `/evidence#casing-N` so existing shared links survive. |

**Implementation notes.** `SECTIONS` in `+page.svelte` drives the scroll-spy nav and `observeSections` analytics, so the ids change with the structure. Every locale is keyed to `en.ts`, so this restructure invalidates the translations. That's your call for later; flagged once here.

---

## 3. Concrete edits (before → after)

Every number, date, name and quote below is copied from the source string named. Where a caveat leaves the main page, its new home is stated.

### Edit 1. `hero.h1` + `hero.subtitle`

**Before** (14 + 27 words): "Laws, Norms, & Statistics: An Audit of the 2026 Alberta Electoral Boundaries Commission Reports" / "Alberta's commission produced two competing riding maps in 2026. This audit ran the same tests on both, asking one question: do they treat voters the same way?"

**After:**
> **Alberta's Electoral Map, Audited**
> In 2026 Alberta's boundary commission split and filed two maps. One looks normal. The other favours the UCP further than nearly all of 1.01 million computer-drawn neutral maps. The map that replaces both is due November 2.

"One looks normal" adapts the unrendered `verdict.p_answer`.

### Edit 2. Opening ("What's happening") replaces `frame_p1`, `frame_p1b`, `frame_p2`–`p4`, `picture.lead`, `tldr_p1`–`p3`

**Before** (~600 words across those keys). It opens: "You came here looking for a smoking gun. This report does not have one. It cannot have one — and the reason it cannot is the most important thing the audit found."

**After** (~260 words):
> Every few years Alberta redraws its ridings, the districts that each elect one MLA. Where the lines fall decides whose votes add up to a seat and whose scatter.
>
> On March 23, 2026 the commission doing the redraw split three to two and filed two maps. The majority map, signed by the chair, behaves like the maps a neutral process draws. The minority map, drawn by the two commissioners the government nominated, does not. It splits Airdrie, a city of 85,805, into four pieces, leaving its residents a minority in every one. In north-east and central Calgary, where the NDP won thirteen of seventeen seats in 2023, it draws districts 11.5% above the provincial average. On 2023's votes it gives the UCP 60 of 89 seats, against 55 on the majority map. At a tied vote, only 69 of 1,010,000 neutral maps give the UCP more.
>
> Three weeks later the Legislative Assembly set both maps aside. Motion 19 passed 44 to 36 on April 16 and gave the job to a committee of five MLAs: three UCP, two NDP, chaired by UCP MLA Brandon Lunty. Per CBC, it will hold no public hearings on its map and release no draft. Its 91-seat map is due November 2.
>
> That map is the test. The audit registered its November checks before the map existed and will score it within 72 hours, whichever way it lands.

Caveats that moved: the "no smoking gun" frame → the verdict box (kept directly below) and `/evidence`. "Deliberately cautious ceiling" → §3 (Edit 9). The efficiency-gap miss → §3 "Where the audit lost" (Edit 10). "Measures outcomes, not intent" → verdict box, `box_cant_1`. "Packing" is described here, not named; the pre-registered packing test is named in §2 (Edit 5).

### Edit 3. `body.clean.legal_body` (107 words) → one line in the verdict box

**Before:** "'Gerrymandering' has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense… They are not proof of a legally-defined wrong, and this report does not describe them in those terms."

**After** (replaces `verdict.box_cant_2`):
> That the map "is" a gerrymander in law. Canadian law has no such category. We use the word the way most people do: drawing lines for partisan advantage.

The full paragraph's home is `/law` ("Why this audit never rules 'gerrymander'"), which already carries it nearly verbatim.

### Edit 4. `body.the_map.p5`: remove an unsupported claim

**Before:** "A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once the population is visible underneath the boundary choices, those choices stop looking random."

**After:**
> On a standard election map Alberta is a wall of blue. Weighted by where people live, it is a dense arc of cities that vote very differently from the countryside around them. Most of the lines the two maps fight over sit where that arc meets the countryside.

Uncertain: the last sentence holds for Airdrie, Cochrane, Chestermere, the Calgary edge, Red Deer and St. Albert. Rocky Mountain House–Banff Park is the exception. Cut the sentence if you want zero exceptions.

### Edit 5. Casing 1 + Casing 3 → §2 "Cracking" and "Packing"

**Before:** `c1_found` + `c1_show` + `c1_experts` + `c1_canada` + `c1_gun` (427 words), and `c3_*` (251 words).

**After** (~190 words):
> **Cracking: one city, four districts.** Airdrie has 85,805 people (2024 municipal census), one council and one school division. The law caps each district at one-and-a-quarter times the provincial average, so Airdrie needs at least two. The majority map gives it two. The minority map gives it four, each attached to a different rural or Calgary-edge district, and Airdrie's residents are a minority in all four. That meets every criterion of the audit's pre-registered cracking test. The majority's split meets none.
>
> **Packing: north-east and central Calgary.** Here the NDP won thirteen of seventeen seats in 2023. The minority map's districts average 11.5% above the provincial population; the majority's average 2.8%. A bigger district means each vote in it weighs less. The pattern meets the audit's pre-registered packing test.
>
> Both moves are legal. The Act lets commissions split cities, every district sits inside the ±25% band, and courts defer to how boundary bodies weigh community of interest.

Dropped on purpose:
- `c1_found`'s "Airdrie is the largest Alberta city without its own MLA". Unverified: the 2019 map has an Airdrie-East district (from memory; check).
- `c3_title`/`c3_found`'s "a quarter too big". The stated numbers do not support it (§5 #8).

The PTA and MLA-office illustration from `c1_show` and the `c1_canada` norm move to `/evidence`.

### Edit 6. Casing 4 → §2 "The cost"

**Before:** `c4_*`, 255 words, with two different spread figures (3,938/2,827 and 4,707/3,180) and no explanation of why there are two.

**After** (~85 words):
> **The cost: vote equality.** Equal populations are the one value the Act puts a number on. By the commission's own tables, the minority map's districts stray from the ideal size by 4,707 people on average, against the majority's 3,180, which is 48% wider. The audit's own measurement on the official shapefiles agrees (3,938 against 2,827): only about 1 in 100 neutral maps spreads populations wider. The usual defence of odd shapes, that they were needed to balance populations, runs backwards here.

### Edit 7. `c6_found2` + `super_lead` + `super_body` + `super_close` + `province_p` → §2 "What it buys"

**Before:** ~530 words across five strings. `super_lead` opens on "a two-thirds supermajority requires exactly 60 seats", then `super_body` explains that the threshold unlocks nothing. The section sets up a stake and then dismantles it. `province_p` then says the 60-seat question is untested (§5 #2).

**After** (~120 words):
> **What it buys.** On the minority map, the UCP keeps the 45 seats it needs for a majority down to about 49.7% of the vote. On the majority map, it needs to win the popular vote by about 4 points. On 2023's actual votes the minority map yields 60 of 89 seats, against 55. Sixty seats unlocks no special power in Alberta's Assembly; a bare majority can already pass laws, invoke closure and set committee membership. What 60 buys is margin: a government a handful of floor-crossings cannot threaten, facing an opposition too small to sustain committee scrutiny.

The caveat from `super_lead` and `c6_gun` that the simulation does not enforce every statutory criterion moves to §3 (Edit 8). `c6_found2`'s "the UCP could lose the popular vote by 0.3 points" is replaced by the vote share it rests on, because "lose by 0.3 points" is ambiguous: at 49.7% against 50.3% two-party, the gap is 0.6.

### Edit 8. `act2_intro_p1` + `act2_intro_p2` + `howmcmc_*` → §3 "The what-if machine"

**Before** (116 + 93 + 76 words). It opens: "Act I needed nothing but the lines. Act II asks a harder question…", followed by a parenthetical: "(4 independent chains × 252,500 steps, base seed from the Cloudflare drand public randomness beacon, pre-registered at OSF before execution)".

**After** (~150 words):
> **How we know.** A computer drew 1,010,000 legal Alberta maps from the official Elections Alberta files. Each keeps every district within the population band and in one connected piece. The computer never sees a vote. Put a real map among them and you can see how far into the tail it sits. The random starting point was locked to a public randomness beacon and registered before the run.
>
> One fact makes every number readable: in Alberta, neutral is not 50/50. At a tied vote the median neutral map gives the UCP 44.8% of seats, because rural UCP ridings are won by wide margins that waste votes. The machine enforces population and contiguity, not every rule the commission weighed, so it is a strong outside check, not a list of every map a commission could lawfully draw.

Chains, steps and the beacon's name stay on `/methods`, which already explains them. The last sentence carries the `super_lead`/`c6_gun` caveat.

### Edit 9. `c8_found` + `c8_show` + `c8_experts` + `c8_gun` → §3 "What 1 in 568,000 means"

**Before:** 420 words. `c8_found` alone is 218, including the retired-figure history.

**After** (~110 words):
> **One in 568,000.** That is the ceiling on how often a neutral process would produce the minority map's combined profile across the four fairness measures. In technical terms it is p ≤ 1.76×10⁻⁶, a Bonferroni-corrected, dependence-robust upper bound. The audit doubled the raw figure because it looked in two places, so the true odds are at most this common. The number is not the chance the map is innocent; mixing those two up is the prosecutor's fallacy. A map this rare can still come from unusual but honest judgment. What the number rules out is routine drafting variation.

The retired "one in fifteen million" history moves to Edit 10.

### Edit 10. New §3 box "Where the audit lost" replaces `frame_p5`, `c5_*`, `c7_*`, the mechanism half of `c9_found`, `c10_*`, and the Fisher history in `c8_found`

**Before:** spread across five casings (~1,400 words). The framing count in `frame_p5` is wrong: "Two casings in the log point the wrong way…"

**After** (~190 words):
> **Where the audit lost.** These results ran against the story. All of them stay on the record.
> - **The anchoring test died.** Early tracings showed the minority map following municipal lines 15% of the time. On the official shapefiles it is 72%, against the majority's 80%; both sit inside the 70–85% Canadian norm. Retracted permanently.
> - **The efficiency gap missed.** The minority scored +4.0%, the 94th percentile. The pre-registered line was the 95th (about +4.1%). It stays a miss.
> - **The mechanism test failed.** The audit tested whether the flagged shapes are what produce the seat advantage. On its test, they are not.
> - **The minority passed one test outright.** On neighbour-drain it shows 1 coupled signal, against the majority's 2 and the 2019 map's 5.
> - **Two statistics were retired.** The Swing-Zone Allocation Test fell from p = 0.0024 to p ≈ 0.19 once corrected for neighbouring areas voting alike (retired 2026-06-13). The old one-in-fifteen-million headline combined two channels that were not independent (retired 2026-06-10).

Full write-ups stay on `/evidence` (Casings 5, 7, 9, 10) and `/methods` ("The tests that died").

### Edit 11. `c13_found` + `c14_found` + `november.intro` → §2b "The pen moved"

**Before:** 259 + 111 + 73 words, with conflicting accounts of who drafts the map (§5 #4).

**After** (~150 words):
> **The pen moved.** The commission held hearings in sixteen communities, received 1,147 written submissions, and reversed its own interim proposal on the strength of 80-plus of them. Three weeks after its split reports arrived, the Legislative Assembly set both aside: Motion 19, April 16, 2026, passed 44 to 36. It handed the job to a Select Special Committee of five MLAs, three UCP and two NDP, chaired by UCP MLA Brandon Lunty. An advisory panel chaired by retired Court of Appeal justice Brian O'Ferrall drafts the map. The five MLA votes decide. Per CBC, the committee will hold no public hearings on its map, and no draft will be released for public challenge. Among the Canadian redistribution cycles this audit reviewed, the move has no precedent, an assessment political scientist Duane Bratt (Mount Royal University) shared in correspondence with the author. Every step was lawful.

Verify before shipping:
- "Panel drafts / committee decides" follows `november.intro` and `/norms`. `c13_found` and `authors_view.p5` say otherwise (§5 #4).
- O'Ferrall as chair conflicts with the glossary (§5 #3).

### Edit 12. The eight `*_gun` legal lessons → §2b "Why every step is legal"

**Before:** scattered across `c1_gun`, `c2_gun`, `c3_gun`, `c4_gun`, `c6_gun`, `c11_gun`, `c13_gun` and `c14_gun` (~540 words), each closing a different casing.

**After** (~150 words):
> **Why every step is legal.**
> 1. The Act's factors are discretionary, and courts defer to how commissions weigh them.
> 2. Commission reports bind no one. The legislature holds the pen.
> 3. Inside the ±25% band, uneven district sizes are lawful, and partisan effect is not a recognized legal harm.
> 4. The Act contains exactly one number, and both maps comply with it.
> 5. Neutral-ensemble evidence, the field's best tool, has no legal home in Canada.
> 6. Bad reasons for a lawful line still leave a lawful line.
> 7. Hearings, drafts and comment periods are optional, and opting out is legal.
> 8. Norms are not law. Courts may name a convention and still decline to enforce it.
>
> That is how a map can carry a gerrymander's signature and break no rule.

Supporting authority for each lesson (the Saskatchewan Reference, *Rucho*, the 1981 Patriation Reference) stays on `/law` and `/evidence`.

### Edit 13. `playbook_p1` + `playbook_p2` + `process_scorecard` + the checklist in `authors_view.p10` → §4 "This week: the November test"

**Before:** ~400 words across four places (D3).

**After** (~200 words, with a slot left for your R5 text):
> **This week: the test.** The committee's 91-seat map is due November 2, 2026. The audit registered its November checks before the map existed (OSF registration qsgy8) and will publish the scoring within 72 hours of release, whichever way it points.
>
> **The process.** Were public hearings held? Was a draft released for comment? Are the advisory panel's members and terms of reference published? [R5: the four conditions (a)–(d) and the "rest of the province" clause go here]
>
> **The map.** Does it repeat the minority map's signatures: a Calgary zone population gap of 10% or more, an Airdrie split four or more ways, an s.15(2) district anchored to uninhabited protected land? Where does it land on every measure above, against the same 1,010,000 neutral maps and the same thresholds?
>
> If it repeats the signature, drawn by different people under different constraints, the structural finding earns confirmatory status. If it lands inside the neutral bands, the finding stands as an observation about one map that was never enacted, and this page will say so.

Uncertain: I took the process and signature sub-checks from the academic report's X-list summary (`reports/academic/report_academic.md` around line 1755). Before publishing, confirm that wording against the frozen `preregistration/november_2026_scoring_spec.md` and OSF qsgy8. The site must not paraphrase a registration into something it didn't say. After the scoring, this section's heading becomes "The results".

### Edit 14. `body.about_me.p1`: fix the conflict-of-interest contradiction

**Before:** "…I have no connection to Elections Alberta, the commission, or any political party."

**After:**
> …I have no connection to Elections Alberta or the commission. I have donated to the NDP and volunteered for it, and I have donated to the Progressive Conservatives, a predecessor party of the UCP.

The facts come from `frame_coi`. Keep `about_me.p2` ("voted for different parties…") as is.

### Edit 15. `suggestions.banff_p`: align with the audit's own ledger

**Before:** "…the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. The commission's own chair called it 'a bad faith effort'…"

**After:**
> …the minority proposed protecting a different riding by extending it into the uninhabited part of Banff National Park. The commission's own chair called that "a bad faith effort" to claim the legal protection. The audit's check undercut the charge: the division qualifies under s.15(2) even without the extension. The extension still claims, over empty land, a protection written for remote communities where people live.

Source for the verdict: `ledger_r3_c`. The townsite fairness point (`c2_experts`) stays in §2. Uncertain: the last sentence is my synthesis of `c2_experts` ("aimed at the empty-park extension the townsite's placement does not touch"). Check that it says no more than that.

---

## 4. Recommendation 5: flags only (yours to rewrite)

**Where R5 sits in the new structure:**
- one sentence in the §0 "This week" strip, linking to §4;
- one paragraph in §2b ("what the government cited");
- the full four-condition checklist in §4 as the X1 check.

Right now R5 first appears about 54 minutes into the page and is described twice in passing.

**Problems in the current copy:**
- **`commission_split.finding3`: "Recommendation 5 was also geographically specific: one additional rural seat south of Edmonton, and one in Clearwater County and western Mountain View County".** R5's text says "restore the two electoral divisions that this Commission has removed". The south-of-Edmonton seat is an inference from R5(c)'s Leduc–Beaumont/Nisku note. The Clearwater one is R5(d), which says only "consider restoring". "Geographically specific" overstates both.
- **`finding3` and `/norms`: "far from the contested urban-edge communities".** R5(c) reaches into Edmonton itself: south-of-river Edmonton reverts to the interim map. R5(a) explicitly protects Airdrie and everything south of it. That protection is the sharpest testable point, and the copy never states it.
- **`finding3`'s opening claims.** "The process now promoting the minority map" asserts the outcome the test is meant to measure. "Lets a cabinet hand redistricting" is wrong on the mechanism: Motion 19 was an Assembly vote, 44 to 36. `c14_found` says "governing-party majority", which is right.
- **`playbook_p1` and `authors_view.p10`.** "Does the map honour the recommendation the government cited" is too vague to be scored by a reader. Name the four conditions and the "rest of the province as we propose must be maintained to the extent possible" clause.
- **Outside site scope.** The academic report's X1 summary (`report_academic.md` around line 1765) shortens R5(a) to "no impact south of Airdrie". R5(a) says "no impact on any electoral division in Airdrie or containing territory south of Airdrie's southernmost border, with the exception of Drumheller-Stettler". The paraphrase drops Airdrie itself.


**Update — done in this PR (2026-10-29):**
- `finding3` rewritten: no "cabinet", no "now promoting the minority map", no "one rural seat south of Edmonton". It ends by pointing to a new block.
- New `body.november.r5_*` block (`#recommendation-5`, in the Lunty section): who wrote R5 and why, the trigger, 89 → 91, the "rest of the province as we propose" clause, conditions (a)–(d) in plain words with district counts read off the majority map (41 / 11 / 10), and how test X1 scores it.
- `/norms` bullet corrected: R5 freezes Airdrie, Calgary and the south — the very lines the commission split over.
- Explorer "EBC '26 Annotations" now marks all four R5 areas (`analysis/scripts/build_lunty_bounds.py`): the two R5 changes (c, d) are shaded; the two it leaves alone (a: Airdrie and everything south; b: north Edmonton) sit inside a dashed limit line, so nothing reads as R5 reaching south of Airdrie. District lists are on `/explorer/text`.
- "Electoral Districts Act" → "Electoral Divisions Act" in four English places (R5's own wording, p. 66).
- Not yet done: moving R5 into a §0 "This week" strip and §4 test section — that waits on the restructure.


---

## 5. Contradictions and accuracy flags (fix whatever the structure)

| # | Keys | Problem | Severity |
|---|---|---|---|
| 1 | `about_me.p1` vs `frame_coi` | "no connection to … any political party" against "volunteered for the [NDP]" | High |
| 2 | `editorial_reflect.province_p` vs `c6_found`, `authors_view.p9` | 60 seats "not yet directly tested" against "60 of 89 seats" on 2023 votes. Uncertain what gap `province_p` meant: possibly other vote shares. Say that if so. | High |
| 3 | `glossary.advisory-panel` vs `c13_found`, `authors_view.p5`, `/norms` | Glossary: four-person panel, chair seat "went unfilled". Elsewhere: chaired by Brian O'Ferrall. The unrendered `november.intro_b` reconciles them ("a chair appointed later"). Update the glossary from it. | High |
| 4 | `november.intro`, `/norms` vs `c13_found`, `authors_view.p5` | "The committee itself does not draw the map" against "to draft a 91-seat map" and "the map they draw". Verify, then pick one. | Medium |
| 5 | `editorial_canada.p6` | The committee was created "to choose between them". It is producing a new 91-seat map. | Medium |
| 6 | `commission_split.finding3` | "process now promoting the minority map" (premature); "a cabinet" (it was an Assembly vote) | High |
| 7 | `editorial_reflect.municipality_p` | "the four statistical measures flag the same districts the structural tests flag". They are whole-map measures, and `c9_found` reports the mechanism test failed. Cut it. | High |
| 8 | `c3_title`, `c3_found` | "a quarter too big / a quarter larger". The source is Zone A mean 61,225 vs provincial 54,929 = +11.5% (`report_academic.md:1202`), against +2.8% on the majority. That makes minority districts about 8.5% larger, not 25%. Uncertain: a zone-total figure I didn't find may exist. | Medium |
| 9 | `frame_p4` | "five legal reasons"; the casings number eight legal lessons | Low |
| 10 | `frame_p5` vs `frame_coi` vs C5/C7/C9/C10 | "Two casings point the wrong way" vs "Three findings that ran against his expectation" vs at least five adverse results on the page | Medium |
| 11 | `tldr_p2`, `t5_r2_b`, `framework_p2` vs `act1_table_close`, `rev_p2`, `rev_found` vs `retractions.conditions_intro` | Structural count given as "four of five", "four of four", and "three of the six independent structural dimensions". Anchoring is also called both "neutral" and "the retracted fifth". | Medium |
| 12 | `c6_found`, `rev_p2`, `retractions.c4_what` vs `tldr_p2` vs `super_lead`, `t5_r2_c` | 69 maps "exceed" vs "award as many seats as" vs "reach". At n = 69, ≥ and > are different claims. Check the chain CSV and use one. | Medium |
| 13 | `act1_intro`, `c13_found`, `authors_view.p5` vs `c12_found` | 1,147 submissions vs "~1,340 submissions" on the same page, with no explanation. These may be different universes (written responses to the interim report vs the full archive). Say so. | Medium |
| 14 | `suggestions.banff_p` vs `ledger_r3_c`, `c2_experts` | "where no one lives" (the townsite is in the park), and the chair's "bad faith" is repeated without the ledger's "Undercut" verdict. See Edit 15. | Medium–High |
| 15 | `the_map.p5` | "most of the people live in areas that vote the other way". Unsupported here. From memory (not checked this session), the UCP won the 2023 province-wide vote at about 52.6% to 44.0%. See Edit 4. | Medium |
| 16 | `c1_found` | "Airdrie is the largest Alberta city without its own MLA". The 2019 map has an Airdrie-East district (from memory; verify). | Low–Medium |
| 17 | `retractions.c5_what` | Points to a Quebec argument "in the Lunty Committee section". The rendered section has none; the argument lives on `/norms`. | Low |
| 18 | `editorial_canada.p7` | Sends readers to "the references section below" for the standing question and reform pathways. That section is a citation list. Verify, or point to `/law`. | Low |
| 19 | `c7_found` vs `details2_p` | Efficiency-gap percentile given as "94th" and "94.5th". Trivial, but pick one. | Low |
| 20 | Legal citations | `SESSION_HANDOFF.md` (dated 2026-06-10, possibly stale) lists T6 legal citations as pending counsel review. The site states its case law without qualification. Confirm T6 is closed. | Note |

**Out of scope, noted once.** All these strings feed 19 locales. Every fix above, and the restructure, lands on translators later.

---

## 6. Word budget

| Section (current id) | Current words | Proposed | Destination |
|---|---:|---:|---|
| hero | 98 | 70 | §0 |
| epigraph | 151 | 0 (→ caption) | §1a |
| the-smoking-gun | 806 | 330 | §1 + verdict box |
| the-picture | 366 | 0 (→ §1, §3) | merged |
| the-map | 307 | 150 | §1a caption |
| act-1 | 2,384 | 450 | §2 (+ §3 table, "lost" box) |
| what-this-means | 1,011 | 150 | §2 |
| history-of-gerrymandering | 374 | 20 (link) | `/law` |
| canada-is-different | 561 | 40 | `/law` + §2b |
| act-2 | 3,221 | 700 | §3 (+ §2 "what it buys") |
| act-3 | 2,337 | 900 | §2b + §3 (ledger kept) |
| the-scorecard | 1,133 | 150 | §3 table + §4 |
| section-7 | 906 | 450 | §2b + §4 (+ `/law`) |
| authors-view | 993 | 500 | §5 |
| section-8 | 1,265 | 60 | `/fixes` |
| retractions | 525 | 250 | §6 |
| references + resources + contact + about-translation | 434 | 380 | §7 |
| **Total main page** | **16,872** | **~4,550** | (~19 min at 238 wpm) |

Proposed totals assume the edits above. The §2/§3 table rows, the ledger table and the figure captions push the real figure toward 5,000–5,500. Material that leaves the main page is not deleted: it lives verbatim on `/evidence`, `/law`, `/methods` or `/fixes`, so the site-wide word count barely moves. What moves is where the reader meets it.
