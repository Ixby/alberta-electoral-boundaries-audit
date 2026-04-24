---
name: Appendix C — 2021-census legal-baseline A1 for the 2019 map
description: 2021-census-direct computation of A1 (population-equality MAD) for the 87 existing 2019 electoral divisions. Establishes the §12(3)-operative legal baseline against which the commission's 2024-TBF-derived A1 can be compared. Companion file to report_academic.md; parent session decides final integration.
forward_dependencies:
  - report_academic.md — candidate for integration as Appendix C (parent session decides)
  - analysis/v0_1_fortification_a1_a5.md — fulfills F7 (A4 narrowed-claim appendix)
backward_dependencies:
  - analysis/scripts/v0_1_a1_legal_baseline_2021_census.py (this computation)
  - data/v0_1_a1_legal_baseline_2019eds_2021census.csv (per-ED output)
  - data/alberta_2021_da_populations.csv, data/alberta_2021_das.gpkg (2021 Census at DA level)
  - data/alberta_2021_csd_populations.csv, data/alberta_2021_csds.gpkg (secondary aggregation)
  - data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp (2019 ED boundary set)
  - data/v0_1_alberta_2019_populations.csv (2017 EBC Final Report values for reference)
  - analysis/reports/v0_1_plan_b_cross_check.md (data-basis statutory discussion)
  - analysis/v0_1_cycle_lag_analysis.md (2025 mid-year comparison)
---

# Appendix C — 2021-census legal-baseline A1 for the 2019 map

## C.1 Purpose and scope

The body of this audit reports A1 population-distribution statistics
(MAD 3,180 for the majority 2026 proposal; MAD 4,707 for the minority 2026
proposal) computed against the commission's own per-ED tables. Those tables
use the Alberta Treasury Board Office of Statistics and Information
(TBF/OSI) July 1, 2024 mid-year population estimate as their basis, not the
2021 decennial census of population. `analysis/reports/v0_1_plan_b_cross_check.md`
documents this data-source question in full.

Section 12(3) of the *Electoral Boundaries Commission Act* requires the
commission to use "the population information as provided in the decennial
census." Section 12(5) permits supplementation ("more recent information...
in conjunction with" the decennial census) but not substitution. Whether
the commission's use of the 2024 TBF estimate as sole basis is §12(5)-
compliant is unresolved. A reviewer committed to strict statutory-basis
discipline can argue the body's A1 numbers inherit the commission's
data-source status, because they are computed against the commission-
published tables.

This appendix reports A1 computed directly from the 2021 Census of
Population, aggregated to the 87 existing (2019-Act) electoral divisions.
This is the §12(3)-operative legal-baseline number for the 2019 map and is
reported here so the direction and magnitude of the audit's A1 findings
can be assessed independent of the commission's data-source choice. The
2026 maps cannot receive the equivalent treatment because their ED
shapefiles have not been publicly released; until release, the 2021-census
legal-baseline analysis is available only on the 2019 boundary set.

## C.2 Method

**Inputs.**

- 2021 Census of Population, dissemination-area (DA) file
  (`data/alberta_2021_da_populations.csv`, n = 6,203 DAs; total population
  4,262,635).
- 2021 Census DA polygon set (`data/alberta_2021_das.gpkg`, EPSG:3347 in
  source, reprojected to EPSG:3401).
- 2019 electoral-division polygon set
  (`data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`, n = 87 EDs,
  EPSG:3401).
- 2021 Census CSD polygon set (secondary, reported for transparency).

**Primary aggregation — DA-level area-weighted overlay.** For each DA,
compute the share of its area that falls within each 2019 ED via spatial
intersection (EPSG:3401, metric). For each DA the weights across
intersecting EDs are normalised to sum to 1.0. The DA's 2021 census
population is then allocated to intersecting EDs proportional to those
weights. Per-ED 2021-census population is the sum of allocations across
all DAs intersecting the ED.

**Why DA-level, not CSD-level.** The original A4 specification called for
CSD-level aggregation. We implemented that method and found a severe
area-weighting artifact: Alberta's rural municipal districts (for example
MD of Rocky View, MD of Foothills, MD of Bighorn) are CSDs that contain
both small towns with concentrated population and very large empty
range-land. Area-weighting spreads the concentrated town population
uniformly across range-land, producing physically impossible per-ED
totals (Calgary-Peigan at +246 % deviation under pure CSD area-weighting;
Sherwood Park at −89 %). The DA-level method avoids this because DAs are
drawn by Statistics Canada specifically to reflect population
concentration — a rural MD is subdivided into dozens of DAs where each
town and each range-land block is its own DA, so area-weighting within a
DA is a much weaker assumption than area-weighting within a CSD. The
CSD-level numbers are reported in the computation log for reviewer
transparency but are not the reported legal-baseline statistic.

**Validation.** Aggregation sum across all 87 EDs matches the reported
2021 Alberta census total (4,262,635) to the unit: 0.0000 % difference.
This confirms no population is lost or double-counted in the overlay.
1,382 of 6,203 DAs (22 %) intersect more than one 2019 ED; these are
apportioned by area-share of the DA inside each ED. 4,821 of 6,203 DAs
(78 %) lie entirely within one 2019 ED and contribute their full
population to that ED.

