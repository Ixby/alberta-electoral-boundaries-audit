<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<svelte:head><title>Law — Alberta Electoral Boundary Audit</title></svelte:head>

<main class="route-stub container">
	<h1>{t(lang.current, 'nav.route_law')}</h1>
	<p class="stub-note">This section is being written. It will cover what the law asks of an electoral map and how this audit relates to it.</p>
	<section id="why-not-gerrymander"></section>
	<section id="effective-representation"></section>
	<section id="ebca"></section>
</main>

<style>
	.route-stub { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
	.stub-note { color: var(--text-muted, #666); font-style: italic; }
</style>
