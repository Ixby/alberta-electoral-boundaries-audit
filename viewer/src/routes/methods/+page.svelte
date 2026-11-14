<!--
  Alberta Electoral Boundary Audit — How the Maps Were Tested
  © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>

  Rewritten 2026-07-13 as the grade-8 walkthrough of every test and statistic
  (author directive). Replaces the prior version, which carried three stale or
  retracted claims: "1 in 714,000" (pre-C10 parametric p), "66 of 1,010,000"
  (pre-C10 exceedance count), and "zero in 1,010,000 is an assumption-free
  statement" (the exact framing retracted in the 2026-07-10 dependence-honesty
  correction — autocorrelated chains mean 0 exceedances honestly supports far
  less). Also fixes the quarter-scale --n-steps 252500 reproduce command.

  Content grounded in: data/outputs/simulation_real_map_scores_canonical.json,
  data/outputs/simulated_ensemble_percentiles_canonical.csv,
  data/outputs/simulation_convergence_diagnostics_canonical.json,
  reports/academic/report_academic.md (C10-C13 era), reports/public/report_public.md.
  Every number here must match those artifacts; update them together.
  Reader-facing text lives in en.ts under pages.methods.* so it can be translated
  (other locales fall back to English until they add these keys).

  Voice target: Flesch-Kincaid grade ~8. Short sentences. Everyday analogies.
-->
<svelte:head>
  <title>{t(lang.current, 'pages.methods.head_title')}</title>
  <meta name="description" content={t(lang.current, 'pages.methods.head_description')}>
</svelte:head>

<script lang="ts">
  import { base } from '$app/paths';
  import { lang } from '$lib/i18n/store.svelte';
  import { t } from '$lib/i18n/dict';
  import FigureLightbox from '$lib/components/FigureLightbox.svelte';

  // Locale strings may hold __BASE__ in links; resolve it to the deploy base.
  const h = (key: string) => t(lang.current, key).replaceAll('__BASE__', base);

  const TOC: [string, string][] = [
    ['what-if', 'what_if'], ['percentile', 'percentile'], ['structural', 'structural'],
    ['ballots', 'ballots'], ['fairness', 'fairness'], ['odds', 'odds'], ['died', 'died'],
    ['break', 'break'], ['november', 'november'], ['prereg', 'prereg'],
    ['reproduce', 'reproduce'], ['words', 'words']
  ];
  // The full results table (the main page shows rows 7, 10, 11 and 12).
  const ROWS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'];
  // "Words used on this site", in the order the methods writer set.
  const WORDS = [
    'riding', 'electoral-district', 'mla', 'ucp', 'ndp', 'ebc', 'lunty-committee', 'advisory-panel',
    'ebca', 'charter-s3', 'effective-representation', 'gerrymander', 'cracking', 'packing',
    'anchoring', 'ensemble', 'percentile', 'seats_5050', 'efficiency_gap', 'mean_median', 'declination',
    'hybrid', 'election_day', 'all_ballots', 'reconstruction', 'fsa'
  ];
</script>

<div class="page-head">
  <div class="header-inner">
    <a href="{base}/" class="back-link">{t(lang.current, 'pages.methods.back')}</a>
    <div class="header-text">
      <div class="site-label">{t(lang.current, 'pages.methods.site_label')}</div>
      <h1>{t(lang.current, 'pages.methods.h1')}</h1>
      <p class="meta">{t(lang.current, 'pages.methods.meta')}</p>
    </div>
  </div>
</div>

