# Two Maps, One Province

*Published April 22, 2026*

By Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

### Disclosure

I am not a neutral observer of Alberta politics. Going into this project, I believed the UCP government's handling of boundary redistribution was worth scrutiny. That belief could have shaped what I looked for. The audit is designed to answer back: every test is applied the same way to both maps; every numeric claim traces to a script and data file anyone can re-run; an independent self-critique sits in the repository and flagged me when my own language overstated a finding. Three specific cases in this document are places where my prior was wrong and the numbers said so — those retractions are here because the methodology surfaced them.

[Full technical report](report_academic.md) · [Visualized version with charts](report.html) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)

---

> **The bottom line, in three sentences.** The minority map tilts UCP by a small, measurable amount. The shift is about 1 to 3 seats in a tied election, well under any published gerrymander cutoff. The bigger story is that the government rejected the commission's work and handed the drafting pencil to a committee of MLAs.

---

On March 23, Alberta's Electoral Boundaries Commission tabled not one map but two. The five commissioners could not agree. Three of them signed a majority report drawing 89 ridings in a shape most of them could defend. The other two signed a dissenting minority report, with different lines in several places. Twenty-four days later, on April 16, the provincial government rejected the majority map outright, passed a motion 44 to 36, and handed the drafting pencil to a committee of MLAs with a UCP majority. The committee is chaired by UCP backbencher Brandon Lunty. It has until November 2 to come back with a 91-seat map instead.

This audit looked at both commission maps using public data, and at the 91-seat plan as far as the public record allows. The headline finding is narrower than some early commentary has suggested. The minority map is measurably, modestly friendlier to the UCP than the majority map on three of four standard tests. It is nowhere near the threshold American courts have used to flag an extreme gerrymander. The government's decision to replace the commission is a bigger story than the map itself.

What follows is a reporter's walk through the numbers, the shapes on the page, and what can and cannot be said about either.

---

## The commission, and the split

**Five commissioners. Two maps. One dissent from the chair.** Here is how the split happened.

Alberta's Electoral Boundaries Commission is a five-member body that redraws the province's 87 ridings roughly every eight years. Two commissioners are appointed on the recommendation of the government, two on the recommendation of the opposition, and one — the chair — is named by the Chief Justice of Alberta. For 2026, that chair was Dallas Miller.

The commission holds hearings, accepts written submissions from the public, and then proposes a map. It is supposed to be arm's length from the legislature. That's the theory. It has worked that way in Alberta for most of the province's history.

This time, the commission split 3-to-2. The three commissioners in the majority — the chair and the two opposition-appointed members — proposed 89 ridings. The two government-appointed commissioners dissented and proposed their own 89-seat configuration. Both maps add two seats to the current 87 to account for twenty percent population growth since 2017. Both agreed on most of the map. They disagreed, visibly, on about a dozen districts.

In his Appendix C, Chair Miller flagged three of the minority's districts by name as what he called engineered — drawn, he wrote, to satisfy a rule rather than to reflect a real community. He also wrote that the minority's configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had **no public support** in the 1,340-plus submissions the commission received.

Both of those claims turn out to hold up in some places and not in others. The audit tested both.

---

## Where the minority map is different

**Most of the province is the same on both maps. The fights are in Calgary and its commuter belt.** The fastest way to see what the maps disagree about is to look at specific districts.

Each of the five disputed districts below is discussed in turn after the table.

| District | Majority map | Minority map |
|---|---|---|
| Rocky Mountain House-Banff Park | Does not exist | Stretches through uninhabited alpine to qualify as "special remote" |
| Olds-Three Hills-Didsbury | Rural anchor kept | Reaches south to capture part of Airdrie |
| Calgary-Nolan Hill-Cochrane | Does not exist | Skips intervening Calgary neighbourhoods |
| Airdrie | Split two ways, city named | Split four ways, city name absent |
| Chestermere | Paired with Strathmore | Split between Calgary and Chestermere-Strathmore |

