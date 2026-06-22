<!--
  Integration-spine slice (THROWAWAY): proves deck.gl works as a native npm module inside this
  SvelteKit + adapter-static app — dynamically imported in the browser only (so prerender can't
  break), with base-path-safe fetches of the spike's binary tile pipeline, rendering VA fills.
  If this renders, the full port is mechanical. Not the final component.
-->
<script>
  import { onMount } from 'svelte';
  import { base } from '$app/paths';

  let container;
  let status = $state('init');

  // Binary bundle (from spike_tiler.py): uint32 headerLen | header JSON {key:[start,len]} | pad
  // to 4 | body. Each tile blob: uint32 nRings | per ring: uint16 vaId, uint16 nPts, nPts*2 f32 XY.
  function decodeBundle(buf) {
    const dv = new DataView(buf);
    const hlen = dv.getUint32(0, true);
    const header = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 4, hlen)));
    const bodyOff = 4 + hlen + ((((-(4 + hlen)) % 4) + 4) % 4); // body is 4-byte aligned
    const out = [];
    for (const k in header) {
      let off = bodyOff + header[k][0];
      const nRings = dv.getUint32(off, true);
      off += 4;
      for (let i = 0; i < nRings; i++) {
        const vid = dv.getUint16(off, true);
        const nPts = dv.getUint16(off + 2, true);
        off += 4;
        out.push({ id: vid, coords: new Float32Array(buf, off, nPts * 2) });
        off += nPts * 2 * 4;
      }
    }
    return out;
  }

  onMount(async () => {
    try {
      status = 'loading deck.gl…';
      const { Deck, OrthographicView, COORDINATE_SYSTEM } = await import('@deck.gl/core');
      const { PolygonLayer, ScatterplotLayer } = await import('@deck.gl/layers');

      status = 'loading data…';
      const M = await (await fetch(`${base}/mapdata/manifest.json`)).json();
      const vaProps = await (await fetch(`${base}/mapdata/va_props.json`)).json();
      const bundle = M.bundles[0]; // coarsest level — covers the whole province for an overview
      const buf = await (await fetch(`${base}/mapdata/${bundle.file}`)).arrayBuffer();
      const feats = decodeBundle(buf);

      const [minx, miny, maxx, maxy] = M.bbox;
      const cx = (minx + maxx) / 2, cy = (miny + maxy) / 2;
      const zoom = 1 - Math.log2(M.side / 256);
      const w = container.clientWidth, h = container.clientHeight;

      // Debug markers at the four bbox corners + centre — if these show, the view is pointed at the
      // data and any missing fills are a polygon/colour issue; if not, it's a view/canvas problem.
      const markers = [
        [minx, miny], [maxx, miny], [maxx, maxy], [minx, maxy], [cx, cy]
      ].map((p) => ({ p }));

      new Deck({
        parent: container,
        width: w || window.innerWidth,
        height: h || Math.round(window.innerHeight * 0.72),
        views: new OrthographicView({ flipY: false }),
        initialViewState: { target: [cx, cy, 0], zoom, minZoom: zoom - 4, maxZoom: zoom + 22 },
        controller: true,
        layers: [
          new PolygonLayer({
            id: 'va',
            data: feats,
            getPolygon: (d) => d.coords,
            positionFormat: 'XY',
            getFillColor: (d) => (vaProps[d.id] ? vaProps[d.id].fill : [200, 200, 200]),
            stroked: false,
            filled: true,
            coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
          }),
          new ScatterplotLayer({
            id: 'debug-markers',
            data: markers,
            getPosition: (d) => d.p,
            getRadius: 6,
            radiusMinPixels: 10,
            getFillColor: [255, 0, 255],
            coordinateSystem: COORDINATE_SYSTEM.CARTESIAN
          })
        ]
      });
      status = `ok — ${feats.length} VA · canvas ${w}×${h} · target [${cx | 0},${cy | 0}] zoom ${zoom.toFixed(2)} · bbox[${minx | 0},${miny | 0},${maxx | 0},${maxy | 0}]`;
    } catch (e) {
      status = 'ERROR: ' + ((e && e.message) || e);
      console.error(e);
    }
  });
</script>

<div class="deck-wrap" bind:this={container}></div>
<div class="deck-status">{status}</div>

<style>
  .deck-wrap { position: relative; width: 100%; height: 72vh; background: #0b1020; }
  .deck-status { font: 13px ui-monospace, monospace; padding: 6px 8px; color: #334; }
</style>
