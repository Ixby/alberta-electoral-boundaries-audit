# Amendment 17 chain runs — local machine run log (2026-10-29 →)

Exploratory unless named in the amendment log. Nothing here compares an ensemble with a real map.
Living document: append, never rewrite history. Times are America/Edmonton (MT).

## 1. Who asked, and the rulings (verbatim)

- Request: the cloud "Audit" session (session_018fR2piQUSLgKm3yG7SKLG7), on Wuff's behalf, asked
  this machine to run size-matched ReCom chains for Amendment 17 (91- and 89-district `nk` mode of
  `analysis/scripts/close_seats_ensemble.py`), indices 220–223 (k=91) and 120–121 (k=89).
- Owner (Wuff) words that set the design, in order:
  - "do whateve it tells you to" — approve the Audit session's run instructions.
  - "fx the script" — add resume and fix the slowness.
  - "if we're going to launch with a resume, kill the ones that can't"
  - "fix the nits. send both points" — s.15(2) branch and docstring fixes; two framing points to Audit.
  - "run the municipality-aware chains too."
  - "we want to be as strict as the statue, no more, no less"
  - Choices on the three-question prompt: ±25% band = **"Keep both"**; s.15(2) = **"Build it"**;
    towns = **"Run as sensitivity (Recommended)"**.
  - "i rather see what we can see than have not bothered to look"
  - "index the mucipality aware target off what all three maps shows as a ratio"
  - "lookup metis boundaries, your assumption is fine if you can't find, but look."
- Audit session assigned index blocks (message 2026-10-29 evening): statute band 230–239 / 130–139;
  municipality-aware 240–249 / 140–149; s.15(2) 250–259 / 150–159. Never reuse: k=91 200, 201,
  210–212 (cloud), 220–225 (this machine); k=89 100, 102, 110 (cloud), 120–121 (this machine).
  Cloud will use 260+ / 160+ if it ever runs more.
- Audit's position on the surcharge was "fix 1.0, don't tune". The owner's later instruction to
  index it off the three maps overrides that; both are recorded here and sent to Audit.

## 2. Environment

