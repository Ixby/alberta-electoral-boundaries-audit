<!--
  Alberta Electoral Boundary Audit — What the Law Asks of an Electoral Map
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Content grounded in reports/academic/report_academic.md §2 (legal-context
  literature review, corrected 2026-06-12 per T1.7 referee findings), §5.1.4–
  §5.1.5 (EBCA §15(2) statutory text and eligibility audit), and the public
  report's legal-terminology box. Every citation below appears in those
  verified sections; do not add case law here without verifying it there first.
  Reader-facing text lives in en.ts under pages.law.* so it can be translated
  (other locales fall back to English until they add these keys).
-->
<svelte:head>
  <title>{t(lang.current, 'pages.law.head_title')}</title>
  <meta name="description" content={t(lang.current, 'pages.law.head_description')}>
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
  import { lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';
</script>

<div class="page-head">
  <div class="header-inner">
    <a href="{base}/" class="back-link">{t(lang.current, 'pages.law.back')}</a>
    <div class="header-text">
      <div class="site-label">{t(lang.current, 'pages.law.site_label')}</div>
      <h1>{t(lang.current, 'pages.law.h1')}</h1>
      <p class="meta">{t(lang.current, 'pages.law.meta')}</p>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
  <div class="content">

    <p class="standfirst">{t(lang.current, 'pages.law.standfirst')}</p>

    <section id="why-not-gerrymander">
      <h2>{t(lang.current, 'pages.law.why_not_gerrymander.heading')}</h2>
      <p>{t(lang.current, 'pages.law.why_not_gerrymander.p1')}</p>
      <p>{@html t(lang.current, 'pages.law.why_not_gerrymander.p2')}</p>
      <p>{@html t(lang.current, 'pages.law.why_not_gerrymander.p3')}</p>
    </section>

    <section id="effective-representation">
      <h2>{t(lang.current, 'pages.law.effective_representation.heading')}</h2>
      <p>{@html t(lang.current, 'pages.law.effective_representation.p1')}</p>
      <p>{@html t(lang.current, 'pages.law.effective_representation.p2')}</p>
      <p>{t(lang.current, 'pages.law.effective_representation.p3')}</p>
      <ul>
        <li>{@html t(lang.current, 'pages.law.effective_representation.li1')}</li>
        <li>{@html t(lang.current, 'pages.law.effective_representation.li2')}</li>
      </ul>
      <p>{t(lang.current, 'pages.law.effective_representation.p4')}</p>
    </section>

    <section id="ebca">
      <h2>{t(lang.current, 'pages.law.ebca.heading')}</h2>
      <p>{@html t(lang.current, 'pages.law.ebca.p1')}</p>
      <p>{@html t(lang.current, 'pages.law.ebca.p2')}</p>
      <p>{@html t(lang.current, 'pages.law.ebca.p3')}</p>
      <ul class="criteria">
        <li>{t(lang.current, 'pages.law.ebca.criterion1')}</li>
        <li>{t(lang.current, 'pages.law.ebca.criterion2')}</li>
        <li>{t(lang.current, 'pages.law.ebca.criterion3')}</li>
        <li>{t(lang.current, 'pages.law.ebca.criterion4')}</li>
        <li>{t(lang.current, 'pages.law.ebca.criterion5')}</li>
      </ul>
      <p>{t(lang.current, 'pages.law.ebca.p4')}</p>
      <blockquote>{t(lang.current, 'pages.law.ebca.quote')}</blockquote>
      <p>{t(lang.current, 'pages.law.ebca.p5')}</p>
      <p>{@html t(lang.current, 'pages.law.ebca.p6')}</p>
      <p class="cross-ref">{@html t(lang.current, 'pages.law.ebca.cross_ref')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.law.audits_standing_rule.heading')}</h2>
      <p>{t(lang.current, 'pages.law.audits_standing_rule.p1')}</p>
      <p class="cross-ref">{@html t(lang.current, 'pages.law.audits_standing_rule.cross_ref').replaceAll('__BASE__', base)}</p>
      <p class="disclaimer">{t(lang.current, 'pages.law.audits_standing_rule.disclaimer')}</p>
    </section>

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

  h1 {
    font-size: clamp(1.4rem, 4vw, 1.9rem);
    font-weight: 700;
    letter-spacing: -0.01em;
    line-height: 1.25;
    margin-bottom: 0.4rem;
  }

  .meta { font-size: 0.82rem; color: rgba(255,255,255,0.55); }

  main { padding: 2.2rem clamp(1.2rem, 4vw, 3.5rem) 4rem; }
  .content { max-width: 760px; margin: 0 auto; }

  .standfirst {
    font-size: 1.06rem;
    color: #3a3a38;
    border-inline-start: 3px solid #1a2e45;
    padding-inline-start: 1rem;
    margin-bottom: 2.2rem;
  }
  :global(:root[data-theme="dark"]) .standfirst {
    color: #b9c0d0;
    border-inline-start-color: #4a6690;
  }

  section { margin-bottom: 2.4rem; scroll-margin-top: 1.5rem; }

  h2 {
    font-size: 1.22rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
  }

  p { margin-bottom: 0.9rem; }

  ul { margin: 0 0 0.9rem 1.4rem; }
  li { margin-bottom: 0.7rem; }

  blockquote {
    margin: 0 0 0.9rem;
    padding: 0.8rem 1.1rem;
    border-inline-start: 3px solid #7B2D3E;
    background: rgba(26, 46, 69, 0.06);
    border-radius: 0 6px 6px 0;
    font-style: italic;
  }
  :global(:root[data-theme="dark"]) blockquote {
    background: rgba(255, 255, 255, 0.05);
  }

  a { color: #1a5276; }
  :global(:root[data-theme="dark"]) a { color: #7fb3d5; }

  .cross-ref { font-size: 0.92rem; color: #55554f; }
  :global(:root[data-theme="dark"]) .cross-ref { color: #9aa3b5; }

  .disclaimer {
    font-size: 0.88rem;
    font-style: italic;
    color: #6b6b65;
    border-top: 1px solid rgba(128,128,128,0.25);
    padding-top: 0.9rem;
  }
  :global(:root[data-theme="dark"]) .disclaimer { color: #8891a8; }
</style>
