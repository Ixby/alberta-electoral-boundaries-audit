// @vitest-environment happy-dom
//
// Tests for src/lib/a11y/focusTrap.ts
//
// Four properties matter:
//   1. On mount, focus moves to the first focusable descendant.
//   2. Pressing Tab while the last focusable element is focused wraps to the first.
//   3. Calling destroy() restores focus to the element that held focus before mount.
//   4. Pressing Escape calls the onEscape callback.

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createFocusTrap, focusTrap } from '../src/lib/a11y/focusTrap';

// ── helpers ───────────────────────────────────────────────────────────────────

/** Build a container with `n` buttons and append it to document.body. */
function makeContainer(n: number): { container: HTMLElement; buttons: HTMLButtonElement[] } {
  const container = document.createElement('div');
  const buttons: HTMLButtonElement[] = [];
  for (let i = 0; i < n; i++) {
    const btn = document.createElement('button');
    btn.textContent = `Button ${i}`;
    container.appendChild(btn);
    buttons.push(btn);
  }
  document.body.appendChild(container);
  return { container, buttons };
}

/** Build and append a standalone button that can hold focus before the trap is created. */
function makeFocusSink(): HTMLButtonElement {
  const btn = document.createElement('button');
  btn.textContent = 'sink';
  document.body.appendChild(btn);
  return btn;
}

/** Fire a keydown event on `target`. */
function keydown(target: EventTarget, key: string, shiftKey = false): void {
  target.dispatchEvent(new KeyboardEvent('keydown', { key, shiftKey, bubbles: true }));
}

// ── cleanup ───────────────────────────────────────────────────────────────────

beforeEach(() => {
  // Clear all DOM nodes added to body between tests.
  document.body.innerHTML = '';
});

// ── tests ─────────────────────────────────────────────────────────────────────

describe('createFocusTrap()', () => {
  it('moves focus to the first focusable child on mount', () => {
    const { container, buttons } = makeContainer(2);
    const cleanup = createFocusTrap(container);
    expect(document.activeElement).toBe(buttons[0]);
    cleanup();
  });

  it('wraps Tab from the last focusable to the first', () => {
    const { container, buttons } = makeContainer(2);
    const cleanup = createFocusTrap(container);

    // Move focus to the last button first.
    buttons[buttons.length - 1].focus();
    expect(document.activeElement).toBe(buttons[1]);

    // Dispatch Tab on the container (keydown listener is on the container node).
    keydown(container, 'Tab');

    expect(document.activeElement).toBe(buttons[0]);
    cleanup();
  });

  it('restores focus to the previously-focused element on destroy', () => {
    const sink = makeFocusSink();
    sink.focus();
    expect(document.activeElement).toBe(sink);

    const { container } = makeContainer(2);
    const cleanup = createFocusTrap(container);

    // Focus has moved into the trap.
    expect(document.activeElement).not.toBe(sink);

    cleanup();

    expect(document.activeElement).toBe(sink);
  });

  it('calls onEscape when Escape is pressed', () => {
    const onEscape = vi.fn();
    const { container } = makeContainer(2);
    const cleanup = createFocusTrap(container, onEscape);

    keydown(container, 'Escape');
    expect(onEscape).toHaveBeenCalledTimes(1);

    cleanup();
  });
});

describe('focusTrap() Svelte action', () => {
  it('moves focus to the first button on mount', () => {
    const { container, buttons } = makeContainer(2);
    const action = focusTrap(container);
    expect(document.activeElement).toBe(buttons[0]);
    action.destroy();
  });

  it('restores focus on destroy', () => {
    const sink = makeFocusSink();
    sink.focus();

    const { container } = makeContainer(2);
    const action = focusTrap(container);
    action.destroy();

    expect(document.activeElement).toBe(sink);
  });

  it('update() refreshes onEscape without re-mounting the trap', () => {
    const first  = vi.fn();
    const second = vi.fn();
    const { container } = makeContainer(2);

    const action = focusTrap(container, { onEscape: first });
    keydown(container, 'Escape');
    expect(first).toHaveBeenCalledTimes(1);
    expect(second).toHaveBeenCalledTimes(0);

    // Swap the handler via update.
    action.update({ onEscape: second });
    keydown(container, 'Escape');
    expect(first).toHaveBeenCalledTimes(1); // still 1 — not called again
    expect(second).toHaveBeenCalledTimes(1);

    action.destroy();
  });
});
