// @ts-nocheck
// Alberta Electoral Boundary Audit — SVG loader & fallback
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Three-tier SVG loading strategy (highest → lowest fidelity):
//   1. Adopt from <object> contentDocument (no re-download, no re-parse).
//   2. XHR + DOMParser + importNode (HTTP or Firefox file://).
//   3. <img> resize fallback (Chrome file://).
//
// After adoption the SVG is inline in the main document; the browser renders
// vector paths at display resolution — no GPU tile limit at any zoom level.
//
// deps shape:
//   { svgUrls, applyBoundaryColor, applyAnomalyHighlight, syncOverlays }

import type { MapCtx } from './types';
import { updateZoomDisplay, updateStrokeWidths, resetVB as vpResetVB } from './viewport';
import { reapplyLayers } from './layers';

// ── VA path merge (perf) ──────────────────────────────────────────────────────
// Collapses 4 771 individually-stroked VA polygons in #PatchCollection_2 into
// one compound <path> per fill colour (~1 400 unique colours in the choropleth).
// Eliminates all stroke computation in that group, cutting Firefox's Skia
// SkPathStroker cost from ~2 400 ms to negligible on a typical load.
// Safe: PatchCollection_2 is purely visual; hover/click lives in #ed_hover_layer.

export function mergeVaPaths(svgRoot: Element): void {
  const g = svgRoot.querySelector('#PatchCollection_2');
  if (!g) return;
  const paths = Array.from(g.querySelectorAll('path'));
  if (paths.length < 50) return; // already merged
  const doc = g.ownerDocument;
  const ns = 'http://www.w3.org/2000/svg';

  // Build #va_hover_layer from paths that carry data-va-id, before the merge destroys them.
  // No-op until SVGs are regenerated with data-va-id attributes.
  const vaPaths = paths.filter(function(p) { return p.hasAttribute('data-va-id'); });
  if (vaPaths.length > 0 && !svgRoot.querySelector('#va_hover_layer')) {
    const vaLayer = doc.createElementNS(ns, 'g');
    vaLayer.id = 'va_hover_layer';
    for (const p of vaPaths) {
      const cp = doc.createElementNS(ns, 'path');
      cp.setAttribute('d', p.getAttribute('d') || '');
      cp.setAttribute('data-va-id', p.getAttribute('data-va-id'));
      cp.setAttribute('style', 'fill:transparent;stroke:none');
      cp.style.pointerEvents = 'all';
      vaLayer.appendChild(cp);
    }
    // Insert immediately after ed_hover_layer so VA paths sit on top for hit detection.
    const edLayer = svgRoot.querySelector('#ed_hover_layer');
    if (edLayer && edLayer.parentNode) edLayer.parentNode.insertBefore(vaLayer, edLayer.nextSibling);
    else svgRoot.appendChild(vaLayer);
  }

  const byColor = new Map<string, string[]>();
  for (const p of paths) {
    const st = p.getAttribute('style') || '';
    const m = st.match(/fill:\s*([^;]+)/);
    const fill = m ? m[1].trim() : (p.getAttribute('fill') || '#808080');
    if (!byColor.has(fill)) byColor.set(fill, []);
    let d = p.getAttribute('d') || '';
    // Subsequent subpaths in a compound path treat a leading 'm' as relative to the
    // previous current point, not the SVG origin. Fix: make the moveto absolute (M)
    // but insert an explicit 'l' so the implicit lineto commands that follow stay
    // relative — changing 'm' to 'M' alone would flip them to absolute 'L', which
    // draws lines toward the SVG origin instead.
    if (d.charAt(0) === 'm') {
      const NUM = '[-+]?(?:\\d+\\.?\\d*|\\.\\d+)(?:[eE][-+]?\\d+)?';
      const moveRe = new RegExp('^m\\s*(' + NUM + ')[\\s,]+(' + NUM + ')\\s*');
      d = d.replace(moveRe, 'M $1 $2 l ');
    }
    if (d) byColor.get(fill)!.push(d);
  }
  while (g.firstChild) g.removeChild(g.firstChild);
  for (const [fill, ds] of byColor) {
    const cp = doc.createElementNS(ns, 'path');
    cp.setAttribute('d', ds.join(' '));
    cp.setAttribute('style', 'fill:' + fill);
    g.appendChild(cp);
  }
}

// ── activateInlineSVG ─────────────────────────────────────────────────────────

