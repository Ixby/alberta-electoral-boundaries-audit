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

<svelte:window onkeydown={handleWindowKeydown} />

<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import { base } from '$app/paths';
  type MapEngineModule = Awaited<typeof import('$lib/mapEngine')>;
  let _ME: MapEngineModule | null = null;
  let _mePromise: Promise<void> | null = null;
  let _pendingState: Pick<MapState, 'primary' | 'mapOn' | 'layers'> | null = null;

  // Push the current language's engine strings into the framework-free
  // map engine. Called at engine init and again on every language switch.
  async function _syncEngineStrings(): Promise<void> {
    const { setEngineStrings } = await import('$lib/mapEngine/strings');
    setEngineStrings({
      votesSuffix:       t(lang.current, 'chrome.map.votes_suffix'),
      totalVotesSuffix:  t(lang.current, 'chrome.map.total_votes_suffix'),
      popPrefix:         t(lang.current, 'chrome.map.pop_prefix'),
      votingAreasSuffix: t(lang.current, 'chrome.map.voting_areas_suffix'),
      otherMaps:         t(lang.current, 'chrome.map.other_maps'),
      uniqueBoundary:    t(lang.current, 'chrome.map.unique_boundary'),
      inPersonVotes:     t(lang.current, 'chrome.map.in_person_votes'),
      loadErrorGeneric:  t(lang.current, 'chrome.map.load_error_generic'),
      loadErrorMap:      t(lang.current, 'chrome.map.load_error_map'),
      contextMinority:   t(lang.current, 'chrome.map.context_minority'),
      contextMajority:   t(lang.current, 'chrome.map.context_majority'),
      context2019:       t(lang.current, 'chrome.map.context_2019'),
      tagMin:            t(lang.current, 'chrome.map.tag_min'),
      tagMaj:            t(lang.current, 'chrome.map.tag_maj'),
      tag2019:           t(lang.current, 'chrome.map.tag_2019'),
    });
  }

  async function ensureMapLoaded(): Promise<void> {
    if (_ME) return;
    if (!_mePromise) {
      _mePromise = (async () => {
        await _syncEngineStrings();
        _ME = await import('$lib/mapEngine');
        _ME.init(base);
        const obj = document.getElementById('zoom-obj') as HTMLObjectElement;
        if (obj) obj.data = `${base}/images/cover_art_2019_hires.svg`;
        _ME.onEvent((event: FlightEvent) => { recordEvent(event); _scheduleCodeRefresh(); });
        if (_pendingState) {
          _ME.applyState(_pendingState.primary, _pendingState.mapOn, _pendingState.layers);
          _pendingState = null;
        }
      })();
    }
    return _mePromise;
  }

  async function handleZoomTrigger(e: Event): Promise<void> {
    e.preventDefault();
    await ensureMapLoaded();
    _ME?.openOverlay();
  }

  // Re-inject engine strings whenever the language changes after the
  // engine has loaded (callouts and error messages re-render with the
  // new language on next interaction; the context line updates on next
  // map switch).
  $effect(() => {
    void lang.current;
    if (_ME) void _syncEngineStrings();
  });

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
  import { isDNT, setParticipation, recordEvent, encodeState, decodeState, setOrigin, saveShare, flushTelemetry, setGpsRegion, setLanguage, type FlightEvent, type MapState } from '$lib/share';
  import { getStoredConsent, storeConsent, getStoredTheme, storeTheme, getLastCode, storeLastCode, getStoredGps, storeGps, getStoredLanguage, storeLanguage } from '$lib/prefs';
  import { lang } from '$lib/i18n/store.svelte';
  import { proseWordCount } from '$lib/i18n/wordCount';
  import { t } from '$lib/i18n/dict';
  import LanguageSelector from '$lib/components/LanguageSelector.svelte';
  import Gloss from '$lib/components/Gloss.svelte';
  import { focusTrap } from '$lib/a11y/focusTrap';

  // ── Share / participation state ───────────────────────────────────────────
  let navOpen           = $state(false);
  let navScrolled       = $state(false);
  let activeLandmark    = $state<string>('');
  let showParticipation = $state(false);
  let dntActive         = $state(false);
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
  let showSharePanel    = $state(false);
  let shareCode         = $state('');
  let loadInput         = $state('');
  let copyState         = $state<'idle' | 'copied' | 'failed'>('idle');
  let loadErrorKey      = $state<'' | 'unrecognised'>('');
  const copyLabel       = $derived(
    copyState === 'copied' ? t(lang.current, 'chrome.share.copied')
    : copyState === 'failed' ? t(lang.current, 'chrome.share.copy_failed')
    : t(lang.current, 'chrome.share.copy')
  );
  const loadError       = $derived(
    loadErrorKey === 'unrecognised' ? t(lang.current, 'chrome.share.unrecognised') : ''
  );

  function _generateCode() {
    const s = _ME ? _ME.getState() : null;
    shareCode = s ? (encodeState(s) ?? '—') : '—';
    if (shareCode !== '—' && s) { saveShare(shareCode, s); storeLastCode(shareCode); }
  }

  function toggleSharePanel() {
    showSharePanel = !showSharePanel;
    if (showSharePanel) {
      _generateCode(); loadErrorKey = '';
      tick().then(() => {
        const panel = document.getElementById('share-panel');
        const first = panel?.querySelector('button, input') as HTMLElement | null;
        first?.focus();
      });
    }
  }

  function closeSharePanel() { showSharePanel = false; }

  function handleWindowKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape' && showSharePanel) closeSharePanel();
  }

  async function copyCode() {
    if (!shareCode || shareCode === '—') return;
    try {
      await navigator.clipboard.writeText(shareCode);
      copyState = 'copied';
    } catch {
      copyState = 'failed';
    }
    setTimeout(() => { copyState = 'idle'; }, 2000);
  }

  function loadShare() {
    const trimmed = loadInput.trim();
    if (!trimmed) return;
    const decoded = decodeState(trimmed);
    if (!decoded) { loadErrorKey = 'unrecognised'; return; }
    if (_ME) { _ME.applyState(decoded.primary, decoded.mapOn, decoded.layers); }
    else { _pendingState = { primary: decoded.primary, mapOn: decoded.mapOn, layers: decoded.layers }; }
    setOrigin(trimmed.toLowerCase().trim());
    showSharePanel = false;
    loadInput  = '';
    loadErrorKey = '';
  }

  // Map Explorer development notice — dismissible per session. It returns
  // next session deliberately: the tool is genuinely changing day to day,
  // and a user who dismissed it last week deserves the reminder.
  let devNoticeDismissed = $state(false);
  if (typeof sessionStorage !== 'undefined') {
    devNoticeDismissed = sessionStorage.getItem('map_dev_notice_dismissed') === '1';
  }
  function dismissDevNotice() {
    devNoticeDismissed = true;
    try { sessionStorage.setItem('map_dev_notice_dismissed', '1'); } catch {}
  }
  const devNoticeParts = $derived.by(() => {
    const raw = t(lang.current, 'chrome.map.dev_notice');
    const label = t(lang.current, 'chrome.map.dev_notice_email_label');
    const idx = raw.indexOf('%s');
    if (idx < 0) return { pre: raw, label, post: '' };
    return { pre: raw.slice(0, idx), label, post: raw.slice(idx + 2) };
  });

  // Loading-skeleton phrases, translated. $derived so a language switch
  // mid-load updates the cycling phrase live.
  const _skelPhrases = $derived([
    t(lang.current, 'chrome.map.skel_1'), t(lang.current, 'chrome.map.skel_2'),
    t(lang.current, 'chrome.map.skel_3'), t(lang.current, 'chrome.map.skel_4'),
    t(lang.current, 'chrome.map.skel_5'), t(lang.current, 'chrome.map.skel_6'),
  ]);
  let skelPhrase = $state('');
  let _skelIdx = 0;

  let _codeRefreshTimer: ReturnType<typeof setTimeout> | null = null;

  function _scheduleCodeRefresh() {
    if (_codeRefreshTimer) clearTimeout(_codeRefreshTimer);
    _codeRefreshTimer = setTimeout(() => {
      _codeRefreshTimer = null;
      const s = _ME ? _ME.getState() : null;
      const code = s ? (encodeState(s) ?? null) : null;
      if (!code || !s) return;
      storeLastCode(code);
      if (showSharePanel) { shareCode = code; saveShare(code, s); }
    }, 200);
  }

  let _telemetryInterval: ReturnType<typeof setInterval>;
  onDestroy(() => {
    clearInterval(_telemetryInterval);
    if (typeof window !== 'undefined') window.removeEventListener('beforeunload', flushTelemetry);
  });

  onMount(async () => {

    window.addEventListener('beforeunload', flushTelemetry);
    _telemetryInterval = setInterval(flushTelemetry, 30_000);

    dntActive = isDNT();
    const storedConsent = await getStoredConsent();
    if (storedConsent !== null) {
      setParticipation(storedConsent === 'yes');
    } else {
      setTimeout(() => { showParticipation = true; }, 900);
    }

    // ── Session resume ────────────────────────────────────────────────────────
    const lastCode = await getLastCode();
    if (lastCode) {
      const lastState = decodeState(lastCode);
      if (lastState) { _pendingState = { primary: lastState.primary, mapOn: lastState.mapOn, layers: lastState.layers }; setOrigin(lastCode); }
    }

    // ── GPS + language (returning consented users) ────────────────────────────
    if (storedConsent === 'yes') {
      const storedLang = await getStoredLanguage();
      if (storedLang) { setLanguage(storedLang); }
      else { await storeLanguage(navigator.language); setLanguage(navigator.language); }

      const storedGps = await getStoredGps();
      if (storedGps) {
        setGpsRegion(storedGps.lat, storedGps.lng);
      } else if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            const lat = Math.round(pos.coords.latitude  * 10) / 10;
            const lng = Math.round(pos.coords.longitude * 10) / 10;
            await storeGps(lat, lng);
            setGpsRegion(lat, lng);
          },
          () => {},
        );
      }
    }

    // ── Skeleton phrase cycling ───────────────────────────────────────────────
    setInterval(() => {
      _skelIdx = (_skelIdx + 1) % _skelPhrases.length;
      skelPhrase = _skelPhrases[_skelIdx];
    }, 2800);

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

    // Map each landmark to the set of section anchors it represents (in order).
    // The currently-visible section's landmark wins.
    const landmarkOf: Record<string, string> = {
      'stakes-heading': 'stakes',
      'boundary-heading': 'stakes',
      'what-is-redistricting': 'stakes',
      'section-1': 'findings',
      'section-2': 'findings',
      'section-3': 'findings',
      'section-4': 'findings',
      'what-this-means': 'findings',
      'section-5': 'findings',
      'section-6': 'findings',
      'history-of-gerrymandering': 'history',
      'canada-is-different': 'history',
      'section-7': 'history',
      'section-8': 'reform',
      'retractions': 'notes',
      'references': 'notes',
      'resources': 'notes'
    };
    const observed = Object.keys(landmarkOf)
      .map(id => document.getElementById(id))
      .filter((el): el is HTMLElement => el !== null);
    if (observed.length) {
      // Observed anchors are headings (point elements). To avoid the active
      // pill clearing whenever no heading is inside a trigger band, pick the
      // last anchor whose top has scrolled above a line just under the nav.
      // The pill stays on that landmark until a later anchor crosses the line,
      // so deep scrolling inside a section keeps its parent highlighted.
      const orderedIds = Object.keys(landmarkOf);
      const updateActive = () => {
        const triggerY = 80;
        let lastPassed: string | null = null;
        for (const id of orderedIds) {
          const el = document.getElementById(id);
          if (!el) continue;
          if (el.getBoundingClientRect().top <= triggerY) lastPassed = id;
          else break;
        }
        activeLandmark = lastPassed ? landmarkOf[lastPassed] : '';
      };
      window.addEventListener('scroll', updateActive, { passive: true });
      window.addEventListener('resize', updateActive);
      updateActive();
    }

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

