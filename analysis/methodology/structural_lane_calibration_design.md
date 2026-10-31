> **Backward:**
> - `preregistration/november_2026_scoring_spec.md` §3 — the two lanes and the 2×2 verdict
> - `findings/pre_registration_amendment_log.md` — Amendments 9 (structural midpoints), 17, 20, 21, 23 and 24
> - `analysis/scripts/calibration_sample_plans.py` — samples the neutral plans
> - `analysis/scripts/structural_lane_calibration.py` — scores them
>
> **Forward:**
> - `findings/structural_lane_calibration_2026-10-31.md` — results (91 districts; 89 and 87 to follow)
> - the November verdict write-up, which reports these rates beside the 2×2

# Calibrating the November verdict on neutral maps: design, method, rationale, timeline

**Written:** 2026-10-31, about 09:30 MDT (Alberta time); plain terms and placements added 09:36 MDT; words, cities-as-towns and unneeded splits added 09:55 MDT. **Status:** calibration, not a registered test. It changes no rule, threshold or verdict. Amendment 24's 2×2 stands as registered.

## Plain terms

- **Computer-drawn ("neutral") map.** A map a computer draws by one rulebook: every district in one piece, every population inside the rulebook's limits. It never sees votes, parties or who holds a seat. Neutral means nobody is steering. It does not mean ideal, and it does not mean what the Act asks for.
- **Sets A–D.** The same computer with four rulebooks. A keeps populations within ±12.5% of average. B allows the Act's full ±25%. C also tries to keep towns whole. D allows up to four large special districts under s.15(2). All four are built to stay inside the Act's population limits.
- **A flag "fires".** Each structural flag is a line drawn halfway between the two commission maps. A map fires it by landing past that line on the minority's side. Firing is not breaking the law.
- **Why computer maps fire.** The computer only follows its rulebook. It does not weigh what s.14 lets a commission weigh, such as municipalities (s.14(b)) and clear boundaries (s.14(e)). Both commission maps have more equal populations and more boundary on town and county lines than every computer-drawn map. The halfway line sits between two maps that are both outside the computer's range, so computer maps land on the minority's side of it. They fire because they sit further out than both commission maps, not because they resemble the minority.
- **Words used.** Equal populations: how close districts are to the same size. Unneeded splits: a municipality split when its population did not require it, which is how a community gets cracked. Boundaries on municipal lines: how much of a map's boundary follows town, city and county limits. No single word sums these up, and none of them says whether a map favours a party. The partisan lane checks that.
- **Cities counted as towns.** The audit counts cities as towns in two places. Neither changes how the three real maps (2019, majority, minority) compare:
  - **s.15(2)(c)** (Amendment 21). Read by legal status alone, "town" would make two Medicine Hat districts on each map, and one Tsuut'ina Calgary district on each 2026 map, eligible to sit 50% under. All of them sit above the average population (+1.4% to +18.5% on 2021 census figures), so none uses the allowance. The districts more than 25% under that meet three criteria hold no city. Two majority districts, Calgary-North East and Calgary-South East, are also more than 25% under on 2021 figures (growth areas the census predates), but they meet one criterion under the audit's reading and two under the legal-status reading, so they are not eligible either way. The reading only stops set D's computer from shrinking a city district to half size, which no Alberta commission has done.
  - **S2** (Amendment 9) counts every split city, town and specialized municipality. That includes the 10 too big for one legal district: Airdrie, Calgary, Edmonton, Grande Prairie, Lethbridge, Medicine Hat, Red Deer, St. Albert, Strathcona County and Wood Buffalo. Every map, real or computer-drawn, splits all 10, so they add the same count to each.

## 1. Rationale

The November verdict combines two lanes (spec §3):

- **Structural lane.** Five discriminating flags (S1–S3, S5, S6), each with a threshold set midway between the majority and minority commission maps (Amendment 9). "Replicated" means three or more fire.
- **Partisan lane.** P1–P4 placed against the 1,010,000-plan, 87-district canonical ensemble. "Present" means two or more fire in the UCP direction.

Neither lane's rate on neutral maps had been measured, so there was no way to weigh a "replicated" or "present" result. Three things raised the question:

- Amendment 9 records S1 firing on 25.7% of neutral plans by itself.
- A dry run on a synthetic 91-district plan tripped both lanes. That plan was later shown not to be a neutral draw.
- The partisan lane measured 4.8–8.3% on the size-matched neutral sets (`findings/size_matched_results_2026-10-30.md`).

**The author's two decisions, in session:**

