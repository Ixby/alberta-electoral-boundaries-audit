# Content Restructure: Audience-Tiered, Layered Argument

**Status:** Proposal — pending implementation
**Branch:** `claude/busy-ride-DmwUm`
**Goal:** Make ~8,400 words of mixed narrative, legal, and statistical content readable for the primary audience — a high-school-educated Albertan with passing interest in provincial politics — while still serving engaged advocates, journalists, MLAs, and the GIS / legal / statistical professional reader. Move from one dense scroll to three audience-tiered routes connected by a shared glossary.

## Primary reader (controls every editorial choice on `/`)

A curious Albertan who:
- Has heard "the boundaries are being redrawn" and doesn't know what that means concretely.
- Doesn't know what an electoral district is, where theirs is, or who their MLA is.
- Doesn't know that "gerrymander" is a contested word in Canadian law.
- Wants to know whether this affects them personally, locally, and how to act if it does.
- Will bounce in under 60 seconds if the first viewport asks them to understand the efficiency gap.

The site must onboard this reader, then layer depth on top. Engaged advocates, MLAs, EAs, and academics are served by the deeper routes — they are not the reason `/` exists.

## Editorial principle: empower, don't advocate

The author has opinions about which map is better and what reforms Alberta should adopt. The site does not. Every action-layer section is written to enable the reader to form and act on their own conclusions, not to import the author's. Concretely:

- **No "support the majority map" framing.** The audit shows what each map does structurally; the reader decides what to do with that.
- **No "Recommendations for X" sections.** They become "Reform pathways" that present options other jurisdictions use, with their tradeoffs, leaving the choice to the reader.
- **"Contact your MLA" prompts ask questions, not request positions.** The reader writes their own ask.
- **Comparative framing over prescriptive.** "Quebec does X, BC does Y, the federal commissions do Z, Alberta does W" — readers see the contrast and judge for themselves.

This principle distinguishes the audit from advocacy material and is the source of its credibility. When in doubt: describe, don't direct.

## Diagnosis

Feedback says the read is dense. The audit currently:
- Buries the verdict in Section 6 at line 604, ~5,000 words into the page.
- Splits legal framing across two distant sections (Section 6 intro lines 380–383 and Section 7 lines 664–669).
- Intermixes MCMC/ReCom/p-value methodology with the on-the-ground story.
- Defines jargon (efficiency gap, declination, mean-median, anchoring) inside callout boxes encountered mid-flow.
- Repeats the "outcomes, not intent" caveat in 4+ places because there's no single canonical statement of it.

Reader's question — *"Is this a gerrymander?"* — is answered, but not where a casual reader looks first.

## Resolved decisions

| Question | Decision |
|---|---|
| Page architecture | Three routes, audience-tiered: `/` (general public), `/law` (engaged readers / advocates / MLAs), `/methods` (GIS, statistical, legal scholars) |
| Reading order intent | Narrative first, law second, science third — corresponding to audience depth |
| Glossary UX | Click-to-define popovers on inline jargon, single source of truth |

## The layered argument

Each route serves a deeper audience and ends with a "what you can do" section calibrated to that reader:

| Route | Audience | Voice | Ends with |
|---|---|---|---|
| `/` | Curious citizen, low prior knowledge | Conversational, second-person, concrete examples (Airdrie, your MLA) | "How to engage" — postcode lookup, contact channels, question prompts, hearing dates |
| `/law` | Advocates, journalists, MLAs, policy staff | Plain professional, citation-aware, structural | "Reform pathways" — levers other jurisdictions use, with tradeoffs, no endorsement |
| `/methods` | Statisticians, GIS analysts, legal scholars, opposing experts | Technical, precise, reproducibility-focused | "Reproducing this audit" — code, notebooks, OSF pre-registration, data downloads |

A reader can stop at any tier and still leave with a complete, defensible understanding at that level. A reader who wants more is signposted to the next tier at every relevant point.

## Route plan

### `/` — For the curious Albertan (target ~4,500 words)

The reader arrives knowing nothing. By the time they leave they should know what redistricting is, why this particular map matters, how it touches them personally, and one concrete thing they can do.

