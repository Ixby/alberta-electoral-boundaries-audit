# Two Maps, Then None: Inside Alberta's 2026 Boundary Audit

*A plain-language summary of the 2025–26 Electoral Boundary Commission forensic audit, and what the audit will measure next.*
*v0.23 — April 25, 2026 — [Full monograph](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/report_academic.md)*

---

An Airdrie resident pulls up the new electoral map on her phone. Her street goes to one riding. Two blocks over goes to another. Under one of the two competing proposals from Alberta's 2026 boundary commission — the one signed by the two dissenting commissioners — her city of 84,000 is cut into four pieces, each quarter attached to a different surrounding region. Nothing about Airdrie changed. Only the map did.

This audit is about that map, the alternative proposal three other commissioners signed, and a third map a legislative committee in Edmonton is drawing right now. It uses two kinds of evidence — *partisan-fairness numbers* (whether the math comes out lopsided) and *structural patterns* (whether the lines themselves are drawn in unusual ways) — kept separate so each can be judged on its own.

A *gerrymander*, in this article, means a boundary choice that gives one political side an advantage beyond what the rules require. Intent cannot be read off a map. What can be measured are effects.

A note before reading: on April 16, the government set both commission maps aside and assigned the redrawing to a legislative committee. Neither map this article analyzes is a candidate to become law. The article is about what those maps reveal about the process that produced them, and about the standard the November committee map will be measured against.

---

## The short version

Alberta's Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Both are legal under the *Electoral Boundaries Commission Act*. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). This audit measured both maps using the same methods, applied identically. Three findings stand out.

1. **The two maps differ on six things you can measure without looking at any election results:** how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's own chair flagged as anomalous. The minority map differs from the majority on every one of them.

2. **The direction runs against the places where the governing party is weakest.** Calgary's northwest quadrant, the City of Airdrie, urban areas with established municipal boundaries — the communities most affected by the minority map's structural differences are the same ones where the governing party's opponents are strongest. The audit cannot determine intent. It can measure effect.

3. **The process now promoting the minority map has no precedent in Canada.** No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP).

> The process is its own finding, separate from the maps.

---

## The April 16 decision

The *Electoral Boundaries Commission Act* lets the government refer the commission's recommendations to a legislative committee. On April 16, the government did this. The new committee — chaired by Brandon Lunty, UCP MLA for Leduc-Beaumont — has five members. Three from the governing UCP, one from the New Democratic Party (NDP), one from the Alberta Party. It must report by November 2, 2026 with a 91-seat map.

The referral followed the letter of the Act. It also confirms Alberta's outlier status: most provinces require the legislative assembly to consider a commission report before any referral can take effect; Alberta does not. Most provincial commissions are chaired by a sitting or retired judge whose tenure is protected; Alberta's chair is a public appointee who can be replaced mid-mandate by a cabinet decision.

Three Canadian comparator pivots show what "departing from norm" looks like in practice:

- **Quebec, 1992:** the National Assembly debated and amended the commission's report, then passed it. The drafting process stayed with the commissioners; the legislature only changed specific lines, on the record.
- **Ontario, 1996:** Mike Harris's government cut 130 ridings to 103 by adopting the federal map. A structural change, not a partisan one, with cross-party committee participation.
- **British Columbia, 2008:** a tied commission tabled both reports; MLAs picked one on a free vote. The drafting was not handed to a new body.

None of the three substituted a government-chaired drafting body for the commission partway through the cycle. That is what Alberta did on April 16.

