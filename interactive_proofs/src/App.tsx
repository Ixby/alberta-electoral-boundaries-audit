import { useState, useEffect, useRef } from 'react';
import Map, { Source, Layer, useMap } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { ChevronRight, ChevronLeft, Lock, Unlock, AlertTriangle } from 'lucide-react';

const mapStyle = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json";

function FitBounds({ bounds }: { bounds: number[] }) {
  const { current: map } = useMap();
  useEffect(() => {
    if (map && bounds) {
      map.fitBounds(
        [[bounds[0], bounds[1]], [bounds[2], bounds[3]]],
        { padding: 100, duration: 1500 }
      );
    }
  }, [bounds, map]);
  return null;
}

function PowerBar({ stats, title }: { stats: any, title: string }) {
  return (
    <div className="mb-6">
      <h3 className="text-slate-400 text-sm font-bold uppercase tracking-wider mb-2">{title}</h3>
      <div className="flex h-12 rounded-lg overflow-hidden relative shadow-lg">
        <div style={{ width: `${stats.ndp}%` }} className="bg-orange-500 flex items-center px-3 transition-all duration-1000">
          {stats.ndp > 15 && <span className="text-white font-bold text-lg drop-shadow-md">{stats.ndp.toFixed(0)}%</span>}
        </div>
        <div style={{ width: `${stats.ucp}%` }} className="bg-blue-600 flex items-center justify-end px-3 transition-all duration-1000">
          {stats.ucp > 15 && <span className="text-white font-bold text-lg drop-shadow-md">{stats.ucp.toFixed(0)}%</span>}
        </div>
      </div>
      <div className="flex justify-between mt-2 items-center">
        <span className="text-white font-bold text-lg">{stats.winner} Wins by {stats.margin.toFixed(0)}%</span>
        <span className={`px-2 py-1 text-xs font-bold rounded ${stats.safety === 'Safe Seat' ? 'bg-red-900/50 text-red-400 border border-red-500/30' : 'bg-slate-800 text-slate-300'}`}>
          {stats.safety === 'Safe Seat' && <Lock className="inline w-3 h-3 mr-1 mb-0.5"/>}
          {stats.safety}
        </span>
      </div>
    </div>
  );
}

