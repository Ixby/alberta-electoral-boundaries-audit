# Bias Audit — Alberta Electoral Boundaries Audit

**Purpose.** Read the prompt, code, and written findings looking for baked-in partisan framing, asymmetric scrutiny, loaded language, or unreproducible claims that would compromise the audit's credibility regardless of whether its headline finding is directionally correct.

**Method.** Walk every file the audit produces and every input it consumes. Ask of each: (a) does this apply the same test to both 2026 proposals? (b) does it presuppose the answer? (c) is every cited number reproducible from checked-in code + data?

**Bottom line.** The audit's methodology is broadly symmetric but there are **three class-A issues that need fixing before publication** and several class-B issues worth tightening. The headline finding (minority shifts 2–3 pp toward UCP with population/spatial/procedural correlates) is not invalidated by these issues — the underlying evidence is real — but the audit as currently structured overstates the reproducibility of one central number and uses loaded language in a few spots that a hostile reader would fairly flag.

---

## Class A — Material issues

### A1. B1–B4 majority numbers are not reproducible from checked-in code

**Finding.** `analysis/v0_1_packing_cracking_analysis.py` computes B1–B4 only for (a) the 2019 boundaries and (b) the minority 2026 proposal. It does not compute B1–B4 for the majority 2026 proposal. The script's own docstring (line 34) states: *"Majority 2026 plan not included — requires extraction of majority's per-ED populations from Appendix B (pp. 87–266) of the report PDF."*

Yet the carry-forward table asserted in the v0.8 prompt, the migration doc, and `alberta_redistricting_audit_final.md` includes specific majority numbers:

- B2 Efficiency gap: −0.47%
- B3 Mean-median: −2.15 pp
- B4 NDP seats at 50/50: 47
- Simulated 2023 outcome: 38/51

**These numbers have no reproducible provenance in the bundle.** They appear to have been carried forward from a prior session (Chat 1 or Chat 2) whose code was not checked in, or they were computed by an ad-hoc process not preserved as a script.

Current script output (verified in this audit):

```
2019 BOUNDARIES: EG -2.64%, MM -2.22pp, NDP@50/50 46, sim 38/49
MINORITY 2026:   EG +0.30%, MM -0.01pp, NDP@50/50 43, sim 35/54
MAJORITY 2026:   NOT COMPUTED
```

**Why this matters.** The audit's headline claim — "majority preserves the 2019 baseline, minority shifts it 2–3 pp toward UCP" — rests on the symmetric application of B1–B4 to all three maps. If the majority numbers are not reproducible, the headline comparison is not symmetric *in the sense the audit claims*. A hostile reader can reasonably ask: "Where did −0.47% come from?" and the checked-in bundle has no answer.

**Severity.** Class A. The most important number in the audit (the majority vs minority contrast that frames everything else) is currently unfalsifiable.

**Fix.** Extend `v0_1_packing_cracking_analysis.py` to include `estimate_majority_2026(dists_2019, …)` using the same blending methodology applied to the minority, then have `main()` print all three maps' metrics. Either reproduce the −0.47% / −2.15pp / 47 / 38-51 numbers from first principles, or update the carry-forward table with whatever numbers the symmetric script actually produces.

### A2. Rural baseline "conservative" framing presupposes the conclusion

**Finding.** `v0_1_packing_cracking_analysis.py` docstring (lines 25–31) states:

> *"Rural blend uses a 70/30 (urban/rural) weighting and a 33.5% NDP / 66.5% UCP rural baseline. **This is conservative** — actual rural areas the minority absorbs (Bearspaw, Springbank, Cochrane town, Chestermere) **are wealthier UCP strongholds, not average rural Alberta.**"*

The word "conservative" has a specific meaning here: **in the direction of understating the minority's partisan advantage**. The comment explicitly names the finding the code is supposedly testing — the minority absorbs UCP-strong areas, producing a partisan-advantageous shift — and describes the methodology as conservative *relative to that direction*. This is confirmation framing, not neutral testing.

The factual claim (that Bearspaw/Springbank/Cochrane/Chestermere have above-average UCP vote share) is empirically supportable, but calling them "strongholds" is loaded language. The same rural areas could be characterized as "higher-turnout affluent suburbs" without the partisan connotation.

