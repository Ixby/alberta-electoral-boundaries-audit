# v0.2 Final Red-Team — Pre-Publication Clean-Room Readiness

**Author:** final red-team agent (Claude Opus 4.7 1M)
**Date:** 2026-04-22
**Scope:** Methodological, framing, citation, and internal-consistency audit of the v0.4 published reports and the v1.2 re-execution prompt, conducted as the last gate before clean-room execution in a new session.

Findings are classified by severity:

- **BLOCKER** — reports should not publish as-is; must be fixed.
- **MATERIAL** — publication-ready only with a correction note; risks defensibility.
- **COSMETIC** — worth fixing but does not alter any claim.

---

## Part 1 — Design Red-Team (Academic + Public Reports)

### 1.1 BLOCKER — B2 majority efficiency gap is reported as two different numbers

The academic report's main result table §3.3 states **Majority B2 EG = −0.78%**. The same academic report's Chen-Rodden framing paragraph §3.6 states **Majority EG = −0.85%**. The sensitivity table §3.4 (urban weight 0.70) shows **−0.78%**.

The public report uses **−0.85%**. The HTML uses **−0.85%**. The v1.2 prompt's carry-forward table says **−0.85%**. The migration doc and CLAUDE.md are consistent with −0.85%.

So within the academic report itself, §3.3 (−0.78%) conflicts with §3.6 (−0.85%). And the academic report (main table −0.78%) conflicts with the public report and HTML (−0.85%).

Line references:
- `report_academic.md:235` — −0.78%
- `report_academic.md:249` — −0.78% (sensitivity 0.70)
- `report_academic.md:263` — −0.85%
- `report_academic.md:475` — −0.78% (synthesis table)
- `report_public.md:194` — −0.85%
- `report.html:259` — −0.85%
- `v1_2_gerrymander_audit_prompt.md:58` — −0.85%

This is not a rounding artifact (0.07 pp gap). One of the numbers is from a superseded pipeline. The v0.4 outputs should settle on a single canonical value before publication; if the current scripts now emit −0.85% at the 70/30 central weight, §3.3 and §3.4 of the academic report and the §7 synthesis table all need updating. If they emit −0.78%, then the public report, HTML, v1.2 prompt, migration, and CLAUDE.md all need updating.

**Action required before clean-room publication:** re-run `v0_2_packing_cracking_analysis.py` and either correct the academic report or correct every other downstream artefact.

### 1.2 BLOCKER — Monte Carlo CI reported as two different intervals

Academic report §1.4 (v0.3 fortifications): 95% CI **[−3.14, +0.74] pp**, mean −1.25 pp, median −1.45 pp.

HTML report §academic-section-B-red-team: 95% CI **[−2.99, +0.76] pp**, mean −1.25 pp.

v1.2 prompt carry-forward table: CI **[−2.99, +0.76] pp**.

Migration.md: CI **[−2.99, +0.76] pp**.

The academic report is an outlier. Same mean, different bounds — this is either a prior Monte Carlo run carried forward without update, or a different seed. Either way, a reader who checks the academic report against the HTML gets inconsistent numbers, and a re-execution will not match one of them. The −3.14 and +0.74 values appear only in the academic report (plus the deprecated v1.1 prompt copy); every other up-to-date artefact uses −2.99 / +0.76.

**Action required:** reconcile to whichever the current `v0_3_monte_carlo_ci.py` run produces and correct the stale one.

### 1.3 MATERIAL — Chen & Rodden framing is applied asymmetrically inside the academic report

In §3.6 the Chen-Rodden natural-packing argument is invoked to *weaken* the partisan-intent implication of the minority's UCP-favorable EG shift: "neither 2026 map is engineered against natural packing; both partially correct it, with the majority correcting more."

But the §7 synthesis table still lists **§B2 Efficiency gap minority −1.36% / +0.58 pp more UCP-favourable** under "direction of minority shift" without the Chen-Rodden framing applied. The academic report therefore says two things in adjacent sections:

- §3.6: Minority EG gap *partially corrects* natural packing — not engineered against it.
- §7: Minority EG *shifts the baseline toward UCP* relative to the majority.

Both can be true (the minority corrects less than the majority, so relatively it is more UCP-favourable), but the §7 table does not carry the §3.6 caveat, so a reader reading the synthesis alone gets the stronger framing. The public report's "probable" list also does not carry this caveat.

