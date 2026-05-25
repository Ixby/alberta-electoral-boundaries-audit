// @ts-nocheck
// Alberta Electoral Boundary Audit — ED interaction
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Tooltip, callout, ED highlight, snap-to-ED, zoom-to-ED.
// Reads/writes: ctx.svgEl, ctx.edHover, ctx.curVB, ctx.mapPrimary, ctx.nameIndex,
//               ctx.selectedEdName, ctx.highlightPath, ctx.mode, ctx.mapLocked, ctx.rafId.
// animateToVB and getStageRect are passed as callbacks to avoid circular deps with viewport.

import type { MapCtx } from './types';

const _fmt = new Intl.NumberFormat();

// ── Tooltip ───────────────────────────────────────────────────────────────────

export function showTip(d, x: number, y: number): void {
  if (!d) return;
  const tip = document.getElementById('ed-tooltip');
  if (!tip) return;
  tip.innerHTML =
    `<strong>${d.name}</strong>` +
    `UCP&nbsp;${d.ucp_pct}%&nbsp;&nbsp;NDP&nbsp;${d.ndp_pct}%` +
    (d.votes ? `<br>${_fmt.format(d.votes)}&nbsp;votes&nbsp;(2023)` : '') +
    (d.pop   ? `<br>Pop.&nbsp;${_fmt.format(d.pop)}` : '');
  const pad = 14, tw = 200, th = 60; // fixed estimates — avoids synchronous layout read on pointermove
  let lx = x + pad, ly = y + pad;
  if (lx + tw > window.innerWidth)  lx = x - tw - pad;
  if (ly + th > window.innerHeight) ly = y - th - pad;
  tip.style.cssText = `display:block;left:${lx}px;top:${ly}px`;
}

export function hideTip(): void {
  const tip = document.getElementById('ed-tooltip');
  if (tip) tip.style.display = 'none';
}

// ── Callout ───────────────────────────────────────────────────────────────────

export function showCallout(ctx: MapCtx, d): void {
  if (!d) return;
  document.getElementById('ec-name').textContent = d.name;
  document.getElementById('ec-ucp-bar').style.width = d.ucp_pct + '%';
  document.getElementById('ec-ndp-bar').style.width = d.ndp_pct + '%';
  document.getElementById('ec-ucp-pct').textContent = d.ucp_pct + '%';
  document.getElementById('ec-ndp-pct').textContent = d.ndp_pct + '%';
  document.getElementById('ec-ucp-votes').textContent = d.ucp_votes ? _fmt.format(d.ucp_votes) + ' votes' : '';
  document.getElementById('ec-ndp-votes').textContent = d.ndp_votes ? _fmt.format(d.ndp_votes) + ' votes' : '';
  document.getElementById('ec-total-votes').textContent = d.votes ? _fmt.format(d.votes) + ' total votes' : '';
  const vaEl = document.getElementById('ec-va-count');
  if (vaEl) vaEl.textContent = d.va_count ? d.va_count + ' voting areas' : '';
  const popN = d.pop ? Math.round(d.pop / 100) * 100 : 0;
  document.getElementById('ec-pop').textContent = popN ? 'Pop. ' + _fmt.format(popN) : '';

  const egEl = document.getElementById('ec-eg');
  if (egEl) {
    if (d.eg !== undefined && d.eg !== null) {
      const sign = d.eg >= 0 ? '+' : '';
      egEl.textContent = sign + (d.eg * 100).toFixed(2) + '%';
      egEl.className = d.eg >= 0 ? 'ec-eg-ucp' : 'ec-eg-ndp';
    } else {
      egEl.textContent = ''; egEl.className = '';
    }
  }

  const ctxEl = document.getElementById('ec-context');
  if (ctxEl) {
    const mapLabel = ctx.mapPrimary === 'minority' ? '2026 minority proposal'
                   : ctx.mapPrimary === 'majority' ? '2026 majority proposal'
                   : '2019 enacted map';
    ctxEl.textContent = mapLabel + ' · 2023 election results';
  }

  const cmpEl = document.getElementById('ec-compare');
  if (cmpEl) {
    const others = ['minority', 'majority', '2019'].filter(k => k !== ctx.mapPrimary);
    const parts = others.map(function(k) {
      const rec = ctx.nameIndex[k] && ctx.nameIndex[k][d.name];
      if (!rec) return null;
      const label = k === 'minority' ? 'Min.' : k === 'majority' ? 'Maj.' : '2019';
      const ucpFirst = rec.ucp_pct >= rec.ndp_pct;
      const winner = ucpFirst
        ? '<span class="ec-cmp-val ec-cmp-ucp">UCP ' + rec.ucp_pct + '%</span>'
        : '<span class="ec-cmp-val ec-cmp-ndp">NDP ' + rec.ndp_pct + '%</span>';
      const loser = ucpFirst
        ? '<span class="ec-cmp-second">NDP ' + rec.ndp_pct + '%</span>'
        : '<span class="ec-cmp-second">UCP ' + rec.ucp_pct + '%</span>';
      return '<span class="ec-cmp-item"><span class="ec-cmp-label">' + label + '</span>' + winner + '<span class="ec-cmp-sep">/</span>' + loser + '</span>';
    }).filter(Boolean);
    if (parts.length) {
      cmpEl.innerHTML = '<span class="ec-cmp-header">Other maps</span>' + parts.join('');
      cmpEl.style.display = 'flex';
    } else {
      cmpEl.innerHTML = '<span class="ec-cmp-unique">Boundary unique to this map</span>';
      cmpEl.style.display = 'flex';
    }
  }

  ctx.selectedEdName = d.name;
  const srEl = document.getElementById('sr-announce');
  if (srEl) srEl.textContent = d.name + ' — UCP ' + d.ucp_pct + '%, NDP ' + d.ndp_pct + '%';
  const vaHint = document.getElementById('ec-va-hint');
  if (vaHint) vaHint.style.display = (ctx.allVaData && ctx.allVaData[ctx.mapPrimary] && Object.keys(ctx.allVaData[ctx.mapPrimary]).length) ? '' : 'none';
  const callout = document.getElementById('ed-callout');
  const hud     = document.getElementById('hud');
  if (callout) callout.classList.add('ec-visible');
  if (hud) hud.classList.add('ec-has-ed');
}

