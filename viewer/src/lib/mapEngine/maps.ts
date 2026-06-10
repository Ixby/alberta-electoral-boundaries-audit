// Alberta Electoral Boundary Audit — map switcher, overlays, boundary colour
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

import type { MapCtx, MapEngineEventHandler, MapKey, ViewBox } from './types';
import { updateStrokeWidths } from './viewport';
import { applyEdFillLayer, reapplyLayers } from './layers';
import { mergeVaPaths } from './svgLoader';
import { showVaCallout } from './edInteraction';
import { DOM_IDS } from './domIds';
import { notifyReady } from './readyState';
import { MAP_ACCENT_COLORS as ACCENT_COLORS } from './constants';
export { MAP_ACCENT_COLORS } from './constants';

type MapsDeps = {
  svgUrls:              Record<MapKey, string>;
  jsonUrls:             Record<MapKey, string>;
  activateInlineSVG:    (node: SVGSVGElement, preserveVB: ViewBox | null | undefined) => void;
  showCallout:          (rec: any) => void;
  hideCallout:          () => void;
  setEdHighlight:       (pathEl: SVGGraphicsElement) => void;
  activateCenterED:     () => void;
  applyAnomalyHighlight:() => void;
  emit:                 MapEngineEventHandler;
};

const MAP_CONTEXT_LABELS: Record<MapKey, string> = {
  minority: '2026 minority proposal · 2023 election results',
  majority: '2026 majority proposal · 2023 election results',
  '2019':   '2019 enacted boundaries · 2023 election results',
};

// ── Boundary colour ───────────────────────────────────────────────────────────

export function applyBoundaryColor(ctx: MapCtx, svgNode: Element | null, mapKey: MapKey | null): void {
  if (!svgNode || !mapKey) return;
  const color = ACCENT_COLORS[mapKey] || '#555';
  const g = svgNode.querySelector('#ed_boundary_layer');
  if (!g) { console.warn('[map] ed_boundary_layer not found in SVG'); return; }
  // Hide direct-child polygon outlines — only LineCollection_1 draws each boundary once.
  Array.from(g.children).forEach(function(child) {
    if (child.tagName === 'path') (child as SVGPathElement).style.display = 'none';
  });
  const lc = svgNode.querySelector('#LineCollection_1');
  if (lc) {
    // LineCollection_1 may itself be a <path> (not a container <g>)
    const targets: SVGPathElement[] = lc.tagName.toLowerCase() === 'path'
      ? [lc as unknown as SVGPathElement]
      : Array.from(lc.querySelectorAll<SVGPathElement>('path'));
    targets.forEach(function(p) {
      p.removeAttribute('clip-path');
      p.style.stroke = color;
      p.style.strokeWidth = '0.5';
      p.style.strokeOpacity = '1';
      p.style.fill = 'none';
    });
  }
  updateStrokeWidths(ctx);
}

// ── Overlay system ────────────────────────────────────────────────────────────

export function extractBoundaryGroup(ctx: MapCtx, key: MapKey): Element | null {
  const doc = ctx.svgCache[key];
  if (!doc) return null;
  const lc = doc.querySelector('#LineCollection_1');
  if (!lc) return null;
  const clone = document.importNode(lc, true);
  const zf = (ctx.natVB && ctx.curVB) ? ctx.natVB.w / ctx.curVB.w : 1;
  const primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
  const sw = primaryW * 0.7; // proportional to primary; no absolute cap so default-zoom overlays stay above sub-pixel
  // Force _lastStrokeW recompute so the new overlay actually receives a stroke update from updateStrokeWidths
  ctx._lastStrokeW = undefined;
  // LineCollection_1 may itself be a <path> (not a container <g>)
  const targets: SVGPathElement[] = clone.tagName.toLowerCase() === 'path'
    ? [clone as unknown as SVGPathElement]
    : Array.from(clone.querySelectorAll<SVGPathElement>('path'));
  targets.forEach(function(p) {
    p.removeAttribute('clip-path');
    p.style.stroke = ACCENT_COLORS[key] || '#555';
    p.style.strokeWidth = String(sw);
    p.style.strokeOpacity = '0.55';
    p.style.fill = 'none';
  });
  clone.setAttribute('pointer-events', 'none');
  clone.id = 'ed-boundary-overlay-' + key;
  return clone;
}

