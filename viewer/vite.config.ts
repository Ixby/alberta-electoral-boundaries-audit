import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { createReadStream, existsSync } from 'fs';
import { resolve, extname } from 'path';

// docs/ lives one level above viewer/
const docsDir = resolve(process.cwd(), '../docs');

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
				const stripped = raw.split('?')[0].replace(/^\/[^/]+(?=\/)/, '');
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
	build: {
		// docs/images/ (~108MB SVGs) must survive every build — never wipe docs/
		emptyOutDir: false
	}
});
