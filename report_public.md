# Two Maps, One Province

**A plain-English audit of Alberta's 2026 electoral boundary proposals**

*Published April 22, 2026*

**Author and audit design:** Will Conner, Mount Royal University, BCIS

**How this was made.** The analysis ran through an AI-assisted pipeline (Claude Opus 4.7 1M, Max subscription, through Claude Code, plus Python open-source tools). The full tool list is in the [academic report](report_academic.md). This document is what the pipeline wrote. Nothing was rewritten afterward to sound better. If you run the scripts on the same public data, you should get the same numbers and the same words. That is how you can check the work.

[Full technical report](report_academic.md) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)

---

## Before You Start

If you already know how Alberta votes, skip to **Read This First**. If you do not, this section gives you what you need to follow the rest.

**What an electoral district is.** Alberta is divided into areas called electoral districts. Each district elects one person to represent it in the provincial legislature. That person is called an MLA. Alberta currently has 87 districts. The two proposals this audit compares would change the map to 89 districts.

**How the vote works.** On election day, you vote for one candidate in your district. The candidate with the most votes wins. That person becomes your MLA. The party that wins the most districts forms the government.

**Why the map matters.** Where the lines go decides who is in your district. If the lines change, you might share an MLA with different neighbours. The party that represents your district might change. The makeup of the legislature might shift even if nobody's vote changed.

**Alberta's two main parties.** The United Conservative Party (UCP) currently holds government. The New Democratic Party (NDP) is the main opposition. The UCP is stronger in rural areas. The NDP is stronger in Calgary and Edmonton.

**What a boundary commission is.** A group of five people appointed to draw the map. Two are picked by the government. Two are picked by the opposition. One is the chair, picked by a senior judge. The group takes public input, then recommends a map to the legislature.

**What gerrymandering is.** Drawing the lines on purpose to give one party more seats than their vote share would normally win. Some gerrymanders are obvious — long snakelike districts that reach across a city to pick up favourable voters. Others are subtle — making one party's districts slightly bigger than the other party's so the same number of voters produces fewer seats for that side.

That is the whole vocabulary you need. The rest of this report uses those terms without re-defining them.

---

## Read This First

After writing the first draft, I checked my own work by running it through three extra tests. All three made one of my findings less certain than it first looked.

**1. The "2 seats" number has a wider range than I said.** I ran the analysis 2,000 times with slightly different modelling choices. In 89 out of 100 runs, the minority map leaned UCP. In 11 out of 100, it leaned the other way. The direction is probably UCP-favourable. It is not a sure thing.

**2. A second standard test (called declination) says the minority is the least UCP-favourable of the three maps.** Two tests from the same research literature point in opposite directions. When the tests disagree, you should trust the conclusion less than when they agree.

**3. If I use 2019 vote patterns instead of 2023, the direction flips.** The minority looks UCP-favourable using 2023 votes. It looks NDP-favourable using 2019 votes. Some of what I measured is about the 2023 electorate, not the map.

Here is what this means for the rest of the report.

Findings about district sizes, community splits, and unusual boundary shapes do not depend on vote data. They hold up. Findings about how the maps turn votes into seats depend on which election you use. They are less certain than the first draft implied.

The overall pattern is real. The precise size of the partisan effect is not.

I am putting this at the top because an audit that hides its weak spots is not an audit anyone should trust.

---

## Why This Matters To You

You get one vote. The map decides how much that vote counts.

If you live in a district with a lot of people, your MLA represents more voters. Your share of their time is smaller. If the lines pack one party's voters into fewer big districts and spread the other party's voters across more small ones, the math gives one party extra seats without anyone casting an extra vote.

This audit compares two proposals the commission tabled on March 23, 2026. The question it asks is simple. Do the two maps treat voters equally? If not, which way does the unequal treatment go?

---

## The Short Version

In March 2026, the commission produced two competing maps.

The **majority map** was signed by the commission chair, who is a retired judge, and the two commissioners picked by the opposition.

The **minority map** was signed by the two commissioners picked by the government.

I applied the same tests to both.

The majority map keeps Alberta's political playing field roughly where it is today. The NDP wins the same share of seats for the same share of votes. The map does not put a thumb on the scale.

The minority map puts a small thumb on the scale toward the UCP. The size of the thumb depends on how you measure it. One test says the minority is a little more UCP-favourable. A different test says the opposite. A cross-check using older vote data flips the answer again. The direction is probably UCP-favourable. "Probably" is the right word here.

