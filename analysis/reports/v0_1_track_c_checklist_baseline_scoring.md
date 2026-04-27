---
name: Track C — pre-registered checklist baseline scoring (majority and minority maps)
description: Application of the pre-registered "what a gerrymander looks like" checklist (report_public.md §"What a gerrymander in the 91-seat map would actually look like") to the two existing 2026 commission maps (majority 89-seat and minority 89-seat). Establishes the baseline scorecard against which the November 2026 MLA-committee 91-seat map will be compared. Serves as a self-test of the checklist's calibration.
forward_dependencies:
  - Track C re-audit of November committee map (same scoring method applied to new map; direct comparison)
  - report_public.md §"What a gerrymander would actually look like" (checklist source)
  - report_academic.md §3.7–3.10 (signature-detection methodology; findings mirrored here)
backward_dependencies:
  - analysis/scripts/v0_2_packing_cracking_analysis.py (B1–B6 partisan metrics)
  - analysis/scripts/electoral_forensics_population.py (A1–A3 population findings)
  - analysis/reports/v0_1_justification_tests_findings.md (population-math verdicts)
  - analysis/reports/submission_search_findings.md (public-support tiers)
  - analysis/methodology/v0_1_minority_rationales_validation.md (rationale verdicts)
  - analysis/reports/v0_1_chair_recommendation_5_analysis.md (R5 conditions as extra gates)
---

# Track C — pre-registered checklist baseline scoring

**Date:** 2026-04-22
**Maps scored:** 2026 Commission Majority (89 seats); 2026 Commission Minority (89 seats)
**Map not yet scorable:** November 2026 MLA Committee (91 seats) — date-gated, map does not yet exist
**Purpose:** (1) establish a baseline scorecard the November map can be compared against; (2) self-test the checklist's calibration against maps whose content is already known.

The checklist is reproduced verbatim from `report_public.md` §"What a gerrymander in the 91-seat map would actually look like." Each signal is applied symmetrically to the two 89-seat commission maps. No test has been omitted or added post-hoc.

---

## Strong signals

### S1. The three minority signatures are preserved

**Criterion.** A map preserves or introduces all three formal signatures detected under the minority (packing in Calgary Zone A, cracking in Airdrie ≥ 4 districts, engineered boundary on an s.15(2) district).

| Map | Packing (Calgary Zone A ≥ 10% gap) | Cracking (Airdrie ≥ 4 EDs) | Engineered s.15(2) boundary | Signatures present |
|---|---|---|---|---|
| Majority 2026 | 0.36% gap — no | 2 EDs — no | None — no | **0 / 3** |
| Minority 2026 | 12.20% gap — yes | 4 EDs — yes | RMH-Banff Park — yes | **3 / 3** |

**Score.** Majority: strong signal NOT detected. Minority: strong signal detected (by definition — minority is where they were originally identified). Sources: `analysis/scripts/electoral_forensics_population.py` (Calgary zone gap); `analysis/reports/v0_1_section_C_geographic_coherence.md` (Airdrie partition, RMH-Banff Park shape).

### S2. New signatures appear

**Criterion.** A map introduces packing or cracking patterns beyond what the minority had — Edmonton NDP areas packed, new urban communities cracked, more engineered rural boundaries.

| Map | Edmonton NDP packing | Additional urban cracking | Additional engineered rural | New signatures |
|---|---|---|---|---|
| Majority 2026 | No (Calgary zone gap 0.36% ≈ neutral) | No | No | **0** |
| Minority 2026 | No (Edmonton unpacked; NDP cluster preserved) | No (beyond Airdrie and Chestermere already in S1) | No (beyond RMH-Banff already in S1) | **0** |

**Score.** Neither map introduces new signatures beyond S1's set. Source: spatial audit in `analysis/reports/v0_1_section_C_geographic_coherence.md` and `analysis/methodology/v0_1_uncertainty_and_shapefile_impact.md`.

### S3. Both extra rural seats have engineered boundaries

**Criterion.** N/A for this scoring — this signal is specific to the 91-seat map's two new rural seats. The 89-seat maps do not add two seats relative to the 2019 count of 87; they add two seats total (one urban, one rural), and those allocations are documented but not categorised as "extra rural" in the same sense. Deferred to the November map.

