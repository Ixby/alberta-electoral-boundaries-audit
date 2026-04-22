---
name: Red-team attack on the academic paper
description: A hostile critique of report_academic.md as a peer reviewer, opposing expert witness, government communications staffer, or political opponent would mount. No defences. No balance. The goal is to find every line of attack that could be used to discredit the audit, ranked by severity.
forward_dependencies:
  - A follow-up fortification pass that addresses each HIGH-severity attack (if the PO directs)
backward_dependencies:
  - report_academic.md v0.12 state (committed aa57424)
  - analysis/v0_1_bias_audit.md (self-audit; this goes further and harder)
  - analysis/v0_1_design_critique.md (prior stress-test pass)
---

# Red-team attack on the academic paper

**Assignment.** Discredit the academic paper. Find every line of attack a hostile reviewer, opposing expert witness, government communications staffer, or political opponent could use. Rank by severity. No defences. No "to be fair." Adversarial pass only.

**Caveat for the reader.** Most of these attacks have partial or full defences in the paper. The point here is not that the paper is wrong — it is to surface where the paper is most *vulnerable*. The PO decides what to fortify.

---

## HIGH-severity attacks (could materially discredit)

### A1. The 95 % confidence interval crosses zero; your core partisan finding is not statistically significant

Your Monte Carlo result is a 95 % CI of [−3.04, +0.76] pp on the minority-majority efficiency-gap asymmetry. The conventional scientific standard for claiming an effect exists is a 95 % CI entirely on one side of zero. Yours is not. You report "89.3 % direction consistency" as a "qualified pass at approximately 90 %," but that is a rhetorical move. Ninety percent is not ninety-five. If you published this in a peer-reviewed political science journal, the referee would tell you the claim "minority is measurably UCP-favourable" cannot be made on this data. You have written an entire section (§3.5) of falsifiability that names a threshold your finding does not cross, and declared the finding passes anyway. A reader who takes statistical significance seriously reads this as special pleading.

Worse: you pair the 89.3 % with cross-election instability (2019 reverses the direction). If a finding is neither statistically significant at 95 % nor stable across elections, the ordinary inference is that there is no effect — the data are consistent with noise. The audit has elevated a null finding into a "qualified" positive finding by inventing graded pass-levels.

**Severity: HIGH.** This is the single line that a peer reviewer would reject the paper on.

### A2. Chen and Rodden's natural-packing argument cuts *against* your case, and you half-admit it

Your §3.6 concedes that "neither 2026 map is engineered *against* natural packing; both partially correct it, with the majority correcting more." Re-read that sentence. You are saying:

- The 2019 baseline has a natural UCP advantage from voter geography (NDP is urban-packed by choice).
- The majority *corrects more of the natural advantage* (EG moves from −2.64 % to −0.85 %).
- The minority *corrects less of the natural advantage* (EG moves from −2.64 % to −1.36 %).

In partisan-framing-neutral language, this means the majority map gives the NDP more than their natural geographic share and the minority map gives the NDP *somewhat less than the majority does, though still more than the 2019 baseline does*. Both maps are NDP-favourable relative to 2019. The minority is just *less NDP-favourable than the majority*. Your "minority is UCP-favourable" claim is true only if you take the majority as the baseline rather than the 2019 map or natural geography.

A defence counsel or government communications staffer will say: the minority commissioners drew a map that is closer to Alberta's natural political geography than the majority proposed. The audit's framing treats deviation from the majority as deviation from neutrality. That is not the same thing.

**Severity: HIGH.** Rewrites the paper's headline finding in reverse.

### A3. The signature-detection thresholds look pre-registered but are not credibly pre-registered

Your packing / cracking / engineered-boundary criteria (P1–P3, C1–C3, E1–E3) have specific numeric thresholds: P1 population ≥ mean + 5 %, P2 winning margin ≥ 15 pp above mean, C1 community split across > single-centre-of-gravity count, etc. You applied these and detected three signatures in the minority, zero in the majority.

Where is the evidence these thresholds were set *before* the data were inspected? The thresholds appear for the first time in v1.2 of the prompt, written after the v0.2 packing-cracking analysis had already been run. "Formally detect" (your phrase) requires the criterion to exist before the test. Your git history does not show the P/C/E criteria being committed before the analysis that generates the values against them.

