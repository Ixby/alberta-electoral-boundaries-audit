import { browser } from '$app/environment';

// Order = approximate Alberta speakers (2021 Census mother tongue):
// English (majority) → Tagalog ~99k → Punjabi ~86k → French ~72k →
// Cantonese ~46k (zh-Hant) → Mandarin ~43k (zh-Hans) → German ~36k
// (plus Hutterite/Mennonite Plautdietsch communities) → Ukrainian ~14k
// (plus the post-2022 arrival wave the census predates). The language
// dropdown renders in this order.
export const SUPPORTED_LANGS = ['en', 'tl', 'pa', 'fr', 'zh-Hant', 'zh-Hans', 'de', 'uk'] as const;
export type Lang = (typeof SUPPORTED_LANGS)[number];

export const LANG_LABELS: Record<
	Lang,
	{ native: string; english: string; htmlLang: string }
> = {
	en: { native: 'English', english: 'English', htmlLang: 'en' },
	fr: { native: 'Français', english: 'French (Canadian)', htmlLang: 'fr-CA' },
	de: { native: 'Deutsch', english: 'German', htmlLang: 'de' },
	uk: { native: 'Українська', english: 'Ukrainian', htmlLang: 'uk' },
	tl: { native: 'Tagalog', english: 'Tagalog', htmlLang: 'tl' },
	pa: { native: 'ਪੰਜਾਬੀ', english: 'Punjabi', htmlLang: 'pa' },
	'zh-Hans': { native: '简体中文', english: 'Chinese (Simplified)', htmlLang: 'zh-Hans' },
	'zh-Hant': { native: '繁體中文', english: 'Chinese (Traditional)', htmlLang: 'zh-Hant' }
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

let _lang = $state<Lang>('en');

if (browser) {
	// Use a local const for the sync side-effects so we never read the
	// `$state` variable at module scope (which Svelte 5 flags as a
	// non-reactive capture and which is genuinely the wrong shape for
	// any future readers of `_lang` on this branch).
	const initial = detectInitialLang();
	_lang = initial;
	const url = new URL(window.location.href);
	if (url.searchParams.get(URL_PARAM) !== initial) {
		url.searchParams.set(URL_PARAM, initial);
		window.history.replaceState({}, '', url.toString());
	}
}

export function setLang(next: Lang): void {
	if (!isSupported(next)) return;
	_lang = next;
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
