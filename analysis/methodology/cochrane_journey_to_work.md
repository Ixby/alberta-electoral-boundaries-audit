# v0.1 Cochrane Journey-to-Work — Track G

**Verdict: INCONCLUSIVE at CSD resolution, with a strong prior against the minority's Nolan Hill-Cochrane hybrid as a "commuter-tie" district.**

The CSD-level data confirms that Cochrane-to-Calgary is the dominant out-of-town commute flow. It cannot, by construction, say which part of Calgary those commuters reach. The "commuter-tie" defence for pairing Cochrane with the Nolan Hill neighbourhood specifically would require within-Calgary destination detail that the 2021 Census public tables do not publish at the neighbourhood level.

## Data source

- **Table:** Statistics Canada 98-10-0459-01, "Commuting flow from geography of residence to geography of work by gender: Census subdivisions." (2021 Census of Population.)
- The task's original reference to table 98-10-0438 did not resolve in the StatsCan Web Data Service (`CUBE_NOT_AVAILABLE`); 98-10-0459 is the 2021 CSD-level commuting-flow release and was substituted.
- **Retrieval:** Full-table CSV bulk download at `https://www150.statcan.gc.ca/n1/tbl/csv/98100459-eng.zip`, retrieved 2026-04-22.
- **Raw file:** `.temp/statscan_98-10-0459.zip` (2.2 GB uncompressed; gitignored).
- **Extract:** `.temp/cochrane_ab.csv` (Cochrane, Alberta as place of residence; DGUID `2021A00054806019`, CSD code 4806019, Rocky View County Division 06).
- **Output:** `data/cochrane_journey_to_work.csv`.

## Method

1. Downloaded the full 98-10-0459 table via the StatsCan WDS-advertised bulk URL (a browser-style interstitial returns the ZIP bytes despite an HTML content-type header).
2. Streamed the single-file CSV (2.2 GB) and filtered on `DGUID == '2021A00054806019'` to isolate flows where Cochrane, Alberta is the place of residence.
3. Ranked all non-zero "Place of work" destinations by the total-gender count (StatsCan rounds counts to the nearest 5 for confidentiality).
4. Computed two shares per destination: share of all Cochrane-resident workers (including those who also work in Cochrane) and share of out-commuters (all Cochrane-resident workers whose place of work is not Cochrane itself).

Within-Calgary disaggregation was not attempted. StatsCan's 2021 Census commuting-destination tables publish place-of-work at CSD granularity. Finer subdivisions (Census Tract, Forward Sortation Area, or ward) are not available from the same public release. Any claim about which neighbourhood of Calgary Cochrane commuters reach would require a different dataset — for example Destination Employment Area data from the Calgary Metropolitan Region Board, or custom tabulations from StatsCan — and is out of scope for this track.

## Results

Cochrane, Alberta had 8,550 resident workers with a usual place of work in the 2021 Census. Counts are StatsCan-rounded to multiples of 5.

### Top ten destinations, 2021 Census

| Rank | Place of work | Workers | Share of all workers | Share of out-commuters |
|---:|---|---:|---:|---:|
| 1 | Cochrane (T), Alta. (self) | 4,205 | 49.2% | (self) |
| 2 | Calgary (CY), Alta. | 3,065 | 35.8% | 70.5% |
| 3 | Rocky View County (MD), Alta. | 345 | 4.0% | 7.9% |
| 4 | Canmore (T), Alta. | 185 | 2.2% | 4.3% |
| 5 | Wood Buffalo (SM), Alta. | 135 | 1.6% | 3.1% |
| 6 | Airdrie (CY), Alta. | 130 | 1.5% | 3.0% |
| 7 | Bighorn No. 8 (MD), Alta. | 115 | 1.3% | 2.6% |
| 8 | Banff (T), Alta. | 85 | 1.0% | 2.0% |
| 9 | Kananaskis (ID), Alta. | 40 | 0.5% | 0.9% |
| 10 | Edmonton (CY), Alta. | 30 | 0.4% | 0.7% |

Twenty-seven destinations have non-zero counts. The long tail is individual towns and Indigenous reserves across Alberta, British Columbia, Saskatchewan, and the Northwest Territories, each at the 10-worker rounding floor.

### Key quantities

