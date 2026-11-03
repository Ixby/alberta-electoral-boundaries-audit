# Stage 1 (the panel's report, tabled 2026-11-02): grades without geometry

These are the Amendment 7, Part 4 deliverables for stage 1. They are due within 72 hours of 07:38 MST on 2026-11-02, so by 07:38 MST on 2026-11-05.

Sources:
- The panel's report: high-resolution PDF `evidence/legislature/iap_report_2026_hires.pdf` (SHA-256 `d8ae78ab…75122`), text layer in `evidence/legislature/iap_report_2026_hires_text/`. Pages are cited as printed pages, with PDF page = printed + 6. Minority paragraphs are cited as ¶.
- The committee's final report: `evidence/legislature/ssceb_final_report_on_iap_2026-11.pdf`.
- The Oct 28 transcript: `evidence/legislature/ceb_transcript_2026-10-28.pdf`.
- Hansard for 2026-04-21: `evidence/hansard/alberta_hansard_2026-04-21_afternoon.pdf`.

The full reading is `analysis/review/iap_report_reading_2026-11.md`.

No verdict is given on whether the map is a gerrymander.

## 1. The process lane (Lane 3 scorecard, OSF u47bq)

Cells are graded under their registered definitions. The readings in Amendment 5, Part 25 and Amendment 7, Part 5 apply:
- P6 and P7 are read against the Legislative Assembly, which the Speaker chairs.
- P5 follows its registered rule: "structurally foreclosed if P2–P4 remain No".

| # | Grade | Evidence |
|---|---|---|
| P1 Arm's-length drafting | **Partial** | The panel drafted the map. GM 37 sets its make-up as a chair (a post-secondary president or a judge or retired judge, or similar), 2 persons nominated by the Leader of the Opposition, and 2 nominated by the President of the Executive Council, none of them MLAs (committee report p. 6). The panel only advises: "It is the Legislature which does the approving or rejecting" (p. 94). The registered definition scores advisory input to a partisan decider as Partial. |
| P2 Public hearings before adoption | **No** | GM 37 C(a)(ii): "without a requirement to direct the holding of public hearings" (committee report p. 6). The minority, ¶73 (p. 132): "The ABEBC heard from hundreds of Albertans orally, and received over 1,000 written submissions. The Panel did none of that due to time constraints." The panel's own list of steps gives public hearings only at the commission stage (steps 1 and 3; panel step 9, "Advisory panel conducts its review"; p. 110). |
| P3 Draft published for challenge | **No** | The report "remains confidential until it is tabled in the Assembly" (committee report p. 11). On Oct 28 the motion to publish it before tabling was ruled "likely out of order because of Government Motion 37" (transcript CEB-66). No draft was released for comment. |
| P4 New public submissions accepted | **No** | ¶73, as above. MLA Ganley, Oct 28: "They didn't take any public submissions" (CEB-66). GM 37 C(f)(i) gave the panel access to the commission's existing submissions, not a new intake (committee report p. 8). |
| P5 Demonstrated responsiveness | **No (structurally foreclosed: P2–P4 are No)** | Reported beside the grade, not as part of it (Amendment 7, Part 5): the panel restores Rocky Mountain House-Sundre after "the Mayors of Lacombe and Blackfalds expressed displeasure" at the commission's final map (p. 41). That input was not made to the panel through a public process. |
| P6 Neutral chair of the deciding body | **No** | The map becomes law only through the Assembly's resolution and bill (pp. 109–110). The Assembly is chaired by the Speaker, "McIver, Hon. Ric, ECA, Calgary-Hays (UC), Speaker" (Hansard 2026-04-21, front matter). The advisory layer is reported beside the grade: the panel's chair, "The Honourable Brian O'Ferrall, Chair" (transmittal, PDF 3), is "a retired Justice of the Alberta Court of Appeal" (App. 5, PDF 197). |
| P7 Opposition presence in the deciding body | **Yes** | The Assembly includes the Official Opposition. |
| P8 Published reasons for contested choices | **Yes** | "Maps and detailed narratives explaining the advisory panel's proposals and the reasons for its proposal come later in this report" (p. 4). There is a narrative for each changed division (pp. 7–89) and sections on mandate, population and law (§§4–12). This cell scores publication, not accuracy. The reading's §8 lists 30 internal discrepancies. One example: the s.15(2)(e) claim for Rocky Mountain House-Sundre (p. 42) does not hold on the panel's own map (`analysis/review/iap_report_reading_2026-11.md`, §5). |
| P9 Precedent conformity | **No** | As registered, and per Amendment 5, Part 25: Alberta's 1992 committee followed a deadlocked commission whose five members filed five separate reports. It is not a precedent for 2026. The panel names no historical precedent; its "not unprecedented" (p. 5) rests on the statutory power to reject a commission's report (p. 112). |
| **Count** | **2 Yes, 1 Partial, 6 No** | |

