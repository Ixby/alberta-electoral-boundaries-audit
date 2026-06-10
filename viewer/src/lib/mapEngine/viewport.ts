// Alberta Electoral Boundary Audit — viewport & animation
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// CSS-transform gesture animation: pointermove/wheel drive applyVB, which writes
// a translate+scale transform onto the SVG element (compositor-threaded).
// After SETTLE_MS of inactivity, _doSettle commits the viewBox attribute and
// resets the transform so the browser re-rasterizes from SVG paths at native res.
//
// Hot path: pointerdown → pointermove → vbPanBy → applyVB → RAF
// ctx properties accessed here are fixed-shape (defined once in mapEngine.ts),
// so V8 uses inline caches — no hidden-class churn.

import type { MapCtx, ViewBox, MapKey } from './types';
import { DOM_IDS } from './domIds';

const SETTLE_MS = 250;

// ── Internal helpers ──────────────────────────────────────────────────────────

function _updateZoomDisplay(ctx: MapCtx): void {
  if (!ctx.natVB || !ctx.curVB) return;
  const pct = Math.round(ctx.natVB.w / ctx.curVB.w * 100);
  const el  = document.getElementById(DOM_IDS.zoomPct);
  const sl  = document.getElementById(DOM_IDS.zoomSlider) as HTMLInputElement | null;
  if (el) el.textContent = pct + '%';
  if (sl) sl.value = String(Math.min(3000, Math.max(25, pct)));
}

function _renderBounds(ctx: MapCtx): { rw: number; rh: number; ox: number; oy: number } {
  const r = getStageRect(ctx);
  const sw = r.width, sh = r.height;
  const natVB = ctx.natVB!;
  const ar = natVB.w / natVB.h;
  let rw: number, rh: number;
  if (ar < sw / sh) { rh = sh; rw = sh * ar; }
  else               { rw = sw; rh = sw / ar; }
  return { rw, rh, ox: (sw - rw) / 2, oy: (sh - rh) / 2 };
}

function _doSettle(ctx: MapCtx): void {
  ctx.settleTimer = null;
  if (!ctx.svgEl || !ctx.curVB) return;
  ctx.settledVB = null;
  if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
  ctx.svgEl.style.transform = '';
  ctx.svgEl.style.willChange = '';
  ctx.svgEl.style.transformOrigin = '';
  ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
  _updateZoomDisplay(ctx);
  requestAnimationFrame(() => updateStrokeWidths(ctx));
}

function _applyVB(ctx: MapCtx, vb: ViewBox): void {
  if (!ctx.curVB) return;
  if (!ctx.settledVB) {
    ctx.settledVB = { ...ctx.curVB };
    if (ctx.svgEl) { ctx.svgEl.style.willChange = 'transform'; ctx.svgEl.style.transformOrigin = '0 0'; }
  }
  ctx.curVB = vb;
  const settledVB = ctx.settledVB;
  const { rw, rh, ox, oy } = _renderBounds(ctx);
  const sx = settledVB.w / ctx.curVB.w;
  ctx.pendingTx = (settledVB.x - ctx.curVB.x) * rw / ctx.curVB.w + ox * (1 - sx);
  ctx.pendingTy = (settledVB.y - ctx.curVB.y) * rh / ctx.curVB.h + oy * (1 - sx);
  ctx.pendingSx = sx;
  if (ctx.rafId === null) {
    ctx.rafId = requestAnimationFrame(() => {
      ctx.rafId = null;
      if (ctx.svgEl) ctx.svgEl.style.transform =
        `translate(${ctx.pendingTx}px,${ctx.pendingTy}px) scale(${ctx.pendingSx})`;
      _updateZoomDisplay(ctx);
    });
  }
  if (ctx.settleTimer !== null) clearTimeout(ctx.settleTimer);
  // Skip settle scheduling while an active gesture is in flight. The settle
  // commits viewBox-as-attribute and forces an SVG re-rasterize that takes
  // ~5–20 ms on the hires cover art; if it fires mid-pinch (e.g. during a
  // slow pause between two finger motions) the visual jumps. We let the
  // pointerup handler trigger settle once the gesture ends.
  if (!ctx.gestureActive) {
    ctx.settleTimer = setTimeout(() => _doSettle(ctx), SETTLE_MS);
  }
}

