---
name: Lunty scorecard dry-run report — Phase A (synthetic neutral 91)
description: "Result of running analysis/scripts/november_red_alert_scorecard.py against a synthetic neutral 91-district plan (produced by generate_synthetic_91.py with labeled seed 'DRY_RUN_SYNTHETIC'). Six production bugs surfaced and were fixed; on the synthetic input MO #1 and MO #3 fired (correct behavior on a random partition) and MO #2 cleared; MO #4 was deliberately deferred for a separate ensemble run."
type: project
---

> **Backward:**
> - `proposals/lunty_dry_run/README.md` — dry-run framing and convention
> - `proposals/lunty_dry_run/generate_synthetic_91.py` — synthetic generator (deterministic from labeled seed)
> - `analysis/scripts/november_red_alert_scorecard.py` — the script under test
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — canonical VA substrate
> - `data/shapefiles/reference/alberta_2021_csds.gpkg` — canonical CSDs (required by MO #1 + MO #3)
>
> **Forward:**
> - `analysis/scripts/november_red_alert_scorecard.py` — bug fixes from this dry-run committed alongside this file
> - `proposals/lunty_dry_run/november_red_alert_SyntheticNeutral91_2026-05-23.md` — scorecard output against the synthetic input (kept for trail-of-work)
> - (leaf otherwise — synthetic outputs are not consumed by any live analysis)

# Lunty scorecard dry-run — Phase A report

**Date run:** 2026-05-23
**Input:** `proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg` (regenerated from `generate_synthetic_91.py` with labeled seed `DRY_RUN_SYNTHETIC` → int 1048440556)
**Scorecard:** `analysis/scripts/november_red_alert_scorecard.py`
**Flags:** `--name-col EDName2025 --out-dir proposals/lunty_dry_run --skip-mcmc`
**Outcome:** 6 production bugs surfaced and fixed; scorecard now runs end-to-end on a 91-district input.

## Synthetic input summary

A 91-district recursive-tree partition of the canonical VA adjacency graph (4,765 nodes / 13,385 edges; same graph the canonical ReCom 1M ensemble runs on). Population balance was ±48.7% envelope — looser than the EBCA ±25% standard, an acknowledged limitation of `recursive_tree_part` without subsequent ReCom iteration. For the Phase A goal (test scorecard plumbing on a 91-district input), this is acceptable; for any future Phase B realistic-plausible input, an EBCA-compliant balanced partition would be required.

The input is **synthetic test data, not a prediction of the Lunty committee's output.** It is excluded from git tracking by `.gitignore` (regenerated deterministically by `generate_synthetic_91.py`).

## Bugs surfaced and fixed

### Bug #1 — `args.shapefile.relative_to(ROOT)` crashes on relative paths

**Severity:** Medium (live Nov 2 run would crash if the user passes a relative path; common mistake)

**Symptom:**
```
ValueError: 'proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg' is not in the subpath of '/home/user/alberta-electoral-boundaries-audit' OR one path is relative and the other is absolute.
```

**Cause:** `args.shapefile.relative_to(ROOT)` at line 437 of the scorecard requires the shapefile argparse path to already be absolute. argparse stores whatever the user typed; if relative, `relative_to(ROOT)` fails.

**Fix:** Resolve to absolute first, then attempt `relative_to(ROOT)`; fall back to the absolute path string if the shapefile lives outside the repo root.

```python
shapefile_abs = args.shapefile.resolve()
try:
    shapefile_display = str(shapefile_abs.relative_to(ROOT))
except ValueError:
    shapefile_display = str(shapefile_abs)
```

### Bug #2 — Output hardcoded to `findings/` directory (no `--out-dir` flag)

**Severity:** Medium (synthetic-test outputs would pollute `findings/`, the live audit directory; reviewers could mistake them for live findings)

**Symptom:** Scorecard wrote to `findings/november_red_alert_SyntheticNeutral91_2026-05-23.md` even though the input was clearly a synthetic test artifact in `proposals/lunty_dry_run/`.

**Cause:** Output path was hardcoded as `_get_findings_dir() / f"november_red_alert_{args.map_name}_{today}.md"`. No CLI flag to redirect.

**Fix:** Added `--out-dir` CLI flag. Default behavior (no flag) still writes to `findings/` so the live Nov 2 run is unaffected. Dry-runs pass `--out-dir proposals/lunty_dry_run`.

### Bug #3 — MO #1 (Drain Pattern) silently skipped when CSD reference is missing

**Severity:** **CRITICAL** — would silently SKIP a tripwire on the live Nov 2 run unless the CSD reference is materialised on disk before the run begins.

**Symptom:**
```
SKIPPED — Alberta CSD polygon file missing at data/shapefiles/reference/alberta_csds.gpkg.
```

**Cause:** `ALBERTA_CSDS` constant pointed at `data/shapefiles/reference/alberta_csds.gpkg`, but the actual file in the repo is `data/shapefiles/reference/alberta_2021_csds.gpkg` (with the year). On any system where the file doesn't exist at the wrong path, MO #1 silently skips with a warning message in the output.

**Fix:** Corrected the path constant to `alberta_2021_csds.gpkg`.

**Note on operational risk:** The CSD reference file is LFS-tracked. On Nov 2, when the live run begins, the operator must verify the LFS pull completed before invoking the scorecard. Recommend adding a pre-flight check to the scorecard that errors out (rather than skipping MOs) if a required reference file is missing.

### Bug #4 — MO #3 (Municipal de-anchoring) silently skipped — same root cause as #3

**Severity:** **CRITICAL** — same risk profile as Bug #3.

**Cause:** Same path mismatch; MO #3 ran the same `if not ALBERTA_CSDS.exists(): skip` guard.

**Fix:** Same fix as Bug #3 (single one-line change resolves both).

### Bug #5 — MO #2 (Lasso compactness) silently degraded to "partial" — same root cause as #3 and #4

**Severity:** Medium (still computes a partial score, doesn't crash, but the VA-CSD urban-share component is dropped silently)

**Cause:** Same path mismatch.

**Fix:** Same fix.

### Bug #6 — `VA_VOTES_PATH` points at DPG-era VA file (LFS-tracked, not materialised on canonical builds)

**Severity:** High (MO #2 crashes when the DPG-era derived VA gpkg isn't pulled; on a clean canonical-only clone the scorecard fails entirely on MO #2)

**Symptom:**
```
pyogrio.errors.DataSourceError: 'data/shapefiles/derived/va_polygons_with_2023_votes.gpkg' not recognized as being in a supported file format.
```

**Cause:** Stale DPG-era reference. `VA_VOTES_PATH` was set to `data/shapefiles/derived/va_polygons_with_2023_votes.gpkg`, which is the DPG-era VA polygon set. The canonical VA polygon set is at `data/shapefiles/canonical/va_2023_election_day_votes.gpkg`. The path was never updated when the canonical infrastructure was added.

**Fix:** Updated `VA_VOTES_PATH` to `data/shapefiles/canonical/va_2023_election_day_votes.gpkg`. The schemas of the two files are similar but the canonical version is the authoritative substrate going forward.

### Bug #7 — `RECOM_SAMPLES` points at deleted DPG-era 250k ensemble (MO #4 silently skips)

**Severity:** **CRITICAL** — surfaces only when MO #4 actually runs (i.e., when the operator passes `--map-s50` or removes `--skip-mcmc`). Equivalent to Bugs #3/#4 but for the partisan-bias channel rather than the structural channel.

**Symptom:** With `--map-s50 X` passed and the old `RECOM_SAMPLES` path:
```
MO #4 — Sampler divergence: SKIPPED — pre-existing ensemble outputs missing.
```

**Cause:** `RECOM_SAMPLES` constant pointed at `data/simulated_ensemble_raw_samples_250k.csv` — the DPG-era 250k ensemble — which doesn't exist in the canonical repo at all. The canonical 1,010,000-plan ReCom samples live at `data/outputs/simulated_ensemble_raw_samples_canonical.csv` (LFS-tracked, ~170 MB).

**Fix:** Updated `RECOM_SAMPLES` to the canonical 1.01M file. The fix is consistent with Stage 11 of the methods paper's case-study arc: the 1.01M canonical ensemble (4 chains × 252,500 steps, seed 1432864451) is the authoritative ensemble for every partisan-metric percentile placement.

**Caught by:** The MO #4 dry-run added 2026-05-23 (this report's later section).

### Pre-flight check (Bugs #3/#4/#5/#6/#7 hardening)

Added 2026-05-23. The scorecard now performs explicit existence + LFS-pointer-vs-binary checks on every required reference path (`args.shapefile`, `ALBERTA_CSDS`, `VA_VOTES_PATH`) at the top of `main()` and aborts with a clear `git lfs pull` instruction if any check fails. Equivalent guards on `RECOM_SAMPLES` and `SMC_OUTPUT` are not yet in pre-flight because MO #4 already self-skips with a visible "SKIPPED — pre-existing ensemble outputs missing" message; consider adding them in a follow-up so the failure modes are uniform.

Verified three ways:
- **LFS pointers in place (no binaries):** pre-flight catches both `ALBERTA_CSDS` and `VA_VOTES_PATH`, lists both with `git lfs pull` remediation, exits 2.
- **Binaries materialised:** pre-flight passes; MO #1/#2/#3 run; output written as expected.
- **Missing input shapefile:** pre-flight catches the missing input, exits 2.

## Scorecard results on the synthetic neutral plan

Three of four MOs computed; MO #4 (sampler divergence) was deliberately skipped (`--skip-mcmc`) because it requires a ReCom + SMC ensemble run against the synthetic plan. That's a separate dry-run task (estimated 1–2 hours of compute) and would be the next step if MO #4 plumbing also needs to be verified before Nov 2.

| MO | Status | Result on synthetic neutral plan | Interpretation |
|---|---|---|---|
| MO #1 — Drain Pattern (city cracking) | 🔴 FIRED | 2 cities flagged: Lethbridge (3 districts, ratio 1.5×), St. Albert (3 districts, ratio 1.5×) | Correct behavior: a random partition that doesn't respect city boundaries will over-split mid-sized cities. Fires as designed. |
| MO #2 — Lasso (surgical non-compactness) | ⚪ clean | No districts hit both bottom-decile PP (threshold 0.149) AND mixed urban-rural composition | Correct behavior: random partitions tend to be moderately compact and either fully urban or fully rural, rarely both at once. Doesn't fire as designed. |
| MO #3 — Municipal de-anchoring | 🔴 FIRED | Municipal anchoring = 19.0% (Canadian norm threshold 70%) | Correct behavior: a random partition doesn't follow municipal edges. Fires as designed; this is the expected null-baseline anchoring for a random tree-partition. |
| MO #4 — Sampler divergence | ⚪ clean | map s50 = 0.4505 → ReCom percentile 51.6 (of canonical 1.01M ensemble); SMC percentile 55.6 (of canonical 5,000-plan weighted ensemble); divergence −4.0 pp; threshold 25 pp | Correct behavior: a random partition converges to the ensemble median, so the two samplers agree (small divergence). MO #4 fires only when ReCom and SMC fundamentally disagree on where the map sits — the signature of deliberate non-compactness exploitation. Plumbing fully verified 2026-05-23. |

**Important reading frame.** 2 of 3 tripwires firing on a synthetic *random* plan is not a "false positive" — it is exactly what the audit's framework predicts. The pre-registered thresholds are calibrated to flag departure from *committee practice* (which respects communities-of-interest and municipal boundaries), not departure from a random null. A random partition will routinely cross MO #1 and MO #3 thresholds because it doesn't respect any of the discipline a real committee imposes.

This is informative for the live Nov 2 run: if the Lunty committee's map fires MO #1 and MO #3, that does **not** automatically mean the map is a gerrymander — it means the map departs from typical Canadian committee practice in the same way a random partition would. The substantive interpretation requires looking at *which* cities/regions trigger which MO, the magnitude of departure, and (when MO #4 runs) where the map sits in the canonical ReCom + SMC ensembles. The scorecard is a tripwire, not a verdict.

## Phase B — Realistic-plausible 91-district input (2026-05-23)

Started from the canonical Elections Alberta majority recommendation (89 EDs) and added two plausible committee-style splits — Calgary-McKenzie and Edmonton-McClung, the two largest EDs by population in canonical majority. Each split bisects the contained VAs perpendicular to the ED's longer axis ("preempt 2031-cycle overflow" rationale — defensible-but-arbitrary, not a Lunty prediction). Generator: `proposals/lunty_dry_run/generate_realistic_91.py` (deterministic).

**Phase B scorecard result:**

| MO | Phase B (canonical maj + 2 splits) | Note |
|---|---|---|
| MO #1 — Drain Pattern | 🔴 FIRED: Lethbridge **4 districts (2.0× ratio)** | This fires on **canonical majority itself** — see Finding #1 below |
| MO #2 — Lasso compactness | ⚪ clean (PP p10 = 0.263) | PP threshold is real-map-like, not random-like |
| MO #3 — Municipal de-anchoring | 🔴 FIRED: **36.0%** (Canadian norm threshold 70%) | **Disagrees with `score_anchoring.py`'s 80.0% on the same input** — see Bug #8 below |
| MO #4 — Sampler divergence | ⚪ clean: ReCom p77.8 vs SMC p95.2, divergence −17.4pp | Larger than Phase A's −4.0 pp but still under the 25pp threshold |

### Finding #1 (substantive) — the canonical majority itself trips MO #1 and MO #3

Ran the scorecard against the **unmodified canonical majority gpkg** (89 EDs, no committee-style splits) as a sanity baseline. Result: identical to Phase B on MO #1, MO #3, and MO #4. The 2 splits added in Phase B do not materially change any MO output.

This means: **the canonical majority recommendation itself tripwires the scorecard on MO #1 (Lethbridge over-split, 2.0× ratio) and MO #3 (36.1% anchoring by MO #3's measure)**. The audit's own commission-majority baseline fires 2 of 4 channels.

The honest interpretation: the scorecard's thresholds are calibrated to flag departure from *committee best practice*, and the canonical majority itself contains a debatable design choice on Lethbridge (4 districts for a city of 98,406 vs population-justified 2). When the Lunty committee's 91-seat map is scored on Nov 2, MO #1 + MO #3 are likely to fire regardless of whether the committee has produced a gerrymander, because the canonical majority baseline already fires them. **The scorecard should be read as a differential measurement against canonical majority, not as an absolute pass/fail.** This needs to be disclosed in the methods paper §6 + the live-Nov-2 prose framing.

### Bug #8 — MO #3 anchoring methodology disagrees with `score_anchoring.py` by ~2×

**Severity:** **CRITICAL** for the live Nov 2 run — false-positive risk on every input.

**Symptom:** Scorecard against unmodified canonical majority gpkg reports MO #3 anchoring at **36.1%**. The audit's headline anchoring number for the same input (per `analysis/scripts/score_anchoring.py`, `findings/redist_python_comparison.md`, `README.md`) is **80.0%**. These cannot both be right.

**Cause (probable):** The two scripts use different anchoring methodologies:
- `score_anchoring.py` (headline): tier-ordered snap to CSD edges with `SNAP_TOL_M=500.0`, vertex density 50m, contiguous ≥1km segments counted as anchored. Returns ~80% for canonical majority, ~72% for canonical minority. This is the methodology the audit publishes.
- MO #3 inside the scorecard: a different implementation in `mo3_municipal_anchoring()` that produces 36% on the same input. The implementation appears to use a simpler "fraction of perimeter within X meters of any CSD edge" measure with different parameters or a different denominator.

**Impact:** The MO #3 threshold (70%, the Canadian comparator norm) was calibrated against the *headline* anchoring methodology (which gives 70-85% on Canadian commission maps), but the MO #3 *measurement* gives a number that's ~half that on the same input. So MO #3 will fire on essentially every commission map, including the audit's own majority recommendation. This is a calibration/measurement mismatch, not just a different number.

**Fix candidates (ordered by safety):**
1. Replace MO #3's implementation with a call into `score_anchoring.py`'s methodology so the measurement and the threshold use the same units.
2. Re-calibrate the MO #3 threshold to match the existing MO #3 measurement (i.e., what is the 70-85% norm under *MO #3's* methodology, on Canadian comparator maps?).
3. Disclose the methodology mismatch in the live-Nov-2 output and report both numbers.

**Recommended:** option 1 (unify methodologies). The headline `score_anchoring.py` methodology is the one with documented provenance, threshold calibration, and external validation; MO #3 should match it, not invent a second methodology.

### Finding #2 — MO #4 divergence on canonical majority is non-trivial

Canonical majority's `seats@50/50 = 0.4607` sits at ReCom p77.8 (1.01M ensemble) and SMC p95.2 (5,000-plan importance-weighted). Divergence of **−17.4pp**. Under the pre-registered 25pp MO #4 threshold this does not fire, but it's the largest divergence we've seen on any non-pathological input. It's worth being aware that the canonical majority is sampler-asymmetric — ReCom places it near median-tail; SMC places it firmly in the upper tail. For Lunty: if the committee map sits anywhere near the canonical majority's position, MO #4 will be close to threshold.

## What this dry-run did not cover

- **EBCA ±25% population balance.** The Phase A neutral synthetic plan has 48.7% envelope; the Phase B realistic synthetic plan inherits canonical majority's tight balance for 87 EDs and a rough half/half split for the 2 new sub-EDs. A real Lunty map would be tighter; whether the scorecard handles tighter or looser inputs differently is not yet tested.
- **Names with special characters.** The synthetic districts use ASCII-safe names. The Lunty committee might use names with diacritics or special punctuation. Not exercised here.
- **CSD layer year sensitivity.** MO #1 and MO #3 use `alberta_2021_csds.gpkg`. If StatsCan updates the CSD layer to 2026 reference before Nov 2, the scorecard will need to be re-checked against the new file.

## Recommendation

Eight production bugs surfaced and seven fixed. **Bug #8 is critical and not yet fixed.** Status before the live Nov 2 run:

1. **Pre-flight check — DONE 2026-05-23.**
2. **MO #4 dry-run — DONE 2026-05-23.** Surfaced Bug #7 (stale DPG ensemble path), fixed. Canonical 87-district ensembles score 91-district inputs directly; no fresh ensemble needed.
3. **Phase B (realistic-plausible synthetic) — DONE 2026-05-23.** Surfaced Bug #8 (MO #3 anchoring methodology mismatch) and Finding #1 (canonical majority itself tripwires MO #1 + MO #3). Plumbing verified; thresholds need re-thinking.
4. **Bug #8 — MO #3 anchoring methodology mismatch (HIGH priority, NOT YET FIXED).** The scorecard's MO #3 implementation gives 36.1% anchoring on canonical majority where `score_anchoring.py` gives 80.0%. Either MO #3 should call into `score_anchoring.py` (recommended) or its 70% threshold must be re-calibrated against MO #3's own measurement. **Fix before Nov 2 or the live scorecard will produce a false-positive on virtually every input.**
5. **Methods paper §6 / live-Nov-2 prose disclosure (MEDIUM priority).** Disclose that MO #1 + MO #3 fire on the canonical majority recommendation itself (Finding #1). The scorecard is a *differential* signal between Lunty's map and canonical majority, not an absolute pass/fail. Without this disclosure, a reviewer who runs the scorecard on canonical majority will catch the audit in an apparent inconsistency.
6. **Follow-up hardening (LOW priority).** Extend the pre-flight check to also cover `RECOM_SAMPLES` and `SMC_OUTPUT`. Currently MO #4 self-skips with a visible message; not silent but not as loud as pre-flight exit-2.

**Live Nov 2 run is blocked by item 4 (Bug #8 fix).** Items 5 and 6 are quality improvements that don't block the run but should be addressed.
