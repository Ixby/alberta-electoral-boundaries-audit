# Two Maps, One Province

**A plain-English audit of Alberta's 2026 electoral boundary proposals**

*Published April 22, 2026 · Non-partisan, evidence-based · [Full technical report](report_academic.md) · [Repository and data](https://github.com/Ixby/alberta-electoral-boundaries-audit)*

---

## The Short Version

Alberta is redrawing its electoral map. In March 2026, an independent five-person commission tabled two competing recommendations:

- **The majority recommendation**, signed by the commission chair (a retired judge) and the two commissioners nominated by the opposition.
- **The minority recommendation**, signed by the two commissioners appointed by the governing party.

We compared both proposals against the 2019 map currently in use, applying the same tests to all three. On every measure we checked, **the two recommendations differ in ways that matter for how votes translate to seats.** The majority recommendation keeps Alberta's political playing field roughly where it sits today. The minority recommendation tilts it — modestly, but measurably, and consistently — toward the UCP.

On April 16, 2026, the provincial government rejected the majority recommendation and created a new drafting process controlled by a UCP-majority legislative committee. That process is scheduled to report back in November 2026.

This audit is not about whether the government can do that. It can. It's about whether the replacement process is being used to favor the configuration that independent analysis shows was more partisan of the two.

## What We Looked At

### 1. Are the districts roughly the same size?

Alberta's rules say each district should have a population within ±25% of the provincial average (currently 54,929), with a few exceptions for remote/rural areas.

Both 2026 proposals stay within that rule. But the majority keeps its districts tightly clustered around the average, while the minority spreads them much more widely:

| | Majority | Minority |
|---|---|---|
| Average distance from the province's average district size | 3,180 people | **4,707 people** |
| Districts more than 10% larger than average | 5 | **15** |
| Districts more than 15% larger than average | 0 | **5** |

The minority proposal has three times as many oversized districts, and five of them are within striking distance of the statutory cap. The majority has zero.

### 2. Are Calgary's districts sized fairly across the city?

Calgary has two broadly recognizable political zones: the north, east, and central areas, which lean more to the NDP, and the south and west, which lean more to the UCP. If a map gives one zone systematically larger districts, it means that zone's voters have less voice per person.

| Calgary zone | Majority proposal | Minority proposal |
|---|---|---|
| North/east/central average population | 56,460 | **61,225** |
| South/west average population | 56,255 | 54,569 |
| Gap | **0.4%** (essentially none) | **12.2%** (big) |

Under the majority proposal, Calgary's zones are balanced — same average population, no apparent zone effect. Under the minority, NDP-leaning zones carry 12% more people per district. That means fewer districts for those voters overall. A simpler rule, using only which party actually won each Calgary district in 2023, confirms the same pattern at 7.7% — different number, same direction.

### 3. Do the districts respect cities, towns, and communities?

A good electoral map tries to keep a city in as few districts as possible so the city can elect representatives focused on its own issues.

**Airdrie** is an Alberta city of 84,000 people, a size that fits comfortably in one or two districts.

- **Majority:** two districts, both named "Airdrie."
- **Minority:** four districts, *none* named Airdrie. The city is split into slices tacked onto Calgary districts, an Olds-area district, and a district named for smaller towns farther north.

**Cochrane** (pop. 34,000) gets a similar treatment:

- **Majority:** Its own district (Cochrane-Springbank).
- **Minority:** Merged into a Calgary district ("Calgary-Nolan Hill-Cochrane") via a narrow corridor reaching through Calgary's NW suburbs.

The majority proposal keeps Chestermere intact in a Chestermere-Strathmore district. The minority partially splits it between Calgary and Chestermere-Strathmore.

### 4. Do the district shapes make geographic sense?

The commission chair himself flagged three specific boundaries in the minority proposal as "engineered" — shapes drawn to meet a legal requirement rather than representing a natural community.

We examined all three on the published maps:

- **Calgary-Nolan Hill-Cochrane.** Confirmed. A long, narrow-waisted district that reaches from Cochrane across Calgary's northwest boundary to the Nolan Hill neighborhood, skipping Calgary's other NW neighborhoods in between.
- **Rocky Mountain House-Banff Park.** Confirmed. A district that extends south and west through the uninhabited portion of Banff National Park to reach the British Columbia border — without that park extension, it fails the statutory criteria that allow it to be smaller than the standard size.
- **Olds-Three Hills-Didsbury.** Confirmed. The riding takes its name from three smaller towns north of Calgary but reaches south to capture a large piece of Airdrie — a city bigger than all three named towns combined.

The majority proposal's Calgary districts — the only majority districts we had published maps for — show none of these features.

### 5. Does any of this change how votes translate to seats?

We calculated three standard measures of partisan fairness on all three maps. These compare what share of the province's votes each party would win versus what share of seats. A result near zero is neutral; a larger result in either direction indicates one party wins more seats than its votes would proportionally support.

| Measure | 2019 map | Majority 2026 | Minority 2026 |
|---|---|---|---|
| Efficiency gap | −2.64% (slight UCP edge) | −0.78% | **−1.36%** |
| Mean-median gap | −2.22 percentage points | −0.16 pp | −0.33 pp |
| NDP seats if votes tied 50/50 | 46 | 44 | **42** |

None of these numbers cross the 7% efficiency gap threshold that American courts treat as a red flag. Alberta's 2019 map already has a mild structural UCP advantage built in by geography, not boundary engineering — rural Alberta just has fewer voters spread across more area.

What matters is the **comparison between the two 2026 proposals**. Using identical methodology, the minority is about 0.6 percentage points more UCP-favorable on the efficiency gap and would give the NDP 2 fewer seats in a tied election than the majority would.

We also tested how sensitive these numbers are to the modeling choices we had to make (without official shapefiles, hybrid districts require estimating how rural and urban voters mix). The direction — minority is more UCP-favorable than majority — holds under every variant we tested. The exact magnitude ranges from about 0.6 to 1.6 percentage points depending on the modeling assumption.

### 6. What about the April 16 decision?

The government can reject or amend an independent commission's recommendations. Three recent Canadian cases are often cited:

- Quebec 1992: the legislature made narrow amendments to the commission's report.
- Ontario 1996: Queen's Park reduced seat count by adopting federal boundaries (another independent commission's work).
- BC 2008: Victoria legislated to keep more Northern seats than the commission recommended.

