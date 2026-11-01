<!--
  Alberta Electoral Boundary Audit — What the Norms Ask of an Electoral Map
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Created 2026-07-14 (author directive: the audit's discussion has three
  dimensions — law, norms, GIS — and the norms dimension deserves its own page
  that INTERROGATES the norms rather than reciting them, because "the norm was
  broken" is part of the opposition's accusation and an audit cannot borrow an
  accusation unexamined).

  Content grounded in already-verified material only: the landing page's
  Casings 12-14 and Lunty section (en.ts, sourced to CBC/CCLA), the academic
  monograph §5.9 and §7, editorial_history (UK/Australia/US comparators),
  retraction condition 5 (Quebec SCC, April 22, 2026), and the Bratt
  correspondence disclosure. Do not add claims here without verifying them
  there first. English-only for now — pending author review before translation.

  Voice target: Flesch-Kincaid grade ~9. Findings voice; no verdict.
-->
<svelte:head>
  <title>{t(lang.current, 'pages.norms.head_title')}</title>
  <meta name="description" content={t(lang.current, 'pages.norms.head_description')}>
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
  import { lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';
</script>

<div class="page-head">
  <div class="header-inner">
    <a href="{base}/" class="back-link">{t(lang.current, 'pages.norms.back')}</a>
    <div class="header-text">
      <div class="site-label">{t(lang.current, 'pages.norms.site_label')}</div>
      <h1>{t(lang.current, 'pages.norms.h1')}</h1>
      <p class="meta">{t(lang.current, 'pages.norms.meta')}</p>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
  <div class="content">

    <p class="standfirst">{@html t(lang.current, 'pages.norms.standfirst').replaceAll('__BASE__', base)}</p>

    <section id="the-norm">
      <h2>{t(lang.current, 'pages.norms.the_norm.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.the_norm.p1')}</p>
      <p>{t(lang.current, 'pages.norms.the_norm.p2')}</p>
    </section>

    <section id="what-it-bought">
      <h2>{t(lang.current, 'pages.norms.what_it_bought.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.what_it_bought.p1')}</p>
    </section>

    <section id="the-departure">
      <h2>{t(lang.current, 'pages.norms.the_departure.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.the_departure.p1')}</p>
      <p>{@html t(lang.current, 'pages.norms.the_departure.p2')}</p>
    </section>

    <section id="steel-man">
      <h2>{t(lang.current, 'pages.norms.steel_man.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.steel_man.p1')}</p>
      <ul>
        <li>{@html t(lang.current, 'pages.norms.steel_man.li1')}</li>
        <li>{@html t(lang.current, 'pages.norms.steel_man.li2')}</li>
        <li>{@html t(lang.current, 'pages.norms.steel_man.li3')}</li>
        <li>{@html t(lang.current, 'pages.norms.steel_man.li4')}</li>
        <li>{@html t(lang.current, 'pages.norms.steel_man.li5')}</li>
      </ul>
    </section>

    <section id="where-it-bends">
      <h2>{t(lang.current, 'pages.norms.where_it_bends.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.where_it_bends.p1')}</p>
      <ul>
        <li>{@html t(lang.current, 'pages.norms.where_it_bends.li1')}</li>
        <li>{@html t(lang.current, 'pages.norms.where_it_bends.li2')}</li>
        <li>{t(lang.current, 'pages.norms.where_it_bends.li3')}</li>
        <li>{t(lang.current, 'pages.norms.where_it_bends.li4')}</li>
        <li>{t(lang.current, 'pages.norms.where_it_bends.li5')}</li>
        <li>{@html t(lang.current, 'pages.norms.where_it_bends.li6')}</li>
      </ul>
    </section>

    <section id="whose-accusation">
      <h2>{t(lang.current, 'pages.norms.whose_accusation.heading')}</h2>
      <p>{@html t(lang.current, 'pages.norms.whose_accusation.p1')}</p>
      <p>{@html t(lang.current, 'pages.norms.whose_accusation.p2')}</p>
    </section>

    <section id="norms-vs-law">
      <h2>{t(lang.current, 'pages.norms.norms_vs_law.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.norms_vs_law.p1')}</p>
      <p>{@html t(lang.current, 'pages.norms.norms_vs_law.p2')}</p>
    </section>

    <section id="measurable">
      <h2>{t(lang.current, 'pages.norms.measurable.heading')}</h2>
      <p>{@html t(lang.current, 'pages.norms.measurable.p1')}</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>{t(lang.current, 'pages.norms.measurable.table.head.feature')}</th>
              <th>{t(lang.current, 'pages.norms.measurable.table.head.commission')}</th>
              <th>{t(lang.current, 'pages.norms.measurable.table.head.committee')}</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.arms_length_drafting.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.arms_length_drafting.commission')}</td><td class="part">{t(lang.current, 'pages.norms.measurable.table.arms_length_drafting.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.public_hearings_before.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.public_hearings_before.commission')}</td><td class="no">{t(lang.current, 'pages.norms.measurable.table.public_hearings_before.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.draft_published_challenge.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.draft_published_challenge.commission')}</td><td class="no">{t(lang.current, 'pages.norms.measurable.table.draft_published_challenge.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.new_public_submissions.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.new_public_submissions.commission')}</td><td class="no">{t(lang.current, 'pages.norms.measurable.table.new_public_submissions.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.demonstrated_responsiveness.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.demonstrated_responsiveness.commission')}</td><td class="pend">{t(lang.current, 'pages.norms.measurable.table.demonstrated_responsiveness.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.neutral_chair_deciding.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.neutral_chair_deciding.commission')}</td><td class="no">{t(lang.current, 'pages.norms.measurable.table.neutral_chair_deciding.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.opposition_deciding_body.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.opposition_deciding_body.commission')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.opposition_deciding_body.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.published_reasons_contested.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.published_reasons_contested.commission')}</td><td class="pend">{t(lang.current, 'pages.norms.measurable.table.published_reasons_contested.committee')}</td></tr>
            <tr><td>{t(lang.current, 'pages.norms.measurable.table.precedent_conformity.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.precedent_conformity.commission')}</td><td class="no">{t(lang.current, 'pages.norms.measurable.table.precedent_conformity.committee')}</td></tr>
            <tr class="count"><td>{t(lang.current, 'pages.norms.measurable.table.count.feature')}</td><td class="yes">{t(lang.current, 'pages.norms.measurable.table.count.commission')}</td><td>{t(lang.current, 'pages.norms.measurable.table.count.committee')}</td></tr>
          </tbody>
        </table>
      </div>
      <p>{@html t(lang.current, 'pages.norms.measurable.p2')}</p>
      <p>{@html t(lang.current, 'pages.norms.measurable.p3')}</p>
      <p class="draft-note">{@html t(lang.current, 'pages.norms.measurable.draft_note')}</p>
    </section>

    <section>
      <h2>{t(lang.current, 'pages.norms.audits_standing_rule.heading')}</h2>
      <p>{t(lang.current, 'pages.norms.audits_standing_rule.p1')}</p>
      <p class="cross-ref">{@html t(lang.current, 'pages.norms.audits_standing_rule.cross_ref').replaceAll('__BASE__', base)}</p>
      <p class="disclaimer">{t(lang.current, 'pages.norms.audits_standing_rule.disclaimer')}</p>
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
    border-inline-start: 3px solid #7B2D3E;
    padding: 0.2rem 0 0.2rem 1rem;
    margin: 0 0 0.9rem;
    font-style: italic;
    color: #3a3a38;
  }
  :global(:root[data-theme="dark"]) blockquote { color: #b9c0d0; }

  .table-wrap { overflow-x: auto; margin: 0 0 0.9rem; }
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.92rem;
    background: #fff;
  }
  :global(:root[data-theme="dark"]) table { background: #26272f; }
  th, td {
    text-align: left;
    padding: 0.5rem 0.7rem;
    border-bottom: 1px solid rgba(0,0,0,0.1);
    vertical-align: top;
  }
  :global(:root[data-theme="dark"]) th,
  :global(:root[data-theme="dark"]) td { border-bottom-color: rgba(255,255,255,0.12); }
  th { background: rgba(26, 46, 69, 0.07); font-weight: 700; }
  :global(:root[data-theme="dark"]) th { background: rgba(255,255,255,0.06); }
  td.yes  { color: #0F6A5C; font-weight: 600; }
  td.no   { color: #7B2D3E; font-weight: 600; }
  td.part, td.pend { color: #6b5900; font-weight: 600; }
  :global(:root[data-theme="dark"]) td.yes  { color: #4fc3ae; }
  :global(:root[data-theme="dark"]) td.no   { color: #e08a9b; }
  :global(:root[data-theme="dark"]) td.part,
  :global(:root[data-theme="dark"]) td.pend { color: #d4b84a; }
  tr.count td { border-top: 2px solid rgba(0,0,0,0.25); font-weight: 700; }
  :global(:root[data-theme="dark"]) tr.count td { border-top-color: rgba(255,255,255,0.3); }

  .draft-note {
    font-size: 0.92rem;
    color: #55554f;
    border-inline-start: 3px solid #7B2D3E;
    padding: 0.2rem 0 0.2rem 1rem;
  }
  :global(:root[data-theme="dark"]) .draft-note { color: #9aa3b5; }

  a { color: #1a5276; }
  :global(:root[data-theme="dark"]) a { color: #7fb3d5; }

  .cross-ref { font-size: 0.92rem; color: #55554f; }
  :global(:root[data-theme="dark"]) .cross-ref { color: #9aa3b5; }

  .disclaimer {
    font-size: 0.85rem;
    color: #77776f;
    border-top: 1px solid rgba(0,0,0,0.1);
    padding-top: 0.8rem;
    margin-top: 1.6rem;
  }
  :global(:root[data-theme="dark"]) .disclaimer {
    color: #8891a8;
    border-top-color: rgba(255,255,255,0.12);
  }
</style>