1. **Measure, don't move** (option 1, 2026-10-31, after 01:20 and before 01:31 MDT). Measure both lanes on neutral maps and report the rates beside the verdict. Don't change thresholds or add a lane two days before the map. The options weighed were: measure; measure plus a reporting rule; add a third lane; rebalance thresholds.
2. **Match sizes** (2026-10-31, about 09:20 MDT: "Why not just match 89 to 89 and 91 to 91?"). Calibrate each map against neutral maps with its own number of districts.

## 2. Design

| Size | What it calibrates | Kernel | Chains | Plans | Status |
|---|---|---|---|---|---|
| 91 | The November map | Set D: s.15(2), Amendment 23 rule | 290, 291, 293, 295 (292 and 294 failed to seed) | 200 | Complete |
| 89 | The two 2026 commission maps | Set D | 190–193 | 200 | Sampling since 09:25 MDT |
| 87 | The registered headline's null, and the 2019 map | Canonical: ±12.5% proposal band, no s.15(2) mode | 300 and up | 200 | Queued after the 89 run |

- **Kernels.** Set D is the primary size-matched set (Amendment 24), so it is used at 89 and 91. At 87 the canonical kernel is used because it is the null the registered partisan comparison uses. The two kernels differ, and their results are reported side by side, not pooled.
- **Sampling.** Each chain starts from a `recursive_tree_part` seed. Seeds use the Amendment 17 formula: (base seed × 100,000 + index × 1,000) mod 2³². After 10,000 burn-in steps, the chain keeps one plan every 2,500 steps, 50 plans per chain. A chain that fails to seed is replaced by the next index, which has happened before for indices 220, 240, 242 and 250.
- **Spacing.** On the size-matched sets, most measures decorrelate over a few hundred to a few thousand steps. Spacing plans 2,500 steps apart reduces that dependence but does not remove it.
- **Separate indices.** Calibration indices (190s, 290s, 300s) sit outside every registered block (A 220s/120s, B 230s/130s, C 240s/140s, D 250s/150s), so calibration output can't be mistaken for registered output.

## 3. Method

**Sampler.** `close_seats_ensemble.py` at `amendment17-local-runs@2994113c` (SHA-256 `2e75ca758a3071bf713084912d93188b48b89ef6d667476d4a4a84ec2a014316`). This is the code the size-matched sets ran. `calibration_sample_plans.py` loads it with only its repository path changed and saves each kept plan's assignment. The runs themselves used a session copy with the same one-line change; checked at 09:32 MDT, the committed script reproduced the first 1,000 steps of live chain 190 row for row.

- At 89 and 91 it runs with the production set-D options: s.15(2) mode on the Amendment 23 table (SHA-256 `48c928b8…2fafc`).
- At 87 it runs with the canonical options.
- Each chain also writes its usual per-step CSV, which supplies the partisan lane.

**Structural lane.** `run_structural_battery.py` runs unchanged on each plan. The plan's districts are the VA polygons dissolved by its assignment, named N01, N02 and so on.

- **S6 limit.** S6 reads district names, such as "Airdrie" in three or more districts, or "Cochrane" together with "Calgary". It cannot fire on unnamed plans, so the registered count is a lower bound.
- **Geometric stand-in for S6.** Reported beside the registered count, it replaces names with where each place's people fall:
  - P1 and P5: Airdrie or Red Deer is split into three or more districts. A district counts when it holds at least 2% of the city's people, the piece rule from Amendment 17.
  - P2–P4: a district has at least 10% of its people in Calgary and at least 10% in Cochrane, Chestermere or Rocky View County. The 10% cut is this calibration's choice.
  - It flags at three or more hits, the registered S6 rule.
- **Validation of the stand-in.** On the commission maps it agrees with the registered S6: the majority gets 0 hits and no flag; the minority gets 4 hits and a flag (the registered S6 counts 5, so the stand-in misses the Chestermere–Calgary hybrid).

**Partisan lane.** Taken from each plan's chain row, scored as spec §3 sets it:

- P1: efficiency gap of 4.10% or more.
- P2–P4: mean-median, declination and seats at 50/50 at or above the 95th percentile of the canonical ensemble, in the UCP direction.
- "Present" means two or more fire.

**Aggregation.** Each rate is reported with a Wilson 95% interval. Each map is compared with the neutral plans of its own size.

## 4. Timeline (Alberta time, MDT)

