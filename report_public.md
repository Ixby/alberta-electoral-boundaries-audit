# Two Maps, One Province

**A plain-English audit of Alberta's 2026 electoral boundary proposals — with the stakes spelled out**

*Published April 22, 2026 · Non-partisan, evidence-based*

**Author and audit design:** Will Conner, Mount Royal University, BCIS

**How this was made:** The analysis was executed by an AI-assisted pipeline (Claude Sonnet 4.6 via Claude Code, plus open-source Python scientific libraries — full tool list in the [academic report](report_academic.md)). **This document is the pipeline's unedited output.** Nothing was rewritten after generation to sound more convincing or less alarming; if you re-run the scripts against the same public data, the numbers and language should match. That's by design — it's how you check someone's work.

*[Full technical report](report_academic.md) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)*

---

## Why This Matters To You

Alberta is redrawing the lines that decide which voters elect which MLAs. You get one vote; the map decides how much that vote is worth. If you live inside a district with a lot of people, your MLA represents more voters and each voter gets a smaller piece of their attention. If the lines are drawn so that one party's voters are packed into fewer, larger districts while the other party's voters are spread across more, smaller ones, the math hands one party extra seats without one extra vote being cast.

This audit compares two competing proposals the independent boundary commission tabled on March 23, 2026. We asked: **do the two maps treat voters equally, and if not, which way does the unequal treatment go?** The answer has practical consequences for anyone who votes in Alberta.

---

## The Short Version

In March 2026, an independent five-person commission tabled two competing recommendations:

- **The majority recommendation**, signed by the commission chair (a retired judge) and the two commissioners nominated by the opposition.
- **The minority recommendation**, signed by the two commissioners appointed by the governing party.

We applied the same tests to both. **The majority keeps Alberta's political playing field roughly where it sits today.** Same vote share, same seat share — no thumb on the scale.

**The minority tilts the playing field toward the UCP by a measurable amount.** Not enormously — this isn't a flagrant US-style gerrymander. But consistently, across six separate tests, in the same direction, using methods the same commission applied to the same data.

**Then on April 16, 2026, the government rejected the more neutral option and built a new process to work from the tilted one.** The government can do that legally. This audit is about whether that choice has consequences voters should know about before the election in fall 2027.

**The practical stakes:** under the minority map's methodology, in a tied election, the NDP wins 2 fewer seats and the UCP wins 2 more, compared to the majority map. That's 2 seats won by a thumb on the scale, not by winning more votes. In a close provincial election, 2 seats can decide whether a party governs with a majority, a minority, or from opposition.

---

## What We Looked At, and Why Each One Matters

### 1. Are the districts roughly the same size?

**The rule, in plain terms:** Alberta law says each district should have about the same number of people (currently ~54,929), so each MLA represents roughly the same number of voters. You're allowed ±25%, with exceptions for very remote areas. This rule exists because if one district has 70,000 people and another has 45,000, the 45,000-person district's voters have more say per person.

**What we found:**

| | Majority | Minority |
|---|---|---|
| Average distance from the province's average district size | 3,180 people | **4,707 people** |
| Districts more than 10% larger than average | 5 | **15** |
| Districts more than 15% larger than average | 0 | **5** |

**So what?** Under the majority map, the size of your district barely depends on where you live — districts cluster tightly around the provincial average. Under the minority map, your district can be 20,000+ people bigger than someone else's before it hits the legal limit. **If you live in one of the minority's 5 biggest districts, you share your MLA with about 13,000 more people than someone in one of the smallest.** Your share of your MLA's attention, office time, and vote in the legislature is proportionally smaller. That's the population-equality consequence.

### 2. Are Calgary's districts sized fairly across the city?

**Why this matters:** Calgary has two broadly recognizable political zones. The north, east, and central areas lean more to the NDP. The south and west lean more to the UCP. If a map systematically makes one zone's districts bigger, that zone's voters have less power per person — and in a general election, their party gets fewer seats for the same share of votes.

**What we found:**

| Calgary zone | Majority proposal | Minority proposal |
|---|---|---|
| North/east/central average population | 56,460 | **61,225** |
| South/west average population | 56,255 | 54,569 |
| Gap | **0.4%** (essentially none) | **12.2%** (big) |

