# November 2 runbook: scoring the committee's map

The order of work when the Select Special Committee's map is tabled. The registered procedure is
`preregistration/november_2026_scoring_spec.md` (v1.2) with Amendments 16 and 17. This file
changes none of it. It gives the commands that run it, plus three supplementary checks that are
labelled as such wherever they appear.

Dry-run on 2026-10-30, end to end, on `proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg`
(a random 91-district plan, not a prediction). Every step below ran and exited 0.

## 0. Ingest

- Put the published file at `data/shapefiles/lunty/lunty_2026_eds.gpkg` and note its source URL,
  download time and SHA-256 in the run log. Check which column holds district names. Every
  command below defaults to `EDName2025`; pass `--name-col` if the name column is different.
- If only a PDF is published, the spec's DPG protocol applies, and the results are provisional (spec §2).
- If the report gives district populations, save them as `data/shapefiles/lunty/stated_populations.csv`
  (`district,population`) for step 4.

## 1. Registered: partisan lane (spec §7 step 2)

```bash
python analysis/scripts/phase4c_canonical_attribution.py \
  --majority data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --output data/outputs/lunty_phase4c_results.json
python analysis/scripts/joint_outlier_score_canonical.py \
  --map-key lunty_2026 --real-scores data/outputs/lunty_phase4c_results.json \
  --output findings/lunty_joint_outlier.json
```

Before 2026-10-30 neither script read arguments. Both ignored the spec's flags and re-scored the
two commission maps, overwriting their outputs. Each now takes the spec's flags. The no-argument
runs are unchanged.

The candidate is scored with `mcmc_ensemble.score_exogenous_map()`, the function that scored the
commission maps for `simulation_real_map_scores_canonical.json`. Check: scoring the minority and
majority maps by this path reproduces that file's four metrics exactly.

## 2. Registered: structural lane (spec §7 step 3), about 5 minutes

```bash
python analysis/scripts/run_structural_battery.py \
  --shapefile data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --output findings/lunty_structural.json --label lunty_2026
```

## 3. Registered: verdict (spec §7 step 4)

```bash
python analysis/scripts/verdict_synthesis.py \
  --structural findings/lunty_structural.json --joint findings/lunty_joint_outlier.json \
  --output findings/lunty_verdict.json
```

Two fixes were made on 2026-10-30, before any committee map existed. Both bring the code into line
with spec §3; no rule or threshold changed.

- **P2, P3 and P4 fire only in the UCP direction.** The code used to read `1 − marginal_tail_p`,
  and `marginal_tail_p` is measured on whichever side of the ensemble mean the map sits. A map in
  the NDP-side tail therefore fired a "UCP direction" flag. On the majority commission map, P2 fired
  at its mean-median's 1st percentile. The partisan count stays 1 or below either way, so the
  majority map's verdict did not change.
- **A missing candidate is now an error.** It used to be scored as partisan "absent".

The guard is `tests/test_verdict_synthesis.py`: 4 of its 5 tests fail on the old code.

Also registered: X1 (Amendment 16), and the size-matched tests in Amendment 17, which Audit runs.

```bash
python analysis/scripts/score_x1.py --map data/shapefiles/lunty/lunty_2026_eds.gpkg \
  [--interim <October 2025 interim map>] [--d-record considered|not_shown] --out findings/lunty_x1.json
```

## 4. Supplementary: EBCA population rules

This is descriptive, not a registered test.

```bash
python analysis/scripts/rules_check.py --map data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --table data/outputs/s15_2_va_criteria.csv \
  [--stated data/shapefiles/lunty/stated_populations.csv] --label lunty_2026 \
  --out findings/lunty_rules_check.json
```

What it reports:

- Each district's deviation from the average.
- Districts outside ±25%, and any below −50%.
- For every district below −25%: criteria (a)–(e) under the Amendment 23 table, whether it meets
  3 of 5, and whether more than 4 districts are below −25%.

The table must be the Amendment 23 table (SHA-256 `48c928b8…2fafc`, on `amendment17-local-runs`).
`origin/master` still has the superseded table, and the tool says so when it is given it.

Deviations use the VA-level 2021 overlay. That overlay is not the official count. Give `--stated`
and a district counts only when both bases put it outside a band; the rest are listed as
"bases disagree".

Known-answer check on the two commission maps, with their published populations: the tool finds
exactly each commission's three s.15(2) divisions, at their published deviations, each meeting at
least 3 criteria. One count differs: Lesser Slave Lake meets 3 criteria here against the
commission's 4. On the overlay alone it also lists two Calgary districts (−39.7%, −25.5%) that the
published figures put at −0.7% and −2.5%. That is the cycle-lag artifact, and `--stated` removes it.

## 5. Supplementary: how much changed

```bash
python analysis/scripts/map_diff.py --a <panel map> --b data/shapefiles/lunty/lunty_2026_eds.gpkg \
  --a-label panel --b-label committee --out findings/lunty_vs_panel.csv
python analysis/scripts/map_diff.py --a data/shapefiles/canonical/ea_majority_2026_eds.gpkg \
  --b data/shapefiles/lunty/lunty_2026_eds.gpkg --a-label majority --b-label committee \
  --out findings/lunty_vs_majority.csv
```

For each district it gives the source district it takes the most population from, and the share in
each direction. A district counts as unchanged at 99% both ways, the X1 rule. Sanity checks: a map
against itself gives 89 of 89 unchanged; minority against majority gives 25 unchanged.

## 6. Supplementary: the documents

These are entered by hand, with page references:

- [ ] Does the committee's report give reasons for its departures from the majority map and from
      Recommendation 5? Record this for X1 (d) with `--d-record`.
- [ ] Is the advisory panel's own report or map public? If so, run step 5 panel vs committee.
- [ ] Minority report(s): who filed them, and what they say was changed in committee.
- [ ] Does Government Motion 37's text adopt the EBCA s.15 rules? This settles whether step 4
      describes binding rules or a yardstick.
- [ ] The map's own population table, saved for `--stated`.

## Dry-run note for Audit (2026-10-30)

On the synthetic neutral plan, the registered pipeline returned "replicates the minority-style
signature on both lanes":

- Structural lane: 3 flags.
- Partisan lane: 2 flags. P1 EG +5.97% and P3 declination at the 99.5th percentile, against the
  87-district canonical ensemble.

That plan is a single random 91-district partition, within ±25%, with no committee-style intent.
One plan is not a rate. Still, it is direct evidence of the specificity concern already recorded
under Amendment 9 (S1 alone fires on 25.7% of neutral plans). It is also consistent with the
district-count mismatch that Amendment 17's size-matched comparison was added to address. The
registered headline should be read beside the size-matched results, as Amendment 17 already
requires.
