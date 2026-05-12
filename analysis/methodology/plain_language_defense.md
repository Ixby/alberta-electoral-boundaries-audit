# Plain-Language Defense — Alberta Electoral Boundaries Audit

**Purpose.** This document interrogates every substantive assertion in the academic audit monograph (`outputs/academic_report/report_academic.md`) with the questions a reader who knows nothing about elections, statistics, or political science would ask. It is organized by the report's section headings. Each entry follows this format:

> **Assertion:** The claim, paraphrased if needed.
> **Why?** The naive question a reader with no domain background would ask.
> **Answer:** A plain-language explanation. No jargon. No assumed knowledge. Self-contained.

Jargon is translated throughout: "efficiency gap" means a measure of how many votes each side wastes unequally; "MCMC ensemble" means a computer simulation that draws thousands of random legal maps; "p-value" means the probability of seeing a result this extreme just by chance; "p95" means a value that 95% of the random maps fall below.

---

## Executive Summary

---

**Assertion:** Alberta's 2025–26 Electoral Boundaries Commission produced two competing 89-seat maps on March 23, 2026.
**Why?** What is an Electoral Boundaries Commission and why would it produce two different maps?
**Answer:** Every few years, a province must redraw the boundaries of the geographic areas — called electoral districts or ridings — that each send one elected representative to the legislature. In Alberta, this is done by an independent commission appointed under provincial law. In 2026 the commission's members could not agree: some members proposed one set of 89 district boundaries (the majority proposal) and other members proposed a different set (the minority proposal). Both were submitted to the legislature.

---

**Assertion:** The audit evaluates both proposals using identical methods applied symmetrically to each.
**Why?** Why does it matter that the same method is used on both maps?
**Answer:** If the audit used different tests on each map, it would be easy to make one map look bad simply by choosing tests that happen to penalize it. Applying exactly the same measurements to both maps means any difference found is a real difference between the maps, not an artifact of a biased testing procedure.

---

**Assertion:** The majority map is within the neutral statistical band on every partisan-fairness metric. The minority map is not.
**Why?** What is a "neutral statistical band" and how do you know the majority map is inside it while the minority is outside?
**Answer:** To judge whether a map is unusual, the audit ran a computer simulation that randomly drew over one million legal Alberta maps — maps that follow all the same rules the commission was required to follow (equal population, connected districts, and so on). Those million random maps form a reference band: the range of outcomes you would expect from an unbiased process. The majority map's scores on every fairness measure fall comfortably inside that range. The minority map's scores on several measures fall outside it — meaning they are more extreme than all but a tiny fraction of the randomly drawn neutral maps.

---

**Assertion:** The minority proposal differs from the majority on four measurable non-partisan-bias dimensions: population dispersion (Median Absolute Deviation 48% wider), Calgary geographic-zone asymmetry (12.2% vs 0.4%), Airdrie community fragmentation (4-way vs 2-way split), and commission-chair-flagged geographic anomalies (3 confirmed vs 0).
**Why?** What do these four things mean and why do they matter?
**Answer:** Population dispersion measures how unevenly people are distributed across districts: if some districts have far more residents than others, some citizens' votes count more than others'. A "Median Absolute Deviation" 48% wider means the minority map's districts vary more in size than the majority's do. The Calgary zone gap means districts inside Calgary's urban core are sized differently from those in Calgary's suburban ring — an imbalance that tilts which party's voters are packed more tightly. Splitting Airdrie four ways means the city's residents are divided among four different ridings and lose the collective political voice they would have in one or two. The chair-flagged anomalies are boundary shapes that the commission's own chair publicly criticized as geographically strange.

---

**Assertion:** A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation; both maps fall within the 70–85% Canadian comparator norm.
**Why?** What happened here — why is a finding being withdrawn?
**Answer:** Earlier in the audit, before Elections Alberta released its official map files, the researchers worked from approximate boundary tracings made from PDF images. Those approximate boundaries suggested the minority map ignored city and town edges far more than the majority did. When the official map files arrived and the same measurement was rerun on those exact files, both maps turned out to respect municipal boundaries at rates (72% and 80%) that are normal for Canadian redistricting. The earlier finding was a measurement artifact from the approximate files, not a real difference between the maps. The audit discloses this openly rather than hiding it.

---

**Assertion:** Two independent statistical tests — the ensemble test (Mahalanobis Ch1) and the boundary-choice test (SZAT Ch2) — return the same answer. Their Fisher combination is p = 6.87×10⁻⁸.
**Why?** What do "Ch1" and "Ch2" mean, what is a "Fisher combination," and what does p = 6.87×10⁻⁸ mean in plain terms?
**Answer:** Ch1 (the ensemble test) asks: how unusual is this map compared to over one million randomly drawn neutral maps? Ch2 (the boundary-choice test) asks: in the specific places where the minority map differs from the majority map, are those differences random or do they consistently move in a direction that favors one party? The Fisher combination is a standard mathematical formula for merging two independent test results into one overall probability. The combined result of p = 6.87×10⁻⁸ means: if there were truly no pattern, you would only get test scores this extreme by coincidence about once in every 15 million tries. That is an extremely unlikely accident.

---

## Abstract

---

**Assertion:** This audit evaluates both proposals against the 2019 baseline using a multi-method structural framework and Monte Carlo ensemble analysis.
**Why?** Why compare to 2019, and what is "Monte Carlo ensemble analysis"?
**Answer:** The 2019 map is the most recent map that was actually used in an election, so it serves as the reference point for what Alberta's districts looked like before any changes. A Monte Carlo ensemble analysis is the process of using a computer to draw thousands or millions of random legal maps and recording their properties — it answers the question "what does a normal, unbiased map look like?" by showing you the full range of possibilities.

---

**Assertion:** A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation (both maps within the Canadian comparator norm); full reconciliation in §5.8.5.
**Why?** What does "pre-registered" mean and why does it matter that this finding failed?
**Answer:** Pre-registration means declaring in advance — before looking at the data — exactly what you plan to test and what threshold would count as a finding. This prevents researchers from quietly dropping tests that do not confirm their hypothesis (a practice called "p-hacking"). When a pre-registered test fails, it must be reported honestly. In this case the test was declared in advance on a public registry, the finding did not hold up when better data arrived, and that failure is reported in full — not hidden.

---

**Assertion:** The joint outlier profile reaches Mahalanobis p = 1.40×10⁻⁶ against the 1,010,000-plan canonical ensemble.
**Why?** What is a "Mahalanobis" score and what does 1.40×10⁻⁶ mean?
**Answer:** A Mahalanobis score is a way of measuring how far a single data point is from the center of a cloud of data points, while accounting for how correlated those dimensions are with each other. Here it measures how far the minority map's combination of four partisan fairness scores sits from the center of the cloud formed by over one million randomly drawn maps. A probability of 1.40×10⁻⁶ means that roughly 1.4 maps in every million drawn at random would be this extreme — in other words, the minority map is more extreme than approximately 999,998 out of every million neutral maps.

---

**Assertion:** All Efficiency Gap magnitudes remain below the Stephanopoulos-McGhee 7% threshold (academic literature only; never judicially adopted).
**Why?** What is the Efficiency Gap, what is this 7% threshold, and why does it matter that courts have not adopted it?
**Answer:** The Efficiency Gap is a measure of how many votes each party "wastes" — votes cast for a losing candidate, plus votes cast for a winning candidate beyond the minimum needed to win. If one party wastes far more votes than the other, that is a sign the map is drawn to their disadvantage. The 7% threshold is a benchmark from academic research suggesting that gaps above 7% are likely to persist across election cycles. Courts in Canada have never declared any specific number as a legal test, so this 7% is informative as a reference but does not by itself determine any legal outcome.

---

## Preface — Scope, Shapefile Status, and Intended Venue

---

**Assertion:** Elections Alberta released the 2026 official shapefile package and the canonical polygon files were received by the audit on 2026-05-06.
**Why?** What is a shapefile and why does it matter when it was received?
**Answer:** A shapefile is a digital file that stores the exact geographic coordinates of boundaries — in this case, the precise lines defining every electoral district. Without the official shapefiles, earlier analysis had to use approximate boundary tracings from images. When the official files arrived, several measurements were rerun to confirm the earlier results. Knowing the exact date matters for establishing that the analysis using official files was done after those files arrived — not that the researchers somehow had access before the public release.

---

**Assertion:** The DPG-substrate runs documented in §5.4.1–§5.4.8 are preserved as the historical record of the pre-shapefile analysis.
**Why?** What are "DPG-substrate runs" and why keep the old results at all?
**Answer:** DPG (Derived Provisional Geometries) refers to approximate boundary tracings made from scanned PDF images of the commission's maps, used before the official digital files were available. The simulation runs performed using those approximate shapes are the pre-shapefile analysis. They are kept in the report because transparency requires showing the full history of the work — including what the analysis showed before and after the better data arrived — so that readers can see whether and how results changed.

---

**Assertion:** The November 2026 committee-map trigger remains pending.
**Why?** What is a "committee-map trigger"?
**Answer:** After the commission's reports were set aside, the Alberta legislature created a Special Select Committee to draw a new 91-seat map by November 2026. The audit pre-registered a commitment to evaluate that map using the same methodology as soon as it is published. The "trigger" is simply that planned rerun, which cannot happen until the committee releases its map.

---

## Author Disclosure

---

**Assertion:** Going into this project the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny.
**Why?** Why admit a bias up front — doesn't that undermine the research?
**Answer:** Every researcher comes to a project with existing beliefs. Admitting those beliefs openly is more credible than pretending to have none, because it lets readers assess whether the methodology was designed to confirm the prior or to test it fairly. The disclosure also sets up the three cases where findings ran against the researcher's prior expectations — showing the method produced results the researcher did not expect or want.

---

**Assertion:** Three cases surfaced findings that ran against the prior and were retained in the report: the partisan-bias asymmetry reverses sign under 2019 vote input; the commission chair's "no public support" claim is upheld on three of seven configurations, not all seven; and the majority map's own MAD is tighter than the 2019 baseline.
**Why?** Why does it matter that some findings went against the researcher's expectations?
**Answer:** A biased research process would quietly drop inconvenient results. These three contra-prior findings were retained precisely to show that the methodology is not rigged. If every single finding had confirmed the researcher's starting suspicion, that would be a red flag. Results that cut against the prior — and are reported anyway — provide evidence that the method is operating independently of the researcher's preferences.

---

**Assertion:** Three large language models were used as analytical and writing assistants (Claude Pro Max, Gemini Pro, Codex). All substantive claims were verified against primary sources by the author.
**Why?** Does using AI tools make the analysis less reliable?
**Answer:** AI tools were used the way a researcher might use a calculator or a grammar checker — to help draft text, identify inconsistencies, and suggest analytical approaches. The audit explicitly states that no AI tool executed code or independently accessed data. Every number was verified by the researcher against the original data files and script outputs. The AI's role was assistance, not decision-making.

---

**Assertion:** No traditional statistical software (R, Stata, SPSS), no GIS desktop software (QGIS, ArcGIS), and no commercial election-analytics platforms were used. All inputs are public.
**Why?** Why does it matter what software was used?
**Answer:** Commercial or proprietary software can make research harder to reproduce because other researchers may not have access to it. Using only open-source Python tools means anyone with a standard computer can run the same code against the same publicly available data and check that the numbers are correct. This is the practical meaning of "reproducible" in this context.

---

## §1 Introduction

---

**Assertion:** The audit is the first systematic computational audit of an Alberta provincial electoral boundary commission's output, evaluated against established Canadian independent-commission practice and statutory norms.
**Why?** Has no one done this kind of analysis before?
**Answer:** Computational tools for measuring partisan fairness in redistricting — especially the MCMC (random-map simulation) approach — have been developed primarily in the United States over the last decade. In Canada, there is an academic literature on boundary commission discretion but systematic computational auditing of commission outputs using neutral-ensemble comparison is new to the Alberta provincial context. This audit is the first to apply those tools to an Alberta provincial map.

---

**Assertion:** The audit situates itself within Canadian political-science and legal frameworks: the Saskatchewan Reference's "effective representation" standard.
**Why?** What is the Saskatchewan Reference?
**Answer:** The Saskatchewan Reference is a 1991 Supreme Court of Canada decision ([1991] 2 SCR 158) that established the constitutional standard for electoral boundaries in Canada. The court ruled that the goal is "effective representation" — meaning that districts should be roughly equal in population, but some variation is allowed when necessary to accommodate communities of interest, geographic factors, and other considerations. Every assertion in this audit about whether a boundary choice is legally defensible is measured against that standard.

---

**Assertion:** The audit asks whether one faction's boundary choices within a Canadian independent commission exceed the discretion space that Canadian law and practice establish — not whether a full gerrymander occurred.
**Why?** What is the difference between asking "did this exceed discretion" versus "is this a gerrymander"?
**Answer:** A full gerrymander is a conclusion about intent and effect — that a map was deliberately drawn to entrench one party's power. This audit does not make that legal conclusion and does not infer intent. Instead it asks a narrower empirical question: do the measurable properties of this map fall within the range that Canadian law and neutral random processes would produce? That is a question the data can answer. Whether those deviations constitute an illegal gerrymander is a legal judgment that courts would need to make.

---

**Assertion:** Computational seeds were committed to the public drand League of Entropy beacon before the official shapefile release.
**Why?** What is a "drand beacon" and why does committing seeds to it before seeing the data matter?
**Answer:** A random seed is the starting number that determines every subsequent "random" choice a computer makes in a simulation. Cloudflare's drand beacon is a public, cryptographically verifiable source of random numbers that are published on a fixed schedule and cannot be altered retroactively. By recording which seed was used on the public beacon before the official maps arrived, the audit proves it could not have run the simulation multiple times with different seeds and selected the one that produced the most extreme result — a form of cheating called "fishing." The beacon acts as a tamper-proof timestamp.

---

