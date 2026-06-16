<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<svelte:head><title>Methods — Alberta Electoral Boundary Audit</title></svelte:head>

<main class="route-stub container">
	<h1>{t(lang.current, 'nav.route_methods')}</h1>
	<p class="stub-note">This section is being written. It will explain how the maps were tested and how to reproduce the result.</p>
	<section id="ensemble"></section>
	<section id="efficiency-gap"></section>
	<section id="mean-median"></section>
	<section id="declination"></section>
	<section id="seats-50-50"></section>
</main>

<style>
	.route-stub { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
	.stub-note { color: var(--text-muted, #666); font-style: italic; }
</style>
