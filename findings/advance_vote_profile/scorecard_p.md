# The scorecard under rule P

2026-11-10 13:35 Alberta time · claude-opus-5-5 · medium

**What this is.** Amendment 14 makes rule P the registered way to place 2023's early ballots when scoring the November map. Amendment 12's rule becomes a sensitivity. Amendment 14, Part 6 left the scorecard counts unrestated until the ensembles were replayed. They have been replayed, and this file restates the counts. It covers four maps: the panel reconstruction (v3), the commission majority, the commission minority and the ¶167 map. Numbers are in `outputs/scorecard_p.json`, written by `12_scorecard_p.py`. Nothing here says whether any map is a gerrymander.

**How each test was scored.**
- **Partisan tests P1 to P4.** Under rule P, the values and ranks come from the replayed canonical ensemble: 87 districts, 1,010,000 plans (`outputs/ensemble_ranks_p.json`). P1's line, +2.15%, comes from `outputs/thresholds_p.json`. Under Amendment 12, the inputs are the filed all-ballots results, and P1's line is +1.39%.
- **S5.** It was recomputed for every map on both vote files with the registered `compute_S5_drain`, which was not edited. On both files it reproduces the filed drain scores of the majority, minority and panel maps.
- **Tests that use no votes** (S1, S2, S3, S6, S4, X1, towns over-divided, city versus rest) do not change.

**Flag rules.**
- **P1:** the efficiency gap is at or above the line.
- **P2 to P4:** the map is at p95 or higher in the UCP direction.
- **S5:** under Amendment 12, the drain is below 0.0019398. Under rule P, S5 is set aside (Amendment 14, Part 3). It gives no flag, and it counts as not flagged.
- **Counts:** 3 or more of 5 structural flags means "replicated". 2 or more of 4 partisan flags means "present".

## The counts

| Map | Structural, Amendment 12 | Structural, rule P | Partisan, Amendment 12 | Partisan, rule P |
|---|---|---|---|---|
| Panel reconstruction (v3, 91) | 2 of 5, not replicated | 2 of 5, not replicated | 1 of 4, absent | 1 of 4, absent |
| Commission majority (89) | 0 of 5 | 0 of 5 | 0 of 4 | 0 of 4 |
| Commission minority (89) | 5 of 5, replicated | **4 of 5**, replicated | 4 of 4, present | 4 of 4, present |
| ¶167 map (91) | 2 of 5, not replicated | 2 of 5, not replicated | 0 of 1 scored; P2–P4 not computed | 0 of 4, absent |

**What changed.**
- **Minority, structural lane: 5 of 5 becomes 4 of 5.** The only change is S5. Its drain was 0.00017 against Amendment 12's line of 0.00194, so it flagged. Under rule P, S5 is set aside. The lane still reads "replicated."
- **No partisan count changes.** The panel's one flag is still P4, now at p97.25 instead of p98.82. The minority's four flags all still fire, and P1 fires by more: +5.64% against a +2.15% line. Before, it was +2.55% against +1.39%.
- **The ¶167 map's structural lane is 2 of 5 on all ballots under both rules.** Its earlier "3 of 5" was on election-day ballots (`findings/iap_para167/README.md`). On all ballots its drain is 0.00371, above Amendment 12's line.

## Partisan lane, test by test

Each cell gives the value and its percentile in the canonical ensemble.

| Map | Test | Amendment 12 | Rule P | Line | Flag (A12 / P) |
|---|---|---|---|---|---|
| Panel v3 | P1 efficiency gap | −1.66% (p47.95) | −2.84% (p18.31) | +1.39% / +2.15% | no / no |
| | P2 mean-median | −1.09 pts, p79.45 | −0.47 pts, p89.16 | p95 | no / no |
| | P3 declination | −0.060, p48.22 | −0.080, p16.89 | p95 | no / no |
| | P4 seats at 50/50 | 49.45%, p98.82 | 49.45%, p97.25 | p95 | **yes / yes** |
| Majority | P1 | −2.70% (p26.48) | −2.83% (p18.41) | +1.39% / +2.15% | no / no |
| | P2 | −3.51 pts, p1.24 | −3.77 pts, p0.52 | p95 | no / no |
| | P3 | −0.093, p17.26 | −0.089, p13.89 | p95 | no / no |
| | P4 | 47.19%, p74.08 | 47.19%, p68.67 | p95 | no / no |
| Minority | P1 | +2.55% (p98.82) | +5.64% (p99.98) | +1.39% / +2.15% | **yes / yes** |
| | P2 | +0.08 pts, p98.73 | +0.51 pts, p99.18 | p95 | **yes / yes** |
| | P3 | +0.046, p99.82 | +0.101, p100.0 | p95 | **yes / yes** |
| | P4 | 51.69%, p99.90 | 51.69%, p99.65 | p95 | **yes / yes** |
| ¶167 | P1 | −2.19% | −2.33% (p25.78) | +1.39% / +2.15% | no / no |
| | P2 | −2.90 pts, not computed | −2.18 pts, p27.00 | p95 | not computed / no |
| | P3 | −0.080, not computed | −0.077, p18.50 | p95 | not computed / no |
| | P4 | 48.35%, not computed | 48.35%, p88.47 | p95 | not computed / no |

