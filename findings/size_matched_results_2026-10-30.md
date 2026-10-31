> **Backward:**
> - `analysis/scripts/size_matched_results.py` — produces every number here
> - `data/outputs/size_matched_results_2026-10-30.json` — the same results, machine-readable
> - `findings/pre_registration_amendment_log.md` — Amendments 17, 20, 21 and 23 define the sets and the rules
> - `analysis/methodology/amendment17_chain_runs/README.md` (branch `amendment17-local-runs`) — how each chain ran
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.4.9 "Size-matched sets" — to be updated from this file

# Size-matched neutral maps: first results

**Date:** 2026-10-30 19:10 MDT (Alberta time). **Status:** provisional under Amendment 21's rule, as explained below.

## What was run

Four sets of neutral maps, each at 89 and 91 districts, drawn by the canonical ReCom harness:

- **A.** ±12.5% proposal band (Amendment 17).
- **B.** The statute's ±25% band (Amendment 20, set 1).
- **C.** Statute band, municipality-aware, W = 0.5 (Amendment 20 set 2; Amendment 21).
- **D.** Statute band plus the s.15(2) exception, Amendment 23 rule (Amendment 20 set 3). The first set D run is superseded and not used.

Each set has 505,000 to 2,020,000 plans. Set A includes chains 201 and 100, run before the harness fixes. Amendment 20 counts them as valid draws from the same distribution.

The two 2026 commission maps have 89 districts, so they are placed only against the 89-district sets. These placements are baselines. The registered test is the November map's, which will be placed against the sets with its own number of districts.

## How sure the numbers are

Amendment 21 makes a result final only when its pooled effective sample size is at least 400 and the canonical estimator's 2,000-lag cap did not bind on any chain. The cap binds on at least one chain for almost every measure, so almost everything here is **provisional**, and those effective sample sizes are upper bounds. The rule stands as registered.

As a diagnostic only, the same estimator with no lag cap gives these figures at 89 districts:

- **Competitive seats:** 975 to 2,854. Well past 400.
- **Partisan measures:** mostly 650 to 2,500. Seats at 50/50 in set C is lower, at 216.
- **Towns split:** 308 to 1,301.
- **City-versus-rest gap:** 78 to 273. That's too few to place a 95th percentile. This measure needs longer or more chains before it can be read.

## What the 89-district sets show

**Minority map**

- **Competitive seats.** It has 4 districts within 4 points. That's at or below the 5th percentile in all four sets (p0.1 to p0.3), so the registered rule flags it in every set. Between 0.09% and 0.49% of neutral plans have 4 or fewer.
- **Partisan tilt.** Its mean-median is beyond almost every same-size neutral plan. The number of plans at or beyond it is 53 of 541,500 in A, 161 of 1,010,000 in B, 232 of 505,000 in C and 261 of 505,000 in D. Its seats at 50/50 (46 of 89) is matched or beaten by none of A's plans, and by 124, 263 and 905 plans in B, C and D. Declination sits at p98.6 to p99.0, and the efficiency gap at p94 to p96. Against same-size maps under every rule set, the tilt found against the 87-district canonical ensemble holds.
- **City versus rest.** It reads +5.4%. That's flagged against set A (p99.9) but not against B, C or D (p72 to p93). This is the least certain measure.
- **Towns split.** It splits 6 towns beyond their minimum. That's typical of population-only neutral maps (p33 to p48), and beyond every municipality-aware plan in set C (p100), where it's flagged.
- **Population spread (MedAD).** It's at p99.7 against set A and p0.0 against B, C and D. It's wide for maps held to ±12.5%, and narrow for maps allowed the statute's ±25%.

**Majority map**

- **No registered flags.**
- **Competitive seats.** It has 13 districts within 4 points, at p94.8 to p95.7: more close seats than most neutral maps.
- **Partisan measures.**
  - Its mean-median sits at p0.9 to p2.1, on the side that favours the NDP.
  - Seats at 50/50 is at p48 to p70.
  - The efficiency gap is at p16 to p19.
- **Towns split.** It splits none (p0 to p9).
- **Population spread (MedAD).** It's at p21 against set A and p0.0 against B, C and D.

## The registered partisan lane on neutral maps

The November spec scores the committee's map against the 87-district canonical ensemble. To see how often that rule fires on a map with no partisan intent, each neutral plan in sets A to D was scored the same way. The lane counts as "present" when at least 2 of P1–P4 fire in the UCP direction, as spec §3 sets out.

