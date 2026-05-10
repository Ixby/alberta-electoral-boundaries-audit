# Six Thinking Hats Analysis — Alberta Electoral Boundary Audit
## Pass 4: The TODO List as a Project Management Problem

*Framework: Edward de Bono's Six Thinking Hats. Pass 4 focuses not on what the audit found or whether the science holds, but on the TODO list itself — the project's current operational state, what is demanded of a solo undergraduate in a compressed window, and what decisions about prioritization reveal.*

---

## WHITE HAT — What the TODO List Actually Says

### Volume and classification

The TODO.md contains approximately 60 distinct named items across five priority tiers (CRITICAL, HIGH, MEDIUM, LOW, Date-Gated), plus a weekend-action table subdivided into "Do before Monday" and "Do if time." The effort estimates, where given, aggregate to:

- Monday prep block: ~7–9 hours across all listed items
- Peer review remediation (ES-01 through ES-36): 40–55 hours stated
- Computational pipeline (C1): 1–2 days
- Red-team code corrections: not estimated, listed as five deferred HIGH findings
- Restructure/hygiene: 18–24 hours, PO-triggered

Total enumerable hours (rough): 75–100 hours of identified work, excluding the sentiment analysis corpus (~218/1,252 complete) and Phase 4C GIS work blocked on C1.

### What is done versus what is open

Six items are explicitly marked DONE in the critical section (CRIT-A through CRIT-C, HIGH-D, HIGH-E, D1–D5, S1–S3, S1-01). This is meaningful — the project has cleared its most severe data-integrity errors. The remaining open CRITICAL items are: HIGH-A (2019 cross-election asymmetry recomputation), HIGH-B (Monte Carlo footnote), HIGH-C (submission count reconciliation), MED-A (plurality-of-Albertans claim), and S4 (small-N noise floor, estimated 20 minutes). The S2-02 item (MCMC full-coverage rescore) is listed under CRITICAL but has no completion marker — it requires updating §3.11 headlines with corrected p-values across four metrics.

### The Monday constraint

Group chat review is Monday, 2026-05-12 — two days from today. The TODO draws a hard line between weekend work and deferred work. Nine items are flagged "Do before Monday" with a combined estimate of ~4–5 hours. Four more items are "Do if time" at ~3–4 hours. The deferred list (ES-07, ES-14, ES-16, ES-10, C1, S2-02) is not described as low-priority — it is described as too large to attempt in the available window.

### The C1 dependency chain

Item C1 (advance-vote splat computation, 1–2 days) is the single most consequential open item structurally. It blocks: G3 (GIS), Phase 4C Stages 4–7, the Fisher empirical independence check (which is a hard submission stop per the TODO), and the VA-to-ED substrate needed for several ES items. C1 also closes a 47.5% missing-vote gap. The TODO correctly identifies C1 as HIGHEST under Computational Pipeline.

### What Duane Bratt's reply does and does not change

The TODO records that Bratt replied 2026-05-09. It does not record what he said, what he committed to, or whether review is confirmed. The pre-review priority list (ES-02, ES-13, ES-14, ES-17, ES-19) is still entirely open. These items are not in the Monday prep block. This is significant: the audit is preparing for group chat review without having completed the items identified as prerequisites for institutional review.

### Pre-registration status

Four OSF registrations (w2s8k, r3zm7, qsgy8, 6pt83) are submitted and verified. The TODO notes an OSF provenance disclosure gap: Ch1/Ch2 are not named in any OSF files. This is an open external blocker — it is not in any of the weekend fix tables.

---

## RED HAT — Gut Reactions to This List

Reading this TODO produces a specific feeling: the project is administratively tidy and substantively overwhelmed. The table formatting is clean. The ES numbers are sequential. The effort estimates are credible. And yet the aggregate demand — 75–100 hours of remaining work for a solo author who also has a Monday review in 48 hours — reads as the kind of list that exists to make an impossible workload legible, not to make it achievable.

There is something uncomfortable about the gap between the "Do before Monday" block and the "Peer Review Remediation" block. The items flagged for Monday are, by design, the easiest ones — prose corrections, citation fixes, label changes. The hardest items (ES-07, ES-14, ES-16, ES-10, C1) are deferred. This is tactically correct. It also means the document going into Monday review is still carrying its most significant scientific weaknesses: the E2 reformulation both-readings problem (ES-08), the comparator-trio (ES-02), the Canadian literature gap (ES-14), and the MCMC headline rescore (S2-02).

