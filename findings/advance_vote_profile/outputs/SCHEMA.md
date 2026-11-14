# Output files

2026-11-10 01:33 Alberta time · claude-opus-5-5 · medium

Every file in this folder is written by a script in `findings/advance_vote_profile/`. Status: exploratory, not registered.

**Conventions.**
- JSON: snake_case keys only (checked when written). Every file starts with a `meta` object: `entry` (stamp, Alberta time, read from the system clock), `script`, `status`, `inputs` (each with `path` and `sha256`), and `seed` where randomness is used. Data are lists of records, not objects keyed by names.
- CSV: snake_case headers (checked when written), one row per unit named below.
- Codes: `ed` is the two-digit 2019 division number (2023) or `ED01`-style sheet name (2015). `station` is `ed` plus the station letter (for example `04H`). "Two-party" is NDP plus UCP (in 2015, NDP against PC plus Wildrose). Margins are UCP minus NDP, in modelled votes. `m0` is the registered Amendment 12 rule; `p` is rule P.

## CSV files

| File | Script | One row per | Columns |
|---|---|---|---|
| `skew_2023_by_division.csv` | 01 | 2019 division (87) | `ed`; `{kind}_ndp`, `{kind}_ucp`, `{kind}_valid` for kind in advance, eday, mobile, special, vote_anywhere; `electors` (names on list); `non_valid` (valid ballots not cast on election day); `name`; `region`; `eday_share` (election-day NDP share of two-party); `eday_margin_pts`; `comp` (closeness band); `non_ndp`, `non_ucp`, `non_share` (non-election-day); `skew_pts` (non-election-day NDP share minus election-day, points); `skew_logit` (same on the log-odds scale); `non_frac_of_votes`; `{kind}_skew_pts`; `eday_rate`, `non_rate` (valid ballots per elector) |
| `skew_2015_by_division.csv` | 01 | 2015 division (87) | as above for kinds advance, eday, mobile, special (no Vote Anywhere in 2015) |
| `polls_2015_parsed.csv` | 01 | 2015 poll row | `ed`, `name` (division), `poll`, `k` (eday, advance, mobile, special), `ndp`, `ucp` (PC plus Wildrose), `valid`, `electors` |
| `advance_catchments_2023.csv` | 04 | voting area in a division with two or more located advance polls | `va_row_idx` (row in the voting-area file), `ed`, `location` (nearest located advance poll), `loc_ndp`, `loc_ucp` (that poll's counts) |
| `advance_locations_2023.csv` | 04 | located 2023 advance poll used in the test | `ed`, `name`, `complete` (every poll of the division located), `a_ndp`, `a_ucp` (poll counts), `c_ndp`, `c_ucp` (election-day votes in its catchment), `c_gap` (election-day non-voters in it), `c_valid` (election-day valid ballots in it), `n_vas`, `adv_share`, `catch_share` (NDP shares) |
| `advance_places_2015.csv` | 04 | 2015 town-named advance poll matched to election-day polls | `ed`, `place`, `a_ndp`, `a_ucp`, `c_ndp`, `c_ucp`, `eday_polls`, `adv_share`, `catch_share` |
| `turnout_stations.csv` | 07 | 2023 election-day station (1,216) | `station`, `ed`, `station_name`, `names_on_list`, `eday_ballots` (total ballots cast on election day), `placed_m0`, `placed_p` (early ballots of every kind placed there), `turnout_eday_only`, `turnout_m0`, `turnout_p` (fractions; 1 = 100%) |
| `division_takeup.csv` | 07 | 2019 division (87) | `ed`, `division`, `region`, `electors` (names on list), `eday_ballots`, `early_ballots` (total non-election-day ballots), `non_voters_eday` (names on list minus election-day ballots, stations over 100% counted as 0), `eday_turnout`, `takeup` (early ballots per election-day non-voter), `total_turnout` |
| `headline_table.csv` | 05 | map × rule × lean value | `map`, `rule` (m0 or p), `beta` (blank for m0), `ucp_seats`, `ndp_seats`, `efficiency_gap_pct`, `mean_median_pct`, `declination`, `ucp_seats_at_tied_vote`, `close_seats_4pts`, `n_districts` |
| `district_margins.csv` | 05 | map × district | `map`, `district`, `m0_ucp`, `m0_ndp`, `m0_ucp_margin`, `p_ucp`, `p_ndp`, `p_ucp_margin` (lean 1.0), `p_ucp_margin_min_over_beta`, `p_ucp_margin_max_over_beta` (lean 0.87 to 1.22), `winner_m0`, `winner_p` |
| `va_allocations.csv` | 05 | voting area (4,765) | `va_row_idx`, `ed`, `va`, `station`, `eday_ndp`, `eday_ucp`, `eday_other`, `electors`, `eday_ballots` (station figures split equally), `m0_ndp`, `m0_ucp`, `m0_other` (all ballots under M0, from the registered file), `p_ndp`, `p_ucp`, `p_other` (all ballots under P, lean 1.0), `p_placed_ballots` (early ballots of every kind placed under P) |
| `territory_null_scores.csv` | 09 | stored redraw-test plan (2,000) | `chain`, `step`, `s152`, then `eg`, `mean_median`, `declination`, `ucp_seats`, `drain`, each with suffix `_m0` and `_p`; `in_reference_set` (chains 1, 2, 4, 6 after step 10,000) |

## JSON files

| File | Script | Contents after `meta` |
|---|---|---|
| `skew_summary.json` | 01 | `y2023`, `y2015`: province totals by ballot kind (`province`), per-division skew summary, `by_region` and `by_competitiveness` lists, `cross_division` fits, and for 2023 `advance_locations_within_division` (chi-square test of one mix per division); `note_2019` |
| `provincial_location_tests.json` | 04 | `located_polls_2023`: counts of polls found and used, `slope_all` (lean strength, clustered SE), `slope_complete_divisions`, `volume` (count-side fit, unreliable), `hide_and_predict_all` (m0, m1, m2 errors), `grid_share_rmse_pts` list, `slope_by_region` list; `town_polls_2015`: `slope`, `share_rmse_pts` |
| `robustness.json` | 06 (seed 20261110) | `located_polls_2023`: other fits, `leverage_top5`, drop-one and drop-two fits, `leave_one_division_out_range`, `cluster_bootstrap_95pct` (the range used for the lean), placebos, `residual_at_located_polls` (P's scatter there and why it is not used as a station error model), `coverage`, `unlocated_polls` |
| `turnout.json` | 07 | `names_on_list` (workbook against the Elections Alberta report, with quoted statements and pages), `turnout_distribution` (election_day_alone, m0, p: percentiles and 5-point bins, each bin including its upper edge), `within_division_sd_pts_median`, `stations_over_100_election_day_alone`, `m0_stations_over_100`, `m0_top10_over_100`, `hard_check_p`, `count_assumption` (across divisions, within divisions at located polls, what cannot be said) |
| `headline.json` | 05 | `rule_p` (lean estimate, range, value used, count dial, betas run), `checks` (each with `passed`), `all_checks_passed`, `stations_over_100pct_on_election_day`, `stations_over_100pct_m0`, `maps` (per map: m0, p at lean 1.0, p range over the lean, `seats_that_change`, `thinnest_p_margins`) |
| `vote_file_p.json` | 08 | the P vote file's path, bytes, SHA-256, rule, rows, columns, province totals, checks, votes placed differently from M0, the registered sibling file, and Git LFS status |
| `territory_null_p.json` | 09 | the redraw-test null rescored: map, settings, pinned code commit, whether the M0 rescore reproduces the filed result, and for `m0` and `p` each statistic's observed value, two-sided p, null mean and 2.5th and 97.5th percentiles, and midrank percentile |
| `replay_check_p.json` | 10 `check` | `chains`: for each ensemble chain, whether its P replay exists and, if so, whether every vote-independent column the original has is present and matches the election-day original and the M0 replay where one exists (`status`, `reasons`, `missing_columns`, `rows_that_differ`, `rows_that_differ_vs_m0`). In this checkout every chain is "not run". |
| `ensemble_ranks_p.json` | 10 `rank` | `sets`: percentiles of each real map's P score against the replayed chains that passed. In this checkout no chain has passed, so no percentile is given. |

## Written outside this folder

| File | Script | What |
|---|---|---|
| `data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg` | 08 | The all-ballots voting-area file under P. Same rows, columns and geometry as `va_polygons_all_2023_ballots_primary.gpkg`; `va_ndp`, `va_ucp`, `va_other` hold all ballots under P. |
