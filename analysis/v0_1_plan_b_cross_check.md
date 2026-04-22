# v0.1 Plan B Cross-Check — Data-Source Compliance and Best-Available-Data Re-Run

**Purpose.** Two goals. First, determine what population data the Alberta
Electoral Boundaries Commission Act requires the commission to use, and
compare that to what each side of the commission says it used and what each
side actually used in its variance tables. Second, re-run the five
justification tests from `analysis/v0_1_justification_tests_findings.md`
using the most-recent-available population data, so that the audit's
findings can be tested independently of any data-source question.

---

## Phase 1 — Statutory Compliance

### Section 12 of the Electoral Boundaries Commission Act

The verbatim statutory text, from the Act (RSA 2000 c E-3) as reproduced on
page 27 of the commission's final report:

> **12 (1)** For the purposes of this Part, the population of Alberta is
> to be determined by the Commission in accordance with this section.
>
> **(2)** In this section, "decennial census" means the most recent
> decennial census of population referred to in section 19(3) of the
> Statistics Act (Canada) from which the population of all proposed
> electoral divisions is available.
>
> **(3)** Subject to subsections (4) and (5), the Commission is to use
>
>   (a) the population information as provided in the decennial census, and
>
>   (b) information respecting the population on Indian reserves that are
>       not included in the decennial census, as provided by the Department
>       of Indian Affairs and Northern Development (Canada).
>
> **(4)** If there is a province-wide census that is more recent than the
> decennial census and from which the population of all proposed electoral
> divisions is available, the Commission is to use
>
>   (c) the population information as provided in the province-wide census,
>       and
>
>   (d) information respecting the population on Indian reserves that are
>       not included in the province-wide census, as provided by the
>       Department of Indian Affairs and Northern Development (Canada).
>
> **(5)** The Commission may, as it considers appropriate, use more recent
> information respecting the population of all or any part of Alberta in
> conjunction with the information referred to in subsection (3) or (4).

The Act is permissive about adding newer data, not substituting for the
decennial census. Subsection (3) is mandatory ("is to use"). Subsection (4)
applies only if a province-wide census has occurred — Alberta has not run
one. Subsection (5) permits supplementing subsection (3) data with more
recent information, but only "in conjunction with" the decennial census,
not in place of it.

### What the commission says it used

The majority's §III (pp. 27–29) is explicit:

> "This Commission was unanimous in agreeing to use the 2021 decennial
> census (updated to a July 1, 2024, estimate by the Alberta Treasury
> Board's Office of Statistics and Information) as the population of
> Alberta."

The minority's §III (pp. 295–297) uses the same basis:

> "The Commission concludes that the 2021 census figures, updated and
> supplemented by OSI population estimates produced by Alberta Treasury
> Board, represent the best available population data."

Both reports cite Alberta's total population as 4,888,723 and derive the
quota (54,929), the -25% floor (41,197), and the +25% ceiling (68,661) from
that figure.

### What the commission actually used

The 4,888,723 figure is the Alberta Treasury Board Office of Statistics and
Information July 1, 2024 mid-year population estimate. The 2021 Census of
Population total for Alberta was 4,262,635 (p. 27 of the majority report
and p. 296 of the minority report both acknowledge this). The difference is
626,088, roughly 14.7%.

Every per-district figure in both the majority's table (Appendix A) and the
minority's table (Appendix E, pp. 357–358) derives from the July 2024 TBF
estimate, not the 2021 decennial census. The ED-level numbers are OSI
dissemination-area estimates aggregated to the commission's proposed
boundaries.

### Compliance verdict

Section 12 is clear that the decennial census is the mandatory primary
source under s.12(3). It permits supplementation under s.12(5) "in
conjunction with" the decennial data. Neither report presents its
population tables as conjunctions of 2021 census figures and 2024
supplements — both reports present only the 2024 estimate and calculate the
quota directly from it. On a strict reading of s.12(3) and s.12(5), this is
**non-compliant** with the Act's stated primary basis; on a generous
reading, it is permissible under s.12(5) because it is "more recent"
information and the Act does not forbid using the supplement as a
stand-alone basis.

This is a legal-interpretation question, not a factual one. What the audit
can say factually is this: both reports assert that they used the
"decennial census updated to a July 1, 2024 estimate," but what they in
fact used is the July 1, 2024 estimate on its own. No intermediate step
shows the 2021 census numbers being used in conjunction with the 2024
supplement. This is **inconsistent with the commission's own stated
methodology** as a matter of fact, and **potentially non-compliant with
s.12(3) and s.12(5) of the Act** as a matter of statutory interpretation,
depending on how tightly "in conjunction with" is read.

### Compliance table — specific population citations

Each claim below is a specific population figure or derived quantity that
appears in one of the reports. The "verified source" is what the figure
actually is, cross-checked against the 2021 Census CSD populations
(StatsCan table 98-10-0005) and the Alberta Regional Dashboard 2024 and
2025 TBF estimates.

| # | Claim (and location in report) | Reported source | Verified source | Verdict |
|---|-----|-----|-----|-----|
| 1 | Alberta total = 4,888,723 (majority p. 29; minority p. 297) | "2021 census updated to July 1, 2024 estimate" | TBF OSI July 1, 2024 estimate (2021 census was 4,262,635) | **PARTIAL** — the 2024 estimate is permissible as a supplement under s.12(5); calling it the "decennial census" in §III text is factually inaccurate |
| 2 | Provincial quota = 54,929 (both reports) | Derived from #1 / 89 | Derived from 2024 estimate only | **PARTIAL** — derivation follows from #1; inherits #1's characterization issue |
| 3 | Floor 41,197 / ceiling 68,661 (both reports) | Derived from #2 | Derived from 2024 estimate only | **PARTIAL** — same as #2 |
| 4 | Majority 89 per-ED populations (Appendix A table) | Commission's text says 2021 census updated to 2024 estimate | OSI DA-level 2024 estimates aggregated to proposed EDs | **PARTIAL** — per-ED numbers reflect 2024 estimates, not 2021 census |
| 5 | Minority 89 per-ED populations (Appendix E, pp. 357–358) | Same stated basis as majority | Same basis: OSI 2024 estimates | **PARTIAL** — same as #4 |
| 6 | Airdrie East = 50,797 (minority p. 358, entry 52) | 2024 TBF estimate (implied by §III basis) | OSI 2024 estimate of a geographic subset of the city plus adjacent rural | **COMPLIANT** on the minority's stated basis |
| 7 | Calgary-Airdrie = 58,820 (minority p. 357, entry 2) | 2024 TBF | OSI 2024 | **COMPLIANT** |
| 8 | Olds-Three Hills-Didsbury = 49,436 (minority p. 358, entry 76) | 2024 TBF | OSI 2024 | **COMPLIANT** — but see Test 1 below: the claim that the district's population justifies the contested Airdrie inclusion fails even on this 2024 basis |
| 9 | Rocky Mountain House-Banff Park = 38,298 (minority p. 358, entry 82) | 2024 TBF, s.15(2) invoked | OSI 2024 | **COMPLIANT** on data source; the s.15(2) pass-criterion analysis is a separate question (see §A3 of the main audit) |
| 10 | Chestermere-Strathmore = 52,982 (minority p. 358, entry 58) | 2024 TBF | OSI 2024 | **COMPLIANT** |
| 11 | Red Deer 4-way minority EDs (pp. 358, entries 78–81, totals ~214,422) | 2024 TBF | OSI 2024 | **COMPLIANT** on data source; see Test 4 — forcing claim still fails |

Count: **0 pure COMPLIANT with the stated Act-primary basis**, **3
PARTIAL** (items 1–3 are the foundational quota derivation, which
inherits the characterization issue), **8 COMPLIANT with the commission's
self-declared 2024 basis** for per-ED figures. The characterization
problem is a text-level issue in §III of both reports. The per-ED numbers
are internally consistent with the 2024 basis the commission actually
used.

**Load-bearing finding.** For the audit's justification-test framework,
none of the contested-configuration conclusions depend on whether the
commission used 2021 or 2024 data — Plan B re-runs below demonstrate this.
But the characterization issue is independently relevant: both reports
tell readers they used the 2021 decennial census when they did not. This
is inconsistent with stated methodology.

---

## Phase 2 — Plan B Data Acquisition

### Sources attempted and outcomes

| Source | URL | Outcome |
|---|---|---|
| Alberta Treasury Board & Finance municipal estimates | https://open.alberta.ca/opendata/alberta-population-estimates-data-tables | **Partial** — 403 on direct fetch; figures reached via Alberta Regional Dashboard (same underlying dataset) |
| Alberta Regional Dashboard | https://regionaldashboard.alberta.ca/ | **Success** — 2025 TBF estimates for all contested-config municipalities, last updated Jan 16 2026 |
| Alberta Municipal Affairs 2024 population list (PDF) | https://open.alberta.ca/dataset/daab9fce-c2f6-49d1-a433-375b2b7aee24/ | **Success** — saved to `.temp/ma_municipal_affairs_population_list_2024.pdf`; mixed basis (2021 census for most entries, 2024 municipal census for the 23 municipalities that ran one) |
| City of Calgary 2024 Civic Census | https://www.calgary.ca/info-requests/civic-census.html | **Blocked** — program cancelled in the 2020 SAVE budget; last civic census was 2018; next one scheduled for 2027 |
| City of Airdrie 2024 municipal census | https://www.airdrie.ca/ | **Success** — 85,805 as of April 1, 2024 (per city bylaw-mandated municipal census) |
| City of Red Deer | https://www.reddeer.ca/ | **Success via dashboard** — 115,409 in 2025 (TBF estimate; Red Deer discontinued its municipal census program in 2019) |
| City of Edmonton | Treasury Board only (discontinued municipal census in 2019) | **Success via dashboard** — ~1.2M in 2025 |

Consolidated output: **`data/v0_1_alberta_population_plan_b.csv`**. Columns
match the output contract: `municipality, csd_code, pop_2021_census,
pop_latest_source, pop_latest_year, pop_latest_value,
pct_change_2021_to_latest`. 39 rows covering every municipality that
appears in the five contested-configuration tests plus the major cities.

### Blocks documented

The only genuinely blocked item is ward-level or community-level Calgary
population for 2024 or 2025. Calgary's civic census was cancelled in 2020
and does not resume until 2027. The StatsCan 2021 Census Dissemination
Area file exists at the sub-CSD level, but no 2024 or 2025 refresh has been
published at that granularity. This means A2 (the Calgary NE/central vs
S/W gap) cannot be independently re-tested with post-2021 sub-CSD Calgary
data under Plan B.

---

## Phase 3 — Plan B Re-Run

All five tests use the commission's own quota (54,929), floor (41,197), and
ceiling (68,661). The only change under Plan B is the population figure for
each municipal component: Plan A uses the 2021 StatsCan CSD file
(`data/alberta_2021_csd_populations.csv`); Plan B uses the 2025 Alberta
Regional Dashboard / TBF values from `data/v0_1_alberta_population_plan_b.csv`.

### Test 1 — Olds-Three Hills-Didsbury rural catchment

Rural-only catchment sum, Plan A vs Plan B:

| Component | 2021 Census | 2025 TBF |
|---|---:|---:|
| Mountain View County | 12,981 | 14,776 |
| Kneehill County | 4,992 | 5,037 |
| Olds | 9,209 | 9,679 |
| Didsbury | 5,070 | 5,185 |
| Carstairs | 4,898 | 5,248 |
| Three Hills | 3,042 | 3,564 |
| Trochu | 998 | 1,191 |
| Cremona | 437 | 486 |
| Linden | 704 | 911 |
| Acme | 606 | 651 |
| Beiseker | 754 | 787 |
| **Sum** | **43,691** | **47,515** |
| Deviation vs quota | −20.46% | **−13.50%** |

The Plan B sum is 3,824 higher than Plan A, and the deviation tightens
from −20.5% to −13.5%, moving *further* inside the −25% floor. The minority's
claim that this rural catchment requires an Airdrie slice to reach
population viability is **FAIL** under Plan B, more strongly than under
Plan A.

### Test 2 — Rocky Mountain House-Banff Park

The area criterion is unchanged by population data. The 2019 predecessor
ED (Bill 33 shapefile) is 24,468 km², well above the 20,000 km² threshold
of s.15(2)(a). The NP extension is not required to reach 20,000 km².

The population criterion under Plan B:

| Component | 2021 Census | 2025 TBF |
|---|---:|---:|
| Clearwater County | 11,865 | 12,326 |
| Rocky Mountain House (town) | 6,765 | 8,144 |
| Sundre | 2,672 | 2,683 |
| Rimbey | 2,470 | 2,502 |
| Ponoka County | 9,998 | 10,670 |
| Caroline (2021 stale) | 470 | 470 |
| **Sum** | **34,240** | **36,795** |
| Deviation vs quota | −37.67% | **−33.01%** |

Plan B rural catchment is closer to the floor than Plan A but still below
it (−33% vs quota; 4,402 short of the 41,197 floor). The district cannot be
population-viable from its own geography without some extension — but that
extension does not have to be Banff National Park. A pull into adjacent
populated rural territory (the approach the majority uses with
Lacombe-Clearwater at 55,750) would close the gap. **The NP extension
remains a geographic choice, not a forced consequence of the statutory
criteria.** Same verdict as Plan A.

### Test 3 — Airdrie 4-way split

Plan A: Airdrie 2021 = 74,100. 2-way split = 37,050 per half, requiring
~4,147 adjacent rural residents to reach the 41,197 floor. Verdict: FAIL
(2-way works cleanly).

Plan B: Airdrie 2025 TBF = 92,544; 2024 municipal census = 85,805. Under
TBF 2025, a 2-way split is 46,272 per half — **already above the 41,197
floor with zero rural top-up required**. Under the 2024 municipal census,
2-way is 42,902 per half — still above the floor with no rural top-up
required.

The minority's 4-way split would distribute 92,544 / 4 = 23,136 Airdrie
residents per quarter, requiring an average of 18,061 residents from
adjacent Rocky View County per quarter to reach the floor.

**Plan B verdict: FAIL, strongly.** Airdrie's measured growth since 2021
makes the 2-way split easier, not harder, than Plan A found. A 4-way split
is even more clearly a choice not forced by arithmetic.

### Test 4 — Red Deer 4 districts

Red Deer 2021 = 100,844. Red Deer 2025 TBF = 115,409.

Minimum districts: ceil(115,409 / 68,661) = **2**. A 2-way split at 2025
is 57,704 per district, within the ±25% band (+5.05%). Four districts
would put each at 28,852, requiring 12,345 rural residents per district to
reach the floor.

**Plan B verdict: FAIL, same as Plan A.** The majority plan's two Red Deer
districts remain both the arithmetic minimum and an achieved
configuration.

### Test 5 — Chestermere split

Natural pairing: Chestermere + Strathmore + Wheatland County.

| Component | 2021 Census | 2025 TBF |
|---|---:|---:|
| Chestermere | 22,163 | 31,671 |
| Strathmore | 14,339 | 16,416 |
| Wheatland County | 8,738 | 10,150 |
| **Sum** | **45,240** | **58,237** |
| Deviation vs quota | −17.64% | **+6.02%** |

The natural pairing is now centred near the provincial quota (+6.02%
deviation). No additional territory is required; the pairing is more
viable under Plan B than under Plan A. The minority's split of Chestermere
into a separate Calgary-Peigan-Chestermere district remains unforced by
population math. **Plan B verdict: FAIL.**

### A1 — MAD from provincial mean

The commission's own variance tables for both the majority and the
minority already use the 2024 TBF estimates. Plan B and Plan A are
literally identical at the ED level: the 89 per-ED numbers in both
`data/v0_1_majority_2026_populations.csv` and
`data/v0_1_minority_2026_populations.csv` are 2024 values. The audit's A1
finding (minority MAD 4,707 vs majority 3,180; minority 15 EDs above +10%
vs majority 5) is already a Plan B result.

### A2 — Calgary NE/central vs S/W zone gap

Plan B BLOCKED at the sub-CSD Calgary level. Calgary's Civic Census
program was cancelled in 2020 and does not resume until 2027. Nothing
fresher than the 2021 Census Dissemination-Area file exists for
community-level Calgary population, and StatsCan has not published a 2024
or 2025 DA-level refresh. The audit's A2 finding (minority NE/central
12.2% larger than S/W; majority 0.4%) therefore can only be reaffirmed
under Plan B, not independently re-tested at a finer grain.