| Set | 89 districts | 91 districts |
|---|---|---|
| A | 4.8% | 4.8% |
| B | 5.8% | 5.7% |
| C | 6.6% | 5.5% |
| D | 8.2% | 8.3% |

The partisan lane's false-positive rate stays near the nominal 5%. It is a little higher in the statute-band sets because P4 (seats at 50/50) fires on 7% to 15% of their plans. The structural lane's rate on neutral maps has not been measured (Amendment 9 records S1 alone firing on 25.7%), so a both-lanes headline is bounded by the partisan figures above.

## Tables

Percentiles are midrank, as in the canonical harness. "(cap)" marks an effective sample size where the lag cap bound, which makes it an upper bound. **flag** marks a registered Amendment 17 flag: towns split and city gap at or above the set's 95th percentile, competitive seats at or below its 5th.

### Set A, 89 districts: ±12.5% proposal band (Amendment 17)

Chains 100, 120, 121.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th | Majority | Minority |
|---|---|---|---|---|---|---|---|---|---|
| towns_flagged | 541,500 | 458 (cap) | provisional | 308 | 4 | 7 | 9 | 0 (p0.0) | 6 (p33.3) |
| city_gap_pct | 541,500 | 275 (cap) | provisional | 162 | -2.7% | -0.2% | +2.5% | -0.7% (p37.2) | +5.4% (p99.9) **flag** |
| close4 | 541,500 | 1,190 (cap) | provisional | 1,123 | 6 | 9 | 13 | 13 (p95.3) | 4 (p0.2) **flag** |
| efficiency_gap | 541,500 | 962 (cap) | provisional | 886 | -0.0083 | +0.0162 | +0.0400 | +0.0010 (p15.8) | +0.0402 (p95.1) |
| mean_median | 541,500 | 810 (cap) | provisional | 674 | -0.0311 | -0.0189 | -0.0052 | -0.0362 (p0.9) | +0.0104 (p100.0) |
| declination | 541,500 | 912 (cap) | provisional | 831 | -0.0530 | +0.0019 | +0.0551 | -0.0267 (p19.9) | +0.0770 (p99.0) |
| seats_at_50_50 | 541,500 | 847 (cap) | provisional | 704 | 42.70% | 44.94% | 48.31% | 46.07% (p69.5) | 51.69% (p100.0) |
| population_mad | 541,500 | 3,244 (cap) | provisional | 3,241 | 2,551 | 3,083 | 3,605 | 2,827 (p21.2) | 3,938 (p99.7) |
| ucp_seats | 541,500 | 778 (cap) | provisional | 699 | 54 | 57 | 59 | 55 (p13.0) | 60 (p99.1) |

### Set A, 91 districts: ±12.5% proposal band (Amendment 17)

Chains 201, 221, 222, 223, 224.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th |
|---|---|---|---|---|---|---|---|
| towns_flagged | 1,057,500 | 936 (cap) | provisional | 740 | 4 | 7 | 9 |
| city_gap_pct | 1,057,500 | 507 (cap) | provisional | 274 | -2.5% | +0.0% | +2.6% |
| close4 | 1,057,500 | 1,977 (cap) | provisional | 1,839 | 6 | 10 | 13 |
| efficiency_gap | 1,057,500 | 1,952 (cap) | provisional | 1,846 | -0.0088 | +0.0157 | +0.0399 |
| mean_median | 1,057,500 | 1,631 (cap) | provisional | 1,518 | -0.0307 | -0.0189 | -0.0058 |
| declination | 1,057,500 | 1,802 (cap) | provisional | 1,681 | -0.0492 | +0.0015 | +0.0543 |
| seats_at_50_50 | 1,057,500 | 1,366 (cap) | provisional | 866 | 42.86% | 45.05% | 48.35% |
| population_mad | 1,057,500 | 5,465 | final | 5,465 | 2,497 | 3,008 | 3,521 |
| ucp_seats | 1,057,500 | 1,560 (cap) | provisional | 1,334 | 56 | 58 | 60 |

### Set B, 89 districts: statute band, ±25% (Amendment 20, set 1)

