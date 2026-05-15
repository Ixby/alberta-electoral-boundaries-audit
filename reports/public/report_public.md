# Two Maps, Then None: Inside Alberta's 2026 Boundary Audit

*A plain-language look at the 2025–26 Electoral Boundary Commission, the math behind the minority map, and what comes next.*

## Part I: How the Commission Broke

Alberta's Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Both are legal under the *Electoral Boundaries Commission Act*. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). This audit measured both maps using the same methods, applied identically. Three findings stand out.

1. **The two maps differ on six things you can measure without looking at any election results:** how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's own chair flagged as anomalous. The minority map differs from the majority on every one of them.

2. **The direction runs against the places where the governing party is weakest.** Calgary's northwest quadrant, the City of Airdrie, urban areas with established municipal boundaries — the communities most affected by the minority map's structural differences are the same ones where the governing party's opponents are strongest. The audit cannot determine intent. It can measure effect.

3. **The process now promoting the minority map has no precedent in Canada.** No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP).

**The process is its own finding, separate from the maps.**

---

## The Map on the Cover

The cover map is the best single image in this audit. Here is how to read it.

Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.

This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.

The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.

For me personally, this was the image that made the stakes clear. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once you can see the population underneath the boundary choices, those choices stop looking random.

---

---

## Part II: The 1,000,000-Map Litmus Test {.new-page}

![How skewed each map looks on the partisan-fairness number. The majority sits at +0.1% — inside the normal range. The minority sits at +4.0%, just below the Alberta line at ~4.1%. The further right the dot, the more the map favours the UCP relative to its provincial vote share.](data/maps/article/lane1_dotplot.svg)



The table compares the two maps. The first five rows use no election results — they're properties of the lines themselves. The last two depend on how votes were attributed to each district.

| What was measured | Majority map | Minority map | Direction / Beneficiary |
|---|---|---|---|
| Population spread across districts (tighter is better) | 3,180 | **4,707 — 48% wider** | Structural (Reduces vote equality) |
| NW Calgary population excess above average | 2.8% | **11.5%** | **UCP** (Packs urban NDP votes) |
| Airdrie split | 2 divisions | **4 divisions** | **UCP** (Cracks urban/suburban power) |
| Borders that follow existing municipal lines | 80% — within norm | 72% — within norm | N/A — both within Canadian norm (70–85%) |
| Boundaries flagged by the commission chair | 0 | **3** | N/A |
| Seats at 50/50 votes (percentile in 1M simulation) | 46.1% — p83 (normal range) | **51.7% — p99.99 (fewer than 100 of 1,000,000 reach this)** | **UCP** |
| Compactness-Weighted Efficiency Gap | +1.5% | **-2.4%** | **UCP** (via irregular shapes) |
| Packing-cracking neighbourhood pattern | 6 coupled chain signals | **2 (pre-registered PASS)** | Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5) |

> **VOCABULARY**
>
> **Efficiency gap.** A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour conservatives; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — roughly the level only 5% of computer-simulated Alberta maps cross.
>
> **Anchoring.** The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.

The bottom rows depend on election results. The *seats@50/50* test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats — Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 83rd percentile of the 1,000,000-map simulation (normal range). The minority map at 51.7% is at the 99.99th percentile — fewer than 100 of 1,000,000 neutral draws reach that value. The *efficiency gap* number measures how lopsidedly each party's votes get translated into seats; on the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, placing it at the 94th percentile — just below the audit's 95th-percentile outlier line. The verdict section unpacks the consequences.

The last row is where the minority map has fewer coupled chain signals than the majority on the neighbour-drain test: 2 against the majority's 6 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS — the minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why: the minority achieves its partisan effect through hybridization (city-splitting that internalises packing and cracking within individual EDs), which is invisible to an adjacency-chain test that only measures how packed districts cluster next to cracked ones.

---

---

## Part III: Cracking, Packing, and Draining

![The division of Airdrie into four separate districts, diluting its urban voting power.](data/maps/article/figure_airdrie_v3.svg)



The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,140 public submissions, and the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts diverge, they diverge on choices someone in the room had to make. Three of those choices are worth seeing as choices, not numbers.

**It splits the City of Airdrie into four pieces.** The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Calgary-Nolan Hill-Cochrane, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. The minor-hockey association, the food bank, the Chamber of Commerce — every organization that operates citywide now operates across four provincial ridings.

