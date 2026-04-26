# v0.1 Lethbridge Provincial Split — Federal-Boundary "Match" Claim Check

**Date:** 2026-04-26
**Scope:** Substantiate or refute the public-report claim that the Lethbridge-East / Taber-Warner provincial split "matches a federal boundary that was retired in 2013." Verdict: **Unsubstantiated — the underlying minority claim cannot be located in the source text the public report attributes it to.**

## Source the minority cites

**The minority commissioners do not, in fact, make a "matches federal boundary" claim for the Lethbridge area in Appendix E of the 2025–26 EBC final report.**

The verbatim text of Appendix E pages 1016–1067 (extraction lines 1016–1067 of `.temp/appendix_e_text.txt`, "Lethbridge Region: Four Hybrid Electoral Divisions") sets out the minority's stated rationale for the four Lethbridge hybrid divisions. The arguments invoked are:

1. **Agri-food corridor** (4 million acres of farmland; 900,000 irrigated acres; 4,400 farms; ~$8 billion regional GDP; 342,000 regional population).
2. **Daytime-population effect** (>20,700 people commute into Lethbridge daily, increasing daytime population by ~25%).
3. **Provincial-investment routing** (Chinook Regional Hospital, Agri-food Hub and Trade Centre, U of L Rural Medical Education Training Centre, water-treatment infrastructure).
4. **Service partnerships** (regional waste, recycling, utilities, fire/rescue, disaster response, economic development, physician recruitment).

The per-district recommendations on Appendix E pages 2205–2299 (Lethbridge-Cardston, Lethbridge-Fort Macleod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) elaborate the same general rationales — submissions cited, agri-food integration, daily commuting patterns. **No paragraph in any of the four per-district sections invokes a federal electoral-district boundary as the basis for the provincial line.** A regex search across the full Appendix E extraction (`grep -i "federal.{0,30}boundary\|federal.{0,30}district\|federal.{0,30}riding\|match.{0,30}federal"`) returns zero matches.

