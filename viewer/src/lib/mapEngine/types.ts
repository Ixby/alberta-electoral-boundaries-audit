// @ts-nocheck
// Alberta Electoral Boundary Audit — MapCtx type
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Shared mutable context passed to all mapEngine sub-modules.
// Created once at IIFE init time; shape is fixed (no hidden-class churn in V8).

export type ViewBox = { x: number; y: number; w: number; h: number };

export type MapKey = 'minority' | 'majority' | '2019';
export type LayerKey = 'vote' | 'ed-fill' | 'ed-lines' | 'eg';

// Events emitted by the engine to outside subscribers (currently: share-link
// auto-generation). Keep this union as the single source of truth; share.ts
// re-exports it as FlightEvent.
export type MapEngineEvent =
  | { type: 'map_switch'; primary: MapKey; mapOn: Record<MapKey, boolean> }
  | { type: 'layer';      key: LayerKey;   on: boolean }
  | { type: 'ed_focus';   ed_id: number };

export type MapEngineEventHandler = (event: MapEngineEvent) => void;

export type MapCtx = {
  // SVG load mode
  mode:               'viewbox' | null;
  ready:              boolean;

  // Viewport
  svgEl:              SVGSVGElement | null;
  natVB:              ViewBox | null;
  curVB:              ViewBox | null;
  settledVB:          ViewBox | null;

  // Stage rect cache
  stageRect:          DOMRect | null;

  // RAF / CSS-transform animation
  rafId:              number | null;
  pendingTx:          number;
  pendingTy:          number;
  pendingSx:          number;
  settleTimer:        ReturnType<typeof setTimeout> | null;

  // Focus management
  prevFocus:          Element | null;

  // Map selector state
  mapOn:              Record<string, boolean>;
  mapPrimary:         string | null;
  mapActivationOrder: string[];
  svgCache:           Record<string, Document>;
  overlayInSvg:       Record<string, Element | null>;
  layerState:         Record<string, boolean>;
  mapLocked:          boolean;

  // ED hover data
  edHover:            Record<string, any> | null;
  allHoverData:       Record<string, Record<string, any>>;
  nameIndex:          Record<string, Record<string, any>>;

  // VA (voting area) data
  allVaData:          Record<string, Record<string, any>>;
  selectedVaId:       string | null;

  // ED selection
  selectedEdName:     string | null;
  highlightPath:      SVGGElement | null;

  // Anomaly highlight
  anomalyOn:          boolean;
  anomalyOverlay:     SVGGElement | null;

  // Gesture state
  drag:               { cx: number; cy: number; startX: number; startY: number; id: number } | null;
  dragMoved:          boolean;
  ptrs:               Map<number, { x: number; y: number }>;
  lastPinchDist:      number | null;
  lastPinchMid:       { x: number; y: number } | null;
  lastTap:            number;

  // viewport cache
  _lastStrokeW?:      number;
};
