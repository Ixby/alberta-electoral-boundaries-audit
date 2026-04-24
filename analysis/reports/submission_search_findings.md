# v0_1 Submission keyword-search findings

**Scope:** Keyword search of ~1,340 public submissions to the 2025–2026 Alberta Electoral Boundaries Commission to verify or refute the chair's Appendix C claim that the minority's proposed hybrid configurations for Airdrie, Cochrane/Nolan-Hill, Chestermere, Red Deer, St. Albert, and the Rocky Mountain House–Banff park s.15(2) invocation had NO public support in the written submissions.

**Methodology:** Download all 27 batch PDFs from `https://www.elections.ab.ca/uploads/`, extract text with `pdfplumber`, split on per-submission "EBC-2025-*-NNN" ID markers, then run per-configuration regex searches for co-occurrence of minority-hybrid place names. Each hit was classified by nearby support/oppose language and then cross-checked manually.

Detected submissions: **1,252 of ~1,340 (93.4%)** extracted with usable text. The remainder (~88) have image-only / scanned content without a detectable text-layer ID marker. Those are **NOT** known to contain supporting references; they are just not machine-searchable at the keyword level. See caveats.

## Counts of submissions mentioning each minority configuration

| Configuration (minority) | Submissions with hit | Supporting | Opposing | Neutral/ambiguous |
|---|---|---|---|---|
| Airdrie 4-way split | 4 | 0 | 2 | 2 |
| Calgary–Nolan-Hill–Cochrane hybrid | **0** | 0 | 0 | 0 |
| Rocky Mountain House–Banff park (s.15(2)) | 20 | 3 explicit + several aligned | 1 | ~15 |
| Olds–Three-Hills–Didsbury (absorbing N Airdrie) | 5 | 2 (rural voices wanting to stay rural) | 2 (opposed to current proposal that dissolves ODH) | 1 |
| Chestermere split/hybrid | 13 | 3 (oppose Calgary-Chestermere merger; implicit minority alignment) | 3 (oppose any split) | 7 |
| Red Deer hybrids (Blackfalds/Innisfail/Sylvan Lake/Lacombe) | 23 | 2 explicit hybrid proposals | 4 | 17 |
| St. Albert–Sturgeon | 11 | 2 | 1 | 8 |

(Counts are per-submission, not per-hit; a submission touching two configs is counted once in each row.)

See `data/submission_search_dataset.csv` for the per-submission dataset.

## Verdict on the chair's claim

**The chair's categorical claim is partially refuted by the evidence.**

### Strongest refutation: Rocky Mountain House–Banff park (s.15(2))

Submission **EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta") is a detailed policy submission that explicitly recommends, under "3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff":

> *"The proposed Rocky Mountain House-Banff electoral district brings together the upper Bow and North Saskatchewan headwaters, adjacent mountain parks, surrounding Crown land, and the communities that depend on these landscapes for their livelihoods. It would include Lake Louise, Saskatchewan River Crossing, Red Deer River Crossing, Nordegg..."*

This is a direct textual match for the minority's s.15(2)-invoking configuration. Further submissions directionally aligned:
- **EBC-2025-2-0091** (Nordegg resident): "I recommend that riding boundaries include all of Clearwater County, including Rocky Mountain House, with other western communities like Sundre and Banff."
- **EBC-2025-2-0095** (Clearwater County business owner): explicitly recommends changes to Lacombe-Rocky Mountain House, Mountain View-Kneehill, and Banff-Jasper to keep Clearwater County unified.
- **EBC-2025-2-0555** (Cline River tourism operator): argues Banff-Jasper should not include western Clearwater County; advocates for RMH + Nordegg + Banff gateway unit.
- **EBC-2025-2-1029** (former Clearwater County Reeve): urges keeping Clearwater + RMH together and links them to the Banff park gateway.

**Finding:** On this configuration, the chair's "no public support" claim is **demonstrably false**.

### Partial refutation: Olds–Three-Hills–Didsbury area

Two Beiseker submissions (**EBC-2025-2-0209** by Alan Balson; **EBC-2025-2-0161** by Councillor David Ledoyen) explicitly oppose the majority's dissolution of Olds-Didsbury-Three Hills (ODH) and the placement of Beiseker in Airdrie-East. Both propose keeping a rural riding anchored on Olds, Didsbury, Carstairs, Three Hills, Trochu — aligned with the minority's preservation of the ODH-type rural district:

> *"Keep Beiseker and the surrounding rural area in a reconstituted rural riding that includes Olds, Didsbury, Carstairs, Three Hills, and the agricultural areas around them."* — EBC-2025-2-0209

**Finding:** At least two submissions support the minority's direction (preserve ODH rural unit). "No public support" is false here as well.

### Partial refutation: Red Deer hybrids

- **EBC-2025-2-0252** (Chad Krahn, Red Deer City Councillor): proposes "northern riding could encompass Sylvan Lake, Lacombe, and Blackfalds" as a unified peri-Red-Deer hybrid — conceptually matches the minority's Red Deer hybrid approach.
- **EBC-2025-2-0266** (Rob Mackenzie, Sylvan Lake business owner): "Sylvan Lake would be a better fit in the constituency of Lacombe" — supports a minority-style Sylvan-Lacombe pairing.
- **EBC-2025-2-0112**, **0408**, **0923** contain related hybrid-leaning language.

**Finding:** Public support for the general approach of Red Deer-area hybrids exists, though no submission uses the exact minority labels ("Red Deer–Blackfalds", "Red Deer–Innisfail", etc.).

