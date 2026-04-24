---
name: References red team — findings
description: Hostile citation checker for the Alberta Electoral Boundaries Audit. Verifies that every URL and citation resolves to the claimed source and supports the claim being made about it.
forward_dependencies:
  - report_public.md (findings pertain to source-trail entries and inline citations)
  - report_academic.md (findings pertain to §5.2, §5.4, References, citations)
  - FROZEN_MANIFEST.md (URL-resolution spot-checks)
backward_dependencies:
  - .temp/commission_report.pdf (PDF verification of page-66 addendum and p. 352 rationale)
  - News article URLs listed in report_public.md source trail and report_academic.md citations
  - Academic / case-law citations enumerated in report_academic.md §References
---

# References red team — findings

**Date of audit:** 2026-04-23
**Reviewer role:** Hostile citation checker (this pass)
**Scope:** `report_public.md`, `report_academic.md`, `FROZEN_MANIFEST.md`, plus internal analysis cross-references and the underlying `.temp/commission_report.pdf`.
**Method:** WebFetch + WebSearch against the claimed source; cross-check quoted text against PDF pp. 62–67 via `pdftotext`. No edits made to any report file; this file records findings only.

## Executive summary

- CRITICAL: 3
- HIGH: 4
- MEDIUM: 6
- LOW: 3
- INFO: 2
- Blocked (paywall / 403 / login): 4
- Total references reviewed: ~45 distinct citations (inline + source trail + references + key internal cross-refs)

Headline: the **page 66 Miller quotes all check out verbatim against the PDF**. The **Nenshi quote is verified verbatim in multiple mirrors**. The **Rizzo v. Rizzo Shoes purposive-interpretation principle is cited substantively correctly** (though with non-standard case-name formatting). The three CRITICAL findings are: (1) attribution of the efficiency-gap 7% threshold to *Gill v. Whitford* (the SCOTUS decision never endorsed the threshold — it dismissed on standing); (2) the Smith "did not want to lose two rural ridings" citation in report_public.md is a reporter paraphrase, not a direct quote; and (3) the p. 352 "historical precedent" quote is selectively truncated — the commission actually lists four rationales, of which "historical precedent" is the last.

---

## Critical findings

### CRIT-01. *Gill v. Whitford* did not establish a 7% efficiency-gap threshold

**Citations in audit:**
- `report_public.md:55` "The efficiency gap measures the gap between the two parties' wasted-vote rates — US courts, in *Gill v. Whitford*, treated seven percent as suspect."
- `report_academic.md:92` "Partisan-bias metrics remain within the 7% efficiency-gap threshold used in *Gill v. Whitford* (2018) for all three maps."
- `report_academic.md:243` "None of the efficiency-gap values cross the 7% threshold from *Gill v. Whitford* (2018)."
- `report_academic.md:768` "The 7% magnitude is the threshold flagged in *Gill v. Whitford* (2018)."

**What the audit says:** US courts (or *Gill v. Whitford*) treated 7% as a suspect/flagged threshold.

**What the source actually says:** *Gill v. Whitford*, 585 U.S. ___ (2018), was a Supreme Court of Canada... correction: US Supreme Court decision that **vacated and remanded** the case on Article III standing grounds and did **not** endorse the efficiency gap as a measure of partisan gerrymandering, let alone a 7% threshold. The 7% threshold was proposed by Stephanopoulos & McGhee (2014/2015) in law-review articles and applied by the three-judge US district court in the Wisconsin redistricting case (*Whitford v. Gill*, 218 F. Supp. 3d 837 (W.D. Wis. 2016)). SCOTUS did not adopt it. See `https://en.wikipedia.org/wiki/Efficiency_gap` and `https://en.wikipedia.org/wiki/Gill_v._Whitford`.

**Impact:** The audit repeatedly characterizes 7% as a "US court" or "Gill v. Whitford" threshold in contexts where the number is doing rhetorical work ("one-fifth of the US-court threshold"). A careful reader who follows the citation will find SCOTUS never endorsed it. The threshold's actual pedigree is Stephanopoulos-McGhee 2014/2015 (which the audit already cites correctly in `report_academic.md:229`). The audit is therefore in conflict with itself on the same page.

**Severity:** CRITICAL because (a) the attribution misstates the legal status of the number, (b) the error is repeated four times across both reports, and (c) a hostile law-review reader would flag this as a first-page failure.

