import { browser } from '$app/environment';

// Order = approximate Alberta speakers (2021 Census mother tongue):
// English (majority) → Tagalog ~99k → Punjabi ~86k → French ~72k →
// Spanish ~62k → Arabic ~55k → Cantonese ~46k (zh-Hant) → Mandarin
// ~43k (zh-Hans) → German ~36k → Hindi ~32k → Vietnamese ~25k →
// Korean ~17k → Urdu ~17k → Polish ~15k → Ukrainian ~14k (plus the
// post-2022 arrival wave the census predates). The language dropdown
// renders in this order.
export const SUPPORTED_LANGS = [
	'en',
	'tl',
	'pa',
	'fr',
	'es',
	'ar',
	'zh-Hant',
	'zh-Hans',
	'de',
	'hi',
	'vi',
	'ko',
	'ur',
	'pl',
	'uk',
	'ru',
	'so',
	'crk',
	'pdt'
] as const;
export type Lang = (typeof SUPPORTED_LANGS)[number];

export const LANG_LABELS: Record<
	Lang,
	{ native: string; english: string; htmlLang: string; dir: 'ltr' | 'rtl' }
> = {
	en: { native: 'English', english: 'English', htmlLang: 'en', dir: 'ltr' },
	tl: { native: 'Tagalog', english: 'Tagalog', htmlLang: 'tl', dir: 'ltr' },
	pa: { native: 'ਪੰਜਾਬੀ', english: 'Punjabi', htmlLang: 'pa', dir: 'ltr' },
	fr: { native: 'Français', english: 'French (Canadian)', htmlLang: 'fr-CA', dir: 'ltr' },
	es: { native: 'Español', english: 'Spanish', htmlLang: 'es', dir: 'ltr' },
	ar: { native: 'العربية', english: 'Arabic', htmlLang: 'ar', dir: 'rtl' },
	'zh-Hant': { native: '繁體中文', english: 'Chinese (Traditional)', htmlLang: 'zh-Hant', dir: 'ltr' },
	'zh-Hans': { native: '简体中文', english: 'Chinese (Simplified)', htmlLang: 'zh-Hans', dir: 'ltr' },
	de: { native: 'Deutsch', english: 'German', htmlLang: 'de', dir: 'ltr' },
	hi: { native: 'हिन्दी', english: 'Hindi', htmlLang: 'hi', dir: 'ltr' },
	vi: { native: 'Tiếng Việt', english: 'Vietnamese', htmlLang: 'vi', dir: 'ltr' },
	ko: { native: '한국어', english: 'Korean', htmlLang: 'ko', dir: 'ltr' },
	ur: { native: 'اردو', english: 'Urdu', htmlLang: 'ur', dir: 'rtl' },
	pl: { native: 'Polski', english: 'Polish', htmlLang: 'pl', dir: 'ltr' },
	uk: { native: 'Українська', english: 'Ukrainian', htmlLang: 'uk', dir: 'ltr' },
	ru: { native: 'Русский', english: 'Russian', htmlLang: 'ru', dir: 'ltr' },
	so: { native: 'Soomaali', english: 'Somali', htmlLang: 'so', dir: 'ltr' },
	crk: { native: 'ᓀᐦᐃᔭᐍᐏᐣ', english: 'Plains Cree', htmlLang: 'crk', dir: 'ltr' },
	pdt: { native: 'Plautdietsch', english: 'Plautdietsch (Mennonite Low German)', htmlLang: 'pdt', dir: 'ltr' }
};

const STORAGE_KEY = 'audit_lang';
const URL_PARAM = 'lang';

function isSupported(s: string | null | undefined): s is Lang {
	return !!s && (SUPPORTED_LANGS as readonly string[]).includes(s);
}

// Match navigator.languages tags against supported locales.
// Prefix rules:
//   - simple two-letter prefix matches the same code (fr-CA -> fr, tl-PH -> tl, pa-IN -> pa)
//   - zh-CN, zh-SG, zh-Hans -> zh-Hans
//   - zh-HK, zh-TW, zh-MO, zh-Hant -> zh-Hant
function matchBrowserTag(tag: string): Lang | null {
	const lower = tag.toLowerCase();
	if (lower.startsWith('zh')) {
		if (
			lower.includes('hant') ||
			lower.startsWith('zh-hk') ||
			lower.startsWith('zh-tw') ||
			lower.startsWith('zh-mo')
		)
			return 'zh-Hant';
		return 'zh-Hans';
	}
	const prefix = lower.split('-')[0];
	if (isSupported(prefix)) return prefix as Lang;
	return null;
}

