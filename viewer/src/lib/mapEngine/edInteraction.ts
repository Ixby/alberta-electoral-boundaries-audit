// Alberta Electoral Boundary Audit — ED interaction
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Tooltip, callout, ED highlight, snap-to-ED, zoom-to-ED.
// animateToVB and getStageRect are passed as callbacks to avoid circular deps with viewport.

import type { MapCtx, MapEngineEventHandler, MapKey, ViewBox } from './types';
import { DOM_IDS } from './domIds';
import { STR } from './strings';

const _fmt = new Intl.NumberFormat();

type EdRec = {
  id: number;
  name: string;
  ucp_pct: number;
  ndp_pct: number;
  ucp_votes?: number;
  ndp_votes?: number;
  votes?: number;
  pop?: number;
  va_count?: number;
  eg?: number | null;
};

type VaRec = {
  va_id?: string | number;
  poll_name?: string;
  ucp_pct?: number;
  ndp_pct?: number;
  in_person_votes?: number;
  ed_name?: string;
};

type BBox = { x: number; y: number; width: number; height: number };

// ── Tooltip ───────────────────────────────────────────────────────────────────

export function showTip(d: EdRec | undefined, x: number, y: number): void {
  if (!d) return;
  const tip = document.getElementById(DOM_IDS.edTooltip);
  if (!tip) return;
  tip.innerHTML =
    `<strong>${d.name}</strong>` +
    `UCP&nbsp;${d.ucp_pct}%&nbsp;&nbsp;NDP&nbsp;${d.ndp_pct}%` +
    (d.votes ? `<br>${_fmt.format(d.votes)}&nbsp;votes&nbsp;(2023)` : '') +
    (d.pop   ? `<br>Pop.&nbsp;${_fmt.format(d.pop)}` : '');
  const pad = 14, tw = 200, th = 60; // fixed estimates — avoids synchronous layout read on pointermove
  const rtl = typeof document !== 'undefined' && document.documentElement.dir === 'rtl';
  let lx = rtl ? x - tw - pad : x + pad;
  let ly = y + pad;
  if (!rtl && lx + tw > window.innerWidth) lx = x - tw - pad;   // LTR: flip left on right overflow
  if (rtl && lx < 0) lx = x + pad;                              // RTL: flip right on left overflow
  if (ly + th > window.innerHeight) ly = y - th - pad;
  tip.style.cssText = `display:block;left:${lx}px;top:${ly}px`;
}

export function hideTip(): void {
  const tip = document.getElementById(DOM_IDS.edTooltip);
  if (tip) tip.style.display = 'none';
}

// ── Callout ───────────────────────────────────────────────────────────────────

function _setText(id: string, text: string): void {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}
function _setWidth(id: string, pct: number | string): void {
  const el = document.getElementById(id) as HTMLElement | null;
  if (el) el.style.width = pct + '%';
}

