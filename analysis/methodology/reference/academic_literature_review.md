# Academic Literature Review and Gaps

**Purpose.** Identify academic work on electoral redistricting, partisan bias measurement, and Canadian boundary commissions that this audit has overlooked or failed to incorporate. Flag what should be read, what should be cited, and what should be implemented if feasible with FOSS and public data.

**Method.** Walk the main literature threads. For each, state what the audit cites today, what the audit should cite, and whether it changes methodology or just strengthens the write-up.

---

## 1. Partisan Bias Measurement

**What we cite today** —

- **Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015.** "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82(2): 831–900. — used for B2 (efficiency gap).
- **McDonald, Michael D., and Robin E. Best. 2015.** "Unfair Partisan Gerrymanders in Politics and Law: A Diagnostic Applied to Six Cases." *Election Law Journal* 14(4): 312–330. — used for B3 (mean-median).
- **Warrington, Gregory S. 2018.** "Quantifying Gerrymandering Using the Vote Distribution." *Election Law Journal* 17(1): 39–57. — used for B6 (declination) in v0.3.

**What we should cite** —

- **Grofman, Bernard. 1983.** "Measures of Bias and Proportionality in Seats-Votes Relationships." *Political Methodology* 9(3): 295–327. — foundational partisan-bias metric. Defines the symmetry standard the audit implicitly uses in B4 (seats at 50/50). Should be cited when discussing seat-vote curve asymmetry.
- **King, Gary, and Robert X. Browning. 1987.** "Democratic Representation and Partisan Bias in Congressional Elections." *American Political Science Review* 81(4): 1251–1273. — seat-vote asymmetry methodology. Operationalizes Grofman's bias measure. Directly relevant to B4.
- **Gelman, Andrew, and Gary King. 1994.** "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." *American Journal of Political Science* 38(2): 514–554. — the standard reference for swing/seats analysis in applied redistricting. B4's uniform-swing calculation is the simplest version of their approach; a Bayesian extension is in this paper.
- **Chen, Jowei, and Jonathan Rodden. 2013.** "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269. — **critical omission**. Their finding that urban-concentrated parties (like NDP) are systematically disadvantaged by neutrally-drawn maps because of voter geography is directly relevant to the audit's §B framing. *[Audit inference, not a source claim]* The −2.64% 2019 efficiency gap in Alberta is likely substantially natural packing, consistent with Chen & Rodden's geography thesis, rather than engineered. **Adding this citation and framing is the single most impactful literature fix for §B.**
- **Rodden, Jonathan. 2019.** *Why Cities Lose: The Deep Roots of the Urban-Rural Political Divide*. New York: Basic Books. — book-length expansion of the 2013 argument; now the more commonly cited source for the "natural suburban expansion" critique. The audit's Urban Hybridization control group (majority: 9 hybrid districts, minority: 25 under identical population constraints) is the empirical counter to this critique. Cross-ref: `private/draft_papers/novel_tests_lit_review.md` §2.2.
- **Chen, Jowei. 2017.** "The Impact of Political Geography on Wisconsin Redistricting: An Analysis of Wisconsin's Act 43 Assembly Districting Plan." *Election Law Journal* 16(4): 443–452. — extends Chen & Rodden to a single-state case similar in structure to our Alberta analysis.
- **DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021.** "Recombination: A Family of Markov Chains for Redistricting." *Harvard Data Science Review* 3(1). — foundational paper for GerryChain's ReCom algorithm (used in Phase 5). Should be cited at the point Phase 5 specifies GerryChain.
- **Campisi, Maria, Tom Ratliff, Joseph Somersille, and Ellen Veomett. 2022.** "Geography and Election Outcome Metric: An Introduction." *Election Law Journal* 21(3). — introduces the GEO metric (Geographic Election Outcomes). Cite separately from DeFord/Duchin/Solomon for any GEO claims.
- **Stephanopoulos, Nicholas O., and Eric M. McGhee. 2018.** "The Measure of a Metric: The Debate Over Quantifying Partisan Gerrymandering." *Stanford Law Review* 70(5): 1503–1568. — self-critique and response to EG criticisms. Relevant because our audit's RT1 finding (95% CI crosses zero for EG under modeling uncertainty) connects to this paper's discussion of EG stability.

