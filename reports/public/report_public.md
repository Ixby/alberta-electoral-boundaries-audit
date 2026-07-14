<!--
© Will Conner 2026 | CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
Data: Elections Alberta (public domain) | https://ixby.github.io
-->
> **Backward:**
> - `reports/academic/report_academic.md` — full technical monograph this report condenses
> - `findings/population_equality.md` — population MAD numbers cited
> - `findings/partisan_bias_summary.md` — partisan-metric numbers cited
> - `findings/airdrie_overlap_report.md` — Airdrie split narrative
> - `findings/joint_outlier_score_summary.md` — Mahalanobis joint outlier
> - `findings/checklist_baseline_scoring.md` — gerrymander checklist source
> - `analysis/methodology/threshold_provenance.md` — threshold context
>
> **Forward:**
> - `README.md` — links to this as the public-audience report
> - `docs/FINDINGS_BRIEF.md` — even shorter brief derived from same findings
> - (leaf otherwise — general-audience report, public-facing)

# Two Maps, Then None: Inside Alberta's 2026 Boundary Audit

*A plain-language look at the 2025–26 Electoral Boundary Commission, the math behind the minority map, and what comes next.*

## How to read this report

You came here looking for a smoking gun. This report does not have one. It cannot have one — and the reason it cannot is the most important thing the audit found.

Alberta's 2025–26 Electoral Boundaries Commission finished its work on March 23, 2026 and could not agree. Three commissioners signed one map. The other two — the two the government nominated — signed a different one. Both maps are legal under the *Electoral Boundaries Commission Act*. Three weeks later, on April 16, the Legislative Assembly set both maps aside and handed the drawing to a committee of five MLAs, three of them from the governing United Conservative Party (UCP), chaired by a UCP member. That committee's map is due November 2, 2026.

This audit measured both commission maps, and the process around them, every way it knew how: five pre-registered structural tests, four partisan-fairness metrics scored against 1,010,000 computer-simulated neutral maps, independent checks of the commissioners' published reasoning, and a review of the process against sixty years of Canadian practice. What it found is not a gun. It is **casings**: fourteen pieces of evidence, each one real, each one measured, each of which would count for something in a courtroom somewhere — and none of which, alone or together, can legally prove the conclusion they invite. A casing on the ground proves a gun existed and was fired. It cannot prove whose hand was on it. That gap between evidence and proof is not a loophole the audit failed to close. In Canada, it is the system as written — and that, too, is a finding.

So this report is built like an evidence log. Each casing gets the same five questions, in the same order, every time:

- **What we found** — the evidence, with its number.
- **What it could show** — the conclusion you will be tempted to draw, stated at full strength.
- **What the experts say** — how this kind of evidence is treated in places that do fight about it in court.
- **What Canadian practice expects** — the norm.
- **Why it isn't a smoking gun** — the specific reason, under Canadian law, this evidence proves less than it seems to.

Each of the five legal reasons is different. By the fourteenth casing you will have learned, one piece at a time, how Canadian boundary law actually works — and why every casing in this log ends the same way.

Two casings in the log point the wrong way for the audit's own story, and both are reported in full — one test the audit had to retract when better data arrived, and one lane where the minority map outperformed the majority. A report that never loses an argument with itself isn't checking. Failed and null tests are part of the record.

> **A NOTE ON LEGAL TERMINOLOGY**
>
> "Gerrymandering" has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense — manipulating electoral boundaries for partisan advantage. The legal tests that actually apply in Canada are different: whether boundaries provide "effective representation" under s.3 of the *Charter of Rights and Freedoms* (the constitutional standard the Supreme Court of Canada set in the 1991 *Saskatchewan Reference*), and whether the commission followed the rules of Alberta's *Electoral Boundaries Commission Act*. The audit's findings are evidence bearing on those legal questions. They are not proof of a legally-defined wrong, and this report does not describe them that way.

The audit measures the maps. It does not try to read the commissioners' minds, and it does not say either map breaks the law. The author has disclosed a relevant prior: he has donated to the NDP and volunteered for the party, and has also donated to the Progressive Conservatives, a predecessor party of the UCP. Three findings that ran against his expectation were kept in the report anyway. The audit is designed so anyone running the same scripts on the same data gets the same numbers. The code is public on GitHub. The random seeds came from a public timing source (Cloudflare drand) before the analysis was run. All input data is public.

---

## The picture, before the proof

