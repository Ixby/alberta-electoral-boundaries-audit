# Rule-P replay run on the PC

2026-11-10 12:15 Alberta time · claude-opus-5-5 · high (from settings, not per-entry)

**Status: exploratory, not registered.** Amendment 14 is an unsigned draft. Nothing registered changes, and nothing went to OSF.

## What ran

These are the commands printed by `10_replay_p.py commands` (see `REPLAY.md`), run unchanged on the machine that holds the `alberta_audit` clone. The P vote file's SHA-256 matched `bf9b2722…73bd` before the run. A detached queue ran the jobs: up to four chains at a time, each started only when enough RAM was free.

| Job | Started | Finished |
|---|---|---|
| Canonical, 4 chains | 03:00 | 05:44 |
| Set D (251–254) | 05:44 | 06:32 |
| Sets A, B, C (24 chains) | 06:47 | 11:19 |
| Forest-ReCom Phase A, 4 chains | 11:19 | 11:49 |

Every job exited with code 0. The chain CSVs are not committed because they are too large (about 45 MB per canonical chain and 60–80 MB per set A–D chain). They sit at:
- this repository's `data/simulation_checkpoints_allballots_p/` and `data/simulation_checkpoints_forest_recom_phaseA_allballots_p/`;
- the `alberta_audit` clone's `data/*_allballots_p/` folders.

`replay_check_p.json` records each one's SHA-256.

## Check (`replay_check_p.json`)

| Set | Chains | Result |
|---|---|---|
| Canonical | 0–3 | 4 of 4 match |
| D91 | 251–254 | 4 of 4 match |
| A91 / A89 | 221–224 / 120–121 | 6 of 6 match |
| B91 / B89 | 230–233, 236–239 / 130–133 | 12 of 12 match |
| C91 / C89 | 241, 243–245 / 140–141 | 6 of 6 match |
| Forest-ReCom | 0–3 | **0 of 4: fail, dropped** |

"Match" means every vote-independent column equals the election-day original row for row, and also equals the M0 (all-ballots) replay where one exists.

**Forest-ReCom fails.** In each chain, `population_mad` differs from the original in 391–451 of 25,000 rows. The largest absolute difference is 9.1×10⁻¹³ and the largest relative difference is 2.5×10⁻¹⁶. Every other compared column matches. Under Amendment 13, Part 2 a failing chain is reported and dropped. Its cause is not assigned here, and the chains were not rerun. `ensemble_ranks_p.json` therefore gives no Forest-ReCom percentile.

*Observation, not a cause (added 2026-11-10 13:16 Alberta time · claude-opus-5-5 · high, from settings):* every differing `population_mad` value is within 2 units in the last place of a double (values 1,801 to 5,647; differences at most 9.1×10⁻¹³). `step`, `reock_proxy_median` and `reock_proxy_pct_below_030` are equal in every row of all four chains. That pattern fits the same plans with different floating-point rounding. A different plan would move a district population by whole people, and so would move the mean deviation by far more than 10⁻¹². The chains stay dropped under Amendment 13.

## Efficiency gap under rule P (`ensemble_ranks_p.json`)

Each value is the percentile of the real map's rule-P efficiency gap among the replayed chains that passed. Higher means more UCP-favouring.

| Set | 2019 enacted | Majority | Minority | Panel (v3) | ¶167 map |
|---|---|---|---|---|---|
| Canonical (87) | p21.05 | p18.41 | p99.98 | p18.31 | p25.78 |
| A (89 / 91) | | p18.86 | p99.99 | p19.10 | p27.22 |
| B (89 / 91) | | p18.84 | p99.98 | p18.82 | p26.68 |
| C (89 / 91) | | p35.47 | p100.00 | p35.76 | p46.46 |
| D (91, s.15(2)) | | | | p18.85 | p26.70 |

The rule-P efficiency gaps are: minority +5.64%, majority −2.83%, panel −2.84%, ¶167 −2.33%, 2019 −2.64%. Mean-median, declination, seats at 50/50, UCP seats and close seats are in the JSON.

## Notes

- **Stamps.** `_common.stamp()` calls `date` with `TZ=America/Edmonton`. On this Windows machine that printed UTC (18:10) labelled as Alberta time. The check and rank were rerun through a wrapper that overrides `stamp()` to give the system clock at UTC−6, with this session's model and effort. Their inputs and results are otherwise unchanged. `_common.py` itself was not edited.
- `10_replay_p.py check` exits 1, because the four Forest-ReCom chains fail.
