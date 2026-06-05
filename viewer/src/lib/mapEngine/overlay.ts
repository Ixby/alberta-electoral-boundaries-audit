// Alberta Electoral Boundary Audit — overlay open / close / focus management
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

import type { MapCtx } from './types';
import { DOM_IDS } from './domIds';
import { hideIntro } from './introModal';

type OverlayDeps = {
  updateMapButtons: () => void;
  maybeShowIntro:   () => void;
  resetVB:          () => void;
  hideTip:          () => void;
  hideCallout:      () => void;
  // Called exactly once on the first open — used to kick off the hover/VA
  // JSON downloads (deferred from init so the page-load critical path stays
  // empty of map-tool work).
  primeOnce:        () => void;
};

function _overlayFocusable(overlayEl: HTMLElement): HTMLElement[] {
  return Array.from(overlayEl.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )).filter(el => !el.hasAttribute('disabled'));
}

// Returns { open, close } so callers can pass them to other modules as deps.
// Trigger wiring is NOT done here — the caller owns the first trigger click
// (lazy-load pattern: Svelte intercepts, dynamic-imports the engine, then calls open()).
export function initOverlay(ctx: MapCtx, overlayEl: HTMLElement, closeBtnEl: HTMLElement, deps: OverlayDeps) {
  let _primed = false;

  function open() {
    if (!_primed) { _primed = true; deps.primeOnce(); }
    ctx.stageRect = null;
    overlayEl.style.display = 'block';
    document.body.style.overflow = 'hidden';
    deps.updateMapButtons();
    deps.maybeShowIntro();
    ctx.prevFocus = document.activeElement;
    const focusable = _overlayFocusable(overlayEl);
    if (focusable.length) focusable[0].focus();
    if (!ctx.ready) return;
    deps.resetVB();
  }

  function close() {
    overlayEl.style.display = 'none';
    document.body.style.overflow = '';
    deps.hideTip();
    deps.hideCallout();
    if (ctx.prevFocus instanceof HTMLElement) ctx.prevFocus.focus();
    ctx.prevFocus = null;
    // Hide intro modal without marking seen — re-shows on next open until dismissed.
    hideIntro();
  }

  // Tab trap
  overlayEl.addEventListener('keydown', function(e) {
    if (e.key !== 'Tab') return;
    const focusable = _overlayFocusable(overlayEl);
    if (!focusable.length) return;
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey) { if (document.activeElement === first) { e.preventDefault(); last.focus(); } }
    else { if (document.activeElement === last) { e.preventDefault(); first.focus(); } }
  });

  closeBtnEl.addEventListener('click', close);
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    const intro = document.getElementById(DOM_IDS.mapIntroModal) as HTMLElement | null;
    if (intro && intro.style.display !== 'none') return; // let modal handle its own Escape
    close();
  });
  overlayEl.addEventListener('click', e => { if (e.target === overlayEl) close(); });

  return { open, close };
}
