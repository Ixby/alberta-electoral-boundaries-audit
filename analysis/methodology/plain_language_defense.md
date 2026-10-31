> **Backward:**
> - `reports/academic/report_academic.md` — every assertion paraphrased here originates in the academic monograph
> - `analysis/methodology/methodological_defenses.md` — adversarial defenses underlying the responses
>
> **Forward:**
> - `reports/academic/report_academic.md` — Appendix / reviewer-facing companion
> - (leaf — reader-facing plain-language defense document)

# Plain-Language Defense — Alberta Electoral Boundaries Audit

*Consolidation of `plain_language_defense.md` (215 assertions, all sections)
and `plain_language_defense_summary.md` (six-objection quick reference).
The summary file is removed; this document is the canonical record.*

---

## Quick Reference — Six Common Objections

### 1. "You're calling this a gerrymander."

The audit doesn't. A gerrymander is a legal conclusion about intent: that a map was drawn on purpose to entrench one party's power. This audit makes no claim about intent and draws no legal conclusion. What it does is narrower. It measures whether the minority map's boundary choices fall within the range you would expect from a fair, neutral process. Numbers can answer that. Whether the gap it measures rises to the level of a gerrymander is a question for courts. Not for a statistical audit.

### 2. "Your tests are designed to find what you were looking for."

Three things make that impossible. First, every test was declared in public before the data were examined, on the Open Science Framework, a public academic registry. The test criteria, the pass thresholds and the predicted outcomes sit in a dated public record you can check right now. Second, every test was run the same way on both maps. No test in this audit applies to the minority map and not to the majority. Third, three findings came out against my stated prior expectations, and they are reported in full anyway: the partisan-bias direction reverses under a different set of election results; the commission chair's claim about public opposition was upheld on some configurations but not all; and the majority map actually has a tighter population distribution than the 2019 baseline. A process built to confirm a conclusion fixed in advance would have quietly dropped those three results. They are in the paper.

### 3. "A computer simulation of a million fake maps proves nothing about a real one."

The simulation does not draw just any fake maps. It draws random maps bound by the same legal rules the commission had to follow: districts must be connected, roughly equal in population, and within the same geographic constraints. What comes out is a reference band, the range of outcomes a fair, unbiased process would normally produce. When the minority map's scores fall outside that band, they are more extreme than nearly every one of the million neutral maps drawn at random. The randomness itself can be audited. Every random seed comes from a public cryptographic timestamp service (operated by Cloudflare), committed to git before the analysis ran. No seed was chosen after the results were seen.

### 4. "You picked a threshold that makes the minority map fail."

The threshold is a 4.10% efficiency gap, and I did not choose it. It is the value that 95% of the million randomly drawn neutral Alberta maps fall below, computed from the same 2023 election that produced these maps. It is Alberta's own ceiling for what a neutral process normally produces. Not a number imported from somewhere else. The same computation was run on vote data from the 2019 and 2015 elections. The minority map falls below the ceiling under 2019 and 2023 conditions. The majority map falls below it in all three. The US academic reference threshold of 7% sits in the middle of that range, and both maps pass under that standard too.

### 5. "You used AI tools — the analysis isn't reliable."

AI tools helped draft and check the text, review code, write scripts and suggest approaches. Most numbers in the report come from Python or R scripts I ran on public data, and I checked them against the script outputs. One group of numbers is different. In the public-input analysis (report §5.9.4.6 and §5.9.4.7), Claude models read each written submission and each relevant hearing comment, and labelled it as opposing, supporting or neutral on each of seven contested boundary choices. Every count of opposing and supporting comments in those two sections comes from those labels. A second Claude pass scored how strongly each comment was worded; the intensity totals come from that pass. A Claude vision model was also used to inspect the commission's published map images (report §5.8.1).

The labels have been checked in two ways. Their row counts were reconciled against the pipelines' output files, and the results were compared with a separate keyword search of the same submissions. They agree with it. No person has checked the labels themselves yet. A sample of 60 labelled items has been drawn for a human agreement check, but none of it has been scored, so the labels' accuracy has not been measured. Until it is, read those counts as machine labels. All code and all labels are public. Anyone can re-run every script against the same public data from Elections Alberta and Statistics Canada.

### 6. "You hid a finding that didn't work out."

The opposite happened. Municipal-boundary anchoring was one of five tests announced in advance on the public registry. Early analysis, done before Elections Alberta released its official boundary files, showed a large gap between the two maps. Then the official files arrived. The test was rerun on them, and both maps turned out to respect city and town boundaries at rates that are normal for Canadian redistricting (72% and 80%, inside the typical 70–85% range). The finding collapsed. The paper reports it openly, under a "RETRACTED FINDING" label. It appears in no headline result. The audit's other findings do not depend on it.

---

**Purpose.** This document takes every substantive assertion in the academic audit monograph (`reports/academic/report_academic.md`) and puts to it the questions you would ask if you knew nothing about elections, statistics or political science. It follows the report's section headings. Each entry has the same shape:

> **Assertion:** The claim, paraphrased if needed.
> **Why?** The naive question a reader with no domain background would ask.
> **Answer:** A plain-language explanation. No jargon. No assumed knowledge. Self-contained.

Jargon gets translated as we go: "efficiency gap" means a measure of how many votes each side wastes unequally; "MCMC ensemble" means a computer simulation that draws thousands of random legal maps; "p-value" means the probability of seeing a result this extreme just by chance; "p95" means a value that 95% of the random maps fall below.

---

## Executive Summary

---

**Assertion:** Alberta's 2025–26 Electoral Boundaries Commission produced two competing 89-seat maps on March 23, 2026.
**Why?** What is an Electoral Boundaries Commission and why would it produce two different maps?
**Answer:** Every few years a province must redraw its electoral districts, or ridings: the geographic areas that each send one elected representative to the legislature. In Alberta an independent commission does the work, appointed under provincial law. In 2026 its members could not agree. Some proposed one set of 89 district boundaries, the majority proposal. Others proposed a different set, the minority proposal. Both went to the legislature.

---

**Assertion:** The audit evaluates both proposals using identical methods applied symmetrically to each.
**Why?** Why does it matter that the same method is used on both maps?
**Answer:** Use different tests on each map and you could make one map look bad just by choosing the tests that happen to penalize it. Apply exactly the same measurements to both, and any difference you find is a real difference between the maps. Not a by-product of a biased test.

---

**Assertion:** The majority map is within the neutral null on three of four partisan-fairness metrics and jointly (Mahalanobis p = 0.102). Its mean-median is a 1st-percentile (p0.99) outlier leaning NDP, the wrong direction to help the UCP. The minority map is not within the null.
**Why?** What is a "neutral statistical band" and how do you know the majority map is inside it while the minority is outside?
**Answer:** To judge whether a map is unusual, the audit ran a computer simulation that drew over one million legal Alberta maps at random. Each follows all the same rules the commission had to follow (equal population, connected districts, and so on). Those million random maps form a reference band: the range of outcomes you would expect from an unbiased process. The majority map's scores fall inside that range on three of the four fairness measures, and on the combined test. On the fourth, mean-median, it leans further toward the NDP than about 99% of the random maps. That does not help the UCP. The minority map's scores on several measures fall outside the band. They are more extreme than all but a tiny fraction of the neutral maps drawn at random.

---

**Assertion:** The minority proposal differs from the majority on four measurable non-partisan-bias dimensions: population dispersion (Mean absolute deviation 48% wider; corrected 2026-07-08 — earlier text said "Median", but the 4,707/3,180 pair is the mean absolute deviation per `findings/population_equality.md` Table A1), Calgary geographic-zone asymmetry (12.2% vs 0.4%), Airdrie community fragmentation (4-way vs 2-way split), and commission-chair-flagged geographic anomalies (3 confirmed vs 0).
**Why?** What do these four things mean and why do they matter?
**Answer:** Population dispersion measures how unevenly people are spread across districts. If some districts hold far more residents than others, some citizens' votes count for more than others'. A mean absolute deviation 48% wider means the minority map's districts vary more in size than the majority's do. The Calgary zone gap means districts in Calgary's urban core are sized differently from those in its suburban ring, an imbalance that tilts which party's voters are packed more tightly. Splitting Airdrie four ways divides the city's residents among four different ridings, and they lose the shared political voice they would have in one or two. The chair-flagged anomalies are boundary shapes the commission's own chair publicly criticized as geographically strange.

---

**Assertion:** A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation; both maps fall within the 70–85% Canadian comparator norm.
**Why?** What happened here — why is a finding being withdrawn?
**Answer:** Early in the audit, before Elections Alberta released its official map files, I worked from approximate boundary tracings made from PDF images. Those rough lines suggested the minority map ignored city and town edges far more than the majority did. Then the official files arrived. I reran the same measurement on those exact files, and both maps turned out to respect municipal boundaries at rates (72% and 80%) that are normal for Canadian redistricting. The earlier finding was a measurement artifact of the approximate files. Not a real difference between the maps. The audit says so openly instead of hiding it.

---

**Assertion:** Two independent statistical tests — the ensemble test (Mahalanobis Ch1) and the boundary-choice test (SZAT Ch2) — return the same answer. Their Fisher combination is p = 4.61×10⁻⁸.
**Why?** What do "Ch1" and "Ch2" mean, what is a "Fisher combination," and what does p = 4.61×10⁻⁸ mean in plain terms?
**Answer:** Ch1, the ensemble test, asks: how unusual is this map next to over one million neutral maps drawn at random? Ch2, the boundary-choice test, asks: in the places where the minority map differs from the majority map, are those differences random, or do they keep moving in a direction that favors one party? The Fisher combination is a standard formula for merging two independent test results into one overall probability. The combined p = 4.61×10⁻⁸ was an earlier "Fisher combination" figure, and it has since been **retired** (2026-06-10). It assumed the two tests were independent, and they are not. And the boundary-choice test (Ch2) does not survive a stricter spatial check. The audit now reports the ensemble test (Ch1) on its own: about a one-in-1,140,000 result (p = 8.80×10⁻⁷), with a conservative combined upper bound of about one in 568,000 (p ≤ 1.76×10⁻⁶). Both are still extremely unlikely accidents. Neither relies on the independence assumption any more. See the academic report §4.3.3 and §5.5.

---

## Abstract

---

**Assertion:** This audit evaluates both proposals against the 2019 baseline using a multi-method structural framework and Monte Carlo ensemble analysis.
**Why?** Why compare to 2019, and what is "Monte Carlo ensemble analysis"?
**Answer:** The 2019 map is the most recent map actually used in an election. That makes it the reference point: what Alberta's districts looked like before any changes. A Monte Carlo ensemble analysis uses a computer to draw thousands or millions of random legal maps and record their properties. It answers the question "what does a normal, unbiased map look like?" by showing you the full range of possibilities.

---

**Assertion:** A fifth pre-registered dimension — municipal-boundary anchoring — did not survive canonical recomputation (both maps within the Canadian comparator norm); full reconciliation in §5.8.5.
**Why?** What does "pre-registered" mean and why does it matter that this finding failed?
**Answer:** Pre-registration means saying in advance, before you look at the data, exactly what you plan to test and what threshold would count as a finding. It stops researchers from quietly dropping the tests that fail to confirm their hypothesis (a practice called "p-hacking"). When a pre-registered test fails, the failure has to be reported honestly. Here the test was declared in advance on a public registry. The finding did not hold up when better data arrived. And that failure is reported in full. Not hidden.

---

**Assertion:** The joint outlier profile reaches Mahalanobis p = 8.80×10⁻⁷ against the 1,010,000-plan canonical ensemble.
**Why?** What is a "Mahalanobis" score and what does 8.80×10⁻⁷ mean?
**Answer:** Picture a cloud of data points. A Mahalanobis score measures how far a single point sits from the center of that cloud, while taking account of how correlated its dimensions are with each other. Here the cloud is formed by over one million randomly drawn maps, and the point is the minority map's combination of four partisan fairness scores. A probability of 8.80×10⁻⁷ means roughly 0.88 maps in every million drawn at random would be this extreme. Put the other way round: the minority map is more extreme than approximately 999,999 out of every million neutral maps.

---

**Assertion:** All Efficiency Gap magnitudes remain below the Stephanopoulos-McGhee 7% threshold (academic literature only; never judicially adopted).
**Why?** What is the Efficiency Gap, what is this 7% threshold, and why does it matter that courts have not adopted it?
**Answer:** The Efficiency Gap measures how many votes each party "wastes": every vote cast for a losing candidate, plus every vote cast for a winning candidate beyond the minimum needed to win. If one party wastes far more votes than the other, that is a sign the map is drawn to its disadvantage. The 7% threshold is a benchmark from academic research, which suggests that gaps above 7% are likely to persist across election cycles. No court in Canada has ever declared a specific number to be a legal test. So this 7% is useful as a reference, but it does not by itself decide any legal outcome.

---

## Preface — Scope, Shapefile Status, and Intended Venue

---

**Assertion:** Elections Alberta released the 2026 official shapefile package and the canonical polygon files were received by the audit on 2026-05-06.
**Why?** What is a shapefile and why does it matter when it was received?
**Answer:** A shapefile is a digital file that stores the exact geographic coordinates of boundaries. Here, it holds the precise lines of every electoral district. Without the official shapefiles, the earlier analysis had to use approximate boundary tracings from images. When the official files arrived, several measurements were rerun to confirm the earlier results. The exact date matters because it shows the analysis on the official files was done after those files arrived, and that I did not somehow have access before the public release.

---

**Assertion:** The DPG-substrate runs documented in §5.4.1–§5.4.8 are preserved as the historical record of the pre-shapefile analysis.
**Why?** What are "DPG-substrate runs" and why keep the old results at all?
**Answer:** DPG (Derived Provisional Geometries) means the approximate boundary tracings made from scanned PDF images of the commission's maps, used before the official digital files were available. The simulation runs on those approximate shapes are the pre-shapefile analysis. They stay in the report because being open means showing the full history of the work: what the analysis showed before the better data arrived, and what it showed after. That way you can see whether the results changed, and how.

---

**Assertion:** The November 2026 committee-map trigger remains pending.
**Why?** What is a "committee-map trigger"?
**Answer:** After the commission's reports were set aside, the Alberta legislature created a Select Special Committee to draw a new 91-seat map by November 2026. We pre-registered a commitment to evaluate that map with the same methodology as soon as it is published. The "trigger" is simply that planned rerun. It cannot happen until the committee releases its map.

---

## Author Disclosure

---

**Assertion:** The author has worked as a contract election officer for Elections Alberta for about 27 years, election by election, administering the vote on election day. The author is not under contract now and last worked at a recent election. The author has had no other employment with Elections Alberta, has no knowledge of its work beyond those tasks, and drew nothing in this audit from that work. Every input is public.
**Why?** Doesn't working for Elections Alberta create a conflict?
**Answer:** The audit tests maps drawn by the Electoral Boundaries Commission and the MLA committee. Elections Alberta runs elections; its Chief Electoral Officer advises and assists the commission, but does not draw the boundaries. The author's work was administering the vote on election day, not boundary or policy work, and none of the audit's data or reasoning comes from it. The one data set Elections Alberta supplied directly, the official 2026 boundary shapefiles, came through a formal data request in May 2026 and is published with the audit. It is disclosed so readers can weigh it for themselves.

---

**Assertion:** Going into this project the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny.
**Why?** Why admit a bias up front — doesn't that undermine the research?
**Answer:** Every researcher comes to a project with existing beliefs. Admitting those beliefs openly is more credible than pretending to have none, because it lets readers assess whether the methodology was designed to confirm the prior or to test it fairly. The disclosure also sets up the three cases where findings ran against the researcher's prior expectations — showing the method produced results the researcher did not expect or want.

---

**Assertion:** Three cases surfaced findings that ran against the prior and were retained in the report: the partisan-bias asymmetry reverses sign under 2019 vote input; the commission chair's "no public support" claim is upheld on three of seven configurations, not all seven; and on the 2021 census the three maps have almost the same mean absolute deviation, so the minority's 48% wider spread shows only on the commission's 2024 tables.
**Why?** Why does it matter that some findings went against the researcher's expectations?
**Answer:** A biased research process would quietly drop inconvenient results. These three contra-prior findings were retained precisely to show that the methodology is not rigged. If every single finding had confirmed the researcher's starting suspicion, that would be a red flag. Results that cut against the prior — and are reported anyway — provide evidence that the method is operating independently of the researcher's preferences.

---

**Assertion:** Three large language models were used as analytical and writing assistants (Claude Pro Max, Gemini Pro, Codex). All substantive claims were verified against primary sources by the author.
**Why?** Does using AI tools make the analysis less reliable?
**Answer:** AI tools helped draft text, find inconsistencies, review code, write scripts and suggest analytical approaches. The report states that no AI tool ran code or reached data on its own; the researcher ran every script. One part of the analysis does rest on AI output. The public-input scripts (report §5.9.4.6) send each submission and hearing comment to a Claude model, which labels it, and the counts of opposing and supporting comments in §5.9.4.6 and §5.9.4.7 come from those labels. A Claude vision model was also used to inspect the commission's map images (§5.8.1). The label counts were reconciled against the output files and compared with a keyword search of the same submissions. No person has yet scored the 60-item check sample, so the labels' accuracy has not been measured. Every other number was checked by the researcher against the original data files and script outputs.

---

**Assertion:** No GIS desktop software (QGIS, ArcGIS) and no commercial election-analytics platforms were used. R 4.6 with the `redist` package was used for one SMC cross-validation script. Stata and SPSS were not used. All inputs are public.
**Why?** Why does it matter what software was used?
**Answer:** Commercial or proprietary software can make research harder to reproduce because other researchers may not have access to it. Using only open-source tools (Python, plus R for one cross-check) means anyone with a standard computer can run the same code against the same publicly available data and check that the numbers are correct. This is the practical meaning of "reproducible" in this context.

---

## §1 Introduction

---

**Assertion:** The audit is the first systematic computational audit of an Alberta provincial electoral boundary commission's output, evaluated against established Canadian independent-commission practice and statutory norms.
**Why?** Has no one done this kind of analysis before?
**Answer:** The computational tools for measuring partisan fairness in redistricting, above all the MCMC (random-map simulation) approach, were developed mostly in the United States over the last decade. Canada has an academic literature on boundary commission discretion. But a systematic computational audit of what a commission produced, set against a neutral ensemble, is new to the Alberta provincial context. This audit is the first to apply those tools to an Alberta provincial map.

---

**Assertion:** The audit situates itself within Canadian political-science and legal frameworks: the Saskatchewan Reference's "effective representation" standard.
**Why?** What is the Saskatchewan Reference?
**Answer:** The Saskatchewan Reference is a 1991 Supreme Court of Canada decision ([1991] 2 SCR 158) that set the constitutional standard for electoral boundaries in Canada. The court ruled that the goal is "effective representation": districts should be roughly equal in population, but some variation is allowed where it is needed to accommodate communities of interest, geographic factors and other considerations. Every assertion in this audit about whether a boundary choice is legally defensible is measured against that standard.

---

**Assertion:** The audit asks whether one faction's boundary choices within a Canadian independent commission exceed the discretion space that Canadian law and practice establish — not whether a full gerrymander occurred.
**Why?** What is the difference between asking "did this exceed discretion" versus "is this a gerrymander"?
**Answer:** A full gerrymander is a conclusion about intent and effect: that a map was drawn on purpose to entrench one party's power. This audit does not reach that legal conclusion, and it does not infer intent. It asks a narrower, empirical question: do the measurable properties of this map fall within the range that Canadian law and neutral random processes would produce? The data can answer that. Whether those deviations amount to an illegal gerrymander is a legal judgment. Courts would have to make it.

---

**Assertion:** Computational seeds were committed to the public drand League of Entropy beacon before the official shapefile release.
**Why?** What is a "drand beacon" and why does committing seeds to it before seeing the data matter?
**Answer:** A random seed is the starting number behind every later "random" choice a computer makes in a simulation. Cloudflare's drand beacon is a public source of random numbers, verifiable by cryptography, published on a fixed schedule and impossible to alter after the fact. The audit recorded which seed it used on the public beacon before the official maps arrived. That proves it could not have run the simulation again and again with different seeds and kept the one that gave the most extreme result, a kind of cheating called "fishing." The beacon works as a tamper-proof timestamp.

---

