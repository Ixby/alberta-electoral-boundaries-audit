# Latent-bias red team — findings

Scope: `report_public.md` (395 lines, final state 2026-04-23). Read against 15-point latent-bias checklist. This pass looks for bias the author's overt prior declaration does not cover — places where language, framing, selection, voice, or silent assumption tilts sharper than the evidence.

## Executive summary

- CRITICAL: 1
- HIGH: 5
- MEDIUM: 7
- LOW: 4
- INFO: 3

## Critical findings

### CRIT-01. "Two NDP-nominated commissioners — Clark on X, Samson in the record, Miller himself on the same page" mis-counts and mis-colours the chair

**Passage (verbatim):** `report_public.md:322`
> The "the commission asked for this" defence rests on a chair-only addendum disavowed by the two NDP-nominated commissioners — Clark on X, Samson in the record, Miller himself on the same page as his own recommendation.

**Bias type:** selective quotation / attribution error / value-laden labelling disguised as neutral

**What a hostile reader of the right would say:** The sentence says "two NDP-nominated commissioners" and then lists THREE names, including Miller. Miller is the Lieutenant-Governor-appointed chair, not an NDP nominee. By bundling him into a phrase that carries a partisan label, the passage converts the neutral tie-breaker into a *de facto* third NDP-nominee, then uses that false pair ("two NDP-nominated") to frame the disavowal as unanimous on the opposition side. This is precisely the rhetorical manoeuvre the piece elsewhere flags Premier Smith for — citing an authority by mis-attributing its composition. A pro-government reader would call this the single most damaging paragraph in the piece to its claim of neutrality. Earlier in the piece (line 79) the author is explicit: the chair is appointed by the LGIC from a statutory list; he is NOT NDP-nominated. Making him the third of "two NDP-nominated" contradicts the author's own setup.

**What the evidence actually supports:** Three people disavowed the use of the addendum: Clark (opposition-nominated), Samson (opposition-nominated), and Miller (the chair, who wrote the disputed sentence himself). That is already a strong finding. It does not need the label "NDP-nominated" attached to Miller, and the label changes the constituency that read the disavowal as unanimous.

**Recommended neutralizing edit:**
- Before: "...rests on a chair-only addendum disavowed by the two NDP-nominated commissioners — Clark on X, Samson in the record, Miller himself on the same page as his own recommendation."
- After: "...rests on a chair-only addendum disavowed by its own author — Miller on the same page as his own recommendation — and by the two opposition-nominated majority commissioners, Clark on X and Samson in the record."

## High findings

### HIGH-01. "It was a retort. It was also a tell" — authorial motive attribution beyond the evidence

**Passage (verbatim):** `report_public.md:43`
> "The members should take our AI Academy, because then they'd learn how to use the marvels of modern technology as well so that they can develop their own maps." The remark was a retort. It was also a tell.

**Bias type:** implicit motive attribution / value-laden descriptor disguised as observation

**What a hostile reader of the right would say:** "Tell" is a poker term meaning an involuntary signal that reveals hidden intent. It reads what Smith said as a slip that exposes her actual plan. Nothing in the quoted sentence — a sarcastic retort about AI — licenses a jump from "retort" to "tell." The author is packaging his own inference as if it were observable on Smith's face. This same author elsewhere (line 322) is rightly vigilant about what Smith "did not read out" — but here he does to Smith exactly what he criticizes Smith for: silently re-weighting a source to fit a thesis. Every UCP reader hits this line and disengages.

**What the evidence actually supports:** That Smith made a sarcastic remark about using AI to draw maps. The subsequent paragraph about responsible AI use is valid and can stand without the "tell" frame.

**Recommended neutralizing edit:**
- Before: "The remark was a retort. It was also a tell."
- After: "The remark was a retort. It also opened a substantive question the committee will have to answer."

### HIGH-02. Asymmetric skepticism on partisan quotes — Nenshi's "full-on assault" is reproduced verbatim without correction; Smith is paraphrased with disclaimers

**Passage (verbatim):** `report_public.md:17` and `report_public.md:224`
> "Let's be clear," he said. "Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and, in fact, not adopting the report is a full-on assault on our democracy."

and

> Premier Smith has said, paraphrasing the commission's own concerns as she understands them, that the commission "made it clear it did not want to lose two rural ridings."

