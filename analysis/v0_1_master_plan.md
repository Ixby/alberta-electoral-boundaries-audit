# Master Plan — Alberta Electoral Boundaries Audit
**Last updated:** 2026-04-23 (session 12)
**Version:** v0.19

This is the single source of truth for what is open, what is answered, and what is next.
Organized by layer: design, statistics, spatial/GIS, data, and computational resolution.
Each item carries: severity, current status, and the specific fix or answer.

---

## LAYER 1 — DESIGN RED-TEAM

### D1. Two-party collapse is undisclosed and potentially fatal
**Severity: FATAL**
**Status: OPEN — highest priority**

EG, mean-median, and declination all assume a two-party system. Alberta 2023 had ~7.4% third-party vote share. The current code computes NDP vs UCP only; third-party votes are dropped from the denominator. This is an analyst degree-of-freedom that can shift EG by multiple pp — potentially larger than the -1.42pp asymmetry itself.

The undisclosed allocation rule is the vulnerability. A critic does not need to prove the rule is wrong — they only need to show it was never stated. In a dominant-party province where NDP-adjacent parties (Greens, NDP splinters) run in urban ridings, dropping their votes disproportionately shrinks the NDP-leaning denominator in urban districts, understating NDP wasted votes and overstating the EG in NDP's favour.

**Fix required:**
1. Document the current rule explicitly: "third-party votes excluded from two-party denominator."
2. Run sensitivity: (a) exclude third-party entirely (current); (b) pro-rate to NDP/UCP by riding-level two-party share; (c) allocate all third-party to the trailing party. Report how the headline -1.42pp asymmetry moves across these three rules.
3. If direction holds under all three, this attack is closed. If it doesn't, the claim requires qualification.

**Effort:** 1 day. This is the single highest-priority open item.

---

### D2. The MC CI is sensitivity analysis mislabeled as a confidence interval
**Severity: FATAL**
**Status: PARTIALLY ANSWERED — relabeling required**

The `v0_3_monte_carlo_ci.py` simulation varies `urban_weight`, `rural_ndp_share`, and per-hybrid jitter. It does not vary boundary positions, spatial assignment, or model specification. Calling the output a "95% CI" implies frequentist coverage that doesn't exist here. It is a sensitivity envelope.

Additionally: the 89 districts are spatially autocorrelated (urban EDs cluster together). Under Moran's I, effective N is probably 20–30, not 89. All CIs computed assuming independence are too narrow by a factor of 2–3.

**Already documented** in `v0_1_design_critique.md` §1.1 (residual concern). **Not fixed.**

**Fix required:**
1. Relabel all CI outputs as "sensitivity interval" in both reports and scripts.
2. Add a footnote: "This interval reflects parameter uncertainty in the vote-share model. It does not account for boundary position uncertainty, spatial assignment error, or spatial autocorrelation in district-level vote shares. Under spatial autocorrelation the effective N is approximately 20–30, which would widen these bounds by a factor of 1.5–2."
3. Keep the 90.5% directional claim but reframe: "Under the full parameter sensitivity range, the direction is consistent in 90.5% of draws."

**Effort:** Half day (text only, no new code required).

---

### D3. Cross-election direction flip is near-falsification, not a robustness check
**Severity: SERIOUS**
**Status: DISCLOSED BUT NOT EXPLAINED**

Under 2019 vote inputs the minority-majority asymmetry direction reverses. The audit reports this as disclosure. A hostile reviewer will read it as evidence against the claim: structural gerrymandering should be stable across elections. If it flips, the finding is vote-distribution-sensitive, not structural.

**Existing answer** (`v0_1_design_critique.md` §2.5): cross-election robustness was added as a fix. But the flip itself is not mechanically explained.

**Fix required:**
1. Explain the flip mechanically: in 2023 the minority absorbed Springbank/Bearspaw/Cochrane (wealthy suburbs, UCP-leaning). In 2019 those areas had different partisan margins (UCP won more convincingly post-2015 NDP majority). The urban-weight blending makes the asymmetry sensitive to how suburban these absorbed areas were in the specific election year.
2. Add one paragraph to §3.3 of `report_academic.md` that makes this argument explicit.
3. Frame the flip as expected rather than unexplained: the finding is sensitive to election-year suburban alignment, which is a documented property, not an anomaly.

