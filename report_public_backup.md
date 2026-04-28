# Two Maps, Then None: Inside Alberta's 2026 Boundary Audit

*A plain-language summary of the 2025–26 Electoral Boundary Commission forensic audit, and what the audit will measure next.*
*v0.24 — April 26, 2026 — [Full monograph](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/report_academic.md)*

---

## How this audit got to its answer

One number signalled that the 2026 minority commission map was impossibly gerrymandered. Another said it was perfectly legal. A third said the bias didn't have to be that extreme. A fourth said the map had elements of fairness. When the numbers don't agree, you keep asking. So this audit's author ran the standard 250,000-map computer simulation; identified a bug in the sampler; hardened the geographic substrate to 100% precision; and ran a legally-defensible 250,000-map standard. The apparent extremity grew more mathematically unassailable rather than reverting to the mean. Improbability that doesn't resolve under more data is a signal that the question is being asked wrong.

So the next move was to audit the methodology and the code itself. An external adversarial reviewer (Google Gemini 3.1 Pro, in five independent passes) found nine fixable bugs in the audit's pipeline — three of them statistically load-bearing. The most damaging two: an MCMC chain that was silently restarting from the 2019 baseline every 20,000 steps (so the "2M-step deep chain" was structurally a stack of 100 short bursts), and a polygon-reconstruction artefact that was leaving 6 of the minority's 89 districts effectively unscored. With some reverse-engineering of the input pipeline — mathematically dissolving the 2023 voting-area substrate using the conservation-exact Phase 4C assignments to produce a topologically-perfect 89/89-district map (the v0_9 substrate, an AI-authored topological map awaiting independent human GIS verification) — the input quality came up to where the answers could be trusted.

Re-run on the corrected pipeline, with all nine bugs fixed and the v0_9 substrate in place, the picture you are about to read is what emerged. *That* is how science is supposed to work: don't fall in love with the first number; chase the contradictions until either the numbers reconcile or the methodology fails honestly. Keeping good notes through that process is itself the discipline — the audit's bug-finding paths, the input-quality work, and the corrected outputs are all in version control under `analysis/methodology/external_code_audit_findings_gemini_2026-04-26.md` and `analysis/reports/post_audit_recompute_deltas.md`.

**The hypotheses, and what killed each.** Three working ideas ran through the audit. Two died on contact with data; the third is the one that survived.

1. **"The 2-million-map ensemble shows the minority map is impossibly extreme."**
*Killed by:* the external code audit. The chunked MCMC orchestration was silently restarting from the 2019 baseline every 20,000 steps. The "2-million-step deep continuous chain" was structurally a stack of 100 short bursts. Bug fixed; the corrected ensemble revised the minority's percentile from "p100, off the chart" down to "p98.6, top 1.5%."

2. **"The minority's seats@50/50 of 52.8% is the singular outlier."**
*Killed by:* a polygon-reconstruction artefact left 6 of the minority's 89 districts effectively unscored. The topologically-perfect v0_9 substrate (mathematically dissolving the 2023 voting-area grid using the conservation-exact Phase 4C assignments) recovered full 89-of-89 coverage. The corrected number is **48.3%**, not 52.8%.

3. **"The non-compact geometry the chair flagged is the load-bearing mechanism through which the minority commissioners reached their UCP advantage."**
*Killed twice — once by a pre-registered falsification test, then again by direct measurement on the v0_9 substrate.* R-SMC plans that reach the corrected 0.4831 value have mean Polsby-Popper compactness of 0.2391 — *more* compact than the 0.2339 of plans that don't reach it (p = 7.7 × 10⁻²³⁴). Independently, on the v0_9 topological substrate, the chair's named lassos themselves score *moderately compact*: Calgary-Nolan Hill-Cochrane PP = 0.40, Rocky Mountain House-Banff Park PP = 0.41 (PP < 0.25 is the conventional flag threshold; PP > 0.40 is the "high compactness" band). The mechanism isn't non-compactness — the minority drew the corridors thick enough that the Area/Perimeter ratio is innocent. The mechanism is *what the corridors connect*: city blocks extracted across municipal limits into suburban districts. That moves the load-bearing mechanism off geometry-shape and onto **municipal anchoring** (minority anchors 14.5% of perimeter on municipal lines, majority 71%) and **urban hybridization** (minority 25 hybrid EDs, majority 9, 12 of the minority's hybrids are *new*). Both are substrate-stable measurements that don't depend on any sampler. (A second unrelated SMC issue — the sampler's tail probabilities swung from 5% to 58% across runs that differed only in PRNG-state consumption — separately disqualifies SMC as a co-equal source of truth here. ReCom converges to publication-grade Gelman-Rubin R̂ < 1.05; SMC, on this geometry, did not.)

What survives all three deaths: the **Lane 2 structural-irregularity scorecard** (5 of 5 pre-registered tests fired against the minority, 0 of 5 against the majority — measured directly off the map geometry, no sampler, no vote attribution), and the **Lane 1 ReCom percentile of 98.6** (top 1.5%, on the corrected 250,000-map baseline ensemble). The audit's central claim now rests on Lane 2; the corrected Lane 1 corroborates it without carrying it.

That is what the article describes from here.

---

An Airdrie resident pulls up the new electoral map on her phone. Her street goes to one riding. Two blocks over goes to another. The kids on her cul-de-sac all attend the same elementary school, but their families now write to four different MLAs about school funding. The Genesis Place rec centre, the Co-op grocery, the Iron Horse Park BMX track — every shared neighbourhood institution sits on the boundary between two divisions, sometimes three. Under one of the two competing proposals from Alberta's 2026 boundary commission — the one signed by the two dissenting commissioners — her city of 84,000 is cut into four pieces — the south to Calgary-Airdrie, the west to Calgary-Foothills-Airdrie West, the north to Calgary-Nolan Hill-Cochrane, and the east to Airdrie East. Nothing about Airdrie changed. Only the map did.

This audit is about that map, the alternative proposal three other commissioners signed, and a third map a legislative committee in Edmonton is drawing right now. It uses two kinds of evidence — *partisan-fairness numbers* (whether the math comes out lopsided) and *structural patterns* (whether the lines themselves are drawn in unusual ways) — kept separate so each can be judged on its own.