**Rocky Mountain House-Banff Park.** The minority draws a district that stretches from Rocky Mountain House down through the uninhabited alpine of Banff National Park to the British Columbia border. Without that southern extension through empty park land, the district wouldn't have enough geography to qualify as a "special remote district" under section 15(2) of the Electoral Boundaries Commission Act — the rule that lets very-remote ridings sit more than 25 percent below the provincial population average. Strip out the empty-park extension and the district's population of 38,298 — 30 percent below the provincial average of 54,929 — can't be justified. The shape exists to qualify for the rule.

**Olds-Three Hills-Didsbury.** Named for three small rural towns in central Alberta. The district also reaches south and captures a substantial piece of Airdrie — which has more people than the three named towns combined. That's not how a boundary commission normally names a district.

**Calgary-Nolan Hill-Cochrane.** Reaches from the town of Cochrane across Calgary's northwest corner to the Nolan Hill neighbourhood, skipping intervening Calgary neighbourhoods. Chair Miller singled this one out in his own report.

**Airdrie, four ways.** Airdrie is a city of about 84,000 just north of Calgary. The majority map puts Airdrie into two ridings — Airdrie-East and Airdrie-Cochrane — both of which carry the city's name. The minority splits it four ways, and no resulting district is named Airdrie. An Airdrie voter under the minority map would never see their city on their ballot.

**Chestermere.** A bedroom community of about 25,000 east of Calgary. The majority keeps it with its natural neighbour Strathmore. The minority splits it between Calgary and Chestermere-Strathmore.

On a map, the difference looks small. On a population table, it's also small: the provincial average is 54,929, and individual districts under both maps cluster inside the legal plus-or-minus 25 percent window. But the minority's spread is wider. Under the majority map, the average district is about 3,180 people off the provincial mean. Under the minority, it's 4,707 — almost fifty percent more variation. Fifteen minority districts sit more than ten percent off the mean. Under the majority, only five do.

Inside Calgary the gap sharpens. Calgary has two rough political zones: a north-east-central band that tends to vote NDP, and a south-west band that tends to vote UCP. Under the majority map, the average district size is nearly identical across the two zones. Under the minority, NDP-leaning Calgary districts average 61,225 people; UCP-leaning ones average 54,569. That's a 12.2 percent gap, and it means the same number of NDP votes in Calgary elects fewer MLAs under the minority map. The zone gap doesn't depend on a model or a vote projection — it's straight from the commission's own population tables.

> **What is a gerrymander, in plain terms?** The word covers any map that uses district lines for partisan advantage. The usual techniques are "packing," where you cram an opposing party's voters into a few big districts where they win overwhelmingly and waste the rest of their votes, and "cracking," where you spread an opposing party's voters thinly across districts where they can't win any. The Calgary zone gap above is the signature of packing. The Airdrie four-way split is the signature of cracking.

---

## The chair's "no public support" claim, sorted

**The chair was wrong in three places, right in three, and the record is split on one.** A closer look at the 1,252 machine-readable submissions — 93 percent of the total — shows a tiered picture.

Our audit searched every submission for keywords matching each disputed district, then hand-reviewed the hits. We also added two districts the minority pushed that Appendix C didn't list but that belong in the same tier: Rocky Mountain House-Banff Park and Olds-Three Hills-Didsbury.

The table below groups the seven disputed districts. It is ordered from the strongest public counter-evidence to the weakest.

| Configuration | Public submissions | Verdict on chair |
|---|---|---|
| **Rocky Mountain House-Banff Park** | 5 support (including detailed position paper EBC-2025-2-0619), 1 oppose | Chair materially wrong; minority adopted from public record |
| **Olds-Three Hills-Didsbury rural unit** | 3 support (2 from Beiseker), 1 oppose | Chair materially wrong |
| **Chestermere as its own unit** | 3 support, 1 oppose | Chair materially wrong |
| **Red Deer-area hybrids** | 4 support, 4 oppose, 15 neutral/ambiguous | Technically false, but record evenly divided |
| **Airdrie 4-way split** | 0 submissions propose this specific carve | Chair's characterization holds |
| **Calgary-Nolan Hill-Cochrane** | 0 submissions propose this configuration | Chair's characterization holds |
| **St. Albert-Sturgeon minority alternative** | 2 name "St. Albert-Sturgeon," but they mean the majority version | Chair's characterization holds |

