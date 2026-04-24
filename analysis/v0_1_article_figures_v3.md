# Article figures v3 — design note

Brief design note for the four magazine-ready article figures produced by
`analysis/v0_1_build_article_figures_v3.py`. Replaces the v2 two-panel
geographic overlays, which were rejected for being informationally dense
and hard to read at column width.

## Design premise

Three of the four figures — Airdrie, Lethbridge, Red Deer — tell a story
about *partition count* ("how many districts is this city split into?")
rather than *geography* ("where in space do the districts sit?"). A
geographic map is the wrong visual metaphor for a partition claim. The
magazine tradition is to use schematic infographics for claims about
categorical structure, reserving real maps for claims that require
geographic fidelity.

The Calgary figure is the exception. The minority's Calgary-named hybrids
reach in specific compass directions — northwest toward Cochrane, south
toward High River, west across the Tsuut'ina boundary — and that spatial
character is part of the claim. v3 keeps a geographic metaphor for
Calgary but strips it to minimum: municipal outline plus three highlighted
hybrids, no interior ED lines, no labelled neighbours.

## Figures

### Figure 1. Airdrie — schematic

Two horizontal bars stacked vertically. Top bar shows the majority's two
Airdrie-named ridings as equal segments. Bottom bar shows the minority's
three segments (Airdrie East, Calgary-Foothills-Airdrie West,
Olds-Three Hills-Didsbury), with the rural-carve segment rendered in a
muted umber tone so the reader sees "this slice belongs to something
that is not Airdrie." The rural segment is drawn narrower (proportion
0.45) because it represents only the sliver of Airdrie that the minority
attaches to a rural district.

### Figure 2. Lethbridge — schematic with rural-pulls inset

Two bars plus a small right-hand column listing the three rural
communities each Lethbridge-prefixed hybrid pulls in (Cardston,
Fort MacLeod, Lomond). The middle segment label is abbreviated to
"Lethbridge-Fort MacLeod" with the rural extension "+ Crowsnest Pass"
shown as a sublabel so the full name "Lethbridge-Fort MacLeod-Crowsnest
Pass" fits in the segment without overflowing. The unabbreviated name is
reconstructable from the sublabel.

### Figure 3. Red Deer — schematic

Four equal segments on each bar. Majority bar shows the two compact city
ridings (Red Deer-North, Red Deer-South) in orange alongside two rural
districts (Lacombe-Clearwater, Sylvan Lake-Innisfail) in the rural
umber. Minority bar shows four Red Deer-prefixed hybrids in the teal
family.

### Figure 4. Calgary — minimal geographic

Single map showing the Calgary municipal boundary in light grey with
three minority hybrids overlaid in teal: Calgary-Nolan Hill-Cochrane
(NW), Calgary-De Winton (S), Calgary-West-Tsuut'ina (W). Labels are
placed in white boxes with short leader lines to the rural tail of each
hybrid (computed as the geometric difference between the hybrid polygon
and the Calgary polygon, so the line points at the rural part of the
district rather than the Calgary part). Scale bar, compass rose, subtle
CALGARY label inside the municipal outline. Rivers are omitted; they
were not essential to the claim and added visual noise at page width.

## Palette

| Role                | Hex       | Notes                                        |
|---------------------|-----------|----------------------------------------------|
| Page background     | `#faf6ee` | Warm ivory                                   |
| Ink                 | `#141414` | Near-black                                   |
| Soft ink            | `#3a3a3a` | Body text, sublabels on light fills          |
| Muted grey          | `#8a8a8a` | Credit and caveat lines                      |
| Majority segment 1  | `#e07a1c` | Saturated orange                             |
| Majority segment 2  | `#f2a14e` | Softer tangerine                             |
| Majority segment 3  | `#c95a0c` | Deeper burnt orange                          |
| Majority segment 4  | `#f5c38a` | Pale ochre                                   |
| Minority segment 1  | `#2f6b7a` | Teal                                         |
| Minority segment 2  | `#4d92a3` | Lighter teal                                 |
| Minority segment 3  | `#254a5a` | Deep slate                                   |
| Minority segment 4  | `#79b1bc` | Pale teal                                    |
| Rural carve         | `#8b5a2b` | Muted umber — "this slice is not the city"   |

Labels on segments with luma < 0.45 automatically flip to white / pale
ivory for contrast.

## Fonts

Per spec: Playfair Display bold for titles, Source Sans 3 for body /
labels. Neither is installed on this Windows build, so the script falls
through to `Georgia` for titles and `Arial` for labels — both are
system fonts present on essentially all Windows installs, so no
font-fallback warning is emitted. Installing the spec fonts would
produce identical geometry with the designer's choice of typeface.

## Honest caveats

- **Schematic bar proportions are not a data encoding.** The story in
  these three figures is partition count, not geography or population
  share. Segments are drawn with near-uniform widths because "how many"
  is the claim. The Airdrie rural-carve segment is drawn narrower
  (proportion 0.45) for visual honesty — it represents only the sliver
  of the city that the minority attaches to the northward rural district,
  not an equal third of the partition. This is the one place in the
  schematics where bar width carries a rough quantitative signal.
- **Bar schematics abstract away shape and population.** The majority
  Red Deer rural segments (Lacombe-Clearwater, Sylvan Lake-Innisfail)
  are drawn the same width as the compact city segments, even though the
  rural districts are geographically larger and have different
  populations. The figure is making a structural claim, not a population
  or area claim.
- **Calgary-West-Tsuut'ina has no transcribed 2026 polygon.** In the v7
  minority gpkg it has tier `C-null`. The Calgary map falls back to the
  2019 Calgary-West polygon as a visual approximation of the district's
  spatial footprint. This is called out in a caveat line below the map's
  caption, and in the figure 4 caption in the article itself.
- **Lethbridge inset is diagrammatic, not to scale.** The small rural
  markers next to the minority bar are labels of which communities each
  hybrid pulls in, not a geographic inset. Three markers, three hybrids,
  three pulls. No spatial fidelity is claimed.
- **Rivers omitted from Calgary.** The Bow and Elbow are usually helpful
  for Calgary-orientation, but at page width they added visual clutter
  without advancing the claim about rural-territory pulls. Decision to
  omit was honest minimisation rather than a technical limitation.

## Outputs

- `maps/article/figure_airdrie_v3.png` — 2100 × 1401 px, 300 dpi
- `maps/article/figure_lethbridge_v3.png` — 2100 × 1401 px, 300 dpi
- `maps/article/figure_reddeer_v3.png` — 2100 × 1401 px, 300 dpi
- `maps/article/figure_calgary_v3.png` — 2100 × 1401 px, 300 dpi

v2 overlays (`overlay_*_v2.png`) are retained on disk per the task
directive and are no longer referenced by `report_public.md`.
