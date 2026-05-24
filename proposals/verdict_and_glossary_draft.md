# Verdict + Glossary — Editorial Draft

**Status:** DRAFT. Pre-implementation editorial content for the content-restructure proposal. Every word is a starting point for your edit, not a final position. The voice aims for high-school-educated, civically curious, no prior knowledge of redistricting, no political prior — and follows the empower-don't-advocate principle from `proposals/content_restructure.md`.

---

## Part 1 — Document opener (`/`, very top of page, above the verdict)

A short first-person paragraph in the author's voice. Sits at the very top of `/`, immediately above the verdict card. Sets the tone — inclusive, party-neutral, foundational — before any structural finding lands.

---

> ### Who's this for?
>
> Us. All of us. Rural, Urban, curious, wonk, journalist, lawyer, academic, politician — all of us. Because it impacts all of us. Whether or not you like the party in power, what the split commission produced has never been done before. And it's given us the opportunity to peer inside the machine in ways we never could before. Now we can establish a baseline — a series of tests, and everything that comes after can be graded on it. Let me show you what I found.

---

**Editorial notes:**

- First person ("us," "let me show you what I found") and singular author voice — distinct from the institutional third-person of the audit's findings sections. The voice is intentional: it signals that a person did this work, takes responsibility for it, and is inviting the reader in. The shift to third-person evidential voice begins at the verdict card immediately below.
- The audience list ("Rural, Urban, curious, wonk, journalist, lawyer, academic, politician") is the answer to anyone who suspects the audit is coded for one side. Naming every plausible reader on the list neutralises that suspicion before the verdict's structural findings arrive. The repeated "all of us" is rhetorical anchoring, not redundancy.
- "Whether or not you like the party in power" is the explicit party-neutrality move. The audit's findings happen to grade the minority proposal harshly; the opener names that anyone, including supporters of the governing party, can read what follows without being asked to change sides. Combined with the three-question lens in Section 5, this is the strongest available defence against partisan-coding accusations.
- "What the split commission produced has never been done before" is a factual claim — the 3–2 EBC split producing two competing proposals rather than a single recommendation is genuinely unprecedented in Alberta's redistricting history. The footnote on the verdict's Q1 already establishes the chain of authority; this sentence is the consequence the reader should sit with.
- "Peer inside the machine" frames the audit as a tool that creates visibility, not as a verdict imposed from outside. "Establish a baseline — a series of tests, and everything that comes after can be graded on it" positions the work as foundational: this isn't just an opinion on the 2026 cycle, it's a yardstick for every cycle after. That framing is the most credible long-term argument for why a curious citizen should care, regardless of how this particular cycle resolves.
- "Let me show you what I found" is the explicit hand-off into the verdict card. Personal, direct, and one beat before the structural evidence lands.
- Light copyediting was applied to the author's draft (typos: Wether → Whether, commision → commission, oppurtunity → opportunity, "A series of test" → "A series of tests", "politician.." → "politician —"). The author's voice, rhythm, and capitalisation choices (Rural / Urban capitalised; the rest lower-case) are preserved exactly.

---

## Part 2 — Hero verdict block (`/`, above the fold)

A single bordered card. Three questions, three short answers. Two routing CTAs at the bottom. Sits above the cover map.

---

> ### Is the proposed map a gerrymander?
>
> "Gerrymander" is not a term Canadian courts use. But if it were — in the everyday sense most people mean by it — the evidence in this audit would reasonably support calling the *minority proposal*, if enacted, a heavily gerrymandered map. Every structural test this audit runs flags the minority proposal; none flag the alternative (the *majority proposal*).
>
> ### What does "gerrymander" mean in Canadian law?
>
> It doesn't. The Canadian test is different: whether the boundaries give voters *effective representation* under section 3 of the Charter. The minority proposal raises serious questions under that test; only a judge can answer them definitively, and no one has asked one yet.
>
> ### What does it mean for Albertans?
>
> At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme — fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because at 58 of 87 seats — a two-thirds supermajority — the governing party unlocks extraordinary procedural powers: it can waive standard notice periods and push public bills through multiple legislative stages in a single day, bypassing deliberation checks that normally constrain it. Whether the minority proposal's tilt is large enough to push one party past that 58-seat threshold at vote shares *other* than 50/50 is a question this audit has not yet tested. Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit.
>
> **[Read the legal context →](/law)**  ·  **[See how we tested →](/methods)**

---

**Editorial notes:**