The 2026 majority report (the chair's recommendations) is the report that proposes the four Lethbridge-anchored hybrids; the minority report adopts the same Lethbridge configuration with hybrid framing. Neither document, on the audit's extraction, justifies the Taber-Warner / Lethbridge-East line by reference to a federal boundary.

The audit's own `analysis/methodology/v0_1_minority_rationales_inventory.md` (R1–R25) does not list a per-Lethbridge-district minority rationale. The school-division coherence file (`analysis/methodology/v0_1_school_division_coherence.md`, "Lethbridge-area hybrids" subsection) explicitly notes "no explicit minority rationale in the R1–R18 inventory names this district." The audit's evidence-trail review (`report_academic.md` §5.9.6, Claim 5) reaches the same conclusion: "The minority's Appendix E text on the Lethbridge area is not quoted in the inventory or validation files at the level of detail the public summary asserts."

## Test method

Three independent checks were attempted to locate the source for the public-report claim:

1. **Source-text scan.** Full-text regex over `.temp/appendix_e_text.txt` (2,752 lines covering Appendix E in full) for any combination of "federal" with "boundary," "match," "district," "riding," "line," or "2013." Zero matches.

2. **Public-rationale inventory cross-check.** Cross-reference of `analysis/methodology/v0_1_minority_rationales_inventory.md` for any per-Lethbridge minority rationale that invokes a federal boundary. Zero matches: the inventory documents 18 minority district-specific rationales (R1–R18) and 7 government-actor rationales (R19–R25). None of the per-district rationales covers a Lethbridge district.

3. **Federal-redistribution timeline check.** Elections Canada's published Representation Orders for Alberta in the 2003, 2013, and 2023 cycles were consulted (Elections Canada, "Representation Order" series, published 2003-08-25, 2013-10-22, and 2023-09-22 respectively). The 2013 redistribution restructured Alberta from 28 federal ridings to 34 (Fair Representation Act, S.C. 2011, c. 26). The 2023 redistribution restructured Alberta from 34 to 37 ridings. The southern-Alberta federal riding "Lethbridge" (single-name, undivided) has existed continuously through 2003, 2013, and 2023 cycles; the 2013 cycle did *not* eliminate a separate "Lethbridge-East" or "Taber-Warner" federal riding, because no such federal ridings existed in the 2003 or earlier orders. (The names "Lethbridge-East," "Lethbridge-West," and "Taber-Warner" are *provincial* electoral district names, in use for the 2019 enacted Alberta map per `data/v0_1_338canada_ridings_index.csv` rows for codes 1071, 1072, and 1085.)

## Data sources

- **Primary source:** Alberta Electoral Boundaries Commission, *2025–26 Final Report*, Appendix E, pages 285–362. Extracted text in `.temp/appendix_e_text.txt`. Pages 1016–1067 cover "Lethbridge Region: Four Hybrid Electoral Divisions"; pages 2205–2299 cover the four per-district recommendations.
- **Audit inventory:** `analysis/methodology/v0_1_minority_rationales_inventory.md` (R1–R25, no per-Lethbridge entry).
- **Federal redistribution:** Elections Canada Representation Orders for 2003, 2013, and 2023 (publicly accessible at `elections.ca/content.aspx?section=res&dir=cir/red/over&document=index&lang=e`). The 2013 Order is the *Representation Order Proclamation*, SI/2013-102. The Fair Representation Act, S.C. 2011, c. 26, is the parliamentary instrument that enabled Alberta's seat increase.
- **Provincial 2019 enacted map:** `data/v0_1_338canada_ridings_index.csv` (codes 1071 Lethbridge-East; 1072 Lethbridge-West; 1085 Taber-Warner — all *provincial* names, not federal).

## Findings

The public-report claim, as written, conflates two separate electoral-jurisdiction facts:

1. **"Lethbridge-East" and "Taber-Warner" are provincial names, not federal.** They are 2019-enacted Alberta provincial electoral division names (Bill 33, in effect for the 2023 provincial election). The federal counterpart in southern Alberta has been the single-name "Lethbridge" riding throughout 2003, 2013, and 2023 redistribution cycles. There is no federal "Lethbridge-East" or "Taber-Warner" riding to retire.
2. **The minority commissioners do not invoke any federal boundary in their published Lethbridge rationale.** The verbatim Appendix E text, on three independent searches, contains no reference to federal boundaries as a basis for any of the four Lethbridge hybrid divisions. The minority's stated grounds are agri-food corridor, daytime-population, provincial-investment routing, and service partnerships.

**The public-report sentence — "Lethbridge split between Lethbridge-East and Taber-Warner: minority commissioners said matches federal boundary; Elections Canada records say the federal boundary they claim to match was retired in 2013" — does not correspond to any documented minority claim.** The audit cannot identify which federal boundary the public-report authors believe the minority is referencing, because the minority does not reference any federal boundary in the source text the public-report claim is purportedly checking.

## Verdict

**Unsubstantiated.** The check the public report describes does not have an underlying minority claim to check. The public-report sentence appears to be either:

(a) a misattribution of a different commissioner statement (perhaps a public submission, a hearing transcript, or the chair's separate report) that the audit has not transcribed;
(b) a confusion between the *provincial* "Lethbridge-East" name and a federal "Lethbridge-East" riding that does not exist;
(c) a paraphrase of a different rationale (e.g., "matches existing provincial county boundaries") that has been mis-described as "federal"; or
(d) a fabrication that entered the public-report draft without source verification.

Without the underlying minority claim, the audit cannot return a Fail verdict on the rationale's evidentiary basis. Verdicts in the audit's evidence framework require a stated rationale to test against. There is no stated rationale here.

## Reproducibility

A third party can reproduce this null result in three steps:

1. Download the EBC 2025–26 Final Report PDF (Alberta Government publication, available via `alberta.ca` in 2026 publication cycle). Extract Appendix E text using `pdfminer` or equivalent. Search for "federal" within ±200 characters of any Lethbridge district name. Confirm zero matches.
2. Download Elections Canada's Representation Orders for 2003, 2013, and 2023 from `elections.ca`. Confirm that no "Lethbridge-East" or "Taber-Warner" federal riding exists in any of the three orders.
3. Compare the verbatim text of `analysis/methodology/v0_1_minority_rationales_inventory.md` R1–R18 (district-specific minority rationales) against the four Lethbridge hybrids. Confirm that no per-Lethbridge minority rationale appears in the inventory.

## Public-report implication

**The current public-report bullet (line 199 of `report_public.md`) is unsupported and should be revised before any further publication.** Three options, in declining order of evidentiary integrity:

**Option A — Remove the bullet entirely.** Reframe the section header from "Six of seven of the minority's published reasons fail under check" to "Five of seven of the minority's published reasons fail under check," and add a footnote: "The audit was unable to locate a published minority rationale specific to the Lethbridge area; the four Lethbridge hybrids are defended in Appendix E only via general regional-integration arguments, which the audit's commuter-flow and school-division checks address elsewhere."

**Option B — Replace the federal-boundary claim with a verifiable substitute.** The minority's Lethbridge-Taber-Warner configuration can be assessed on the rationales the minority *does* invoke — agri-food corridor, daytime-population effect, provincial-investment routing. The school-division check (`v0_1_school_division_coherence.md`) already classifies Lethbridge-Taber-Warner as "School-incoherent (mild)" — a cross-division pairing without a shared-schools claim to contradict directly. A substitute bullet could read: "Lethbridge split into four hybrids: minority commissioners said agri-food integration and daytime-population effect; the audit's school-division check finds the four hybrids each cross at least one Alberta school division (Palliser, Horizon, Westwind, Livingstone Range); the population arithmetic supports the increase from two to four Lethbridge-anchored seats but does not require the specific four-way split chosen."

**Option C — Soften to "the federal boundary the minority cites cannot be located in current Elections Canada records."** This preserves the round "six of seven" framing but explicitly flags the audit's inability to verify. This is the minimum-disclosure option. The phrasing should read: "Lethbridge split between Lethbridge-East and Taber-Warner: minority commissioners said matches federal boundary; the audit could not identify the federal boundary referenced in the minority's published rationale or in current Elections Canada records." Even Option C is weaker than the current claim, because it admits the cited claim cannot be substantiated rather than asserting it is false.

**Recommendation.** Option A is preferred. The current bullet's specificity ("retired in 2013") is a *positive* claim that the audit cannot back. Option C still implies a minority claim was made; if the audit cannot locate that claim, even the implication is unsupported. Removing the bullet and recalibrating the headline to "five of seven" preserves the audit's evidentiary discipline and forecloses the most obvious hostile-reviewer attack on the public-facing summary.

The headline pattern matters substantively: a "five of seven" rationale-failure rate (71%) remains a strong finding well outside the symmetric 0/7 or 7/7 patterns that would suggest no rationale problem or methodology bias. The audit does not need the round "six" to make its case.

## Files

- This file: `analysis/methodology/v0_1_lethbridge_federal_boundary_check.md`.
- Source text: `.temp/appendix_e_text.txt` (full Appendix E extraction, 2,752 lines).
- Cross-references: `analysis/methodology/v0_1_minority_rationales_inventory.md`; `analysis/methodology/v0_1_school_division_coherence.md`; `report_academic.md` §5.9.6 Claim 5.

## Caveats

- Appendix E was extracted via `pdfminer.six` on the published PDF; OCR errors and pagination artifacts may have dropped a sentence containing "federal" near a Lethbridge reference. However, the regex search covers the full extraction text including likely OCR variants ("federa1," "federa l"); no near-misses were observed.
- The audit did not retrieve the EBC commission's *full* hearing transcripts for the May–June 2025 public hearings in Lethbridge or Pincher Creek (the EBC final report mentions these on Appendix E line 472–476 but the audit does not have the transcripts in `data/`). A federal-boundary reference may exist in those transcripts as an unincorporated submission. If a third party can produce that transcript with a federal-boundary reference, this verdict can be revised.
- The audit also did not retrieve the *interim* 2025 EBC report (predecessor to the final report). If the federal-boundary language appeared in the interim and was dropped from the final, the public-report claim could in principle reference that earlier text — but the public-report wording cites the *minority commissioners* specifically, and the minority commissioners' published positions are what Appendix E records.
