# Map Explorer Rebuild — deck.gl + Bottom-Dock UI

**Status:** Design (awaiting review)
**Date:** 2026-06-18
**Author:** Will Conner (with Claude)

## 1. Problem

The interactive map explorer is slow and janky. Diagnosis:

- Each map variant (minority / majority / 2019) is a **~37 MB hi-res SVG** (`docs/images/cover_art_*_hires.svg`), ~112 MB total. Every map toggle does `fetch()` → `DOMParser` → inject **~4,765 `<path>` elements** into the live DOM.
- The weight and the jank are both the **per-VA heatmap layer** (4,765 voting-area polygons at full precision; matplotlib emits them with `path.simplify = False`). The 89 ED boundaries are trivial by comparison.
- Pan/zoom transforms and repaints ~4,947 SVG DOM nodes — slow even after a file loads.

The vote/attribute data is already small and well-separated (`docs/data/*_hover.json`, 888 KB total). The geometry is the problem.

## 2. Decisions locked (from brainstorming)

1. **Keep the VA layer fully interactive** (per-VA hover retained) → move to GPU rendering.
2. **Preserve the exact projection** (EPSG:3401, Alberta 3TM) so the province shape matches official EA maps and the PDF cover → **deck.gl** with a flat orthographic view (not MapLibre, which forces web-Mercator).
3. **Inputs are the canonical GeoPackages** already used by `build_cover.py`.
4. **Embed per-feature tooltip data into the geometry** (replaces the fragile path-index-aligned `*_hover.json`).
5. **Retire the 3 hi-res web SVGs** (~112 MB); the PDF cover keeps `cover_art.png`.
6. **Full UI overhaul** of the explorer chrome (visual, information architecture, interaction, mobile), identification-first, in the **bottom-dock** layout (mock direction C).

## 3. Architecture

### 3.1 Rendering
A standalone `Deck` instance (`@deck.gl/core` + `@deck.gl/layers`, not the React wrapper) on a `<canvas>`, using:
- `OrthographicView` with `COORDINATE_SYSTEM.CARTESIAN`. Source coordinates are **raw EPSG:3401 metres**; deck.gl treats them as flat XY, so the rendered shape is pixel-identical to the current matplotlib output. North-up orientation is fixed at export/view config and verified against the current render. (Known gotcha: deck.gl orthographic Y direction — resolve by negating northing at export or `flipY`, then eyeball-confirm orientation.)
- Layers per active map:
  - `PolygonLayer` — VA fills. `getFillColor` reads the precomputed `fill` property. `pickable: true`.
  - `PathLayer` — ED boundaries. **All EDs of the active map are drawn in one uniform colour** (each of the three maps has its own single boundary colour). Stroke uses `widthUnits: 'pixels'` with `widthMinPixels` so lines stay a crisp constant width at every zoom level. `pickable: true` for ED selection.
  - **Selected ED** gets a **glow** highlight (e.g. a wider, soft-edged stroke or an additive `PathLayer`/`PolygonLayer` outline) — only the active district glows; all others keep the uniform map colour.

**Deep zoom (up to ~40,000×).** deck.gl rasterizes vector geometry on the GPU at render time, so polygon edges and strokes are resolution-independent — crisp at any zoom, no LOD tiling needed. The only deep-zoom hazard is GPU float32 precision over province-scale coordinates (see §11), handled by shifting coordinates to a local origin.
- **Lazy-loaded**: deck.gl and the active map's geometry are dynamically `import()`ed only when the explorer opens (`#zoom-trigger`), so the initial page load is unaffected.
- **WebGL fallback**: if WebGL is unavailable, render the existing per-map `cover_art.png` as a static image with a short "interactive map needs WebGL" note. Graceful degradation, no hard failure.