export function showCallout(ctx: MapCtx, d: EdRec | undefined): void {
  if (!d) return;
  _setText(DOM_IDS.ecName, d.name);
  _setWidth(DOM_IDS.ecUcpBar, d.ucp_pct);
  _setWidth(DOM_IDS.ecNdpBar, d.ndp_pct);
  _setText(DOM_IDS.ecUcpPct, d.ucp_pct + '%');
  _setText(DOM_IDS.ecNdpPct, d.ndp_pct + '%');
  _setText(DOM_IDS.ecUcpVotes, d.ucp_votes ? _fmt.format(d.ucp_votes) + ' ' + STR.votesSuffix : '');
  _setText(DOM_IDS.ecNdpVotes, d.ndp_votes ? _fmt.format(d.ndp_votes) + ' ' + STR.votesSuffix : '');
  _setText(DOM_IDS.ecTotalVotes, d.votes ? _fmt.format(d.votes) + ' ' + STR.totalVotesSuffix : '');
  const vaEl = document.getElementById(DOM_IDS.ecVaCount);
  if (vaEl) vaEl.textContent = d.va_count ? d.va_count + ' ' + STR.votingAreasSuffix : '';
  const popN = d.pop ? Math.round(d.pop / 100) * 100 : 0;
  _setText(DOM_IDS.ecPop, popN ? STR.popPrefix + ' ' + _fmt.format(popN) : '');

  const egEl = document.getElementById(DOM_IDS.ecEg);
  if (egEl) {
    if (d.eg !== undefined && d.eg !== null) {
      const sign = d.eg >= 0 ? '+' : '';
      egEl.textContent = sign + (d.eg * 100).toFixed(2) + '%';
      egEl.className = d.eg >= 0 ? 'ec-eg-ucp' : 'ec-eg-ndp';
    } else {
      egEl.textContent = ''; egEl.className = '';
    }
  }

  const ctxEl = document.getElementById(DOM_IDS.ecContext);
  if (ctxEl) {
    ctxEl.textContent = ctx.mapPrimary === 'minority' ? STR.contextMinority
                      : ctx.mapPrimary === 'majority' ? STR.contextMajority
                      : STR.context2019;
  }

  const cmpEl = document.getElementById(DOM_IDS.ecCompare);
  if (cmpEl) {
    const others = (['minority', 'majority', '2019'] as const).filter(k => k !== ctx.mapPrimary);
    const parts = others.map(function(k) {
      const idx = ctx.nameIndex[k];
      const rec = idx && idx[d.name] as EdRec | undefined;
      if (!rec) return null;
      const label = k === 'minority' ? STR.tagMin + '.' : k === 'majority' ? STR.tagMaj + '.' : STR.tag2019;
      const ucpFirst = rec.ucp_pct >= rec.ndp_pct;
      const winner = ucpFirst
        ? '<span class="ec-cmp-val ec-cmp-ucp">UCP ' + rec.ucp_pct + '%</span>'
        : '<span class="ec-cmp-val ec-cmp-ndp">NDP ' + rec.ndp_pct + '%</span>';
      const loser = ucpFirst
        ? '<span class="ec-cmp-second">NDP ' + rec.ndp_pct + '%</span>'
        : '<span class="ec-cmp-second">UCP ' + rec.ucp_pct + '%</span>';
      return '<span class="ec-cmp-item"><span class="ec-cmp-label">' + label + '</span>' + winner + '<span class="ec-cmp-sep">/</span>' + loser + '</span>';
    }).filter((s): s is string => s !== null);
    if (parts.length) {
      cmpEl.innerHTML = '<span class="ec-cmp-header">' + STR.otherMaps + '</span>' + parts.join('');
      cmpEl.style.display = 'flex';
    } else {
      cmpEl.innerHTML = '<span class="ec-cmp-unique">' + STR.uniqueBoundary + '</span>';
      cmpEl.style.display = 'flex';
    }
  }

  ctx.selectedEdName = d.name;
  const srEl = document.getElementById(DOM_IDS.srAnnounce);
  if (srEl) srEl.textContent = d.name + ' — UCP ' + d.ucp_pct + '%, NDP ' + d.ndp_pct + '%';
  const vaHint = document.getElementById(DOM_IDS.ecVaHint);
  if (vaHint) {
    const vaForMap = ctx.mapPrimary ? ctx.allVaData[ctx.mapPrimary] : null;
    vaHint.style.display = (vaForMap && Object.keys(vaForMap).length) ? '' : 'none';
  }
  const callout = document.getElementById(DOM_IDS.edCallout);
  const hud     = document.getElementById(DOM_IDS.hud);
  if (callout) callout.classList.add('ec-visible');
  if (hud) hud.classList.add('ec-has-ed');
}

export function hideCallout(ctx: MapCtx): void {
  const callout = document.getElementById(DOM_IDS.edCallout);
  const hud     = document.getElementById(DOM_IDS.hud);
  if (callout) callout.classList.remove('ec-visible');
  if (hud) hud.classList.remove('ec-has-ed');
  ctx.selectedEdName = null;
  clearEdHighlight(ctx);
  const srEl = document.getElementById(DOM_IDS.srAnnounce);
  if (srEl) srEl.textContent = '';
  const vaHint = document.getElementById(DOM_IDS.ecVaHint);
  if (vaHint) vaHint.style.display = 'none';
}