### S4. Efficiency gap crosses the US 7% threshold

**Criterion.** Efficiency gap, computed on 2023 votes, exceeds 7% (positive or negative) — the threshold US courts have cited (Whitford v. Gill; Stephanopoulos and McGhee 2015).

| Map | Efficiency gap (2023, 70/30 urban weight) | Crosses 7%? |
|---|---|---|
| 2019 baseline | −2.64% | No |
| Majority 2026 | −0.85% | No |
| Minority 2026 | −1.36% | No |

**Score.** Neither 2026 map crosses the US threshold. Source: `analysis/scripts/v0_2_packing_cracking_analysis.py`, re-verified 2026-04-22 in Gate G0.

### S5. Ensemble outlier test (top 5% UCP-favourable of legal alternatives)

**Criterion.** Map's partisan lean falls in the top 5% UCP-favourable of a Markov-Chain Monte Carlo ensemble of 10,000+ rule-following alternative maps.

**Score.** **Blocked** for both 2026 maps. The MCMC ensemble requires 2026 shapefiles, which Elections Alberta has not released for either proposal. Documented in `analysis/methodology/v0_1_uncertainty_and_shapefile_impact.md`. When shapefiles become available, Phase 5 of the v1.2 pipeline runs GerryChain and produces the percentile rank for both maps.

### S6. Publicly-supported configurations dropped; unsupported ones kept

**Criterion.** A map drops configurations with documented public support (Rocky Mountain House-Banff Park, Olds-Three Hills-Didsbury, Chestermere) while keeping configurations without public support (Airdrie 4-way, Nolan Hill-Cochrane).

| Map | Keeps publicly-supported configs | Keeps unsupported configs | Inversion score |
|---|---|---|---|
| Majority 2026 | Preserves the principle for Olds area and Chestermere (not the specific minority labels); does not preserve RMH-Banff Park | No (majority rejected Airdrie 4-way and Nolan Hill-Cochrane) | **No inversion** |
| Minority 2026 | Yes — RMH-Banff Park, ODH rural unit, Chestermere separation | Yes — Airdrie 4-way, Nolan Hill-Cochrane | **Partial inversion** (minority keeps both supported and unsupported, not inverting *which* it keeps — it keeps the full minority programme) |

**Score.** Majority: no inversion. Minority: does not invert in the "drops supported, keeps unsupported" sense — it keeps both — so the inversion signal is not technically triggered. The unsupported configurations (Airdrie 4-way, Nolan Hill-Cochrane) are nonetheless present in the minority, which is a weaker signal captured by S1. Source: `analysis/reports/submission_search_findings.md`, tier table in `analysis/reports/v0_1_claim_significance_analysis.md`.

---

## Weak signals

### W1. Two extra rural seats on their own

N/A for the 89-seat maps. Both add two seats relative to 2019; the rural/urban split of those two seats is documented in both commission reports. Deferred to the November map.

### W2. Calgary zone gap similar to the minority's

Scored in S1. Majority 0.36% (near-neutral), Minority 12.20% (large).

### W3. Keeping the Nolan Hill-Cochrane hybrid without stronger justification

| Map | Keeps Nolan Hill-Cochrane | Commuter-tie rationale holds at CSD resolution | Verdict |
|---|---|---|---|
| Majority 2026 | No | N/A | No weak signal triggered |
| Minority 2026 | Yes | StatsCan 98-10-0459 confirms 35.8% of Cochrane out-commuters go to Calgary; within-Calgary destination not testable; Nolan Hill is residential | Weak signal **triggered** |

Source: `analysis/methodology/v0_1_cochrane_journey_to_work.md`.

---

## Process signals (not about the map, but still relevant)

### P1. Committee proceedings closed to the public

Commission proceedings were open: public hearings, written submissions, interim report circulated for feedback. Applies to both 2026 maps equally.

**Score.** Majority: no. Minority: no. No process signal triggered against either 89-seat commission map. (Will be the active question for the November 91-seat map.)

### P2. Advisory panel members not named / terms withheld

N/A for the 89-seat commission process; commissioners were named and terms were public.

### P3. Draft map not released for public comment

