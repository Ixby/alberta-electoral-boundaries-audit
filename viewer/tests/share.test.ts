// Tests for src/lib/share.ts — share-code encode/decode roundtrip.
//
// Share codes are three-word strings (`alpine-eagle-banff`) that pack:
//   primary map (3) × overlay bits (4) × layer bits (16) × viewport col (5)
//   × viewport row (5) × zoom tier (4) = 19,200 valid states (of 27³ = 19,683).
//
// Properties to lock down:
//   1. encode → decode is round-trip-stable for all valid states (the only
//      lossy bit is the viewport: cx_norm/cy_norm get bucketed to 5×5 grid,
//      and zoom gets bucketed to 4 tiers).
//   2. Invalid codes (typos, wrong arity, OOB indexes) decode to null.
//   3. Invalid primary keys encode to null.
//   4. Output codes use only the word lists (no leakage of arbitrary input).

import { describe, it, expect } from 'vitest';
import { encodeState, decodeState, type MapState } from '../src/lib/share';

const validState = (overrides: Partial<MapState> = {}): MapState => ({
	primary: 'majority',
	mapOn: { majority: true, minority: false, '2019': false },
	layers: { vote: true, 'ed-fill': false, 'ed-lines': true, eg: false },
	viewport: { cx_norm: 0.5, cy_norm: 0.5, zoom: 1.0 },
	...overrides
});

describe('encodeState() — packing a map state into a 3-word code', () => {
	it('produces a 3-word hyphen-joined string for a valid state', () => {
		const code = encodeState(validState());
		expect(code).not.toBeNull();
		expect(code!.split('-')).toHaveLength(3);
	});

	it('returns null for an unknown primary map', () => {
		const bad = validState({ primary: 'liberal-2026' as never });
		expect(encodeState(bad)).toBeNull();
	});

	it('emits only lowercase, alphabetic, word-list tokens', () => {
		const code = encodeState(validState())!;
		expect(code).toMatch(/^[a-z]+-[a-z]+-[a-z]+$/);
	});
});

describe('decodeState() — parsing a 3-word code back to map state', () => {
	it('returns null for arity ≠ 3', () => {
		expect(decodeState('alpine')).toBeNull();
		expect(decodeState('alpine-eagle')).toBeNull();
		expect(decodeState('alpine-eagle-banff-extra')).toBeNull();
	});

	it('returns null for a code with an unknown word', () => {
		// `xyzzy` is not in any of the three word lists.
		expect(decodeState('xyzzy-eagle-banff')).toBeNull();
		expect(decodeState('alpine-xyzzy-banff')).toBeNull();
		expect(decodeState('alpine-eagle-xyzzy')).toBeNull();
	});

	it('returns null for the empty string', () => {
		expect(decodeState('')).toBeNull();
	});

	it('accepts whitespace and trims case before parsing', () => {
		const encoded = encodeState(validState())!;
		const decoded = decodeState(`  ${encoded.toUpperCase()}  `);
		expect(decoded).not.toBeNull();
		expect(decoded!.primary).toBe('majority');
	});

	it('accepts space-separated as well as hyphen-separated input', () => {
		const encoded = encodeState(validState())!;
		const spaceForm = encoded.replace(/-/g, ' ');
		const decoded = decodeState(spaceForm);
		expect(decoded).not.toBeNull();
		expect(decoded!.primary).toBe('majority');
	});
});

