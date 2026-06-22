<!--
  Alberta Electoral Boundary Audit — root layout
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  https://ixby.github.io
-->
<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { base } from '$app/paths';
	import { lang, LANG_LABELS } from '$lib/i18n/store.svelte';
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
	// search engines see absolute alternates.
	const canonicalBase: string = import.meta.env.VITE_CANONICAL_URL ?? '';
	// hreflang href base: prefer the absolute canonical origin; otherwise fall
	// back to the app's base path so the strict prerender never sees a base-less
	// absolute URL (a bare "/" fails "does not begin with base").
	const altBase: string = canonicalBase || base;
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<!-- Tell search engines which language variant each query-param URL serves -->
	<link rel="alternate" hreflang="en" href="{altBase}/?lang=en" />
	<link rel="alternate" hreflang="fr-CA" href="{altBase}/?lang=fr" />
	<link rel="alternate" hreflang="es" href="{altBase}/?lang=es" />
	<link rel="alternate" hreflang="ar" href="{altBase}/?lang=ar" />
	<link rel="alternate" hreflang="de" href="{altBase}/?lang=de" />
	<link rel="alternate" hreflang="uk" href="{altBase}/?lang=uk" />
	<link rel="alternate" hreflang="tl" href="{altBase}/?lang=tl" />
	<link rel="alternate" hreflang="pa" href="{altBase}/?lang=pa" />
	<link rel="alternate" hreflang="zh-Hans" href="{altBase}/?lang=zh-Hans" />
	<link rel="alternate" hreflang="zh-Hant" href="{altBase}/?lang=zh-Hant" />
	<link rel="alternate" hreflang="hi" href="{altBase}/?lang=hi" />
	<link rel="alternate" hreflang="vi" href="{altBase}/?lang=vi" />
	<link rel="alternate" hreflang="ko" href="{altBase}/?lang=ko" />
	<link rel="alternate" hreflang="ur" href="{altBase}/?lang=ur" />
	<link rel="alternate" hreflang="pl" href="{altBase}/?lang=pl" />
	<link rel="alternate" hreflang="x-default" href="{altBase}/" />
</svelte:head>

<div class="app-shell">
	<TranslationDisclaimer />

	{@render children()}
</div>

<style>
	/* Desktop max width: box the whole page (sticky nav, hero band, reading
	   column) into one centered shell so ultra-wide monitors get margins on
	   both sides instead of edge-to-edge content. The reading column keeps its
	   own 720px cap inside this. Fixed overlays — the fullscreen map explorer,
	   modals, back-to-top — are position:fixed and stay viewport-bound, since
	   .app-shell sets no transform/filter/contain and so forms no containing
	   block for them. */
	.app-shell {
		max-width: 1200px;
		margin-inline: auto;
		box-sizing: border-box;
		/* Repaint the content background over the darker --shell-outer that
		   the body paints behind the surround. */
		background: var(--bg);
	}
	/* Only frame the shell once there's an actual surround to frame against
	   (viewport wider than the shell). Below this, the shell fills the screen
	   and a border/shadow would just hug the edges. */
	@media (min-width: 1240px) {
		.app-shell {
			border: 1px solid var(--shell-frame);
			box-shadow: 0 0 60px rgba(15, 23, 42, 0.16);
		}
	}
</style>

