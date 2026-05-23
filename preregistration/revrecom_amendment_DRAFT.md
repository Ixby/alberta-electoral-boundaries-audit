---
name: Pre-registration amendment — Reversible ReCom (RevReCom) robustness check (DRAFT)
description: "DRAFT pre-registration amendment committing the audit to running a Reversible-ReCom ensemble against the canonical 2026 commission maps and publishing the result regardless of direction. Status: NOT SIGNED, NOT LOCKED — the drand round number is a placeholder; this file is read-only methodology documentation until the principal investigator fills it in, drops _DRAFT from the filename, and commits."
type: preregistration
---

> **Backward:**
> - `analysis/methodology/revrecom_run_plan.md` — operational run plan that this amendment governs
> - `preregistration/null_hypotheses.md` — parent pre-registration document
> - `preregistration/seed_commitments.md` — drand-beacon seed-commitment convention used throughout the audit
>
> **Forward:**
> - `findings/redist_python_comparison.md` — sampler cross-validation that will incorporate the RevReCom result
> - `reports/academic/report_academic.md` §5.4 — joint outlier analysis that will incorporate the RevReCom result
> - (leaf — once locked, this file is a binding methodological commitment, not consumed by any script)

# Pre-registration amendment — Reversible ReCom (RevReCom) robustness check

**DRAFT — UNSIGNED.** Status fields below are placeholders. This amendment must be filled in (drand round number, signature, date), renamed to drop `_DRAFT`, and committed before the RevReCom run begins.

## Status fields (to be filled at authorization)

- **Amendment proposed by:** Will Conner (principal investigator)
- **Amendment date:** _to be filled at authorization_
- **drand beacon round (RNG seed):** _to be filled at authorization — first drand round above the authorization timestamp_
- **drand round URL (for verification):** `https://api.drand.sh/<chain-hash>/public/<round-number>`
- **Parent pre-registration:** `preregistration/null_hypotheses.md` (and prior amendments)
- **OSF / AsPredicted ID:** _to be filled if registered externally_

## Why this amendment exists

The audit's sampler-cross-validation rests on two ensembles: Python `gerrychain` ReCom (1,010,000 plans, canonical EA shapefiles) and R `redist` SMC (5,000 plans, importance-weighted, ESS 1,116). Both agree the canonical minority `seats@50/50` (0.5169) is an extreme outlier on canonical geometry. A reviewer raised the methodological objection that ReCom has no writable stationary distribution.

Reversible ReCom (RevReCom; Cannon, Goldbloom-Helzner, Gupta, Matthews, Suwal 2022 — arXiv:2210.01401) is a reversible variant of ReCom whose stationary distribution is the spanning-tree distribution: plan probability ∝ ∏ τ(district_i). Running RevReCom and reporting where the minority value falls in its distribution is a targeted methodological inoculation against the unknown-stationary-distribution objection. It does **not** answer the separate compactness-bias objection (the SMC cross-check answers that one) — RevReCom inherits the spanning-tree compactness preference by construction.

The principal investigator's primary methodological concern in adding this run is avoiding p-hacking / cherry-picking. This amendment is the binding instrument that prevents post-hoc reframing of the result.

## Pre-committed parameters

Locked in `analysis/methodology/revrecom_run_plan.md` §"Parameters — pre-committed before run." Key bindings:

- Sampler: `frcw --variant reversible` (Rust binary, MGGG-canonical at https://github.com/mggg/frcw.rs)
- Graph: canonical VA adjacency, 4,765 nodes / 13,385 edges, bit-identical to the ReCom and SMC inputs
- Seed partition: 2019 enacted Bill 33 (87 districts)
- `--n-steps`: 1,010,000 (matches the ReCom canonical ensemble exactly)
- `--tol`: 0.25 (EBCA ±25% population band)
- `--rng-seed`: drand round number (filled above)
- Burn-in: first 10% discarded
- Convergence threshold: GR92 R-hat < 1.10 publishable; < 1.05 preferred

These parameters cannot be changed after the RNG seed is drawn. If a parameter must be changed for technical reasons (e.g., the graph adapter needs a different population column), the amendment must be re-drafted and re-signed.

## Pre-committed reporting (publish-regardless)

The principal investigator commits to publishing the following items in `findings/redist_python_comparison.md` and `reports/academic/report_academic.md` §5.4 **within 7 days of the run completing, regardless of direction:**

1. Headline minority percentile (RevReCom). Number of plans equal-or-exceeding the canonical minority `seats@50/50` (0.5169), and the resulting percentile.
2. Headline majority percentile (RevReCom). Same for the canonical majority value (0.4607).
3. Convergence diagnostics: GR92 R-hat for the four partisan metrics; ESS per metric; pass/fail against the R-hat < 1.10 threshold.
4. Tri-sampler reconciliation table (ReCom / SMC / RevReCom) for both maps.
5. Mean and median Polsby-Popper across the RevReCom ensemble vs. ReCom and SMC.
6. Mahalanobis joint outlier D² for both maps under the RevReCom covariance.
7. Joint-distribution overlay plot (RevReCom + ReCom + SMC ensemble densities with real-map markers).

**If the RevReCom result contradicts the headline finding** (e.g., the canonical minority falls in the central body of the RevReCom distribution rather than the extreme upper tail), the audit's central claim will be re-framed in the next revision of `reports/academic/report_academic.md` to reflect the contradiction, and the methods paper's claim that the headline is "robust across operator families" will be downgraded or withdrawn.

**If the RevReCom result confirms the headline finding** (the canonical minority sits in the extreme upper tail of the RevReCom distribution as well, consistent with ReCom and SMC), the audit will report it as such with appropriate weight — a single additional sampler does not multiply the existing finding's strength; it answers a specific reviewer objection.

**If the RevReCom result partially confirms** (e.g., minority in the upper tail but not as extreme as under ReCom), the audit will report both numbers and the comparison.

**No suppression. No re-running for a different result. No swapping in a different sampler if RevReCom disappoints.** This amendment is the binding instrument.

## Binding signatures

- **Principal investigator:** _Will Conner, signature/initials and date to be entered at authorization_
- **Witness or co-investigator (if applicable):** _N/A — this is a single-PI audit_

Once signed and committed, this file becomes immutable. Any future amendment must be a new file with a new drand round.
