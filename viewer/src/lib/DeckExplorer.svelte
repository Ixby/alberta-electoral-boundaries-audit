<!--
  DeckExplorer — the production deck.gl map explorer for the boundary audit.

  Ports the validated prototype (viewer/static/spike/index.html) into a Svelte 5
  component, MINUS all dev/debug chrome (no HUD, no ?debug instrumentation, no
  JS-error-to-HUD handlers). The framework-free data + layer logic lives in
  $lib/deckExplorer/{loader,layers,pois}; this component wires them into a live
  deck.gl map: critical-path data load, lazy LOD tile streaming, the paint loop,
  the map-version toggles, the zoom slider + resolution readout, the three layer
  filters with zoom auto-enable, the hover tooltip, and POI pin click / deep-link.

  deck.gl is imported DYNAMICALLY in onMount so adapter-static prerender (which
  runs in node, no WebGL) never imports it. All browser-only work is in onMount.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import {
		loadBundle,
		tileLevelForZoom,
		levelsToKeep,
		type TileArchive,
		type TileFeature,
		type BundleRef
	} from '$lib/deckExplorer/loader';
	import {
		MAPS,
		MAP_RGB,
		buildEdLayers,
		buildVaLayer,
		buildHairlines,
		buildBasemap,
		buildPois,
		edgeBbox,
		bboxIntersects,
		padBbox,
		type Edge,
		type Bbox
	} from '$lib/deckExplorer/layers';
	import { FLAGS } from '$lib/deckExplorer/pois';
	import { buildNameIndex, matchNames, type NameIndex, type EdRec } from '$lib/deckExplorer/search';
	import { track, zoomBucket } from '$lib/analytics';

	// ── Props ────────────────────────────────────────────────────────────────
	// base: SvelteKit base path (pass `base` from $app/paths at the call site so
	//   all asset fetches are base-path-safe under a non-root deployment).
	// initialPoi: a FLAGS id to open focused on (deep link from the report).
	let { base = '', initialPoi = null }: { base?: string; initialPoi?: string | null } = $props();

	// ── Diagnostic HUD (debug-only) ────────────────────────────────────────────
	// A perf HUD ported from the prototype, shown ONLY at ?debug=1. `browser`
	// short-circuits so `location` is never read during SSR / prerender (the deck
	// component is prerendered in node). The HUD is written imperatively via
	// hudEl.innerHTML inside the paint loop — no reactive state on the hot path.
	const APP_VERSION = 'v1'; // viewer component version (bump on meaningful changes)
	const DEBUG = browser && new URLSearchParams(location.search).has('debug');
	let hudEl = $state<HTMLDivElement | undefined>(undefined);

	// ── Agreement-dash presets ─────────────────────────────────────────────────
	// Where 2+ maps share a boundary the line is drawn as an alternating-colour
	// dash (one solid sub-segment per agreeing map, cycling). `px` is the target
	// dash length in SCREEN pixels (converted to world units per-paint from the
	// view scale); `gap` is the skipped fraction after each dash (0 = continuous
	// barber-pole, >0 = dash-with-gap). Switch via `?dash=<name>` (default medium).
	const DASH_PRESETS: Record<string, { px: number; gap: number }> = {
		tight: { px: 6, gap: 0 },
		medium: { px: 9, gap: 0 },
		long: { px: 14, gap: 0 },
		dashdot: { px: 9, gap: 0.5 }
	};
	const dashParam = browser ? new URLSearchParams(location.search).get('dash') : null;
	const DASH = DASH_PRESETS[dashParam ?? ''] ?? DASH_PRESETS.medium;

	// ── Reactive UI state ──────────────────────────────────────────────────────
	let activeMaps = $state<string[]>(['minority', 'majority', '2019']);
	let filters = $state<{ hwy: boolean; water: boolean; pois: boolean }>({
		hwy: false,
		water: false,
		pois: true
	});
	let zoomVal = $state(0); // slider value (== viewState.zoom)
	let zoomMin = $state(0);
	let zoomMax = $state(1);
	let resText = $state('—'); // "1 pixel ≈ X" readout body

	// ── Search state (district-name autocomplete) ────────────────────────────────
	let searchQuery = $state('');
	let searchResults = $state<EdRec[]>([]);
	let searchActive = $state(-1); // highlighted dropdown index (keyboard nav)
	let searchOpen = $state(false);

	// Control panel collapse. Defaults collapsed on touch/coarse-pointer devices
	// (set on mount) so the panel doesn't bury the map on phones; expanded on
	// desktop. Toggleable everywhere via the panel header.
	let panelCollapsed = $state(false);

	// DOM refs
	let mapEl: HTMLDivElement;
	let canvasEl: HTMLCanvasElement;
	let tipEl: HTMLDivElement;
	let searchInputEl: HTMLInputElement;

	// Bridges from the onMount closure to template event handlers (assigned in onMount).
	let zoomSetter: (z: number) => void = () => {};
	let dragSetter: (v: boolean) => void = () => {};
	let mapToggler: (mk: string) => void = () => {};
	let filterSetter: (which: 'hwy' | 'water' | 'pois', val: boolean) => void = () => {};
	let edSelector: (rec: EdRec) => void = () => {};

	// Non-reactive search index (built once ed_index loads in onMount).
	let nameIndex: NameIndex | null = null;

	const isActive = (mk: string) => activeMaps.includes(mk);
	const rgbCss = (mk: string) => {
		const c = MAP_RGB[mk];
		return c ? `rgb(${c[0]},${c[1]},${c[2]})` : '#9fb4d4';
	};
	// Button styling: filled when on, outlined when off (a live legend).
	function btnStyle(mk: string): string {
		const c = MAP_RGB[mk];
		if (!c) return '';
		const rgb = `rgb(${c[0]},${c[1]},${c[2]})`;
		const dark = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] > 150 ? '#1a2230' : '#fff';
		return isActive(mk)
			? `border-color:${rgb};background:${rgb};color:${dark}`
			: `border-color:${rgb};background:transparent;color:${rgb}`;
	}

	// ── Search handlers (reactive UI side; the fly-to lives in onMount) ──────────
	function runSearch() {
		searchResults = nameIndex ? matchNames(nameIndex, searchQuery) : [];
		searchActive = -1;
		searchOpen = searchResults.length > 0;
	}
	function chooseResult(rec: EdRec) {
		searchQuery = rec.name;
		searchResults = [];
		searchActive = -1;
		searchOpen = false;
		edSelector(rec);
		// Fire-and-forget analytics: which district was selected (name only — the
		// collector's allow-list for district_select is { name }).
		track('district_select', { name: rec.name });
		if (searchInputEl) searchInputEl.blur();
	}
	function onSearchKeydown(e: KeyboardEvent) {
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			if (!searchOpen || !searchResults.length) return;
			searchActive = searchActive < 0 ? 0 : Math.min(searchResults.length - 1, searchActive + 1);
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			if (!searchOpen || !searchResults.length) return;
			searchActive = searchActive <= 0 ? 0 : searchActive - 1;
		} else if (e.key === 'Enter') {
			e.preventDefault();
			const target =
				searchActive >= 0
					? searchResults[searchActive]
					: searchResults.length === 1
						? searchResults[0]
						: null;
			if (target) chooseResult(target);
		} else if (e.key === 'Escape') {
			searchQuery = '';
			searchResults = [];
			searchActive = -1;
			searchOpen = false;
		}
	}

	onMount(() => {
		let cleanup: (() => void) | null = null;
		let disposed = false;

		(async () => {
			// Dynamic, browser-only deck.gl import (keeps prerender working).
			const { Deck, OrthographicView, COORDINATE_SYSTEM } = await import('@deck.gl/core');
			const { PolygonLayer, PathLayer, ScatterplotLayer } = await import('@deck.gl/layers');
			const { PathStyleExtension } = await import('@deck.gl/extensions');
			if (disposed) return;

			// First-paint timing markers (debug HUD). performance.now() is ms from
			// timeOrigin (≈ navigation), the same basis as the prototype's number.
			// tLib: deck.gl dynamic import resolved; tAssets/tDeck set further down.
			const tLib = DEBUG ? performance.now() : 0;
			let tAssets = 0;
			let tDeck = 0;

			// Analytics: the explorer overlay is now live (fire-and-forget).
			track('explorer_open');

			const deckClasses = {
				PolygonLayer,
				PathLayer,
				ScatterplotLayer,
				PathStyleExtension,
				COORDINATE_SYSTEM
			};
			const CART = COORDINATE_SYSTEM.CARTESIAN;
			const DPR = Math.min(window.devicePixelRatio || 1, 1.5);

			// ── Module-local (non-reactive) data state ─────────────────────────────
			interface Manifest {
				version?: string;
				side: number;
				minZoom: number;
				maxZoom: number;
				bbox: [number, number, number, number];
				maps: string[];
				bundles: (BundleRef & { lo: number; hi: number })[];
				// Debug HUD only: per-level byte totals and tile counts (keyed by level).
				levelBytes?: Record<string, number>;
				tileCounts?: Record<string, number>;
			}
			let M: Manifest;
			let lastVS: Record<string, number | number[]> | null = null;
			let provinceData: number[][][] = [];
			let vaProps: { fill?: [number, number, number]; [k: string]: unknown }[] = [];
			const archive: TileArchive = {};
			let edEdges: Edge[] = [];
			// Per-edge world bbox, parallel-indexed to `edEdges`. Precomputed ONCE when
			// ed_edges.json loads so the per-paint viewport cull is a cheap box test.
			let edBboxes: Bbox[] = [];
			let vaLines: number[][][] = [];
			const labels: Record<string, Record<number, string>> = {};
			let waterData: { path: number[][] }[] | null = null;
			let highwaysData: { path: number[][]; major?: boolean }[] | null = null;
			let secondaryData: { path: number[][] }[] | null = null;
			let trunkData: { path: number[][] }[] | null = null;

			let deckgl: InstanceType<typeof Deck> | null = null;
			// Currently selected district (from search) — drives the boundary glow.
			let selectedEd: EdRec | null = null;
			let curLevel = 0;
			// Last zoom_depth bucket reported to analytics. The tile level L is the
			// discrete zoom signal computed each paint; we only emit when its bucket
			// changes (so the event fires on settle / level change, not every frame).
			let lastZoomBucket: string | null = null;
			let draggingZoom = false;
			let paintScheduled = false;
			const lazyTriggered = new Set<string>();

			// ── Debug HUD counters (only mutated/read when DEBUG) ──────────────────
			let firstPaintMs = 0; // ms from navigation to first map paint
			let lastPaintMs = 0; // duration of the most recent paint() layer build + submit
			let bundlesLoaded = 0;
			let bundleTotal = 0;
			let archiveBytes = 0;
			let lastPolyCount = 0; // visible feature count, stashed by buildLayers

			const dataUrl = (f: string) => `${base}/mapdata/${f}`;
			async function fetchJSON<T>(f: string): Promise<T> {
				const r = await fetch(dataUrl(f), { cache: 'no-store' });
				if (!r.ok) throw new Error('fetch ' + f);
				return r.json() as Promise<T>;
			}
			const tileData = (k: string): TileFeature[] | null => archive[k] || null;
			const edNameFor = (mk: string, id: number) => (labels[mk] && labels[mk][id]) || '';

			// ── Visible-tile + best-available-feature selection (inline in prototype) ──
			const PAD = 2; // extra tile ring so edges stay covered during pan / mobile resize
			function visibleTiles(vp: { getBounds: () => number[] }, L: number): [number, number, number][] {
				const n = 2 ** L;
				const tsize = M.side / n;
				const [minx, miny] = M.bbox;
				const b = vp.getBounds();
				const x0 = Math.max(0, Math.floor((b[0] - minx) / tsize) - PAD);
				const x1 = Math.min(n - 1, Math.floor((b[2] - minx) / tsize) + PAD);
				const y0 = Math.max(0, Math.floor((b[1] - miny) / tsize) - PAD);
				const y1 = Math.min(n - 1, Math.floor((b[3] - miny) / tsize) + PAD);
				const out: [number, number, number][] = [];
				for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++) out.push([L, x, y]);
				return out;
			}
			// Best-available: current-level tile if present, else nearest loaded ancestor.
			function featsForView(keys: [number, number, number][]): TileFeature[] {
				const used = new Set<string>();
				let feats: TileFeature[] = [];
				for (let [z, x, y] of keys) {
					while (z >= M.minZoom) {
						const k = `${z}/${x}/${y}`;
						const t = tileData(k);
						if (t) {
							if (!used.has(k)) {
								used.add(k);
								feats = feats.concat(t);
							}
							break;
						}
						z--;
						x = Math.floor(x / 2);
						y = Math.floor(y / 2);
					}
				}
				return feats;
			}

			// ── ED stroke alpha/width by level (ported) ────────────────────────────
			const edAlpha = (L: number) => (L <= 1 ? 50 : L <= 2 ? 110 : L <= 3 ? 180 : 255);
			const edWidth = (L: number) => (L <= 1 ? 1.2 : L <= 2 ? 1.9 : L <= 3 ? 2.5 : 3.2);

			// ── Lazy LOD: keep levels 0..L+1 loaded, fetch deeper bins only on approach ──
			function maybeLoadLevels(L: number) {
				if (!M) return;
				const keep = new Set(levelsToKeep(L, M.minZoom));
				for (const b of M.bundles) {
					if (keep.has(b.lo) && !lazyTriggered.has(b.file)) {
						lazyTriggered.add(b.file);
						loadBundle(`${base}/mapdata`, b, archive).then((n) => {
							if (DEBUG) {
								archiveBytes += n;
								bundlesLoaded++;
							}
							schedulePaint();
						});
					}
				}
			}

			// ── Lazy detail data (highways / water) ────────────────────────────────
			let hwyLoaded = false;
			function loadHwyData() {
				if (hwyLoaded) return;
				hwyLoaded = true;
				fetchJSON<{ path: number[][] }[]>('trunk.json').then((d) => {
					trunkData = d;
					schedulePaint();
				});
				fetchJSON<{ path: number[][] }[]>('secondary.json').then((d) => {
					secondaryData = d;
					schedulePaint();
				});
				fetchJSON<{ path: number[][]; major?: boolean }[]>('highways.json').then((d) => {
					highwaysData = d;
					schedulePaint();
				});
			}
			let waterLoaded = false;
			function loadWaterData() {
				if (waterLoaded) return;
				waterLoaded = true;
				fetchJSON<{ path: number[][] }[]>('water.json').then((d) => {
					waterData = d;
					schedulePaint();
				});
			}
			// Auto-enable detail layers as the user zooms: highways at level 3, water at 4.
			let hwyAuto = false;
			let waterAuto = false;
			function maybeAutoLayers(L: number) {
				if (L >= 3 && !hwyAuto) {
					hwyAuto = true;
					filters.hwy = true;
					loadHwyData();
					schedulePaint();
				}
				if (L >= 4 && !waterAuto) {
					waterAuto = true;
					filters.water = true;
					loadWaterData();
					schedulePaint();
				}
			}

			// ── Tooltip (ported HTML/markup) ───────────────────────────────────────
			function voteBar(P: { votes?: number; ucp?: number; ndp?: number }): string {
				const u = P.ucp || 0;
				const n = P.ndp || 0;
				return (
					`<div class="vs"><b>${(P.votes || 0).toLocaleString()}</b> in-person votes</div>` +
					`<div class="bar"><span style="width:${u}%;background:#142e94"></span><span style="width:${n}%;background:#e86310"></span></div>` +
					`<div class="barlbl"><span style="color:#142e94">UCP ${u}%</span><span style="color:#c2540e">NDP ${n}%</span></div>`
				);
			}
			function hideTip() {
				if (tipEl) tipEl.style.display = 'none';
			}
			// Position the hover tip near (x, y) but always fully inside the viewport.
			// Defaults to below-right of the cursor; flips to the opposite side when
			// that would overflow, then clamps so it never spills past an edge.
			// Must run AFTER the tip's innerHTML is set so offsetWidth/Height are real.
			function placeTip(x: number, y: number) {
				if (!tipEl) return;
				const m = 8; // min gap from each viewport edge
				const w = tipEl.offsetWidth;
				const h = tipEl.offsetHeight;
				const vw = window.innerWidth;
				const vh = window.innerHeight;
				let left = x + 12;
				if (left + w + m > vw) left = x - 12 - w;
				left = Math.min(Math.max(m, left), Math.max(m, vw - w - m));
				let top = y + 12;
				if (top + h + m > vh) top = y - 12 - h;
				top = Math.min(Math.max(m, top), Math.max(m, vh - h - m));
				tipEl.style.left = left + 'px';
				tipEl.style.top = top + 'px';
			}

			// ── Paint loop ─────────────────────────────────────────────────────────
			function buildLayers(
				L: number,
				keys: [number, number, number][],
				vp: { getBounds: () => number[] }
			) {
				const feats = featsForView(keys);
				if (DEBUG) lastPolyCount = feats.length; // visible feature count for the HUD
				// deck.gl layer instances are opaque here (builders are deck-free / DI); the array is
				// handed straight to deckgl.setProps, which validates them at runtime.
				/* eslint-disable @typescript-eslint/no-explicit-any */
				const layers: any[] = [];
				// Province fill (paper-grey base under the VA polys).
				layers.push(
					new PolygonLayer({
						id: 'province-fill',
						data: provinceData,
						getPolygon: (d: number[][]) => d,
						pickable: true,
						getFillColor: [232, 230, 224],
						stroked: false,
						filled: true,
						coordinateSystem: CART
					})
				);
				// VA fills.
				layers.push(buildVaLayer(deckClasses, feats, vaProps));
				// VA hairline outlines (level >= 3).
				layers.push(...buildHairlines(deckClasses, vaLines, L));
				// Water as filled polygons (handled here — the basemap builder skips water).
				if (filters.water && waterData) {
					layers.push(
						new PolygonLayer({
							id: 'water',
							data: waterData,
							getPolygon: (d: { path: number[][] }) => d.path,
							positionFormat: 'XY',
							filled: true,
							getFillColor: [20, 92, 156, 150],
							stroked: true,
							getLineColor: [8, 64, 124, 235],
							getLineWidth: 0.7,
							lineWidthUnits: 'pixels',
							lineWidthMinPixels: 0.5,
							coordinateSystem: CART
						})
					);
				}
				// Road basemap (highways / secondary / trunk) under filters.hwy + level gating.
				layers.push(
					...buildBasemap(
						deckClasses,
						{ highways: highwaysData, secondary: secondaryData, trunk: trunkData },
						filters,
						L
					)
				);
				// ED boundary overlays (instant toggle — current active maps). Agreement
				// strokes (2+ maps) render as an alternating-colour dash; the dash length
				// is kept ~constant in screen pixels by converting DASH.px to world units
				// via the current OrthographicView scale (2**zoom).
				const scale = 2 ** ((lastVS?.zoom as number) ?? 0);
				const dashWorldLen = DASH.px / scale;
				// Viewport-cull the agreement edges BEFORE chunking. `getBounds()` returns
				// the visible world bounds in the same EPSG:3401 space as the edge geometry
				// (it is the exact source `visibleTiles` already trusts). Pad 25% so edges
				// stay covered through small pans between paints. At deep zoom only a handful
				// of edges' bboxes intersect the tiny window → bounded chunk geometry → no
				// GPU blowup (the per-edge MAX_CHUNKS cap in chunkPath bounds the long-edge
				// case). Each ed_edges.json edge already carries its world path, so an edge
				// whose bbox overlaps the window is chunked fully along its visible length.
				const vb = vp.getBounds() as Bbox;
				const padded = padBbox(vb, 0.25);
				const visibleEdges =
					edBboxes.length === edEdges.length
						? edEdges.filter((_, i) => bboxIntersects(edBboxes[i], padded))
						: edEdges;
				layers.push(
					...buildEdLayers(
						deckClasses,
						activeMaps,
						visibleEdges,
						edAlpha(L),
						edWidth(L),
						dashWorldLen,
						DASH.gap,
						// Clip each agreement edge to the same padded window we culled with,
						// so its dash covers the FULL visible span at deep zoom instead of
						// the per-edge cap "retreating" partway along a long off-screen edge.
						padded
					)
				);
				// Selected-district glow (search result) — drawn under the pins, over the
				// boundary overlays so the highlighted district reads clearly.
				layers.push(...buildSelectedGlow());
				// Annotation pins on top.
				layers.push(...buildPois(deckClasses, FLAGS, filters.pois));
				return layers;
			}

			// ── Selected-ED glow ───────────────────────────────────────────────────
			// The ed_edges geometry is keyed by which maps share each arc, not by
			// district name, so there is no clean per-district boundary to trace by
			// name. Instead we draw a boundary glow assembled from the ed_edges arcs
			// that fall inside the selected district's bbox AND belong to the primary
			// active map, plus a ring marker at the centroid as a reliable anchor (the
			// ring always shows even when the bbox catches no arcs, e.g. very small or
			// edge-of-province districts). The bbox half-side is recovered from the
			// fit-zoom the index stored: zoom = 1 - log2(side / 256)  →  side = 256·2^(1−zoom).
			/* eslint-disable @typescript-eslint/no-explicit-any */
			function buildSelectedGlow(): any[] {
				if (!selectedEd) return [];
				const sel = selectedEd;
				const side = 256 * 2 ** (1 - sel.zoom);
				const half = side / 2;
				const x0 = sel.cx - half,
					x1 = sel.cx + half,
					y0 = sel.cy - half,
					y1 = sel.cy + half;
				const primary = activeMaps.length ? activeMaps[0] : 'minority';
				const bit = (MAPS as readonly string[]).indexOf(primary);
				// The boundary glow is assembled by bbox proximity, which only reads as
				// "this district" for compact (urban / suburban) shapes. For large rural
				// districts the square reaches far enough to catch unrelated arcs, so above
				// a side threshold we skip the path glow and let the ring marker carry it.
				const GLOW_MAX_SIDE = 60000; // m (~60 km) — Calgary/Edmonton EDs are well under this
				const near: { g: number[][] }[] = [];
				if (bit >= 0 && side <= GLOW_MAX_SIDE) {
					for (const e of edEdges) {
						if (!e.m[bit]) continue;
						// Keep an arc if any vertex lands inside the district bbox.
						let hit = false;
						for (const p of e.g) {
							if (p[0] >= x0 && p[0] <= x1 && p[1] >= y0 && p[1] <= y1) {
								hit = true;
								break;
							}
						}
						if (hit) near.push({ g: e.g });
					}
				}
				const out: any[] = [];
				if (near.length) {
					out.push(
						new PathLayer({
							id: 'ed-glow',
							data: near,
							getPath: (d: { g: number[][] }) => d.g as any,
							getColor: [255, 226, 120, 235],
							widthUnits: 'pixels',
							getWidth: 5,
							widthMinPixels: 3,
							capRounded: true,
							jointRounded: true,
							parameters: { depthTest: false },
							coordinateSystem: CART
						})
					);
				}
				// Centroid ring marker — sized to the district (in meters), with a pixel
				// floor so it stays visible at the overview.
				out.push(
					new ScatterplotLayer({
						id: 'ed-glow-ring',
						data: [sel],
						getPosition: (d: EdRec) => [d.cx, d.cy, 0],
						getRadius: half * 0.9,
						radiusUnits: 'meters',
						radiusMinPixels: 10,
						filled: false,
						stroked: true,
						getLineColor: [255, 214, 80, 235],
						getLineWidth: 3,
						lineWidthUnits: 'pixels',
						lineWidthMinPixels: 2,
						parameters: { depthTest: false },
						coordinateSystem: CART
					})
				);
				return out;
			}

			function paint() {
				if (!deckgl || !lastVS || !M) return;
				const vp = new OrthographicView({ flipY: false }).makeViewport({
					width: window.innerWidth,
					height: window.innerHeight,
					viewState: lastVS
				});
				if (!vp) return;
				const L = tileLevelForZoom(lastVS.zoom as number, M.side, M.minZoom, M.maxZoom);
				curLevel = L;
				// Analytics: emit zoom_depth only when the zoom bucket changes (throttle).
				const zb = zoomBucket(L);
				if (zb !== lastZoomBucket) {
					lastZoomBucket = zb;
					track('zoom_depth', { bucket: zb });
				}
				maybeLoadLevels(L);
				maybeAutoLayers(L);
				syncZoomUI(L);
				const t0 = DEBUG ? performance.now() : 0;
				deckgl.setProps({ layers: buildLayers(L, visibleTiles(vp, L), vp) });
				if (DEBUG) {
					lastPaintMs = Math.round((performance.now() - t0) * 10) / 10;
					renderHud(L);
				}
			}

			// ── Debug HUD (only built/written when DEBUG) ──────────────────────────
			// Imperative innerHTML write each paint — mirrors the prototype, keeps the
			// hot path free of reactive state. Injected markup is not scoped by Svelte,
			// so the HUD CSS below uses :global() selectors.
			function renderHud(L: number) {
				if (!hudEl || !M) return;
				const br =
					firstPaintMs && tDeck
						? ` <span style="color:#8aa0c2">[lib ${(tLib - 0) | 0} · assets ${(tAssets - tLib) | 0} · deckctor ${(tDeck - tAssets) | 0} · head+gpu ${(firstPaintMs - tDeck) | 0}]</span>`
						: '';
				// Per-level byte / tile table (from manifest levelBytes + tileCounts).
				let table = '';
				if (M.levelBytes && M.tileCounts) {
					let cum = 0;
					let rows = '';
					for (let z = M.minZoom; z <= M.maxZoom; z++) {
						const tol = M.side / 2 ** z / 256;
						const mb = (M.levelBytes[z] || 0) / 1e6;
						cum += mb;
						const tolS = tol >= 1000 ? (tol / 1000).toFixed(1) + 'km' : Math.round(tol) + 'm';
						const cls = 'lv' + (z === L ? ' cur' : '');
						rows +=
							`<span class="${cls}">z${z} ${tolS.padStart(6)} ` +
							`${String(M.tileCounts[z] || 0).padStart(6)}t ${mb.toFixed(2)}MB Σ${cum.toFixed(1)}</span>`;
					}
					table = `<div class="lvt">${rows}</div>`;
				}
				const heap =
					typeof performance !== 'undefined' &&
					(performance as unknown as { memory?: { usedJSHeapSize: number } }).memory
						? ` · heap <b>${((performance as unknown as { memory: { usedJSHeapSize: number } }).memory.usedJSHeapSize / 1e6) | 0}MB</b>`
						: '';
				hudEl.innerHTML =
					`<b>deck.gl · EPSG:3401</b> &nbsp; <b>${activeMaps.join('+') || 'fills only'}</b> &nbsp; ` +
					`<span style="color:#8aa0c2">data <b>${M.version || '?'}</b> · app <b>${APP_VERSION}</b></span><br>` +
					`level <b>${L}</b>/${M.maxZoom} &nbsp; polys <b>${lastPolyCount}</b> &nbsp; ` +
					`loaded <b>${bundlesLoaded}/${bundleTotal}</b> · <b>${(archiveBytes / 1e6).toFixed(1)}MB</b>${heap}<br>` +
					`first paint <b>${firstPaintMs ? firstPaintMs + 'ms' : '…'}</b>${br} &nbsp; last paint <b>${lastPaintMs}ms</b>` +
					table;
			}
			function schedulePaint() {
				if (paintScheduled) return;
				paintScheduled = true;
				requestAnimationFrame(() => {
					paintScheduled = false;
					paint();
				});
			}
			function syncZoomUI(L: number) {
				if (!M || !lastVS) return;
				if (!draggingZoom) zoomVal = lastVS.zoom as number;
				const tol = M.side / 2 ** L / 256;
				resText = tol >= 1000 ? (tol / 1000).toFixed(1) + ' km' : Math.round(tol) + ' m';
			}
			function update(vs: Record<string, number | number[]>) {
				lastVS = vs;
				if (deckgl) deckgl.setProps({ viewState: vs });
				paint();
			}
			function setZoom(z: number) {
				if (!lastVS) return;
				z = Math.max(lastVS.minZoom as number, Math.min(lastVS.maxZoom as number, z));
				update({ ...lastVS, zoom: z });
			}
			// Expose for slider handlers in the template.
			zoomSetter = setZoom;
			dragSetter = (v: boolean) => {
				draggingZoom = v;
			};
			// Map-version toggle: instant switch (no crossfade), kept in MAPS order.
			mapToggler = (mk: string) => {
				if (isActive(mk)) activeMaps = activeMaps.filter((m) => m !== mk);
				else activeMaps = MAPS.filter((m) => m === mk || isActive(m));
				// Analytics: which map version was toggled (on or off).
				track('map_toggle', { map: mk });
				schedulePaint();
			};
			// Filter checkbox handlers (lazy-load data on manual enable).
			filterSetter = (which: 'hwy' | 'water' | 'pois', val: boolean) => {
				filters[which] = val;
				if (which === 'hwy' && val) loadHwyData();
				if (which === 'water' && val) loadWaterData();
				// Analytics: user-driven layer toggle. (The zoom auto-enable in
				// maybeAutoLayers flips these programmatically and is intentionally
				// NOT logged — only genuine user toggles count.)
				track('layer_toggle', { layer: which, on: val });
				schedulePaint();
			};
			// Search → fly to the chosen district and glow it. Clamp the fit-zoom to
			// the deck view's min/max so an off-range index value can't desync the UI.
			edSelector = (rec: EdRec) => {
				selectedEd = rec;
				if (!lastVS) return;
				const z = Math.max(
					lastVS.minZoom as number,
					Math.min(lastVS.maxZoom as number, rec.zoom)
				);
				update({ ...lastVS, target: [rec.cx, rec.cy, 0], zoom: z });
			};

			// ── Critical path load ─────────────────────────────────────────────────
			M = await fetchJSON<Manifest>('manifest.json');
			provinceData = await fetchJSON<number[][][]>('province.json');
			vaProps = await fetchJSON('va_props.json');
			if (disposed) return;
			if (DEBUG) {
				bundleTotal = M.bundles.length;
				tAssets = performance.now();
			}

			const [minx, miny, maxx, maxy] = M.bbox;
			const cx = (minx + maxx) / 2;
			const cy = (miny + maxy) / 2;
			const z = 1 - Math.log2(M.side / 256); // level 1 — the default opening overview
			// Floor the camera at the coarsest tile level (z0) rather than level 1, so the province
			// can be pulled back for breathing room — and the z0 tiles stop being dead weight.
			const zFloor = M.minZoom - Math.log2(M.side / 256);
			const initial: Record<string, number | number[]> = {
				target: [cx, cy, 0],
				zoom: z,
				minZoom: zFloor,
				maxZoom: z + 22
			};
			// Deep link: open focused on the named pin at ~level 6.
			const poiFlag = initialPoi ? FLAGS.find((f) => f.id === initialPoi) : null;
			if (poiFlag) {
				initial.target = [poiFlag.x, poiFlag.y, 0];
				initial.zoom = Math.min(initial.maxZoom as number, 6 - Math.log2(M.side / 256));
			}

			// Slider bounds: z0 (fully pulled-back overview) → maxZoom (finest data scale).
			zoomMin = +zFloor.toFixed(2);
			zoomMax = +(M.maxZoom - Math.log2(M.side / 256)).toFixed(2);
			zoomVal = initial.zoom as number;

			// Touch devices: start with the control panel collapsed so it doesn't
			// bury the map on a phone screen (the screenshot problem). Desktop stays
			// expanded. Either way the user can toggle from the panel header.
			panelCollapsed = window.matchMedia?.('(pointer: coarse)').matches === true;

			// Explicit, sized canvas (defensive — set canvas/width/height and keep in sync).
			canvasEl.width = window.innerWidth;
			canvasEl.height = window.innerHeight;

			lastVS = initial;
			deckgl = new Deck({
				canvas: canvasEl,
				width: window.innerWidth,
				height: window.innerHeight,
				views: new OrthographicView({ flipY: false }),
				viewState: initial, // controlled, so the zoom slider can drive it
				controller: { scrollZoom: { smooth: true } },
				useDevicePixels: DPR,
				// deck.gl picking callbacks: typed loosely (deck's PickingInfo is runtime-imported).
				onHover: (info: any) => {
					const o = info.object as
						| { id?: number; title?: string; body?: string }
						| undefined;
					if (!o) {
						hideTip();
						return;
					}
					tipEl.style.display = 'block';
					if (info.layer && info.layer.id === 'flags') {
						tipEl.innerHTML =
							`<div class="n">${o.title}</div><div class="flagbody">${o.body}</div>` +
							`<div class="flaglink">Click to zoom in</div>`;
					} else if (info.layer && info.layer.id === 'va') {
						const P = (vaProps[o.id as number] || {}) as {
							name?: string;
							community?: string;
							cin?: boolean;
							fill?: [number, number, number];
							ucp?: number;
							ndp?: number;
							votes?: number;
						};
						const shown = activeMaps.length ? activeMaps : ['minority'];
						const names = shown.map((mk) => edNameFor(mk, o.id as number) || '(unassigned)');
						const agree = names.every((n) => n === names[0]);
						const ed = names[0];
						const distCmp = agree
							? ''
							: `<div class="vs">` +
								shown
									.map(
										(mk, i) =>
											`<span style="color:${rgbCss(mk)}">■</span> ${names[i]}`
									)
									.join('<br>') +
								`</div>`;
						const title = agree ? ed : P.name;
						const where = P.community
							? `${P.name == title ? '' : P.name + ' · '}${P.cin ? 'in' : 'near'} ${P.community}`
							: P.name == title
								? ''
								: P.name;
						const pale = P.fill && P.fill[0] + P.fill[1] + P.fill[2] >= 666;
						if (pale) {
							const some = (P.ucp || 0) + (P.ndp || 0) > 0;
							tipEl.innerHTML =
								`<div class="n">${title}</div>${where}${distCmp}` +
								(some ? voteBar(P) : ``) +
								`<div class="note">${
									some
										? "A sparsely populated area — with few votes cast here, the colour stays close to the map's neutral baseline."
										: "No votes were recorded here, so this area shows the map's neutral baseline tone."
								}</div>`;
						} else {
							tipEl.innerHTML = `<div class="n">${title}</div>${where}${distCmp}` + voteBar(P);
						}
					} else {
						tipEl.innerHTML =
							`<div class="n">No one votes here</div>No polling division covers this spot — nobody is recorded living or voting here, so it stays the map's neutral tone.`;
					}
					// Content is set; now place the tip clamped to the viewport.
					placeTip(info.x, info.y);
				},
				onViewStateChange: ({ viewState }: any) => {
					update(viewState);
				},
				onClick: (info: any) => {
					if (info.layer && info.layer.id === 'flags' && info.object) {
						// Analytics: a POI pin was clicked (fire-and-forget).
						track('poi_open', { id: String(info.object.id) });
						const tz = 6 - Math.log2(M.side / 256); // level 6
						update({
							...lastVS!,
							target: [info.object.x, info.object.y, 0],
							zoom: Math.min(
								lastVS!.maxZoom as number,
								Math.max(lastVS!.minZoom as number, tz)
							)
						});
					}
				},
				layers: []
			});
			deckgl.setProps({ width: window.innerWidth, height: window.innerHeight });
			if (DEBUG) tDeck = performance.now();

			// Keep deck sized to the viewport (mobile address bars resize it).
			const onResize = () => {
				canvasEl.width = window.innerWidth;
				canvasEl.height = window.innerHeight;
				deckgl!.setProps({ width: window.innerWidth, height: window.innerHeight });
				schedulePaint();
			};
			window.addEventListener('resize', onResize);
			if (window.visualViewport) window.visualViewport.addEventListener('resize', onResize);

			// ── Post-paint layer data (value-ordered) ──────────────────────────────
			async function loadEd() {
				const ee = await fetchJSON<{ edges: Edge[]; outline: number[][] }>('ed_edges.json');
				edEdges = ee.edges;
				// Precompute each edge's world bbox once (parallel array) for the per-paint
				// viewport cull. ~2790 edges → a one-time O(vertices) pass, never per frame.
				edBboxes = edEdges.map(edgeBbox);
				schedulePaint();
			}
			async function loadLabels() {
				for (const mk of M.maps) labels[mk] = await fetchJSON('valabels_' + mk + '.json');
			}
			async function loadVaLines() {
				vaLines = await fetchJSON<number[][][]>('va_lines.json');
				schedulePaint();
			}
			// District-name search index for the primary (first active) map. The names
			// shown in search come from this map; selecting flies to its centroid.
			async function loadEdIndex() {
				const primary = activeMaps.length ? activeMaps[0] : 'minority';
				const recs = await fetchJSON<EdRec[]>('ed_index_' + primary + '.json');
				nameIndex = buildNameIndex(recs);
			}

			// View-first load: gate first paint on the bundle covering the initial level.
			let L0 = tileLevelForZoom(initial.zoom as number, M.side, M.minZoom, M.maxZoom);
			const head = M.bundles.find((b) => b.lo <= L0 && L0 <= b.hi) || M.bundles[0];
			lazyTriggered.add(head.file);
			const headBytes = await loadBundle(`${base}/mapdata`, head, archive);
			if (DEBUG) {
				archiveBytes += headBytes;
				bundlesLoaded++;
			}
			if (disposed) return;
			update(initial);
			// Capture first paint with an idle main thread, BEFORE any further loading.
			if (DEBUG) {
				await new Promise<void>((r) =>
					requestAnimationFrame(() => {
						firstPaintMs = Math.round(performance.now());
						schedulePaint();
						r();
					})
				);
			}
			await loadEd();
			await loadLabels();
			await loadEdIndex();
			if (poiFlag) {
				// Surface the focused pin's note on arrival (deep link).
				const vp = new OrthographicView({ flipY: false }).makeViewport({
					width: window.innerWidth,
					height: window.innerHeight,
					viewState: lastVS!
				});
				const [sx, sy] = vp ? vp.project([poiFlag.x, poiFlag.y]) : [0, 0];
				tipEl.style.display = 'block';
				tipEl.style.left = sx + 14 + 'px';
				tipEl.style.top = sy + 14 + 'px';
				tipEl.innerHTML = `<div class="n">${poiFlag.title}</div><div class="flagbody">${poiFlag.body}</div>`;
			}
			maybeLoadLevels(L0); // backfill coarse + one level lookahead
			await loadVaLines();

			cleanup = () => {
				window.removeEventListener('resize', onResize);
				if (window.visualViewport) window.visualViewport.removeEventListener('resize', onResize);
				if (deckgl) deckgl.finalize();
			};
		})();

		return () => {
			disposed = true;
			if (cleanup) cleanup();
		};
	});
