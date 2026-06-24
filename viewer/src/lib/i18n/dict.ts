import en from './locales/en';
import { dictVersion, loadedDict } from './store.svelte';
import type { Lang } from './store.svelte';

// Only English is bundled eagerly here — it is the prerender default and the
// universal fallback, so t() can always answer synchronously. Every other locale
// is a separate chunk fetched on demand by the store's loadLang(); see
// store.svelte.ts. Until the active locale's chunk arrives, t() falls back to en;
// reading dictVersion() subscribes callers so they re-render once it does.

function activeDict(activeLang: Lang): unknown {
	return activeLang === 'en' ? en : loadedDict(activeLang);
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

/**
 * Look up a dotted key path in the active locale's dictionary.
 * Falls back to English if the target is missing (or its chunk hasn't loaded yet).
 * Returns `[missing:keypath]` if even English is missing — a deliberately loud
 * signal in development.
 */
export function t(activeLang: Lang, keyPath: string): string {
	dictVersion(); // subscribe: re-run when the active locale's chunk arrives
	const target = lookup(activeDict(activeLang), keyPath);
	if (typeof target === 'string') return target;
	const fallback = lookup(en, keyPath);
	if (typeof fallback === 'string') return fallback;
	return `[missing:${keyPath}]`;
}

/** True when the active locale has its own translation for this key (not fallback). */
export function hasTranslation(activeLang: Lang, keyPath: string): boolean {
	dictVersion(); // subscribe (so a key flips from fallback to real once loaded)
	return typeof lookup(activeDict(activeLang), keyPath) === 'string';
}
