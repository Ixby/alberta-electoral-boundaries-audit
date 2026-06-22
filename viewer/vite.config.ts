import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { createReadStream, existsSync } from 'fs';
import { resolve, extname } from 'path';

// docs/ lives one level above viewer/
const docsDir = resolve(process.cwd(), '../docs');
// Strip the SvelteKit base path prefix from incoming URLs before mapping to docs/.
// In dev (VITE_BASE unset), base is '' so no prefix is stripped.
// In production, VITE_BASE = '/alberta-electoral-boundaries-audit' is stripped.
const _devBase = (process.env.VITE_BASE ?? '').replace(/\/$/, '');

const MIME: Record<string, string> = {
	'.json': 'application/json',
	'.svg':  'image/svg+xml',
	'.png':  'image/png',
	'.jpg':  'image/jpeg',
	'.css':  'text/css',
};

// In dev mode, serve docs/ assets so data/ and images/ resolve correctly.
// Production builds write directly into docs/ and don't need this.
function serveDocsAssets(): import('vite').Plugin {
	return {
		name: 'serve-docs-assets',
		configureServer(server) {
			server.middlewares.use((req: any, res: any, next: () => void) => {
				const raw: string = req.url ?? '';
				const path = raw.split('?')[0];
				// Remove the base-path prefix (if any) to get the docs-relative path.
				const stripped = _devBase && path.startsWith(_devBase)
					? path.slice(_devBase.length) || '/'
					: path;
				if (!stripped || stripped === '/') return next();
				const candidate = resolve(docsDir, stripped.replace(/^\//, ''));
				if (existsSync(candidate) && !candidate.endsWith('index.html')) {
					const mime = MIME[extname(candidate)] ?? 'application/octet-stream';
					res.setHeader('Content-Type', mime);
					res.setHeader('Cache-Control', 'no-store');
					createReadStream(candidate).pipe(res);
				} else {
					next();
				}
			});
		},
	};
}

export default defineConfig({
	plugins: [sveltekit(), serveDocsAssets()],
	// Pre-bundle deck.gl at server start so the explorer's dynamic import is instant.
	// Otherwise Vite optimizes these large deps on the FIRST import (the multi-second
	// "lib" time in the explorer's first-paint HUD; production is unaffected — it's a
	// pre-built chunk there).
	optimizeDeps: {
		include: ['@deck.gl/core', '@deck.gl/layers', '@deck.gl/extensions']
	},
	server: {
		// Never watch the adapter-static build output. It contains the multi-MB tile
		// `.bin` files (e.g. build/mapdata/va_10_10.bin ~38MB); vite's file watcher
		// crashes the dev server with EBUSY when one is locked mid-/post-build.
		watch: { ignored: ['**/build/**'] }
	},
	build: {
		// docs/images/ (~108MB SVGs) must survive every build — never wipe docs/
		emptyOutDir: false
	}
});
