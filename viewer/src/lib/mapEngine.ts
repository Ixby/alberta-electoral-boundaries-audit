// @ts-nocheck

export function init(basePath: string): void {
    // Pre-fetch all three hover datasets so cross-map comparison is available
      // immediately after the overlay opens, regardless of which map is active.
      let _edHover = null;                              // current map, keyed by id
      const _allHoverData = {};                         // key → {id: rec}
      const _nameIndex = {};                            // key → {name: rec}

      function _loadHoverJson(key, url) {
        fetch(url).then(r => r.json()).then(d => {
          const byId = {}, byName = {};
          d.forEach(rec => { byId[rec.id] = rec; byName[rec.name] = rec; });
          _allHoverData[key] = byId;
          _nameIndex[key] = byName;
          if (key === 'minority') _edHover = byId;
        }).catch(() => {});
      }
      _loadHoverJson('minority', 'data/ed_hover_minority.json');
      _loadHoverJson('majority', 'data/ed_hover_majority.json');
      _loadHoverJson('2019',    'data/ed_hover_2019.json');

      (function () {
        const navLinks = Array.from(document.querySelectorAll('nav a[href^="#"]'));
        const sections = navLinks
          .map(a => document.querySelector(a.getAttribute('href')))
          .filter(Boolean);

        function setActive(id) {
          navLinks.forEach(a => {
            a.classList.toggle('active', a.getAttribute('href') === '#' + id);
          });
        }

        const observer = new IntersectionObserver(entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) setActive(entry.target.id);
          });
        }, { rootMargin: '-50px 0px -60% 0px', threshold: 0 });

        sections.forEach(s => observer.observe(s));
      })();

      // ── Zoom viewer — inline SVG adoption (true infinite zoom, no tile ceiling)
      //    Primary: adopt SVG node from <object> contentDocument into main document.
      //    Secondary: XHR-parse and importNode (HTTP or Firefox file://).
      //    Tertiary fallback: img.width resize (Chrome file://).
      //
      //    Once inline, the browser renders SVG vector paths directly from the main
      //    document's paint record. ViewBox manipulation re-renders from paths at
      //    display resolution — no GPU tile rasterization limit at any zoom level.
      (function () {
        const overlay  = document.getElementById('zoom-overlay');
        const stage    = document.getElementById('zoom-stage');
        const obj      = document.getElementById('zoom-obj');
        const trigger  = document.getElementById('zoom-trigger');
        const closeBtn = document.getElementById('zoom-close');
        const zoomPct  = document.getElementById('zoom-pct');

        let mode = null, ready = false;  // 'viewbox' | 'fallback'

        // ── ViewBox state ─────────────────────────────────────────────────────
        let svgEl = null;
        let natVB = null;  // { x, y, w, h } — SVG's full coordinate space
        let curVB = null;

        // Cache stage rect so wheel/pointermove don't force synchronous layout.
        // Invalidated on open and resize.
        let _stageRect = null;
        function _getStageRect() {
          return _stageRect || (_stageRect = stage.getBoundingClientRect());
        }
        window.addEventListener('resize', () => { _stageRect = null; });
        if (window.ResizeObserver) {
          new ResizeObserver(() => { _stageRect = null; if (svgEl && mode === 'viewbox') _doSettle(); }).observe(stage);
        }

        function _renderBounds() {
          const r = _getStageRect();
          const sw = r.width, sh = r.height;
          const ar = natVB.w / natVB.h;
          let rw, rh;
          if (ar < sw / sh) { rh = sh; rw = sh * ar; }
          else               { rw = sw; rh = sw / ar; }
          return { rw, rh, ox: (sw - rw) / 2, oy: (sh - rh) / 2 };
        }

        // All gestures (drag, wheel, pinch) use CSS transform: translate+scale on
        // the SVG element — compositor-threaded, no SVG re-rasterization per frame.
        // settledVB = the viewBox actually rendered; curVB = logical destination.
        // After SETTLE_MS of no new gesture events, the viewBox attribute is
        // committed to curVB and the transform reset (one clean vector re-render).
        let _rafId = null, _pendingTx = 0, _pendingTy = 0, _pendingSx = 1;
        let settledVB = null, _settleTimer = null;
        const SETTLE_MS = 90;

        function _doSettle() {
          _settleTimer = null;
          if (!svgEl || !curVB) return;
          settledVB = null;
          if (_rafId !== null) { cancelAnimationFrame(_rafId); _rafId = null; }
          svgEl.style.transform = '';
          svgEl.style.willChange = '';
          svgEl.style.transformOrigin = '';
          svgEl.setAttribute('viewBox', `${curVB.x} ${curVB.y} ${curVB.w} ${curVB.h}`);
          if (zoomPct) zoomPct.textContent = Math.round(natVB.w / curVB.w * 100) + '%';
        }

        function applyVB(vb) {
          if (!settledVB) {
            // First change since last settle — snapshot current rendered position.
            settledVB = { ...curVB };
            if (svgEl) { svgEl.style.willChange = 'transform'; svgEl.style.transformOrigin = '0 0'; }
          }
          curVB = vb;
          // CSS transform: translate(tx,ty) scale(sx) maps settledVB rendering
          // to appear as curVB. With transform-origin:0 0:
          //   sx = settledVB.w / curVB.w
          //   tx = (settledVB.x - curVB.x)*rw/curVB.w + ox*(1 - 1/sx)
          const { rw, rh, ox, oy } = _renderBounds();
          const sx = settledVB.w / curVB.w;
          _pendingTx = (settledVB.x - curVB.x) * rw / curVB.w + ox * (1 - 1 / sx);
          _pendingTy = (settledVB.y - curVB.y) * rh / curVB.h + oy * (1 - 1 / sx);
          _pendingSx = sx;
          if (_rafId === null) {
            _rafId = requestAnimationFrame(() => {
              _rafId = null;
              if (svgEl) svgEl.style.transform =
                `translate(${_pendingTx}px,${_pendingTy}px) scale(${_pendingSx})`;
              if (zoomPct) zoomPct.textContent = Math.round(natVB.w / curVB.w * 100) + '%';
            });
          }
          if (_settleTimer !== null) clearTimeout(_settleTimer);
          _settleTimer = setTimeout(_doSettle, SETTLE_MS);
        }

        function resetVB() {
          if (_settleTimer !== null) { clearTimeout(_settleTimer); _settleTimer = null; }
          if (_rafId !== null) { cancelAnimationFrame(_rafId); _rafId = null; }
          settledVB = null;
          curVB = { ...natVB };
          if (svgEl) {
            svgEl.style.transform = '';
            svgEl.style.willChange = '';
            svgEl.style.transformOrigin = '';
            svgEl.setAttribute('viewBox', `${curVB.x} ${curVB.y} ${curVB.w} ${curVB.h}`);
          }
          if (zoomPct) zoomPct.textContent = '100%';
        }

        function vbZoomAt(mx, my, factor) {
          const { rw, rh, ox, oy } = _renderBounds();
          const lx = mx - ox, ly = my - oy;
          const svgX = curVB.x + (lx / rw) * curVB.w;
          const svgY = curVB.y + (ly / rh) * curVB.h;
          const newW = Math.max(natVB.w / 1000, Math.min(natVB.w * 20, curVB.w / factor));
          const newH = newW * (natVB.h / natVB.w);
          applyVB({ x: svgX - (lx / rw) * newW, y: svgY - (ly / rh) * newH, w: newW, h: newH });
        }

        function vbPanBy(dx, dy) {
          const { rw, rh } = _renderBounds();
          applyVB({ x: curVB.x - (dx / rw) * curVB.w, y: curVB.y - (dy / rh) * curVB.h, w: curVB.w, h: curVB.h });
        }

        function _activateInlineSVG(node, preserveVB) {
          node.setAttribute('width', '100%');
          node.setAttribute('height', '100%');
          node.setAttribute('preserveAspectRatio', 'xMidYMid meet');
          node.style.cssText = 'position:absolute;left:0;top:0;display:block;touch-action:none;';
          const _cur = (svgEl && svgEl.parentNode === stage) ? svgEl
                     : (obj.parentNode === stage)             ? obj
                     : null;
          if (_cur) stage.replaceChild(node, _cur);
          else stage.appendChild(node);

          // ed_hover_layer paths have fill:none, so pointer-events defaults to none.
          // Set pointer-events:all so elementFromPoint hits them for click/hover.
          const _hoverLayer = node.querySelector('#ed_hover_layer');
          if (_hoverLayer) _hoverLayer.style.pointerEvents = 'all';

          const vb = node.viewBox.baseVal;
          if (vb.width && vb.height) {
            natVB = { x: vb.x, y: vb.y, w: vb.width, h: vb.height };
          } else {
            const w = parseFloat(node.getAttribute('width'))  || 432;
            const h = parseFloat(node.getAttribute('height')) || 648;
            natVB = { x: 0, y: 0, w, h };
            node.setAttribute('viewBox', `0 0 ${w} ${h}`);
          }
          curVB = { ...natVB };
          svgEl = node;
          mode = 'viewbox';
          ready = true;
          _applyBoundaryColor(node, _mapPrimary);
          _reapplyLayers();
          _syncOverlays();
          if (overlay.style.display !== 'none') {
            if (preserveVB) {
              // Restore saved view without resetting to full province
              if (_settleTimer !== null) { clearTimeout(_settleTimer); _settleTimer = null; }
              if (_rafId !== null) { cancelAnimationFrame(_rafId); _rafId = null; }
              settledVB = null;
              curVB = { ...preserveVB };
              svgEl.style.transform = '';
              svgEl.style.willChange = '';
              svgEl.style.transformOrigin = '';
              svgEl.setAttribute('viewBox', `${curVB.x} ${curVB.y} ${curVB.w} ${curVB.h}`);
              if (zoomPct) zoomPct.textContent = Math.round(natVB.w / curVB.w * 100) + '%';
            } else {
              resetVB();
            }
          }
        }

        // ── Fallback state ────────────────────────────────────────────────────
        let fbImg = null, fbNatW = 0, fbNatH = 0, fbScale = 1, fbTx = 0, fbTy = 0;

        function applyFallback() {
          const w = Math.max(1, Math.round(fbNatW * fbScale));
          const h = Math.max(1, Math.round(fbNatH * fbScale));
          fbImg.width = w; fbImg.height = h;
          fbImg.style.left = Math.round(fbTx) + 'px';
          fbImg.style.top  = Math.round(fbTy) + 'px';
          if (zoomPct) zoomPct.textContent = Math.round(fbScale * 100) + '%';
        }

        function resetFallback() {
          const sw = stage.offsetWidth, sh = stage.offsetHeight;
          fbScale = Math.min(sw / fbNatW, sh / fbNatH) * 0.94;
          fbTx = (sw - fbNatW * fbScale) / 2;
          fbTy = (sh - fbNatH * fbScale) / 2;
          applyFallback();
        }

        function initFallback() {
          mode = 'fallback';
          fbImg = document.createElement('img');
          fbImg.src = obj.data; fbImg.alt = obj.title; fbImg.draggable = false;
          fbImg.style.cssText = 'position:absolute;display:block;user-select:none;pointer-events:none;';
          stage.replaceChild(fbImg, obj);
          function onLoad() {
            fbNatW = fbImg.naturalWidth || 600; fbNatH = fbImg.naturalHeight || 900;
            ready = true;
            if (overlay.style.display !== 'none') resetFallback();
          }
          if (fbImg.complete && fbImg.naturalWidth) onLoad();
          else fbImg.onload = onLoad;
        }

        // ── Initialisation ────────────────────────────────────────────────────
        function _xhrFallback() {
          // Try XHR inline injection (works over HTTP or Firefox file://)
          try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', obj.data, true);
            xhr.onload = () => {
              if (xhr.status === 200 || xhr.status === 0) {
                const doc = new DOMParser().parseFromString(xhr.responseText, 'image/svg+xml');
                const root = doc.documentElement;
                if (root && root.tagName.toLowerCase() !== 'parsererror') {
                  _activateInlineSVG(document.importNode(root, true));
                  return;
                }
              }
              initFallback();
            };
            xhr.onerror = initFallback;
            xhr.send();
          } catch (e) { initFallback(); }
        }

        function tryInit() {
          if (ready) return;
          // Primary: adopt the already-parsed SVG from the object's nested document.
          // replaceChild implicitly adopts the node — no re-download, no re-parse.
          const doc = obj.contentDocument || (obj.getSVGDocument && obj.getSVGDocument());
          if (doc && doc.documentElement && doc.documentElement.tagName.toLowerCase() === 'svg') {
            _activateInlineSVG(doc.documentElement);
            return;
          }
          // Secondary: XHR then importNode
          _xhrFallback();
        }

        obj.addEventListener('load', tryInit);
        if (obj.contentDocument && obj.contentDocument.readyState === 'complete') tryInit();

        // ── Open / close ──────────────────────────────────────────────────────
        function open() {
          _stageRect = null;  // stage may have reflowed since last open
          overlay.style.display = 'block';
          document.body.style.overflow = 'hidden';
          if (!ready) return;
          if (mode === 'viewbox') resetVB(); else resetFallback();
        }

        function close() {
          overlay.style.display = 'none';
          document.body.style.overflow = '';
          _hideTip();
          _hideCallout();
        }

        trigger.addEventListener('click', e => { e.preventDefault(); open(); });
        closeBtn.addEventListener('click', close);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
        overlay.addEventListener('click', e => { if (e.target === overlay) close(); });

        // ── Zoom ──────────────────────────────────────────────────────────────
        function zoomAt(mx, my, factor) {
          if (!ready) return;
          if (mode === 'viewbox') {
            vbZoomAt(mx, my, factor);
          } else {
            const newScale = Math.min(Math.max(fbScale * factor, 0.05), 500);
            const ratio = newScale / fbScale;
            fbTx = mx - ratio * (mx - fbTx);
            fbTy = my - ratio * (my - fbTy);
            fbScale = newScale;
            applyFallback();
          }
        }

        stage.addEventListener('wheel', e => {
          e.preventDefault();
          const r = _getStageRect();
          zoomAt(e.clientX - r.left, e.clientY - r.top, Math.pow(0.88, e.deltaY / 100));
        }, { passive: false });

        // ── Tooltip helpers ───────────────────────────────────────────────────
        const _tip = document.getElementById('ed-tooltip');

        function _showTip(d, x, y) {
          if (!d) return;
          _tip.innerHTML =
            `<strong>${d.name}</strong>` +
            `UCP&nbsp;${d.ucp_pct}%&nbsp;&nbsp;NDP&nbsp;${d.ndp_pct}%` +
            (d.votes ? `<br>${d.votes.toLocaleString()}&nbsp;votes&nbsp;(2023)` : '') +
            (d.pop   ? `<br>Pop.&nbsp;${d.pop.toLocaleString()}` : '');
          _tip.style.display = 'block';
          const pad = 14, tw = _tip.offsetWidth, th = _tip.offsetHeight;
          let lx = x + pad, ly = y + pad;
          if (lx + tw > window.innerWidth)  lx = x - tw - pad;
          if (ly + th > window.innerHeight) ly = y - th - pad;
          _tip.style.left = lx + 'px';
          _tip.style.top  = ly + 'px';
        }

        function _hideTip() { _tip.style.display = 'none'; }

        // ── Touch callout (bottom panel on tap) ───────────────────────────────
        const _callout = document.getElementById('ed-callout');
        function _showCallout(d) {
          if (!d) return;
          document.getElementById('ec-name').textContent = d.name;
          document.getElementById('ec-ucp-bar').style.width = d.ucp_pct + '%';
          document.getElementById('ec-ndp-bar').style.width = d.ndp_pct + '%';
          document.getElementById('ec-ucp-pct').textContent = d.ucp_pct + '%';
          document.getElementById('ec-ndp-pct').textContent = d.ndp_pct + '%';
          document.getElementById('ec-ucp-votes').textContent = d.ucp_votes ? d.ucp_votes.toLocaleString() + ' votes' : '';
          document.getElementById('ec-ndp-votes').textContent = d.ndp_votes ? d.ndp_votes.toLocaleString() + ' votes' : '';
          document.getElementById('ec-total-votes').textContent = d.votes ? d.votes.toLocaleString() + ' total votes' : '';
          document.getElementById('ec-va-count').textContent = d.va_count ? d.va_count + ' voting areas' : '';
          const popN = d.pop ? Math.round(d.pop / 100) * 100 : 0;
          document.getElementById('ec-pop').textContent = popN ? 'Pop. ' + popN.toLocaleString() : '';
          // Cross-map comparison
          const cmpEl = document.getElementById('ec-compare');
          if (cmpEl) {
            const others = ['minority', 'majority', '2019'].filter(k => k !== _mapPrimary);
            const parts = others.map(k => {
              const rec = _nameIndex[k] && _nameIndex[k][d.name];
              if (!rec) return null;
              const label = k === 'minority' ? 'Min.' : k === 'majority' ? 'Maj.' : '2019';
              const w = rec.ucp_pct > rec.ndp_pct
                ? '<span class="ec-cmp-val">UCP ' + rec.ucp_pct + '%</span>'
                : '<span class="ec-cmp-val">NDP ' + rec.ndp_pct + '%</span>';
              return '<span class="ec-cmp-item"><span class="ec-cmp-label">' + label + '</span>' + w + '</span>';
            }).filter(Boolean);
            if (parts.length) {
              cmpEl.innerHTML = '<span class="ec-cmp-header">Other maps</span>' + parts.join('');
              cmpEl.style.display = 'flex';
            } else {
              cmpEl.innerHTML = '<span class="ec-cmp-unique">Boundary unique to this map</span>';
              cmpEl.style.display = 'flex';
            }
          }
          _selectedEdName = d.name;
          _callout.classList.add('ec-visible');
        }
        function _hideCallout() {
          if (_rafId !== null) { cancelAnimationFrame(_rafId); _rafId = null; }
          _callout.classList.remove('ec-visible');
          _selectedEdName = null;
          _clearEdHighlight();
        }

        // ── Map selector ──────────────────────────────────────────────────────────
        const _mapSvgUrls = {
          minority: `${basePath}/images/cover_art_minority_hires.svg`,
          majority: `${basePath}/images/cover_art_majority_hires.svg`,
          '2019':   `${basePath}/images/cover_art_2019_hires.svg`,
        };
        const _mapJsonUrls = {
          minority: 'data/ed_hover_minority.json',
          majority: 'data/ed_hover_majority.json',
          '2019':   'data/ed_hover_2019.json',
        };
        const _mapContextLabels = {
          minority: '2026 minority proposal · 2023 election results',
          majority: '2026 majority proposal · 2023 election results',
          '2019':   '2019 enacted boundaries · 2023 election results',
        };
        const _mapAccentColors = {
          minority: '#6B35A7',
          majority: '#1A7A6E',
          '2019':   '#aaaaaa',
        };
        const _mapOn      = { minority: true, majority: false, '2019': false };
        let   _mapPrimary = 'minority';
        const _svgCache   = {};
        const _overlayInSvg = {};
        const _layerState = { vote: true, 'ed-fill': true, 'ed-lines': true };
        let   _mapLocked  = false;

        // ── Map-wide boundary color ───────────────────────────────────────────────
        function _applyBoundaryColor(svgNode, mapKey) {
          if (!svgNode) return;
          const color = _mapAccentColors[mapKey] || '#555';
          const g = svgNode.querySelector('#ed_boundary_layer');
          if (!g) { console.warn('[map] ed_boundary_layer not found in SVG'); return; }
          g.querySelectorAll('path').forEach(p => p.setAttribute('stroke', color));
        }

        // ── Active ED boundary highlight ──────────────────────────────────────────
        let _selectedEdName = null;
        let _highlightPath = null;
        function _setEdHighlight(pathEl) {
          _clearEdHighlight();
          if (!svgEl || !pathEl) return;
          const color = _mapAccentColors[_mapPrimary] || '#fff';
          const d = pathEl.getAttribute('d');
          _highlightPath = document.createElementNS('http://www.w3.org/2000/svg', 'g');
          _highlightPath.setAttribute('pointer-events', 'none');
          const glow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          glow.setAttribute('d', d);
          glow.setAttribute('fill', 'none');
          glow.setAttribute('stroke', color);
          glow.setAttribute('stroke-width', '9');
          glow.setAttribute('stroke-linejoin', 'round');
          glow.style.vectorEffect = 'non-scaling-stroke';
          glow.style.opacity = '0.3';
          glow.style.filter = 'drop-shadow(0 0 5px ' + color + ')';
          const sharp = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          sharp.setAttribute('d', d);
          sharp.setAttribute('fill', 'none');
          sharp.setAttribute('stroke', color);
          sharp.setAttribute('stroke-width', '3.5');
          sharp.setAttribute('stroke-linejoin', 'round');
          sharp.style.vectorEffect = 'non-scaling-stroke';
          _highlightPath.appendChild(glow);
          _highlightPath.appendChild(sharp);
          svgEl.appendChild(_highlightPath);
        }
        function _clearEdHighlight() {
          if (_highlightPath) { _highlightPath.remove(); _highlightPath = null; }
        }
        function _activateCenterED() {
          if (_mapLocked || !svgEl || !_edHover || !curVB) return;
          const cx = curVB.x + curVB.w / 2, cy = curVB.y + curVB.h / 2;
          let bestPath = null, bestDist = Infinity;
          svgEl.querySelectorAll('[data-ed-id]').forEach(p => {
            const bb = p.getBBox();
            const dist = Math.hypot(bb.x + bb.width / 2 - cx, bb.y + bb.height / 2 - cy);
            if (dist < bestDist) { bestDist = dist; bestPath = p; }
          });
          if (!bestPath) return;
          const rec = _edHover[parseInt(bestPath.getAttribute('data-ed-id'), 10)];
          if (rec) { _showCallout(rec); _setEdHighlight(bestPath); }
        }

        // ── Map overlay system ─────────────────────────────────────────────────────

        function _extractBoundaryGroup(key) {
          var doc = _svgCache[key];
          if (!doc) return null;
          var g = doc.querySelector('#ed_boundary_layer');
          if (!g) return null;
          var clone = document.importNode(g, true);
          clone.querySelectorAll('path').forEach(function(p) {
            p.setAttribute('stroke', _mapAccentColors[key] || '#555');
          });
          clone.setAttribute('pointer-events', 'none');
          clone.id = 'ed-boundary-overlay-' + key;
          return clone;
        }

        function _syncOverlays() {
          ['minority', 'majority', '2019'].forEach(function(key) {
            if (!_mapOn[key] || key === _mapPrimary) {
              if (_overlayInSvg[key]) { _overlayInSvg[key].remove(); _overlayInSvg[key] = null; }
              return;
            }
            if (!_overlayInSvg[key] && svgEl) _fetchAndOverlay(key);
          });
        }

        function _fetchAndOverlay(key) {
          function apply() {
            if (!_mapOn[key] || key === _mapPrimary || !svgEl) return;
            var g = _extractBoundaryGroup(key);
            if (g) { svgEl.appendChild(g); _overlayInSvg[key] = g; }
          }
          if (_svgCache[key]) { apply(); return; }
          fetch(_mapSvgUrls[key]).then(function(r) { return r.text(); }).then(function(text) {
            _svgCache[key] = new DOMParser().parseFromString(text, 'image/svg+xml');
            apply();
          }).catch(function() {});
        }

        function _updateMapButtons() {
          document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
            var key = b.dataset.map;
            b.classList.toggle('tb-map-primary', _mapOn[key] && key === _mapPrimary);
            b.classList.toggle('tb-map-overlay',  _mapOn[key] && key !== _mapPrimary);
          });
        }

        function _doSwitchPrimary(key) {
          var ctxEl = document.getElementById('ec-context');
          if (ctxEl) ctxEl.textContent = _mapContextLabels[key];
          var savedName = _selectedEdName;
          _hideCallout();
          _edHover = null;
          var savedVB = curVB ? Object.assign({}, curVB) : null;
          ready = false;
          stage.style.opacity = '0.45';
          stage.style.transition = 'opacity 0.15s';
          fetch(_mapSvgUrls[key])
            .then(function(r) { return r.text(); })
            .then(function(text) {
              var doc = new DOMParser().parseFromString(text, 'image/svg+xml');
              _svgCache[key] = doc;
              var root = doc.documentElement;
              if (root && root.tagName.toLowerCase() !== 'parsererror') {
                _activateInlineSVG(document.importNode(root, true), savedVB);
                if (_allHoverData[key] && Object.keys(_allHoverData[key]).length) {
                  _edHover = _allHoverData[key];
                }
                if (savedName) {
                  var rec = _nameIndex[key] && _nameIndex[key][savedName];
                  if (rec) {
                    var path = svgEl && svgEl.querySelector('[data-ed-id="' + rec.id + '"]');
                    if (path) { _showCallout(rec); _setEdHighlight(path); }
                  } else { _activateCenterED(); }
                } else { _activateCenterED(); }
              } else { ready = true; }
              stage.style.opacity = '';
              setTimeout(function() { stage.style.transition = ''; }, 200);
            })
            .catch(function() {
              ready = true;
              stage.style.opacity = '';
              setTimeout(function() { stage.style.transition = ''; }, 200);
            });
          fetch(_mapJsonUrls[key])
            .then(function(r) { return r.json(); })
            .then(function(d) {
              var byId = {}, byName = {};
              d.forEach(function(rec) { byId[rec.id] = rec; byName[rec.name] = rec; });
              _allHoverData[key] = byId;
              _nameIndex[key] = byName;
              _edHover = byId;
              if (_layerState['ed-fill']) _applyEdFillLayer(true);
            })
            .catch(function() { _edHover = null; });
        }

        function toggleMap(key) {
          if (!_mapSvgUrls[key]) return;
          if (_mapOn[key]) {
            if (key === _mapPrimary) {
              var next = ['minority', 'majority', '2019'].find(function(k) { return k !== key && _mapOn[k]; });
              if (!next) return;
              _mapOn[key] = false;
              if (_overlayInSvg[key]) { _overlayInSvg[key].remove(); _overlayInSvg[key] = null; }
              _mapPrimary = next;
              _doSwitchPrimary(next);
            } else {
              _mapOn[key] = false;
              if (_overlayInSvg[key]) { _overlayInSvg[key].remove(); _overlayInSvg[key] = null; }
            }
          } else {
            _mapOn[key] = true;
            _mapPrimary = key;
            _doSwitchPrimary(key);
          }
          _updateMapButtons();
        }

        document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
          b.addEventListener('click', function() { toggleMap(b.dataset.map); });
        });

        document.getElementById('ec-close').addEventListener('click', _hideCallout);

        // ── Layer panel ────────────────────────────────────────────────────────────

        function _applyVoteLayer(on) {
          if (!svgEl) return;
          var g = svgEl.querySelector('#PatchCollection_1');
          if (g) g.style.display = on ? '' : 'none';
        }
        function _applyEdFillLayer(on) {
          if (!svgEl || !_edHover) return;
          var g = svgEl.querySelector('#ed_hover_layer');
          if (!g) return;
          g.querySelectorAll('[data-ed-id]').forEach(function(p) {
            if (on) {
              var id = parseInt(p.getAttribute('data-ed-id'), 10);
              var rec = _edHover[id];
              if (rec) {
                var isUCP = rec.ucp_pct >= rec.ndp_pct;
                var pct = Math.max(rec.ucp_pct, rec.ndp_pct);
                var a = (0.15 + Math.min((pct - 50) / 35, 1) * 0.5).toFixed(2);
                p.style.fill = isUCP ? 'rgba(20,46,148,' + a + ')' : 'rgba(232,99,16,' + a + ')';
              }
            } else { p.style.fill = ''; }
          });
        }
        function _applyEdLinesLayer(on) {
          if (!svgEl) return;
          var g = svgEl.querySelector('#ed_boundary_layer');
          if (g) g.style.display = on ? '' : 'none';
          Object.keys(_overlayInSvg).forEach(function(k) {
            var og = _overlayInSvg[k];
            if (og) og.style.display = on ? '' : 'none';
          });
        }
        function _reapplyLayers() {
          _applyVoteLayer(_layerState.vote);
          _applyEdFillLayer(_layerState['ed-fill']);
          _applyEdLinesLayer(_layerState['ed-lines']);
        }

        document.querySelectorAll('.tb-btn[data-layer]').forEach(function(b) {
          b.addEventListener('click', function() {
            var key = b.dataset.layer;
            if (key === 'lock') {
              _mapLocked = !_mapLocked;
              b.classList.toggle('tb-layer-on', _mapLocked);
              return;
            }
            var on = !_layerState[key];
            _layerState[key] = on;
            b.classList.toggle('tb-layer-on', on);
            if (key === 'vote')     _applyVoteLayer(on);
            if (key === 'ed-fill')  _applyEdFillLayer(on);
            if (key === 'ed-lines') _applyEdLinesLayer(on);
          });
        });

        // ── Snap-to-ED animation ───────────────────────────────────────────────
        function _animateToVB(targetVB, dur) {
          if (_mapLocked) return;
          if (_settleTimer !== null) { clearTimeout(_settleTimer); _settleTimer = null; }
          if (_rafId !== null) { cancelAnimationFrame(_rafId); _rafId = null; }
          const startVB = { ...curVB };
          if (!settledVB) {
            settledVB = { ...curVB };
            svgEl.style.willChange = 'transform';
            svgEl.style.transformOrigin = '0 0';
          }
          const t0 = performance.now();
          function step(now) {
            const t = Math.min((now - t0) / dur, 1);
            const ease = t < 0.5 ? 2*t*t : -1 + (4 - 2*t)*t;
            curVB = {
              x: startVB.x + (targetVB.x - startVB.x) * ease,
              y: startVB.y + (targetVB.y - startVB.y) * ease,
              w: startVB.w + (targetVB.w - startVB.w) * ease,
              h: startVB.h + (targetVB.h - startVB.h) * ease,
            };
            const { rw, rh, ox, oy } = _renderBounds();
            const sx = settledVB.w / curVB.w;
            svgEl.style.transform =
              `translate(${(settledVB.x - curVB.x)*rw/curVB.w + ox*(1-1/sx)}px,` +
              `${(settledVB.y - curVB.y)*rh/curVB.h + oy*(1-1/sx)}px) scale(${sx})`;
            if (zoomPct) zoomPct.textContent = Math.round(natVB.w / curVB.w * 100) + '%';
            if (t < 1) { requestAnimationFrame(step); }
            else { _settleTimer = setTimeout(_doSettle, SETTLE_MS); }
          }
          requestAnimationFrame(step);
        }

        function _snapToED(pathEl) {
          if (!svgEl || mode !== 'viewbox') return;
          const bb = pathEl.getBBox();
          const pad = Math.max(bb.width, bb.height) * 0.35;
          let tw = bb.width + pad * 2, th = bb.height + pad * 2;
          const r = _getStageRect();
          if (tw / th < r.width / r.height) tw = th * r.width / r.height;
          else th = tw * r.height / r.width;
          const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
          _animateToVB({ x: cx - tw/2, y: cy - th/2, w: tw, h: th }, 280);
        }

        function _tipTarget(e) {
          // pointer capture redirects e.target to the stage during drag/touch,
          // so use elementFromPoint which hits the actual SVG path under the finger.
          const el = document.elementFromPoint(e.clientX, e.clientY);
          return el && el.closest ? el.closest('[data-ed-id]') : null;
        }

        // ── Unified drag + tap + pinch (Pointer Events — all gesture types) ──────
        let drag = null, _dragMoved = false;
        const _ptrs = new Map();
        let _lastPinchDist = null, _lastPinchMid = null;

        function _ptrMid() {
          const [a, b] = [..._ptrs.values()];
          return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
        }
        function _ptrDist() {
          const [a, b] = [..._ptrs.values()];
          return Math.hypot(a.x - b.x, a.y - b.y);
        }

        stage.addEventListener('pointerdown', e => {
          if (!ready) return;
          if (e.pointerType === 'mouse' && e.button !== 0) return;
          _ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
          try { stage.setPointerCapture(e.pointerId); } catch (_) {}
          if (_ptrs.size === 2) {
            if (drag) { drag = null; stage.classList.remove('dragging'); }
            _hideTip();
            _lastPinchDist = _ptrDist();
            _lastPinchMid = _ptrMid();
            return;
          }
          if (_ptrs.size > 2) return;
          drag = { cx: e.clientX, cy: e.clientY, startX: e.clientX, startY: e.clientY, id: e.pointerId };
          _dragMoved = false;
          stage.classList.add('dragging');
        });

        stage.addEventListener('pointermove', e => {
          if (!ready || !_ptrs.has(e.pointerId)) return;
          _ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });

          if (_ptrs.size >= 2) {
            const dist = _ptrDist(), mid = _ptrMid(), r = _getStageRect();
            if (_lastPinchDist && dist > 0) zoomAt(mid.x - r.left, mid.y - r.top, dist / _lastPinchDist);
            if (_lastPinchMid) {
              if (mode === 'viewbox') vbPanBy(mid.x - _lastPinchMid.x, mid.y - _lastPinchMid.y);
              else { fbTx += mid.x - _lastPinchMid.x; fbTy += mid.y - _lastPinchMid.y;
                     fbImg.style.left = Math.round(fbTx) + 'px'; fbImg.style.top = Math.round(fbTy) + 'px'; }
            }
            _lastPinchDist = dist; _lastPinchMid = mid;
            return;
          }

          if (e.pointerType !== 'touch' && !drag && mode === 'viewbox' && _edHover) {
            const hit = _tipTarget(e);
            if (hit) _showTip(_edHover[parseInt(hit.getAttribute('data-ed-id'), 10)], e.clientX, e.clientY);
            else _hideTip();
          }
          if (!drag || drag.id !== e.pointerId) return;
          const dx = e.clientX - drag.cx, dy = e.clientY - drag.cy;
          if (!_dragMoved && Math.hypot(e.clientX - drag.startX, e.clientY - drag.startY) < 6) return;
          if (!_dragMoved) { _dragMoved = true; _hideTip(); }
          drag.cx = e.clientX; drag.cy = e.clientY;
          if (mode === 'viewbox') vbPanBy(dx, dy);
          else { fbTx += dx; fbTy += dy; fbImg.style.left = Math.round(fbTx) + 'px'; fbImg.style.top = Math.round(fbTy) + 'px'; }
        });

        let _lastTap = 0;

        stage.addEventListener('pointerup', e => {
          _ptrs.delete(e.pointerId);
          try { stage.releasePointerCapture(e.pointerId); } catch (_) {}
          if (_ptrs.size < 2) { _lastPinchDist = null; _lastPinchMid = null; }
          if (!drag || drag.id !== e.pointerId) return;
          stage.classList.remove('dragging');
          if (!_dragMoved && mode === 'viewbox') {
            if (e.pointerType === 'touch') {
              const now = performance.now();
              if (now - _lastTap < 300) {
                _hideCallout();
                _animateToVB({ ...natVB }, 280);
                _lastTap = 0;
              } else {
                _lastTap = now;
                if (_edHover) {
                  const hit = _tipTarget(e);
                  if (hit) {
                    _showCallout(_edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
                    _setEdHighlight(hit);
                    _snapToED(hit);
                  } else _hideCallout();
                }
              }
            } else if (_edHover) {
              const hit = _tipTarget(e);
              if (hit) {
                _hideTip();
                _showCallout(_edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
                _setEdHighlight(hit);
                if (!_mapLocked) _snapToED(hit);
              } else {
                _hideCallout();
              }
            }
          }
          drag = null;
        });

        stage.addEventListener('pointercancel', e => {
          _ptrs.delete(e.pointerId);
          if (drag && drag.id === e.pointerId) { drag = null; stage.classList.remove('dragging'); }
          if (_ptrs.size < 2) { _lastPinchDist = null; _lastPinchMid = null; }
        });

        stage.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch') _hideTip(); });

        stage.addEventListener('dblclick', () => {
          if (!ready) return;
          if (mode === 'viewbox') _animateToVB({ ...natVB }, 280); else resetFallback();
        });
      })();
}