Chains 130, 131, 132, 133.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th | Majority | Minority |
|---|---|---|---|---|---|---|---|---|---|
| towns_flagged | 1,010,000 | 1,428 (cap) | provisional | 1,301 | 4 | 6 | 8 | 0 (p0.0) | 6 (p45.0) |
| city_gap_pct | 1,010,000 | 488 (cap) | provisional | 273 | -4.8% | +0.4% | +6.0% | -0.7% (p37.0) | +5.4% (p93.0) |
| close4 | 1,010,000 | 2,854 | final | 2,854 | 6 | 10 | 13 | 13 (p94.8) | 4 (p0.2) **flag** |
| efficiency_gap | 1,010,000 | 2,581 (cap) | provisional | 2,519 | -0.0104 | +0.0155 | +0.0413 | +0.0010 (p17.8) | +0.0402 (p94.2) |
| mean_median | 1,010,000 | 2,172 (cap) | provisional | 2,102 | -0.0310 | -0.0187 | -0.0050 | -0.0362 (p1.1) | +0.0104 (p100.0) |
| declination | 1,010,000 | 2,386 (cap) | provisional | 2,315 | -0.0563 | -0.0009 | +0.0567 | -0.0267 (p22.5) | +0.0770 (p98.8) |
| seats_at_50_50 | 1,010,000 | 1,374 (cap) | provisional | 1,256 | 42.70% | 44.94% | 48.31% | 46.07% (p66.3) | 51.69% (p100.0) |
| population_mad | 1,010,000 | 5,482 | final | 5,482 | 5,166 | 6,249 | 7,309 | 2,827 (p0.0) | 3,938 (p0.0) |
| ucp_seats | 1,010,000 | 1,698 (cap) | provisional | 1,425 | 54 | 57 | 59 | 55 (p16.0) | 60 (p98.7) |

### Set B, 91 districts: statute band, ±25% (Amendment 20, set 1)

Chains 230, 231, 232, 233, 236, 237, 238, 239.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th |
|---|---|---|---|---|---|---|---|
| towns_flagged | 2,020,000 | 3,202 (cap) | provisional | 3,054 | 4 | 6 | 9 |
| city_gap_pct | 2,020,000 | 1,004 (cap) | provisional | 554 | -4.3% | +0.6% | +5.8% |
| close4 | 2,020,000 | 5,489 (cap) | provisional | 5,384 | 6 | 10 | 13 |
| efficiency_gap | 2,020,000 | 4,894 (cap) | provisional | 4,882 | -0.0105 | +0.0154 | +0.0407 |
| mean_median | 2,020,000 | 4,432 (cap) | provisional | 4,203 | -0.0309 | -0.0189 | -0.0051 |
| declination | 2,020,000 | 4,423 (cap) | provisional | 4,400 | -0.0546 | +0.0003 | +0.0574 |
| seats_at_50_50 | 2,020,000 | 2,864 (cap) | provisional | 2,542 | 42.86% | 45.05% | 48.35% |
| population_mad | 2,020,000 | 12,124 | final | 12,124 | 5,077 | 6,117 | 7,139 |
| ucp_seats | 2,020,000 | 3,055 (cap) | provisional | 2,356 | 56 | 58 | 60 |

### Set C, 89 districts: municipality-aware, W = 0.5 (Amendment 20 set 2; Amendment 21)

Chains 140, 141.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th | Majority | Minority |
|---|---|---|---|---|---|---|---|---|---|
| towns_flagged | 505,000 | 866 (cap) | provisional | 621 | 0 | 1 | 3 | 0 (p9.0) | 6 (p100.0) **flag** |
| city_gap_pct | 505,000 | 190 (cap) | provisional | 78 | -2.4% | +2.0% | +6.7% | -0.7% (p16.1) | +5.4% (p87.8) |
| close4 | 505,000 | 1,023 (cap) | provisional | 975 | 7 | 10 | 13 | 13 (p95.7) | 4 (p0.1) **flag** |
| efficiency_gap | 505,000 | 1,058 (cap) | provisional | 903 | -0.0102 | +0.0151 | +0.0391 | +0.0010 (p18.0) | +0.0402 (p95.8) |
| mean_median | 505,000 | 720 (cap) | provisional | 657 | -0.0330 | -0.0206 | -0.0049 | -0.0362 (p2.1) | +0.0104 (p100.0) |
| declination | 505,000 | 854 (cap) | provisional | 721 | -0.0524 | +0.0012 | +0.0565 | -0.0267 (p20.5) | +0.0770 (p98.7) |
| seats_at_50_50 | 505,000 | 524 (cap) | provisional | 216 | 43.82% | 46.07% | 48.31% | 46.07% (p47.9) | 51.69% (p100.0) |
| population_mad | 505,000 | 1,773 | final | 1,773 | 5,237 | 6,328 | 7,410 | 2,827 (p0.0) | 3,938 (p0.0) |
| ucp_seats | 505,000 | 543 (cap) | provisional | 293 | 54 | 57 | 59 | 55 (p15.4) | 60 (p99.0) |

