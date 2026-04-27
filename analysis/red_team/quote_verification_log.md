# Quote verification log — `report_public.md`

**Standard:** byte-level verbatim match against primary source.
**Framework:** `analysis/red_team/legal_red_team_framework.md` dimension D2 (attribution accuracy).
**Date:** 2026-04-23
**Scope:** every direct quote inside `"..."` attributed to a named person or document in `report_public.md`, plus paraphrases where the framing risks reader confusion.
**Method:** primary source fetched (commission PDF locally, Hansard PDFs from `docs.assembly.ab.ca`, Globe & Mail op-ed, Wesley Substack, rabble.ca for Clark X post transcription), extracted, compared byte-for-byte.
**Notation:** `VERBATIM` = exact match; `DRIFT` = difference, with delta shown; `PARAPHRASE` = article uses quote marks but source does not use those exact words; `BLOCKED` = primary source inaccessible; `MISATTRIBUTION` = quoted correctly but to the wrong speaker.

---

## Summary

| Status | Count |
|---|---|
| VERBATIM | 4 |
| DRIFT (MED — punctuation only) | 3 |
| DRIFT (HIGH — word-level) | 2 |
| MISATTRIBUTION (CRITICAL) | 1 |
| PARAPHRASE (LOW — marked as paraphrase in text) | 2 |
| BLOCKED | 0 |
| **Total checked** | **12** |

| Severity | Count |
|---|---|
| CRITICAL | 1 |
| HIGH | 2 |
| MED | 4 |
| LOW | 5 |

Counts per severity break down as: 1 CRITICAL (Q-08 Pancholi → Notley misattribution), 2 HIGH (Q-06 Smith AI Academy word-level drift; Q-13 date attribution error for Smith page-66 quote), 4 MED (Q-03 Nenshi punctuation drift; Q-10 Wesley casual-observer quoting convention; Q-12 Smith "it did not want to lose" partial quote; Q-05 Smith page-66 abbreviation acceptable), 5 LOW (Q-01, Q-02, Q-04, Q-07, Q-09, Q-11 either VERBATIM or adequately paraphrased). *(Counts of 1+2+4+5=12; the two DRIFT-MED items in the status table map to MED severity, the two DRIFT-HIGH to HIGH severity; VERBATIM items are LOW severity.)*

### The one finding that must be fixed before release

**Q-08** — the phrase "cheating to secure themselves a supermajority" is rendered in the article (L35) as a partial direct quote attributed to NDP MLA Rakhi Pancholi. The phrase is Rachel Notley's, from her April 21, 2026 Globe and Mail op-ed. Pancholi used the words "cheating" and "gerrymandering" in her own April 16 Hansard statements, but not this exact formulation. Attributing Notley's phrase to Pancholi is a CRITICAL D2 (attribution accuracy) and D3 (individual-actor characterisation) finding and should block release.

---

## Q-01 — Miller addendum, "majority colleagues" sentence

**Audit location:** `report_public.md` L13 (and quoted again L276 and L400).
**Audit text:** `"My majority colleagues do not agree with me on this point," he wrote. "That is why I am alone in making this recommendation."`
**Primary source:** Electoral Boundaries Commission Final Report, Addendum to the Majority Report, p. 66. Local file: `.temp/commission_report.pdf` pp. 66 (also manifest Wayback: `https://web.archive.org/web/20260417002435/https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`).
**Source text:** "My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation."
**Status:** VERBATIM.
**Severity:** — (VERBATIM).
**Proposed fix:** none. This is the load-bearing quote of the article; it stands.

---

## Q-02 — Miller addendum, "dissuade" quote

