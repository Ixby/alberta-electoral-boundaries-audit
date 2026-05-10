# Ch1-COMP: Inter-Map Comparison Permutation Test

**Purpose:** Full documentation of the inter-map partisan-bias comparison test —
methodology, pre-registration chain, results, and anticipated reviewer objections.

**Pre-registration:** OSF [yvc7g](https://osf.io/yvc7g), git ba0e686, drand seed
1823538405 (salt "ch1-comp").

**Result:** SUPPORTED at classical threshold on both versions. V-A p = 0.0303;
V-B p = 0.0001.

**Script:** `analysis/scripts/intermap_permutation_test.py`
**Output:** `analysis/reports/intermap_permutation_test_results.json` + `.md`

*Last updated: 2026-05-10*

---

## 1. What the test claims

**H₀:** The minority and majority commission proposals differ in their joint
partisan-metric position by no more than randomly drawn pairs of constraint-legal
neutral maps from the canonical ensemble.

**H₁ (pre-specified direction):** The minority-majority gap exceeds the 95th
percentile of random neutral-plan-pair distances, with the minority more
UCP-favorable.

**Pre-commitment:** The result is reported regardless of direction, per the
TODO.md Ch1-COMP specification entered before the test ran.

This is not the same question as Ch1 (absolute position). Ch1 asks: "is the
minority map an outlier relative to the neutral ensemble?" Ch1-COMP asks: "do
the two commission maps differ from each other more than randomly chosen neutral
plans differ from each other?" A Yes on Ch1-COMP means the asymmetry between the
maps is not an artefact of both maps being extreme in the same direction — they
are genuinely separated in partisan-metric space.

---

## 2. Pre-registration chain

| Event | Detail |
| --- | --- |
| drand beacon infrastructure committed | 2026-04-27 09:49 (salt framework; predates shapefiles by 9 days) |
| Official EA shapefiles received | 2026-05-06 09:51 (Raymond Mok, Elections Alberta) |
| Canonical ensemble computed | 2026-05-06 to 2026-05-07 (250k steps, seed 1432864451) |
| OSF yvc7g pre-registration filed | 2026-05-10 (before this test run) |
| git ba0e686 committed | 2026-05-10 (test script + pre-registration record) |
| `intermap_permutation_test.py` run | 2026-05-10 |

The drand seed 1823538405 is derived as `SHA256(randomness_hex + "ch1-comp")[:4]`
where `randomness_hex` is the Cloudflare League of Entropy beacon at round 5500000.
The beacon round is immutable and public; any reviewer can verify the seed
independently at `https://drand.cloudflare.com/public/5500000`.

---

## 3. Test design

### 3.1 Two versions

The pre-registration specifies two versions with different test statistics and
different expected power.

**Version A (EG-only, one-tailed):**
T_A = EG(minority) − EG(majority)
Null: draw 10,000 random ordered pairs (i, j) from the ensemble; compute
EG(i) − EG(j). The null is symmetric around 0 by construction (random ordering).
p = fraction of null pairs with EG-diff ≥ T_A.

*Honest pre-run prediction (recorded in TODO.md):* "Honest prediction: likely
fails (typical pair gap ~2.8 pp > 1.42 pp)." The prediction was based on the
DPG-era EG difference of 1.42 pp. The canonical run produced 3.92 pp (larger
gap due to official geometry), which exceeded the null 95th percentile. Version A
was expected to fail and it passed.

**Version B (Mahalanobis joint, one-tailed in distance):**
T_B = ||Σ⁻¹/²(v_min − v_maj)||
where v = [EG, MM, declination, seats@50/50] and Σ is the ensemble covariance.
Null: same 10,000 random pairs; compute T_B for each pair.
p = fraction of null pairs with T_B ≥ observed T_B.

Mahalanobis distance is always non-negative, so the test is one-tailed in distance
(equivalent to a two-tailed directional test in metric space). All four partisan
metrics enter jointly; the direction check (fraction of metrics with minority more
UCP-favorable) is a post-hoc characterisation, not a pre-specification.

### 3.2 Why random pairs, not a fixed null distribution

An alternative design would compare T_A or T_B to a parametric null (e.g.,
chi-squared). The random-pair approach is preferred because:

1. It uses the same ensemble that anchors Ch1, requiring no additional assumptions.
2. The null distribution of inter-plan distances is not chi-squared in finite
   samples with the estimated covariance — the random-pair empirical null is exact.
3. It directly answers the question of interest: "do these two maps differ more
   than typical random-plan pairs?" without invoking asymptotic approximations.

---

## 4. Results

### 4.1 Observed metric values

| Metric | Minority | Majority | Delta (min − maj) | Direction |
| --- | --- | --- | --- | --- |
| Efficiency Gap | +0.0402 | +0.0010 | +0.0392 (+3.92 pp) | Minority more UCP-favorable |
| Mean-Median | +0.0104 | −0.0362 | +0.0466 (+4.66 pp) | Minority more UCP-favorable |
| Declination | −0.0770 | +0.0267 | −0.1037 | Majority more UCP-favorable |
| Seats@50/50 | +0.5169 | +0.4607 | +0.0562 (+5.62 pp) | Minority more UCP-favorable |

3/4 metrics show minority more UCP-favorable. Declination reverses: see §5 below.

### 4.2 Version A (EG-only)

| | Value |
| --- | --- |
| Observed EG gap | +3.92 pp |
| Null SD | 2.12 pp |
| Null 95th percentile | +3.43 pp |
| z-score | 1.849 |
| p (one-tailed) | **0.0303** |
| p (two-tailed) | 0.0647 |
| Significant at α = 0.05 | YES |

The observed gap (+3.92 pp) exceeds the null 95th percentile (+3.43 pp) by
0.49 pp. The result is significant but marginal. Version B provides the stronger
confirmation.

### 4.3 Version B (Mahalanobis joint)

| | Value |
| --- | --- |
| Observed Mahalanobis distance D | 7.19 |
| Null mean distance | 2.66 |
| Null SD | 0.98 |
| Null 95th percentile | 4.38 |
| p | **0.0001** |
| Significant at α = 0.05 | YES |

The observed D = 7.19 is 4.61 null-SD above the null mean — well outside the null
distribution. This result is not marginal.

### 4.4 Contextual comparison

| Test | Map | D | p |
| --- | --- | --- | --- |
| Ch1 absolute position | Minority | 5.71 | 1.46×10⁻⁶ |
| Ch1 absolute position | Majority | 2.79 | 0.100 |
| Ch1-COMP inter-map | Minority vs Majority | **7.19** | **0.0001** |

The inter-map distance (7.19) exceeds each map's individual distance from the
ensemble centroid (5.71 and 2.79 respectively). This is geometrically interpretable:
the two maps are not both sitting on the same side of the ensemble — they are
positioned on opposite flanks, so the distance between them is larger than either
map's distance to centre. This is consistent with the direction reversal on MM
(minority UCP-tail, majority NDP-tail) and on declination.

---

## 5. Declination direction reversal

Declination is the only metric where the majority map is more UCP-favorable than
the minority (delta −10.37 pp; majority declination +0.027, minority −0.077).

This does not undermine the test result. The Mahalanobis distance uses the full
covariance matrix, including the negative correlation structure between declination
and the other three metrics. The reversal is expected from asymmetric-packing
theory and is documented in §5.4.9 and the §6.2.1 direction-disagreement
reconciliation before this test ran.

Mechanically: EG and seats@50/50 respond to narrow-loss-district packing
(whether NDP votes are concentrated in heavy losses). Declination responds to the
winning-margin angle (whether the UCP wins by larger margins relative to the NDP's
winning margins). A map can concentrate NDP votes in a small number of
safe districts (high EG) while simultaneously giving NDP narrow wins in its safe
seats (low declination). These are geometrically different properties of the same
boundary placement. The minority map appears to do both simultaneously: it packs
NDP votes in a small number of safe seats (EG extreme) AND those safe seats produce
narrower NDP margins than UCP margins (declination reversal). The majority map does
neither as strongly.

---

## 6. Relationship to other channels

| Channel | What it tests | Direction vs Ch1-COMP |
| --- | --- | --- |
| Ch1 absolute (Mahalanobis) | Minority position vs neutral ensemble | Different question — absolute outlier status |
| Ch2 SZAT | Swing-zone allocation vs shuffle null | Different question — causal mechanism in swing zones |
| Fisher (Ch1+Ch2) | Joint significance of Ch1 and Ch2 | Different question — combined p for minority |
| **Ch1-COMP** | **Minority vs majority, vs random neutral pairs** | **Confirmatory — is the asymmetry itself significant?** |

Ch1-COMP is not a substitute for Ch1 or Fisher. Its role is confirmatory: once Ch1
establishes that the minority is an outlier, Ch1-COMP establishes that the two maps
are not outliers in the same direction from the same cause. The minority-majority
asymmetry is a real feature of the map pair, not an artefact of both maps being
drawn under the same geographic constraints.

Ch1-COMP is not included in the BH correction battery (§4.3.1) because it is
derived from the same ensemble as Ch1, not an independent test.

---

## 7. Anticipated reviewer objections

### AV1 — "The one-tailed direction was chosen after seeing preliminary results"

**Response:** The direction (minority more UCP-favorable) is entered in the
pre-registration and in the TODO.md Ch1-COMP specification before the test ran.
The honest pre-run prediction — recorded in writing — was that Version A would
*fail* (too small a gap). The test passed despite the pessimistic prediction.
Cherry-picking a direction to make a test fail is not the usual objection.

### AV2 — "Version A barely passed; the finding is marginal"

**Response:** Version A p = 0.0303 is marginal. Version B p = 0.0001 is not.
Both versions are reported per pre-commitment. The finding rests on Version B,
which uses all four metrics jointly and is comfortably significant. Version A
is reported for completeness and because the pre-registration specified both
versions independently.

### AV3 — "Declination reversal undermines the direction pre-specification"

**Response:** The pre-specification is for the direction of the joint test (Version B
distance, which is non-negative) and for Version A (EG only). The per-metric
direction breakdown is a post-hoc characterisation, not part of the pre-specified
hypothesis. The declination reversal is consistent with established theory
(§5.4.9 asymmetric-packing discussion) and does not change the p-values.

### AV4 — "Ch1-COMP doesn't add anything Ch1 doesn't already provide"

**Response:** Ch1 establishes that the minority map is an outlier relative to
the neutral ensemble. Ch1-COMP tests a different claim: that the two maps are
further apart in partisan-metric space than randomly chosen neutral-plan pairs.
If both maps were equally extreme in the same direction (e.g., both near the same
corner of the metric space due to shared geographic constraints), Ch1 would fire
but Ch1-COMP would not. Ch1-COMP firing means the asymmetry between the maps is
a genuine feature, not a shared constraint artefact.

### AV5 — "Random pairs from the ensemble are not independent"

**Response:** The random pairs are drawn independently from the ensemble using the
pre-registered seed. The individual plans within the ensemble are spatially
autocorrelated (MCMC moves one district at a time), but the 10,000 pair indices
are drawn with `np.random.default_rng(seed).integers(0, n, size=10000)` — the
pair selection is independent. The null distribution is therefore an empirical
estimate of the true random-pair distance distribution under the ensemble's
spatial structure, not a parametric approximation that ignores autocorrelation.

### AV6 — "The OSF pre-registration postdates the canonical ensemble"

**Response:** True — OSF yvc7g was filed 2026-05-10, after the canonical ensemble
was computed (2026-05-06 to 2026-05-07). The provenance claim does not rest on
the OSF timestamp. It rests on the drand seed: 1823538405 is derived from the
League of Entropy beacon at round 5500000, which is an immutable public record.
Any observer can recompute `SHA256(randomness_hex + "ch1-comp")[:4]` and
verify the seed is not chosen to produce a particular result — it is derived
from a beacon output that predates the ensemble. The OSF record establishes
methodology and direction pre-specification; the beacon establishes randomness
non-cherry-picking.

---

## 8. What this finding does not mean

- Ch1-COMP does not establish intent. A significant inter-map distance means the
  two maps are different in partisan-metric space; it does not explain why.
- Ch1-COMP is not the primary significance finding. The load-bearing test is Ch1
  (minority absolute position, p = 1.60×10⁻⁷) and Fisher (Ch1+Ch2, p = 1.55×10⁻⁸).
  Ch1-COMP is confirmatory.
- Version A marginal significance (p = 0.0303) should not be read in isolation
  from Version B (p = 0.0001). Both versions are reported because both were
  pre-specified; the joint picture is the finding.

---

*Companion documents:*
- `fisher_combination_defense.md` — Fisher combination methodology (Ch1+Ch2)
- `fisher_independence_defense.md` — independence assumption defense
- `analysis/reports/intermap_permutation_test_results.md` — full numerical output
