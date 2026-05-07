# SZAT Pre-Registration Draft — AsPredicted Submission

**Purpose.** This document contains the verbatim text to be filed at
aspredicted.org for the Swing-Zone Allocation Test bootstrap null. File
this before citing any SZAT results in the reports.

**Methodological note on timing.** The SZAT bootstrap seed was derived
from the pre-committed drand beacon (CANONICAL_ROUND = 5500000, committed
at git hash `d2aea42` before any simulation results were generated). The
`szat.py` script was written and a preliminary run was executed on
2026-05-06 before this registration was filed. This diverges from the
ideal pre-analysis registration sequence. It is disclosed here and in the
report: the analysis plan and seed were pre-committed, but the registration
text was filed after a preliminary run confirmed the pipeline worked.
The specific numerical results were known to the analyst at time of filing.

---

## AsPredicted submission text

### 1. Have any data been collected for this study already?

Yes. We use the 2023 Alberta general election results by Voting Area (VA),
obtained from Elections Alberta, and the official 2026 Electoral Boundary
Commission proposed boundary shapefiles (majority and minority reports),
released 2026-04-09 and obtained directly from Elections Alberta. All data
were already in our possession before the SZAT analysis pipeline was
designed.

### 2. What is the main question being asked or hypothesis being tested?

Do the specific boundary choices that differ between the 2026 EBC majority
and minority proposed maps — the "swing zones," defined as Voting Areas
whose centroid falls in a different Electoral Division under the minority
map than under the majority map — systematically shift partisan vote
efficiency in a directional way?

**Null hypothesis (H0):** The minority map's swing-zone boundary choices
produce no systematic difference in efficiency-gap contribution compared to
the majority map. Formally: the observed SZAT score (minority EG − majority
EG, computed over swing-zone VA reallocation) does not exceed the 95th
percentile of the randomization null distribution.

**Alternative hypothesis (H1):** The swing-zone allocations under the
minority map are directionally non-neutral — they produce a larger
efficiency-gap asymmetry than would be expected if the boundary choices
were randomly assigned across swing-zone VAs.

### 3. Describe the key dependent variable(s)

**SZAT score** = EG(minority map) − EG(majority map), where EG is the
standard Stephanopoulos-McGhee (2015, *U. Chi. L. Rev.* 82(2): 831–900)
efficiency gap computed from 2023 election-day Voting Area vote totals
spatially joined to each proposed map.

EG sign convention: positive = more NDP votes wasted than UCP (structural
UCP advantage). SZAT score positive = minority map's boundary choices
increase NDP vote waste relative to the majority map.

Secondary outputs:
- Regional decomposition of SZAT score (Calgary, Edmonton, Mountain-West,
  Rest of Alberta)
- Canmore/RMH focal-ED contribution (the specific Banff-area boundary
  choices that motivated this test; see `analysis/methodology/s15_2_reaudit.md`)

### 4. How many observations will be collected?

4,765 Voting Areas assigned via centroid-in-polygon spatial join to each
proposed map. Of these, swing zones (VAs assigned to different EDs under
the two maps) number approximately 2,100 (exact count from the spatial
join). The bootstrap uses 10,000 permutations.

### 5. What are the analyses?

**Primary test — randomization bootstrap:**

For each of 10,000 permutations:
1. For each swing-zone VA, randomly assign it to either its majority-map
   ED or its minority-map ED (independent Bernoulli(0.5) draws)
2. Compute EG for each map under the randomized assignment
3. Record SZAT score under the permutation

Bootstrap seed: `get_canonical_seed("szat-bootstrap")` derived from
Cloudflare drand League of Entropy beacon round 5,500,000
(randomness `45922177bf69644aa0b8f8043695221eacad1147dfde0967c72fbf3756ffacac`),
committed at git hash `d2aea42` before any simulation results were computed.
Derivation: SHA-256(CANONICAL_RANDOMNESS + "szat-bootstrap"), first 4 bytes
as uint32 mod 2^32 = 23687475.

**Verdict criterion:** Reject H0 if |SZAT_score| > 95th percentile of the
bootstrap null distribution (two-tailed α = 0.05).

**Boundary shapefiles (canonical):** Elections Alberta official shapefiles
`EBC2025_Boundaries_Apr092026.shp` (majority) and
`Minority_Report_Boundaries.shp` (minority), both EPSG:3400, 89 EDs each,
stored at `data/shapefiles/canonical/` in the audit repository.

All code in `analysis/scripts/szat.py` (committed in the same git push as
this pre-registration record).

### 6. Any other comments?

This test was motivated by the §15(2) population-deviation re-audit
(`analysis/methodology/s15_2_reaudit.md`, 2026-04-23), which found that the
minority map's Rocky Mountain House-Banff Park ED is 5.3 percentage points
outside the normal ±25% population band and invokes the §15(2) exception —
the smallest margin of any §15(2) invocation in either map. The question
arose whether the specific partition between Canmore-Kananaskis and
Rocky Mountain House-Banff Park under the minority map serves a partisan
efficiency purpose. SZAT answers this for those EDs specifically and for
all 2,100+ swing zones jointly.

**Relationship to existing pre-registrations:**
- AsPredicted #289449: DPG v11 validation (complete)
- AsPredicted #289451: Neighbour-Drain label-shuffle null (pending)
- AsPredicted #289455: Lunty 91-seat forensic scorecard (pending)
- This registration: SZAT bootstrap null (new)

Cross-ref: `analysis/methodology/szat_proposal.md`,
`dpg_validation/dpg2_worklog.md` §Pre-registration table.

---

## After filing

1. Record the AsPredicted number in `dpg_validation/dpg2_worklog.md`
   §Pre-registration table (new row: SZAT bootstrap null / #XXXXXX / [OSF] /
   Registered 2026-05-06 / results known at registration)
2. Update `analysis/methodology/szat_proposal.md` §8 checklist — check off
   pre-registration item and add the AsPredicted number
3. Add disclosure to `report_academic.md` §3 SZAT section: "Pre-registered
   at AsPredicted #XXXXXX; note results were known to analyst at time of
   filing — seed was pre-committed at git hash d2aea42."
