// Gate: the "casings, not a smoking gun" metaphor is retired (author, 2026-11-07: "we're not using
// casings as a metaphor anymore", "globally"). The public report and the English site text must not
// bring it back. Internal identifiers stay: the `casings` key group, the `smoking_gun` key, the
// `beat_gun` key and the #casing-N anchors are kept so other locales and shared links keep working.
// The other 18 locale files are out of scope until translations are redone (author: "translations can
// happen later"); add them here when they are.

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const EN = join(__dirname, '..', 'src', 'lib', 'i18n', 'locales', 'en.ts');
const REPORT = join(__dirname, '..', '..', 'reports', 'public', 'report_public.md');

const FORBIDDEN = /\bcasings?\b|smoking gun|\bthe gun\b|\ba gun\b|no gun\b/gi;
// Identifiers, not reader-facing words.
const ALLOWED = [/evidence#casing-\d+/g, /\bcasings: \{/g, /\bsmoking_gun:/g, /\bbeat_gun:/g];

function offenders(text: string): string[] {
	let t = text;
	for (const re of ALLOWED) t = t.replace(re, '');
	const out: string[] = [];
	for (const m of t.matchAll(FORBIDDEN)) {
		const i = m.index ?? 0;
		out.push(t.slice(Math.max(0, i - 40), i + 40).replace(/\s+/g, ' '));
	}
	return out;
}

describe('casing metaphor retired', () => {
	it('is absent from the English site text', () => {
		expect(offenders(readFileSync(EN, 'utf8'))).toEqual([]);
	});
	it('is absent from the public report', () => {
		expect(offenders(readFileSync(REPORT, 'utf8'))).toEqual([]);
	});
});
