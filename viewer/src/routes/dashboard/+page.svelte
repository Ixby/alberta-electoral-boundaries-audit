<script lang="ts">
  import { onMount } from 'svelte';
  import { db } from '$lib/db';
  import { base } from '$app/paths';

  // ── Types ─────────────────────────────────────────────────────────────────
  type RawEvent = { id: number; session_id: string; event_type: string; payload: any; created_at: string };
  type Session = {
    session_id: string;
    event_count: number; ed_clicks: number; map_switches: number; layer_toggles: number;
    maps_used: string[]; ed_ids: number[];
    first: string; last: string; duration_min: number;
  };
  type EdRow = { id: number; name: string; count: number };

  // ── State ─────────────────────────────────────────────────────────────────
  let loading      = $state(true);
  let err          = $state<string | null>(null);

  let allEvents    = $state<RawEvent[]>([]);
  let edHover      = $state<any[]>([]);

  let totalSessions = $state(0);
  let totalEvents   = $state(0);
  let totalShares   = $state(0);
  let sessions      = $state<Session[]>([]);
  let edCounts      = $state<EdRow[]>([]);
  let maxCount      = $state(1);

  let selectedId   = $state<string | null>(null);
  let replayEvents = $state<RawEvent[]>([]);

  let heatmapEl: HTMLDivElement;
  let heatmapLoaded  = $state(false);
  let heatmapLoading = $state(false);

  const MAP_LABEL: Record<string, string> = { minority: 'Minority', majority: 'Majority', '2019': 'Current' };

  // ── Init ──────────────────────────────────────────────────────────────────
  function withTimeout<T>(p: Promise<T>, ms: number): Promise<T> {
    let id: ReturnType<typeof setTimeout>;
    const timeout = new Promise<T>((_, reject) => {
      id = setTimeout(() => reject(new Error('request timed out')), ms);
    });
    return Promise.race([p, timeout]).finally(() => clearTimeout(id));
  }

  onMount(async () => {
    try {
      const [evResult, shResult, hoverResult] = await Promise.allSettled([
        withTimeout(db.from('telemetry').select('id, session_id, event_type, payload, created_at').order('id'), 10_000),
        withTimeout(db.from('shares').select('id', { count: 'exact' }).limit(0), 10_000),
        withTimeout(fetch(`${base}/data/ed_hover_2019.json`).then(r => { if (!r.ok) throw new Error(`${r.status}`); return r.json(); }), 10_000),
      ]);

      if (evResult.status === 'rejected') throw new Error(`Telemetry: ${(evResult as PromiseRejectedResult).reason?.message ?? (evResult as PromiseRejectedResult).reason}`);
      const evRes = (evResult as PromiseFulfilledResult<any>).value;
      if (evRes.error) throw new Error(evRes.error.message);

      allEvents   = evRes.data ?? [];
      edHover     = hoverResult.status === 'fulfilled' ? (hoverResult.value ?? []) : [];
      totalShares = shResult.status === 'fulfilled'   ? ((shResult.value as any).count ?? 0) : 0;
      totalEvents = allEvents.length;

      // Sessions
      const map: Record<string, Session> = {};
      for (const ev of allEvents) {
        if (!map[ev.session_id]) map[ev.session_id] = {
          session_id: ev.session_id,
          event_count: 0, ed_clicks: 0, map_switches: 0, layer_toggles: 0,
          maps_used: [], ed_ids: [], first: ev.created_at, last: ev.created_at, duration_min: 0,
        };
        const s = map[ev.session_id];
        s.event_count++;
        s.last = ev.created_at;
        if (ev.event_type === 'ed_focus')   { s.ed_clicks++;  s.ed_ids.push(ev.payload.ed_id); }
        if (ev.event_type === 'map_switch')  {
          s.map_switches++;
          if (!s.maps_used.includes(ev.payload.primary)) s.maps_used.push(ev.payload.primary);
        }
        if (ev.event_type === 'layer') s.layer_toggles++;
      }
      for (const s of Object.values(map))
        s.duration_min = Math.round((new Date(s.last).getTime() - new Date(s.first).getTime()) / 60000);

      sessions = Object.values(map).sort((a, b) => +new Date(b.first) - +new Date(a.first));
      totalSessions = sessions.length;

      // ED counts
      const cm: Record<number, number> = {};
      for (const ev of allEvents.filter(e => e.event_type === 'ed_focus'))
        cm[ev.payload.ed_id] = (cm[ev.payload.ed_id] || 0) + 1;
      maxCount = Math.max(...Object.values(cm), 1);
      edCounts = Object.entries(cm)
        .map(([id, count]) => ({ id: +id, name: edHover[+id]?.name ?? `ED ${id}`, count }))
        .sort((a, b) => b.count - a.count);

    } catch (e: any) {
      err = e.message;
    } finally {
      loading = false;
    }
  });

  // ── Replay ────────────────────────────────────────────────────────────────
  function toggleSession(s: Session) {
    if (selectedId === s.session_id) { selectedId = null; replayEvents = []; return; }
    selectedId   = s.session_id;
    replayEvents = allEvents.filter(e => e.session_id === s.session_id);
  }

  function label(ev: RawEvent): string {
    if (ev.event_type === 'ed_focus')   return `Clicked ${edHover[ev.payload.ed_id]?.name ?? `ED ${ev.payload.ed_id}`}`;
    if (ev.event_type === 'map_switch') return `Switched to ${MAP_LABEL[ev.payload.primary] ?? ev.payload.primary} map`;
    if (ev.event_type === 'layer')      return `${ev.payload.on ? 'Enabled' : 'Disabled'} ${ev.payload.key}`;
    return ev.event_type;
  }

  // ── Heatmap ───────────────────────────────────────────────────────────────
  async function loadHeatmap() {
    if (heatmapLoaded || heatmapLoading) return;
    heatmapLoading = true;
    try {
      const text = await fetch(`${base}/images/cover_art_2019_hires.svg`).then(r => r.text());
      const doc  = new DOMParser().parseFromString(text, 'image/svg+xml');
      const svg  = doc.querySelector('svg')!;
      svg.removeAttribute('width'); svg.removeAttribute('height');
      svg.style.cssText = 'width:100%;height:auto;display:block;';

      const cm: Record<number, number> = {};
      for (const { id, count } of edCounts) cm[id] = count;

      svg.querySelectorAll<SVGPathElement>('#ed_hover_layer path[data-ed-id]').forEach(p => {
        const id    = parseInt(p.getAttribute('data-ed-id')!, 10);
        const count = cm[id] || 0;
        if (count > 0) {
          const t = count / maxCount;
          p.style.fill        = lerp('#d4b3f0', '#6B35A7', t);
          p.style.fillOpacity = String((0.3 + t * 0.65).toFixed(2));
        } else {
          p.style.fill = 'none';
        }
      });

      heatmapEl.appendChild(svg);
      heatmapLoaded = true;
    } finally {
      heatmapLoading = false;
    }
  }

  function lerp(a: string, b: string, t: number): string {
    const [r1,g1,b1] = [parseInt(a.slice(1,3),16), parseInt(a.slice(3,5),16), parseInt(a.slice(5,7),16)];
    const [r2,g2,b2] = [parseInt(b.slice(1,3),16), parseInt(b.slice(3,5),16), parseInt(b.slice(5,7),16)];
    return `rgb(${Math.round(r1+(r2-r1)*t)},${Math.round(g1+(g2-g1)*t)},${Math.round(b1+(b2-b1)*t)})`;
  }

  // ── Helpers ───────────────────────────────────────────────────────────────
  function fmtDate(iso: string): string {
    return new Date(iso).toLocaleString('en-CA', { dateStyle: 'short', timeStyle: 'short' });
  }
  function shortId(uuid: string): string { return uuid.slice(0, 8) + '…'; }
