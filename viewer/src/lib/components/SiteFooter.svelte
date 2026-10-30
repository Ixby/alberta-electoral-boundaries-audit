<!--
  Alberta Electoral Boundary Audit — site footer, shared by every page (+layout.svelte)
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
-->
<script lang="ts">
	import { base } from '$app/paths';
	import { lang } from '$lib/i18n/store.svelte';
	import { t } from '$lib/i18n/dict';
</script>

<footer class="site-footer">
	<div class="footer-inner">
		{t(lang.current, 'chrome.footer.title')}<br />
		{t(lang.current, 'chrome.footer.copyright')}
		{t(lang.current, 'chrome.footer.text_label')} <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a> &mdash;
		{t(lang.current, 'chrome.footer.code_label')} <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v3.0</a> &mdash;
		{t(lang.current, 'chrome.footer.translation_label')} {t(lang.current, 'chrome.footer.translation_credit')}<br />
		<span class="data-credit">{t(lang.current, 'chrome.footer.data_credit')}</span><br />
		<a href="https://ixby.github.io">ixby.github.io</a> &mdash;
		<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a><br />
		<a href="{base}/privacy-policy">{t(lang.current, 'chrome.participation.privacy_policy')}</a> &mdash;
		<a href="{base}/feedback">{t(lang.current, 'feedback.nav_link')}</a>
	</div>
</footer>

<style>
	/* Colours match the main page's --nav-bg / --nav-accent tokens, carried
	   here because only the main page declares them. */
	.site-footer {
		--ftr-bg: #1e3552;
		--ftr-accent: #6fd3fb;
		background: var(--ftr-bg);
		color: rgba(255, 255, 255, 0.6);
		padding: 1.8rem 1.5rem 1.6rem;
		text-align: center;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
		font-size: 0.82rem;
		line-height: 1.7;
		margin-top: 2rem;
		border-top: 2px solid var(--ftr-accent);
		letter-spacing: 0.005em;
	}
	:global(:root[data-theme='dark']) .site-footer {
		--ftr-bg: #1a1e2d;
		--ftr-accent: #4fc3f7;
	}
	.footer-inner {
		width: 100%;
		max-width: 1000px;
		margin-inline: auto;
		padding: 0 clamp(1.2rem, 4vw, 3.5rem);
		box-sizing: border-box;
	}
	.site-footer a {
		color: rgba(255, 255, 255, 0.78);
		text-decoration: none;
		border-bottom: 1px solid rgba(255, 255, 255, 0.18);
		transition: color 0.15s ease, border-color 0.15s ease;
	}
	.site-footer a:hover {
		color: #fff;
		border-bottom-color: rgba(255, 255, 255, 0.55);
	}
	.site-footer a:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.55);
		outline-offset: 2px;
		border-radius: 2px;
	}
</style>
