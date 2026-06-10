---
title: November 2026 held-out test — pre-registered scoring specification
version: 1.0
date_committed: 2026-06-10
drand_round_target: round at or after first publication of the Lunty committee's final map
status: PRE-COMMITTED — do not amend after the Lunty committee's map is published except via dated, signed amendment log entries
---

# November 2026 held-out test — pre-registered scoring specification

This document freezes — *before* the Special Select Committee on Electoral Boundaries (the "Lunty committee") publishes its final map — the exact procedure by which this audit will score that map. It is the audit's classical prospective pre-registration. Every metric, threshold, substrate choice, and tiebreaker is fixed here. Drand round, scripts, and commit hashes are pinned.

The audit's published headline verdicts (`reports/academic/report_academic.md`, `reports/public/report_public.md`, `docs/FINDINGS_BRIEF.md`) include a public commitment to apply this procedure to the November map and to update the public site within 72 hours of the map's release with the result *regardless of which direction the result falls*. This document is the operational form of that commitment.

## 1. Scope and what this test answers

**Single bright-line question.** Does the Lunty committee's final map exhibit the same structural-lane signature the audit detected on the minority commission proposal — population deviation, municipal split count, anchoring to administrative boundaries, compactness, neighbour-drain pattern, and the chair's anomaly flags — and the same partisan-bias profile against the audit's 1,010,000-plan canonical ReCom ensemble?

**Two outcomes, both publishable.**
1. The Lunty map matches the minority's tail-profile on three or more structural-lane checks AND lands at p95 or higher on at least one partisan-bias metric in the UCP direction → the audit reports a *replication of the minority-style signature*.
2. The Lunty map matches the majority's neutral profile (within central band on every structural check, no partisan tail above p95) → the audit reports a *break from the minority-style signature* and updates the §6.2 verdict accordingly.

**The audit will publish either outcome.** No private re-running, no waiting, no editorial re-framing. The 72-hour public commitment is binding.

## 2. Substrate

| Component | Pre-committed choice |
|---|---|
| Lunty map ingestion | The first Elections Alberta-published shapefile of the Lunty committee's final map (`.gpkg` or `.shp`), pulled at the drand round below. If only PDF/image releases are available within 72 hours, the audit applies the DPG-construction protocol from `analysis/methodology/shape_refinement_v2.md` and re-runs at official-shapefile release within 14 days (sunset clause as in §4.1.4). The DPG-based scoring is reported as *provisional* and explicitly excluded from the headline; the official-shapefile re-run is the headline. |
| 2023 vote data | `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` (election-day only; the same substrate used for canonical real-map scoring of the May 2026 commission proposals). |
| VA-to-ED attribution | `analysis/scripts/phase4c_canonical_attribution.py` `representative_point()` centroid-in-polygon. The chain ensemble and the Lunty map will be scored under the *same* attribution method. |
| Reference ensemble | `data/simulation_checkpoints_canonical/chain[0–3]_samples.csv` (1,010,000 plans, 4 chains × 252,500 steps, base_seed=1432864451). This ensemble is fixed and will not be regenerated for the Lunty test. If the constraint-enforcing ensemble (T1.4 in TODO_REMEDIATION) is available before the Lunty map publishes, the audit reports against *both* ensembles; the constraint-enforcing one is the more conservative reading. |

If any of the above artifacts is unavailable at scoring time, the audit publishes a one-paragraph note documenting which fallback path was used and why, and re-runs against the canonical substrate when it becomes available. No silent fallbacks.

## 3. Metrics and thresholds (pre-committed; do not move on result)

The audit applies the same battery used in `reports/academic/report_academic.md` §4.3 with the thresholds pre-committed in `preregistration/thresholds.md`. The values below are the *Alberta-calibrated* values (not US-imported) per §5.2.8.

### Structural-lane (geometric, no vote model)

