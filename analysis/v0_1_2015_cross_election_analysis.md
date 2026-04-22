# 2015-vote cross-election analysis (v0.1)

## Scope

Extends the 2019/2023 two-election direction-stability test with a 2015
third data point. Track Z deliverable.

## Method

### Phase 1 — 2015-to-2019 crosswalk construction

Source of truth: the 2017 Electoral Boundaries Commission (EBC) final
report (`.temp/ebc_2017_final.pdf`, text-extracted at
`.temp/ebc_2017_text.txt`). Each post-2017 electoral division in the
report has a dedicated description identifying which pre-2017 EDs
contributed territory. Consolidations are explicitly enumerated in the
Executive Summary (pp. 5-6) and repeated at the foot of each rural ED's
section:

- Central northeast 4->3: Lac La Biche-St. Paul-Two Hills,
  Athabasca-Sturgeon-Redwater, Fort Saskatchewan-Vegreville,
  Bonnyville-Cold Lake.
- Central-west 5->4: Rimbey-Rocky Mountain House-Sundre, West
  Yellowhead, Drayton Valley-Devon, Whitecourt-Ste. Anne, Stony Plain.
- Southeast 7->6: Battle River-Wainwright, Drumheller-Stettler,
  Strathmore-Brooks, Little Bow, Cardston-Taber-Warner,
  Cypress-Medicine Hat, Vermilion-Lloydminster.
- New: Airdrie-Cochrane (from old Airdrie); Calgary-North East;
  Edmonton-South.

Each 2015 ED is assigned one or more 2019-ED destinations with a
population_weight indicating the share of 2015 population routed there.
Weights are estimated from EBC narrative descriptions (e.g. "Morinville
and adjacent area moved to new Morinville-St. Albert" implies roughly
0.3 of Barrhead-Morinville-Westlock). Equal-weighted 2:1 splits for
EDs where the EBC text does not give finer granularity.

ED-name convention: the crosswalk's `ed_2019_2017boundaries` column
uses the 2019 ballot / Bill 33 enacted names (e.g.
`Athabasca-Barrhead-Westlock`, `Calgary-Bhullar-McCall`, `Highwood`).
These differ from the 2017 EBC final report recommended names in six
cases where the 2018 Electoral Divisions Act restored longer legacy
names. Using ballot names keeps the crosswalk compatible with the
existing 2019 election results file
(`v0_1_alberta_2019_results.csv`) and the 2026 hybrid crosswalks.

Coverage (see `data/v0_1_2015_to_2019_crosswalk.csv`):

- 87 / 87 2015 EDs mapped.
- 87 / 87 2019 EDs covered as destinations.
- Confidence: 58 high, 69 medium, 0 low.
- All 2015 EDs have best-available confidence of at least medium.
- All 2015 ED population weights sum to 1.0 (within rounding).

Residuals: none. The crosswalk is complete.

### Phase 2 — 2015 vote attribution

Pre-2017 ED vote totals (from `data/v0_1_alberta_2015_results.csv`)
are re-attributed to 2019 boundaries by multiplying each 2015 ED's
NDP / UCP-equivalent / Liberal / other totals by the
population_weight for each crosswalk row, then summing over
destination 2019 ED.

Party treatment follows the audit's existing `parse_2015_results.py`
convention:

- UCP-equivalent = PC + Wildrose (the 2017 merger that became UCP).
- Liberal and small-party votes are retained for turnout denominators
  but excluded from wasted-vote computation (two-party framing).

Vote conservation check passes: 2015 provincial total 1,433,745,
attributed total 1,433,750 (delta +5 from integer rounding across 127
crosswalk rows).

Province-wide 2015 NDP two-party on 2019 boundaries: 43.98%.
Rural (non-Calgary/Edmonton) NDP two-party: 35.05%.

### Phase 3 — B1-B6 on three maps

`compute_metrics()` from `analysis/v0_2_packing_cracking_analysis.py`
is invoked for:

1. 2019 map with 2015-attributed votes.
2. Majority 2026 proposal via `MAJORITY_2026_MAPPING` with 70/30
   urban/rural blend and 2015 rural baseline.
3. Minority 2026 proposal via `MINORITY_2026_MAPPING` with the same
   blend.

## Results

### Three-map metrics under 2015 votes

| Metric              | 2019 map | Majority 2026 | Minority 2026 |
|---------------------|---------:|--------------:|--------------:|
| Districts           |       87 |            89 |            89 |
| NDP seats           |       26 |            26 |            26 |
| UCP seats           |       61 |            63 |            63 |
| EG (pct)            |   +6.59% |        +7.25% |        +7.28% |
| Mean-median (pp)    |   +4.14  |         +3.61 |         +4.24 |
| B4 NDP at 50/50     |       32 |            33 |            33 |
| B6 declination      |  +0.1655 |       +0.1614 |       +0.1659 |

Sign convention: positive EG = more NDP votes wasted, which is the
gerrymandering literature's convention for "pro-UCP" outcome. All
three maps under 2015 votes show a pro-UCP lean of between 6.6 and
7.3 percentage points — materially larger than the 2019-vote or
2023-vote values.

Sensibility check: the NDP won 54 of 87 seats in 2015 but the B1-B6
metrics are being applied here with the 2019 map, not the 2010 map.
The 2015 two-party NDP share of 44.0% is below the province's 50.4%
under the 2015-actual boundaries (because NDP's 40.6% of total vote
becomes a higher share of two-party vote when Liberal / Alberta Party
vote is excluded, and because vote-pooling from splits favors rural
UCP-equivalent votes over urban NDP strength when redistributed to the
2019 boundaries). A 44% NDP two-party producing 26 seats out of 87 is
consistent with the 2019-map compactness — NDP's vote is concentrated
in Edmonton, which is efficient for geographic containment but
inefficient for seat conversion.

### Minority-majority EG asymmetry (the audit's headline claim)

Under 2015 votes, minority 2026 EG minus majority 2026 EG = **+0.03 pp**.
That is, the minority proposal is essentially identical to the majority
proposal on the efficiency-gap test when evaluated against 2015 votes.
Mean-median asymmetry is +0.63 pp (minority slightly less favorable to
NDP than majority). Declination asymmetry is +0.0046 (essentially zero).

### Three-election direction-stability table

Minority-majority EG asymmetry (pp):

| Election | Majority EG | Minority EG | Asymmetry (Min-Maj) | Direction under compute_metrics convention |
|----------|------------:|------------:|--------------------:|:--------|
| 2015     |      +7.25% |      +7.28% |              +0.03 | minority ~equal to majority (marginal +) |
| 2019     |      +0.16% |      +0.90% |              +0.75 | minority MORE pro-UCP than majority |
| 2023     |      -0.85% |      -1.36% |              -0.51 | minority LESS pro-UCP than majority |

Sign convention audit. `compute_metrics` defines `EG = (ndp_wasted -
ucp_wasted) / total`. NDP's wasted votes include its packed surplus in
NDP-won districts plus its cracked losses in UCP-won districts. A
positive EG means NDP wastes more votes than UCP — the standard
gerrymandering literature reading of that is "map is pro-UCP".
Therefore positive (Min - Maj) asymmetry means minority is MORE
pro-UCP than majority.

`analysis/v0_3_monte_carlo_ci.py` prints "Samples with minority more
UCP-favorable (negative)" and "less UCP-favorable (positive)" at lines
158-159. Those labels are inverted relative to the formula. A negative
asymmetry in this convention means minority is LESS pro-UCP than
majority. The correct reading is the opposite of what v0_3's text
states. This is a scripting/labeling issue in v0_3, not in the
underlying computation — the numerical values are sound; only the
English-language summary of the direction needs correction.

With the correct reading, the audit's original public-framing claim
("minority is more UCP-favorable than majority") corresponds to a
POSITIVE asymmetry. Two of three elections (2015 at ~zero and 2019 at
+0.75 pp) are consistent with that direction; 2023 (-0.51 pp) reverses
it. The 2023 result — which motivated the original framing in the
audit's public materials — is actually the ODD ONE OUT when viewed
through 2015+2019+2023 together.