**So what?** Under the majority proposal, if you live in Calgary, it doesn't matter which zone you're in — your district has about the same number of people as any other Calgary district. Under the minority proposal, **NDP-leaning zone residents share their MLA with 6,656 more people per district than UCP-leaning zone residents.** Over 17 such districts, that's roughly 113,000 "extra" NDP-leaning voters who would need to be represented in more districts if the sizes were equal. Instead, they're packed into existing districts, meaning NDP-leaning Calgary gets the same number of seats representing more voters.

The practical effect: for the same number of NDP votes cast, the minority map produces fewer NDP seats than the majority map would. **That's how map lines turn into legislature seats without a single vote changing.**

We tested this using a simpler, different rule too (which districts did the UCP actually win in 2023?) — different number, same direction: the minority produces a 7.7% gap, the majority still essentially zero.

### 3. Do the districts respect cities, towns, and communities?

**Why this matters:** MLAs work for a district's issues. If your city is split across four different districts, four different MLAs each represent a slice of your city — none of them fully responsible for it. A city of 84,000 deserves a representative focused on its housing, roads, schools, and infrastructure, not four representatives each juggling a quarter of your city alongside other places. When you call your MLA about a city problem, you want someone whose political career depends on fixing it.

**What we found:**

**Airdrie** (population 84,000):
- **Majority:** Two districts, both named "Airdrie." One MLA splits the city with a colleague; both are accountable to Airdrie residents as their primary constituency.
- **Minority:** Four districts, *none* named Airdrie. Your MLA's main constituency is a Calgary neighborhood, an Olds-area rural riding, or something else — Airdrie is a secondary consideration.

**So what?** If you live in Airdrie under the minority map, your voice on city issues gets split four ways, and no MLA's political survival depends on serving you specifically. Under the majority map, two MLAs make Airdrie their core constituency.

**Cochrane** (population 34,000):
- **Majority:** Its own district, paired with the natural rural area around it (Cochrane-Springbank).
- **Minority:** Folded into a Calgary district ("Calgary-Nolan Hill-Cochrane") via a narrow strip of land reaching through Calgary's northwest suburbs.

**So what?** Cochrane's issues — highway access to Calgary, water, the Bow River, small-town infrastructure — are different from Calgary's issues. Under the minority map, a Cochrane voter shares an MLA with a Calgary neighborhood whose concerns don't overlap with theirs. Under the majority map, Cochrane gets an MLA whose constituency is Cochrane and the rural area around it — same kind of community, same issues.

**Chestermere, Enoch Cree Nation, and others** show the same pattern: minority splits communities that the majority keeps intact. The consequence is the same — fragmented political voice for communities that fit comfortably in one district.

### 4. Do the district shapes make geographic sense?

**Why this matters:** A district whose boundaries follow rivers, highways, and municipal lines is one whose shape emerged from geography. A district shaped like a lasso or a tentacle is one whose boundaries were drawn for a reason — often a reason that doesn't serve the people inside the shape. The US Supreme Court has spent 40 years dealing with maps that were drawn in weird shapes to guarantee specific election results; Alberta doesn't have that history, but the warning signs are the same.

**What we found:** The commission chair himself flagged three specific boundaries in the minority proposal as *engineered* — shapes drawn to meet a legal requirement rather than representing a natural community. We examined all three on the published maps:

- **Calgary-Nolan Hill-Cochrane.** Confirmed. A long, narrow-waisted district that reaches from Cochrane across Calgary's northwest boundary to the Nolan Hill neighborhood, skipping Calgary's other northwestern neighborhoods in between.

  **So what?** A district shaped like this doesn't represent a community — it represents a boundary decision. When the shape is this unnatural, voters inside it end up being a collection of people who happen to be on the same side of a line, not a community with shared needs their MLA would fight for.

- **Rocky Mountain House-Banff Park.** Confirmed. A district whose southwest extension traces the uninhabited portion of Banff National Park to reach the British Columbia border.

  **So what?** Alberta's law lets remote rural districts have fewer people if they're big, far from cities, have Indigenous reserves, and touch another province. Rocky Mountain House-Banff Park only meets the "big" and "touches BC" requirements because of the extension through the national park — uninhabited land, added to the boundary specifically so the district qualifies for smaller-than-average population. Without the park addition, it wouldn't qualify, and would have to be drawn bigger, probably reducing the number of rural-weighted seats in the map by one. **The practical effect is that this boundary creates an extra rural seat that wouldn't otherwise exist under the same legal framework.**

