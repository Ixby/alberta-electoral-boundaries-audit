// One-off: rasterize the diagonal "MAP EXPLORER" watermark tile to a transparent
// PNG so the explorer can paint it as a cheap GPU-composited background image
// instead of a live inline-SVG <pattern> (which also couldn't be a CSS background
// because it needs the self-hosted Cinzel webfont — a raster bakes Cinzel into
// pixels). Renders ONE seamless horizontal cell (240x120 at 2x = 480x240); the
// component repeats it and rotates the layer -45deg in CSS.
//
// Run: node scripts/gen-watermark.mjs   (requires a local Chrome)
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, resolve, dirname } from 'node:path';

const FONT = resolve('static/fonts/cinzel-700.woff2');
const OUT = resolve('static/images/watermark-tile.png');
mkdirSync(dirname(OUT), { recursive: true });
const W = 480;
const H = 240; // 2x of the 240x120 SVG pattern cell

const CHROMES = [
	'C:/Program Files/Google/Chrome/Application/chrome.exe',
	'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
];
const chrome = CHROMES.find((p) => existsSync(p));
if (!chrome) throw new Error('No Chrome found');

const b64 = readFileSync(FONT).toString('base64');
// Text geometry mirrors the SVG cell scaled 2x: font 15->30px, letter-spacing
// 3->6px, baseline y 20->40. White text; the component sets layer opacity (0.08).
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Cinzel';font-weight:700;font-style:normal;src:url(data:font/woff2;base64,${b64}) format('woff2');}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px;background:transparent;overflow:hidden}
.cell{position:absolute;left:0;top:0;width:${W}px;height:${H}px}
.cell span{position:absolute;left:0;top:0;width:${W}px;height:${H}px;
  font-family:'Cinzel',serif;font-weight:700;font-size:30px;letter-spacing:6px;
  color:#f0e6d6;white-space:nowrap;line-height:80px;text-indent:0}
</style></head><body><div class="cell"><span>MAP&nbsp;EXPLORER</span></div></body></html>`;

const htmlPath = join(tmpdir(), 'wm.html');
writeFileSync(htmlPath, html);

execFileSync(
	chrome,
	[
		'--headless=new',
		'--disable-gpu',
		'--hide-scrollbars',
		'--force-device-scale-factor=1',
		'--default-background-color=00000000',
		`--window-size=${W},${H}`,
		`--screenshot=${OUT}`,
		'file:///' + htmlPath.replace(/\\/g, '/')
	],
	{ stdio: ['ignore', 'pipe', 'pipe'] }
);
console.log('wrote', OUT);
