---
name: Alberta government administrative databases survey — candidates for a non-partisan sub-provincial population source of truth
description: Inventory, reliability assessment, constitutional-suitability analysis, and composite-basis recommendation for the §12 amendment proposal. Identifies which provincial and federal administrative data sources could serve as a legislatively-recognised population base for electoral-boundary redistribution, and how they should be wired into the Option B composite basis.
forward_dependencies:
  - analysis/reports/v0_1_act_amendment_proposal.md Phase 5 Option B §12(5) — this survey specifies which datasets the statute should name as the composite components and which should be the tie-breaker
  - analysis/reports/v0_1_act_amendment_proposal.md Phase 4 objection 4.2 — this survey sharpens the "political vulnerability of provincial estimates" answer by quantifying which non-provincial cross-checks are available
  - analysis/reports/v0_1_ai_use_recommendations_for_committee.md §2.5 — methodology-level sibling on data-source transparency
backward_dependencies:
  - analysis/reports/v0_1_plan_b_cross_check.md — Track K, empirical anchor that §12(3) is being overridden in practice
  - analysis/v0_1_cycle_lag_analysis.md — Track L, cycle-lag quantification that motivates data-source reform
  - analysis/methodology/v0_1_calgary_data_sources_audit.md — Calgary sub-city source catalogue; this survey is the provincial-scale analogue
  - Alberta Electoral Boundaries Commission Act, RSA 2000 c E-3, §12
  - Constitution Act, 1867, §51
  - Canadian Charter of Rights and Freedoms, §3
  - Statistics Act, RSC 1985 c S-19
  - Alberta Health Care Insurance Act, RSA 2000 c A-20
  - Freedom of Information and Protection of Privacy Act, RSA 2000 c F-25
  - Reference re Provincial Electoral Boundaries (Saskatchewan), [1991] 2 SCR 158
---

# Alberta government administrative databases — survey for the §12 amendment

**Purpose.** The reform proposal's Option B names a "composite basis" built from the Alberta Treasury Board and Finance (TBF) provincial quarterly estimate and the Statistics Canada quarterly provincial estimate (Table 17-10-0009), with a ±2% tie-breaker. Objection 4.2 flags that any rule anchored on a provincial-agency estimate is only as robust as that agency's current independence. This survey inventories every Alberta government administrative database that tracks population at sub-provincial geography on a cadence faster than the decennial census, assesses each for independence, auditability, completeness, and cross-check potential, then recommends which candidate(s) should be written into a reformed §12.

**Scope note.** The survey is desk research built on published Alberta government data catalogues, Statistics Canada release documentation, and the authorizing statutes of each custodian. It does not commission custom tabulations. Where a dataset's public availability has changed recently (municipal census programs, AHCIP coverage rules), the survey records both the status as of 2026-04-22 and the statutory authority under which the custodian could in principle release finer-grained data.

---

## Phase 1 — Inventory of candidate databases

Twelve Alberta government and federally-sourced databases are surveyed below. Each entry records custodian, URL or access path, geography, update frequency, public availability, methodology transparency, and a one-line viability verdict.

### 1.1 Alberta Health Care Insurance Plan (AHCIP) registrations

- **Custodian.** Alberta Health (ministry), administered by Alberta Health Services insurance services.
- **Access path.** Underlying register is closed. Aggregates are released via the Alberta Health Open Government portal (open.alberta.ca) as annual "population by age and sex" tables for Alberta Health Services zones, LGAs (Local Geographic Areas, roughly 70 in Alberta), and in some years sub-municipal neighbourhoods. The micro-level register is not publicly accessible and is governed under the Health Information Act, RSA 2000 c H-5.
- **Geography.** AHS zone (5), AHS sub-zone (~70 LGAs), in some publications Calgary neighbourhood, Edmonton neighbourhood, CSD. Dissemination area is achievable in principle (postal codes link to DAs via the StatsCan PCCF) but is not a published granularity.
- **Update frequency.** Register is continuous. Published aggregates are annual (typically released ~9 months after the reference date).
- **Data source.** Registrations of Albertans for provincial health coverage. Coverage criterion: physical presence in Alberta for the purpose of becoming a resident, continuous physical presence except for temporary absences, and intention to make Alberta one's primary residence (per AHCIP eligibility rules under the Alberta Health Care Insurance Act). Captures roughly 99% of the residents a census would count.
- **Public availability.** Aggregates open; register closed.
- **Methodology transparency.** Partially documented. Eligibility rules are published; coverage gaps (RCMP, military, federal inmates, new arrivals in the 3-month waiting period, Albertans who have left but not de-registered) are known in kind but not quantified in public releases.
- **Viability:** **viable-with-adjustment.** AHCIP is the closest thing Alberta has to a population register. The sub-provincial aggregates published on Open Government include the geographies a commission needs. The adjustment required is (a) publication of the register's coverage gap estimates and (b) a documented reconciliation to StatsCan postcensal provincial totals.

### 1.2 Alberta Treasury Board and Finance (TBF) population estimates

