---
name: Red-team attack on the academic paper — round 2 (v0.14 state)
description: Second adversarial pass on report_academic.md after the v0.14 fortifications. New attack vectors introduced by the fortifications themselves, residual vulnerabilities the first red-team's fortifications did not fully close, and attacks the first red-team missed entirely. No defences.
forward_dependencies:
  - optional round-3 fortification if the PO directs
backward_dependencies:
  - analysis/v0_1_red_team_academic_discredit.md (first red-team)
  - analysis/v0_1_fortification_a1_a5.md, b1_b6.md, c1_c10.md (first-pass defences)
  - report_academic.md v0.14 state (committed 22b156e)
---

# Red-team round 2 — v0.14

**Assignment.** Discredit the paper in its v0.14 state. The v0.13 red-team (21 attacks) has been fortified. This pass finds (a) NEW attack surfaces the fortifications themselves created, (b) RESIDUAL attack surfaces the fortifications narrowed but did not close, and (c) attacks the first pass missed because the attacker had been thinking along particular lines.

---

## NEW ATTACK SURFACES INTRODUCED BY FORTIFICATION

### D1. Your own §3.13 table literally says RT1 and RT3 "Fail strong pass"

You added §3.13 "Stress-test grades mini-audit" to defend against B1 (qualified-pass gradations). The table is now in the paper and contains two rows that read:

| Gate | Outcome |
|---|---|
| RT1 — Monte Carlo 95% CI | **Fails strong pass** |
| RT3 — Cross-election stability | **Fails strong** |

You introduced this table to demonstrate auditable transparency. What it actually does is put on a single page, at reviewer-quotable granularity, that two of your six stress-test gates fail. A peer reviewer asks: "of the six gates you set for yourself, two fail. Why is the paper a finding rather than a non-finding?" Your answer has to be the multi-dimensional consistency argument, but a reviewer can now quote your own table against you.

**Severity: HIGH.** This is a self-inflicted wound. The graded-pass table was supposed to be auditable transparency. In practice, it's a tabulated concession.

### D2. The AI-provenance manifest says every quantitative finding is AI-authored

You added (§1.4 preamble): "AI-authored, human-verified: all quantitative findings in §§2–3, the sensitivity tables, the signature-detection numerics, the counter-test results in §3.12, the cycle-lag analysis, the Plan B cross-check, the Track C baseline scorecard, and the 338Canada cross-validation."

"AI-authored" covers every numeric claim in the paper. "Human-verified" is the qualifier. In the current discourse about AI-generated content, "AI wrote it, human clicked yes" is a rhetorical devastation. Your disclosure is more honest than most AI-assisted work, which is exactly what gives opponents the material. A political opponent only needs one sentence: "by the audit's own disclosure, every number in the paper was written by an AI."

The original B6 fortification was meant to position the audit as an example of responsible AI use. The manifest you added exceeds the disclosure requirements of *Nature*, ICML, and ACM 2023. That is good for integrity and bad for rhetorical defensibility. The two are now in tension and you chose integrity. A press release will choose the other reading.

**Severity: HIGH.** You cannot unpublish the manifest. Anyone who disagrees with the finding now has a one-sentence dismissal.

### D3. Appendix C reveals the current 2019 map is already malapportioned

You added Appendix C to defend against A4 (main-body uses non-census data). Appendix C reports that under the 2021 Census, **seven of 87 current 2019 electoral divisions** deviate by more than ±25 % from the legal quota. Five are urban-growth EDs. Two are s.15(2)-protected rurals.

Your paper's §2.1 narrative compares the two 2026 proposals on population-equality grounds. The comparison point has implicitly been a legally-compliant baseline. Appendix C establishes that the legal baseline (2019 map, 2021 Census) is *itself non-compliant*. Any defence counsel now argues: "the minority 2026 proposal is not measurably worse than the 87-seat map Alberta currently uses; both have five-plus urban EDs outside the ±25 % window; the minority adds two more seats precisely to relieve this pressure."

Your A4 defence establishes that the minority is not worse than the incumbent. That is the kind of defence the minority would have written for itself.

**Severity: HIGH.** The audit added a finding that the minority can quote as a defence.

### D4. The Lethbridge 4-way "new finding" was discovered in the defensive fortification pass