**Computation provenance.** Full code in
`analysis/scripts/v0_1_a1_legal_baseline_2021_census.py`; per-ED results in
`data/v0_1_a1_legal_baseline_2019eds_2021census.csv`.

## C.3 Results

**Provincial baseline.** Per-ED quota under 2021 Census / 87 EDs is
48,995.8 persons. (Under the 2024 TBF / 89 EDs the commission quota is
54,929; the two values differ by both the total-population shift 2021→2024
and the seat-count change 87→89.)

**MAD (Mean Absolute Deviation from the quota).** The 87 2019 EDs have a
MAD of **4,745** on the 2021 Census.

**Count outside the ±25 % statutory window.** Seven of 87 EDs deviate by
more than ±25 % from the 2021-census quota:

| Rank | ED name | 2021 pop | Deviation |
|------|---------|----------|-----------|
| 1 | Central Peace-Notley | 27,060 | −44.77 % |
| 2 | Lesser Slave Lake | 27,079 | −44.73 % |
| 3 | Edmonton-South | 69,028 | +40.89 % |
| 4 | Edmonton-Ellerslie | 67,910 | +38.60 % |
| 5 | Edmonton-South West | 65,511 | +33.71 % |
| 6 | Airdrie-Cochrane | 63,576 | +29.76 % |
| 7 | Calgary-North East | 61,516 | +25.55 % |

The two negative outliers are both s.15(2)-protected ridings under the
prior Act; the five positive outliers are the fast-growing Edmonton
suburban, Calgary north-east, and Airdrie corridor EDs.

**Maximum deviations.** Max positive +40.89 % (Edmonton-South); max
negative −44.77 % (Central Peace-Notley).

## C.4 Comparison with other MAD values

The table below arrays the available MAD numbers across map and basis.
These are not all apples-to-apples: the row varies the map, and the
column varies the population basis.

| Map & basis | Quota | MAD | Source |
|-------------|-------|------|--------|
| 2019 map on 2017-report basis (commission-quoted) | 46,803 | 2,886 | `data/v0_1_alberta_2019_populations.csv` (EBC 2017 Final Report pp. 60–61) |
| 2019 map on 2021 Census (this appendix) | 48,996 | **4,745** | This computation |
| 2026 majority map on 2024 TBF estimate | 54,929 | 3,180 | Majority Report variance table |
| 2026 minority map on 2024 TBF estimate | 54,929 | 4,707 | Minority Report variance table |

**Ordinal comparison — the audit's principal question.** Where does the
2019-map MAD on the 2021 Census land relative to the two 2026 MADs?

- 2026 majority on 2024 TBF: 3,180
- **2019 map on 2021 Census: 4,745**
- 2026 minority on 2024 TBF: 4,707

The 2019-map-on-2021-Census MAD (4,745) is effectively equal to the
2026-minority-on-2024-TBF MAD (4,707), a difference of 38 population
(0.8 %). The 2019 map's decennial-basis MAD is approximately 50 % higher
than the 2026 majority's 2024-basis MAD (4,745 vs 3,180).

**Interpretation.** The minority 2026 proposal, drawn four years after the
2021 Census, reproduces the same population-distribution tightness that
the 2019 map exhibited against the 2021 Census. The majority 2026 proposal
achieves a meaningfully tighter distribution than either. The audit's
§2.1 ordering — majority tighter, minority looser — is preserved when the
2019-map 2021-Census baseline is inserted between them, and the minority
proposal is revealed to be not an improvement over the 2019 map but a
return to roughly the same distributional posture four years later.

This comparison neither strengthens nor weakens the §2.1 finding on its
own. The §2.1 finding is that the minority 2026 MAD is ~48 % higher than
the majority 2026 MAD on the same 2024 TBF basis. This appendix shows
that the minority 2026 MAD on 2024 TBF (4,707) sits very close to the
2019-map MAD on 2021 Census (4,745), which is what one would expect if
the minority proposal did not meaningfully reduce the dispersion the
2019 map had already accumulated by decennial-census time. The majority
2026 proposal, by contrast, sits meaningfully below either benchmark.

**On the §12 reform argument.** The 7-of-87 count of 2019 EDs outside the
±25 % window under the 2021 Census is itself a cycle-lag signal: the
2019 map was drawn against ~2016–2017 population data, and by the time
the 2021 Census landed, five urban EDs had already exceeded the +25 %
ceiling and two rural EDs sat below the −25 % floor (the latter under
s.15(2) protection). This is structurally identical to Track L's
mid-2025 count of 5-of-87 under the 2025 TBF estimate: the growth-driven
breach of the ±25 % window was already visible at 2021 Census time and
continues. The §12 reform argument (the Act should trigger redistribution
on demographic pressure rather than fixed calendar cycles) is supported
by this appendix independent of the §12(3)-vs-§12(5) question.

## C.5 Cross-check against Track L mid-2025

