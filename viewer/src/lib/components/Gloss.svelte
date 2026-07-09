<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import { gloss, type GlossKey } from '$lib/i18n/glossary';

	// Glossary hrefs are root-absolute ("/law#ebca"). Rendered verbatim at
	// runtime they escape the project subpath on the GitHub Pages deployment
	// (ixby.github.io/law — 404): the prerenderer only relativizes links it
	// sees at build time, and these popovers mount on interaction. base='' at
	// build, so $app/paths can't help; instead resolve against the live URL —
	// "." + "/law#ebca" = "./law#ebca" relative to the current document, which
	// lands inside whatever directory the app is deployed under. Popovers only
	// render client-side ({#if open}), so location always exists here; the
	// typeof guard keeps SSR type-checking happy. (2026-07-09 link-audit fix.)
	function glossHref(href: string): string {
		if (typeof location === 'undefined') return href;
		const u = new URL('.' + href, location.href);
		return u.pathname + u.hash;
	}

	let { key, children } = $props<{
		key: GlossKey;
		children: import('svelte').Snippet;
	}>();

	let open = $state(false);
	let trigger: HTMLButtonElement | null = $state(null);
	let panel: HTMLDivElement | null = $state(null);

	const entry = $derived(gloss(lang.current, key));

	function toggle(e: MouseEvent) {
		e.preventDefault();
		e.stopPropagation();
		open = !open;
	}

	function onDocumentClick(e: MouseEvent) {
		if (!open) return;
		const target = e.target as Node | null;
		if (target && panel && !panel.contains(target) && trigger && !trigger.contains(target)) {
			open = false;
		}
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape' && open) {
			open = false;
			trigger?.focus();
		}
	}

	$effect(() => {
		if (typeof document === 'undefined') return;
		document.addEventListener('click', onDocumentClick);
		document.addEventListener('keydown', onKey);
		return () => {
			document.removeEventListener('click', onDocumentClick);
			document.removeEventListener('keydown', onKey);
		};
	});
</script>

<span class="gloss">
	<button
		bind:this={trigger}
		type="button"
		class="trigger"
		aria-expanded={open}
		aria-describedby={open ? `gloss-${key}-panel` : undefined}
		onclick={toggle}
	>
		{@render children()}
	</button>
	{#if open}
		<div bind:this={panel} class="panel" id="gloss-{key}-panel" role="dialog">
			<div class="term">{entry.term}</div>
			<div class="definition">
				{entry.definition}
			</div>
			{#if entry.href}
				<a class="more" href={glossHref(entry.href)} onclick={() => (open = false)}>
					{t(lang.current, 'glossary.more_link')}
				</a>
			{/if}
		</div>
	{/if}
</span>

<style>
	.gloss {
		position: relative;
		display: inline;
	}
	.trigger {
		background: none;
		border: 0;
		padding: 0;
		font: inherit;
		color: inherit;
		cursor: help;
		text-decoration: underline dotted;
		text-decoration-color: var(--link, #1a5276);
		text-underline-offset: 0.18em;
		text-decoration-thickness: 1px;
	}
	.trigger:hover,
	.trigger:focus-visible {
		text-decoration-style: solid;
		outline: none;
	}
	.panel {
		position: absolute;
		inset-inline-start: 0;
		top: calc(100% + 0.3rem);
		max-width: min(22rem, 90vw);
		padding: 0.7rem 0.9rem;
		background: var(--bg, white);
		color: var(--text, inherit);
		border: 1px solid var(--border, #ccc);
		border-radius: 6px;
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
		z-index: 60;
		font-size: 0.9rem;
		line-height: 1.5;
		cursor: auto;
	}
	.term {
		font-weight: bold;
		margin-bottom: 0.3rem;
	}
	.definition {
		color: var(--text, inherit);
	}
	.more {
		display: inline-block;
		margin-top: 0.5rem;
		font-size: 0.83rem;
		color: var(--link, #1a5276);
		text-decoration: none;
	}
	.more:hover,
	.more:focus-visible {
		text-decoration: underline;
	}
</style>
