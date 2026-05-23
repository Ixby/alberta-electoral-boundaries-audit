# Multi-Select Electoral Districts (Desktop)

**Status:** Proposal — pending implementation
**Branch:** `claude/busy-ride-DmwUm`
**Scope:** Desktop interaction only. Mobile is hypothesized but explicitly out of scope.

## Goal

Let users select multiple Electoral Districts at once via `Ctrl`/`⌘` + click. Each selected ED gets its own info card; cards stack in a responsive grid in the existing right-side panel. Each selection is color-coded so the user can pair a card with its highlighted polygon on the map.

## Current architecture (baseline)

- Vanilla JS in `viewer/src/lib/mapEngine.ts`. No framework state.
- Single static callout DOM (`#ed-callout`) in `viewer/src/routes/+page.svelte` (lines 881–909).
- One global `_selectedEdName: string | null` (`mapEngine.ts:500`) tracks selection.
- One global `_highlightPath: SVGGElement | null` (`mapEngine.ts:501`) tracks the SVG highlight `<g>`.
- Selection mutation entry points:
  - Pointer click (desktop): `mapEngine.ts:941–951`
  - Touch tap / double-tap: `mapEngine.ts:924–940`
  - Close button: `mapEngine.ts:686`
  - Escape (in overlay context): `mapEngine.ts:343`
  - Empty-area click: `mapEngine.ts:949`
  - Search dropdown: `mapEngine.ts:1001`
  - Inline article ed-triggers: `mapEngine.ts:1185`
  - Map switch persistence: `mapEngine.ts:598–614`
  - Center activation: `mapEngine.ts:543`

## Resolved design decisions

| Question | Decision |
|---|---|
| Zoom behavior on additive add | Zoom to fit all selected EDs (combined bounding box) |
| How to pair card ↔ highlight | Per-selection accent color (6-color palette) + numeric badge as color-blind fallback |
| Empty-area click w/ modifier held | No-op (modifier = additive; only plain empty click clears) |
| Selection cap | Hard cap of 6 (matches palette size); 7th click flashes counter, is no-op |
| Mobile | Not implemented in this pass |

## State refactor

Replace the two globals in `mapEngine.ts:500–501`:

```ts
const _selectedEds = new Map<string /* ED name */, {
  rec: EdRec;              // hover record from _edHover
  pathEl: SVGPathElement;  // polygon in the current SVG
  highlightEl: SVGGElement;// glow+sharp group appended to svgEl
  cardEl: HTMLElement;     // card in #ec-stack
  color: string;           // assigned palette hex
  index: number;           // 1-6, used for the badge
}>();

const _colorPalette = [
  '#E63946', // red
  '#F4A261', // orange
  '#2A9D8F', // teal-green
  '#4361EE', // blue
  '#B5179E', // magenta
  '#F1C453', // yellow
];

const _colorInUse = new Set<string>();
```

`Map` preserves insertion order → renders correspond to grid insertion. Color is allocated by scanning the palette for the first unused entry; freed on `_removeSelection`.

## DOM refactor

Replace innards of `#ed-callout` in `+page.svelte:881–909`:

```html
<div id="ed-callout" aria-live="polite">
  <div id="ec-stack-header" hidden>
    <span id="ec-count">0 selected</span>
    <button id="ec-clear-all" type="button">Clear all ×</button>
  </div>
  <div id="ec-stack"></div>
  <div id="ec-hint">⌘/Ctrl-click to compare districts</div>
</div>

<template id="ec-card-template">
  <div class="ec-card">
    <div class="ec-accent"></div>
    <span class="ec-badge"></span>
    <button class="ec-close" type="button" aria-label="Remove">×</button>
    <div class="ec-header">
      <div class="ec-name"></div>
      <div class="ec-context"></div>
    </div>
    <div class="ec-bar"><div class="ec-ucp-bar"></div><div class="ec-ndp-bar"></div></div>
    <div class="ec-split">
      <div class="ec-party ec-ucp">
        <span class="ec-pct ec-ucp-pct"></span>
        <span class="ec-party-name">UCP</span>
        <span class="ec-votes ec-ucp-votes"></span>
      </div>
      <div class="ec-party ec-ndp">
        <span class="ec-pct ec-ndp-pct"></span>
        <span class="ec-party-name">NDP</span>
        <span class="ec-votes ec-ndp-votes"></span>
      </div>
    </div>
    <div class="ec-meta">
      <span class="ec-total-votes"></span><span class="ec-dot">·</span>
      <span class="ec-va-count"></span><span class="ec-dot">·</span>
      <span class="ec-pop"></span>
    </div>
    <div class="ec-eg-row"><span class="ec-eg-label">EG</span> <span class="ec-eg"></span></div>
    <div class="ec-compare"></div>
  </div>
</template>
```

**Critical**: every `#ec-*` ID inside the existing callout becomes a `.ec-*` class within the template (IDs must be unique; classes can repeat across 6 cards).

`_showCallout(d)` is replaced by `_renderCard(rec, color, index) → HTMLElement` that clones the template, fills via `card.querySelector('.ec-name')` etc., wires the per-card `.ec-close` to `_removeSelection(rec.name)`.

## Grid layout

Current cards waste horizontal space at full-panel width. New grid:

```css
#ed-callout              { width: clamp(260px, 33vw, 360px); transition: width 0.22s ease; }
#ed-callout.ec-multi     { width: clamp(360px, 55vw, 720px); }

#ec-stack {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 0.5rem;
  padding: 0.5rem 0;
}

.ec-card {
  position: relative;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px;
  padding: 0.55rem 0.7rem 0.65rem;
  background: rgba(255,255,255,0.02);
  animation: ec-card-in 0.18s ease both;
}
.ec-accent {
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  border-radius: 6px 6px 0 0;
  background: var(--card-color);
}
.ec-badge {
  position: absolute; top: 0.4rem; right: 1.7rem;
  font-size: 0.65rem; font-weight: 700;
  padding: 0.05rem 0.32rem;
  border-radius: 3px;
  color: var(--card-color);
  border: 1px solid currentColor;
}
.ec-close {
  position: absolute; top: 0.2rem; right: 0.35rem;
  background: none; border: none;
  color: rgba(255,255,255,0.45);
  font-size: 1.1rem; line-height: 1; cursor: pointer;
  padding: 0.15rem 0.3rem;
}
.ec-close:hover { color: #fff; }

@keyframes ec-card-in { from { opacity: 0; transform: scale(0.96); } to { opacity: 1; transform: none; } }
@keyframes ec-card-out { to { opacity: 0; transform: scale(0.96); } }
.ec-card.ec-removing { animation: ec-card-out 0.14s ease forwards; }

#ec-stack-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.4rem 0.1rem 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.06);
  font-size: 0.75rem; color: rgba(255,255,255,0.55);
}
#ec-clear-all {
  background: none; border: none; color: rgba(255,255,255,0.55);
  cursor: pointer; font-size: 0.72rem;
}
#ec-clear-all:hover { color: #fff; }

#ec-hint {
  position: sticky; bottom: 0;
  font-size: 0.65rem; color: rgba(255,255,255,0.35);
  padding: 0.4rem 0; text-align: center;
  border-top: 1px solid rgba(255,255,255,0.05);
}
#ed-callout.ec-multi #ec-hint { display: none; } /* user has already discovered it */
```

Column count follows naturally from `minmax(170px, 1fr)`:
- 1 selection → narrow panel → 1 column
- 2–4 → wide panel → 2 columns
- 5–6 → wide panel → 3 columns

Content density inside each ~170–200px card stays close to current; only the cross-map "Other maps" row drops the loser-pct to fit width.

## Click handler refactor

Replace `mapEngine.ts:941–951` (desktop branch of `pointerup`):

