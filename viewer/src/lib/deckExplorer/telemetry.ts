// Alberta Electoral Boundary Audit — deck.gl explorer telemetry
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Parity with the SVG explorer's telemetry (src/lib/share.ts → flushTelemetry):
//   - inserts into the same `telemetry` table via the SHARED supabase client (db.ts),
//   - rows are { session_id, origin_code, event_type, payload },
//   - session_id / origin_code come from the shared share.ts singletons so the two
//     explorers share one session identity,
//   - the insert is fire-and-forget (.then(undefined, () => {}) — never throws),
//   - and it is CONSENT-GATED: nothing is sent unless participates() is true,
//     exactly as flushTelemetry() early-returns on !_participates. This is the
//     single chokepoint, so no call site can accidentally log without consent.
//
// The pure payload builders below are framework-free and unit-tested; the network
// insert (logEvent) is mocked out of unit tests.

import { db } from '../db';
import { getSessionId, getOrigin, participates } from '../share';

// ── Event types ────────────────────────────────────────────────────────────────
// snake_case, matching the existing engine union style (map_switch / layer / ed_focus).

export type DeckTelemetryEvent =
	| { event_type: 'overlay_open'; payload: Record<string, never> }
	| { event_type: 'district_select'; payload: { name: string; map: string } }
	| { event_type: 'poi_click'; payload: { id: string } };

// ── Pure payload builders ───────────────────────────────────────────────────────
// Each returns { event_type, payload } only; logEvent wraps the row with the
// session / origin fields (mirrors flushTelemetry's .map shape).

export function evtOverlayOpen(): DeckTelemetryEvent {
	return { event_type: 'overlay_open', payload: {} };
}

export function evtDistrictSelect(name: string, map: string): DeckTelemetryEvent {
	return { event_type: 'district_select', payload: { name, map } };
}

export function evtPoiClick(id: string): DeckTelemetryEvent {
	return { event_type: 'poi_click', payload: { id } };
}

// ── Fire-and-forget insert ──────────────────────────────────────────────────────
// Consent-gated; swallows every failure. NEVER throws to the caller and NEVER
// blocks the UI — any error (no consent, network, schema) is silently dropped.

export function logEvent(event: DeckTelemetryEvent): void {
	try {
		if (!participates()) return;
		const row = {
			session_id: getSessionId(),
			origin_code: getOrigin(),
			event_type: event.event_type,
			payload: event.payload
		};
		db.from('telemetry').insert(row).then(undefined, () => {});
	} catch {
		// fire-and-forget: any synchronous failure is swallowed
	}
}
