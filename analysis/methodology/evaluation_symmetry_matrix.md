> **Backward:**
> - `findings/structural_battery_result.json` — minority structural-lane scorecard (5/5)
> - `findings/structural_battery_majority.json` — majority structural-lane scorecard (0/5)
> - `reports/academic/report_academic.md` §5.4.9 — both-map partisan percentile placements
> - `analysis/methodology/fisher_combination_defense.md` §3 (AV3) — why SZAT/Fisher is minority-anchored
>
> **Forward:**
> - `reports/academic/report_academic.md` §4.3.1 (conflict-of-interest disclosure) — symmetric methodology is the stated defense

# Evaluation Symmetry Matrix

**Purpose.** The audit's author carries a disclosed conflict of interest (donation to and volunteer work for the NDP; see report §4.3.1). The stated methodological defense against that conflict is **symmetric evaluation**: every discriminating test is applied to *both* commission proposals — the majority map and the minority map — through the same pipeline, with thresholds pre-committed before scoring. This document records, test by test, whether that symmetry holds, names the disclosed exceptions and why they are directional by construction, and points to the artifacts that demonstrate each claim.

**Verification basis.** Built 2026-06-14 from (a) a coverage scan of all 80 tracked result JSONs under `data/outputs/` and `findings/`; (b) a per-script triage of all 122 tracked scripts under `analysis/scripts/`; (c) a direct run of the structural battery on the majority shapefile (this session). Every figure below was read from the cited source file in this session.

---

## 1. Headline matrix — discriminating tests run on both maps

*(Corrected 2026-07-08: the majority Ch1 cell previously read p = 0.125 — the committed `joint_outlier_score.json` value is 0.097; EG p15 → p15.5 per the percentiles CSV; the Ch3 row previously carried the superseded DPG-era reading "within null / anomalously clean" — the canonical label-shuffle re-run finds all three maps anomalously low, with 2019 enacted the most anomalous at z = −3.52.)*

| Test | Minority | Majority | Both scored | Source |
|---|---|---|---|---|
| Ch1 Mahalanobis joint outlier | p = 1.40×10⁻⁶ | p = 0.097 | Yes | `findings/joint_outlier_score.json`; report §5.4.9 |
| Efficiency gap (ensemble percentile) | p94.4 | p15.5 | Yes | report §5.4.9 |
| Mean–median | p99.98 (UCP-tail) | p0.924 (NDP-tail) | Yes | report §5.4.9; `simulated_ensemble_percentiles_canonical.csv` |
| Declination (Warrington, Amendment-10 sign) | p98.79 (UCP-tail) | p20.4 | Yes | report §5.4.9 |
| Seats @ 50/50 | p99.99 | p77.8 | Yes | report §5.4.9 |
| Drain / neighbour-drain (Ch3) | anomalously low (z = −2.75, p ≤ 0.0002) | anomalously low (z = −3.17, p ≤ 0.0002) | Yes | `findings/drain_label_shuffle_null_canonical.json` |
| CSD / municipal anchoring | 72.0% | 80.0% | Yes | report §5.8.5 |
| Regional swing (canonical) | scored | scored | Yes | `data/outputs/regional_swing_canonical*.json` |
| Packing / cracking B1–B6 | scored | scored | Yes (all three maps) | `data/outputs/district_patterns/packing_cracking_events.json` |
| MAUP / population-weighted attribution | scored | scored | Yes | `maup_population_weighted_ensemble.json` (both CSVs committed) |
| Cross-election (2015/2019/2023) | scored | scored | Yes | `data/outputs/cross_election_per_map.json` |
| Municipal splits | scored | scored | Yes | `data/outputs/municipal_splits.json` |
| Extended partisan metrics | scored | scored | Yes | `extended_partisan_metrics_canonical.json` |
| **Structural battery (S1–S6)** | **5/5 — `replicated`** | **0/5 — `not_replicated`** | **Yes (demonstrated 2026-06-14)** | §2 below |

The strongest internal evidence that this matrix reflects genuine symmetry and not nominal even-handedness: the audit **reports the majority's own outlier honestly**. The majority sits at mean–median p0.924 — in the NDP-cracking tail, outside the p5 floor — and that is recorded in §5.4.9 as a pre-registered positive finding (Row 8), not suppressed.

Of 80 tracked result JSONs, every map-scoring output carries both maps except the structural-battery files (one candidate per file, by design — see §2) and reference-baseline files (e.g. the 2019 enacted map).

---

## 2. Structural battery — demonstrated symmetric (closed 2026-06-14)

The structural battery (the November held-out framework) is a **midpoint classifier**: its thresholds are pre-committed at the majority↔minority midpoint (`november_2026_scoring_spec.md`), and it scores whichever map is supplied as the candidate. Through 2026-06-13 only the minority had been scored-and-committed; the majority's 0/5 was asserted "by construction" but not demonstrated. It is now demonstrated. The majority was run as the candidate (same `--reference`, same pre-committed thresholds) and committed to `findings/structural_battery_majority.json`.

