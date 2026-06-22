// Alberta Electoral Boundary Audit — share-code encoding/decoding + share persistence
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

// ── Word lists (27 × 27 × 27 = 19,683 codes; 19,200 valid) ──────────────────
// Primary (3) × overlays (4) × layers (16) × vp-col (5) × vp-row (5) × zoom (4)
// = 19,200 valid states. Remaining 483 codes return null on decode (typo guard).

const ADJECTIVES: readonly string[] = [
	'alpine',     'arctic',     'aspen',      'badlands',   'boreal',
	'bunchgrass', 'chinook',    'clearwater', 'coulee',     'dryland',
	'fescue',     'foothills',  'glacial',    'grassland',  'gravel',
	'hoarfrost',  'kettle',     'lichen',     'lodgepole',  'meadow',
	'montane',    'muskeg',     'parkland',   'prairie',    'riparian',
	'shortgrass', 'subalpine',
];

const ANIMALS: readonly string[] = [
	'badger',    'bison',    'bluebird',  'caribou',   'cougar',
	'coyote',    'crane',    'eagle',     'elk',       'falcon',
	'ferret',    'fisher',   'goose',     'grizzly',   'hare',
	'hawk',      'heron',    'killdeer',  'loon',      'lynx',
	'marten',    'moose',    'osprey',    'owl',       'pronghorn',
	'ptarmigan', 'wolverine',
];

const PLACES: readonly string[] = [
	'athabasca', 'banff',      'bow',        'camrose',    'canmore',
	'cardston',  'cochrane',   'drumheller', 'edson',      'elbow',
	'ghost',     'highwood',   'hinton',     'innisfail',  'jasper',
	'kananaskis','lacombe',    'lethbridge', 'maligne',    'okotoks',
	'oldman',    'peace',      'ponoka',     'smoky',      'sundre',
	'wapiti',    'wetaskiwin',
];

const BASE    = 27;
const MAX_N   = 19_200;
const MAP_KEYS = ['minority', 'majority', '2019'] as const;

// ── Types ─────────────────────────────────────────────────────────────────────

import type { MapKey, LayerKey } from './mapEngine/types';

export type MapState = {
	primary:  MapKey;
	mapOn:    Record<MapKey, boolean>;
	layers:   Record<LayerKey, boolean>;
	viewport: { cx_norm: number; cy_norm: number; zoom: number };
};

// ── Encode ────────────────────────────────────────────────────────────────────

export function encodeState(state: MapState): string | null {
	const pIdx = MAP_KEYS.indexOf(state.primary as typeof MAP_KEYS[number]);
	if (pIdx === -1) return null;

	const others = MAP_KEYS.filter(k => k !== state.primary);
	const oBits  = (state.mapOn[others[0]] ? 1 : 0) | (state.mapOn[others[1]] ? 2 : 0);

	const lBits =
		(state.layers['vote']     ? 1 : 0) |
		(state.layers['ed-fill']  ? 2 : 0) |
		(state.layers['ed-lines'] ? 4 : 0) |
		(state.layers['eg']       ? 8 : 0);

	const col  = Math.min(4, Math.max(0, Math.floor(state.viewport.cx_norm * 5)));
	const row  = Math.min(4, Math.max(0, Math.floor(state.viewport.cy_norm * 5)));
	const zoom = state.viewport.zoom;
	const zT   = zoom >= 0.5 ? 0 : zoom >= 0.2 ? 1 : zoom >= 0.08 ? 2 : 3;

	const n = pIdx + 3 * (oBits + 4 * (lBits + 16 * (col + 5 * (row + 5 * zT))));
	if (n >= MAX_N) return null;

	return `${ADJECTIVES[n % BASE]}-${ANIMALS[Math.floor(n / BASE) % BASE]}-${PLACES[Math.floor(n / (BASE * BASE))]}`;
}

// ── Decode ────────────────────────────────────────────────────────────────────

export function decodeState(code: string): MapState | null {
	const parts = code.toLowerCase().trim().split(/[-\s]+/);
	if (parts.length !== 3) return null;

	const i1 = ADJECTIVES.indexOf(parts[0]);
	const i2 = ANIMALS.indexOf(parts[1]);
	const i3 = PLACES.indexOf(parts[2]);
	if (i1 === -1 || i2 === -1 || i3 === -1) return null;

	const n = i1 + BASE * i2 + BASE * BASE * i3;
	if (n >= MAX_N) return null;

	const pIdx = n % 3;
	const oBits = Math.floor(n / 3) % 4;
	const lBits = Math.floor(n / 12) % 16;
	const col   = Math.floor(n / 192) % 5;
	const row   = Math.floor(n / 960) % 5;
	const zT    = Math.floor(n / 4800);

	const primary = MAP_KEYS[pIdx];
	const others  = MAP_KEYS.filter(k => k !== primary);

	const mapOn: Record<MapKey, boolean> = { minority: false, majority: false, '2019': false };
	mapOn[primary]   = true;
	mapOn[others[0]] = !!(oBits & 1);
	mapOn[others[1]] = !!(oBits & 2);

	return {
		primary,
		mapOn,
		layers: {
			'vote':     !!(lBits & 1),
			'ed-fill':  !!(lBits & 2),
			'ed-lines': !!(lBits & 4),
			'eg':       !!(lBits & 8),
		},
		viewport: {
			cx_norm: (col + 0.5) / 5,
			cy_norm: (row + 0.5) / 5,
			zoom:    [0.7, 0.35, 0.14, 0.05][zT],
		},
	};
}

// ── Share origin + optional share metadata ────────────────────────────────────
// These back the share-code feature only: the origin code threads a loaded share
// through to saveShare, and the GPS region / language are optional fields attached
// to a saved share. None of this is tracking — it is written only when the user
// explicitly generates/saves a share code.

let _originCode: string | null = null;  // null = default start; code = loaded from share
let _gpsRegion: { lat: number; lng: number } | null = null;
let _language: string | null = null;

export function setOrigin(code: string | null): void {
	_originCode = code;
}

export function setGpsRegion(lat: number, lng: number): void {
	_gpsRegion = { lat, lng };
}

export function setLanguage(lang: string): void {
	_language = lang;
}

// ── Supabase persistence ──────────────────────────────────────────────────────

import { db } from './db';

export function saveShare(code: string, state: MapState): void {
	if (!code || code === '—') return;
	const payload: Record<string, unknown> = { ...state };
	if (_gpsRegion) { payload.region_lat = _gpsRegion.lat; payload.region_lng = _gpsRegion.lng; }
	if (_language)  payload.language = _language;
	db.from('shares').upsert(
		{ code, state_json: payload, origin_code: _originCode },
		{ onConflict: 'code', ignoreDuplicates: true },
	).then(undefined, () => {});
}
