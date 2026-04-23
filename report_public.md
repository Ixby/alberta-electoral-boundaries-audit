# Two Maps, One Province

*Three commissioners. Two maps. One legislative override. An audit of what Alberta's 2026 boundary maps actually say, and what the government now wants to replace them with.*

By Will Conner · Mount Royal University, BSc Computer Information Systems (4th year) · Published April 22, 2026

[Full technical report](report_academic.md) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)

---

### Disclosure

I am not a neutral observer of Alberta politics. Going into this project, I believed the UCP government's handling of boundary redistribution was worth scrutiny. That belief could have shaped what I looked for. The audit is designed to answer back: every test is applied the same way to both maps; every numeric claim traces to a script and data file anyone can re-run; an independent self-critique sits in the repository and flagged me when my own language overstated a finding. Three specific cases in this document are places where my prior was wrong and the numbers said so — those retractions are here because the methodology surfaced them.

---

> **The bottom line, in four sentences.** The minority map tilts UCP by a small, measurable amount in a tied election — about 1 to 3 seats, well under any published gerrymander cutoff. Several of the minority's distinctive choices — the Banff-park extension under s.15(2), the four-way Airdrie split, and the Nolan Hill-Cochrane corridor — fail their own stated rationales when tested against the census, the statutory population limits, and the commission's own public submissions. Six of the seven contested redraws had cleaner options the minority didn't take. The bigger story is that the government rejected the commission's work and handed the drafting pencil to a committee of MLAs.

---

On March 23, Alberta's Electoral Boundaries Commission tabled not one map but two. The five commissioners could not agree. Three signed a majority report drawing 89 ridings in a shape most of them could defend. The other two signed a dissenting minority report with different lines in several places. Twenty-four days later, on April 16, the provincial government rejected the majority map outright, passed a motion 44 to 36, and handed the drafting pencil to a committee of MLAs with a UCP majority. The committee is chaired by UCP backbencher Brandon Lunty. It has until November 2 to come back with a 91-seat map instead.

This audit looked at both commission maps using public data, and at the 91-seat plan as far as the public record allows. The headline is narrower than some early commentary has suggested. The minority map is measurably, modestly friendlier to the UCP than the majority map on three of four standard tests. It is nowhere near the threshold American courts have used to flag an extreme gerrymander. The government's decision to replace the commission is a bigger story than the map itself.

What follows is a walk through the numbers, the shapes on the page, and what can and cannot be said about either.

---

## PART I · HOW THE COMMISSION CAME APART

### Five commissioners, two maps

**Five commissioners. Two maps. One dissent from the chair.** Here is how the split happened.

Alberta's Electoral Boundaries Commission is a five-member body that redraws the province's 87 ridings roughly every eight years. Two commissioners are appointed on the recommendation of the government, two on the recommendation of the opposition, and one — the chair — is named by the Chief Justice of Alberta. For 2026, that chair was Dallas Miller.

The commission holds hearings, accepts written submissions from the public, and then proposes a map. It is supposed to be arm's length from the legislature. That's the theory. It has worked that way in Alberta for most of the province's history.

This time, the commission split 3-to-2. The three commissioners in the majority — the chair and the two opposition-appointed members (Greg Clark, a former Alberta Party MLA for Calgary-Elbow, being one of them) — proposed 89 ridings. The two government-appointed commissioners dissented and proposed their own 89-seat configuration. Both maps add two seats to the current 87 to account for twenty percent population growth since 2017. Both agreed on most of the map. They disagreed, visibly, on about a dozen districts.

In his Appendix C, Chair Miller flagged three of the minority's districts by name as what he called *engineered* — drawn, he wrote, to satisfy a rule rather than to reflect a real community. He also wrote that the minority's configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had **no public support** in the 1,340-plus submissions the commission received.

Both of those claims turn out to hold up in some places and not in others. The audit tested both.

---

### Where the minority map is different

**Most of the province is the same on both maps. The fights are in Calgary and its commuter belt.** The fastest way to see what the maps disagree about is to look at specific districts.

| District | Majority map | Minority map |
|---|---|---|
| Rocky Mountain House-Banff Park | Does not exist | Stretches through uninhabited alpine to qualify as "special remote" |
| Olds-Three Hills-Didsbury | Rural anchor kept | Reaches south to capture part of Airdrie |
| Calgary-Nolan Hill-Cochrane | Does not exist | Skips intervening Calgary neighbourhoods |
| Airdrie | Split two ways, city named | Split four ways, city name absent |
| Chestermere | Paired with Strathmore | Split between Calgary and Chestermere-Strathmore |

*Table 1. The five districts where the maps disagree most visibly.*

**Rocky Mountain House-Banff Park.** The minority draws a district that stretches from Rocky Mountain House down through the uninhabited alpine of Banff National Park to the British Columbia border. Without that southern extension through empty park land, the district wouldn't have enough geography to qualify as a "special remote district" under section 15(2) of the Electoral Boundaries Commission Act — the rule that lets very-remote ridings sit more than 25 percent below the provincial population average. Strip out the empty-park extension and the district's population of 38,298 — 30 percent below the provincial average of 54,929 — can't be justified. The shape exists to qualify for the rule.

**Olds-Three Hills-Didsbury.** Named for three small rural towns in central Alberta. The district also reaches south and captures a substantial piece of Airdrie — which has more people than the three named towns combined. That's not how a boundary commission normally names a district.

**Calgary-Nolan Hill-Cochrane.** Reaches from the town of Cochrane across Calgary's northwest corner to the Nolan Hill neighbourhood, skipping intervening Calgary neighbourhoods. Chair Miller singled this one out in his own report.

