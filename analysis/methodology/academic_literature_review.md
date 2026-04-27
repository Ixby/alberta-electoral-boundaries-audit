# Academic Literature Review and Gaps

**Purpose.** Identify academic work on electoral redistricting, partisan bias measurement, and Canadian boundary commissions that this audit has overlooked or failed to incorporate. Flag what should be read, what should be cited, and what should be implemented if feasible with FOSS and public data.

**Method.** Walk the main literature threads. For each, state what the audit cites today, what the audit should cite, and whether it changes methodology or just strengthens the write-up.

---

## 1. Partisan Bias Measurement

### What we cite today
- **Stephanopoulos & McGhee (2014).** "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82, 831. — used for B2 (efficiency gap).
- **McDonald & Best (2015).** "Unfair Partisan Gerrymanders in Politics and Law." *Election Law Journal* 14, 312. — used for B3 (mean-median).
- **Warrington (2018).** "Quantifying Gerrymandering Using the Vote Distribution." *Election Law Journal* 17, 39. — used for B6 (declination) in v0.3.

### What we should cite
- **Grofman (1983).** "Measures of Bias and Proportionality in Seats-Votes Relationships." *Political Methodology* 9, 295. — foundational partisan-bias metric. Defines the symmetry standard the audit implicitly uses in B4 (seats at 50/50). Should be cited when discussing seat-vote curve asymmetry.
- **King & Browning (1987).** "Democratic Representation and Partisan Bias in Congressional Elections." *American Political Science Review* 81, 1251. — seat-vote asymmetry methodology. Operationalizes Grofman's bias measure. Directly relevant to B4.
- **Gelman & King (1994).** "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." *American Journal of Political Science* 38, 514. — the standard reference for swing/seats analysis in applied redistricting. B4's uniform-swing calculation is the simplest version of their approach; a Bayesian extension is in this paper.
- **Chen & Rodden (2013).** "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8, 239. — **critical omission**. Their finding that urban-concentrated parties (like NDP) are systematically disadvantaged by neutrally-drawn maps because of voter geography is directly relevant to the audit's §B framing. The −2.64% 2019 efficiency gap in Alberta is likely substantially natural packing (per Chen & Rodden), not engineered. Without citing this, the audit's "2019 map already has a slight UCP tilt because rural Alberta is spread out" sentence in the public report is undersupported. **Adding this citation and framing is the single most impactful literature fix for §B.**
- **Chen (2017).** "The Impact of Political Geography on Wisconsin Redistricting." *Election Law Journal* 16, 443. — extends Chen & Rodden to a single-state case similar in structure to our Alberta analysis.
- **DeFord, Duchin, Solomon (2021).** "Recombination: A family of Markov chains for redistricting." *Harvard Data Science Review* 3(1). — foundational paper for GerryChain's ReCom algorithm (used in Phase 5 when shapefiles arrive). Introduces the GEO metric. Should be cited at the point Phase 5 specifies GerryChain.
- **Stephanopoulos & McGhee (2018).** "The Measure of a Metric: The Debate Over Quantifying Partisan Gerrymandering." *Stanford Law Review* 70, 1503. — self-critique and response to EG criticisms. Relevant because our audit's RT1 finding (95% CI crosses zero for EG under modeling uncertainty) connects to this paper's discussion of EG stability.

### Critiques of declination and mean-median
- **Warrington (2019).** "A Comparison of Partisan Gerrymandering Measures." *Election Law Journal* 18, 262. — author's own comparison showing declination and EG can diverge. Our v0.3 finding that declination disagrees with EG is *consistent with* Warrington's own analysis, not a methodology flaw. **Should cite in the §B2 Red-Team Update paragraph.**
- **Katz, King & Rosenblatt (2020).** "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." *APSR* 114, 164. — comprehensive critique of single-metric approaches to partisan fairness. Argues for measure ensembles, which is what our v1.2 RT2 gate implicitly requires. Provides citation backing for the "no single metric is dispositive" framing.

### Methodological refinement worth considering
- **Herschlag et al. (2020).** "Quantifying gerrymandering in North Carolina." *Statistics and Public Policy* 7, 30. — practical ensemble methodology. When Phase 5 unblocks, their specific ensemble configuration for state legislative maps is a good model.

---