A peer reviewer will ask: "if you had found four signatures in the majority map and zero in the minority, would you have reported it?" If your answer is yes, where is the version of the code that would have identified signatures in the majority? If your answer is no — the thresholds would have been retuned — this is post-hoc fishing. The paper's claim "the detection is not 'we think the minority looks engineered'; it is 'apply P/C/E criteria mechanically, record what passes'" fails.

**Severity: HIGH.** Any pre-registration claim that cannot be git-proven falls on audit.

### A4. The main-body population analysis is not against the Act's data standard

Your §2 analyses A1 MAD, A2 Calgary zone gap, A3 s.15(2) eligibility — all against the commission's own per-ED tables. You have now discovered (Session 9, Track K) that those tables are derived from July 2024 Alberta TBF estimates, not from the 2021 census. The Electoral Boundaries Commission Act §12(3) requires the commission to use "the population information as provided in the decennial census."

You wrote an end-note acknowledging this. The end-note does not repair the main body. Your A1 MAD of 3,180 for the majority and 4,707 for the minority, your Calgary zone gap of 0.36 % vs 12.20 %, your s.15(2) failure counts — all are derived from numbers the commission should not have been using as the primary basis under a narrow reading of §12. If a court reads §12(5) narrowly, every per-ED number in your Section A is derivative of non-compliant commission data, and your analysis inherits the defect.

You either need to (a) re-run Section A from the 2021 census directly and report the results as the legally-operative analysis, demoting the commission-table analysis to diagnostic, or (b) argue that §12(5) reads permissively and the commission's approach was fine — in which case your whole legislative-reform proposal is weaker. You cannot have it both ways.

**Severity: HIGH.** Structural flaw now that Track K has been published.

### A5. You selected the urban weight that supports your finding

Your sensitivity table (§3.4) shows the B2 efficiency-gap asymmetry ranges from +1.53 % (at 60/40 urban weight, minority less UCP-favourable than 2019) to −1.52 % (at 80/20, minority more UCP-favourable). Your "central" is 70/30, which produces −0.51 %. You have not justified 70/30 as the objectively correct weight. You have reported a sensitivity range that *includes zero and changes sign* across plausible weights. The choice of 70/30 as the headline is the choice that shows your finding.

A political opponent writes: "when the audit is forced to use a symmetric 50/50 weight or a rural-heavier 60/40, the minority-UCP effect disappears or reverses. The author picked the weight that produces a UCP tilt." The only defence is a principled argument for 70/30 from Alberta Election Day apportionment data. Your footnote says 70/30 is "based on observed 2023 apportionment." Does 2023 apportionment generalise to 2027 or 2031? If it does not, your central finding is 2023-specific, a point you partly concede in §3 but do not carry through.

**Severity: HIGH.** The sensitivity table is in the paper and undermines the central claim.

---

## MEDIUM-severity attacks (rhetorically effective; peer reviewers would flag)

### B1. "Qualified pass" creates infinite gradations that make falsification impossible

Your stress-test structure has:

- Strong pass (95 % CI same sign)
- Qualified pass (90 % CI same sign; 95 % crosses zero)
- Fail (90 % crosses zero)
- Plus cross-metric: strong pass, qualified pass, fail
- Plus cross-election: strong pass, qualified pass on direction / fail on magnitude, fail on magnitude
- Plus "retractions" (your three proof-of-discipline cases)

A careful reader can count that your finding either fails outright or "qualified-passes" on all three stress-test categories. You have not reported a result in the strict "strong pass" category for the minority-majority partisan claim. Yet you continue to treat the claim as a finding the audit can defend.

The counter-reading: you have defined pass-levels granular enough that no finding can ever fully fail, and used that structure to rescue a borderline result from the ordinary statistical conclusion (which would be "no measurable effect").

**Severity: MEDIUM.** A reviewer sensitive to falsifiability notices this and cannot un-see it.

### B2. The declination (B6) disagrees with your other metrics and you label it "disagreement" rather than "null"

B2, B3, B4 all point weakly UCP-favourable for the minority. B6 declination shows the opposite (−0.015 for minority vs −0.021 for majority — majority *more* UCP-favourable by this metric). You could report this as "three out of four metrics agree." You could also report it as "one in four metrics contradicts" — and given B6 is the most sophisticated metric in the set (Warrington 2018), a reviewer could legitimately argue B6 should be weighted higher.

Your §3 effectively says "three versus one is majority." Political science methodology does not work that way. If four thermometers disagree, you investigate which is reading correctly, not vote by majority. Your treatment of B6 reads as "the most advanced metric disagreed, so we bundled it into a 'cross-metric disagreement' label and moved on."