**Recommendation:** Replace all four occurrences with something like: "the seven-percent threshold proposed by Stephanopoulos & McGhee (2015) and applied in the Wisconsin district-court ruling *Whitford v. Gill* (2016), later vacated on standing by SCOTUS in *Gill v. Whitford* (2018)." Or simply: "the Stephanopoulos-McGhee seven-percent threshold."

---

### CRIT-02. Smith's "did not want to lose two rural ridings" is a reporter paraphrase, not a direct quote

**Citation in audit:**
- `report_public.md:198` "Premier Smith's stated reason for rejecting the commission's work was that it 'did not want to lose two rural ridings.' Rural preservation is the policy goal she has named in public."

**What the audit says:** Implies Smith said this verbatim; uses quotation marks around the phrase.

**What the source actually says:** The Rimbey Review April 16, 2026 article (`https://rimbeyreview.com/2026/04/16/alberta-considering-electoral-boundary-do-over/`) contains this sentence: **"Smith said Miller's addendum to the report recommends 91 ridings and the commission made it clear it did not want to lose two rural ridings."** This is a reporter's paraphrase — the subject of "did not want" is "the commission," not "Smith." Smith's stated reason is mediated through the reporter's summary.

**Impact:** The audit puts the phrase inside quotation marks and attributes it to Smith as her direct characterization of her own reason. The phrase actually describes what Smith told the reporter the commission (chair) wanted. Either Smith was paraphrasing Miller's addendum (accurate) or the reporter was paraphrasing Smith. Either way, the punctuation in `report_public.md:198` falsely implies Smith uttered these words verbatim.

**Severity:** CRITICAL in the hostile-citation frame: the audit is aware of the paraphrase-vs-quote distinction (it handles Miller quotes carefully) but stumbles here.

**Recommendation:** Drop the quotation marks, or rewrite as: "Premier Smith told reporters the commission did not want to lose two rural ridings. Rural preservation is the policy goal she has named in public." If verbatim quote is essential, find a direct Smith quote (she may have said this in Question Period — but the Rimbey Review text does not provide it).

---

### CRIT-03. Commission's p. 352 "historical precedent" rationale is truncated; four rationales given, not one

**Citation in audit:**
- `report_public.md:130` "The minority's own paperwork says the commission considered this territory. The commission's rationale for choosing the park extension, on page 352, is not community of interest. It is this, verbatim: 'the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division.' A because-we-did-it-before rationale."

**What the audit says:** The commission's rationale for including the Banff NP extension is this single phrase, which reduces to "because we did it before."

**What the source actually says:** On the PDF page containing the phrase (audit calls it p. 352; my extraction via pdftotext places it with the minority Appendix E text around PDF page 350s), the full passage is:

> "These themes included: the north-south character of economic corridors in the region along Highway 22; the unique nature of Rocky Mountain House being the only town in Clearwater County and acting as a hub for the entire surrounding population; the implications of dividing regional Indian reserves from the nearest economic hub; and the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division."

Four rationale themes, of which "historical precedent" is the last. The subsequent paragraph adds: "The proposed electoral division boundaries will keep interconnected communities together along Highway 22... Finally, Stoney Nakoda Indian reserves are added to the constituency and form the southern boundary. This allows Stoney Nakoda 142, 142B, 143, and 144 to be included in the same electoral division as the Big Horn reserve..."

**Impact:** The audit quotes the weakest of four rationales and presents it as "the" rationale. The three other rationales (economic corridors, Clearwater County hub, Indigenous reserves) are community-of-interest arguments. A hostile defender of the minority will point to this selective quotation and argue the audit mischaracterizes the commission's own reasoning. The audit's underlying finding — that the park extension itself adds no community — may still hold, but the argument is now stronger because the commission's full text has to be engaged, not just its last theme.

**Severity:** CRITICAL because the rhetorical weight of the passage rests on "not community of interest... because-we-did-it-before," and the source text contradicts both halves of that framing.

**Recommendation:** Rewrite the passage to acknowledge the four themes, then argue that (a) the economic-corridor and Clearwater-hub rationales could be served by populated alternatives (Caroline, Nordegg, Mountain View, Bighorn, Sundre) without the NP extension, and (b) the NP extension specifically is justified only by historical precedent. This is closer to the `v0_1_s15_2_reaudit.md` analysis, which already handles this distinction correctly — the public report has to match the internal analysis.