</script>

<div class="explorer">
	<div class="map" bind:this={mapEl}>
		<canvas bind:this={canvasEl}></canvas>
	</div>

	<div class="mapsw" class:collapsed={panelCollapsed}>
		<button
			type="button"
			class="mapsw-toggle"
			aria-expanded={!panelCollapsed}
			aria-controls="mapsw-body"
			onclick={() => (panelCollapsed = !panelCollapsed)}
		>
			<span class="mapsw-title">Map controls</span>
			<span class="chev" aria-hidden="true">{panelCollapsed ? '▾' : '▴'}</span>
		</button>

		<div class="mapsw-body" id="mapsw-body">
		<div class="search">
			<input
				class="search-input"
				type="text"
				placeholder="Search a district…"
				autocomplete="off"
				bind:this={searchInputEl}
				bind:value={searchQuery}
				oninput={runSearch}
				onkeydown={onSearchKeydown}
				onfocus={() => {
					if (searchResults.length) searchOpen = true;
				}}
				onblur={() => {
					searchOpen = false;
				}}
			/>
			{#if searchOpen && searchResults.length}
				<ul class="search-results" role="listbox">
					{#each searchResults as r, i (r.name)}
						<li
							role="option"
							aria-selected={i === searchActive}
							class:sr-active={i === searchActive}
							onmousedown={(e) => {
								e.preventDefault();
								chooseResult(r);
							}}
							onmouseenter={() => (searchActive = i)}
						>
							{r.name}
						</li>
					{/each}
				</ul>
			{/if}
		</div>

		<div class="hdr">Map version <span>· click to toggle</span></div>
		<div class="btns">
			{#each MAPS as mk (mk)}
				<button
					data-m={mk}
					style={btnStyle(mk)}
					title="Toggle this map on/off"
					onclick={() => mapToggler(mk)}
				>
					{mk === '2019' ? '2019' : mk === 'minority' ? 'Minority' : 'Majority'}
				</button>
			{/each}
		</div>

		<input
			class="zoom"
			type="range"
			min={zoomMin}
			max={zoomMax}
			step="0.01"
			bind:value={zoomVal}
			oninput={() => {
				dragSetter(true);
				zoomSetter(zoomVal);
			}}
			onchange={() => dragSetter(false)}
		/>
		<div class="res">1 pixel ≈ <b>{resText}</b></div>

		<div class="filters">
			<div class="fhdr">Geographic filters</div>
			<label>
				<input
					type="checkbox"
					checked={filters.hwy}
					onchange={(e) => filterSetter('hwy', e.currentTarget.checked)}
				/> Highways
			</label>
			<label>
				<input
					type="checkbox"
					checked={filters.water}
					onchange={(e) => filterSetter('water', e.currentTarget.checked)}
				/> Rivers &amp; lakes
			</label>
			<label>
				<input
					type="checkbox"
					checked={filters.pois}
					onchange={(e) => filterSetter('pois', e.currentTarget.checked)}
				/> Annotations
			</label>
		</div>

		<div class="lines-note">
			<b>Reading the lines</b><br />
			Every odd shape or split line is a <b>deliberate choice by the committee</b> — not a data error.
			Lines follow the edges of polling areas; where two maps agree they sit on the same line, where
			they split apart the proposals genuinely disagree.
		</div>
		</div>
	</div>

	<div class="tip" bind:this={tipEl}></div>

	{#if DEBUG}
		<div class="hud" bind:this={hudEl}>loading…</div>
	{/if}
</div>

<style>
	.explorer {
		position: relative;
		width: 100%;
		height: 100%;
		/* Warm near-black behind the map (deck.gl clears transparent, so this shows
		   through around the province silhouette). Replaces the cold navy #0c0f1a. */
		background: #1a1511;
		font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
	}
	.map {
		position: absolute;
		inset: 0;
	}
	.map canvas {
		width: 100%;
		height: 100%;
		display: block;
	}
	.mapsw {
		position: absolute;
		top: 10px;
		right: 10px;
		z-index: 6;
		display: flex;
		flex-direction: column;
		gap: 6px;
		background: rgba(18, 16, 13, 0.84);
		padding: 7px 7px 6px;
		border-radius: 10px;
		border: 1px solid #3a342a;
		max-height: calc(100% - 20px);
		overflow-y: auto;
	}
	/* Collapsed: only the header toggle remains; the panel shrinks to a pill. */
	.mapsw.collapsed {
		overflow: visible;
	}
	.mapsw.collapsed .mapsw-body {
		display: none;
	}
	.mapsw-toggle {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		width: 100%;
		background: none;
		border: none;
		padding: 1px 2px;
		cursor: pointer;
		color: #cbb89c;
	}
	.mapsw-title {
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 0.02em;
	}
	.mapsw-toggle .chev {
		font-size: 11px;
		line-height: 1;
		color: #8a7d66;
	}
	.mapsw-body {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}
	.mapsw .hdr {
		font-size: 11px;
		font-weight: 600;
		color: #9fb4d4;
		padding: 0 2px;
	}
	.mapsw .hdr span {
		font-weight: 400;
		font-size: 10px;
		color: #6b7d99;
	}
	.mapsw .search {
		position: relative;
	}
	.mapsw .search-input {
		width: 100%;
		box-sizing: border-box;
		background: #11182a;
		border: 1px solid #2a3550;
		border-radius: 7px;
		color: #e6eefb;
		font: 400 13px -apple-system, 'Segoe UI', sans-serif;
		padding: 7px 9px;
		outline: none;
	}
	.mapsw .search-input:focus {
		border-color: #6fd3fb;
	}
	.mapsw .search-input::placeholder {
		color: #6b7d99;
	}
	.mapsw .search-results {
		position: absolute;
		top: calc(100% + 3px);
		left: 0;
		right: 0;
		z-index: 8;
		margin: 0;
		padding: 4px;
		list-style: none;
		max-height: 240px;
		overflow-y: auto;
		background: rgba(12, 15, 26, 0.97);
		border: 1px solid #2a3550;
		border-radius: 8px;
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
	}
	.mapsw .search-results li {
		padding: 6px 8px;
		border-radius: 5px;
		font-size: 12.5px;
		color: #cfe0f5;
		cursor: pointer;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.mapsw .search-results li.sr-active {
		background: #1f6feb;
		color: #fff;
	}
	.mapsw .btns {
		display: flex;
		gap: 5px;
	}
	.mapsw button {
		border: 1px solid transparent;
		background: none;
		color: #9fb4d4;
		font: 600 13px -apple-system, 'Segoe UI', sans-serif;
		padding: 6px 12px;
		border-radius: 7px;
		cursor: pointer;
	}
	.mapsw .zoom {
		width: 100%;
		margin: 6px 0 2px;
		accent-color: #6fd3fb;
		cursor: pointer;
	}
	.mapsw .res {
		font-size: 11px;
		color: #9fb4d4;
		text-align: center;
	}
	.mapsw .res b {
		color: #6fd3fb;
	}
	.mapsw .lines-note {
		font-size: 11px;
		color: #9fb4d4;
		line-height: 1.5;
		margin-top: 7px;
		padding-top: 7px;
		border-top: 1px solid #2a3550;
		max-width: 228px;
	}
	.mapsw .lines-note b {
		color: #cfe0f5;
	}
	.mapsw .filters {
		margin-top: 7px;
		padding-top: 6px;
		border-top: 1px solid #2a3550;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.mapsw .filters .fhdr {
		font-size: 11px;
		font-weight: 600;
		color: #9fb4d4;
	}
	.mapsw .filters label {
		font-size: 12px;
		color: #cfe0f5;
		display: flex;
		align-items: center;
		gap: 6px;
		cursor: pointer;
	}
	.mapsw .filters input {
		accent-color: #6fd3fb;
		cursor: pointer;
	}
	.tip {
		position: absolute;
		z-index: 6;
		pointer-events: none;
		background: #f9f7f2;
		color: #1a2e45;
		padding: 9px 12px;
		border-radius: 8px;
		font-size: 13.5px;
		line-height: 1.45;
		box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
		display: none;
		max-width: 250px;
	}
	.tip :global(.n) {
		font-weight: 600;
		font-family: Palatino, Georgia, serif;
		font-size: 15px;
		margin-bottom: 3px;
	}
	.tip :global(.vs) {
		white-space: nowrap;
		margin-top: 7px;
		padding-top: 6px;
		border-top: 1px solid #e6e0d2;
	}
	.tip :global(.bar) {
		display: flex;
		height: 9px;
		border-radius: 5px;
		overflow: hidden;
		margin-top: 7px;
		box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.12);
	}
	.tip :global(.barlbl) {
		display: flex;
		justify-content: space-between;
		font-size: 12.5px;
		font-weight: 600;
		margin-top: 4px;
	}
	.tip :global(.note) {
		font-size: 12px;
		color: #6b7280;
		margin-top: 7px;
		line-height: 1.4;
	}
	.tip :global(.flagbody) {
		font-size: 12.5px;
		color: #3a4658;
		margin-top: 5px;
		line-height: 1.5;
		max-width: 260px;
	}
	.tip :global(.flaglink) {
		font-size: 11.5px;
		color: #1763c8;
		margin-top: 6px;
		font-weight: 600;
	}
	/* Debug-only diagnostic HUD (?debug=1). Ported from the prototype's #hud.
	   Contents are injected via innerHTML, so child selectors use :global(). */
	.hud {
		position: absolute;
		top: 10px;
		left: 10px;
		z-index: 5;
		background: rgba(12, 15, 26, 0.82);
		color: #cfe0f5;
		padding: 10px 13px;
		border-radius: 9px;
		font-size: 12.5px;
		line-height: 1.55;
		border: 1px solid #2a3550;
		min-width: 230px;
		/* Selectable so the diagnostics can be highlighted + copied (e.g. to paste timings). */
		pointer-events: auto;
		user-select: text;
		-webkit-user-select: text;
		cursor: text;
	}
	.hud :global(b) {
		color: #6fd3fb;
	}
	.hud :global(.lvt) {
		font-family: ui-monospace, Consolas, monospace;
		font-size: 11px;
		line-height: 1.5;
		margin: 6px 0 0;
		padding: 5px 0 0;
		border-top: 1px solid #2a3550;
	}
	.hud :global(.lv) {
		display: block;
		color: #9fb4d4;
		padding: 0 4px;
		border-radius: 3px;
		white-space: pre;
	}
	.hud :global(.lv.cur) {
		color: #eaf2ff;
		font-weight: 600;
	}

	@media (pointer: coarse) {
		.tip {
			font-size: 16px;
			max-width: 80vw;
		}
		.tip :global(.n) {
			font-size: 18px;
		}
		.tip :global(.barlbl) {
			font-size: 14px;
		}
		.tip :global(.note) {
			font-size: 14px;
		}
		/* Phones: keep the panel compact instead of enlarging it. Cap its width,
		   shrink the map-version buttons, and tighten the verbose copy so the
		   expanded panel never dominates the map. */
		.mapsw {
			max-width: 76vw;
			gap: 5px;
		}
		.mapsw .hdr {
			font-size: 11px;
		}
		.mapsw .hdr span {
			font-size: 10px;
		}
		.mapsw .btns {
			gap: 4px;
		}
		.mapsw button {
			font-size: 12px;
			padding: 6px 8px;
			flex: 1;
		}
		.mapsw .lines-note {
			font-size: 10.5px;
			line-height: 1.4;
			max-width: none;
		}
		.mapsw-title {
			font-size: 12px;
		}
	}
</style>
