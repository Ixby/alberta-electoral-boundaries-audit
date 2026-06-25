// Property tests for serializeState → parseState round-trip with state
// shapes that match what the deck explorer actually produces.
//
// The URL share is self-contained and lossless to 4-dp on the viewport, so
// primary, mapOn, and layers MUST survive intact, and the viewport must
// round-trip within float tolerance.

import { describe, it, expect } from 'vitest';
import { serializeState, parseState } from '../src/lib/share';
import type { MapState } from '../src/lib/share';

const baseViewport = { cx_norm: 0.5, cy_norm: 0.5, zoom: 0.7 };

function mk(overrides: Partial<MapState> = {}): MapState {
	return {
		primary: 'minority',
		mapOn: { minority: true, majority: false, '2019': false },
		layers: { hwy: true, water: false, pois: true },
		viewport: { ...baseViewport },
		...overrides
	};
}

function back(s: MapState): MapState {
	const r = parseState(new URLSearchParams(serializeState(s)));
	expect(r).not.toBeNull();
	return r!;
}

describe('serialize → parse round-trip', () => {
	it('preserves primary across all three maps', () => {
		for (const primary of ['minority', 'majority', '2019'] as const) {
			const s = mk({ primary, mapOn: { minority: true, majority: true, '2019': true } });
			expect(back(s).primary).toBe(primary);
		}
	});

	it('preserves the mapOn bits of the two non-primary maps', () => {
		const states: Array<MapState['mapOn']> = [
			{ minority: true, majority: false, '2019': false },
			{ minority: true, majority: true, '2019': false },
			{ minority: true, majority: false, '2019': true },
			{ minority: true, majority: true, '2019': true }
		];
		for (const mapOn of states) {
			expect(back(mk({ mapOn })).mapOn).toEqual(mapOn);
		}
	});

	it('preserves all 8 layer combinations', () => {
		for (let i = 0; i < 8; i++) {
			const layers = { hwy: !!(i & 1), water: !!(i & 2), pois: !!(i & 4) };
			expect(back(mk({ layers })).layers).toEqual(layers);
		}
	});

	it('round-trips the viewport within 4-dp tolerance', () => {
		const s = mk({ viewport: { cx_norm: 0.4242, cy_norm: 0.7878, zoom: 0.7 } });
		const r = back(s);
		expect(r.viewport.cx_norm).toBeCloseTo(0.4242, 3);
		expect(r.viewport.cy_norm).toBeCloseTo(0.7878, 3);
		expect(r.viewport.zoom).toBeCloseTo(0.7, 3);
	});
});

describe('parseState rejects malformed queries', () => {
	it('rejects a query with no `m`', () => {
		expect(parseState(new URLSearchParams('f=hwy'))).toBeNull();
	});

	it('rejects an `m` with only unknown tokens', () => {
		expect(parseState(new URLSearchParams('m=xxxx,yyyy'))).toBeNull();
	});
});
