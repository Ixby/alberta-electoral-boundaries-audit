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
import { groupsFor, chunkPath, MAPS, type Edge } from '../../src/lib/deckExplorer/layers';

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

// chunkPath subdivides an agreement edge's polyline into fixed-length sub-polylines
// for the alternating-colour dash. Each chunk gets an incrementing colorIdx the
// caller maps to one of the N agreeing maps' colours via colorIdx % N.
describe('chunkPath', () => {
	it('subdivides a straight 100-unit line into ~10 chunks with incrementing colorIdx', () => {
		const line: [number, number][] = [
			[0, 0],
			[100, 0]
		];
		const chunks = chunkPath(line, 10, 0);
		expect(chunks.length).toBe(10);
		// colorIdx is 0,1,2,…,9 in order.
		expect(chunks.map((c) => c.colorIdx)).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
		// First chunk spans [0,0]→[10,0]; last ends at the path end.
		expect(chunks[0].coords[0]).toEqual([0, 0]);
		expect(chunks[0].coords[chunks[0].coords.length - 1][0]).toBeCloseTo(10, 6);
		expect(chunks[9].coords[chunks[9].coords.length - 1][0]).toBeCloseTo(100, 6);
		// Total covered length equals the line length (no gap).
		const covered = chunks.reduce((sum, c) => sum + segLen(c.coords), 0);
		expect(covered).toBeCloseTo(100, 4);
	});

	it('gapFrac>0 reduces coverage to 1/(1+gapFrac)', () => {
		const line: [number, number][] = [
			[0, 0],
			[100, 0]
		];
		const chunks = chunkPath(line, 10, 1); // dash 10, gap 10 → 50% coverage
		const covered = chunks.reduce((sum, c) => sum + segLen(c.coords), 0);
		// ~50 units covered out of 100 (allow slack for the trailing partial period).
		expect(covered).toBeGreaterThan(45);
		expect(covered).toBeLessThan(55);
		// Each chunk is at most dashLen long.
		for (const c of chunks) expect(segLen(c.coords)).toBeLessThanOrEqual(10 + 1e-6);
	});

	it('follows bends: a chunk spanning a right angle carries the corner vertex', () => {
		// L-shaped path: 6 units east, then 6 units north. A 100-unit dashLen spans
		// the whole L in one chunk, which must include the corner (6,0).
		const ell: [number, number][] = [
			[0, 0],
			[6, 0],
			[6, 6]
		];
		const chunks = chunkPath(ell, 100, 0);
		expect(chunks.length).toBe(1);
		// The single chunk preserves the corner vertex — not a straight chord.
		expect(chunks[0].coords).toEqual([
			[0, 0],
			[6, 0],
			[6, 6]
		]);
		// Its length is the full polyline length (12), not the chord (~8.49).
		expect(segLen(chunks[0].coords)).toBeCloseTo(12, 6);
	});

	it('a short dashLen across a bend splits at the corner and interpolates', () => {
		// dashLen 4 on a 6+6 L: first chunk [0,0]→[4,0]; a later chunk straddles the
		// corner, so it must contain the corner vertex (6,0) between its endpoints.
		const ell: [number, number][] = [
			[0, 0],
			[6, 0],
			[6, 6]
		];
		const chunks = chunkPath(ell, 4, 0);
		// Total covered length ≈ 12 (full polyline), every chunk ≤ 4 long.
		const covered = chunks.reduce((sum, c) => sum + segLen(c.coords), 0);
		expect(covered).toBeCloseTo(12, 4);
		for (const c of chunks) expect(segLen(c.coords)).toBeLessThanOrEqual(4 + 1e-6);
		// The chunk that crosses the corner contains (6,0) as an interior vertex.
		const straddles = chunks.some((c) =>
			c.coords.some((p, idx) => idx > 0 && idx < c.coords.length - 1 && p[0] === 6 && p[1] === 0)
		);
		expect(straddles).toBe(true);
	});

	it('maxChunks caps the chunk count (guards against deep-zoom explosion)', () => {
		const line: [number, number][] = [
			[0, 0],
			[10000, 0]
		];
		// dashLen 1 would give 10000 chunks; cap at 50.
		const chunks = chunkPath(line, 1, 0, 50);
		expect(chunks.length).toBeLessThanOrEqual(50);
		// The capped final chunk runs to the end so the line stays continuous.
		const last = chunks[chunks.length - 1].coords;
		expect(last[last.length - 1][0]).toBeCloseTo(10000, 6);
	});

	it('returns [] for degenerate input', () => {
		expect(chunkPath([], 10, 0)).toEqual([]);
		expect(chunkPath([[0, 0]], 10, 0)).toEqual([]);
		expect(
			chunkPath(
				[
					[0, 0],
					[10, 0]
				],
				0,
				0
			)
		).toEqual([]);
	});
});

/** Sum of segment lengths of a polyline (test helper). */
function segLen(coords: [number, number][]): number {
	let s = 0;
	for (let i = 1; i < coords.length; i++) {
		const dx = coords[i][0] - coords[i - 1][0];
		const dy = coords[i][1] - coords[i - 1][1];
		s += Math.sqrt(dx * dx + dy * dy);
	}
	return s;
}
