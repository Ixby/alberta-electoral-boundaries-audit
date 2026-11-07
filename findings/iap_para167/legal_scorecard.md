# The panel's map against *Carter* and the Electoral Boundaries Commission Act (2026-11-07)

**Unregistered and not legal advice.** The grades were chosen after the results were known. They grade the evidence the audit holds, not the law. A court applies these tests, and nothing here says whether any map is lawful or a gerrymander. ("Gerrymander" does not appear in *Carter*.) Numbers: `legal_numbers.py`, `legal_numbers.json`.

Population figures are the panel's stated Appendix 7 and the commission's stated tables, so they do not depend on the page reconstruction. They come from the source both bodies state: the Office of Statistics and Information's July 1, 2024 dissemination-area estimates (commission PDF pp. 28-29; panel PDF pp. 107-108). Those are the primary figures here. The 2021 overlay (approximate; voting areas by representative point, v3 for the panel) and 2026 referendum electors are side references, and neither is the Act's test. See `../referendum_electors/README.md`. The Act addresses the Commission; Motion 37 clause (e) copied ss.13-15's rules into the panel's mandate, though not s.12's population rules.

**Scale.** A: clearly met, with room. B: met, weaker than at least one comparison map. C: partly met or genuinely contested. D: not met. **Not graded:** the audit has no measure, or the question is for a court.

## The Act

| Rule | Text | Panel's map | Majority | Minority | Grade |
|---|---|---|---|---|---|
| s.13 | 91 divisions (2026 amendment) | 91 | 89 (rule then) | 89 (rule then) | A |
| s.15(1) | Within ±25% of average | 88 within; highest +18.1%, lowest −21.9% (Lethbridge-Cardston); 3 rely on s.15(2). Side reference, 2021 overlay: Calgary-North East and Edmonton-Windermere would also fall below −25% | +14.3%, −21.0%. Overlay: Calgary-North East, Calgary-South East | +24.1%, −21.0%. Overlay: none | A on the stated source |
| s.15(2) cap | No more than 4 special divisions | 3 | 3 | 3 | A |
| s.15(2) floor | No more than 50% below average | Lowest −46.5% (Central Peace-Notley) | −47.7% | −45.4% | A |
| s.15(2) criteria | At least 3 of 5 in each | Central Peace-Notley 5, Rocky Mountain House-Sundre 5, Lesser Slave Lake 3 | Includes Canmore-Banff, 3 | 5, 5, 3 | A |
| s.12 | Census, with more recent data allowed "in conjunction" | Uses "Estimated Population", the same total as the commission (4,888,723; census 4,262,635) | Same | Same | C: open. Both bodies give reasons for the estimates, and no court has ruled on this use. 2026 electors track the 2021 overlay better than the estimates inside Calgary and Edmonton (0.81 against 0.18 on the majority map), which is unexplained until the 2026 census |
| s.14 lead-in | "shall" consider effective representation | Discussed across the report; its application is disputed between panel members | | | C: contested |
| s.14(a) | Sparsity, density, growth | Calgary and Edmonton average 13.4% above the rest on stated estimates (56,821 / 50,107), about 4% on the 2021 overlay, −3.8% on electors; growth not separately measured | 9.2%; overlay −0.7%; electors −7.6% | 15.9%; overlay 5.6%; electors −0.6% | B on the stated source |
| s.14(b) | Communities of interest | 24 municipal splits; Lethbridge in 4 districts where population justifies 2; reasons stated for nearly every change | 23; none over-divided | 30; 6 over-divided | C |
| s.14(c) | Geographical features | Cited in reasons; no measure | | | Not graded |
| s.14(d) | Communication and transportation | Cited (for example Highway 22); no measure | | | Not graded |
| s.14(e) | Understandable, clear boundaries | Median Polsby-Popper 0.4549 on v3; provisional, and this measure does not separate the commission maps | 0.4366 | 0.4366 | B |
| s.14(f) | Other factors | Open-ended; nothing to test against | | | Not graded |

s.14(a) to (f) are things the body "may" consider. Weak evidence on one is not a breach of it.

**Motion 37, clause (e)(ii)(B):** Recommendation 5 "subject to any modifications the independent advisory panel considers necessary". Graded by degree in `../iap_r5_degree/README.md`: restoration, (b), (c) and (d) followed; (a) partly (29 of 41 identical).

## *Carter*

*Reference re Prov. Electoral Boundaries (Sask.)*, [1991] 2 S.C.R. 158. Wording checked against `evidence/law/carter_1991_2scr158_lexum_item766.html`.

| Element | Text | Evidence on the panel's map | Grade |
|---|---|---|---|
| The right | Purpose of s.3 "is not equality of voting power per se but the right to 'effective representation'" | The framework, not a test to score | Not graded |
| Relative parity | "a prime condition of effective representation" | 67 of 91 within ±10% (73.6%). Majority 79 of 89 (88.8%), minority 60 of 89 (67.4%). Average gap from the mean 4,214 people; majority 3,179, minority 4,706. Side reference, 2021 overlay: panel 47 of 91, majority 53, minority 52 | B on the stated source |
| Dilution, urban and rural | "dilution of one citizen's vote as compared with another's should not be countenanced" beyond justified deviations | City gap +13.4% on stated figures, between the commission maps (about 4% on the overlay, also between them; −3.8% on electors, so the sign changes). *Carter* itself upheld a map with rural over-representation | B |
| Justified deviations | "practical impossibility or the provision of more effective representation" | 3 special divisions have criteria and reasons. Reasons are given for the zone (a) changes. Consistency of those reasons is untested | C |
| Community factors | "geography, community history, community interests and minority representation" | Community reasons are stated throughout, and Lethbridge's are disputed. The effect on minority representation is untested | C |
| Better government | "contribute to better government of the populace as a whole" | A judgment, not a measurement | Not graded |
| The standard | Courts should not interfere "unless it appears that reasonable persons applying the appropriate principles ... could not have set the electoral boundaries as they exist" | For a court. A deferential standard, applied to the legislature's map, which is not yet enacted | Not graded |

## Three things that affect how to read this

- **Passing the Act does not settle *Carter*, and the reverse also holds.** In *Quebec (AG) v. Lalande*, 2026 SCC 13, the dissent (Côté and Rowe JJ.) applies *Carter* and says that neither Quebec's 25% threshold nor an independent process is a constitutional requirement. That passage is the dissent's, not the Court's. The majority struck down a law interrupting a commission's process because it was not minimally impairing under s.1; the appeal concerned only s.1 justification, not whether s.3 was infringed.
- **Partisan effect is not a *Carter* element.** The audit's partisan and structural results (`README.md`, `../iap_v3_two_lane/`) are evidence for other questions. Nothing in the *Carter* passages above turns on which party benefits.
- **Grades are not additive.** A row of As on the numeric rules says the hard limits are met. It says little about the contested rows, where any real dispute lies.
