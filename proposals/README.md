---
name: Proposals — speculative future work
description: "Landing for proposals/ — speculative future work that is NOT part of the current audit. Anything in this directory is a plan for work that has not been authorized, not been pre-registered (or pre-registered only in draft form), and not been executed. None of it appears in the audit's published claims. Reviewers can safely skip this entire directory unless they are specifically interested in what work might be done next."
type: project
---

> **Backward:**
> - `TODO.md` — flags which proposals are prep-complete and awaiting authorization
>
> **Forward:**
> - `analysis/methodology/` — where a proposal moves once authorized and the run is in progress
> - `preregistration/` — where the pre-registration amendment lands once signed and locked
> - (leaf — reviewer-facing landing for the proposals directory; not consumed by any script)

# Proposals

**This directory is not part of the audit.** Everything here is speculative future work.

A file lives here when:

- A method, run, or analysis has been *planned* in enough detail to be ready-to-execute
- The work has **not** been authorized by the principal investigator
- No compute has been consumed
- No claims, numbers, or findings have been produced
- Reviewers should not treat anything here as evidence

Files leave this directory in one of two ways:

1. **Authorized.** The principal investigator signs the pre-registration amendment, fills in the drand round number, and explicitly authorizes the run. The run plan moves to `analysis/methodology/` and the pre-registration amendment moves to `preregistration/`. From that point forward the work is part of the audit and bound by the audit's publish-regardless commitments.
2. **Declined or superseded.** The proposal is abandoned, or a different approach is taken instead. The files stay in `proposals/` but are clearly marked as historical. Git history is the redundant record.

**Reading guide.** If you are a reviewer and want to know what the audit *claims* — go to `README.md`, `findings/`, and `reports/`. If you want to know what the audit's principal investigator is *thinking about doing next* — read here. The two questions have different audiences and different evidentiary standards. Nothing here has been peer-reviewed, pre-registered (in non-draft form), or run.

## Current proposals

| Proposal | Status | Brief |
|---|---|---|
| `revrecom/` | PREP COMPLETE 2026-05-23, NOT AUTHORIZED | Reversible ReCom (Forest-ReCom; Cannon et al. 2022) robustness check against the canonical 1.01M-plan ReCom and 5,000-plan SMC ensembles. Targets the reviewer objection that ReCom has no writable stationary distribution. See `proposals/revrecom/run_plan.md` for the operational plan and `proposals/revrecom/pre_registration_amendment_DRAFT.md` for the binding-on-authorization pre-registration text. |
| `cross_vote_share/` | PREP COMPLETE 2026-05-23, NOT AUTHORIZED | Generalization of the pre-registered 48% NDP responsiveness test to a UCP-share sweep {0.45, 0.46, …, 0.55} across both proposals and the 1.01M-plan ensemble, asking at what vote-share range each proposal pushes one party past the 58-of-87 two-thirds supermajority threshold. Reuses the canonical uniform-swing algorithm; no new ensemble run required. See `proposals/cross_vote_share/run_plan.md` and `proposals/cross_vote_share/pre_registration_amendment_DRAFT.md`. |
| `hardcoded_values_audit.md` | PARTIALLY RESOLVED 2026-05-24 | Inventory of every hardcoded literal in the Phase B scorecard pipeline, classified by necessity. The notable finding — `phase_b_scorecard.py` maintained two separately-defined city lists (10 in mo1's drain check, 8 in mo2's lasso-urban-share denominator) — was confirmed as an unintentional asymmetry by the PI and fixed in the same day's commit (lists consolidated into module-level `LUNTY_CITIES`; mo2 now derives the CSD-codes set from it so no drift is possible). The audit's class-A through class-D recommendations remain unauthorized future work. |
| `i18n_implementation.md` | PREP COMPLETE 2026-05-24, NOT AUTHORIZED | Ready-to-execute plan for adding a language selector to `/` (English, Canadian French, Tagalog, Punjabi) with browser-language detection, query-param URL strategy, and localStorage persistence. Includes drop-in Svelte 5 store + selector component, sample translations of the document opener and verdict (French ready for editorial review; Tagalog and Punjabi drafts staged for native-speaker review). Recommends soft-launch (EN + FR only at first) so TL and PA wait for native review before being advertised on the selector. |