The ED-level aggregation used for A2 in the original audit already uses
the commission's own 2024 per-ED numbers, so the gap finding itself does
not change under Plan B. What is blocked is the finer-grained sub-CSD
sanity check that would use fresh community-level counts.

### Side-by-side verdict table

| Test | District | Plan A (2021 Census) verdict | Plan B (2025 TBF / 2024 munic census) verdict | Same direction? |
|---|---|---|---|---|
| 1 | Olds-Three Hills-Didsbury | FAIL (43,691 rural-only; −20.5%) | **FAIL (47,515; −13.5%)** | Yes (stronger) |
| 2 | Rocky Mountain House-Banff Park | FAIL on area (2019 ED = 24,468 km²); pop still below floor | FAIL on area (unchanged); pop 36,795 still below floor | Yes |
| 3 | Airdrie 4-way | FAIL (2-way at 37,050/half works with rural top-up) | **FAIL (2-way at 46,272/half works with zero rural top-up)** | Yes (stronger) |
| 4 | Red Deer 4 districts | FAIL (2 is minimum; achieved) | FAIL (2 is minimum; 2-way averages 57,704/half at 2025) | Yes |
| 5 | Chestermere split | FAIL (natural sum 45,240; −17.6%) | **FAIL (natural sum 58,237; +6.0%)** | Yes (stronger) |
| A1 | Variance MAD | Minority 4,707 vs majority 3,180 | Identical (commission's tables already TBF 2024) | Yes |
| A2 | Calgary zone gap | Minority +12.2%, majority +0.4% | Identical at ED level; BLOCKED at sub-CSD | Yes (reaffirmed, not independently tested) |

**Every test reaches the same verdict under Plan B. Three of the five
justification tests (1, 3, 5) become more decisively a failure of the
minority's forcing claim when tested against the latest data.** No audit
finding is rescued by switching data sources; none is overturned.

---

## Interpretation — What Does This Mean for the Audit?

Three takeaways.

First, the audit's existing findings do not depend on the data-source
question. Whether one uses the 2021 Census (which s.12(3) of the Act
arguably mandates as the primary basis) or the 2024 TBF estimate (which
both commission sides actually used and which s.12(5) permits as a
supplement), the verdicts are the same. The five contested configurations
are unforced by population or area arithmetic.

Second, the specific claim that Airdrie's growth forces a 4-way split does
not survive the growth itself. Airdrie was 74,100 in 2021 and is 92,544 in
2025. A 2-way split was already sufficient in 2021 (needing ~4,100 rural
top-up per half). In 2025 a 2-way split needs zero rural top-up — each
half is already above the −25% floor by itself. The minority's 4-way
configuration is not forced by 2024-era data; it becomes more clearly a
choice.

Third, there is a separate, narrow, factual finding worth recording. Both
reports assert in their §III text that they used the "2021 decennial
census updated to July 1, 2024 estimate." In fact, the per-ED numbers and
the 4,888,723 provincial total are the TBF July 2024 estimate directly,
with the 2021 census figure appearing only as historical context in the
narrative. This is **inconsistent with the commission's own stated
methodology** as a factual matter. It is potentially **non-compliant with
s.12(3) and s.12(5) of the Act** as a matter of interpretation, depending
on how tightly the phrase "in conjunction with" in s.12(5) is read. The
audit does not call this illegal — that is a court's determination. The
audit can say that the basis described in the text is not the basis
actually used in the tables.

This third finding cuts in both directions. On the one hand, it shows
that both commission sides have a characterization issue — neither side's
§III text fully matches what its table contains. On the other hand, it
means the audit's five justification-test findings (which use 2021 Census
numbers as an independent check) are themselves anchored to the statutory
primary basis, not to the supplementary basis the commission itself chose.
Plan B shows that the findings survive on either anchor.