A *gerrymander*, in this article, means a boundary choice that gives one political side an advantage beyond what the rules require. Intent cannot be read off a map. What can be measured are effects.

A note before reading: on April 16, the government set both commission maps aside and assigned the redrawing to a legislative committee. Neither map this article analyzes is a candidate to become law. The article is about what those maps reveal about the process that produced them, and about the standard the November committee map will be measured against.

---

## The short version

Alberta's Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Both are legal under the *Electoral Boundaries Commission Act*. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). This audit measured both maps using the same methods, applied identically. Three findings stand out.

1. **The two maps differ on six things you can measure without looking at any election results:** how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's own chair flagged as anomalous. The minority map differs from the majority on every one of them.

2. **The direction runs against the places where the governing party is weakest.** Calgary's northwest quadrant, the City of Airdrie, urban areas with established municipal boundaries — the communities most affected by the minority map's structural differences are the same ones where the governing party's opponents are strongest. The audit cannot determine intent. It can measure effect.

3. **The process now promoting the minority map has no precedent in Canada.** No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP).

**The process is its own finding, separate from the maps.**

---

## The April 16 decision {.new-page}

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

## How the audit measures gerrymandering {.new-page}

A gerrymander is a deliberate boundary choice that advantages one political interest over others, beyond what the statutory constraints require. Two methodological problems make this hard to measure honestly.

The first is that there is no single correct Alberta map. The number of legal Alberta maps — those satisfying the *Electoral Boundaries Commission Act*'s rules on population deviation within ±25%, contiguity, compactness, community-of-interest preservation, Indigenous effective representation, and public-hearing input — runs into the astronomical billions. There is no way to test them all. Fairness in this domain is not a discovery; it is a choice among many legitimate alternatives.

The second is that intent cannot be observed from a map. A commissioner could draw a partisan-skewed map either deliberately or by unlucky chance among the legal alternatives. The audit cannot read minds. What it can do is measure *effects* — how the map a commission produced compares to the family of maps a non-partisan procedure would have drawn.

The audit handles both problems with three layered tools.

**A 250,000-map computer simulation.** The audit generates 250,000 different legal Alberta maps using a published redistricting algorithm (called ReCom) under the same statutory constraints the commission worked under. 250,000 is the audit's pre-registered baseline; an earlier exploratory enlargement to 2,000,000 maps was rolled back when convergence diagnostics confirmed gold-standard chain mixing at 250k. The corrected ensemble is run as four parallel chains of 62,500 maps each (Gelman-Rubin R̂ between 1.007 and 1.017 across all four partisan-fairness metrics, comfortably below the publication-standard 1.05 threshold). Each simulated map is scored on the four standard partisan-bias measures. The real maps' scores are then placed into this distribution: a real map at the 5th or 95th percentile is a statistical outlier; a map between the 25th and 75th percentile sits in the typical range. On the four standard partisan-fairness scores, the 2019 enacted map and the 2026 majority map both sit comfortably inside the bulk of the distribution — telling the audit what is geography (Alberta's persistent rural-conservative tilt shows up under any map) versus what is drawing (the minority map's structural irregularities, which the majority and 2019 do not share).

**Two reference lines for the efficiency-gap test.** The audit uses two: the famous **7% line** from US case law (Whitford v. Gill, calibrated to US Congressional delegation sizes), and the audit's **~4% Alberta-calibrated line** derived from its own computer simulation. The ~4% line is rounded from the empirical 3.90% — the 95th percentile of the simulation's efficiency-gap distribution. The exact percentile is in the monograph; the magazine uses ~4% because the threshold is partly a subjective choice (the decision to call p95 "outlier") and the rounded number is honest about that. The Alberta-calibrated ~4% line is the more demanding test, since both lines are above zero and ~4% is closer to neutral. On the corrected v0_9 substrate, neither 2026 map exceeds ~4% (majority +1.4%, minority +1.8%); both sit comfortably inside the bulk of the simulated distribution on this metric. The Lane 1 finding the audit ends up resting on is *not* efficiency gap — it is `seats@50/50`, where the minority sits at p98.6 while the majority sits at p77 (see "The 50/50 test: surgical fortification vs. blunt force" below).

