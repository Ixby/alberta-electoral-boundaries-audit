// @ts-nocheck
// Alberta Electoral Boundary Audit — anomaly highlight
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// All 7 configurations criticized by commission chair (Justice Miller):
//   Geometric flags (4): 13=Foothills-Airdrie West, 20=Nolan Hill-Cochrane,
//                        75=Olds-Three Hills-Didsbury, 81=RMH-Banff Park
//   Appendix C (no public support): 57=Chestermere-Strathmore,
//                        80=Red Deer-Sylvan Lake, 83=St Albert
// Source: AEBC (2026) majority report §5.8.2 + Appendix C; union = 7 configs.
//
// deps for initAnomalyButtons: activateAsTop, open, emit.

import type { MapCtx } from './types';
import { setLayerOn } from './layers';

const ANOMALY_IDS = new Set([13, 20, 57, 75, 80, 81, 83]);

export function applyAnomalyHighlight(ctx: MapCtx): void {
  if (!ctx.svgEl) return;
  if (ctx.anomalyOverlay) { ctx.anomalyOverlay.remove(); ctx.anomalyOverlay = null; }
  ctx.svgEl.querySelectorAll('#ed_hover_layer path[data-ed-id]').forEach(p => { p.style.fill = 'none'; });
  if (!ctx.anomalyOn) return;

  const NS = 'http://www.w3.org/2000/svg';
  ctx.anomalyOverlay = document.createElementNS(NS, 'g');
  ctx.anomalyOverlay.setAttribute('id', 'anomaly-overlay');
  ctx.anomalyOverlay.setAttribute('pointer-events', 'none');

  ctx.svgEl.querySelectorAll('#ed_hover_layer path[data-ed-id]').forEach(function(p) {
    const id = parseInt(p.getAttribute('data-ed-id'), 10);
    if (!ANOMALY_IDS.has(id)) return;
    const d = p.getAttribute('d');

    const glow = document.createElementNS(NS, 'path');
    glow.setAttribute('d', d);
    glow.setAttribute('fill', 'none');
    glow.setAttribute('stroke', '#e63946');
    glow.setAttribute('stroke-width', '12');
    glow.setAttribute('stroke-linejoin', 'round');
    glow.style.vectorEffect = 'non-scaling-stroke';
    glow.setAttribute('class', 'anomaly-glow-path');
    ctx.anomalyOverlay.appendChild(glow);

    const outline = document.createElementNS(NS, 'path');
    outline.setAttribute('d', d);
    outline.setAttribute('fill', 'none');
    outline.setAttribute('stroke', '#e63946');
    outline.setAttribute('stroke-width', '3');
    outline.setAttribute('stroke-linejoin', 'round');
    outline.style.vectorEffect = 'non-scaling-stroke';
    outline.setAttribute('class', 'anomaly-pulse-path');
    ctx.anomalyOverlay.appendChild(outline);
  });

  ctx.svgEl.appendChild(ctx.anomalyOverlay);
}

export function zoomToAnomalyDistricts(ctx: MapCtx, attempt: number, animateToVB, getStageRect): void {
  if (!ctx.svgEl || !ctx.ready) {
    if ((attempt || 0) < 25) setTimeout(function() { zoomToAnomalyDistricts(ctx, (attempt || 0) + 1, animateToVB, getStageRect); }, 120);
    return;
  }
  var combined = null;
  ctx.svgEl.querySelectorAll('#ed_hover_layer path[data-ed-id]').forEach(function(p) {
    if (!ANOMALY_IDS.has(parseInt(p.getAttribute('data-ed-id'), 10))) return;
    var bb = p.getBBox();
    if (!combined) combined = { x: bb.x, y: bb.y, r: bb.x + bb.width, b: bb.y + bb.height };
    else {
      combined.x = Math.min(combined.x, bb.x);
      combined.y = Math.min(combined.y, bb.y);
      combined.r = Math.max(combined.r, bb.x + bb.width);
      combined.b = Math.max(combined.b, bb.y + bb.height);
    }
  });
  if (!combined) return;
  var w = (combined.r - combined.x) * 1.40, h = (combined.b - combined.y) * 1.40;
  var cx = (combined.x + combined.r) / 2, cy = (combined.y + combined.b) / 2;
  var r = getStageRect();
  if (r.width / r.height > w / h) w = h * r.width / r.height;
  else h = w * r.height / r.width;
  animateToVB({ x: cx - w/2, y: cy - h/2, w: w, h: h }, 500);
}

export function initAnomalyButtons(ctx: MapCtx, deps): void {
  const { activateAsTop, open, emit } = deps;
  document.querySelectorAll('[data-anomaly]').forEach(function(b) {
    b.addEventListener('click', function() {
      activateAsTop('minority');
      var wasOff = !ctx.anomalyOn;
      if (!deps.isOverlayOpen()) open();
      ctx.anomalyOn = !ctx.anomalyOn;
      b.classList.toggle('tb-layer-on', ctx.anomalyOn);
      applyAnomalyHighlight(ctx);
      if (ctx.anomalyOn && wasOff) {
        if (!ctx.layerState['eg'])     setLayerOn(ctx, 'eg', true, emit);
        if (ctx.layerState['ed-fill']) setLayerOn(ctx, 'ed-fill', false, emit);
        if (!ctx.mapLocked) zoomToAnomalyDistricts(ctx, 0, deps.animateToVB, deps.getStageRect);
      }
    });
  });
}
