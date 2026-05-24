﻿// Alberta Electoral Boundary Audit — map engine
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io
// @ts-nocheck

import { initNavScrollspy } from './mapEngine/navScrollspy';
import { initIntroModal }   from './mapEngine/introModal';
import { hasSeenIntro }     from './prefs';
import { applyVoteLayer, applyEdFillLayer, applyEdLinesLayer, applyEGLayer, setLayerOn } from './mapEngine/layers';
import { hideTip, showCallout, hideCallout, hideVaCallout, setEdHighlight, activateCenterED, snapToED } from './mapEngine/edInteraction';
import { initSearch } from './mapEngine/search';
import { applyAnomalyHighlight, initAnomalyButtons } from './mapEngine/anomaly';
import { initNamedEdButtons } from './mapEngine/namedEdZoom';
import { initViewport, getStageRect, animateToVB as vpAnimateToVB, resetVB as vpResetVB } from './mapEngine/viewport';
import { activateInlineSVG as sl_activateInlineSVG, applyFallback as sl_applyFallback, resetFallback as sl_resetFallback, tryInit as sl_tryInit } from './mapEngine/svgLoader';
import { initGestures } from './mapEngine/gestures';
import { initOverlay } from './mapEngine/overlay';
import { applyBoundaryColor as mpApplyBoundaryColor, syncOverlays as mpSyncOverlays, updateMapButtons as mpUpdateMapButtons, doSwitchPrimary as mpDoSwitchPrimary, activateAsTop as mpActivateAsTop, toggleMap as mpToggleMap, loadHoverJson as mpLoadHoverJson, loadVaJson as mpLoadVaJson } from './mapEngine/maps';

let _onEvent      = null;
let _getState     = null;
let _applyStateFn = null;
let _openFn: (() => void) | null = null;

