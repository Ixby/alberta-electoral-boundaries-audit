// Framework-free data layer for the deck.gl map explorer.
//
// Pure TypeScript: NO Svelte, NO `$app/paths` — kept unit-testable in node.
// Ported from the validated prototype at viewer/static/spike/index.html (whose
// `decodeBundle` this mirrors). Two concerns:
//
//   1. decodeBundle / decodeTile — parse the binary tile bundle into a map of
//      { id, coords } features, keyed by tile key, with zero-copy Float32Array
//      views into the source ArrayBuffer.
//   2. LOD level math — tileLevelForZoom / levelsToKeep — the zoom→level
//      mapping and the lazy-load window, lifted verbatim from `paint()` and
//      `maybeLoadLevels()` in the prototype.
//   3. loadBundle — async tile loader with an IndexedDB cache (version-checked),
//      falling back to fetch. This path needs a browser env (indexedDB + fetch)
//      and is not unit-tested; the decode + level math above are the testable
//      core.

// ── Types ───────────────────────────────────────────────────────────────────

/** A single VA polygon ring decoded from a tile: its VA id and a flat XY
 *  Float32Array (a zero-copy view into the bundle's ArrayBuffer). */
export interface TileFeature {
	id: number;
	coords: Float32Array;
}

/** Decoded tiles, keyed by tile key ("z/x/y"). */
export type TileArchive = Record<string, TileFeature[]>;

/** A bundle descriptor from the manifest: the file to fetch and its content
 *  version (sha1 prefix from build_explorer_tiles.py), used as the cache key. */
export interface BundleRef {
	file: string;
	ver: string;
}

// ── Binary decode ─────────────────────────────────────────────────────────────
//
// Bundle layout (from build_explorer_tiles.py `write_bundle_bin`):
//   uint32 headerLen | header JSON {tileKey:[start,len]} | pad to 4-byte | body
// Each tile blob in the body:
//   uint32 nRings | per ring: uint16 vaId, uint16 nPts, nPts*2 float32 XY
// All little-endian. Coordinate blocks are 4-byte aligned so the Float32Array
// views below are zero-copy (no per-coord copy, no JSON parse on the hot path).

/** Decode one tile blob starting at byte offset `off` into a list of features.
 *  `coords` is a zero-copy Float32Array view into `buf`. */
export function decodeTile(buf: ArrayBuffer, dv: DataView, off: number): TileFeature[] {
	const nRings = dv.getUint32(off, true);
	off += 4;
	const feats: TileFeature[] = new Array(nRings);
	for (let i = 0; i < nRings; i++) {
		const vid = dv.getUint16(off, true);
		const nPts = dv.getUint16(off + 2, true);
		off += 4;
		feats[i] = { id: vid, coords: new Float32Array(buf, off, nPts * 2) };
		off += nPts * 2 * 4;
	}
	return feats;
}

/** Decode a binary bundle into a tile archive keyed by tile key. */
export function decodeBundle(buf: ArrayBuffer): TileArchive {
	const dv = new DataView(buf);
	const hlen = dv.getUint32(0, true);
	const header: Record<string, [number, number]> = JSON.parse(
		new TextDecoder().decode(new Uint8Array(buf, 4, hlen))
	);
	const bodyOff = 4 + hlen + (((-(4 + hlen)) % 4) + 4) % 4; // body is 4-byte aligned
	const out: TileArchive = {};
	for (const k in header) out[k] = decodeTile(buf, dv, bodyOff + header[k][0]);
	return out;
}

// ── LOD level math ────────────────────────────────────────────────────────────

/** Map a camera zoom to a tile LOD level.
 *  raw = round(zoom + log2(side/256)); clamp to [minZoom, maxZoom]; then apply
 *  the visual cap (min with levelCap) when one is set. Ported from `paint()`. */
