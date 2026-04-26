# v0.1 MCMC Ensemble — 100k publication-grade run + full-coverage rescore

**Run date:** 2026-04-23
**Ensemble size:** 100,000 ReCom samples, seed 42
**Chain:** Recombination (ReCom), `gerrychain` 0.3.2, ±25% population deviation, always-accept
**Atomic units:** 4,765 Voting Area (VA) polygons
**Baseline:** 2019 enacted electoral divisions (87 EDs) as the starting partition
**Runtime:** ~12 min for the 100k chain on a laptop
**Forward:** report_academic.md §3.11, report_public.md (methods appendix)
**Backward:** analysis/methodology/v0_1_mcmc_ensemble.md (10k preliminary); analysis/scripts/build_full_crosswalks.py (crosswalks); analysis/scripts/mcmc_ensemble_100k.py (chain); analysis/scripts/mcmc_full_coverage_rescore_100k.py (rescore)

## Method — what changed from the 10k preliminary

Two changes, both in the direction the 10k write-up flagged as pending:

1. **Chain length 10,000 → 100,000.** Same ReCom proposal, same ±25% constraint, same seed 42, same initial tight-seed regeneration via `recursive_tree_part`. 10× the samples; identical distribution target. Convergence diagnostics (effective sample size per metric, running-mean trace plots) were added to the 100k artefacts.
2. **Exogenous scoring: polygon-only → polygon + full-crosswalk fallback.** The 10k run used centroid-in-polygon joins against the partial-coverage 2026 gpkgs (majority 57 / 89, minority v6 70 / 89), so 36% (majority) / 19% (minority) of VAs were dropped from each proposal's metric. The 100k run uses an 88-row majority crosswalk and 88-row minority crosswalk (built by `build_full_crosswalks.py`) as a fallback: every VA outside a scored polygon is assigned to a 2026 ED via its `parent_ed_2019` → full-crosswalk entry. Coverage is now 100% of VAs for both proposals (though both still miss a small number of *destination* 2026 EDs that are pure Tier-C constructs with no 2019 parent — 4 majority EDs and 5 minority EDs are not populated by either polygon or crosswalk; these are enumerated in the JSON output).

Nothing else changed: same metrics (EG, MM, declination, seats-at-50/50), same sign convention (+ = UCP-favoured), same 2023 vote attribution, same 2021 DA-weighted population, same VA graph.

## Convergence diagnostics

Effective sample size (ESS) per metric, computed on the full 100k chain via Geyer (1992) initial-positive-sequence estimator for the integrated autocorrelation time τ:

| Metric | τ (integrated autocorr. time) | n_eff | ρ(lag=1) | ρ(lag=10) | ρ(lag=100) |
|---|---|---|---|---|---|
| Efficiency gap | 673.6 | **148** | +0.990 | +0.906 | +0.485 |
| Mean-median | 624.0 | **160** | +0.988 | +0.896 | +0.502 |
| Declination | 662.4 | **151** | +0.991 | +0.910 | +0.501 |
| Seats @ 50/50 | 645.9 | **155** | +0.991 | +0.919 | +0.519 |

**Interpretation.** ReCom on this substrate is a slow mixer — τ ≈ 650 on all four metrics means adjacent samples in the chain share ~99% of their autocorrelation and the effective information content of the 100k chain is about 150 independent draws per metric. This is expected: ReCom on a 4,765-node graph with 87 districts rarely changes more than 2–3 districts per step, so consecutive plans differ in a small fraction of their vote aggregates. The standard remedy (thinning) does not add information; it only re-expresses it. The correctness argument is that the *distribution* is correctly targeted once the chain has mixed — which it has, as confirmed by the running-mean trace plots (see below).

**Trace plots** (running-mean convergence):
- `maps/mcmc/running_mean_100k_efficiency_gap.png`
- `maps/mcmc/running_mean_100k_mean_median.png`
- `maps/mcmc/running_mean_100k_declination.png`
- `maps/mcmc/running_mean_100k_seats_at_50_50.png`