export function onEvent(cb)                                 { _onEvent = cb; }
export function getState()                                  { return _getState ? _getState() : null; }
export function applyState(primary, mapOn, layers)          { if (_applyStateFn) _applyStateFn(primary, mapOn, layers); }
export function openOverlay(): void                         { if (_openFn) _openFn(); }

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
        const closeBtn = document.getElementById('zoom-close');
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

          // VA (voting area) data (pre-fetched at init; no-op until SVGs carry data-va-id)
          allVaData:          {},         // mapKey → { va_id: rec }
          selectedVaId:       null,

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
        initViewport(ctx);
        function _getStageRect() { return getStageRect(ctx); }

        function resetVB() { vpResetVB(ctx); }

        // ── SVG loader thin wrappers — declared here (hoisted), deps wired after _mapSvgUrls ──
        function _activateInlineSVG(node, pVB) { sl_activateInlineSVG(ctx, node, pVB, stage, overlay, _svgDeps); }
        function applyFallback()               { sl_applyFallback(ctx); }
        function resetFallback()               { sl_resetFallback(ctx, stage); }

        // ── Open / close ──────────────────────────────────────────────────────
        const { open, close } = initOverlay(ctx, overlay, closeBtn, {
          updateMapButtons: () => _updateMapButtons(),
          maybeShowIntro:   () => _maybeShowIntro(),
          resetVB:          () => resetVB(),
          resetFallback:    () => resetFallback(),
          hideTip:          () => hideTip(),
          hideCallout:      () => _hideCallout(),
        });
        _openFn = open;

        // ── District callout (info bar) ───────────────────────────────────────
        function _showCallout(d) { showCallout(ctx, d); }
        function _hideCallout()  { hideCallout(ctx); hideVaCallout(ctx); }

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
        const _mapVaJsonUrls = {
          minority: 'data/va_hover_minority.json',
          majority: 'data/va_hover_majority.json',
          '2019':   'data/va_hover_2019.json',
        };

        // ── SVG loader deps + event wiring (after _mapSvgUrls is defined) ────────────
        const _svgDeps = {
          obj,
          svgUrls: _mapSvgUrls,
          applyBoundaryColor: (n, k) => _applyBoundaryColor(n, k),
          applyAnomalyHighlight: () => _applyAnomalyHighlight(),
          syncOverlays: () => _syncOverlays(),
        };
        obj.addEventListener('load', () => sl_tryInit(ctx, obj, stage, overlay, _svgDeps));
        if (obj.contentDocument && obj.contentDocument.readyState === 'complete') sl_tryInit(ctx, obj, stage, overlay, _svgDeps);

        // ── Maps module deps ──────────────────────────────────────────────────────
        const _mapsDeps = {
          svgUrls: _mapSvgUrls,
          jsonUrls: _mapJsonUrls,
          activateInlineSVG: (node, pVB) => _activateInlineSVG(node, pVB),
          showCallout:        (d) => _showCallout(d),
          hideCallout:        () => _hideCallout(),
          setEdHighlight:     (p) => _setEdHighlight(p),
          activateCenterED:   () => _activateCenterED(),
          applyAnomalyHighlight: () => _applyAnomalyHighlight(),
          emit:               (e) => _emit(e),
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

        // ── Maps thin wrappers ────────────────────────────────────────────────────
        function _applyBoundaryColor(svgNode, mapKey) { mpApplyBoundaryColor(ctx, svgNode, mapKey); }
        function _syncOverlays()                       { mpSyncOverlays(ctx, _mapsDeps); }
        function _updateMapButtons()                   { mpUpdateMapButtons(ctx, _mapsDeps); }
        function _doSwitchPrimary(key)                 { mpDoSwitchPrimary(ctx, key, _mapsDeps); }
        function _activateAsTop(key)                   { mpActivateAsTop(ctx, key, _mapsDeps); }
        function toggleMap(key)                        { mpToggleMap(ctx, key, _mapsDeps); }

        // ── Active ED boundary highlight ──────────────────────────────────────────
        function _setEdHighlight(p)  { setEdHighlight(ctx, p); }
        function _activateCenterED() { activateCenterED(ctx, _animateToVB, _emit); }

        document.querySelectorAll('.tb-btn[data-map]').forEach(function(b) {
          b.addEventListener('click', function() { toggleMap(b.dataset.map); });
        });

        document.getElementById('ec-close').addEventListener('click', _hideCallout);

        // ── Layer panel ────────────────────────────────────────────────────────────

        mpLoadHoverJson(ctx, 'minority', _mapJsonUrls.minority);
        mpLoadHoverJson(ctx, 'majority', _mapJsonUrls.majority);
        mpLoadHoverJson(ctx, '2019',    _mapJsonUrls['2019']);

        mpLoadVaJson(ctx, 'minority', _mapVaJsonUrls.minority);
        mpLoadVaJson(ctx, 'majority', _mapVaJsonUrls.majority);
        mpLoadVaJson(ctx, '2019',    _mapVaJsonUrls['2019']);

        const vcClose = document.getElementById('vc-close');
        if (vcClose) vcClose.addEventListener('click', function() { hideVaCallout(ctx); });

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
        function _animateToVB(targetVB, dur) { vpAnimateToVB(ctx, targetVB, dur); }
        function _snapToED(pathEl, force) { snapToED(ctx, pathEl, !!force, _animateToVB, _getStageRect); }

        // ── Gestures ──────────────────────────────────────────────────────────────
        initGestures(ctx, stage);

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
        const _helpBtn = document.getElementById('tb-help-btn');
        if (_helpBtn) {
          _helpBtn.addEventListener('click', () => {
            const modal = document.getElementById('map-intro-modal');
            if (modal) modal.style.display = 'flex';
          });
        }

        async function _maybeShowIntro() {
          if (await hasSeenIntro()) return;
          var modal = document.getElementById('map-intro-modal');
          if (modal) modal.style.display = 'flex';
        }

      })();
}
