# Academic Literature Review and Gaps

**Purpose.** Identify academic work on electoral redistricting, partisan bias measurement, and Canadian boundary commissions that this audit has overlooked or failed to incorporate. Flag what should be read, what should be cited, and what should be implemented if feasible with FOSS and public data.

**Method.** Walk the main literature threads. For each, state what the audit cites today, what the audit should cite, and whether it changes methodology or just strengthens the write-up.

---

## 1. Partisan Bias Measurement

**What we cite today** —

- **Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015.** "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82(2): 831–900. — used for B2 (efficiency gap).
- **McDonald, Michael D., and Robin E. Best. 2015.** "Unfair Partisan Gerrymanders in Politics and Law: An Assessment of Partisan Asymmetry." *Election Law Journal* 14(4): 312–330. — used for B3 (mean-median).
- **Warrington, Gregory S. 2018.** "Quantifying Gerrymandering Using the Vote Distribution." *Election Law Journal* 17(1): 39–57. — used for B6 (declination) in v0.3.

**What we should cite** —

- **Grofman, Bernard. 1983.** "Measures of Bias and Proportionality in Seats-Votes Relationships." *Political Methodology* 9(3): 295–327. — foundational partisan-bias metric. Defines the symmetry standard the audit implicitly uses in B4 (seats at 50/50). Should be cited when discussing seat-vote curve asymmetry.
- **King, Gary, and Robert X. Browning. 1987.** "Democratic Representation and Partisan Bias in Congressional Elections." *American Political Science Review* 81(4): 1251–1273. — seat-vote asymmetry methodology. Operationalizes Grofman's bias measure. Directly relevant to B4.
- **Gelman, Andrew, and Gary King. 1994.** "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." *American Journal of Political Science* 38(2): 514–554. — the standard reference for swing/seats analysis in applied redistricting. B4's uniform-swing calculation is the simplest version of their approach; a Bayesian extension is in this paper.
- **Chen, Jowei, and Jonathan Rodden. 2013.** "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269. — **critical omission**. Their finding that urban-concentrated parties (like NDP) are systematically disadvantaged by neutrally-drawn maps because of voter geography is directly relevant to the audit's §B framing. The −2.64% 2019 efficiency gap in Alberta is likely substantially natural packing (per Chen & Rodden), not engineered. **Adding this citation and framing is the single most impactful literature fix for §B.**
- **Rodden, Jonathan. 2019.** *Why Cities Lose: The Deep Roots of the Urban-Rural Political Divide*. New York: Basic Books. — book-length expansion of the 2013 argument; now the more commonly cited source for the "natural suburban expansion" critique. The audit's Urban Hybridization control group (majority: 9 hybrid districts, minority: 25 under identical population constraints) is the empirical counter to this critique. Cross-ref: `private/draft_papers/novel_tests_lit_review.md` §2.2.
- **Chen, Jowei. 2017.** "The Impact of Political Geography on Wisconsin Redistricting." *Election Law Journal* 16(4): 443–452. — extends Chen & Rodden to a single-state case similar in structure to our Alberta analysis.
- **DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021.** "Recombination: A Family of Markov Chains for Redistricting." *Harvard Data Science Review* 3(1). — foundational paper for GerryChain's ReCom algorithm (used in Phase 5). Introduces the GEO metric. Should be cited at the point Phase 5 specifies GerryChain.
- **Stephanopoulos, Nicholas O., and Eric M. McGhee. 2018.** "The Measure of a Metric: The Debate Over Quantifying Partisan Gerrymandering." *Stanford Law Review* 70(5): 1503–1568. — self-critique and response to EG criticisms. Relevant because our audit's RT1 finding (95% CI crosses zero for EG under modeling uncertainty) connects to this paper's discussion of EG stability.

### Critiques of declination and mean-median