§3.12 reports the Lethbridge 4-way split as a new minority-map cracking candidate, discovered by the B3 symmetry counter-test that was itself run as a red-team defence. The finding entered the paper within the same session that the red-team attack was authored, the fortification was designed, and the counter-test was executed. The git log of session 9 shows the counter-test script, the counter-test data, and the §3.12 paragraph all commit at the same point (commit 22b156e, 2026-04-22).

Your A3 fortification relied heavily on git timestamps separating the v1.2 prompt (commit 5b0bc06, 08:32) from the signature-detection analysis (commit 282bc6d, 10:56) — a 2h24m gap. The Lethbridge finding has no such separation. The counter-test criteria, the counter-test code, and the paper's new §3.12 paragraph all landed in the same commit. A reviewer sensitive to pre-registration discipline asks: "what is the pre-registration timestamp for the symmetric counter-test criteria?" The answer is: the criteria were specified in the same session as the execution. A sceptic calls this a post-hoc tuning pattern at a 30-minute scale rather than an 8-hour one.

**Severity: HIGH.** The Lethbridge finding's methodological anchor is weaker than the signatures it joins. It is presented in §3.12 at near-equal weight with the pre-registered §3.7–3.9 signatures.

### D5. The comparative base rate is explicitly absent

You added to §3.3: "A comparative base rate for inter-map partisan-asymmetry magnitude in Canadian provincial redistribution does not exist in the published literature; the closest available benchmark is Stephanopoulos & McGhee's (2018) US-state inter-map range of approximately 0.5–4 % EG asymmetry. Alberta's 0.5–1.6 pp range sits at the low end of that US benchmark."

You added this to defend against C4 (no base rate). The defence acknowledges the gap. But the acknowledgement now reads, on its face: *the audit's 0.5-1.6 pp asymmetry sits at the low end of a US benchmark*. Low-end of benchmark is the descriptive meaning of "unremarkable." A hostile reviewer quotes this and asks: "the audit itself says the magnitude sits at the low end of the only available benchmark. What is the finding?"

The answer the paper wants is the multi-dimensional consistency argument. But you have given reviewers a numeric statement about magnitude that reads as self-defeating.

**Severity: MEDIUM-to-HIGH.** Conceding base-rate low-end in writing is a more expensive concession than leaving the base rate unmentioned.

### D6. The §11 Saskatchewan Reference two-way reading gives the defence its legal framing

You added (§11): "the same legal standard that the audit's findings implicate also permits the minority commissioners to invoke it for their configurations."

A defence lawyer, presented with the audit as a plaintiff's exhibit, opens with this sentence. A government communications staffer does the same in a press release. You introduced the two-way reading to defend against C3 (Saskatchewan Reference cuts both ways). What you actually did is draft the first paragraph of the minority's legal brief.

The C3 attack can be answered without the concession. Citing Saskatchewan Reference's permissive-on-deviation character is one paragraph; stating that it grounds the defence is another. You wrote both.

**Severity: MEDIUM.** A narrower version of the same defence would not have given the defence its opening argument.

### D7. The audit now holds three roles simultaneously: analysis, reform advocacy, AI-use guidance

v0.11 was analysis. v0.12 added chair-R5 interpretation. v0.13 added Plan B, cycle-lag, and a legislative reform proposal. v0.14 added an AI-use recommendations file referenced from the paper.

The audit is now simultaneously (a) an analysis of the 2026 maps, (b) a legal-reform proposal for §12 of the Electoral Boundaries Commission Act, and (c) a normative framework for AI use in future redistribution. Each role has different epistemic standards. A reviewer asks: "is this a paper, a policy brief, or a standards document?" The answer is yes, all three.

The C7 attack in the first pass was "scope creep." The fortification (expanded §7 scope-discipline paragraph) made the scope explicit rather than narrowing it. A critic now reads the paper as an advocacy document with analytical citations, which is a legitimate rhetorical framing given the three-role structure you disclosed.

**Severity: MEDIUM.** The scope is now honestly stated but is itself the target.

---

## RESIDUAL ATTACK SURFACES FROM ROUND 1

### D8. The "§2.1 ordering preserved" claim leans on an approximate equality

Appendix C reports 2019-on-2021 MAD 4,745 and the minority-on-2024 MAD 4,707 — a 38-population gap, 0.8 % difference. You frame this as "2026 minority map does not improve on the 2019 map's distribution tightness; majority (3,180) meaningfully does."