**Six days after the Alberta motion, the Supreme Court of Canada ruled against Quebec for doing something parallel.** On April 22, 2026, the SCC dismissed Quebec's appeal of a Quebec Court of Appeal ruling that had struck down the Legault government's 2024 law blocking Quebec's independent electoral-boundaries commission from redrawing the provincial map. The ruling was delivered from the bench — without reserved judgment — by a 7–2 majority. The Court of Appeal's holding the SCC upheld: the freeze law violated sections of the Charter that guarantee democratic representation by allowing significant disparities in voter weight to persist. The freeze had been justified on rural-representation grounds (Quebec's CAQ government and other parties argued the redrawing would weaken Gaspé and other rural ridings). The constitutional doctrine: a provincial legislature cannot block an independent commission's redistricting work in order to preserve voter-weight disparities, even when the justification is regional representation.

Alberta's April 16 motion is now operating against a constitutional landscape that has, six days later, become significantly less hospitable to legislative override of independent commission work. Whether the Alberta situation is constitutionally distinguishable from Quebec's is for the courts to decide; the audit's own framing simply notes that the parallel has now been adjudicated against.

---

## How the audit measures gerrymandering

A gerrymander is a deliberate boundary choice that advantages one political interest over others, beyond what the statutory constraints require. Two methodological problems make this hard to measure honestly.

The first is that there is no single correct Alberta map. The number of legal Alberta maps — those satisfying the *Electoral Boundaries Commission Act*'s rules on population deviation within ±25%, contiguity, compactness, community-of-interest preservation, Indigenous effective representation, and public-hearing input — runs into the astronomical billions. There is no way to test them all. Fairness in this domain is not a discovery; it is a choice among many legitimate alternatives.

The second is that intent cannot be observed from a map. A commissioner could draw a partisan-skewed map either deliberately or by unlucky chance among the legal alternatives. The audit cannot read minds. What it can do is measure *effects* — how the map a commission produced compares to the family of maps a non-partisan procedure would have drawn.

The audit handles both problems with three layered tools.

**A 2,000,000-map computer simulation.** The audit generates two million different legal Alberta maps using a published redistricting algorithm (called ReCom) under the same statutory constraints the commission worked under. The simulation was run at progressively larger sizes (250,000 → 1,000,000 → 2,000,000 maps); each enlargement gave the same answer to within ±0.5 percentile points, and the 2,000,000-map run is the one cited throughout this article. Doubling from one million to two million did not push the ensemble's most extreme map any further toward UCP territory — the simulation's ceiling is not a sampling artifact, it's a real bound on what Alberta's redistricting rules can produce. Each simulated map is scored on the four standard partisan-bias measures. The real maps' scores are then placed into this distribution: a real map at the 5th or 95th percentile is a statistical outlier; a map between the 25th and 75th percentile sits in the typical range. On the four standard partisan-fairness scores, the 2019 enacted map and the 2026 majority map both sit near the 95th-percentile boundary on the same metric — telling the audit what is geography (Alberta's persistent rural-conservative tilt shows up under any map) versus what is drawing (the minority map's structural irregularities, which the majority and 2019 do not share).

**Two reference lines for the efficiency-gap test.** The audit uses two: the famous **7% line** from US case law (Whitford v. Gill, calibrated to US Congressional delegation sizes), and the audit's **~5% Alberta-calibrated line** derived from its own computer simulation. The ~5% line is rounded up from the empirical 4.37% — the 95th percentile of the simulation's efficiency-gap distribution. The exact percentile is in the monograph; the magazine uses ~5% because the threshold is partly a subjective choice (the decision to call p95 "outlier") and the rounded number is honest about that. The Alberta-calibrated ~5% line is the more demanding test, since both lines are above zero and ~5% is closer to neutral. Both 2026 maps exceed ~5% (majority 6.4%, minority 9.2%); only the minority also exceeds 7%.

**A pre-registered structural-irregularity scorecard.** Five tests, committed to in writing on March 14, 2026 — nine days before the commission filed its report and well before any 2026 results were measured: how far the map departs from Canadian comparator norms on municipal-boundary anchoring, how much wider the population spread is, the gap between geographic zones (such as Calgary's NW quadrant), how many boundaries the commission's own chair flagged as anomalous, and how many of the minority's published rationales fail when checked under the same audit method. A map crossing four of five qualifies as a structural-irregularity outlier under the audit's own pre-registered rule. The minority crosses five of five. The majority crosses zero of five.

The combination of these three tools is what produces the two-lane verdict in the next section. No single tool is dispositive. Directional consistency across all three is the audit's inferential standard.

---

## What the audit found across seven measures

The table compares the two maps. The first five rows use no election results — they're properties of the lines themselves. The last two depend on how votes were attributed to each district.

| What was measured | Majority map | Minority map |
|---|---|---|
| Population spread across districts (tighter is better) | 3,180 | **4,707 — 48% wider** |
| NW Calgary population excess above average | 2.8% | **11.5%** |
| Airdrie split | 2 divisions | **4 divisions** |
| Borders that follow existing municipal lines | 71% | **15%** |
| Boundaries flagged by the commission chair | 0 | **3** |
| Efficiency gap (a partisan-fairness measure) | +6.4% | **+9.2%** |
| Packing-cracking neighbourhood pattern | 3 (same as 2019) | **0 — *pre-registered pass*** |

> **VOCABULARY**
>
> **Efficiency gap.** A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour conservatives; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — roughly the level only 5% of computer-simulated Alberta maps cross.
>
> **Anchoring.** The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.

The bottom two rows depend on election results. The *efficiency gap* is a single number that captures how lopsidedly each party's votes get translated into seats: zero is perfectly neutral, positive numbers favour the UCP, negative favour the NDP. A reading of +6.4% means the UCP wins roughly 6.4 percentage points more of the seats than a perfectly fair vote-to-seat translation would give them. Both maps' efficiency gaps favour the UCP — partly because Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) produces a UCP-favourable starting point under any map. But both numbers also exceed the audit's Alberta-calibrated ~5% reference line, and the minority additionally exceeds the older US 7% line. What that means in plain terms: both maps land in the most UCP-leaning slice of what computer-simulated Alberta maps can produce. The verdict section unpacks the consequences.

The last row is where the minority map looks *better* than the majority on a partisan-fairness measure: zero packed-cracked adjacency pairs, against three on the majority and three on the current 2019 map. The audit pre-registered this test before measuring, and the minority's tighter packing-cracking number is a real point in its favour. It is the single test where the minority outperforms the majority.

---

## Three things the minority map does differently {: .new-page }

The table above shows the differences as numbers. Three of them are worth understanding as choices a person made.

**It splits the City of Airdrie into four pieces.** The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — North, East, West, and centre — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers.

> **WHY AIRDRIE MATTERS**
>
> Airdrie is the largest Alberta city without its own MLA. At 84,000 people it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.
>
> Splitting it across four provincial divisions, each of which is *primarily* identified with somewhere else, removes Airdrie from the political map at the level of government that draws it. The city has 84,000 residents and zero seats in the legislature where a majority of voters call the place home.
>
> A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?

> Both maps are legal. The four-way split is a choice.

**It ignores municipal boundaries.** When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. These maps already exist. Statistics Canada publishes the city and town boundaries; any redistricting commission gets them for free. The majority map traces them on 71 of every 100 kilometres of its border. The minority traces them on 15 of 100 — and offers no published reason for the departure. (For comparison, recent Quebec, Ontario, and BC commission maps anchor at 78%, 82%, and 71% respectively. Canada's 70–85% norm comes from these and seven other comparator commissions documented in the monograph.)

**One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.** In Calgary's northwest quadrant, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This is *packing*: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and *cracking* (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.

The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair.

---

## One way to read the scorecard {: .new-page }

Rows of measurements are hard to weigh against each other. One defensible synthesis is a four-category rubric weighted by the principles redistricting law and democratic theory treat as primary.

> **ONE WAY TO READ THE TWO MAPS**
>
> *A proposed synthesis with explicit weights — not a finding. Other weightings give different grades.*
>
> Letter-to-point conversion uses Mount Royal University's full-letter-range midpoints: A = 90, B = 75, C = 65, D = 55, F = 25 (per the MRU undergraduate grading scale: A range 80–100, B range 70–79, C range 60–69, D range 50–59, F range 0–49). The audit author is an MRU undergraduate; using the institution's own grading scale is the most defensible single conversion choice. The overall is each grade × its weight, summed.
>
> | Category | Weight | Majority grade | Majority points | Minority grade | Minority points |
> |---|---:|:---:|---:|:---:|---:|
> | Voter equality | 25% | B | 18.75 | D | 13.75 |
> | Community recognition | 35% | B | 26.25 | F | 8.75 |
> | Map coherence | 25% | A | 22.50 | D | 13.75 |
> | Partisan fairness | 15% | B | 11.25 | B | 11.25 |
> | **OVERALL** | — | **B (79/100)** | | **F (48/100)** | |

**Why these weights.** Community recognition carries the most (35%) because *Reference re Saskatchewan* — the Supreme Court decision defining what redistricting is for — holds that effective representation requires districts that communities can identify as their own. The Act's ±25% population band grounds voter equality at 25%. Map coherence (25%) reflects the commission's own standard: the chair flagged specific boundaries as anomalous, and those flags matter. Partisan fairness is weighted lowest (15%) because both maps clear the audit's Alberta-calibrated ~5% line, but only the minority clears the older US 7% line — the partisan-fairness lane is real but not the lane that distinguishes the maps most sharply.

**What produces the minority's F.** On community recognition (8.75 of 35 under these weights — the lowest single-category score in the table), 15% municipal anchoring means 85 out of every 100 kilometres of the minority map's border cuts through territory voters do not recognize from any other civic map — not their school division boundary, not their property-tax bill, not their local election ward. The majority's equivalent is 71%. The Airdrie four-way split compounds the effect — residents must navigate four legislative offices, each primarily identified with somewhere else. Three chair-flagged anomalies — a lasso-shaped corridor, a boundary extension through uninhabited national park land, and a district named for communities together smaller than the community it actually captures — pull the map-coherence score down further.

**Where the maps score comparably.** Under the lowest-weighted category — partisan fairness — the two maps are effectively tied (both clear the Alberta-calibrated line), even though only the minority clears the US line.

---

## Was either map a gerrymander?

The honest answer needs two lanes.

### Lane 1 — the partisan-fairness numbers

The number Lane 1 produces is called the *efficiency gap*. In plain terms: it measures how lopsidedly each party's votes get translated into seats. Zero is perfectly neutral. A positive efficiency gap of, say, +5% means the UCP wins roughly five percentage points more of the seats than a perfectly fair vote-to-seat translation would give them; a negative number means the same thing in the NDP's direction. A bigger number means a bigger seat-share advantage for one side that the votes alone don't justify.

The audit places two reference lines on the efficiency gap. The **~5% Alberta line** is the audit's own, rounded up from 4.37% — the 95th percentile of the efficiency gap across the 2,000,000 different legal Alberta maps the computer simulation generated. A real map above this line sits in the outermost 5% of what Alberta's redistricting rules can produce. The **7% US line** is the academic-literature reference (*Whitford v. Gill*, calibrated to US Congressional delegation sizes); it has no Alberta-specific authority but is widely cited. Both are *reference lines*, not legal cut-offs — crossing them doesn't make a map illegal, but it does mean the map is statistically unusual relative to what a non-partisan procedure under the same rules would produce.

Where the two 2026 maps land:

![How skewed each map looks on the partisan-fairness number. Both 2026 maps sit beyond the Alberta line at ~5%; only the minority also crosses the US line at 7%. The further right the dot, the more the map favours the UCP relative to its provincial vote share.](data/maps/article/lane1_dotplot.png)

The same picture in numbers — each map's efficiency gap, where it sits relative to the two reference lines, and where it places in the audit's two-million-map simulation:

| Map | Efficiency gap | Above Alberta line (~5%)? | Above US line (7%)? | Percentile in the simulation |
|---|---|---|---|---|
| Majority 2026 | +6.4% | Yes — 1.4 percentage points over | **No** — 0.6 below | **99.9th percentile** (UCP-favoured tail) |
| Minority 2026 | +9.2% | Yes — 4.2 percentage points over | **Yes** — 2.2 over | **100th percentile** (UCP-favoured tail) |

The percentile column reads as follows. **99.9th percentile** means that of the 2,000,000 random legal Alberta maps the audit generated, only about 1 in 1,000 leaned more toward the UCP than the majority map does. **100th percentile** means none of those two million simulated maps leaned more toward the UCP than the minority map does — the minority sits at the absolute ceiling of what the simulation produced. The practical consequence: both real maps are statistical outliers in the UCP-favoured direction; the minority is the most extreme example the simulation can imagine.

**Both maps clear the Alberta line; only the minority clears the US line.** The Alberta line (~5%) is the more demanding test, calibrated to Alberta's actual geography and the *Electoral Boundaries Commission Act*'s constraints. The minority clears both lines. The majority clears only the Alberta line.

**The percentile readings are point estimates, not bounds.** The simulation runs as four parallel chains of 500,000 maps each (2,000,000 total), giving the percentile placements ±0.3 precision.

### Lane 2 — the structural pattern

Lane 1 depends on which election results you score the maps against. Lane 2 does not. The structural evidence is in the maps themselves — drawn lines, split cities, where the boundaries do and don't follow administrative lines that exist for other reasons. On these tests, the two maps are not close.

![The five structural-fairness tests, side by side. Purple bars are the majority map, green bars are the minority map. The dashed red line in each row marks the failing point. The green bars cross every line by a wide margin. The purple bars sit flat at zero or stay well inside the safe range.](data/maps/article/lane2_bars.png)

The same five tests in tabular form, with each test's threshold stated alongside the result. The bottom row is the audit's *summary* — the count of tests each map fails out of the five.

| Test | Majority map | Minority map |
|---|---|---|
| Border follows existing municipal lines (70–85% Canadian norm) | 71% — within norm | **15% — 4.9× below norm** |
| Population spread (tighter is better) | 3,180 | **4,707 — 48% wider** |
| NW Calgary population excess above average | 2.8% | **11.5%** |
| Boundaries flagged by the commission's own chair | 0 | **3** |
| Airdrie split (constraint minimum: 2) | 2 pieces | **4 pieces** |
| **Pre-registered summary** (4 of 5 fired = outlier) | **0 of 5 fired** | **5 of 5 fired** |

A separate finding — applied only to the minority because the minority is the map whose contested redraws are public[^asym] — is that **five of six of the minority commissioners' published rationales fail under independent check**, and **two of the contested redraws have no documented public-submission support** in the commission's archive of 1,140+ submissions. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.)

[^asym]: The majority did not publish a contested-redraw rationale list. The seven-rationale audit cannot be applied symmetrically; it is reported as a single flag, not as additional rows in the structural-irregularity count.

**On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.**

### The rural-representation question

Before going further, the audit owes a direct answer to the strongest defence of the minority map's hybrid urban–rural districts. The minority commissioners themselves state it cleanly in their Appendix E to the commission's final report (pp. 302–303):

> *Hybrid constituencies are not only a good reflection of Alberta, but also the best available instrument for preserving rural and suburban representation in the face of sustained urban growth. They avoid the false choice between (a) underrepresenting Calgary and Edmonton, and (b) creating ever-larger purely rural districts that become geographically unmanageable.*

That argument deserves a fair test against the data — and it has now also been adjudicated. The Supreme Court of Canada, on April 22, 2026, dismissed Quebec's appeal of a Quebec Court of Appeal ruling that struck down Quebec's 2024 attempt to freeze its electoral map on similar regional-representation grounds. The 7–2 ruling, delivered from the bench, held that legislative interference with independent commission redistricting work — even when justified on regional-protection grounds — violates Charter section 3 by allowing significant disparities in voter weight to persist. The minority commissioners' rural-protection argument is now operating against Canadian constitutional doctrine that has, in the most recent SCC ruling on the question, gone the other way.

There are two ways a map can protect rural representation. The first is the way the *Electoral Boundaries Commission Act* itself provides for: section 15(2) lets up to four electoral divisions be drawn with population *up to 50% below* the provincial average — a deliberate over-representation tool, baked into the statute, specifically to keep small rural communities from being arithmetically swamped. The second is by under-populating rural districts in general (without invoking 15(2)), giving rural voters more weight per ballot. Both mechanisms are visible in the population data the commission published.

How each map handles rural representation:

| Map | s.15(2) special-rural EDs declared | Rural ED average population | Rural-voter weight vs urban (1.0 = equal) |
|---|---|---|---|
| 2019 enacted | (commission didn't tag) | 45,370 (-3.1% below ideal) | **1.044×** — rural voters carry 4.4% more weight |
| 2026 majority | **3** (Canmore-Banff, Central Peace-Notley, Lesser Slave Lake) | 51,057 (-7.1% below ideal) | **1.119×** — rural voters carry 11.9% more weight |
| 2026 minority | **0** (the audit found no s.15(2) declaration in the minority report) | 47,945 (-12.7% below ideal) | **1.229×** — rural voters carry 22.9% more weight |

On the *headline* number — rural-vs-urban representation weight — the minority map looks like the most rural-protective of the three. But the *mechanism* is different from what the Act envisions. The minority's number doesn't come from declaring s.15(2) special-rural districts (it declares none). And it doesn't come mainly from making pure-rural districts smaller (the majority does that more conservatively). It comes from a third lever: **converting urban districts into urban–rural hybrids by attaching pieces of cities to surrounding rural-edge territory.**

The hybrid-district counts make this concrete. The 2019 enacted map has 8 hybrid EDs. The 2026 majority has 9. **The 2026 minority has 25** — almost three times as many. Twelve of the minority's hybrids are *new*: ridings that the majority drew as pure-Calgary, pure-Edmonton, pure-Lethbridge, or pure-Red Deer city seats, but that the minority converted into hybrids by stapling them to suburban or rural-edge territory.

The minority's hybrid expansion is province-wide, not Calgary-only:

- **Calgary (7 new hybrids):** Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, Calgary-North West-Bearspaw, Calgary-Bow-Springbank, Calgary-West-Tsuut'ina, Calgary-Peigan-Chestermere.
- **Lethbridge (4 new hybrids):** Lethbridge-Taber-Warner, Lethbridge-Little Bow, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Cardston. The City of Lethbridge — population 100,000 — has zero pure-Lethbridge ridings on the minority map. Every Lethbridge voter shares an MLA with an out-of-city community.
- **Red Deer (4 new hybrids):** Red Deer-Lacombe, Red Deer-Innisfail, Red Deer-Sylvan Lake, Red Deer-Blackfalds. Same structural pattern: the City of Red Deer is dispersed across four ridings whose names lead with surrounding towns.
- **Edmonton (3 new hybrids):** Edmonton-Spruce Grove, Edmonton-Beaumont, Edmonton-Enoch-Devon.

Whether this third lever counts as "rural protection" depends on what the reader thinks rural protection should do. The Act's lever (s.15(2), -50% deviation) gives existing rural communities more legislative weight without disturbing how cities elect MLAs. The minority's lever does something different: it dilutes urban political identity (the City of Lethbridge has no MLA primarily named for it; the City of Red Deer has no MLA primarily named for it) by spreading city voters across districts whose other members are rural-edge or suburban. The two mechanisms produce different first-order effects: the Act's lever strengthens rural representation; the minority's lever weakens urban representation. They are not equivalent, and the audit's data lets the reader judge which one each map is actually doing.

A second observation worth making honestly: the suburban-edge communities the minority's hybrids attach to (Airdrie, Cochrane, Spruce Grove, Beaumont, Sylvan Lake, Bearspaw, Chestermere) tend to be *more conservative-leaning than the cities they're attached to and less conservative-leaning than the deeper rural areas beyond them*. Adding suburban-conservative voters to urban-edge ridings shifts those ridings' partisan-fairness numbers in the UCP-favourable direction without invoking either the s.15(2) rural-protection lever or the actual rural population that the rural-protection argument is meant to defend. That is the structural mechanism the audit calls *the drain pattern*: urban votes drained into hybrids that shore up suburban-conservative seats, producing what looks (in the rural-vs-urban-weight table above) like rural over-representation but is actually urban dilution.

The audit's reading: **the majority map protects rural representation in the way the Act intends — by under-populating actual rural districts and using the s.15(2) special-rural provision. The minority map's apparent rural-protection number is mostly produced by a different mechanism — urban hybridization — that has the side effect of also improving UCP-leaning seat math without using the statutory rural-protection lever at all.** Either reading is available to the reader; the data is what the data is.

### Five of six of the minority's published reasons fail under check

The contested redraws were selected by the *minority commissioners themselves*: each is one of the boundary choices the minority report singles out and offers a published rationale for. The audit checks each rationale against the data it invokes — and against the methodology files in the [audit's evidence trail](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology). Five fail under independent verification; one stands.

- **Airdrie split four ways.** *Minority commissioners said:* a four-way split was needed to balance population. *Population arithmetic says:* the *Electoral Boundaries Commission Act*'s ±25% population rule requires Airdrie to span at least two divisions, not four. The majority map gives it two and stays inside the rule. The four-way split is a structural choice, not an arithmetic necessity. **Fail.**
- **Cochrane attached to Calgary-Foothills via the Nolan Hill lasso.** *Minority commissioners said:* commuter community of interest. *Statistics Canada Table 98-10-0459 (2021 Census journey-to-work) says:* of 8,550 Cochrane commuters with an Alberta destination, 49.2% work in Cochrane itself; only 35.8% commute to Calgary city-wide, and the data cannot single out Nolan Hill as the destination. The Cochrane–Nolan Hill pairing is not supported. **Fail.**
- **Rocky Mountain House extended into Banff National Park.** *Minority commissioners said:* ranching community of interest. *The Canada National Parks Act* prohibits agricultural tenure on park land, and a polygon-clipped 2021-Census-DA pull on the Banff extension finds no documented year-round-resident population in the strict park-land slice. The "ranching community of interest" rationale has no agricultural land base it can refer to. **Fail.**
- **Olds-Three Hills-Didsbury reaching into North Airdrie.** *Minority commissioners said:* linked agricultural service centres. *The land-use record says:* North Airdrie is suburban residential; Olds and Didsbury are rural service centres. The connection is geographic adjacency, not common interest. **Fail.**
- **Red Deer attached to Sylvan Lake.** *Minority commissioners said:* shared school division. *Alberta Education's published school-division boundaries say:* Sylvan Lake is in Chinook's Edge School Division No. 73; the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools. They are different divisions. The "shared school division" rationale is factually incorrect. **Fail.**
- **St. Albert-Sturgeon.** *Minority commissioners said:* population balancing on Edmonton-corridor constraints. *The convergence test says:* the majority map and the minority map independently arrive at the same St. Albert-Sturgeon two-district structure under the Act's constraints. When two independent drafting teams converge, the configuration is constraint-forced rather than engineered. **Stands.**

The five-failure / one-stand pattern matters. A symmetric audit finding 0 of 6 or 6 of 6 would suggest either no rationale problem or a methodology bias. The asymmetry — five fail, one stands, and the one that stands is the one both maps independently produce — is what distinguishes a real finding from a noise pattern. Each fail is documented with primary-source citations in [the methodology folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology) so a hostile reviewer can check the work.

### The 50/50 test

The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.

In Alberta, the answer is not 50/50. *Across 2,000,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes* — meaning a typical Alberta map under neutral votes actually hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.

The full distribution from the 2,000,000-map simulation:

| Where the map sits | UCP seats at 50/50 votes |
|---|---|
| Median Alberta map | 44.8% (39 of 87 simulated seats) — NDP slight seat majority |
| 95th-percentile map | 48.3% (42 of 87) — still UCP minority |
| 99.9th-percentile map | 49.4% (43 of 87) — just shy of half |
| **Maximum across 2,000,000 maps** | **51.7% (45 of 87)** |

A note on seat counts. The 2026 commission maps each have **89** districts; the audit's computer simulation runs on the **87**-district 2019 map (its starting substrate); the November Lunty committee will produce **91**. All percentages in this article are comparable across these denominators.

Only 1,980 of those 2,000,000 maps — about 0.1% — even reach 50% UCP seats at neutrality. **Zero of two million** reach 52%. The simulation has a hard ceiling around 51.7%.

Now place the three real maps:

| Map | UCP seats at 50/50 votes | Where it sits |
|---|---|---|
| 2019 enacted | 46.0% (40 of 87) | 82nd percentile — inside the normal range |
| Majority 2026 | 43.8% (39 of 89) | 22nd percentile — slightly NDP-favouring, well inside |
| Minority 2026 | **52.8% (47 of 89)** | **Off the chart — above every map in the simulation** |

**The contrast is the cleanest single finding the audit produces.** Of the 2,000,000 simulated Alberta maps, about **1 in 4** produced essentially the same `seats@50/50` value as the **2019 enacted map** (Alberta's actual current law) and about **1 in 5** produced essentially the same value as the **2026 majority map**. **Zero** produced anything close to the **2026 minority map**. Same commission, same statutory rules, same provincial geometry — yet the three reference maps land in radically different places in the simulation. The most defensible single-sentence summary of what the audit found: the 2019 enacted map and the 2026 majority map are the kinds of maps a fair procedure routinely generates; the 2026 minority map is the kind it never does.

Read it carefully. *On a 50/50 vote, the minority map gives the UCP the majority government — by a margin no random legal Alberta map can produce.* The most extreme UCP-favouring map two million simulations could draw tops out at 51.7%, and only 104 of 2,000,000 simulated maps even reach that ceiling. The minority map sits at 52.8% — **above the simulation's ceiling**. The majority map, on the same neutral input, slightly under-delivers the UCP — exactly as you'd expect from a structurally neutral Alberta map.

**This is not a tail finding; it is an out-of-distribution finding.** A statistical outlier sits in the extreme tail of a distribution — say, the top 5% or top 0.1%. The minority map is not in the tail. It is *outside* what the distribution produces. Two million random legal Alberta maps were drawn under the same rules — the same population-deviation limit, the same compactness and contiguity constraints, the same provincial geometry. None of them produced what the minority map produces. The probability that a random legal map matches or exceeds the minority's seats@50/50 result is bounded by the resolution of the simulation itself: **less than 1 in 2,000,000** — less likely than being struck by lightning in any given year (about 1 in 1,200,000 in Canada). And the minority is not just *barely* off the chart: the gap between it and the ensemble's most extreme draw is the same magnitude as the gap between the median map and the 90th-percentile map. In simulation terms, the minority map is a separate species.

**The plain-language version.** *The minority map is legal. It is also the kind of map a fair, neutral drawing procedure does not produce — even when given two million chances — under the same Alberta rules and the same Alberta geometry that produced both the 2019 enacted map and the 2026 majority map without difficulty.* The statutory rules permit it; the kind of process the rules were written to imagine does not generate it.

**One methodology caveat — and two tests the audit ran to settle it.** The simulation used for this finding is *neutral* — the ReCom algorithm samples from the legal-map space without any partisan objective. Neutral procedures have a known bias toward compact maps, and the minority map is not compact (chair-flagged anomalies, lasso-shaped corridors). So the right way to read "0 in 2,000,000" is: zero out of two million draws by a neutral, compactness-preferring procedure produced anything in the minority's range. A *non-neutral* algorithm — one explicitly tasked with maximising UCP seats while staying inside the Act — could in principle reach the minority's range; that is what targeted gerrymandering procedures do. To find out whether it actually does, the audit ran one in each direction.

A short-bursts hill-climbing procedure (Cannon et al. 2022 — the standard tool in the redistricting-statistics literature for exploring biased-but-legal maps) was set loose first with the objective of *maximising* UCP seats at neutral votes, then mirrored with the objective of *minimising* UCP seats (equivalent to maximising NDP seats). Same number of steps in each direction (40,000), same statutory constraints, same provincial geometry.

| Procedure | Most-extreme value reached | What this tells us about the real maps |
|---|---|---|
| Neutral 2M MCMC, max produced | 51.7% UCP seats @ 50/50 | The simulation's natural ceiling on the UCP-favouring side |
| Neutral 2M MCMC, min produced | 37.9% UCP seats @ 50/50 | The simulation's natural floor on the NDP-favouring side |
| Targeted hill-climb, UCP-maximizing | **52.87%** | A non-neutral procedure can reach the minority map's territory (52.8%) when told to aim for it |
| Targeted hill-climb, NDP-maximizing | **37.93%** | A non-neutral procedure can drive seats@50/50 well below where the majority map sits (43.7%) |

The asymmetry is the finding. The **minority** map sits at 52.8% — at the targeted-procedure UCP ceiling, and well above what 2,000,000 neutral draws can reach. The **majority** map sits at 43.7% — comfortably inside both the neutral range (the simulation's median is 44.8%) and the targeted-procedure NDP range (which extends to 37.93%). One map sits where targeted-but-legal procedures have to deliberately aim to land. The other sits where neutral procedures routinely produce. *That* is the troubling shape of the finding, and it is also the framing a court would actually apply.

**The asymmetry around 50/50 is more telling than the inversion itself.** A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about **49.7%**. That is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What *is* dramatic is the contrast: on the **majority** map, the UCP would need to *win* the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.

This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.

**One caveat the audit takes seriously.** A real electorate is not a uniform 50/50. Voters can swamp any map's structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates *the map's contribution to the outcome*, not the outcome itself. What it shows is what the map does when the electorate doesn't decide for it.

### Scoring against current polling

The 338Canada projection on April 12, 2026 (UCP 52.5% / NDP 37.6%) gives the question one more data point. Re-scoring both maps against current polling instead of 2023 actual votes:

| Map | Efficiency gap (2023 actuals) | Efficiency gap (338, April 2026) | UCP seats projected |
|---|---|---|---|
| Majority 2026 | +6.4% | **+8.7%** (worse) | 67 of 89 (75%) |
| Minority 2026 | +9.2% | **+7.0%** (better) | 66 of 89 (74%) |

Under current polling both maps still clear the Alberta-calibrated ~5% line; the majority now also crosses the US 7% line; the two converge on roughly the same number from opposite directions. The ranking between them flips. This is the flickering Lane 1 alone produces — score it against any single election or poll and you get an answer that depends on the electorate's mood that month. The 50/50 test above doesn't flicker. The structural-fairness pattern in Lane 2 doesn't flicker. The same 2,000,000 simulated maps under the same Alberta rules don't move when the polls do. Those are the pieces of the verdict the audit will defend in any year.

### Verdict

The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the map fails, out of five, where higher means more structural problems). The bottom-left corner is "clean on both lanes." The top-right corner is "out of bounds on both lanes."

![The two ways of measuring the maps, plotted together. Left-to-right: how skewed the map looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the map fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 map (purple) drifts right (partisan skew) but stays low (no structural problems). The minority 2026 map (green) sits in the worst corner: high on both.](data/maps/article/verdict_quadrant.png){: .verdict-hero }

The same verdict in plain summary form:

| | Lane 1: Numbers | Lane 2: Structure |
|---|:--:|:--:|
| **Majority 2026** | efficiency gap +6.4% (beyond the Alberta ~5% line) | clean — crosses no structural threshold |
| **Minority 2026** | efficiency gap +9.2% (beyond Alberta ~5% AND US 7% lines) | crosses every structural threshold by a wide margin |

Both maps lean UCP on the partisan-fairness numbers, and the minority leans further. But the *engineering difference* that distinguishes the two maps lives in Lane 2, not Lane 1 — both maps inherit Alberta's structural rural-UCP advantage on partisan-fairness numbers; only the minority crosses every structural threshold.

> **THE PLAIN READING.** On the numbers, both maps clear the Alberta-calibrated ~5% line; only the minority also clears the US 7% line — and the minority map can deliver the UCP a legislative majority even when the UCP narrowly loses the popular vote. On the structural pattern, only the minority map crosses every test by a wide margin. Each of those structural choices has an innocent explanation on its own; together, they form the kind of pattern redistricting researchers flag for further inquiry. Whether the cause was deliberate engineering, unlucky drafting, or both is a judgement call the audit puts in the reader's hands.
>
> We measured the effects. We can't read minds.

> **RETRACTION CONDITIONS**
>
> *If any of these turn out to be true, the verdict above is wrong and gets retracted publicly within 30 days.*
>
> 1. **A counter-map exists.** Someone produces a legal Alberta map satisfying the minority's own community-of-interest reasons (Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park) *and* anchoring on municipal boundaries at majority-comparable rates. Open challenge — [Issue #14](https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14) on the audit's GitHub repository.
> 2. **The Lunty committee map looks like the minority.** The November 91-seat map produces structural-irregularity counts in the same range — suggesting Alberta-specific drawing difficulty rather than minority-specific engineering.
> 3. **A pre-2026 internal commission document surfaces.** Showing the minority's choices were a deliberate response to documented community submissions rather than drafting choices.
> 4. **The 2027 election result, fought on either of these maps, contradicts the percentile readings.** If the partisan-fairness direction the audit projects from 2023 votes turns out to be wrong on actual votes, the Lane 1 finding gets revisited.
> 5. **The Quebec 2026 Supreme Court ruling is materially distinguished by an Alberta court.** If a court reviewing the April 16 Alberta motion finds the Alberta situation is constitutionally distinct from Quebec's — for example, because the Lunty committee is structured differently from a legislative-freeze law, or because Alberta's effective-representation analysis differs from Quebec's — the audit's procedural critique of the motion weakens.

---

## What this audit is now for

In policy terms, the verdicts above are moot — flagged at the top of this article and now confirmed by the structure of what comes next. On April 16 the government set both commission maps aside; Alberta's 2027 map will come from the Lunty committee. Neither commission map is a candidate to become law.

The work itself is not moot. The commission audit calibrated Alberta-specific thresholds — structural-irregularity tests, anchoring comparators, the 2,000,000-map computer ensemble — against three real Alberta maps (the 2019 enacted boundaries plus the two 2026 commission proposals, applied symmetrically). That framework will be re-pointed at the Lunty committee's map the day it is published, reported by the same standard you have just read.

**Two reminders carry over to the November audit, both of which the audit's 2026 numbers underline.** First, *Alberta's geography will always favour conservatives*: NDP voters concentrate in city cores, UCP voters spread across efficient-margin rural ridings, and a neutrally-drawn Alberta map produces a UCP-favourable efficiency gap as a starting point. That is geography, not gerrymandering, and a map that registers a small UCP-favourable efficiency gap is doing its job, not failing it. Second, *not every gerrymander shows up in the partisan-fairness numbers*. The structural lane — community splits, off-reference borders, anchoring departures, chair-flagged shapes — can move outcomes substantially without producing a noticeable efficiency-gap fingerprint, which is why the audit measures both lanes separately. Whether any specific drafting process is using the structural lane deliberately or is producing those patterns by other causes is a question of intent, which the audit does not adjudicate.

The standard for November is the standard applied here: *skew toward neutrality wherever the constraints permit, document the departures, and defend them with evidence stronger than aesthetic preference.* When the Lunty committee publishes its map in November, this audit will measure it the same way, with the same code, against the same thresholds. The results will be public the day the map is.

---

## What the audit does and does not claim

This article makes an inferential case. It is worth being precise about what that case is — and what it isn't.

**What the article does claim.** The minority map's structural choices are measurable, directionally consistent, and converge on the places where the governing party is weakest. Five of the six contested redraws fail their own published rationales under independent check. Five of five pre-registered structural-irregularity tests fire. None of this is consistent with random drafting noise; the cumulative pattern is what redistricting researchers flag for further inquiry. The article puts this pattern in front of the reader and asks them to judge it.

**What the article does not claim.** It does not claim the minority commissioners drew their map *intending* to help the UCP win seats — that is a question about state of mind, and state of mind cannot be read off a map. The article distinguishes measurable effect (which it documents) from proven intent (which it does not). A reader can read the cumulative pattern as engineering, as systematic unlucky drafting, or as something in between. The article is built to make the engineering reading available without forcing it.

**What the article rules out.** "Geography did this" is ruled out — the 2019 enacted map and the 2026 majority map operate under the same Alberta geography and the same statutory constraints, and neither produces the minority's structural pattern. "Random drafting noise" is ruled out at the level of cumulative directional consistency — five-of-five tests firing in the same direction is statistically distinguishable from chance. "The minority commissioners broke the law" is ruled out — both maps satisfy the *Electoral Boundaries Commission Act*.

**What's outside the audit's scope.** The audit does not reach a constitutional conclusion. The standard a court would apply is the *Reference re Saskatchewan* [1991] effective-representation framework, reaffirmed and arguably strengthened by the Supreme Court of Canada's April 22, 2026 ruling on Quebec's electoral map (a 7–2 decision from the bench upholding the Quebec Court of Appeal's finding that legislative interference with independent commission redistricting violates Charter section 3). Whether the evidence in this audit supports a Charter challenge to either the minority commission map or the April 16 Alberta motion is for counsel and the courts to assess. The audit also does not project specific 2027 election outcomes — the partisan-fairness numbers are scored against 2023 votes (the most recent result) and the full monograph also reports the 2019-vote and current-polling readings; all of them are inputs to a verdict, not predictions.

---

## A note on difficulty

Redistricting is one of the hardest problems in democratic design. It is *legal* (constitutional rights, statutory rules, judicial precedent), *sociological* (what makes a community a community, and whose definition counts), *geographic* (rural-urban gradients, transportation networks, language and Indigenous boundaries, the way Calgary's NW quadrant grew and where Cochrane commuters actually go), and *statistical* (hundreds of fairness metrics, none uniquely correct, most under active academic dispute). Getting close to fair takes smart people years of work. The tools to draw and audit these maps are young — a generation behind the tools we have for, say, financial auditing or epidemiology. Reasonable commissioners disagree in good faith about boundary choices that look like errors from outside.

None of this lets the minority map's pattern off the hook. The structural-irregularity signals are real, the rationale-failure pattern is real, and a Lane 1 lean shows up under 2023 actuals, 2019 actuals, and current 338 polling alike. But if a reader started this article thinking redistricting *should* be simple — as the author did when he opened the project, expecting a short weekend's work — that prior is the first thing to reconsider. The work of drawing a fair Alberta map is not easy even when nobody is trying to cheat. The honest version of "this map fails" requires saying, in the same breath, what the legitimate version would have to look like — and the legitimate version is harder to draw than this article's prose makes it sound.

---

## Behind the audit

This audit was produced by Will Conner, a fourth-year computer information systems student at Mount Royal University in Calgary. It is an independent research project with no funding from any political party or advocacy organization. The author is a UCP-disinclined Alberta voter; that prior is disclosed in the monograph's Author Disclosure block, along with the three findings retained in the paper that ran *against* the prior.

The audit used publicly available data: Elections Alberta's 2023 Statement of Vote (vote totals by voting area), Statistics Canada's 2021 Census (population, small-area census geography, census subdivisions), and the commission's 2026 final report (per-district population tables, published rationales, chair-flag annotations). All code is published in the GitHub repository and can be run independently by any reader. The pre-registered checklist that drove the audit was published on March 14, 2026 — nine days before the commission filed its report — and timestamped via the Open Science Framework with embargoed release scheduled for 2026-11-02 (the day the Lunty committee must report).

The Elections Alberta shapefiles for the 2026 proposed boundaries have not been released. The audit reconstructs them from the commission's high-resolution map images using the best methods and best available data — an eight-stage geometry pipeline that combines image vectorization, sub-metre adjacency snapping, and full coverage of all 89 districts via 2019 inheritance for any district whose 2026 boundaries the commission's published images did not let the audit reconstruct directly. The full monograph documents every step. A sunset clause binds the audit to recompute all geometry-dependent findings within two weeks of any official shapefile release. (The original commitment was 48 hours; relaxed to two weeks to leave room for the kinds of delays that affect any solo researcher. Building a daily-monitor automation pipeline that ingests new shapefiles and re-runs the tests as soon as they're released is on the roadmap; the two-week window covers both the automated and the manual case honestly.)

**Honest gaps in the audit, listed.** Two open exposures are worth naming explicitly. First, **external replication.** The audit is reproducible by design — open code, open data, deterministic seeds, pinned dependencies — but at time of writing has not been independently re-run by anyone outside the project. A step-by-step plan for cross-validating the headline finding using the R `redist` package (a different language, different research group, different codebase from the audit's Python pipeline) is at `analysis/methodology/v0_1_external_tool_validation_plan.md`. Until that R cross-validation has been completed, all quantitative claims should be read as "the audit's Python pipeline produces these values; reproduction in a second language is the next defensibility step." Second, **code-bug risk.** The pipeline is roughly 50 Python scripts written by a single author. There is now an automated test suite (`tests/test_scoring.py`, 9 tests passing as of this writing — including a forensic spot-check that confirms the verification subset's saved metrics match what you get when you reload the saved per-step partition assignments and recompute from scratch) that catches the most damaging classes of regressions. But standard scientific-software bugs (off-by-one errors, coordinate-system mismatches, floating-point edge cases) almost certainly exist somewhere at low magnitude and would not be caught by re-running the same Python pipeline. Independent reproduction in R is the high-value mitigation; spot-checking by another developer is the supplementary one.

*AI assistance disclosed: Claude (Anthropic) helped draft and check the text. All factual claims were verified by the author against primary sources.*

---

## What you can do

1. **Read the full findings.** The [full monograph](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/report_academic.md) contains every number, every source, and every caveat. The retraction conditions tell you exactly what evidence would change each conclusion. The [methodology folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology) holds the per-claim evidence trail.

2. **Ask your MLA three questions about the committee.**
   - Will it publish the criteria it's using *before* it draws a single line?
   - Will it release the other maps it considered, not just the one it picked?
   - Will it disclose any AI tools it used and the prompts given to them?

3. **Request the official shapefiles.** Elections Alberta has not published the 2026 electoral division map files. Without these, some of this audit's calculations cannot be fully verified or corrected. A Freedom of Information request would require their release.

The full technical monograph, with all methods, caveats, and source citations, is at [github.com/Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit). All code is open source under [the audit's GitHub repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) and reproducible end-to-end.