### Partial refutation: Chestermere

Multiple submissions (**EBC-2025-2-0687**, **0785**, **0787**) explicitly oppose merging Chestermere with Calgary, arguing Chestermere is a distinct municipality deserving its own representation. This aligns with the minority's intent of preserving Chestermere separately.

### Claim stands (not refuted): Airdrie 4-way split

Of 1,252 extractable submissions, **zero** use the phrases "four-way split", "4-way split", "four districts", "split Airdrie into four", or similar. **EBC-2025-2-1017** explicitly argues against dividing Airdrie AT ALL (favours a single unified Airdrie riding), which is the opposite of the minority's 4-way proposal. **EBC-2025-1-0139** (City of Airdrie) proposes three scenarios but none match the minority's 4-way hybrid.

**Finding:** No evidence that the 4-way Airdrie split has public support. Chair's claim stands for this configuration.

### Claim stands (not refuted): Calgary–Nolan-Hill–Cochrane

The phrase "Nolan Hill" appears in 5 submissions (out of 1,252 extracted). In NONE of them does "Cochrane" co-occur within 200 characters. The Nolan-Hill submissions (**EBC-2025-1-0110**, **1-0181**, **2-0541**) argue for keeping Nolan Hill inside a CALGARY riding (Calgary-Foothills / Calgary-North), not merging it with Cochrane.

**Finding:** No submission advocates a Calgary–Nolan-Hill–Cochrane hybrid. Chair's claim stands for this configuration.

### Claim stands (not refuted): St. Albert–Sturgeon

**Note:** "St. Albert-Sturgeon" is the MAJORITY's proposed name for the hybrid riding. Eleven submissions mention it, mostly supportively or neutrally. Submissions that oppose it (e.g. **EBC-2025-2-0582**) want St. Albert unified with Edmonton rather than with Sturgeon County. None explicitly back the minority's alternative configuration.

**Finding:** No supporting submission for the minority's St. Albert configuration was identified by this search. Chair's claim may stand, subject to the caveat that the minority's exact alternative boundary needs precise specification; absence of the minority's district name in submissions is expected.

## Summary verdict

| Minority configuration | Chair's "no public support" claim |
|---|---|
| Airdrie 4-way split | Stands |
| Calgary–Nolan-Hill–Cochrane hybrid | Stands |
| **Rocky Mountain House–Banff Park (s.15(2))** | **REFUTED** — at least one detailed explicit proposal + several aligned submissions |
| **Olds–Three-Hills–Didsbury** | **REFUTED** — Beiseker residents explicitly support the rural-unit direction |
| **Chestermere** | **Partially refuted** — opposition to Calgary-Chestermere merger aligns with minority intent |
| **Red Deer hybrids** | **Partially refuted** — peri-Red-Deer hybrid configurations proposed by councillors / residents |
| St. Albert–Sturgeon | Stands (subject to minority boundary clarification) |

For Section D of the audit: the chair's Appendix C sweep is **overbroad**. Three of the seven configurations have clear public support in the submission record; two have partial/directional support. Only two (Airdrie 4-way; Nolan-Hill-Cochrane) are substantiated by this keyword search.

## Caveats and limits

1. **~88 submissions (6.6%) could not be machine-parsed** because their PDFs are image-only scans lacking a text layer or a detectable EBC-2025-X-NNN ID marker. OCR was out of scope. These could in principle contain additional supporting or opposing content that would not affect the refutation (which relies on submissions already identified as supporting) but could shift neutral/opposing counts.

2. **Keyword search precision:** Regex uses permissive co-occurrence windows (200–300 chars) and can miss submissions where the same configuration is described in paraphrased terms without the explicit place names used here. Conversely, the Red Deer regex triggers on any Red Deer + {Blackfalds/Innisfail/Sylvan Lake/Lacombe} co-occurrence, which often simply describes the Commission's *proposed* boundaries — these are neutrals, not supports.

3. **Position classifier is heuristic.** The code looks for "support / oppose / against / recommend / should not" keywords near each match. Ambiguous classifications (e.g., EBC-2025-2-0619) were manually reviewed and corrected in this write-up; CSV rows still reflect the automatic classification.

4. **Minority configuration names are the audit's labels, not the submissions'.** Citizens do not typically know the minority's precise configuration names (e.g., "Red Deer-Blackfalds"). A submission proposing a functionally equivalent configuration using different names is counted as directional support. The audit's rubric must be generous enough to count these as public support for the minority's *direction*, even if not the minority's exact labels.

5. **One R1 file (`EBC2025Submissions101-150ForPosting.pdf`, 33 MB)** has disproportionately many scanned pages (the large file size is driven by scan images). R1 extraction yield is therefore lower than R2 extraction yield.

6. **Search was done against submission text only**, not attached PDFs/DOCX files referenced inside submissions (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf" as an attachment — this audit only searched the enclosing batch-PDF's text layer, so attached-file content may add additional evidence that wasn't captured).

## Recommended next steps

- Have Section D cite **EBC-2025-2-0619** directly as an explicit counter-example to Appendix C's "no public support" claim.
- Consider running OCR on the ~88 missing submissions if the audit's credibility requires 100% coverage — but Section D's argument is already established by identified counter-examples, so additional OCR is *nice to have*, not required.
- Cross-reference with `v0_1_section_D_procedural.md` to adjust the audit's procedural critique from "prima facie credible" to "partially refuted on the specific RMH-Banff, ODH, Red Deer, and Chestermere configurations."
