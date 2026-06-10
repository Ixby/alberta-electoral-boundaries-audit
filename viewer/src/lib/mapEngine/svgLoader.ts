// Alberta Electoral Boundary Audit — SVG loader
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Two load paths (both yield an inline SVG in the main document):
//   1. Adopt from <object> contentDocument (no re-download, no re-parse).
//   2. XHR + DOMParser + importNode (when contentDocument is not yet ready).
//
// Both result in inline SVG; the browser renders vector paths at display
// resolution — no GPU tile limit at any zoom level.
//
// If both paths fail, the user sees #map-load-error. There is no bitmap
// fallback — the site is HTTP-served and same-origin, so the SVG must load.

import type { MapCtx, MapKey, ViewBox } from './types';
import { updateZoomDisplay, updateStrokeWidths, resetVB as vpResetVB } from './viewport';
import { reapplyLayers } from './layers';
import { DOM_IDS } from './domIds';
import { notifyReady } from './readyState';

export type SvgLoaderDeps = {
  obj:                   HTMLObjectElement;
  svgUrls:               Record<MapKey, string>;
  applyBoundaryColor:    (node: SVGSVGElement, key: MapKey | null) => void;
  applyAnomalyHighlight: () => void;
  syncOverlays:          () => void;
};

// ── VA path merge (perf) ──────────────────────────────────────────────────────
// Collapses 4 771 individually-stroked VA polygons in #PatchCollection_2 into
// one compound <path> per fill colour (~1 400 unique colours in the choropleth).
// Eliminates all stroke computation in that group, cutting Firefox's Skia
// SkPathStroker cost from ~2 400 ms to negligible on a typical load.
// Safe: PatchCollection_2 is purely visual; hover/click lives in #ed_hover_layer.

// Match #ffffff, #FFF, white, rgb(255,255,255), rgba(255,255,255,…).
// Matplotlib writes whichever encoding it feels like; one canonical check.
function _isWhiteFill(fill: string): boolean {
  const f = fill.toLowerCase().replace(/\s+/g, '');
  if (f === '#fff' || f === '#ffffff' || f === 'white') return true;
  if (f.startsWith('rgb(255,255,255)')) return true;
  if (f.startsWith('rgba(255,255,255,')) return true;
  return false;
}

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
    const vaLayer = doc.createElementNS(ns, 'g') as SVGGElement;
    vaLayer.id = 'va_hover_layer';
    for (const p of vaPaths) {
      const cp = doc.createElementNS(ns, 'path') as SVGPathElement;
      cp.setAttribute('d', p.getAttribute('d') || '');
      cp.setAttribute('data-va-id', p.getAttribute('data-va-id') || '');
      cp.setAttribute('style', 'fill:transparent;stroke:none');
      cp.style.pointerEvents = 'all';
      vaLayer.appendChild(cp);
    }
    const edLayer = svgRoot.querySelector('#ed_hover_layer');
    if (edLayer && edLayer.parentNode) edLayer.parentNode.insertBefore(vaLayer, edLayer.nextSibling);
    else svgRoot.appendChild(vaLayer);
  }

  const byColor = new Map<string, string[]>();
  for (const p of paths) {
    const st = p.getAttribute('style') || '';
    const m = st.match(/fill:\s*([^;]+)/);
    const fill = m ? m[1].trim() : (p.getAttribute('fill') || '#808080');
    // Skip pure-white fills entirely. These are "no data" VAs in the source
    // SVG (industrial land, water bodies, zero-eligible-voter zones) that
    // matplotlib rendered as #ffffff because no vote share applied. As fills
    // they read visually as opaque white gaps INSIDE coloured clusters —
    // sharper than any real geographic feature should look. Dropping them
    // from the merge lets the ED-level accent tint underneath show through,
    // so a "no data" zone fades into its district rather than punching a
    // hole in it.
    if (_isWhiteFill(fill)) continue;
    if (!byColor.has(fill)) byColor.set(fill, []);
    let d = p.getAttribute('d') || '';
    // Subsequent subpaths in a compound path treat a leading 'm' as relative
    // to the previous current point, not the SVG origin. Fix: make the moveto
    // absolute (M). If the original path used 'm' as the start of an implicit
    // lineto run (e.g. 'm x y X Y X Y …'), insert an explicit 'l ' so the
    // implicit linetos stay relative. If the next token is an explicit
    // command letter (e.g. 'm x y c …') do NOT insert 'l' — the previous
    // unconditional 'l ' insertion produced 'l c …' (an 'l' with no
    // coordinates), which renderers handle inconsistently and was the source
    // of the pacman / triangle-wedge artifact at high zoom.
    if (d.charAt(0) === 'm') {
      const NUM = '[-+]?(?:\\d+\\.?\\d*|\\.\\d+)(?:[eE][-+]?\\d+)?';
      const moveRe = new RegExp('^m\\s*(' + NUM + ')[\\s,]+(' + NUM + ')\\s*');
      const match = d.match(moveRe);
      if (match) {
        const tail = d.slice(match[0].length);
        const needsImplicitL = /^[-+0-9.]/.test(tail);
        d = 'M ' + match[1] + ' ' + match[2] + ' ' + (needsImplicitL ? 'l ' : '') + tail;
      }
    }
    if (d) byColor.get(fill)!.push(d);
  }
  while (g.firstChild) g.removeChild(g.firstChild);
  for (const [fill, ds] of byColor) {
    const cp = doc.createElementNS(ns, 'path');
    cp.setAttribute('d', ds.join(' '));
    cp.setAttribute('style', 'fill:' + fill);
    // evenodd defends against the other half of the pacman artifact: when
    // multiple same-colour polygons in the merged compound path have mixed
    // winding directions, the default nonzero fill rule cancels at shared
    // edges and produces visible wedges. The Alberta VAs are
    // geographically disjoint, so evenodd's "every subpath fills
    // independently" rule is the semantically correct choice.
    cp.setAttribute('fill-rule', 'evenodd');
    g.appendChild(cp);
  }
}