---

## Proposed Report Insertions

The parent session owns `report_public.md`, `report_academic.md`, and
`report.html`. Flagged for parent insertion; do not edit these files
directly.

### Proposed §2.5 insertion for `report_academic.md`

> **§2.5 Data-source compliance and best-available-data cross-check**
>
> Section 12 of the Electoral Boundaries Commission Act directs the
> commission to use the most recent decennial census of population under
> s.12(3), with supplementation permitted under s.12(5) "in conjunction
> with" the decennial data. Both the majority and the minority reports
> state in their §III text that they used "the 2021 decennial census
> updated to a July 1, 2024 estimate by the Alberta Treasury Board's
> Office of Statistics and Information" (majority p. 29; minority
> p. 297). In fact, both reports' variance tables are derived directly
> from the July 1, 2024 TBF estimate — 4,888,723 province-wide — and the
> 2021 census figure of 4,262,635 appears only as narrative context. The
> derivation of the provincial quota of 54,929 and the variance band of
> 41,197 to 68,661 uses the 2024 estimate as the sole basis, not as a
> supplement to the 2021 decennial. This is inconsistent with the
> commission's own stated methodology as a factual matter and arguably
> non-compliant with s.12(3) and s.12(5) of the Act depending on how
> strictly the "in conjunction with" clause is read.
>
> To test whether the audit's findings depend on this data-source
> question, a Plan B cross-check re-ran the five justification tests
> (§3.2–§3.6) using the most-recent-available population data: the 2025
> Alberta Treasury Board estimates from the Alberta Regional Dashboard
> (updated January 16, 2026) for every contested-configuration
> municipality, supplemented by the 2024 City of Airdrie municipal census
> for sensitivity. Calgary's civic census was cancelled in 2020 and does
> not resume until 2027, so sub-CSD Calgary data cannot be independently
> refreshed under Plan B. The full cross-check is documented in
> `analysis/v0_1_plan_b_cross_check.md` and the consolidated population
> table is in `data/v0_1_alberta_population_plan_b.csv`.
>
> **Every test reaches the same verdict under Plan B as under Plan A.**
> Three tests (Olds-Three Hills-Didsbury, the Airdrie 4-way split, and
> the Chestermere split) become more decisively unforced when tested
> against 2025 data: the Olds rural catchment rises from 43,691 to
> 47,515 (deviation tightens from −20.5% to −13.5%); Airdrie's 2-way
> split moves from needing 4,147 rural top-up per half to needing zero
> rural top-up; the Chestermere + Strathmore + Wheatland pairing moves
> from 45,240 (−17.6%) to 58,237 (+6.0%), centred near quota. The
> finding that the five contested configurations are unforced by
> population or area arithmetic is robust to the data-source question
> raised by the commission's §III characterization issue.

