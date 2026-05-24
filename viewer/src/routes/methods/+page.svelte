<script lang="ts">
	import { base } from '$app/paths';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<svelte:head>
	<title>{t(lang.current, 'methods.title')}</title>
	<meta name="description" content={t(lang.current, 'methods.lede')} />
</svelte:head>

<main class="container deep-route">
	<a href="{base}/?lang={lang.current}" class="back-link">{t(lang.current, 'methods.back')}</a>
	<h1>{t(lang.current, 'methods.heading')}</h1>
	<p class="lede">{t(lang.current, 'methods.lede')}</p>
	<div class="coming-soon">
		<p>{t(lang.current, 'methods.coming_soon')}</p>
	</div>
</main>

<style>
	.deep-route {
		padding: 2.5rem 1rem 3rem;
		max-width: 720px;
	}
	.back-link {
		display: inline-block;
		margin-bottom: 1.5rem;
		color: var(--link, #1a5276);
		text-decoration: none;
		font-size: 0.95rem;
	}
	.back-link:hover {
		text-decoration: underline;
	}
	h1 {
		font-size: 1.8rem;
		color: var(--heading, #1a2e45);
		margin: 0 0 0.8rem;
		font-weight: 600;
		line-height: 1.3;
	}
	.lede {
		font-size: 1.05rem;
		color: var(--lead, #333);
		line-height: 1.65;
		margin: 0 0 1.5rem;
	}
	.coming-soon {
		padding: 1.1rem 1.2rem;
		background: var(--bg-alt, #f5f7f9);
		border-left: 3px solid var(--link, #1a5276);
		border-radius: 4px;
	}
	.coming-soon p {
		margin: 0;
		line-height: 1.6;
		color: var(--text, #222);
	}
</style>