| Signal | Threshold | Minority | flag | Majority | flag |
|---|---|---|---|---|---|
| S1 population MAD | > 3382.5 | 3938.11 | yes | 2826.89 | no |
| S2 municipal split count | > 26.5 | 30 | yes | 23 | no |
| S3 anchoring score | < 0.7601 | 0.7178 | yes | 0.7996 | no |
| S4 Polsby–Popper median | non-discriminating | 0.4366 | no | 0.4366 | no |
| S5 drain score | < 0.0039018 | 0.000591 | yes | 0.007213 | no |
| S6 chair-flag replication | > 2.5 patterns | 6 patterns | yes | 1 pattern | no |
| **Verdict** | ≥ 3 of 5 discriminating | **5 flags — replicated** | | **0 flags — not_replicated** | |

Both scorecards report `structural_lane_unexecuted = 0` — every signal executed on both maps. Honest detail on S6: the majority reproduces one of the six chair-flagged patterns (P6, the St Albert–Sturgeon hybrid, a constraint-forced shared boundary); the minority reproduces all six. S4 is identical on both maps and is excluded from the flag count by design.

---

## 3. Disclosed directional exceptions (not gaps)

Two evaluations are not run symmetrically. Both are directional **by construction**, disclosed, and do not represent selective application.

1. **SZAT / Fisher combination (Ch2).** Minority-anchored because the SZAT null fixes non-swing voting areas to the majority map's assignment, making the majority's SZAT score identically zero by construction (`fisher_combination_defense.md` §3, AV3). A symmetric flip-the-anchor variant is argued mathematically equivalent (~0.0024) but is not run as a primary result. **This exception is now moot:** SZAT does not survive a contiguity-respecting block-permutation null (p ≈ 0.19) and the Fisher combination was retired 2026-06-10. The operative headline is Ch1 alone (scored on both maps; see §1).

2. **Justification / rationale tests.** These interrogate *the minority faction's stated rationales* for its deviations, using the majority's cleaner alternative as the comparator (`analysis/scripts/` justification test loads both `majority_2026_populations.csv` and `minority_2026_populations.csv`). They are directional because the minority is the map that deviated and offered the rationales under test; the majority is the baseline, not a co-subject. This is a property of the question, not an asymmetry of application.

---

## 4. Per-script audit (122 scripts) — no hidden single-map findings

A triage of all 122 tracked scripts found 14 that reference only one map. A per-script review (2026-06-14) classified all 14 as benign — none is a comparative finding withheld from one map:

- **Disabled stubs** (raise `NotImplementedError`, uncited, self-condemned in their docstrings): `federal_boundary_correlation_official.py`, `sub_ed_clustering_official.py`, `cross_commissioner_official.py`, `historical_durability_official.py`, `tier_aware_perturbation_official.py`.
- **Utilities / diagnostics / baselines** (not map-scoring, or applied to both maps via a caller): `va_attribution_population_weighted.py` (run on both maps by `maup_population_weighted_ensemble.py`), `chen_rodden_alberta.py` (province-level mechanism probe; per-map scoring done by `chen_rodden_decomposition.py`, which covers both maps), `core_retention.py`, `marginal_seats_analysis.py`, `submission_search.py`, `mahalanobis_qqplot.py`.
- **By-design single-map probes** (a symmetric counterpart would be meaningless): `november_tripwires.py` (scores whatever candidate map is fed in — aimed at the future Lunty map), `local_perturbation_chain.py` (durability retractor seeded from the minority's own outlier geometry), `targeted_gerrymander_burst.py` (symmetric on procedural *direction* via the UCP/NDP mirror `targeted_gerrymander_burst_ndp.py`, not on map).

**Caution for future maintainers.** The five disabled stubs hardcode minority-only shapefile paths. They are inert today, but if any is revived into a live test it must be given both maps, or it becomes a real synchrony gap.

---

## 5. Reproducibility

```bash
# Re-derive the majority structural scorecard (expected: 0 flags, not_replicated)
python analysis/scripts/run_structural_battery.py \
  --shapefile data/shapefiles/canonical/ea_majority_2026_eds.gpkg \
  --label ea_majority_2026_eds \
  --output findings/structural_battery_majority.json

# Re-derive the minority scorecard (expected: 5 flags, replicated)
python analysis/scripts/run_structural_battery.py \
  --shapefile data/shapefiles/canonical/ea_minority_2026_eds.gpkg \
  --label ea_minority_2026_eds \
  --output findings/structural_minority_recheck.json
```

When the Lunty committee tables its 91-seat map (November 2026), the same battery scores it as a third candidate against the same pre-committed thresholds — the symmetry recorded here extends forward to that test.

*Compiled 2026-06-14.*