### Critiques of declination and mean-median

- **Warrington, Gregory S. 2019.** "A Comparison of Partisan Gerrymandering Measures." *Election Law Journal* 18(3): 262–281. — author's own comparison showing declination and EG can diverge. Our v0.3 finding that declination disagrees with EG is *consistent with* Warrington's own analysis, not a methodology flaw. **Should cite in the §B2 Red-Team Update paragraph.**
- **Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020.** "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." *American Political Science Review* 114(1): 164–178. — comprehensive critique of single-metric approaches to partisan fairness. Supports separating fairness quantities from metrics and using multiple diagnostics; consistent with the "no single metric is dispositive" framing our v1.2 RT2 gate relies on.

### Methodological refinement worth considering

- **Herschlag, Gregory, et al. 2020.** "Quantifying Gerrymandering in North Carolina." *Statistics and Public Policy* 7(1): 30–38. — practical ensemble methodology. When Phase 5 unblocks, their specific ensemble configuration for state legislative maps is a good model.

---

## 2. Canadian Electoral Boundary Literature

**What we cite today** —

- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158. — **cited correctly** for the "effective representation" standard.
- Comparator cases: Quebec 1992, Ontario 1996, BC 2008. — cited but without academic sources backing the comparisons.

**What we should cite** —

- **Alberta.** *Electoral Boundaries Commission Act*, RSA 2000, c. E-3 (as consolidated 2024-12-05). — primary statutory authority for the population-deviation test. §15(1) sets the ±25% standard band; §15(2) permits up to four EDs to deviate as much as −50% below the provincial average if at least three of five specific criteria are present (area, distance from the Legislature, absence of large town, Indigenous reserve or Metis settlement, shared provincial border); §15(3) excludes the Municipality of Crowsnest Pass from the §15(2)(c) town-population test. Detailed per-ED audit in `analysis/methodology/s15_2_reaudit.md`. Constitutional backdrop for how far deviation can go before "effective representation" is impaired: *Reference re Saskatchewan* [1991] 2 SCR 158 (see §5).
- **Courtney, John C. 2001.** *Commissioned Ridings: Designing Canada's Electoral Districts*. Montreal and Kingston: McGill-Queen's University Press. — **the foundational Canadian work on boundary commissions.** Covers the independent-commission model, its development, and the range of practice across provinces, including how provinces implement deviation exceptions analogous to EBCA §15(2). Every claim in §D about Canadian norms should reference this with chapter/page pincites, not as a general authority. **Critical omission.**
- **Courtney, John C. 2004.** *Elections*. Vancouver: UBC Press. — broader Canadian elections context; Chapter 3 covers redistribution.
- **Pal, Michael. 2015.** "The Fractured Right to Vote: Democracy, Discretion, and Designing Electoral Districts." *McGill Law Journal* 61(2): 231–274. — verified on-topic source. Examines boundary-commission discretion, §3 Charter protection, and the limits of courts' role in electoral district design. Should be cited in the §D discussion of commission authority and the academic report legal note.
  > ℹ **Replaces** two prior S6-01/S6-02-flagged entries — Pal 2015 "The Fragmentation of Party Politics" (*UTLJ* 65) and Pal 2019 "The Charter and the Constitutionality of Electoral Boundaries" (*CJLJ* 32) — both of which failed DOI and title verification. See red-team notes 2026-04-23.
  > ℹ **Page range corrected 2026-05-07:** Erudit PDF confirms full range 231–274, not 231–287.
- **Sancton, Andrew. 2008.** *The Limits of Boundaries: Why City-Regions Cannot Be Self-Governing*. Montreal and Kingston: McGill-Queen's University Press. — relevant for the community-of-interest and municipal-boundary anchoring discussion in §C4 (Airdrie-Cochrane-Chestermere treatment and similar urban-fringe splits).
- **Carty, R. Kenneth. 2015.** *Big Tent Politics: The Liberal Party's Long Mastery of Canada's Public Life*. Vancouver: UBC Press. — Liberal Party organization and political-history context; for party-system background only. Chapter 5 is party-history content, not representation or electoral systems.
  > ⚠ **Year corrected 2026-05-07:** UBC Press confirms 2015, not 2017. Chapter 5 claim removed — do not use for boundary-commission or electoral-systems claims.

