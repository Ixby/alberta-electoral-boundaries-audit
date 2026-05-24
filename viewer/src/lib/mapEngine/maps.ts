// @ts-nocheck
// Alberta Electoral Boundary Audit — map switcher, overlays, boundary colour
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// deps shape:
//   { svgUrls, jsonUrls, activateInlineSVG, showCallout, hideCallout,
//     setEdHighlight, activateCenterED, applyAnomalyHighlight, emit }

import type { MapCtx } from './types';
import { updateStrokeWidths } from './viewport';
import { applyEdFillLayer, reapplyLayers } from './layers';

export const MAP_ACCENT_COLORS: Record<string, string> = {
  minority: '#6B35A7',
  majority: '#1A7A6E',
  '2019':   '#7a98b4',
};

const MAP_CONTEXT_LABELS: Record<string, string> = {
  minority: '2026 minority proposal · 2023 election results',
  majority: '2026 majority proposal · 2023 election results',
  '2019':   '2019 enacted boundaries · 2023 election results',
};

// ── Boundary colour ───────────────────────────────────────────────────────────

export function applyBoundaryColor(ctx: MapCtx, svgNode, mapKey): void {
  if (!svgNode) return;
  const color = MAP_ACCENT_COLORS[mapKey] || '#555';
  const g = svgNode.querySelector('#ed_boundary_layer');
  if (!g) { console.warn('[map] ed_boundary_layer not found in SVG'); return; }
  // Hide direct-child polygon outlines — only LineCollection_1 draws each boundary once.
  Array.from(g.children).forEach(function(child) {
    if (child.tagName === 'path') child.style.display = 'none';
  });
  const lc = g.querySelector('#LineCollection_1');
  if (lc) lc.querySelectorAll('path').forEach(p => {
    p.style.stroke = color;
    p.style.strokeWidth = '0.5';
    p.style.strokeOpacity = '1';
    p.style.fill = 'none';
  });
  updateStrokeWidths(ctx);
}

// ── Overlay system ────────────────────────────────────────────────────────────

export function extractBoundaryGroup(ctx: MapCtx, key): Element | null {
  const doc = ctx.svgCache[key];
  if (!doc) return null;
  const g = doc.querySelector('#ed_boundary_layer');
  if (!g) return null;
  const clone = document.importNode(g, true);
  Array.from(clone.children).forEach(function(child) {
    if (child.tagName === 'path') child.style.display = 'none';
  });
  const zf = (ctx.natVB && ctx.curVB) ? ctx.natVB.w / ctx.curVB.w : 1;
  const primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
  const sw = Math.min(0.35, primaryW * 0.6);
  const lc = clone.querySelector('#LineCollection_1');
  if (lc) lc.querySelectorAll('path').forEach(function(p) {
    p.style.stroke = MAP_ACCENT_COLORS[key] || '#555';
    p.style.strokeWidth = String(sw);
    p.style.strokeOpacity = '0.55';
    p.style.fill = 'none';
  });
  clone.setAttribute('pointer-events', 'none');
  clone.id = 'ed-boundary-overlay-' + key;
  return clone;
}

export function fetchAndOverlay(ctx: MapCtx, key, deps): void {
  function apply() {
    if (!ctx.mapOn[key] || key === ctx.mapPrimary || !ctx.svgEl) return;
    const g = extractBoundaryGroup(ctx, key);
    if (g) { ctx.svgEl.appendChild(g); ctx.overlayInSvg[key] = g; }
  }
  if (ctx.svgCache[key]) { apply(); return; }
  fetch(deps.svgUrls[key]).then(function(r) { return r.text(); }).then(function(text) {
    ctx.svgCache[key] = new DOMParser().parseFromString(text, 'image/svg+xml');
    apply();
  }).catch(function() {});
}

export function syncOverlays(ctx: MapCtx, deps): void {
  ['minority', 'majority', '2019'].forEach(function(key) {
    if (!ctx.mapOn[key] || key === ctx.mapPrimary) {
      if (ctx.overlayInSvg[key]) { ctx.overlayInSvg[key].remove(); ctx.overlayInSvg[key] = null; }
      return;
    }
    if (!ctx.overlayInSvg[key] && ctx.svgEl) fetchAndOverlay(ctx, key, deps);
  });
}

// ── Map buttons ───────────────────────────────────────────────────────────────