The Fisher independence check being a hard submission stop while blocked on C1 (1–2 days) creates a specific anxiety. The project cannot submit as long as fisher_independence_defense.md shows "pending," and the thing that would unblock it is the largest single computational task on the list.

The sentiment analysis corpus — 218 of 1,252 complete as of May 9 — feels like a background process that the main analysis is not waiting on. But "cleanup, re-classify, Hansard, forensic pipeline, cross-reference all pending" after 218 completions is not a small trailing task. It is most of the work.

The list also triggers a reaction to the phrase "Red-Team Code Corrections — Five HIGH findings deferred: magic-number bounding boxes, mixed RNG sources, 2015 region classification error-bounds, Chrome hardening, suppressed-DA uncertainty." These are code correctness issues, not prose issues. Deferring them is defensible in a pre-Monday context. It is less defensible in a pre-submission context. Their presence as a permanent section without resolution dates is a quiet admission that the codebase has known quality gaps.

---

## BLACK HAT — Risk, Gaps, and Failure Modes

### The solo-author scaling problem

A 75–100 hour TODO carried by one person with a 48-hour hard deadline before group review is a structural risk. The Monday prep block assumes ~5 hours of uninterrupted focused editing. If that estimate is off by 50% — which is normal for academic prose revision — the "Do if time" block evaporates. ES-08 (E2 both-readings paragraph, 1.5–2 hours, which is also under CRITICAL in the peer review section) would not get done before Monday. That item is among the most likely to draw questions from an academic reviewer.

### The MCMC headline problem

S2-02 is listed in CRITICAL but has no completion date and is deferred from the Monday block. The §3.11 headlines currently contain numbers that are wrong by the TODO's own accounting: the minority mean-median p100 → p98.76, seats@50/50 p95+ → p94.27 (below the 95 threshold), majority mean-median p6.6 → p92.66, majority seats@50/50 at p57.86. These are not rounding errors. The minority seats@50/50 crossing below the 95 threshold changes the interpretive claim. If Bratt or another reviewer reads §3.11 before S2-02 is resolved, the audit's central MCMC claim is vulnerable.

### The E2 reformulation transparency gap

ES-08 requires showing RMH-Banff under both the original E2 formulation and the substantive reformulation, with the reformulation labeled explicitly. This item is in the Monday "Do if time" block but is also CRITICAL in the peer review section. The fact that E2 was reformulated mid-audit after the initial formulation failed detection is known to the author and disclosed in-document, but only implicitly. If it is not shown explicitly with both readings before Bratt's review, it will almost certainly be raised as a concern about researcher degrees of freedom.

### The comparator-trio exposure

ES-02 requires dropping all three current international comparators (Quebec 1992, Ontario 1996, BC 2008) and anchoring to Quebec 2024 and the SCC April 22 ruling. The TODO classifies this as CRITICAL. It is in the "Do if time" block for the weekend, meaning it may or may not happen before Monday. If it does not happen, the audit goes into group review with three comparators the TODO itself acknowledges are misdescribed. A political scientist reviewing comparative cases is likely to catch this.

### The submission blocker chain

The Fisher independence check is a self-declared hard submission stop. It is blocked on C1. C1 is a 1–2 day computational task that has not started. The Fisher check has downstream dependencies on the VA substrate. This chain means the project cannot submit under its own stated criteria until at minimum 3–4 days of work are completed after C1 begins. There is no start date for C1 in the TODO.

### The OSF gap

OSF pre-registrations cover the 17-test November grid but do not name Ch1/Ch2. This is listed under External Blockers without a resolution plan. If a reviewer checks the OSF record against the paper's claims, the provenance gap is visible. The TODO does not assign this item to anyone or give it an effort estimate.

### The sentiment corpus completion gap

78/1,252 (6.2%) complete means the sentiment analysis results in the current report are based on a very small fraction of the corpus. If the LLM scan surface at 100% changes the distribution of coded responses, any claims currently in the report that depend on submission sentiment are at risk. The TODO notes this is "in progress" but does not estimate when it will be complete or what the plan is if findings shift.

### The Canadian literature gap

ES-14 (Pal, Wesley, Courtney pin-cites) is deferred post-Monday with a 3–4 hour estimate and PRE-REVIEW PRIORITY status. Bratt, who replied 2026-05-09, is a political science department chair whose work engages Alberta legislative politics. The probability that he notices the absence of engagement with the Canadian electoral administration literature is high. Deferring this item past Monday review, when Bratt may already be reading, is a sequencing risk.

