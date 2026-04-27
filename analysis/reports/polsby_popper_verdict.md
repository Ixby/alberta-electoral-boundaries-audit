---
name: polsby_popper_verdict
description: Does the Lane 2 lasso/non-compactness claim survive the v0_9 topological substrate?
type: project
---

# v0_9 Polsby-Popper verdict

**Status: claim survives directionally, but the specific 7.1% / 3.5% framing and one of the five named lasso districts do not.**

## Headline

Two of the five publicly-named lasso districts are **above** the conventional PP < 0.25 flag threshold under the v0_9 topological substrate:

- **Calgary-Nolan Hill-Cochrane (minority): PP = 0.402 — above 0.25.** This is the single district the commission chair flagged by name as a "lasso-shaped corridor". Under the gapless / overlap-free v0_9 substrate it scores in the *moderate* compactness band, not the *low* band. It still has a visible narrow waist on the map, but the Polsby-Popper number does not by itself put it in flag territory. The chair's qualitative flag is independent of any PP threshold; this verdict is only about whether the PP metric supports the flag.
- **Calgary-Airdrie (minority): PP = 0.286** — above 0.25, low end of moderate.

The other three are below 0.25 and remain in the flagged band:

- **Edmonton-Enoch-Devon: PP = 0.065** (very low — bottom of the minority distribution)
- **Calgary-Foothills-Airdrie West: PP = 0.140** (very low)
- **Stony Plain-Drayton Valley (minority): PP = 0.175** (low). Note this name appears in *both* maps; the **majority's Stony Plain-Drayton Valley scores PP = 0.303**, comfortably above the threshold. Same name, different geometry, opposite verdict.

## Asymmetry

Pre-v0_9 (Tier A/B subset only): minority 5/70 = 7.1 % below 0.25, majority 2/57 = 3.5 % below 0.25 → ~2.0× asymmetry on a partial-coverage subset.

v0_9 (full 89/89 coverage on both maps): **minority 27/89 = 30.3 % below 0.25, majority 20/89 = 22.5 % below 0.25 → ~1.35× asymmetry.**

Both rates jump under v0_9 because the topological substrate carries true VA-level perimeter detail (the v0_1 Tier A/B subset inherited smooth 2019-shapefile perimeters). The directional asymmetry — minority less compact than majority — survives, but the magnitude shrinks from ~2× to ~1.35×, and the absolute rates are now too high (>20 % both maps) for the conventional PP < 0.25 threshold to function as a discriminator. A v0_9-appropriate threshold would have to be re-derived.

## Did the claim survive?

**Partially.** The minority is still measurably less compact than the majority on PP under v0_9 (mean 0.334 vs 0.356; share-below-0.25 30.3 % vs 22.5 %), and three of the five named lasso districts are below the conventional flag threshold. But:

1. The **"~7.1 % vs 3.5 %"** numerical framing is an artefact of the v0_1 Tier A/B partial-coverage subset and does not survive the v0_9 substrate.
2. The **"~2× asymmetry"** framing is closer to **~1.35×** under full coverage.
3. **Calgary-Nolan Hill-Cochrane**, the chair's named lasso, scores **PP 0.402** under v0_9 — moderate, not low. The lasso-shape claim has to rest on the visual / qualitative chair flag and the §5.9.4 submission-archive null result, not on PP.

## Recommended report-text changes (PO to decide)

**`report_academic.md`:**

- Lines 2111–2117 (the "Tier A/B archived" block): the surrounding `pre-v0_7` framing is already correct; add a line pointing forward to v0_9 (PP < 0.25 rates are 30.3 % minority / 22.5 % majority, ~1.35× ratio) so a reader does not anchor on the 7.1 % / 3.5 % numbers.
- Line 2142: replace **"roughly double the rate of low-compactness EDs"** with the v0_9 ratio (~1.35×), and call out that the conventional PP < 0.25 threshold no longer discriminates well at v0_9 perimeter resolution.
- Line 2144: re-list the Tier-C-flagged hybrids with their v0_9 PP values (Calgary-Nolan Hill-Cochrane 0.402, Calgary-Airdrie 0.286 → both *above* threshold under v0_9).

**`report_public.md`:**

- Line 144 (chair-flag paragraph) and line 168 (lasso-corridor framing): no PP number is cited, so no edit required for numerical accuracy. If the PO wants defensive framing, note that the "lasso" descriptor is the chair's qualitative flag; the PP score for Calgary-Nolan Hill-Cochrane under v0_9 (0.402) is moderate, not low.
- Line 252 (Calgary 7-hybrids list): unchanged — these are all hybrids, but two (Calgary-Nolan Hill-Cochrane, Calgary-Airdrie) are not low-compactness under v0_9.

## Data

`data/polsby_popper_per_district.csv` (178 rows: 89 minority + 89 majority). Script: `analysis/scripts/polsby_popper.py`.
