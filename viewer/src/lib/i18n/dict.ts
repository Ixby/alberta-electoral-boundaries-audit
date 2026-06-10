import en from './locales/en';
import fr from './locales/fr';
import de from './locales/de';
import uk from './locales/uk';
import tl from './locales/tl';
import pa from './locales/pa';
import zhHans from './locales/zh-Hans';
import zhHant from './locales/zh-Hant';
import type { Lang } from './store.svelte';

const dictionaries: Record<Lang, unknown> = {
	en,
	fr,
	de,
	uk,
	tl,
	pa,
	'zh-Hans': zhHans,
	'zh-Hant': zhHant
};

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

/**
 * Look up a dotted key path in the active locale's dictionary.
 * Falls back to English if the target is missing. Returns `[missing:keypath]`
 * if even English is missing — a deliberately loud signal in development.
 */
export function t(activeLang: Lang, keyPath: string): string {
	const target = lookup(dictionaries[activeLang], keyPath);
	if (typeof target === 'string') return target;
	const fallback = lookup(dictionaries.en, keyPath);
	if (typeof fallback === 'string') return fallback;
	return `[missing:${keyPath}]`;
}

/** True when the active locale has its own translation for this key (not fallback). */
export function hasTranslation(activeLang: Lang, keyPath: string): boolean {
	return typeof lookup(dictionaries[activeLang], keyPath) === 'string';
}
