// Alberta Electoral Boundary Audit — share-state URL serialization
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

// ── Types ─────────────────────────────────────────────────────────────────────
// Deck-explorer state model. The map state is serialized into a self-contained
// URL query string (no DB resolution needed): the active maps, the layer
// overlays, and the normalised viewport. viewport.zoom is normalised 0..1 over
// the deck's zoom range; cx_norm/cy_norm are normalised 0..1 over the bbox.

export type MapKey = 'minority' | 'majority' | '2019';

export type MapState = {
	primary:  MapKey;
	mapOn:    Record<MapKey, boolean>;
	layers:   { hwy: boolean; water: boolean; pois: boolean };
	viewport: { cx_norm: number; cy_norm: number; zoom: number }; // zoom: 0..1 normalised
};

// ── Serialize ───────────────────────────────────────────────────────────────
// Pack a MapState into a URL query string. `m` lists the active maps, primary
// first; `f` lists the active overlay filters; cx/cy/z are the normalised
// viewport at full (4-dp) precision.

export function serializeState(s: MapState): string {
	const p = new URLSearchParams();
	const order: MapKey[] = ['minority', 'majority', '2019'];
	const maps = [s.primary, ...order.filter((k) => k !== s.primary && s.mapOn[k])];
	p.set('m', maps.join(','));
	const on = (['hwy', 'water', 'pois'] as const).filter((k) => s.layers[k]);
	if (on.length) p.set('f', on.join(','));
	p.set('cx', s.viewport.cx_norm.toFixed(4));
	p.set('cy', s.viewport.cy_norm.toFixed(4));
	p.set('z', s.viewport.zoom.toFixed(4));
	return p.toString();
}

// ── Parse ───────────────────────────────────────────────────────────────────
// Read a MapState back from a URLSearchParams. Returns null when no valid `m`
// is present (the only required key). Missing/invalid viewport params fall back
// to the 0.5 centre.

export function parseState(p: URLSearchParams): MapState | null {
	const m = p.get('m');
	if (!m) return null;
	const order: MapKey[] = ['minority', 'majority', '2019'];
	const maps = m.split(',').filter((x) => (order as string[]).includes(x)) as MapKey[];
	if (!maps.length) return null;
	const primary = maps[0];
	const mapOn = { minority: false, majority: false, '2019': false } as Record<MapKey, boolean>;
	for (const k of maps) mapOn[k] = true;
	const f = (p.get('f') || '').split(',');
	const layers = { hwy: f.includes('hwy'), water: f.includes('water'), pois: f.includes('pois') };
	const c01 = (v: string | null, d: number) => {
		const n = parseFloat(v ?? '');
		return isFinite(n) ? Math.min(1, Math.max(0, n)) : d;
	};
	return {
		primary,
		mapOn,
		layers,
		viewport: { cx_norm: c01(p.get('cx'), 0.5), cy_norm: c01(p.get('cy'), 0.5), zoom: c01(p.get('z'), 0.5) }
	};
}