- **Warrington, Gregory S. 2019.** "A Comparison of Partisan Gerrymandering Measures." *Election Law Journal* 18(3): 262–281. — author's own comparison showing declination and EG can diverge. Our v0.3 finding that declination disagrees with EG is *consistent with* Warrington's own analysis, not a methodology flaw. **Should cite in the §B2 Red-Team Update paragraph.**
- **Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020.** "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." *American Political Science Review* 114(1): 164–178. — comprehensive critique of single-metric approaches to partisan fairness. Argues for measure ensembles, which is what our v1.2 RT2 gate implicitly requires. Provides citation backing for the "no single metric is dispositive" framing.

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
- **Pal, Michael. 2015.** "The Fractured Right to Vote: Democracy, Discretion, and Designing Electoral Districts." *McGill Law Journal* 61(2): 231–287. — verified on-topic source. Examines boundary-commission discretion, §3 Charter protection, and the limits of courts' role in electoral district design. Should be cited in the §D discussion of commission authority and the academic report legal note.
  > ℹ **Replaces** two prior S6-01/S6-02-flagged entries — Pal 2015 "The Fragmentation of Party Politics" (*UTLJ* 65) and Pal 2019 "The Charter and the Constitutionality of Electoral Boundaries" (*CJLJ* 32) — both of which failed DOI and title verification. See red-team notes 2026-04-23.
- **Smith, David E. 2010.** *Canada's Deep Crown: Beyond Elizabeth II*. Toronto: University of Toronto Press. — Chapter on representation includes provincial redistribution context.
- **Sancton, Andrew. 2008.** *The Limits of Boundaries: Why City-Regions Cannot Be Self-Governing*. Montreal and Kingston: McGill-Queen's University Press. — relevant for the community-of-interest and municipal-boundary anchoring discussion in §C4 (Airdrie-Cochrane-Chestermere treatment and similar urban-fringe splits).
- **Carty, R. Kenneth. 2017.** *Big Tent Politics: The Liberal Party's Long Mastery of Canada's Public Life*. Vancouver: UBC Press. — Chapter 5 on representation and electoral systems.

> **Still unresolved:** The report now cites Courtney but Canadian-lineage engagement remains thin until Courtney is used with chapter/page pincites rather than as a general authority, and until a confirmed Pal article on Canadian gerrymandering methods — if one exists beyond the verified 2015 entry — is located and incorporated.

### Alberta-specific

- **Archer, Keith. 1992.** "Voting Behaviour and Political Dominance in Alberta, 1971–1991." In *Government and Politics in Alberta*, edited by Allan Tupper and Roger Gibbins, xxx–xxx. Edmonton: University of Alberta Press. — former Alberta Chief Electoral Officer; rare academic background on Alberta electoral geography.
  > ⚠ **Citation incomplete:** page numbers needed.
- **Stewart, David K., and Keith Archer. 2000.** *Quasi-Democracy? Parties and Leadership Selection in Alberta*. Vancouver: UBC Press. — context for Alberta's PC/WRP/UCP evolution, relevant to the 2015/2019/2023 cross-election analysis.
- **Wiseman, Nelson. 2020.** *Partisan Odysseys: Canada's Political Parties*. Toronto: University of Toronto Press. — Alberta chapter has political-geography analysis.
- **Bratt, Duane, Keith Brownsey, Richard Sutherland, and David Taras, eds. 2019.** *Orange Chinook: Politics in the New Alberta*. Calgary: University of Calgary Press. — academic compilation on NDP 2015 victory and UCP emergence. Directly relevant to the 2015 cross-election data interpretation. Reference present in report; substantive body engagement still thin.
  > ⚠ **Editor verification note:** the prior version of this entry listed "Brown, Keith, Sayers, Anthony" — the correct editors are Brownsey, Keith and Sutherland, Richard. Verify before submission.

### Indigenous representation

- **Ladner, Kiera L. 2003.** "Treaty Federalism: An Indigenous Vision of Canadian Federalisms." In *New Trends in Canadian Federalism*, edited by François Rocher and Miriam Smith, xxx–xxx. Peterborough, ON: Broadview Press. — relevant to §C4 treatment of Tsuut'ina, Enoch Cree, Siksika Nations and the s.15(2) criterion (d) around Indigenous populations.
  > ⚠ **Citation incomplete:** page numbers needed.
- **Papillon, Martin, and [co-author]. 2021.** "Faire une place à l'autochtonie dans le système électoral canadien." — more recent Canadian literature on Indigenous electoral representation. Relevant to §C4 and A3(d).
  > ⚠ **Citation incomplete:** co-author name, journal, volume, and page data needed before submission.

---

## 3. Compactness and Geographic Analysis

