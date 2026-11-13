> **Backward:**
> - `analysis/scripts/submission_search.py` — companion keyword-search pipeline (pdfplumber + regex)
> - 27 batch PDFs from elections.ab.ca (raw submissions)
> - `data/submission_search_dataset.csv` — per-submission dataset produced by the search
>
> **Forward:**
> - `findings/claim_significance_analysis.md` — quantifies the engagement/net/absolute support framework on top of these counts
> - `reports/academic/report_academic.md` — incorporates the keyword-search findings
> - `reports/public/report_public.md` — references the check of the majority's "no public support" statement
> - `findings/README.md` — indexes this finding

# v0_1 Submission keyword-search findings

**Status.** The support/oppose/neutral labels in this search are unreliable. Read in full, none of the submissions it named as supporters at Chestermere or Red Deer supports the minority's arrangement. In a random sample of the later classifier pass over the same submissions, 26 of 31 stance labels were wrong (`findings/audit_2026-11-10/submissions_sample48_judgements.csv`). The stance columns that stood in the table below are withdrawn, and the classification is being redone in `findings/submissions_recode/`. The verdicts below rest on reading the named submissions directly.

**Scope:** Keyword search of the public submissions to the 2025–2026 Alberta Electoral Boundaries Commission (1,345 received: 198 before the interim report and 1,147 after) to check the majority's statement that the minority's changes in five places (Airdrie, Cochrane, Chestermere, Red Deer and St. Albert) had "no public support" (final report, pp. 59 and 62). Two other minority configurations, Rocky Mountain House–Banff Park and Olds–Three Hills–Didsbury, were searched as well; they are not among the five.

**Methodology:** Download all 27 batch PDFs from `https://www.elections.ab.ca/uploads/`, extract text with `pdfplumber`, split on per-submission "EBC-2025-*-NNN" ID markers, then run per-configuration regex searches for co-occurrence of minority-hybrid place names. Each hit was first classified by nearby support/oppose language; that classification is the part now withdrawn.

Detected submissions: **1,252 of the 1,345 (93.1%)** extracted with usable text. Of the other 93, 88 are in the posted files but could not be split out by id, most of them image-only scans without a detectable text-layer ID marker, and 5 are not in the posted files (the batches run to ids 197 and 1,143; `findings/submission_search_log.md`). Those are **NOT** known to contain supporting references; they are just not machine-searchable at the keyword level. See caveats.

## Counts of submissions mentioning each minority configuration

| Configuration (minority) | Submissions with hit |
|---|---|
| Airdrie 4-way split | 4 |
| Calgary–Nolan-Hill–Cochrane hybrid | **0** |
| Rocky Mountain House–Banff park (s.15(2)) | 20 |
| Olds–Three-Hills–Didsbury (absorbing N Airdrie) | 5 |
| Chestermere split/hybrid | 13 |
| Red Deer hybrids (Blackfalds/Innisfail/Sylvan Lake/Lacombe) | 23 |
| St. Albert–Sturgeon | 11 |

The supporting, opposing and neutral columns are withdrawn pending the recode.

(Counts are per-submission, not per-hit; a submission touching two configs is counted once in each row.)

See `data/submission_search_dataset.csv` for the per-submission dataset. Its stance column carries the unreliable labels.

## Verdict on the majority's statement

**The majority's statement is right in four of the five places it names and partly wrong on Chestermere.**

### Documented support, outside the five places: Rocky Mountain House–Banff park (s.15(2))

Submission **EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta") is a detailed policy submission that explicitly recommends, under "3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff":

> *"The proposed Rocky Mountain House-Banff electoral district brings together the upper Bow and North Saskatchewan headwaters, adjacent mountain parks, surrounding Crown land, and the communities that depend on these landscapes for their livelihoods. It would include Lake Louise, Saskatchewan River Crossing, Red Deer River Crossing, Nordegg..."*

This is a direct textual match for the minority's s.15(2)-invoking configuration. Further submissions directionally aligned:
- **EBC-2025-2-0091** (Nordegg resident): "I recommend that riding boundaries include all of Clearwater County, including Rocky Mountain House, with other western communities like Sundre and Banff."
- **EBC-2025-2-0095** (Clearwater County business owner): explicitly recommends changes to Lacombe-Rocky Mountain House, Mountain View-Kneehill, and Banff-Jasper to keep Clearwater County unified.
- **EBC-2025-2-0555** (Cline River tourism operator): argues Banff-Jasper should not include western Clearwater County; advocates for RMH + Nordegg + Banff gateway unit.
- **EBC-2025-2-1029** (former Clearwater County Reeve): urges keeping Clearwater + RMH together and links them to the Banff park gateway.

**Finding:** This configuration has documented public support. It is not one of the five places the majority's statement names.

### Documented support, outside the five places: Olds–Three-Hills–Didsbury area

Two Beiseker submissions (**EBC-2025-2-0209** by Alan Balson; **EBC-2025-2-0161** by Councillor David Ledoyen) explicitly oppose the majority's dissolution of Olds-Didsbury-Three Hills (ODH) and the placement of Beiseker in Airdrie-East. Both propose keeping a rural riding anchored on Olds, Didsbury, Carstairs, Three Hills, Trochu — aligned with the minority's preservation of the ODH-type rural district:

> *"Keep Beiseker and the surrounding rural area in a reconstituted rural riding that includes Olds, Didsbury, Carstairs, Three Hills, and the agricultural areas around them."* — EBC-2025-2-0209

