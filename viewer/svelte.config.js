import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		runes: ({ filename }) => (filename.split(/[/\\]/).includes('node_modules') ? undefined : true)
	},
	kit: {
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
