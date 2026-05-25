---
name: Homepage i18n — English + French + Tagalog + Punjabi + Simplified & Traditional Chinese
description: "AUTHORIZED 2026-05-24. Adds a language selector to / supporting English, Canadian French (fr-CA), Tagalog (tl), Punjabi (pa, Gurmukhi), Simplified Chinese (zh-Hans, for Mandarin speakers), and Traditional Chinese (zh-Hant, for Cantonese / Hong Kong readership). Every non-English locale carries an explicit AI-translation disclaimer inviting the reader to report errors or volunteer to translate. Detection: URL ?lang= -> localStorage -> navigator.languages -> default 'en'. Implementation lives in viewer/src/lib/i18n/ and viewer/src/lib/components/. This document is the design source of truth; the actual code is the implementation."
type: methodology
---

> **Backward:**
> - `proposals/verdict_and_glossary_draft.md` — the source-of-truth English content this plan translates
> - `proposals/content_restructure.md` — the audience-tier architecture this plan inherits
> - `viewer/svelte.config.js` — adapter-static configuration (query-param i18n is what fits)
>
> **Forward:**
> - `viewer/src/lib/i18n/` — the live implementation (store, dictionary, per-locale files)
> - `viewer/src/lib/components/LanguageSelector.svelte` — the selector UI
> - `viewer/src/lib/components/TranslationDisclaimer.svelte` — the AI-translation banner shown on non-English locales
> - `viewer/src/routes/+layout.svelte` — mounts the selector + disclaimer, sets `<html lang>`, emits `hreflang`

# Homepage i18n — six locales with AI-translation disclaimer

**Status as of 2026-05-24: AUTHORIZED.** PI authorized the architecture and the six-locale scope; this document is now the design record. The live implementation is in `viewer/src/lib/i18n/` and `viewer/src/lib/components/`. Translation quality is honestly disclosed — every non-English page shows an AI-translation banner inviting the reader to report errors or volunteer to translate.

## Why these six locales

Statistics Canada 2021 Census, Alberta:

| Locale | Language | Reach | Notes |
|---|---|---|---|
| `en` | English | 76% mother tongue | Source of truth |
| `fr` | Canadian French | 1.5%, plus federal official-language conventions | Communities in NE Alberta (St. Paul, Bonnyville, Plamondon, Falher) + Edmonton |
| `tl` | Tagalog | 2.5%, fastest-growing | Calgary, Edmonton |
| `pa` | Punjabi (Gurmukhi) | 2.2% | Calgary, Edmonton |
| `zh-Hans` | Simplified Chinese | Mandarin speakers, ~1.7% | Mainland-China-origin readers |
| `zh-Hant` | Traditional Chinese | Cantonese speakers, ~1.3% | Hong-Kong-origin readers; same standard written Chinese, Traditional script |

Combined Chinese (Mandarin + Cantonese) is ~3% — outranks both Tagalog and Punjabi by raw speaker count. Splitting into `zh-Hans` and `zh-Hant` lets Mandarin and Cantonese readers each see their conventional script. Standard written Chinese (the formal civic-document register) is largely identical between the two; only the character set differs. Colloquial written Cantonese (粵文) is not used for formal civic text and is not the target here.

Indigenous-language reach (Cree, Blackfoot, Dene, Stoney Nakoda) remains a separate engagement that must work with the Treaty 6 / 7 / 8 nations' language authorities — not a top-down AI translation.

## The AI-translation disclaimer

Every non-English locale renders a banner at the top of the page, in that locale, with the following structure:

> This site has been translated by AI. Some content may still appear in English while translations are in progress. If you notice errors or would like to help translate this project, please contact us.

The banner:

- Is honest about machine translation (no pretending a human translator vetted it).
- Acknowledges the partial-translation state — some pages or sections may still be English until the dictionary covers them.
- Invites the community in. The volunteer call is the most important part: native speakers reading their language on a civic-document site are the right reviewers, and the volunteer call gives them an explicit lane to participate.
- Links to `#contact` (the existing site's contact anchor) so the reach-out path is one click away.

The disclaimer does **not** appear on the English page, because the English content is the source of truth and is not AI-translated. The selector remains visible on every locale so a reader who landed on English by accident can switch.

## Architecture (committed)

### Detection priority (highest → lowest wins)

1. URL `?lang=` parameter
2. `localStorage.audit_lang` (saved choice)
3. `navigator.languages` match against the supported set (prefix match: `fr-CA` matches `fr`; `zh-CN` matches `zh-Hans`; `zh-HK`/`zh-TW` match `zh-Hant`)
4. Default: `en`

### URL strategy

Query parameter `?lang=fr` (or `tl`, `pa`, `zh-Hans`, `zh-Hant`). Fits `adapter-static` without per-language route trees; the single prerendered page applies the language client-side via the Svelte store.

### Persistence

`localStorage.audit_lang`, set when the selector changes language, read on page load as the second-priority signal.

### Fallback

Every translation key falls back to English if missing. UI never goes blank. Untranslated sections render in English. Combined with the disclaimer banner, the reader understands they are seeing a mix of translated and source-language content.

### Supported set (committed)

```ts
export const SUPPORTED_LANGS = ['en', 'fr', 'tl', 'pa', 'zh-Hans', 'zh-Hant'] as const;
```

Native-name selector labels:

| Locale | Native label | English label | `<html lang>` |
|---|---|---|---|
| `en` | English | English | `en` |
| `fr` | Français | French (Canadian) | `fr-CA` |
| `tl` | Tagalog | Tagalog | `tl` |
| `pa` | ਪੰਜਾਬੀ | Punjabi | `pa` |
| `zh-Hans` | 简体中文 | Chinese (Simplified) | `zh-Hans` |
| `zh-Hant` | 繁體中文 | Chinese (Traditional) | `zh-Hant` |

## File layout (implemented)

```
viewer/src/lib/i18n/
  store.ts                      # Svelte 5 rune store, detection, persistence
  dict.ts                       # t() function, lookup, fallback
  locales/
    en.ts
    fr.ts
    tl.ts
    pa.ts
    zh-Hans.ts
    zh-Hant.ts

viewer/src/lib/components/
  LanguageSelector.svelte       # native-name dropdown
  TranslationDisclaimer.svelte  # AI-translation banner, shown when lang != 'en'

viewer/src/routes/
  +layout.svelte                # mounts selector + disclaimer, binds <html lang>, emits hreflang
```

## Translation quality and review

| Locale | Confidence | Review path |
|---|---|---|
| `en` | Source | n/a |
| `fr` | Strong; Canadian-French register choices (vous, élus, mordus de politique, point de repère) deliberately picked | One editorial pass by anyone with native or near-native French is sufficient |
| `tl` | Competent at meaning; register and idiom imperfect | Native review actively invited via the banner; structural errors should be reported |
| `pa` | Competent at meaning; Gurmukhi script confirmed; Eastern-Punjabi vocabulary used | Native review actively invited via the banner |
| `zh-Hans` | Strong at meaning; standard written Mandarin register | Native review actively invited via the banner |
| `zh-Hant` | Same text as `zh-Hans` converted to Traditional characters; the formal civic-document register is essentially identical between Simplified and Traditional | Native review actively invited via the banner |

The disclaimer is what makes shipping all six locales at once defensible: the reader is told up front that the translation is AI-generated, and the volunteer call gives the audit a clear improvement path. This is the same pattern Wikipedia and similar civic-information sites use for machine-assisted translations.

## Rollout (implemented in this commit)

1. Infrastructure (`store.ts`, `dict.ts`) ✓
2. Components (`LanguageSelector`, `TranslationDisclaimer`) ✓
3. Layout integration (`+layout.svelte` mounts both, sets `<html lang>`, emits `hreflang`) ✓
4. Per-locale dictionaries (en, fr, tl, pa, zh-Hans, zh-Hant) seeded with the document opener + verdict + CTAs + disclaimer text ✓
5. Existing `+page.svelte` content remains untranslated for now — the new editorial content (per `proposals/verdict_and_glossary_draft.md`) will be wired through `t()` as it lands in the viewer. The disclaimer's "some content may still appear in English" sentence covers the partial-translation state honestly.

## Open questions deferred to follow-up

- **Selector position and styling.** Initial placement is top-right of the page; CSS uses inherited colours so it adapts to light/dark mode. Visual refinement is a separate pass.
- **`#contact` anchor.** The disclaimer links to `#contact`. The existing `+page.svelte` has a Resources section near the bottom; whoever wires the new editorial content should add a `#contact` anchor (or update the disclaimer link to whatever the canonical contact mechanism becomes).
- **Native translators.** The volunteer call invites them. Once volunteers are identified, their corrections land in the per-locale files via pull request; the AI-disclaimer banner stays until a locale is fully human-reviewed (a future commit can hide the banner on a per-locale basis once review completes).


**Status as of 2026-05-24: PREP COMPLETE, NOT AUTHORIZED.** The architecture, implementation code, and sample translations below are drafted to drop into the viewer cleanly. No live viewer files are touched until the PI authorizes the translation-quality gate, specifically: confirming that Canadian French is suitable for the audit's register (model-generated is acceptable for a first pass) and that Tagalog and Punjabi will go through native-speaker review before those locales are advertised on the language selector.

## Why these three languages

Statistics Canada 2021 Census, by mother tongue, Alberta:

| Language | ≈ % of population | Concentration |
|---|---|---|
| English | 76% | province-wide (default) |
| Tagalog (Filipino) | 2.5% | Edmonton, Calgary |
| Punjabi | 2.2% | Calgary, Edmonton |
| Mandarin + Cantonese (combined) | ~3% | Calgary, Edmonton |
| French | 1.5% | NE Alberta (St. Paul, Bonnyville, Plamondon, Falher) + Edmonton (La Cité francophone) |

French is below Tagalog and Punjabi by raw speaker count but is Canada's other official language and carries federal-civic-document conventions; including it is conventional for Alberta public-facing material. Combined Chinese (Mandarin + Cantonese) outranks both Tagalog and Punjabi but splits into two scripts and two oral languages; doing it well is a separate proposal.

This proposal covers French + Tagalog + Punjabi. Combined Chinese is deferred to a follow-up; Indigenous-language reach (Cree, Blackfoot, Dene, Stoney Nakoda) is a separate engagement that should work with the Treaty 6, 7, and 8 nations' language authorities, not a top-down translation.

## Architecture

### Detection priority (highest → lowest wins)

1. **URL `?lang=` parameter** — explicit user intent, always wins. Enables shareable links in a chosen language.
2. **`localStorage.audit_lang`** — saved choice from a prior visit.
3. **`navigator.languages` match** against supported set (`en`, `fr`, `tl`, `pa`) — respects the user's browser/OS preference. Matches against the locale prefix (e.g., `fr-CA` and `fr-FR` both match `fr`).
4. **Default: `en`** — the audit's source language.

Setting via the selector writes both the URL param AND localStorage, so the next visit and a shared link both pick up the choice.

### URL strategy: query parameter

The viewer uses `@sveltejs/adapter-static` and ships a single prerendered page (`docs/index.html`). Per-language path prefixes (`/fr/`, `/tl/`, `/pa/`) would require prerendering separate route trees, which is doable but adds build-config surface area and breaks the existing `merge-to-docs.mjs` postbuild script's assumptions.

Query-param routing (`?lang=fr`) is the pragmatic fit:

- Zero changes to `svelte.config.js` and the postbuild script.
- One prerendered page; language is applied client-side via a Svelte store.
- Bookmarkable and shareable URLs in a specific language.
- `hreflang` tags can still be added to `<head>` pointing at the language-suffixed URLs.

Tradeoff: search engines treat each query-param URL as the same canonical page unless `hreflang` annotations are explicit. Adding the four `hreflang` tags in `+layout.svelte` covers that.

### Persistence

`localStorage.audit_lang` — written when the selector changes language. Read at page load, used as the second-priority signal in detection.

### Fallback behavior

For every translation key, the dictionary falls back to English if the target locale is missing or returns `undefined`. The UI never goes blank because a translation is missing. Sections with no translation in the active locale render in English with a small badge: `[en]` — so the reader sees what's still in the source language and the operator sees which sections are still untranslated.

### Supported set

```ts
export const SUPPORTED_LANGS = ['en', 'fr', 'tl', 'pa'] as const;
export type Lang = typeof SUPPORTED_LANGS[number];

export const LANG_LABELS: Record<Lang, { native: string; english: string; htmlLang: string }> = {
  en: { native: 'English',     english: 'English',           htmlLang: 'en'    },
  fr: { native: 'Français',    english: 'French (Canadian)', htmlLang: 'fr-CA' },
  tl: { native: 'Tagalog',     english: 'Tagalog',           htmlLang: 'tl'    },
  pa: { native: 'ਪੰਜਾਬੀ',       english: 'Punjabi',           htmlLang: 'pa'    },
};
```

The selector renders native names so a reader who can't read English still finds their language. `htmlLang` is applied to the `<html lang="...">` attribute on language change so screen readers pick the right pronunciation.

## File layout

```
viewer/src/lib/i18n/
  index.ts                     # public exports (lang store, t() function, SUPPORTED_LANGS, LANG_LABELS)
  store.ts                     # Svelte 5 rune store, detection logic, persistence
  dict.ts                      # locale loader (re-exports from per-locale files)
  locales/
    en.ts                      # source of truth
    fr.ts
    tl.ts
    pa.ts

viewer/src/lib/components/
  LanguageSelector.svelte      # the selector UI

viewer/src/routes/
  +layout.svelte               # adds <html lang=...> binding, hreflang tags
  +page.svelte                 # uses t() instead of literal strings
```

## Drop-in implementation

### `viewer/src/lib/i18n/store.ts`

```ts
import { browser } from '$app/environment';

export const SUPPORTED_LANGS = ['en', 'fr', 'tl', 'pa'] as const;
export type Lang = typeof SUPPORTED_LANGS[number];

const STORAGE_KEY = 'audit_lang';
const URL_PARAM = 'lang';

function isSupported(s: string | null | undefined): s is Lang {
  return !!s && (SUPPORTED_LANGS as readonly string[]).includes(s);
}

function detectInitialLang(): Lang {
  if (!browser) return 'en';

  // 1. URL ?lang= param wins
  const url = new URL(window.location.href);
  const urlLang = url.searchParams.get(URL_PARAM);
  if (isSupported(urlLang)) return urlLang;

  // 2. Saved choice from prior visit
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (isSupported(saved)) return saved;
  } catch { /* private-browsing mode, ignore */ }

  // 3. Browser preference list — match against the locale prefix
  // navigator.languages is preferred over navigator.language (returns full ordered list)
  const browserLangs = navigator.languages ?? [navigator.language];
  for (const tag of browserLangs) {
    const prefix = tag.toLowerCase().split('-')[0];
    if (isSupported(prefix)) return prefix;
  }

  // 4. Default
  return 'en';
}

// Svelte 5 rune-based store
let _lang = $state<Lang>('en');

if (browser) {
  _lang = detectInitialLang();
  // Sync URL on initial load if it had a recognised language but query param wasn't set
  const url = new URL(window.location.href);
  if (url.searchParams.get(URL_PARAM) !== _lang) {
    url.searchParams.set(URL_PARAM, _lang);
    window.history.replaceState({}, '', url.toString());
  }
}

export function getLang(): Lang {
  return _lang;
}

export function setLang(next: Lang): void {
  if (!isSupported(next)) return;
  _lang = next;
  if (!browser) return;
  try {
    localStorage.setItem(STORAGE_KEY, next);
  } catch { /* ignore */ }
  const url = new URL(window.location.href);
  url.searchParams.set(URL_PARAM, next);
  window.history.replaceState({}, '', url.toString());
}

// Reactive accessor for components: import { lang } from '$lib/i18n/store';
// and use lang.current in template
export const lang = {
  get current(): Lang { return _lang; },
};
```

### `viewer/src/lib/i18n/dict.ts`

```ts
import en from './locales/en';
import fr from './locales/fr';
import tl from './locales/tl';
import pa from './locales/pa';
import type { Lang } from './store';

const dictionaries = { en, fr, tl, pa } as const;

// Looks up a dotted key path. Falls back to English if the target is missing.
// Returns the key path itself if even English is missing (loud development signal).
export function t(lang: Lang, keyPath: string): string {
  const target = lookup(dictionaries[lang], keyPath);
  if (typeof target === 'string') return target;
  const fallback = lookup(dictionaries.en, keyPath);
  if (typeof fallback === 'string') return fallback;
  return `[missing:${keyPath}]`;
}

// Returns true when the target language has its own translation
// for a key (used to render an [en] badge when falling back).
export function hasTranslation(lang: Lang, keyPath: string): boolean {
  return typeof lookup(dictionaries[lang], keyPath) === 'string';
}

function lookup(obj: unknown, keyPath: string): unknown {
  let cur: unknown = obj;
  for (const k of keyPath.split('.')) {
    if (cur && typeof cur === 'object' && k in (cur as Record<string, unknown>)) {
      cur = (cur as Record<string, unknown>)[k];
    } else {
      return undefined;
    }
  }
  return cur;
}
```

### `viewer/src/lib/i18n/locales/en.ts`

```ts
export default {
  opener: {
    heading: "Who's this for?",
    body: "Us. All of us. Rural, Urban, curious, wonk, journalist, lawyer, academic, politician — all of us. Because it impacts all of us. Whether or not you like the party in power, what the split commission produced has never been done before. And it's given us the opportunity to peer inside the machine in ways we never could before. Now we can establish a baseline — a series of tests, and everything that comes after can be graded on it. Let me show you what I found.",
  },
  verdict: {
    q1: {
      heading: "Is the proposed map a gerrymander?",
      body: "\"Gerrymander\" is not a term Canadian courts use. But if it were — in the everyday sense most people mean by it — the evidence in this audit would reasonably support calling the minority proposal, if enacted, a heavily gerrymandered map. Every structural test this audit runs flags the minority proposal; none flag the alternative (the majority proposal).",
    },
    q2: {
      heading: "What does \"gerrymander\" mean in Canadian law?",
      body: "It doesn't. The Canadian test is different: whether the boundaries give voters effective representation under section 3 of the Charter. The minority proposal raises serious questions under that test; only a judge can answer them definitively, and no one has asked one yet.",
    },
    q3: {
      heading: "What does it mean for Albertans?",
      body: "At a 50/50 provincial vote, the audit's measurements place the minority proposal at a structural extreme — fewer than 100 of the 1.01 million neutral comparison maps produce the same kind of seat imbalance. That imbalance matters because at 58 of 87 seats — a two-thirds supermajority — the governing party unlocks extraordinary procedural powers: it can waive standard notice periods and push public bills through multiple legislative stages in a single day, bypassing deliberation checks that normally constrain it. Whether the minority proposal's tilt is large enough to push one party past that 58-seat threshold at vote shares other than 50/50 is a question this audit has not yet tested. Whether the tradeoff itself is acceptable is a question for Albertans, not for this audit.",
    },
    cta_law: "Read the legal context →",
    cta_methods: "See how we tested →",
  },
} as const;
```

### `viewer/src/lib/components/LanguageSelector.svelte`

```svelte
<script lang="ts">
  import { lang, setLang, SUPPORTED_LANGS, LANG_LABELS, type Lang } from '$lib/i18n/store';

  let open = $state(false);

  function choose(next: Lang) {
    setLang(next);
    open = false;
    if (typeof document !== 'undefined') {
      document.documentElement.lang = LANG_LABELS[next].htmlLang;
    }
  }
</script>

<div class="lang-selector">
  <button
    class="lang-trigger"
    aria-haspopup="listbox"
    aria-expanded={open}
    onclick={() => (open = !open)}
  >
    {LANG_LABELS[lang.current].native}
    <span aria-hidden="true">▾</span>
  </button>
  {#if open}
    <ul class="lang-menu" role="listbox">
      {#each SUPPORTED_LANGS as code}
        <li>
          <button
            class="lang-option"
            class:active={code === lang.current}
            role="option"
            aria-selected={code === lang.current}
            onclick={() => choose(code)}
          >
            {LANG_LABELS[code].native}
            <span class="lang-english">{LANG_LABELS[code].english}</span>
          </button>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .lang-selector { position: relative; display: inline-block; font-size: 0.9rem; }
  .lang-trigger { background: transparent; border: 1px solid currentColor; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer; color: inherit; }
  .lang-menu { position: absolute; top: 100%; right: 0; margin: 0.3rem 0 0; padding: 0.3rem 0; list-style: none; background: var(--bg, white); border: 1px solid currentColor; border-radius: 4px; min-width: 12rem; z-index: 50; }
  .lang-option { display: flex; flex-direction: column; align-items: flex-start; width: 100%; padding: 0.4rem 0.8rem; background: transparent; border: 0; cursor: pointer; text-align: left; color: inherit; }
  .lang-option:hover, .lang-option:focus { background: rgba(0,0,0,0.06); }
  .lang-option.active { font-weight: 600; }
  .lang-english { font-size: 0.75rem; opacity: 0.6; }
</style>
```

### `viewer/src/routes/+layout.svelte` additions

```svelte
<script lang="ts">
  import { lang, LANG_LABELS } from '$lib/i18n/store';

  // Keep <html lang="..."> in sync with the active language for screen readers + search engines
  $effect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.lang = LANG_LABELS[lang.current].htmlLang;
    }
  });

  let { children } = $props();
</script>

<svelte:head>
  <!-- Tell search engines about each language variant of this URL -->
  <link rel="alternate" hreflang="en"    href="{import.meta.env.VITE_CANONICAL_URL ?? ''}/?lang=en" />
  <link rel="alternate" hreflang="fr-CA" href="{import.meta.env.VITE_CANONICAL_URL ?? ''}/?lang=fr" />
  <link rel="alternate" hreflang="tl"    href="{import.meta.env.VITE_CANONICAL_URL ?? ''}/?lang=tl" />
  <link rel="alternate" hreflang="pa"    href="{import.meta.env.VITE_CANONICAL_URL ?? ''}/?lang=pa" />
  <link rel="alternate" hreflang="x-default" href="{import.meta.env.VITE_CANONICAL_URL ?? ''}/" />
</svelte:head>

{@render children()}
```

## Sample translations

These are drafted to drop into `viewer/src/lib/i18n/locales/{fr,tl,pa}.ts`. Quality varies by language — see the **Quality gate** section below for what's ready to ship vs what needs native-speaker review.

### Canadian French (`fr.ts`) — ready for editorial review, not native review-blocked

```ts
export default {
  opener: {
    heading: "À qui s'adresse ce document ?",
    body: "À nous. À nous tous. Aux ruraux, aux urbains, aux curieux, aux mordus de politique, aux journalistes, aux avocats, aux universitaires, aux élus — à nous tous. Parce que cela nous touche tous. Que vous aimiez ou non le parti au pouvoir, ce que la commission divisée a produit ne s'était jamais vu auparavant. Et cela nous donne l'occasion d'observer la mécanique de l'intérieur comme nous n'avions jamais pu le faire. Nous pouvons maintenant établir un point de repère — une série de tests, et tout ce qui suivra pourra être évalué à cette aune. Laissez-moi vous montrer ce que j'ai trouvé.",
  },
  verdict: {
    q1: {
      heading: "La carte proposée est-elle un découpage partisan ?",
      body: "« Gerrymander » n'est pas un terme employé par les tribunaux canadiens. Mais s'il l'était — au sens courant que la plupart des gens lui donnent — les éléments de cet audit appuieraient raisonnablement la qualification de la proposition minoritaire, si elle était adoptée, comme une carte fortement remaniée à des fins partisanes. Tous les tests structurels de cet audit signalent la proposition minoritaire ; aucun ne signale l'autre (la proposition majoritaire).",
    },
    q2: {
      heading: "Que signifie « gerrymander » en droit canadien ?",
      body: "Rien. Le critère canadien est différent : il s'agit de savoir si les limites garantissent aux électeurs une représentation effective au sens de l'article 3 de la Charte. La proposition minoritaire soulève de sérieuses questions sous ce critère ; seul un juge peut y répondre de façon définitive, et personne n'en a saisi un.",
    },
    q3: {
      heading: "Qu'est-ce que cela signifie pour les Albertains ?",
      body: "Lors d'un vote provincial à 50/50, les mesures de l'audit placent la proposition minoritaire dans un extrême structurel — moins de 100 des 1,01 million de cartes neutres de comparaison produisent un déséquilibre de sièges comparable. Ce déséquilibre compte parce qu'à 58 sièges sur 87 — une majorité des deux tiers — le parti au pouvoir débloque des pouvoirs procéduraux exceptionnels : il peut écarter les délais d'avis habituels et faire franchir à un projet de loi public plusieurs étapes législatives en une seule journée, contournant les freins délibératifs qui le contraignent normalement. Savoir si l'inclinaison de la proposition minoritaire est assez forte pour porter un parti au-delà de ce seuil de 58 sièges à des résultats de vote autres que 50/50 est une question que cet audit n'a pas encore examinée. Savoir si le compromis lui-même est acceptable est une question pour les Albertains, et non pour cet audit.",
    },
    cta_law: "Lire le contexte juridique →",
    cta_methods: "Voir notre méthodologie →",
  },
} as const;
```

### Tagalog (`tl.ts`) — DRAFT, NEEDS NATIVE-SPEAKER REVIEW BEFORE SHIPPING

```ts
export default {
  opener: {
    heading: "Para kanino ito?",
    body: "Para sa atin. Para sa ating lahat. Sa mga taga-bukid, sa mga taga-lungsod, sa mga curious, sa mga mahilig sa pulitika, sa mga mamamahayag, sa mga abugado, sa mga akademiko, sa mga pulitiko — para sa ating lahat. Dahil nakakaapekto ito sa ating lahat. Anuman ang iyong palagay sa partidong nasa poder, ang ginawa ng hating komisyon ay hindi pa nangyari noon. At binigyan tayo nito ng pagkakataong masilip ang loob ng makinarya sa paraang hindi pa natin nagawa. Ngayon ay maaari na tayong magtatag ng isang batayan — isang serye ng mga pagsusulit, at lahat ng susunod ay maaaring sukatin batay dito. Hayaan ninyong ipakita ko sa inyo ang aking natuklasan.",
  },
  // Verdict Q1 / Q2 / Q3 deliberately omitted from this draft until native-speaker
  // review of the opener confirms register and idiom — translating more before
  // that gate risks compounding any systematic errors across the whole page.
} as const;
```

### Punjabi (Gurmukhi, `pa.ts`) — DRAFT, NEEDS NATIVE-SPEAKER REVIEW BEFORE SHIPPING

```ts
export default {
  opener: {
    heading: "ਇਹ ਕਿਸ ਲਈ ਹੈ?",
    body: "ਸਾਡੇ ਲਈ। ਸਾਡੇ ਸਾਰਿਆਂ ਲਈ। ਪੇਂਡੂ, ਸ਼ਹਿਰੀ, ਜਿਗਿਆਸੂ, ਸਿਆਸਤ ਦੇ ਸ਼ੁਕੀਨ, ਪੱਤਰਕਾਰ, ਵਕੀਲ, ਵਿਦਵਾਨ, ਚੁਣੇ ਹੋਏ ਨੁਮਾਇੰਦੇ — ਸਾਡੇ ਸਾਰਿਆਂ ਲਈ। ਕਿਉਂਕਿ ਇਹ ਸਾਨੂੰ ਸਾਰਿਆਂ ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰਦਾ ਹੈ। ਭਾਵੇਂ ਤੁਸੀਂ ਸੱਤਾਧਾਰੀ ਪਾਰਟੀ ਨੂੰ ਪਸੰਦ ਕਰਦੇ ਹੋ ਜਾਂ ਨਹੀਂ, ਜੋ ਵੰਡੇ ਹੋਏ ਕਮਿਸ਼ਨ ਨੇ ਪੈਦਾ ਕੀਤਾ ਉਹ ਪਹਿਲਾਂ ਕਦੇ ਨਹੀਂ ਹੋਇਆ। ਅਤੇ ਇਸ ਨੇ ਸਾਨੂੰ ਇਸ ਮਸ਼ੀਨ ਦੇ ਅੰਦਰ ਝਾਤੀ ਮਾਰਨ ਦਾ ਮੌਕਾ ਦਿੱਤਾ ਹੈ ਜਿਸ ਤਰ੍ਹਾਂ ਅਸੀਂ ਪਹਿਲਾਂ ਕਦੇ ਨਹੀਂ ਮਾਰ ਸਕੇ। ਹੁਣ ਅਸੀਂ ਇੱਕ ਆਧਾਰ-ਰੇਖਾ ਸਥਾਪਤ ਕਰ ਸਕਦੇ ਹਾਂ — ਪਰੀਖਣਾਂ ਦੀ ਇੱਕ ਲੜੀ, ਅਤੇ ਜੋ ਕੁਝ ਵੀ ਬਾਅਦ ਵਿੱਚ ਆਉਂਦਾ ਹੈ ਉਸਨੂੰ ਇਸ ਦੇ ਆਧਾਰ ਉੱਤੇ ਪਰਖਿਆ ਜਾ ਸਕਦਾ ਹੈ। ਮੈਨੂੰ ਤੁਹਾਨੂੰ ਦਿਖਾਉਣ ਦਿਓ ਕਿ ਮੈਂ ਕੀ ਲੱਭਿਆ ਹੈ।",
  },
  // Verdict Q1 / Q2 / Q3 deliberately omitted until native-speaker review of the
  // opener confirms register, script (Gurmukhi vs Shahmukhi — confirmed Gurmukhi
  // for the Canadian Punjabi diaspora), and Eastern-vs-Western Punjabi dialect
  // conventions. Same compounding-risk rationale as the Tagalog draft.
} as const;
```

## Quality gate — what's ready to ship vs what isn't

| Language | Capability honest read | Ready to ship? |
|---|---|---|
| **English** | Source of truth | ✓ Ship |
| **Canadian French** | Strong on register and idiom; can match the audit's direct-but-respectful tone; technical / legal vocabulary handled correctly. The draft below uses `vous` throughout and Canadian-French conventions (*élus* over *politiciens*, *mordus de politique* over *passionnés*, *point de repère* over *référentiel*). | ✓ Ship after one editorial pass by anyone with native or near-native French. The model-generated text is at "good first draft" quality. |
| **Tagalog** | Competent at structure and meaning; register and idiom are harder for the model to land natively. Specific risk: the *po/opo* respect markers and the formal/informal `kayo/ninyo` vs `ikaw/mo` choice — the draft uses formal *ninyo* / *kayo*. Calgary/Edmonton Filipino community is largely Tagalog-speaking with some regional variation. | ⚠ Do NOT ship without native-speaker review. The draft is a starting point for a translator, not a finished translation. |
| **Punjabi (Gurmukhi)** | Competent at meaning; script is correct (Gurmukhi is the Canadian Punjabi diaspora standard, not Shahmukhi). Dialect risk: the draft uses Eastern Punjabi vocabulary that is dominant in Calgary/Edmonton. Specific risk: technical terms like *baseline* (the draft uses *ਆਧਾਰ-ਰੇਖਾ*) have multiple correct renderings and a native speaker should pick the most natural. | ⚠ Do NOT ship without native-speaker review. Same starting-point-not-finished caveat as Tagalog. |

The selector should not advertise Tagalog or Punjabi until their drafts have been through review. Options for the gate:

- **Option A — Soft launch.** Ship the infrastructure + French + English. Selector shows only `en` and `fr`. Tagalog and Punjabi land as a follow-up commit when native review completes.
- **Option B — Beta channel.** Ship all four locales with a "BETA — under review" label next to TL and PA in the selector menu. Risk: a casual reader may not notice the label.
- **Option C — Wait for review.** Don't ship any of the infrastructure until all four locales are ready.

Recommendation: **Option A.** Ships the system; defers the language additions until each is reviewed. Lowest risk of putting a substandard translation in front of a community it's supposed to serve.

## Rollout sequence

1. **PI authorizes the architecture and the quality gate.** Confirm Option A (soft launch with EN + FR only at first), confirm French draft passes one editorial review pass, confirm the URL-param + localStorage + browser-language detection chain.
2. **Implementation.** Create files per the file-layout section. Drop in the code per the implementation section. Wire the selector into the `+page.svelte` header. Update `+page.svelte` to call `t('opener.heading')` etc instead of literal strings for the translated keys.
3. **Translate the rest of the page progressively.** The dictionary covers the document opener + verdict in the initial commit. Subsequent commits add Section 1, Section 5, Section 6, Section 7. Each section can be translated independently and shipped when its EN source is locked.
4. **Native review for TL + PA.** Once a translator is identified for each, the existing drafts in this proposal are the starting point. When review completes, the selector adds those options.
5. **Indigenous-language outreach.** Separate engagement; do not attempt model-driven translation. Connect with the Treaty 6 / 7 / 8 nations' language authorities; offer to support whatever they produce with technical/structural editing only.

## Open questions for the PI

- **Selector position.** Top-right of the header is the convention. Confirm or pick an alternative.
- **Whether to detect French at all by default.** A Canadian browser set to `fr-CA` will get French automatically. Is that desired, or should English remain the default until the reader opts in? (Recommendation: respect `fr-CA` automatically; that is the conventional Canadian-civic-document behaviour.)
- **Whether to add Mandarin / Cantonese as a follow-up proposal.** Combined Chinese outranks both Tagalog and Punjabi by raw speaker count in Alberta and would meaningfully extend reach.
- **Whether to commission native translators for TL + PA now, or wait.** The translations sit in proposals/ until reviewed. The longer the gap, the more the source content drifts; pinning translators sooner reduces re-translation cost later.

## Authorization checklist

Before any code in this proposal lands in `viewer/`:

- [ ] PI approves Option A (soft-launch with EN + FR only at first)
- [ ] PI confirms the URL-param + localStorage + browser-language detection chain
- [ ] French draft passes one editorial review pass (anyone with native or near-native French)
- [ ] Native-speaker translators identified for Tagalog and Punjabi (their work lands in a follow-up commit, not the initial ship)
- [ ] Selector position and styling confirmed