A reviewer notes: a 0.8 % difference between the minority and the 2019 baseline is within the noise floor of cross-basis-cross-vintage population comparisons. The minority MAD (4,707, on 2024 TBF) and the 2019 MAD (4,745, on 2021 census) are comparing different maps against different population bases at different vintages. Numerically similar is not analytically equivalent.

The §2.1 ordering argument wants "majority < 2019 < minority" but the data say "majority < 2019 ≈ minority." Within 38 population of equality, the ordering claim is fragile.

**Severity: MEDIUM.** The A4 defence landed, but the ordering claim in the narrow zone is softer than the prose suggests.

### D9. A3 pre-registration is intra-session, not days-blinded

Your A3 defence relies on a 2h24m gap between commit `5b0bc06` (v1.2 prompt with P/C/E criteria) and commit `282bc6d` (signature-detection analysis). This establishes that the criteria predate the analysis within a single session. A true pre-registration standard (OSF, AsPredicted) requires a time-blinded prior commitment — hours before is weaker than days or weeks.

Your own fortification (F3) acknowledges: "the pre-registration is intra-session (hours, not days, of separation)." This acknowledgement is honest. It is also quotable. A sceptic asks: "is intra-session pre-registration pre-registration at all?"

The November 2026 held-out test closes this attack fully. Until November, it does not.

**Severity: MEDIUM.** Honest and narrow but still present.

### D10. The paper asserts "minority more UCP-favourable" despite §3.6 conceding the opposite direction

After the A2 fortification, §3.6 says: "the minority 2026 map corrects less of Alberta's natural UCP-favouring geography than the majority map does." This is literally equivalent to saying both maps are *more NDP-favourable than natural geography*, with the majority *more NDP-favourable* than the minority.

Your paper still leads (§3.3) with "the minority's EG is 0.58 pp more UCP-favorable than the majority's under 70/30 blending." A hostile reviewer points out: these two claims describe the same numeric fact. One framing ("minority more UCP-favourable") supports the audit's headline; the other framing ("majority more NDP-corrective") supports the defence. The same number backs both. Your paper preferentially presents the first framing.

The §3.6 scoping fortification added a note that partisan-bias is "one dimension among six." But the partisan-bias finding is still the numerically strongest headline in the paper. The reframing has not resolved the tension.

**Severity: MEDIUM.** The tension remains visible.

### D11. The tier-based public-support refutation is majority-of-configurations favourable to the chair

Your §5.4 distinguishes three tiers: precisely-AND-effectively wrong (3 configurations), precisely-wrong-effectively-ambiguous (1), and chair-effectively-correct (3). That is 3 refuted, 1 ambiguous, 3 upheld out of 7 configurations — a 3:3 split with a tie-breaker.

The paper's §5.4 narrative emphasizes the "chair was wrong" tier. The distribution says something different: the chair was right about as often as wrong. A hostile reader says: "the audit refutes the chair on three configurations and upholds him on three others, plus one ambiguous. By your own tiered audit, the chair's 'no public support' characterization was at least half correct."

Your B4 fortification added a categorical-refutation defence (one counter-example suffices for a universal-negative claim). That defence is sound for the categorical claim. It does not neutralize the majority-rhetorical reading, which is what audiences actually use.

**Severity: MEDIUM.** The categorical-refutation defence is logically right and rhetorically inadequate.

---

## ATTACKS THE FIRST PASS MISSED

### D12. The fortification was produced in the same session as the red-team

Git log for session 9 shows: red-team attack at commit `fa85610` (v0.13); fortification at commit `22b156e` (v0.14). Both commits are dated 2026-04-22. The fortification was designed, drafted, and committed within hours of the red-team attack. No external peer review occurred in the window.

A reviewer who inspects the git log asks: "the 21 attacks were answered inside a single work-day by the author being attacked. Is the defence independent?"

The honest answer is no, the defence is self-defence. The first red-team attack was constructed by the author-operated audit. The fortification was constructed by the same author-operated audit. Peer review, by definition, requires a party external to the author. The audit has run adversarial and defensive passes within itself.

**Severity: HIGH.** The audit's strongest integrity claim (adversarial self-audit) is also its strongest vulnerability (no external adversary was involved).

### D13. Chen-Rodden is US voter geography applied to Alberta without validation