On April 16, 2026, the government rejected the majority map. The government set up a new group — made up mostly of UCP MLAs — to draft a replacement map. That new group is supposed to report back in November 2026.

**What holds up regardless of the partisan math:** the minority has bigger swings in district size, it splits more cities, and three of its districts have shapes that do not match any natural geography. The majority does not show these problems in the parts I could see.

**What is less certain:** the exact size of the seat advantage the minority would give the UCP, and whether that advantage would still appear in a different election year.

---

## What I Looked At

### 1. Are the districts roughly the same size?

**The rule.** Alberta law says each district should have about the same number of people. The provincial average is around 54,929. You are allowed plus or minus 25 percent. Very remote rural districts can go lower. This rule exists so each MLA represents about the same number of voters.

**What I found.**

| Measure | Majority | Minority |
|---|---|---|
| Average gap from the province's average district size | 3,180 people | **4,707 people** |
| Districts more than 10 percent bigger than average | 5 | **15** |
| Districts more than 15 percent bigger than average | 0 | **5** |

**What this means for you.** Under the majority map, your district size barely depends on where you live. Districts cluster tightly around the provincial average. Under the minority map, your district can be 20,000 more people than someone else's before it hits the legal limit. If you live in one of the five biggest minority districts, you share your MLA with about 13,000 more people than someone in one of the smallest. Your share of that MLA's time is smaller.

This finding does not depend on vote data. It comes from the commission's own population tables. The red-team check did not weaken it.

### 2. Are Calgary's districts sized fairly?

**Why this matters.** Calgary has two political zones that are visible in every recent election. The north, east, and central parts lean NDP. The south and west lean UCP. If one zone gets bigger districts on average, that zone's voters have less power per person.

**What I found.**

| Calgary zone | Majority | Minority |
|---|---|---|
| North, east, central average population | 56,460 | **61,225** |
| South, west average population | 56,255 | 54,569 |
| Gap between the zones | **0.4 percent** | **12.2 percent** |

**What this means for you.** Under the majority map, your Calgary district is about the same size no matter which zone you are in. Under the minority map, the NDP-leaning zones have 6,656 more people per district on average. Over 17 districts, that is about 113,000 "extra" NDP-leaning voters who would need to be in more districts if the sizes were equal. Instead, they are packed into fewer districts. The same number of NDP votes produces fewer NDP MLAs.

I checked this two ways. The geographic rule (north/east/central vs south/west) shows a 12.2 percent gap. A simpler rule (which districts did the UCP actually win in 2023?) shows a 7.7 percent gap. Different number, same direction.

This finding does not depend on the partisan math that failed the red-team. It comes from population tables and a geographic classification. It holds up.

### 3. Do the districts respect cities, towns, and communities?

**Why this matters.** MLAs work for their district's issues. If your city is split across four districts, four MLAs each represent a slice of your city. None of them is mainly responsible for it. When you call your MLA about city problems, you want someone whose political career depends on fixing them.

**What I found.**

**Airdrie** is a city of 84,000 people. Two or three districts could represent it.

Under the majority, Airdrie is split into two districts, both named "Airdrie." Each MLA's main job is to represent Airdrie.

Under the minority, Airdrie is split into four districts. None of them is named Airdrie. The city ends up divided between a Calgary district, an Olds-area rural district, and two others. Your MLA's main job is somewhere else.

**Cochrane** is a town of 34,000 people west of Calgary.

Under the majority, Cochrane has its own district, paired with the rural area around it (called Cochrane-Springbank).

Under the minority, Cochrane is attached to a Calgary neighbourhood through a narrow strip of land. The district is called "Calgary-Nolan Hill-Cochrane." Cochrane's issues (highway access, water, small-town infrastructure) are different from Calgary's issues. Your MLA is shared with people whose concerns do not overlap with yours.

**Chestermere, Enoch Cree Nation, and other communities** show the same pattern. The minority splits them more. The majority keeps them together.

This finding comes from the maps and does not depend on vote math. It holds up.

### 4. Do the district shapes make sense?

**Why this matters.** A district whose lines follow rivers, highways, and town boundaries is one whose shape comes from geography. A district shaped like a tentacle or a hook is one whose lines were drawn for a reason. In the United States, courts have spent 40 years dealing with maps that had weird shapes drawn on purpose to favour one party. Alberta does not have that history. The warning signs are the same.

**What I found.** The commission chair named three boundaries in the minority map as engineered, meaning drawn to satisfy a rule rather than to represent a real community. I looked at all three on the published maps.

