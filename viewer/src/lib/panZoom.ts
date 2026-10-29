// Alberta Electoral Boundary Audit — pan/zoom for the figure lightbox
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
//
// Pinch zooms about the pinch midpoint and pans with it; one pointer drags the
// zoomed image; the wheel zooms about the cursor; a double-tap/double-click
// toggles zoom; + − 0 and the arrow keys do the same from the keyboard.
//
// The target is drawn with `translate(x, y) scale(s)` and transform-origin at
// its centre, and sits centred in the container (a flex lightbox), so a screen
// point p maps to the image as  p = c + t + s·(q − c),  c = container centre.
// The maths is pure and exported for tests; attachPanZoom wires it to events.

export interface View {
	s: number;
	x: number;
	y: number;
}

export const MIN_SCALE = 1;
export const MAX_SCALE = 8;
const TAP_ZOOM = 2.5;
const DOUBLE_TAP_MS = 300;
const DOUBLE_TAP_PX = 24;
const DRAG_SLOP_PX = 5;
const KEY_PAN_PX = 60;

export const IDENTITY: View = { s: 1, x: 0, y: 0 };

/** Zoom by `factor` keeping screen point (px, py) fixed; (cx, cy) = container centre. */
export function zoomAbout(v: View, factor: number, px: number, py: number, cx: number, cy: number): View {
	const s = Math.min(MAX_SCALE, Math.max(MIN_SCALE, v.s * factor));
	if (s === MIN_SCALE) return { ...IDENTITY };
	const k = s / v.s;
	return { s, x: px - cx - k * (px - cx - v.x), y: py - cy - k * (py - cy - v.y) };
}

/** One pinch step: zoom about the old midpoint by the distance ratio, then
 *  follow the midpoint's travel — so the content under the fingers stays put. */
export function pinchStep(
	v: View,
	from: { mx: number; my: number; d: number },
	to: { mx: number; my: number; d: number },
	cx: number,
	cy: number
): View {
	if (from.d <= 0) return v;
	const z = zoomAbout(v, to.d / from.d, from.mx, from.my, cx, cy);
	if (z.s === MIN_SCALE) return z;
	return { s: z.s, x: z.x + (to.mx - from.mx), y: z.y + (to.my - from.my) };
}

/** Keep part of the image on screen: the centre may travel at most half the
 *  scaled image's size from the container centre. Unzoomed, it is pinned. */
export function clamp(v: View, w: number, h: number): View {
	if (v.s <= MIN_SCALE) return { ...IDENTITY };
	const mx = (v.s * w) / 2;
	const my = (v.s * h) / 2;
	return { s: v.s, x: Math.max(-mx, Math.min(mx, v.x)), y: Math.max(-my, Math.min(my, v.y)) };
}

export function toCss(v: View): string {
	return v.s === 1 && v.x === 0 && v.y === 0 ? '' : `translate(${v.x}px, ${v.y}px) scale(${v.s})`;
}

/**
 * Wire pan/zoom onto `container` (receives the pointer events; needs
 * `touch-action: none`) for `target` (the image; `pointer-events: none`).
 * `wasDrag()` lets a click handler tell a drag from a tap on the backdrop.
 */