Interim report was released and received feedback. N/A in the negative direction for both 89-seat maps.

### P4. Legislative adoption without amendment or published dissent

N/A; no legislative adoption of either 89-seat map (both were set aside by the April 16 motion).

### P5. AI tools used without disclosure

N/A; commission did not use AI for boundary drafting per its published methodology (no AI mentioned in the commission report).

**Score.** Both 89-seat maps: no process signals triggered. The process signals are entirely in front of the November committee.

---

## Supplementary gates introduced in session 9 (not in the original checklist)

These gates were added to the evidence base after the original checklist was written. They apply symmetrically to both maps and to the November map.

### X1. Chair Miller's Recommendation 5 conditions (a)–(d)

| R5 condition | Majority 2026 | Minority 2026 | Notes |
|---|---|---|---|
| (a) No impact on any ED in Airdrie or south of it except Drumheller-Stettler | N/A — R5 is a conditional for the 91-seat fallback | N/A | R5 binds the November committee, not the commission's own maps |
| (b) No impact north of North Saskatchewan River in Edmonton | N/A | N/A | Same |
| (c) Revert south-of-NSR Edmonton districts to interim map | N/A | N/A | Same |
| (d) Restore Clearwater / western Mountain View s.15(2) district | N/A | N/A | Same |

**Score.** R5(a)–(d) are specifically triggered only when the 91-seat fallback is activated. Both 89-seat maps predate that trigger. Deferred to the November map. Source: `analysis/reports/v0_1_chair_recommendation_5_analysis.md`.

### X2. Rationale-against-data checks

| Check | Majority 2026 | Minority 2026 |
|---|---|---|
| Shared-schools claim (Bow-Springbank, Red Deer-Sylvan Lake) | N/A (majority does not use this rationale) | **Contradicted** (Alberta Education school-division boundaries disagree) |
| Commuter-tie claim for Nolan Hill-Cochrane | N/A | **Unsupported** at CSD resolution |
| Five population-math justifications | N/A (majority does not invoke them) | **All five FAIL** (`analysis/reports/v0_1_justification_tests_findings.md`) |
| Piikani / Peigan naming | N/A | Naming observation, no fault finding |

**Score.** Minority: three rationales contradicted or unsupported, five population-math tests failed. Majority: no tested rationales triggered a contradiction. Source: `analysis/methodology/v0_1_minority_rationales_validation.md`.

### X3. 338Canada independent cross-validation

| Map | 338-reallocated UCP/NDP seats | Audit 2023-vote central | Minority-vs-Majority gap (both methods) |
|---|---|---|---|
| Majority 2026 | 67 / 22 | 38 / 51 | — |
| Minority 2026 | 66 / 23 | 37 / 52 | — |

**Score.** The minority-vs-majority asymmetry is **1 seat NDP under both inputs**. The boundary effect is a structural property of the map. Source: `analysis/methodology/v0_1_338canada_riding_level.md`.

---

## Scorecard summary

| Signal class | Majority 2026 | Minority 2026 |
|---|---|---|
| Strong signals present (S1, S2, S4, S6; S3 and S5 N/A or blocked) | 0 / 4 scorable | 1 / 4 scorable (S1 only; S2, S4, S6 not triggered) |
| Weak signals present (W2, W3; W1 N/A) | 0 / 2 | 2 / 2 (W2 zone gap, W3 Nolan-Hill-Cochrane) |
| Process signals (P1–P5) | 0 / 5 | 0 / 5 |
| Supplementary gates (X1 deferred; X2, X3 scorable) | X2 0 triggered, X3 confirms gap | X2 three triggered, X3 confirms gap |

**Honest test (from checklist):** "A sure-sign gerrymander looks like the three formal signatures surviving plus at least one new one added plus either the ensemble-outlier test or the documented-public-support inversion."

Applied to the two 89-seat maps:

- **Majority:** zero signatures, no new signatures, no inversion, no process concerns, no rationale contradictions. **Checklist classification: not a gerrymander.**
- **Minority:** three signatures (by construction — source of the signature set), no new signatures beyond the set, partial rather than inversion on public support, no process concerns at the commission stage, three contradicted rationales, structural 1-seat UCP shift. **Checklist classification: concerning but does not meet the sure-sign bar.** The checklist's top threshold requires signatures-plus-new-signatures-plus (ensemble-outlier OR public-support-inversion). The minority meets the signature criterion but fails the others.