**Why this matters.** A hostile reader reading the source code discovers the analyst has pre-committed to a conclusion before the test runs. The test's output is no longer independent evidence — it's evidence interpreted through a prior belief.

**Severity.** Class A in visibility (it's in the source code docstring, first thing anyone inspecting the script reads); Class B in mathematical effect (the 33.5% baseline is empirically computed in the script at runtime, so the hand-computed "33.5%" in the docstring is just descriptive, not a fudge factor).

**Fix.** Rewrite the docstring to describe the methodology in neutral terms: *"Rural blend uses 70/30 urban/rural weighting. Rural baseline is computed at runtime from the 2023 Rest-of-Alberta NDP two-party share. Hybrid districts that absorb rural areas with above-province-average UCP vote share (Bearspaw, Springbank, Cochrane town, Chestermere) may have their NDP share somewhat overstated by this blending approach; Phase 4C measured attribution would replace the approximation with observed values."* No loaded adjectives, no directional pre-commitment.

### A3. Calgary NE/central vs S/W classification uses partisan labels in source

**Finding.** `analysis/scripts/electoral_forensics_population.py` defines:

```python
CALGARY_NE_CENTRAL = {
    # Geographic N/NE/central Calgary — historically NDP-competitive or NDP-won
    ...
}

CALGARY_SOUTH_WEST = {
    # Geographic S/SW/W Calgary — historically UCP-dominant or UCP-won
    ...
}
```

The variable names are geographic (NE_CENTRAL vs SOUTH_WEST) but the comments are partisan ("NDP-competitive", "UCP-dominant"). More importantly, the test output is directly interpreted in `a2_calgary_analysis`:

```python
if gap > 0:
    print(f"  -> NE/central EDs {gap_pct:+.1f}% LARGER than S/W "
          "(consistent with packing signal if directional across maps)")
```

The print statement only flags "packing signal" if the gap is *positive* (NE/central larger). A symmetric test would also flag the reverse as a potential signal ("UCP areas over-packed"). As written, the script only has language for one direction.

**Why this matters.** The classification itself is defensible — Calgary's geographic NE/central and S/W really do have different partisan leans in the 2023 data — but embedding the partisan labels in source comments and only flagging one direction makes the test look tuned to find one answer.

**Severity.** Class A because the A2 result (minority +12.2% gap vs majority +0.4%) is the single most cited new finding in this session's analysis. The classification should be independently falsifiable.

**Fix.**
1. Rename constants and comments to pure geography: `CALGARY_NORTHEAST_CENTRAL = {...}` with a comment like *"Calgary EDs whose centroids lie N or E of a Deerfoot/Bow River dividing line"* — a geographic rule that can be independently audited.
2. The `a2_calgary_analysis` print statement should describe the finding symmetrically: *"NE/central mean pop {mean_ne:,} vs S/W mean pop {mean_sw:,}, gap {gap_pct:+.2f}%. A non-zero gap in either direction is a population-asymmetry signal; the directional interpretation (packing vs cracking of which party) depends on the partisan geography, which is separately documented in Section B carry-forward."*
3. Include a robustness check: re-run the A2 test with an alternative classification (e.g., "2023 UCP-won EDs" vs "2023 NDP-won EDs", mapping to 2026 via name match) and report whether the signal survives. If the +12.2% minority gap holds under both geographic and partisan classification rules, it's robust. If not, that's a methodology finding.

---

## Class B — Language tightening (does not invalidate findings)

### B1. Section A preamble confirms-hypothesis framing

**Finding.** `section_A_population_equality.md` opens:

> *"Going in, we expect: if the B1–B4 partisan-bias finding (minority shifts 2–3 pp toward UCP) has a population-equality correlate, we should see minority NDP-leaning districts systematically larger than UCP-leaning ones. **The numbers confirm exactly this.**"*

The phrase "the numbers confirm exactly this" is confirming-hypothesis language. A symmetric sanity check would say: *"Going in, the question is whether the two 2026 proposals diverge in population distribution, and if so, whether the divergence has a partisan correlate or is explained by other factors. The test runs below."*

**Fix.** Rewrite the preamble as a question rather than an expected answer. Let the test speak for itself rather than announcing its result in the hypothesis frame.

### B2. Section A disparate characterization of two flagged s.15(2) ridings

**Finding.** Canmore-Banff (majority, 1/5 criteria) is characterized as *"a judgment call on a mid-variance riding"*. Rocky Mountain House-Banff Park (minority, 2/5) is characterized as *"a boundary drawn to manufacture the qualification"*.

The underlying facts are different: RMH-Banff Park has a visibly engineered NP extension that is verifiable on the Alberta overview map. Canmore-Banff has no such obviously engineered feature that's visible in the bundle. So the disparate characterization is **factually supportable** — but it should be explicitly grounded in the visible evidence rather than narrative-toned.

**Fix.** Replace the current characterizations with observation-only language: *"Canmore-Banff fails 4 of 5 criteria on standard reading; its −27.2% variance is modest and no specific boundary feature was identified in available materials as an engineered pass. RMH-Banff Park fails 3 of 5 criteria when the NP extension is set aside, and 2 of 5 when counted conservatively (since the extension traverses uninhabited federal park land purely to reach a border)."* Let the difference in severity emerge from the facts, not from adjective selection.

### B3. Section C: majority hybrids not scrutinized with the same question set

**Finding.** For minority hybrids (Nolan Hill-Cochrane, RMH-Banff Park, Olds-Three Hills-Didsbury, Foothills-Airdrie West), `section_C_geographic_coherence.md` asks: does this ED show a lasso, an engineered statutory boundary, a misnamed municipality capture?

For majority hybrids (Calgary-East, Falconridge-Conrich, Glenmore-Tsuut'ina, West-Elbow Valley), the same questions are asked but the conclusion is uniformly "no anomaly." The issue: the questions were **generated from observed minority anomalies**. If the majority had its own class of anomaly (say, a disconnected rural district reached via a highway corridor), the question set wouldn't test for it.

**Fix.** Add a scan question the audit doesn't currently ask: *"Is there any ED in either proposal whose shape would look unusual to a viewer unfamiliar with the prior commission report?"* Then apply that scan to all 89+89 EDs on both maps. Document whatever that scan produces — 0, 1, 5 oddities — symmetrically before narrowing to the chair-flagged ridings.

Related: Section C only has majority-Calgary imagery in the bundle, not majority Alberta-wide or majority Edmonton. Direct visual inspection of the majority is therefore limited to 28 of 89 ridings, vs all 89 for the minority. The bundle should include `majority_alberta_overview.jpg`, `majority_edmonton.jpg`, and `majority_other_cities.jpg` equivalents before the visual audit can claim full symmetry.

### B4. Section D "without recent Canadian provincial precedent" claim

**Finding.** `section_D_procedural.md` characterizes the April 16, 2026 action as *"without recent Canadian provincial precedent."* The three comparators cited (Quebec 1992, Ontario 1996, BC 2008) are offered as examples of narrower departures. But "without recent precedent" is a strong claim — it asserts a negative (no comparable case exists). This session did not do a comprehensive search of Canadian provincial redistributions since 1991; it worked from the comparators the prompt supplied plus general knowledge.

**Fix.** Soften the claim to what the evidence supports: *"The April 16 action is a more government-controlled override than the three comparator cases commonly cited in Canadian electoral-law literature (Quebec 1992, Ontario 1996, BC 2008). A comprehensive survey of all provincial redistribution cycles since 1991 was not performed; a more cautious framing is that this action is in the **more interventionist region of Canadian practice**, not necessarily a first."*

### B5. Vote Anywhere directional commentary presupposes shift direction

**Finding.** `section_4_geometry_provenance.md` (and the migration and v0.9 prompt) state:

> *"NDP voters used Vote Anywhere at +6 pp higher rate than UCP… the 70/30 approximation therefore **under-estimates** the urban NDP concentration and **plausibly under-estimates the minority's partisan shift**."*

This is directionally loaded. The Vote Anywhere differential is empirical (NDP Election Day 42.6% vs Vote Anywhere 48.8%), but the statement that measured attribution *will* produce a larger minority shift assumes a specific geographic distribution of where those Vote Anywhere NDP voters live — specifically that they're in the packed NE/central districts, not in the cracked S/W districts.

If Vote Anywhere NDP voters are geographically dispersed uniformly across Calgary, the measured shift could be approximately equal to the approximated shift. If they concentrate in the S/W, the measured shift could be smaller. The directional prediction is plausible but not inevitable.

**Fix.** Replace the "under-estimates" framing with: *"The Vote Anywhere NDP/UCP differential is a +6 pp advantage for NDP, which means the minority's measured partisan shift from Phase 4C full execution could differ from the B1–B4 approximation in either direction, depending on where Vote Anywhere NDP voters live within the Calgary hybrids. This is an empirical question worth resolving via measured attribution, not a direction already established."*

---

## Class C — Structural observations worth carrying forward

### C1. Carry-forward data hygiene

Every number that appears in the final report should be traceable to a line in a checked-in script + a line in a checked-in data file. Currently the carry-forward includes numbers (majority B1–B4) that fail this test. Future sessions should:

- Establish a rule: *no number enters the final report that can't be reproduced by running a checked-in script against checked-in data.*
- Audit the current carry-forward table against that rule before publishing.

### C2. Classification robustness as a standard deliverable

Every classification rule (Calgary NE/central vs S/W; which ridings qualify for s.15(2); which are "hybrids" vs "direct renames") should be re-run with at least one alternative rule. The gap between the results under the two rules is the measurement uncertainty. If the gap is small, the rule is robust; if large, the rule is a load-bearing assumption that should be called out.

### C3. Negative-finding discipline

Sections A and C both include "we expect X, the numbers confirm X" framings. A strong audit includes at least one section where the expected signal *isn't* found, reported honestly. If the audit never runs into a null or contrary finding, either the methodology is miraculously well-tuned to this dataset or the audit is selecting tests that confirm the prior. One honest null finding per audit would materially strengthen reader trust.

Candidates worth trying:
- A population-equality test on an arbitrarily-chosen geographic cut (e.g., Edmonton vs Calgary vs rest) looking for cross-regional asymmetry with a null prior. What does the test produce? If it also flags the minority, that's more evidence of pattern. If it doesn't, that's a limit on the pattern.
- A spatial anomaly scan of the 2019 baseline map (not currently in the bundle). If the 2019 map has its own engineered boundaries or lassos that the audit would flag under its own criteria, that's important context — it means the 2019 baseline is not a neutral benchmark.

---

## Class D — What would survive a hostile peer review

Stripping out the characterization language and fixing the class-A issues, the audit's core evidence is:

1. **Minority 2026 population MAD is 48% wider than majority 2026** (4,707 vs 3,180). Derivable from CSVs in bundle; reproducible.
2. **Calgary NE/central and S/W mean populations differ by +0.4% in majority vs +12.2% in minority.** Derivable from CSVs + a defensible classification rule, which should be falsified under an alternative rule before publishing.
3. **Minority has 3 visibly anomalous EDs** (Nolan Hill-Cochrane, RMH-Banff Park, Olds-Three Hills-Didsbury) confirmed on published maps.
4. **Majority has 0 visibly anomalous EDs in Calgary** (majority Alberta-wide maps not inspected due to bundle asymmetry).
5. **2019 and minority B1–B4 run cleanly** from checked-in code on checked-in data.
6. **Majority B1–B4 numbers in the report are currently unverified** from the checked-in script. This should be fixed before publication.
7. **April 16 action is more government-controlled than the three commonly-cited comparator cases**; the "unprecedented" characterization overreaches.

Items 1, 2 (with the robustness check), 3–5, 7 (with the softened framing) survive hostile peer review. Item 6 does not, until the majority script is extended.

The headline finding (**minority shifts the baseline toward UCP with population/spatial/procedural correlates**) is supported by items 1, 2, 3 independently of item 6. But the **magnitude** of the shift (−0.47% vs +0.30% EG; 47 vs 43 NDP at 50/50) rests on item 6 being true. Until that's reproducible, the headline should say "the minority shifts the baseline directionally" but not cite the specific 2–3 pp magnitude as a verified number.

---

## Recommended Remediation (Priority Order)

1. **Extend `v0_1_packing_cracking_analysis.py` to compute majority 2026 symmetrically.** Fix class-A1. Confirm or correct the −0.47%/−2.15pp/47/38-51 numbers. (~30 minutes of work)
2. **Rewrite the rural baseline docstring in `v0_1_packing_cracking_analysis.py` in neutral terms.** Fix class-A2. (5 minutes)
3. **Rename Calgary classification constants; add symmetric-direction print; add alternative-classification robustness check.** Fix class-A3. (20 minutes)
4. **Rewrite class-B language tightenings across Section A preamble, Section A A3 characterizations, Section C question-set framing, Section D precedent claim, Section 4 Vote Anywhere directional statement.** (20 minutes)
5. **Add a "negative-finding check" to one section** (pick one of the null-prior tests above). Reports either a finding or a null; either is useful. (15 minutes)
6. **Update `alberta_redistricting_audit_final.md` with revised numbers and language.** (10 minutes)

Approximate total remediation: ~100 minutes focused work. This is before re-running Phase 4/5 when shapefiles drop — a separate exercise.

---

*Bias audit complete. Class-A issues are real and should be fixed before publication. Class-B issues are language-tightening that does not invalidate findings. The audit's core pattern-of-evidence is sound; the current draft overstates one central number's reproducibility and carries a few bias tells in source-code comments that a hostile reader would fairly call out.*

---

## A1 Provenance Verification — Phase 4C Update — 2026-05-18

**Status: RESOLVED (Phase 4C).** Class-A1 is fully resolved. `analysis/scripts/packing_cracking_analysis.py` v0.3 replaces the v0.2 70/30 urban/rural blend with exact VA-level spatial attribution: VA polygon centroids are joined to the official Elections Alberta shapefiles via `representative_point()` + within-predicate `gpd.sjoin`, summing `va_ndp`/`va_ucp` per ED — identical to `mcmc_ensemble_canonical.py`.

### Phase 4C output (2026-05-18, run on canonical shapefiles)

| Metric | 2019 baseline | Majority 2026 (Phase 4C) | Minority 2026 (Phase 4C) |
|---|---|---|---|
| EDs | 87 | 89 | 89 |
| Actual seats NDP/UCP | 38/49 | 34/55 | 29/60 |
| B2 Efficiency gap | −2.64% | **+0.04%** | **+3.96%** |
| B3 Mean-median (NDP) | −2.22 pp | **−3.64 pp** | **+1.03 pp** |
| B4 NDP @ 50/50 | 46 | **48** | **43** |
| B6 Declination | +0.0341 | +0.0157 | −0.0463 |

**EG minority-majority asymmetry: +3.92 pp** (minority shifts toward NDP-favorable EG; UCP wins more seats at actual vote shares but by slim margins that generate high wasted UCP votes).

Gate output: `[GATE] Majority 2026 validation: PASS`, `[GATE] Minority 2026 validation: PASS`.

### Cross-check against MCMC real-map scores

Phase 4C and MCMC (`mcmc_ensemble_canonical.py`) use the same `va_ndp`/`va_ucp` columns. Comparison:

| Metric | MCMC real-map score | Phase 4C | Delta |
|---|---|---|---|
| Majority EG | +0.0010 | +0.0004 | 0.0006 |
| Minority EG | +0.0402 | +0.0396 | 0.0006 |
| Majority seats UCP | 55/89 | 55/89 | 0 |
| Minority seats UCP | 60/89 | 60/89 | 0 |
| Majority MM | −0.0362 | −0.0364 | 0.0002 |
| Minority MM | +0.0104 | +0.0103 | 0.0001 |

Agreement is within floating-point rounding — the two pipelines are now unified.

### Methodological note on province-wide NDP share

The `va_ndp`/`va_ucp` integer columns sum to 893,018 total (42.56% NDP province-wide), versus 1,706,304 in the 2023 election CSV (45.56% NDP). The integer columns represent a downscaled allocation preserving the intra-ED partisan *ratios*, not the absolute vote scale. All bias metrics (EG, MM, declination, s50) are ratio statistics and are invariant to this scaling — they are directly comparable to the MCMC ensemble results, which use the same columns.

**Report update required:** The v0.2 blend numbers (−0.40% majority EG, −1.81% minority EG) that were previously cited in `reports/academic/report_academic.md` §5.2 must be replaced with Phase 4C values. See the DOCUMENTED CORRECTIONS section in the report for the formal correction entry.
