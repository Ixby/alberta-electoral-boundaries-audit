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
	import { browser, version as APP_VERSION } from '$app/environment';
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
	import {
		track,
		zoomBucket,
		firstPaintBand,
		heapBand,
		viewportBucket,
		deviceClass,
		browserFamily
	} from '$lib/analytics';

	// ── Props ────────────────────────────────────────────────────────────────
	// base: SvelteKit base path (pass `base` from $app/paths at the call site so
	//   all asset fetches are base-path-safe under a non-root deployment).
	// initialPoi: a FLAGS id to open focused on (deep link from the report).
	let {
		base = '',
		initialPoi = null,
		onClose
	}: { base?: string; initialPoi?: string | null; onClose?: () => void } = $props();

	// ── Diagnostic HUD (debug-only) ────────────────────────────────────────────
	// A perf HUD ported from the prototype, shown ONLY at ?debug=1. `browser`
	// short-circuits so `location` is never read during SSR / prerender (the deck
	// component is prerendered in node). The HUD is written imperatively via
	// hudEl.innerHTML inside the paint loop — no reactive state on the hot path.
	// APP_VERSION is the git short-hash of the build (kit.version in svelte.config.js),
	// imported above as `version` — a real, verifiable build id, not a hand-bumped tag.
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
	let activeMaps = $state<string[]>(['minority']);
	// 4th map version: a SCAFFOLD for the Nov 2026 Lunty (91-seat) committee. There
	// is no Lunty map yet, so this isn't a tiled map — toggling it overlays the
	// approximate restoration zone the chair named in Addendum Rec 5 (Clearwater +
	// W. Mountain View County). It sits alongside the three real maps, not in them.
	let filters = $state<{ hwy: boolean; water: boolean; pois: boolean; miller: boolean }>({
		hwy: false,
		water: false,
		pois: true,
		miller: false
	});
	let zoomVal = $state(0); // slider value (== viewState.zoom)
	let zoomMin = $state(0);
	let zoomMax = $state(1);
	let resText = $state('—'); // "1 pixel ≈ X" readout body
	// Zoom-slider accent: yellow at overview, flips to blue once the resolution
	// crosses 38 m/pixel (i.e. zoomed into detail). Drives --zoom-accent.
	const ZOOM_ACCENT_COARSE = '#f5c518'; // yellow (overview)
	const ZOOM_ACCENT_DETAIL = '#6fd3fb'; // blue (past 38 m)
	let zoomAccent = $state(ZOOM_ACCENT_COARSE);
	// Visible viewport height (shrinks when the mobile keyboard opens). Used to cap
	// the mobile search-results list so it never hides behind the keyboard.
	let vvH = $state(0);
	let lastTapMs = 0; // last click/tap time, for double-tap/double-click zoom

	// ── Search state (district-name autocomplete) ────────────────────────────────
	let searchQuery = $state('');
	let searchResults = $state<EdRec[]>([]);
	let searchActive = $state(-1); // highlighted dropdown index (keyboard nav)
	let searchOpen = $state(false);

	// Desktop control-panel collapse (toggled from the panel header).
	let panelCollapsed = $state(false);
	// Touch devices get a re-imagined compact UI instead of the desktop panel:
	// a slim corner bar (segmented map toggle + search/layers/info icon popovers)
	// plus a bottom zoom pill. `coarse` is decided once on mount; `mobilePanel`
	// tracks which icon popover is open ('none' = just the bar).
	let coarse = $state(false);
	let mobilePanel = $state<'none' | 'search' | 'layers' | 'info'>('none');

	function toggleMobilePanel(p: 'search' | 'layers' | 'info'): void {
		mobilePanel = mobilePanel === p ? 'none' : p;
		// The community/district target lives with the search: leaving the search
		// popover (closing it or switching panels) drops the target marker.
		if (mobilePanel !== 'search') clearSelection();
	}
	// Focus a node as soon as it mounts (brings up the keyboard for mobile search).
	function focusOnMount(node: HTMLElement) {
		node.focus();
	}

	// DOM refs
	let mapEl: HTMLDivElement;
	let canvasEl: HTMLCanvasElement;
	let tipEl: HTMLDivElement;
	let searchInputEl: HTMLInputElement;

	// Bridges from the onMount closure to template event handlers (assigned in onMount).
	let zoomSetter: (z: number) => void = () => {};
	let dragSetter: (v: boolean) => void = () => {};
	let mapToggler: (mk: string) => void = () => {};
	let filterSetter: (which: 'hwy' | 'water' | 'pois' | 'miller', val: boolean) => void = () => {};
	let edSelector: (rec: EdRec) => void = () => {};
	let clearSelection: () => void = () => {};
	// Miller restoration-zone polygons (loaded lazily when the Miller layer toggle
	// is first enabled); non-reactive.
	let luntyBounds: { zones: { name: string; note?: string; rings: number[][][] }[] } | null = null;

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
	function clearSearch() {
		searchQuery = '';
		searchResults = [];
		searchActive = -1;
		searchOpen = false;
		clearSelection(); // also drop the district ring / community marker + tip
		searchInputEl?.focus();
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

	// Expose the visible viewport height as a CSS var so the mobile search results
	// can stay above the on-screen keyboard (which shrinks visualViewport).
	$effect(() => {
		if (vvH > 0) document.documentElement.style.setProperty('--vvh', vvH + 'px');
	});

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
			// VA id under the cursor. A poll split across quadtree tiles shares one id,
			// so highlighting by id lights the whole poll, not just the hovered tile.
			let hoveredVaId: number | null = null;
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
			// The exact perf payload transmitted at first paint. The HUD renders THIS
			// (not a live recompute) so its "→ analytics" line matches what was sent,
			// instead of drifting as bundles lazy-load and the user zooms.
			let perfSent: Record<string, string | number> | null = null;

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
				const w = tipEl.offsetWidth;
				const h = tipEl.offsetHeight;
				const vw = window.innerWidth;
				const vh = window.innerHeight;
				// Mobile: anchor the tip to a fixed edge rather than the tap point —
				// a finger-following tip covers exactly what you're inspecting.
				if (coarse) {
					if (vw > vh) {
						// Landscape: short on height, controls sit top-right → anchor to
						// the left edge, vertically centred (the free zone).
						tipEl.style.right = 'auto';
						tipEl.style.bottom = 'auto';
						tipEl.style.left = '8px';
						tipEl.style.top = Math.max(8, Math.round((vh - h) / 2)) + 'px';
					} else {
						// Portrait: anchor bottom-centre.
						tipEl.style.top = 'auto';
						tipEl.style.left = '8px';
						tipEl.style.right = '8px';
						tipEl.style.bottom = '10px';
					}
					return;
				}
				const m = 8; // min gap from each viewport edge
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
				lastPolyCount = feats.length; // visible feature count (HUD + perf snapshot)
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
				layers.push(buildVaLayer(deckClasses, feats, vaProps, hoveredVaId));
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
				// Lunty scaffold: the chair's Rec-5 restoration zone (approximate),
				// in dark grey, shown only while the Lunty toggle is on — plus a single
				// explanatory point at the zone's centroid (hover to read what it is).
				if (filters.miller && luntyBounds) {
					const TERRA = [224, 142, 96];
					for (const z of luntyBounds.zones) {
						layers.push(
							new PolygonLayer({
								id: 'lunty-' + z.name,
								data: z.rings,
								getPolygon: (r: number[][]) => r as any,
								filled: false,
								stroked: true,
								getLineColor: [...TERRA, 255],
								getLineWidth: 2,
								lineWidthUnits: 'pixels',
								lineWidthMinPixels: 2,
								parameters: { depthTest: false },
								coordinateSystem: CART
							})
						);
						// Centroid of the largest ring → the explanatory point.
						const ring = z.rings.reduce((a, b) => (b.length > a.length ? b : a), z.rings[0]);
						let sx = 0;
						let sy = 0;
						for (const p of ring) {
							sx += p[0];
							sy += p[1];
						}
						layers.push(
							new ScatterplotLayer({
								id: 'lunty-point',
								// The pin is an annotation, so the annotations (POIs) toggle hides
								// it too. The Miller zone outline stays under the Miller toggle alone.
								visible: filters.pois,
								data: [
									{
										x: sx / ring.length,
										y: sy / ring.length,
										title: 'Miller — a restored rural seat',
										body: 'This area is on the map because of Justice Dallas Miller, the commission’s chair. In an addendum to the final report, he wrote that if the Legislature would not accept cutting two rural ridings, it should instead add two seats — going from 89 to 91 — and restore them. He pointed to this spot, around Clearwater and western Mountain View counties west of Red Deer, as where one of those rural seats should go. It’s sketched from county lines as a placeholder, not an official boundary, until the next commission redraws the map.'
									}
								],
								getPosition: (d: any) => [d.x, d.y, 0],
								getRadius: 7,
								radiusUnits: 'pixels',
								radiusMinPixels: 5,
								filled: true,
								stroked: true,
								getFillColor: [210, 173, 108, 255], // match the other annotation pins
								getLineColor: [88, 72, 40, 255],
								getLineWidth: 1.4,
								lineWidthUnits: 'pixels',
								// Pickable on desktop (hover tip). On touch it is NON-pickable so it
								// can't intercept the two-finger pinch-zoom gesture; the explanation
								// is shown in the mobile info (ⓘ) popover instead.
								pickable: true,
								parameters: { depthTest: false },
								coordinateSystem: CART
							})
						);
					}
				}
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

				// Community / municipality hit (sel.ed set, with its own centroid):
				// a DISTINCT magenta marker — a center point plus a ring scaled to the
				// community's extent — to set it apart from the gold ED glow and pinpoint
				// the place within the district it sits in.
				if (sel.ed && sel.ccx != null && sel.ccy != null) {
					const cc: [number, number, number] = [sel.ccx, sel.ccy, 0];
					const PINK = [255, 64, 150];
					return [
						new ScatterplotLayer({
							id: 'comm-ring',
							data: [sel],
							getPosition: () => cc,
							getRadius: sel.crad ?? 800,
							radiusUnits: 'meters',
							radiusMinPixels: 16,
							filled: true,
							stroked: true,
							getFillColor: [...PINK, 26],
							getLineColor: [...PINK, 240],
							getLineWidth: 3,
							lineWidthUnits: 'pixels',
							lineWidthMinPixels: 2,
							parameters: { depthTest: false },
							coordinateSystem: CART
						}),
						new ScatterplotLayer({
							id: 'comm-center',
							data: [sel],
							getPosition: () => cc,
							getRadius: 5,
							radiusUnits: 'pixels',
							radiusMinPixels: 4,
							filled: true,
							stroked: true,
							getFillColor: [...PINK, 255],
							getLineColor: [255, 255, 255, 235],
							getLineWidth: 1.5,
							lineWidthUnits: 'pixels',
							parameters: { depthTest: false },
							coordinateSystem: CART
						})
					];
				}

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

			// ── Shared perf telemetry ──────────────────────────────────────────────
			// The single source of truth for both the analytics `perf` event and the
			// debug HUD's "→ analytics" line — so the HUD shows exactly what is sent.
			// Flat scalars only (the collector drops non-scalar props), coarsened for
			// privacy: `fp` is a load-time band, `heap_mb` a 50 MB step. The high-res
			// paint breakdown (lib/assets/deck/gpu) is intentionally NOT included here —
			// it stays HUD-only because a 4-way timing vector is fingerprint-adjacent.
			function perfPayload(L: number): Record<string, string | number> {
				const mem = (performance as unknown as { memory?: { usedJSHeapSize: number } }).memory;
				const p: Record<string, string | number> = {
					fp: firstPaintBand(firstPaintMs),
					loaded_mb: Math.round(archiveBytes / 1e5) / 10,
					polys: lastPolyCount,
					level: L,
					maps: activeMaps.join('+') || 'fills',
					data_ver: (M && M.version) || '?',
					app_ver: APP_VERSION
				};
				if (mem) p.heap_mb = heapBand(mem.usedJSHeapSize / 1e6);
				return p;
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
				// The exact payload the analytics `perf` event carried, captured once at
				// first paint (not recomputed live) so the HUD mirrors what was sent.
				const sentLine = perfSent
					? Object.keys(perfSent)
							.map((k) => `${k} <b>${perfSent![k]}</b>`)
							.join(' · ')
					: '…';
				hudEl.innerHTML =
					`<b>deck.gl · EPSG:3401</b> &nbsp; <b>${activeMaps.join('+') || 'fills only'}</b> &nbsp; ` +
					`<span style="color:#8aa0c2">data <b>${M.version || '?'}</b> · app <b>${APP_VERSION}</b></span><br>` +
					`level <b>${L}</b>/${M.maxZoom} &nbsp; polys <b>${lastPolyCount}</b> &nbsp; ` +
					`loaded <b>${bundlesLoaded}/${bundleTotal}</b> · <b>${(archiveBytes / 1e6).toFixed(1)}MB</b>${heap}<br>` +
					`first paint <b>${firstPaintMs ? firstPaintMs + 'ms' : '…'}</b>${br} &nbsp; last paint <b>${lastPaintMs}ms</b><br>` +
					`<span style="color:#9fb380">→ analytics perf:</span> ${sentLine}<br><span style="color:#9fb380">→ analytics pageview:</span> device <b>${deviceClass()}</b> · viewport <b>${viewportBucket(window.innerWidth)}</b> · browser <b>${browserFamily(navigator.userAgent)}</b>` +
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
				// Continuous metres/pixel (2^-zoom in EPSG:3401 metres) drives the slider
				// accent: yellow until it passes 38 m, blue once zoomed in past that.
				const mpp = 2 ** -(lastVS.zoom as number);
				zoomAccent = mpp < 38 ? ZOOM_ACCENT_DETAIL : ZOOM_ACCENT_COARSE;
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
			filterSetter = (which: 'hwy' | 'water' | 'pois' | 'miller', val: boolean) => {
				filters[which] = val;
				if (which === 'hwy' && val) loadHwyData();
				if (which === 'water' && val) loadWaterData();
				if (which === 'miller' && val && !luntyBounds) {
					fetchJSON('lunty_bounds.json')
						.then((d) => {
							luntyBounds = d as any;
							schedulePaint();
						})
						.catch(() => {});
				}
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
			// Clear the current selection: drop the district ring / community marker
			// and any open tip, and repaint. Bound to the search clear-× button.
			clearSelection = () => {
				selectedEd = null;
				hideTip();
				schedulePaint();
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

			// Touch devices render the compact mobile control UI instead of the
			// desktop panel (decided once here; pointer type rarely changes mid-session).
			coarse = window.matchMedia?.('(pointer: coarse)').matches === true;

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
				controller: { scrollZoom: { smooth: true }, doubleClickZoom: true },
				useDevicePixels: DPR,
				// deck.gl picking callbacks: typed loosely (deck's PickingInfo is runtime-imported).
				onHover: (info: any) => {
					const o = info.object as
						| { id?: number; title?: string; body?: string }
						| undefined;
					// Merged poll highlight: a VA split across tiles shares one id, so track
					// the hovered VA id and light every piece of it (see buildVaLayer), not
					// just the tile under the cursor. Repaint only when the id changes.
					const nextHover =
						info.layer && info.layer.id === 'va' && o && typeof o.id === 'number'
							? (o.id as number)
							: null;
					if (nextHover !== hoveredVaId) {
						hoveredVaId = nextHover;
						schedulePaint();
					}
					if (!o) {
						hideTip();
						return;
					}
					tipEl.style.display = 'block';
					if (info.layer && info.layer.id === 'flags') {
						tipEl.innerHTML =
							`<div class="n">${o.title}</div><div class="flagbody">${o.body}</div>` +
							`<div class="flaglink">Click to zoom in</div>`;
					} else if (info.layer && info.layer.id === 'lunty-point') {
						tipEl.innerHTML = `<div class="n">${o.title}</div><div class="flagbody">${o.body}</div>`;
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
						// Zoom in to fill the view on the pin, then nudge the camera so the
						// pin lands LEFT of the right-side controls (panel on desktop, the
						// compact bar on mobile) instead of being hidden beneath them.
						const tz = 6.3 - Math.log2(M.side / 256);
						const z = Math.min(
							lastVS!.maxZoom as number,
							Math.max(lastVS!.minZoom as number, tz)
						);
						const mpp = 2 ** -z; // metres per pixel at z
						const dxPx = coarse ? 64 : 150; // shift pin left, clearing the controls
						update({
							...lastVS!,
							target: [info.object.x + dxPx * mpp, info.object.y, 0],
							zoom: z
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
				vvH = window.visualViewport?.height ?? window.innerHeight;
				schedulePaint();
			};
			vvH = window.visualViewport?.height ?? window.innerHeight;
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
			// Search index: the primary (first active) map's districts, PLUS every
			// community / municipality keyed to its 2019 electoral district. The 2019
			// map is the fixed cross-reference for orientation — a community entry
			// flies to (and glows) the ED that contains it; the other proposals shift
			// around that anchor. Community entries carry the 2019 ED's centroid/zoom,
			// so the name-agnostic glow highlights that district automatically.
			async function loadEdIndex() {
				const primary = activeMaps.length ? activeMaps[0] : 'minority';
				const recs = await fetchJSON<EdRec[]>('ed_index_' + primary + '.json');
				let communities: EdRec[] = [];
				try {
					communities = await fetchJSON<EdRec[]>('community_index_2019.json');
				} catch {
					communities = []; // search still works on districts alone if absent
				}
				nameIndex = buildNameIndex(recs.concat(communities));
			}

			// View-first load: gate first paint on the bundle covering the initial level.
			let L0 = tileLevelForZoom(initial.zoom as number, M.side, M.minZoom, M.maxZoom);
			const head = M.bundles.find((b) => b.lo <= L0 && L0 <= b.hi) || M.bundles[0];
			lazyTriggered.add(head.file);
			const headBytes = await loadBundle(`${base}/mapdata`, head, archive);
			// Counted for all visitors (not just DEBUG): the perf snapshot reports
			// loaded_mb, and at first paint only the head bundle has arrived.
			archiveBytes += headBytes;
			bundlesLoaded++;
			if (disposed) return;
			update(initial);
			// Capture first paint with an idle main thread, BEFORE any further loading.
			// Runs for every visitor now: the perf snapshot is sent here (one event,
			// first paint), and the debug HUD — when shown — renders the same numbers.
			await new Promise<void>((r) =>
				requestAnimationFrame(() => {
					firstPaintMs = Math.round(performance.now());
					perfSent = perfPayload(L0);
					track('perf', perfSent);
					schedulePaint();
					r();
				})
			);
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

<div class="explorer" style="--zoom-accent: {zoomAccent}">
	<svg class="watermark" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
		<defs>
			<pattern
				id="wm-pat"
				width="240"
				height="120"
				patternUnits="userSpaceOnUse"
				patternTransform="rotate(-45)"
			>
				<text x="0" y="20" class="wm-text">MAP EXPLORER</text>
			</pattern>
		</defs>
		<rect width="100%" height="100%" fill="url(#wm-pat)" />
	</svg>
	<div class="map" bind:this={mapEl}>
		<canvas bind:this={canvasEl}></canvas>
	</div>

	{#if coarse}
		<!-- ── Compact mobile control bar (top-right) ─────────────────────────── -->
		<div class="msw-m">
			<div class="msw-m-head">
			<div class="msw-m-bar">
				<div class="seg" role="group" aria-label="Map version">
					{#each MAPS as mk (mk)}
						<button
							class="seg-btn"
							class:on={activeMaps.includes(mk)}
							style={btnStyle(mk)}
							title="Toggle this map on/off"
							onclick={() => mapToggler(mk)}
						>{mk === '2019' ? "’19" : mk === 'minority' ? 'Min' : 'Maj'}</button>
					{/each}
				</div>
				<button
					class="ic"
					class:on={mobilePanel === 'search'}
					aria-label="Search districts"
					aria-pressed={mobilePanel === 'search'}
					onclick={() => toggleMobilePanel('search')}
				>
					<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" /><line x1="16.5" y1="16.5" x2="21" y2="21" /></svg>
				</button>
				<button
					class="ic"
					class:on={mobilePanel === 'layers'}
					aria-label="Map layers"
					aria-pressed={mobilePanel === 'layers'}
					onclick={() => toggleMobilePanel('layers')}
				>
					<svg viewBox="0 0 24 24" aria-hidden="true"><polygon points="12 3 22 8.5 12 14 2 8.5" /><polyline points="2 15 12 20.5 22 15" /></svg>
				</button>
				<button
					class="ic"
					class:on={mobilePanel === 'info'}
					aria-label="About the boundary lines"
					aria-pressed={mobilePanel === 'info'}
					onclick={() => toggleMobilePanel('info')}
				>
					<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9.2" /><line x1="12" y1="11" x2="12" y2="16.5" /><circle cx="12" cy="7.6" r="0.4" fill="currentColor" stroke="none" /></svg>
				</button>
				{#if onClose}
					<span class="ic-div" aria-hidden="true"></span>
					<button class="ic ic-close" aria-label="Close map" onclick={() => onClose?.()}>
						<svg viewBox="0 0 24 24" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18" /><line x1="18" y1="6" x2="6" y2="18" /></svg>
					</button>
				{/if}
			</div>

			<!-- Zoom pill, upper-right (under the bar) — always visible -->
			<div class="zoom-m">
				<input
					class="zoom"
					type="range"
					min={zoomMin}
					max={zoomMax}
					step="0.01"
					aria-label="Zoom"
					bind:value={zoomVal}
					oninput={() => {
						dragSetter(true);
						zoomSetter(zoomVal);
					}}
					onchange={() => dragSetter(false)}
				/>
				<span class="res-m"><b>{resText}</b></span>
			</div>
			</div>

			{#if mobilePanel === 'search'}
				<div class="msw-m-pop">
					<div class="search">
					<input
						class="search-input"
						type="text"
						placeholder="Search a district…"
						autocomplete="off"
						bind:this={searchInputEl}
						bind:value={searchQuery}
						use:focusOnMount
						oninput={runSearch}
						onkeydown={onSearchKeydown}
						onfocus={() => {
							if (searchResults.length) searchOpen = true;
						}}
					/>
					{#if searchQuery}
						<button
							class="search-clear"
							type="button"
							aria-label="Clear search"
							onmousedown={(e) => {
								e.preventDefault();
								clearSearch();
							}}>×</button>
					{/if}
					</div>
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
										// keep the search popover open while the target marker is up
									}}
									onmouseenter={() => (searchActive = i)}
								>
									<span class="sr-name">{r.name}</span>{#if r.ed}<span class="sr-ed">in {r.ed}</span>{/if}
								</li>
							{/each}
						</ul>
					{/if}
				</div>
			{:else if mobilePanel === 'layers'}
				<div class="msw-m-pop">
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
					<label>
						<input
							type="checkbox"
							checked={filters.miller}
							onchange={(e) => filterSetter('miller', e.currentTarget.checked)}
						/> Miller's seat
					</label>
				</div>
			{:else if mobilePanel === 'info'}
				<div class="msw-m-pop note">
					<b>Reading the lines</b><br />
					Every odd shape or split line is a <b>deliberate choice by the committee</b> — not a
					data error. Lines follow the edges of polling areas; where two maps agree they sit on the
					same line, where they split apart the proposals genuinely disagree.
				</div>
			{/if}
		</div>
	{:else}
	<div class="mapsw" class:collapsed={panelCollapsed}>
		<div class="mapsw-head">
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
			{#if onClose}
				<button
					type="button"
					class="mapsw-close"
					aria-label="Close map"
					onclick={() => onClose?.()}>×</button>
			{/if}
		</div>

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
			{#if searchQuery}
				<button
					class="search-clear"
					type="button"
					aria-label="Clear search"
					onmousedown={(e) => {
						e.preventDefault();
						clearSearch();
					}}>×</button>
			{/if}
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
							<span class="sr-name">{r.name}</span>{#if r.ed}<span class="sr-ed">in {r.ed}</span>{/if}
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
			<label>
				<input
					type="checkbox"
					checked={filters.miller}
					onchange={(e) => filterSetter('miller', e.currentTarget.checked)}
				/> Miller's proposed seat
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
	{/if}

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
		   through around the province silhouette). The diagonal "MAP EXPLORER"
		   watermark is a separate inline-SVG layer (.watermark) so it can use the
		   self-hosted Cinzel webfont — a CSS background data-URI can't. */
		background-color: #1a1511;
		font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
	}
	/* Tiled diagonal expedition-style watermark, behind the (transparent-cleared)
	   map canvas. Shows in the margin around the province silhouette. */
	.watermark {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		z-index: 0;
		pointer-events: none;
	}
	.watermark .wm-text {
		font-family: 'Cinzel', 'Trajan Pro', Georgia, serif;
		font-weight: 700;
		font-size: 15px;
		letter-spacing: 3px;
		fill: #f0e6d6;
		fill-opacity: 0.08;
	}
	.map {
		position: absolute;
		inset: 0;
		/* Let deck.gl own all touch gestures — stop the browser from claiming the
		   first finger as a scroll, which breaks pinch when fingers land in sequence. */
		touch-action: none;
	}
	.map canvas {
		width: 100%;
		height: 100%;
		display: block;
		touch-action: none;
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
	/* Panel header row: collapse toggle (fills) + a close button (folds the map's
	   close into the panel so the overlay's floating corner × no longer overlaps
	   these controls on desktop). */
	.mapsw-head {
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.mapsw-head .mapsw-toggle {
		flex: 1;
		width: auto;
	}
	.mapsw-close {
		flex: none;
		display: grid;
		place-items: center;
		width: 22px;
		height: 22px;
		padding: 0;
		border: none;
		background: none;
		border-radius: 5px;
		color: #b89a8a;
		font-size: 18px;
		line-height: 1;
		cursor: pointer;
	}
	.mapsw-close:hover {
		color: #e7d6c4;
		background: rgba(255, 255, 255, 0.07);
	}
	/* Clear-text button inside the search field (both desktop + mobile). */
	.search {
		position: relative;
	}
	.search-clear {
		position: absolute;
		top: 50%;
		right: 6px;
		transform: translateY(-50%);
		width: 22px;
		height: 22px;
		display: grid;
		place-items: center;
		padding: 0;
		border: none;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.06);
		color: #9fb4d4;
		font-size: 16px;
		line-height: 1;
		cursor: pointer;
	}
	.search-clear:hover {
		background: rgba(255, 255, 255, 0.15);
		color: #e6eefb;
	}
	.mapsw-body {
		display: flex;
		flex-direction: column;
		gap: 11px;
	}
	/* Section labels (Map version / Geographic filters): small warm uppercase. */
	.mapsw .hdr,
	.mapsw .fhdr {
		font-size: 9.5px;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #9a8c72;
		padding: 0 1px;
		margin-bottom: 1px;
	}
	.mapsw .hdr span {
		display: none;
	}
	.mapsw .search {
		position: relative;
	}
	.mapsw .search-input,
	.msw-m-pop .search-input {
		width: 100%;
		box-sizing: border-box;
		background: #11182a;
		border: 1px solid #2a3550;
		border-radius: 7px;
		color: #e6eefb;
		font: 400 13px -apple-system, 'Segoe UI', sans-serif;
		padding: 7px 32px 7px 9px;
		outline: none;
	}
	.mapsw .search-input:focus,
	.msw-m-pop .search-input:focus {
		border-color: #6fd3fb;
	}
	.mapsw .search-input::placeholder,
	.msw-m-pop .search-input::placeholder {
		color: #6b7d99;
	}
	/* Mobile popover: results flow in-card below the input (not absolute), capped
	   to the visible viewport (var --vvh shrinks when the keyboard opens) so the
	   list never hides behind the on-screen keyboard. */
	.msw-m-pop .search-results {
		list-style: none;
		margin: 2px 0 0;
		padding: 0;
		max-height: min(44vh, calc(var(--vvh, 100vh) - 120px));
		overflow-y: auto;
	}
	.msw-m-pop .search-results li {
		padding: 9px 8px;
		border-radius: 5px;
		font-size: 13.5px;
		color: #cfe0f5;
		cursor: pointer;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.msw-m-pop .search-results li.sr-active {
		background: #1f6feb;
		color: #fff;
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
	/* Result rows: name on top, the resolving 2019 district as a muted subtitle. */
	.sr-name {
		display: block;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.sr-ed {
		display: block;
		font-size: 11px;
		color: #8090a8;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		margin-top: 1px;
	}
	.sr-active .sr-ed {
		color: #cdd9ee;
	}
	.msw-m-pop .sr-ed {
		font-size: 12px;
	}
	/* Balanced 2×2 grid: Minority / Majority / 2019 / Lunty, equal cells. */
	.mapsw .btns {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 5px;
	}
	.mapsw button {
		border: 1px solid transparent;
		background: none;
		color: #9fb4d4;
		font: 600 12.5px -apple-system, 'Segoe UI', sans-serif;
		padding: 7px 8px;
		border-radius: 7px;
		cursor: pointer;
		text-align: center;
	}
	.mapsw .zoom {
		width: 100%;
		margin: 6px 0 2px;
		accent-color: var(--zoom-accent, #6fd3fb);
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
		/* Anchored to the bottom-left so the debug overlay sits below the map UI
		   (controls live top-right / top-left); it grows upward as rows are added. */
		bottom: 10px;
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

	/* ── Compact mobile control UI (rendered only on coarse-pointer devices) ──── */
	.msw-m {
		position: absolute;
		/* The close (×) lives in the bar itself (the overlay's corner × is hidden
		   on touch), so the bar reclaims the top-right corner. */
		top: 8px;
		right: 8px;
		z-index: 6;
		display: flex;
		flex-direction: column;
		align-items: flex-end;
		gap: 6px;
		max-width: calc(100% - 16px);
	}
	.msw-m-bar {
		display: flex;
		align-items: center;
		gap: 5px;
		background: rgba(18, 16, 13, 0.9);
		border: 1px solid #3a342a;
		border-radius: 11px;
		padding: 4px;
		-webkit-backdrop-filter: blur(7px);
		backdrop-filter: blur(7px);
		box-shadow: 0 3px 14px rgba(0, 0, 0, 0.4);
	}
	.msw-m .seg {
		display: flex;
		gap: 2px;
	}
	.msw-m .seg-btn {
		border: 1px solid transparent;
		font: 600 12px -apple-system, 'Segoe UI', sans-serif;
		padding: 6px 9px;
		border-radius: 7px;
		cursor: pointer;
		min-width: 38px;
		text-align: center;
	}
	.msw-m .ic {
		display: grid;
		place-items: center;
		width: 34px;
		height: 34px;
		padding: 0;
		border: 1px solid #3a342a;
		background: #1d1812;
		border-radius: 8px;
		color: #cbb89c;
		cursor: pointer;
	}
	.msw-m .ic.on {
		background: #6fd3fb;
		border-color: #6fd3fb;
		color: #0c0f1a;
	}
	.msw-m .ic-div {
		width: 1px;
		align-self: stretch;
		margin: 3px 1px;
		background: #3a342a;
	}
	.msw-m .ic-close {
		color: #d8a99a;
		border-color: #4a3a34;
		background: #241813;
	}
	.msw-m .ic svg {
		width: 18px;
		height: 18px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.msw-m-pop {
		width: min(80vw, 290px);
		box-sizing: border-box;
		background: rgba(18, 16, 13, 0.95);
		border: 1px solid #3a342a;
		border-radius: 11px;
		padding: 10px;
		-webkit-backdrop-filter: blur(7px);
		backdrop-filter: blur(7px);
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55);
		display: flex;
		flex-direction: column;
		gap: 8px;
	}
	.msw-m-pop label {
		display: flex;
		align-items: center;
		gap: 10px;
		font-size: 14px;
		color: #cfe0f5;
		cursor: pointer;
	}
	.msw-m-pop label input {
		width: 18px;
		height: 18px;
		accent-color: #6fd3fb;
		cursor: pointer;
	}
	.msw-m-pop.note {
		font-size: 12.5px;
		line-height: 1.55;
		color: #9fb4d4;
		display: block;
	}
	.msw-m-pop.note b {
		color: #cfe0f5;
	}
	/* Bar + zoom grouped; the vertical zoom sits right-aligned under the bar. */
	/* Flatten the bar+zoom group into the .msw-m flex column (display:contents) so
	   an open popover (e.g. the layers card) can nest BETWEEN the bar and the zoom
	   via flex order, rather than below the zoom. */
	.msw-m-head {
		display: contents;
	}
	.msw-m .msw-m-bar {
		order: 0;
	}
	.msw-m .msw-m-pop {
		order: 1;
	}
	.msw-m .zoom-m {
		order: 2;
	}
	/* Vertical zoom capsule — tall slider + scale readout, under the bar. */
	.zoom-m {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 7px;
		box-sizing: border-box;
		padding: 12px 7px 9px;
		background: rgba(18, 16, 13, 0.9);
		border: 1px solid #3a342a;
		border-radius: 999px;
		-webkit-backdrop-filter: blur(7px);
		backdrop-filter: blur(7px);
		box-shadow: 0 3px 14px rgba(0, 0, 0, 0.4);
	}
	.zoom-m .zoom {
		/* Render the range input vertically. direction:rtl puts the max (zoomed
		   in) at the top, matching the conventional map zoom control. */
		writing-mode: vertical-lr;
		direction: rtl;
		width: 22px;
		height: 130px;
		margin: 0;
		accent-color: var(--zoom-accent, #6fd3fb);
		cursor: pointer;
	}
	.zoom-m .res-m {
		font-size: 10px;
		color: #9fb4d4;
		white-space: nowrap;
	}
	.zoom-m .res-m b {
		color: #6fd3fb;
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
	}
	/* Portrait phones: the tip becomes a full-width bottom sheet (placeTip pins it
	   left/right/bottom), so it reads as part of the UI rather than a floating card. */
	@media (pointer: coarse) and (orientation: portrait) {
		.tip {
			max-width: none;
			border-radius: 12px;
			box-shadow: 0 -3px 18px rgba(0, 0, 0, 0.45);
		}
	}
</style>