No map lands in P3's other tail (p5 or lower). That tail is reported but never counted.

## Structural lane, test by test

| Map | S1 population MAD (above 3,382.5) | S2 splits (above 26.5) | S3 anchoring (below 76.01%) | S6 patterns (3 or more) | S5 drain, A12 (below 0.00194) | S5 drain, rule P (midpoint 0.00588; set aside) |
|---|---|---|---|---|---|---|
| Panel v3 | **3,557** | 24 | **74.29%** | 1 | 0.01043, no flag | 0.00053, no flag |
| Majority | 2,827 | 23 | 79.96% | 0 | 0.00371, no flag | 0.00403, no flag |
| Minority | **3,938** | **30** | **71.78%** | **5** | **0.00017, flag** | 0.00773, no flag |
| ¶167 | **3,413** | 23 | **75.84%** | 0 | 0.00371, no flag | 0.00403, no flag |

Bold = flag. S1, S2, S3 and S6 use no votes and are the same under both rules. S4, Polsby-Popper, is measured but not counted.

**Shown beside S5, because Amendment 14 requires it.** Under rule P, the panel's drain (0.00053), the majority's (0.00403) and the ¶167 map's (0.00403) are all below the 0.00588 midpoint. The minority's (0.00773) is above it. Read as written, S5 would flag those three maps and not the minority. That reversal is why Amendment 14 sets S5 aside. If S5 counted that way, the panel would be at 3 of 5 and the ¶167 map at 3 of 5. Neither is the registered result.

The ¶167 map's drain equals the majority's to every digit on Amendment 12's file. On election-day ballots, the same code reproduces both filed values, which differ (0.00369 and 0.00721). So the tie is the code's result on that file, not a mix-up of maps.

## Other tests that use votes

**Competitive seats in the size-matched sets** (Amendment 5, Part 17: flag at or below the set's 5th percentile).
- **Amendment 12.** The panel has 10 close seats, above the 5th percentile (8) in sets A, B, C and D, so there is no flag. The ¶167 map has 10, with no flag in set D, the only set it was placed in. The commission maps were not computed: no 89-district all-ballots run is filed.
- **Rule P: not computed for any map.** `ensemble_ranks_p.json` gives only each map's midrank percentile and the set's median, not the 5th percentile that the flag needs. For reference:
  - panel 9 seats (p25.7 to p28.6);
  - majority 11 (p67.2 to p67.8);
  - minority 9 (p24.6 to p30.2; 8 to 9 across the lean range);
  - ¶167 10 (p44.2 to p47.3).

**Redraw tests R1 and R2 (panel only).** Neither flags under either rule (flag at p < 0.05).

| Test | Amendment 12 | Rule P |
|---|---|---|
| R1, efficiency gap | −1.66%, p = 0.914 | −2.84%, p = 0.619 |
| R2, neighbour drain | 0.01043, p = 0.419 | 0.00053, p = 0.576 |

These tests compare the November map's changes with the majority map, so they do not apply to the commission maps. No null has been run for the ¶167 map, so they were not computed for it.

## Not computed

- **The ¶167 map's P2, P3 and P4 under Amendment 12.** They need the all-ballots canonical chains, which are not in this checkout. No canonical rank of that map on that file is filed. So its Amendment 12 partisan count rests on P1 alone.
- **Competitive-seat flags under rule P, all maps.** The 5th percentile of each set is missing.
- **Competitive seats for the commission maps under Amendment 12.** No run is filed.

## Limits

- **Percentile method.** The rule-P ranks are midrank percentiles. The registered rule counts plans at or below the map. The two differ only on ties. P4 cannot tie for these maps, because a share out of 89 or 91 never equals one out of 87 (the script checks this). Ties on the other measures were not checked, because the chains are not here.
- **Rounding.** The rule-P values in `ensemble_ranks_p.json` are rounded (for example, −0.02836) and taken at lean 1.0. No flag is near enough to its line for this to matter.
- **Same votes for v1 and v3.** The panel's Amendment 12 partisan figures and R1/R2 were scored on the v1 assembled map. v3 moves no voting area, so its votes per district are the same.
- **The qsgy8 tripwires** stay on election-day ballots, as filed.
