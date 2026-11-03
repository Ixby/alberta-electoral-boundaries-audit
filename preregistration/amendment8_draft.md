## Amendment 8: Two redraw tests on the November map, the swing-zone test and neighbour-drain, calibrated before the map is scored

> **Status: DRAFT, not filed.** Written 2026-11-03 (Alberta time). At the time of writing:
> - The panel's map had been published as images only.
> - No geometry of the panel's map had been scored on any partisan measure.
> - No official shapefile had been released.
> - The calibration below uses only neutral plans and the commission maps. It reads no November geometry.

**Why.** Wuff asked that the two adjacency-and-boundary tests be carried to the November map: the swing-zone allocation test (SZAT, OSF 6pt83) and neighbour-drain (OSF r3zm7; AsPredicted #289451). Both need changes before they can be used.
- **SZAT's registered null does not work on these maps.**
  - It flips each swing-zone voting area independently.
  - On the commission maps, 2,086 of the 2,110 swing-zone areas form one connected block. The block-permutation correction moved p from 0.0024 to about 0.19, and SZAT was retired as a confirmatory test (academic report §5.2.10).
  - The panel's changed districts are contiguous, so the same collapse is expected.
  - The November map also has 91 districts against the majority map's 89, so a difference in efficiency gap between them mixes the two added seats with the boundary choices.
- **Neighbour-drain is already scored on the November map, as S5 of the structural lane (Amendment 5, Part 7).** On 200 neutral 91-district maps, S5 fires 43.5% of the time (`findings/structural_lane_calibration_2026-10-31.md`). That makes S5 a weak screen on its own.

This amendment adds one null that fits both tests: neutral redraws of the territory the panel changed, with the districts it left alone held fixed.

**Part 1: The territory null.**
- *Fixed districts.* These are the 56 districts the panel left unchanged (Amendment 7, Step A; `findings/iap_unchanged_districts.md`), at the commission majority's official geometry.
  - Calgary-Acadia is also fixed. On the voting-area graph it is cut off from the rest of the changed territory, so it can only ever hold one district. The panel changed it by 2 people.
- *Redrawn territory.* Everything else: one connected region of 1,782 voting areas, which the panel divides into 34 districts. Voting areas are placed in districts by representative point.
- *Sampler.* This is the set D sampler (`close_seats_ensemble.py`, Amendment 17), unchanged: ReCom on the canonical voting-area graph, 2021 census population overlay. The statute is applied as written:
  - s.15(1): every district within ±25% of the provincial average (overlay total ÷ 91), not the territory's own average;
  - s.15(2): up to 50% below the average for a district meeting at least 3 of the 5 criteria, on the Amendment 23 criteria table (SHA-256 `48c928b8…2fafc`). At most 4 such districts province-wide. Two unchanged districts already use s.15(2) (Central Peace-Notley, Lesser Slave Lake), so at most 2 in the territory.
- *Code.* `analysis/scripts/territory_null.py` and `territory_score.py`, branch `a8-territory-null`, commit `401e15b5` (calibration outputs in `data/outputs/a8_territory_null/`, commit `10032155`).
- *Seeds.* drand round 6606642 (`preregistration/seed_commitments.md`). Chain i uses salt `a8-territory-null-chain<i>`; the label-shuffle draws use salt `a8-drain-label-shuffle-<map>`.
- *Runs.*
  - Reference chains 1–4 and holdout chain 5, 100,000 steps each.
  - One plan is kept every 250 steps, and the first 10,000 steps are discarded.
  - That leaves 1,440 reference plans and 360 holdout plans.

**Part 2: Test R1, the swing-zone test as a redraw test.**
- *Statistic.* The efficiency gap of the full 91-district November map: 2023 election-day two-party votes, voting areas by representative point (`territory_score.py`, the same substrate as the null).
- *Null.* The efficiency gaps of the reference plans: the 57 fixed districts plus 34 neutral districts in the territory.
- *p.* Two-sided rank, 2 × min(share of null ≤ observed, share ≥ observed).
- *Flag.* The test flags at p < 0.05, and the direction is reported.
- *Reported beside it, not gating.* Mean-median, declination and UCP seats, each ranked the same way.

This asks the swing-zone test's question directly: given the districts the panel kept, are its lines in the territory it redrew unusual among neutral lines drawn under the same statute?

**Part 3: Test R2, neighbour-drain as a redraw test.**
- *Statistic.* The registered neighbour-drain score: the sum, over coupled directed adjacent pairs, of max(0, s_X − 0.15) × max(0, 0.05 − m_Y).
  - It is computed on the same substrate, with adjacency taken from shared voting-area edges.
  - On the majority map this gives 0.0072418, and the original `drain_score` function gives the same number (S5's registered value is 0.0072127, from polygon adjacency).
- *Null, p and flag.* As in R1, against the reference plans' drain scores.
- *Reported beside it.* The registered label-shuffle p (10,000 permutations), with its false-positive rate on neutral plans from Part 4. S5 itself is unchanged.

**Part 4: Calibration, run before filing.**

| Check | Result |
|---|---|
| Split-R̂ across chains 1–4, efficiency gap | 1.009 |
| Split-R̂, drain | 1.004 |
| Null 95% interval, efficiency gap | −0.02% to +2.24% (mean +1.21%, UCP-favoured positive) |
| Null 95% interval, drain | 0.0022 to 0.0258 (mean 0.0083) |
| Holdout false-positive rate at p < 0.05, R1 | 4.4% (mean-median 5.3%, declination 4.7%) |
| Holdout false-positive rate at p < 0.05, R2 | 1.4% (conservative) |
| Label-shuffle null on neutral holdout plans, share with p < 0.05 | **97.5%** of 200 (2,000 permutations each) |
| Majority map on this substrate: EG, drain | majority (89 districts) EG +0.10%, drain 0.00724; minority EG +4.02%, drain 0.00059. These match the audit's canonical values. Neither map is in the null's population (89 districts, and nothing held fixed), so they are not ranked. |

On reading it:
- The rank tests are calibrated: false-positive rates are near or below 5%, and the chains agree (R̂ ≤ 1.011).
- The registered label-shuffle null flags nearly every neutral plan. It ignores geography, and real districting arranges similar neighbours next to each other. Its p is therefore reported only and never used as a gate. This also explains why both commission maps come out at p ≈ 0 under it.
- **Sensitivity.** R1 flags a November map whose efficiency gap falls outside −0.02% to +2.24%, given the 57 fixed districts. R2 flags a drain score outside 0.0022 to 0.0258.

**Part 5: Which map, and when.**
- *Headline.* R1 and R2 are scored on the official shapefiles within 72 hours of their release, beside the structural and partisan lanes.
- *Before the shapefiles.* There is no provisional score. Amendment 7's Step B calibration was run on 2026-11-03 and failed (`findings/a7_stepb_calibration.md`), so no reconstruction of the panel's map is scored.
- *If the enacted map changes any of the 57 fixed districts* (a resolution, an amendment, the bill), the null is rerun with that map's unchanged set before scoring. The code, seeds and rules stay the same, and the rerun is disclosed.

**Part 6: What this changes and what it does not.**
- SZAT as registered (6pt83, swing-zone permutation null) stays retired. R1 is a new test, scored beside the specification and not part of its verdict.
- S5 and the structural lane are unchanged. R2 is reported beside them.
- Neither test gives a verdict on whether the map is a gerrymander. Each locates the panel's choices within neutral choices under the same statute and the same fixed districts.
- The two tests are reported separately, each at its own 0.05. Where both flag, that is stated; they are not combined.

**Part 7: Erratum (Amendment 7, Part 3).** Amendment 7 calls the efficiency-gap gate "T4". In the w2s8k plan (`dpg2_experiment_plan.md`, §T-C) that gate is "T1 EG delta" (< 0.5 points), and w2s8k's T4 is population MAD. The quantities and thresholds Amendment 7 states are what Step B computes. Only the label is wrong.