**Bias type:** asymmetric skepticism on quotes / framing order

**What a hostile reader of the right would say:** Nenshi gets a full unbroken three-clause quote with the phrase "full-on assault on our democracy" allowed to stand without comment in the piece's second scene. It sets the emotional register for the rest of the piece. Smith, by contrast, is not quoted on rural preservation directly — she is paraphrased, and the paraphrase is framed "as she understands them," which is a polite-sounding signal that her understanding may not be the commission's. The opposition gets the amplifier, the government gets the filter. Later, the piece does adjudicate the supermajority claim (line 324) and partially walks back Nenshi's and Notley's framing — but that reversal is buried 307 lines later, by which point the reader's frame is set. A disciplined version would either pre-emptively acknowledge at line 17 that the piece will end up finding "supermajority" unsupported, or it would apply the same "as she understands them" caveat to Nenshi.

**What the evidence actually supports:** Nenshi said what he said. Smith said what she said. Both deserve direct attribution at the same epistemic level. The piece's own findings (line 324: "the word 'supermajority' fits no tested scenario") mean the piece knows Nenshi's framing is over-sized. Leaving his phrase to stand at line 17 while filtering Smith's at 224 is a voice asymmetry.

**Recommended neutralizing edit:**
- Either add to line 17: "His phrasing, which this audit will return to, set the tone of the week."
- Or restore Smith's line to direct quotation at line 224: "Smith has said, 'the commission made it clear it did not want to lose two rural ridings.' " and drop the "as she understands them" editorial.

### HIGH-03. "A because-we-did-it-before rationale" — author-supplied paraphrase, loaded, then used as the rationale's full weight

**Passage (verbatim):** `report_public.md:144-146`
> Page 352 of the commission report offers four rationales for the configuration — highway-22 corridors, Rocky Mountain House as Clearwater hub, regional Indian reserves, and historical precedent. Three of those rationales are community-of-interest arguments that apply equally to the no-park-extension alternative; the only rationale unique to the park route is the fourth, which reads verbatim: "the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division."
>
> A because-we-did-it-before rationale.

**Bias type:** loaded paraphrase / strawmanning

**What a hostile reader of the right would say:** "Historical precedent" in an electoral-boundary context is a term of art. It covers continuity of representation, institutional memory, voter recognition of a riding name, and incumbent-constituent relationships — all things the Act's community-of-interest principle explicitly protects. Collapsing all that into "because-we-did-it-before" is not a translation; it is a demotion. Doing it in three monosyllabic hyphenated words dressed up as a colloquialism makes the minority's argument sound petulant. The author already made the substantive point — that three of the four rationales apply to a non-park alternative — so the paraphrase is load-bearing in attitude, not in argument. A pro-government reader sees this and notes that nowhere in the piece is a majority rationale compressed this way. The chair's 91-seat addendum, by contrast, is treated to a long, literal parsing of its conditions (lines 258-268).

**What the evidence actually supports:** That the minority's fourth rationale is historical precedent. Whether historical precedent is a serious rationale in this context is a policy argument, not a colloquialism.

**Recommended neutralizing edit:**
- Before: "A because-we-did-it-before rationale."
- After: "Historical precedent — a community-of-interest argument the commission did not elaborate — is the one rationale the non-park alternative does not satisfy." (Leaves the reader to weigh the argument without a thumb on the scale.)

### HIGH-04. "Engineered boundary" — survived a retraction and is now carried on a purposive reading only; label is sharper than the retained evidence

**Passage (verbatim):** `report_public.md:148-150, 236`
> Under a purposive reading, the boundary is engineered.
>
> This is the engineered-boundary signature. It was tempting, while reviewing the re-audit, to retract it — the district passes section 15(2) either way, so the narrow form of the test was wrong. The narrow form was wrong. The question underneath it was not.

And table at line 236:
> Engineered boundary | Detected (Rocky Mountain House-Banff Park) | Not detected | Park extension chosen over populated alternatives

**Bias type:** loaded language / survived retraction

