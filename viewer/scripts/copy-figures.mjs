// Syncs generated article figures from data/maps/article/ into docs/images/.
// Run after regenerating Python figure scripts; before npm run build.
import { cpSync, existsSync, readdirSync } from 'fs';
import { resolve, dirname, extname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = resolve(__dirname, '../../../data/maps/article');
const dst = resolve(__dirname, '../../docs/images');

if (!existsSync(src)) {
	console.error(`Source not found: ${src}`);
	process.exit(1);
}

let copied = 0;
for (const f of readdirSync(src)) {
	if (extname(f) === '.svg') {
		cpSync(resolve(src, f), resolve(dst, f));
		copied++;
	}
}
console.log(`Copied ${copied} SVG(s) from data/maps/article/ → docs/images/`);
