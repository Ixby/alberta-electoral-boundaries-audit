# Verdict + Glossary — Editorial Draft

**Status:** DRAFT. Pre-implementation editorial content for the content-restructure proposal. Every word is a starting point for your edit, not a final position. The voice aims for high-school-educated, civically curious, no prior knowledge of redistricting, no political prior — and follows the empower-don't-advocate principle from `proposals/content_restructure.md`.

---

## Part 1 — Hero verdict block (`/`, above the fold)

A single bordered card. Three questions, three short answers. Two routing CTAs at the bottom. Sits above the cover map.

---

> ### Is the proposed map a gerrymander?
>
> One of the two maps under consideration — the *minority* map — shows clear signs that it would be one. Every structural test this audit runs flags the minority map; none flag the alternative (the *majority* map).
>
> ### What does "gerrymander" mean in Canadian law?
>
> Canada doesn't use the word in court. Our test is different: whether the boundaries give voters *effective representation* under section 3 of the Charter. The minority map raises serious questions under that test; only a judge can answer them definitively, and no one has asked one yet.
>
> ### What does it mean for Albertans?
>
> If the minority map were adopted, the math suggests that a 50/50 provincial vote would still produce a supermajority for one party in the legislature. The majority map produces a much more balanced result at the same vote split. Whether that tradeoff is acceptable is a question for Albertans, not for this audit.
>
> **[Read the legal context →](/law)**  ·  **[See how we tested →](/methods)**

---

**Editorial notes:**

- "Clear signs that it would be one" rather than "is one" — preserves the audit's epistemic stance (we measure structure, not intent).
- "Only a judge can answer them definitively, and no one has asked one yet" — flags that a Charter challenge is hypothetical, prevents the reader from inferring that litigation is underway.
- "Whether that tradeoff is acceptable is a question for Albertans, not for this audit" — explicit hand-off to the reader. The empower-don't-advocate principle in three words.
- Italics on *minority* and *majority* the first time each appears. These are common English words being used in a specific technical sense; the italics signal that.
- The two CTA buttons should be visually distinct from each other and from the main text — e.g., one in the `/law` accent color, one in the `/methods` accent color.

**Alternates to consider:**

- *"…would still produce a supermajority"* — a punchier version: *"would still hand a supermajority to one party."* Slight loss of neutrality; the verb "hand" implies a recipient. The current "produce" keeps it mechanical.
- The closing question of #3 could be removed (`Whether that tradeoff…`) for brevity. Keeping it because it's the one sentence on the page that names the reader's role.

---

## Part 2 — Epistemic boundary card (`/`, immediately below the verdict)

A smaller, plainer card. Two columns: what the audit can say vs. what it can't. Reads in 30 seconds. Establishes credibility by acknowledging limits before any deeper claim is made.

---

> ### What this audit can and can't tell you
>
> | | |
> |---|---|
> | ✓ | Only about 7 of the 1,010,000 randomly generated comparison maps produced patterns as extreme as the minority map on all four statistical measures combined. |
> | ✓ | The minority map fails 5 of 5 pre-registered structural tests. The majority map fails 0 of 5. |
> | ✓ | These results are consistent with what a partisan-targeted map would look like, and inconsistent with what the random comparison set produces. |
> | ✗ | The audit does *not* establish that any commissioner intended the partisan effects it measures. Boundary geometry cannot reveal intent. |
> | ✗ | The audit does *not* predict what the Lunty committee will choose, what the November 2026 vote will be, or how Albertans will react. |
> | ✗ | The audit does *not* predict how a court would rule if a Charter challenge were brought against either map. |
> | ✗ | The audit does *not* tell any individual voter what position to take or what to do with this information. That's yours to decide. |

---

**Editorial notes:**

- The asymmetry (3 "can" rows, 4 "can't" rows) is deliberate. Limits matter more for an audit's credibility than findings do. A reader who finishes this card knows what they can and can't rely on.
- The last "can't" row is the empowerment principle stated as the audit's own boundary. It's the bridge into "How to engage."
- "About 7 of 1,010,000" is more accessible than the existing "fewer than 1 in 14.5 million." The two phrasings express the same fact; the first one is easier to picture.
- "Consistent with… and inconsistent with…" is careful language. It doesn't say "this map was drawn to be a gerrymander"; it says "this map looks like ones that are, and not like ones that aren't."

---

## Part 3 — Glossary (`viewer/src/lib/glossary.ts`)

27 terms grouped by tier. Each entry has:
- `term` — the canonical capitalized display form
- `definition` — 2–3 sentences, plain language, no math notation, no Latin where avoidable
- `href` — anchor on `/law` or `/methods` for "Learn more →"

Tier indicates where the term *first appears* in the site flow. A term may appear on multiple routes; the popover content is the same everywhere.

### Tier 1 — appears on `/` (the curious-reader route)

```ts
electoralDistrict: {
  term: 'Electoral district',
  definition: 'The geographic area that elects one member to the provincial legislature. ' +
              'In Alberta these are also called "ridings" or "constituencies." Each ' +
              'electoral district has one MLA.',
  href: undefined, // no deeper page; the definition is complete
},

riding: {
  term: 'Riding',
  definition: 'Informal Canadian term for an electoral district. Used interchangeably ' +
              'with "constituency" and "ED."',
  href: undefined,
},

mla: {
  term: 'MLA',
  definition: 'Member of the Legislative Assembly — the person elected from one ' +
              'electoral district to represent it in the Alberta legislature.',
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
  definition: 'A gerrymandering technique that shifts a district\'s political character ' +
              'by altering its boundaries — for example, extending a riding into ' +
              'uninhabited land, or splitting it along non-municipal lines to remove ' +
              'specific voter blocs.',
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

luntyCommittee: {
  term: 'Lunty committee',
  definition: 'The MLA committee, chaired by Brandon Lunty, that is choosing between ' +
              'the commission\'s majority and minority map proposals before the ' +
              'November 2026 deadline. It is not part of the standard Electoral ' +
              'Boundaries Commission Act process; the legislature created it for ' +
              'this specific decision.',
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
2. **"Riding" vs "electoral district" — pick one in the body text.** Both have entries above so the reader sees them both. The narrative voice on `/` could go either way. *Riding* is more conversational and Canadian; *electoral district* matches official language. Suggestion: use *riding* in `/` body text and *electoral district* on `/law` and `/methods`.
3. **"Majority/minority commissioners" vs "majority/minority map."** The current site uses both. The verdict block uses the *map* phrasing because the *commissioners* phrasing tempts readers to score the people. Recommend standardizing to *map* throughout, with one explicit footnote on `/` that the names come from the 3–2 commission split.
4. **Whether to name the parties in the verdict.** Currently it says "one party" — not naming UCP or NDP. Pros: keeps the audit neutral, lets the reader's mental model fill in either party. Cons: a reader who already knows the politics will read "one party" as evasive. The existing site does name UCP and NDP throughout. Decision: name them in the lived examples on `/`, but in the verdict block keep "one party" — the verdict is about structure, not partisanship.
5. **Whether to include UCP/NDP at all in the glossary.** Currently not included. The site assumes the reader knows what these are. For the high-school-educated curious Albertan, that's a defensible assumption. If not, two short entries are cheap to add.
6. **Order of "How we tested →" vs "Read the legal context →"** in the verdict CTAs. Current order matches the narrative-law-science depth ordering, so law first.

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