**What we cite today** —

- Polsby-Popper (standard formula, no citation given).
- Reock (standard formula, no citation given).

**What we should cite** —

- **Polsby, Daniel D., and Robert D. Popper. 1991.** "The Third Criterion: Compactness as a Procedural Safeguard Against Partisan Gerrymandering." *Yale Law and Policy Review* 9(2): 301–353. — the paper PP comes from.
- **Reock, Ernest C. 1961.** "Measuring Compactness as a Requirement of Legislative Apportionment." *Midwest Journal of Political Science* 5(1): 70–74. — original Reock.
- **Young, H. Peyton. 1988.** "Measuring the Compactness of Legislative Districts." *Legislative Studies Quarterly* 13(1): 105–115. — compares multiple compactness measures; background for why we should report both PP and Reock.
- **Barnes, Toni, and Justin Solomon. 2021.** "Gerrymandering and Compactness: Implementation Flexibility and Abuse." *Political Analysis* 29(4): 448–466. — critical perspective on compactness as a standalone anti-gerrymander test. Relevant: our §C3 anomaly scan is essentially a compactness critique applied visually without numerical scores.

---

## 4. Vote-Distribution and Apportionment

**What we cite today** —

- No formal citation for the 70/30 urban/rural blending methodology. Admitted in v0.3 critique as a judgment call.

### What we should cite (or at least read)

- **Altman, Micah, and Michael P. McDonald. 2014.** "Public Participation GIS: The Case of Redistricting." In *Proceedings of the 47th Hawaii International Conference on System Sciences*, 2032–2041. Washington, DC: IEEE Computer Society. — describes public-data-only methods for modeling redistricting effects. The 70/30 blend is a simple version of what Altman & McDonald formalize with DA-level precision.
- **Fifield, Benjamin, Kosuke Imai, Jun Kawahara, and Christopher T. Kenny. 2020.** "The Essential Role of Empirical Validation in Legislative Redistricting Simulation." *Statistics and Public Policy* 7(1): 52–68. — methodology for simulating redistricting with empirical vote attribution. Directly relevant to what Phase 4C full execution would do.

---

## 5. Legal and Constitutional Framework

**What we cite today** —

- *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

**What we should cite** —

- *Rucho v. Common Cause*, 588 U.S. 684 (2019). — **critical intellectual context (US).** The US Supreme Court ruled that federal courts have no role in adjudicating partisan gerrymandering claims; the majority explicitly declined to endorse the Efficiency Gap as a judicially manageable standard. This ruling is the direct intellectual motivator for why the audit's two-lane architecture grounds its strongest findings in structural / Traditional Districting Principles measures (Lane 2) rather than purely statistical partisan-effect metrics (Lane 1). Canadian courts operate under *Reference re Saskatchewan* not *Rucho*, but the ruling explains the contemporary analytical climate. Cross-ref: `private/draft_papers/novel_tests_lit_review.md` §3.1.
- *Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912. — extends §3 Charter analysis; relevant for any argument that a majority-committee drafting process impairs effective representation.
- *Frank v. Canada (Attorney General)*, [2019] 1 SCR 3. — recent §3 Charter case; reinforces the "effective representation" standard as binding.
- *Haig v. Canada*, [1993] 2 SCR 995. — earlier case on voting rights, cited in Reference re Saskatchewan discussion.
- > ⚠ **Unverified Pal entry removed:** a prior entry attributed "Gerrymandering in Canada: A Comparative Analysis" to Pal (2021) in *CJPS* 54 based on recalled knowledge. This could not be confirmed and has been removed. The verified on-topic Pal source is listed in §2. A confirmed Pal article specifically on Canadian gerrymandering methodology, if one exists, should be found and inserted here before submission.

---

## 6. What Changes in the Audit If We Incorporate This?

### Methodology-affecting changes

**6.1 Chen & Rodden natural-packing framing.** The 2019 map's −2.64% EG should be framed as "partly a natural artifact of NDP urban concentration (per Chen & Rodden 2013)" rather than "a slight structural UCP advantage." This strengthens the finding in a different way: if the 2019 EG is mostly natural, then the minority map's further shift *beyond* 2019 is more clearly engineered rather than natural.

