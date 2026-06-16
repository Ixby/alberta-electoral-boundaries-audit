// CI gate: no retired statistical figures may appear in any locale file.
//
// Background: the Fisher combined p-value 6.87×10⁻⁸ and its plain-language
// derivations ("1 in 14.5 million", "1 in 15 million", and translations) were
// retired and replaced by the dependence-robust Bonferroni bound p ≤ 2.80×10⁻⁶
// (~1 in 350,000). This test is the permanent gate ensuring the retired figures
// never ship again.
//
// Scope: every src/lib/i18n/locales/*.ts file (not _wip/ partials).
// On failure: the assertion message includes the file name and ~80 chars of
// context around each match so the fix is immediately actionable.

import { describe, it, expect } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const LOCALES_DIR = join(__dirname, '..', 'src', 'lib', 'i18n', 'locales');

// Patterns that must NOT appear in any locale file.
// All are case-insensitive to catch capitalisation variants.
const FORBIDDEN: Array<{ label: string; re: RegExp }> = [
	// Fisher p-value in either decimal-separator convention
	{ label: 'Fisher p=6.87e-8', re: /6[.,]87/i },

	// "14.5 million" variants (plain-language form of the old Fisher figure)
	{
		label: '14.5-million variants',
		re: /14[.,]5\s*(million|milyan|millionen|millones|milh[oõ]es|миллион|miljoen|mill?i[oó]n[e]?|milion)/i,
	},

	// "1 in 14.5 million" shorthand with no unit word (e.g. "14,5 Milljon" in pdt)
	{ label: '14.5 bare', re: /14[.,]5\s*Mill/i },

	// "15 million" variants across all live languages
	{
		label: '15-million variants',
		re: /\b15\s*(million|milyan|millionen|millones|milh[oõ]es|миллион|miljoen|mill?i[oó]n[e]?|milion)/i,
	},

	// Fisher bare reference: "Fisher … 6.87" or "Fisher … ×10" within 40 chars
	{ label: 'Fisher bare reference', re: /Fisher[^.]{0,40}(6[.,]87|×\s*10)/i },
];

function surroundingContext(source: string, index: number, radius = 80): string {
	const start = Math.max(0, index - radius);
	const end = Math.min(source.length, index + radius);
	const prefix = start > 0 ? '…' : '';
	const suffix = end < source.length ? '…' : '';
	return prefix + source.slice(start, end) + suffix;
}

function findViolations(
	source: string,
	filename: string,
): Array<{ file: string; label: string; context: string }> {
	const violations: Array<{ file: string; label: string; context: string }> = [];
	for (const { label, re } of FORBIDDEN) {
		// Use global flag clone to find all matches
		const globalRe = new RegExp(re.source, re.flags.includes('g') ? re.flags : re.flags + 'g');
		let m: RegExpExecArray | null;
		while ((m = globalRe.exec(source)) !== null) {
			violations.push({
				file: filename,
				label,
				context: surroundingContext(source, m.index),
			});
		}
	}
	return violations;
}

describe('no retired statistical figures in locale files', () => {
	// Read locale files at test execution time (not import time) so the list
	// stays up to date without touching this test when locales are added.
	const localeFiles = readdirSync(LOCALES_DIR)
		.filter((f) => f.endsWith('.ts') && !f.startsWith('_'))
		.sort();

	it('locale directory is non-empty (sanity check)', () => {
		expect(localeFiles.length).toBeGreaterThan(0);
	});

	it('no locale file contains a retired figure', () => {
		const allViolations: Array<{ file: string; label: string; context: string }> = [];

		for (const filename of localeFiles) {
			const filepath = join(LOCALES_DIR, filename);
			const source = readFileSync(filepath, 'utf-8');
			allViolations.push(...findViolations(source, filename));
		}

		if (allViolations.length > 0) {
			const report = allViolations
				.map((v) => `\n  [${v.file}] pattern="${v.label}"\n    context: ${v.context}`)
				.join('\n');
			expect.fail(
				`Found ${allViolations.length} retired-figure occurrence(s) across locale files:${report}\n\n` +
					`Retired figures (FORBIDDEN on the public site):\n` +
					`  - Fisher p=6.87×10⁻⁸\n` +
					`  - "1 in 14.5 million" / "14.5 million" and translations\n` +
					`  - "1 in 15 million" and translations\n\n` +
					`Replace with: p ≤ 2.80×10⁻⁶ / "approximately 1 in 350,000"`,
			);
		}
	});
});