> **WHY AIRDRIE MATTERS**
>
> Airdrie is the largest Alberta city without its own MLA. At 85,805 people (2024 municipal census) it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.
>
> Splitting it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, and Airdrie East — each primarily identified with a different surrounding jurisdiction, removes Airdrie from the political map at the level of government that draws it. The city has 85,805 residents and zero seats in the legislature where a majority of voters call the place home.
>
> A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?

> Both maps are legal. The four-way split is a choice.

**Where it departs from municipal lines, it departs at strategically important places.** When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates: the majority at 80%, the minority at 72%, both within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). *(The audit's initial provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.)* The striking observation is not the overall rate but where the minority's departures are concentrated: the three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park's extension into uninhabited national-park land, the Nolan Hill–Cochrane lasso corridor, and the Olds–North Airdrie reach — are each departures from pre-existing civic geography in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.

**One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.** In Calgary's northwest quadrant, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This is *packing*: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and *cracking* (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.

The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair. (The chair's published criticism covers seven boundary configurations in total — four geometric flags in the main report and three in Appendix C. This audit independently confirmed anomalous geometry for three of the four geometric flags; the fourth, Calgary-Foothills-Airdrie West, did not meet the audit's confirmation threshold.)

---

---

## Part IV: The Impact on the Ground {.new-page}

Lane 1 depends on which election results you score the maps against. Lane 2 does not. The structural evidence is in the maps themselves — drawn lines, split cities, where the boundaries do and don't follow administrative lines that exist for other reasons. On these tests, the two maps are not close.

![The five structural-fairness tests, side by side. Purple bars are the majority map, green bars are the minority map. The dashed red line in each row marks the failing point. The green bars cross every line by a wide margin. The purple bars sit flat at zero or stay well inside the safe range.](data/maps/article/lane2_bars.svg)

The same five tests in tabular form, with each test's threshold stated alongside the result. The bottom row is the audit's *summary* — the count of tests each map fails out of the five.

| Test | Majority map | Minority map | Direction / Beneficiary |
|---|---|---|---|
| Border follows existing municipal lines (70–85% Canadian norm) | 80% — within norm | 72% — within norm | N/A — both within Canadian norm |
| Population spread (tighter is better) | 3,180 | **4,707 — 48% wider** | Structural (Reduces vote equality) |
| NW Calgary population excess above average | 2.8% | **11.5%** | **UCP** (Packs urban NDP votes) |
| Boundaries flagged by the commission's own chair | 0 | **3** | N/A |
| Airdrie split (constraint minimum: 2) | 2 pieces | **4 pieces** | **UCP** (Cracks urban/suburban power) |
| **Pre-registered summary** (≥ 4 of 5 = outlier) | **0 of 5 fired** | **4 of 5 fired** (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire) | **UCP** |

A separate finding — applied only to the minority because the minority is the map whose contested redraws are public[^asym] — is that **five of six of the minority commissioners' published rationales fail under independent check**. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.)

The audit also tested the chair's separate, blanket assertion in Appendix C that the minority's seven contested hybrid configurations had **no public support** in the 1,140+ public submissions. A keyword search across the full submission archive (94% machine-parsed, 6% image-only and excluded; methodology and per-configuration evidence at [`findings/submission_search_findings.md`](findings/submission_search_findings.md)) returned a more nuanced picture than either the chair's blanket claim or its blanket dismissal: the chair was right on three of seven (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane hybrid, and the St. Albert minority alternative each lack any documented support), wrong on three of seven (Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission plus several aligned ones; Olds–Three-Hills–Didsbury was supported by Beiseker residents in writing; Chestermere drew multiple submissions opposing a Calgary merger that materially align with the minority's intent), and partially wrong on one (Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, with directional but not configuration-exact alignment). The chair's Appendix C "no public support" sweep is therefore demonstrably overbroad — three of seven are demonstrably false — but it is not invented out of whole cloth, since three of seven do hold up. **This finding cuts against the chair, not against the minority.**

[^asym]: The majority did not publish a contested-redraw rationale list. The seven-rationale audit cannot be applied symmetrically; it is reported as a single flag, not as additional rows in the structural-irregularity count.

**On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.**

---

## Part V: How "Clean Gerrymanders" Work {.new-page}

The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.

To answer this, the audit generated 1,000,000 computer-simulated, mathematically neutral Alberta maps (4 independent chains × 252,500 steps, base seed from Cloudflare drand beacon, pre-registered at OSF before execution) using the official Elections Alberta shapefiles, holding to the exact same statutory rules and geographic boundaries the commission used. We then placed the commission's two 2026 maps into that distribution to see how normal they are.