**Action recommended:** Add a footnote to §7 and to the public report's "probable" bullet tying the partisan-bias finding to the §3.6 natural-packing caveat, or restate the finding as "minority corrects the 2019 natural-packing baseline less than the majority does."

### 1.4 MATERIAL — Structural vs vote-based blurring in the public report

The public report's "demonstrable" list (§What the data supports) mixes structural findings (population swings, Airdrie split, anomaly shapes) with one vote-based finding: the chair's "no public support" refutation, which IS a documentary finding so belongs in "demonstrable," and that is correct. But:

- The "probable" list contains "Alberta's current 2019 map has a mild UCP tilt, about −2.6% on the efficiency gap. Most of this is natural geography, not boundary engineering." This mixes a computed metric (the -2.6% number comes from vote attribution) with a causal attribution ("natural geography, not boundary engineering"). The causal attribution is a Chen-Rodden-style *interpretation*, not a finding. It is presented in the same tone as the numeric finding.

- The "unlikely" list contains "The majority map is partisan in favour of the NDP. Not supported by the data. The majority map keeps the status quo partisan balance; the status quo has a mild UCP tilt." This dismisses an NDP-favourable-majority claim using the same Chen-Rodden framing. But if the minority's shift is directionally UCP-favourable, then by the same logic anything with a UCP-tilt reduction could be called NDP-favourable, and the public report doesn't show that analytical step. The dismissal is plausible but a hostile UCP-aligned reader could call this one-sided.

**Action recommended:** Rephrase the 2019-UCP-tilt bullet to separate the measurement (−2.6% EG) from the causal claim (natural geography). The causal claim is defensible but should be marked as an interpretation, not a fact.

### 1.5 MATERIAL — Section D submission-archive "partially refuted" framing is defensible but not fully even-handed

Section 5.4 reports verdicts by configuration (Airdrie 4-way: chair stands, RMH-Banff: refuted, Olds-ODH: refuted, Chestermere: partially refuted, Red Deer: partially refuted, Nolan Hill-Cochrane: stands, St. Albert: stands).

The even-handed treatment is mostly good: the §5.4.3 sample-size caveat is honest, and §5.4.4 explicitly names that the minority cannot claim public mandate for two of the five configurations. However:

1. The verdict labels are not symmetric. The two configurations where the chair's claim stands (Airdrie 4-way 0/4, Nolan Hill-Cochrane 0/0) are labelled "chair's claim stands." But "stands" for 0/4 is different from "stands" for 0/0 (no data). A strict symmetric framing would distinguish "chair's claim uncontested (no data)" from "chair's claim confirmed by counter-evidence (Airdrie 4-way has 2 opposing submissions)."

2. The Red Deer row uses an "aligned" category (2 explicit + 3 aligned of 23). Other rows don't add an "aligned" category. This is disclosed (limit 4 in §5.4.5) but creates a lower bar for minority-refutation on Red Deer than on other configurations.

3. The "support rate" denominator mixes engaged-citizen and mention counts across rows in a way that isn't statistically comparable (e.g., RMH 20 mentions most of which are neutral, vs ODH 5 mentions most of which are explicit). A reader who skims the table sees "15%" and "40%" and reads them as comparable. They aren't.

**Action recommended:** Add a one-line note above the §5.4.1 table clarifying that support rates across rows are not directly comparable because mention counts and neutrality distributions differ.

### 1.6 MATERIAL — Citations that back claims loosely

The academic report adds APA citations; spot-check against specific claims:

**Pal (2015). "The fragmentation of party politics and the rise of political fixers."** Cited at line 334 as "applies contemporary quantitative gerrymandering analysis to Canadian cases within the Charter framework." The title of the paper does not suggest a gerrymandering-specific analysis; it is a party-politics paper. The v0.1 literature review (`analysis/v0_1_academic_literature_review.md:43`) more modestly describes it as "work on the design and legal constraints of Canadian boundary commissions" — still a stretch. Pal's 2019 paper (The Charter and the constitutionality of electoral boundaries) is directly on-topic; Pal 2015 is not. The sentence should cite Pal (2019) and drop Pal (2015).

**Figueroa v. Canada (2003) and Frank v. Canada (2019).** Cited at line 334 as §3 Charter cases "applying the effective representation standard." Figueroa is about party registration thresholds; Frank is about the 5-year expatriate voting rule. Neither applies the effective-representation standard from the 1991 Saskatchewan Reference to redistribution. They are §3 Charter cases but on different §3 issues. Citing them as a lineage applying the effective-representation standard to redistribution is incorrect. The accurate statement is that they are other §3 cases in the Charter democratic-rights family.

