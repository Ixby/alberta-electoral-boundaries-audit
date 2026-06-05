﻿// Alberta Electoral Boundary Audit — map engine
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
// https://ixby.github.io

import { initNavScrollspy } from './mapEngine/navScrollspy';
import { initIntroModal }   from './mapEngine/introModal';
import { hasSeenIntro }     from './prefs';
import { applyVoteLayer, applyEdFillLayer, applyEdLinesLayer, applyEGLayer, setLayerOn } from './mapEngine/layers';
import { hideTip, showCallout, hideCallout, hideVaCallout, setEdHighlight, activateCenterED, snapToED } from './mapEngine/edInteraction';
import { initSearch } from './mapEngine/search';
import { applyAnomalyHighlight, initAnomalyButtons } from './mapEngine/anomaly';
import { initNamedEdButtons } from './mapEngine/namedEdZoom';
import { initViewport, getStageRect, animateToVB as vpAnimateToVB, resetVB as vpResetVB } from './mapEngine/viewport';
import { activateInlineSVG as sl_activateInlineSVG, tryInit as sl_tryInit } from './mapEngine/svgLoader';
import { initGestures } from './mapEngine/gestures';
import { initOverlay } from './mapEngine/overlay';
import { applyBoundaryColor as mpApplyBoundaryColor, syncOverlays as mpSyncOverlays, updateMapButtons as mpUpdateMapButtons, doSwitchPrimary as mpDoSwitchPrimary, activateAsTop as mpActivateAsTop, toggleMap as mpToggleMap, loadHoverJson as mpLoadHoverJson, loadVaJson as mpLoadVaJson } from './mapEngine/maps';
import type { MapEngineEvent, MapEngineEventHandler, MapCtx, MapKey, LayerKey, ViewBox } from './mapEngine/types';
import type { MapState } from './share';
import { DOM_IDS } from './mapEngine/domIds';

export type { MapEngineEvent, MapEngineEventHandler };

let _onEvent: MapEngineEventHandler | null = null;
let _getState: (() => MapState) | null = null;
let _applyStateFn: ((primary: MapKey, mapOn: Record<MapKey, boolean>, layers: Record<LayerKey, boolean>) => void) | null = null;
let _openFn: (() => void) | null = null;

export function onEvent(cb: MapEngineEventHandler)          { _onEvent = cb; }
export function getState(): MapState | null                 { return _getState ? _getState() : null; }
export function applyState(primary: MapKey, mapOn: Record<MapKey, boolean>, layers: Record<LayerKey, boolean>): void {
  if (_applyStateFn) _applyStateFn(primary, mapOn, layers);
}
export function openOverlay(): void                         { if (_openFn) _openFn(); }

