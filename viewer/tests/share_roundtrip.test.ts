// Property tests for encodeState → decodeState roundtrip with state
// shapes that match what the engine actually produces.
//
// The share-code space is a lossy 19,200-state hash (3-word code), so
// exact roundtrip isn't expected for viewport — but primary, mapOn, and
// layers MUST survive intact because those are the user-visible state
// the share-link is meant to capture.

import { describe, it, expect } from 'vitest';
import { encodeState, decodeState } from '../src/lib/share';
import type { MapState } from '../src/lib/share';

const baseViewport = { cx_norm: 0.5, cy_norm: 0.5, zoom: 0.7 };

function mk(overrides: Partial<MapState> = {}): MapState {
	return {
		primary: 'minority',
		mapOn: { minority: true, majority: false, '2019': false },
		layers: { vote: true, 'ed-fill': false, 'ed-lines': true, eg: false },
		viewport: { ...baseViewport },
		...overrides,
	};
}

describe('encode → decode roundtrip', () => {
	it('preserves primary across all three maps', () => {
		for (const primary of ['minority', 'majority', '2019'] as const) {
			const s = mk({ primary, mapOn: { minority: true, majority: true, '2019': true } });
			const code = encodeState(s);
			expect(code).not.toBeNull();
			const back = decodeState(code!);
			expect(back?.primary).toBe(primary);
		}
	});

	it('preserves the mapOn bits of the two non-primary maps', () => {
		const states: Array<Partial<MapState>['mapOn']> = [
			{ minority: true, majority: false, '2019': false },
			{ minority: true, majority: true,  '2019': false },
			{ minority: true, majority: false, '2019': true  },
			{ minority: true, majority: true,  '2019': true  },
		];
		for (const mapOn of states) {
			const s = mk({ mapOn: mapOn as Record<'minority' | 'majority' | '2019', boolean> });
			const back = decodeState(encodeState(s)!);
			expect(back?.mapOn).toEqual(s.mapOn);
		}
	});

	it('preserves all 16 layer bit combinations', () => {
		for (let i = 0; i < 16; i++) {
			const s = mk({
				layers: {
					vote:       !!(i & 1),
					'ed-fill':  !!(i & 2),
					'ed-lines': !!(i & 4),
					eg:         !!(i & 8),
				},
			});
			const back = decodeState(encodeState(s)!);
			expect(back?.layers).toEqual(s.layers);
		}
	});

	it('viewport is quantized but the decoded centre lies inside the same 5×5 cell', () => {
		const s = mk({ viewport: { cx_norm: 0.42, cy_norm: 0.78, zoom: 0.7 } });
		const back = decodeState(encodeState(s)!);
		// 0.42 lies in column 2 (range 0.4..0.6) → bucket centre 0.5
		// 0.78 lies in row 3 (range 0.6..0.8) → bucket centre 0.7
		expect(back?.viewport.cx_norm).toBeCloseTo(0.5, 6);
		expect(back?.viewport.cy_norm).toBeCloseTo(0.7, 6);
	});
});

describe('decode rejects malformed codes', () => {
	it('rejects unknown words', () => {
		expect(decodeState('xxxx-yyyy-zzzz')).toBeNull();
	});

	it('rejects fewer than three tokens', () => {
		expect(decodeState('abc-def')).toBeNull();
	});

	it('rejects more than three tokens', () => {
		expect(decodeState('abc-def-ghi-jkl')).toBeNull();
	});

	it('is case-insensitive on input', () => {
		const s = mk();
		const code = encodeState(s)!;
		const upper = decodeState(code.toUpperCase());
		const lower = decodeState(code.toLowerCase());
		expect(upper).not.toBeNull();
		expect(lower).not.toBeNull();
		expect(upper?.primary).toBe(s.primary);
	});
});
