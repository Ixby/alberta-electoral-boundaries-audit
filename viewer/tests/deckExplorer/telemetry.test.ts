// Unit tests for the deck.gl explorer telemetry payload builders.
//
// The pure builders (evtOverlayOpen / evtDistrictSelect / evtPoiClick) turn a UI
// action into a { event_type, payload } row fragment matching the existing
// SVG-explorer telemetry contract (src/lib/share.ts → flushTelemetry inserts
// { session_id, origin_code, event_type, payload } into the `telemetry` table).
// The builders are framework-free; the supabase insert in logEvent is NOT unit
// tested against a live client — db + share are mocked so we can assert the
// consent gate and fire-and-forget behaviour without a network call.
//
// Placement under tests/ mirrors the other deckExplorer specs; vitest.config.ts
// only collects tests/**/*.test.ts.

import { describe, it, expect, vi, beforeEach } from 'vitest';

// ── Mock the shared supabase client + share.ts singletons ───────────────────────
// vi.mock factories are hoisted above the file, so the mock fns / mutable consent
// flag must live in a vi.hoisted() block to be referenceable inside them.
const h = vi.hoisted(() => {
	const insertMock = vi.fn(() => ({ then: (_ok: unknown, _err: unknown) => undefined }));
	const fromMock = vi.fn(() => ({ insert: insertMock }));
	return { insertMock, fromMock, participatesValue: true };
});
const { insertMock, fromMock } = h;

vi.mock('../../src/lib/db', () => ({ db: { from: h.fromMock } }));
vi.mock('../../src/lib/share', () => ({
	getSessionId: () => 'sess-test',
	getOrigin: () => 'origin-test',
	participates: () => h.participatesValue
}));

import {
	evtOverlayOpen,
	evtDistrictSelect,
	evtPoiClick,
	logEvent
} from '../../src/lib/deckExplorer/telemetry';

describe('telemetry payload builders', () => {
	it('evtOverlayOpen() → { event_type: "overlay_open", payload: {} }', () => {
		expect(evtOverlayOpen()).toEqual({ event_type: 'overlay_open', payload: {} });
	});

	it('evtDistrictSelect(name, map) → district_select with name + map in payload', () => {
		expect(evtDistrictSelect('Calgary-Beddington', 'minority')).toEqual({
			event_type: 'district_select',
			payload: { name: 'Calgary-Beddington', map: 'minority' }
		});
	});

	it('evtPoiClick(id) → poi_click with id in payload', () => {
		expect(evtPoiClick('airdrie-split')).toEqual({
			event_type: 'poi_click',
			payload: { id: 'airdrie-split' }
		});
	});
});

describe('logEvent() — consent-gated fire-and-forget insert', () => {
	beforeEach(() => {
		insertMock.mockClear();
		fromMock.mockClear();
		h.participatesValue = true;
	});

	it('inserts a row with session_id, origin_code, event_type, payload into `telemetry`', () => {
		logEvent(evtPoiClick('airdrie-split'));
		expect(fromMock).toHaveBeenCalledWith('telemetry');
		expect(insertMock).toHaveBeenCalledTimes(1);
		expect(insertMock).toHaveBeenCalledWith({
			session_id: 'sess-test',
			origin_code: 'origin-test',
			event_type: 'poi_click',
			payload: { id: 'airdrie-split' }
		});
	});

	it('does NOT insert when the user has not consented (participates() === false)', () => {
		h.participatesValue = false;
		logEvent(evtOverlayOpen());
		expect(insertMock).not.toHaveBeenCalled();
	});

	it('never throws even if the insert call blows up (fire-and-forget)', () => {
		insertMock.mockImplementationOnce(() => {
			throw new Error('boom');
		});
		expect(() => logEvent(evtDistrictSelect('X', 'minority'))).not.toThrow();
	});
});
