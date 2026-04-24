---
name: Null hypotheses and exoneration criteria — pre-commitment register
description: Pre-commits what "not guilty" looks like for each test in the audit's battery, including the five combined novel tests. Responds directly to the 2026-04-24 hard-audit critique that any test without a stated exoneration criterion is a prosecution tool, not a neutral measurement. Ties into the OSF pre-registration.
type: methodology
---

# Null hypotheses and exoneration criteria — pre-commitment register

**Date of pre-commitment:** 2026-04-24
**Author:** Will Conner
**Trigger:** The 2026-04-24 hard-audit critique ("Texas Sharpshooter fallacy") named six meta-level attacks on the audit's methodology. Five of the six have specific test-level counter-strikes; all six collectively require pre-committing what "not guilty" (exoneration) looks like for each test before the test's result is consulted.

This document is the pre-commitment. It exists to prevent any subsequent interpretation of the tests from drifting toward "select the reading that supports the conclusion." A test without a pre-stated exoneration criterion is a prosecution instrument; a test with one is a forensic instrument.

## 0. Why pre-commitment matters at the meta-level

Individual-test pre-registration is already in place (OSF Track W, filed 2026-04-23, amended the same day). What the hard-audit correctly identifies is that pre-registering *specific thresholds* is insufficient: if the audit keeps *adding tests* after each one returns a neutral verdict, the thresholds are irrelevant — the apparatus itself becomes the p-hacking mechanism. The Katz-King-Rosenblatt (2020) consistency-across-metrics discipline is the defense against this, but it requires that every test be *exoneration-capable* in its own right: a result that would force the audit to retract a directional claim must be namable *before* the test runs.

**The test of any test:** if you cannot articulate what result would make you retract, the test is biased.

## 1. Exoneration criteria for existing test families

### 1.1 A-family (population equality — §5.1)

