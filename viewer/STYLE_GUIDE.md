# Alberta Electoral Boundary Audit — Style Guide

The single reference for the report site's visual and editorial standards. It
records the conventions already in use so new work stays consistent. When a rule
here conflicts with something in the code, the code should be brought to the
rule (see **Known inconsistencies** at the end).

> Scope: the SvelteKit viewer (`viewer/`) — the public report homepage, the map
> explorer, and the satellite routes (feedback, privacy, law, methods).

---

## 1. Colour

### 1.1 Partisan colours (the parties' official brand palette)

These are the **only** colours used to represent the two parties. One token each
— no near-duplicates.

| Token | Hex | Use |
|---|---|---|
| **NDP orange** | `#F58220` | Map VA fills, tooltip bar fills, any NDP swatch |
| NDP orange (on-light text) | `#AB5B16` | NDP **text** on the warm-paper tooltip/light bg (the brand orange fails WCAG AA as small text; this darkened variant clears it at 4.63:1) |
| **UCP blue** | `#1C4583` | Map VA fills, tooltip bar fills, UCP text/swatch |
| UCP green (accent) | `#136936` | Reserved; not currently used |

Sources: NDP `#F58220` = Pantone 1505 C (NDP branding toolkit); UCP `#1C4583` =
dominant fill of the official UCP 2026 logo. The map VA fill is a direct
`#F58220 ↔ #1C4583` ramp (`build_cover.py`), with **population encoded as
lightness** (dense = saturated, empty = white). Any change to these endpoints
requires re-running `build_explorer_tiles.py` and re-rendering the hero cover art.

**Accessibility:** the partisan pair must stay colour-blind-safe. The current
pair tests ΔE 90–117 across protanopia/deuteranopia/tritanopia (Machado 2009).
Re-check with the CVD simulation before changing either endpoint.

### 1.2 Boundary-line colours (the three maps)

Per-map electoral-district boundary lines (`MAP_RGB` in `deckExplorer/layers.ts`).
Distinguished by hue **and** lightness, plus an alternating-dash pattern where
maps agree:

| Map | RGB | Hex |
|---|---|---|
| Minority proposal | `124, 58, 196` | `#7C3AC4` (purple) |
| Majority proposal | `88, 230, 212` | `#58E6D4` (teal) |
| 2019 / Official | `245, 197, 24` | `#F5C518` (yellow) |

### 1.3 UI palette (CSS custom properties)

Defined once at `:root` in the report homepage and inherited site-wide. **Use the
token, never the literal.**

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#f9f7f2` | `#1e1f26` |
| `--bg-alt` | `#f5f5f5` | `#26272f` |
| `--text` | `#1a1a1a` | `#dde2ed` |
| `--text-muted` | `#444` | `#9ea8c0` |
| `--text-subtle` | `#666` | `#7a8296` |
| `--lead` | `#333` | `#b8c2d8` |
| `--heading` | `#1a2e45` | `#9eb8d0` |
| `--heading-2` | `#243b53` | `#8aa6be` |
| `--link` | `#1a5276` | `#6ab0d8` |
| `--border` | `#ddd` | `#38394a` |
| `--border-subtle` | `#e8e8e8` | `#2e2f3e` |
| `--callout-bg` | `#eaf1f8` | (themed) |
| `--callout-warn` | `#fdfbe4` | (themed) |
| `--nav-bg` | `#1e3552` | `#111722` |
| `--nav-accent` | `#6FD3FB` | — |

Dark mode rides on the global `:root[data-theme="dark"]` attribute.

---

## 2. Typography

- **Display / headings:** `'Palatino Linotype', Palatino, Georgia, 'Times New
  Roman', serif` — the literary serif used for section headings, the opener
  block, and the opening epigraph.
- **Body / UI:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
  'Helvetica Neue', Arial, sans-serif`.
- **Reading measure:** `--measure: 92ch`. Running prose is capped at this width;
  figures, tables, and the map explorer stay full-width. Change in one place.
- Body copy ~17px / line-height ~1.65. No more than the established weights
  (400 body, 500 nav, 600 headings/emphasis).

---

## 3. Layout & spacing

- Desktop page sits in a centred **1000px** reading container (`.container`)
  inside a **1200px** app shell (`.app-shell`), on a darker surround.
- Section blocks use the boxed-card pattern (`.opener-block`: rounded card,
  1px `--border`, soft shadow, a 4px top accent gradient `--heading → --link →
  --nav-accent`).
- Callouts: amber preliminary-findings banner pattern for pending/under-review
  content; never hedge the prose to compensate — the banner carries the caveat.

---

## 4. Editorial voice

- Public report targets **Flesch–Kincaid grade 11** (overrides any higher
  default). Academic report targets ≤ grade 13.
- Plain, grounded prose. **No templated triads, no mirrored reversals, no emoji.**
- **No verdict** on whether a map "is a gerrymander" — describe the statistical
  position and the Charter s.3 / EBCA framing; let readers draw legal
  conclusions. "Gerrymander" has no legal definition in Canada.
- Every claim, number, quote, and citation is verified against a primary source
  before it is written (the grounding standard). Retracted findings move to the
  DOCUMENTED CORRECTIONS box — never deleted silently.

---

## 5. Internationalisation

- 19 locales. **English is the source of truth**; French is human-reviewed and
  first-class; the other 17 are AI machine translations (labelled to users,
  awaiting native review).
- New keys: add to `en.ts` (and `fr.ts`); other locales fall back to English via
  `t()` until a per-locale pass. Keep key names identical across locales.
- **Apostrophe-escaping rule (build-breaker):** locale files use single-quoted TS
  strings. Any value containing an apostrophe — including word-internal ones
  (Ukrainian `дев'ять`, Somali `su'aal`) — **must** be a double-quoted `"..."`
  string, or the build breaks. When unsure, double-quote.
- Don't give satellite pages their own language selector — they inherit the
  active language from the shared store.

---

## 6. Components & patterns

- **Nav:** dark bar (`--nav-bg`). Desktop shows a windowed prev/current/next
  scroll-spy (current centred, accent underline); the hamburger opens the full
  grouped TOC. The map explorer carries a return-to-report control (labelled bar
  on desktop, home icon on mobile).
- **Epigraph:** the opening exchange — muted italic serif for the challenge,
  upright serif for the reply, the ethic set off with a top rule.
- **Focus:** every interactive control has a visible `:focus-visible` ring.
- **Accessibility:** the explorer has a screen-reader text equivalent
  (`/explorer/text`); honour reduced-motion; maintain WCAG AA contrast for text.

---

## 7. Known inconsistencies (bring code to the guide)

- The **satellite routes** (`feedback`, `privacy-policy`) hardcode `#1a2e45`,
  `#1a5276`, `#f9f7f2` etc. instead of the `--heading` / `--link` / `--bg`
  tokens. They render correctly but should be migrated to the tokens so a theme
  change propagates. (Low priority; cosmetic-internal.)
- Resolved: the partisan colours were previously three near-duplicate oranges and
  two blues; now consolidated to the single brand tokens above.
