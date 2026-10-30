<!--
  Alberta Electoral Boundary Audit — site header, shared by every page (+layout.svelte)
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Row 1 (every page): home, the site's pages, language, theme, menu. Row 2, the
  previous / current / next section stepper, appears only while a page has
  registered sections in $lib/sectionNav (the main page). The stepper hangs
  just below row 1 instead of growing the header, because pages register after
  hydration: a growing header would shove the page down on load. The main page
  reserves that strip in its hero.

  Publishes --site-header-h (bar height, stepper included) and
  --site-header-bottom (bar bottom edge in the viewport) on <html>, so anchors
  clear the sticky bar and the explorer's fixed map starts beneath it.
-->
<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import { afterNavigate } from '$app/navigation';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import LanguageSelector from './LanguageSelector.svelte';
	import { focusTrap } from '$lib/a11y/focusTrap';
	import { getStoredTheme, storeTheme } from '$lib/prefs';
	import { sectionNav } from '$lib/sectionNav.svelte';

	// bar: short label on the bar; drawer: the fuller label in the menu.
	const PAGES: { path: string; bar: string; drawer: string }[] = [
		{ path: '/evidence', bar: 'bar_evidence', drawer: 'evidence' },
		{ path: '/explorer', bar: 'bar_explorer', drawer: 'bar_explorer' },
		{ path: '/law', bar: 'route_law', drawer: 'route_law' },
		{ path: '/norms', bar: 'bar_norms', drawer: 'bar_norms' },
		{ path: '/methods', bar: 'route_methods', drawer: 'route_methods' },
		{ path: '/explainers', bar: 'bar_explainers', drawer: 'explainers' },
		{ path: '/fixes', bar: 'bar_fixes', drawer: 'fixes' },
		{ path: '/feedback', bar: 'bar_feedback', drawer: 'feedback' }
	];

	let navOpen = $state(false);
	let navScrolled = $state(false);
	let darkMode = $state(false);
	let headerEl: HTMLElement;

	// Route id ('/', '/evidence', '/explorer/text', …) is independent of the
	// deploy base path, unlike location.pathname.
	const here = $derived(page.route.id ?? '/');
	const sections = $derived(sectionNav.sections);
	const cur = $derived(Math.min(sectionNav.current, Math.max(0, sections.length - 1)));
	const isHere = (path: string) => here === path || here.startsWith(path + '/');

	function toggleTheme() {
		darkMode = !darkMode;
		document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
		storeTheme(darkMode ? 'dark' : 'light');
	}
	function toggleNavDrawer() {
		navOpen = !navOpen;
	}
	function closeNavDrawer() {
		navOpen = false;
	}

	function publish() {
		if (!headerEl) return;
		const bar = headerEl.getBoundingClientRect();
		const step = headerEl.querySelector('.section-bar')?.getBoundingClientRect();
		const bottom = step && step.height ? step.bottom : bar.bottom;
		const root = document.documentElement.style;
		root.setProperty('--site-header-h', Math.round(bottom - bar.top) + 'px');
		root.setProperty('--site-header-bottom', Math.round(Math.max(bottom, 0)) + 'px');
	}

	afterNavigate(() => {
		navOpen = false;
		requestAnimationFrame(publish);
	});

	// Re-measure when the stepper appears or goes away.
	$effect(() => {
		void sections.length;
		requestAnimationFrame(publish);
	});

	onMount(() => {
		// Dark mode: respects the OS preference; a user override is persisted.
		// app.html's inline script already set the attribute to avoid a flash;
		// this only syncs the toggle's state.
		getStoredTheme().then((stored) => {
			const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
			darkMode = stored === 'dark' || (stored === null && prefersDark);
		});

		const onScroll = () => {
			navScrolled = window.scrollY > 8;
			publish();
		};
		onScroll();
		window.addEventListener('scroll', onScroll, { passive: true });
		window.addEventListener('resize', publish);
		const ro = new ResizeObserver(publish);
		ro.observe(headerEl);
		return () => {
			window.removeEventListener('scroll', onScroll);
			window.removeEventListener('resize', publish);
			ro.disconnect();
		};
	});
</script>

<a class="skip-link" href="#main">{t(lang.current, 'nav.skip_to_content')}</a>

