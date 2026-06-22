// @vitest-environment happy-dom
//
// Tests for src/lib/deckExplorer/webglSupport.ts
//
// hasWebGL() must:
//   1. Return true when a canvas yields a webgl2 context.
//   2. Return true when webgl2 is null but webgl succeeds (fallback).
//   3. Return false when neither context is available.
//   4. Return false (not throw) when getContext throws.
//   5. Return false immediately when forceOff is passed (no probe).

import { describe, it, expect, vi, afterEach } from 'vitest';
import { hasWebGL } from '../../src/lib/deckExplorer/webglSupport';

const realGetContext = HTMLCanvasElement.prototype.getContext;

afterEach(() => {
  HTMLCanvasElement.prototype.getContext = realGetContext;
  vi.restoreAllMocks();
});

// Stub getContext to return a truthy object only for the named context type(s).
function stubContexts(available: string[]) {
  HTMLCanvasElement.prototype.getContext = vi.fn(function (
    this: HTMLCanvasElement,
    type: string,
  ) {
    return available.includes(type) ? ({} as RenderingContext) : null;
  }) as typeof HTMLCanvasElement.prototype.getContext;
}

describe('hasWebGL', () => {
  it('returns true when webgl2 is available', () => {
    stubContexts(['webgl2']);
    expect(hasWebGL()).toBe(true);
  });

  it('returns true when only webgl (no webgl2) is available', () => {
    stubContexts(['webgl']);
    expect(hasWebGL()).toBe(true);
  });

  it('returns false when no WebGL context is available', () => {
    stubContexts([]); // every getContext call returns null
    expect(hasWebGL()).toBe(false);
  });

  it('returns false (does not throw) when getContext throws', () => {
    HTMLCanvasElement.prototype.getContext = vi.fn(() => {
      throw new Error('context creation blocked');
    }) as typeof HTMLCanvasElement.prototype.getContext;
    expect(() => hasWebGL()).not.toThrow();
    expect(hasWebGL()).toBe(false);
  });

  it('returns false immediately when forceOff is true, without probing', () => {
    const spy = vi.fn();
    HTMLCanvasElement.prototype.getContext =
      spy as typeof HTMLCanvasElement.prototype.getContext;
    expect(hasWebGL(true)).toBe(false);
    expect(spy).not.toHaveBeenCalled();
  });
});