The tiering matters. A flat "the chair lied about public support" is wrong. So is "the chair was right." The precise story is: on three configurations the minority was adopting public proposals, and the chair's Appendix C reversed the record. On one, the record is split. On three, the chair's description of the submissions is defensible.

---

## What the seat numbers actually say

**Three of four fairness tests agree the minority map tilts UCP. The tilt is small. The fourth test disagrees.**

The audit runs three standard measures of partisan fairness — the efficiency gap, the mean-median gap, and a Monte Carlo simulation of seats under past vote patterns — plus a fourth called declination. Against 2023 vote patterns, three of the four measures agree: the minority map is modestly more UCP-favourable than the majority. Declination disagrees. When tests disagree, readers should lower their confidence.

The table below shows each test's value on the current 2019 map and on both 2026 maps. More negative means a larger UCP tilt. Closer to zero is more balanced.

| Test | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | −2.64% | −0.85% | −1.36% |
| Mean-median gap | −2.22 | −0.18 | −0.33 |
| NDP seats in a tied election | 46 | 44 | 42 |
| Declination | −0.034 | −0.021 | −0.015 |

A negative efficiency gap points toward UCP advantage. The minority's −1.36% is about one-fifth the size of the 7% threshold that American courts have used to flag suspect maps. In seats, the Monte Carlo point estimate is two NDP seats lost under the minority in a tied election. The 95 percent confidence interval actually crosses zero — meaning under the full range of modelling assumptions the minority could give the UCP three extra seats, or give the NDP one extra seat. The direction is probably UCP-favourable. The exact size is uncertain.

There is a more uncomfortable wrinkle. Run the same calculation using the 2019 election as the underlying vote pattern instead of 2023, and the advantage reverses — the minority map would help the NDP. When a test's answer depends on which election you feed it, the answer is partly about the voters rather than about the map. That cuts against any confident claim that the minority is a reliable UCP assist in every scenario.