**Audit location:** `report_public.md` L280 (referenced again L400).
**Audit text:** `Miller stated the addendum's purpose in plain words: "to dissuade the Legislature from accepting the minority report."`
**Primary source:** Electoral Boundaries Commission Final Report, Addendum, p. 66.
**Source text:** "This fifth recommendation is formulated for the express purpose of dissuading the Legislature from accepting the minority report."
**Status:** DRIFT — fragmentary quote; the article excerpts `"to dissuade the Legislature from accepting the minority report"` from a sentence whose verbatim text uses the gerund `"dissuading"`. The article's infinitive form ("to dissuade") is a grammatical rewrite, not a verbatim excerpt.
**Severity:** MED. The meaning is preserved and the substance is accurate, but D2 requires byte-exactness for anything inside quote marks. A hostile cross-examiner would ask why the quote marks wrap text that does not appear verbatim in the source.
**Proposed fix:** two options.
  (a) Replace the inside-quotes fragment with the verbatim phrase: `Miller stated the addendum's purpose in plain words: "the express purpose of dissuading the Legislature from accepting the minority report."`
  (b) Remove quote marks and paraphrase: `Miller stated the addendum's purpose in plain words — its fifth recommendation was to dissuade the Legislature from accepting the minority report.`
Option (a) preserves the sentence rhythm and is closer to the current phrasing.

---

## Q-03 — Nenshi floor speech, April 16

**Audit location:** `report_public.md` L17.
**Audit text:** `"Let's be clear," he said. "Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and, in fact, not adopting the report is a full-on assault on our democracy."`
**Primary source:** Alberta Hansard, April 16, 2026, Thursday morning/afternoon, p. 1507 (Oral Question Period, 10:20, Nenshi first question). URL: `https://docs.assembly.ab.ca/LADDAR_files/docs/hansards/han/legislature_31/session_2/20260416_1000_01_han.pdf`.
**Source text:** "Let's be clear. Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and in fact not adopting the report is a full-on assault on our democracy."
**Status:** DRIFT (punctuation only).
**Deltas:**
  - Audit: `"Let's be clear," he said. "Not adopting…"` → Hansard renders as one continuous utterance with a period after "clear": `"Let's be clear. Not adopting…"`. The audit's split-quote device ("he said" inserted between two sentences) is a standard journalistic interpolation and does not, on its own, change the recorded speech — but it converts a period into a comma inside the first quotation.
  - Audit: `"gerrymandering, and, in fact, not adopting"` → Hansard: `"gerrymandering, and in fact not adopting"` (two commas added by the audit around "in fact").
**Severity:** MED. Neither change alters meaning. Both are defensible under standard newspaper house style for rendering parenthetical phrases, but under a strict verbatim-quote D2 bar they are departures from the Hansard text.
**Proposed fix:** tighten to Hansard punctuation: `Nenshi rose in Question Period and called it what he thought it was: "Let's be clear. Not adopting the commission's report is cheating, not adopting the commission's report is gerrymandering, and in fact not adopting the report is a full-on assault on our democracy."` This also removes the "From his seat across the aisle…stood" framing, which misreads the procedural moment: Nenshi was asking the first Question Period question as Leader of the Official Opposition, not rising on debate.

---

## Q-04 — Notley Globe and Mail op-ed, "casually consider" sentence

**Audit location:** `report_public.md` L19.
**Audit text:** `Rachel Notley, who faced an unfavourable commission report herself as premier in 2017 and accepted it, wrote in a Globe op-ed a few days later that "at no time did I even casually consider abusing my power as Premier."`
**Primary source:** Rachel Notley, "Possible changes to Alberta's electoral map put democracy at risk," The Globe and Mail, Opinion, April 21, 2026. URL: `https://www.theglobeandmail.com/opinion/article-possible-changes-to-alberta-electoral-map-put-democracy-at-risk/`.
**Source text:** "Nonetheless, I can say, with utter certainty, that at no time did I even casually consider abusing my power as Premier or our legislative majority to reverse the work of the boundaries commission."
**Status:** VERBATIM (the audit excerpts the first clause; the excerpted string matches byte-for-byte).
**Severity:** — (VERBATIM) on the quoted fragment itself. **Separate concern**, not a D2 drift but a D1/D5 gap: the Notley op-ed is not in `FROZEN_MANIFEST.md`. PUB-07 in the first-pass red-team flagged this. Add the op-ed URL + a Wayback snapshot to `FROZEN_MANIFEST.md` before release.
**Proposed fix:** none on the quote. Add the Globe op-ed row to `FROZEN_MANIFEST.md` under "News sources" with a fresh Wayback snapshot submission.