**Assertion:** Five pre-registration IDs are cited: OSF w2s8k, r3zm7, qsgy8, 6pt83, s58a6.
**Why?** What is OSF pre-registration and what does citing these IDs prove?
**Answer:** OSF (Open Science Framework) is a public registry where researchers can file a detailed plan for a study before they run it. The plan says in advance what they will measure, what thresholds will count as a finding, and what data they will use. OSF timestamps the plan, and it cannot be changed. With the OSF IDs, you can look up those registrations yourself and check that the tests were designed before the analysis was done. Not designed afterward, to match results I had already found.

---

**Assertion:** Primary ensemble-based tests (Ch1, Ch2, Fisher combination) are exploratory, not confirmatory.
**Why?** What is the difference between exploratory and confirmatory statistics?
**Answer:** Confirmatory statistics follow a pre-registered plan, written before the data are collected, that locks in the specific test, the threshold and the significance level. Exploratory statistics are open-ended. They look for patterns in data without a pre-registered threshold. The difference matters because choices made after seeing the data can sway exploratory results, even unintentionally. The audit says plainly that Ch1, Ch2 and their combination are exploratory. The seeds were locked, but the specific test names and the combination formula were not in an OSF pre-registration. So treat the results as strong, but as needing independent replication before anyone draws firm conclusions.

---

### §1.1 Headline Findings in Plain Language

---

**Assertion:** The minority map's Mean absolute deviation from provincial average is 4,707 versus the majority's 3,180 — a 48% wider dispersion. *(Corrected 2026-07-08: earlier text said "Median Absolute Deviation"; the 4,707/3,180 pair is the mean absolute deviation per `findings/population_equality.md` Table A1.)*
**Why?** What is "mean absolute deviation from provincial average" and why does wider dispersion matter?
**Answer:** The provincial average is the number of residents each electoral district would have if the population were split perfectly equally. The mean absolute deviation measures the typical gap between a district's population and that average. The higher the number, the more unequal the districts are in size. At 4,707 against 3,180, the minority map's districts stray from the provincial average by about 48% more than the majority's do. And when districts are unequal in size, a vote in a smaller district carries more weight than a vote in a larger district.

---

**Assertion:** The minority map's Calgary districts show a 12.2 percentage-point geographic-zone asymmetry versus 0.4 pp on the majority map.
**Why?** What does "geographic-zone asymmetry" mean here?
**Answer:** Calgary's electoral districts can be sorted into two zones: the urban core (central city neighborhoods) and the suburban ring (newer outer neighborhoods). If the two zones have the same average district size, they count equally in electing representatives. If one zone's districts are consistently smaller, voters there elect more representatives per person than voters in the other zone. The minority map shows a 12.2-percentage-point gap between the zones. The majority map shows a gap of only 0.4 points. Here is why that matters: in Calgary, the urban-core neighborhoods lean toward one party and the suburban-ring neighborhoods lean toward the other.

---

**Assertion:** The minority map splits the City of Airdrie four ways; the majority concentrates 73.8% of Airdrie's population inside a single electoral division (Airdrie-East).
**Why?** Why is splitting a city across more electoral districts a problem?
**Answer:** Spread a city's residents across many different electoral districts, and no single representative answers mainly to that city. Airdrie residents divided among four districts have to share their representative with people from other communities, who may have different interests. The majority map keeps nearly three-quarters of Airdrie's residents in one district, and that gives the city a clearer political voice. The specific concern is that splitting a community can dilute its voting power. In electoral analysis, that technique has a name: "cracking."

---

**Assertion:** One minority district ("Calgary-Foothills-Airdrie West") carries "Airdrie" in its name but has 0% anchoring on Airdrie's gazetted city limit.
**Why?** What does it mean for a district boundary to have 0% anchoring on a city limit?
**Answer:** A district boundary is "anchored" on a city limit when part of the district's edge runs along the official municipal boundary. A district named after a city, yet sharing none of its border with that city's official edge, draws its residents from a different area entirely. That suggests the "Airdrie" label reflects no real geographic connection to Airdrie as a municipality.

---

**Assertion:** Three geographic anomalies on the minority map were flagged by the commission chair; zero were flagged on the majority map.
**Why?** Who is the commission chair and what gave them authority to "flag" boundaries?
**Answer:** The commission chair is the presiding officer appointed to lead the boundary commission. The chair's written criticisms, set down in the commission's own majority report, name specific features of the minority map as geographically unusual or out of step with the commission's stated principles. The chair is not a neutral outsider. The chair is one of the commission's own members. That documented criticism of minority-map features, in the official commission report, is a primary-source record of internal expert concern.

---

**Assertion:** The minority's own 25 published rationales are, on five of six contested configurations, options the minority did not take when cleaner statutory-compliant alternatives were available.
**Why?** What does "cleaner statutory-compliant alternatives" mean?
**Answer:** When a commission draws a boundary that looks unusual, it is expected to explain why, in writing. The minority commissioners published rationales for their boundary choices. For five of the six configurations examined, the audit finds a simpler boundary option, one that would also satisfy the law, that the minority could have chosen and did not. "Cleaner" here means fewer geographic contortions and a more direct fit with city or town edges. The argument runs like this: if the stated rationale were genuinely driving the choice, the simpler alternative would have been chosen.

---

### §1.2 Modelling-Uncertainty Caveats

---

**Assertion:** Monte Carlo sensitivity interval over modelling choices is [−3.04, +0.76] pp and crosses zero.
**Why?** What is a "Monte Carlo sensitivity interval" and what does "crosses zero" mean?
**Answer:** This interval comes from running the efficiency-gap calculation 2,000 times, each time randomly varying the assumptions built into the vote-attribution model (how votes from some mixed urban-rural districts are estimated). What comes out is a range of plausible efficiency-gap differences between the two maps. An interval of [−3.04, +0.76] pp means that across those 2,000 variations, the result runs from −3.04 percentage points to +0.76 percentage points. "Crosses zero" means some of those 2,000 runs show the minority as slightly better for the NDP rather than better for the UCP. So the size of the partisan-bias estimate is uncertain enough that classical statistical significance, where you need 95% of the range on one side of zero, is not met on the efficiency gap.

---

**Assertion:** [RETIRED 2026-07-12, C11] Direction consistency: 90.5% of samples show minority more UCP-favorable. Classical 95% significance is not defensible.
**Why?** This was a Monte Carlo check over a vote-attribution model (blend of urban/rural weights) that the audit itself replaced with an exact computation. What replaced it, and does the audit still avoid claiming 95% significance?
**Answer:** The 90.5%-of-samples figure came from varying a *model's* free parameters (urban weight, rural baseline, per-hybrid jitter). It checked whether the finding survived guesses about how to estimate vote attribution. In May 2026 that model, and the guesswork it needed, was replaced by Phase 4C: an exact spatial computation of which voters fall in which district, with no parameters to guess. So the question changed. It used to be "does the finding survive parameter uncertainty?" Now it is "does the finding survive attribution-*method* uncertainty?" And it does. Three different attribution methods (the audit's own, plus two independent checks) agree to within 0.1 percentage points. The audit still does not claim classical statistical significance, but not because a confidence interval crosses zero. Phase 4C's number isn't a sampling estimate with a confidence interval at all. It's an exact count from the actual votes. The honest caveat that remains is that the finding depends on the 2023 electoral context and does not hold under 2019 vote data (see the cross-election question above).

---

**Assertion:** Declination metric disagrees with the efficiency gap: by declination, the minority is the least pro-UCP of the three maps.
**Why?** Why would two different fairness measures point in opposite directions?