![The two ways of measuring the maps, plotted together. Left-to-right: how skewed the map looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of four discriminating structural tests the map fails (municipal anchoring was the fifth but did not survive canonical recomputation — both maps within Canadian norm — so it is no longer counted; corrected 2026-06-12 per T1.7 R2 Ref #6) — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 map (teal) stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 map (purple) is a structural outlier on **four of four discriminating tests**; its efficiency gap (+4.0%) sits just below the Alberta threshold line. (Caption colours corrected 2026-07-08: an earlier caption called the majority purple and the minority green; in the chart the majority is teal and the minority purple.)](data/maps/article/stakes_quadrant.svg){: .verdict-hero }

Three maps, two lanes of measurement. One dot is not like the others. This picture is the audit's whole case in one image — and right now you have no way to judge whether it means anything. The lines on it are not laws. The corner is not a courtroom. By the end of this report you will know exactly what this picture can prove, and exactly what it cannot. The report comes back to it at the end.

---

## The Map on the Cover

The cover map is the best single image in this audit. Here is how to read it.

Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.

This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.

The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.

This was the image that made the stakes clear. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once you can see the population underneath the boundary choices, those choices stop looking random.

---

## Act I: What the Map Does {.new-page}

Act I walks the lines themselves. No election results, no simulation — geometry anyone can check against a paper map. The two drafts were drawn in the same room, by five commissioners working from the same statutory rules, the same provincial geography, the same archive of 1,147 public submissions, and the same demographic data. They agree on most of Alberta. Where they diverge, they diverge on choices someone in the room had to make.

### Casing 1 — A city of 85,805 with zero seats {#casing-1}

![The division of Airdrie into four separate districts, diluting its urban voting power.](data/maps/article/figure_airdrie_v3.svg)

**What we found.** The minority map splits the City of Airdrie into four pieces. Airdrie is the largest Alberta city without its own MLA: at 85,805 people (2024 municipal census) it is bigger than Red Deer, and it has one council, one tax bill, one school division — every civic system treats it as a unit. The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Olds-Three Hills-Didsbury, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district, and Airdrie's residents a minority in all four. The split meets every criterion of the audit's pre-registered cracking test (academic report §5.3.2); the majority's two-way split meets none.

**What it could show.** The textbook definition of *cracking* — splitting a community thinly enough that it decides nothing. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. If you wanted to dilute a fast-growing, politically contested city, this is what it would look like.

**What the experts say.** Community splitting is one of the primary red flags in the redistricting literature, because it is one of the two mechanical moves — with packing, its mirror — by which lines convert votes into fewer seats. A four-way split is invisible to every partisan-fairness statistic except the one that asks: can a voter find their MLA?

**What Canadian practice expects.** Canadian commissions treat municipal integrity as a core community-of-interest anchor. Splitting a city of this size in two is routine. Splitting it four ways, leaving its residents a minority everywhere, is not — and the same commission's majority draft proves a two-way split was available on the same geography.

**Why it isn't a smoking gun.** The *Electoral Boundaries Commission Act* permits splitting municipalities. Community of interest is one non-binding factor among several the Act lists, and the *Saskatchewan Reference* directs courts to defer to how boundary bodies weigh those factors. The audit's review found no Canadian decision striking down a map for splitting a city. Both maps are legal. The four-way split is a choice — and under Canadian law, choices inside the statute's wide lanes belong to the drawer. *(Legal lesson 1: the statute's factors are discretionary, and courts defer.)*

*A casing, not a gun.* — [Know more: Appendix A, what "cracking" actually does to a vote](#appendix-a)

### Casing 2 — The three boundaries the chair called out {#casing-2}

**What we found.** The commission's own chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national-park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; and the Olds–Three Hills–Didsbury reach into north Airdrie. In the commission's official final report, the chair called the park extension "a bad faith effort" to claim a population protection written for remote communities where people actually live. The majority map received zero such flags from the same chair — though the chair signed the majority report, so his criticism running only against the minority is what you would expect, not an independent verdict between the two maps. What gives the flags weight is that the audit's own blind geometric tests, which carry no allegiance, independently confirmed anomalous geometry for three of the chair's four geometric flags (the fourth, Calgary-Foothills-Airdrie West, did not meet the audit's confirmation threshold; his published criticism covers seven boundary configurations in total).

**What it could show.** An insider — the person legally responsible for the process — looked at these lines as they were being drawn and publicly alleged that a legal protection was being gamed. That is as close to direct evidence as this record gets.

**What the experts say.** Bizarre-shape analysis is where gerrymandering detection started, and corridors and uninhabited extensions are its canonical signatures. In fairness, the Banff arrangement has a defensible geography underneath the odd name and the odd shape — the town of Banff sits inside a federal park it cannot grow into, and grouping the townsite with Canmore has sound community-of-interest logic. That two-sided story is told in full in [the Banff section below](#banff); it credits what deserves credit and shows why the chair's objection stands anyway, aimed at the empty-park extension the townsite's placement does not touch.

**What Canadian practice expects.** Commissioners disagree in reports all the time. A chair accusing colleagues of bad faith in the official final report is, in the Canadian redistribution cycles this audit reviewed, unprecedented.

**Why it isn't a smoking gun.** The chair's words are opinion inside a report that has no legal force. "Bad faith" in a commission report is an accusation, not an adjudicated finding — no tribunal ever weighed it, and under the Act both reports became advisory the moment they were filed. The legislature could, and did, set them both aside. *(Legal lesson 2: commission reports bind no one — the legislature holds the pen.)*

*A casing, not a gun.* — [Know more: Appendix B, shape analysis and what s.15(2) protection is for](#appendix-b)

### Casing 3 — One zone of Calgary, drawn a quarter too big {#casing-3}

**What we found.** In Calgary's north-east and central districts — the audit's "Zone A" — the minority map's divisions average 11.5% above the province-wide population, versus 2.8% on the majority *(corrected 2026-07-08: earlier text said "northwest"; the zone the audit measures is NE/central Calgary — see §5.1.2 of the academic report)*. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. Thirteen of the zone's seventeen districts went NDP in 2023. The pattern meets the audit's pre-registered packing-signature test (academic report §5.3.1).

**What it could show.** This is *packing*: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and *cracking* (Casing 1) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.

**What the experts say.** Packing and cracking are the mechanism behind essentially every partisan-gerrymandering case ever litigated in the United States. Oversized districts precisely where one party's voters concentrate is the pattern the detection literature is built to find.

**What Canadian practice expects.** Deviations inside the legal band are normal, but Canadian commissions justify them with community-of-interest reasons. The minority's published reasons for this zone are among those that fail independent check — see Casing 11.

**Why it isn't a smoking gun.** Every one of those districts sits inside the Act's ±25% population band, and Canadian law has no cause of action for partisan *effect*. Section 3 of the Charter protects effective representation of citizens; it does not promise parties a proportional translation of votes into seats, and no Canadian court has read it that way. *(Legal lesson 3: inside the band, size asymmetry is lawful discretion — partisan effect is not a recognized legal harm.)*

*A casing, not a gun.* — [Know more: Appendix C, packing in a three-district toy example](#appendix-c)

### Casing 4 — Worse at the one thing the law actually measures {#casing-4}

**What we found.** The minority map's population spread is markedly wider than the majority's. Measured against the commission's own population tables, its Population Mean Absolute Deviation (MAD) is 4,707 — 48% wider than the majority map's 3,180. Measured instead on the audit's official-shapefile substrate, the minority's spread (3,938 vs the majority's 2,827) sits at the 99th percentile of the canonical neutral ensemble — only about 1 in 100 neutral maps produces a worse spread. *(Corrected 2026-07-08: earlier text merged these two separate measurements — the commission-table MAD and the shapefile-substrate ensemble percentile — into one figure; see [`findings/population_equality.md`](findings/population_equality.md) and `data/outputs/simulated_ensemble_percentiles_canonical.csv`.)*

**What it could show.** Vote equality is the one value the statute quantifies, and this map paid it away. Neutral processes do not pay that price for nothing; a map in the 99th percentile of spread is buying something with it. The common defence — "they had to draw weird boundaries to equalize population" — runs exactly backwards here: the minority map is *worse* at population equality than the majority drawn beside it.

**What the experts say.** Population equality is the first-order constraint in every redistricting formalism; spread this wide, on a map drawn simultaneously with a tighter one, is a cost signal — evidence that other objectives outranked the statute's central value.

**What Canadian practice expects.** Canadian commissions treat the deviation band as a limit, not a budget, and the long-run trend since the *Saskatchewan Reference* era has been toward tighter equality, not looser.

**Why it isn't a smoking gun.** The ±25% band is the *only* number in the statute, and no district on either map crosses it. The law does not rank maps inside the band: a 99th-percentile spread and a median spread are legally identical. *(Legal lesson 4: the statute contains exactly one number, and this map complies with it.)*

*A casing, not a gun.* — [Know more: Appendix D, what MAD measures and why the band exists](#appendix-d)

### Casing 5 — The casing that dissolved when we picked it up {#casing-5}

**What we found.** Early analysis showed the minority map anchoring to municipal boundaries only 15% of the time — 4.9× below the Canadian norm of 70–85%. On official Elections Alberta shapefiles the figure died: the majority anchors at 80%, the minority at 72%, both inside the norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). The 15% figure was an artefact of the audit's early provisional boundary reconstructions, traced from commission PDF images before official map files existed. The retraction is permanent and displayed in the corrections box below. What survives is narrower: where the minority *does* depart from pre-existing civic lines, the departures concentrate at the exact chair-flagged urban-edge zones — Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie — where pairing urban and rural voters most directly affects which party wins the seat. (*Anchoring*: the fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.)

**What it could show.** As originally computed, systematic abandonment of recognizable civic geography. It did not survive.

**What the experts say.** This is what an artifact looks like: provisional tracings manufactured a signal that the real map files erased. The methodological lesson is why this audit re-ran everything on official shapefiles the day Elections Alberta released them.

**What Canadian practice expects.** Nothing — no Canadian statute or practice guide requires any particular anchoring rate. The 70–85% norm is descriptive, not prescriptive.

**Why it isn't a smoking gun.** It isn't even evidence. It is the audit's own error, kept on display because a report that shows you its dead casings is the only kind whose live ones you should trust. *(Epistemic lesson: the null can win — and when it does, the report says so.)*

*Not even a casing. We logged it anyway.* — [Know more: Appendix E, how a data artifact fooled us and how it was caught](#appendix-e)

### Act I in one picture

![Four discriminating structural-fairness tests, side by side, plus the summary score (five tests were pre-registered; municipal anchoring was the fifth and did not fire on canonical shapefiles — both maps within Canadian norm; retracted 2026-05-18 and not plotted). Teal bars are the majority map, purple bars are the minority map. Where a test has a pre-registered failing line (the dashed red line), the purple bar crosses it and the teal bar stays inside it. On every test the teal bar sits at zero or well inside the safe range.](data/maps/article/lane2_bars.svg)

*(Figure corrected 2026-07-08: the previous version of this chart still plotted the retracted anchoring panel, showed the summary score as 5 of 5 instead of 4 of 5, labelled the Calgary zone "NW", and paired the zone-gap values with the wrong threshold. Its caption also had the two bar colours swapped. The chart is regenerated from `analysis/scripts/article_figures.py` against the canonical values.)*

The same tests in tabular form, with the pre-registered summary in the bottom row:

| Test | Majority map | Minority map | Direction / Beneficiary |
|---|---|---|---|
| Border follows existing municipal lines (70–85% Canadian norm) | 80% — within norm | 72% — within norm | N/A — both within Canadian norm |
| Population spread (tighter is better) | 3,180 | **4,707 — 48% wider** | Structural (Reduces vote equality) |
| NE/central Calgary population excess above average | 2.8% | **11.5%** | **UCP** (Packs urban NDP votes) |
| Boundaries flagged by the commission's own chair | 0 | **3** | N/A |
| Airdrie split (constraint minimum: 2) | 2 pieces | **4 pieces** | **UCP** (Cracks urban/suburban power) |
| **Pre-registered summary** (≥ 4 of 5 = outlier) | **0 of 5 fired** | **4 of 5 fired** (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire) | **UCP** |

On Act I's tests, the majority crosses zero discriminating structural thresholds. The minority crosses every discriminating one — four of four, with the retracted fifth shown rather than hidden. These measurements are geometric; they do not depend on any statistical sampler or any vote attribution. The audit pre-registered all five on April 24, 2026, before the final simulation results were compiled.

---

## Act II: What the Simulation Sees {.new-page}

Act I needed nothing but the lines. Act II asks a harder question: how unusual are these maps, compared to what a process with no agenda would draw? To answer it, the audit generated 1,010,000 computer-simulated, mathematically neutral Alberta maps (4 independent chains × 252,500 steps, base seed from the Cloudflare drand public randomness beacon, pre-registered at OSF before execution) using the official Elections Alberta shapefiles, holding to the same statutory rules and geographic boundaries the commission used. The simulation is a "what-if machine": what would Alberta's maps look like if nobody was trying to do anything? Place a real map inside that distribution and its percentile tells you how far into the tail it sits. A note on seat counts: the 2026 commission maps each have **89** districts; the simulation runs on the **87**-district 2019 substrate; the November committee will produce **91**. All percentages are seat *shares*, comparable across denominators.

One fact about Alberta makes every number below readable. In this province, neutral is not 50/50. Across the 1,010,000 neutral maps, the median map gives the UCP only 44.8% of seats when the province-wide vote splits exactly evenly — because rural UCP voters win their ridings by wide 60-40 margins (wasting many "extra" votes) while urban NDP voters win theirs by tighter 51-49 margins (wasting fewer). Alberta's natural political geography, left alone, mildly favours the NDP's seat efficiency. Keep that baseline in mind: it is what the maps below are being measured against.

### Casing 6 — Fewer than 100 maps in 1,010,000 {#casing-6}

**What we found.** Hold the electorate at a perfect 50/50 split and ask each map how many seats it awards the UCP:

| Map | UCP seats at 50/50 votes | Where it sits |
|---|---|---|
| 2019 enacted | 46.0% | 78th percentile — inside the normal range |
| **Majority 2026** | **46.1%** | **78th percentile — well within bounds** |
| **Minority 2026** | **51.7% (46 seats)** | **99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach this** |

The full neutral distribution: median 44.8%, 95th percentile 47.1%, 99th percentile 48.4%, maximum 51.72% — and 69 of the 1,010,000 plans exceed the minority map's 51.69%. *(Corrected 2026-07-08: this report previously described the maximum as "below 51.7%"; the committed ensemble data shows it is 51.72% — narrowly above the minority's value, not below it.)* On the other partisan-fairness metrics the same map sits at p99.97 (mean-median) and p98.8 (declination), all pointing the same UCP-favoured direction. Based on actual recent voting patterns, the minority map's geometry awards the UCP 60 of 89 seats, against 55 on the majority map.

To calibrate what "aiming" can achieve, the audit also ran a targeted hill-climbing procedure (Cannon et al. 2022 — the standard tool for exploring biased-but-legal maps) in both directions, 40,000 steps each, same constraints, same geometry:

| Procedure | Most-extreme value reached | What it tells us |
|---|---|---|
| Neutral simulation, maximum produced | 51.72% UCP seats @ 50/50 *(corrected 2026-07-08)* | The natural ceiling under neutral drawing |
| Neutral simulation, minimum produced | ~39% UCP seats @ 50/50 | The natural floor under neutral drawing |
| Targeted hill-climb, UCP-maximizing | **52.9%** | What a procedure deliberately aiming for UCP advantage can reach |
| Targeted hill-climb, NDP-maximizing | **37.9%** | What deliberate aiming the other way can reach |

The minority map's 51.7% sits closer to the deliberately-aimed UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. And the asymmetry around 50/50 is starker than the number alone: a precision sweep finds the minority map keeps the UCP at or above the 45-seat majority threshold down to a UCP vote share of about **49.7%** — the UCP could lose the popular vote by 0.3 points and still form government — while on the majority map the UCP would need to *win* the popular vote by about 4 points to reach the same threshold. Same geography, same rules; the gap between the two maps is structural, not noise.

**What it could show.** Neutral processes essentially never produce this map. The majority map is the kind of map a neutral procedure routinely generates. The minority map is the kind of map you have to specifically aim to draw.

**What the experts say.** Ensemble outlier analysis is the state of the art in redistricting statistics — the method US courts found persuasive in the state cases that struck maps down. Three of four pre-registered metrics in the extreme tail, all four directionally aligned, is a strong outlier profile. And the "it's just Alberta's natural geography" defence is already answered inside the method: the simulation runs *on* Alberta's natural geography. That geography's baseline advantage tops out where the 2019 map and the 2026 majority sit — the 78th percentile, with the 2019 map's highest placement on any partisan measure in the low 90s. The minority sits at p99.99 *against Alberta's naturally skewed baseline*. *(Corrected 2026-07-08: an earlier version said the natural advantage "caps around the 83rd to 90th percentile" — figures from a superseded provisional-geometry run.)*

**What Canadian practice expects.** No Canadian commission has ever been required to test its map against a neutral ensemble. This is the audit importing a standard the process itself never had to meet — which is exactly why the result is informative and exactly why it is not binding on anyone.

**Why it isn't a smoking gun.** Two reasons, one legal and one statistical. Legal: as far as this audit's review found, no Canadian court has yet weighed ensemble evidence, and in the United States the Supreme Court held in *Rucho v. Common Cause* (2019) that even strong statistical evidence of partisan gerrymandering is not for federal courts to police. A percentile is a description, not a threshold crossed. Statistical: the ensemble respects population and contiguity but does not enforce every statutory criterion the commission worked under (s.15(2) hybrid protections, community of interest, municipal anchoring), so its percentiles measure extremity against that reference distribution — not against "everything a legally compliant commission might have drawn." A strong external check; not a perfect one. One further honest limit: a real electorate is not a frozen 50/50 — voters can swamp any map's structural lean with a big enough swing. The 50/50 test isolates the map's contribution to the outcome, not the outcome itself. *(Legal lesson 5: the best evidence type in the field has no legal home in Canada.)*

*A casing, not a gun.* — [Know more: Appendix F, how the what-if machine works and how to read a percentile](#appendix-f)

### Casing 7 — The test that missed {#casing-7}

![How skewed each map looks on the partisan-fairness number. The majority sits at +0.1% — inside the normal range. The minority sits at +4.0%, just below the Alberta line at ~4.1%. The further right the dot, the more the map favours the UCP relative to its provincial vote share.](data/maps/article/lane1_dotplot.svg)

**What we found.** The fourth partisan-fairness metric, the *efficiency gap* — a single number measuring how lopsidedly a party's votes translate into seats — came in at +4.0% for the minority map: the 94th percentile. The audit's pre-registered outlier line is the 95th percentile (about +4.1% on Alberta's simulated distribution). It missed. Directionally UCP-favoured, but below the line, and reported that way in every table in this report. The majority map's efficiency gap is +0.1% (16th percentile).

**What it could show.** Taken alone, almost nothing — which is exactly why it is in the log.

**What the experts say.** The efficiency gap's proposed US threshold (about 7%) is an academic proposal no court has adopted. Near-misses are the natural behaviour of honest test batteries: a report whose every test fires should make a reader more suspicious of the auditor than of the map.

**What Canadian practice expects.** Nothing — no Canadian body uses the efficiency gap at all.

**Why it isn't a smoking gun.** It isn't even claimed as one. This casing exists to show the pile was counted honestly. Pre-registration cuts both ways: the same locked line that gives the other metrics their force makes this one a miss, and it stays a miss. *(Epistemic lesson: the threshold was set before the answer was known — so the answer is allowed to be "no.")*

*A casing, not a gun — and this one the audit does not even fire.* — [Know more: Appendix G, the efficiency gap in one worked example](#appendix-g)

### Casing 8 — One in 568,000, and what that number is not {#casing-8}

**What we found.** The probability that a neutral drawing process produces the minority map's combined four-metric profile is bounded at about **one in 568,000**. That is a deliberately cautious ceiling: the audit doubled its own margin to cover the second analytical channel it examined, so the true odds are at most this common — likely rarer. Why double it, rather than quote the stronger single-test number? Because the audit gave itself two chances to find something rare — two channels, two chances for luck to look like a signal — so the odds are multiplied by two before being quoted. The doubling also needs no assumption about how the two channels relate: it holds whether they are independent, correlated, or anything in between, which is exactly the objection that killed the old figure. And the four measures inside the simulation count as one look, not four, because they are combined into a single joint score before any probability is computed — that is why the multiplier is two and not more. (For the technical record: p ≤ 1.76×10⁻⁶, a Bonferroni-corrected, dependence-robust upper bound.) This report used to carry a stronger number — roughly one in fifteen million. That figure combined two channels (the four-metric joint score and the Swing-Zone Allocation Test) that were not statistically independent, and one of the channels later failed a corrected spatial null (Casing 10). The Fisher combination was retired as the headline on 2026-06-10; the correction is permanent and displayed.

**What it could show.** The reader wants this number to be "the probability the map is innocent." It is the audit's strongest single number, and the temptation to read it that way is enormous.

**What the experts say.** The number is well-defined and defensible as what it actually is: the probability of the *map's measured profile* arising under a *neutral drawing process*. In statistics, confusing P(evidence given innocence) with P(innocence given evidence) has a name — the prosecutor's fallacy — and it has sent innocent people to prison. This report refuses the swap. The rarity of the observation under the neutral null is not the posterior probability of wrongdoing; for that you would need things no one has, like the base rate of eccentric-but-sincere drafting.

**What Canadian practice expects.** No Canadian legal standard consumes a number like this. There is no threshold it could cross, because the law never defined one.

**Why it isn't a smoking gun.** A one-in-568,000 map can still, in principle, be the product of unusual but honest judgment. The number measures how far outside neutral practice the map sits. It cannot see motive, and this report will not pretend it can. What the audit does claim is the weaker, well-supported statement: routine drafting variation is not a plausible explanation for this profile. What *is* the explanation is a question the audit puts in the reader's hands. *(Legal-epistemic lesson: no probability of a map is a probability of intent.)*

*A casing, not a gun.* — [Know more: Appendix H, the prosecutor's fallacy in plain language](#appendix-h)

### Casing 9 — We tried to shoot our own result down {#casing-9}

**What we found.** Three attacks the audit mounted on its own headline, with mixed results — reported in full. First, the sampler swap: the tail position survives replacing the simulation's mathematical engine with a structurally different one (a spanning-forest sampler, pre-registered at OSF as registration he53s and executed 2026-07-10) — every metric's percentile moved by less than one point, a pre-registered ROBUST verdict on all four. Second, the software swap: an earlier cross-check against an independent implementation (the R `redist` package) produced unstable results on the old provisional geometry — a sampler-convergence failure documented at [`findings/redist_python_comparison.md`](findings/redist_python_comparison.md) — and became moot on official shapefiles, where zero plans from either implementation reach the minority's value at comparable sample sizes. Third, the mechanism test, which the audit's claim *failed*: the audit tested whether the flagged geometry of Act I (the corridors, the park extension, the splits) is the specific mechanism producing the Act II seat advantage. The answer is no. The two lanes converge on the same map and the same direction, but the geometry-is-the-mechanism claim did not survive its falsification test, and the report says so.

**What it could show.** The outlier is a property of the map, not of the audit's tooling.

**What the experts say.** Robustness across samplers and implementations is what separates a finding from an artifact; publishing your own failed falsification is what separates an audit from advocacy.

**What Canadian practice expects.** None of this is required by anyone. The audit imposed it on itself, in writing, before running it.

**Why it isn't a smoking gun.** Ruling out artifacts is not ruling in design. Surviving every attack the audit could mount establishes that the map is genuinely, robustly extreme — it says nothing about *why*. *(Epistemic lesson: robustness strengthens the description, never the accusation.)*

*A casing, not a gun.* — [Know more: Appendix I, what a sampler is and why swapping it matters](#appendix-i)

### Casing 10 — The signals that pointed the other way {#casing-10}

**What we found.** Three entries in the log that do not help the audit's story, all reported. **One the minority passed outright:** the neighbour-drain test looks for the classic adjacency pattern where packed districts sit right beside thin-margin ones. The minority shows 1 coupled chain signal against the majority's 2 (and the 2019 enacted map's 5) — a genuine pre-registered PASS, the single test where the minority numerically outperforms the majority. *(Corrected 2026-07-08: earlier versions carried the provisional-geometry counts — minority 2, majority 6; the official-shapefile run of 2026-05-23 gives minority 1, majority 2, and the pre-registered PASS is unchanged.)* Section 5.3.5 of the academic report explains why the pass is real but narrow: the minority achieves its partisan effect through *hybridization* — splitting cities into districts that mix urban and rural voters inside single ridings — which an adjacency test cannot see, because the packing and cracking happen within districts rather than between them. **Two the audit retired:** the Swing-Zone Allocation Test looked significant (p = 0.0024) until the audit corrected its null for spatial clustering — neighbouring voting areas vote alike, violating the test's independence assumption — after which it returns p ≈ 0.19, not significant; it was retired to exploratory status on 2026-06-13. And the Fisher combination that once produced the one-in-fifteen-million headline assumed an independence its channels did not have; retired 2026-06-10 (Casing 8).

**What it could show.** As originally computed, the retired tests suggested the specific boundary choices — not just the overall map — were partisan-loaded. After correction, they suggest nothing.

**What the experts say.** Spatial autocorrelation is the classic way redistricting statistics fool their own makers, and correcting for it is the method working as intended. A drain-test pass alongside tail results elsewhere is not a contradiction; it is a fingerprint — it tells you *which* mechanism this map does not use.

**What Canadian practice expects.** Not applicable — these are the audit's own instruments.

**Why it isn't a smoking gun.** Two of these were the audit's casings, not the map's, and the third points in the map's favour. They are in the log because an evidence log that only records convenient entries is not an evidence log. *(Epistemic lesson, stated twice in this report on purpose: the null can win.)*

*Two retired, one pass for the other side. We logged them anyway.* — [Know more: Appendix J, why neighbours voting alike breaks naive statistics](#appendix-j)

---

## Act III: What People Did {.new-page}

Acts I and II measured paper. Act III reads conduct — what the people in and around the process wrote, claimed, and chose. Conduct evidence is where intent questions usually get answered in court. Watch what happens to it here.

### Casing 11 — Five of six reasons don't survive checking {#casing-11}

**What we found.** Five of six of the minority commissioners' published rationales for their contested redraws fail under independent check — applied only to the minority because the minority is the map whose contested redraws are public.[^asym] (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.) The point is not that the minority's reasoning is invented; in most of these cases the general claim is true, and a boundary honouring it *could have* been drawn. What the data does not reach is the *particular line the minority actually drew*. It defends Calgary-Nolan Hill–Cochrane on the idea that Cochrane residents "move fluidly" into Calgary; Statistics Canada's 2021 journey-to-work data shows about a third of Cochrane's workers commute somewhere in Calgary while roughly half work within Cochrane — a real city-to-city tie, but one that says nothing about the Nolan Hill neighbourhood the corridor actually reaches. Airdrie's commute to Calgary (about 76 percent of its out-commuters) and its rapid growth are both real, and could have supported a new Airdrie-area seat — but neither requires splitting the city four ways. Chestermere sends 86 percent of its out-commuters to Calgary, yet shares no school division or transit system with the specific Calgary district the minority slices part of it into. And the minority's "shared schools" argument for pairing Red Deer with Sylvan Lake does not hold — Sylvan Lake is in Chinook's Edge School Division, the City of Red Deer in Red Deer Public.

[^asym]: The majority did not publish a contested-redraw rationale list. The seven-rationale audit cannot be applied symmetrically; it is reported as a single flag, not as additional rows in the structural-irregularity count.

**What it could show.** Reasons that do not survive checking look like rationalizations — reasons found after the line, not before. In each case a map honouring the real community-of-interest tie was available; the specific line drawn is not the one the evidence points to.

**What the experts say.** Comparing stated justification against what the evidence supports is pretext analysis — exactly how US courts probe intent in the gerrymandering cases they do hear. Rationales that fail on public data are the standard tell.

**What Canadian practice expects.** Commissions publish reasons precisely so the public can weigh them. Reasons that collapse against free, public Statistics Canada data defeat the purpose of publishing them.

**Why it isn't a smoking gun.** No Canadian law requires a commissioner's rationale to survive independent verification, and a failed rationale is legally consistent with sloppiness just as much as with pretext. Courts reviewing boundaries ask whether the outcome denies effective representation — not whether the reasoning in the file was good. *(Legal lesson 6: bad reasons for a lawful line are still a lawful line.)*

*A casing, not a gun.* — [Know more: Appendix K, how to check a stated reason against public data](#appendix-k)

### Casing 12 — The commission that couldn't sign one map {#casing-12}

**What we found.** The commission split: two final reports, two incompatible 89-seat maps, filed the same day. The three-commissioner majority included the chair; the two-commissioner minority — the commissioners the government nominated — produced the map every previous casing describes. The audit's instruments cut both ways across that divide. The chair asserted in his Appendix C that the minority's seven contested configurations had **no public support** in the ~1,340 submissions; the audit keyword-searched the full archive (93.4% machine-parsed; methodology and per-configuration evidence at [`findings/submission_search_findings.md`](findings/submission_search_findings.md)) and found the chair right on three of seven, wrong on three (Rocky Mountain House–Banff Park, Olds–Three Hills–Didsbury, and Chestermere each had documented public support or aligned submissions), and partially wrong on one. The chair's blanket claim is demonstrably overbroad. **That finding cuts against the chair, not the minority** — and it is in this log for exactly that reason. The criticism also ran the other way, and the log records that too: the minority report charges the majority with “an inclination to delete or mangle rural electoral divisions and, in effect, reduce effective rural representation” (minority report, p. 356; see also p. 287: the minority “departed from the majority where we believe the legislative direction given to the Commission and the thoughtfulness of public submissions has not been given sufficient effect”). The audit's one majority-targeted structural counter-test to date — whether the majority's rural districts are engineered corridors of isolation — came back supporting the innocent, geographic explanation (exploratory; design and limits at `preregistration/t3_2_majority_rural_isolation_design.md`). The audit ran that count the same day the charge was surfaced (exploratory; hypotheses frozen before execution; full method, names, and classifier limits at `findings/rural_division_count.md`). The direction reverses: against 2019's 31 rural-anchored divisions, the majority keeps 28 — absorbing three into city-named districts and amalgamating six into three — while the minority keeps 23, absorbing seven, including the two divisions merged into the chair-flagged Rocky Mountain House–Banff Park. A stricter classifier variant gives the same ordering (28 → 24 → 19). Both maps thin rural representation relative to 2019, which is the true core of the charge and consistent with the chair's own call for added rural seats; but on the measure the accusation itself names, the minority map does more of what it accuses the majority of. The same page makes a second measurable charge — that the majority "declined to use" the Act's ±25% flexibility in rural Alberta — and that one holds (`findings/rural_variance_usage.md`): the majority's rural divisions average 6% below the provincial mean with only four drawn more than 10% light; the minority's average 12% below with eleven drawn more than 10% light. Tested together, the two charges describe two design philosophies, not one vice: more-but-fuller rural divisions on the majority, fewer-but-lighter on the minority. Both directions of every cut are in the log.

**What it could show.** A process designed to converge produced two answers, and the outlier map came from the government's nominees. The reader is invited to find that suggestive; many will.

**What the experts say.** Who appointed whom is standard evidence in institutional-capture analysis — and it only carries weight when the instruments are applied symmetrically, which is why the audit's correction of the chair matters as much as its findings against the minority.

**What Canadian practice expects.** Consensus reports are the norm; the machinery of the Act assumes one map arrives. A split commission, with the chair publicly accusing colleagues, is not a scenario the statute was written for.

**Why it isn't a smoking gun.** Nomination is not instruction. The audit found no evidence of coordination between the government and its nominees, and none is inferable from appointment alone. Commissioners of every provenance have gone their own way before. *(Epistemic lesson: provenance raises the question; it cannot answer it.)*

*A casing, not a gun.* — [Know more: Appendix L, how commissioners are appointed and what nomination does and doesn't imply](#appendix-l)

### Both sides, tested — the accusations ledger

Every accusation each side put in writing, run through the same instruments and reported where it landed. All results are exploratory unless the linked finding says otherwise.

| The accusation | Who made it | Where it landed |
| --- | --- | --- |
| Three of the minority's boundaries are geometrically anomalous | The chair (majority report) | Largely confirmed — the audit's blind tests independently confirmed three of the chair's four geometric flags; the fourth fell below threshold |
| The minority's seven contested configurations had "no public support" | The chair (Appendix C) | Overbroad — right on three of seven, wrong on three, partially wrong on one (`findings/submission_search_findings.md`) |
| The park extension was "a bad faith effort" to claim s.15(2) protection | The chair (final report, p. 10) | Undercut — the division qualifies under s.15(2) even without the flagged extension |
| The majority "delete[s] or mangle[s] rural electoral divisions" | The minority (p. 356) | Reversed — the minority keeps fewer rural-anchored divisions (23 vs 28, against 2019's 31) and absorbs more into city-named districts (`findings/rural_division_count.md`) |
| The majority "decline[d] to use" the ±25% flexibility in rural Alberta | The minority (p. 356) | Supported — majority rural divisions average −6.0% deviation (4 below −10%); the minority's average −12.2% (11 below −10%) (`findings/rural_variance_usage.md`) |
| "Substantial and consistent testimony" for hybrids was ignored | The minority (p. 356) | Overbroad — support was configuration-specific: documented for three of seven hybrid configurations, absent for three |
| The majority's rural districts are engineered corridors of isolation | The audit's own counter-hypothesis (T3.2) | Not supported — the geographic explanation held; the majority cleared |

Neither side's accusations survived intact, and neither side's map escaped a hit. On the floor of the legislature, no one criticized the majority report at all — the government wrapped its motion in the majority chair's own recommendation, and the opposition demanded the report's adoption (`findings/hansard_april16_motion19.md`); the written charges against the majority exist only in the minority's own pages, which is why the audit had to test them itself.

### Casing 13 — When the process might have answered, it was replaced {#casing-13}

**What we found.** Three weeks after the split reports arrived, the Legislative Assembly passed Motion 19 (April 16, 2026, by a vote of 44 to 36), setting both reports aside and establishing a Special Select Committee of five MLAs — three UCP, two NDP, chaired by UCP MLA Brandon Lunty — to draft a 91-seat map by November 2, 2026. The committee is not required to hold public hearings, and per [CBC's reporting](https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743) it will not hold hearings on the map it produces; no draft will be released for public challenge before the map is final. The commission this committee replaced held hearings in sixteen communities, received 1,147 written submissions, and reversed its own interim proposal on the strength of 80-plus of them — the system visibly responding to public input. The committee is served by an advisory panel (government-appointed chair plus two nominees per party, [chaired by retired Court of Appeal justice Brian O'Ferrall](https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-panel-legislative-committee-elections-9.7187435)); the panel advises, and the five MLA votes decide.

**What it could show.** When the independent route failed to deliver a usable answer, the government took the pen — and the vehicle it chose removed every mechanism by which the public could contest what it writes before it becomes law.

**What the experts say.** The design forfeits each transparency feature the redistricting literature treats as protective: published drafts, public hearings, arm's-length drafters. Civil-liberties observers ([CCLA](https://ccla.org/press-release/ccla-sounds-the-alarm-over-the-politicization-of-albertas-electoral-map/)) raised the politicization concern independently of this audit.

**What Canadian practice expects.** This is the deepest norm in Canadian redistribution — politicians do not draw their own districts. The audit's November tests (below) will measure the committee's process against exactly the features it is not required to provide.

**Why it isn't a smoking gun.** Every step is lawful. The Act makes the commission's reports advisory, sets no minimum notice or comment period, and imposes no hearing or draft-release requirement on what follows. Under parliamentary sovereignty the legislature may lawfully do precisely what it did. *(Legal lesson 7: the process that could have created accountability is optional — and opting out is legal.)*

*A casing, not a gun.* — [Know more: Appendix M, the Act's process from commission to committee, end to end](#appendix-m)

### Casing 14 — The sixty-year norm, set aside in an afternoon {#casing-14}

**What we found.** Canada spent roughly sixty years building independent boundary commissions — the institutional answer, since the 1960s federal reform era, to the once-routine practice of governing parties drawing their own ridings (Courtney 2001, the standard history). The process now promoting a government-controlled committee mid-cycle is **without precedent among the Canadian redistribution cycles this audit reviewed** — an assessment political scientist Duane Bratt (Mount Royal University) shared in correspondence with the author. None of the reviewed provinces lets a governing-party majority hand redistricting to a committee its own party controls partway through a cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither.

**What it could show.** The injury is not one map. It is the demonstration that the guardrail was a convention — and conventions only bind governments that consent to be bound. Nothing prevents the next government, of any party, from citing this cycle as precedent.

**What the experts say.** The comparative literature treats independent commissions as the single most protective institutional feature against gerrymandering. Removing the institution matters more than any one boundary it might have drawn.

**What Canadian practice expects.** Every province and the federal process use arm's-length commissions. That is the standard this cycle departed from — mid-cycle, by simple majority vote.

**Why it isn't a smoking gun.** Constitutional conventions are politically binding but not judicially enforceable — the Supreme Court said as much in the 1981 Patriation Reference, and courts have held the line since: a court may name a convention, and will still decline to enforce it. The norm's violation is real, documented, and judicially irrelevant. *(Legal lesson 8, the last one: norms are not law — and the gap between them is where this entire episode lives.)*

*A casing, not a gun.* — [Know more: Appendix N, conventions versus law, and how norms erode](#appendix-n)

---

## The Scorecard, Revisited {.new-page}

Fourteen casings. No gun. Now go back to the picture from the start of this report — you can read it now.

The horizontal axis is Act II's headline number (the efficiency gap — further right, more UCP-favoured). The vertical axis is Act I's count of discriminating structural tests failed. The 2019 map and the 2026 majority sit in the quiet corner: near-zero skew, zero structural flags. The minority sits alone: four of four structural flags, efficiency gap just under the audit's calibration line, and — off this chart's axes — the p99.99 tipping point, the p99.97 mean-median, the 60-of-89 seat outcome. The two lanes converge on the same map, the same direction, and the same communities: the urban-hybridization pattern Act I found is the structural pattern consistent with the seat advantage Act II measured — even though the specific geometry-is-the-mechanism claim failed its test (Casing 9), the direction of both lanes agrees. (Earlier drafts of this paragraph used intent language — "strategically dilutes… engineers" — inconsistent with the audit's posture; reworded 2026-06-12.)

| | Act I: Structure (geometry-only, no votes) | Act II: Numbers (vote-dependent) |
|---|:--|:--|
| **Majority 2026** | clean — crosses *no* structural threshold | inside the normal range on every metric (`seats@50/50` 46.1% — p78; efficiency gap +0.1%) |
| **Minority 2026** | **crosses 4 of 5 structural thresholds** by a wide margin (anchoring neutral — both maps within Canadian norm) | tail flags on **three of four** partisan-fairness metrics, all four directionally UCP-favoured (Amendment 10 sign correction, 2026-06-12); `seats@50/50` 51.7% (p99.99, roughly 69 of 1,010,000 reach it); mean-median p99.97; declination p98.79 (UCP-tail under corrected Warrington sign); efficiency gap +4.0% (p94.5 — *near, but below*, the pre-registered 95th-percentile threshold; directionally UCP-favoured but sub-threshold); dependence-robust joint bound p ≤ 1.76×10⁻⁶ (~1 in 568,000) |

Act I carries the case. Its five tests were pre-registered on April 24, 2026, before the final simulation results were compiled; its measurements are geometric and do not depend on any sampler or vote attribution. Act II corroborates without carrying (the earlier Fisher combined p = 6.87×10⁻⁸ assumed channel independence and was retired as the headline 2026-06-10 — see academic report §5.5).

> **THE PLAIN READING.** Two electoral maps were drawn in the same room, by five commissioners working from the same rules and the same data. The majority map is the kind of map a neutral procedure routinely produces: clean on every one of the audit's pre-registered structural tests, comfortably inside the simulated partisan-fairness distribution. The minority map is something else. It crosses four of five structural-irregularity tests — chair-flagged lasso corridors (3 confirmed of 7 configurations criticized), the four-way Airdrie split, the national-park extension, and the 48%-wider population spread — and on 1,010,000 computer-simulated neutral maps drawn from the official Elections Alberta shapefiles, its `seats@50/50` value is reached by fewer than 100 neutral maps. *(Municipal anchoring is the fifth pre-registered test; it is retracted — both maps fall within the 70–85% Canadian norm on official shapefiles. See the correction note below.)* Three of four partisan-fairness measures flag it in the statistical tail (efficiency gap at p94.4 is directionally aligned but sub-threshold; all four agree on direction); the joint probability of that combination under a neutral drawing process is at most one in 568,000 (Bonferroni dependence-robust upper bound). The audit tested whether the unusual geometry is the specific mechanism that produces the seat advantage; that claim did not survive the falsification. What does survive: same room, same rules, same data, two very different maps, and only one of them has the structural pattern that researchers flag for further inquiry. Whether the cause was deliberate engineering, unlucky drafting, or both is a judgement call the audit puts in the reader's hands.
>
> The audit measured the effects. It cannot read minds.

Now run this instrument itself through the same five questions, one last time.

**What we found.** A scorecard: the best instrument the author could build to correlate fourteen casings into something that can be stated, checked, and falsified. Five pre-registered structural tests — the minority crosses every discriminating one, the majority none, the retracted fifth displayed. Four partisan-fairness metrics against 1,010,000 neutral maps — three in the extreme tail, one reported miss.

**What it could show.** The closest thing to a gerrymandering *signal* that can exist under Alberta law and Canadian norms: a disciplined way of saying "this map is the kind of map that aiming produces," with every threshold set before any answer was known.

**What the experts say.** Composite outlier batteries are how the field reads maps when intent is unobservable; pre-registration is what keeps them honest.

**What Canadian practice expects.** Nothing — no Canadian institution scores maps this way. That is exactly why the audit had to build one.

**Why it isn't a smoking gun.** Its thresholds are the audit's own calibrations, not legal lines. Alberta is one province with one split commission — a sample size of one. And no accumulation of casings ever becomes a gun, because the gap between "extreme" and "deliberate" is not statistical. It is the gap the law chose to leave open.

*A casing, not a gun. But this casing fires again in November.*

> **WHY A LARGE MAJORITY MATTERS**
>
> Under Canada's Westminster parliamentary system, Alberta's Assembly has no two-thirds threshold that unlocks special powers: a governing majority — even a bare one — can already pass laws and budgets, invoke "closure" to end debate, change the rules of the House, and set the membership of every committee. What a very large majority changes is margin and durability, not the menu of powers. A government holding 60 of 89 seats is effectively immune to internal dissent — a handful of floor-crossings cannot threaten it — and faces an opposition too small to force recorded divisions or sustain committee scrutiny. The concern here is the concentration of seats and the thinning of effective opposition, not a procedural threshold being crossed.

### What running the play again would look like

This report cannot prove a gerrymander — the word has no legal home here. What it can do is say, in advance and in public, exactly what the signature looks like, and then say whether the November map carries it. The audit's November tests were registered (OSF, registration qsgy8) before the committee's map existed. The registration's own name for the check is **the Lunty test**: it is the confirmatory counterpart to everything above. The signature has two halves. Process: were public hearings held; was a draft released; are the advisory panel's members and terms of reference published; does the map honour the recommendation the government cited when it took the pen — nine process features now frozen as their own registered scorecard (OSF, registration u47bq, filed July 14, 2026), so the process half is scored the same locked way the map half is. Outcome: where the map lands on every metric in this report, against the same million-map distribution, under the same pre-registered thresholds — including whether the two added rural seats are a plain addition or an engineered one.

If the committee's map replicates the minority's signature — drawn by different people, under different constraints, on a different timeline — the structural finding above earns confirmatory status. If it lands inside the neutral bands, the finding stands as an isolated observation about one map that was never enacted, and this report will say exactly that. The scoring runs within 72 hours of the map's release, whichever way it points. That commitment was registered before anyone knew the answer. Pass or fail, the reader will not have to trust this audit's judgment — only its arithmetic, which is public, seeded from a public beacon, and reproducible by anyone.

> **RETRACTION CONDITIONS**
>
> *The audit's findings are pre-committed to falsifiability. Retractions apply per-finding. If any condition below materialises, the specific finding it relates to is retracted publicly within 30 days. The overall verdict (directional consistency across multiple correlated dimensions) is retracted only if at least three of the dimensions fail.*
>
> 1. **A counter-map exists.** Someone produces a legal Alberta map satisfying the minority's own community-of-interest reasons (Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park) *and* anchoring on municipal boundaries at majority-comparable rates. Open challenge — [Issue #14](https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14) on the audit's GitHub repository.
> 2. **The Neighbour-Drain Pass fails the label-shuffling null.** If the v2 continuous drain score (Phase B of `analysis/scripts/drain_phase_b_canonical.py`, documented in `findings/drain_label_shuffle_null_canonical.md`) falls in the extreme upper tail (p < 0.05) of random permutations across the fixed contiguity graph, the "pre-registered pass" is retracted and reclassified as a detected spatial signature.
> 3. **A pre-2026 internal commission document surfaces.** Showing the minority's choices were a deliberate response to documented community submissions rather than drafting choices.
> 4. **The 2027 election result, fought on either of these maps, contradicts the percentile readings.** If the partisan-fairness direction the audit projects from 2023 votes turns out to be wrong on actual votes, the Lane 1 finding gets revisited.
> 5. **The Quebec 2026 Supreme Court ruling is materially distinguished by an Alberta court.** If a court reviewing the April 16 Alberta motion finds the Alberta situation is constitutionally distinct from Quebec's — for example, because the Lunty committee is structured differently from a legislative-freeze law, or because Alberta's effective-representation analysis differs from Quebec's — the audit's procedural critique of the motion weakens.

> **DOCUMENTED CORRECTIONS**
>
> **2026-05-11 (canonical recomputation).** The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.
>
> **Municipal anchoring (retracted).** Early analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9× below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring *divergence* between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction.
>
> **2026-07-08 (verification pass).** A verification pass against the audit's committed data files caught two more figures that were stale or internally inconsistent with other parts of this report. Both are corrected in place above; documented here per the same never-delete-silently policy.
>
> **Neighbour-drain coupled-signal counts (corrected).** This report previously cited the neighbour-drain adjacency test's provisional-geometry counts — minority 2 coupled chain signals versus the majority's 6. The canonical run against official Elections Alberta shapefiles ([`findings/neighbour_drain_analysis.md`](findings/neighbour_drain_analysis.md), 2026-05-23) gives minority 1 versus majority 2 (and the 2019 enacted map's 5). The pre-registered PASS for the minority is unchanged under either count.
>
> **Ensemble maximum, seats@50/50 (corrected).** This report previously described the 1,010,000-map simulation's maximum `seats@50/50` value as "below 51.7%." The committed ensemble data (`data/outputs/simulated_ensemble_raw_samples_canonical.csv`) shows the true maximum is 51.72% — narrowly above, not below, that figure — and that 69 of the 1,010,000 plans exceed the minority map's 51.69% value. The report's separate "fewer than 100 of 1,010,000 reach this" statements elsewhere remain accurate (69 < 100) and are unchanged.

---

## The Invisible Part

This audit ran into two data problems that have nothing to do with the commission and everything to do with how Alberta's electoral system is designed. Both are fixable.

**Elections Alberta already has the data to tell us where advance voters live — it just doesn't publish it.** About half of all Alberta votes are now cast before election day — advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. That means roughly 395,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted; they just can't be located. This is not a technical problem. Every advance voter is checked against a voters list before receiving their ballot, and that list links each voter to their specific Voting Area. The information exists at the moment of voting. Elections Alberta simply does not retain or publish that link in its results. No change to the voting process is required — only a change to what EA reports from data it already holds.

This affects the commissioners too, not just outside analysts. When a commission decides whether to keep Airdrie whole or split it, whether a corridor between two communities makes sense, whether a proposed boundary divides a natural constituency — those are judgments that depend on knowing where voters live. Commissioners work from the same published dataset as everyone else. Half the geographic signal about the communities they are drawing boundaries around is missing for them as well.

There is at least one community in northern Alberta where this gap is total. In the northern part of the Lesser Slave Lake division, there is a Voting Area covering 4,832 km² — larger than Prince Edward Island — where every single vote in 2023 was cast through Elections Alberta's mobile polling team. Those 844 residents' choices are counted in the divisional total but cannot be pinned to any location on a map. That community is entirely invisible in the published election results.

When the commission initially considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. The commission eventually preserved the division — after 80+ public submissions, many from the Indigenous communities in the northern part of the riding — invoking a provincial law that allows ridings with First Nations and Métis communities to have smaller populations than the provincial average. They got there. But the data they were working with didn't show them who was voting in the communities they were deciding to protect.

### Banff: the town and the park {#banff}

Here is the other side of that story: while the Indigenous communities in Lesser Slave Lake were fighting to be counted, the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. There is a detail in the name itself. The minority calls that riding "Rocky Mountain House–Banff Park" — but the town of Banff is not in it. The Banff townsite, along with Canmore, sits in a neighbouring riding the minority names "Canmore-Kananaskis." The district that carries Banff's name is the uninhabited park; the place where Banff residents actually live was drawn into a different seat. The commission's own chair called the move "a bad faith effort" to claim the legal protection. That phrase is in the commission's official final report. The protection designed for remote communities with Indigenous populations was used, in the minority's map, to defend a boundary through uninhabited wilderness. The communities it was designed to help had to fight for it through public submissions.

There is, in fairness, a coherent geography underneath the odd name and the odd shape — and it is worth stating, because on a map the arrangement looks like an error and by name it sounds like one. Banff is unusual among Alberta towns: it sits *inside* a national park, on federal land it is not permitted to grow into. For provincial purposes, almost the only people the province represents in that whole stretch of the Rockies live in the townsite itself; the park around it is empty federal land. Seen that way, grouping the townsite with Canmore — the next town down the Bow Valley — is a defensible community-of-interest choice: it keeps the valley's residents together in one seat and leaves the uninhabited park as a separate, sprawling rural division. It is also why the boundary looks wrong on a screen. The line wraps tightly around the town because the town is the only populated pocket for miles, and the riding carries a different name than the park because Alberta names many of its divisions for the land they cover, not the towns inside them. This does not dissolve the chair's objection; it separates two questions that the shape on the map runs together. *Where* Banff's residents were placed has a sound logic, and that logic is worth crediting. The chair's objection was aimed at something the placement does not touch, and it is the part that matters for this audit: in the commission's official final report, the chair called the minority's extension of the riding through the uninhabited park "a bad faith effort" to claim a population protection — one written for remote communities where people actually live — for a boundary drawn where no one does. That objection stands on its own. The defensible geography of the town's placement does not answer it, and is not offered here as if it did.

[**See it on the map ↗**](https://ixby.github.io/alberta-electoral-boundaries-audit/?poi=banff-town) — opens the explorer on Banff, where the town's boundary and the park riding to its north are both annotated.

**Alberta should draw its next maps on the most current census data available.** Canada counts its population every ten years, and the gap between the count and usable map data is long. The 2026 census was enumerated in spring 2026, but Statistics Canada will not release usable sub-provincial data until roughly 2027 or 2028. The commission that drew the maps assessed in this audit had to use the 2021 census — already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the *Electoral Boundaries Commission Act* could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live, not where they lived a decade ago.

Neither of these is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be. They are offered here as practical suggestions, not conclusions.

---

## The Author's View {#authors-view}

*Everything above this line is the audit. Pre-registered tests. Documented corrections. Evidence you can check without trusting me. Delete this section and not one number changes. What follows is not a finding. It is an opinion — signed, severable, and mine.*

The audit cannot prove intent. I have kept that discipline on every page above. This page is where I set it down.

Start with the two facts I cannot make innocent. Government-nominated commissioners drew a map that neutral map-drawing almost never produces — fewer than a hundred matches in a million draws. And when the commission split rather than endorse it, the government did not ask why. It took the pen.

Each fact has an innocent reading. A commissioner can be eccentric in good faith. A legislature can lose patience with deadlock. But put the facts in sequence and the innocent readings strain. A government wanted a certain kind of map. The independent route did not deliver one. A route was found that would.

Here is what alarms me. It is not that a law was broken. No law was broken — I checked, and that checking is most of what this audit is. The statute makes the commission's report advisory. It sets no notice period. It requires no draft, no hearings, no consultation. Every step of the takeover was legal. That is the alarm. The guardrail was never law. It was a habit — and habits only bind governments that choose to keep them.

Look at what the habit used to buy. The commission held hearings in sixteen communities. It read 1,147 written submissions. It changed its mind in public, because the public gave it reasons to. The committee that replaced it is five MLAs: three government, two opposition, government chair. No rule required an independent voice at that table, and none sits there. There is an advisory panel — chaired, to its credit, by a retired judge. But advisers advise. The five votes belong to the MLAs, and the map they draw is the map they will run in. It will face no public hearing. No draft will be released for the public to contest. It arrives finished.

And this government has been here before. Its first bill, as written, would have let cabinet rewrite laws without the legislature. That power was stripped — after the outcry, not before. Its own ethics commissioner found the Premier breached the conflicts law by pressing her attorney general about a criminal case, and called interference with the administration of justice "a threat to democracy." It passed a law letting cabinet repeal local bylaws and trigger the removal of elected councillors. And when a court paused one of its laws in December 2025, it invoked the notwithstanding clause; within a week the injunction was gone. Every one of those moves was lawful. Every one spent a norm to get past an independent check. Redrawing the electoral map through a committee the government controls is not a departure. It is the pattern, applied to elections.

Political scientists have names for governments that keep the letter of the law while hollowing out the norms beneath it. The gentlest is *democratic backsliding*. The literature is blunt about how it works. Democracies rarely die of coups anymore. They die of this — one lawful, norm-breaking step at a time, each with a plausible reason, none of them illegal.

Canada spent sixty years building one norm above the rest: politicians do not draw their own districts. Voters choose their representatives. Not the reverse. In April 2026, Alberta set that norm aside in an afternoon, by a vote of 44 to 36.

I worry about what the map buys. On recent voting patterns, the minority map's geometry yields sixty seats of eighty-nine. That is not a mandate. It is insulation — from floor-crossings, from committees, from any opposition large enough to sustain scrutiny. I would worry about that insulation in any hands. I worry more in the hands of a government that has just shown me, in this very file, what it does with procedural control when a process threatens to answer back.

I could be wrong. Unlike most opinions about this government, mine ships with the terms of its own destruction. The committee's map is due November 2. The tests were locked before it existed. Were hearings held. Are the advisers named, their terms of reference published. Does the map honour the recommendation used to justify the takeover. Where does it land against a million neutral maps. If it lands inside the neutral bands, my suspicion took real damage — and this site will say so within seventy-two hours, because I committed to that before I knew the answer. That is the difference between an opinion and an accusation. An opinion tells you what would change it.

— Will Conner

*Sources for this section.* The ethics finding and the quoted phrase are verbatim from the Ethics Commissioner's report, [Allegations Involving Premier Danielle Smith (May 17, 2023)](https://www.ethicscommissioner.ab.ca/media/3124/allegations-involving-premier-danielle-smith-may-17-2023.pdf): "In my opinion, Premier Smith contravened s.3 of the Conflicts of Interest Act in her interaction with the Minister of Justice and Attorney General." The Sovereignty Act's original cabinet powers and their removal: [CBC, December 2022](https://www.cbc.ca/news/canada/edmonton/alberta-sovereignty-act-1.6678407). Bill 20's cabinet powers over councillors and bylaws: [CBC, April 2024](https://www.cbc.ca/news/canada/edmonton/alberta-bill-gives-cabinet-power-to-remove-municipal-councillors-change-or-repeal-bylaws-1.7185346) and the [RMA analysis of the act as passed](https://rmalberta.com/wp-content/uploads/2025/10/Bill-20-Member-Resource-Branded.pdf). The notwithstanding-clause invocation and the injunction's end: [CBC, December 2025](https://www.cbc.ca/news/canada/edmonton/alberta-government-notwithstanding-clause-bills-9.6983786) and [Egale Canada's case timeline](https://egale.ca/awareness/egale-v-alberta-healthcare/). The committee's structure, the advisory panel, and its judicial chair: [CBC, April 2026](https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743) and [CBC, May 2026](https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-panel-legislative-committee-elections-9.7187435); the commission's sixteen-community hearings and 1,147 written submissions are from the same reporting. Motion 19's 44–36 vote and the committee's mandate: §5.9 of the [academic monograph](https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md). "Democratic backsliding" follows Steven Levitsky and Daniel Ziblatt, *How Democracies Die* (Crown, 2018), and Nancy Bermeo, "On Democratic Backsliding," *Journal of Democracy* 27(1), 2016. The ensemble and seat figures are this audit's own, sourced throughout the report above.

---

## Appendices: From Confusing to Clear {.new-page}

Each casing above links to one appendix here. Each appendix owns exactly one concept, starts from the honest confusion, builds the idea with one concrete example, sends you back to the casing's number able to read it unaided — and ends with what the concept *cannot* tell you. They can be read in any order.

### Appendix A — What "cracking" actually does to a vote {#appendix-a}

*The confusion:* "Airdrie voters still vote. Nobody took their ballots. How does drawing lines 'dilute' anything?"

Imagine a town of 40,000 that mostly votes Orange, sitting in a region that mostly votes Blue. Give the town its own riding and it elects an Orange MLA: 40,000 people, one seat, a voice. Now slice the town into four pieces and staple each piece to a chunk of Blue countryside. In each new riding the town's 10,000 voters face 30,000 rural voters. Orange loses all four. Same voters, same ballots, zero seats. Nothing was stolen from any individual voter; what was taken is the *community's* ability to elect anyone. That is cracking. The mirror move, packing (Appendix C), stuffs a group into as few ridings as possible so it wins those overwhelmingly and nothing else.

Now re-read Casing 1: 85,805 people, four ridings, a minority in every one — and the same commission's other draft shows two ridings were enough to satisfy the law.

*The limit:* cracking describes an effect, not a motive. A split can happen because someone wanted dilution — or because other constraints crowded the map. The geometry alone cannot say which. [Back to Casing 1](#casing-1)

### Appendix B — Shape analysis, and what s.15(2) protection is for {#appendix-b}

*The confusion:* "All electoral districts look weird. Why do these three shapes matter?"

Districts follow geography, so lumpy is normal. What shape analysis looks for is *work* — a boundary doing something no ordinary constraint explains. A corridor that lassoes one neighbourhood into a distant district. An arm reaching into a city's edge. A line extended through land where nobody lives. Alberta's law has a special provision, section 15(2), that lets up to four districts fall below the normal population floor — written for remote districts with strong community ties, like northern ridings serving Indigenous communities across vast distances. Extending a boundary through uninhabited national park to qualify a district for that protection is what the commission's own chair called "a bad faith effort": using a rule written for people who live far apart to protect a line where no one lives at all.

Now re-read Casing 2: three shapes, flagged by the process's own chair, independently confirmed by tests that had no stake in his fight.

*The limit:* a strange shape is a question, not an answer. The Banff section of this report shows how one of these shapes has a real, creditable logic underneath — and why the chair's objection survives it anyway. [Back to Casing 2](#casing-2)

### Appendix C — Packing, in a three-district toy example {#appendix-c}

*The confusion:* "Bigger districts have more voters. So what? Everyone still gets one vote."

Take 12,000 voters, 7,000 Orange and 5,000 Blue, split into three districts of 4,000. Draw them evenly and Orange wins all three. Now redraw: cram 4,000 Orange voters into one district (Orange wins it 100–0), and spread the remaining 3,000 Orange across two districts of 4,000 where Blue's 5,000 give it the edge in both. Same 12,000 voters, same 7,000 Orange majority — but now Orange holds one seat and Blue holds two. That is packing: your opponents' votes get warehoused where they pile up as surplus, wasted on margins they didn't need. The tell is district *size and concentration*: opponents' districts run big and deep, yours run lean and efficient.

Now re-read Casing 3: in the one Calgary zone where 13 of 17 districts vote NDP, the minority's districts run 11.5% over the provincial average; the majority's, drawn in the same room, run 2.8%.

*The limit:* oversized districts can also come from honest guesses about growth, or from keeping a community whole. Size asymmetry is the signature packing leaves — and also the signature several innocent choices leave. [Back to Casing 3](#casing-3)

### Appendix D — What MAD measures, and why the band exists {#appendix-d}

*The confusion:* "Population Mean Absolute Deviation — is this just statistics for 'the districts aren't identical'?"

Almost. Every district can't hold exactly the same number of people — communities come in awkward sizes. MAD asks: on average, how far does each district stray from the ideal share? A MAD of 3,180 means districts miss the ideal by about 3,180 people on average; 4,707 means the misses average half again larger. The law tolerates straying — Alberta allows ±25% — because respecting real communities is worth some inequality. That's the bargain: deviation is the currency, and you spend it to buy things like whole towns and sensible boundaries. Which is what makes Casing 4 pointed: the minority map spends 48% more of that currency than the majority — and Casing 1 shows it *didn't* buy Airdrie's wholeness with it.

Now re-read Casing 4: wider spread than 99 of every 100 neutral maps, on the one value the statute actually quantifies.

*The limit:* the law ranks nothing inside the band. "Spent more deviation" is an observation about priorities, not a violation — every district on both maps is legal. [Back to Casing 4](#casing-4)

### Appendix E — How a data artifact fooled us, and how it was caught {#appendix-e}

*The confusion:* "You published 15%, then said 72%. Why should I trust any of your other numbers?"

Because of *why* the number changed. Early in the audit, no official digital boundaries existed for the proposed maps — only PDF images in the commission's reports. The audit traced those images into approximate digital boundaries. Tracing is lossy: a boundary that actually runs along a city limit can end up drawn a few hundred metres off, and a metric that asks "does this border follow the municipal line?" then answers *no* for borders that really do. Multiply that across a whole map and you manufacture a dramatic, false signal. The day Elections Alberta released official shapefiles, the audit re-ran everything. Most findings survived. This one died, and was retracted in place — the corrections box below preserves it permanently.

Now re-read Casing 5: the retraction is not a stain on the method. It *is* the method — the same recomputation that killed this finding is what makes the surviving ones credible.

*The limit:* one honest retraction doesn't certify everything else; reproducibility does. Every surviving number can be regenerated from public data and public code, which is the only guarantee worth having. [Back to Casing 5](#casing-5)

### Appendix F — The what-if machine, and how to read a percentile {#appendix-f}

*The confusion:* "A million computer maps? A percentile of a simulation? What does that even mean?"

You can't judge whether a map is unusual without knowing what usual looks like — and for electoral maps, nobody gets to see the alternatives. So the audit built them. An algorithm starts from a legal map and makes a long chain of random legal edits: merge two neighbouring districts, re-split them a random valid way, repeat — 252,500 times over, in four independent chains, 1,010,000 maps in all. No vote data is consulted while drawing; the machine cannot favour anyone because it cannot see anyone. Then you take the real map, measure it, and ask: out of the million neutral maps, how many score this high? If 500,000 do, your map is ordinary. If 69 do, your map is the kind of map that neutral drawing produces 69 times in a million tries.

Now re-read Casing 6: the majority map at the 78th percentile — ordinary. The minority at the 99.99th — 69 matches in 1,010,000.

*The limit:* the machine respects population and contiguity but not every statutory nicety a real commission weighs, so its percentiles measure distance from *neutral drawing*, not from *everything a lawful commission might do*. And a percentile is a distance, not a verdict. [Back to Casing 6](#casing-6)

### Appendix G — The efficiency gap, in one worked example {#appendix-g}

*The confusion:* "One number that captures gerrymandering? That sounds too convenient."

It is, slightly — which is why it gets a threshold and a miss in this report. The idea: every vote that doesn't help win a seat is "wasted" — all votes cast for losers, plus winners' votes beyond the 50%-plus-one they needed. In a fair map both parties waste about equally. The efficiency gap is the difference in wasted votes, as a share of all votes. Suppose in a 100-vote district Orange wins 90–10: Orange wasted 39 (surplus beyond 51), Blue wasted 10 (all losers). Packed and cracked maps make one party waste systematically more. Positive gaps favour conservatives in this report's sign convention; the audit's Alberta calibration line (~4.1%) is the level only 5% of the million neutral maps cross.

Now re-read Casing 7: minority at +4.0%, 94th percentile — below the audit's own pre-registered line, reported as the miss it is.

*The limit:* the efficiency gap compresses a whole map into one number, and one number can't distinguish a gerrymander from geography being lumpy. That's why this audit uses four metrics and a locked threshold — and keeps the miss on the books. [Back to Casing 7](#casing-7)

### Appendix H — The prosecutor's fallacy, in plain language {#appendix-h}

*The confusion:* "One in 568,000 that this map is innocent. That's the finding, right?"

No — and the difference matters enough to have a name. The number says: *if* a neutral process drew Alberta's map, the chance it would look like the minority map is at most one in 568,000. That is P(this evidence, given innocence). It is not P(innocence, given this evidence) — and swapping them is the prosecutor's fallacy. Classic example: a suspect matches a DNA profile found at a scene, and the profile occurs in one in a million people. "One in a million chance he's innocent"? Wrong. In a city of ten million, about ten people match; on the DNA alone, the suspect is one of ten — a 90% chance *someone else* matches too. The rarity of the evidence under innocence is not the probability of innocence, because you also need to know how many innocent ways the evidence could arise.

Now re-read Casing 8: the audit states the number it can defend — the rarity of the map under neutral drawing — and refuses the swap that would turn it into a verdict.

*The limit:* refusing the fallacy costs the audit its most quotable sentence, and that cost is deliberate. Rarity is evidence. It is not, and never becomes, proof of intent. [Back to Casing 8](#casing-8)

### Appendix I — What a sampler is, and why swapping it matters {#appendix-i}

*The confusion:* "You checked your simulation with… another simulation? How is that a check?"

Because the two machines are built differently, and artifacts don't usually survive a change of machinery. Any map-drawing algorithm has quirks — the standard one (ReCom) has a documented lean toward compact, tidy districts, which could in principle exaggerate how extreme a sprawling real map looks. So the audit swapped the engine: a variant that grows districts from random spanning *forests* instead of trees, with measurably different internal behaviour, registered publicly (OSF he53s) before a single map was drawn with it, seeds derived from a public randomness beacon anyone can verify. If the minority's tail position were an artifact of the first engine's quirks, the second engine would move it. It moved less than one percentile point on every metric — a pre-registered ROBUST verdict. The audit also reports the check that *failed*: the claim that Act I's flagged geometry is the specific mechanism behind the seat numbers did not survive testing, and was dropped.

Now re-read Casing 9: three attacks, two survived, one claim honestly lost.

*The limit:* robustness rules out tooling artifacts. It cannot rule in design — a genuinely extreme map is genuinely extreme whatever produced it. [Back to Casing 9](#casing-9)

### Appendix J — Why neighbours voting alike breaks naive statistics {#appendix-j}

*The confusion:* "A test gave p = 0.0024 and you threw it away? That looks like hiding a result."

The opposite — it's correcting one. Many tests assume observations are independent, like separate coin flips. Voting areas aren't: neighbouring areas share demographics, incomes, histories — they vote alike. Treating 100 clustered areas as 100 independent flips is really more like 20 informative observations wearing 100 coats, and it makes coincidences look impossible when they're merely uncommon. The fix is to build a null that preserves the clustering — shuffle *blocks* of neighbouring areas together rather than each area separately — and ask the question again. The audit's swing-zone test looked significant under the naive null (p = 0.0024) and unremarkable under the corrected one (p ≈ 0.19). When the honest null disagrees with the flattering one, you keep the honest null and retire the result.

Now re-read Casing 10: two of the audit's own instruments retired, one pre-registered test the minority map outright passed.

*The limit:* the correction shows the *boundary-choice* signal doesn't stand — it says nothing against the ensemble findings, which never assumed independence in the first place. [Back to Casing 10](#casing-10)

### Appendix K — How to check a stated reason against public data {#appendix-k}

*The confusion:* "Commissioners are the experts. Who is an audit to grade their reasons?"

Nobody special — and that's the point: the check requires no special access. The minority report says Cochrane residents "move fluidly" into Calgary; Statistics Canada's journey-to-work tables (free, public) show about a third of Cochrane's workers commute into Calgary while roughly half work in Cochrane — a real tie, and one that says nothing about the specific Nolan Hill corridor drawn. The report implies shared schools link Red Deer and Sylvan Lake; the two towns' school-division boundaries (also public) put them in different divisions. Each check follows the same recipe: take the stated reason, find the public dataset that would show it, and see whether the *particular line drawn* is the line the data supports. Five of six checked rationales fail that last step — the tie is real, the line is not the one the tie points to.

Now re-read Casing 11 — and notice the audit retracted one of its own seven claims by the same standard, when the source couldn't be located.

*The limit:* a rationale that fails checking proves the *stated* reason doesn't fit. It cannot reveal the real one — sloppiness and pretext leave identical paperwork. [Back to Casing 11](#casing-11)

### Appendix L — How commissioners are appointed, and what nomination implies {#appendix-l}

*The confusion:* "Government-nominated commissioners drew the government-favouring map. Case closed, surely?"

Alberta's commission is built from nominations: a chair, plus commissioners nominated from government and opposition sides — a design that assumes partisan perspectives and balances them, betting that a mixed room converges on one defensible map. For decades the bet paid: commissions signed consensus reports. This cycle the room split along its nomination lines, and the government's nominees produced the statistical outlier. That correlation is real and worth recording. It is also exactly where the inference must stop. Nominated commissioners are not agents; no evidence in this audit's record shows the government directed, coordinated with, or even knew the shape of its nominees' map before filing. History is full of nominees who disappointed their nominators. The correlation invites a question — it cannot answer it, and the audit's instruments cut against the chair's side too when the data went that way, which is what symmetric measurement means.

Now re-read Casing 12: the split is the anomaly; the provenance is the question mark, not the answer.

*The limit:* appointment provenance is context, never proof. Treating it as proof is the same fallacy as Appendix H, wearing a political coat. [Back to Casing 12](#casing-12)

### Appendix M — The Act's process, commission to committee, end to end {#appendix-m}

*The confusion:* "How can the legislature just… take over redistricting? Isn't the commission's map the map?"

No — and this is the load-bearing surprise of the whole episode. Under Alberta's *Electoral Boundaries Commission Act*, the commission proposes; only the Legislative Assembly disposes. The commission's final report — hearings, submissions, revisions and all — is advice. It has no legal effect until the Assembly enacts a map, and the Act places almost no constraints on what the Assembly does instead: no minimum debate, no notice period, no obligation to prefer the commission's work, no hearing requirement for whatever process follows. Section 12 lets the Assembly refer the work onward — which is what Motion 19 did, to a select committee. Select committees of the Assembly are composed of MLAs; independence was excluded by the choice of vehicle itself, lawfully. Every previous cycle, the Assembly's restraint — not the statute — was what kept politicians' hands off the pen.

Now re-read Casing 13: sixteen communities of hearings replaced by a body required to hold none. All of it inside the Act.

*The limit:* this appendix explains what the law permits. Whether what the law permits is what Albertans should accept is a political question — the one the November tests are built to inform. [Back to Casing 13](#casing-13)

### Appendix N — Conventions versus law, and how norms erode {#appendix-n}

*The confusion:* "If politicians drawing their own districts violates our deepest electoral norm, how can it be legal?"

Because Canada's constitution runs on two operating systems. One is law: written, justiciable, enforced by courts. The other is convention: unwritten rules of political behaviour — binding in practice, invisible to a courtroom. The Supreme Court described the divide in the 1981 Patriation Reference: courts may *recognize* a convention and will still decline to *enforce* it, because conventions are policed politically — by opposition, press, and voters — not judicially. Independent boundary commissions live on the convention side. Sixty years of practice, in every province and federally, built the rule that politicians do not draw their own ridings; no statute anywhere makes that rule mandatory. Which means the guardrail's entire strength was that governments kept choosing to honour it. A norm violated once, without consequence, is weaker for every government that follows — of any party.

Now re-read Casing 14: real violation, fully documented, judicially irrelevant — all three at once.

*The limit:* "unenforceable" is a statement about courts, not about consequences. Conventions are enforced at elections, by people who know what was done. Reports like this one exist so they know. [Back to Casing 14](#casing-14)

---

## References & Methodology

While this report summarizes the audit for a general audience, the underlying methodology relies on established political science and legal literature on electoral boundary design. Key references include:

* **Chen, Jowei, and Jonathan Rodden. 2013.** "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269. (Establishes the framework for evaluating how "natural packing" of urban voters interacts with neutrally drawn boundaries).
* **Courtney, John C. 2001.** *Commissioned Ridings: Designing Canada's Electoral Districts*. Montreal and Kingston: McGill-Queen's University Press. (The foundational text on the history and structural norms of independent Canadian boundary commissions).