---

## High findings

### HIGH-01. Wesley quote predates the April 16 override by two weeks

**Citation in audit:**
- `report_public.md:19` "Jared Wesley, the University of Alberta political scientist who chaired the 2018 Edmonton commission, said any casual observer could see it for what it was."
- `report_public.md:288` (blockquote) "Even casual observers can see it for what it is."

**What the audit says:** Implies Wesley was commenting on the April 16 government override — the context of the paragraph is the post-vote reaction.

**What the source actually says:** Wesley's Substack post "Drawing the Line Against Gerrymandering" (`https://drjaredwesley.substack.com/p/drawing-the-line-against-gerrymandering`) is dated **April 2, 2026** — two weeks **before** the April 16 vote. Wesley's post opens: "The Government of Alberta should accept the Electoral Boundaries Commission's report and reject the minority map appended to it. Full stop. The majority recommendations add two ridings in Calgary and one in Edmonton..." Wesley is urging the government to accept the majority and reject the minority — he is not yet reacting to the April 16 override.

**Impact:** The audit sequences Wesley's comment alongside Nenshi's post-vote floor speech and Notley's post-vote op-ed, implying all three reactions to the override. In fact Wesley's "attempt to gerrymander" language was about the minority map submitted by the two UCP-appointed commissioners, not about the legislative committee created April 16. The quote is attributable to Wesley, but the context misleads.

**Severity:** HIGH because the audit's opening paragraph sets the frame, and if Wesley's comment is re-contextualised as pre-override the rhetorical weight of "any casual observer" shifts.

**Recommendation:** Either pick a post-April-16 Wesley comment, or clarify: "Writing two weeks before the vote, Wesley had already said any casual observer could see the minority's direction for what it was — 'an attempt to gerrymander Alberta's electoral map to the advantage of the governing party.' The override has since removed both maps from the table."

Also: **Wesley chaired the 2020 Edmonton Ward Boundaries Commission, not a 2018 Edmonton commission.** The report_public.md `:19` line says "chaired the 2018 Edmonton commission" — WebSearch confirms he chaired in 2020. This is a factual error inside the citation setup. Severity downgraded from CRITICAL because it is a side fact, not the load-bearing citation.

---

### HIGH-02. Notley op-ed quote is paraphrased, not verbatim

**Citation in audit:**
- `report_public.md:19` "Rachel Notley, who faced an unfavourable commission report herself as premier in 2017 and accepted it, wrote in a Globe op-ed a few days later that she 'never even casually considered abusing my power.'"

**What the source actually says:** Globe and Mail op-ed "Possible changes to Alberta's electoral map put democracy at risk" (`https://www.theglobeandmail.com/opinion/article-possible-changes-to-alberta-electoral-map-put-democracy-at-risk/`), published **April 21, 2026**, by Rachel Notley. WebFetch returns the actual Notley phrase as: **"at no time did I even casually consider abusing my power as Premier or our legislative majority to reverse the work"** (extracted with contextual verification by the WebFetch AI summariser).

The audit's phrasing ("never even casually considered abusing my power") is close but not identical to the source's "at no time did I even casually consider abusing my power as Premier or our legislative majority." A copy editor would not accept this as a direct quotation.

**Impact:** The audit places the short version in quotation marks. A hostile reader would flag this as a slight misquote.

**Severity:** HIGH because the audit's discipline throughout is very careful about Miller's quotes (to the point of transcribing page 66 verbatim). The same standard should apply to Notley.

**Recommendation:** Replace with the verbatim phrase: "she wrote that 'at no time did I even casually consider abusing my power as Premier or our legislative majority to reverse the work.'" Note the slight grammatical restructure the audit used trims "as Premier or our legislative majority" and shifts "at no time did" to "never" — both small changes individually, but cumulatively they cross the fidelity line for a quoted phrase.

---

### HIGH-03. Submission total count inconsistent across the audit

