# Website Rewrite — Plan 1: Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the structural plumbing for the three-route rewrite — an i18n-aware glossary, a `Gloss` popover component, a shared three-route nav, and empty `/law` and `/methods` routes — without moving any prose yet. The site stays live and English-complete throughout.

**Architecture:** SvelteKit 2 / Svelte 5 (runes) static site under `viewer/`. Translation flows through `t(lang, keyPath)` (dotted lookup with English fallback). The glossary follows the same path: term definitions live in each locale's `glossary` section so popovers translate; a pure-logic accessor (`glossary.ts`) resolves them and is unit-tested with vitest. UI components are Svelte 5 and verified with `svelte-check` + `vite build` (the harness's vitest runs in a node env against pure `.ts` only, so components are not unit-tested).

**Tech Stack:** SvelteKit 2.57, Svelte 5.55 (runes: `$props`, `$state`, `$derived`), TypeScript, vitest (node env), svelte-check, `$app/state` for the active route.

**Scope:** This is Plan 1 of a phased rewrite (spec: `proposals/website_rewrite/design.md`). It implements spec §9 phases 1–2 (plumbing + empty routes) and §7 (components). It does NOT rewrite prose — that is Plan 2 (`/` Story), Plan 3 (`/law`), Plan 4 (`/methods`), Plan 5 (re-translation). Each lands as its own plan after Foundation.

**Commit discipline (per user request):** every task is one self-contained, clearly-labelled commit so any step can be rolled back independently. All commit subjects are prefixed `…(website-foundation):`.

**Working directory for all commands:** `C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit/viewer` unless noted. Git commands run from the repo root `…/alberta_audit`.

---

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `viewer/src/lib/i18n/locales/en.ts` | English source of truth; gains a `glossary` section + three `nav.route_*` keys | Modify |
| `viewer/src/lib/i18n/glossary.ts` | Pure-logic accessor: list of term keys + `gloss(lang, key)` → `{term, definition, href?}` | Create |
| `viewer/tests/glossary.test.ts` | Unit tests for `gloss()` (resolution, English fallback, loud-missing) | Create |
| `viewer/src/lib/components/Gloss.svelte` | Click-to-define popover; Svelte 5; RTL-safe; reads active lang + glossary | Create |
| `viewer/src/routes/+layout.svelte` | Gains a shared sticky three-route nav (Story · Law · Methods) | Modify |
| `viewer/src/routes/law/+page.svelte` | Empty `/law` scaffold with section anchors + placeholder string | Create |
| `viewer/src/routes/methods/+page.svelte` | Empty `/methods` scaffold with section anchors + placeholder string | Create |

---

## Task 1: i18n-aware glossary accessor (TDD)

**Files:**
- Modify: `viewer/src/lib/i18n/locales/en.ts` (add a `glossary` section)
- Create: `viewer/src/lib/i18n/glossary.ts`
- Create: `viewer/tests/glossary.test.ts`

- [ ] **Step 1: Add the `glossary` section to `en.ts`**

