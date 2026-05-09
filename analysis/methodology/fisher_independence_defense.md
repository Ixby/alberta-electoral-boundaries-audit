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

## Empirical independence check (recommended, not yet run)

Compute the Spearman rank correlation between:
- **ρ₁**: For each of the 100k MCMC plans, the Ch1 Mahalanobis distance D of
  that plan from the ensemble centre of mass (partisan metrics only).
- **ρ₂**: For each of the SZAT bootstrap draws, the EG of the resulting map.

If ρ(ρ₁, ρ₂) < 0.30, the channels are empirically near-independent and the
"approximately independent" Fisher claim is defensible for this dataset.

**Implementation sketch:**

```python
# In joint_outlier_score_canonical.py or a standalone validate script
from scipy.stats import spearmanr

# Ch1 Mahalanobis distances (per MCMC sample)
X = ensemble[PARTISAN_COLS].dropna().values
mu = X.mean(axis=0)
cov_inv = np.linalg.pinv(np.cov(X, rowvar=False))
D_samples = np.array([float((x - mu) @ cov_inv @ (x - mu)) for x in X])

# Ch2 bootstrap EG distribution (from SZAT bootstrap, if saved)
# Requires szat.py to export bootstrap_eg_samples — currently not output.
# Add: np.save(DATA / "szat_bootstrap_eg_samples.npy", boot_eg_array)

# correlation — currently blocked pending szat bootstrap export
rho, pval = spearmanr(D_samples[:len(boot_eg)], boot_eg)
print(f"Spearman ρ(Ch1-D, Ch2-EG) = {rho:.3f}  p = {pval:.4f}")
```

**Blocker:** `szat.py` does not currently save the per-draw EG distribution from
its bootstrap. To enable this check, add a save line inside the bootstrap loop
in `szat.py` (under `run()`, after the bootstrap array is built).

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

## Recommended addition to the paper methodology section

> "Channel 1 and Channel 2 are tested independently and combined via Fisher's
> method. Both channels use 2023 Alberta vote totals, but they measure different
> quantities: Ch1 asks whether the minority map is an outlier in the space of
> valid provincial plans (marginalising over all boundary configurations via MCMC);
> Ch2 asks whether the specific swing-zone boundary choices within the minority
> plan are systematically biased (conditioning on the minority boundary and
> shuffling only those assignments). The channels are therefore approximately
> conditionally independent given the shared vote data. If a positive correlation
> exists, Fisher's method is conservative — it understates joint significance.
> An empirical Spearman correlation check between Ch1 Mahalanobis distances and
> Ch2 bootstrap EG draws is planned for the supplementary materials."

---

*Last updated: 2026-05-08*