**Airdrie, four ways.** Airdrie is a city of about 74,100 in the 2021 census. (The minority's paperwork uses 84,000, the 2024 estimate.) The majority map puts Airdrie into two ridings — Airdrie-East and Airdrie-Cochrane — both of which carry the city's name. The minority splits it four ways, and no resulting district is named Airdrie. An Airdrie voter under the minority map would never see their city on their ballot. The city projects growth to about 128,000 by 2033. That is a real argument for more Airdrie-adjacent seats next time. It is not an argument for four-way splitting today; a two-way split fits the legal window and leaves room for the next redraw.

**Chestermere.** A bedroom community of about 25,000 east of Calgary. The majority keeps it with its natural neighbour Strathmore. The minority splits it between Calgary and Chestermere-Strathmore.

On a map, the difference looks small. On a population table, it's also small: the provincial average is 54,929, and individual districts under both maps cluster inside the legal plus-or-minus 25 percent window. But the minority's spread is wider. Under the majority map, the average district is about 3,180 people off the provincial mean. Under the minority, it's 4,707 — almost fifty percent more variation. Fifteen minority districts sit more than ten percent off the mean. Under the majority, only five do.

Inside Calgary the gap sharpens. Calgary has two rough political zones: a north-east-central band that tends to vote NDP, and a south-west band that tends to vote UCP. Under the majority map, the average district size is nearly identical across the two zones. Under the minority, NDP-leaning Calgary districts average 61,225 people; UCP-leaning ones average 54,569. That's a 12.2 percent gap, and it means the same number of NDP votes in Calgary elects fewer MLAs under the minority map. The zone gap doesn't depend on a model or a vote projection — it's straight from the commission's own population tables.

> **Sidebar · What is a gerrymander, in plain terms?** The word covers any map that uses district lines for partisan advantage. The usual techniques are *packing*, where you cram an opposing party's voters into a few big districts where they win overwhelmingly and waste the rest of their votes, and *cracking*, where you spread an opposing party's voters thinly across districts where they can't win any. The Calgary zone gap above is the signature of packing. The Airdrie four-way split is the signature of cracking.

**A pattern, not a one-off.** The Airdrie four-way split looked like a one-city decision until a broader symmetric scan was run. Every Alberta city with 50,000 or more residents was checked for four-way splits on both maps. The majority splits none of them four ways. The minority splits three — Airdrie, **Lethbridge**, and **Red Deer**. Lethbridge goes to four districts under the minority (Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) where the majority keeps it at two. Red Deer does the same. Three cities, same pattern, minority only. That is the audit's definition of a pattern. Raw counter-test data at [data/v0_1_majority_symmetry_counter_test.csv](data/v0_1_majority_symmetry_counter_test.csv).

---

### The chair's "no public support" claim, sorted

**The chair was wrong in three places, right in three, and the record is split on one.** A closer look at the 1,252 machine-readable submissions — 93 percent of the total — shows a tiered picture.

The audit searched every submission for keywords matching each disputed district, then hand-reviewed the hits. Two districts the minority pushed that Appendix C didn't list are added because they belong in the same tier: Rocky Mountain House-Banff Park and Olds-Three Hills-Didsbury.

| Configuration | Public submissions | Verdict on chair |
|---|---|---|
| **Rocky Mountain House-Banff Park** | 5 support (including detailed position paper EBC-2025-2-0619), 1 oppose | Chair materially wrong; minority adopted from public record |
| **Olds-Three Hills-Didsbury rural unit** | 3 support (2 from Beiseker), 1 oppose | Chair materially wrong |
| **Chestermere as its own unit** | 3 support, 1 oppose | Chair materially wrong |
| **Red Deer-area hybrids** | 4 support, 4 oppose, 15 neutral/ambiguous | Technically false, but record evenly divided |
| **Airdrie 4-way split** | 0 submissions propose this specific carve | Chair's characterization holds |
| **Calgary-Nolan Hill-Cochrane** | 0 submissions propose this configuration | Chair's characterization holds |
| **St. Albert-Sturgeon minority alternative** | 2 name "St. Albert-Sturgeon," but they mean the majority version | Chair's characterization holds |

*Table 2. Seven disputed districts, ordered strongest public counter-evidence at top.*

The tiering matters. A flat "the chair lied about public support" is wrong. So is "the chair was right." The precise story is: on three configurations the minority was adopting public proposals, and the chair's Appendix C reversed the record. On one, the record is split. On three, the chair's description of the submissions is defensible.

---

## PART II · WHAT THE MAPS ACTUALLY DO

### Four fairness tests, read together

**Four standard measures of partisan fairness. Three of them describe the same wasted-vote story. The fourth looks at a different shape. Here is how to read them together.**

The audit runs four standard measures of partisan fairness against each of the three maps. They are not four independent verdicts on the same question — they are four different cameras pointed at the same underlying pattern, and they pick up different features.

| Test | What it measures | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|---|
| Efficiency gap | How many votes each party "wastes" (votes for losers plus surplus votes for winners) | −2.64% | −0.85% | −1.36% |
| Mean-median gap | Whether one party's vote share skews left or right of the typical district | −2.22 | −0.18 | −0.33 |
| NDP seats at a tied vote | How many seats the NDP would win if the province-wide vote were 50/50 | 46 | 44 | 42 |
| Declination | The geometric angle between the two parties' winning-district clouds | −0.034 | −0.021 | −0.015 |

*Table 3. Reading convention: negative numbers favour the UCP in this reporting; positive favour the NDP.*

**Three tests agree with each other, and one points the other way. That is not the end of the analysis.**

The first three tests — efficiency gap, mean-median, and NDP seats at a tied vote — all say the minority is modestly more UCP-favourable than the majority. The fourth — declination — says the minority is *less* UCP-favourable than the majority. At first read that looks like a 3-versus-1 vote, and readers sometimes decide on that basis to lower their confidence. That would be the wrong conclusion from what the math is actually doing.

**The first three tests are closely related.** The efficiency gap, the mean-median, and seats-at-50/50 are not four independent tests any more than a thermometer, a thermostat, and a hand on the forehead are three independent tests of temperature. All three ask: does one party's votes translate into seats as efficiently as the other party's? They use different formulas, but they are measuring the same property. When one of them shows a tilt, the others usually show the same tilt. When all three agree, that is consistency, not triangulation.

**Declination is measuring something different.** It does not count wasted votes. It looks at the shape each party's winning districts make on a graph, and it measures how different those two shapes are. When both parties win by similar margins across the map, declination is low. When one party wins by blowout and the other by narrow margins, declination is high. The question is not "who wastes more votes?" but "do the two parties win in similar ways?"

**Why they can disagree.** Consider two ways to give a party a structural disadvantage on a map:

1. **Blowout packing.** Pack the losing party into a few districts they win 80-20. They win those seats but waste huge numbers of votes. Efficiency gap is large. Declination is large too — the two parties' winning patterns look very different.
2. **Narrow-margin packing.** Pack the losing party into many districts they lose by thin margins, 45-55. They lose each one by a sliver. Wasted votes still add up, so efficiency gap is large. But declination is *smaller*, because the losing districts sit close to the margin and the two patterns look similar.

The Alberta minority map shows the second pattern. It packs NDP-leaning Calgary voters into larger districts (the 12.2% Calgary zone gap), splits Airdrie / Lethbridge / Red Deer into four-way configurations, and leaves NDP voters in narrow-margin losses rather than blowout losses. Efficiency gap says "you wasted more NDP votes." Declination says "your winning-district geometry is not especially asymmetric." Both are looking at the same structural map; they pick up different fingerprints of the same design.

**The declination disagreement does not falsify the other three tests. It tells you how the packing works.** If the minority were a blowout-packing map, declination would agree. Because the minority is a narrow-margin-packing map, it does not. A hostile reader can cite declination to argue the effect is smaller than the other three tests suggest. The honest response: declination is consistent with packing through narrow losses, which is what the four-way splits and zone gap show on their own.

**What the size of the tilt means.** The minority efficiency gap of −1.36% is about one-fifth of the 7% threshold American courts have used to flag suspect maps. In seats, the central estimate is two NDP seats lost under the minority at a tied vote. The 95 percent confidence interval crosses zero. Under the full range of modelling assumptions, the minority could cost the NDP three seats or give the NDP one extra seat. The direction is UCP-favourable in about 90 percent of runs. The size is not pinned to a single number.

**The election-input wrinkle.** Run the same calculation using the 2019 election vote pattern instead of 2023 and the advantage reverses — the minority map would help the NDP under 2019 voters. When a test's answer depends on which election you feed it, the answer is partly about the voters rather than about the map. That said, plugging in April 2026 polling from 338Canada instead of 2023 results gives the same one-seat minority-vs-majority gap — but in the opposite direction, because the province-wide environment is so UCP-favourable that the minority map's narrow-margin packing structure flips to the NDP's advantage. The gap size is stable across 2023 and April 2026 inputs; the direction depends on the competitive environment.

**How does this compare to other Canadian redistricts?** A first-pass catalogue of six other Canadian redistribution cycles — Federal 2022 (Alberta sub-commission), BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, and Manitoba 2018 — finds that more than half of recent Canadian cycles produce zero partisan shift between the commission's interim draft and its final report. The ones that do produce a shift do so at modest magnitude. Alberta 2025-26's low-end 0.5 point shift is in the same range as Manitoba 2018 and Alberta's own 2017 cycle. Its high-end 1.6 point shift, under the wider modelling assumptions, exceeds the largest Canadian inter-map shift in this sample. Put simply: the minority map is not out of line with the typical Canadian redistricting exercise at its low end, but it is at the far end of the observed Canadian range at its high end. Full data at [analysis/v0_1_canadian_base_rate_computed.md](analysis/v0_1_canadian_base_rate_computed.md).

**A common defence, tested.** One argument says both 2026 maps look UCP-favourable because urban NDP voters naturally cluster in Calgary and Edmonton. Any fair map on Alberta's geography, the argument goes, would tilt UCP. A test of 150 neutrally-drawn 87-seat plans confirms the direction — neutral Alberta maps do produce a UCP-favourable efficiency gap, around −2.3 to −2.4 percent on average. But the mechanism the argument invokes does not hold. In Alberta, UCP voters in rural ridings win by an average of 43 points. NDP voters in urban ridings win by 21 points. The UCP is the more concentrated party by wasted-vote measure (15.9 percent excess votes to the NDP's 9.3). Alberta's UCP tilt comes from rural UCP margins being very wide, not from NDP voters being packed into cities. More at [analysis/v0_1_chen_rodden_alberta_validation.md](analysis/v0_1_chen_rodden_alberta_validation.md).

