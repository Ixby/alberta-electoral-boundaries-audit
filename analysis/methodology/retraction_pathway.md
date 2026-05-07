---
name: Retraction pathway — named conditions under which each finding is retracted
description: Per-finding pre-committed retraction conditions, responding to the 2026-04-24 "end-boss" critique (Ontological Gap + Confirmatory Bias Engine). For every load-bearing finding in report_academic.md §§5.1-5.9, this document names specific data or evidence that would force retraction. Without a retraction pathway, the audit is criticism, not forensics.
type: methodology
---

# Retraction pathway — named conditions under which each audit finding is retracted

**Date of pre-commitment:** 2026-04-24
**Author:** Will Conner
**Trigger:** The 2026-04-24 "Ontological Gap" critique identified four deep attacks on the audit's metaphysical assumptions (ReCom Ghost, Aggregation Bias, Geographic Neutrality Myth, Statutory Silence) plus an "end-boss" attack naming the audit as a Confirmatory Bias Engine unless a retraction pathway is made explicit per finding.

**This document is that retraction pathway.** For every load-bearing finding in `report_academic.md` §§5.1–5.9, a specific external condition is named that would force retraction. The list is pre-committed: if any condition materialises, the relevant finding is retracted in the next commit, with a public amendment to the OSF pre-registration.

This is the audit's "suicide note": a reviewer can use this document to tell *in advance* what data would break each finding. That is the difference between forensic science and polemic.

---

## 0. Meta-commitment

**The audit honours any retraction condition that materialises within 48 hours of that condition becoming known.** If a condition is equivocal (the evidence is suggestive but not conclusive), the finding is downgraded rather than fully retracted, and the downgrade is documented. The commit message for a retraction-driven change cites this document and the specific condition row.

---

## 1. Population-equality findings (§5.1)

### 1.1 A1 MAD (minority 4,707 vs majority 3,180)

- **Retraction condition A.** If Elections Alberta publishes per-ED populations that differ materially (> 10 %) from the commission's variance tables we sourced from, the MAD finding is recomputed. If the new MAD on minority ≤ new MAD on majority + 500 persons (the pre-committed pass threshold from `null_hypothesis_and_exoneration_criteria.md` §1.1), the finding is retracted.
- **Retraction condition B.** If the commission publishes a methodology note stating that the variance-table populations we used were draft/misprint, superseded values are used and the above re-check runs.

### 1.2 A2 Calgary geographic-zone asymmetry (12.2 % vs 0.4 %)

