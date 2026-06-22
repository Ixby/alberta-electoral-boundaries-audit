// Unit tests for the pure grouping logic of the deck.gl explorer layer builder.
//
// Only `groupsFor` is unit-tested here: it is the framework-free agreement logic
// (which subset of active maps each boundary segment is shared by) and the piece
// that broke and was fixed this session. The layer-building functions in
// layers.ts take injected deck.gl classes and produce layer instances; they need
// a browser/deck.gl env and are exercised by the Svelte integration, not here.
//
// Placement: under tests/ (not co-located in src/) because vitest.config.ts
// restricts the include glob to tests/**/*.test.ts — same as loader.test.ts.

import { describe, it, expect } from 'vitest';
import { groupsFor, MAPS, type Edge } from '../../src/lib/deckExplorer/layers';

// MAPS order is ['minority','majority','2019']; `m` is one-hot/multi-hot over
// that index. Edge 4 (2019-only) is present to exercise the "no active map" drop.
const EDGES: Edge[] = [
	{ g: [[0, 0]], m: [1, 0, 0] }, // minority only
	{ g: [[1, 1]], m: [1, 1, 0] }, // minority + majority
	{ g: [[2, 2]], m: [1, 1, 1] }, // all three
	{ g: [[3, 3]], m: [0, 0, 1] } // 2019 only
];

describe('groupsFor', () => {
	it('MAPS is in canonical order', () => {
		expect(MAPS).toEqual(['minority', 'majority', '2019']);
	});

	it('groups edges by the subset of active maps that share them', () => {
		const groups = groupsFor(['minority', 'majority'], EDGES);
		const byKey = Object.fromEntries(groups.map((grp) => [grp.key, grp]));

		// With 2019 inactive, the all-three edge collapses to minority+majority,
		// so exactly two groups exist (the 2019-only edge is dropped entirely).
		expect(Object.keys(byKey).sort()).toEqual(['minority', 'minority+majority']);
		expect(groups.length).toBe(2);

		expect(byKey['minority'].mks).toEqual(['minority']);
		expect(byKey['minority'].list).toEqual([EDGES[0]]);

		expect(byKey['minority+majority'].mks).toEqual(['minority', 'majority']);
		expect(byKey['minority+majority'].list).toEqual([EDGES[1], EDGES[2]]);
	});

	it('drops edges that share no active map', () => {
		// Only 2019 active → the minority-only and minority+majority edges drop;
		// both the all-three and the 2019-only edge land in the single "2019" group.
		const groups = groupsFor(['2019'], EDGES);
		expect(groups.length).toBe(1);
		expect(groups[0].key).toBe('2019');
		expect(groups[0].list).toEqual([EDGES[2], EDGES[3]]);
	});

	it('returns no groups when nothing is active', () => {
		expect(groupsFor([], EDGES)).toEqual([]);
	});

	it('keys preserve the order maps are passed in', () => {
		// The key is mks.join('+'), preserving the activeMaps argument order; the
		// caller is responsible for passing maps in MAPS order.
		const groups = groupsFor(['majority', 'minority'], EDGES);
		const keys = groups.map((grp) => grp.key);
		expect(keys).toContain('majority+minority');
	});
});
