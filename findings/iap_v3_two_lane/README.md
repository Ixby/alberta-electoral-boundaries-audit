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

Logs: `partisan.log`, `structural_verdict.log`, `qsgy8.log`.

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
