# Two Maps, One Province

**A plain-English guide to Alberta's 2026 electoral boundary debate**

*Published April 22, 2026*

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student).

**How this was made.** The analysis ran through an AI-assisted pipeline (Claude Opus 4.7 1M, Max subscription, through Claude Code, plus Python open-source tools). The full tool list is in the [academic report](report_academic.md). This document is what the pipeline wrote. Nothing was rewritten afterward to sound better. If you run the scripts on the same public data, you should get the same numbers and the same words. That is how you can check the work.

[Full technical report](report_academic.md) · [Accessible HTML version](report.html) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)

---

## What This Document Is, and Is Not

**This is:** a reproducible comparison of two proposed maps for Alberta's electoral districts, using public data. It applies the same tests to both maps. It tries to find gaps in its own reasoning before publishing. It explains, in plain language, what the numbers say and what they don't.

**This is not:**

- a proof that anyone on the boundary commission acted in bad faith
- a prediction of who will win the 2027 Alberta election
- a legal opinion on whether the April 16 government action is valid
- a complete account of every factor the commission weighed
- a final document — several pieces of data have not yet been released by Elections Alberta, and this analysis will be updated when they are

If you are looking for proof of a scandal, this document won't give you one. If you are looking for proof that nothing unusual is happening, this document won't give you that either. What it gives you is the measurable evidence, with the uncertainty spelled out honestly.

---

## What You Can Reliably Take From This