> **Sidebar · What's the efficiency gap?** A measure of how many votes each party "wastes." Votes for a loser are wasted. Votes for a winner above what was needed to win are also wasted. The efficiency gap is the difference between the two parties' wasted-vote rates. Zero means neither party systematically wastes more votes than the other. Negative numbers (in this province's reporting convention) favour the UCP; positive favour the NDP.

> **Sidebar · What's declination?** A geometric measure. Draw each party's winning districts as points on a graph — x-axis is the district's winning margin, y-axis is the district's vote share. The two parties produce two clouds of points. Declination measures the angle between the best-fit lines through each cloud. A symmetric map produces near-zero declination. A packed map — where one party wins by large margins and the other by small margins — produces larger declination.

> **Sidebar · What's the mean-median gap?** The difference between the *mean* and *median* of a party's district vote shares across all the districts on the map. If the two are the same, the map is symmetric around the middle district. If they differ, the party is either over-represented or under-represented relative to what its vote share would predict. The 3 pp threshold from McDonald and Best (2015) is the point at which serious partisan skew is typically flagged; Alberta's mean-median gaps are well under that.

---

### Per-redraw seat-count breakdown

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

*Table 4. Each contested redraw, what it does, and how much it moves the seat count.*

**The net adds up.** One rural s.15(2) seat (roughly +0.7 UCP effective), plus 1 to 2 Calgary seats shifted through Zone A packing, equals roughly the 1-to-3 seat band the audit reports. The rest of the contested redraws mostly affect representation quality — who your MLA answers to — rather than the seat count. That is a distinction worth holding.

**Which of these is "fixable" in the November committee's map?** The rural s.15(2) boundary and the Calgary zone packing are the two that actually move seat math. If the committee redraws Rocky Mountain House-Banff Park to a normally-sized rural district and equalizes the Calgary zone populations, most of the seat-count effect disappears even if other minority choices survive. If the committee keeps both, the seat effect stays.

---

### The three signatures

**Three gerrymander signatures appear under the minority map. None appear under the majority map.**

Packing means a party's voters are crammed into fewer, larger districts so their extra votes are wasted. Cracking means a group's voters are split across so many districts that they are outnumbered in each. An engineered boundary is a line drawn to qualify for a rule rather than to represent a place.

| Signature | Minority 2026 | Majority 2026 | Detail |
|---|---|---|---|
| Packing | Detected in Calgary Zone A | Not detected | NDP-leaning Calgary districts carry 6,656 more people each on average. About 113,000 extra NDP-leaning voters packed into existing districts. |
| Cracking | Detected for Airdrie | Not detected | Airdrie (84,000 people) split across 4 districts. None are named Airdrie. Airdrie voters are outnumbered in each. |
| Engineered boundary | Detected at Rocky Mountain House-Banff Park | Not detected | Boundary runs through empty Banff National Park land to qualify for a low-population rule. |

*Table 5. Three formal signatures of partisan map design. Each follows a short checklist laid out in the academic report; all three are met by the minority map in three specific places.*

**A compactness check on the shapes themselves.** Elections Alberta has not released shapefiles for the 2026 proposals, but an approximation built from the 2019 boundaries plus the commission's hybrid crosswalks lets the audit compute compactness scores for the roughly two-thirds to three-quarters of EDs whose boundaries can be inferred with confidence. On that measurable subset, the minority map has about twice the rate of low-compactness districts (where Polsby-Popper compactness falls below 0.25) as the majority map — 7 percent versus 3.5 percent. The three most controversial minority districts (Rocky Mountain House-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) are exactly the ones whose actual shapes the audit cannot score without the real shapefiles. The audit has drafted a request to Elections Alberta asking for research access to the proposal shapefiles.

---

### Where the minority's rationales fail

**Six of seven contested redraws had cleaner options. The minority did not take them.**

The same question applies to every disputed redraw: was the minority's choice the best available geographic option, or was a cleaner alternative on the table? The answer varies by case. The table below names the alternative where one exists.

| Contested redraw | Was a cleaner alternative available? | What it would have been |
|---|---|---|
| **Cochrane merged with Calgary-Nolan Hill** | Yes | Cochrane plus Rocky View rural (as the majority does), or Cochrane plus the Bow Valley mountain corridor, or Cochrane plus the foothills-north belt. |
| **Airdrie split four ways** | Yes | Airdrie is 84,000 people. Two Airdrie-named districts (what the majority does) is the minimum and maximum needed. Four districts is not forced by population or geography. |
| **Rocky Mountain House-Banff Park (s.15(2))** | Yes | Rocky Mountain House plus Clearwater County plus Sundre fits a normal-sized rural district without invoking s.15(2) and without extending the boundary through uninhabited national-park land. Roughly what the majority's Lacombe-Clearwater does. |
| **Olds-Three Hills-Didsbury reaching into Airdrie** | Yes | Olds plus Didsbury plus Three Hills plus Carstairs plus Beiseker plus Crossfield plus the surrounding agricultural belt adds up to a population-feasible rural district without the Airdrie slice. Rural anchors keep rural representation; Airdrie stays intact. |
| **Chestermere partially split into Calgary** | Yes | Chestermere plus Strathmore (what the majority does) keeps both rural-edge communities whole in one district. Neither needs a Calgary attachment. |
| **Red Deer split across four hybrids** | Yes | Red Deer (population 100,844 at 2021 Census; ~106,000 at 2024 estimate) needs two districts. Two Red Deer-core districts plus separate adjacent-rural districts is the standard split. Four Red Deer-named hybrids dilutes city representation without population necessity. |
| **St. Albert-Sturgeon variants** | No materially different option on the table | Both maps pair St. Albert with Sturgeon County rural territory. The variants differ on specific boundaries inside that pairing rather than on the pairing concept. |

*Table 6. Seven contested redraws, whether a cleaner option existed, and what it would have been.*

Six of seven contested redraws had cleaner options. The minority did not take them. The seventh (St. Albert-Sturgeon) has no real alternative. This is not a claim that every departure is engineered. It is an observation. When not forced by geography or population, the minority chose the less-natural option. The majority, with the same constraints, chose the natural option in all seven cases.

**Were the minority's configurations forced by population math?** Five population-math tests were run from Statistics Canada 2021 Census data against the minority's specific justifications. All five came back the same way.

| Minority's justification | Population-math verdict |
|---|---|
| Olds-Three Hills-Didsbury needs the Airdrie slice for population | **Fails.** Rural counties and towns (Mountain View + Kneehill + Olds + Didsbury + Three Hills + Carstairs + Beiseker + Crossfield) sum to 43,691 — above the 41,197 lower limit. The Airdrie slice is not needed. |
| Rocky Mountain House-Banff Park needs the Banff NP extension for area | **Fails.** The 2019 predecessor district was already 24,468 km², above the 20,000 km² s.15(2) threshold. The NP extension is not load-bearing for the area criterion. |
| Airdrie needs a 4-way split because 84,000 is too many for one district | **Fails.** Airdrie's 2021 population is 74,100 (the 84,000 figure is stale). A 2-way split of 37,000 each plus a small rural addition fits cleanly under the 68,661 upper limit. Four splits are not required. |
| Red Deer needs 4 districts | **Fails.** Red Deer at 100,844 divided by the 68,661 upper limit rounds up to 2. Two Red Deer districts is the minimum, which is what the majority does. Four is unforced. |
| Chestermere must be split into Calgary | **Fails.** Chestermere + Strathmore + Wheatland County = 45,240, a viable standalone hybrid. No part of Chestermere is mathematically required by the Calgary-Peigan-Chestermere district. |

*Table 7. Five of the minority's specific population-math defences, tested.*

Five tested, five failed. In plain language: none of these five contested minority configurations were required by the population rules they would invoke as defence. The configurations may be defensible on other grounds — community philosophy, commuter patterns, geographic intuition — but not on population math. The specific arithmetic defence is not available.

Raw tables and the reproducible pipeline: [analysis/v0_1_justification_tests_findings.md](analysis/v0_1_justification_tests_findings.md). Rationale-by-rationale validation: [analysis/v0_1_minority_rationales_validation.md](analysis/v0_1_minority_rationales_validation.md).

---

### Which data did the commission actually use?

Both the majority and minority reports say they used "the 2021 census updated to a July 1, 2024 estimate." Trace the arithmetic and the per-district tables add up to the July 2024 Alberta Treasury Board estimate — about 4.89 million — not the 2021 census count of about 4.26 million. The provincial average used to draw the ±25 percent legal window is 54,929, which is the 2024 number divided by 89, not the 2021 number divided by 89. The Electoral Boundaries Commission Act says the commission "is to use" the decennial census and "may" use more recent information "in conjunction with" it. Whether the commission's approach fits the statute is a question for lawyers; what the audit can say is that both sides used fresher data than they disclosed, and any reader who wants to verify against the 2021 baseline the Act names will find the baseline is not actually what the commission used. Details, including the side-by-side Plan A (2021 census) vs Plan B (2024 estimate) re-run of the five justification tests, are in [analysis/v0_1_plan_b_cross_check.md](analysis/v0_1_plan_b_cross_check.md). All five tests reach the same verdict under both data sources; three become more clearly "unforced" at 2024 numbers. Airdrie's April 2025 municipal census measured 90,044 residents (the provincial 2025 estimate is about 92,500). Either number means a two-way split already clears the legal floor with no rural top-up needed. The audit has also drafted a separate legislative-reform proposal with two options for clarifying §12 going forward: [analysis/v0_1_act_amendment_proposal.md](analysis/v0_1_act_amendment_proposal.md).

**Old data, new boundaries — the cycle-lag problem.** Alberta grew about 17.8 percent between the 2021 census and mid-2025. Plug the mid-2025 populations back into the 2026 proposed maps and the majority map sees zero districts shift out of the ±25 percent window. The minority map sees five: Calgary-North East, both Fort McMurray ridings, Peace River, and Lesser Slave Lake. That is a second-order population-equality signal the census-only view misses. The legal baseline does not change — the Act binds the commission to census data — but a map that looks fine on 2021 numbers and fails on 2025 numbers is a map whose legal safety depends on the lag. More at [analysis/v0_1_cycle_lag_analysis.md](analysis/v0_1_cycle_lag_analysis.md).

**Two more rationales, checked against simple public data.** The minority defends Calgary-Bow-Springbank partly on the claim that Springbank and west Calgary share schools. They do not. Springbank is in Rocky View Schools; west Calgary is in the Calgary Board of Education. The same mismatch shows up for Red Deer-Sylvan Lake: Sylvan Lake is in Chinook's Edge; Red Deer city is in Red Deer Public. The "shared schools" argument does not hold in either case. The minority's broader regional-economy framing does fare better. Alberta has a Central REDA covering Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake. It has a Calgary Regional Partnership covering Calgary, Airdrie, Cochrane, Chestermere, and the commuter ring. Those groupings are real. They do not pick specific boundaries, but they show the cities cluster for reasons other than partisan math.

---

### The Calgary hybrid concentration

**Total hybrid counts are almost identical across the three maps. What changed is where the hybrids are. The minority concentrates them in Calgary.**

A hybrid district is one that pairs part of a city with part of a surrounding rural area or another municipality. The commission's own Appendix C defines it.

| Map | Total hybrid districts | Calgary hybrids | Edmonton hybrids | Rest-of-province hybrids |
|---|---|---|---|---|
| 2019 (current) | 19 | 0 | 0 | 19 (including Airdrie-Cochrane, Chestermere-Strathmore, several rural-town pairings) |
| Majority 2026 | 19 | 4 | 2 | 13 |
| Minority 2026 | 20 | **7** | 4 (one a merger) | 9 |

*Table 8. Hybrid-district count and distribution by region.*

The total count is roughly constant. The distribution is not.

**The minority's seven Calgary hybrids** are the key shift: Calgary-Bow-Springbank, Calgary-De Winton, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, Calgary-North West-Bearspaw, Calgary-Peigan-Chestermere, and Calgary-West-Tsuut'ina. Each one takes a rural community or small town — Bearspaw, Springbank, Cochrane, Chestermere, Airdrie-West, Tsuut'ina Nation — and pairs it with a Calgary neighbourhood. The Calgary side has more people. The rural side becomes a minority inside a Calgary-dominated district.

The majority has only four Calgary hybrids. Three are narrow. Calgary-East extends just past city limits. Falconridge-Conrich adds a small adjacent community. West-Elbow Valley picks up a contiguous suburb. Glenmore-Tsuut'ina includes the Tsuut'ina Nation (both maps do this). The majority keeps Cochrane as its own district. It keeps Chestermere with Strathmore. It keeps Airdrie inside Airdrie-named districts.

The same shift shows around Red Deer. The majority has **zero** Red Deer hybrids. It uses two Red Deer-only districts (Red Deer-North, Red Deer-South) and keeps rural districts separate. The minority has **four** Red Deer hybrids. Each takes part of Red Deer and pairs it with a nearby town or rural area. A city of roughly 100,000 at the 2021 Census (and about 106,000 at 2024 estimates) gets split four ways with no district of its own.

**The government's stated reason.** Premier Smith's justification for rejecting the commission's work and pursuing a 91-seat alternative was that the commission "did not want to lose two rural ridings." The stated policy goal is preserving rural representation.

That rationale aligns with the majority map. The majority keeps Cochrane standalone. It keeps Chestermere with Strathmore. It gives High River its own rural district. Rural communities sit in rural-named districts where rural voters are the majority.

The minority map does the opposite. The seven Calgary hybrids pull rural and small-town communities into Calgary-dominated districts. Rural voters become a minority in those seats. The Calgary side sets the political character. That is the reverse of rural preservation. It dilutes rural voice into urban majorities.

On the evidence, a government whose stated reason is rural preservation would support the majority's approach. The November committee's 91-seat map will tell us whether the stated reason matches the policy.

---

### What the audit extends benefit of the doubt to

**Not every asymmetry in this audit is equally suspicious.** The signatures table above names what the data flags as hard to explain as coincidence. The list below handles the other findings — the ones that look suspicious at first glance but, on closer inspection, have innocent explanations.

**Probably innocent — looks suspicious, but the data says otherwise:**

- **The minority's rural districts are smaller on average (50,336 vs 52,281).** An earlier draft of this audit called this rural UCP packing. A deeper look shows it's mostly driven by one extra s.15(2) invocation — Rocky Mountain House-Banff Park uses the rule where the majority uses a normal rural district. Roughly a third of the gap comes from that single substitution. The two maps pack their ten smallest rural seats into almost-identical UCP territory.
- **Alberta's 2019 map already tilts UCP.** Pre-existing political-science research (Chen and Rodden, 2013) shows that urban-concentrated parties get disadvantaged by any neutrally-drawn map. The 2019 UCP tilt of −2.64% on the efficiency gap is mostly this, not boundary engineering.
- **The minority's efficiency gap shifts with election year.** Under 2023 data it's UCP-leaning. Under 2019 data it's NDP-leaning. Either this says the map is unstable in a concerning way, or it says that efficiency gap as a metric is noisy at this magnitude. The audit treats the flip as reason to be less confident in the partisan-math finding, not as evidence of engineering.

**Genuinely innocent — both maps do the same thing:**

- **Tsuut'ina Nation and Siksika Nation are kept intact in single named districts in both maps.** Where the commissioners agreed, they used sensible practice.
- **Most direct-rename districts.** 59 of the 89 majority districts map one-for-one to a 2019 district with minor boundary tweaks. The same is broadly true of the minority.

**Too early to say:**

- **The 91-seat committee's output.** The map doesn't exist. Treating it as either a gerrymander or a benign technical adjustment is pre-commitment, not analysis.
- **November committee output's relationship to the commission's minority.** The committee could stick close to the minority, dilute it, or produce something different. The audit's verdict will follow the data.

This pass leaves room for good-faith disagreement with the minority's choices without alleging deliberate partisan engineering across every finding. The three signatures above are where the case is strong. Everything else has innocent readings available.

All of this assumes the minority map matters. On April 16, the government decided it does not. A new map, drafted outside the commission, will replace both 89-seat proposals before 2027. Part III covers that process.

---

## PART III · WHAT COMES NEXT

### The 91-seat idea did not come from the majority

**Premier Smith said the commission itself recommended a 91-seat option. The commission's own documentation says something different.**

Premier Danielle Smith says the commissioners "did not want to lose two rural ridings." She was pointing to a part of the commission's final report called Recommendation 5 — an addendum filed at the back of the majority report. If the legislature rejected 89 seats, it said, the province should go to 91 instead with two more rural seats added back.

Two things about Recommendation 5 matter for how the April 16 motion should be read.

**First, its opening sentence is written in the voice of "the majority."** It says "the majority of the Commission recommends" the move to 91 seats.

**Second, the same document admits the majority did not actually agree.** Chair Dallas Miller writes, in the same addendum: *"My majority colleagues do not agree with me on this point."* On the commission's own paperwork, the 91-seat idea came from the chair alone. The two opposition-nominated commissioners who signed the 89-seat majority report did not back it. (Commissioner Greg Clark, one of those two, has since said the same thing on social media.)

That changes what the April 16 motion inherited. The vehicle — a committee raising seats from 89 to 91 — traces to the chair, not the majority. A government citing "the commission's own recommendation" as cover is really citing the chair's personal note. And the chair himself said, in the note, that his own majority did not agree with him.

Chair Miller's addendum had other conditions too. The 91-seat step should use the majority map as a starting point, he said, add two rural seats, and leave the rest of the province alone. He set four rules: no changes in Airdrie or south of it; no changes north of Edmonton's river; a return of south-Edmonton districts to the earlier draft; and the restoration of a specific Clearwater / Mountain View rural district. He also wrote plainly that his goal was *"to dissuade the Legislature from accepting the minority report."* The April 16 motion borrows the 91-seat number. It does not borrow the majority map, the four rules, or the goal. It sends the redraw to an MLA committee that could put the minority's configurations back on the table.

Full close-reading: [analysis/v0_1_chair_recommendation_5_analysis.md](analysis/v0_1_chair_recommendation_5_analysis.md).

---

### April 16, and what the override took

The government took that off-ramp. On April 16 the legislature passed the motion 44 to 36. A select committee, chaired by UCP MLA Brandon Lunty, now has until November 2 to recommend a 91-seat map. An independent advisory panel sits behind the committee, but its members and terms have not been made public. Elections Alberta called the timeline "very challenging." Boundary changes are supposed to be in place at least 18 months before a general election, and the next one is in fall 2027.

NDP Leader Naheed Nenshi called it "gerrymandering — a full-on assault on our democracy." NDP MLA Rakhi Pancholi said "changing electoral boundaries to give their own party an advantage is gerrymandering." Both framings assume a map that does not yet exist.

No 91-seat map has been drafted. The motion passed on party lines. The two extra seats appear, from the Premier's rationale, to be rural rather than urban. If both added seats are rural, the rural-district population mean will drop from roughly 52,281 on the majority map to somewhere around 49,790, widening rural over-representation rather than narrowing it. The Calgary zone gap probably doesn't change much; the two added seats aren't urban.

---

### What a gerrymander in the 91-seat map would actually look like

When the committee tables its map in November, calling it a gerrymander requires evidence, not reflex. Here is what would count as a sure sign versus a weak signal.

**Strong signals (high-confidence gerrymander):**

- **The three minority signatures are preserved.** If the 91-seat map keeps Rocky Mountain House-Banff Park (or an equivalent s.15(2) district with an engineered boundary), keeps Airdrie split across four or more districts, and keeps Calgary NDP-leaning districts 10 percent or more larger than UCP-leaning ones — all three formal signatures detected in this audit carry forward into a map the committee produced. That is strong.
- **New signatures appear.** If the committee introduces packing or cracking patterns beyond what the minority had — Edmonton NDP areas packed, new urban communities cracked, more engineered rural boundaries — that is independent evidence of deliberate choice.
- **Both extra rural seats have engineered boundaries.** Two more rural seats is consistent with the Premier's stated rationale. But if both new seats are drawn with negligible-population extensions to qualify for s.15(2), that is harder to explain as policy.
- **The efficiency gap crosses the US 7 percent threshold.** Neither commission map crossed it. If the 91-seat version does, the map enters the zone American courts have used to flag unconstitutional partisan gerrymanders.
- **The map falls in the top 5 percent UCP-favourable of computer-generated legal alternatives.** This is the MCMC ensemble test described in the academic report. It requires the committee to release shapefiles and the audit to run the ensemble. If the real map is a statistical outlier against thousands of rule-following alternatives, the partisan fingerprint is hard to miss.
- **Publicly-supported configurations are dropped; unsupported ones are kept.** If the committee drops Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, and Chestermere (which have documented public support) while keeping Airdrie 4-way and Nolan Hill-Cochrane (which do not), that inversion tells a story.

**Weak signals (ambiguous, could be policy-driven):**

- Two extra rural seats on their own. That is what Smith said would happen. Not a gerrymander signal on its own.
- Calgary zone gap similar to the minority's. Could be inherited from the minority's structure rather than re-engineered.
- Keeping the Nolan Hill-Cochrane hybrid — but the usual commuter-tie defence is weaker than it looks. Statistics Canada's 2021 journey-to-work data shows 49 percent of Cochrane workers work inside Cochrane, 36 percent commute somewhere in Calgary, and the rest scatter. The Cochrane-to-Calgary commute is real. It is still a minority of workers. And the data cannot say whether the Calgary-bound workers head to Nolan Hill; it groups all of Calgary as one destination. Nolan Hill is a quiet residential area with little employment. The leap from "Cochrane commutes to Calgary" to "Cochrane belongs in the Nolan Hill district" is not supported by the data. A committee that keeps this pairing would need a different justification.

**Process signals (not about the map but still relevant):**

- Committee proceedings closed to the public.
- Advisory panel members not publicly named or their terms of reference withheld.
- Draft map not released for public comment before the legislative vote.
- Legislative adoption without amendment, without published dissent.
- AI tools used to draft the map without the prompts, seeds, and candidate ensembles published alongside the final report. The Premier's April 16 remark implied AI might be in the workflow. A committee that uses AI responsibly can document every prompt, every seed, every model version, and publish the ensemble its chosen map was picked from. A committee that can't — or won't — is borrowing legitimacy it hasn't earned.

**Things that look bad but are not sure signs:**

- The UCP wins more seats under the new map. That could be the electorate moving, not the map.
- Specific Calgary NDP ridings flip UCP. That could be 2023 voter patterns hardening, not boundary engineering.
- Rural districts smaller than urban on average. That is Alberta's natural geography.
- The map looks "weird" in places. Commission maps often look weird for legitimate reasons (river boundaries, First Nations land, protected areas).

**The honest test.** A sure-sign gerrymander in November looks like the three formal signatures surviving, plus at least one new one added, plus either the ensemble-outlier test or the documented-public-support inversion. Any one of the three alone is a concern. All three together would be hard to read as anything but deliberate.

**What the two existing maps score on this same checklist.** The audit scored the majority and minority against the checklist above, before the November map exists, as a calibration check. The majority scores zero on every signal that is testable today. The minority scores three strong signals (by definition — it is where the signatures were originally detected), two weak signals (the Calgary zone gap, the Nolan Hill-Cochrane retention), zero process signals at the commission stage, and three contradicted data-driven rationales. Neither map meets the sure-sign bar because neither crosses the US 7 percent efficiency-gap threshold and the ensemble-outlier test cannot run without 2026 shapefiles. The baseline scorecard is in [analysis/v0_1_track_c_checklist_baseline_scoring.md](analysis/v0_1_track_c_checklist_baseline_scoring.md); the November map will be scored on the same grid.

---

### The procedural question is different

That one doesn't wait. Replacing an independent boundary commission with a government-majority committee of MLAs is the thing the independent-commission model exists to prevent. Quebec's government in 1992, Ontario's in 1996, and BC's in 2008 all amended commission recommendations after the fact. None of them replaced the commission itself with a legislative committee. Whether Alberta's April 16 step is unprecedented in all Canadian history is a broader question this audit didn't fully survey. It is more government-controlled than any of the three recent comparators. And the usual "the commission itself said so" defence, as shown above, does not hold up against the commission's own documentation.

---

### Policy decision, or partisan move?

It is tempting to frame Alberta's April 16 action as either "the UCP is stacking the deck" or "the UCP is making a policy choice about rural representation the commission didn't get right." Both framings oversimplify. The evidence lets us say three specific things:

- **The process change is real.** The government moved the drafting pencil from an independent commission to a UCP-majority MLA committee. That happened on April 16. Premier Smith's stated reason — "the commission did not want to lose two rural ridings" — is a policy rationale for the 91-seat plan.
- **Three minority configurations that the chair said had no public support actually did** (Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere). Two configurations the chair flagged genuinely lacked support (Airdrie 4-way, Nolan Hill-Cochrane). A policy-driven committee could keep the three publicly-supported ones and drop the two that weren't asked for. A partisan-driven committee might do the opposite.
- **The audit cannot distinguish motive from evidence alone.** What it can do is tell you what to watch for in November. If the committee's map keeps Nolan Hill-Cochrane and the Airdrie 4-way split, that's a signal worth taking seriously. If the committee drops those two and retains only the publicly-supported configurations, the partisan-framing gets weaker.

The responsible reader position here is patience with specifics. "The UCP is stacking the deck" may be true. Saying so now, before the map exists, requires a leap the data does not make. So does "the UCP is just making good-faith policy adjustments."

---

## KICKER · 2027 AND BEYOND

**Twelve of fourteen razor-thin ridings in 2023 were in Calgary. That is where a 1-to-3 seat shift lands.**

The seat-count finding sounds small until you look at where Alberta's close races actually happened in 2023. Fourteen of the province's 87 ridings were decided by less than three points. That is nearly double the seven seats in that range in 2019. Twelve of those fourteen marginal seats are in Calgary — most of them in the same NDP-leaning zone that the minority's packing analysis flags.

Apply a 1.5 percentage point swing toward the UCP — the middle of the map-effect estimate — to the 2023 results, and six seats flip: five in Calgary, plus Banff-Kananaskis. Apply the same swing the other way and four seats flip toward the NDP.

The 2023 election wasn't close enough for a map effect of this size to change who formed government. The UCP won 49 seats to the NDP's 38 — an 11-seat gap. A 1-to-3 seat map shift is a rounding error at that spread. As of April 2026, 338Canada's aggregate projection does not show 2027 landing in close-race territory either — it shows a UCP majority around 63 seats. But Alberta polling has moved more than 10 points inside a single cycle twice in the last decade. A 14-point April 2026 gap is not locked in.

**Under what scenarios does this actually matter?**

- **Doesn't matter — 2023-style blowout.** If 2027 looks like 2023, a 1-to-3 seat map effect does not change which party forms government.
- **Matters for government type — tight race.** If an election lands within 5 seats of a tie, the 1-to-3 seat map effect is exactly the size that decides whether a party governs with a majority, a minority, or from opposition. Eight of the 14 Calgary ridings that sat inside a 3-point margin in 2023 could flip with a 1.5-point swing.
- **Matters most — close Calgary race.** Seven of the 14 marginal 2023 Calgary ridings are ones the audit's zone-gap analysis identifies as packed under the minority map. If 2027 is close and those seats decide the race, the map choice weighs directly.
- **Doesn't matter — the committee produces a different map.** The November committee could make any of this moot.

The adopted map is also in place for more than one election. If 2027 breaks the way 338Canada's April snapshot suggests, the map effect is an insurance policy rather than a live intervention. If 2031 or 2035 tightens, the same effect is waiting. That's the stake. It is not whether the minority map is an extreme gerrymander. It is whether a shift equal to the margin in Calgary-Acadia in 2023 gets baked into the next decade of Alberta maps. That shift is small. It is also, by direct inspection, in a specific direction.

---

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

The analysis uses open-source Python tooling and the commission's own public documents. The [full technical report](report_academic.md) walks every calculation, cites every submission, and lists every piece of code.

The data folder holds the commission's population tables and Elections Alberta's vote returns. The analysis folder holds the scripts. Running them on the same public files will produce the same numbers in this document. That's the point. A reader who doesn't trust one paragraph of this can run the script behind it and check.

This audit will be updated when Elections Alberta releases the digital boundary files, when the Lunty committee tables its 91-seat map, or when additional submissions become searchable. The raw data and the commits are in the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit). If you find an error, file an issue — it accepts them.