```js
} else if (_edHover) {
  if (e.button !== 0) { drag = null; return; }   // primary button only
  const hit = _tipTarget(e);
  if (hit) {
    _hideTip();
    const rec = _edHover[parseInt(hit.getAttribute('data-ed-id'), 10)];
    const additive = e.ctrlKey || e.metaKey;
    if (additive) {
      if (_selectedEds.has(rec.name)) {
        _removeSelection(rec.name);                // toggle off
      } else if (_selectedEds.size < 6) {
        _addSelection(rec, hit);
      } else {
        _flashCapNotice();
      }
      if (!_mapLocked) _zoomToFitAll();
    } else {
      _clearAllSelections();
      _addSelection(rec, hit);
      if (!_mapLocked) _snapToED(hit);             // single-click zoom unchanged
    }
  } else if (!(e.ctrlKey || e.metaKey)) {
    _clearAllSelections();                         // plain empty click clears
  }                                                 // modifier+empty = no-op
}
```

Also add, alongside the existing pointer listeners:

```js
stage.addEventListener('contextmenu', e => {
  if (e.ctrlKey || e.metaKey) e.preventDefault();  // suppress Mac ctrl-click menu
});
```

## New helpers (in `mapEngine.ts`)

```js
function _allocColor() {
  for (const c of _colorPalette) if (!_colorInUse.has(c)) { _colorInUse.add(c); return c; }
  return null;  // shouldn't happen given the cap
}
function _freeColor(c) { _colorInUse.delete(c); }

function _addSelection(rec, pathEl) {
  if (_selectedEds.has(rec.name)) return;          // idempotent guard
  const color = _allocColor();
  if (!color) return;
  const index = _selectedEds.size + 1;             // 1-based for the badge
  const highlightEl = _buildHighlight(pathEl, color);
  const cardEl = _renderCard(rec, color, index);
  svgEl.appendChild(highlightEl);
  document.getElementById('ec-stack').appendChild(cardEl);
  _selectedEds.set(rec.name, { rec, pathEl, highlightEl, cardEl, color, index });
  _refreshStackChrome();
}

function _removeSelection(name) {
  const entry = _selectedEds.get(name);
  if (!entry) return;
  entry.highlightEl.remove();
  entry.cardEl.classList.add('ec-removing');
  setTimeout(() => entry.cardEl.remove(), 140);    // matches animation
  _freeColor(entry.color);
  _selectedEds.delete(name);
  _renumberBadges();                                // keep 1..N contiguous
  _refreshStackChrome();
}

function _clearAllSelections() {
  for (const entry of _selectedEds.values()) {
    entry.highlightEl.remove();
    entry.cardEl.remove();
    _freeColor(entry.color);
  }
  _selectedEds.clear();
  _refreshStackChrome();
}

function _refreshStackChrome() {
  const n = _selectedEds.size;
  const callout = document.getElementById('ed-callout');
  const header  = document.getElementById('ec-stack-header');
  const count   = document.getElementById('ec-count');
  callout.classList.toggle('ec-visible', n > 0);
  callout.classList.toggle('ec-multi',   n > 1);
  header.hidden = n <= 1;
  count.textContent = n + ' selected';
}

function _zoomToFitAll() {
  if (!svgEl || mode !== 'viewbox' || _selectedEds.size === 0) return;
  if (_zoomRafId) { cancelAnimationFrame(_zoomRafId); _zoomRafId = null; }
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const s of _selectedEds.values()) {
    const bb = s.pathEl.getBBox();
    if (bb.x < minX) minX = bb.x;
    if (bb.y < minY) minY = bb.y;
    if (bb.x + bb.width  > maxX) maxX = bb.x + bb.width;
    if (bb.y + bb.height > maxY) maxY = bb.y + bb.height;
  }
  const combined = { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
  if (_isEdVisible(combined)) return;              // already in view — no animation
  const pad = Math.max(combined.width, combined.height) * 0.25;
  let tw = combined.width + pad*2, th = combined.height + pad*2;
  const r = _getStageRect();
  if (tw/th < r.width/r.height) tw = th * r.width / r.height;
  else                          th = tw * r.height / r.width;
  const cx = combined.x + combined.width/2, cy = combined.y + combined.height/2;
  _animateToVB({ x: cx - tw/2, y: cy - th/2, w: tw, h: th }, 280);
}
```