</script>

<svelte:head><title>MapExplorer Analytics</title></svelte:head>

<main>
  <header>
    <h1>MapExplorer Analytics</h1>
    {#if !loading && !err}
    <div class="stats-bar">
      <div class="stat"><span class="n">{totalSessions}</span><span class="l">sessions</span></div>
      <div class="stat"><span class="n">{totalEvents}</span><span class="l">events</span></div>
      <div class="stat"><span class="n">{totalShares}</span><span class="l">shares</span></div>
      <div class="stat"><span class="n">{edCounts.reduce((s, r) => s + r.count, 0)}</span><span class="l">district clicks</span></div>
    </div>
    {/if}
  </header>

  {#if loading}
    <p class="loading">Loading…</p>
  {:else if err}
    <p class="error">Error: {err}</p>
  {:else}

  <div class="grid">
    <!-- ED click frequency -->
    <section class="card">
      <h2>Most-clicked districts</h2>
      {#if edCounts.length === 0}
        <p class="muted">No district clicks recorded yet.</p>
      {:else}
      <table>
        <thead><tr><th>District</th><th style="text-align:right">Clicks</th><th></th></tr></thead>
        <tbody>
          {#each edCounts as r}
          <tr>
            <td class="ed-name">{r.name}</td>
            <td class="ed-ct">{r.count}</td>
            <td class="ed-bar"><div class="bar" style="width:{Math.round(r.count/maxCount*100)}%"></div></td>
          </tr>
          {/each}
        </tbody>
      </table>
      {/if}
    </section>

    <!-- Sessions -->
    <section class="card">
      <h2>Sessions <span class="muted" style="font-weight:400;font-size:0.8rem">— click to replay</span></h2>
      <table class="sess">
        <thead><tr><th>ID</th><th>Events</th><th>EDs</th><th>Maps used</th><th>Started</th></tr></thead>
        <tbody>
          {#each sessions as s}
          <tr class="sess-row" class:open={selectedId === s.session_id} onclick={() => toggleSession(s)}>
            <td class="mono">{shortId(s.session_id)}</td>
            <td>{s.event_count}</td>
            <td>{s.ed_clicks}</td>
            <td class="maps">{s.maps_used.map(m => MAP_LABEL[m] ?? m).join(', ') || '—'}</td>
            <td class="muted">{fmtDate(s.first)}</td>
          </tr>
          {#if selectedId === s.session_id}
          <tr class="replay-row">
            <td colspan="5">
              <div class="replay">
                <p class="replay-meta">{s.event_count} events · {s.duration_min} min · {s.ed_clicks} district clicks</p>
                <ol class="flight">
                  {#each replayEvents as ev, i}
                  <li class="step step-{ev.event_type}">
                    <span class="step-i">{i + 1}</span>
                    <span class="step-lbl">{label(ev)}</span>
                  </li>
                  {/each}
                </ol>
              </div>
            </td>
          </tr>
          {/if}
          {/each}
        </tbody>
      </table>
    </section>
  </div>

  <!-- Heatmap -->
  <section class="card heatmap-card">
    <div class="heatmap-hdr">
      <h2>District click heatmap</h2>
      {#if !heatmapLoaded}
      <button class="load-btn" onclick={loadHeatmap} disabled={heatmapLoading}>
        {heatmapLoading ? 'Loading SVG…' : 'Load map (9 MB)'}
      </button>
      {:else}
      <div class="legend">
        <span>1 click</span>
        <div class="grad"></div>
        <span>{maxCount} click{maxCount !== 1 ? 's' : ''}</span>
      </div>
      {/if}
    </div>
    <div class="heatmap-wrap" bind:this={heatmapEl}></div>
  </section>

  {/if}
</main>

<style>
  :global(body) { margin: 0; font-family: system-ui, -apple-system, sans-serif; background: #f2f2f2; color: #111; }
  main  { max-width: 1280px; margin: 0 auto; padding: 1.5rem; }

  header { margin-bottom: 1.5rem; }
  h1 { margin: 0 0 1rem; font-size: 1.35rem; font-weight: 700; }
  h2 { margin: 0 0 1rem; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: #555; }

  .stats-bar { display: flex; gap: 2rem; flex-wrap: wrap; }
  .stat { display: flex; flex-direction: column; }
  .n { font-size: 2.2rem; font-weight: 700; line-height: 1; color: #6B35A7; }
  .l { font-size: 0.75rem; color: #888; margin-top: 0.15rem; text-transform: uppercase; letter-spacing: 0.05em; }

  .loading { padding: 3rem; text-align: center; color: #888; }
  .error   { color: #c00; padding: 1rem; }
  .muted   { color: #999; }

  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem; }
  @media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }

  .card {
    background: #fff; border-radius: 10px; padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    overflow: hidden;
  }

  /* ED table */
  table { width: 100%; border-collapse: collapse; font-size: 0.84rem; }
  th { text-align: left; padding: 0 0.5rem 0.5rem 0; color: #aaa; font-weight: 500; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid #eee; }
  td { padding: 0.38rem 0.5rem 0.38rem 0; border-bottom: 1px solid #f2f2f2; vertical-align: middle; }
  .ed-name { font-size: 0.83rem; }
  .ed-ct   { text-align: right; font-weight: 600; color: #6B35A7; width: 3rem; }
  .ed-bar  { width: 100px; padding-left: 0.5rem; }
  .bar { height: 7px; background: #6B35A7; border-radius: 2px; min-width: 3px; }

  /* Sessions */
  .sess-row { cursor: pointer; transition: background 0.1s; }
  .sess-row:hover td { background: #faf6ff; }
  .sess-row.open td { background: #f3ebfd; }
  .mono { font-family: monospace; font-size: 0.78rem; color: #666; }
  .maps { font-size: 0.78rem; color: #666; }

  /* Replay */
  .replay-row td { padding: 0; }
  .replay { padding: 0.75rem 1rem 1rem; background: #f9f5ff; border-left: 3px solid #6B35A7; }
  .replay-meta { margin: 0 0 0.7rem; font-size: 0.78rem; color: #888; }
  .flight { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 0.25rem; max-height: 300px; overflow-y: auto; }
  .step { display: flex; align-items: baseline; gap: 0.5rem; font-size: 0.81rem; }
  .step-i { width: 1.8rem; text-align: right; color: #ccc; font-size: 0.72rem; flex-shrink: 0; font-variant-numeric: tabular-nums; }
  .step-ed_focus   .step-lbl { color: #6B35A7; font-weight: 500; }
  .step-map_switch .step-lbl { color: #0a6b3e; }
  .step-layer      .step-lbl { color: #666; }

  /* Heatmap */
  .heatmap-card { margin-top: 0; }
  .heatmap-hdr { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
  .heatmap-hdr h2 { margin: 0; }
  .load-btn { background: #6B35A7; color: #fff; border: none; border-radius: 5px; padding: 0.45rem 1rem; font-size: 0.82rem; cursor: pointer; }
  .load-btn:disabled { opacity: 0.55; cursor: default; }
  .load-btn:hover:not(:disabled) { background: #5a2a90; }
  .heatmap-wrap :global(svg) { width: 100%; height: auto; display: block; }

  .legend { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; color: #888; }
  .grad { width: 80px; height: 9px; background: linear-gradient(to right, #d4b3f0, #6B35A7); border-radius: 2px; }
</style>