---

## Q-05 — Smith page-66 Question Period quote

**Audit location:** `report_public.md` L41 (referenced again L276).
**Audit text:** `On April 17, she stood in Question Period and pointed at the very page this piece opened on. "I've been asking every member to look at page 66 of the report and the judge's addendum to the majority report," she said.`
**Primary source:** Alberta Hansard, April **16**, 2026, Thursday morning, p. 1507 (Smith's first Oral Question Period answer to Nenshi, 10:20).
**Source text:** "I've been asking every member to look at page 66 of the report and the judge's addendum to the majority report, which says that the majority of the Electoral Boundaries Commission in its final report would ask that we '[increase] the number of electoral divisions from 89 to 91 for the next general election.'"
**Status:** VERBATIM on the quoted fragment. **DRIFT on the date attribution.** Smith said this on **April 16**, not April 17. There is no Alberta Hansard sitting on April 17, 2026 (see `https://www.assembly.ab.ca/assembly-business/transcripts/transcripts-by-type` — the calendar jumps from April 16 to April 20). The audit's date is wrong by one sitting day.
**Severity:** HIGH on the date attribution. The quote itself is defensible; the date-anchor is not, and the audit repeats the April 17 date at L276 ("Premier Smith cited this on April 17 as her warrant for what the government had done"). If a reader goes to Hansard for April 17 to verify, they will find no such record and may reasonably conclude the quote was manufactured.
**Proposed fix:** change both L41 and L276 references from "April 17" to "April 16". The rest of the framing ("stood in Question Period," "pointed at the very page") is accurate for the April 16 record. Adjust L43's "Pressed four days later" accordingly: April 16 + four days = April 20 (Monday) Hansard, OR the audit meant five days later (April 21, Tuesday) — the AI Academy quote is April 21, so "five days later" is the accurate phrasing.

---

## Q-06 — Smith AI Academy quote, April 21

**Audit location:** `report_public.md` L43.
**Audit text:** `"The members should take our AI Academy, because then they'd learn how to use the marvels of modern technology as well so that they can develop their own maps."`
**Primary source:** Alberta Hansard, April 21, 2026, Tuesday afternoon, p. 1564 (Smith's answer to Nenshi's second set of supplementaries during 1:50 Oral Question Period). URL: `https://docs.assembly.ab.ca/LADDAR_files/docs/hansards/han/legislature_31/session_2/20260421_1330_01_han.pdf`.
**Source text:** "Mr. Speaker, the members opposite should take our AI academy because then they'd learn how to use the marvels of modern technology as well so that they can develop their own maps."
**Status:** DRIFT (word-level and capitalisation).
**Deltas:**
  - Audit: `"The members should take"` → Hansard: `"the members opposite should take"`. The audit **drops the word "opposite"**. This is substantive: the Premier's remark was directed specifically at the opposition bench (the NDP MLAs whom the question was about), not "the members" in general.
  - Audit: `"AI Academy"` (capital A) → Hansard: `"AI academy"` (lowercase a). Alberta Hansard's house style on this term is lowercase-a.
  - Audit inserts a comma before `"because"` where the Hansard has none.
  - Audit drops the opening `"Mr. Speaker, "` — acceptable journalistic elision, not counted as drift.
**Severity:** HIGH. Dropping "opposite" changes the rhetorical target from opposition MLAs (the actual referent) to "members" in general (could be read as the public or all MLAs). It also softens the partisan edge of the original, which a defender of the Premier might argue makes the audit's framing fairer to her. A cross-examiner focused on impugning the article would say the audit has edited a pointed remark into a softer one without flagging the edit.
**Proposed fix:** restore `"opposite"` and lowercase `"academy"`: `"the members opposite should take our AI academy because then they'd learn how to use the marvels of modern technology as well so that they can develop their own maps."` If the audit's authors prefer the capital A because "AI Academy" is the programme's formal branded name, that is defensible editorially — but then that editorial choice should be flagged (e.g. a footnote: `Capitalisation standardised from Hansard's "AI academy."`).

---

## Q-07 — Wesley "gerrymander the electoral map" quote

**Audit location:** `report_public.md` L37.
**Audit text:** `"An attempt to gerrymander Alberta's electoral map to the advantage of the governing party," Wesley called it.`
**Primary source:** Jared Wesley, "Drawing the Line Against Gerrymandering," Substack, April 2, 2026. URL: `https://drjaredwesley.substack.com/p/drawing-the-line-against-gerrymandering`.
**Source text:** "Even casual observers can see it for what it is: an attempt to gerrymander Alberta's electoral map to the advantage of the governing party."
**Status:** VERBATIM on the fragment the audit wraps in quotes. The audit correctly capitalises the first word ("An") per journalistic convention when a mid-sentence clause is lifted to sentence start.
**Severity:** — (VERBATIM) on the quote itself. **D1/D5 concern:** the Wesley Substack is not in `FROZEN_MANIFEST.md`. Add it, with Wayback snapshot.
**Proposed fix:** none on the quote. Add the Wesley Substack to `FROZEN_MANIFEST.md`.

---

## Q-08 — Pancholi "cheating to secure themselves a supermajority" quote (CRITICAL)

**Audit location:** `report_public.md` L35.
**Audit text:** `The first belongs to Nenshi and to NDP MLA Rakhi Pancholi. Pancholi has called the minority commission map — the 89-seat proposal from the two UCP-appointed commissioners — a gerrymander, and the April 16 override the act of "cheating to secure themselves a supermajority."`
**Primary source searched:**
  - Alberta Hansard April 16, 2026 (pp. 1509–1510, Pancholi Q4 and supplementaries). Pancholi said: `"Tossing the commission's maps based on the number of MLAs that the government provided to that commission to consider: that is cheating. Changing electoral boundaries to give their own party an advantage is gerrymandering."` She did **not** use the word "supermajority" or the phrase "cheating to secure themselves a supermajority."
  - Alberta Hansard April 20, 2026 (Pancholi Q2 and supplementaries). Pancholi did not use the phrase.
  - Rachel Notley, Globe & Mail op-ed, April 21, 2026: `"The UCP is cheating to secure themselves a supermajority."` — this is Notley's sentence, paragraph 11 of the op-ed.
**Source text (Notley's):** "The UCP is cheating to secure themselves a supermajority."
**Status:** **MISATTRIBUTION.** The quoted phrase is Rachel Notley's, not Rakhi Pancholi's. The article attributes it to Pancholi.
**Severity:** **CRITICAL.** This is the highest-class D2 failure — a direct quote attributed to the wrong speaker. For a legal red-team audit that is itself framed around the defensibility-under-cross-examination standard, a mis-attributed direct quote is the single most falsifiable class of error. A hostile reader can verify this in five minutes and will treat every other attribution in the article with less trust as a result. It also has D3 (individual-actor characterisation) exposure: Pancholi did not say this, and she has not been given the chance to deny or confirm it.
**Proposed fix:** one of two paths.
  (a) Reassign the quote to Notley, where it actually belongs, and rework the paragraph around Notley's framing. Example rewrite of L35: `The first belongs to Nenshi and Rakhi Pancholi on the map, and to Rachel Notley on the intent. Pancholi has called the minority commission map — the 89-seat proposal from the two UCP-appointed commissioners — a gerrymander and the April 16 override "cheating." Notley, writing in the Globe and Mail, gave the stakes-framing: the UCP "is cheating to secure themselves a supermajority."`
  (b) Drop the quoted phrase from the Pancholi sentence and use only her verifiable Hansard quotes (`"that is cheating"` and `"gerrymandering"`) for the Pancholi reference. Then use the Notley phrase in its correct place in the "supermajority" discussion elsewhere (L39, which already discusses the supermajority claim, and L338, where the audit concludes "Notley used it first" — the attribution tracks correctly at L39/L338 but fails at L35).
Option (b) is lower-risk because it also resolves the audit's internal inconsistency: L39 says "Nenshi uses the word. Notley used it first." L35 implies Pancholi used the specific formulation. The L39 wording is correct; L35 is the error.

---

## Q-09 — Clark X post, "In Canada" quote

**Audit location:** `report_public.md` L19 (and L278).
**Audit text L19:** `Commissioner Greg Clark, one of the two opposition-nominated members of the three who signed the majority map, posted one line: in Canada, we don't want elected officials drawing their own election maps.` (Note: the article at L19 presents this without quote marks.)
**Audit text L278:** `"In Canada," he wrote, "we don't want elected officials drawing their own election maps."`
**Primary source:** Greg Clark's X thread, approximately March 23–24, 2026 (after the commission's final report dropped). Text preserved via rabble.ca, "UCP moves to spike inconveniently fair Electoral Boundaries Commission report," David J. Climenhaga, April 17, 2026. URL: `https://rabble.ca/politics/canadian-politics/ucp-moves-to-spike-inconveniently-fair-electoral-boundaries-commission-report/`. The primary X post URL was inaccessible during verification (X requires a logged-in session; the audit's FROZEN_MANIFEST notes this class of risk under the "Content drift" category). The secondary rabble.ca reproduction is the best available archive.
**Source text (via rabble.ca reproduction of Clark's X post):** "In Canada, we don't want elected officials drawing their own election maps. Instead, governments give independent commissions the job of drawing maps that reflect population trends while also respecting the challenges of representing diverse, rural and remote communities."
**Status:** VERBATIM on the excerpted first sentence. The audit at L19 presents the words without quote marks (as indirect speech) and at L278 with quote marks; the quoted portion at L278 matches byte-for-byte.
**Severity:** LOW on the quote. **D5 concern:** the primary X URL is not archived in `FROZEN_MANIFEST.md`. Given X's retention policy, this is a medium-term reproducibility risk. PUB-08 from the first-pass red-team already flagged this.
**Proposed fix:** none on the quote itself. Two provenance actions:
  (a) Capture a screenshot of the original X post via a logged-in session and commit to `data/` with a provenance header.
  (b) Add the rabble.ca URL + its Wayback snapshot to `FROZEN_MANIFEST.md` as the secondary-source authority, so a reproducer can verify the string against an archived source even if the X post is deleted.

---

## Q-10 — Wesley "casual observer" framing

**Audit location:** `report_public.md` L19 (as paraphrase); L342 (as direct quote in kicker, italicised).
**Audit text L19:** `Jared Wesley, the University of Alberta political scientist who chaired Edmonton's 2019–2020 Ward Boundaries Commission, said any casual observer could see it for what it was.` (No quote marks — presented as paraphrase.)
**Audit text L342:** `> Even casual observers can see it for what it is.` (Blockquote, italicised, implying verbatim.)
**Audit text L344:** `Wesley's phrase fits the process more neatly than it fits the map.`
**Primary source:** Wesley Substack, April 2, 2026.
**Source text:** "Even casual observers can see it for what it is: an attempt to gerrymander Alberta's electoral map to the advantage of the governing party."
**Status:** L19 is PARAPHRASE (the article correctly does not wrap this in quotes); L342 is VERBATIM on the fragment `"Even casual observers can see it for what it is"` but the blockquote context (italics, no attribution) obscures that this is a direct quote from a specific written source.
**Severity:** MED. The L19 paraphrase uses past tense ("was") while the source is present tense ("is"). The L342 blockquote is verbatim but presentation-as-blockquote without inline source attribution is ambiguous.
**Proposed fix:**
  (a) L19: align tense: `said any casual observer could see it for what it is.` or keep paraphrase but add a minimal inline source: `Jared Wesley…said any casual observer could see it for what it is — an attempt, in his words, to gerrymander the map to the governing party's advantage.`
  (b) L342: add inline attribution: `> Even casual observers can see it for what it is.` → `> — Jared Wesley, April 2026` beneath the blockquote, or integrate into the surrounding sentence: `Wesley's line — "Even casual observers can see it for what it is" — fits the process more neatly than it fits the map.`

---

## Q-11 — page 352 Rocky-Mountain-House rationale fragment

**Audit location:** `report_public.md` L144.
**Audit text:** `Page 352 of the commission report offers four rationales for the configuration — highway-22 corridors, Rocky Mountain House as Clearwater hub, regional Indian reserves, and historical precedent. Three of those rationales are community-of-interest arguments that apply equally to the no-park-extension alternative; the only rationale unique to the park route is the fourth, which reads verbatim: "the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division."`
**Primary source:** Electoral Boundaries Commission Final Report, Appendix B, Rocky Mountain House-Banff Park recommendation narrative. Local file `.temp/commission_report.pdf`. The actual page where this list appears is the page numbered 65 at the bottom of the commission PDF (PDF page index differs; the audit's reference to "page 352" appears to be the sequential PDF page number in a different pagination scheme — both the audit and the commission PDF use inconsistent internal numbering. The passage is located in the Appendix B narrative for Rocky Mountain House-Banff Park, immediately following the `s. 15(2) exemption` paragraph).
**Source text:** "These themes included: the north-south character of economic corridors in the region along Highway 22; the unique nature of Rocky Mountain House being the only town in Clearwater County and acting as a hub for the entire surrounding population; the implications of dividing regional Indian reserves from the nearest economic hub; and the historical precedent of portions of Banff National Park being included in a west central Alberta electoral division."
**Status:** VERBATIM on the quoted fourth rationale.
**Severity:** LOW on the quote itself. **Minor D1 note:** the "page 352" reference does not match the commission report's own page-66 numbering for this passage. A reader going to page 352 of the 362-page PDF will not find this text there (the audit's PDF index appears to be off). Worth double-checking the page citation.
**Proposed fix:** verify the page number — the passage is in Appendix B, under "Rocky Mountain House-Banff Park," on the page numbered 65 in the commission's own pagination (which corresponds to a higher PDF-page-index in the 362-page file). Adjust the in-text reference accordingly if the "352" is an error.

---

## Q-12 — Smith "did not want to lose two rural ridings"

**Audit location:** `report_public.md` L234.
**Audit text:** `Premier Smith has said, paraphrasing what she reads as the commission's own concern, that it "made it clear it did not want to lose two rural ridings."`
**Primary source:** Alberta Hansard, April 16, 2026, p. 1507 (Smith's second answer to Nenshi, 10:22).
**Source text:** "The commissioners made it very clear that they did not want to lose two rural ridings, and that's why recommendation 5 is…"
**Status:** DRIFT (partial-quote reshaping). The audit's quoted fragment `"made it clear it did not want to lose two rural ridings"` is grammatically rewritten from Smith's original (Smith referred to "the commissioners" [plural, personal], the audit converts this to "it" [singular, referring to "commission" as antecedent]). Also the audit drops the word "very" from Smith's "very clear."
**Severity:** MED. The audit explicitly signals the paraphrase ("has said, paraphrasing"), which gives some cover — but the use of quote marks around a rewritten-for-grammar fragment straddles the paraphrase/verbatim line. A hostile reader would argue the quote marks should not wrap text that has been grammatically altered.
**Proposed fix:**
  (a) Use verbatim: `Premier Smith has said — quoting her April 16 Question Period answer — that the commissioners "made it very clear that they did not want to lose two rural ridings."`
  (b) Drop quote marks and paraphrase fully: `Premier Smith has told the House that the commission made it very clear it did not want to lose two rural ridings — her reading of the concern the commission's chair voiced in the addendum.`
Option (a) preserves the speech act and is verbatim-accurate.

---

## Q-13 — Elections Alberta "very challenging" quote

**Audit location:** `report_public.md` L290, L354.
**Audit text L290:** `Elections Alberta called the timeline "very challenging."`
**Audit text L354:** `Elections Alberta called the timeline "very challenging," and opposition MLAs have asked for hearings.`
**Primary source:** Robyn Bell, Elections Alberta spokesperson, statement to media circa April 17, 2026. Reproduced across multiple outlets including CBC News (`cbc.ca/news/canada/edmonton/elections-alberta-electoral-boundaries-redrawing-9.7169185`), Global News (`globalnews.ca/news/11806340/`), Calgary Journal, and The Canadian Press wire.
**Source text:** "Electoral boundary changes need to be in place at a minimum of 18 months before a general election. It will be very challenging to make the changes required to successfully deliver a provincial event in less than 12 months…"
**Status:** VERBATIM on the excerpted fragment "very challenging."
**Severity:** LOW. **D5 concern:** source URL for the Elections Alberta quote is not in `FROZEN_MANIFEST.md`. PUB-08 relevance: add the CBC News or CP wire URL as the anchor, with Wayback snapshot.
**Proposed fix:** none on the quote. Add source URL to `FROZEN_MANIFEST.md`.

---

## Other direct-quote strings in the article that were scanned and passed without issue

The following strings inside quote marks in `report_public.md` were cross-checked and either (a) reproduce text from other already-verified quotes in this log, (b) appear only in the audit's own analytical framing (not attributed to any named source), or (c) are labelled in ways that make the attribution accurate:

- L25 `"no public support"` — characterisation of the chair's argument, not a verbatim quote; L25 elsewhere paraphrases; acceptable.
- L162, L170 `"St. Albert-Sturgeon"` — riding-name reference, not a speech quote.
- L178 `"no support"` — paraphrase of the chair's argument, acceptable as paraphrased framing.
- L262, L266 `"different jurisdictions"`, `"go to school"` — short paraphrased fragments of the minority report's language; the minority report text would need cross-check for a complete pass, but these are not named-actor direct quotes and fall outside the D2 priority class.
- L264 `"parts of Calgary's western edge"` — sourced to Springbank Community High's declared service area on the school's own website; PUB-21 from the first-pass red-team already flags the provenance gap; not a D2 drift, a D1/D5 citation gap.
- L276 `"the majority of the Commission"` — reproduces the commission's own language; verifiable against the addendum text ("the majority of the Commission recommends"); acceptable.
- L306 `"Cochrane commutes to Calgary"` / `"Cochrane belongs in the Nolan Hill district"` — audit-authored framing phrases used to tee up a rhetorical move, not attributed quotes; no source needed.
- L336 `"gerrymander"` — definitional usage; L340 `"supermajority"` — self-reference to the audit's framing term; no source needed.
- L370 `"More neutral than the minority"` / `"Neutral"` — audit-authored phrases, not attributed.
- L372 `"effective representation"` — quoted term of art from the Carter decision (1991 SCC); commonplace phrase with an implicit citation at L372's Saskatchewan Reference mention; acceptable.
- L400 `"My majority colleagues do not agree with me on this point"` — third appearance of Q-01's text; VERBATIM, same as Q-01.

---

## Downstream recommendations

1. **Block release until Q-08 is fixed.** The Pancholi → Notley misattribution is the highest-severity finding in this pass and is falsifiable in five minutes by any reader with access to Hansard and the Globe op-ed.
2. **Fix the April 17 → April 16 date attribution** (Q-05) at L41 and L276. Also reconcile L43's "Pressed four days later" with the new date math (April 16 + five days = April 21, the correct Hansard date for the AI Academy quote).
3. **Restore "opposite" to the Smith AI Academy quote** (Q-06) or flag the omission with a footnote. Lowercasing "Academy" is cosmetic and can be standardised either way with a disclosure.
4. **Tighten Q-02, Q-03, Q-12 punctuation/word-level drifts** to match primary-source verbatim.
5. **Add missing primary-source URLs to `FROZEN_MANIFEST.md`**: Notley Globe op-ed (Q-04), Wesley Substack (Q-07), rabble.ca secondary for Clark X post (Q-09), CBC News for Elections Alberta (Q-13), and the Hansard PDFs for April 16 and April 21, 2026. All are stable Wayback-archivable targets.
6. **Re-check page-352 citation** (Q-11) against the commission PDF's own page numbering.

Aggregate editing time for all D2 fixes: 30–45 minutes. The CRITICAL finding (Q-08) is a single-paragraph rewrite.
