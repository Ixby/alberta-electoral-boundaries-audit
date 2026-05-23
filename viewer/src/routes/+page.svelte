<!--
  Alberta Electoral Boundary Audit — main page
  © Will Conner 2026
  Text/content: CC BY-NC-SA 4.0 <https://creativecommons.org/licenses/by-nc-sa/4.0/>
  Code: GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  https://ixby.github.io
-->
<svelte:head>
  <meta name="description" content="Statistical audit of Alberta's 2026 electoral boundary commission — 1,010,000 neutral maps, official Elections Alberta shapefiles, pre-registered tests.">
  <meta name="author" content="Will Conner">
  <meta name="copyright" content="© Will Conner 2026">
  <meta name="license" content="Text/content: CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/); Code: GNU GPL v3.0 (https://www.gnu.org/licenses/gpl-3.0.html)">
  <link rel="icon" type="image/svg+xml" href="{base}/favicon.svg">
  <link rel="apple-touch-icon" href="{base}/favicon.svg">
</svelte:head>

<script lang="ts">
  import { onMount } from 'svelte';
  import { base } from '$app/paths';
  import { init, onEvent as mapOnEvent, getState, applyState } from '$lib/mapEngine';
  import { isDNT, setParticipation, recordEvent, encodeState, decodeState } from '$lib/share';

  // ── Share / participation state ───────────────────────────────────────────
  let showParticipation = $state(false);
  let dntActive         = $state(false);
  let showSharePanel    = $state(false);
  let shareCode         = $state('');
  let loadInput         = $state('');
  let copyLabel         = $state('Copy');
  let loadError         = $state('');

  function _generateCode() {
    const s = getState();
    shareCode = s ? (encodeState(s) ?? '—') : '—';
  }

  function toggleSharePanel() {
    showSharePanel = !showSharePanel;
    if (showSharePanel) { _generateCode(); loadError = ''; }
  }

  async function copyCode() {
    if (!shareCode || shareCode === '—') return;
    try {
      await navigator.clipboard.writeText(shareCode);
      copyLabel = 'Copied!';
    } catch {
      copyLabel = 'Failed';
    }
    setTimeout(() => { copyLabel = 'Copy'; }, 2000);
  }

  function loadShare() {
    const trimmed = loadInput.trim();
    if (!trimmed) return;
    const decoded = decodeState(trimmed);
    if (!decoded) { loadError = 'Unrecognised code — check spelling.'; return; }
    applyState(decoded.primary, decoded.mapOn, decoded.layers);
    showSharePanel = false;
    loadInput  = '';
    loadError  = '';
  }

  let skelPhrase = 'Loading Map Explorer…';
  const _SKEL_PHRASES = [
    'Loading Map Explorer…', 'drawing Alberta…', 'crunching the numbers…',
    'counting every vote…', 'plotting the boundaries…', 'almost there…',
  ];
  let _skelIdx = 0;

  onMount(() => {
    init(base);
    mapOnEvent(recordEvent);

    dntActive = isDNT();
    setTimeout(() => { showParticipation = true; }, 900);

    // ── Skeleton phrase cycling ───────────────────────────────────────────────
    setInterval(() => {
      _skelIdx = (_skelIdx + 1) % _SKEL_PHRASES.length;
      skelPhrase = _SKEL_PHRASES[_skelIdx];
    }, 2800);

    // ── Dark mode — light by default; user toggle persisted in localStorage ─
    const root = document.documentElement;
    const stored = localStorage.getItem('theme');
    if (stored === 'dark') root.setAttribute('data-theme', 'dark');
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });

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

    function openLb(src: string) {
      lbScale = 1; lbImg.style.transform = '';
      lbImg.src = src;
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
      (img as HTMLElement).addEventListener('click', () => openLb((img as HTMLImageElement).src));
    });
    lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
    lb.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeLb();
      if (e.key === 'Tab') e.preventDefault();
    });

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

<nav aria-label="Page sections">
  <div class="nav-inner">
  <a href="#top" class="nav-home" aria-label="Back to top"><svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 2L2 9h2v9h5v-5h2v5h5V9h2L10 2z"/></svg></a>
  <a href="#section-1">Map</a>
  <a href="#section-2">The Split</a>
  <a href="#section-3">Litmus Test</a>
  <a href="#section-4">Crack &amp; Pack</a>
  <a href="#section-5">Impact</a>
  <a href="#section-6">Gerrymanders</a>
  <a href="#section-7">Lunty</a>
  <a href="#section-8">Suggestions</a>
  <a href="#retractions">Retractions</a>
  <a href="#references">References</a>
  <a href="#resources">Technical</a>
  <button id="theme-toggle" class="nav-theme-btn" aria-label="Toggle dark/light mode" title="Toggle dark mode">
    <svg class="icon-sun" width="15" height="15" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-9a1 1 0 0 0 1-1V2a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm0 14a1 1 0 0 0 1-1v-1a1 1 0 0 0-2 0v1a1 1 0 0 0 1 1zm7-7a1 1 0 0 0 0-2h-1a1 1 0 0 0 0 2h1zM4 10a1 1 0 0 0-1-1H2a1 1 0 0 0 0 2h1a1 1 0 0 0 1-1zm10.95-4.95a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm-9.9 9.9a1 1 0 0 0-1.41-1.41l-.71.71a1 1 0 0 0 1.41 1.41l.71-.71zm9.9.01a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71zm-9.9-9.9a1 1 0 0 0 1.41-1.41l-.71-.71a1 1 0 0 0-1.41 1.41l.71.71z"/></svg>
    <svg class="icon-moon" width="14" height="14" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path d="M17.293 13.293A8 8 0 0 1 6.707 2.707a8.001 8.001 0 1 0 10.586 10.586z"/></svg>
  </button>
  </div>
</nav>

<header>
  <div class="header-inner">
    <div class="header-text">
      <h1>Alberta Electoral Boundary Audit</h1>
      <p class="subtitle">Alberta's commission produced two riding maps in 2026. This audit compared them — using the same tests, applied equally to both — to ask whether they treat voters the same way.</p>
      <span class="badge">Official Elections Alberta maps &mdash; Published May 2026</span>
      <p class="cover-note">Click to zoom and explore all three boundary proposals simultaneously. Pin the viewport and flip between maps &mdash; boundaries shift, voters stay put. Scroll down for the analysis.</p>
    </div>
    <button id="zoom-trigger" class="hero-map-btn" title="Click to open interactive map" aria-label="Open interactive map">
      <div class="hero-map-wrap">
        <img src="images/cover_art.png" alt="Alberta electoral district maps — minority commission proposal, coloured by 2023 vote" class="header-image" fetchpriority="high" loading="eager" width="1020" height="1807">
        <img src="images/province_outline.svg" class="province-border-overlay" aria-hidden="true" alt="" fetchpriority="high" loading="eager">
        <div class="hero-map-hint">Click to explore interactively</div>
      </div>
    </button>
  </div>
</header>

