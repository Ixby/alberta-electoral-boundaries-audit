# Website Rewrite — Plan 2: `/` Story page

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development or executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Rewrite the public `/` (Story) page prose to the approved design — verdict-first, Canadian-high-school voice, corrected findings, no academic/Claude tells — authoring it in **English only**, then stopping at a review gate before any translation.

**Architecture:** New/edited strings live in `en.ts` under a restructured `body`/new `verdict` section; `+page.svelte`'s hero + body sections render them and wire `<Gloss key="…">` around specialist terms. No other locale is touched in this plan (translation is Plan 5, gated on the user approving the English).

**Tech Stack:** SvelteKit 2 / Svelte 5, the `t()` i18n layer, `Gloss` component, the `no_retired_figures` + voice/readability checks.

**Prose-plan note:** Unlike a code plan, the deliverable here *is* prose. This plan fixes the **structure, the exact verdict-card/boundary-box copy (already validated in the brainstorming mockups), and per-section briefs + voice rules**; the body-section prose is authored during execution against the spec's voice rules (`design.md` §4) and verified by the voice script + a read-cold pass — not pre-written verbatim for every paragraph here (that would duplicate the whole page into the plan).

**Hard gate:** This plan ends BEFORE translation. After the English `/` Story ships, STOP and get user sign-off; only then run Plan 5 (re-translate the changed keys across 18 locales).

---

## Editorial invariants (from `design.md` §3–§5 — enforce in every string)
- **No verdict on "gerrymander."** Describe the position; never declare a map "is" one. "Gerrymander" appears once, as a not-legal-in-Canada aside.
- **Outcomes, not intent** — stated once, in the boundary box. Never "the commission intended…".
- **Empower, don't advocate** — channels and questions, never positions or "support map X."
- **Corrected figures only** (`design.md` §5): ~1 in 568,000 / p ≤ 1.76×10⁻⁶; four-of-four agree; SZAT not headline; anchoring retired. The `no_retired_figures` gate enforces this.
- **Voice** (`design.md` §4): lead with the point; short declaratives; plain words; gloss specialist terms in the same breath; no triads, mirrored reversals, em-dash stacking, "it's worth noting."
- **Audience floor:** standard Canadian high school — trust civics (riding, MLA, Charter, UCP/NDP); explain the specialist layer.

---

## Task 1: Verdict card + boundary box (the hero) — exact copy

**Files:** Modify `en.ts` (add a `verdict` section); modify `+page.svelte` (hero region, above the map).

- [ ] **Step 1: Add the `verdict` strings to `en.ts`** (validated in the 2026-06-16 mockups; figures per §5):

```ts
	verdict: {
		headline: 'Alberta is redrawing its electoral map.',
		p_what: 'Every so often the province redraws its ridings — the local areas that each elect one MLA. Where the lines fall decides who you vote with, and who represents you in the legislature.',
		p_split: 'This time, the panel doing the redraw split. It produced two competing maps, and a committee will pick one later this year.',
		p_question: 'We tested both maps for one question: is either one shaped to favour a party — even if no one set out to do that?',
		p_answer: 'One of the two is. The other looks normal.',
		p_howfar: 'How far from normal? A computer drew 1.01 million legal versions of the map at random. One of the two real maps is more one-sided than all but about 1 in 568,000 of them, in the UCP’s favour. The other sits in the normal range.',
		aside: 'You might call a map shaped like that “gerrymandered.” That word has no legal meaning in Canada, so we don’t use it as a verdict. We show you what the map does; you judge. For the deeper layers — what the law actually requires, and exactly how we ran the test — see Law and Methods.',
		box_heading: 'What we can and can’t say',
		box_can_1: 'The minority map sits outside what 1.01 million neutral maps produce, in the UCP-favoured direction.',
		box_can_2: 'All four partisan-fairness measures point the same way.',
		box_cant_1: 'That any commissioner intended this — the audit reads outcomes, not motives.',
		box_cant_2: 'That the map “is” a gerrymander — that isn’t a category Canadian law recognizes.',
		box_cant_3: 'How a court would rule, or what the committee will choose.'
	},
```
(Reconcile the "four of four" count and the exact "1 in 568,000" wording against the report before commit — `design.md` §5 flags this; pin one public number.)

- [ ] **Step 2: Render the hero in `+page.svelte`** above the cover map, using `{t(lang.current,'verdict.*')}`. The "UCP" gets `<Gloss key="gerrymander">` is NOT right — instead wrap the word **gerrymander** in the aside with `<Gloss key="gerrymander">gerrymandered</Gloss>` and link "Law"/"Methods" to `/law`/`/methods`. The boundary box renders box_can_*/box_cant_* as a two-state list.

- [ ] **Step 3: Verify** `npm test -- no_retired` (green — proves no retired figure crept in), `npm run build` (✓). Visual/voice check deferred to the read-cold pass in Task 6.

- [ ] **Step 4: Commit** `feat(website-story): verdict card + boundary box (corrected, no-verdict framing)`

## Task 2: Section spine — "What's being redrawn & why it matters" (new, ~350w)
**Files:** `en.ts` (`body.why_redrawn.*`), `+page.svelte`. Author per §6.1 brief: ridings, the cycle, who draws them, why a skewed map matters to the reader. No statistics. Voice rules. Commit `feat(website-story): why-redrawn section`.

## Task 3: "Two maps, one deadline" + cover map (condensed)
Condense the existing commission-split story to ~400w; one-paragraph "how to read the map" above the existing interactive cover map (keep the map + its triggers). Commit.

## Task 4: "What the odd map does on the ground" + "What it means for you" (the ladder)
Airdrie/NW-Calgary shown on the map (jargon stripped to `<Gloss>`); then the you → community → municipality → province ladder (§6.1). The supermajority stakes described qualitatively only (no `cross_vote_share` result — it's unrun). Commit each subsection.

## Task 5: "The evidence, in plain terms" + "How to engage" + "Going deeper"
Plain 4-measure summary with every term `<Gloss>`-wrapped and "see the math" links to `/methods`; the engagement section (channels + questions, not positions); signposts to `/law`/`/methods`. Commit.

## Task 6: Read-cold voice pass + retire the old Story prose
Run `analysis/scripts/check_voice_and_readability.py` (or the viewer equivalent) on the new English; read `/` cold against §4 (kill any triad/mirrored-reversal/em-dash-stack/"it's worth noting" that slipped in); ensure the outcomes-not-intent caveat appears ONCE (the boundary box); remove the superseded old Story strings/markup. Commit.

## REVIEW GATE (do not cross without user sign-off)
- [ ] Present the rendered English `/` to the user. Only after approval proceed to **Plan 5 (translate the changed keys to 18 locales)**. Translating before approval would waste 18× the effort on prose that may change.

## Self-Review
1. **Spec coverage:** verdict+box (T1) and the 8-section spine (T2–T5) map to `design.md` §6.1; voice/figures/no-verdict invariants enforced per task; review gate before translation (§8).
2. **No retired figures:** the `no_retired_figures` gate runs in T1 Step 3 and after each task — a retired number can't ship.
3. **Scope:** English only; translation explicitly deferred to Plan 5 behind the review gate.
