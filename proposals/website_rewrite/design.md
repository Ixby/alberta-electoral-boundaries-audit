# Website rewrite & restructure — design spec

**Status:** Design — pending user review, then implementation plan
**Date:** 2026-06-16
**Supersedes:** `proposals/content_restructure.md` (2026-05 migration proposal). That proposal was a *migration, not a rewrite*, predated the multilingual i18n architecture, and quoted pre-correction figures. This is a fresh take per a 2026-06-16 brainstorming session and replaces it.

---

## 1. Goal

Rewrite **and** restructure the public viewer so a general Albertan reader can understand, in plain language, what the boundary redraw is, whether either map is shaped to favour a party, what that means for them, and how to verify it — without wading through academic prose or undefined jargon. The rewrite optimizes four things the user named, all at once:

1. **Voice / engagement** — less academic, less "AI." Lead with the point; short declaratives; plain words; no hedging, no triad tics, no mirrored reversals, no em-dash stacking.
2. **Structure / argument flow** — verdict-first, then orientation, then personal stakes, then evidence, then verification.
3. **Accuracy to corrected findings** — bake in this session's corrections (see §5). No stale Fisher / 1-in-15M / "declination disagrees" language anywhere.
4. **Density / accessibility** — front-load the answer; gloss the specialist layer; trust the civics basics.

## 2. Audience (controls every editorial choice)

**Floor: a standard Canadian high-school education.** Validated in the brainstorming session.

