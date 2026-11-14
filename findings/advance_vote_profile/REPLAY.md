# Replaying the ensembles on the P vote file

2026-11-10 01:33 Alberta time · claude-opus-5-5 · medium

**Status: exploratory, not registered.** Nothing here changes a registered result. No percentile against these ensembles is given under P until the replays below have run and passed their checks.

## Why the replays cannot run here

The audit ranks each map against computer-drawn maps (the "ensembles"). The repository does not store those maps. It stores one row of scores per map. A drawn map can only be rebuilt by rerunning its chain from its registered seed.

The drawing step reads population, not votes. So a rerun on the P vote file draws the same maps, and only the scores change. A rerun counts only if every column that does not depend on votes matches the original, row for row (Amendment 12, Part 2; Amendment 13).

Two things stop that rerun on this machine.

1. **Most chains are not here.** Sets A, B, C and D, and the all-ballots (M0) replays of every set, are on the machine that holds the `alberta_audit` clone. This checkout holds only the election-day canonical chains (`data/simulation_checkpoints_canonical/`), the Forest-ReCom scores (`data/outputs/forest_recom_raw_samples_phaseA.csv`), and set A's early chains 201 and 100, which Amendment 13 already excludes because they do not replay.
2. **The sampler is far too slow here.** A test of canonical chain 0 on this machine (Python 3.13.17, NumPy 2.5.3, GerryChain 0.3.2, networkx 3.6.1) reached step 3 of 20 after 135 seconds. A first test of 600 steps did not finish its first 300-step chunk in 15 minutes. The canonical ensemble is 4 × 252,500 steps; on the machine that ran it, the 4 chains ran in parallel from 01:55 to 04:18 (`findings/allballots_ranking/README.md`). A rerun here would take months, and a different software stack may not draw the same maps anyway (Amendment 13 records two chains that failed to replay on a different platform).

**One ensemble was rescored here:** the redraw-test null for R1 and R2. Its maps are stored in the repository (`findings/a10_stepc/territory/`). See `09_rescore_territory_null.py` and `outputs/territory_null_p.json`.

## What to run, and where

Everything below uses the P vote file:

```
data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg
SHA-256 bf9b27226e457ddb4b8c2feaa77f7402d1c3d1284657c821d208f6597b8f73bd
```

Check that hash first. The file can be rebuilt byte for byte with `python findings/advance_vote_profile/08_build_vote_file_p.py`. It is not yet committed, so copy it, or rebuild it, on the machine that runs the chains.

`python findings/advance_vote_profile/10_replay_p.py commands` prints every command below with its chain number.

| Ensemble | Where | Command | Chains |
|---|---|---|---|
| Canonical, 87 districts, ±25% (ReCom proposals ±12.5%), base seed 1432864451 | this repository, on the machine that ran the canonical | `python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 1010000 --n-chains 4 --chunk-size 5000 --run-id allballots_p --va-file data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg --max-workers 4` | 0–3, 252,500 each; writes `data/simulation_checkpoints_allballots_p/` |
| Set D, 91 districts, s.15(2) | `alberta_audit` clone | `python -I -W ignore analysis/scripts/close_seats_ensemble.py nk --k 91 --idx N --steps 252500 --chunk 500 --s152 data/outputs/s15_2_va_criteria.csv --va-file <P file> --out data/simulation_checkpoints_k91_s152a23_allballots_p/chainN_samples.csv` | 251–254 |
| Set A | `alberta_audit` clone | same as set D without `--s152`: `--k 91` (221–224) or `--k 89` (120, 121), out dir `simulation_checkpoints_k91_allballots_p` / `simulation_checkpoints_k89_allballots_p` | 221–224, 120–121 (201 and 100 excluded, Amendment 13) |
| Set B | `alberta_audit` clone | same with `--proposal-eps 0.25`, out dir `…_eps25_allballots_p` | 230–233, 236–239; 130–133 |
| Set C | `alberta_audit` clone | same with `--proposal-eps 0.25 --muni-surcharge 0.5`, out dir `…_muni_allballots_p` | 241, 243–245; 140, 141 |
| Forest-ReCom Phase A (robustness check, OSF he53s; not in Amendment 12's list) | this repository, on the machine that ran it | `python findings/advance_vote_profile/10_replay_p.py forest` (redirects the script's outputs to `data/simulation_checkpoints_forest_recom_phaseA_allballots_p/`, so no committed file is overwritten) | 0–3, 25,000 each |
| Territory null for the official map (R1, R2) | as Amendment 13, Part 1 | score its plans on the P file, as `09_rescore_territory_null.py` does for the provisional map | — |

Run the `alberta_audit` chains with that clone's `close_seats_ensemble.py` unchanged, as `findings/amendment12_replays/replay_queue.py` did for M0. The set D original directory is assumed to be `data/simulation_checkpoints_k91_s152a23/` (the M0 replay sits beside it with `_allballots`); check the name before running.

Ensembles that need no replay: the 2015 and 2019 threshold ensembles use those years' votes, not 2023's, so the 2023 placement rule does not touch them.

## The checks a replay must pass

1. The P file's SHA-256 is the value above.
2. Every chain has its full number of rows.
3. Every vote-independent column equals the original chain, row for row: `step, population_mad, reock_proxy_median, reock_proxy_pct_below_030, n_districts` for the canonical and forest chains; also `n_parts, n_city_districts, towns_flagged, city_gap_pct, s152_districts` where present for sets A to D. Compare with the election-day original, and with the M0 replay where one exists (`…_allballots/`; Forest-ReCom has none). Both must match. A vote-independent column that the original has and the replay lacks is a failure, not a skipped column.
4. Any chain that fails is reported and dropped (Amendment 13, Part 2). Its cause is not guessed.

`python findings/advance_vote_profile/10_replay_p.py check --audit <path to alberta_audit>` runs checks 2 and 3, against both the original and the M0 replay, and writes `outputs/replay_check_p.json`. It exits non-zero, naming each failing chain and column, if any replay fails. In this checkout it reports every chain as "not run".

## What to bring back

- `outputs/replay_check_p.json` from the `check` step.
- `outputs/ensemble_ranks_p.json` from `python findings/advance_vote_profile/10_replay_p.py rank --audit <path>`. It ranks each real map's P score (from `outputs/headline_table.csv`, beta = 1.0) against the chains that passed: efficiency gap, mean-median, declination, seats at 50/50, UCP seats, and close seats where the chain records them. 87-district sets rank all five maps, as `findings/allballots_ranking/canonical_ranking.json` does; 89- and 91-district sets rank the maps of their size.
- The SHA-256 of every replayed chain CSV (recorded in `replay_check_p.json`).
- For set D and sets A to C, the vote-free statistics (towns split, city versus rest) do not change, so only the vote-based ones need restating.