**What a hostile reader of the right would say:** The author is explicit: the originally-specified test failed. The district qualifies under section 15(2) without the park. Rather than mark the signature "not detected" and move on, the piece invents a second, softer standard ("purposive reading") to preserve the label. This is the author moving the goalposts to keep a finding. "Engineered" is the most pointed of the three gerrymander-fingerprint words and it is the one word in the summary table that, if dropped, would rebalance the three-to-zero scoreline the piece builds toward. A disciplined author who caught his own error on section 15(2) would either (a) retract the signature and note the lesson, or (b) detect it on a clearly-labelled alternate test and rename it — "inefficient use of populated alternatives" is a fair description. Keeping the original label with a footnoted re-derivation reads as sunk-cost reasoning. This is the single most exploitable rhetorical move in the piece because the author himself flags the temptation to retract (line 150) and then openly declines to.

**What the evidence actually supports:** The minority drew a boundary through uninhabited land when populated alternatives existed and were on the record. That fact. No more, no less. Whether "engineered" applies to this fact depends on the reader's prior about whether historical precedent is a real consideration — which is exactly the kind of contested-framing issue a bias audit is supposed to flag.

**Recommended neutralizing edit:**
- Either retitle the signature: "Unpopulated-alternative boundary (detected: Rocky Mountain House-Banff Park)".
- Or in the table at line 236, add a footnote: "Detected under purposive rather than section-15(2) reading; the district passes section 15(2)."
- Either preserves the finding without pretending the narrow test survived.

### HIGH-05. Asymmetric scrutiny of rationales — minority's four rationales parsed in detail, majority's rural-preservation policy goal adopted without test

**Passage (verbatim):** `report_public.md:224`
> Rural preservation is the policy goal she has named in public. The majority map is consistent with that goal. The minority's seven Calgary hybrids and four Red Deer hybrids run the other way — pulling rural and small-town voters into districts dominated by urban neighbours.

**Bias type:** asymmetric scrutiny / silent assumption

**What a hostile reader of the right would say:** The piece subjects the minority's "shared schools" and "population" defences to cross-check and finds them wanting (lines 248-252). It does not apply the same cross-check to the majority map's rural-preservation claim. Is rural preservation actually a statutory principle, a policy preference, or a partisan euphemism for "keep Alberta's UCP-friendly seats"? The piece treats it as a neutral policy goal and uses it to credit the majority map (line 224). A UCP reader would notice that "rural preservation" is itself contested framing — the minority's defenders would argue the minority map *better* preserves rural representation by keeping Cochrane, Springbank, and Bearspaw attached to rural ridings rather than consolidating the Calgary urban vote. The piece never tests this alternative reading.

**What the evidence actually supports:** That Smith has invoked rural preservation. That the majority map uses more rural-named anchor districts than the minority map. Whether "rural preservation" as a goal is served better by rural anchors or by keeping rural populations attached to proximate urban commuter sheds is a policy argument with legitimate positions on both sides.

**Recommended neutralizing edit:**
- Before: "Rural preservation is the policy goal she has named in public. The majority map is consistent with that goal. The minority's seven Calgary hybrids and four Red Deer hybrids run the other way..."
- After: "Rural preservation is the policy goal Smith has named in public, and the two maps pursue it differently. The majority keeps rural-named anchor districts. The minority folds rural communities into proximate urban districts, arguing the commuter shed is itself a community of interest. Whether 'rural preservation' is served better by anchor districts or by commuter-shed hybrids is a substantive policy question the maps resolve opposite ways."

## Medium findings

### MED-01. The Airdrie voter is urban, female, professional-adjacent, pre-registered as voter — implied reader identification

**Passage (verbatim):** `report_public.md:97`
> It's a Monday in late June 2027. The woman is in her thirties, she has lived in Airdrie for eleven years, she works at a dental office on Main Street, and she is walking from her kitchen table to her front door with an advance-polling card in her hand. She knows how to vote. She has done this before.

**Bias type:** implicit reader identification

**What a hostile reader of the right would say:** The exemplar voter is civically engaged ("she knows how to vote, she has done this before"), young-to-middle-aged, female, service-sector professional, urban. This is an Alberta Views demographic portrait. It is *not* neutral. The piece could have picked a retired farmer in Bighorn MD watching his riding get drawn south of where he has shopped for 40 years, or a commuter in Chestermere who thinks being folded into a Calgary district reflects his actual economic life. Choosing the Airdrie voter is a defensible narrative choice — Airdrie is the starkest cracking case — but the specific demographic details add flavour that skews to the magazine's audience. A rural UCP reader does not see himself in this scene, and the piece relies on the scene to do most of the cracking argument's emotional work.