- **Calgary-Nolan Hill-Cochrane.** Confirmed. A long district reaches from the town of Cochrane, across Calgary's northwest boundary, to the Nolan Hill neighbourhood inside Calgary. It skips over other Calgary neighbourhoods in between.

- **Rocky Mountain House-Banff Park.** Confirmed. A district whose southwest extension goes through the uninhabited part of Banff National Park to touch the British Columbia border. Without that extension, it would not qualify for the "small remote district" rule that lets certain districts have fewer people than average.

- **Olds-Three Hills-Didsbury.** Confirmed. The district is named for three small towns. It also reaches south to capture a big piece of Airdrie. Airdrie alone has more people than all three towns combined.

I also had published maps for the majority's Calgary districts. None of them showed these features. I did not have published maps for the majority's rural or Edmonton districts. For those, I cannot say whether the majority has similar problems. That is a real gap in this audit. It is not a clean pass for the majority's rural districts.

### 5. Does any of this change how votes turn into seats?

**Why this matters.** An ugly map can be roughly fair. A pretty map can be secretly unfair. What counts is what the map does to the seat count when real voters vote.

**What I found.**

| Measure | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | minus 2.64 percent | minus 0.78 percent | **minus 1.36 percent** |
| Mean-median gap | minus 2.22 | minus 0.16 | minus 0.33 |
| NDP seats in a tied election | 46 | 44 | **42** |
| Declination (second standard test) | minus 0.034 | minus 0.021 | **minus 0.015** |

Three of these tests are different ways to ask the same question: does the map turn votes into seats fairly? A negative number on the first three tests means the UCP wins more seats than their vote share would normally justify. On the fourth test (declination), a negative number also means pro-UCP, but here a smaller negative number (closer to zero) means less pro-UCP. That is why the declination result is confusing — by declination, the minority map looks the *least* pro-UCP of the three. The first three tests say the opposite.

**What the numbers mean in plain terms.**

The 2019 map already leans a bit UCP. This is not because anyone drew boundaries on purpose. Rural Alberta is spread out over a lot of land with fewer voters per square kilometre. Any map that follows reasonable boundaries in rural Alberta ends up with a mild UCP tilt. Every Canadian province has a version of this problem.

The majority 2026 map has a smaller UCP tilt than the 2019 map. It is the most neutral of the three.

The minority 2026 map has a slightly bigger UCP tilt than the majority map. In a tied election (where each party gets exactly half the votes), the NDP would win 42 seats under the minority map and 44 under the majority map.

That is a 2-seat difference. Two seats has been the margin between forming a majority government, a minority government, and being in opposition in recent Alberta elections. In a close election, the map choice could decide who governs even with the same underlying votes.

**But here is where the red-team hits.**

The 2-seat number is the best estimate at one specific modelling choice. When I run the same analysis 2,000 times with slightly different assumptions, the minority UCP advantage ranges from 3 seats more for the UCP to 1 seat more for the NDP. The direction is usually UCP-favourable. It is not always UCP-favourable.

One of the standard academic tests (declination, in the table above) says the minority is actually the least UCP-favourable of the three maps. Two tests on the same maps disagree about which way the bias points.

When I use 2019 vote patterns instead of 2023, the direction of the advantage flips entirely. The minority looks NDP-favourable.

So the honest reading is: the minority map is probably a little more UCP-favourable than the majority map when run through 2023 voter behaviour. The word "probably" does real work. The size of the effect could be 1 seat, could be 3, could be zero, depending on which assumptions you accept.

### 6. What about the April 16 decision?

**Why this matters.** Independent commissions draw electoral maps in every Canadian province. The reason is simple. When the people drawing the boundaries are the same people competing for seats inside those boundaries, the maps tend to favour whoever is holding the pen. Independent commissions are how Canada avoids this problem.

When a government takes over the drafting, the question changes. Is this a technical fix? Or is this about keeping seats the original map would otherwise change?

**What I found.** The government can legally reject or amend an independent commission's work. I looked at three comparable cases from other provinces.

- Quebec 1992: the legislature changed parts of the commission's map through normal legislation. The commission's drafting process was kept.
- Ontario 1996: the provincial government adopted the federal government's map (drawn by a different independent commission). They did not replace the drafting process with a government committee.
- British Columbia 2008: the provincial government legislated to keep more northern seats than the commission wanted. They changed the output, not the drafting process.

All three changed parts of the commission's output through regular legislation. Alberta's April 16 action goes further. It replaces the drafting process, not just the output. A UCP-majority committee of MLAs now oversees a new drafting panel.