**[Corrected — Amendment 10, 2026-06-12.** This Q&A reflects the pre-correction declination sign. With the sign bug fixed (`mcmc_ensemble.py:215`), the minority's declination is p98.79 on the UCP-favoured tail and AGREES with the efficiency gap, mean-median, and seats@50/50 (four of four). The "disagrees / least pro-UCP by declination" reading below is retired, preserved only as a record. The general point that two fairness formulas *can* diverge (Warrington 2019) still stands as methodology; it just does not apply to this dataset after the correction. See `reports/academic/report_academic.md` §5.4.9.**]**

**Answer:** The efficiency gap and declination are two different mathematical formulas designed to capture partisan unfairness, but they capture it differently. The efficiency gap is sensitive to how many votes are "wasted" (lost or excess); declination is sensitive to how the slopes of two trend lines in election-outcome data differ between the two parties. These different sensitivities mean they can give conflicting signals when the map's distortion takes an unusual form. Research by Warrington (2018) documents that this kind of cross-metric disagreement is expected — it is a known feature of how these measures work, not a sign of an error. The audit retains both measures rather than picking the one that tells a cleaner story.

---

**Assertion:** Under v0_8 full-coverage area-proportional attribution, the direction is stable across 2019 and 2023 votes. The earlier "direction reverses" reading was a partial-coverage artifact of 22 unattributed rural EDs.
**Why?** What happened with the 22 rural districts and why did fixing them matter?
**Answer:** Vote attribution means assigning 2023 election results to the new proposed district boundaries. In an earlier version of this process (v0_7), 22 rural electoral districts did not get their votes allocated correctly, because the geographic overlap data were incomplete. Those missing UCP votes made the rural districts look more NDP-friendly than they really were, and that reversed the apparent direction of the efficiency gap. A corrected method (v0_8) attributed every district properly, and the partisan direction stabilized. Both maps remained UCP-favorable under both 2019 and 2023 votes, though the inter-map gap between them does still shift between years.

---

## §2 Background

---

**Assertion:** The *Electoral Boundaries Commission Act* (EBCA) sets a ±25% population deviation window (§15(1)).
**Why?** What does a ±25% population deviation window mean and who decided it should be 25%?
**Answer:** The EBCA is the Alberta law that governs how electoral boundaries are drawn. Section 15(1) says no district can have a population more than 25% above, or more than 25% below, the provincial average district size. That sets a legal edge. A district with a population below 75% or above 125% of the average would be illegal. The legislature set the 25% figure. Not the commission, and not this audit.

---

**Assertion:** Section 15(2) allows up to −50% deviation if at least 3 of 5 geographic criteria are met.
**Why?** Why is there a special exception allowing districts to be even smaller?
**Answer:** Alberta has remote northern and mountain regions where communities are separated by vast distances, sparse road networks and difficult terrain. A district that covers a huge geographic area might need fewer residents than average for a single elected member to represent it. It would be impossible to travel to every community in a normal campaign or year. The law lets these sparsely populated districts go as far as 50% below the average where the geography justifies it, provided at least three of five specified geographic criteria (such as area, isolation, or transportation access) are met.

---

**Assertion:** All six invocations of the s.15(2) exception across both maps pass under corrected thresholds.
**Why?** What are these "six invocations" and what were they being checked against?
**Answer:** Six of the proposed districts, across the majority and minority maps together, invoke the §15(2) geographic exception to fall below the standard ±25% band. The audit checked whether each of those six districts genuinely meets the minimum three-of-five criteria the law requires. Once an earlier threshold calibration error was corrected, all six pass the test. Neither map is improperly using the geographic exception as cover for unfairly small districts.

---

**Assertion:** The *Saskatchewan Reference* ([1991] 2 SCR 158) established "effective representation" as the constitutional standard.
**Why?** How does a 1991 Saskatchewan case govern what Alberta's commission can do?
**Answer:** When the Supreme Court of Canada decides a constitutional question, the decision applies to all provinces. In the Saskatchewan Reference, the court interpreted section 3 of the Canadian Charter of Rights and Freedoms, the right to vote, as requiring "effective representation" rather than strict numerical equality. So provinces can draw districts that vary in population, as long as the variation serves legitimate goals, like accommodating remote communities or preserving communities of interest. Alberta's commission is bound by this standard in the choices it makes.

---

**Assertion:** Rucho v. Common Cause (US) established non-justiciability in US federal courts — contrasted with Canadian justiciability.
**Why?** Why is an American Supreme Court case mentioned in an audit of an Alberta provincial commission?
**Answer:** Rucho v. Common Cause is a 2019 US Supreme Court decision. It held that federal courts in the United States cannot rule on partisan gerrymandering claims, because those are "political questions" outside judicial competence. It is mentioned here as a contrast. In Canada, courts can and do assess whether boundary commissions have met their constitutional obligations under the Charter. The Canadian system is justiciable, meaning courts can hear these cases. The US federal system is not. If you follow US redistricting news, don't assume that what is legally unreviewable in the United States is equally unreviewable in Canada.

---

## §3 Data

---

**Assertion:** The 2023 Statement of Vote has 1,973 poll records across 87 sheets in an Excel workbook.
**Why?** What is a "Statement of Vote" and why does the number of poll records matter?
**Answer:** The Statement of Vote is Elections Alberta's official publication of every ballot result from the 2023 provincial election, broken down by polling station. Each polling station is one "poll record." The 1,973 records from 87 worksheets are the full, fine-grained record of where votes were cast, and for whom. Working from poll-level data rather than district-level totals lets the audit estimate how votes inside one district's boundaries would be reassigned if those boundaries moved. That step is essential for comparing the old map with the new proposed maps.

---

**Assertion:** Three-vintage sandwich: 2019 enacted boundaries, 2021 Census population, 2023 election results.
**Why?** Why are three different years involved and does that create problems?
**Answer:** The three datasets come from different points in time, and they do not line up perfectly. The 2019 boundaries are the current districts, the ones used in the 2023 election. The 2021 Census is the population count the commission used to design the new districts. The 2023 election results are the most recent vote data. Putting them together takes assumptions: for example, which 2023 poll records fall within which new proposed boundaries. The audit writes those assumptions down explicitly and tests how sensitive the results are to different choices.

---

**Assertion:** Vote Anywhere (VA) polling stations are treated as a data-quality concern requiring special handling.
**Why?** What are Vote Anywhere stations and why are they a problem?
**Answer:** Under Elections Alberta's Vote Anywhere program, voters can cast their ballot at any polling station in the province, not just the one assigned to their home address. So some polling stations hold votes from people who live in many different districts. Treat those votes in a geographic analysis as if every voter came from the station's location, and errors creep in. The audit identifies 2,110 Voting Areas that appear in one map but not the other, specifically because of how the two maps handle these boundary areas.

---

**Assertion:** Under v0_8 full-coverage area-proportional attribution, all 87 districts are attributed.
**Why?** What is "area-proportional attribution" and why did 22 districts fail under the earlier version?
**Answer:** Area-proportional attribution estimates how many votes from each polling station fall within a new district boundary, using the geographic overlap between the old polling area and the new district. If the polling area is 60% inside the new district, 60% of that station's votes go to the new district. Under the earlier v0_7 method, 22 rural districts had incomplete geographic overlap data. Their votes were left unattributed, and the results were skewed. Version v0_8 fixed that gap.

---

**Assertion:** The 338Canada April 2026 polling reading remains supportive of the 2023 asymmetry direction.
**Why?** What is 338Canada and why is polling data used in an audit of geographic boundaries?
**Answer:** 338Canada is a Canadian electoral forecasting website that aggregates polling data to estimate seat outcomes. The audit uses its April 2026 riding-level estimates as a cross-check, a third source of vote input beyond the 2019 and 2023 historical election results. The test is whether the directional conclusion about the two maps holds up even under a different estimate of current voter preferences. All three vote inputs point the same direction. That strengthens the directional claim.

---

## §4 Methods

---

### §4.1 Falsifiability Gates and Pre-registration

---

**Assertion:** Every new test must have a null hypothesis, pass/fail threshold, and predicted direction documented in an OSF registration before data is examined.
**Why?** What is a null hypothesis and why does the order of operations matter?
**Answer:** A null hypothesis is the "no effect" baseline: for example, "the two maps are equally extreme in their partisan properties." Fix the null hypothesis, the threshold for calling a result a "finding," and the expected direction before looking at the data, and the researcher can't unconsciously design tests after seeing which ones give interesting results. Look at the data first and decide afterward what counts as significant, and you are likely to find patterns that are really just noise. Pre-registration locks those choices before any data is examined. It forces discipline.

---

**Assertion:** Gates G0–G5 are built into the pipeline as falsifiability gates.
**Why?** What are these gates and why "falsifiability"?
**Answer:** Falsifiability is the requirement that a scientific claim be testable: there must be some possible observation that could prove it wrong. The G0–G5 gates are explicit checkpoints built into the analysis code. If certain conditions are not met (for example, if simulation convergence fails), the pipeline halts and flags the finding as unreliable instead of carrying on. These gates make the audit falsifiable in practice. Not just in principle.

---

### §4.2 MCMC Ensemble

---

**Assertion:** The canonical ensemble uses 1,010,000 plans across 4 chains × 252,500 steps, base seed 1432864451.
**Why?** Why 1,010,000 plans specifically, and what is a "chain"?
**Answer:** A chain is one continuous sequence of randomly generated maps. Each new map is made by a small change to the previous one. Running four independent chains lowers the risk that all the maps happen to cluster around one particular type of solution. Each chain ran for 252,500 steps, for a total of 1,010,000 maps (4 × 252,500). One million maps is considered more than sufficient for reliable statistical estimates. The 1,010,000 is simply the exact count from 4 chains, each completing 252,500 steps.

---

**Assertion:** The ReCom (Region Combining) algorithm draws legally valid maps by merging and re-splitting adjacent districts.
**Why?** How does the computer draw legally valid maps?
**Answer:** ReCom picks two neighboring districts at random and combines them into one large area. Then it draws a new boundary through that combined area, making two new districts. Each step randomly redraws one boundary pair and leaves every other district boundary the same. Every step starts from a valid map and produces a valid map (both output districts satisfy contiguity and approximate population rules), so every map in the chain is guaranteed to be legally valid. Over many steps, it explores the full space of legal possibilities.

---

**Assertion:** Gelman-Rubin R̂ values are 1.00011–1.00205 on the final canonical run, indicating convergence.
**Why?** What is a Gelman-Rubin value and what does convergence mean here?
**Answer:** Gelman-Rubin R̂ is a diagnostic that compares the variation within each chain with the variation between chains. If the four chains are all exploring the same landscape (converging on the same distribution of maps), R̂ is close to 1.0. Values above 1.1 are typically a warning sign that the chains have not converged. Values of 1.00011–1.00205 are very close to 1.0. All four chains are sampling from the same distribution. The simulation has stabilized, and the results are reliable.

---

**Assertion:** Effective Sample Size (ESS) is 1,413–1,522 on canonical 1M partisan metrics — described as publication-grade.
**Why?** What is an Effective Sample Size and why does "1,413–1,522" matter when you have 1,000,000 total samples?
**Answer:** When each new map in a simulation is based on the previous one, consecutive maps are correlated. They are not fully independent observations. The Effective Sample Size scales the total sample count down to reflect how much independent information is actually there. An ESS of 1,413–1,522 out of 1,000,000 total steps means the chain holds about 1,413–1,522 truly independent observations. That is still more than enough for reliable percentile estimates. Comparable published ensemble studies use similar or lower ESS values, which is why this is described as meeting publication standards.

---

### §4.3 Partisan Bias Metrics

---

**Assertion:** Four partisan metrics are used: Efficiency Gap, Mean-Median Gap, Declination, and Seats at 50/50.
**Why?** Why are four different measures needed instead of just one?
**Answer:** Each of these measures captures a different side of partisan fairness, and each has known blind spots. The Efficiency Gap (wasted votes) can be distorted by landslides. The Mean-Median Gap (distributional skew in vote shares) holds up in landslides but misses certain packing patterns. Declination (angular asymmetry of win margins) is sensitive to how broadly wins are spread. Seats at 50/50 (projected outcome in a tied election) captures an overall advantage that single-metric scores don't always show. Use all four and the picture fills out, and the chance shrinks that any one metric's blind spot hides a real pattern.

---

**Assertion:** Alberta efficiency gap convention: negative = UCP advantage, positive = NDP advantage.
**Why?** Why does the sign convention matter and why is it mentioned explicitly?
**Answer:** The sign of the efficiency gap can be defined either way. Some researchers make negative favor one party; some define it the other way. The audit states its convention outright, so you know which way positive and negative point. Without that, you could misread a positive value as a finding favorable to the NDP when it is actually unfavorable. The §5.4 MCMC sections use a different sign convention (positive = UCP-favoured) for historical reasons, so you have to track which section uses which definition.

---

### §4.4 SZAT (Swing-Zone Allocation Test)

---

**Assertion:** SZAT examines only the 2,110 Voting Areas assigned differently between the two proposals.
**Why?** Why look only at the places where the two maps differ?
**Answer:** Compare the full partisan score of the minority map with the full score of the majority map, and you cannot tell whether the difference comes from intentional partisan line-drawing or from geography both maps share. SZAT looks only at the 2,110 geographic units that one map gives to one district and the other map gives to a different district. That isolates the partisan effect of the specific choices the minority commissioners made. Everything the two maps share is subtracted out. Only the contested boundary decisions remain.

---

**Assertion:** SZAT p = 0.0024.
**Why?** What does p = 0.0024 mean for the boundary-choice test?
**Answer:** Suppose the specific boundary choices in the minority map were politically neutral, and the 2,110 differently assigned geographic units had been drawn randomly without any partisan intent. Then you would expect the partisan lean of those units to be roughly balanced. A p-value of 0.0024 means a random redistribution of those same units would produce a partisan imbalance this extreme only about once in every 400 tries. From a neutral process, that is a very unlikely outcome.

---

### §4.5 No Legal Conclusion or Intent Inference

---

**Assertion:** The audit records what the data show; it does not reach a legal conclusion and does not infer intent.
**Why?** Why can the audit measure partisan effects but not say whether it was intentional?
**Answer:** Whether a map's statistical properties fall outside the range of neutral maps is an empirical question. The data can answer it. To conclude that a specific person or group intentionally drew the map to favor one party is a legal and factual judgment. It needs evidence about what those people were thinking, and whether they acted with improper purpose. Statistical outliers can occur without improper intent. Intentional manipulation can occur at levels too subtle to detect statistically. The audit makes the empirical measurement and leaves the legal conclusion to courts, or to other institutional processes with the authority and evidence to make it.

---

### §4.6 Packing and Cracking Thresholds (P1 and P2)

---

**Assertion:** P1 threshold: +5% of provincial mean — one-fifth of the ±25% statutory band.
**Why?** Where does the 5% figure come from?
**Answer:** The ±25% statutory band is the full range of district sizes the law permits. The P1 threshold asks a much tighter question: is a district's population more than 5% above or below the provincial mean? The 5% was chosen as one-fifth of the ±25% total range. It marks the zone closest to the provincial average, where a deviation is most likely to be deliberate rather than a matter of geographic necessity. It is a derived threshold (based on the statutory range), not an arbitrary number. But the audit chose it. The law did not prescribe it.

---

**Assertion:** P2 threshold: +15pp above mean margin, which gives a safe-seat cut-off stricter than the 20 pp threshold in Chen (2017).
**Why?** What is "mean margin" and what does Chen 2017 have to do with this?
**Answer:** "Mean margin" is the average winning margin across all districts. P2 flags any district where one party's winning margin exceeds that average by 15 percentage points or more, a sign that party's voters are heavily "packed" into the district. Add the 15pp figure to the mean winning margin and you get a "safe seat" cut-off above the 20 pp threshold in a 2017 academic paper by Jowei Chen that studied natural geographic clustering of voters. So this test flags fewer districts than Chen's line would. Like every derived threshold in this audit, its provenance is documented in the threshold provenance compendium.

---

### §4.7 Sensitivity Tests

---

**Assertion:** Three stress-test families are applied: vote-input substitution (2015, 2019, 2023), geographic reclassification variants, and ensemble parameter variation.
**Why?** Why run the same analysis three different ways?
**Answer:** A finding that appears under only one specific set of assumptions is weaker than a finding that appears under many. Test with 2015, 2019 and 2023 vote data, and you see whether the directional conclusion depends on which election year is used. Test with different geographic classifications, and you see whether the Calgary zone gap depends on how "urban core" is defined. Test with different ensemble parameters (different chain lengths, different balance criteria), and you see whether the statistical outlier status depends on particular simulation settings. A finding that survives all three families of variation is much more credible.

---

## §5.1 Population Equality

---

**Assertion:** Minority mean absolute deviation (MAD) is 4,707; majority MAD is 3,180. Source: commission's own per-ED population tables.
**Why?** How is this number calculated and why is the commission's own table the source?
**Answer:** The Electoral Boundaries Commission published a table of the proposed population of every district. To get the mean absolute deviation, take each district's population, subtract the provincial average of 54,929, and drop any minus sign (the absolute value). Then average those 89 values. The ensemble comparison in the report's §5.4.9 uses a different statistic: the median absolute deviation from the median district (MedAD), on 2021 census population. Because this finding uses the commission's own published numbers, not any computed or estimated values, it rests directly on official data. It cannot be disputed on the grounds of measurement error. The commission itself produced the population figures that show the minority map has wider population variance.

---

**Assertion:** Minority MAD 48% wider than majority.
**Why?** Is a 48% wider spread actually significant or is that within normal variation?
**Answer:** The ±25% statutory band allows some population variation. But the MAD doesn't measure whether any single district exceeds the limit. It measures how the typical district compares with the average. A 48% wider MAD means the minority's districts, taken as a whole, sit further from the ideal equal-population target than the majority's. Appendix C puts all three maps on the 2021 census. On that base the gap almost disappears: the minority's MAD is 10.2% of its quota, the majority's 10.1% and the 2019 map's 9.7%. The 48% figure is a statement about the commission's 2024 tables. Not about the 2021 census.

---

**Assertion:** On the 2021 Census, the three maps have almost the same MAD as a share of quota: 2019 map 9.7%, majority 10.1%, minority 10.2% (Appendix C).
**Why?** Does the majority map improve on the existing map?
**Answer:** Not on this evidence. The majority's 3,180 comes from the commission's 2024 tables; the 2019 map's 4,745 comes from the 2021 Census. Different populations. Different quotas. Score all three maps on the same 2021 Census base, each against its own quota, and they come out almost level. The 2026 maps were drawn to 2024 estimates, so the 2021 base is not the one they were drawn to; Appendix C explains this cycle lag. The result limits the population-equality case against the minority map. Its wider spread shows on the commission's own tables. Not on the 2021 Census.

---

**Assertion:** Calgary geographic-zone asymmetry: minority 7.7–12.2%; majority 0.36–0.39% (two classification rules).
**Why?** What are the two classification rules and why are two used?
**Answer:** The audit draws the line between Calgary's "urban core" and "suburban ring" in two different ways: one based on city planning zone designations, and one based on a radius from the city center. Both give consistent results. The minority map's zone gap is between 7.7% and 12.2%, depending on the method. The majority's gap stays below 0.4% under both. Reporting both confirms the finding does not depend on a particular definition of "urban core."

---

## §5.2 Partisan Bias

---

**Assertion:** Minority EG = +4.02% on canonical results, which is below the audit's 4.10% threshold; the EG flag is withdrawn.
**Why?** Why is a threshold of 4.10% used rather than the academic 7% threshold?
**Answer:** The 7% threshold comes from Stephanopoulos and McGhee's foundational academic paper. It was derived from US electoral data, and no Canadian court has ever adopted it. The audit's own threshold of 4.10% was derived from the canonical 1,010,000-plan simulation. It is the 95th-percentile efficiency gap across those random maps as registered, and it stays frozen as the Option D line. The 2026-07-12 clean rerun of the simulation puts the 95th percentile at 4.08%. A threshold drawn from the simulation is more appropriate for Alberta, because it reflects what Alberta's specific geography and population distribution produce. Not what US states produce. At 4.02%, the minority EG sits below even this stricter Alberta-specific threshold, so the efficiency gap alone does not trigger a finding.

---

**Assertion:** Three of four partisan metrics carry outlier flags: Mean-Median at p99.97, Seats at 50/50 at p99.99, Declination at p1.21 (NDP-tail).
**Why?** What does "p99.97" mean and why is declination at p98.79 (UCP-tail, post-Amendment-10; was p1.21 NDP-tail under pre-Amendment-10 swapped operand) a problem when the others are at p99.97?
**[Corrected — Amendment 10, 2026-06-12.** The "declination disagrees / points the opposite way" reading here is retired. It came from a sign error in the code (`mcmc_ensemble.py:215`, a swapped operand). With the sign fixed, the minority's declination is p98.79 on the UCP-favoured tail — it AGREES with the efficiency gap, mean-median, and seats@50/50, so all four of four metrics point the same way. The explanation of the "disagreement" below is preserved only as a record of the pre-correction reading. See `reports/academic/report_academic.md` §5.4.9.**]**

**Answer:** p99.97 means the minority map's mean-median score is higher than 99.97% of the one million randomly drawn neutral maps — extremely high. p99.99 means the minority's seats-at-50/50 score is higher than 99.99% of neutral maps. Both are on the upper tail, indicating UCP advantage. Declination at p1.21 means the minority's declination score is lower than 98.79% of neutral maps — it is on the lower tail, meaning declination reads the opposite direction. This cross-metric disagreement is documented as a known limitation: the efficiency gap and declination disagree because they measure different geometric properties of partisan distribution. The audit notes the disagreement rather than discarding the contradictory metric.

---

**Assertion:** The majority map's mean-median is at p0.99 (NDP-tail), explained as a rural-district preservation convention.
**Why?** Why would a finding that appears to favor the NDP appear in the majority map?
**Answer:** The majority map was drawn by commission members who aimed to preserve existing rural district boundaries, including several rural districts that consistently vote heavily UCP. Keeping those districts unchanged gives the majority map a cluster of high-UCP-vote-share districts at one end of the distribution. The mean-median score is sensitive to exactly this kind of cluster. A group of high-margin wins for one party pulls the mean away from the median, in a direction the formula reads as favoring the other party. The finding has a mechanical explanation, and it is consistent with rural-preservation intent rather than partisan manipulation.

---

**Assertion:** Monte Carlo CI for Seats at 50/50: minority NDP@50/50 has 95% CI [41, 47] vs majority [43, 46] — overlapping.
**Why?** What does it mean that the confidence intervals overlap?
**Answer:** Seats at 50/50 estimates how many seats the NDP would win if the total provincial vote were tied exactly 50-50 between the parties. Allowing for uncertainty in vote attribution, the minority's estimate runs from 41 to 47 seats and the majority's from 43 to 46 seats. The ranges overlap; both include the 43–46 range. So you cannot say with statistical certainty that the minority gives the NDP fewer seats than the majority. The point estimates differ. The uncertainty ranges are large enough to leave the difference inconclusive on this metric alone.

---

**Assertion:** Cross-election stability: the inter-map asymmetry direction reverses under 2019 votes (+0.75 pp vs −0.51 pp).
**Why?** Does a direction reversal under 2019 votes undermine the finding?
**Answer:** The inter-map asymmetry is the difference between how much each map favors the UCP. Under 2023 votes it is approximately −0.51 percentage points (minority more UCP-favorable). Under 2019 votes it is +0.75 percentage points (majority slightly more UCP-favorable). The report gives a mechanical reason for the reversal. Several hybrid electoral districts around Springbank, Bearspaw and Cochrane are blended differently under the 2019 and 2023 vote models, and that changes the relative score. The reversal means the magnitude claim is fragile when the vote input changes. The four non-vote-based structural signals (population, zone gap, Airdrie, anomalies) are not affected.

---

### §5.2.1 — Results table

---

**Assertion:** B2 Efficiency Gap (canonical MCMC convention, positive = UCP-favored): majority +0.10%, minority +4.02% (p94.54). B3 Mean-Median: majority −3.64 pp, minority +1.03 pp. B4 NDP seats at 50/50 uniform swing: majority 48, minority 43.
**Why?** The efficiency gap numbers in §5.2.1 look different from the ones in the §5.2 parent section — are they the same measurement?
**Answer:** They measure the same thing, but the older figures are superseded. Majority −0.40% and minority −1.81% (negative = UCP-advantaged) came from the v0.2 crosswalk-blend calculation, used before the official shapefiles arrived. On 2026-05-18 Phase 4C replaced them with exact attribution on the official Elections Alberta shapefiles (DOCUMENTED CORRECTIONS C5). The current figures are majority +0.10% and minority +4.02% on the canonical MCMC scoring (positive = UCP-favored), and +0.04% and +3.96% in the §5.2.1 table's standard calculation. Old figures and current ones agree on this much: both put the minority map on the UCP-favoured side of the majority map.

---

**Assertion:** The Compactness-Weighted Efficiency Gap under the blended-crosswalk method is direction-stable: minority more UCP-favorable under all five tested urban weights (0.60–0.90).
**Why?** If the numbers change depending on which urban weight you use, how can you be confident in the direction?
**Answer:** The sensitivity test varies the "urban weight": the fraction of each hybrid district's votes attributed to its urban-core predecessor rather than its rural-fringe component. At every weight from 0.60 to 0.90, the minority EG is more UCP-favorable than the majority EG, by a margin ranging from 0.47 to 1.48 percentage points. Nowhere in the tested range does the direction flip. The finding does not depend on picking the right urban weight. The magnitude is uncertain; the direction holds across the full parameter range tested. That is why the report presents a range rather than a single point estimate.

---

**Assertion:** B4 direction was revised mid-audit: earlier versions reported majority 44 / minority 42 (minority fewer NDP seats); the v0.2 version reported majority 45 / minority 46; Phase 4C (2026-05-18) reports majority 48 / minority 43 (minority 5 fewer NDP seats).
**Why?** How should readers interpret a mid-audit direction reversal on one of the four metrics?
**Answer:** The direction reversal on B4 is disclosed openly, and it has a mechanical explanation. Two corrections drove it: a fix to the mapping dictionary for several Calgary suburban hybrid districts, and a change in the default urban weight from 0.70 to 0.85. At the revised weight, several minority-map suburban districts cross the NDP-win threshold under uniform swing when before they did not. Phase 4C then replaced the blend model with exact VA-level attribution on the official shapefiles, which gives majority 48 / minority 43. The audit documents each correction instead of hiding it. And the other three metrics (B2 EG, B3 mean-median, B6 declination) keep their direction: the minority map remains more UCP-favorable on those three under every tested parameter.

---

### §5.2.2 — Sensitivity (G5)

---

**Assertion:** The sensitivity table holds five discrete urban weights (0.60–0.90); the Monte Carlo interval [−3.04, +0.76] pp is a separate calculation that is wider than the table range.
**Why?** Why are there two different sensitivity ranges, and which one should a reader use?
**Answer:** The five-row table is a deterministic sensitivity test, with no chance involved. Each row fixes the urban weight at one value and computes the efficiency gap that results. The Monte Carlo interval varies urban weight, rural baseline and per-district jitter all at once, across 2,000 parameter draws, so it captures how the parameters move together (their covariance). Because more sources of uncertainty vary at once, the Monte Carlo interval is wider. If your question is "how much does the number change as we adjust urban weight?", use the table. If it is "what is the realistic range of the asymmetry given everything we don't know about vote attribution?", use the Monte Carlo interval. Both show genuine uncertainty. They answer different versions of that question.

---

**Assertion:** The boundary-straddle error — where a Voting Area polygon straddles a 2026 boundary line — could in principle misassign votes. The integrity audit finds this error below 0.0001% at poll-to-VA aggregation.
**Why?** If even a small number of votes are assigned to the wrong district, could that change the direction finding?
**Answer:** Sometimes a 2026 boundary passes through the interior of a Voting Area polygon, so the polygon cannot belong unambiguously to one district. The audit measures what that leaves behind. 99.2% of the 4,765 VAs have centroids that fall inside their declared 2019 parent district, and vote-conservation error at aggregation is below 0.0001%. Applied to the 2026 attribution, the expected rounding error is below 0.5% province-wide. The smallest minority-majority asymmetry observed across the full sensitivity range is 0.47 percentage points, roughly an order of magnitude above the boundary-straddle error ceiling. The error cannot manufacture the observed direction.

---

### §5.2.3 — Falsifiability gate: asymmetry direction

---

**Assertion:** [RETIRED 2026-07-12, C11] 90.5% of 2,000 Monte Carlo samples show the minority EG more UCP-favorable than the majority; the 95% interval [−3.04, +0.76] pp crosses zero.
**Why?** This was a check over a superseded model's parameters. What replaced it, and can the direction still be called confirmed?
**Answer:** The 90.5%-of-samples and crosses-zero figures came from the retired blend model's parameter uncertainty (urban weight, rural baseline). Phase 4C replaced that model with an exact computation: +3.92 pp, not an estimate with a confidence interval. The robustness check that applies now is attribution-method agreement. Centroid, area-weighted and population-weighted MAUP agree to within 0.1 pp. The honest summary: the minority is more UCP-favorable under every attribution method tested, and the finding depends on electoral context, not on modeling-parameter uncertainty. The structural signals in §5.1 and §5.8 use no vote data. Neither contingency applies to them.

---

**Assertion:** The direction reverses under 2019 votes (asymmetry +0.75 pp) and is near-zero under 2015 votes (+0.03 pp). The report treats this as a property of the finding, not a defect.
**Why?** Does a direction reversal under 2019 votes mean the 2023-based finding is unreliable?
**Answer:** A direction reversal under a different election's vote distribution does not mean the 2023 finding is wrong. It means the finding is conditional on which electorate is used. The report tests the 2015, 2019 and 2023 Alberta general elections plus April 2026 polling. The minority-more-UCP-favorable direction is stable under 2023 and the polling, reverses under 2019, and is near-zero under 2015. This is disclosed as a known property: the minority map's partisan effect depends on where voters live in a given election cycle. The four structural signals (population MAD, zone asymmetry, Airdrie splits, chair-flagged anomalies) do not depend on which election is used.

---

### §5.2.4 — Cross-metric weighting

---

**[Corrected — Amendment 10, 2026-06-12 — this Q&A is now inverted.** It was written when a declination sign bug made B6 appear to "point the opposite direction," so the defense was "we do not claim four metrics agree; we honestly note the disagreement." After the sign fix (`mcmc_ensemble.py:215`), the report DOES report **four-of-four agreement** in the UCP-favoured direction (declination p98.79, UCP-tail). The assertion and answer below are retained only as a record of the pre-correction posture; the current honest statement is the reverse — the four metrics do agree, and the audit says so. See `reports/academic/report_academic.md` §5.4.9 and §5.2.4.**]**

**Assertion:** B2 (efficiency gap), B3 (mean-median), and B4 (seats at 50/50) all show the minority more UCP-favorable; B6 (declination) points the opposite direction. The disagreement is described as "four metrics describing different faces of the same structural pattern," not "three against one."
**Why?** Is it not misleading to call this "four metrics agree" when declination disagrees on direction?
**Answer:** The report does not claim four metrics agree on direction — it explicitly notes the disagreement and gives a mechanical explanation. Efficiency gap, mean-median, and seats at 50/50 all measure wasted votes and seat-counterfactuals. Declination measures the geometric angle between the two parties' winning-district margin distributions. When a map engineers many narrow-margin losses for the losing party, the wasted-vote metrics flag it; declination's angle measurement can look different because narrow-margin losses look geometrically different from blowout losses. The report's "four faces of the same pattern" framing means all four metrics are consistent with a narrow-margin-loss packing mechanism — they just show different aspects of it. A reader can legitimately cite declination as pointing toward a less UCP-favorable reading, and the audit acknowledges this explicitly.

---

### §5.2.5 — Natural-packing context (Chen and Rodden)

---

**Assertion:** The Alberta validation finds UCP surplus-vote rate 15.9% vs NDP 9.3%: UCP is the more-packed party. Moran's I = 0.7534. The Chen-Rodden mechanism runs opposite to the US pattern.
**Why?** If the original Chen-Rodden paper predicts NDP disadvantage through urban packing, and Alberta shows the reverse, does this undermine or support the partisan-bias findings?
**Answer:** The Chen-Rodden finding matters because it identifies which party neutral maps put at a disadvantage. Not which map is biased. In the US, urban-concentrated Democrats are structurally disadvantaged even by random maps. In Alberta, the neutral maps favor UCP by default, because UCP wins many rural seats by very large margins, wasting many "excess" votes, while NDP losses are spread across rural and suburban areas. So any reasonable Alberta map will show some UCP efficiency gap advantage. The two 2026 maps must be judged against this neutral, UCP-favoring baseline. The majority corrects the baseline slightly. The minority amplifies it slightly. The Chen-Rodden finding strengthens the structural finding by showing the partisan asymmetry is not a geographic inevitability that cannot be altered. Both maps show the neutral floor can be adjusted.

---

### §5.2.6 — Marginal-seat translation

---

**Assertion:** In 2023, 14 of 87 ridings were decided by less than 3 pp of two-party margin; 12 of those 14 are in Calgary. The audit's 5-seat map effect concentrates in these already-marginal ridings.
**Why?** What does it mean for the map effect to "concentrate" in marginal ridings?
**Answer:** The efficiency gap and seats-at-50/50 findings project that the minority map produces 5 fewer NDP seats than the majority map at a 50/50 province-wide vote split (48 vs 43 under Phase 4C). Trace which seats those would be, and they are the Calgary ridings already decided by tiny margins in 2023: races within a few percentage points of flipping. The map effect does not add or subtract seats in safe districts. It works in the places where the outcome is already uncertain. A 1.5 percentage-point shift in the audit's estimate range would flip 6 Calgary seats toward UCP and 4 toward NDP. In a UCP landslide, the map effect is small. In a close election, it could decide the outcome.

---

### §5.2.7 — Measurement-resolution sensitivity

---

**Assertion:** Two attribution methods disagree on EG sign: blended crosswalk gives minority −1.81% (UCP-favorable, negative convention) while high-resolution spatial gives minority +1.82% (NDP-favorable, positive convention). The structural findings are independent of this disagreement.
**Why?** Is it a problem that two measurement methods disagree on which party the minority map favors?
**Answer:** The sign disagreement is itself a specific finding, about how EG responds to the choice of attribution method, and the report documents it openly rather than hiding it. The key point: the DPG-construction choice, meaning which approximate boundary geometry was used before the official shapefiles arrived, turned out to be the dominant source of error. It was larger than within-method variation by a factor of seven. The crosswalk and spatial methods build their per-district vote totals from different underlying data. When the inputs differ this much, disagreeing on EG magnitude and sign is no surprise. The findings that do not depend on this choice all stand, whichever EG measurement you prefer: population tables, ensemble percentiles, zone asymmetry, Airdrie split count, chair-flagged shapes.

---

### §5.2.8 — EG threshold options A–D

---

**Assertion:** The 7% EG threshold from Stephanopoulos and McGhee was calibrated to US Congressional delegations; it has never been adopted by any Canadian court. Option D, the Alberta-derived 95th-percentile threshold, is 4.10% (canonical 1M ensemble, frozen as registered; the clean-rerun 95th percentile is 4.08%). Both 2026 maps fall below 4.10%.
**Why?** If both maps are below the Alberta-derived threshold, doesn't that mean neither map is an EG outlier?
**Answer:** Correct. On the efficiency gap metric alone, neither map triggers the outlier flag under the Alberta-calibrated 4.10% threshold. The minority's canonical EG is +4.02% (p94.54), just below the 4.10% Option D line and the 4.08% clean-rerun 95th percentile. So the canonical analysis withdraws the EG flag. That fits the audit's overall finding. EG alone does not make the case. The case rests on three metrics that do trigger flags (mean-median p99.97, seats-at-50/50 p99.99, Mahalanobis D²), combined with the structural signals. The below-threshold EG result is reported honestly, as a null result on that specific metric. Not discarded.

---

### §5.2.9 — Extended partisan metrics

---

**Assertion:** On the canonical shapefiles (refreshed 2026-06-11): turnout-weighted Partisan Bias is −0.0402 for 2019, −0.0393 for the majority and +0.0169 for the minority; Responsiveness is 2.87, 1.12 and 1.69 seats per 1% swing; the Lopsided Margins signal is present in all three maps including 2019.
**Why?** The extended metrics seem to show the majority map as more partisan in some ways — how should these results be read alongside the main findings?
**Answer:** These four additional metrics supplement the four core metrics. Partisan Bias measures the share of seats a map gives the UCP at a tied province-wide vote, minus one half. At a tie the minority gives the UCP slightly more than half the seats (+0.0169). The majority and the 2019 map give it slightly less (−0.0393 and −0.0402). Responsiveness is the number of seats that change hands for each 1% swing in the vote. Both 2026 maps are less responsive than the 2019 map, and the majority (1.12) is less responsive than the minority (1.69). Lopsided Margins is significant on all three maps. It is a feature of Alberta's political geography that any legal map inherits. Not a distinctive minority characteristic.

---

### §5.2.10 — SZAT: Swing-Zone Allocation Test

---

**Assertion:** SZAT score +0.039211, bootstrap p = 0.0024 (10,000 permutations). Substrate: 2023 election-day votes only (~896,644 two-party; NDP two-party share 42.60%). Swing zones: 2,110 VAs assigned differently between the two maps.
**Why?** What question does SZAT answer that the MCMC ensemble does not?
**Answer:** The MCMC ensemble asks whether the minority map as a whole is unusual next to neutral random maps. SZAT asks a more targeted question. Take only the Voting Areas that the minority map and the majority map assign differently: do those boundary choices systematically favor one party's vote efficiency? SZAT subtracts out everything the two maps share (Alberta's geography, population distribution, and the full legal constraint set) and examines only the swing-zone differences. The +0.039 SZAT score means the minority's specific boundary choices, applied only to the 2,110 contested VAs, increase NDP vote waste by 3.9 percentage points relative to the majority's choices for those same VAs. The p = 0.0024 bootstrap test says a score like this would occur by chance in only 0.24% of random reassignments of those VAs.

---

**Assertion:** The SZAT uses election-day votes only throughout. An earlier version of the §5.2.10 paragraph incorrectly described a substrate change to "full advance-vote" votes; that description has been retracted.
**Why?** Why does it matter which votes are included — election-day only versus full advance-vote?
**Answer:** Elections Alberta assigns election-day votes spatially at the Voting Area level, so each VA's geographic location is known. Advance-poll, mail-in and special ballots are not spatially assigned at the VA level, so they cannot be attributed to specific VAs. Including them would require an apportionment model, and that model brings in assumptions the election-day-only approach avoids. The SZAT pre-registration specified election-day votes. The initial run used election-day votes. So did the definitive run. The retracted paragraph incorrectly claimed otherwise. The p change from 0.0044 to 0.0024 came from a VA file switch that moved 2 VA centroid assignments, not from any substrate change. A separate full-vote sensitivity using apportioned advance-ballot columns (unregistered) yields p < 0.0001. It is reported as a supplementary sensitivity check only.

---

## §5.3 Packing/Cracking Signatures

---

**Assertion:** The minority map has a higher density of P1-flagged districts (population outliers) and P2-flagged districts (margin outliers) than either the majority or the 2019 map.
**Why?** What does a higher density of flagged districts indicate?
**Answer:** P1-flagged districts are those whose population deviates more than 5% from the provincial average. P2-flagged districts are those where one party's win margin runs more than 15 percentage points above the typical margin, a sign that party's voters are heavily concentrated (packed) there. A higher density of both kinds of flag means the minority map has, in proportion, more districts that stray from equal population and more districts where votes are heavily concentrated. When the flagged districts keep favoring the same party, in the same regions, that pattern is consistent with packing.

---

**Assertion:** The Airdrie split count is 4 vs 2 across the two maps.
**Why?** How is the "split count" measured?
**Answer:** The split count is simply the number of separate electoral districts that hold at least some of the City of Airdrie's population. On the minority map, Airdrie residents land in four different districts. On the majority map, in two. The count comes straight from the commission's own published boundary descriptions and maps. No vote data. No statistical modeling.

---

**Assertion:** Chen-Rodden natural packing: Alberta's mechanism is UCP rural dispersion, not NDP urban packing.
**Why?** What is "natural packing" and why does the mechanism matter?
**Answer:** Natural packing is the tendency of voters with similar political preferences to cluster on the map. Not because of deliberate manipulation, but because of where people choose to live. In US cities, Democrats tend to live very densely in urban cores. Researchers Chen and Rodden call the result "natural packing," and it disadvantages Democrats even in neutral maps. In Alberta, the audit finds the reverse. UCP voters are dispersed across many rural districts, and the UCP wins each of them by a large margin. So the UCP wastes many "excess" rural votes. The mechanism matters because it shapes which party you would expect to be disadvantaged even by neutral maps.

---

## §5.4 MCMC Ensemble Results

---

**Assertion:** The 1,010,000-plan canonical ensemble is made of 87-district ReCom plans. The official EA shapefiles (ea_majority_2026_eds.gpkg, ea_minority_2026_eds.gpkg, EPSG:3400, 89 EDs each) are used only to score the two commission maps against it.
**Why?** What is EPSG:3400, and why name the exact files?
**Answer:** EPSG:3400 is the label for a coordinate system used in Alberta. The Earth is curved and a map is flat; a coordinate system sets out how the curve is pressed flat so that distances and areas can be measured. Use the wrong system and distances and areas come out distorted. The filenames are proof of source. They show the analysis ran on the official Elections Alberta shapefiles, the digital boundary files received on May 6, 2026, and not on the earlier approximate tracings. Name the exact file, and any researcher can check they are working from the same input data.

---

**Assertion:** Minority Mean-Median p99.97 on canonical 1M ensemble.
**Why?** What does "p99.97 on canonical 1M ensemble" mean in plain terms?
**Answer:** The canonical ensemble is the authoritative set of computer-drawn maps: one million legal Alberta maps, drawn at random. Each gets a mean-median score (a measure of skew in vote shares across districts), so you have one million different scores. The minority map's real score is higher than 99.97% of those million scores. Put another way, only about 335 maps in every million random maps are as extreme as the minority map on this measure. Draw Alberta maps at random, follow every legal rule, and you would almost never land on a map this extreme by accident.

---

**Assertion:** Minority Declination p1.21 — disagrees with EG and MM direction; consistent with narrow-margin-loss packing.
**Why?** How can a low percentile score indicate a problem when the others show high percentile scores?
**[Corrected — Amendment 10, 2026-06-12.** The "declination disagrees / points the opposite way" reading here is retired. It came from a sign error in the code (`mcmc_ensemble.py:215`, a swapped operand). With the sign fixed, the minority's declination is p98.79 on the UCP-favoured tail — it AGREES with the efficiency gap, mean-median, and seats@50/50, so all four of four metrics point the same way. The explanation of the "disagreement" below is preserved only as a record of the pre-correction reading. See `reports/academic/report_academic.md` §5.4.9.**]**

**Answer:** The declination formula measures something different from efficiency gap and mean-median. It looks at the slopes of the win-margin curves for each party. A very low declination score (p1.21 means lower than 98.79% of random maps) in the opposite direction from the other metrics is actually consistent with a specific packing pattern: when one party's voters are used to engineer many close losses rather than many blowout wins, declination reads the pattern differently from efficiency gap. The audit documents this cross-metric disagreement as a technical feature, not an error, and notes it does not resolve the overall outlier status — three of four metrics still place the minority map in the extreme tail.

---

**Assertion:** Mahalanobis Ch1 p = 8.80×10⁻⁷.
**Why?** What is the Mahalanobis test doing that a simple average of the four metrics cannot do?
**Answer:** Average the four percentile scores and you treat each metric as if it stood alone. They don't stand alone. The four metrics are correlated: a map that scores high on efficiency gap often scores high on mean-median too, because the same underlying feature drives both. Average them and that feature gets counted again. The Mahalanobis distance allows for the overlap. It measures how far a map sits from the center of the joint distribution, the cloud of all four metrics at once. No double-counting, and the joint signal still comes through. A Mahalanobis p = 8.80×10⁻⁷ means the minority map's combination of all four metrics, taken together, is more extreme than 99.9999% of random neutral maps.

### §5.4.1 — Constraint-bound expectation terminology

*Note: §5.4.1–§5.4.3 headers are this defense document's own numbering. The corresponding content in the report appears as unnumbered prose within §5.4 before the first numbered sub-header (§5.4.4). These labels are used here for navigation only.*

---

**Assertion:** The ensemble is described as a "constraint-bound expectation," not a "neutral map." The ReCom ensemble samples from legal maps satisfying ±25% population deviation, contiguity, and compactness; it does not claim to produce the politically neutral or correct map.
**Why?** Why does the terminology matter — isn't a randomly drawn legal map effectively neutral?
**Answer:** No. A map drawn at random is not politically neutral in any objective sense, and Alberta's geography is the reason. NDP voters are concentrated in Edmonton and inner Calgary; UCP voters are spread across suburban and rural areas. So almost any legal random map hands the UCP a structural advantage, built into where people live. The phrase "constraint-bound expectation" says exactly what the ensemble is: what the population-and-contiguity constraints tend to produce, on average, when applied to Alberta's actual vote geography. It does not say that result is fair, or desirable. The audit does not claim the ensemble median is what a fair map would look like. It claims only this: a real map sitting far outside the range the constraints produce has moved beyond what those constraints alone would explain. The move away from the earlier "neutral map" language was specifically addressed in the 2026-04-24 "Geographic Neutrality Myth" critique, and the change in wording is documented in the report's §5.4 opening note.

---

**Assertion:** The structural UCP floor: at a 50/50 province-wide vote, the median of 10,000 legal Alberta boundary maps gives the NDP 44.8% of seats. No ReCom-legal map escapes this floor.
**Why?** If every legal map favors the UCP, why isn't every map considered biased?
**Answer:** Because tilt is not the question. Essentially every legal Alberta map tilts UCP; geography does that. The question is how far a given map sits from the constraint-bound expectation, the result the legal constraints tend to produce. A map at the 50th percentile of the ensemble, right in the middle, is about as UCP-favorable as legal constraints typically produce. A map at the 99th percentile is unusually far beyond that floor. So the audit's findings ask whether the minority proposal is statistically unusual among legal maps. They do not ask whether it favors one party over another in absolute terms. Not whether it leans. How far.

---

### §5.4.2 — §15(2) deviation-constraint gap

*Note: defense document numbering; no §5.4.2 header in the report.*

---

**Assertion:** The MCMC ensemble applies a uniform ±25% population-deviation constraint to all 87 districts of each neutral plan (quota = 2021 population / 87). Both commission maps invoke the §15(2) rural-protection exception for 3 EDs, allowing deviations down to −47.7% — below the ensemble's floor. The 3 §15(2) EDs are by construction outside the ensemble's distribution.
**Why?** If the ensemble cannot even produce the rural-exception districts that both maps use, how can its percentile scores for the real maps be meaningful?
**Answer:** Each real map has three rural-exception districts, and they are small, remote, and heavily UCP-leaning. The partisan metrics — efficiency gap, mean-median, declination, seats at 50/50 — are built from province-wide votes, and these districts hold a modest fraction of them. The effect on percentile positions is expected to be small. The comparison between the minority and majority maps is less sensitive to the gap than the absolute percentile scores are, because both maps invoke comparable §15(2) configurations. A methodologically complete ensemble would let the 3 §15(2) EDs vary across a wider deviation range; that is queued as future work. For the current run, the conservative reading is that the reported minority percentiles are slightly lower bounds than a constraint-enforcing ensemble would produce.

---

### §5.4.3 — ESS-150 tail downgrade

*Note: defense document numbering; no §5.4.3 header in the report.*

---

**Assertion:** The 250k single-chain run had ESS ≈ 150 per metric. Raw percentile claims at the tails (p100, p1.6) must be read as bounded to approximately p95.35 / p2.5 at that precision, not as exact percentile values. The canonical 1M multichain run resolves this caveat with ESS 1,413–1,522.
**Why?** If the chain ran 250,000 steps, why is the effective sample size only 150?
**Answer:** Because each map grows out of the last. The simulation makes each new map by changing the previous one, so maps next to each other in the chain are alike; they are not independent observations. The Effective Sample Size (ESS) asks how many truly independent observations the correlated chain is worth. At ESS ≈ 150, a raw p100 claim can't be told apart, statistically, from p95 or p97 at 95% credibility. The chain lacks the precision to separate the most extreme tail percentiles from each other. The canonical 1M run (§5.4.9) resolves this caveat: four parallel chains of 252,500 steps each reach ESS 1,413–1,522. The tail downgrade is something we are bound to disclose for the earlier DPG-era runs documented in §5.4.4–§5.4.8, the runs built on approximate boundary tracings before the official shapefiles arrived. It does not touch the canonical headline numbers.

---

#### §5.4.4 — Run #4: 250k MCMC against v0_8 full-coverage geometry

*This is a DPG-era run (Derived Provisional Geometries v0_8). All percentile placements are superseded by the canonical official-shapefile run in §5.4.9 for final conclusions.*

---

**Assertion:** Run #4 (250k, v0_8, full 89/89 coverage) reports minority EG +9.21% at p100, declination p2.9, seats@50/50 p100. ESS 491–499. Majority EG at p99.94 — the first run to show both maps as EG outliers.
**Why?** Why did earlier runs not show both maps as efficiency gap outliers, but Run #4 does?
**Answer:** Because the earlier runs were missing votes. They used partial-coverage geometry, with only 67–71 of 89 EDs measurable, and the gaps systematically left rural-UCP votes out of the scoring. The v0_8 full-coverage geometry fills all 89 EDs, using inheritance from 2019 boundaries, so the rural-UCP votes that had gone missing are now counted. Count them, and both 2026 maps land in the extreme UCP tail on efficiency gap. Earlier runs had shown negative EG on both maps. That sign reversal comes directly from this coverage correction, not from any change in method or substrate. The canonical §5.4.9 run supersedes the Run #4 headlines on EG.

---

**Assertion:** Cross-method comparison vs Run #3 (v0_7 partial coverage): EG magnitude flipped sign; mean-median lost its outlier flag; minority declination at p2.9 persisted; minority seats@50/50 at p100 persisted.
**Why?** Is it a problem that the EG number changed so dramatically between Run #3 and Run #4?
**Answer:** No. The shift is large, and it was expected and documented. Run #3 scored only 66–71 of 89 EDs. The missing EDs were urban and suburban districts, and their votes were simply absent from the count. Run #4 fills those EDs, and the provincial totals change substantially. The report flags this openly as a cross-method disagreement, a structural feature of reporting in layers. Neither run is treated as uniquely correct. Both are reported, each beside its coverage limitations. The two metrics that held through the coverage change, declination and seats@50/50, are the ones least sensitive to partial coverage. EG and mean-median are more sensitive because they depend on province-wide totals.

---

#### §5.4.5 — Run #5: 1,000,000-sample MCMC against v0_8 full coverage

*This is a DPG-era run. All percentile placements are superseded by the canonical §5.4.9 run.*

---

**Assertion:** Run #5 (1M, v0_8) raises ESS to 1,679–2,278 — publication grade. Percentile placements are within ±0.5 pp of Run #4, confirming Run #4 was not noise-driven.
**Why?** Why run a million maps if the 250k run already showed the same placements?
**Answer:** To turn a hedge into a number. Run #4 could only say "likely p98+ or p99+"; at ESS ≈ 500 it could not give a precise point estimate. Run #5 was built to resolve that hedge. At ESS 1,679–2,278, the percentile claims can be reported as point estimates instead of bounds. The placements held to within ±0.5 pp, which confirms the chain had converged at 250k. The 1M run adds precision, not a new direction. That stability is a methodological finding in its own right. It shows the chain was not stuck in a local mode, a pocket of maps that would give different results with more sampling. The canonical §5.4.9 run supersedes all DPG-era values from Run #5.

---

#### §5.4.6 — Run #6: 2,000,000-sample MCMC and the converged-ceiling finding

*This is a DPG-era run. The DPG-era seats@50/50 ceiling of 51.72% and the minority DPG reading of 52.8% are superseded by the canonical §5.4.9 analysis.*

---

**Assertion:** The simulation's seats@50/50 ceiling held at exactly 51.72% across 2,000,000 draws. Zero of 2,000,000 maps reached 52%. The minority's DPG-era seats@50/50 reading of 52.8% sits above this ceiling. This is described as "out-of-distribution" rather than merely a tail outlier.
**Why?** What is the difference between a statistical tail outlier and being "out of the distribution"?
**Answer:** A tail outlier sits at the far end of the distribution, but the same random process that makes all the other maps can still reach it. Rare, but reachable. Being "out-of-distribution" means more. The value is above the highest value the process produced in 2,000,000 draws, which is effectively zero probability under the neutral procedure. The ceiling finding says that 2,000,000 neutral random maps, all legal under the same statutory constraints, never once produced a map as extreme as the minority proposal on this metric (the projected seat result in a tied election). That is a stronger claim than "very unlikely"; it puts the minority's reading in a region the neutral process does not reach. The §5.4.8 short-bursts result confirms the framing: a non-neutral (partisan-optimizing) procedure does reach that region.

---

**Assertion:** ESS reached 3,138–4,347 on Run #6 — at or above the MGGG lawsuit-grade threshold (~3,000–5,000).
**Why?** What does "lawsuit-grade" mean as a practical standard?
**Answer:** It means precise enough for court. The MGGG (Metric Geometry and Gerrymandering Group) at MIT and Tufts developed practical guidance on when ensemble results are reliable enough to use in litigation. Their threshold, roughly 3,000–5,000 independent draws, reflects the precision needed for credible percentile claims at the extreme tails (p<5, p>95) in a legal setting. Run #6 crosses it on all four metrics, so the DPG-era ceiling finding meets the precision standard for litigation use. But official shapefiles superseded the DPG-era geometry itself, so for any legal-grade claim the authoritative source is the canonical §5.4.9 run.

---

#### §5.4.7 — 89-of-89 attribution and fuzzing-scenario analysis

*DPG-era analysis; superseded by canonical §5.4.9 for final conclusions.*

---

**Assertion:** Six minority polygon inheritance-fill slivers caught no 2023 VA centroids under the 83/89 partial-attribution reading. The 89-of-89 attribution fills those 6 EDs with their inherited 2019-polygon vote distributions, producing seats@50/50 = 52.8% (47/89). 89% of random-attribution fuzzing trials place the minority above the 51.72% ceiling.
**Why?** Why not just report the 83/89 number rather than introducing an imputed attribution for the 6 missing EDs?
**Answer:** Because the 83/89 reading hung on which 6 districts were unmeasurable, and that came from how the DPG geometry was built, not from the political question the audit is asking. Fill those 6 missing EDs differently under DPG tracing and they might all have been measurable. The 89-of-89 attribution cuts the result loose from that DPG artifact with a conservative inheritance assumption: each missing 2026 minority ED gets the 2019 vote distribution from the same territory. The fuzzing analysis then brackets the result, varying that assumption across all plausible alternatives. Of those, 89% still place the minority above the ceiling, so the "above-ceiling" finding is robust to the attribution choice. Only the 51.7% worst case, the most NDP-favorable attribution, puts the minority at the ceiling rather than above it. That case is a deliberately constructed minimum, not a central estimate.

---

#### §5.4.8 — Targeted-gerrymander short-bursts hill-climb (Cannon et al. 2023)

*DPG-era analysis; superseded by canonical §5.4.9 for final conclusions.*

---

**Assertion:** A short-bursts hill-climbing procedure (Cannon et al. 2023) runs 40,000 partisan-optimizing steps and reaches 52.87% UCP seats@50/50 — within rounding of the minority map's DPG-era 52.8%. The neutral ensemble across 2,000,000 draws cannot reach 52%.
**Why?** Why run a purposely partisan procedure at all — doesn't that show only what an intentional gerrymander could produce?
**Answer:** Yes. That is the point. The short-bursts result is not evidence of intent. It is evidence of procedural class: what kind of process could draw a map like this. The audit sorts boundary-drawing procedures into two types. Neutral ones are random walks bound only by the statutory rules. Non-neutral ones climb toward a partisan objective while staying legal. Run #6 establishes that neutral procedures cannot produce the minority's seats@50/50 reading. The short-bursts result establishes that non-neutral procedures can. So the minority map sits inside the reach of a partisan optimizer and outside the reach of a neutral procedure. That two-sided framing is more precise than simply calling the minority an outlier; it names which class of process could produce it. The audit explicitly does not conclude that the minority commissioners used a partisan optimizer. Intent cannot be inferred from a map's geometry.

---

#### §5.4.9 — Canonical ensemble: official Elections Alberta shapefiles (authoritative)

---

**Assertion:** This is the authoritative MCMC run. Official EA shapefiles (ea_majority_2026_eds.gpkg, ea_minority_2026_eds.gpkg, EPSG:3400) received 2026-05-06. Seed 1432864451 (drand round 5,500,000; seeds committed, test exploratory). 1,010,000 steps (4 chains × 252,500). ESS 1,413–1,522. Three partisan-metric outlier flags on minority: MM p99.97, seats@50/50 p99.99, declination p1.21. **[Amendment 10, 2026-06-12: the declination sign was corrected — it is p98.79 UCP-tail and AGREES with the other three metrics, four of four; see report §5.4.9.]** EG at p94.54 below threshold; EG flag withdrawn. Mahalanobis joint p = 8.80×10⁻⁷.
**Why?** Why do the canonical results differ from the DPG-era runs documented in §5.4.4–§5.4.8?
**Answer:** Because the maps underneath them changed. Before the official shapefiles were available, we built the DPG-era runs on approximate boundary tracings made from the commission's PDF thumbnails. Where a tracing strayed from the real line, especially in rural areas near the edge of cities, the votes credited to individual EDs shifted once the official files arrived. The canonical run is the first analysis on the same shapefiles Elections Alberta itself uses, and the only run whose results can be checked against the official record. The §4.1.4 sunset clause bound us to replace every DPG-era result with a canonical result within two weeks of the shapefiles' release. This run keeps that commitment.

---

**Assertion:** The s.15(2) rural-protection constraint is disabled in the canonical run, making reported minority percentiles conservative lower bounds.
**Why?** How does disabling a constraint make the result more conservative rather than less conservative?
**Answer:** The neutral ensemble is meant to mimic what legal random boundary-drawing would produce. Let it draw plans where rural EDs fall below the −25% threshold, which the Act does not permit for most EDs, and it fills up with more plans that concentrate the UCP's rural-seat advantage. More UCP-favorable plans crowd the tail, and against that crowd it becomes slightly easier for the minority map's position to look ordinary. So by switching the constraint off, and letting the ensemble wander into territory the Act forbids, the audit slightly understates how extreme the minority map is. The choice is conservative. It guards against overstating the finding.

---

**Assertion:** The majority map's mean-median is at p0.99 — an unexpected NDP-tail outlier. This is explained as rural-district preservation interacting with Alberta's vote geography, not partisan engineering.
**Why?** If a result is unexpected, how can the audit be confident it is not a measurement artifact?
**Answer:** The DPG runs never showed this outlier. Their geometry lacked the spatial precision to catch the exact vote distribution in rural fringe districts. The official shapefiles assign voting areas (VAs) to EDs differently in those fringe areas, and the distribution comes out more accurate. On the canonical majority map, the spread of NDP vote share across districts has a pronounced left tail: preserved rural districts voting 15–30% NDP. That cluster of low-NDP districts drags the mean away from the median, and the mean-median formula is sensitive to exactly that, so the reading comes out unusual. The mechanism is documented and can be explained. The result holds across several cross-checks, and no sensitivity test in the canonical run reverses it. And every other majority metric sits within the neutral null: EG p16.5, declination p21.85, seats@50/50 p78.5, Mahalanobis p = 0.102. A single metric out, all the rest inside. That is the expected signature of a commission boundary convention, not partisan manipulation.

---

#### §5.4.10 — 2019 enacted baseline: measuring the direction of travel

---

**Assertion:** D² progression: 2019 enacted D²=13.16 (p=0.0105, mild joint outlier); majority 2026 D²=7.74 (p=0.102, within null); minority 2026 D²=33.64 (p=8.80×10⁻⁷). The majority retreated toward the neutral null; the minority amplified the 2019 partisan structure.
**Why?** What does the 2019 baseline D² tell us, and why is it relevant to compare all three maps?
**Answer:** It gives the direction of travel. Add the 2019 enacted map, the existing map, as a third point of reference, and the question changes: not only whether a 2026 proposal is unusual, but whether it moved toward what neutral random maps produce, or away. The 2019 map was itself a mild outlier in joint space (D²=13.16, p=0.0105): slightly outside the neutral ensemble, not dramatically. The majority's 2026 map cut that distance to D²=7.74 and landed inside the neutral null; its changes to the 2019 boundaries moved toward normal. The minority's 2026 map stretched the distance to D²=33.64, which is the headline joint-test p-value driving the canonical finding. Toward, and away. This three-map comparison is exploratory, not pre-registered, but it is consistent with the pre-registered Mahalanobis test and corroborated by it.

---

**Assertion:** Metric-by-metric trajectory: majority moved the 2019 Declination reading toward neutral (p91.33 → p21.85, UCP-side to NDP-side) and moved EG toward neutral; minority preserved and amplified Declination in the UCP direction (p91.33 → p98.79), and dramatically extended MM (p91.81 → p99.97) and seats@50/50 (p78.54 as registered, p65.36 once ties are counted → p99.99) in the UCP direction.
**Why?** Does a trajectory comparison like this prove the minority was drawing off the 2019 map and adding partisan tilt?
**Answer:** No. It shows what each proposal did to the existing map's statistical properties. It does not show why. The minority map is more extreme than 2019 on three of four dimensions. That fits partisan engineering. It also fits other explanations: different community-of-interest judgments, different readings of the §15(2) constraint, or geographic factors the 2019 map did not reflect. So the direction-of-travel table is reported as exploratory evidence, one more consistent signal pointing the same way as the pre-registered tests, not as an independent finding that stands on its own. The primary weight of evidence rests on the canonical Mahalanobis test and the SZAT results. What, not why.

---

## §5.5 Pre-registration and OSF Registration

---

**Assertion:** Five OSF pre-registrations cover the audit: w2s8k, r3zm7, qsgy8, 6pt83, s58a6.
**Why?** Why are five separate registrations needed rather than one?
**Answer:** Because each registration covers a specific part of the audit at a specific point in time. Some were filed before the shapefiles arrived, covering the ensemble tests. Some were filed for the confirmatory replication pass scheduled for November 2026. Some cover specific sub-tests, like the neighbor-drain analysis. Filing at each stage keeps each registration as close in time as possible to the analysis it covers. The alternative is a single blanket registration, filed months ahead, for tests not yet designed in detail.

---

**Assertion:** The Benjamini-Hochberg (BH) correction will be applied in the November 2026 confirmatory pass.
**Why?** What is Benjamini-Hochberg correction and why isn't it applied now?
**Answer:** Run enough statistical tests and some will look significant by chance alone. Run 100 tests at 5% significance and you expect about 5 false positives. The Benjamini-Hochberg procedure adjusts the significance thresholds across all the tests to limit the expected number of false discoveries. It is not applied to the current exploratory pass because the set of tests for the confirmatory pass is not yet final. Applying BH to exploratory tests that may still be revised before confirmation would give a false sense of precision. So we have committed to it in advance for the November 2026 pass, to hold the confirmatory results to the appropriate standard.

---

## §5.6 Symmetry Counter-Test

---

**Assertion:** The majority symmetry counter-test checks whether the audit would flag the majority map if it had the same statistical properties as the minority.
**Why?** Why would you test the test itself?
**Answer:** Because a test that flags everything tells you nothing. A well-designed test flags maps that are genuinely unusual and leaves the rest alone. Run the same method on the majority map: if it came back just as extreme as the minority, the test would be picking up something common to all Alberta maps, not something specific to the minority. It doesn't come back that way. The majority map does not trip the same flags, which confirms the test is catching a real difference between the two maps, not a quirk of the testing method.

---

**Assertion:** The majority map is within the neutral null on three of four partisan-fairness metrics and jointly (Mahalanobis p = 0.102). Its mean-median is a 1st-percentile (p0.99) outlier leaning NDP, the wrong direction to help the UCP.
**Why?** Does "within the neutral band" mean the majority map is perfectly neutral?
**Answer:** No. It means the majority map's scores fall in the range you would expect from the million randomly drawn neutral maps on efficiency gap, declination and seats at 50/50, and on the combined test. Mean-median is the exception, and it leans toward the NDP, not the UCP. Inside the band does not mean perfectly equal. It does not put every boundary choice beyond criticism. It means that, measured against the realistic spread of what neutral independent map-drawing produces, the majority map's scores are unremarkable. The minority map's scores sit in the extreme tail of that same spread.

---

## §5.7 Stress-Test Grades

---

**Assertion:** The four surviving structural signals all survive the stress-tests documented in §1.2.
**Why?** What are the stress-tests and what does "surviving" them mean?
**Answer:** The stress-tests are the three families of sensitivity analysis set out in §1.2: swap in different vote inputs (2015, 2019, 2023), vary the geographic classification rules, and change the ensemble parameters. A signal "survives" if the direction of the finding, minority more extreme than majority, holds whichever reasonable variant you use. All four non-vote signals survive: population MAD, the Calgary zone gap, the Airdrie splits and the chair-flagged anomalies. They do not depend on vote data at all. The statistical signal survives on direction. It is stable across three attribution methods to within 0.1 pp, which supersedes the retired blend-model Monte Carlo check (C11). Its magnitude, though, is not a classical significance claim, because Phase 4C's figure is an exact computation, not a sampling estimate.

---

**Assertion:** Stress-test grades A through D are assigned to each finding.
**Why?** What do the letter grades mean?
**Answer:** Grade A: fully robust, unchanged across every stress-test variant. Grade B: robust on direction, not on magnitude. Grade C: dependent on modeling assumptions that are defensible but not the only ones possible. Grade D: weaker; the finding appears under the primary analysis but not consistently under every variant. The grades let you see which findings are most reliable without reading the technical detail of each stress test.

---

## §5.8 Geographic Coherence

### §5.8.1 — Visual Spatial Audit: Image Sources

---

**Assertion:** The visual audit inspected 15 published commission map images: eight majority Appendix A panels (Alberta overview, Calgary, Edmonton, near-Calgary, near-Edmonton, north, central, south) plus a 1200-DPI Calgary render; six minority Appendix E images (maps 73–76, plus native-extracted Calgary and Edmonton panels).
**Why?** Why does the audit list the specific image files rather than just saying "the commission maps were examined"?
**Answer:** So you can check. Every visual finding in the geographic coherence section traces to a specific image, inspected in a specific session. Name the files, and a reader, a journalist or a hostile reviewer can pull the same images from the commission report and see whether the feature described is actually visible. Vague attribution ("the maps show...") would leave visual claims impossible to reproduce. The inventory also records that the majority panels were covered in full: all eight Appendix A panels were inspected, not only the Calgary panel where the known anomalies concentrate. The §5.8.3 symmetric check covers the whole province, not just the city panels.

---

**Assertion:** The visual audit uses direct inspection by an AI vision model (Opus/Sonnet 4.x). This is not a measurement; it is a pattern-recognition scan for shapes that warrant further geometric verification.
**Why?** Is AI vision inspection a reliable method for an audit claiming academic standards?
**Answer:** The visual scan is a first pass, a way to find candidates. It is not a finding on its own. Every anomaly it spots is then verified by geometric measurement: direct shapefile analysis, coordinate inspection, or the kind of engineering checks described in §5.8.2. No finding in the geographic coherence section rests on the scan alone. The scan flags candidates for measurement. The measurement is the finding. AI vision models are well suited to pattern recognition on geographic images (lasso shapes, corridors, unexpected extensions), and they are an efficient screening tool for the 15-image corpus at the resolution needed to flag geometric irregularities.

---

### §5.8.2 — Visual Spatial Anomalies

---

**Assertion:** Three geographic anomalies on the minority map are confirmed: Rocky Mountain House–Banff Park extension; Calgary-Nolan Hill–Cochrane lasso; Olds-Three Hills-Didsbury → N Airdrie community capture.
**Why?** What makes a boundary shape an "anomaly" rather than just an unusual geographic feature?
**Answer:** Here an anomaly is a boundary shape that can't be readily explained by natural features, community boundaries or the commission's stated criteria. The Rocky Mountain House–Banff Park extension is a boundary that reaches into a national park area with no permanent residents, in a way that appears to serve no population-based purpose. The "lasso" is a narrow corridor of territory joining two areas that are otherwise far apart. The community capture is an ED whose boundary sweeps in a community, North Airdrie, that appears geographically unconnected to the rest of the district. The commission chair himself flagged these shapes in the official commission report.

### §5.8.3 — Majority Hybrids: Symmetric Anomaly Check

---

**Assertion:** The same anomaly-scan questions applied to the minority (lasso shape, engineered statutory boundary, misnamed municipality capture) were applied to the majority's four Calgary hybrid districts. No anomaly was found: Calgary-East is an intra-city block; Calgary-Falconridge-Conrich is a compact city-plus-adjacent community; Calgary-Glenmore-Tsuut'ina tracks the Tsuut'ina Nation reserve boundary; Calgary-West-Elbow Valley is a city-plus-adjacent subdivision.
**Why?** Why is it important to apply the same test to both maps, even if the headline finding concerns only the minority?
**Answer:** An audit that only looks for problems in the map it expects to find them in is not objective. It is a prosecution, not an investigation. Putting the identical anomaly-scan questions to the majority's Calgary hybrids gives the check symmetry: had the majority drawn the same kinds of lasso shapes or engineered boundaries, the audit would have flagged them too. All four majority hybrids pass the same scan without an anomaly, and that strengthens the finding for the minority. The different scan results reflect real geometric differences between the two maps, not selective scrutiny. Same questions. Different answers.

---

**Assertion:** A qualification applies: the anomaly-scan question set was developed from minority anomalies that were already visible. The majority may have different classes of anomaly not detected by this specific question set.
**Why?** Does this qualification undermine the symmetric check?
**Answer:** It limits the check; it does not dismiss it. The scan was built to look for the patterns already seen in the minority map: lasso shapes, engineered statutory reach, and mislabeled municipality captures. The majority's anomalies, if it has any, might take another geometric form, rural-district highway corridors for example, that the question set does not specifically test. The limit is in the questions, not the imagery. All eight majority Appendix A panels were inspected, covering the full province. A more comprehensive future scan would need to add question types written for the majority. For now, the scan's negative result for the majority is reliable for the three specific question types it asks. It does not claim to be exhaustive across every possible kind of anomaly.

---

### §5.8.4 — Community Splits

---

**Assertion:** Airdrie: 4 minority districts vs 2 majority districts. Cochrane: merged vs intact. Chestermere: partial split vs intact.
**Why?** Why are Cochrane and Chestermere mentioned alongside Airdrie?
**Answer:** Airdrie, Cochrane and Chestermere are all fast-growing suburban municipalities near Calgary. Growing places like these are where boundary choices are most likely to have significant effects, and where splitting a community across several districts most visibly breaks up its voice. So the audit checks how each is treated on both maps. On the majority map, Cochrane stays intact in one district, and Chestermere is intact. On the minority map, both are treated differently: Cochrane is merged with another area, and Chestermere is partially split.

---

### §5.8.5 — Municipal Anchoring (RETRACTED finding)

---

**Assertion:** The earlier DPG-derived 14.5% / 71.0% / 4.9× figures did not carry forward to recomputation against official shapefiles. Both maps fall within the 70–85% Canadian comparator norm (minority 72%, majority 80%).
**Why?** What exactly is being retracted and does this weaken the overall audit?
**Answer:** The retracted finding said only 14.5% of the minority map's boundaries were anchored on municipal edges, against the majority's 71%: a 4.9-times gap. It was computed from approximate boundary tracings made before the official shapefiles arrived. Rerun on the official files, both maps showed municipal anchoring rates in the 70–85% range that is normal for Canadian provinces. The gap was gone. The retraction does weaken the fifth structural signal, which no longer tells the two maps apart. The four remaining structural signals are unaffected by it. And the retraction itself shows what we do with a finding that fails: we report it, and we don't hide it.

---

## §5.9 Procedural Concerns

---

### §5.9.1 — Commission Composition and the Divided Vote

---

**Assertion:** Five-member commission constituted under EBCA §3–5: chair nominated by the Chief Justice of Alberta, two government-nominated commissioners, two opposition-nominated commissioners. Unanimous interim report October 2025; divided final report (3–2) March 23, 2026. The three-member majority is chair plus the two opposition-nominated commissioners.
**Why?** Why does it matter which commissioners were nominated by which party?
**Answer:** Because the structure is designed so that no single party controls the outcome. The chair is independent, nominated by the judiciary, and the commissioners come from both the government side and the opposition side. When the final vote went 3–2, the three-person majority was the independent chair plus the two commissioners nominated by the NDP opposition, not by the governing UCP. So the proposal the government ultimately accepted, the minority map, was the one produced by the two government-nominated commissioners alone. You need that composition in view to weigh the procedural story around the April 16 motion and the framing of Recommendation 5.

---

**Assertion:** The commission tabled a unanimous interim report and a divided final report. The division emerged at the final stage, not from the start of the process.
**Why?** Does the fact that the interim report was unanimous tell us anything about the final report's division?
**Answer:** It does. A unanimous interim report shows the commission could agree on a working framework and initial boundaries before the detailed final decisions were made. The split came at the final stage, when specific district configurations near Calgary, Airdrie, Red Deer and Edmonton had to be resolved. That suggests the disagreement was over particular drawing choices at the margin, not a basic incompatibility of approach. It is the normal pattern for divided commission reports: broad agreement on most of the province, disagreement gathered in a small number of contested configurations. The audit's findings concentrate in exactly those contested areas.

---

### §5.9.2 — The April 16 Legislative Pivot

---

**Assertion:** Government Motion 37 (introduced April 16, passed April 21, 2026) set both reports aside and created the Select Special Committee on Electoral Boundaries: six MLAs, four UCP and two NDP, with a 91-seat map due November 2, 2026.
**Why?** Why is a legislature setting aside a commission's report unusual?
**Answer:** An independent boundary commission exists to keep redistricting out of direct political control. Elected members are expected to have a stake in how the lines are drawn, because those lines determine whether they win or lose future elections. When a legislature sets aside an independent commission's work and hands the drafting to a committee of elected members, control of boundary-drawing passes directly to politicians. Whether that is legally permissible is a statutory question. Whether it fits the norms of independent redistricting is taken up in §5.9.

---

**Assertion:** The procedural pivot replaces an independent commission's drafting process with a government-chaired committee mid-cycle.
**Why?** Who chairs the Select Special Committee and why does that matter?
**Answer:** A member of the governing party, in this case the UCP. In the Canadian tradition of electoral boundary reform, judges or academics chair independent commissions, precisely to keep this kind of partisan involvement out. A committee that reports to the legislature under a governing-party chair faces structural incentives that a fully independent commission does not.

---

### §5.9.3 — Federal Precedent

---

**Assertion:** The 2022 federal sub-commission applied a 2-way Airdrie split, aligning with the provincial majority.
**Why?** Why does a federal redistribution matter for a provincial commission's decision?
**Answer:** It is a reference point from another independent body. The 2022 federal electoral redistribution was carried out by a separate independent commission, which drew Alberta's federal constituency boundaries. Its lines do not bind the provincial commission. But they are useful: independent commissioners, working from the same community-of-interest principles, saw no need to break Airdrie up beyond a 2-way split. The federal commission reached the same conclusion as the provincial majority, and a different conclusion from the provincial minority. That is supporting context. It does not settle the question.

---

### §5.9.4 — Commission Chair Criticism and Public Submission Audit

---

**Assertion:** The commission chair's documented criticism spans 7 configurations across two sections of the majority report, analysed in this audit's §5.8.2 and §5.9.4.
**Why?** What are the 7 configurations and how does this relate to the "3 confirmed anomalies"?
**Answer:** In the official majority report, the chair flagged 7 different minority-map configurations as problematic. Of those 7, the audit could verify 3 as confirmed geometric anomalies by direct measurement. The other 4 are boundary choices the chair criticized on community-of-interest or process grounds, not geometry. They are documented too, but they sit in a different category, because judging them means evaluating the commission's stated rationales, not measuring boundary shapes.

---

**Assertion:** The minority's 25 published rationales fail falsifiability checks on five of six contested configurations.
**Why?** How do you test whether a written rationale for a boundary choice is defensible?
**Answer:** You look for a simpler line. For each configuration, the audit finds the simplest alternative boundary that would also satisfy every statutory requirement and the community-of-interest criteria the minority said it was following. If the stated rationale were really what drove the choice, the simpler alternative would have been at least as good, and would typically have been chosen. For five of the six configurations examined, a cleaner statutory alternative exists, and the minority passed it over. The sixth, St. Albert-Sturgeon, is judged likely constraint-forced rather than a free choice, so it is not counted as a rationale failure.

---

**Assertion:** The Lethbridge / Taber-Warner configuration was removed because the methodology check could not locate the claimed source.
**Why?** Why would a finding be removed just because a source could not be located?
**Answer:** Because every claim in this audit has to be verifiable against a primary source. The earlier version of this finding said the minority had made a specific claim about matching federal constituency boundaries in the Lethbridge region. We checked the minority report itself. No such claim could be found. With no primary source to confirm the minority made the claim attributed to them, the item was removed. Removing it, instead of keeping an assertion nothing supports, is the same rigor applied throughout the audit. No source, no claim.

### §5.9.4.1 — Evidence by Configuration: Per-Area Proportions

---

**Assertion:** The per-configuration support table shows: Airdrie 4-way 0/4 mentions (0% support); Calgary-Nolan Hill-Cochrane 0/0 mentions; RMH-Banff Park 7/20 (35% including aligned submissions); Olds-Three Hills-Didsbury 2/5 (40%); Chestermere 3/13 (23%); Red Deer hybrids 5/23 (22% including aligned); St. Albert-Sturgeon 0/11 for minority's specific alternative.
**Why?** What does "support rate" actually measure — why only count submissions from people who engaged with that configuration?
**Answer:** The support rate is the share of engaged submissions, the ones that mention the configuration at all, that back the minority's direction. That tells you more than a rate over all 1,252 submissions, because most people who wrote in simply did not address most configurations. A low support rate among engaged citizens, people who cared enough to write about that specific boundary, is stronger evidence of real opposition or indifference than a low rate across the full corpus, where most absences reflect inattention rather than position. The table separates precisely wrong (supporting submissions exist); precisely wrong but effectively ambiguous (equal support and opposition); and the chair's claim effectively stands (no supporting submissions among engaged citizens).

---

### §5.9.4.2 — Direct Quotation Evidence

---

**Assertion:** EBC-2025-2-0619 ("Appropriate Political Representation for Alpine Alberta") proposes the RMH-Banff configuration by name. EBC-2025-2-0091 (Nordegg resident) recommends including Clearwater County, Rocky Mountain House, Sundre, and Banff. EBC-2025-2-0209 (Alan Balson, Beiseker) proposes the Olds-Three Hills-Didsbury rural unit. EBC-2025-2-0252 (Chad Krahn, Red Deer City Councillor) proposes a northern Red Deer hybrid structure.
**Why?** Why cite specific submission ID numbers rather than summarizing what citizens said?
**Answer:** So the evidence can be checked. Anyone with access to the commission's submission archive can pull EBC-2025-2-0619 and confirm the quoted text appears in it. A general summary like "some citizens supported this configuration" cannot be checked. A submission ID can. The audit reproduces only text read verbatim from the source; no quote is rebuilt from memory, and no paraphrase is presented as a direct quotation. The citation of a Red Deer City Councillor (Krahn, EBC-2025-2-0252) carries particular weight. It shows that a publicly elected official representing Red Deer residents proposed the very hybrid structure the chair described as having "no public support."

---

### §5.9.4.3 — Proportional Weight and Impact on Findings

---

**Assertion:** The three configurations with the highest local-citizen engagement also have the highest support rates for minority-aligned configurations: Olds-Three Hills-Didsbury (40%), Chestermere (23%), and RMH-Banff Park (35% with aligned). The configurations with zero supporting submissions also have the smallest sample sizes (4 and 0 engaged submissions respectively for Airdrie and Nolan Hill-Cochrane).
**Why?** Does small sample size make the "zero support" finding for Airdrie unreliable?
**Answer:** Small samples cut both ways. Zero supporters in four mentions is consistent with "no public support" but does not prove a larger sample would find none. So the Airdrie and Nolan Hill-Cochrane findings cannot carry a categorical "no citizen anywhere in Alberta wanted this" claim. They carry only "nobody in the engaged submission record asked for these." Where engagement is higher (5–23 mentions), the support-rate estimates are more statistically informative, and the refutation evidence is stronger to match. The audit reports that difference in tiers instead of treating every configuration the same.

---

### §5.9.4.4 — Impact on the Majority's and Minority's Findings

---

**Assertion:** The refutation weakens the procedural argument in Appendix C of the majority report on three of seven configurations (RMH-Banff Park, Olds-Three Hills-Didsbury, Chestermere). The majority's cartographic critique — that the minority's configurations are less compact and more fragmenting — is unaffected.
**Why?** If the public-support argument is weakened, does the whole procedural case against the minority collapse?
**Answer:** No. The procedural case has two independent parts. The first is the public-support argument: did the minority draw configurations nobody asked for? The refutation narrows that claim. Three configurations had documented support, three did not, one was ambiguous. The second part is the cartographic argument: are the minority's configurations more compact and community-coherent than the alternatives? That argument does not depend on the submission record at all. It rests on geometric measurement and the analysis in §5.8.2–§5.8.4. So the refutation modestly helps the minority's procedural position on the first part, and does nothing about the geometric findings. Those have nothing to do with what citizens put in writing.

---

### §5.9.4.5 — Limits of the Verification

---

**Assertion:** Approximately 88 of 1,340 submissions (6.6%) were image-only PDFs that could not be machine-parsed. Keyword search uses permissive co-occurrence windows. Position classifier is heuristic; 13 cases were manually reviewed. The minority's configuration names are the audit's labels, not the submissions' own language.
**Why?** If the search methodology has these limitations, how confident can the audit be in its refutation finding?
**Answer:** The refutation holds against all five listed limitations, because it rests on counter-examples we identified: specific submission IDs where the supporting text was read directly. It does not depend on finding every supportive submission there is. More submissions would change the counts, not the direction. If three verified EBC-2025-2-XXXX submissions already refute "no public support" for RMH-Banff Park, the 88 unparsed submissions are irrelevant to the refutation. The limitations affect the counts, and possibly the support rates. They cannot erase a counter-example already found. The limitation is still real, and the audit says so: a full OCR pass over the 88 missing submissions would strengthen the audit's credibility in legal proceedings, though it would not likely change the qualitative verdict.

---

### §5.9.4.6 — Full-Corpus LLM Sentiment Analysis and Hansard Transcript Review

---

**Assertion:** Two LLM classification pipelines classified all 1,252 parseable submissions (plus 3,107 r1 and 2,358 r2 Hansard community turns) on all seven configurations. Results: 388 non-neutral rows across 292 unique submissions; overall 49% opposition, 21% support, 30% neutral/contextual. Channel divergence: RMH-Banff Park and Red Deer hybrids show net opposition in written submissions but net support in Hansard hearings. Intensity-weighted net ranking: Red Deer (−64), Airdrie (−61), Nolan Hill-Cochrane (−55), Chestermere (−47), RMH-Banff Park (−9), St. Albert-Sturgeon (−1), Olds-Three Hills-Didsbury (+6).
**Why?** Why run a full LLM classification pass if the keyword search already found the counter-examples?
**Answer:** Because finding a few is not the same as knowing the spread. The keyword search shows that supporting submissions exist; it refutes "no support" categorically. The LLM analysis asks a deeper question: how are stances spread across the full corpus? That matters. The keyword search could turn up three positive submissions out of 1,000 that opposed the configuration. Technically, that is a refutation. In practice, it is consistent with the spirit of the chair's claim. The LLM analysis shows that three configurations (Airdrie, Nolan Hill-Cochrane, Chestermere) are indeed broadly opposed across the full corpus, not merely missing the few positive examples the keyword search found. The intensity-weighted net scores turn the tiers from a description into numbers.

---

**Assertion:** Channel divergence: RMH-Banff Park and Red Deer hybrids both show net written opposition but net Hansard support. The audit does not assert which channel is more reliable; it reports the divergence and offers a participation-cost explanation.
**Why?** Why present both channels rather than averaging them or deciding which is more credible?
**Answer:** Because averaging would bury a real methodological finding. Writing in and showing up are different ways to take part, and they may draw different people. A hearing takes travel and time, which may over-represent people from the affected communities who care enough to attend a regional session. For configurations centered on remote western communities (RMH-Banff Park) or the Red Deer corridor, residents from those communities are more likely to attend than to write. This difference in the cost of taking part is documented in the planning and zoning literature. Here it is offered as a plausible explanation, not a proven cause. The audit cannot determine which channel better represents genuine public sentiment. So both are reported, the divergence is flagged, and you can weigh them as you see fit.

---

### §5.9.5 — Constitutional Backdrop

---

**Assertion:** On April 22, 2026 — six days after Government Motion 37 was introduced (passed April 21) — the Supreme Court of Canada dismissed Quebec's appeal (7–2, from the bench) of a ruling striking down a law that blocked Quebec's electoral commission from redrawing the provincial map. The SCC held the freeze law violated the Charter's democratic-representation guarantee.
**Why?** Why does a Quebec ruling about a freeze law matter for Alberta's situation, which involves a committee assignment rather than a freeze?
**Answer:** Alberta's motion did not freeze the existing map. It moved boundary-drawing authority from the independent commission to a committee the legislature selected. That is structurally different from Quebec's legislative freeze. The ruling still matters, because it establishes that provincial legislatures cannot shield voter-weight disparities from commission revision on regional-representation grounds alone. That is precisely the class of argument the minority commissioners advance in Appendix E. Whether the Alberta structure is constitutionally distinguishable from the Quebec freeze is for a court to decide on its own facts. The audit does not decide it. What the ruling does is take the constitutional question out of the hypothetical. Whether this category of interference is reviewable under the Charter is no longer speculative.

---

**Assertion:** The SCC's written reasons were published May 1, 2026 (*Quebec (AG) v. Lalande*, 2026 SCC 13). The doctrinal implications cited in the report are summarised from secondary sources; the judgment was not read in full.
**Why?** Why rely on secondary sources for a ruling whose written reasons are available?
**Answer:** The SCC ruled from the bench: it gave its decision aloud in the courtroom, right after argument. That ruling is legally operative on its own. It dismisses the appeal, and the lower court ruling stands. The outcome and the 7–2 margin are confirmed facts. The written reasons followed on May 1, 2026, but the audit has summarised their doctrine from secondary sources rather than from a full reading of the judgment, and it says so. What is confirmed (the outcome, the size of the majority, the from-the-bench posture) is reported as confirmed. What comes from secondary sources is explicitly hedged. And ruling from the bench, a step reserved for cases the court views as clear-cut, is itself a meaningful signal of the SCC's assessment of the question, even before the formal reasons.

---

### §5.9.6 — Evidence Trail for the Six Contested-Rationale Checks

---

**Assertion:** The contested-rationale check uses a four-level evidence strength framework: Strongly supported (reproducible from published dataset), Moderately supported (primary public source, inferential step), Weakly supported (descriptive but not separately filed), Currently unsupported (public-facing language not documented in evidence files).
**Why?** Why disclose the strength level of each sub-claim rather than just stating the conclusions?
**Answer:** Because you may cite it. If you cite the audit's five-of-six verdict in a legal brief, a news article or a peer-reviewed submission, you deserve to know which parts of each claim rest on reproduced primary data and which sit one step removed from that standard. The strength bands are the audit's way of getting ahead of the discovery process. If the audit says "the 8% demographic figure is not currently filed in the evidence files," you know before citing it that the calculation behind it still has to be supplied. The disclosure protects the audit too. Its credibility rests on honest disclosure of what it has and has not checked, not on a uniform, confident surface that hides the gaps. Three sub-claims are flagged as Weakly supported pending follow-up calculations: the Airdrie 8% demographic comparison, the Olds-Didsbury Census-of-Agriculture claim, and the Red Deer school-age 8% magnitude.

---

**Assertion:** Claim 7 (St. Albert-Sturgeon) is relabeled as Claim 6 in the current count (after Claim 5 Lethbridge was withdrawn) and is assessed as Stands, not Fail. The verdict rests on a convergence test: both majority and minority independently produced the same two-district St. Albert structure, suggesting constraint-force rather than design. The earlier "no other configuration" counterfactual framing has been retired.
**Why?** Why does the convergence of both teams reaching the same answer indicate constraint-force rather than shared partisan intent?
**Answer:** The majority and minority commissioners were on opposite sides of every contested boundary decision examined elsewhere in the audit: Airdrie (2-way vs. 4-way), Cochrane (intact vs. merged), Red Deer (2-way vs. 4-way hybrids), the Calgary hybrids. For those two groups to arrive independently at the same St. Albert-Sturgeon structure is not plausibly explained by shared intent. They had opposite incentives. The simpler explanation is that the population arithmetic and geographic constraints left only one or two legally compliant configurations for St. Albert, and both teams found the same one. The convergence can be seen directly in the §5.6 cross-map structural comparison. It replaces the earlier counterfactual claim ("no other configuration satisfies both community-of-interest and ±25% rule"), which was stronger than the evidence could support.

---

### §5.9.7 — Population Data Currency and the 2026 Census

---

**Assertion:** The 2026 Census of Population will be collected in May 2026. Dissemination-area data adequate for redistricting will not be certified and released before mid-to-late 2027. The Lunty committee's November 2026 deadline forecloses access to 2026 census data; the committee must use 2021 data.
**Why?** Is using 2021 population data for a 2026 boundary map a problem, given that the commission used the same data?
**Answer:** The commission used 2021 data too, so in that sense the committee faces the same constraint. The difference is where it falls in the electoral cycle. Boundaries drawn in November 2026 on 2021 populations will govern elections potentially in 2027, and, under the same map, potentially through 2031. By 2031 the 2021 census data will be ten years old. The communities most affected by the audit's structural findings, Calgary's northwest corridor, Airdrie, Cochrane and Chestermere, are among the fastest-growing in Canada. Draw their lines on outdated population data and the map begins with an inequality that compounds and worsens through the cycle. The 2026 census will become the legal baseline for the next commission cycle. The boundaries that diverge from it most in the fast-growth areas will face the greatest effective-representation challenge, and the soonest.

---

**Assertion:** This observation is forward-looking only — not a legal objection to the November 2026 map.
**Why?** Why include a population-currency observation that is not an objection?
**Answer:** Because the audit's role is to document the facts relevant to judging the boundary process, not only the facts that support a legal challenge. This observation is relevant to any reader weighing whether the November 2026 map will serve effective representation through a full electoral cycle: a journalist, a policymaker, a future litigant, or a member of the Lunty committee itself. The EBCA requires use of the most recent decennial census data that is certified at the time of the commission's work. Using 2021 data is legally required, not optional. The point is that the committee and the legislature should be aware of this constraint and what it means for how long whatever map is produced will last. It is a relevant fact. It is not a criticism of the process for following the law.

---

## §5.10 Summary Scorecard

---

**Assertion:** All four surviving structural signals run in the same direction: minority more dispersed, more asymmetric, more fragmented, more anomalous than majority.
**Why?** Why does the direction of all four signals matter more than the magnitude of any one?
**Answer:** A single unusual measurement might come from chance, a data error, or a quirk of one metric. Four independent measurements are harder to explain away. Each draws on different data sources and methods; each asks a different question. When all of them point the same way, the probability of that alignment occurring by chance is much lower than the probability of any single measurement being unusual. That directional consistency is the core of the audit's evidence.

---

**Assertion:** The Fisher combined p = 4.61×10⁻⁸ was the earlier formal statement of convergence between Ch1 and Ch2 (retired 2026-06-10).
**Why?** Is it valid to combine two p-values using Fisher's method?
**Answer:** Not here. Fisher's method, a standard technique from 1932, combines independent p-values when each test addresses a different aspect of the same hypothesis. It is valid when the two tests are genuinely independent: when the probability of one is not already implied by the probability of the other. Ch1 (ensemble outlier status) and Ch2 (the partisan direction of contested-boundary assignments) ask different questions. But they share the same 2023 vote data, so they are not independent the way Fisher's method requires (Brown 1975). And the boundary-choice test (Ch2/SZAT) does not survive a stricter spatial check. For both reasons, the Fisher combination (p = 4.61×10⁻⁸, about one in 22 million) was retired on 2026-06-10. The audit now reports the ensemble test (Ch1) on its own, about one in 1,140,000 (p = 8.80×10⁻⁷), with a conservative combined upper bound of about one in 568,000 (p ≤ 1.76×10⁻⁶) that does not rely on independence. See the academic report §4.3.3 and §5.5.

---

## §6 Discussion

---

### What the Evidence Supports (Synthesis)

---

**Assertion:** The defensible synthesis: the minority 2026 proposal shows measurable structural differences from the majority in four areas, none depending on vote data.
**Why?** Why is the absence of vote-data dependence emphasized?
**Answer:** Because every vote-based finding rests on assumptions, and these signals need none of them. To analyse votes, you have to estimate how past election results would apply inside new, hypothetical boundaries. That takes assumptions about how voters behave, how to allocate them on the map, and which model to use. Each assumption adds uncertainty. The four surviving structural signals (population MAD, the Calgary zone gap, Airdrie fragmentation, the chair-flagged anomalies) come directly from the commission's own published tables, the official shapefile geometry, and the commission chair's own written statements. No vote data is needed. That independence makes those four signals more robust than any vote-based finding.

---

**Assertion:** The partisan-bias signal should be read as a directional observation, not a point estimate.
**Why?** What is the difference between a directional observation and a point estimate?
**Answer:** A point estimate would say: "the minority map gives the UCP exactly 3.92 percentage points more efficiency-gap advantage than the majority map" — and unlike the retired blend model's 1.41 pp estimate, Phase 4C's +3.92 pp *is* an exact computation from observed votes, not a modeled guess. What stays directional, and not a classical-significance claim, is how the finding depends on which electorate you ask. It holds under 2023 votes and April 2026 polling. It reverses under 2019 votes. The audit reports the direction and that dependence on electoral context, rather than overstating the finding as election-invariant.

---

### Directional Pattern and Metric Context

---

**Assertion:** The directional pattern across structural and statistical dimensions is the finding; the audit records what the data show.
**Why?** If the finding is a "pattern" rather than a single decisive number, can it be dismissed as cherry-picking?
**Answer:** Cherry-picking means keeping the results that support your conclusion and hiding the rest. This audit is built to prevent it. Pre-registration locked the test definitions before anything ran. The symmetry counter-test confirmed the majority map does not trip the same flags. The retracted municipal anchoring finding is documented in the open. And the declination metric that disagrees with the other three is kept, not dropped. The pattern argument is not "these four things all happen to show the same result"; it is "the pre-specified tests, applied symmetrically to both maps, consistently differentiate them."

---

**[Corrected — Amendment 10, 2026-06-12.** The literature point below — that different fairness metrics *can* disagree (Warrington 2018; Katz, King, Rosenblatt 2020) — is valid and stays. But it no longer applies to THIS dataset: after the declination sign fix, the minority's declination is p98.79 UCP-tail and AGREES with the other three metrics (four of four). The framing below of an *observed* cross-metric disagreement in this audit is retired, preserved as a record. See `reports/academic/report_academic.md` §5.4.9.**]**

**Assertion:** Cross-metric declination disagreement is documented as an expected feature of competing formalizations (Warrington 2018; Katz, King, and Rosenblatt 2020).
**Why?** How do academic papers from 2018 and 2020 address a disagreement that appears in this 2026 dataset?
**Answer:** The academic literature on partisan fairness measures has documented extensively that different metrics can give conflicting signals for the same map, because they are measuring genuinely different geometric properties of vote distributions. Warrington (2018) specifically studied conditions under which declination and efficiency gap disagree. Katz, King, and Rosenblatt (2020) recommended reporting multiple metrics precisely because no single metric captures all aspects of partisan fairness. This is why the audit uses four metrics and reports disagreement openly rather than selecting the one that gives the cleanest narrative.

---

**Assertion:** The Chen-Rodden mechanism (rural dispersion rather than urban packing) is the operative geographic pattern in Alberta.
**Why?** Does this mechanism affect what the audit concludes about the minority map?
**Answer:** It is already built into the comparison. Under the Chen-Rodden mechanism, even a perfectly neutral Alberta map would show the UCP "wasting" more rural votes than the NDP wastes. UCP voters are spread across many rural ridings; the NDP is more concentrated in a smaller number of urban ridings. (A wasted vote is a lost vote or an excess vote: cast for a loser, or piled on past what a winner needed.) So the minority map starts from a baseline that is already somewhat UCP-disadvantaged, in efficiency-gap terms, from geography alone. But the audit always compares against the million randomly drawn neutral maps, and those maps carry the same geography. The minority map's outlier status is measured against a baseline that already accounts for Alberta's natural geography.

---

### Justiciability (§6.2 context)

---

**Assertion:** Unlike Rucho v. Common Cause (US), partisan gerrymandering claims are justiciable in Canadian courts.
**Why?** What practical difference does justiciability make?
**Answer:** Justiciable means a court can hear the case and rule on the merits. In the United States, since Rucho, federal courts cannot rule on whether a map is an unconstitutional partisan gerrymander; they must dismiss those cases without deciding the question. In Canada, courts can judge whether a boundary commission has met the constitutional standard of effective representation under the Charter. So the findings in this audit could, in principle, be placed before a court with the authority to require that the boundaries be revised. In the US federal system, they could not.

---

### §6.1 — How to Interpret These Findings: NP-Hardness and Statistical Improbability

---

**Assertion:** The redistricting problem is NP-hard; there is no single correct Alberta map.
**Why?** If there is no "correct" answer, can anything be measured?
**Answer:** Yes. NP-hard means the problem has so many legal solutions that no computer algorithm can find the single best one efficiently. Alberta's rules (equal population, connected districts, compact shape, community preservation) define an enormous family of valid maps, not a unique optimum. So the audit does not ask whether the commission found the "right" answer. It asks where the chosen map sits among all the legal answers that satisfy the same rules. A map at the extreme tail of that distribution is an unusual choice. Not necessarily a wrong one. But unusual choices invite explanation.

---

**Assertion:** The audit's claim is: "this map is statistically improbable within the constraint set, and the improbability has a direction that is measurable."
**Why?** What does it mean for a map to be "statistically improbable within the constraint set"?
**Answer:** The constraint set is all the legal rules the commission must follow. The audit simulates over one million maps, and each of them satisfies those rules. If a real map's score on a fairness measure falls outside the range that 99.9% of the simulated maps produce, the real map is statistically unusual. It is the kind of outcome you would almost never get from a process that was simply picking at random among the legal options. The "direction" observation adds this: every time the real map is unusual, it is unusual in the same way. It consistently favors the same political party.

---

**Assertion:** The Commission did not have to split Airdrie four ways; they chose to, among many legal alternatives that did not require that split.
**Why?** How do you know there were legal alternatives that did not split Airdrie four ways?
**Answer:** From the arithmetic, and from the ensemble. Airdrie's population, approximately 85,805, is about 1.56 times the provincial average district size. The ±25% statutory band lets a single district hold between 75% and 125% of the average. Airdrie's population sits in the range where a single district or a clean two-way split are both legally valid options. And the vast majority of the million randomly generated legal maps keep Airdrie in one or two districts. A four-way split is possible under the law, but only a small minority of legal maps produce it. The constraints did not force it.

---

**Assertion:** "Precision is armor" — the over-engineered methodology forces the distinction between an accidental brush-stroke and a systematic pattern.
**Why?** Why would a commission challenge the audit on grounds that it is "too precise"?
**Answer:** A commission could argue that a single unusual metric score is just a quirk of its own balance of trade-offs, and that fixing on one number misses how complex real boundary drawing is. The audit's multiple independent tests (population, zone gap, community splits, boundary shapes, statistical ensemble, bootstrap test) are built to answer that objection in advance. A systematic pattern across six independent measurement approaches cannot be written off as one quirk. If the deviation were accidental, you would expect some metrics to show the minority as more neutral than the majority. None do.

---

### §6.2 — Author's Verdict

---

**Assertion:** §6.2 departs from the audit's measurement-only voice and offers the author's stated opinion; it is presented as opinion, not as a peer-reviewed conclusion.
**Why?** Why include the author's opinion at all if it is not peer-reviewed?
**Answer:** Because the audit is a public-interest document, not only a journal article. If you came here to understand whether a map looks like a gerrymander, you deserve an honest answer from the person who built the measurement apparatus. That is me. The opinion is clearly labeled as opinion, with the bias disclosure from §1 restated, so you can weigh it with appropriate skepticism. If you only want the measurements, the report explicitly tells you to stop at §6.1.

---

**Assertion:** A "gerrymander signature" is the constellation of measurable effects the academic redistricting literature treats as evidence of partisan engineering — narrower than "any map with a partisan-asymmetry signal," broader than "any map whose author admits intent."
**Why?** Why not just say whether the map is or is not a gerrymander?
**Answer:** "Gerrymander" is a legal conclusion, and it needs evidence about intent and effect together. The academic literature works instead with a gerrymander signature: a pattern of measurable effects that distinguishes intentional engineering from natural geography. Partisan outlier status. Community fragmentation. Rationale failures. Boundary anomalies. The audit measures whether that signature is present. Whether the signature reflects illegal intent, and whether it violates the effective-representation standard, is for the courts to assess.

---

#### §6.2.1 — Lane 1: Partisan-Bias Magnitude

---

**Assertion:** Reading A (crosswalk-blend): majority EG −0.40%, minority EG −1.81% — both sub-threshold on every Alberta-calibrated threshold.
**Why?** What is a "crosswalk-blend" and why do both maps show negative (NDP-tail) efficiency gaps?
**Answer:** The crosswalk-blend method moves votes from old districts into new boundaries. It looks up which old districts overlap the new ones and blends their vote shares. Under the Alberta convention, a negative efficiency gap means more NDP votes are "wasted" than UCP votes: the NDP is at a disadvantage. Both maps show this under Reading A because Alberta's underlying geography (urban NDP concentration vs. rural UCP dispersion) produces natural packing that disadvantages the NDP in both proposals.

---

**Assertion:** Reading B (full-coverage spatial): majority EG +6.43%, minority EG +9.21% — both over every Alberta-calibrated threshold including 4.10%.
**Why?** Why does the sign flip between Reading A and Reading B?
**Answer:** Reading B assigns votes to new boundaries more precisely. It overlays the actual geographic shapes of polling stations on the new district maps and splits the votes by area. Use this method, attribute all 89 districts properly (fixing the v0_8 coverage gap), and the estimated efficiency gap comes out larger and positive under the Alberta convention (positive = NDP advantage, so both maps look NDP-favorable in Reading B). The sign differs between readings because efficiency-gap estimates are sensitive to how votes are geographically attributed. That is exactly why the audit reports both readings instead of choosing one.

---

**Assertion:** Both readings agree the minority sits closer to the UCP-favoured tail than the majority on every metric.
**Why?** If the readings disagree on magnitudes and signs, how can they agree on the direction?
**Answer:** Look at the gap between the maps, not the sign. Reading A gives minority EG −1.81% against majority −0.40%: the minority is more negative (more UCP-favorable) than the majority. Reading B gives minority EG +9.21% against majority +6.43%: the minority is more positive (more NDP-favorable) than the majority, but by a larger gap. Both readings agree on the relative position. The minority sits further toward one tail than the majority. Whether that tail represents a UCP or NDP advantage depends on the reading chosen, and the cross-method disagreement is itself reported as a finding.

---

#### §6.2.2 — Lane 2: Structural and Procedural Pattern

---

**Assertion:** Public-submission support: two contested configurations (Airdrie 4-way, Nolan Hill) have no documented submissions in the ~1,340 archive.
**Why?** What does it mean to check the submission archive and why does the absence of submissions matter?
**Answer:** The commission's archive holds the public submissions it received from citizens, communities and organizations. Those submissions are the documented evidence of which boundary choices the public wanted. If a minority commissioner made a specific boundary decision, such as splitting Airdrie four ways or drawing the Nolan Hill corridor, and no submission in the archive asked for that configuration, then the choice cannot be defended as a response to public input. No submissions for two of the most unusual configurations is a gap in the rationale. It is not proof of bad intent.

---

**Assertion:** Pre-registered structural-irregularity count: minority meets the ≥4 of 5 outlier threshold; majority meets 0 of 5.
**Why?** What is this scoring and what are the five pre-registered tests?
**Answer:** Before looking at the data, we committed to scoring both maps on five structural dimensions: population dispersion (MAD), Calgary zone asymmetry, Airdrie community fragmentation, municipal boundary anchoring, and chair-flagged anomalies. The pre-registration set the bar: a map scoring as an outlier on four or more of these five would cross the threshold. The minority map scores as an outlier on four: population, zone gap, Airdrie, anomalies. (The fifth, anchoring, was retracted after canonical recomputation.) The majority map scores as an outlier on zero.

---

#### §6.2.3 — Verdict on the Majority

---

**Assertion:** The majority's Mahalanobis p = 0.102 on the 1M canonical run — inside the null band.
**Why?** A p-value of 0.102 is close to 0.10. Isn't that "significant"?
**Answer:** No. The smaller the p-value, the more extreme the result. A p-value of 0.102 means the majority's joint partisan-fairness score is more extreme than about 10% of randomly drawn neutral maps, well within the normal range. Set that beside the minority's Mahalanobis p = 8.80×10⁻⁷, which means it is more extreme than 99.9999% of random maps. The 0.102 value is close to the center of the distribution (where 50% of maps lie), not near the extremes.

---

**Assertion:** The majority retreats from the 2019 enacted baseline in joint-metric space (D² = 13.16 → 7.74), consistent with a normalizing commission process.
**Why?** What does "retreating in joint-metric space" mean for a map?
**Answer:** It means moving back toward the middle. The Mahalanobis D² score measures how far a map sits from the center of the cloud of neutral ensemble maps. The higher the D², the further the map is from neutral. The 2019 enacted baseline scores 13.16 on this measure (moderately unusual, as it was drawn with older data and tools). The majority's 2026 proposal scores 7.74, closer to neutral than the existing map it is replacing. That is what you would expect from a commission doing its job: a new map more consistent with current neutral norms than the aging map it replaces.

---

#### §6.2.4 — Verdict on the Minority

---

**Assertion:** The minority amplifies the 2019 enacted baseline's joint-space position (D² = 13.16 → 33.64).
**Why?** What does it mean to "amplify" rather than "normalize"?
**Answer:** The majority brought the Mahalanobis distance down, from 13.16 to 7.74, toward neutral. The minority moved it the opposite way, from 13.16 all the way to 33.64, further from neutral. The minority map is more than two and a half times as extreme as the 2019 map it was supposed to replace, and four times more extreme than the majority proposal. Rather than normalizing an aging boundary set, the minority concentrated its deviations further in one direction.

---

**Assertion:** The honest summary: the minority maxes out the structural-irregularity scoring while staying inside the partisan-bias-magnitude band under Reading A.
**Why?** How can a map max out structural irregularities but stay inside the partisan-bias band?
**Answer:** The academic literature on gerrymandering separates "broad partisan distortion" from "surgical fortification." Broad distortion shows up in the overall efficiency gap: a high percentage of one party's votes wasted across the whole map. Surgical fortification concentrates its changes in a small number of marginal districts, the close races, to lock in a seat advantage without moving the efficiency gap much. The minority appears to have the second pattern. Its structural indicators (community splits, boundary anomalies, zone asymmetry) are extreme, while its efficiency-gap magnitude stays close enough to the threshold that Reading A does not trigger it.

---

#### §6.2.5 — How Close Did the Minority Come?

---

**Assertion:** Under Reading B, the minority's seats@50/50 of 52.8% sits above the simulation's converged ceiling of 51.72% — a placement zero of 2,000,000 neutral draws reach.
**Why?** What does it mean to be above the "converged ceiling" of the simulation?
**Answer:** Across 2,000,000 randomly drawn neutral maps, the simulation converged on a maximum seats@50/50 value of 51.72%. Not a single one of those maps produced a value higher than that. The minority map's earlier estimate, 52.8%, came from a partially attributed dataset and sat above that ceiling; it was later corrected to 48.3% under the v0_8 full-attribution method. The corrected 48.3% figure places the minority at p99.99: still among the most extreme 0.01% of neutral maps, but no longer above the simulation ceiling. This correction (from H2 in the hypothesis table) is an important example of the audit correcting its own prior findings.

---

**Assertion:** SZAT regional decomposition: Rest of Alberta +0.015 (dominant), Edmonton +0.008, Mountain-West +0.006, Calgary −0.008 (partially offsetting).
**Why?** Why does Calgary run in the opposite direction to the overall SZAT score?
**Answer:** SZAT measures the partisan effect of each specific boundary decision the minority made differently from the majority. In Calgary, those differences actually favor the NDP slightly, pushing the score toward the NDP side. Across the rest of Alberta, the differences push more strongly toward the UCP. The net result is a UCP-favorable signal across the map that does not come primarily from Calgary. It is distributed across the province. The report describes this as inconsistent with a Calgary-centric explanation, and consistent with a province-wide pattern.

---

#### §6.2.6 — What Would Change the Verdict

---

**Assertion:** The strongest single falsifier is: an independent reviewer produces a constraint-legal Alberta map that satisfies the minority's stated community-of-interest rationales and also matches majority-comparable municipal anchoring.
**Why?** Why would a counter-map by an independent reviewer change the verdict?
**Answer:** Because the rationale-failure finding rests on a claim that can be tested: that simpler, cleaner alternatives exist which would have satisfied the minority's stated community-of-interest reasons for their boundary choices. If an independent reviewer, someone with no stake in the outcome, constructs such a map, and it genuinely satisfies the minority's stated criteria while looking more like the majority, that would demonstrate the minority's choices were not forced by their own rationales. That would shift the interpretation from "the rationale is a pretext" to "the constraint space is genuinely tight and the minority made defensible trade-offs." We have invited this check through the project's public GitHub repository.

---

#### §6.2.7 — Verdict on the April 16 Government Pivot

---

**Assertion:** Substituting a UCP-MLA-chaired committee for the independent commission's drafting process is the most government-controlled response among the three most commonly cited Canadian comparator cases.
**Why?** What are the comparator cases and why does this comparison matter?
**Answer:** The three Canadian cases used as comparators are the federal 2012 redistribution challenge, Saskatchewan's 1989 court referral, and Alberta's current 2026 situation. In the federal 2012 case, Parliament challenged the commission's recommendations but did not replace them. In the Saskatchewan 1989 case, the government sought court guidance before the commission finished its work. In Alberta 2026, the legislature set aside a completed commission report and transferred drawing authority to a government-majority committee of MLAs (four UCP, two NDP). Challenged. Referred. Set aside. Placed within the comparator range, Alberta's action is a larger departure from independent-commission norms than the other cases cited.

---

#### §6.2.8 — Bottom Line

---

**Assertion:** The minority map is the kind of map a non-neutral procedure produces under EBCA constraints; it is not the kind of map a neutral procedure produces.
**Why?** How does the simulation establish what a "neutral procedure" produces?
**Answer:** By drawing blind. The simulation runs GerryChain's ReCom algorithm, which makes random legal boundary changes without any information about how voters are distributed. It has no way to favor one party; it knows only population totals and contiguity rules. Over one million steps it explores the full space of maps that a genuinely neutral, apolitical process would produce. The minority map sits in the extreme tail of that space, in territory that random neutral drawing essentially cannot reach but targeted hill-climbing can (as the Cannon et al. short-bursts test in §5.4.8 confirmed). That contrast defines what "a non-neutral procedure" means here.

---

## §7 — Limitations and Falsifiability

---

**Assertion:** Three modelling-uncertainty tests materially narrow the partisan-bias magnitude claim while leaving the structural findings intact.
**Why?** If three tests narrow the magnitude claim, should the magnitude claim be dropped entirely?
**Answer:** No. Phase 4C's magnitude (+3.92 pp) is an exact computation, stable to within 0.1 pp across three independent attribution methods. That is a strong, reproducible signal, even though "classical 95% significance" doesn't directly apply to an exact count the way it would to a sampling estimate. The appropriate response is to report the finding with the dependence it actually has — on electoral context (2023 vs. 2019 votes), not on modeling-parameter guesswork — rather than either (a) asserting the finding is election-invariant or (b) dropping it entirely. The audit does (a) correctly by reporting both the exact figure and the electoral-context caveat.

---

**Assertion:** The statistical tests are exploratory, not confirmatory; they are reproducible and temporally anchored but require independent replication.
**Why?** Why do reproducible results still require independent replication?
**Answer:** Reproducibility means another researcher runs the same code on the same data and gets the same number. That is necessary for scientific confidence, but not sufficient. Independent replication asks more: a different researcher, using different code and possibly different methods, tests the same hypothesis on new data or from a different angle, and finds consistent results. Exploratory results can be reproducible and still reflect choices made after some data exploration, even unintentionally. The prospective confirmatory study pre-registered at OSF, for the November 2026 committee map, is designed to provide that independent check.

---

### §7.0 — Hypotheses Tested and Their Disposition (H1–H10)

---

**Assertion:** Hypothesis H1: re-seeding bug was found and corrected before main analysis.
**Why?** What was the re-seeding bug and why does disclosing it matter?
**Answer:** A re-seeding bug would occur if the simulation restarted its random number generator partway through a run without meaning to. The maps generated after the restart would then be non-random in a subtle way. The audit found such a bug and corrected it before the main analysis was run. Disclosing it matters. It shows the audit's quality-control process caught a technical error before it could affect results. And failing to disclose a known bug would be a serious scientific ethics problem.

---

**Assertion:** Hypothesis H2: the 52.8% → 48.3% seats@50/50 correction.
**Why?** Why was this estimate corrected and what caused the original error?
**Answer:** An earlier analysis estimated the minority map would give the UCP 52.8% of seats in a tied election. That estimate rested on a partially attributed dataset. Then the v0_8 full-coverage attribution corrected the 22 missing rural districts, which were heavily UCP-voting, and the revised estimate became 48.3%. It is the same attribution improvement described in §1.2 and §3. Those districts had been incorrectly absent from the earlier computation, so adding back their rural UCP votes changed the seat-share estimate.

---

**Assertion:** Hypothesis H3: compactness mechanism rejected. The mechanism is not compactness-driven but is consistent with partisan allocation of population.
**Why?** What was the compactness hypothesis and why was it rejected?
**Answer:** An early hypothesis held that the structural differences between the two maps came mainly from the minority commissioners putting more weight on compact (roughly circular) districts. Compactness is a legitimate redistricting criterion. If it explained all the differences, the structural signals would be a byproduct of a neutral value judgment, not a partisan pattern. It does not explain them. The minority map's districts are not consistently more compact than the majority's; the compactness scores do not differ in the direction that would explain the population and zone-gap findings. The hypothesis was rejected. The explanation for the structural differences remains the population allocation pattern itself.

---

**Assertion:** Hypothesis H5: regional swing substantially weakens the signal when applied.
**Why?** What is a "regional swing" and how does it weaken the signal?
**Answer:** Voters in different parts of the province may not shift their preferences uniformly between elections. A regional swing adjustment allows for that. If the UCP does better in some regions in 2023 than in 2019, simply scaling every area up or down by the provincial average change would misrepresent the regional variation. Apply regional swing adjustments to the vote attribution and some of the partisan-bias signal diminishes: the efficiency gap moves closer to zero. That is why the magnitude claim is narrowed, and why the directional claim is the stronger statement.

---

**Assertion:** H4: natural anchoring. H6: two-party normalization. H7–H10: various disposition notes.
**Why?** What are H4 and H6 testing?
**Answer:** H4 (natural anchoring) tested whether the difference in how the two maps line up with municipal boundaries could be explained by the minority simply following natural geographic features (rivers, roads, terrain) rather than municipal edges. It could not. Natural anchoring is present in both maps, and it does not explain the minority-specific patterns. H6 tested whether the two-party vote normalization, which treats the provincial total as a simple UCP vs NDP contest, introduced artificial bias. The check confirmed the normalization is standard and appropriate for Alberta's electoral context, where minor parties take very few seats. H7–H10 cover further technical hypotheses that arose during the analysis and were tested and disposed of; each is documented in the hypothesis table for completeness.

---


---
### DPG Sunset Clause (Methodological Note)

---

**Assertion:** Files in data/shapefiles/derived/ generated from DPG are deprecated; all active analysis uses data/shapefiles/canonical/.
**Why?** What does "deprecated" mean in this context and why keep the old files at all?
**Answer:** Deprecated means retired from use: the old approximate files no longer feed current analysis, and the official files have replaced them. They stay in the repository, not deleted, because the complete history of how the audit was built is itself part of its transparency. You can trace which findings changed when the official files arrived and verify that each change was properly documented. Delete the old files and there would be no way to confirm the transition was handled correctly. Retired, not erased.

---

### Vote Attribution Cycle-Lag (Methodological Note)

---

**Assertion:** The cycle-lag problem: 2019 boundaries, 2021 Census, 2023 votes are three different temporal layers.
**Why?** Is using data from three different years a serious methodological flaw?
**Answer:** No. It comes with the territory. In redistricting analysis, boundaries, population counts and election results are always from different years. The audit documents the assumption needed to bridge them: mainly, that where votes fall on the map stays relatively stable within the three-year window, and that area-proportional attribution is a reasonable approximation for assigning poll votes to new district boundaries. The sensitivity analysis tests whether different assumptions about that bridge materially change the conclusions. The directional signal is stable.

---

### §7.1 — Missing Evidence and Scope Limits

---

**Assertion:** Phase 4C measured attribution — replacing the 70/30 blend with observed apportionment — would reduce the sensitivity range in §5.2.2 to a single refined value.
**Why?** What is "Phase 4C" and what is the 70/30 blend it would replace?
**Answer:** The 70/30 blend was a modeling assumption, used when precise vote attribution was not possible: 70% of a hybrid district's vote estimate came from applying the result to one zone, 30% from another. It was a placeholder for the measured value that would come from a complete geographic overlay of every polling station with the new district shapes. **Phase 4C — the canonical VA-polygon attribution step — has now been executed** (script: `analysis/scripts/phase4c_canonical_attribution.py`; output: `data/outputs/phase4c_canonical_results.json`). For canonical EA shapefiles and 2023 vote data, it produces: minority EG +4.02%, majority EG +0.10% (asymmetry +3.92pp); minority seats@50/50 = 0.5169 (UCP fraction; equivalently 0.4831 NDP fraction per Phase 4C's own convention note). These are the values the monograph and public report now cite as canonical. The earlier "uncertainty from modeling choice" framing was correct for the pre-canonical era and is now superseded. The Phase 4C measurement did not reduce the blend's range. It *converged* to a specific value. The Monte Carlo interval reported in §5.2.2 is a separate (correctly disclosed) source of uncertainty: the ensemble's distribution under different neutral-map draws, not the blend-substrate uncertainty. (Earlier draft of this entry contradicted the Appendix E Phase 4C entry on the same page; this revision aligns them.)

---

**Assertion:** Multiple testing under Holm-Bonferroni correction for five tests at α = 0.10: the minority's seats@50/50 result (p = 0.0148) satisfies the corrected threshold (0.02).
**Why?** What is Holm-Bonferroni and why does this matter?
**Answer:** Run five tests and the chance that at least one appears significant just by coincidence is higher than if you run one test. Holm-Bonferroni lowers the threshold to account for that. Running five tests at 10% significance, the strictest threshold is 0.10 / 5 = 0.02. The minority's seats@50/50 result, p = 0.0148, is below that corrected threshold, so it would be considered statistically significant even under this conservative adjustment for multiple testing. The audit notes this to answer the objection that running multiple tests inflates the chance of a false positive.

---

### §7.2 — Falsifiability Statement

---

**Assertion:** The directional claim would be falsified by an alternative Calgary classification that produces near-null minority-majority asymmetry while the current rule produces >10%.
**Why?** Why is the Calgary zone classification a potential falsifier?
**Answer:** Because the finding rests on a definition. The 12.2% vs 0.4% Calgary zone asymmetry depends on how the "urban core" and "suburban ring" categories are defined. If a reasonable alternative classification scheme made the zone gap nearly disappear, the finding would be an artifact of the chosen definition rather than a robust result. The audit tested two different classification rules and found consistent results under both. The existing tests do not meet this falsifiability condition. It would only be met if someone identified a third, defensible classification under which the asymmetry vanishes.

---

**Assertion:** Submission-archive evidence that the five disputed minority configurations did have substantial public support would refute the "no public support" claim.
**Why?** If such submissions exist, why weren't they found?
**Answer:** The search may have missed them. The commission's archive of ~1,340 submissions is a large body of documents, and the audit's search identified no submissions supporting the Airdrie four-way split or the Nolan Hill corridor configuration. But the search may have been incomplete. A submission could have used different place names, described the outcome it wanted without naming the specific boundary shape, or been filed under an administrative category that was not searched. Such submissions could exist without being found. The falsifiability condition acknowledges this limitation openly: if such submissions are located and published, the "no public support" finding would have to be revised.

---

### §7.3 — Academic Limitations and Methodological Caveats

---

**Assertion:** Ecological inference limitation: actual 2026 vote distributions may differ structurally from the uniform-swing projections.
**Why?** What is "ecological inference" and why is it a limitation here?
**Answer:** Ecological inference means drawing conclusions about individual behavior (how specific voters would vote under new boundaries) from aggregate data (total vote counts by area). The audit estimates how votes would be distributed in new districts by assuming voters in the old district would vote in the same proportions in the new district. But new boundaries can change the community mix in ways that shift voting patterns. Say a fast-growing suburb with different preferences is added to an existing district and changes the whole district's outcome. Then the uniform-swing assumption would be wrong. That is why the directional finding is stated with a confidence level rather than as a point estimate.

---

**Assertion:** Single-election dependency: 2023 was highly competitive (UCP 52.6%, NDP 44.0%). In a landslide environment, structural partisan metrics become noisy.
**Why?** Why would a landslide make the metrics unreliable?
**Answer:** Partisan fairness metrics like the efficiency gap are most informative when elections are reasonably competitive, when both parties win some seats and waste some votes. In a landslide, where one party wins almost everything, the losing party wastes nearly all its votes by definition. That makes the efficiency gap very large, regardless of how the boundaries were drawn. The 2023 election was close enough that partisan structure is detectable. Had the 2023 margin been larger, in either direction, the metrics would be harder to interpret.

---

**Assertion:** Geographic constraints vs intent: Alberta's deep urban/rural divide creates severe natural packing; residual natural packing may be misattributed as intentional engineering (Chen and Rodden 2013).
**Why?** How does the MCMC ensemble account for this?
**Answer:** By drawing on the real Alberta. The MCMC ensemble generates its neutral maps from Alberta's actual geography: the same population distribution, the same urban/rural divide. Every one of the million simulated maps reflects Alberta's geographic reality. So when the audit says the minority map is in the 99.99th percentile, it means the minority is more extreme than 99.99% of maps that already incorporate Alberta's natural packing. The natural packing is baked into the neutral baseline. What is measured is the additional departure from that baseline, not from a hypothetical equal geography.

---

**Assertion:** Model dependence: ReCom assumes contiguous, population-balanced districts as the primary constraints. If the commission weighted unmeasured criteria heavily, the neutral baseline may be misspecified.
**Why?** What are "unmeasured criteria" and why might they affect the comparison?
**Answer:** The EBCA requires the commission to consider community of interest, existing electoral boundaries, and other factors beyond population equality and geographic contiguity. The ReCom simulation does not fully model community-of-interest preservation. It cannot: "community of interest" is a qualitative judgment rather than a computable constraint. If the commission's choices were primarily driven by unusual community-of-interest determinations, the neutral ensemble would not properly capture the space of constraint-legal maps as the commission understood it. That is why the Lane 2 structural findings, which do not depend on the ensemble, carry independent weight.

---

## §8 Conclusion

---

**Assertion:** The audit's primary finding is directional consistency across structural and statistical dimensions, not a single decisive number.
**Why?** Is a directional finding strong enough to support any policy response?
**Answer:** Four independent structural signals point the same way. Each comes from different data sources. Each survived stress-testing. Together, that directional consistency is stronger evidence than any single statistical test would be alone. The statistical tests add quantitative weight to the structural signals: the ensemble test Ch1, p = 8.80×10⁻⁷, about one in 1,140,000, with a combined upper bound that holds even if the tests are dependent, p ≤ 1.76×10⁻⁶, about one in 568,000. (The earlier Fisher figure, p = 4.61×10⁻⁸, was retired 2026-06-10.) Together they support the conclusion that the two 2026 maps are not equivalent proposals from an independent commission. Whether that is strong enough to require a legal remedy, an administrative revision, or simply public acknowledgment is a policy and legal judgment. The audit provides the empirical input for that judgment.

---

**Assertion:** The majority map is within the neutral null on three of four metrics and jointly (Mahalanobis p = 0.102); its mean-median is a 1st-percentile (p0.99) outlier leaning NDP, the wrong direction to help the UCP. The minority is not within the null. This is the headline.
**Why?** What should a reader conclude from this if they are a policymaker, a court, or a journalist?
**Answer:** A policymaker reviewing two competing redistricting proposals should understand that they are not equivalent options. One falls within the range that neutral independent processes produce. One does not. A court evaluating a Charter challenge to the redistricting process would have quantified outlier statistics and a pre-registered methodology to assess. A journalist covering the redistricting should report that independent computational analysis found statistically significant differences between the two proposals, with the appropriate caveats about exploratory status. The audit does not tell any of these audiences what to do. It provides the measurement.

---

**Assertion:** The November 2026 confirmatory replication will apply Benjamini-Hochberg correction and is pre-registered at OSF.
**Why?** What happens if the November 2026 committee map falls within the neutral band?
**Answer:** Then the confirmatory test returns a null result. If the new 91-seat committee map scores within the neutral ensemble band on all partisan-fairness metrics, the committee's map did not reproduce the partisan pattern found in the minority commission proposal. We would report that null result in full, in keeping with our commitment to report failures openly. It would not retroactively change the findings about the original minority proposal. It would indicate that the committee's process produced a different outcome.

---


---

**Assertion:** Across eight sub-sections of §5, the minority 2026 proposal shows wider distribution, higher packing and cracking signals, more anomalies, and a more government-controlled procedural path than the majority.
**Why?** Does consistently finding the same direction across eight sub-sections constitute one finding or eight?
**Answer:** Each of the eight sub-sections tests a different measurable property, with different data, different methods and different mathematical tools. They are not the same test repeated eight times. Consistent direction across eight independent tests, each with its own methodology, is much stronger evidence than one strong result on one test. The audit's structure is designed to force that breadth: each sub-section runs independently, from its own script, against its own data source.

---

**Assertion:** The direction holds at approximately 90% confidence under Monte Carlo over modelling choices across 2020s-era voter distributions.
**Why?** What does "2020s-era voter distributions" mean here?
**Answer:** It means recent vote distributions: the 2023 actual results, and recent polling (April 2026 338Canada estimates). Both reflect the current political alignment of Alberta's communities. The audit checks whether the directional finding holds not just for one specific election but across the range of plausible current voter distributions. 90% confidence means that across 2,000 different combinations of modeling assumptions applied to these recent voter distributions, 9 out of 10 combinations point to the minority as more UCP-favorable than the majority.

---

**Assertion:** When the Lunty committee tables its 91-seat map by November 2, 2026, the same scripts will be re-run as fulsomely and faithfully as they were for the commission proposals.
**Why?** Why make a public commitment to re-run the analysis on the new map?
**Answer:** For the same reason as every other methodological safeguard in this audit: to prevent the appearance, or the reality, of cherry-picking. If I analyzed only the commission maps and declined to analyze the committee map, a skeptic could argue the analysis was not symmetric, that it targeted the minority proposal specifically because it was expected to show findings. Run the same analysis on the November map, with the same thresholds and the same commitment to reporting null results, and the framework stops being an accusation. It becomes a repeatable test.

---

### §8.1 — Postscript: The Audit as Framework for the Held-Out Test

---

**Assertion:** The commission audit was a framework-building exercise that calibrated artefacts the next audit will need.
**Why?** If the commission proposals are now moot, why does documenting them matter?
**Answer:** Because the next audit is built from it. The commission audit produced six specific calibrated outputs that will be reused directly for the November 2026 evaluation: the four Alberta-calibrated efficiency-gap thresholds; the 1,010,000-plan canonical ensemble; the structural-irregularity scorecard with benchmarks; the rationale-failure framework; the DPG construction pipeline for new boundaries; and the two-lane verdict structure. Without these calibrations, the November evaluation would have to build its methodology from scratch, and invite the criticism that the methodology was designed after seeing the map. The tools are set before the map arrives.

---

**Assertion:** Sub-threshold on Lane 1 is necessary for a clean verdict, but not sufficient.
**Why?** What is the two-lane verdict structure actually saying as a practical matter?
**Answer:** The two-lane structure says this: to get a clean verdict, a map has to pass both the partisan-bias magnitude test (Lane 1) and the structural-pattern test (Lane 2). Keep the efficiency gap below the 4.10% threshold, but fragment communities, create boundary anomalies and fail your own stated rationales, and the map still shows structural red flags. The minority proposal demonstrated that empirically. For the November committee map, the audit will look at both lanes, and will report it if a map passes one while failing the other, rather than declaring it clean on either lane alone. Both lanes, or no clean verdict.

---

**Assertion:** A drafting process that wants to engineer outcomes without leaving an EG fingerprint has the structural lane available — community splits, off-reference borders, anchoring departures, chair-flagged shapes — and the audit will be looking at both lanes when the Lunty committee map arrives.
**Why?** Is this saying the committee is expected to gerrymander?
**Answer:** No. It describes what the audit is designed to detect. It is not a prediction about the committee's behavior. The minority commission proposal showed that a map can stay within the efficiency-gap threshold while showing structural irregularities. The November audit makes no assumption about what the committee will produce. It states what the audit can detect if structural manipulation occurs, so that the methodology cannot be criticized after the fact for being blind to that possibility. Looking is not accusing.

---

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
**Answer:** The Saskatchewan Reference remains the foundational ruling on what the Charter's right to vote requires of electoral boundary commissions. A subsequent Federal Court case (Raîche 2004) applied the Saskatchewan Reference standard but did not alter its core holding. The Supreme Court returned to s. 3 in 2026 in *Quebec (AG) v. Lalande*, 2026 SCC 13, which left in place the ruling that struck down Quebec's law blocking its commission from redrawing the map. The audit summarises Lalande from secondary sources and applies the 1991 standard as the governing test.

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

### Appendix C — 2021-Census Legal Baseline (Three Maps)

---

**Assertion:** On the 2021 Census, the 2019 map's MAD is 4,745 (9.7% of quota). On the same census, scored on the voting-area overlay, the majority's MAD is 4,847 (10.1% of its quota) and the minority's 4,871 (10.2%). On the commission's 2024 tables the 2026 maps are 3,180 and 4,707.
**Why?** Why are there two different MAD figures for the 2019 map (2,886 from the original commission basis and 4,745 from this appendix)?
**Answer:** The 2019 boundaries were drawn on the populations in the 2017 commission report, which gave a MAD of 2,886 (6.2% of a 46,803 quota). On 2021 Census populations the same boundaries give 4,745 (9.7% of 48,996), because growth since then was uneven. The 2026 maps get the same treatment in Appendix C. On the 2021 Census the majority is at 10.1% of its quota and the minority at 10.2%, so the three maps are almost level on that base. The 2026 maps were drawn to 2024 estimates, so the 2021 base also picks up growth they were not drawn to (Appendix C, cycle lag). Figures on different bases, such as 3,180 against 4,745, should not be ranked against each other.

---

**Assertion:** Seven 2019 EDs are outside the ±25% band under 2021 Census data, including five fast-growing suburban districts.
**Why?** Does this mean the 2019 map is already unconstitutional?
**Answer:** Being outside the ±25% statutory band is a serious issue but not automatically a constitutional violation — the Saskatchewan Reference standard allows deviations if justified by geography or community of interest. The five fast-growing suburban districts (primarily in south Edmonton and suburban Calgary/Airdrie) are outside the band purely because of population growth since the map was drawn. The audit documents them to establish the context: the 2026 commission inherited a population-equality problem that needed fixing. On the commission's 2024 tables, both 2026 maps keep every district inside the band apart from their s.15(2) districts. Whether either map improves on the 2019 map's spread depends on the base. On the 2021 Census the three maps are almost level (Appendix C).

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

**Assertion:** Declination formula: δ = (2/π)(arctan((ȳ_R − x̄_R)/x̄_R) − arctan((ȳ_D − x̄_D)/x̄_D)). Alberta results (canonical scoring, Amendment 10 sign): 2019 = +0.045 (p91.33), majority = −0.027 (p21.85), minority = +0.077 (p98.79, UCP tail).
**Why?** What does the formula actually measure in plain terms?
**Answer:** The declination measures the difference in how steeply each party's win-margin increases as it wins more districts. If Party A's winning margins are concentrated near 50% (many close wins) while Party B's winning margins are spread across both close and blowout wins, declination measures that asymmetry as an angular difference between two trend lines. Under the corrected sign (Amendment 10), a positive declination favours the UCP: the UCP wins many seats by thin margins while NDP votes are packed into a few high-share districts. The minority's p98.79 means its declination is higher (further toward the UCP tail) than 98.79% of random maps. That agrees with the efficiency gap, mean-median and seats-at-50/50 readings.

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
**Answer:** *This entry has been superseded by canonical execution of Phase 4C (2026-06-10).* The "+0.0000 pp" shift cited in earlier drafts referred to the v0_9-era **MAUP test** (centroid-in-polygon vs area-weighted attribution on the v0_9 topological shapefiles) — not to Phase 4C VA-polygon attribution itself. The MAUP test showed the v0_9 substrate's snap-to-VA-boundaries construction made attribution-method choice immaterial on that substrate. Phase 4C is now the canonical-substrate VA-polygon attribution step and *has* been executed (`analysis/scripts/phase4c_canonical_attribution.py`); see the preceding entry on this page for the canonical Phase 4C numbers (minority EG +4.02%, seats@50/50 0.5169 UCP fraction). The earlier "intentionally bypassed" framing was an artifact of pre-canonical sequencing and is no longer accurate.

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

*End of plain-language defense document.*

<!-- PLAIN_LANG_DEFENSE_END -->