**Effort:** Half day (writing only).

---

### D4. Asymmetry framing has no null hypothesis
**Severity: SERIOUS**
**Status: PARTIALLY ANSWERED — ensemble still missing**

The audit measures minority EG minus majority EG. The implicit null is that both maps should produce the same EG. There is no theoretical basis for this null. Two honest commissions with different geographic priorities will produce different EGs. Without an ensemble of neutral Alberta maps, -1.42pp is a difference, not evidence of distortion.

**Existing answer** (`v0_1_design_critique.md` §1.2): "Not possible without 2026 shapefiles. GerryChain is installed. Blocked on shapefile release." This is the correct answer. The limitation is disclosed.

**Residual exposure:** The reports do not state this limitation as prominently as they should. The headline claim implies the comparison is meaningful without qualifying that a proper null requires an ensemble.

**Fix required:**
1. Add a one-sentence caveat to §3 of `report_academic.md`: "Without a simulated ensemble of neutral Alberta maps, the minority-majority difference is not benchmarked against the range of outcomes achievable under good-faith redistricting. That benchmark requires official 2026 shapefiles (Track A)."
2. No code change needed.

**Effort:** 20 minutes (text only).

---

### D5. "Six of seven cleaner alternatives" is post-hoc unless pre-specified
**Severity: SERIOUS**
**Status: OPEN**

The pre-registration covers B1–B6 metric methodology. It does not pre-specify the criteria for identifying "cleaner alternatives" to seven specific minority redraws. Without a mechanical pre-specified rule applied blindly, this is the analyst's judgment presented as a structural finding.

**Fix required:**
1. In the academic report, downgrade this finding from "structural" to "qualitative." Use language: "In six of seven cases, alternative boundary configurations exist that would satisfy the same stated rationale while producing smaller EG shifts. These alternatives are not uniquely identifiable by a mechanical rule; their identification reflects the auditors' judgment applied to publicly available commission map data."
2. Disclose the OSF registration does not pre-cover this finding.

**Effort:** 1 hour (text reframing only).

---

### D6. Legal framing mismatch — Saskatchewan Reference vs EG threshold
**Severity: MANAGEABLE**
**Status: DOCUMENTED**

*Saskatchewan Reference* [1991] requires "effective representation," not partisan symmetry. An EG of -1.42pp with a CI crossing zero does not establish a violation of effective representation. The audit occupies an uncomfortable middle ground: too strong in implication for a purely descriptive exercise, too weak in evidence for a legal claim.

Additionally: dominant-party provinces structurally produce asymmetric EGs under any neutral map. Alberta's geographic polarization (urban NDP, rural UCP) means even a perfectly neutral map would produce a pro-UCP EG. The audit does not estimate this structural baseline.

**Existing answer:** The audit explicitly disclaims intent to prove gerrymandering intent and frames findings as "patterns consistent with partisan influence, not proof of it." This is the correct posture.

**Fix required:**
1. Add a sentence to §1 of both reports: "Alberta's geographic polarization structurally produces pro-UCP efficiency gaps under any neutral map. The relevant question is whether the minority map's gap exceeds what neutral redistricting would produce — a test that requires a map ensemble and is gated on official shapefile release."
2. Ensure the academic report's legal section (§5, Saskatchewan Reference) makes this explicit.

**Effort:** 30 minutes.

---

## LAYER 2 — STATISTICAL RED-TEAM

### S1. B4 uniform swing assumption is wrong for Alberta
**Severity: SIGNIFICANT**
**Status: UNDOCUMENTED**

B4 (NDP seats at 50/50) uses a uniform swing applied to all 89 districts equally. In Alberta, the seat-vote curve is highly non-linear: urban NDP seats swing less (already marginal), rural UCP margins are enormous. A uniform +7.4pp swing to reach 50/50 would flip several urban marginals while barely touching 40 rural seats with 20pp+ UCP margins. The uniform swing model overstates NDP's seat gain at 50/50.

