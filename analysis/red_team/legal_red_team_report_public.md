# Legal red-team — `report_public.md`

**Standard:** defensible under hostile cross-examination in a court of law.
**Framework:** `analysis/red_team/legal_red_team_framework.md` (ten dimensions D1–D10).
**Date:** 2026-04-23
**Scope:** a first-pass review of the public-facing magazine article. This
document flags findings; it does not rewrite. Each finding carries a
dimension, severity, specific line reference, and a proposed fix.

---

## Summary table

| # | Severity | Dimension | Region | One-line |
|---|---|---|---|---|
| PUB-01 | HIGH | D3, D6 | L11 | "Justice Dallas Miller sat alone and wrote a sentence most chairs would never write" — characterisation of what chairs do is opinion, not fact, presented in fact voice |
| PUB-02 | MED | D2 | L13 | Miller addendum verbatim quote needs byte-level verification against the commission PDF page 66 |
| PUB-03 | MED | D1 | L15 | Vote count "44 to 36" and motion content ("no public hearings required, none scheduled") need inline citation |
| PUB-04 | HIGH | D3, D6 | L15 | "throw out both maps the commission produced — the majority's and the minority's — and hand the pencil to a committee of five MLAs" — "throw out" and "hand the pencil" are narrative characterisations that a hostile reader could construe as bias; the motion's verbatim language is "rejected" and "replaced" |
| PUB-05 | MED | D2 | L17 | Nenshi "cheating…gerrymandering…assault on our democracy" quote requires Hansard verbatim match plus Hansard date + speech record line reference |
| PUB-06 | HIGH | D2 | L19 | Wesley "any casual observer could see it for what it was" is a paraphrase shown inside a sentence that also names direct quotes from Notley; reader cannot distinguish which is verbatim and which is paraphrase |
| PUB-07 | MED | D1, D2 | L19 | Notley Globe op-ed quote needs URL + archive snapshot; currently traceable only through the FROZEN_MANIFEST's "News sources" section, which does not list the Globe op-ed |
| PUB-08 | MED | D1, D2 | L19, L278, L403 | Clark X-post quote ("in Canada, we don't want elected officials drawing their own election maps") cites "rabble.ca and albertapolitics.substack.com" as secondary sources; primary X post URL not archived; the X platform's retention policy makes primary-source loss a real risk |
| PUB-09 | HIGH | D3, D6 | L25 | "the chair's own claim that five minority configurations had 'no public support' turned out to be materially wrong on three of them" — adverse claim about a sitting judge; supported in the body (L162) on one of three ("materially wrong" applied only to Chestermere); the L25 framing overstates by using "three" where the body count is "one materially wrong plus one split plus one not matching"; internal inconsistency with L162 is itself a HIGH finding |
| PUB-10 | MED | D2 | L41 | Smith Question Period quote requires Hansard date (April 17, 2026) + speech record line reference |
| PUB-11 | MED | D2 | L43 | Smith "take our AI Academy…develop their own maps" quote requires Hansard date (approximately April 21, 2026, "four days later") + line reference |
| PUB-12 | MED | D6 | L43 | "It raised the question of how a committee would use such tools" — prior edit removed motive-imputation ("it was a retort, it was also a tell"); current framing is defensible |
| PUB-13 | HIGH | D1, D5 | L81 | Commissioner backgrounds ("former Alberta Party MLA, nominated by NDP leader Naheed Nenshi", "also NDP-nominated", "both UCP-nominated") require an inline citation to the Order in Council establishing the commission and the nomination record. Currently these characterisations rest on the audit's own interpretation of public documents without inline anchors |
| PUB-14 | MED | D1 | L160 | "roughly 1,345 written submissions across two rounds of hearings. I was able to keyword-search 1,252 of them" — submission count and search-coverage fraction require method citation (`analysis/v0_1_submission_search_method.md` if one exists, else flag as D4 methodology gap) |
| PUB-15 | HIGH | D1, D5 | L162 | Submission count breakdowns per configuration ("four submissions in support, four opposed, fifteen neutral", "three submissions in favour and only one opposed") rest on `data/submission_search_dataset.csv` per file inventory. Inline citation to that file, with row/column selector, is needed for each count |
| PUB-16 | MED | D1 | L164 | "Rocky Mountain House-Banff Park attracted five submissions in support and one opposed. Olds-Three Hills-Didsbury as a rural unit attracted three in support, one opposed" — same D1/D5 as PUB-15 |
| PUB-17 | HIGH | D3, D6 | L276 | "What she did not read out is the sentence a paragraph later" — narrow factual claim about what Smith did or did not say. Requires Hansard transcript showing the specific paragraph was skipped. If Hansard transcript shows she read more than this article implies, the claim is falsified. Needs primary-source anchor |
| PUB-18 | HIGH | D3, D6 | L280 | Miller "to dissuade the Legislature from accepting the minority report" — direct quote imputing persuasive intent to a sitting judge's addendum. If verbatim, defensible. If paraphrase, defamation exposure. Must be verbatim verified against the commission PDF |
| PUB-19 | MED | D2 | L402 | "Premier Smith's April 17 legislature statement and April 16 Rimbey Review quote" — Rimbey Review quote is referenced but not reproduced verbatim in the audit body. Needs either verbatim reproduction or removal of the Rimbey citation until a specific quote is anchored |
| PUB-20 | MED | D1 | L262 (schools rebuttal, recently revised) | "about 375 Sylvan Lake students — about a third of the town's grades-nine-to-twelve population — are bussed into Red Deer Catholic schools each morning" — derives from an educationnewscanada.com article and Chinook's Edge planning documents. Neither URL is in `FROZEN_MANIFEST.md`. New citation needed |
| PUB-21 | MED | D1 | L262 | "Springbank Community High…lists 'parts of Calgary's western edge' in its declared service area" — derives from the school's own website. URL not in manifest. New citation needed |
| PUB-22 | MED | D4 | L203 (neutral-ensemble test, recently inserted) | Percentile numbers (100th, 1.7th, 96th) cite the MCMC ensemble script and the 10k sample data. D4 reproducibility gate: the script must produce the cited percentiles exactly on a fresh run. Currently covered under `analysis/red_team/red_team_code_fixes.md` which verified reproduction |
| PUB-23 | LOW | D10 | L203 | "A hundred-thousand-sample version is in progress" — prospective claim. Adequate as labelled. |
| PUB-24 | MED | D3 | L35 | Pancholi characterisation ("cheating to secure themselves a supermajority") as a direct quote — needs Hansard / press conference / social-media date anchor |
| PUB-25 | LOW | D7 | Throughout | Author's standing (no visible disclosure of Alberta political affiliation or past commission involvement beyond "wconn161@mtroyal.ca" byline). If author has a public-record party donation history or prior commission role, disclosure section at bottom of article (before THE SOURCE TRAIL) would close the gap |

