// Accessibility smoke tests — axe-core in a real browser.
//
// Gates on SERIOUS and CRITICAL WCAG 2.0/2.1 A/AA violations (the actionable
// tier). Moderate/minor issues are printed for visibility but do not fail the
// run, to keep the smoke test stable. This is the automated half of the a11y
// release gate; the manual NVDA/VoiceOver + keyboard pass is tracked separately
// in docs/ACCESSIBILITY.md and remains a human sign-off.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const WCAG = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'];
const GATE = new Set(['serious', 'critical']);

async function settle(page: import('@playwright/test').Page, route: string) {
	await page.goto(route, { waitUntil: 'domcontentloaded' });
	// Let i18n hydrate and (on /explorer) the deck.gl canvas mount.
	await page.waitForTimeout(2500);
}

function report(violations: Awaited<ReturnType<AxeBuilder['analyze']>>['violations']) {
	const gating = violations.filter((v) => GATE.has(v.impact ?? ''));
	const other = violations.filter((v) => !GATE.has(v.impact ?? ''));
	if (other.length) {
		console.info(
			'[a11y] non-gating issues:\n' +
				other.map((v) => `  ${v.impact} ${v.id} (${v.nodes.length}): ${v.help}`).join('\n')
		);
	}
	return gating;
}

// /explorer/text is the screen-reader shadow site; / is the report; /explorer is
// the deck.gl map.
for (const route of ['/', '/explorer', '/explorer/text']) {
	test(`a11y: ${route} — no serious/critical violations`, async ({ page }) => {
		await settle(page, route);
		const { violations } = await new AxeBuilder({ page }).withTags(WCAG).analyze();
		const gating = report(violations);
		expect(
			gating,
			`axe serious/critical on ${route}:\n` +
				gating.map((v) => `  ${v.impact} ${v.id} (${v.nodes.length}): ${v.help}`).join('\n')
		).toEqual([]);
	});
}

// RTL path: the Arabic report sets dir="rtl"; confirm it stays clean.
test('a11y: report in Arabic (RTL) — no serious/critical violations', async ({ page }) => {
	await page.addInitScript(() => localStorage.setItem('audit_lang', 'ar'));
	await settle(page, '/');
	const { violations } = await new AxeBuilder({ page }).withTags(WCAG).analyze();
	const gating = report(violations);
	expect(
		gating,
		`axe serious/critical on / (ar):\n` +
			gating.map((v) => `  ${v.impact} ${v.id} (${v.nodes.length}): ${v.help}`).join('\n')
	).toEqual([]);
});
