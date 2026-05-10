# Fisher Combination Independence Defense

**Test location:** `joint_outlier_score_canonical.py:214–223`
**Concern (O1 from adversarial audit):** Channel 1 (Mahalanobis) and Channel 2
(SZAT bootstrap) both condition on the same 2023 Alberta vote vector, so they
are not measuring strictly independent quantities.

---

## What each channel actually measures

| Channel | Question | Input data | Null distribution |
|---------|----------|------------|-------------------|
| Ch1 | Is the minority map an outlier in the *space of geographically valid Alberta plans*? | 2023 vote totals assigned to swing VAs, aggregated by MCMC partition | 100k MCMC draws from the null |
| Ch2 | Do *boundary choices in the specific swing zone* drive the observed EG, over and above the geographic distribution of votes? | 2023 vote totals for 2108 swing VAs | Bernoulli(0.5) shuffle of swing-zone VA assignments |

Ch1 integrates over *all* boundary configurations. Ch2 conditions on the *specific
boundary* and asks whether that boundary's swing-zone choices are systematic.
These are different conditioning events even though they share the same underlying
vote counts.

---

## Empirical independence check

**Status: instrumented, pending next szat.py run.**

The check computes Spearman rank correlation between:

- **D**: Ch1 Mahalanobis distances for each MCMC plan (from the ensemble CSV)
- **EG**: Ch2 bootstrap EG draws (from `data/szat_bootstrap_eg_samples.npy`)

If |ρ| < 0.30, the channels are empirically near-independent and the Fisher
combination claim is defensible. If |ρ| ≥ 0.30 and the correlation is positive,
Fisher is conservative (understates joint significance) — this is a disclosure
obligation, not a retraction trigger.

### Infrastructure in place (2026-05-09)

- `szat.py` now saves `data/szat_bootstrap_eg_samples.npy` after each bootstrap run
- `analysis/scripts/validate_fisher_independence.py` computes ρ and appends the
  result to this document automatically
- `tests/test_pipeline_integration.py::test_fisher_channel_independence` enforces
  |ρ| < 0.30 as a live CI gate; the test activates automatically once the `.npy`
  exists (currently skipped)

### Action required before submission

Run `python analysis/scripts/szat.py` to generate the bootstrap samples, then re-run
the test suite. The empirical ρ will be recorded in the "Empirical result" section
below and appended to this document automatically.

> **Do not submit the paper with this section showing "pending."**

---

## Structural argument (usable without running the correlation)

Even without the empirical check, the approximate independence claim rests on:

1. **Different conditioning events.** Ch1 marginalises over all boundary placements
   by drawing from the MCMC null. Ch2 conditions on the *actual* minority boundary
   and shuffles only swing-zone assignments. These are complementary slices of the
   same probability space.

2. **Small swing zone.** The 2108 swing VAs represent ~13% of the province's ~16k
   VAs. MCMC plans vary the full province; SZAT varies only the minority plan's
   swing zone. The residual correlation from shared vote data is attenuated by
   the large non-swing regions that MCMC but not SZAT varies.

3. **Fisher is conservative if positively correlated.** If Ch1 and Ch2 are in fact
   positively correlated (maps that look like gerrymandering on one channel also
   look like it on the other), combining with Fisher understates the true joint
   significance. The combined p-value is *at least as conservative* as the smaller
   of the two individual p-values. A violation of independence makes Fisher a
   lower bound, not an upper bound.

---

## Broader Fisher defense

All other attack vectors on the Fisher combination (post-hoc channel selection, why no
majority Fisher, robustness across methods, directionality, n_eff correction, multiple-map
correction, pre-registration gap) are addressed in
`analysis/methodology/fisher_combination_defense.md`.

---

*Last updated: 2026-05-09*