- The verdict's Q1 uses a doubly-conditional construction ("if gerrymander were a Canadian legal term, in the everyday sense, the evidence would support…") to answer the question the reader is actually asking without literally calling the proposal a gerrymander. The audit cannot apply a term Canadian law doesn't have. But it can describe what the evidence would support if that term were available, and it can do so in the same plain-language frame the reader is using.
- "If enacted" — second conditional. The minority proposal hasn't been adopted; it's a discarded commissioners' submission that the Lunty committee may forward to the legislature.
- "It doesn't" — Q2's one-sentence opening. Direct, accurate, and immediately reframes to the *effective representation* test.
- Q3 deliberately states what the audit *has* measured (the 50/50 result) and what it has *not* yet measured (behaviour at other vote shares). Naming the limit explicitly — rather than asserting a likelihood differential at vote shares the audit hasn't tested — is the kind of constraint that earns the reader's trust in everything else.
- The supermajority effect is named narrowly and concretely: at 58 of 87 seats (mathematically 2/3 × 87 = 58), a governing party can waive notice periods and accelerate bills through multiple stages in a single day. Standard legislation and budgets only need a simple majority; the 58-seat threshold is the one that unlocks *procedural* shortcuts. Naming the specific capabilities lets the reader judge their weight; a broader claim about "the opposition losing accountability" would overstate what the supermajority actually enables.
- "Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit." — explicit hand-off. The empower-don't-advocate principle in one sentence.
- Italics on *minority proposal* and *majority proposal* the first time each appears. These are common words being used in a specific procedural sense; the italics signal that.
- The two CTA buttons should be visually distinct from each other and from the main text — e.g., one in the `/law` accent color, one in the `/methods` accent color.

**Identified research gap — scoped as a proposal:**

The `seats@50/50` result and the tipping-point statistic both measure behaviour at the 50/50 vote split. They do not establish how the minority proposal behaves at other plausible vote shares (e.g., 48/52, 47/53). The substantive question — *does the minority proposal make it materially easier for one party to reach a two-thirds supermajority at the vote shares Albertans actually deliver?* — is what would let Q3 be tightened from "the audit has not yet tested" to a concrete vote-share range.

A pre-execution proposal now exists at `proposals/cross_vote_share/` (status PREP COMPLETE, NOT AUTHORIZED). It reuses the canonical uniform-swing algorithm against the existing 1.01M-plan ensemble and the per-district vote artifacts for both proposals — no new ensemble run required. The pre-registration amendment is drafted but unsigned; the parameter grid (UCP share {0.45, …, 0.55} in 1% steps), the finding criteria, and the publish-regardless commitment are all pinned in advance so the result cannot be reframed post-hoc.