**Hero / Verdict block** (above the fold, before the map)

A single bordered card answering the reader's three questions in plain language:

> **Is this a gerrymander?**
> The minority map shows the structural fingerprints of one. Five of the audit's structural tests fire on the minority proposal; none fire on the majority.
>
> **What does that mean in Canadian law?**
> Canadian courts don't use the word "gerrymander." The test under s.3 of the Charter is whether boundaries give voters *effective representation*. This map raises that question; only a court can answer it.
>
> **What does it mean for Albertans?**
> If adopted, the minority map shifts seats in a way that could turn a competitive election into a supermajority. The majority map does not.
>
> [Read the legal framing →](/law)  [See the math →](/methods)

**Epistemic boundary card** (immediately below verdict)

A small, persistent "What we can and can't say" block:

| | Statement |
|---|---|
| ✓ Can say | The minority map sits outside what 1.01M neutral maps produce. |
| ✓ Can infer | The map likely fails s.3 effective-representation tests a court would apply. |
| ✗ Cannot say | That any commissioner intended this outcome. |
| ✗ Cannot say | What the November vote will be. |
| ✗ Cannot say | How a court would actually rule. |

**Section flow** (audience-onboarding spine):

1. **What is redistricting and why should you care?** (new, ~400 words)
   Plainest-language onboarding. What an electoral district is. Why boundaries are redrawn periodically. Who is supposed to draw them and who is drawing them this time. Why a poorly-drawn map matters to the reader specifically. Sets the stakes before any data appears.

2. **The Map** (existing Section 1 condensed to ~250 words)
   Interactive cover map — the visual anchor. One paragraph telling the reader how to read it.

3. **Two Maps, One Commission, One Deadline** (existing Section 2 condensed to ~400 words)
   The human story: the commission split 3–2, two competing maps were produced, the Lunty committee is choosing, November is the deadline.

4. **What the Minority Map Does on the Ground** (existing Section 4 condensed to ~600 words)
   Airdrie split, packing in NW Calgary, anchoring departures. Keep the inline `ed-trigger` and `anomaly-trigger` buttons. Strip statistical jargon (moved to `/methods`); strip legal jargon (moved to `/law`). Every effect is shown on the map.

5. **What this means for you and your community** (new, ~900 words)
   The personal-to-provincial ladder. Five short subsections, each ~180 words:
   - **You.** Look up your riding. Does it change? Who is your MLA right now, and would that change?
   - **Your community.** What stays together and what gets split. Airdrie as the canonical lived example — four MLAs for one city, no single representative who owes accountability to the whole place.
   - **Your municipality.** How a fractured city loses bargaining power on infrastructure, school boards, and provincial funding. Calgary NW as the example.
   - **Your region.** Rural-vs-urban implications. Boundary departures from municipal lines and what they cost.
   - **Your province.** Party-power consequences. The supermajority effect: closure, debate control, floor-crossing, the legislative dynamics that change at a 2/3 threshold.

6. **A short history of gerrymandering** (new, ~400 words)
   The 1812 Massachusetts salamander origin. Why the term endures. Brief international snapshot (U.S. Supreme Court abdication in *Rucho*, U.K. boundary commissions, Australia). One paragraph each. Sets up the Canadian comparison.

7. **Canada is different — and similar** (new, ~500 words)
   How Canada's approach resembles others (single-member districts, FPTP, periodic redistricting) and how it differs (constitutionally-protected independent commissions, the s.3 *effective representation* standard, no "one person one vote" rigidity). Frames why "gerrymander" isn't the legal word here while the concept still applies. This is the bridge to `/law`.

8. **What this audit can and can't tell you** (new, ~300 words)
   Restates the epistemic boundary card now that the reader has context. Concrete examples of valid inference vs. overreach.

