<!--
  Alberta Electoral Boundary Audit — Fixes for next time
  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Created 2026-10-29 with the main-page rewrite: the reform suggestions that used
  to sit on the main page (body.suggestions.*), kept whole. The main page keeps
  a short teaser that links here.
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	// In-page anchors in these strings point at main-page sections.
	const s = (k: string) =>
		t(lang.current, 'body.suggestions.' + k).replace(/href="#([^"]+)"/g, (_m, id: string) => `href="${base}/#${id}"`);
</script>

<svelte:head>
	<title>{t(lang.current, 'fixes.page_title')}</title>
	<meta name="description" content={s('intro')} />
</svelte:head>

<header>
	<div class="header-inner">
		<a href="{base}/" class="back-link">{t(lang.current, 'fixes.back')}</a>
		<div class="site-label">Alberta Electoral Boundary Audit</div>
		<h1>{t(lang.current, 'fixes.h1')}</h1>
		<p class="meta">{t(lang.current, 'fixes.meta')}</p>
	</div>
</header>

<main>
	<div class="content">
		<p class="standfirst">{s('intro')}</p>

		<section id="advance-votes">
			<p>{@html s('advance_p1')}</p>
			<p>{s('advance_p2')}</p>
		</section>

		<section id="lesser-slave-lake">
			<p>{@html s('lesser_slave_p1')}</p>
			<p>{@html s('lesser_slave_p2')}</p>
			<div class="callout">
				<p><strong>{s('ebca_label')}</strong></p>
				<p>{@html s('ebca_body')}</p>
			</div>
			<p>{@html s('rationale_p1')}</p>
			<p>{@html s('rationale_p2')}</p>
			<p>{@html s('banff_p')}</p>
		</section>

		<section id="census">
			<p>{@html s('census_p1')}</p>
			<p>{@html s('census_p2')}</p>
			<p>{s('closing')}</p>
		</section>
	</div>
</main>

<style>
	*,
	*::before,
	*::after {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}
	:global(body) {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
		font-size: 17px;
		line-height: 1.65;
		color: #1a1a1a;
		background: #f9f7f2;
	}
	:global(:root[data-theme='dark'] body) {
		color: #dde2ed;
		background: #1e1f26;
	}
	header {
		background: #1a2e45;
		color: #fff;
		padding: 2rem clamp(1.2rem, 4vw, 3.5rem);
	}
	:global(:root[data-theme='dark']) header {
		background: #111722;
	}
	.header-inner {
		max-width: 760px;
		margin: 0 auto;
	}
	.back-link {
		display: inline-block;
		color: rgba(255, 255, 255, 0.6);
		text-decoration: none;
		font-size: 0.85rem;
		margin-bottom: 1.1rem;
		padding: 4px 0;
	}
	.back-link:hover {
		color: #fff;
	}
	.site-label {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: rgba(255, 255, 255, 0.55);
		margin-bottom: 0.35rem;
	}
	h1 {
		font-size: clamp(1.4rem, 4vw, 1.9rem);
		font-weight: 700;
		line-height: 1.25;
		margin-bottom: 0.4rem;
	}
	.meta {
		font-size: 0.82rem;
		color: rgba(255, 255, 255, 0.55);
	}
	main {
		padding: 2.2rem clamp(1.2rem, 4vw, 3.5rem) 4rem;
	}
	.content {
		max-width: 760px;
		margin: 0 auto;
	}
	.standfirst {
		font-size: 1.06rem;
		color: #3a3a38;
		border-inline-start: 3px solid #1a2e45;
		padding-inline-start: 1rem;
		margin-bottom: 2.2rem;
	}
	:global(:root[data-theme='dark']) .standfirst {
		color: #b9c0d0;
		border-inline-start-color: #4a6690;
	}
	h2.group {
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #6b6b66;
		margin: 2.6rem 0 1rem;
	}
	section {
		margin-bottom: 2.2rem;
		scroll-margin-top: 1.5rem;
	}
	h3 {
		font-size: 1.18rem;
		font-weight: 700;
		margin-bottom: 0.7rem;
	}
	p {
		margin-bottom: 0.9rem;
	}
	a {
		color: #1a5276;
	}
	:global(:root[data-theme='dark']) a {
		color: #7fb3d5;
	}
	.cross-ref {
		font-size: 0.92rem;
	}
	figure {
		margin: 1.2rem 0;
		text-align: center;
	}
	.chart-img {
		max-width: 100%;
		height: auto;
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 4px;
		background: #f9f7f2;
		padding: 0.5rem;
	}
	:global(:root[data-theme='dark']) .chart-img {
		filter: brightness(0.88) contrast(0.95);
	}
	figcaption {
		font-size: 0.82rem;
		color: #6b6b66;
		margin-top: 0.4rem;
		text-align: start;
	}
	.callout {
		border-inline-start: 3px solid #1a2e45;
		background: rgba(26, 46, 69, 0.05);
		padding: 0.8rem 1rem 0.1rem;
		margin: 0 0 1rem;
	}
	:global(:root[data-theme='dark']) .callout {
		background: rgba(255, 255, 255, 0.04);
		border-inline-start-color: #4a6690;
	}
</style>