**A pre-registered structural-irregularity scorecard.** Five tests, formally committed to in writing on April 24, 2026 — prior to the execution of the final 250,000-map ensemble and establishing a cryptographic baseline for the upcoming November committee map: how far the map departs from Canadian comparator norms on municipal-boundary anchoring, how much wider the population spread is, the gap between geographic zones (such as Calgary's NW quadrant), how many boundaries the commission's own chair flagged as anomalous, and how many of the minority's published rationales fail when checked under the same audit method. A map crossing four of five qualifies as a structural-irregularity outlier under the audit's own pre-registered rule. The minority crosses five of five. The majority crosses zero of five.

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
| Seats at 50/50 votes (percentile in 250k simulation) | 46.1% — p77 (normal range) | **48.3% — p98.6 (top 1.5%)** |
| Efficiency gap (a partisan-fairness measure) | +1.4% | +1.8% |
| Packing-cracking neighbourhood pattern | 3 (same as 2019) | **0 — *pre-registered pass*** |

> **VOCABULARY**
>
> **Efficiency gap.** A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour conservatives; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — roughly the level only 5% of computer-simulated Alberta maps cross.
>
> **Anchoring.** The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.

The bottom rows depend on election results. The *seats@50/50* test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats — Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 77th percentile of the 250,000-map simulation (normal range). The minority map at 48.3% sits at the 98.5th percentile (top 1.5%). The *efficiency gap* number measures how lopsidedly each party's votes get translated into seats; on the corrected v0_9 substrate both maps' efficiency gaps are inside the simulation's bulk (+1.4% and +1.8%) and so do not separate the two maps the way `seats@50/50` does. The verdict section unpacks the consequences.

The last row is where the minority map looks *better* than the majority on a partisan-fairness measure: zero packed-cracked adjacency pairs, against three on the majority and three on the current 2019 map. The audit pre-registered this test before measuring, and the minority's tighter packing-cracking number is a real point in its favour. It is the single test where the minority outperforms the majority.

---

## Three things the minority map does differently {: .new-page }

The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,140 public submissions, and the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts diverge, they diverge on choices someone in the room had to make. Three of those choices are worth seeing as choices, not numbers.

**It splits the City of Airdrie into four pieces.** The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Calgary-Nolan Hill-Cochrane, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. The minor-hockey association, the food bank, the Chamber of Commerce — every organization that operates citywide now operates across four provincial ridings.

> **WHY AIRDRIE MATTERS**
>
> Airdrie is the largest Alberta city without its own MLA. At 84,000 people it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.
>
> Splitting it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, and Airdrie East — each primarily identified with a different surrounding jurisdiction, removes Airdrie from the political map at the level of government that draws it. The city has 84,000 residents and zero seats in the legislature where a majority of voters call the place home.
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
> Letter-to-point conversion uses Mount Royal University's full undergraduate +/- grading scale (A+ 95–100, A 90–94, A- 85–89, B+ 80–84, B 75–79, B- 70–74, C+ 65–69, C 60–64, C- 55–59, D+ 52–54, D 50–51, F 0–49). Each grade converts to its range midpoint (A+ = 97, A = 92, A- = 87, B+ = 82, B = 77, B- = 72, C+ = 67, C = 62, C- = 57, D+ = 53, D = 50, F = 25). The audit author is an MRU undergraduate; using the institution's published grading scale is the most defensible single conversion choice. The overall is each grade × its weight, summed.
>
> | Category | Weight | Majority grade | Majority points | Minority grade | Minority points |
> |---|---:|:---:|---:|:---:|---:|
> | Voter equality | 25% | B | 19.25 | D | 12.50 |
> | Community recognition | 35% | B | 26.95 | F | 8.75 |
> | Map coherence | 25% | A | 23.00 | D | 12.50 |
> | Partisan fairness | 15% | B | 11.55 | C+ | 10.05 |
> | **OVERALL** | — | **B+ (81/100)** | | **F (44/100)** | |

**Why these weights.** Community recognition carries the most (35%) because *Reference re Saskatchewan* — the Supreme Court decision defining what redistricting is for — holds that effective representation requires districts that communities can identify as their own. The Act's ±25% population band grounds voter equality at 25%. Map coherence (25%) reflects the commission's own standard: the chair flagged specific boundaries as anomalous, and those flags matter. Partisan fairness is weighted lowest (15%) because the global partisan-fairness numbers (efficiency gap, mean-median, declination) sit inside the bulk of the simulated distribution for both maps; the lane's distinguishing finding lives in the narrow tipping-point metric `seats@50/50` (where the minority sits at the 98th percentile). The partisan-fairness lane is real but the surgical-fortification pattern in `seats@50/50` is what distinguishes the two maps.

**What produces the minority's F.** On community recognition (8.75 of 35 under these weights — the lowest single-category score in the table), 15% municipal anchoring means 85 out of every 100 kilometres of the minority map's border cuts through territory voters do not recognize from any other civic map — not their school division boundary, not their property-tax bill, not their local election ward. The majority's equivalent is 71%. The Airdrie four-way split compounds the effect — residents must navigate four legislative offices, each primarily identified with somewhere else. Three chair-flagged anomalies — a corridor extracting NW-Calgary across the city limit into a Cochrane-anchored suburban riding (Calgary-Nolan Hill-Cochrane), a boundary extension through uninhabited national park land (Rocky Mountain House-Banff Park), and a rural district named for communities together smaller than the suburban community it actually captures (Olds-Three Hills-Didsbury reaching into north Airdrie) — pull the map-coherence score down further. None of the three breaches conventional Polsby-Popper compactness under the v0_9 substrate; the chair's flags are qualitative shape-and-content anomalies, and what makes them count for the audit is the municipal-boundary breach in each one.

**Where the maps differ less sharply.** Under the lowest-weighted category — partisan fairness — the global metrics (efficiency gap, mean-median, declination) sit inside the simulation's bulk for both maps, so neither map crosses the Alberta-calibrated ~4% efficiency-gap line under the corrected v0_9 substrate. The lane's distinguishing finding is in the narrow tipping-point metric `seats@50/50`: the majority sits at p77 (normal range) and the minority sits at p98.6 (top 1.5%). The +/- distinction the MRU scale supports captures this asymmetry: the majority earns a B (clean Lane 1 globally; modest tipping-point lean), the minority a C+ (clean Lane 1 globally; near-top-percentile tipping-point fortification on the one metric where surgical engineering shows). Both grades are above passing; the minority's grade is closer to the cut-off.

---

## Was either map a gerrymander?

The honest answer needs two lanes.

### Lane 1 — the partisan-fairness numbers

The number Lane 1 produces is called the *efficiency gap*. In plain terms: it measures how lopsidedly each party's votes get translated into seats. Zero is perfectly neutral. A positive efficiency gap of, say, +5% means the UCP wins roughly five percentage points more of the seats than a perfectly fair vote-to-seat translation would give them; a negative number means the same thing in the NDP's direction. A bigger number means a bigger seat-share advantage for one side that the votes alone don't justify.

The audit places two reference lines on the efficiency gap. The **~4% Alberta line** is the audit's own, the 95th percentile of the efficiency gap across the 250,000 legal Alberta maps the corrected computer simulation generated (empirical p95 = 3.90%, rounded up to ~4% to acknowledge sampling-tolerance). A real map above this line sits in the outermost 5% of what Alberta's redistricting rules can produce. The **7% US line** is the academic-literature reference (*Whitford v. Gill*, calibrated to US Congressional delegation sizes); it has no Alberta-specific authority but is widely cited. Both are *reference lines*, not legal cut-offs — crossing them doesn't make a map illegal, but it does mean the map is statistically unusual relative to what a non-partisan procedure under the same rules would produce.

Where the two 2026 maps land:

![How skewed each map looks on the partisan-fairness number. Both 2026 maps sit beyond the Alberta line at ~5%; only the minority also crosses the US line at 7%. The further right the dot, the more the map favours the UCP relative to its provincial vote share.](data/maps/article/lane1_dotplot.png)

The same picture in numbers — each map's efficiency gap, scored on the topologically-perfect v0_9 substrate and placed in the audit's corrected 250,000-map simulation:

| Map | Efficiency gap (v0_9) | Above Alberta line (~4%)? | Above US line (7%)? | Percentile in the 250k simulation |
|---|---|---|---|---|
| Majority 2026 | +1.4% | **No** — 2.6 below | **No** — 5.6 below | 49.8 (median-like) |
| Minority 2026 | +1.8% | **No** — 2.2 below | **No** — 5.2 below | 57.5 (slightly UCP-tilted, within bulk) |

Under the corrected v0_9 substrate, neither map is an efficiency-gap outlier on its own — both sit inside the bulk of the simulated distribution. The Lane 1 weight in the scorecard reflects this: the partisan-fairness lane gives essentially the same answer for both maps on the global metrics. The minority-vs-majority distinction on Lane 1 lives almost entirely in the `seats@50/50` test (covered in the next section), where the surgical-fortification pattern shows up. The article's overall finding rests primarily on Lane 2 (structural irregularity), which is unaffected by vote-distribution measurement choices.

**The seats@50/50 metric tells a different and more interesting story** — see ["The rural-representation question"](#the-rural-representation-question) below.

**The percentile readings are point estimates, not bounds.** The simulation runs as four parallel chains of 62,500 maps each (250,000 total), giving the percentile placements roughly ±1 percentile-point precision in the right tail.

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

A separate finding — applied only to the minority because the minority is the map whose contested redraws are public[^asym] — is that **five of six of the minority commissioners' published rationales fail under independent check**. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.)

The audit also tested the chair's separate, blanket assertion in Appendix C that the minority's seven contested hybrid configurations had **no public support** in the 1,140+ public submissions. A keyword search across the full submission archive (94% machine-parsed, 6% image-only and excluded; methodology and per-configuration evidence at [`analysis/reports/submission_search_findings.md`](analysis/reports/submission_search_findings.md)) returned a more nuanced picture than either the chair's blanket claim or its blanket dismissal: the chair was right on three of seven (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane hybrid, and the St. Albert minority alternative each lack any documented support), wrong on three of seven (Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission plus several aligned ones; Olds–Three-Hills–Didsbury was supported by Beiseker residents in writing; Chestermere drew multiple submissions opposing a Calgary merger that materially align with the minority's intent), and partially wrong on one (Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, with directional but not configuration-exact alignment). The chair's Appendix C "no public support" sweep is therefore demonstrably overbroad — three of seven are demonstrably false — but it is not invented out of whole cloth, since three of seven do hold up. **This finding cuts against the chair, not against the minority.**

[^asym]: The majority did not publish a contested-redraw rationale list. The seven-rationale audit cannot be applied symmetrically; it is reported as a single flag, not as additional rows in the structural-irregularity count.

**On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.**

### The rural-representation question

Before going further, the audit owes a direct answer to the strongest defence of the minority map's hybrid urban–rural districts. The minority commissioners themselves state it cleanly in their Appendix E to the commission's final report (pp. 302–303):

> *"Hybrid constituencies are not only a good reflection of Alberta, but also the best available instrument for preserving rural and suburban representation in the face of sustained urban growth. They avoid the false choice between (a) underrepresenting Calgary and Edmonton, and (b) creating ever-larger purely rural districts that become geographically unmanageable."*
>
> — Minority commissioners, *Final Report* Appendix E (pp. 302–303)

That argument deserves a fair test against the data — and it has now also been adjudicated. The Supreme Court of Canada, on April 22, 2026, dismissed Quebec's appeal of a Quebec Court of Appeal ruling that struck down Quebec's 2024 attempt to freeze its electoral map on similar regional-representation grounds. The 7–2 ruling, delivered from the bench, held that legislative interference with independent commission redistricting work — even when justified on regional-protection grounds — violates Charter section 3 by allowing significant disparities in voter weight to persist. The minority commissioners' rural-protection argument is now operating against Canadian constitutional doctrine that has, in the most recent SCC ruling on the question, gone the other way.

There are two ways a map can protect rural representation. The first is the way the *Electoral Boundaries Commission Act* itself provides for: section 15(2) lets up to four electoral divisions be drawn with population *up to 50% below* the provincial average — a deliberate over-representation tool, baked into the statute, specifically to keep small rural communities from being arithmetically swamped. The second is by under-populating rural districts in general (without invoking 15(2)), giving rural voters more weight per ballot. Both mechanisms are visible in the population data the commission published.

How each map handles rural representation:

| Map | s.15(2) special-rural EDs declared | Rural ED average population | Rural-voter weight vs urban (1.0 = equal) |
|---|---|---|---|
| 2019 enacted | (commission didn't tag) | 45,370 (-3.1% below ideal) | **1.044×** — rural voters carry 4.4% more weight |
| 2026 majority | **3** (Canmore-Banff, Central Peace-Notley, Lesser Slave Lake) | 51,057 (-7.1% below ideal) | **1.119×** — rural voters carry 11.9% more weight |
| 2026 minority | **0** (the audit found no s.15(2) declaration in the minority report) | 47,945 (-12.7% below ideal) | **1.229×** — rural voters carry 22.9% more weight |

On the *headline* number — rural-vs-urban representation weight — the minority map looks like the most rural-protective of the three. But the *mechanism* is different from what the Act envisions. The minority's number doesn't come from declaring s.15(2) special-rural districts (it declares none). And it doesn't come mainly from making pure-rural districts smaller (the majority does that more conservatively). It comes from a third lever: **converting urban districts into urban–rural hybrids by attaching pieces of cities to surrounding rural-edge territory.**

The hybrid-district counts make this concrete — under a programmatic definition (an electoral division whose territory contains at least 5% of its area inside a Census Sub-Division for a city *and* at least 5% outside), the 2019 enacted map has 8 hybrid EDs, the 2026 majority has 14, and the 2026 minority has 17. Both 2026 maps expand on 2019; the minority expands further. The headline isn't the gross count, though — it's *what kind of hybrid each map draws*. The minority's hybrids systematically violate municipal anchoring at the rate above (14.5% vs 71%); the majority's hybrids do not. The minority's converted ridings — described below — are ones the majority drew as pure-Calgary, pure-Edmonton, pure-Lethbridge, or pure-Red Deer city seats, but that the minority converted into hybrids by stapling them to suburban or rural-edge territory.

The minority's hybrid expansion is province-wide, not Calgary-only:

- **Calgary (7 new hybrids):** Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, Calgary-North West-Bearspaw, Calgary-Bow-Springbank, Calgary-West-Tsuut'ina, Calgary-Peigan-Chestermere.
- **Lethbridge (4 new hybrids):** Lethbridge-Taber-Warner, Lethbridge-Little Bow, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Cardston. The City of Lethbridge — population 100,000 — has zero pure-Lethbridge ridings on the minority map. Every Lethbridge voter shares an MLA with an out-of-city community. The University of Lethbridge, Lethbridge Polytechnic, the regional hospital, the city's downtown business association — all of them lobby a province whose every Lethbridge MLA has constituents in Cardston, Taber, or the Crowsnest Pass who don't share their priorities.
- **Red Deer (4 new hybrids):** Red Deer-Lacombe, Red Deer-Innisfail, Red Deer-Sylvan Lake, Red Deer-Blackfalds. Same structural pattern: the City of Red Deer — 100,000 people, the third-largest city in Alberta — is dispersed across four ridings whose names lead with surrounding towns. The Red Deer Catholic Regional Schools division ends at the city limits; it sees its catchment now spread across four MLAs each accountable to a different rural service centre.
- **Edmonton (3 new hybrids):** Edmonton-Spruce Grove, Edmonton-Beaumont, Edmonton-Enoch-Devon. Each one bonds a slice of west, south, or southwest Edmonton to a separate satellite municipality whose city council and provincial MLA primary residency lie outside the Edmonton city boundary.

Whether this third lever counts as "rural protection" depends on what the reader thinks rural protection should do. The Act's lever (s.15(2), -50% deviation) gives existing rural communities more legislative weight without disturbing how cities elect MLAs. The minority's lever does something different: it dilutes urban political identity (the City of Lethbridge has no MLA primarily named for it; the City of Red Deer has no MLA primarily named for it) by spreading city voters across districts whose other members are rural-edge or suburban. The two mechanisms produce different first-order effects: the Act's lever strengthens rural representation; the minority's lever weakens urban representation. They are not equivalent, and the audit's data lets the reader judge which one each map is actually doing.

A second observation worth making honestly: the suburban-edge communities the minority's hybrids attach to (Airdrie, Cochrane, Spruce Grove, Beaumont, Sylvan Lake, Bearspaw, Chestermere) tend to be *more conservative-leaning than the cities they're attached to and less conservative-leaning than the deeper rural areas beyond them*. Adding suburban-conservative voters to urban-edge ridings shifts those ridings' partisan-fairness numbers in the UCP-favourable direction without invoking either the s.15(2) rural-protection lever or the actual rural population that the rural-protection argument is meant to defend. That is the structural mechanism the audit calls *the drain pattern*: urban votes drained into hybrids that shore up suburban-conservative seats, producing what looks (in the rural-vs-urban-weight table above) like rural over-representation but is actually urban dilution.

The audit's reading: **the majority map protects rural representation in the way the Act intends — by under-populating actual rural districts and using the s.15(2) special-rural provision. The minority map's apparent rural-protection number is mostly produced by a different mechanism — urban hybridization — that has the side effect of also improving UCP-leaning seat math without using the statutory rural-protection lever at all.** Either reading is available to the reader; the data is what the data is.

### Five of six of the minority's published reasons fail under check

The minority commissioners did the audit a favour. Their published report singles out the boundary choices they expected to be questioned and offers a one-paragraph rationale for each. That made the audit's job small and concrete: take each rationale at face value, find the public dataset the rationale invokes, see if the data says what the rationale says it says. A weekend's worth of journey-to-work table lookups, school-division boundary cross-references, and Census-of-Agriculture polygon clips. Five out of six, the data says no — sometimes by a small margin, sometimes by a large one. Each check is documented in the [audit's evidence trail](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology).

- **Airdrie split four ways.** *Minority commissioners said:* a four-way split was needed to balance population. *The spatial evidence says:* The lines don't follow natural constraints; they are drawn across the residential mass. Of the four minority EDs that draw Airdrie residents into themselves, **Calgary-Airdrie's perimeter is 70.9% on neither the city limit nor any major highway** — the highest free-perimeter share of any electoral division touching the city, in either map. The minority's lines enter Airdrie's residential mass via Highway 2 and Highway 567 but exit via free-drawn diagonals that cut through populated neighbourhoods to reach distant rural service centres. The Act permits anchoring on roads; it does not permit using a road as the entry corridor and then carving free-handed across the city behind it. The four-way split is an intentional structural choice, not an arithmetic or geometric necessity. The data trail and a side-by-side visual are at `data/maps/airdrie_4way_teardown.png`. **Fail.**
- **Cochrane attached to Calgary-Foothills via the Nolan Hill lasso.** *Minority commissioners said:* commuter community of interest. *Statistics Canada Table 98-10-0459 (2021 Census journey-to-work) says:* of 8,550 Cochrane workers, 4,205 of them never leave Cochrane to work — they walk to the local Sobeys, drive across town to one of the industrial parks, or commute within the same town's commercial corridor. Of the rest, 35.8% commute to Calgary somewhere; the data cannot single out Nolan Hill as the destination. The Cochrane–Nolan Hill pairing is not supported. **Fail.**
- **Rocky Mountain House extended into Banff National Park.** *Minority commissioners said:* ranching community of interest. The polygon the minority drew reaches into glaciers, alpine meadows, and the Columbia Icefield. *The Canada National Parks Act* prohibits agricultural tenure on park land, and a polygon-clipped 2021-Census-DA pull on the Banff extension finds no documented year-round-resident population in the strict park-land slice. The "ranching community of interest" rationale has no agricultural land base it can refer to. **Fail.**
- **Olds-Three Hills-Didsbury reaching into North Airdrie.** *Minority commissioners said:* linked agricultural service centres. *The land-use record says:* North Airdrie is suburban residential; Olds and Didsbury are rural service centres. The connection is geographic adjacency, not common interest. **Fail.**
- **Red Deer attached to Sylvan Lake.** *Minority commissioners said:* shared school division. *Alberta Education's published school-division boundaries say:* Sylvan Lake is in Chinook's Edge School Division No. 73; the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools. They are different divisions. The "shared school division" rationale is factually incorrect. **Fail.**
- **St. Albert-Sturgeon.** *Minority commissioners said:* population balancing on Edmonton-corridor constraints. *The convergence test says:* the majority map and the minority map independently arrive at the same St. Albert-Sturgeon two-district structure under the Act's constraints. When two independent drafting teams converge, the configuration is constraint-forced rather than engineered. **Stands.**

The five-failure / one-stand pattern matters. A symmetric audit finding 0 of 6 or 6 of 6 would suggest either no rationale problem or a methodology bias. The asymmetry — five fail, one stands, and the one that stands is the one both maps independently produce — is what distinguishes a real finding from a noise pattern. Each fail is documented with primary-source citations in [the methodology folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology) so a hostile reviewer can check the work.

### The 50/50 test: surgical fortification vs. blunt force

The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.

To answer this, the audit generated 250,000 computer-simulated, mathematically neutral Alberta maps, holding to the exact same statutory rules and geographic boundaries the commission used. We then placed the commission's two 2026 maps into that distribution to see how normal they are.

In Alberta, the neutral answer is not 50/50. *Across 250,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes* — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.

The full distribution from the corrected 250,000-map simulation:

| Where the map sits | UCP seats at 50/50 votes |
|---|---|
| Median Alberta map | 44.8% — NDP slight seat majority |
| 95th-percentile map | 48.31% (43 seats) — the floor of the outlier tier |
| 99th-percentile map | 49.4% — just shy of half |
| **Maximum across 250,000 maps** | **50.6%** |

A note on seat counts. The 2026 commission maps each have **89** districts; the audit's computer simulation runs on the **87**-district 2019 map (its starting substrate); the November Lunty committee will produce **91**. All percentages are seat *shares*, comparable across these denominators.

The results — placing the three real maps in this distribution — point to a specific, surgical pattern of boundary drawing.

#### 1. The global metrics are normal (the disguise)

A classic blunt-force gerrymander packs and cracks voters everywhere, creating a map with an extreme efficiency gap that stands out like a sore thumb. Neither 2026 map does this. When measured on global fairness metrics — efficiency gap, mean-median, and declination — *both* the majority and the minority maps sit comfortably in the middle of the simulated distribution (between the 50th and 58th percentiles). On the surface, the minority map looks entirely mathematically innocent.

| Map | Efficiency gap | Mean-median | Declination |
|---|---|---|---|
| Majority 2026 | +1.4% (p50) | -0.8% (p90) | -0.028 (p18) |
| Minority 2026 | +1.8% (p58) | -1.8% (p51) | +0.011 (p58) |

Three of four Lane 1 metrics for the minority sit within ten percentile points of the median. If you stopped here, you would conclude the minority map is mathematically unremarkable.

#### 2. The 50/50 tipping point is an extreme outlier (the strike)

But when you look specifically at the tipping-point metric — `seats@50/50` — the minority map suddenly rockets out of the median and into the extreme right tail.

| Map | UCP seats at 50/50 votes | Where it sits |
|---|---|---|
| 2019 enacted | 46.0% | 77th percentile — inside the normal range |
| **Majority 2026** | **46.1%** | **77th percentile — respects Alberta's rural-conservative geography, but well within bounds** |
| **Minority 2026** | **48.31% (43 seats)** | **98.57th percentile — top 1.5% (sharing this floor with every map down to the 95th percentile)** |

*Out of 250,000 neutral maps, only 3,750 — exactly 1.5% — pushed the tipping-point advantage this far.* (Note on statistical precision: the 250,000 maps are drawn from a Markov chain with an effective sample size [ESS] of roughly 375 independent draws. At an ESS of 375, the true percentile placement carries an uncertainty of about ±2 points, placing the map securely between the 96th and 99th percentiles.) The majority map is the kind of map a neutral procedure routinely generates. The minority map is the kind of map you have to specifically aim to draw.

#### What this means in plain language

The minority commission map is not a sloppy, widespread gerrymander. We interpret this as a *surgical fortification of the tipping point*. The mapmakers didn't waste time manipulating safe rural seats or deep-urban strongholds — which is why the global efficiency gap looks normal. Instead, they executed a targeted strike exactly where it matters: the marginal, 50/50 hybrid districts.

By strategically diluting urban voters into surrounding rural-edge districts (the "urban hybridization" pattern identified in Lane 2), the minority map engineers a structural firewall that maximises UCP seat retention in a tied election — pushing the map into the extreme top 1.5% of mathematical possibility — while keeping the overall provincial metrics looking completely innocent.

The corrected 250k v0_9 ensemble bears this out empirically. Of the four standard partisan-fairness metrics, the minority sits near the median on three: efficiency gap (p56), mean-median (p53), declination (p62) — exactly where a "normal" Alberta map sits. Only the tipping-point metric `seats@50/50` registers the fortification, at p98.5 (top 1.5%). Three doors look untouched; one door is wedged shut. That asymmetry is the surgical-fortification fingerprint, and it is exactly the pattern the audit's methodological-defenses appendix predicts a hostile reviewer would otherwise miss: in a polarised two-party system with rigid geographic packing, the global metrics are mathematically numb to surgical micro-targeting.

#### Confirmation from the targeted-procedure test

To be sure this isn't a quirk of the neutral simulation's known compactness preference, the audit ran a targeted hill-climbing procedure (Cannon et al. 2022 — the standard tool in the redistricting-statistics literature for exploring biased-but-legal maps) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.

| Procedure | Most-extreme value reached | What it tells us |
|---|---|---|
| Neutral v0_9 MCMC, max produced | 50.6% UCP seats @ 50/50 | The natural ceiling under neutral drawing |
| Neutral v0_9 MCMC, min produced | 39.1% UCP seats @ 50/50 | The natural floor under neutral drawing |
| Targeted hill-climb, UCP-maximizing | **52.9%** | What a procedure deliberately aiming for UCP advantage can reach |
| Targeted hill-climb, NDP-maximizing | **37.9%** | What a procedure deliberately aiming for NDP advantage can reach (below the neutral floor) |

The minority map's 48.3% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. The 2019 enacted map and the 2026 majority sit at *identical* percentile on `seats@50/50` (both p78.6 against the v0_9 250k ensemble) — not because they record the same vote share, but because both fall well within what neutral procedure routinely produces. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (71.0% vs 2019's 75.2%). Two doors closed in the same way; the minority is the one wedged shut. Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.

*That* is the shape of the finding, and it is also the framing a court would actually apply.

#### A note on the R cross-validation

Gemini's design review (the same external reviewer that found the nine bugs) insisted on cross-validating the Python ReCom ensemble against the R `redist` package's Sequential Monte Carlo sampler — a fundamentally different statistical approach. The audit did the cross-check. The result was unhelpful in a particular way: across three runs of the R-SMC sampler with the same nominal random seed and the same parameters, the fraction of plans reaching the minority's 48.3% value was 5.6%, then 28%, then 58%. That kind of run-to-run instability isn't a discovery; it's a sampler-convergence failure. (For comparison, the Python ReCom ensemble passed the gold-standard Gelman-Rubin convergence diagnostic at R̂ < 1.05 across all four metrics — meaning the four parallel chains have lost memory of their starting point and are sampling from the same underlying distribution.)

The audit therefore treats the Python ReCom ensemble as the authoritative baseline for the percentile placement (the 98.5th-percentile figure cited above), and the R-SMC cross-validation as an unsuccessful convergence check rather than a co-equal source of truth. The full diagnostic write-up is at [`analysis/reports/redist_python_comparison.md`](analysis/reports/redist_python_comparison.md), including the falsification test that killed the working hypothesis described in this article's opening section ("non-compact geometry is the load-bearing mechanism") — that's the third of the three hypotheses the data killed.

**The asymmetry around 50/50 is more telling than the inversion itself.** A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about **49.7%**. That is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What *is* dramatic is the contrast: on the **majority** map, the UCP would need to *win* the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.

This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.

**One caveat the audit takes seriously.** A real electorate is not a uniform 50/50. Voters can swamp any map's structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates *the map's contribution to the outcome*, not the outcome itself. What it shows is what the map does when the electorate doesn't decide for it.

### Scoring against current polling

The 338Canada projection on April 12, 2026 (UCP 52.5% / NDP 37.6%) gives the question one more data point. Re-scoring both maps against current polling instead of 2023 actual votes:

| Map | Efficiency gap (2023 actuals, v0_9 substrate) | Efficiency gap (338, April 2026) — v0_8 substrate, not yet re-scored on v0_9 |
|---|---|---|
| Majority 2026 | +1.4% | **+8.7%** (was on v0_8) |
| Minority 2026 | +1.8% | **+7.0%** (was on v0_8) |

The 338-projection numbers in the right-hand column were computed against the v0_8 substrate and have not yet been re-scored on the corrected v0_9 substrate; the audit treats them as draft until that re-score lands. The left-hand column (2023 actuals on v0_9) is what the corrected pipeline produces. Even with the right column held in place pending re-score, the conclusion is consistent: under any single electorate, Lane 1 efficiency gap flickers a few percentage points either way; *the 50/50 test above doesn't flicker, the structural-fairness pattern in Lane 2 doesn't flicker, and the 250,000 corrected simulated maps under the same Alberta rules don't move when the polls do.* Those are the pieces of the verdict the audit will defend in any year.

### Verdict {.new-page}

The audit's central finding is geometric. **Lane 2 — the structural-irregularity scorecard — is the foundation; Lane 1 is the proof that the geometry is doing partisan work.**

The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the map fails, out of five, where higher means more structural problems). The bottom-left corner is "clean on both lanes." The top-right corner is "out of bounds on both lanes."

![The two ways of measuring the maps, plotted together. Left-to-right: how skewed the map looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the map fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 map (purple) drifts right (partisan skew) but stays low (no structural problems). The minority 2026 map (green) sits in the worst corner: high on both.](data/maps/article/verdict_quadrant.png){: .verdict-hero }

The same verdict in plain summary form, leading with the structural finding because that is what the cross-validated evidence supports most strongly:

| | Lane 2: Structure (geometry-only, no votes) | Lane 1: Numbers (vote-dependent) |
|---|:--|:--|
| **Majority 2026** | clean — crosses *no* structural threshold | inside the bulk of the simulated distribution on every metric (`seats@50/50` 46.1% — p77; efficiency gap +1.4% — well inside) |
| **Minority 2026** | **crosses every one of five structural thresholds** by a wide margin | mathematically innocent on the global metrics; **surgical fortification on the `seats@50/50` tipping-point metric** (48.3% — p98.6 under ReCom; near-median under SMC) |

**Why Lane 2 carries the case.** The audit pre-registered five structural-irregularity tests on April 24, 2026, establishing a strict evaluative baseline before the final simulation results were compiled and serving as a formal tripwire for the upcoming November committee map. The minority crosses every one of them; the majority crosses none. Those measurements are geometric — they don't depend on any statistical sampler or any vote attribution. Lane 1 (the partisan-fairness numbers) corroborates Lane 2 under the Python ReCom ensemble (minority `seats@50/50` at the 98.5th percentile, top 1.5%, on the corrected 250,000-map baseline; ReCom passes the gold-standard Gelman-Rubin convergence diagnostic). The natural follow-on question — *can we say Lane 2's unusual non-compact shapes are the specific mechanism that produces Lane 1's seat advantage?* — was tested directly and the answer is no: see the article's opening section "How this audit got to its answer" for the falsification result, and [`analysis/reports/redist_python_comparison.md`](analysis/reports/redist_python_comparison.md) for the full write-up. Lane 1 stops being the central finding the audit defends. *Lane 2 is the central finding.* Lane 1 corroborates without carrying.

> **THE PLAIN READING.** Two electoral maps were drawn in the same room, by five commissioners working from the same rules and the same data. The majority map is the kind of map a neutral procedure routinely produces: clean on every one of the audit's pre-registered structural tests, comfortably inside the simulated partisan-fairness distribution. The minority map is something else. It crosses every one of those structural-irregularity tests by a wide margin — chair-flagged lasso corridors, the four-way Airdrie split, the national-park extension, the urban-rural hybridizations, 15% municipal anchoring against the Canadian norm of 70-85% — and on the corrected 250,000-map computer simulation its `seats@50/50` value sits in the top 1.5% of what the simulation produces. The audit *did* test whether the unusual geometry is the specific mechanism that produces the seat advantage; that more-ambitious claim did not survive the falsification (full record in the article's opening section). What does survive: same room, same rules, same data, two very different maps, and only one of them has the structural pattern that researchers flag for further inquiry. Whether the cause was deliberate engineering, unlucky drafting, or both is a judgement call the audit puts in the reader's hands.
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

