// Alberta Electoral Boundary Audit — live prose word count
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Computed once at module load from the actual English dictionary so the
// number volunteers see never goes stale as the prose grows. Rounded to
// the nearest 500 — it's a scale signal, not an invoice. Shared by the
// top-of-page translation disclaimer and the about-this-translation
// section at the bottom.

import en from './locales/en';

function countWords(node: unknown): number {
	if (typeof node === 'string') {
		return node
			.replace(/<[^>]+>/g, ' ')
			.replace(/&[a-z#0-9]+;/gi, ' ')
			.split(/\s+/)
			.filter(Boolean).length;
	}
	if (node && typeof node === 'object') {
		return Object.values(node as Record<string, unknown>).reduce(
			(sum: number, v) => sum + countWords(v),
			0
		);
	}
	return 0;
}

export const proseWordCount = Math.round(countWords(en) / 500) * 500;