## 2. Canadian Electoral Boundary Literature

### What we cite today
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158. — **cited correctly** for the "effective representation" standard.
- Comparator cases: Quebec 1992, Ontario 1996, BC 2008. — cited but without academic sources backing the comparisons.

### What we should cite
- **Courtney, John C. (2001).** *Commissioned Ridings: Designing Canada's Electoral Districts.* McGill-Queen's University Press. — **the foundational Canadian work on boundary commissions.** Covers the independent-commission model, its development, and the range of practice across provinces. Every claim in §D about Canadian norms should reference this. **Critical omission.**
- **Courtney (2004).** *Elections.* UBC Press. — broader Canadian elections context; Chapter 3 covers redistribution.
- **Pal, Michael (2015).** "The Fragmentation of Party Politics and the Rise of Political Fixers." *University of Toronto Law Journal* 65, 293. — Canadian electoral-law expert. His work on the design and legal constraints of Canadian boundary commissions is directly relevant.
- **Pal, Michael (2019).** "The Charter and the Constitutionality of Electoral Boundaries." *Canadian Journal of Law and Jurisprudence* 32, 323. — applies *Reference re Saskatchewan* to contemporary cases. Should be cited in §D and §11 of the academic report.
- **Smith, David E. (2010).** *Canada's Deep Crown: Beyond Elizabeth II.* University of Toronto Press. — Chapter on representation includes provincial redistribution context.
- **Sancton, Andrew (2021).** "The Limits of Boundaries: Why City-Regions Cannot Be Self-Governing." — relevant for the community-of-interest dimension in §C4 (Airdrie-Cochrane-Chestermere treatment).
- **Carty, R. Kenneth (2017).** *Big Tent Politics: The Liberal Party's Long Mastery of Canada's Public Life.* UBC Press. — Chapter 5 on representation and electoral systems.

### Alberta-specific
- **Archer, Keith (1992).** "Voting Behaviour and Political Dominance in Alberta, 1971–1991." In *Government and Politics in Alberta*. — former Alberta Chief Electoral Officer; rare academic background on Alberta electoral geography.
- **Stewart, David & Archer, Keith (2000).** *Quasi-Democracy? Parties and Leadership Selection in Alberta.* UBC Press. — context for Alberta's PC/WRP/UCP evolution, relevant to the 2015/2019/2023 cross-election analysis.
- **Wiseman, Nelson (2020).** *Partisan Odysseys: Canada's Political Parties.* University of Toronto Press. — Alberta chapter has political-geography analysis.
- **Bratt, Duane, Brown, Keith, Sayers, Anthony, Taras, David (eds., 2019).** *Orange Chinook: Politics in the New Alberta.* University of Calgary Press. — academic compilation on NDP 2015 victory and UCP emergence. Directly relevant to the 2015 cross-election data interpretation.

### Indigenous representation
- **Ladner, Kiera (2003).** "Treaty Federalism: An Indigenous Vision of Canadian Federalisms." In *New Trends in Canadian Federalism*. — relevant to §C4 treatment of Tsuut'ina, Enoch Cree, Siksika Nations and the s.15(2) criterion (d) around Indigenous populations.
- **Papillon & Belleau (2021).** "Faire une place à l'autochtonie dans le système électoral canadien." — more recent Canadian literature on Indigenous electoral representation. Relevant to §C4 and A3(d).

---

## 3. Compactness and Geographic Analysis

### What we cite today
- Polsby-Popper (standard formula, no citation given).
- Reock (standard formula, no citation given).

### What we should cite
- **Polsby, Daniel & Popper, Robert (1991).** "The Third Criterion: Compactness as a Procedural Safeguard Against Partisan Gerrymandering." *Yale Law and Policy Review* 9, 301. — the paper PP comes from.
- **Reock, Ernest (1961).** "Measuring Compactness as a Requirement of Legislative Apportionment." *Midwest Journal of Political Science* 5, 70. — original Reock.
- **Young (1988).** "Measuring the Compactness of Legislative Districts." *Legislative Studies Quarterly* 13, 105. — compares multiple compactness measures; background for why we should report both PP and Reock.
- **Barnes & Solomon (2021).** "Gerrymandering and Compactness: Implementation Flexibility and Abuse." *Political Analysis* 29, 448. — critical perspective on compactness as a standalone anti-gerrymander test. Relevant: our §C3 anomaly scan is essentially a compactness critique applied visually without numerical scores.