---

## Further reading

- [Full technical report with every calculation cited](report_academic.md)
- [Marginal-seats analysis and 2023 flip-zone list](analysis/v0_1_marginal_seats_findings.md)
- [Rationale-by-rationale validation of the minority report's justifications](analysis/v0_1_minority_rationales_validation.md)
- [Chair's Recommendation 5 addendum, close reading](analysis/v0_1_chair_recommendation_5_analysis.md)
- [Checklist baseline scorecard (majority and minority)](analysis/v0_1_track_c_checklist_baseline_scoring.md)
- [Plan B re-run under 2024 provincial estimates](analysis/v0_1_plan_b_cross_check.md)
- [Cycle-lag analysis under mid-2025 populations](analysis/v0_1_cycle_lag_analysis.md)
- [Proposed Act §12 amendment (legislative reform)](analysis/v0_1_act_amendment_proposal.md)
- [Calgary data-sources audit and A2 sensitivity plan](analysis/v0_1_calgary_data_sources_audit.md)
- [Source repository, data, and commit history](https://github.com/Ixby/alberta-electoral-boundaries-audit)

## Source trail

Sources and submission identifiers are cited in-line throughout. Full bibliography in the [academic report](report_academic.md). Key public sources:

- Premier Smith quote: Rimbey Review, April 16, 2026
- Chair Miller's Recommendation 5 addendum, including the text *"My majority colleagues do not agree with me on this point"*: Electoral Boundaries Commission Final Report, Addendum to Majority Report, pp. 66–67
- CBC News Edmonton, April 16, 2026 (corroborates Miller's in-text disavowal): [MLA committee to review Alberta electoral boundaries after report is set aside](https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743)
- Commissioner Greg Clark's public reinforcement of the attribution point (social-media thread, April 2026): @GregClarkAB on X, referenced in rabble.ca and albertapolitics.substack.com
- NDP responses: DiscoverAirdrie, April 17, 2026
- Seat allocation figures: Global News, March 26, 2026
- Marginal-seat analysis: Elections Alberta 2023 Statement of Vote
- Commissioner nomination details (Clark nominated by NDP Leader Nenshi): rabble.ca and albertapolitics.substack.com, April 2026