- **Assume (do not explain):** how a legislature, election, political party, MLA, and riding work; that ridings get periodically redrawn; that the Charter of Rights exists; UCP and NDP as Alberta's two main parties.
- **Explain (the specialist layer):** the word "gerrymander" (an American term, not standard Canadian curriculum — gloss on first use, flagged as having no legal meaning in Canada); the statistics (the 1.01M-map neutral ensemble, "1 in 357,000," what each partisan-bias measure means); the legal doctrine (s.3 Charter "effective representation" — plain words on `/`, depth on `/law`); the commission split and what "minority report / majority report" means.
- **Reading level:** Flesch-Kincaid ~grade 11 on `/` (per the project's public-report standard, which overrides the academic FK 13–18). `/law` and `/methods` may run higher for their narrower audiences.

## 3. Editorial principles (non-negotiable)

These come from the audit's conflict-of-interest posture and are the source of its credibility.

1. **No verdict on "gerrymander."** The word has no legal definition in Canada. The site describes the statistical and structural position and lets the reader draw their own legal conclusion. It never declares a map "is" a gerrymander.
2. **Outcomes, not intent.** Every claim about a map favouring a party is stated as an outcome ("shaped to favour a party — even if no one set out to do that"), never as motive. Stated **once** canonically (the verdict card's "what we can / can't say" box) and not repeated four times as today.
3. **Empower, don't advocate.** The site never tells the reader which map to support or what reform to back. "What you can do" provides channels and questions, not positions. Reform options are presented comparatively (what other jurisdictions do, with trade-offs), never as recommendations.
4. **Symmetric and honest.** The majority map's own outlier (mean-median p0.924, NDP-tail) is reported, not buried. Both maps are scored by the same tests (see `analysis/methodology/evaluation_symmetry_matrix.md`).

## 4. Voice rules (the "less academic, less Claude" register)

Concrete, enforceable rules for every string written:

- Lead each paragraph with its point. No throat-clearing ("It is worth noting that…", "Importantly,…").
- Short sentences; rarely more than two clauses. Cut subordinate-clause stacking.
- Plain Anglo-Saxon words over Latinate: *shows* not *demonstrates*, *odd* not *anomalous*, *one-sided* not *asymmetric* (in body prose), *rules* not *statutory framework*.
- Gloss every specialist term **in the same breath** the first time it appears — a short appositive or a `<Gloss>` popover, never a forward reference.
- Banned constructions: templated triads ("not X, not Y, but Z"), mirrored reversals ("the question is not whether… but whether…"), em-dash appositive stacking (one em-dash per paragraph max), "in a sense / arguably / somewhat" hedges, rhetorical questions used as transitions.
- One idea per paragraph. If a paragraph needs a label ("The structure." / "The statistics.") to hold together, split or rewrite it.
- Numbers as hooks, in plain comparison: "more one-sided than all but about 1 in 357,000" beats "at the 99.9997th percentile."
- No emoji (house rule).

A short worked example (the verdict opener), to anchor the register, is in §6.1.

## 5. Corrected-findings basis (the prose must use these, not the stale ones)

All from this session's corrections. The rewrite is the first place the public copy is brought fully into sync.

| Claim | Use this | NOT this (retired) |
|---|---|---|
| Joint headline | Ch1 alone p = 1.40×10⁻⁶ (~1 in 714,000); dependence-robust bound **p ≤ 2.80×10⁻⁶ (~1 in 357,000)** | Fisher 6.87×10⁻⁸ / "1 in ~15 million" |
| Partisan metrics | **Four of four** agree in the UCP-favoured direction (EG p94.4 sub-threshold but aligned, mean-median p99.98, declination **p98.79 UCP-tail**, seats@50/50 p99.99) | "three agree, declination disagrees" / "p1.21 NDP-tail" |
| SZAT (boundary-choice test) | Exploratory context only; does not survive the spatial null (p≈0.19); **not in the headline** | "Channel 2, p = 0.0024, confirmatory" |
| Structural tests (Lane 2) | Discriminating pre-registered tests fire on the minority, none on the majority. **Exact count to be pinned in the plan** — public report frames it "four of four (anchoring retired as the fifth)"; the structural battery scores minority 5/5, majority 0/5 on S1–S6. Reconcile to one public number before copy is written. | "five structural tests" without the anchoring-retraction note |
| Municipal anchoring | Retired — did not survive canonical recomputation (minority 72%, majority 80%, both in-norm) | the old 4.9× anchoring gap as a live finding |
| Majority map | Honestly reported: within neutral on 3 of 4; at p0.924 (NDP-tail) on mean-median | silence |
| Supermajority / vote-share sweep | The `cross_vote_share` test is **unrun**. May describe the supermajority *stakes* qualitatively on `/`'s "your province" rung; must **not** present any vote-share-curve result as a finding. | any "crosses 58 seats at X%" number |

## 6. Information architecture — three routes (audience-tiered)

Validated: three self-contained, cross-linked routes. Sticky nav `Story · Law · Methods`, active route highlighted. The map lives on `/` only. Progressive-disclosure toggles (the user's interest from option C) are used *inside* `/law` and `/methods` where depth stacks, not on `/`.

### 6.1 `/` — Story (target ~3,500–4,500 words, FK ~11)

The casual reader's spine. Verdict-first, then orient, then personal stakes, then plain evidence, then engage.

**Hero — the on-ramp + verdict (above the map).** Plain situation first, answer second, then the hook number. Worked example (the locked register):

> **Alberta is redrawing its electoral map.**
> Every so often the province redraws its ridings — the local areas that each elect one MLA. Where the lines fall decides who you vote with, and who represents you in the legislature.
> This time, the panel doing the redraw split. It produced two competing maps, and a committee will pick one later this year.
> We tested both maps for one question: **is either one shaped to favour a party — even if no one set out to do that?**
> One of the two is. The other looks normal.
> How far from normal? A computer drew 1.01 million legal versions of the map at random. One of the two real maps is more one-sided than all but about **1 in 357,000** of them, in the UCP's favour. The other sits in the normal range.

Immediately below: the **"what we can / can't say" box** (the single canonical home of the outcomes-not-intent caveat and the no-verdict stance). "Gerrymander" is introduced here as a not-legal-in-Canada aside, with links to Law and Methods.

**Section spine (reading order):**
1. Hero verdict + boundary box (above).
2. **What's being redrawn, and why it matters** (new, ~350w) — ridings, the cycle, who draws them, who's drawing them this time, why a skewed map matters to the reader. No statistics yet.
3. **Two maps, one deadline** (condensed) — the commission split 3–2; the two maps; the committee choosing; the timeline. Interactive cover map as the visual anchor with a one-paragraph "how to read it."
4. **What the odd map does on the ground** (condensed) — Airdrie split four ways, packing in NW Calgary — shown on the map via the existing ED/anomaly triggers. Stat and legal jargon stripped to glosses; depth linked out.
5. **What it means for you** (new, the personal→provincial ladder) — you (riding lookup: does yours change, who's your MLA) → your community (Airdrie as the lived example) → your municipality (a split city's lost bargaining power) → your province (party-power stakes, including the supermajority threshold described qualitatively).
6. **The evidence, in plain terms** (~400w) — the 1.01M-map test in one plain paragraph; the four agreeing measures named and one-line-glossed; the structural fingerprints. Every term `<Gloss>`-wrapped; "see the math" pills link to `/methods`.
7. **How to engage** (new) — riding lookup, the next hearing's date/livestream (from a maintained JSON with a visible "verified" date), questions a reader could ask (not positions), how to submit a brief. Channels, not scripts.
8. **Going deeper** — signposts to `/law` and `/methods`.

Removed from `/` (moved to depth routes): p-value/MCMC/ReCom mechanics, the four-metric tables, Lane 1/Lane 2 framing, deep s.3/Saskatchewan-Reference/Quebec treatment, pre-registration/OSF/falsification, data-gap detail, the anchoring-correction detail.

### 6.2 `/law` — for advocates, journalists, MLAs, policy staff (target ~2,500 words)

Plain-professional register (still no academic throat-clearing). Progressive-disclosure toggles for case detail.

Sections: why "gerrymander" isn't a Canadian legal term; the s.3 *effective representation* test (plain, then a toggle to the Saskatchewan Reference detail and McLachlin J. quote); the commission split and the committee that replaced it (why that's unusual); the Quebec contrast (permanent commission, ⅔ override, the April 2026 SCC ruling); **what this audit can and cannot establish legally** (explicit limits); **reform pathways** — process levers and structural models other jurisdictions use, as a comparison table with trade-offs, **no endorsement**; engagement channels (standing, complaint routes, the legislative process), described not encouraged; legal references.

### 6.3 `/methods` — for analysts, statisticians, legal scholars, opposing experts (target ~3,500 words)

Technical and precise; reproducibility-focused. This is where the corrected statistical framing lives in full.

Sections: the 1.01M-map ReCom ensemble (what MCMC/ReCom is, how to read the dot-plot); the four partisan-bias measures, each with its corrected value and the Amendment-10 declination-sign note; **why the joint headline is Ch1 + a dependence-robust Bonferroni bound, and why the earlier Fisher combination was retired** (this is the public home of that correction); SZAT presented as exploratory-only with the block-permutation result; the structural tests (Lane 2) and the symmetry matrix (both maps scored the same); pre-registration, drand seeds, and the falsification conditions; cross-validation; data coverage and known gaps; the documented anchoring retraction; the verdict restated with intervals; **reproducing this audit** (repo, OSF, ensemble outputs, raw inputs, how to file a methodological concern).

## 7. Components

- **`Gloss` popover** (`viewer/src/lib/components/Gloss.svelte`) + **single-source glossary** (`viewer/src/lib/glossary.ts`, but see §8 — it must be i18n-aware). Click-to-define for every specialist term; `aria-expanded` + `role="tooltip"`; Escape closes; ≤8 terms per route. Definitions short (2–3 plain sentences) and consistent across routes.
- **Verdict card** — a styled hero component on `/`, fed from i18n strings.
- **Sticky three-route nav** — in `+layout.svelte` (already exists; extend with the three pills). RTL-safe (this session's logical-CSS pass already converted directional CSS; new components must follow logical-property rules).
- **Riding lookup** and **engagement JSON** — carried over from the prior proposal's design (FSA-first static lookup, Nominatim opt-in; a maintained `engagement.json` with a visible "verified" date). Detail deferred to the implementation plan; not re-litigated here.

## 8. Multilingual — re-translate all 18 locales (validated scope)

This is the heaviest part and a first-class design constraint, not an afterthought.

- The rewrite **changes the i18n key set** (new sections, new strings, retired strings). `en.ts` is authored first as the canonical source.
- **All 18 non-English locales are re-translated** as part of this effort — not left to fall back to English. Translation is machine-assisted draft + the project's existing review/IRR-style workflow, language by language.
- **Key-set discipline:** because every changed key multiplies by 18, the rewrite minimizes gratuitous key churn — stable section keys, no needless renames — even though the *content* is new.
- **The glossary must be i18n-aware:** `glossary.ts` as written in the old proposal hardcodes English. Definitions move into the locale files (or a per-locale glossary map) so popovers translate. This is a design change from the superseded proposal.
- **Sequencing:** English ships first (the other locales fall back to English for new keys in the interim), then locales are completed in speaker-count order (the existing dropdown order). The site is shippable in English at each step.
- RTL (Arabic, Urdu) already handled by this session's logical-CSS pass; new components inherit it.

## 9. Migration / build approach (phased, shippable at each step)

1. **Plumbing** — `Gloss.svelte`, i18n-aware glossary, extend `+layout.svelte` nav. No content moved.
2. **Empty `/law` and `/methods` routes** with anchors; nav works.
3. **Author `en.ts` rewrite** section by section, `/` first (verdict card + spine), then `/law`, then `/methods`. Wrap specialist terms in `<Gloss>`. Preserve external anchors / add a hash-redirect for legacy `#section-N`.
4. **Consolidate the outcomes-not-intent caveat** to the single boundary box.
5. **Re-translate locales** in speaker-count order; each language is a separable unit.
6. **Voice + readability pass** — run `check_voice_and_readability.py`; read each route cold for the §4 rules and the §3 principles.

Each phase is a separable commit; the site stays live throughout.

## 10. Out of scope

- New analysis or findings (the prose reflects existing, corrected results only).
- Presenting any `cross_vote_share` / vote-share-sweep result (unrun).
- Petition / signature / sample-letter generators (violate the empower-don't-advocate principle).
- Reader-progress indicators, print/PDF combined view, interactive calculators.

## 11. Acceptance criteria

- A casual reader on `/` sees the plain situation **and** the answer in the first screen, with no undefined specialist term above the fold.
- No academic/Claude tells in `/` body copy (no triads, mirrored reversals, em-dash stacking, "it's worth noting"); FK ~11 verified by the voice script.
- No retired figure or framing anywhere (no Fisher 1-in-15M, no "declination disagrees," no live anchoring gap). All claims match §5.
- The outcomes-not-intent caveat appears **once** canonically; the site never declares a map "is" a gerrymander; no section tells the reader which map or reform to back.
- Every specialist term in `/` body copy has a working `<Gloss>` (or inline gloss) that **translates** in every locale.
- The three-route nav is visible and correct on every route; the map and existing ED/anomaly triggers still work on `/`.
- All 18 locales are re-translated (or English-fallback with a tracked completion list); RTL renders correctly.
- A high-school-educated reader can read only `/` and come away knowing what was decided, what's at stake for them, and one thing they can do; a policy/legal reader gets `/`+`/law`; an analyst can reproduce or critique from `/methods`.
