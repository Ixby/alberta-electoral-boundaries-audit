> **Backward:**
> - `analysis/scripts/rural_division_count.py` — companion script (hypotheses frozen in its header before first execution)
> - `data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg`, `data/shapefiles/reference/alberta_2019_eds/` — substrates
> - Commission final report, minority report pp. 287, 356 — the charge under test (verified verbatim via pdfplumber, 2026-07-14)
> - `analysis/scripts/t3_2_majority_rural_isolation.py` — classifier provenance
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.6 equal-application disclosure — cites this result
> - `reports/public/report_public.md` Casing 12 — cites this result
> - `viewer` Casing 12 and the norms page — cite this result
> - `findings/README.md` — indexes this finding

# Rural-division count and succession — the minority's charge, tested

**Status: exploratory.** Designed and executed 2026-07-14, in-session, on data
that already existed. The hypotheses were frozen in the companion script's
header before first execution, but nothing here was externally time-stamped
before the data was seen, and adjacent analyses had already touched this
substrate. Under the audit's own §4.3.1 standard this finding can never be
described as pre-registered.

## The charge

The minority report accuses the majority map of:

> "an inclination to delete or mangle rural electoral divisions and, in
> effect, reduce effective rural representation" (p. 356)

> "insistence on eliminating and amalgamating certain rural divisions"
> (p. 356)

and states that the minority "departed from the majority where we believe the
legislative direction given to the Commission and the thoughtfulness of public
submissions has not been given sufficient effect" (p. 287).

The audit surfaced this charge into its record on 2026-07-14 and, rather than
deferring the test, ran it the same day — the same treatment the chair's
flags against the minority received.

## Method

The audit's established rural/urban name classifier (identical to T3.2's,
including its Airdrie hyphen amendment) was applied to all three maps: an ED
is **rural-anchored** iff its name does not begin with a city prefix. Each
2019 ED's **successor** under each 2026 map is the district with the largest
area overlap (EPSG:3400). A 2019 rural division is **absorbed** if its
successor is urban-anchored; two or more are **amalgamated** if they share
one rural-anchored successor.

**Classifier artifacts found on inspection, and how they were handled.** The
frozen rule's output contained bare city names classified rural ("St. Albert",
"Sherwood Park", "Grande Prairie", "Spruce Grove" — the same hyphen-
sensitivity the T3.2 amendment fixed for "Airdrie"), and the minority map
spells "St Albert" without a period, dodging even the corrected prefix. A
**corrected sensitivity rule** (bare-name / hyphen / space / period robust)
was added *after* first execution, is disclosed as such, and is reported
alongside the frozen rule — never in place of it. The finding's direction is
identical under both.

## Results

| Map | Rural-anchored divisions (frozen rule) | (corrected rule) |
|---|---|---|
| 2019 enacted (87 EDs) | 31 (35.6%) | 28 (32.2%) |
| Majority 2026 (89 EDs) | 28 (31.5%) | 24 (27.0%) |
| **Minority 2026 (89 EDs)** | **23 (25.8%)** | **19 (21.3%)** |

**Succession (identical under both rules):**

- **Majority:** absorbs 3 of 2019's rural divisions into urban-anchored
  successors (Brooks-Medicine Hat, Cypress-Medicine Hat, Morinville-St.
  Albert); amalgamates 6 rural divisions into 3 (Cardston-Siksika +
  Taber-Warner → Taber-Cardston; Drumheller-Stettler + Lacombe-Ponoka →
  Drumheller-Stettler; Athabasca-Barrhead-Westlock + Lac Ste. Anne-Parkland
  → Barrhead-Westlock-Athabasca); creates 2 rural divisions with no 2019
  rural predecessor (Cochrane-Springbank, High River-Vulcan-Siksika).
- **Minority:** absorbs **7** of 2019's rural divisions into urban-anchored
  successors (Brooks-Medicine Hat, Cardston-Siksika, Cypress-Medicine Hat,
  Innisfail-Sylvan Lake, Lacombe-Ponoka, Strathcona-Sherwood Park,
  Taber-Warner); amalgamates Banff-Kananaskis + Rimbey-Rocky Mountain
  House-Sundre into Rocky Mountain House-Banff Park (the chair-flagged
  division); creates no new rural division.

## Verdict on the frozen hypotheses

**H-charge (the minority's prediction) is not supported — the direction
reverses.** Under both classifier variants, the minority map has *fewer*
rural-anchored divisions than the majority (23 vs 28 frozen; 19 vs 24
corrected), reduces the 2019 rural count by more (−8 vs −3 frozen; −9 vs −4
corrected), and absorbs more 2019 rural divisions into city-named districts
(7 vs 3). On the measure its own accusation names, the minority map does more
of what it accuses the majority of.

## The fair reading — what survives for the minority

Reporting this fairly requires saying what the numbers do *not* do:

1. **The charge's underlying observation is real, for both maps.** Both 2026
   proposals reduce rural-anchored divisions relative to 2019, in a province
   that added two seats. That is consistent with the chair's own
   Recommendation 5, which called for *adding* rural seats — the concern that
   rural representation thinned this cycle is not invented, and the majority
   map genuinely did absorb three rural divisions and amalgamate six into
   three.
2. **The classifier is coarse, symmetrically.** Name-based classification
   treats a city-named hybrid as urban even where it contains large rural
   territory. A defender of the minority could argue its hybrids still
   *serve* rural communities. Two things cut against that defence — the
   minority's own charge is framed in terms of divisions being eliminated
   and amalgamated, which is exactly what the count measures; and the
   audit's separate structural analysis found the minority's hybrids anchor
   population in their urban ends — but the coarseness is disclosed, the
   same rule scored every map, and every classified name is listed in
   `findings/rural_division_count.json` for anyone to re-score.
3. **No intent is inferred, in either direction.** The count says what each
   map does to rural-anchored divisions. It does not say why, and a
   rural-division count is not a measure of representation quality.