These findings come from public documents (the commission's own population tables, the published maps, official election results). They do not depend on modelling choices. If you remember nothing else, these are the parts of the audit that hold up under every check.

1. **The minority map has wider population swings between districts than the majority map.** Under the minority, you can have two districts whose populations differ by over 20,000 people before hitting the legal limit. Under the majority, the swings are about two-thirds as wide. [Details below.](#district-size)

2. **The minority map splits Airdrie across four districts. The majority splits it across two.** Airdrie is a city of 84,000 people. Four districts means no single MLA has Airdrie as their main responsibility. [Details below.](#community-splits)

3. **The minority map merges Cochrane with a Calgary neighbourhood through a narrow corridor. The majority gives Cochrane its own district.**

4. **Three minority districts have shapes that the commission chair flagged in his own report as engineered** — drawn to satisfy a rule rather than to represent a real community. The three are Calgary-Nolan Hill-Cochrane, Rocky Mountain House-Banff Park, and Olds-Three Hills-Didsbury. Direct inspection of the published maps confirms the chair's description on all three.

5. **On April 16, 2026, the government rejected the majority map and set up a new process — controlled by a UCP-majority committee of MLAs — to draft a replacement.** This happened; it is in the public record.

6. **The commission chair claimed the minority's configurations had "no public support" in the 1,340+ submissions.** This claim is partially wrong. A text search of the submissions found clear public support for three of the five disputed configurations (Rocky Mountain House-Banff Park, the Olds-Three Hills-Didsbury rural unit, and Red Deer-area hybrids). For two configurations (Airdrie 4-way split and Calgary-Nolan Hill-Cochrane), the chair's claim holds up.

Everything in this list is either a number drawn from an official document, or a visible feature on an official map, or a verifiable fact of the public record. These findings are what a careful reader should carry forward.

---

## What You Cannot Reliably Take From This

These are places where the evidence does not support a confident claim, even though the first draft of this audit was more confident than it should have been.

1. **You cannot reliably claim the minority map would reliably give the UCP a specific number of extra seats in the 2027 election.** The audit estimates a range of 1 to 3 seats in a tied election using 2023 vote patterns. Using 2019 patterns, the direction of the advantage actually *flips* and the NDP would gain seats under the minority. When a test's answer depends on which election you use, the answer is partly about the voters rather than about the map.

2. **You cannot reliably claim the minority is an intentional gerrymander.** The audit can measure effects. It cannot read the minds of the two government-appointed commissioners. The effects are real but small — below the threshold American courts have used to flag suspect maps. Intent is not demonstrated by the numbers.

3. **You cannot reliably claim the majority map is "neutral" or "fair" in an absolute sense.** The 2019 baseline map already has a mild UCP tilt that exists because rural Alberta is spread out over a lot of land. Any map that follows sensible geography in Alberta ends up with this tilt. The majority map does not remove it; it keeps it about where it was. "More neutral than the minority" is defensible. "Neutral" as a standalone claim is not.

4. **You cannot reliably claim the government's April 16 action is without precedent.** The audit looked at three recent Canadian comparator cases (Quebec 1992, Ontario 1996, BC 2008). The April 16 action is more government-controlled than any of those three. It is not necessarily without precedent across all Canadian history, which the audit did not comprehensively survey.

5. **You cannot reliably claim the minority's districts were drawn to favour the UCP.** That specific claim requires evidence of intent. What the audit shows is a pattern of effects. The pattern is consistent with deliberate partisan advantage. It is also consistent with good-faith disagreement between commissioners with different views of fair representation. The audit cannot distinguish between those two explanations.

---

## What's Floating in the Public Debate, and What the Data Supports

Several claims are being made by different sides of this debate. Here is what the audit's evidence supports, treats as plausible, and treats as unsupported.

### Demonstrable (supported by the data)

- **"The minority map has wider population swings than the majority."** Yes — the minority's mean absolute deviation from the provincial average is 48% wider than the majority's.
- **"The minority splits Airdrie more than the majority."** Yes — four districts versus two.
- **"Three minority districts have unusual shapes."** Yes — visible on the published maps. The commission chair said so himself.
- **"The government's April 16 process is run by a UCP-majority committee."** Yes — this is public record.
- **"The commission chair was wrong that the minority had no public support."** Partially — the chair was right on two configurations and wrong on three.

### Probable (directionally supported, with uncertainty)

- **"The minority map is somewhat more UCP-favourable than the majority map."** Probably. 89 out of 100 re-runs of the analysis say so. 11 out of 100 say the opposite. The exact size of the advantage is uncertain and depends on which election you use for the calculation.
- **"The minority map would cost the NDP 1 to 3 seats in a tied election."** Probably, for a 2023-style electorate. A 2019-style electorate produces different numbers.
- **"Alberta's current 2019 map has a mild UCP tilt."** Yes, about −2.6% on the efficiency gap. Most of this is natural geography, not boundary engineering.
- **"The April 16 process is more interventionist than similar actions in other provinces."** Probably, based on the three comparator cases reviewed.

### Unlikely (not supported by the data, sometimes contradicted)

- **"The minority map is an extreme gerrymander."** Not supported. It does not cross the threshold US courts have used for extreme partisan gerrymanders. The minority's efficiency-gap effect is one-fifth the size of the US-courts threshold.
- **"Neither map differs in a meaningful way."** Not supported. Six independent tests show differences. The differences are small but consistent.
- **"The majority map is partisan in favour of the NDP."** Not supported by the data. The majority map keeps the status quo partisan balance; the status quo has a mild UCP tilt.
- **"The minority had no public support for any of its configurations."** Contradicted. Three of five disputed configurations have documented public support in the submissions. The chair was correct on the Airdrie 4-way and Nolan Hill-Cochrane configurations and wrong on the others.
- **"The April 16 action is a clear constitutional violation."** Not established. It may or may not satisfy the effective-representation standard from the 1991 Saskatchewan Reference. That determination is for courts, not this audit.
- **"The April 16 committee will definitely produce a partisan map."** Speculative. The committee has not yet reported. The audit cannot evaluate a map that does not yet exist.

---

## If the 2027 Election Is Close

The audit's seat-count difference between the two maps (1 to 3 seats in a tied election) sounds abstract. Here is what it actually means if the 2027 provincial election is a close race — which several recent polls and political analysts have suggested it will be.

**What the data says about "close":**

- **In 2023**, fourteen ridings were decided by less than three percentage points of two-party margin. That is almost double the seven seats within three points in 2019 and eight in 2015. The marginal seats in 2023 are almost entirely in Calgary.
- **If the 2027 election is similar to 2023 in tightness,** a 1.5 percentage point swing (the midpoint of the audit's map-effect estimate) would flip six seats toward the UCP or four toward the NDP depending on direction.
- **If the 2027 election is within 5 seats overall** — which the "slim majority or minority government" scenario implies — then the 1 to 3 seat map effect is exactly the size that decides whether a party governs alone, governs in a minority, or is in opposition.

**The specific seats at stake in a close 2027 election** (based on 2023 margins under 3 points):

- In Calgary: Acadia, Glenmore, Foothills, Edgemont, Beddington, North West, North, Bow, and several others. These are in the audit's Zone A (NDP-leaning) packing region.
- In Edmonton: marginal seats are fewer but include some of the Edmonton-South / Edmonton-Ellerslie area.
- In rural Alberta: Banff-Kananaskis, Lethbridge-East.

**The honest caveat.** The audit cannot predict the 2027 election. The map effect is small, consistent, and in a specific direction (probably UCP-favourable). Whether it matters for which party forms government depends entirely on how close the actual vote is. If the NDP wins by 10 points, the map effect is a footnote. If the race is within 2 points, the map could decide it.

**What reasonable people can disagree about:** whether a map effect of this size should be considered a democratic concern. Some argue any systematic advantage is worth addressing regardless of size. Others argue that an advantage this small is well within the noise of normal political geography and does not warrant treating the minority map as illegitimate. The audit does not take a position on this normative question. It provides the numbers.

---

## What Is Missing From This Analysis

This audit is incomplete in specific, documented ways. A reader should know these limits before drawing conclusions.

1. **Elections Alberta has not released the digital boundary files for either 2026 proposal.** This means several standard tests from the academic literature (MCMC ensemble comparison, precise compactness scores) cannot run. When the files are released, the audit will re-run those tests, and the results could confirm, strengthen, or weaken the current findings.

2. **Approximately 88 of the 1,340 public submissions are scanned images that the audit's text search could not read.** That is about 6.6% of the total. A full OCR pass of those submissions is possible but was not done. The refutation finding (that the chair's "no public support" claim is partially wrong) rests on identified supporting submissions, so additional supporting submissions in the unread 6.6% would only strengthen that finding, not change it. Opposition counts could shift.

3. **The audit has published maps for the majority's Calgary districts but not for the majority's rural or Edmonton districts.** That means the visual-anomaly check (which flagged three minority districts) was applied to the minority's entire map but only about a quarter of the majority's. If the majority has rural or Edmonton districts with unusual shapes, the audit did not catch them.

4. **The partisan-bias numbers depend on an assumption about how rural and urban voters mix in hybrid districts.** The audit uses a 70/30 urban/rural split. Testing across 0.60, 0.70, and 0.80 shows the direction is stable but the magnitude varies. A more precise estimate requires the 2026 shapefiles.

5. **The 2015 election data is in the bundle but the 2015 map used different district boundaries than the 2019 map.** The audit could not use 2015 vote data directly in the cross-election check for that reason. A 2015→2019 boundary crosswalk was not available.

6. **The audit does not include First Nations and Métis voter-specific analysis beyond the population-criteria discussion in Section A3.** A fuller treatment of Indigenous representation under the UN Declaration and the effective-representation framework would require separate work.

---

## A Note on Scientific vs Sociological Claims

The audit is built on scientific method: hypotheses, tests, data, uncertainty bounds. It is defensible as science in the sense that the calculations are reproducible and the limits are disclosed.

It is not a sociological account. It does not claim to explain why anyone did anything. It does not attempt to characterize the motivations of the commissioners, the government, or voters. Claims about motive, intent, or political strategy that appear in this audit are explicitly marked as possibilities rather than findings.

This matters because the audit's findings are currently being used in a political debate. Both sides have an interest in stretching what the data says. The numbers here are small. The confidence is qualified. Using this document to support extreme claims in either direction — "the minority is a deliberate gerrymander" or "both maps are completely fine" — goes beyond what the analysis supports.

If you are tempted to share a specific claim from this audit, ask first: is it in the "demonstrable" list above, or the "probable" list, or the "unlikely" list? Represent it at the level of confidence the audit actually has. That is the single biggest favour you can do for the public conversation.

---

<a id="district-size"></a>
## Plain-English Walkthrough of the Findings

If you want to understand the specifics, here they are. Every number in this section comes from a public document. The underlying scripts are in the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) and can be re-run by anyone with Python installed.

### Before you start

Alberta is divided into areas called electoral districts. Each district elects one person (an MLA) to the provincial legislature. Alberta has 87 districts now. Both 2026 proposals would change the map to 89 districts.

An independent five-person commission drew both proposals. Two commissioners were picked by the government, two by the opposition, and one by a senior judge. The commission heard public input and tabled two competing maps on March 23, 2026.

### District size

Alberta law says each district should have about 54,929 people, with a range of plus or minus 25 percent allowed. Very remote rural districts can go lower.

Under the majority map, most districts cluster close to the average. Under the minority map, districts spread out more.

| Measure | Majority | Minority |
|---|---|---|
| Average distance of a district from the 54,929 average | 3,180 people | 4,707 people |
| Districts more than 10% bigger than average | 5 | 15 |
| Districts more than 15% bigger than average | 0 | 5 |

If you live in a big district, you share your MLA with more people than someone in a small district. The minority map has more big districts and more small districts; the majority map clusters closer to the average.

### Calgary zone balance

Calgary has two loose political zones. The north, east, and central parts lean more to the NDP. The south and west lean more to the UCP.

| Calgary zone | Majority average | Minority average |
|---|---|---|
| North, east, central | 56,460 people | 61,225 people |
| South, west | 56,255 people | 54,569 people |
| Gap | 0.4% | 12.2% |

Under the majority map, Calgary's political zones have about the same average district size. Under the minority map, the NDP-leaning zones are packed about 12% fuller per district. That means the same number of NDP votes in Calgary produces fewer NDP MLAs under the minority map than under the majority map.

This finding does not depend on which election or which modelling choice. It comes from the commission's own population tables.

<a id="community-splits"></a>
### Community splits

A good map tries to keep a city inside as few districts as possible. Your MLA's job is clearer when your city is their main constituency.

- **Airdrie** (84,000 people): majority splits across 2 districts, both named Airdrie. Minority splits across 4 districts, none of them named Airdrie.
- **Cochrane** (34,000 people): majority gives Cochrane its own district (Cochrane-Springbank). Minority merges Cochrane with a Calgary neighbourhood through a narrow strip of land.
- **Chestermere**: majority keeps it with its natural neighbour Strathmore. Minority partially splits it between Calgary and Chestermere-Strathmore.
- **Tsuut'ina Nation and Siksika Nation**: both maps keep these reserves intact. Both maps name districts after them. This is a point of agreement.

### Unusual district shapes

A district whose lines follow rivers, highways, and town edges has a shape that came from geography. A district shaped like a tentacle or a hook has lines drawn for some other reason.

The commission chair named three minority districts as engineered. Visual inspection of the published maps confirms his description:

- **Calgary-Nolan Hill-Cochrane.** A long district reaches from the town of Cochrane across Calgary's NW edge to the Nolan Hill neighbourhood, skipping other NW Calgary neighbourhoods in between.
- **Rocky Mountain House-Banff Park.** The district's SW extension goes through the uninhabited part of Banff National Park to reach the British Columbia border. Without that extension, it wouldn't qualify for the "small remote district" rule.
- **Olds-Three Hills-Didsbury.** The district is named for three small towns. It also reaches south to capture a big piece of Airdrie. Airdrie has more people than all three named towns combined.

For the majority map, the published Calgary districts do not show these features. The audit did not have published maps for the majority's rural or Edmonton districts. That is a real gap.

### Effect on seats

The audit calculates three standard measures of partisan fairness. Summary:

| Measure | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | −2.64% | −0.85% | −1.36% |
| Mean-median gap | −2.22 | −0.18 | −0.33 |
| NDP seats in a tied election | 46 | 44 | 42 |
| Declination (fourth test) | −0.034 | −0.021 | −0.015 |

Three of the four tests say the same thing: the minority is modestly more UCP-favourable than the majority. The fourth test (declination) says the opposite. When tests disagree, readers should reduce their confidence in the finding.

The minority's efficiency gap is about one-fifth the size of the threshold US courts have used to flag suspect maps. If Alberta used the US threshold, the minority would not be flagged. Whether Alberta would apply a different threshold is for courts.

The seat-count difference (2 seats in a tied election) is a directional finding at 89% confidence. A strict 95%-confidence interval crosses zero, which means under the full range of modelling uncertainty the minority could give the UCP between 3 extra seats and 1 fewer seat. The direction is probably UCP-favourable. The size is uncertain.

### The April 16 process

After the commission tabled both maps, the government rejected the majority map on April 16, 2026. Instead of amending it (as Quebec did in 1992, Ontario in 1996, and BC in 2008), the government replaced the drafting process with a new committee. The committee has a UCP majority and is chaired by UCP MLA Brandon Lunty. It is scheduled to report back in November 2026.

The commission heard from 1,340+ members of the public. The chair said the minority's specific configurations for five areas had no support in those submissions. An independent text search of the submissions found that three of the five actually do have public support. Two hold up. So the chair's claim was wrong on part of its scope.

The strongest procedural concern is that the new process is government-controlled. Two of the minority's configurations (Airdrie 4-way, Nolan Hill-Cochrane) have no documented public support in the submissions. Whether the November committee keeps those configurations, changes them, or proposes something else entirely is not yet known. That concern is narrower than the first draft of this audit suggested but is real — contingent on what the committee actually produces.

---

## How to Check the Work

Everything in this audit is reproducible. If you want to check a specific number, here is what to look for.

1. The underlying data (election results, populations, maps) is in the [repository's `data/` folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/data) and sourced from Elections Alberta.

2. The analysis scripts are in the [`analysis/` folder](https://github.com/Ixby/alberta-electoral-boundaries-audit/tree/master/analysis). Running `python3 analysis/v0_2_packing_cracking_analysis.py` reproduces the efficiency-gap and related numbers.

3. The academic report ([`report_academic.md`](report_academic.md)) walks through each finding with methodology and citations.

4. The self-audit of the audit's own methodology is in [`analysis/v0_1_bias_audit.md`](analysis/v0_1_bias_audit.md) and [`analysis/v0_1_design_critique.md`](analysis/v0_1_design_critique.md).

If you find an error, the repository accepts issues.

---

## Sources and Further Reading

- Alberta Electoral Boundaries Commission final report (March 23, 2026): elections.ab.ca
- 2023 Statement of Vote: elections.ab.ca
- Chen, Jowei and Jonathan Rodden (2013). "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science*. Explains why urban-concentrated parties can be disadvantaged by neutrally-drawn maps.
- Courtney, John C. (2001). *Commissioned Ridings: Designing Canada's Electoral Districts.* Foundational Canadian work on boundary commissions.
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158. The Supreme Court case that set Canada's "effective representation" standard.
- Warrington, G. S. (2018). Declination metric for partisan gerrymandering.
- Stephanopoulos, N. O. and McGhee, E. M. (2014). Efficiency gap metric.

---

*I will update this report when Elections Alberta releases the digital boundary files, or when additional submission-archive work closes remaining gaps.*