Chen and Rodden (2013) analysed US Democratic voter concentration in urban cores. Their "natural-packing" argument rests on specific US geographic conditions: party-dense urban precincts, non-party-dense suburban rings, strong rural partisan alignment.

Alberta's geography is different. Edmonton NDP concentration is real but smaller and less spatially distinct than, say, Chicago or Philadelphia Democratic concentration. Calgary's NDP districts are not packed the way US urban cores are packed — they are scattered.

You invoke Chen-Rodden (§3.6) as authority for the claim that the majority map corrects natural packing. You do not test whether Alberta's voter geography actually produces the kind of natural packing Chen-Rodden theorised. The invocation is rhetorical.

A methodologist with Canadian redistricting expertise (e.g., Pal, who you cite) would ask: "which Canadian study has replicated the Chen-Rodden effect for provincial-level geography? None that I know of." The §3.6 defence borrows US theoretical authority without Canadian empirical validation.

**Severity: MEDIUM.** A peer reviewer familiar with Chen-Rodden's original scope will flag this.

### D14. The "structural findings primary" reordering is post-hoc

Your v0.3 report presented §B partisan-bias findings as the headline ("minority shifts baseline toward UCP"). Your v0.14 §7 says: "The primary finding is structural: the minority map shows wider population dispersion..." (§3.6 reframing). This reorders which findings are primary.

The reorder happened in the fortification pass, specifically to defend against A2. A reviewer reading the git diff asks: "was the structural-primary framing present in your v0.3, v0.11, or v0.12? Or did it emerge in v0.14 to answer A2?"

The honest answer is v0.14. A sceptic calls this "fortification-driven finding prioritization." The reorder makes the audit more defensible; it also makes the audit's framing less stable over time.

**Severity: MEDIUM.** The reframe is visible in the commit history.

### D15. The sub-agent prompt archive reveals author-controlled framing, not removed it

You published every sub-agent prompt used in session 9 (`analysis/v0_1_subagent_prompts_appendix.md`). The B3 counter-test prompt, the Track N database-survey prompt, the Track O provenance-audit prompt, the Track Q fortification prompt — all are author-written instructions telling the sub-agent what to look for and how to phrase the result.

Publishing the prompts cures the invisibility. It does not cure the framing. A sub-agent prompt that says "find whether the minority map has packing patterns" will find them if they exist (and report nothing if they do not). A sub-agent prompt that says "find whether either map has packing patterns, starting with the minority as the hypothesis-generating map" is directing attention. The latter is the kind of prompt the audit used.

The C6 fortification relied on "publishing the prompts archives framing control." The publication establishes accountability but does not establish neutrality.

**Severity: MEDIUM.** The prompts are author-crafted. The archive documents this honestly; it does not neutralize it.

### D16. Track N's "census not constitutionally required" cuts against the audit's §12 critique

Track N established that census-based redistribution for provincial elections is not constitutionally required. The reform proposal cites this finding to argue that Option B (composite basis) is constitutionally safe.

A sceptic reads the same finding differently: if §12(3)'s "decennial census" requirement is not constitutionally anchored, the commission's use of 2024 TBF estimates as primary basis is not a constitutional concern. It is, at most, a statutory interpretation question under §12(5). The audit's A4 attack (and your A4 fortification) was built on the premise that the commission's practice sits in statutory tension. If the whole §12 census-primary structure is mere policy, the tension is policy-level, not principle-level.

The Track N constitutional verdict weakens the force of both (a) the audit's critique of the commission's methodology disclosure and (b) the reform proposal's urgency. You now have the strongest possible defensive argument for the commission: "the Act's data-source rule is itself a policy choice; our choice was within that policy discretion."

**Severity: MEDIUM-to-HIGH.** Track N's finding helps the reform proposal's constitutional safety and simultaneously weakens the paper's characterization of the commission's methodology as inconsistent.

### D17. The November held-out test is conditional, revisable, and still in the future

Your A3 and B3 defences both rely on the November 2026 MLA-committee 91-seat map as a held-out test. Pre-registration against a future map is methodologically stronger than intra-session pre-registration, but:

- The map does not yet exist. The pre-registration could be revised before the map lands.
- The audit's author (who has produced the fortifications) will also score the November map. There is no external, neutral scorer.
- If the November map fails the pre-registered criteria, the author's interpretation will be published; if it passes, the same author's interpretation will be published. The scorer and the defender are the same person.

