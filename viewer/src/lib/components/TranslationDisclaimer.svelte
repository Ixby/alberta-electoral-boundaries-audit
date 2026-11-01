<script lang="ts">
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import { proseWordCount as proseWords } from '$lib/i18n/wordCount';

	// Disclaimer text contains a "%s" placeholder where the contact link goes.
	// Split here so the link is a real <a>, not raw HTML, and so the surrounding
	// text remains a translatable single string per locale.
	let parts = $derived.by(() => {
		// English is the source; French has had a native-speaker review, so neither
		// shows the "AI-translated, pending review" notice.
		if (lang.current === 'en' || lang.current === 'fr') return null;
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
	// On narrow screens the notice is clamped to two lines; a tap shows all of it.
	let open = $state(false);
</script>

{#if parts}
	<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
	<aside
		class="ai-disclaimer"
		class:open
		role="note"
		lang={lang.current === 'en' ? 'en' : undefined}
		onclick={() => (open = true)}
	>
		<span class="msg">
			{parts.pre}<a href="#contact" class="link">{parts.label}</a>{parts.post}
			<span class="scale">{parts.scale}</span>
		</span>
	</aside>
{/if}

<style>
	/* Quiet by design: a slim muted line above the header, present but not competing with it. */
	.ai-disclaimer {
		display: flex;
		align-items: flex-start;
		padding: 0.3rem 0.9rem;
		margin: 0;
		background: transparent;
		border-bottom: 1px solid color-mix(in srgb, currentColor 12%, transparent);
		color: inherit;
		opacity: 0.72;
		font-size: 0.76rem;
		line-height: 1.4;
	}
	.msg {
		flex: 1 1 auto;
	}
	.link {
		color: inherit;
		text-decoration: underline;
		text-underline-offset: 2px;
	}
	.link:hover,
	.link:focus-visible {
		text-decoration-thickness: 2px;
	}
	.scale {
		opacity: 0.85;
	}
	@media (max-width: 640px) {
		.ai-disclaimer:not(.open) .msg {
			display: -webkit-box;
			-webkit-box-orient: vertical;
			-webkit-line-clamp: 2;
			line-clamp: 2;
			overflow: hidden;
			cursor: pointer;
		}
	}
</style>