### 3.2 Data
Per map (minority / majority / 2019), two static files under `docs/data/`:
- `va_<map>.geojson` — 4,765 VA polygons, **EPSG:3401 coords shifted to a local origin** (§11), **topology-preserving simplification** so shared edges stay coincident (no inter-polygon gaps — this replaces the SVG micro-stroke gap-fill hack). Each feature carries `{fill, ucp_pct, ndp_pct, in_person_votes, poll_name, ed_name}`.
- `ed_<map>.geojson` — 89/87 ED polygons (boundary + hit), with `{name, ucp_pct, ndp_pct, votes, pop, va_count, region}`.

**Crispness over size.** Deep-zoom fidelity (up to ~40,000×) is the priority; the map must look good at maximum zoom. Because GPU vector rendering is resolution-independent, crispness does not depend on simplification — simplification is purely a download-size lever, so it must be **gentle**: remove only redundant (collinear / sub-millimetre) vertices, never real boundary detail. There is **no hard size budget**; the target is the smallest file that loses **zero** visible detail at 40,000×. Expectation: a few MB raw, ~1–3 MB gzipped per VA file — still a ~10× win over 37 MB and irrelevant to GPU smoothness. Coordinates are quantized to millimetre precision (sub-pixel at max zoom) for size with no visible loss.

Simplification uses the **`topojson` Python package** (`Topology(...).toposimplify(tolerance)`) inside the build script — topology-aware, so adjacent VAs don't separate. Tolerance set conservatively low and verified by eye at maximum zoom (a size regression test guards against accidental bloat, but fidelity wins ties).

## 4. Data pipeline (build script)

Extend `analysis/scripts/build_cover.py` (it already loads canonical GeoPackages, computes per-VA partisan×density fills via `_va_fill`, and does the VA→ED vote join). Changes:

- **Add** a GeoJSON export path: reuse the existing `va_render` GeoDataFrame and `eds` frame; for each, run topology-preserving simplification, attach the embedded properties (the same values currently written to `*_hover.json`, plus the precomputed `fill` hex/rgb), and write `va_<map>.geojson` / `ed_<map>.geojson`.
- **Remove** the hi-res SVG export (`plt.savefig(..., format="svg")` and `_tag_ed_hover_paths`) from the web path. **Keep** `cover_art.png` (used by the PDF cover and the WebGL fallback).
- The legacy `*_hover.json` files may be deleted once the viewer no longer reads them (properties now live in the GeoJSON). Keep the export function until the viewer cutover is verified.
- In-script validation: feature counts (4,765 VA, 89/89/87 ED), every feature has the required props, output gzips under budget. Fail loudly otherwise.

## 5. UI redesign — Bottom-dock (direction C)

