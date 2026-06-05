// Alberta Electoral Boundary Audit — ready-state signalling
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Replaces hand-rolled setTimeout polling loops (zoomToEd, search.waitAndNav).
// Callers do `await awaitReady(ctx, 3000)`; modules that flip ctx.ready=true
// call notifyReady(ctx) once the SVG is fully attached.

import type { MapCtx } from './types';

export function awaitReady(ctx: MapCtx, timeoutMs = 3000): Promise<void> {
  if (ctx.ready) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      ctx.readyWaiters = ctx.readyWaiters.filter(w => w !== onReady);
      reject(new Error('mapEngine: not ready within ' + timeoutMs + 'ms'));
    }, timeoutMs);
    const onReady = () => { clearTimeout(timer); resolve(); };
    ctx.readyWaiters.push(onReady);
  });
}

export function notifyReady(ctx: MapCtx): void {
  const waiters = ctx.readyWaiters;
  ctx.readyWaiters = [];
  waiters.forEach(w => { try { w(); } catch (_) {} });
}