---

## YELLOW HAT — What the List Does Well

### The triage structure is honest

The TODO distinguishes cleanly between what is achievable before Monday, what is achievable before submission, and what is deferred to post-review. Many project management documents of this type obscure the gap between the two. This one does not: the deferred items are named, their effort is estimated, and they carry their priority labels. A reader can reconstruct the true scope of remaining work without having to infer it.

### DONE items are marked and timestamped

D1–D5, S1–S3, CRIT-A through CRIT-C, HIGH-D, HIGH-E are all marked with their completion dates. This is good epistemic hygiene. It prevents re-doing completed work and makes it possible to audit progress over time. The May 9 completion cluster represents a real burst of remediation work and should be credited as such.

### The C1 dependency is correctly identified

The TODO correctly flags C1 as the critical path item — HIGHEST priority, explicitly listed as blocking four downstream items. This kind of dependency identification prevents wasted effort: it would be counterproductive to work on Phase 4C Stages 4–7, G3, or the Fisher check before C1 is resolved. Having the block structure visible in the document protects against exactly that failure.

### The pre-registration grid for November is the project's strongest asset

The 17-test prospective scoring grid, committed for the November 2, 2026 Lunty committee map, is the most credible scientific contribution in the project. The TODO does not describe it as needing work — it is in place. The four OSF registrations and the AsPredicted records are submitted and verified. Whatever weaknesses the Phase 1 retrospective analysis carries, the prospective November analysis has pre-commitment that makes it robust to degrees-of-freedom concerns. The TODO correctly treats this as background infrastructure rather than as outstanding work.

### The Monday prep block is realistically scoped

Nine items in ~4–5 hours is tight but achievable. The individual items are correctly described as prose corrections and short insertions. ES-24 (abstract word count), ES-25 (judicial threshold language), ES-01 (Rizzo case name), ES-34 (label fix), ES-26 (declination formula) are all sub-30-minute tasks that compound into a meaningfully improved document. This is good sprint design: achievable in the time available, materially improves the product going into review.

### The red-team code findings are documented

Having five HIGH code findings documented by name — even in a deferred state — is better than not having them documented. The project knows about the magic-number bounding boxes, the mixed RNG sources, the 2015 classification error-bounds, the Chrome hardening issue, and the suppressed-DA uncertainty. These are not hidden. A reviewer who asks about code quality can be pointed to a named list of known issues with disclosed status.

---

## GREEN HAT — Alternatives, Reframings, and Creative Options

### Reframe the Monday review objective

The Monday group chat review does not have to be a full document review. One option: frame it explicitly as a methodology review only — put §3 (MCMC), §4 (Monte Carlo), and §5.4 (VA coverage) in front of reviewers and ask specifically about those sections. This concentrates the review on the parts the author most needs external eyes on, and protects against reviewers encountering the misdescribed comparator trio (ES-02) or the MCMC headline errors (S2-02) before those items are fixed.

### Start C1 as a background process

C1 (advance-vote splat, 1–2 days) is the longest-pole item and the most consequential blocker. There is no reason it cannot start running during the weekend while prose corrections happen in parallel. If C1 is a computational pipeline rather than a manually intensive task, setting it running Friday night and picking up the output Sunday removes it from the critical path before Monday. The TODO does not say C1 requires full-time supervision. If it does not, parallelization is the correct move.

### Collapse S2-02 into the Monday prep block

S2-02 (MCMC headline rescore) is listed as CRITICAL but deferred from Monday prep. The corrected values are already known — they are in the TODO itself: p98.76, p94.27, p92.66, p57.86. Updating §3.11 headlines is a find-and-replace operation with four known substitutions. This could be 20–30 minutes, not an open research task. Treating it as deferred is unnecessarily conservative.

### Write the OSF disclosure gap as a note in the paper

The OSF gap (Ch1/Ch2 not named in any OSF files) is an External Blocker with no resolution plan. One option that does not require retroactively modifying OSF records: add a disclosure note to the paper itself — "Ch1 and Ch2 analyses were conducted prior to formal OSF registration; pre-registration covers the prospective 17-test grid for the November 2026 map." This converts the gap from a hidden provenance problem into a disclosed limitation, which is the standard academic handling of pre-registration scope mismatches.

### Separate the Bratt engagement from the group chat review