- **Custodian.** Alberta Treasury Board and Finance, Office of Statistics and Information (OSI).
- **Access path.** Public. Alberta Regional Dashboard (regionaldashboard.alberta.ca), open.alberta.ca data portal, and TBF's quarterly population reports.
- **Geography.** Province; Census Divisions (19); Census Subdivisions (municipalities and MDs); AHS zones; Economic Regions; Alberta Regional Economic Development regions. Dissemination area is not published.
- **Update frequency.** Quarterly (Q1–Q4). Municipal-level updates annual, usually published in January with a July reference date of the prior year.
- **Data source.** Component-cohort-survival model calibrated against: StatsCan vital statistics (births, deaths from Vital Statistics Alberta, Act RSA 2000 c V-4), inter-provincial migration from CRA T1 tax-return address changes, international migration from Immigration Refugees and Citizenship Canada administrative records, intra-provincial migration inferred from TBF's annual municipal affairs population lists and AHCIP registration moves.
- **Public availability.** Aggregates open. Underlying admin-record inputs closed (they come from federal CRA and IRCC under data-sharing agreements governed by Statistics Canada Act s. 13 and the bilateral Canada-Alberta information-sharing agreements).
- **Methodology transparency.** Documented. TBF publishes its population projections methodology paper (latest version 2024), the low/medium/high scenario assumptions, and annual reconciliation notes against StatsCan postcensal.
- **Viability:** **viable.** TBF is the database the 2025–26 commission in fact used. Its methodology is documented at a level of detail comparable to StatsCan's.

### 1.3 Service Alberta motor vehicle registrations (driver licence, vehicle)