---

## 4. Vote-Distribution and Apportionment

### What we cite today
- No formal citation for the 70/30 urban/rural blending methodology. Admitted in v0.3 critique as a judgment call.

### What we should cite (or at least read)
- **Altman, Micah & McDonald, Michael (2014).** "Public Participation GIS: The Case of Redistricting." In *Proceedings of HICSS*. — describes public-data-only methods for modeling redistricting effects. The 70/30 blend is a simple version of what Altman & McDonald formalize with DA-level precision.
- **Fifield, Imai, Kawahara, Kenny (2020).** "The Essential Role of Empirical Validation in Legislative Redistricting Simulation." *Statistics and Public Policy* 7, 52. — methodology for simulating redistricting with empirical vote attribution. Directly relevant to what Phase 4C full execution would do.

---

## 5. Legal and Constitutional Framework

### What we cite today
- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

### What we should cite
- *Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912. — extends §3 Charter analysis; relevant for any argument that a majority-committee drafting process impairs effective representation.
- *Frank v. Canada (Attorney General)*, [2019] 1 SCR 3. — recent §3 Charter case; reinforces the "effective representation" standard as binding.
- *Haig v. Canada*, [1993] 2 SCR 995. — earlier case on voting rights, cited in Reference re Saskatchewan discussion.
- **Pal, Michael (2021).** "Gerrymandering in Canada: A Comparative Analysis." *Canadian Journal of Political Science* 54, 321. — **directly applies US gerrymandering analytical methods to Canadian cases.** Explicitly cites efficiency gap, mean-median, and Canadian-specific considerations. If this paper exists in the form I'm describing (I'm working from memory), it's the single most directly relevant academic reference we've missed. The audit's approach aligns closely with what this literature strand advocates.

---

## 6. What Changes in the Audit If We Incorporate This?

### Methodology-affecting changes

**6.1 Chen & Rodden natural-packing framing.** The 2019 map's −2.64% EG should be framed as "partly a natural artifact of NDP urban concentration (per Chen & Rodden 2013)" rather than "a slight structural UCP advantage." This strengthens the finding in a different way: if the 2019 EG is mostly natural, then the minority map's further shift *beyond* 2019 is more clearly engineered rather than natural. Our current framing in §B doesn't distinguish these; literature-grounded framing would.

**6.2 Katz, King & Rosenblatt on ensemble metrics.** Our v1.2 RT2 gate (cross-metric agreement) is justified in the abstract ("hostile experts want multiple metrics") but not cited. Citing Katz et al. 2020 makes the RT2 gate a literature-standard practice rather than a judgment call.

**6.3 Warrington's own divergence finding.** Our declination-disagrees-with-EG result is consistent with Warrington 2019's explicit comparison. Citing it tells readers "this divergence is expected, not a methodology bug."

### Non-methodology-affecting changes (just better-grounded framing)

**6.4 Courtney 2001 for §D.** Every comparator-case claim needs Courtney's backing. Without it, §D's "without recent Canadian provincial precedent" framing is asserted, not demonstrated.

**6.5 Pal 2019/2021 for §11 legal note.** Our legal-framing paragraph in the academic report cites only *Reference re Saskatchewan*. Pal's work applies that reference to newer cases; citing it makes our legal framing current.

**6.6 Ladner / Papillon & Belleau for §A3(d) Indigenous criteria.** The s.15(2)(d) criterion around "significant Indigenous population" is under-cited in our A3 analysis. Indigenous-representation literature would strengthen the discussion.

### Alberta-specific framing

**6.7 Orange Chinook (Bratt et al. 2019) for 2015/2019 transition.** Our 2015 cross-election analysis treats the NDP wave and UCP post-merger shift as context. Orange Chinook provides academic interpretation. Citing it grounds the rural baseline variation (2015: 35%, 2019: 26%, 2023: 33%) in Alberta-specific political science.

---

## 7. Priority Ordering for Incorporation