// ── activateInlineSVG ─────────────────────────────────────────────────────────

export function activateInlineSVG(
  ctx: MapCtx,
  node: SVGSVGElement,
  preserveVB: ViewBox | undefined,
  stage: HTMLElement,
  overlay: HTMLElement,
  deps: SvgLoaderDeps,
): void {
  mergeVaPaths(node);
  (['minority', 'majority', '2019'] as const).forEach(function(k) { ctx.overlayInSvg[k] = null; });
  node.setAttribute('width', '100%');
  node.setAttribute('height', '100%');
  node.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  node.style.cssText = 'position:absolute;left:0;top:0;display:block;touch-action:none;';
  const _cur: Element | null = (ctx.svgEl && ctx.svgEl.parentNode === stage) ? ctx.svgEl
             : (deps.obj && deps.obj.parentNode === stage)   ? deps.obj
             : null;
  if (_cur) stage.replaceChild(node, _cur);
  else stage.appendChild(node);

  const _hoverLayer = node.querySelector<SVGGElement>('#ed_hover_layer');
  if (_hoverLayer) {
    _hoverLayer.style.pointerEvents = 'all';
    _hoverLayer.querySelectorAll<SVGPathElement>('path[data-ed-id]').forEach(function(p) {
      p.style.pointerEvents = 'all';
    });
  }

  // Strip redundant clip-path attributes from every path. Matplotlib decorates
  // each of its ~7,300 output paths with `clip-path="url(#…)"` referencing a
  // single view-boundary rect — but the SVG viewBox already enforces the same
  // boundary. Firefox re-evaluates the clip-rect intersection against every
  // path on every frame even during compositor-only CSS transform updates,
  // which is the primary source of mobile/desktop Firefox drag lag on this
  // SVG (chrome / blink caches the result; Firefox does not).
  // `applyBoundaryColor` strips clip-path from LineCollection_1's paths
  // separately when the boundary colour is set; this is the bulk strip for
  // the other ~5,000 paths (PatchCollection_2 + ed_hover_layer +
  // PatchCollection_1).
  node.querySelectorAll<SVGElement>('[clip-path]').forEach(function(el) {
    el.removeAttribute('clip-path');
  });

  const vb = node.viewBox.baseVal;
  if (vb.width && vb.height) {
    ctx.natVB = { x: vb.x, y: vb.y, w: vb.width, h: vb.height };
  } else {
    const w = parseFloat(node.getAttribute('width')  || '') || 432;
    const h = parseFloat(node.getAttribute('height') || '') || 648;
    ctx.natVB = { x: 0, y: 0, w, h };
    node.setAttribute('viewBox', `0 0 ${w} ${h}`);
  }
  ctx.curVB = { ...ctx.natVB };
  ctx.svgEl = node;
  ctx.mode = 'viewbox';
  ctx.ready = true;
  notifyReady(ctx);
  const skel = document.getElementById(DOM_IDS.zoomSkeleton); if (skel) skel.classList.add('hidden');
  // Pre-warm the other two maps so switching is instant
  setTimeout(function() {
    (['minority', 'majority', '2019'] as const).forEach(function(k) {
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
  deps.applyBoundaryColor(node, ctx.mapPrimary as MapKey | null);
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

// ── XHR load (when contentDocument isn't yet available) ──────────────────────

function showLoadError(): void {
  const el = document.getElementById(DOM_IDS.mapLoadError);
  if (!el) return;
  el.style.display = '';
  el.textContent = 'Could not load the boundary map. Try reloading the page.';
}

export function xhrLoad(ctx: MapCtx, obj: HTMLObjectElement, stage: HTMLElement, overlay: HTMLElement, deps: SvgLoaderDeps): void {
  try {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', obj.data, true);
    xhr.onload = () => {
      if (xhr.status === 200 || xhr.status === 0) {
        const doc = new DOMParser().parseFromString(xhr.responseText, 'image/svg+xml');
        const root = doc.documentElement;
        if (root && root.tagName.toLowerCase() !== 'parsererror') {
          activateInlineSVG(ctx, document.importNode(root, true) as unknown as SVGSVGElement, undefined, stage, overlay, deps);
          return;
        }
      }
      showLoadError();
    };
    xhr.onerror = () => showLoadError();
    xhr.send();
  } catch (_e) {
    showLoadError();
  }
}

export function tryInit(ctx: MapCtx, obj: HTMLObjectElement, stage: HTMLElement, overlay: HTMLElement, deps: SvgLoaderDeps): void {
  if (ctx.ready) return;
  const objAny = obj as HTMLObjectElement & { getSVGDocument?: () => Document | null };
  const doc = objAny.contentDocument || (objAny.getSVGDocument && objAny.getSVGDocument());
  if (doc && doc.documentElement && doc.documentElement.tagName.toLowerCase() === 'svg') {
    activateInlineSVG(ctx, doc.documentElement as unknown as SVGSVGElement, undefined, stage, overlay, deps);
    return;
  }
  xhrLoad(ctx, obj, stage, overlay, deps);
}
