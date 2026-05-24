// @ts-nocheck
// Alberta Electoral Boundary Audit — MapCtx type
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Shared mutable context passed to all mapEngine sub-modules.
// Created once at IIFE init time; shape is fixed (no hidden-class churn in V8).

export type ViewBox = { x: number; y: number; w: number; h: number };

export type MapCtx = {
  // SVG load mode
  mode:               'viewbox' | 'fallback' | null;
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

  // Fallback image state
  fbImg:              HTMLImageElement | null;
  fbNatW:             number;
  fbNatH:             number;
  fbScale:            number;
  fbTx:               number;
  fbTy:               number;

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
};