Pre-registration as typically practiced (OSF, AsPredicted) requires a third party (e.g., a journal's editorial board) to hold the pre-registered criteria. The audit's November checklist is self-held.

**Severity: MEDIUM.** The held-out test is a methodological promise, not a methodological fact.

---

## Ranking

| Attack | Severity | Who it lands on |
|---|---|---|
| D1 §3.13 table shows RT1 + RT3 fail strong | HIGH | Peer reviewer |
| D2 AI manifest admits AI authored all numerics | HIGH | Political opponent, integrity reviewer |
| D3 Appendix C shows 2019 map already malapportioned | HIGH | Defence counsel |
| D4 Lethbridge new finding lacks pre-registration | HIGH | Methodologist |
| D5 Base rate is low-end of US benchmark | MEDIUM-HIGH | Peer reviewer |
| D6 Saskatchewan two-way gives defence opening | MEDIUM | Defence counsel |
| D7 Three-role scope (analysis + reform + AI guidance) | MEDIUM | Peer reviewer |
| D8 §2.1 ordering within noise floor | MEDIUM | Methodologist |
| D9 Pre-registration is intra-session | MEDIUM | Methodologist |
| D10 §3.6 concession vs §3.3 headline tension | MEDIUM | Peer reviewer |
| D11 Tier refutation is 3:3:1 split, not victory | MEDIUM | Rhetorical reader |
| D12 Red-team + fortification same-session | HIGH | Peer reviewer |
| D13 Chen-Rodden US application to Alberta unvalidated | MEDIUM | Specialist reviewer |
| D14 Structural-primary reorder is post-hoc | MEDIUM | Methodologist |
| D15 Prompts archive documents framing, doesn't cure | MEDIUM | AI-integrity reviewer |
| D16 Track N kills §12 constitutional framing | MEDIUM-HIGH | Defence counsel |
| D17 November held-out test is self-held | MEDIUM | Methodologist |

---

## What the paper cannot defend against

These attacks admit no defence inside the current paper:

- **D1** (graded-pass table shows failures): the table is now in the paper; the concession is in print.
- **D2** (AI-authored all numerics): the manifest is more honest than most. No amount of honesty will neutralize the rhetorical payload.
- **D3** (2019 map also malapportioned): Appendix C established this as a finding. A defence counsel for the minority can now quote Appendix C against §2.
- **D12** (same-session self-audit): the git log is immutable. External peer review is the only cure and it has not happened.

## What the paper can defend against but currently does not

- **D4** (Lethbridge pre-registration): add an explicit timestamp note. The Lethbridge finding should be flagged as "post-hoc, discovered in the B3 counter-test, to be held out from signature-count claims until re-tested in November."
- **D5** (base-rate low-end): acquire 3-5 Canadian comparator cycles. The base-rate acquisition was flagged but not completed; completing it closes the attack.
- **D13** (Chen-Rodden Alberta validation): run a Chen-Rodden-style simulated ensemble on Alberta's 2019 map with 2023 votes. Determine whether "natural packing" in the US sense actually applies. This is a ~40K-token sub-agent task.
- **D17** (November held-out test): commit the November re-audit execution to an external peer or a public pre-registration platform (OSF) before the map lands.

## What would fortification round 3 look like

If the PO directs a round-3 fortification:

1. Add a "same-session disclosure" note to the Reproducibility Disclosure acknowledging D12 honestly.
2. Add a timestamp and held-out-from-headline caveat for the Lethbridge finding (D4).
3. Acquire 3-5 Canadian comparator EG asymmetries to close D5.
4. Run a Chen-Rodden Alberta validation sub-agent to close D13.
5. Post the November pre-registered checklist to OSF or an equivalent third-party pre-registration platform (D17).
6. Accept D1, D2, D3, and D12 as permanent vulnerabilities inherent to the pipeline, not fortifiable via more analysis.

Note that D1, D2, and D3 were each *created* by the fortifications. A round-3 fortification that tries to cure them risks creating round-3 vulnerabilities in turn. At some point the paper has to stop fortifying and accept that the defence surface is the surface.

*Round-2 attack. No defence. 17 new / residual / missed attacks catalogued with severity and target audience. Round 3 fortification scope outlined for PO direction.*