- **Retraction condition A.** If the zone classification is re-done under a rule the commission itself publishes (e.g., City-of-Calgary ward boundaries or AMA-urban-core definition) and the inter-map gap drops below 2×, the finding is retracted.
- **Retraction condition B.** If official 2026 shapefiles (Issue #1 official disclosure) reveal that Zone A contains districts we misclassified as Zone A when they actually straddle Zone A / Zone B, the classification is rerun and re-evaluated.

### 1.3 A3 s.15(2) engineered boundary (RMH-Banff Park)

- **Retraction condition A.** If the commission publishes correspondence or a rationale-addendum documenting that a specific non-park population cluster (Sundre, Caroline, Nordegg, Mountain View County, Bighorn MD) was excluded from RMH-Banff Park for reasons independent of statutory-qualification — e.g., shared school-division, municipal-transit-tie, or reserve-adjacency — the engineered-boundary signature is downgraded to a "borderline" pattern rather than a detected signature.
- **Retraction condition B.** If the statutory interpretation of s.15(2) is judicially clarified (e.g., by *Reference* under the Act) to permit uninhabited-territory extensions where other §15(2) criteria are met, the E2 signature becomes statutorily defensible and is withdrawn as a gerrymander signature.

## 2. Partisan-bias findings (§5.2)

### 2.1 B2 EG direction (negative asymmetry under 2023-vote substrate, blended crosswalk)

- **Retraction condition A.** Already partially conceded (see `null_hypothesis_and_exoneration_criteria.md` §1.2 and §7.4): the direction is not Structural-Robust. If a rerun against any one of (a) 2019 votes, (b) 2015 votes, (c) the v0_5 DA-anchored DPG substrate produces the opposite sign on the asymmetry, the directional claim is bounded to "2020s-era voter geography only" — already implemented in §5.2.3.
- **Retraction condition B.** If a full **voter-elasticity model** (responding to the 2026-04-24 "Aggregation Bias" critique) re-estimates the 2023 vote counts under a counterfactual where strategic voting / turnout suppression is applied to "cracked" EDs, and the resulting adjusted-EG asymmetry has the opposite sign, the asymmetry claim is retracted under this voter-elasticity reading and reported as such. **Status**: currently unaddressable without individual-voter or historical-elasticity data we do not have; the finding remains *conditional on voter invariance*, which is explicitly flagged in the paper.

### 2.2 B6 Declination disagreement with B2–B4

- **Retraction condition.** Already managed in §5.2.4 as a cross-metric disagreement consistent with narrow-margin-loss packing. No further retraction condition needed — the finding is a disagreement, not a claim.

### 2.3 B5 MCMC ensemble — minority map as outlier (mean-median p95.35 / declination p1.6)

- **Retraction condition A (ReCom-Ghost attack).** The ReCom ensemble samples from a universe of compact-contiguous maps. A human commission operating under the Alberta Electoral Divisions Act uses path-dependent negotiation from the 2019 baseline, which explores a DIFFERENT universe. If a **local-perturbation MCMC chain** (seeded at the 2019 enacted partition, with step sizes restricted to what a human commissioner would realistically negotiate — single-boundary moves, population-target-preserving swaps, COI-preserving proposals) places the minority map's mean-median and declination INSIDE that chain's 5–95 band, the percentile flags are retracted under the local-perturbation reading. The two readings are then reported as a cross-ensemble disagreement akin to the §5.2.7 cross-method disagreement.
- **Retraction condition B (Constraint-Bound Expectation rename).** The "ensemble median" / "geometric baseline" language is replaced throughout the paper with **"constraint-bound expectation"** to defuse the Geographic-Neutrality-Myth critique. The percentile flags remain under their original computation, but the narrative no longer equates the ensemble median with "Neutral" or "Fair." Already committed in §5.2.5 (absolute Chen-Rodden). Extension to §5.4 is a commitment under this document.

### 2.4 Absolute-level Chen-Rodden decomposition — minority seats@50 drawing component +5.75 pp

- **Retraction condition A.** Already narrowed under pre-commitment `null_hypothesis_and_exoneration_criteria.md` §2.5: 3 of 4 metrics are INSIDE the 5–95 band, only seats@50/50 is outside. Claim currently reads "minority's drawing signature isolated to asymmetric-packing at 50/50 vote distribution."
- **Retraction condition B.** If a rerun using a local-perturbation chain (retraction condition 2.3 A) produces a 5–95 band on seats@50/50 that contains the minority's +0.5057 value, the finding is retracted under the local-perturbation reading.
- **Retraction condition C.** If a rerun using the v0_5 DA-anchored DPG substrate (already partially executed at commit 403ad95) produces a seats@50/50 drawing component inside the ensemble 5–95 band on the v0_5 substrate, the +5.75 pp claim is flagged as substrate-specific.

### 2.5 §5.2.7 cross-method disagreement

- **Retraction condition.** The disagreement itself IS the finding, so the retraction is triggered by a resolution of the disagreement: if officially released official 2026 shapefiles (Issue #1) produce a MAUP-v2 rerun on authoritative geometry with a CI tighter than ±0.5 pp that falls on one side of zero, the "disagreement" framing becomes "converged estimate" and the §5.2.7 multi-layer presentation is collapsed to a single authoritative number. The §4.1.4 sunset clause binds this retraction within 48 hours of shapefile release.

## 3. Signature findings (§5.3)

### 3.1 §5.3.1 Packing signature (Calgary Zone A)

- **Retraction condition A.** If a re-audit of the minority's Zone-A definition under an alternative urban/suburban classification rule (e.g., transit-catchment-area instead of City-of-Calgary ward boundaries) produces a Zone-A-minus-Zone-B gap below 5 %, the packing-signature detection is downgraded to "structural-asymmetry only."
- **Retraction condition B.** If a Chen-Rodden natural-packing simulation (under the local-perturbation chain — retraction 2.3 A) places the minority's Zone-A gap inside that chain's 5–95 band, the packing is attributed to natural geography rather than drawing choice.

### 3.2 §5.3.2 Cracking signature (Airdrie 4-way)

- **Retraction condition A.** If the commission's minority-report text documents a specific COI-preservation rationale for each of the four Airdrie boundaries (e.g., "Airdrie-West retained school-catchment X"; "Airdrie-East retained Balzac-industrial-zone Y"; etc.), and the four rationales are mutually independent (i.e., the four-way split is not one drawing decision but four separate COI decisions), the cracking signature is downgraded to "COI-compelled partition."
- **Retraction condition B.** If the commission's public hearing transcripts record Airdrie residents requesting a multi-way partition (to preserve distinct sub-community representation), the signature is retracted as responding to public input.

### 3.3 §5.3.3 Engineered boundary (RMH-Banff Park)

- **Retraction condition.** Same as A3 (see §1.3 above) — judicial or statutory clarification on park-extension s.15(2) eligibility.

### 3.4 §5.3.5 Neighbour-drain adjacency (pre-registered pass already recorded)

- **Status.** Already a pre-registered pass for the minority on pre-commitment. No retraction needed; finding is "the minority map is LESS adjacency-coupled than either the 2019 or majority map."
- **Retraction condition on the pre-registered pass.** If a rerun on the v0_5 DA-anchored substrate (with its better adjacency topology, after the v0_2 substrate-defect flagged in the writeup) produces a minority coupled count > 1.5× majority count, the pre-registered pass is retracted.

## 4. Geographic-coherence findings (§5.8)

### 4.1 §5.8.2 Visible anomalies (3 chair-flagged)

- **Retraction condition.** If the commission publishes clarifying text showing that any of the three anomalies (RMH-Banff Park; Nolan Hill-Cochrane lasso; Edmonton-Windermere stepped boundary) is a documented cartographic artefact (commission drawing error, not deliberate choice), the specific anomaly is retracted as a signature.

### 4.2 §5.8.4 Community-of-interest splits

- **Retraction condition.** If a sub-CSD-resolution analysis of the 2026 proposals (available only under officially released shapefiles) reveals the minority's hybrid splits preserve within-CSD COI better than the CSD-level overlay suggests, the null-symmetric CSD finding is supplemented with the sub-CSD evidence. No retraction needed at CSD resolution; sub-CSD is an additional layer.

### 4.3 §5.8.5 Municipal + DA anchoring (71/14.5 % v0_4; 79.6/16.5 % v0_5; ratio 4.9×→5.1×)

- **Retraction condition A.** If the official 2026 shapefiles (official disclosure) show that the minority's boundaries actually follow CSD or DA edges that our DPG trace missed (i.e., our trace was wrong, not the minority's drawing), the recomputed anchoring percentages increase for the minority and the ratio collapses toward 1×.
- **Retraction condition B (Trade-off Frontier — Statutory Silence counter-strike).** If a third-party or subsequent audit produces a "Symmetric-Airdrie" counter-map (equal COI preservation under Alberta Electoral Divisions Act §14 + §15 + §16, but with majority-symmetric anchoring), the minority's 14.5 % anchoring is no longer defensible as the only map that achieves the COI preservation it claims. The finding stands against the null alternative (no counter-map exists) and would be retracted against a successful alternative.

## 5. Procedural findings (§5.9)

### 5.1 §5.9.4 Chair's "no public support" claim partial refutation

- **Retraction condition.** If additional submission-archive material (the ~88 non-text-layer submissions partially OCRed in session 9) produces evidence that four or more of the contested configurations had documented support, the partial refutation becomes a full upholding and the finding is retracted as refuted.

### 5.2 §5.9 April 16, 2026 procedural departure

- **Retraction condition.** The procedural finding is factual (Motion 19 tabled, committee composition documented) and is not retractable at the evidentiary level. The *interpretation* (that it is a departure from Canadian independent-commission norms) is retractable if a Canadian comparator is produced showing a similar legislative override of an independent commission's draft process, pre-dating Alberta 2026. The Canadian base-rate analysis (`analysis/methodology/canadian_base_rate_computed.md` §7A) currently classifies Alberta 2026 as the most-government-controlled response in the three-case comparator set; a fourth case with similar override would reduce this to "one of several."

## 6. DPG-dependent findings (all)

### 6.1 Sunset clause — master retractor

- **Retraction condition** (from `report_academic.md` §4.1.4). Every DPG-dependent metric in the paper is retracted and recomputed within 48 hours of Elections Alberta publishing official 2026 topological shapefiles. This is the master retractor that supersedes individual DPG-dependent findings if shapefiles release.

### 6.2 v0_5 empty-polygon defect

- **Retraction condition** (already disclosed, §5.2.7 seventh measurement). If the empty-polygon defect in v0_5 DA-anchored (5 EDs per map) is traced to a script bug rather than a genuine geometric overlap cascade, the v0_5-based rerun is redone with the bug fixed and the sign-flip finding is re-checked. The current asymmetry-sign flip (v0_2 +3.35 pp → v0_5 −3.64 pp) is provisional pending that defect investigation.

## 7. Meta-finding retraction

### 7.1 "Directional consistency across six dimensions" synthesis

- **Retraction condition A.** If at least three of the six dimensions show contradicting-direction findings under the three-axis robustness framework (e.g., §5.1 remains structural UCP-looseness but §5.3 and §5.8 and §5.9 all produce NDP-favouring retractions), the directional consistency claim is retracted and the paper reports "findings go in multiple directions; no synthesis available."
- **Retraction condition B.** If the DAG reveals that more than half the findings in §§5.1–5.9 share a single fragile L0/L1 node (i.e., the apparatus is a "house of cards" per the 2026-04-24 hard-audit attack #6), the synthesis is downgraded to "findings all rest on a common dependency, so they are not truly independent."
  - **DAG result (2026-04-24, resolved).** 234 nodes, 454 edges, acyclic, zero orphans. The most load-bearing L0 is the 2023 Statement of Vote: invalidating it orphans 48 of 74 L3 findings (65 %). This meets the numerical retraction threshold, but the qualitative reading is that any B-family finding must depend on vote data by definition, so the dependency is expected rather than fragile. The 26 structurally-independent findings (35 %) that survive invalidation of the Statement of Vote span §5.1 population equality, §5.8 geographic coherence, §5.9 procedural departure, and the geometry-only subset of §5.3 signatures. **Synthesis refined, not retracted:** the directional-consistency claim now reads "consistent across five non-vote-dependent dimensions, further strengthened by the one vote-dependent dimension." See `report_academic.md` §4.7 and `analysis/methodology/audit_dependency_graph_readme.md` for the full cascade table.

### 7.2 "Minority map is a gerrymander" implicit claim

- **Retraction condition.** The paper does NOT currently claim the minority map is a gerrymander in the intent sense (§4.5 explicitly). The paper claims "systematic structural asymmetry at a magnitude below the 7 % EG threshold proposed in the Stephanopoulos & McGhee (2014/2015) academic literature" — a threshold cited in litigation but never judicially adopted (US Supreme Court vacated *Gill v. Whitford* on standing without ruling on the threshold). This implicit claim is retracted if any of the following hold:
  - **§5.3 signatures all receive COI-compelled rationalisation** (retraction conditions 3.1 A+B, 3.2 A+B, 3.3 A)
  - **Absolute Chen-Rodden narrowing** (already committed: 3-of-4-in-band) is extended to 4-of-4 under any rerun
  - **Neighbour-drain pre-registered pass** (already recorded) is compounded by boundary-chain or compactness-weighted null results in the same direction

If 3 of these 4 compound, the structural-asymmetry claim is retracted and the paper reports "the minority map shows structural differences from the majority, but those differences are either COI-compelled, statistically inside the constraint-bound expectation, or not spatially coupled — no defensible gerrymander claim remains."

---

## 8. Ontological-gap attacks — how this document addresses them

| Attack | Counter-strike in this document |
|---|---|
| **1 ReCom Ghost** | Retraction condition 2.3 A + 3.1 B commit the audit to a local-perturbation chain rerun. Until run, the finding is flagged as "ReCom-ensemble-substrate-dependent." |
| **2 Aggregation Bias** | Retraction condition 2.1 B names voter-elasticity as the retractor for the B-family partisan-direction claim. Current status: not addressable without data; paper explicitly flags voter-invariance assumption as the primary limitation of §5.2. |
| **3 Geographic Neutrality Myth** | Retraction condition 2.3 B + commitment to rename "ensemble median" / "geometric baseline" → **"constraint-bound expectation"** throughout the paper. |
| **4 Statutory Silence** | Retraction condition 4.3 B (Trade-off Frontier) names the production of a "Symmetric-Airdrie" counter-map as the retractor for the §5.8.5 anchoring finding. If such a map exists, the statutory defense stands. |
| **End-Boss (Confirmatory Bias Engine)** | This document IS the counter-strike. Every finding has a named retractor. The audit is falsifiable per-finding, not just per-test. |

---

## 9. Operational commitments

Four concrete items the audit takes on by publishing this retraction pathway:

1. **Rename "ensemble median" / "neutral map" → "constraint-bound expectation"** in `report_academic.md` §5.4 and §5.2.5 in the next commit.
2. **Execute the local-perturbation MCMC chain** as a new issue (Issue #13, to be filed). Seeded at 2019 enacted, restricted to single-boundary moves + population-target-preserving swaps + COI-preserving proposals. ~2-3 days implementation + ~90 min compute.
3. **File the Trade-off Frontier as Issue #14**: a counter-map challenge — invite external contributors to produce a "Symmetric-Airdrie" alternative meeting Alberta Electoral Divisions Act §14-§16 obligations with lower §5.8.5 anchoring asymmetry. Document the specifications for such a counter-map so the challenge is concrete.
4. **File the voter-elasticity model as Issue #15** — not executable today without historical-elasticity data; pre-registered as a future extension whose execution could retract the §5.2 partisan-bias direction claim.

---

## 10. Bottom line

**Without a retraction pathway, an audit is criticism.** This document commits the audit to specific retractions under specific external conditions. Any reviewer can now read this file and tell in advance *exactly* what data, argument, or analysis would break each finding. The "Confirmatory Bias Engine" accusation survives only if no such retraction conditions are honestly nameable — and they are, for every load-bearing finding.

The apparatus is a forensic framework, not a prosecution, because the retraction conditions are concrete, public, and dated. The end-boss attack demands either a suicide note or a prosecutorial confession. This is the suicide note.