export function attachPanZoom(container: HTMLElement, target: HTMLElement) {
	let v: View = { ...IDENTITY };
	const ptrs = new Map<number, { x: number; y: number }>();
	let pinch: { mx: number; my: number; d: number } | null = null;
	let downAt: { x: number; y: number } | null = null;
	let dragged = false;
	let lastTap = { t: 0, x: 0, y: 0 };

	const centre = () => {
		const r = container.getBoundingClientRect();
		return { cx: r.left + r.width / 2, cy: r.top + r.height / 2 };
	};
	function apply(next: View) {
		v = clamp(next, target.offsetWidth, target.offsetHeight);
		target.style.transform = toCss(v);
		container.style.cursor = v.s > MIN_SCALE ? (ptrs.size ? 'grabbing' : 'grab') : '';
	}
	function zoomAt(factor: number, px: number, py: number) {
		const { cx, cy } = centre();
		apply(zoomAbout(v, factor, px, py, cx, cy));
	}
	function pinchState() {
		const [a, b] = [...ptrs.values()];
		return { mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2, d: Math.hypot(b.x - a.x, b.y - a.y) };
	}

	const onWheel = (e: WheelEvent) => {
		e.preventDefault();
		zoomAt(e.deltaY < 0 ? 1.15 : 1 / 1.15, e.clientX, e.clientY);
	};
	const onDown = (e: PointerEvent) => {
		// Only the backdrop (and the image, which passes its pointers through)
		// takes gestures; a press on a control inside the container stays a click.
		if (e.target !== container) return;
		container.setPointerCapture?.(e.pointerId);
		ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
		if (ptrs.size === 1) {
			downAt = { x: e.clientX, y: e.clientY };
			dragged = false;
		}
		pinch = ptrs.size === 2 ? pinchState() : null;
		apply(v);
	};
	const onMove = (e: PointerEvent) => {
		const prev = ptrs.get(e.pointerId);
		if (!prev) return;
		const cur = { x: e.clientX, y: e.clientY };
		ptrs.set(e.pointerId, cur);
		if (downAt && Math.hypot(cur.x - downAt.x, cur.y - downAt.y) > DRAG_SLOP_PX) dragged = true;
		if (ptrs.size >= 2 && pinch) {
			const next = pinchState();
			const { cx, cy } = centre();
			apply(pinchStep(v, pinch, next, cx, cy));
			pinch = next;
		} else if (ptrs.size === 1 && v.s > MIN_SCALE) {
			apply({ s: v.s, x: v.x + cur.x - prev.x, y: v.y + cur.y - prev.y });
		}
	};
	const onUp = (e: PointerEvent) => {
		if (!ptrs.delete(e.pointerId)) return;
		pinch = ptrs.size === 2 ? pinchState() : null;
		// Double-tap / double-click toggles zoom about the tap point.
		if (!dragged && ptrs.size === 0) {
			const now = performance.now();
			const near = Math.hypot(e.clientX - lastTap.x, e.clientY - lastTap.y) < DOUBLE_TAP_PX;
			if (now - lastTap.t < DOUBLE_TAP_MS && near) {
				if (v.s > MIN_SCALE) apply({ ...IDENTITY });
				else zoomAt(TAP_ZOOM, e.clientX, e.clientY);
				lastTap = { t: 0, x: 0, y: 0 };
			} else lastTap = { t: now, x: e.clientX, y: e.clientY };
		}
		apply(v);
	};
	const onKey = (e: KeyboardEvent) => {
		const { cx, cy } = centre();
		const k = e.key;
		if (k === '+' || k === '=') zoomAt(1.25, cx, cy);
		else if (k === '-' || k === '_') zoomAt(1 / 1.25, cx, cy);
		else if (k === '0') apply({ ...IDENTITY });
		else if (v.s > MIN_SCALE && k.startsWith('Arrow')) {
			const dx = k === 'ArrowLeft' ? KEY_PAN_PX : k === 'ArrowRight' ? -KEY_PAN_PX : 0;
			const dy = k === 'ArrowUp' ? KEY_PAN_PX : k === 'ArrowDown' ? -KEY_PAN_PX : 0;
			apply({ s: v.s, x: v.x + dx, y: v.y + dy });
		} else return;
		e.preventDefault();
	};

	container.addEventListener('wheel', onWheel, { passive: false });
	container.addEventListener('pointerdown', onDown);
	container.addEventListener('pointermove', onMove);
	container.addEventListener('pointerup', onUp);
	container.addEventListener('pointercancel', onUp);
	container.addEventListener('keydown', onKey);

	return {
		reset() {
			ptrs.clear();
			pinch = null;
			dragged = false;
			apply({ ...IDENTITY });
		},
		/** True when the pointer sequence that just ended moved the image. */
		wasDrag: () => dragged,
		/** True when screen point (x, y) falls on the image as currently drawn. */
		onTarget(x: number, y: number) {
			const r = target.getBoundingClientRect();
			return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
		},
		destroy() {
			container.removeEventListener('wheel', onWheel);
			container.removeEventListener('pointerdown', onDown);
			container.removeEventListener('pointermove', onMove);
			container.removeEventListener('pointerup', onUp);
			container.removeEventListener('pointercancel', onUp);
			container.removeEventListener('keydown', onKey);
		}
	};
}