**Assertion:** Five pre-registration IDs are cited: OSF w2s8k, r3zm7, qsgy8, 6pt83, s58a6.
**Why?** What is OSF pre-registration and what does citing these IDs prove?
**Answer:** OSF (Open Science Framework) is a public registry where researchers can file a detailed plan for a study before running it — specifying in advance what they will measure, what thresholds will count as a finding, and what data they will use. The plan is timestamped by OSF and cannot be changed. Citing the OSF IDs lets any reader look up those registrations and verify that the tests were designed before the analysis was done, not designed afterward to match results the researcher had already found.

---

**Assertion:** Primary ensemble-based tests (Ch1, Ch2, Fisher combination) are exploratory, not confirmatory.
**Why?** What is the difference between exploratory and confirmatory statistics?
**Answer:** Confirmatory statistics follow a pre-registered plan written before data collection, where the specific test, threshold, and significance level are all locked in advance. Exploratory statistics are open-ended: they explore patterns in data without a pre-registered threshold. The distinction matters because exploratory results can be influenced by choices made after seeing the data, even unintentionally. The audit is honest that Ch1, Ch2, and their combination are exploratory — the seeds were locked but the specific test names and combination formula were not in an OSF pre-registration. That means the results should be treated as strong but requiring independent replication before drawing firm conclusions.

---

### §1.1 Headline Findings in Plain Language

---

**Assertion:** The minority map's Median Absolute Deviation from provincial average is 4,707 versus the majority's 3,180 — a 48% wider dispersion.
**Why?** What is "Median Absolute Deviation from provincial average" and why does wider dispersion matter?
**Answer:** The provincial average is the number of residents that each electoral district would have if the population were split perfectly equally. The Median Absolute Deviation measures the typical gap between each individual district's population and that average — a higher number means districts are more unequal in size. At 4,707 versus 3,180, the minority map's districts vary from the provincial average by about 48% more than the majority's districts do. When districts are unequal in size, votes in smaller districts carry more weight than votes in larger districts.

---

**Assertion:** The minority map's Calgary districts show a 12.2 percentage-point geographic-zone asymmetry versus 0.4 pp on the majority map.
**Why?** What does "geographic-zone asymmetry" mean here?
**Answer:** Calgary's electoral districts can be divided into two zones: the urban core (central city neighborhoods) and the suburban ring (newer outer neighborhoods). If the two zones have the same average district size, they contribute equally to electing representatives. If one zone's districts are systematically smaller, voters there elect more representatives per person than voters in the other zone. The minority map shows a 12.2-percentage-point gap between these zones; the majority map shows only a 0.4-point gap. This matters because urban-core neighborhoods in Calgary lean toward one party and suburban-ring neighborhoods lean toward the other.

---

**Assertion:** The minority map splits the City of Airdrie four ways; the majority concentrates 73.8% of Airdrie's population inside a single electoral division (Airdrie-East).
**Why?** Why is splitting a city across more electoral districts a problem?
**Answer:** When a city's residents are spread across many different electoral districts, no single representative is primarily accountable to that city. Residents of Airdrie who are divided across four districts have to share their representative with people from other communities who may have different interests. The majority map, by keeping nearly three-quarters of Airdrie residents in one district, gives that city a clearer political voice. The specific concern is that splitting a community can dilute its voting power — a technique called "cracking" in electoral analysis.

---

**Assertion:** One minority district ("Calgary-Foothills-Airdrie West") carries "Airdrie" in its name but has 0% anchoring on Airdrie's gazetted city limit.
**Why?** What does it mean for a district boundary to have 0% anchoring on a city limit?
**Answer:** A district boundary is "anchored" on a city limit if a portion of the district's edge runs along the official municipal boundary. A district named after a city that shares none of its border with that city's official edge is drawing in residents from a different area entirely — suggesting the "Airdrie" label is not reflecting any real geographic connection to Airdrie as a municipality.

---

**Assertion:** Three geographic anomalies on the minority map were flagged by the commission chair; zero were flagged on the majority map.
**Why?** Who is the commission chair and what gave them authority to "flag" boundaries?
**Answer:** The commission chair is the presiding officer appointed to lead the boundary commission. The chair's written criticisms, documented in the commission's own majority report, identify specific minority map features as geographically unusual or inconsistent with the commission's stated principles. The chair is not a neutral outsider — they are one of the commission's own members. Their documented criticism of minority-map features, contained in the official commission report, is a primary-source record of internal expert concern.

---

**Assertion:** The minority's own 25 published rationales are, on five of six contested configurations, options the minority did not take when cleaner statutory-compliant alternatives were available.
**Why?** What does "cleaner statutory-compliant alternatives" mean?
**Answer:** When a commission draws a boundary that looks unusual, it is expected to explain why in writing. The minority commissioners published rationales for their boundary choices. For five of the six configurations examined, the audit identifies a simpler boundary option — one that would also satisfy the law — that the minority could have chosen but did not. "Cleaner" here means fewer geographic contortions, more direct alignment with city or town edges. The argument is that if the stated rationale were genuinely driving the choice, the simpler alternative would have been chosen.

---

### §1.2 Modelling-Uncertainty Caveats

---

**Assertion:** Monte Carlo sensitivity interval over modelling choices is [−3.04, +0.76] pp and crosses zero.
**Why?** What is a "Monte Carlo sensitivity interval" and what does "crosses zero" mean?
**Answer:** This interval comes from running the efficiency-gap calculation 2,000 times while randomly varying the assumptions built into the vote-attribution model (how votes from some mixed urban-rural districts are estimated). The result is a range of plausible efficiency-gap differences between the two maps. An interval of [−3.04, +0.76] pp means that across those 2,000 variations, the result ranges from −3.04 percentage points to +0.76 percentage points. "Crosses zero" means some of those 2,000 runs show the minority as slightly better for the NDP rather than better for the UCP. This means the magnitude of the partisan-bias estimate is uncertain enough that classical statistical significance — where you need 95% of the range on one side of zero — is not met on the efficiency gap.

---

**Assertion:** Direction consistency: 90.5% of samples show minority more UCP-favorable. Classical 95% significance is not defensible.
**Why?** What is the difference between 90.5% direction consistency and 95% classical significance?
**Answer:** Classical statistical significance in this context means that 95% of your uncertainty range would need to favor the same conclusion — that the minority map consistently advantages the UCP. At 90.5%, roughly 9 in 10 of the simulated parameter sets point the same direction, but about 1 in 10 do not. That is a strong directional signal but falls short of the conventional threshold. The audit reports it honestly as a "defensible directional claim" rather than overstating it as a definitive finding.

---

**Assertion:** Declination metric disagrees with the efficiency gap: by declination, the minority is the least pro-UCP of the three maps.
**Why?** Why would two different fairness measures point in opposite directions?
**Answer:** The efficiency gap and declination are two different mathematical formulas designed to capture partisan unfairness, but they capture it differently. The efficiency gap is sensitive to how many votes are "wasted" (lost or excess); declination is sensitive to how the slopes of two trend lines in election-outcome data differ between the two parties. These different sensitivities mean they can give conflicting signals when the map's distortion takes an unusual form. Research by Warrington (2018) documents that this kind of cross-metric disagreement is expected — it is a known feature of how these measures work, not a sign of an error. The audit retains both measures rather than picking the one that tells a cleaner story.

---

**Assertion:** Under v0_8 full-coverage area-proportional attribution, the direction is stable across 2019 and 2023 votes. The earlier "direction reverses" reading was a partial-coverage artifact of 22 unattributed rural EDs.
**Why?** What happened with the 22 rural districts and why did fixing them matter?
**Answer:** Vote attribution means assigning 2023 election results to the new proposed district boundaries. In an earlier version of this process (v0_7), 22 rural electoral districts did not get their votes correctly allocated because of incomplete geographic overlap data. Those missing UCP votes made the rural districts appear more NDP-friendly than they really were, which reversed the apparent direction of the efficiency gap. When a corrected method (v0_8) was used that properly attributed all districts, the partisan direction stabilized — both maps remained UCP-favorable under both 2019 and 2023 votes, though the inter-map gap between them does still shift between years.

---

## §2 Background

---

**Assertion:** The *Electoral Boundaries Commission Act* (EBCA) sets a ±25% population deviation window (§14).
**Why?** What does a ±25% population deviation window mean and who decided it should be 25%?
**Answer:** The EBCA is the Alberta law governing how electoral boundaries are drawn. Section 14 says that no district can have a population more than 25% above or more than 25% below the provincial average district size. This creates a legal boundary: a district with a population below 75% or above 125% of the average would be illegal. The 25% figure is set by the legislature, not by the commission or by this audit.

---

**Assertion:** Section 15(2) allows up to −50% deviation if at least 3 of 5 geographic criteria are met.
**Why?** Why is there a special exception allowing districts to be even smaller?
**Answer:** Alberta includes remote northern and mountain regions where communities are separated by vast distances, sparse road networks, and difficult terrain. A district covering a huge geographic area might need to have fewer residents than average in order to be representable by a single elected member — it would be impossible to travel to every community in a normal campaign or year. The law allows these sparsely populated districts to go up to 50% below the average if the geography justifies it, provided at least three of five specified geographic criteria (such as area, isolation, or transportation access) are met.

---

**Assertion:** All six invocations of the s.15(2) exception across both maps pass under corrected thresholds.
**Why?** What are these "six invocations" and what were they being checked against?
**Answer:** Six of the proposed districts — across both the majority and minority maps — invoke the §15(2) geographic exception to fall below the standard ±25% band. The audit checked whether each of those six districts genuinely meets the minimum three-of-five criteria the law requires. After correcting an earlier threshold calibration error, all six pass the test. This means neither map is improperly using the geographic exception as a cover for creating unfairly small districts.

---

**Assertion:** The *Saskatchewan Reference* ([1991] 2 SCR 158) established "effective representation" as the constitutional standard.
**Why?** How does a 1991 Saskatchewan case govern what Alberta's commission can do?
**Answer:** The Supreme Court of Canada's decisions on constitutional questions apply to all provinces. In the Saskatchewan Reference, the court interpreted section 3 of the Canadian Charter of Rights and Freedoms — the right to vote — as requiring "effective representation" rather than strict numerical equality. That means provinces can draw districts that vary in population, as long as the variation serves legitimate goals like accommodating remote communities or preserving communities of interest. Alberta's commission is bound by this standard when making its choices.

---

**Assertion:** Rucho v. Common Cause (US) established non-justiciability in US federal courts — contrasted with Canadian justiciability.
**Why?** Why is an American Supreme Court case mentioned in an audit of an Alberta provincial commission?
**Answer:** Rucho v. Common Cause is a 2019 US Supreme Court decision holding that federal courts in the United States cannot rule on partisan gerrymandering claims because those are "political questions" outside judicial competence. This is mentioned as a contrast: in Canada, courts can and do assess whether boundary commissions have met their constitutional obligations under the Charter. The Canadian system is justiciable — meaning courts can hear these cases — where the US federal system is not. Readers familiar with US redistricting news should not assume that what is legally unreviewable in the United States is equally unreviewable in Canada.

---

## §3 Data

---

**Assertion:** The 2023 Statement of Vote has 1,973 poll records across 87 sheets in an Excel workbook.
**Why?** What is a "Statement of Vote" and why does the number of poll records matter?
**Answer:** The Statement of Vote is the official Elections Alberta publication of every ballot result from the 2023 provincial election, broken down by polling station. Each polling station is one "poll record." The 1,973 records from 87 worksheets represent the full granular record of where votes were cast and for whom. Using poll-level data rather than district-level totals allows the audit to estimate how votes from one district's boundaries would be reassigned if those boundaries moved — which is essential for comparing the old map to the new proposed maps.

---

**Assertion:** Three-vintage sandwich: 2019 enacted boundaries, 2021 Census population, 2023 election results.
**Why?** Why are three different years involved and does that create problems?
**Answer:** The three datasets come from different points in time and do not perfectly align. The 2019 boundaries are the current districts used in the 2023 election. The 2021 Census is the population count the commission used to design the new districts. The 2023 election results are the most recent vote data. Combining them requires making assumptions — for example, which 2023 poll records fall within which new proposed boundaries. The audit documents these assumptions explicitly and tests the sensitivity of results to different choices.

---

**Assertion:** Vote Anywhere (VA) polling stations are treated as a data-quality concern requiring special handling.
**Why?** What are Vote Anywhere stations and why are they a problem?
**Answer:** Under Elections Alberta's Vote Anywhere program, voters can cast their ballot at any polling station in the province, not just the one assigned to their home address. This means some polling stations have votes from people who live in many different districts. Including those votes in a geographic analysis as if all voters came from the station's location would introduce errors. The audit identifies 2,110 Voting Areas that appear in one map but not the other, specifically because of how the two maps handle these boundary areas.

---

**Assertion:** Under v0_8 full-coverage area-proportional attribution, all 87 districts are attributed.
**Why?** What is "area-proportional attribution" and why did 22 districts fail under the earlier version?
**Answer:** Area-proportional attribution is a method of estimating how many votes from each polling station would fall within a new district boundary by using the geographic overlap between the old polling area and the new district. If the polling area is 60% inside the new district, it attributes 60% of that station's votes to the new district. Under the earlier v0_7 method, 22 rural districts had incomplete geographic overlap data, leaving their votes unattributed and skewing the results. Version v0_8 fixed that gap.

---

**Assertion:** The 338Canada April 2026 polling reading remains supportive of the 2023 asymmetry direction.
**Why?** What is 338Canada and why is polling data used in an audit of geographic boundaries?
**Answer:** 338Canada is a Canadian electoral forecasting website that aggregates polling data to estimate seat outcomes. The audit uses its April 2026 riding-level estimates as a cross-check — a third vote-input source beyond the 2019 and 2023 historical election results — to test whether the directional conclusion about the two maps holds up even with a different estimate of current voter preferences. The fact that all three vote inputs point the same direction strengthens the directional claim.

---

## §4 Methods

---

### §4.1 Falsifiability Gates and Pre-registration

---

