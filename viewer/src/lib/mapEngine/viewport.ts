// @ts-nocheck
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

import type { MapCtx, ViewBox } from './types';

const SETTLE_MS = 250;

// ── Internal helpers ──────────────────────────────────────────────────────────

function _updateZoomDisplay(ctx: MapCtx): void {
  let pct: number;
  if (ctx.mode === 'fallback') {
    pct = Math.round(ctx.fbScale * 100);
  } else if (ctx.natVB && ctx.curVB) {
    pct = Math.round(ctx.natVB.w / ctx.curVB.w * 100);
  } else {
    return;
  }
  const el  = document.getElementById('zoom-pct');
  const sl  = document.getElementById('zoom-slider') as HTMLInputElement | null;
  if (el) el.textContent = pct + '%';
  if (sl) sl.value = String(Math.min(3000, Math.max(25, pct)));
}

function _renderBounds(ctx: MapCtx): { rw: number; rh: number; ox: number; oy: number } {
  const r = getStageRect(ctx);
  const sw = r.width, sh = r.height;
  const ar = ctx.natVB.w / ctx.natVB.h;
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
  if (!ctx.settledVB) {
    ctx.settledVB = { ...ctx.curVB };
    if (ctx.svgEl) { ctx.svgEl.style.willChange = 'transform'; ctx.svgEl.style.transformOrigin = '0 0'; }
  }
  ctx.curVB = vb;
  const { rw, rh, ox, oy } = _renderBounds(ctx);
  const sx = ctx.settledVB.w / ctx.curVB.w;
  ctx.pendingTx = (ctx.settledVB.x - ctx.curVB.x) * rw / ctx.curVB.w + ox * (1 - sx);
  ctx.pendingTy = (ctx.settledVB.y - ctx.curVB.y) * rh / ctx.curVB.h + oy * (1 - sx);
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
  ctx.settleTimer = setTimeout(() => _doSettle(ctx), SETTLE_MS);
}

function _zoomToPct(ctx: MapCtx, pct: number): void {
  if (!ctx.ready || ctx.mode !== 'viewbox' || !ctx.natVB || !ctx.curVB) return;
  var targetW = ctx.natVB.w * 100 / pct;
  var targetH = ctx.natVB.h * 100 / pct;
  var cx = ctx.curVB.x + ctx.curVB.w / 2;
  var cy = ctx.curVB.y + ctx.curVB.h / 2;
  ctx.curVB = { x: cx - targetW/2, y: cy - targetH/2, w: targetW, h: targetH };
  _doSettle(ctx);
}

// ── Exported API ──────────────────────────────────────────────────────────────

export function getStageRect(ctx: MapCtx): DOMRect {
  if (!ctx.stageRect) {
    const stage = document.getElementById('zoom-stage');
    ctx.stageRect = stage ? stage.getBoundingClientRect() : new DOMRect();
  }
  return ctx.stageRect;
}

export function updateZoomDisplay(ctx: MapCtx): void {
  _updateZoomDisplay(ctx);
}

export function updateStrokeWidths(ctx: MapCtx): void {
  if (!ctx.svgEl || !ctx.natVB || !ctx.curVB) return;
  var zf = ctx.natVB.w / ctx.curVB.w;
  var primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
  var overlayW = Math.min(0.35, primaryW * 0.6);
  var pLc = ctx.svgEl.querySelector('#LineCollection_1');
  if (pLc) pLc.querySelectorAll('path').forEach(function(p) {
    p.style.strokeWidth = String(primaryW);
  });
  ['minority', 'majority', '2019'].forEach(function(key) {
    var og = ctx.overlayInSvg[key];
    if (og) {
      var lc = og.querySelector('#LineCollection_1');
      if (lc) lc.querySelectorAll('path').forEach(function(p) {
        p.style.strokeWidth = String(overlayW);
      });
    }
  });
}

export function resetVB(ctx: MapCtx): void {
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
  const { rw, rh, ox, oy } = _renderBounds(ctx);
  const lx = mx - ox, ly = my - oy;
  const svgX = ctx.curVB.x + (lx / rw) * ctx.curVB.w;
  const svgY = ctx.curVB.y + (ly / rh) * ctx.curVB.h;
  const newW = Math.max(ctx.natVB.w / 200, Math.min(ctx.natVB.w * 20, ctx.curVB.w / factor));
  const newH = newW * (ctx.natVB.h / ctx.natVB.w);
  _applyVB(ctx, { x: svgX - (lx / rw) * newW, y: svgY - (ly / rh) * newH, w: newW, h: newH });
}

export function vbPanBy(ctx: MapCtx, dx: number, dy: number): void {
  const { rw, rh } = _renderBounds(ctx);
  _applyVB(ctx, { x: ctx.curVB.x - (dx / rw) * ctx.curVB.w, y: ctx.curVB.y - (dy / rh) * ctx.curVB.h, w: ctx.curVB.w, h: ctx.curVB.h });
}

export function animateToVB(ctx: MapCtx, targetVB: ViewBox, dur: number): void {
  if (ctx.mapLocked) return;
  if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
  if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
  const startVB = { ...ctx.curVB };
  if (!ctx.settledVB) {
    ctx.settledVB = { ...ctx.curVB };
    ctx.svgEl.style.willChange = 'transform';
    ctx.svgEl.style.transformOrigin = '0 0';
  }
  const t0 = performance.now();
  function step(now: number) {
    const t = Math.min((now - t0) / dur, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    ctx.curVB = {
      x: startVB.x + (targetVB.x - startVB.x) * ease,
      y: startVB.y + (targetVB.y - startVB.y) * ease,
      w: startVB.w + (targetVB.w - startVB.w) * ease,
      h: startVB.h + (targetVB.h - startVB.h) * ease,
    };
    const { rw, rh, ox, oy } = _renderBounds(ctx);
    const sx = ctx.settledVB.w / ctx.curVB.w;
    ctx.svgEl.style.transform =
      `translate(${(ctx.settledVB.x - ctx.curVB.x)*rw/ctx.curVB.w + ox*(1-sx)}px,` +
      `${(ctx.settledVB.y - ctx.curVB.y)*rh/ctx.curVB.h + oy*(1-sx)}px) scale(${sx})`;
    _updateZoomDisplay(ctx);
    if (t < 1) { requestAnimationFrame(step); }
    else { ctx.settleTimer = setTimeout(() => _doSettle(ctx), SETTLE_MS); }
  }
  requestAnimationFrame(step);
}

export function initViewport(ctx: MapCtx): void {
  const stage = document.getElementById('zoom-stage');
  if (!stage) return;
  window.addEventListener('resize', () => { ctx.stageRect = null; });
  if (window.ResizeObserver) {
    new ResizeObserver(() => {
      ctx.stageRect = null;
      if (ctx.svgEl && ctx.mode === 'viewbox') _doSettle(ctx);
    }).observe(stage);
  }
  const slider = document.getElementById('zoom-slider') as HTMLInputElement | null;
  if (slider) {
    slider.addEventListener('input', function() {
      _zoomToPct(ctx, parseInt(slider.value, 10));
    });
  }
}