### Set C, 91 districts: municipality-aware, W = 0.5 (Amendment 20 set 2; Amendment 21)

Chains 241, 243, 244, 245.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th |
|---|---|---|---|---|---|---|---|
| towns_flagged | 1,010,000 | 1,512 (cap) | provisional | 1,166 | 0 | 2 | 3 |
| city_gap_pct | 1,010,000 | 343 (cap) | provisional | 96 | -2.1% | +2.8% | +7.9% |
| close4 | 1,010,000 | 2,344 (cap) | provisional | 2,183 | 7 | 10 | 13 |
| efficiency_gap | 1,010,000 | 2,325 (cap) | provisional | 2,299 | -0.0106 | +0.0143 | +0.0379 |
| mean_median | 1,010,000 | 1,498 (cap) | provisional | 1,080 | -0.0333 | -0.0207 | -0.0051 |
| declination | 1,010,000 | 2,078 (cap) | provisional | 1,798 | -0.0533 | -0.0021 | +0.0500 |
| seats_at_50_50 | 1,010,000 | 935 (cap) | provisional | 522 | 43.96% | 46.15% | 48.35% |
| population_mad | 1,010,000 | 3,878 (cap) | provisional | 3,693 | 5,172 | 6,226 | 7,255 |
| ucp_seats | 1,010,000 | 1,284 (cap) | provisional | 775 | 55 | 58 | 60 |

### Set D, 89 districts: s.15(2), Amendment 23 rule (Amendment 20 set 3)

Chains 150, 151.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th | Majority | Minority |
|---|---|---|---|---|---|---|---|---|---|
| towns_flagged | 505,000 | 706 (cap) | provisional | 601 | 4 | 6 | 8 | 0 (p0.0) | 6 (p47.5) |
| city_gap_pct | 505,000 | 246 (cap) | provisional | 158 | -2.1% | +3.4% | +9.0% | -0.7% (p10.9) | +5.4% (p71.7) |
| close4 | 505,000 | 1,432 (cap) | provisional | 1,422 | 6 | 9 | 13 | 13 (p95.7) | 4 (p0.3) **flag** |
| efficiency_gap | 505,000 | 1,131 (cap) | provisional | 1,030 | -0.0118 | +0.0148 | +0.0400 | +0.0010 (p19.1) | +0.0402 (p95.1) |
| mean_median | 505,000 | 1,077 (cap) | provisional | 1,031 | -0.0307 | -0.0179 | -0.0030 | -0.0362 (p0.9) | +0.0104 (p100.0) |
| declination | 505,000 | 1,039 (cap) | provisional | 879 | -0.0546 | +0.0005 | +0.0563 | -0.0267 (p21.0) | +0.0770 (p98.6) |
| seats_at_50_50 | 505,000 | 714 (cap) | provisional | 633 | 43.82% | 46.07% | 48.31% | 46.07% (p51.7) | 51.69% (p99.9) |
| population_mad | 505,000 | 3,594 | final | 3,594 | 5,314 | 6,415 | 7,498 | 2,827 (p0.0) | 3,938 (p0.0) |
| ucp_seats | 505,000 | 726 (cap) | provisional | 571 | 55 | 57 | 59 | 55 (p10.4) | 60 (p97.6) |

### Set D, 91 districts: s.15(2), Amendment 23 rule (Amendment 20 set 3)

Chains 251, 252, 253, 254.

| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th |
|---|---|---|---|---|---|---|---|
| towns_flagged | 1,010,000 | 1,652 (cap) | provisional | 1,574 | 4 | 6 | 9 |
| city_gap_pct | 1,010,000 | 523 (cap) | provisional | 281 | -1.7% | +3.5% | +8.6% |
| close4 | 1,010,000 | 2,615 (cap) | provisional | 2,526 | 6 | 10 | 13 |
| efficiency_gap | 1,010,000 | 2,250 (cap) | provisional | 2,225 | -0.0110 | +0.0153 | +0.0408 |
| mean_median | 1,010,000 | 1,729 (cap) | provisional | 1,616 | -0.0305 | -0.0182 | -0.0032 |
| declination | 1,010,000 | 2,238 (cap) | provisional | 2,227 | -0.0542 | +0.0013 | +0.0585 |
| seats_at_50_50 | 1,010,000 | 1,354 (cap) | provisional | 1,201 | 42.86% | 46.15% | 48.35% |
| population_mad | 1,010,000 | 7,216 | final | 7,216 | 5,219 | 6,272 | 7,308 |
| ucp_seats | 1,010,000 | 1,631 (cap) | provisional | 1,575 | 56 | 58 | 61 |