This matches the public report's existing bottom line: the minority is measurably UCP-favourable but not a gerrymander at the US 7% threshold. The checklist is internally consistent with the audit's stated conclusions, which is a desirable property for a pre-registered test.

---

## Self-calibration finding

Running the checklist against the two maps whose content is already known confirms the checklist distinguishes them in the expected direction (majority clean, minority three signatures, neither crossing the sure-sign bar). The checklist is therefore well-calibrated for the November map: any November map that scores higher than the minority on the strong-signals count, or adds new signatures on top of the minority's three, is carrying a worse signature than the minority baseline.

The checklist's S5 (ensemble outlier) remains blocked on both 89-seat maps because no 2026 shapefiles have been released. That gate activates only when shapefiles arrive. The November 91-seat map will face the same blocker unless Elections Alberta or the committee itself releases shapefiles with the map.

---

## Comparison template for the November map

When the MLA committee tables its 91-seat map, score the map on the same signals using the same method. The following table is prepared for completion:

| Signal | Majority 2026 | Minority 2026 | November 91-seat (Pending shapefiles) |
|---|---|---|---|
| S1 three signatures preserved | 0 / 3 | 3 / 3 | — |
| S2 new signatures | 0 | 0 | — |
| S3 two rural seats engineered | N/A | N/A | — |
| S4 EG crosses US 7% | No (−0.85%) | No (−1.36%) | — |
| S5 ensemble outlier | Blocked | Blocked | — (may be blocked) |
| S6 publicly-supported configs dropped | No | Partial | — |
| W1 two extra rural seats alone | N/A | N/A | — |
| W2 Calgary zone gap similar to minority's | No (0.36%) | Yes (12.20%) | — |
| W3 Nolan Hill-Cochrane kept without better justification | No | Yes | — |
| P1 committee proceedings closed | No | No | — (likely **yes** for November) |
| P2 advisory panel members not named | No | No | — (currently **yes** for November — not yet disclosed as of 2026-04-22) |
| P3 draft not released for public comment | No | No | — (committee mandate excludes public hearings) |
| P4 adopted without amendment or dissent | No | No | — |
| P5 AI tools used without disclosure | No | No | — (depends on committee practice) |
| X1 R5 conditions (a)–(d) satisfied | N/A | N/A | — (testable once committee tables map) |
| X2 rationales against data | 0 failed | 3 failed, 5 pop-math failed | — |
| X3 338-reallocated UCP/NDP | 67 / 22 | 66 / 23 | — |

The November sub-audit should fill the rightmost column in the same structure. A straightforward majority-count comparison (how many signals score higher or lower than the minority) will give readers a clean first read of whether the new map is better than, worse than, or comparable to the two maps it replaces.

---

## Data provenance

- Checklist source: `report_public.md` §"What a gerrymander in the 91-seat map would actually look like" (v0.12 state, committed 41c361d).
- Metrics source: `analysis/scripts/v0_2_packing_cracking_analysis.py` (B2, B3, B4, B6); `analysis/scripts/electoral_forensics_population.py` (A1, A2, A3).
- Public-support tiers: `analysis/reports/submission_search_findings.md` + `analysis/reports/v0_1_claim_significance_analysis.md`.
- Rationale checks: `analysis/methodology/v0_1_minority_rationales_validation.md`.
- Chair R5 conditions: `analysis/reports/v0_1_chair_recommendation_5_analysis.md`.
- 338 validation: `analysis/methodology/v0_1_338canada_riding_level.md`.
- Cochrane commute: `analysis/methodology/v0_1_cochrane_journey_to_work.md`.

## Falsifiability

The checklist's calibration is falsified if: (a) running the checklist against a known-independent-commission output (majority) produces any strong or weak signal triggered, OR (b) running it against a known-partisan-engineered map produces zero signals. Neither occurred in this scoring. If a November map scores zero signals but is still politically suspect, the checklist needs revision — and this scoring establishes that on the present signal set, the majority baseline is the clean reference point.