**Fix required:**
1. Add a footnote to the B4 row in every comparison table: "B4 uses a uniform swing model. Alberta's non-linear seat-vote curve means the true NDP seat count at 50/50 is likely lower than reported here. This metric is presented for comparability across maps, not as a predictive model."
2. Optionally: run a non-uniform swing using 338Canada district-level elasticities (already integrated in `v0_1_338canada_integration.md`).

**Effort:** Half day for the non-uniform version; 20 minutes for the footnote-only fix.

---

### S2. Multiple comparisons not disclosed
**Severity: SIGNIFICANT**
**Status: UNDOCUMENTED**

Four metrics (B2, B3, B4, B6) are computed and three maps compared = 12 comparisons. B6 (declination) in Phase 4C disagrees directionally with B2 (EG): majority declination = +0.0167 (pro-NDP) vs minority = -0.0061 (pro-UCP) — the metrics agree in direction. But in v0.2, B2 shows -1.42pp asymmetry while B6 shows a smaller directional signal. The audit treats "directional consistency across metrics" as strengthening evidence without acknowledging the multiple-comparison structure.

**Fix required:**
1. Add a note to the comparison tables: "Four metrics are reported. Under Bonferroni correction for four tests at alpha=0.05, the individual threshold is alpha=0.0125. None of our metrics reaches this threshold individually. The finding rests on directional consistency across metrics, not statistical significance of any single metric."
2. This is honest disclosure, not retraction.

**Effort:** 30 minutes.

---

### S3. "90% directional confidence" misrepresents what the MC draws show
**Severity: SIGNIFICANT**
**Status: MISLEADING LABEL**

"90.5% of MC draws show the asymmetry in the same direction" is not a frequentist confidence interval, not a Bayesian posterior, and not a p-value. It is a statement about parameter sensitivity: "if urban_weight is uniform between 0.55 and 0.85, the direction is stable." The 9.5% of draws where direction flips are not evidence that direction is wrong 9.5% of the time — they are evidence that extreme parameter values produce direction flips.

**Fix required:**
Rewrite all instances of "90% directional confidence" to: "Under the full parameter sensitivity range, direction is consistent in 90.5% of draws. This is a sensitivity result, not a frequentist confidence level."

**Effort:** 30 minutes.

---

### S4. Small-N regime not disclosed for B2/B3
**Severity: MINOR**
**Status: UNDOCUMENTED**

The standard error of the efficiency gap in an 89-district system is approximately 1–2pp (derived from the variance in wasted-vote fractions across districts). The -1.42pp asymmetry is within this noise range for a single-election estimate. This does not make the finding wrong — direction consistency across metrics and elections matters — but it means the point estimate should not be cited without its noise floor.

**Fix required:**
Add to the MC CI section: "The standard error of a single-election EG estimate in an 89-district system is approximately 1–2pp, placing the -1.42pp asymmetry near the lower bound of reliable detection. This is why directional consistency across multiple metrics and the full sensitivity range is the primary evidence, not the point estimate."

**Effort:** 20 minutes.

---

## LAYER 3 — SPATIAL/GIS RED-TEAM

### G1. Centroid-in-polygon fails for large rural VAs
**Severity: SIGNIFICANT**
**Status: DOCUMENTED AS LIMITATION**

Rural VA polygons can cover 500–5,000 km². The centroid may be kilometers from the actual polling cluster. This particularly affects hybrid EDs where the rural absorption zone has large VAs — exactly the EDs where the blending model matters most.

**Current mitigation:** Phase 4C Method 0 (direct-rename crosswalk override) captures most rural VAs before spatial assignment fires. Only 1,765 majority VAs are assigned by centroid-in-polygon; the rest by crosswalk or candidate.

**Fix required:** Document this in the Phase 4C methodology note. No code change until official shapefiles available.

---

### G2. 81/95 overlapping polygon pairs corrupt a subset of spatial assignments
**Severity: SIGNIFICANT**
**Status: DOCUMENTED, IMPACT UNQUANTIFIED**

Largest overlaps: Calgary-Airdrie × Calgary-Nolan Hill-Cochrane (264 km², minority). VAs in overlap zones are assigned to whichever polygon comes first in the GDF index — effectively arbitrary for those VAs.