- **Custodian.** Service Alberta (ministry), registry services delivered through private registry agents under Service Alberta oversight.
- **Access path.** Register is closed. Aggregate counts of active driver licences by postal FSA and municipality are published irregularly in Service Alberta's annual business plan. FOIP requests can yield more detail.
- **Geography.** Address-level in the register. Published aggregates typically at postal FSA or municipality.
- **Update frequency.** Continuous in the register; public aggregates annual at best.
- **Data source.** Driver licence issuance and renewal, vehicle registration. Captures roughly the 16+ licensed-driver population — about 78% of Alberta residents 16+ (per 2021 Census-estimated driving-age population and Service Alberta's ~3.2M active licences). Under-counts youth under 16 entirely, elderly non-drivers, and the ~22% of adults without licences (urban non-drivers, medical exemptions).
- **Public availability.** FOIP-gated for finer-than-annual detail.
- **Methodology transparency.** Undocumented at the aggregate-release level.
- **Viability:** **not-viable as primary.** Licence data is not a population register. Useful as a growth-direction signal for sub-provincial change (because licence addresses update when residents move), but not a population count.

### 1.4 Alberta Education K–12 enrolment

- **Custodian.** Alberta Education (ministry). Enrolment data aggregated from school authorities (public school boards, Catholic school boards, separate school boards, francophone authorities, charter schools, private schools, and home-education programs).
- **Access path.** Public via open.alberta.ca and Alberta Education's annual Student Population Statistics reports.
- **Geography.** School authority (~60+ authorities), school catchment (~2,000+ schools), in some reports municipal breakdown. Ward-level or DA-level is not published.
- **Update frequency.** Annual (Sept 30 count), published ~3 months after.
- **Data source.** Enrolment registrations as reported by school authorities. Captures roughly the 5–17 age band (~17–19% of Alberta's population). Misses pre-K, post-18, home-educators outside the registered program, and students enrolled outside their geographic catchment.
- **Public availability.** Open at school-authority level; finer granularity FOIP-gated.
- **Methodology transparency.** Documented (enrolment count procedures published by Alberta Education).
- **Viability:** **not-viable as primary, viable as growth proxy.** Age-band limitation means it cannot represent total population. Useful as a K–12 growth signal to cross-check TBF age-cohort projections in fast-growth communities.

### 1.5 Alberta Works / Income Support / AISH caseloads

- **Custodian.** Ministry of Seniors, Community and Social Services (SCSS).
- **Access path.** Aggregate caseloads published monthly on open.alberta.ca. Finer geographies FOIP-gated.
- **Geography.** Province, region (~6 SCSS regions), SCSS district office (~25). Sub-district is FOIP-gated.
- **Update frequency.** Monthly caseload counts, published ~2 months after the reference month.
- **Data source.** Income Support caseloads (adults and families receiving provincial income support), AISH caseloads (Assured Income for the Severely Handicapped). Captures roughly 5–7% of the working-age population. Subject to program-specific eligibility.
- **Public availability.** Aggregates open; individual records closed under FOIP and social-services privacy rules.
- **Methodology transparency.** Program eligibility rules published. Aggregation methods documented.
- **Viability:** **not-viable as primary.** Caseload counts are a transfer-payment metric, not a population count. Useful for equity analysis of economic vulnerability by region but not a redistribution base.

### 1.6 Alberta Municipal Affairs annual municipal population list

- **Custodian.** Alberta Municipal Affairs (ministry), Office of the Deputy Minister.
- **Access path.** Public. Published annually as an open.alberta.ca dataset; the 2024 list is the data source for the provincial MSI (Municipal Sustainability Initiative) funding formula and the Basic Municipal Transportation Grant.
- **Geography.** Municipality (city, town, village, summer village, specialized municipality, municipal district, improvement district, special area, Métis settlement). Each CSD as defined by StatsCan has an entry. Approximately 340 rows.
- **Update frequency.** Annual (typically released in Q4 of the following year — the 2024 list is the basis for 2025–26 funding formulas).
- **Data source.** Mixed basis: (a) the most recent StatsCan federal census figure for that municipality, OR (b) the most recent municipal-census figure if the municipality has run one within the statutory window (3 years, Municipal Government Act s. 656), OR (c) a TBF estimate if neither is current. The list publishes the source per municipality.
- **Public availability.** Open.
- **Methodology transparency.** Documented. The "population basis" for each municipality is recorded in the list itself.
- **Viability:** **viable-with-adjustment.** The list is the statutory basis for municipal funding formulas and is already a legally-recognised Alberta government population dataset. Its mixed basis is both its strength (reflects the freshest defensible count per municipality) and its weakness (not a single-vintage uniform dataset). For redistribution, the commission would need a uniform-vintage projection rather than a mixed-vintage list. Useful as a calibration reference point for TBF estimates at the municipal level.

### 1.7 Alberta Labour and Immigration / ESDC Employment Insurance, SIN

- **Custodian.** Federal — Employment and Social Development Canada (ESDC). Alberta's labour market figures published in the Alberta Labour Force Survey, jointly produced with StatsCan.
- **Access path.** Public via StatsCan (Labour Force Survey monthly release, Table 14-10-0287 and others).
- **Geography.** Province, Economic Regions (4 in Alberta: Calgary, Edmonton, rural North, rural South). CMA-level (Calgary CMA, Edmonton CMA). Sub-CMA is not regularly published.
- **Update frequency.** Monthly (LFS); annual consolidated tables.
- **Data source.** LFS is a ~56,000-household sample survey, not administrative. EI claims and SIN registrations are administrative. The composite "Alberta employed labour force" used in policy is LFS-based.
- **Public availability.** Open.
- **Methodology transparency.** Fully documented (LFS methodology, StatsCan technical reports).
- **Viability:** **not-viable as primary.** LFS is a sample survey of a subset of the population (15+ labour force). Too coarse spatially. EI claims and SIN registrations are federal and not released at sub-provincial granularity sufficient for redistribution. Useful for working-age-cohort cross-check at Economic Region level only.

### 1.8 Service Canada / Passport / SIN aggregates

- **Custodian.** Federal — Service Canada (ESDC).
- **Access path.** SIN counts and passport issuance are published in ESDC annual reports at province-level. Sub-provincial is not in the public record.
- **Geography.** Province only in public releases.
- **Update frequency.** Annual.
- **Data source.** SIN issuance (first-time SIN issuance roughly tracks births, naturalizations, and first work-eligible immigration). Passport issuance tracks a subset.
- **Public availability.** Province-level only publicly.
- **Methodology transparency.** Not published at sub-provincial level.
- **Viability:** **not-viable.** Federally held; no published sub-provincial breakdown; federal-provincial data-sharing would be required to obtain usable granularity.

### 1.9 Canada Revenue Agency T1 taxfiler data via StatsCan

- **Custodian.** Federal — Canada Revenue Agency; StatsCan is the aggregator.
- **Access path.** Public. StatsCan Table 11-10-0109 (Taxfilers and dependents, income statistics, for the 98% of Canadian residents who file taxes) and the Postal Area analogue Table 11-10-0082.
- **Geography.** Postal FSA (first three characters of the postal code, ~50 Alberta FSAs), CSD, CMA, economic region. Dissemination area is available in the paid custom-tabulation product (T1 Family File) but is not in the free public release.
- **Update frequency.** Annual (T1 returns for year N are aggregated and released ~16 months after year-end). 2023 tax-year data was released in roughly late 2024.
- **Data source.** Administrative CRA T1 returns. Captures about 95–98% of the 18+ population (non-filers, recent arrivals pre-first-return, and low-income dependents are under-represented).
- **Public availability.** Open at FSA/CSD level. Individual records closed.
- **Methodology transparency.** Documented (StatsCan T1 Family File methodology).
- **Viability:** **viable-with-adjustment.** Taxfiler data is the best federal non-census administrative population source for sub-provincial geography. Under-counts children and recent arrivals but captures nearly all adults. Useful as a cross-check against TBF sub-provincial estimates. Not fine-grained enough at the free-release level for ED-level redistribution without purchasing custom tabulations.

### 1.10 Elections Alberta — Register of Electors

- **Custodian.** Elections Alberta, a statutorily-independent officer of the Legislature under the Election Act, RSA 2000 c E-1, and the Chief Electoral Officer Act.
- **Access path.** The register is maintained continuously. Elections Alberta publishes aggregate enumerations at electoral division (87 current EDs) level, and in statements-of-vote by voting subdivision / voting area. An extract of the register by ED is published with each provincial general election's statement of vote.
- **Geography.** Electoral division (87 current, 89 proposed); voting subdivision (~4,700 VAs at 2023 election). Address-level internally.
- **Update frequency.** Continuous in the register. Published aggregates are election-cycle (every 3–4 years typically). Between elections, Elections Alberta updates the register via address changes notified by Elections Canada (federal National Register of Electors), driver-licence changes, and voter-initiated updates.
- **Data source.** Voter registration. Captures the 18+ Canadian-citizen Alberta-resident population. Excludes non-citizen residents (~9–10% of Alberta adults), non-registered citizens (estimated ~10% under-registration, concentrated among young-adult, renter, and recent-mover populations), and all children. Effectively captures about 75–80% of the total resident population under full-coverage assumptions, declining where registration lapses.
- **Public availability.** Aggregates open at ED and VA level. Individual register closed to the public; candidates and registered political parties receive copies under the Election Act.
- **Methodology transparency.** Documented. Elections Alberta publishes the methodology of the National Register of Electors Alberta component.
- **Viability:** **viable-with-adjustment as a secondary / local-geography check.** Cannot serve as primary because the population it measures (registered 18+ citizens) is not the population redistribution needs (all residents). Useful as a voting-age cross-check for ED-level TBF estimates and as a pure democratic-participation-weighted overlay (the Quebec model).

### 1.11 Alberta Health Services catchment population

- **Custodian.** Alberta Health Services (provincial public agency; functions as an arm's-length body under the Regional Health Authorities Act, RSA 2000 c R-10, though structurally integrated with Alberta Health).
- **Access path.** Public. AHS publishes population by zone and sub-zone in the annual AHS Zone Summary and the Alberta Population Model (available through Interactive Health Data Application, IHDA).
- **Geography.** AHS zones (5: Calgary, Edmonton, North, Central, South). AHS sub-zones (~70 LGAs). CSD in some publications.
- **Update frequency.** Annual.
- **Data source.** Derived from AHCIP registrations plus reconciliation against TBF estimates. AHS does not produce an independent count; it uses AHCIP plus TBF as inputs.
- **Public availability.** Open.
- **Methodology transparency.** Partially documented. Reconciliation method between AHCIP and TBF is described in IHDA technical notes.
- **Viability:** **viable-with-adjustment as a derivative.** AHS population data is effectively AHCIP filtered to a geography. Its viability inherits from AHCIP's — it is not an independent source.

### 1.12 Provincial Vital Statistics (births, deaths)

- **Custodian.** Service Alberta (registry services), under the Vital Statistics Act, RSA 2000 c V-4.
- **Access path.** Public aggregates on open.alberta.ca. Individual records closed.
- **Geography.** Province, Census Division, CSD, AHS zone. Postal-code is in the register.
- **Update frequency.** Monthly registrations; annual consolidated publications.
- **Data source.** Statutory registrations of births and deaths. Captures 100% (statutorily mandatory).
- **Public availability.** Aggregates open; individual records FOIP-gated.
- **Methodology transparency.** Documented.
- **Viability:** **not-viable as a population count; viable as a component.** Vital statistics are inputs to the TBF component-cohort-survival model, not outputs. Useful for cross-checking TBF's natural-increase assumptions but not a direct population source.

### 1.13 Summary inventory table

| # | Dataset | Custodian | Geography (finest public) | Frequency | Source type | Public | Viability |
|---|---|---|---|---|---|---|---|
| 1 | AHCIP registrations (agg.) | Alberta Health | AHS sub-zone (~70 LGAs) | Annual | Registrations | Open (agg.) | **viable-with-adjustment** |
| 2 | TBF population estimates | Treasury Board & Finance | CSD | Quarterly | Component-cohort model | Open | **viable** |
| 3 | Driver licences / MVR | Service Alberta | Municipality / FSA | Annual | Registrations | FOIP-gated | not-viable |
| 4 | K–12 enrolment | Alberta Education | School authority | Annual | Registrations | Open | not-viable as primary |
| 5 | Income Support / AISH | SCSS | SCSS region / district | Monthly | Caseloads | Open (agg.) | not-viable |
| 6 | Municipal Affairs pop. list | Municipal Affairs | CSD | Annual | Mixed | Open | **viable-with-adjustment** |
| 7 | EI / LFS labour market | ESDC / StatsCan | Economic region | Monthly | Sample / admin | Open | not-viable |
| 8 | Passport / SIN agg. | Service Canada | Province | Annual | Registrations | Closed sub-prov | not-viable |
| 9 | CRA T1 taxfiler (StatsCan) | CRA / StatsCan | FSA / CSD | Annual | Tax returns | Open | **viable-with-adjustment** |
| 10 | Register of Electors | Elections Alberta | ED / VA | Continuous | Voter registration | Open (agg.) | **viable-with-adjustment** |
| 11 | AHS catchment pop. | Alberta Health Services | AHS zone / LGA | Annual | Derived from AHCIP+TBF | Open | viable as derivative |
| 12 | Vital Statistics | Service Alberta (VS) | CSD | Monthly | Registrations | Open (agg.) | not-viable as count |

Of the twelve, four candidates warrant Phase 2 reliability assessment as potential primary or major-component sources for a §12 composite basis: AHCIP (1), TBF (2), CRA taxfiler (9), and Register of Electors (10). A fifth (Municipal Affairs list, 6) warrants assessment as a calibration overlay.

---

## Phase 2 — Reliability and partisan-neutrality assessment

For each of the five candidates that cleared Phase 1, the assessment below records: independence from government direction, auditability, completeness of population coverage, and cross-check potential against StatsCan Table 17-10-0142 (postcensal estimates) and the decennial census.

### 2.1 AHCIP registrations

- **Independence.** Alberta Health is a ministry of the Government of Alberta. The AHCIP register is administered under the Alberta Health Care Insurance Act and the Health Information Act, both of which are provincial legislation subject to amendment by the government of the day. The Minister of Health has statutory authority over registration rules. Independence from government direction: **low** at the structural level; **moderate** in practice because the register is operationally embedded and politically sensitive to amend mid-cycle.
- **Auditability.** Aggregates can be reconciled against AHS publications and against StatsCan postcensal figures. The reconciliation is published in TBF's annual methodology paper. A third party cannot audit the register itself without Health Information Act authorization, but can audit the published aggregates for internal consistency and year-over-year coherence.
- **Completeness.** Covers ~99% of the population a census would count. Known gaps: RCMP and Canadian Armed Forces (federally covered), federal inmates (federal penitentiary population), Albertans in the 90-day waiting period for new registration, Albertans who have left the province but have not de-registered (net positive bias), undocumented residents (net negative bias).
- **Cross-check against StatsCan.** Reconciles to StatsCan provincial postcensal estimates typically within ±1% (2021 census year: AHCIP registered ~4.20M vs census 4.26M, a ~1.4% gap closed by the known coverage classes above). Reconciles to decennial census within ~2%.
- **Partisan-neutrality assessment.** The register is robust to short-term political direction because rewriting eligibility criteria would be observable and disruptive. Long-term drift (narrowing or broadening eligibility for partisan-demographic reasons) is structurally possible but would be highly visible. The register itself is run by a civil-service function, not a political office.

### 2.2 TBF (Treasury Board and Finance) quarterly estimates

- **Independence.** TBF is a ministry, with the Office of Statistics and Information reporting through the Deputy Minister of Treasury Board and Finance. OSI's methodology and releases are operationally separate from political direction, but OSI is not a statutorily-independent office (unlike, say, the Auditor General under the Auditor General Act, RSA 2000 c A-46). Independence: **low-to-moderate** structurally. The 2022 establishment of Treasury Board and Finance as a single portfolio did not change OSI's reporting line.
- **Auditability.** Methodology paper is public and reproducible. Inputs (StatsCan vital statistics, CRA migration data, IRCC records) are public or federally-controlled. A third party can re-run the component-cohort model from the published inputs and compare to TBF's published output, within the limits of TBF's proprietary age-cohort disaggregation rules.
- **Completeness.** Full population coverage by construction (the model extrapolates to everyone).
- **Cross-check against StatsCan.** TBF and StatsCan provincial estimates reconcile to within ±1% in most quarters. Historical maximum drift ~2.5% (StatsCan published a different quarterly reference than TBF in one 2022 period due to IRCC data lag). Structurally, both use the same underlying vital-statistics and CRA inputs, so material divergence is not expected.
- **Partisan-neutrality assessment.** TBF's methodology paper is the answer to objection 4.2. As long as the paper remains published and OSI's methodology change log is public, a future government could be challenged if it altered the methodology for partisan reasons. But there is no statutory bar to doing so. The ±2% StatsCan tie-breaker in Option B §12(5) is the external check that makes this safe.

### 2.3 CRA T1 taxfiler data (via StatsCan)

- **Independence.** CRA is a federal agency under the Canada Revenue Agency Act, SC 1999 c 17. StatsCan is a federal agency under the Statistics Act, RSC 1985 c S-19. Independence from Alberta provincial government: **high**. Independence from federal government direction: **moderate** — the Chief Statistician has statutory protection but is federally appointed.
- **Auditability.** Fully documented. T1 Family File methodology is public.
- **Completeness.** ~95–98% of the 18+ Alberta population files a T1 return. Under-counts: children (almost entirely via the family-filer link but not always), very-low-income non-filers (estimated 2–3% of adults), recent arrivals in their first tax year, unhoused populations. The under-count is geographically non-uniform — downtown urban cores and remote Indigenous areas show higher non-filing rates.
- **Cross-check against StatsCan postcensal.** T1 Family File totals reconcile to StatsCan provincial postcensal within ±2% in most years. Cross-check against census: T1 under-counts census population by ~3–5% (the non-filing adults plus children not captured via the family link).
- **Partisan-neutrality assessment.** The least vulnerable to provincial manipulation of the four. CRA is federally administered; StatsCan aggregates the data. Neither is under the Government of Alberta's direction. A hostile provincial government cannot tell CRA to under-count a region. This is a critical independence property for the objection 4.2 answer.

### 2.4 Register of Electors (Elections Alberta)

- **Independence.** Elections Alberta is a statutorily-independent Officer of the Legislature under the Election Act and reports to the Legislative Assembly through the Chief Electoral Officer, not through a minister. Structurally the most independent of the five candidates. Independence: **high**.
- **Auditability.** Aggregates published with each statement of vote and in-between-election updates. The register itself is subject to statutory audit by the Chief Electoral Officer's office; Elections Alberta publishes annual reports.
- **Completeness.** Covers registered 18+ Canadian citizens resident in Alberta. Under-registration is ~10%; non-citizens are not eligible to register. Effective coverage of the total population is ~75–80% — far lower than AHCIP or TBF.
- **Cross-check against StatsCan.** The register and the census are measuring different populations (register: registered citizen voters; census: all residents). Reconciliation requires population-cohort modelling and is not a direct cross-check.
- **Partisan-neutrality assessment.** Structurally the most independent, but measures a partial population. Its use as a secondary / democratic-overlay metric (Quebec's model) is coherent. Its use as the primary basis for redistribution would systematically under-weight communities with high non-citizen or low-registration populations — New Canadians, young adults, rural First Nations.

### 2.5 Municipal Affairs annual population list

- **Independence.** Municipal Affairs is a ministry. The list is compiled from (a) StatsCan census figures (federal, independent), (b) municipal census results (each municipality's independent count, subject to provincial municipal census regulations), and (c) TBF fallback estimates. Independence: **moderate** (the compilation is under provincial control, but the major components come from federally-independent or municipally-independent sources).
- **Auditability.** Each row in the list records its source. A third party can cross-check a city's municipal census (Airdrie 2024, Calgary 2019) against the list's entry.
- **Completeness.** Captures every CSD in Alberta. Internal consistency is high.
- **Cross-check against StatsCan.** The list deliberately uses StatsCan census figures where no municipal census exists, so agreement is structural rather than independent.
- **Partisan-neutrality assessment.** The list is driven by the MSI funding formula, which creates incentive pressure to favour municipalities (especially fast-growing ones) that have completed municipal censuses. This is an indirect partisan-vulnerability: a future government could adjust municipal-census rules to favour or disfavour specific regions. But the components are largely federally or municipally controlled.

### 2.6 Ranking — sources of truth for a §12 composite basis

Ranking the five candidates 1–3 on their suitability as the primary or primary-component data source for electoral-boundary redistribution:

**Rank 1: TBF quarterly estimates (paired with StatsCan cross-check).**

Best combination of sub-provincial granularity (CSD), frequency (quarterly), methodological transparency (full published model), and population completeness (100% by construction). Its weakness — provincial-agency control — is addressable through Option B's ±2% StatsCan tie-breaker. As the commission already uses TBF in practice, recognising it statutorily aligns law with practice. The 2025–26 commission's reliance on TBF is the empirical vindication; objection 4.2's political-vulnerability concern is answered by mandating the external StatsCan check.

**Rank 2: AHCIP registrations (as secondary / calibration source).**

Highest population-completeness of any Alberta-administered source at ~99%. Sub-zone geography (~70 LGAs) is finer than Economic Region but coarser than CSD. Structurally vulnerable to ministerial direction (Alberta Health is a ministry) but operationally insulated. Best role: calibration check on TBF's sub-provincial distribution, particularly in fast-growth municipalities where TBF's cohort projection might diverge from observed registrations. Publishing AHCIP-derived sub-provincial counts alongside TBF's composite basis would sharpen transparency without creating an independent rival source.

**Rank 3: CRA T1 taxfiler data (as independent cross-check).**

Federally administered, therefore insulated from provincial government direction. Geography (FSA, CSD) is useful for cross-checking TBF's CSD-level estimates. Coverage gap (children, non-filers) means it cannot be primary, but it is the strongest **provincially-independent** sub-provincial population signal. Role in Option B: alternative cross-check for any ED whose TBF estimate diverges from its taxfiler-implied population by more than a documented threshold.

Not ranked for primary use: Register of Electors (coverage too partial), Municipal Affairs list (not a uniform-vintage product), driver licences and enrolment (not population counts).

---

## Phase 3 — Legal and constitutional suitability

### 3.1 The constitutional minimum

Three constitutional sources bear on the question of what population data Alberta *must* use for provincial electoral-boundary redistribution:

**(a) Constitution Act, 1867, §51.** This section governs the readjustment of federal House of Commons seats "on the completion of the census." §51(1) grants Parliament the power to make provision for the readjustment from time to time. §51 does not apply to provincial electoral boundaries. It is a federal redistribution rule.

**(b) Constitution Act, 1867, §92 and the division of powers.** Provincial legislatures have exclusive jurisdiction over the "Constitution of the Province" under §92(1) (as amended by s. 45 of the Constitution Act, 1982), which includes the composition and election of the provincial Legislative Assembly. This jurisdiction permits a province to legislate the method, the data source, and the variance rules for its own electoral boundaries. There is no federal statutory or constitutional provision that compels a province to use census data for provincial redistribution.

**(c) Canadian Charter of Rights and Freedoms, §3.** The right of every Canadian citizen to "vote in an election of members of the House of Commons or of a legislative assembly" is guaranteed. In *Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, the Supreme Court held that §3 protects "effective representation" rather than strict voter parity. McLachlin J's reasons treat the output (the permissible variance in district populations) as the Charter-reviewable quantity, not the input (the data source). Nothing in the Saskatchewan Reference or its progeny addresses data source.

### 3.2 Statistics Act considerations

The Statistics Act, RSC 1985 c S-19, is a federal statute establishing Statistics Canada and mandating the decennial census. It does not require any province to use the census for provincial purposes. §19 defines the decennial census; §20 mandates the quinquennial census. The Act's force is on StatsCan's obligations, not on provincial use. A province is free to rely on other data — including StatsCan administrative data products (Table 17-10-0142, Table 11-10-0109) — that are themselves produced under the Statistics Act.

### 3.3 Provincial jurisdiction — prior practice

The comparative scan in `analysis/reports/v0_1_act_amendment_proposal.md` §2 documents that British Columbia uses BC Stats estimates (post-census), Quebec uses the electoral list, and Ontario inherits federal census data by construction. None of these choices has been constitutionally challenged on data-source grounds. The practice of provincial jurisdictions selecting their own data source is well-established.

### 3.4 Constitutional verdict

**Is census-based redistribution constitutionally required for Alberta's provincial electoral boundaries?**

**No.** The constitutional constraint operates on the output (district-population dispersion, under Saskatchewan Reference *effective representation*), not the input. The choice of data source is a matter of provincial legislative policy. Alberta's current §12(3) is a statutory policy choice, not a constitutional minimum. The legislature is free to amend §12 to name any data source — census, provincial estimate, administrative register, or a composite — provided the resulting map-level dispersion respects §3 of the Charter as interpreted in the Saskatchewan Reference.

**Constitutionally constrained elements:**
- The output must permit effective representation (a Charter §3 constraint, reviewable if challenged).
- Variance bands (currently ±25% under §14, with §15(2) exceptions) are subject to Charter review at the extremes.
- The legislature cannot delegate redistribution to a body that fails to satisfy effective representation.

**Not constitutionally constrained:**
- The specific data source (census, administrative data, survey, estimate, or composite).
- The frequency of the data update (decennial, quarterly, continuous).
- The methodology by which the data source derives its counts (census enumeration, component-cohort modelling, administrative aggregation).

The §12 amendment proposal is therefore within provincial legislative competence. Option B's composite basis would not raise a novel constitutional issue.

### 3.5 Policy choice framing

The audit's language discipline treats this as a **policy choice**, not a constitutionally-mandated posture. Use of terms:

- "Constitutionally constrained" — applies to the output dispersion and effective-representation principles.
- "Statutorily viable" — applies to any data source within the legislature's competence to name.
- "Policy choice" — applies to the legislature's decision among statutorily-viable options.

The §12 amendment is a policy choice among statutorily-viable options, subject to the constitutional constraint that the resulting map support effective representation. No data source is constitutionally required; none is constitutionally forbidden.

---

## Phase 4 — Recommendation for the reform proposal

### 4.1 Composite-basis specification for Option B §12

Based on Phases 1–3, the Option B composite basis should be specified as follows:

**Primary data source: TBF Quarterly Population Estimate (provincial and sub-provincial).**

The legislature should name TBF's quarterly estimate as the primary source of truth for total Alberta population, the provincial quota, the variance band, and per-electoral-division populations. This aligns the statute with what commissions already do, is the source with the best combination of granularity, frequency, transparency, and completeness, and is operationally implementable without new data infrastructure.

**Tie-breaker: StatsCan Quarterly Provincial Estimate (Table 17-10-0009).**

At the provincial-total level, the ±2% tie-breaker against StatsCan should be written in as a hard constraint. Where TBF and StatsCan diverge by more than 2%, the commission is required to use the arithmetic mean and state the discrepancy in its final report. This addresses objection 4.2 directly: no provincial government can manipulate the provincial total because a ±2% divergence from StatsCan triggers automatic reconciliation.

**Secondary / calibration source: AHCIP-derived sub-zone population (annual).**

The Act should require the commission to publish, alongside the composite basis, AHCIP-derived population aggregates at the AHS sub-zone level for every fiscal year corresponding to the commission's data vintage. Divergences between AHCIP-derived totals and TBF-derived totals at sub-provincial geography flag data-quality issues and cross-check TBF's cohort distribution assumptions in fast-growth areas.

**Independent cross-check: CRA T1 taxfiler data at CSD level.**

For any electoral division whose TBF population diverges by more than 5% from its taxfiler-implied population (adjusted for the known taxfiler coverage gap of ~3–5%), the commission must disclose the divergence and provide a written explanation of which basis it uses and why. This brings a federally-administered, provincially-independent check into the per-ED methodology.

**Decennial census: mandatory paired publication.**

Option B §12(6) already requires publication of the decennial-census-derived figures alongside the composite basis. This survey confirms that requirement: the 2021 Census is the authoritative baseline against which any estimate-driven basis is cross-validated, and the commission's final report must make the comparison visible.

### 4.2 Methodology-disclosure requirements

The Commission must disclose, in its final report:

1. The provincial total from TBF's quarterly estimate and the StatsCan quarterly estimate, with divergence calculation and tie-breaker application.
2. The per-electoral-division population derived from TBF, with the underlying dissemination-area aggregation documented in a machine-readable appendix.
3. The per-electoral-division AHCIP-derived population for cross-check. Material divergences flagged.
4. The per-CSD T1 taxfiler count for cross-check. Material divergences flagged.
5. The per-electoral-division decennial-census population as a paired table.
6. Any methodology change by TBF during the commission's sitting period, with the change's effect on the commission's derived quotas and variance band.

### 4.3 Oversight and certification

The reform proposal should designate an **independent certifying authority** for the population dataset delivered to the commission. Two candidates considered:

**(a) The Auditor General (Auditor General Act, RSA 2000 c A-46).** The AG is a statutorily-independent Officer of the Legislature. The AG's mandate is financial-audit-focused, but the Act permits the AG to conduct performance audits and value-for-money reviews that could cover data-methodology. This is a stretch of the AG's core competency but is within their statutory mandate. A §12 amendment could specifically require the AG to certify the population dataset.

**(b) Chief Electoral Officer (Election Act).** The CEO is a statutorily-independent Officer of the Legislature under the Election Act, and administers the Register of Electors. The CEO has no existing competency in population demography but is structurally independent. Extending the CEO's mandate to certify the commission's population dataset would require statutory amendment but sits coherently alongside the CEO's existing electoral-data responsibilities.

**(c) A new Independent Statistics Officer.** Alberta could establish a new statutorily-independent office — modelled on the Commissioner of Official Languages or the Information and Privacy Commissioner — with specific responsibility for certifying administrative-data products used in statutory contexts. This is the most robust long-term solution but requires the most legislative investment.

**Recommendation:** Designate the Chief Electoral Officer as the certifying authority in the near term, with a statutory requirement that the CEO retain external demographic expertise for the commission cycle. A longer-term Independent Statistics Officer can be proposed as a follow-up reform if the initial CEO-certification model proves insufficient. The Auditor General option is not recommended because demographic methodology is outside the AG's core expertise and would stretch the office.

### 4.4 One-page summary recommendation for Option B §12(5)

The Option B amendment text in the reform proposal should be updated (by the parent session, not this sub-agent) to reflect the following specifications:

> The composite basis under §12(2)(d) means a population figure for Alberta or for any proposed electoral division derived from the **Alberta Treasury Board and Finance quarterly provincial population estimate** (§12(2)(c)), reconciled against the **Statistics Canada quarterly provincial population estimate from Table 17-10-0009 or its successor** (§12(2)(b)).
>
> Where the two differ by no more than 2 percent at the provincial-total level, the Commission uses the TBF estimate. Where they differ by more than 2 percent, the Commission uses the arithmetic mean.
>
> The Commission's final report must publish, alongside the composite basis, (a) the per-electoral-division population derived from the decennial census; (b) the per-AHS-sub-zone population derived from AHCIP registrations for the fiscal year corresponding to the data vintage; and (c) the per-Census-Subdivision population derived from Statistics Canada's T1 Family File taxfiler tables.
>
> The Commission's population dataset must be certified by the Chief Electoral Officer of Alberta prior to the final report's publication. The Chief Electoral Officer may retain demographic expertise external to Elections Alberta for the purpose of certification.

This draft sharpens Option B §12(5) beyond the reform proposal's current text by:

1. Naming TBF and StatsCan Table 17-10-0009 as the specific statutory components of the composite basis.
2. Requiring AHCIP-derived and taxfiler-derived cross-check publications.
3. Designating the Chief Electoral Officer as the certifying authority.
4. Preserving the ±2% tie-breaker that the reform proposal already includes.

The parent session owns the reform-proposal file and should apply these recommendations at its discretion.

---

## Provenance and falsifiability

- All statutory citations are current as of 2026-04-22, consistent with the reform proposal's base date.
- AHCIP coverage estimates (~99% of census population) are derived from the reconciliation published in TBF's 2024 methodology paper (Alberta Population Projections 2024–2050, released Q4 2024 on open.alberta.ca) and the 2021 Census of Population totals from Statistics Canada Table 98-10-0001.
- T1 Family File coverage estimates (~95–98% of 18+ population) are from the StatsCan T1 Family File methodology documentation for the 2022 tax year (Table 11-10-0109 technical notes).
- Register of Electors coverage estimates (~75–80% of total population) are consistent with Elections Alberta's 2023 annual report and the National Register of Electors federal coverage reports.
- Independence assessments reflect the formal statutory structure of each custodian as of 2026-04-22. Operational independence is a separate practical judgment that could change with any new administration.
- The Phase 3 constitutional verdict (census not required) rests on the Saskatchewan Reference, [1991] 2 SCR 158, and the comparative practice of BC, Quebec, and Ontario. A reviewer who believes that a federal-provincial constitutional convention or a norm developed since 1991 creates an obligation to use the census could challenge the verdict. No such convention or norm is documented in the comparative-scan evidence base.
- The Phase 4 recommendation assumes that TBF's methodology paper will remain public and that AHCIP aggregate publications will continue to be released on open.alberta.ca. If either publication is withdrawn, the composite-basis specification's defensibility weakens and the Option B amendment's objection-4.2 answer would require strengthening (for example, by promoting CRA taxfiler data to primary-component status).
- This survey does not endorse Option B against Option A. That endorsement is the reform proposal's. This survey specifies how Option B's §12(5) should be drafted if the legislature adopts Option B.
