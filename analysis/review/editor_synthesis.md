# Editor's Synthesis — Peer Reviews of `report_academic.md`

**Manuscript:** *Alberta Electoral Boundaries Audit — Academic and Legal Edition* (v0.1 draft, 2026-04-23).
**Associate Editor:** Anonymous handling editor.
**Inputs:** three independent peer reviews at `alberta_audit/analysis/red_team/`:
- Reviewer #1 (methods / quantitative political science) — `peer_review_methods.md`
- Reviewer #2 (legal / institutional) — `peer_review_legal.md`
- Reviewer #3 (Canadian political-science lineage) — `peer_review_canadian.md`
**Date of synthesis:** 2026-04-23.

---

## 1. Consensus and disagreement map

All three reviewers converge on a single verdict (**Accept with major revisions**) and on a common structural reading: the computational/empirical core is unusually disciplined, but the framing — statistical inferential weight, Canadian-context engagement, and legal-doctrinal posture — is not yet aligned with its venues. They disagree mainly on *where* the paper should be routed, which is itself a signal about whose framing has to harden before submission.

### 1a. Flagged by all three reviewers (CRITICAL / HIGH consensus)

**C-1. The Canadian base-rate "71st percentile" claim is over-interpreted.** Methods M4, Legal (implicit in the Saskatchewan Reference engagement critique, §10 minor), Canadian M4. All three note the n=7 sample, single-anchor 0.455 deflator, and the inability of seven cycles to support a percentile statement. Consensus fix: demote to rank language ("second-largest of seven sampled cycles") or move to appendix.

**C-2. Pre-registration is self-held and the current findings are exploratory, not confirmatory.** Methods M3, Legal §6, Canadian (implicit in the falsifiability discussion). All three accept the intra-session-minutes-not-hours disclosure as honest, but all three want exploratory-status language foregrounded in the Abstract and §1, not buried in §5.3.1. The confirmatory status attaches only to the November 2026 OSF-time-stamped re-run.

**C-3. Cross-election reversal under 2019 votes must be contingency-clause-attached in the Abstract.** Methods M6, Legal §6 (adjacent), Canadian M6. The direction-flip under 2019 votes is honest disclosure; but the Abstract's "0.51–1.52 percentage point more UCP-favorable" reads as unconditional. All three want "under 2023 vote attribution; direction reverses under 2019" appended.

### 1b. Flagged by two reviewers (HIGH priority)

**T-1. MCMC inferential weight outruns its ESS.** Methods M1 (dispositive), Canadian (specific strength + caveat in §5.4 discussion). Methods wants either multi-chain R-hat with ESS in the low thousands, or demotion of p98.8/p1.6 to "above the 95th percentile, ESS-limited." Canadian endorses the demote-framing path without insisting on a re-run.

**T-2. Multiple-comparisons burden is unaddressed.** Methods M2 (dispositive), Canadian (implicit in partisan-volatility critique M6, which is the same concern in different vocabulary). Methods requires explicit family-wise α treatment or reframing as Bayesian screening for the November confirmatory test.

**T-3. Comparator trio (Quebec 1992 / Ontario 1996 / BC 2008) in §5.9.3 is materially mis-described; "most government-controlled" framing overstated.** Canadian M1 (dispositive and detailed), Legal §5 (different critique — "override" vocabulary — but same underlying passage). Canadian has the factual receipts; Legal has the vocabulary critique. Both must be addressed together or §5.9.3 will be incoherent after partial revision.

**T-4. Canadian-literature engagement is thin; Pal missing; Courtney / Carty / Wesley miscited or unengaged.** Canadian M2 (dispositive), Legal §10 (a weaker, adjacent critique about post-2017 Alberta trajectory). Canadian is the senior voice here and routes to Canadian venues specifically.