export function init(basePath: string): void {
    initNavScrollspy();

      // ── Zoom viewer — inline SVG adoption (true infinite zoom, no tile ceiling)
      //    Primary: adopt SVG node from <object> contentDocument into main document.
      //    Secondary: XHR-parse and importNode (when contentDocument isn't ready).
      //
      //    Once inline, the browser renders SVG vector paths directly from the main
      //    document's paint record. ViewBox manipulation re-renders from paths at
      //    display resolution — no GPU tile rasterization limit at any zoom level.
      (function () {
        const overlay  = document.getElementById(DOM_IDS.zoomOverlay) as HTMLElement;
        const stage    = document.getElementById(DOM_IDS.zoomStage)   as HTMLElement;
        const obj      = document.getElementById(DOM_IDS.zoomObj)     as HTMLObjectElement;
        const closeBtn = document.getElementById(DOM_IDS.zoomClose)   as HTMLElement;
        // ── Shared mutable state ──────────────────────────────────────────────────
        const ctx: MapCtx = {
          // SVG load mode
          mode:               null,       // 'viewbox' | null
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

        // ── SVG loader thin wrapper — declared here (hoisted), deps wired after _mapSvgUrls ──
        function _activateInlineSVG(node: SVGSVGElement, pVB?: ViewBox) { sl_activateInlineSVG(ctx, node, pVB, stage, overlay, _svgDeps); }

        // ── Open / close ──────────────────────────────────────────────────────
        const { open, close } = initOverlay(ctx, overlay, closeBtn, {
          updateMapButtons: () => _updateMapButtons(),
          maybeShowIntro:   () => _maybeShowIntro(),
          resetVB:          () => resetVB(),
          hideTip:          () => hideTip(),
          hideCallout:      () => _hideCallout(),
          primeOnce:        () => _primeMapData(),
        });
        _openFn = open;

        // ── District callout (info bar) ───────────────────────────────────────
        function _showCallout(d: any) { showCallout(ctx, d); }
        function _hideCallout()       { hideCallout(ctx); hideVaCallout(ctx); }

        // ── Map selector ──────────────────────────────────────────────────────────
        const _mapSvgUrls: Record<MapKey, string> = {
          minority: `${basePath}/images/cover_art_minority_hires.svg`,
          majority: `${basePath}/images/cover_art_majority_hires.svg`,
          '2019':   `${basePath}/images/cover_art_2019_hires.svg`,
        };
        const _mapJsonUrls: Record<MapKey, string> = {
          minority: 'data/ed_hover_minority.json',
          majority: 'data/ed_hover_majority.json',
          '2019':   'data/ed_hover_2019.json',
        };
        const _mapVaJsonUrls: Record<MapKey, string> = {
          minority: 'data/va_hover_minority.json',
          majority: 'data/va_hover_majority.json',
          '2019':   'data/va_hover_2019.json',
        };

        // ── SVG loader deps + event wiring (after _mapSvgUrls is defined) ────────────
        const _svgDeps = {
          obj,
          svgUrls: _mapSvgUrls,
          applyBoundaryColor: (n: SVGSVGElement, k: MapKey | null) => _applyBoundaryColor(n, k),
          applyAnomalyHighlight: () => _applyAnomalyHighlight(),
          syncOverlays: () => _syncOverlays(),
        };
        obj.addEventListener('load', () => sl_tryInit(ctx, obj, stage, overlay, _svgDeps));
        if (obj.contentDocument && obj.contentDocument.readyState === 'complete') sl_tryInit(ctx, obj, stage, overlay, _svgDeps);

        // ── Maps module deps ──────────────────────────────────────────────────────
        const _mapsDeps = {
          svgUrls: _mapSvgUrls,
          jsonUrls: _mapJsonUrls,
          activateInlineSVG: (node: SVGSVGElement, pVB?: ViewBox | null) => _activateInlineSVG(node, pVB || undefined),
          showCallout:        (d: any) => _showCallout(d),
          hideCallout:        () => _hideCallout(),
          setEdHighlight:     (p: SVGGraphicsElement) => _setEdHighlight(p),
          activateCenterED:   () => _activateCenterED(),
          applyAnomalyHighlight: () => _applyAnomalyHighlight(),
          emit:               (e: MapEngineEvent) => _emit(e),
        };

        // ── Share bridge ──────────────────────────────────────────────────────
        _getState = function() {
          return {
            primary: (ctx.mapPrimary || '2019') as MapKey,
            mapOn:   { minority: ctx.mapOn.minority, majority: ctx.mapOn.majority, '2019': ctx.mapOn['2019'] },
            layers:  { vote: ctx.layerState.vote, 'ed-fill': ctx.layerState['ed-fill'], 'ed-lines': ctx.layerState['ed-lines'], eg: ctx.layerState.eg },
            viewport: ctx.svgEl && ctx.natVB && ctx.curVB ? {
              cx_norm: Math.max(0, Math.min(1, (ctx.curVB.x + ctx.curVB.w / 2 - ctx.natVB.x) / ctx.natVB.w)),
              cy_norm: Math.max(0, Math.min(1, (ctx.curVB.y + ctx.curVB.h / 2 - ctx.natVB.y) / ctx.natVB.h)),
              zoom:    ctx.curVB.w / ctx.natVB.w,
            } : { cx_norm: 0.5, cy_norm: 0.5, zoom: 1.0 },
          };
        };
        _applyStateFn = function(primary: MapKey, targetMapOn: Record<MapKey, boolean>, targetLayers: Record<LayerKey, boolean>) {
          ctx.mapPrimary       = primary;
          ctx.mapOn.minority   = !!targetMapOn.minority;
          ctx.mapOn.majority   = !!targetMapOn.majority;
          ctx.mapOn['2019']    = !!targetMapOn['2019'];
          ctx.mapActivationOrder = (['minority', 'majority', '2019'] as const).filter(function(k) { return ctx.mapOn[k]; });
          const pi = ctx.mapActivationOrder.indexOf(primary);
          if (pi !== -1) { ctx.mapActivationOrder.splice(pi, 1); ctx.mapActivationOrder.push(primary); }
          _doSwitchPrimary(primary);
          _syncOverlays();
          (['vote', 'ed-fill', 'ed-lines', 'eg'] as const).forEach(function(k) {
            const on = !!targetLayers[k];
            ctx.layerState[k] = on;
            const btn = document.querySelector('.tb-btn[data-layer="' + k + '"]');
            if (btn) btn.classList.toggle('tb-layer-on', on);
            if (k === 'vote')     applyVoteLayer(ctx, on);
            if (k === 'ed-fill')  applyEdFillLayer(ctx, on);
            if (k === 'ed-lines') applyEdLinesLayer(ctx, on);
            if (k === 'eg')       applyEGLayer(ctx, on);
          });
          _updateMapButtons();
        };
        function _emit(event: MapEngineEvent) { if (_onEvent) _onEvent(event); }

        // ── Maps thin wrappers ────────────────────────────────────────────────────
        function _applyBoundaryColor(svgNode: SVGSVGElement, mapKey: MapKey | null) { mpApplyBoundaryColor(ctx, svgNode, mapKey); }
        function _syncOverlays()                       { mpSyncOverlays(ctx, _mapsDeps); }
        function _updateMapButtons()                   { mpUpdateMapButtons(ctx, _mapsDeps); }
        function _doSwitchPrimary(key: MapKey)         { mpDoSwitchPrimary(ctx, key, _mapsDeps); }
        function _activateAsTop(key: MapKey)           { mpActivateAsTop(ctx, key, _mapsDeps); }
        function toggleMap(key: MapKey)                { mpToggleMap(ctx, key, _mapsDeps); }

        // ── Active ED boundary highlight ──────────────────────────────────────────
        function _setEdHighlight(p: SVGGraphicsElement) { setEdHighlight(ctx, p); }
        function _activateCenterED() { activateCenterED(ctx, _animateToVB, _emit); }

        document.querySelectorAll<HTMLElement>('.tb-btn[data-map]').forEach(function(b) {
          b.addEventListener('click', function() {
            const key = b.dataset.map as MapKey | undefined;
            if (key) toggleMap(key);
          });
        });

        const _ecCloseBtn = document.getElementById(DOM_IDS.ecClose);
        if (_ecCloseBtn) _ecCloseBtn.addEventListener('click', _hideCallout);

        // ── Lazy map-data load (fired on first overlay open) ──────────────────
        // Defers 6 JSON downloads from init to first open so the page-load
        // critical path stays empty of map-tool work. The primeOnce gate in
        // overlay.ts ensures this runs at most once per session.
        function _primeMapData() {
          mpLoadHoverJson(ctx, 'minority', _mapJsonUrls.minority);
          mpLoadHoverJson(ctx, 'majority', _mapJsonUrls.majority);
          mpLoadHoverJson(ctx, '2019',    _mapJsonUrls['2019']);
          mpLoadVaJson(ctx, 'minority', _mapVaJsonUrls.minority);
          mpLoadVaJson(ctx, 'majority', _mapVaJsonUrls.majority);
          mpLoadVaJson(ctx, '2019',    _mapVaJsonUrls['2019']);
        }

        const vcClose = document.getElementById(DOM_IDS.vcClose);
        if (vcClose) vcClose.addEventListener('click', function() { hideVaCallout(ctx); });

        document.querySelectorAll<HTMLElement>('.tb-btn[data-layer]').forEach(function(b) {
          b.addEventListener('click', function() {
            const key = b.dataset.layer;
            if (!key) return;
            if (key === 'lock') {
              ctx.mapLocked = !ctx.mapLocked;
              b.classList.toggle('tb-layer-on', ctx.mapLocked);
              return;
            }
            const lKey = key as LayerKey;
            const on = !ctx.layerState[lKey];
            setLayerOn(ctx, lKey, on, _emit);
            if (lKey === 'ed-fill' && on && ctx.layerState['eg'])      setLayerOn(ctx, 'eg', false, _emit);
            if (lKey === 'eg'      && on && ctx.layerState['ed-fill']) setLayerOn(ctx, 'ed-fill', false, _emit);
          });
        });

        // ── Snap-to-ED animation ───────────────────────────────────────────────
        function _animateToVB(targetVB: ViewBox, dur: number) { vpAnimateToVB(ctx, targetVB, dur); }
        function _snapToED(pathEl: SVGGraphicsElement, force?: boolean) { snapToED(ctx, pathEl, !!force, _animateToVB, _getStageRect); }

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
        const _helpBtn = document.getElementById(DOM_IDS.tbHelpBtn);
        if (_helpBtn) {
          _helpBtn.addEventListener('click', () => {
            const modal = document.getElementById(DOM_IDS.mapIntroModal);
            if (modal) modal.style.display = 'flex';
          });
        }

        async function _maybeShowIntro() {
          if (await hasSeenIntro()) return;
          var modal = document.getElementById(DOM_IDS.mapIntroModal);
          if (modal) modal.style.display = 'flex';
        }

      })();
}