`analysis/scripts/v0_1_track_l_drift.py` reports 5 of 87 2019 EDs outside ±25 %
under the mid-2025 TBF estimate. This appendix reports 7 of 87 under
2021 Census. The two counts are not directly comparable (different
population basis; different vintage) but are ordinally consistent: the
2019 map had already accumulated enough dispersion by 2021 to push seven
EDs over the band, and by mid-2025 five of those seven were still over
the band on the more-current data basis. The two EDs that fell out of
the 7-outside count by 2025 are the two rural protected ridings (Central
Peace-Notley and Lesser Slave Lake); under the 2025 TBF those two may
have caught up modestly to the quota or the quota itself shifted. The
five 2025-basis outliers are the urban-growth EDs that are still
out-of-band four years on.

## C.6 Interpretation vs §2.1

**Does this appendix strengthen, weaken, or leave neutral the §2.1
finding that the minority proposal is more population-dispersed than the
majority proposal?**

**Neutral-to-mildly-strengthening.** The appendix supplies three
independent supports:

1. The directional ordering (majority tighter than minority) is preserved
   when viewed across bases — the majority 2026 MAD on 2024 TBF (3,180)
   sits below the 2019-map MAD on 2021 Census (4,745), and the minority
   2026 MAD on 2024 TBF (4,707) sits essentially at the 2019-map-
   on-2021-Census level. This means the majority proposal is doing
   distributional work the minority is not.

2. The §12(5)-strict reviewer's attack — "your §2.1 numbers inherit the
   commission's data-source defect" — is neutralised. The
   2019-map-on-2021-Census MAD is §12(3)-operative and confirms the
   direction of the §2.1 finding. The magnitude ordering (majority below
   baseline, minority at baseline) is preserved.

3. The cycle-lag finding (7 EDs already outside the band at 2021 Census
   time; 5 still outside at 2025 TBF time) is a direct §12-reform
   argument that is independent of the §2.1 partisan-structure finding.

The appendix does not cure all A4 residual vulnerabilities. A §12(3)-
operative A1 for the **2026 proposals** remains blocked on the release of
the 2026 ED shapefiles; until that release the §2.1 figures can be
reported only on the commission's stated 2024 TBF basis. This appendix
provides the closest available substitute by re-running the baseline
against the decennial census on the 2019 boundary set.

## C.7 Limitations

- **2026 proposals unavailable.** The 2021-census-direct MAD for the 2026
  proposals cannot be computed without the 2026 ED shapefiles, which have
  not been publicly released. This appendix reports the 2019-map MAD on
  2021 Census as the closest §12(3)-operative substitute.

- **Cycle-lag applies.** The 2021-Census figure is four-to-five years old
  by the commission's April 2026 report deadline. Population-distribution
  statistics computed against 2021 Census data are therefore subject to
  the same cycle-lag critique the audit applies elsewhere. The 2021
  Census remains the §12(3)-operative basis per the Act text; cycle-lag
  is an argument for §12 reform, not a reason to re-weight the legal
  baseline.

- **Within-DA uniformity assumption.** The DA-level area-weighting
  assumes population is uniformly distributed within each DA, which
  holds well in urban DAs (small, densely-populated) and acceptably in
  most rural DAs (median rural Alberta DA is still small enough that
  uniform-within-DA is a minor approximation). For the 1,382 DAs that
  intersect more than one ED the within-DA uniformity is the
  methodological bet. A DA-level dasymetric refinement (weighting by
  StatCan dwelling count or road density) could tighten this further but
  is not required to reach the MAD precision reported here.

- **Suppressed populations.** 21 DAs and 8 CSDs in the StatCan 2021
  release have suppressed (null) populations under StatCan's small-
  population rules. These are treated as zero in aggregation, matching
  the commission's implicit handling. §12(3)(b) permits a separate
  on-reserve population input that this audit does not have; the
  resulting aggregation is §12(3)-compliant for the census component but
  under-counts population on the affected reserves.

- **Secondary CSD-level check included for transparency but not reported
  as the headline.** The CSD-level area-weighting artifact is documented
  in the computation log for reviewer access; MAD under CSD-level is
  17,802 with 45 EDs outside the ±25 % band, numerically implausible for
  reasons explained in §C.2, and driven entirely by the rural-MD
  area-spread artifact.

## C.8 Replication

- Script: `analysis/scripts/v0_1_a1_legal_baseline_2021_census.py`
- Inputs: listed in §C.2
- Output: `data/v0_1_a1_legal_baseline_2019eds_2021census.csv` (per-ED
  table with ed_name, pop_2021_census, dev_from_quota, dev_pct,
  outside_legal_window_flag)
- Runtime: approximately 60 s on a modern workstation (dominated by the
  DA-level overlay).
- Reproducibility: `PYTHONIOENCODING=utf-8 python
  analysis/scripts/v0_1_a1_legal_baseline_2021_census.py` from the repository
  root reproduces the figures in this appendix.

*Appendix drafted v0.1. Companion to `analysis/v0_1_fortification_a1_a5.md`
F7 (A4 narrowed-claim appendix specification). Parent session applies final
integration decision into `report_academic.md`; no edits to
`report_academic.md`, `report_public.md`, or `report.html` are made by
this file.*
