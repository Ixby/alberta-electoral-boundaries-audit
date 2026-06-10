// Alberta Electoral Boundary Audit — cross-module visual constants
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Constants shared between maps.ts (boundary tint, overlay rendering) and
// layers.ts (ED-fill identity colour when partisan layer is off). Kept in
// its own module to avoid the otherwise-circular maps ↔ layers import edge.

import type { MapKey } from './types';

// Per-map accent palette. Each map advertises its identity through this
// colour at every visual layer: boundary lines (maps.applyBoundaryColor),
// boundary overlays (maps.extractBoundaryGroup), and the ED hover-layer
// fill when no partisan/EG layer is overriding it (layers.applyEdFillLayer
// off-state).
export const MAP_ACCENT_COLORS: Record<MapKey, string> = {
  minority: '#6B35A7',  // purple
  majority: '#1A7A6E',  // teal/green
  '2019':   '#7a98b4',  // muted blue
};

// Default tint opacity for the ED-fill OFF state — visible but doesn't
// overpower partisan or vote-layer information layered above.
export const MAP_ACCENT_FILL_ALPHA = 0.18;
