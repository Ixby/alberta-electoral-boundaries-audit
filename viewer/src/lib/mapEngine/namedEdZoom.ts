// @ts-nocheck
// Alberta Electoral Boundary Audit — named-ED zoom
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wires [data-ed-name] buttons. Each button opens the overlay (if needed) and
// flies the viewport to the named district with callout + highlight.
//
// deps for initNamedEdButtons: open, isOverlayOpen, animateToVB, getStageRect,
//                               showCallout, setEdHighlight.

import type { MapCtx } from './types';

export function zoomToEd(ctx: MapCtx, name, attempt, deps): void {
  if (!ctx.svgEl || !ctx.ready) {
    if ((attempt || 0) < 20) setTimeout(function() { zoomToEd(ctx, name, (attempt || 0) + 1, deps); }, 120);
    return;
  }
  var mapOrder = [ctx.mapPrimary, 'minority', 'majority', '2019'].filter(
    function(k, i, a) { return a.indexOf(k) === i; }
  );
  var rec = null;
  for (var i = 0; i < mapOrder.length; i++) {
    var idx = ctx.nameIndex[mapOrder[i]];
    if (idx && idx[name]) { rec = idx[name]; break; }
  }
  if (!rec) return;
  var path = ctx.svgEl.querySelector('#ed_hover_layer path[data-ed-id="' + rec.id + '"]');
  if (!path) return;
  var bb = path.getBBox();
  var pad = 1.7;
  var w = bb.width * pad, h = bb.height * pad;
  var cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
  var r = deps.getStageRect();
  if (r.width / r.height > w / h) w = h * r.width / r.height;
  else h = w * r.height / r.width;
  deps.animateToVB({ x: cx - w/2, y: cy - h/2, w: w, h: h }, 500);
  deps.showCallout(rec);
  deps.setEdHighlight(path);
}

export function initNamedEdButtons(ctx: MapCtx, deps): void {
  document.querySelectorAll('[data-ed-name]').forEach(function(b) {
    b.addEventListener('click', function() {
      if (!deps.isOverlayOpen()) deps.open();
      zoomToEd(ctx, b.getAttribute('data-ed-name'), 0, deps);
    });
  });
}
