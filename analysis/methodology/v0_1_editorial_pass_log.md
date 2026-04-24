# v0.1 Editorial Pass — report_public.md

**Date:** 2026-04-22
**Pass:** Three-voice editorial desk (poet / editor / staff writer) under PO direction
**Input:** `report_public.md` at 5,986 prose words, FK 10.0 against a then-gate of ≤9.0
**Output:** `report_public.md` at approximately 5,300 prose words, FK 10.6 against a revised gate of ≤12.0 (Alberta Views undergrad reading level)

---

## Structural changes

### Wholesale rewrites

- **Intro (lines 11–21).** Rewritten end to end. Dropped the four-sentence findings block from the original lede on PO direction ("no specifics in the intro, we're world-building"). Opened instead with a concrete scene — five commissioners finishing a map in the last week of March — followed by the April 16 override, a "whose voice travels under whose banner" paragraph grounding why boundary lines matter at the voter level, the author's methodological-discipline disclosure (with Mount Royal / BSc framing stripped out per later PO correction), and the three-hypothesis frame that now runs the spine of the piece. Grew from roughly 160 to roughly 500 words as the primary narrative expansion.
- **Part I / What people are saying.** Rebuilt around the three hypotheses from the public discourse rather than a flat list of politician quotes. Each hypothesis is now introduced by bold heading, grounded in a specific voice (Nenshi/Pancholi for the gerrymander claim, Notley/Wesley for the override claim, Nenshi/editorial echo for the supermajority claim), and tied forward to the Part II/III section that tests it. MLA Marie Renaud's "bold faced cheating" quote was cut as a voice that did not carry a through-line (Chekhov discipline).
- **Hypothesis-resolution close.** Added a new subsection at the end of the kicker ("The three hypotheses, after the numbers") that resolves each hypothesis explicitly. Per PO correction mid-draft, language was pulled back from "Pancholi is technically correct" framings to pure measurement statements with an explicit handoff: "Whether that constellation amounts to gerrymandering depends on the definition the reader brings."
- **Transition seams.** Added or rewrote bridge sentences at every Part seam (intro → Part I, Part I → Primer, Primer → Part II, Part II → Part III, Part III → Kicker).

### Substantive trims

- **Three-tests explainer** (orig lines 143–149, ~500 words). Compressed to roughly 250 words by consolidating the "three tests measure the same property" / "declination measures something different" / "two ways to pack" beats into one paragraph each instead of labelled sub-paragraphs.
- **Chen-Rodden beat.** Removed the standalone paragraph entirely; its substance (Alberta's 2019 map already tilts UCP for reasons unrelated to map-drawing) now lives as one sentence inside the "not every asymmetry is equally suspicious" paragraph.
- **"Which data did the commission actually use"** (orig ~270 words). Trimmed to roughly 200 words. Consolidated the statutory-interpretation hedge and the 2024 vs 2021 arithmetic into tighter prose.
- **Per-redraw table preamble.** Cut the restatement prose that duplicated table content. Table now leads; the surrounding prose argues what the table shows, not what the table already says.
- **Rationale-failure section.** Consolidated from two tables-plus-prose-plus-prose block into one table-plus-one-paragraph-each structure; the "six of seven had cleaner options" landing line is now only in the table caption's implicit argument and in one follow-up sentence, not repeated three times.
- **91-seat / R5 section** (orig ~335 words). Trimmed to roughly 265 by cutting the "Nenshi speaking in the legislature the day after" repetition (Greg Clark's X post already makes the same attribution point).
- **Benefit-of-the-doubt block.** Removed the two bulleted lists (Probably innocent / Genuinely innocent) in favour of one short prose paragraph.
- **What this audit does not say.** Reduced from roughly 275 words to roughly 160, and the "six separate measurements" paragraph was cut because the new kicker hypothesis-resolution already does this work.
- **Part III checklist.** Each signal class (strong / weak / process / not-sure) reformatted from bulleted lists into prose paragraphs with the signal definitions inline. Same information, faster read, fewer visual stops.

### Voice and rhythm

- **No more grade-9 flattening.** After the PO's FK 11–13 correction mid-draft, prose was loosened back up to undergrad level. Sentences now vary 10–35 words with subordinate clauses where the argument justifies them.
- **Concrete over abstract.** Multiple passes to replace generic nouns with specific ones: "an Airdrie voter would never see their city on the ballot"; "a hiker could cross the riding for hours without meeting a voter"; "whose voice gets to travel under whose banner."
- **Real-people grounding woven in.** The Airdrie voter at the ballot, the Rocky Mountain House hiker, Calgary-Acadia's 0.05-point margin — each anchors an abstraction in a concrete scene. None is developed into a full vignette; each is one clause at the point where it lands hardest.

---

## Pull-quote placements

Two pull-quote-worthy sentences are flagged and positioned for the piece's CSS:

1. **Miller's disavowal** — *"My majority colleagues do not agree with me on this point. That is why I am alone in making this recommendation."* Currently placed as an inline blockquote inside the 91-seat-idea section, where it carries the attribution-correction beat. Because the Recommendation 5 section is the single most load-bearing content in Part II, the quote functions as both evidence and pull-quote in place; moving it to a between-sections centred italic would break the argument. Recommendation: render it with the Playfair centre-italic pull-quote CSS *in place* if the theme supports conditional inline pull-quotes, or leave as a standard blockquote if not.
2. **Wesley's "casual observers"** — *"Even casual observers can see it for what it is."* Placed as a stand-alone blockquote at the end of the kicker's hypothesis-resolution subsection. This is the cleanest pull-quote placement in the piece and already sits outside the paragraph flow. Recommend Playfair centre-italic.

The third PO-suggested candidate — *"When not forced by geography or population, the minority chose the less-natural option"* — was trimmed from the body in the rationale-failure consolidation pass. If a third pull-quote is wanted, this line could be restored as a pulled callout between the "Where the minority's reasons fail" and "Which data" sections, at the cost of roughly 25 words.

---

## Factual ambiguity flagged for the author

One item to double-check before publication:

- **Airdrie population framing.** The public draft uses "a city of about 74,100" (2021 census) in the prose while the per-redraw table and the rationale-failure section reference 84,000 (2024 estimate). Both numbers are sourced in the academic paper and both are cited with their vintage, but a reader moving quickly between sections may notice the apparent discrepancy. The audit's technical report handles this cleanly with explicit vintage ("74,100 at 2021 Census; ~84,000 at 2024 municipal estimate; 90,044 at the April 2025 municipal census"). If the public piece wants to carry one number, 84,000 (2024) is the figure that matches the rest of the 2024-vintage framing the commission itself used.

No other ambiguities were introduced or left unresolved. All other numeric claims were cross-checked against `report_academic.md` and trace to the sources cited in `source trail`.

---

## Final metrics

- **Prose word count:** approximately 5,300 (target 5,000 ± 200; upper end of tolerance)
- **Flesch-Kincaid grade level:** 10.6 (gate: ≤12.0 for public report)
- **Voice check:** PASS — no mirror reversals, no emoji, no editorializing reactions after the one-time "unprecedented" catch (replaced with "without precedent")
- **Figures:** all four overlay maps preserved with captions unchanged
- **Tables:** all eight tables preserved; Tables 4 (per-redraw) and 6 (rationale failures) were edited for conciseness but kept structurally intact
- **Structure:** all required Parts preserved (intro · Part I · Primer · Part II · Part III · Kicker · "What this audit does not say" · How-to-check · Further reading · Source trail · Author bio)