<a class="skip-link" href="#main">{t(lang.current, 'nav.skip_to_content')}</a>

<nav aria-label="Page sections" class:scrolled={navScrolled}>
  <div class="nav-inner">
    <a href="#top" class="nav-home" aria-label={t(lang.current, 'nav.home_aria')}><svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 2L2 9h2v9h5v-5h2v5h5V9h2L10 2z"/></svg></a>
    <div class="nav-landmarks">
      <a href="#stakes-heading" class:active={activeLandmark === 'stakes'} aria-current={activeLandmark === 'stakes' ? 'location' : undefined}>{t(lang.current, 'nav.stakes')}</a>
      <a href="#section-1" class:active={activeLandmark === 'findings'} aria-current={activeLandmark === 'findings' ? 'location' : undefined}>{t(lang.current, 'nav.findings')}</a>
      <a href="#history-of-gerrymandering" class:active={activeLandmark === 'history'} aria-current={activeLandmark === 'history' ? 'location' : undefined}>{t(lang.current, 'nav.history')}</a>
      <a href="#section-8" class:active={activeLandmark === 'reform'} aria-current={activeLandmark === 'reform' ? 'location' : undefined}>{t(lang.current, 'nav.reform')}</a>
      <a href="#references" class:active={activeLandmark === 'notes'} aria-current={activeLandmark === 'notes' ? 'location' : undefined}>{t(lang.current, 'nav.notes')}</a>
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
    <a href="#stakes-heading" onclick={closeNavDrawer}>{t(lang.current, 'nav.stakes')}</a>
    <a href="#what-is-redistricting" onclick={closeNavDrawer}>{t(lang.current, 'nav.why')}</a>
    <a href="#section-1" onclick={closeNavDrawer}>{t(lang.current, 'nav.map')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_audit')}</h4>
    <a href="#section-2" onclick={closeNavDrawer}>{t(lang.current, 'nav.split')}</a>
    <a href="#section-3" onclick={closeNavDrawer}>{t(lang.current, 'nav.litmus')}</a>
    <a href="#section-4" onclick={closeNavDrawer}>{t(lang.current, 'nav.crack_pack')}</a>
    <a href="#what-this-means" onclick={closeNavDrawer}>{t(lang.current, 'nav.for_you')}</a>
    <a href="#section-5" onclick={closeNavDrawer}>{t(lang.current, 'nav.impact')}</a>
    <a href="#section-6" onclick={closeNavDrawer}>{t(lang.current, 'nav.gerrymanders')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_context')}</h4>
    <a href="#history-of-gerrymandering" onclick={closeNavDrawer}>{t(lang.current, 'nav.history_full')}</a>
    <a href="#canada-is-different" onclick={closeNavDrawer}>{t(lang.current, 'nav.canada')}</a>
    <a href="#section-7" onclick={closeNavDrawer}>{t(lang.current, 'nav.lunty')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_forward')}</h4>
    <a href="#section-8" onclick={closeNavDrawer}>{t(lang.current, 'nav.suggestions')}</a>

    <h4 class="drawer-group">{t(lang.current, 'nav.group_apparatus')}</h4>
    <a href="#retractions" onclick={closeNavDrawer}>{t(lang.current, 'nav.retractions')}</a>
    <a href="#references" onclick={closeNavDrawer}>{t(lang.current, 'nav.references')}</a>
    <a href="#resources" onclick={closeNavDrawer}>{t(lang.current, 'nav.technical')}</a>
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
    <button id="zoom-trigger" class="hero-map-btn" title={t(lang.current, 'hero.btn_title')} aria-label={t(lang.current, 'hero.btn_aria')} onclick={handleZoomTrigger}>
      <div class="hero-map-wrap">
        <picture>
          <source type="image/webp" srcset="images/cover_art.webp 680w" sizes="(min-width: 600px) 339px, 90vw">
          <img src="images/cover_art.png" alt={t(lang.current, 'hero.image_alt')} class="header-image" fetchpriority="high" loading="eager" width="680" height="1205">
        </picture>
        <img src="images/province_outline.svg" class="province-border-overlay" aria-hidden="true" alt="" fetchpriority="high" loading="eager">
        <div class="hero-map-hint">{t(lang.current, 'hero.map_hint')}</div>
      </div>
    </button>
  </div>
</header>

<section class="opener-block container" aria-labelledby="opener-heading">
  <h2 id="opener-heading">{t(lang.current, 'verdict.headline')}</h2>
  <p>{t(lang.current, 'verdict.p_what')}</p>
  <p>{t(lang.current, 'verdict.p_split')}</p>
  <p>{t(lang.current, 'verdict.p_question')}</p>
  <p class="verdict-answer">{t(lang.current, 'verdict.p_answer')}</p>
  <p>{t(lang.current, 'verdict.p_howfar')}</p>
  <p class="verdict-aside">{t(lang.current, 'verdict.aside_pre')}<Gloss key="gerrymander">gerrymandered</Gloss>{t(lang.current, 'verdict.aside_post')}<a href="/law">{t(lang.current, 'verdict.law_link')}</a> and <a href="/methods">{t(lang.current, 'verdict.methods_link')}</a>.</p>
</section>

<section class="stakes-block container" aria-labelledby="stakes-heading">
  <h2 id="stakes-heading" class="visually-hidden">{t(lang.current, 'nav.stakes')}</h2>
  <div class="stakes-q">
    <h3>{t(lang.current, 'stakes.q1.heading')}</h3>
    <p>{@html t(lang.current, 'stakes.q1.body')}</p>
    <p class="stakes-footnote">{t(lang.current, 'stakes.q1.footnote')}</p>
  </div>
  <div class="stakes-q">
    <h3>{t(lang.current, 'stakes.q2.heading')}</h3>
    <p>{@html t(lang.current, 'stakes.q2.body')}</p>
  </div>
  <div class="stakes-q">
    <h3>{t(lang.current, 'stakes.q3.heading')}</h3>
    <p>{@html t(lang.current, 'stakes.q3.body')}</p>
  </div>
  <div class="stakes-scorecard" aria-labelledby="stakes-scorecard-h">
    <h3 id="stakes-scorecard-h">{t(lang.current, 'stakes.scorecard_h')}</h3>
    <p class="stakes-scorecard-intro">{t(lang.current, 'stakes.scorecard_intro')}</p>
    <figure class="stakes-scorecard-fig">
      <img src="{base}/images/stakes_quadrant.svg" alt={t(lang.current, 'stakes.scorecard_fig_alt')} width="474" height="351" loading="lazy">
      <figcaption>{t(lang.current, 'stakes.scorecard_fig_caption')}</figcaption>
    </figure>
    <p class="stakes-scorecard-close">{t(lang.current, 'stakes.scorecard_close')}</p>
  </div>
  <div class="stakes-ctas">
    <a href="#canada-is-different" class="stakes-cta">{t(lang.current, 'stakes.cta_law')}</a>
    <a href="#section-3" class="stakes-cta">{t(lang.current, 'stakes.cta_methods')}</a>
  </div>
</section>

<section class="boundary-block container" aria-labelledby="boundary-heading">
  <h2 id="boundary-heading">{t(lang.current, 'verdict.box_heading')}</h2>
  <ul class="boundary-list">
    <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{t(lang.current, 'verdict.box_can_1')}</span></li>
    <li class="row can"><span class="mark" aria-hidden="true">✓</span><span class="text">{t(lang.current, 'verdict.box_can_2')}</span></li>
    <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_1')}</span></li>
    <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_2')}</span></li>
    <li class="row cant"><span class="mark" aria-hidden="true">✗</span><span class="text">{t(lang.current, 'verdict.box_cant_3')}</span></li>
  </ul>
</section>

<section class="editorial-block container" id="what-is-redistricting" aria-labelledby="s1-heading">
  <h2 id="s1-heading">{t(lang.current, 'why_redrawn.heading')}</h2>
  <p>{t(lang.current, 'why_redrawn.p1')}</p>
  <p>{t(lang.current, 'why_redrawn.p2')}</p>
  <p>{t(lang.current, 'why_redrawn.p3')}</p>
  <p class="section-punch">{t(lang.current, 'why_redrawn.p4')}</p>
</section>

<main id="main" class="container" tabindex="-1">

  <div style="padding: 1.5rem 0 0.5rem;">
    <div class="callout callout-minority" style="border-inline-start-color:#6B35A7; font-size:1.05rem; padding:0.9rem 1rem; margin-bottom:0.8rem;">
      <p style="margin:0;"><strong>{t(lang.current, 'top_callouts.gerrymander_lead')}</strong> {@html t(lang.current, 'top_callouts.gerrymander_body')}</p>
    </div>
    <div class="callout callout-tldr" style="border-inline-start-color: #1A7A6E; font-size: 1.02rem; line-height: 1.65;">
      <p style="margin:0 0 0.6rem;"><strong>{t(lang.current, 'top_callouts.tldr_label')}</strong></p>
      <p style="margin:0 0 0.6rem;">{@html t(lang.current, 'top_callouts.tldr_p1')}</p>
      <p style="margin:0 0 0.6rem;">{@html t(lang.current, 'top_callouts.tldr_p2')}</p>
      <p style="margin:0;">{t(lang.current, 'top_callouts.tldr_p3')}</p>
      <p style="margin:0.6rem 0 0; font-size:0.88rem; color:var(--text-muted);">{@html t(lang.current, 'top_callouts.tldr_footer').replace('%s', '<a href=\"#retractions\">' + t(lang.current, 'top_callouts.tldr_footer_link') + '</a>')}</p>
    </div>
  </div>

  <section id="section-1">
    <h2>{t(lang.current, 'two_maps.heading')} <a href="#section-1" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 1">#</a></h2>
    <p>{t(lang.current, 'two_maps.p1')}</p>
    <p>{t(lang.current, 'two_maps.p2')}</p>
    <p>{t(lang.current, 'two_maps.p3')}</p>
  </section>

  <section id="section-2">
    <h2>{t(lang.current, 'body.commission_split.heading')} <a href="#section-2" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 2">#</a></h2>
    <p>{@html t(lang.current, 'body.commission_split.intro')}</p>
    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.commission_split.finding1')}</li>
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.commission_split.finding2')}</li>
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.commission_split.finding3')}</li>
    </ol>
    <p>{@html t(lang.current, 'body.commission_split.closing')}</p>
  </section>

  <div class="callout callout-info" style="border-inline-start-color:#2B5BA1; margin:0.5rem 0 1rem;">
    <p style="margin:0 0 0.4rem;"><strong>{t(lang.current, 'body.structural_results.heading')}</strong></p>
    <p style="margin:0;">{@html t(lang.current, 'body.structural_results.body')}</p>
  </div>

  <section id="section-3">
    <h2>{t(lang.current, 'body.litmus.heading')} <a href="#section-3" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 3">#</a></h2>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane1_dotplot.svg" alt={t(lang.current, 'body.litmus.fig_alt')} class="chart-img" style="max-width: 100%;" width="463" height="247" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{@html t(lang.current, 'body.litmus.fig_caption')}</figcaption>
    </figure>

    <p>{t(lang.current, 'body.litmus.table_intro')}</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.litmus.table_col_measured')}</th>
            <th>{t(lang.current, 'body.litmus.table_col_majority')}</th>
            <th>{t(lang.current, 'body.litmus.table_col_minority')}</th>
            <th>{t(lang.current, 'body.litmus.table_col_direction')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r1_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r1_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r1_c')}</td>
            <td>{t(lang.current, 'body.litmus.table_r1_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r2_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r2_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r2_c')}</td>
            <td>{@html t(lang.current, 'body.litmus.table_r2_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r3_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r3_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r3_c')}</td>
            <td>{@html t(lang.current, 'body.litmus.table_r3_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r4_a')}</td>
            <td>{t(lang.current, 'body.litmus.table_r4_b')}</td>
            <td>{t(lang.current, 'body.litmus.table_r4_c')}</td>
            <td>{t(lang.current, 'body.litmus.table_r4_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r5_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r5_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r5_c')}</td>
            <td>{t(lang.current, 'body.litmus.table_r5_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r6_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r6_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r6_c')}</td>
            <td>{@html t(lang.current, 'body.litmus.table_r6_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r7_a')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r7_b')}</td>
            <td class="flag">{t(lang.current, 'body.litmus.table_r7_c')}</td>
            <td>{@html t(lang.current, 'body.litmus.table_r7_d')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.litmus.table_r8_a')}</td>
            <td>{t(lang.current, 'body.litmus.table_r8_b')}</td>
            <td class="normal">{t(lang.current, 'body.litmus.table_r8_c')}</td>
            <td>{t(lang.current, 'body.litmus.table_r8_d')}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.litmus.vocab_label')}</strong></p>
      <p>{@html t(lang.current, 'body.litmus.vocab_eg')}</p>
      <p>{@html t(lang.current, 'body.litmus.vocab_mm')}</p>
      <p>{@html t(lang.current, 'body.litmus.vocab_percentile')}</p>
      <p>{@html t(lang.current, 'body.litmus.vocab_anchoring')}</p>
    </div>

    <p>{@html t(lang.current, 'body.litmus.closing_p1')}</p>

    <p>{t(lang.current, 'body.litmus.closing_p2')}</p>

    <p class="back-link"><a href="#stakes-heading">{t(lang.current, 'chrome.back_to_stakes')}</a></p>
  </section>

  <section id="section-4">
    <h2>{t(lang.current, 'body.cpd.heading')} <a href="#section-4" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 4">#</a></h2>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.cpd.vocab_label')}</strong></p>
      <p>{@html t(lang.current, 'body.cpd.vocab_packing')}</p>
      <p>{@html t(lang.current, 'body.cpd.vocab_cracking')}</p>
      <p>{@html t(lang.current, 'body.cpd.vocab_draining')}</p>
      <p>{@html t(lang.current, 'body.cpd.vocab_disclaimer')}</p>
    </div>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/figure_airdrie_v3.svg" alt={t(lang.current, 'body.cpd.fig_alt')} class="chart-img" style="max-width: 100%;" width="504" height="336" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.cpd.fig_caption')}</figcaption>
    </figure>

    <p>{t(lang.current, 'body.cpd.intro')}</p>

    <p>{@html t(lang.current, 'body.cpd.airdrie_p')}</p>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.cpd.airdrie_callout_label')}</strong></p>
      <p>{t(lang.current, 'body.cpd.airdrie_callout_p1')}</p>
      <p>{t(lang.current, 'body.cpd.airdrie_callout_p2')}</p>
      <p>{t(lang.current, 'body.cpd.airdrie_callout_p3')}</p>
    </div>

    <div class="callout">
      {t(lang.current, 'body.cpd.airdrie_callout_summary')}
    </div>

    <p style="text-align:center; margin: 0.2rem 0 1.1rem;">
      <button class="anomaly-trigger" data-anomaly="airdrie">{t(lang.current, 'body.cpd.airdrie_btn')}</button>
    </p>

    <p>{@html t(lang.current, 'body.cpd.anchoring_p')}</p>

    <p>{t(lang.current, 'body.cpd.anchoring_followup')}</p>

    <p>{@html t(lang.current, 'body.cpd.packing_p')}</p>

    <p>{@html t(lang.current, 'body.cpd.chair_p')}</p>
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

    <p class="back-link"><a href="#stakes-heading">{t(lang.current, 'chrome.back_to_stakes')}</a></p>
  </section>

  <section id="section-5">
    <h2>{t(lang.current, 'body.impact.heading')} <a href="#section-5" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 5">#</a></h2>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.impact.lanes_label')}</strong></p>
      <p>{@html t(lang.current, 'body.impact.lanes_body')}</p>
    </div>

    <p>{t(lang.current, 'body.impact.intro')}</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane2_bars.svg" alt={t(lang.current, 'body.impact.fig_alt')} class="chart-img" style="max-width: 100%;" width="441" height="545" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.impact.fig_caption')}</figcaption>
    </figure>

    <p>{@html t(lang.current, 'body.impact.table_intro')}</p>

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
        </tbody>
      </table>
    </div>

    <p>{@html t(lang.current, 'body.impact.rationales_p')}</p>

    <p>{@html t(lang.current, 'body.impact.chair_appendix_p')}</p>

    <p>{@html t(lang.current, 'body.impact.summary_p')}</p>
  </section>

  <section id="section-6">
    <h2>{t(lang.current, 'body.clean.heading')} <a href="#section-6" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 6">#</a></h2>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.legal_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.legal_body')}</p>
    </div>

    <p>{t(lang.current, 'body.clean.intro_p1')}</p>

    <p>{t(lang.current, 'body.clean.intro_p2')}</p>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.howmcmc_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.howmcmc_mcmc')}</p>
      <p>{@html t(lang.current, 'body.clean.howmcmc_recom')}</p>
    </div>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.prereg_label')}</strong></p>
      <p>{t(lang.current, 'body.clean.prereg_body')}</p>
    </div>

    <p>{@html t(lang.current, 'body.clean.neutral_p')}</p>

    <p>{t(lang.current, 'body.clean.full_dist')}</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.clean.t1_col_a')}</th>
            <th>{t(lang.current, 'body.clean.t1_col_b')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.clean.t1_r1_a')}</td>
            <td class="normal">{t(lang.current, 'body.clean.t1_r1_b')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t1_r2_a')}</td>
            <td>{t(lang.current, 'body.clean.t1_r2_b')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t1_r3_a')}</td>
            <td>{t(lang.current, 'body.clean.t1_r3_b')}</td>
          </tr>
          <tr>
            <td>{@html t(lang.current, 'body.clean.t1_r4_a')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t1_r4_b')}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>{@html t(lang.current, 'body.clean.seat_count_note')}</p>

    <p>{t(lang.current, 'body.clean.pattern_intro')}</p>

    <h3>{t(lang.current, 'body.clean.sub1_h')}</h3>

    <p>{t(lang.current, 'body.clean.sub1_p')}</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{t(lang.current, 'body.clean.t2_col_a')}</th>
            <th>{t(lang.current, 'body.clean.t2_col_b')}</th>
            <th>{t(lang.current, 'body.clean.t2_col_c')}</th>
            <th>{@html t(lang.current, 'body.clean.t2_col_d')}</th>
            <th>{t(lang.current, 'body.clean.t2_col_e')}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{t(lang.current, 'body.clean.t2_r1_a')}</td>
            <td class="normal">{t(lang.current, 'body.clean.t2_r1_b')}</td>
            <td>{t(lang.current, 'body.clean.t2_r1_c')}</td>
            <td>{t(lang.current, 'body.clean.t2_r1_d')}</td>
            <td class="normal">{t(lang.current, 'body.clean.t2_r1_e')}</td>
          </tr>
          <tr>
            <td>{t(lang.current, 'body.clean.t2_r2_a')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t2_r2_b')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t2_r2_c')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t2_r2_d')}</td>
            <td class="flag">{@html t(lang.current, 'body.clean.t2_r2_e')}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>{t(lang.current, 'body.clean.sub1_close')}</p>

    <h3>{t(lang.current, 'body.clean.sub2_h')}</h3>

    <p>{t(lang.current, 'body.clean.sub2_p')}</p>

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

    <p>{t(lang.current, 'body.clean.sub2_close')}</p>

    <h3>{t(lang.current, 'body.clean.sub3_h')}</h3>

    <p>{@html t(lang.current, 'body.clean.sub3_p')}</p>

    <details class="audit-detail">
      <summary>{t(lang.current, 'body.clean.details_summary')}</summary>
      <div class="audit-detail-body">
        <p>{@html t(lang.current, 'body.clean.details_p1')}</p>
        <p>{t(lang.current, 'body.clean.details_p2')}</p>
        <p>{@html t(lang.current, 'body.clean.details_p3')}</p>
      </div>
    </details>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.szat_label')}</strong></p>
      <p>{@html t(lang.current, 'body.clean.szat_body')}</p>
    </div>

    <p>{@html t(lang.current, 'body.clean.two_q')}</p>

    <p>{t(lang.current, 'body.clean.super_lead')}</p>

    <div class="callout">
      <p><strong>{t(lang.current, 'body.clean.super_label')}</strong></p>
      <p>{t(lang.current, 'body.clean.super_body')}</p>
    </div>

    <p>{t(lang.current, 'body.clean.super_close')}</p>

    <h3>{t(lang.current, 'body.clean.sub4_h')}</h3>

    <p>{@html t(lang.current, 'body.clean.sub4_p')}</p>

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

    <p>{t(lang.current, 'body.clean.sub4_close')}</p>

    <p>{@html t(lang.current, 'body.clean.sub4_quote')}</p>

    <h3>{t(lang.current, 'body.clean.sub5_h')}</h3>

    <p>{t(lang.current, 'body.clean.sub5_p')}</p>

    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.clean.defense1')}</li>
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.clean.defense2')}</li>
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.clean.defense3')}</li>
      <li style="margin-bottom: 0.6rem;">{@html t(lang.current, 'body.clean.defense4')}</li>
    </ol>

    <p>{t(lang.current, 'body.clean.sub5_close')}</p>

    <h3>{t(lang.current, 'body.clean.sub6_h')}</h3>

    <p>{@html t(lang.current, 'body.clean.sub6_p1')}</p>

    <p>{@html t(lang.current, 'body.clean.sub6_p2')}</p>

    <p>{@html t(lang.current, 'body.clean.sub6_asymm')}</p>

    <p>{t(lang.current, 'body.clean.sub6_close')}</p>

    <p>{@html t(lang.current, 'body.clean.sub6_caveat')}</p>

    <h3>{t(lang.current, 'body.clean.sub7_h')}</h3>

    <p>{@html t(lang.current, 'body.clean.sub7_p1')}</p>

    <p>{t(lang.current, 'body.clean.sub7_p2')}</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/stakes_quadrant.svg" alt={t(lang.current, 'body.clean.stakes_fig_alt')} class="chart-img" style="max-width: 100%;" width="474" height="351" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.4rem;">{t(lang.current, 'body.clean.stakes_fig_caption')}</figcaption>
    </figure>

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
  </section>

  <section id="section-7">
    <h2>{t(lang.current, 'body.november.heading')} <a href="#section-7" class="section-link" aria-label="{t(lang.current, 'body.section_link_aria')} 7">#</a></h2>

    <div class="callout callout-neutral" style="border-inline-start-color:#888; font-size:0.95rem;">
      <p style="margin:0;"><strong>{t(lang.current, 'body.november.context_label')}</strong>{t(lang.current, 'body.november.context_body')}</p>
    </div>

    <p>{t(lang.current, 'body.november.intro')}</p>

    <h3>{t(lang.current, 'body.november.h_anomalous')}</h3>

    <p>{@html t(lang.current, 'body.november.anomalous_p1')}</p>

    <p>{t(lang.current, 'body.november.anomalous_p2')}</p>

    <h3>{t(lang.current, 'body.november.h_framework')}</h3>

    <p>{@html t(lang.current, 'body.november.framework_p1')}</p>

    <p>{t(lang.current, 'body.november.framework_p2')}</p>

    <p>{@html t(lang.current, 'body.november.framework_p3')}</p>

    <h3>{t(lang.current, 'body.november.h_quebec')}</h3>

    <p>{@html t(lang.current, 'body.november.quebec_p1')}</p>

    <p>{t(lang.current, 'body.november.quebec_p2')}</p>

    <p>{t(lang.current, 'body.november.closing')}</p>
  </section>

  <section id="section-8">
    <h2>{t(lang.current, 'body.suggestions.heading')} <a href="#section-8" class="section-link" aria-label={t(lang.current, 'body.suggestions.heading_aria')}>#</a></h2>

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
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.pdf">{t(lang.current, 'body.resources.plain_label')}</a> &mdash; {t(lang.current, 'body.resources.plain_desc')}
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
      {@html t(lang.current, 'body.about_me.p4')}
    </p>
  </section>

  {#if lang.current !== 'en'}
    <!-- Rendered only on translated versions — sits under About me so the
         translation provenance reads as part of the audit's transparency
         apparatus, alongside the author's own disclosure. -->
    <section id="about-translation">
      <h2>{t(lang.current, 'body.translation_about.heading')}</h2>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {t(lang.current, 'body.translation_about.p1')}
      </p>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {t(lang.current, 'body.translation_about.p2')}
      </p>
      <p style="font-size:0.9rem; color:var(--text-muted);">
        {translationHelpParts.pre}<a href="mailto:wconn161@mtroyal.ca">{translationHelpParts.label}</a>{translationHelpParts.post}
      </p>
    </section>
  {/if}

</main><!-- /.container -->

<a href="#top" id="back-top" aria-label={t(lang.current, 'chrome.back_to_top')}>↑</a>

<div id="site-copyright" aria-label={t(lang.current, 'chrome.license_aria')}>
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="license noopener" title={t(lang.current, 'chrome.license_title')}>
    <img src="https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png" alt={t(lang.current, 'chrome.license_alt')} width="80" height="15">
  </a>
</div>

<!-- Figure lightbox -->
<div id="fig-lightbox" role="dialog" aria-modal="true" aria-label={t(lang.current, 'chrome.lightbox.fig_aria')} tabindex="-1">
  <button id="fig-lightbox-close" aria-label={t(lang.current, 'chrome.lightbox.fig_close_aria')}>&times;</button>
  <img id="fig-lightbox-img" alt="">
</div>

<!-- Participation prompt -->
{#if showParticipation}
<div id="participation-overlay" role="dialog" aria-modal="true" aria-labelledby="part-heading">
  <div id="participation-card" use:focusTrap={{ onEscape: () => showParticipation = false }}>
    <h2 id="part-heading">{t(lang.current, 'chrome.participation.heading')}</h2>
    <p>{t(lang.current, 'chrome.participation.body')}</p>
    <p class="part-no-collect">{t(lang.current, 'chrome.participation.no_collect')}</p>
    {#if dntActive}
    <p class="part-dnt">{t(lang.current, 'chrome.participation.dnt')}</p>
    {/if}
    <div class="part-actions">
      <button class="part-btn" class:part-primary={dntActive} class:part-secondary={!dntActive}
        onclick={() => { storeConsent(false); setParticipation(false); showParticipation = false; }}>{t(lang.current, 'chrome.participation.no_thanks')}</button>
      <button class="part-btn" class:part-primary={!dntActive} class:part-secondary={dntActive}
        onclick={async () => {
          await storeConsent(true);
          setParticipation(true);
          showParticipation = false;
          await storeLanguage(navigator.language);
          setLanguage(navigator.language);
          if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
              async (pos) => {
                const lat = Math.round(pos.coords.latitude  * 10) / 10;
                const lng = Math.round(pos.coords.longitude * 10) / 10;
                await storeGps(lat, lng);
                setGpsRegion(lat, lng);
              },
              () => {},
            );
          }
        }}>{t(lang.current, 'chrome.participation.yes_help')}</button>
    </div>
    <p class="part-policy"><a href="{base}/privacy-policy" target="_blank" rel="noopener noreferrer">{t(lang.current, 'chrome.participation.privacy_policy')}</a></p>
  </div>
</div>
{/if}

<!-- Zoom overlay -->
<div id="zoom-overlay" aria-modal="true" role="dialog" aria-label={t(lang.current, 'chrome.lightbox.map_aria')} style="display:none;">
  <button id="zoom-close" aria-label={t(lang.current, 'chrome.lightbox.map_close_aria')} title={t(lang.current, 'chrome.lightbox.close_title')}>&times;</button>
  <div id="hud">
  {#if !devNoticeDismissed}
    <div id="map-dev-notice" role="note">
      <span aria-hidden="true" class="mdn-icon"
        onclick={(e) => { e.currentTarget.parentElement?.classList.toggle('mdn-expanded'); }}
        onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.currentTarget.parentElement?.classList.toggle('mdn-expanded'); } }}
        role="button" tabindex="0">🚧</span>
      <span class="mdn-msg">{devNoticeParts.pre}<a href="mailto:wconn161@mtroyal.ca">{devNoticeParts.label}</a>{devNoticeParts.post}</span>
      <button class="mdn-dismiss" onclick={dismissDevNotice} aria-label={t(lang.current, 'chrome.map.dev_notice_dismiss')}>&times;</button>
    </div>
  {/if}
  <div id="top-bar">
    <div class="tb-group">
      <button class="tb-btn" data-map="minority">{t(lang.current, 'chrome.map.minority')}</button>
      <button class="tb-btn" data-map="majority">{t(lang.current, 'chrome.map.majority')}</button>
      <button class="tb-btn tb-map-primary" data-map="2019">{t(lang.current, 'chrome.map.current')}</button>
    </div>
    <div class="tb-sep"></div>
    <div class="tb-group">
      <button class="tb-btn" data-layer="eg" title={t(lang.current, 'chrome.map.wasted_title')}>{t(lang.current, 'chrome.map.wasted')}</button>
      <button class="tb-btn" data-layer="ed-fill" title={t(lang.current, 'chrome.map.partisan_title')}>{t(lang.current, 'chrome.map.partisan')}</button>
      <button class="tb-btn tb-layer-on" data-layer="ed-lines">{t(lang.current, 'chrome.map.borders')}</button>
    </div>
    <div class="tb-sep"></div>
    <button class="tb-btn" data-anomaly="airdrie" title={t(lang.current, 'chrome.map.flagged_title')}>{t(lang.current, 'chrome.map.flagged')}</button>
    <div class="tb-sep"></div>
    <button class="tb-btn tb-help-btn" id="tb-help-btn" aria-label={t(lang.current, 'chrome.map.help_aria')} title={t(lang.current, 'chrome.map.help_title')}>?</button>
    <div class="tb-sep"></div>
    <button class="tb-btn tb-pin-btn" data-layer="lock" title={t(lang.current, 'chrome.map.pin_title')} aria-label={t(lang.current, 'chrome.map.pin_aria')}>
      <svg class="pin-icon" viewBox="0 0 16 16" width="14" height="14" fill="currentColor" aria-hidden="true">
        <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a5.9 5.9 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182a.5.5 0 0 1-.707-.707l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a5.9 5.9 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
      </svg>
    </button>
    <div class="tb-sep"></div>
    <div id="tb-search-wrap">
      <input id="tb-search" type="search" aria-label={t(lang.current, 'chrome.map.search_aria')} placeholder={t(lang.current, 'chrome.map.search_placeholder')} autocomplete="off" spellcheck="false">
      <ul id="tb-search-results"></ul>
    </div>
    <div class="tb-sep"></div>
    <div id="ec-zoom-section">
      <span id="zoom-pct">100%</span>
      <input type="range" id="zoom-slider" min="25" max="50000" step="5" value="100" aria-label={t(lang.current, 'chrome.map.zoom_aria')}>
    </div>
    <button id="ec-close" class="tb-btn tb-close-btn" aria-label={t(lang.current, 'chrome.map.clear_aria')} title={t(lang.current, 'chrome.map.clear_title')}>&times;</button>
  </div>
  <div id="tb-share-wrap">
    <button class="tb-btn" id="tb-share-btn" onclick={toggleSharePanel} title={t(lang.current, 'chrome.share.button_title')}>{t(lang.current, 'chrome.share.button')}</button>
    {#if showSharePanel}
    <div class="share-backdrop" onclick={closeSharePanel} aria-hidden="true"></div>
    <div id="share-panel" role="dialog" aria-label={t(lang.current, 'chrome.share.dialog_aria')} aria-modal="true" tabindex="-1"
         onkeydown={(e: KeyboardEvent) => {
           if (e.key !== 'Tab') return;
           const focusable = Array.from(document.getElementById('share-panel')?.querySelectorAll('button, input') ?? []) as HTMLElement[];
           if (!focusable.length) return;
           const first = focusable[0], last = focusable[focusable.length - 1];
           if (e.shiftKey) { if (document.activeElement === first) { e.preventDefault(); last.focus(); } }
           else { if (document.activeElement === last) { e.preventDefault(); first.focus(); } }
         }}>
      <button class="share-close" onclick={closeSharePanel} aria-label={t(lang.current, 'chrome.share.close_aria')}>✕</button>
      <div class="share-section">
        <div class="share-label">{t(lang.current, 'chrome.share.share_label')}</div>
        <div class="share-code-row">
          <span class="share-code">{shareCode}</span>
          <button class="share-action-btn" onclick={copyCode}>{copyLabel}</button>
        </div>
        <div class="share-hint">{t(lang.current, 'chrome.share.share_hint')}</div>
      </div>
      <div class="share-divider"></div>
      <div class="share-section">
        <div class="share-label">{t(lang.current, 'chrome.share.load_label')}</div>
        <div class="share-load-row">
          <input
            class="share-load-input"
            type="text"
            placeholder={t(lang.current, 'chrome.share.load_placeholder')}
            bind:value={loadInput}
            onkeydown={(e) => { if (e.key === 'Enter') loadShare(); }}
            spellcheck="false"
            autocomplete="off"
          />
          <button class="share-action-btn" onclick={loadShare}>{t(lang.current, 'chrome.share.load_btn')}</button>
        </div>
        {#if loadError}<div class="share-error">{loadError}</div>{/if}
      </div>
    </div>
    {/if}
  </div>
  <!-- ed-callout — only shown when an ED is selected -->
  <div id="ed-callout" aria-live="polite">
    <div id="ec-ed-section">
      <div id="ec-name"></div>
      <div id="ec-bar"><div id="ec-ucp-bar"></div><div id="ec-ndp-bar"></div></div>
      <div id="ec-split">
        <div class="ec-party ec-ucp">
          <span class="ec-pct" id="ec-ucp-pct"></span>
          <span class="ec-party-name">UCP</span>
          <span class="ec-votes" id="ec-ucp-votes"></span>
        </div>
        <div class="ec-party ec-ndp">
          <span class="ec-pct" id="ec-ndp-pct"></span>
          <span class="ec-party-name">NDP</span>
          <span class="ec-votes" id="ec-ndp-votes"></span>
        </div>
      </div>
      <div id="ec-meta">
        <span id="ec-total-votes"></span>
        <span class="ec-meta-sep">·</span>
        <span id="ec-pop"></span>
      </div>
      <div id="ec-eg-row"><span class="ec-eg-label">EG</span> <span id="ec-eg"></span></div>
      <div id="ec-context"></div>
      <div id="ec-compare"></div>
      <div id="ec-va-hint" style="display:none;">{t(lang.current, 'chrome.map.va_hint')}</div>
    </div>
  </div>
  <div id="va-callout" aria-live="polite">
    <div id="vc-name"></div>
    <div id="vc-bar"><div id="vc-ucp-bar"></div><div id="vc-ndp-bar"></div></div>
    <div id="vc-split">
      <div class="vc-party vc-ucp">
        <span class="vc-pct" id="vc-ucp-pct"></span>
        <span class="vc-party-name">UCP</span>
      </div>
      <div class="vc-party vc-ndp">
        <span class="vc-pct" id="vc-ndp-pct"></span>
        <span class="vc-party-name">NDP</span>
      </div>
    </div>
    <span id="vc-total"></span>
    <button id="vc-close" aria-label={t(lang.current, 'chrome.map.va_close_aria')} title={t(lang.current, 'chrome.map.va_close_title')}>&times;</button>
  </div>
  <div id="map-load-error" style="display:none;"></div>
  </div><!-- /#hud -->
  <div id="sr-announce" role="status" aria-live="polite" class="sr-only"></div>
  <div id="zoom-stage">
    <div id="zoom-skeleton" aria-hidden="true">
      <!-- Alberta province outline — 31-pt RDP simplification, perimeter ≈ 1872 SVG units -->
      <div class="skel-inner">
        <svg class="skel-province-svg" viewBox="0 0 368 651" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          <defs>
            <filter id="skel-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/>
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>
          <path class="skel-province-bg"   d="M 3.25 362.94 L 29.50 4.65 L 179.23 10.25 L 319.11 4.73 L 364.29 640.15 L 209.77 646.12 L 183.67 611.14 L 186.95 584.77 L 173.60 554.80 L 166.69 558.07 L 162.81 546.63 L 150.86 539.82 L 151.53 532.09 L 128.45 512.37 L 114.98 483.74 L 105.51 488.91 L 92.08 460.83 L 83.31 464.03 L 74.42 457.99 L 78.14 448.63 L 68.85 441.88 L 60.55 448.87 L 55.96 421.21 L 47.96 418.82 L 37.39 397.66 L 33.59 403.79 L 22.32 389.51 L 11.03 387.32 L 4.87 374.07 L 11.52 371.29 L 3.25 362.94 Z" />
          <path class="skel-province-glow" d="M 3.25 362.94 L 29.50 4.65 L 179.23 10.25 L 319.11 4.73 L 364.29 640.15 L 209.77 646.12 L 183.67 611.14 L 186.95 584.77 L 173.60 554.80 L 166.69 558.07 L 162.81 546.63 L 150.86 539.82 L 151.53 532.09 L 128.45 512.37 L 114.98 483.74 L 105.51 488.91 L 92.08 460.83 L 83.31 464.03 L 74.42 457.99 L 78.14 448.63 L 68.85 441.88 L 60.55 448.87 L 55.96 421.21 L 47.96 418.82 L 37.39 397.66 L 33.59 403.79 L 22.32 389.51 L 11.03 387.32 L 4.87 374.07 L 11.52 371.29 L 3.25 362.94 Z" />
          <path class="skel-province-shine" d="M 3.25 362.94 L 29.50 4.65 L 179.23 10.25 L 319.11 4.73 L 364.29 640.15 L 209.77 646.12 L 183.67 611.14 L 186.95 584.77 L 173.60 554.80 L 166.69 558.07 L 162.81 546.63 L 150.86 539.82 L 151.53 532.09 L 128.45 512.37 L 114.98 483.74 L 105.51 488.91 L 92.08 460.83 L 83.31 464.03 L 74.42 457.99 L 78.14 448.63 L 68.85 441.88 L 60.55 448.87 L 55.96 421.21 L 47.96 418.82 L 37.39 397.66 L 33.59 403.79 L 22.32 389.51 L 11.03 387.32 L 4.87 374.07 L 11.52 371.29 L 3.25 362.94 Z" />
        </svg>
        <div class="skel-phrase">{skelPhrase || _skelPhrases[0]}</div>
      </div>
    </div>
    <object id="zoom-obj" type="image/svg+xml" data=""
      title={t(lang.current, 'chrome.map.object_title')}></object>
  </div>
  <div id="ed-tooltip"></div>
  <div id="map-attribution">
    <span id="map-ea-credit">{t(lang.current, 'chrome.map.ea_credit')} <a href="https://www.elections.ab.ca/resources/maps/" target="_blank" rel="noopener">Elections Alberta</a></span>
    <a id="map-cc-badge" href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="license noopener" title={t(lang.current, 'chrome.map.cc_title')}>
      <img src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" alt={t(lang.current, 'chrome.map.cc_alt')} width="80" height="15">
    </a>
    <span id="map-cc-owner">2026 Will Conner</span>
  </div>
</div>

<footer>
  <div class="container">
    {t(lang.current, 'chrome.footer.title')}<br>
    {t(lang.current, 'chrome.footer.copyright')}
    {t(lang.current, 'chrome.footer.text_label')} <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a> &mdash;
    {t(lang.current, 'chrome.footer.code_label')} <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v3.0</a> &mdash;
    {t(lang.current, 'chrome.footer.translation_label')} {t(lang.current, 'chrome.footer.translation_credit')}<br>
    <a href="https://ixby.github.io">ixby.github.io</a> &mdash;
    <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
  </div>
</footer>

<!-- Map onboarding modal — shown once per session via sessionStorage; logic in mapEngine.ts -->
<div id="map-intro-modal" role="dialog" aria-modal="true" aria-labelledby="map-intro-heading" style="display:none;">
  <div id="map-intro-inner">
    <h3 id="map-intro-heading">{t(lang.current, 'chrome.map_intro.heading')}</h3>
    <ul>
      <li><strong>{t(lang.current, 'chrome.map_intro.click_district')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.click_district_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.click_within')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.click_within_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.dblclick')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.dblclick_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.layers_primary')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.layers_primary_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.layers_data')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.layers_data_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.search')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.search_desc')}</li>
      <li><strong>{t(lang.current, 'chrome.map_intro.escape')}</strong> &mdash; {t(lang.current, 'chrome.map_intro.escape_desc')}</li>
    </ul>
    <p style="margin:0 0 0.9rem; font-size:0.9rem;">{@html t(lang.current, 'chrome.map_intro.s4_tip')}</p>
    <button id="map-intro-close">{t(lang.current, 'chrome.map_intro.got_it')}</button>
  </div>
</div>

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
    max-width: 62ch;
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
    max-width: 62ch;
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
    opacity: 0.7;
  }
  .back-link a {
    color: var(--text-muted);
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
}
:root[data-theme="dark"] {
  --bg:            #1e1f26;
  --bg-alt:        #26272f;
  --text:          #dde2ed;
  --text-muted:    #9ea8c0;
  --text-subtle:   #7a8296;
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
      background: var(--bg);
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
      /* Fill the visible viewport below the sticky nav so all prose lands
         below the fold; the reader scrolls past the title card to reach
         Stakes and everything else. 100svh accounts for mobile UI chrome. */
      min-height: calc(100svh - 2.75rem);
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
      max-height: min(600px, calc(100svh - 140px));
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
    .nav-landmarks {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 0.1rem;
      overflow-x: auto;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }
    .nav-landmarks::-webkit-scrollbar { display: none; }
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
    nav .nav-landmarks a.active {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }
    nav .nav-landmarks a.active::after {
      content: '';
      position: absolute;
      left: 0.7rem;
      right: 0.7rem;
      bottom: 0;
      height: 2px;
      background: var(--nav-accent);
      border-radius: 1px;
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

    .container {
      width: 100%;
      max-width: 100%;
      padding: 0 clamp(1.2rem, 4vw, 3.5rem);
      box-sizing: border-box;
    }

    section { padding: 2.2rem 0 1.8rem; border-bottom: 1px solid var(--border); scroll-margin-top: 72px; }
    section:last-of-type { border-bottom: none; }

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
    #participation-card h2::before { display: none; }

    h3 {
      font-size: 1rem;
      font-weight: 600;
      margin: 1.3rem 0 0.4rem;
      color: var(--heading-2);
    }

    p { margin-bottom: 0.9rem; }

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
      background: var(--table-bg);
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

#zoom-overlay {
    position: fixed; inset: 0; z-index: 9000;
    background: rgba(0,0,0,0.92);
    width: 100dvw; height: 100dvh;
  }
  #map-attribution {
    position: absolute; bottom: 0.6rem; inset-inline-end: 0.8rem;
    z-index: 9003; opacity: 0.55; transition: opacity 0.15s;
    display: flex; align-items: center; gap: 0.5rem;
  }
  #map-attribution:hover { opacity: 1; }
  #map-ea-credit {
    font-size: 0.6rem; color: rgba(255,255,255,0.8);
    white-space: nowrap;
  }
  #map-ea-credit a { color: rgba(255,255,255,0.9); text-decoration: underline; }
  #map-cc-badge { display: block; line-height: 0; }
  #map-cc-badge img { display: block; }
  #map-cc-owner { font-size: 0.6rem; color: rgba(255,255,255,0.7); white-space: nowrap; }
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
  #zoom-stage {
    position: absolute; inset: 0;
    overflow: hidden;
    cursor: grab;
    touch-action: none;
    will-change: transform;
  }
  #zoom-stage.dragging { cursor: grabbing; }
  /* Loading skeleton — shimmering Alberta province outline */
  #zoom-skeleton {
    position: absolute; inset: 0;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    pointer-events: none; z-index: 2;
    background: #0d1a26;
  }
  #zoom-skeleton.hidden { display: none; }
  .skel-inner {
    position: relative;
    display: flex; align-items: center; justify-content: center;
    height: 55%; max-width: 36%;
  }
  .skel-province-svg { height: 100%; width: auto; }
  .skel-province-bg {
    fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 3;
    stroke-linejoin: round; stroke-linecap: round;
  }
  .skel-province-glow {
    fill: none; stroke: #FFBE00; stroke-width: 12;
    stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 12 362;
    stroke-dashoffset: 1872;
    opacity: 0.22;
    filter: url(#skel-glow);
    animation: skel-race 4.5s linear infinite;
  }
  .skel-province-shine {
    fill: none; stroke: #FFBE00; stroke-width: 2.5;
    stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 5 369;
    stroke-dashoffset: 1872;
    animation: skel-race 4.5s linear infinite;
  }
  @keyframes skel-race {
    from { stroke-dashoffset: 1872; }
    to   { stroke-dashoffset: 0; }
  }
  .skel-phrase {
    position: absolute; top: 48%; left: 50%;
    transform: translate(-50%, -50%);
    color: rgba(255,255,255,0.78);
    font-family: 'Palatino Linotype', Palatino, Georgia, serif;
    font-style: italic; font-size: 1.05rem;
    text-align: center; pointer-events: none; white-space: normal; max-width: 88%;
    text-shadow: 0 0 14px rgba(255,190,0,0.45), 0 0 30px rgba(255,190,0,0.2);
  }
  #zoom-obj {
    position: absolute; display: block; border: 0;
  }
  #zoom-close {
    position: fixed; top: 1rem; inset-inline-end: 1.4rem; z-index: 9001;
    background: none; border: none;
    color: #fff; font-size: 2.4rem; line-height: 1;
    width: 44px; height: 44px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; opacity: 0.7;
    transition: opacity 0.15s;
  }
  #zoom-close:hover { opacity: 1; }
  /* Mobile: smaller close button so it doesn't overlap the BORDERS chip */
  @media (max-width: 600px) {
    #zoom-close { top: 0.5rem; inset-inline-end: 0.6rem; font-size: 1.6rem; }
  }
  #zoom-pct { font-weight: 700; color: rgba(255,255,255,0.75); font-variant-numeric: tabular-nums; font-size: 0.72rem; min-width: 3em; text-align: end; }
  #ed-tooltip {
    display: none; position: fixed; z-index: 9002;
    background: rgba(10,10,10,0.88);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px; padding: 0.45rem 0.7rem;
    color: #fff; font-size: 0.76rem; line-height: 1.65;
    pointer-events: none; backdrop-filter: blur(4px);
    white-space: nowrap;
  }
  #ed-tooltip strong { display: block; font-size: 0.8rem; margin-bottom: 0.1rem; }
  /* ── HUD: stacks top-bar + info-bar as a column ─────────────────────────── */
  #hud {
    position: absolute;
    top: 10px; inset-inline-start: 10px; inset-inline-end: 52px;
    z-index: 9002;
    display: flex; flex-direction: column; gap: 5px;
    pointer-events: none;

    /* Mobile: hug the edges and tighten gaps so the map gets more screen */
    @media (max-width: 600px) {
      top: 6px; inset-inline-start: 6px; inset-inline-end: 36px;  /* clears the smaller mobile close button */
      gap: 3px;
    }
  }
  #hud > * { pointer-events: auto; }
  /* Map Explorer development notice — amber strip at the top of the HUD */
  #map-dev-notice {
    display: flex; align-items: flex-start; gap: 7px;
    background: rgba(120, 84, 10, 0.92);
    border: 1px solid rgba(255, 200, 60, 0.35);
    border-radius: 8px;
    padding: 5px 9px;
    color: rgba(255, 240, 210, 0.95);
    font-size: 0.72rem; line-height: 1.45;
    backdrop-filter: blur(8px);
  }
  #map-dev-notice .mdn-icon { flex: 0 0 auto; font-size: 0.85em; }
  #map-dev-notice .mdn-msg { flex: 1 1 auto; }
  #map-dev-notice a { color: inherit; text-decoration: underline; font-weight: 600; }
  #map-dev-notice .mdn-dismiss {
    flex: 0 0 auto;
    background: none; border: none; cursor: pointer;
    color: rgba(255, 240, 210, 0.7); font-size: 1rem; line-height: 1;
    padding: 0 2px;
  }
  #map-dev-notice .mdn-dismiss:hover { color: #fff; }

  /* Mobile: collapse dev notice into a compact pill */
  @media (max-width: 600px) {
    #map-dev-notice {
      gap: 5px;
      padding: 4px 7px;
      font-size: 0.66rem;
      line-height: 1.3;
      align-items: center;
    }
    /* Two-state mobile dev notice: tap the icon to expand the message */
    #map-dev-notice:not(.mdn-expanded) .mdn-msg { display: none; }
    #map-dev-notice:not(.mdn-expanded)::after {
      content: 'BETA — tap for details';
      flex: 1 1 auto;
      color: rgba(255, 230, 180, 0.85);
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      font-size: 0.6rem;
    }
    #map-dev-notice.mdn-expanded::after { display: none; }
    #map-dev-notice .mdn-icon { cursor: pointer; }
  }
  /* ── Unified top bar ─────────────────────────────────────────────────────── */
  #top-bar {
    display: flex; align-items: center; gap: 5px; flex-wrap: wrap;
    background: rgba(10,12,18,0.88);
    border-radius: 10px; padding: 5px 8px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.07);
  }
  .tb-group { display: flex; gap: 4px; align-items: center; }
  .tb-sep { width: 1px; height: 16px; background: rgba(255,255,255,0.12); margin: 0 2px; flex-shrink: 0; }
  .tb-btn {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.55);
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;
    padding: 6px 12px; border-radius: 6px; cursor: pointer;
    transition: background 0.13s, color 0.13s, border-color 0.13s;
    white-space: nowrap;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }
  .tb-btn:hover { border-color: rgba(255,255,255,0.25); color: rgba(255,255,255,0.65); }
  .tb-btn[data-map="minority"].tb-map-primary  { background: rgba(107,53,167,0.4); border-color: #6B35A7; color: #d4b0ff; }
  .tb-btn[data-map="majority"].tb-map-primary  { background: rgba(26,122,110,0.4); border-color: #1A7A6E; color: #8eecd8; }
  .tb-btn[data-map="2019"].tb-map-primary      { background: rgba(122,152,180,0.22); border-color: #7a98b4; color: #b8d0e8; }
  .tb-btn[data-map="minority"].tb-map-overlay  { border-color: rgba(107,53,167,0.7); color: rgba(180,130,255,0.8); }
  .tb-btn[data-map="majority"].tb-map-overlay  { border-color: rgba(26,122,110,0.7); color: rgba(100,210,185,0.8); }
  .tb-btn[data-map="2019"].tb-map-overlay      { border-color: rgba(122,152,180,0.6); color: rgba(184,208,232,0.85); }
  .tb-btn.tb-layer-on { background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3); color: rgba(255,255,255,0.9); }
  .tb-pin-btn { padding: 4px 8px; }
  .tb-pin-btn .pin-icon { display: block; }
  .tb-btn[data-layer="lock"].tb-layer-on { background: rgba(220,30,30,0.15); border-color: rgba(220,30,30,0.6); color: #f05050; }
  /* Distinct color identity per layer/feature button */
  .tb-btn[data-layer="eg"]                  { border-color: rgba(200,136,42,0.32); color: rgba(200,136,42,0.7); }
  .tb-btn[data-layer="eg"].tb-layer-on      { background: rgba(200,136,42,0.14); border-color: #C8882A; color: #F0C070; }
  .tb-btn[data-layer="ed-fill"]             { border-color: rgba(184,85,168,0.32); color: rgba(184,85,168,0.7); }
  .tb-btn[data-layer="ed-fill"].tb-layer-on { background: rgba(184,85,168,0.14); border-color: #B855A8; color: #E898D8; }
  .tb-btn[data-layer="ed-lines"]                { border-color: rgba(96,120,145,0.32); color: rgba(96,120,145,0.7); }
  .tb-btn[data-layer="ed-lines"].tb-layer-on    { background: rgba(96,120,145,0.12); border-color: #607890; color: #98B8CC; }
  .tb-btn[data-anomaly]                     { border-color: rgba(208,85,64,0.38); color: rgba(208,85,64,0.78); }
  .tb-btn[data-anomaly].tb-layer-on         { background: rgba(208,85,64,0.15); border-color: #D05540; color: #F09080; }
  .tb-btn[data-anomaly]:disabled,
  .tb-btn[data-anomaly].tb-btn-disabled     { opacity: 0.32; cursor: not-allowed; border-color: rgba(128,128,128,0.25); color: rgba(128,128,128,0.45); }
  @media (max-width: 700px) { #ec-name { max-width: 120px; } #zoom-slider { width: 70px; } }

  /* Mobile: tighten top bar so the map gets more real estate */
  @media (max-width: 600px) {
    #top-bar {
      gap: 3px;
      padding: 4px 5px;
      border-radius: 8px;
    }
    .tb-group { gap: 3px; }
    .tb-sep { display: none; }   /* drop separators on phone — chip outlines provide visual grouping */
    .tb-btn {
      padding: 5px 8px;
      font-size: 0.58rem;
      letter-spacing: 0.03em;
    }
    .tb-pin-btn { padding: 3px 6px; }
    .tb-help-btn { padding: 5px 9px; }
  }
  @media (max-width: 380px) {
    /* Very narrow phones — only show button data-label icons via abbreviated text */
    .tb-btn { padding: 4px 6px; font-size: 0.54rem; }
  }
  /* District info bar — only rendered when an ED is selected */
  #ed-callout {
    background: rgba(10,12,18,0.92);
    border: 2px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 5px 10px;
    backdrop-filter: blur(10px);
    color: #fff;
    display: none; align-items: center; gap: 10px;
    min-height: 38px;
    align-self: flex-start;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  #ed-callout.ec-visible {
    display: flex;
    border-color: #F5A800;
    box-shadow: 0 0 0 1px rgba(245,168,0,0.25), 0 0 12px rgba(245,168,0,0.15);
  }
  #ec-ed-section {
    display: flex; align-items: center; gap: 8px;
    flex: 1; min-width: 0; overflow: hidden;
  }
  #ec-close { display: none; }
  #hud.ec-has-ed #ec-close { display: inline-flex; }
  .tb-close-btn { font-size: 1.1rem; line-height: 1; padding: 4px 9px; }
  #ec-name { font-size: 0.82rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; max-width: 180px; }
  #ec-bar {
    display: flex; height: 6px; border-radius: 3px;
    overflow: hidden; flex-shrink: 0; width: 72px;
  }
  #ec-ucp-bar { background: #142e94; }
  #ec-ndp-bar { background: #e86310; }
  #ec-split { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
  .ec-party { display: flex; align-items: center; gap: 3px; }
  .ec-pct { font-size: 0.8rem; font-weight: 700; font-variant-numeric: tabular-nums; }
  .ec-ucp .ec-pct { color: #6b8fd4; }
  .ec-ndp .ec-pct { color: #e8934a; }
  .ec-party-name { font-size: 0.63rem; color: rgba(255,255,255,0.45); letter-spacing: 0.04em; text-transform: uppercase; }
  .ec-votes { font-size: 0.63rem; color: rgba(255,255,255,0.45); white-space: nowrap; }
  #ec-meta { display: flex; align-items: center; gap: 5px; flex-shrink: 0; }
  #ec-pop { font-size: 0.7rem; color: rgba(255,255,255,0.55); white-space: nowrap; }
  #ec-total-votes { font-size: 0.7rem; color: rgba(255,255,255,0.55); white-space: nowrap; }
  .ec-meta-sep { font-size: 0.65rem; color: rgba(255,255,255,0.25); }
  #ec-va-count { display: none; }
  #ec-eg-row {
    display: flex; align-items: center; gap: 4px; flex-shrink: 0;
  }
  .ec-eg-label { color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 0.04em; font-size: 0.6rem; }
  #ec-eg { font-variant-numeric: tabular-nums; font-weight: 600; font-size: 0.72rem; }
  #ec-eg.ec-eg-ucp { color: #82b4e0; }
  #ec-eg.ec-eg-ndp { color: #f4a26a; }
  #ec-context { display: none; }
  #ec-compare { display: none !important; }

  /* Mobile: keep the district info compact and never let it cut off mid-percentage */
  @media (max-width: 600px) {
    #ed-callout { padding: 4px 7px; gap: 6px; min-height: 34px; flex-wrap: wrap; row-gap: 3px; }
    #ec-ed-section { gap: 6px; min-width: 0; }
    #ec-name { font-size: 0.78rem; max-width: 110px; }
    #ec-bar { width: 56px; height: 5px; }
    #ec-split { gap: 4px; }
    .ec-pct { font-size: 0.72rem; }
    .ec-party-name { display: none; }   /* "UCP" / "NDP" labels redundant with bar colours */
    .ec-votes { display: none; }        /* hide raw vote counts on phones */
    #ec-meta { gap: 4px; flex-wrap: wrap; }
    #ec-pop, #ec-total-votes { font-size: 0.64rem; }
    .ec-meta-sep { display: none; }
    .ec-eg-label { font-size: 0.55rem; }
    #ec-eg { font-size: 0.68rem; }
  }
  @media (max-width: 380px) {
    #ec-name { max-width: 92px; font-size: 0.74rem; }
    #ec-bar { width: 44px; }
    #ec-pop { display: none; }   /* the population fits poorly on the narrowest phones */
  }
  /* VA callout — secondary panel attached directly below #ed-callout in the HUD column */
  #va-callout {
    display: none;
    background: rgba(10,12,18,0.92);
    border: 1.5px solid rgba(255,255,255,0.07);
    border-top: none;
    border-radius: 0 0 10px 10px;
    margin-top: -5px; /* collapse the HUD gap to attach flush against ed-callout */
    padding: 5px 14px 9px;
    align-items: center; gap: 8px;
    max-width: 100%;
    font-size: 0.75rem; color: rgba(255,255,255,0.8);
    transition: border-color 0.2s;
  }
  #va-callout.vc-visible {
    display: flex;
    border-color: rgba(255,255,255,0.18);
  }
  /* When VA callout is visible, remove bottom rounding from ED callout so they merge.
     :has() for modern browsers; .ec-has-va class is a JS-set fallback for older ones. */
  #hud:has(#va-callout.vc-visible) #ed-callout,
  #ed-callout.ec-has-va {
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }
  #vc-name { font-size: 0.72rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0; max-width: 160px; }
  #vc-bar { display: flex; height: 4px; border-radius: 2px; overflow: hidden; flex-shrink: 0; width: 52px; }
  #vc-ucp-bar { background: #142e94; }
  #vc-ndp-bar { background: #e86310; }
  #vc-split { display: flex; align-items: center; gap: 5px; flex-shrink: 0; }
  .vc-party { display: flex; align-items: center; gap: 3px; }
  .vc-pct { font-size: 0.75rem; font-weight: 700; font-variant-numeric: tabular-nums; }
  .vc-ucp .vc-pct { color: #6b8fd4; }
  .vc-ndp .vc-pct { color: #e8934a; }
  .vc-party-name { font-size: 0.6rem; color: rgba(255,255,255,0.4); letter-spacing: 0.04em; text-transform: uppercase; }
  #vc-total { font-size: 0.65rem; color: rgba(255,255,255,0.45); white-space: nowrap; flex: 1; }
  #vc-close {
    background: none; border: none; color: rgba(255,255,255,0.4); cursor: pointer;
    font-size: 1rem; line-height: 1; padding: 2px 4px; flex-shrink: 0;
  }
  #vc-close:hover { color: rgba(255,255,255,0.75); }
  /* Zoom section — lives in top-bar */
  #ec-zoom-section {
    display: flex; align-items: center; gap: 7px;
    flex-shrink: 0;
  }
  #zoom-slider {
    width: 100px; cursor: pointer;
    accent-color: rgba(255,255,255,0.55);
  }
  .ec-cmp-header { color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.65rem; }
  .ec-cmp-item { display: flex; align-items: center; gap: 0.25rem; }
  .ec-cmp-label {
    font-size: 0.63rem; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
    border: 1px solid rgba(255,255,255,0.18); border-radius: 3px;
    padding: 0.05rem 0.35rem;
  }
  .ec-cmp-val { color: rgba(255,255,255,0.7); font-variant-numeric: tabular-nums; }
  .ec-cmp-unique { color: rgba(255,180,60,0.75); font-style: italic; font-size: 0.68rem; }

  /* In-article anomaly trigger */
  .anomaly-trigger {
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
    .skel-province-glow,
    .skel-province-shine {
      animation: none !important;
    }
    :global(.anomaly-pulse-path),
    :global(.anomaly-glow-path),
    :global(.anomaly-fill-path) {
      animation: none !important;
    }
  }

  /* Cross-map comparison — coloured party values */
  .ec-cmp-ucp { color: rgba(120,150,255,0.9); }
  .ec-cmp-ndp { color: rgba(255,160,80,0.9); }
  .ec-cmp-sep { color: rgba(255,255,255,0.25); font-size: 0.65rem; margin: 0 1px; }
  .ec-cmp-second { color: rgba(255,255,255,0.38); font-size: 0.67rem; font-variant-numeric: tabular-nums; }

  /* ED search in top bar */
  #tb-search-wrap { position: relative; display: flex; align-items: center; }
  #tb-search {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.18);
    color: rgba(255,255,255,0.85);
    border-radius: 4px;
    padding: 0.18rem 0.5rem;
    font-size: 0.76rem;
    width: 138px;
    outline: none;
    font-family: inherit;
  }
  #tb-search:focus { border-color: rgba(255,255,255,0.38); }
  #tb-search::placeholder { color: rgba(255,255,255,0.32); }
  #tb-search::-webkit-search-cancel-button { opacity: 0.4; cursor: pointer; }
  #tb-search-results {
    display: none;
    position: absolute;
    top: calc(100% + 5px);
    inset-inline-start: 0;
    min-width: 210px;
    background: #1a1a2e;
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 5px;
    list-style: none;
    margin: 0; padding: 0.25rem 0;
    z-index: 300;
    max-height: 240px;
    overflow-y: auto;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  }
  #tb-search-results li {
    padding: 0.32rem 0.75rem;
    color: rgba(255,255,255,0.78);
    font-size: 0.78rem;
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  #tb-search-results li:hover,
  #tb-search-results li.sr-active { background: rgba(255,255,255,0.18); color: #fff; }
  .sr-map-tag {
    display: inline-block; margin-inline-start: 0.4em;
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.04em;
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 3px; padding: 0.05rem 0.28rem;
    color: rgba(255,255,255,0.55); vertical-align: middle;
  }

  /* Map onboarding modal */
  #map-intro-modal {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.58);
    z-index: 9500;
    align-items: center;
    justify-content: center;
  }
  #map-intro-inner {
    background: #1a1a2e;
    color: #e0e0e0;
    border-radius: 8px;
    padding: 1.5rem;
    max-width: 430px;
    width: 90%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 28px rgba(0,0,0,0.55);
  }
  #map-intro-inner h3 { margin: 0 0 0.8rem; font-size: 1.1rem; color: #fff; }
  #map-intro-inner ul { margin: 0 0 0.8rem; padding-inline-start: 1.2rem; }
  #map-intro-inner li { margin-bottom: 0.4rem; }
  #map-intro-inner p { margin: 0 0 1rem; }
  #map-intro-close {
    background: #6B35A7;
    border: none;
    color: #fff;
    padding: 0.5rem 1.4rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.92rem;
    font-weight: 600;
  }
  #map-intro-close:hover { background: #7f46c0; }
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

  /* Screen-reader only */
  .sr-only {
    position: absolute; width: 1px; height: 1px; padding: 0;
    margin: -1px; overflow: hidden; clip: rect(0,0,0,0);
    white-space: nowrap; border: 0;
  }

  /* Tooltip must never capture pointer events */
  #ed-tooltip { pointer-events: none; }

  /* District name truncation */
  #ec-name {
    max-width: min(300px, calc(100vw - 140px));
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* VA hint in ED callout */
  #ec-va-hint {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.42);
    margin-top: 3px;
    font-style: italic;
  }

  /* Help button */
  .tb-help-btn { font-size: 0.8rem !important; font-weight: 700; }

  /* Map load error notice */
  #map-load-error {
    color: #fff;
    font-size: 0.72rem;
    padding: 5px 10px;
    border-radius: 6px;
    backdrop-filter: blur(6px);
    align-self: flex-start;
    pointer-events: none;
    background: rgba(180,60,40,0.88);
  }

  /* Mobile toolbar: horizontal scroll instead of wrap */
  @media (max-width: 600px) {
    #top-bar {
      flex-wrap: nowrap;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    #top-bar::-webkit-scrollbar { display: none; }
  }

  /* Persistent CC badge */
  #site-copyright {
    position: fixed; bottom: 0.45rem; inset-inline-end: 1rem;
    z-index: 300; opacity: 0.45; pointer-events: auto;
    transition: opacity 0.15s;
  }
  #site-copyright:hover { opacity: 0.85; }
  #site-copyright a { display: block; line-height: 0; }
  #site-copyright img { display: block; }
  :root[data-theme="dark"] #site-copyright { opacity: 0.3; }
  :root[data-theme="dark"] #site-copyright:hover { opacity: 0.7; }

  /* Back-to-top button */
  #back-top {
    position: fixed; bottom: 1.6rem; inset-inline-end: 1.4rem;
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
  @media (max-width: 600px) { #back-top { bottom: 1rem; inset-inline-end: 0.8rem; } }

  /* ── Participation prompt ─────────────────────────────────────────────── */
  :global(#participation-overlay) {
    position: fixed; inset: 0; z-index: 9100;
    background: rgba(0,0,0,0.55);
    display: flex; align-items: center; justify-content: center;
    padding: 1rem;
  }
  :global(#participation-card) {
    background: var(--bg, #fff);
    color: var(--text, #111);
    border-radius: 10px;
    padding: 2rem 2.2rem;
    max-width: 480px; width: 100%;
    box-shadow: 0 8px 32px rgba(0,0,0,0.28);
  }
  :global(#participation-card h2) {
    margin: 0 0 1rem; font-size: 1.15rem; font-weight: 600; line-height: 1.3;
  }
  :global(#participation-card p) {
    margin: 0 0 0.9rem; font-size: 0.88rem; line-height: 1.55; color: var(--text-muted, #444);
  }
  :global(.part-no-collect) {
    font-size: 0.82rem !important;
    color: var(--text-muted, #666) !important;
    opacity: 0.85;
  }
  :global(.part-dnt) {
    font-size: 0.82rem !important;
    background: rgba(107,53,167,0.08);
    border-inline-start: 3px solid #6B35A7;
    padding: 0.5rem 0.7rem;
    border-start-start-radius: 0; border-start-end-radius: 4px;
    border-end-end-radius: 4px; border-end-start-radius: 0;
  }
  :global(.part-actions) {
    display: flex; gap: 0.6rem; justify-content: flex-end; margin: 1.2rem 0 0.8rem;
  }
  :global(.part-btn) {
    padding: 0.5rem 1.2rem; border-radius: 6px;
    border: none; cursor: pointer; font-size: 0.88rem; font-weight: 500;
    transition: opacity 0.15s;
  }
  :global(.part-btn:hover) { opacity: 0.82; }
  :global(.part-secondary) { background: var(--btn-muted, #e8e8e8); color: var(--text, #111); }
  :global(.part-primary)   { background: #6B35A7; color: #fff; }
  :root[data-theme="dark"] :global(.part-secondary) { background: #3a3b47; color: var(--text); }
  :root[data-theme="dark"] :global(.part-primary)   { background: #8B50D4; color: #fff; }
  :global(.part-policy) {
    font-size: 0.78rem !important; text-align: end;
    margin: 0 !important; color: var(--text-muted, #888) !important;
  }
  :global(.part-policy a) { color: inherit; text-decoration: underline; opacity: 0.7; }

  /* ── Share panel ─────────────────────────────────────────────────────── */
  :global(.share-backdrop) {
    position: fixed; inset: 0; z-index: 7999;
  }
  :global(.share-close) {
    position: absolute; top: 0.5rem; inset-inline-end: 0.55rem;
    background: none; border: none; cursor: pointer;
    color: rgba(255,255,255,0.45); font-size: 0.95rem; line-height: 1;
    padding: 0.2rem 0.35rem; border-radius: 4px;
    transition: color 0.15s;
  }
  :global(.share-close:hover) { color: rgba(255,255,255,0.85); }
  :global(#tb-share-wrap) {
    position: absolute; top: 5px; inset-inline-end: 0;
    z-index: 200;
  }
  :global(#share-panel) {
    position: absolute; top: calc(100% + 6px); inset-inline-end: 0;
    background: rgba(10,12,18,0.95); border: 1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(12px);
    border-radius: 8px; padding: 0.85rem; width: 320px;
    max-width: calc(100vw - 16px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.55);
    z-index: 8000;
  }
  :global(.share-section) { display: flex; flex-direction: column; gap: 0.45rem; }
  :global(.share-label) { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; opacity: 0.55; }
  :global(.share-code-row) { display: flex; align-items: center; gap: 0.5rem; }
  :global(.share-code) {
    flex: 1; font-family: monospace; font-size: 0.92rem; font-weight: 600;
    letter-spacing: 0.02em; background: rgba(255,255,255,0.06);
    padding: 0.4rem 0.6rem; border-radius: 5px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  :global(.share-action-btn) {
    padding: 0.35rem 0.75rem; border-radius: 5px; border: none;
    background: #6B35A7; color: #fff; font-size: 0.8rem; font-weight: 500;
    cursor: pointer; white-space: nowrap; transition: opacity 0.15s;
    flex-shrink: 0;
  }
  :global(.share-action-btn:hover) { opacity: 0.82; }
  :global(.share-hint) {
    font-size: 0.74rem; opacity: 0.5; line-height: 1.4;
  }
  :global(.share-divider) {
    height: 1px; background: rgba(255,255,255,0.1); margin: 0.7rem 0;
  }
  :global(.share-load-row) { display: flex; gap: 0.5rem; }
  :global(.share-load-input) {
    flex: 1; padding: 0.38rem 0.55rem; border-radius: 5px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.06); color: inherit;
    font-family: monospace; font-size: 0.85rem;
  }
  :global(.share-load-input::placeholder) { opacity: 0.4; }
  :global(.share-error) {
    font-size: 0.76rem; color: #e57373; margin-top: 0.3rem;
  }
  @media (max-width: 600px) {
    :global(.share-backdrop) { z-index: 9001; }
    :global(#share-panel) {
      position: fixed;
      top: auto; bottom: 0; left: 0; right: 0;
      width: 100%; border-radius: 14px 14px 0 0;
      padding: 1.1rem 1rem 1.4rem;
      box-shadow: 0 -4px 24px rgba(0,0,0,0.5);
      z-index: 9002;
    }
  }
</style>
