// Copies viewer/build/ into docs/ without deleting docs/images/ or other non-Svelte files.
import { cpSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = resolve(__dirname, '../build');
const dst = resolve(__dirname, '../../docs');

if (!existsSync(src)) {
	console.error('build/ not found — run npm run build first');
	process.exit(1);
}

cpSync(src, dst, { recursive: true, force: true });
console.log(`Merged build/ → docs/`);