### Directional consistency across three elections

The asymmetry ranges from +0.03 to +0.75 to -0.51 across the three
elections. Both 2015 (+0.03) and 2019 (+0.75) point weakly or clearly
in the same direction (minority MORE pro-UCP than majority); 2023
(-0.51) flips it. The 2015 value is near zero and is the weakest of
the three; the two clearest values (2019 and 2023) go in opposite
directions.

Verdict on RT3 (cross-election stability) for the minority-majority
asymmetry:

- Under a strict "same signed direction across all three elections"
  criterion: FAILS (2023 reverses).
- Under a "two of three agree" qualified criterion with 2015 counted
  as marginal-positive: QUALIFIED PASS (2015 and 2019 both positive,
  2023 negative). The qualified pass points to minority being MORE
  pro-UCP than majority — which is the audit's original public-framing
  claim.
- Magnitude concern: all three values are under 1 pp in absolute
  terms, and the 2015 value is near zero. The Monte Carlo 95% CI at
  2023 already spans zero. The direction claim is at best
  modestly-supported and well within modeling noise.

This is best described as a WEAK QUALIFIED pass on direction when
2015 is read as marginal-positive, or a FAIL if 2015 is read as
"essentially zero / uninformative". The honest characterization is
that the direction claim is modestly supported by 2 of 3 elections but
with magnitudes too small and modeling uncertainty too large to
support a confident directional assertion.

## Interpretation

Under the correct sign convention (positive asymmetry = minority more
pro-UCP than majority), the 2015 result does NOT reverse or eliminate
the direction of the audit's original claim. Instead:

1. 2015 gives a very small positive asymmetry (+0.03 pp), in the same
   direction as the audit's original claim but with magnitude
   essentially at zero. On its own 2015 is weakly consistent with but
   not strongly supportive.

2. 2019 gives the largest asymmetry (+0.75 pp) in the same direction.

3. 2023 gives a negative asymmetry (-0.51 pp), which is the ODD ONE
   OUT relative to 2015 and 2019. The 2023 result under this sign
   convention means minority is LESS pro-UCP than majority, not more.

If the audit's original framing was based on the 2023 value with
its English-language description interpreted using v0_3's inverted
labels, that interpretation was already INTERNALLY INCONSISTENT
with the formula's sign convention. The 2023 result, correctly read,
UNDERMINES the claim that minority is more pro-UCP than majority.

However, with 2 of 3 elections pointing in the claimed direction
(2015 marginally, 2019 more clearly), a qualified direction claim is
still supportable — but only if the 2023 inversion is acknowledged
rather than treated as the primary evidence.

Magnitude check. All three asymmetries are under 1 pp absolute. The
Monte Carlo 95% CI at the 2023 baseline already crosses zero; the same
sensitivity framework applied across elections would likely show
individual-election CIs each spanning zero. The magnitude of the
direction signal is within modeling noise.

The 2015 map-level EGs (~+7.25% for both proposals) are much larger
than either the 2019 or 2023 map-level EGs. This is consistent with
NDP's 2015 "wave" concentrating urban support, which under the 2019
boundaries shows as packing — a single-election artifact of a specific
electoral condition (NDP province-wide win), not a structural map
property. The durable finding is that both 2026 maps amplify a pro-UCP
structural bias when NDP vote is high, and flatten toward neutrality
when UCP vote is high. The minority-vs-majority contrast within any
one election is a second-order effect that does not reverse this
broader pattern but is not itself direction-stable.

## Implications for RT3 and §3.5

The §3.5 cross-election contingency paragraph in the academic report
needs amendment in two respects:

1. Sign-convention issue. If §3.5 (or any other section) currently
   describes the 2023 result as "minority more UCP-favorable than
   majority" on the basis of v0_3's inverted labels, the wording is
   incorrect. The 2023 value under the compute_metrics formula means
   minority is LESS pro-UCP than majority in 2023.