**Unquantified exposure:** How many VAs fall in overlap zones? How many votes do they carry? Which EDs are most affected?

**Fix required:**
1. Run a diagnostic: for each overlapping pair, count VAs whose centroids fall in the overlap area and sum their vote totals.
2. Report the maximum possible swing in EG if all overlap-zone VAs were reassigned to the other ED.
3. This converts "unknown error" to "bounded error."

**Effort:** Half day.

---

### G3. Advance-vote splat design needs validation
**Severity: SIGNIFICANT**
**Status: PLANNED, NOT YET BUILT**

`polls_2023_unified.csv` has per-poll ballot_type (Election Day/Advance/Special/Mobile) with `voting_areas` (comma-separated VA numbers). Plan: distribute each poll's non-Election-Day votes to its VAs proportionally by that poll's Election-Day share.

**Assumption risk:** proportional-by-Election-Day-share assumes advance voters have the same partisan distribution as Election-Day voters within a poll's VA set. This assumption breaks when a poll serves VAs with very different partisan lean. However, NDP's 6pp higher advance-ballot rate is a province-wide average; within a single poll (small geographic area), partisan composition is relatively homogeneous.

**Fix required:**
1. Build the splat (see Computational Layer, C1).
2. Validate: compare pre-splat vs post-splat EG. If EG shifts by more than 0.5pp, investigate which polls drove the shift.
3. Report the splat as a model: "advance votes apportioned to VAs by Election-Day partisan share within each poll. Assumes uniform advance-ballot rate within poll catchment areas."

**Effort:** 1–2 days (build + validate).

---

### G4. Calgary-Airdrie 264 km² minority overlap needs investigation
**Severity: SIGNIFICANT**
**Status: FLAGGED, NOT INVESTIGATED**

The 264 km² Calgary-Airdrie × Calgary-Nolan Hill-Cochrane overlap is the largest single overlap in either canonical file. Calgary-Airdrie's pixel-extracted minority boundary over-extends into at least three adjacent EDs. This is a pixel-extraction error, not a genuine boundary ambiguity.

**Fix required:**
1. Visually inspect the Calgary-Airdrie minority polygon against the commission's minority Calgary map.
2. If the over-extension is clearly a pixel-extraction artifact, manually clip the boundary and save as a corrected Tier A polygon.
3. Re-run Phase 4C after the clip.

**Effort:** 2 hours.

---

### G5. Direct-rename override fires on string match, not territory identity
**Severity: MINOR**
**Status: KNOWN**

Method 0 fires when `2019_parent_name == 2026_ED_name`. An ED that was renamed but has identical territory would miss the override (fine). An ED with the same name but different territory would incorrectly get the override (bad). Edmonton-Beaumont fix (session 12) demonstrates this risk was real.

**Fix required:**
Add a validation check: for every direct-override ED, verify the 2026 canonical polygon area is within 10% of the 2019 parent polygon area. Flag mismatches for manual review.

**Effort:** 2 hours.

---

## LAYER 4 — DATA DEFICIENCY INVENTORY

| Gap | Impact | Fix |
|---|---|---|
| Election-Day votes only (47.5% missing) | EG direction flip Phase4C vs v0.2; NDP underestimated 1.6pp | Advance-vote splat (C1) |
| No official 2026 shapefiles | 81/95 overlaps; 4 C-null EDs; Edmonton-Beaumont partial | Track A (shapefile release) |
| Edmonton-Beaumont 68% unresolved | ED vote total understated | Parametric split model (C3) |
| 206 nearest-ED fallback assignments | Low-confidence rural assignment | Overlap-zone fuzz (C2) |
| Vote Anywhere polls non-residence-based | Unknown spatial attribution error | Identify + exclude (C5) |
| Two-party collapse undisclosed | Potentially fatal; see D1 | Sensitivity run (D1) |
| Sensitivity table stale (CRIT-01) | Report numbers don't match script output | Rerun + update (existing finding) |

---

## LAYER 5 — COMPUTATIONAL RESOLUTION (PRIORITY ORDER)