In Alberta, the neutral answer is not 50/50. *Across 1,000,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes* — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.

The full distribution from the canonical 1,000,000-map simulation:

| Where the map sits | UCP seats at 50/50 votes |
|---|---|
| Median Alberta map | 44.8% — NDP slight seat majority |
| 95th-percentile map | 47.1% |
| 99th-percentile map | 48.4% |
| **Maximum across 1,000,000 maps** | **below 51.7% (fewer than 100 plans reach this value)** |

A note on seat counts. The 2026 commission maps each have **89** districts; the audit's computer simulation runs on the **87**-district 2019 map (its starting substrate); the November Lunty committee will produce **91**. All percentages are seat *shares*, comparable across these denominators.

The results — placing the three real maps in this distribution — point to a specific, surgical pattern of boundary drawing.

### All four statistical measures fire simultaneously

When the official Elections Alberta shapefiles are used, the minority map is a statistical outlier on every partisan-fairness metric — not just the tipping-point one.

| Map | Efficiency gap | Mean-median | Declination | Seats at 50/50 |
|---|---|---|---|---|
| Majority 2026 | +0.1% (p15) | −3.6% (p2) | +0.027 (p81) | 46.1% (p83) |
| Minority 2026 | **+4.0% (p94)** | **+1.0% (p99.98)** | **−0.077 (p1.2)** | **51.7% (p99.99)** |

The majority map sits comfortably inside the normal range on three of four metrics. Its mean-median sits at p2 in the NDP-favourable direction — an unusual result but pointing the wrong way to help the UCP. The minority map is in the tail on all four, each pointing in the same partisan direction.

### The 50/50 tipping point: fewer than 100 of 1,000,000 neutral maps reach it

The tipping-point metric is the most intuitive: if the province split exactly 50/50 between the two parties, how many seats does each map give the UCP?

| Map | UCP seats at 50/50 votes | Where it sits |
|---|---|---|
| 2019 enacted | 46.0% | 83rd percentile — inside the normal range |
| **Majority 2026** | **46.1%** | **83rd percentile — well within bounds** |
| **Minority 2026** | **51.7% (46 seats)** | **99.99th percentile — fewer than 100 of 1,000,000 neutral draws reach this** |

Fewer than 100 of 1,000,000 computer-simulated neutral Alberta maps produced a `seats@50/50` value as high as the minority map's. Based on actual recent voting patterns, it awards the UCP 60 seats (compared to 55 in the majority map). The majority map is the kind of map a neutral procedure routinely generates. The minority map is the kind of map you have to specifically aim to draw.

### What this means in plain language

The official shapefiles reveal a map that is statistically extreme in the same partisan direction on all four measures at once. The joint probability of a neutral drawing process producing a map this extreme across all four measures simultaneously is roughly one in 15 million (p = 6.87×10⁻⁸, pre-registered Fisher combined test). That is not a rounding error or a measurement artefact — it is the same answer from four independent statistical instruments read in the same room.

**Two questions, one answer.** The 1,000,000-map simulation asks: *is this map extreme compared to neutral maps drawn on the same Alberta geography?* A second, separate test — called the Swing-Zone Allocation Test — asks a different question: *are the specific lines on the map partisan-neutral?* It works by looking only at the Voting Areas where the minority drew differently from the majority and asking whether those particular choices, taken together, shifted vote efficiency in one party's direction. Because it compares only the places where the two maps differ, it automatically controls for everything they share — the same provincial geography, the same population targets, the same statutory rules. Both questions return the same answer. That is why the one-in-15-million figure is a combined result rather than a single test: it is two independent lines of evidence converging.

This explains why the minority map had to be such an extreme statistical outlier (p99.99) against 1,000,000 neutral simulations. In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. You do not hit the 60-seat supermajority threshold by drawing natural, community-respecting boundaries; you have to surgically force the map to get there.

> **WHY A SUPERMAJORITY MATTERS**
> 
> Under Canada's Westminster parliamentary system, a simple majority (45 seats) is enough to pass routine laws and budgets. But securing a two-thirds supermajority (60 seats) grants a government near-absolute control. It allows the ruling party to effortlessly invoke "closure" to shut down debate, rewrite the rules of the legislature without opposition consent, and completely dominate all legislative committees. More importantly, it makes a Premier mathematically bulletproof to internal revolts—even if half a dozen backbenchers cross the floor, the government retains absolute control. A simple majority lets you drive the car; a 60-seat supermajority lets you rewrite the traffic laws.

