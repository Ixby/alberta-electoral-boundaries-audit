# Science red-team — Reproducibility (S3), Falsifiability (S4), Confounder control (S5), Researcher degrees of freedom (S8)

**Directive anchor:** `analysis/v0_1_science_red_team_framework.md`
**Companion files:**
- `analysis/methodology/v0_1_science_red_team_design_and_stats.md` (S1, S2, S9) — sibling
- `analysis/methodology/v0_1_science_red_team_data_priorart_peerreview.md` (S6, S7, S10) — sibling
- `analysis/v0_1_legal_red_team_framework.md` (D4 conceptual reproducibility overlaps)

**Posture.** This file is written in the voice of a methods-paper reviewer for *Election Law Journal*, *Statistics and Public Policy*, or *PNAS Nexus*. It asks: do the audit's central findings survive when a competent reviewer swaps a metric formulation, a seed, a weighting rule, or an election; are the null hypotheses and falsification conditions cleanly stated for every finding; have both the Chen-Rodden geography confounder and the 2023-electorate confounder been fully characterised; and are the researcher degrees of freedom (hybrid set, focus cities, thresholds, n=7 base rate) pre-committed or post-hoc? Where the audit survives, the audit survives; where it does not, this file says so.

**Scope note.** Computational reproducibility (does the code run, do the numbers match) is audited in parallel by the legal D4 sibling; this file does not duplicate that. What this file adds is *conceptual* reproducibility (does the finding survive metric / seed / weighting swaps) and falsifiability framing.

---

## Status update — 2026-04-23 (post-T0/T1/T2 remediation)

Authoritative current-state view of the findings in this file against the remediation commits that landed 2026-04-23 (d25e659 T0, a62eb53 T1, de7c48e T2, afb3a4a + 3b7dbfb session-12 data pipeline).

