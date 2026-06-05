// Alberta Electoral Boundary Audit — named-ED zoom
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wires [data-ed-name] buttons. Each button opens the overlay (if needed) and
// flies the viewport to the named district with callout + highlight.

import type { MapCtx, ViewBox } from './types';

type NamedEdDeps = {
  open: () => void;
  isOverlayOpen: () => boolean;
  animateToVB: (vb: ViewBox, dur: number) => void;
  getStageRect: () => DOMRect;
  showCallout: (rec: any) => void;
  setEdHighlight: (pathEl: SVGGraphicsElement) => void;
};

export function zoomToEd(ctx: MapCtx, name: string, attempt: number, deps: NamedEdDeps): void {
  if (!ctx.svgEl || !ctx.ready) {
    if ((attempt || 0) < 20) setTimeout(function() { zoomToEd(ctx, name, (attempt || 0) + 1, deps); }, 120);
    return;
  }
  const mapOrder = [ctx.mapPrimary, 'minority', 'majority', '2019'].filter(
    function(k, i, a) { return k !== null && a.indexOf(k) === i; }
  );
  let rec: any = null;
  for (const key of mapOrder) {
    if (!key) continue;
    const idx = ctx.nameIndex[key];
    if (idx && idx[name]) { rec = idx[name]; break; }
  }
  if (!rec) return;
  const path = ctx.svgEl.querySelector<SVGGraphicsElement>('#ed_hover_layer path[data-ed-id="' + rec.id + '"]');
  if (!path) return;
  const bb = path.getBBox();
  const pad = 1.7;
  let w = bb.width * pad, h = bb.height * pad;
  const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
  const r = deps.getStageRect();
  if (r.width / r.height > w / h) w = h * r.width / r.height;
  else h = w * r.height / r.width;
  deps.animateToVB({ x: cx - w/2, y: cy - h/2, w: w, h: h }, 500);
  deps.showCallout(rec);
  deps.setEdHighlight(path);
}

export function initNamedEdButtons(ctx: MapCtx, deps: NamedEdDeps): void {
  document.querySelectorAll<HTMLElement>('[data-ed-name]').forEach(function(b) {
    b.addEventListener('click', function() {
      if (!deps.isOverlayOpen()) deps.open();
      const name = b.getAttribute('data-ed-name');
      if (name) zoomToEd(ctx, name, 0, deps);
    });
  });
}