By strategically diluting urban voters into surrounding rural-edge districts (the "urban hybridization" pattern identified in Lane 2), the minority map engineers the exact structural firewall needed to secure those 60 seats. The Lane 2 structural finding and the Lane 1 statistical finding converge on the same map, the same direction, and the same communities.

### Confirmation from the targeted-procedure test

To be sure this isn't a quirk of the neutral simulation's known compactness preference, the audit ran a targeted hill-climbing procedure (Cannon et al. 2022 — the standard tool in the redistricting-statistics literature for exploring biased-but-legal maps) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.

| Procedure | Most-extreme value reached | What it tells us |
|---|---|---|
| Neutral MCMC, max produced | below 51.7% UCP seats @ 50/50 | The natural ceiling under neutral drawing |
| Neutral MCMC, min produced | ~39% UCP seats @ 50/50 | The natural floor under neutral drawing |
| Targeted hill-climb, UCP-maximizing | **52.9%** | What a procedure deliberately aiming for UCP advantage can reach |
| Targeted hill-climb, NDP-maximizing | **37.9%** | What a procedure deliberately aiming for NDP advantage can reach (below the neutral floor) |

The minority map's 51.7% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. Both the 2019 enacted map and the 2026 majority fall comfortably within what neutral procedure routinely produces — different vote shares, same zone of unremarkable outcomes. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (80.0% vs 2019's 75.2%). Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.

*That* is the shape of the finding, and it is also the framing a court would actually apply.

### Ruling Out Alternative Explanations

When presented with a statistical outlier of this magnitude, a rigorous audit must rule out innocent explanations before concluding intentional gerrymandering. The structural data (Lane 2) systematically dismantles the standard alternative defenses:

1. **The "Natural Political Geography" Defense:** *("Urban voters are naturally packed; the map just reflects Alberta's geography.")* The 1,000,000 simulations already account for Alberta's natural geography. The simulation proves that while geography gives the UCP a baseline efficiency advantage, it naturally caps around the 83rd to 90th percentile. The minority map sits at the 99.99th percentile — an extreme outlier *even when compared to Alberta's naturally skewed baseline*.
2. **The "Communities of Interest" Defense:** *("The odd shapes were drawn to keep specific communities together.")* If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices that cannot be explained by community-of-interest logic.
3. **The "Population Equality" Defense:** *("They had to draw weird boundaries to make sure every district had the exact same population.")* The minority map is actually much *worse* at population equality. Its Population Mean Absolute Deviation (MAD) was 3938, placing it in the 98.7th percentile of badness for population parity. It sacrificed population equality to achieve its shape.
4. **The "Incompetence or Bad Luck" Defense:** *("They just drew a sloppy map and got unlucky with the numbers.")* Hitting exactly 60 seats for a supermajority while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission's own chair flagged as anomalous requires surgical precision. The joint probability of accidentally drawing a map that hits the extreme statistical tail across four independent partisan metrics simultaneously is roughly **1 in 15 million** ($p = 6.87 \times 10^{-8}$). You cannot blunder your way into the 99.99th percentile.

Because the data proves the drafters actively worsened cities and population parity, the only remaining mathematical interpretation is that the partisan skew *was* the primary optimization goal.

### A note on the R cross-validation

An earlier version of this audit (using approximated rather than official shapefiles) cross-validated the Python ReCom ensemble against the R `redist` package's Sequential Monte Carlo sampler. That cross-check produced unstable results: across three runs with the same nominal seed, the fraction of plans reaching the old minority value (48.3% on the approximated geometry) was 5.6%, then 28%, then 58% — a sampler-convergence failure, not a discovery. The full write-up is at [`findings/redist_python_comparison.md`](findings/redist_python_comparison.md).

With official Elections Alberta shapefiles, the minority map's `seats@50/50` rises to 51.7% — a value fewer than 100 of 1,000,000 neutral plans reach. The R cross-validation question becomes moot: zero plans from either sampler reach the canonical value at comparable sample sizes.

**The asymmetry around 50/50 is more telling than the inversion itself.** A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about **49.7%**. That is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What *is* dramatic is the contrast: on the **majority** map, the UCP would need to *win* the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.

