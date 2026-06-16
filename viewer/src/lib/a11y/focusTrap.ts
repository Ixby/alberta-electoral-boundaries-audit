// Alberta Electoral Boundary Audit — focus-trap a11y primitive
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Two exports:
//   createFocusTrap(node, onEscape?) → cleanup()
//     Imperative helper: saves active element, moves focus in, traps Tab, calls
//     onEscape on Escape key, restores focus on cleanup. Reusable from plain JS.
//
//   focusTrap(node, opts?)
//     Svelte action wrapping createFocusTrap. Supports update(newOpts) to refresh
//     onEscape without tearing down and re-mounting the trap.

const FOCUSABLE =
  'a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])';

/**
 * Imperative focus trap. Sets up focus management on `node` immediately.
 * Returns a cleanup function that removes the listener and restores focus.
 *
 * @param node     - The container element to trap focus within.
 * @param onEscape - Optional callback invoked when Escape is pressed.
 * @returns cleanup function
 */
export function createFocusTrap(
  node: HTMLElement,
  onEscape?: () => void,
): () => void {
  const saved = document.activeElement as HTMLElement | null;

  const focusables = (): HTMLElement[] =>
    Array.from(node.querySelectorAll<HTMLElement>(FOCUSABLE)).filter(
      (el) => !el.closest('[hidden]'),
    );

  // Move focus into the trap on mount.
  const first = focusables()[0];
  if (first) {
    first.focus();
  } else {
    // No focusable children — focus the container itself.
    if (!node.hasAttribute('tabindex')) node.setAttribute('tabindex', '-1');
    node.focus();
  }

  function onKeydown(e: KeyboardEvent): void {
    if (e.key === 'Escape') {
      onEscape?.();
      return;
    }
    if (e.key !== 'Tab') return;

    const items = focusables();
    if (!items.length) { e.preventDefault(); return; }

    const firstEl = items[0];
    const lastEl  = items[items.length - 1];
    const active  = document.activeElement;

    if (e.shiftKey) {
      // Shift+Tab: wrap from first → last
      if (active === firstEl || active === node) {
        e.preventDefault();
        lastEl.focus();
      }
    } else {
      // Tab: wrap from last → first
      if (active === lastEl) {
        e.preventDefault();
        firstEl.focus();
      }
    }
  }

  node.addEventListener('keydown', onKeydown);

  return function cleanup(): void {
    node.removeEventListener('keydown', onKeydown);
    if (saved && typeof saved.focus === 'function') {
      saved.focus();
    }
  };
}

// ── Svelte action ─────────────────────────────────────────────────────────────

export interface FocusTrapOptions {
  onEscape?: () => void;
}

/**
 * Svelte action: traps Tab focus inside `node` while mounted, moves focus in on
 * mount, restores focus to the previously-focused element on destroy, and calls
 * onEscape (if provided) when Escape is pressed.
 *
 * Usage:
 *   <div use:focusTrap={{ onEscape: () => open = false }}>…</div>
 */
export function focusTrap(
  node: HTMLElement,
  opts?: FocusTrapOptions,
): { destroy(): void; update(newOpts?: FocusTrapOptions): void } {
  // Hold opts in a mutable reference so update() doesn't need to rebuild the trap.
  let currentOpts = opts;

  // Pass a stable wrapper so the keydown closure always calls the current onEscape.
  const cleanup = createFocusTrap(node, () => currentOpts?.onEscape?.());

  return {
    update(newOpts?: FocusTrapOptions): void {
      currentOpts = newOpts;
    },
    destroy(): void {
      cleanup();
    },
  };
}