Identification-first: when a district is selected, the panel leads with plain identity; partisan data is a calm second tier (consistent with the project's no-per-district-verdict stance).

**Desktop layout** (fullscreen explorer stage):
- **Search** pill, top-left: "Find your riding or address…".
- **Map switch** segmented control, top-right: Minority / Majority / 2019.
- **Zoom** rail (+/−), bottom-right; **legend** (UCP/NDP swatches) bottom-left.
- **Bottom dock** — a slim persistent bar across the foot of the stage:
  `[ eyebrow: "2026 minority proposal" · district name (serif) · location line ]  |  [ Residents: 46,210 ]  |  [ 2023 vote bar + UCP%/NDP% ]`
- Map area is maximal (only the dock height is reserved).

**Mobile**: identical structure; the dock grows taller and stacks (identity → residents → vote bar), search full-width on top, map switch directly below. No overlap with the map.

**Content & interaction**:
- **Click / tap a district** → dock updates to that ED's identity + residents + 2023 vote split. This is the primary selection.
- **Hover a VA** (desktop) → a lightweight tooltip with the poll name and its UCP/NDP split (preserves VA-level interactivity).
- **Empty state** (nothing selected): dock shows a one-line prompt and the active map's name.
- **Map switch** swaps the active VA+ED layers and refreshes the dock/legend. Each map draws **all** its ED boundaries in that map's single uniform colour; only the **selected** ED glows.
- **Anomaly highlight** (chair-flagged boundaries) and any layer toggles live as a small control near the legend.
- **Search** resolves to a district and animates to its bounds (respecting reduced-motion).

Visual language matches the editorial site: cream/`--bg` panels, `--heading` navy, serif (Palatino/Georgia) for district names and numbers, system sans for controls, `--nav-accent` for active/selected affordances.

## 6. Interaction parity checklist (must survive the rewrite)

Pan · zoom (wheel / pinch / buttons) · district select → dock · VA hover tooltip · active-ED boundary highlight · per-map boundary recolor · 3-map switch · search → zoom-to-district · named-ED deep zoom / deep-link · anomaly highlight · intro/onboarding modal (refreshed) · reduced-motion · RTL · keyboard focus & a11y for the new controls.

## 7. Removed / kept

**Removed** (after parity is verified in the browser): the 3 hi-res SVGs (~112 MB), the SVG-specific `mapEngine` modules (svgLoader, the SVG pan/zoom viewport math, SVG-path hit detection). **Kept / refactored**: search logic, named-ED zoom, anomaly data, the per-map vote data, `cover_art.png`.

## 8. Error handling / edge cases

- WebGL unavailable → static PNG fallback (§3.1).
- Search no-match → inline "no riding found" message, no state change.
- A map's GeoJSON fails to load → keep the previous map, surface a non-blocking error.
- Reduced-motion → no fly-to animation; instant jumps.
- Picking nothing (click on empty stage) → clears selection to empty state.

## 9. Testing

- **Data export tests** (Python): feature counts per map, required-property presence, gzip size budget, deterministic output.
- **Geometry integrity**: simplified VA layer has no gaps at shared edges (topology check); ED↔VA `ed_name` references resolve.
- **Render smoke** (viewer): deck.gl initializes, all three maps load, switch works.
- **Interaction unit tests**: hover returns the correct feature props; click selects the right ED; search resolves to the right district.
- **Visual regression**: deck.gl render vs current SVG at 2–3 zoom levels **including maximum (~40,000×)** — edges crisp, no jitter, no inter-VA gaps (eyeballed locally on the dev server).
- **Size regression guard** in CI: flags if a `va_<map>.geojson` grows unexpectedly (a guard against accidental bloat, not a hard cap — fidelity wins ties).

## 10. Rollout / rollback

Build incrementally, old explorer intact until parity:
1. **Phase 1 — data pipeline** (independent): extend `build_cover.py`, emit GeoJSON, add data tests. No viewer change yet.
2. **Phase 2 — deck.gl render + dock UI**: new explorer component behind a flag, rendering from the GeoJSON, wired to the new bottom-dock UI. The SVG explorer stays as the default until parity is confirmed in the browser.
3. **Phase 3 — cutover & cleanup**: flip the flag, delete the SVG engine modules and the 112 MB SVGs, drop unused `*_hover.json`. Each phase is its own commit / set of commits for clean rollback.

## 11. Open risks

- **deck.gl orthographic orientation/scale** needs a careful first-pass calibration against the current render (Y direction, fit-to-bounds). Mitigated by visual regression early in Phase 2.
- **GPU float32 precision at 40,000× zoom**: raw 3401 eastings/northings are large (~hundreds of thousands of metres); float32 precision there (~cm) becomes multiple pixels at extreme zoom, causing edge jitter. **Mitigation:** shift all coordinates to a local origin near Alberta's centre at export so on-GPU magnitudes are small; if residual jitter remains, enable deck.gl 64-bit (`Fp64`/double-precision) handling. Validate at maximum zoom early in Phase 2 — this is the single most important deep-zoom check.
- **Simplification fidelity**: tolerance must stay conservative enough that no real boundary detail is lost at 40,000×. Crispness is the priority over size; mitigated by eyeball check at max zoom, with size as a soft guard only.
- **Bundle size**: deck.gl adds ~150–200 KB gz, but only on explorer open, and it replaces 112 MB of SVG. Net strongly positive.
- **Feature-parity surface is large** (§6); Phase 2 must enumerate each as a task so nothing silently drops.