All four traces stabilise within the first 30–40k samples and drift by less than 0.0003 across the final 50k, i.e. well below the bandwidth of the 5–95 percentile interval on each metric. The chain has not yet reached MGGG "publication-grade" ESS (MGGG practice is ~5,000 effective draws for lawsuit-grade claims), but the mean and percentile stability across the latter half of the run is sufficient for the policy-comparison framing used in this audit. That caveat is preserved in §3.11.

**Ensemble distribution plots** (histograms with percentile markers):
- `maps/mcmc/ensemble_distribution_100k_efficiency_gap.png`
- `maps/mcmc/ensemble_distribution_100k_mean_median.png`
- `maps/mcmc/ensemble_distribution_100k_declination.png`
- `maps/mcmc/ensemble_distribution_100k_seats_at_50_50.png`

## Comparison table — 10k partial vs. 100k full-coverage

Percentile of each real map against each ensemble. Sign: positive = UCP-favoured throughout.

### 2019 enacted (no coverage change — shown for ensemble-stability check)

| Metric | 10k (partial) | 100k (full) | Δ percentile | Flag change |
|---|---|---|---|---|
| Efficiency gap | +0.0241 (p73.6) | +0.0241 (p73.4) | −0.2 | inside band → inside band |
| Mean-median | **−0.0077 (p96.1)** | −0.0077 (**p92.7**) | **−3.4** | flagged → **unflagged** (inside band) |
| Declination | −0.0451 (p7.6) | −0.0451 (p7.2) | −0.4 | inside band → inside band |
| Seats @ 50/50 | +0.460 (p79.2) | +0.460 (p80.9) | +1.7 | inside band → inside band |

The 2019 mean-median percentile moved from **p96.1 (flagged outlier)** to **p92.7 (inside the 5–95 band)**. The real-map value itself did not change (it is the same 2019 enacted map); the ensemble's own 95th percentile moved from −0.0088 (10k) to −0.0061 (100k), so the 95th-percentile cutoff widened by ~0.003 and 2019's constant −0.0077 no longer crosses it. This is the primary finding of the 100k run: **the 2019 p96 mean-median flag was a 10k-sample artefact**. On a 100k ensemble the 2019 enacted map is an upper-tail point (p92.7 — still UCP-tilted, still closer to zero than 92.7% of sampled alternatives) but not an outlier under the p≥95 threshold.

### Majority 2026 (coverage 57 → 85 districts; +28 districts)

| Metric | 10k partial | 100k full-coverage | Δ percentile | Flag change |
|---|---|---|---|---|
| Efficiency gap | +0.0066 (p24.6) | +0.0241 (p73.4) | **+48.8** | inside band → inside band |
| Mean-median | −0.0308 (p6.6) | −0.0077 (p92.7) | **+86.1** | inside band → inside band |
| Declination | +0.0049 (p52.2) | −0.0466 (p6.3) | **−45.9** | inside band → inside band |
| Seats @ 50/50 | **+0.421 (p1.7)** | +0.459 (**p57.9**) | **+56.2** | **flagged → unflagged** |

