import { defineConfig, devices } from '@playwright/test';

// Accessibility smoke tests (axe-core) live in tests/a11y/*.spec.ts and run in a
// real browser against the dev server. Separate from the vitest suite (which
// only collects tests/**/*.test.ts). Firefox is the installed Playwright browser.
//
// Pin everything to 127.0.0.1 (not "localhost"): on Windows, localhost can
// resolve to ::1 while Vite binds to 127.0.0.1, which makes Firefox fail with
// NS_ERROR_CONNECTION_REFUSED even though the server is up.
const HOST = '127.0.0.1';
const PORT = 4180;
const BASE = `http://${HOST}:${PORT}`;

export default defineConfig({
	testDir: 'tests/a11y',
	testMatch: '**/*.spec.ts',
	fullyParallel: false,
	workers: 1,
	reporter: 'list',
	timeout: 90_000,
	use: {
		baseURL: BASE,
		// deck.gl WebGL needs a real GL context; Firefox honours this flag.
		launchOptions: { firefoxUserPrefs: { 'webgl.force-enabled': true } },
	},
	projects: [{ name: 'firefox', use: { ...devices['Desktop Firefox'] } }],
	// Test the production build via `vite preview` (served at root): the dev
	// server crashes server-side on the deck.gl /explorer route, and preview is
	// what users actually get. Requires `npm run build` first (CI builds before
	// running this; locally, build then `npm run test:a11y`).
	webServer: {
		command: `npm run preview -- --port ${PORT} --strictPort --host ${HOST}`,
		url: BASE,
		reuseExistingServer: !process.env.CI,
		timeout: 120_000,
	},
});
