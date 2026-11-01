<!--
  Alberta Electoral Boundary Audit — The Fourteen Explainers (Appendices A–N)
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  One appendix per casing on the main page. Each owns exactly one concept and
  walks a fixed arc: name the confusion, build the concept with one concrete
  example, send the reader back to the casing able to read its number unaided,
  close with what the concept cannot tell you. Content mirrors the appendices
  of reports/public/report_public.md — keep the two in sync.
  Reader-facing text lives in en.ts under pages.explainers.* so it can be translated
  (other locales fall back to English until they add these keys).
-->
<svelte:head>
  <title>{t(lang.current, 'pages.explainers.head_title')}</title>
  <meta name="description" content={t(lang.current, 'pages.explainers.head_description')}>
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
  import { lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';
</script>

<div class="page-head">
  <div class="header-inner">
    <a href="{base}/" class="back-link">{t(lang.current, 'pages.explainers.back')}</a>
    <div class="header-text">
      <div class="site-label">{t(lang.current, 'pages.explainers.site_label')}</div>
      <h1>{t(lang.current, 'pages.explainers.h1')}</h1>
      <p class="meta">{t(lang.current, 'pages.explainers.meta')}</p>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
  <div class="content">

    <p class="standfirst">{@html t(lang.current, 'pages.explainers.standfirst')}</p>

    <section id="appendix-a">
      <h2>{t(lang.current, 'pages.explainers.appendix_a.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_a.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_a.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_a.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_a.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_a.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-b">
      <h2>{t(lang.current, 'pages.explainers.appendix_b.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_b.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_b.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_b.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_b.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_b.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-c">
      <h2>{t(lang.current, 'pages.explainers.appendix_c.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_c.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_c.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_c.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_c.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_c.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-d">
      <h2>{t(lang.current, 'pages.explainers.appendix_d.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_d.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_d.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_d.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_d.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_d.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-e">
      <h2>{t(lang.current, 'pages.explainers.appendix_e.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_e.confusion')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_e.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_e.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_e.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_e.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-f">
      <h2>{t(lang.current, 'pages.explainers.appendix_f.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_f.confusion')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_f.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_f.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_f.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_f.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-g">
      <h2>{t(lang.current, 'pages.explainers.appendix_g.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_g.confusion')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_g.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_g.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_g.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_g.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-h">
      <h2>{t(lang.current, 'pages.explainers.appendix_h.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_h.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_h.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_h.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_h.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_h.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-i">
      <h2>{t(lang.current, 'pages.explainers.appendix_i.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_i.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_i.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_i.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_i.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_i.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-j">
      <h2>{t(lang.current, 'pages.explainers.appendix_j.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_j.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_j.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_j.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_j.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_j.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-k">
      <h2>{t(lang.current, 'pages.explainers.appendix_k.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_k.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_k.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_k.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_k.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_k.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-l">
      <h2>{t(lang.current, 'pages.explainers.appendix_l.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_l.confusion')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_l.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_l.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_l.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_l.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-m">
      <h2>{t(lang.current, 'pages.explainers.appendix_m.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_m.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_m.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_m.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_m.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_m.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="appendix-n">
      <h2>{t(lang.current, 'pages.explainers.appendix_n.heading')}</h2>
      <p class="confusion">{@html t(lang.current, 'pages.explainers.appendix_n.confusion')}</p>
      <p>{@html t(lang.current, 'pages.explainers.appendix_n.p1')}</p>
      <p>{t(lang.current, 'pages.explainers.appendix_n.p2')}</p>
      <p class="limit">{@html t(lang.current, 'pages.explainers.appendix_n.limit')}</p>
      <p class="back-anchor">{@html t(lang.current, 'pages.explainers.appendix_n.back_anchor').replaceAll('__BASE__', base)}</p>
    </section>

    <p class="footer-note">{@html t(lang.current, 'pages.explainers.footer_note')}</p>

  </div>
</main>

<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :global(body) {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 17px;
    line-height: 1.65;
    color: #1a1a1a;
    background: #f9f7f2;
  }
  :global(:root[data-theme="dark"] body) {
    color: #dde2ed;
    background: #1e1f26;
  }

  .page-head {
    background: #1a2e45;
    color: #fff;
    padding: 2rem clamp(1.2rem, 4vw, 3.5rem);
  }
  :global(:root[data-theme="dark"]) .page-head { background: #111722; }

  .header-inner { max-width: 760px; margin: 0 auto; }

  .back-link {
    display: inline-block;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    margin-bottom: 1.1rem;
    padding: 4px 0;
    transition: color 0.15s;
  }
  .back-link:hover { color: #fff; }

  .site-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.55);
    margin-bottom: 0.35rem;
  }

  h1 { font-size: clamp(1.5rem, 4vw, 2.1rem); line-height: 1.2; }

  .meta { font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-top: 0.5rem; }

  main { padding: 2.2rem clamp(1.2rem, 4vw, 3.5rem) 4rem; }

  .content { max-width: 760px; margin: 0 auto; }

  .standfirst {
    font-size: 1.08rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: #333;
  }
  :global(:root[data-theme="dark"]) .standfirst { color: #c4cad8; }

  section { margin-bottom: 2.6rem; }

  h2 {
    font-size: 1.22rem;
    line-height: 1.35;
    margin-bottom: 0.8rem;
    padding-top: 0.5rem;
  }

  p { margin-bottom: 0.9rem; }

  .confusion { color: #555; }
  :global(:root[data-theme="dark"]) .confusion { color: #a8b0c0; }

  .limit {
    border-inline-start: 3px solid #b8860b;
    padding: 0.4rem 0 0.4rem 0.9rem;
    color: #444;
  }
  :global(:root[data-theme="dark"]) .limit { color: #b8c0d0; }

  .back-anchor { font-size: 0.9rem; }
  .back-anchor a, a { color: #1a5c8f; }
  :global(:root[data-theme="dark"]) a { color: #7db3e0; }

  .footer-note {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(128,128,128,0.3);
    font-size: 0.85rem;
    color: #666;
  }
  :global(:root[data-theme="dark"]) .footer-note { color: #98a0b0; }
</style>