| When | What | Record |
|---|---|---|
| 2026-10-30 19:10 | Size-matched results committed; partisan lane measured at 4.8–8.3% on neutral maps | `2ecd7931` |
| 2026-10-31 01:20 | PR #37 merged | `f530a9b1` |
| after 01:20, before 01:31 | The author chooses option 1 | session |
| 01:31–02:20 | 91-district plans sampled; chains 292 and 294 fail to seed, 295 replaces them | chain logs |
| 01:32 | Calibration script committed | `d2c38904` |
| 01:57–03:57 | First scoring pass, 86 plans; stopped by the 2-hour job limit | scoring log |
| 03:58–05:56 | Second pass, the remaining 114 plans | scoring log |
| 05:58 | 91-district results committed | `9f193b35` |
| 09:15 | Merged as PR #41 | `eb1c38ac` |
| about 09:20 | The author asks for size matching | session |
| 09:25 | 89-district sampling starts (chains 190–193); 87 queued behind it | chain logs |
| about 09:30 | Partisan lane on the canonical 87-district ensemble: 5.9% present | this file |

## 5. Results so far

- **91 districts** (`findings/structural_lane_calibration_2026-10-31.md`):
  - structural "replicated": 93.5% (registered battery); 100% (with the S6 stand-in);
  - partisan "present": 8.5%;
  - both lanes: 7.5%.
- **87 districts, partisan lane only.** On the canonical ensemble's 1,010,000 plans:
  - two or more flags: 5.9%;
  - three or more: 0.25%;
  - all four: 0.02%.
- **Where the two commission maps sit among the 91-district computer maps** (200 plans, set D; battery outputs per plan). The commission maps have 89 districts, so this is a size-mismatched first look; the 89-district run replaces it.

  | Measure | Computer maps: lowest – median – highest | Minority | Majority |
  |---|---|---|---|
  | S1 population spread (MAD; lower is more equal) | 4,637 – 6,192 – 7,624 | 3,938: more equal than all 200 | 2,827: more equal than all 200 |
  | S3 share of boundary on town and county lines | 38.5% – 44.0% – 47.5% | 72.0%: above all 200 | 80.1%: above all 200 |
  | S2 towns split | 24 – 31 – 41 | 30: 41.5% of computer maps split 30 or fewer | 23: fewer than all 200 |
  | S5 neighbour drain | 0 – 0.0050 – 0.0454 | 0.0006: 12% at or below | 0.0072: 37% at or above |

  S6 reads district names and cannot be placed.

  The registered S2 counts land: any 5 hectares of a municipality in a second district is a split. Counted by people instead (a split needs a second district holding at least 2% of the municipality's people, Amendment 17's piece rule), at voting-area resolution, and leaving out the 10 municipalities that must be split, the picture changes for the minority:

  | Unneeded splits | 2019 (87 districts) | Majority (89) | Minority (89) | Computer maps (91) |
  |---|---|---|---|---|
  | Count | 0 | 1 (Strathmore) | 7 (Blackfalds, Chestermere, Coaldale, Lac la Biche County, Okotoks, Stony Plain, Sylvan Lake) | 6 – 11 – 16 |
  | Computer maps with as few or fewer | 0 of 200 | 0 of 200 | 15 of 200 | |

  By land the minority's 30 is mid-range among computer maps; by people its 7 is near the low end. The people count is a calibration measure, not the registered S2. Single splits at voting-area resolution can be edge effects and have not been checked on the map. Script `analysis/scripts/calibration_unneeded_splits.py`; output `data/outputs/calibration_unneeded_splits_91_2026-10-31.json`.

  Two cautions: set D allows the Act's widest population range, so its spread is wide partly by design, and set A would be tighter; and computer maps are built from voting-area blocks, which may hold down their share of boundary on town and county lines. The second has not been tested.
- **89 districts, and the 87-district structural lane:** pending. This file and the findings file will be updated when they land.

## 6. Limits

- **The intervals are too narrow.** Plans 2,500 steps apart in one chain are not independent, and the Wilson intervals treat them as if they were.
- **Set D only at 89 and 91.** Sets A (±12.5%) and C (municipality-aware) would lower S1 and S2–S3. Set D is used because it is the primary set.
- **The S6 stand-in is a construction.** The registered S6 cannot be computed on unnamed maps.
- **Different kernels.** The 87-district calibration uses a different kernel from the 89- and 91-district runs, so the sizes are compared with that difference in view.

## 7. Reproduce

```bash
git show 2994113c:analysis/scripts/close_seats_ensemble.py > /tmp/cse_2994113c.py
python analysis/scripts/calibration_sample_plans.py --sampler /tmp/cse_2994113c.py \
  --idx 290 --out <dir> --k 91 --kernel s152          # repeat per chain index
python analysis/scripts/structural_lane_calibration.py --plans <dir> \
  --out-json <file>.json --out-md <file>.md --jobs 4
```