| Finding | Status | Fix location |
|---|---|---|
| S3-01 (HIGH) MCMC seed hardcoded in `v0_1_mcmc_ensemble.py` | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S3-02 (HIGH) MCMC ESS ≈148–160; p100 rests on ~150 effective draws | ADDRESSED | a62eb53 §5.4 ESS-150 tail downgrade paragraph: raw p100/p1.6 bounded to p95.35/p2.5 at chain effective precision; minority seats-at-50/50 retracted to p89.72. Directly implements S3-02's recommendation. |
| S3-03 (MED) Urban-weight sensitivity range omits 50/50 and population-weighted alternatives | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S3-04 (HIGH) Full-coverage MCMC rescore downgrades minority p100 → p95.35 / p89.72; §3.11 stale | ADDRESSED | afb3a4a + 3b7dbfb MCMC rescore reads canonical shapefiles (`data/v0_1_canonical_{majority,minority}_2026_eds.gpkg`); a62eb53 ESS-150 downgrade aligns reported percentiles with effective precision. The falsifiability hook §3.11 set for itself is now resolved in-paper. |
| S3-05 (HIGH) Declination sign-convention label vs Warrington | ADDRESSED | a62eb53 §4.3 universal sign-convention glossary (negative = UCP advantage, positive = NDP advantage) applies across all metrics including declination. |
| S3-06 (MED) Compactness formulation swap (Convex-Hull, Schwartzberg) | PARTIAL | a62eb53 §E.7 adds Tier-dependent ± bands + ordinal convention (High/Moderate/Low-flagged/Very-low PP+Reock). Addresses band/uncertainty reporting; full alternative-formulation swap (Convex-Hull, Schwartzberg) still pending. |
| S3-07 (LOW) VA centroid-in-polygon ±0.5% rounding | ADDRESSED | d25e659 §4.1.4 DPG disclaimer formalizes perimeter-mode (±500m) vs area-mode (Tier-dependent, up to >100% on Tier-C) error disclosure; a62eb53 §5.2.7 Core-vs-Margin VA partition quantifies ~8–12% of two-party votes in Margin VAs with max ±1.5pp swing at risk. |
| S3-08 (HIGH) 2015-vote sign-convention stacking (`v0_1_2015_cross_election_analysis.md` vs paper) | ADDRESSED | a62eb53 §4.3 universal sign-convention glossary + d25e659 correction of 2019 EG sign (afb3a4a + 3b7dbfb confirm 2019 EG now matches paper's documented −2.64%) close the cross-document convention conflict. |
| S4-01 (HIGH) Minority asymmetry falsification blocked on 2026 shapefile | STRUCTURAL LIMIT | d25e659 §4.1.4 adds 48-hour sunset clause committing to recompute against official Elections Alberta 2026 shapefiles when released; until then the underlying shapefile unavailability is a structural limit, but the DPG disclaimer + sunset clause is the honest remediation. |
| S4-02 (MED) Calgary Zone A packing null (G4 robustness) | NOT ADDRESSED | Not in T0/T1/T2 scope; file notes null is already rejected on existing G4 evidence. |
| S4-03 (MED) Airdrie 4-way cracking null | ADDRESSED | a62eb53 `analysis/reports/v0_1_airdrie_overlap_report.md` header reframes 530 km² overlap as DPG transcription artifact, not commission cartography — sharpens the null engagement for the Airdrie finding. |
| S4-04 (HIGH) RMH-Banff Park E2 reformulation | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual — the reformulation disclosure work is still pending. |
| S4-05 (LOW) MCMC p100 falsification has fired | ADDRESSED | a62eb53 §5.4 ESS downgrade paragraph explicitly reports fired falsification: p100/p1.6 → p95.35/p2.5; minority seats-at-50/50 retracted to p89.72. |
| S4-06 (HIGH) OCR 7% residual on public-support refutation | PARTIAL | d25e659 §5.9.4 softens Chair-claim language to "materially overstates the absence of public support" — narrowing the claim to one the 93% coverage can support. Full OCR backfill still residual. |
| S4-07 (HIGH) Six-dimensions chance-agreement p-value uncomputed | ADDRESSED | de7c48e §6 Discussion adds paragraph explicitly naming FWER concern, explaining why Bonferroni/BH is the wrong response for consistency-of-correlated-dimensions frame, with Katz-King-Rosenblatt (2020) + Altman-McDonald (2011) authority. Directly engages the independence / effective-dimensions concern. |
| S5-01 (MED) Chen-Rodden geography-vs-drawing decomposition | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual (requires paired GerryChain ensemble on post-shapefile substrate). |
| S5-02 (HIGH) §7 synthesis table missing ", under 2023 votes" qualifier | PARTIAL | d25e659 Abstract + §5.2.7 two-measurement framing (blended crosswalk −1.42pp vs high-resolution spatial +4.15pp) reframes magnitude as systematic spatial-resolution sensitivity, which partly addresses the framing-finding mismatch at the measurement level; explicit ", under 2023 votes" propagation through headline tables still residual. |
| S5-03 (MED) Turnout confound (2019 67% vs 2023 59%) | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S5-04 (MED) 2024-TBF vs 2021-census basis inline reminder | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual (file notes fix is one sentence at §2.1). |
| S5-05 (HIGH) Hybrid-weight 50/50 and population-weighted alternatives | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S8-01 (LOW) 21 hybrid set ex ante | NOT APPLICABLE | Not a defect per the file's own assessment. |
| S8-02 (MED) Focus regions — full 89-ED differ test not run | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S8-03 (MED) Intra-session pre-registration weakness | NOT ADDRESSED | Not in T0/T1/T2 scope; OSF pre-registration still queued. |
| S8-04 (HIGH) E2 reformulation as post-hoc rescue | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S8-05 (MED) n=7 Canadian base rate shallow | NOT ADDRESSED | Not in T0/T1/T2 scope. Residual. |
| S8-06 (MED) 338Canada 77-snapshot window | NOT APPLICABLE | File notes this is audit-strengthening, not a defect. |
| Implicit finding — two-measurement framing (−1.42pp vs +4.15pp contradiction risk) | ADDRESSED | d25e659 Abstract + §5.2.7 explicitly reframe as systematic spatial-resolution sensitivity, not contradiction. |
| Implicit finding — Gill v. Whitford / 7% threshold | ADDRESSED | d25e659 corrects Gill v. Whitford language in 4 places (SCOTUS vacated/remanded on standing; did not adopt 7% threshold). |
| Implicit finding — Rizzo citation | ADDRESSED | d25e659 corrects Rizzo universally to *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 S.C.R. 27. |

Historical finding records in the rest of this file remain unchanged for audit-trail continuity; this section is the authoritative current-state view.

---

## Summary table — finding-level severity by dimension

| ID | Dimension | Severity | Finding (one-line) |
|---|---|---|---|
| S3-01 | Reproducibility | HIGH | MCMC ensemble seed is hardcoded (seed=42 in `v0_1_mcmc_ensemble.py:439`); CLI takes only `n_steps`. A reviewer who wants to stress-test seed invariance must edit source. |
| S3-02 | Reproducibility | HIGH | 100k-sample convergence diagnostics show **effective sample size ≈ 148–160** across all four metrics (autocorrelation τ ≈ 624–674). p100 and p1.7 tail claims rest on ~150 effectively-independent draws, not 100,000. |
| S3-03 | Reproducibility | MED | Hybrid urban-weight sensitivity range (0.55–0.85 Monte Carlo; 0.60–0.80 point) **does not cover a straight 50/50 or a population-weighted alternative**. Canonical methodologist would ask for one. |
| S3-04 | Reproducibility | HIGH | Full-coverage MCMC rescore (`v0_1_mcmc_ensemble_percentiles_full.csv`) **shifts the minority 2026 map from p100 to p95.35 on mean-median and puts seats-at-50/50 at p89.72 (inside the ensemble)** — a downgrade the paper's §3.11 text has not absorbed. |
| S3-05 | Reproducibility | HIGH | Stephanopoulos-Warrington declination swap: the audit implements declination but reports a positive-for-NDP / negative-for-UCP convention that is internally consistent yet cites Warrington (2018) as formula authority, whose sign convention is opposite on winning-district treatment. The ordinal ranking survives; the sign label does not. |
| S3-06 | Reproducibility | MED | Compactness is computed only under Polsby-Popper and Reock. Convex-Hull and Schwartzberg are named in the literature review but not reported. Calgary Zone A packing is *not* a compactness claim so swap doesn't affect it; the §6.7 "mean Polsby-Popper" differences are directionally stable but magnitude-sensitive. |
| S3-07 | Reproducibility | LOW | VA centroid-in-polygon attribution: paper claims ±0.5% rounding error on border VAs. Consistent with MCMC §3.11 note; no swap-test executed, but order of magnitude is defensible. |
| S3-08 | Reproducibility | HIGH | 2015-vote rerun is executed (`v0_1_2015_cross_election.py`), but the derived value (+0.03 pp) is reported under a sign convention the sibling doc `v0_1_sign_convention_resolution.md` resolves *differently* from `v0_1_2015_cross_election_analysis.md`. The paper's headline ("2015 gives +0.03 pp") is correct in magnitude; the direction interpretation is doubly-flipped. |
| S4-01 | Falsifiability | HIGH | "Minority more UCP-favourable than majority by 0.51–1.52 pp" — the paper's §3.5 states a falsification condition (Phase 4C measured attribution with opposite sign at central weight), but the condition **cannot be executed without the 2026 shapefile**, making this falsifiability hook not currently testable. |
| S4-02 | Falsifiability | MED | "Calgary Zone A packing: 12.2% gap vs 0.4%" — null ("gap is a property of classification rule, not the minority's drawing") is engaged via G4 robustness (2023-winner-based rule yields 7.71% — still >10×  majority); residual: no null statistic is reported, only the rule comparison. |
| S4-03 | Falsifiability | MED | "Airdrie 4-way is a cracking pattern" — null is "split is forced by population arithmetic." The counter-test script (`v0_1_majority_symmetry_counter_test.py`) engages this by setting the 3-quota (205,983) force-threshold; Airdrie (84k) fits under one or two EDs at ±25%. Null is rejected on population-arithmetic grounds. Defensible. |
| S4-04 | Falsifiability | HIGH | "Engineered boundary at RMH-Banff Park" — §3.9 **reformulates E2 mid-audit** from "without extension the ED would not qualify" (fails) to "alternatives existed and were not taken" (passes). The reformulation is disclosed and audit-trail-documented, but a reviewer will read this as post-hoc criterion-softening. Null framing is correspondingly softened. |
| S4-05 | Falsifiability | LOW | MCMC p100 flags against neutral ensemble — null is "minority inside ReCom-reachable distribution on that metric." Clearly rejected for mean-median and seats-at-50/50 on the 10k run. DOWNGRADED to p95.35 / p89.72 on full-coverage rescore (see S3-04). |
| S4-06 | Falsifiability | HIGH | "Three of five 'no public support' characterisations materially fail" — null is "zero genuine supporting submissions for all five." OCR/regex coverage is 93%; the remaining 7% cannot disconfirm. The verdict is defensible *conditional on the found counter-examples*; a disciplined reviewer will ask for the 88 unscanned submissions. |
| S4-07 | Falsifiability | HIGH | "Six dimensions directionally consistent" — null is "chance directional agreement across six binary signs." **Paper does not compute the under-chance p-value** (6 binary = 1/64 two-sided, 1/32 one-sided). Nor does it address the correlation between the six dimensions (e.g., MAD and Calgary zone gap are not independent). Missing computation plus missing independence justification is HIGH. |
| S5-01 | Confounders | MED | Chen-Rodden natural-packing confounder engagement is genuine (§3.6 + `v0_1_chen_rodden_alberta_validation.md`) — but the paper's statement that both 2026 maps sit inside the neutral range [−4.4%, −0.7%] weakens the §B partisan-bias finding to a directional-only claim without the follow-through discipline §3.6's Revision C would require. |
| S5-02 | Confounders | HIGH | 2023-electorate confounder: §3.5 engages this via cross-election stability (2015 +0.03 / 2019 +0.75 / 2023 −0.51 / April 2026 polling matches 2023). The headline survives in the §3.5 bracket; **but the academic paper's Stress-Test Preamble bullet 3 and the §7 synthesis table continue to report 0.51–1.52 pp as a property of "the minority map" rather than as a property of "the minority map scored against 2023 votes"**. This is a framing vs. finding mismatch. |
| S5-03 | Confounders | MED | Turnout confound (2019 67% vs 2023 59%): the cross-election test takes ED-level vote totals as given; selection-into-voting differences between the two elections are *not* modelled. A hostile reviewer will say "the 2023 electorate's ~8-pp lower turnout is partly *why* the asymmetry shows up under 2023 votes — a lower-turnout electorate selects more partisan and more UCP, producing the asymmetry even under identical boundaries." Not fatal; worth explicit disclosure. |
| S5-04 | Confounders | MED | 2024-TBF vs 2021-census basis: §12(3) discussion is thorough (`v0_1_plan_b_cross_check.md`, `v0_1_cycle_lag_analysis.md`). The Plan-B cross-check shows every justification verdict is invariant to basis choice, which resolves the most plausible confound. Worth explicit note in §3 rather than only in the footer paragraph. |
| S5-05 | Confounders | HIGH | Hybrid urban/rural weight (70/30) sensitivity: the tested range 0.55–0.85 omits straight 50/50 (area-weighted for roughly-equal-territory hybrids) and population-weighted (where absorbed rural territory contains 10–20% of population). The audit's §3.4 range is defensible against a ±15pp jitter attack but not against an "assume hybrids are half-urban-by-population" attack. |
| S8-01 | Researcher DoF | LOW | 21 hybrids in school-division coherence audit: defined ex ante as "every minority ED with `-hybrid` or `-merged` in the `region_type` column of `v0_1_minority_2026_populations.csv`." That's a data-driven, non-arbitrary filter. Not a cherry-pick. |
| S8-02 | Researcher DoF | MED | "Focus regions" Calgary / Edmonton / Red Deer / Lethbridge / Airdrie / St. Albert / RMH-Banff: these are the regions where the two commission maps *visibly differ*. The majority symmetry counter-test (§3.13) demonstrates the Edmonton null holds and discovers Red Deer and Lethbridge 4-way patterns (added to the finding list honestly). Residual: **the audit never runs a full ED-level `differ-by-polygon` test** (as flagged in the framework) — the §3.13 counter-test checks city-level 4-way splits but not all 89 EDs for minority/majority geographic divergence. |
| S8-03 | Researcher DoF | MED | P1/P2/P3, C1/C2/C3, E1/E2/E3 numeric thresholds: the paper's §3.7 pre-registration-provenance paragraph documents that `v1_2_gerrymander_audit_prompt.md` committed the thresholds at `5b0bc06` (2026-04-22 08:32:20) and the detection run at `282bc6d` (same day 10:56:11). **Intra-session pre-registration (2h 24m separation, single author, no third-party custody)** is a weak pre-registration. The OSF plan closes this for the November map; it does not close it retroactively. |
| S8-04 | Researcher DoF | HIGH | E2 reformulation from "eligibility-only" to "alternatives-over-negligible-territory" happened *after* the corrected §15(2) re-audit showed the narrow test fails. The paper discloses this at §3.9 end, but a reviewer will read this as a post-hoc rescue of the engineered-boundary signature. The substantive E2 test is itself reasonable; the *move from narrow-E2 to substantive-E2 under pressure* is the cherry-picking concern. |
| S8-05 | Researcher DoF | MED | n=7 Canadian base-rate sample: `v0_1_canadian_base_rate_computed.md` exclusion criteria are methodologically principled (Nova Scotia 2019's menu-of-four structure is not structurally comparable) but the sample is shallow. Limits section admits pre-2010 cycles and federal cycles outside Alberta are absent. A methods reviewer will say: "expand first, then cite the position in the distribution." |
| S8-06 | Researcher DoF | MED | 338Canada 77-snapshot historical stability probe: snapshot window (2020-02-23 → 2026-04-12) captures the 2019→2026 era; it does not extend back to 2015 or 2017. The audit uses this correctly to qualify the "1-seat gap is structural" claim (it's state-dependent), which *strengthens* the paper, not weakens it. But the window is a selection. |

**Severity counts:**

| Dimension | CRITICAL | HIGH | MED | LOW | Total |
|---|---:|---:|---:|---:|---:|
| S3 Reproducibility | 0 | 5 | 2 | 1 | 8 |
| S4 Falsifiability | 0 | 4 | 2 | 1 | 7 |
| S5 Confounder control | 0 | 2 | 3 | 0 | 5 |
| S8 Researcher DoF | 0 | 1 | 4 | 1 | 6 |
| **Total** | **0** | **12** | **11** | **3** | **26** |

No CRITICAL findings — the audit is internally coherent and honest about its limits. 12 HIGH findings cluster on two themes: (a) the MCMC ensemble's real statistical power is much smaller than the nominal sample size suggests (S3-02) and the full-coverage rescore demotes the headline p100 flag to p95 (S3-04); (b) the falsifiability and confounder engagement around the cross-election contingency (§3.5) is present but *framed inconsistently* — the paper's headline treats 2023-specific asymmetry as a property of the map rather than of the map-times-electorate interaction (S5-02, S4-01, S4-07).

---

## Per-dimension discussion

### S3 — Reproducibility (conceptual)

**S3-01 MCMC seed plumbing.** The ensemble script hardcodes `seed=42` at `analysis/scripts/v0_1_mcmc_ensemble.py:439` with the CLI only exposing `n_steps`:

```python
def main(n_steps: int = 5000, seed: int = 42):
    np.random.seed(seed)
    ...
if __name__ == "__main__":
    n = 5000
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    ...
    main(n_steps=n)
```

A reviewer who wants to verify seed-invariance of the p100 flags must edit source. For a publication-grade methodology paper this is a routine ask. The fix is a one-line `argparse` addition.

**S3-02 MCMC effective sample size.** The 100k run's convergence diagnostics (`data/v0_1_mcmc_convergence_diagnostics_100k.json`) show autocorrelation integrated time τ ≈ 624–674 across the four metrics, giving `n_eff ≈ 148–160`. This is the load-bearing number for tail-percentile claims. At `n_eff ≈ 150` the standard error on a tail percentile is materially wider than 1/100,000. The audit's §3.11 language ("100,000-sample publication-grade MCMC run") implies the naive 100k SE; the honest SE is the τ-corrected one. A reviewer will ask: "what does p100 mean when you have 150 effective draws?" The answer is that both the 2019 mean-median p96.1 and the minority p100 flags rest on the right tail of a distribution with ~150 independent samples, which is lab-worthy but not lawsuit-worthy.

**S3-03 Urban-weight sensitivity range gap.** The tested range is 0.55–0.85 (Monte Carlo) and 0.60–0.80 (point). A reviewer familiar with the political-geography literature will ask: "what about a straight 50/50, or a population-weighted alternative?" The `threshold_provenance.md` Part C sensitivity range is defended as "±10 pp about central 0.70" — this anchors on the audit's choice rather than on the empirical hybrid composition. A straight 50/50 is off-range by 10 pp on the low side and would produce a materially different picture for minority 2026 hybrids with heavy rural content. The audit does not report this swap.

**S3-04 Full-coverage rescore moves the minority off p100.** This is the single most-important finding of this red-team, because it directly touches the paper's headline §3.11 claim. The full-coverage rescore file (`data/v0_1_mcmc_ensemble_percentiles_full.csv`) shows:

| Metric | Paper §3.11 (partial coverage) | Full-coverage rescore |
|---|---|---|
| Mean-median (minority 2026 v6) | **p100.0** | **p95.35** |
| Seats-at-50/50 (minority 2026 v6) | **p100.0** | **p89.72** |

The paper's §3.11 states "a 100,000-sample publication-grade MCMC run, with full-coverage rescore and convergence diagnostics (effective sample size per metric, trace plots), is in progress and will be reported in `analysis/methodology/v0_1_mcmc_100k_and_full_coverage.md`" and further states "If either artifact shifts the tail-percentile verdicts, §3.11 will be revised and a change note added." The artifact *has* shifted a verdict (mean-median p100 → p95.35; seats-at-50/50 p100 → p89.72 — inside the 5–95 band), and §3.11 has not yet been revised. For a paper submission, this is a hard blocker. The falsifiability hook the paper set for itself has fired.

**S3-05 Declination sign/convention swap.** The sign-convention resolution doc (`v0_1_sign_convention_resolution.md`) is detailed and correct on the EG convention, but the audit does not produce the same analysis for declination. Warrington (2018) defines positive declination as favouring the first-party; the audit's code (`compute_metrics()`, lines 156–173) calls this "positive = pro-NDP; negative = pro-UCP" via its own derivation. The ordinal ranking of the three maps survives a sign flip; the label does not. A reviewer citing Warrington (2018) from memory will read the paper's declination direction opposite to its actual label. Needs a matching footnote.

**S3-06 Compactness formulation swap.** The audit reports Polsby-Popper and Reock (§6.7). The literature also commonly reports Convex-Hull (ratio of district area to convex hull area) and Schwartzberg (perimeter / circumference of equal-area circle). A reviewer may ask whether the "minority's mean Polsby-Popper is modestly lower" finding survives under Schwartzberg; the audit does not engage this. The underlying claim about Calgary Zone A **does not depend on compactness** — it depends on population-zone gap — so the swap-risk is local to §6.7 rather than to the headline. MED not HIGH.

**S3-07 VA centroid-in-polygon.** Paper states "centroid-in-polygon assignment. VAs that straddle proposed-ED boundaries get assigned by their interior point, not split. This introduces rounding error on the order of the boundary-VA vote totals. For Alberta where VAs are small relative to EDs this error is <0.5% on every metric." Reasonable in magnitude (VAs are much smaller than EDs and border-crossing VAs are a small fraction). A swap test with half-VA edge bias is not executed but the error is plausibly capped. LOW.

**S3-08 2015-vote sign-convention stacking.** The 2015-vote rerun was executed; result +0.03 pp. Paper's §3.5 reports "2015 +0.03 pp under this paper's convention: positive asymmetry = minority less UCP-favourable." The companion analysis (`v0_1_2015_cross_election_analysis.md`) reads this under the S-M convention as "minority MORE pro-UCP than majority." The sign-convention-resolution doc (`v0_1_sign_convention_resolution.md`) resolves the conflict in the paper's favour but the 2015 analysis doc has not been updated. A reviewer reading the 2015 analysis doc first will find two mutually-contradictory "verdicts" in the audit bundle. The paper's text is defensible (+0.03 pp in the NDP-advantage direction under the paper's 1:1 proportional convention = essentially neutral). The companion analysis needs a sign-convention note or retraction of its "MORE pro-UCP" reading.

### S4 — Null hypothesis + falsifiability framing

A finding-by-finding audit. For each the null, the falsification condition, and whether the condition is currently testable.

| Finding | Null hypothesis being rejected | Falsification condition | Testable now? | Status |
|---|---|---|---|---|
| "Minority more UCP-favourable than majority by 0.51–1.52 pp" (§3.3) | No inter-map partisan-bias asymmetry beyond natural-ensemble noise | Phase 4C measured attribution with opposite sign at 0.70 central weight | **No — blocked on 2026 shapefile** | S4-01 HIGH |
| "Calgary Zone A packing: 12.2% gap vs 0.4%" (§A2) | The 12.2% gap is an artefact of the classification rule (Bow/Deerfoot line) | G4 2023-winner-based classification produces near-null | Yes — G4 test produces 7.71%, still >10× majority | S4-02 MED |
| "Airdrie 4-way is a cracking pattern" (§3.8) | Airdrie's 4-way split is forced by population arithmetic | Airdrie (84k, 2025 est) fits in ≤2 EDs at ±25% | Yes — `v0_1_justification_tests.py` | S4-03 MED |
| "Engineered boundary at RMH-Banff Park" (§3.9) | Purposive reading of §15(2) supports NP extension / extension is statutorily needed | Under narrow E2: re-audit finds ED qualifies 4/5 without extension (narrow E2 fails). Under substantive E2: alternative populated territories (Caroline, Nordegg, etc.) existed and were not taken | Yes, under substantive E2; narrow E2 has failed | S4-04 HIGH (criterion reformulated mid-audit) |
| MCMC p100 on minority (§3.11) | Minority 2026 inside the ReCom-reachable neighbourhood distribution | Minority percentile drops below 95 on the full-coverage rescore | **Yes — the full-coverage rescore has shifted to p95.35 mean-median and p89.72 seats-at-50/50** | S4-05 LOW — but see S3-04: falsification fired for seats-at-50/50 |
| "Three of five 'no public support' chair characterisations materially fail" (§5.4) | All five have zero genuine supporting submissions | 1,252 of 1,340 submissions with text layer, searched via regex + manual review; counter-examples identified for three | Yes, conditional on text-searchable subset (93%) | S4-06 HIGH for residual 7% OCR gap |
| "Six dimensions directionally consistent" (§7) | Six binary signs agree by chance across six dimensions | Under independence 6/6 = 1/64 ≈ 1.56% (two-sided) or 1/32 ≈ 3.1% (one-sided). Under correlation the null is laxer. | **Chance p-value is not computed in the paper.** Six dimensions include MAD (§A1) and Calgary-zone (§A2) which are *correlated* (both driven by population distribution); independence assumption not defended | S4-07 HIGH |

The paper's §10 falsifiability section enumerates five named falsification conditions for the macro claim. These are good — each is a specific observable that would retract the finding. But three of the six findings listed in the synthesis table (§7) do **not** have individual null/falsification pairs stated in their own prose. A peer reviewer will ask: "what would I observe that would retract your Calgary Zone A packing claim specifically, independent of the six-dimension pattern?" The answer exists (a G4 robustness check with opposite direction would do it) but is not stated in §3.7 or §A2 prose. This is fixable by a one-paragraph add per finding.

The **6-of-6 directional-consistency claim (§7) needs the most attention**. Under naive binary independence, 6/6 alignment is p = 1/64 = 1.56% two-sided. But the six dimensions are not independent: A1 (MAD) and A2 (Calgary zone gap) both derive from population distribution and are correlated; A2 and C4 (Airdrie splits) both measure within-city treatment and are partly correlated; B (partisan bias) and §D (procedural) are plausibly correlated via political incentive. A reviewer will ask: what is the effective number of independent dimensions? Likely closer to 3–4 than 6. Under 4 independent dimensions, 4/4 alignment is p = 1/16 = 6.25% — still evidence, but not the "five-nines" directional signal the §7 framing implies. This is a HIGH S4 finding that the paper can fix without changing the underlying evidence: compute a simple pairwise correlation matrix across the six dimensions, or state a "k independent dimensions under reasonable grouping" bound and report under that.

### S5 — Confounder control

Two confounders the audit MUST address (per the science framework):

**1. Chen-Rodden natural geographic packing.** Engagement is genuine and detailed (`v0_1_chen_rodden_alberta_validation.md`). The audit finds:

- Direction prediction transfers: neutral 87-seat Alberta maps produce UCP-favourable EG centered near the 2019 baseline of −2.64% (CI [−4.4%, −0.7%] after advance-ballot scaling).
- Mechanism prediction fails: Alberta's UCP-favourable floor is not produced by NDP urban packing (NDP surplus 9.3%) but by UCP rural dispersion (UCP surplus 15.9%; rural UCP winning margins 43.0 pp vs urban NDP 21.5 pp).
- Both 2026 maps sit inside the neutral range; the majority is closer to zero and the minority is closer to the neutral median.

**This is a thorough engagement but the implication is uncomfortable for the paper.** Revision C (explicit) from the Chen-Rodden validation doc states: *"Under that reading, neither 2026 map is engineered against the natural floor; both are consistent with neutrally-drawn plans."* The academic paper §3.6 implements a softer Revision A/B. If a reviewer applies Revision C rigorously, the §B partisan-bias finding contributes only directionally to the six-dimension synthesis, not as a distinguishing-magnitude finding. The paper's §7.2 synthesis text does acknowledge this ("some portion of the minority-to-majority partisan-bias gap is not attributable to engineering"), which is what keeps this finding at MED rather than HIGH. What would push it to HIGH is a reviewer demanding the full GerryChain ReCom ensemble (not the single-unit flip walk) — which the audit concedes is future work.

**The quantitative answer to "what fraction of the minority-vs-majority asymmetry is attributable to geography vs. drawing choices?" is not computed.** The Chen-Rodden validation addresses only the *absolute* level (both 2026 maps inside neutral range); it does not decompose the 0.51 pp *gap* between the two 2026 maps into geography and drawing components. This is the specific decomposition a reviewer will ask for. Currently the paper's claim is: both are inside the neutral band, and the minority is closer to the neutral median than the majority is. This is a qualitative statement. A reviewer will prefer "X% of the 0.51 pp gap is attributable to how the two maps differ in their treatment of natural packing, Y% is attributable to other drawing choices." That decomposition requires a paired ensemble — the audit acknowledges this as pending.

**2. 2023-electorate confounder.** Engagement exists via cross-election stability (§3.5):

| Election | Minority-Majority EG asymmetry (paper's convention) |
|---|---|
| 2015 | +0.03 pp (minority less UCP-favourable — essentially neutral) |
| 2019 | +0.75 pp (minority less UCP-favourable — direction reverses) |
| 2023 | −0.51 pp (minority more UCP-favourable — paper's headline) |
| April 2026 338Canada polling | ~−0.5 pp (direction matches 2023) |

The paper's §3.5 states this contingency honestly. The academic paper's **Stress-Test Preamble bullet 3** acknowledges the sign flip under 2019 votes and reports the direction as "stable across 2020s-era political geography but not across the 2019 electorate." Good.

**The residual HIGH finding (S5-02):** The §7 synthesis table and §3.3 results table continue to state "Minority 2026: EG −1.36%" and "+0.58 pp more UCP-favourable" as properties **of the map**, without the ", under 2023 votes" qualifier. A peer reviewer who reads §7 before §3.5 will come away with the impression that the partisan-bias property is a structural property of the drawing; they will not learn the contingency until §3.5. This is *framing* rather than *substance*, but framing-vs-finding alignment is exactly the kind of thing a methods-paper reviewer will flag. Easy fix: consistent ", under 2023 vote input" qualifier wherever the EG numbers appear in summary tables.

**Additional confounders (check list):**

- **Turnout differences between 2019 (67%) and 2023 (59%) — S5-03 MED.** The 2023 election had roughly 8 pp lower turnout than 2019, with well-documented differential turnout patterns (older voters, rural voters, and UCP-leaning voters more likely to turn out in a low-turnout cycle). A non-random selection into 2023 voting is conceptually different from "the electorate shifted"; it's *who showed up* from a potentially-stable distribution. The audit treats 2023 votes as given (correctly — that's what a statement of vote is). But a reviewer can legitimately ask: would a modelled 2023 "full-electorate-hypothetical" (turnout-inflated) produce the same asymmetry? This is not modelled. Not fatal; worth a paragraph acknowledging that the 2023 asymmetry is computed on 2023 actual voters, and that turnout-mediated selection effects contribute to, but are not separable from, the "2023 electorate" effect §3.5 describes.

- **2024-TBF basis vs 2021-census basis — S5-04 MED.** The §12(3) compliance discussion is thorough. Plan-B cross-check shows justification verdicts invariant to basis choice. The audit is on solid ground here. The reason this is still MED rather than LOW is that the §2 and §7 tables inherit the 2024-TBF basis without a sentence-level reminder that the statutory basis is the 2021 census — a reviewer reading the §7 synthesis may not know the population numbers derive from 2024 TBF until they reach the footnote paragraph. A one-sentence reminder at §2.1 opening would close this.

- **Urban-weight sensitivity range width — S5-05 HIGH.** The test range 0.55–0.85 (Monte Carlo) and 0.60–0.80 (point) is defended as "±10–15 pp about central 0.70." This defence is methodology-internal; it does not map to the empirical question "what fraction of hybrid-ED voters live in the urban core vs the absorbed rural area?" A population-weighted hybrid (which would typically put a rural component at 10–20% of the hybrid population for Calgary-ring hybrids but up to 30–40% for Red Deer hybrids) is inside the tested range for most hybrids but at the edge for some. A straight 50/50 (0.50) is *outside* the tested range and would produce a qualitatively different picture. The audit does not report the straight 50/50 case. A reviewer will ask for it. The likely effect is to narrow the asymmetry magnitude further (both maps' EGs move toward each other as rural weight increases), which *weakens* the paper but remains directionally consistent.

### S8 — Cherry-picking / researcher degrees of freedom

**S8-01 Hybrid count of 21.** Defined ex ante via the `region_type` column in `data/v0_1_minority_2026_populations.csv` (any ED flagged `-hybrid` or `-merged`). This is a data-driven, non-arbitrary filter. A reviewer who asks "why 21?" gets the answer: "that's how many hybrids the minority map has; the filter is mechanical." Not cherry-picking. LOW.

**S8-02 Focus regions (Calgary, Edmonton, Red Deer, Lethbridge, Airdrie, St. Albert, RMH-Banff).** Defensible as "where the two maps visibly differ." The majority symmetry counter-test (§3.13) demonstrates the Edmonton null holds (zone gap 1.4–2.0 pp vs Calgary's 12.2 pp) and discovers Red Deer and Lethbridge 4-way patterns (added honestly and pre-registration-caveated). The Edmonton null is the crucial symmetric check. Residual: **the framework asked for a `differ-by-polygon` test across all 89 EDs**, which the §3.13 counter-test does not run. The city-level 4-way split test is a subset of the full polygon-level differ test. Running the full differ test would confirm the focus regions capture all materially-different EDs. MED. Not fatal — the counter-test at §3.13 is a reasonable proxy — but a reviewer will ask.

**S8-03 P/C/E numeric thresholds.** Pre-registration provenance is documented via git timestamps (`5b0bc06` at 08:32:20; detection at `282bc6d` at 10:56:11, separation 2h 24m). This is intra-session; single-author; no third-party custody. The audit acknowledges this as "residual vulnerability" and flags the November 2026 map as the held-out test under an OSF-submitted pre-registration. The intra-session pre-registration is *weak* pre-registration but it is not *no* pre-registration, and the signed/dated thresholds correspond closely to literature-anchored values (P2 at 34 pp safe-seat cut-off is above Chen 2017's 20 pp; C3 at ±25% is the statutory band; P1 at +5% is 1/5 of the statutory band). The *substance* of the thresholds is defensible; the *process* of pre-registering them is internal, not external, which is what the OSF plan fixes. MED.

**S8-04 E2 reformulation.** This is the clearest post-hoc concern in the audit. The original E2 ("without the extension, the ED would not qualify") was operationalised against the corrected §15(2) thresholds in the §2.4 re-audit, which found the ED qualifies 4/5 without the extension. Rather than retracting the engineered-boundary signature, the audit reformulated E2 to "alternatives existed and were not taken" and preserved the signature. The reformulation is *disclosed* (§3.9 openly states this) and is *substantively reasonable* (the purposive reading of §15(2) is a legitimate interpretive framework supported by *Rizzo v. Rizzo Shoes*). But: a reviewer sees the pattern (narrow test fails → criterion softened → finding preserved) and will apply the post-hoc discount. HIGH.

The appropriate peer-review response is not to retract the engineered-boundary finding (the substantive E2 test holds on its own merits, and the populated-alternatives evidence is empirically robust) but to (a) move the substantive E2 test to the primary definition in §3.9 so the narrative does not read as a reformulation, (b) retain the narrow-E2 discussion as a subsidiary "additional observation" rather than the original framing, and (c) be honest that under a strict pre-registration discipline with narrow E2 as the pre-committed criterion, the engineered-boundary signature count would be zero, and the headline "three formal signatures" would become "two formal signatures plus one substantive-E2 finding." The paper's current framing tries to have it both ways.

**S8-05 n=7 Canadian base rate.** Selection is principled: most-recent preliminary-vs-final pairs from provincial and federal commissions, excluding Nova Scotia 2019 (menu-of-four structure) and government-override cycles (not interim-vs-final). Limits section acknowledges gaps (pre-2010, federal 2002, Quebec 2017, Ontario 2013). A reviewer will say: "before positioning Alberta 2025-26 at the 71st percentile of a 7-cycle distribution, expand to ≥20 cycles." This is correct peer-review practice. Severity MED rather than HIGH because the audit flags the limitation explicitly and reports the high-end 1.6 pp figure as exceeding the 7-cycle max.

**S8-06 338Canada snapshot window.** 77 snapshots from 2020-02-23 to 2026-04-12. The audit uses this to show that the 1-seat minority-vs-majority gap's *direction* is state-dependent (UCP-landslide conditions flip it NDP-favourable; competitive conditions give UCP +1–3 seats on the minority; NDP-wave conditions flip the other way). This is a good, honest, audit-strengthening use of the data. The window selection (2020–2026) is pragmatic: it's the available 338Canada per-riding data. A 2015–2020 extension is not feasible because 338Canada's Alberta model did not exist pre-2020. MED for window selection; LOW in substance because the audit uses this to *narrow* its claim (structural-invariance retracted, state-dependence reported), which is exactly the right scientific move.

---

## Null-hypothesis + falsification-condition table (§S4 consolidated)

| # | Finding (as stated in paper) | Null hypothesis | Falsification condition | Testable now? | Current status |
|---|---|---|---|---|---|
| N1 | Minority more UCP-favourable than majority by 0.51–1.52 pp (§3.3, §3.4) | No inter-map asymmetry beyond modelling noise | Phase 4C measured attribution with opposite sign at central weight, or Monte Carlo CI lower bound > 0 (wrong sign) | Partially — 90.5% direction consistency observed; magnitude CI [−3.04, +0.76] crosses zero | Defensible as directional; magnitude retracted |
| N2 | Calgary Zone A packing 12.2% vs 0.4% (§A2) | Gap is a classification-rule artefact | G4 robustness produces near-null direction OR any other reasonable classification gives <10× majority | No — G4 test gives 7.71%, still >10× majority (0.39%) | Null rejected |
| N3 | Airdrie 4-way is cracking (§3.8) | 4-way is population-forced | Airdrie fits in ≤3 EDs at the ±25% band | Yes — 84k fits in 2 EDs at +25% ceiling (68,661/ED) | Null rejected |
| N4 | RMH-Banff Park engineered (§3.9) — substantive E2 | Purposive §15(2) reading supports extension / no populated alternatives exist | Alternative populated territories (Caroline, Nordegg, Mountain View County, Bighorn MD, Sundre) are inconsistent with the rest of the district's community of interest | Yes — populated-alternatives evidence in §3.9 | Null rejected under substantive E2; null *not* rejected under narrow E2 |
| N5 | Minority at p100 on mean-median and seats-at-50/50 against ReCom ensemble (§3.11) | Minority inside the ReCom-reachable neighbourhood distribution | Minority percentile drops inside 5–95 on rescored ensemble | **Yes — the full-coverage rescore has fired this condition for seats-at-50/50 (p89.72) and partially for mean-median (p95.35)** | **Seats-at-50/50 falsification has FIRED. Paper §3.11 not yet revised.** |
| N6 | 3 of 5 "no public support" characterisations fail (§5.4) | Zero supporting submissions across all five | For each failing configuration, ≥1 documented supporting submission | Yes for 93% of submissions (text layer); 7% unscanned | Null rejected for RMH-Banff, ODH, Chestermere; upheld for Airdrie 4-way, Nolan Hill-Cochrane; ambiguous for Red Deer |
| N7 | Six dimensions directionally consistent (§7) | Chance agreement across 6 binary signs | Either the computed p-value under independence exceeds α, OR the effective number of independent dimensions is small enough to make 6/6 non-surprising | **Chance p-value not computed; independence not justified** | HIGH — audit must compute or bound |
| N8 | 2023-vote asymmetry is state-dependent (§3.5) | Direction holds across 2015, 2019, 2023 electorates | Direction flips under any 2020s-era Alberta general election | **Direction flips under 2019 and 2015 votes** | Paper correctly reports this contingency. Direction stable across 2020s-era inputs only. |

**Overall:** five of eight findings have clean null / falsification pairs, three are HIGH problems (N5 has fired, N7 is uncomputed, N4's E2 reformulation). The N5 fire is the most acute — §3.11 needs a revision note before submission.

---

## Confounder engagement status table (§S5 consolidated)

| Confounder | Engagement location | Quantitative decomposition present? | Residual risk | Severity |
|---|---|---|---|---|
| Chen-Rodden natural packing | §3.6 + `v0_1_chen_rodden_alberta_validation.md` | Partial — absolute level (both 2026 maps inside neutral range) present; decomposition of 0.51 pp gap into geography vs drawing is missing | A reviewer may push for full GerryChain ReCom decomposition of the 0.51 pp gap | MED |
| 2023-electorate effect | §3.5 + Stress-Test Preamble bullet 3 | Present via cross-election stability (2015, 2019, 2023, April 2026 polling) | §7 synthesis table does not carry the ", under 2023 votes" qualifier; framing-finding mismatch | HIGH |
| Turnout (2019 67% vs 2023 59%) | Not modelled | No | Differential selection-into-voting is conceptually different from "electorate shifted" | MED |
| 2024-TBF vs 2021-census basis | §12 discussion + `v0_1_plan_b_cross_check.md` | Thorough — Plan-B shows verdicts basis-invariant | §2 / §7 tables inherit 2024-TBF basis without inline reminder | MED |
| Urban/rural hybrid weight | §3.4 sensitivity (0.60–0.80) + Monte Carlo (0.55–0.85) | Present, but not covering 0.50 straight / population-weighted / area-weighted | A reviewer can ask: "what if hybrids are half-urban-by-population?" — not currently reported | HIGH |

---

## Researcher-degrees-of-freedom exposure table (§S8 consolidated)

| Choice | Made ex ante or post-hoc? | Disclosure level | Alternative tested? | Severity |
|---|---|---|---|---|
| 21 hybrid set for school-division audit | Ex ante (filter on `region_type` column) | Clear; data-driven filter | N/A | LOW |
| Focus regions (Calgary / Edmonton / Red Deer / Lethbridge / Airdrie / St. Albert / RMH-Banff) | Ex post but principled (where maps differ) | Clear; symmetric counter-test in §3.13 | Edmonton symmetric test run, Red Deer and Lethbridge added honestly when found | MED (full 89-ED differ test not run) |
| P/C/E numeric thresholds | Intra-session pre-registration (git-timestamped, 2h 24m separation) | Clear; `threshold_provenance.md` is paper-grade | Sensitivity band ±20% for P1, P2, 70/30 | MED (intra-session is weak pre-reg; OSF fixes for November map) |
| E2 reformulation (narrow → substantive) | **Post-hoc after §15(2) re-audit** | Clear; §3.9 discloses openly | Substantive E2 is defensible on its own; narrow E2 fails | HIGH (pattern recognition: criterion softened after original failed) |
| n=7 Canadian base-rate sample | Ex ante selection criteria applied consistently | Clear; limits section explicit | Nova Scotia 2019 excluded on structural-comparability grounds; pre-2010, federal non-Alberta not included | MED (sample too small for confident percentile placement) |
| 338Canada 77-snapshot window | Ex ante (available data window 2020–2026) | Clear; window rationale given | Pre-2020 data unavailable | LOW |

---

## What the audit gets right (reproducibility / falsifiability / confounder / DoF)

To be honest with the methodology review: the audit has done a substantial amount of work in each of these dimensions that a reviewer will value.

- The sign-convention resolution doc (`v0_1_sign_convention_resolution.md`) is the kind of internal-discipline artefact methodology papers rarely produce. It is diligent and correct on EG.
- The three-election cross-election test (2015 + 2019 + 2023 + April 2026 polling) is the kind of hard test that takes hours to execute and that the audit ran. The verdict (state-dependent direction, structural invariance retracted) is a stronger finding than the pre-execution hypothesis.
- The Chen-Rodden validation is a 150-plan ensemble with Moran's I and margin-asymmetry decomposition. The mechanism correction (UCP rural dispersion, not NDP urban packing) is a peer-quality finding that tightens the audit rather than dissolving it.
- The symmetry-of-test-selection counter-test (§3.13) is good methodology practice. It *discovered* two new findings (Lethbridge and Red Deer 4-way) and reported them separately from the pre-registered Airdrie cracking signature.
- The Canadian base-rate computation (`v0_1_canadian_base_rate_computed.md`), despite its n=7 limit, is the correct *kind* of external anchoring for a methodology paper.
- The submission-search verification of the chair's "no public support" claim (§5.4) is labour-intensive and tiered into "precisely wrong" vs "effectively wrong," a discipline many political-analysis reports do not observe.
- The threshold provenance compendium is paper-grade and defends each numeric choice against a hostile reviewer.

**The audit is a strong methodology submission with specific, fixable defects.** The 12 HIGH findings above are revise-and-resubmit issues, not reject issues. There are no CRITICAL findings in this red-team's scope.

---

## Concrete recommendations for the revise-and-resubmit pass

1. **§3.11 MCMC update (S3-04).** Replace p100 / p1.7 headline numbers with the full-coverage rescore numbers (mean-median p95.35, seats-at-50/50 p89.72 inside the 5–95 band). Retain mean-median p95 as a flagged result; retract seats-at-50/50 as outside the flag zone. Add a change note citing the falsifiability hook the paper set for itself at §3.11 end.

2. **§3.11 effective sample size disclosure (S3-02).** Report `n_eff ≈ 148–160` per metric alongside the nominal 100,000. State that tail-percentile SE is τ-corrected (with τ ≈ 625–674 integrated autocorrelation time). A reviewer will thank you.

3. **§3.5 and §7 framing harmonisation (S5-02).** Every appearance of "minority 2026 EG −1.36%" or "Minority 2026" in summary tables needs ", under 2023 vote input" qualifier. The contingency is stated in §3.5 prose but needs to propagate to headline table labels.

4. **§7 chance-agreement p-value (S4-07).** Compute and report either a 6/6 directional-consistency p-value under independence assumption (flag independence as optimistic) or an effective-dimensions bound (k=3 or k=4 with rationale). Current "directional consistency" language implies a stronger probabilistic claim than is substantiated.

5. **§3.9 E2 primary-definition cleanup (S8-04).** State substantive E2 as the primary definition in §3.9 opening; move the narrow-E2 discussion to "additional observation." Acknowledge explicitly: under a strict narrow-E2 pre-registration discipline, the engineered-boundary signature count would be zero.

6. **Hybrid-weight additional swap (S3-03, S5-05).** Report the 0.50 straight case and the population-weighted case in §3.4. Expected outcome: magnitude narrows further; direction remains.

7. **MCMC seed plumbing (S3-01).** Add `argparse` seed support to `v0_1_mcmc_ensemble.py`. One-liner, supports reviewer replication.

8. **Sign-convention internal consistency (S3-08).** Update `v0_1_2015_cross_election_analysis.md` to use the paper's 1:1 proportional convention (per resolution in `v0_1_sign_convention_resolution.md`), or add a prominent top-of-doc note that the 2015 doc uses the S-M 2:1-slope convention for framing purposes.

9. **Decomposition of 0.51 pp gap (S5-01).** For revise-and-resubmit, the paired GerryChain ReCom ensemble on both 2026 substrates (when shapefiles arrive) will enable a geography-vs-drawing decomposition of the minority-vs-majority asymmetry. Commit to this in the limitations / future work section.

10. **Per-finding nulls in §3.7–§3.10 (S4 various).** Add a one-paragraph null statement to each of the P1–P3, C1–C3, E1–E3 sections mirroring the structure of the table above. This is low-effort and closes the "would I know what would falsify this specific finding?" question for each signature independently of the six-dimension synthesis.

---

## How this red-team interacts with other framework passes

- **Legal D4 (reproducibility — computational).** S3-01 and S3-02 overlap with D4's "does the code run" check. D4 verifies commands execute; S3 verifies conceptual swaps produce stable findings. The two are complementary.
- **Science S1 / S2 (design & stats — sibling file).** S8-04 (E2 reformulation) overlaps with S1 (pre-registration discipline) — both flag the same event from different angles. S3-02 (effective sample size) overlaps with S2 (statistical power).
- **Legal D10 (time-stamping).** The intra-session git-timestamped P/C/E thresholds (S8-03) are a legal time-stamping claim and a science pre-registration claim. Legal D10 should reference the same artefact.
- **Science S7 (data quality).** The 7% OCR gap (S4-06) is a data-quality residual; S7 sibling will assess whether 93% text-layer coverage is peer-review-defensible. Both dimensions flag it; the science question is "is 93% enough evidentiary support for the 3/5 refutation?" (likely yes, because the refutation rests on found counter-examples not exhaustive enumeration) — but the dimension S7 sibling is closer to this question.

---

## Final verdict

**Net severity:** 12 HIGH, 11 MED, 3 LOW, 0 CRITICAL. The audit is internally coherent and honest about its limits. It is a revise-and-resubmit submission, not a reject. The most acute single fix is the §3.11 MCMC update (S3-04) — a falsifiability hook the paper set for itself has fired on the full-coverage rescore, and the paper text has not yet caught up. Fixing that one issue, propagating the cross-election contingency qualifier through the synthesis table (S5-02), and computing a chance-agreement p-value for the six-dimension synthesis (S4-07) would move the audit from revise-and-resubmit to accept-with-minor-revisions under the review standards of *Election Law Journal* and *Statistics and Public Policy*.

**Author's posture note.** This review applies peer-review standards; it is not a legal review or a political-science critique of the paper's substantive conclusions. The substantive conclusions (directional-six-dimension asymmetry; procedural concerns about April 16; tiered refutation of the chair's "no public support") survive this review.
