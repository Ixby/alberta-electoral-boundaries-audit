# Two-lane scorecard on the v3 reconstruction (2026-11-06)

**Unregistered sensitivity, run after Step C was seen.** The registered Step C reading (`../a10_stepc/`) scored the frozen assembled map, `iap_2026_assembled.gpkg`, and it stands. This reruns the same registered commands, unchanged, on `data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg` (SHA-256 `8ea5caf68ac95bffe3d7e8a58635b8888f742b3bf115cf3787da3cc92caca1b7`; how it was built: `../iap_reconstruction_check/README.md`, v3 section). Nothing here is a finding on whether the map is a gerrymander.

v3 moves no voting area's representative point, so every vote-based measure is the same by construction. Only the geometry-based measures can move.

## Commands (Step C run sheet steps 1–3 and the qsgy8 scorer, paths changed only)

```
phase4c_canonical_attribution.py --majority <v3> --output data/outputs/iap_assembled_v3_phase4c.json --map-key iap_2026_assembled_v3
joint_outlier_score_canonical.py --map-key iap_2026_assembled_v3 --real-scores data/outputs/iap_assembled_v3_phase4c.json --output findings/iap_v3_two_lane/joint_outlier.json
run_structural_battery.py --shapefile <v3> --output findings/iap_v3_two_lane/structural.json --label iap_2026_assembled_v3
verdict_synthesis.py --structural findings/iap_v3_two_lane/structural.json --joint findings/iap_v3_two_lane/joint_outlier.json --output findings/iap_v3_two_lane/verdict.json
phase_b_scorecard.py --shapefile <v3> --map-name iap_2026_assembled_v3 --name-col EDName2025 --skip-mcmc --map-s50 0.4835 --out-dir findings/iap_v3_two_lane
```

Logs: `partisan.log`, `structural_verdict.log`, `qsgy8.log`, not in the repository (`.gitignore` excludes `*.log`).

## Results: no flag changes

| Lane | Registered Step C (v1) | v3 |
|---|---|---|
| Structural | 2 of 5: not replicated | 2 of 5: not replicated |
| Partisan bias | 1 of 4: absent | 1 of 4: absent |
| Spec §3 outcome | breaks from the minority-style signature on both lanes | same |

| Check | v1 | v3 | Midpoint | Flag (v1 → v3) |
|---|---|---|---|---|
| S1 population MAD | 3,557 | 3,557 | above 3,382.5 | yes → yes |
| S2 municipal splits | 24 | 24 | above 26.5 | no → no |
| S3 anchoring | 74.06% | 74.29% | below 76.01% | yes → yes |
| S5 drain | 0.00442 | 0.00442 | below 0.00390 | no → no |
| S6 chair-flag patterns | 1 | 1 (same: Calgary-North West-Bearspaw hybrid) | above 2.5 | no → no |
| S4 Polsby-Popper median (not counted) | 0.4366 | 0.4549 | — | — |
| P1 efficiency gap | +1.45%, p45.3 | same | p95 | no |
| P2 mean-median | −2.53 pts, p19.7 | same | p95 | no |
| P3 declination | +0.0035, p52.4 | same | p95 | no |
| P4 seats at 50/50 | 48.35%, p98.8 | same | p95 | yes → yes |
| Joint (reported only) | Mahalanobis 2.45, p = 0.20 | same | | |

qsgy8 tripwires (beside the verdict): 1 of 4 on both. MO #1 fires on Lethbridge (4 districts for 2 justified); MO #2 clean; MO #3 74.3% against 70% (was 74.1%); MO #4 unchanged (vote-based).

## Reading