If Bratt's reply was received May 9 and the status of engagement is unclear, there is time before Monday to clarify. Specifically: before sending anything for Bratt's formal review, complete at minimum ES-02, ES-14, ES-17, and ES-19, which are the four items the TODO already flags as PRE-REVIEW PRIORITY. If Bratt is not yet reading the document — if his reply was an initial response rather than a review comment — the window still exists to complete those items before they become live vulnerabilities.

### Create a two-column submission status table

The TODO's current structure mixes "what is wrong" with "when it will be fixed." A simple two-column table — Blocker | When Resolved — would make the submission readiness state immediately legible. Currently, determining whether the project is submission-ready requires reading across four separate sections and inferring which done-items close which blockers. A single table would also make the Fisher stop condition and its C1 dependency visible at a glance.

---

## BLUE HAT — Process, Sequencing, and What the List Tells Us About the Project's State

### The list is doing two jobs simultaneously

The TODO is simultaneously a pre-Monday sprint plan and a pre-submission audit log. These are different documents with different audiences and different time horizons. As a sprint plan, it is appropriately scoped and honest about tradeoffs. As a submission audit log, it is incomplete — it does not have resolution dates for most items, does not have a clear path from current state to submission-ready, and does not model the dependencies between items in a way that would let a third party reconstruct the critical path. Both documents should exist. Only one currently does.

### The project's operational mode is reactive triage, not staged completion

The structure of the TODO — items added as they are discovered, grouped by source (peer review, red-team, computational, GIS, Monday review), prioritized within groups but not across groups — reflects a project that is managing discoveries as they arise rather than executing against a pre-committed completion plan. This is not a criticism of the author; it is the normal state of an independent audit under time pressure. But it means the "when does this end" question is not answered anywhere in the document. The November 2 date-gate drives Phase 2 (Lunty map), not Phase 1 submission.

### Monday is a quality gate, not a deadline

The Monday review is described as a "group chat review" with no formal deliverable attached. The TODO's framing — "these items require no new research" — correctly identifies it as a polish sprint. But a group chat review is only a quality gate if reviewers are qualified, engaged, and willing to raise issues. The TODO does not describe who else is in the group. If the group does not include the institutional reviewers (Bratt, Nguyen, Moorman), Monday's review is a peer support function, not a scientific quality gate. This affects how much weight to put on getting items done before Monday vs. getting items done before institutional review.

### The sentiment analysis deserves explicit status

218/1,252 at approximately May 9 with no completion estimate is a significant open corpus. Sentiment analysis is either in the paper as a finding or it is not. If it is, the current 17% completion rate means any reported results are based on an unrepresentative fraction of the corpus. The TODO acknowledges "cleanup, re-classify, Hansard, forensic pipeline, cross-reference all pending" but does not attach a timeline or priority to any of those steps. This should be named explicitly in the project's operational plan — either as a submission blocker (like Fisher) or as a deferred-until-Phase-2 item.

### The deletion of planning docs is a sequencing question

The "Planning Docs — Flagged for Deletion" section lists nine files. These presumably contain context, intermediate decisions, and rationale that is not fully captured elsewhere. Deleting them before submission removes the ability to reconstruct analytical choices post-hoc, which matters if a reviewer raises a question about why a particular method was chosen. The deletion should happen after, not before, any information in those files that is not already in the main document has been either migrated or explicitly decided against.

### What the list reveals about what the author knows

A TODO list of this specificity — with ES numbers, effort estimates in 20-minute increments, per-metric ESS values, and exact corrected p-values — was not written by someone who does not understand their project. The analytical literacy embedded in the list (knowing that p94.27 is below the 95 threshold and therefore changes the interpretive claim, knowing that the declination direction opposing EG requires explanation) is higher than the surrounding prose problems (case name errors, label mismatches) would suggest. The Monday prep items are the kind of errors that survive draft iterations because the author is reading for substance, not surface. That is a normal failure mode, not an indictment.

### The right question for Blue Hat

The question the TODO does not answer is: what is the minimum viable state for submission, and how many hours away is it? The current document does not draw that line. Fisher stop is one named submission condition. What are the others? If the answer is "all CRITICAL and HIGH items must be resolved," that is 40–55 hours. If the answer is "all CRITICAL items plus selected HIGH items plus C1," that is something else. Without that line, the project risks finishing Monday's sprint and then facing an undifferentiated mass of remaining work without a clear signal for when it is acceptable to submit.

The TODO is an honest and detailed accounting. What it needs next is a submission gate — a defined set of conditions that, when met, allow the paper to go out. Right now the only named gate is Fisher. That is not enough.