### C1. Advance-vote splat — closes the 47.5% gap [HIGHEST PRIORITY]
**Input:** `polls_2023_unified.csv` (ballot_type, voting_areas, ndp_votes, ucp_votes)
**Method:** For each non-Election-Day poll, distribute votes to its VAs proportionally by Election-Day share.
**Output:** Updated VA substrate with full 2023 vote totals (target: 1,706,304 two-party).
**Consequence:** Makes Phase 4C comparable to v0.2; likely resolves EG sign flip; probably raises NDP province-wide share from 42.60% to ~44.17%.
**Effort:** 1–2 days.

### C2. Overlap-zone fuzzing — bounds boundary uncertainty
**Input:** Canonical shapefiles + VA polygons.
**Method:** For each overlapping pair, identify VAs in the overlap area. Run Phase 4C N=500 times with those VAs randomly assigned to either competing ED. Report EG distribution.
**Output:** EG ± Xpp from boundary uncertainty.
**Effort:** Half day.

### C3. Edmonton-Beaumont parametric split
**Input:** Edmonton-South 2019 VA vote totals + commission population target (55,802).
**Method:** Compute fraction of Edmonton-South 2019 that should go to Edmonton-Beaumont 2026 = (55,802 − 17,000_Beaumont) / Edmonton-South_2019_pop. Run Phase 4C with that fraction of Edmonton-South VAs reassigned to Edmonton-Beaumont. Sweep ±10pp.
**Output:** Edmonton-Beaumont vote total range; sensitivity of EG to this parameter.
**Effort:** Half day.

### C4. Third-party vote sensitivity (D1 fix)
**Input:** `polls_2023_unified.csv` — full vote totals including third-party.
**Method:** Run v0.2 under three allocation rules: (a) drop, (b) pro-rate, (c) give to trailing party.
**Output:** Headline asymmetry under all three rules.
**Effort:** 1 day.

### C5. Vote Anywhere identification and exclusion
**Input:** `polls_2023_unified.csv` — poll_name column.
**Method:** Filter for Vote Anywhere polls, extract their vote totals, exclude from VA substrate.
**Output:** Clean substrate; quantified Vote Anywhere vote total (expected: small fraction of Election-Day votes).
**Effort:** 1 hour.

### C6. Sensitivity table re-run (existing CRIT-01)
**Input:** Current `v0_2_packing_cracking_analysis.py` at w=0.60, 0.70, 0.80, 0.85.
**Method:** Rerun, compare to table in `report_academic.md` §3.4.
**Output:** Updated table with correct values; text correction to "0.51 to 1.52 pp" range.
**Effort:** 30 minutes.

### C7. Calgary-Airdrie overlap clip
**Input:** Minority canonical shapefile + commission minority Calgary map.
**Method:** Visually verify over-extension; manually clip to correct boundary; save as Tier A.
**Output:** Reduced minority overlap count; more defensible Calgary spatial assignments.
**Effort:** 2 hours.

---

## LAYER 6 — WHAT IS ALREADY ANSWERED

These attacks were raised and closed in sessions 1–11. They should not be re-opened unless new evidence emerges.

| Attack | Answer | Location |
|---|---|---|
| EG is the wrong metric (chooses its result) | All four metrics (B2, B3, B4, B6) agree in direction | `v0_1_design_critique.md` §1.3 |
| 70/30 urban weight is arbitrary | w=0.85 derived from commission population targets; validated against 2023 turnout (0.3pp differential) | `v0_1_urban_weight_defense.md` |
| 338Canada cross-check | 1-seat structural asymmetry state-dependent; retracted as absolute claim | `v0_1_338canada_historical.md` |
| Chen-Rodden framing doesn't transfer | UCP is the packed party in Alberta (opposite to NDP urban packing in US) | `v0_1_chen_rodden_alberta_validation.md` |
| Canadian base rate | Median Canadian inter-map asymmetry = 0; Alberta finding is non-trivial | `v0_1_canadian_base_rate_computed.md` |
| No public support claim | Submission search partially refuted it (14 recovered submissions supporting contested configs) | `analysis/submission_search_findings.md` |
| Five minority population justifications | All five fail: A1 census deviation, A2 zone gap, A3 density, §15(2) criteria, MAD | `v0_1_section_A_population_equality.md` |
| Intent vs effect distinction | Explicitly disclaimed throughout | `report_academic.md` §1 |
| Sign convention ambiguity | Resolved; both conventions produce same ordinal ranking | `v0_1_sign_convention_resolution.md` |
| Sensitivity table stale (CRIT-01) | Numbers confirmed stale by session 12; fix in C6 | `v0_1_red_team_assertions.md` CRIT-01 |
| Edmonton-Highlands-Norwood 43 VAs stolen | Direct-rename override restores correct assignment | Session 11 |
| Phase 4C 89/89 resolution | Achieved in session 12 | `analysis/phase_4c_gerrymander_comparison.md` |

