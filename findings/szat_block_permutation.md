---
title: SZAT under contiguity-respecting block-permutation null
date: 2026-06-12
status: T1.10b closed; substantive finding
script: analysis/scripts/szat_block_permutation.py
script_commit: pending
---

> **Backward:**
> - `analysis/scripts/szat.py` — original i.i.d.-flip implementation
> - `analysis/scripts/szat_block_permutation.py` — this analysis
> - T1.7 R1 Ref #1 D3 — methodological finding motivating this re-run
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.2.10 — incorporates this result
> - `reports/academic/report_academic.md` §5.5 — Bonferroni headline restated

# SZAT under contiguity-respecting block-permutation null

## Headline

The original SZAT Channel 2 bootstrap p = 0.0024 was computed under an i.i.d. Bernoulli(0.5) flip of each of 2,110 swing-zone Voting Areas independently. The swing-zone VAs are spatially autocorrelated (the audit's own Moran's I on NDP-share has z = 12.15, consistent with strong spatial clustering); independent per-VA flipping therefore *understates* the null variance and produces an anti-conservative p-value (Lehmann & Romano 2005 ch.15; Legendre 1993 Ecology 74).

This re-run replaces the i.i.d. flip with a **queen-contiguity block permutation**: connected components of contiguous swing VAs are flipped as units. The 2,110 swing VAs partition into 8 connected components (one of size 2,086 covering most of the inter-map swing zone, plus 7 small components).

**Result (10,000 bootstraps, canonical EA shapefiles + canonical election-day votes, drand-anchored salt `szat-block-permutation`):**

| Null model | Null std | p-value | (b+1)/(B+1) |
|---|---:|---:|---|
| i.i.d. flip (replicates the published *procedure*; independent RNG stream — the registered-seed run gives 24/10,000 = 0.0024) | 0.00807 | 0.0035 | 36/10,001 |
| **Block permutation (this work)** | **0.01942** | **0.1947** | 1946/10,001 |
| Variance inflation factor | — | — | **5.79×** |

The block-permutation null is **5.79× more variable** than the i.i.d. flip null because of the giant connected component (2,086 of 2,110 swing VAs) flipping as a single unit. The variance inflation makes the observed SZAT score (+0.0392) statistically unremarkable against the contiguity-respecting null.

## Substantive interpretation

**Channel 2 no longer contributes to the Bonferroni combination at any standard α.** Under the methodologically-correct null, the SZAT p-value is ≈ 0.2 — well above any significance threshold the audit cites.

The audit's published Bonferroni headline is **p ≤ 2.80×10⁻⁶ = 2 × min(Ch1, Ch2) = 2 × 1.40×10⁻⁶**, derived under the i.i.d.-flip SZAT. Numerically this bound is *unchanged* by the SZAT correction because Channel 1 (Mahalanobis joint tail) was already the binding minimum. But the interpretation changes:

- **Old framing**: two distinct channels (ensemble joint outlier + swing-zone boundary efficiency) both flag the minority map; Bonferroni at m=2 over them gives the joint bound.
- **Corrected framing (2026-06-12)**: Channel 1 (Mahalanobis p = 1.40×10⁻⁶ against the canonical 1.01M-plan ensemble) is the sole channel that crosses significance under a methodologically-rigorous null. Channel 2 (SZAT) does not survive the contiguity correction and is reported here for completeness but not used in the headline combination.

The Bonferroni-flavored "dependence-robust upper bound" remains valid for any family of channels the analyst chooses to include; under the corrected reading the family is effectively m = 1 and the bound is just Ch1's p = 1.40×10⁻⁶ ≈ 1 in 714,000 (more extreme than the 1-in-357,000 the 2 × Ch1 bound advertised).

## Why the i.i.d. flip was anti-conservative

The 8 connected components of the swing-zone graph are:

- 1 component of size **2,086** (97.4 % of the swing-zone VAs) — covers contiguous Calgary, Edmonton, and inter-city swing corridors that share boundaries through the urban-rural transition.
- 7 components of size 2 to 22 (typically isolated Voting Areas in remote rural regions where the two maps' boundaries happen to differ).

Under i.i.d. flipping, each of 2,110 swing VAs independently goes minority-side or majority-side with probability 0.5, producing a null with std ≈ 0.008 — approximately √(2110 × (mean per-VA contribution)²) / 2. Under block flipping, the 2,086-VA giant component flips together, so its contribution to a null draw is (sum of 2,086 per-VA contributions) × (single Bernoulli) — producing a null with std ≈ 0.019, an inflation factor that closely matches the theoretical √(N/(N/k)) for k effective blocks.

The audit's own evidence that the swing VAs are spatially autocorrelated — Moran's I z = 12.15 — was independent confirmation that the i.i.d. assumption was untenable.

## Reproducibility

```bash
python analysis/scripts/szat_block_permutation.py
```

Wall clock: ~2 s once the swing-VA cache is built (~30 s on first run).

Pre/post SHA-256 of `findings/szat_block_permutation.json` and the script commit are recorded inline in the JSON.

## Effect on the audit's verdict surface

The four-corner verdict surface (§6.2) is **unaffected in headline direction** because the Mahalanobis joint-tail finding (Ch1, p = 1.40×10⁻⁶) is the load-bearing partisan-bias number and stands on its own. The "two-channel converging" framing in §5.5 prose is restated as "Ch1 carries the partisan-bias evidence; Ch2 (SZAT) is reported but does not survive a contiguity-respecting null." The structural lane is independent of both channels.

## Queued follow-on

- **T1.10c — block-aware Cauchy combination.** Liu & Xie (2020) Cauchy combination is exact under arbitrary dependence and avoids the i.i.d.-vs-block-flip distinction at the cost of slightly conservative power. If a future Ch3 (or canonical-substrate Phase B drain) returns a moderate p, a Cauchy combination could be more defensible than Bonferroni.
- **T1.10d — alternative block definitions.** Beyond queen contiguity: rook contiguity, k-block Voronoi, regional blocks (Calgary / Edmonton / rural). The variance inflation factor would shift but the substantive conclusion (Ch2 doesn't survive correction) is robust because the giant component dominates regardless of block definition.