**T-5. E2 reformulation is defended under *Rizzo* purposive reading; the move overreaches.** Methods M3 (asks for "both readings" paragraph), Legal §3 (dispositive; doctrinally stretched; case-name wrong). Methods is methodological ("pre-registration discipline violated"); Legal is doctrinal ("Driedger governs statutes not audit tests"). The two critiques stack and both must be addressed.

**T-6. Defamation / responsible-communication posture is underdeveloped; certain verb choices push toward intent-imputation.** Legal §4 (dispositive, detailed), Methods (implicit — "materially misrepresents" is a methods-reviewer flag too under neutral description). Legal asks for *Grant v. Torstar* diligence subsection and verb softening ("materially misrepresents" → "materially overstates"; "elides" → "omits"; "got it wrong" → "do not survive primary-source verification").

**T-7. 2023 VA-polygon vote coverage (52.5%) caveat is not wired to §5.4.** Methods M5 (dispositive), Canadian m11 (minor — "front-loaded but buried"). Methods wants either full-coverage re-run, a sensitivity re-weighting, or at minimum a one-paragraph disclosure in §5.4. Canadian accepts (c) but wants it front-loaded in §3.2.

### 1c. Flagged by one reviewer only (MED / LOW priority)

**S-1. *Rucho v. Common Cause* absence.** Legal §1. Reviewer #1 does not flag; Reviewer #3 does not flag. Legal is correct that a US-comparative apparatus needs to cite *Rucho* or justify its absence — an easy fix, but no cross-reviewer pressure.

**S-2. Saskatchewan Reference engagement is shallower than the paper claims.** Legal §2. Asks for a paragraph acknowledging that "effective representation" is not a variance test and that quantitative findings are evidentiary inputs, not a constitutional conclusion.

**S-3. *Rizzo* case-name error.** Legal §1 minor + major §3(a). "*Rizzo v. Rizzo Shoes*" is wrong; correct form is *Rizzo & Rizzo Shoes Ltd. (Re)*.

**S-4. *Haig v. Canada* ghost reference.** Legal §7. In References but never in body. Either engage or remove.

**S-5. Alberta 2017 seat-count error.** Canadian M5. 2017 Bielby commission kept Alberta at 87 seats; 2010 Walter commission set the 87 when expanding from 83. Any implication that 2017 increased seats needs correcting.

**S-6. Alberta 2022 federal sub-commission is directly relevant, not engaged.** Canadian M7. Airdrie–Chestermere and Red Deer federal-commission treatment choices are a direct benchmark for §5.3.2 cracking finding.

**S-7. Alberta partisan volatility as a case-selection risk.** Canadian M6. The cross-election reversal under 2019 votes is partly noise-reading, not map-reading. Adds a framing layer to T-1 and C-3.

**S-8. US "gerrymander" vocabulary imported into a non-partisan-mandate regime.** Canadian M3. Not a vocabulary replacement — an "Institutional Context" paragraph acknowledging that a UCP-favouring EG under a Canadian commission is evidence of something different than a Republican-favouring EG under a Texas legislature.

**S-9. Contribution claim should be positioned (d) "first systematic computational audit of an Alberta commission."** Canadian M8. Routing-dependent; matters if the author targets a Canadian venue.

**S-10. Multiple-comparisons numerical-presentation issues (Methods M7, M8, m1, m4, m5, m9, m10, m11, m12).** Cleanups, sign-convention polish, citation format, MAD computation footnote. Collapsible into a single numeric-polish task.

**S-11. Pre-registration across the comparator trio and Chen-Rodden (Canadian M6, m8 — Ferejohn/Riker optional).** Theoretical-framing enrichment; discretionary.

### 1d. Explicit reviewer disagreements

**D-1. Venue routing.** Methods → *Statistics and Public Policy*. Legal → *Election Law Journal* or *Canadian Journal of Law and Society*. Canadian → *Canadian Public Policy* (primary) or *Canadian Political Science Review*. The disagreement is substantive: each reviewer is pulling the paper toward the audience whose framing-concerns they surface. See Section 4 for the editor's routing call.