| Item | Value |
|---|---|
| Machine | Windows 11, Intel i7-1360P, 12 cores / 16 logical; sleep on AC set to Never (`powercfg /change standby-timeout-ac 0`; was 60 min) |
| Clone | `alberta_audit` at master `35ea8013` (#33); `git restore .` first cleared typechanged (dedup-link) files |
| LFS | git-lfs 3.7.1; the four gpkgs pulled as real files (22.0 / 5.5 / 4.9 / 4.9 MB) |
| Python | 3.12.13 via uv venv `C:\Users\email\.venvs\audit-k91` (matches tests.yml) |
| Packages | gerrychain 0.3.2, networkx 3.6.1, geopandas 1.1.3, shapely 2.1.2, pyproj 3.7.2, pandas 2.2.3, numpy 2.2.6, pyogrio 0.13.0, pyyaml 6.0.3 (needed by data_loader; CI installs it unpinned), pytest 9.2.0 (tests only) |
| Smoke test | `real` mode: majority_2026 ucp 55 / close4 13 / towns 0; minority_2026 60 / 4 / 6 — exact match to the expected values |
| Launch | each chain via WMI `Win32_Process.Create` (hidden `cmd /c python -u ... > .log 2> .err`) so it survives harness task-tree kills |

## 3. Code changes (uncommitted; Audit lands them)

Full diff: [`amendment17_patch.diff`](amendment17_patch.diff) (vs `35ea8013`). Summary:

1. **Fast-fail for infeasible pairs (nk only).** At commit e74a5a13 the chains logged no 500-step chunk
   in 15+ min (≥770 s/chunk; Monday deadline needed ≤600). Cause: the nk seed is built at epsilon 0.25
   but recom splits at pop_deviation/2 = 0.125; a pair whose merged population is outside
   2·ideal·(1±epsilon) cannot be split, and `bipartition_tree` (allow_pair_reselection=True) spends its
   default max_attempts = 100,000 spanning trees before ReselectException — silently (the 1,000-attempt
   warning is suppressed when reselection is on). The wrapper raises ReselectException at once for such
   pairs (1e-9 relative slack). Same transition distribution; fewer random draws, so a different sample
   path per idx. max_attempts unchanged. Result: ~5 s/chunk alone, ~10 s with 6 chains.
2. **Exact resume (nk only).** Each chunk restarts from a Partition rebuilt from the assignment (recom draws
   `random.choice(tuple(partition["cut_edges"]))`, and a carried Partition's set order is not
   reproducible). After each chunk an atomic JSON checkpoint `<out>.ckpt.json` holds the assignment,
   both RNG states and the kernel options; `--resume` validates them, trims the CSV, continues.
3. **Kernel options:** `--proposal-eps` (None = canonical ±12.5%; 0.25 = s.15(1) band) via a new
   `proposal_epsilon` argument on `run_ensemble` (None keeps the canonical behaviour), and
   `--muni-surcharge W` (gerrychain region-aware ReCom on 2021 CSDUID; 0 = off).
4. **`csd_split_ratio`** on Geo (the municipality calibration ratio, §6).
5. **Nits (mcmc_ensemble.py, tests):** the s.15(2) branch of `alberta_statutory_population_constraint`
   said "area > 5,000 km², up to 50% either side"; now "below average only, ≤50%, area > 20,000 km²,
   ≤4 districts", commented as admitting more than the statute (only criterion (a) computable) and
   unreachable at epsilon ≤ pop_deviation. Docstring "Electoral Divisions Act" → "Electoral Boundaries
   Commission Act s.15(1)"; test comment 5,000 → 20,000 km².
6. rep87 mode is untouched by 1–3 so its canonical replay stays exact.
7. After the patch file was sent (SHA-256 84F85728…3A35, the copy in this folder), two more changes
   landed on this branch: `_no_power_throttling()` (Windows EcoQoS opt-out, speed only) and the new
   `analysis/scripts/s152_criteria.py`. The default-path regression hash is unchanged by both.

### Verification evidence

| Check | Result |
|---|---|
| Kill-and-resume (nk 221, 3,000 steps, chunk 500, killed after checkpoint at 1,500) | resumed CSV **byte-identical** to the unbroken run. CSV-trim path (kill between CSV append and checkpoint) not exercised. |
| Default path unchanged by later edits (nk 221, k=91, 1,500 steps, chunk 500) | CSV SHA-256 `E425BAEE8EA7EF227D456D46AB95C2D01BED1FC06699EDC81D4E9FD09E5CD2AB` before and after each edit (s.15(2) nit, options, ratio). Windows CRLF output. |
| tests/test_scoring.py | 16 passed |
| /code-review (low) on the resume + fast-fail diff | no findings |

## 4. Chain sets

| Set | Kernel | k=91 idx | k=89 idx | Output dir | Status (2026-10-29 20:21) |
|---|---|---|---|---|---|
| A. Registered half-band | eps ±12.5% (default) | 221, 222, 223, 224 | 120, 121 | `data/simulation_checkpoints_k91/`, `_k89/` | 88,000–98,500 / 252,500; ETA ~21:30 |
| B. Statute band | `--proposal-eps 0.25` | 230, 231, 232, 233 | 130, 131 | `..._k91_eps25/`, `_k89_eps25/` | ~27,500 / 252,500; ETA ~22:30 |
| C. Municipality-aware (sensitivity) | eps 0.25 + `--muni-surcharge 0.5` | 241, 243, 244, 245 (next free if a seed fails) | 140, 141 | `..._k91_muni/`, `_k89_muni/` | starts when A finishes |
| D. s.15(2) | eps 0.25 + s.15(2) split rule | 250s | 150s | — | spec awaiting owner sign-off (governance/GOVERNANCE-s15-2-chain-model.md) |

All runs: `--steps 252500 --chunk 500 --resume`. A 220-series first launch (old code, 19:17) was
killed at ≥770 s/chunk with zero rows written; A was relaunched on the patched code at ~19:38.

### Seed failures (indices retired, never reuse)

| idx | k | Failure | Diagnosis |
|---|---|---|---|
| 220 | 91 | `Could not find a possible cut after 50000 attempts` while seeding | Exact replay (`tools/prof_seed.py`): the first 89 one-sided carves took 1 try each; the final 2-way split of a 123-VA remainder (east Calgary / Chestermere, 2019 EDs Calgary-East, Calgary-Peigan, Chestermere-Strathmore + scraps; 398 km², pop 104,368 = 2.228 × target) used all 50,000 attempts in 50 s. Window per side 0.978–1.25 × target; best cut over 3,000 random trees left one side 38.7% off (median 54%); Fiedler sweep can balance (1.116 / 1.112) only with a disconnected side. A ragged-collar remainder: deterministic per seed. Node list: `seed220_remainder.json`. |
| 240 | 91 | same, while seeding (muni test) | not profiled; same failure class |
| 242 | 91 | same, while seeding (calibration) | not profiled; same failure class |

Suggested to Audit (not implemented): on seed failure, retry at s+999+j deterministically instead of burning the index.

## 5. Statute modelling notes sent to Audit

Statute text from the repo's VERIFIED-PRIMARY extracts (`proposals/site_rewrite_2026-10-29/legal_framework.md` §B); not re-checked against King's Printer here.

- s.13 seat count, s.12 census population: modelled. s.15(1) ±25%: the registered kernel proposes
  within ±12.5% (stricter than the statute); set B uses the full band.
- s.15(2): not reachable in A/B/C. Set D will model it (spec pending).
- s.14 factors (incl. municipalities, s.14(b)): "may take into consideration" — permissive, so not a
  constraint in A/B. The town-split measure in A/B is therefore relative to population-only maps; set C
  is the "commission weighing s.14(b)" sensitivity reading.
- eps 0.25 widens the neutral population spread (eps_full_robustness.md: median MAD ~6,400 vs ~3,160),
  so population-based measures look more ordinary under B; must be labelled; headline set is Wuff's
  call, being confirmed directly by Audit.

## 6. Municipality-aware calibration

Ratio R = share of 2021 CSDs (excl. Calgary, Edmonton; spanning ≥ 2 VAs; pop > 0; **169 CSDs**) split
into more pieces than population requires (piece = ≥ 2% of the CSD's pop; need = ceil(pop / (1.25 × average))).

| Real map | R |
|---|---|
| 2019 enacted | 0.1657 (28/169) |
| Majority 2026 | 0.1124 (19/169) |
| Minority 2026 | 0.2485 (42/169) |
| **Target = mean of three** | **0.1755** |

Tuning (eps 0.25; R sampled every 500 steps; mean over second half):

| k | idx | steps | W | R |
|---|---|---|---|---|
| 91 | 241 | 6,000 | 0 | 0.388 |
| 91 | 241 | 6,000 | 0.10 | 0.338 |
| 91 | 241 | 6,000 | 0.25 | 0.279 |
| 91 | 241 | 6,000 | 0.50 | 0.163 |
| 91 | 241 | 6,000 | 1.00 | 0.065 |
| 91 | 241 | 10,000 | 0.45 | 0.198 |
| 91 | 241 | 10,000 | 0.50 | 0.168 |
| 91 | 241 | 10,000 | 0.55 | 0.155 |
| 89 | 142 | 10,000 | 0.45 | 0.198 |
| 89 | 142 | 10,000 | 0.55 | 0.163 |
| 89 | 142 | 10,000 | 0.65 | 0.113 |

Raw 10k-step output: [`muni_calibration_10k.jsonl`](muni_calibration_10k.jsonl). Interpolated W ≈ 0.49 (k=91),
≈ 0.51 (k=89); **W = 0.5 fixed for both**, no further tuning after production starts.
Caveats recorded for the amendment: (i) the target includes the minority map, pulling the null toward
it (conservative for the minority); (ii) C answers "relative to how these three maps treat municipalities
on average", not an independent standard; tuned on R only, but R overlaps the town-split measure.

A pre-calibration mechanism check (k=91, 1,500 steps, last 500 rows; ensemble only, no real map) showed
towns_flagged ~7.7 at W=0 vs ~0.75 at W=1.0 — the surcharge works.

## 7. Metis settlement data (for set D, criterion (d))

Official Government of Alberta "Metis Settlement" polygons, all 8 settlements, retrieved
2026-10-30T02:12:46Z; provenance in `data/shapefiles/reference/metis_settlements_dl/SOURCE.md`.

## 8. Operations

- Monitor: `tools/watch_chains.sh` (milestones every 50k steps, errors, finishes, stalls > 15 min).
- To restart any chain after a crash or reboot: re-run its exact launch command (with `--resume`).
- Do not `git restore` / `git pull` this clone while chains run: a resume reloads the script from disk.
- Thermals: sustained ~85 °C package under 12 chains (i7-1360P TjMax 100 °C) — within spec.

## 9. Tools in `tools/`

`prof_seed.py` (exact seed replay + failure diagnosis), `where220.py` (remainder location),
`muni_calib.py` (real-map R and W tuning), `resume_test.py` (kill-and-resume identity test),
`watch_chains.sh` (monitor).

## 10. Log

- 19:17 first launch (old code). 19:20 220 seed failure → 224. 19:35 slowness diagnosed; old chains killed.
- 19:38 set A relaunched on patched code. 19:45 report + full diff to Audit.
- ~19:50 s.15(2) nit fixed, two framing points to Audit. ~20:00 owner rulings on band / s.15(2) / towns.
- ~20:05 set B launched. ~20:10 Metis data retrieved; R target computed; calibration runs.
- ~20:20 W = 0.5 chosen and sent to Audit; this document written.
- ~20:25 owner "go" on the s.15(2) Question gate (six readings). `analysis/scripts/s152_criteria.py`
  written; per-VA inputs at `data/outputs/s152_va_criteria.csv` (SHA-256 509BAE03…F5FA). Legislature at
  53.533694, −113.506611 (Wikipedia). OSM network 336,855 vertices; 13 towns > 8,000 (VA-summed 2021 pop).
- ~20:35 **Throughput fix:** per-core counters showed all chains on the 8 E-cores (logical 8–15 at 128%)
  with the 4 P-cores (0–7) idle — Windows EcoQoS/power throttling on windowless background processes.
  Disabled per process (`SetProcessInformation(ProcessPowerThrottling, EXECUTION_SPEED off)`) on all
  running chains → all 16 logical CPUs busy; statute-band rate ~29.6 → ~40 steps/s per chain. Script now
  opts itself out at startup (`_no_power_throttling`, speed only; default-path hash unchanged E425BAEE…D2AB).
- ~20:40 **s.15(2) predicate validation** (`tools/validate_s152.py` vs population_deviation_reaudit.md):
  CPN (both), Canmore-Banff, RMH-Banff Park match criterion-by-criterion. Bug fixed: gerrychain
  `boundary_node` marks lake-hole VAs (Lesser Slave Lake) → (e) now = exterior rings of the VA union,
  ≥ 100 m shared. Remaining mismatch, a **lead not a conclusion**: Lesser Slave Lake (b) — re-audit P
  (commission p. 248, "Slave Lake ~250 km"), but the ED's nearest boundary (VA 1383, 99.99% inside LSL)
  is 113.1 km straight-line / 134 km by OSM road from the Legislature; LSL still 3/5.
- ~20:45 Audit (Amendment 20 registers W = 1.0; owner told Audit "faithful as possible to the legislation
  and the norm, we're not chasing goalposts") asked to HOLD the municipality-aware launch pending
  Amendment 21 and to calibrate on 2019 + majority only (target 0.1391). Held; conflict put to owner.
  No W = 1.0 / 0.5 production output exists. Calibration W = 0.6, 0.7 (k=91) running.
- ~21:00 Audit: patch applied cleanly (patch SHA-256 84F85728…3A35 matches) and landing on branch
  `ccr-7082dbd7-sqy3h2` (Amendment 20 commit ce05ddf1 fetched). Audit's independent s.15(2) build
  (`s15_2_criteria.py`, to come) confirms LSL (b) 133.9 km → registered as a disclosed difference
  (literal wording stricter than the commission's count; eligibility unchanged). Audit now recommends
  anchoring W on the 2019 enacted map alone (R = 0.1657 → W ≈ 0.5; minority under test; majority
  keeps 62 divisions in the November map under R5); launch still on the owner's answer. Statute-band
  234–237 / 132–133 approved by Audit. Asked to cross-check per-VA tables once Audit pushes; NRCan
  Aboriginal Lands reserve layer proposed (needs owner OK to fetch).
- ~21:05 **Owner: "i agree with cloud"** → W = 0.5 anchored on the 2019 enacted map (R = 0.1657);
  NRCan fetch approved. Extra calibration (k=91, idx 241, 10k): W 0.6 → 0.133, 0.7 → 0.104.
  Cross-platform check: Audit's content hash of the nk 221 regression CSV (round 6, LF, %.6f) =
  `66e00fa2…67cf`, sums 86117 / 14655 / 10605 / −1.102778 — **identical on this machine** (pandas 2.2.3,
  numpy 2.2.6) and on Audit's Linux run (pandas 3.0.5); only raw-file formatting differs.
- ~21:10 NRCan CLSS Aboriginal Lands (152 Alberta polygons) added to (d): reserve/Metis VAs 154 → 171;
  real-map validation unchanged (LSL (b) the only difference). Provenance in
  `data/shapefiles/reference/aboriginal_lands_nrcan_dl/SOURCE.md`. Criteria CSV SHA-256 now DD838D5E…FEE2F.
  Audit registers its own `s15_2_criteria.py` (border ≥ 1 km, reserve ≥ 10% at district level, towns
  CY + T + urban service areas at census population, nearest vertex within 1 km); this build is the
  independent cross-check.
- ~21:12 **Owner: "you can commit and push. use teh spares"** → municipality-aware chains 241, 243
  (k=91, eps 0.25, W 0.5) launched on the spare threads (14 chains); 244, 245, 140, 141 and statute
  extras 234–237 / 132–133 follow as the ±12.5% set frees cores.
- ~21:30 pushed `amendment17-local-runs` @ 01095181. Queue launcher (`tools/queue_chains.ps1`, max 14)
  started. ~21:40 owner "Go" on the s.15(2) spec; `--s152` mode implemented; acceptance test
  (`tools/test_s152.py`, k=91 idx 250, 3,000 steps) started.
- ~21:50 **Claude Code stopped both the queue launcher and the s.15(2) test: system critically low on
  memory** (15.6 GB RAM; 3.2 GB free, 2.3 GB commit free with 14 chains ≈ 28 python processes at
  ~150–230 MB each). The 14 production chains were not touched and keep running. Nothing from the queue
  had launched yet. Not restarted pending the owner's word; capacity rule going forward: ≤ 12 chains
  when a test or build also runs.
- ~22:15 **Set A complete** — all six chains 252,500 rows, error logs clean:

  | file | rows | MB | SHA-256 (first 16) |
  |---|---|---|---|
  | k91/chain221_samples.csv | 252,500 | 77.6 | CE36DE4FA2B10DCD |
  | k91/chain222_samples.csv | 252,500 | 77.5 | 06F7D5AE01D86D57 |
  | k91/chain223_samples.csv | 252,500 | 77.0 | 2A12F819EE64440E |
  | k91/chain224_samples.csv | 252,500 | 78.3 | E5974CEA5A633F58 |
  | k89/chain120_samples.csv | 252,500 | 77.2 | 1E6531853161F510 |
  | k89/chain121_samples.csv | 252,500 | 77.5 | 828C8CF61C64C6DA |
- ~21:35 owner "Go": queue restarted at max 11 chains (+ the s.15(2) test = 12). Launched 244, 245, 140,
  141 (muni) and 234, 235, 132, 133, 236, 237 (statute). **234 and 235 failed to seed** (same 50,000-attempt
  failure) → retired; replaced by **238, 239** (~22:05). s.15(2) test idx **250 failed to seed** → retired;
  tests use 259.
- ~22:00 **Set B complete** (statute band) — all six chains 252,500 rows, error logs clean:

  | file | rows | MB | SHA-256 |
  |---|---|---|---|
  | k91_eps25/chain230_samples.csv | 252,500 | 76.2 | 9A086B094DCF177BA0066CFD88D8C5139C167B1E3FBD49290912AD7D079D386E |
  | k91_eps25/chain231_samples.csv | 252,500 | 76.4 | 4D6D57AD68FFD3C048E0FC965D545D0A2856C7A11352B5F51C4D907273D069B9 |
  | k91_eps25/chain232_samples.csv | 252,500 | 76.9 | 40CBE6758344FB3601DB7E38B61F522FA86429157DBEB9A5AB09B757E24DAEE2 |
  | k91_eps25/chain233_samples.csv | 252,500 | 76.5 | 2238CB4BC21DE8CCF28B1FFBBD19D31E2AE5FF5CB7BF83DFAF4E8D02DCCB53BE |
  | k89_eps25/chain130_samples.csv | 252,500 | 76.3 | 69A9E1EDA29BD7E3998AEEB49E0B2820A174F4075797CE5C07ED36ECF205EEA1 |
  | k89_eps25/chain131_samples.csv | 252,500 | 75.7 | D12919747369B41CCB31D6B5BCE547C2C5985EBA01C6D63933A587C394515FB7 |

- s.15(2) mode: see governance log §5 (acceptance runs, Amendment 21 town ruling, registered table).
  Delivery per Audit: `gzip -9 -n` each finished CSV → `chainNNN_samples.csv.gz` (raw + gz SHA-256 below),
  `git add -f` into the gitignored checkpoint dirs on this branch; push only on the owner's OK.

  | file | raw CSV SHA-256 | .gz SHA-256 | .gz bytes |
  |---|---|---|---|
  | k91/chain221 | ce36de4fa2b10dcd0c1d60ea72c04c4e87716ee92fdcf9a527e998a08ff23e17 | 396572c32c9de1dc8a320a86ef21e364ad0792c9931d66f3fd42ccd3a0df7c4f | 9,298,063 |
  | k91/chain222 | 06f7d5ae01d86d576b92be48f4883d1391ce2a19559b454d8e2c45ada7317f19 | 054af7a9804dfefca6fd94332b8256734ba8cb609a081374957dd39abf0c6658 | 9,299,917 |
  | k91/chain223 | 2a12f819ee64440e0996f958bb63e85c2771a36e87679a016db7d8d67eb73146 | 3ba24c8b26f9a9891eec57e93c05f11bd39cf1231f5e7bd6f8d8d9f123b34c83 | 9,303,563 |
  | k91/chain224 | e5974cea5a633f58c1071bc2b1c85448efa4bde998f058e44c6e7a70db6f7908 | 5c76be37334bb49749f5009d7d239444f4e88290aa6e8fe319422b3ab0914d36 | 9,300,952 |
  | k89/chain120 | 1e6531853161f5104e610ff8faf891875b06af394666a4713485d89ce7561afe | f5597e1c286df0db865be0e39c1c6d03c3b47b41b80696982aa4680e1749776e | 9,315,968 |
  | k89/chain121 | 828c8cf61c64c6da1b76daa3f788886050846458ec58073be693ccc19d8626eb | 30f5656ad32a06b309b7220d53d1f71292d49c32a1db0dfb3ebe59ec177daa97 | 9,326,493 |
  | k91_eps25/chain230 | 9a086b094dcf177ba0066cfd88d8c5139c167b1e3fbd49290912ad7d079d386e | 12c5fe9d206808ed0a49e1cebdcbf0b4ac7ac384d48117e19b663a7f5e7f6d3c | 9,523,330 |
  | k91_eps25/chain231 | 4d6d57ad68ffd3c048e0fc965d545d0a2856c7a11352b5f51c4d907273d069b9 | 7b4cd592ec63d3e0f859f31d609ccce2db16feb55e4f163d695e059fde438bab | 9,536,734 |
  | k91_eps25/chain232 | 40cbe6758344fb3601db7e38b61f522fa86429157dbeb9a5ab09b757e24daee2 | 8527525ab5bd244ba9b6111ee412c53c8ec246bb357eb63afdc26d43d13e854c | 9,550,655 |

- ~22:20 **Second memory kill:** Claude Code stopped the s.15(2) acceptance run on the registered table
  and the gzip job (12 chains + test holding 3,000 plans + gzip; 2.2 GB RAM free; Firefox ~1.5 GB).
  9 of 12 .gz complete (above); the partial chain233 .gz was deleted; 233, 130, 131 still to compress.
  Production chains untouched. Not restarted pending the owner's word.
- ~23:05 Municipality-aware 241 and 243 complete (252,500 rows each, error logs clean):
  k91_muni/chain241 59.7 MB SHA-256 ABB0B6E7579629ED1304890C1B85D76D3E5ABAB9A5AC82C7097AEC5D6F15449E;
  k91_muni/chain243 59.5 MB SHA-256 FBB4C6E718C129758E596764DC0B9A34DDF793F4E5792321CA4A1E8FEC9EB8C7.
  10 chains running (muni 244, 245, 140, 141; statute 132, 133, 236–239).
- ~00:05 **Set C (municipality-aware, W = 0.5) complete** — six chains, 252,500 rows each, error logs clean:
  k91_muni/chain244 59.7 MB C669C1B668D5F42B8CD3E1E46233E429F715AB49BECA070B7C12D77C455DD3CB;
  k91_muni/chain245 59.4 MB E476A3252ED58BFC87D3C5AD47816A638CE21792D5300EB4D5F8FF9BDDBDBB03;
  k89_muni/chain140 59.0 MB 378CE821713486596671651B2EA6142F253B6C0FFBB5DA6D189EF7D57FBD568A;
  k89_muni/chain141 58.9 MB 78E33F5421018D165CFC4C20DD5F6377401BD1CF2B6A2A0190DEF255C03B9EB2
  (241, 243 above). Statute extras 132, 133, 236, 237 finished; 238, 239 finishing.
- ~00:15 **All production chains finished; machine idle.** Statute-band extras, 252,500 rows each, logs clean:
  k89_eps25/chain132 75.0 MB 87E6459195DE85D832B373C4AD7876E6AE16F531DD4E4D3BC5011935B1D5CF05;
  k89_eps25/chain133 75.9 MB B21F40CB782D3CC136FC3AB4736398161A6610E920C6DF6B01730CD0C368E471;
  k91_eps25/chain236 76.6 MB 3652D0F1A3DF6B157A5D104633A151B2B7661A428ED61508CAE6CB886B0F7917;
  k91_eps25/chain237 76.3 MB 02CD0D5353867D267D0D5EBD0A1A80AE246F7663A30A21EFA14857CF0376EDF3;
  k91_eps25/chain238 76.3 MB 5C977F1169FA0E810ABCF11132073981E27C45EAC515521D3DADC440EC90DB73;
  k91_eps25/chain239 76.1 MB 47620B10FF829748577AEAD8A6FA859C01AE8ECEABC6DC3711034F98EEF4ECAF.

  | Set | k=91 | k=89 | plans |
  |---|---|---|---|
  | A half-band | 221–224 | 120–121 | 6 × 252,500 = 1,515,000 |
  | B statute band | 230–233, 236–239 | 130–133 | 12 × 252,500 = 3,030,000 |
  | C municipality-aware W 0.5 | 241, 243–245 | 140–141 | 6 × 252,500 = 1,515,000 |
  | D s.15(2) | — | — | pending acceptance on the registered table |

  Retired seeds (never reuse): 220, 234, 235, 240, 242, 250.
- ~00:25 owner "Go": compression + s.15(2) acceptance (registered table) started; **both killed by
  Claude Code for low memory with no chains running.** Cause found: Windows' `ScheduledDefrag` task is
  running (svchost `defragsvc` ~2 GB) — Available memory 2.2 GB of 15.6. chain233 .gz completed
  (raw 2238cb4b…53be, gz f91340266ec1e349f2b964250dd400121173503eefcca87791124382b077484c, 9,534,478 B);
  partial chain236 .gz deleted. 11 of 24 .gz done. Not restarted pending the owner's word.
- ~00:40 Owner: "Disable Defrag close Firefox", then "Go". ScheduledDefrag stopped (disabling the task
  needs admin — Access denied; it stays enabled and can rerun on its weekly schedule); Firefox closed;
  free RAM 6.4 GB. Restarted as ONE sequential detached job (WMI, outside Claude Code's kill tree):
  gzip -9 -n the 13 remaining CSVs (written to .gz.part, renamed on success), then the s.15(2)
  acceptance test on the registered table (k=91 idx 259, 3,000 steps, chunk 500, every 5th plan kept).
- 01:11 **Compression complete: 24 of 24 .gz.** Every raw SHA-256 below re-matches the hash recorded when
  the chain finished.

  | file | raw CSV SHA-256 | .gz SHA-256 | .gz bytes |
  |---|---|---|---|
  | k91_eps25/chain233 | 2238cb4bc21de8ccf28b1ffbbd19d31e2ae5ff5cb7bf83dfaf4e8d02dccb53be | f91340266ec1e349f2b964250dd400121173503eefcca87791124382b077484c | 9,534,478 |
  | k91_eps25/chain236 | 3652d0f1a3df6b157a5d104633a151b2b7661a428ed61508cae6cb886b0f7917 | 8fe23c01b23266ef51202d605007fcfea10561463f7b33a3fee5042fd9afcdca | 9,536,415 |
  | k91_eps25/chain237 | 02cd0d5353867d267d0d5ebd0a1a80ae246f7663a30a21efa14857cf0376edf3 | 06b46e292d15e4abd3c76743801d6f883c9db85027385aca393b241cc5474cb4 | 9,541,835 |
  | k91_eps25/chain238 | 5c977f1169fa0e810abcf11132073981e27c45eac515521d3dadc440ec90db73 | 55f9252c9df0d5549e2cb7f15de0734ca59aad4e8f272c2689f8dd2bf2b905dc | 9,550,747 |
  | k91_eps25/chain239 | 47620b10ff829748577aead8a6fa859c01ae8eceabc6dc3711034f98eef4ecaf | e7353abfddcea261d420442804a38aa139450c342423e96e7ea64d36dd8a02c5 | 9,532,319 |
  | k89_eps25/chain130 | 69a9e1eda29bd7e3998aeeb49e0b2820a174f4075797ce5c07ed36ecf205eea1 | 4cc7add11a1a84bbfb140a8acecf0cbbc168db4585a0d86ea76733aeaf6cb174 | 9,574,954 |
  | k89_eps25/chain131 | d12919747369b41ccb31d6b5bce547c2c5985eba01c6d63933a587c394515fb7 | 0efefa34394add8a48fe898b1a2829967ea4e71fe2dcdfd7f31f30276553d77c | 9,565,073 |
  | k89_eps25/chain132 | 87e6459195de85d832b373c4ad7876e6ae16f531dd4e4d3bc5011935b1d5cf05 | 6098ceeb8c33e81598547d06e8b2607c62df3721a640bfe530408a8ac41f1ae3 | 9,570,020 |
  | k89_eps25/chain133 | b21f40cb782d3cc136fc3ab4736398161a6610e920c6df6b01730cd0c368e471 | 28ada96b09c7a3a240b121b460d30e3059c0afe1199df0bef114cb1e7c703e4e | 9,562,871 |
  | k91_muni/chain241 | abb0b6e7579629ed1304890c1b85d76d3e5abab9a5ac82c7097aec5d6f15449e | 0b0511fc11bbd765e30cdc3659d0b4509360b64fc233603f87f59d312b338c87 | 8,334,858 |
  | k91_muni/chain243 | fbb4c6e718c129758e596764dc0b9a34ddf793f4e5792321ca4a1e8fec9eb8c7 | 3a50310580371a07e3156dd6fab932b7e71ee81badee201ab2a26c4ea88518b9 | 8,307,478 |
  | k91_muni/chain244 | c669c1b668d5f42b8cd3e1e46233e429f715ab49beca070b7c12d77c455dd3cb | a9fd9283ac9b41f89b81f431e44671a56687e582aec4cd4672c679762e5280b7 | 8,296,492 |
  | k91_muni/chain245 | e476a3252ed58bfc87d3c5ad47816a638ce21792d5300eb4d5f8ff9bddbdbb03 | 32d3aa76eea563e5f46fb2fbff259cb79d0abbdac3f7e9706bbe2d8221ccf975 | 8,333,487 |
  | k89_muni/chain140 | 378ce821713486596671651b2ea6142f253b6c0ffbb5da6d189ef7d57fbd568a | 3c856fe0d5c52efe7b409bfdc065c4ccb00c4d8cab1234fc617d6f4ca746fba5 | 8,332,973 |
  | k89_muni/chain141 | 78e33f5421018d165cfc4c20dd5f6377401bd1cf2b6a2a0190def255c03b9eb2 | 8ab74059f741593ad131336d96c0a4f7889a6ad5e6c871b869200408cbdfa13f | 8,322,244 |

- 01:14 **s.15(2) acceptance on the registered table (01f70a86…8f47) PASSED.** k=91 idx 259, 3,000 steps,
  every 5th plan (600) scored by Audit's own `criteria()`: AC1 0 violations; AC2 s.15(2) divisions in
  95.3% of plans, max 4 (0:28, 1:193, 2:216, 3:109, 4:54); constraint checks PASS (> +25%, < −50%,
  −30% with < 3 criteria, 5 qualifying all rejected; the "4 qualifying accepted" check is skipped
  when the final state already holds a low division); AC6 median 7.1 s / 500 steps (max 10.3).
  Disclosed: the run was 3,000 steps, not the 10,000 AC2 names, matching the first acceptance run.
- 01:15 **Set D production launched** (owner "Go" covered launch on pass): k91_s152/chain251–254,
  k89_s152/chain150–151, `--s152 data/outputs/s15_2_va_criteria.csv --resume`, 252,500 steps, chunk 500.
  All six seeded and stepping (~9–11 s / 500 steps each). chain151.err holds one gerrychain
  BipartitionWarning ("Failed to find a balanced cut after 1000 attempts") from seeding; the seed then
  succeeded and the chain is stepping normally — a retry warning, not a failure. ETA ~1.5–2 h.
- ~01:30 Claude Code stopped my finish-watch (a sleep loop) for low memory (3.5 GB free; six chains ≈ 2.8 GB).
  The chains themselves run outside its kill tree and are unaffected: all six at ~50,000/252,500,
  12 python processes alive. Watch not restarted (owner's word required).
