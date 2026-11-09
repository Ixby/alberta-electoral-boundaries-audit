# Amendment 12 replays

Amendment 12, Part 2: each size-matched ensemble chain is replayed from its registered seed on the all-ballots file (`data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg`). A replay counts only if every vote-independent column equals the original, row for row. `replay_queue.py worker` ran the chains (four detached workers, `alberta_audit`'s `close_seats_ensemble.py` unchanged); `replay_queue.py check` compares them and writes `replay_check.json`.

## Result (checked 2026-11-08)

| Set | Chains | Replay |
|---|---|---|
| A, 91 districts | 221, 222, 223, 224 | match |
| A, 91 districts, early | 201 | **fails** |
| A, 89 districts | 120, 121 | match |
| A, 89 districts, early | 100 | **fails** |
| B, 91 districts | 230–233, 236–239 | match |
| B, 89 districts | 130–133 | match |
| C, 91 districts | 241, 243, 244, 245 | match |
| C, 89 districts | 140, 141 | match |

24 of 26 match over every row (252,500 each). Set D (251–254) is checked in `findings/allballots_ranking`.

**The two failures.** Chains 201 (47,500 rows) and 100 (36,500 rows) agree with their originals on `step`, `n_districts` and `n_parts`, and on the first row, then differ from the first proposal on:

| Column | Chain 201: rows that differ | Chain 100: rows that differ |
|---|---:|---:|
| `population_mad` | 47,495 | 36,497 |
| `reock_proxy_median` | 47,494 | 36,492 |
| `city_gap_pct` | 47,480 | 36,499 |
| `towns_flagged` | 37,524 | 29,258 |
| `n_city_districts` | 36,496 | 26,381 |

The rehearsal (`../amendment12_rehearsal/`) and Amendment 13 give 47,497 and 47,498 for chain 201's first two columns. The per-column counts are not stored (`replay_check.json` holds pass/fail only), so the difference cannot be resolved here.

So the replays are different sets of plans. Under Amendment 13, Part 2 both are dropped from the all-ballots sets: set A is 221–224 (91 districts) and 120–121 (89 districts). On election-day ballots the sets stay as filed.

**Cause: not established.** Two leads, and they coincide, so neither can be separated from the other:
- **Platform.** 201 and 100 are the only chains in this list that the run log records as run in the cloud (`alberta_audit/analysis/methodology/amendment17_chain_runs/README.md`, §1: "k=91 200, 201 … (cloud); k=89 100 … (cloud)"). Every chain run on this machine replays.
- **Code version.** 201 and 100 are also the only chains in this list that ran before the harness fixes at commit `01095181` (Amendment 5, Part 14: "Chains 201 and 100 ran before these fixes and later chains after"). The run log at that commit says the fast-fail for infeasible pairs keeps the same transition distribution but makes "fewer random draws, so a different sample path per idx". The replays ran `alberta_audit`'s current `close_seats_ensemble.py`; this repository's copy (`analysis/scripts/close_seats_ensemble.py`) has the fast-fail.

Either a different code version or a different library version or platform would change the sampler's path without any vote being read.
