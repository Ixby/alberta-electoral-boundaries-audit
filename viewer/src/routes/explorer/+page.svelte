<!--
  Alberta Electoral Boundary Audit — interactive map explorer (deck.gl)
  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  https://ixby.github.io

  Full-viewport deck.gl explorer, lifted out of the report homepage into its
  own route. The container is position:fixed; inset:0 so it fills the screen
  regardless of the root layout's 1200px .app-shell (which sets no
  transform/filter/contain and so forms no containing block — see +layout.svelte).
-->
<script lang="ts">
  import { base } from '$app/paths';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import DeckExplorer from '$lib/DeckExplorer.svelte';
  import { hasWebGL } from '$lib/deckExplorer/webglSupport';
  import { FLAGS } from '$lib/deckExplorer/pois';
  import { pageview } from '$lib/analytics';
  import { SUPPORTED_LANGS, lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';

  let ready = $state(false);
  let webgl = $state(true);
  let poi = $state<string | null>(null);

  onMount(() => {
    const params = new URLSearchParams(location.search);
    webgl = hasWebGL(params.has('nowebgl'));
    const poiParam = params.get('poi');
    if (poiParam && FLAGS.some((f) => f.id === poiParam)) poi = poiParam;
    ready = true;
    pageview();
  });

  function goHome(): void {
    goto((base || '') + '/');
  }
</script>

<svelte:head>
  <title>MapExplorer — Beta</title>
</svelte:head>

<div class="explorer-root">
  <a class="text-version-link" href="{base}/explorer/text">
    {t(lang.current, 'explorer.text.link_to_text')}
  </a>
  {#if webgl && ready}
    <!-- Return-to-report navigation. Desktop shows a labelled bar; mobile
         collapses it to a single home icon to keep the map clear. -->
    <a class="explorer-back" href="{base}/" title={t(lang.current, 'feedback.back_to_report')} aria-label={t(lang.current, 'feedback.back_to_report')}>
      <svg class="explorer-back-ico" width="16" height="16" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 2L2 9h2v9h5v-5h2v5h5V9h2L10 2z"/></svg>
      <span class="explorer-back-label">{t(lang.current, 'feedback.back_to_report')}</span>
    </a>
  {/if}
  {#if webgl}
    {#if ready}
      <!-- All supported locales are offered — every explorer.* key is translated
           across the full locale set. The language switcher is integrated into
           DeckExplorer's control bar/panel. -->
      <DeckExplorer base={base} initialPoi={poi} onClose={goHome} langs={SUPPORTED_LANGS} />
    {/if}
  {:else}
    <div class="nowebgl">
      <div class="nowebgl-inner">
        <h1>The interactive map needs WebGL</h1>
        <p>
          This map renders with hardware-accelerated WebGL, which is not
          available in your browser right now. Try enabling hardware
          acceleration, or switch to a browser that supports it.
        </p>
        <p>
          <a href="{base}/">Back to the report</a>
          <span aria-hidden="true">·</span>
          <a href="{base}/feedback">{t(lang.current, 'feedback.nav_link')}</a>
        </p>
      </div>
    </div>
  {/if}
</div>

<style>
  /* Fill the viewport regardless of the root layout's 1200px shell. */
  .explorer-root {
    position: fixed;
    inset: 0;
    z-index: 9000;
    background: #0d1a26;
  }
  /* Screen-reader-only: the link to the accessible text version is exposed to
     assistive tech (kept in the a11y tree and tab order) but visually hidden, so
     it doesn't sit over the map for sighted users. Standard visually-hidden clip. */
  .text-version-link {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: -1px;
    padding: 0;
    border: 0;
    overflow: hidden;
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    white-space: nowrap;
  }
  /* Return-to-report control over the map: a labelled bar on desktop, a single
     home icon on mobile. Sits top-left, clear of the right-side map controls. */
  .explorer-back {
    position: absolute;
    top: 0.7rem;
    left: 0.7rem;
    z-index: 9500;
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.5rem 0.85rem 0.5rem 0.7rem;
    background: rgba(13, 26, 38, 0.92);
    color: #e6edf3;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
    text-decoration: none;
    font: 600 0.85rem/1 -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(4px);
    transition: background 0.15s ease, border-color 0.15s ease;
  }
  .explorer-back:hover {
    background: rgba(20, 40, 58, 0.96);
    border-color: rgba(255, 255, 255, 0.28);
  }
  .explorer-back:focus-visible {
    outline: 2px solid #8ab4ff;
    outline-offset: 2px;
  }
  .explorer-back-ico { flex-shrink: 0; }
  @media (max-width: 720px) {
    .explorer-back {
      padding: 0.55rem;
      border-radius: 50%;
    }
    .explorer-back-label { display: none; }
  }
  .nowebgl {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    color: #e6edf3;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
  }
  .nowebgl-inner {
    max-width: 32rem;
    text-align: center;
  }
  .nowebgl-inner h1 {
    font-size: 1.4rem;
    margin: 0 0 0.8rem;
  }
  .nowebgl-inner p {
    margin: 0 0 0.8rem;
    line-height: 1.6;
    color: rgba(230, 237, 243, 0.85);
  }
  .nowebgl-inner a {
    color: #8ab4ff;
    text-decoration: underline;
  }
</style>