**What the evidence actually supports:** That Airdrie is split four ways, no district carries its name, her hypothetical experience is reasonable. None of that requires specifying her occupation or gender.

**Recommended neutralizing edit:**
- Before: "The woman is in her thirties, she has lived in Airdrie for eleven years, she works at a dental office on Main Street..."
- After: "The voter has lived in Airdrie for eleven years. She is walking to her front door with an advance-polling card."
- Cuts 40 words, removes the urban-professional signifier, keeps the Airdrie-voter scene.

### MED-02. "Eighty-four thousand people. Not one carrying Airdrie's name." — cracking framing in emotional register

**Passage (verbatim):** `report_public.md:101`
> Four ridings. Eighty-four thousand people. Not one carrying Airdrie's name.

**Bias type:** loaded framing

**What a hostile reader of the right would say:** Naming conventions are at the discretion of the commission and ultimately of the Legislature. The structural claim — that Airdrie is split four ways when two would suffice — is a legitimate cracking test. The naming framing ("not one carrying Airdrie's name") implicitly argues that absence of the name is a partisan signal. Naming could be defended on other grounds (the minority names districts for the urban centre with which they share commuter flow). The piece does not engage this alternative and instead lets the naming absence carry the emotional weight of the cracking finding.

**What the evidence actually supports:** That Airdrie fits a two-way split. The four-way split is the substantive cracking finding. The naming claim is stylistic.

**Recommended neutralizing edit:**
- Before: "Four ridings. Eighty-four thousand people. Not one carrying Airdrie's name."
- After: "Four ridings. Eighty-four thousand people. None named for the city they share."
- Slightly softer. Preserves the observation that the naming convention shifts; less like an accusation.

### MED-03. "The rural voice becomes the secondary voice" — one-sided reading of hybrid districts

**Passage (verbatim):** `report_public.md:217`
> Each of the minority's seven Calgary hybrids folds a rural community or small town — Bearspaw, Springbank, Cochrane, Chestermere, Airdrie-West, Tsuut'ina Nation — into a district where a Calgary neighbourhood holds the majority of the population. The rural voice, in each case, becomes the secondary voice.

**Bias type:** framing / silent assumption

**What a hostile reader of the right would say:** "The rural voice becomes the secondary voice" is one reading. Another is: "The rural commuter is re-joined to the economy they actually live in." Whether a Cochrane resident who commutes to Calgary is better represented by a Calgary-Nolan Hill MLA or by a rural Olds-Three Hills-Didsbury MLA is a genuine question. The piece elsewhere (line 290) acknowledges "the leap from 'Cochrane commutes to Calgary' to 'Cochrane belongs in the Nolan Hill district' is a narrative one, not a data one" — but that acknowledgement runs parallel to a passage where the author himself makes the opposite narrative leap ("the rural voice becomes the secondary voice") without flagging it as narrative. The two passages contradict each other on the same question.

**What the evidence actually supports:** That seven of the minority's districts pair a rural community with a Calgary neighbourhood. Whether that reduces rural voice or integrates rural commuters is a policy question the piece treats as settled only in one direction.

**Recommended neutralizing edit:**
- Before: "The rural voice, in each case, becomes the secondary voice."
- After: "In each, the rural community is the smaller share of the district population. The minority argues the commuter shed is a shared community of interest; the majority treats the rural area as a community that should anchor its own district."

### MED-04. Framing order — the reader always hits rebuttals last

**Passage (verbatim):** pattern across the piece; examples `report_public.md:41-45, 148-150, 224`

Line 41-45:
> Premier Smith disagrees with all three, and her defence rests on a single piece of paper. ... That is one way to read page 66. It is not the only way.

Line 148-150:
> The minority's configuration satisfies the letter of the rule. The park extension adds no represented community. Under a purposive reading, the boundary is engineered.

Line 224:
> Rural preservation is the policy goal she has named in public. The majority map is consistent with that goal. The minority's seven Calgary hybrids and four Red Deer hybrids run the other way...

