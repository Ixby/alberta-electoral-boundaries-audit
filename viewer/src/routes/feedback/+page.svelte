<!--
  Alberta Electoral Boundary Audit — public feedback form.
  Accessible, internationalized, store-first. Posts to the feedback-submit
  Supabase Edge Function via lib/feedback.ts. No tracking, no account.

  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { lang, setLang, SUPPORTED_LANGS, LANG_LABELS, type Lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
	import { submitFeedback } from '$lib/feedback';

	// Form state (Svelte 5 runes). No name/email is collected — the form is
	// anonymous; the message is the only content field.
	let message = $state('');
	let website = $state(''); // honeypot — stays empty for real users
	let status = $state<'idle' | 'sending' | 'sent' | 'error'>('idle');
	let errorMsg = $state('');

	let messageEl: HTMLTextAreaElement | undefined = $state();

	// Friendly label for the language dropdown: drop the parenthetical, and use
	// Traditional/Simplified for the two Chinese variants (matches the explorer).
	function langLabel(code: Lang): string {
		const { native, english } = LANG_LABELS[code];
		if (code === 'zh-Hant') return `${native} — Traditional`;
		if (code === 'zh-Hans') return `${native} — Simplified`;
		return `${native} — ${english.replace(/\s*\([^)]*\)/, '')}`;
	}

	async function onSubmit(e: SubmitEvent) {
		e.preventDefault();
		if (status === 'sending') return;
		if (!message.trim()) {
			status = 'error';
			errorMsg = t(lang.current, 'feedback.error_empty');
			messageEl?.focus();
			return;
		}
		status = 'sending';
		errorMsg = '';

		const result = await submitFeedback({
			message: message.trim(),
			website,
			context: {
				page: 'feedback',
				lang: lang.current,
				path: typeof location !== 'undefined' ? location.pathname : null,
				ref: typeof document !== 'undefined' ? document.referrer || null : null
			}
		});

		if (result.ok) {
			status = 'sent';
			message = '';
		} else {
			status = 'error';
			errorMsg = t(
				lang.current,
				result.reason === 'rate'
					? 'feedback.error_rate'
					: result.reason === 'empty'
						? 'feedback.error_empty'
						: 'feedback.error_generic'
			);
		}
	}

	function sendAnother() {
		status = 'idle';
		errorMsg = '';
	}

	// Split the privacy note around its {privacy} placeholder so the policy link
	// can be rendered inline without using @html.
	const noteParts = $derived(t(lang.current, 'feedback.privacy_note').split('{privacy}'));
</script>

<svelte:head>
	<title>{t(lang.current, 'feedback.page_title')} · Alberta Electoral Boundary Audit</title>
	<meta name="description" content={t(lang.current, 'feedback.meta_description')} />
</svelte:head>

<header>
	<div class="header-inner">
		<a href="{base}/" class="back-link">← {t(lang.current, 'feedback.back_to_report')}</a>
		<div class="header-top">
			<div class="header-text">
				<div class="site-label">Alberta Electoral Boundary Audit</div>
				<h1>{t(lang.current, 'feedback.heading')}</h1>
			</div>
			<label class="lang-picker">
				<span class="sr-only">Language</span>
				<select
					value={lang.current}
					onchange={(e) => setLang(e.currentTarget.value as Lang)}
				>
					{#each SUPPORTED_LANGS as code (code)}
						<option value={code}>{langLabel(code)}</option>
					{/each}
				</select>
			</label>
		</div>
	</div>
</header>

<main>
	<div class="wrap">
		{#if status === 'sent'}
			<div class="confirm" role="status" aria-live="polite">
				<h2>{t(lang.current, 'feedback.success_title')}</h2>
				<p>{t(lang.current, 'feedback.success_body')}</p>
				<button type="button" class="btn ghost" onclick={sendAnother}>
					{t(lang.current, 'feedback.send_another')}
				</button>
			</div>
		{:else}
			<p class="intro">{t(lang.current, 'feedback.intro')}</p>

			<form onsubmit={onSubmit} novalidate>
				<!-- Honeypot: visually hidden + off the tab order. Bots fill it; humans don't. -->
				<div class="hp" aria-hidden="true">
					<label for="website">Leave this field empty</label>
					<input
						id="website"
						name="website"
						type="text"
						tabindex="-1"
						autocomplete="off"
						bind:value={website}
					/>
				</div>

				<div class="field">
					<label for="fb-message">
						{t(lang.current, 'feedback.message_label')}
						<span class="req">({t(lang.current, 'feedback.message_required')})</span>
					</label>
					<textarea
						id="fb-message"
						rows="7"
						required
						maxlength="5000"
						placeholder={t(lang.current, 'feedback.message_placeholder')}
						aria-describedby={status === 'error' ? 'fb-error' : undefined}
						aria-invalid={status === 'error'}
						bind:this={messageEl}
						bind:value={message}
					></textarea>
				</div>

				{#if status === 'error'}
					<p id="fb-error" class="error" role="alert">{errorMsg}</p>
				{/if}

				<div class="actions">
					<button type="submit" class="btn" disabled={status === 'sending'}>
						{status === 'sending'
							? t(lang.current, 'feedback.submitting')
							: t(lang.current, 'feedback.submit')}
					</button>
				</div>

				<p class="note">
					{noteParts[0]}<a href="{base}/privacy-policy">{t(lang.current, 'feedback.privacy_link_text')}</a>{noteParts[1] ?? ''}
				</p>
			</form>
		{/if}

		<p class="footer-links">
			<a href="{base}/">{t(lang.current, 'feedback.back_to_report')}</a>
			<span aria-hidden="true">·</span>
			<a href="{base}/explorer">{t(lang.current, 'feedback.back_to_map')}</a>
		</p>
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
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			sans-serif;
		font-size: 17px;
		line-height: 1.65;
		color: #1a1a1a;
		background: #f9f7f2;
	}
	:global(:root[data-theme='dark'] body) {
		color: #dde2ed;
		background: #1e1f26;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		clip-path: inset(50%);
		white-space: nowrap;
		border: 0;
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
		max-width: 680px;
		margin: 0 auto;
	}

	.header-top {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.back-link {
		display: inline-block;
		color: rgba(255, 255, 255, 0.6);
		text-decoration: none;
		font-size: 0.85rem;
		margin-bottom: 1.1rem;
		transition: color 0.15s;
	}
	.back-link:hover {
		color: #fff;
	}

	.site-label {
		font-size: 0.75rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: rgba(255, 255, 255, 0.45);
		margin-bottom: 0.35rem;
	}

	h1 {
		font-size: clamp(1.4rem, 4vw, 1.9rem);
		font-weight: 700;
		letter-spacing: -0.01em;
		line-height: 1.25;
	}

	.lang-picker select {
		font-size: 0.85rem;
		padding: 0.35rem 0.5rem;
		border-radius: 6px;
		border: 1px solid rgba(255, 255, 255, 0.25);
		background: rgba(255, 255, 255, 0.08);
		color: #fff;
		max-width: 14rem;
	}
	.lang-picker select option {
		color: #1a1a1a;
	}

	main {
		padding: 2.5rem clamp(1.2rem, 4vw, 3.5rem) 4rem;
	}

	.wrap {
		max-width: 680px;
		margin: 0 auto;
	}

	.intro {
		margin-bottom: 1.8rem;
		max-width: 60ch;
	}

	.field {
		margin-bottom: 1.4rem;
	}

	label {
		display: block;
		font-weight: 600;
		margin-bottom: 0.4rem;
		color: #1a2e45;
	}
	:global(:root[data-theme='dark']) label {
		color: #a8c4e0;
	}

	.opt {
		font-weight: 400;
		font-size: 0.85rem;
		opacity: 0.6;
	}
	.req {
		font-weight: 400;
		font-size: 0.85rem;
		color: #9a3a3a;
	}
	:global(:root[data-theme='dark']) .req {
		color: #e08a8a;
	}

	textarea {
		width: 100%;
		font: inherit;
		padding: 0.6rem 0.7rem;
		border: 1px solid #c9c4ba;
		border-radius: 7px;
		background: #fff;
		color: inherit;
		resize: vertical;
		min-height: 7em;
	}
	:global(:root[data-theme='dark']) textarea {
		background: #262833;
		border-color: #3a3d4d;
	}

	textarea:focus-visible,
	select:focus-visible,
	.btn:focus-visible {
		outline: 3px solid #1a5276;
		outline-offset: 2px;
	}

	/* Honeypot: removed from layout and the accessibility tree, off the tab order. */
	.hp {
		position: absolute;
		left: -9999px;
		width: 1px;
		height: 1px;
		overflow: hidden;
	}

	.error {
		color: #9a3a3a;
		font-weight: 600;
		margin-bottom: 1rem;
	}
	:global(:root[data-theme='dark']) .error {
		color: #e08a8a;
	}

	.actions {
		margin-top: 0.5rem;
	}

	.btn {
		font: inherit;
		font-weight: 600;
		cursor: pointer;
		padding: 0.65rem 1.4rem;
		border: none;
		border-radius: 7px;
		background: #1a5276;
		color: #fff;
		transition: background 0.15s;
	}
	.btn:hover:not(:disabled) {
		background: #154360;
	}
	.btn:disabled {
		opacity: 0.6;
		cursor: default;
	}
	.btn.ghost {
		background: transparent;
		color: #1a5276;
		border: 1px solid #1a5276;
	}
	:global(:root[data-theme='dark']) .btn.ghost {
		color: #6aaddb;
		border-color: #6aaddb;
	}

	.note {
		font-size: 0.85rem;
		opacity: 0.75;
		margin-top: 1.4rem;
		max-width: 60ch;
	}

	.confirm {
		padding: 1.5rem;
		border: 1px solid #cdd9c8;
		background: #f0f6ec;
		border-radius: 10px;
	}
	:global(:root[data-theme='dark']) .confirm {
		background: #1f2b22;
		border-color: #34503a;
	}
	.confirm h2 {
		color: #2c5a32;
		margin-bottom: 0.6rem;
		font-size: 1.25rem;
	}
	:global(:root[data-theme='dark']) .confirm h2 {
		color: #8fce98;
	}
	.confirm p {
		margin-bottom: 1.1rem;
	}

	a {
		color: #1a5276;
	}
	a:hover {
		text-decoration: underline;
	}
	:global(:root[data-theme='dark']) a {
		color: #6aaddb;
	}

	.footer-links {
		margin-top: 2.5rem;
		padding-top: 1.2rem;
		border-top: 1px solid #e0ddd6;
		font-size: 0.95rem;
	}
	:global(:root[data-theme='dark']) .footer-links {
		border-top-color: #2e3040;
	}
	.footer-links span {
		margin: 0 0.5rem;
		color: #c9c4ba;
	}
</style>