// Explicit settle trigger — used by the gesture engine on pointerup when the
// gesture flag clears, so the SVG re-rasterizes to its final viewBox once
// without interfering with the gesture itself.
export function commitSettle(ctx: MapCtx): void {
  if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
  _doSettle(ctx);
}

function _zoomToPct(ctx: MapCtx, pct: number): void {
  if (!ctx.ready || !ctx.natVB || !ctx.curVB) return;
  const targetW = ctx.natVB.w * 100 / pct;
  const targetH = ctx.natVB.h * 100 / pct;
  const cx = ctx.curVB.x + ctx.curVB.w / 2;
  const cy = ctx.curVB.y + ctx.curVB.h / 2;
  ctx.curVB = { x: cx - targetW/2, y: cy - targetH/2, w: targetW, h: targetH };
  _doSettle(ctx);
}

// ── Exported API ──────────────────────────────────────────────────────────────

export function getStageRect(ctx: MapCtx): DOMRect {
  if (!ctx.stageRect) {
    const stage = document.getElementById(DOM_IDS.zoomStage);
    ctx.stageRect = stage ? stage.getBoundingClientRect() : new DOMRect();
  }
  return ctx.stageRect;
}

export function updateZoomDisplay(ctx: MapCtx): void {
  _updateZoomDisplay(ctx);
}

export function updateStrokeWidths(ctx: MapCtx): void {
  if (!ctx.svgEl || !ctx.natVB || !ctx.curVB) return;
  const zf = ctx.natVB.w / ctx.curVB.w;
  const primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
  if (Math.abs(primaryW - (ctx._lastStrokeW ?? -1)) < 0.005) return;
  ctx._lastStrokeW = primaryW;
  const overlayW = primaryW * 0.7; // proportional to primary, no absolute cap (0.35 cap was sub-pixel at default zoom)
  const pLc = ctx.svgEl.querySelector('#LineCollection_1');
  if (pLc) pLc.querySelectorAll<SVGPathElement>('path').forEach(function(p) {
    p.style.strokeWidth = String(primaryW);
  });
  (['minority', 'majority', '2019'] as const).forEach(function(key) {
    const og = ctx.overlayInSvg[key] as SVGElement | null;
    if (!og) return;
    // og is the renamed clone of LineCollection_1 (id is now "ed-boundary-overlay-{key}").
    // Query paths directly on og — not via "#LineCollection_1" which no longer matches.
    const paths: ArrayLike<SVGPathElement> =
      og.tagName.toLowerCase() === 'path' ? [og as SVGPathElement] : og.querySelectorAll<SVGPathElement>('path');
    Array.from(paths).forEach(function(p) {
      p.style.strokeWidth = String(overlayW);
    });
  });
}

export function resetVB(ctx: MapCtx): void {
  if (!ctx.natVB) return;
  if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
  if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
  ctx.settledVB = null;
  ctx.curVB = { ...ctx.natVB };
  if (ctx.svgEl) {
    ctx.svgEl.style.transform = '';
    ctx.svgEl.style.willChange = '';
    ctx.svgEl.style.transformOrigin = '';
    ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
  }
  _updateZoomDisplay(ctx);
  updateStrokeWidths(ctx);
}

export function vbZoomAt(ctx: MapCtx, mx: number, my: number, factor: number): void {
  if (!ctx.natVB || !ctx.curVB) return;
  const { rw, rh, ox, oy } = _renderBounds(ctx);
  const lx = mx - ox, ly = my - oy;
  const svgX = ctx.curVB.x + (lx / rw) * ctx.curVB.w;
  const svgY = ctx.curVB.y + (ly / rh) * ctx.curVB.h;
  const newW = Math.max(ctx.natVB.w / 200, Math.min(ctx.natVB.w * 20, ctx.curVB.w / factor));
  const newH = newW * (ctx.natVB.h / ctx.natVB.w);
  _applyVB(ctx, { x: svgX - (lx / rw) * newW, y: svgY - (ly / rh) * newH, w: newW, h: newH });
}

export function vbPanBy(ctx: MapCtx, dx: number, dy: number): void {
  if (!ctx.curVB) return;
  const { rw, rh } = _renderBounds(ctx);
  _applyVB(ctx, { x: ctx.curVB.x - (dx / rw) * ctx.curVB.w, y: ctx.curVB.y - (dy / rh) * ctx.curVB.h, w: ctx.curVB.w, h: ctx.curVB.h });
}

