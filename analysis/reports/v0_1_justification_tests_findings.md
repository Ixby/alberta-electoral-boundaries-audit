# v0.1 Justification Tests — Findings

**Scope.** Test whether the 2026 Alberta Electoral Boundaries Commission minority
report's (and, in Test 4, the majority report's own) justifications for five
contested electoral divisions are *necessary* by population or area arithmetic.
A **FAIL** verdict means the justification is unforced — a cleaner alternative
was available. A **PASS** means the arithmetic actually does force the contested
configuration.

**Provincial quota (2021 Census).** Average = 54,929. +/-25% window =
**41,197 to 68,661**.

**Data sources.**
- `data/alberta_2021_csds.gpkg` + `data/alberta_2021_csd_populations.csv`
  (StatsCan 2021 CSD populations).
- `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp` (Bill 33 areas in km²).
- `data/v0_1_minority_2026_populations.csv`,
  `data/v0_1_majority_2026_populations.csv` (Commission's own variance tables).

All intermediate values are written to
`data/v0_1_justification_test_inputs.csv`.

---

## Test 1 — Does *Olds-Three Hills-Didsbury* need the Airdrie slice?

**Verdict: FAIL.** The minority's justification is unsupported by population
arithmetic.

The sum of the rural + small-town CSDs that naturally compose an
Olds/Three Hills/Didsbury district is **43,691** (2021 Census):

| CSD | Pop (2021) |
|---|---:|
| Mountain View County | 12,981 |
| Kneehill County | 4,992 |
| Olds, Town | 9,209 |
| Didsbury, Town | 5,070 |
| Carstairs, Town | 4,898 |
| Three Hills, Town | 3,042 |
| Trochu, Town | 998 |
| Cremona, Village | 437 |
| Linden, Village | 704 |
| Acme, Village | 606 |
| Beiseker, Village | 754 |
| **Total** | **43,691** |

43,691 is **above** the 41,197 minimum and well within the +/-25% window
(−20.5% deviation). No Airdrie population is required for this district to be
legally viable.

Cross-check: the majority report's own `Mountain View-Kneehill` (52,432,
−4.55%) demonstrates that an equivalent rural district can be built without
reaching into Airdrie — it simply pulls a small additional rural catchment
instead. The minority chose to dilute Airdrie rather than use either option.

**Population math does not force the Airdrie slice. A non-population
justification is required for that choice.**

---

## Test 2 — Does *Rocky Mountain House-Banff Park* need the national-park extension?

**Verdict (area criterion): FAIL.** The NP extension is not required to meet s.15(2)(a).
**Verdict (population): PASS with caveat.** The district is not population-viable without
*some* extension, but that extension does not have to be Banff National Park.

- The 2019 predecessor, *Rimbey-Rocky Mountain House-Sundre*, has an enacted
  area of **24,468 km²** (Bill 33 shapefile attribute `Km2`). That is already
  **22% above** the s.15(2)(a) 20,000 km² threshold — **without** Banff
  National Park.
- The natural rural catchment (Clearwater County + Rocky Mountain House +
  Caroline + Sundre + Rimbey + Ponoka County) sums to **34,240**, which is
  below the 41,197 minimum (−37.7%). So some territory needs to be added.
- The minority's own figure for `Rocky Mountain House-Banff Park` is **38,298
  (−30.3%)** — still *outside* the +/-25% band. Adding Banff NP doesn't even
  fix the population deficit; the district is flagged as s.15(2)
  exception-eligible either way.

Since (a) the area criterion is already met at ~24,500 km² without the park,
and (b) the population deficit is *not* closed by adding the park, **the NP
extension is not load-bearing for either s.15(2)(a) or population
qualification.** The minority could have satisfied s.15(2) by pulling
adjacent populated rural territory (e.g., reaching further into the
Lacombe-Ponoka catchment, which the majority does with `Lacombe-Clearwater`
at 55,750, +1.49%). The Banff NP extension is a geographic choice, not a
forced consequence of the legal criteria.

---

## Test 3 — Does Airdrie's population force a 4-way split?

**Verdict: FAIL.** 2-way is sufficient.

- Airdrie (City, CY) 2021 population: **74,100** (StatsCan; note: the
  justification's "~84,000" figure appears to be an overstatement relative
  to the Census used for redistribution).
- 74,100 exceeds the 68,661 upper bound by only **5,439**, so the city
  cannot sit inside one district.