> **Still unresolved:** The report now cites Courtney but Canadian-lineage engagement remains thin until Courtney is used with chapter/page pincites rather than as a general authority, and until a confirmed Pal article on Canadian gerrymandering methods — if one exists beyond the verified 2015 entry — is located and incorporated.

### Alberta-specific

- **Archer, Keith. 1992.** "Voting Behaviour and Political Dominance in Alberta, 1971–1991." In *Government and Politics in Alberta*, edited by Allan Tupper and Roger Gibbins, 109–136. Edmonton: University of Alberta Press. — former Alberta Chief Electoral Officer; rare academic background on Alberta electoral geography.
- **Stewart, David K., and Keith Archer. 2000.** *Quasi-Democracy? Parties and Leadership Selection in Alberta*. Vancouver: UBC Press. — covers PC-era party and leadership selection in Alberta. Use for PC-era context only; do not extend to WRP/UCP evolution, which postdates this source.
- **Wiseman, Nelson. 2020.** *Partisan Odysseys: Canada's Political Parties*. Toronto: University of Toronto Press. — broad Canadian party-system and Conservative realignment context. Use only for general party-system background; the book integrates Alberta's history into broader themes rather than dedicating a specific chapter to the province, so do not cite it for specific Alberta political geography.
- **Bratt, Duane, Keith Brownsey, Richard Sutherland, and David Taras, eds. 2019.** *Orange Chinook: Politics in the New Alberta*. Calgary: University of Calgary Press. — academic compilation on NDP 2015 victory and UCP emergence. Directly relevant to the 2015 cross-election data interpretation. Reference present in report; substantive body engagement still thin.

### Indigenous representation

- **Ladner, Kiera L. 2003.** "Treaty Federalism: An Indigenous Vision of Canadian Federalisms." In *New Trends in Canadian Federalism*, edited by François Rocher and Miriam Smith, 167–196. Peterborough, ON: Broadview Press. — relevant to §C4 treatment of Tsuut'ina, Enoch Cree, Siksika Nations and the s.15(2) criterion (d) around Indigenous populations.
- **Dabin, Simon, Jean-François Daoust, and Martin Papillon. 2019.** "Indigenous Peoples and Affinity Voting in Canada." *Canadian Journal of Political Science* 52(1): 39–53. — replaces unverifiable Papillon 2021 placeholder. Covers Indigenous electoral participation in Canada; relevant to §C4 and A3(d) as background on Indigenous communities' engagement with electoral systems, though not directly a boundary-design source.
  > ℹ **Source substituted 2026-05-07:** original "Papillon 2021" citation could not be verified. Dabin/Daoust/Papillon 2019 is confirmed via Cambridge and is the closest verified source for Indigenous electoral participation in Canada.

---

## 3. Compactness and Geographic Analysis

**What we cite today** —

- Polsby-Popper (standard formula, no citation given).
- Reock (standard formula, no citation given).

**What we should cite** —

- **Polsby, Daniel D., and Robert D. Popper. 1991.** "The Third Criterion: Compactness as a Procedural Safeguard Against Partisan Gerrymandering." *Yale Law and Policy Review* 9(2): 301–353. — the paper PP comes from.
- **Reock, Ernest C. 1961.** "Measuring Compactness as a Requirement of Legislative Apportionment." *Midwest Journal of Political Science* 5(1): 70–74. — original Reock.
- **Young, H. Peyton. 1988.** "Measuring the Compactness of Legislative Districts." *Legislative Studies Quarterly* 13(1): 105–115. — compares multiple compactness measures; background for why we should report both PP and Reock.
- **Barnes, Richard, and Justin Solomon. 2021.** "Gerrymandering and Compactness: Implementation Flexibility and Abuse." *Political Analysis* 29(4): 448–466. — critical perspective on compactness as a standalone anti-gerrymander test. Relevant: our §C3 anomaly scan is essentially a compactness critique applied visually without numerical scores.

---

## 4. Vote-Distribution and Apportionment

**What we cite today** —

- The 70/30 urban/rural blending methodology was used in v0.3 as a proxy proxy but is now **formally deprecated**. The receipt of official Elections Alberta shapefiles allowed us to supersede it completely with Phase 4C measured attribution.