**6.2 Katz, King & Rosenblatt on ensemble metrics.** Our v1.2 RT2 gate (cross-metric agreement) is justified in the abstract ("hostile experts want multiple metrics") but not cited. Citing Katz et al. 2020 makes the RT2 gate a literature-standard practice rather than a judgment call.

**6.3 Warrington's own divergence finding.** Our declination-disagrees-with-EG result is consistent with Warrington 2019's explicit comparison. Citing it tells readers "this divergence is expected, not a methodology bug."

### Non-methodology-affecting changes (just better-grounded framing)

**6.4 Courtney 2001 for §D.** Every comparator-case claim needs Courtney's backing with chapter/page pincites, not as a general citation.

**6.5 Pal 2015 (verified) for the legal framing note.** The academic report's legal note should cite Pal's "Fractured Right to Vote" (*McGill LJ* 61(2): 231–287) for the boundary-commission discretion framing. The two prior unverifiable Pal entries have been removed.

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
| Courtney 2001 | §D comparator discussion | Grounds Canadian-practice claims | **High** | Cited in report; pincites/substantive engagement still needed |
| Pal 2015 "Fractured Right to Vote" | legal framing note, §D | Boundary-commission discretion and electoral-district design | **High** | Verified entry in §2; not yet incorporated in report body |
| Nosek et al. 2018 | §10 pre-registration | Pre-reg as standard practice | **High** | Added §10 |
| Warrington 2019 | §B2 Red-Team Update | Declination-EG divergence is expected | Medium | Incorporated in report |
| Katz, King & Rosenblatt 2020 | RT2 justification | Literature-grounded ensemble-metric practice | Medium | Incorporated in report |
| Gelman & King 1994 | §B4 methodology | Standard reference for swing/seats | Medium | Incorporated in report |
| DeFord, Duchin, Solomon 2021 | Stage 5 methodology | GerryChain ReCom reference | Medium | Incorporated in report |
| Polsby & Popper 1991 | §8.3 formula | Foundational citation | Low | Incorporated in report |
| Reock 1961 | §8.4 formula | Foundational citation | Low | Incorporated in report |
| Bratt et al. 2019 | 2015 cross-election context | Alberta-specific political science | Low | Reference present; body engagement still thin |
| Sancton 2008 | §C4 community-of-interest | Municipal-boundary anchoring | Low | Reference present; body engagement still thin |
| Ladner 2003, Papillon 2021 | §A3(d) | Indigenous representation literature | Low | Not yet incorporated |

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

A defensible synthesis: *cite Chen & Rodden for the §B framing ("partisan-bias metrics in Alberta are confounded by natural NDP urban concentration per Chen & Rodden 2013"), but note that the structural findings of §A/C/D are not affected by the natural-packing argument because they measure geographic and procedural choices, not vote distribution.*

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