export function hideCallout(ctx: MapCtx): void {
  const callout = document.getElementById('ed-callout');
  const hud     = document.getElementById('hud');
  if (callout) callout.classList.remove('ec-visible');
  if (hud) hud.classList.remove('ec-has-ed');
  ctx.selectedEdName = null;
  clearEdHighlight(ctx);
  const srEl = document.getElementById('sr-announce');
  if (srEl) srEl.textContent = '';
  const vaHint = document.getElementById('ec-va-hint');
  if (vaHint) vaHint.style.display = 'none';
}

// ── ED highlight ──────────────────────────────────────────────────────────────

export function setEdHighlight(ctx: MapCtx, pathEl): void {
  clearEdHighlight(ctx);
  if (!ctx.svgEl || !pathEl) return;
  const d = pathEl.getAttribute('d');
  ctx.highlightPath = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  ctx.highlightPath.setAttribute('pointer-events', 'none');
  const glow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  glow.setAttribute('d', d);
  glow.setAttribute('fill', 'none');
  glow.setAttribute('stroke', 'rgba(255,255,255,0.25)');
  glow.setAttribute('stroke-width', '6');
  glow.setAttribute('stroke-linejoin', 'round');
  glow.style.vectorEffect = 'non-scaling-stroke';
  glow.style.filter = 'blur(2px)';
  const sharp = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  sharp.setAttribute('d', d);
  sharp.setAttribute('fill', 'none');
  sharp.setAttribute('stroke', '#ffffff');
  sharp.setAttribute('stroke-width', '2.5');
  sharp.setAttribute('stroke-linejoin', 'round');
  sharp.style.vectorEffect = 'non-scaling-stroke';
  ctx.highlightPath.appendChild(glow);
  ctx.highlightPath.appendChild(sharp);
  ctx.svgEl.appendChild(ctx.highlightPath);
}

export function clearEdHighlight(ctx: MapCtx): void {
  if (ctx.highlightPath) { ctx.highlightPath.remove(); ctx.highlightPath = null; }
}

// ── Hit-testing ───────────────────────────────────────────────────────────────

export function tipTarget(e): Element | null {
  const els = document.elementsFromPoint
    ? document.elementsFromPoint(e.clientX, e.clientY)
    : [document.elementFromPoint(e.clientX, e.clientY)];
  for (let i = 0; i < els.length; i++) {
    if (els[i] && els[i].hasAttribute && els[i].hasAttribute('data-ed-id')) return els[i];
  }
  return null;
}

export function vaTarget(e): Element | null {
  const els = document.elementsFromPoint
    ? document.elementsFromPoint(e.clientX, e.clientY)
    : [document.elementFromPoint(e.clientX, e.clientY)];
  for (let i = 0; i < els.length; i++) {
    if (els[i] && els[i].hasAttribute && els[i].hasAttribute('data-va-id')) return els[i];
  }
  return null;
}

