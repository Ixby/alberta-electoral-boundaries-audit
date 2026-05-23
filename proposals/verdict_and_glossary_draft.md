# Verdict + Glossary — Editorial Draft

**Status:** DRAFT. Pre-implementation editorial content for the content-restructure proposal. Every word is a starting point for your edit, not a final position. The voice aims for high-school-educated, civically curious, no prior knowledge of redistricting, no political prior — and follows the empower-don't-advocate principle from `proposals/content_restructure.md`.

---

## Part 1 — Hero verdict block (`/`, above the fold)

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
- Q3 deliberately states what the audit *has* measured (the 50/50 result) and what it has *not* yet measured (behaviour at other vote shares). The earlier draft asserted a likelihood differential "at the same level of provincial support" — but the audit hasn't tested vote shares other than 50/50, so that phrasing overreached. The current draft is narrower and honest about the limit, which is the kind of constraint that earns the reader's trust in everything else.
- The supermajority effect is now narrow and concrete: at 58 of 87 seats (mathematically 2/3 × 87 = 58), a governing party can waive notice periods and accelerate bills through multiple stages in a single day. Standard legislation and budgets only need a simple majority; the 58-seat threshold is the one that unlocks *procedural* shortcuts. The earlier draft said "the opposition loses much of its procedural power to hold the government accountable" — too broad. The current phrasing names the specific capabilities and lets the reader judge their weight.
- "Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit." — explicit hand-off. The empower-don't-advocate principle in one sentence.
- Italics on *minority proposal* and *majority proposal* the first time each appears. These are common words being used in a specific procedural sense; the italics signal that.
- The two CTA buttons should be visually distinct from each other and from the main text — e.g., one in the `/law` accent color, one in the `/methods` accent color.

**Identified research gap (raised in review):**

The seats@50/50 result and the tipping-point statistic both measure behaviour at the 50/50 vote split. They do not establish how the minority proposal behaves at other plausible vote shares (e.g., 48/52, 47/53). The substantive question — *does the minority proposal make it materially easier for one party to reach a two-thirds supermajority at the vote shares Albertans actually deliver?* — is exactly what this audit needs to answer in order to fully support the kind of verdict the public is asking for.

This is an analytical extension, not a content question. The existing ensemble of 1.01M maps presumably contains the simulated district-by-district vote data needed to compute seats-vs-vote-share curves under various uniform-swing assumptions. If the data supports it, the test is:

1. For each of the 1.01M neutral comparison maps, plus the minority proposal and the majority proposal, apply a uniform swing across a range of vote splits (say, 45/55 → 55/45 in 1% steps).
2. At each split, compute the seat count for each party.
3. Plot the proposal's curves on top of the ensemble distribution. Identify the vote-share range over which the minority proposal sits in the supermajority region while the ensemble does not.

If that test produces results that hold up, Q3 can be tightened to make a claim about the vote-share range — "from X% to Y%, the minority proposal puts one party past the two-thirds supermajority threshold; the majority proposal does not." That's the verdict the public discourse is asking for.

If the test produces ambiguous results, Q3 stays in its current honest-about-limits form.

**Status:** flagged as a follow-up. Out of scope for this content-restructure proposal. Tell me if you want me to scope it as its own proposal in `proposals/`.

---

## Part 2 — Epistemic boundary card (`/`, immediately below the verdict)

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

## Part 3 — Glossary (`viewer/src/lib/glossary.ts`)

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

## Part 4 — Open editorial choices

Things to settle before the glossary ships:

1. **"Gerrymander" — capitalization and italics.** Currently lowercase in body text. AP and CP style both treat it as lowercase. Confirming.
2. **"Riding" vs "electoral district" — resolved.** *Riding* is the federal term; *electoral district* (or "ED") is the provincial term and the right word for an Alberta audit. **Implementation note:** during content migration, normalize *riding* → *electoral district* / *ED* across the entire existing prose. Each route defines "electoral district (ED)" on first occurrence, then uses *ED* thereafter for readability. The *riding* glossary entry exists to catch readers who arrive with the wrong word and gently correct them.
3. **Naming — resolved.** The site uses *minority proposal* and *majority proposal* throughout. A short footnote attaches to the first occurrence on `/`:

   > *The "majority" and "minority" names come from a 3–2 split among the Electoral Boundaries Commission (chaired by Justice Miller), which produced two competing proposals rather than a single recommendation. A separate MLA committee chaired by Brandon Lunty — a Premier-appointed MLA — is now choosing between them before the November 2026 deadline.*

   That establishes the chain of authority (commission → competing proposals → Lunty committee → legislature) once, in one place, so deeper sections don't need to keep re-explaining it.
4. **Whether to name the parties in the verdict.** Currently it says "one party" — not naming UCP or NDP. Pros: keeps the audit neutral, lets the reader's mental model fill in either party. Cons: a reader who already knows the politics will read "one party" as evasive. The existing site does name UCP and NDP throughout. Decision: name them in the lived examples on `/`, but in the verdict block keep "one party" — the verdict is about structure, not partisanship.
5. **UCP/NDP glossary entries — added.** Short factual entries with no editorial framing.
6. **CTA order — keeping current.** *Read the legal context →* appears before *See how we tested →* because that matches the recommended depth order (narrative → law → science) you endorsed earlier. A reader who wants the answer fastest reads the verdict and stops; a reader who wants context next reaches the legal framing before the methodology. Override if you'd rather lead with the math.

---

## Part 5 — What's not in this draft (deliberately)

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
