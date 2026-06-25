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
  import LanguageSelector from '$lib/components/LanguageSelector.svelte';
  import { hasWebGL } from '$lib/deckExplorer/webglSupport';
  import { FLAGS } from '$lib/deckExplorer/pois';
  import { pageview } from '$lib/analytics';

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
  <title>Interactive map — Alberta Electoral Boundary Audit</title>
</svelte:head>

<div class="explorer-root">
  {#if webgl}
    {#if ready}
      <DeckExplorer base={base} initialPoi={poi} onClose={goHome} />
      <div class="lang-corner"><LanguageSelector /></div>
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
  /* Language selector pinned to the top-left corner (map controls are top-right,
     the debug HUD is bottom-left, so top-left is clear). Above the deck canvas. */
  .lang-corner {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 9100;
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