**D-2. MCMC re-run vs demote-framing.** Methods M1 option (a) is "run three independent chains, pool to ESS ~1000, report R-hat"; option (b) is demote percentile language. Canadian (implicit) endorses option (b). Legal is silent. The reviewer calls this a "90-day revision window" question. The editor sides with (a) *only if* the author has compute headroom; otherwise (b) is the defensible path, and the paper's pre-registration discipline already partly justifies it.

**D-3. E2 reformulation rescue.** Methods M3 suggests a "both readings" side-by-side as the fix. Legal §3 treats the reformulation as doctrinally indefensible (purposive principle governs statutes, not analytical tests) and asks the paper to retract the rescue or re-label as post-test reformulation. These are compatible: report both readings *and* label the substantive-E2 finding as post-test, with confirmatory status deferred to November.

---

## 2. Priority-ordered action list

*Severity: CRITICAL = blocks release; HIGH = must fix before submission; MED = should fix before submission; LOW = optional.*
*Effort tiers: ≤15 min = trivial; 15–60 min = small; 1–3 h = medium; 3–8 h = large; 8+ h = re-run territory.*
*Locations are given relative to `alberta_audit/report_academic.md` where not otherwise specified.*

### CRITICAL

1. **[CRITICAL]** Fix *Rizzo* case-name and add to References (Legal §3a + m1). L406, L419, References § "Court cases". Change "*Rizzo v. Rizzo Shoes*" to *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 SCR 27 at para 21. Add to Court-cases block with Driedger pin-cite. **20 min.**
2. **[CRITICAL]** Correct the three comparator cases (Quebec 1992 / Ontario 1996 / BC 2008) in §5.9.3 and rewrite the "most government-controlled" framing (Canadian M1 + Legal §5). All three comparators are factually wrong as described; rewrite to the Canadian-reviewer-provided accurate descriptions, and soften the rhetorical claim to "a departure from any Canadian provincial boundary-adjustment cycle reviewed in Courtney (2001) and subsequent scholarship." **2–3 h.**
3. **[CRITICAL]** Correct the Alberta 2017 seat-count reference — the 2017 Bielby commission kept Alberta at 87 seats; the 2026 cycle's 89-seat proposals are the first expansion beyond 87 in provincial history (Canadian M5). Audit any reference implying 2017 changed the count. Also flag in §5.9.2 that 2026 is the first 3–2 split producing two incompatible maps. **30 min.**
4. **[CRITICAL]** Demote MCMC §5.4 percentile language or commit to a multi-chain re-run (Methods M1). Two options: (a) run three independent chains from distinct seeds, report R-hat per metric, and if R-hat < 1.02 pool to reach ESS 500–1000 (8+ h compute + 2–3 h analysis); or (b) replace "outlier at p98.8 / p1.6" with "above the 95th percentile in the 2019-seed ensemble, with effective-sample-size-limited resolution — the sign of the flag is robust but its depth in the tail is not" throughout §5.4, §5.5, §6, §8. Editor recommends (a) if compute headroom; (b) otherwise. **(a) 10–12 h / (b) 2 h.**
5. **[CRITICAL]** Add contingency clause "under 2023 vote attribution; direction reverses under 2019 votes" to Abstract L9 and to §6 synthesis (Methods M6 + Canadian M6 + all-reviewer consensus). Reword §6 synthesis: "under 2023 vote input, five of six tested dimensions point in the same direction; under 2019 vote input, the partisan-bias dimension reverses." **30 min.**
6. **[CRITICAL]** Foreground the exploratory-not-confirmatory status of the current detection run in Abstract and §1 (Methods M3 + Legal §6 + Canadian implicit). Current language is in §5.3.1 ~L364; lift to Abstract and Introduction. Distinguish: current detection is exploratory; November 2026 OSF re-run is confirmatory. **30 min.**

