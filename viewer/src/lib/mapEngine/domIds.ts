// Alberta Electoral Boundary Audit — DOM ID registry
// © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
//
// Single source of truth for every element ID the engine reaches into.
// Adding/renaming an ID here will surface every callsite via TypeScript;
// renaming the element in +page.svelte without updating this file is the
// only way it can break, and it will break at the registry boundary, not
// silently in a leaf module that returns null from getElementById.

// IDs owned by the host page (+page.svelte).
export const DOM_IDS = {
  // Zoom viewer / overlay shell
  zoomOverlay:    'zoom-overlay',
  zoomStage:      'zoom-stage',
  zoomObj:        'zoom-obj',
  zoomClose:      'zoom-close',
  zoomPct:        'zoom-pct',
  zoomSlider:     'zoom-slider',
  zoomSkeleton:   'zoom-skeleton',

  // ED callout (info bar)
  edCallout:      'ed-callout',
  edTooltip:      'ed-tooltip',
  ecClose:        'ec-close',
  ecName:         'ec-name',
  ecContext:      'ec-context',
  ecEg:           'ec-eg',
  ecPop:          'ec-pop',
  ecCompare:      'ec-compare',
  ecUcpBar:       'ec-ucp-bar',
  ecUcpPct:       'ec-ucp-pct',
  ecUcpVotes:     'ec-ucp-votes',
  ecNdpBar:       'ec-ndp-bar',
  ecNdpPct:       'ec-ndp-pct',
  ecNdpVotes:     'ec-ndp-votes',
  ecTotalVotes:   'ec-total-votes',
  ecVaCount:      'ec-va-count',
  ecVaHint:       'ec-va-hint',

  // VA callout (polling-area detail)
  vaCallout:      'va-callout',
  vcClose:        'vc-close',
  vcName:         'vc-name',
  vcTotal:        'vc-total',
  vcUcpBar:       'vc-ucp-bar',
  vcUcpPct:       'vc-ucp-pct',
  vcNdpBar:       'vc-ndp-bar',
  vcNdpPct:       'vc-ndp-pct',

  // Toolbar
  tbHelpBtn:      'tb-help-btn',
  tbSearch:       'tb-search',
  tbSearchResults:'tb-search-results',

  // Intro modal + misc HUD
  hud:            'hud',
  mapIntroModal:  'map-intro-modal',
  mapIntroClose:  'map-intro-close',
  mapLoadError:   'map-load-error',
  srAnnounce:     'sr-announce',
} as const;

// IDs that live inside the loaded SVG document (upstream from cover_art_*.svg).
// Renaming any of these requires regenerating SVGs from the source pipeline,
// so they are listed here for documentation; not part of the typo-safety story.
export const SVG_INNER_IDS = {
  lineCollection1: 'LineCollection_1',
  patchCollection1:'PatchCollection_1',
  patchCollection2:'PatchCollection_2',
  edBoundaryLayer: 'ed_boundary_layer',
  edHoverLayer:    'ed_hover_layer',
  vaHoverLayer:    'va_hover_layer',
} as const;
