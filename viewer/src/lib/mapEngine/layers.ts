// Alberta Electoral Boundary Audit — layer management
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Reads/writes: ctx.svgEl, ctx.edHover, ctx.layerState, ctx.overlayInSvg.
// No dependency on viewport, gestures, or the event bridge (_emit is a callback).

import type { MapCtx, MapEngineEventHandler, LayerKey, MapKey } from './types';

type EdHoverRec = { id: number; ucp_pct: number; ndp_pct: number; ucp_votes?: number; ndp_votes?: number; votes?: number };

export function applyVoteLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  const g = ctx.svgEl.querySelector<SVGGElement>('#PatchCollection_1');
  if (g) g.style.display = on ? '' : 'none';
}

export function applyEdFillLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl || !ctx.edHover) return;
  const edHover = ctx.edHover;
  const g = ctx.svgEl.querySelector('#ed_hover_layer');
  if (!g) return;
  g.querySelectorAll<SVGPathElement>('[data-ed-id]').forEach(function(p) {
    if (on) {
      const id = parseInt(p.getAttribute('data-ed-id') || '0', 10);
      const rec = edHover[id] as EdHoverRec | undefined;
      if (rec) {
        const isUCP = rec.ucp_pct >= rec.ndp_pct;
        const pct = Math.max(rec.ucp_pct, rec.ndp_pct);
        const a = (0.15 + Math.min((pct - 50) / 35, 1) * 0.5).toFixed(2);
        p.style.fill = isUCP ? 'rgba(20,46,148,' + a + ')' : 'rgba(232,99,16,' + a + ')';
      }
    } else { p.style.fill = 'rgba(180,180,180,0.10)'; }
  });
}

export function applyEdLinesLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  const g = ctx.svgEl.querySelector<SVGGElement>('#ed_boundary_layer');
  if (g) g.style.display = on ? '' : 'none';
  (['minority', 'majority', '2019'] as const).forEach(function(key) {
    const og = ctx.overlayInSvg[key] as SVGGElement | null;
    if (og) og.style.display = on ? '' : 'none';
  });
}

export function computeEGContribs(ctx: MapCtx): Record<number, number> {
  if (!ctx.edHover) return {};
  const recs = Object.values(ctx.edHover) as EdHoverRec[];
  const totalVotes = recs.reduce(function(s, r) { return s + (r.votes || 0); }, 0);
  if (!totalVotes) return {};
  const contribs: Record<number, number> = {};
  recs.forEach(function(r) {
    const ucp = r.ucp_votes || 0, ndp = r.ndp_votes || 0, tot = r.votes || (ucp + ndp);
    const half = tot / 2;
    const ucpWon = ucp > ndp;
    const ucpWasted = ucpWon ? ucp - half : ucp;
    const ndpWasted = !ucpWon ? ndp - half : ndp;
    contribs[r.id] = (ucpWasted - ndpWasted) / totalVotes;
  });
  return contribs;
}

export function applyEGLayer(ctx: MapCtx, on: boolean): void {
  if (!ctx.svgEl) return;
  const contribs = on ? computeEGContribs(ctx) : {};
  const vals = on ? Object.values(contribs).map(Math.abs) : [1];
  const maxVal = vals.length ? Math.max.apply(null, vals) : 1;
  ctx.svgEl.querySelectorAll<SVGPathElement>('#ed_hover_layer path[data-ed-id]').forEach(function(p) {
    if (!on) { p.style.fill = 'none'; return; }
    const id = parseInt(p.getAttribute('data-ed-id') || '0', 10);
    const v = contribs[id] || 0;
    const t = maxVal > 0 ? Math.min(Math.abs(v) / maxVal, 1) : 0;
    const alpha = (0.12 + t * 0.58).toFixed(2);
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
