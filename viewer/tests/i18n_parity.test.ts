// i18n key-parity gate.
//
// English (en) is the source of truth. Every other locale's keys must be a
// SUBSET of en's: a key present in a locale but ABSENT from en signals a
// structural bug — almost always a brace mis-nesting that re-parents a whole
// block (e.g. `explorer.text` landing under `explorer.flags`), which silently
// drops those strings to the English fallback. This test fails on any such
// "extra" key. Missing keys are allowed by design (t() falls back to en); we
// report their counts for visibility but do not fail on them.
import { describe, it, expect } from 'vitest';
import en from '../src/lib/i18n/locales/en';
import ar from '../src/lib/i18n/locales/ar';
import crk from '../src/lib/i18n/locales/crk';
import de from '../src/lib/i18n/locales/de';
import es from '../src/lib/i18n/locales/es';
import fr from '../src/lib/i18n/locales/fr';
import hi from '../src/lib/i18n/locales/hi';
import ko from '../src/lib/i18n/locales/ko';
import pa from '../src/lib/i18n/locales/pa';
import pdt from '../src/lib/i18n/locales/pdt';
import pl from '../src/lib/i18n/locales/pl';
import ru from '../src/lib/i18n/locales/ru';
import so from '../src/lib/i18n/locales/so';
import tl from '../src/lib/i18n/locales/tl';
import uk from '../src/lib/i18n/locales/uk';
import ur from '../src/lib/i18n/locales/ur';
import vi from '../src/lib/i18n/locales/vi';
import zhHans from '../src/lib/i18n/locales/zh-Hans';
import zhHant from '../src/lib/i18n/locales/zh-Hant';

const LOCALES: Record<string, unknown> = {
	ar, crk, de, es, fr, hi, ko, pa, pdt, pl, ru, so, tl, uk, ur, vi,
	'zh-Hans': zhHans,
	'zh-Hant': zhHant,
};

function flatten(obj: unknown, prefix = '', out = new Set<string>()): Set<string> {
	if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
		for (const [k, v] of Object.entries(obj as Record<string, unknown>)) {
			flatten(v, prefix ? `${prefix}.${k}` : k, out);
		}
	} else {
		out.add(prefix);
	}
	return out;
}

const enKeys = flatten(en);

describe('i18n key parity (no key may exist outside en)', () => {
	for (const [code, dict] of Object.entries(LOCALES)) {
		it(`${code}: has no keys absent from en`, () => {
			const keys = flatten(dict);
			const extra = [...keys].filter((k) => !enKeys.has(k)).sort();
			const missing = [...enKeys].filter((k) => !keys.has(k)).length;
			// Visibility only — missing keys fall back to en by design.
			if (missing) console.info(`[i18n] ${code}: ${missing} keys fall back to en`);
			expect(extra, `${code} has ${extra.length} key(s) not in en (structural mis-nesting?): ${extra.join(', ')}`).toEqual([]);
		});
	}
});
