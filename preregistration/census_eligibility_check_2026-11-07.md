# How much of the low elector count does the 2021 census explain? (written before any comparison)

> Written 2026-11-07, after finding the census fields and testing the download, before any census figure has been placed on a division. Unregistered and not blind: the author knows the elector counts and that northeast Calgary has the lowest ratio. Requested by the author on 2026-11-07. GitHub only; no OSF filing. Nothing here is a finding on whether any map is lawful or a gerrymander.

## The question

Calgary-North East has 0.28 electors per stated person, against 0.67 provincially. Is that because of who lives there, or is something left over that points to list lag or an estimate that is too high?

## Data

2021 Census Profile, dissemination-area level, through Statistics Canada's official API (dataflow `STC_CP:DF_DA`). All are counts for all genders:

| Field | ID | Sample |
|---|---|---|
| Population, 2021 | 1 | 100% |
| Total age groups; 0 to 14 | 8; 9 | 100% |
| Total citizenship, private households | 1508 | 25% |
| Canadian citizens aged 18 and over | 1511 | 25% |
| Not Canadian citizens | 1512 | 25% |
| Immigrants; non-permanent residents; total immigrant status | 1515; 1523; 1513 | 25% |
| Total visible minority population; South Asian; Chinese; Filipino; total visible minority table | 1670; 1671; 1672; 1674; 1669 | 25% |

**Eligibility is taken as Canadian citizens aged 18 and over, private households.** Census counts are rounded and small areas can be suppressed; the share of 2021 population lost to suppression is reported first. If over 5% of population is in areas with no eligibility figure, the result is marked unreliable.

Dissemination areas go to divisions by representative point, on the majority map (official polygons and stated populations) and the panel's map (v3). Check: population by this route is compared with the audit's existing 2021 overlay.

## What is computed

For each division:
- **Eligible share** = citizens 18+ / total citizenship population, 2021.
- **Expected electors** = eligible share × stated 2024 population × one provincial scaling factor, so the expected figures sum to the 3,286,778 actual electors. This assumes residents added since 2021 resemble residents in 2021, which is the weakest assumption here.
- **Share explained** = for each division below the provincial ratio, how much of its gap from 0.672 electors per stated person the eligible share accounts for.
- **Left over** = actual electors / expected electors.

Reported: the named northeast Calgary divisions (Calgary-North East, Calgary-Bhullar-McCall, Calgary-Falconridge-Conrich), the other lowest-ratio divisions, and the size of the average miss against electors with and without the census adjustment. As the elector check found, correlation with the stated figures is confounded because maps were drawn to equalise them, so correlation is not used here.

Described beside these, without a grade: immigrant, non-permanent resident, visible minority, South Asian, Chinese and Filipino shares, for *Carter*'s "minority representation" factor.

## How the result is read

- If the left-over figure for a named division is near 1, who lives there explains its low ratio on these assumptions.
- If it is well below 1, something else is also at work, and this check cannot say which of three things: recent growth that is more heavily non-citizen than 2021, an elector list that lags, or an estimate that is too high.
- Ancestry is not eligibility. Visible minority shares are description only, and are not used to compute eligibility.
- No grade for s.15(1) changes, because the Act's test is population. The *Carter* row on minority representation may change from untested to described.

**Signed:** Claude (acting as session agent), directed by Will Conner