The closest methodological analogs are spatial autocorrelation approaches (Moran's I applied to vote shares), but these are global statistics; they do not isolate directional packed→cracked adjacency pairs.

### Audit's contribution

**"Neighbour-Drain"** is coined in this audit (AsPredicted #289,451; 2026-05-06) to name: a packed ED (losing-party surplus ≥ 0.15) directly adjacent to a cracked ED (winning margin ≤ 0.05) with the same losing party in both — a *coupled chain signal*. The continuous intensity version:

  intensity(X, Y) = max(0, s_X − 0.15) × max(0, 0.05 − m_Y)

and the label-shuffle null distribution are new analytical contributions. Results are reported in `analysis/reports/neighbour_drain_analysis.md` and the academic report.

### Literature to cite when publishing

- Chen & Rodden (2013) — natural-packing baseline that the drain metric must be adjusted against
- Stephanopoulos & McGhee (2015) — whole-map packing/cracking context
- State: "based on a targeted search of the redistricting literature, the specific adjacency coupling we call Neighbour-Drain has no established named measure; this audit introduces the term as a proposed operationalization pending fuller prior-art review"

---

## 10. Pre-Registration and Open Science in Electoral Forensics

### Motivation

Electoral forensics analyses are at high risk of inadvertent p-hacking: the analyst often has partial knowledge of vote distributions before choosing metrics, and there is a natural tendency to foreground metrics that produce larger effects. Pre-registration addresses this by creating a timestamped record of hypotheses, metrics, and inference criteria before outcomes are computed.

### Pre-registration platforms and methodology

- **Nosek, Brian A., et al. 2018.** "The Preregistration Revolution." *Proceedings of the National Academy of Sciences* 115(11): 2600–2606. — canonical paper establishing pre-registration as a standard scientific practice. Directly applicable to electoral forensics; the audit's AsPredicted registrations follow the framework described here.
- **Uhlmann, Eric Luis, et al. 2019.** "Scientific Utopia: III. Crowdsourcing Science, Transparency, and Replication." *Perspectives on Psychological Science* 14(3): 375–395. — covers AsPredicted as a platform designed for pre-registration of observational social-science studies. Our use is consistent with the intended scope.
- **van 't Veer, Anna Elisabeth, and Roger Giner-Sorolla. 2016.** "Pre-Registration in Social Psychology (and Not Only There): Benefits, Challenges and Recommendations." *Journal of Experimental Social Psychology* 67: 2–9. — designed the AsPredicted question template the audit uses.
- **Center for Open Science. n.d.** "Open Science Framework." <https://osf.io>. — the audit's OSF registrations ([w2s8k](https://osf.io/w2s8k/), [r3zm7](https://osf.io/r3zm7/), [qsgy8](https://osf.io/qsgy8/)) are stored here as a parallel public record.

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
| DPG v11 Validation | [#289,449](https://aspredicted.org/289449.pdf) | [w2s8k](https://osf.io/w2s8k/) | Complete; results in report_academic.md |
| Neighbour-Drain null | [#289,451](https://aspredicted.org/289451.pdf) | [r3zm7](https://osf.io/r3zm7/) | Registered; v1 adjacency analysis executed; Drain Phase B label-shuffle null pending |
| ~~89-seat comparison~~ | ~~#289,452~~ | — | Superseded; test unrunnable; noted in writeup |
| Lunty 91-seat scorecard | [#289,455](https://aspredicted.org/289455.pdf) | [qsgy8](https://osf.io/qsgy8/) | Registered; awaiting map publication |

Git pre-analysis commit: `d2aea42` (seeds and analysis scripts committed before any simulation runs).

---

## 11. What This Literature Review Does Not Cover

- **Specific individual boundary commissioners' academic backgrounds.** Relevant if any commissioner has prior academic writing on redistricting, but tangential to this audit.
- **US redistricting litigation history in depth.** Our US-case-law references (Gill v. Whitford) are appropriate given Alberta law has looked to US methodology, but we don't need to cite the full Whitford lineage.
- **Election-administration literature.** Peripheral to boundary-drawing questions.
- **Voting-rights literature as a distinct sub-field.** Important but outside scope.

---

## 12. Publication Implications

If this audit is submitted to an academic journal or used in legal proceedings:

- Chen & Rodden must be cited. Not citing it is a credibility risk.
- Courtney 2001 must be cited with chapter/page pincites rather than as a general authority.
- Pal's verified work on boundary-commission discretion and electoral-district design ("The Fractured Right to Vote," *McGill LJ* 61(2): 231–287, 2015) should be cited for the legal framing note. The previously listed Pal 2015 (*UTLJ*) and 2019 (*CJLJ*) entries have been removed as unverifiable. A confirmed Pal article specifically on Canadian gerrymandering methodology, if one exists, should replace the §5 placeholder before submission.
- The existing Stephanopoulos & McGhee (2015), McDonald & Best, Warrington citations are sufficient for a v0.3-level technical writeup but should be supplemented with the partisan-symmetry literature (Grofman, King & Browning) for full academic grounding.

If the audit is used only for public / media purposes, the literature gap is less urgent. But even in that context, one or two citations — especially to Chen & Rodden and Courtney — would strengthen the credibility of the plain-English framing.

---

*Literature review v0.3. Corrections pass 2026-05-06: Pal hallucination remediation (verified citation: McGill LJ 61(2): 231–287, 2015); Stephanopoulos & McGhee corrected to 2015, 82(2); Sancton corrected to 2008 book (Montreal and Kingston: MQUP); Neighbour-Drain pre-reg status updated; drand seed scopes clarified (5500000 = current simulations, 6062459 = November pre-commitment); priority table updated against report_academic.md; sections renumbered 9–12.*
