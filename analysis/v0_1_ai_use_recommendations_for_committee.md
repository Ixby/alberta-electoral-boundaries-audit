---
name: AI-use recommendations for the Alberta Electoral Boundaries MLA Committee
description: Technical, non-partisan recommendations for how the Special Select Committee of MLAs (chaired by Brandon Lunty, due November 2, 2026) can use AI tools responsibly if it chooses to. Grounded in the audit's own methodology discipline (reproducibility, transparency, pre-registration, defensibility gates).
forward_dependencies:
  - report_academic.md §Recommendations (candidate target for a summary insertion)
  - report_public.md §"The 91-seat proposal, so far" (candidate target for a brief paragraph)
backward_dependencies:
  - Calgary Journal article 2026-04-21 (Premier Smith's "AI academy" remark — the signal that AI use is on the table)
  - CLAUDE.md §House voice
  - v1_2_gerrymander_audit_prompt.md §Defensibility Audit Gate (DA1–DA7)
---

# AI-use recommendations for the Alberta Electoral Boundaries MLA Committee

**Audience.** The Special Select Committee of MLAs chaired by Brandon Lunty, MLA for Leduc-Beaumont. This document is technical advice on *how* to use AI tools responsibly if the committee chooses to use them. It does not take a position on whether the committee should use them.

**Why this document exists.** On April 16, 2026, the Premier made a public remark suggesting that members of the opposition "should take our AI academy" in the context of the boundary-drawing process. Whether that was rhetoric or procedure is not something this audit can determine. What it can do is provide a concrete framework that distinguishes responsible AI assistance from AI use that would compound the independence concerns already raised about the April 16 process.

**Scope.** Any AI system — large language model, computational redistricting software, optimization solver, clustering algorithm, or natural-language-processing tool applied to public submissions. Each has different risks and different disciplines. This document treats them together at the principle level and separately at the technical level.

**Framing principle.** A boundary-drawing process is a decision with thirty-year effects, binding every citizen. AI tools can make such a process faster, more consistent, and more testable. They can also make it less transparent, more biased, and less accountable. Which of those happens depends on how the committee designs its workflow, not on whether it uses AI.

---

## Part 1 — Core principles

### 1. Humans decide; AI assists

A boundary map has legal and constitutional effect. It should be proposed, debated, and signed by named humans who can be held accountable. An AI system's output is not a proposal until a committee member reads it, understands it, and says so. "The computer drew this" is not a defence if a line is wrong.

**Implementation.** Every boundary in the final map should have at least one committee member or advisor of record who will answer for it in public. No map should be finalized on the grounds that "the algorithm converged" alone.

### 2. Transparency over opacity

Every prompt, input dataset, model version, and output used in the drafting process should be logged, timestamped, and publicly releasable with the final report. If a committee member asked a model to "suggest boundaries that minimize urban-rural hybrids in Calgary," that prompt should appear in the public record.

**Implementation.** Maintain a workflow log. Publish it with the final map. Redact only where necessary for personal privacy; do not redact for reputational reasons.

### 3. Reproducibility over one-shot generation

Any AI output used in the map should be reproducible by an independent third party given the same inputs. This requires fixing random seeds, pinning model versions, and publishing the prompt templates.

**Implementation.** If the committee uses stochastic methods (MCMC, simulated annealing, LLM completions), publish seeds and software versions. Prefer methods whose outputs are stable under the same inputs.

### 4. Pre-registration over post-hoc justification

The committee should publicly commit to its testing criteria *before* drawing the map, not after. The audit's own pre-registered checklist for the 91-seat map is a template: it names the signals, criteria, and thresholds in advance, so that later claims of "not a gerrymander" cannot be assembled by selecting flattering tests after the fact.

**Implementation.** Publish the committee's evaluation criteria (population equality targets, community-of-interest priorities, compactness thresholds) before any map draft is circulated. Treat them as a gate the map must clear.

### 5. Independence tests over single-model reliance

If AI is used to generate or evaluate boundaries, run at least two independent tools and compare their outputs. Disagreements are not noise to be averaged — they are signals that a human needs to adjudicate.

**Implementation.** Where two models disagree on a proposed boundary, require a written human explanation for the choice. Where they agree, the agreement is weak evidence that the boundary is a natural fit.

### 6. Falsifiability over rhetoric

Every claim attached to the final map ("this preserves community of interest," "this reflects commuter ties," "this provides effective representation") should be stated in a form that can be checked against data after the fact.

**Implementation.** For each claim, name the dataset that would confirm or refute it. If no dataset exists and none is possible, downgrade the claim to "opinion" and label it so in the report.

### 7. Auditability over ease of use

The cheapest AI workflow is also the least auditable: an MLA types a question into a chatbot, reads the answer, and acts on it. The second-cheapest is slightly better logged. Neither is adequate for a constitutional decision. Invest in the workflow that makes every step reproducible, even when that workflow is slower.

---

## Part 2 — Specific technical recommendations

### 2.1 Generation of candidate boundaries

If the committee uses AI to generate candidate district configurations:

- **Use purpose-built redistricting software**, not a general-purpose chatbot. Tools built on Markov Chain Monte Carlo (MCMC) sampling such as GerryChain (the Metric Geometry and Gerrymandering Group's open-source Python library) or commercial equivalents such as Dave's Redistricting App or Maptitude for Redistricting. These tools treat the space of legal maps as a sample space and can produce thousands of plans meeting a defined set of rules.
- **Define the rule set in advance**, in writing. Hard constraints (population within ±25%, contiguity, s. 15(2) eligibility criteria) are parameters; soft constraints (community of interest, compactness) are scoring weights. Publish both before any run.
- **Publish the ensemble, not only the chosen map.** A single map says nothing about whether the committee's choice is typical or an outlier. An ensemble of 10,000 rule-following alternatives lets the public see where the committee's final map sits in the distribution.
- **Do not use an LLM to write boundary descriptions directly.** Large language models hallucinate street names, invert cardinal directions, and confuse jurisdictions. Use them only as a drafting aid for human-reviewed text — never as the source of the boundary itself.

### 2.2 Evaluation of candidate boundaries

If the committee uses AI to evaluate proposed districts:

- **Apply the same partisan-fairness metrics used in the academic literature** — efficiency gap, mean-median difference, declination, seats-votes curve — against vote data from the three most recent provincial elections, not one. The audit's v0_2_packing_cracking_analysis.py is a reference implementation; any independent implementation that reproduces its numbers on the 2019 map within ±0.05 pp is a valid check.
- **Run a Chen and Rodden (2013) natural-packing test.** If the proposed map's partisan lean falls within the distribution of randomly-generated legal alternatives, the map is consistent with Alberta's underlying voter geography. If it falls outside the 95th percentile of that distribution in either direction, the map is an outlier and requires a stated, testable explanation.
- **Compute compactness scores** (Polsby-Popper, Reock, or both) on every district. Publish them. Districts in the bottom 5% of compactness against recent Canadian provincial averages should have a written community-of-interest rationale.
- **Code public submissions by theme** using an LLM classifier, then publish the classifier's prompt, the coded output, and a human-audited spot-check on a random sample of 10%. Classification is fine for volume reduction; it is not a substitute for the committee's own reading.

### 2.3 Analysis of public input

If the committee solicits public input (even through the advisory panel) and uses AI to process it:

- **Publish the input corpus** (redacted for personal information) so that independent researchers can reproduce the theme coding.
- **Do not rank submissions by length, signature count, or other engagement proxies.** Electoral boundary decisions weigh arguments, not volume. A single submission from an affected community of interest can be load-bearing; a form letter signed by hundreds does not supersede it.
- **Flag the absence of input as well as the presence of it.** If a region produced no submissions, the committee should ask why (lack of awareness, lack of trust in the process, lack of time to respond) and act on that question rather than treating silence as consent.

### 2.4 Justification drafting

If the committee uses AI to draft justification text for the final report:

- **Every factual claim in an AI-drafted paragraph must be human-verified against a cited source.** Treat AI-generated prose the way an editor treats a new reporter: read every sentence, check every number.
- **Do not let an AI generate the committee's interpretation of legal or constitutional standards.** *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] has a specific holding on "effective representation." AI summaries of Canadian constitutional law are generally unreliable and occasionally invert the holding.
- **Publish the prompts used to generate any passage that appears in the final report.** A reader should be able to tell which paragraphs were human-written and which were AI-assisted.

---

## Part 3 — What AI should not do

The following tasks should not be delegated to AI, even with human review:

- **Final decisions on district boundaries.** A committee member, not a model, signs each district.
- **Weighing constitutional considerations.** s. 3 Charter analysis, *Saskatchewan Reference* application, and s. 15(2) criteria are legal judgments, not optimization outputs.
- **Determining community of interest.** Lived experience in a community is not retrievable from a census table. A classifier can code submissions about community of interest; it cannot determine what a community's interest is.
- **Drafting the committee's findings on contested districts.** If a district is contested (Airdrie, Chestermere, Nolan Hill-Cochrane, Rocky Mountain House-Banff Park, or any new flashpoint under the 91-seat plan), the committee's written reasoning should come from a named committee member, not an LLM.
- **Assessing partisan intent.** The audit's own discipline on this is strict: evidence cannot distinguish motive, and AI cannot either. Claims about what any individual or party intended should not appear in the report.

---

## Part 4 — Public disclosure checklist

Before publishing the final map, the committee should be able to answer each of the following publicly:

1. Which AI tools (by name and version) were used at any stage?
2. What prompts and inputs were given to each tool?
3. What outputs were used in the final map, and which were discarded?
4. What random seeds, model configurations, and parameter values were set?
5. Which committee member or advisor takes personal responsibility for each district's boundary?
6. What evaluation criteria were established before drafting began?
7. What ensemble of alternative maps was generated, and where does the final map sit in that ensemble?
8. What Charter and statutory analyses were performed, and by whom?
9. Which claims in the final report are AI-drafted and human-verified, which are human-drafted, and which are AI-drafted without human verification?

A committee that can answer all nine, and publishes the answers, has used AI responsibly. A committee that cannot has not — regardless of how sophisticated the tooling was.

---

## Part 5 — Risks specific to the April 2026 context

Three risks apply to this particular committee and this particular process, not to boundary work in general:

### 5.1 Independence-washing

The April 16 mandate includes an "advisory panel" with the three-party chair-plus-two structure. If the advisory panel uses AI tools whose outputs are then filtered through a UCP-majority MLA committee, the panel's independence is nominal. To preserve the panel's independence, the advisory panel's AI outputs (if any) should be published in full before the MLA committee acts on them, and any substantive deviation by the MLA committee from panel recommendations should carry a written explanation.

### 5.2 Legitimacy-by-association

An AI tool's output inherits only as much legitimacy as its inputs and its operators provide. If a committee presents a map as "algorithmically generated" without disclosing the prompt or the constraint set, it is borrowing technical legitimacy it has not earned. The public-disclosure checklist above is the minimum standard for avoiding this.

### 5.3 Acceleration past deliberation

AI tools can generate thousands of candidate maps in hours. They can also short-circuit the slow, deliberative work that a committee is supposed to do. A proposed boundary should not be adopted because it was the output of a model run — even a well-designed one — without the committee's own independent consideration of each contested district. Speed is not a virtue in redistricting.

---

## Part 6 — Reference implementations and datasets

For any committee or staff member beginning this work:

- **GerryChain**: https://gerrychain.readthedocs.io — open-source Python library for MCMC sampling of districting plans. Used in US Supreme Court redistricting litigation; well-documented; reproducible.
- **Dave's Redistricting App**: https://davesredistricting.org — web-based tool; used for US states; supports compactness, competitiveness, and demographic scoring.
- **The Chen-Rodden (2013) natural-packing method**: see Chen, J. and Rodden, J., "Unintentional Gerrymandering," *Quarterly Journal of Political Science* 8(3), 239–269. Reference for the "is this map an outlier or a natural product of geography?" question.
- **Alberta 2021 Census CSD populations**: Statistics Canada, public, directly loadable as a constraint dataset.
- **Alberta 2019 ED shapefile**: Elections Alberta, public. The reference geometry for any crosswalk to new boundaries.
- **Journey-to-work (StatsCan 98-10-0459)**: for any commuter-tie rationale, this is the dataset that tests it at CSD resolution.
- **This audit's codebase**: https://github.com/Ixby/alberta-electoral-boundaries-audit — the evaluation metrics the committee's output will be tested against. Publishing its own metrics in the same form would make the final map's defensibility easier to establish.

---

## Summary

Responsible AI use in a boundary-drawing process is not a question of which model or which vendor. It is a question of discipline. The five disciplines that matter most:

1. Humans decide, AI assists.
2. Every prompt, seed, and output is logged and published.
3. Evaluation criteria are registered before drafting begins.
4. Two independent tools run in parallel on any question whose answer matters.
5. Every boundary has a named human of record.

A committee that follows these disciplines will produce a map that holds up to scrutiny whether or not AI was used. A committee that skips them will produce a map that fails scrutiny in proportion to how central the AI was to the decision.

The audit's own methodology is written to the same discipline. It is available as a reference implementation, and the committee is welcome to use it — or to use something better.

---

## Provenance and falsifiability

- All tool names (GerryChain, Dave's Redistricting App) and academic references (Chen & Rodden 2013, *Saskatchewan Reference* 1991) are real and verifiable.
- StatsCan Table 98-10-0459 is verified accessed 2026-04-22 (see `analysis/v0_1_cochrane_journey_to_work.md`).
- No AI system has been "endorsed" by this document. The committee is free to use any tool; the discipline required is independent of the tool choice.
- If the committee adopts any of these recommendations and wishes to cite them, the appropriate citation is: Conner, W., *AI-use recommendations for the Alberta Electoral Boundaries MLA Committee*, Alberta Electoral Boundaries Audit, v0.1, 2026-04-22.
