// Alberta Electoral Boundary Audit — ED search
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wires the toolbar search input once at init. Internally self-contained after that.

import type { MapCtx, MapKey } from './types';
import { DOM_IDS } from './domIds';
import { awaitReady } from './readyState';
import { STR } from './strings';
import { clearEdHighlight } from './edInteraction';

type SearchDeps = {
  showCallout:       (rec: any) => void;
  setEdHighlight:    (pathEl: SVGGraphicsElement) => void;
  snapToED:          (pathEl: SVGGraphicsElement, force?: boolean) => void;
  updateMapButtons:  () => void;
  doSwitchPrimary:   (key: MapKey) => void;
};

export function initSearch(ctx: MapCtx, deps: SearchDeps): void {
  const { showCallout, setEdHighlight, snapToED, updateMapButtons, doSwitchPrimary } = deps;

  const searchInput   = document.getElementById(DOM_IDS.tbSearch)        as HTMLInputElement | null;
  const searchResults = document.getElementById(DOM_IDS.tbSearchResults) as HTMLElement      | null;
  if (!searchInput || !searchResults) return;

  let _srActive = -1;

  function _srItems(): HTMLLIElement[] {
    return Array.from(searchResults!.querySelectorAll<HTMLLIElement>('li'));
  }

  function _srHighlight(newIdx: number) {
    const items = _srItems();
    if (!items.length) return;
    _srActive = Math.max(0, Math.min(items.length - 1, newIdx));
    items.forEach(function(li, i) { li.classList.toggle('sr-active', i === _srActive); });
    items[_srActive].scrollIntoView({ block: 'nearest' });
    _previewHighlight(items[_srActive]);
  }

  function _srSelect(li: HTMLLIElement | null) {
    if (!li) return;
    const name = li.dataset.edName || (li.textContent || '').replace(/\s*(Min|Maj|2019)$/, '').trim();
    const fromMap = (li.dataset.edMap || ctx.mapPrimary) as MapKey;
    searchInput!.value = name;
    searchResults!.style.display = 'none';
    _srActive = -1;
    if (!ctx.svgEl) return;

    function navigateToEd(mapKey: MapKey, edName: string) {
      const idx2 = ctx.nameIndex[mapKey] || {};
      const rec2 = idx2[edName];
      if (!rec2) return;
      const path = ctx.svgEl && ctx.svgEl.querySelector<SVGGraphicsElement>('#ed_hover_layer path[data-ed-id="' + rec2.id + '"]');
      if (path) { showCallout(rec2); setEdHighlight(path); if (!ctx.mapLocked) snapToED(path, true); }
    }

    if (fromMap !== ctx.mapPrimary) {
      ctx.mapOn[fromMap] = true;
      ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== fromMap; });
      ctx.mapActivationOrder.push(fromMap);
      ctx.mapPrimary = fromMap;
      updateMapButtons();
      doSwitchPrimary(fromMap);
      awaitReady(ctx, 4500)
        .then(() => { if (ctx.svgEl) navigateToEd(fromMap, name); })
        .catch(() => {});
    } else {
      navigateToEd(ctx.mapPrimary as MapKey, name);
    }
  }

  // ── Live map highlight while browsing the list ────────────────────────────
  // As the user hovers or arrow-keys through entries, the corresponding
  // district lights up on the map (no viewport snap — just the glow), so
  // scrolling the list doubles as a tour of the map. Entries from other
  // maps can't be highlighted without a map switch and are skipped.
  function _previewHighlight(li: HTMLLIElement | null) {
    if (!li || !ctx.svgEl) return;
    const name = li.dataset.edName || '';
    const fromMap = li.dataset.edMap as MapKey | undefined;
    if (fromMap && fromMap !== ctx.mapPrimary) { _restoreSelectionHighlight(); return; }
    const idx2 = ctx.mapPrimary ? ctx.nameIndex[ctx.mapPrimary] : null;
    const rec = idx2 ? idx2[name] : null;
    if (!rec) return;
    const path = ctx.svgEl.querySelector<SVGGraphicsElement>('#ed_hover_layer path[data-ed-id="' + rec.id + '"]');
    if (path) setEdHighlight(path);
  }

  // On dropdown close (without selection), restore the highlight to the
  // currently selected district if there is one; otherwise clear the
  // transient preview glow.
  function _restoreSelectionHighlight() {
    if (!ctx.svgEl) return;
    if (ctx.selectedEdName && ctx.mapPrimary) {
      const idx2 = ctx.nameIndex[ctx.mapPrimary];
      const rec = idx2 ? idx2[ctx.selectedEdName] : null;
      const path = rec ? ctx.svgEl.querySelector<SVGGraphicsElement>('#ed_hover_layer path[data-ed-id="' + rec.id + '"]') : null;
      if (path) { setEdHighlight(path); return; }
    }
    clearEdHighlight(ctx);
  }

  function _closeDropdown() {
    searchResults!.style.display = 'none';
    _srActive = -1;
    _restoreSelectionHighlight();
  }

  function _renderResults(results: Array<{ name: string; map: MapKey }>) {
    searchResults!.innerHTML = '';
    _srActive = -1;
    if (!results.length) { searchResults!.style.display = 'none'; return; }
    results.forEach(function(r) {
      const li = document.createElement('li');
      li.dataset.edName = r.name;
      li.dataset.edMap = r.map;
      const nameSpan = document.createElement('span');
      nameSpan.textContent = r.name;
      li.appendChild(nameSpan);
      if (r.map !== ctx.mapPrimary) {
        const tag = document.createElement('span');
        tag.className = 'sr-map-tag';
        tag.textContent = r.map === '2019' ? STR.tag2019 : r.map === 'minority' ? STR.tagMin : STR.tagMaj;
        li.appendChild(tag);
      }
      li.addEventListener('mousedown', function(e) { e.preventDefault(); });
      li.addEventListener('click', function(e) { e.stopPropagation(); _srSelect(li); });
      li.addEventListener('mouseover', function() {
        _srActive = _srItems().indexOf(li);
        _srItems().forEach(function(item) { item.classList.toggle('sr-active', item === li); });
        _previewHighlight(li);
      });
      searchResults!.appendChild(li);
    });
    searchResults!.style.display = 'block';
  }

  function _collectResults(q: string): Array<{ name: string; map: MapKey }> {
    const seen = new Set<string>();
    const results: Array<{ name: string; map: MapKey }> = [];
    const mapOrder = ([ctx.mapPrimary, 'minority', 'majority', '2019'] as Array<MapKey | null>).filter(
      function(k, i, a) { return k !== null && a.indexOf(k) === i; }
    ) as MapKey[];
    mapOrder.forEach(function(k) {
      const idx2 = ctx.nameIndex[k] || {};
      Object.keys(idx2).forEach(function(n) {
        if ((q === '' || n.toLowerCase().indexOf(q) !== -1) && !seen.has(n)) {
          seen.add(n); results.push({ name: n, map: k });
        }
      });
    });
    // Alphabetical within each map group keeps the full-list browse sane;
    // primary-map entries naturally sort first because they were seen first.
    results.sort(function(a, b) {
      const aPrimary = a.map === ctx.mapPrimary ? 0 : 1;
      const bPrimary = b.map === ctx.mapPrimary ? 0 : 1;
      if (aPrimary !== bPrimary) return aPrimary - bPrimary;
      return a.name.localeCompare(b.name);
    });
    return results;
  }

  // Focus (or click into) the empty search box → show the full scrollable
  // riding list so users can browse without knowing any names. The list
  // is capped only by the dropdown's own max-height + scroll.
  searchInput.addEventListener('focus', function() {
    if (searchInput.value.trim() === '') _renderResults(_collectResults(''));
  });

  searchInput.addEventListener('input', function() {
    const q = searchInput.value.trim().toLowerCase();
    _renderResults(_collectResults(q));
  });

  searchInput.addEventListener('keydown', function(e) {
    const items = _srItems();
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (searchResults!.style.display === 'none') return;
      _srHighlight(_srActive < 0 ? 0 : _srActive + 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (searchResults!.style.display === 'none') return;
      _srHighlight(_srActive <= 0 ? 0 : _srActive - 1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      const target = _srActive >= 0 ? items[_srActive] : (items.length === 1 ? items[0] : null);
      if (target) _srSelect(target);
    } else if (e.key === 'Escape') {
      searchInput.value = '';
      _closeDropdown();
    } else if (e.key === 'Tab') {
      _closeDropdown();
    }
  });

  document.addEventListener('click', function(e) {
    if (e.target !== searchInput && !searchResults!.contains(e.target as Node)) {
      _closeDropdown();
    }
  });
}
