// Alberta Electoral Boundary Audit — ED search
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wires the toolbar search input once at init. Internally self-contained after that.

import type { MapCtx, MapKey } from './types';
import { DOM_IDS } from './domIds';
import { awaitReady } from './readyState';

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

  searchInput.addEventListener('input', function() {
    const q = searchInput.value.trim().toLowerCase();
    searchResults!.innerHTML = '';
    _srActive = -1;
    if (q.length < 2) { searchResults!.style.display = 'none'; return; }
    const seen = new Set<string>();
    let results: Array<{ name: string; map: MapKey }> = [];
    const mapOrder = ([ctx.mapPrimary, 'minority', 'majority', '2019'] as Array<MapKey | null>).filter(
      function(k, i, a) { return k !== null && a.indexOf(k) === i; }
    ) as MapKey[];
    mapOrder.forEach(function(k) {
      const idx2 = ctx.nameIndex[k] || {};
      Object.keys(idx2).forEach(function(n) {
        if (n.toLowerCase().indexOf(q) !== -1 && !seen.has(n)) {
          seen.add(n); results.push({ name: n, map: k });
        }
      });
    });
    results = results.slice(0, 12);
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
        tag.textContent = r.map === '2019' ? '2019' : r.map === 'minority' ? 'Min' : 'Maj';
        li.appendChild(tag);
      }
      li.addEventListener('mousedown', function(e) { e.preventDefault(); });
      li.addEventListener('click', function(e) { e.stopPropagation(); _srSelect(li); });
      li.addEventListener('mouseover', function() {
        _srActive = _srItems().indexOf(li);
        _srItems().forEach(function(item) { item.classList.toggle('sr-active', item === li); });
      });
      searchResults!.appendChild(li);
    });
    searchResults.style.display = 'block';
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
      searchResults!.style.display = 'none';
      _srActive = -1;
    } else if (e.key === 'Tab') {
      searchResults!.style.display = 'none';
      _srActive = -1;
    }
  });

  document.addEventListener('click', function(e) {
    if (e.target !== searchInput && !searchResults!.contains(e.target as Node)) {
      searchResults!.style.display = 'none';
      _srActive = -1;
    }
  });
}
