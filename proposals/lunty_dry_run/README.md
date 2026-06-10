---
name: Lunty dry-run — synthetic 91-district test inputs for the November scorecard
description: "Synthetic 91-district plans used only to dry-run analysis/scripts/phase_b_scorecard.py before the real Lunty Select Special Committee map drops on 2026-11-02. Nothing in this directory is a prediction of what Lunty will produce. The synthetic plans exist to test the scorecard plumbing and surface 91-district edge cases that would otherwise be discovered during the live 72-hour window."
type: project
---

> **Backward:**
> - `analysis/scripts/phase_b_scorecard.py` — the scorecard being dry-run
> - `analysis/scripts/mcmc_ensemble.py` — provides `build_va_graph()` used by the generator
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — canonical VA substrate (LFS-tracked)
> - `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg` — canonical commission maps used as a starting point for the "realistic-plausible" synthetic plan (Approach B)
> - `preregistration/null_hypotheses.md` — pre-registered scorecard methodology this dry-run exercises
>
> **Forward:**
> - `proposals/lunty_dry_run/dry_run_report.md` — what worked and what bugs surfaced
> - `analysis/scripts/phase_b_scorecard.py` — bug fixes discovered here flow back to the scorecard for the live Nov 2 run
> - (leaf otherwise — synthetic inputs are not consumed by any live analysis; they exist solely for testing the production pipeline)

# Lunty dry-run — synthetic 91-district test inputs

**This directory is not part of the audit.** It is a dry-run sandbox for the November 2026 Lunty Select Special Committee scorecard (`analysis/scripts/phase_b_scorecard.py`).

## Why this exists

The Lunty committee reports by **2026-11-02**. The audit's pre-registered scorecard methodology (OSF [qsgy8](https://osf.io/qsgy8/) / AsPredicted #289,455) is locked. When the real map is released, the operational standard is to score it within **72 hours** (Amendment 2 Bucket C). If the scorecard crashes on a 91-district input — because the canonical infrastructure was developed for 87 districts (2019 enacted) and 89 districts (commission maps) — the 72-hour window is wasted debugging plumbing rather than producing the public scorecard.

This directory's purpose is to **find those bugs now, with synthetic inputs**, so the live Nov 2 run is methodology-only rather than methodology-plus-debugging.

## What is NOT in this directory

- **Predictions about the Lunty committee's output.** The committee draws from scratch with five MLAs and their own deliberation. Nothing the audit produces here is informative about the real outcome, and no synthetic input here is offered as a prediction.
- **Real analytical findings.** The scorecard outputs against synthetic inputs are not audit findings. They are test fixtures. They appear only in `dry_run_report.md` as plumbing-verification evidence.
- **External commitments.** This dry-run is not pre-registered anywhere. It is internal preparation for a pre-registered live test.

## What IS in this directory

| File | Purpose |
|---|---|
| `generate_synthetic_91.py` | Generator script. Builds a 91-district plan from the canonical VA adjacency graph using a ReCom proposal step seeded from a clearly-non-real label ("DRY_RUN_SYNTHETIC"). Output is a GeoPackage with one polygon per synthetic district, named `Synthetic-01` through `Synthetic-91`. |
| `synthetic_neutral_91_test_input.gpkg` | Output of the generator. A 91-district plan that satisfies the audit's standard constraints (±25% population balance, contiguity) but has **no committee-style adjustment** — it's just a random valid plan. Use case: confirms the scorecard handles arbitrary 91-district input. |
| `dry_run_report.md` | What worked, what didn't, what bugs were fixed in `analysis/scripts/phase_b_scorecard.py` as a result. |

## Naming convention

Every synthetic district is named `Synthetic-NN` (zero-padded). Every output file contains the substring `synthetic_*_test_input` in its filename. Every scorecard output produced against a synthetic input is written to `proposals/lunty_dry_run/`, never to `findings/` or `reports/`. This is the firebreak that prevents synthetic test outputs from being mistaken for live audit results.

## Approach (Phase A — neutral synthetic)

1. Build the canonical VA adjacency graph using `build_va_graph()` from `analysis/scripts/mcmc_ensemble.py` (4,765 nodes, 13,385 edges; same graph the canonical ensemble runs on).
2. Use `gerrychain.tree.recursive_tree_part()` with `n_parts=91`, population tolerance ±25%, RNG seed labeled "DRY_RUN_SYNTHETIC" (a verbally-tagged seed; integer derived from the label hash so the run is reproducible).
3. Map VA → district assignment back to the GeoDataFrame; dissolve VAs by district to get district polygons.
4. Write the result as a GeoPackage with columns `EDName2025` (synthetic name) and `geometry`, matching the canonical EA shapefile schema so the scorecard reads it without modification.
5. Run the scorecard against the output.
6. Document every error message, column mismatch, and 89/91 assumption that surfaces in `dry_run_report.md`.

## Phase B (realistic plausible synthetic) — not yet executed

When/if approached, Phase B will start from the canonical majority (87 EDs) and add 4 splits in plausible committee-adjustment locations (e.g., Airdrie + Calgary urban-fringe + Edmonton urban-fringe + one rural seat). The goal is to test the scorecard on a plausibly-realistic 91-district input. **Phase B is not a prediction either** — it tests sensitivity, not prophecy. Filename will be `synthetic_realistic_91_test_input.gpkg`; will not be produced without explicit authorization.

## What this directory does NOT replace

The pre-registered scorecard methodology at OSF qsgy8 / AsPredicted #289,455. Nothing here amends, supplements, or substitutes for that registration. The dry-run is plumbing verification, not methodology.
