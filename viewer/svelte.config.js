import adapter from '@sveltejs/adapter-static';
import { execFileSync } from 'node:child_process';

// App version = the git commit the bundle was built from. This mirrors the data
// pipeline's content-hash version (manifest.json), so the HUD/analytics app_ver
// is a real, verifiable identifier rather than a hand-bumped constant. Falls back
// to 'dev' when there's no git checkout (e.g. a tarball build). execFileSync with
// a fixed arg array — no shell, no interpolation.
let appVersion = 'dev';
try {
	appVersion = execFileSync('git', ['rev-parse', '--short=12', 'HEAD'], {
		stdio: ['ignore', 'pipe', 'ignore']
	})
		.toString()
		.trim();
} catch {
	// not a git checkout — keep 'dev'
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
	},
	kit: {
		version: { name: appVersion },
		prerender: {
			// docs/images/ exists at runtime but not in viewer/static/ — suppress prerender 404s for them
			handleHttpError: ({ path, message }) => {
				if (path.includes('/images/')) return;
				throw new Error(message);
			}
		},
		adapter: adapter({
			// Build to viewer/build/ — a postbuild script merges into docs/ without wiping docs/images/
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		paths: {
			base: process.env.VITE_BASE ?? ''
		}
	}
};

export default config;