**Severity: MEDIUM.** Exposes methodological preference for the metrics that support the finding.

### B3. Symmetry claims are asserted, not demonstrated

You repeatedly invoke "symmetry discipline" — that every test is applied identically to both 2026 maps. But several of your tests were *designed around* the minority map's features. Specifically:

- Calgary Zone A vs Zone B classification was constructed to exhibit the minority's apparent packing; you do not document a Zone C or Zone D analysis or ask whether the majority's zone structure has a similar asymmetry that you did not operationalise.
- The "engineered boundary" (E1-E3) criterion was constructed around the RMH-Banff Park extension — a specific minority choice. Canmore-Banff (a majority district) fails your §A3 at 1/5 on the same criteria space; you note this and move on. A truly symmetric test would have been pre-specified for *any* district meeting the criteria, across both maps, not designed with the minority's anomaly in mind and then back-applied.
- Airdrie 4-way vs 2-way is a minority-specific configuration. You do not propose and test an equivalent "4-way split exists somewhere in the majority" counter-question.

The asymmetry of your *test selection* is not cured by applying each selected test "symmetrically to both maps." You chose tests that the minority was already known to fail.

**Severity: MEDIUM.** Undermines the "non-partisan" framing.

### B4. Track D's OCR recovered 14 of 88 submissions — 74 remain unread — yet you claim to have refuted the chair's "no public support" claim

Your §5.4 says the chair's claim is refuted on three configurations. The refutation rests on identified supporting submissions in the 1,252 text-layer submissions you parsed plus 14 OCR recoveries. You never parsed 74 of the 1,340 total submissions. The chair's claim was about the full record. Your counter-example method is valid for "at least one supporter exists" but cannot adjudicate "the record on balance supports the minority" against "the record on balance opposes the minority" without the missing 74.

More fundamentally: the chair's "no public support" statement is about *active advocacy*, not mere non-opposition. A submission that does not mention RMH-Banff Park at all does not count as either support or opposition. Your counter-examples are three submissions (RMH) to 1,340, which is 0.2 % of the record. A hostile reader says: "three submissions is not public support; it is three citizens."

**Severity: MEDIUM.** Your refutation is technical, not substantive.

### B5. The procedural critique has been destabilised by Chair Miller's R5

You pitched §5 as establishing the April 16 process was a government-controlled replacement of an independent commission, distinguished from Quebec 1992, Ontario 1996, and BC 2008. Then you discovered (Session 9) that the commission chair himself proposed a 91-seat Select Special Committee as a fallback in his Addendum, with specific conditions. The April 16 motion invokes chair R5's vehicle.

You wrote a close reading (`v0_1_chair_recommendation_5_analysis.md`) concluding "form match, conditions pending, intent inverted." A hostile reader reads this as: the chair himself proposed the committee, the government accepted it, and the audit is now reduced to arguing about whether the committee will honour the chair's conditions — which is an argument about a map that does not yet exist. Your procedural critique has become conditional: *if* the November map violates R5(a)–(d), the procedural critique stands; *if* it honours them, the procedural critique evaporates.

**Severity: MEDIUM.** Undermines a core framing — and you are stuck with it because the paper is public.

### B6. The paper is declared "AI-assisted, published unedited after generation"

Your Reproducibility Disclosure at the top says the paper is "the direct output of the scripts and agent interactions listed below" and "no human-authored text was substituted for AI-generated analysis." A reader who takes this at face value concludes: the author ran an AI pipeline, accepted the output, signed their name. In the current state of scholarly discussion about AI-generated text, this is a target.

A peer reviewer says: "who actually wrote this?" A politically hostile reader says: "a bot wrote a 700-line critique of the government and the author put their name on it." Your disclosure is *more* honest than most AI-assisted work, and that honesty is exactly what gives opponents the material. You have given them a real, cited concern about authorship.

**Severity: MEDIUM.** The disclosure cuts both ways.

---

## LOWER-severity attacks (available to political opposition but easier to answer)

### C1. Author bias disclosure does not cure methodology

You disclose a prior that UCP boundary handling was worth scrutiny. You cite three "retractions" as evidence the methodology over-ruled the author's prior. A hostile reviewer says: three disclosed retractions in a 700-line paper are a ritual gesture. The underlying methodology was designed by someone with the prior; every test selected, every threshold set, every comparator chosen was filtered through that prior.

### C2. Comparator-case selection is self-serving

