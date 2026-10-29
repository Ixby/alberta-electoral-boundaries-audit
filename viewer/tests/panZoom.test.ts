import { describe, it, expect } from 'vitest';
import { zoomAbout, pinchStep, clamp, toCss, IDENTITY, MAX_SCALE, type View } from '../src/lib/panZoom';

// Screen position of image point q under view v, container centre c
// (transform-origin at the centre): p = c + t + s·(q − c).
const screen = (v: View, qx: number, qy: number, cx: number, cy: number) => ({
	x: cx + v.x + v.s * (qx - cx),
	y: cy + v.y + v.s * (qy - cy)
});
// Inverse: the image point under screen point p.
const local = (v: View, px: number, py: number, cx: number, cy: number) => ({
	x: cx + (px - cx - v.x) / v.s,
	y: cy + (py - cy - v.y) / v.s
});

describe('zoomAbout', () => {
	it('keeps the point under the cursor fixed', () => {
		const v0: View = { s: 1.5, x: 30, y: -20 };
		const q = local(v0, 700, 200, 500, 400);
		const v1 = zoomAbout(v0, 2, 700, 200, 500, 400);
		const p = screen(v1, q.x, q.y, 500, 400);
		expect(p.x).toBeCloseTo(700, 9);
		expect(p.y).toBeCloseTo(200, 9);
		expect(v1.s).toBe(3);
	});
	it('clamps to the scale limits and resets translation at 1×', () => {
		expect(zoomAbout({ s: 6, x: 0, y: 0 }, 10, 0, 0, 0, 0).s).toBe(MAX_SCALE);
		expect(zoomAbout({ s: 1.2, x: 40, y: 40 }, 0.1, 10, 10, 0, 0)).toEqual(IDENTITY);
	});
});

describe('pinchStep', () => {
	it('keeps the content under the fingers under the fingers', () => {
		const v0: View = { s: 2, x: 10, y: 15 };
		const from = { mx: 400, my: 300, d: 100 };
		const to = { mx: 450, my: 320, d: 150 }; // spread and slide
		const q = local(v0, from.mx, from.my, 500, 400);
		const v1 = pinchStep(v0, from, to, 500, 400);
		const p = screen(v1, q.x, q.y, 500, 400);
		expect(v1.s).toBeCloseTo(3, 9);
		expect(p.x).toBeCloseTo(to.mx, 9);
		expect(p.y).toBeCloseTo(to.my, 9);
	});
	it('ignores a zero-length starting pinch', () => {
		const v0: View = { s: 2, x: 1, y: 2 };
		expect(pinchStep(v0, { mx: 0, my: 0, d: 0 }, { mx: 5, my: 5, d: 50 }, 0, 0)).toBe(v0);
	});
});

describe('clamp', () => {
	it('pins an unzoomed image to the centre', () => {
		expect(clamp({ s: 1, x: 80, y: -80 }, 400, 300)).toEqual(IDENTITY);
	});
	it('stops a zoomed image from being dragged off screen', () => {
		expect(clamp({ s: 2, x: 9999, y: -9999 }, 400, 300)).toEqual({ s: 2, x: 400, y: -300 });
	});
});

describe('toCss', () => {
	it('clears the transform at rest and writes translate-then-scale otherwise', () => {
		expect(toCss(IDENTITY)).toBe('');
		expect(toCss({ s: 2, x: 5, y: -3 })).toBe('translate(5px, -3px) scale(2)');
	});
});
