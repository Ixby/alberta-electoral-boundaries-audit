<script lang="ts">
  // Alberta Electoral Boundary Audit — private analytics dashboard
  // © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
  // Unlinked admin route. Lives at /admin/analytics — nothing in the site nav points here.
  import { onMount } from 'svelte';
  import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';

  const FN_URL = `${PUBLIC_SUPABASE_URL}/functions/v1/analytics-dashboard`;
  const SS_KEY = 'aa_analytics_key';

  // ── Types ─────────────────────────────────────────────────────────────────
  type Totals = { pageviews: number; visitors: number; explorer_opens: number };
  type DailyRow = { day: string; pageviews: number; visitors: number };
  type SectionRow = { id: string; views: number };
  type DistrictRow = { name: string; selects: number };
  type PerfBlock = {
    samples: number;
    fp: Record<string, number>;
    heap: Record<string, number>;
    fp_p50: number | null;
    fp_p90: number | null;
    heap_p50: number | null;
    loaded_mb_avg: number | null;
  };
  type Dashboard = {
    range_days: number;
    generated_at: string;
    totals: Totals;
    daily: DailyRow[];
    scroll_depth: Record<string, number>;
    engaged: Record<string, number>;
    top_sections: SectionRow[];
    pois: Record<string, number>;
    map_toggle: Record<string, number>;
    zoom_depth: Record<string, number>;
    top_districts: DistrictRow[];
    layer_toggle: Record<string, number>;
    viewport?: Record<string, number>;
    device?: Record<string, number>;
    browser?: Record<string, number>;
    perf?: PerfBlock;
  };

  // ── State ─────────────────────────────────────────────────────────────────
  let key       = $state('');
  let days      = $state<7 | 30 | 90>(30);
  let authed    = $state(false);
  let loading   = $state(false);
  let wrongPass = $state(false);
  let err       = $state<string | null>(null);
  let data      = $state<Dashboard | null>(null);

  // ── Fetch ─────────────────────────────────────────────────────────────────
  async function fetchDashboard(k: string, d: number): Promise<'ok' | 'unauthorized' | 'error'> {
    loading = true;
    err = null;
    try {
      const res = await fetch(FN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          apikey: PUBLIC_SUPABASE_ANON_KEY,
          Authorization: `Bearer ${PUBLIC_SUPABASE_ANON_KEY}`,
        },
        body: JSON.stringify({ key: k, days: d }),
      });
      if (res.status === 401) return 'unauthorized';
      if (!res.ok) {
        err = `Request failed (${res.status})`;
        return 'error';
      }
      data = (await res.json()) as Dashboard;
      return 'ok';
    } catch (e: any) {
      err = e?.message ?? 'Network error';
      return 'error';
    } finally {
      loading = false;
    }
  }

  async function submit() {
    if (!key) return;
    wrongPass = false;
    const r = await fetchDashboard(key, days);
    if (r === 'unauthorized') {
      wrongPass = true;
      authed = false;
      data = null;
      return;
    }
    if (r === 'ok') {
      authed = true;
      try { sessionStorage.setItem(SS_KEY, key); } catch {}
    }
  }

  async function changeDays(d: 7 | 30 | 90) {
    if (d === days) return;
    days = d;
    if (authed) {
      const r = await fetchDashboard(key, d);
      if (r === 'unauthorized') { lock(); wrongPass = true; }
    }
  }

  function lock() {
    authed = false;
    data = null;
    key = '';
    try { sessionStorage.removeItem(SS_KEY); } catch {}
  }

  // ── Restore session (browser-only; never at module scope) ──────────────────
  onMount(async () => {
    let saved: string | null = null;
    try { saved = sessionStorage.getItem(SS_KEY); } catch {}
    if (saved) {
      key = saved;
      const r = await fetchDashboard(saved, days);
      if (r === 'ok') authed = true;
      else { lock(); }
    }
  });

  // ── Chart helpers ──────────────────────────────────────────────────────────
  // Clamp every denominator so the all-zero state never divides by zero → NaN.
  const MAP_COLORS: Record<string, string> = {
    minority: '#7c3ac4',
    majority: '#58e0d4',
    '2019':   '#f5c518',
  };
  const MAP_LABEL: Record<string, string> = {
    minority: 'Minority', majority: 'Majority', '2019': 'Current (2019)',
  };
  const SCROLL_STEPS = ['25', '50', '75', '100'];
  const ENGAGED_STEPS = ['5', '15', '30', '60', '120', '300'];
  const ENGAGED_LABEL: Record<string, string> = {
    '5': '5s', '15': '15s', '30': '30s', '60': '1m', '120': '2m', '300': '5m',
  };
  const ZOOM_ORDER = ['province', 'region', 'city', 'district', 'street'];
  // First-paint bands (must match firstPaintBand() in analytics.ts). Each key is
  // the band's lower-bound ms; labels read as the lower bound in seconds.
  const FP_BANDS = ['0', '250', '500', '750', '1000', '1500', '2000', '3000', '5000'];
  const FP_LABEL: Record<string, string> = {
    '0': '<¼s', '250': '¼s', '500': '½s', '750': '¾s',
    '1000': '1s', '1500': '1½s', '2000': '2s', '3000': '3s', '5000': '5s+',
  };
  // ms → short seconds label (e.g. 750 → "0.75s") for the perf headline figures.
  function fmtMs(ms: number | null | undefined): string {
    if (ms == null) return '—';
    return ms < 1000 ? `${Math.round(ms)}ms` : `${(ms / 1000).toFixed(2).replace(/\.?0+$/, '')}s`;
  }
  // Heap step keys present in the data, ordered numerically (0, 50, 100, …).
  function heapSteps(o: Record<string, number> | undefined): string[] {
    return Object.keys(o ?? {}).sort((a, b) => Number(a) - Number(b));
  }
  // Client-setup dimensions (from pageview props). Fixed display orders + labels.
  const VIEWPORT_ORDER = ['xs', 'sm', 'md', 'lg', 'xl'];
  const VIEWPORT_LABEL: Record<string, string> = {
    xs: 'XS · <480', sm: 'SM · <768', md: 'MD · <1024', lg: 'LG · <1440', xl: 'XL · ≥1440',
  };
  const DEVICE_ORDER = ['mobile', 'tablet', 'desktop'];
  const DEVICE_LABEL: Record<string, string> = {
    mobile: 'Mobile', tablet: 'Tablet', desktop: 'Desktop',
  };
  const BROWSER_LABEL: Record<string, string> = {
    chrome: 'Chrome', safari: 'Safari', firefox: 'Firefox',
    edge: 'Edge', opera: 'Opera', samsung: 'Samsung', other: 'Other',
  };

  function vmax(vals: number[]): number {
    return Math.max(...vals, 1);
  }
  function pct(v: number, max: number): number {
    return Math.round((v / Math.max(max, 1)) * 100);
  }
  function objMax(o: Record<string, number>): number {
    return Math.max(...Object.values(o ?? {}), 1);
  }
  function hasData(o: Record<string, number> | undefined): boolean {
    return !!o && Object.values(o).some((v) => v > 0);
  }
  function fmtDay(iso: string): string {
    // "2026-06-22" → "Jun 22"
    const d = new Date(iso + 'T00:00:00');
    return isNaN(d.getTime()) ? iso : d.toLocaleDateString('en-CA', { month: 'short', day: 'numeric' });
  }
  function fmtTime(iso: string): string {
    const d = new Date(iso);
    return isNaN(d.getTime()) ? iso : d.toLocaleString('en-CA', { dateStyle: 'medium', timeStyle: 'short' });
  }

  // Daily line-chart geometry (computed reactively)
  const CW = 640, CH = 160, PAD = 8;
  // dailyMax is the clamped denominator for scaling; dailyPeak is the true peak for display.
  let dailyMax  = $derived(data ? vmax(data.daily.flatMap((r) => [r.pageviews, r.visitors])) : 1);
  let dailyPeak = $derived(data ? Math.max(0, ...data.daily.flatMap((r) => [r.pageviews, r.visitors])) : 0);
  function linePoints(rows: DailyRow[], pick: (r: DailyRow) => number): string {
    const n = rows.length;
    if (n === 0) return '';
    return rows
      .map((r, i) => {
        const x = n === 1 ? CW / 2 : PAD + (i / (n - 1)) * (CW - 2 * PAD);
        const y = CH - PAD - (pick(r) / Math.max(dailyMax, 1)) * (CH - 2 * PAD);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      })
      .join(' ');
  }
