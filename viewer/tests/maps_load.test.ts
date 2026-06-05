// @vitest-environment happy-dom
//
// Tests for loadHoverJson / loadVaJson. Verifies the post-fetch ctx
// mutation: the hover JSON populates ctx.allHoverData[key] keyed by id
// AND ctx.nameIndex[key] keyed by name; the VA JSON populates
// ctx.allVaData[key] keyed by stringified va_id.

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { loadHoverJson, loadVaJson } from '../src/lib/mapEngine/maps';
import type { MapCtx } from '../src/lib/mapEngine/types';

function mkCtx(): MapCtx {
	return {
		svgEl: null,
		mapPrimary: null,
		layerState: { vote: false, 'ed-fill': false, 'ed-lines': false, eg: false },
		allHoverData: {},
		nameIndex: {},
		allVaData: {},
		edHover: null,
		overlayInSvg: { minority: null, majority: null, '2019': null },
	} as unknown as MapCtx;
}

beforeEach(() => { vi.restoreAllMocks(); });

describe('loadHoverJson', () => {
	it('populates allHoverData[key] keyed by id', async () => {
		const ctx = mkCtx();
		const records = [
			{ id: 1, name: 'Calgary-Foothills', ucp_pct: 52, ndp_pct: 48 },
			{ id: 2, name: 'Edmonton-Whitemud', ucp_pct: 41, ndp_pct: 59 },
		];
		vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: () => Promise.resolve(records) }));
		loadHoverJson(ctx, 'minority', 'unused-url');
		await new Promise(r => setTimeout(r, 0));
		expect(ctx.allHoverData.minority).toEqual({
			1: records[0],
			2: records[1],
		});
	});

	it('also builds a nameIndex keyed by district name', async () => {
		const ctx = mkCtx();
		const records = [
			{ id: 1, name: 'Calgary-Foothills', ucp_pct: 52, ndp_pct: 48 },
			{ id: 2, name: 'Edmonton-Whitemud', ucp_pct: 41, ndp_pct: 59 },
		];
		vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: () => Promise.resolve(records) }));
		loadHoverJson(ctx, 'majority', 'unused-url');
		await new Promise(r => setTimeout(r, 0));
		expect(ctx.nameIndex.majority['Calgary-Foothills']).toEqual(records[0]);
		expect(ctx.nameIndex.majority['Edmonton-Whitemud']).toEqual(records[1]);
	});

	it('swallows fetch failure silently (leaves ctx untouched)', async () => {
		const ctx = mkCtx();
		vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('network')));
		loadHoverJson(ctx, '2019', 'unused-url');
		await new Promise(r => setTimeout(r, 5));
		expect(ctx.allHoverData['2019']).toBeUndefined();
		expect(ctx.nameIndex['2019']).toBeUndefined();
	});
});

describe('loadVaJson', () => {
	it('populates allVaData[key] keyed by stringified va_id', async () => {
		const ctx = mkCtx();
		const records = [
			{ va_id: 1001, poll_name: 'Poll A', ucp_pct: 60, ndp_pct: 40 },
			{ va_id: 1002, poll_name: 'Poll B', ucp_pct: 45, ndp_pct: 55 },
		];
		vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: () => Promise.resolve(records) }));
		loadVaJson(ctx, 'minority', 'unused-url');
		await new Promise(r => setTimeout(r, 0));
		expect(ctx.allVaData.minority).toEqual({
			'1001': records[0],
			'1002': records[1],
		});
	});

	it('handles empty response cleanly', async () => {
		const ctx = mkCtx();
		vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: () => Promise.resolve([]) }));
		loadVaJson(ctx, '2019', 'unused-url');
		await new Promise(r => setTimeout(r, 0));
		expect(ctx.allVaData['2019']).toEqual({});
	});
});