- **S3 anchoring rises 0.24 points** because v3's lines sit on the panel's drawn lines rather than on page-trace wobble and slivers. It stays 1.7 points below the midpoint, so the flag holds.
- **S4's median Polsby-Popper rises from 0.4366 to 0.4549**, because two districts cross the old median: Cochrane (placed; 0.314 → 0.519, its page-trace wobble and slivers gone) and Calgary-Falconridge-Conrich (copied; 0.431 → 0.456, back to its official value after v1's slivers). The median district moves from Calgary-Currie (copied, at its official value, which is why v1 matched both commission maps' 0.4366) to Medicine Hat-Cypress, and the ranks there are spread out. S4 is not counted, so nothing turns on it.
- **The `verdict.json` template text** ("Lunty map …", `publishable_72h`) is the script's fixed wording and does not apply, as in Step C.

## Against the majority and minority maps

The structural battery was rerun today on both commission maps' official shapefiles (`structural_majority_rerun.json`, `structural_minority_rerun.json`; their logs are not committed); it reproduces S1, S2, S5 and S6 exactly. S3 now reads 79.96% and 71.78% against June's 80.05% and 71.97%, so the like-for-like midpoint is 75.87% against the registered 76.01%; no flag changes. Partisan values are the canonical ensemble's (`data/outputs/simulated_ensemble_percentiles_canonical.csv`). Chart: `two_lane_chart.svg` / `.png`, from `two_lane_chart.py` (a draft; not wired into the report or the viewer).

| Check (flag rule, spec §3) | 2019 enacted | Majority | Panel's map (v3) | Minority |
|---|---|---|---|---|
| S1 population MAD (above 3,382.5) | 3,085 | 2,827 | **3,557** | **3,938** |
| S2 municipal splits (above 26.5) | 19 | 23 | 24 | **30** |
| S3 anchoring (below 76.01%) | **75.09%** | 79.96% | **74.29%** | **71.78%** |
| S5 drain (below 0.0039) | **0.00153** | 0.00721 | 0.00442 | **0.00059** |
| S6 chair-flag patterns (3 or more) | 0 (asks about 2026 patterns) | 0 | 1 (Calgary-North West-Bearspaw) | **5** |
| **Structural lane** | **2 of 5, not replicated** | **0 of 5, not replicated** | **2 of 5, not replicated** | **5 of 5, replicated** |
| P1 efficiency gap (+4.10% or more) | +2.41% | +0.10% | +1.45% | +4.02% |
| P2 mean-median (p95 or more, UCP direction) | p91.8 | p0.99 | p19.7 | **p99.97** |
| P3 declination (p95 or more, or p5 or less) | p91.3 | p21.8 | p52.4 | **p98.8** |
| P4 seats at 50/50 (p95 or more) | p78.5 | p78.5 | **p98.8** | **p99.99** |
| **Partisan lane** | **0 of 4, absent** | **0 of 4, absent** | **1 of 4, absent** | **3 of 4, present** |

Bold = flag. On every structural check the panel's map lies between the two commission maps; on S1 and S3 it is on the minority's side of the midpoint, on S2, S5 and S6 on the majority's. Its one partisan flag, P4, is a 91-district map ranked against 87-district plans (as registered); against 91-district set D it is p91.6.

**The 2019 map** was added at the author's direction (`structural_2019_rerun.json`, same command, on a copy of the shapefile with the 2017 names in `EDName2025`). It lands on 2 of 5 here, against 0 of 5 on the public chart, and on different checks from the panel's: S3 and S5, where the panel's are S1 and S3. Those midpoints were set between the two 2026 maps, so they do not measure 2019 against anything it was drawn to meet. S1 here is on the 2021 overlay (3,085); the public chart's note cites 2,010 from Appendix C, and the two have not been reconciled.

**None of these checks is Recommendation 5.** The panel's departures from it are in `../iap_r5_degree/README.md`.

**Why this is not the public chart's battery.** The public scorecard chart (`article_figures.build_bias_structure_matrix`, "Where the three maps sit on the audit's two lanes") uses Act I's April tests, on which the minority is 4 of 5 because anchoring is counted neutral there. Those tests were set by comparing the two commission maps and have no rule for a third map. §3's midpoint battery was registered for scoring a third map, and on it anchoring discriminates (79.96% against 71.78%), so the minority is 5 of 5.