// Composite pinch transform — collapses what used to be vbZoomAt + vbPanBy
// (two _applyVB calls per pointermove) into one. The previous formulation
// composed correctly in steady state but each call recomputed pendingTx/Ty
// from a curVB the prior call had just mutated, which is fragile under iOS's
// coalesced-pointermove behavior — small inconsistencies showed up as visible
// jumps during fast pinches. Single composite write per frame: no jitter.
//
// Geometry: the SVG point that was under lastMid at the previous frame should
// be under mid at this frame; the SVG distance between the two fingers should
// scale by lastDist/dist. rw/rh come from the stage's render rect; they don't
// change within a gesture (only on resize), so we can read them once and
// compose the new viewBox directly.
export function vbPinch(
  ctx: MapCtx,
  lastMid: { x: number; y: number },
  lastDist: number,
  mid: { x: number; y: number },
  dist: number,
  stageLeft: number,
  stageTop: number,
): void {
  if (!ctx.natVB || !ctx.curVB || !lastDist || dist <= 0) return;
  const { rw, rh, ox, oy } = _renderBounds(ctx);

  // SVG point under last frame's midpoint (relative to current viewBox)
  const lastLx = (lastMid.x - stageLeft) - ox;
  const lastLy = (lastMid.y - stageTop) - oy;
  const svgX = ctx.curVB.x + (lastLx / rw) * ctx.curVB.w;
  const svgY = ctx.curVB.y + (lastLy / rh) * ctx.curVB.h;

  // New viewBox dimensions: scale current by (dist/lastDist), clamp to native bounds
  const factor = dist / lastDist;
  const newW = Math.max(ctx.natVB.w / 200, Math.min(ctx.natVB.w * 20, ctx.curVB.w / factor));
  const newH = newW * (ctx.natVB.h / ctx.natVB.w);

  // New viewBox origin: place svgX,svgY under the CURRENT frame's mid
  const lx = (mid.x - stageLeft) - ox;
  const ly = (mid.y - stageTop) - oy;
  _applyVB(ctx, {
    x: svgX - (lx / rw) * newW,
    y: svgY - (ly / rh) * newH,
    w: newW,
    h: newH,
  });
}

export function animateToVB(ctx: MapCtx, targetVB: ViewBox, dur: number): void {
  if (ctx.mapLocked) return;
  if (!ctx.curVB || !ctx.svgEl) return;
  if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
  if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
  const startVB: ViewBox = { ...ctx.curVB };
  if (!ctx.settledVB) {
    ctx.settledVB = { ...ctx.curVB };
    ctx.svgEl.style.willChange = 'transform';
    ctx.svgEl.style.transformOrigin = '0 0';
  }
  const settledVB = ctx.settledVB;
  const svgEl = ctx.svgEl;
  const t0 = performance.now();
  function step(now: number) {
    const t = Math.min((now - t0) / dur, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    const cur: ViewBox = {
      x: startVB.x + (targetVB.x - startVB.x) * ease,
      y: startVB.y + (targetVB.y - startVB.y) * ease,
      w: startVB.w + (targetVB.w - startVB.w) * ease,
      h: startVB.h + (targetVB.h - startVB.h) * ease,
    };
    ctx.curVB = cur;
    const { rw, rh, ox, oy } = _renderBounds(ctx);
    const sx = settledVB.w / cur.w;
    svgEl.style.transform =
      `translate(${(settledVB.x - cur.x)*rw/cur.w + ox*(1-sx)}px,` +
      `${(settledVB.y - cur.y)*rh/cur.h + oy*(1-sx)}px) scale(${sx})`;
    _updateZoomDisplay(ctx);
    if (t < 1) { requestAnimationFrame(step); }
    else { ctx.settleTimer = setTimeout(() => _doSettle(ctx), SETTLE_MS); }
  }
  requestAnimationFrame(step);
}

export function initViewport(ctx: MapCtx): void {
  const stage = document.getElementById(DOM_IDS.zoomStage);
  if (!stage) return;
  window.addEventListener('resize', () => { ctx.stageRect = null; });
  if (window.ResizeObserver) {
    new ResizeObserver(() => {
      ctx.stageRect = null;
      if (ctx.svgEl && ctx.ready) _doSettle(ctx);
    }).observe(stage);
  }
  const slider = document.getElementById(DOM_IDS.zoomSlider) as HTMLInputElement | null;
  if (slider) {
    slider.addEventListener('input', function() {
      _zoomToPct(ctx, parseInt(slider.value, 10));
    });
  }
}