export function activateInlineSVG(ctx: MapCtx, node, preserveVB, stage, overlay, deps): void {
  mergeVaPaths(node);
  ['minority', 'majority', '2019'].forEach(function(k) { ctx.overlayInSvg[k] = null; });
  node.setAttribute('width', '100%');
  node.setAttribute('height', '100%');
  node.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  node.style.cssText = 'position:absolute;left:0;top:0;display:block;touch-action:none;';
  const _cur = (ctx.svgEl && ctx.svgEl.parentNode === stage) ? ctx.svgEl
             : (deps.obj && deps.obj.parentNode === stage)   ? deps.obj
             : null;
  if (_cur) stage.replaceChild(node, _cur);
  else stage.appendChild(node);

  const _hoverLayer = node.querySelector('#ed_hover_layer');
  if (_hoverLayer) {
    _hoverLayer.style.pointerEvents = 'all';
    _hoverLayer.querySelectorAll('path[data-ed-id]').forEach(function(p) {
      p.style.pointerEvents = 'all';
    });
  }

  const vb = node.viewBox.baseVal;
  if (vb.width && vb.height) {
    ctx.natVB = { x: vb.x, y: vb.y, w: vb.width, h: vb.height };
  } else {
    const w = parseFloat(node.getAttribute('width'))  || 432;
    const h = parseFloat(node.getAttribute('height')) || 648;
    ctx.natVB = { x: 0, y: 0, w, h };
    node.setAttribute('viewBox', `0 0 ${w} ${h}`);
  }
  ctx.curVB = { ...ctx.natVB };
  ctx.svgEl = node;
  ctx.mode = 'viewbox';
  ctx.ready = true;
  var skel = document.getElementById('zoom-skeleton'); if (skel) skel.classList.add('hidden');
  // Pre-warm the other two maps so switching is instant
  setTimeout(function() {
    ['minority', 'majority', '2019'].forEach(function(k) {
      if (!ctx.svgCache[k]) {
        fetch(deps.svgUrls[k]).then(function(r) { return r.text(); })
          .then(function(t) {
            const doc = new DOMParser().parseFromString(t, 'image/svg+xml');
            mergeVaPaths(doc.documentElement);
            ctx.svgCache[k] = doc;
          })
          .catch(function() {});
      }
    });
  }, 400);
  deps.applyBoundaryColor(node, ctx.mapPrimary);
  reapplyLayers(ctx);
  deps.applyAnomalyHighlight();
  deps.syncOverlays();
  updateStrokeWidths(ctx);
  if (overlay.style.display !== 'none') {
    if (preserveVB) {
      if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
      if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
      ctx.settledVB = null;
      ctx.curVB = { ...preserveVB };
      ctx.svgEl.style.transform = '';
      ctx.svgEl.style.willChange = '';
      ctx.svgEl.style.transformOrigin = '';
      ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
      updateZoomDisplay(ctx);
      updateStrokeWidths(ctx);
    } else {
      vpResetVB(ctx);
    }
  }
}

// ── Fallback (img-based) ──────────────────────────────────────────────────────

export function applyFallback(ctx: MapCtx): void {
  const w = Math.max(1, Math.round(ctx.fbNatW * ctx.fbScale));
  const h = Math.max(1, Math.round(ctx.fbNatH * ctx.fbScale));
  ctx.fbImg.width = w; ctx.fbImg.height = h;
  ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px';
  ctx.fbImg.style.top  = Math.round(ctx.fbTy) + 'px';
  updateZoomDisplay(ctx);
}

export function resetFallback(ctx: MapCtx, stage): void {
  const sw = stage.offsetWidth, sh = stage.offsetHeight;
  ctx.fbScale = Math.min(sw / ctx.fbNatW, sh / ctx.fbNatH) * 0.94;
  ctx.fbTx = (sw - ctx.fbNatW * ctx.fbScale) / 2;
  ctx.fbTy = (sh - ctx.fbNatH * ctx.fbScale) / 2;
  applyFallback(ctx);
}

export function initFallback(ctx: MapCtx, obj, stage, overlay): void {
  ctx.mode = 'fallback';
  const notice = document.getElementById('map-fallback-notice');
  if (notice) { notice.style.display = ''; setTimeout(() => { notice.style.display = 'none'; }, 6000); }
  ctx.fbImg = document.createElement('img');
  ctx.fbImg.src = obj.data; ctx.fbImg.alt = obj.title; ctx.fbImg.draggable = false;
  ctx.fbImg.style.cssText = 'position:absolute;display:block;user-select:none;pointer-events:none;';
  stage.replaceChild(ctx.fbImg, obj);
  function onLoad() {
    ctx.fbNatW = ctx.fbImg.naturalWidth || 600; ctx.fbNatH = ctx.fbImg.naturalHeight || 900;
    ctx.ready = true;
    if (overlay.style.display !== 'none') resetFallback(ctx, stage);
  }
  if (ctx.fbImg.complete && ctx.fbImg.naturalWidth) onLoad();
  else ctx.fbImg.onload = onLoad;
}

export function xhrFallback(ctx: MapCtx, obj, stage, overlay, deps): void {
  try {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', obj.data, true);
    xhr.onload = () => {
      if (xhr.status === 200 || xhr.status === 0) {
        const doc = new DOMParser().parseFromString(xhr.responseText, 'image/svg+xml');
        const root = doc.documentElement;
        if (root && root.tagName.toLowerCase() !== 'parsererror') {
          activateInlineSVG(ctx, document.importNode(root, true), undefined, stage, overlay, deps);
          return;
        }
      }
      initFallback(ctx, obj, stage, overlay);
    };
    xhr.onerror = () => initFallback(ctx, obj, stage, overlay);
    xhr.send();
  } catch (e) { initFallback(ctx, obj, stage, overlay); }
}

export function tryInit(ctx: MapCtx, obj, stage, overlay, deps): void {
  if (ctx.ready) return;
  const doc = obj.contentDocument || (obj.getSVGDocument && obj.getSVGDocument());
  if (doc && doc.documentElement && doc.documentElement.tagName.toLowerCase() === 'svg') {
    activateInlineSVG(ctx, doc.documentElement, undefined, stage, overlay, deps);
    return;
  }
  xhrFallback(ctx, obj, stage, overlay, deps);
}