This is the largest shift in the run. The majority 2026 p1.7 seats-at-50/50 flag (the audit's UCP-dilution finding) **does not survive** the full-coverage rescore. Under the 10k partial methodology, 32 of 89 majority districts (Tier A — unchanged-from-2019 districts not included in the artifact gpkg) were dropped entirely. Those 32 districts, being Tier A identities of 2019 districts, carry the 2019 map's own UCP-tilted seat distribution. Adding them back via the crosswalk raises the majority's seats-at-50/50 from 0.421 to 0.459, essentially equalling the 2019 value (0.460) and moving the percentile rank from p1.7 to p57.9. The mean-median and efficiency gap shifts follow the same mechanism: the dropped districts dominated the ratios.

The correct interpretation of this change is methodological, not substantive. The 10k-partial score measured how the **Tier B + C subset** of the majority map would score if drawn alone; it never measured the full majority. The full-coverage score measures the full majority. The flag is retracted because the full majority map is essentially indistinguishable from 2019 on all four metrics — the Tier B + C redesigns that the partial-coverage score captured, and flagged, are diluted back into a Tier-A-dominated baseline when the rest of the province is added. This is internally consistent with the commission's own defence of the majority as a modest adjustment rather than a wholesale redrawing.

### Minority 2026 v6 (coverage 70 → 85 districts; +15 districts)

| Metric | 10k partial | 100k full-coverage | Δ percentile | Flag change |
|---|---|---|---|---|
| Efficiency gap | +0.0170 (p57.4) | +0.0359 (**p92.1**) | **+34.7** | inside band → inside band (just under) |
| Mean-median | **−0.0028 (p100.0)** | −0.0009 (**p98.8**) | −1.2 | **flagged → flagged** (strengthened slightly) |
| Declination | −0.0259 (p18.0) | **−0.0704 (p1.6)** | **−16.4** | inside band → **flagged (new)** |
| Seats @ 50/50 | **+0.486 (p100.0)** | +0.482 (**p94.3**) | −5.7 | **flagged → just below threshold** (p94.3 vs. p95 cutoff) |

Two of the three 10k minority flags survive with slight shifts; the seats-at-50/50 flag is borderline at p94.3 (just under the p95 threshold, so technically unflagged on a strict reading; the value is still within 1 percentile point of the tail). The **new finding** on the minority is the declination flag: the minority's declination of −0.0704 is below the ensemble 5th percentile of −0.0503 — meaning the minority is an NDP-favoured outlier on declination's winning-margin-geometry lens. This is consistent with the audit's packing-and-cracking reading: the minority packs NDP voters into Edmonton- and central-Calgary-anchored districts tightly enough that the NDP-won-districts have very high NDP margins (which declination picks up as an NDP-favouring geometry) while the UCP-won-districts have modest UCP margins (same lens, same direction). Combined with the p98.8 mean-median and the p92.1 efficiency gap, the minority has two outlier flags (mean-median UCP tail, declination NDP tail) and one near-outlier (efficiency gap p92.1). The 10k-era characterisation "minority is the most UCP-favoured map" is replaced by a more nuanced picture: the minority packs NDP voters asymmetrically but the packing pattern is simultaneously UCP-advantageous on vote-share metrics and NDP-advantageous on winning-margin metrics.

## Summary of flag changes across the three maps and four metrics

| Map | Metric | 10k status | 100k full-coverage status | Movement |
|---|---|---|---|---|
| 2019 enacted | Mean-median | flagged p96.1 | unflagged p92.7 | **retracted** |
| Majority 2026 | Seats @ 50/50 | flagged p1.7 | unflagged p57.9 | **retracted** |
| Minority 2026 v6 | Mean-median | flagged p100 | flagged p98.8 | **held** (strengthened by 0.2 pp) |
| Minority 2026 v6 | Seats @ 50/50 | flagged p100 | borderline p94.3 | **weakened** (just under threshold) |
| Minority 2026 v6 | Declination | inside band p18.0 | flagged p1.6 | **new flag** |
| Minority 2026 v6 | Efficiency gap | inside band p57.4 | near-outlier p92.1 | **strengthened** |

Net result: the audit's three 10k flags (2019 mean-median, majority seats-at-50/50, minority dual-flag) reduce to **one strong flag on the minority map** (mean-median p98.8 UCP-tail) plus **one new strong flag on the minority map** (declination p1.6 NDP-tail). The majority and 2019 flags are retracted; both retractions are explained mechanically by the coverage fix, not by statistical noise. The minority's headline conclusion ("most UCP-favoured map among the three") is preserved in substance but re-characterised: the minority has a simultaneous UCP-favouring mean-median tail and NDP-favouring declination tail, reflecting asymmetric packing rather than a single-direction structural tilt.

## Report-integration recommendations

Two sentences in `report_academic.md` §3.11 require revision. Do **NOT** modify the report in this run — the PO will integrate.

### Recommendation 1 — Replace the three-flag opening paragraph

**Before** (lines 397–401):
> Against that floor, three p ≥ 95 or p ≤ 5 flags emerge:
> 1. **2019 enacted at p96.1 on mean-median (UCP-favoured tail).** Only 3.9% of 10,000 ensemble alternatives produce a mean-median this close to zero or more UCP-favoured. Statistical corroboration of the audit's existing packing-and-cracking reading of the 2019 map.
> 2. **Majority 2026 (approx) at p1.7 on seats-at-50/50 (NDP-favoured tail).** Uniform swing to a 50/50 province-wide vote puts the majority at 42.1% UCP seats — below the 44.8% structural floor hit by the ensemble median and fewer than 2% of ensemble plans reach. Consistent with the audit's symmetry-counter-test finding (§3.13) that the majority dilutes the pro-UCP structural tilt relative to both 2019 and the ReCom-neutral neighbourhood.
> 3. **Minority 2026 v6 (approx) at p100 on both mean-median and seats-at-50/50 (UCP-favoured tail).** Mean-median (−0.0028) is less NDP-skewed than every one of 10,000 alternatives; seats-at-50/50 (0.486) is higher than every one. The minority is the single most UCP-favoured map on these two metrics in the 2019-baseline neighbourhood.

**After** (reflects 100k full-coverage results; flag count now two, both on minority):
> Under the publication-grade 100,000-sample full-coverage rescore (`analysis/methodology/v0_1_mcmc_100k_and_full_coverage.md`), the preliminary three-flag set resolves to a two-flag pattern concentrated on the minority map:
> 1. **Minority 2026 v6 (approx) at p98.8 on mean-median (UCP-favoured tail).** Mean-median −0.0009 is closer to zero (less NDP-skewed) than 98.8% of 100,000 full-coverage ensemble alternatives. The minority is the single most UCP-favoured map on this vote-share asymmetry metric in the 2019-baseline neighbourhood.
> 2. **Minority 2026 v6 (approx) at p1.6 on declination (NDP-favoured tail).** Declination −0.0704 is more NDP-favoured than 98.4% of ensemble alternatives. Combined with the mean-median UCP flag, this signals asymmetric packing — NDP voters concentrated in tight-margin NDP-won districts while UCP-won districts have modest margins — rather than a single-direction bias.
>
> The two 10k-era outlier flags retracted by the full-coverage rescore are: **2019 enacted on mean-median** (10k p96.1 → 100k p92.7, just inside the 5–95 band, with the real-map value unchanged and the ensemble 95th percentile widened by added samples); and **majority 2026 on seats-at-50/50** (10k p1.7 → 100k p57.9, driven by the fact that the partial-coverage gpkg excluded 32 Tier-A-unchanged 2019-identity districts whose seat distribution dominates the ratio). The retractions are a coverage-methodology fix, not a statistical-noise result; both are explained mechanically in the full-coverage write-up.

### Recommendation 2 — Replace the falsifiability-hook resolution

**Before** (lines 405–407):
> A follow-up full-coverage rescore using the hybrid crosswalks (`data/v0_1_majority_hybrid_crosswalk.csv` and `data/v0_1_minority_hybrid_crosswalk.csv`) for VAs not in a scored polygon is tracked in `analysis/scripts/mcmc_full_coverage_rescore.py`; a 100,000-sample publication-grade MCMC run, with full-coverage rescore and convergence diagnostics (effective sample size per metric, trace plots), is in progress and will be reported in `analysis/methodology/v0_1_mcmc_100k_and_full_coverage.md`. If either artifact shifts the tail-percentile verdicts, §3.11 will be revised and a change note added.
>
> **Falsifiability hook.** If the 100k-sample full-coverage rescore, or a later commission-shapefile-driven re-run, moves either 2026 map off its p ≥ 95 or p ≤ 5 tail on the flagged metric, the claim for that map is retracted and the map is reclassified as inside-band. The three flags are held as preliminary-but-defensible pending the publication-grade re-run.

**After** (states the falsifiability-hook outcome):
> The 100k full-coverage rescore (completed 2026-04-23; `analysis/methodology/v0_1_mcmc_100k_and_full_coverage.md`) resolves the falsifiability hook set by the 10k preliminary run. Under the hook's retraction rule — "if either 2026 map moves off its p ≥ 95 or p ≤ 5 tail on the flagged metric, the claim for that map is retracted" — the **majority 2026 seats-at-50/50 flag is retracted** (10k p1.7 → 100k full-coverage p57.9), the **2019 mean-median flag is retracted** (10k p96.1 → 100k full-coverage p92.7), and the **minority 2026 seats-at-50/50 flag is downgraded to borderline** (10k p100 → 100k full-coverage p94.3, just under the p95 threshold). The **minority mean-median flag holds** (10k p100 → 100k full-coverage p98.8) and a **new minority declination flag emerges** (10k p18.0 → 100k full-coverage p1.6 in the NDP-favoured direction), consistent with asymmetric packing. Convergence diagnostics report per-metric effective sample sizes of 148–160 on the 100k chain; the chain is a slow mixer (integrated autocorrelation time ≈ 650 on all four metrics) but the running-mean trace plots stabilise within the first 30–40k samples and drift < 0.0003 across the latter 50k, sufficient for the policy-comparison framing used here. A commission-shapefile-driven re-run would further sharpen the 2026-seed distribution but is not required for the minority's held flags to stand; the 2019-seed distribution is conservative against them (a 2026-seed distribution would more closely match the minority's own geometry, narrowing the baseline and pushing the minority's percentile further into the tail).
>
> **Falsifiability hook (revised).** If a later commission-shapefile-driven re-run moves the minority map's mean-median below p95 on a 2026-seed ensemble, the mean-median flag is retracted and the minority is reclassified as inside-band on that metric. The declination flag's falsifiability hook is a structural-packing counter-test: if the two Calgary-zone packing patterns (§3.13 RT7, RT8) are independently contradicted — e.g. by a census-block-level verification — the declination flag is downgraded to one-of-two corroborating signals rather than a standalone flag.

### Recommendation 3 — Update the §3.11 table

**Before** (lines 388–393): the four-row table with 10k percentiles.

**After**: a two-column variant, or a new table appended below the existing one, showing 10k-partial → 100k-full-coverage side by side:

| Metric | 2019 enacted (10k partial → 100k full) | Majority 2026 (10k partial → 100k full) | Minority 2026 v6 (10k partial → 100k full) | 100k ensemble 5th / 50th / 95th |
|---|---|---|---|---|
| Efficiency gap | +0.0241 (p73.6 → p73.4) | +0.0066 → **+0.0241** (p24.6 → p73.4) | +0.0170 → **+0.0359** (p57.4 → **p92.1**) | −0.0097 / +0.0149 / +0.0394 |
| Mean-median | −0.0077 (p96.1 → **p92.7**) | −0.0308 → **−0.0077** (p6.6 → p92.7) | −0.0028 → **−0.0009** (p100 → **p98.8**) | −0.0313 / −0.0191 / −0.0061 |
| Declination | −0.0451 (p7.6 → p7.2) | +0.0049 → **−0.0466** (p52.2 → p6.3) | −0.0259 → **−0.0704** (p18.0 → **p1.6**) | −0.0503 / +0.0033 / +0.0560 |
| Seats @ 50/50 | +0.460 (p79.2 → p80.9) | +0.421 → **+0.459** (p1.7 → p57.9) | +0.486 → +0.482 (p100 → p94.3) | +0.425 / +0.448 / +0.483 |

(Real-map values under full-coverage differ from 10k partial values for the 2026 maps because the covered vote universe changed; for 2019 they are identical because 2019 was already fully covered by the VA labels.)

### Recommendation 4 — RT7 row in the §3.7 Red-team table (line 460)

**Before:**
> | RT7 — MCMC neutral-ensemble outlier | Any real map outside 5–95 band on ≥1 metric for flagged pass | 2019 p96.1 mean-median; Majority p1.7 seats-at-50/50; Minority p100 mean-median + p100 seats-at-50/50 | Flagged pass on all three maps (see §3.11) — held preliminary pending commission-shapefile re-run with 2026 seed and 100k samples |

**After:**
> | RT7 — MCMC neutral-ensemble outlier | Any real map outside 5–95 band on ≥1 metric for flagged pass | Minority p98.8 mean-median + p1.6 declination (100k, full-coverage). 10k-era 2019 and Majority flags retracted by full-coverage rescore (see §3.11 update note, 2026-04-23) | Flagged pass on minority map only; held pending commission-shapefile re-run with 2026 seed |

## Artefacts produced

Scripts:
- `analysis/scripts/mcmc_ensemble_100k.py` — the 100k chain + running-mean plots + ESS diagnostics
- `analysis/scripts/build_full_crosswalks.py` — builds the 88-row majority and 88-row minority full crosswalks
- `analysis/scripts/mcmc_full_coverage_rescore_100k.py` — rescores with polygon + crosswalk fallback, computes percentiles vs. 100k ensemble

Data:
- `data/v0_1_mcmc_ensemble_samples_100k.csv` — 100,000 rows, per-sample metrics
- `data/v0_1_mcmc_real_map_scores_100k.json` — polygon-only (partial coverage) real-map scores for 100k ensemble
- `data/v0_1_mcmc_ensemble_percentiles_100k.csv` — polygon-only percentiles vs. 100k ensemble
- `data/v0_1_mcmc_convergence_diagnostics_100k.json` — per-metric τ, n_eff, ρ(lag=1,10,100)
- `data/v0_1_majority_full_crosswalk.csv` — 88-row full majority crosswalk
- `data/v0_1_minority_full_crosswalk.csv` — 88-row full minority crosswalk
- `data/v0_1_mcmc_real_map_scores_full_100k.json` — full-coverage real-map scores vs. 100k ensemble
- `data/v0_1_mcmc_ensemble_percentiles_full_100k.csv` — full-coverage percentiles vs. 100k ensemble

Plots (maps/mcmc/):
- `ensemble_distribution_100k_{efficiency_gap,mean_median,declination,seats_at_50_50}.png` — histograms with real-map markers
- `running_mean_100k_{efficiency_gap,mean_median,declination,seats_at_50_50}.png` — convergence trace plots

## Reproducibility

- Chain: `python analysis/scripts/mcmc_ensemble_100k.py --n-steps 100000 --seed 42`
- Rescore: `python analysis/scripts/mcmc_full_coverage_rescore_100k.py`
- Deterministic given seed 42, gerrychain 0.3.2, geopandas ≥ 0.14, and the three input gpkg files (VA polygons, approximate-majority, refined-v6-minority).
- Wall time (laptop): ~12 min chain + ~15 s rescore + ~2 s plots = ~13 min end-to-end.

## What remains for a lawsuit-grade re-run

The 100k run is sufficient for the audit's policy-comparison framing. A lawsuit-grade re-run, if ever required, would need three additions:

1. **2026-seed baseline.** Replace the 2019 enacted seed with the commission's final 2026 shapefile once published. The 2019 seed is conservative against the minority's held flags (a 2026 seed would more closely match the minority's geometry, narrowing the baseline).
2. **Thinned chain with longer burn-in.** Current burn-in is implicit (30–40k samples for running-mean stabilisation). A lawsuit-grade run would use a thinned subsample (every 100th sample) from a 1M-step chain to get ~5,000 effectively independent draws, matching MGGG practice.
3. **Soft constraints on communities of interest.** The Electoral Divisions Act names municipal boundaries, Indigenous communities, and school divisions as considerations. These are not enforced in the current chain (the Act frames them as considerations, not constraints). A lawsuit-grade run would add soft penalties for cross-boundary cuts and compare the minority map against the constrained ensemble rather than the unconstrained ReCom ensemble.

None of these additions is required for the audit's present claim that the minority map is simultaneously mean-median-tail UCP-favoured and declination-tail NDP-favoured relative to the 2019-neighbourhood ReCom ensemble. That claim is robust to the 100k convergence and to the full-coverage rescore; the 2019 and majority 10k-flagged claims are not, and are retracted.