This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.

**One caveat the audit takes seriously.** A real electorate is not a uniform 50/50. Voters can swamp any map's structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates *the map's contribution to the outcome*, not the outcome itself. What it shows is what the map does when the electorate doesn't decide for it.

---

## Part VI: What Happens in November

The audit's central finding is geometric. **Lane 2 — the structural-irregularity scorecard — is the foundation; Lane 1 is the proof that the geometry is doing partisan work.**

The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the map fails, out of five, where higher means more structural problems). The bottom-left corner is "clean on both lanes." The top-right corner is "out of bounds on both lanes."

![The two ways of measuring the maps, plotted together. Left-to-right: how skewed the map looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the map fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 map (purple) stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 map (green) is a structural outlier on all five tests; its efficiency gap (+4.0%) sits just below the Alberta threshold line.](data/maps/article/verdict_quadrant.svg){: .verdict-hero }

The same verdict in plain summary form, leading with the structural finding because that is what the cross-validated evidence supports most strongly:

| | Lane 2: Structure (geometry-only, no votes) | Lane 1: Numbers (vote-dependent) |
|---|:--|:--|
| **Majority 2026** | clean — crosses *no* structural threshold | inside the normal range on every metric (`seats@50/50` 46.1% — p83; efficiency gap +0.1%) |
| **Minority 2026** | **crosses 4 of 5 structural thresholds** by a wide margin (anchoring neutral — both maps within Canadian norm) | statistical outlier on all four partisan-fairness measures simultaneously — `seats@50/50` 51.7% (p99.99, fewer than 100 of 1,000,000 reach it); efficiency gap +4.0% (p94); all four pre-registered; Fisher combined p = 6.87×10⁻⁸ |

**Why Lane 2 carries the case.** The audit pre-registered five structural-irregularity tests on April 24, 2026 before the final simulation results were compiled. The minority crosses every one; the majority crosses none. Those measurements are geometric — they don't depend on any statistical sampler or any vote attribution. Lane 1 (the partisan-fairness numbers) corroborates Lane 2 strongly under canonical official shapefiles: the minority is a statistical outlier on all four pre-registered metrics simultaneously, with a joint neutral-null probability of p = 6.87×10⁻⁸ (pre-registered Fisher combined test, OSF [6pt83](https://osf.io/6pt83/)). The question of whether Lane 2's unusual geometry is the specific *mechanism* behind the Lane 1 numbers was tested and the answer is no — see [`findings/redist_python_comparison.md`](findings/redist_python_comparison.md). Lane 2 is the central finding. Lane 1 corroborates without carrying.

> **THE PLAIN READING.** Two electoral maps were drawn in the same room, by five commissioners working from the same rules and the same data. The majority map is the kind of map a neutral procedure routinely produces: clean on every one of the audit's pre-registered structural tests, comfortably inside the simulated partisan-fairness distribution. The minority map is something else. It crosses four of five structural-irregularity tests — chair-flagged lasso corridors (3 confirmed of 7 configurations criticized), the four-way Airdrie split, the national-park extension, and the 48%-wider population spread — and on 1,000,000 computer-simulated neutral maps drawn from the official Elections Alberta shapefiles, its `seats@50/50` value is reached by fewer than 100 neutral maps. *(Municipal anchoring is the fifth pre-registered test; it is retracted — both maps fall within the 70–85% Canadian norm on official shapefiles. See the correction note below.)* All four partisan-fairness measures simultaneously place it in the statistical tail; the joint probability of that combination under a neutral drawing process is roughly one in 15 million. The audit tested whether the unusual geometry is the specific mechanism that produces the seat advantage; that claim did not survive the falsification. What does survive: same room, same rules, same data, two very different maps, and only one of them has the structural pattern that researchers flag for further inquiry. Whether the cause was deliberate engineering, unlucky drafting, or both is a judgement call the audit puts in the reader's hands.
>
> We measured the effects. We can't read minds.

