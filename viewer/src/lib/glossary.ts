/**
 * Glossary source — the list of terms the audit defines for the curious reader.
 *
 * Each entry has:
 *   - id: stable key used by <Gloss id="..."> markup + the en.ts dictionary
 *   - href: optional in-page anchor for "Learn more →" (or null if no deeper section)
 *
 * Term text and definition text live in viewer/src/lib/i18n/locales/*.ts under
 * glossary.{id}.term and glossary.{id}.definition. That keeps both translatable
 * and means the Gloss component fully renders from t() without hardcoded English.
 *
 * Terms are taken from proposals/verdict_and_glossary_draft.md Part 8 (the
 * glossary draft). Tier-1 terms — those the curious-citizen route encounters
 * first — are populated below. Tier-2 (legal-route) and Tier-3 (methods-route)
 * terms can be added in subsequent commits using the same id/href shape.
 */

export interface GlossaryEntry {
	id: string;
	/** Anchor on the homepage for "Learn more →" link, or null if no destination. */
	href: string | null;
}

export const GLOSSARY: Record<string, GlossaryEntry> = {
	'electoral-district': { id: 'electoral-district', href: '#what-is-redistricting' },
	riding: { id: 'riding', href: '#what-is-redistricting' },
	mla: { id: 'mla', href: '#what-is-redistricting' },
	ucp: { id: 'ucp', href: null },
	ndp: { id: 'ndp', href: null },
	gerrymander: { id: 'gerrymander', href: '#history-of-gerrymandering' },
	cracking: { id: 'cracking', href: '#section-4' },
	packing: { id: 'packing', href: '#section-4' },
	draining: { id: 'draining', href: '#section-4' },
	anchoring: { id: 'anchoring', href: '#section-3' },
	'charter-s3': { id: 'charter-s3', href: '#canada-is-different' },
	'effective-representation': { id: 'effective-representation', href: '#canada-is-different' },
	ebc: { id: 'ebc', href: '#what-is-redistricting' },
	'lunty-committee': { id: 'lunty-committee', href: '#section-7' },
	ebca: { id: 'ebca', href: '#canada-is-different' },
	fsa: { id: 'fsa', href: null }
};

/** True when an entry id is registered. The Gloss component uses this to fail
 *  loudly during development if the markup references an unknown id. */
export function isGlossaryId(id: string): id is keyof typeof GLOSSARY {
	return Object.prototype.hasOwnProperty.call(GLOSSARY, id);
}