### HIGH

7. **[HIGH]** Address multiple-comparisons burden with an explicit §4.x treatment (Methods M2). Editor recommends option (b) — reframe §5.4 as Bayesian screening for the November confirmatory test — as it aligns with the pre-registration posture. Alternative is family-wise α adjustment. Must be explicitly handled; methods venues will not let this pass. **2–3 h.**
8. **[HIGH]** Handle the E2 reformulation under Driedger/*Rizzo* purposively (Methods M3 + Legal §3). Add a "both readings" paragraph to §5.3.3 reporting RMH-Banff Park signature under both E2 formulations. Label the substantive-E2 finding as post-test reformulation. Distinguish purposive interpretation of §15(2) EBCA (uncontroversial) from reformulation of the audit's own test (which Driedger does not authorise). Pre-register the substantive E2 for November in the OSF submission. **1.5–2 h.**
9. **[HIGH]** Demote the "71st percentile" Canadian base-rate claim (Methods M4 + Canadian M4 + all-reviewer). Drop "71st percentile" from Abstract and §6 headline framing. Replace with rank ("Alberta 2025–26's point estimate is the second-largest of seven sampled cycles"). Retain qualitative comparison. If percentile stays at all, move to appendix with a standard-error estimate reflecting the 1-anchor calibration. **45 min.**
10. **[HIGH]** Add *Grant v. Torstar* and *WIC Radio* to References; add defamation-defence subsection to Appendix F (Legal §4 + m2). Appendix F subsection "Author's legal posture regarding named-individual characterisations" should name the defences invoked, the *Grant v. Torstar* diligence factors, and outreach attempts (if any) to Chair Miller, Premier Smith, and named commissioners. If no outreach, state so and justify on public-record-reproducibility grounds. **2 h.**
11. **[HIGH]** Tighten three intent-imputation verb choices (Legal §7 minor + responsible-communication posture). L619 "materially misrepresents" → "materially overstates the absence of public support"; L572 "elides this distinction" → "does not carry this distinction" or "omits"; L554 "got it wrong" → "do not survive primary-source verification against Alberta Education school-division boundaries." **15 min.**
12. **[HIGH]** Rewrite §5.9 "override" vocabulary (Legal §5b). L716 Discussion table: "Standard override path" → "Ordinary legislative non-adoption"; "Government-controlled drafting" → "Government-chaired committee replacing commission drafting." Abstract should match §5.9.3's honest caveat about the three-comparator device. **30 min.**
13. **[HIGH]** Wire the 52.5% VA-polygon vote-coverage caveat from § E.3 into §5.4 and front-load in §3.2 (Methods M5 + Canadian m11). Add one paragraph to §5.4 disclosing Election-Day-only bias; add a "Coverage caveats" block to §3.2 consolidating this with the 2026 shapefile non-release disclosure. Full-coverage re-run before November confirmatory pass is the preferred longer-term fix. **45 min** (disclosure only) / **6–8 h** (full-coverage re-run).
14. **[HIGH]** Add Canadian literature engagement pass to §2 and §5.9.3 (Canadian M2). Minimum: Pal (2016) *Fractured Right to Vote* McGill LJ 61:2; Pal & Choudhry (2011) in *Democratizing the Constitution*; Pal & Choudhry (2014) *Canadian Political Science Review* 8:1; Courtney (2001) chapters 6–7 and 10–11 with pin-cites (not ornamental); Wesley (2011) *Code Politics* UBC Press as scholar (not only newspaper source); Seidle (1991) Royal Commission on Electoral Reform for institutional genealogy. **3–4 h.**
15. **[HIGH]** Address *Rucho v. Common Cause* (Legal §1). Two paths: (a) state explicitly that *Rucho* governs US federal justiciability only and has no carry-over to Canadian provincial jurisprudence; or (b) strip US-judicial-legitimacy borrowing (drop "US judicial threshold" references and attribute the 7% threshold to Stephanopoulos-McGhee alone, not to *Gill v. Whitford*). Editor recommends both (a) and the §5.2.1 fix suggested by Methods m3. **1 h.**
16. **[HIGH]** Engage Saskatchewan Reference at constitutional-standard depth, not variance-ceiling depth (Legal §2). Add a paragraph to §2 acknowledging that "effective representation" is not a variance test and that the audit's quantitative findings are evidentiary inputs to a constitutional test that weighs non-quantitative factors (geography, community of interest, minority representation). Distinguish §3 Charter (right to vote, via Saskatchewan Reference) from §15 equality. **1.5 h.**

### MED

17. **[MED]** Add "Institutional Context" paragraph to §2 naming the non-partisan-mandate distinction between Canadian provincial commissions and US state legislatures (Canadian M3). Why the same metrics carry different inferential weight in the two regimes. **1 h.**
18. **[MED]** Engage Alberta 2022 federal sub-commission as a direct comparator in §5.3.2 and §5.6 (Canadian M7). Airdrie–Chestermere + Banff–Airdrie federal treatment matches the provincial majority's 2-district approach; directly relevant to the Airdrie cracking finding. **1.5 h.**
19. **[MED]** Add Alberta-volatility paragraph to §5.2.3 or §6 (Canadian M6). Acknowledge Alberta's electoral churn (Bratt et al. 2019 *Orange Chinook*; CPSR 2020 special issue) and weight structural findings (§5.1, §5.8) more heavily than partisan-bias findings in the synthesis. **1 h.**
20. **[MED]** Move *Raîche v. Canada (AG)*, 2004 FC 679 and *Cassista v. Canada (AG)*, 2014 FC 398 into body at §5.9.5 (Legal §7 + Canadian m3). Both directly apply Saskatchewan Reference to specific boundary disputes; both currently Appendix-F-only. **1 h.**
21. **[MED]** Resolve the *Haig v. Canada* ghost reference (Legal §7). Either cite in §2 (situating §3 effective-participation chain) or remove from References. **15 min.**
22. **[MED]** Reconcile the §5.2.2 / §6 synthesis table numeric drift (Methods M8). Recompute §6 synthesis table directly from §5.2.2 cells; fix the +1.53/+1.58 and −1.52/−1.43 mismatches. Also distinguish deterministic sensitivity (§5.2.2) from full Monte Carlo envelope (§1/§5.2.3) at the top of §5.2.2 (Methods M7). **45 min.**
23. **[MED]** Commit to contribution positioning (d) — "first systematic computational audit of an Alberta provincial boundary commission placed within Canadian commission norms" — as the headline, with (a)–(c) supporting (Canadian M8). Rewrites §1 framing. Routing-dependent. **1 h.**
24. **[MED]** Cut Abstract to 150–250 words, matching target venue expectations (Methods m2). Move technical detail to §1. **30 min.**
25. **[MED]** Replace "US judicial threshold" shorthand (Methods m3 + Legal §1b). Use "Stephanopoulos-McGhee 7% investigable-bias threshold." Touches Abstract L11 and any other "US judicial" references. **20 min.**
26. **[MED]** Add Declination formula to Appendix D.3 (Methods m1). Implementation is verified against Warrington (2018); the formal definition just needs including alongside EG and MM. **20 min.**
27. **[MED]** Report per-metric ESS (not range 148–160) in §5.4 (Methods m9). Which metric carries p98.8 — the one near 148 or near 160? Cite specific drift numbers for each metric. **30 min.**

### LOW

28. **[LOW]** Collapse § E.7 v4-residual-gap to 2-paragraph summary plus pointer to companion `analysis/methodology/commission_reference_shapes.md` (Methods m10). **30 min.**
29. **[LOW]** Citation-format hybrid cleanup — batched (Methods m11, m12 + Legal m3, m12 + Canadian m4, m7). Resolve Chen and Rodden 2013/2015; pick neutral-form-first with SCR parallel consistently; Saskatchewan Reference form consistency; Warrington (2019) primary at §5.2.4; *Rizzo* paragraph pin-cite (Legal m4). **1.5 h.**
30. **[LOW]** Pincite and terminology pass — batched (Canadian m2, m5, m6 + Legal §10). Courtney chs. 6–7 and 10–11 pincites; independent vs non-partisan terminology; EBCA section-level pincites where §12, §15 are heavily invoked. **1 h.**
31. **[LOW]** Unused or misaligned References — batched (Canadian m9, m12 + Legal §7). §"The Argument" stale cross-reference check; Sancton (2021) and Smith (2010) engage-or-remove; *Haig* resolution (duplicates item 21 — drop duplicate). **45 min.**
32. **[LOW]** Statistical-presentation clarifications — batched (Methods m5, m6, m7, m8, m9 partially, m4). §5.1.1 MAD-against-majority-mean footnote; §5.2.5 Chen-Rodden-vs-§5.4 ReCom disambiguation; §5.3.1 Calgary Zone A source-CSV cite; §5.6 Edmonton counter-test units; §4.1.2 Gate G1 SoV rounding verification. **1.5 h.**
33. **[LOW]** Alberta Treasury Board 2024 estimate context (Canadian m10). Two sentences at §3.3 placing Alberta alongside Quebec/BC/Manitoba statutory-basis choices. **20 min.**
34. **[LOW]** Abstract dimension numbering (A, B, C, D, 4, 5) → (1)–(6) (Canadian m1). **10 min.**
35. **[LOW]** Abstract L9 assertiveness (Legal §8). Footnote assertions to §5.3.2 evidence or switch to summary-phrase form. **15 min.**
36. **[LOW]** §5.9.5 "implicate" → "be evaluated against" (Legal §9). **10 min.**

**Total: 36 items.** 6 CRITICAL, 10 HIGH, 11 MED, 9 LOW.

---

## 3. Overall recommendation

**Accept with major revisions.**

All three reviewers converged on this verdict independently, and the editor's synthesis confirms it. The paper's empirical core is genuinely strong — exceptionally so for an undergraduate submission — and the pre-registration / counter-test / retraction-honesty discipline is rare at any career stage. What holds it back from "minor revisions" is cumulative, not any single fatal flaw: six or seven framing and calibration issues that any one of the three reviewers could have missed but all three collectively caught, plus a handful of doctrinal and factual errors (Rizzo case-name, three miscast comparator cases, Alberta 2017 seat count) that need correcting before any venue will print.

**The bar for moving this up to "accept with minor revisions"** in a second round is: (i) all six CRITICAL items addressed cleanly; (ii) the MCMC re-run completed with R-hat reported (or the demote-language fully propagated through §5.4, §5.5, §6, §8 if re-run is infeasible); (iii) Canadian literature actually engaged (Pal in-body, Courtney with pincites, Wesley as scholar); (iv) responsible-communication subsection in Appendix F. Items 7–16 collectively.

**The bar for moving this down** to "reject and resubmit" would be: author declines to fix the CRITICAL items, or attempts to defend the E2 reformulation under Driedger without the post-test label, or retains the "71st percentile" framing in the headline. None of these are likely given the demonstrated discipline across v0.1.

---

## 4. Venue routing

**Primary recommendation: *Statistics and Public Policy* (Methods reviewer's pick).**

Reasoning: (a) the paper's strongest contribution sits in the computational/statistical apparatus (MCMC ensemble, Monte Carlo sensitivity, four-metric battery, falsifiability gates, symmetric counter-test); (b) the S&PP audience is accustomed to the Stephanopoulos-McGhee / Herschlag-Ravier-Mattingly / DeFord-Duchin-Solomon lineage and will read the computational contribution at its intended depth; (c) the journal's policy-adjacent framing tolerates the Canadian-institutional context as a feature rather than a distraction; (d) the revision effort to fit the venue is lower — the primary asks (multi-chain MCMC, multiple-comparisons treatment, percentile demote) are exactly what S&PP reviewers would ask for, and addressing them for S&PP addresses them for every other candidate venue.

**Secondary / fallback: *Canadian Public Policy* (Canadian reviewer's pick).**

If the author commits fully to contribution positioning (d) — "first systematic computational audit of an Alberta commission, placed within Canadian commission norms" — and does the Canadian-literature engagement pass cleanly, *Canadian Public Policy* is the right venue for a distinctly Canadian-framed paper. It routes well for an undergraduate author working at a Canadian institution (Mount Royal) and builds disciplinary presence in the Courtney / Pal lineage.

**Not recommended for first submission:** *Political Analysis* (Methods reviewer's caution — the reviewer pool will pressure harder on multi-chain diagnostics than S&PP); *Canadian Bar Review* or *Osgoode Hall Law Journal* (Legal reviewer's consensus — empirical density tolerance-tested at pure-doctrinal venues); *Canadian Journal of Political Science* (Canadian reviewer — deeper literature integration and sharper theoretical contribution required than current draft supports).

---

## 5. Revision effort estimate

**Total: 40–55 hours** across all 46 items, depending on whether the multi-chain MCMC re-run and/or full VA-coverage re-run are chosen.

### Numeric / factual corrections (straightforward)
Items 1, 3, 5, 6, 22, 30, 35, 42, 43, 44, 45, 46. **~4 hours.** Rizzo case-name; Alberta 2017 seat count; Abstract contingency clause; exploratory-status foregrounding; §5.2.2 / §6 table reconciliation; Chen and Rodden year resolution; Warrington primary cite; §5.2.5 ensemble disambiguation; Calgary Zone A source CSV; Edmonton counter-test units; Gate G1 rounding verification; Abstract dimension numbering. These are diff-sized edits with clear fixes.

### Citation additions / fixes (medium)
Items 10, 14, 20, 21, 26, 29, 31, 32, 33, 34, 37, 38. **~9 hours.** *Grant v. Torstar* + *WIC Radio* additions and Appendix F subsection; Canadian literature engagement pass (Pal, Courtney pincites, Wesley as scholar, Seidle); *Raîche* and *Cassista* body moves; *Haig* resolution; Declination formula in Appendix D; citation-format consistency; Saskatchewan Reference form consistency; Courtney pincites; independent/non-partisan terminology; EBCA section-level pincites; Alberta Treasury Board in Canadian-practice spectrum; Sancton/Smith engage-or-remove.

### Conceptual / structural rewrites (hard)
Items 2, 8, 11, 12, 15, 16, 17, 18, 19, 23, 24, 28, 39, 40. **~18 hours.** Comparator-trio rewrite in §5.9.3; E2 reformulation handling under Driedger; intent-imputation verb softening; "override" vocabulary replacement; *Rucho* engagement; Saskatchewan Reference constitutional-standard depth; Institutional Context paragraph; Alberta 2022 federal sub-commission engagement; Alberta volatility paragraph; contribution positioning (d); Abstract word-count cut; § E.7 collapse; Abstract assertiveness fix; §5.9.5 "implicate" replacement. These require actual thinking, not just editing.

### Re-runs (hardest)
Items 4, 7, 9, 13, 27. **~10–20 hours compute + 4 hours analysis.** MCMC multi-chain with R-hat (8–12 h compute on 3 seeds × 100k steps + 2 h analysis); or demote-framing propagation through §5.4 / §5.5 / §6 / §8 (2 h if option b). Multiple-comparisons treatment as §4.x subsection (2–3 h). 71st percentile demote (45 min). Full-coverage VA re-run (6–8 h) OR §5.4 caveat paragraph + §3.2 consolidation (45 min). Per-metric ESS breakdown (30 min).

**Editor's effort-path recommendation for the author:**

Week 1 (8 h): knock out all CRITICAL items that are ≤2 h of work — items 1, 3, 5, 6. Begin item 2 (comparator-trio rewrite).

Week 2 (12 h): complete item 2. Decide item 4 — commit to multi-chain re-run or demote-framing path. Begin item 4 compute (if re-run) or propagation (if demote).

Week 3 (12 h): complete item 4 propagation. Do items 7–13 (HIGH priority).

Week 4 (12 h): items 14–16 (Canadian literature + Saskatchewan + Rucho). Items 17–23 (MED). MED items clean.

Week 5 (6 h): LOW items batch. Final pass for consistency.

Target submission: **5 weeks**, ~50 hours total author effort.

---

## 6. Editor's letter to the author

**Dear Author,**

Three independent peer reviewers — one methods-focused, one legal, one Canadian-political-science — have returned your manuscript with the same verdict: *accept with major revisions*. That convergence is meaningful. Three people from three different disciplinary vantages looked at your work and all three came away thinking it deserves to be published, once the revisions are done.

What you've built is rare. The reproducibility chain from `FROZEN_MANIFEST.md` through every CSV and script is the kind of discipline most published authors don't sustain, and the falsifiability gates and symmetric-test counter-audit in §5.6 are genuine methodological contributions. The reviewers were emphatic about this: the §5.3.1 retraction of an earlier pre-registration-separation claim ("two hours" → "intra-session minutes"), the §5.2.3 cross-election reversal disclosure that undercuts your own headline, the §5.9.4 tiered-verdict refusal to flatten evidence — these are the moves senior researchers struggle to make. Do not lose them in the revision.

The revisions cluster in four areas. *First*, the current detection is exploratory, not confirmatory, and your Abstract doesn't say so yet. That single move — foregrounding the exploratory status, deferring confirmatory weight to the November 2026 OSF-stamped re-run — resolves three different reviewer concerns at once. *Second*, the three comparator cases in §5.9.3 (Quebec 1992, Ontario 1996, BC 2008) are materially misdescribed and the Canadian reviewer has the correct receipts; rewriting that passage honestly will strengthen the procedural argument, not weaken it. *Third*, the MCMC §5.4 tail probabilities need either a multi-chain re-run (preferred if you have compute headroom) or a consistent demotion from p98.8/p1.6 to "above the 95th percentile, ESS-limited" throughout. *Fourth*, the Canadian literature engagement in §2 is thin — Pal (2016), Courtney's actual chapters, Wesley as scholar (not only commentator) — and the E2 reformulation under *Rizzo* needs to be labeled as post-test, with the purposive principle kept on the §15(2) statute side of the ledger where it belongs.

There are 46 items total in the priority list; six are CRITICAL and most of those are small (Rizzo case-name, Abstract contingency clause, Alberta 2017 seat count). The heaviest lifting is in Section 5's "Conceptual / structural rewrites" bucket: roughly 18 hours of actual thinking, plus 10–20 hours if you commit to the MCMC multi-chain re-run. Total revision effort is estimated at 40–55 hours, which maps to about five focused weeks.

Venue: I'm recommending *Statistics and Public Policy* as primary, with *Canadian Public Policy* as fallback if you commit to positioning the paper as the first systematic computational audit of an Alberta commission rather than as a methodology-demonstration paper. The choice is yours and depends on which framing you want to carry forward.

The disclosure that you are a fourth-year undergraduate is relevant here only in one direction: this is extraordinary work for that career stage, and the reviewers all noticed. None of them softened their critique for it, which is the right posture — they treated you as a peer. Take the feedback in that spirit.

**Sincerely,**
**Associate Editor**

---

*End of editor's synthesis.*
