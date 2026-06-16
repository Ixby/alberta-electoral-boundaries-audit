<!--
  Alberta Electoral Boundary Audit — root layout
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  https://ixby.github.io
-->
<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/state';
	import { lang, LANG_LABELS } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import TranslationDisclaimer from '$lib/components/TranslationDisclaimer.svelte';

	let { children } = $props();

	// Keep <html lang="..."> in sync with the active language so screen readers
	// announce pronunciation correctly and search engines see the right locale.
	$effect(() => {
		if (typeof document === 'undefined') return;
		document.documentElement.lang = LANG_LABELS[lang.current].htmlLang;
		// Arabic is the site's first RTL locale. Document-level dir mirrors
		// the prose correctly (flex layouts flip automatically); the map
		// explorer HUD uses physical left/right offsets and keeps LTR
		// quirks under RTL until a dedicated pass.
		document.documentElement.dir = LANG_LABELS[lang.current].dir;
	});

	// Canonical origin for hreflang annotations. Set VITE_CANONICAL_URL at build
	// time (e.g. "https://ixby.github.io/alberta-electoral-boundaries-audit") so
	// search engines see absolute alternates. Falls back to relative URLs.
	const canonicalBase: string = import.meta.env.VITE_CANONICAL_URL ?? '';
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<!-- Tell search engines which language variant each query-param URL serves -->
	<link rel="alternate" hreflang="en" href="{canonicalBase}/?lang=en" />
	<link rel="alternate" hreflang="fr-CA" href="{canonicalBase}/?lang=fr" />
	<link rel="alternate" hreflang="es" href="{canonicalBase}/?lang=es" />
	<link rel="alternate" hreflang="ar" href="{canonicalBase}/?lang=ar" />
	<link rel="alternate" hreflang="de" href="{canonicalBase}/?lang=de" />
	<link rel="alternate" hreflang="uk" href="{canonicalBase}/?lang=uk" />
	<link rel="alternate" hreflang="tl" href="{canonicalBase}/?lang=tl" />
	<link rel="alternate" hreflang="pa" href="{canonicalBase}/?lang=pa" />
	<link rel="alternate" hreflang="zh-Hans" href="{canonicalBase}/?lang=zh-Hans" />
	<link rel="alternate" hreflang="zh-Hant" href="{canonicalBase}/?lang=zh-Hant" />
	<link rel="alternate" hreflang="hi" href="{canonicalBase}/?lang=hi" />
	<link rel="alternate" hreflang="vi" href="{canonicalBase}/?lang=vi" />
	<link rel="alternate" hreflang="ko" href="{canonicalBase}/?lang=ko" />
	<link rel="alternate" hreflang="ur" href="{canonicalBase}/?lang=ur" />
	<link rel="alternate" hreflang="pl" href="{canonicalBase}/?lang=pl" />
	<link rel="alternate" hreflang="x-default" href="{canonicalBase}/" />
</svelte:head>

<nav class="route-nav" aria-label="Site sections">
	<a class="route-pill" class:active={page.url.pathname === '/'} href="/">{t(lang.current, 'nav.route_story')}</a>
	<a class="route-pill" class:active={page.url.pathname.startsWith('/law')} href="/law">{t(lang.current, 'nav.route_law')}</a>
	<a class="route-pill" class:active={page.url.pathname.startsWith('/methods')} href="/methods">{t(lang.current, 'nav.route_methods')}</a>
</nav>

<TranslationDisclaimer />

{@render children()}

<style>
	/* Foundation scaffold: a static top bar so it never fights the page's own
	   sticky in-page nav on `/`. The rewrite (Plan 2) unifies navigation. */
	.route-nav {
		display: flex;
		gap: 0.4rem;
		justify-content: center;
		padding: 0.45rem 0.6rem;
		background: var(--bg, #fff);
		border-bottom: 1px solid rgba(127, 127, 127, 0.18);
	}
	.route-pill {
		font-size: 0.85rem;
		font-weight: 600;
		padding: 0.25rem 0.9rem;
		border-radius: 999px;
		text-decoration: none;
		color: var(--text-muted, #555);
		border: 1px solid transparent;
	}
	.route-pill:hover {
		color: var(--text, #111);
	}
	.route-pill.active {
		color: var(--text, #111);
		border-color: rgba(127, 127, 127, 0.4);
		background: rgba(127, 127, 127, 0.08);
	}
	.route-pill:focus-visible {
		outline: 2px solid var(--link, #2b5ba1);
		outline-offset: 2px;
	}
</style>
