<!--
  Alberta Electoral Boundary Audit — The full record
  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Created 2026-10-29 with the main-page rewrite (proposals/site_rewrite_2026-10-29):
  the fourteen findings the old main page carried as an evidence log, kept here in
  full so no caveat lost its home. Plain headings; the #casing-N anchors stay so
  shared links (and the main page's redirect of /#casing-N) still land. Body text
  is the existing body.casings.* strings, so their translations keep working.
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import FigureLightbox from '$lib/components/FigureLightbox.svelte';

	type Item = { n: number; app: string; context?: boolean; canada?: boolean };
	// canada:false = the beat had nothing to say ("Nothing", "Not applicable");
	// context:true = the one-line expert/context beat is substantive and sourced.
	const GROUPS: { key: string; items: Item[] }[] = [
		{
			key: 'group_map',
			items: [
				{ n: 1, app: 'a' },
				{ n: 2, app: 'b', context: true },
				{ n: 3, app: 'c' },
				{ n: 4, app: 'd' },
				{ n: 5, app: 'e', canada: false }
			]
		},
		{
			key: 'group_sim',
			items: [
				{ n: 6, app: 'f' },
				{ n: 7, app: 'g', canada: false },
				{ n: 8, app: 'h', context: true },
				{ n: 9, app: 'i', canada: false },
				{ n: 10, app: 'j', canada: false }
			]
		},
		{
			key: 'group_conduct',
			items: [
				{ n: 11, app: 'k' },
				{ n: 12, app: 'l' },
				{ n: 13, app: 'm', context: true },
				{ n: 14, app: 'n' }
			]
		}
	];
	// In-page anchors in these strings point at main-page sections; send them home
	// (retired ids map to their new ones). #casing-N links stay on this page.
	const MOVED: Record<string, string> = { retractions: 'change-our-mind' };
	const c = (n: number, beat: string) =>
		t(lang.current, `body.casings.c${n}_${beat}`).replace(
			/href="#(?!casing-)([^"]+)"/g,
			(_m, id: string) => `href="${base}/#${MOVED[id] ?? id}"`
		);
</script>

<svelte:head>
	<title>{t(lang.current, 'evidence.page_title')}</title>
	<meta name="description" content={t(lang.current, 'evidence.intro')} />
</svelte:head>

<header>
	<div class="header-inner">
		<a href="{base}/" class="back-link">{t(lang.current, 'evidence.back')}</a>
		<div class="site-label">Alberta Electoral Boundary Audit</div>
		<h1>{t(lang.current, 'evidence.h1')}</h1>
		<p class="meta">{t(lang.current, 'evidence.meta')}</p>
	</div>
</header>

<main>
	<div class="content">
		<p class="standfirst">{t(lang.current, 'evidence.intro')}</p>

		{#each GROUPS as g (g.key)}
			<h2 class="group">{t(lang.current, 'evidence.' + g.key)}</h2>
			{#each g.items as it (it.n)}
				<section id={'casing-' + it.n}>
					<h3>{it.n}. {t(lang.current, 'evidence.e' + it.n)}</h3>
					<p><strong>{t(lang.current, 'evidence.beat_found')}.</strong> {@html c(it.n, 'found')}</p>
					{#if it.n === 1}
						<figure>
							<picture>
								<source type="image/webp" srcset="{base}/images/figure_airdrie_v3.webp" />
								<img src="{base}/images/figure_airdrie_v3.jpg" data-full="{base}/images/figure_airdrie_v3.svg" alt={t(lang.current, 'body.cpd.fig_alt')} class="chart-img" width="504" height="336" loading="lazy" decoding="async" />
							</picture>
							<figcaption>{t(lang.current, 'body.cpd.fig_caption')}</figcaption>
						</figure>
					{/if}
					<p><strong>{t(lang.current, 'evidence.beat_show')}.</strong> {@html c(it.n, 'show')}</p>
					{#if it.context}
						<p><strong>{t(lang.current, 'evidence.beat_context')}.</strong> {@html c(it.n, 'experts')}</p>
					{/if}
					{#if it.canada !== false}
						<p><strong>{t(lang.current, 'evidence.beat_canada')}.</strong> {@html c(it.n, 'canada')}</p>
					{/if}
					<p><strong>{t(lang.current, 'evidence.beat_law')}.</strong> {@html c(it.n, 'gun')}</p>
					{#if it.n === 7}
						<figure>
							<picture>
								<source type="image/webp" srcset="{base}/images/lane1_dotplot.webp" />
								<img src="{base}/images/lane1_dotplot.jpg" data-full="{base}/images/lane1_dotplot.svg" alt={t(lang.current, 'body.litmus.fig_alt')} class="chart-img" width="463" height="251" loading="lazy" decoding="async" />
							</picture>
							<figcaption>{@html t(lang.current, 'body.litmus.fig_caption')}</figcaption>
						</figure>
					{/if}
					<p class="cross-ref">
						<a href="{base}/explainers#appendix-{it.app}">{t(lang.current, 'evidence.explainer')}: {t(lang.current, `body.casings.c${it.n}_app`)}</a>
					</p>
				</section>
			{/each}
			{#if g.key === 'group_map'}
				<figure id="act-1-picture">
					<picture>
						<source type="image/webp" srcset="{base}/images/lane2_bars.webp" />
						<img src="{base}/images/lane2_bars.jpg" data-full="{base}/images/lane2_bars.svg" alt={t(lang.current, 'body.impact.fig_alt')} class="chart-img" width="441" height="531" loading="lazy" decoding="async" />
					</picture>
					<figcaption>{t(lang.current, 'body.impact.fig_caption')}</figcaption>
				</figure>
			{/if}
		{/each}
	</div>
</main>

<FigureLightbox />

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
</style>