function detectInitialLang(): Lang {
	if (!browser) return 'en';

	const url = new URL(window.location.href);
	const urlLang = url.searchParams.get(URL_PARAM);
	if (isSupported(urlLang)) return urlLang;

	try {
		const saved = localStorage.getItem(STORAGE_KEY);
		if (isSupported(saved)) return saved;
	} catch {
		// private-browsing or storage disabled; ignore
	}

	const browserLangs: readonly string[] = navigator.languages ?? [navigator.language];
	for (const tag of browserLangs) {
		const matched = matchBrowserTag(tag);
		if (matched) return matched;
	}

	return 'en';
}

// ── Lazy locale loading ──────────────────────────────────────────────────────
// Only `en` ships in the initial bundle (the prerender default + sync fallback in
// dict.ts). Every other locale is its own chunk, fetched on demand — this keeps
// ~700 KB of translations off the first load. Each loader is the ONLY reference to
// its locale module, so Rollup code-splits them into separate chunks.
const loaders: Partial<Record<Lang, () => Promise<{ default: unknown }>>> = {
	tl: () => import('./locales/tl'),
	pa: () => import('./locales/pa'),
	fr: () => import('./locales/fr'),
	es: () => import('./locales/es'),
	ar: () => import('./locales/ar'),
	'zh-Hant': () => import('./locales/zh-Hant'),
	'zh-Hans': () => import('./locales/zh-Hans'),
	de: () => import('./locales/de'),
	hi: () => import('./locales/hi'),
	vi: () => import('./locales/vi'),
	ko: () => import('./locales/ko'),
	ur: () => import('./locales/ur'),
	pl: () => import('./locales/pl'),
	uk: () => import('./locales/uk'),
	ru: () => import('./locales/ru'),
	so: () => import('./locales/so'),
	crk: () => import('./locales/crk'),
	pdt: () => import('./locales/pdt')
};

const _loaded: Partial<Record<Lang, unknown>> = {};
let _dictVersion = $state(0);

/** Reactive version — read it inside t()/hasTranslation so consumers re-render
 *  when a locale chunk arrives (the en→target swap). */
export function dictVersion(): number {
	return _dictVersion;
}

/** The loaded dictionary for a locale, or undefined if its chunk isn't here yet
 *  (en is handled directly in dict.ts and is never stored here). */
export function loadedDict(l: Lang): unknown {
	return _loaded[l];
}

/** Fetch a locale's chunk on demand. No-op for en / already-loaded. Bumps
 *  dictVersion on arrival so the active view re-renders into the new language. */
export async function loadLang(l: Lang): Promise<void> {
	if (l === 'en' || _loaded[l]) return;
	const loader = loaders[l];
	if (!loader) return;
	try {
		const mod = await loader();
		_loaded[l] = mod.default;
		_dictVersion++;
	} catch {
		// chunk fetch failed (e.g. offline) — t() keeps using the en fallback
	}
}

let _lang = $state<Lang>('en');

if (browser) {
	// Use a local const for the sync side-effects so we never read the
	// `$state` variable at module scope (which Svelte 5 flags as a
	// non-reactive capture and which is genuinely the wrong shape for
	// any future readers of `_lang` on this branch).
	const initial = detectInitialLang();
	_lang = initial;
	// Kick off the active locale's chunk immediately (no-op for en). The view
	// renders with the en fallback until it arrives, then swaps.
	void loadLang(initial);
	const url = new URL(window.location.href);
	if (url.searchParams.get(URL_PARAM) !== initial) {
		url.searchParams.set(URL_PARAM, initial);
		window.history.replaceState({}, '', url.toString());
	}
}

export function setLang(next: Lang): void {
	if (!isSupported(next)) return;
	_lang = next;
	// Fetch the chosen locale's chunk; t() uses the en fallback until it lands.
	void loadLang(next);
	if (!browser) return;
	try {
		localStorage.setItem(STORAGE_KEY, next);
	} catch {
		// ignore
	}
	const url = new URL(window.location.href);
	url.searchParams.set(URL_PARAM, next);
	window.history.replaceState({}, '', url.toString());
}

export const lang = {
	get current(): Lang {
		return _lang;
	}
};