### Proposed paragraph insertion for `report_public.md`

The parent session can drop this into the section currently titled
"Were the minority's configurations forced by population math?" or its
equivalent in the public report:

> Both sides of the commission say in their introductions that they
> used the 2021 national census updated with newer Alberta estimates.
> In practice the tables in both reports use the newer Alberta
> estimates — July 2024 figures — on their own. The 2021 census number
> does not appear in their variance calculations. This is a gap
> between what the reports say they did and what they actually did.
>
> We re-checked our five "was the configuration forced?" tests using
> the newest figures we could find (2025 Alberta Treasury Board
> estimates, released January 2026) to make sure our findings were not
> dependent on one data source. Every test reaches the same answer.
> Three of the five tests — Olds-Three Hills-Didsbury, the 4-way
> Airdrie split, and the Chestermere split — are even more clearly
> choices rather than forced arithmetic when we use the newest
> numbers. Airdrie is now 92,544 people. Splitting it 2 ways gives two
> districts of 46,272 each, already above the legal floor of 41,197
> without adding any rural voters at all. A 4-way Airdrie split is not
> forced by the math. It is a choice.

---

## Reproducibility

- Plan B consolidated table: `data/v0_1_alberta_population_plan_b.csv`
- Plan B re-run script: `analysis/v0_1_plan_b_rerun.py`
- Run: `PYTHONIOENCODING=utf-8 python3 analysis/v0_1_plan_b_rerun.py`
- Commission report PDF: `.temp/commission_report.pdf` (pp. 27–29 for
  majority §III, pp. 295–297 for minority §III)
- Alberta Treasury Board Municipal Affairs 2024 list PDF:
  `.temp/ma_municipal_affairs_population_list_2024.pdf`
- Data sources: Alberta Regional Dashboard
  (https://regionaldashboard.alberta.ca/, 2025 TBF values last updated
  Jan 16, 2026); City of Airdrie 2024 Municipal Census
  (https://www.airdrie.ca/); StatsCan 2021 Census of Population CSD file
  (`data/alberta_2021_csd_populations.csv`).