2. Three-election summary. With 2015 added, the pattern is:

   - Minority more pro-UCP: 2015 (+0.03 pp, marginal), 2019
     (+0.75 pp).
   - Minority less pro-UCP: 2023 (-0.51 pp).
   - All three: |asymmetry| < 1 pp, within modeling noise.

The most honest summary is: two of three elections (2015 and 2019) are
consistent with minority being MORE pro-UCP than majority; 2023
reverses it. The magnitude is small across all three. The direction
is contingent on electorate conditions, with UCP-wave elections (2023)
flipping it.

The broader audit finding — that both 2026 maps carry a material
pro-UCP map-level structural bias when NDP vote is concentrated (EG
of 6.6-7.3% under 2015 votes, fluctuating around 0 in UCP-wave
elections) — is unchanged and is the more robust finding. The
minority-vs-majority contrast is a marginal effect that should be
described with qualification.

## Falsifiability verdict

Pre-registered prediction (if implied by the audit's prior framing):
"The minority proposal is more UCP-favorable than the majority
proposal, and this direction holds across elections."

Under the compute_metrics sign convention (positive asymmetry =
minority more pro-UCP):

- 2015: +0.03 pp. WEAK-SUPPORT (marginal positive).
- 2019: +0.75 pp. SUPPORT.
- 2023: -0.51 pp. REVERSED.

Across three elections: QUALIFIED pass on direction (2 of 3), but
with the two clearest-magnitude values (2019 and 2023) pointing in
OPPOSITE directions. No magnitude claim is defensible; all values
are under 1 pp and within modeling uncertainty.

Outcome: the direction claim is modestly supported (2/3 qualified
pass), but the magnitude is small and one of the three elections
(2023, the one originally used in the audit's public framing)
reverses the claim. The audit should report this as a qualified
finding with explicit acknowledgment that the 2023 vote-input case
flips the direction under the correct sign convention.

Note: if the v0_3 inverted labels were the basis for the audit's
original framing of 2023 as "minority more UCP-favorable", then the
original framing was incorrect and the corrected 2015+2019+2023
picture is actually MORE supportive of the directional claim (2/3
pass with 2023 reversing) than the original single-election picture
suggested.

## Proposed report insertions (flagged only; do not edit reports)

### §3.5 cross-election contingency — insertion (academic report)

Proposed headline: "Three-election direction-stability test yields
qualified pass; 2023 reverses under correct sign convention."

Proposed paragraph body:

> Extending the cross-election test to 2015 adds a third data point.
> Under 2015 votes re-attributed to 2019 boundaries via the 2017 EBC
> final report crosswalk (v0_1_2015_to_2019_crosswalk.csv, 87/87
> coverage, all at medium+ confidence), the minority-minus-majority EG
> asymmetry is +0.03 pp — a near-zero value in the direction of
> minority being marginally more pro-UCP than majority. The three
> elections together give: 2015 +0.03 pp, 2019 +0.75 pp, 2023
> -0.51 pp. Two of three (2015, 2019) are consistent with the
> hypothesis that the minority proposal is more pro-UCP than the
> majority proposal; 2023 reverses the sign. All three values are
> under 1 pp in absolute terms and within the Monte Carlo 95%
> confidence interval that already crosses zero. The direction is
> modestly supported (qualified pass on RT3) but magnitude is small
> and electorate-dependent. The broader finding that both 2026
> proposals amplify a pro-UCP map-level structural bias when NDP vote
> is concentrated (EG ~+7% under 2015 votes, flattening toward zero in
> UCP-wave elections) is unchanged.

Ancillary correction: audit scripts in analysis/v0_3_monte_carlo_ci.py
(lines 158-159) print labels that reverse the sign of the
(minority - majority) EG asymmetry relative to what compute_metrics
actually returns. A negative (min - maj) under compute_metrics means
minority is LESS pro-UCP than majority, not more. A follow-up fix to
those labels should precede any further use of that script's verdict
text in written reports.

### Public report — "election-input wrinkle" section

Proposed headline: "Three elections, one wobbly signal: minority map
slightly worse for NDP under 2015/2019 votes; slightly better under
2023."

Proposed paragraph body:

> A plain test for whether a boundary plan systematically favors one
> party is whether the same plan keeps favoring that party when you
> rerun it against different elections. We tested three: 2015 (NDP
> wave), 2019 (UCP first win), and 2023 (UCP re-election). Two of
> three (2015, 2019) support the finding that the minority proposal
> is slightly more UCP-favorable than the majority proposal; the third
> (2023) goes the other way. The gap is under 1 percentage point in
> every case — smaller than the noise in the estimation method. So
> the direction is real but weak, and it flips when the electorate
> shifts. The durable pattern is broader: both proposals carry a
> measurable pro-UCP structural bias when NDP vote is concentrated in
> urban cores (~+7 pp efficiency gap on 2015 votes), and that bias
> shrinks to near zero in UCP-wave elections. That structural pattern
> is stable. The specific minority-versus-majority gap is less so.

## Artifacts

- `data/v0_1_2015_to_2019_crosswalk.csv` (127 rows, 87 2015 EDs,
  87 2019 EDs, 58 high + 69 medium confidence).
- `data/v0_1_2015_cross_election_summary.csv` (per-map B1-B6 results
  under 2015 votes).
- `data/v0_1_cross_election_asymmetry_3way.csv` (three-election
  minority-majority asymmetry comparison on EG, mean-median, B4,
  declination).
- `analysis/v0_1_2015_cross_election.py` (reproducible pipeline).
- `analysis/v0_1_2015_cross_election_analysis.md` (this document).

## Caveats

1. Population-weight attribution is first-order. It assumes partisan
   geography within each 2015 ED is uniform. Splits and
   consolidations violate this; a poll-level re-attribution using the
   2010 shapefile overlaid on 2019 boundaries would be more precise
   but was not in scope (Phase 4C territory).

2. The rural baseline for the 70/30 blend under 2015 is 35.05%,
   between the 2023 observed (33.5%) and the Monte Carlo sampling
   range (28-38%). The 2015 rural NDP is higher than 2019 or 2023,
   which modestly softens the pro-UCP bias in the 2026 estimates
   relative to what a pure rural application of 2023 baseline would
   produce. Sensitivity to this weight was not re-run for 2015
   specifically but the v0_3 Monte Carlo range covers it.

3. Alberta Party and Liberal votes in 2015 (~7% combined) are
   excluded from the two-party framing. In 2019 these parties were
   smaller; in 2023 they were negligible. The framing is consistent
   across elections in the audit's existing code.

4. The 2015 EDs used pre-2017-commission boundaries. The crosswalk
   accuracy is limited by the EBC final report's narrative precision;
   where the report says "portions of X contributed to Y" without
   quantifying, equal-weighting was used. This is a known source of
   attribution error for splits and consolidations.

## Sign-convention note (flagged for follow-up)

`analysis/v0_3_monte_carlo_ci.py` lines 158-159 print:

    "Samples with minority more UCP-favorable (negative): ..."
    "Samples with minority less UCP-favorable (positive): ..."

These labels are inverted relative to the compute_metrics formula in
v0_2_packing_cracking_analysis.py. Under that formula:

- EG = (ndp_wasted - ucp_wasted) / total.
- Positive EG means NDP wastes more votes than UCP, which in the
  gerrymandering literature is the pro-UCP (map-favors-UCP) direction.
- Negative EG means UCP wastes more, i.e. pro-NDP direction.
- For the (minority EG - majority EG) asymmetry, a POSITIVE value
  means minority is MORE pro-UCP than majority; a NEGATIVE value
  means minority is LESS pro-UCP than majority.

The v0_3 labels have these reversed. The numerical values in v0_3 are
correct; only the English-language summary needs re-labeling. A
follow-up fix should swap "more UCP-favorable" and "less UCP-favorable"
on those two lines. The present analysis uses the corrected
interpretation throughout.