export function updateMapButtons(ctx: MapCtx, deps): void {
  document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
    const key = b.dataset.map;
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

export function doSwitchPrimary(ctx: MapCtx, key, deps): void {
  const ctxEl = document.getElementById('ec-context');
  if (ctxEl) ctxEl.textContent = MAP_CONTEXT_LABELS[key];
  const savedName = ctx.selectedEdName;
  deps.hideCallout();
  ctx.edHover = null;
  const savedVB = ctx.curVB ? Object.assign({}, ctx.curVB) : null;
  const stage = document.getElementById('zoom-stage');

  function _applySvgDoc(doc) {
    const root = doc.documentElement;
    if (root && root.tagName.toLowerCase() !== 'parsererror') {
      deps.activateInlineSVG(document.importNode(root, true), savedVB);
      if (ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length) {
        ctx.edHover = ctx.allHoverData[key];
      }
      if (savedName) {
        const rec = ctx.nameIndex[key] && ctx.nameIndex[key][savedName];
        if (rec) {
          const path = ctx.svgEl && ctx.svgEl.querySelector('[data-ed-id="' + rec.id + '"]');
          if (path) { deps.showCallout(rec); deps.setEdHighlight(path); }
        } else { deps.activateCenterED(); }
      } else { deps.activateCenterED(); }
    } else { ctx.ready = true; }
    if (stage) { stage.style.opacity = ''; setTimeout(function() { stage.style.transition = ''; }, 200); }
  }

  if (ctx.svgCache[key]) {
    _applySvgDoc(ctx.svgCache[key]);
  } else {
    ctx.ready = false;
    const skelEl = document.getElementById('zoom-skeleton'); if (skelEl) skelEl.classList.remove('hidden');
    if (stage) { stage.style.opacity = '0.45'; stage.style.transition = 'opacity 0.15s'; }
    fetch(deps.svgUrls[key])
      .then(function(r) { return r.text(); })
      .then(function(text) {
        const doc = new DOMParser().parseFromString(text, 'image/svg+xml');
        ctx.svgCache[key] = doc;
        _applySvgDoc(doc);
      })
      .catch(function() {
        ctx.ready = true;
        if (stage) { stage.style.opacity = ''; setTimeout(function() { stage.style.transition = ''; }, 200); }
      });
  }
  // JSON pre-fetched at init via loadHoverJson; only fetch if not yet available
  if (!(ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length)) {
    fetch(deps.jsonUrls[key])
      .then(function(r) { return r.json(); })
      .then(function(d) {
        const byId = {}, byName = {};
        d.forEach(function(rec) { byId[rec.id] = rec; byName[rec.name] = rec; });
        ctx.allHoverData[key] = byId;
        ctx.nameIndex[key] = byName;
        ctx.edHover = byId;
        if (ctx.layerState['ed-fill']) applyEdFillLayer(ctx, true);
      })
      .catch(function() { ctx.edHover = null; });
  }
}

export function activateAsTop(ctx: MapCtx, key, deps): void {
  if (!deps.svgUrls[key]) return;
  if (ctx.mapPrimary === key) return;
  ctx.mapOn[key] = true;
  ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
  ctx.mapActivationOrder.push(key);
  ctx.mapPrimary = key;
  doSwitchPrimary(ctx, key, deps);
  updateMapButtons(ctx, deps);
}

export function toggleMap(ctx: MapCtx, key, deps): void {
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
    if (ctx.overlayInSvg[key]) { ctx.overlayInSvg[key].remove(); ctx.overlayInSvg[key] = null; }
    if (key === ctx.mapPrimary) {
      const next = ctx.mapActivationOrder.length > 0
        ? ctx.mapActivationOrder[ctx.mapActivationOrder.length - 1] : null;
      if (next) {
        ctx.mapPrimary = next;
        doSwitchPrimary(ctx, next, deps);
      } else {
        ctx.mapPrimary = null;
        if (ctx.svgEl) { ctx.svgEl.remove(); ctx.svgEl = null; }
        const skelEl = document.getElementById('zoom-skeleton');
        if (skelEl) skelEl.classList.remove('hidden');
      }
    }
  }
  updateMapButtons(ctx, deps);
  deps.emit({ type: 'map_switch', primary: ctx.mapPrimary, mapOn: { minority: ctx.mapOn.minority, majority: ctx.mapOn.majority, '2019': ctx.mapOn['2019'] } });
}

// ── Hover JSON pre-fetch ──────────────────────────────────────────────────────

export function loadHoverJson(ctx: MapCtx, key, url): void {
  fetch(url).then(r => r.json()).then(d => {
    const byId = {}, byName = {};
    d.forEach(rec => { byId[rec.id] = rec; byName[rec.name] = rec; });
    ctx.allHoverData[key] = byId;
    ctx.nameIndex[key] = byName;
    if (key === ctx.mapPrimary) { ctx.edHover = byId; reapplyLayers(ctx); }
  }).catch(() => {});
}
