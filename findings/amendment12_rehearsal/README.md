# Amendment 12 rehearsal: Step C on all ballots

> **A rehearsal on the reconstructed map, provisional, not a registered result.** The map is the Independent Advisory Panel's 91-district map as assembled by the registered Amendment 10 run (`data/shapefiles/iap_assembled/iap_2026_assembled.gpkg`), not an official shapefile. Nothing here says or implies whether any map is a gerrymander: each test places the map among neutral maps, or against the commission maps, on its measure.

Run 2026-11-07, about 9:30 to 11:10 AM Alberta Time (UTC−6), under `preregistration/amendment12_rehearsal_run_sheet_2026-11-07.md` (written before any all-ballots measure of this map was computed here; its "Changes to this sheet" lists four corrections made afterwards). Repo `wt-osf` at `c01cbdcd` (nothing committed); `../alberta_audit` at `2994113c`, branch `amendment17-local-runs`, read only; `../wt-a8` at `569250cd`. Python `C:/Users/email/.venvs/audit-k91/Scripts/python.exe -I -W ignore`. No MCMC chain was started; free RAM stayed above 1.8 GB.

The only difference from the filed Step C (`findings/a10_stepc/`) is the vote substrate: `data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg` (SHA-256 `c9e21ac9…be72`, checked equal to Amendment 12's value), with P1's line at 0.01394 and S5's midpoint at 0.0019398. Registered scripts were not edited; wrappers `w01`–`w09` import them and override only the constants and the VA-file argument named in the run sheet.

## Side by side

"ED" = election-day votes, from `findings/a10_stepc/`. "AB" = all ballots, this rehearsal. Percentiles are as each script prints them.

| Step | ED result (filed) | AB result (rehearsal) | What changed |
|---|---|---|---|
| 1a. Map's scores (`iap_assembled_phase4c*.json`) | efficiency gap +1.445%, mean-median −2.53 pts, declination +0.0035, seats at 50/50 48.35%, UCP seats 58 | −1.664%, −1.09 pts, −0.0598, 49.45%, UCP seats 51 | Every vote measure. Matches `findings/allballots_ranking/real_maps_all_ballots.json` (−1.66%, 51 seats). |
| 1b. P1 efficiency gap, line | +1.45% vs +4.10%: no flag (p45.3) | −1.66% vs +1.394%: no flag (p48.0) | Line and value. |
| 1b. P2 mean-median, P3 declination, P4 seats at 50/50 (flag at p95 or more) | p19.7 / p52.4 / **p98.8, flag** | p79.4 / p48.2 / **p98.8, flag** | P2 moves from p19.7 to p79.4; P3 and P4 barely. |
| 1b. Joint (reported only) | Mahalanobis 2.45, p = 0.200 (n_eff 1,413) | 1.83, p = 0.503 (n_eff 1,248) | Ensemble and its n_eff. |
| 2. Structural lane | **2 of 5**: S1 3,557 flag, S2 24, S3 74.1% flag, S5 0.00442 (line 0.00390), S6 1 | **2 of 5**: same S1, S2, S3, S4 (0.4366), S6; S5 **0.01043** (line 0.0019398), no flag | Only S5. S1–S4 and S6 equal the filed `structural.json` exactly (checked field by field). |
| 3. Specification outcome | structural not replicated, partisan absent (1 of 4) | structural not replicated, partisan absent (1 of 4) | Nothing. Same flags (P4 only). |
| 4. X1 | not met; (a) 31 of 41, (b) 11 of 11, (c) not scored, (d) adopted | identical (byte for byte with `x1.json`) | Nothing (no votes). |
| 5. Size-matched, set D (primary) | towns p0.0; city vs rest p59.2; competitive seats (11) p75.2; EG p47.9; MM p17.0; declination p52.4; seats at 50/50 p91.6; MAD p0.0; UCP seats 58, p42.7. No Part 17 flag | towns p0.0; city vs rest p59.2; competitive seats (10) **p34.4**; EG p48.0; MM **p77.4**; declination p47.6; seats at 50/50 p89.9; MAD p0.0; UCP seats 51, p42.9. No Part 17 flag | Competitive seats 11 to 10 and p75.2 to p34.4; MM p17.0 to p77.4. No flag either way. Set D matches `findings/allballots_ranking/setD_panel_all_ballots.json`. |
| 5. Set A (chains 221–224; Amendment 13, Part 2 drops chain 201) | city vs rest p99.5 **flag**; seats at 50/50 p96.7; MM p18.5; competitive seats p72.9 | city vs rest p99.6 **flag**; seats at 50/50 p95.9; MM p79.2; competitive seats p31.1 | Same flag. |
| 5. Set B (all eight chains, rerun 2026-11-08) | city p87.7; seats at 50/50 p95.4; MM p19.7; competitive seats p73.0 | city p87.7; seats at 50/50 p94.7; MM p79.2; competitive seats p31.4 | No flag either way. |
| 5. Set C (chains 241, 243–245, run 2026-11-08) | towns p32.1; city p67.8; seats at 50/50 p90.4; MM p25.9; competitive seats p73.6 | towns p32.1; city p67.8; seats at 50/50 p92.0; MM p82.6; competitive seats p39.4 | No flag either way. |
| 6. qsgy8 tripwires | 1 of 4 (MO #1 Lethbridge, ratio 2.0); MO #4 divergence −1.2 pts | as filed (run with the ED seats at 50/50): identical to the filed scorecard apart from its date; with the AB seats at 50/50 (0.4945): 1 of 4, MO #4 divergence −0.2 pts | Amendment 12 does not list the tripwires. MO #4's comparison percentiles are cached ReCom and SMC outputs on ED votes, so the AB variant mixes substrates and is a sensitivity only. |
| 7. R1 efficiency gap (flag p < 0.05) | +1.45%; null mean +1.14%; **p = 0.665** | −1.66%; null mean −1.72%, 95% −3.39% to −0.06%; **p = 0.914** | No flag. |
| 7. R2 neighbour drain | 0.00441; null mean 0.00847; **p = 0.597** | 0.01043; null mean 0.00598, 95% 0.0004 to 0.0253; **p = 0.419** | No flag. |
| 7. Beside R1/R2: mean-median, declination, UCP seats | p 0.064, 0.818, 1.000 | p 0.913, 0.794, 1.000 | Mean-median moves from near the edge of its null to the middle. |
| 7. Calibration (holdout chain 5) | EG false-positive rate 5.3%, drain 1.4%; split-R̂ 1.000, 0.999 | EG 3.3%, drain 1.7%; split-R̂ 0.999, 0.999 | Label-shuffle drain p: 0.0 (flags 97% of neutral plans) becomes 0.034 (flags 71%); still reported only. |
| 8. Cut voting-area range (sensitivity) | 245 cut VAs, 132 flipped; 6 raise, 5 lower, 121 no change; bounds +1.32% to +2.94% around +1.45% | 245 cut VAs, 132 flipped; 8 raise, 10 lower, 114 no change; bounds **−3.26% to −1.49%** around −1.66% | A change under 10⁻⁹ points (floating-point noise) counts as none. Pipeline EG matches step 1a. The AB range stays below P1's 1.394% line, set D's 95th percentile (+1.38%) and R1's null 97.5th percentile (−0.06%). Largest single flip: −1.39 pts (VA 053, Calgary-Confluence to Calgary-Acadia). Greedy bounds ignore interactions. |
| 9. Voting areas cut | 211 (2023) / 218 (2026) | identical (byte for byte with `va_cuts.csv`) | Nothing (no votes). |
| 10. EBCA rules (supplementary) | as filed | identical (`rules_check.json`) | Nothing (no votes). |

Set A, B, C, D tables in full: `size_matched_allballots.md` / `.json`. Territory: `territory_allballots/` (`rank.json`, `calibration.json`, `scores.csv`).

## Update, 2026-11-08: every replay is in

All 26 Amendment 12 replays finished (`findings/amendment12_replays/replay_check.json`). 24 match their originals row for row in every vote-independent column. Two do not: set A's early chains **201** (91 districts) and **100** (89 districts). Both diverge from the first proposal on: row 0 matches and later rows differ in `population_mad`, `reock_proxy_median`, `city_gap_pct` and the city and town counts, while `step`, `n_districts` and `n_parts` match. Under Amendment 13, Part 2 both are dropped from the all-ballots sets, so set A is 221–224 (91) and 120–121 (89). They are the only two chains in the replay list that the run log says were run in the cloud (`alberta_audit/analysis/methodology/amendment17_chain_runs/README.md`, §1); every chain run on this machine replays. That is a lead, not an established cause.

`w00` now checks sets A (221–224), B (all eight) and C (all four) and writes `replay_check_ABC.json`; `w05` uses those whitelists. Both were rerun. The size-matched results are now complete for all four 91-district sets, and the reading is unchanged: set A's city-versus-rest flag (p99.6) is the only flag, as filed (p99.5). `replay_check_AB.json` is the earlier, superseded check.

## Cross-checks

| Check | Expected | Found |
|---|---|---|
| S1–S4 and S6 equal filed `structural.json` | exactly | **equal** |
| X1 equals `x1.json` | exactly | **equal** (byte for byte) |
| S5 on all ballots | about 0.0104 for the v3 map | **0.010429** for the assembled map, and the same 0.010429 for `iap_2026_assembled_v3.gpkg` (the files differ by hash; their S5 is identical to 15 digits). Amendment 12, Part 5: 0.01043. The R2 drain (0.010434) differs in the fifth digit because it is computed on the voting-area graph. |
| P1–P4 against Amendment 12, Part 5 | close | P1 −1.66% (−1.66%); P2 p79.4 (p79.45); P3 p48.2 (p48.22); P4 p98.8 (p98.82). Same map, so they agree to rounding. |
| Pipeline EG in step 8 equals step 1a | equal | −0.016637 in both |
| Territory plans identical to the filed plans | SHA-256 | asserted in `w07` before scoring (`plans_sha256.txt`); passed |
| Replay check, vote-independent columns, sets A, B and C | every chain row for row | A 221–224, B (all eight) and C (all four) pass over all 252,500 rows (`replay_check_ABC.json`, 2026-11-08); **A chain 201 fails** (below) |

## Failures and blockers

1. **Set C: blocked on 2026-11-07.** `../alberta_audit/data/simulation_checkpoints_k91_muni_allballots` did not exist, so there was nothing to run. Its four chains (241, 243–245) were replayed on 2026-11-08 and pass (`replay_check_ABC.json`; see the update above).
2. **Set A: chain 201 fails the Amendment 12, Part 2 replay check.** The filed set A is chains 201, 221–224 (`findings/a10_stepc/size_matched.json`; the run sheet first said otherwise, corrected in its "Changes"). The all-ballots chain 201 (47,500 rows, `[nk 201] 47500/47500 638s`) has the same `step` and `n_parts` as the original in `data/simulation_checkpoints_k91/chain201_samples.csv`, but `population_mad` differs in 47,497 of 47,500 rows (largest gap 1,687), `reock_proxy_median` in 47,498, `towns_flagged` in 37,524 and `n_city_districts` in 36,496. So it is not the same set of plans. Chain 201 is dropped (`replay_check_AB.json`, `A201`), and set A is partial (4 of 5 chains). Cause not investigated; the likely candidates are a different chunk size, seed or code version between the original and the replay of chain 201.
3. **Set B: partial on 2026-11-07.** Chains 230–233 were complete and passed (252,500 rows each); the filed set has eight chains, and 236–239 had no all-ballots files. All eight were run by 2026-11-08 and pass (`replay_check_ABC.json`).
4. **R1/R2's territory null: the replay is blocked; a rescore ran.** `territory_null.py` (SHA-256 `46fc7a16…ee02`, the filed one) has no `--va-file` and no votes input. Its only vote-bearing call is `me.build_va_graph(verbose=False)` at line 172, and its sampler reads no votes; votes enter only in `territory_score.Substrate` (line 53). The plans are therefore the same whatever the ballots. `w07` rescored the filed plans (chains 1, 2, 4, 5, 6; their SHA-256s asserted equal to `plans_sha256.txt`) on the all-ballots file: 33 territory districts, 58 fixed, s.15(2) cap 2, 1,440 reference plans, as filed. That is **not** the Part 2 replay and is labelled as a rescore. Code is `wt-a8` at `569250cd`; Step C ran `42b5fda8`. The diff is CLI arguments only (`territory_score.py` lines 227–243, SHA now `47ead096…`, the sheet recorded `0485e788…`); `Substrate`, `score_plans` and `calibrate` are unchanged. `wt-a8/analysis/scripts/mcmc_ensemble.py` and `close_seats_ensemble.py` differ from `wt-osf`'s copies; the rescore used `wt-a8`'s, as Step C did.
5. **`size_matched_results.main()` cannot be called as filed on all ballots.** It always places the 89-district commission maps, which needs an 89-district set, and `simulation_checkpoints_k89_s152a23_allballots` does not exist (it exits "no 89-district neutral-map set found"). `w05` calls the module's `load_chains`/`summarize`/`render` for k = 91 only. This is a wrapper limit, not a registered-code defect.
6. **`run_structural_battery.compute_S5_drain` returns a "STUB" dict on any exception** (`flag: None`). The wrapper's run returned a real value; any official run must check `_note` is absent.
7. **`joint_outlier_score_canonical` and others append to `data/outputs/script_run_audit.jsonl`** (an existing file). The wrappers no-op `_log_run`; registered scripts called directly (`score_x1.py`, `va_bisection.py`, `rules_check.py`, `phase_b_scorecard.py`, `close_seats_ensemble.py real`) did not add lines (checked with `git diff`: only three earlier lines, dated 2026-11-05 and 11-06, differ from HEAD; not from this run). `reports/public/report_public.md` showed as modified for a while during the session; this run did not write it.
8. **Superseded run.** The first `w05` run (before the replay gate and before chain 201 was found) is overwritten; its set A/B results did not differ materially from the gated ones. The run-sheet error about chain 201 is recorded in the sheet.

No other step failed. Some commands exceeded the tool's 120-second limit and ran in the background; all that were kept completed with exit code 0.

## The R1/R2 replay command the official run needs

`territory_null.py` takes no votes, so the replay is the filed command with the all-ballots form of the wrapper, `w09_territory_null_allballots.py` (written, **not launched**; it defaults `mcmc_ensemble.build_va_graph` to the all-ballots file and calls the module's own `main()`). From `../wt-a8`, once per chain (1, 2, 4, 5, 6 for the Step C map; chain 3 does not seed there; the official map needs its own `--enacted` and `--stated-low`, and its chain 3 may seed), detached by WMI with a `pythonw` runner as the filed run was:

```
C:/Users/email/.venvs/audit-k91/Scripts/python.exe -I -W ignore "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/wt-osf/findings/amendment12_rehearsal/w09_territory_null_allballots.py" --idx N --enacted "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/wt-osf/data/shapefiles/iap_assembled/iap_2026_assembled.gpkg" --stated-low 2 --out C:/tmp/a12rehearsal/territory --steps 100000 --thin 250
```

Chain time as filed: about 13 minutes each (chain 1: 783 s). Then score and rank with `w07` (its `MAP`, `STATED_LOW` and plan directory are constants at the top; they would be arguments for the official map). For the Step C map the replay's plans must hash to `plans_sha256.txt`; the rescore already shows that, so the replay would add no information for this map. It is only needed for a map whose plans have not been generated.

## What must still happen before the official run can be done on all ballots

1. **Set A:** decided. Amendment 13, Part 2 drops chain 201, so set A on all ballots is chains 221–224.
2. **Sets B and C:** done. All eight set B chains and set C's four chains (241, 243–245) pass the `w00` vote-independent-column check (`replay_check_ABC.json`).
3. **The territory null** for the official map's own territory (Amendment 8, Part 5's rerun rule is applied to the official map, not this one). Amendment 12, Part 2 says "replayed … with `--va-file`", but `territory_null.py` has no such flag and reads no votes. The text needs a reading before the run: either the Part 2 check for the territory is the plans' byte identity plus scoring on the all-ballots file (what `w07`/`w09` do), or the script is changed. That is the author's decision; this rehearsal changed nothing.
4. **Parametrise** `w07` (map, `--stated-low`, plan directory, reference and holdout chains) and `w05` (chain whitelists) for the official map, and commit the wrappers and a final run sheet before the official map is scored. `w08` (cut voting-area range) is specific to the reconstruction (it needs `C:/tmp/a10reg/fixed`) and has no counterpart for an official map.
5. **Run order from Amendment 12, Part 4:** if a replay has not finished when the map is posted, the election-day run goes first as a sensitivity and the all-ballots run follows once replays pass; the run record states the order.
6. **MO #4 (tripwire sampler divergence)** compares against cached election-day-substrate ReCom and SMC outputs. Amendment 12 does not list the tripwires among the vote-using steps, and its "What this amendment does not change" paragraph names the qsgy8 tripwires explicitly. So the official run uses the election-day seats at 50/50, as filed (resolved 2026-11-07 from the amendment's text; this rehearsal ran both, 1 of 4 either way).
7. **The canonical all-ballots ensemble** is the registered comparison for P1–P4 (4 × 252,500, n_eff 1,248 from `simulation_convergence_diagnostics_allballots.json`, against 1,413 on ED). The joint-score p uses it; if a registered n_eff is wanted, Amendment 12 should name this file.
8. **`verdict_synthesis.py`'s template text** ("Lunty map …") is not applicable to any other map; the headline must not be read.

## Files

Run sheet: `preregistration/amendment12_rehearsal_run_sheet_2026-11-07.md`. Wrappers: `_a12.py` (shared setup), `w00_replay_check.py`, `w01_score_assembled_allballots.py`, `w02_joint_outlier_allballots.py`, `w03_structural_allballots.py`, `w04_verdict_allballots.py`, `w05_size_matched_allballots.py`, `w07_territory_rescore_allballots.py`, `w08_cut_va_allballots.py`, `w09_territory_null_allballots.py` (not launched). Results: `iap_assembled_phase4c_allballots.json`, `joint_outlier_allballots.json`, `structural_allballots.json`, `structural_v3_allballots.json`, `verdict_allballots.json`, `x1_rerun.json`, `iap_assembled_real_maps_allballots.json`, `size_matched_allballots.{json,md}`, `replay_check_AB.json`, `tripwires_as_filed/`, `tripwires_allballots_s50/`, `territory_allballots/`, `cut_va_sensitivity_allballots_fixed.json`, `cut_vas_fixed.csv`, `va_cuts_rerun.csv`, `rules_check_rerun.{json,csv}`. Logs: `step*.log`, not in the repository (`.gitignore` excludes `*.log`).
