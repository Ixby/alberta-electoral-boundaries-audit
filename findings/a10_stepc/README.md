# Step C: the panel's assembled map, scored provisionally

> **Provisional.** Kept out of the headline. The map scored is the Independent Advisory Panel's 91-district map as assembled by the registered Amendment 10 run (`fd82cdd1`), not an official shapefile. Its calibration passed (T1 0 of 1,909; efficiency-gap delta 0.00 points; final mean Hausdorff 0.031 km; mean IoU 0.9993), but that calibration was a reproducibility run on seen data (Amendment 10, Part 2), not out-of-sample evidence of accuracy. The headline remains the enacted map's official shapefiles. Nothing here is a finding on whether the map is a gerrymander: each test places the map among neutral maps, or against the commission maps, on its registered measure.

Run 2026-11-04 (evening, MST) under the run sheet `preregistration/a10_stepc_run_sheet_2026-11-04.md`, committed at `63cbf7d1` before any measure was computed, with changes recorded at `a9c1e3a6` and after (listed under "Deviations" below). Votes: 2023 election-day voting-area votes (the registered substrate). The seat-claim test's rescaled substrate is not used here.

## Results

### Registered specification (spec v1.2, §3): both lanes

| Lane | Result | Rule |
|---|---|---|
| Structural | **2 of 5 flags: not replicated** | 3 or more of 5 = replicated |
| Partisan bias | **1 of 4 flags: absent** | 2 or more of 4 in the UCP direction = present |
| Spec outcome (§3 2×2) | "breaks from the minority-style signature on both lanes" | |

Structural lane (`structural.json`), midpoint rule:

| Check | Panel's map | Midpoint | Flag |
|---|---|---|---|
| S1 population MAD | 3,557 | above 3,382.5 flags | **yes** |
| S2 municipal splits | 24 | above 26.5 flags | no |
| S3 anchoring | 74.1% | below 76.0% flags | **yes** |
| S5 drain | 0.00442 | below 0.00390 flags | no |
| S6 chair-flag patterns | 1 (Calgary-North West-Bearspaw hybrid) | above 2.5 flags | no |
| S4 Polsby-Popper median (not counted) | 0.4366 | — | — |

Partisan lane (`joint_outlier.json`, `verdict.json`), against the 87-district canonical ensemble:

| Measure | Panel's map | UCP-direction percentile | Flag (p95 or more) |
|---|---|---|---|
| P1 efficiency gap | +1.45% | 45.3 | no |
| P2 mean-median | −2.53 pts | 19.7 | no |
| P3 declination | +0.0035 | 52.4 | no |
| P4 seats at 50/50 | 48.35% (44 of 91) | 98.8 | **yes** |
| Joint (reported only) | Mahalanobis 2.45, p = 0.20 | | |

`verdict.json` carries the script's fixed template text ("Lunty map …", `headline_to_publish`, `publishable_72h: true`). None of it applies here: the map is the panel's, the reading is provisional, and it is out of the headline. `structural.json` records `drand_round_at_execution: null`. That field is a provenance stamp the script leaves for a driver to fill; the November round is pinned as 6606642 in `preregistration/seed_commitments.md`, and the structural lane uses no random draw.

P4 is scored against the 87-district ensemble, as registered. Against neutral maps with 91 districts (below) the same 48.35% sits at p91.6 in set D, p95.4 in set B, p96.7 in set A and p90.4 in set C.

### X1, Recommendation 5 (Amendment 5, Part 13): **not met**

`x1.json`. (a) 31 of 41 divisions unchanged; the 10 changed are Calgary-Bow, Calgary-West-Elbow Valley, Canmore-Banff, Cochrane-Springbank, High River-Vulcan-Siksika, Lethbridge-East, Lethbridge-West, Livingstone-Macleod, Okotoks-Diamond Valley and Taber-Cardston. (b) 11 of 11. (c) not scored: the October 2025 interim map is not in the repository. (d) adopted: Rocky Mountain House-Sundre has 61% of its population in the Clearwater County and western Mountain View County zone. Because (a) fails, X1 is not met whatever (c) would show. Of the other 27 majority divisions, 13 return unchanged.