**Counts:** 0 CRITICAL, 9 HIGH, 14 MEDIUM, 2 LOW.

## Discussion per dimension

### D1 Evidentiary chain

The single largest class of findings. Most adverse factual claims about named actors (Miller, Smith, Clark, Nenshi, Notley, Wesley, Pancholi) are supported somewhere in the source-trail footer, but very few are supported *inline* in the body. The magazine-style narrative voice makes inline citation harder, but the D1 bar expects every specific, testable claim to trace to a primary source. Proposed fix: introduce a per-section footnote anchor (e.g., a superscript number referencing the THE SOURCE TRAIL list). This is minimally disruptive to the narrative voice.

### D2 Attribution accuracy

Every direct quote attributed to a named person (10+ instances) needs verbatim verification against the primary source (Hansard for MLA floor statements, commission PDF for Miller's addendum, the actual op-ed / X post for media attributions). Without this verification, any of the 10+ quotes could be paraphrase-creep from an earlier draft. Proposed fix: a single verification pass producing `analysis/red_team/quote_verification_log.md` where every direct quote is paired with the primary-source extract. This is a one-time mechanical check; low effort, high return.

### D3 Individual-actor characterisation

The highest defamation-risk claims are:
- Miller "materially wrong on three of [five configurations]" (L25)
- Smith "She did not read that sentence" (L15) and "What she did not read out is the sentence a paragraph later" (L276)
- Miller "to dissuade the Legislature from accepting the minority report" (L280)

Each rests on either a verifiable primary source (Hansard for Smith; commission PDF for Miller) or on the audit's own analysis (the "materially wrong" count). For defamation defence in Canadian common law, the relevant heads are:
1. **Truth (justification)** — if provable by primary source, fully defends.
2. **Fair comment** — if labelled as opinion and based on demonstrable facts, defends.
3. **Responsible communication on matters of public interest** — Grant v. Torstar (2009) SCC — if reporting was diligent and the matter is one of public interest.

Proposed fix: mark each of the three claims above with the supporting evidentiary anchor inline. For L25, either (a) tighten "three" to "one" to match L162 or (b) add the explanatory sentence the body says but the intro omits.

### D4 Methodology reproducibility

Principal concerns:
- L25's "three findings contradicted the direction I expected" summary claims — each traceable to a specific analysis artifact (§15(2) re-audit, cross-election stability test, submission-search dataset). The reproducer needs a map from the three summary claims to the three artifacts.
- L160's submission search coverage fraction (1,252 of 1,345) requires a documented search methodology.
- L203's MCMC percentiles require the ensemble CSV + ensemble script.

These are addressable via a reproducibility appendix in the academic report that the public report can reference. Currently the public report points to the academic report ("[Full technical report](...)") which in turn points to the analysis docs. The chain is intact but multi-hop. A one-hop direct reference from public to the method doc would tighten it.

### D5 Data provenance

All CSV/JSON/GPKG artifacts cited explicitly by name in the public report body (there are two implicit ones: the submission search dataset and the 2023 Statement of Vote) need a provenance line. Currently the submission search dataset's origin is undocumented in `data/submission_search_dataset.csv`'s header.

### D6 Privilege / scope (fact vs opinion vs allegation)

Most fact/opinion lines are clear in the public report. The problem cases are:
- "sat alone and wrote a sentence most chairs would never write" (L11) — narrative voice, fine as colour commentary, but a hostile reader could argue the "most chairs would never" is a factual claim requiring a survey of commission chairs; soften to "wrote what most commission chairs avoid writing" or similar opinion framing.
- "materially wrong on three" (L25) — see D3 above.
- "to dissuade the Legislature from accepting the minority report" (L280) — if verbatim, fine. If the article is paraphrasing the addendum's stated purpose, that must be made clear.

### D7 Conflict of interest

No disclosure section. The author byline ("wconn161@mtroyal.ca") identifies the author as affiliated with Mount Royal University (Calgary) but does not disclose any past or present involvement in Alberta boundary-drawing processes, political party donation history, or related consulting. For a hostile cross-examination witness-standing challenge, the absence of a disclosure section is a weakness. Proposed fix: add one paragraph between `THE METHOD` and `FURTHER READING` labelled "THE AUTHOR" with the standard conflict-of-interest disclosures.

### D8 Copyright / fair dealing

The article includes four map-overlay figures. The overlays are derived from commission PNG thumbnails via the HSV-red-mask / affine-georeference pipeline — i.e., they reinterpret the underlying boundary data rather than reproducing the commission's visual design. This is defensible under s.29 fair dealing for criticism/review. Proposed fix: ensure each figure caption in the article acknowledges the commission final report as the underlying data source.

### D9 PII / confidentiality

No PII in the article. The "woman in her thirties, she has lived in Airdrie for eleven years, she works at a dental office on Main Street" composite is a narrative device and cannot be re-identified as any specific person. Safe.

### D10 Time-stamped / falsifiable claims

Several prospective claims ("the November draft is where…", "by the next commission convenes…") are labelled as prospective. Adequate. The one place to tighten: the MCMC "preliminary" labelling in the new neutral-ensemble section states "percentiles may shift" — good; the rest of the report should carry the same "preliminary pending commission shapefile release" labelling where applicable.

## Recommended next actions

1. **Block release** until the 9 HIGH findings are addressed. Most are one- or two-sentence fixes; aggregate editing time estimated at 2–3 hours.
2. **Queue a parallel agent at 4:30am restart** to do the verbatim-verification pass (D2, findings PUB-02, PUB-05, PUB-06, PUB-07, PUB-08, PUB-10, PUB-11, PUB-17, PUB-18, PUB-19, PUB-24).
3. **Add a disclosure paragraph** (D7 PUB-25) — minimal effort, high cross-examination defensibility return.
4. **Resolve the L25 / L162 internal inconsistency** (PUB-09) — this is the single most defamation-exposed claim and the fix is a 20-word edit.
5. **Add inline anchors** (D1, findings PUB-03, PUB-13, PUB-14, PUB-15, PUB-16, PUB-20, PUB-21) — numbered endnotes keyed to THE SOURCE TRAIL.

## Not-yet-reviewed in this pass

This first-pass focuses on the highest-risk classes (named-actor quotes and characterisations; specific number claims; framing of adverse claims about identifiable individuals). The following classes of claim are flagged for a later pass:

- **Data provenance of every CSV/GPKG** cited by name in the public report body (D5) — requires cross-check against the `data/` inventory and each file's header.
- **Figure attribution** for the four overlay PNGs (D8) — currently adequate; review after the overlays are rebuilt per the design critique above.
- **Copyright posture on the commission PDF reproductions** (D8) — no images from the PDF are reproduced, only numeric extracts; review if that changes.

## Parallel-agent assignment (for 4:30am restart)

When rate limits reset, four agents run in parallel:
1. **Quote verification** — fetch Hansard / commission PDF / social-media primary sources, produce `analysis/red_team/quote_verification_log.md`, report any paraphrase drift as CRITICAL or HIGH per D2.
2. **Data provenance** — walk every `data/*.csv` and `data/*.gpkg`, confirm each file has a provenance header pointing at `FROZEN_MANIFEST.md`, produce `analysis/red_team/legal_red_team_data_artifacts.md`.
3. **Script reproducibility** — re-run each script in the triage list from the framework, compare outputs against the numbers cited in the public report, produce `analysis/red_team/legal_red_team_scripts.md`.
4. **Academic-report parallel pass** — apply this same framework to `report_academic.md`, produce `analysis/red_team/legal_red_team_report_academic.md`.