**Assertion:** Every new test must have a null hypothesis, pass/fail threshold, and predicted direction documented in an OSF registration before data is examined.
**Why?** What is a null hypothesis and why does the order of operations matter?
**Answer:** A null hypothesis is the "no effect" baseline — for example, "the two maps are equally extreme in their partisan properties." Specifying the null hypothesis, the threshold for calling a result a "finding," and the expected direction before looking at the data prevents the researcher from unconsciously designing tests after seeing which ones give interesting results. If you look at data first and then decide what counts as significant, you are likely to find patterns that are really just noise. Pre-registration forces discipline by locking those choices before any data is examined.

---

**Assertion:** Gates G0–G5 are built into the pipeline as falsifiability gates.
**Why?** What are these gates and why "falsifiability"?
**Answer:** Falsifiability is the requirement that a scientific claim be testable — that there be some possible observation that could prove it wrong. The G0–G5 gates are explicit checkpoints built into the analysis code: if certain conditions are not met (for example, if simulation convergence fails), the pipeline halts and flags the finding as unreliable rather than proceeding. These gates make the audit falsifiable in practice, not just in principle.

---

### §4.2 MCMC Ensemble

---

**Assertion:** The canonical ensemble uses 1,010,000 plans across 4 chains × 252,500 steps, base seed 1432864451.
**Why?** Why 1,010,000 plans specifically, and what is a "chain"?
**Answer:** A chain is one continuous sequence of randomly generated maps, where each new map is created by making a small modification to the previous one. Running four independent chains reduces the risk that all maps happen to cluster around one particular type of solution. Each chain ran for 252,500 steps, producing a total of 1,010,000 maps (4 × 252,500). One million maps is considered more than sufficient for reliable statistical estimates; 1,010,000 is the exact count from 4 chains each completing 252,500 steps.

---

**Assertion:** The ReCom (Region Combining) algorithm draws legally valid maps by merging and re-splitting adjacent districts.
**Why?** How does the computer draw legally valid maps?
**Answer:** ReCom works by randomly selecting two neighboring districts, combining them into one large area, and then drawing a new boundary through that combined area to create two new districts. Each step randomly re-draws one boundary pair while leaving all other district boundaries the same. Because every step starts from a valid map and produces a valid map (both output districts satisfy contiguity and approximate population rules), every map in the chain is guaranteed to be legally valid. Over many steps this explores the full space of legal possibilities.

---

**Assertion:** Gelman-Rubin R̂ values are 1.007–1.017 on the final canonical run, indicating convergence.
**Why?** What is a Gelman-Rubin value and what does convergence mean here?
**Answer:** Gelman-Rubin R̂ is a diagnostic that compares variation within each chain to variation between chains. If the four chains are all exploring the same landscape (converging on the same distribution of maps), R̂ is close to 1.0. Values above 1.1 are typically a warning sign that the chains have not converged. Values of 1.007–1.017 are very close to 1.0 and indicate that all four chains are sampling from the same distribution — the simulation has stabilized and the results are reliable.

---

**Assertion:** Effective Sample Size (ESS) is 1,429–1,682 on canonical 1M partisan metrics — described as publication-grade.
**Why?** What is an Effective Sample Size and why does "1,429–1,682" matter when you have 1,000,000 total samples?
**Answer:** In a simulation where each new map is based on the previous one, consecutive maps are correlated — they are not fully independent observations. The Effective Sample Size adjusts the total sample count downward to reflect how much independent information is actually present. An ESS of 1,429–1,682 out of 1,000,000 total steps means the chain has about 1,400–1,700 truly independent observations. That is still more than enough for reliable percentile estimates; comparable published ensemble studies use similar or lower ESS values, which is why this is described as meeting publication standards.

---

### §4.3 Partisan Bias Metrics

---

**Assertion:** Four partisan metrics are used: Efficiency Gap, Mean-Median Gap, Declination, and Seats at 50/50.
**Why?** Why are four different measures needed instead of just one?
**Answer:** Each of these measures captures a different aspect of partisan fairness, and each has known blind spots. The Efficiency Gap (wasted votes) can be distorted by landslides. The Mean-Median Gap (distributional skew in vote shares) is robust to landslides but misses certain packing patterns. Declination (angular asymmetry of win margins) is sensitive to how broadly wins are distributed. Seats at 50/50 (projected outcome in a tied election) captures an overall advantage not always visible in single-metric scores. Using all four provides a fuller picture and reduces the chance that any one metric's blind spot hides a real pattern.

---

**Assertion:** Alberta efficiency gap convention: negative = UCP advantage, positive = NDP advantage.
**Why?** Why does the sign convention matter and why is it mentioned explicitly?
**Answer:** The sign of the efficiency gap can be defined either way — some researchers define negative as favoring one party, some define it the other way. The audit explicitly states its convention so readers know which direction positive and negative point. Without this declaration, a reader could misinterpret a positive value as a finding favorable to the NDP when it is actually unfavorable. The §5.4 MCMC sections use a different sign convention (positive = UCP-favoured) for historical reasons, so readers must track which section uses which definition.

---

### §4.4 SZAT (Swing-Zone Allocation Test)

---

**Assertion:** SZAT examines only the 2,110 Voting Areas assigned differently between the two proposals.
**Why?** Why look only at the places where the two maps differ?
**Answer:** If you compare the full partisan score of the minority map to the full score of the majority map, you cannot tell whether the difference comes from intentional partisan line-drawing or from geography that both maps share. By looking only at the 2,110 geographic units that one map gives to one district and the other map gives to a different district, SZAT isolates the partisan effect of the specific choices the minority commissioners made. Everything the two maps share is differenced out; only the contested boundary decisions remain.

---

**Assertion:** SZAT p = 0.0024.
**Why?** What does p = 0.0024 mean for the boundary-choice test?
**Answer:** If the specific boundary choices in the minority map were politically neutral — if the 2,110 differently assigned geographic units were drawn randomly without any partisan intent — you would expect the partisan lean of those units to be roughly balanced. A p-value of 0.0024 means that a random redistribution of those same units would produce as extreme a partisan imbalance only about once in every 400 tries. That is a very unlikely outcome from a neutral process.

---

### §4.5 No Legal Conclusion or Intent Inference

---

**Assertion:** The audit records what the data show; it does not reach a legal conclusion and does not infer intent.
**Why?** Why can the audit measure partisan effects but not say whether it was intentional?
**Answer:** Measuring whether a map's statistical properties fall outside the range of neutral maps is an empirical question the data can answer. Concluding that a specific person or group intentionally drew the map to favor one party is a legal and factual judgment that requires evidence about what those people were thinking and whether they acted with improper purpose. Statistical outliers can occur without improper intent, and intentional manipulation can occur at levels too subtle to detect statistically. The audit makes the empirical measurement but leaves the legal conclusion to courts or other institutional processes with the authority and evidence to make it.

---

### §4.6 Packing and Cracking Thresholds (P1 and P2)

---

**Assertion:** P1 threshold: +5% of provincial mean — one-fifth of the ±25% statutory band.
**Why?** Where does the 5% figure come from?
**Answer:** The ±25% statutory band is the full legally permissible range of district sizes. The P1 threshold asks whether a district's population is more than 5% above or below the provincial mean — a much tighter standard. This 5% was chosen as one-fifth of the ±25% total range, representing the zone closest to the provincial average where deviations are most likely to be deliberate rather than geographic necessity. It is a derived threshold (based on the statutory range), not an arbitrary number, but it was chosen by the audit rather than prescribed by law.

---

**Assertion:** P2 threshold: +15pp above mean margin — described as calibrated to Chen 2017.
**Why?** What is "mean margin" and what does Chen 2017 have to do with this?
**Answer:** "Mean margin" is the average winning margin across all districts. P2 flags any district where one party's winning margin exceeds the average by 15 percentage points or more — indicating that party's voters are heavily "packed" into that district. The 15pp figure is calibrated to a 2017 academic paper by Jowei Chen that studied natural geographic clustering of voters; it is set at the level where packing effects become distinguishable from the natural tendency of like-minded people to live near each other. Like all derived thresholds in this audit, its provenance is documented in the threshold provenance compendium.

---

### §4.7 Sensitivity Tests

---

**Assertion:** Three stress-test families are applied: vote-input substitution (2015, 2019, 2023), geographic reclassification variants, and ensemble parameter variation.
**Why?** Why run the same analysis three different ways?
**Answer:** A finding that only appears under one specific set of assumptions is weaker than a finding that appears under many different assumptions. Testing with 2015, 2019, and 2023 vote data shows whether the directional conclusion depends on which election year is used. Testing with different geographic classifications shows whether the Calgary zone gap depends on how "urban core" is defined. Testing with different ensemble parameters (different chain lengths, different balance criteria) shows whether the statistical outlier status depends on specific simulation settings. A finding that survives all three families of variation is much more credible.

---

## §5.1 Population Equality

---