Open `viewer/src/lib/i18n/locales/en.ts`. The file is one big `export default { … }` object with top-level sections (`selector`, `disclaimer`, `nav`, …). Add a new top-level `glossary` section. Insert it immediately after the `selector: { … },` block (near the top, so it's easy to find). Use this exact content (plain, grade-11, reflecting the corrected findings — `proposals/website_rewrite/design.md` §5):

```ts
	glossary: {
		gerrymander: {
			term: 'Gerrymander',
			definition:
				'An American nickname for an electoral map drawn to favour one party. It has no legal meaning in Canada — no court or law uses it — so this site never uses it as a verdict.'
		},
		ensemble: {
			term: 'The 1.01-million-map test',
			definition:
				'A computer drew 1.01 million legal Alberta maps at random, all following the same rules. A real map counts as unusual when it falls outside what almost all of these neutral maps produce.'
		},
		efficiency_gap: {
			term: 'Efficiency gap',
			definition:
				'A measure of "wasted" votes — votes beyond what a candidate needed to win, plus every vote for a loser — compared between the two parties. A large gap points to a one-sided map.'
		},
		mean_median: {
			term: 'Mean-median gap',
			definition:
				'The gap between a party\'s average vote share across districts and its middle (median) one. A large gap suggests its voters are spread in a way that wastes votes.'
		},
		declination: {
			term: 'Declination',
			definition:
				'A measure of how lopsidedly each party wins its seats — by blowouts or by squeakers. On the minority map it points the same way as the other measures (toward the governing party) after a June 2026 sign correction.'
		},
		seats_5050: {
			term: 'Seats at a tie',
			definition:
				'How many seats each party would win if the province split its vote exactly 50-50. It strips out who actually won and tests the map\'s built-in tilt.'
		},
		effective_representation: {
			term: 'Effective representation',
			definition:
				'The standard Canadian courts use under section 3 of the Charter: boundaries must give voters a real, fair voice — not perfectly equal districts, but representation that genuinely works.'
		},
		ebca: {
			term: 'EBCA',
			definition:
				'The Electoral Boundaries Commission Act — the Alberta law that sets the rules a new map must follow, including how far district populations may vary.'
		}
	},
```

- [ ] **Step 2: Write the failing test**

Create `viewer/tests/glossary.test.ts`:

```ts
// Tests for src/lib/i18n/glossary.ts — the i18n-aware glossary accessor.
// Properties that matter:
//   1. A known key in English resolves to a non-empty term + definition.
//   2. Entries that should link out carry an href.
//   3. A locale without its own glossary falls back to the English definition
//      (never a loud [missing:…] token), because only en.ts has glossary copy in Plan 1.
import { describe, it, expect } from 'vitest';
import { gloss, GLOSS_KEYS } from '../src/lib/i18n/glossary';

describe('gloss() — i18n-aware glossary', () => {
	it('resolves every declared key to a non-empty term and definition in English', () => {
		for (const key of GLOSS_KEYS) {
			const e = gloss('en', key);
			expect(e.term, key).toBeTruthy();
			expect(e.definition, key).toBeTruthy();
			expect(e.term).not.toMatch(/^\[missing:/);
			expect(e.definition).not.toMatch(/^\[missing:/);
		}
	});

	it('attaches an href for terms that have a deep-dive anchor', () => {
		expect(gloss('en', 'efficiency_gap').href).toBe('/methods#efficiency-gap');
		expect(gloss('en', 'gerrymander').href).toBe('/law#why-not-gerrymander');
	});

	it('falls back to the English definition for a locale that has no glossary yet', () => {
		const en = gloss('en', 'gerrymander').definition;
		const fr = gloss('fr', 'gerrymander').definition;
		expect(fr).toBe(en);
		expect(fr).not.toMatch(/^\[missing:/);
	});
});
```

- [ ] **Step 3: Run the test to verify it fails**

Run (from `viewer/`): `npm test -- glossary`
Expected: FAIL — `Cannot find module '../src/lib/i18n/glossary'` (the module doesn't exist yet).

- [ ] **Step 4: Implement `glossary.ts`**

Create `viewer/src/lib/i18n/glossary.ts`:

```ts
// i18n-aware glossary. The specialist terms that get click-to-define popovers.
// Definitions live in each locale's `glossary` section (so they translate);
// this module lists the keys, owns the deep-dive hrefs, and resolves an entry
// through the same English-fallback path as all other UI strings.
import { t } from './dict';
import type { Lang } from './store.svelte';

export const GLOSS_KEYS = [
	'gerrymander',
	'ensemble',
	'efficiency_gap',
	'mean_median',
	'declination',
	'seats_5050',
	'effective_representation',
	'ebca'
] as const;

export type GlossKey = (typeof GLOSS_KEYS)[number];

export interface GlossEntry {
	term: string;
	definition: string;
	href?: string;
}

// Where each term's long-form explanation lives, once Plans 3–4 fill those routes.
const HREFS: Partial<Record<GlossKey, string>> = {
	gerrymander: '/law#why-not-gerrymander',
	effective_representation: '/law#effective-representation',
	ebca: '/law#ebca',
	ensemble: '/methods#ensemble',
	efficiency_gap: '/methods#efficiency-gap',
	mean_median: '/methods#mean-median',
	declination: '/methods#declination',
	seats_5050: '/methods#seats-50-50'
};

export function gloss(lang: Lang, key: GlossKey): GlossEntry {
	return {
		term: t(lang, `glossary.${key}.term`),
		definition: t(lang, `glossary.${key}.definition`),
		href: HREFS[key]
	};
}
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `npm test -- glossary`
Expected: PASS (3 passing).

- [ ] **Step 6: Type-check**

Run: `npm run check`
Expected: completes with 0 errors (warnings about other files are acceptable; there must be no new error in `glossary.ts` or `en.ts`).

- [ ] **Step 7: Commit**

```bash
cd "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
git add viewer/src/lib/i18n/glossary.ts viewer/tests/glossary.test.ts viewer/src/lib/i18n/locales/en.ts
git commit -m "feat(website-foundation): i18n-aware glossary accessor + English term definitions

Adds src/lib/i18n/glossary.ts (gloss(lang,key) resolving localized term+definition
via the existing English-fallback path) plus the en.ts glossary section with 8 terms
written to the corrected findings. Unit-tested in tests/glossary.test.ts. No prose moved."
```

---

## Task 2: `Gloss` popover component

**Files:**
- Create: `viewer/src/lib/components/Gloss.svelte`

Svelte 5 runes. The component is verified by `svelte-check` + `vite build` (no component unit test under the node-env vitest harness).

- [ ] **Step 1: Create the component**

Create `viewer/src/lib/components/Gloss.svelte`:

```svelte
<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { gloss, type GlossKey } from '$lib/i18n/glossary';
	import type { Snippet } from 'svelte';

	let { key, children }: { key: GlossKey; children?: Snippet } = $props();

	let open = $state(false);
	const entry = $derived(gloss(lang.current, key));
</script>

<span class="gloss-wrap">
	<button
		type="button"
		class="gloss-trigger"
		aria-expanded={open}
		onclick={() => (open = !open)}
		onblur={() => (open = false)}
	>{#if children}{@render children()}{:else}{entry.term}{/if}</button>
	{#if open}
		<span class="gloss-pop" role="tooltip">
			<strong class="gloss-term">{entry.term}</strong>
			<span class="gloss-def">{entry.definition}</span>
			{#if entry.href}<a class="gloss-link" href={entry.href}>Learn more →</a>{/if}
		</span>
	{/if}
</span>

<style>
	.gloss-wrap { position: relative; display: inline; }
	.gloss-trigger {
		background: none; border: 0; padding: 0;
		color: inherit; font: inherit;
		border-bottom: 1px dotted rgba(43, 91, 161, 0.7);
		cursor: help;
	}
	.gloss-trigger[aria-expanded='true'] { background: rgba(43, 91, 161, 0.08); }
	.gloss-pop {
		position: absolute; top: 1.5em; inset-inline-start: 0; z-index: 60;
		width: min(300px, 84vw);
		background: var(--bg-alt, var(--bg, #fff));
		color: var(--text, inherit);
		border: 1px solid rgba(127, 127, 127, 0.3);
		border-radius: 6px;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.14);
		padding: 0.65rem 0.85rem;
		font-size: 0.85rem; line-height: 1.45;
		display: block; text-align: start;
	}
	.gloss-term { display: block; font-weight: 600; margin-bottom: 0.25rem; }
	.gloss-def { display: block; }
	.gloss-link { display: inline-block; margin-top: 0.4rem; font-size: 0.8rem; }
</style>
```

(Note the RTL-safe logical properties — `inset-inline-start`, `text-align: start` — consistent with this session's RTL pass.)

- [ ] **Step 2: Type-check**

Run: `npm run check`
Expected: 0 errors. If `Snippet` import errors, confirm svelte version exposes it (Svelte 5 does); do not downgrade to `<slot>`.

- [ ] **Step 3: Build to confirm it compiles in context**

Run: `npm run build`
Expected: `✓ built` and `Merged build/ → docs/` (exit 0).

- [ ] **Step 4: Commit**

```bash
cd "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
git add viewer/src/lib/components/Gloss.svelte
git commit -m "feat(website-foundation): Gloss click-to-define popover (Svelte 5, RTL-safe)

Reusable <Gloss key=\"...\"> popover that pulls the localized term+definition from
the glossary accessor and links to its deep-dive anchor. No callers wired yet."
```

---

## Task 3: Shared three-route nav in the layout

**Files:**
- Modify: `viewer/src/lib/i18n/locales/en.ts` (add `nav.route_story|route_law|route_methods`)
- Modify: `viewer/src/routes/+layout.svelte`

- [ ] **Step 1: Add the three nav-label keys to `en.ts`**

In `viewer/src/lib/i18n/locales/en.ts`, inside the existing `nav: { … }` section, add these three keys (place them right after `drawer_top: '↑ Top',`):

```ts
		route_story: 'Story',
		route_law: 'Law',
		route_methods: 'Methods',
```

- [ ] **Step 2: Add the sticky route-nav to `+layout.svelte`**

Open `viewer/src/routes/+layout.svelte`. It currently imports `lang, LANG_LABELS`, renders `<TranslationDisclaimer />` then `{@render children()}`. Add the active-route source and a nav bar.

In the `<script lang="ts">` block, add these imports near the existing ones:

```ts
	import { page } from '$app/state';
	import { t } from '$lib/i18n/dict';
```

Then, in the markup, immediately BEFORE `<TranslationDisclaimer />`, insert:

```svelte
<nav class="route-nav" aria-label="Site sections">
	<a class="route-pill" class:active={page.url.pathname === '/'} href="/">{t(lang.current, 'nav.route_story')}</a>
	<a class="route-pill" class:active={page.url.pathname.startsWith('/law')} href="/law">{t(lang.current, 'nav.route_law')}</a>
	<a class="route-pill" class:active={page.url.pathname.startsWith('/methods')} href="/methods">{t(lang.current, 'nav.route_methods')}</a>
</nav>
```

And add a `<style>` block at the end of the file (create one if absent):

```svelte
<style>
	.route-nav {
		position: sticky; top: 0; z-index: 70;
		display: flex; gap: 0.4rem; justify-content: center;
		padding: 0.4rem 0.6rem;
		background: var(--bg, #fff);
		border-bottom: 1px solid rgba(127, 127, 127, 0.18);
	}
	.route-pill {
		font-size: 0.85rem; font-weight: 600;
		padding: 0.25rem 0.85rem; border-radius: 999px;
		text-decoration: none; color: var(--text-muted, #555);
		border: 1px solid transparent;
	}
	.route-pill:hover { color: var(--text, #111); }
	.route-pill.active {
		color: var(--text, #111);
		border-color: rgba(127, 127, 127, 0.4);
		background: rgba(127, 127, 127, 0.08);
	}
</style>
```

- [ ] **Step 3: Type-check + build**

Run: `npm run check && npm run build`
Expected: 0 errors; `✓ built`. If `$app/state` is not found, the SvelteKit version is < 2.12 — it is 2.57, so it must resolve; do not substitute `$app/stores` unless `check` proves `$app/state` missing.

- [ ] **Step 4: Manual smoke check**

Run: `npm run preview` and open the printed URL. Confirm: the three pills render at the top of `/`; "Story" is highlighted; clicking "Law"/"Methods" navigates (they 404 until Task 4 — that's expected this step). Stop the preview server (Ctrl-C) when done.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
git add viewer/src/routes/+layout.svelte viewer/src/lib/i18n/locales/en.ts
git commit -m "feat(website-foundation): shared sticky three-route nav (Story/Law/Methods)

Adds a route-level nav to +layout.svelte using \$app/state for active-route
highlighting and i18n nav.route_* labels. /law and /methods 404 until the next task."
```

---

## Task 4: Empty `/law` and `/methods` route scaffolds

**Files:**
- Create: `viewer/src/routes/law/+page.svelte`
- Create: `viewer/src/routes/methods/+page.svelte`

These are intentionally minimal — they make the nav targets real and reserve the section anchors the glossary hrefs point at. Prose arrives in Plans 3–4.

- [ ] **Step 1: Create `/law` scaffold**

Create `viewer/src/routes/law/+page.svelte`:

```svelte
<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<svelte:head><title>Law — Alberta Electoral Boundary Audit</title></svelte:head>

<main class="route-stub container">
	<h1>{t(lang.current, 'nav.route_law')}</h1>
	<p class="stub-note">This section is being written. It will cover what the law asks of an electoral map and how this audit relates to it.</p>
	<section id="why-not-gerrymander"></section>
	<section id="effective-representation"></section>
	<section id="ebca"></section>
</main>

<style>
	.route-stub { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
	.stub-note { color: var(--text-muted, #666); font-style: italic; }
</style>
```

- [ ] **Step 2: Create `/methods` scaffold**

Create `viewer/src/routes/methods/+page.svelte`:

```svelte
<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<svelte:head><title>Methods — Alberta Electoral Boundary Audit</title></svelte:head>

<main class="route-stub container">
	<h1>{t(lang.current, 'nav.route_methods')}</h1>
	<p class="stub-note">This section is being written. It will explain how the maps were tested and how to reproduce the result.</p>
	<section id="ensemble"></section>
	<section id="efficiency-gap"></section>
	<section id="mean-median"></section>
	<section id="declination"></section>
	<section id="seats-50-50"></section>
</main>

<style>
	.route-stub { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
	.stub-note { color: var(--text-muted, #666); font-style: italic; }
</style>
```

- [ ] **Step 3: Build + verify routes resolve**

Run: `npm run build`
Expected: `✓ built`; the build output lists `/law` and `/methods` as prerendered pages (adapter-static). Then:
```bash
ls build/law/index.html build/methods/index.html
```
Expected: both files exist.

- [ ] **Step 4: Manual smoke check**

Run: `npm run preview`, open the URL, click "Law" and "Methods" in the nav. Confirm each loads its stub heading, the active pill updates, and the glossary anchors exist (e.g., open `/methods#efficiency-gap` directly — no 404). Stop the server when done.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
git add viewer/src/routes/law/+page.svelte viewer/src/routes/methods/+page.svelte
git commit -m "feat(website-foundation): empty /law and /methods route scaffolds

Minimal pages so the three-route nav targets resolve and the glossary deep-dive
anchors (#efficiency-gap, #why-not-gerrymander, etc.) exist. Prose lands in Plans 3-4."
```

---

## Task 5: Wire one `Gloss` into `/` as an end-to-end smoke test

**Files:**
- Modify: `viewer/src/routes/+page.svelte` (one existing mention of a term → wrap in `<Gloss>`)

This proves the whole chain (component → accessor → i18n → href → route anchor) works in the real page, before Plan 2 wires many. Pick the existing "efficiency gap" mention in the litmus table area.

- [ ] **Step 1: Import `Gloss` in `+page.svelte`**

In `viewer/src/routes/+page.svelte`'s `<script>` block, add:

```ts
	import Gloss from '$lib/components/Gloss.svelte';
```

- [ ] **Step 2: Wrap one term**

Find a single, literal English occurrence of the phrase "efficiency gap" in the page body markup (not inside a `t()` key — pick a hardcoded one if present, otherwise add the Gloss to a visible label). Replace that occurrence with:

```svelte
<Gloss key="efficiency_gap">efficiency gap</Gloss>
```

If every occurrence is inside a `t()` string (so there is no literal to wrap), instead add a single demonstrator line just below the litmus table's `table_intro` paragraph:

```svelte
<p style="font-size:0.85rem;color:var(--text-muted)">New term help, for example: <Gloss key="efficiency_gap">efficiency gap</Gloss> — click it.</p>
```

- [ ] **Step 3: Build + check**

Run: `npm run check && npm run build`
Expected: 0 errors; `✓ built`.

- [ ] **Step 4: Manual smoke check**

Run: `npm run preview`. On `/`, click the dotted "efficiency gap" — the popover shows the term, the definition, and a "Learn more →" link to `/methods#efficiency-gap`. Click the link; it lands on the methods page at that anchor. Switch language to Arabic (RTL) and re-open the popover; confirm it doesn't clip off the wrong edge. Stop the server.

- [ ] **Step 5: Commit**

```bash
cd "C:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
git add viewer/src/routes/+page.svelte
git commit -m "feat(website-foundation): wire one Gloss into / as end-to-end smoke test

Proves component → glossary accessor → i18n fallback → deep-dive href → route anchor
works in the live page. Plan 2 wires the rest of the terms during the / rewrite."
```

---

## Self-Review

1. **Spec coverage (vs `design.md`):** §7 components → Tasks 1–2 (glossary, Gloss); §6 nav → Task 3; §6.2/§6.3 routes → Task 4; §8 i18n-aware glossary → Task 1 (definitions in locale files, accessor uses `t()` fallback). Prose rewrite (§6.1 spine, §6.2/§6.3 content), the outcomes-not-intent consolidation (§3), riding lookup + engagement JSON (§7), and re-translation (§8) are explicitly deferred to Plans 2–5 — not gaps, scope boundaries stated in the header.
2. **Placeholder scan:** No "TBD"/"handle edge cases". Task 5 Step 2 has a stated conditional (wrap an existing literal, else add a demonstrator line) with both branches given in full — not a placeholder.
3. **Type/name consistency:** `GlossKey`, `GLOSS_KEYS`, `gloss()`, `GlossEntry` are defined in Task 1 and used identically in Tasks 2 and 5. The glossary keys (`efficiency_gap`, `gerrymander`, …) match the `en.ts` section keys (Task 1 Step 1) and the route anchor ids (Task 4) the hrefs point to (`/methods#efficiency-gap` ↔ `<section id="efficiency-gap">`). `nav.route_story|route_law|route_methods` defined in Task 3 Step 1, used in Tasks 3–4.
4. **Reality check:** all commands are the project's real scripts (`npm test`, `npm run check`, `npm run build`, `npm run preview`); vitest targets `tests/**/*.test.ts` (node env) so only the pure-logic accessor is unit-tested, components use check+build+preview — matching the harness.
