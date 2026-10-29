// Alberta Electoral Boundary Audit — rasterize-figures build script
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
// Renders each deployed article figure in docs/images/*.svg to a WebP and a
// JPEG sibling. The main page serves them through <picture>: the WebP <source>
// is listed first, so WebP-capable browsers fetch only the WebP and older ones
// fall back to the JPEG. The SVGs stay in docs/images/ as the source of truth.
// Run after `npm run copy-figures`; before `npm run build`.
//
// Uses the Chromium that ships with @playwright/test (already a devDependency)
// for both rendering and encoding — no image library needed. Set
// CHROMIUM_PATH to point at a different Chromium binary if the bundled one is
// not installed (e.g. CHROMIUM_PATH=/opt/pw-browsers/chromium).
import { readFileSync, writeFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { chromium } from '@playwright/test';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dir = resolve(__dirname, '../../docs/images');

// Figure → its on-page CSS width (the width attribute in +page.svelte).
// Rasters are rendered at 2× that width so they stay sharp on high-DPI
// screens. Keep in sync with copy-figures.mjs DEPLOYED_FIGURES.
const FIGURES = {
	lane1_dotplot: 463,
	lane2_bars: 441,
	stakes_quadrant: 474,
	figure_airdrie_v3: 504
};
const SCALE = 2;
// The figures' baked-in paper colour (matches .chart-img background), so any
// transparent pixels flatten to the same sheet in the JPEG.
const PAPER = '#f9f7f2';
const WEBP_QUALITY = 0.9;
const JPEG_QUALITY = 0.88;

const browser = await chromium.launch(
	process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}
);
const page = await browser.newPage();

for (const [name, cssWidth] of Object.entries(FIGURES)) {
	const svg = readFileSync(resolve(dir, `${name}.svg`), 'utf8');
	const out = await page.evaluate(
		async ({ svg, width, paper, qWebp, qJpeg }) => {
			const img = new Image();
			img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
			await img.decode();
			const vb = new DOMParser()
				.parseFromString(svg, 'image/svg+xml')
				.documentElement.getAttribute('viewBox')
				.split(/[\s,]+/)
				.map(Number);
			const height = Math.round((width * vb[3]) / vb[2]);
			const canvas = document.createElement('canvas');
			canvas.width = width;
			canvas.height = height;
			const ctx = canvas.getContext('2d');
			ctx.fillStyle = paper;
			ctx.fillRect(0, 0, width, height);
			ctx.drawImage(img, 0, 0, width, height);
			return {
				height,
				webp: canvas.toDataURL('image/webp', qWebp),
				jpeg: canvas.toDataURL('image/jpeg', qJpeg)
			};
		},
		{ svg, width: cssWidth * SCALE, paper: PAPER, qWebp: WEBP_QUALITY, qJpeg: JPEG_QUALITY }
	);
	if (!out.webp.startsWith('data:image/webp')) {
		throw new Error(`${name}: this Chromium cannot encode WebP`);
	}
	for (const [ext, url] of [['webp', out.webp], ['jpg', out.jpeg]]) {
		const buf = Buffer.from(url.slice(url.indexOf(',') + 1), 'base64');
		writeFileSync(resolve(dir, `${name}.${ext}`), buf);
		console.log(`${name}.${ext}  ${cssWidth * SCALE}×${out.height}  ${(buf.length / 1024).toFixed(0)} KB`);
	}
}

await browser.close();
