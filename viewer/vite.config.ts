import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	build: {
		// docs/images/ (~108MB SVGs) must survive every build — never wipe docs/
		emptyOutDir: false
	}
});