**Haig v. Canada (1993)** appears in the Court cases list but is not cited anywhere in the body text. It should either be added to a specific argument or removed.

**Action required:** Tighten §5.3's lineage sentence to not overclaim what Figueroa/Frank/Pal-2015 stand for. This is the kind of overclaim a hostile legal reader would flag immediately.

### 1.7 COSMETIC — Cross-report framing consistency

The public report labels the 89% direction-consistency finding as "89 out of 100 re-runs of the analysis say so. 11 out of 100 say the opposite." That is accurate and well-framed. The academic report's §1.4 uses "89.3% of samples." These agree. The HTML uses "89% of Monte Carlo samples." All three agree on the direction. Good.

One small mismatch: public report §Effect on seats (line 197) says declination is "the fourth test." The academic report calls declination B6, not B4 — so "fourth" might confuse a reader who cross-references to the academic report. Minor.

### 1.8 COSMETIC — Author-as-student disclosure is load-bearing and should stay prominent

The author is identified as "Mount Royal University, BSc Computer Information Systems (4th year student)" at the top of both reports. This is a credibility-management choice and correct. However, the academic report's tone and citation density read as graduate-level political science. A hostile reviewer could compare the level of sophistication against the disclosure and either (a) dismiss it as AI-generated or (b) question the student's authorship. The current "How this was made" disclosure on the public report handles this well; the academic report's "Reproducibility disclosure" paragraph is also fine. No action.

---

## Part 2 — Prompt Red-Team (v1.2)

### 2.1 BLOCKER — Prompt references a script that does not exist

The v1.2 prompt at line 40 and Gate G0 (line 74) specifies `python3 analysis/check_wuff_voice.py`. The actual checked-in script is `analysis/check_voice_and_readability.py`. The script's own docstring (line 15) even says "Usage: python3 analysis/check_wuff_voice.py report_public.md report_academic.md" — so the script was renamed but its docstring and the prompt both still reference the old name.

A cold-start agent running Gate G0 verbatim will get `FileNotFoundError` and either (a) improvise, violating "no mid-run improvisation," or (b) fail the gate and stop.

**Action required:** Either rename `check_voice_and_readability.py` back to `check_wuff_voice.py`, or update the v1.2 prompt (4 locations: line 40, 74, 156, and the docstring in the script itself) to reference the current name.

### 2.2 BLOCKER — Prompt claims no minority crosswalk exists, but one does

v1.2 prompt line 23: *"No analogous minority crosswalk found in the bundle."*

But `data/v0_1_minority_hybrid_crosswalk.csv` exists (per `ls data/` and `data_acquisition_manifest.md`). A cold-start agent following the prompt will not discover and use this asset, or will be confused when it finds it contradicting the prompt.

**Action required:** Either confirm the minority crosswalk file is canonical and update the prompt to instruct using it, or explain in the prompt why it is not being used.

### 2.3 MATERIAL — Gate G0 asserts "all 5 reproducibility scripts match carry-forward" but the carry-forward table contains −0.85% while the academic report contains −0.78%

See §1.1 above. If G0 requires carry-forward match within 0.05 pp and the academic report has −0.78% against the prompt's −0.85%, G0 will fail on re-execution — not because of methodological drift, but because the prompt and the academic report disagree. The cold-start agent will flag a G0 failure that is really a documentation inconsistency.

**Action required:** Reconcile the EG number (see §1.1) before running G0.

### 2.4 MATERIAL — RT1 threshold arithmetic vs current status

v1.2 RT1 says "90% CI bounds same sign, 95% crosses zero: qualified pass." The current status line cites "95% CI [−2.99, +0.76] pp crosses zero; 89.3% direction consistency. Qualified pass at ~90%."

But 89.3% direction consistency does NOT imply "90% CI same sign." Those are different statistics. 89.3% directional consistency = 89.3% of samples are on one side of zero. The 90% CI could still cross zero (it likely does given that only 89.3% are one-sided). The prompt's "Qualified pass at ~90%" is a reasonable summary but the logic path from 89.3% → "90% CI qualification" is not spelled out; a strict reading of RT1 as written could fail the gate because nowhere is the 90% CI actually checked (vs direction consistency).

**Action recommended:** Tighten RT1 to distinguish "90% CI same sign" (computed statistic) from "direction consistency ≥ 90%" (simpler frequency count). The current Monte Carlo output should produce both; the prompt should say which triggers "qualified pass."

