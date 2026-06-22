// Layer construction for the deck.gl map explorer.
//
// CRITICAL design rule: this module has NO top-level `@deck.gl/*` import — not
// even `import type`. Keeping it deck.gl-free makes it node-importable so the
// pure grouping logic (`groupsFor`) can be unit-tested without a browser/WebGL
// env, and so a grep for `@deck.gl` over this file finds nothing. The layer
// builders receive the deck.gl layer classes (PathLayer, PolygonLayer, …),
// COORDINATE_SYSTEM, and the PathStyleExtension class as ARGUMENTS — dependency
// injection. The Svelte component imports deck.gl dynamically (browser-only) and
// passes the classes in.
//
// Ported from the validated prototype (viewer/static/spike/index.html). The only
// piece worth unit-testing is `groupsFor`: the agreement logic (which subset of
// active maps each boundary segment is shared by) that broke and was fixed this
// session. The layer builders are faithful ports of the prototype's emit code.
//
// NOTE: the freeze fix this session made toggling INSTANT — no crossfade. So the
// old prevGroups / easeInOut / DURATION / animLoop machinery is intentionally not
// ported; `buildEdLayers` emits the current groups once.

// ── Structural DI types (no deck.gl import) ───────────────────────────────────
//
// Layer classes are constructors taking a single props object and returning a
// layer instance; we type them structurally so this file never imports deck.gl.

/** A deck.gl layer class, used purely as `new LayerClass(props)`. */
export type LayerClass = new (props: Record<string, unknown>) => unknown;
/** A deck.gl layer instance (opaque to this module). */
export type LayerInstance = unknown;
/** The PathStyleExtension class, used as `new PathStyleExtension({dash:true})`. */
export type ExtensionClass = new (props: Record<string, unknown>) => unknown;
/** deck.gl's COORDINATE_SYSTEM enum object (we only read `.CARTESIAN`). */
export type CoordinateSystem = Record<string, unknown>;

// ── Map identities + colours ──────────────────────────────────────────────────

/** Canonical map order. `Edge.m` is one-hot/multi-hot over this index. */
export const MAPS = ['minority', 'majority', '2019'] as const;
export type MapKey = (typeof MAPS)[number] | string;

/** Index of a map key within MAPS (the bit position in `Edge.m`). */
const mapIdx = (mk: string): number => MAPS.indexOf(mk as (typeof MAPS)[number]);

/** Per-map canonical boundary colours (from the website constants): deep purple
 *  / bright teal / Elections Alberta yellow. Saturated; width carries visibility. */
export const MAP_RGB: Record<string, [number, number, number]> = {
	minority: [124, 58, 196],
	majority: [58, 208, 190],
	'2019': [245, 197, 24]
};

/** Overlay dash patterns per agreement stroke: 1st map solid, 2nd dashed, 3rd
 *  dotted — so every map's colour shows where the maps agree. */
export const OVERLAY: (number[] | null)[] = [null, [11, 8], [2, 7]];

/** Blend a set of map colours into one RGB (used for the perimeter/outline). */
export function blend(mks: string[]): [number, number, number] {
	let r = 0,
		g = 0,
		b = 0;
	for (const mk of mks) {
		const c = MAP_RGB[mk];
		r += c[0];
		g += c[1];
		b += c[2];
	}
	const n = mks.length;
	return [(r / n) | 0, (g / n) | 0, (b / n) | 0];
}

// ── Edge data + the pure grouping logic ───────────────────────────────────────

/** A shared VA-edge from ed_edges.json: geometry `g` (a path of XY points) and
 *  `m` = [minority, majority, 2019] agreement flags (one-hot or multi-hot). */
export interface Edge {
	g: number[][];
	m: number[];
}

/** A group of boundary segments shared by exactly the same subset of active
 *  maps. `mks` is that subset (in the order maps were passed), `key` is
 *  `mks.join('+')`, and `list` is the edges in the group. */
export interface Group {
	mks: string[];
	key: string;
	list: Edge[];
}

/**
 * Partition `edges` into groups by which subset of `activeMaps` shares each one.
 *
 * For each edge, keep the active maps whose bit is set in `edge.m` (indexed via
 * MAPS order, NOT the order of activeMaps). Edges with no active map are dropped.
 * The surviving maps form the group key (`mks.join('+')`), so e.g. an all-three
 * edge collapses to `minority+majority` when 2019 is inactive.
 *
 * Pure: no deck.gl, no globals. The caller passes maps in MAPS order so keys are
 * canonical. Ported from `groupsFor` in the prototype (index.html ~250).
 */