> **What's the efficiency gap?** A measure of how many votes each party "wastes." Votes for a loser are wasted. Votes for a winner above what was needed to win are also wasted. The efficiency gap is the difference between the two parties' wasted-vote rates. Zero means neither party systematically wastes more votes than the other. Negative numbers (in this province's reporting convention) favour the UCP; positive favour the NDP.

### What each contested redraw actually does to the seat count

The 1-to-3 seat range is the net effect of several specific redraws. Breaking it apart helps a reader see where the money actually moves.

| Contested redraw | Mechanism in plain terms | Seat-count effect |
|---|---|---|
| **Rocky Mountain House-Banff Park** (minority s.15(2) invocation) | Minority adds one extra rural riding at 38,298 people — 30 percent below average — by extending the boundary through uninhabited national park land. The majority covers that same territory with a normally-sized rural riding. | One extra rural seat under minority. Since rural Alberta votes ~67 percent UCP, that's the largest single contributor to the minority's UCP tilt. Roughly +0.7 of the 1-to-3 seat gap. |
| **Calgary Zone A-vs-B packing** (minority packs NDP-leaning Calgary 12 percent larger) | Minority's 17 NDP-leaning Calgary districts carry 6,656 more people each on average. That's about 113,000 NDP-leaning voters packed into existing districts rather than getting more districts. | About 1-2 fewer NDP Calgary seats in a tied election. The second-largest single contributor. Under 2023 results it's closer to 1 seat; under 2019 it would have flipped the other way. |
| **Calgary-Nolan Hill-Cochrane** (minority hybrid) | Merges a Calgary NDP-leaning neighbourhood with the town of Cochrane via a narrow corridor. Creates one district where Nolan Hill voters (NDP-competitive) are diluted by Cochrane voters (strongly UCP). | One Calgary-flagged seat shifts from NDP-competitive to safe UCP. No direct seat count change; the partisan flavour of the seat shifts ~10 points UCP-ward. |
| **Airdrie split four ways** (minority) | Airdrie's 84,000 residents are divided across four districts, none named Airdrie. Majority splits Airdrie across two Airdrie-named districts. | Zero seats flip. Airdrie voters lose primary representation; partisan math roughly neutral because Airdrie leans UCP in every configuration. |
| **Olds-Three Hills-Didsbury with Airdrie addition** (minority rural unit keeps Airdrie chunk) | A rural district named for three small towns adds a slice of Airdrie. Rural voters outnumber the Airdrie slice ~3 to 1. | Zero seats flip. Airdrie voters inside this district are a permanent minority; the district's rural-UCP lean holds. |
| **Chestermere split** (minority partial split vs majority intact) | Some Chestermere voters go to Calgary-Peigan-Chestermere, others to Chestermere-Strathmore. Majority keeps Chestermere whole inside Chestermere-Strathmore. | Zero seats flip. Chestermere voice diluted across two districts; partisan math unchanged. |
| **Red Deer hybrids** (minority 4 peri-Red-Deer hybrids vs majority 3) | Minority adds one more Red Deer-adjacent hybrid district than majority. Both maps split Red Deer — the minority splits it more. | Roughly zero net seats flip. More splitting marginally reduces NDP ability to consolidate Red Deer urban voters. |
| **St. Albert-Sturgeon variants** | Both maps pair St. Albert with Sturgeon County; specific boundaries differ. | Zero seats flip. Partisan math essentially identical. |

**The net adds up.** One rural s.15(2) seat (roughly +0.7 UCP effective), plus 1 to 2 Calgary seats shifted through Zone A packing, equals roughly the 1-to-3 seat band the audit reports. The rest of the contested redraws mostly affect representation quality — who your MLA answers to — rather than the seat count. That is a distinction worth holding.

**Which of these is "fixable" in the November committee's map?** The rural s.15(2) boundary and the Calgary zone packing are the two that actually move seat math. If the committee redraws Rocky Mountain House-Banff Park to a normally-sized rural district and equalizes the Calgary zone populations, most of the seat-count effect disappears even if other minority choices survive. If the committee keeps both, the seat effect stays.

---

## Why 2027 is where this actually lands

**Twelve of fourteen razor-thin ridings in 2023 were in Calgary. That is where a 1-to-3 seat shift lands.**

The seat-count finding sounds small until you look at where Alberta's close races actually happened in 2023.

Fourteen of the province's 87 ridings were decided by less than three points in 2023. That is nearly double the seven seats in that range in 2019. The table below shows where those marginal seats live.

| Region | Marginal seats (<3 pp, 2023) |
|---|---|
| Calgary | 12 (Acadia, Glenmore, Foothills, Edgemont, Beddington, North West, North, Bow, Elbow, Cross, Klein, East) |
| Edmonton | 0 |
| Rural and other | 2 (Banff-Kananaskis, Lethbridge-East) |
| **Province total** | **14 of 87** |

Twelve of fourteen marginal seats are in Calgary — most of them in the same NDP-leaning zone that the minority's packing analysis flags. Calgary-Acadia was decided by 0.05 percentage points. Calgary-Glenmore by 0.09. Calgary-Foothills, Calgary-Edgemont, Banff-Kananaskis — all inside a single point.

Apply a 1.5 percentage point swing toward the UCP — the middle of our map-effect estimate — to the 2023 results, and six seats flip: five in Calgary, plus Banff-Kananaskis. Apply the same swing the other way and four seats flip toward the NDP, including Calgary-Bow, Calgary-North and Calgary-North West.

The 2023 election wasn't close enough for a map effect of this size to change who formed government. The UCP won 49 seats to the NDP's 38 — an 11-seat gap. A 1-to-3 seat map shift is a rounding error at that spread.

What does 2027 look like from here? The 338Canada aggregator, which pools Alberta polling into a seat projection, had the UCP at 52 percent and the NDP at 38 percent as of its April 12, 2026 update, with a central projection of 63 UCP seats to 24 NDP and UCP majority odds above 99 percent (Fournier, 338Canada Alberta, accessed April 22, 2026). On those numbers, 2027 does not look close. A 1-to-3 seat map effect does not change a 39-seat gap.

That matters for how to read this audit. The map effect is real and measurable. But whether it decides a 2027 election is a separate question from whether it decides an election. Alberta polling has moved more than 10 points inside a single cycle twice in the last decade — the NDP's 2015 win came out of a double-digit swing during the writ period; the UCP's 2023 result narrowed over months from a projected NDP lead. A 14-point April 2026 gap is not locked in.

The adopted map is also in place for more than one election. If 2027 breaks the way 338Canada's April snapshot suggests, the map effect is an insurance policy rather than a live intervention. If 2031 or 2035 tightens, the same effect is waiting. That's the stake. It is not whether the minority map is an extreme gerrymander. It is whether a shift equal to the margin in Calgary-Acadia in 2023 gets baked into the next decade of Alberta maps. That shift is small. It is also, by direct inspection, in a specific direction.

---

## The 91-seat proposal, so far

**No 91-seat map exists yet. What is known, what can be inferred, and what can't yet be said are three different things — in that order below.**

Premier Danielle Smith's stated reason for rejecting the commission's work is that the commissioners "did not want to lose two rural ridings." She was quoting, roughly, a conditional addendum Chair Miller filed alongside the majority report — a proposal that, if the legislature rejected 89 seats, the province should consider 91 instead, with two more rural seats added back.

The government took that off-ramp. On April 16 the legislature passed the motion 44 to 36. A select committee, chaired by UCP MLA Brandon Lunty, now has until November 2 to recommend a 91-seat map, advised by an independent panel whose members and terms haven't been made public. Elections Alberta called the timeline "very challenging" — boundary changes are supposed to be in place at least 18 months before a general election, and the next one is in fall 2027.

NDP Leader Naheed Nenshi called it "gerrymandering — a full-on assault on our democracy." NDP MLA Rakhi Pancholi said "changing electoral boundaries to give their own party an advantage is gerrymandering." Both framings assume a map that does not yet exist.

Here is what can and can't be said honestly.

### What is known

No 91-seat map has been drafted. The motion passed on party lines. The two extra seats appear, from the Premier's rationale, to be rural rather than urban.

### What can be inferred

If both added seats are rural, the rural-district population mean will drop from roughly 52,281 on the majority map to somewhere around 49,790, widening rural over-representation rather than narrowing it. The Calgary zone gap probably doesn't change much; the two added seats aren't urban.

### What can't yet be said

Whether the finished 91-seat map is a gerrymander. Nobody's seen it. The label needs a map to test. When the Lunty committee tables one in November, this audit will re-run every test in it against the new boundaries, and the answers will be what they are.

### The procedural question is different

That one doesn't wait. Replacing an independent boundary commission with a government-majority committee of MLAs is the thing the independent-commission model exists to prevent. Quebec's government in 1992, Ontario's in 1996, and BC's in 2008 all amended commission recommendations after the fact. None of them replaced the commission itself with a legislative committee. Whether Alberta's April 16 step is unprecedented in all Canadian history is a broader question this audit didn't fully survey. It is more government-controlled than any of the three recent comparators.

---

## Signatures detected

**Three gerrymander signatures appear under the minority map. None appear under the majority map.**

Packing means a party's voters are crammed into fewer, larger districts so their extra votes are wasted. Cracking means a group's voters are split across so many districts that they are outnumbered in each. An engineered boundary is a line drawn to qualify for a rule rather than to represent a place.

| Signature | Minority 2026 | Majority 2026 | Detail |
|---|---|---|---|
| Packing | Detected in Calgary Zone A | Not detected | NDP-leaning Calgary districts carry 6,656 more people each on average. About 113,000 extra NDP-leaning voters packed into existing districts. |
| Cracking | Detected for Airdrie | Not detected | Airdrie (84,000 people) split across 4 districts. None are named Airdrie. Airdrie voters are outnumbered in each. |
| Engineered boundary | Detected at Rocky Mountain House-Banff Park | Not detected | Boundary runs through empty Banff National Park land to qualify for a low-population rule. |

These are not aesthetic calls. Each signature follows a short checklist laid out in the academic report. The minority map meets the checklist in three places. The majority map does not meet it anywhere this audit could verify.

Cochrane's merger into a Calgary district looks like cracking but fails one test: Cochrane is too small (34,000 people) for its own district. The community concern is real; the formal signature is not.

---

## Stacking the deck, or looking like it? A suspicion sort

**Not every asymmetry in this audit is equally suspicious.** Some findings read as engineered on sight. Others look suspicious but have innocent explanations. The tabbed-list below sorts the audit's main findings by how much benefit of the doubt the data supports.

**Genuinely suspicious (pattern is hard to explain as coincidence):**

- **Rocky Mountain House-Banff Park's boundary through Banff National Park.** Empty parkland exists inside the district precisely because its inclusion is what lets the district qualify as a "special remote district." A drafter could have drawn a district with real inhabitants in it and accepted a higher population. This one was engineered.
- **Calgary-Nolan Hill-Cochrane reaching across the city boundary through a narrow corridor.** Nobody in the commission's public record proposed this configuration. It skips the neighbouring Calgary communities that share Nolan Hill's services to reach Cochrane.
- **Airdrie split four ways with no district named Airdrie.** A city of 84,000 appearing as a suffix on four different district names, none of which make Airdrie the primary constituency. Nobody in the public record asked for this split.

**Looks suspicious, but the data says it's probably innocent:**

- **The minority's rural districts are smaller on average (50,336 vs 52,281).** An earlier draft of this audit called this rural UCP packing. A deeper look shows it's mostly driven by one extra s.15(2) invocation — Rocky Mountain House-Banff Park uses the rule where the majority uses a normal rural district. Roughly a third of the gap comes from that single substitution. The two maps pack their ten smallest rural seats into almost-identical UCP territory.
- **Alberta's 2019 map already tilts UCP.** Pre-existing political-science research (Chen and Rodden, 2013) shows that urban-concentrated parties get disadvantaged by any neutrally-drawn map. The 2019 UCP tilt of −2.64% on the efficiency gap is mostly this, not boundary engineering.
- **The minority's efficiency gap shifts with election year.** Under 2023 data it's UCP-leaning. Under 2019 data it's NDP-leaning. Either this says the map is unstable in a concerning way, or it says that efficiency gap as a metric is noisy at this magnitude. The audit treats the flip as reason to be less confident in the partisan-math finding, not as evidence of engineering.

**Genuinely innocent (both maps do the same thing):**

- **Tsuut'ina Nation and Siksika Nation are kept intact in single named districts in both maps.** Where the commissioners agreed, they used sensible practice.
- **Most direct-rename districts.** 59 of the 89 majority districts map one-for-one to a 2019 district with minor boundary tweaks. The same is broadly true of the minority.

**Too early to say:**

- **The 91-seat committee's output.** The map doesn't exist. Treating it as either a gerrymander or a benign technical adjustment is pre-commitment, not analysis.
- **November committee output's relationship to the commission's minority.** The committee could stick close to the minority, dilute it, or produce something different. The audit's verdict will follow the data.

This sort deliberately leaves room for good-faith disagreement with the government's process without alleging deliberate partisan engineering everywhere.

## Under what scenarios does this matter

The audit's seat-count finding (roughly 1 to 3 seats of UCP advantage under 2023 voter conditions) is abstract without political context. Here is when that advantage actually changes outcomes.

**Doesn't matter — 2023-style blowout.** If 2027 looks like 2023 (UCP 49, NDP 38, an 11-seat gap), a 1 to 3 seat map effect does not change which party forms government. The 2023 election was already decided by ten more seats than the map effect could move.

**Matters for government type — tight race.** If an election lands within 5 seats of a tie, the 1 to 3 seat map effect is exactly the size that decides whether a party governs with a majority, a minority, or from opposition. Eight of the 14 Calgary ridings that sat inside a 3-point margin in 2023 could flip with a 1.5-point swing. As of April 2026, 338Canada's aggregate projection does not show 2027 landing in this range — it shows a UCP majority around 63 seats — but Alberta polling has moved more than 10 points inside a single cycle twice in the last decade, and the map is in place for future elections as well.

**Matters most — close Calgary race.** Seven of the 14 marginal 2023 Calgary ridings are ones the audit's Calgary zone-gap analysis identifies as packed under the minority map (more NDP voters per riding than the majority map has). If 2027 is close and those seats are where the race is decided, the map choice weighs directly.

**Doesn't matter — the committee produces a different map.** The November 2026 committee could make any of this moot by producing a new map that resembles the majority more than the minority. The audit's findings apply to what the commission produced, not to whatever the committee does.

## Policy decision, or partisan move?

It is tempting to frame Alberta's April 16 action as either "the UCP is stacking the deck" or "the UCP is making a policy choice about rural representation the commission didn't get right." Both framings oversimplify. The evidence lets us say three specific things:

- **The process change is real.** The government moved the drafting pencil from an independent commission to a UCP-majority MLA committee. That happened on April 16. Premier Smith's stated reason — "the commission did not want to lose two rural ridings" — is a policy rationale for the 91-seat plan.
- **Three minority configurations that the chair said had no public support actually did** (Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere). Two configurations the chair flagged genuinely lacked support (Airdrie 4-way, Nolan Hill-Cochrane). A policy-driven committee could keep the three publicly-supported ones and drop the two that weren't asked for. A partisan-driven committee might do the opposite.
- **The audit cannot distinguish motive from evidence alone.** What it can do is tell you what to watch for in November. If the committee's map keeps Nolan Hill-Cochrane and the Airdrie 4-way split, that's a signal worth taking seriously. If the committee drops those two and retains only the publicly-supported configurations, the partisan-framing gets weaker.

The responsible reader position here is patience with specifics. "The UCP is stacking the deck" may be true. Saying so now, before the map exists, requires a leap the data does not make. So does "the UCP is just making good-faith policy adjustments."

## What this audit does not say

**Four claims this audit does not support — no matter which side wants to make them.**

The temptation on either side of this file is to pick the findings that suit. Both sides have that temptation. So, one more time, in plain terms, here is what the numbers do not support.

The minority map is not an extreme gerrymander by any published international standard. Its efficiency gap is a fifth of the threshold U.S. courts have used. The seat-count advantage crosses zero at a 95 percent confidence level, and flips direction depending on which past election you use as a baseline.

The minority map is also not indistinguishable from the majority. Six separate measurements show consistent, small, UCP-favourable differences. The Calgary zone gap, the Airdrie split, the Rocky Mountain House-Banff Park shape, and the community splits aren't statistical artefacts. They are what the commissioners drew.

The majority map is not "neutral" in some absolute sense. Alberta's geography — big urban NDP concentrations in Edmonton and Calgary, rural UCP strength spread thin — gives any good-faith map a small UCP tilt. The majority keeps that tilt roughly where it was. "More neutral than the minority" is fair. "Neutral" on its own isn't.

The April 16 government action is not established as a constitutional violation. The Supreme Court's 1991 Saskatchewan Reference sets an "effective representation" standard that leaves substantial room for legislative involvement. Whether the April 16 process clears that bar is a question for courts, not an audit.

And the 91-seat committee's map cannot yet be called anything — because it doesn't exist. Calling it a gerrymander now requires a leap the data does not make. Calling it benign requires the same leap.

---

## How this was done, and how to check it

**Every number in this report can be re-run from public files.**

The analysis ran through an AI-assisted pipeline using Claude Opus 4.7, open-source Python tools, and the commission's own public documents. The [full technical report](report_academic.md) walks every calculation, cites every submission, and lists every piece of code. The [visualized version](report.html) carries three figures — a map comparison, the Calgary zone gap, and the marginal-seats chart — for readers who want to see rather than read.

The data folder holds the commission's population tables and Elections Alberta's vote returns. The analysis folder holds the scripts. Running them on the same public files will produce the same numbers in this document. That's the point. A reader who doesn't trust one paragraph of this can run the script behind it and check.

This audit will be updated when Elections Alberta releases the digital boundary files, when the Lunty committee tables its 91-seat map, or when additional submissions become searchable. The raw data and the commits are in the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit). If you find an error, file an issue — it accepts them.

---

## Further reading

- [Full technical report with every calculation cited](report_academic.md)
- [Visualized version with three interactive figures](report.html)
- [Marginal-seats analysis and 2023 flip-zone list](analysis/v0_1_marginal_seats_findings.md)
- [Source repository, data, and commit history](https://github.com/Ixby/alberta-electoral-boundaries-audit)

## Source trail

Sources and submission identifiers are cited in-line throughout. Full bibliography in the [academic report](report_academic.md). Key public sources:

- Premier Smith quote: Rimbey Review, April 16, 2026
- NDP responses: DiscoverAirdrie, April 17, 2026
- Seat allocation figures: Global News, March 26, 2026
- Marginal-seat analysis: Elections Alberta 2023 Statement of Vote