**Bias type:** framing order / rhetorical architecture

**What a hostile reader of the right would say:** Across the piece, when Smith's or the minority's position is presented alongside a rebuttal, the rebuttal always lands last. This is a small-scale but consistent rhetorical pattern — the Smith defence is followed by "that is one way to read page 66. It is not the only way" (41-45); the statute-letter-passes defence is followed by "under a purposive reading, the boundary is engineered" (148); the rural-preservation policy goal is followed by "the minority's Calgary hybrids run the other way" (224). A disciplined piece would alternate who gets the last word, or structure paragraphs so the government defence occasionally lands last. The uniform direction here reinforces the piece's priors without doing it through explicit argument.

**What the evidence actually supports:** The piece's evidence supports the rebuttals. The issue is architectural, not factual.

**Recommended neutralizing edit:**
- At one or two junctures, give the government defence the concluding sentence. Example at line 41-45: "That is one reading. It is not the only one. Before testing it, the words the premier chose are worth noting: the judge wrote the recommendation; the judge asked the Legislature to raise the seat count to 91. That is also what the government did."
- Pattern-break the order once, and the cumulative effect relaxes.

### MED-05. "The reading of page 66 the government did not cite" — rhetorical close that editorializes the finding

**Passage (verbatim):** `report_public.md:270`
> That is the reading of page 66 the government did not cite.

**Bias type:** editorializing on a finding

**What a hostile reader of the right would say:** The piece has just laid out a thorough reading of Miller's addendum (lines 258-268). That reading is the finding. Closing with "the reading of page 66 the government did not cite" converts an evidentiary section into a gotcha. The evidentiary section can stand on its own. The closing sentence is commentary.

**What the evidence actually supports:** That the government cited part of page 66 and not other parts. The author's paragraph already makes this clear.

**Recommended neutralizing edit:**
- Before: "That is the reading of page 66 the government did not cite."
- After: Delete the line. The preceding paragraph ends strongly on "explicitly written against what the April 16 committee is positioned to produce."

### MED-06. Samson and Miller's credentials are partial, Clark's is full — small but visible asymmetry

**Passage (verbatim):** `report_public.md:81`
> The majority were Miller, Greg Clark of Calgary (former Alberta Party MLA, nominated by NDP leader Naheed Nenshi), and Susan Samson of Sylvan Lake (also NDP-nominated). They submitted an 89-seat map. The minority were John D. Evans, KC, of Lethbridge and Dr. Julian Martin of Sherwood Park, both UCP-nominated.

**Bias type:** credentials applied asymmetrically

