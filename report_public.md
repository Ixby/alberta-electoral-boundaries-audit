# Two Maps, One Province

**A plain-English audit of Alberta's 2026 electoral boundary proposals**

*Published April 22, 2026*

**Author and audit design:** Will Conner, Mount Royal University, BCIS

**How this was made.** The analysis ran through an AI-assisted pipeline (Claude Sonnet 4.6 through Claude Code, plus Python open-source tools). The full tool list is in the [academic report](report_academic.md). This document is what the pipeline wrote. Nothing was rewritten afterward to sound better. If you run the scripts on the same public data, you should get the same numbers and the same words. That lets you check the work.

[Full technical report](report_academic.md) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)

---

## Read This First

After writing the first draft, I red-teamed my own work. Three tests made the partisan-math claim weaker than it first looked.

**1. The "2 seats" number has a wider range than I said.** I ran the analysis 2,000 times with slightly different modeling choices. In 89 out of 100 runs, the minority map leaned UCP. In 11 out of 100, it leaned the other way. So the direction is probably UCP-favorable, but it is not a sure thing.

**2. A second standard test (called declination) says the minority is the least UCP-favorable of the three maps.** Two tests from the same research literature point in opposite directions. When the tests disagree, readers should trust the conclusion less.

**3. If I use 2019 vote patterns instead of 2023, the direction flips.** The minority looks UCP-favorable using 2023 votes. It looks NDP-favorable using 2019 votes. That means some of what I measured is about the 2023 electorate, not the map.

Here is what this means for how you should read the rest.

The findings about district sizes, community splits, and weird boundary shapes do not depend on vote data. Those findings hold up. The findings about how the maps turn votes into seats depend on which election you use. Those findings are less certain than the first draft implied.

The overall pattern is real. The precise size of the partisan effect is not.

I am putting this at the top because an audit that hides its weak spots is not an audit anyone should trust.

---

## Why This Matters To You

Alberta is redrawing the lines that decide which voters elect which MLAs. You get one vote. The map decides how much that vote counts.

If you live in a district with a lot of people, your MLA represents more voters. Each person gets a smaller share of their attention. If the lines pack one party's voters into fewer big districts and spread the other party's voters across more small ones, the math gives one party extra seats without anyone casting an extra vote.

This audit compares two proposals the independent boundary commission tabled on March 23, 2026. The question it asks is simple. Do the two maps treat voters equally? If not, which way does the unequal treatment go?

---

## The Short Version

In March 2026, an independent five-person commission tabled two competing recommendations.

The **majority recommendation** was signed by the commission chair, who is a retired judge, and the two commissioners nominated by the opposition.

The **minority recommendation** was signed by the two commissioners appointed by the governing party.

I applied the same tests to both.

The majority keeps Alberta's political playing field roughly where it is today. The NDP wins the same share of seats for the same share of votes. The map does not put a thumb on the scale.

The minority puts a small thumb on the scale toward the UCP. The size of the thumb depends on how you measure it. One measure (efficiency gap) says the minority is a little more UCP-favorable. A second measure (declination) says the opposite. A cross-check with older election data flips the answer again. The direction is probably UCP-favorable. "Probably" is the right word.

On April 16, 2026, the government rejected the majority and set up a new process run by a UCP-majority committee of MLAs. That committee is supposed to report back in November 2026.

**What holds up regardless of the partisan math:** the minority has bigger swings in district size, it splits more communities, and three of its districts have shapes that do not match any natural geography. The majority does not show any of these problems in the parts we could see.

**What is less certain:** the exact size of the seat advantage the minority gives the UCP, and whether that advantage would still appear in a different election year.

---

## What I Looked At

### 1. Are the districts roughly the same size?

**The rule.** Alberta law says each district should have about the same number of people, around 54,929. You are allowed plus or minus 25 percent, with a few exceptions for remote rural areas. The rule is there so each MLA represents about the same number of voters.

**What I found.**

| | Majority | Minority |
|---|---|---|
| Average gap from the province's average district size | 3,180 people | **4,707 people** |
| Districts more than 10 percent bigger than average | 5 | **15** |
| Districts more than 15 percent bigger than average | 0 | **5** |

**What this means for you.** Under the majority map, your district size does not depend much on where you live. Under the minority map, your district can be 20,000 more people than someone else's before the legal limit kicks in. If you live in one of the five biggest minority districts, you share your MLA with about 13,000 more people than someone in one of the smallest. Your share of that MLA's time is smaller.

This finding does not depend on vote data. It comes straight from the commission's own population tables. A red-team does not weaken it.

### 2. Are Calgary's districts sized fairly?

**Why this matters.** Calgary has two political zones. The north, east, and central parts lean NDP. The south and west lean UCP. If one zone gets bigger districts on average, that zone's voters have less power per person.

**What I found.**

