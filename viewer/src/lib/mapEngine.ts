﻿// Alberta Electoral Boundary Audit — map engine
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
// @ts-nocheck

import { initNavScrollspy } from './mapEngine/navScrollspy';
import { initIntroModal }   from './mapEngine/introModal';
import { hasSeenIntro }     from './prefs';
import { applyVoteLayer, applyEdFillLayer, applyEdLinesLayer, applyEGLayer, reapplyLayers, setLayerOn } from './mapEngine/layers';
import { showTip, hideTip, showCallout, hideCallout, setEdHighlight, clearEdHighlight, activateCenterED, tipTarget, isEdVisible, snapToED, zoomEdTo70 } from './mapEngine/edInteraction';
import { initSearch } from './mapEngine/search';
import { applyAnomalyHighlight, initAnomalyButtons } from './mapEngine/anomaly';
import { initNamedEdButtons } from './mapEngine/namedEdZoom';

let _onEvent      = null;
let _getState     = null;
let _applyStateFn = null;

export function onEvent(cb)                                 { _onEvent = cb; }
export function getState()                                  { return _getState ? _getState() : null; }
export function applyState(primary, mapOn, layers)          { if (_applyStateFn) _applyStateFn(primary, mapOn, layers); }

export function init(basePath: string): void {
    initNavScrollspy();

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
        const _zoomSlider = document.getElementById('zoom-slider');
        function _updateZoomDisplay(pct) {
          if (zoomPct) zoomPct.textContent = pct + '%';
          if (_zoomSlider) _zoomSlider.value = String(Math.min(3000, Math.max(25, pct)));
        }

        // ── Shared mutable state ──────────────────────────────────────────────────
        const ctx = {
          // SVG load mode
          mode:               null,       // 'viewbox' | 'fallback' | null
          ready:              false,

          // Viewport
          svgEl:              null,
          natVB:              null,       // { x, y, w, h } — SVG full coordinate space
          curVB:              null,
          settledVB:          null,

          // Stage rect cache (invalidated on open/resize)
          stageRect:          null,

          // RAF / CSS-transform animation
          rafId:              null,
          pendingTx:          0,
          pendingTy:          0,
          pendingSx:          1,
          settleTimer:        null,

          // Fallback image state
          fbImg:              null,
          fbNatW:             0,
          fbNatH:             0,
          fbScale:            1,
          fbTx:               0,
          fbTy:               0,

          // Focus management (overlay open/close)
          prevFocus:          null,

          // Map selector state
          mapOn:              { minority: false, majority: false, '2019': true },
          mapPrimary:         '2019',
          mapActivationOrder: ['2019'],
          svgCache:           {},
          overlayInSvg:       {},
          layerState:         { vote: true, 'ed-fill': false, 'ed-lines': true, eg: false },
          mapLocked:          false,

          // ED hover data (pre-fetched at init)
          edHover:            null,       // current-map records keyed by id
          allHoverData:       {},         // mapKey → { id: rec }
          nameIndex:          {},         // mapKey → { name: rec }

          // ED selection
          selectedEdName:     null,
          highlightPath:      null,

          // Anomaly highlight
          anomalyOn:          false,
          anomalyOverlay:     null,

          // Gesture state
          drag:               null,
          dragMoved:          false,
          ptrs:               new Map(),
          lastPinchDist:      null,
          lastPinchMid:       null,
          lastTap:            0,
        };
        function _getStageRect() {
          return ctx.stageRect || (ctx.stageRect = stage.getBoundingClientRect());
        }
        window.addEventListener('resize', () => { ctx.stageRect = null; });
        if (window.ResizeObserver) {
          new ResizeObserver(() => { ctx.stageRect = null; if (ctx.svgEl && ctx.mode === 'viewbox') _doSettle(); }).observe(stage);
        }

        function _renderBounds() {
          const r = _getStageRect();
          const sw = r.width, sh = r.height;
          const ar = ctx.natVB.w / ctx.natVB.h;
          let rw, rh;
          if (ar < sw / sh) { rh = sh; rw = sh * ar; }
          else               { rw = sw; rh = sw / ar; }
          return { rw, rh, ox: (sw - rw) / 2, oy: (sh - rh) / 2 };
        }

        // All gestures (ctx.drag, wheel, pinch) use CSS transform: translate+scale on
        // the SVG element — compositor-threaded, no SVG re-rasterization per frame.
        // ctx.settledVB = the viewBox actually rendered; ctx.curVB = logical destination.
        // After SETTLE_MS of no new gesture events, the viewBox attribute is
        // committed to ctx.curVB and the transform reset (one clean vector re-render).
        const SETTLE_MS = 250;

        function _doSettle() {
          ctx.settleTimer = null;
          if (!ctx.svgEl || !ctx.curVB) return;
          ctx.settledVB = null;
          if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
          // Frame 1: reset transform + commit viewBox (compositor swap)
          ctx.svgEl.style.transform = '';
          ctx.svgEl.style.willChange = '';
          ctx.svgEl.style.transformOrigin = '';
          ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
          _updateZoomDisplay(Math.round(ctx.natVB.w / ctx.curVB.w * 100));
          // Frame 2: update stroke widths after browser renders the new viewBox
          requestAnimationFrame(_updateStrokeWidths);
        }

        function applyVB(vb) {
          if (!ctx.settledVB) {
            // First change since last settle — snapshot current rendered position.
            ctx.settledVB = { ...ctx.curVB };
            if (ctx.svgEl) { ctx.svgEl.style.willChange = 'transform'; ctx.svgEl.style.transformOrigin = '0 0'; }
          }
          ctx.curVB = vb;
          // CSS transform: translate(tx,ty) scale(sx) maps ctx.settledVB rendering
          // to appear as ctx.curVB. With transform-origin:0 0:
          //   sx = ctx.settledVB.w / ctx.curVB.w
          //   tx = (ctx.settledVB.x - ctx.curVB.x)*rw/ctx.curVB.w + ox*(1 - sx)
          const { rw, rh, ox, oy } = _renderBounds();
          const sx = ctx.settledVB.w / ctx.curVB.w;
          ctx.pendingTx = (ctx.settledVB.x - ctx.curVB.x) * rw / ctx.curVB.w + ox * (1 - sx);
          ctx.pendingTy = (ctx.settledVB.y - ctx.curVB.y) * rh / ctx.curVB.h + oy * (1 - sx);
          ctx.pendingSx = sx;
          if (ctx.rafId === null) {
            ctx.rafId = requestAnimationFrame(() => {
              ctx.rafId = null;
              if (ctx.svgEl) ctx.svgEl.style.transform =
                `translate(${ctx.pendingTx}px,${ctx.pendingTy}px) scale(${ctx.pendingSx})`;
              _updateZoomDisplay(Math.round(ctx.natVB.w / ctx.curVB.w * 100));
            });
          }
          if (ctx.settleTimer !== null) clearTimeout(ctx.settleTimer);
          ctx.settleTimer = setTimeout(_doSettle, SETTLE_MS);
        }

        function resetVB() {
          if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
          if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
          ctx.settledVB = null;
          ctx.curVB = { ...ctx.natVB };
          if (ctx.svgEl) {
            ctx.svgEl.style.transform = '';
            ctx.svgEl.style.willChange = '';
            ctx.svgEl.style.transformOrigin = '';
            ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
          }
          _updateZoomDisplay(100);
          _updateStrokeWidths();
        }

        function vbZoomAt(mx, my, factor) {
          const { rw, rh, ox, oy } = _renderBounds();
          const lx = mx - ox, ly = my - oy;
          const svgX = ctx.curVB.x + (lx / rw) * ctx.curVB.w;
          const svgY = ctx.curVB.y + (ly / rh) * ctx.curVB.h;
          const newW = Math.max(ctx.natVB.w / 3000, Math.min(ctx.natVB.w * 20, ctx.curVB.w / factor));
          const newH = newW * (ctx.natVB.h / ctx.natVB.w);
          applyVB({ x: svgX - (lx / rw) * newW, y: svgY - (ly / rh) * newH, w: newW, h: newH });
        }

        function vbPanBy(dx, dy) {
          const { rw, rh } = _renderBounds();
          applyVB({ x: ctx.curVB.x - (dx / rw) * ctx.curVB.w, y: ctx.curVB.y - (dy / rh) * ctx.curVB.h, w: ctx.curVB.w, h: ctx.curVB.h });
        }

        function _activateInlineSVG(node, preserveVB) {
          // Null out stale references so _syncOverlays re-adds them to the new node
          ['minority', 'majority', '2019'].forEach(function(k) { ctx.overlayInSvg[k] = null; });
          node.setAttribute('width', '100%');
          node.setAttribute('height', '100%');
          node.setAttribute('preserveAspectRatio', 'xMidYMid meet');
          node.style.cssText = 'position:absolute;left:0;top:0;display:block;touch-action:none;';
          const _cur = (ctx.svgEl && ctx.svgEl.parentNode === stage) ? ctx.svgEl
                     : (obj.parentNode === stage)             ? obj
                     : null;
          if (_cur) stage.replaceChild(node, _cur);
          else stage.appendChild(node);

          // ed_hover_layer paths have fill:none, so pointer-events is visiblePainted
          // by default, giving zero hit area. Set all on each path so
          // document.elementsFromPoint returns them for click/hover targets.
          const _hoverLayer = node.querySelector('#ed_hover_layer');
          if (_hoverLayer) {
            _hoverLayer.style.pointerEvents = 'all';
            _hoverLayer.querySelectorAll('path[data-ed-id]').forEach(function(p) {
              p.style.pointerEvents = 'all';
            });
          }

          const vb = node.viewBox.baseVal;
          if (vb.width && vb.height) {
            ctx.natVB = { x: vb.x, y: vb.y, w: vb.width, h: vb.height };
          } else {
            const w = parseFloat(node.getAttribute('width'))  || 432;
            const h = parseFloat(node.getAttribute('height')) || 648;
            ctx.natVB = { x: 0, y: 0, w, h };
            node.setAttribute('viewBox', `0 0 ${w} ${h}`);
          }
          ctx.curVB = { ...ctx.natVB };
          ctx.svgEl = node;
          ctx.mode = 'viewbox';
          ctx.ready = true;
          var skel = document.getElementById('zoom-skeleton'); if (skel) skel.classList.add('hidden');
          // Pre-warm the other two maps so switching is instant
          setTimeout(function() {
            ['minority', 'majority', '2019'].forEach(function(k) {
              if (!ctx.svgCache[k]) {
                fetch(_mapSvgUrls[k]).then(function(r) { return r.text(); })
                  .then(function(t) { ctx.svgCache[k] = new DOMParser().parseFromString(t, 'image/svg+xml'); })
                  .catch(function() {});
              }
            });
          }, 400);
          _applyBoundaryColor(node, ctx.mapPrimary);
          reapplyLayers(ctx);
          if (typeof _applyAnomalyHighlight === 'function') _applyAnomalyHighlight();
          _syncOverlays();
          _updateStrokeWidths();
          if (overlay.style.display !== 'none') {
            if (preserveVB) {
              // Restore saved view without resetting to full province
              if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
              if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
              ctx.settledVB = null;
              ctx.curVB = { ...preserveVB };
              ctx.svgEl.style.transform = '';
              ctx.svgEl.style.willChange = '';
              ctx.svgEl.style.transformOrigin = '';
              ctx.svgEl.setAttribute('viewBox', `${ctx.curVB.x} ${ctx.curVB.y} ${ctx.curVB.w} ${ctx.curVB.h}`);
              _updateZoomDisplay(Math.round(ctx.natVB.w / ctx.curVB.w * 100));
              _updateStrokeWidths();
            } else {
              resetVB();
            }
          }
        }

        // ── Fallback state ────────────────────────────────────────────────────

        function applyFallback() {
          const w = Math.max(1, Math.round(ctx.fbNatW * ctx.fbScale));
          const h = Math.max(1, Math.round(ctx.fbNatH * ctx.fbScale));
          ctx.fbImg.width = w; ctx.fbImg.height = h;
          ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px';
          ctx.fbImg.style.top  = Math.round(ctx.fbTy) + 'px';
          _updateZoomDisplay(Math.round(ctx.fbScale * 100));
        }

        function resetFallback() {
          const sw = stage.offsetWidth, sh = stage.offsetHeight;
          ctx.fbScale = Math.min(sw / ctx.fbNatW, sh / ctx.fbNatH) * 0.94;
          ctx.fbTx = (sw - ctx.fbNatW * ctx.fbScale) / 2;
          ctx.fbTy = (sh - ctx.fbNatH * ctx.fbScale) / 2;
          applyFallback();
        }

        function initFallback() {
          ctx.mode = 'fallback';
          ctx.fbImg = document.createElement('img');
          ctx.fbImg.src = obj.data; ctx.fbImg.alt = obj.title; ctx.fbImg.draggable = false;
          ctx.fbImg.style.cssText = 'position:absolute;display:block;user-select:none;pointer-events:none;';
          stage.replaceChild(ctx.fbImg, obj);
          function onLoad() {
            ctx.fbNatW = ctx.fbImg.naturalWidth || 600; ctx.fbNatH = ctx.fbImg.naturalHeight || 900;
            ctx.ready = true;
            if (overlay.style.display !== 'none') resetFallback();
          }
          if (ctx.fbImg.complete && ctx.fbImg.naturalWidth) onLoad();
          else ctx.fbImg.onload = onLoad;
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
          if (ctx.ready) return;
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
        function _overlayFocusable() {
          return Array.from(overlay.querySelectorAll<HTMLElement>(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          )).filter(el => !el.hasAttribute('disabled'));
        }

        function open() {
          ctx.stageRect = null;  // stage may have reflowed since last open
          overlay.style.display = 'block';
          document.body.style.overflow = 'hidden';
          _updateMapButtons();
          _maybeShowIntro();
          ctx.prevFocus = document.activeElement;
          var focusable = _overlayFocusable();
          if (focusable.length) focusable[0].focus();
          if (!ctx.ready) return;
          if (ctx.mode === 'viewbox') resetVB(); else resetFallback();
        }

        function close() {
          overlay.style.display = 'none';
          document.body.style.overflow = '';
          _hideTip();
          _hideCallout();
          if (ctx.prevFocus instanceof HTMLElement) { ctx.prevFocus.focus(); }
          ctx.prevFocus = null;
          // Hide intro modal without marking seen — it will re-show on next open until dismissed
          var _intro = document.getElementById('map-intro-modal');
          if (_intro) _intro.style.display = 'none';
        }

        overlay.addEventListener('keydown', function(e: KeyboardEvent) {
          if (e.key !== 'Tab') return;
          var focusable = _overlayFocusable();
          if (focusable.length === 0) return;
          var first = focusable[0], last = focusable[focusable.length - 1];
          if (e.shiftKey) {
            if (document.activeElement === first) { e.preventDefault(); last.focus(); }
          } else {
            if (document.activeElement === last) { e.preventDefault(); first.focus(); }
          }
        });

        trigger.addEventListener('click', e => { e.preventDefault(); open(); });
        closeBtn.addEventListener('click', close);
        document.addEventListener('keydown', e => {
          if (e.key !== 'Escape') return;
          var _intro = document.getElementById('map-intro-modal');
          if (_intro && _intro.style.display !== 'none') return; // let modal handle its own Escape
          close();
        });
        overlay.addEventListener('click', e => { if (e.target === overlay) close(); });

        // ── Zoom ──────────────────────────────────────────────────────────────
        function zoomAt(mx, my, factor) {
          if (!ctx.ready) return;
          if (ctx.mode === 'viewbox') {
            vbZoomAt(mx, my, factor);
          } else {
            const newScale = Math.min(Math.max(ctx.fbScale * factor, 0.05), 500);
            const ratio = newScale / ctx.fbScale;
            ctx.fbTx = mx - ratio * (mx - ctx.fbTx);
            ctx.fbTy = my - ratio * (my - ctx.fbTy);
            ctx.fbScale = newScale;
            applyFallback();
          }
        }

        stage.addEventListener('wheel', e => {
          e.preventDefault();
          const r = _getStageRect();
          zoomAt(e.clientX - r.left, e.clientY - r.top, Math.pow(0.88, e.deltaY / 100));
        }, { passive: false });

        // ── Tooltip helpers ───────────────────────────────────────────────────
        function _showTip(d, x, y) { showTip(d, x, y); }
        function _hideTip()        { hideTip(); }

        // ── District callout (info bar) ───────────────────────────────────────
        function _showCallout(d) { showCallout(ctx, d); }
        function _hideCallout()  { hideCallout(ctx); }

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
          '2019':   '#7a98b4',
        };

        // ── Share bridge ──────────────────────────────────────────────────────
        _getState = function() {
          return {
            primary: ctx.mapPrimary,
            mapOn:   { minority: ctx.mapOn.minority, majority: ctx.mapOn.majority, '2019': ctx.mapOn['2019'] },
            layers:  { vote: ctx.layerState.vote, 'ed-fill': ctx.layerState['ed-fill'], 'ed-lines': ctx.layerState['ed-lines'], eg: ctx.layerState.eg },
            viewport: ctx.svgEl && ctx.natVB && ctx.curVB ? {
              cx_norm: Math.max(0, Math.min(1, (ctx.curVB.x + ctx.curVB.w / 2 - ctx.natVB.x) / ctx.natVB.w)),
              cy_norm: Math.max(0, Math.min(1, (ctx.curVB.y + ctx.curVB.h / 2 - ctx.natVB.y) / ctx.natVB.h)),
              zoom:    ctx.curVB.w / ctx.natVB.w,
            } : { cx_norm: 0.5, cy_norm: 0.5, zoom: 1.0 },
          };
        };
        _applyStateFn = function(primary, targetMapOn, targetLayers) {
          ctx.mapPrimary       = primary;
          ctx.mapOn.minority   = !!targetMapOn.minority;
          ctx.mapOn.majority   = !!targetMapOn.majority;
          ctx.mapOn['2019']    = !!targetMapOn['2019'];
          ctx.mapActivationOrder = ['minority', 'majority', '2019'].filter(function(k) { return ctx.mapOn[k]; });
          var pi = ctx.mapActivationOrder.indexOf(primary);
          if (pi !== -1) { ctx.mapActivationOrder.splice(pi, 1); ctx.mapActivationOrder.push(primary); }
          _doSwitchPrimary(primary);
          _syncOverlays();
          ['vote', 'ed-fill', 'ed-lines', 'eg'].forEach(function(k) {
            var on = !!targetLayers[k];
            ctx.layerState[k] = on;
            var btn = document.querySelector('.tb-btn[data-layer="' + k + '"]');
            if (btn) btn.classList.toggle('tb-layer-on', on);
            if (k === 'vote')     applyVoteLayer(ctx, on);
            if (k === 'ed-fill')  applyEdFillLayer(ctx, on);
            if (k === 'ed-lines') applyEdLinesLayer(ctx, on);
            if (k === 'eg')       applyEGLayer(ctx, on);
          });
          _updateMapButtons();
        };
        function _emit(event) { if (_onEvent) _onEvent(event); }

        // ── Map-wide boundary color ───────────────────────────────────────────────
        function _applyBoundaryColor(svgNode, mapKey) {
          if (!svgNode) return;
          const color = _mapAccentColors[mapKey] || '#555';
          const g = svgNode.querySelector('#ed_boundary_layer');
          if (!g) { console.warn('[map] ed_boundary_layer not found in SVG'); return; }
          // Hide the direct-child polygon outlines (each ED drawn as closed path → double lines).
          // Only LineCollection_1 draws each boundary once; use that exclusively.
          Array.from(g.children).forEach(function(child) {
            if (child.tagName === 'path') child.style.display = 'none';
          });
          const lc = g.querySelector('#LineCollection_1');
          if (lc) lc.querySelectorAll('path').forEach(p => {
            p.style.stroke = color;
            p.style.strokeWidth = '0.5';
            p.style.strokeOpacity = '1';
            p.style.fill = 'none';
          });
          _updateStrokeWidths();
        }

        // ── Zoom-relative stroke widths ────────────────────────────────────────
        // Keeps lines visually proportional as the user zooms in/out.
        // Overlay is always 60% of primary (slightly thinner, same zoom tracking).
        // Floor/ceil in SVG user units; at 400%+ zoom floors are intentionally
        // very thin so overlays don't clutter the primary boundaries.
        function _updateStrokeWidths() {
          if (!ctx.svgEl || !ctx.natVB || !ctx.curVB) return;
          var zf = ctx.natVB.w / ctx.curVB.w;                            // 1 = 100%, 4 = 400%
          var primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
          var overlayW = Math.min(0.35, primaryW * 0.6);
          var pLc = ctx.svgEl.querySelector('#ed_boundary_layer #LineCollection_1');
          if (pLc) pLc.querySelectorAll('path').forEach(function(p) {
            p.style.strokeWidth = String(primaryW);
          });
          ['minority', 'majority', '2019'].forEach(function(key) {
            var og = ctx.overlayInSvg[key];
            if (og) {
              var lc = og.querySelector('#LineCollection_1');
              if (lc) lc.querySelectorAll('path').forEach(function(p) {
                p.style.strokeWidth = String(overlayW);
              });
            }
          });
        }

        // ── Active ED boundary highlight ──────────────────────────────────────────
        function _setEdHighlight(p)   { setEdHighlight(ctx, p); }
        function _clearEdHighlight()   { clearEdHighlight(ctx); }
        function _activateCenterED()   { activateCenterED(ctx, _animateToVB, _emit); }

        // ── Map overlay system ─────────────────────────────────────────────────────

        function _extractBoundaryGroup(key) {
          var doc = ctx.svgCache[key];
          if (!doc) return null;
          var g = doc.querySelector('#ed_boundary_layer');
          if (!g) return null;
          var clone = document.importNode(g, true);
          // Hide direct-child polygon outlines — same fix as _applyBoundaryColor.
          Array.from(clone.children).forEach(function(child) {
            if (child.tagName === 'path') child.style.display = 'none';
          });
          var zf = (ctx.natVB && ctx.curVB) ? ctx.natVB.w / ctx.curVB.w : 1;
          var primaryW = Math.min(2.5, Math.max(0.10, 1.0 / zf));
          var sw = Math.min(0.35, primaryW * 0.6);
          var lc = clone.querySelector('#LineCollection_1');
          if (lc) lc.querySelectorAll('path').forEach(function(p) {
            p.style.stroke = _mapAccentColors[key] || '#555';
            p.style.strokeWidth = String(sw);
            p.style.strokeOpacity = '0.55';
            p.style.fill = 'none';
          });
          clone.setAttribute('pointer-events', 'none');
          clone.id = 'ed-boundary-overlay-' + key;
          return clone;
        }

        function _syncOverlays() {
          ['minority', 'majority', '2019'].forEach(function(key) {
            if (!ctx.mapOn[key] || key === ctx.mapPrimary) {
              if (ctx.overlayInSvg[key]) { ctx.overlayInSvg[key].remove(); ctx.overlayInSvg[key] = null; }
              return;
            }
            if (!ctx.overlayInSvg[key] && ctx.svgEl) _fetchAndOverlay(key);
          });
        }

        function _fetchAndOverlay(key) {
          function apply() {
            if (!ctx.mapOn[key] || key === ctx.mapPrimary || !ctx.svgEl) return;
            var g = _extractBoundaryGroup(key);
            if (g) { ctx.svgEl.appendChild(g); ctx.overlayInSvg[key] = g; }
          }
          if (ctx.svgCache[key]) { apply(); return; }
          fetch(_mapSvgUrls[key]).then(function(r) { return r.text(); }).then(function(text) {
            ctx.svgCache[key] = new DOMParser().parseFromString(text, 'image/svg+xml');
            apply();
          }).catch(function() {});
        }

        function _updateMapButtons() {
          document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
            var key = b.dataset.map;
            b.classList.toggle('tb-map-primary', !!ctx.mapPrimary && ctx.mapOn[key] && key === ctx.mapPrimary);
            b.classList.toggle('tb-map-overlay',  !!ctx.mapPrimary && ctx.mapOn[key] && key !== ctx.mapPrimary);
          });
          // Clear anomaly state when minority is no longer the top layer
          if (ctx.mapPrimary !== 'minority' && ctx.anomalyOn) {
            ctx.anomalyOn = false;
            document.querySelectorAll('[data-anomaly]').forEach(function(b) { b.classList.remove('tb-layer-on'); });
            if (ctx.svgEl) _applyAnomalyHighlight();
          }
        }

        // Hoist a map to the top of the stack without toggling it off
        function _activateAsTop(key) {
          if (!_mapSvgUrls[key]) return;
          if (ctx.mapPrimary === key) return; // already top
          ctx.mapOn[key] = true;
          ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
          ctx.mapActivationOrder.push(key);
          ctx.mapPrimary = key;
          _doSwitchPrimary(key);
          _updateMapButtons();
        }

        function _doSwitchPrimary(key) {
          var ctxEl = document.getElementById('ec-context');
          if (ctxEl) ctxEl.textContent = _mapContextLabels[key];
          var savedName = ctx.selectedEdName;
          _hideCallout();
          ctx.edHover = null;
          var savedVB = ctx.curVB ? Object.assign({}, ctx.curVB) : null;
          // Helper: activate a parsed SVG document as the new primary
          function _applySvgDoc(doc) {
            var root = doc.documentElement;
            if (root && root.tagName.toLowerCase() !== 'parsererror') {
              _activateInlineSVG(document.importNode(root, true), savedVB);
              if (ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length) {
                ctx.edHover = ctx.allHoverData[key];
              }
              if (savedName) {
                var rec = ctx.nameIndex[key] && ctx.nameIndex[key][savedName];
                if (rec) {
                  var path = ctx.svgEl && ctx.svgEl.querySelector('[data-ed-id="' + rec.id + '"]');
                  if (path) { _showCallout(rec); _setEdHighlight(path); }
                } else { _activateCenterED(); }
              } else { _activateCenterED(); }
            } else { ctx.ready = true; }
            stage.style.opacity = '';
            setTimeout(function() { stage.style.transition = ''; }, 200);
          }

          if (ctx.svgCache[key]) {
            // Cache hit — instant, no loading state needed
            _applySvgDoc(ctx.svgCache[key]);
          } else {
            // Cache miss — show loading state while fetching
            ctx.ready = false;
            var _skelEl = document.getElementById('zoom-skeleton'); if (_skelEl) _skelEl.classList.remove('hidden');
            stage.style.opacity = '0.45';
            stage.style.transition = 'opacity 0.15s';
            fetch(_mapSvgUrls[key])
              .then(function(r) { return r.text(); })
              .then(function(text) {
                var doc = new DOMParser().parseFromString(text, 'image/svg+xml');
                ctx.svgCache[key] = doc;
                _applySvgDoc(doc);
              })
              .catch(function() {
                ctx.ready = true;
                stage.style.opacity = '';
                setTimeout(function() { stage.style.transition = ''; }, 200);
              });
          }
          // JSON is pre-fetched at init via _loadHoverJson; only fetch if not yet ctx.ready
          if (!(ctx.allHoverData[key] && Object.keys(ctx.allHoverData[key]).length)) {
            fetch(_mapJsonUrls[key])
              .then(function(r) { return r.json(); })
              .then(function(d) {
                var byId = {}, byName = {};
                d.forEach(function(rec) { byId[rec.id] = rec; byName[rec.name] = rec; });
                ctx.allHoverData[key] = byId;
                ctx.nameIndex[key] = byName;
                ctx.edHover = byId;
                if (ctx.layerState['ed-fill']) applyEdFillLayer(ctx, true);
              })
              .catch(function() { ctx.edHover = null; });
          }
        }

        function toggleMap(key) {
          if (!_mapSvgUrls[key]) return;
          if (!ctx.mapOn[key]) {
            // Toggle ON — becomes the new top layer
            ctx.mapOn[key] = true;
            ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
            ctx.mapActivationOrder.push(key);
            ctx.mapPrimary = key;
            _doSwitchPrimary(key);  // old primary becomes overlay via _syncOverlays inside
          } else {
            // Toggle OFF
            ctx.mapOn[key] = false;
            ctx.mapActivationOrder = ctx.mapActivationOrder.filter(function(k) { return k !== key; });
            if (ctx.overlayInSvg[key]) { ctx.overlayInSvg[key].remove(); ctx.overlayInSvg[key] = null; }
            if (key === ctx.mapPrimary) {
              // Was the top — promote next most-recently-activated map
              var next = ctx.mapActivationOrder.length > 0
                ? ctx.mapActivationOrder[ctx.mapActivationOrder.length - 1] : null;
              if (next) {
                ctx.mapPrimary = next;
                _doSwitchPrimary(next);
              } else {
                ctx.mapPrimary = null;
                if (ctx.svgEl) { ctx.svgEl.remove(); ctx.svgEl = null; }
                var skelEl = document.getElementById('zoom-skeleton');
                if (skelEl) skelEl.classList.remove('hidden');
              }
            }
            // If it was an overlay, overlay reference was already removed above
          }
          _updateMapButtons();
          _emit({ type: 'map_switch', primary: ctx.mapPrimary, mapOn: { minority: ctx.mapOn.minority, majority: ctx.mapOn.majority, '2019': ctx.mapOn['2019'] } });
        }

        document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
          b.addEventListener('click', function() { toggleMap(b.dataset.map); });
        });

        document.getElementById('ec-close').addEventListener('click', _hideCallout);

        // ── Layer panel ────────────────────────────────────────────────────────────

        function _loadHoverJson(key, url) {
          fetch(url).then(r => r.json()).then(d => {
            const byId = {}, byName = {};
            d.forEach(rec => { byId[rec.id] = rec; byName[rec.name] = rec; });
            ctx.allHoverData[key] = byId;
            ctx.nameIndex[key] = byName;
            if (key === ctx.mapPrimary) { ctx.edHover = byId; reapplyLayers(ctx); }
          }).catch(() => {});
        }
        _loadHoverJson('minority', 'data/ed_hover_minority.json');
        _loadHoverJson('majority', 'data/ed_hover_majority.json');
        _loadHoverJson('2019',    'data/ed_hover_2019.json');

        document.querySelectorAll('.tb-btn[data-layer]').forEach(function(b) {
          b.addEventListener('click', function() {
            var key = b.dataset.layer;
            if (key === 'lock') {
              ctx.mapLocked = !ctx.mapLocked;
              b.classList.toggle('tb-layer-on', ctx.mapLocked);
              return;
            }
            var on = !ctx.layerState[key];
            setLayerOn(ctx, key, on, _emit);
            if (key === 'ed-fill' && on && ctx.layerState['eg'])      setLayerOn(ctx, 'eg', false, _emit);
            if (key === 'eg'      && on && ctx.layerState['ed-fill']) setLayerOn(ctx, 'ed-fill', false, _emit);
          });
        });

        // ── Snap-to-ED animation ───────────────────────────────────────────────
        function _animateToVB(targetVB, dur) {
          if (ctx.mapLocked) return;
          if (ctx.settleTimer !== null) { clearTimeout(ctx.settleTimer); ctx.settleTimer = null; }
          if (ctx.rafId !== null) { cancelAnimationFrame(ctx.rafId); ctx.rafId = null; }
          const startVB = { ...ctx.curVB };
          if (!ctx.settledVB) {
            ctx.settledVB = { ...ctx.curVB };
            ctx.svgEl.style.willChange = 'transform';
            ctx.svgEl.style.transformOrigin = '0 0';
          }
          const t0 = performance.now();
          function step(now) {
            const t = Math.min((now - t0) / dur, 1);
            const ease = 1 - Math.pow(1 - t, 3); // ease-out cubic — fast start, buttery decel
            ctx.curVB = {
              x: startVB.x + (targetVB.x - startVB.x) * ease,
              y: startVB.y + (targetVB.y - startVB.y) * ease,
              w: startVB.w + (targetVB.w - startVB.w) * ease,
              h: startVB.h + (targetVB.h - startVB.h) * ease,
            };
            const { rw, rh, ox, oy } = _renderBounds();
            const sx = ctx.settledVB.w / ctx.curVB.w;
            ctx.svgEl.style.transform =
              `translate(${(ctx.settledVB.x - ctx.curVB.x)*rw/ctx.curVB.w + ox*(1-sx)}px,` +
              `${(ctx.settledVB.y - ctx.curVB.y)*rh/ctx.curVB.h + oy*(1-sx)}px) scale(${sx})`;
            _updateZoomDisplay(Math.round(ctx.natVB.w / ctx.curVB.w * 100));
            if (t < 1) { requestAnimationFrame(step); }
            else { ctx.settleTimer = setTimeout(_doSettle, SETTLE_MS); }
          }
          requestAnimationFrame(step);
        }

        function _isEdVisible(bb)      { return isEdVisible(ctx, bb); }
        function _snapToED(pathEl, force) { snapToED(ctx, pathEl, !!force, _animateToVB, _getStageRect); }
        function _zoomEdTo70(pathEl)      { zoomEdTo70(ctx, pathEl, _animateToVB, _getStageRect); }
        function _tipTarget(e)            { return tipTarget(e); }

        // ── Unified ctx.drag + tap + pinch (Pointer Events — all gesture types) ──────

        function _ptrMid() {
          const [a, b] = [...ctx.ptrs.values()];
          return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
        }
        function _ptrDist() {
          const [a, b] = [...ctx.ptrs.values()];
          return Math.hypot(a.x - b.x, a.y - b.y);
        }

        stage.addEventListener('pointerdown', e => {
          if (!ctx.ready) return;
          if (e.pointerType === 'mouse' && e.button !== 0) return;
          ctx.ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
          try { stage.setPointerCapture(e.pointerId); } catch (_) {}
          if (ctx.ptrs.size === 2) {
            if (ctx.drag) { ctx.drag = null; stage.classList.remove('dragging'); }
            _hideTip();
            ctx.lastPinchDist = _ptrDist();
            ctx.lastPinchMid = _ptrMid();
            return;
          }
          if (ctx.ptrs.size > 2) return;
          ctx.drag = { cx: e.clientX, cy: e.clientY, startX: e.clientX, startY: e.clientY, id: e.pointerId };
          ctx.dragMoved = false;
          stage.classList.add('dragging');
        });

        stage.addEventListener('pointermove', e => {
          if (!ctx.ready || !ctx.ptrs.has(e.pointerId)) return;
          ctx.ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });

          if (ctx.ptrs.size >= 2) {
            const dist = _ptrDist(), mid = _ptrMid(), r = _getStageRect();
            if (ctx.lastPinchDist && dist > 0) zoomAt(mid.x - r.left, mid.y - r.top, dist / ctx.lastPinchDist);
            if (ctx.lastPinchMid) {
              if (ctx.mode === 'viewbox') vbPanBy(mid.x - ctx.lastPinchMid.x, mid.y - ctx.lastPinchMid.y);
              else { ctx.fbTx += mid.x - ctx.lastPinchMid.x; ctx.fbTy += mid.y - ctx.lastPinchMid.y;
                     ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px'; ctx.fbImg.style.top = Math.round(ctx.fbTy) + 'px'; }
            }
            ctx.lastPinchDist = dist; ctx.lastPinchMid = mid;
            return;
          }

          if (e.pointerType !== 'touch' && !ctx.drag && ctx.mode === 'viewbox' && ctx.edHover) {
            const hit = _tipTarget(e);
            if (hit) _showTip(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)], e.clientX, e.clientY);
            else _hideTip();
          }
          if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
          const dx = e.clientX - ctx.drag.cx, dy = e.clientY - ctx.drag.cy;
          if (!ctx.dragMoved && Math.hypot(e.clientX - ctx.drag.startX, e.clientY - ctx.drag.startY) < 6) return;
          if (!ctx.dragMoved) { ctx.dragMoved = true; _hideTip(); }
          ctx.drag.cx = e.clientX; ctx.drag.cy = e.clientY;
          if (ctx.mode === 'viewbox') vbPanBy(dx, dy);
          else { ctx.fbTx += dx; ctx.fbTy += dy; ctx.fbImg.style.left = Math.round(ctx.fbTx) + 'px'; ctx.fbImg.style.top = Math.round(ctx.fbTy) + 'px'; }
        });


        stage.addEventListener('pointerup', e => {
          ctx.ptrs.delete(e.pointerId);
          try { stage.releasePointerCapture(e.pointerId); } catch (_) {}
          if (ctx.ptrs.size < 2) { ctx.lastPinchDist = null; ctx.lastPinchMid = null; }
          if (!ctx.drag || ctx.drag.id !== e.pointerId) return;
          stage.classList.remove('dragging');
          if (!ctx.dragMoved && ctx.mode === 'viewbox') {
            if (e.pointerType === 'touch') {
              const now = performance.now();
              if (now - ctx.lastTap < 300) {
                const hit = _tipTarget(e);
                if (hit) { _zoomEdTo70(hit); }
                else { _hideCallout(); _animateToVB({ ...ctx.natVB }, 420); }
                ctx.lastTap = 0;
              } else {
                ctx.lastTap = now;
                if (ctx.edHover) {
                  const hit = _tipTarget(e);
                  if (hit) {
                    _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
                    _setEdHighlight(hit);
                    _snapToED(hit);
                  } else _hideCallout();
                }
              }
            } else if (ctx.edHover) {
              const hit = _tipTarget(e);
              if (hit) {
                _hideTip();
                _showCallout(ctx.edHover[parseInt(hit.getAttribute('data-ed-id'), 10)]);
                _setEdHighlight(hit);
                if (!ctx.mapLocked) _snapToED(hit);
              } else {
                _hideCallout();
              }
            }
          }
          ctx.drag = null;
        });

        stage.addEventListener('pointercancel', e => {
          ctx.ptrs.delete(e.pointerId);
          if (ctx.drag && ctx.drag.id === e.pointerId) { ctx.drag = null; stage.classList.remove('dragging'); }
          if (ctx.ptrs.size < 2) { ctx.lastPinchDist = null; ctx.lastPinchMid = null; }
        });

        stage.addEventListener('pointerleave', e => { if (e.pointerType !== 'touch') _hideTip(); });

        stage.addEventListener('dblclick', e => {
          if (!ctx.ready) return;
          if (ctx.mode === 'viewbox') {
            const hit = _tipTarget(e);
            if (hit) _zoomEdTo70(hit);
            else _animateToVB({ ...ctx.natVB }, 420);
          } else resetFallback();
        });

        // ── Zoom slider ───────────────────────────────────────────────────────────
        function _zoomToPct(pct) {
          if (!ctx.ready || ctx.mode !== 'viewbox' || !ctx.natVB || !ctx.curVB) return;
          var targetW = ctx.natVB.w * 100 / pct;
          var targetH = ctx.natVB.h * 100 / pct;
          var cx = ctx.curVB.x + ctx.curVB.w / 2;
          var cy = ctx.curVB.y + ctx.curVB.h / 2;
          ctx.curVB = { x: cx - targetW/2, y: cy - targetH/2, w: targetW, h: targetH };
          _doSettle();
        }
        if (_zoomSlider) {
          _zoomSlider.addEventListener('input', function() {
            _zoomToPct(parseInt(_zoomSlider.value, 10));
          });
        }

        // ── ED search ─────────────────────────────────────────────────────────────
        initSearch(ctx, {
          showCallout: _showCallout, setEdHighlight: _setEdHighlight, snapToED: _snapToED,
          updateMapButtons: _updateMapButtons, doSwitchPrimary: _doSwitchPrimary,
        });

        // ── Anomaly highlight ─────────────────────────────────────────────────────
        function _applyAnomalyHighlight() { applyAnomalyHighlight(ctx); }
        initAnomalyButtons(ctx, {
          activateAsTop: _activateAsTop, open: open, emit: _emit,
          isOverlayOpen: function() { return overlay.style.display === 'block'; },
          animateToVB: _animateToVB, getStageRect: _getStageRect,
        });

        // ── Named-ED zoom (inline buttons) ──────────────────────────────────────
        initNamedEdButtons(ctx, {
          open: open, isOverlayOpen: function() { return overlay.style.display === 'block'; },
          animateToVB: _animateToVB, getStageRect: _getStageRect,
          showCallout: _showCallout, setEdHighlight: _setEdHighlight,
        });

        // ── Map onboarding modal ──────────────────────────────────────────────────
        initIntroModal();  // wires close-btn, backdrop-click, and Escape handlers

        async function _maybeShowIntro() {
          if (await hasSeenIntro()) return;
          var modal = document.getElementById('map-intro-modal');
          if (modal) modal.style.display = 'flex';
        }

      })();
}
