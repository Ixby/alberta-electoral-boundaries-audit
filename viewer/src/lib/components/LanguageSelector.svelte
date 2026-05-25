<script lang="ts">
	import { lang, setLang, SUPPORTED_LANGS, LANG_LABELS, type Lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';

	let open = $state(false);
	let menuEl: HTMLUListElement | null = $state(null);
	let triggerEl: HTMLButtonElement | null = $state(null);

	function choose(next: Lang) {
		setLang(next);
		open = false;
		if (typeof document !== 'undefined') {
			document.documentElement.lang = LANG_LABELS[next].htmlLang;
		}
		triggerEl?.focus();
	}

	function onDocumentClick(e: MouseEvent) {
		if (!open) return;
		const target = e.target as Node | null;
		if (target && menuEl && !menuEl.contains(target) && triggerEl && !triggerEl.contains(target)) {
			open = false;
		}
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape' && open) {
			open = false;
			triggerEl?.focus();
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

<div class="lang-selector">
	<button
		bind:this={triggerEl}
		type="button"
		class="lang-trigger"
		aria-haspopup="listbox"
		aria-expanded={open}
		aria-label={t(lang.current, 'selector.label')}
		onclick={() => (open = !open)}
	>
		<span lang={LANG_LABELS[lang.current].htmlLang}>{LANG_LABELS[lang.current].native}</span>
		<span aria-hidden="true" class="caret">▾</span>
	</button>
	{#if open}
		<ul bind:this={menuEl} class="lang-menu" role="listbox">
			{#each SUPPORTED_LANGS as code (code)}
				<li>
					<button
						type="button"
						class="lang-option"
						class:active={code === lang.current}
						role="option"
						aria-selected={code === lang.current}
						onclick={() => choose(code)}
					>
						<span class="native" lang={LANG_LABELS[code].htmlLang}>{LANG_LABELS[code].native}</span>
						<span class="english">{LANG_LABELS[code].english}</span>
					</button>
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.lang-selector {
		position: relative;
		display: inline-block;
		font-size: 0.875rem;
	}
	.lang-trigger {
		background: transparent;
		border: 1px solid currentColor;
		padding: 0.3rem 0.6rem;
		border-radius: 4px;
		cursor: pointer;
		color: inherit;
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		font: inherit;
	}
	.lang-trigger:focus-visible {
		outline: 2px solid currentColor;
		outline-offset: 2px;
	}
	.caret {
		font-size: 0.7em;
		opacity: 0.7;
	}
	.lang-menu {
		position: absolute;
		top: calc(100% + 0.25rem);
		right: 0;
		margin: 0;
		padding: 0.25rem 0;
		list-style: none;
		background: var(--bg, white);
		color: var(--fg, inherit);
		border: 1px solid currentColor;
		border-radius: 4px;
		min-width: 13rem;
		z-index: 50;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}
	.lang-option {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		width: 100%;
		padding: 0.45rem 0.8rem;
		background: transparent;
		border: 0;
		cursor: pointer;
		text-align: left;
		color: inherit;
		font: inherit;
	}
	.lang-option:hover,
	.lang-option:focus-visible {
		background: rgba(127, 127, 127, 0.12);
		outline: none;
	}
	.lang-option.active {
		font-weight: 600;
	}
	.native {
		font-size: 0.95rem;
	}
	.english {
		font-size: 0.72rem;
		opacity: 0.65;
		margin-top: 0.1rem;
	}
</style>