<main id="main" tabindex="-1">
  <div class="content">

    <p class="standfirst">{@html h('pages.methods.standfirst')}</p>

    <nav class="toc" aria-label={t(lang.current, 'pages.methods.toc.aria')}>
      {#each TOC as [id, key] (id)}
        <a href="#{id}">{t(lang.current, 'pages.methods.toc.' + key)}</a>
      {/each}
    </nav>

    <section id="what-if">
      <span id="ensemble" class="anchor-alias" aria-hidden="true"></span>
      <h2>{t(lang.current, 'pages.methods.what_if.heading')}</h2>
      <p>{@html h('pages.methods.what_if.p1')}</p>
      <p>{@html h('pages.methods.what_if.p2')}</p>
      <p>{@html h('pages.methods.what_if.p3')}</p>
      <p>{@html h('pages.methods.what_if.p4')}</p>
      <ul>
        <li>{@html h('pages.methods.what_if.li1')}</li>
        <li>{@html h('pages.methods.what_if.li2')}</li>
        <li>{@html h('pages.methods.what_if.li3')}</li>
        <li>{@html h('pages.methods.what_if.li4')}</li>
      </ul>
    </section>

    <section id="percentile">
      <h2>{t(lang.current, 'pages.methods.percentile.heading')}</h2>
      <p>{@html h('pages.methods.percentile.p1')}</p>
      <p>{@html h('pages.methods.percentile.p2')}</p>
    </section>

    <section id="structural">
      <h2>{t(lang.current, 'pages.methods.structural.heading')}</h2>
      <p>{@html h('pages.methods.structural.p1')}</p>
      <p>{@html h('home.know.p4')}</p>
      <ul>
        <li>{@html h('pages.methods.structural.li1')}</li>
        <li>{@html h('pages.methods.structural.li2')}</li>
        <li>{@html h('pages.methods.structural.li3')}</li>
        <li>{@html h('pages.methods.structural.li4')}</li>
        <li>{@html h('pages.methods.structural.li5')}</li>
      </ul>
      <p>{@html h('pages.methods.structural.p2')}</p>
    </section>

    <section id="ballots">
      <h2>{t(lang.current, 'pages.methods.ballots.heading')}</h2>
      <p>{@html h('pages.methods.ballots.p1')}</p>
      <p>{@html h('pages.methods.ballots.p2')}</p>
    </section>

    <section id="fairness">
      <h2>{t(lang.current, 'pages.methods.fairness.heading')}</h2>
      <p>{@html h('pages.methods.fairness.p1')}</p>
      <ul>
        <li id="seats-50-50">{@html h('pages.methods.fairness.li1')}</li>
        <li id="efficiency-gap">{@html h('pages.methods.fairness.li2')}</li>
        <li id="mean-median">{@html h('pages.methods.fairness.li3')}</li>
        <li id="declination">{@html h('pages.methods.fairness.li4')}</li>
      </ul>
      <p>{@html h('pages.methods.fairness.p2')}</p>
      <div class="table-wrap" id="results-table">
        <table>
          <thead><tr><th scope="col">{@html h('home.know.table1_h1')}</th><th scope="col">{@html h('home.know.table1_h2')}</th><th scope="col">{@html h('home.know.table1_h3')}</th></tr></thead>
          <tbody>
            {#each ROWS as r (r)}
              <tr><td>{@html h(`home.know.table1_r${r}c1`)}</td><td>{@html h(`home.know.table1_r${r}c2`)}</td><td>{@html h(`home.know.table1_r${r}c3`)}</td></tr>
            {/each}
          </tbody>
        </table>
      </div>
      <figure>
        <picture>
          <source type="image/webp" srcset="{base}/images/stakes_quadrant.webp">
          <img src="{base}/images/stakes_quadrant.jpg" data-full="{base}/images/stakes_quadrant.svg" alt={t(lang.current, 'stakes.scorecard_fig_alt')} class="chart-img" width="474" height="377" loading="lazy" decoding="async">
        </picture>
        <figcaption>{@html h('home.know.fig_caption')}</figcaption>
      </figure>
      <h3 id="what-the-machine-can-t-see">{t(lang.current, 'home.know.h3_6')}</h3>
      <p>{@html h('home.know.p8')}</p>
    </section>

    <section id="odds">
      <h2>{t(lang.current, 'pages.methods.odds.heading')}</h2>
      <p>{@html h('pages.methods.odds.p1')}</p>
      <p>{@html h('pages.methods.odds.p2')}</p>
      <p>{@html h('pages.methods.odds.p3')}</p>
      <p>{@html h('pages.methods.odds.p4')}</p>
    </section>

    <section id="died">
      <h2>{t(lang.current, 'pages.methods.died.heading')}</h2>
      <p>{@html h('pages.methods.died.p1')}</p>
      <ul>
        <li>{@html h('pages.methods.died.li1')}</li>
        <li>{@html h('pages.methods.died.li2')}</li>
      </ul>
    </section>

    <section id="break">
      <h2>{t(lang.current, 'pages.methods.break.heading')}</h2>
      <p>{@html h('pages.methods.break.p1')}</p>
      <ul>
        <li>{@html h('pages.methods.break.li1')}</li>
        <li>{@html h('pages.methods.break.li2')}</li>
        <li>{@html h('pages.methods.break.li3')}</li>
      </ul>
      <p>{@html h('home.know.p7')}</p>
    </section>

    <section id="november">
      <span id="november-test" class="anchor-alias" aria-hidden="true"></span>
      <h2>{t(lang.current, 'home.test.h')}</h2>
      <p>{@html h('home.test.p6')}</p>
      <p>{@html h('home.test.p3')}</p>
      <ul>
        <li>{@html h('home.test.li1')}</li>
        <li>{@html h('home.test.li2')}</li>
      </ul>
      <p>{@html h('home.test.p4')}</p>
    </section>

    <section id="prereg">
      <h2>{t(lang.current, 'pages.methods.prereg.heading')}</h2>
      <p>{@html h('pages.methods.prereg.p1')}</p>
      <p>{@html h('home.know.p2')}</p>
      <p>{@html h('body.about_me.p3')}</p>
    </section>

    <section id="reproduce">
      <h2>{t(lang.current, 'pages.methods.reproduce.heading')}</h2>
      <p>{@html h('pages.methods.reproduce.p1')}</p>
      <pre><code>git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit
git lfs install &amp;&amp; git lfs pull
pip install -r requirements.txt

# regenerate the 1,010,000-map ensemble (long-running; checkpointed;
# --n-steps is the TOTAL across 4 chains)
python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 1010000

# score the real maps against the ensemble
python analysis/scripts/joint_outlier_score_canonical.py</code></pre>
      <p>{@html h('pages.methods.reproduce.p2')}</p>
      <p class="cross-ref">{@html t(lang.current, 'pages.methods.reproduce.cross_ref').replaceAll('__BASE__', base)}</p>
    </section>

    <section id="words">
      <h2>{t(lang.current, 'pages.methods.words.heading')}</h2>
      <dl class="glossary">
        {#each WORDS as w (w)}
          <div class="entry" id={'term-' + w}>
            <dt>{@html h(`glossary.${w}.term`)}</dt>
            <dd>{@html h(`glossary.${w}.definition`)}</dd>
          </div>
        {/each}
      </dl>
    </section>

  </div>
</main>

<FigureLightbox />

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
    margin-bottom: 1.6rem;
  }
  :global(:root[data-theme="dark"]) .standfirst {
    color: #b9c0d0;
    border-inline-start-color: #4a6690;
  }

  .toc {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 0.9rem;
    font-size: 0.88rem;
    margin-bottom: 2.2rem;
    padding: 0.7rem 0.9rem;
    background: rgba(26, 46, 69, 0.05);
    border-radius: 6px;
  }
  :global(:root[data-theme="dark"]) .toc { background: rgba(255,255,255,0.05); }
  .toc a { text-decoration: none; }
  .toc a:hover { text-decoration: underline; }

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

  a { color: #1a5276; }
  :global(:root[data-theme="dark"]) a { color: #7fb3d5; }

  .cross-ref { font-size: 0.92rem; color: #55554f; }
  :global(:root[data-theme="dark"]) .cross-ref { color: #9aa3b5; }

  pre {
    background: #14181f;
    color: #d8dee9;
    padding: 1rem 1.2rem;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.84rem;
    line-height: 1.55;
    margin-bottom: 0.9rem;
  }
  h3 { font-size: 1.05rem; font-weight: 700; margin: 1.4rem 0 0.6rem; }
  .anchor-alias { display: block; height: 0; }
  li[id], .entry { scroll-margin-top: 4rem; }
  .table-wrap { overflow-x: auto; margin: 0 0 1rem; }
  table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
  th, td { border: 1px solid rgba(0,0,0,0.12); padding: 0.45rem 0.6rem; text-align: start; vertical-align: top; }
  :global(:root[data-theme="dark"]) th, :global(:root[data-theme="dark"]) td { border-color: rgba(255,255,255,0.14); }
  figure { margin: 1.2rem 0; text-align: center; }
  .chart-img { max-width: 100%; height: auto; border: 1px solid rgba(0,0,0,0.1); border-radius: 4px; background: #f9f7f2; padding: 0.5rem; }
  figcaption { font-size: 0.82rem; color: #6b6b66; margin-top: 0.4rem; text-align: start; }
  .glossary { display: grid; gap: 0.9rem; }
  .glossary dt { font-weight: 700; }
  .glossary dd { margin: 0.15rem 0 0; }
  code { font-family: ui-monospace, SFMono-Regular, "Cascadia Mono", Consolas, monospace; }
</style>