- **Olds-Three Hills-Didsbury.** Confirmed. The district is named for three small towns north of Calgary but reaches south to capture a slice of Airdrie — a city bigger than all three named towns combined.

  **So what?** If you live in the "Olds-Three Hills-Didsbury" portion that's actually in Airdrie, your MLA is elected primarily by voters in small towns 50+ km away, with different issues and different economic bases. The name tells you who the district represents; the map tells you that's not who actually lives in a big chunk of it.

**The majority proposal's Calgary districts** — the only majority districts we had published maps for — show none of these features. We don't have published maps for the majority's rural and Edmonton districts, so our answer for those is "we don't know yet." **That's an honest gap in the audit, not a clean bill of health for the majority's rural districts.** Shapefiles, when released, will close this gap.

### 5. Does any of this actually change how votes turn into seats?

**Why this matters:** You can draw an ugly map, and it can turn out to be roughly fair by accident. You can draw a pretty map that's secretly unfair. What counts is what the map actually does to the seat count when real voters vote. Three standard measures tell you whether a map gives one party extra seats beyond their share of votes.

**What we found:**

| Measure | 2019 map (current) | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | −2.64% (slight UCP edge) | −0.78% | **−1.36%** |
| Mean-median gap | −2.22 percentage points | −0.16 pp | −0.33 pp |
| NDP seats in a 50/50 tied election | 46 | 44 | **42** |

**So what, in plain terms:**

- **The 2019 map already has a slight built-in UCP advantage.** In a tied election, the UCP wins a few more seats than the NDP — not because of boundary engineering, but because rural Alberta is geographically spread out. Every Canadian province deals with this.

- **The majority map gives the UCP a smaller built-in advantage than the 2019 map.** It's the most neutral of the three.

- **The minority map restores part of the 2019 UCP advantage and adds a bit more.** In a 50/50 tied election, the NDP wins 42 seats under the minority map vs 44 under the majority map. **That's 2 seats won by how the lines are drawn, not by winning more votes.**

In Alberta's last few elections, 2 seats has been the margin between a majority government, a minority government, and the opposition. The 2023 election went UCP 49, NDP 38 — a solid UCP majority. If the next election is closer (and the political environment in 2027 is genuinely uncertain), **the map choice could be the difference between the NDP forming government and the UCP forming government with the same underlying voter sentiment.**

We tested how sensitive these numbers are to modeling choices we had to make (official boundary shapefiles haven't been released; hybrid districts require estimating how rural and urban voters mix). The direction — minority more UCP-favorable than majority — holds under every variant we tested. The exact magnitude ranges from 0.6 to 1.6 percentage points depending on assumption, and from 1 to 3 seats depending on how tied the election is.

None of these numbers cross the threshold US courts have used to flag suspect maps (7% efficiency gap). **This isn't a smoking-gun gerrymander. It's a finger on the scale, not a thumb.** But a finger, consistently, in the same direction.

### 6. What about the April 16 decision?

**Why this matters:** Independent commissions exist because when the people drawing the boundaries are also the people competing for seats in them, the maps tend to benefit whoever's holding the pen. Every Canadian province uses independent commissions for this reason. When a government overrides an independent commission's work, the question becomes: is this a technical amendment to improve representation, or is it about gaining advantage?

**What we found:** The government can legally reject or amend an independent commission's recommendations. We looked at three recent comparable cases:

- Quebec 1992: the legislature tweaked specific commission recommendations.
- Ontario 1996: Queen's Park reduced seat count by adopting federal boundaries (another independent commission's work).
- BC 2008: Victoria legislated to keep more northern seats than their commission recommended.

**All three overrode a specific part of their commission's work.** Alberta's April 16 action — forming a UCP-majority MLA committee chaired by Brandon Lunty to oversee a new advisory panel — goes further. It replaces the drafting process, not just the output.

**So what?** The commission heard from 1,140+ Albertans who made submissions about how the new map should be drawn. The commission chair's own report says the minority's specific configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert **had no public support in those 1,140+ submissions.** If that claim is correct — and we haven't independently verified it, it's from the majority report's Appendix C — the April 16 process is using government control to promote the boundary choices *no one asked for* over the boundary choices everyone got to comment on.

**The practical effect:** in a province where the map determines ~2 seats' worth of partisan advantage, the process that picks the map is now controlled by the party that benefits from the more advantageous option. Even if the advantage is small, the combination — more advantageous map + process control to pick it — is what makes this worth paying attention to.

---

## What This Audit Cannot Tell You (And Why That Matters)

Honest limits, spelled out:

- **We cannot prove intent.** We can show that one map produces a more UCP-favorable result than the other, that the more-favorable one uses configurations no one asked for publicly, and that the process being used to promote it is government-controlled. We can't prove the two government-appointed commissioners drew the map intending this result. Good-faith disagreement with the chair is an alternate explanation. Don't let anyone (including us) tell you we've proven intent. What we've shown is the *effect*, which is observable; the *intent* is not.

- **We cannot give you a single precise number for the partisan shift.** We can give you a range (0.6 to 1.6 percentage points, 1 to 3 seats). The range is honest uncertainty about modeling choices, not a hedge. When the province releases the official digital boundary files — standard after a map is finalized — we can collapse this to a single number. That hasn't happened yet. What we can tell you: the range's *direction* is rock-solid; the exact value within the range will be determined when the data arrives.

- **We cannot tell you whether the override is legal.** It appears to be. The statute gives the legislature final say. Whether it's wise, fair, or well-precedented is a different question than whether it's permitted.

- **We cannot tell you how the final November 2026 MLA-committee map will differ from the commission's minority.** The committee could stick close to the minority, or could modify it substantially. Our audit is of the two commission proposals as they stand — not of what the committee will produce. **If the committee produces a map materially closer to the majority, the substantive concern in this audit diminishes proportionally.** If it produces the minority or something more partisan, the concerns in this audit apply directly.

---

## The One Big Uncertainty That Could Change Everything

When the boundary files are released, we'll run an additional test called an **ensemble comparison.** This generates thousands of alternative maps that follow all the same legal rules, then checks where the real maps fall within that computer-generated distribution.

**If the minority map turns out to be an extreme outlier** (in the top 5% most UCP-favorable of all legally-allowed maps), the audit's finding strengthens substantially. The interpretation becomes: *the commissioners drew a map no random, legal process would likely produce — that's evidence of intent.*

**If the minority map turns out to be a normal-ish map** (somewhere in the middle of the distribution), the audit's finding softens. The interpretation becomes: *the minority is directionally more UCP-favorable than the majority, but well within the range of what any reasonable map-drawer could end up with.* The direction of the advantage is still real; the "intentional partisan choice" framing weakens.

**We think there's about a 35% chance the outlier-test shows the minority is *not* extreme.** We're flagging this so you hear it from us first rather than discovering later that the audit's framing got revised. If you share this audit, **share the fact that this additional test is coming, and its result could change the interpretation.**

What it won't change: the population asymmetry, the community splits, the visible boundary shapes, the procedural concern about the April 16 action. Those stand regardless.

---

## Bottom Line, For A Reader Deciding Whether To Care

1. **If you live in Calgary and vote NDP:** the minority map's districts in your neighborhood carry about 12% more people than districts in UCP-leaning neighborhoods. Your share of an MLA is proportionally smaller under that map.

2. **If you live in Airdrie or Cochrane:** the minority map splits your city up among four or five districts without giving any of them your city's name. Under the majority map, your city has its own MLA.

3. **If you live in rural Alberta:** the minority map gives rural districts slightly smaller populations on average, which means slightly more rural MLAs per capita. If you're a rural UCP voter, this map slightly benefits you. If you're a rural NDP voter (there are some, especially in Peace Country and near Indigenous communities), it slightly disadvantages you.

4. **If you care about fair process regardless of party:** the government is replacing the independent drafting process with a government-controlled one in order to promote the option the commission's public submissions didn't support. That's worth paying attention to whether you vote NDP, UCP, or neither.

5. **If you're waiting for a smoking gun before caring:** there isn't one here. What there is instead is a consistent, modest-sized effect across six separate tests. Multiple small pushes in the same direction is the 2020s gerrymandering playbook; 1990s-style obvious weirdness is rare now. The test that matters is whether the effect is reproducible across multiple independent measurements. It is.

6. **The concrete 2027 election stakes:** in a tied election, the minority map gives the UCP 2 seats the majority map wouldn't. In the 2023 election — UCP 49 / NDP 38 — that would not have flipped the result. In a tight election (say, 46-45), it could be the difference between governments.

---

*This audit applies identical forensic methodology symmetrically to all three maps. Full section-by-section technical writeups, reproducibility scripts, data files, and a self-audit of our own methodology are available in the [academic/legal report](report_academic.md) and in the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit).*

*We will update the public finding if and when Elections Alberta releases digital boundary files, or if the commission's 1,140+ public submissions, independently searched, refute the claim that the five disputed minority configurations had no public support.*