// ── ED highlight ──────────────────────────────────────────────────────────────

export function setEdHighlight(ctx: MapCtx, pathEl: SVGGraphicsElement | null): void {
  clearEdHighlight(ctx);
  if (!ctx.svgEl || !pathEl) return;
  const d = pathEl.getAttribute('d') || '';
  const NS = 'http://www.w3.org/2000/svg';
  const hp = document.createElementNS(NS, 'g');
  hp.setAttribute('pointer-events', 'none');
  const glow = document.createElementNS(NS, 'path');
  glow.setAttribute('d', d);
  glow.setAttribute('fill', 'none');
  glow.setAttribute('stroke', 'rgba(255,255,255,0.25)');
  glow.setAttribute('stroke-width', '6');
  glow.setAttribute('stroke-linejoin', 'round');
  (glow as SVGPathElement).style.vectorEffect = 'non-scaling-stroke';
  (glow as SVGPathElement).style.filter = 'blur(2px)';
  const sharp = document.createElementNS(NS, 'path');
  sharp.setAttribute('d', d);
  sharp.setAttribute('fill', 'none');
  sharp.setAttribute('stroke', '#ffffff');
  sharp.setAttribute('stroke-width', '2.5');
  sharp.setAttribute('stroke-linejoin', 'round');
  (sharp as SVGPathElement).style.vectorEffect = 'non-scaling-stroke';
  hp.appendChild(glow);
  hp.appendChild(sharp);
  ctx.svgEl.appendChild(hp);
  ctx.highlightPath = hp as unknown as SVGGElement;
}

export function clearEdHighlight(ctx: MapCtx): void {
  if (ctx.highlightPath) { ctx.highlightPath.remove(); ctx.highlightPath = null; }
}

// ── Hit-testing ───────────────────────────────────────────────────────────────

export function tipTarget(e: { clientX: number; clientY: number }): Element | null {
  const els = document.elementsFromPoint
    ? document.elementsFromPoint(e.clientX, e.clientY)
    : ([document.elementFromPoint(e.clientX, e.clientY)].filter(Boolean) as Element[]);
  for (let i = 0; i < els.length; i++) {
    if (els[i] && els[i].hasAttribute && els[i].hasAttribute('data-ed-id')) return els[i];
  }
  return null;
}

export function vaTarget(e: { clientX: number; clientY: number }): Element | null {
  const els = document.elementsFromPoint
    ? document.elementsFromPoint(e.clientX, e.clientY)
    : ([document.elementFromPoint(e.clientX, e.clientY)].filter(Boolean) as Element[]);
  for (let i = 0; i < els.length; i++) {
    if (els[i] && els[i].hasAttribute && els[i].hasAttribute('data-va-id')) return els[i];
  }
  return null;
}

// ── VA callout ────────────────────────────────────────────────────────────────

export function showVaCallout(ctx: MapCtx, d: VaRec | undefined): void {
  if (!d) return;
  const el = document.getElementById(DOM_IDS.vaCallout);
  if (!el) return;
  const vaHint = document.getElementById(DOM_IDS.ecVaHint);
  if (vaHint) vaHint.style.display = 'none';
  _setText(DOM_IDS.vcName, d.poll_name || '');
  _setText(DOM_IDS.vcUcpPct, d.ucp_pct != null ? d.ucp_pct + '%' : '');
  _setText(DOM_IDS.vcNdpPct, d.ndp_pct != null ? d.ndp_pct + '%' : '');
  _setWidth(DOM_IDS.vcUcpBar, d.ucp_pct || 0);
  _setWidth(DOM_IDS.vcNdpBar, d.ndp_pct || 0);
  _setText(DOM_IDS.vcTotal, d.in_person_votes ? _fmt.format(d.in_person_votes) + ' ' + STR.inPersonVotes : '');
  ctx.selectedVaId = d.va_id != null ? String(d.va_id) : null;
  el.classList.add('vc-visible');
  // Fallback for browsers without :has() support — merge ed-callout's bottom with va-callout
  const edCallout = document.getElementById(DOM_IDS.edCallout);
  if (edCallout) edCallout.classList.add('ec-has-va');
}

