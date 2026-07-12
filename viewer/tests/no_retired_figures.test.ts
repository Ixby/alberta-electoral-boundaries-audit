// CI gate: no retired statistical figures may appear in any locale file.
//
// Background: The Fisher combined p-value 6.87×10⁻⁸ and its plain-language
// derivations ("1 in 14.5 million", "1 in 15 million") were retired in 2026-06-10
// and replaced by the dependence-robust Bonferroni bound p ≤ 2.80×10⁻⁶ (~1 in 350,000).
// Following the MCMC ensemble rerun on 2026-07-12, that Bonferroni bound was itself
// retired and replaced by p ≤ 1.76×10⁻⁶ (~1 in 568,000). This test is the permanent
// gate ensuring all retired figures never ship again.
//
// Scope: every src/lib/i18n/locales/*.ts file (not _wip/ partials) for the
// Fisher-era patterns, which were synced across all 19 locales back in
// 2026-06-10. The 2026-07-12 Bonferroni-figure patterns are checked in en.ts
// ONLY for now: the author deliberately held the other 18 locale files back
// pending his own edit pass on the casings text (translations paused until
// the English source is locked), so those files still legitimately contain
// the pre-2026-07-12 figures. Move ALL_LOCALES_FORBIDDEN entries into
// EN_ONLY_FORBIDDEN's counterpart list — i.e. promote them back to
// all-locale scope — once the 18 locales are resynced; don't leave this
// split in place indefinitely.
// On failure: the assertion message includes the file name and ~80 chars of
// context around each match so the fix is immediately actionable.

import { describe, it, expect } from 'vitest';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const LOCALES_DIR = join(__dirname, '..', 'src', 'lib', 'i18n', 'locales');

// Patterns that must NOT appear in ANY locale file (fully synced across all
// 19 locales since the 2026-06-10 Fisher retirement).
// All are case-insensitive to catch capitalisation variants.
const ALL_LOCALES_FORBIDDEN: Array<{ label: string; re: RegExp }> = [
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

// Patterns retired by the 2026-07-12 MCMC ensemble rerun. EN-ONLY until the
// other 18 locales are resynced (see file header note above).
const EN_ONLY_FORBIDDEN: Array<{ label: string; re: RegExp }> = [
	{ label: 'Bonferroni p=2.80e-6', re: /2[.,]80\s*×\s*10[⁻-]6/i },
	{ label: 'Bonferroni p=2.8e-6', re: /2[.,]8\s*×\s*10[⁻-]6/i },
	{ label: 'Old verbal 357,000', re: /357[.,]?000/i },
	{ label: 'Old verbal 350,000', re: /\b350[.,]?000\b/i },
	{ label: 'Ch1 parametric p=1.40e-6', re: /1[.,]40\s*×\s*10[⁻-]6/i },
	{ label: 'Old Mahalanobis D² 32.67', re: /32[.,]6[67](?![0-9])/i },
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
	patterns: Array<{ label: string; re: RegExp }>,
): Array<{ file: string; label: string; context: string }> {
	const violations: Array<{ file: string; label: string; context: string }> = [];
	for (const { label, re } of patterns) {
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

	it('no locale file contains a Fisher-era retired figure', () => {
		const allViolations: Array<{ file: string; label: string; context: string }> = [];

		for (const filename of localeFiles) {
			const filepath = join(LOCALES_DIR, filename);
			const source = readFileSync(filepath, 'utf-8');
			allViolations.push(...findViolations(source, filename, ALL_LOCALES_FORBIDDEN));
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
					`  - "1 in 15 million" and translations`,
			);
		}
	});

	it('en.ts contains no pre-2026-07-12 Bonferroni figure', () => {
		const filepath = join(LOCALES_DIR, 'en.ts');
		const source = readFileSync(filepath, 'utf-8');
		const violations = findViolations(source, 'en.ts', EN_ONLY_FORBIDDEN);

		if (violations.length > 0) {
			const report = violations
				.map((v) => `\n  [${v.file}] pattern="${v.label}"\n    context: ${v.context}`)
				.join('\n');
			expect.fail(
				`Found ${violations.length} retired-figure occurrence(s) in en.ts:${report}\n\n` +
					`Replace with: p ≤ 1.76×10⁻⁶ / "about one in 568,000"`,
			);
		}
	});
});