**Assertion:** Minority MAD is 4,707; majority MAD is 3,180. Source: commission's own per-ED population tables.
**Why?** How is this number calculated and why is the commission's own table the source?
**Answer:** The Electoral Boundaries Commission published a table listing the proposed population of every district. The Median Absolute Deviation is computed by taking the absolute value of (each district's population minus the provincial average), then finding the median of those 89 values. Using the commission's own published numbers — not any computed or estimated values — means this finding is based directly on official data and cannot be disputed on the grounds of measurement error. The commission itself produced the population figures used to show the minority map has wider population variance.

---

**Assertion:** Minority MAD 48% wider than majority.
**Why?** Is a 48% wider spread actually significant or is that within normal variation?
**Answer:** The ±25% statutory band allows some population variation. However, the MAD measures not whether any individual district exceeds the limit, but how the typical district compares to the average. A 48% wider MAD means the minority's districts, taken as a whole, are spread further from the ideal equal-population target than the majority's. For comparison, the 2019 current map's MAD is also computed in Appendix C; it can be used to judge whether this difference between the two 2026 proposals is large or small relative to what Alberta has had before.

---

**Assertion:** The majority map's MAD of 3,180 is tighter than the 2019 current-map baseline computed on 2021 Census data (Appendix C).
**Why?** What does it mean that the majority map is tighter than the existing map?
**Answer:** The 2019 map was drawn before the 2021 Census data was available and is now outdated in terms of population equality. When the 2021 Census populations are applied to 2019 district boundaries, those boundaries produce a higher MAD than the majority 2026 proposal. This means the majority commission's work would actually improve population equality compared to the current situation — it is moving in the right direction. This result ran against the researcher's prior expectations and is reported as a finding that limits any blanket criticism of the commission's overall work.

---

**Assertion:** Calgary geographic-zone asymmetry: minority 7.7–12.2%; majority 0.36–0.39% (two classification rules).
**Why?** What are the two classification rules and why are two used?
**Answer:** The audit uses two different methods to define the boundary between Calgary's "urban core" and "suburban ring": one based on city planning zone designations and one based on a radius from the city center. Both methods produce consistent results — the minority map's zone gap is between 7.7% and 12.2% depending on which method is used, while the majority's gap is consistently below 0.4% under both methods. Reporting both confirms the finding does not depend on a particular definition of "urban core."

---

## §5.2 Partisan Bias

---

**Assertion:** Minority EG = +4.02% on canonical results, which is below the audit's 4.10% threshold; the EG flag is withdrawn.
**Why?** Why is a threshold of 4.10% used rather than the academic 7% threshold?
**Answer:** The 7% threshold from Stephanopoulos and McGhee's foundational academic paper was derived from US electoral data and has never been adopted by any Canadian court. The audit's own threshold of 4.10% was derived from the canonical 1,010,000-plan simulation: it is the value at the 95th percentile of efficiency gap magnitudes across those random maps, meaning 95% of neutral randomly drawn maps fall below 4.10%. Using this simulation-derived threshold is more appropriate for Alberta because it reflects what Alberta's specific geography and population distribution produce, not what US states produce. At 4.02%, the minority EG is below even this stricter Alberta-specific threshold, so the efficiency gap alone does not trigger a finding.

---

**Assertion:** Three of four partisan metrics carry outlier flags: Mean-Median at p99.98, Seats at 50/50 at p99.99, Declination at p1.21 (NDP-tail).
**Why?** What does "p99.98" mean and why is declination at p1.21 a problem when the others are at p99.98?
**Answer:** p99.98 means the minority map's mean-median score is higher than 99.98% of the one million randomly drawn neutral maps — extremely high. p99.99 means the minority's seats-at-50/50 score is higher than 99.99% of neutral maps. Both are on the upper tail, indicating UCP advantage. Declination at p1.21 means the minority's declination score is lower than 98.79% of neutral maps — it is on the lower tail, meaning declination reads the opposite direction. This cross-metric disagreement is documented as a known limitation: the efficiency gap and declination disagree because they measure different geometric properties of partisan distribution. The audit notes the disagreement rather than discarding the contradictory metric.

---

**Assertion:** The majority map's mean-median is at p0.85 (NDP-tail), explained as a rural-district preservation convention.
**Why?** Why would a finding that appears to favor the NDP appear in the majority map?
**Answer:** The majority map was drawn by commission members who aimed to preserve existing rural district boundaries, including several rural districts that consistently vote heavily UCP. By preserving those districts unchanged, the majority map creates a cluster of high-UCP-vote-share districts at one end of the distribution. The mean-median score is sensitive to exactly this kind of clustering; a group of high-margin wins for one party shifts the mean away from the median in a direction the formula interprets as favoring the other party. The finding is mechanically explained and is consistent with rural-preservation intent rather than partisan manipulation.

---

**Assertion:** Monte Carlo CI for Seats at 50/50: minority NDP@50/50 has 95% CI [41, 47] vs majority [43, 46] — overlapping.
**Why?** What does it mean that the confidence intervals overlap?
**Answer:** Seats at 50/50 estimates how many seats the NDP would win if the total provincial vote were exactly tied 50-50 between the parties. Under uncertainty in vote attribution, the minority's estimate ranges from 41 to 47 seats and the majority's ranges from 43 to 46 seats. Because these ranges overlap — both include the 43–46 range — you cannot say with statistical certainty that the minority gives the NDP fewer seats than the majority. The point estimates differ, but the uncertainty ranges are large enough to make the difference non-conclusive on this metric alone.

---

**Assertion:** Cross-election stability: the inter-map asymmetry direction reverses under 2019 votes (+0.75 pp vs −0.51 pp).
**Why?** Does a direction reversal under 2019 votes undermine the finding?
**Answer:** The inter-map asymmetry — the difference between how much each map favors the UCP — is approximately −0.51 percentage points under 2023 votes (minority more UCP-favorable) but +0.75 percentage points under 2019 votes (majority slightly more UCP-favorable). The report explains this reversal mechanically: several hybrid electoral districts around Springbank, Bearspaw, and Cochrane are blended differently under the 2019 versus 2023 vote models, and this changes the relative score. The reversal means the magnitude claim is fragile under vote-input change; the four non-vote-based structural signals (population, zone gap, Airdrie, anomalies) are not affected.

---

## §5.3 Packing/Cracking Signatures

---

**Assertion:** The minority map has a higher density of P1-flagged districts (population outliers) and P2-flagged districts (margin outliers) than either the majority or the 2019 map.
**Why?** What does a higher density of flagged districts indicate?
**Answer:** P1-flagged districts are those whose population deviates more than 5% from the provincial average. P2-flagged districts are those where one party's win margin is more than 15 percentage points above the typical margin — suggesting that party's voters are heavily concentrated (packed) in that district. A higher density of both types of flags means the minority map, proportionally, has more districts that deviate from equal-population and more districts where votes are heavily concentrated. When the flagged districts consistently favor the same party and occur in the same regions, that pattern is consistent with packing.

---

**Assertion:** The Airdrie split count is 4 vs 2 across the two maps.
**Why?** How is the "split count" measured?
**Answer:** The split count is simply the number of separate electoral districts that contain at least some portion of the City of Airdrie's population. Under the minority map, Airdrie residents appear in four different districts; under the majority map, they appear in two. This is counted directly from the commission's own published boundary descriptions and maps. No vote data or statistical modeling is involved.

---

**Assertion:** Chen-Rodden natural packing: Alberta's mechanism is UCP rural dispersion, not NDP urban packing.
**Why?** What is "natural packing" and why does the mechanism matter?
**Answer:** Natural packing refers to the tendency of voters with similar political preferences to cluster geographically — not because of deliberate manipulation but because of where people choose to live. In US cities, Democrats tend to live very densely in urban cores, producing what researchers Chen and Rodden call "natural packing" that disadvantages Democrats even in neutral maps. In Alberta, the audit finds the reverse dynamic: UCP voters are dispersed across many rural districts, each of which the UCP wins by large margins. This means the UCP wastes many "excess" rural votes. Understanding this mechanism matters because it affects which party is expected to be disadvantaged even by neutral maps.

---

## §5.4 MCMC Ensemble Results

---

**Assertion:** The 1,010,000-plan canonical ensemble uses official EA shapefiles (ea_majority_2026_eds.gpkg, ea_minority_2026_eds.gpkg, EPSG:3400, 89 EDs each).
**Why?** What is EPSG:3400 and why do the specific filenames matter?
**Answer:** EPSG:3400 is the identifier for a specific geographic coordinate system used in Alberta — it describes how the curved surface of the Earth is flattened onto a flat map for measurement purposes. Using the wrong coordinate system would distort distances and areas. The specific filenames confirm the analysis used the official Elections Alberta shapefiles received on May 6, 2026, rather than the earlier approximate tracings. Citing exact filenames allows any researcher to verify they are using the same input data.

---

**Assertion:** Minority Mean-Median p99.98 on canonical 1M ensemble.
**Why?** What does "p99.98 on canonical 1M ensemble" mean in plain terms?
**Answer:** The canonical ensemble of one million randomly drawn legal Alberta maps produces one million different mean-median scores. The minority map's actual mean-median score is higher than 99.98% of those million scores — meaning only about 200 maps out of every million random maps are as extreme as the minority map on this measure. Said differently: if you drew Alberta maps randomly, following all the legal rules, you would almost never produce a map as extreme as the minority proposal by accident.

---

**Assertion:** Minority Declination p1.21 — disagrees with EG and MM direction; consistent with narrow-margin-loss packing.
**Why?** How can a low percentile score indicate a problem when the others show high percentile scores?
**Answer:** The declination formula measures something different from efficiency gap and mean-median. It looks at the slopes of the win-margin curves for each party. A very low declination score (p1.21 means lower than 98.79% of random maps) in the opposite direction from the other metrics is actually consistent with a specific packing pattern: when one party's voters are used to engineer many close losses rather than many blowout wins, declination reads the pattern differently from efficiency gap. The audit documents this cross-metric disagreement as a technical feature, not an error, and notes it does not resolve the overall outlier status — three of four metrics still place the minority map in the extreme tail.

---

**Assertion:** Mahalanobis Ch1 p = 1.40×10⁻⁶.
**Why?** What is the Mahalanobis test doing that a simple average of the four metrics cannot do?
**Answer:** If you simply averaged the four percentile scores, you would treat each metric as independent. But the four metrics are correlated — maps that score high on efficiency gap often also score high on mean-median, because the same underlying feature drives both. The Mahalanobis distance accounts for those correlations, measuring how far a map is from the center of the joint distribution of all four metrics simultaneously. This prevents double-counting while still capturing the joint signal. A Mahalanobis p = 1.40×10⁻⁶ means the minority map's combination of all four metrics simultaneously is more extreme than 99.9999% of random neutral maps.

---

## §5.5 Pre-registration and OSF Registration

---

**Assertion:** Five OSF pre-registrations cover the audit: w2s8k, r3zm7, qsgy8, 6pt83, s58a6.
**Why?** Why are five separate registrations needed rather than one?
**Answer:** Each registration covers a specific component of the audit at a different point in time. Some were filed before the shapefiles arrived (covering the ensemble tests), some were filed for the confirmatory replication pass scheduled for November 2026, and some cover specific sub-tests like the neighbor-drain analysis. Filing separately at each stage means the registration is as contemporaneous as possible with the analysis — not a single blanket registration filed months in advance for tests that had not yet been designed in detail.

---

**Assertion:** The Benjamini-Hochberg (BH) correction will be applied in the November 2026 confirmatory pass.
**Why?** What is Benjamini-Hochberg correction and why isn't it applied now?
**Answer:** When you run many statistical tests, some will appear significant just by chance — if you run 100 tests at 5% significance, you expect about 5 false positives. The Benjamini-Hochberg procedure adjusts the significance thresholds across all tests to limit the expected number of false discoveries. It is not applied to the current exploratory pass because the specific set of tests for the confirmatory pass has not yet been finalized. Applying BH to exploratory tests that may be revised before confirmation would produce a false sense of precision. The procedure is committed to in advance for the November 2026 pass to ensure the confirmatory results are held to the appropriate standard.

---

## §5.6 Symmetry Counter-Test

---

**Assertion:** The majority symmetry counter-test checks whether the audit would flag the majority map if it had the same statistical properties as the minority.
**Why?** Why would you test the test itself?
**Answer:** A well-designed test should flag maps that are genuinely unusual and not flag maps that are not. If the same test methodology, applied to the majority map, returned the same extreme results as the minority map, that would suggest the test is picking up something inherent to all Alberta maps rather than something specific to the minority map. The counter-test demonstrates that the majority map does not trigger the same flags — confirming the test is detecting a real difference between the two maps rather than a quirk of the testing method.

---

**Assertion:** The majority map is within the neutral statistical band on every partisan-fairness metric.
**Why?** Does "within the neutral band" mean the majority map is perfectly neutral?
**Answer:** Being within the neutral band means the majority map's scores fall in the range you would expect from the million randomly drawn neutral maps — its values are not unusually extreme. It does not mean the majority map is perfectly equal or that every boundary choice is beyond criticism. It means that when measured against the realistic distribution of what neutral independent map-drawing produces, the majority map's scores are unremarkable. The minority map's scores, by contrast, are in the extreme tail of that distribution.

---

## §5.7 Stress-Test Grades

---

**Assertion:** The four surviving structural signals all survive the stress-tests documented in §1.2.
**Why?** What are the stress-tests and what does "surviving" them mean?
**Answer:** The stress-tests are the three families of sensitivity analysis described in §1.2: substituting different vote inputs (2015, 2019, 2023), varying the geographic classification rules, and changing ensemble parameters. A signal "survives" if the direction of the finding — minority more extreme than majority — holds up regardless of which reasonable variant is used. All four non-vote signals (population MAD, Calgary zone gap, Airdrie splits, chair-flagged anomalies) survive because they do not depend on vote data at all. The statistical signals survive on direction (90.5% consistency across Monte Carlo draws) but not on classical 95% magnitude significance.

---

**Assertion:** Stress-test grades A through D are assigned to each finding.
**Why?** What do the letter grades mean?
**Answer:** Grade A means the finding is fully robust — unchanged across all stress-test variants. Grade B means robust on direction but not magnitude. Grade C means dependent on modeling assumptions that are defensible but not unique. Grade D means the finding is weaker — it appears under the primary analysis but not consistently under all variants. Assigning grades makes it easy for readers to identify which findings are most reliable without reading all the technical details of each stress test.

---

## §5.8 Geographic Coherence

---

### §5.8.2 — Visual Spatial Anomalies

---

**Assertion:** Three geographic anomalies on the minority map are confirmed: Rocky Mountain House–Banff Park extension; Calgary-Nolan Hill–Cochrane lasso; Olds-Three Hills-Didsbury → N Airdrie community capture.
**Why?** What makes a boundary shape an "anomaly" rather than just an unusual geographic feature?
**Answer:** A geographic anomaly here means a boundary shape that cannot be straightforwardly explained by following natural features, community boundaries, or the commission's stated criteria. The Rocky Mountain House–Banff Park extension refers to a boundary that reaches into a national park area with no permanent residents in a way that appears to serve no population-based purpose. The "lasso" is a narrow corridor of territory that connects two otherwise distant areas. The community capture refers to an ED whose boundary sweeps in a community — North Airdrie — that appears geographically unconnected to the rest of the district. These shapes were flagged by the commission chair himself in the official commission report.

---

### §5.8.4 — Community Splits

---

**Assertion:** Airdrie: 4 minority districts vs 2 majority districts. Cochrane: merged vs intact. Chestermere: partial split vs intact.
**Why?** Why are Cochrane and Chestermere mentioned alongside Airdrie?
**Answer:** Airdrie, Cochrane, and Chestermere are all fast-growing suburban municipalities near Calgary. The audit checks each city's treatment in both maps because these communities represent the kind of growing areas where boundary choices are most likely to have significant effects — and where splitting across multiple districts most visibly fragments a community's voice. Under the majority map, Cochrane remains intact in one district and Chestermere is intact. Under the minority map, both are treated differently: Cochrane is merged with another area, and Chestermere is partially split.

---

### §5.8.5 — Municipal Anchoring (RETRACTED finding)

---

**Assertion:** The earlier DPG-derived 14.5% / 71.0% / 4.9× figures did not carry forward to recomputation against official shapefiles. Both maps fall within the 70–85% Canadian comparator norm (minority 72%, majority 80%).
**Why?** What exactly is being retracted and does this weaken the overall audit?
**Answer:** The retracted finding claimed the minority map had only 14.5% of its boundaries anchored on municipal edges, compared to the majority's 71% — a 4.9-times gap. This was computed from approximate boundary tracings made before official shapefiles arrived. When the official files were used instead, both maps showed municipal anchoring rates in the 70–85% range that is normal for Canadian provinces. The retracted finding does weaken the fifth structural signal, which no longer differentiates the two maps. However, the four remaining structural signals are unaffected by this retraction, and the retraction itself demonstrates the audit's willingness to report honest failures rather than hiding inconvenient results.

---

## §5.9 Procedural Concerns

---

### §5.9.1 — The April 16 Legislative Pivot

---

**Assertion:** On April 16, 2026, the Alberta Legislative Assembly passed Motion 19 setting aside both reports and establishing a Special Select Committee of five MLAs to draft a 91-seat map by November 2, 2026.
**Why?** Why is a legislature setting aside a commission's report unusual?
**Answer:** The purpose of an independent boundary commission is to insulate the redistricting process from direct political control. Elected representatives are expected to have an interest in how boundaries are drawn because those boundaries determine whether they win or lose future elections. When a legislature sets aside an independent commission's work and replaces the drafting process with a committee of elected members, that transfers control of boundary-drawing directly to politicians. Whether this is legally permissible is a statutory question; whether it is consistent with the norms of independent redistricting is addressed in §5.9.

---

**Assertion:** The procedural pivot replaces an independent commission's drafting process with a government-chaired committee mid-cycle.
**Why?** Who chairs the Special Select Committee and why does that matter?
**Answer:** A government-chaired committee is chaired by a member of the governing party — in this case, the UCP. In the Canadian tradition of electoral boundary reform, independent commissions are chaired by judges or academics specifically to avoid this kind of partisan involvement. A committee that reports to the legislature, with a governing-party chair, faces structural incentives that a fully independent commission does not.

---

### §5.9.3 — Federal Precedent

---

**Assertion:** The 2022 federal sub-commission applied a 2-way Airdrie split, aligning with the provincial majority.
**Why?** Why does a federal redistribution matter for a provincial commission's decision?
**Answer:** The 2022 federal electoral redistribution was conducted by a separate independent commission that drew federal constituency boundaries in Alberta. Those federal boundaries are not binding on the provincial commission, but they provide a useful reference point: independent commissioners, using the same community-of-interest principles, saw no need to fragment Airdrie beyond a 2-way split. The fact that the federal commission reached the same conclusion as the provincial majority — and a different conclusion from the provincial minority — is supporting context, not determinative evidence.

---

### §5.9.4 — Commission Chair Criticism and Public Submission Audit

---

**Assertion:** The commission chair's documented criticism spans 7 configurations across two sections of the majority report (§5.8.2 and §5.9.4).
**Why?** What are the 7 configurations and how does this relate to the "3 confirmed anomalies"?
**Answer:** The chair flagged 7 different minority-map configurations as problematic in the official majority report. Of those 7, the audit was able to verify 3 as confirmed geometric anomalies through direct measurement. The other 4 involve boundary choices that the chair criticized on community-of-interest or process grounds rather than geometry — these are also documented but are categorized differently because they require evaluating the commission's stated rationales rather than measuring boundary shapes.

---

**Assertion:** The minority's 25 published rationales fail falsifiability checks on five of six contested configurations.
**Why?** How do you test whether a written rationale for a boundary choice is defensible?
**Answer:** The audit identifies the simplest alternative boundary that would also satisfy all statutory requirements and the community of interest criteria the minority claimed to be following. If the minority's stated rationale were genuinely the driver, the simpler alternative would have been at least as good and would typically have been chosen. For five of the six configurations examined, a cleaner statutory alternative exists that the minority passed over. The sixth configuration — St. Albert-Sturgeon — is identified as likely constraint-forced rather than a free choice, so it is not counted as a rationale failure.

---

**Assertion:** The Lethbridge / Taber-Warner configuration was removed because the methodology check could not locate the claimed source.
**Why?** Why would a finding be removed just because a source could not be located?
**Answer:** The grounding standard for this audit requires that every claim be verifiable against a primary source. The earlier version of this finding asserted that the minority had made a specific claim about matching federal constituency boundaries in the Lethbridge region. When the actual minority report was checked, no such claim could be found. Without a primary source to confirm that the minority made the claim attributed to them, the item was removed. Removing it rather than keeping an unsupported assertion is an application of the same rigor applied throughout the audit.

---

## §5.10 Summary Scorecard

---

**Assertion:** All four surviving structural signals run in the same direction: minority more dispersed, more asymmetric, more fragmented, more anomalous than majority.
**Why?** Why does the direction of all four signals mattering more than the magnitude of any one?
**Answer:** A single unusual measurement might be explained by chance, a data error, or a quirk of one metric. When four independent measurements — each derived from different data sources and methods, each asking a different question — all point the same direction, the probability of that alignment occurring by chance is much lower than the probability of any individual measurement being unusual. The directional consistency is the audit's core evidentiary argument.

---

**Assertion:** The Fisher combined p = 6.87×10⁻⁸ is the formal statement of convergence between Ch1 and Ch2.
**Why?** Is it valid to combine two p-values using Fisher's method?
**Answer:** Fisher's method is a standard technique from 1932 for combining independent p-values when each test addresses a different aspect of the same hypothesis. It is valid when the two tests are genuinely independent — when the probability of one is not already implied by the probability of the other. Ch1 (ensemble outlier status) and Ch2 (partisan direction of contested-boundary assignments) ask different questions using different data structures, so they are treated as independent. The method multiplies the evidence from both tests; a combined p = 6.87×10⁻⁸ means that if there were no real pattern, both tests would simultaneously return results this extreme roughly once in 15 million repetitions.

---

## §6 Discussion

---

### What the Evidence Supports (Synthesis)

---

**Assertion:** The defensible synthesis: the minority 2026 proposal shows measurable structural differences from the majority in four areas, none depending on vote data.
**Why?** Why is the absence of vote-data dependence emphasized?
**Answer:** Vote-based analysis requires estimating how historical election results would apply under hypothetical new boundaries — a process involving assumptions about voter behavior, geographic allocation, and model choices. All of those assumptions introduce uncertainty. The four surviving structural signals (population MAD, Calgary zone gap, Airdrie fragmentation, chair-flagged anomalies) come directly from the commission's own published tables, the official shapefile geometry, and the commission chair's own written statements. No vote data is needed. That independence makes those four signals more robust than any vote-based finding.

---

**Assertion:** The partisan-bias signal should be read as a directional observation, not a point estimate.
**Why?** What is the difference between a directional observation and a point estimate?
**Answer:** A point estimate would say: "the minority map gives the UCP exactly 1.41 percentage points more efficiency-gap advantage than the majority map." A directional observation says: "across most reasonable ways of modeling vote attribution, the minority map consistently favors the UCP more than the majority map does." The Monte Carlo interval [−3.04, +0.76] shows the point estimate is too uncertain to state precisely. What is stable is the direction: 90.5% of model variants agree the minority is more UCP-favorable. The audit reports the direction honestly without overstating the precision.

---

### Directional Pattern and Metric Context

---

**Assertion:** The directional pattern across structural and statistical dimensions is the finding; the audit records what the data show.
**Why?** If the finding is a "pattern" rather than a single decisive number, can it be dismissed as cherry-picking?
**Answer:** Cherry-picking means selecting only the results that support your conclusion and hiding others. This audit is designed to prevent that: pre-registration locked the test definitions before execution, the symmetry counter-test confirmed the majority map does not trigger the same flags, the retracted municipal anchoring finding is documented openly, and the declination metric that disagrees with the other three is retained rather than dropped. The pattern argument is not "these four things all happen to show the same result"; it is "the pre-specified tests, applied symmetrically to both maps, consistently differentiate them."

---

**Assertion:** Cross-metric declination disagreement is documented as an expected feature of competing formalizations (Warrington 2018; Katz, King, and Rosenblatt 2020).
**Why?** How do academic papers from 2018 and 2020 address a disagreement that appears in this 2026 dataset?
**Answer:** The academic literature on partisan fairness measures has documented extensively that different metrics can give conflicting signals for the same map, because they are measuring genuinely different geometric properties of vote distributions. Warrington (2018) specifically studied conditions under which declination and efficiency gap disagree. Katz, King, and Rosenblatt (2020) recommended reporting multiple metrics precisely because no single metric captures all aspects of partisan fairness. This is why the audit uses four metrics and reports disagreement openly rather than selecting the one that gives the cleanest narrative.

---

**Assertion:** The Chen-Rodden mechanism (rural dispersion rather than urban packing) is the operative geographic pattern in Alberta.
**Why?** Does this mechanism affect what the audit concludes about the minority map?
**Answer:** The Chen-Rodden mechanism means that even a perfectly neutral Alberta map would show the UCP "wasting" more rural votes than the NDP wastes, because UCP voters are geographically spread across many rural ridings while the NDP is more concentrated in a smaller number of urban ridings. This background pattern means the minority map starts from a baseline that is already somewhat UCP-disadvantaged (in efficiency-gap terms) just from geography. The audit's comparisons are always against the million randomly drawn neutral maps, which incorporate this same geographic reality — so the outlier status of the minority map is computed relative to a baseline that already accounts for Alberta's natural geography.

---

### Justiciability (§6.2 context)

---

**Assertion:** Unlike Rucho v. Common Cause (US), partisan gerrymandering claims are justiciable in Canadian courts.
**Why?** What practical difference does justiciability make?
**Answer:** Justiciable means a court can hear the case and issue a ruling on the merits. In the United States after Rucho, federal courts cannot rule on whether a map is an unconstitutional partisan gerrymander — they must dismiss those cases without deciding the question. In Canada, courts can evaluate whether a boundary commission has met the constitutional standard of effective representation under the Charter. This means the findings in this audit could in principle be placed before a court that has the authority to require revision of the boundaries, unlike in the US federal system.

---

### §6.1 — How to Interpret These Findings: NP-Hardness and Statistical Improbability

---

**Assertion:** The redistricting problem is NP-hard; there is no single correct Alberta map.
**Why?** If there is no "correct" answer, can anything be measured?
**Answer:** NP-hard means the problem has so many legal solutions that no computer algorithm can find the single best one efficiently. Alberta's rules (equal population, connected districts, compact shape, community preservation) define an enormous family of valid maps, not a unique optimum. The audit does not measure whether the commission found the "right" answer — it measures where the chosen map sits within the distribution of all the legal answers that satisfy the same rules. Being at the extreme tail of that distribution means the map is an unusual choice, not necessarily a wrong one. But unusual choices invite explanation.

---

**Assertion:** The audit's claim is: "this map is statistically improbable within the constraint set, and the improbability has a direction that is measurable."
**Why?** What does it mean for a map to be "statistically improbable within the constraint set"?
**Answer:** The constraint set is all the legal rules the commission must follow. The audit simulates over one million maps that all satisfy those rules. If a real map's score on a fairness measure falls outside the range that 99.9% of the simulated maps produce, the real map is statistically unusual — it is the kind of outcome you would almost never get from a process that was just randomly selecting among the legal options. The "direction" observation means that every time the real map is unusual, it is unusual in the same way: consistently favoring the same political party.

---

**Assertion:** The Commission did not have to split Airdrie four ways; they chose to, among many legal alternatives that did not require that split.
**Why?** How do you know there were legal alternatives that did not split Airdrie four ways?
**Answer:** Airdrie's population of approximately 85,805 is about 1.56 times the provincial average district size. The ±25% statutory band permits a single district to hold between 75% and 125% of the average. Airdrie's population sits in the range where a single district or a clean two-way split are both legally valid options. The vast majority of the million randomly generated legal maps keep Airdrie in one or two districts. The four-way split is possible under the law but is something only a small minority of legal maps produce — meaning it was not forced by the constraints.

---

**Assertion:** "Precision is armor" — the over-engineered methodology forces the distinction between an accidental brush-stroke and a systematic pattern.
**Why?** Why would a commission challenge the audit on grounds that it is "too precise"?
**Answer:** A commission could argue that a single unusual metric score is just a quirk of their particular balance of trade-offs — that focusing on one number misses the complexity of real boundary drawing. The audit's multiple independent tests (population, zone gap, community splits, boundary shapes, statistical ensemble, bootstrap test) are designed to answer that objection in advance: a systematic pattern across six independent measurement approaches cannot be dismissed as one quirk. If the deviation were accidental, you would expect some metrics to show the minority as more neutral than the majority — but none do.

---

### §6.2 — Author's Verdict

---

**Assertion:** §6.2 departs from the audit's measurement-only voice and offers the author's stated opinion; it is presented as opinion, not as a peer-reviewed conclusion.
**Why?** Why include the author's opinion at all if it is not peer-reviewed?
**Answer:** The audit is a public-interest document, not only a journal article. Readers who came here to understand whether a map looks like a gerrymander deserve an honest answer from the person who built the measurement apparatus. Presenting the opinion clearly labeled as opinion — with the bias disclosure from §1 restated — lets readers weigh it with appropriate skepticism. A reader who only wants the measurements is explicitly told to stop at §6.1.

---

**Assertion:** A "gerrymander signature" is the constellation of measurable effects the academic redistricting literature treats as evidence of partisan engineering — narrower than "any map with a partisan-asymmetry signal," broader than "any map whose author admits intent."
**Why?** Why not just say whether the map is or is not a gerrymander?
**Answer:** "Gerrymander" is a legal conclusion that requires evidence about intent and effect together. The academic literature instead defines a gerrymander signature: a pattern of measurable effects — partisan outlier status, community fragmentation, rationale failures, boundary anomalies — that distinguishes intentional engineering from natural geography. The audit measures whether that signature is present; courts would need to assess whether the signature reflects illegal intent and constitutes a violation of the effective-representation standard.

---

#### §6.2.1 — Lane 1: Partisan-Bias Magnitude

---

**Assertion:** Reading A (crosswalk-blend): majority EG −0.40%, minority EG −1.81% — both sub-threshold on every Alberta-calibrated threshold.
**Why?** What is a "crosswalk-blend" and why do both maps show negative (NDP-tail) efficiency gaps?
**Answer:** The crosswalk-blend method assigns votes from old districts to new district boundaries by looking up which old districts overlap the new ones and blending their vote shares. Negative efficiency gap under the Alberta convention means more NDP votes are "wasted" than UCP votes — the NDP is at a disadvantage. Both maps show this under Reading A because the underlying Alberta geography (urban NDP concentration vs. rural UCP dispersion) produces natural packing that disadvantages the NDP in both proposals.

---

**Assertion:** Reading B (full-coverage spatial): majority EG +6.43%, minority EG +9.21% — both over every Alberta-calibrated threshold including 4.10%.
**Why?** Why does the sign flip between Reading A and Reading B?
**Answer:** Reading B uses a more precise method of assigning votes to new boundaries: it overlays the actual geographic shapes of polling stations against the new district maps and attributes votes proportionally by area. When this method is used and all 89 districts are properly attributed (fixing the v0_8 coverage gap), the estimated efficiency gap is larger and positive under the Alberta convention (positive = NDP advantage, so both maps look NDP-favorable in Reading B). The sign difference between readings reflects the sensitivity of efficiency-gap estimates to how votes are geographically attributed — which is exactly why the audit reports both readings rather than choosing one.

---

**Assertion:** Both readings agree the minority sits closer to the UCP-favoured tail than the majority on every metric.
**Why?** If the readings disagree on magnitudes and signs, how can they agree on the direction?
**Answer:** Reading A shows minority EG −1.81% vs majority −0.40%: the minority is more negative (more UCP-favorable) than the majority. Reading B shows minority EG +9.21% vs majority +6.43%: the minority is more positive (more NDP-favorable) than the majority, but by a larger gap. Both readings agree on the relative position: the minority is further toward one tail than the majority. Whether that tail represents a UCP or NDP advantage depends on the reading chosen — the cross-method disagreement is itself reported as a finding.

---

#### §6.2.2 — Lane 2: Structural and Procedural Pattern

---

**Assertion:** Public-submission support: two contested configurations (Airdrie 4-way, Nolan Hill) have no documented submissions in the 1,140+ archive.
**Why?** What does it mean to check the submission archive and why does the absence of submissions matter?
**Answer:** The commission received over 1,140 public submissions from citizens, communities, and organizations. These submissions are the documented evidence that the public wanted specific boundary choices. If a minority commissioner made a specific boundary decision — such as splitting Airdrie four ways or drawing the Nolan Hill corridor — and no submission in the archive requested that specific configuration, then the choice cannot be defended as responding to public input. Finding no submissions for two of the most unusual configurations is a gap in the rationale, not proof of bad intent.

---

**Assertion:** Pre-registered structural-irregularity count: minority meets the ≥4 of 5 outlier threshold; majority meets 0 of 5.
**Why?** What is this scoring and what are the five pre-registered tests?
**Answer:** Before looking at the data, the audit committed to scoring both maps on five structural dimensions: population dispersion (MAD), Calgary zone asymmetry, Airdrie community fragmentation, municipal boundary anchoring, and chair-flagged anomalies. The pre-registration declared that a map scoring as an outlier on four or more of these five would cross the threshold. The minority map scores as an outlier on four (population, zone gap, Airdrie, anomalies; the fifth — anchoring — was retracted after canonical recomputation). The majority map scores as an outlier on zero.

---

#### §6.2.3 — Verdict on the Majority

---

**Assertion:** The majority's Mahalanobis p = 0.097 on the 1M canonical run — inside the null band.
**Why?** A p-value of 0.097 is less than 0.10. Isn't that "significant"?
**Answer:** No. Smaller p-values mean the result is more extreme, not less. A p-value of 0.097 means the majority's joint partisan-fairness score is more extreme than 9.7% of randomly drawn neutral maps — well within the normal range. By comparison, the minority's Mahalanobis p = 1.40×10⁻⁶ means it is more extreme than 99.9999% of random maps. The 0.097 value is close to the center of the distribution (where 50% of maps lie), not near the extremes.

---

**Assertion:** The majority retreats from the 2019 enacted baseline in joint-metric space (D² = 12.75 → 7.85), consistent with a normalizing commission process.
**Why?** What does "retreating in joint-metric space" mean for a map?
**Answer:** The Mahalanobis D² score measures how far a map is from the center of the neutral ensemble cloud. A higher D² means the map is further from neutral. The 2019 enacted baseline scores 12.75 on this measure (moderately unusual, as it was drawn with older data and tools). The majority 2026 proposal scores 7.85 — closer to neutral than the existing map it is replacing. This is what you would expect from a commission doing its job: producing a new map that is more consistent with current neutral norms than the aging map it replaces.

---

#### §6.2.4 — Verdict on the Minority

---

**Assertion:** The minority amplifies the 2019 enacted baseline's joint-space position (D² = 12.75 → 32.67).
**Why?** What does it mean to "amplify" rather than "normalize"?
**Answer:** Where the majority brought the Mahalanobis distance down from 12.75 to 7.85 (moving toward neutral), the minority moved it in the opposite direction — from 12.75 all the way to 32.67 (moving further from neutral). The minority map is more than two and a half times as extreme as the 2019 map it was supposed to replace and four times more extreme than the majority proposal. Rather than normalizing an aging boundary set, the minority concentrated its deviations further in one direction.

---

**Assertion:** The honest summary: the minority maxes out the structural-irregularity scoring while staying inside the partisan-bias-magnitude band under Reading A.
**Why?** How can a map max out structural irregularities but stay inside the partisan-bias band?
**Answer:** The academic literature on gerrymandering distinguishes "broad partisan distortion" from "surgical fortification." Broad distortion shows up in the overall efficiency gap — a high percentage of one party's votes are wasted across the whole map. Surgical fortification concentrates changes in a small number of marginal districts to lock in a seat advantage without moving the efficiency gap much. The minority appears to have the second pattern: the structural indicators (community splits, boundary anomalies, zone asymmetry) are extreme, but the efficiency-gap magnitude stays close enough to the threshold that Reading A does not trigger it.

---

#### §6.2.5 — How Close Did the Minority Come?

---

**Assertion:** Under Reading B, the minority's seats@50/50 of 52.8% sits above the simulation's converged ceiling of 51.72% — a placement zero of 2,000,000 neutral draws reach.
**Why?** What does it mean to be above the "converged ceiling" of the simulation?
**Answer:** The simulation converged on a maximum seats@50/50 value of 51.72% across 2,000,000 randomly drawn neutral maps — not a single one of those maps produced a value higher than that. The minority map's earlier estimate of 52.8% (from a partially attributed dataset, later corrected to 48.3% under the v0_8 full-attribution method) was above that ceiling. The corrected 48.3% figure places the minority at p99.99 — still among the most extreme 0.01% of neutral maps — but no longer above the simulation ceiling. This correction (from H2 in the hypothesis table) is an important example of the audit correcting its own prior findings.

---

**Assertion:** SZAT regional decomposition: Rest of Alberta +0.015 (dominant), Edmonton +0.008, Mountain-West +0.006, Calgary −0.008 (partially offsetting).
**Why?** Why does Calgary run in the opposite direction to the overall SZAT score?
**Answer:** The SZAT test measures the partisan effect of each specific boundary decision the minority made differently from the majority. The Calgary region boundary differences actually slightly favor the NDP (pushing the score toward NDP-favorable), while the rest of Alberta's boundary differences push more strongly toward UCP-favorable. The net result is a map-wide UCP-favorable signal that does not come primarily from Calgary — it is distributed across the province. This is described as inconsistent with a Calgary-centric explanation and consistent with a province-wide pattern.

---

#### §6.2.6 — What Would Change the Verdict

---

**Assertion:** The strongest single falsifier is: an independent reviewer produces a constraint-legal Alberta map that satisfies the minority's stated community-of-interest rationales and also matches majority-comparable municipal anchoring.
**Why?** Why would a counter-map by an independent reviewer change the verdict?
**Answer:** The rationale-failure finding rests on the claim that simpler, cleaner alternatives exist that would have satisfied the minority's stated community-of-interest reasons for their boundary choices. If an independent reviewer — someone with no stake in the outcome — constructs such a map and it genuinely satisfies the minority's stated criteria while looking more like the majority, that would demonstrate the minority's choices were not forced by their own rationales. That would shift the interpretation from "the rationale is a pretext" to "the constraint space is genuinely tight and the minority made defensible trade-offs." The audit has invited this check via its public GitHub repository.

---

#### §6.2.7 — Verdict on the April 16 Government Pivot

---

**Assertion:** Substituting a UCP-MLA-chaired committee for the independent commission's drafting process is the most government-controlled response among the three most commonly cited Canadian comparator cases.
**Why?** What are the comparator cases and why does this comparison matter?
**Answer:** The three Canadian cases used as comparators are the federal 2012 redistribution challenge, Saskatchewan's 1989 court referral, and Alberta's current 2026 situation. In the federal 2012 case, Parliament challenged but did not replace the commission's recommendations. In the Saskatchewan 1989 case, the government sought court guidance before the commission finished its work. In Alberta 2026, the legislature set aside a completed commission report and transferred drawing authority to a committee of elected members from the governing party. Placing this action within the comparator range establishes that it represents a larger departure from independent-commission norms than the other cases cited.

---

#### §6.2.8 — Bottom Line

---

**Assertion:** The minority map is the kind of map a non-neutral procedure produces under EBCA constraints; it is not the kind of map a neutral procedure produces.
**Why?** How does the simulation establish what a "neutral procedure" produces?
**Answer:** The simulation runs GerryChain's ReCom algorithm, which makes random legal boundary changes without any information about how voters are distributed. It has no ability to favor one party; it only knows population totals and contiguity rules. Over one million steps it explores the full space of maps that a genuinely neutral, apolitical process would produce. The minority map sits in the extreme tail of that space — in territory that is essentially unreachable by random neutral drawing but reachable by targeted hill-climbing (as confirmed by the Cannon et al. short-bursts test in §5.4.8). That contrast defines what "a non-neutral procedure" means here.

---

## §7 — Limitations and Falsifiability

---

**Assertion:** Three modelling-uncertainty tests materially narrow the partisan-bias magnitude claim while leaving the structural findings intact.
**Why?** If three tests narrow the magnitude claim, should the magnitude claim be dropped entirely?
**Answer:** The tests show the magnitude is uncertain — the 95% confidence interval crosses zero — but they do not show the magnitude is zero. 90.5% directional consistency across 2,000 Monte Carlo draws is a strong signal even if it falls short of the 95% classical significance threshold. The appropriate response is to report the finding with accurate uncertainty bounds rather than either (a) asserting a precise magnitude or (b) dropping the finding entirely. The audit does (a) correctly by reporting both the central estimate and the uncertainty interval.

---

**Assertion:** The statistical tests are exploratory, not confirmatory; they are reproducible and temporally anchored but require independent replication.
**Why?** Why do reproducible results still require independent replication?
**Answer:** Reproducibility means another researcher running the same code against the same data gets the same number. That is necessary but not sufficient for scientific confidence. Independent replication means a different researcher, using different code and possibly different methods, testing the same hypothesis on new data or from a different angle, finds consistent results. Exploratory results can be reproducible but still reflect choices made after some data exploration, even unintentionally. The prospective confirmatory study pre-registered at OSF (for the November 2026 committee map) is designed to provide that independent check.

---

### §7.0 — Hypotheses Tested and Their Disposition (H1–H10)

---

**Assertion:** Hypothesis H1: re-seeding bug was found and corrected before main analysis.
**Why?** What was the re-seeding bug and why does disclosing it matter?
**Answer:** A re-seeding bug would occur if the simulation unintentionally restarted its random number generator partway through a run, causing the maps generated after the restart to be non-random in a subtle way. The audit identified and corrected such a bug before the main analysis was run. Disclosing it matters because it shows the audit's quality-control process caught a technical error before it could affect results — and because failing to disclose a known bug would be a serious scientific ethics problem.

---

**Assertion:** Hypothesis H2: the 52.8% → 48.3% seats@50/50 correction.
**Why?** Why was this estimate corrected and what caused the original error?
**Answer:** An earlier analysis estimated the minority map would give the UCP 52.8% of seats in a tied election. That estimate was based on a partially attributed dataset. After the v0_8 full-coverage attribution corrected the 22 missing rural districts (which were heavily UCP-voting), the revised estimate became 48.3%. The correction reflects the same attribution improvement described in §1.2 and §3: adding back the missing rural UCP votes changed the seat-share estimate because those districts were incorrectly absent from the earlier computation.

---

**Assertion:** Hypothesis H3: compactness mechanism rejected. The mechanism is not compactness-driven but is consistent with partisan allocation of population.
**Why?** What was the compactness hypothesis and why was it rejected?
**Answer:** An early hypothesis was that the structural differences between the two maps were driven primarily by the minority commission placing more emphasis on compact (roughly circular) districts. Compactness is a legitimate redistricting criterion and if it explained all the differences, the structural signals would be a byproduct of a neutral value judgment rather than a partisan pattern. The analysis found that the minority map's districts are not consistently more compact than the majority's — compactness scores do not differ in the direction that would explain the population and zone-gap findings. The hypothesis was rejected and the explanation for the structural differences remains the population allocation pattern itself.

---

**Assertion:** Hypothesis H5: regional swing substantially weakens the signal when applied.
**Why?** What is a "regional swing" and how does it weaken the signal?
**Answer:** A regional swing adjustment assumes that voters in different parts of the province may not shift their preferences uniformly across elections. If the UCP performs better in some regions in 2023 than in 2019, simply scaling up or down by the provincial average change would misrepresent regional variation. When regional swing adjustments are applied to the vote attribution, some of the partisan-bias signal diminishes — the efficiency gap moves closer to zero. This is why the magnitude claim is narrowed and the directional claim is the stronger statement.

---

**Assertion:** H4: natural anchoring. H6: two-party normalization. H7–H10: various disposition notes.
**Why?** What are H4 and H6 testing?
**Answer:** H4 (natural anchoring) tested whether municipal boundary alignment differences between the two maps could be explained by the minority commission simply following natural geographic features (rivers, roads, terrain) rather than municipal edges. The finding was that natural anchoring is present in both maps and does not explain the minority-specific patterns. H6 tested whether the two-party vote normalization (treating the provincial total as a simple UCP vs NDP contest) introduced artificial bias. The check confirmed the normalization is standard and appropriate for Alberta's electoral context where minor parties take very few seats. H7–H10 cover additional technical hypotheses that arose during analysis and were tested and disposed of; each is documented in the hypothesis table for completeness.

---


---
### DPG Sunset Clause (Methodological Note)

---

**Assertion:** Files in data/shapefiles/derived/ generated from DPG are deprecated; all active analysis uses data/shapefiles/canonical/.
**Why?** What does "deprecated" mean in this context and why keep the old files at all?
**Answer:** Deprecated means the old approximate files are no longer used in current analysis — they have been replaced by the official files. They are kept in the repository, not deleted, because the complete historical record of the audit's development is itself part of the audit's transparency. Readers can trace which findings changed when the official files arrived and verify that the change was properly documented. Deleting the old files would make it impossible to confirm that the transition was handled correctly.

---

### Vote Attribution Cycle-Lag (Methodological Note)

---

**Assertion:** The cycle-lag problem: 2019 boundaries, 2021 Census, 2023 votes are three different temporal layers.
**Why?** Is using data from three different years a serious methodological flaw?
**Answer:** The cycle lag is not a flaw but an inherent feature of redistricting analysis: boundaries, population counts, and election results are always from different years in this context. The audit documents the assumption required to bridge them — primarily that geographic vote distributions are relatively stable within the three-year window and that the area-proportional attribution method is a reasonable approximation for assigning poll votes to new district boundaries. The sensitivity analysis tests whether different assumptions about this bridge materially change the conclusions; the directional signal is stable.

---

### §7.1 — Missing Evidence and Scope Limits

---

**Assertion:** Phase 4C measured attribution — replacing the 70/30 blend with observed apportionment — would reduce the sensitivity range in §5.2.2 to a single refined value.
**Why?** What is "Phase 4C" and what is the 70/30 blend it would replace?
**Answer:** The 70/30 blend is a modeling assumption used when precise vote attribution is not possible: 70% of a hybrid district's vote estimate comes from applying the result to one zone, 30% from another. It is a placeholder for the measured value that would come from a complete geographic overlay of every polling station with the new district shapes. Phase 4C is the planned analysis step that would replace this placeholder with a directly measured value. Until that step is executed, the efficiency gap estimates carry uncertainty from this modeling choice, which is part of why the Monte Carlo interval is wide.

---

**Assertion:** Multiple testing under Holm-Bonferroni correction for five tests at α = 0.10: the minority's seats@50/50 result (p = 0.0148) satisfies the corrected threshold (0.02).
**Why?** What is Holm-Bonferroni and why does this matter?
**Answer:** When you run five tests, the chance that at least one appears significant just by coincidence is higher than when you run one test. Holm-Bonferroni is a method for adjusting the threshold downward to account for this: the strictest threshold when running five tests at 10% significance is 0.10 / 5 = 0.02. The minority's seats@50/50 result of p = 0.0148 is below this corrected threshold, meaning it would be considered statistically significant even under this conservative multi-testing adjustment. The audit notes this to address the objection that running multiple tests inflates the chance of a false positive.

---

### §7.2 — Falsifiability Statement

---

**Assertion:** The directional claim would be falsified by an alternative Calgary classification that produces near-null minority-majority asymmetry while the current rule produces >10%.
**Why?** Why is the Calgary zone classification a potential falsifier?
**Answer:** The 12.2% vs 0.4% Calgary zone asymmetry finding depends on how the "urban core" and "suburban ring" categories are defined. If there were a reasonable alternative classification scheme under which the zone gap nearly disappeared, the finding would be an artifact of the chosen definition rather than a robust result. The audit tested two different classification rules and found consistent results under both. This falsifiability condition is not met by the existing tests; it would only be met if someone identified a third, defensible classification under which the asymmetry vanishes.

---

**Assertion:** Submission-archive evidence that the five disputed minority configurations did have substantial public support would refute the "no public support" claim.
**Why?** If such submissions exist, why weren't they found?
**Answer:** The commission's 1,140+ submission archive is a large body of documents. The audit's search identified no submissions supporting the Airdrie four-way split or the Nolan Hill corridor configuration. However, the search may have been incomplete — if submissions used different place names, described the desired outcome without naming the specific boundary shape, or were filed under administrative categories that were not searched, they could exist without being found. The falsifiability condition acknowledges this limitation honestly: if such submissions are located and published, that would require revising the "no public support" finding.

---

### §7.3 — Academic Limitations and Methodological Caveats

---

**Assertion:** Ecological inference limitation: actual 2026 vote distributions may differ structurally from the uniform-swing projections.
**Why?** What is "ecological inference" and why is it a limitation here?
**Answer:** Ecological inference is the practice of drawing conclusions about individual behavior (how specific voters would vote under new boundaries) from aggregate data (total vote counts by area). The audit estimates how votes would be distributed in new districts by assuming voters in the old district would vote in the same proportions in the new district. If the new boundaries change the community mix in ways that shift voting patterns — for example, if adding a fast-growing suburb with different preferences to an existing district changes the whole district's outcome — the uniform-swing assumption would be wrong. This is why the directional finding is stated with a confidence level rather than as a point estimate.

---

**Assertion:** Single-election dependency: 2023 was highly competitive (UCP 52.6%, NDP 44.0%). In a landslide environment, structural partisan metrics become noisy.
**Why?** Why would a landslide make the metrics unreliable?
**Answer:** Partisan fairness metrics like the efficiency gap are most informative when elections are reasonably competitive — when both parties win some seats and waste some votes. In a landslide where one party wins almost everything, the losing party wastes nearly all its votes by definition, which makes the efficiency gap very large regardless of how the boundaries were drawn. The 2023 election was close enough that partisan structure is detectable; if the 2023 margin had been larger in either direction, the metrics would be harder to interpret.

---

**Assertion:** Geographic constraints vs intent: Alberta's deep urban/rural divide creates severe natural packing; residual natural packing may be misattributed as intentional engineering (Chen and Rodden 2013).
**Why?** How does the MCMC ensemble account for this?
**Answer:** The MCMC ensemble generates neutral maps using Alberta's actual geography — the same population distribution, the same urban/rural divide. Every one of the million simulated maps reflects Alberta's geographic reality. When the audit says the minority map is in the 99.99th percentile, it means the minority is more extreme than 99.99% of maps that already incorporate Alberta's natural packing. The natural packing is baked into the neutral baseline; what is measured is the additional departure from that baseline, not from a hypothetical equal geography.

---

**Assertion:** Model dependence: ReCom assumes contiguous, population-balanced districts as the primary constraints. If the commission weighted unmeasured criteria heavily, the neutral baseline may be misspecified.
**Why?** What are "unmeasured criteria" and why might they affect the comparison?
**Answer:** The EBCA requires the commission to consider community of interest, existing electoral boundaries, and other factors beyond just population equality and geographic contiguity. The ReCom simulation does not fully model community-of-interest preservation — it cannot, because "community of interest" is a qualitative judgment rather than a computable constraint. If the commission's choices were primarily driven by unusual community-of-interest determinations, the neutral ensemble would not properly capture the space of constraint-legal maps as the commission understood it. This is why the Lane 2 structural findings, which do not depend on the ensemble, carry independent weight.

---

## §8 Conclusion

---

**Assertion:** The audit's primary finding is directional consistency across structural and statistical dimensions, not a single decisive number.
**Why?** Is a directional finding strong enough to support any policy response?
**Answer:** The directional consistency across four independent structural signals — each derived from different data sources, each surviving stress-testing — is stronger evidence than any single statistical test would be alone. The statistical tests (Fisher p = 6.87×10⁻⁸) add quantitative weight to the structural signals. Together they support the conclusion that the two 2026 maps are not equivalent proposals from an independent commission. Whether this is strong enough to require legal remedy, administrative revision, or simply public acknowledgment is a policy and legal judgment; the audit provides the empirical input for that judgment.

---

**Assertion:** The majority map is within the neutral statistical band on every metric; the minority is not. This is the headline.
**Why?** What should a reader conclude from this if they are a policymaker, a court, or a journalist?
**Answer:** A policymaker reviewing two competing redistricting proposals should understand that these are not equivalent options: one falls within the range that neutral independent processes produce, and one does not. A court evaluating a Charter challenge to the redistricting process would have access to quantified outlier statistics and pre-registered methodology to assess. A journalist covering the redistricting should report that independent computational analysis found statistically significant differences between the two proposals — with the appropriate caveats about exploratory status. The audit does not tell any of these audiences what to do; it provides the measurement.

---

**Assertion:** The November 2026 confirmatory replication will apply Benjamini-Hochberg correction and is pre-registered at OSF.
**Why?** What happens if the November 2026 committee map falls within the neutral band?
**Answer:** If the new 91-seat committee map scores within the neutral ensemble band on all partisan-fairness metrics, that would be a null result on the confirmatory test — the committee's map did not reproduce the partisan pattern found in the minority commission proposal. That null result would be reported fully, consistent with the audit's commitment to transparent failure reporting. It would not retroactively change the findings about the original minority proposal, but it would indicate the committee's process produced a different outcome.

---


---

**Assertion:** Across eight sub-sections of §5, the minority 2026 proposal shows wider distribution, higher packing and cracking signals, more anomalies, and a more government-controlled procedural path than the majority.
**Why?** Does consistently finding the same direction across eight sub-sections constitute one finding or eight?
**Answer:** The eight sub-sections each test a different measurable property using different data, different methods, and different mathematical tools. They are not the same test repeated eight times. Finding consistent direction across eight independent tests — each with its own methodology — is much stronger evidence than finding one strong result on one test. The audit's structure is designed precisely to force this breadth: each sub-section is independently runnable from its own script against its own data source.

---

**Assertion:** The direction holds at approximately 90% confidence under Monte Carlo over modelling choices across 2020s-era voter distributions.
**Why?** What does "2020s-era voter distributions" mean here?
**Answer:** This refers to vote distributions from recent elections (2023 actual results) and recent polling (April 2026 338Canada estimates), which both reflect the contemporary political alignment of Alberta's communities. The audit cross-checks whether the directional finding holds not just for one specific election but for the range of plausible current voter distributions. 90% confidence means that across 2,000 different combinations of modeling assumptions applied to these recent voter distributions, 9 out of 10 combinations point to the minority as more UCP-favorable than the majority.

---

**Assertion:** When the Lunty committee tables its 91-seat map by November 2, 2026, the same scripts will be re-run as fulsomely and faithfully as they were for the commission proposals.
**Why?** Why make a public commitment to re-run the analysis on the new map?
**Answer:** The pre-registration and commitment to replication serve the same purpose as every other methodological discipline in this audit: they prevent the appearance (or reality) of cherry-picking. If the author only analyzed the commission maps and declined to analyze the committee map, a skeptic could argue the analysis was not symmetric — that it targeted the minority proposal specifically because it was expected to show findings. Running the same analysis on the November map, with the same thresholds and the same commitment to reporting null results, converts the framework from an accusation into a repeatable test.

---

### §8.1 — Postscript: The Audit as Framework for the Held-Out Test

---

**Assertion:** The commission audit was a framework-building exercise that calibrated artefacts the next audit will need.
**Why?** If the commission proposals are now moot, why does documenting them matter?
**Answer:** The audit produced six specific calibrated outputs that will be directly reused for the November 2026 evaluation: the four Alberta-calibrated efficiency-gap thresholds; the 1,010,000-plan canonical ensemble; the structural-irregularity scorecard with benchmarks; the rationale-failure framework; the DPG construction pipeline for new boundaries; and the two-lane verdict structure. Without these calibrations from the commission audit, the November evaluation would need to build its methodology from scratch, inviting the criticism that the methodology was designed after seeing the map.

---

**Assertion:** Sub-threshold on Lane 1 is necessary for a clean verdict, but not sufficient.
**Why?** What is the two-lane verdict structure actually saying as a practical matter?
**Answer:** The two-lane structure says: to give a map a clean verdict, it must pass both the partisan-bias magnitude test (Lane 1) and the structural-pattern test (Lane 2). A map that keeps its efficiency gap below the 4.10% threshold but fragments communities, creates boundary anomalies, and fails its own stated rationales still exhibits structural red flags — which the minority proposal demonstrated empirically. For the November committee map, the audit will be looking at both lanes and will report if a map passes one while failing the other, rather than declaring it clean based on either lane alone.

---

**Assertion:** A drafting process that wants to engineer outcomes without leaving an EG fingerprint has the structural lane available — community splits, off-reference borders, anchoring departures, chair-flagged shapes — and the audit will be looking at both lanes when the Lunty committee map arrives.
**Why?** Is this saying the committee is expected to gerrymander?
**Answer:** No. This is an analytical observation about what the audit apparatus is designed to detect, not a prediction about the committee's behavior. The minority commission proposal demonstrated that it is possible for a map to stay within the efficiency-gap threshold while showing structural irregularities. The November audit makes no assumption about what the committee will produce. It states what the audit is capable of detecting if structural manipulation occurs, so that the methodology cannot be criticized after the fact for being blind to that possibility.

---

*End of plain-language defense document.*

<!-- PLAIN_LANG_DEFENSE_END -->

## References

---

**Assertion:** Citations follow American Political Science Association (APSA) style; court cases follow Canadian legal citation convention.
**Why?** Why does a technical audit use a political science citation style rather than a legal one?
**Answer:** The audit is primarily an empirical, data-driven study situated within the academic political science literature on redistricting, not a legal submission or court document. APSA style is standard for political science journals and preprints. The court cases are cited in the standard Canadian legal format (which uses square brackets for year of decision and volume/page identifiers) separately from the academic references, because legal citations serve a different function — they identify the specific reported decision rather than crediting an author's argument.

---

**Assertion:** Five key academic works are Stephanopoulos and McGhee (2014/2018), DeFord et al. (2021), Warrington (2018), Katz/King/Rosenblatt (2020), and Chen and Rodden (2013).
**Why?** Why are these specific works the primary academic references?
**Answer:** Stephanopoulos and McGhee invented the efficiency gap metric and defined the 7% reference threshold. DeFord et al. developed and validated the ReCom algorithm used in this audit's simulation. Warrington introduced the declination metric and documented conditions under which it disagrees with the efficiency gap. Katz, King, and Rosenblatt provided the theoretical case for using multiple metrics simultaneously rather than relying on any single measure. Chen and Rodden documented the natural-packing mechanism by which urban Democratic voters in the US — and by analogy, urban NDP voters in Alberta — are geographically concentrated in ways that disadvantage them even in neutral maps.

---

**Assertion:** The Saskatchewan Reference ([1991] 2 SCR 158) is the governing Canadian constitutional case.
**Why?** Why is this a 1991 case and not something more recent?
**Answer:** The Supreme Court of Canada has not substantially revisited the effective-representation standard since 1991. The Saskatchewan Reference remains the foundational ruling on what the Charter's right to vote requires of electoral boundary commissions. Subsequent federal court cases (Raîche 2004, Cassista 2014) have applied the Saskatchewan Reference standard but have not altered its core holding. Until the Supreme Court revisits the question, the 1991 standard governs.

---

## Appendices

---

### Appendix A — Reproducibility

---

**Assertion:** The three-election direction-stability test shows minority-majority efficiency-gap asymmetry of +0.03 pp in 2015, +0.75 pp in 2019, and −0.51 pp in 2023.
**Why?** Why do the sign and magnitude of the inter-map gap vary across elections?
**Answer:** The inter-map gap measures the difference between how much the majority map and the minority map favor the UCP — not whether either map favors the UCP in absolute terms. In 2015, both maps looked almost identical in partisan terms. In 2019, the minority was 0.75 pp more UCP-favorable. In 2023, the minority was 0.51 pp less UCP-favorable (the minority appeared slightly better for the NDP under 2023 votes). This variation is explained by how the minority's hybrid districts around Springbank, Bearspaw, and Cochrane behave under different election results: those areas lean urban-NDP in competitive elections (2023) and lean rural-UCP in elections with smaller urban-suburban swings (2015, 2019). The direction of the individual maps does not change — both maps consistently favor the UCP under all three elections — only the relative gap between them shifts.

---

**Assertion:** Every script prints a gate PASS/FAIL line; numbers in the body text must match the gate-passed output.
**Why?** What is a gate PASS/FAIL check and how does it prevent errors?
**Answer:** Each analysis script includes an assertion that checks its own key output values against expected ranges. When the script runs, it prints "GATE PASS" if the computed values are within the expected range, or "GATE FAIL" with a description of the discrepancy if they are not. This is a form of automated self-checking: it prevents a situation where a script runs without error but produces a wrong answer because of a subtle data issue. Any number cited in the report must be traced back to a gate-passing script run, ensuring that no number was copied from a failed or intermediate calculation.

---

**Assertion:** A version-pinned environment manifest (requirements.txt) and a FROZEN_MANIFEST.md list every external URL accessed during the audit with its access date.
**Why?** Why does it matter what version of each software package was used?
**Answer:** Software packages update over time, and different versions can produce different numerical results for the same code. Pinning every package to an exact version means a future researcher installing the pinned environment gets the same computational results the audit got. The FROZEN_MANIFEST.md serves a parallel function for web-accessible data sources: since web pages can change or be deleted, recording the access date and content for every URL lets future researchers verify that the audit's sources said what the audit claims they said.

---

### Appendix B — Supporting Analysis Documents

---

**Assertion:** The full set of supporting documents includes a bias audit, a design critique, methodological defenses, a Fisher combination defense, a Fisher independence defense, and a Warrington declination defense.
**Why?** Why does an audit need to defend its own methodology so extensively?
**Answer:** The audit is designed to withstand adversarial review — not just friendly scrutiny. Each defense document addresses a specific category of objection that a hostile reviewer, a lawyer for the other side, or a skeptical journalist might raise. The Fisher combination defense addresses whether combining two p-values using Fisher's method is statistically valid here. The Fisher independence defense addresses whether the two tests are sufficiently independent to apply that method. The declination defense addresses why a metric that disagrees with the others is still retained rather than dropped. Having these defenses written out in advance means no objection can be met with silence; each has a documented response.

---

**Assertion:** The threshold provenance compendium (`analysis/methodology/threshold_provenance.md`) justifies every numeric threshold with a source and sensitivity analysis.
**Why?** Why does every threshold need its own justification?
**Answer:** A threshold that was chosen after seeing the data — chosen because it happens to produce a finding — is a form of methodological bias. A threshold chosen for documented, independent reasons (from the law, from the academic literature, from the simulation's own distribution, or from first principles) cannot be accused of being designed to guarantee a finding. The compendium exists to make this documentation systematic: for every number used in the audit, a reader can verify where it came from and whether different reasonable choices for that number would change the conclusion.

---

### Appendix C — 2021-Census Legal Baseline (2019 Map)

---

**Assertion:** The 2021-Census-direct computation shows 2019 map MAD = 4,745, majority 2026 MAD = 3,180, minority 2026 MAD = 4,707.
**Why?** Why are there two different MAD figures for the 2019 map (2,886 from the original commission basis and 4,745 from this appendix)?
**Answer:** The 2019 boundaries were drawn using 2011 Census data and 2017-era population estimates, which gave a MAD of 2,886 at the time. When the same 2019 boundaries are evaluated using 2021 Census populations — the data the 2026 commission used to assess current population equality — the MAD rises to 4,745 because those boundaries are now outdated relative to where Albertans actually live. The comparison that matters for assessing the 2026 proposals against the current baseline is the 2021-Census version: 4,745. Under that comparison, the minority 2026 proposal (4,707) is essentially equivalent to the aging 2019 map, while the majority (3,180) represents a meaningful improvement.

---

**Assertion:** Seven 2019 EDs are outside the ±25% band under 2021 Census data, including five fast-growing suburban districts.
**Why?** Does this mean the 2019 map is already unconstitutional?
**Answer:** Being outside the ±25% statutory band is a serious issue but not automatically a constitutional violation — the Saskatchewan Reference standard allows deviations if justified by geography or community of interest. The five fast-growing suburban districts (primarily in south Edmonton and suburban Calgary/Airdrie) are outside the band purely because of population growth since the map was drawn. The audit documents them to establish the context: the 2026 commission was inheriting a population-equality problem that needed fixing, which makes the majority's improvement (MAD 3,180 vs baseline 4,745) a meaningful achievement and the minority's reproduction of the old variance level (4,707) a notable failure to improve.

---

### Appendix D — Mathematical Formalism

---

**Assertion:** The Efficiency Gap formula is EG = (W_A − W_B) / N, where wasted votes include both losing-district votes and winning-district surplus votes.
**Why?** What are "wasted" votes in plain terms?
**Answer:** For a losing candidate, all votes are wasted — they did not elect anyone. For a winning candidate, votes above the bare minimum needed to win are wasted — they were surplus to the purpose of winning that district. If Party A consistently loses races by large margins (wasting many losing votes) and wins races by slim margins (wasting few surplus votes), while Party B wins races by large margins (wasting many surplus votes), Party B is "packing" its own voters and Party A is cracking theirs — or vice versa. The efficiency gap measures whether one party wastes significantly more votes than the other across the entire map.

---

**Assertion:** Sign-convention reconciliation: this audit uses a 1:1 proportional-seat baseline rather than the Stephanopoulos-McGhee 2:1 canonical baseline.
**Why?** Does using a different baseline produce different results?
**Answer:** The choice of baseline affects the numerical value of the efficiency gap but not the ordinal ranking of the three Alberta maps. Under either convention, the minority map is further from zero (more partisan) than the majority map on this metric. The audit documents the convention choice explicitly so readers who compute their own EG from the same data do not get confused by a sign or magnitude difference. The full derivation and verification confirming that both conventions produce the same directional ranking are in `analysis/methodology/sign_convention_resolution.md`.

---

**Assertion:** Mean-Median Gap formula: MM = mean(v) − median(v), where v is NDP vote share across districts. Positive MM indicates mean > median, consistent with packing.
**Why?** Why does mean greater than median indicate packing?
**Answer:** If one party's votes are evenly spread across all districts, the average and the middle value of vote shares would be about the same — the distribution would be roughly symmetric. If that party's votes are packed into a smaller number of districts with very high concentrations, the distribution becomes skewed: a few districts with very high vote shares pull the mean above the median. This skew is the mathematical fingerprint of packed voters. A positive mean-median gap (mean above median) for the NDP means their voters are concentrated in a few high-NDP districts rather than spread across many competitive ones.

---

**Assertion:** Declination formula: δ = (2/π)(arctan((ȳ_R − x̄_R)/x̄_R) − arctan((ȳ_D − x̄_D)/x̄_D)). Alberta results: 2019 = −0.034, majority = −0.021, minority = −0.015. Minority is at p1.21 (NDP-tail).
**Why?** What does the formula actually measure in plain terms?
**Answer:** The declination measures the difference in how steeply each party's win-margin increases as it wins more districts. If Party A's winning margins are concentrated near 50% (many close wins) while Party B's winning margins are spread across both close and blowout wins, declination measures that asymmetry as an angular difference between two trend lines. A negative declination in the Alberta convention means the NDP's wins are harder-earned (closer to 50%) relative to the UCP's wins — consistent with NDP voters being packed in a way that makes their votes "less efficient" at producing wins. The minority's p1.21 means its declination is lower (more NDP-tail) than 98.79% of random maps — disagreeing with the EG and mean-median direction.

---

**Assertion:** Polsby-Popper (PP) results: minority 2026 mean PP = 0.334, majority 2026 = 0.356, 2019 enacted = 0.419. All three pass the gate (mean PP > 0.15).
**Why?** What does Polsby-Popper measure and why does a lower score matter?
**Answer:** The Polsby-Popper score is a shape compactness measure: a perfect circle scores 1.0, and irregular, elongated, or contorted shapes score close to 0. The minority map's districts are, on average, more geometrically irregular than the majority's or the 2019 map's — its lower mean PP reflects more convoluted boundaries. The gate threshold of 0.15 is a very low floor (below which districts are pathologically misshapen); passing the gate means none of the three maps has absurdly shaped districts. The minority's lower score is a noteworthy difference but not a gate failure.

---

**Assertion:** Reock score: Calgary-Nolan Hill-Cochrane scores R = 0.230, which is flagged under the conventional R < 0.30 threshold.
**Why?** Why does Reock catch this district when Polsby-Popper (PP = 0.402) rated it as moderately compact?
**Answer:** Polsby-Popper penalizes wiggly, convoluted perimeters. Reock penalizes elongation — it compares the district's area to the smallest circle that could contain it. A narrow corridor (a "lasso" shape) can have a relatively smooth perimeter (high PP) but still be very elongated (low Reock) because the corridor fits inside a very large enclosing circle relative to its area. The Calgary-Nolan Hill-Cochrane district appears to be a corridor shape that looks geometrically reasonable in terms of perimeter complexity but is flagged as unusual in terms of elongation. H10 in the hypothesis table explicitly tested and confirmed this finding.

---

### Appendix E — Geometric Data Provenance

---

**Assertion:** 47.5% of 2023 valid votes are Vote Anywhere Advance/Mobile ballots; Elections Alberta verified no disaggregated VA-level mapping exists for these ballots.
**Why?** Why does this resolve the question of data precision rather than being a limitation?
**Answer:** If disaggregated data existed, using it would improve the vote attribution. But Elections Alberta confirmed that the data does not exist: the advance ballots are not tracked at the polling-station level in a way that maps them to a geographic location. This means no researcher — regardless of their methods — can do better than the area-weighted spread approach used here. The audit's method is not merely the best available; it is the only mathematically valid approach given the data that exists. The +0.0000 pp shift from the residual geographic error (1,396 votes, 0.15% of the province) confirms the area-weighted method is at the precision ceiling.

---

**Assertion:** Phase 4C (VA-polygon attribution) was intentionally bypassed because it would require ~4–8 hours of compute and yields no measurable precision gain.
**Why?** Why run millions of simulation steps (which take much longer) but not a 4–8 hour attribution pipeline?
**Answer:** The simulation steps are necessary for the ensemble test — there is no shortcut to generating one million legal maps. The VA-polygon attribution pipeline, by contrast, was tested and found to shift the key metric by exactly +0.0000 pp. Spending 4–8 hours to move a critical metric by zero percentage points is not a precision gain; it is computational work with no impact on findings. The audit documents this explicitly so reviewers understand the bypass was a principled decision, not a shortcut taken to avoid inconvenient results.

---

**Assertion:** DPG Tier A/B compactness findings were superseded on May 6, 2026, upon receipt of the canonical shapefiles.
**Why?** What happened to findings that were based on the provisional geometry?
**Answer:** The DPG findings are archived rather than deleted. Any finding that was computed on DPG and that had material uncertainty is flagged as superseded; findings that survived canonical recomputation are updated with the canonical values. The audit's formal position is that the canonical values are authoritative. The DPG values are historical record — they show what the analysis showed before better data arrived — and are preserved because transparency requires showing the full history of the work, including the values that changed.

---

### Appendix F — Legal Interpretive Note

---

**Assertion:** The audit does not offer a legal conclusion; it provides the evidentiary basis on which a legal challenge could be constructed.
**Why?** Why is the distinction between evidence and legal conclusion important?
**Answer:** A legal conclusion — such as "this boundary violates the Charter" — requires findings of fact and law that are within a court's authority to make. The audit is a public-interest empirical document; it can measure statistical patterns and document procedural departures, but it cannot adjudicate intent, apply legal standards, or grant remedies. By explicitly positioning its findings as evidence rather than conclusions, the audit avoids overstepping its competence and remains a credible input for legal proceedings rather than an advocacy document.

---

**Assertion:** The *Saskatchewan Reference* requires holistic assessment; there is no bright-line variance ceiling. Partisan asymmetry, standing alone, does not trigger a violation.
**Why?** If there is no bright-line test, how would a court ever find a violation?
**Answer:** Courts applying the Saskatchewan Reference look at the totality of evidence: are population deviations justified by genuine geographic necessity or community preservation, or do they appear to serve partisan purposes? Is there evidence that non-partisan factors were invoked post-hoc to rationalize predetermined choices? The audit provides exactly the kind of evidence a court would examine under that holistic test: directional consistency across six independent measurements, rationale failures where stated reasons do not hold up against cleaner alternatives, and procedural departure from comparator Canadian practice. A court would weigh all of this together, not look for a single threshold violation.

---

**Assertion:** Adverse characterizations of named public officials are defensible under *Grant v. Torstar* (responsible communication) and *WIC Radio* (fair comment).
**Why?** Why does a technical audit need to discuss defamation defenses?
**Answer:** The audit characterizes specific statements made by the commission chair and specific boundary choices made by named commissioners as not holding up against the primary-source evidence. These characterizations could theoretically form the basis of a defamation complaint. The audit's legal note addresses this by documenting that all characterizations are (a) grounded in publicly verifiable facts from official documents, (b) made in a context of genuine public interest (electoral boundaries affecting all Albertans), and (c) clearly framed as inferences from the public record rather than assertions about private intent. Both Canadian defamation defenses cited protect exactly this kind of public-interest accountability reporting.

---

**Assertion:** The seven *Grant v. Torstar* diligence factors are all satisfied by the audit's methodology.
**Why?** What are the seven factors and why does each apply?
**Answer:** The Grant v. Torstar test asks whether the person publishing the characterization took reasonable steps to verify it and presented it responsibly. The seven factors include: seriousness of the allegation (electoral process legitimacy is serious), public importance (yes — boundaries affect every voter), urgency (the audit was conducted before the April 16 vote), reliability of sources (all public records), verification (all claims are reproducible), inclusion of the subject's side (the commission's own rationales are quoted and analyzed), and justifiability (the factual record is publicly accessible for anyone to check). The audit satisfies each because it is a methodologically rigorous document built entirely on public-record sources.

---