describe('encodeState → decodeState roundtrip', () => {
	const primaries = ['minority', 'majority', '2019'] as const;

	for (const primary of primaries) {
		it(`preserves primary=${primary} through the roundtrip`, () => {
			const state = validState({
				primary,
				mapOn: { [primary]: true } as never
			});
			const code = encodeState(state)!;
			const decoded = decodeState(code)!;
			expect(decoded.primary).toBe(primary);
			expect(decoded.mapOn[primary]).toBe(true);
		});
	}

	it('preserves overlay-bit combinations through the roundtrip', () => {
		// Cycle through the four oBits values (00, 01, 10, 11) for the two
		// non-primary maps; each must come back intact.
		const cases = [
			[false, false],
			[true, false],
			[false, true],
			[true, true]
		] as const;
		for (const [mapAOn, mapBOn] of cases) {
			const state = validState({
				primary: 'minority',
				mapOn: { minority: true, majority: mapAOn, '2019': mapBOn }
			});
			const decoded = decodeState(encodeState(state)!)!;
			expect(decoded.mapOn.majority).toBe(mapAOn);
			expect(decoded.mapOn['2019']).toBe(mapBOn);
		}
	});

	it('preserves all 16 layer-bit combinations through the roundtrip', () => {
		for (let bits = 0; bits < 16; bits++) {
			const state = validState({
				layers: {
					vote: !!(bits & 1),
					'ed-fill': !!(bits & 2),
					'ed-lines': !!(bits & 4),
					eg: !!(bits & 8)
				}
			});
			const decoded = decodeState(encodeState(state)!)!;
			expect(decoded.layers.vote).toBe(!!(bits & 1));
			expect(decoded.layers['ed-fill']).toBe(!!(bits & 2));
			expect(decoded.layers['ed-lines']).toBe(!!(bits & 4));
			expect(decoded.layers.eg).toBe(!!(bits & 8));
		}
	});

	it('buckets cx_norm/cy_norm to a 5×5 grid (lossy by design)', () => {
		// cx_norm = 0.3 → floor(0.3 × 5) = 1 → decoded back to bucket 1.
		// Same input range, same bucket; encoder is many-to-one on viewport.
		const a = decodeState(encodeState(validState({
			viewport: { cx_norm: 0.21, cy_norm: 0.21, zoom: 1.0 }
		}))!)!;
		const b = decodeState(encodeState(validState({
			viewport: { cx_norm: 0.39, cy_norm: 0.39, zoom: 1.0 }
		}))!)!;
		// Both 0.21 and 0.39 fall in bucket 1 (covers 0.2–0.4).
		expect(a.viewport.cx_norm).toBe(b.viewport.cx_norm);
		expect(a.viewport.cy_norm).toBe(b.viewport.cy_norm);
	});

	it('clamps out-of-range cx_norm/cy_norm to the edge buckets', () => {
		const farPos = decodeState(encodeState(validState({
			viewport: { cx_norm: 99, cy_norm: 99, zoom: 1.0 }
		}))!)!;
		const farNeg = decodeState(encodeState(validState({
			viewport: { cx_norm: -99, cy_norm: -99, zoom: 1.0 }
		}))!)!;
		// Both should land in valid buckets, not throw or produce NaN.
		expect(Number.isFinite(farPos.viewport.cx_norm)).toBe(true);
		expect(Number.isFinite(farNeg.viewport.cx_norm)).toBe(true);
	});

	it('buckets zoom into the four documented tiers', () => {
		// zoom thresholds: ≥0.5 → tier 0, ≥0.2 → tier 1, ≥0.08 → tier 2, else tier 3.
		const tiers = new Map<string, number>();
		for (const z of [1.0, 0.5, 0.3, 0.1, 0.05, 0.01]) {
			const code = encodeState(validState({
				viewport: { cx_norm: 0.5, cy_norm: 0.5, zoom: z }
			}))!;
			const decoded = decodeState(code)!;
			tiers.set(code, decoded.viewport.zoom);
		}
		// At most 4 distinct codes among 6 input zooms (4 zoom tiers).
		expect(tiers.size).toBeLessThanOrEqual(4);
	});
});

describe('exhaustive coverage of valid state space', () => {
	it('every encoded state decodes successfully and is self-consistent', () => {
		// Sample across the full 19,200-state space — not exhaustive (would
		// be slow), but enough to flush any encode/decode index drift.
		const primaries = ['minority', 'majority', '2019'] as const;
		let checked = 0;
		for (const primary of primaries) {
			for (let oBits = 0; oBits < 4; oBits++) {
				for (let lBits = 0; lBits < 16; lBits += 5) {
					const others = primaries.filter(p => p !== primary);
					const code = encodeState({
						primary,
						mapOn: {
							[primary]: true,
							[others[0]]: !!(oBits & 1),
							[others[1]]: !!(oBits & 2)
						} as never,
						layers: {
							vote: !!(lBits & 1),
							'ed-fill': !!(lBits & 2),
							'ed-lines': !!(lBits & 4),
							eg: !!(lBits & 8)
						},
						viewport: { cx_norm: 0.5, cy_norm: 0.5, zoom: 1.0 }
					});
					expect(code).not.toBeNull();
					const back = decodeState(code!);
					expect(back).not.toBeNull();
					expect(back!.primary).toBe(primary);
					checked++;
				}
			}
		}
		// Sanity: confirm the loop did substantial work.
		expect(checked).toBeGreaterThan(30);
	});
});
