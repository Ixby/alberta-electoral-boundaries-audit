// Alberta Electoral Boundary Audit — copy-figures build script
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
// Syncs generated article figures from data/maps/article/ into docs/images/.
// Run after regenerating Python figure scripts; before npm run build.
import { cpSync, existsSync, readdirSync } from 'fs';
import { resolve, dirname, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = resolve(__dirname, '../../data/maps/article');
const dst = resolve(__dirname, '../../docs/images');

if (!existsSync(src)) {
	console.error(`Source not found: ${src}`);
	process.exit(1);
}

// Explicit allowlist (2026-07-09): the old *.svg glob redeployed every figure in
// data/maps/article/, including orphans from retired article drafts. The
// link audit found figure_{calgary,lethbridge,reddeer}_v3.svg and
// bias_structure_matrix.svg referenced by no page while still shipping stale
// content to docs/images/. Only figures actually embedded by the viewer or
// report_public.html get deployed; add a name here when a page starts using it.
const DEPLOYED_FIGURES = new Set([
	'lane1_dotplot.svg',
	'lane2_bars.svg',
	'stakes_quadrant.svg',
	'figure_airdrie_v3.svg'
]);

let copied = 0;
for (const f of readdirSync(src)) {
	if (extname(f) === '.svg' && DEPLOYED_FIGURES.has(f)) {
		cpSync(resolve(src, f), resolve(dst, f));
		copied++;
	}
}
if (copied !== DEPLOYED_FIGURES.size) {
	console.error(`Expected ${DEPLOYED_FIGURES.size} allowlisted figures, copied ${copied} — check data/maps/article/`);
	process.exit(1);
}
console.log(`Copied ${copied} allowlisted SVG(s) from data/maps/article/ → docs/images/`);
