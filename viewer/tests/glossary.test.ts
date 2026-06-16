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
		// `ensemble` is one of the Plan-1 terms; no locale other than en has it yet.
		const en = gloss('en', 'ensemble').definition;
		const fr = gloss('fr', 'ensemble').definition;
		expect(fr).toBe(en);
		expect(fr).not.toMatch(/^\[missing:/);
	});
});
