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
