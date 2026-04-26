# v0.1 Red Deer-Sylvan Lake — "8% of Red Deer's School-Aged Population" Magnitude Check

**Date:** 2026-04-26
**Scope:** Substantiate or revise the public-report claim that the school division shared between Red Deer and Sylvan Lake "contains 8% of Red Deer's school-aged population." Verdict: **The 8% figure is not derivable from any data file in the audit and is incorrectly framed; the underlying qualitative finding (Red Deer city and Sylvan Lake are in entirely separate school divisions with no shared catchment) is strongly supported and should be the public-report wording.**

## Source the minority cites

Appendix E, p. 351 (R11 in the audit's rationale inventory). The minority frames the Red Deer-Sylvan Lake hybrid as a community-of-interest pairing. The exact verbatim language from the inventory: *"By placing rural populations in the same electoral division as urban communities in the Hwy 2 corridor, it is possible to achieve effective representation and overcome challenges with dividing communities of interest that existed in previous electoral divisions."*

The "shared school division" framing in the public-report bullet is the audit's gloss on a broader R11 rationale that includes "go to school" language alongside work and social-life arguments. The minority does not, in Appendix E, cite a specific *named* school division shared by both populations — the audit's interpretation in `v0_1_school_division_coherence.md` is that the rationale invokes shared schools as one of several glue-factors.

## Test method

The "8% of Red Deer's school-aged population" claim could in principle be substantiated by one of three data extractions:

1. **StatsCan Table 17-10-0142-01** ("Public elementary-secondary education statistics, school year") — publishes K-12 enrolment by Alberta school authority, including Red Deer Public Schools, Red Deer Catholic Regional Schools, and Chinook's Edge School Division. From this: total K-12 enrolment in each authority, and the number/share of those students who reside in the City of Red Deer.
2. **Alberta Education's annual "Student Population by Grade" data** (publicly released via `open.alberta.ca`, dataset "Student population by grade and authority") — gives per-school enrolment with school name and authority.
3. **StatsCan 2021 Census Profile Table 98-10-0019-01** ("Population by selected age groups by census subdivision") — gives age-bracket counts including 5–19 year olds, by CSD. From this: City of Red Deer 5–19 population; Sylvan Lake CSD 5–19 population; for context, the absolute numbers of school-aged residents in each.

**None of these three datasets are in the audit's `data/` folder.** A grep over all CSV headers in `data/` for "income," "age," "median," "demographic," "dwelling," "tongue," or "immigrant" returns zero matches. The audit's only public-source numerical files for population are dissemination-area (DA) totals (`alberta_2021_da_populations.csv`) and CSD totals (`alberta_2021_csd_populations.csv`); neither breaks population down by age.

The claim "the shared school division contains 8% of Red Deer's school-aged population" is also internally confused: there *is no shared school division* between Red Deer and Sylvan Lake. The qualitative finding from `v0_1_school_division_coherence.md` is that Red Deer City is served by Red Deer Public Schools (City of Red Deer territory only) and Red Deer Catholic Regional Schools (City + partial county), while Sylvan Lake is in Chinook's Edge School Division No. 73 (central-Alberta rural). These divisions do not share a catchment. So the 8% figure cannot mean "the share of Red Deer students who attend a school in the shared division" because no such shared division exists.

A more charitable reading of the public-report wording: "the shared school division contains 8% of Red Deer's school-aged population" might mean *"the rural school division (Chinook's Edge) on the minority's hybrid side contains a number of K-12 students equal to ~8% of Red Deer's school-aged population."* That reading is testable from publicly available data even though it requires StatsCan and Alberta Education numbers the audit has not pulled.

## Data sources

- **Red Deer city CSD population:** `data/alberta_2021_csd_populations.csv` confirms City of Red Deer (CSD 4806020) population is **100,844**. Sylvan Lake (CSD 4806021) population not listed in the head sample but documented in `v0_1_school_division_coherence.md` as **15,995**.
- **No school-age extraction available** from the audit's `data/`: the StatsCan 2021 Census age-bracket tables (98-10-0019-01 and equivalents) are not downloaded.
- **No Alberta Education enrolment data** in `data/`. The Government of Alberta publishes student counts by authority annually (most recent: 2024–25 school year, Alberta Education Funding Manual Appendix B); these are not in the audit.
- **School-division boundary documentation** is in `analysis/methodology/v0_1_school_division_coherence.md` (uses Alberta Education's school-authority directory and division-by-division descriptions verified via web search).

## Findings

**The 8% figure cannot be substantiated from any file in the audit's `data/` or `analysis/` folders.** No dataset in the audit decomposes Red Deer's school-aged population, no dataset extracts Chinook's Edge enrolment by residence, and no dataset extracts the share of any school division served from Red Deer city neighbourhoods.

**Order-of-magnitude estimate from public sources** (offered as a sanity check, not as a substitution for filed evidence):

- If Red Deer city's 100,844 residents follow the Alberta-wide age structure, approximately 18% are aged 5–19 (Statistics Canada 2021 Census, age structure of Alberta). That gives ≈18,150 school-aged residents in Red Deer city.
- Chinook's Edge School Division's most recent published enrolment is approximately 11,500 K-12 students across all of central-Alberta rural territory (Innisfail, Penhold, Olds, Sylvan Lake, Didsbury, Carstairs, Three Hills, etc., plus surrounding rural). Sylvan Lake-area schools within Chinook's Edge (H.J. Cody Senior High, Steffie Woima Elementary, Beacon Hill Elementary, Mother Teresa Catholic — Mother Teresa is RDCRS, not Chinook's Edge) account for roughly 2,000–2,500 students per Alberta Education's authority report.
- 2,000 / 18,150 ≈ 11%. The "8%" figure is in the right order of magnitude but not exactly recoverable from public-source quick-math; the actual ratio depends on whether the comparison is "Sylvan Lake area enrolment vs Red Deer city school-age population," "Chinook's Edge total enrolment vs Red Deer city school-age population," or some other framing.

**The order-of-magnitude check is not a substitute for filed evidence.** None of the three numbers above (Red Deer 5–19 population; Chinook's Edge total enrolment; Sylvan Lake-area Chinook's Edge enrolment) is documented in an audit data file. A reader cannot trace the 8% figure back to a primary source via the audit's existing files.

**The qualitative finding is strongly supported.** `v0_1_school_division_coherence.md` documents that Red Deer city kids attend Red Deer Public or Red Deer Catholic; Sylvan Lake kids attend Chinook's Edge; the two student populations do not overlap in any standard catchment. This is the durable finding regardless of what magnitude figure the public report cites.

## Verdict

**Unsubstantiated on the "8%" magnitude as written.** The qualitative claim ("Red Deer city and Sylvan Lake are in different school divisions with no shared catchment") **Stands**, but the specific 8% figure is not in any audit file and the order-of-magnitude check produces ~11% rather than 8%, suggesting the figure may be either (a) an estimate from a source not transcribed into the audit, (b) a quick mental calculation that has not been documented, or (c) a placeholder that was not replaced before publication.

The wording "the shared school division contains 8% of Red Deer's school-aged population" is also internally confused: there *is* no shared school division. The intended meaning is probably "the school division on the rural side of the hybrid (Chinook's Edge) accounts for approximately 8% of the school-aged population of the urban side of the hybrid (City of Red Deer)" — which is a different and more complex claim.

## Reproducibility

To substantiate the 8% figure, a third party would need to:

1. Pull StatsCan 2021 Census Table 98-10-0019-01 (population by age group, by CSD), filter to City of Red Deer (CSD 4806020) and Sylvan Lake (CSD 4806021) and the Chinook's Edge service-territory CSDs (Innisfail town 4806011, Sylvan Lake town 4806021, Didsbury 4806009, Olds 4806014, Three Hills 4805017, Carstairs 4806010, Penhold 4806012, plus surrounding rural Red Deer County 4806022 and Mountain View County 4806011 portions).
2. Pull Alberta Education's annual Student Population by Grade and Authority (`open.alberta.ca` dataset, most recent year). Filter to Red Deer Public Schools, Red Deer Catholic Regional Schools, and Chinook's Edge School Division No. 73.
3. Compute the relevant ratio. The "8%" figure could be any of: (a) Sylvan Lake area Chinook's Edge enrolment / Red Deer city K-12 total; (b) Sylvan Lake town K-12 enrolment / Red Deer city K-12 total; (c) Sylvan Lake CSD school-age population / Red Deer CSD school-age population. Without the audit's own source documentation, the audit cannot say which calculation produced the 8%.

This work is straightforward (a few hours of data extraction and arithmetic) but has not been done. None of the three intermediate files exist in the audit's `data/` or `.temp/`.

## Public-report implication

**The current public-report sentence (line 200) — "Red Deer attached to Sylvan Lake: minority commissioners said shared school division; the shared school division contains 8% of Red Deer's school-aged population. **Fail (on magnitude).**" — should be revised because (a) the 8% figure is unsubstantiated, and (b) the framing "the shared school division" is internally inconsistent with the audit's documented finding that there is no shared division.**

**Suggested rewrites, in declining order of evidentiary strength:**

**Rewrite A (preferred, matches filed evidence exactly).** "Red Deer attached to Sylvan Lake: minority commissioners said shared school division and 'go to school' community-of-interest; Alberta Education's published division boundaries say Red Deer city is served by Red Deer Public Schools and Red Deer Catholic Regional Schools (city-only catchments); Sylvan Lake is in Chinook's Edge School Division No. 73 (central-Alberta rural). The two student populations do not share a school in the standard public catchment. **Fail.**"

**Rewrite B (preserves magnitude framing, substantiable form).** "Red Deer attached to Sylvan Lake: minority commissioners said shared school division; in fact, Red Deer city and Sylvan Lake are in entirely different school divisions (Red Deer Public + Red Deer Catholic for the city; Chinook's Edge for Sylvan Lake), and the rural division on the hybrid side contains a small fraction (under 15%) of the school-aged population the urban side contains. **Fail.**"

**Rewrite C (only if the 8% calculation is filed before publication).** Substantively the same as the current public-report bullet, but with a new methodology file documenting the 8% calculation step-by-step from StatsCan and Alberta Education sources. The required sources are publicly available; the calculation is small but has not been done.

**Recommendation: adopt Rewrite A.** It removes the unsubstantiated magnitude figure entirely and replaces it with the audit's strongly-documented qualitative finding. The qualitative finding is itself sufficient to support the **Fail** verdict on the rationale: the minority claimed shared schools, and there are no shared schools. The magnitude was rhetorical filler that adds no analytic weight to the verdict and exposes the audit to a hostile-reviewer attack.

## Files

- This file: `analysis/methodology/v0_1_red_deer_sylvan_lake_school_age_magnitude.md`.
- Cross-references: `analysis/methodology/v0_1_school_division_coherence.md` (R11 verdict and Red Deer-area subsection); `analysis/methodology/v0_1_minority_rationales_validation.md` §R11; `report_academic.md` §5.9.6 Claim 6.
- Source files that *would need to be added* to substantiate the 8% figure: a StatsCan Census 2021 age-bracket extraction for Red Deer-area CSDs; an Alberta Education enrolment-by-authority extraction for the relevant divisions.

## Caveats

- The order-of-magnitude estimate (~11%) above uses the Alberta-wide 5–19 age-share applied to Red Deer's CSD total, plus a rough enrolment estimate for Sylvan Lake-area Chinook's Edge schools. Both numbers are public-source quick-math, not filed extractions. Red Deer's actual age structure may differ from the provincial average (Red Deer has historically slightly younger demographics than the provincial mean, which would push the 5–19 share above 18%). The order-of-magnitude check should not be cited as audit-grade evidence.
- The claim "8%" might originate in a source the audit is aware of but has not transcribed (e.g., a public submission to the EBC, a media report, an Alberta Education news release). If that source can be produced, the audit can revise this file to either substantiate or contradict it.
- The qualitative finding (different school divisions, no shared catchment) does not depend on the magnitude. The **Fail** verdict on the rationale is robust to the magnitude question.
