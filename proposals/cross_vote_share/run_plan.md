---
name: Cross-vote-share supermajority test — run plan
description: "Ready-to-execute plan for extending the existing 48% NDP responsiveness test (pre-registered) to a parameterized sweep over provincial vote shares from 45% to 60% UCP two-party share in 1% steps, asking at what vote-share range each proposal pushes one party past the 58-of-87 two-thirds supermajority threshold. The 0.60 upper bound brackets the April 2026 338Canada polling operating point (UCP ≈ 58.3% two-party). Reuses the canonical uniform-swing algorithm and existing per-district vote artifacts; no new ensemble run required. Status PREP COMPLETE — explicit principal-investigator authorization and a signed pre-registration amendment required before running."
type: methodology
---

> **Backward:**
> - `preregistration/null_hypotheses.md` §2.2 — pre-registered 48% NDP responsiveness test (the narrower case this plan generalizes)
> - `analysis/scripts/mcmc_ensemble.py` — `seat_results()` (lines 133–232); the canonical uniform-swing algorithm this plan reuses unchanged
> - `analysis/scripts/marginal_seats_analysis.py` — `apply_uniform_swing()` (lines 154–190); a precedent for looping over a range of swing values
> - `data/simulated_ensemble_raw_samples_section_c.csv` — 200k-row aggregate ensemble (per-draw `seats_at_50_50`, `ucp_seats`, etc.)
> - `data/outputs/phase4c_per_ed_votes_minority.csv`, `phase4c_per_ed_votes_majority.csv` — per-district 2023 vote counts for the two proposals
> - `proposals/cross_vote_share/pre_registration_amendment_DRAFT.md` — pre-registration amendment draft (must be signed and locked before the run)
>
> **Forward:**
> - `findings/` — new file `findings/supermajority_threshold_curve.md` would be created if executed
> - `reports/academic/report_academic.md` — would gain a §5.x discussion of the supermajority threshold curve
> - `viewer/` `/` homepage Q3 — would gain a follow-up sentence naming the vote-share range at which each proposal crosses 58 seats
> - `TODO.md` — flags this plan as ready-to-run pending PI authorization

# Cross-vote-share supermajority test — run plan

**Status as of 2026-05-23: PREP COMPLETE, NOT RUN.** This file is a ready-to-execute plan. The principal investigator (Will Conner) must explicitly authorize the run, lock the pre-registration amendment (`proposals/cross_vote_share/pre_registration_amendment_DRAFT.md`), and confirm the drand seed before any analysis is started. Until that point, no script in this directory has been executed and no number derived from a vote-share other than 50/50 or 48/52 has been computed for either proposal.

## Why this would be run

The current audit measures `seats@50/50` — what each map produces when the provincial two-party vote splits exactly evenly. The pre-registered responsiveness test extends that to 48% NDP (`preregistration/null_hypotheses.md` §2.2), which is the operationalization of *Reference re Saskatchewan* 1991's requirement that boundaries respect partisan responsiveness.

Neither test answers the question the homepage verdict raises: **at what range of provincial vote shares does the minority proposal push one party past 58 of 87 seats — the two-thirds supermajority threshold that unlocks extraordinary procedural powers (waiving notice periods, accelerating bills through multiple legislative stages in a single day)?** The verdict honestly admits this gap; this run closes it.

The test is also a natural generalization of the pre-registered responsiveness test (48% is one point on the curve this plan would sweep). The generalization is what requires the pre-registration amendment — see `pre_registration_amendment_DRAFT.md`.

## What this run produces

A single CSV and a single figure:

- `data/outputs/supermajority_threshold_curve.csv` — for each of the three artifacts (minority, majority, 1.01M ensemble) and each vote share in {0.45, 0.46, …, 0.60}, the expected UCP seat count, NDP seat count, and the indicator `is_supermajority` (1 if max(ucp_seats, ndp_seats) ≥ 58, else 0). For the ensemble: per-draw values plus mean, median, p2.5, p97.5 across draws.
- `reports/figures/supermajority_threshold_curve.svg` — three curves (minority, majority, ensemble band) showing UCP seat count vs. provincial UCP vote share, with the 58-seat threshold drawn as a horizontal line.

No other artifacts. No interactive widgets. No sub-tests. The scope is fixed here to prevent post-hoc expansion.

## Method — pre-committed before run

Reuses the canonical uniform-swing algorithm (`mcmc_ensemble.py::seat_results()` lines 215–222) unchanged. The only change is sweeping the target share rather than hard-coding 0.5.

```python
# For each map (per-district arrays: ucp, ndp), for each target share s in 0.45..0.60:
province_ucp = ucp.sum() / (ucp.sum() + ndp.sum())
swing = s - province_ucp
ucp_share = ucp / (ucp + ndp)
shifted = np.clip(ucp_share + swing, 0.0, 1.0)
wins = (shifted > 0.5 + 1e-9).sum()
ties = (np.abs(shifted - 0.5) <= 1e-9).sum()
seats = wins + 0.5 * ties
```

