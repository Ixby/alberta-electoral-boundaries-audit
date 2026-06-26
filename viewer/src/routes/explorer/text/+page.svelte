<!--
  Alberta Electoral Boundary Audit — accessible text version of the map explorer.
  A static, screen-reader-first equivalent of the deck.gl map: anomaly-first
  (the flagged boundaries lead), followed by a combined district directory.
  No WebGL, no map-state coupling, no live regions — fully prerendered HTML.

  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import { FLAGS } from '$lib/deckExplorer/pois';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>{t(lang.current, 'explorer.text.page_title')}</title>
	<meta name="description" content={t(lang.current, 'explorer.text.intro')} />
</svelte:head>

<a class="skip-link" href="#main">{t(lang.current, 'explorer.text.skip_to_main')}</a>

<div class="shadow">
	<header class="prose">
		<div class="site-label">Alberta Electoral Boundary Audit</div>
		<h1>{t(lang.current, 'explorer.text.page_title')}</h1>
		<p>{t(lang.current, 'explorer.text.intro')}</p>
		<p class="header-links">
			<a href="{base}/explorer">{t(lang.current, 'explorer.text.link_map')}</a>
			<span aria-hidden="true">·</span>
			<a href="{base}/">{t(lang.current, 'explorer.text.link_report')}</a>
		</p>
	</header>

	<nav aria-label={t(lang.current, 'explorer.text.toc_heading')} class="toc prose">
		<h2 class="toc-heading">{t(lang.current, 'explorer.text.toc_heading')}</h2>
		<ul>
			<li><a href="#summary">{t(lang.current, 'explorer.text.toc_summary')}</a></li>
			<li><a href="#flagged">{t(lang.current, 'explorer.text.toc_flagged')}</a></li>
			<li><a href="#directory">{t(lang.current, 'explorer.text.toc_directory')}</a></li>
		</ul>
	</nav>

	<main id="main">
		<section aria-labelledby="summary" class="prose">
			<h2 id="summary">{t(lang.current, 'explorer.text.summary_heading')}</h2>
			<p>{t(lang.current, 'explorer.text.summary_p1')}</p>
			<p>{t(lang.current, 'explorer.text.summary_p2')}</p>
			<p>{t(lang.current, 'explorer.text.summary_p3')}</p>
		</section>

		<section aria-labelledby="flagged">
			<div class="prose">
				<h2 id="flagged">{t(lang.current, 'explorer.text.flagged_heading')}</h2>
				<p>{t(lang.current, 'explorer.text.flagged_lead')}</p>
			</div>
			{#each FLAGS as f (f.id)}
				<article class="flag prose">
					<h3 id={'flag-' + f.id}>{t(lang.current, 'explorer.flags.' + f.id + '.title')}</h3>
					<p>{t(lang.current, 'explorer.flags.' + f.id + '.body')}</p>
				</article>
			{/each}
		</section>

		<section aria-labelledby="directory">
			<div class="prose">
				<h2 id="directory">{t(lang.current, 'explorer.text.directory_heading')}</h2>
				<p>{t(lang.current, 'explorer.text.directory_lead')}</p>
			</div>
			<div class="table-wrap">
				<table>
					<caption>{t(lang.current, 'explorer.text.directory_heading')}</caption>
					<thead>
						<tr>
							<th scope="col">{t(lang.current, 'explorer.text.col_district')}</th>
							<th scope="col">{t(lang.current, 'explorer.text.col_minority')}</th>
							<th scope="col">{t(lang.current, 'explorer.text.col_majority')}</th>
							<th scope="col">{t(lang.current, 'explorer.text.col_2019')}</th>
						</tr>
					</thead>
					<tbody>
						{#each data.directory as row (row.name)}
							<tr>
								<th scope="row">{row.name}</th>
								<td class:no={!row.minority}>
									{row.minority
										? t(lang.current, 'explorer.text.present_yes')
										: t(lang.current, 'explorer.text.present_no')}
								</td>
								<td class:no={!row.majority}>
									{row.majority
										? t(lang.current, 'explorer.text.present_yes')
										: t(lang.current, 'explorer.text.present_no')}
								</td>
								<td class:no={!row.ed2019}>
									{row.ed2019
										? t(lang.current, 'explorer.text.present_yes')
										: t(lang.current, 'explorer.text.present_no')}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</section>
	</main>

	<footer class="prose">
		<p class="methodology">{t(lang.current, 'explorer.text.methodology_note')}</p>
		<p class="footer-links">
			<a href="{base}/explorer">{t(lang.current, 'explorer.text.back_to_map')}</a>
			<span aria-hidden="true">·</span>
			<a href="{base}/">{t(lang.current, 'explorer.text.link_report')}</a>
		</p>
	</footer>
</div>

<style>
	/* Warm-paper theme. The report defines --bg/--text/--heading/--link/--border/
	   --measure at :root, but those declarations are scoped to the report page's
	   component and do not reach this route — so each var carries a sensible
	   fallback here. Dark mode rides on the global [data-theme="dark"] attribute
	   set by app.html. */
	.shadow {
		--c-bg: var(--bg, #f9f7f2);
		--c-text: var(--text, #1a1a1a);
		--c-heading: var(--heading, #1a2e45);
		--c-link: var(--link, #1a5276);
		--c-border: var(--border, #ddd);
		--c-measure: var(--measure, 70ch);

		min-height: 100vh;
		background: var(--c-bg);
		color: var(--c-text);
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue',
			Arial, sans-serif;
		font-size: 17px;
		line-height: 1.65;
		padding: 1.5rem 1.25rem 4rem;
	}

	:global(:root[data-theme='dark']) .shadow {
		--c-bg: #1e1f26;
		--c-text: #dde2ed;
		--c-heading: #9eb8d0;
		--c-link: #6ab0d8;
		--c-border: #38394a;
	}

	.prose {
		max-width: var(--c-measure);
		margin-inline: auto;
	}

	.skip-link {
		position: absolute;
		left: -9999px;
		top: 0;
		z-index: 10;
		padding: 0.6rem 1rem;
		background: var(--bg, #f9f7f2);
		color: var(--link, #1a5276);
		border: 1px solid var(--border, #ddd);
		border-radius: 4px;
		text-decoration: underline;
	}
	.skip-link:focus {
		left: 0.75rem;
		top: 0.75rem;
	}

	.site-label {
		font-size: 0.8rem;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--c-heading);
		opacity: 0.75;
		margin-bottom: 0.4rem;
	}

	h1 {
		color: var(--c-heading);
		font-size: 1.9rem;
		line-height: 1.25;
		margin: 0 0 0.75rem;
	}
	h2 {
		color: var(--c-heading);
		font-size: 1.4rem;
		margin: 2.25rem 0 0.6rem;
		padding-top: 0.5rem;
		border-top: 1px solid var(--c-border);
	}
	h3 {
		color: var(--c-heading);
		font-size: 1.12rem;
		margin: 1.6rem 0 0.4rem;
	}
	p {
		margin: 0 0 0.85rem;
	}

	a {
		color: var(--c-link);
	}
	a:hover {
		text-decoration: underline;
	}

	.header-links,
	.footer-links {
		font-size: 0.95rem;
	}
	.header-links span,
	.footer-links span {
		margin: 0 0.5rem;
		color: var(--c-border);
	}

	.toc {
		margin-top: 1.75rem;
	}
	.toc-heading {
		font-size: 1.05rem;
		border-top: none;
		margin: 0 0 0.4rem;
		padding-top: 0;
	}
	.toc ul {
		margin: 0;
		padding-left: 1.25rem;
	}
	.toc li {
		margin-bottom: 0.25rem;
	}

	.flag {
		margin-top: 0.5rem;
	}

	/* The table stays wider than the prose measure so all four columns breathe. */
	.table-wrap {
		max-width: 60rem;
		margin-inline: auto;
		overflow-x: auto;
	}
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.95rem;
		margin-top: 0.5rem;
	}
	caption {
		caption-side: top;
		text-align: left;
		font-weight: 600;
		color: var(--c-heading);
		padding-bottom: 0.5rem;
	}
	thead th {
		text-align: left;
		font-weight: 600;
		color: var(--c-heading);
		background: color-mix(in srgb, var(--c-heading) 8%, transparent);
		border-bottom: 2px solid var(--c-border);
		padding: 0.5rem 0.7rem;
		vertical-align: bottom;
	}
	tbody th {
		text-align: left;
		font-weight: 600;
	}
	tbody th,
	tbody td {
		padding: 0.45rem 0.7rem;
		border-bottom: 1px solid var(--c-border);
		vertical-align: top;
	}
	tbody td {
		text-align: center;
	}
	/* "No" cells: meaningful text for screen readers, dimmed visually. */
	td.no {
		opacity: 0.55;
	}
	tbody tr:hover {
		background: color-mix(in srgb, var(--c-heading) 5%, transparent);
	}

	.methodology {
		margin-top: 2.5rem;
		padding-top: 1rem;
		border-top: 1px solid var(--c-border);
		font-size: 0.9rem;
		opacity: 0.85;
	}
</style>