export function fetchAndOverlay(ctx: MapCtx, key: MapKey, deps: MapsDeps): void {
  function apply() {
    if (!ctx.mapOn[key] || key === ctx.mapPrimary || !ctx.svgEl) return;
    const g = extractBoundaryGroup(ctx, key);
    if (g) {
      ctx.svgEl.appendChild(g);
      ctx.overlayInSvg[key] = g;
      updateStrokeWidths(ctx); // ensure overlay paths get correct stroke width now (cache was just invalidated)
    }
  }
  if (ctx.svgCache[key]) { apply(); return; }
  fetch(deps.svgUrls[key]).then(function(r) { return r.text(); }).then(function(text) {
    const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
    mergeVaPaths(doc.documentElement);
    ctx.svgCache[key] = doc;
    apply();
  }).catch(function() {});
}

export function syncOverlays(ctx: MapCtx, deps: MapsDeps): void {
  (['minority', 'majority', '2019'] as const).forEach(function(key) {
    if (!ctx.mapOn[key] || key === ctx.mapPrimary) {
      const existing = ctx.overlayInSvg[key];
      if (existing) { (existing as Element).remove(); ctx.overlayInSvg[key] = null; }
      return;
    }
    if (!ctx.overlayInSvg[key] && ctx.svgEl) fetchAndOverlay(ctx, key, deps);
  });
}

// ── Map buttons ───────────────────────────────────────────────────────────────

export function updateMapButtons(ctx: MapCtx, deps: MapsDeps): void {
  document.querySelectorAll<HTMLElement>('.tb-btn[data-map]').forEach(function(b) {
    const key = b.dataset.map as MapKey | undefined;
    if (!key) return;
    b.classList.toggle('tb-map-primary', !!ctx.mapPrimary && ctx.mapOn[key] && key === ctx.mapPrimary);
    b.classList.toggle('tb-map-overlay',  !!ctx.mapPrimary && ctx.mapOn[key] && key !== ctx.mapPrimary);
  });
  // Clear anomaly state when minority is no longer the top layer
  if (ctx.mapPrimary !== 'minority' && ctx.anomalyOn) {
    ctx.anomalyOn = false;
    document.querySelectorAll('[data-anomaly]').forEach(function(b) { b.classList.remove('tb-layer-on'); });
    if (ctx.svgEl) deps.applyAnomalyHighlight();
  }
}

// ── Primary map switching ─────────────────────────────────────────────────────

export function doSwitchPrimary(ctx: MapCtx, key: MapKey, deps: MapsDeps): void {
  const ctxEl = document.getElementById(DOM_IDS.ecContext);
  if (ctxEl) ctxEl.textContent = MAP_CONTEXT_LABELS[key];
  const savedName = ctx.selectedEdName;
  const savedVaId = ctx.selectedVaId;
  deps.hideCallout();
  ctx.edHover = null;
  const savedVB: ViewBox | null = ctx.curVB ? Object.assign({} as ViewBox, ctx.curVB) : null;
  const stage = document.getElementById(DOM_IDS.zoomStage);

  function _applySvgDoc(doc: Document) {
    const root = doc.documentElement;
    if (root && root.tagName.toLowerCase() !== 'parsererror') {
      deps.activateInlineSVG(document.importNode(root, true) as unknown as SVGSVGElement, savedVB);
      if (ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length) {
        ctx.edHover = ctx.allHoverData[key];
      }
      // VA is the focal point when selected; fall back to ED name
      const vaForMap = ctx.allVaData[key];
      const vaRec = savedVaId && vaForMap ? vaForMap[savedVaId] : null;
      const focalName: string | null = vaRec ? vaRec.ed_name : savedName;
      if (focalName) {
        const nameIdx = ctx.nameIndex[key];
        const rec = nameIdx && nameIdx[focalName];
        if (rec) {
          const path = ctx.svgEl && ctx.svgEl.querySelector<SVGGraphicsElement>('[data-ed-id="' + rec.id + '"]');
          if (path) {
            deps.showCallout(rec);
            deps.setEdHighlight(path);
            if (vaRec) showVaCallout(ctx, vaRec);
          }
        } else { deps.activateCenterED(); }
      } else { deps.activateCenterED(); }
    } else { ctx.ready = true; notifyReady(ctx); }
    if (stage) { stage.style.opacity = ''; setTimeout(function() { stage.style.transition = ''; }, 200); }
  }

  if (ctx.svgCache[key]) {
    _applySvgDoc(ctx.svgCache[key]);
  } else {
    ctx.ready = false;
    const skelEl = document.getElementById(DOM_IDS.zoomSkeleton); if (skelEl) skelEl.classList.remove('hidden');
    if (stage) { stage.style.opacity = '0.45'; stage.style.transition = 'opacity 0.15s'; }
    fetch(deps.svgUrls[key])
      .then(function(r) { return r.text(); })
      .then(function(text) {
        const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
        mergeVaPaths(doc.documentElement);
        ctx.svgCache[key] = doc;
        _applySvgDoc(doc);
      })
      .catch(function() {
        ctx.ready = true;
        notifyReady(ctx);
        if (stage) { stage.style.opacity = ''; setTimeout(function() { stage.style.transition = ''; }, 200); }
        const errEl = document.getElementById(DOM_IDS.mapLoadError);
        if (errEl) {
          errEl.textContent = 'Could not load the ' + key + ' map — check your connection.';
          errEl.style.display = '';
          setTimeout(function() { errEl.style.display = 'none'; }, 5000);
        }
      });
  }
  // JSON pre-fetched at init via loadHoverJson; only fetch if not yet available
  if (!(ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length)) {
    fetch(deps.jsonUrls[key])
      .then(function(r) { return r.json(); })
      .then(function(d: any[]) {
        const byId: Record<number, any> = {};
        const byName: Record<string, any> = {};
        d.forEach(function(rec) { byId[rec.id] = rec; byName[rec.name] = rec; });
        ctx.allHoverData[key] = byId;
        ctx.nameIndex[key] = byName;
        ctx.edHover = byId;
        if (ctx.layerState['ed-fill']) applyEdFillLayer(ctx, true);
      })
      .catch(function() { ctx.edHover = null; });
  }
}