### What we should cite (or at least read)

- **Altman, Micah, and Michael P. McDonald. 2011.** "BARD: Better Automated Redistricting." *Journal of Statistical Software* 42(4): 1–28. — redistricting software and modeling methodology. Use for software/modeling context; do not use as formal support for the audit's 70/30 vote blend (which is an audit assumption, not a literature-derived method).
  > ℹ **Citation updated 2026-05-07:** replaces Altman & McDonald 2014 HICSS (public-participation GIS, pp. 2063–2072), which does not justify the 70/30 blend. BARD 2011 is the more directly relevant redistricting source.
- **Altman, Micah, and Michael P. McDonald. 2014.** "Public Participation GIS: The Case of Redistricting." In *Proceedings of the 47th Hawaii International Conference on System Sciences*, 2063–2072. Washington, DC: IEEE Computer Society. — public-data redistricting participation; note this is GIS/public-input context, not methodology for vote attribution.
  > ℹ **Pages corrected 2026-05-07:** 2063–2072 (not 2032–2041 as previously listed).
- **Fifield, Benjamin, Kosuke Imai, Jun Kawahara, and Christopher T. Kenny. 2020.** "The Essential Role of Empirical Validation in Legislative Redistricting Simulation." *Statistics and Public Policy* 7(1): 52–68. — methodology for simulating redistricting with empirical vote attribution. This literature is now strictly adhered to, as Phase 4C full execution was successfully run against the official Elections Alberta shapefiles (replacing the deprecated 70/30 blend).

---

## 5. Legal and Constitutional Framework

**What we cite today** —

- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

**What we should cite** —

- *Rucho v. Common Cause*, 588 U.S. 684 (2019). — **critical intellectual context (US).** The US Supreme Court ruled that federal courts have no role in adjudicating partisan gerrymandering claims; the majority explicitly declined to endorse the Efficiency Gap as a judicially manageable standard. Canadian courts operate under *Reference re Saskatchewan* not *Rucho*, but the ruling explains the contemporary analytical climate in which statistical partisan metrics are contested. *[Interpretive context, not source fact]* This is the analytical backdrop against which the audit's two-lane architecture — grounding strongest findings in structural measures (Lane 2) rather than statistical partisan-effect metrics alone (Lane 1) — is positioned. Cross-ref: `private/draft_papers/novel_tests_lit_review.md` §3.1.
- *Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912. — §3 Charter analysis; supports meaningful participation under s.3. Use only for broad §3 voting-rights context; does not directly address boundary-commission design.
- *Frank v. Canada (Attorney General)*, [2019] 1 SCR 3. — §3 Charter case on voting rights of incarcerated persons. Use only for broad §3 scope; it is not a boundary case and does not directly reinforce the effective-representation standard in the redistricting context.
  > ⚠ **Codex finding 2026-05-07:** do not use Frank to support "effective representation" boundary-commission claims — it addresses §3 voting entitlement, not district design standards.
- *Haig v. Canada*, [1993] 2 SCR 995. — §3 voting rights and limits of s.3; cited in Reference re Saskatchewan commentary. Use only for §3 scope context; no direct boundary relevance.
- > ℹ **Unverified Pal methodology entry removed:** a prior entry attributed "Gerrymandering in Canada: A Comparative Analysis" to Pal (2021) in *CJPS* 54 based on recalled knowledge. This could not be confirmed and was likely a hallucination. The verified 2015 Pal source ("The Fractured Right to Vote") in §2 provides sufficient scholarly context for boundary commission discretion; no further Canadian methodology paper from Pal is required.

---

## 6. What Changes in the Audit If We Incorporate This?

### Methodology-affecting changes

**6.1 Chen & Rodden natural-packing framing.** The 2019 map's −2.64% EG should be framed as "partly a natural artifact of NDP urban concentration (per Chen & Rodden 2013)" rather than "a slight structural UCP advantage." This strengthens the finding in a different way: if the 2019 EG is mostly natural, then the minority map's further shift *beyond* 2019 is more clearly engineered rather than natural.

**6.2 Katz, King & Rosenblatt on ensemble metrics.** Our v1.2 RT2 gate (cross-metric agreement) is justified in the abstract ("hostile experts want multiple metrics") but not cited. Citing Katz et al. 2020 makes the RT2 gate a literature-standard practice rather than a judgment call.