**Finding:** At least two submissions support the minority's direction (preserve ODH rural unit). This configuration is not one of the five places the majority's statement names.

### Statement holds: Red Deer hybrids

The minority's Red Deer arrangement is four hybrids, each taking a slice of the city (final report PDF pp. 350–351). No submission supporting that arrangement was found. The submissions the keyword pass had listed as supportive (**EBC-2025-2-0252**, **0266**, **0112**, **0408**, **0923**) do not support it when read in full.

**Finding:** No supporter was found. The majority's statement holds for Red Deer.

### Partly wrong: Chestermere

The minority puts southern Chestermere into Calgary-Peigan-Chestermere (final report PDF p. 332).

- **For (3):** **EBC-2025-2-0384**, **0811** and **1091** support the minority's arrangement.
- **Against (3):** **EBC-2025-2-0687**, **0785** and **0787** oppose it.

**Finding:** Three submissions support the minority's arrangement and three oppose it. The majority's statement is partly wrong there.

### Claim stands (not refuted): Airdrie 4-way split

Of 1,252 extractable submissions, **zero** use the phrases "four-way split", "4-way split", "four districts", "split Airdrie into four", or similar. **EBC-2025-2-1017** explicitly argues against dividing Airdrie AT ALL (favours a single unified Airdrie riding), which is the opposite of the minority's 4-way proposal. **EBC-2025-1-0139** (City of Airdrie) proposes three scenarios but none match the minority's 4-way hybrid.

**Finding:** No evidence that the 4-way Airdrie split has public support. The majority's statement stands for this configuration.

### Claim stands (not refuted): Calgary–Nolan-Hill–Cochrane

The phrase "Nolan Hill" appears in 5 submissions (out of 1,252 extracted). In NONE of them does "Cochrane" co-occur within 200 characters. The Nolan-Hill submissions (**EBC-2025-1-0110**, **1-0181**, **2-0541**) argue for keeping Nolan Hill inside a CALGARY riding (Calgary-Foothills / Calgary-North), not merging it with Cochrane.

**Finding:** No submission advocates a Calgary–Nolan-Hill–Cochrane hybrid. The majority's statement stands for this configuration.

### Claim stands (not refuted): St. Albert–Sturgeon

**Note:** "St. Albert-Sturgeon" is the MAJORITY's proposed name for the hybrid riding. Eleven submissions mention it. Submissions that oppose it (e.g. **EBC-2025-2-0582**) want St. Albert unified with Edmonton rather than with Sturgeon County. None explicitly back the minority's alternative configuration.

**Finding:** No supporting submission for the minority's St. Albert configuration was identified by this search. The majority's statement stands, subject to the caveat that the minority's exact alternative boundary needs precise specification; absence of the minority's district name in submissions is expected.

## Summary verdict

| Minority configuration | Majority's "no public support" statement |
|---|---|
| Airdrie 4-way split | Holds |
| Calgary–Nolan-Hill–Cochrane hybrid | Holds |
| Red Deer hybrids | Holds — no supporter found |
| St. Albert–Sturgeon | Holds (subject to minority boundary clarification) |
| **Chestermere** | **Partly wrong** — three submissions for (0384, 0811, 1091), three against (0687, 0785, 0787) |
| Rocky Mountain House–Banff Park (s.15(2)) | Not one of the five places; documented support (EBC-2025-2-0619 and others) |
| Olds–Three-Hills–Didsbury | Not one of the five places; documented support (Beiseker submissions) |

Tally: the majority's statement is right in four of five places and partly wrong on Chestermere.

## Caveats and limits

1. **88 posted submissions could not be machine-parsed** (and 5 more are not in the posted files), most of them because their PDFs are image-only scans lacking a text layer or a detectable EBC-2025-X-NNN ID marker. OCR was out of scope. These could contain further supporting or opposing content. They cannot remove a supporter already found, but they could add one where none was found.

2. **Keyword search precision:** Regex uses permissive co-occurrence windows (200–300 chars) and can miss submissions where the same configuration is described in paraphrased terms without the explicit place names used here. Conversely, the Red Deer regex triggers on any Red Deer + {Blackfalds/Innisfail/Sylvan Lake/Lacombe} co-occurrence, which often simply describes the Commission's *proposed* boundaries — these are neutrals, not supports.

3. **The position classifier is unreliable.** The code looks for "support / oppose / against / recommend / should not" keywords near each match. The submissions it named as supporters at Chestermere and Red Deer do not support the minority's arrangement when read in full. The CSV rows still carry the automatic classification; no log of manual corrections exists.

4. **Minority configuration names are the audit's labels, not the submissions'.** Citizens do not typically know the minority's precise configuration names (e.g., "Red Deer-Blackfalds"). A submission proposing a functionally equivalent configuration using different names is counted as directional support. The audit's rubric must be generous enough to count these as public support for the minority's *direction*, even if not the minority's exact labels.

5. **One R1 file (`EBC2025Submissions101-150ForPosting.pdf`, 33 MB)** has disproportionately many scanned pages (the large file size is driven by scan images). R1 extraction yield is therefore lower than R2 extraction yield.

6. **Search was done against submission text only**, not attached PDFs/DOCX files referenced inside submissions (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf" as an attachment — this audit only searched the enclosing batch-PDF's text layer, so attached-file content may add additional evidence that wasn't captured).

## Next step

A full recode, under way in `findings/submissions_recode/`, will replace the stance labels. Until it lands, no stance table, weighted ranking or comparison of written submissions with hearings is reported from this search.
