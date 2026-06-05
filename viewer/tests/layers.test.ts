// @vitest-environment happy-dom
//
// Tests for layer toggles. Verifies setLayerOn emits the right event,
// mutates ctx.layerState, toggles the .tb-layer-on class on matching
// buttons, and that computeEGContribs produces a normalized vote-waste
// signal symmetric around the 50/50 line.

import { describe, it, expect, beforeEach } from 'vitest';
import { setLayerOn, computeEGContribs } from '../src/lib/mapEngine/layers';
import type { MapCtx, MapEngineEvent } from '../src/lib/mapEngine/types';

function mkCtx(): MapCtx {
	const stub = {
		svgEl: null,
		edHover: null,
		overlayInSvg: { minority: null, majority: null, '2019': null },
		layerState: { vote: true, 'ed-fill': false, 'ed-lines': true, eg: false },
	};
	return stub as unknown as MapCtx;
}

function mkBtn(layer: string): HTMLElement {
	const b = document.createElement('button');
	b.className = 'tb-btn';
	b.setAttribute('data-layer', layer);
	document.body.appendChild(b);
	return b;
}

beforeEach(() => { document.body.innerHTML = ''; });

// ── setLayerOn ────────────────────────────────────────────────────────────────

describe('setLayerOn', () => {
	it('mutates ctx.layerState[key] and emits a layer event', () => {
		const ctx = mkCtx();
		const events: MapEngineEvent[] = [];
		setLayerOn(ctx, 'ed-fill', true, e => events.push(e));
		expect(ctx.layerState['ed-fill']).toBe(true);
		expect(events).toEqual([{ type: 'layer', key: 'ed-fill', on: true }]);
	});

	it('toggles .tb-layer-on on all matching buttons', () => {
		const ctx = mkCtx();
		const b1 = mkBtn('ed-fill');
		const b2 = mkBtn('ed-fill');
		const bOther = mkBtn('eg');
		setLayerOn(ctx, 'ed-fill', true, () => {});
		expect(b1.classList.contains('tb-layer-on')).toBe(true);
		expect(b2.classList.contains('tb-layer-on')).toBe(true);
		expect(bOther.classList.contains('tb-layer-on')).toBe(false);
	});

	it('is a no-op when key is already in the requested state (no event)', () => {
		const ctx = mkCtx();
		// vote starts true in mkCtx
		const events: MapEngineEvent[] = [];
		setLayerOn(ctx, 'vote', true, e => events.push(e));
		expect(events).toEqual([]);
	});

	it('handles toggle-off cleanly', () => {
		const ctx = mkCtx();
		const events: MapEngineEvent[] = [];
		setLayerOn(ctx, 'vote', false, e => events.push(e));
		expect(ctx.layerState.vote).toBe(false);
		expect(events).toEqual([{ type: 'layer', key: 'vote', on: false }]);
	});
});

// ── computeEGContribs ─────────────────────────────────────────────────────────
//
// Efficiency-gap contribution per district: signed wasted-vote share where
// positive = UCP, negative = NDP. Empty/zero-vote inputs return {}.

describe('computeEGContribs', () => {
	it('returns {} when ctx.edHover is null', () => {
		const ctx = mkCtx();
		expect(computeEGContribs(ctx)).toEqual({});
	});

	it('returns {} when no district has any votes', () => {
		const ctx = mkCtx();
		ctx.edHover = { 1: { id: 1, ucp_votes: 0, ndp_votes: 0, votes: 0 } } as any;
		expect(computeEGContribs(ctx)).toEqual({});
	});

	it('contribution per district follows (UCP_wasted − NDP_wasted) / total_votes_overall', () => {
		const ctx = mkCtx();
		// Two districts, both 100 votes. Contribs normalize by the SUM
		// of all votes (200), not per-district.
		//   D1: UCP 51 NDP 49 → UCP wins. UCP wasted 1, NDP wasted 49.
		//        contrib = (1 − 49) / 200 = −0.24
		//   D2: UCP 10 NDP 90 → NDP wins. UCP wasted 10, NDP wasted 40.
		//        contrib = (10 − 40) / 200 = −0.15
		// Sign convention: positive = UCP wasted more (UCP disadvantaged).
		ctx.edHover = {
			1: { id: 1, ucp_votes: 51, ndp_votes: 49, votes: 100 },
			2: { id: 2, ucp_votes: 10, ndp_votes: 90, votes: 100 },
		} as any;
		const c = computeEGContribs(ctx);
		expect(c[1]).toBeCloseTo(-0.24, 6);
		expect(c[2]).toBeCloseTo(-0.15, 6);
	});

	it('reverses sign when NDP wastes fewer votes (NDP efficient)', () => {
		const ctx = mkCtx();
		// D1: UCP 49 NDP 51 → NDP wins by 1. UCP wasted 49, NDP wasted 1.
		//      contrib = (49 − 1) / 100 = +0.48 (UCP disadvantaged).
		ctx.edHover = {
			1: { id: 1, ucp_votes: 49, ndp_votes: 51, votes: 100 },
		} as any;
		const c = computeEGContribs(ctx);
		expect(c[1]).toBeCloseTo(0.48, 6);
	});

	it('contributions sum to the classic efficiency-gap definition', () => {
		// Three even districts; sum of contribs should equal (wastedUcp − wastedNdp) / totalVotes.
		const ctx = mkCtx();
		ctx.edHover = {
			1: { id: 1, ucp_votes: 60, ndp_votes: 40, votes: 100 },
			2: { id: 2, ucp_votes: 30, ndp_votes: 70, votes: 100 },
			3: { id: 3, ucp_votes: 55, ndp_votes: 45, votes: 100 },
		} as any;
		const c = computeEGContribs(ctx);
		const sum = c[1] + c[2] + c[3];
		// Wasted UCP: 10 + 30 + 5 = 45; wasted NDP: 40 + 20 + 45 = 105.
		// EG = (45 − 105) / 300 = −0.20.
		expect(sum).toBeCloseTo(-0.20, 6);
	});
});