**What a hostile reader of the right would say:** Evans gets "KC" (King's Counsel). Martin gets "Dr." (the academic title). Clark gets his former-MLA status AND his nominator's party affiliation. Samson gets no credential and no political background. A charitable reading is that Samson's professional background is less relevant to the reader. A less charitable reading — which a UCP reader will reach — is that Clark's credibility is established in detail because he becomes a critical witness later (line 262, the X post on elected officials drawing maps), while the minority's credentials are brought forward neutrally.

**What the evidence actually supports:** That all four commissioners have credentials. Clark was the leader of the Alberta Party for a time; Samson is a former Sylvan Lake mayor — a credential the piece omits.

**Recommended neutralizing edit:**
- Before: "Susan Samson of Sylvan Lake (also NDP-nominated)"
- After: "Susan Samson, former mayor of Sylvan Lake (also NDP-nominated)"
- Parallel structure with Clark. Closes the gap.

### MED-07. "What she did not read out" — focuses on omission as a partisan act

**Passage (verbatim):** `report_public.md:15` and `report_public.md:260`
> She cited that recommendation. She did not read that sentence.

And:
> What she did not read out is the sentence a paragraph later...

**Bias type:** framing / implicit motive attribution

**What a hostile reader of the right would say:** Politicians routinely cite documents selectively — it is what all of them do in Question Period. The piece makes Smith's selective citation a repeated motif (lines 15 and 260). The same scrutiny is not applied to Nenshi's "full-on assault" framing, which compresses a week of complex procedural developments into three words, or to Notley's op-ed framing her own decision as the clean template (line 37). All three speakers are being rhetorical. Only Smith is framed as being caught.

**What the evidence actually supports:** That Smith cited page 66 without reading the disavowal sentence. The author can note this once. Naming it twice, and with the motif "she did not" in both instances, is a choice.

**Recommended neutralizing edit:**
- Consolidate the two mentions into one. Keep the first (line 15, which sets up the page 66 theme) and paraphrase the second. At line 260: "Smith's citation stopped short of the next sentence: 'My majority colleagues do not agree with me on this point.' "
- Same content, less finger-wagging.

## Low findings

### LOW-01. "Three scenes. Three signatures." — narrative patterning doing evidentiary work

**Passage (verbatim):** `report_public.md:156, 240`
> Three scenes. Three signatures.
>
> Three signatures. Concentrated in one map. Not the majority's.

**Bias type:** rhetorical architecture

**What a hostile reader of the right would say:** The piece leans on the number three — three hypotheses, three scenes, three findings-that-reversed-my-prior, three signatures. The rhythm is good. But at line 240 ("three signatures, concentrated in one map") the cumulative effect is that three tests found the same verdict — which they did, but the tests were chosen to be three. The weak counter-tests (majority symmetry) are run; they also return null. The null returns on the counter-tests do not get their own "three" moment. A more disciplined rhythm would note symmetrically: "three signatures detected in the minority; three counter-tests run on the majority; all null."

**What the evidence actually supports:** The finding stands. The rhetorical rhythm is fine.

**Recommended neutralizing edit:**
- Small: at line 240, "Three signatures. Concentrated in one map. Three counter-tests on the majority map, all null."

### LOW-02. "A 12.2-percent gap, drawn straight from the commission's own tables" — technically accurate, rhetorically sharp

**Passage (verbatim):** `report_public.md:126`
> A 12.2-percent gap, drawn straight from the commission's own tables.

**Bias type:** loaded phrasing

**What a hostile reader of the right would say:** "Drawn straight from" carries the implication of "caught in the act." The number is the number. The phrase "the commission's own tables" is accurate; "straight from" is the editorial flourish.

**Recommended neutralizing edit:**
- Before: "A 12.2-percent gap, drawn straight from the commission's own tables."
- After: "A 12.2-percent gap, from the commission's population tables."

### LOW-03. "Borrowing algorithmic legitimacy without earning it"

**Passage (verbatim):** `report_public.md:292`
> A committee that uses AI privately and publishes only the output is borrowing algorithmic legitimacy without earning it.

**Bias type:** loaded language

**What a hostile reader of the right would say:** "Borrowing without earning" assigns motive to a hypothetical committee that has not yet produced a map. The author is entitled to argue for publication of prompts and seeds; the motive attribution adds nothing but tone.

**Recommended neutralizing edit:**
- Before: "...is borrowing algorithmic legitimacy without earning it."
- After: "...claims the neutrality of an ensemble without showing the work."

### LOW-04. "A rounding error at that spread" — dismissive of NDP voters whose seat does turn on the shift

**Passage (verbatim):** `report_public.md:308`
> A one-to-three-seat shift is a rounding error at that spread.

**Bias type:** dismissal pattern

**What a hostile reader of the right would say:** The piece's own kicker then walks this back — "Ask the 2023 NDP candidate in Calgary-Acadia about five one-hundredths of a percentage point" (314). A seat is a seat; the individuals in the seats are not a rounding error. A UCP reader and an NDP reader would both take the same view here: if it is a rounding error, it is not worth the three-signature case. The piece makes both claims and lives with the tension. That is a defensible authorial choice, not a bias issue per se, but a hostile reader *of either side* has ammunition in the tension.

**Recommended neutralizing edit:**
- Softer dismissal: "A one-to-three-seat shift does not close an eleven-seat gap."

## INFO / observations

### INFO-01. Adjectives that survived scrutiny

"Engineered supermajority" appears at line 21 as a question ("Is Alberta watching a gerrymander, an override, an engineered supermajority") and the piece then spends 300 lines answering "no, not a supermajority" (line 324). That is honest framing — the piece admits it is testing a claim it ended up rejecting. The opening use is set up for the reversal. This is not bias; it is the piece's built-in discipline.

Similarly, "full-on assault on our democracy" is attributed to Nenshi (line 17), not ratified by the author. The piece's conclusion does not say "assault on democracy"; it says "process concerns, measurable-but-small map concerns, no supermajority." The quote stays Nenshi's.

### INFO-02. The piece names and adjudicates its own error

The Rocky Mountain House section (138-152) is the strongest piece of insurance in the whole article. It opens with "I was working from the wrong numbers" and walks the error through, in full, to the reader's face. A pro-government reader who hits this paragraph and walks away cannot credibly say the piece is a stitch-up. Keep this section exactly as it is.

### INFO-03. The "Limits" section is the piece's other strongest defence

Lines 348-358 concede every reasonable UCP counter-argument: the map is not extreme, the majority is not neutral, the override is not established as unconstitutional, the Lunty committee's map does not yet exist. This is a model of disciplined scope. Keep the section exactly as it is.

## Cross-cutting patterns observed

1. **Rebuttals land last.** Across three junctures (lines 41-45, 148-150, 224), Smith's or the minority's position is stated and then rebutted in the same paragraph. The cumulative architectural effect is that the reader's last impression is always the rebuttal. The piece does not reciprocate — no rebuttal of the author's own finding lands *after* the finding, except in the limits section at 348.

2. **Omission is scrutinized one direction.** "What she did not read out" / "She did not read that sentence" (lines 15, 260) repeatedly flag Smith's selective citation. Nenshi's and Notley's rhetorical compressions receive no parallel treatment even though the piece's own conclusions (line 324) show their framing to be over-sized.

3. **Majority rationales are adopted; minority rationales are tested.** The majority's rural-preservation framing is ratified (line 224); the minority's schools and population math are cross-checked and fail (lines 248-252); the minority's historical-precedent rationale is paraphrased dismissively (line 146). The Calgary zone gap is presented as a choice that reveals intent ("one map sees a zone gap you could drive a truck through, and the other does not") without parallel scrutiny of how the majority's 0.4-percent Calgary balance was achieved — which may itself have required deliberate redistribution that a symmetric audit would call out.

4. **The chair receives two framings.** At line 79 he is the neutral LGIC appointee; at line 322 he is listed alongside "two NDP-nominated commissioners." The slippage matters because the piece's strongest finding (the addendum disavowal) relies on Miller's disavowal being understood as a chair-level, not NDP-side, verdict.

5. **Voter portraits identify with one audience.** The Airdrie voter (line 97) is urban-professional, female, civically engaged. The Calgary scene voters (line 124) "shop at the same Costco" and "commute on the same ring road." Both portraits select for a specific Alberta Views reader demographic — urban, middle-class, engaged. A Bighorn MD farmer, a Strathmore small-business owner, and a Stoney First Nation member are named only in aggregate.

## Where the piece is disciplined and even-handed

The piece's insurance against bias accusations is substantial. Five strong points:

1. **Overt prior declaration** at line 23. The author names what he expected going in.

2. **Three reversals against prior** (line 25): Canmore-Banff cleared, partisan direction flips under 2019 voters and April 2026 polling, chair's "no support" claim holds mostly. All three survive into the final piece. An author who wanted to build a hit piece would have buried these.

3. **Section 15(2) re-audit, transparent** (lines 140-152). The piece shows its error on Rocky Mountain House in public. This is the single best defence against "stitch-up" accusations.

4. **The limits section** (348-358) concedes every reasonable UCP counter-point: not extreme, geography-driven tilt exists, not a constitutional violation, Lunty committee can still be clean.

5. **The supermajority verdict** (324) explicitly rejects the framing Nenshi and Notley used and that the piece quoted at the top. The piece says "the word 'supermajority' fits no tested scenario" — against the Opposition leader's own phrasing. That sentence alone wins back a lot of ground with a UCP reader.

The residual bias flagged above is mostly in language, framing order, and one factual/labelling slip (CRIT-01). None of it reaches the evidentiary level. A disciplined revision of the six highest-severity items — the CRIT-01 attribution error, the "retort / tell" rhetorical move, the Nenshi-Smith quote asymmetry, the "because-we-did-it-before" paraphrase, the "engineered" label on a retracted test, and the uncross-checked rural-preservation framing — would close the gap between the piece's evidence discipline and its language discipline. With those six fixes the piece would hold up against a hostile pro-government reading.