**Against the registered prediction:** "No or Pending on P2, P3, P4, P5, P6, and P9". All six score No, so the prediction holds. The mitigation pass condition (Yes on P2 and P3, and at least one of P4/P5) is not met. Under the registered fail condition, this is reported as a count and compared with the commission process's 9 of 9, and nothing further is concluded.

## 2. The population table the stage publishes (App. 7, pp. 205–206)

Checked against the text layer (PDF 211–212) and the page images. Every population and area in the transcription (`stated_populations.csv`) appears in the text layer.

- **Total:** 4,888,723, over 91 divisions. The average is 53,722.2, matching the stated 53,722.
- **Recomputed deviations:** every row's "Difference from Average" equals population − 53,722, and every percentage agrees within rounding.
- **Range:** −46.5% (Central Peace-Notley) to +18.1% (Leduc-Beaumont). Excluding the three divisions below −25%, the range is −21.9% to +18.1%.
- **s.15(1) band, ±25%:** no division is above +25%. Three are below −25%:

  | Division | Deviation | Area |
  |---|---|---|
  | Central Peace-Notley | −46.5% | 47,312 km² |
  | Lesser Slave Lake | −44.1% | 75,775 km² |
  | Rocky Mountain House-Sundre | −41.3% | 25,122 km² |

  All three are above −50%, and three is within the s.15(2) cap of four.
- **Above +15%:** Calgary-McKenzie +16.8%, Edmonton-McClung +15.1%, Leduc-Beaumont +18.1%.
- **Mean absolute deviation (computed):** 7.84% across all 91; 6.61% excluding the three s.15(2) divisions. The panel quotes the commission's map at 4.63% and 5.72% (p. 104). Recomputed from the commission's own list, those are 4.59% and 5.79% (`reports/iap_review/`).
- **Narrative figures that disagree with the table** (the reading's §8):

  | Division | Narrative | App. 7 |
  |---|---|---|
  | Rocky Mountain House-Sundre | "approximately 30,000 … about 44%" (p. 42) | 31,540, −41.3% |
  | Morinville-Sturgeon | "47,131 or 12% below average" (p. 13) | 53,458, −0.5% |
  | Cochrane | "almost 13%" below (p. 64); "about 48,000 … about 11% below" (p. 71) | 46,785, −12.9% |

## 3. Split cities and towns, read from the published maps and names

These are counts read from the published maps, the division names and the narrative text, not geometric scores (Amendment 7, Part 4). The table is in the reading, §6. Firm counts:

| Place | Districts |
|---|---|
| Calgary | 28 Calgary-named divisions. Three reach into Rocky View County. |
| Edmonton | 21 Edmonton-named divisions. Edmonton-Nisku also spans Leduc County. |
| Lethbridge | 4 |
| Medicine Hat | 2 |
| Grande Prairie | 2 |
| Airdrie | 2 |
| Springbank | 2 |

Less certain counts:
- **Red Deer:** 3 by the text (part in Blackfalds-Innisfail, pp. 49 and 107; minority ¶37), 2 on the map insets.
- **St. Albert:** 2 by the text (p. 13). The map piece is small.
- **Fort McMurray:** likely 2.
- **Sherwood Park:** likely 2, possibly 3.