- **2-way split:** each half ≈ **37,050**. To reach the 41,197 floor, each
  half only needs **4,147** additional non-Airdrie residents — trivially
  sourced from adjacent rural Rocky View.
- **4-way split (minority):** each quarter ≈ **18,525**, needing **22,672**
  non-Airdrie residents per district.

A 2-way split therefore fits every district cleanly inside the +/-25% band.
Cross-check: the majority's own plan executes exactly this — `Airdrie-East`
(53,809, −2.04%) + `Airdrie-West` (48,145, −12.35%) — two districts, both
legal.

**The minority's 4-way Airdrie split is unforced by population. Any
justification for it must rest on non-population grounds.**

---

## Test 4 — Does Red Deer's population force 4 districts?

**Verdict: FAIL.** 2 districts are the population-required minimum.

- Red Deer (City, CY) 2021 population: **100,844**.
- Minimum districts at the 68,661 ceiling: ceil(100,844 / 68,661) = **2**.
- **Majority plan (2 districts):** `Red Deer-North` 53,798 (−2.06%) +
  `Red Deer-South` 59,123 (+7.64%). Both within +/-8% of quota; both are
  entirely-Red-Deer districts (`is_hybrid = False`).
- **Minority plan (4 districts):** `Red Deer-Blackfalds`, `-Innisfail`,
  `-Lacombe`, `-Sylvan Lake`, all flagged `Rest-hybrid` (each mixes a Red
  Deer slice with a different rural catchment). Each quarter of Red Deer
  (~25,211) must absorb ~15,986 rural residents to clear the 41,197 floor.

2 is both the arithmetic minimum and an achieved configuration. 4 is a
choice, not a requirement. **Population math does not justify splitting
Red Deer 4 ways.**

---

## Test 5 — Is the Chestermere split (into Calgary-Peigan-Chestermere) necessary?

**Verdict: FAIL.** The natural pairing is population-viable without touching
Calgary.

- Chestermere (City) 2021 pop: **22,163** — below the 41,197 floor, so it
  cannot stand alone.
- Natural pairing: Chestermere (22,163) + Strathmore (14,339) + Wheatland
  County (8,738) = **45,240** — a standalone rural/exurban district **within
  the +/-25% window** (−17.6%).
- The minority's own table shows `Chestermere-Strathmore` at **52,982**
  (−3.54%), which already proves the pairing works with only modest
  additional rural territory (~7,742 beyond the three core CSDs above).
  That district is population-viable **without splitting Chestermere**.
- Yet the minority *also* carves a second Chestermere slice into
  `Calgary-Peigan-Chestermere` (52,639, −4.17%). The 2019 predecessor
  `Calgary-Peigan` (Bill 33 shapefile) had all-Calgary boundaries; adding
  Chestermere voters is a net annexation, not a necessity to reach quota.

If `Chestermere-Strathmore` already reaches 52,982 using the full City of
Chestermere plus adjacent rural, a standalone Calgary-Peigan ED can be
re-drawn inside Calgary to reach quota the same way every other Calgary
district does. **The split of Chestermere into a Calgary-hybrid ED is
unforced by population.**

---

## Summary Table

| Test | District | Justification | Verdict |
|---|---|---|---|
| 1 | Olds-Three Hills-Didsbury | Needs Airdrie slice for population | **FAIL** — rural+town sum is 43,691 (within band) |
| 2 | Rocky Mountain House-Banff Park | Needs NP extension for s.15(2)(a) area | **FAIL** — 2019 predecessor is already 24,468 km² |
| 3 | Airdrie | 4-way split forced by population | **FAIL** — 2-way (37,050 each) is sufficient |
| 4 | Red Deer | 4 districts forced by population | **FAIL** — 2 districts are minimum and achieved by majority |
| 5 | Chestermere | Some split unavoidable, and Calgary slice is part of it | **FAIL** — Chestermere + Strathmore + Wheatland = 45,240 (viable) |

All five contested configurations are **unforced by population or area math**.
Cleaner alternatives were arithmetically available to the minority in every
case. This finding is descriptive: it states that the stated population/area
justifications do not, on their own, necessitate the contested boundaries. It
does not attribute motive.

## Reproducibility

- Script: `analysis/scripts/v0_1_justification_tests.py`
- Input table: `data/v0_1_justification_test_inputs.csv`
- Run: `python analysis/scripts/v0_1_justification_tests.py`