export function activateAsTop(ctx: MapCtx, key: MapKey, deps: MapsDeps): void {
  if (!deps.svgUrls[key]) return;
  if (ctx.mapPrimary === key) return;
  ctx.mapOn[key] = true;
  ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
  ctx.mapActivationOrder.push(key);
  ctx.mapPrimary = key;
  doSwitchPrimary(ctx, key, deps);
  updateMapButtons(ctx, deps);
}

export function toggleMap(ctx: MapCtx, key: MapKey, deps: MapsDeps): void {
  if (!deps.svgUrls[key]) return;
  if (!ctx.mapOn[key]) {
    // Toggle ON — becomes the new top layer
    ctx.mapOn[key] = true;
    ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
    ctx.mapActivationOrder.push(key);
    ctx.mapPrimary = key;
    doSwitchPrimary(ctx, key, deps);
  } else {
    // Toggle OFF
    ctx.mapOn[key] = false;
    ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
    const existing = ctx.overlayInSvg[key];
    if (existing) { (existing as Element).remove(); ctx.overlayInSvg[key] = null; }
    if (key === ctx.mapPrimary) {
      const next: MapKey | null = ctx.mapActivationOrder.length > 0
        ? (ctx.mapActivationOrder[ctx.mapActivationOrder.length - 1] as MapKey) : null;
      if (next) {
        ctx.mapPrimary = next;
        doSwitchPrimary(ctx, next, deps);
      } else {
        ctx.mapPrimary = null;
        if (ctx.svgEl) { ctx.svgEl.remove(); ctx.svgEl = null; }
        const skelEl = document.getElementById(DOM_IDS.zoomSkeleton);
        if (skelEl) skelEl.classList.remove('hidden');
      }
    }
  }
  updateMapButtons(ctx, deps);
  if (ctx.mapPrimary) {
    deps.emit({
      type: 'map_switch',
      primary: ctx.mapPrimary,
      mapOn: { minority: ctx.mapOn.minority, majority: ctx.mapOn.majority, '2019': ctx.mapOn['2019'] },
    });
  }
}

// ── Hover JSON pre-fetch ──────────────────────────────────────────────────────

export function loadHoverJson(ctx: MapCtx, key: MapKey, url: string): void {
  fetch(url).then(r => r.json()).then((d: any[]) => {
    const byId: Record<number, any> = {};
    const byName: Record<string, any> = {};
    d.forEach(rec => { byId[rec.id] = rec; byName[rec.name] = rec; });
    ctx.allHoverData[key] = byId;
    ctx.nameIndex[key] = byName;
    if (key === ctx.mapPrimary) { ctx.edHover = byId; reapplyLayers(ctx); }
  }).catch(() => {});
}

export function loadVaJson(ctx: MapCtx, key: MapKey, url: string): void {
  fetch(url).then(r => r.json()).then((d: any[]) => {
    const byId: Record<string, any> = {};
    d.forEach(rec => { byId[String(rec.va_id)] = rec; });
    ctx.allVaData[key] = byId;
  }).catch(() => {});
}
