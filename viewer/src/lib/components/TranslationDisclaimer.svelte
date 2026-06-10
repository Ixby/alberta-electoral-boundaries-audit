<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import en from '$lib/i18n/locales/en';

	// Live word count of the English prose, so a prospective volunteer
	// translator knows the size of the job before raising their hand.
	// Computed once at module load from the actual dictionary — never a
	// hardcoded number that goes stale as the prose grows. Rounded to the
	// nearest 500: this is a scale signal, not an invoice.
	function countWords(node: unknown): number {
		if (typeof node === 'string') {
			return node
				.replace(/<[^>]+>/g, ' ')
				.replace(/&[a-z#0-9]+;/gi, ' ')
				.split(/\s+/)
				.filter(Boolean).length;
		}
		if (node && typeof node === 'object') {
			return Object.values(node as Record<string, unknown>).reduce(
				(sum: number, v) => sum + countWords(v),
				0
			);
		}
		return 0;
	}
	const proseWords = Math.round(countWords(en) / 500) * 500;

	// Disclaimer text contains a "%s" placeholder where the contact link goes.
	// Split here so the link is a real <a>, not raw HTML, and so the surrounding
	// text remains a translatable single string per locale.
	let parts = $derived.by(() => {
		if (lang.current === 'en') return null;
		const raw = t(lang.current, 'disclaimer.text');
		const label = t(lang.current, 'disclaimer.link_label');
		const scale = t(lang.current, 'disclaimer.word_count').replace(
			'{count}',
			proseWords.toLocaleString()
		);
		const idx = raw.indexOf('%s');
		if (idx < 0) return { pre: raw, label, post: '', scale };
		return { pre: raw.slice(0, idx), label, post: raw.slice(idx + 2), scale };
	});
</script>

{#if parts}
	<aside class="ai-disclaimer" role="note" lang={lang.current === 'en' ? 'en' : undefined}>
		<span aria-hidden="true" class="icon">⚙</span>
		<span class="msg">
			{parts.pre}<a href="#contact" class="link">{parts.label}</a>{parts.post}
			<span class="scale">{parts.scale}</span>
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
	.scale {
		opacity: 0.75;
		font-size: 0.94em;
	}
</style>
