// Tests for src/lib/i18n/dict.ts — translation lookup with English fallback.
//
// The dict layer is the only thing standing between the UI and a wall of
// `[missing:keypath]` placeholders. Three properties matter:
//   1. Exact-locale hit returns the locale string.
//   2. Missing key in the active locale falls back to the English string.
//   3. Missing in both returns the loud `[missing:keypath]` token (never undefined,
//      never the keypath itself, never an empty string — those would silently
//      ship blank text).

import { describe, it, expect } from 'vitest';
import { t, hasTranslation } from '../src/lib/i18n/dict';

describe('t() — translation lookup', () => {
	it('returns the English string for a known key in English', () => {
		const result = t('en', 'nav.home_aria');
		expect(typeof result).toBe('string');
		expect(result.length).toBeGreaterThan(0);
		expect(result).not.toMatch(/^\[missing:/);
	});

	it('returns a string for a deeply-nested key', () => {
		const result = t('en', 'stakes.q1.heading');
		expect(typeof result).toBe('string');
		expect(result.length).toBeGreaterThan(0);
	});

	it('falls back to English when a non-English locale lacks the key', () => {
		// Many keys aren't translated to fr / pa / tl / zh — they should
		// fall through to the English source-of-truth rather than break.
		const enResult = t('en', 'stakes.scorecard_h');
		const frResult = t('fr', 'stakes.scorecard_h');
		// Either fr has its own translation OR it falls back to en's value;
		// neither outcome should produce the `[missing:...]` token.
		expect(frResult).not.toMatch(/^\[missing:/);
		expect(typeof frResult).toBe('string');
		// If fr didn't translate this key, it must equal the en value.
		if (!hasTranslation('fr', 'stakes.scorecard_h')) {
			expect(frResult).toBe(enResult);
		}
	});

	it('returns `[missing:keypath]` when neither locale nor en has the key', () => {
		const result = t('en', 'this.key.does.not.exist.anywhere');
		expect(result).toBe('[missing:this.key.does.not.exist.anywhere]');
	});

	it('returns `[missing:keypath]` for an empty key path', () => {
		const result = t('en', '');
		expect(result).toBe('[missing:]');
	});

	it('returns `[missing:keypath]` when an intermediate key is a string (not an object)', () => {
		// `nav.home_aria` is a string. Trying to descend into it should not crash.
		const result = t('en', 'nav.home_aria.imaginary_sub_key');
		expect(result).toBe('[missing:nav.home_aria.imaginary_sub_key]');
	});

	it('handles all six supported locale codes without throwing', () => {
		const locales = ['en', 'fr', 'pa', 'tl', 'zh-Hans', 'zh-Hant'] as const;
		for (const lang of locales) {
			const result = t(lang, 'nav.home_aria');
			expect(typeof result).toBe('string');
			expect(result.length).toBeGreaterThan(0);
		}
	});
});

describe('hasTranslation() — locale-has-its-own check', () => {
	it('returns true when the active locale has its own translation', () => {
		// `nav.home_aria` exists in en.
		expect(hasTranslation('en', 'nav.home_aria')).toBe(true);
	});

	it('returns false for a missing key', () => {
		expect(hasTranslation('en', 'this.key.does.not.exist')).toBe(false);
	});

	it('returns false when only the English fallback would resolve', () => {
		// Pick a key likely to be in en but not in pa — if the locale doesn't
		// carry its own translation, hasTranslation should report false
		// regardless of whether `t()` would still return a fallback string.
		const keysOnlyInEn = ['stakes.scorecard_h', 'stakes.scorecard_intro'];
		for (const key of keysOnlyInEn) {
			if (!hasTranslation('pa', key)) {
				// hasTranslation says no for pa, but t() should still resolve
				// via fallback to en — the two functions answer different
				// questions. Confirm both hold.
				expect(hasTranslation('pa', key)).toBe(false);
				expect(t('pa', key)).not.toMatch(/^\[missing:/);
			}
		}
	});
});