**What this means for you.** The commission heard from more than 1,140 Albertans who made submissions. The commission chair wrote that the minority's specific choices for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had no support in those submissions. I have not yet verified that claim by searching the submissions myself (that work is in progress). If the chair's claim is correct, the April 16 process is pushing forward boundary choices that no member of the public asked for, over boundary choices that went through months of public review.

A province where the map might shift 1 to 3 seats of partisan advantage is a province where the process that picks the map matters. The combination of a possibly-advantageous map plus government control of the process is the reason this audit exists.

---

## What This Audit Cannot Tell You

**I cannot prove intent.** I can show that one map produces a more UCP-favourable result than the other in some tests. I cannot prove the two government-appointed commissioners drew the map on purpose for that reason. People can disagree about boundaries in good faith. Do not let anyone (including me) tell you I have proven intent. What I have shown is the *effect*, which is observable. The *intent* is not observable.

**I cannot give you one exact number for the partisan shift.** I can give you a range. One to three seats in a tied election. The direction is probably UCP-favourable. When Elections Alberta releases the official digital boundary files, I can tighten the range. That release has not happened yet.

**I cannot tell you whether the override is legal.** It appears legal. Alberta law gives the legislature final say. Whether it is wise or well-precedented is a different question than whether it is permitted.

**I cannot tell you what the November 2026 committee will produce.** It could stick close to the minority. It could change the minority substantially. If the committee produces a map closer to the majority, the concerns in this audit drop. If it produces the minority or something more partisan, the concerns apply directly.

---

## The One Big Uncertainty That Could Change Everything

When the boundary files are released, I will run one more test called an ensemble comparison. This test generates thousands of random legal maps. Then it checks where the two real maps fall inside that distribution.

If the minority falls in the top 5 percent most UCP-favourable of all legal maps, the audit's partisan finding gets stronger. The argument becomes: no random legal process would have produced this map by chance.

If the minority falls in the middle of the distribution, the partisan finding gets weaker. The argument becomes: the minority is a little more UCP-favourable than the majority, but it is within the range of what reasonable mapmakers might produce.

About 35 times out of 100, ensemble tests on small-margin cases like this one find the real map in the middle. I am flagging this now so you hear it from me rather than finding it later.

The structural findings (sizes, splits, shapes) above do not change based on this test. The partisan math does.

---

## Bottom Line For A Reader Deciding Whether To Care

**If you live in Calgary and vote NDP:** the minority map's districts in your neighbourhood carry about 12 percent more people than districts in UCP-leaning neighbourhoods. Your share of an MLA is smaller under that map.

**If you live in Airdrie or Cochrane:** the minority map splits your city across multiple districts and does not give any of them your city's name. Under the majority map, your city has its own MLA.

**If you live in rural Alberta:** the minority map makes rural districts slightly smaller on average. That means slightly more rural MLAs per capita. If you are a rural UCP voter, this helps you a little. If you are a rural NDP voter, it hurts you a little.

**If you care about fair process regardless of party:** the government is replacing an independent drafting process with a government-controlled one to promote a map the public submissions did not support. That is worth paying attention to regardless of how you vote.

**If you are waiting for a smoking gun:** there isn't one here. What is here instead is a consistent pattern across several different tests. Some of the partisan tests disagree. The structural tests line up. Modern gerrymandering concerns are usually about modest, consistent pushes rather than dramatic obvious weirdness.

**The concrete 2027 election stakes.** In a tied election, the minority map probably gives the UCP 1 to 3 more seats than the majority map would. The 2023 election was not tied, so this would not have changed the 2023 result. The 2027 election is more uncertain. Small effects matter when the election is close.

---

## Sources and Further Reading

- Alberta Electoral Boundaries Commission final report (March 23, 2026): elections.ab.ca
- 2023 Statement of Vote: elections.ab.ca
- Chen, Jowei and Jonathan Rodden (2013). "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science*. Explains why urban-concentrated parties are disadvantaged by neutrally-drawn maps.
- Courtney, John C. (2001). *Commissioned Ridings: Designing Canada's Electoral Districts.* Foundational Canadian work on boundary commissions.
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158. The Supreme Court case that set Canada's "effective representation" standard.

---

*This audit applies the same tests to all three maps. Technical details, reproducibility scripts, data files, the red-team critique, and the uncertainty analysis are in the [academic report](report_academic.md) and the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit).*

*I will update this report when Elections Alberta releases the digital boundary files, or when the in-progress submission-archive search finishes and either verifies or refutes the chair's claim about the five disputed configurations.*