9. **How to engage** (new, ~500 words)
   The participation layer. Five concrete enablers, each one sentence to a short paragraph. Written to make action possible, not to direct what the action should be:
   - **Look up your riding** under both maps (postal-code lookup widget; see Postal-code lookup section below).
   - **Find and contact your MLA.** Provide the contact channel and a list of *questions* the reader can ask — not positions to demand. Examples: "Have you read the audit?" "Which structural tests do you find most or least compelling, and why?" "What process would you use to weigh public input against the commission's submission?" The reader assembles the message that reflects their own view.
   - **Attend or watch the next public hearing.** Date, location, livestream link, deadline to register a speaking slot. Sourced from a single maintained JSON file with a "last verified" date visible to the reader.
   - **Submit a written brief.** What the committee accepts, where to send it, the deadline. The site does not template the brief's content — that's the reader's voice.
   - **Share with people you know.** A short link, a one-sentence neutral framing, and a note that personal conversations move opinion more than petition signatures. No script.

10. **Going deeper** (new, ~250 words)
    Signposts to `/law` (for advocates, MLAs, policy staff) and `/methods` (for analysts and scholars). Brief description of what each route offers and why a reader might continue.

All numerical claims get an inline `<Gloss>` popover for jargon and, where relevant, a small "→ see the test" link to `/methods#anchor`.

**Removed from `/`:**
- p-value mechanics, MCMC, ReCom → `/methods`
- Lane 1 / Lane 2 framing in detail → `/methods`
- 4-metric tables → `/methods`
- s.3 Charter / Saskatchewan Reference / Quebec contrast (deep treatment) → `/law` (a one-paragraph version stays on `/`)
- Pre-registration / OSF / falsification conditions → `/methods`
- Data gaps (advance voting, mobile polling) → `/methods`
- Documented anchoring correction → `/methods`
- The committee anomaly (deep treatment) → `/law` (a one-paragraph version stays on `/`)

### `/law` — For advocates, journalists, MLAs, policy staff (target ~2,500 words)

Pulls together everything currently scattered across Section 6 intro, Section 7, and Section 8 (legal portions), and adds the action layer for this audience.

**Sections:**

1. **Why "gerrymander" isn't a legal term in Canada** (~300 words) — the existing Legal Terminology callout (lines 380–383) expanded.
2. **The s.3 test: effective representation** (~500 words) — currently lines 662–669, expanded with context. Quote McLachlin J. from the Saskatchewan Reference. Explain what "effective representation" includes (voter parity, community of interest, geographic features, minority representation, etc.).
3. **The Saskatchewan Reference and what it left open** (~300 words) — when parity may be displaced; the dissent; subsequent jurisprudence.
4. **The Quebec contrast** (~300 words) — existing lines 670–674. Quebec's permanent CRE, the two-thirds override, and the April 22 2026 SCC ruling. Why Alberta's process is structurally different.
5. **The committee anomaly** (~300 words) — existing Section 7's "Why the Committee Is Anomalous." The Lunty committee replacing the commission; default legal effect; how this differs from other provinces.
6. **What this audit can and cannot establish legally** (~200 words) — explicit statement of epistemic limits. The audit produces structural evidence relevant to a s.3 challenge; it does not adjudicate one.
7. **Reform pathways: process** (new, ~350 words) — *Procedural levers that exist within the current statutory framework, and how comparable jurisdictions use them.* The section presents options without endorsing any. Each item names the lever, the jurisdictions that use it, and the tradeoffs an Alberta reader should weigh:
   - **Published response to public submissions.** Some federal commissions publish a structured response to every submission with accept/reject rationale; Alberta's EBCA does not require this. Tradeoff: transparency vs. commissioner workload.
   - **Independent methodological audit before hearings close.** Practice varies. Tradeoff: rigor vs. timeline pressure.
   - **Disclosure of considered-and-rejected alternatives.** Tradeoff: shows the decision space vs. risks producing "kitchen sink" defenses.
   - **Machine-readable publication of chair flags and dissents.** Tradeoff: enables third-party analysis (like this audit) vs. shifts political weight to whoever owns the analysis.
   The reader judges which levers, if any, they would advocate for.
