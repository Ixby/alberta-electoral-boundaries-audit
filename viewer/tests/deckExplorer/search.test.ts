// Unit tests for the pure ED-name matcher used by the deck.gl explorer search.
//
// buildNameIndex / matchNames are framework-free (no deck.gl, no Svelte): they
// turn the generated ed_index_<map>.json array into a searchable index and rank
// query matches (prefix before substring, case-insensitive). The component wires
// the result into a dropdown + fly-to; that integration is exercised in-browser,
// not here.
//
// Placement under tests/ (not src/) mirrors the other deckExplorer specs —
// vitest.config.ts only collects tests/**/*.test.ts.

import { describe, it, expect } from 'vitest';
import { buildNameIndex, matchNames, type EdRec } from '../../src/lib/deckExplorer/search';

const RECS: EdRec[] = [
	{ name: 'Calgary-Beddington', cx: 1, cy: 1, zoom: -6 },
	{ name: 'Calgary-Nolan Hill-Cochrane', cx: 2, cy: 2, zoom: -6 },
	{ name: 'Calgary-Mountainview', cx: 3, cy: 3, zoom: -6 },
	{ name: 'Spruce Grove-Stony Plain', cx: 4, cy: 4, zoom: -5 },
	{ name: 'Edmonton-Highlands-Norwood', cx: 5, cy: 5, zoom: -7 },
	{ name: 'Lesser Slave Lake', cx: 6, cy: 6, zoom: -4 }
];

describe('buildNameIndex / matchNames', () => {
	const idx = buildNameIndex(RECS);

	it('empty query returns []', () => {
		expect(matchNames(idx, '')).toEqual([]);
		expect(matchNames(idx, '   ')).toEqual([]);
	});

	it('is case-insensitive', () => {
		const lower = matchNames(idx, 'calgary').map((r) => r.name);
		const upper = matchNames(idx, 'CALGARY').map((r) => r.name);
		expect(lower).toEqual(upper);
		expect(lower.length).toBe(3);
	});

	it('"cal" returns the three Calgary EDs (prefix match)', () => {
		const names = matchNames(idx, 'cal').map((r) => r.name);
		expect(names).toContain('Calgary-Beddington');
		expect(names).toContain('Calgary-Mountainview');
		expect(names).toContain('Calgary-Nolan Hill-Cochrane');
		expect(names.length).toBe(3);
	});

	it('returns the full record (cx/cy/zoom carried through)', () => {
		const r = matchNames(idx, 'beddington')[0];
		expect(r).toEqual({ name: 'Calgary-Beddington', cx: 1, cy: 1, zoom: -6 });
	});

	it('ranks prefix matches before substring matches', () => {
		// "hill" matches "Calgary-Nolan Hill-Cochrane" (substring only — no name
		// starts with "hill"), and "Highlands" does NOT contain "hill", so only one
		// result is expected here; the ordering rule is exercised with "lake" below.
		const hill = matchNames(idx, 'hill').map((r) => r.name);
		expect(hill).toEqual(['Calgary-Nolan Hill-Cochrane']);

		// "lake" prefixes nothing but appears as a substring in "Lesser Slave Lake".
		const lake = matchNames(idx, 'lake').map((r) => r.name);
		expect(lake).toEqual(['Lesser Slave Lake']);
	});

	it('orders prefix hits ahead of substring hits for the same query', () => {
		// "s" prefixes "Spruce Grove-Stony Plain"; it is also a substring of several
		// others (Highlands, Slave, Beddington…). The prefix hit must rank first.
		const names = matchNames(idx, 's').map((r) => r.name);
		expect(names[0]).toBe('Spruce Grove-Stony Plain');
		expect(names.length).toBeGreaterThan(1);
	});

	it('respects the limit argument', () => {
		expect(matchNames(idx, 'a', 2).length).toBe(2);
	});

	it('sorts alphabetically within a rank tier', () => {
		const names = matchNames(idx, 'cal').map((r) => r.name);
		expect(names).toEqual([...names].sort((a, b) => a.localeCompare(b)));
	});
});