**Citations in audit:**
- `report_public.md:144` "The commission took 1,345 written submissions across two rounds of hearings. I was able to keyword-search 1,252 of them."
- `report_academic.md:538` "The commission received approximately 1,340 written submissions across two rounds of public consultation."
- `report_academic.md:540` "A keyword search with manual review of the commission's submission archive — 1,252 of approximately 1,340 submissions extracted with machine-readable text and 14 recovered via OCR..."
- `report_academic.md:808` "Requires text-search of the commission's 1,140+ submission archive."
- `report_academic.md:818` "Submission-archive evidence that the five disputed minority configurations (Airdrie, Cochrane, Chestermere, Red Deer, St. Albert) did have substantial public support in the 1,140+ record."

**What the source actually says:** Commission final report, introduction: "our Commission received **more than 1,140 written submissions** commenting on our interim report." That's 1,140+ for the **second round** only. The audit's 1,345 (or 1,340) figure likely aggregates rounds 1 and 2. But the academic report uses 1,140+ inconsistently alongside 1,340.

**Impact:** The audit's own numbers disagree across the two reports and within the academic report. The hostile reader asks: is it 1,140, 1,252, 1,340, or 1,345?

**Severity:** HIGH because the audit is built on the submission-archive verification; the total count is load-bearing.

**Recommendation:** Pick one number (and one basis — round 1 only, round 2 only, or aggregate), state the basis explicitly, and use it consistently. My best guess from the numbers: 1,140+ is round 2 alone; 1,340–1,345 is rounds 1 and 2 combined. Document the split in `submission_search_findings.md`.

---

### HIGH-04. Rizzo case-name formatting is non-standard; likely should be "Re Rizzo & Rizzo Shoes Ltd" or "Rizzo & Rizzo Shoes Ltd. (Re)"

**Citations in audit:**
- `report_public.md:134` "The Supreme Court of Canada in *Rizzo v. Rizzo Shoes* (1998) codified the modern Canadian rule of statutory interpretation..."
- `report_academic.md:369` "Canadian statutory interpretation follows Driedger's purposive principle as codified by the Supreme Court in *Rizzo v. Rizzo Shoes* (1998)..."
- `report_academic.md:382` "Under the purposive reading of §15(2) established by *Rizzo v. Rizzo Shoes* (1998)..."

**What the source actually says:** The case is *Rizzo & Rizzo Shoes Ltd. (Re)*, [1998] 1 SCR 27 (CanLII 837). It is a bankruptcy re-reference, not an inter-party dispute. The standard Canadian legal citation is "Rizzo & Rizzo Shoes Ltd. (Re)" or "Re Rizzo & Rizzo Shoes Ltd." — no "v." because there is no opposing party.