function App() {
  const [events, setEvents] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showNew, setShowNew] = useState(false);
  const [geojsons, setGeojsons] = useState<any>({ old: null, new: null, dots: null });
  
  useEffect(() => {
    fetch('/data/events.json').then(res => res.json()).then(data => setEvents(data));
  }, []);

  useEffect(() => {
    if (events.length === 0) return;
    const ev = events[currentIndex];
    setShowNew(false);
    Promise.all([
      fetch(`/data/${ev.id}_2019.geojson`).then(res => res.json()),
      fetch(`/data/${ev.id}_2026.geojson`).then(res => res.json()),
      fetch(`/data/${ev.id}_dots.geojson`).then(res => res.json())
    ]).then(([oldData, newData, dotsData]) => {
      setGeojsons({ old: oldData, new: newData, dots: dotsData });
    });
  }, [currentIndex, events]);

  if (events.length === 0 || !geojsons.old) return (
    <div className="h-screen w-full bg-slate-950 flex items-center justify-center flex-col">
      <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
      <h1 className="text-white font-bold text-2xl tracking-tight">Loading Forensic Pipeline...</h1>
    </div>
  );

  const ev = events[currentIndex];

  return (
    <div className="flex h-screen w-full bg-slate-950 overflow-hidden font-sans">
      
      {/* LEFT PANEL: NARRATIVE */}
      <div className="w-[30%] min-w-[450px] max-w-[500px] bg-slate-900/90 backdrop-blur-xl border-r border-slate-800 z-10 flex flex-col shadow-2xl">
        
        {/* HEADER */}
        <div className="p-8 pb-6 border-b border-slate-800">
          <div className="flex items-center gap-2 mb-4">
            <span className="px-2 py-1 bg-red-500 text-white text-xs font-bold rounded uppercase tracking-wider flex items-center">
              <AlertTriangle className="w-3 h-3 mr-1" />
              {ev.type}
            </span>
            <span className="text-slate-400 text-xs font-bold tracking-wider uppercase border border-slate-700 px-2 py-1 rounded">
              {ev.map_label} Proposal
            </span>
          </div>
          <h1 className="text-4xl font-black text-white leading-tight tracking-tight mb-4">
            {ev.title}
          </h1>
          <p className="text-slate-300 text-lg leading-relaxed border-l-4 border-blue-500 pl-4">
            {ev.desc}
          </p>
        </div>

        {/* HUMAN IMPACT */}
        <div className="p-8 py-6 bg-slate-800/30">
          <p className="text-white font-medium italic text-lg leading-snug">
            "{ev.voter_impact}"
          </p>
        </div>

        {/* POWER SHIFT */}
        <div className="p-8 flex-1 overflow-y-auto">
          <PowerBar stats={ev.old_stats} title="2023 Result (Old Boundaries)" />
          
          <div className="flex justify-center my-4">
            <div className="h-8 w-px bg-slate-700"></div>
          </div>
          
          <div className={`transition-all duration-700 ${showNew ? 'opacity-100 blur-none' : 'opacity-30 blur-sm'}`}>
             <PowerBar stats={ev.new_stats} title="Projected Result (New Boundaries)" />
          </div>
        </div>

        {/* CONTROLS */}
        <div className="p-6 border-t border-slate-800 bg-slate-950 flex flex-col gap-4">
          <button 
            onClick={() => setShowNew(!showNew)}
            className={`w-full py-4 rounded-lg font-black text-xl tracking-wide transition-all duration-300 shadow-lg border ${
              showNew ? 'bg-slate-800 text-white border-slate-700 hover:bg-slate-700' : 'bg-blue-600 text-white border-blue-500 hover:bg-blue-500 animate-pulse'
            }`}
          >
            {showNew ? 'REVERT TO OLD MAP' : 'REVEAL THE NEW MAP'}
          </button>
          
          <div className="flex justify-between items-center text-slate-400">
            <button 
              onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
              disabled={currentIndex === 0}
              className="p-2 hover:text-white hover:bg-slate-800 rounded disabled:opacity-30 disabled:hover:bg-transparent"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
            <span className="font-bold tracking-widest text-xs uppercase">
              Event {currentIndex + 1} of {events.length}
            </span>
            <button 
              onClick={() => setCurrentIndex(Math.min(events.length - 1, currentIndex + 1))}
              disabled={currentIndex === events.length - 1}
              className="p-2 hover:text-white hover:bg-slate-800 rounded disabled:opacity-30 disabled:hover:bg-transparent"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      {/* RIGHT PANEL: MAP */}
      <div className="flex-1 relative bg-slate-950">
        <Map
          initialViewState={{ longitude: -114.07, latitude: 51.04, zoom: 6 }}
          mapStyle={mapStyle}
          interactive={true}
        >
          <FitBounds bounds={ev.bounds} />

          {/* DOTS (Render underneath borders) */}
          {geojsons.dots && (
            <Source id="dots" type="geojson" data={geojsons.dots}>
              <Layer
                id="dots-layer"
                type="circle"
                paint={{
                  'circle-radius': ['interpolate', ['linear'], ['zoom'], 6, 2, 12, 6],
                  'circle-color': ['match', ['get', 'party'], 'NDP', '#f37021', 'UCP', '#003f72', '#ffffff'],
                  'circle-opacity': 0.8,
                  'circle-stroke-width': 0
                }}
              />
            </Source>
          )}

          {/* OLD BORDERS */}
          {geojsons.old && (
            <Source id="old" type="geojson" data={geojsons.old}>
              <Layer
                id="old-fill"
                type="fill"
                paint={{
                  'fill-color': '#000000',
                  'fill-opacity': showNew ? 0.4 : 0.0,
                }}
              />
              <Layer
                id="old-line"
                type="line"
                paint={{
                  'line-color': showNew ? '#475569' : '#94a3b8',
                  'line-width': showNew ? 1 : 3,
                  'line-dasharray': showNew ? [2, 2] : [1]
                }}
              />
            </Source>
          )}

          {/* NEW BORDERS */}
          {geojsons.new && showNew && (
            <Source id="new" type="geojson" data={geojsons.new}>
              <Layer
                id="new-line"
                type="line"
                paint={{
                  'line-color': '#ef4444',
                  'line-width': 4,
                }}
              />
              <Layer
                id="new-fill"
                type="fill"
                paint={{
                  'fill-color': '#ef4444',
                  'fill-opacity': 0.1,
                }}
              />
            </Source>
          )}
        </Map>
        
        {/* Overlay Title */}
        <div className="absolute top-6 left-6 pointer-events-none">
           <h2 className="text-white font-black text-6xl opacity-20 tracking-tighter drop-shadow-lg uppercase">
             {showNew ? 'Proposed Map' : '2019 Map'}
           </h2>
        </div>
      </div>
      
    </div>
  );
}

export default App;