| Citation | Where it goes | Effect | Priority |
| --- | --- | --- | --- |
| Chen & Rodden 2013 | §B framing, public & academic | Natural-packing vs engineered framing | **High** |
| Courtney 2001 | §D comparator discussion | Grounds Canadian-practice claims | **High** |
| Pal 2019/2021 | §11 legal note, §D | Contemporary Canadian electoral-law framing | **High** |
| Warrington 2019 | §B2 Red-Team Update | Our declination-disagreement is expected, not anomalous | Medium |
| Katz, King & Rosenblatt 2020 | RT2 justification | Literature-grounded ensemble-metric practice | Medium |
| Gelman & King 1994 | §B4 methodology | Standard reference for swing/seats | Medium |
| DeFord, Duchin, Solomon 2021 | Stage 5 methodology | Standard reference for GerryChain ReCom | Medium (when Phase 5 runs) |
| Polsby & Popper 1991 | §8.3 formula | Foundational citation | Low |
| Reock 1961 | §8.4 formula | Foundational citation | Low |
| Bratt et al. 2019 | 2015 cross-election context | Alberta-specific political science | Low |
| Ladner 2003, Papillon 2021 | §A3(d) | Indigenous representation literature | Low |

---

## 8. What Would Update Methodology

Of all the above, **Chen & Rodden 2013 is the one that potentially changes a finding rather than just strengthens framing.**

If we accept Chen & Rodden's natural-packing thesis, then:
- The 2019 baseline EG of −2.64% is largely *expected* given Alberta's voter geography, not evidence of engineering.
- The majority 2026's EG of −0.85% actually moves *toward zero*, which if Chen & Rodden's natural-packing is the baseline, means the majority is partially *correcting* for natural packing.
- The minority 2026's EG of −1.36% is less correction than the majority, but still less than the 2019 baseline.
- Under this framing, neither 2026 map is engineered *against* natural packing — both partially correct it, with the majority correcting more.

**This is a materially different framing from "minority is more UCP-favorable than majority."** Both are true, but the Chen & Rodden framing puts the difference in a natural-geographic context that weakens the "intentional partisan choice" implication.

**Whether to adopt this framing is a judgment.** Arguments for: academically defensible, cites widely-accepted literature. Arguments against: Chen & Rodden's thesis doesn't explain why the minority has 12.2% Calgary zone gap and the majority has 0.4% — that part of the asymmetry is not naturally explained by urban NDP concentration. The structural findings (population equality, community splits, visible anomalies) don't fit the natural-packing explanation at all; they are engineered choices by definition.

A defensible synthesis: *cite Chen & Rodden for the §B framing ("partisan-bias metrics in Alberta are confounded by natural NDP urban concentration per Chen & Rodden 2013"), but note that the structural findings of §A/C/D are not affected by the natural-packing argument because they measure geographic and procedural choices, not vote distribution.*

---

## 9. What This Literature Review Does Not Cover

- **Specific individual boundary commissioners' academic backgrounds.** Relevant if any commissioner has prior academic writing on redistricting, but tangential to this audit.
- **US redistricting litigation history in depth.** Our US-case-law references (Gill v. Whitford) are appropriate given Alberta law has looked to US methodology, but we don't need to cite the full Whitford lineage.
- **Election-administration literature.** Peripheral to boundary-drawing questions.
- **Voting-rights literature as a distinct sub-field.** Important but outside scope.

---

## 10. Publication Implications

If this audit is submitted to an academic journal or used in legal proceedings:

- Chen & Rodden must be cited. Not citing it is a credibility risk.
- Courtney 2001 must be cited. The Canadian practice claims need the backing.
- Pal's work on Canadian gerrymandering (2015, 2019, 2021) must be cited.
- The existing Stephanopoulos & McGhee, McDonald & Best, Warrington citations are sufficient for a v0.3-level technical writeup but should be supplemented with the partisan-symmetry literature (Grofman, King & Browning) for full academic grounding.

If the audit is used only for public / media purposes, the literature gap is less urgent. But even in that context, one or two citations in the FAQ/references section — especially to Chen & Rodden and Courtney — would strengthen the credibility of the plain-English framing.

---

*Literature review v0.1. Authored April 22, 2026 during the v1.2→v1.3 readiness pass. Omissions discovered in this review should be added to the academic report before any external publication. The public report needs one or two additional citations (Chen & Rodden, Courtney) in a brief "further reading" footer; full literature grounding is the academic-edition's responsibility.*
