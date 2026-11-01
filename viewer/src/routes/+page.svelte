<!--
  Alberta Electoral Boundary Audit — main page
  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  https://ixby.github.io
-->
<svelte:head>
  <title>{t(lang.current, 'head.title')}</title>
  <meta name="description" content={t(lang.current, 'head.meta_description')}>
  <meta name="author" content="Will Conner">
  <meta name="copyright" content="© Will Conner 2026">
  <meta name="license" content="Text/content: CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/); Code: GNU GPL v3.0 (https://www.gnu.org/licenses/gpl-3.0.html)">
  <link rel="icon" type="image/svg+xml" href="{base}/favicon.svg">
  <link rel="apple-touch-icon" href="{base}/favicon.svg">
</svelte:head>

<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { base } from '$app/paths';
  import { goto } from '$app/navigation';

  // "About this translation" help sentence: split the %s link placeholder
  // and inject the live prose word count, mirroring the top disclaimer.
  const translationHelpParts = $derived.by(() => {
    const raw = t(lang.current, 'body.translation_about.p3').replace(
      '{count}',
      proseWordCount.toLocaleString()
    );
    const label = t(lang.current, 'body.translation_about.p3_link');
    const idx = raw.indexOf('%s');
    if (idx < 0) return { pre: raw, label, post: '' };
    return { pre: raw.slice(0, idx), label, post: raw.slice(idx + 2) };
  });
  import { lang } from '$lib/i18n/store.svelte';
  import { proseWordCount } from '$lib/i18n/wordCount';
  import { t } from '$lib/i18n/dict';
  import { sectionNav } from '$lib/sectionNav.svelte';
  import FigureLightbox from '$lib/components/FigureLightbox.svelte';
  import { pageview, initEngagement, observeSections } from '$lib/analytics';

  // Cleanups for the cookieless analytics instrumentation (engaged-time + scroll
  // listeners, and the section-view IntersectionObserver). Detached on destroy.
  let _analyticsCleanups: Array<() => void> = [];

  // Landmark sections. Registered with the site header ($lib/sectionNav), which
  // shows the previous / current / next stepper and lists them in its menu.
  const SECTIONS: { id: string; key: string }[] = [
    { id: 'what-happened',         key: 'happened' },
    { id: 'what-the-map-does',     key: 'does' },
    { id: 'what-the-law-requires', key: 'law' },
    { id: 'how-it-got-here',       key: 'system' },
    { id: 'how-we-know',           key: 'know' },
    { id: 'november-test',         key: 'test' },
    { id: 'change-our-mind',       key: 'mind' },
    { id: 'authors-view',          key: 'authors_view' },
    { id: 'references',            key: 'references' },
    { id: 'resources',             key: 'technical' }
  ];

  onDestroy(() => {
    sectionNav.sections = [];
    sectionNav.current = 0;
    for (const fn of _analyticsCleanups) fn();
    _analyticsCleanups = [];
  });

  onMount(async () => {

    // ── Back-compat: forward old ?poi=<id> deep links to the explorer route ───
    // The map moved to /explorer. A bare /?poi=X link (shared before the move)
    // is redirected there so the pin still focuses. Return early so the rest of
    // the report-page setup is skipped for that navigation.
    const poiParam = new URLSearchParams(location.search).get('poi');
    if (poiParam) {
      goto((base || '') + '/explorer?poi=' + encodeURIComponent(poiParam));
      return;
    }

    // ── Cookieless analytics ────────────────────────────────────────────────
    // Fire the pageview, set up engaged-time + scroll-depth reporting, and
    // observe the major finding sections for section_view. All browser-only and
    // fire-and-forget (the SDK no-ops in SSR); no consent gate — see analytics.ts.
    // Section ids tracked: the report's stake/finding anchors. Kept best-effort —
    // ids that don't exist are simply skipped by observeSections.
    // ── Old anchors (pre-2026-10-29 structure) → their new homes ─────────────
    const oldHash = location.hash.slice(1);
    const moved: Record<string, string> = {
      'the-smoking-gun': '#what-happened', 'the-picture': '#what-happened', 'the-map': '#what-happened',
      'act-1': '#what-the-map-does', 'what-this-means': '#what-the-map-does',
      'act-2': '#how-we-know', 'the-scorecard': '#how-we-know', 'act-3': '#how-it-got-here',
      'section-7': '#november-test', 'retractions': '#change-our-mind',
      'history-of-gerrymandering': '/law', 'canada-is-different': '/law', 'section-8': '/fixes'
    };
    if (/^casing-\d+$/.test(oldHash) || /^act-\d-picture$/.test(oldHash) || oldHash === 'ledger') {
      goto((base || '') + '/evidence#' + oldHash, { replaceState: true });
      return;
    }
    if (moved[oldHash]) {
      const to = moved[oldHash];
      if (to.startsWith('#')) {
        history.replaceState(null, '', to);
        requestAnimationFrame(() => document.getElementById(to.slice(1))?.scrollIntoView());
      } else {
        goto((base || '') + to, { replaceState: true });
        return;
      }
    }

    pageview();
    _analyticsCleanups.push(initEngagement(location.pathname));
    _analyticsCleanups.push(
      observeSections([
        'what-happened',          // the finding, the split, the can/can't box
        'what-the-map-does',      // cracking, packing, the cost, what it buys
        'what-the-law-requires',  // Charter, statute, gaps, the 1992 precedent
        'how-it-got-here',        // the committee, Recommendation 5
        'how-we-know',            // ensemble, results, where the audit lost
        'november-test',          // this week's scoring
        'change-our-mind',        // retraction conditions
        'authors-view',           // severable signed opinion
        'references'              // apparatus
      ])
    );


    // ── Section stepper in the site header: register, then track ─────────────
    sectionNav.sections = SECTIONS;

    // Windowed scroll-spy. Find the last section whose heading has scrolled above
    // a line just under the header; that is the section the reader is currently
    // in. It stays current until the next section's heading crosses the line, so
    // deep scrolling within a section keeps the stepper steady.
    const updateActive = () => {
      const bar = document.querySelector('.site-header .section-bar') ?? document.querySelector('.site-header');
      const headerBottom = bar?.getBoundingClientRect().bottom ?? 44;
      const triggerY = headerBottom + 36;
      let idx = 0;
      for (let i = 0; i < SECTIONS.length; i++) {
        const el = document.getElementById(SECTIONS[i].id);
        if (!el) continue;
        if (el.getBoundingClientRect().top <= triggerY) idx = i;
        else break;
      }
      sectionNav.current = idx;
    };
    window.addEventListener('scroll', updateActive, { passive: true });
    window.addEventListener('resize', updateActive);
    updateActive();

    // ── Vocab term expand/collapse ────────────────────────────────────────────
    document.querySelectorAll('.vocab-term').forEach(btn => {
      btn.addEventListener('click', () => {
        const def = (btn as HTMLElement).dataset.def ?? '';
        const isOpen = btn.getAttribute('aria-expanded') === 'true';
        // Remove any existing panel for this term
        const existing = (btn as HTMLElement).nextElementSibling;
        if (existing && existing.classList.contains('vocab-panel')) existing.remove();
        if (!isOpen) {
          const panel = document.createElement('span');
          panel.className = 'vocab-panel';
          panel.textContent = def;
          (btn as HTMLElement).insertAdjacentElement('afterend', panel);
          btn.setAttribute('aria-expanded', 'true');
        } else {
          btn.setAttribute('aria-expanded', 'false');
        }
      });
    });

  });
</script>

