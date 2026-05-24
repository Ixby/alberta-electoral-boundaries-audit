// @ts-nocheck
// Alberta Electoral Boundary Audit — pointer/wheel/keyboard gesture engine
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Hot-path contract: pointermove → vbPanBy → vpVbPanBy(ctx) → RAF only.
// No promises, no async, no closures that re-allocate on each event.

import type { MapCtx } from './types';
import { vbZoomAt as vpVbZoomAt, vbPanBy as vpVbPanBy, animateToVB as vpAnimateToVB, getStageRect as vpGetStageRect } from './viewport';
import { applyFallback as sl_applyFallback, resetFallback as sl_resetFallback } from './svgLoader';
import { tipTarget, vaTarget, showTip, hideTip, showCallout, hideCallout, showVaCallout, hideVaCallout, setEdHighlight, snapToED, zoomEdTo70 } from './edInteraction';

export function initGestures(ctx: MapCtx, stage): void {
  // ctx-bound local helpers (declared once, reused by all handlers)
  function _animateToVB(vb, dur)  { vpAnimateToVB(ctx, vb, dur); }
  function _getStageRect()        { return vpGetStageRect(ctx); }
  function _showCallout(d)        { showCallout(ctx, d); }
  function _hideCallout()         { hideCallout(ctx); }
  function _showVaCallout(d)      { showVaCallout(ctx, d); }
  function _hideVaCallout()       { hideVaCallout(ctx); }
  function _setEdHighlight(p)     { setEdHighlight(ctx, p); }
  function _snapToED(pathEl, force) { snapToED(ctx, pathEl, !!force, _animateToVB, _getStageRect); }
  function _zoomEdTo70(pathEl)    { zoomEdTo70(ctx, pathEl, _animateToVB, _getStageRect); }

  function _vaDataForMap() { return ctx.allVaData && ctx.allVaData[ctx.mapPrimary]; }
  function _vaRec(el) {
    const vaData = _vaDataForMap();
    return vaData ? vaData[el.getAttribute('data-va-id')] : null;
  }

  // ── Unified zoom (viewbox + fallback) ────────────────────────────────────
  function zoomAt(mx, my, factor) {
    if (!ctx.ready) return;
    if (ctx.mode === 'viewbox') {
      vpVbZoomAt(ctx, mx, my, factor);
    } else {
      const newScale = Math.min(Math.max(ctx.fbScale * factor, 0.05), 200);
      const ratio = newScale / ctx.fbScale;
      ctx.fbTx = mx - ratio * (mx - ctx.fbTx);
      ctx.fbTy = my - ratio * (my - ctx.fbTy);
      ctx.fbScale = newScale;
      sl_applyFallback(ctx);
    }
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
    ctx.ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    try { stage.setPointerCapture(e.pointerId); } catch (_) {}
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
      if (ctx.lastPinchDist && dist > 0) zoomAt(mid.x - r.left, mid.y - r.top, dist / ctx.lastPinchDist);
      if (ctx.lastPinchMid) {
        if (ctx.mode === 'viewbox') vpVbPanBy(ctx, mid.x - ctx.lastPinchMid.x, mid.y - ctx.lastPinchMid.y);
        else {
          ctx.fbTx += mid.x - ctx.lastPinchMid.x; ctx.fbTy += mid.y - ctx.lastPinchMid.y;
          ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px'; ctx.fbImg.style.top = Math.round(ctx.fbTy) + 'px';
        }
      }
      ctx.lastPinchDist = dist; ctx.lastPinchMid = mid;
      return;
    }

    if (e.pointerType !== 'touch' && !ctx.drag && ctx.mode === 'viewbox' && ctx.edHover) {
      const hit = tipTarget(e);
      if (hit) showTip(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)], e.clientX, e.clientY);
      else hideTip();
    }
    if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
    const dx = e.clientX - ctx.drag.cx, dy = e.clientY - ctx.drag.cy;
    if (!ctx.dragMoved && Math.hypot(e.clientX - ctx.drag.startX, e.clientY - ctx.drag.startY) < 6) return;
    if (!ctx.dragMoved) { ctx.dragMoved = true; hideTip(); }
    ctx.drag.cx = e.clientX; ctx.drag.cy = e.clientY;
    if (ctx.mode === 'viewbox') vpVbPanBy(ctx, dx, dy);
    else {
      ctx.fbTx += dx; ctx.fbTy += dy;
      ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px'; ctx.fbImg.style.top = Math.round(ctx.fbTy) + 'px';
    }
  });

  stage.addEventListener('pointerup', e => {
    ctx.ptrs.delete(e.pointerId);
    try { stage.releasePointerCapture(e.pointerId); } catch (_) {}
    if (ctx.ptrs.size < 2) { ctx.lastPinchDist = null; ctx.lastPinchMid = null; }
    if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
    stage.classList.remove('dragging');
    if (!ctx.dragMoved && ctx.mode === 'viewbox') {
      if (e.pointerType === 'touch') {
        const now = performance.now();
        if (now - ctx.lastTap < 300) {
          const hit = tipTarget(e);
          if (hit) { _zoomEdTo70(hit); }
          else { _hideCallout(); _hideVaCallout(); _animateToVB({ ...ctx.natVB }, 420); }
          ctx.lastTap = 0;
        } else {
          ctx.lastTap = now;
          if (ctx.edHover) {
            const hit = tipTarget(e);
            if (hit) {
              const vaHit = _vaDataForMap() ? vaTarget(e) : null;
              const vaRec  = vaHit ? _vaRec(vaHit) : null;
              if (vaRec && vaRec.ed_name && vaRec.ed_name === ctx.selectedEdName) {
                _showVaCallout(vaRec);
              } else {
                _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
                _setEdHighlight(hit);
                _snapToED(hit);
                _hideVaCallout();
              }
            } else { _hideCallout(); _hideVaCallout(); }
          }
        }
      } else if (ctx.edHover) {
        const hit = tipTarget(e);
        if (hit) {
          hideTip();
          const vaHit = _vaDataForMap() ? vaTarget(e) : null;
          const vaRec  = vaHit ? _vaRec(vaHit) : null;
          if (vaRec && vaRec.ed_name && vaRec.ed_name === ctx.selectedEdName) {
            _showVaCallout(vaRec);
          } else {
            _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
            _setEdHighlight(hit);
            if (!ctx.mapLocked) _snapToED(hit);
            _hideVaCallout();
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
  });

  stage.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch') hideTip(); });

  stage.addEventListener('dblclick', e => {
    if (!ctx.ready) return;
    if (ctx.mode === 'viewbox') {
      const hit = tipTarget(e);
      if (hit) _zoomEdTo70(hit);
      else _animateToVB({ ...ctx.natVB }, 420);
    } else sl_resetFallback(ctx, stage);
  });
}
