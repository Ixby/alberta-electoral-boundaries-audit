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

## Scorecard results on the synthetic neutral plan

Three of four MOs computed; MO #4 (sampler divergence) was deliberately skipped (`--skip-mcmc`) because it requires a ReCom + SMC ensemble run against the synthetic plan. That's a separate dry-run task (estimated 1–2 hours of compute) and would be the next step if MO #4 plumbing also needs to be verified before Nov 2.

| MO | Status | Result on synthetic neutral plan | Interpretation |
|---|---|---|---|
| MO #1 — Drain Pattern (city cracking) | 🔴 FIRED | 2 cities flagged: Lethbridge (3 districts, ratio 1.5×), St. Albert (3 districts, ratio 1.5×) | Correct behavior: a random partition that doesn't respect city boundaries will over-split mid-sized cities. Fires as designed. |
| MO #2 — Lasso (surgical non-compactness) | ⚪ clean | No districts hit both bottom-decile PP (threshold 0.149) AND mixed urban-rural composition | Correct behavior: random partitions tend to be moderately compact and either fully urban or fully rural, rarely both at once. Doesn't fire as designed. |
| MO #3 — Municipal de-anchoring | 🔴 FIRED | Municipal anchoring = 19.0% (Canadian norm threshold 70%) | Correct behavior: a random partition doesn't follow municipal edges. Fires as designed; this is the expected null-baseline anchoring for a random tree-partition. |
| MO #4 — Sampler divergence | (skipped, `--skip-mcmc`) | — | Plumbing not yet dry-run. |

**Important reading frame.** 2 of 3 tripwires firing on a synthetic *random* plan is not a "false positive" — it is exactly what the audit's framework predicts. The pre-registered thresholds are calibrated to flag departure from *committee practice* (which respects communities-of-interest and municipal boundaries), not departure from a random null. A random partition will routinely cross MO #1 and MO #3 thresholds because it doesn't respect any of the discipline a real committee imposes.

This is informative for the live Nov 2 run: if the Lunty committee's map fires MO #1 and MO #3, that does **not** automatically mean the map is a gerrymander — it means the map departs from typical Canadian committee practice in the same way a random partition would. The substantive interpretation requires looking at *which* cities/regions trigger which MO, the magnitude of departure, and (when MO #4 runs) where the map sits in the canonical ReCom + SMC ensembles. The scorecard is a tripwire, not a verdict.

## What this dry-run did not cover

- **MO #4 (Sampler divergence).** Requires a ReCom ensemble + R `redist` SMC ensemble run against the 91-district synthetic plan. Plumbing not exercised here. Estimated 1–2 hours of compute. Should be done before Nov 2 if there's any uncertainty about whether the existing canonical ensembles (87 districts) can score a 91-district input, or whether a fresh 91-district ensemble must be generated.
- **Realistic-plausible 91-district input (Phase B).** The neutral synthetic plan is not committee-like. A Phase B input that starts from the canonical majority (87 EDs) and adds 4 splits in plausible adjustment locations would test the scorecard against a more committee-like product. Not executed in Phase A.
- **EBCA ±25% population balance.** The synthetic plan has 48.7% envelope. A real committee map would be tighter; whether the scorecard handles tighter or looser inputs differently is not yet tested.
- **Names with special characters.** The synthetic districts are `Synthetic-01` through `Synthetic-91` (ASCII-safe). The Lunty committee might use names with diacritics (e.g., "Bonnyville-Cold Lake-St. Paul") or special punctuation. Not exercised here.

## Recommendation

The scorecard is now production-ready for the live Nov 2 run with respect to the six bugs surfaced. Before the live run:

1. **Pre-flight check (HIGH priority) — DONE 2026-05-23.** Added explicit existence + LFS-pointer-vs-binary checks at the top of `main()` for both `ALBERTA_CSDS` and `VA_VOTES_PATH`. The scorecard now errors out loudly (exit code 2 with a clear `git lfs pull` instruction) instead of silently skipping MOs. Tested three ways:
   - **LFS pointers in place (no binaries):** pre-flight catches both files, reports them as pointer files, exits 2.
   - **Binaries materialised:** pre-flight passes; MO #1/#2/#3 run; output written as expected.
   - **Missing input shapefile:** pre-flight catches the missing input, exits 2.
2. **MO #4 dry-run (MEDIUM priority).** Run the scorecard without `--skip-mcmc` against the synthetic plan, or against the canonical majority/minority maps, to confirm the ensemble-comparison code can handle a 91-district input.
3. **Phase B (LOW priority).** Build the realistic-plausible 91-district input and re-run the scorecard.

Items 2 and 3 are "do before Nov 2" items but none are blocking the live run as long as the operator pulls all LFS files first.
