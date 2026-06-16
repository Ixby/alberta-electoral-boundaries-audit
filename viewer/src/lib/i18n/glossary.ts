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
