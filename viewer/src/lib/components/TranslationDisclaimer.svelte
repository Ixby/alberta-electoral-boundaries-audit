<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';

	// Disclaimer text contains a "%s" placeholder where the contact link goes.
	// Split here so the link is a real <a>, not raw HTML, and so the surrounding
	// text remains a translatable single string per locale.
	let parts = $derived.by(() => {
		if (lang.current === 'en') return null;
		const raw = t(lang.current, 'disclaimer.text');
		const label = t(lang.current, 'disclaimer.link_label');
		const idx = raw.indexOf('%s');
		if (idx < 0) return { pre: raw, label, post: '' };
		return { pre: raw.slice(0, idx), label, post: raw.slice(idx + 2) };
	});
</script>

{#if parts}
	<aside class="ai-disclaimer" role="note" lang={lang.current === 'en' ? 'en' : undefined}>
		<span aria-hidden="true" class="icon">⚙</span>
		<span class="msg">
			{parts.pre}<a href="#contact" class="link">{parts.label}</a>{parts.post}
		</span>
	</aside>
{/if}

<style>
	.ai-disclaimer {
		display: flex;
		align-items: flex-start;
		gap: 0.5rem;
		padding: 0.6rem 0.9rem;
		margin: 0;
		background: rgba(255, 200, 60, 0.12);
		border-bottom: 1px solid rgba(180, 130, 0, 0.35);
		color: inherit;
		font-size: 0.88rem;
		line-height: 1.45;
	}
	.icon {
		font-size: 1em;
		opacity: 0.7;
		flex: 0 0 auto;
	}
	.msg {
		flex: 1 1 auto;
	}
	.link {
		color: inherit;
		text-decoration: underline;
		font-weight: 500;
	}
	.link:hover,
	.link:focus-visible {
		text-decoration-thickness: 2px;
	}
</style>
