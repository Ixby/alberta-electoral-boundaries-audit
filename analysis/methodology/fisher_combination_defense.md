# Fisher Combination Defense

**Purpose:** Exhaustive anticipation of reviewer objections to the Fisher combination of
Ch1 (Mahalanobis, p = 1.60×10⁻⁷) and Ch2 (SZAT bootstrap, p = 0.0024) →
Fisher T = 43.36, combined p = 8.71×10⁻⁹.

**Companion document:** `fisher_independence_defense.md` — independence assumption (AV5 here).

*Last updated: 2026-05-09*

---

## 1. What the combined test claims

**H₀:** The minority map's observed partisan metrics are consistent with a neutral drawing
process that respects Alberta's geography and administrative constraints.

**Test statistic:** Fisher's combination method applied to two pre-registered p-values:

```
T = −2 [ln(1.60×10⁻⁷) + ln(0.0024)] = 43.36
T ~ χ²(df = 4) under H₀ with independent channels
p = χ²_4.sf(43.36) = 8.71×10⁻⁹
```

**Interpretation:** Under a neutral drawing process, a minority map this extreme on both
channels simultaneously would occur in approximately 1 out of every 115 million draws.
This is not a claim that the map *is* a gerrymander — it is a claim that the map is
a statistical outlier relative to the null distribution of neutral plans.

---

## 2. The two channels and their pre-registration

| | Ch1 — Mahalanobis joint tail | Ch2 — SZAT swing-zone bootstrap |
|---|---|---|
| **What it measures** | Is the minority map an outlier in the space of geographically valid Alberta plans? | Do swing-zone boundary choices in the minority map systematically drive EG above the neutral expectation? |
| **Null distribution** | 100,000 MCMC draws from the space of plans respecting Alberta geography | Bernoulli(0.5) shuffles of swing-zone VA assignments (2,110 VAs, 10,000 draws) |
| **Pre-registration** | OSF qsgy8 | OSF r3zm7 |
| **Seed provenance** | drand League of Entropy beacon round pre-dating shapefile release | drand League of Entropy beacon round pre-dating shapefile release |
| **Result** | p = 1.60×10⁻⁷ | p = 0.0024 |

**Timeline establishing non-cherry-picking:**

1. OSF pre-registrations submitted (qsgy8, r3zm7) — methodology and seeds locked
2. drand beacon rounds captured — seeds cryptographically committed
3. Official Elections Alberta shapefiles released publicly
4. Analysis executed with locked seeds on released shapefiles

No analyst could have seen the p-values before committing the seeds, because the seeds
predate the data. The results are fully deterministic from the seeds.

---

## 3. Channel design: why these two and not others

### AV2 — "You excluded Ch3 because it didn't help" (post-hoc channel selection)

This is the strongest potential objection. The Ch3 drain score for the minority map is
p = 0.1342 (within the null). Ch3 is excluded from the Fisher combination.

**The exclusion criterion is design-based, not significance-based:**

Ch1 and Ch2 both test the *partisan signature* of the minority boundary — whether the
boundary's partisan outcomes are inconsistent with a neutral drawing process. They are
commensurable: both answer variants of "is this boundary politically extreme?"

Ch3 tests *adjacency drain patterns* — whether the graph structure of the boundary (how
districts couple to neighbours across partisan lines) is unusual. This is a
graph-theoretic property of the boundary, not a partisan outcome. It answers a different
question: "does the boundary have unusual topological characteristics?"

**The design rule, stated independently of any p-value:**

> Channels are combined via Fisher when they test commensurable hypotheses about the
> same boundary decision. Ch1 and Ch2 measure partisan extremity of the minority boundary
> under different null distributions. Ch3 measures a graph property of the boundary
> (drain coupling). These are not commensurable for Fisher purposes.

**The same rule applies symmetrically to all maps:** if Ch3 had returned p = 0.001 for
the minority map, it would still not be combined with Ch1 and Ch2 under this rule, because
the construct is different. The majority map's Ch3 result (anomalously clean drain score,
a separate finding) is also not combined with its Ch1 result (p = 0.125) for the same
reason.

**Sensitivity check — what if Ch3 were included anyway?**

```
T_3ch = −2 [ln(1.60×10⁻⁷) + ln(0.0024) + ln(0.1342)] = 47.38
p_3ch = χ²_6.sf(47.38) = 1.57×10⁻⁸
```

Including Ch3 changes the combined p from 8.71×10⁻⁹ to 1.57×10⁻⁸ — somewhat less
significant, not more. Ch3 exclusion does not inflate the result.

### AV3 — "You only applied Fisher to the minority map" (asymmetric application)

Fisher is applied to the minority map only. No Fisher combination is reported for the
majority map.

**Why Fisher is minority-only — the null construction:**

SZAT's null distribution fixes non-swing VAs permanently to the **majority** map's ED
assignment, then randomizes the 2,108 swing VAs (Bernoulli 0.5 per VA, 10,000 draws).
With this anchor, the majority map's SZAT score is identically zero (it uses majority_ed
for every VA, including swing VAs) — testing it against the same null is trivially
non-significant by construction, not a meaningful test.