> **RETRACTION CONDITIONS**
>
> *The audit's findings are pre-committed to falsifiability. Retractions apply per-finding. If any condition below materialises, the specific finding it relates to is retracted publicly within 30 days. The overall verdict (directional consistency across multiple independent tests) is retracted only if at least three of the tests fail.*
>
> 1. **A counter-map exists.** Someone produces a legal Alberta map satisfying the minority's own community-of-interest reasons (Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park) *and* anchoring on municipal boundaries at majority-comparable rates. Open challenge — [Issue #14](https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14) on the audit's GitHub repository.
> 2. **The Neighbour-Drain Pass fails the label-shuffling null.** If the v2 continuous drain score (Phase B of `drain_v2_plan.md`) falls in the extreme upper tail (p < 0.05) of random permutations across the fixed contiguity graph, the "pre-registered pass" is retracted and reclassified as a detected spatial signature.
> 3. **A pre-2026 internal commission document surfaces.** Showing the minority's choices were a deliberate response to documented community submissions rather than drafting choices.
> 4. **The 2027 election result, fought on either of these maps, contradicts the percentile readings.** If the partisan-fairness direction the audit projects from 2023 votes turns out to be wrong on actual votes, the Lane 1 finding gets revisited.
> 5. **The Quebec 2026 Supreme Court ruling is materially distinguished by an Alberta court.** If a court reviewing the April 16 Alberta motion finds the Alberta situation is constitutionally distinct from Quebec's — for example, because the Lunty committee is structured differently from a legislative-freeze law, or because Alberta's effective-representation analysis differs from Quebec's — the audit's procedural critique of the motion weakens.

> **DOCUMENTED CORRECTIONS (canonical recomputation, 2026-05-11)**
>
> The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.
>
> **Municipal anchoring (retracted).** Early analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9× below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring *divergence* between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction.

---

## The Invisible Part

This audit ran into two data problems that have nothing to do with the commission and everything to do with how Alberta's electoral system is designed. Both are fixable.

**Elections Alberta already has the data to tell us where advance voters live — it just doesn't publish it.** About half of all Alberta votes are now cast before election day — advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. That means roughly 395,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted; they just can't be located. This is not a technical problem. Every advance voter is checked against a voters list before receiving their ballot, and that list links each voter to their specific Voting Area. The information exists at the moment of voting. Elections Alberta simply does not retain or publish that link in its results. No change to the voting process is required — only a change to what EA reports from data it already holds.

This affects the commissioners too, not just outside analysts. When a commission decides whether to keep Airdrie whole or split it, whether a corridor between two communities makes sense, whether a proposed boundary divides a natural constituency — those are judgments that depend on knowing where voters live. Commissioners work from the same published dataset as everyone else. Half the geographic signal about the communities they are drawing boundaries around is missing for them as well.

There is at least one community in northern Alberta where this gap is total. In the northern part of the Lesser Slave Lake division, there is a Voting Area covering 4,832 km² — larger than Prince Edward Island — where every single vote in 2023 was cast through Elections Alberta's mobile polling team. Those 844 residents' choices are counted in the divisional total but cannot be pinned to any location on a map. That community is entirely invisible in the published election results.

When the commission initially considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. The commission eventually preserved the division — after 80+ public submissions, many from the Indigenous communities in the northern part of the riding — invoking a provincial law that allows ridings with First Nations and Métis communities to have smaller populations than the provincial average. They got there. But the data they were working with didn't show them who was voting in the communities they were deciding to protect.

Here is the other side of that story: while the Indigenous communities in Lesser Slave Lake were fighting to be counted, the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. The commission's own chair called that "a bad faith effort" to claim the legal protection. That phrase is in the commission's official final report. The protection designed for remote communities with Indigenous populations was used, in the minority's map, to defend a boundary through uninhabited wilderness. The communities it was designed to help had to fight for it through public submissions.

**Alberta should wait for the 2026 census before drawing the next map.** Canada counts its population every ten years. The 2026 census enumeration happens in spring 2026; Statistics Canada releases usable sub-provincial data roughly two years later, in 2027 or 2028. The commission that drew the maps assessed in this audit had to use the 2021 census — already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the *Electoral Boundaries Commission Act* could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live, not where they lived a decade ago.

Neither of these is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be. They are offered here as practical suggestions, not conclusions.

---

## References & Methodology

While this report summarizes the audit for a general audience, the underlying methodology relies on established political science and legal literature on electoral boundary design. Key references include:

* **Chen, Jowei, and Jonathan Rodden. 2013.** "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269. (Establishes the framework for evaluating how "natural packing" of urban voters interacts with neutrally drawn boundaries).
* **Courtney, John C. 2001.** *Commissioned Ridings: Designing Canada's Electoral Districts*. Montreal and Kingston: McGill-Queen's University Press. (The foundational text on the history and structural norms of independent Canadian boundary commissions).