<header class="site-header" class:scrolled={navScrolled} class:open={navOpen} bind:this={headerEl}>
	<nav class="site-bar" aria-label={t(lang.current, 'nav.bar_aria')}>
		<div class="nav-inner">
			<a href="{base}/" class="nav-home" aria-label={t(lang.current, 'nav.bar_home')} title={t(lang.current, 'nav.bar_home')} aria-current={here === '/' ? 'page' : undefined}><svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 2L2 9h2v9h5v-5h2v5h5V9h2L10 2z"/></svg></a>
			<ul class="nav-pages">
				{#each PAGES as p (p.path)}
					<li><a href="{base}{p.path}" aria-current={isHere(p.path) ? 'page' : undefined}>{t(lang.current, 'nav.' + p.bar)}</a></li>
				{/each}
			</ul>
			<div class="nav-tools">
				<LanguageSelector />
				<button id="theme-toggle" class="nav-theme-btn" aria-label={t(lang.current, 'nav.theme_aria')} title={t(lang.current, 'nav.theme_title')} onclick={toggleTheme}>
					<svg class="icon-sun" width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-9a1 1 0 0 0 1-1V2a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm0 14a1 1 0 0 0 1-1v-1a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm7-7a1 1 0 0 0 0-2h-1a1 1 0 0 0 0 2h1zM4 10a1 1 0 0 0-1-1H2a1 1 0 0 0 0 2h1a1 1 0 0 0 1-1zm10.95-4.95a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm-9.9 9.9a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm9.9.01a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71zm-9.9-9.9a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71z"/></svg>
					<svg class="icon-moon" width="14" height="14" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M17.293 13.293A8 8 0 0 1 6.707 2.707a8.001 8.001 0 1 0 10.586 10.586z"/></svg>
				</button>
				<button id="hamburger" class="nav-hamburger" aria-label={t(lang.current, 'nav.nav_aria')} aria-expanded={navOpen} aria-controls="nav-drawer" onclick={toggleNavDrawer}>
					<svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor" aria-hidden="true">
						{#if navOpen}
							<path d="M2 2l14 14M2 16L16 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/>
						{:else}
							<rect y="2" width="18" height="2" rx="1"/>
							<rect y="8" width="18" height="2" rx="1"/>
							<rect y="14" width="18" height="2" rx="1"/>
						{/if}
					</svg>
				</button>
			</div>
		</div>
	</nav>

	{#if sections.length}
		<nav class="section-bar" aria-label={t(lang.current, 'nav.group_this_page')}>
			<div class="nav-landmarks">
				{#if cur > 0}
					<a class="nav-step nav-prev" href={'#' + sections[cur - 1].id} title={t(lang.current, 'nav.' + sections[cur - 1].key)}>
						<span class="nav-chev" aria-hidden="true">‹</span><span class="nav-step-lbl">{t(lang.current, 'nav.' + sections[cur - 1].key)}</span>
					</a>
				{:else}
					<span class="nav-step nav-edge" aria-hidden="true"></span>
				{/if}
				<span class="nav-step nav-current" aria-current="location">{t(lang.current, 'nav.' + sections[cur].key)}</span>
				{#if cur < sections.length - 1}
					<a class="nav-step nav-next" href={'#' + sections[cur + 1].id} title={t(lang.current, 'nav.' + sections[cur + 1].key)}>
						<span class="nav-step-lbl">{t(lang.current, 'nav.' + sections[cur + 1].key)}</span><span class="nav-chev" aria-hidden="true">›</span>
					</a>
				{:else}
					<span class="nav-step nav-edge" aria-hidden="true"></span>
				{/if}
			</div>
		</nav>
	{/if}

	{#if navOpen}
		<div id="nav-drawer" role="dialog" aria-modal="true" aria-label={t(lang.current, 'nav.nav_aria')} use:focusTrap={{ onEscape: () => (navOpen = false) }}>
			{#if sections.length}
				<a href="#top" class="drawer-top" onclick={closeNavDrawer}>{t(lang.current, 'nav.drawer_top')}</a>
				<h4 class="drawer-group">{t(lang.current, 'nav.group_this_page')}</h4>
				{#each sections as s (s.id)}
					<a href={'#' + s.id} onclick={closeNavDrawer}>{t(lang.current, 'nav.' + s.key)}</a>
				{/each}
			{/if}
			<h4 class="drawer-group">{t(lang.current, 'nav.group_pages')}</h4>
			<a href="{base}/" aria-current={here === '/' ? 'page' : undefined} onclick={closeNavDrawer}>{t(lang.current, 'nav.bar_home')}</a>
			{#each PAGES as p (p.path)}
				<a href="{base}{p.path}" aria-current={isHere(p.path) ? 'page' : undefined} onclick={closeNavDrawer}>{t(lang.current, 'nav.' + p.drawer)}</a>
			{/each}
		</div>
	{/if}
</header>

<style>
	/* Bar colours match the main page's --nav-bg / --nav-accent tokens. Those
	   tokens are declared by the main page only, so the header carries its own. */
	.site-header {
		--hdr-bg: #1e3552;
		--hdr-accent: #6fd3fb;
		position: sticky;
		top: 0;
		/* Above the explorer's fixed map (z 9000) so the menu and the language
		   list open over it; the figure lightbox sits above this. */
		z-index: 9100;
		background: var(--hdr-bg);
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
		line-height: 1.65;
		transition: box-shadow 0.18s ease;
	}
	:global(:root[data-theme='dark']) .site-header {
		--hdr-bg: #1a1e2d;
		--hdr-accent: #4fc3f7;
	}
	.site-header * {
		box-sizing: border-box;
	}
	.site-header.scrolled {
		box-shadow: 0 2px 14px rgba(0, 0, 0, 0.28);
	}
	:global(:root[data-theme='dark']) .site-header.scrolled {
		box-shadow: 0 2px 14px rgba(0, 0, 0, 0.55);
	}
	/* Anchor jumps land below the sticky bar on every page. */
	:global(html) {
		scroll-padding-top: calc(var(--site-header-h, 2.75rem) + 0.5rem);
	}
	/* The bar starts at the very top on every page (the main page already resets
	   this; the others kept the browser's 8px body margin). */
	:global(body) {
		margin: 0;
	}
	/* The skip link's target takes focus programmatically; no ring on the box. */
	:global(#main:focus) {
		outline: none;
	}

	.skip-link {
		position: absolute;
		inset-inline-start: 0.5rem;
		top: 0.5rem;
		background: #0a1e36;
		color: #fff;
		padding: 0.55rem 0.95rem;
		border-radius: 4px;
		text-decoration: none;
		font-size: 0.9rem;
		font-weight: 600;
		z-index: 9200;
		transform: translateY(-150%);
		transition: transform 0.15s ease;
	}
	.skip-link:focus,
	.skip-link:focus-visible {
		transform: translateY(0);
		outline: 2px solid #fff;
		outline-offset: 2px;
	}

	.nav-inner {
		display: flex;
		align-items: center;
		gap: 0.3rem;
		padding-block: 0;
		padding-inline-start: max(0.75rem, env(safe-area-inset-left));
		padding-inline-end: max(0.75rem, env(safe-area-inset-right));
		min-height: 2.75rem;
		max-width: 1400px;
		margin: 0 auto;
	}

	.nav-pages {
		flex: 1;
		min-width: 0;
		display: flex;
		align-items: center;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.site-header a {
		color: rgba(255, 255, 255, 0.72);
		text-decoration: none;
		display: inline-flex;
		align-items: center;
		font-size: 0.84rem;
		font-weight: 500;
		letter-spacing: 0.005em;
		min-height: 2.75rem;
		padding: 0 0.7rem;
		white-space: nowrap;
		position: relative;
		transition: color 0.15s ease, background 0.15s ease;
	}
	.site-header a:hover {
		color: #fff;
		background: rgba(255, 255, 255, 0.06);
		text-decoration: none;
	}
	.site-header a:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.55);
		outline-offset: -3px;
		border-radius: 3px;
	}
	.nav-pages a[aria-current='page'] {
		color: #fff;
	}
	.nav-pages a[aria-current='page']::after,
	.nav-current::after {
		content: '';
		position: absolute;
		left: 0.7rem;
		right: 0.7rem;
		bottom: 0;
		height: 2px;
		background: var(--hdr-accent);
		border-radius: 1px;
	}
	.site-header a.nav-home {
		color: rgba(255, 255, 255, 0.55);
		padding: 0 0.65rem 0 0.3rem;
		margin-inline-end: 0.2rem;
		border-inline-end: 1px solid rgba(255, 255, 255, 0.12);
	}
	.site-header a.nav-home:hover,
	.site-header a.nav-home[aria-current='page'] {
		color: #fff;
		background: transparent;
	}

	.nav-tools {
		display: flex;
		align-items: center;
		gap: 0.25rem;
		padding-inline-start: 0.5rem;
		margin-inline-start: auto;
		border-inline-start: 1px solid rgba(255, 255, 255, 0.12);
	}

	/* Section stepper: hangs below row 1 (see the header comment). A 3-column
	   grid keeps the current section centred while the previous and next slots
	   flank it and slide as the reader scrolls. */
	.section-bar {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: var(--hdr-bg);
		border-top: 1px solid rgba(255, 255, 255, 0.06);
	}
	.site-header.scrolled .section-bar {
		box-shadow: 0 2px 14px rgba(0, 0, 0, 0.28);
	}
	.nav-landmarks {
		max-width: 1400px;
		margin: 0 auto;
		padding-inline: max(0.75rem, env(safe-area-inset-left));
		min-width: 0;
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: center;
		gap: 0.3rem;
	}
	.nav-step {
		min-width: 0;
	}
	.nav-step-lbl {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.site-header a.nav-prev {
		justify-self: end;
		color: rgba(255, 255, 255, 0.62);
		max-width: 16rem;
	}
	.site-header a.nav-next {
		justify-self: start;
		color: rgba(255, 255, 255, 0.62);
		max-width: 16rem;
	}
	.nav-prev .nav-step-lbl,
	.nav-next .nav-step-lbl {
		max-width: 13rem;
	}
	.nav-chev {
		opacity: 0.65;
		font-size: 1.15em;
		line-height: 1;
		padding: 0 0.1rem;
	}
	.nav-current {
		justify-self: center;
		display: inline-flex;
		align-items: center;
		min-height: 2.75rem;
		padding: 0 0.7rem;
		color: #fff;
		font-size: 0.9rem;
		font-weight: 600;
		letter-spacing: 0.005em;
		text-align: center;
		max-width: 24rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		position: relative;
	}
	.nav-edge {
		min-width: 0;
	}

	.nav-hamburger:focus-visible,
	.nav-theme-btn:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.55);
		outline-offset: -3px;
		border-radius: 3px;
	}
	.nav-hamburger {
		display: inline-flex;
		background: none;
		border: none;
		cursor: pointer;
		color: rgba(255, 255, 255, 0.72);
		padding: 0 0.45rem;
		min-height: 2.75rem;
		align-items: center;
		justify-content: center;
		border-radius: 4px;
		transition: color 0.15s ease, background 0.15s ease;
	}
	.nav-hamburger:hover {
		color: #fff;
		background: rgba(255, 255, 255, 0.06);
	}
	.nav-hamburger[aria-expanded='true'] {
		color: #fff;
		background: rgba(255, 255, 255, 0.08);
	}
	.nav-theme-btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		background: none;
		border: none;
		cursor: pointer;
		color: #f5c518;
		padding: 0 0.45rem;
		min-height: 2.75rem;
		border-radius: 4px;
		transition: color 0.15s ease, background 0.15s ease;
	}
	.nav-theme-btn:hover {
		color: #fff;
		background: rgba(255, 255, 255, 0.06);
	}
	/* Sun shown (and yellow) in light mode; moon shown (and bright blue) in dark mode */
	.icon-sun {
		display: block;
	}
	.icon-moon {
		display: none;
	}
	:global(:root[data-theme='dark']) .nav-theme-btn {
		color: #4fc3f7;
	}
	:global(:root[data-theme='dark']) .icon-sun {
		display: none;
	}
	:global(:root[data-theme='dark']) .icon-moon {
		display: block;
	}

	#nav-drawer {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		z-index: 1;
		display: flex;
		flex-direction: column;
		background: #15263d;
		border-top: 1px solid rgba(255, 255, 255, 0.06);
		padding: 0.4rem 0 0.8rem;
		max-height: calc(100vh - 2.75rem);
		overflow-y: auto;
		box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
	}
	:global(:root[data-theme='dark']) #nav-drawer {
		background: #131623;
	}
	#nav-drawer a {
		display: block;
		min-height: 0;
		color: rgba(255, 255, 255, 0.82);
		font-size: 0.92rem;
		padding: 0.55rem 1.4rem;
		transition: background 0.12s ease, color 0.12s ease;
	}
	#nav-drawer a:hover {
		background: rgba(255, 255, 255, 0.07);
		color: #fff;
	}
	#nav-drawer a[aria-current='page'] {
		color: #fff;
		font-weight: 600;
	}
	#nav-drawer a.drawer-top {
		color: rgba(255, 255, 255, 0.55);
		font-size: 0.82rem;
		padding: 0.45rem 1.4rem 0.65rem;
		border-bottom: 1px solid rgba(255, 255, 255, 0.06);
		margin-bottom: 0.3rem;
	}
	#nav-drawer .drawer-group {
		margin: 0.7rem 0 0.2rem;
		padding: 0 1.4rem;
		font-size: 0.68rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: rgba(255, 255, 255, 0.42);
	}

	/* The page links fit inline from 960px; below that they live in the menu. */
	@media (max-width: 959px) {
		.nav-pages {
			display: none;
		}
	}
	@media (max-width: 720px) {
		.section-bar {
			display: none;
		}
		.nav-tools {
			border-inline-start: none;
			padding-inline-start: 0;
		}
	}
</style>