### 2.5 MATERIAL — Vision budget math

v1.2 line 196: "≤ 800 VA centroid inspections total across both maps, concentrated on hybrid-adjacent VAs (interior VAs are trivially assigned by 2019-ED membership alone). At ~400 tokens per inspection, 320K tokens."

800 × 400 = 320,000 tokens. Total budget is 450K. That leaves 130K for everything else — PDF recon, all script writing, all report generation, all 9 gate outputs. That's extremely tight. Reasonable cold-start execution will overflow. The prior readiness doc (`v0_1_prompt_readiness.md`) noted this tension ("400 for majority + 700 for minority = 1,100 VAs × 500 tokens = 550K — still over budget") and the v1.2 cap of 800 is a response, but the remaining 130K headroom is not realistic for Stage 6 report regeneration alone. If Phase 4C actually executes, budget overrun is likely.

**Action recommended:** Either raise the total budget to 600K (which Opus 4.7 1M supports) or explicitly defer Phase 4C to a separate session. The prompt as written risks mid-run budget exhaustion.

### 2.6 MATERIAL — Stage 3a "known result: none" is asymmetric

Known Constraint #1 says "The commission report PDF (pp 87–266, Appendix B) is prose, not tables." This is a majority-side finding (Appendix B is the majority's ED descriptions). The minority's Appendix E was not subject to the same machine-readability recon in the prompt's known-constraints section. If the prompt's symmetry rule is "every test applied identically to both maps," the Appendix-recon knowledge state should be: recon done on both, or recon done on neither. Current state is recon done on majority only, with the minority Appendix E recon noted as "TBD on next execution" (line 190).

**Action recommended:** Either recon Appendix E before prompt execution begins (closes the known-vs-unknown asymmetry), or explicitly document that Appendix E recon is the first Stage 3 task in the new session.

### 2.7 COSMETIC — Appendix C crosswalk verification

Line 23: "mismatches found in v0.3→v1.2 pass (Airdrie-East and Medicine Hat-Brooks were `blend` but should be `direct`)." This is correct scholarly process, but the prompt doesn't state whether those two mismatches have been *fixed* in the mappings or just identified. A cold-start agent needs to know.

**Action recommended:** State whether `MAJORITY_2026_MAPPING` in `v0_2_packing_cracking_analysis.py` has been corrected or still contains the two identified errors.

### 2.8 COSMETIC — "Token budget 450K" vs Opus 4.7 1M

The prompt opens: "Opus 4.7 1M context. 450,000 token budget." The 1M context vs 450K budget gap is large. No explanation of why the budget is capped so far below context. If cost-managed, fine; if from an older prompt version before 1M was available, the cap could be lifted without risk.

---

## Part 3 — Bias Check on the Rewritten Public Report

### 3.1 "Demonstrable" list — defensible

All five items are documentary or measurement-based, and all are consistent with the academic report and source data:

1. Population MAD 48% wider — from commission's own tables, election-independent. **Defensible.**
2. Airdrie 4 vs 2 — visible count from published maps. **Defensible.**
3. Cochrane merged vs intact — visible from published maps. **Defensible.**
4. Three minority districts with chair-flagged shapes — corroborated by direct inspection (§4.2). **Defensible.**
5. April 16 government action, UCP-majority committee — public record. **Defensible.**
6. "No public support" partially wrong — supported by §5.4 submission search. **Defensible.**

None of these depend on modeling choices. None overstate.

### 3.2 "Probable" list — mostly defensible, one overreach

1. "Minority somewhat more UCP-favourable" at 89% — matches the academic report's framing. **Defensible.**
2. "1 to 3 seats" for 2023-style electorate — matches §3.4 sensitivity range. **Defensible.**
3. "Alberta 2019 has mild UCP tilt, mostly natural geography" — the measurement (−2.6% EG) is defensible; the causal attribution ("mostly natural geography") is a Chen-Rodden interpretation, not a direct finding. Should be marked as interpretation. **Mild overreach.**
4. "April 16 more interventionist than three comparators" — matches §5.3's explicit framing. **Defensible.**

### 3.3 "Unlikely" list — check for items that should actually be probable

Scan:

- "Extreme gerrymander" — correctly classified unlikely. The US-courts-threshold test is sound.
- "Neither map differs meaningfully" — correctly classified unlikely given six structural dimensions.
- "Majority is NDP-partisan" — correctly classified unlikely. No evidence.
- "No public support for any minority config" — correctly contradicted by three of five.
- "Clear constitutional violation" — correctly unestablished.
- "April 16 committee will definitely produce a partisan map" — correctly unlikely; speculation.