| ID | Metric | Threshold | How it's read |
|---|---|---|---|
| S1 | Population MAD (per-ED deviation from ideal) | ≥ 1.5× the majority commission proposal's MAD | flag |
| S2 | Municipal split count | ≥ 1.5× majority's count of municipalities split into 2+ EDs (canonical: 8) | flag |
| S3 | Anchoring score (% population in EDs anchored to single municipality / county) | within 70–85% Canadian norm = neutral; outside the band = flag | flag if outside |
| S4 | Polsby–Popper compactness median | < majority's median by 0.10 or more | flag |
| S5 | Neighbour-drain adjacency pattern score | drain_score > 0.05 AND label-shuffle null p < 0.05 | flag |
| S6 | Chair-flagged boundary count (per Justice Miller's published anomaly notes) | ≥ 1 of the minority's pre-flagged boundary patterns reproduced | flag |

**Structural-lane verdict rule (frozen):** ≥ 3 flags fire = "structural-lane signature replicated"; 0–2 flags = "structural-lane signature not replicated."

### Partisan-bias lane (vote model required)

| ID | Metric | Threshold (Alberta-calibrated) | How it's read |
|---|---|---|---|
| P1 | Efficiency Gap, UCP direction | ≥ +4.10% on 2023 votes | flag |
| P2 | Mean-median gap, UCP direction | ≥ p95 against canonical 1,010,000-plan ensemble | flag |
| P3 | Declination (Warrington 2018, UCP=R convention) | ≤ p5 OR ≥ p95 against canonical ensemble | flag in tail direction |
| P4 | Seats@50/50 (uniform partisan swing), UCP direction | ≥ p95 against canonical ensemble | flag |
| P5 | Joint Mahalanobis distance across P1–P4 | Bonferroni upper bound across the four marginal p-values | report bound only; NOT a flag axis (the joint statistic is dependence-robust framing, not an additional independent test) |

**Partisan-bias verdict rule (frozen):** ≥ 2 of P1–P4 fire in the UCP direction = "partisan-bias signature present"; 0–1 flags = "partisan-bias signature absent or marginal."

### Combined verdict rule (frozen)

| Structural | Partisan | Headline |
|---|---|---|
| Replicated (≥ 3) | Present (≥ 2 in UCP direction) | "Lunty map replicates the minority-style signature on both lanes" |
| Replicated (≥ 3) | Absent (≤ 1) | "Lunty map replicates the structural signature only; partisan-bias lane is neutral" |
| Not replicated (≤ 2) | Present (≥ 2 in UCP direction) | "Lunty map does not replicate the structural signature; partisan-bias signature present" |
| Not replicated | Absent | "Lunty map breaks from the minority-style signature on both lanes" |

The 2×2 is the entire verdict surface. No "partial replication," no "qualitative judgment," no editorial re-weighting after the result is in.

## 4. Substrate-iteration handling

If the substrate-iteration history of the May 2026 canonical run is any guide, the Lunty map's metric values may shift across attribution refinements. The audit pre-commits to:

1. **Publishing the first canonical-attribution reading within 72 hours** with the threshold ratings above.
2. **Re-publishing within 14 days if an attribution refinement** (e.g., a corrected Vote-Anywhere or Phase 4F population validation step) shifts any flagged metric by more than the threshold margin.
3. **Both readings remain visible** in the final report. The audit does not retract the first reading; it amends with a dated correction note.

## 5. What is NOT changed by this test

- The two-lane verdict on the *commission's* majority and minority proposals (§6.2) is not affected by the Lunty map's result. The Lunty map is a separate object.
- The audit's headline framing on the *process* anomaly (the April 16 cabinet pivot) is not affected by this test. The procedural finding stands on its own.
- The dependence-robust Bonferroni upper bound (p ≤ 2.80×10⁻⁶) for the May commission proposals is not affected.

## 6. drand pinning

This document is committed at git hash `[committed]` to be pinned at the next drand round following publication of this document. The drand round and SHA-256 of this file at commit time are recorded in `preregistration/seed_commitments.md` under the entry `november_2026_scoring_spec`.

Any amendment to this document after the Lunty committee publishes its map is **not permitted** except via a dated, signed entry in `findings/pre_registration_amendment_log.md` explaining (a) what was amended, (b) why the amendment does not move a goalpost in response to a seen result, and (c) why an unamended reading is not feasible.

## 7. Reproducibility — the exact command sequence

```bash
# 1. Pull the Lunty map (substitute the EA-published path)
mkdir -p data/shapefiles/lunty
cp /path/to/lunty_2026_eds.gpkg data/shapefiles/lunty/

# 2. Score it against the canonical ensemble
python analysis/scripts/phase4c_canonical_attribution.py \
  --majority data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --output data/outputs/lunty_phase4c_results.json

python analysis/scripts/joint_outlier_score_canonical.py \
  --map-key lunty_2026 \
  --real-scores data/outputs/lunty_phase4c_results.json \
  --output findings/lunty_joint_outlier.json

# 3. Structural lane
python analysis/scripts/run_structural_battery.py \
  --shapefile data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --output findings/lunty_structural.json
# (NB: run_structural_battery.py does NOT exist yet — see TODO_REMEDIATION T5.2; must be
#  written by 2026-10-01 to clear the gate.)

# 4. Verdict synthesis
python analysis/scripts/verdict_synthesis.py \
  --structural findings/lunty_structural.json \
  --joint findings/lunty_joint_outlier.json \
  --output findings/lunty_verdict.json
# (NB: verdict_synthesis.py does NOT exist yet — must be written by 2026-10-01.)

# 5. Update the public site
python analysis/scripts/build_html_reports.py
cd viewer && npm run build
git commit -am "lunty: 72-hour held-out test result — [outcome]"
git push -u origin master
```

**Tracking:** TODO_REMEDIATION.md item T5.1 (this document) is now CLOSED. Items T5.2 (`rural_gap_dissection.py`), T5.3 (OSF refresh), and the script gaps in §7 above remain OPEN and must close by 2026-10-01 — three weeks before the Lunty committee's reporting deadline.

## 8. Why this works as a falsifier

The honest framing: the audit's hypothesis on the May minority proposal is exploratory by §4.3.1. The Lunty test is the *confirmatory* counterpart. If the Lunty committee — drawing under different procedural constraints, with different members, on a different timeline — produces a map that replicates the minority's signature on both lanes, the structural finding earns confirmatory status. If it does not, the audit's verdict on the minority proposal stands as an isolated exploratory observation, not as evidence of a recurring pattern under the diverted process. Either outcome shifts the published verdict; this is what pre-registration is supposed to do.
