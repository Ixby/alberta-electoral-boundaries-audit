// Unit tests for the framework-free deck.gl explorer data layer.
//
// Covers the pure, node-testable core: binary bundle decode (zero-copy
// Float32Array views, keyed by tile key) and the LOD level math ported from
// the validated prototype (viewer/static/spike/index.html). The IndexedDB /
// fetch path in loadBundle is intentionally NOT unit-tested here — it needs a
// browser environment (indexedDB + fetch); decode + level math are the
// testable logic.
//
// NOTE on placement: this file lives under tests/ (not co-located in
// src/lib/deckExplorer/) because vitest.config.ts restricts the include glob to
// tests/**/*.test.ts. Co-locating would require committing a config change,
// which is out of scope for this task.

import { describe, it, expect } from 'vitest';
import {
	decodeBundle,
	tileLevelForZoom,
	levelsToKeep
} from '../../src/lib/deckExplorer/loader';

// Build a synthetic bundle: header {"0/0/0":[0,N]} | 4-byte pad | body.
// Body = one tile: uint32 nRings=1, then uint16 vid=7, uint16 nPts=4, then
// 8 float32 [1..8]. Tile length N = 4 (nRings) + 4 (vid+nPts) + 32 (8*f32) = 40.
function makeBundle(): ArrayBuffer {
	const headerStr = '{"0/0/0":[0,40]}';
	const headerBytes = new TextEncoder().encode(headerStr);
	const hlen = headerBytes.length;
	const pad = (((-(4 + hlen)) % 4) + 4) % 4;
	const bodyOff = 4 + hlen + pad;
	const tileLen = 4 + 4 + 8 * 4; // 40

	const buf = new ArrayBuffer(bodyOff + tileLen);
	const dv = new DataView(buf);
	dv.setUint32(0, hlen, true);
	new Uint8Array(buf, 4, hlen).set(headerBytes);

	let off = bodyOff;
	dv.setUint32(off, 1, true); // nRings
	off += 4;
	dv.setUint16(off, 7, true); // vid
	dv.setUint16(off + 2, 4, true); // nPts
	off += 4;
	for (let i = 0; i < 8; i++) {
		dv.setFloat32(off, i + 1, true);
		off += 4;
	}
	return buf;
}

describe('decodeBundle', () => {
	it('decodes one tile keyed by its header key', () => {
		const out = decodeBundle(makeBundle());
		expect(Object.keys(out)).toEqual(['0/0/0']);
		const tile = out['0/0/0'];
		expect(tile.length).toBe(1);
		expect(tile[0].id).toBe(7);
		expect(Array.from(tile[0].coords)).toEqual([1, 2, 3, 4, 5, 6, 7, 8]);
	});

	it('returns Float32Array coords (zero-copy view into the buffer)', () => {
		const out = decodeBundle(makeBundle());
		expect(out['0/0/0'][0].coords).toBeInstanceOf(Float32Array);
	});
});

// ── LOD level math (ported from paint() / maybeLoadLevels in index.html) ──

describe('tileLevelForZoom', () => {
	// raw = round(zoom + log2(side/256)); clamp to [minZoom, maxZoom]; then
	// min(levelCap) if the cap is set.
	it('clamps the raw target down to maxZoom', () => {
		// side=256 → log2(1)=0, so raw == round(zoom). zoom 20 → raw 20 → clamp to 10.
		expect(tileLevelForZoom(20, 256, 0, 10)).toBe(10);
	});

	it('clamps the raw target up to minZoom', () => {
		expect(tileLevelForZoom(-5, 256, 1, 10)).toBe(1);
	});

	it('accounts for the side/256 log2 offset', () => {
		// side=512 → log2(2)=1, so raw = round(zoom+1). zoom 4 → raw 5.
		expect(tileLevelForZoom(4, 512, 0, 10)).toBe(5);
	});

	it('levelCap lowers the returned level below the clamped value', () => {
		// raw=8, clamp(0..10)=8, cap 3 → 3.
		expect(tileLevelForZoom(8, 256, 0, 10, 3)).toBe(3);
	});

	it('levelCap of null is ignored', () => {
		expect(tileLevelForZoom(8, 256, 0, 10, null)).toBe(8);
	});
});

describe('levelsToKeep', () => {
	it('returns 0..L+1 (lookahead), clamped at the lower bound', () => {
		// minZoom 0, L=3 → keep 0,1,2,3,4.
		expect(levelsToKeep(3, 0)).toEqual([0, 1, 2, 3, 4]);
	});

	it('never returns a level below minZoom', () => {
		// minZoom 2, L=2 → keep 2,3.
		expect(levelsToKeep(2, 2)).toEqual([2, 3]);
	});
});