**One item that could be argued to belong in "probable" rather than "unlikely":** the report does not list "the minority map systematically favours the UCP at a sub-threshold level" as a "probable" item explicitly — it only lists "somewhat more UCP-favourable than the majority," which is different from "systematically sub-threshold favours UCP." The §7 six-dimensional finding in the academic report IS a "probable" claim, but the public report doesn't elevate it. This is a judgment call; the current framing is probably more cautious than the evidence requires, which is the correct direction for a contested public document. No change needed.

### 3.4 "Demonstrable" items that depend on modeling choices

All six demonstrable items are independent of vote modeling. No issue.

### 3.5 Partisan-weaponization resistance

The document explicitly addresses this in §A Note on Scientific vs Sociological Claims and in §How to Share: "Using this document to support extreme claims in either direction — 'the minority is a deliberate gerrymander' or 'both maps are completely fine' — goes beyond what the analysis supports."

This is good defensive framing. The report does NOT read as partisan. A UCP-aligned reader can find support for "the map doesn't cross the US gerrymander threshold"; an NDP-aligned reader can find support for "the structural differences consistently favour the UCP"; both framings are accurate. The document refuses to give either side a quotable gotcha.

**The framing is defensively sound.**

### 3.6 One residual concern

Public report line 211: "The strongest procedural concern is that the new process is government-controlled and is advancing two configurations (Airdrie 4-way, Nolan Hill-Cochrane) that the public did not ask for."

This is a strong claim. The §5.4.4 academic framing is more measured: "The §D critique narrows but does not disappear." The public report sharpens this to "strongest procedural concern" and names the two configurations. A hostile reviewer could argue: (a) the committee hasn't reported yet, so we don't know the committee is "advancing" those configurations; and (b) the audit knows, from §5.4 itself, that there are 4 opposing submissions for the Airdrie 4-way — "public did not ask for" is true, but the committee could respond to those opposing submissions. The public-report framing is a step sharper than the evidence.

**Action recommended:** Soften public report line 211 to "If the November committee advances the Airdrie 4-way or Nolan Hill-Cochrane configurations, the strongest procedural concern applies to those specifically, which the public record does not support." Conditional, not declarative.

---

## Part 4 — Deliverable Summary

**Are the current outputs ready to publish publicly?**

**No, not as-is.** Two blockers must be fixed before publication:

1. **EG number inconsistency** (§1.1): majority B2 is simultaneously −0.78% (academic §3.3, §7) and −0.85% (public, HTML, v1.2 prompt). Pick one, rerun scripts, update all.
2. **Monte Carlo CI inconsistency** (§1.2): academic report has [−3.14, +0.74]; everything else has [−2.99, +0.76]. Pick one, update other.

With those two fixes and the citation-tightening in §1.6 (drop Pal 2015, remove the Figueroa/Frank effective-representation lineage claim, remove unused Haig reference), the reports are publication-ready with appropriate caveats.

**Top 3 residual risks:**

1. **Citation overreach in §5.3.** Figueroa and Frank are §3 Charter cases but not effective-representation/redistribution cases. Pal (2015) is mis-cited as gerrymandering scholarship. A legal reader will catch this fast and it will undercut the academic report's authority.
2. **Chen-Rodden framing asymmetry between §3.6 and §7.** The synthesis table does not carry the natural-packing caveat that §3.6 introduces. The public report inherits this. Medium risk of partisan critique.
3. **Structural/vote-based blending** in the public report's 2019-tilt bullet (§1.4 above). The measurement is fine; the causal attribution rides on top without a label.

**Is the v1.2 prompt ready to execute in a new session?**

**No, not until two fixes:** (a) rename `check_wuff_voice.py`→`check_voice_and_readability.py` references in the prompt (or rename the script), and (b) correct the "no minority crosswalk" claim (line 23) to match the actual data inventory. Also reconcile the EG number (§1.1) so Gate G0 does not fail spuriously.

After those fixes, v1.2 can execute cold. Budget tightness (§2.5) and RT1 logic (§2.4) are tunings, not blockers.

---

*End of v0.2 final red-team. Clean-room execution should not begin until §1.1, §1.2, §2.1, §2.2 are resolved. The other material items (§1.3–1.6, §2.3–2.6) should be addressed in the same pass but are correctable in-flight if needed.*