### Size-matched comparison (Amendment 5, Parts 14–18): set D primary

`size_matched.md`, `size_matched.json`. 91-district sets; percentiles as the script prints them; **flag** = at or above the 95th (towns, city gap) or at or below the 5th (competitive seats), per Part 17. "Provisional" in those tables is Part 16's effective-sample-size label, separate from this Step C label.

| Measure | Set D (primary) | Set A | Set B | Set C |
|---|---|---|---|---|
| Towns split beyond their minimum (1: Lethbridge 4 for 2) | p0.0 | p0.0 | p0.0 | p32.1 |
| City versus rest (+4.3%) | p59.2 | p99.5 **flag** | p87.7 | p67.8 |
| Competitive seats within 4 pts (11) | p75.2 | p72.9 | p73.0 | p73.6 |
| Efficiency gap (+1.45%) | p47.9 | p46.4 | p47.5 | p50.5 |
| Mean-median (−2.53 pts) | p17.0 | p18.5 | p19.7 | p25.9 |
| Declination (+0.0035) | p52.4 | p53.6 | p53.9 | p56.8 |
| Seats at 50/50 (48.35%) | p91.6 | p96.7 | p95.4 | p90.4 |
| Population MAD (3,557) | p0.0 (final) | p96.1 (final) | p0.0 (final) | p0.0 |
| UCP seats (58) | p42.7 | p50.7 | p50.6 | p59.5 |

In set D, the primary set, none of the three Part 17 tests flags. Set A's city-versus-rest flag is in the ±12.5% set; the statute's own band (B, D) does not flag it.

### qsgy8 tripwires (beside the verdict; they do not decide it)

`phase_b_scorecard_iap_2026_assembled_2026-11-04.md`: **1 of 4 fired.** MO #1 fired on Lethbridge (4 districts against 2 justified by population, ratio 2.0, threshold 1.5). MO #2 (lasso: no district both in the bottom decile of Polsby-Popper, below 0.268, and mixed urban-rural), MO #3 (the scorecard's anchoring, 74.1%, above 70%; same `score_anchoring.py` method as S3) and MO #4 (sampler divergence −1.2 points, threshold 25) are clean. MO #4 used the cached ReCom and SMC outputs (`--skip-mcmc`) with step 1's seats at 50/50.

### R1 and R2, the territory redraw tests (Amendment 8, via Amendment 10, Part 5)