<!-- Lane 1 (statistical / neutral-ensemble) sections — §3 (litmus) and §6 (clean
     gerrymanders) — are shown in full but framed as preliminary pending an
     independent expert review. The banner frames review *status* only; it makes
     no claim about the findings and is distinct from the hero's draft notice. -->
{#snippet preliminaryBanner()}
  <aside class="prelim-banner" role="note" aria-label={t(lang.current, 'body.preliminary.heading')}>
    <svg class="prelim-ico" viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="10.5" cy="10.5" r="6.4" />
      <line x1="15.2" y1="15.2" x2="20.5" y2="20.5" />
      <polyline points="7.8,10.6 9.7,12.5 13.4,8.4" />
    </svg>
    <div class="prelim-text">
      <span class="prelim-badge">{t(lang.current, 'body.preliminary.badge')}</span>
      <p class="prelim-heading">{t(lang.current, 'body.preliminary.heading')}</p>
      <p class="prelim-body">{t(lang.current, 'body.preliminary.body')}</p>
    </div>
  </aside>
{/snippet}


<div class="hero">
  <div class="header-inner">
    <div class="header-text">
      <h1>{t(lang.current, 'home.hero.h1')}</h1>
      <p class="subtitle">{t(lang.current, 'home.hero.subtitle')}</p>
      <p class="subtitle hero-status">{t(lang.current, 'home.hero.status')}</p>
      <span class="badge">{t(lang.current, 'hero.badge')}</span>
      <p class="cover-note">{t(lang.current, 'hero.cover_note')}</p>
    </div>
    <a id="zoom-trigger" href="{base}/explorer" class="hero-map-btn" title={t(lang.current, 'hero.btn_title')} aria-label={t(lang.current, 'hero.btn_aria')}>
      <div class="hero-map-wrap">
        <picture>
          <source type="image/webp" srcset="images/cover_art.webp 680w" sizes="(min-width: 600px) 339px, 90vw">
          <img src="images/cover_art.png" alt={t(lang.current, 'hero.image_alt')} class="header-image" fetchpriority="high" loading="eager" width="680" height="1205">
        </picture>
        <img src="images/province_outline.svg" class="province-border-overlay" aria-hidden="true" alt="" fetchpriority="high" loading="eager">
        <div class="hero-map-hint">{t(lang.current, 'hero.map_hint')}</div>
      </div>
    </a>
  </div>
</div>

<main id="main" class="container" tabindex="-1">

  <div class="callout callout-tldr week-strip" style="border-inline-start-color: #1A7A6E; margin-top: 1.4rem;">
    <p style="margin:0;">{@html t(lang.current, 'home.hero.week')}</p>
  </div>

  <section id="what-happened">
    <h2>{t(lang.current, 'home.happened.h')} <a href="#what-happened" class="section-link" aria-label={t(lang.current, 'home.happened.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.happened.p1')}</p>
    <p>{@html t(lang.current, 'home.happened.p2')}</p>
    <p>{@html t(lang.current, 'home.happened.p3')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.happened.li1')}</li>
      <li>{@html t(lang.current, 'home.happened.li2')}</li>
      <li>{@html t(lang.current, 'home.happened.li3')}</li>
      <li>{@html t(lang.current, 'home.happened.li4')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.happened.p4')}</p>
    <div class="boundary-block">
      <h3 id="what-we-can-say-and-what-we-can-t">{t(lang.current, 'home.happened.box_h')}</h3>
      <ul class="boundary-list">
        <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{@html t(lang.current, 'home.happened.can1')}</span></li>
        <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{@html t(lang.current, 'home.happened.can2')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{@html t(lang.current, 'home.happened.cant1')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{@html t(lang.current, 'home.happened.cant2')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{@html t(lang.current, 'home.happened.cant3')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{@html t(lang.current, 'home.happened.cant4')}</span></li>
      </ul>
    </div>
    <p>{@html t(lang.current, 'home.happened.p5')}</p>
    <p>{@html t(lang.current, 'home.happened.p6').replaceAll('__BASE__', base)}</p>
  </section>

  <section id="what-the-map-does">
    <h2>{t(lang.current, 'home.does.h')} <a href="#what-the-map-does" class="section-link" aria-label={t(lang.current, 'home.does.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.does.p1')}</p>
    <h3 id="one-city-four-districts">{t(lang.current, 'home.does.h3_1')}</h3>
    <p>{@html t(lang.current, 'home.does.p2')}</p>
    <p>{@html t(lang.current, 'home.does.p3')}</p>
    <p>{@html t(lang.current, 'home.does.p4')}</p>
    <h3 id="bigger-districts-where-the-ndp-is-strongest">{t(lang.current, 'home.does.h3_2')}</h3>
    <p>{@html t(lang.current, 'home.does.p5')}</p>
    <h3 id="the-cost-equal-votes">{t(lang.current, 'home.does.h3_3')}</h3>
    <p>{@html t(lang.current, 'home.does.p6')}</p>
    <h3 id="rural-tails-on-urban-districts">{t(lang.current, 'home.does.h3_4')}</h3>
    <p>{@html t(lang.current, 'home.does.p7')}</p>
    <p>{@html t(lang.current, 'home.does.p8')}</p>
    <h3 id="three-boundaries-the-chair-called-out">{t(lang.current, 'home.does.h3_5')}</h3>
    <p>{@html t(lang.current, 'home.does.p9')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.does.li1')}</li>
      <li>{@html t(lang.current, 'home.does.li2')}</li>
      <li>{@html t(lang.current, 'home.does.li3')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.does.p10')}</p>
    <p>{@html t(lang.current, 'home.does.p11')}</p>
    <h3 id="what-it-buys">{t(lang.current, 'home.does.h3_6')}</h3>
    <p>{@html t(lang.current, 'home.does.p12')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.does.li4')}</li>
      <li>{@html t(lang.current, 'home.does.li5')}</li>
      <li>{@html t(lang.current, 'home.does.li6')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.does.p13')}</p>
    <p>{@html t(lang.current, 'home.does.p14')}</p>
    <p>{@html t(lang.current, 'home.does.p15')}</p>
  </section>

  <section id="what-the-law-requires">
    <h2>{t(lang.current, 'home.law.h')} <a href="#what-the-law-requires" class="section-link" aria-label={t(lang.current, 'home.law.h')}>#</a></h2>
    <h3 id="the-constitution">{t(lang.current, 'home.law.h3_1')}</h3>
    <p>{@html t(lang.current, 'home.law.p1')}</p>
    <p>{@html t(lang.current, 'home.law.p2')}</p>
    <p>{@html t(lang.current, 'home.law.p3')}</p>
    <p>{@html t(lang.current, 'home.law.p4')}</p>
    <h3 id="alberta-s-statute">{t(lang.current, 'home.law.h3_2')}</h3>
    <p>{@html t(lang.current, 'home.law.p5')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.law.li1')}</li>
      <li>{@html t(lang.current, 'home.law.li2')}</li>
      <li>{@html t(lang.current, 'home.law.li3')}</li>
      <li>{@html t(lang.current, 'home.law.li4')}</li>
      <li>{@html t(lang.current, 'home.law.li5')}</li>
      <li>{@html t(lang.current, 'home.law.li6')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.law.p6')}</p>
    <h3 id="what-the-law-doesn-t-require">{t(lang.current, 'home.law.h3_3')}</h3>
    <p>{@html t(lang.current, 'home.law.p7')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.law.li7')}</li>
      <li>{@html t(lang.current, 'home.law.li8')}</li>
      <li>{@html t(lang.current, 'home.law.li9')}</li>
      <li>{@html t(lang.current, 'home.law.li10')}</li>
      <li>{@html t(lang.current, 'home.law.li11')}</li>
    </ul>
    <h3 id="it-has-happened-here-before">{t(lang.current, 'home.law.h3_4')}</h3>
    <p>{@html t(lang.current, 'home.law.p8')}</p>
    <p>{@html t(lang.current, 'home.law.p9')}</p>
    <h3 id="what-this-means-in-november">{t(lang.current, 'home.law.h3_5')}</h3>
    <p>{@html t(lang.current, 'home.law.p10')}</p>
  </section>

  <section id="how-it-got-here">
    <h2>{t(lang.current, 'home.system.h')} <a href="#how-it-got-here" class="section-link" aria-label={t(lang.current, 'home.system.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.system.p1')}</p>
    <p>{@html t(lang.current, 'home.system.p2')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.system.li1')}</li>
      <li>{@html t(lang.current, 'home.system.li2')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.system.p3')}</p>
    <p>{@html t(lang.current, 'home.system.p4')}</p>
    <p>{@html t(lang.current, 'home.system.p5')}</p>
    <p>{@html t(lang.current, 'home.system.p6')}</p>
    <p>{@html t(lang.current, 'home.system.p7')}</p>
    <p>{@html t(lang.current, 'home.system.p8')}</p>
    <h3 id="recommendation-5">{t(lang.current, 'home.system.h3_1')}</h3>
    <p>{@html t(lang.current, 'home.system.p9')}</p>
    <p>{@html t(lang.current, 'home.system.p10')}</p>
    <ul class="r5-conditions">
      <li>{@html t(lang.current, 'home.system.li3')}</li>
      <li>{@html t(lang.current, 'home.system.li4')}</li>
      <li>{@html t(lang.current, 'home.system.li5')}</li>
      <li>{@html t(lang.current, 'home.system.li6')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.system.p11').replaceAll('__BASE__', base)}</p>
  </section>

  <section id="how-we-know">
    <h2>{t(lang.current, 'home.know.h')} <a href="#how-we-know" class="section-link" aria-label={t(lang.current, 'home.know.h')}>#</a></h2>
    <h3 id="the-what-if-machine">{t(lang.current, 'home.know.h3_1')}</h3>
    <p>{@html t(lang.current, 'home.know.p1')}</p>
    <p>{@html t(lang.current, 'home.know.p2').replaceAll('__BASE__', base)}</p>
    <h3 id="in-alberta-neutral-is-not-50-50">{t(lang.current, 'home.know.h3_2')}</h3>
    <p>{@html t(lang.current, 'home.know.p3')}</p>
    <h3 id="the-results-side-by-side">{t(lang.current, 'home.know.h3_3')}</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">{@html t(lang.current, 'home.know.table1_h1')}</th><th scope="col">{@html t(lang.current, 'home.know.table1_h2')}</th><th scope="col">{@html t(lang.current, 'home.know.table1_h3')}</th></tr></thead>
        <tbody>
          <tr><td>{@html t(lang.current, 'home.know.table1_r1c1')}</td><td>{@html t(lang.current, 'home.know.table1_r1c2')}</td><td>{@html t(lang.current, 'home.know.table1_r1c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r2c1')}</td><td>{@html t(lang.current, 'home.know.table1_r2c2')}</td><td>{@html t(lang.current, 'home.know.table1_r2c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r3c1')}</td><td>{@html t(lang.current, 'home.know.table1_r3c2')}</td><td>{@html t(lang.current, 'home.know.table1_r3c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r4c1')}</td><td>{@html t(lang.current, 'home.know.table1_r4c2')}</td><td>{@html t(lang.current, 'home.know.table1_r4c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r5c1')}</td><td>{@html t(lang.current, 'home.know.table1_r5c2')}</td><td>{@html t(lang.current, 'home.know.table1_r5c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r6c1')}</td><td>{@html t(lang.current, 'home.know.table1_r6c2')}</td><td>{@html t(lang.current, 'home.know.table1_r6c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r7c1')}</td><td>{@html t(lang.current, 'home.know.table1_r7c2')}</td><td>{@html t(lang.current, 'home.know.table1_r7c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r8c1')}</td><td>{@html t(lang.current, 'home.know.table1_r8c2')}</td><td>{@html t(lang.current, 'home.know.table1_r8c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r9c1')}</td><td>{@html t(lang.current, 'home.know.table1_r9c2')}</td><td>{@html t(lang.current, 'home.know.table1_r9c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r10c1')}</td><td>{@html t(lang.current, 'home.know.table1_r10c2')}</td><td>{@html t(lang.current, 'home.know.table1_r10c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r11c1')}</td><td>{@html t(lang.current, 'home.know.table1_r11c2')}</td><td>{@html t(lang.current, 'home.know.table1_r11c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table1_r12c1')}</td><td>{@html t(lang.current, 'home.know.table1_r12c2')}</td><td>{@html t(lang.current, 'home.know.table1_r12c3')}</td></tr>
        </tbody>
      </table>
    </div>
    <p>{@html t(lang.current, 'home.know.p4')}</p>
    <figure style="margin:1.2rem 0;text-align:center;">
      <picture>
        <source type="image/webp" srcset="images/stakes_quadrant.webp">
        <img src="images/stakes_quadrant.jpg" data-full="images/stakes_quadrant.svg" alt={t(lang.current, 'stakes.scorecard_fig_alt')} class="chart-img" style="max-width: 100%;" width="474" height="377" loading="lazy" decoding="async">
      </picture>
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{@html t(lang.current, 'home.know.fig_caption')}</figcaption>
    </figure>
    <h3 id="what-1-in-568-000-means">{t(lang.current, 'home.know.h3_4')}</h3>
    <p>{@html t(lang.current, 'home.know.p5')}</p>
    <p>{@html t(lang.current, 'home.know.p6')}</p>
    <h3 id="did-the-result-survive-attack">{t(lang.current, 'home.know.h3_5')}</h3>
    <p>{@html t(lang.current, 'home.know.p7')}</p>
    <h3 id="what-the-machine-can-t-see">{t(lang.current, 'home.know.h3_6')}</h3>
    <p>{@html t(lang.current, 'home.know.p8')}</p>
    <h3 id="where-the-audit-lost">{t(lang.current, 'home.know.h3_7')}</h3>
    <p>{@html t(lang.current, 'home.know.p9')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.know.li1')}</li>
      <li>{@html t(lang.current, 'home.know.li2')}</li>
      <li>{@html t(lang.current, 'home.know.li3')}</li>
      <li>{@html t(lang.current, 'home.know.li4')}</li>
      <li>{@html t(lang.current, 'home.know.li5')}</li>
    </ul>
    <h3 id="both-sides-tested">{t(lang.current, 'home.know.h3_8')}</h3>
    <p>{@html t(lang.current, 'home.know.p10')}</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">{@html t(lang.current, 'home.know.table2_h1')}</th><th scope="col">{@html t(lang.current, 'home.know.table2_h2')}</th><th scope="col">{@html t(lang.current, 'home.know.table2_h3')}</th></tr></thead>
        <tbody>
          <tr><td>{@html t(lang.current, 'home.know.table2_r1c1')}</td><td>{@html t(lang.current, 'home.know.table2_r1c2')}</td><td>{@html t(lang.current, 'home.know.table2_r1c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r2c1')}</td><td>{@html t(lang.current, 'home.know.table2_r2c2')}</td><td>{@html t(lang.current, 'home.know.table2_r2c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r3c1')}</td><td>{@html t(lang.current, 'home.know.table2_r3c2')}</td><td>{@html t(lang.current, 'home.know.table2_r3c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r4c1')}</td><td>{@html t(lang.current, 'home.know.table2_r4c2')}</td><td>{@html t(lang.current, 'home.know.table2_r4c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r5c1')}</td><td>{@html t(lang.current, 'home.know.table2_r5c2')}</td><td>{@html t(lang.current, 'home.know.table2_r5c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r6c1')}</td><td>{@html t(lang.current, 'home.know.table2_r6c2')}</td><td>{@html t(lang.current, 'home.know.table2_r6c3')}</td></tr>
          <tr><td>{@html t(lang.current, 'home.know.table2_r7c1')}</td><td>{@html t(lang.current, 'home.know.table2_r7c2')}</td><td>{@html t(lang.current, 'home.know.table2_r7c3')}</td></tr>
        </tbody>
      </table>
    </div>
    <p>{@html t(lang.current, 'home.know.p11')}</p>
    <h3 id="who-did-this">{t(lang.current, 'home.know.h3_9')}</h3>
    <p>{@html t(lang.current, 'home.know.p12')}</p>
    <h3 id="the-full-record">{t(lang.current, 'home.know.h3_10')}</h3>
    <p>{@html t(lang.current, 'home.know.p13').replaceAll('__BASE__', base)}</p>
  </section>

  <section id="november-test">
    <h2>{t(lang.current, 'home.test.h')} <a href="#november-test" class="section-link" aria-label={t(lang.current, 'home.test.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.test.p1')}</p>
    <p>{@html t(lang.current, 'home.test.p2').replaceAll('__BASE__', base)}</p>
    <p>{@html t(lang.current, 'home.test.p3')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.test.li1')}</li>
      <li>{@html t(lang.current, 'home.test.li2')}</li>
    </ul>
    <p>{@html t(lang.current, 'home.test.p4')}</p>
    <p>{@html t(lang.current, 'home.test.p5')}</p>
    <p>{@html t(lang.current, 'home.test.p6')}</p>
    <!-- "The results" slot: filled after the November scoring (see proposals/site_rewrite_2026-10-29). -->
  </section>

  <section id="change-our-mind">
    <h2>{t(lang.current, 'home.mind.h')} <a href="#change-our-mind" class="section-link" aria-label={t(lang.current, 'home.mind.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.mind.p1')}</p>
    <ul>
      <li>{@html t(lang.current, 'home.mind.li1')}</li>
      <li>{@html t(lang.current, 'home.mind.li2')}</li>
      <li>{@html t(lang.current, 'home.mind.li3')}</li>
      <li>{@html t(lang.current, 'home.mind.li4')}</li>
      <li>{@html t(lang.current, 'home.mind.li5').replaceAll('__BASE__', base)}</li>
    </ul>
    <p>{@html t(lang.current, 'home.mind.p2')}</p>
  </section>

  <section id="authors-view">
    <h2>{t(lang.current, 'home.authors.h')} <a href="#authors-view" class="section-link" aria-label={t(lang.current, 'home.authors.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.authors.p1')}</p>
    <p>{@html t(lang.current, 'home.authors.p2')}</p>
    <p>{@html t(lang.current, 'home.authors.p3')}</p>
    <p>{@html t(lang.current, 'home.authors.p4')}</p>
    <p>{@html t(lang.current, 'home.authors.p5')}</p>
    <p>{@html t(lang.current, 'home.authors.p6')}</p>
    <p>{@html t(lang.current, 'home.authors.p7')}</p>
    <p>{@html t(lang.current, 'home.authors.p8')}</p>
    <p style="margin: 1rem 0 1.4rem;">{t(lang.current, 'home.authors.signed')}</p>
    <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">{@html t(lang.current, 'body.authors_view.sources')}</p>
  </section>

  <section id="fixes-teaser">
    <h2>{t(lang.current, 'home.fixes.h')} <a href="#fixes-teaser" class="section-link" aria-label={t(lang.current, 'home.fixes.h')}>#</a></h2>
    <p>{@html t(lang.current, 'home.fixes.p1').replaceAll('__BASE__', base)}</p>
  </section>


  <section id="references">
    <h2>{@html t(lang.current, 'body.references.heading')} <a href="#references" class="section-link" aria-label={t(lang.current, 'body.references.heading_aria')}>#</a></h2>

    <p>{@html t(lang.current, 'body.references.intro')}</p>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: var(--heading-2);">{t(lang.current, 'body.references.h_academic')}</h3>
    <ul style="margin: 0 0 1rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><strong>Alberta Electoral Boundaries Commission. 2026.</strong> <em>2025–26 Electoral Boundaries Commission Final Report (Majority and Minority)</em>. Government of Alberta.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Chen, Jowei, and Jonathan Rodden. 2013.</strong> "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." <em>Quarterly Journal of Political Science</em> 8(3): 239–269.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Courtney, John C. 2001.</strong> <em>Commissioned Ridings: Designing Canada's Electoral Districts</em>. Montreal and Kingston: McGill-Queen's University Press.</li>
      <li style="margin-bottom: 0.5rem;"><strong>DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021.</strong> "Recombination: A Family of Markov Chains for Redistricting." <em>Harvard Data Science Review</em> 3(1). (The ReCom algorithm used to generate the 1,010,000-map ensemble.)</li>
      <li style="margin-bottom: 0.5rem;"><strong>Gelman, Andrew, and Gary King. 1994.</strong> "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." <em>American Journal of Political Science</em> 38(2): 514–554.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020.</strong> "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." <em>American Political Science Review</em> 114(1): 164–178.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Pal, Michael. 2015.</strong> "The Fractured Right to Vote." <em>McGill Law Journal</em> 61(2): 231–274. (Canadian constitutional framework for electoral boundaries.)</li>
      <li style="margin-bottom: 0.5rem;"><strong>Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015.</strong> "Partisan Gerrymandering and the Efficiency Gap." <em>University of Chicago Law Review</em> 82(2): 831–900. (Source of the efficiency gap measure used throughout.)</li>
    </ul>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: var(--heading-2);">{t(lang.current, 'body.references.h_cases')}</h3>
    <ul style="margin: 0 0 1rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>, [1991] 2 SCR 158. (The leading Supreme Court of Canada authority on the constitutional standard for electoral boundary drawing.)</li>
      <li style="margin-bottom: 0.5rem;"><em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679. (Federal Court; leading Canadian authority on community-of-interest evidence in electoral boundary disputes.)</li>
      <li style="margin-bottom: 0.5rem;"><em>Rucho v. Common Cause</em>, 139 S. Ct. 2484 (2019). (U.S. Supreme Court; establishes the non-justiciability of partisan gerrymandering claims in federal courts — context for why Canada's s.3 effective-representation standard differs.)</li>
    </ul>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: var(--heading-2);">{t(lang.current, 'body.references.h_statutes')}</h3>
    <ul style="margin: 0 0 0.5rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><em>Electoral Boundaries Commission Act</em>, RSA 2000, c E-3.</li>
    </ul>
  </section>

  <section id="resources">
    <h2>{t(lang.current, 'body.resources.heading')} <a href="#resources" class="section-link" aria-label={t(lang.current, 'body.resources.heading_aria')}>#</a></h2>

    <ul class="links-list">
      <li>
        <span class="tag">{t(lang.current, 'body.resources.tag_plain')}</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.md">{t(lang.current, 'body.resources.plain_label')}</a> &mdash; {t(lang.current, 'body.resources.plain_desc')}
      </li>
      <li>
        <span class="tag">{t(lang.current, 'body.resources.tag_summary')}</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/FINDINGS_BRIEF.md">{t(lang.current, 'body.resources.summary_label')}</a> &mdash; {t(lang.current, 'body.resources.summary_desc')}
      </li>
      <li>
        <span class="tag">{t(lang.current, 'body.resources.tag_academic')}</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md">{t(lang.current, 'body.resources.academic_label')}</a> &mdash; {t(lang.current, 'body.resources.academic_desc')}
      </li>
      <li>
        <span class="tag">{t(lang.current, 'body.resources.tag_notebook')}</span>
        <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">{t(lang.current, 'body.resources.notebook_label')}</a> &mdash; {t(lang.current, 'body.resources.notebook_desc')}
      </li>
      <li>
        <span class="tag">{t(lang.current, 'body.resources.tag_code')}</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit" rel="noopener">github.com/Ixby/alberta-electoral-boundaries-audit</a>
      </li>
    </ul>
  </section>

  <section id="contact">
    <h2>{t(lang.current, 'body.about_me.heading')}</h2>
    <p style="font-size:0.9rem; color:var(--text-muted);">
      {t(lang.current, 'body.about_me.p1')}
    </p>
    <p style="font-size:0.9rem; color:var(--text-muted);">
      {t(lang.current, 'body.about_me.p2')}
    </p>
    <p style="font-size:0.9rem; color:var(--text-muted);">
      {@html t(lang.current, 'body.about_me.p3')}
    </p>
    <p style="font-size:0.9rem; color:var(--text-muted);">
      {@html t(lang.current, 'body.about_me.p4')} <a href="{base}/feedback">{t(lang.current, 'feedback.nav_link')}</a>
    </p>
  </section>

  {#if lang.current !== 'en'}
    <!-- Rendered only on machine-translated versions — sits under About me so the
         translation provenance reads as part of the audit's transparency
         apparatus, alongside the author's own disclosure. English is the source,
         so it shows no notice; French is now mostly machine-translated, so it does. -->
    <section id="about-translation">
      <h2>{t(lang.current, 'body.translation_about.heading')}</h2>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {t(lang.current, 'body.translation_about.p1')}
      </p>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {t(lang.current, 'body.translation_about.p2')}
      </p>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {translationHelpParts.pre}<a href="{base}/feedback">{translationHelpParts.label}</a>{translationHelpParts.post}
      </p>
    </section>
  {/if}

</main><!-- /.container -->

<a href="#top" id="back-top" aria-label={t(lang.current, 'chrome.back_to_top')}>↑</a>

<div id="site-copyright" aria-label={t(lang.current, 'chrome.license_aria')}>
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="license noopener" title={t(lang.current, 'chrome.license_title')}>
    <!-- Self-hosted official CC badge (2026-07-09): the licensebuttons.net PNG was
         the page's only third-party request — a privacy leak, a resolution-dependent
         raster, and a console error when the CDN is unreachable. SVG scales at any DPR. -->
    <img src="images-local/cc-by-nc-sa.svg" alt={t(lang.current, 'chrome.license_alt')} width="63" height="22">
  </a>
</div>

<FigureLightbox />


<style>
  /* --- Editorial blocks: opener, stakes, boundary card, sections 1/5/6/7 --- */
  :global(.visually-hidden) {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  /* Verdict card — the page's most important element. Front-page treatment:
     an elevated card with a serif headline and the answer set as a pull-quote. */
  /* Opening epigraph — a real exchange framing how to read the cover map, set
     apart from the boxed report blocks with a quieter, more literary treatment. */
  :global(.epigraph-block) {
    margin: 1.6rem 0 0.6rem;
  }
  :global(.epigraph-inner) {
    max-width: var(--measure, 92ch);
    margin-inline: auto;
    padding: clamp(1rem, 3.5vw, 1.8rem) 0;
  }
  :global(.epigraph-quote) {
    margin: 0 0 1.3rem;
    padding-inline-start: 1.15rem;
    border-inline-start: 3px solid var(--border);
    font-family: 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif;
    line-height: 1.6;
  }
  :global(.epigraph-quote p) {
    margin: 0 0 0.6rem;
  }
  :global(.epigraph-quote.reader) {
    color: var(--text-muted);
    font-size: 1.02rem;
    font-style: italic;
  }
  :global(.epigraph-quote.author) {
    color: var(--text);
    border-inline-start-color: var(--link);
    font-size: 1.07rem;
  }
  :global(.epigraph-attrib) {
    font-style: normal;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.02em;
    color: var(--text-subtle);
    margin-top: 0.15rem;
  }
  :global(.epigraph-ethic) {
    margin: 1.2rem 0 0;
    padding-top: 1.1rem;
    border-top: 1px solid var(--border);
    font-family: 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif;
    font-size: 1.12rem;
    line-height: 1.45;
    color: var(--heading);
    font-weight: 600;
  }
  :global(.opener-block) {
    margin-top: 1.4rem;
    background: var(--table-bg, #fff);
    border: 1px solid var(--border);
    border-radius: 10px;
    box-shadow: 0 2px 22px rgba(26, 46, 69, 0.07);
    padding: clamp(1.4rem, 4vw, 2.3rem);
    position: relative;
    overflow: hidden;
  }
  :global(.opener-block)::before {
    content: "";
    position: absolute;
    inset-block-start: 0;
    inset-inline: 0;
    block-size: 4px;
    background: linear-gradient(90deg, var(--heading) 0%, var(--link) 55%, var(--nav-accent) 100%);
  }
  :global(.opener-block h2) {
    font-family: 'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif;
    font-size: clamp(1.5rem, 4.2vw, 1.95rem);
    line-height: 1.18;
    letter-spacing: -0.01em;
    color: var(--heading);
    margin: 0 0 1rem;
    font-weight: 600;
  }
  :global(.opener-block p) {
    font-size: 1.02rem;
    line-height: 1.7;
    color: var(--lead);
    margin: 0 0 0.85rem;
    max-width: var(--measure);
  }
  :global(.opener-block p:last-child) {
    margin-block-end: 0;
  }
  :global(.verdict-answer) {
    font-family: 'Palatino Linotype', Palatino, Georgia, serif;
    font-size: clamp(1.2rem, 3.4vw, 1.45rem);
    font-weight: 600;
    line-height: 1.35;
    color: var(--heading);
    margin: 1.15rem 0;
    padding-inline-start: 1rem;
    border-inline-start: 3px solid var(--link);
    max-width: var(--measure);
  }
  :global(.verdict-aside) {
    margin-block-start: 1.35rem;
    padding-block-start: 0.95rem;
    border-block-start: 1px solid var(--border-subtle);
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text-subtle);
  }
  :global(.stakes-block) {
    margin-top: 1.5rem;
    padding: 1.5rem 1.2rem;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg-alt);
  }
  :global(.stakes-q) { margin-bottom: 1.1rem; }
  :global(.stakes-q:last-of-type) { margin-bottom: 1.4rem; }
  :global(.stakes-q h3) {
    font-size: 1.1rem;
    color: var(--heading);
    margin: 0 0 0.4rem;
    font-weight: 600;
  }
  :global(.stakes-q p) { margin: 0; line-height: 1.6; color: var(--text); }
  :global(.stakes-q em) { font-style: italic; }
  :global(.stakes-footnote) {
    margin-top: 0.6rem !important;
    font-size: 0.85rem;
    color: var(--text-muted, #666);
    line-height: 1.5;
    border-inline-start: 2px solid var(--border-subtle);
    padding-inline-start: 0.7rem;
  }
  :global(.stakes-scorecard) {
    margin: 1.6rem 0 1.4rem;
    padding: 1.1rem 1.2rem 1.2rem;
    border: 1px solid var(--border);
    border-inline-start: 3px solid var(--nav-accent);
    border-radius: 6px;
    background: var(--bg);
  }
  :global(.stakes-scorecard h3) {
    margin: 0 0 0.5rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    color: var(--heading);
  }
  :global(.stakes-scorecard-intro) {
    margin: 0 0 0.9rem !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
    color: var(--text-muted) !important;
  }
  :global(.stakes-scorecard-fig) {
    margin: 0.4rem 0 1.1rem;
    text-align: center;
  }
  :global(.stakes-scorecard-fig img) {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
  }
  :global(.stakes-scorecard-fig figcaption) {
    margin-top: 0.5rem;
    font-size: 0.82rem;
    line-height: 1.45;
    color: var(--text-muted);
    text-align: start;
  }
  :global(.stakes-scorecard-close) {
    margin: 0.9rem 0 0 !important;
    font-size: 0.92rem !important;
    font-style: italic;
    color: var(--text) !important;
    text-align: center;
  }

  :global(.stakes-ctas) {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem 1rem;
    border-top: 1px solid var(--border-subtle);
    padding-top: 1rem;
  }
  :global(.stakes-cta) {
    text-decoration: none;
    color: var(--link);
    font-weight: 500;
    font-size: 0.95rem;
  }
  :global(.stakes-cta:hover) { text-decoration: underline; }

  .back-link {
    margin-top: 1.4rem;
    font-size: 0.88rem;
    text-align: end;
  }
  .back-link a {
    /* was hardcoded #5d5d5b (2.48:1 on the dark surface — WCAG AA failure);
       the theme variable adapts per surface (2026-07-08) */
    color: var(--text-subtle);
    text-decoration: none;
    border-bottom: 1px dotted var(--border);
    padding-bottom: 1px;
    transition: color 0.15s ease, border-color 0.15s ease;
  }
  .back-link a:hover {
    color: var(--link);
    border-bottom-color: var(--link);
  }
  :global(.boundary-block) {
    margin-top: 1.2rem;
    padding: 1.2rem 1.2rem 1.4rem;
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
  }
  :global(.boundary-block h2) {
    font-size: 1rem;
    color: var(--heading);
    margin: 0 0 0.9rem;
    font-weight: 600;
    letter-spacing: 0.01em;
  }
  :global(.boundary-list) {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 0.5rem;
  }
  :global(.boundary-list .row) {
    display: grid;
    grid-template-columns: 1.5rem 1fr;
    align-items: start;
    gap: 0.4rem;
    padding: 0.4rem 0;
    border-bottom: 1px dashed var(--border-subtle);
    font-size: 0.95rem;
    line-height: 1.55;
  }
  :global(.boundary-list .row:last-child) { border-bottom: 0; }
  :global(.boundary-list .mark) {
    font-weight: 700;
    font-size: 1.05rem;
    line-height: 1.5;
    text-align: center;
  }
  :global(.boundary-list .can .mark) { color: #2c7a4a; }
  :global(.boundary-list .cant .mark) { color: #a8423b; }
  :global(.boundary-list .text) { color: var(--text); }

  /* Emphasized closing line of a Story section — lighter echo of the verdict pull-quote. */
  :global(.section-punch) {
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--heading-2);
    margin-block-start: 1.2rem;
    padding-inline-start: 1rem;
    border-inline-start: 3px solid var(--nav-accent);
    max-width: var(--measure);
  }

  :global(.editorial-block) {
    padding: 2rem 0 1.6rem;
    border-top: 1px solid var(--border-subtle);
  }
  :global(.editorial-block:first-of-type) {
    border-top: 0;
    margin-top: 1.4rem;
  }
  :global(.editorial-block h2) {
    font-size: 1.45rem;
    color: var(--heading);
    margin: 0 0 1rem;
    font-weight: 600;
    line-height: 1.3;
  }
  :global(.editorial-block h3.rung) {
    font-size: 1.05rem;
    color: var(--heading-2);
    margin: 1.4rem 0 0.4rem;
    font-weight: 600;
  }
  :global(.editorial-block p) {
    margin: 0 0 0.9rem;
    line-height: 1.65;
    color: var(--text);
    max-width: var(--measure);
  }
  :global(.editorial-block p:last-of-type) { margin-bottom: 0; }
  :global(.editorial-block em) { font-style: italic; color: var(--text); }
  :global(.ladder-questions) {
    list-style: none;
    padding: 0;
    margin: 0 0 1rem;
    display: grid;
    gap: 0.4rem;
    counter-reset: ladder;
  }
  :global(.ladder-questions li) {
    display: grid;
    grid-template-columns: 1.7rem 1fr;
    gap: 0.5rem;
    align-items: baseline;
    padding: 0.5rem 0.8rem;
    background: var(--bg-alt);
    border-inline-start: 3px solid var(--link);
    border-radius: 3px;
    counter-increment: ladder;
  }
  :global(.ladder-questions li::before) {
    content: counter(ladder) ".";
    color: var(--link);
    font-weight: 600;
  }
  :global(.ladder-questions strong) {
    font-weight: 500;
    color: var(--heading);
  }

  :global {
:root {
  --bg:              #f9f7f2;
  --bg-alt:          #f5f5f5;
  --text:            #1a1a1a;
  --text-muted:      #444;
  --text-subtle:     #666;
  --lead:            #333;
  --heading:         #1a2e45;
  --heading-2:       #243b53;
  --link:            #1a5276;
  --border:          #ddd;
  --border-subtle:   #e8e8e8;
  --table-bg:        #fff;
  --row-hover:       #f4f6f8;
  --callout-bg:      #eaf1f8;
  --callout-warn:    #fdfbe4;
  --tag-bg:          #dce6f0;
  --tag-text:        #1a3550;
  --nav-bg:          #1e3552;
  --nav-accent:      #6FD3FB;
  /* Single reading measure for all running Story prose. Figures, the map
     explorer, and tables stay full-width; only paragraphs are constrained
     to a comfortable line length. Change here, not per-block. */
  --measure:         92ch;
  /* Desktop shell: the page sits in a centered 1200px card on a darker,
     blue-tinted surround (--shell-outer), lifted by a thin frame + shadow. */
  --shell-outer:     #d0d9e8;
  --shell-frame:     rgba(26, 46, 69, 0.18);
}
:root[data-theme="dark"] {
  --bg:            #1e1f26;
  --shell-outer:   #0c0f1a;
  --shell-frame:   rgba(120, 170, 210, 0.14);
  --bg-alt:        #26272f;
  --text:          #dde2ed;
  --text-muted:    #9ea8c0;
  --text-subtle:   #8891a8; /* raised from #7a8296 2026-07-08: 4.26:1 on the dark surface failed WCAG AA (4.5:1); #8891a8 gives 5.21:1 */
  --lead:          #b8c2d8;
  --heading:       #9eb8d0;
  --heading-2:     #8aa6be;
  --link:          #6ab0d8;
  --border:        #38394a;
  --border-subtle: #2e2f3e;
  --table-bg:      #26272f;
  --row-hover:     #2e303a;
  --callout-bg:    #1c253a;
  --callout-warn:  #2a2300;
  --tag-bg:        #252f45;
  --tag-text:      #9ab8d4;
  --nav-bg:        #1a1e2d;
  --nav-accent:    #4FC3F7;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 17px;
      line-height: 1.65;
      color: var(--text);
      /* Outer surround behind the centered desktop shell. The shell itself
         repaints var(--bg) over the reading area (see .app-shell in layout). */
      background: var(--shell-outer);
    }

    a { color: var(--link); }
    a:hover { text-decoration: underline; }

    .hero {
      background: #1a2e45;
      color: #fff;
      padding: 2.5rem clamp(1.2rem, 4vw, 3.5rem) 2rem;
      display: flex;
      flex-direction: column;
      justify-content: center;
      box-sizing: border-box;
      /* A tall title card, but deliberately SHORTER than the viewport so the
         top of the report prose peeks above the fold — readers need to see
         there's a document underneath, not a full-screen cover that reads as
         the whole page. 72svh leaves a consistent strip of the next section
         visible; svh accounts for mobile UI chrome. */
      min-height: calc(72svh - 2.75rem);
    }
    /* The site header's section stepper hangs over the top of the hero from
       721px up (see SiteHeader.svelte); reserve that strip. */
    @media (min-width: 721px) {
      .hero { padding-top: calc(2.5rem + 2.75rem); }
    }

    .header-inner {
      max-width: 1060px;
      margin: 0 auto;
      display: flex;
      align-items: flex-start;
      gap: 2.5rem;
    }

    .header-text {
      flex: 0 1 500px;
      min-width: 0;
    }

    .hero h1 {
      font-size: clamp(1.4rem, 4vw, 2.1rem);
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.3;
      margin-bottom: 0.5rem;
    }

    .hero .subtitle {
      font-size: 1rem;
      opacity: 0.78;
    }

    .hero .badge {
      display: inline-block;
      margin-top: 1rem;
      padding: 0.25rem 0.75rem;
      border: 1px solid rgba(255,255,255,0.4);
      border-radius: 3px;
      font-size: 0.82rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.85);
    }

    .hero-map-btn {
      background: none; border: none; padding: 0;
      flex-shrink: 0; cursor: zoom-in;
      display: block;
    }
    /* Hydration gap: the renderer choice is not yet known, so the launch button
       is busy. Subtle affordance only — the cover art stays at full opacity; the
       map hint dims and shows a small spinner, and the cursor reads "wait". */
    .hero-map-btn.is-loading { cursor: wait; }
    .hero-map-btn.is-loading .hero-map-hint {
      opacity: 0.7;
    }
    .hero-map-btn.is-loading .hero-map-hint::before {
      content: "";
      display: inline-block;
      width: 0.7em; height: 0.7em;
      margin-inline-end: 0.45em;
      vertical-align: -0.08em;
      border: 2px solid rgba(255,255,255,0.45);
      border-top-color: rgba(255,255,255,0.95);
      border-radius: 50%;
      animation: hero-map-spin 0.7s linear infinite;
    }
    @keyframes hero-map-spin { to { transform: rotate(360deg); } }
    @media (prefers-reduced-motion: reduce) {
      .hero-map-btn.is-loading .hero-map-hint::before { animation: none; }
    }
    .hero-map-wrap {
      position: relative;
      display: inline-block;
    }
    .province-border-overlay {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }
    .hero-map-hint {
      position: absolute;
      bottom: 0.7rem;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(26,46,69,0.82);
      color: rgba(255,255,255,0.9);
      font-size: 0.72rem;
      padding: 0.3rem 0.75rem;
      border-radius: 20px;
      white-space: nowrap;
      pointer-events: none;
      letter-spacing: 0.03em;
      /* Soft yellow glow (the explorer's accent, #f5c518) so the launch pill
         reads as the thing to press; a touch brighter on hover/focus. */
      border: 1px solid rgba(245,197,24,0.65);
      box-shadow: 0 0 8px 1px rgba(245,197,24,0.45), 0 0 20px 6px rgba(245,197,24,0.18);
      transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .hero-map-btn:hover .hero-map-hint,
    .hero-map-btn:focus-visible .hero-map-hint {
      border-color: rgba(245,197,24,0.9);
      box-shadow: 0 0 10px 2px rgba(245,197,24,0.6), 0 0 26px 8px rgba(245,197,24,0.26);
    }
    .header-image {
      /* Larger chrome subtraction (was 140px) so on shorter screens the cover
         art leaves room for the prose strip below the fold. */
      max-height: min(600px, calc(100svh - 230px));
      width: auto;
      display: block;
      border-radius: 6px;
    }

    @media (max-width: 660px) {
      .hero { padding: 0; }
      .header-inner { flex-direction: column; gap: 0; align-items: stretch; }
      .header-text { flex: none; padding: 1.3rem 1.2rem 1.2rem; order: 2; }
      .hero-map-btn { order: 1; width: 100%; display: block; flex-shrink: 0; }
      .hero-map-wrap { display: block; width: 100%; overflow: hidden; }
      .header-image {
        width: 100%; height: 56vw; max-height: none;
        object-fit: cover; object-position: 35% 62%; border-radius: 0;
      }
      .province-border-overlay { display: none; }
      .cover-note { display: none; }
    }

    .cover-note {
      font-size: 0.78rem;
      opacity: 0.62;
      margin-top: 0.85rem;
      line-height: 1.5;
      max-width: 380px;
    }

    .section-link {
      color: transparent;
      font-size: 0.72em;
      font-weight: 400;
      margin-inline-start: 0.4em;
      text-decoration: none;
      vertical-align: middle;
      transition: color 0.15s;
      user-select: none;
    }
    h2:hover .section-link, .section-link:hover, .section-link:focus {
      color: #6b8eb0;
      text-decoration: none;
    }

    /* One reading column for ALL prose blocks (opener, stakes, boundary,
       editorial, and the body sections in <main>). The full-bleed hero and
       the interactive map explorer live outside .container, so this never
       touches them. Reverses an earlier "let prose fill the container"
       direction — the container IS the measure now. */
    .container {
      width: 100%;
      max-width: 1000px;
      margin-inline: auto;
      padding: 0 clamp(1.2rem, 4vw, 3.5rem);
      box-sizing: border-box;
    }

    section { padding: 2.2rem 0 1.8rem; border-bottom: 1px solid var(--border); scroll-margin-top: 1rem; }
    section:last-of-type { border-bottom: none; }

    /* "Preliminary findings — pending expert review" banner at the head of the
       two Lane 1 (statistical) sections. Amber, deliberately distinct from the
       blue info callouts; frames review status only, never the findings. */
    .prelim-banner {
      display: flex;
      align-items: flex-start;
      gap: 0.95rem;
      margin: 0.4rem 0 1.6rem;
      padding: 1.05rem 1.2rem 1.1rem;
      border: 1px solid #e3c78a;
      border-inline-start: 5px solid #b7791f;
      border-radius: 8px;
      background: linear-gradient(180deg, #fdf4dd 0%, #fbedc8 100%);
      box-shadow: 0 1px 3px rgba(120, 84, 12, 0.12);
    }
    .prelim-ico {
      flex: none;
      width: 30px;
      height: 30px;
      margin-top: 0.1rem;
      fill: none;
      stroke: #b7791f;
      stroke-width: 1.9;
      stroke-linecap: round;
      stroke-linejoin: round;
    }
    .prelim-text { min-width: 0; }
    .prelim-badge {
      display: inline-block;
      margin-bottom: 0.4rem;
      padding: 0.16rem 0.55rem;
      border-radius: 3px;
      background: #8c5a12;
      color: #fff;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }
    .prelim-heading {
      margin: 0 0 0.3rem;
      font-weight: 700;
      font-size: 1.02rem;
      line-height: 1.3;
      color: #7a530f;
    }
    .prelim-body {
      margin: 0;
      font-size: 0.92rem;
      line-height: 1.55;
      color: #6b4e1c;
    }
    :root[data-theme="dark"] .prelim-banner {
      border-color: #5a4717;
      border-inline-start-color: #d6a93b;
      background: linear-gradient(180deg, #2a2410 0%, #221d0c 100%);
      box-shadow: none;
    }
    :root[data-theme="dark"] .prelim-ico { stroke: #e2b84e; }
    :root[data-theme="dark"] .prelim-badge { background: #d6a93b; color: #201a0a; }
    :root[data-theme="dark"] .prelim-heading { color: #f0d28a; }
    :root[data-theme="dark"] .prelim-body { color: #d8c79c; }

    /* The stakes and boundary blocks anchor on a visually-hidden h2 inside the
       section, not on the section itself, so the section rule's scroll-margin
       doesn't apply when those ids are the jump target. Match the offset on
       the h2 ids directly so back-links land at the heading rather than
       behind the sticky nav. */
    #stakes-heading, #boundary-heading { scroll-margin-top: 1rem; }
    /* NOTE: these sections used to carry content-visibility:auto with a
       600px contain-intrinsic-size placeholder as a below-the-fold paint
       optimization. Removed deliberately: every one of them is an anchor
       target from the nav, and the placeholder estimate made anchor jumps
       land mid-paragraph — the browser scrolled to where the section would
       be if the skipped sections above it were really 600px each, then
       they rendered at true height (3000–6000px) and pushed the target
       far below the viewport. Anchor correctness beats a paint
       micro-optimization on prose. */

    h2 {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 0.9rem;
      color: var(--heading);
      letter-spacing: -0.005em;
    }
    section h2:not(.visually-hidden)::before {
      content: '';
      display: block;
      width: 28px;
      height: 2px;
      background: var(--nav-accent);
      border-radius: 1px;
      margin-bottom: 0.55rem;
      opacity: 0.85;
    }

    h3 {
      font-size: 1rem;
      font-weight: 600;
      margin: 1.3rem 0 0.4rem;
      color: var(--heading-2);
    }

    p { margin-bottom: 0.9rem; }

    /* Story narrative sections that render as bare running prose share the
       one reading measure, matching the opener and editorial blocks. Later
       body sections (3+) mix cards, tables, and figures and keep their own
       layout widths; they are addressed in the consolidation pass. */
    #section-1 p,
    #section-2 p,
    #section-2 ol { max-width: var(--measure); }

    .lead {
      font-size: 1.08rem;
      line-height: 1.7;
      color: var(--lead);
    }

    /* Findings cards */
    .findings-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 1rem;
      margin: 1.2rem 0;
    }

    .card {
      background: var(--bg-alt);
      border: 1px solid var(--border);
      border-radius: 5px;
      padding: 1.1rem 1.1rem 1rem;
    }

    .card .label {
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-subtle);
      margin-bottom: 0.3rem;
    }

    .card .number {
      font-size: 1.9rem;
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 0.25rem;
    }

    .card .number.neutral { color: #1a5276; }
    .card .number.flag    { color: #6B35A7; }
    :root[data-theme="dark"] .card .number.neutral { color: #6ab0d8; }
    :root[data-theme="dark"] .card .number.flag    { color: #c090f0; }

    .card .description {
      font-size: 0.86rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* Summary table */
    .table-wrap { overflow-x: auto; margin: 1.2rem 0; }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      background: var(--table-bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      overflow: hidden;
    }

    th {
      background: #1a2e45;
      color: #fff;
      font-weight: 600;
      padding: 0.55rem 0.8rem;
      text-align: start;
    }
    /* Links inside the dark table header need a light color (AA on #1a2e45). */
    th a { color: #bcd4ee; }

    td {
      padding: 0.5rem 0.8rem;
      border-top: 1px solid var(--border-subtle);
      vertical-align: top;
    }

    tr:hover td { background: var(--row-hover); }

    td.flag { color: #6B35A7; font-weight: 600; }
    td.normal { color: #1A7A6E; }
    :root[data-theme="dark"] td.flag   { color: #c090f0; }
    :root[data-theme="dark"] td.normal { color: #3dcfba; }

    /* Callout box */
    .callout {
      background: var(--callout-bg);
      border-inline-start: 4px solid var(--link);
      padding: 0.9rem 1.1rem;
      border-start-start-radius: 0; border-start-end-radius: 4px;
      border-end-end-radius: 4px; border-end-start-radius: 0;
      margin: 1.1rem 0;
      font-size: 0.94rem;
    }

    .callout.warning {
      background: var(--callout-warn);
      border-inline-start-color: #b7950b;
    }

    .callout-minority { background: #F0EBF8; }
    .callout-tldr     { background: #D0EEEA; }
    .callout-info     { background: #EAF3FF; }
    .callout-neutral  { background: #F5F5F5; }

    :root[data-theme="dark"] .callout-minority { background: #1e1230; }
    :root[data-theme="dark"] .callout-tldr     { background: #0c2520; }
    :root[data-theme="dark"] .callout-info     { background: #111e2e; }
    :root[data-theme="dark"] .callout-neutral  { background: #26272f; }

    .chart-img {
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      /* Fixed to the figures' own baked-in paper (#f9f7f2 = light --bg) so the
         plate and the figure surface are one continuous sheet in both themes;
         dark mode dims the plate via the filter below. */
      background: #f9f7f2;
      padding: 0.5rem;
      /* Raster figures (WebP/JPEG) stretch rather than letterbox, so the
         height must follow the width when max-width shrinks it on phones. */
      height: auto;
    }
    :root[data-theme="dark"] .chart-img { filter: brightness(0.88) contrast(0.95); }

    /* Recommendation 5 conditions (a)–(d) in the Lunty section */
    .r5-conditions { margin: 0.4rem 0 1rem; padding-inline-start: 1.3rem; }
    .r5-conditions li { margin-bottom: 0.55rem; }

    /* Links section */
    .links-list {
      list-style: none;
      padding: 0;
    }

    .links-list li {
      padding: 0.4rem 0;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 0.94rem;
    }

    .links-list li:last-child { border-bottom: none; }

    .links-list .tag {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 0.1rem 0.4rem;
      border-radius: 3px;
      background: var(--tag-bg);
      color: var(--tag-text);
      margin-inline-end: 0.4rem;
      vertical-align: middle;
    }

    @media (max-width: 700px) {
      .header-inner { flex-direction: column; gap: 1.5rem; }
      .header-image { max-height: min(300px, 45svh); }
    }

    @media (max-width: 540px) {
      .findings-grid { grid-template-columns: 1fr; }
    }

  /* Expandable detail panels — follow visual language */
  :global(details.audit-detail) {
    margin: 0.8rem 0 1rem;
    border-inline-start: 3px solid rgba(107,53,167,0.55);
    background: rgba(107,53,167,0.05);
    border-start-start-radius: 0; border-start-end-radius: 4px;
    border-end-end-radius: 4px; border-end-start-radius: 0;
    padding: 0.45rem 0;
    padding-inline-start: 0.9rem;
  }
  :global(details.audit-detail summary) {
    cursor: pointer; list-style: none; user-select: none;
    font-weight: 600; font-size: 0.9rem; color: #6B35A7;
  }
  :root[data-theme="dark"] :global(details.audit-detail summary) { color: #b48fd4; }
  :global(details.audit-detail summary::-webkit-details-marker) { display: none; }
  :global(details.audit-detail summary::before) { content: '▶ '; font-size: 0.7em; }
  :global(details.audit-detail[open] summary::before) { content: '▼ '; }
  :global(details.audit-detail[open] summary) { margin-bottom: 0.5rem; }
  :global(.audit-detail-body) { font-size: 0.91rem; line-height: 1.65; color: inherit; }
  :global(.audit-detail-body p) { margin: 0 0 0.5rem; }
  /* Vocab term — inline expandable definitions */
  :global(.vocab-term) {
    border-bottom: 1.5px dashed rgba(107,53,167,0.55);
    cursor: pointer; color: inherit;
    display: inline; background: none; border-top: none; border-inline-start: none; border-inline-end: none;
    font: inherit; padding: 0; text-align: start;
  }
  :global(.vocab-term:hover) { border-bottom-color: #6B35A7; }
  :global(.vocab-panel) {
    display: block;
    background: rgba(107,53,167,0.07); border-inline-start: 3px solid #6B35A7;
    border-start-start-radius: 0; border-start-end-radius: 4px; border-end-end-radius: 4px; border-end-start-radius: 0; padding: 0.3rem 0.8rem; margin: 0.35rem 0;
    font-size: 0.86rem; line-height: 1.5; color: var(--text);
  }
  /* In-article anomaly trigger */
  .anomaly-trigger {
    display: inline-block;
    text-decoration: none;
    background: #fff3e0;
    border: 1px solid rgba(200,110,0,0.4);
    border-radius: 5px;
    color: #7a3e00;
    cursor: pointer;
    font-size: 0.84rem;
    font-family: inherit;
    padding: 0.3rem 1rem;
    transition: background 0.12s;
  }
  .anomaly-trigger:hover { background: #ffe0b2; border-color: rgba(200,110,0,0.7); }
  .anomaly-trigger.tb-layer-on { background: #ffe0b2; border-color: rgba(200,110,0,0.7); font-weight: 600; }
  :global(:root[data-theme="dark"]) .anomaly-trigger {
    background: rgba(200,110,0,0.18); border-color: rgba(200,130,0,0.5); color: #f0c07a;
  }
  :global(:root[data-theme="dark"]) .anomaly-trigger:hover,
  :global(:root[data-theme="dark"]) .anomaly-trigger.tb-layer-on {
    background: rgba(200,110,0,0.28); border-color: rgba(200,150,0,0.65);
  }

  /* Inline "show ↗" ED buttons */
  .ed-trigger {
    display: inline-flex;
    align-items: center;
    padding: 0.05em 0.42em 0.08em;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 3px;
    color: var(--link);
    font-size: 0.77em;
    font-family: inherit;
    cursor: pointer;
    vertical-align: middle;
    line-height: 1.4;
    transition: background 0.12s, border-color 0.12s;
    white-space: nowrap;
    margin-inline-start: 0.2em;
  }
  .ed-trigger:hover {
    background: var(--callout-bg);
    border-color: var(--link);
  }

  /* Flagged-district overlay animations — opacity-only keyframes so the
     filter is baked into the static rule and never repainted per-frame */
  @keyframes anomaly-pulse {
    0%, 100% { opacity: 0.90; }
    50%       { opacity: 0.42; }
  }
  @keyframes anomaly-glow-pulse {
    0%, 100% { opacity: 0.18; }
    50%       { opacity: 0.45; }
  }
  @keyframes anomaly-fill-pulse {
    0%, 100% { opacity: 0.85; }
    50%       { opacity: 0.38; }
  }
  .anomaly-pulse-path {
    filter: drop-shadow(0 0 2px #e63946);
    will-change: opacity;
    animation: anomaly-pulse 2.4s ease-in-out infinite;
  }
  .anomaly-glow-path {
    will-change: opacity;
    animation: anomaly-glow-pulse 2.4s ease-in-out infinite;
  }
  .anomaly-fill-path {
    will-change: opacity;
    animation: anomaly-fill-pulse 2.4s ease-in-out infinite;
  }

  @media (prefers-reduced-motion: reduce) {
    :global(.anomaly-pulse-path),
    :global(.anomaly-glow-path),
    :global(.anomaly-fill-path) {
      animation: none !important;
    }
  }

  }

  /* Persistent CC badge */
  #site-copyright {
    position: fixed; bottom: 0.45rem; inset-inline-end: 1rem;
    z-index: 300; opacity: 0.45; pointer-events: auto;
    transition: opacity 0.15s;
  }
  #site-copyright:hover { opacity: 0.85; }
  /* padding+negative margin expands the tap target of the 80x15 CC badge to
     ~92x27px (Lighthouse target-size fix, 2026-07-08) without moving it */
  #site-copyright a { display: block; line-height: 0; padding: 6px; margin: -6px; }
  #site-copyright img { display: block; }
  :root[data-theme="dark"] #site-copyright { opacity: 0.3; }
  :root[data-theme="dark"] #site-copyright:hover { opacity: 0.7; }

  /* Back-to-top button */
  #back-top {
    /* bottom raised 1.6rem -> 3rem (2026-07-09): the button's tap area overlapped
       the fixed CC-badge target below it — Lighthouse target-size failure */
    position: fixed; bottom: 3rem; inset-inline-end: 1.4rem;
    width: 2.6rem; height: 2.6rem;
    background: #6B35A7; color: #fff;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; text-decoration: none;
    opacity: 0.72; transition: opacity 0.2s;
    z-index: 200;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  }
  #back-top:hover { opacity: 1; }
  @media (max-width: 600px) { #back-top { bottom: 2.75rem; inset-inline-end: 0.8rem; } }
</style>