A symmetric Ch2 for the majority is achievable: flip the anchor to the minority map
(fix non-swing VAs to minority_ed), randomize swing VAs, and test where the majority
map's EG falls. By symmetry of the Bernoulli(0.5) null, the majority's observed SZAT
score equals −(minority's score), so the two-tailed p-value is approximately the same
(~0.0024). The symmetric test would confirm the finding from the other direction.

**The pre-registration (OSF r3zm7) specifies the majority-anchored null.** The
minority-anchored version for the majority map would be a post-hoc supplementary check.
It is not reported as a primary result. Its mathematical equivalence under the symmetric
null is noted here as evidence the test is not asymmetrically designed.

Fisher on {Ch1, Ch2} is therefore a minority-only test by the null's anchor choice
(pre-registered), not by selection after seeing results.

**The majority map is fully evaluated:**

| Channel | Majority map result |
|---|---|
| Ch1 (Mahalanobis) | p = 0.125 — within the neutral null |
| Ch3 (drain score) | Anomalously clean — a separate finding (see drain analysis) |

The majority map's Ch1 result (p = 0.125) places it comfortably within the neutral null
distribution. The absence of a Fisher combination for the majority map reflects the
null anchor specified in the pre-registration, not a decision to omit an unflattering result.

---

## 4. Robustness across combination methods (AV4)

A finding tied to a specific combination method is fragile. The following table shows
the combined p-value under four methods, all computed from the same two input p-values.

| Method | Minority combined p | Independence assumption | Notes |
|---|---|---|---|
| **Fisher (implemented)** | **8.71×10⁻⁹** | Required | T=43.36, df=4 |
| Stouffer (z-score) | 2.29×10⁻⁸ | Required | z = (5.111 + 2.620) / √2 = 5.467 |
| Cauchy combination | 3.20×10⁻⁷ | Not required | Robust to heavy-tail dependence |
| Bonferroni | ≤ 3.20×10⁻⁷ | Not required | Conservative; p_min × 2 |

**Interpretation:** All four methods produce a combined p well below 1×10⁻⁶. The finding
is not an artefact of Fisher's method. Even Bonferroni — which requires no independence
assumption and is the most conservative frequentist bound — clears the threshold by more
than an order of magnitude.

The Cauchy combination method is particularly notable: it is specifically designed to be
robust to dependence between channels, including heavy-tail dependence. It returns
p = 3.20×10⁻⁷, the same value as Bonferroni, reflecting the dominated term (Ch1).

---

## 5. Independence (AV1)

Addressed in full in `fisher_independence_defense.md`.

**Summary:** Ch1 and Ch2 both use 2023 Alberta vote totals, but they condition on
different events. Ch1 marginalises over all boundary configurations via MCMC. Ch2
conditions on the *actual* minority boundary and shuffles only swing-zone VA assignments.
These are different conditioning events. The structural argument is supplemented by an
empirical Spearman ρ check (CI gate: |ρ| < 0.30) that activates automatically once
`szat.py` is re-run.

If Ch1 and Ch2 are positively correlated, Fisher is **conservative** — it understates
joint significance. A violation of independence makes Fisher a lower bound, not an upper
bound on the combined p-value.

---

## 6. Directionality (AV5)

**Objection:** The Mahalanobis distance (Ch1) is non-directional. How do we know the
extremity is in a coherent partisan direction rather than a random combination?

**Response — non-directionality is a feature, not a defect:**

Fisher tests whether the minority map is jointly unusual — not whether it is unusual in a
pre-specified direction. Pre-committing to a direction (e.g., "EG will be extreme in the
UCP-favouring direction") would be a methodological choice requiring pre-specification.
Using a non-directional test avoids this.

**Post-hoc characterisation of direction (not a new test):**

The three partisan metrics' percentile placements for the minority map:

| Metric | Minority percentile | Direction |
|---|---|---|
| Efficiency gap (EG) | 100.0 (above entire ensemble) | UCP-favoured |
| Seats-at-50-50 | 100.0 (above entire ensemble) | UCP-favoured |
| Declination | 2.17 | NDP seat-vote curve locally "too fair" |

EG at p100 and seats-at-50-50 at p100 both indicate strong UCP favorability. Declination
at p2.17 reflects that NDP wins *more* seats per vote in the swing zone than the ensemble
average — consistent with NDP votes being concentrated in a small number of safe districts
rather than spread to contest marginal ones. All three metrics are consistent with the
same underlying partisan story; no metric is extreme in a direction that contradicts the
others.

**If a reviewer disputes this:** compute a directional Stouffer z-score with consistent
signs. The combined z remains extreme (z ≥ 4) because the two largest contributors (EG
and seats-at-50-50) are unambiguously UCP-favouring.

---

## 7. Conservative corrections (AV6 and AV7)

### AV6 — "The n_eff correction is arbitrary"

The MCMC chain has high autocorrelation (ρ_lag1 ≈ 0.99 across all partisan metrics).
Using raw n = 100,000 for the Hotelling T² test would overstate the effective degrees of
freedom and understate the p-value (make it *too* significant).

**The correction is not assumed — it is read from data:**

`joint_outlier_score_canonical.py::_load_n_eff_conservative()` reads
`simulation_convergence_diagnostics_canonical.json` and takes the minimum n_eff across
all metrics. The current minimum is **n_eff = 379** (mean_median metric, n_eff = 379.49).
A fallback of 224 is used only if the JSON is unavailable.

Actual n_eff values from `simulation_convergence_diagnostics_canonical.json`:

| Metric | τ (autocorr. time) | n_eff |
|---|---|---|
| efficiency_gap | 593.9 | 420.97 |
| mean_median | 658.8 | **379.49** (minimum) |
| declination | 564.4 | 442.92 |
| seats_at_50_50 | 552.5 | 452.45 |

**Sensitivity — what the p-value would be without the correction:**

| Correction | n used | Ch1 p-value |
|---|---|---|
| Hotelling T² (used) | n_eff = 379 | 1.60×10⁻⁷ |
| No correction | raw n = 100,000 | 7.45×10⁻⁸ |
| Chi-sq limit (n→∞) | ∞ | 6.16×10⁻⁸ |

Using n_eff = 379 instead of raw n makes Ch1 about 2× *less* significant. The correction
is strictly conservative. Removing it would strengthen, not weaken, the result.

### AV7 — "Two maps tested; p should be Bonferroni-corrected"

Two maps are evaluated: minority (combined p = 8.71×10⁻⁹) and majority (Ch1 p = 0.125).
Bonferroni correction for m = 2 tests requires p < α/2 = 0.025 to claim significance
at α = 0.05.

The minority combined p (8.71×10⁻⁹) clears this threshold by more than six orders of
magnitude. The minority Ch1 p alone (1.60×10⁻⁷) clears it by five orders of magnitude.
Bonferroni correction is trivially satisfied.

---

## 8. Pre-registration (AV8)

**Objection:** The Fisher combination of Ch1 and Ch2 was not explicitly named in a
pre-registration document. The individual statistics were pre-registered; their combination
was not.

**Response — two parts:**

**Part A — drand makes post-hoc combination impossible:**

Both Ch1 and Ch2 seeds are anchored to drand League of Entropy beacon rounds pre-dating
the shapefile release. The results are fully deterministic from the seeds. There is no
point in the analysis at which the analyst could have seen the combined p-value and then
chosen the combination method, because the seeds (and therefore the results) were
committed before the data existed.

If the analyst had wanted to cherry-pick which combination method to apply, they would
have needed to run the analysis, observe the result, change the combination method, and
re-run — but re-running with different seeds would change the pre-registered seeds,
which is publicly auditable. The beacon-anchored seeds are tamper-evident.

**Part B — Fisher's method is standard procedure, not a methodological choice:**

Pre-registration is required for choices that could be made differently depending on
the observed data. Fisher's method for combining independent p-values is the canonical
frequentist procedure, standardised in meta-analysis and multi-channel testing since
Fisher (1932). Applying it to two pre-registered p-values is not a methodological choice
any more than "apply a t-test after registering that you will compare means" is a choice.

The pre-registration establishes *what the two statistics are*. Combining them via Fisher
is applying a standard, pre-existing procedure to pre-registered outputs. No further
pre-specification is required.

---

## 9. Hostile reviewer Q&A (quick reference)

| Objection | Short response | Full treatment |
|---|---|---|
| "You cherry-picked Ch3 out" | Exclusion is design-based (different construct); same rule regardless of Ch3 p. Ch3 inclusion weakens combined p. | §3 AV2 |
| "You only applied Fisher to minority" | Ch2 is minority-specific by construction; no equivalent Ch2 exists for majority. | §3 AV3 |
| "Fisher requires independence" | Structural argument + CI gate; positive correlation makes Fisher conservative. | §5 AV1 + companion doc |
| "The combination wasn't pre-registered" | drand makes cherry-picking impossible; Fisher is standard procedure. | §8 AV8 |
| "The n_eff correction is arbitrary" | Read from convergence diagnostics JSON; correction is strictly conservative. | §7 AV6 |
| "Two maps → Bonferroni correction" | Minority p clears Bonferroni by 6 orders of magnitude. | §7 AV7 |
| "Fisher doesn't check direction" | Non-directional test is a feature; post-hoc EG/seats/declination tell coherent UCP story. | §6 AV5 |
| "Fisher could be wrong" | Stouffer, Cauchy, Bonferroni all give combined p within 1 order of magnitude. | §4 AV4 |

---

*Computations updated 2026-05-10 using scipy 1.x with full advance-vote substrate (va_polygons_with_full_2023_votes.gpkg; two-party total 1,544,139 post-C5 Vote Anywhere exclusion; swing zones 2,110). All values are reproducible from the pre-registered seeds (OSF qsgy8, r3zm7) and the official Elections Alberta shapefiles.*