**6.3 Warrington's own divergence finding.** Our declination-disagrees-with-EG result is consistent with Warrington 2019's explicit comparison. Citing it tells readers "this divergence is expected, not a methodology bug."

### Non-methodology-affecting changes (just better-grounded framing)

**6.4 Courtney 2001 for §D.** Every comparator-case claim needs Courtney's backing with chapter/page pincites, not as a general citation.

**6.5 Pal 2015 (verified) for the legal framing note.** The academic report's legal note should cite Pal's "Fractured Right to Vote" (*McGill LJ* 61(2): 231–274) for the boundary-commission discretion framing. The two prior unverifiable Pal entries have been removed.

**6.6 Ladner / Papillon & Belleau for §A3(d) Indigenous criteria.** The s.15(2)(d) criterion around "significant Indigenous population" is under-cited in our A3 analysis. Indigenous-representation literature would strengthen the discussion.

### Alberta-specific framing

**6.7 Orange Chinook (Bratt et al. 2019) for 2015/2019 transition.** Our 2015 cross-election analysis treats the NDP wave and UCP post-merger shift as context. Orange Chinook provides academic interpretation. Citing it grounds the rural baseline variation (2015: 35%, 2019: 26%, 2023: 33%) in Alberta-specific political science.

---

## 7. Priority Ordering for Incorporation

| Citation | Where it goes | Effect | Priority | Status |
| --- | --- | --- | --- | --- |
| Chen & Rodden 2013 | §B framing, public & academic | Natural-packing vs engineered framing | **High** | Partially incorporated — §B framing note added; §9 cites it |
| Rodden 2019 *Why Cities Lose* | §B / Urban Hybridization counter | Book-length natural-expansion critique | **High** | Added §1; cross-ref to draft paper lit review |
| Rucho v. Common Cause 2019 | §5 legal; Lane 2 rationale | Explains why structural tests exist | **High** | Added §5 |
| Courtney 2001 | §D comparator discussion | Grounds Canadian-practice claims | **High** | Incorporated in report |
| Pal 2015 "Fractured Right to Vote" | legal framing note, §D | Boundary-commission discretion and electoral-district design | **High** | Incorporated in report |
| Nosek et al. 2018 | §10 pre-registration | Pre-reg as standard practice | **High** | Added §10 |
| Warrington 2019 | §B2 Red-Team Update | Declination-EG divergence is expected | Medium | Incorporated in report |
| Katz, King & Rosenblatt 2020 | RT2 justification | Literature-grounded ensemble-metric practice | Medium | Incorporated in report |
| Gelman & King 1994 | §B4 methodology | Standard reference for swing/seats | Medium | Incorporated in report |
| DeFord, Duchin, Solomon 2021 | Stage 5 methodology | GerryChain ReCom reference (not GEO) | Medium | Incorporated in report |
| Campisi, Ratliff, Somersille, Veomett 2022 | Stage 5 (if GEO used) | GEO metric introduction — cite separately from ReCom | Low | Not yet incorporated |
| Polsby & Popper 1991 | §8.3 formula | Foundational citation | Low | Incorporated in report |
| Reock 1961 | §8.4 formula | Foundational citation | Low | Incorporated in report |
| Bratt et al. 2019 | 2015 cross-election context | Alberta-specific political science | Low | Reference present; body engagement still thin |
| Sancton 2008 | §C4 community-of-interest | Municipal-boundary anchoring | Low | Reference present; body engagement still thin |
| Dabin, Daoust, Papillon 2019 | §A3(d) | Indigenous electoral participation (replaces unverified Papillon 2021) | Low | Citation updated 2026-05-07 |

---

## 8. What Would Update Methodology

Of all the above, **Chen & Rodden 2013 is the one that potentially changes a finding rather than just strengthens framing.**

If we accept Chen & Rodden's natural-packing thesis, then:

- The 2019 baseline EG of −2.64% is largely *expected* given Alberta's voter geography, not evidence of engineering.
- The majority 2026's EG of −0.85% actually moves *toward zero*, which if Chen & Rodden's natural-packing is the baseline, means the majority is partially *correcting* for natural packing.
- The minority 2026's EG of −1.36% is less correction than the majority, but still less than the 2019 baseline.
- Under this framing, neither 2026 map is engineered *against* natural packing — both partially correct it, with the majority correcting more.