## Highlight refactor

`_setEdHighlight` (`mapEngine.ts:502`) → `_buildHighlight(pathEl, color)` that returns the `<g>` instead of storing it globally. Color comes from the palette instead of `_mapAccentColors`. Also append a `<text>` numeric badge centered on the polygon's bbox:

```js
function _buildHighlight(pathEl, color) {
  const d = pathEl.getAttribute('d');
  const g = document.createElementNS(NS_SVG, 'g');
  g.setAttribute('pointer-events', 'none');
  // glow (unchanged structure, color swapped)
  // sharp outline (unchanged structure, color swapped)
  // numeric label at bbox centroid (small white text on color halo)
  return g;
}
```

`_clearEdHighlight` (`mapEngine.ts:529`) is no longer needed — highlights are removed per-entry via `entry.highlightEl.remove()`.

## Other call-site updates

| Site | Was | Becomes |
|---|---|---|
| `mapEngine.ts:543` (`_activateCenterED`) | `_showCallout + _setEdHighlight` | `_clearAllSelections(); _addSelection(rec, path)` |
| `mapEngine.ts:614` (map-switch restore) | restores one selected name | restores list (see Map switch section) |
| `mapEngine.ts:686` (close-btn listener) | wires `#ec-close` | remove this line; new per-card closes are wired in `_renderCard` |
| `mapEngine.ts:1001` (search result) | `_showCallout + _setEdHighlight` | `_clearAllSelections(); _addSelection(rec, path)` |
| `mapEngine.ts:1185` (article ed-trigger) | `_showCallout + _setEdHighlight` | `_clearAllSelections(); _addSelection(rec, path)` |
| `mapEngine.ts:343` (Escape in overlay) | `_hideCallout` | `_clearAllSelections` |
| `mapEngine.ts:927` (touch double-tap) | `_hideCallout` | `_clearAllSelections` |
| Touch single-tap (`mapEngine.ts:935`) | `_showCallout + _setEdHighlight` | `_clearAllSelections(); _addSelection(rec, hit)` (single-select on touch) |
| Touch empty-tap (`mapEngine.ts:938`) | `_hideCallout` | `_clearAllSelections` |

## Map switch persistence

Generalize `_doSwitchPrimary` (`mapEngine.ts:595–620`):

```js
const saved = [..._selectedEds.values()].map(s => ({ name: s.rec.name, color: s.color }));
_clearAllSelections();
// ...load new SVG...
// after _activateInlineSVG and _edHover assignment:
for (const { name, color } of saved) {
  const rec = _nameIndex[key] && _nameIndex[key][name];
  if (!rec) continue;                              // ED absent in new map — drop
  const path = svgEl && svgEl.querySelector('[data-ed-id="' + rec.id + '"]');
  if (!path) continue;
  // Re-add preserving original color slot:
  _colorInUse.add(color);
  _addSelectionWithColor(rec, path, color);        // variant that skips _allocColor
}
```

Names absent from the new map are silently dropped — consistent with the existing "boundary unique to this map" notion.

## Risk audit

### Performance
- Highlight `<g>` re-mount on duplicate add: idempotency guard in `_addSelection`.
- `_zoomToFitAll` queueing: stored `_zoomRafId` cancellation; short-circuit when combined bbox is already visible (mirror `_isEdVisible:836`).
- `getBBox` cost: triggers layout, called ≤ 6 times per add. Negligible.

### Race conditions
- Map switch mid-click: existing `_edHover` truthiness guard in pointerup handler covers it (`_doSwitchPrimary` sets it to null at line 600).
- Stale `pathEl` refs across map switches: mitigated by explicit `_clearAllSelections` before remount.