All three overrode a specific piece of the commission's work. None replaced the commission's drafting process with a government-controlled panel. Alberta's April 16 action — forming a UCP-majority MLA committee chaired by Brandon Lunty to oversee a new advisory panel — is in the more interventionist part of that comparison set. Whether it's without precedent depends on what survey you run; among the three cases most commonly cited, it's the most government-controlled.

The material question, in our view, is this: the commission chair himself stated in the majority report that the five specific configurations the minority proposed for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert had **no public support** in the 1,140+ submissions the commission received. If that claim is correct, the replacement process is promoting the less-publicly-supported option using a procedure designed for a different purpose.

## What This Audit Cannot Tell You

Honest limits:

- **Intent.** We can see that one map produces a more UCP-favorable result than the other, and that the more-favorable one uses configurations with no public support. We cannot tell you why the two government-appointed commissioners drew the map they did. Good-faith disagreement with the chair is one explanation; there are others.
- **The absolute magnitude of the shift.** The provincial government has not yet released official digital boundaries for either 2026 proposal. Our efficiency-gap numbers depend on some modeling of how 2023 voters distribute into proposed districts. The direction of the shift (minority more UCP-favorable than majority) is stable across every modeling assumption we tested. The size of the shift (0.6–1.6 percentage points) has a wider range.
- **Whether the override is legal.** It appears to be — the statute gives the legislature final say. Whether it's wise, fair, or well-precedented is a different question than whether it's permitted.

When Alberta's Electoral Boundaries Commission publishes the digital boundary files for both 2026 proposals — which is standard practice once a final map is adopted — we can refine all of the above from estimates to measured values. That hasn't happened yet. Nothing we've found so far requires the boundary files to confirm; they would tighten the magnitude estimates.

## Bottom Line

The minority proposal is not an extreme partisan gerrymander by US standards. It does not cross the 7% efficiency-gap threshold courts have used to flag suspect maps. Its s.15(2) uses are not all the same — two of six are flagged as engineered; four are defensible.

What it is, consistently, across six independent lines of evidence (population distribution, Calgary zone asymmetry, community splits, visible boundary shapes, partisan-fairness measures, s.15(2) engineering), is **the more UCP-favorable of two proposals the same commission produced from the same data**. The majority proposal does not share that profile.

The April 16 process favors the UCP-favorable proposal over the more-publicly-supported and more-neutral one. That combination — the substance of the maps plus the procedure being used to promote one of them — is the reason we think this audit is worth your time, whether you live in Calgary, Cochrane, Airdrie, or a district that looks settled.

---

*This audit applies identical forensic methodology symmetrically to all three maps. Full section-by-section technical writeups, reproducibility scripts, data files, and a self-audit of our own methodology are available in the [academic/legal report](report_academic.md) and in the [repository](https://github.com/Ixby/alberta-electoral-boundaries-audit).*

*We will update the public finding if and when Elections Alberta releases digital boundary files, or if the commission's 1,140+ public submissions, independently searched, refute the claim that the five disputed minority configurations had no public support.*
