# The panel's stated reasons, checked for consistency (2026-11-07)

**Unregistered and not blind.** Plan committed first (`preregistration/reasons_consistency_2026-11-07.md`, commit `231efd5d`). The panel's map is the v3 reconstruction, but every check here uses the panel's own words and its own published populations (Appendix 7), or 2021 census figures. Page references are PDF pages of the high-resolution report (`evidence/legislature/iap_report_2026_hires_text/pNNN.txt`). Nothing here says whether any map is a gerrymander or why a line was drawn. Districts are drawn by deliberate choice, and the question is whether a stated reason is applied the same way to comparable cases. Inconsistency is the kind of evidence that bears on intent. It is not proof of it.

**Source of the reasons.** `stated_reasons.json` holds 23 principles and 34 division entries, with verbatim quotes extracted by a reading agent and checked by script against the page text. On a second, stricter check, 11 of 257 quotes did not match exactly (encoding or line breaks). None of those 11 is used below. Every quote below was matched against its page.

## The reasons that move a seat

### 1. Lethbridge: "population to spare", not applied to Red Deer

- **What the panel says:** "Lethbridge already has population to spare" (p.80). It then adds that "if it grows any more, its population will have to be shared with electoral divisions outside of Lethbridge because it will have too much population for two electoral divisions and not enough population for three" (p.80).
- **The pairing the panel draws itself:** it names the only two Alberta cities with no division reaching past their limits: "Those two cities are Lethbridge and Red Deer and even Red Deer was once hybridized and will likely have to be hybridized again in the future" (p.81). (Corrected 2026-11-07 after the report fact-check: an earlier wording said the panel names Red Deer as "the comparable case"; it names the two together, as the only non-hybrid cities.)
- **The numbers:** on the July 2024 municipal estimates, Red Deer has 113,145 people, 2.11 times the panel's average division (53,722). Lethbridge has 111,776, or 2.08 times.
- **What the map does:** it keeps Red Deer in two urban divisions, taking only "a bit of population from Red Deer" (p.113) for Blackfalds-Innisfail. It splits Lethbridge four ways, with 22% of the city in divisions where it is a minority.
- **Reading: inconsistent.** By the panel's own description, Lethbridge would need to share population only if it grows further, and Red Deer, which is slightly larger, is not shared.

### 2. Lethbridge: the panel's own test for a hybrid

- **The test:** "whether a proposed hybrid reflects a genuine community of interest or is needed to achieve population-compliance" (p.81).
- **Population:** not needed. The commission majority's two Lethbridge divisions were already inside the band at 91 divisions, at +7.0% and +1.0%. The panel's single city division is +9.6%.
- **Community of interest:** what is left is the panel's southern argument, "better regional representation of the people of southern Alberta" (p.79). The minority's counters: "Lethbridge is a city of approximately 110,000 people. Its residents and leaders clearly want two MLAs" (p.149), and "Hybridizing Lethbridge to such a significant extent does not fit into any of the three examples of hybrid electoral divisions that we cite above" (p.149).
- **Reading:** on population, the test is not met. On community of interest, it is contested, and not testable here with public data.

### 3. Lethbridge: "mid-size cities get their own representative"

- **The principle:** the panel uses it to justify its changes elsewhere. Cochrane gets "a representative in the Legislature in the same way that similar-sized cities such as Okotoks, Airdrie and Spruce Grove will have dedicated representation" (p.70), and separating Diamond Valley "gives Okotoks its own representative" (p.96).
- **Lethbridge:** it goes the other way, from two all-Lethbridge divisions to one.
- **Reading: inconsistent.** The same principle adds dedicated seats for smaller places and removes one from a larger city.

### 4. Banff: "a minor change ... to capture the necessary population"

- **What the panel says:** "the Act does mandate that the population of ordinary electoral divisions must not be more than 25% below the average population" (p.95), so it adds the Highway 22 corridor.
- **What was needed:** the commission majority's Canmore-Banff had 39,961 people, 331 short of the −25% floor (40,292). The unanimous transfer to Rocky Mountain House-Sundre took away fewer than 1,000 more, by the minority's account. So at most about 1,300 people were needed.
- **What the panel did:** Banff-Canmore-Diamond Valley has 48,862, a net 8,901 more.
- **What the panel also argues:** a community-of-interest case, "a logically connected mountain-foothills community of interest" (p.96). The minority counters: "Not a single submission, to our knowledge, asked for Diamond Valley to be paired with Banff" (p.154).
- **Reading: inconsistent with "necessary".** The panel added about seven times the population the Act required. Its separate community-of-interest argument is contested.

## Other reasons

| Reason | The panel's words | Check | Reading |
|---|---|---|---|
| Springbank is "urban with urban" | "It mixes urban with urban residents." (p.71) | 2021 density: the Springbank parts of Calgary-Bow-Springbank and Calgary-West-Springbank hold 42 and 68 people per km², against 1,489 and 1,905 in their Calgary parts (Calgary overall 1,542). The minority: residents "have consciously chosen not to live in Calgary" (p.146) | **Not supported** by density. Commuting ties are claimed (p.74) and not tested here |
| Regular shapes | Calgary-West-Springbank "would have a much more regular polygon shape with straight line boundaries" (p.73) | Polsby-Popper 0.27 → 0.53. Calgary-North West-Bearspaw 0.25 → 0.51; Cochrane 0.36 → 0.53 | **Consistent** |
| s.15(2) is for "huge, sparsely settled areas of the Province far away from Edmonton" (p.95) | Refused for Canmore-Banff ("high-end vacation home communities", p.95); granted to Rocky Mountain House-Sundre | Rocky Mountain House-Sundre: 27,995 km², about 1.1 people per km², nearest boundary 157 km from the Legislature by road. Canmore-Banff (majority version): 15,404 km², about 2.6 per km², 313 km | **Mixed.** "Huge and sparse" fits Rocky Mountain House-Sundre; "far away from Edmonton" fits Canmore-Banff better. The Act's test is the five criteria, which both meet |
| Population parity | "Voter parity or relative voter parity is the most important consideration" (p.117); elsewhere, "minimal population variance tells you little about the merit of any particular electoral division" (p.110) | Text only | **Internal tension** in the stated principle |
| Keeping communities whole | "to keep most of Sturgeon County united" (p.14); reuniting three Treaty 6 reserves (p.13) | Lethbridge is split four ways; Springbank is split between two Calgary divisions, which the minority calls "odd" (p.147) | **Applied in some places, not others** |

## What this does and does not show

- **Where the consistent reasons fall:** where the panel's reasons are checkable and the change does not move a seat, they mostly hold. Regular shapes, the restorations and Bearspaw (which the minority calls "the most defensible change", p.147) are examples.
- **Where the inconsistent ones fall:** the two changes that do move a seat, Lethbridge and Banff, rest on reasons the panel does not apply to the comparable case (Red Deer), or that its own numbers do not support (necessary population, population compliance).
- **What that adds up to:** a pattern of evidence that matters for effective representation and for the reasonableness of the panel's choices. It is not proof of purpose. The record of how those choices were made would be.

Files: `stated_reasons.json` (all reasons and counter-quotes), `measurable_checks.py` and `.json` (M1-M3), `springbank_density.json`.
