---
name: Pre-registration amendment — cross-vote-share supermajority test (DRAFT)
description: "DRAFT pre-registration amendment generalizing the existing 48% NDP responsiveness test to a parameterized sweep over UCP vote shares from 45% to 55% in 1% steps, asking at what vote-share range each proposal pushes one party past the 58-of-87 two-thirds supermajority threshold. Commits the audit to publishing the result regardless of direction. Status: NOT SIGNED, NOT LOCKED — this file is read-only methodology documentation until the principal investigator fills in the drand round, drops _DRAFT from the filename, and commits."
type: preregistration
---

> **Backward:**
> - `proposals/cross_vote_share/run_plan.md` — operational run plan that this amendment governs
> - `preregistration/null_hypotheses.md` §2.2 — parent pre-registration; the 48% NDP responsiveness test is a single point on the curve this amendment generalizes
> - `preregistration/seed_commitments.md` — drand-beacon seed-commitment convention
>
> **Forward:**
> - `findings/supermajority_threshold_curve.md` — finding that this amendment governs (will be created if executed)
> - `reports/academic/report_academic.md` — would incorporate the threshold curve into the responsiveness discussion
> - (leaf — once locked, this file is a binding methodological commitment, not consumed by any script)

# Pre-registration amendment — cross-vote-share supermajority test

**DRAFT — UNSIGNED.** Status fields below are placeholders. This amendment must be filled in (drand round number, signature, date), renamed to drop `_DRAFT`, and committed before the run begins.

## Status fields (to be filled at authorization)

- **Amendment proposed by:** Will Conner (principal investigator)
- **Amendment date:** _to be filled at authorization_
- **drand beacon round (documentation seed):** _to be filled at authorization — first drand round above the authorization timestamp_
- **drand round URL (for verification):** `https://api.drand.sh/<chain-hash>/public/<round-number>`
- **Parent pre-registration:** `preregistration/null_hypotheses.md` §2.2 (responsiveness-gerrymander test, 48% NDP case)
- **OSF / AsPredicted ID:** _to be filled if registered externally_

Note on the seed: this test is a deterministic transformation of fixed input data. The drand round is documentation — it timestamps the authorization, not the result. The seed cannot be used to seed-shop because changing it does not change the output.

## Why this amendment exists

The parent pre-registration (`preregistration/null_hypotheses.md` §2.2) commits the audit to a responsiveness-gerrymander test at one specific point: 48% NDP provincial share. That point was chosen to operationalize *Reference re Saskatchewan* 1991's responsiveness requirement.

The homepage verdict raises a question the 48% test does not answer: **at what range of vote shares does each proposal push one party past 58 of 87 seats — Alberta's two-thirds supermajority threshold?** Answering that requires sweeping the parameter the parent test holds fixed. The sweep is a natural generalization (the 48% test is the point at NDP share 0.48, equivalent to UCP share 0.52, on the curve this amendment proposes), but it is not literal — so it requires a pre-registration amendment rather than a quiet extension.

This amendment is the minimum widening of the parent test's scope necessary to answer the verdict's question. It does not introduce a new method, a new model, or a new dataset; it sweeps an existing axis.

## What is being committed

The audit commits to the following, regardless of direction of result:

1. **Run the test as specified in `run_plan.md`** — vote-share grid {0.45, 0.46, …, 0.55} (UCP two-party share), three maps (minority, majority, 1.01M-plan canonical ensemble), uniform-swing model identical to the parent test, 58-seat supermajority threshold.

2. **Publish the resulting curve** as `findings/supermajority_threshold_curve.md` and the figure as `reports/figures/supermajority_threshold_curve.svg`, regardless of which of the pre-specified outcomes (finding A, finding B, or null — see `run_plan.md`) the data produces.

3. **Update the homepage verdict** to reflect the result. If a finding: extend Q3 with one sentence naming the vote-share range at which the minority proposal crosses 58 seats. If a null: extend Q3 with one sentence narrowing the verdict to "extreme at 50/50, but symmetric across the 45–55% range." The verdict cannot be left untouched after this test runs.

4. **No additional sweeps, sub-tests, or post-hoc reframings.** If the curve suggests an interesting question outside the pre-committed grid (e.g., 56% UCP, or NDP-side supermajority paths), that question requires its own amendment before any further analysis.

## What this amendment does NOT do

- It does not retire the 48% NDP responsiveness test in the parent pre-registration. That test still runs as specified; this amendment is additive.
- It does not change the method, the input data, or the threshold values for any other pre-registered test.
- It does not authorize a new ensemble run. The existing 1.01M-plan canonical ReCom ensemble is the only ensemble this test uses.

## Retraction conditions

In addition to the audit-wide retraction conditions in `preregistration/retraction_conditions.md`, this test is retracted if:

- The uniform-swing algorithm is found to misbehave on per-district counts outside the [0.45, 0.55] target range (e.g., excessive clipping in extreme districts that biases seat counts).
- The per-district vote inputs (`phase4c_per_ed_votes_minority.csv`, `phase4c_per_ed_votes_majority.csv`) are superseded by a corrected version. In that case the test must be rerun and the finding re-published on the corrected inputs.
- The 58-seat supermajority threshold is found to be procedurally incorrect (e.g., if Standing Order interpretation pins the threshold at 59 strict-greater-than rather than 58 ≥). In that case the test is rerun with the corrected threshold; the curve itself does not change, only the threshold line.

None of these conditions are expected. They are listed to make the retraction pathway explicit.

## Sign-off

- [ ] **Principal investigator (Will Conner):** _signature, date_
- [ ] **drand round number:** _to be filled_
- [ ] **Filename:** rename from `pre_registration_amendment_DRAFT.md` to `pre_registration_amendment.md`
- [ ] **Commit:** lock this amendment in git before any code in `proposals/cross_vote_share/` runs