The work itself is not moot. The commission audit calibrated Alberta-specific thresholds — structural-irregularity tests, anchoring comparators, the 250,000-map computer ensemble (corrected post-audit; an exploratory 2,000,000-map enlargement was rolled back when convergence diagnostics confirmed gold-standard mixing at much smaller sample sizes) — against three real Alberta maps (the 2019 enacted boundaries plus the two 2026 commission proposals, applied symmetrically). That framework will be re-pointed at the Lunty committee's map the day it is published, reported by the same standard you have just read.

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

## Behind the audit {.new-page}

This audit was produced by Will Conner, a fourth-year computer information systems student at Mount Royal University in Calgary. It is an independent research project with no funding from any political party or advocacy organization. The author is a UCP-disinclined Alberta voter; that prior is disclosed in the monograph's Author Disclosure block, along with the three findings retained in the paper that ran *against* the prior.

The audit used publicly available data: Elections Alberta's 2023 Statement of Vote (vote totals by voting area), Statistics Canada's 2021 Census (population, small-area census geography, census subdivisions), and the commission's 2026 final report (per-district population tables, published rationales, chair-flag annotations). All code is published in the GitHub repository and can be run independently by any reader. The pre-registered checklist that drove the algorithmic audit was timestamped on April 24, 2026 via the Open Science Framework (https://osf.io/2gue9/overview), establishing a rigid "hands-off" criteria baseline prior to the execution of the 250,000-map ensemble. This document also serves as an embargoed, cryptographic pre-commitment for auditing the November 2026 Lunty committee map the day it is released.