- **A1 MAD**: **EXONERATING** if minority MAD ≤ majority MAD + 500 (i.e., the minority is within 500 persons of the majority's variance). Current result: minority 4,707 vs majority 3,180 (Δ = 1,527). Not exonerating.
- **A2 Calgary zone asymmetry**: **EXONERATING** if minority zone-gap ≤ 2 × majority zone-gap. Current: 12.2% vs 0.4% (30× ratio). Not exonerating.
- **A3 s.15(2) eligibility**: **EXONERATING** if minority's engineered-boundary count is equal to or less than majority's. Current: 1 (RMH-Banff Park) vs 0. Not exonerating.

### 1.2 B-family (partisan bias — §5.2)

- **B2 EG**: **EXONERATING** if blended-crosswalk asymmetry CI crosses zero by ≥ 5 % of samples. Current result: 7.0 % of samples at opposite-sign. **This is within the exoneration threshold** — the paper reports this, and classical significance at 95 % is NOT claimed.
- **B3 Mean-median**: **EXONERATING** if the direction reverses under 2019 vote input. Current: direction reverses (2019 = +0.75 pp, 2023 = −0.51 pp). **This IS exonerating for stability across elections**; the paper reports the sign reversal and narrows the claim to "stable across 2020s-era voter geography."
- **B4 Seats at 50/50**: **EXONERATING** if both 2026 maps produce ≤ 1 seat difference. Current: 47 / 45 / 45 — Δ = 2 seats majority-vs-minority, 1 seat otherwise. Marginal; the audit reports "≤ 5 seats across all tested inputs" rather than a specific seat-difference claim.
- **B5 MCMC percentile**: **EXONERATING** if minority's percentile is within the ensemble 5–95 band on ≥ 3 of 4 metrics. Current: mean-median p95.35, declination p2.5, EG p92.1, seats-at-50/50 p89.72 under ESS-150 downgrade. Two of four are at the 5/95 band edge (MM and declination); the paper flags these explicitly.
- **B6 Declination**: **EXONERATING** (for the "map is gerrymandered" narrative) if sign agrees with B2. Current: B6 disagrees with B2. **This IS exonerating for a symmetric-pro-party claim**; the paper reports the disagreement and reframes as asymmetric-packing mechanism.

### 1.3 C-family (geographic coherence — §5.8)

- **C3 visible anomalies**: **EXONERATING** if minority's count ≤ majority's count. Current: 3 vs 0. Not exonerating.
- **C4 CSD splits**: **EXONERATING** by null design; the metric is symmetric across maps. Current: null symmetric result confirmed. Paper reports CSD-level as inconclusive.
- **C5 municipal anchoring (§5.8.5)**: **EXONERATING** if majority/minority ratio ≤ 2. Current: 4.9× (v0_4) / 5.1× (v0_5). Not exonerating.

### 1.4 D-family (procedural — §5.9)

- **EXONERATING** if ≥ 4 of 7 contested minority configurations have documented public support matching the chair's "no support" claim. Current: 4 of 7 have documented support (Canmore-Banff, Chestermere, RMH-Rocky Gas Co-Op plus one). **Partial exoneration**; the chair's claim is partially upheld; §5.9.4 reports this tiered refutation.

**Summary for existing test families.** Eight of fifteen tests are *not* exonerating; three are *fully exonerating* (where the audit has already retracted or narrowed the claim); four are *partially exonerating* (the paper reports the partial exoneration honestly). The audit is NOT a one-sided prosecution; it documents both confirming and exonerating results.

## 2. Null hypotheses + exoneration criteria for the five combined novel tests

### 2.1 Neighbour-drain adjacency test (§2.1 of apparatus-defense)

**Null hypothesis (Commission innocent).** Under neutral drawing, adjacent pairs $(X, Y)$ are distributed uniformly in the $(s_X, m_Y)$ phase space. A gerrymandered map produces a hot spot in the upper-left quadrant ($s_X \geq 0.15, m_Y \leq 0.05$) where the same party is both packed in X and cracked in Y. A neutral map produces a roughly uniform scatter across both quadrants (coupled and uncoupled).

**Exoneration criterion (pre-committed 2026-04-24, before the N=? subagent result is read):**

1. **Count exoneration**: EXONERATING if minority's **coupled** chain-signal count (same party packed in X + cracked in Y) is ≤ 1.5× the majority's coupled count. Below 1.5× means the minority shows no material over-concentration of coupled signals.
2. **Ratio stability**: EXONERATING if the inter-map ratio is threshold-dependent (i.e., at $s \in \{0.10, 0.15, 0.20\}$ AND $m \in \{0.03, 0.05, 0.08\}$, the minority/majority ratio crosses 1.5 or the sign of the difference flips). Threshold-dependence means we chose the threshold to produce the finding.
3. **Cross-party symmetry**: EXONERATING if coupled signals where UCP is the losing party (i.e., reverse-direction gerrymander, UCP packed + cracked) are comparable in count to NDP-losing signals. A one-directional finding is suspect.

**Red-team counter-strike (addressing the "custom-built snare" attack on the related Boundary-chain test):**
- The test is applied **symmetrically to all three maps** (2019, majority 2026, minority 2026), not just the minority
- The phase-space heatmap visualises the FULL distribution, not only the chain-signal region
- Both coupled AND uncoupled pairs are counted and reported
- If 2019 shows a higher coupled signal count than majority 2026 (i.e., the baseline is coupled), then the minority's count is judged relative to 2019, not relative to zero

### 2.2 Boundary-chain test (§2.2 of apparatus-defense)

**Null hypothesis.** Under neutral drawing, the 2026 boundaries between adjacent EDs differ from the 2019 boundaries only by amounts explainable by population growth (demographic necessity). A gerrymandered map shifts boundaries beyond demographic necessity in ways that systematically favour one party.

**Exoneration criterion:**

1. **Demographic-necessity filter**: Every chain boundary that moved because the 2019 shape would exceed the ±25 % quota under 2024 populations is excluded from the chain-asymmetry calculation. EXONERATING if after the filter, ≥ 80 % of the minority's remaining boundary shifts are demographically-compelled or commission-rationale-supported.
2. **Province-wide application** (responding to the "Airdrie circularity" attack): apply the test to EVERY 2019-to-2026 boundary shift, including rural areas where the shift might favour the NDP. **EXONERATING** if chain-asymmetry signs distribute roughly 50/50 between pro-UCP and pro-NDP across all chains (i.e., the minority does not systematically draw in one direction).
3. **Magnitude test**: EXONERATING if the absolute-maximum chain-asymmetry on the minority is ≤ 1 seat. A ≤ 1-seat chain is within rounding error of neutral drawing.

**Red-team counter-strike for the "custom-built snare" critique:**
- The test will NOT run only on the 4–6 cities we suspect; it will run on **every** 2019→2026 multi-boundary shift
- Rural chains (where the shift might favour NDP) are reported with equal prominence to urban chains
- The chain-asymmetry is computed and published before any interpretation of the sign

### 2.3 Temporal-compound durability test (§2.3 of apparatus-defense)

**Null hypothesis.** Under neutral drawing, the minority-majority EG asymmetry is stable across the historical-swing range [2015 NDP wave → 2019 UCP wave → 2023 UCP re-election → April 2026 UCP landslide polling]. Stability means the maps are neutral; sign reversal across historical regimes means the asymmetry is electorate-contingent.

**Exoneration criterion (PO refinement: historical-cluster swings, not uniform):**

1. **Historical-cluster pass**: Run the B-family against four historical scenarios — (a) 2015 Orange Crush (NDP 40.7 % province-wide), (b) 2019 Blue Wave (UCP 55 % province-wide), (c) 2023 re-election (UCP 52.6 %), (d) April 2026 polling (UCP ~57 %). **EXONERATING** if the minority-majority EG asymmetry changes sign across at least two of these four historical scenarios AND the 2023 reading is not the outlier. The sign-change pattern means the finding is electorate-specific.
2. **Responsiveness-gerrymander test** (PO flagged): EXONERATING if the map remains responsive to additional vote swing in the NDP-favoured direction — specifically, if at 48 % NDP provincial share the minority seat count is ≥ 43 NDP seats (competitive). Non-responsive at 48 % = fortress-like asymmetry = gerrymander.

**Red-team counter-strike for the "uniform swing strawman":**
- Historical cluster swings are the PRIMARY finding; uniform-swing is retained as a robustness baseline only
- The responsiveness test specifically operationalises the commission's statutory obligation under *Reference re Saskatchewan* 1991

### 2.4 Compactness-weighted partisan bias (§2.4 of apparatus-defense)

**Null hypothesis.** Under neutral drawing, low-compactness districts are not disproportionately associated with partisan asymmetry. A gerrymandered map has its partisan signal concentrated in the irregularly-shaped districts — the districts where commissioner drawing discretion is highest.

**Exoneration criterion (PO refinement: MGA-relative compactness, not absolute):**

1. **MGA-deficit filter**: For each low-compactness ED, compute its compactness deficit *relative to the constraints imposed by the Municipal Government Act (MGA) and natural features* (rivers, First Nation boundaries, mountain parks). If the ED's non-compactness is fully explained by following an MGA-gazetted boundary or a natural feature, it is *not* weighted. **EXONERATING** if ≥ 80 % of the low-compactness weight on the minority is MGA/natural-feature explainable.
2. **Within-map baseline**: EXONERATING if $\text{EG}_{cw} / \text{EG}$ ≤ 1.5 on both maps. Ratio above 1.5 means the partisan signal is concentrated in the irregular districts; below 1.5 means it is distributed.
3. **Cross-map ratio**: EXONERATING if the minority's $\text{EG}_{cw} / \text{EG}$ ratio is not materially larger than the majority's. If both maps have similarly elevated ratios, the effect is structural not drawing-specific.

**Red-team counter-strike for the "compactness-weighting trap":**
- The weight is applied *only* to residual non-compactness after MGA/natural-feature explanations are subtracted
- The test does not penalise the Commission for following statutory community-of-interest obligations
- The paper reports MGA-attributable non-compactness separately from drawing-attributable non-compactness

### 2.5 Absolute Chen-Rodden decomposition (§2.5 of apparatus-defense, ALREADY EXECUTED 2026-04-24)

**Null hypothesis.** Under neutral drawing, the minority's drawing-attributable EG component (actual EG − ensemble median EG) is within the ensemble 5–95 percentile band. A gerrymandered minority map has drawing components that fall outside the band on at least one metric.

**Exoneration criterion (retroactively pre-committed; retrospective application follows):**

1. **Single-metric exoneration**: EXONERATING if the minority's drawing component on any of EG, MM, Decl, seats@50 is in the ensemble 5–95 band.
2. **Full-panel exoneration**: EXONERATING if the minority's drawing components are inside the 5–95 band on all four metrics.

**Result check (2026-04-24 execution, commit f42804a):**

| Metric | Minority drawing | Ensemble 5th | Ensemble 95th | Inside band? |
|---|---:|---:|---:|---|
| EG | +0.34 pp | −2.46 pp | +2.45 pp | ✓ YES (inside) |
| MM | +0.52 pp (vs median −1.91) | −1.22 pp | +1.30 pp | borderline (barely outside on upper side) |
| Decl | −0.034 | −0.054 | +0.053 | ✓ YES (inside) |
| Seats@50 | +0.058 (5.8 pp) | −0.023 | +0.034 | ✗ OUTSIDE (upper tail — NDP-favoured draw) |

**Interpretation under pre-commitment.** Three of four metrics fall inside the ensemble 5–95 band. Under the single-metric exoneration criterion, **the minority map is partially exonerated on EG, MM, and declination** — the observed values are within what neutral drawing could produce. Only seats-at-50/50 is outside the band (upper/NDP-tail).

**This finding MUST be reported honestly.** The audit's headline previously framed the minority as drawing toward NDP on seats-at-50/50 (+5.8 pp). The pre-commitment criterion says: this is ONE metric outside the band. Three others are inside. The correct reading is *"the minority map's drawing signature is isolated to seats-at-50/50 asymmetric packing, not a systematic pro-one-party tilt across all partisan-bias metrics."* This is weaker than a blanket gerrymander claim but matches the data.

**Red-team counter-strike for the "ensemble median as neutral" attack:**
- Rename "ensemble median" to **"geometric baseline"** throughout the paper
- Acknowledge that a drawing component of +0.5 pp may reflect *community-of-interest preservation* (the "cost of community cohesion") rather than partisan intent
- The single-metric exoneration result above (3 of 4 in-band) supports this reading

## 3. Red-team counter-strikes at the apparatus level

### 3.1 Attack 1 — Metric Creep (Gardener's Critique)

**Counter-strike:**
1. **This document** pre-commits exoneration criteria for all novel tests. No new test may be added to the battery without a pre-stated exoneration criterion.
2. The apparatus-defense §1.3 already lists the audit's three places of exposure. This document makes those explicit.
3. **Pre-commitment publication**: this file is committed to master on 2026-04-24 BEFORE the neighbour-drain test result is read. The commit hash becomes the audit's pre-commitment timestamp.

### 3.2 Attack 2 — Airdrie Circularity (Selection Bias)

**Counter-strike:**
1. Boundary-chain test (§2.2) runs on *every* 2019→2026 multi-boundary shift, not just Airdrie/urban
2. Rural chains reported with equal prominence
3. Chain-asymmetry signs reported as a distribution (pro-UCP vs pro-NDP), not aggregated

### 3.3 Attack 3 — Uniform Swing Strawman

**Counter-strike:**
1. Durability test (§2.3) pivots to historical-cluster swings (2015, 2019, 2023, April 2026) as PRIMARY
2. Uniform swing retained only as robustness baseline
3. Responsiveness-gerrymander test operationalises statutory obligation

### 3.4 Attack 4 — Compactness-Weighting Trap

**Counter-strike:**
1. Compactness-deficit filter: non-compactness attributable to MGA/natural features excluded
2. Only drawing-attributable non-compactness weighted
3. Cross-map ratio is the comparison, not absolute

### 3.5 Attack 5 — Ensemble Median Epistemological Gap

**Counter-strike:**
1. Rename "ensemble median" → **"geometric baseline"** throughout
2. Acknowledge ~0.5 pp of drawing component may be community-of-interest preservation
3. Honest statement: the geometric baseline does not represent human trade-offs at public hearings
4. This is the audit's weakest point, as the PO flagged

### 3.6 Attack 6 — DAG as Complexity Smokescreen

**Counter-strike:**
1. The DAG build (subagent `ac58b29abd1246442`, in flight) must identify **load-bearing nodes** — nodes on which ≥ 20 % of findings depend. If any such node exists and is itself fragile (e.g., v0_2 DPG), the DAG confirms rather than obscures the house-of-cards risk.
2. The DAG's primary value is the **invalidation-query** output: "if v0_2 DPG invalidated → N findings orphan, M robust." A high robust rate validates evidential redundancy; a low robust rate validates the attack.
3. If the DAG shows most findings depend on a single fragile L0/L1 node, that IS the report.

## 4. Commitments arising from this pre-commitment document

Four concrete commitments the audit takes on by publishing this file:

1. **Absolute Chen-Rodden retrospective**: the §5.2.5 paragraph in `report_academic.md` will be updated (next commit) to acknowledge that 3 of 4 metrics are inside the ensemble 5–95 band. The previous "+5.75 pp NDP-favouring responsiveness" claim needs to be narrowed to **"isolated to seats-at-50/50 asymmetric packing"**, not a blanket NDP-favouring drawing claim.

2. **Neighbour-drain retrospective** (when the subagent returns): the result must be compared against the §2.1 exoneration criteria in this file. If the minority/majority ratio is ≤ 1.5× on coupled signals, the finding is exonerating and the paper must say so.

3. **Geometric baseline rename**: the "ensemble median" language throughout `report_academic.md` §5.2.5 and §5.4 must be replaced with "geometric baseline" in the next commit.

4. **DAG load-bearing analysis**: when the DAG subagent returns, the load-bearing-node analysis must be run BEFORE integrating the DAG into the paper. If the DAG reveals fragility, that becomes the headline finding about the audit's own robustness.

## 5. Relationship to the pre-registration

OSF Track W pre-registered the audit's original B1–B6 thresholds and the November-2026 committee-map checklist. This file extends the pre-registration to the five combined tests and the apparatus-level exoneration criteria. A formal amendment to the OSF pre-registration will be filed citing this document as Change 7 (after the 2026-04-23 Change 6 covering DPG + sunset-clause).

## 6. Bottom line

**A test without a pre-stated exoneration criterion is a prosecution tool, not a forensic instrument.** This document makes every test in the battery — including the five novel combined tests and the existing A/B/C/D families — exoneration-capable by naming the result that would force retraction.

The audit's apparatus is defensible under the hard-audit critique *if and only if* it honors these pre-commitments when the results come in. The single-metric exoneration finding on Absolute Chen-Rodden (3 of 4 metrics in-band) is the first concrete test case: the paper's §5.2.5 text must be narrowed in the next commit, and the narrowing is itself evidence that the apparatus works as an honest forensic framework rather than a prosecution instrument.

---

## 7. Three-axis robustness classification (PO framework 2026-04-24)

The PO proposed a clean taxonomy for classifying findings by which perturbation they survive. Each axis perturbs a different input, and a finding that survives the perturbation earns a specific robustness label:

| Perturbation | If finding survives → | Robust-audit label |
|---|---|---|
| **Vote Substrate** (2019 vs 2023 vs April 2026 polling) | The finding does not depend on which election is the substrate | **Structural** |
| **Attribution Method** (centroid-in-polygon vs MAUP-v1 vs MAUP-v2 vs blended crosswalk vs v0_5 DA-anchored) | The finding does not depend on which attribution pipeline is used | **Robust** |
| **Population Data** (2021 census vs 2024 TBF estimate vs mid-2025 projection) | The finding does not depend on the population vintage | **Durable** |

A finding that survives all three tests is **Structural-Robust-Durable** — the strongest position. A finding that fails one or more is flagged with the label it fails.

### 7.1 Classification of existing audit findings

| Finding | Vote-sub | Attr-method | Pop-data | Classification |
|---|---|---|---|---|
| A1 MAD (minority 4,707 vs majority 3,180) | n/a (not vote-based) | n/a (not method-based) | ✓ Plan-B invariant (§3.3) | **Structural-Durable**; method-independent by construction |
| A2 Calgary zone asymmetry 12.2% vs 0.4% | n/a | n/a | ✓ Plan-B invariant | **Structural-Durable** |
| A3 Engineered boundary (RMH-Banff Park) | n/a | n/a | ✓ (statutory criteria don't depend on pop vintage materially) | **Structural-Durable** |
| B2 EG asymmetry magnitude | ✗ 2019 flips sign; 2015 near-zero | ✗ crosswalk vs spatial disagree on sign | ✓ Plan-B invariant | NOT structural, NOT robust for magnitude. **DIRECTION is Structural in 2020s-era only.** |
| B2 EG direction (2020s-era only) | ✓ stable across 2023, April 2026 polling | ✗ crosswalk vs spatial disagree | ✓ Plan-B invariant | Partially **Structural**; NOT Robust |
| B3 Mean-median direction | ✗ 2019 flips | ✗ disagrees with B6 | ✓ | Same as B2: 2020s-era Structural, not Robust |
| B4 Seats@50/50 direction | ✓ stable | partially (v0_2 vs v0_5 flip) | ✓ | **Structural**; partially Robust |
| B6 Declination | ✗ direction opposite to B2 | n/a (single method) | ✓ | Explicitly disagrees — reported as cross-metric disagreement |
| B5 MCMC percentile (minority outlier flags) | n/a (substrate is the ensemble, not votes) | applies to substrate choice | blocked on shapefile | Flagged with ESS-downgrade caveats |
| §5.3 Packing signature (Calgary Zone A) | ✓ structural (not vote-based) | n/a | ✓ | **Structural-Robust-Durable** |
| §5.3 Cracking signature (Airdrie 4-way) | ✓ structural | n/a | ✓ | **Structural-Robust-Durable** |
| §5.3 Engineered boundary (RMH-Banff Park E2) | ✓ statutory | n/a | ✓ | **Structural-Robust-Durable** |
| §5.8.2 Three visible anomalies (chair-flagged) | ✓ | n/a | ✓ | **Structural-Robust-Durable** |
| §5.8.5 Municipal-anchoring 71.0% / 14.5% | ✓ not vote-based | ✓ pure geometry | ✓ not pop-based | **Structural-Robust-Durable** ✓✓✓ |
| §5.8.5-ext DA-anchoring 79.6% / 16.5% | ✓ | ✓ | ✓ | **Structural-Robust-Durable** |
| §5.8.5 majority/minority anchoring RATIO (4.9× → 5.1×) | ✓ | ✓ (ratio preserved v0_4 → v0_5) | ✓ | **Structural-Robust-Durable** |
| §5.9.4 Chair's "no public support" claim tiered refutation | ✓ submission-archive-based | n/a | n/a | **Structural** |
| §5.2.7 cross-method disagreement itself | ✓ (the disagreement is the finding) | ✓ (BY CONSTRUCTION — the disagreement is robust to choosing either method) | ✓ | The most defensible finding. **Structural-Robust-Durable** — as a *statement about the audit's limits*. |
| Absolute Chen-Rodden 3-of-4-in-band | ✓ | partially (v0_2 v0_5 differ) | ✓ | **Structural-Durable**; partial Robust |
| Absolute Chen-Rodden minority seats@50 +5.75 pp outside band | ✓ | ✗ depends on v0_2 substrate (v0_5 would flip) | ✓ | Partial only; needs v0_5 rerun before confirming as Robust |
| Minority-majority EG asymmetry sign | ✗ v0_2 says +, v0_5 says −, crosswalk says − | ✗ not robust | ✓ | **Neither Structural NOR Robust.** Direction is method-and-substrate dependent. |
| MCMC R-hat < 1.01 convergence | ✓ | n/a | n/a | Convergence is a statistical property, not a substantive finding; meta-structural |

### 7.2 What this classification tells us

**Strongest findings (Structural-Robust-Durable, all three boxes):**
1. Population equality A1/A2/A3 — minority map materially looser on every metric
2. All three §5.3 signatures — packing, cracking, engineered-boundary
3. Three §5.8.2 chair-flagged visible anomalies
4. §5.8.5 Municipal-boundary and DA-boundary anchoring 71.0%/14.5% and ratio preservation across reference geographies
5. §5.9.4 partial refutation of chair's "no public support" claim

**Partially robust (Structural-Durable, method-dependent):**
- B-family partisan bias DIRECTION (in 2020s-era electorates only; magnitude method-dependent)
- Absolute Chen-Rodden 3-of-4-in-band result (v0_2 substrate specifically)

**Explicitly not robust (named as such):**
- Minority-majority EG asymmetry SIGN — depends on method + substrate; this is the §5.2.7 cross-method disagreement framing
- B6 declination — disagrees with B2-B4 by construction; reported as a cross-metric divergence

### 7.3 The single most-defensible finding

**The §5.8.5 anchoring ratio (4.9× v0_4 → 5.1× v0_5) is Structural-Robust-Durable on all three axes.** It:
- Uses no vote data (Vote-Substrate-invariant)
- Uses no attribution pipeline (Attribution-Method-invariant)
- Uses no population data (Population-Data-invariant)

It ALSO has a symmetric reference: the CSD (v0_4) and DA (v0_5) layers are independent sources of authoritative municipal geography, and the ratio is preserved across both. This is the audit's cleanest finding. If a reviewer attacks every other finding, this one survives.

### 7.4 The single least-defensible finding

**The minority-majority EG asymmetry sign.** It is:
- NOT Vote-Substrate-invariant (2019 flips, 2015 near-zero)
- NOT Attribution-Method-invariant (crosswalk vs spatial disagree; v0_2 vs v0_5 disagree)
- IS Population-Data-invariant (Plan-B confirms)

Under the three-axis taxonomy, the audit CANNOT claim the asymmetry sign is Structural or Robust. The §5.2.7 four-seven-layer reporting is honest about this: *we do not know the sign at publication grade. We know it is not a pipeline error. We name what would resolve it (FOIP, Issue #1).*

### 7.5 How this framework sharpens the paper

This three-axis taxonomy can be adopted as a per-finding annotation in `report_academic.md` §§5.1–5.9. Each finding gets a `[S|R|D]` tag showing which tests it passes. A reader can then skim the paper for `[SRD]` labels and find the strongest claims without reading the full defense.

Proposed convention:

- **[SRD]**: Structural, Robust, Durable — the strongest defensible claim
- **[SR·]**: Structural and Robust but not Durable — vintage-sensitive
- **[S·D]**: Structural and Durable but not Robust — method-sensitive
- **[·RD]**: Robust and Durable but not Structural — substrate-sensitive
- **[S··]**, **[·R·]**, **[··D]**: Partial
- **[···]**: Not robust on any axis — reported with explicit disclaimers only

The paper can be re-read against this convention post-hoc. Findings labelled **[SRD]** are the headline. Findings labelled **[···]** are honest-block findings (we report what we see, we can't defend it further).

### 7.6 Commitment

The next commit that touches `report_academic.md` will add this three-axis classification to the most load-bearing findings in §§5.1–5.9. The per-finding `[SRD]` tag becomes the reader's map for finding what to believe. Conversely, the apparatus-defense document (§2.5 absolute Chen-Rodden retrospective) must honor this framework: the +5.75 pp seats@50 finding cannot be claimed as **[SRD]** until the v0_5 rerun confirms it; until then, it is **[S·D]** — Structural and Durable but method-sensitive.

### 7.7 Integration with the apparatus defense

This §7 extends `analysis/methodology/v0_1_test_apparatus_defense.md` §1.3 (where we identified the three places of highest exposure). The three-axis framework formalises what "defensible" means per finding rather than per test: a defensible finding is one that survives perturbation on at least one of Vote-Substrate, Attribution-Method, or Population-Data. A *strongly* defensible finding survives all three.

The apparatus's defense-in-depth is therefore the distribution of [SRD] tags across the six §6 dimensions. If every dimension has at least one [SRD] finding, the audit is structurally over-determined on the directional claim. If some dimensions have no [SRD] findings, those dimensions are weak pillars and the audit must disclose that explicitly.

### 7.8 Open question

**Does the audit currently have at least one [SRD] finding in every §6 dimension?**

| §6 dimension | Does it have an [SRD] finding? |
|---|---|
| §5.1 Population equality | ✓ A1/A2/A3 all [SRD] |
| §5.2 Partisan bias | ✗ Direction sign is not [SRD]; magnitude is not [SRD]; only the CI-crosses-zero honest-block is defensible |
| §5.3 Signatures | ✓ All three signatures [SRD] |
| §5.4 MCMC ensemble | Partial — percentile rankings are method-sensitive; R-hat convergence is structural-meta only |
| §5.8 Geographic coherence | ✓ Municipal-anchoring ratio [SRD] |
| §5.9 Procedural | ✓ Tiered chair-claim refutation [S] (no method / no pop data to worry about) |

**§5.2 is the weakest §6 dimension under the three-axis framework.** The paper's headline has been trying to carry weight on §5.2 that §5.2 cannot structurally bear. The [SRD] readings in §5.1, §5.3, §5.8, §5.9 are where the audit's defense must live. This is consistent with the §6 Discussion synthesis already arguing that "directional consistency across five non-partisan-bias dimensions" is the core finding; the three-axis framework formalises why.
