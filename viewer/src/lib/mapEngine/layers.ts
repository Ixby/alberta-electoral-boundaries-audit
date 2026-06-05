// @ts-nocheck
// Alberta Electoral Boundary Audit — layer management
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Reads/writes: ctx.svgEl, ctx.edHover, ctx.layerState, ctx.overlayInSvg.
// No dependency on viewport, gestures, or the event bridge (_emit is a callback).

import type { MapCtx, MapEngineEventHandler, LayerKey } from './types';

export function applyVoteLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  var g = ctx.svgEl.querySelector('#PatchCollection_1');
  if (g) g.style.display = on ? '' : 'none';
}

export function applyEdFillLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl || !ctx.edHover) return;
  var g = ctx.svgEl.querySelector('#ed_hover_layer');
  if (!g) return;
  g.querySelectorAll('[data-ed-id]').forEach(function(p) {
    if (on) {
      var id = parseInt(p.getAttribute('data-ed-id'), 10);
      var rec = ctx.edHover[id];
      if (rec) {
        var isUCP = rec.ucp_pct >= rec.ndp_pct;
        var pct = Math.max(rec.ucp_pct, rec.ndp_pct);
        var a = (0.15 + Math.min((pct - 50) / 35, 1) * 0.5).toFixed(2);
        p.style.fill = isUCP ? 'rgba(20,46,148,' + a + ')' : 'rgba(232,99,16,' + a + ')';
      }
    } else { p.style.fill = 'rgba(180,180,180,0.10)'; }
  });
}

export function applyEdLinesLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  var g = ctx.svgEl.querySelector('#ed_boundary_layer');
  if (g) g.style.display = on ? '' : 'none';
  ['minority', 'majority', '2019'].forEach(function(key) {
    var og = ctx.overlayInSvg[key];
    if (og) og.style.display = on ? '' : 'none';
  });
}

export function computeEGContribs(ctx: MapCtx): Record<number, number> {
  if (!ctx.edHover) return {};
  var recs = Object.values(ctx.edHover);
  var totalVotes = recs.reduce(function(s, r) { return s + (r.votes || 0); }, 0);
  if (!totalVotes) return {};
  var contribs = {};
  recs.forEach(function(r) {
    var ucp = r.ucp_votes || 0, ndp = r.ndp_votes || 0, tot = r.votes || (ucp + ndp);
    var half = tot / 2;
    var ucpWon = ucp > ndp;
    var ucpWasted = ucpWon ? ucp - half : ucp;
    var ndpWasted = !ucpWon ? ndp - half : ndp;
    contribs[r.id] = (ucpWasted - ndpWasted) / totalVotes;
  });
  return contribs;
}

export function applyEGLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  var contribs = on ? computeEGContribs(ctx) : {};
  var vals = on ? Object.values(contribs).map(Math.abs) : [1];
  var maxVal = vals.length ? Math.max.apply(null, vals) : 1;
  ctx.svgEl.querySelectorAll('#ed_hover_layer path[data-ed-id]').forEach(function(p) {
    if (!on) { p.style.fill = 'none'; return; }
    var id = parseInt(p.getAttribute('data-ed-id'), 10);
    var v = contribs[id] || 0;
    var t = maxVal > 0 ? Math.min(Math.abs(v) / maxVal, 1) : 0;
    var alpha = (0.12 + t * 0.58).toFixed(2);
    p.style.fill = v >= 0
      ? 'rgba(20,46,148,' + alpha + ')'
      : 'rgba(232,99,16,' + alpha + ')';
  });
}

export function reapplyLayers(ctx: MapCtx): void {
  applyVoteLayer(ctx, ctx.layerState.vote);
  applyEdFillLayer(ctx, ctx.layerState['ed-fill']);
  applyEdLinesLayer(ctx, ctx.layerState['ed-lines']);
  if (ctx.layerState.eg) applyEGLayer(ctx, true);
}

export function setLayerOn(ctx: MapCtx, key: LayerKey, on: boolean, emit: MapEngineEventHandler): void {
  if (ctx.layerState[key] === on) return;
  ctx.layerState[key] = on;
  document.querySelectorAll('.tb-btn[data-layer="' + key + '"]').forEach(function(btn) {
    btn.classList.toggle('tb-layer-on', on);
  });
  if (key === 'vote')     applyVoteLayer(ctx, on);
  if (key === 'ed-fill')  applyEdFillLayer(ctx, on);
  if (key === 'ed-lines') applyEdLinesLayer(ctx, on);
  if (key === 'eg')       applyEGLayer(ctx, on);
  emit({ type: 'layer', key: key, on: on });
}
