// @ts-nocheck
// Alberta Electoral Boundary Audit — ED search
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Wires the toolbar search input once at init. Internally self-contained after that.
// deps: showCallout, setEdHighlight, snapToED, updateMapButtons, doSwitchPrimary.

import type { MapCtx } from './types';
import { DOM_IDS } from './domIds';

export function initSearch(ctx: MapCtx, deps): void {
  const { showCallout, setEdHighlight, snapToED, updateMapButtons, doSwitchPrimary } = deps;

  const searchInput   = document.getElementById(DOM_IDS.tbSearch);
  const searchResults = document.getElementById(DOM_IDS.tbSearchResults);
  if (!searchInput || !searchResults) return;

  let _srActive = -1;

  function _srItems() {
    return Array.from(searchResults.querySelectorAll('li'));
  }

  function _srHighlight(newIdx) {
    var items = _srItems();
    if (!items.length) return;
    _srActive = Math.max(0, Math.min(items.length - 1, newIdx));
    items.forEach(function(li, i) { li.classList.toggle('sr-active', i === _srActive); });
    items[_srActive].scrollIntoView({ block: 'nearest' });
  }

  function _srSelect(li) {
    if (!li) return;
    var name = li.dataset.edName || li.textContent.replace(/\s*(Min|Maj|2019)$/, '').trim();
    var fromMap = li.dataset.edMap || ctx.mapPrimary;
    searchInput.value = name;
    searchResults.style.display = 'none';
    _srActive = -1;
    if (!ctx.svgEl) return;

    function navigateToEd(mapKey, edName) {
      var idx2 = ctx.nameIndex[mapKey] || {};
      var rec2 = idx2[edName];
      if (!rec2) return;
      var path = ctx.svgEl && ctx.svgEl.querySelector('#ed_hover_layer path[data-ed-id="' + rec2.id + '"]');
      if (path) { showCallout(rec2); setEdHighlight(path); if (!ctx.mapLocked) snapToED(path, true); }
    }

    if (fromMap !== ctx.mapPrimary) {
      ctx.mapOn[fromMap] = true;
      ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== fromMap; });
      ctx.mapActivationOrder.push(fromMap);
      ctx.mapPrimary = fromMap;
      updateMapButtons();
      doSwitchPrimary(fromMap);
      var _pendingName = name, _waitAttempts = 0;
      (function waitAndNav() {
        if (!ctx.svgEl || !ctx.ready) {
          if (++_waitAttempts < 30) { setTimeout(waitAndNav, 150); return; }
          return;
        }
        navigateToEd(fromMap, _pendingName);
      })();
    } else {
      navigateToEd(ctx.mapPrimary, name);
    }
  }

  searchInput.addEventListener('input', function() {
    var q = searchInput.value.trim().toLowerCase();
    searchResults.innerHTML = '';
    _srActive = -1;
    if (q.length < 2) { searchResults.style.display = 'none'; return; }
    var seen = new Set(), results = [];
    var mapOrder = [ctx.mapPrimary, 'minority', 'majority', '2019'].filter(
      function(k, i, a) { return a.indexOf(k) === i; }
    );
    mapOrder.forEach(function(k) {
      var idx2 = ctx.nameIndex[k] || {};
      Object.keys(idx2).forEach(function(n) {
        if (n.toLowerCase().indexOf(q) !== -1 && !seen.has(n)) {
          seen.add(n); results.push({ name: n, map: k });
        }
      });
    });
    results = results.slice(0, 12);
    if (!results.length) { searchResults.style.display = 'none'; return; }
    results.forEach(function(r) {
      var li = document.createElement('li');
      li.dataset.edName = r.name;
      li.dataset.edMap = r.map;
      var nameSpan = document.createElement('span');
      nameSpan.textContent = r.name;
      li.appendChild(nameSpan);
      if (r.map !== ctx.mapPrimary) {
        var tag = document.createElement('span');
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
      searchResults.appendChild(li);
    });
    searchResults.style.display = 'block';
  });

  searchInput.addEventListener('keydown', function(e) {
    var items = _srItems();
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (searchResults.style.display === 'none') return;
      _srHighlight(_srActive < 0 ? 0 : _srActive + 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (searchResults.style.display === 'none') return;
      _srHighlight(_srActive <= 0 ? 0 : _srActive - 1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var target = _srActive >= 0 ? items[_srActive] : (items.length === 1 ? items[0] : null);
      if (target) _srSelect(target);
    } else if (e.key === 'Escape') {
      searchInput.value = '';
      searchResults.style.display = 'none';
      _srActive = -1;
    } else if (e.key === 'Tab') {
      searchResults.style.display = 'none';
      _srActive = -1;
    }
  });

  document.addEventListener('click', function(e) {
    if (e.target !== searchInput && !searchResults.contains(e.target)) {
      searchResults.style.display = 'none';
      _srActive = -1;
    }
  });
}