</script>

<svelte:head><title>Audit Analytics</title></svelte:head>

<main>
  {#if !authed}
    <!-- ── Password gate (also the prerendered shell) ── -->
    <div class="gate">
      <h1>Audit Analytics</h1>
      <p class="sub">Private dashboard. Enter the access key.</p>
      <form onsubmit={(e) => { e.preventDefault(); submit(); }}>
        <input
          type="password"
          autocomplete="current-password"
          placeholder="Access key"
          bind:value={key}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !key}>
          {loading ? 'Checking…' : 'View'}
        </button>
      </form>
      {#if wrongPass}<p class="bad">Wrong password</p>{/if}
      {#if err}<p class="bad">{err}</p>{/if}
    </div>
  {:else if data}
    <!-- ── Dashboard ── -->
    <header class="topbar">
      <div>
        <h1>Audit Analytics</h1>
        <p class="meta">
          Last {data.range_days} days · generated {fmtTime(data.generated_at)}
        </p>
      </div>
      <div class="controls">
        <div class="seg" role="group" aria-label="Date range">
          {#each [7, 30, 90] as d}
            <button
              class:active={days === d}
              disabled={loading}
              onclick={() => changeDays(d as 7 | 30 | 90)}
            >{d}d</button>
          {/each}
        </div>
        <button class="lock" onclick={lock}>Lock</button>
      </div>
    </header>

    {#if loading}<p class="loading">Refreshing…</p>{/if}
    {#if err}<p class="bad">{err}</p>{/if}

    <!-- Totals -->
    <section class="totals">
      <div class="stat">
        <span class="n">{data.totals.visitors.toLocaleString('en-CA')}</span>
        <span class="l">Visitors</span>
      </div>
      <div class="stat">
        <span class="n">{data.totals.pageviews.toLocaleString('en-CA')}</span>
        <span class="l">Pageviews</span>
      </div>
      <div class="stat">
        <span class="n">{data.totals.explorer_opens.toLocaleString('en-CA')}</span>
        <span class="l">Explorer opens</span>
      </div>
      <div class="stat">
        <span class="n">{data.perf && data.perf.samples > 0 ? fmtMs(data.perf.fp_p50) : '—'}</span>
        <span class="l">Median first paint</span>
      </div>
    </section>

    <div class="grid">
      <!-- Daily traffic -->
      <section class="card span2">
        <h2>Daily traffic</h2>
        {#if data.daily.length === 0}
          <p class="muted">No data yet</p>
        {:else}
          <svg class="chart" viewBox="0 0 {CW} {CH}" preserveAspectRatio="none" role="img" aria-label="Daily visitors and pageviews">
            <line x1={PAD} y1={CH - PAD} x2={CW - PAD} y2={CH - PAD} class="axis" />
            <polyline points={linePoints(data.daily, (r) => r.pageviews)} class="line pv" />
            <polyline points={linePoints(data.daily, (r) => r.visitors)} class="line vi" />
            {#each data.daily as r, i}
              {@const n = data.daily.length}
              {@const x = n === 1 ? CW / 2 : PAD + (i / (n - 1)) * (CW - 2 * PAD)}
              <circle cx={x} cy={CH - PAD - (r.visitors / Math.max(dailyMax, 1)) * (CH - 2 * PAD)} r="2" class="dot vi" />
            {/each}
          </svg>
          <div class="legend">
            <span><i class="sw vi"></i>Visitors</span>
            <span><i class="sw pv"></i>Pageviews</span>
            <span class="muted">{fmtDay(data.daily[0].day)} – {fmtDay(data.daily[data.daily.length - 1].day)} · peak {dailyPeak}</span>
          </div>
        {/if}
      </section>

      <!-- Scroll-depth funnel -->
      <section class="card">
        <h2>Scroll depth</h2>
        {#if !hasData(data.scroll_depth)}
          <p class="muted">No data yet</p>
        {:else}
          {@const sMax = objMax(data.scroll_depth)}
          <div class="funnel">
            {#each SCROLL_STEPS as step}
              {@const v = data.scroll_depth[step] ?? 0}
              <div class="frow">
                <span class="flabel">{step}%</span>
                <div class="ftrack"><div class="fbar" style="width:{pct(v, sMax)}%"></div></div>
                <span class="fval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Engaged time -->
      <section class="card">
        <h2>Engaged time</h2>
        {#if !hasData(data.engaged)}
          <p class="muted">No data yet</p>
        {:else}
          {@const eMax = objMax(data.engaged)}
          <div class="vbars">
            {#each ENGAGED_STEPS as step}
              {@const v = data.engaged[step] ?? 0}
              <div class="vbar-wrap">
                <span class="vbar-val">{v}</span>
                <div class="vbar" style="height:{pct(v, eMax)}%"></div>
                <span class="vbar-lbl">{ENGAGED_LABEL[step]}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Top sections -->
      <section class="card">
        <h2>Top sections</h2>
        {#if data.top_sections.length === 0}
          <p class="muted">No data yet</p>
        {:else}
          {@const secMax = vmax(data.top_sections.map((s) => s.views))}
          <div class="hbars">
            {#each data.top_sections as s}
              <div class="hrow">
                <span class="hlabel" title={s.id}>{s.id}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(s.views, secMax)}%"></div></div>
                <span class="hval">{s.views}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Points of interest -->
      <section class="card">
        <h2>Points of interest</h2>
        {#if !hasData(data.pois)}
          <p class="muted">No data yet</p>
        {:else}
          {@const pMax = objMax(data.pois)}
          <div class="hbars">
            {#each Object.entries(data.pois).sort((a, b) => b[1] - a[1]) as [name, v]}
              <div class="hrow">
                <span class="hlabel" title={name}>{name}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, pMax)}%"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Map toggle -->
      <section class="card">
        <h2>Map views</h2>
        {#if !hasData(data.map_toggle)}
          <p class="muted">No data yet</p>
        {:else}
          {@const mMax = objMax(data.map_toggle)}
          <div class="hbars">
            {#each ['minority', 'majority', '2019'] as m}
              {@const v = data.map_toggle[m] ?? 0}
              <div class="hrow">
                <span class="hlabel">{MAP_LABEL[m] ?? m}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, mMax)}%; background:{MAP_COLORS[m]}"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Zoom depth -->
      <section class="card">
        <h2>Zoom depth</h2>
        {#if !hasData(data.zoom_depth)}
          <p class="muted">No data yet</p>
        {:else}
          {@const zMax = objMax(data.zoom_depth)}
          <div class="vbars">
            {#each ZOOM_ORDER as z}
              {@const v = data.zoom_depth[z] ?? 0}
              <div class="vbar-wrap">
                <span class="vbar-val">{v}</span>
                <div class="vbar zoom" style="height:{pct(v, zMax)}%"></div>
                <span class="vbar-lbl">{z}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Top districts -->
      <section class="card span2">
        <h2>Top districts</h2>
        {#if data.top_districts.length === 0}
          <p class="muted">No data yet</p>
        {:else}
          {@const dMax = vmax(data.top_districts.map((d) => d.selects))}
          <div class="hbars">
            {#each data.top_districts as dist}
              <div class="hrow">
                <span class="hlabel wide" title={dist.name}>{dist.name}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(dist.selects, dMax)}%"></div></div>
                <span class="hval">{dist.selects}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Layer toggle -->
      <section class="card">
        <h2>Layer toggles</h2>
        {#if !hasData(data.layer_toggle)}
          <p class="muted">No data yet</p>
        {:else}
          {@const lMax = objMax(data.layer_toggle)}
          <div class="hbars">
            {#each Object.entries(data.layer_toggle).sort((a, b) => b[1] - a[1]) as [name, v]}
              <div class="hrow">
                <span class="hlabel">{name}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, lMax)}%"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Load performance (first-paint snapshot) -->
      <section class="card span2">
        <h2>Load performance</h2>
        {#if !data.perf || data.perf.samples === 0}
          <p class="muted">No data yet</p>
        {:else}
          <div class="perf-head">
            <div class="pstat"><span class="pn">{fmtMs(data.perf.fp_p50)}</span><span class="pl">Median first paint</span></div>
            <div class="pstat"><span class="pn">{fmtMs(data.perf.fp_p90)}</span><span class="pl">p90 first paint</span></div>
            <div class="pstat"><span class="pn">{data.perf.heap_p50 != null ? data.perf.heap_p50 + ' MB' : '—'}</span><span class="pl">Median heap</span></div>
            <div class="pstat"><span class="pn">{data.perf.loaded_mb_avg != null ? data.perf.loaded_mb_avg + ' MB' : '—'}</span><span class="pl">Avg first payload</span></div>
            <div class="pstat"><span class="pn">{data.perf.samples.toLocaleString('en-CA')}</span><span class="pl">Samples</span></div>
          </div>
          {#if hasData(data.perf.fp)}
            {@const fMax = objMax(data.perf.fp)}
            <h3 class="sub-h">First-paint distribution</h3>
            <div class="vbars">
              {#each FP_BANDS as b}
                {@const v = data.perf.fp[b] ?? 0}
                <div class="vbar-wrap">
                  <span class="vbar-val">{v}</span>
                  <div class="vbar perf" style="height:{pct(v, fMax)}%"></div>
                  <span class="vbar-lbl">{FP_LABEL[b] ?? b}</span>
                </div>
              {/each}
            </div>
          {/if}
        {/if}
      </section>

      <!-- Memory (heap) -->
      <section class="card">
        <h2>Memory (heap)</h2>
        {#if !data.perf || !hasData(data.perf.heap)}
          <p class="muted">No data yet</p>
        {:else}
          {@const hMax = objMax(data.perf.heap)}
          <div class="vbars">
            {#each heapSteps(data.perf.heap) as step}
              {@const v = data.perf.heap[step] ?? 0}
              <div class="vbar-wrap">
                <span class="vbar-val">{v}</span>
                <div class="vbar heap" style="height:{pct(v, hMax)}%"></div>
                <span class="vbar-lbl">{step}</span>
              </div>
            {/each}
          </div>
          <p class="muted unit">MB used (25 MB bands)</p>
        {/if}
      </section>

      <!-- Device -->
      <section class="card">
        <h2>Device</h2>
        {#if !hasData(data.device)}
          <p class="muted">No data yet</p>
        {:else}
          {@const dev = data.device ?? {}}
          {@const dvMax = objMax(dev)}
          <div class="hbars">
            {#each DEVICE_ORDER.filter((k) => (dev[k] ?? 0) > 0) as k}
              {@const v = dev[k] ?? 0}
              <div class="hrow">
                <span class="hlabel">{DEVICE_LABEL[k] ?? k}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, dvMax)}%"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>

      <!-- Screen size -->
      <section class="card">
        <h2>Screen size</h2>
        {#if !hasData(data.viewport)}
          <p class="muted">No data yet</p>
        {:else}
          {@const vp = data.viewport ?? {}}
          {@const vpMax = objMax(vp)}
          <div class="hbars">
            {#each VIEWPORT_ORDER.filter((k) => (vp[k] ?? 0) > 0) as k}
              {@const v = vp[k] ?? 0}
              <div class="hrow">
                <span class="hlabel">{VIEWPORT_LABEL[k] ?? k}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, vpMax)}%"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
          <p class="muted unit">Viewport width band (px)</p>
        {/if}
      </section>

      <!-- Browser -->
      <section class="card">
        <h2>Browser</h2>
        {#if !hasData(data.browser)}
          <p class="muted">No data yet</p>
        {:else}
          {@const br = data.browser ?? {}}
          {@const brMax = objMax(br)}
          <div class="hbars">
            {#each Object.entries(br).sort((a, b) => b[1] - a[1]) as [k, v]}
              <div class="hrow">
                <span class="hlabel">{BROWSER_LABEL[k] ?? k}</span>
                <div class="htrack"><div class="hbar" style="width:{pct(v, brMax)}%"></div></div>
                <span class="hval">{v}</span>
              </div>
            {/each}
          </div>
        {/if}
      </section>
    </div>
  {/if}
</main>

<style>
  :global(body) { margin: 0; }

  main {
    min-height: 100vh;
    background: #0d0f14;
    color: #e7e9ee;
    font-family: ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    padding: 1.5rem;
    box-sizing: border-box;
  }

  h1 { font-size: 1.4rem; margin: 0; font-weight: 650; letter-spacing: -0.01em; }
  h2 { font-size: 0.85rem; margin: 0 0 0.85rem; font-weight: 600; color: #aab2c2; text-transform: uppercase; letter-spacing: 0.04em; }

  /* ── Gate ── */
  .gate {
    max-width: 360px;
    margin: 14vh auto 0;
    text-align: center;
  }
  .gate .sub { color: #8b93a3; font-size: 0.9rem; margin: 0.4rem 0 1.5rem; }
  .gate form { display: flex; gap: 0.5rem; }
  .gate input {
    flex: 1;
    background: #161a22;
    border: 1px solid #2a303c;
    color: #e7e9ee;
    border-radius: 8px;
    padding: 0.6rem 0.75rem;
    font-size: 0.95rem;
    outline: none;
  }
  .gate input:focus { border-color: #7c3ac4; }
  .gate button {
    background: #7c3ac4;
    color: #fff;
    border: 0;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    cursor: pointer;
  }
  .gate button:disabled { opacity: 0.5; cursor: default; }

  .bad { color: #f87171; font-size: 0.9rem; margin: 0.9rem 0 0; }
  .loading { color: #8b93a3; font-size: 0.9rem; }
  .muted { color: #6c7385; font-size: 0.85rem; margin: 0.4rem 0; }

  /* ── Topbar ── */
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.25rem;
  }
  .meta { color: #8b93a3; font-size: 0.82rem; margin: 0.3rem 0 0; }
  .controls { display: flex; gap: 0.6rem; align-items: center; }
  .seg { display: inline-flex; background: #161a22; border: 1px solid #2a303c; border-radius: 8px; overflow: hidden; }
  .seg button {
    background: transparent; border: 0; color: #aab2c2;
    padding: 0.45rem 0.8rem; font-size: 0.85rem; cursor: pointer;
  }
  .seg button.active { background: #7c3ac4; color: #fff; }
  .seg button:disabled { opacity: 0.5; cursor: default; }
  .lock {
    background: #161a22; border: 1px solid #2a303c; color: #aab2c2;
    border-radius: 8px; padding: 0.45rem 0.9rem; font-size: 0.85rem; cursor: pointer;
  }
  .lock:hover { border-color: #3a4253; color: #e7e9ee; }

  /* ── Totals ── */
  .totals {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.25rem;
  }
  .stat {
    background: #141821;
    border: 1px solid #222836;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .stat .n { font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; }
  .stat .l { font-size: 0.8rem; color: #8b93a3; text-transform: uppercase; letter-spacing: 0.04em; }

  /* ── Grid of cards ── */
  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  .card {
    background: #141821;
    border: 1px solid #222836;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    min-width: 0;
  }
  .span2 { grid-column: 1 / -1; }

  /* ── Daily line chart ── */
  .chart { width: 100%; height: 160px; display: block; }
  .axis { stroke: #2a303c; stroke-width: 1; }
  .line { fill: none; stroke-width: 2; vector-effect: non-scaling-stroke; }
  .line.pv { stroke: #58e0d4; }
  .line.vi { stroke: #7c3ac4; }
  .dot.vi { fill: #7c3ac4; }
  .legend { display: flex; gap: 1rem; align-items: center; margin-top: 0.5rem; font-size: 0.8rem; color: #aab2c2; flex-wrap: wrap; }
  .legend .sw { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 0.35rem; vertical-align: middle; }
  .sw.pv { background: #58e0d4; }
  .sw.vi { background: #7c3ac4; }

  /* ── Funnel / horizontal bars ── */
  .funnel, .hbars { display: flex; flex-direction: column; gap: 0.55rem; }
  .frow, .hrow { display: grid; grid-template-columns: auto 1fr auto; gap: 0.6rem; align-items: center; }
  .flabel { font-size: 0.82rem; color: #aab2c2; min-width: 2.5rem; }
  .hlabel {
    font-size: 0.82rem; color: #c3c9d6; min-width: 5rem; max-width: 9rem;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .hlabel.wide { max-width: 14rem; }
  .ftrack, .htrack { background: #1d222d; border-radius: 5px; height: 14px; overflow: hidden; }
  .fbar, .hbar { height: 100%; background: #7c3ac4; border-radius: 5px; min-width: 2px; transition: width 0.3s ease; }
  .fval, .hval { font-size: 0.82rem; color: #aab2c2; min-width: 2rem; text-align: right; font-variant-numeric: tabular-nums; }

  /* ── Vertical bars ── */
  .vbars { display: flex; align-items: flex-end; gap: 0.5rem; height: 150px; }
  .vbar-wrap { flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; gap: 0.3rem; }
  .vbar { width: 100%; max-width: 38px; background: #58e0d4; border-radius: 4px 4px 0 0; min-height: 2px; transition: height 0.3s ease; }
  .vbar.zoom { background: #7c3ac4; }
  .vbar.perf { background: #f5c518; }
  .vbar.heap { background: #f08e60; }

  /* ── Perf headline ── */
  .perf-head {
    display: flex; flex-wrap: wrap; gap: 1.5rem;
    margin-bottom: 1.1rem; padding-bottom: 1rem;
    border-bottom: 1px solid #222836;
  }
  .pstat { display: flex; flex-direction: column; gap: 0.15rem; }
  .pstat .pn { font-size: 1.35rem; font-weight: 700; letter-spacing: -0.01em; font-variant-numeric: tabular-nums; }
  .pstat .pl { font-size: 0.74rem; color: #8b93a3; text-transform: uppercase; letter-spacing: 0.04em; }
  .sub-h { font-size: 0.74rem; margin: 0 0 0.7rem; font-weight: 600; color: #8b93a3; text-transform: uppercase; letter-spacing: 0.04em; }
  .unit { text-align: center; margin-top: 0.5rem; }
  .vbar-val { font-size: 0.78rem; color: #aab2c2; font-variant-numeric: tabular-nums; }
  .vbar-lbl { font-size: 0.72rem; color: #6c7385; }

  @media (max-width: 960px) {
    .totals { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 720px) {
    .grid { grid-template-columns: 1fr; }
    .span2 { grid-column: auto; }
  }
</style>
