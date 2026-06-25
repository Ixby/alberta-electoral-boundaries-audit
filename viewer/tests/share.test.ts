// Tests for src/lib/share.ts — serializeState / parseState URL round-trip.
//
// The share state is now packed into a URL query string (self-contained, no
// DB resolution). Properties to lock down:
//   1. serialize → parse round-trips primary, mapOn, and layers EXACTLY.
//   2. The viewport (normalised 0..1 floats) round-trips to 4-dp precision.
//   3. parseState rejects a missing/invalid `m` key (returns null).
//   4. Out-of-range viewport values clamp to [0, 1]; missing ones default to 0.5.

import { describe, it, expect } from 'vitest';
import { serializeState, parseState, type MapState } from '../src/lib/share';

const validState = (overrides: Partial<MapState> = {}): MapState => ({
	primary: 'majority',
	mapOn: { majority: true, minority: false, '2019': false },
	layers: { hwy: true, water: false, pois: true },
	viewport: { cx_norm: 0.5, cy_norm: 0.5, zoom: 0.5 },
	...overrides
});

function roundTrip(s: MapState): MapState {
	const back = parseState(new URLSearchParams(serializeState(s)));
	expect(back).not.toBeNull();
	return back!;
}

describe('serializeState() — packing a map state into a URL query', () => {
	it('produces a query string with the required `m` key', () => {
		const q = serializeState(validState());
		const p = new URLSearchParams(q);
		expect(p.get('m')).toBe('majority');
	});

	it('lists active overlay filters in `f`, primary map first in `m`', () => {
		const q = serializeState(
			validState({
				primary: 'minority',
				mapOn: { minority: true, majority: true, '2019': false },
				layers: { hwy: false, water: true, pois: true }
			})
		);
		const p = new URLSearchParams(q);
		expect(p.get('m')).toBe('minority,majority');
		expect(p.get('f')).toBe('water,pois');
	});

	it('omits `f` entirely when no overlay filter is on', () => {
		const q = serializeState(validState({ layers: { hwy: false, water: false, pois: false } }));
		expect(new URLSearchParams(q).has('f')).toBe(false);
	});
});

describe('parseState() — reading a query back to map state', () => {
	it('returns null when `m` is absent', () => {
		expect(parseState(new URLSearchParams(''))).toBeNull();
		expect(parseState(new URLSearchParams('f=hwy&cx=0.5'))).toBeNull();
	});

	it('returns null when `m` contains no recognised map key', () => {
		expect(parseState(new URLSearchParams('m=bogus,liberal'))).toBeNull();
	});

	it('clamps out-of-range viewport values into [0, 1]', () => {
		const back = parseState(new URLSearchParams('m=minority&cx=9&cy=-9&z=2'))!;
		expect(back.viewport.cx_norm).toBe(1);
		expect(back.viewport.cy_norm).toBe(0);
		expect(back.viewport.zoom).toBe(1);
	});

	it('defaults missing viewport params to the 0.5 centre', () => {
		const back = parseState(new URLSearchParams('m=2019'))!;
		expect(back.viewport.cx_norm).toBe(0.5);
		expect(back.viewport.cy_norm).toBe(0.5);
		expect(back.viewport.zoom).toBe(0.5);
	});
});

describe('serializeState → parseState round-trip', () => {
	const primaries = ['minority', 'majority', '2019'] as const;

	for (const primary of primaries) {
		it(`preserves primary=${primary} and its mapOn flag`, () => {
			const back = roundTrip(
				validState({ primary, mapOn: { minority: false, majority: false, '2019': false, [primary]: true } as never })
			);
			expect(back.primary).toBe(primary);
			expect(back.mapOn[primary]).toBe(true);
		});
	}

	it('preserves every mapOn combination of the two non-primary maps', () => {
		const cases = [
			[false, false],
			[true, false],
			[false, true],
			[true, true]
		] as const;
		for (const [a, b] of cases) {
			const back = roundTrip(
				validState({ primary: 'minority', mapOn: { minority: true, majority: a, '2019': b } })
			);
			expect(back.mapOn.majority).toBe(a);
			expect(back.mapOn['2019']).toBe(b);
		}
	});

	it('preserves all 8 layer combinations exactly', () => {
		for (let bits = 0; bits < 8; bits++) {
			const layers = { hwy: !!(bits & 1), water: !!(bits & 2), pois: !!(bits & 4) };
			const back = roundTrip(validState({ layers }));
			expect(back.layers).toEqual(layers);
		}
	});

	it('preserves the viewport to 4-dp precision', () => {
		const back = roundTrip(validState({ viewport: { cx_norm: 0.1234, cy_norm: 0.8765, zoom: 0.4321 } }));
		expect(back.viewport.cx_norm).toBeCloseTo(0.1234, 3);
		expect(back.viewport.cy_norm).toBeCloseTo(0.8765, 3);
		expect(back.viewport.zoom).toBeCloseTo(0.4321, 3);
	});
});