Identical algorithm to the existing `seats@50/50` and the existing 48% NDP responsiveness test. The cross-vote-share test is **the same code applied to a wider sweep of target shares**.

## Parameters — pre-committed before run

| Parameter | Value | Source / justification |
|---|---|---|
| Vote-share grid | `[0.45, 0.46, 0.47, …, 0.60]` (16 points, UCP two-party share) | Lower bound 0.45 = floor of the 2015–2023 Alberta provincial-election range. Upper bound 0.60 brackets the April 2026 338Canada polling operating point (UCP ≈ 58.3% two-party = 52.46/(52.46+37.59) from the 2026-04-12 snapshot) with ~1.7 pp headroom, so the curve runs *through* today's operative vote environment rather than truncating at its edge. Extended from an earlier `[0.45, 0.55]` draft on 2026-06-14, before any run — see the grid-range note in the amendment for the anti-grid-shopping rationale. |
| Step size | 0.01 (1 percentage point) | Finest resolution that produces a visually distinguishable curve without overstating the precision of the underlying vote model |
| Maps tested | Minority proposal, Majority proposal, 1.01M-plan canonical ReCom ensemble | The three artifacts the homepage names |
| Per-district vote data | `phase4c_per_ed_votes_minority.csv`, `phase4c_per_ed_votes_majority.csv`, MCMC chain per-district counts | The same data the existing `seats@50/50` test uses |
| Swing model | Uniform swing on UCP two-party share | Same model as `mcmc_ensemble.py::seat_results()`; same model as the pre-registered 48% responsiveness test |
| Supermajority threshold | 58 of 87 seats | Mathematically 2/3 × 87 = 58; matches the threshold cited in the homepage verdict |
| Tie-break | UCP wins if shifted share > 0.5 + 1e-9; tied seats counted as 0.5 each | Identical to `seat_results()` |
| Clipping | Per-district shifted share clipped to [0, 1] | Identical to `seat_results()`; conservative against extreme swings that would push districts past 100% |
| Random seed | None — this is a deterministic transformation of fixed input data | No MCMC, no resampling, no randomness in the test itself |

**No tuning parameters.** No bandwidth, no prior, no thinning, no burn-in. The test is a deterministic function of the three input artifacts and the vote-share grid. Re-running it with the same inputs must produce bit-identical outputs.

## What counts as a finding vs. a null

Stated before the run, so the result cannot be reframed:

- **Finding — "minority proposal crosses 58 below 50% UCP vote share":** the minority proposal map, at some target UCP share ≤ 0.50, produces UCP seats ≥ 58 that fewer than 2.5% of ensemble draws produce at the same target share. This would mean the minority proposal hits a supermajority for UCP at a vote share where neutral maps almost never do.
- **Finding — "majority proposal symmetric":** the majority proposal stays within the ensemble's central 95% band across the full 0.45–0.60 grid for both UCP and NDP supermajority counts.
- **Null:** at every point on the 0.45–0.60 grid, both proposals' supermajority-crossing behaviour falls within the central 95% band of the ensemble. The verdict would then narrow: the minority proposal is extreme at 50/50 but does not systematically push past the supermajority threshold at adjacent vote shares, including the current ≈58% polling operating point.

Any of the three outcomes is publishable. The pre-registration amendment locks the publish-regardless commitment.

## What this test does NOT do

Stated to prevent scope creep:

- It does not test 2-party share models other than uniform swing.
- It does not test vote shares outside [0.45, 0.60]. This bound spans every Alberta provincial election since 2015 (UCP ≈ 0.52–0.55 two-party) and the April 2026 polling operating point (≈ 0.58); extrapolating above 0.60 or below 0.45 would multiply model error beyond any realistic Alberta vote environment.
- It does not test third parties. The two-party UCP/NDP model is the same one the canonical ensemble uses.
- It does not test district-level competitiveness, marginal-seat counts, or efficiency-gap variants — those have their own pre-registered tests.
- It does not produce a single headline number. It produces a curve; reviewers may read it differently, and that is the point.

## Estimated effort

- Implementation: 100–200 lines of Python (one script in `analysis/scripts/`, reusing `seat_results()` from `mcmc_ensemble.py`)
- Execution time: < 1 minute on the 200k-row ensemble CSV; trivial on the two 87-row proposal CSVs
- Write-up: one `findings/` markdown file (~300 lines), one figure
- Total: 2–4 hours from authorization to published finding

## Authorization checklist

Before any code in this directory runs:

- [ ] Principal investigator signs `pre_registration_amendment_DRAFT.md` and drops `_DRAFT` from the filename
- [ ] drand round number filled in (first round above authorization timestamp); note that this test is deterministic so the seed is documentation-only, not result-affecting
- [ ] `TODO.md` updated to reflect AUTHORIZED status
- [ ] Run plan and amendment moved out of `proposals/` per the directory protocol (`proposals/README.md`)