// ── VA callout ────────────────────────────────────────────────────────────────

export function showVaCallout(ctx: MapCtx, d): void {
  if (!d) return;
  const el = document.getElementById('va-callout');
  if (!el) return;
  const vaHint = document.getElementById('ec-va-hint');
  if (vaHint) vaHint.style.display = 'none';
  const nameEl = document.getElementById('vc-name');
  if (nameEl) nameEl.textContent = d.poll_name || '';
  const ucpEl = document.getElementById('vc-ucp-pct');
  if (ucpEl) ucpEl.textContent = d.ucp_pct != null ? d.ucp_pct + '%' : '';
  const ndpEl = document.getElementById('vc-ndp-pct');
  if (ndpEl) ndpEl.textContent = d.ndp_pct != null ? d.ndp_pct + '%' : '';
  const ucpBarEl = document.getElementById('vc-ucp-bar');
  if (ucpBarEl) ucpBarEl.style.width = (d.ucp_pct || 0) + '%';
  const ndpBarEl = document.getElementById('vc-ndp-bar');
  if (ndpBarEl) ndpBarEl.style.width = (d.ndp_pct || 0) + '%';
  const totalEl = document.getElementById('vc-total');
  if (totalEl) totalEl.textContent = d.in_person_votes ? _fmt.format(d.in_person_votes) + ' in-person votes (excl. Vote Anywhere)' : '';
  ctx.selectedVaId = d.va_id != null ? String(d.va_id) : null;
  el.classList.add('vc-visible');
  // Fallback for browsers without :has() support — merge ed-callout's bottom with va-callout
  const edCallout = document.getElementById('ed-callout');
  if (edCallout) edCallout.classList.add('ec-has-va');
}

export function hideVaCallout(ctx: MapCtx): void {
  const el = document.getElementById('va-callout');
  if (el) el.classList.remove('vc-visible');
  ctx.selectedVaId = null;
  const edCallout = document.getElementById('ed-callout');
  if (edCallout) edCallout.classList.remove('ec-has-va');
}

export function isEdVisible(ctx: MapCtx, bb): boolean {
  if (!ctx.curVB || !bb.width || !bb.height) return false;
  const xOv = Math.max(0, Math.min(bb.x + bb.width, ctx.curVB.x + ctx.curVB.w) - Math.max(bb.x, ctx.curVB.x));
  const yOv = Math.max(0, Math.min(bb.y + bb.height, ctx.curVB.y + ctx.curVB.h) - Math.max(bb.y, ctx.curVB.y));
  return (xOv * yOv) / (bb.width * bb.height) >= 0.95;
}

// ── Navigation ────────────────────────────────────────────────────────────────

export function snapToED(ctx: MapCtx, pathEl, force: boolean, animateToVB, getStageRect): void {
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

export function zoomEdTo70(ctx: MapCtx, pathEl, animateToVB, getStageRect): void {
  if (!ctx.svgEl || ctx.mode !== 'viewbox' || ctx.mapLocked) return;
  const bb = pathEl.getBBox();
  const r = getStageRect();
  const vw = Math.max(bb.width / 0.70, bb.height / 0.70 * r.width / r.height);
  const vh = vw * r.height / r.width;
  const cx = bb.x + bb.width  / 2;
  const cy = bb.y + bb.height / 2;
  animateToVB({ x: cx - vw/2, y: cy - vh/2, w: vw, h: vh }, 380);
}

export function activateCenterED(ctx: MapCtx, animateToVB, emit): void {
  if (ctx.mapLocked || !ctx.svgEl || !ctx.edHover || !ctx.curVB) return;
  const cx = ctx.curVB.x + ctx.curVB.w / 2, cy = ctx.curVB.y + ctx.curVB.h / 2;
  let bestPath = null, bestDist = Infinity;
  ctx.svgEl.querySelectorAll('[data-ed-id]').forEach(p => {
    const bb = p.getBBox();
    const dist = Math.hypot(bb.x + bb.width / 2 - cx, bb.y + bb.height / 2 - cy);
    if (dist < bestDist) { bestDist = dist; bestPath = p; }
  });
  if (!bestPath) return;
  const rec = ctx.edHover[parseInt(bestPath.getAttribute('data-ed-id'), 10)];
  if (rec) {
    showCallout(ctx, rec);
    setEdHighlight(ctx, bestPath);
    emit({ type: 'ed_focus', ed_id: parseInt(bestPath.getAttribute('data-ed-id'), 10) });
  }
}
