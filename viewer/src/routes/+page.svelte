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
  import { getStoredTheme, storeTheme } from '$lib/prefs';
  import { lang } from '$lib/i18n/store.svelte';
  import { proseWordCount } from '$lib/i18n/wordCount';
  import { t } from '$lib/i18n/dict';
  import LanguageSelector from '$lib/components/LanguageSelector.svelte';
  import { focusTrap } from '$lib/a11y/focusTrap';
  import { pageview, initEngagement, observeSections } from '$lib/analytics';

  // Cleanups for the cookieless analytics instrumentation (engaged-time + scroll
  // listeners, and the section-view IntersectionObserver). Detached on destroy.
  let _analyticsCleanups: Array<() => void> = [];

  // ── Share state ───────────────────────────────────────────────────────────
  let navOpen           = $state(false);
  let navScrolled       = $state(false);
  // Windowed scroll-spy: the index of the section currently under the nav line.
  // The sticky bar shows only the previous / current / next section, sliding as
  // the reader scrolls, instead of laying every landmark out at once.
  let currentIdx        = $state(0);
  const SECTIONS: { id: string; key: string }[] = [
    { id: 'the-smoking-gun',          key: 'smoking_gun' },
    { id: 'the-picture',              key: 'picture' },
    { id: 'the-map',                  key: 'map' },
    { id: 'act-1',                    key: 'act1' },
    { id: 'what-this-means',          key: 'for_you' },
    { id: 'history-of-gerrymandering', key: 'history_full' },
    { id: 'canada-is-different',      key: 'canada' },
    { id: 'act-2',                    key: 'act2' },
    { id: 'act-3',                    key: 'act3' },
    { id: 'the-scorecard',            key: 'revisited' },
    { id: 'section-7',                key: 'lunty' },
    { id: 'authors-view',             key: 'authors_view' },
    { id: 'section-8',                key: 'suggestions' },
    { id: 'retractions',              key: 'retractions' },
    { id: 'references',               key: 'references' },
    { id: 'resources',                key: 'technical' }
  ];
  let darkMode          = $state(false);

  function toggleTheme() {
    darkMode = !darkMode;
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
    storeTheme(darkMode ? 'dark' : 'light');
  }

  function toggleNavDrawer() {
    navOpen = !navOpen;
  }
  function closeNavDrawer() {
    if (!navOpen) return;
    navOpen = false;
  }

  onDestroy(() => {
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
    pageview();
    _analyticsCleanups.push(initEngagement(location.pathname));
    _analyticsCleanups.push(
      observeSections([
        'the-smoking-gun',       // the cold open / evidence-log frame
        'the-picture',           // the whole case in one image
        'the-map',               // how to read the cover map
        'act-1',                 // what the map does (casings 1-5)
        'what-this-means',       // editorial: what this means for you
        'history-of-gerrymandering',
        'canada-is-different',
        'act-2',                 // what the simulation sees (casings 6-10)
        'act-3',                 // what people did (casings 11-14)
        'the-scorecard',         // the synthesis
        'section-7',             // the Lunty committee map
        'authors-view',          // severable signed opinion
        'section-8',             // suggested reforms
        'retractions',           // documented corrections
        'references'             // apparatus
      ])
    );

    // ── Dark mode — respects OS preference; user override persisted in cookie ──
    const storedTheme = await getStoredTheme();
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    darkMode = storedTheme === 'dark' || (storedTheme === null && prefersDark);
    // app.html inline script already set the attribute to avoid FOUC; sync state var only

    // ── Lightbox ───────────────────────────────────────────────────────────
    const lb = document.getElementById('fig-lightbox') as HTMLElement;
    const lbImg = document.getElementById('fig-lightbox-img') as HTMLImageElement;
    let lbPrevFocus: Element | null = null;
    let lbScale = 1;
    let lbPtrs: Map<number, {x: number; y: number}> = new Map();
    let lbPinchDist = 0;

    function lbApply() {
      lbImg.style.transform = `scale(${lbScale})`;
    }

    function openLb(src: string, altText = '') {
      lbScale = 1; lbImg.style.transform = '';
      lbImg.src = src;
      lbImg.alt = altText;
      lb.style.display = 'flex';
      lbPrevFocus = document.activeElement;
      lb.focus();
    }
    function closeLb() {
      lb.style.display = 'none';
      if (lbPrevFocus instanceof HTMLElement) lbPrevFocus.focus();
      lbPrevFocus = null;
    }

    lb.addEventListener('wheel', (e) => {
      e.preventDefault();
      const f = (e as WheelEvent).deltaY < 0 ? 1.15 : (1 / 1.15);
      lbScale = Math.max(0.5, Math.min(8, lbScale * f));
      lbApply();
    }, { passive: false });

    lb.addEventListener('pointerdown', (e) => {
      lbPtrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (lbPtrs.size === 2) {
        const pts = Array.from(lbPtrs.values());
        lbPinchDist = Math.hypot(pts[1].x - pts[0].x, pts[1].y - pts[0].y);
      }
    });
    lb.addEventListener('pointermove', (e) => {
      if (!lbPtrs.has(e.pointerId)) return;
      lbPtrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (lbPtrs.size === 2) {
        const pts = Array.from(lbPtrs.values());
        const d = Math.hypot(pts[1].x - pts[0].x, pts[1].y - pts[0].y);
        if (lbPinchDist > 0) {
          lbScale = Math.max(0.5, Math.min(8, lbScale * d / lbPinchDist));
          lbApply();
        }
        lbPinchDist = d;
      }
    });
    lb.addEventListener('pointerup', (e) => { lbPtrs.delete(e.pointerId); lbPinchDist = 0; });
    lb.addEventListener('pointercancel', (e) => { lbPtrs.delete(e.pointerId); lbPinchDist = 0; });
    lb.addEventListener('dblclick', () => { lbScale = 1; lbApply(); });

    document.querySelectorAll('figure img').forEach(img => {
      (img as HTMLElement).addEventListener('click', () => openLb((img as HTMLImageElement).src, (img as HTMLImageElement).alt));
    });
    lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
    (document.getElementById('fig-lightbox-close') as HTMLElement)?.addEventListener('click', closeLb);
    lb.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeLb();
      if (e.key === 'Tab') { e.preventDefault(); (document.getElementById('fig-lightbox-close') as HTMLElement)?.focus(); }
    });

    // ── Nav: scroll shadow + active-landmark tracking ─────────────────────────
    const onScroll = () => { navScrolled = window.scrollY > 8; };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    // Windowed scroll-spy. Find the last section whose heading has scrolled above
    // a line just under the nav; that is the section the reader is currently in.
    // It stays current until the next section's heading crosses the line, so deep
    // scrolling within a section keeps the bar steady. currentIdx drives the
    // previous / current / next window rendered in the bar.
    const updateActive = () => {
      const triggerY = 80;
      let idx = 0;
      for (let i = 0; i < SECTIONS.length; i++) {
        const el = document.getElementById(SECTIONS[i].id);
        if (!el) continue;
        if (el.getBoundingClientRect().top <= triggerY) idx = i;
        else break;
      }
      currentIdx = idx;
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

<a class="skip-link" href="#main">{t(lang.current, 'nav.skip_to_content')}</a>

<nav aria-label="Page sections" class:scrolled={navScrolled}>
  <div class="nav-inner">
    <a href="#top" class="nav-home" aria-label={t(lang.current, 'nav.home_aria')}><svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 2L2 9h2v9h5v-5h2v5h5V9h2L10 2z"/></svg></a>
    <div class="nav-landmarks" aria-label={t(lang.current, 'nav.nav_aria')}>
      {#if currentIdx > 0}
        <a class="nav-step nav-prev" href={'#' + SECTIONS[currentIdx - 1].id} title={t(lang.current, 'nav.' + SECTIONS[currentIdx - 1].key)}>
          <span class="nav-chev" aria-hidden="true">‹</span><span class="nav-step-lbl">{t(lang.current, 'nav.' + SECTIONS[currentIdx - 1].key)}</span>
        </a>
      {:else}
        <span class="nav-step nav-edge" aria-hidden="true"></span>
      {/if}
      <span class="nav-step nav-current" aria-current="location">{t(lang.current, 'nav.' + SECTIONS[currentIdx].key)}</span>
      {#if currentIdx < SECTIONS.length - 1}
        <a class="nav-step nav-next" href={'#' + SECTIONS[currentIdx + 1].id} title={t(lang.current, 'nav.' + SECTIONS[currentIdx + 1].key)}>
          <span class="nav-step-lbl">{t(lang.current, 'nav.' + SECTIONS[currentIdx + 1].key)}</span><span class="nav-chev" aria-hidden="true">›</span>
        </a>
      {:else}
        <span class="nav-step nav-edge" aria-hidden="true"></span>
      {/if}
    </div>
    <div class="nav-tools">
      <LanguageSelector />
      <button id="theme-toggle" class="nav-theme-btn" aria-label={t(lang.current, 'nav.theme_aria')} title={t(lang.current, 'nav.theme_title')} onclick={toggleTheme}>
        <svg class="icon-sun" width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-9a1 1 0 0 0 1-1V2a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm0 14a1 1 0 0 0 1-1v-1a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm7-7a1 1 0 0 0 0-2h-1a1 1 0 0 0 0 2h1zM4 10a1 1 0 0 0-1-1H2a1 1 0 0 0 0 2h1a1 1 0 0 0 1-1zm10.95-4.95a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm-9.9 9.9a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm9.9.01a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71zm-9.9-9.9a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71z"/></svg>
        <svg class="icon-moon" width="14" height="14" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M17.293 13.293A8 8 0 0 1 6.707 2.707a8.001 8.001 0 1 0 10.586 10.586z"/></svg>
      </button>
      <button id="hamburger" class="nav-hamburger" aria-label={t(lang.current, 'nav.nav_aria')} aria-expanded={navOpen} aria-controls="nav-drawer"
        onclick={toggleNavDrawer}>
        <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor" aria-hidden="true">
          {#if navOpen}
            <path d="M2 2l14 14M2 16L16 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/>
          {:else}
            <rect y="2"  width="18" height="2" rx="1"/>
            <rect y="8"  width="18" height="2" rx="1"/>
            <rect y="14" width="18" height="2" rx="1"/>
          {/if}
        </svg>
      </button>
    </div>
  </div>
  {#if navOpen}
  <div id="nav-drawer" role="dialog" aria-modal="true" aria-label={t(lang.current, 'nav.nav_aria')} use:focusTrap={{ onEscape: () => navOpen = false }}>
    <a href="#top" class="drawer-top" onclick={closeNavDrawer}>{t(lang.current, 'nav.drawer_top')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_overview')}</h4>
    <a href="#the-smoking-gun" onclick={closeNavDrawer}>{t(lang.current, 'nav.smoking_gun')}</a>
    <a href="#the-picture" onclick={closeNavDrawer}>{t(lang.current, 'nav.picture')}</a>
    <a href="#the-map" onclick={closeNavDrawer}>{t(lang.current, 'nav.map')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_audit')}</h4>
    <a href="#act-1" onclick={closeNavDrawer}>{t(lang.current, 'nav.act1')}</a>
    <a href="#what-this-means" onclick={closeNavDrawer}>{t(lang.current, 'nav.for_you')}</a>
    <a href="#act-2" onclick={closeNavDrawer}>{t(lang.current, 'nav.act2')}</a>
    <a href="#act-3" onclick={closeNavDrawer}>{t(lang.current, 'nav.act3')}</a>
    <a href="#the-scorecard" onclick={closeNavDrawer}>{t(lang.current, 'nav.revisited')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_context')}</h4>
    <a href="#history-of-gerrymandering" onclick={closeNavDrawer}>{t(lang.current, 'nav.history_full')}</a>
    <a href="#canada-is-different" onclick={closeNavDrawer}>{t(lang.current, 'nav.canada')}</a>
    <a href="#section-7" onclick={closeNavDrawer}>{t(lang.current, 'nav.lunty')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_forward')}</h4>
    <a href="#authors-view" onclick={closeNavDrawer}>{t(lang.current, 'nav.authors_view')}</a>
    <a href="#section-8" onclick={closeNavDrawer}>{t(lang.current, 'nav.suggestions')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_apparatus')}</h4>
    <a href="#retractions" onclick={closeNavDrawer}>{t(lang.current, 'nav.retractions')}</a>
    <a href="#references" onclick={closeNavDrawer}>{t(lang.current, 'nav.references')}</a>
    <a href="#resources" onclick={closeNavDrawer}>{t(lang.current, 'nav.technical')}</a>
    <a href="{base}/feedback" onclick={closeNavDrawer}>{t(lang.current, 'nav.feedback')}</a>
  </div>
  {/if}
</nav>

<header>
  <div class="header-inner">
    <div class="header-text">
      <h1>{t(lang.current, 'hero.h1')}</h1>
      <p class="subtitle">{t(lang.current, 'hero.subtitle')}</p>
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
</header>

<section class="epigraph-block container" aria-labelledby="epigraph-heading">
  <h2 id="epigraph-heading" class="visually-hidden">{t(lang.current, 'epigraph.heading')}</h2>
  <div class="epigraph-inner">
    <blockquote class="epigraph-quote reader">
      <p>{t(lang.current, 'epigraph.reader')}</p>
      <p class="epigraph-attrib">— {t(lang.current, 'epigraph.reader_label')}</p>
    </blockquote>
    <blockquote class="epigraph-quote author">
      <p>{t(lang.current, 'epigraph.author_p1')}</p>
      <p>{t(lang.current, 'epigraph.author_p2')}</p>
      <p class="epigraph-attrib">— {t(lang.current, 'epigraph.author_label')}</p>
    </blockquote>
  </div>
</section>

<main id="main" class="container" tabindex="-1">

  <section id="the-smoking-gun">
    <h2>{t(lang.current, 'body.casings.frame_h')} <a href="#the-smoking-gun" class="section-link" aria-label={t(lang.current, 'nav.smoking_gun')}>#</a></h2>
    <p class="section-punch">{t(lang.current, 'body.casings.frame_p1')}</p>
    <p>{t(lang.current, 'body.casings.frame_p1b')}</p>
    <p>{t(lang.current, 'body.casings.frame_p2')}</p>
    <p>{t(lang.current, 'body.casings.frame_p3')}</p>
    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li><strong>{t(lang.current, 'body.casings.beat_found')}</strong> — {t(lang.current, 'body.casings.beat_found_d')}</li>
      <li><strong>{t(lang.current, 'body.casings.beat_show')}</strong> — {t(lang.current, 'body.casings.beat_show_d')}</li>
      <li><strong>{t(lang.current, 'body.casings.beat_experts')}</strong> — {t(lang.current, 'body.casings.beat_experts_d')}</li>
      <li><strong>{t(lang.current, 'body.casings.beat_canada')}</strong> — {t(lang.current, 'body.casings.beat_canada_d')}</li>
      <li><strong>{t(lang.current, 'body.casings.beat_gun')}</strong> — {t(lang.current, 'body.casings.beat_gun_d')}</li>
    </ol>
    <p>{t(lang.current, 'body.casings.frame_p4')}</p>
    <p>{t(lang.current, 'body.casings.frame_p5')}</p>
    <p>{t(lang.current, 'body.casings.frame_coi')}</p>
    <p>{@html t(lang.current, 'body.casings.frame_routes').replaceAll('__BASE__', base)}</p>
    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.legal_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.legal_body')}</p>
    </div>
    <div class="boundary-block">
      <h3>{t(lang.current, 'verdict.box_heading')}</h3>
      <ul class="boundary-list">
        <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{t(lang.current, 'verdict.box_can_1')}</span></li>
        <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{t(lang.current, 'verdict.box_can_2')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_1')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_2')}</span></li>
        <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_3')}</span></li>
      </ul>
    </div>
  </section>

  <section id="the-picture">
    <h2>{t(lang.current, 'picture.heading')} <a href="#the-picture" class="section-link" aria-label={t(lang.current, 'nav.picture')}>#</a></h2>
    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/stakes_quadrant.svg" alt={t(lang.current, 'stakes.scorecard_fig_alt')} class="chart-img" style="max-width: 100%;" width="474" height="346" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'stakes.scorecard_fig_caption')}</figcaption>
    </figure>
    <p>{t(lang.current, 'picture.lead')}</p>
    <div class="callout callout-tldr" style="border-inline-start-color: #1A7A6E; font-size: 1.02rem; line-height: 1.65;">
      <p style="margin:0 0 0.6rem;"><strong>{t(lang.current, 'top_callouts.tldr_label')}</strong></p>
      <p style="margin:0 0 0.6rem;">{@html t(lang.current, 'top_callouts.tldr_p1')}</p>
      <p style="margin:0 0 0.6rem;">{@html t(lang.current, 'top_callouts.tldr_p2')}</p>
      <p style="margin:0;">{t(lang.current, 'top_callouts.tldr_p3')}</p>
      <p style="margin:0.6rem 0 0; font-size:0.88rem; color:var(--text-muted);">{@html t(lang.current, 'top_callouts.tldr_footer').replace('%s', '<a href=\"#retractions\">' + t(lang.current, 'top_callouts.tldr_footer_link') + '</a>')}</p>
    </div>
  </section>

  <section id="the-map">
    <h2>{t(lang.current, 'body.the_map.heading2')} <a href="#the-map" class="section-link" aria-label={t(lang.current, 'nav.map')}>#</a></h2>
    <p>{t(lang.current, 'body.the_map.p1')}</p>
    <p>{t(lang.current, 'body.the_map.p2')}</p>
    <p>{t(lang.current, 'body.the_map.p3')}</p>
    <p>{t(lang.current, 'body.the_map.p4')}</p>
    <p>{t(lang.current, 'body.the_map.p5')}</p>
  </section>

  <section id="act-1">
    <h2>{t(lang.current, 'body.casings.act1_h')} <a href="#act-1" class="section-link" aria-label={t(lang.current, 'nav.act1')}>#</a></h2>
    <p>{t(lang.current, 'body.casings.act1_intro')}</p>
    <h3 id="casing-1">{t(lang.current, 'body.casings.c1_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c1_found')}</p>
    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/figure_airdrie_v3.svg" alt={t(lang.current, 'body.cpd.fig_alt')} class="chart-img" style="max-width: 100%;" width="504" height="336" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.cpd.fig_caption')}</figcaption>
    </figure>
    <p style="text-align:center; margin: 0.2rem 0 1.1rem;">
      <a class="anomaly-trigger" href="{base}/explorer?poi=airdrie-split">{t(lang.current, 'body.cpd.airdrie_btn')}</a>
    </p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c1_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c1_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c1_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c1_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-a">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c1_app')}</a></p>
    <h3 id="casing-2">{t(lang.current, 'body.casings.c2_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c2_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c2_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c2_experts')}</p>
    <p style="margin: 0.2rem 0 0.9rem;"><a href="{base}/explorer?poi=banff-town">{t(lang.current, 'body.casings.c2_banff_link')} ↗</a></p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c2_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c2_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-b">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c2_app')}</a></p>
    <h3 id="casing-3">{t(lang.current, 'body.casings.c3_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c3_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c3_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c3_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c3_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c3_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-c">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c3_app')}</a></p>
    <h3 id="casing-4">{t(lang.current, 'body.casings.c4_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c4_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c4_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c4_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c4_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c4_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-d">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c4_app')}</a></p>
    <h3 id="casing-5">{t(lang.current, 'body.casings.c5_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c5_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c5_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c5_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c5_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c5_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain_not_even')}</strong> — <a href="{base}/explainers#appendix-e">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c5_app')}</a></p>
    <h3 id="act-1-picture">{t(lang.current, 'body.casings.act1_table_h')}</h3>
    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane2_bars.svg" alt={t(lang.current, 'body.impact.fig_alt')} class="chart-img" style="max-width: 100%;" width="441" height="532" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.impact.fig_caption')}</figcaption>
    </figure>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.impact.table_col_test')}</th>
            <th>{t(lang.current, 'body.impact.table_col_majority')}</th>
            <th>{t(lang.current, 'body.impact.table_col_minority')}</th>
            <th>{t(lang.current, 'body.impact.table_col_direction')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.impact.table_r1_a')}</td>
            <td class="normal">{t(lang.current, 'body.impact.table_r1_b')}</td>
            <td>{t(lang.current, 'body.impact.table_r1_c')}</td>
            <td>{t(lang.current, 'body.impact.table_r1_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.impact.table_r2_a')}</td>
            <td class="normal">{t(lang.current, 'body.impact.table_r2_b')}</td>
            <td class="flag">{t(lang.current, 'body.impact.table_r2_c')}</td>
            <td>{t(lang.current, 'body.impact.table_r2_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.impact.table_r3_a')}</td>
            <td class="normal">{t(lang.current, 'body.impact.table_r3_b')}</td>
            <td class="flag">{t(lang.current, 'body.impact.table_r3_c')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r3_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.impact.table_r4_a')}</td>
            <td class="normal">{t(lang.current, 'body.impact.table_r4_b')}</td>
            <td class="flag">{t(lang.current, 'body.impact.table_r4_c')}</td>
            <td>{t(lang.current, 'body.impact.table_r4_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.impact.table_r5_a')}</td>
            <td class="normal">{t(lang.current, 'body.impact.table_r5_b')}</td>
            <td class="flag">{t(lang.current, 'body.impact.table_r5_c')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r5_d')}</td>
          </tr>
          <tr>
            <td>{@html t(lang.current, 'body.impact.table_r6_a')}</td>
            <td class="normal">{@html t(lang.current, 'body.impact.table_r6_b')}</td>
            <td class="flag">{@html t(lang.current, 'body.impact.table_r6_c')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r6_d')}</td>
          </tr>
          <tr style="opacity: 0.85;">
            <td>{@html t(lang.current, 'body.impact.table_r7_a')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r7_b')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r7_c')}</td>
            <td>{@html t(lang.current, 'body.impact.table_r7_d')}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p>{t(lang.current, 'body.casings.act1_table_close')}</p>
    <p class="back-link"><a href="#the-picture">{t(lang.current, 'chrome.back_to_picture')}</a></p>
  </section>

  <section class="editorial-block" id="what-this-means" aria-labelledby="s5-heading">
    <h2 id="s5-heading">{t(lang.current, 'editorial_reflect.heading')}</h2>
    <p>{t(lang.current, 'editorial_reflect.intro_p1')}</p>
    <ol class="ladder-questions">
      <li><strong>{t(lang.current, 'editorial_reflect.intro_q1')}</strong></li>
      <li><strong>{t(lang.current, 'editorial_reflect.intro_q2')}</strong></li>
      <li><strong>{t(lang.current, 'editorial_reflect.intro_q3')}</strong></li>
    </ol>
    <p>{t(lang.current, 'editorial_reflect.intro_p2')}</p>

    <h3 class="rung">{t(lang.current, 'editorial_reflect.you_h')}</h3>
    <p>{t(lang.current, 'editorial_reflect.you_p')}</p>

    <h3 class="rung">{t(lang.current, 'editorial_reflect.community_h')}</h3>
    <p>{@html t(lang.current, 'editorial_reflect.community_p')}</p>

    <h3 class="rung">{t(lang.current, 'editorial_reflect.municipality_h')}</h3>
    <p>{@html t(lang.current, 'editorial_reflect.municipality_p')}</p>

    <h3 class="rung">{t(lang.current, 'editorial_reflect.region_h')}</h3>
    <p>{t(lang.current, 'editorial_reflect.region_p1')}</p>
    <p>{@html t(lang.current, 'editorial_reflect.region_p2')}</p>
    <p>{@html t(lang.current, 'editorial_reflect.region_p3')}</p>
    <p>{t(lang.current, 'editorial_reflect.region_p4')}</p>

    <h3 class="rung">{t(lang.current, 'editorial_reflect.province_h')}</h3>
    <p>{@html t(lang.current, 'editorial_reflect.province_p')}</p>
  </section>

  <section class="editorial-block" id="history-of-gerrymandering" aria-labelledby="s6-heading">
    <h2 id="s6-heading">{t(lang.current, 'editorial_history.heading')}</h2>
    <p>{@html t(lang.current, 'editorial_history.p1')}</p>
    <p>{t(lang.current, 'editorial_history.p2')}</p>
    <p>{@html t(lang.current, 'editorial_history.p3')}</p>
    <p>{@html t(lang.current, 'editorial_history.p4')}</p>
    <p>{@html t(lang.current, 'editorial_history.p5')}</p>
    <p>{t(lang.current, 'editorial_history.p6')}</p>
  </section>

  <section class="editorial-block" id="canada-is-different" aria-labelledby="s7-heading">
    <h2 id="s7-heading">{t(lang.current, 'editorial_canada.heading')}</h2>
    <p>{t(lang.current, 'editorial_canada.p1')}</p>
    <p>{t(lang.current, 'editorial_canada.p2')}</p>
    <p>{@html t(lang.current, 'editorial_canada.p3')}</p>
    <p>{@html t(lang.current, 'editorial_canada.p4')}</p>
    <p>{@html t(lang.current, 'editorial_canada.p5')}</p>
    <p>{@html t(lang.current, 'editorial_canada.p6')}</p>
    <p>{@html t(lang.current, 'editorial_canada.p7')}</p>

    <p class="back-link"><a href="#the-picture">{t(lang.current, 'chrome.back_to_picture')}</a></p>
  </section>

  <section id="act-2">
    <h2>{t(lang.current, 'body.casings.act2_h')} <a href="#act-2" class="section-link" aria-label={t(lang.current, 'nav.act2')}>#</a></h2>
    {@render preliminaryBanner()}
    <p>{t(lang.current, 'body.casings.act2_intro_p1')}</p>
    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.howmcmc_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.howmcmc_mcmc').replaceAll('__BASE__', base)}</p>
      <p>{@html t(lang.current, 'body.clean.howmcmc_recom')}</p>
    </div>
    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.prereg_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.prereg_body').replaceAll('__BASE__', base)}</p>
    </div>
    <p>{t(lang.current, 'body.casings.act2_intro_p2')}</p>
    <h3 id="casing-6">{t(lang.current, 'body.casings.c6_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c6_found')}</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.clean.t3_col_a')}</th>
            <th>{t(lang.current, 'body.clean.t3_col_b')}</th>
            <th>{t(lang.current, 'body.clean.t3_col_c')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.clean.t3_r1_a')}</td>
            <td class="normal">{t(lang.current, 'body.clean.t3_r1_b')}</td>
            <td class="normal">{t(lang.current, 'body.clean.t3_r1_c')}</td>
          </tr>
          <tr>
            <td>{@html t(lang.current, 'body.clean.t3_r2_a')}</td>
            <td class="normal">{@html t(lang.current, 'body.clean.t3_r2_b')}</td>
            <td class="normal">{@html t(lang.current, 'body.clean.t3_r2_c')}</td>
          </tr>
          <tr>
            <td>{@html t(lang.current, 'body.clean.t3_r3_a')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t3_r3_b')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t3_r3_c')}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p><strong>{t(lang.current, 'body.casings.beat_found')} (2).</strong> {@html t(lang.current, 'body.casings.c6_found2')}</p>
    <p>{t(lang.current, 'body.clean.super_lead')}</p>
    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.super_label')}</strong></p>
      <p>{t(lang.current, 'body.clean.super_body')}</p>
    </div>
    <p>{t(lang.current, 'body.clean.super_close')}</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.clean.t4_col_a')}</th>
            <th>{t(lang.current, 'body.clean.t4_col_b')}</th>
            <th>{t(lang.current, 'body.clean.t4_col_c')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.clean.t4_r1_a')}</td>
            <td>{t(lang.current, 'body.clean.t4_r1_b')}</td>
            <td>{t(lang.current, 'body.clean.t4_r1_c')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t4_r2_a')}</td>
            <td>{t(lang.current, 'body.clean.t4_r2_b')}</td>
            <td>{t(lang.current, 'body.clean.t4_r2_c')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t4_r3_a')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t4_r3_b')}</td>
            <td>{t(lang.current, 'body.clean.t4_r3_c')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t4_r4_a')}</td>
            <td>{@html t(lang.current, 'body.clean.t4_r4_b')}</td>
            <td>{t(lang.current, 'body.clean.t4_r4_c')}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c6_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c6_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c6_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c6_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-f">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c6_app')}</a></p>
    <h3 id="casing-7">{t(lang.current, 'body.casings.c7_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c7_found')}</p>
    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane1_dotplot.svg" alt={t(lang.current, 'body.litmus.fig_alt')} class="chart-img" style="max-width: 100%;" width="463" height="247" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{@html t(lang.current, 'body.litmus.fig_caption')}</figcaption>
    </figure>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c7_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c7_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c7_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c7_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.c7_refrain')}</strong> — <a href="{base}/explainers#appendix-g">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c7_app')}</a></p>
    <h3 id="casing-8">{t(lang.current, 'body.casings.c8_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c8_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c8_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c8_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c8_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c8_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-h">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c8_app')}</a></p>
    <h3 id="casing-9">{t(lang.current, 'body.casings.c9_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c9_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c9_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c9_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c9_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c9_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-i">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c9_app')}</a></p>
    <h3 id="casing-10">{t(lang.current, 'body.casings.c10_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c10_found')}</p>
    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.szat_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.szat_body')}</p>
    </div>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c10_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c10_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c10_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c10_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.c10_refrain')}</strong> — <a href="{base}/explainers#appendix-j">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c10_app')}</a></p>
    <p class="back-link"><a href="#the-picture">{t(lang.current, 'chrome.back_to_picture')}</a></p>
  </section>

  <section id="act-3">
    <h2>{t(lang.current, 'body.casings.act3_h')} <a href="#act-3" class="section-link" aria-label={t(lang.current, 'nav.act3')}>#</a></h2>
    <p>{t(lang.current, 'body.casings.act3_intro')}</p>
    <h3 id="casing-11">{t(lang.current, 'body.casings.c11_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c11_found')}</p>
    <p style="font-size: 0.88rem; color: var(--text-muted);">{t(lang.current, 'body.casings.c11_note')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c11_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c11_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c11_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c11_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-k">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c11_app')}</a></p>
    <h3 id="casing-12">{t(lang.current, 'body.casings.c12_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c12_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c12_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c12_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c12_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c12_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-l">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c12_app')}</a></p>
    <h3 id="casing-13">{t(lang.current, 'body.casings.c13_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c13_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c13_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c13_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c13_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c13_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-m">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c13_app')}</a></p>
    <h3 id="casing-14">{t(lang.current, 'body.casings.c14_title')}</h3>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {@html t(lang.current, 'body.casings.c14_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {@html t(lang.current, 'body.casings.c14_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {@html t(lang.current, 'body.casings.c14_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {@html t(lang.current, 'body.casings.c14_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {@html t(lang.current, 'body.casings.c14_gun')}</p>
    <p class="casing-refrain" style="font-style: italic; margin: 0.9rem 0 0.4rem;"><strong>{t(lang.current, 'body.casings.refrain')}</strong> — <a href="{base}/explainers#appendix-n">{t(lang.current, 'body.casings.know_more')}: {t(lang.current, 'body.casings.c14_app')}</a></p>
  </section>

  <section id="the-scorecard">
    <h2>{t(lang.current, 'body.casings.rev_h')} <a href="#the-scorecard" class="section-link" aria-label={t(lang.current, 'nav.revisited')}>#</a></h2>
    <p>{t(lang.current, 'body.casings.rev_p1')}</p>
    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/stakes_quadrant.svg" alt={t(lang.current, 'body.clean.stakes_fig_alt')} class="chart-img" style="max-width: 100%;" width="474" height="346" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.clean.stakes_fig_caption')}</figcaption>
    </figure>
    <p>{t(lang.current, 'body.casings.rev_p2')}</p>
    <p>{t(lang.current, 'body.clean.stakes_table_intro')}</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th></th>
            <th>{t(lang.current, 'body.clean.t5_col_b')}</th>
            <th>{t(lang.current, 'body.clean.t5_col_c')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{@html t(lang.current, 'body.clean.t5_r1_a')}</td>
            <td class="normal">{@html t(lang.current, 'body.clean.t5_r1_b')}</td>
            <td class="normal">{@html t(lang.current, 'body.clean.t5_r1_c')}</td>
          </tr>
          <tr>
            <td>{@html t(lang.current, 'body.clean.t5_r2_a')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t5_r2_b')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t5_r2_c')}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <details class="audit-detail">
      <summary>{t(lang.current, 'body.clean.details2_summary')}</summary>
      <p style="margin:0.7rem 0 0;">{@html t(lang.current, 'body.clean.details2_p')}</p>
    </details>
    <p>{t(lang.current, 'body.casings.rev_litany_intro')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_found')}.</strong> {t(lang.current, 'body.casings.rev_found')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_show')}.</strong> {t(lang.current, 'body.casings.rev_show')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_experts')}.</strong> {t(lang.current, 'body.casings.rev_experts')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_canada')}.</strong> {t(lang.current, 'body.casings.rev_canada')}</p>
    <p><strong>{t(lang.current, 'body.casings.beat_gun')}.</strong> {t(lang.current, 'body.casings.rev_gun')}</p>
    <p class="casing-refrain" style="font-style: italic;"><strong>{t(lang.current, 'body.casings.rev_refrain')}</strong></p>
    <h3>{t(lang.current, 'body.casings.playbook_h')}</h3>
    <p>{@html t(lang.current, 'body.casings.playbook_p1')}</p>
    <p>{@html t(lang.current, 'body.casings.playbook_p2')}</p>
    <p>{t(lang.current, 'body.casings.appendices_note')} <a href="{base}/explainers">{t(lang.current, 'body.casings.appendices_link')}</a></p>
  </section>

  <section id="section-7">
    <h2>{t(lang.current, 'body.november.heading')} <a href="#section-7" class="section-link" aria-label={t(lang.current, 'body.november.heading')}>#</a></h2>

    <div class="callout callout-neutral" style="border-inline-start-color:#888; font-size:0.95rem;">
      <p style="margin:0;"><strong>{t(lang.current, 'body.november.context_label')}</strong>{t(lang.current, 'body.november.context_body')}</p>
    </div>

    <p>{t(lang.current, 'body.november.intro')}</p>


    <p>{@html t(lang.current, 'body.commission_split.finding3')}</p>

    <h3>{t(lang.current, 'body.november.h_framework')}</h3>

    <p>{@html t(lang.current, 'body.november.framework_p1')}</p>

    <p>{t(lang.current, 'body.november.framework_p2')}</p>

    <p>{@html t(lang.current, 'body.november.framework_p3')}</p>


    <p>{t(lang.current, 'body.november.closing')}</p>

    <p>{@html t(lang.current, 'body.november.process_scorecard').replaceAll('__BASE__', base)}</p>
  </section>

  <section id="authors-view">
    <h2>{t(lang.current, 'body.authors_view.heading')} <a href="#authors-view" class="section-link" aria-label={t(lang.current, 'body.authors_view.heading_aria')}>#</a></h2>

    <div style="border-left: 3px solid var(--text-muted); padding: 0.2rem 0 0.2rem 1rem; margin: 0 0 1.3rem;">
      <p style="margin: 0; font-style: italic;">{t(lang.current, 'body.authors_view.preamble')}</p>
    </div>

    <p>{t(lang.current, 'body.authors_view.p1')}</p>
    <p>{t(lang.current, 'body.authors_view.p2')}</p>
    <p>{t(lang.current, 'body.authors_view.p3')}</p>
    <p>{t(lang.current, 'body.authors_view.p4')}</p>
    <p>{t(lang.current, 'body.authors_view.p5')}</p>
    <p>{t(lang.current, 'body.authors_view.p6')}</p>
    <p>{@html t(lang.current, 'body.authors_view.p7')}</p>
    <p>{t(lang.current, 'body.authors_view.p8')}</p>
    <p>{t(lang.current, 'body.authors_view.p9')}</p>
    <p>{t(lang.current, 'body.authors_view.p10')}</p>
    <p style="margin: 1rem 0 1.4rem;">{t(lang.current, 'body.authors_view.signed')}</p>
    <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">{@html t(lang.current, 'body.authors_view.sources')}</p>
  </section>

  <section id="section-8">
    <h2>{t(lang.current, 'body.suggestions.heading')} <a href="#section-8" class="section-link" aria-label={t(lang.current, 'body.suggestions.heading_aria')}>#</a></h2>

    <p style="font-style: italic; color: var(--text-muted);">{t(lang.current, 'body.suggestions.resume')}</p>

    <p>{t(lang.current, 'body.suggestions.intro')}</p>

    <p>{@html t(lang.current, 'body.suggestions.advance_p1')}</p>

    <p>{t(lang.current, 'body.suggestions.advance_p2')}</p>

    <p>{@html t(lang.current, 'body.suggestions.lesser_slave_p1')}</p>

    <p>{@html t(lang.current, 'body.suggestions.lesser_slave_p2')}</p>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.suggestions.ebca_label')}</strong></p>
      <p>{@html t(lang.current, 'body.suggestions.ebca_body')}</p>
    </div>

    <p>{@html t(lang.current, 'body.suggestions.rationale_p1')}</p>
    <p>{@html t(lang.current, 'body.suggestions.rationale_p2')}</p>

    <p>{@html t(lang.current, 'body.suggestions.banff_p')}</p>

    <p>{@html t(lang.current, 'body.suggestions.census_p1')}</p>

    <p>{@html t(lang.current, 'body.suggestions.census_p2')}</p>

    <p>{t(lang.current, 'body.suggestions.closing')}</p>
  </section>

  <section id="retractions">
    <h2>{t(lang.current, 'body.retractions.heading')} <a href="#retractions" class="section-link" aria-label={t(lang.current, 'body.retractions.heading_aria')}>#</a></h2>

    <div class="callout warning">
      <p><strong>{t(lang.current, 'body.retractions.conditions_label')}</strong></p>
      <p>{t(lang.current, 'body.retractions.conditions_intro')}</p>

      <div style="margin: 0.8rem 0 0; border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>{t(lang.current, 'body.retractions.c1_title')}</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: var(--text-muted);">{@html t(lang.current, 'body.retractions.c1_what')}</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">{@html t(lang.current, 'body.retractions.c1_cond')}</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>{t(lang.current, 'body.retractions.c2_title')}</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: var(--text-muted);">{@html t(lang.current, 'body.retractions.c2_what')}</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">{@html t(lang.current, 'body.retractions.c2_cond')}</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>{t(lang.current, 'body.retractions.c3_title')}</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: var(--text-muted);">{@html t(lang.current, 'body.retractions.c3_what')}</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">{@html t(lang.current, 'body.retractions.c3_cond')}</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>{t(lang.current, 'body.retractions.c4_title')}</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: var(--text-muted);">{@html t(lang.current, 'body.retractions.c4_what')}</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">{@html t(lang.current, 'body.retractions.c4_cond')}</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>{t(lang.current, 'body.retractions.c5_title')}</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: var(--text-muted);">{@html t(lang.current, 'body.retractions.c5_what')}</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">{@html t(lang.current, 'body.retractions.c5_cond')}</p>
      </div>
    </div>

    <div class="callout warning">
      <p><strong>{t(lang.current, 'body.retractions.corr_label')}</strong></p>
      <p>{t(lang.current, 'body.retractions.corr_intro')}</p>
      <p>{@html t(lang.current, 'body.retractions.corr_municipal')}</p>
    </div>
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

  {#if lang.current !== 'en' && lang.current !== 'fr'}
    <!-- Rendered only on machine-translated versions — sits under About me so the
         translation provenance reads as part of the audit's transparency
         apparatus, alongside the author's own disclosure. English is the source;
         French has had a native-speaker review, so neither shows this notice. -->
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

<!-- Figure lightbox -->
<div id="fig-lightbox" role="dialog" aria-modal="true" aria-label={t(lang.current, 'chrome.lightbox.fig_aria')} tabindex="-1">
  <button id="fig-lightbox-close" aria-label={t(lang.current, 'chrome.lightbox.fig_close_aria')}>&times;</button>
  <img id="fig-lightbox-img" alt="">
</div>

<footer>
  <div class="container">
    {t(lang.current, 'chrome.footer.title')}<br>
    {t(lang.current, 'chrome.footer.copyright')}
    {t(lang.current, 'chrome.footer.text_label')} <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a> &mdash;
    {t(lang.current, 'chrome.footer.code_label')} <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v3.0</a> &mdash;
    {t(lang.current, 'chrome.footer.translation_label')} {t(lang.current, 'chrome.footer.translation_credit')}<br>
    <span class="data-credit">{t(lang.current, 'chrome.footer.data_credit')}</span><br>
    <a href="https://ixby.github.io">ixby.github.io</a> &mdash;
    <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a><br>
    <a href="{base}/privacy-policy">{t(lang.current, 'chrome.participation.privacy_policy')}</a> &mdash;
    <a href="{base}/feedback">{t(lang.current, 'feedback.nav_link')}</a>
  </div>
</footer>

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

    header {
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

    header h1 {
      font-size: clamp(1.4rem, 4vw, 2.1rem);
      font-weight: 700;
      letter-spacing: -0.01em;
      line-height: 1.3;
      margin-bottom: 0.5rem;
    }

    header .subtitle {
      font-size: 1rem;
      opacity: 0.78;
    }

    header .badge {
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
      border: 1px solid rgba(212,175,55,0.4);
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
      header { padding: 0; }
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

    .skip-link {
      position: absolute;
      inset-inline-start: 0.5rem;
      top: 0.5rem;
      background: #0a1e36;
      color: #fff;
      padding: 0.55rem 0.95rem;
      border-radius: 4px;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 600;
      z-index: 200;
      transform: translateY(-150%);
      transition: transform 0.15s ease;
    }
    .skip-link:focus,
    .skip-link:focus-visible {
      transform: translateY(0);
      outline: 2px solid #fff;
      outline-offset: 2px;
    }

    nav {
      background: var(--nav-bg);
      position: sticky;
      top: 0;
      z-index: 100;
      transition: box-shadow 0.18s ease;
    }
    nav.scrolled {
      box-shadow: 0 2px 14px rgba(0, 0, 0, 0.28);
    }
    :root[data-theme="dark"] nav.scrolled { box-shadow: 0 2px 14px rgba(0, 0, 0, 0.55); }

    .nav-inner {
      display: flex;
      align-items: center;
      gap: 0.3rem;
      padding-block: 0;
      padding-inline-start: max(0.75rem, env(safe-area-inset-left));
      padding-inline-end: max(0.75rem, env(safe-area-inset-right));
      min-height: 2.75rem;
      max-width: 1400px;
      margin: 0 auto;
    }
    /* Windowed prev / current / next nav. A 3-column grid keeps the current
       section centred while the previous and next slots flank it and slide as
       the reader scrolls. */
    .nav-landmarks {
      flex: 1;
      min-width: 0;
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 0.3rem;
    }
    .nav-step { min-width: 0; }
    .nav-step-lbl {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .nav-prev  { justify-self: end;   color: rgba(255, 255, 255, 0.62); max-width: 16rem; }
    .nav-next  { justify-self: start; color: rgba(255, 255, 255, 0.62); max-width: 16rem; }
    .nav-prev .nav-step-lbl, .nav-next .nav-step-lbl { max-width: 13rem; }
    .nav-chev { opacity: 0.65; font-size: 1.15em; line-height: 1; padding: 0 0.1rem; }
    .nav-current {
      justify-self: center;
      display: inline-flex;
      align-items: center;
      min-height: 2.75rem;
      padding: 0 0.7rem;
      color: #fff;
      font-size: 0.9rem;
      font-weight: 600;
      letter-spacing: 0.005em;
      text-align: center;
      max-width: 24rem;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      position: relative;
    }
    .nav-current::after {
      content: '';
      position: absolute;
      left: 0.7rem;
      right: 0.7rem;
      bottom: 0;
      height: 2px;
      background: var(--nav-accent);
      border-radius: 1px;
    }
    .nav-edge { min-width: 0; }
    .nav-tools {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      padding-inline-start: 0.5rem;
      margin-inline-start: 0.25rem;
      border-inline-start: 1px solid rgba(255,255,255,0.12);
    }

    nav a {
      color: rgba(255, 255, 255, 0.72);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      font-size: 0.84rem;
      font-weight: 500;
      letter-spacing: 0.005em;
      min-height: 2.75rem;
      padding: 0 0.7rem;
      white-space: nowrap;
      position: relative;
      transition: color 0.15s ease, background 0.15s ease;
    }
    nav a:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.06);
      text-decoration: none;
    }
    nav a:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.55);
      outline-offset: -3px;
      border-radius: 3px;
    }
    nav a.nav-home {
      color: rgba(255,255,255,0.55);
      padding: 0 0.65rem 0 0.3rem;
      margin-inline-end: 0.2rem;
      border-inline-end: 1px solid rgba(255,255,255,0.12);
      text-decoration: none;
    }
    nav a.nav-home:hover {
      color: #fff;
      background: transparent;
    }
    nav a.nav-home:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.55);
      outline-offset: -3px;
      border-radius: 3px;
    }
    nav a.nav-home.active::after { display: none; }

    .nav-hamburger:focus-visible,
    .nav-theme-btn:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.55);
      outline-offset: -3px;
      border-radius: 3px;
    }

    .nav-hamburger {
      display: inline-flex;
      background: none; border: none; cursor: pointer;
      color: rgba(255,255,255,0.72); padding: 0 0.45rem;
      min-height: 2.75rem; align-items: center; justify-content: center;
      border-radius: 4px;
      transition: color 0.15s ease, background 0.15s ease;
    }
    .nav-hamburger:hover { color: #fff; background: rgba(255, 255, 255, 0.06); }
    .nav-hamburger[aria-expanded="true"] { color: #fff; background: rgba(255, 255, 255, 0.08); }

    #nav-drawer {
      display: flex;
      flex-direction: column;
      background: #15263d;
      border-top: 1px solid rgba(255,255,255,0.06);
      padding: 0.4rem 0 0.8rem;
      max-height: calc(100vh - 2.75rem);
      overflow-y: auto;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    }
    :root[data-theme="dark"] #nav-drawer { background: #131623; }

    #nav-drawer a {
      display: block;
      color: rgba(255,255,255,0.82);
      text-decoration: none;
      font-size: 0.92rem;
      padding: 0.55rem 1.4rem;
      transition: background 0.12s ease, color 0.12s ease;
    }
    #nav-drawer a:hover {
      background: rgba(255,255,255,0.07);
      color: #fff;
      text-decoration: none;
    }
    #nav-drawer a.drawer-top {
      color: rgba(255,255,255,0.55);
      font-size: 0.82rem;
      padding: 0.45rem 1.4rem 0.65rem;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      margin-bottom: 0.3rem;
    }
    #nav-drawer .drawer-group {
      margin: 0.7rem 0 0.2rem;
      padding: 0 1.4rem;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: rgba(255,255,255,0.42);
    }

    @media (max-width: 720px) {
      .nav-landmarks { display: none; }
      .nav-tools { border-inline-start: none; padding-inline-start: 0; margin-inline-start: auto; }
    }

    .nav-theme-btn {
      display: inline-flex; align-items: center; justify-content: center;
      background: none; border: none; cursor: pointer;
      color: #F5C518; padding: 0 0.45rem;
      min-height: 2.75rem;
      border-radius: 4px;
      transition: color 0.15s ease, background 0.15s ease;
    }
    .nav-theme-btn:hover { color: #fff; background: rgba(255, 255, 255, 0.06); }
    /* Sun shown (and yellow) in light mode; moon shown (and bright blue) in dark mode */
    .icon-sun { display: block; }
    .icon-moon { display: none; }
    :root[data-theme="dark"] .nav-theme-btn { color: #4FC3F7; }
    :root[data-theme="dark"] .icon-sun { display: none; }
    :root[data-theme="dark"] .icon-moon { display: block; }

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

    section { padding: 2.2rem 0 1.8rem; border-bottom: 1px solid var(--border); scroll-margin-top: 72px; }
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
    #stakes-heading, #boundary-heading { scroll-margin-top: 72px; }
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
    }
    :root[data-theme="dark"] .chart-img { filter: brightness(0.88) contrast(0.95); }

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

    footer {
      background: var(--nav-bg);
      color: rgba(255, 255, 255, 0.6);
      padding: 1.8rem 1.5rem 1.6rem;
      text-align: center;
      font-size: 0.82rem;
      line-height: 1.7;
      margin-top: 2rem;
      border-top: 2px solid var(--nav-accent);
      letter-spacing: 0.005em;
    }
    footer .container { padding-block: 0; }
    footer a {
      color: rgba(255, 255, 255, 0.78);
      text-decoration: none;
      border-bottom: 1px solid rgba(255, 255, 255, 0.18);
      transition: color 0.15s ease, border-color 0.15s ease;
    }
    footer a:hover {
      color: #fff;
      border-bottom-color: rgba(255, 255, 255, 0.55);
    }
    footer a:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.55);
      outline-offset: 2px;
      border-radius: 2px;
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

  /* Figure image lightbox */
  figure img { cursor: zoom-in; }
  #fig-lightbox {
    position: fixed; inset: 0; z-index: 8000;
    background: rgba(0,0,0,0.90);
    display: none; align-items: center; justify-content: center;
    cursor: default;
    touch-action: none;
    overflow: hidden;
  }
  #fig-lightbox:focus { outline: none; }
  #fig-lightbox-close {
    position: absolute; top: 12px; inset-inline-end: 16px;
    background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
    color: #fff; font-size: 1.4rem; line-height: 1;
    width: 36px; height: 36px; border-radius: 50%; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    z-index: 1;
  }
  #fig-lightbox-close:hover { background: rgba(255,255,255,0.22); }
  #fig-lightbox img {
    max-width: 92vw; max-height: 92dvh;
    object-fit: contain;
    border-radius: 4px;
    box-shadow: 0 0 60px rgba(0,0,0,0.6);
    transform-origin: center center;
    cursor: default;
    pointer-events: none;
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