Your §5.3 cites Quebec 1992, Ontario 1996, and BC 2008 as the three Canadian comparators for government action on commission output. These are the three most commonly cited because they are the three *least* intrusive mid-cycle amendments. You do not survey all Canadian provincial redistributions since 1991 — you admit this. A hostile reviewer says: you picked the three cases that make the April 16 Alberta action look worst. There may be Canadian cases of more intrusive government action that would moderate your conclusion.

### C3. The constitutional standard (Saskatchewan Reference) is permissive, not restrictive

*Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158 held that substantial deviation from population equality is permissible when it serves factors like community of interest, geography, and minority representation. Your §11 invokes Saskatchewan Reference as the standard against which a challenge could be mounted. A defence lawyer applies the *same case* in support of the minority map — the minority's rural preservation, s.15(2) invocations, and community-of-interest arguments are exactly what Saskatchewan Reference permits. Your framing selects Saskatchewan Reference as a ceiling; the case also functions as a floor.

### C4. Missing international and intra-provincial base rate

You report a 1-to-3-seat minority-majority asymmetry as "measurably UCP-favourable." What is the comparator? In a 2022 federal redistribution with demographic shifts, what is the typical partisan asymmetry of the interim versus final map? In BC 2023? Saskatchewan 2022? If 1-to-3 seats is below the ordinary variance of Canadian redistribution processes, your finding is not remarkable. You do not provide this base rate. A reviewer pushes back: "your paper documents that two maps differ by 1 to 3 seats. Is that anomalous for Canadian redistribution? You do not say."

### C5. The 338 Canada cross-validation has two model layers, not one

Track J's 338 per-riding integration is presented as independent validation of the structural boundary effect. But 338 Canada is itself a modelled aggregation of polling and demographic data. Reallocating it through your hybrid crosswalks to produce per-proposal seat projections stacks two models. Agreement between the audit's 2023-vote projection and 338's April 2026 polling projection may reflect shared structural assumptions — both use similar aggregation methods at the riding level — rather than independent triangulation. A methodologist says: model-plus-model agreement is not the same as data-plus-data agreement.

### C6. Sub-agent-generated analyses inherit their prompts

Several pieces of evidence in the paper — the signature detections, the rationale inventory, the Plan B cross-check, the cycle-lag analysis, the Calgary data-completeness check — were produced by sub-agents spawned by the parent session. The parent writes the prompts. The sub-agents produce outputs that fit the prompts. There is no chain where a sub-agent produced a finding that contradicted the parent's hypothesis and the parent let it ride. The chain of production is: human author → AI parent → AI sub-agent → writeup → paper. At every step, framing control was with the preceding layer.

### C7. Scope creep

Your original prompt (v0.1, v0.2) was a symmetric partisan-bias audit: B1–B6 on three maps. Your current paper includes: population equality (A1–A3), geographic coherence (C), procedural critique (D), signature detection (P/C/E), chair R5 close reading, public-support refutation, AI-use framework, legislative reform proposal, 338 cross-validation, CSD splits, journey-to-work, rationale inventory. Each addition deepens the attack on the minority. A hostile reviewer says: "the author kept adding tests until one of them showed what they were looking for." The scope now has the shape of a prosecution brief, not a scientific analysis.

### C8. The pre-registered November checklist is self-advantaging

Your "honest test" threshold for a November gerrymander — three signatures PLUS new signatures PLUS (ensemble-outlier OR inversion) — is three conjunctive conditions. Empirically, almost no real-world redistricting map will meet all three. By setting the bar this high, you have guaranteed that almost any November map will fall short of the "sure-sign" category. You can then say "the November map is concerning but not a sure-sign gerrymander," which retains your authority as a measured analyst regardless of the actual map. A hostile reader says: you designed a test you could always interpret.

### C9. Reproducibility claims over-promise

Your paper repeatedly claims every number is reproducible from the repository. This is true in principle. In practice: Python 3.14.3 + specific textstat version + specific pdfplumber version + specific geopandas installation + live access to 338 Canada's specific HTML structure + live access to StatsCan's specific table layout. An attempt to reproduce 18 months from now will likely encounter at least three version or URL breakages that require manual repair. Your "reproducible" claim is an aspiration that decays as dependencies change.

### C10. Small differences framed as patterns

You repeatedly take 1–3 seat effects, 1–2 percentage point efficiency gaps, and 0.5 pp asymmetries and describe them as "measurable," "directional," "systematic." All three words suggest a pattern. A hostile reviewer says: a 0.5 pp efficiency-gap difference in a chamber where turnout varies by 5+ pp across elections is signal sized smaller than natural noise. Calling that "measurable" is technically correct and rhetorically misleading.