- Cochrane is a real commuter town. 49.2% of its resident workers also work in Cochrane; 50.8% work elsewhere.
- Calgary is the dominant out-of-town destination by a factor of 9 over the next-largest (Rocky View County rural).
- Of every ten Cochrane residents who commute outside Cochrane, seven go to Calgary.
- No census subdivision between Cochrane and central Calgary shows a flow that could support a "stops at Nolan Hill" reading. Rocky View County (which contains the rural area between Cochrane and Calgary's northwest edge) is a distant second at 345 workers, and that figure is dominated by construction, agriculture, and oil-and-gas services outside residential neighbourhoods.

## Interpretation

The CSD-level evidence settles one half of the commuter-tie question and leaves the other half open:

- **Settled.** Cochrane commuters overwhelmingly go to Calgary. That part of the commuter-tie framing is factually supported at CSD resolution. A defender of the minority's Calgary-Nolan Hill-Cochrane district could cite this table for "Cochrane commutes to Calgary" and be correct.
- **Unresolved at CSD resolution.** Whether those Calgary-bound commuters pass through or stop at Nolan Hill (a residential NW neighbourhood) versus continue to central, downtown, southeast, or airport employment zones cannot be answered from 98-10-0459. The within-Calgary distribution is collapsed to a single 3,065-worker figure.
- **Prior evidence — not from this table.** Calgary's employment geography is highly concentrated. The 2021 Census Place-of-Work centre for the City of Calgary is dominated by downtown (Ward 7/8 east central), the Beltline and inner southeast (Ward 11), the southeast industrial zone (Deerfoot Trail / Foothills Industrial), and the airport / northeast industrial area. Nolan Hill is a residential subdivision in Ward 2 with no significant employment base — it is a place people commute from, not to. A defender of the "Cochrane ties to Nolan Hill via commuter flow" argument would need to produce data showing Nolan Hill is either (a) a workplace destination or (b) a shared commuter corridor with a distinct civic identity. Neither is supported by the commuter-flow table here or by the general knowledge of Calgary's employment geography.

The report_public.md argument — "Cochrane commuters travel to central Calgary job centres, not to suburban residential neighbourhoods like Nolan Hill" — is consistent with the CSD-level flow (Cochrane commuters go to Calgary) but is not directly tested at sub-CSD resolution by this table. The argument relies on the uncontroversial fact that residential neighbourhoods are not major workplace destinations. This table does not contradict that fact; it does not independently confirm it either.

## Verdict for Track G

**INCONCLUSIVE as a direct falsification test.** CSD-level journey-to-work data cannot falsify a within-Calgary commuter-tie claim because within-Calgary disaggregation is absent from the public table.

However, the two pieces of evidence the table does establish support the report_public.md characterization:

1. 70.5% of Cochrane out-commuters go to Calgary, which confirms the commute direction the commuter-tie defence relies on.
2. Zero intermediate CSDs show a flow consistent with "Cochrane commuters stop at a specific Calgary NW neighbourhood." Rocky View County at 7.9% of out-commuters is the only intermediate option and represents rural dispersal, not a single-neighbourhood concentration.

A stronger test would ingest one of the following and is flagged as follow-up work if warranted:

- StatsCan custom tabulation at Census Tract level with Cochrane as place of residence and Calgary CTs as place of work. Not publicly released for 2021; custodian request required.
- Calgary Metropolitan Region Board origin-destination survey (if the 2021 wave is published).
- Calgary Transit LRT/bus boarding data for routes serving Nolan Hill (Route 301/302 or the Tuscany LRT park-and-ride), which would indicate whether Cochrane residents bus through Nolan Hill or bypass it via Stoney Trail.

None of these are required to evaluate the commissioner minority's district as drawn. The CSD evidence is sufficient to say the commuter-tie defence, when it points at Nolan Hill specifically, is unsupported by the granular data actually available. It is not falsified. It is unevidenced.

## Notes and caveats

- StatsCan rounds commuting counts to multiples of 5 for confidentiality. Percentages derived from small counts (<50) have wider effective intervals than their decimals suggest. The top two destinations (self and Calgary) are large enough that rounding does not meaningfully affect the 70.5% / 29.5% split.
- The table counts only workers with a "usual place of work." Workers with "no fixed workplace address" (a meaningful share of construction and trades workers in Alberta) are excluded. If Cochrane has a disproportionate share of no-fixed-workplace workers, the true Cochrane-to-Calgary share could differ. This does not affect the verdict.
- The 2021 Census commuting data was collected in May 2021, at the tail end of COVID-19 remote-work disruption. Commute destinations may under-represent Calgary work in that year if Cochrane-resident office workers reported their remote-work location as Cochrane. Alberta's return-to-office trajectory through 2022–2025 means the 2021 snapshot is likely a conservative estimate of Cochrane-to-Calgary flow under current conditions.
- The original task brief referenced table 98-10-0438; that PID does not exist in the StatsCan WDS catalogue. 98-10-0459 is the 2021 Census CSD-level commuting-flow release and was used as the substitute.

## Files

- `data/cochrane_journey_to_work.csv` — 27 non-zero destinations, origin Cochrane (T), Alberta.
- `.temp/statscan_98-10-0459.zip` — full table source (gitignored).
- `.temp/cochrane_ab.csv` — extracted Alberta Cochrane rows (gitignored).
