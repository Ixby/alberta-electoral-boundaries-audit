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
  <title>MapExplorer (Beta) — Alberta Electoral Boundary Audit</title>
</svelte:head>

<div class="explorer-root">
  <a class="text-version-link" href="{base}/explorer/text">
    {t(lang.current, 'explorer.text.link_to_text')}
  </a>
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
        <p><a href="{base}/">Back to the report</a></p>
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