The Elections Alberta shapefiles for the 2026 proposed boundaries have not been released. The audit reconstructs them from the commission's high-resolution map images using the best methods and best available data — an eight-stage geometry pipeline that combines image vectorization, sub-metre adjacency snapping, and full coverage of all 89 districts via 2019 inheritance for any district whose 2026 boundaries the commission's published images did not let the audit reconstruct directly. The full monograph documents every step. A sunset clause binds the audit to recompute all geometry-dependent findings within two weeks of any official shapefile release. (The original commitment was 48 hours; relaxed to two weeks to leave room for the kinds of delays that affect any solo researcher. Building a daily-monitor automation pipeline that ingests new shapefiles and re-runs the tests as soon as they're released is on the roadmap; the two-week window covers both the automated and the manual case honestly.)

**Honest gaps in the audit, listed.** Three open exposures are worth naming explicitly. First, **external replication in a second language.** The audit is reproducible by design — open code, open data, deterministic seeds, pinned dependencies, automated pytest CI on every push — and a Sequential-Monte-Carlo cross-validation in R via the Harvard `redist` package was kicked off the same day as the code-audit fixes (script: [`analysis/scripts/redist_crossvalidation.R`](analysis/scripts/redist_crossvalidation.R); plan and run protocol at [`analysis/methodology/external_tool_validation_plan.md`](analysis/methodology/external_tool_validation_plan.md)). The R run uses a fundamentally different sampler (SMC) from the Python pipeline's ReCom Markov chain; if both produce the same percentile placements within ±0.5pp, the audit's headline finding is algorithm-independent and library-independent. Second, **code-bug risk that the test suite caught.** During the drafting phase, an external code audit by Google Gemini 3.1 Pro surfaced nine fixable bugs in the pipeline — three of them statistically load-bearing — and all nine are now fixed in source with three new regression tests (12 of 12 tests passing under GitHub Actions CI on every push). Two findings drove the bulk of the headline numbers in this draft: a chain-state-reset bug in the chunked MCMC orchestration, and an under-coverage in the v0_8 polygon reconstruction that left 6 of 89 minority districts effectively unscored (the latter resolved by a Gemini-authored topological VA-dissolve, the v0_9 substrate). The "How this audit got to its answer" section above tells that story; the full audit memo is at `analysis/methodology/external_code_audit_findings_gemini_2026-04-26.md`; side-by-side before/after number deltas are at `analysis/reports/post_audit_recompute_deltas.md`. Third, **bug-class risk that no test suite catches.** Standard scientific-software bugs (off-by-one errors, coordinate-system mismatches, floating-point edge cases) almost certainly exist somewhere at low magnitude and would not be caught by re-running the same Python pipeline. The April 26 audit is one snapshot of an adversarial review by one external AI reviewer plus a parallel reconnaissance by GitHub Copilot; that snapshot is *not* a guarantee that no other bugs exist. The high-value mitigation is the in-progress R cross-validation (a different language, sampler, and codebase); the supplementary mitigations are continued external code audits and spot-checking by another developer.

*AI assistance disclosed: Claude (Anthropic, Opus 4.7 1M-context) helped draft and check the text and ran the audit's bug-fix and pipeline operations. Gemini (Google, 3.1 Pro High) performed five passes of independent adversarial code audit against the pipeline (nine bug findings, all remediated; full memo at `analysis/methodology/external_code_audit_findings_gemini_2026-04-26.md`) and authored the v0_9 topological VA-dissolve resolver that eliminated the pixel-traced polygon overlaps. GitHub Copilot was also briefly engaged for a parallel reconnaissance pass; its preliminary findings duplicated Gemini's earlier finds and added no new ones. All factual claims were verified by the author against primary sources; all AI-authored or AI-edited code passed the 12-test pytest suite under CI before landing on `master`.*

---

## What you can do

1. **Read the full findings.** The [full monograph](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/report_academic.md) contains every number, every source, and every caveat. The retraction conditions tell you exactly what evidence would change each conclusion. The [methodology folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis/methodology) holds the per-claim evidence trail.

2. **Ask your MLA three questions about the committee.**
   - Will it publish the criteria it's using *before* it draws a single line?
   - Will it release the other maps it considered, not just the one it picked?
   - Will it disclose any AI tools it used and the prompts given to them?

3. **Request the official shapefiles.** Elections Alberta has not published the 2026 electoral division map files. Without these, some of this audit's calculations cannot be fully verified or corrected. A Freedom of Information request would require their release.

The full technical monograph, with all methods, caveats, and source citations, is at [github.com/Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit). All code is open source under [the audit's GitHub repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) and reproducible end-to-end.