8. **Reform pathways: structural** (new, ~350 words) — *Constitutional and statutory changes other jurisdictions have made. Presented as a comparison table, not a recommendation list.*
   - **Independent permanent commission (Quebec CRE model).** Standing body with constitutional protection. Tradeoff: insulation from political cycle vs. accountability to elected legislatures.
   - **Supermajority override (Quebec ⅔ rule).** Tradeoff: shields against narrow partisan flips vs. risks deadlock.
   - **Constitutionally entrenched default-adopt status.** Tradeoff: closes the procedural gap the Lunty committee exposes vs. removes a check the legislature currently has.
   - **Census-timed redistricting.** Use the next decennial census as the trigger, not the preceding one. Tradeoff: better data vs. longer staleness at end of cycle.
   - **Anchoring thresholds with explicit derogation criteria.** Tradeoff: predictability vs. flexibility for genuinely unique geography.
   The section concludes: "These are the levers that exist. Whether to pull any, and which combination, is a question for the public and the legislature — not for this audit."
9. **Pathways for engagement** (new, ~250 words) — practical channels, neutrally described:
   - The Charter challenge route: who has standing, what evidentiary record is needed, typical timeline. Descriptive, not encouraging.
   - Formal complaint channels at Elections Alberta. What they can and can't address.
   - Private members' motions and the existing legislative committee process. How a citizen contacts a member who sits on relevant committees.
   - Public hearings and brief submission to the Lunty committee (cross-link to `/`'s "How to engage" section).
10. **Legal references** — court cases and statutes from existing Section 10.

Each legal term `<Gloss>`-wrapped: *s.3 Charter*, *effective representation*, *Saskatchewan Reference*, *parity of voting power*, *community of interest*, *EBCA*, *standing*, *Charter challenge*.

### `/methods` — For GIS analysts, statisticians, legal scholars, opposing experts (target ~3,500 words)

The deepest pool — for readers who want to verify or replicate the claim.

**Sections:**

1. **The 1.01M-map ensemble** (~400 words) — currently inside Section 3 and Section 6. What MCMC is, what ReCom does, why we use it, how to read the dot-plot. The existing `lane1_dotplot.svg` figure.
2. **Lane 1 vs. Lane 2** (~300 words) — currently buried in callouts. Explicit framing: Lane 1 is statistical outlier testing; Lane 2 is structural / pre-registered failure tests. Why both matter and why Lane 2 carries the case (the existing `<details>` block at line 641 promoted to a full subsection).
3. **The four statistical measures** (~600 words) — efficiency gap, mean-median, declination, seats@50/50. One subheading each, with the existing 4-metric table.
4. **The targeted-procedure (hill-climbing) test** (~400 words) — existing Section 6 lines 537–600.
5. **The five structural tests** (~400 words) — existing Section 5 content (Lane 2 pre-registered tests), moved verbatim plus the `lane2_bars.svg` figure.
6. **Pre-registration and falsification** (~400 words) — existing Pre-Registration callout (lines 395–398), plus the five falsification conditions from existing Section 9.
7. **Cross-validation** (~150 words) — existing R cross-validation note (lines 592–596).
8. **Data coverage and known gaps** (~400 words) — existing Section 8 (advance voting, mobile polling in Lesser Slave Lake) reframed as methodological limitations rather than narrative.
9. **Documented correction** (~150 words) — existing lines 746–750 (the anchoring retraction).
10. **The verdict, restated with confidence intervals** (~200 words) — the existing verdict quadrant figure and summary table.
11. **Reproducing this audit** (new, ~300 words) — for the professional reader who wants to verify rather than trust:
    - Code repository (GitHub link, structure, how to run end-to-end).
    - Pre-registration record (OSF link, what was registered when).
    - Ensemble outputs (where the 1.01M-map sample lives, how to query it).
    - Raw inputs (shapefiles, 2023 election results, population estimates).
    - Notebooks for the headline figures.
    - How to report a methodological concern (issue tracker link, the standing offer to retract on the five pre-registered conditions).
12. **Academic references** — from existing Section 10.

Each statistical term `<Gloss>`-wrapped: *efficiency gap*, *mean-median gap*, *declination*, *seats@50/50*, *MCMC*, *ReCom*, *ensemble*, *percentile*, *p-value*, *anchoring*, *SZAT*, *Lane 1*, *Lane 2*.

## Postal-code → riding lookup

The "Look up your riding" CTA on `/` is the single most important call-to-action for an undecided reader. It needs to be cheap, fast, free, and respectful of privacy. Canada Post charges for their address data product; we use free Canadian sources instead.

**Two-tier lookup:**

1. **FSA-only (default, instant, offline).** The first three characters of a postal code (the Forward Sortation Area) cover roughly 270 areas in Alberta. We ship a static JSON table `viewer/static/data/fsa_to_ed.json` mapping each Alberta FSA → list of EDs it overlaps (both maps). Typing `T2N` returns "Your FSA is in Calgary-Currie (minority map) / Calgary-Currie (majority map)" instantly with no network call. For most users this resolution is sufficient because most FSAs fall entirely within a single ED.
2. **Full postcode (precise, opt-in, rate-limited).** When the FSA spans multiple EDs (the JSON marks these), the UI offers: "Your FSA overlaps 3 ridings. Enter your full postal code for exact lookup." On opt-in we call OpenStreetMap's Nominatim API (`https://nominatim.openstreetmap.org/search?postalcode=T2N+4M2&country=CA&format=json`), retrieve a lat/lon, then run point-in-polygon against the ED shapefiles we already have. Results cached in `sessionStorage` so the same postcode isn't re-queried in a session.

**Generating the FSA table** (one-time build step):

- Source 1: Statistics Canada's Postal Code Conversion File (PCCF) — free, downloadable, gives postal code → census division → we map census division to ED. Best precision.
- Source 2 (fallback / verification): OSM has FSA boundary polygons under `boundary=postal_code, postal_code=T2N`. We can dissolve these against our ED polygons to produce the overlap table.
- Output: a ~50KB JSON file shipped with the site, no API needed at runtime for the default path.

**Nominatim usage policy compliance:**

- Set `User-Agent: alberta-electoral-boundaries-audit (contact@…)`.
- Cap to 1 request/second client-side via a small queue.
- Cache every result in `sessionStorage` to avoid repeat hits.
- Treat any failure (network, rate limit, ambiguous match) as graceful degradation — fall back to FSA-only message with a "Try again in a moment, or browse the map" CTA.
- For high traffic spikes, consider proxying through the static-site host or upgrading to a self-hosted Nominatim instance. Out of scope for v1.

**Privacy:**

- Postcode is queried only on explicit opt-in click; no auto-submit.
- No postcode is logged to any analytics; the network call goes only to OSM.
- A one-line "Privacy" note next to the input explains this.
- Nothing is stored in `localStorage`; `sessionStorage` clears on tab close.

**Failure modes & UX:**

- Invalid format (non-Canadian postcode): inline error, no network call.
- FSA unknown (e.g. a new FSA not yet in the shipped JSON): "Not in our index — try the full postcode option" plus a link to file an issue.
- Multiple-ED ambiguous FSA without opt-in: list all overlapping EDs with "Most likely yours: X" if the JSON marks a dominant ED.

**Files added:**

| File | Purpose |
|---|---|
| `viewer/static/data/fsa_to_ed.json` | FSA → ED list, both maps. ~50 KB. |
| `viewer/src/lib/PostcodeLookup.svelte` | Input + result UI, called from `/` and (smaller variant) from `/methods` if useful. |
| `viewer/src/lib/postcodeLookup.ts` | Pure logic: parse postcode, FSA table lookup, Nominatim fetch with rate limit + cache. |
| `viewer/scripts/build_fsa_to_ed.py` (or `.js`) | One-time build script using PCCF + shapefiles. Re-run when boundaries change. |

## Shared layout

Create `viewer/src/routes/+layout.svelte` to host:

- **Sticky top nav** with three pills: `Story · Law · Math` (or numeric: `1 Story · 2 Law · 3 Math` to make order obvious). The current route is highlighted. Mobile: same horizontal bar (fits easily — only three items).
- **Site title** and publication date.
- **Footer** with About + GitHub link (existing footer content).

The map stays on `/` only. `/law` and `/methods` are pure prose with figures.

## Glossary component

New file: `viewer/src/lib/Gloss.svelte`

```svelte
<script lang="ts">
  export let term: string;
  export let definition: string;
  export let href: string | undefined = undefined;
  let open = false;
  function toggle() { open = !open; }
  function close() { open = false; }
</script>

<span class="gloss-wrap">
  <button
    type="button"
    class="gloss-trigger"
    aria-expanded={open}
    on:click={toggle}
    on:blur={close}
  >
    <slot>{term}</slot>
  </button>
  {#if open}
    <span class="gloss-pop" role="tooltip">
      <strong class="gloss-term">{term}</strong>
      <span class="gloss-def">{definition}</span>
      {#if href}<a class="gloss-link" href={href}>Learn more →</a>{/if}
    </span>
  {/if}
</span>

<style>
  .gloss-trigger {
    background: none; border: none; padding: 0;
    color: inherit; font: inherit;
    border-bottom: 1px dotted rgba(26,46,69,0.5);
    cursor: help;
  }
  .gloss-trigger[aria-expanded="true"] { background: rgba(26,46,69,0.05); }
  .gloss-wrap { position: relative; display: inline; }
  .gloss-pop {
    position: absolute; top: 1.4em; left: 0; z-index: 10;
    width: min(280px, 80vw);
    background: #fff;
    border: 1px solid rgba(26,46,69,0.18);
    border-radius: 6px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    padding: 0.65rem 0.85rem;
    font-size: 0.85rem; line-height: 1.4;
    display: block;
  }
  .gloss-term  { display: block; font-weight: 600; margin-bottom: 0.25rem; }
  .gloss-def   { display: block; color: #333; }
  .gloss-link  { display: inline-block; margin-top: 0.4rem; font-size: 0.8rem; }
</style>
```

Single source of truth: `viewer/src/lib/glossary.ts`

```ts
export const GLOSS = {
  efficiencyGap: {
    term: 'Efficiency gap',
    definition: 'Wasted votes (those over 50% in a win, or all votes in a loss) ' +
                'as a share of total votes, expressed as the gap between the two parties. ' +
                'A gap above ~7% is academic shorthand for a partisan map.',
    href: '/methods#efficiency-gap',
  },
  meanMedian: {
    term: 'Mean-median gap',
    definition: 'The difference between a party\'s mean vote share across districts ' +
                'and its median. A large gap suggests the party\'s voters are arranged ' +
                'in a way that wastes their votes.',
    href: '/methods#mean-median',
  },
  // ... declination, seatsFiftyFifty, ReCom, MCMC, ensemble, percentile,
  //     anchoring, Lane1, Lane2, SZAT, charterSection3, effectiveRepresentation,
  //     saskatchewanReference, EBCA
};
```

Usage anywhere in markup:

```svelte
<script>
  import Gloss from '$lib/Gloss.svelte';
  import { GLOSS } from '$lib/glossary';
</script>

The minority map's <Gloss {...GLOSS.efficiencyGap}>efficiency gap</Gloss>
sits at the 99.99th percentile…
```

This keeps definitions consistent across all three routes and avoids the current pattern of redefining terms each time they appear.

## Accessibility

- `<Gloss>` button uses `aria-expanded`; the popover uses `role="tooltip"`.
- Keyboard: Tab focuses the trigger, Enter/Space opens, blur closes. Escape closes (added globally on the layout). Tab through to next focusable element.
- Screen readers: trigger reads the term; popover content is then read via the role.
- Color contrast: dotted underline is the only visual affordance; pair with `cursor: help` for sighted users. The dotted underline meets WCAG AA at the chosen opacity.
- The popover renders absolutely positioned but in normal document flow — no portal — so reading order is preserved.

## URL preservation

External links currently point to `/` and to anchors like `/#section-3`. Migration risks:

1. **Anchors in the wild** (e.g., the `lunty_dry_run` reports may link to specific section IDs).
   - Mitigation: keep the existing section IDs on whichever route the content lands on. Add a small `/`-resident anchor-redirect script that catches old hashes like `#methods-1010000-test` and pushes to `/methods#1010000-test`.
2. **The verdict** stays on `/` (in the hero block), so external "is this a gerrymander" links still land on the answer.
3. **Cover map** stays on `/` — no change for users following social-share previews.

## Migration approach (mechanical, low-risk)

1. **Phase 0 — Component plumbing.** Create `Gloss.svelte`, `glossary.ts`, and `+layout.svelte` with sticky nav. Don't move any content yet. Verify the nav renders on the existing single-page site (it just sits above the current page).
2. **Phase 1 — Create empty `/law` and `/methods` routes** with placeholder copy and section anchors. Nav links work, both routes are reachable.
3. **Phase 2 — Move content section-by-section.** For each existing section in `+page.svelte`:
   - Decide its destination route (per the route plan above).
   - Cut from `+page.svelte`, paste into destination, wrap jargon in `<Gloss>`.
   - Keep the section's `id="…"` attribute identical to preserve external anchors.
   - Add a "→ deeper reading" link on `/` to the destination anchor.
4. **Phase 3 — Write the hero verdict + epistemic boundary cards** on `/`. These are the only genuinely new prose.
5. **Phase 4 — Consolidate the "outcomes, not intent" caveat** to exactly two places: the epistemic boundary card on `/` and one statement on `/law`. Delete the four duplicates currently scattered through Section 6.
6. **Phase 5 — Style pass and copy-edit pass.** Read each route cold; tighten transitions.

Each phase is a separable commit. The site is shippable at every step (Phase 0 only adds a nav; Phases 1-2 progressively move content).

## Performance / build

- SvelteKit splits per-route automatically; the map's `mapEngine.ts` (~1,200 lines) loads only on `/`. `/law` and `/methods` are lean.
- Glossary popovers are local Svelte state — no portal, no shared store — so they're cheap.
- Static export should continue to work (current `viewer/svelte.config.js` adapter unchanged).

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Readers don't follow `/law` and `/methods` links | Sticky three-route nav makes alternates visible at all times; inline "→ see the math" pills on every claim that touches stats; verdict block on `/` ends with two prominent CTA buttons. |
| Argument feels fragmented across pages | Each route is internally self-contained and signposts to the others. The verdict on `/` is the spine; everything else is the skeleton. |
| External links break | Preserve section IDs; add hash-redirect script for legacy anchors. |
| Glossary popovers feel intrusive if used too liberally | Cap to ~6-8 terms per route. Definitions are short (2-3 sentences) and the trigger is a subtle dotted underline, not a button. |
| Mobile popover positioning conflicts with viewport edges | Popover uses `width: min(280px, 80vw)` and `left: 0`; if a term is in the right margin, the popover may clip. Add a follow-up: detect bounding box and flip to `right: 0` if needed. Acceptable for v1. |
| Authorial voice gets lost in restructuring | This is a content migration, not a rewrite. Existing prose moves intact; only the *order* and *page* change. New prose is restricted to the verdict block, the epistemic boundary card, and section transitions. |
| Three pages = three SEO surfaces | Each route gets its own `<svelte:head>` title and meta description. Open Graph tags on `/` continue to drive social shares to the verdict. |

## Out of scope (future passes)

- Persistent right-rail glossary (rejected at decision time).
- Print/PDF view of the combined three pages.
- Multilingual (French) version.
- Reader-progress indicator across the three routes.
- Interactive Lane 1 / Lane 2 calculator on `/methods`.
- Sample-letter generator for MLA outreach. (Deliberately excluded — runs counter to the empower-don't-advocate principle. Reader writes their own.)
- Petition or signature-gathering integration. (Same reason.)
- Multi-language translation.

## Resolved follow-ups

- **Postal-code lookup:** in scope. FSA-only via static JSON by default; OSM Nominatim for full postcode on opt-in. See Postal-code lookup section above.
- **Advocacy vs. empowerment:** resolved. Editorial principle established at the top of this proposal. `/law` "Recommendations" sections rewritten as neutral "Reform pathways" presenting options other jurisdictions use, with tradeoffs, no endorsement. `/` "What you can do" rewritten as "How to engage" — provides channels and question prompts, not positions to advocate.

## Open questions (still to resolve before implementation)

1. **History-of-gerrymandering depth.** The proposal allots ~400 words. Could expand to its own subroute (`/history`). Recommend keeping it on `/` and brief — readers don't need *Rucho* in detail, they need to know the word has a 200-year pedigree and is used internationally for a reason.
2. **Hearing-date freshness.** The "Attend a public hearing" enabler depends on dates that age. Plan: a single `viewer/static/data/engagement.json` file with the hearing schedule, brief-submission deadline, and a `last_verified` timestamp visible to the reader ("Verified 2026-05-23 — check Elections Alberta for the latest"). Confirms the data has a maintenance cost; needs an owner.
3. **PCCF licensing.** Statistics Canada's PCCF is free but has terms of use (attribution, no resale). Need a one-line license check before bundling it in the build script. OSM FSA polygons (ODbL) require attribution in the site footer; confirm the existing footer accommodates this.
4. **Multi-language reach.** Alberta has substantial French and Indigenous-language speaking populations. Out of scope here but flag for an editorial roadmap.

## Files touched

| File | Change |
|---|---|
| `viewer/src/routes/+layout.svelte` | **New.** Sticky three-route nav, shared header/footer, global Escape-closes-popovers handler. |
| `viewer/src/routes/+page.svelte` | **Major.** Strip to narrative-only content; add hero verdict block + epistemic boundary card; keep map. |
| `viewer/src/routes/law/+page.svelte` | **New.** Pulls existing legal content from current Sections 6 intro, 7, 8 (legal parts). |
| `viewer/src/routes/methods/+page.svelte` | **New.** Pulls existing methodology content from current Sections 3, 5, 6, 8 (methods parts), 9. |
| `viewer/src/lib/Gloss.svelte` | **New.** Reusable click-to-define popover. |
| `viewer/src/lib/glossary.ts` | **New.** Single source of truth for ~15 defined terms. |
| `viewer/src/lib/PostcodeLookup.svelte` | **New.** Postal-code → riding UI; FSA-first, Nominatim opt-in. |
| `viewer/src/lib/postcodeLookup.ts` | **New.** Pure logic (parse, FSA table, rate-limited fetch, cache). |
| `viewer/static/data/fsa_to_ed.json` | **New.** FSA → ED list, both maps. ~50 KB. |
| `viewer/static/data/engagement.json` | **New.** Hearing dates, brief deadline, `last_verified` timestamp. |
| `viewer/scripts/build_fsa_to_ed.py` | **New.** One-time build from PCCF + shapefiles. |
| `viewer/src/routes/+page.svelte` (script tag) | Add hash-redirect for legacy anchors. |

## Acceptance criteria

- A casual reader reaching `/` sees the verdict in the first viewport on desktop.
- The three-route nav is visible on every route, and the active route is clearly indicated.
- Every statistical term that appears in narrative copy has a `<Gloss>` wrapper with a working popover.
- No technical methodology (MCMC, ReCom, p-values, ensemble percentiles, declination, mean-median, hill-climbing) appears in the body text of `/`.
- No statistical methodology repeats across `/` and `/methods` — each definition lives in `glossary.ts`; the methods page has the long-form explanation.
- The "outcomes, not intent" caveat appears in exactly two places (epistemic boundary card on `/`, one paragraph on `/law`), not four+ as today.
- The cover map and existing anomaly/ED triggers continue to function on `/`.
- All existing external links to anchored sections still land at the correct content (via preserved IDs or hash redirect).
- Word-count distribution roughly matches: `/` ~4,500, `/law` ~2,500, `/methods` ~3,500 (up from one ~8,400-word scroll, but distributed across three audience-tiered routes so each is shorter than today's monolith).
- A reader with no prior knowledge of redistricting can read only `/` and come away knowing what was decided, what's at stake for them, and one thing they can do.
- A reader with a policy or legal background can read `/` + `/law` and come away with both the popular and the doctrinal framing, plus a neutral comparison of reform pathways used in other jurisdictions.
- No section of the site tells a reader which map to support, what position to advocate, or what reform Alberta should adopt. Channels and choices are provided; conclusions are the reader's.
- The postal-code lookup returns a riding name within 100ms for the FSA path and within 2s for the full-postcode path; gracefully degrades on Nominatim failure.
- A reader with a statistical or GIS background can read `/methods` directly and either reproduce or critique the analysis using the materials linked there.