---

## Ranking of attack severity

| Attack | Severity | Where it lands |
|---|---|---|
| A1 CI crosses zero | HIGH | Peer reviewer, methodologist |
| A2 Chen-Rodden flips the framing | HIGH | Expert witness, policy analyst |
| A3 Signatures not credibly pre-registered | HIGH | Pre-registration advocate, peer reviewer |
| A4 Main-body analysis on non-census data | HIGH | Counsel, peer reviewer |
| A5 70/30 weight chosen to support finding | HIGH | Methodologist, political opponent |
| B1 Qualified-pass structure protects finding | MEDIUM | Careful reviewer |
| B2 B6 declination disagreement underweighted | MEDIUM | Political scientist |
| B3 Symmetry asserted not demonstrated | MEDIUM | Reviewer familiar with the minority |
| B4 Public-support refutation is technical only | MEDIUM | Procedural-fairness lawyer |
| B5 R5 destabilises procedural critique | MEDIUM | Defence counsel, government comms |
| B6 AI-assisted authorship | MEDIUM | Integrity-focused reviewer, political opponent |
| C1 Bias disclosure ≠ bias cure | LOW | Political opponent |
| C2 Comparator selection | LOW | Comparativist scholar |
| C3 Saskatchewan Reference cuts both ways | LOW | Defence counsel |
| C4 No base rate | LOW | Quantitative methodologist |
| C5 338 validation has two model layers | LOW | Methodologist |
| C6 Sub-agent outputs inherit prompts | LOW | AI-integrity reviewer |
| C7 Scope creep | LOW | Political opponent |
| C8 Checklist too strict to ever trigger | LOW | Political opponent |
| C9 Reproducibility decays | LOW | Software-engineering reviewer |
| C10 Small differences framed as patterns | LOW | Political opponent |

---

## Which attacks the paper is most exposed on

If I had to kill this paper as a peer reviewer, I would lead with **A1 and A5**. A1 because statistical significance is a bright-line test that political science generally respects. A5 because the sensitivity table is *in the paper* and shows the finding reversing under plausible weights the author did not use. Both are tightly evidence-based, both come from the paper's own numbers, and both admit only narrow defences (arguing for an enriched significance criterion, arguing for 70/30 as objective).

If I had to kill this paper as a government communications staffer, I would lead with **A2 and B5**. A2 because Chen-Rodden gives the government a counter-framing that sounds like a compliment ("the minority map respects Alberta's natural political geography"). B5 because the chair's own R5 gives the government a chair-endorsed anchor for the April 16 action.

If I had to kill this paper as a political opponent with no technical expertise, I would lead with **C7 and B6**. C7 because "scope creep from audit to prosecution" is easy to understand. B6 because "AI wrote the report attacking the government" is a one-sentence dismissal.

---

## What the paper does not defend itself against

These attacks are largely un-addressed in the current paper:

- **A1**: the paper acknowledges CI crosses zero but defends via "qualified pass" structure; it does not engage the underlying "90 % is not 95 %" critique head-on.
- **A3**: the paper claims the signature criteria were formally pre-registered in v1.2, but does not produce a git timestamp proving the criteria predate the analysis runs that generate values against them.
- **A5**: the paper's defence of 70/30 is a footnote citing "2023 apportionment." A fuller defence would require showing 70/30 is robust across elections or principled on its face. Neither is in the paper.
- **B5**: the paper's chair R5 close reading is posted as a separate file; §5 in the academic paper has been updated with the R5 analysis, but the "form match / intent inverted" framing is itself an interpretation a hostile reader will dispute.
- **C4**: no comparative base rate is offered. The paper could survey BC 2023, Saskatchewan 2022, federal 2022 for partisan asymmetries between commission alternatives and find its own finding's magnitude in context.

---

## Author's position if this red-team were real

If the author were sitting in a peer-review exchange or a courtroom deposition with a competent opposing expert, the five questions above (A1, A2, A3, A4, A5) would be the ones that would produce the least defensible answers under pressure. The paper's disciplined structure (defensibility gates DA1–DA7, stress-test gates RT1–RT6, multiple self-audits) is a stronger defence against weaker attacks but does not obviate these five. Any fortification pass should start there.

A fortification pass is not commissioned by this document. This document is the attack, not the defence.
