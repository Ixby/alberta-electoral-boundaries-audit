// Vitest config for the viewer.
// Tests live in viewer/tests/ and target pure-logic modules in src/lib/.
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	test: {
		include: ['tests/**/*.test.ts'],
		environment: 'node',
		globals: false,
		coverage: {
			provider: 'v8',
			include: ['src/lib/**/*.ts'],
			exclude: ['src/lib/**/*.d.ts', 'src/lib/i18n/locales/**']
		}
	}
});