`territory/rank.json`, `territory/calibration.json`. Scored, because every changed district is placed or filled (Fort McMurray-Wood Buffalo is filled from its neighbours' hole). The null was rerun on the assembled map's own fixed set, as Amendment 8, Part 5 requires: 58 fixed districts (Step A's 56, Calgary-Acadia, and Edmonton-Meadows; see the next paragraph), and one territory of 1,753 voting areas holding 33 districts. s.15(2) cap in the territory: 2. Reference chains 1, 2, 4 and 6 (chain 3 retired, see Deviations), 1,440 plans after burn-in; holdout chain 5, 360 plans.

**Edmonton-Meadows is fixed because of a reconstruction limit.** The panel changed it: App. 7 gives 53,318 people against the majority's 56,880 (−3,562, several voting areas' worth). The assembly did not place its page; it filled Meadows from the hole its placed neighbours (Ellerslie, Nisku, South, Whitemud) left. That hole holds exactly the majority's 29 voting areas, so the rerun rule fixes Meadows. On the panel's true map, Meadows would most likely be in the territory, which would then hold 34 districts. R1 and R2 are internally consistent, because the rule was applied to the map Step C scores. But the fixed set itself depends on this reconstruction error, and that holds for every measure here: whatever moved out of Meadows is placed on the majority's line in this map.

| Test | Panel's map | Null mean | Null 95% | Two-sided p | Flag (p < 0.05) |
|---|---|---|---|---|---|
| **R1** efficiency gap | +1.45% | +1.14% | −0.14% to +2.09% | **0.665** | no |
| **R2** neighbour-drain | 0.00441 | 0.00847 | 0.0022 to 0.0259 | **0.597** | no |
| Mean-median (beside) | −2.53 pts | −0.50 | −2.58 to +0.59 | 0.064 | — |
| Declination (beside) | +0.0035 | +0.0016 | −0.028 to +0.026 | 0.818 | — |
| UCP seats (beside) | 58 | 58.1 | | 1.000 | — |

Neither test flags. Mean-median sits near the edge of the null, on the NDP-favourable side, at p = 0.064, not a flag. Reported only: the registered label-shuffle p for drain is 0.0; on this rerun's neutral holdout plans that null flags 97% of them (Amendment 8, Part 4 found 97.5%), so it carries no information. Rerun diagnostics: split-R̂ 1.000 (EG), 0.999 (drain); holdout false-positive rates 5.3% (EG), 1.4% (drain).

Territory districts outside the null's ±25% band on the 2021 overlay (Amendment 8, Part 5): Rocky Mountain House-Sundre −31.4% (stated −41.3%; an s.15(2) district, which the null allows) and Edmonton-Windermere −27.3% (stated +0.8%; the overlay predates its growth).

### Cut voting-area range (Amendment 10, Part 5; sensitivity, not a gate)

`cut_va_sensitivity_fixed.json`, `cut_vas_fixed.csv`. 245 cut voting areas; 132 have at least 10% of their area on the minority side and were flipped one at a time (87 of them involve a changed district). 29 single flips raise the efficiency gap, 19 lower it, 84 leave it unchanged. Greedy bounds: **+1.32% to +2.94%** around the pipeline's +1.45%. The bounds ignore interactions between flips.

What moves the range is not the reconstruction:
- **The upper bound comes from two voting areas on a line the panel did not change.** Two voting areas in Strathcona-Sherwood Park, on its line with Sherwood Park (polls 012 and 013, OBJECTIDs 3074 and 4352), each add 1.42 points when flipped alone to Sherwood Park. Both districts are unchanged, so both are at the commission's official geometry; the cut is the commission's own line. Those VAs are placed by representative point, the same rule every map in the audit and every neutral plan in the nulls uses. The 45 flips between two unchanged districts give every large delta (largest +1.42 points).
- **Flips that involve a changed district, the only ones reconstruction error can reach,** move the efficiency gap by at most +0.023 and −0.036 points each. Their 18 raising flips sum to +0.045 points.
- **Against the registered lines:** the upper bound (+2.94%) is above R1's null 97.5th percentile (+2.09%), so R1 would flag if those two commission-line VAs were attributed by area instead of by representative point. That would change the attribution rule, not correct a reconstruction error, and the null uses the same rule. Neither bound reaches P1's +4.10% or set D's 95th percentile (+4.08%). This describes the test's sensitivity, not a verdict.

### Voting areas cut (Amendment 9, Part 5; descriptive, on the assembled map)

`va_cuts.csv`, `va_cuts_marked.csv`. Rule: more than 1% and more than 0.01 km² outside the main district.

| Voting areas | Cut | Involve a changed district | Marked uncertain |
|---|---|---|---|
| 2023 (4,765) | 211 | 144 | 1 |
| 2026 (4,904) | 218 | 149 | 1 |

Baselines on the 2026 set: majority map 229, minority map 364. "Uncertain" means the part outside the main district lies within 31 m of it, the calibration's final mean Hausdorff distance. That is a mean, not a worst case, so the mark is narrow.

### Supplementary: EBCA population rules (not a registered test)

`rules_check.json`, `rules_check.csv`. On App. 7's stated populations: none above +25%, none below −50%, three below −25% (s.15(2) allows four): Central Peace-Notley −46.5% (5 of 5 criteria), Lesser Slave Lake −44.1% (3 of 5) and Rocky Mountain House-Sundre −41.3% (5 of 5). Each meets at least three. Two districts are below −25% on the overlay only (Calgary-North East, Edmonton-Windermere); on the stated figures both are near average.

## How the polygon path and the registered assignment differ

Steps that read polygons place voting areas by representative point. That reproduces the registered assignment for 4,764 of 4,765. VA 875 (old Rimbey-Rocky Mountain House-Sundre poll 042; 498 people, 218 votes) goes to Lacombe-Sylvan Lake by representative point and to Rocky Mountain House-Sundre in the registered run. Both are UCP seats. The efficiency gap is the same on both paths (+0.0144505; they differ by 2 × 10⁻¹⁸, rounding: moving votes between two seats won by the same party does not change its total surplus), so no partisan figure depends on it.

## Deviations from the run sheet, and failed attempts

1. **qsgy8 scorer.** The run sheet named `november_tripwires.py`. That is an unregistered city-split check; it failed twice (it requires EPSG:3401, then a `name` column the CSD file lacks) and gave no result. The registered MO #1–#4 scorer, `phase_b_scorecard.py`, was run instead. The change was written into the sheet after the scorecard had run; no other script or flag set was tried.
2. **Chain 3 does not seed** on the 33-district territory (`recursive_tree_part`: no cut after 50,000 attempts; `territory/chain3.log`). It was retired and chain 6 (salt `a8-territory-null-chain6`) took its place, following Amendment 5, Part 14's precedent for set D's index 250. Recorded in the sheet before any plan was scored.
3. **The territory scorer's CLI cannot score a rerun.** At `42b5fda8`, `territory_score.py`'s `plans` and `calibrate` subcommands build the territory without the enacted map, so they fail on the rerun's 1,753-voting-area plans (shape mismatch). Two short wrappers (`territory/score_plans_enacted.py`, `territory/calibrate_enacted.py`) call the pinned module's own `Substrate`, `score_plans` and `calibrate` with the enacted map, as its `rank` subcommand does. No scoring code was changed.
4. **The registered cut-VA script does not score the panel's map.** `findings/a10_dev/cut_va_sensitivity.py` (SHA `c264a49e…`, registered in Amendment 10) builds the calibration composite, the majority map with only the sample districts replaced, for every map. On `--map fixed` it therefore never scored the changed districts: its "pipeline" efficiency gap was +0.098%, the majority map's, not the panel's +1.45%. That output is kept, labelled, as `cut_va_sensitivity_fixed_REGISTERED_CODE_DEFECT.json` with its log. A Step C copy, `cut_va_sensitivity_stepc.py`, changes only that one step: on `--map fixed`, every district is the union of the voting areas the registered assignment gives it. Its pipeline efficiency gap, +1.4450%, matches the partisan lane's and R1's. The range above is from the copy. The registered file is unchanged.
5. **Ingest ran before the run sheet was committed.** It is a set of checks, not a measure, and its result is recorded in the sheet.

Scripts written for Step C (SHA-256): `cut_va_sensitivity_stepc.py` `5f45ec65e7266b29146567190fa906084da958f9dca2bf490b394ec0f4defe8b`; `territory/score_plans_enacted.py` `9ed54016b130aab22fa6064f45cc0a4f968811761a2dc522d0f329f6928dc79a`; `territory/calibrate_enacted.py` `db2273641123b61555a5d90c6cd9d83ab38d9bae7cd2641bb9ba3578e02ff5da`; `mark_uncertain_cuts.py` `025db29b3167b9116357a3d79215f68539400637cb93ea798edaa072b853e9d9`.

## Files

Logs: `step1_partisan.log`, `step2_3_structural_verdict.log`, `step4_x1.log`, `step5_size_matched.log`, `step6_qsgy8_tripwires.log`, `step8_cut_va.log`, `step9_va_cuts.log`, `step10_rules.log`. Territory: `territory/` (chain logs, plans and their SHA-256s, scores, rank, calibration). Scoring copy: `data/shapefiles/iap_assembled/iap_2026_assembled.gpkg` with its ingest record. Candidate scores: `data/outputs/iap_assembled_phase4c.json`, `data/outputs/iap_assembled_real_maps.json`.