**This is a materially different framing from "minority is more UCP-favorable than majority."** Both are true, but the Chen & Rodden framing puts the difference in a natural-geographic context that weakens the "intentional partisan choice" implication.

**Whether to adopt this framing is a judgment.** Arguments for: academically defensible, cites widely-accepted literature. Arguments against: Chen & Rodden's thesis doesn't explain why the minority has 12.2% Calgary zone gap and the majority has 0.4% — that part of the asymmetry is not naturally explained by urban NDP concentration. The structural findings (population equality, community splits, visible anomalies) are engineered choices by definition.

A defensible synthesis: *cite Chen & Rodden for the §B framing ("partisan-bias metrics in Alberta are confounded by natural NDP urban concentration per Chen & Rodden 2013"), but note that the structural findings of §A/C/D are not affected by the natural-packing argument because they measure geographic and procedural choices, not vote distribution. The claim that Alberta's 2019 EG is "substantially natural packing" is an audit inference drawn from Chen & Rodden's general finding, not a direct conclusion of their paper, and should be labelled as such in the report.*

---

## 9. Neighbour-Drain and Pack-Crack Adjacency (Novel Metric)

### Prior literature on packing and cracking

- **Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015.** — EG explicitly models packed and cracked seats as components of wasted votes. Packing and cracking as a *joint* strategy are named and measured at the whole-map level.
- **Chen, Jowei, and Jonathan Rodden. 2013.** — natural packing of urban parties creates an EG disadvantage without any intent; this is the most important context for interpreting the drain metric.
- **McGann, Anthony J., Charles Anthony Smith, Michael Latner, and Alex Keena. 2016.** *Gerrymandering in America: The House of Representatives, the Supreme Court, and the Future of Popular Sovereignty*. Cambridge: Cambridge University Press. — book-length treatment of EG and partisan symmetry; includes case studies in which packing + cracking are described qualitatively as spatially correlated patterns.

### Prior art scope

I have not found an established named measure for the **local packed-to-cracked adjacency coupling** — where the same losing-party votes that overflow a packed ED sit directly adjacent to a narrow-margin cracked ED of the same party. The gerrymandering literature discusses packing and cracking as co-occurring whole-map strategies but not as a measurable spatial adjacency signature at the ED-pair level. This claim is based on the targeted search conducted for this audit; it should be verified against recent redistricting literature before submission and is presented as a proposed operationalization pending fuller prior-art review.

Informal terminology in advocacy and journalism — "pizza-slice," "hub-and-spoke," "tentacle" districts — describes the visual geometry of specific cracked EDs but does not operationalise the pack-crack **coupling** between adjacent EDs.

**Naming note for publication:** The audit's Urban Hybridization count maps directly onto the "hub-and-spoke" / "pizza-slice" tradition and must cite that prior art explicitly. The Neighbour-Drain metric is the ED-pair-level operationalisation of the adjacency coupling — a distinct and more precise measure than the whole-map count. Both must be presented as building on, not replacing, the informal prior terminology. Cross-ref: `private/draft_papers/novel_tests_lit_review.md` §6.

