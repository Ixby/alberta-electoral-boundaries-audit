// Alberta Electoral Boundary Audit — pointer/wheel/keyboard gesture engine
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Hot-path contract: pointermove → vbPanBy → vpVbPanBy(ctx) → RAF only.
// No promises, no async, no closures that re-allocate on each event.

import type { MapCtx, ViewBox } from './types';
import { vbZoomAt as vpVbZoomAt, vbPanBy as vpVbPanBy, vbPinch as vpVbPinch, animateToVB as vpAnimateToVB, getStageRect as vpGetStageRect, commitSettle as vpCommitSettle, rasterIsStale as vpRasterIsStale } from './viewport';
import { tipTarget, vaTarget, showTip, hideTip, showCallout, hideCallout, showVaCallout, hideVaCallout, setEdHighlight, snapToED, zoomEdTo70 } from './edInteraction';
import { DOM_IDS } from './domIds';

export function initGestures(ctx: MapCtx, stage: HTMLElement): void {
  // ctx-bound local helpers (declared once, reused by all handlers)
  function _animateToVB(vb: ViewBox, dur: number)  { vpAnimateToVB(ctx, vb, dur); }
  function _getStageRect()                          { return vpGetStageRect(ctx); }
  function _showCallout(d: any)                     { showCallout(ctx, d); }
  function _hideCallout()                           { hideCallout(ctx); }
  function _showVaCallout(d: any)                   { showVaCallout(ctx, d); }
  function _hideVaCallout()                         { hideVaCallout(ctx); }
  function _setEdHighlight(p: SVGGraphicsElement | null) { setEdHighlight(ctx, p); }
  function _snapToED(pathEl: SVGGraphicsElement, force?: boolean) { snapToED(ctx, pathEl, !!force, _animateToVB, _getStageRect); }
  function _zoomEdTo70(pathEl: SVGGraphicsElement) { zoomEdTo70(ctx, pathEl, _animateToVB, _getStageRect); }

  function _vaDataForMap() { return ctx.mapPrimary ? ctx.allVaData[ctx.mapPrimary] : null; }
  function _vaRec(el: Element) {
    const vaData = _vaDataForMap();
    const id = el.getAttribute('data-va-id');
    return vaData && id ? vaData[id] : null;
  }

  // ── Zoom ──────────────────────────────────────────────────────────────────
  function zoomAt(mx: number, my: number, factor: number) {
    if (!ctx.ready) return;
    vpVbZoomAt(ctx, mx, my, factor);
  }

  // ── Pinch helpers ─────────────────────────────────────────────────────────
  function _ptrMid() {
    const [a, b] = [...ctx.ptrs.values()];
    return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
  }
  function _ptrDist() {
    const [a, b] = [...ctx.ptrs.values()];
    return Math.hypot(a.x - b.x, a.y - b.y);
  }

  // ── Wheel ─────────────────────────────────────────────────────────────────
  stage.addEventListener('wheel', e => {
    e.preventDefault();
    const r = _getStageRect();
    zoomAt(e.clientX - r.left, e.clientY - r.top, Math.pow(0.88, e.deltaY / 100));
  }, { passive: false });

  // ── Pointer events ────────────────────────────────────────────────────────
  stage.addEventListener('pointerdown', e => {
    if (!ctx.ready) return;
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    // Pre-settle if the cached raster scale is significantly different from
    // the current viewBox scale. Without this, a drag at 30× zoom over a
    // raster cached at 1× makes the GPU stretch a stale, low-resolution
    // layer every frame — that's the "drag feels heavy" symptom at extreme
    // zoom. The settle is cheap at extreme zoom because only the small
    // visible viewBox region needs rendering.
    if (ctx.ptrs.size === 0 && vpRasterIsStale(ctx)) vpCommitSettle(ctx);
    ctx.ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    try { stage.setPointerCapture(e.pointerId); } catch (_) {}
    ctx.gestureActive = true;
    if (ctx.ptrs.size === 2) {
      if (ctx.drag) { ctx.drag = null; stage.classList.remove('dragging'); }
      hideTip();
      ctx.lastPinchDist = _ptrDist();
      ctx.lastPinchMid = _ptrMid();
      return;
    }
    if (ctx.ptrs.size > 2) return;
    ctx.drag = { cx: e.clientX, cy: e.clientY, startX: e.clientX, startY: e.clientY, id: e.pointerId };
    ctx.dragMoved = false;
    stage.classList.add('dragging');
  });

  stage.addEventListener('pointermove', e => {
    if (!ctx.ready || !ctx.ptrs.has(e.pointerId)) return;
    ctx.ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });

    if (ctx.ptrs.size >= 2) {
      const dist = _ptrDist(), mid = _ptrMid(), r = _getStageRect();
      // Single composite pinch transform — replaces what used to be two
      // sequential calls (zoomAt + panBy) per pointermove. The composite
      // formulation in viewport.vbPinch reads stage.curVB exactly once and
      // writes exactly one updated viewBox + RAF, so iOS's coalesced or
      // out-of-order pointermove events can't desync the zoom and pan
      // half-steps against each other.
      if (ctx.lastPinchDist && ctx.lastPinchMid) {
        vpVbPinch(ctx, ctx.lastPinchMid, ctx.lastPinchDist, mid, dist, r.left, r.top);
      }
      ctx.lastPinchDist = dist; ctx.lastPinchMid = mid;
      return;
    }

    if (e.pointerType !== 'touch' && !ctx.drag && ctx.edHover) {
      const hit = tipTarget(e);
      if (hit) showTip(ctx.edHover[parseInt(hit.getAttribute('data-ed-id') || '0', 10)], e.clientX, e.clientY);
      else hideTip();
    }
    if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
    const dx = e.clientX - ctx.drag.cx, dy = e.clientY - ctx.drag.cy;
    if (!ctx.dragMoved && Math.hypot(e.clientX - ctx.drag.startX, e.clientY - ctx.drag.startY) < 6) return;
    if (!ctx.dragMoved) { ctx.dragMoved = true; hideTip(); }
    ctx.drag.cx = e.clientX; ctx.drag.cy = e.clientY;
    vpVbPanBy(ctx, dx, dy);
  });

  stage.addEventListener('pointerup', e => {
    ctx.ptrs.delete(e.pointerId);
    try { stage.releasePointerCapture(e.pointerId); } catch (_) {}
    if (ctx.ptrs.size < 2) { ctx.lastPinchDist = null; ctx.lastPinchMid = null; }
    if (ctx.ptrs.size === 0) {
      // All fingers up → end of gesture. Settle to commit viewBox now
      // (the in-gesture suppression in _applyVB means no timer was queued).
      ctx.gestureActive = false;
      vpCommitSettle(ctx);
    }
    if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
    stage.classList.remove('dragging');
    if (!ctx.dragMoved) {
      if (e.pointerType === 'touch') {
        const now = performance.now();
        if (now - ctx.lastTap < 300) {
          const hit = tipTarget(e) as SVGGraphicsElement | null;
          if (hit) { _zoomEdTo70(hit); }
          else {
            const _wasSelected = !!ctx.selectedEdName;
            _hideCallout(); _hideVaCallout();
            if (!_wasSelected && ctx.natVB) _animateToVB({ ...ctx.natVB }, 420);
          }
          ctx.lastTap = 0;
        } else {
          ctx.lastTap = now;
          if (ctx.edHover) {
            const hit = tipTarget(e) as SVGGraphicsElement | null;
            if (hit) {
              const vaHit = _vaDataForMap() ? vaTarget(e) : null;
              const vaRec  = vaHit ? _vaRec(vaHit) : null;
              if (vaRec && vaRec.ed_name && vaRec.ed_name === ctx.selectedEdName) {
                _showVaCallout(vaRec);
              } else {
                _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id') || '0', 10)]);
                _setEdHighlight(hit);
                _snapToED(hit);
              }
            } else { _hideCallout(); _hideVaCallout(); }
          }
        }
      } else if (ctx.edHover) {
        const hit = tipTarget(e) as SVGGraphicsElement | null;
        if (hit) {
          hideTip();
          const vaHit = _vaDataForMap() ? vaTarget(e) : null;
          const vaRec  = vaHit ? _vaRec(vaHit) : null;
          if (vaRec && vaRec.ed_name && vaRec.ed_name === ctx.selectedEdName) {
            _showVaCallout(vaRec);
          } else {
            _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id') || '0', 10)]);
            _setEdHighlight(hit);
            if (!ctx.mapLocked) _snapToED(hit);
          }
        } else { _hideCallout(); _hideVaCallout(); }
      }
    }
    ctx.drag = null;
  });

  stage.addEventListener('pointercancel', e => {
    ctx.ptrs.delete(e.pointerId);
    if (ctx.drag && ctx.drag.id === e.pointerId) { ctx.drag = null; stage.classList.remove('dragging'); }
    if (ctx.ptrs.size < 2) { ctx.lastPinchDist = null; ctx.lastPinchMid = null; }
    if (ctx.ptrs.size === 0) { ctx.gestureActive = false; vpCommitSettle(ctx); }
  });

  stage.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch') hideTip(); });

  stage.addEventListener('dblclick', e => {
    if (!ctx.ready) return;
    const hit = tipTarget(e) as SVGGraphicsElement | null;
    if (hit) _zoomEdTo70(hit);
    else if (ctx.natVB) _animateToVB({ ...ctx.natVB }, 420);
  });

  // ── Keyboard pan / zoom ───────────────────────────────────────────────────
  document.addEventListener('keydown', e => {
    if (!ctx.ready) return;
    const overlay = document.getElementById(DOM_IDS.zoomOverlay);
    if (!overlay || overlay.style.display === 'none') return;
    const active = document.activeElement;
    if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.tagName === 'SELECT')) return;
    const r = _getStageRect();
    const PAN = 0.18;
    switch (e.key) {
      case 'ArrowLeft':  e.preventDefault(); vpVbPanBy(ctx,  r.width  * PAN, 0); break;
      case 'ArrowRight': e.preventDefault(); vpVbPanBy(ctx, -r.width  * PAN, 0); break;
      case 'ArrowUp':    e.preventDefault(); vpVbPanBy(ctx, 0,  r.height * PAN); break;
      case 'ArrowDown':  e.preventDefault(); vpVbPanBy(ctx, 0, -r.height * PAN); break;
      case '+': case '=': e.preventDefault(); vpVbZoomAt(ctx, r.width / 2, r.height / 2, 1.3); break;
      case '-': case '_': e.preventDefault(); vpVbZoomAt(ctx, r.width / 2, r.height / 2, 1 / 1.3); break;
      case '0':           e.preventDefault(); if (ctx.natVB) _animateToVB({ ...ctx.natVB }, 420); break;
    }
  });
}