export function groupsFor(activeMaps: string[], edges: Edge[]): Group[] {
	const g: Record<string, Group> = {};
	for (const e of edges) {
		const mks = activeMaps.filter((mk) => e.m[mapIdx(mk)]);
		if (!mks.length) continue;
		const key = mks.join('+');
		(g[key] || (g[key] = { mks, key, list: [] })).list.push(e);
	}
	return Object.values(g);
}

// ── Layer builders (deck.gl classes injected) ─────────────────────────────────

/** One PathLayer for a single agreement stroke. Solid when `dash` is null;
 *  dashed/dotted (via the injected PathStyleExtension) when a pattern is given.
 *  Ported from `edPath` in the prototype. */
function edPath(
	PathLayer: LayerClass,
	COORDINATE_SYSTEM: CoordinateSystem,
	dashExt: unknown | null,
	id: string,
	list: Edge[],
	rgb: [number, number, number],
	alpha: number,
	width: number,
	dash: number[] | null
): LayerInstance {
	const a = Math.round(alpha);
	const props: Record<string, unknown> = {
		id,
		data: list,
		getPath: (d: Edge) => d.g,
		getColor: [rgb[0], rgb[1], rgb[2], a],
		widthUnits: 'pixels',
		getWidth: width,
		widthMinPixels: 0.4,
		capRounded: true,
		jointRounded: true,
		updateTriggers: { getColor: `${rgb}:${a}`, getWidth: width },
		coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
	};
	if (dash && dashExt) {
		props.extensions = [dashExt];
		props.getDashArray = dash;
		props.dashJustified = true;
	}
	return new PathLayer(props);
}

/**
 * Build the ED boundary layers for the current active maps. Computes the groups
 * once (no crossfade — toggling is instant) and emits, per group, one overlaid
 * PathLayer per map in that group: each in its own MAP_RGB colour with pattern
 * OVERLAY[i] (1st solid, 2nd dashed, 3rd dotted). Agreement strokes are NOT
 * blended — the blend is only for the perimeter outline elsewhere.
 *
 * Ported from `emitGroups` (index.html ~277). A single PathStyleExtension is
 * instantiated from the injected class.
 */
export function buildEdLayers(
	deps: { PathLayer: LayerClass; PathStyleExtension: ExtensionClass; COORDINATE_SYSTEM: CoordinateSystem },
	activeMaps: string[],
	edEdges: Edge[],
	alpha: number,
	width: number
): LayerInstance[] {
	const { PathLayer, PathStyleExtension, COORDINATE_SYSTEM } = deps;
	if (!edEdges.length) return [];
	const dashExt = PathStyleExtension ? new PathStyleExtension({ dash: true }) : null;
	const groups = groupsFor(activeMaps, edEdges);
	const layers: LayerInstance[] = [];
	for (const grp of groups) {
		const mks = grp.mks;
		for (let i = 0; i < mks.length; i++) {
			layers.push(
				edPath(
					PathLayer,
					COORDINATE_SYSTEM,
					dashExt,
					'ed-' + grp.key + i,
					grp.list,
					MAP_RGB[mks[i]],
					alpha,
					width,
					OVERLAY[i] || null
				)
			);
		}
	}
	return layers;
}

/** VA fill polygons. `vaProps` is indexed by VA id; a VA with no props falls
 *  back to the paper-grey fill. Ported from the `va` PolygonLayer (~335). */
export function buildVaLayer(
	deps: { PolygonLayer: LayerClass; COORDINATE_SYSTEM: CoordinateSystem },
	feats: { id: number; coords: Float32Array }[],
	vaProps: { fill?: [number, number, number] }[]
): LayerInstance {
	const { PolygonLayer, COORDINATE_SYSTEM } = deps;
	return new PolygonLayer({
		id: 'va',
		data: feats,
		pickable: true,
		getPolygon: (d: { coords: Float32Array }) => d.coords,
		positionFormat: 'XY',
		getFillColor: (d: { id: number }) => (vaProps[d.id] ? vaProps[d.id].fill : [232, 230, 224]),
		stroked: false,
		filled: true,
		coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
	});
}

/** Faint hairline around every VA so abutting same-colour polls stay
 *  distinguishable when zoomed in (shown from level 3). Returns [] otherwise.
 *  Ported from the `va-outline` PathLayer (~342). */