The closest methodological analogs are spatial autocorrelation approaches (Moran's I applied to vote shares), but global Moran's I does not isolate directional packed→cracked adjacency pairs. However, the Neighbour-Drain metric is essentially a targeted, bivariate variant of Local Spatial Autocorrelation (Local Moran's I / LISA) applied across the district contiguity graph. It uses contiguity analysis to map adjacencies and creates a custom asymmetric High-Low spatial outlier detector that specifically flags "packed" areas directly neighboring "cracked" areas.

### Audit's contribution

**"Neighbour-Drain"** is coined in this audit (AsPredicted #289,451; 2026-05-06) to name: a packed ED (losing-party surplus ≥ 0.15) directly adjacent to a cracked ED (winning margin ≤ 0.05) with the same losing party in both — a *coupled chain signal*. The continuous intensity version:

  intensity(X, Y) = max(0, s_X − 0.15) × max(0, 0.05 − m_Y)

and the label-shuffle null distribution are new analytical contributions. Results are reported in `findings/neighbour_drain_analysis.md` and the academic report.

### Literature to cite when publishing

- Chen & Rodden (2013) — natural-packing baseline that the drain metric must be adjusted against
- Stephanopoulos & McGhee (2015) — whole-map packing/cracking context
- State: "based on a targeted search of the redistricting literature, the specific adjacency coupling we call Neighbour-Drain has no established named measure; this audit introduces the term as a proposed operationalization pending fuller prior-art review"

---

## 9b. Swing-Zone Allocation Test (SZAT) — Novel Decomposition

### Prior literature

SZAT decomposes the between-map efficiency-gap difference into the specific boundary choices (swing zones) that drive it. No established test performs this decomposition directly; the closest prior work is:

- **Stephanopoulos & McGhee (2015)** — EG at the whole-map level; does not decompose to individual boundary decisions.
- **Chen & Rodden (2013)** — decomposes EG into geography vs. drawing at the map level using an ensemble median; does not decompose to individual VA-boundary choices.
- **Altman & McDonald (2011).** "BARD: Better Automated Redistricting." *Journal of Statistical Software* 42(4): 1–28. — simulation-based comparison of map alternatives; does not identify which specific boundaries drive partisan differences.

SZAT asks a different question from all of these: not "is the map anomalous compared to neutral draws?" but "which of the specific boundary decisions that differ between two real proposed maps are responsible for the between-map partisan-efficiency gap?"

### SZAT contribution

**"Swing-Zone Allocation Test"** (SZAT) is introduced in this audit ([AsPredicted #289,469](https://aspredicted.org/9zr792.pdf), filed 2026-05-07, made public 2026-05-07). A swing zone is a Voting Area whose centroid falls in a different Electoral Division under Map A than Map B. SZAT score = EG(A) − EG(B) summed over swing zones only, tested against a permutation null in which each swing zone is randomly assigned to either map's configuration. The test is generalizable to any pair of maps covering the same geography.

Applied to the 2026 Alberta commission proposals against canonical Elections Alberta shapefiles: SZAT score = +0.039211 (p = 0.0024, two-tailed bootstrap, full-recompute, N = 10,000, seed 23687475). The minority map's boundary choices increase NDP vote waste by 3.9 percentage points relative to the majority map, with the dominant contribution from Rest of Alberta (+0.015) and Edmonton (+0.008). Full methodology: `analysis/methodology/szat_proposal.md`. Results: `findings/szat_summary.json`.
  > ℹ **p-value history:** original additive-delta approximation gave p = 0.000; 500-perm full-recompute check gave p ~ 0.012; definitive 10k full-recompute run (Election-Day-only substrate) gives p = 0.0044; re-run with full advance-vote substrate (2026-05-10) gives p = 0.0024 (swing zone count 2108 → 2110). H0 rejected at α = 0.05 throughout.

**Generalisation note (documented for future work):** The majority-vs-minority framing is natural for this audit, but the same test applies to any proposed map against the current enacted baseline. Comparing proposed-vs-2019 would test whether a new map's specific boundary changes improve or worsen efficiency relative to the prior plan — potentially more useful to courts and commissions than a between-proposals comparison.

### SZAT citations for publication

- Stephanopoulos & McGhee (2015) — EG framework the decomposition lives on
- Chen & Rodden (2013) — geography-vs-drawing decomposition (SZAT is the boundary-choice-level complement)
- State: "the decomposition of between-map EG differences to individual Voting Area boundary choices, and its permutation test, are novel to this audit"

---

## 10. Pre-Registration and Open Science in Electoral Forensics

### Motivation

Electoral forensics analyses are at high risk of inadvertent p-hacking: the analyst often has partial knowledge of vote distributions before choosing metrics, and there is a natural tendency to foreground metrics that produce larger effects. Pre-registration addresses this by creating a timestamped record of hypotheses, metrics, and inference criteria before outcomes are computed.

### Pre-registration platforms and methodology

- **Nosek, Brian A., et al. 2018.** "The Preregistration Revolution." *Proceedings of the National Academy of Sciences* 115(11): 2600–2606. — canonical paper establishing pre-registration as a standard scientific practice. Directly applicable to electoral forensics; the audit's AsPredicted registrations follow the framework described here.
- **Uhlmann, Eric Luis, et al. 2019.** "Scientific Utopia III: Crowdsourcing Science." *Perspectives on Psychological Science* 14(5): 711–733. — crowdsourcing and transparency in science; supports open-science framing but does not specifically validate the AsPredicted platform.
  > ℹ **Metadata corrected 2026-05-07:** title, issue, and pages fixed (was 14(3):375–395; "Crowdsourcing Science" subtitle added). Remove AsPredicted-specific claims not directly sourced from this paper.
- **van 't Veer, Anna Elisabeth, and Roger Giner-Sorolla. 2016.** "Pre-registration in social psychology — A discussion and suggested template." *Journal of Experimental Social Psychology* 67: 2–12. — proposes a pre-registration template for social psychology; general pre-reg methodology context.
  > ℹ **Metadata corrected 2026-05-07:** title and page range fixed (was 2–9; "designed the AsPredicted template" claim removed as unverified from this source).
- **Center for Open Science. n.d.** "Open Science Framework." <https://osf.io>. — the audit's OSF registrations are stored here as a pre-analysis record pending public release. Registration URLs will be disclosed on publication; they are not currently public.
  > ℹ **Status corrected 2026-05-07:** registrations are private/pending release; do not describe as "parallel public record" until released.

### Cryptographic randomness for reproducibility

**Two distinct drand beacon rounds are in use:**

- **Round 5500000** (Cloudflare League of Entropy) is the canonical seed for all Phase 4/5 simulation analyses to date: DPG v11 validation and Neighbour-Drain label-shuffle null infrastructure. The `drand_seed.py` module derives per-analysis salted seeds from this root.
- **Round 6062459** has been pre-committed as the seed for future November forensic testing (Lunty 91-seat analysis). It is not yet active; it exists as a verifiable pre-commitment only.

These are separate scopes. All published simulation results to date use round 5500000. When publishing, note: *"Simulation seeds are derived from public randomness beacon drand (Cloudflare League of Entropy, round 5500000). Salt-derived seeds for each analysis chain are committed to version control prior to simulation runs, creating a pre-analysis timestamp record that precludes retroactive seed selection."*

The closest analog is:

- **Stark, Philip B. 2010.** "Super-Simple Simultaneous Single-Ballot Risk-Limiting Audits." In *Proceedings of the 2010 Electronic Voting Technology Workshop/Workshop on Trustworthy Elections*, 1–11. Berkeley: USENIX. — same principle (publicly verifiable randomness for audit integrity), different application.

### Pre-registration status for this audit (as of 2026-05-06)

| Registration | AsPredicted | OSF | Status |
| --- | --- | --- | --- |
| DPG v11 Validation | [#289,449](https://aspredicted.org/tb9bq3.pdf) | [w2s8k](https://osf.io/w2s8k/) | Complete; results in report_academic.md |
| Neighbour-Drain null | [#289,451](https://aspredicted.org/ig73yy.pdf) | [r3zm7](https://osf.io/r3zm7/) | Complete; minority within null; majority anomalously clean |
| ~~89-seat comparison~~ | [~~#289,452~~](https://aspredicted.org/u5kr84.pdf) | — | Superseded; test unrunnable; noted in writeup |
| Lunty 91-seat scorecard | [#289,455](https://aspredicted.org/ib9w4k.pdf) | [qsgy8](https://osf.io/qsgy8/) | Registered; awaiting map publication |

Git pre-analysis commit: `d2aea42` (seeds and analysis scripts committed before any simulation runs).

---

## 11. What This Literature Review Does Not Cover

- **Specific individual boundary commissioners' academic backgrounds.** Relevant if any commissioner has prior academic writing on redistricting, but tangential to this audit.
- **US redistricting litigation history in depth.** US-case-law references (e.g., *Gill v. Whitford*, *Rucho v. Common Cause*) are included strictly as analytical context for the partisan-symmetry and efficiency-gap validity debates. Canadian law and constitutional jurisprudence solely govern the Alberta boundary process.
- **Election-administration literature.** Peripheral to boundary-drawing questions.
- **Voting-rights literature as a distinct sub-field.** Important but outside scope.

---