**Impact:** A Canadian law reviewer would flag the "v." usage as a citation-format error. The underlying substantive quote (Driedger's modern principle) is verbatim correct: "the words of an Act are to be read in their entire context and in their grammatical and ordinary sense harmoniously with the scheme of the Act, the object of the Act, and the intention of Parliament." (Verified against CanLII text.)

**Severity:** HIGH for an academic-edition report (where citation format matters); MEDIUM for a public-edition summary. For this audit, HIGH because the academic report's Reference list at line 994 already omits Rizzo — it lists Figueroa, Frank, Gill, Haig, and Reference re Saskatchewan, but Rizzo is missing from the court-cases section despite being cited three times in-text.

**Recommendation:** Change all three in-text occurrences to *Rizzo & Rizzo Shoes Ltd. (Re)* or *Re Rizzo & Rizzo Shoes Ltd*, and add the case to the References court-cases list with its [1998] 1 SCR 27 citation.

---

## Medium findings

### MED-01. Calgary-Acadia 2023 margin: 0.05pp vs 0.03pp

**Citation in audit:**
- `report_public.md:268` "On the night of May 29, 2023, a vote count in Calgary-Acadia came in five one-hundredths of a percentage point apart."
- `analysis/v0_1_marginal_seats_findings.md:55` shows Calgary-Acadia at NDP +0.05 pp.

**What the source says:** Public reports (e.g., daveberta.substack.com "Top 12 closest races of Alberta's 2023 election") and Global News describe Calgary-Acadia as NDP +7 votes, with an all-candidate margin of approximately 0.03 percentage points.

**Impact:** The audit's 0.05 figure is a two-party margin (NDP / (NDP+UCP)) while public reporting uses all-candidate share (NDP / total valid). Both are defensible but the numbers differ. The audit should flag this explicitly.

**Severity:** MEDIUM. The direction of the finding (razor-thin) is preserved; only the number differs.

**Recommendation:** Add a footnote in the Kicker section explaining that the 0.05 pp figure is a two-party margin, consistent with the audit's methodology throughout.

---

### MED-02. Clark's X post is cited without a retrievable URL

**Citation in audit:**
- `report_public.md:230` "Commissioner Greg Clark, one of the two opposition-nominated majority members — Clark had been nominated by NDP leader Naheed Nenshi — posted on X after the report dropped. 'In Canada,' he wrote, 'we don't want elected officials drawing their own election maps.'"
- `report_public.md:349` "Commissioner Greg Clark's post on X, April 2026, referenced at rabble.ca and albertapolitics.substack.com"
- `analysis/v0_1_chair_recommendation_5_analysis.md:48` "Clark's thread was referenced by multiple outlets (rabble.ca, albertapolitics.substack.com). Full citation pending direct archival retrieval at @GregClarkAB."

**What the source says:** WebFetch to `https://x.com/GregClarkAB` returned a 402 (paywall / rate limit). WebSearch for the exact phrase "In Canada, we don't want elected officials drawing their own election maps" attributed to Clark did not return the X post directly; `albertapolitics.ca` April 16/22 articles and `daveberta.ca` did not contain the quote in the fetched content. The internal analysis file even flags "Full citation pending direct archival retrieval."

**Impact:** The quote is presented as verbatim. Without a resolvable source URL and with the internal analysis itself acknowledging "pending direct archival retrieval," this is a load-bearing quote hanging on a placeholder.

**Severity:** MEDIUM (not HIGH because Clark's *direction* — that he supports the chair's "my colleagues disagree" disavowal — is consistent with the rest of the audit). If the quote cannot be directly sourced, it should be paraphrased or dropped.

**Recommendation:** Either retrieve the X post URL (e.g., via Wayback Machine on @GregClarkAB's timeline around April 17–20, 2026) and cite the snapshot URL in FROZEN_MANIFEST.md, or re-word as reported speech with a named secondary source (e.g., "As reported by albertapolitics.substack.com, Clark later said on social media that...").

---

### MED-03. Miller's "substantively unreasonable" and "s. 3 Charter" framings conflated with the chair alone

**Citation in audit:**
- `analysis/v0_1_chair_recommendation_5_analysis.md:77` "The chair's Addendum specifically described the minority's hybrids in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, and St. Albert as 'not something that I can condone' and said the minority report was 'substantively unreasonable' and 'likely to offend s. 3 of the Charter.'"

**What the source says:** PDF p. 67 (Miller's addendum) contains: "This is unlike the other hybrids the minority has proposed in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, and St. Albert. The minority's radical about face and substantive unreasonableness regarding these hybrids, to say nothing about the many other administrative and constitutional law problems with their report, is not something that I can condone." Verified verbatim.

However, the phrases "substantively unreasonable" and "likely to offend s. 3 of the Charter" as such actually appear in the **majority report's §X** ("Response to the Minority Report," pp. 62–64), signed by Miller + Clark + Samson, not in Miller's solo addendum. The addendum refers back to those problems. The internal analysis file is slightly imprecise in attributing "substantively unreasonable" and the Charter concern to the chair alone.

**Impact:** The distinction matters because the audit's main line is that Miller sits alone on Recommendation 5. Attributing the broader "substantively unreasonable / s. 3" critique to Miller-alone misrepresents the majority-report mechanics: those phrases are majority consensus, not Miller-alone. The audit's chain-of-evidence should distinguish Miller-alone from Miller-plus-Clark-plus-Samson.

**Severity:** MEDIUM. The evidence supports the audit's position either way; the attribution is just sloppy.

**Recommendation:** In the internal analysis file, distinguish "the majority report (signed by all three majority commissioners) characterised the minority as substantively unreasonable and likely to offend s. 3" from "Miller's addendum alone described the minority's hybrids as 'not something that I can condone' and stated the purpose of R5 as dissuading the Legislature from accepting the minority report."

---

### MED-04. DiscoverAirdrie is the primary source for Pancholi's "89 seats" quote, but the public report attributes it only obliquely

**Citation in audit:**
- `report_public.md:33` "Her framing is about the map. The shape of the lines."
- `report_public.md:34` "Pancholi has called the minority commission map... a gerrymander, and the April 16 override the act of 'cheating to secure themselves a supermajority.'"

**What the source says:** DiscoverAirdrie April 17, 2026 article (`https://www.discoverairdrie.com/articles/alberta-introduces-motion-to-review-electoral-boundaries-as-parties-dispute-commission-findings`) contains Pancholi's quote: "The commission's report presented maps based on the 89 seats that the UCP gave them to work with. That's what was taken to Albertans." It also contains her characterisation of the April 16 vote.

The phrase "cheating to secure themselves a supermajority" — the audit quotes this in quotation marks attributed to Pancholi. I could not verify this exact phrase from DiscoverAirdrie. WebSearch snippets show Pancholi using the word "cheating" but the specific "secure themselves a supermajority" wording is not confirmed in my fetches.

**Impact:** The Pancholi quote on "supermajority" may be paraphrased rather than verbatim.

**Severity:** MEDIUM. If the phrase is verbatim, cite the source. If it's paraphrased, drop the quotation marks.

**Recommendation:** Add a specific per-sentence cite for every quoted Pancholi phrase.

---

### MED-05. "1,140+" vs "1,345" — commission's own stated count

**Citation in audit:** See HIGH-03 above, and:
- `report_academic.md:508` "(CBC Edmonton, April 16, 2026; Calgary Journal, April 21, 2026)."

**What the source says:** Commission letter of transmittal (PDF page 1): "our Commission received **more than 1,140 written submissions** commenting on our interim report." So 1,140+ refers to the second round (post-interim) comments only. If round 1 submissions add to this, the audit's 1,340/1,345 figure needs its own source (i.e., a commission statement somewhere aggregating both rounds).

**Severity:** MEDIUM (duplicate of HIGH-03 to mark that the finding applies in two places).

**Recommendation:** Verify the 1,345 figure against a commission document (Appendix, methodology section, or consultation summary).

---

### MED-06. FROZEN_MANIFEST lists the 2026 commission report as 80.0 MB but the local copy is 83.9 MB

**Citation:**
- `FROZEN_MANIFEST.md:31` lists the 2026 report at 80.0 MB.
- Local `.temp/commission_report.pdf` is 83,912,947 bytes = 83.9 MB (via `ls -la`).

**Impact:** Minor. The discrepancy is 4.9% and could be a rounding or a re-download with different embedding.

**Severity:** MEDIUM (reproducibility flag), LOW if the file content hash-matches.

**Recommendation:** Add a SHA-256 hash of the local file to FROZEN_MANIFEST.md alongside byte count.

---

## Low findings

### LOW-01. FROZEN_MANIFEST Wayback snapshot dates are future-dated (e.g., 2026-04-17, 2026-04-22) — verify these are correct

**Citation:**
- FROZEN_MANIFEST entries include Wayback snapshots dated 2026-02-02, 2026-04-17, 2026-04-22, 2026-04-20, etc.

**What the source says:** Wayback snapshot URLs like `https://web.archive.org/web/20260417002435/...` were not resolved from inside this audit pass (WebFetch returned paywall/403 on most direct calls). The snapshot dates are plausible given the audit's frozen date of 2026-04-22, but the assumption that "all dates are 2026" is a working assumption, not a verified one.

**Severity:** LOW.

**Recommendation:** A standalone archival-verification pass (one URL at a time via WebFetch against the Wayback Machine's public API) would close this. Not necessary for this red-team pass.

---

### LOW-02. Source-trail line `report_public.md:350` "Statistics Canada, 2021 Census of Population and Journey-to-Work tables"

**Citation:** No URL, no table number, no direct link. The academic report at `report_academic.md:29–30` specifies Table 98-10-0459. The public report does not.

**Severity:** LOW.

**Recommendation:** Add the specific table number (98-10-0459) to `report_public.md:350`.

---

### LOW-03. `report_public.md:338–340` internal analysis links are relative paths

**Citation:** The further-reading list uses relative paths like `analysis/v0_1_marginal_seats_findings.md`. These resolve when viewing from the repo root but break when the file is rendered via the `willconner.ca` URL or any other mirror.

**Severity:** LOW.

**Recommendation:** Use GitHub blob URLs (e.g., `https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/main/analysis/v0_1_marginal_seats_findings.md`) so the links resolve when the piece is hosted off-repo.

---

## Info findings

### INFO-01. All six internal `analysis/v0_1_*.md` cross-references in `report_public.md:335–340` resolve to files that exist

Verified by `ls -la analysis/`:
- `v0_1_marginal_seats_findings.md` — exists (8,136 bytes)
- `v0_1_minority_rationales_validation.md` — exists (31,015 bytes)
- `v0_1_chair_recommendation_5_analysis.md` — exists (12,725 bytes)
- `v0_1_terms_of_reference_audit.md` — exists (31,937 bytes)
- `v0_1_s15_2_reaudit.md` — exists (35,951 bytes)
- Plus the scripts and data directories referenced in `report_academic.md`.

The internal cross-references are a closed loop; the audit's forward-reading path resolves without breaks.

### INFO-02. Source for the Calgary-Acadia +0.05 pp margin (`report_public.md:268`) is correctly grounded in `analysis/v0_1_marginal_seats_findings.md:55`, which in turn grounds in `data/v0_1_alberta_2023_results.csv`

The audit's internal grounding is consistent, even where it differs from public reporting's 0.03 figure (see MED-01).

---

## Verified references (short list for confidence)

1. **Miller "My majority colleagues do not agree with me on this point"** — `report_public.md:13`, `report_academic.md:512`, `v0_1_chair_recommendation_5_analysis.md:44`. Verified verbatim against `.temp/commission_report.pdf` p. 66. PASS.
2. **Miller "That is why I am alone in making this recommendation"** — `report_public.md:13`. Verified verbatim p. 66. PASS.
3. **Miller "This fifth recommendation is formulated for the express purpose of dissuading the Legislature from accepting the minority report"** — `report_public.md:232`, `report_academic.md:520`. Verified verbatim p. 66. PASS.
4. **Miller "not something that I can condone"** — `analysis/v0_1_chair_recommendation_5_analysis.md:77`. Verified verbatim p. 67. PASS.
5. **Recommendation 5 text (a–d)** — `analysis/v0_1_chair_recommendation_5_analysis.md:25–32`. Verified verbatim p. 66. PASS.
6. **Nenshi "full-on assault on our democracy"** — `report_public.md:17`. Verified against Rimbey Review, Lacombe Express, Stettler Independent, DiscoverAirdrie — all three mirrors carry the same quote verbatim. PASS with the caveat that the quote is from the floor of the legislature and is consistently reproduced.
7. **Smith "I've been asking every member to look at page 66"** — `report_public.md:39`. Verified verbatim against DiscoverAirdrie April 17, 2026. PASS.
8. **Pancholi "89 seats that the UCP gave them to work with"** — `report_public.md:(implicit)`. Verified verbatim against DiscoverAirdrie. PASS.
9. **Miller "substantive unreasonableness... not something that I can condone" with city list (Airdrie, Calgary, Chestermere, Cochrane, Red Deer, St. Albert)** — Verified verbatim p. 67. PASS.
10. **Electoral Boundaries Commission Act §15(2) five-criterion text** — Verified via CanLII and the commission's own reproduction pp. 15–16, 291–292 against `v0_1_s15_2_reaudit.md:17–27`. PASS.
11. **Reference re Provincial Electoral Boundaries (Saskatchewan), [1991] 2 SCR 158 — "effective representation" standard** — Verified via CanLII 1991 SCC 61; McLachlin J's para. 26 and para. 33 are correctly referenced by `report_academic.md:832`. PASS.
12. **Stephanopoulos & McGhee (2014/2015) efficiency gap** — Verified; the audit cites the concept correctly. The error is only in how the 7% threshold's legal status is characterised (see CRIT-01).
13. **Chen & Rodden (2013) "Unintentional gerrymandering"** — Verified via DOI `10.1561/100.00012033`. PASS.
14. **Warrington (2018) "Quantifying gerrymandering using the vote distribution"** — Verified via DOI `10.1089/elj.2017.0447`. PASS.
15. **McDonald & Best (2015) "Unfair partisan gerrymanders"** — Verified via DOI. PASS.
16. **Katz, King, & Rosenblatt (2020) "Partisan fairness in district-based democracies"** — Verified via DOI `10.1017/S000305541900056X`. PASS.
17. **Altman & McDonald (2011)** — Cited in `report_academic.md:748` as "four-axis redistricting-audit discipline." The reference is not in the References list (`report_academic.md:930–925`). See MED-07 below — adding one more medium finding.
18. **CBC Edmonton April 16, 2026** — `report_public.md:347` URL (`https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743`) was 403 in this pass; exists in public search results. Verified by proxy.
19. **Airdrie 2025 municipal census: 90,044** — Verified against `airdrie.ca` and `airdriecityview.com`. PASS.
20. **Elections Alberta "very challenging" timeline** — Verified. PASS.

---

### MED-07 (late finding). Altman & McDonald (2011) cited in-text but missing from References list

**Citation in audit:**
- `report_academic.md:748` "The six-dimensional framing follows the four-axis redistricting-audit discipline of Altman and McDonald (2011)..."

**What the source says:** The References list at `report_academic.md:930–990` has no "Altman" or "Altman & McDonald" entry. The likely target is Altman, M., & McDonald, M. P. (2011). "BARD: Better Automated Redistricting." *Journal of Statistical Software*, 42(4), or their separate 2011 work.

**Impact:** The reader cannot look up the citation.

**Severity:** MEDIUM.

**Recommendation:** Add the Altman & McDonald (2011) bibliography entry.

---

## Blocked references (paywall / login / 403)

These could not be fully resolved in this pass. They are marked "blocked," not "wrong."

1. **`https://www.theglobeandmail.com/canada/alberta/article-alberta-government-rejects-commissions-proposed-changes-to-provinces/`** — Globe and Mail paywall. News article confirmed to exist via WebFetch's AI summary. Direct verbatim read not possible.
2. **`https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743`** — CBC News. WebFetch returned 403 for both main and `/lite/story/` URLs in this pass, though WebSearch confirmed the article's existence and substance. Direct verbatim read not possible in this pass.
3. **`https://x.com/GregClarkAB`** — X / Twitter requires auth; 402 on WebFetch. Clark's post could not be directly retrieved. See MED-02.
4. **`https://www.nationalobserver.com/2026/04/17/news/ucp-smith-gerrymandering-electoral-map`** — 403 on WebFetch.
5. **Elections Alberta `abebc_2026_rpt_final.pdf`** — WebFetch returns a content-length error (file >10 MB limit). The local copy at `.temp/commission_report.pdf` is the audit's working substitute; the URL does resolve publicly at the FROZEN_MANIFEST "last verified" date.
6. **FROZEN_MANIFEST Wayback snapshot URLs** — Not individually resolved in this pass. See LOW-01.

---

## Summary recommendations for audit authors

1. **Fix the *Gill v. Whitford* 7% attribution everywhere** (CRIT-01, four occurrences).
2. **Drop quotation marks around Smith's "did not want to lose two rural ridings"** (CRIT-02) and Notley's "never even casually considered abusing my power" (HIGH-02) unless direct-quote sources are found.
3. **Rewrite the p. 352 passage** to acknowledge the commission's four rationales rather than quoting only "historical precedent" (CRIT-03).
4. **Date-tag the Wesley quote** to April 2, 2026 and re-contextualise it pre-override (HIGH-01). Fix "2018 Edmonton commission" → "2020 Edmonton Ward Boundaries Commission."
5. **Pick one submission-count number** and source it (HIGH-03, MED-05).
6. **Fix Rizzo case-name format** to *Rizzo & Rizzo Shoes Ltd. (Re)* and add the case to the References court-case list (HIGH-04).
7. **Source or re-word the Clark X quote** with a retrievable URL or secondary source (MED-02).
8. **Distinguish Miller-alone from majority-consensus** in the internal analysis file for the "substantively unreasonable" framing (MED-03).
9. **Add the Altman & McDonald (2011) bibliography entry** (MED-07).
10. **Hash the PDF and record SHA-256 in FROZEN_MANIFEST** to close the 80 MB / 83.9 MB discrepancy (MED-06).

---

## Method notes

- This pass used WebFetch against public URLs and WebSearch for cross-verification. Paywalled sources (Globe, CBC, National Observer, X) were marked blocked rather than wrong.
- PDF verification was done via `pdftotext` (MinGW / Poppler) against `.temp/commission_report.pdf` pages 62–67 and around the "historical precedent" passage.
- No edits were made to any audit file. No commits. This file is an analysis output only.
- Budget consumed: ~30K tokens of the ~40K allocated; ~90 min of the ~120 min budget.