| Calgary zone | Majority | Minority |
|---|---|---|
| North, east, central average population | 56,460 | **61,225** |
| South, west average population | 56,255 | 54,569 |
| Gap | **0.4 percent** | **12.2 percent** |

**What this means for you.** Under the majority map, your Calgary district is about the same size no matter which zone you are in. Under the minority map, the NDP-leaning zones have 6,656 more people per district on average. Over 17 districts, that is about 113,000 "extra" NDP-leaning voters who would need to be in more districts if the sizes were equal. Instead, they are packed into fewer districts. The same number of NDP votes produces fewer NDP MLAs.

I checked this two ways. The geographic rule (north/east/central vs south/west) produces a 12.2 percent gap. A simpler rule (which districts did the UCP actually win in 2023?) produces a 7.7 percent gap. Different number, same direction.

This finding does not depend on the partisan math that failed the red-team. It comes from the population tables and a geographic classification. It holds up.

### 3. Do the districts respect cities, towns, and communities?

**Why this matters.** MLAs work for their district's issues. If your city is split across four districts, four MLAs each represent a slice of your city. None of them is mainly responsible for it. When you call your MLA about city problems, you want someone whose political career depends on fixing them.

**What I found.**

**Airdrie** has 84,000 people. Two or three districts could handle it.

Under the majority, Airdrie is split into two districts, both named "Airdrie."

Under the minority, Airdrie is split into four districts, none of them named Airdrie. The city ends up in a Calgary district, an Olds-area rural district, and two others. Your MLA's main constituency is somewhere else.

**Cochrane** has 34,000 people.

Under the majority, Cochrane gets its own district, Cochrane-Springbank.

Under the minority, Cochrane is attached to a Calgary neighborhood through a narrow strip of land. The district name is "Calgary-Nolan Hill-Cochrane." Cochrane's issues are not Calgary's issues, but Cochrane voters end up sharing an MLA with Calgarians.

**Chestermere, Enoch Cree Nation, and others** show the same pattern. The minority splits them more. The majority keeps them together.

This finding comes from the maps and does not depend on vote math. It holds up.

### 4. Do the district shapes make sense?

**Why this matters.** A district whose lines follow rivers, highways, and town boundaries is one whose shape came from geography. A district shaped like a tentacle is one whose lines were drawn for a reason. The US Supreme Court has spent 40 years dealing with maps that had weird shapes drawn on purpose. Alberta does not have that history. The warning signs are the same.

**What I found.** The commission chair named three boundaries in the minority proposal as engineered, meaning drawn to meet a rule rather than to represent a real community. I looked at all three on the published maps.

- **Calgary-Nolan Hill-Cochrane.** Confirmed. A long district that reaches from the town of Cochrane across Calgary's northwest edge to the Nolan Hill neighborhood. It skips over other Calgary neighborhoods in between.

- **Rocky Mountain House-Banff Park.** Confirmed. A district whose southwest extension goes through the empty part of Banff National Park to touch the BC border. Without that extension, it would not qualify for the "small remote district" rule.

- **Olds-Three Hills-Didsbury.** Confirmed. The district is named for three small towns. It also reaches down into a big piece of Airdrie, a city bigger than all three towns combined.

I also had published maps for the majority's Calgary districts. None of them showed these features. I did not have published maps for the majority's rural or Edmonton districts. For those, I cannot say whether the majority has similar problems. That is a real gap in the audit, not a clean pass for the majority.

### 5. Does this change how votes turn into seats?

**Why this matters.** An ugly map can be roughly fair. A pretty map can be secretly unfair. What matters is what the map does to the seat count when real voters vote.

**What I found.**

| Measure | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | −2.64 percent | −0.78 percent | **−1.36 percent** |
| Mean-median gap | −2.22 | −0.16 | −0.33 |
| NDP seats in a tied election | 46 | 44 | **42** |
| Declination (second standard test) | −0.034 | −0.021 | **−0.015** |

**What the numbers mean in plain terms.**

The 2019 map already leans a bit UCP. Rural Alberta has fewer voters spread across more area, so the math tilts a little even without anyone drawing boundaries on purpose.

The majority map has a smaller UCP tilt than the 2019 map. It is the most neutral of the three.

The minority map has a slightly bigger UCP tilt than the majority map. In a tied election, the NDP would win 42 seats under the minority map and 44 under the majority map.

That is a 2-seat difference. Two seats has been the margin between a majority government, a minority government, and opposition in some recent Alberta elections. In a close election, the map choice could decide who governs with the same underlying votes.

**But here is where the red-team hits.**

The 2-seat number is the best estimate at a specific modeling assumption. When I run the same analysis 2,000 times with slightly different modeling choices, the minority-UCP advantage ranges from −3 seats to +1 seat. The direction is usually UCP-favorable, but not always.