<main class="container">

  <div style="padding: 1.5rem 0 0.5rem;">
    <div class="callout" style="background:#F0EBF8; border-left-color:#6B35A7; font-size:1.05rem; padding:0.9rem 1rem; margin-bottom:0.8rem;">
      <p style="margin:0;"><strong>Is the minority map a gerrymander?</strong> The commission&rsquo;s minority map would occur by chance in fewer than 1&nbsp;in&nbsp;14.5&nbsp;million randomly drawn maps. The majority map falls well within normal range.</p>
    </div>
    <div class="callout" style="background: #D0EEEA; border-left-color: #1A7A6E; font-size: 1.02rem; line-height: 1.65;">
      <p style="margin:0 0 0.6rem;"><strong>TL;DR</strong></p>
      <p style="margin:0 0 0.6rem;">Alberta's redistribution commission split 3&ndash;2 in 2026 and produced two different proposed maps. The government set both aside and assigned redistricting to a five-member committee of MLAs (the Lunty committee), expected to report in November 2026. Neither commission map is law.</p>
      <p style="margin:0 0 0.6rem;">This audit tested both commission maps the same way, using 1,010,000 computer-drawn neutral maps built from the official Elections Alberta shapefiles as a reference point. The majority proposal sits within the neutral range on every pre-registered test. The minority proposal crosses four of five structural tests, and its partisan-fairness seat split at a 50/50 vote is reached by fewer than 100 of those neutral maps &mdash; a joint probability of roughly 1 in 15 million under a neutral drawing process.</p>
      <p style="margin:0;">The audit measures outcomes, not intent. When the Lunty committee releases its map, this audit will apply the same tests to it.</p>
      <p style="margin:0.6rem 0 0; font-size:0.88rem; color:#555;">Pre-registered falsification conditions and retraction commitments are in <a href="#retractions">§9</a>.</p>
    </div>
  </div>

  <section id="section-1">
    <h2>1: The Map <a href="#section-1" class="section-link" aria-label="Link to section 1">#</a></h2>
    <p>The cover map is the best single image in this audit. Here is how to read it.</p>
    <p>Alberta is divided into 4,765 Voting Areas — small geographic zones Elections Alberta uses to count polling-station ballots. Each one is coloured by how people in it actually voted in 2023: orange where NDP votes are concentrated, blue where UCP votes are concentrated. But the colour only becomes dark and saturated where a lot of people live. A Voting Area that covers hundreds of square kilometres of parkland or farmland stays pale — nearly invisible. The map lights up where people are, and fades where they aren't.</p>
    <p>This is very different from the Alberta you see on election night. Most election maps colour entire ridings solid blue or orange based on who won. Rural ridings are geographically large and the UCP wins most of them, so election-night Alberta looks like a wall of blue with small orange pockets in Edmonton and Calgary. The cover map uses the same votes and the same geography — but shows them weighted by where people actually live. What appears is a province where most of the population is concentrated in a dense arc of cities, and those cities vote very differently from the rural map that normally represents them.</p>
    <p>The boundary lines drawn over the colour are the minority commission's 89 proposed electoral districts — the map this audit ends up critiquing. The audit's work is to ask what those lines do to the people underneath them.</p>
    <p>For me personally, this was the image that made the stakes clear. A province that looks like it votes one way on a standard map is actually a province where most of the people live in areas that vote the other way. Once you can see the population underneath the boundary choices, those choices stop looking random.</p>
  </section>

  <section id="section-2">
    <h2>2: How the Commission Broke <a href="#section-2" class="section-link" aria-label="Link to section 2">#</a></h2>
    <p>Alberta's Electoral Boundary Commission finished its work on March 23, 2026 and could not agree. Three commissioners produced one map; the other two produced a different one. Commission Chair Justice Dallas K. Miller and two opposition-nominated commissioners wrote the majority report; two government-nominated commissioners — Dr. Julian Martin and John D. Evans — wrote the minority report. The split centred on how to draw boundaries in fast-growing urban-edge communities: the majority gave Airdrie two districts, the minority four; the majority drew northwest Calgary's divisions close to the provincial average size, the minority drew them 11.5% above it. Both maps follow the same statute; the disagreement was about which specific geographic configurations best served the communities being drawn. Both are legal under the <em>Electoral Boundaries Commission Act</em>. The governing party is the United Conservative Party (UCP); its main opposition is the New Democratic Party (NDP). Alberta also has smaller parties — the Alberta Party, the Liberal Party of Alberta, and others — that contest seats but whose combined provincial vote share has remained low enough in recent elections that they do not materially affect the audit's partisan-fairness calculations, which are grounded in the 2023 UCP–NDP vote split. This audit measured both maps using the same methods, applied identically. Three findings stand out.</p>
    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;"><strong>The two maps differ on six things you can measure without looking at any election results:</strong> how evenly people are spread across districts, whether voters are concentrated, how badly cities are cut up, whether borders follow city limits, the shape of the districts, and how many boundaries the commission's own chair flagged as anomalous. The minority map differs from the majority on every one of them.</li>
      <li style="margin-bottom: 0.6rem;"><strong>Every measured difference cuts the same way.</strong> Everywhere the two maps diverge — northwest Calgary, Airdrie, urban areas with clear city limits — the minority map draws boundaries that spread NDP votes thinner and let UCP votes count more efficiently. The communities most reshaped by the minority map are the same communities where the NDP is strongest. The audit cannot determine intent. It can measure effect.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The process now promoting the minority map has no precedent in Canada.</strong> No other province lets a cabinet hand redistricting to a committee its own party controls partway through a redistribution cycle. Most provinces either require the legislature to debate the commissioners' map first, or give the commission's map automatic effect unless overridden. Alberta does neither. On April 16, the government set both commission maps aside and assigned the work to a five-member committee of MLAs (Members of the Legislative Assembly), three from the governing United Conservative Party (UCP). Alberta's <em>Electoral Boundaries Commission Act</em> requires the legislature to pass a separate Electoral Districts Act to give a commission report legal effect — the commission report itself changes nothing. Most other provinces make a commission's report legally effective unless the legislature actively overrides it; Alberta's default reverses that, meaning the governing party controls whether any commission map ever becomes law. The government's stated justification was to implement Commission Chair Justice Miller's Recommendation 5. But Miller had written that recommendation specifically to dissuade the legislature from accepting the minority map, and his majority colleagues did not endorse it. Recommendation 5 was also geographically specific: one additional rural seat south of Edmonton, and one in Clearwater County and western Mountain View County — both far from the fast-growing Calgary and Edmonton urban-edge communities where the commission actually split. It was not an invitation to redesign those contested boundaries. The government adopted the seat count while handing a committee it controls authority over exactly the lines the commission disagreed on.</li>
    </ol>
    <p><strong>The process is its own finding, separate from the maps.</strong></p>
  </section>

  <div class="callout" style="background:#EAF3FF; border-left-color:#2B5BA1; margin:0.5rem 0 1rem;">
    <p style="margin:0 0 0.4rem;"><strong>Structural audit results — before any statistics:</strong></p>
    <p style="margin:0;">The majority map crosses <strong>zero of five</strong> pre-registered structural thresholds. The minority map crosses <strong>all five</strong>. These are geometric measurements — population spread, <button class="vocab-term" data-def="how closely a district's borders follow pre-existing city and municipal limits, rather than cutting through them" aria-expanded="false">municipal anchoring</button>, Airdrie split count, NW Calgary population excess, and chair-flagged boundary anomalies — that require no election data and no statistical sampler. The next section tests both maps against 1,010,000 computer-generated neutral maps and reaches the same conclusion through a completely different instrument.</p>
  </div>

  <section id="section-3">
    <h2>3: The 1,010,000-Map Litmus Test <a href="#section-3" class="section-link" aria-label="Link to section 3">#</a></h2>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane1_dotplot.svg" alt="Histogram showing the distribution of efficiency gaps across 250,000 neutral Alberta maps. Most maps cluster near zero. The minority commission map (purple line) sits at the 94th percentile (+4.0%), in the shaded right tail. The majority map (teal line) sits at +0.1%, well within the normal range." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;" width="463" height="247" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">Distribution of <button class="vocab-term" data-def="a measure of how lopsidedly votes are converted into seats — positive values favour the UCP, negative values favour the NDP" aria-expanded="false">efficiency gaps</button> across 250,000 neutral Alberta maps drawn from the same geography. Most neutral maps cluster near zero; the shaded right tail marks the top 10%. The minority proposal&rsquo;s +4.0% sits at the 94th <button class="vocab-term" data-def="the percentage of maps that scored lower — p94 means 94 out of 100 neutral maps were less partisan than this" aria-expanded="false">percentile</button> — a region fewer than 6 in 100 neutral maps ever reach. The majority proposal&rsquo;s +0.1% is indistinguishable from what a neutral process typically produces.</figcaption>
    </figure>

    <p>The table compares the two maps. The first five rows use no election results — they're properties of the lines themselves. The last two depend on how votes were attributed to each district.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>What was measured</th>
            <th>Majority map</th>
            <th>Minority map</th>
            <th>Direction / Beneficiary</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Population spread across districts (tighter is better)</td>
            <td class="normal">3,180</td>
            <td class="flag">4,707 — 48% wider</td>
            <td>Structural (Reduces vote equality)</td>
          </tr>
          <tr>
            <td>NW Calgary population excess above average</td>
            <td class="normal">2.8%</td>
            <td class="flag">11.5%</td>
            <td><strong>UCP</strong> (Packs urban NDP votes)</td>
          </tr>
          <tr>
            <td>Airdrie split</td>
            <td class="normal">2 divisions</td>
            <td class="flag">4 divisions</td>
            <td><strong>UCP</strong> (Cracks urban/suburban power)</td>
          </tr>
          <tr>
            <td>Borders that follow existing municipal lines</td>
            <td>80% — within norm</td>
            <td>72% — within norm</td>
            <td>N/A — both within Canadian norm (70–85%)</td>
          </tr>
          <tr>
            <td>Boundaries flagged by the commission chair</td>
            <td class="normal">0</td>
            <td class="flag">3</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Seats at 50/50 votes (percentile in 1,010,000-map simulation)</td>
            <td class="normal">46.1% — p83 (normal range)</td>
            <td class="flag">51.7% — p99.99 (fewer than 100 of 1,010,000 reach this)</td>
            <td><strong>UCP</strong></td>
          </tr>
          <tr>
            <td>Compactness-Weighted Efficiency Gap</td>
            <td class="normal">+1.5%</td>
            <td class="flag">-2.4%</td>
            <td><strong>UCP</strong> (via irregular shapes)</td>
          </tr>
          <tr>
            <td>Packing-cracking neighbourhood pattern</td>
            <td>6 coupled chain signals</td>
            <td class="normal">2 (pre-registered PASS)</td>
            <td>Neutral — minority achieves partisan effect via hybridization, not adjacency drain (§5.3.5)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="callout">
      <p><strong>VOCABULARY</strong></p>
      <p><strong>Efficiency gap.</strong> A single number that measures how lopsidedly a party's votes are translated into seats. Positive numbers favour the UCP; negative favour the NDP. The audit uses ~5% as Alberta's outlier line — the value exceeded by only 5% of the 1,010,000 neutral Alberta-specific simulations. This threshold is not borrowed from US or general literature; a threshold calibrated to another jurisdiction would be wrong because Alberta's natural geography produces a different neutral range.</p>
      <p><strong>Mean-median difference.</strong> The gap between a party's median district vote share and its mean district vote share. When one party wins many close races, the median sits above the mean — those votes are distributed efficiently. When a party wins many races by large margins, the mean sits above the median — votes are being wasted. A large mean-median gap in one direction flags structural inefficiency in how one side's votes are spread across districts.</p>
      <p><strong>Percentile ranking.</strong> In this audit, a "percentile" is a rank within the 1,010,000 neutral simulated maps. "p94" means 94% of neutral maps score lower — the real map is more extreme than 94% of neutral draws. "p99.99" means fewer than 1 in 10,000 neutral maps reach that level.</p>
      <p><strong>Anchoring.</strong> The fraction of an electoral border that lies on a pre-existing administrative line — a city limit, a school-division boundary, a Statistics Canada census line.</p>
    </div>

    <p>The bottom rows depend on election results. The <em>seats@50/50</em> test holds the electorate at perfect parity (UCP and NDP each win exactly half the votes province-wide) and asks how many seats the map awards the UCP. A neutral Alberta map produces a median around 44.8% UCP seats — Alberta's geography (NDP voters concentrated in city cores, UCP voters spread across rural ridings) gives the NDP a small efficiency advantage at neutrality. The majority map at 46.1% sits at the 83rd percentile of the 1,010,000-map simulation (normal range). The minority map at 51.7% is at the 99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach that value. The <em>efficiency gap</em> number measures how lopsidedly each party's votes get translated into seats; on the official Elections Alberta shapefiles the minority's efficiency gap is +4.0%, placing it at the 94th percentile — just below the audit's 95th-percentile outlier line. The verdict section unpacks the consequences.</p>

    <p>The last row is where the minority map has fewer coupled chain signals than the majority on the neighbour-drain test: 2 against the majority's 6 (and the 2019 enacted map's 5). The audit pre-registered this test before measuring, and the minority's lower count is a genuine pre-registered PASS — the minority does not show the classic pack-and-drain adjacency pattern. It is the single test where the minority numerically outperforms the majority. §5.3.5 of the academic report explains why: the minority achieves its partisan effect through hybridization (city-splitting that internalises packing and cracking within individual EDs), which is invisible to an adjacency-chain test that only measures how packed districts cluster next to cracked ones.</p>
  </section>

  <section id="section-4">
    <h2>4: Cracking, Packing, and Draining <a href="#section-4" class="section-link" aria-label="Link to section 4">#</a></h2>

    <div class="callout">
      <p><strong>Three moves, one playbook</strong></p>
      <p><strong>Packing</strong> means cramming one party's voters into districts that party wins by landslides — each packed ballot still counts, but it contributes nothing beyond victory. Large, lopsided wins. Wasted votes.</p>
      <p><strong>Cracking</strong> means splitting a community across multiple districts so it wins none of them outright. A city strong enough to carry two seats gets carved into four, each tethered to a different rural area. Diluted votes. No seat for anyone.</p>
      <p><strong>Draining</strong> is the spatial companion: packed and cracked districts are placed next to each other so that over-concentrated supporters on one side "drain" voting power away from the contested districts nearby. The adjacency pattern amplifies both effects — packing and cracking reinforce each other across district lines.</p>
      <p>All three can occur without any explicit partisan intent. What the audit measures is whether the pattern — and its statistical magnitude — is consistent with what a neutral map-drawing process produces. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md#5-results" rel="noopener">Full methodology at §5 of the technical report.</a></p>
    </div>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/figure_airdrie_v3.svg" alt="Map showing the division of Airdrie into four separate districts under the minority map" style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;" width="504" height="336" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The division of Airdrie into four separate districts under the minority map, diluting its urban voting power.</figcaption>
    </figure>

    <p>The five commissioners worked from the same statutory rules, the same provincial geography, the same archive of 1,140 public submissions, and the same demographic data. Their two competing drafts agree on most of Alberta. Where the drafts diverge, they diverge on choices someone in the room had to make. Three of those choices are worth seeing as choices, not numbers.</p>

    <p><strong>It splits the City of Airdrie into four pieces.</strong> The law caps each electoral division at one-and-a-quarter times the provincial average, so Airdrie needs at least two divisions. The majority map gives it two. The minority gives it four — north to Calgary-Nolan Hill-Cochrane, east to Airdrie East, west to Calgary-Foothills-Airdrie West, and centre-south to Calgary-Airdrie — each one stapled to a different rural or Calgary-edge district. An Airdrie resident with a question for her MLA has to know which quarter of the city she lives in before she can call the right office. Her neighbours two blocks over will give her three different answers. The PTA at her child's school cannot send a single delegation to one MLA on a school-funding question; they have to coordinate four delegations to four offices, each MLA primarily accountable to a different rural or suburban constituency. The minor-hockey association, the food bank, the Chamber of Commerce — every organization that operates citywide now operates across four provincial ridings.</p>

    <div class="callout">
      <p><strong>WHY AIRDRIE MATTERS</strong></p>
      <p>Airdrie is the largest Alberta city without its own MLA. At 85,805 people (2024 municipal census) it is bigger than Red Deer; it has one council, one tax bill, one school division — every civic system treats it as a unit.</p>
      <p>Splitting it across four provincial divisions — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, and Airdrie East — each primarily identified with a different surrounding jurisdiction, removes Airdrie from the political map at the level of government that draws it. The city has 85,805 residents and zero seats in the legislature where a majority of voters call the place home.</p>
      <p>A four-way split is invisible to every partisan-fairness test except the one that asks: can a voter find their MLA?</p>
    </div>

    <div class="callout">
      Both maps are legal. The four-way split is a choice.
    </div>

    <p style="text-align:center; margin: 0.2rem 0 1.1rem;">
      <button class="anomaly-trigger" data-anomaly="airdrie">Show flagged districts on map</button>
    </p>

    <p><strong>Where it departs from municipal lines, it departs at strategically important places.</strong> When electoral maps follow the edge of a city or town, voters recognize where their division begins and ends — the property-tax line, the school-division line, the local-election ward line, and the provincial-election line all coincide. Statistics Canada publishes these boundaries for free. On official Elections Alberta shapefiles, both maps follow municipal lines at comparable overall rates: the majority at 80%, the minority at 72%, both within Canada's 70–85% norm (Quebec: 78%, Ontario: 82%, BC: 71%; comparator commissions documented in the monograph). (The audit's initial provisional analysis showed the minority anchoring at only 15%; that figure did not survive recomputation on official shapefiles — see the correction note below.) The striking observation is not the overall rate but where the minority's departures are concentrated: the three boundaries the commission's own chair flagged as anomalous — Rocky Mountain House–Banff Park <button class="ed-trigger" data-ed-name="Rocky Mountain House-Banff Park">show ↗</button>'s extension into uninhabited national-park land, the Nolan Hill–Cochrane <button class="ed-trigger" data-ed-name="Calgary-Nolan Hill-Cochrane">show ↗</button> lasso corridor, and the Olds–North Airdrie <button class="ed-trigger" data-ed-name="Olds-Three Hills-Didsbury">show ↗</button> reach — are each departures from pre-existing civic geography in the exact urban-edge zones where pairing urban and rural voters most directly affects which party wins the seat.</p>

    <p>The minority commissioners gave reasons for each of the three flagged boundaries. For Rocky Mountain House–Banff Park, they cited geographic size, the Highway 22 corridor, and the proximity of First Nations reserves to Rocky Mountain House; the commission chair called the extension into uninhabited national park land "a bad faith effort" to satisfy the area criterion, and that phrase appears in the commission's official final report. For Nolan Hill–Cochrane, they cited shared transportation and employment ties between northwest Calgary and Cochrane; Statistics Canada journey-to-work data shows only 35.8% of Cochrane workers travel to Calgary at all, with most working within Cochrane itself. For the Olds–North Airdrie reach, they cited Highway 2 corridor continuity; the audit found the specific Airdrie extension fails on population grounds. Independent check found five of the minority's six published sub-rationales fail or only partially hold against primary data.</p>

    <p><strong>One area of Calgary is carved up to concentrate NDP voters into larger-than-average divisions.</strong> In Calgary's northwest quadrant <button class="ed-trigger" data-ed-name="Calgary-North West-Bearspaw">show ↗</button>, the minority map's divisions average 11.5% above the province-wide population — versus 2.8% on the majority. The same geographic zone, drawn by the same commission under the same constraints, produces districts a quarter larger on one map than on the other. This is <em>packing</em>: concentrating one party's voters into fewer, larger districts so each of their ballots weighs less. Packing and <em>cracking</em> (splitting a party's voters thinly across districts they narrowly lose) are the two classic gerrymandering moves; both shrink a party's seat count below its vote share.</p>

    <p>The commission chair — appointed under the same Act, working from the same submissions — flagged three boundaries on the minority map as geographically anomalous: Rocky Mountain House–Banff Park's extension into uninhabited national park land; the Calgary-Nolan Hill–Cochrane lasso-shaped corridor; the Olds–Three Hills–Didsbury reach into north Airdrie. The majority received zero such flags from the same chair. (The chair's published criticism covers seven boundary configurations in total — four geometric flags in the main report and three in Appendix C. This audit independently confirmed anomalous geometry for three of the four geometric flags; the fourth, Calgary-Foothills-Airdrie West <button class="ed-trigger" data-ed-name="Calgary-Foothills-Airdrie West">show ↗</button>, did not meet the audit's confirmation threshold.)</p>
  </section>

  <section id="section-5">
    <h2>5: The Impact on the Ground <a href="#section-5" class="section-link" aria-label="Link to section 5">#</a></h2>

    <div class="callout">
      <p><strong>LANE 1 AND LANE 2</strong></p>
      <p><strong>Lane 1 (numbers)</strong> uses election results to test whether the map converts votes into seats fairly — it asks how the map performs across different vote splits. <strong>Lane 2 (structure)</strong> examines only the drawn lines — city splits, population spread, boundary shapes — with no election data at all. Each lane is independent: a map can fail one while passing the other. The minority proposal fails both; the majority passes both.</p>
    </div>

    <p>Lane 1 depends on which election results you score the maps against. Lane 2 does not. The structural evidence is in the maps themselves — drawn lines, split cities, where the boundaries do and don't follow administrative lines that exist for other reasons. On these tests, the two maps are not close.</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/lane2_bars.svg" alt="Bar chart comparing five structural-fairness tests side by side. The majority map bars sit at zero or well inside safe ranges. The minority map bars cross every threshold by a wide margin." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;" width="441" height="545" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The five structural-fairness tests, side by side. Teal bars are the majority map; purple bars are the minority map. The dashed line in each row marks the failing threshold. The minority bars cross every threshold by a wide margin. The majority bars sit flat at zero or well inside the safe range.</figcaption>
    </figure>

    <p>The same five tests in tabular form, with each test's threshold stated alongside the result. The bottom row is the audit's <em>summary</em> — the count of tests each map fails out of the five.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Test</th>
            <th>Majority map</th>
            <th>Minority map</th>
            <th>Direction / Beneficiary</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Border follows existing municipal lines (70–85% Canadian norm)</td>
            <td class="normal">80% — within norm</td>
            <td>72% — within norm</td>
            <td>N/A — both within Canadian norm</td>
          </tr>
          <tr>
            <td>Population spread (tighter is better)</td>
            <td class="normal">3,180</td>
            <td class="flag">4,707 — 48% wider</td>
            <td>Structural (Reduces vote equality)</td>
          </tr>
          <tr>
            <td>NW Calgary population excess above average</td>
            <td class="normal">2.8%</td>
            <td class="flag">11.5%</td>
            <td><strong>UCP</strong> (Packs urban NDP votes)</td>
          </tr>
          <tr>
            <td>Boundaries flagged by the commission's own chair</td>
            <td class="normal">0</td>
            <td class="flag">3</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Airdrie split (constraint minimum: 2)</td>
            <td class="normal">2 pieces</td>
            <td class="flag">4 pieces</td>
            <td><strong>UCP</strong> (Cracks urban/suburban power)</td>
          </tr>
          <tr>
            <td><strong>Pre-registered summary</strong> (&ge; 4 of 5 = outlier)</td>
            <td class="normal"><strong>0 of 5 fired</strong></td>
            <td class="flag"><strong>4 of 5 fired</strong> (anchoring test neutral — both maps within Canadian norm; remaining 4 tests all fire)</td>
            <td><strong>UCP</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>A separate finding — applied only to the minority because the minority is the map whose contested redraws are public (the majority did not publish a contested-redraw rationale list; the seven-rationale audit cannot be applied symmetrically and is reported as a single flag, not as additional rows in the structural-irregularity count) — is that <strong>five of six of the minority commissioners' published rationales fail under independent check</strong>. (A seventh redraw the audit had previously listed turned out to rest on a federal-boundary claim that cannot be located in the minority report; it has been removed rather than left as a weak claim.)</p>

    <p>The audit also tested the chair's separate, blanket assertion in Appendix C that the minority's seven contested hybrid configurations had <strong>no public support</strong> in the 1,140+ public submissions. A keyword search across the full submission archive (94% machine-parsed, 6% image-only and excluded; methodology and per-configuration evidence at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) returned a more nuanced picture than either the chair's blanket claim or its blanket dismissal: the chair was right on three of seven (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane hybrid, and the St. Albert minority alternative each lack any documented support), wrong on three of seven (Rocky Mountain House–Banff Park drew an explicit, detailed proposal from at least one Clearwater-area submission plus several aligned ones; Olds–Three-Hills–Didsbury was supported by Beiseker residents in writing; Chestermere drew multiple submissions opposing a Calgary merger that materially align with the minority's intent), and partially wrong on one (Red Deer hybrids drew a peri-Red-Deer hybrid proposal from a sitting Red Deer councillor, with directional but not configuration-exact alignment). The chair's Appendix C "no public support" sweep is therefore demonstrably overbroad — three of seven are demonstrably false — but it is not invented out of whole cloth, since three of seven do hold up. <strong>This finding cuts against the chair, not against the minority.</strong></p>

    <p><strong>On Lane 2, the majority crosses zero structural thresholds. The minority crosses every one of them by a wide margin.</strong></p>
  </section>

  <section id="section-6">
    <h2>6: How &#8220;Clean Gerrymanders&#8221; Work <a href="#section-6" class="section-link" aria-label="Link to section 6">#</a></h2>

    <div class="callout">
      <p><strong>A NOTE ON LEGAL TERMINOLOGY</strong></p>
      <p>"Gerrymandering" has no legal definition in Canadian law. The word is used throughout this report in its everyday political sense — manipulating electoral boundaries for partisan advantage. The legal tests that actually apply in Canada are different: whether boundaries provide "effective representation" under s.3 of the <em>Charter of Rights and Freedoms</em> (the constitutional standard the Supreme Court of Canada set in the 1991 <em>Saskatchewan Reference</em>), and whether the commission followed the rules of Alberta's <em>Electoral Boundaries Commission Act</em>. The audit's findings are evidence bearing on those legal questions. They are not proof of a legally-defined wrong, and this report does not describe them that way.</p>
    </div>

    <p>The cleanest single question to ask of any electoral map is this: if the province's vote split exactly evenly between the two main parties, what seat count would the map produce? This holds the electorate constant and asks the map alone what it does.</p>

    <p>To answer this, the audit generated 1,010,000 computer-simulated, mathematically neutral Alberta maps (4 independent chains &times; 252,500 steps, base seed from Cloudflare drand beacon, pre-registered at OSF before execution) using the official Elections Alberta shapefiles, holding to the exact same statutory rules and geographic boundaries the commission used. We then placed the commission's two 2026 maps into that distribution to see how normal they are.</p>

    <div class="callout">
      <p><strong>HOW THE SIMULATION WORKS</strong></p>
      <p><strong>MCMC (Markov Chain Monte Carlo)</strong> is a method for exploring a large space — here, the space of all legal Alberta maps — by taking random steps from a starting point. Each step proposes a small swap between adjacent districts; if the result stays within the statutory rules, it becomes the new starting point. After enough steps, the visited maps form a representative sample of legal plans. The simulation is seeded from the Cloudflare drand public randomness beacon to prevent any cherry-picking of starting conditions.</p>
      <p><strong>ReCom (Redistricting Compiler)</strong> is the specific algorithm used here. Each step merges two adjacent districts into one region and re-splits it randomly into two new valid districts, preserving contiguity and population balance by construction — so the algorithm never needs to reject an invalid proposal.</p>
    </div>

    <div class="callout">
      <p><strong>PRE-REGISTRATION</strong></p>
      <p>Pre-registration means writing down the exact tests, thresholds, and predicted directions before looking at any data, and locking those commitments into a public time-stamped record. The Open Science Framework (OSF) is the public repository where this audit's commitments are filed. It prevents retrofitting: if a result doesn't emerge cleanly, the threshold cannot be changed after the fact and then presented as always having been the test. All five structural tests and four partisan-fairness metrics in this audit were registered at OSF before any simulation was run.</p>
    </div>

    <p>In Alberta, the neutral answer is not 50/50. <em>Across 1,010,000 computer-simulated legal Alberta maps, the median map gives the UCP only 44.8% of the seats at 50/50 votes</em> — a typical Alberta map under neutral votes hands the NDP a small seat majority. This is counterintuitive but mechanical: rural UCP voters win their ridings by 60-40 margins (wasting many "extra" UCP votes), while urban NDP voters win their ridings by tighter 51-49 margins (wasting fewer NDP votes per win). At neutrality, NDP comes out ahead on seat efficiency.</p>

    <p>The full distribution from the canonical 1,010,000-map simulation:</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Where the map sits</th>
            <th>UCP seats at 50/50 votes</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Median Alberta map</td>
            <td class="normal">44.8% — NDP slight seat majority</td>
          </tr>
          <tr>
            <td>95th-percentile map</td>
            <td>47.1%</td>
          </tr>
          <tr>
            <td>99th-percentile map</td>
            <td>48.4%</td>
          </tr>
          <tr>
            <td><strong>Maximum across 1,010,000 maps</strong></td>
            <td class="flag"><strong>below 51.7% (fewer than 100 plans reach this value)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>A note on seat counts. The 2026 commission maps each have <strong>89</strong> districts; the audit's computer simulation runs on the <strong>87</strong>-district 2019 map (its starting substrate); the November Lunty committee will produce <strong>91</strong>. All percentages are seat <em>shares</em>, comparable across these denominators. The simulation uses the 2019 map as its starting point because the ReCom algorithm needs a legally enacted map to propose swaps from — the 2019 map is the last enacted Alberta electoral map. Using either commission proposal as the substrate would be circular: we would be measuring whether a map is extreme compared to maps derived from itself.</p>

    <p>The results — placing the three real maps in this distribution — point to a specific, surgical pattern of boundary drawing.</p>

    <h3>All four statistical measures fire simultaneously</h3>

    <p>When the official Elections Alberta shapefiles are used, the minority map is a statistical outlier on every partisan-fairness metric — not just the tipping-point one.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Map</th>
            <th>Efficiency gap</th>
            <th>Mean-median</th>
            <th><a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener" title="Declination measures the angular difference between the seats-votes curve for each party. Negative values favour the UCP; positive favour the NDP.">Declination</a></th>
            <th>Seats at 50/50</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Majority 2026</td>
            <td class="normal">+0.1% (p15)</td>
            <td>&#8722;3.6% (p2)</td>
            <td>+0.027 (p81)</td>
            <td class="normal">46.1% (p83)</td>
          </tr>
          <tr>
            <td>Minority 2026</td>
            <td class="flag"><strong>+4.0% (p94)</strong></td>
            <td class="flag"><strong>+1.0% (p99.98)</strong></td>
            <td class="flag"><strong>&#8722;0.077 (p1.2)</strong></td>
            <td class="flag"><strong>51.7% (p99.99)</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>The majority map sits comfortably inside the normal range on three of four metrics. Its mean-median sits at p2 in the NDP-favourable direction — an unusual result but pointing the wrong way to help the UCP. The majority map's close adherence to municipal boundaries places NDP-heavy urban cores into their own compact districts, where NDP votes win by efficient margins while UCP rural wins tend to be by larger margins; this mild structural NDP efficiency advantage is what shows up in the mean-median measure. The minority map is in the tail on all four, each pointing in the same partisan direction.</p>

    <h3>The 50/50 tipping point: fewer than 100 of 1,010,000 neutral maps reach it</h3>

    <p>The tipping-point metric is the most intuitive: if the province split exactly 50/50 between the two parties, how many seats does each map give the UCP?</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Map</th>
            <th>UCP seats at 50/50 votes</th>
            <th>Where it sits</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>2019 enacted</td>
            <td class="normal">46.0%</td>
            <td class="normal">83rd percentile — inside the normal range</td>
          </tr>
          <tr>
            <td><strong>Majority 2026</strong></td>
            <td class="normal"><strong>46.1%</strong></td>
            <td class="normal"><strong>83rd percentile — well within bounds</strong></td>
          </tr>
          <tr>
            <td><strong>Minority 2026</strong></td>
            <td class="flag"><strong>51.7% (46 seats)</strong></td>
            <td class="flag"><strong>99.99th percentile — fewer than 100 of 1,010,000 neutral draws reach this</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>Fewer than 100 of 1,010,000 computer-simulated neutral Alberta maps produced a <code>seats@50/50</code> value as high as the minority proposal's. Based on actual recent voting patterns, it would award the UCP 60 seats (compared to 55 in the majority proposal). The majority proposal is the kind of map a neutral procedure routinely generates. The minority proposal is the kind of map you have to specifically aim to draw.</p>

    <h3>What this means in plain language</h3>

    <p>The official shapefiles reveal a map that is statistically extreme in the same partisan direction on all four measures at once. The joint probability of a neutral drawing process producing a map this extreme across all four measures simultaneously is roughly one in 15 million (p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>, <a href="https://osf.io/6pt83" rel="noopener">pre-registered Fisher combined test</a>). That is not a rounding error or a measurement artefact — it is the same answer from four independent statistical instruments read in the same room.</p>

    <details class="audit-detail">
      <summary>What this p-value means — and what it doesn&rsquo;t</summary>
      <div class="audit-detail-body">
        <p>A p-value answers one question: if the map were drawn by a neutral process, how often would we see a result this extreme or more extreme? At p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>, the answer is about once in 14.5 million trials.</p>
        <p>This is a frequentist hypothesis test, not a measurement of intent. It does not say the commission intended to gerrymander, and it does not quantify how unfair the map is in practical terms. It says the boundary pattern is statistically inconsistent with a neutral drawing process — the same conclusion a randomized audit would reach regardless of who drew the map or why.</p>
        <p>The test was pre-registered before the data were analyzed (<a href="https://osf.io/w2s8k" rel="noopener">OSF registration w2s8k</a>). The pre-registration specifies the null hypothesis, the metrics, and the rejection threshold in advance, so the result cannot be attributed to choosing a favorable framing after seeing the numbers.</p>
      </div>
    </details>

    <div class="callout">
      <p><strong>SWING-ZONE ALLOCATION TEST (SZAT)</strong></p>
      <p>SZAT is the audit's second independent test, and it asks a different question from the simulation: not "is this map extreme overall?" but "are the specific line choices partisan-neutral?" It works by isolating only the Voting Areas where the minority's map differs from the majority's — the contested re-draws — and testing whether those particular choices, taken together, shift vote efficiency in one party's direction. Because it compares only the points of departure, it automatically controls for everything the two maps share: the same geography, population targets, and statutory rules. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Technical details and bootstrap results &rarr;</a></p>
    </div>

    <p><strong>Two questions, one answer.</strong> The 1,010,000-map simulation asks: <em>is this map extreme compared to neutral maps drawn on the same Alberta geography?</em> A second, separate test — called the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Swing-Zone Allocation Test</a> — asks a different question: <em>are the specific lines on the map partisan-neutral?</em> It works by looking only at the Voting Areas where the minority drew differently from the majority and asking whether those particular choices, taken together, shifted vote efficiency in one party's direction. Because it compares only the places where the two maps differ, it automatically controls for everything they share — the same provincial geography, the same population targets, the same statutory rules. Both questions return the same answer. That is why the one-in-15-million figure is a combined result rather than a single test: it is two independent lines of evidence converging.</p>

    <p>This explains why the minority proposal had to be such an extreme statistical outlier (p99.99) against 1,010,000 neutral simulations. In an 89-seat legislature, a two-thirds supermajority requires exactly 60 seats. You do not hit the 60-seat supermajority threshold by drawing natural, community-respecting boundaries; you have to surgically force the map to get there.</p>

    <div class="callout">
      <p><strong>WHY A SUPERMAJORITY MATTERS</strong></p>
      <p>Under Canada's Westminster parliamentary system, a simple majority (45 seats) is enough to pass routine laws and budgets. But securing a two-thirds supermajority (60 seats) grants a government near-absolute control. It allows the ruling party to effortlessly invoke "closure" to shut down debate, rewrite the rules of the legislature without opposition consent, and completely dominate all legislative committees. More importantly, it makes a Premier mathematically bulletproof to internal revolts — even if half a dozen backbenchers cross the floor, the government retains absolute control. A simple majority lets you drive the car; a 60-seat supermajority lets you rewrite the traffic laws.</p>
    </div>

    <p>By strategically diluting urban voters into surrounding rural-edge districts (the "urban hybridization" pattern identified in Lane 2), the minority proposal engineers the exact structural firewall needed to secure those 60 seats. The Lane 2 structural finding and the Lane 1 statistical finding converge on the same proposal, the same direction, and the same communities.</p>

    <h3>Confirmation from the targeted-procedure test</h3>

    <p>To be sure this isn't a quirk of the neutral simulation's known compactness preference, the audit ran a targeted hill-climbing procedure (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">Cannon et al. 2022 — cited and described in the technical report</a>) in both directions: maximising UCP seats and maximising NDP seats. Same number of steps (40,000) in each direction, same statutory constraints, same provincial geometry.</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Procedure</th>
            <th>Most-extreme value reached</th>
            <th>What it tells us</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Neutral MCMC, max produced</td>
            <td>below 51.7% UCP seats @ 50/50</td>
            <td>The natural ceiling under neutral drawing</td>
          </tr>
          <tr>
            <td>Neutral MCMC, min produced</td>
            <td>~39% UCP seats @ 50/50</td>
            <td>The natural floor under neutral drawing</td>
          </tr>
          <tr>
            <td>Targeted hill-climb, UCP-maximizing</td>
            <td class="flag"><strong>52.9%</strong></td>
            <td>What a procedure deliberately aiming for UCP advantage can reach</td>
          </tr>
          <tr>
            <td>Targeted hill-climb, NDP-maximizing</td>
            <td><strong>37.9%</strong></td>
            <td>What a procedure deliberately aiming for NDP advantage can reach (below the neutral floor)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p>The minority map's 51.7% sits closer to the targeted-UCP ceiling (52.9%) than to the neutral median (44.8%). The majority map's 46.1% sits at the neutral median. Both the 2019 enacted map and the 2026 majority fall comfortably within what neutral procedure routinely produces — different vote shares, same zone of unremarkable outcomes. The majority continues 2019 Alberta practice on the partisan-fairness axis the same way it continues 2019 practice on municipal anchoring (80.0% vs 2019's 75.2%). Two maps drawn under the same Alberta rules, by the same five commissioners, in the same room: one lands where neutral procedures routinely produce, the other lands where you have to specifically aim to land.</p>

    <p><em>That</em> is the shape of the finding, and it is also the framing a court would actually apply.</p>

    <h3>Ruling Out Alternative Explanations</h3>

    <p>When presented with a statistical outlier of this magnitude, a rigorous audit must rule out innocent explanations before attributing these patterns to deliberate design. The structural data (Lane 2) systematically dismantles the standard alternative defenses:</p>

    <ol style="margin: 0.8rem 0 0.9rem 1.4rem;">
      <li style="margin-bottom: 0.6rem;"><strong>The "Natural Political Geography" Defense:</strong> <em>("Urban voters are naturally packed; the map just reflects Alberta's geography.")</em> The 1,010,000 simulations already account for Alberta's natural geography. The simulation proves that while geography gives the UCP a baseline efficiency advantage, it naturally caps around the 83rd to 90th percentile. The minority map sits at the 99.99th percentile — an extreme outlier <em>even when compared to Alberta's naturally skewed baseline</em>.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Communities of Interest" Defense:</strong> <em>("The odd shapes were drawn to keep specific communities together.")</em> If you are trying to keep communities together, you follow municipal borders. The majority map followed existing city limits 80% of the time. The minority map followed them 72% of the time — both within the 70–85% Canadian norm. What the minority map does do is actively split the unified city of Airdrie into four separate pieces, and place three of its boundary decisions precisely in the urban-edge zones the commission chair flagged as geometrically anomalous — choices that cannot be explained by community-of-interest logic.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Population Equality" Defense:</strong> <em>("They had to draw weird boundaries to make sure every district had the exact same population.")</em> The minority map is actually much <em>worse</em> at population equality. Its Population Mean Absolute Deviation (MAD) was 4,707 — 48% wider than the majority map's 3,180 — placing it at the 99th percentile of the canonical ensemble (only 1 in 100 neutral maps produces a worse spread). It sacrificed population equality to achieve its shape.</li>
      <li style="margin-bottom: 0.6rem;"><strong>The "Incompetence or Bad Luck" Defense:</strong> <em>("They just drew a sloppy map and got unlucky with the numbers.")</em> Hitting exactly 60 seats for a supermajority while also splitting Airdrie into four pieces and placing three boundaries in the exact zones the commission's own chair flagged as anomalous requires surgical precision. The joint probability of accidentally drawing a map that hits the extreme statistical tail across four independent partisan metrics simultaneously is roughly <strong>1 in 15 million</strong> (p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup>). You cannot blunder your way into the 99.99th percentile.</li>
    </ol>

    <p>What the data shows is that the minority proposal worsened both population parity and community coherence relative to what the same five commissioners produced simultaneously under identical statutory rules. The audit does not determine what the minority commissioners intended — boundary geometry cannot reveal intent — but the structural departure from both the neutral ensemble and the majority proposal's output stands regardless of intention.</p>

    <h3>A note on the R cross-validation</h3>

    <p>An earlier version of this audit (using approximated rather than official shapefiles) cross-validated the Python ReCom ensemble against the R <code>redist</code> package's Sequential Monte Carlo sampler. That cross-check produced unstable results: across three runs with the same nominal seed, the fraction of plans reaching the old minority value (48.3% on the approximated geometry) was 5.6%, then 28%, then 58% — a sampler-convergence failure, not a discovery. The full write-up is at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>.</p>

    <p>With official Elections Alberta shapefiles, the minority map's <code>seats@50/50</code> rises to 51.7% — a value fewer than 100 of 1,010,000 neutral plans reach. The R cross-validation question becomes moot: zero plans from either sampler reach the canonical value at comparable sample sizes.</p>

    <p><strong>The asymmetry around 50/50 is more telling than the inversion itself.</strong> A precision sweep of the seat-vote curve at 0.01-percentage-point resolution finds the minority map keeps the UCP at or above the 45-seat legislative-majority threshold down to a UCP provincial vote share of about <strong>49.7%</strong>. That is technically a vote-seat inversion — the UCP would form government on the minority map while losing the popular vote by 0.3 percentage points — but 0.3 points is well within ordinary polling noise, so on its own this is not a dramatic finding. What <em>is</em> dramatic is the contrast: on the <strong>majority</strong> map, the UCP would need to <em>win</em> the popular vote by about 4 percentage points to reach the same 45-seat threshold. Both maps face the same Alberta geography and the same statutory rules; the gap between them — 0.3pp vs +4pp — is structural difference, not noise.</p>

    <p>This is the structural-bias finding the audit holds with confidence. It is geometry-only; it does not depend on any election result; it does not move when polls do.</p>

    <p><strong>One caveat the audit takes seriously.</strong> A real electorate is not a uniform 50/50. Voters can swamp any map's structural lean with enough swing — a particularly upset or inspired electorate will tip the result regardless of how the boundaries are drawn. The 50/50 test isolates <em>the map's contribution to the outcome</em>, not the outcome itself. What it shows is what the map does when the electorate doesn't decide for it.</p>

    <h3>The verdict</h3>

    <p>The audit's central finding is geometric. <strong>Lane 2 — the structural-irregularity scorecard — is the foundation; Lane 1 is the proof that the geometry is doing partisan work.</strong></p>

    <p>The chart below puts both lanes on a single picture. The horizontal axis is Lane 1 (the partisan-fairness efficiency gap, where further right means more UCP-favoured); the vertical axis is Lane 2 (the count of structural-fairness tests the proposal fails, out of five, where higher means more structural problems).</p>

    <figure style="margin:1.2rem 0;text-align:center;">
      <img src="images/verdict_quadrant.svg" alt="Scatter plot with efficiency gap on the horizontal axis and count of structural tests failed on the vertical axis. The 2019 enacted map and the majority 2026 map cluster in the safe lower-left corner. The minority 2026 map appears in the upper-right outlier region." style="max-width: 100%; border: 1px solid #ddd; border-radius: 4px; background: #fff; padding: 0.5rem;" width="474" height="351" loading="lazy">
      <figcaption style="font-size: 0.82rem; color: #666; margin-top: 0.4rem;">The two ways of measuring the two commission proposals, plotted together. Left-to-right: how skewed the proposal looks on the partisan-fairness number — the further right, the more it favours the UCP. Bottom-to-top: how many of five structural-fairness tests the proposal fails — the higher, the worse. The 2019 enacted map sits in the safe corner: low on both. The majority 2026 proposal stays flat at zero structural problems and near-zero partisan skew (+0.1%). The minority 2026 proposal is a structural outlier on all five tests; its efficiency gap (+4.0%) sits just below the Alberta threshold line.</figcaption>
    </figure>

    <p>The same verdict in plain summary form, leading with the structural finding because that is what the cross-validated evidence supports most strongly:</p>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th></th>
            <th>Lane 2: Structure (geometry-only, no votes)</th>
            <th>Lane 1: Numbers (vote-dependent)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Majority 2026</strong></td>
            <td class="normal">clean — crosses <em>no</em> structural threshold</td>
            <td class="normal">inside the normal range on every metric (<code>seats@50/50</code> 46.1% — p83; efficiency gap +0.1%)</td>
          </tr>
          <tr>
            <td><strong>Minority 2026</strong></td>
            <td class="flag"><strong>crosses 4 of 5 structural thresholds</strong> by a wide margin (anchoring neutral — both maps within Canadian norm)</td>
            <td class="flag">statistical outlier on all four partisan-fairness measures simultaneously — <code>seats@50/50</code> 51.7% (p99.99, fewer than 100 of 1,010,000 reach it); efficiency gap +4.0% (p94); all four pre-registered; Fisher combined p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup></td>
          </tr>
        </tbody>
      </table>
    </div>

    <details class="audit-detail">
      <summary>Why Lane 2 carries the case — technical detail</summary>
      <p style="margin:0.7rem 0 0;">The audit pre-registered five structural-irregularity tests on April 24, 2026 before the final simulation results were compiled. The minority crosses every one; the majority crosses none. Those measurements are geometric — they don't depend on any statistical sampler or any vote attribution. Lane 1 (the partisan-fairness numbers) corroborates Lane 2 strongly under canonical official shapefiles: the minority is a statistical outlier on all four pre-registered metrics simultaneously, with a joint neutral-null probability of p&nbsp;=&nbsp;6.87&times;10<sup>&#8722;8</sup> (pre-registered Fisher combined test — a method that combines four independent test results into a single probability by multiplying their individual tail probabilities; the combined figure is far smaller than any single test's because all four point the same direction; OSF <a href="https://osf.io/6pt83" rel="noopener">6pt83</a>). The question of whether Lane 2's unusual geometry is the specific <em>mechanism</em> behind the Lane 1 numbers was tested and the answer is no — see <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>. The Swing-Zone Allocation Test shows the contested boundary choices are partisan-skewed, but the tested question was whether the boundary shapes themselves — the lasso corridor, the park extension — are the direct cause of the seat swing; they are not. The seat effect comes from how redrawn Voting Area assignments shift vote efficiency across districts, not from the shapes per se. Both lanes flag the minority map; they reach that conclusion through independent instruments. Lane 2 is the central finding. Lane 1 corroborates without carrying.</p>
    </details>
  </section>

  <section id="section-7">
    <h2>7: The Lunty Committee <a href="#section-7" class="section-link" aria-label="Link to section 7">#</a></h2>

    <div class="callout" style="background:#F5F5F5; border-left-color:#888; font-size:0.95rem;">
      <p style="margin:0;"><strong>CONTEXT</strong> — This section describes the process that replaced the commission and the legal framework that applies to it. It is not part of the statistical findings. The findings are in §3–§6 above.</p>
    </div>

    <p>Neither commission map is in force. The government set both aside in April 2026 and referred redistricting to a Special Select Committee of five MLAs — three UCP, two NDP — chaired by Brandon Lunty (UCP, Leduc-Beaumont). The committee itself does not draw the map; it oversees a separate advisory panel of five appointees (government-appointed chair, two UCP nominees, two NDP nominees) tasked with producing a 91-seat boundary proposal. The committee must deliver its report to the Legislature by November 2, 2026. Unlike the original commission, neither the committee nor the advisory panel is required to hold public hearings; the panel draws on submissions the original commission gathered. The all-party committee sought a retired or sitting judge to chair the advisory panel; Alberta's acting chief justice declined to nominate one. When the committee's map is released, this audit will apply the same methodology to evaluate it.</p>

    <h3>Why the Committee Is Anomalous</h3>

    <p>Canadian redistricting practice has, since the 1960s, settled on a single model: an independent commission, insulated from government direction, produces boundary recommendations; the legislature may debate them but cannot easily override them without a formal legislative vote. Alberta's statutory process under the <em>Electoral Boundaries Commission Act</em> follows this template — but with one structural difference from most provinces: Alberta's commission report has no automatic legal effect. Under the Act, a separate Electoral Districts Act must be passed by the legislature to give any commission map force of law. That means the government of the day controls not only whether the commission map is debated, but whether it ever becomes law at all. Other Canadian jurisdictions take the opposite default: the commission's recommendations take effect unless the legislature affirmatively votes to override them.</p>

    <p>What the government did in April 2026 has no recorded precedent in post-Confederation redistricting: it allowed a completed, published commission process to conclude — both majority and minority reports filed — and then referred the redistricting task to a five-member committee of MLAs whose majority (three of five) is held by the governing party, without bringing either commission report to a vote. The Lunty committee is not a commission. It has no statutory independence from the government's legislative direction. Its three-member UCP majority mirrors the government's control of the legislature. No other Canadian province has transferred redistricting authority, mid-cycle, to a government-controlled legislative committee after an independent commission had completed its work.</p>

    <h3>The Constitutional Framework</h3>

    <p>Section 3 of the <em>Charter of Rights and Freedoms</em> — "Every citizen of Canada has the right to vote in an election of members of the House of Commons or of a legislative assembly" — has been interpreted by the Supreme Court of Canada to guarantee not merely the act of casting a ballot but <em>effective representation</em>. The leading authority is <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em> [1991] 2 SCR 158, in which McLachlin J. (as she then was) wrote for the majority that the purpose of s.3 "is not equality of voting power per se, but the right to effective representation." Population parity is the primary consideration; departures are permitted when justified by community of interest, geography, history, or minority-representation objectives.</p>

    <p>The Saskatchewan framework does not categorically prohibit partisan considerations in redistricting. What it establishes is that boundary maps must, on the whole, provide effective representation to voters — and that systematic impairment of one identifiable group's ability to elect proportionate representation is the pattern that s.3 challenges target. The audit's statistical and structural findings — the minority map's position at the 99.99th percentile of 1,010,000 neutral draws, its crossing of all five structural thresholds, the identified communities affected — are the evidentiary record a s.3 applicant would need to assemble. Whether that record meets the constitutional threshold is a legal question this audit does not decide; the audit reports the measurement.</p>

    <p>The committee's legality as a process is a separate question. Alberta's <em>Electoral Boundaries Commission Act</em> does not expressly prohibit the legislature from constituting a parallel redistricting body, because the Act contemplates that the legislature will enact the final boundaries through ordinary legislation regardless. Whether the committee process, if it produces a map with the structural and statistical profile of the minority proposal, could survive a s.3 Charter challenge turns on whether effective representation is achievable under the resulting boundaries — the same test that would apply to any commission-produced map.</p>

    <h3>The Quebec Contrast</h3>

    <p>Quebec offers the comparison most relevant to Alberta's situation. Quebec's Commission de la représentation électorale (CRE) is a permanent, independent electoral boundaries body, not an ad hoc commission constituted per redistribution cycle. The CRE operates continuously and cannot be dissolved or bypassed by cabinet action. Under Quebec's <em>Loi électorale</em>, the National Assembly must adopt the CRE's recommendations unless it votes to deviate — and deviations require a two-thirds majority of all members of the Assembly, not a bare legislative majority. The practical effect is that a governing party cannot, acting alone with its own majority, substitute its preferred map for the commission's. Cross-party agreement is constitutionally required to override the independent body's judgment.</p>

    <p>Quebec's model emerged partly from lessons about what happens when redistricting is not insulated from partisan control. The contrast with Alberta's current process — where a majority-controlled committee has replaced the commission's work before the legislature has voted on either commission report — illustrates the structural difference between redistricting systems that assume partisan pressure and design against it, versus systems where that pressure has a clearer path to the outcome.</p>

    <p>The audit will apply the same tests to the Lunty committee's map when it is released. The constitutional and comparative observations above are contextual; the methodology does not change.</p>
  </section>

  <section id="section-8">
    <h2>8: Suggestions <a href="#section-8" class="section-link" aria-label="Link to section 8">#</a></h2>

    <p>This audit ran into two data problems that have nothing to do with the commission and everything to do with how Alberta's electoral system is designed. Both are fixable.</p>

    <p><strong>About half of all Alberta votes now arrive before election day</strong> — advance polls, mobile polls, special ballots. Elections Alberta reports these results as totals for each electoral division, not by specific Voting Area. That means roughly 395,000 NDP and UCP votes cast in 2023 cannot be pinned to any neighbourhood on a map. They are counted; they just can't be located. Every advance voter is checked against a voters list before receiving their ballot, and that list links each voter to their specific Voting Area. Publishing VA-level advance-vote totals would not require any change to the voting process — only to what EA reports.</p>

    <p>This affects the commissioners too, not just outside analysts. When a commission decides whether to keep Airdrie whole or split it, whether a corridor between two communities makes sense, whether a proposed boundary divides a natural constituency — those are judgments that depend on knowing where voters live. Commissioners work from the same published dataset as everyone else. Half the geographic signal about the communities they are drawing boundaries around is missing for them as well.</p>

    <p>There is at least one community in northern Alberta where this gap is total. In the northern part of the Lesser Slave Lake <button class="ed-trigger" data-ed-name="Lesser Slave Lake">show ↗</button> division, there is a Voting Area covering 4,832 km&#178; — larger than Prince Edward Island — where every single vote in 2023 was cast through Elections Alberta's mobile polling team. Those 844 residents' choices are counted in the divisional total but cannot be pinned to any location on a map. That community is entirely invisible in the published election results.</p>

    <p>When the commission initially considered eliminating the Lesser Slave Lake division and merging it into a larger riding, it was working without geographic vote data from those communities. The commission eventually preserved the division — after 80+ public submissions, many from the Indigenous communities in the northern part of the riding — invoking a provincial law that allows ridings with First Nations and M&#233;tis communities to have smaller populations than the provincial average. They got there. But the data they were working with didn't show them who was voting in the communities they were deciding to protect.</p>

    <div class="callout">
      <p><strong>SECTION 15(2) EBCA</strong></p>
      <p>Section 15(2) of Alberta's <em>Electoral Boundaries Commission Act</em> is a discretionary provision that allows commissions to protect undersize ridings — those more than 25% below the provincial population average — when the riding meets at least three of five specific criteria: (a) geographic area exceeding 20,000 km², (b) distance more than 150 km from the Legislature Building by most direct highway route, (c) absence of any town with more than 8,000 residents, (d) presence of an Indian reserve or a Métis settlement, and (e) whether the riding is coterminous with a boundary of the Province of Alberta. The provision is not automatic; the commission must judge whether the criteria are met. Lesser Slave Lake independently meets four of the five.</p>
    </div>

    <p>The interim rationale for eliminating the riding was population: at roughly 27,000 residents, Lesser Slave Lake sits about 45% below the provincial average, approaching the legal floor. That reads as a straightforward application of the rules. It isn't. Alberta law gives commissions explicit discretion to protect undersize ridings when at least three of five specific criteria apply — and Lesser Slave Lake meets four of them independently. Its area is 69,566 km² (criterion a — threshold 20,000 km²). Its nearest boundary is more than 150 km from the Legislature by highway (criterion b). No town in the riding has a population over 8,000 (criterion c). And the riding contains fourteen Indian reserves and M&#233;tis settlements whose communities share a common northern geography, a common dependence on mobile polling to vote at all, and a collective interest in having a representative primarily accountable to northern Alberta (criterion d). Under the proposed Mackenzie merger, that collective voice would have been permanently absorbed into a riding where the other party wins by more than two to one — not because those communities changed, but because the lines around them did. Each of those four criteria is an objective fact about the riding's geography, not a judgment call. Together they describe a constituency the provision was written to protect: remote, large, sparsely populated, and containing communities whose representation interest cannot be read from raw population numbers. You need three to qualify; Lesser Slave Lake has four. Treating the population shortfall as if it compelled elimination misreads the statute. The commission's reversal was the correct application of the law, not a concession to political pressure.</p>

    <p>Here is the other side of that story: while the Indigenous communities in Lesser Slave Lake were fighting to be counted, the dissenting commissioners proposed protecting a different riding by drawing its boundary through Banff National Park, where no one lives. The commission's own chair called that "a bad faith effort" to claim the legal protection. That phrase is in the commission's official final report. The protection designed for remote communities with Indigenous populations was used, in the minority's map, to defend a boundary through uninhabited wilderness. The communities it was designed to help had to fight for it through public submissions. The Lunty committee will face the same §&#x2009;15(2) decision in November — with no statutory requirement to hold public hearings, and no guarantee that the 80 submissions that reversed the commission's interim position will carry the same weight a second time.</p>

    <p><strong>Alberta should wait for the 2026 census before drawing the next map.</strong> Canada counts its population every ten years. The 2026 census enumeration happens in spring 2026; Statistics Canada releases usable sub-provincial data roughly two years later, in 2027 or 2028. The commission that drew the maps assessed in this audit had to use the 2021 census — already four years old when the maps were drawn, and potentially fourteen years old by the time those boundaries retire. Fast-growing cities like Airdrie and Chestermere will change by 40% or more over that window. Rural communities will shrink. The map will be wrong from the day it is used. A straightforward change to the <em>Electoral Boundaries Commission Act</em> could require that any new commission be appointed only after Statistics Canada releases the most current dissemination-area data from the preceding census. The result: maps that reflect where Albertans actually live, not where they lived a decade ago.</p>

    <p>The Lunty committee is operating under the existing statute, which sets no census-timing requirement, and cannot unilaterally delay past its November 2026 deadline. This recommendation applies to a future amendment to the <em>Electoral Boundaries Commission Act</em>, not to the current process. The tension is real: a committee required to deliver a map by November is working from data that will already be five years old — naming that constraint is more useful than pretending it does not exist.</p>

    <p>Neither of these is a finding about the current commission's maps. They are observations about a system that makes accurate electoral analysis harder than it needs to be. They are offered here as practical suggestions, not conclusions. Both are genuinely fixable, and fixing them would make every future commission — and every future audit — work from better ground.</p>
  </section>

  <section id="retractions">
    <h2>9: Retractions and Corrections <a href="#retractions" class="section-link" aria-label="Link to retractions">#</a></h2>

    <div class="callout warning">
      <p><strong>RETRACTION CONDITIONS</strong></p>
      <p>Every finding is pre-committed to a specific falsification condition. If any condition below materialises, the finding it names is retracted publicly within 30 days. The overall directional conclusion — that the minority map sits outside the neutral range on multiple independent tests — is retracted only if at least three of the five tests fail.</p>

      <div style="margin: 0.8rem 0 0; border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>Condition 1 — A counter-map exists</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: #555;"><em>What gets retracted:</em> The structural finding that the Airdrie four-way split and the three chair-flagged boundaries cannot be explained by the minority's stated community-of-interest rationale.</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">Condition: someone produces a legal Alberta map that satisfies the minority's own stated reasons — Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park — and anchors on municipal lines at majority-comparable rates. Open challenge at <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14" rel="noopener">Issue #14</a>.</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>Condition 2 — The Neighbour-Drain pre-registered pass is reversed</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: #555;"><em>What gets retracted:</em> The Section 3 table entry recording the minority map as a pre-registered PASS on the neighbour-drain adjacency test.</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">Condition: the v2 continuous drain score falls in the extreme upper tail (p &lt; 0.05) of random permutations across the fixed contiguity graph, meaning the pass was a measurement artefact of the v1 binary scoring method rather than a genuine null result.</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>Condition 3 — A pre-2026 commission document surfaces</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: #555;"><em>What gets retracted:</em> The inference that the minority's boundary choices were drafting decisions rather than responses to documented community submissions.</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">Condition: an internal commission document dated before the minority's final boundary choices shows those choices were explicitly driven by community submissions the audit has not seen — not by the six published sub-rationales the audit tested.</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>Condition 4 — The 2027 election result contradicts the simulation</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: #555;"><em>What gets retracted:</em> The Lane 1 finding — that the minority map's seats@50/50 score sits at the 99.99th percentile of 1,010,000 neutral draws.</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">Condition: if the 2027 provincial election is fought on either commission map and the actual partisan seat split contradicts the directional projection from 2023 votes, the Lane 1 percentile findings are revisited against actual results.</p>
      </div>

      <div style="border-top: 1px solid rgba(180,120,0,0.25); padding-top: 0.7rem;">
        <p style="margin: 0 0 0.2rem;"><strong>Condition 5 — An Alberta court distinguishes the Quebec SCC ruling</strong></p>
        <p style="margin: 0 0 0.3rem; font-size: 0.92rem; color: #555;"><em>What gets retracted:</em> The Section 7 procedural argument that the April 16 motion to replace the commission with the Lunty committee sits in the same constitutional class as Quebec's 2024 redistricting freeze.</p>
        <p style="margin: 0 0 0.7rem; font-size: 0.93rem;">Background: on April 22, 2026 — six days after Alberta's April 16 motion — the Supreme Court of Canada upheld, 7–2 and from the bench, a Quebec Court of Appeal ruling that the Legault government's legislative freeze on its redistricting commission violated the Charter's s.3 democratic-representation guarantee. Condition: a court reviewing the Alberta motion finds it constitutionally distinct — for example, because reassigning the work to an MLA committee differs structurally from a legislative freeze, or because Alberta's effective-representation analysis under s.3 comes out differently than Quebec's.</p>
      </div>
    </div>

    <div class="callout warning">
      <p><strong>DOCUMENTED CORRECTIONS (canonical recomputation, 2026-05-11)</strong></p>
      <p>The following early finding did not survive reanalysis against official Elections Alberta shapefiles (received 2026-05-06). It is retained here per the audit's pre-committed policy of never deleting failed findings.</p>
      <p><strong>Municipal anchoring (retracted).</strong> Early analysis using provisional map boundaries showed the minority map anchored to municipal lines only 15% of the time — 4.9&times; below the 70–85% Canadian norm. This figure was an artefact of the provisional (DPG-era) boundary reconstructions. On official Elections Alberta canonical shapefiles, both maps anchor within the Canadian norm: majority 80%, minority 72%. The municipal-anchoring <em>divergence</em> between the two maps is not a signal that survives canonical recomputation. The three boundary anomalies flagged by the commission chair (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) remain and are not affected by this correction.</p>
    </div>
  </section>

  <section id="references">
    <h2>10: References &amp; Methodology <a href="#references" class="section-link" aria-label="Link to references">#</a></h2>

    <p>The underlying methodology draws on established political science, statistics, and legal literature. Full citations follow American Political Science Association (APSA) style; court cases follow Canadian legal convention. The complete reference list appears in the <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">technical report</a>. Key sources are listed here.</p>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: #333;">Academic literature</h3>
    <ul style="margin: 0 0 1rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><strong>Alberta Electoral Boundaries Commission. 2026.</strong> <em>2025–26 Electoral Boundaries Commission Final Report (Majority and Minority)</em>. Government of Alberta.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Chen, Jowei, and Jonathan Rodden. 2013.</strong> "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." <em>Quarterly Journal of Political Science</em> 8(3): 239–269.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Courtney, John C. 2001.</strong> <em>Commissioned Ridings: Designing Canada's Electoral Districts</em>. Montreal and Kingston: McGill-Queen's University Press.</li>
      <li style="margin-bottom: 0.5rem;"><strong>DeFord, Daryl, Moon Duchin, and Justin Solomon. 2021.</strong> "Recombination: A Family of Markov Chains for Redistricting." <em>Harvard Data Science Review</em> 3(1). (The ReCom algorithm used to generate the 1,010,000-map ensemble.)</li>
      <li style="margin-bottom: 0.5rem;"><strong>Gelman, Andrew, and Gary King. 1994.</strong> "A Unified Method of Evaluating Electoral Systems and Redistricting Plans." <em>American Journal of Political Science</em> 38(2): 514–554.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Katz, Jonathan N., Gary King, and Elizabeth Rosenblatt. 2020.</strong> "Theoretical Foundations and Empirical Evaluations of Partisan Fairness in District-Based Democracies." <em>American Political Science Review</em> 114(1): 164–178.</li>
      <li style="margin-bottom: 0.5rem;"><strong>Pal, Michael. 2015.</strong> "The Fractured Right to Vote." <em>McGill Law Journal</em> 61(2): 231–274. (Canadian constitutional framework for electoral boundaries.)</li>
      <li style="margin-bottom: 0.5rem;"><strong>Stephanopoulos, Nicholas O., and Eric M. McGhee. 2014.</strong> "Partisan Gerrymandering and the Efficiency Gap." <em>University of Chicago Law Review</em> 82(2): 831–900. (Source of the efficiency gap measure used throughout.)</li>
    </ul>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: #333;">Court cases</h3>
    <ul style="margin: 0 0 1rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em>, [1991] 2 SCR 158. (The leading Supreme Court of Canada authority on the constitutional standard for electoral boundary drawing.)</li>
      <li style="margin-bottom: 0.5rem;"><em>Figueroa v. Canada (Attorney General)</em>, [2003] 1 SCR 912.</li>
      <li style="margin-bottom: 0.5rem;"><em>Raîche v. Canada (Attorney General)</em>, 2004 FC 679.</li>
      <li style="margin-bottom: 0.5rem;"><em>Rucho v. Common Cause</em>, 139 S. Ct. 2484 (2019). (U.S. Supreme Court; establishes the non-justiciability of partisan gerrymandering claims in federal courts — context for why Canada's s.3 effective-representation standard differs.)</li>
    </ul>

    <h3 style="margin: 1.2rem 0 0.5rem; font-size: 1rem; color: #333;">Statutes</h3>
    <ul style="margin: 0 0 0.5rem 1.4rem; line-height: 1.7;">
      <li style="margin-bottom: 0.5rem;"><em>Electoral Boundaries Commission Act</em>, RSA 2000, c E-3.</li>
    </ul>
  </section>

  <section id="resources">
    <h2>11: Technical <a href="#resources" class="section-link" aria-label="Link to technical">#</a></h2>

    <ul class="links-list">
      <li>
        <span class="tag">Plain Language</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/public/report_public.pdf">Full public report</a> &mdash; Long-form, with maps, for general readers
      </li>
      <li>
        <span class="tag">Summary</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/docs/FINDINGS_BRIEF.md">Summary of findings</a> &mdash; Plain-language overview, explains every concept from scratch
      </li>
      <li>
        <span class="tag">Academic</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md">Technical report</a> &mdash; Full methods and citations for researchers
      </li>
      <li>
        <span class="tag">Notebook</span>
        <a href="https://colab.research.google.com/github/Ixby/alberta-electoral-boundaries-audit/blob/master/notebooks/alberta_audit_explorer.ipynb" rel="noopener">Interactive notebook</a> &mdash; Run the charts yourself in your browser, no install needed
      </li>
      <li>
        <span class="tag">Code</span>
        <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit" rel="noopener">github.com/Ixby/alberta-electoral-boundaries-audit</a>
      </li>
    </ul>
  </section>

  <section>
    <h2>About me</h2>
    <p style="font-size:0.9rem; color:#444;">
      I'm a student at Mount Royal University. I did this research on my own &mdash; it was not assigned as coursework and the university did not commission it. My views are my own and do not represent the university. I have no connection to Elections Alberta, the commission, or any political party.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      I have supported parties on all sides of the political spectrum depending on the election. I'm telling you that because my political history could affect how I look at this issue. The main protection against that is the method: I tested both maps the same way, wrote down my predictions before looking at the results, and put everything online so anyone can check my work. I paid for this research myself. If you find something I got wrong, I genuinely want to know.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      Pre-registration records (written before results were examined): <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted:#289,469, AsPredicted:#289,451.
    </p>
    <p style="font-size:0.9rem; color:#444;">
      Questions or corrections: <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a>
    </p>
  </section>

</main><!-- /.container -->

<a href="#top" id="back-top" aria-label="Back to top">↑</a>

<div id="site-copyright" aria-label="Creative Commons BY-NC-SA 4.0">
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="license noopener" title="Creative Commons Attribution-NonCommercial-ShareAlike 4.0">
    <img src="https://licensebuttons.net/l/by-nc-sa/4.0/80x15.png" alt="CC BY-NC-SA 4.0" width="80" height="15">
  </a>
</div>

<!-- Figure lightbox -->
<div id="fig-lightbox" role="dialog" aria-modal="true" aria-label="Figure enlarged view" tabindex="-1">
  <img id="fig-lightbox-img" alt="">
</div>

<!-- Participation prompt -->
{#if showParticipation}
<div id="participation-overlay" role="dialog" aria-modal="true" aria-labelledby="part-heading">
  <div id="participation-card">
    <h2 id="part-heading">May we connect anonymous usage data?</h2>
    <p>This audit is ongoing research. Connecting anonymous data helps us understand how people navigate the tool and where the design can improve. No personal information is collected — all inputs are pre-anonymized in your browser before anything is transmitted.</p>
    {#if dntActive}
    <p class="part-dnt">Your browser has Do Not Track enabled. No is pre-selected on your behalf. You can change your answer.</p>
    {/if}
    <div class="part-actions">
      <button class="part-btn part-no" onclick={() => { setParticipation(false); showParticipation = false; }}>No thanks</button>
      <button class="part-btn part-yes" onclick={() => { setParticipation(true); showParticipation = false; }}>Yes, connect</button>
    </div>
    <p class="part-policy"><a href="{base}/privacy-policy.md" target="_blank" rel="noopener noreferrer">Privacy policy</a></p>
  </div>
</div>
{/if}

<!-- Zoom overlay -->
<div id="zoom-overlay" aria-modal="true" role="dialog" aria-label="Map zoom viewer" style="display:none;">
  <button id="zoom-close" title="Close (Esc)">&times;</button>
  <div id="hud">
  <div id="top-bar">
    <div class="tb-group">
      <button class="tb-btn" data-map="minority">Minority</button>
      <button class="tb-btn" data-map="majority">Majority</button>
      <button class="tb-btn tb-map-primary" data-map="2019">Current</button>
    </div>
    <div class="tb-sep"></div>
    <div class="tb-group">
      <button class="tb-btn" data-layer="eg" title="Efficiency-gap contribution per district">Wasted</button>
      <button class="tb-btn" data-layer="ed-fill" title="Colour each district by partisan outcome (UCP blue / NDP orange)">Partisan</button>
      <button class="tb-btn tb-layer-on" data-layer="ed-lines">Borders</button>
    </div>
    <div class="tb-sep"></div>
    <button class="tb-btn" data-anomaly="airdrie" title="All 7 configurations flagged by commission chair Justice Miller — switches to minority map automatically">Flagged</button>
    <div class="tb-sep"></div>
    <button class="tb-btn tb-pin-btn" data-layer="lock" title="Pin Map — prevent auto-pan on district click" aria-label="Pin Map">
      <svg class="pin-icon" viewBox="0 0 16 16" width="14" height="14" fill="currentColor" aria-hidden="true">
        <path d="M9.828.722a.5.5 0 0 1 .354.146l4.95 4.95a.5.5 0 0 1 0 .707c-.48.48-1.072.588-1.503.588-.177 0-.335-.018-.46-.039l-3.134 3.134a5.9 5.9 0 0 1 .16 1.013c.046.702-.032 1.687-.72 2.375a.5.5 0 0 1-.707 0l-2.829-2.828-3.182 3.182a.5.5 0 0 1-.707-.707l3.182-3.182-2.828-2.829a.5.5 0 0 1 0-.707c.688-.688 1.673-.767 2.375-.72a5.9 5.9 0 0 1 1.013.16l3.134-3.133a3 3 0 0 1-.04-.461c0-.43.108-1.022.589-1.503a.5.5 0 0 1 .353-.146"/>
      </svg>
    </button>
    <div class="tb-sep"></div>
    <div id="tb-search-wrap">
      <input id="tb-search" type="search" placeholder="Find district…" autocomplete="off" spellcheck="false">
      <ul id="tb-search-results"></ul>
    </div>
    <div class="tb-sep"></div>
    <div id="ec-zoom-section">
      <span id="zoom-pct">100%</span>
      <input type="range" id="zoom-slider" min="25" max="3000" step="5" value="100" aria-label="Map zoom">
    </div>
    <button id="ec-close" class="tb-btn tb-close-btn" title="Clear selection">&times;</button>
    <div class="tb-sep"></div>
    <div id="tb-share-wrap">
      <button class="tb-btn" id="tb-share-btn" onclick={toggleSharePanel} title="Share or load a map configuration">Share</button>
      {#if showSharePanel}
      <div id="share-panel" role="dialog" aria-label="Share map configuration">
        <div class="share-section">
          <div class="share-label">Share this configuration</div>
          <div class="share-code-row">
            <span class="share-code">{shareCode}</span>
            <button class="share-action-btn" onclick={copyCode}>{copyLabel}</button>
          </div>
          <div class="share-hint">Type this code into any browser running the audit to load this configuration. The code is never placed in a URL.</div>
        </div>
        <div class="share-divider"></div>
        <div class="share-section">
          <div class="share-label">Load a configuration</div>
          <div class="share-load-row">
            <input
              class="share-load-input"
              type="text"
              placeholder="alpine-eagle-banff"
              bind:value={loadInput}
              onkeydown={(e) => { if (e.key === 'Enter') loadShare(); }}
              spellcheck="false"
              autocomplete="off"
            />
            <button class="share-action-btn" onclick={loadShare}>Load</button>
          </div>
          {#if loadError}<div class="share-error">{loadError}</div>{/if}
        </div>
      </div>
      {/if}
    </div>
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
    </div>
  </div>
  </div><!-- /#hud -->
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
        <div class="skel-phrase">{skelPhrase}</div>
      </div>
    </div>
    <object id="zoom-obj" type="image/svg+xml" data="images/cover_art_2019_hires.svg"
      title="Alberta electoral district map — full resolution"></object>
  </div>
  <div id="ed-tooltip"></div>
  <div id="map-attribution">
    <span id="map-ea-credit">Map data: <a href="https://www.elections.ab.ca/resources/maps/" target="_blank" rel="noopener">Elections Alberta</a></span>
    <a id="map-cc-badge" href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="license noopener" title="Text content: CC BY-NC-SA 4.0">
      <img src="https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png" alt="Creative Commons BY-NC-SA 4.0" width="80" height="15">
    </a>
    <span id="map-cc-owner">2026 Will Conner</span>
  </div>
</div>

<footer>
  <div class="container">
    Alberta Electoral Boundary Audit &mdash; May 2026<br>
    &copy; Will Conner 2026 &mdash;
    Text: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a> &mdash;
    Code: <a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU GPL v3.0</a><br>
    <a href="https://ixby.github.io">ixby.github.io</a> &mdash;
    <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit">github.com/Ixby/alberta-electoral-boundaries-audit</a>
  </div>
</footer>

<!-- Map onboarding modal — shown once per session via sessionStorage; logic in mapEngine.ts -->
<div id="map-intro-modal" style="display:none;">
  <div id="map-intro-inner">
    <h3>How to use the map</h3>
    <p style="margin:0 0 0.7rem; font-size:0.93rem;"><strong>Start here:</strong> click <strong>Minority → Majority</strong> to watch the boundaries shift while the voters stay still. The <strong>Partisan</strong> colours show which party holds each district.</p>
    <ul>
      <li><strong>Minority / Majority / 2019</strong> &mdash; switch which commission map you&rsquo;re viewing as the primary layer</li>
      <li><strong>Partisan</strong> &mdash; colour districts by partisan outcome (UCP blue, NDP orange); neutral grey when off</li>
      <li><strong>Vote %</strong> &mdash; show 2023 vote results at polling-area granularity underneath</li>
      <li><strong>Borders</strong> &mdash; show or hide district boundary edges</li>
      <li><strong>Pin</strong> (pin icon, turns red when active) &mdash; prevent the map from auto-panning when you click a district</li>
      <li><strong>Find district</strong> &mdash; type any district name to jump to it</li>
      <li><strong>Wasted</strong> &mdash; shade each district by its efficiency-gap contribution (wasted votes): blue = UCP-favoured, orange = NDP-favoured</li>
    </ul>
    <p><strong>Try this:</strong> In §4 below, click <em>Show flagged districts on map</em> to highlight the Airdrie split and NW Calgary zone, then click any highlighted district to see its vote data and compare across all three maps.</p>
    <button id="map-intro-close">Got it</button>
  </div>
</div>

<style>
  :global {
:root {
  --bg:              #f9f7f2;
  --bg-alt:          #f5f5f5;
  --text:            #1a1a1a;
  --text-muted:      #555;
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
}
:root[data-theme="dark"] {
  --bg:            #1e1f26;
  --bg-alt:        #26272f;
  --text:          #dde2ed;
  --text-muted:    #8890a4;
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

    .cover-note {
      font-size: 0.78rem;
      opacity: 0.62;
      margin-top: 0.85rem;
      line-height: 1.5;
      max-width: 380px;
    }

    nav {
      background: #243b53;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .nav-inner {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 0.75rem;
      overflow-x: auto;
      white-space: nowrap;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }
    .nav-inner::-webkit-scrollbar { display: none; }

    nav a {
      color: #a8c7e8;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      font-size: 0.82rem;
      min-height: 2.6rem;
      padding: 0 0.55rem;
      white-space: nowrap;
    }
    nav a:hover { color: #fff; text-decoration: underline; }
    nav a.active { color: #fff; border-bottom: 2px solid rgba(255,255,255,0.6); }
    nav a.nav-home { color: rgba(255,255,255,0.45); padding-right: 0.8rem; margin-right: 0.4rem; border-right: 1px solid rgba(255,255,255,0.15); text-decoration: none; }
    nav a.nav-home:hover { color: #fff; text-decoration: none; }
    .nav-theme-btn {
      display: inline-flex; align-items: center; justify-content: center;
      background: none; border: none; cursor: pointer;
      color: #F5C518; padding: 0 0.55rem;
      margin-left: 0.4rem; padding-left: 0.8rem;
      border-left: 1px solid rgba(255,255,255,0.15);
      min-height: 2.6rem;
      transition: color 0.15s;
    }
    .nav-theme-btn:hover { color: #fff; }
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
      margin-left: 0.4em;
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
    /* Defer layout of sections far below the fold — browser skips paint until near viewport */
    #section-5, #section-6, #section-7, #section-8,
    #retractions, #references, #resources {
      content-visibility: auto;
      contain-intrinsic-size: auto 1px auto 600px;
    }

    h2 {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 0.9rem;
      color: var(--heading);
    }

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
      text-align: left;
    }

    td {
      padding: 0.5rem 0.8rem;
      border-top: 1px solid var(--border-subtle);
      vertical-align: top;
    }

    tr:hover td { background: var(--row-hover); }

    td.flag { color: #6B35A7; font-weight: 600; }
    td.normal { color: #1A7A6E; }

    /* Callout box */
    .callout {
      background: var(--callout-bg);
      border-left: 4px solid var(--link);
      padding: 0.9rem 1.1rem;
      border-radius: 0 4px 4px 0;
      margin: 1.1rem 0;
      font-size: 0.94rem;
    }

    .callout.warning {
      background: var(--callout-warn);
      border-left-color: #b7950b;
    }

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
      margin-right: 0.4rem;
      vertical-align: middle;
    }

    footer {
      background: #1a2e45;
      color: rgba(255,255,255,0.7);
      padding: 1.6rem 1.5rem;
      text-align: center;
      font-size: 0.82rem;
      margin-top: 1rem;
    }

    footer a { color: rgba(255,255,255,0.85); }

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
    position: absolute; bottom: 0.6rem; right: 0.8rem;
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
    border-left: 3px solid rgba(245,166,35,0.7);
    background: rgba(245,166,35,0.05);
    border-radius: 0 4px 4px 0;
    padding: 0.45rem 0 0.45rem 0.9rem;
  }
  :global(details.audit-detail summary) {
    cursor: pointer; list-style: none; user-select: none;
    font-weight: 600; font-size: 0.9rem; color: #F5A623;
  }
  :global(details.audit-detail summary::-webkit-details-marker) { display: none; }
  :global(details.audit-detail summary::before) { content: '▶ '; font-size: 0.7em; }
  :global(details.audit-detail[open] summary::before) { content: '▼ '; }
  :global(details.audit-detail[open] summary) { margin-bottom: 0.5rem; }
  :global(.audit-detail-body) { font-size: 0.91rem; line-height: 1.65; color: inherit; }
  :global(.audit-detail-body p) { margin: 0 0 0.5rem; }
  /* Vocab term — inline expandable definitions */
  :global(.vocab-term) {
    border-bottom: 1.5px dashed rgba(245,166,35,0.65);
    cursor: pointer; color: inherit;
    display: inline; background: none; border-top: none; border-left: none; border-right: none;
    font: inherit; padding: 0; text-align: left;
  }
  :global(.vocab-term:hover) { border-bottom-color: #F5A623; }
  :global(.vocab-panel) {
    display: block;
    background: rgba(245,166,35,0.07); border-left: 3px solid #F5A623;
    border-radius: 0 4px 4px 0; padding: 0.3rem 0.8rem; margin: 0.35rem 0;
    font-size: 0.86rem; line-height: 1.5; color: rgba(255,255,255,0.8);
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
    fill: none; stroke: #7a98b4; stroke-width: 12;
    stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 12 612;
    stroke-dashoffset: 1872;
    opacity: 0.22;
    filter: url(#skel-glow);
    animation: skel-race 4.5s linear infinite;
  }
  .skel-province-shine {
    fill: none; stroke: #7a98b4; stroke-width: 2.5;
    stroke-linecap: round; stroke-linejoin: round;
    stroke-dasharray: 5 619;
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
    text-align: center; pointer-events: none; white-space: nowrap;
    text-shadow: 0 0 14px rgba(122,152,180,0.45), 0 0 30px rgba(122,152,180,0.2);
  }
  #zoom-obj {
    position: absolute; display: block; border: 0;
  }
  #zoom-close {
    position: fixed; top: 1rem; right: 1.4rem; z-index: 9001;
    background: none; border: none;
    color: #fff; font-size: 2.4rem; line-height: 1;
    cursor: pointer; opacity: 0.7;
    transition: opacity 0.15s;
  }
  #zoom-close:hover { opacity: 1; }
  #zoom-pct { font-weight: 700; color: rgba(255,255,255,0.75); font-variant-numeric: tabular-nums; font-size: 0.72rem; min-width: 3em; text-align: right; }
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
    top: 10px; left: 10px; right: 52px;
    z-index: 9002;
    display: flex; flex-direction: column; gap: 5px;
    pointer-events: none;
  }
  #hud > * { pointer-events: auto; }
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
  /* District info bar — only rendered when an ED is selected */
  #ed-callout {
    background: rgba(10,12,18,0.92);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 5px 10px;
    backdrop-filter: blur(10px);
    color: #fff;
    display: none; align-items: center; gap: 10px;
    min-height: 38px;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  #ed-callout.ec-visible {
    display: flex;
    border-color: rgba(122,152,180,0.75);
    box-shadow: 0 0 0 1px rgba(122,152,180,0.25), 0 0 12px rgba(122,152,180,0.15);
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
    margin-left: 0.2em;
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
    left: 0;
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
    display: inline-block; margin-left: 0.4em;
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.04em;
    background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    border-radius: 3px; padding: 0.05rem 0.28rem;
    color: rgba(255,255,255,0.55); vertical-align: middle;
  }

  /* Map onboarding modal */
  #map-intro-modal {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.58);
    z-index: 500;
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
  #map-intro-inner ul { margin: 0 0 0.8rem; padding-left: 1.2rem; }
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
    position: fixed; bottom: 0.45rem; right: 1rem;
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
    position: fixed; bottom: 1.6rem; right: 1.4rem;
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
  @media (max-width: 600px) { #back-top { bottom: 1rem; right: 0.8rem; } }

  /* ── Participation prompt ─────────────────────────────────────────────── */
  :global(#participation-overlay) {
    position: fixed; inset: 0; z-index: 9000;
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
  :global(.part-dnt) {
    font-size: 0.82rem !important;
    background: rgba(107,53,167,0.08);
    border-left: 3px solid #6B35A7;
    padding: 0.5rem 0.7rem;
    border-radius: 0 4px 4px 0;
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
  :global(.part-no)  { background: var(--btn-muted, #e8e8e8); color: var(--text, #111); }
  :global(.part-yes) { background: #6B35A7; color: #fff; }
  :global(.part-policy) {
    font-size: 0.78rem !important; text-align: right;
    margin: 0 !important; color: var(--text-muted, #888) !important;
  }
  :global(.part-policy a) { color: inherit; text-decoration: underline; opacity: 0.7; }

  /* ── Share panel ─────────────────────────────────────────────────────── */
  :global(#tb-share-wrap) { position: relative; }
  :global(#share-panel) {
    position: absolute; top: calc(100% + 6px); right: 0;
    background: var(--bg, #1a1a1a); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px; padding: 0.85rem; width: 320px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
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
</style>
