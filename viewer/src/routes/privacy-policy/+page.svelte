<!--
  Alberta Electoral Boundary Audit — Privacy Policy
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
-->
<svelte:head>
  <title>{t(lang.current, 'pages.privacy_policy.head_title')}</title>
  <meta name="description" content={t(lang.current, 'pages.privacy_policy.head_description')}>
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
  import { lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';
</script>

<div class="page-head">
  <div class="header-inner">
    <a href="{base}/" class="back-link">{t(lang.current, 'pages.privacy_policy.back')}</a>
    <div class="header-text">
      <div class="site-label">{t(lang.current, 'pages.privacy_policy.site_label')}</div>
      <h1>{t(lang.current, 'pages.privacy_policy.h1')}</h1>
      <p class="meta">{t(lang.current, 'pages.privacy_policy.meta')}</p>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
  <div class="policy">

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.overview.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.overview.p1')}</p>
      <p>{t(lang.current, 'pages.privacy_policy.overview.p2')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.how_analytics_work.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.how_analytics_work.p1')}</p>
      <p>{@html t(lang.current, 'pages.privacy_policy.how_analytics_work.p2')}</p>
      <p>{t(lang.current, 'pages.privacy_policy.how_analytics_work.p3')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.measured.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.measured.p1')}</p>
      <ul>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li1')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li2')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li3')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li4')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li5')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li6')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li7')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li8')}</li>
        <li>{t(lang.current, 'pages.privacy_policy.measured.li9')}</li>
      </ul>
      <p>{t(lang.current, 'pages.privacy_policy.measured.p2')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.never_collected.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.never_collected.p1')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.github_pages_collects.heading')}</h2>
      <p>{@html t(lang.current, 'pages.privacy_policy.github_pages_collects.p1')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.share_codes.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.share_codes.p1')}</p>
      <p>{t(lang.current, 'pages.privacy_policy.share_codes.p2')}</p>
      <p>{t(lang.current, 'pages.privacy_policy.share_codes.p3')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.cookies_browser_storage.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.cookies_browser_storage.p1')}</p>
      <p>{@html t(lang.current, 'pages.privacy_policy.cookies_browser_storage.p2')}</p>
      <ul>
        <li>{@html t(lang.current, 'pages.privacy_policy.cookies_browser_storage.li1')}</li>
        <li>{@html t(lang.current, 'pages.privacy_policy.cookies_browser_storage.li2')}</li>
        <li>{@html t(lang.current, 'pages.privacy_policy.cookies_browser_storage.li3')}</li>
        <li>{@html t(lang.current, 'pages.privacy_policy.cookies_browser_storage.li4')}</li>
      </ul>
      <p>{t(lang.current, 'pages.privacy_policy.cookies_browser_storage.p3')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.data_retention.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.data_retention.p1')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.your_choices.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.your_choices.p1')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.contact.heading')}</h2>
      <p>{t(lang.current, 'pages.privacy_policy.contact.p1')}</p>
      <p>{@html t(lang.current, 'pages.privacy_policy.contact.p2').replaceAll('__BASE__', base)}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.privacy_policy.policy_updates.heading')}</h2>
      <p>{@html t(lang.current, 'pages.privacy_policy.policy_updates.p1')}</p>
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
  :global(:root[data-theme="dark"]) .page-head {
    background: #111722;
  }

  .header-inner {
    max-width: 760px;
    margin: 0 auto;
  }

  .back-link {
    display: inline-block;
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    font-size: 0.85rem;
    margin-bottom: 1.1rem;
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

  .meta {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.55);
  }

  main {
    padding: 2.5rem clamp(1.2rem, 4vw, 3.5rem) 4rem;
  }

  .policy {
    max-width: 760px;
    margin: 0 auto;
  }

  section {
    margin-bottom: 2.4rem;
    padding-bottom: 2.4rem;
    border-bottom: 1px solid #e0ddd6;
  }
  :global(:root[data-theme="dark"]) section {
    border-bottom-color: #2e3040;
  }
  section:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }

  h2 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a2e45;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
  }
  :global(:root[data-theme="dark"]) h2 { color: #a8c4e0; }

  p { margin-bottom: 0.85rem; }
  p:last-child { margin-bottom: 0; }

  ul {
    padding-inline-start: 1.4rem;
    margin-bottom: 0.85rem;
  }
  li { margin-bottom: 0.45rem; }

  em { font-style: italic; }

  a { color: #1a5276; }
  a:hover { text-decoration: underline; }
  :global(:root[data-theme="dark"]) a { color: #6aaddb; }

  @media (max-width: 600px) {
    h2 { font-size: 1.05rem; }
    main { padding-top: 1.8rem; }
  }
</style>