One of the standard academic tests (declination, shown in the table above) says the minority is actually the least UCP-favorable of the three maps. Two research-standard tests on the same maps disagree about which way the bias points.

When I use 2019 vote patterns instead of 2023, the direction of the advantage flips entirely. The minority looks NDP-favorable.

So the honest reading is: the minority map is probably a little more UCP-favorable than the majority map when run through 2023 voter behavior. The word "probably" does real work here. The size of the effect could be 1 seat, could be 3, could be zero, depending on what assumptions you accept.

### 6. What about the April 16 decision?

**Why this matters.** Independent commissions draw maps because when the people drawing boundaries are also competing for seats, the maps tend to favor whoever is holding the pen. Every Canadian province uses an independent commission for this reason. When a government takes over, the question is: is this a technical fix, or is this about keeping seats the map would otherwise change?

**What I found.** The government can legally reject or amend a commission's work. I looked at three similar cases.

- Quebec 1992: the legislature made small changes.
- Ontario 1996: Queen's Park reduced the seat count.
- BC 2008: Victoria kept more northern seats than the commission wanted.

All three changed parts of the commission's output. Alberta's April 16 action goes further. It replaces the process, not just the output. A UCP-majority committee of MLAs now oversees drafting a new map.

**What this means for you.** The commission heard from more than 1,140 Albertans who made submissions. The commission chair wrote that the minority's specific choices for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had no support in those submissions. I have not verified that claim independently. If it is correct, the April 16 process is now being used to push boundary choices no one asked for, over the boundary choices that went through public review.

A province where the map could shift 1 to 3 seats of partisan advantage is a province where the process that picks the map matters. The combination of a possibly-advantageous map plus government control of the process is the reason this audit exists.

---

## What This Audit Cannot Tell You

**I cannot prove intent.** I can show that one map produces a more UCP-favorable result than the other in some tests. I cannot prove the two government-appointed commissioners drew the map on purpose for that reason. People can disagree about boundaries in good faith.

**I cannot give you one exact number for the partisan shift.** I can give you a range of 1 to 3 seats in a tied election, with the direction probably UCP-favorable. When the province releases the official digital boundary files, I can tighten the range. That release has not happened yet.

**I cannot tell you whether the override is legal.** It looks legal. The law gives the legislature final say. Whether it is wise or well-precedented is a different question.

**I cannot tell you what the November 2026 committee will produce.** It could stick close to the minority, or change it a lot. If the committee produces a map closer to the majority, the concerns in this audit drop. If it produces the minority or something more partisan, the concerns apply.

---

## The One Big Uncertainty That Could Change Everything

When the boundary files are released, I will run one more test called an ensemble comparison. This generates thousands of random legal maps, then checks where the two real maps fall in that distribution.

If the minority falls in the top 5 percent most UCP-favorable of all legal maps, the audit's partisan finding gets stronger. The argument becomes: no random legal process would have produced this map by chance.

If the minority falls in the middle of the distribution, the partisan finding gets weaker. The argument becomes: the minority is a little more UCP-favorable than the majority, but it is within the range of what reasonable mapmakers might produce.

About 35 out of 100 times, ensemble tests on small-margin cases like this one find the real map in the middle. I am flagging this now so readers hear about it from me rather than finding it later.

The structural findings above do not change based on this test. The partisan math does.

---

## Bottom Line

**If you live in Calgary and vote NDP:** the minority map's districts in your neighborhood carry about 12 percent more people than districts in UCP-leaning neighborhoods. Your share of an MLA is smaller under that map.

**If you live in Airdrie or Cochrane:** the minority map splits your city across multiple districts and does not give any of them your city's name. Under the majority map, your city has its own MLA.

**If you live in rural Alberta:** the minority map makes rural districts a bit smaller on average, which means a bit more rural MLAs per capita. If you are a rural UCP voter, this helps you a little. If you are a rural NDP voter, it hurts you a little.

**If you care about fair process:** the government is replacing an independent drafting process with a government-controlled one to promote an option the public submissions did not support. That is worth paying attention to regardless of how you vote.

**If you are waiting for a smoking gun:** there isn't one. What there is instead is a consistent pattern across several different tests. Some of the partisan tests disagree. The structural tests line up. Modern redistricting concerns are usually about modest, consistent pushes rather than dramatic obvious weirdness.

**If you want the concrete 2027 election stakes:** in a tied election, the minority map probably gives the UCP 1 to 3 more seats than the majority map would. The 2023 election was not tied, so this would not have changed the result. The 2027 election is more uncertain. Small effects matter when the election is close.

---

*This audit applies the same tests to all three maps. Full technical details, reproducibility scripts, the data files, the red-team critique, and the uncertainty analysis are in the [academic report](report_academic.md) and the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit).*

*I will update this report when Elections Alberta releases the digital boundary files, or if the commission's public submissions, searched independently, turn up evidence that refutes the chair's claim about the five disputed configurations.*