export function tileLevelForZoom(
	zoom: number,
	side: number,
	minZoom: number,
	maxZoom: number,
	levelCap: number | null = null
): number {
	const raw = Math.round(zoom + Math.log2(side / 256));
	let L = Math.max(minZoom, Math.min(maxZoom, raw));
	if (levelCap != null) L = Math.min(L, levelCap);
	return L;
}

/** The levels to keep loaded for a rendered level `L`: 0..L+1 (one level of
 *  lookahead for zoom-in), clamped to the [minZoom, …] floor. Ported from
 *  `maybeLoadLevels()`, which keeps every bundle with `lo <= L + 1`. */
export function levelsToKeep(L: number, minZoom: number): number[] {
	const out: number[] = [];
	for (let z = Math.max(minZoom, 0); z <= L + 1; z++) out.push(z);
	return out;
}

// ── Bundle loading + IndexedDB cache ──────────────────────────────────────────
//
// Not unit-tested: indexedDB and fetch require a browser environment. The
// IndexedDB DB/store names are renamed from the prototype's `spikeArchive` to
// `albertaExplorerTiles` for this app. A bundle is keyed by file + version; a
// version mismatch (new build) invalidates the cached entry instantly, and a
// 30-day TTL is a hygiene backstop.

const DBN = 'albertaExplorerTiles';
const STORE = 't';
const CACHE_TTL = 30 * 864e5; // 30 days in ms

interface CacheRow {
	t: number;
	ver: string;
	v: ArrayBuffer;
}

let _dbP: Promise<IDBDatabase | null> | null = null;

/** Open (once) the IndexedDB connection. Resolves null if indexedDB is
 *  unavailable or the open fails, so callers degrade to network-only. */
function dbConn(): Promise<IDBDatabase | null> {
	if (typeof indexedDB === 'undefined') return Promise.resolve(null);
	if (!_dbP) {
		_dbP = new Promise((res) => {
			const r = indexedDB.open(DBN, 1);
			r.onupgradeneeded = () => {
				if (!r.result.objectStoreNames.contains(STORE)) r.result.createObjectStore(STORE);
			};
			r.onsuccess = () => res(r.result);
			r.onerror = () => res(null);
		});
	}
	return _dbP;
}

/** Read a cached bundle buffer by key, honouring version match and TTL. */
function idbGet(k: string, ver: string): Promise<ArrayBuffer | null> {
	return dbConn().then(
		(db) =>
			!db
				? null
				: new Promise<ArrayBuffer | null>((res) => {
						const q = db.transaction(STORE).objectStore(STORE).get(k);
						q.onsuccess = () => {
							const r = q.result as CacheRow | undefined;
							res(
								r && r.v !== undefined && r.ver === ver && Date.now() - r.t < CACHE_TTL
									? r.v
									: null
							);
						};
						q.onerror = () => res(null);
					})
	);
}

/** Write a bundle buffer into the cache under key `k` with version `ver`. */
function idbSet(k: string, ver: string, v: ArrayBuffer): Promise<boolean> {
	return dbConn().then((db) => {
		if (!db) return false;
		const row: CacheRow = { t: Date.now(), ver, v };
		db.transaction(STORE, 'readwrite').objectStore(STORE).put(row, k);
		return true;
	});
}

/**
 * Load a tile bundle and merge its tiles into `archive`. Tries the IndexedDB
 * cache (keyed by file + version) first; on a miss, fetches
 * `baseUrl + '/' + bundle.file`, caches the bytes, then decodes. Returns the
 * number of bytes loaded (decoded), for byte accounting.
 */
export async function loadBundle(
	baseUrl: string,
	bundle: BundleRef,
	archive: TileArchive
): Promise<number> {
	const key = bundle.file;
	let buf = await idbGet(key, bundle.ver);
	if (!buf) {
		const r = await fetch(baseUrl + '/' + bundle.file);
		buf = await r.arrayBuffer();
		idbSet(key, bundle.ver, buf);
	}
	const tiles = decodeBundle(buf);
	for (const k in tiles) archive[k] = tiles[k];
	return buf.byteLength;
}