### Bugs
- **Mac ctrl-click = secondary click + contextmenu**: filter on `e.button === 0`; add `contextmenu` listener with `preventDefault` when modifier is held. Mac users naturally use `metaKey`.
- **Dead listener on `#ec-close`**: line `mapEngine.ts:686` must be deleted since the button is removed from the DOM.
- **Escape key currently calls `_hideCallout`**: confirm scope (it's inside the overlay keyhandler at line 343) before changing to `_clearAllSelections` — verify it doesn't run during normal map use.
- **`innerHTML` in `#ec-compare`** (`mapEngine.ts:441`): current data is numeric, safe. Flag for future hardening if ED names ever enter that template.

### Overloads / DoS
- Hard cap of 6 prevents stack stuffing.
- No async/network on selection — fully in-memory.

### Injection
- No LLM in path → no prompt-injection surface.
- ED name uses `textContent` (safe). Numeric fields safe. `ec-compare innerHTML` flagged above.
- Color palette is static.

### UX
- **Discoverability**: `#ec-hint` line at panel bottom; hidden once `size > 1` (user has clearly discovered it).
- **Color-blind safety**: numeric badge (1–6) on every card and on every highlight serves as a non-color pairing cue.
- **Touchscreen-desktop users** can't multi-select (no modifier key on tap). Acknowledged gap. Resolved with the future "compare mode" toggle (see Mobile section).

## Mobile (hypothesis only — not implementing)

The bottom-sheet panel (`max-width: 700px`, `height: min(280px, 33vh)` per `+page.svelte:1467`) can't sensibly stack 6 cards vertically. Three viable paths for a future pass:

1. **Long-press = additive.** Tap = replace; long-press = toggle in stack. Needs onboarding tooltip.
2. **"Compare mode" toolbar toggle.** When on, every tap is additive; when off, tap replaces. Mode is explicit and teachable.
3. **Horizontal carousel** of cards instead of vertical stack — fixed-height sheet with swipe + dot pagination.

**Recommendation** when picked up: option 2 + option 3 combined. Explicit mode toggle beats a hidden gesture; the carousel keeps the bottom sheet at a fixed height.

## Out of scope (for future PRs)

- Shareable URL hash encoding the selected names.
- Persisting selection in `sessionStorage` across reload.
- `Shift`-click on inline article `ed-trigger` buttons to append.
- A side-by-side compare table view (different UI, same state).

## Files touched

| File | Change |
|---|---|
| `viewer/src/lib/mapEngine.ts` | State refactor, `_addSelection`/`_removeSelection`/`_clearAllSelections`/`_renderCard`/`_buildHighlight`/`_zoomToFitAll`/`_refreshStackChrome`/`_renumberBadges`/`_flashCapNotice`; pointerup handler rewrite; contextmenu suppress; updates to search, ed-trigger, center activation, map switch, Escape, touch branches |
| `viewer/src/routes/+page.svelte` | Replace `#ed-callout` innards; add `<template id="ec-card-template">`; new grid CSS; `.ec-multi` width transition; card-in/out animations; per-card class-based selectors |

## Acceptance criteria

- Ctrl/⌘-click on an unselected ED adds a card and a same-colored highlight; cap at 6.
- Ctrl/⌘-click on a selected ED toggles it off (card + highlight removed; color freed).
- Plain click replaces the entire selection with one ED and snap-zooms to it.
- Additive add (when not locked) zooms to fit all selections; skipped if already in view.
- Plain empty-area click clears all. Modifier + empty-area click is a no-op.
- Escape clears all. Per-card × removes that card. "Clear all" appears only when size > 1.
- Map switch preserves selection by name; same colors re-applied; missing-name selections dropped.
- Mac users don't see a context menu on ⌘-click or Ctrl-click on EDs.
- Color-blind users can pair cards to highlights via the numeric badge.
- Touch interaction (where it exists) continues to work as single-select.