If the test is authorized and run, Q3 gets one additional sentence naming the vote-share range at which each proposal crosses 58 seats. If the test produces a null (both proposals stay inside the ensemble's central 95% band across the full grid), Q3 gets a narrowing sentence — "extreme at 50/50, symmetric across 45–55%." Either result is publishable. Until the PI authorizes the run, Q3 stays in its current honest-about-limits form.

---

## Part 3 — Epistemic boundary card (`/`, immediately below the verdict)

A smaller, plainer card. Two columns: what the audit can say vs. what it can't. Reads in 30 seconds. Establishes credibility by acknowledging limits before any deeper claim is made.

---

> ### What this audit can and can't tell you
>
> | | |
> |---|---|
> | ✓ | Fewer than 1 in 14.5 million randomly generated comparison maps produced patterns as extreme as the minority proposal on all four statistical measures combined. |
> | ✓ | The minority proposal fails 5 of 5 pre-registered structural tests. The majority proposal fails 0 of 5. |
> | ✓ | These results are consistent with maps that produce strong partisan effects, and inconsistent with what the random comparison set produces. |
> | ✗ | The audit does *not* establish that any commissioner intended the partisan effects it measures. Boundary geometry cannot reveal intent. |
> | ✗ | The audit does *not* predict what the Lunty committee will choose, what the November 2026 vote will be, or how Albertans will react. |
> | ✗ | The audit does *not* predict how a court would rule if a Charter challenge were brought against either proposal. |
> | ✗ | The audit does *not* tell any individual voter what position to take or what to do with this information. That's yours to decide. |

---

**Editorial notes:**

- The asymmetry (3 "can" rows, 4 "can't" rows) is deliberate. Limits matter more for an audit's credibility than findings do. A reader who finishes this card knows what they can and can't rely on.
- The last "can't" row is the empowerment principle stated as the audit's own boundary. It's the bridge into "How to engage."
- "Fewer than 1 in 14.5 million" — kept verbatim from the existing site. It carries weight that a smaller, more recent-feeling number would not.
- "Consistent with maps that produce strong partisan effects" — phrased to avoid implying intent ("targeted" would carry agency). The structure of the sentence still conveys the asymmetry: the minority proposal looks like the partisan-effect cluster of the comparison set, not the neutral cluster.

---

## Part 4 — Section 1 onboarding (`/`, immediately below the boundary card)

The first piece of body prose after the verdict and the boundary card. The reader arrives knowing nothing — possibly without a clear sense of what an electoral district is, who their MLA is, or why a map matters. This section onboards them in ~400 words. No statistical jargon. No legal jargon. Second-person. Empower-don't-advocate.

---

> ### What is redistricting and why should you care?
>
> Every voter in Alberta lives in an *electoral district* — a slice of the province that elects one person to the legislature. There are 87 districts. Each district elects one MLA. When you cast a ballot in a provincial election, you are choosing the MLA for the district you live in. That is the entire connection most Albertans have to the legislature: one MLA, one district, one vote.
>
> Those district lines are not permanent. People move, neighbourhoods grow, rural areas thin out, cities sprawl. Every eight to ten years, Alberta is supposed to redraw the lines so each district is roughly the right size and reflects the way Albertans actually live now. The body that does the redrawing is the *Electoral Boundaries Commission* — an independent commission with judges, lawyers, and public members, not politicians.
>
> That is the standard process. This time, the standard process produced something unusual. The commission's five members split 3–2 on what the map should look like, and rather than settling on one recommendation they produced two: a *majority proposal* (backed by three commissioners) and a *minority proposal* (backed by two). Both are sitting on the table. A separate committee of MLAs chaired by Brandon Lunty — appointed by the Premier for this specific decision — is choosing between them. The legislature must approve whichever one survives that committee before November 2026.
>
> Why it matters to you: the lines decide who your MLA is. They decide which neighbourhoods, towns, and concerns get represented together. If your city is split across four MLAs instead of one, no single representative is accountable for the city as a whole. If your community of interest — a small town, a rural region, a downtown core — is divided between districts, your voice on provincial decisions is diluted. The map also shapes which party can form a government, and at what margins. The audit's specific finding (that the minority proposal sits at a structural extreme) is the reason you are reading this site, but the broader question is older and applies to every redistricting cycle: do the lines reflect the way Albertans live, or do they shape the politics that follow?
>
> The rest of this page walks through what the two proposed maps actually do.

---

**Editorial notes:**

- The opening sentence starts where the reader is, not where the technical material is. "A slice of the province that elects one person to the legislature" replaces any phrasing like "geographic area returning one MLA" — same meaning, plainer words. The reader who doesn't know what an MLA is gets a working definition in the next sentence ("each district elects one MLA"), and the Tier 1 glossary entry catches anyone who needs more.
- "One MLA, one district, one vote." — establishes the personal stake before any structural argument. The reader should feel implicated by the time the redistricting machinery is introduced.
- "Every eight to ten years, Alberta is supposed to redraw the lines…" — "supposed to" is doing real work. It signals that the process has a normative shape (independent, periodic, neutral) without yet alleging it has been violated. The verdict argues that; this onboarding section sets up the standard the verdict measures against.
- The pivot "That is the standard process. This time, the standard process produced something unusual." is the article's whole thesis in two sentences. The reader who stops here still leaves with the right shape of the story.
- The 3–2 commission split and the Lunty committee chain of authority are stated *in prose* here, not just in the verdict's footnote. The reader who skipped the footnote still gets the provenance. Both anchors (footnote on `/` Q1, prose paragraph in Section 1) reinforce each other.
- "Why it matters to you" — paragraph 4 is the personal-to-provincial ladder previewed. Section 5 ("What this means for you and your community") will expand each rung; this paragraph is the trailer.
- The closing question — "do the lines reflect the way Albertans live, or do they shape the politics that follow?" — is deliberately a question, not a thesis. The audit answers part of it (the minority proposal's structural extremes); the broader question is older and bigger than any one cycle. Framing it as a question rather than an answer is the empower-don't-advocate principle applied to the section's last line.
- "The rest of this page walks through what the two proposed maps actually do." — explicit hand-off to Section 2 (The Map) and Section 3 (Two Maps, One Commission, One Deadline). The reader knows where they're going.

---

## Part 5 — Section 5 personal-to-provincial ladder (`/`, mid-page)

The biggest piece of new prose on `/`. Sits after Section 4 ("What the Minority Map Does on the Ground" — existing content, to be condensed during implementation) and before Section 6 ("A short history of gerrymandering" — also new). Five short subsections, ~180 words each, that walk the reader from their own ballot up to the legislature. Empower-don't-advocate throughout: every claim is a description the reader can verify, not a position they're being asked to adopt. Each subsection ends with a question or pivot that hands the next rung to the reader.

---

> ### What this means for you and your community
>
> Set aside, for a moment, the question of which party gains or loses seats. Politicians and parties tend to frame this as a fight over power concentration in the legislature, and at that scale it is. But power concentration in the legislature is not where you experience these maps. You experience them through three concrete questions about your own district:
>
> 1. **Where does your MLA live?**
> 2. **Are they invested in your community?**
> 3. **Will the demands of the head dominate the demands of the tails?**
>
> Every other framing — partisan advantage, supermajority threshold, statistical extreme — eventually points back to those three. The five rungs below walk through how each proposed map answers them, at five scales.
>
> #### You.
>
> Your electoral district decides who represents you in the legislature. Right now you live in one of 87 districts. Under both proposed maps you may live in a different one — possibly with a different MLA, possibly anchored to different neighbouring communities. If you don't know what district you're in right now, or who your MLA is, you're not alone: most Albertans couldn't name their MLA. But the boundary lines are not abstract. They decide whose phone number is on your local representative's office wall, whose neighbourhood petition gets your name attached to it, whose concerns your MLA hears about first. The postal-code lookup on this site shows which district you sit in under each proposal. If your district changes, your representative changes — and your representative's relationship to your community changes with it.
>
> #### Your community.
>
> Communities are not abstract either. A high school's catchment area, a chamber of commerce, a faith community, a neighbourhood association — these are real groupings of people with shared local concerns. When a boundary line cuts through them, no single MLA is responsible for the whole. Take Airdrie under the minority proposal: a city of about 74,000 people sliced into four electoral districts, each anchored to a different rural hinterland. No single representative is accountable for Airdrie as a city. The same dynamic plays out anywhere a town, neighbourhood, or recognised community of interest is split — the bigger the split, the weaker the representation. The audit measures *municipal anchoring* (what fraction of each district's perimeter follows existing municipal lines), and the minority proposal scores notably lower than the majority on that test.
>
> #### Your municipality.
>
> When a city is fractured across many representatives, its ability to bargain on provincial decisions weakens. A council asking for transit funding, a school board negotiating a new school, a mayor lobbying for highway extensions — each of those goes better when the city can point to a few MLAs who owe accountability to the city as a whole. The minority proposal splits Calgary's northwest quadrant across multiple districts whose vote-share patterns suggest *packing* (concentrating one party's voters into a few high-margin seats) on top of *cracking* (splitting the other party's voters across many low-margin seats). Whether the pattern is intentional is a question the audit cannot answer — boundary geometry doesn't reveal intent. What it can say is that the four statistical measures flag the same districts that the structural tests flag, and that the alternative proposal does not produce the same fingerprint.
>
> #### Your region.
>
> If you live outside Alberta's cities you have probably noticed that political conversations about boundaries always seem to centre the cities. That's a fair complaint, so let's be direct about what this audit does and does not say about rural Alberta.
>
> What it does **not** say: that rural Alberta has too many seats. The EBCA allows district populations to vary by up to 25% so that one rural MLA isn't representing a geography the size of southern France. Canadian courts treat that variance as legitimate. Both proposed maps preserve it. Nothing in this audit changes that.
>
> What it **does** say: in several places on the minority proposal, rural communities are being attached as the *tail* of a district whose population centre sits in a city. Look at how the minority proposal handles Airdrie — a city of about 74,000 sliced into four districts, each one extended out into a different stretch of rural countryside. The population centre of each new district is the urban slice, not the rural tail. An MLA elected from that kind of district is most likely to live, campaign, and prioritise where the votes are — which means rural communities formerly represented by a dedicated rural MLA become the back half of an urban-led seat. That pattern repeats on the minority proposal in ways it does not on the majority proposal.
>
> The audit doesn't propose taking seats away from rural Alberta. It asks whether the lines respect the rural communities those seats are meant to represent, or whether rural geography is being used as ballast to absorb urban votes into districts whose centre is somewhere else. If you live in one of those rural tails, the question of which map gets enacted decides whether your MLA represents the rural community you actually live in, or an urban district whose lines happen to include your land.
>
> #### Your province.
>
> The legislature is what you get when you sum every district's answers to the three questions above. If most districts are anchored to communities whose MLAs actually live in them, the legislature represents those communities. If most districts have rural tails attached to urban heads, the legislature represents the heads — and the tails get whatever attention is left over. The partisan question — which party wins a majority — is downstream of that. The supermajority question — whether one party crosses 58 of 87 seats and unlocks procedural shortcuts like waiving notice periods or accelerating bills through multiple stages in a single day — is downstream of *that*. At a hypothetical 50/50 provincial split, the audit's measurements place the minority proposal at a structural extreme: fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. Whether that imbalance pushes a party past 58 seats at the vote shares Albertans actually deliver is a question this audit has not yet directly tested; the verdict at the top of this page is honest about the gap. Whether the answer to any of these questions matters enough to act on is, again, a question for you.

---

**Editorial notes:**

- The framing paragraph that opens the section names the partisan/legislature frame as *the parties' frame* and offers three lived-reality questions in its place. The questions are deliberately reader-owned ("your MLA," "your community," "the tails" — the reader fills in their own place on the ladder). The audit's value-add over the parties' framing is precisely this: the audit measures geometry, and geometry decides residence, investment, and head-vs-tail, all of which the partisan framing obscures. Stating that contrast at the top of the section makes the rest of the ladder land as answers to questions the reader is already asking, not lectures.
- Question 3 ("Will the demands of the head dominate the demands of the tails?") is the structural one. It applies symmetrically: an urban-headed district with rural tails (the Airdrie pattern) treats rural voters as the tail; a rural-headed district with a suburban tail would treat suburban voters the same way. The audit measures the geometry; the reader names which side they sit on. Empower, don't advocate.
- "The 'You → Your community → Your municipality → Your region → Your province' ladder" is the structure that makes a 900-word block readable. Each rung is the next-largest scale; each ends with a hand-off to the next; each is short enough to read in 30 seconds. A reader who stops anywhere on the ladder still leaves with a complete frame for the rung they stopped on — and the three-question lens at the top works at every rung.
- "You" leads with the postcode lookup because that's the only action a reader can take without first agreeing with anything. The audit's empowerment principle starts with "give the reader the tool" before "make the argument."
- "Your community" anchors the Airdrie example — the canonical lived case the existing prose already uses. Importing it here keeps the new section consistent with the rest of `/` and means the reader has seen the example once before the deeper section gets into the structural mechanics. The municipal-anchoring metric is glossed inline so a reader who skipped the glossary still gets a working definition.
- "Your municipality" introduces *packing* and *cracking* in passing — they're in the Tier 1 glossary, so a click-popover reader gets the definitions; a glossary-skipper still picks up the rough meaning from the parenthetical. The "intent vs. fingerprint" caveat is repeated here because it's the single most important epistemic boundary in the audit, and the deeper-section reader needs it at the moment they meet the packing/cracking framing.
- "Your region" addresses a real obstacle for rural readers: a reader who already feels under-represented by the current system will hear a "fair-maps" argument as urban-coded — "they're trying to strip the cities of the structural advantages they finally have." If the section doesn't acknowledge that perception directly, it loses the rural reader inside the first sentence. The rung opens by naming the perception ("political conversations about boundaries always seem to centre the cities — that's a fair complaint") and then makes the rural case from the rural side rather than the urban side.
- Two-move structure — *what the audit does NOT say* (rural seats are not being taken away; 25% variance preserved by both maps) and *what it DOES say* (the minority proposal uses rural communities as anchors for urban slices). Saying NOT first is what earns the right to be heard on the DOES.
- Airdrie does double duty in the section: in "Your community" it shows what an urban split looks like from the city side; in "Your region" the same split is reframed from the rural side as "rural countryside becomes the back half of an urban-led seat." Two readings of the same geometry. The unified frame across the two rungs — hybrid districts hurt whoever is the smaller half — is the strongest single argument in the section.
- The "geography the size of southern France" line is kept as the concrete hook for the 25% variance; it does work for any reader who has never thought about Alberta's geography in comparative terms.
- "An MLA elected from that kind of district is most likely to live, campaign, and prioritise where the votes are" — phrased as a likely outcome rather than a certainty. The audit can measure the geometry; the representation-quality implication is a reasonable inference, not a measurement, and the prose calibrates accordingly.
- The closing question — "decides whether your MLA represents the rural community you actually live in, or an urban district whose lines happen to include your land" — is deliberately phrased so the answer depends on which map gets enacted, not on which party the reader supports. Reader empowerment, not advocacy.
- "Your province" presents the legislature as the **sum** of every district's answers to the three questions, not as a separate top-down partisan-power story. The partisan-majority question is "downstream of that"; the supermajority question is "downstream of *that*." That ordering matches what the audit actually measures (district-level geometry) and what it has not (vote-share-conditional seat behaviour). Leading with "the lines shape who governs" would import the parties' framing — the very frame the section's opener sets aside.
- The supermajority point appears in this rung as one of several downstream consequences, not as the rung's punchline. It needs to be named because Q3 of the verdict names it; flagging it as a question the audit has not yet answered at the relevant vote shares keeps the section's voice consistent with the verdict's honesty.
- Italics on jargon terms (*packing*, *cracking*, *municipal anchoring*, *two-thirds supermajority threshold*) signal "this is a defined term; the popover has more" without breaking the reading rhythm.
- The whole section assumes Section 4 has already shown the Airdrie split visually on the map. If implementation reorders the page, Airdrie either needs a one-line picture-the-scene addition here or the section needs a glance-back link to Section 4.

---

## Part 6 — Glossary (`viewer/src/lib/glossary.ts`)

33 terms grouped by tier. Each entry has:
- `term` — the canonical capitalized display form
- `definition` — 2–3 sentences, plain language, no math notation, no Latin where avoidable
- `href` — anchor on `/law` or `/methods` for "Learn more →"

Tier indicates where the term *first appears* in the site flow. A term may appear on multiple routes; the popover content is the same everywhere.

### Tier 1 — appears on `/` (the curious-reader route)

```ts
electoralDistrict: {
  term: 'Electoral district (ED)',
  definition: 'The geographic area that elects one member to the provincial ' +
              'legislature. Often shortened to "ED" after first use. Each ED has ' +
              'one MLA. (The word "riding" usually refers to federal districts; ' +
              'in the provincial context the proper term is electoral district.)',
  href: undefined,
},

riding: {
  term: 'Riding',
  definition: 'In Canadian usage, this most often refers to a federal electoral ' +
              'district. The Alberta provincial equivalent is called an "electoral ' +
              'district" (ED). The audit uses the provincial term throughout.',
  href: undefined,
},

mla: {
  term: 'MLA',
  definition: 'Member of the Legislative Assembly — the person elected from one ' +
              'electoral district to represent it in the Alberta legislature.',
  href: undefined,
},

ucp: {
  term: 'UCP',
  definition: 'United Conservative Party — Alberta\'s current governing provincial ' +
              'party. Formed in 2017 from the merger of the Progressive Conservatives ' +
              'and the Wildrose Party; has held government since 2019.',
  href: undefined,
},

ndp: {
  term: 'NDP',
  definition: 'New Democratic Party (Alberta NDP) — Alberta\'s current official ' +
              'opposition. The Alberta NDP held government from 2015 to 2019.',
  href: undefined,
},

gerrymander: {
  term: 'Gerrymander',
  definition: 'A map drawn so that one political party wins more seats than its share ' +
              'of the vote would suggest. The word comes from an 1812 Massachusetts ' +
              'district shaped like a salamander. It is not a legal term in Canada, ' +
              'but the concept is widely studied.',
  href: '/#history-of-gerrymandering',
},

cracking: {
  term: 'Cracking',
  definition: 'A gerrymandering technique that splits a voting bloc across many ' +
              'districts so it never reaches a majority in any single one. For example, ' +
              'dividing a city across four ridings so its voters are outnumbered in each.',
  href: '/methods#cracking-packing-draining',
},

packing: {
  term: 'Packing',
  definition: 'A gerrymandering technique that concentrates one party\'s voters into ' +
              'a small number of districts. The party wins those districts overwhelmingly ' +
              'but "wastes" many votes — leaving fewer of its voters available to compete ' +
              'in other districts.',
  href: '/methods#cracking-packing-draining',
},

draining: {
  term: 'Draining',
  definition: 'A term this audit uses for a follow-on effect of cracking and packing: ' +
              'the wasted votes those techniques produce get pushed into strategically ' +
              'chosen places, altering the political character of nearby electoral ' +
              'districts. It is the audit\'s own framing rather than an established ' +
              'concept in the redistricting literature — the audit tests for the effect ' +
              'and finds results consistent with it, but treats it as exploratory ' +
              'rather than a settled methodology.',
  href: '/methods#cracking-packing-draining',
},

anchoring: {
  term: 'Anchoring',
  definition: 'How firmly the proposed boundaries follow existing municipal lines ' +
              '(city limits, town boundaries). A highly anchored map mostly respects ' +
              'those lines; a loosely anchored map departs from them often — especially ' +
              'at politically meaningful spots, which is a structural warning sign.',
  href: '/methods#anchoring',
},

charterSection3: {
  term: 'Section 3 of the Charter',
  definition: 'The section of the Canadian Charter of Rights and Freedoms that ' +
              'guarantees citizens the right to vote. Canadian courts have interpreted ' +
              'it not as a strict "one person, one vote" rule but as a right to ' +
              '"effective representation."',
  href: '/law#section-3',
},

effectiveRepresentation: {
  term: 'Effective representation',
  definition: 'The standard Canadian courts apply when judging electoral boundaries. ' +
              'It means voters should have a meaningful voice — not just numerical ' +
              'equality of riding populations, but also recognition of community ties, ' +
              'geography, and minority representation. The leading statement is from ' +
              'the Supreme Court of Canada\'s 1991 Saskatchewan Reference.',
  href: '/law#effective-representation',
},

ebc: {
  term: 'Electoral Boundaries Commission (EBC)',
  definition: 'The body that draws Alberta\'s provincial electoral boundaries under ' +
              'the EBCA. The 2026 commission was chaired by Justice Miller and ' +
              'split 3–2 among its commissioners, producing two competing ' +
              'proposals (the majority and minority proposals) rather than a single ' +
              'recommendation.',
  href: '/law#ebc',
},

luntyCommittee: {
  term: 'Lunty committee',
  definition: 'An MLA committee chaired by Brandon Lunty — an MLA appointed by ' +
              'the Premier — that is choosing between the EBC\'s majority and ' +
              'minority proposals before the November 2026 deadline. The committee ' +
              'is separate from the EBC; the legislature created it for this ' +
              'specific decision and it is not part of the standard EBCA process.',
  href: '/law#committee-anomaly',
},

ebca: {
  term: 'EBCA',
  definition: 'The Alberta Electoral Boundaries Commission Act — the law that ' +
              'governs how electoral boundaries are drawn in the province. It sets ' +
              'up the commission, the public-hearing process, and the rules for when ' +
              'a new map takes effect.',
  href: '/law#ebca',
},

fsa: {
  term: 'Forward sortation area (FSA)',
  definition: 'The first three characters of a Canadian postal code (the ' +
              'letter-digit-letter part). About 270 FSAs cover Alberta. Most fall ' +
              'entirely within a single electoral district.',
  href: undefined,
},
```

### Tier 2 — appears on `/law` (the engaged-reader route)

```ts
saskatchewanReference: {
  term: 'Saskatchewan Reference',
  definition: 'The 1991 Supreme Court of Canada decision (formally Reference re ' +
              'Provincial Electoral Boundaries (Sask.)) that set the modern Canadian ' +
              'test for electoral fairness. Chief Justice McLachlin wrote the majority ' +
              'opinion, establishing "effective representation" as the s.3 standard.',
  href: '/law#saskatchewan-reference',
},

parityOfVotingPower: {
  term: 'Parity of voting power',
  definition: 'The principle that every voter\'s ballot should count roughly equally. ' +
              'Canadian law treats this as one factor in effective representation rather ' +
              'than an absolute requirement — districts can vary in population for ' +
              'legitimate reasons (geography, community of interest), but not without limit.',
  href: '/law#parity',
},

communityOfInterest: {
  term: 'Community of interest',
  definition: 'A group of people who share common ground — neighbourhood, language, ' +
              'economy, or shared local concerns — and benefit from being represented ' +
              'together. Canadian courts treat it as a legitimate reason to depart from ' +
              'strict equal-population rules when drawing electoral boundaries.',
  href: '/law#community-of-interest',
},

standing: {
  term: 'Standing',
  definition: 'In law, the right to bring a case to court. For a Charter challenge ' +
              'to electoral boundaries, a court must first decide whether the person ' +
              'bringing the case has a direct enough stake — usually a voter affected ' +
              'by the boundaries, or sometimes an organization with public-interest standing.',
  href: '/law#standing',
},

charterChallenge: {
  term: 'Charter challenge',
  definition: 'A court case asking a judge to declare a law or government action ' +
              'incompatible with the Canadian Charter of Rights and Freedoms. If ' +
              'successful, the law or action can be struck down or sent back to be redrawn.',
  href: '/law#charter-challenge',
},

defaultAdopt: {
  term: 'Default-adopt',
  definition: 'The rule in some provinces and at the federal level that says: if the ' +
              'legislature doesn\'t act on a commission\'s report by a deadline, the ' +
              'commission\'s recommendation takes effect automatically. Alberta\'s ' +
              'process leaves the decision to the legislature instead, which is one ' +
              'of the structural distinctions this audit examines.',
  href: '/law#default-adopt',
},

quebecCRE: {
  term: 'Quebec CRE',
  definition: 'The Commission de la représentation électorale du Québec — Quebec\'s ' +
              'permanent, independent body that draws provincial electoral boundaries. ' +
              'Unlike Alberta\'s process, Quebec requires a two-thirds legislative ' +
              'majority to override the CRE\'s recommendations.',
  href: '/law#quebec-contrast',
},

bcEBC: {
  term: 'BC EBC',
  definition: 'The British Columbia Electoral Boundaries Commission — BC\'s ' +
              'periodically-constituted body that recommends provincial boundary ' +
              'changes. Like federal commissions, BC operates under a default-adopt ' +
              'rule: the legislature must act explicitly to reject the commission\'s ' +
              'recommendations rather than to accept them.',
  href: '/law#bc-contrast',
},

federalCommissions: {
  term: 'Federal boundary commissions',
  definition: 'Independent commissions established once per decade after each census ' +
              'to redraw federal electoral districts in each province. They operate ' +
              'under the Electoral Boundaries Readjustment Act with a default-adopt ' +
              'rule and a structured public-hearing process.',
  href: '/law#federal-contrast',
},
```

### Tier 3 — appears on `/methods` (the analyst/scholar route)

```ts
efficiencyGap: {
  term: 'Efficiency gap',
  definition: 'A measure of how "wasted" each party\'s votes are. Every vote over 50% ' +
              'in a winning district, and every vote for a losing candidate, counts as ' +
              'wasted. The gap is the difference between the two parties\' wasted-vote ' +
              'shares; political scientists treat anything above about 7% as a sign of a ' +
              'partisan-tilted map.',
  href: '/methods#efficiency-gap',
},

meanMedian: {
  term: 'Mean-median gap',
  definition: 'The difference between a party\'s average vote share across districts ' +
              'and its middle (median) vote share. A small gap suggests the party\'s ' +
              'voters are evenly spread; a large gap suggests they\'re bunched into a ' +
              'few high-margin districts in a way that wastes votes.',
  href: '/methods#mean-median',
},

declination: {
  term: 'Declination',
  definition: 'A geometric test that looks at how district-level vote shares are ' +
              'arranged on a chart. The closer the line connecting them stays to flat, ' +
              'the more neutral the map; sharp angles signal that the map is treating ' +
              'the two parties\' votes unequally.',
  href: '/methods#declination',
},

seatsFiftyFifty: {
  term: 'Seats at 50/50',
  definition: 'A thought experiment: if the province voted exactly 50/50 between the ' +
              'two parties, how many seats would each party get under this map? In a ' +
              'fair map, the answer is close to half. A large gap is a structural ' +
              'signature of a partisan map.',
  href: '/methods#seats-fifty-fifty',
},

mcmc: {
  term: 'MCMC (Markov chain Monte Carlo)',
  definition: 'A computer technique for generating many random examples from a ' +
              'complicated set of possibilities. Here, it\'s used to draw a huge sample ' +
              'of plausible alternative electoral maps to compare the actual proposed ' +
              'map against.',
  href: '/methods#mcmc',
},

recom: {
  term: 'ReCom (recombination)',
  definition: 'The specific algorithm used to generate the alternative maps in this ' +
              'audit. Starting from a valid map, ReCom repeatedly merges two adjacent ' +
              'districts and re-splits them at random — producing a different but ' +
              'still-valid map. Repeating this generates the comparison set.',
  href: '/methods#recom',
},

ensemble: {
  term: 'Ensemble',
  definition: 'The full collection of alternative maps generated for comparison — ' +
              '1,010,000 in this audit. The actual proposed map\'s measurements are ' +
              'compared against the spread of measurements across the ensemble.',
  href: '/methods#ensemble',
},

percentile: {
  term: 'Percentile',
  definition: 'Where a value falls within a ranked list, expressed from 0 to 100. ' +
              'If a map is at the 99.99th percentile for efficiency gap, that means ' +
              'it sits above 99.99% of the random comparison maps — extremely far ' +
              'from the typical.',
  href: '/methods#percentile',
},

pValue: {
  term: 'p-value',
  definition: 'The probability that a result this extreme would occur by chance, ' +
              'if there were nothing unusual going on. A small p-value means ' +
              '"unlikely to be a coincidence." It does not by itself prove anyone ' +
              'intended the result — only that random chance is an unlikely explanation.',
  href: '/methods#p-value',
},

lane1: {
  term: 'Lane 1',
  definition: 'The audit\'s statistical-outlier lane. Tests in Lane 1 compare the ' +
              'proposed map\'s measurements against the 1,010,000-map random sample ' +
              'and ask whether the proposed map is unusually extreme.',
  href: '/methods#lane-1',
},

lane2: {
  term: 'Lane 2',
  definition: 'The audit\'s pre-registered structural lane. Tests in Lane 2 check ' +
              'whether the proposed map fails specific structural criteria the audit ' +
              'committed to in advance — independent of any statistical comparison. ' +
              'Lane 2 is the audit\'s primary evidence.',
  href: '/methods#lane-2',
},

szat: {
  term: 'SZAT (swing-zone allocation test)',
  definition: 'A test that checks how a map allocates districts in "swing zones" — ' +
              'areas where elections are competitive. A neutral map distributes ' +
              'swing-zone districts roughly proportionally; a partisan map allocates ' +
              'them unevenly between the two parties\' favourable territory.',
  href: '/methods#szat',
},

hillClimbing: {
  term: 'Hill-climbing test',
  definition: 'A targeted-procedure test that asks: starting from a neutral map, ' +
              'how much partisan tilt can you produce by only making changes that the ' +
              'proposed map\'s choices appear to favour? It confirms whether the ' +
              'proposed map\'s pattern matches what a targeted, intentional process ' +
              'would produce — without claiming anything about actual intent.',
  href: '/methods#hill-climbing',
},
```

---

## Part 7 — Open editorial choices

Things to settle before the glossary ships:

1. **"Gerrymander" — resolved.** Lowercase in body text. AP and CP style both treat it as a common noun (the eponym is centuries old and naturalized). No italics except on first occurrence where the audit is naming the term itself rather than using it.
2. **"Riding" vs "electoral district" — resolved.** *Riding* is the federal term; *electoral district* (or "ED") is the provincial term and the right word for an Alberta audit. **Implementation note:** during content migration, normalize *riding* → *electoral district* / *ED* across the entire existing prose. Each route defines "electoral district (ED)" on first occurrence, then uses *ED* thereafter for readability. The *riding* glossary entry exists to catch readers who arrive with the wrong word and gently correct them.
3. **Naming — resolved.** The site uses *minority proposal* and *majority proposal* throughout. A short footnote attaches to the first occurrence on `/`:

   > *The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. A separate MLA committee chaired by Brandon Lunty — a Premier-appointed MLA — is now choosing between them before the November 2026 deadline.*

   That establishes the chain of authority (commission → competing proposals → Lunty committee → legislature) once, in one place, so deeper sections don't need to keep re-explaining it.
4. **Whether to name the parties in the verdict.** Currently it says "one party" — not naming UCP or NDP. Pros: keeps the audit neutral, lets the reader's mental model fill in either party. Cons: a reader who already knows the politics will read "one party" as evasive. The existing site does name UCP and NDP throughout. Decision: name them in the lived examples on `/`, but in the verdict block keep "one party" — the verdict is about structure, not partisanship.
5. **UCP/NDP glossary entries — added.** Short factual entries with no editorial framing.
6. **CTA order — keeping current.** *Read the legal context →* appears before *See how we tested →* because that matches the recommended depth order (narrative → law → science) you endorsed earlier. A reader who wants the answer fastest reads the verdict and stops; a reader who wants context next reaches the legal framing before the methodology. Override if you'd rather lead with the math.

---

## Part 8 — What's not in this draft (deliberately)

- **Section transitions and lead-in text.** Each route's section-by-section prose comes in a later editorial pass; this draft is just the verdict, the boundary card, and the defined vocabulary that the rest of the site will reference.
- **References list (academic + legal).** Already exists in the current site and migrates wholesale.
- **The "How to engage" copy block.** Depends on `engagement.json` schema being defined first (see open question #2 in `content_restructure.md`).
- **Verdict block visual treatment.** Color, border, typography are CSS questions; this draft only fixes the language.

---

## Sign-off questions

- Does the verdict block answer the question a curious Albertan is actually asking when they land on `/`?
- Is the boundary card too long, too short, or roughly right?
- Are there terms in the glossary that should be cut (already self-explanatory) or merged?
- Are there terms that should be added (jargon you know you use that isn't here)?
- Is any glossary definition too academic, condescending, or off-key?
