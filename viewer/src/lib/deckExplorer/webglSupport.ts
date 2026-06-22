// Alberta Electoral Boundary Audit — WebGL capability probe
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// hasWebGL() decides, at runtime in the browser, whether the deck.gl explorer
// (which needs a WebGL/WebGL2 context) can run. When it returns false the caller
// falls back to the production inline-SVG explorer (mapEngine). It also accepts a
// `forceOff` override so a caller can disable WebGL deliberately (e.g. the
// ?nowebgl=1 query escape hatch) without re-probing.
//
// SSR / prerender safety: this touches `document`, so it must only be called in
// the browser. The caller guards by invoking it from onMount (never at module
// top level and never during adapter-static prerender).

/**
 * Returns true when a WebGL2 or WebGL rendering context can be created.
 *
 * @param forceOff - When true, skip the probe and return false (deliberate
 *                   opt-out, e.g. the ?nowebgl=1 escape hatch).
 * @returns whether deck.gl can be rendered in this environment.
 */
export function hasWebGL(forceOff = false): boolean {
  if (forceOff) return false;
  try {
    const canvas = document.createElement('canvas');
    const gl =
      canvas.getContext('webgl2') || canvas.getContext('webgl');
    return !!gl;
  } catch {
    // Some environments throw from getContext (or createElement) rather than
    // returning null — treat any failure as "no WebGL".
    return false;
  }
}