export function buildHairlines(
	deps: { PathLayer: LayerClass; COORDINATE_SYSTEM: CoordinateSystem },
	vaLines: number[][][],
	level: number
): LayerInstance[] {
	const { PathLayer, COORDINATE_SYSTEM } = deps;
	if (!(vaLines.length && level >= 3)) return [];
	return [
		new PathLayer({
			id: 'va-outline',
			data: vaLines,
			getPath: (d: number[][]) => d,
			getColor: [205, 210, 222, level <= 3 ? 45 : level <= 4 ? 80 : 120],
			widthUnits: 'pixels',
			getWidth: 0.6,
			widthMinPixels: 0.3,
			updateTriggers: { getColor: level },
			coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
		})
	];
}

/** A path feature with a flat/nested coordinate path and a `major` flag. */
interface PathFeature {
	path: number[][];
	major?: boolean;
}

/**
 * Build the basemap path layers — primary highways, secondary highways, and
 * trunk roads — gated by the `filters.hwy` toggle and the zoom `level`
 * (secondary appears from level 3; minor primaries from level 5).
 * Ported from the hwy / secondary / trunk PathLayers (index.html ~356–379).
 *
 * Deviation from the prototype: there, primary highways were gated on the `?hwy=1`
 * URL param while secondary/trunk were gated on the `layerFilters.hwy` toggle.
 * This unifies all three road layers under the single `filters.hwy` contract.
 *
 * NOTE: water in the prototype is a filled PolygonLayer, not a PathLayer; it is
 * handled separately by the component and is not part of this PathLayer basemap,
 * so `data.water` / `filters.water` are accepted but unused here.
 */
export function buildBasemap(
	deps: { PathLayer: LayerClass; COORDINATE_SYSTEM: CoordinateSystem },
	data: {
		water?: PathFeature[] | null;
		highways?: PathFeature[] | null;
		secondary?: PathFeature[] | null;
		trunk?: PathFeature[] | null;
	},
	filters: { hwy?: boolean; water?: boolean },
	level: number
): LayerInstance[] {
	const { PathLayer, COORDINATE_SYSTEM } = deps;
	const layers: LayerInstance[] = [];

	if (data.highways && data.highways.length && filters.hwy) {
		layers.push(
			new PathLayer({
				id: 'hwy',
				data: data.highways.filter((d) => d.major || level >= 5),
				getPath: (d: PathFeature) => d.path,
				getColor: (d: PathFeature) => (d.major ? [198, 52, 40, 245] : [208, 112, 98, 195]),
				widthUnits: 'pixels',
				getWidth: (d: PathFeature) => (d.major ? 1.4 : 0.8),
				widthMinPixels: 0.5,
				capRounded: true,
				jointRounded: true,
				coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
			})
		);
	}

	if (data.secondary && data.secondary.length && filters.hwy && level >= 3) {
		layers.push(
			new PathLayer({
				id: 'secondary',
				data: data.secondary,
				getPath: (d: PathFeature) => d.path,
				getColor: [96, 108, 158, 200], // navy at ~50% saturation
				widthUnits: 'pixels',
				getWidth: level <= 4 ? 0.6 : 0.8,
				widthMinPixels: 0.3,
				capRounded: true,
				jointRounded: true,
				updateTriggers: { getWidth: level },
				coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
			})
		);
	}

	if (data.trunk && data.trunk.length && filters.hwy) {
		layers.push(
			new PathLayer({
				id: 'trunk',
				data: data.trunk,
				getPath: (d: PathFeature) => d.path,
				getColor: [22, 32, 90, 200], // navy
				widthUnits: 'pixels',
				getWidth: level <= 2 ? 1.0 : 1.2,
				widthMinPixels: 0.5,
				capRounded: true,
				jointRounded: true,
				updateTriggers: { getWidth: level },
				coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
			})
		);
	}

	return layers;
}

/** Annotation pins (the "looks wrong, is faithful" markers). Returns [] when
 *  disabled or empty. Ported from the `flags` ScatterplotLayer (~382). */
export function buildPois(
	deps: { ScatterplotLayer: LayerClass; COORDINATE_SYSTEM: CoordinateSystem },
	flags: { id: string; x: number; y: number }[],
	enabled: boolean
): LayerInstance[] {
	const { ScatterplotLayer, COORDINATE_SYSTEM } = deps;
	if (!(flags.length && enabled)) return [];
	return [
		new ScatterplotLayer({
			id: 'flags',
			data: flags,
			pickable: true,
			getPosition: (d: { x: number; y: number }) => [d.x, d.y, 0],
			getRadius: 7,
			radiusUnits: 'pixels',
			radiusMinPixels: 5,
			getFillColor: [210, 173, 108, 255],
			stroked: true,
			getLineColor: [88, 72, 40, 255],
			lineWidthMinPixels: 1.4,
			coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
		})
	];
}