---

## WORK QUEUE — PRIORITY ORDER

| # | Task | Layer | Severity | Effort | Blocks |
|---|---|---|---|---|---|
| 1 | Third-party sensitivity run | D1, C4 | **Fatal** | 1 day | Headline claim defensibility |
| 2 | Advance-vote splat (Phase 4C full count) | C1 | **Fatal** | 1–2 days | Phase 4C vs v0.2 comparability |
| 3 | Sensitivity interval relabeling (not "CI") | D2, S3 | **Fatal** | Half day | Reports |
| 4 | Sensitivity table re-run + report update | C6 | Critical | 30 min | Report accuracy |
| 5 | Overlap-zone impact quantification | G2, C2 | Significant | Half day | Spatial confidence |
| 6 | B4 uniform swing footnote | S1 | Significant | 20 min | Reports |
| 7 | Multiple comparisons disclosure | S2 | Significant | 30 min | Reports |
| 8 | Cross-election flip mechanical explanation | D3 | Serious | Half day | Reports |
| 9 | Asymmetry null hypothesis caveat | D4 | Serious | 20 min | Reports |
| 10 | "Six of seven" downgrade to qualitative | D5 | Serious | 1 hour | Reports |
| 11 | Vote Anywhere exclusion | C5 | Significant | 1 hour | Substrate integrity |
| 12 | Calgary-Airdrie overlap clip | G4, C7 | Significant | 2 hours | Minority spatial quality |
| 13 | Edmonton-Beaumont parametric split | C3 | Significant | Half day | ED completeness |
| 14 | Direct-rename area validation | G5 | Minor | 2 hours | Crosswalk integrity |
| 15 | Small-N noise floor disclosure | S4 | Minor | 20 min | Reports |

---

## BLOCKERS (REQUIRE EXTERNAL INPUT)

| Blocker | What it unlocks | Timeline |
|---|---|---|
| Official 2026 shapefiles (Elections Alberta) | GerryChain ensemble; true spatial Phase 4C; eliminate all derived-boundary uncertainty | Unknown; requested (Track A) |
| OSF DOI from pre-registration | Add to §3 footnote of `report_academic.md` | User has DOI from session 11 — confirm and insert |
| November 2026 committee date | Re-audit on 91-seat map | November 2, 2026 |
| 338Canada refresh | Updated polling cross-validation | ~June 2026 |

---

## STRUCTURAL FINDINGS STATUS (NOT BLOCKED BY SHAPEFILES)

These findings are independent of vote-based metrics and survive all three stress-test layers.

| Finding | Status | Section |
|---|---|---|
| A1: Population deviation — minority has 3 EDs outside ±25% | Confirmed | §A |
| A2: Calgary zone gap — minority 4-ED gap (14.1K extra/seat) | Confirmed under 3 classification rules | §A |
| A3: MAD — minority higher than majority | Confirmed | §A |
| C: Visual spatial patterns — 6 configurations flagged | Confirmed; shape refinement at v4 | §C |
| D: Procedural — "no public support" claim partially refuted | Confirmed (14 of 1,252 submissions) | §D |
| D: Five population justifications fail data test | Confirmed | §A, §D |

Structural findings are the strongest part of the audit. They should be the primary claim in public-facing outputs. Vote-based findings are supporting evidence, not headline claims.
