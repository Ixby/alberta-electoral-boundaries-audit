<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import { lang, LANG_LABELS } from '$lib/i18n/store.svelte';
	import LanguageSelector from '$lib/components/LanguageSelector.svelte';
	import TranslationDisclaimer from '$lib/components/TranslationDisclaimer.svelte';

	let { children } = $props();

	// Keep <html lang="..."> in sync with the active language so screen readers
	// announce pronunciation correctly and search engines see the right locale.
	$effect(() => {
		if (typeof document === 'undefined') return;
		document.documentElement.lang = LANG_LABELS[lang.current].htmlLang;
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
	<link rel="alternate" hreflang="tl" href="{canonicalBase}/?lang=tl" />
	<link rel="alternate" hreflang="pa" href="{canonicalBase}/?lang=pa" />
	<link rel="alternate" hreflang="zh-Hans" href="{canonicalBase}/?lang=zh-Hans" />
	<link rel="alternate" hreflang="zh-Hant" href="{canonicalBase}/?lang=zh-Hant" />
	<link rel="alternate" hreflang="x-default" href="{canonicalBase}/" />
</svelte:head>

<TranslationDisclaimer />

<div class="lang-selector-anchor">
	<LanguageSelector />
</div>

{@render children()}

<style>
	.lang-selector-anchor {
		position: fixed;
		top: 0.75rem;
		right: 0.75rem;
		z-index: 100;
	}
</style>