export function hideVaCallout(ctx: MapCtx): void {
  const el = document.getElementById(DOM_IDS.vaCallout);
  if (el) el.classList.remove('vc-visible');
  ctx.selectedVaId = null;
  const edCallout = document.getElementById(DOM_IDS.edCallout);
  if (edCallout) edCallout.classList.remove('ec-has-va');
}

export function isEdVisible(ctx: MapCtx, bb: BBox): boolean {
  if (!ctx.curVB || !bb.width || !bb.height) return false;
  const xOv = Math.max(0, Math.min(bb.x + bb.width, ctx.curVB.x + ctx.curVB.w) - Math.max(bb.x, ctx.curVB.x));
  const yOv = Math.max(0, Math.min(bb.y + bb.height, ctx.curVB.y + ctx.curVB.h) - Math.max(bb.y, ctx.curVB.y));
  return (xOv * yOv) / (bb.width * bb.height) >= 0.95;
}

// ── Navigation ────────────────────────────────────────────────────────────────

type AnimateToVB = (vb: ViewBox, dur: number) => void;
type GetStageRect = () => DOMRect;

export function snapToED(
  ctx: MapCtx,
  pathEl: SVGGraphicsElement,
  force: boolean,
  animateToVB: AnimateToVB,
  getStageRect: GetStageRect,
): void {
  if (!ctx.svgEl || ctx.mode !== 'viewbox') return;
  const bb = pathEl.getBBox();
  if (!force && isEdVisible(ctx, bb)) return;
  const pad = Math.max(bb.width, bb.height) * 0.35;
  let tw = bb.width + pad * 2, th = bb.height + pad * 2;
  const r = getStageRect();
  if (tw / th < r.width / r.height) tw = th * r.width / r.height;
  else th = tw * r.height / r.width;
  const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
  animateToVB({ x: cx - tw/2, y: cy - th/2, w: tw, h: th }, 420);
}

export function zoomEdTo70(
  ctx: MapCtx,
  pathEl: SVGGraphicsElement,
  animateToVB: AnimateToVB,
  getStageRect: GetStageRect,
): void {
  if (!ctx.svgEl || ctx.mode !== 'viewbox' || ctx.mapLocked) return;
  const bb = pathEl.getBBox();
  const r = getStageRect();
  const vw = Math.max(bb.width / 0.70, bb.height / 0.70 * r.width / r.height);
  const vh = vw * r.height / r.width;
  const cx = bb.x + bb.width  / 2;
  const cy = bb.y + bb.height / 2;
  animateToVB({ x: cx - vw/2, y: cy - vh/2, w: vw, h: vh }, 380);
}

export function activateCenterED(ctx: MapCtx, animateToVB: AnimateToVB, emit: MapEngineEventHandler): void {
  if (ctx.mapLocked || !ctx.svgEl || !ctx.edHover || !ctx.curVB) return;
  const cx = ctx.curVB.x + ctx.curVB.w / 2, cy = ctx.curVB.y + ctx.curVB.h / 2;
  let bestPath: SVGGraphicsElement | null = null;
  let bestDist = Infinity;
  ctx.svgEl.querySelectorAll<SVGGraphicsElement>('[data-ed-id]').forEach(p => {
    const bb = p.getBBox();
    const dist = Math.hypot(bb.x + bb.width / 2 - cx, bb.y + bb.height / 2 - cy);
    if (dist < bestDist) { bestDist = dist; bestPath = p; }
  });
  if (!bestPath) return;
  // Local non-null alias so the closure-mutated bestPath narrows correctly.
  const path = bestPath as SVGGraphicsElement;
  const edId = parseInt(path.getAttribute('data-ed-id') || '0', 10);
  const rec = ctx.edHover[edId] as EdRec | undefined;
  if (rec) {
    showCallout(ctx, rec);
    setEdHighlight(ctx, path);
    emit({ type: 'ed_focus', ed_id: edId });
  }
  // Silence unused-import warning when callers pass animateToVB but no caller uses it here.
  void animateToVB;
}
