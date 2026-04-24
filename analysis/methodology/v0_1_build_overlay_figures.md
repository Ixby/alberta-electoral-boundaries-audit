# Article Overlay Figures — Majority vs Minority 2026 ED Proposals

**Generated:** 2026-04-22
**Script:** `analysis/scripts/v0_1_build_overlay_figures.py`
**Output directory:** `maps/article/`

## Purpose

Four publication-quality per-municipality translucent overlay maps that let a
reader see, at a glance, where the majority and minority 2026 ED proposals
agree, where they diverge, and how each plan partitions the same territory
into electoral divisions.

## Method

### Data inputs

| Source | Path | Used as |
|--------|------|---------|
| 2019 enacted ED shapefile | `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp` | (a) Dashed grey baseline reference; (b) 2019 polygon proxy for Tier C majority EDs missing from the approximate gpkg |
| Approximate majority 2026 | `data/v0_1_approximate_majority_2026_eds.gpkg` | Tier A (identity) + Tier B (union) majority polygons, 57 of 89 |
| Refined minority 2026 v5 | `data/v0_1_refined_v5_minority_2026_eds.gpkg` | All 70 minority polygons (A / B / C-approximated) |
| Majority 89-ED list | `data/v0_1_majority_2026_populations.csv` | Completeness check + target list |
| Majority rename crosswalk | `data/v0_1_majority_hybrid_crosswalk.csv` | Lineage for Tier C proxies |

The script prefers v5 minority shapes and falls back to v4 automatically
(`data/v0_1_refined_v4_minority_2026_eds.gpkg`) if v5 is absent.

### Geometry assembly

* **Majority polygons:** start with the 57 Tier A / B polygons in the gpkg.
  For the 32 missing Tier C majority EDs, assign the 2019 polygon(s) listed
  in `MAJORITY_TIER_C_2019_PROXIES` (inside the script) as a proxy. This is
  an honest fallback because the majority Tier C EDs largely preserve 2019
  urban cores with minor tweaks -- using the 2019 polygon is the closest
  readily available approximation. The proxies are flagged in the captions.
* **Minority polygons:** use v5 as-is.
* All layers reprojected to `EPSG:3401` (NAD83 / Alberta 10-TM Forest,
  metres) for area-preserving local rendering.

### Per-frame set algebra

For each municipality bounding box, we compute three zones explicitly via
shapely set operations:

```
only_maj = (⋃ majority_clipped) − (⋃ minority_clipped)
only_min = (⋃ minority_clipped) − (⋃ majority_clipped)
both     = (⋃ majority_clipped) ∩ (⋃ minority_clipped)
```

Each zone is filled with a distinct, non-transparent colour (vs the naive
alpha-blending approach, which yielded flat grey in the first draft).

| Zone | Fill | Fill alpha |
|------|------|-----------|
| Majority only | `#e87722` (UCP-ish orange) | 0.55 |
| Minority only | `#335c81` (dusty blue) | 0.55 |
| Both plans cover | `#8d5a3b` (mid brown) | 0.55 |

Each plan's partition lines are drawn **on top** of the fills with strong
contrasting edges, so the reader can see how each plan cuts the territory
even where both cover the same ground:

| Line | Colour | Style |
|------|--------|-------|
| Majority partitions | `#b74000` (deep orange/red) | solid 1.7 pt |
| Minority partitions | `#0b1d3a` (deep navy) | dashed (4/2.5) 1.7 pt |
| 2019 baseline | `#555555` (grey) | dashed 0.55 pt |
| Tier C minority (visually transcribed) | `#0a0a0a` (black) | dashed 1.6 pt |

### Labelling

Two-pass greedy placement:

1. Collect candidate labels from both plans' EDs whose clipped area exceeds
   ~1.2% of the frame.
2. Sort candidates by polygon area (largest first) and place each label only
   if no already-placed label is within 7% of the frame's shorter edge --
   this prevents the stacked-label problem visible in the first draft.

Shared names (an ED that appears in both plans with the same name) are
labelled once in black bold. Majority-only names are labelled in dark orange;
minority-only names in dark navy.

### Cartographic furniture

* Primary city marker: filled black circle with white halo + label box.
* Scale bar: 10 km (or 5 km for tighter frames).
* North arrow: simple N-arrow with white circle halo.
* Legend: upper-left, seven entries (3 fill + 3 line + optional Tier C marker).

### Output spec

* 8 in wide, height auto from bbox aspect + caption margin, 300 DPI.
* Saved at `maps/article/overlay_{slug}.png` with `bbox_inches='tight'`.
* Final pixel dimensions: ~2410 x ~2889 pixels (well above the required
  8-inch-at-300-DPI minimum of 2400 x 1200).

## Figures and captions

### 1. Calgary

**File:** `maps/article/overlay_calgary.png`
**Frame:** 70 km across (half-width 35 km) centred on Calgary (51.0447 N,
-114.0719 W)
**Visible EDs:** 36 majority (incl. Tier C proxies), 26 minority (2 of them
Tier C-approximated)

> **Calgary and its commuter belt.** Orange = majority-only territory; blue
> = minority-only territory; brown = both plans cover the same area. Where
> the plans diverge most visibly: the northwest corridor (blue-only, the
> minority's Nolan Hill / Cochrane lasso), Chestermere / Strathmore
> (blue-only, the minority's Chestermere-Strathmore splits the majority's
> Chestermere-Strathmore hybrid), and the south exurbs (blue-only, the
> minority's Calgary-De Winton / Calgary-South). Approximate 2026 geometry
> -- Elections Alberta has not released shapefiles. Tier A / B EDs inherit
> 2019 boundaries; Tier C minority EDs (heavy dashed black outline, if
> visible) are visually transcribed from commission thumbnails. Missing
> majority Tier C polygons are proxied from 2019. Minority shapes use v5
> refinement (improved Tier C shapes for De Winton, Calgary-South,
> Windermere).

**Reader cue:** watch the solid orange partition lines (majority) vs the
dashed navy partition lines (minority) cutting the brown-filled core
differently. The 4 vs 7 Calgary hybrid count shows up as the number of
dashed-vs-solid crossings along the city perimeter.

**Caveats specific to this figure:**
* Most Calgary-named Tier C majority EDs (Calgary-Bhullar-McCall,
  Calgary-Confluence, Calgary-East, Calgary-Falconridge-Conrich,
  Calgary-Glenmore-Tsuut'ina, Calgary-McKenzie, Calgary-Nose Creek,
  Calgary-Symons Valley, Calgary-West-Elbow Valley) are proxied from
  best-guess 2019 EDs. The proxy mapping is a low-confidence approximation
  of the majority plan's actual boundaries in these EDs.
* The 2 visible Tier C-approximated minority EDs (expected: Calgary-De
  Winton, Calgary-South) are sub-shapefile-grade, visually transcribed
  from commission thumbnails.

### 2. Red Deer

**File:** `maps/article/overlay_reddeer.png`
**Frame:** 54 km across (half-width 27 km) centred on Red Deer (52.2681 N,
-113.8117 W)
**Visible EDs:** 4 majority, 5 minority, 0 Tier C

> **The Red Deer area.** Orange = majority-only; blue = minority-only;
> brown = both plans cover the same territory. Both plans cover the same
> footprint -- but they name and partition it differently. The majority
> draws two compact city EDs (Red Deer-North, Red Deer-South) plus regional
> Lacombe-Clearwater and Sylvan Lake-Innisfail (solid orange lines). The
> minority renames and repartitions into four Red Deer-prefixed hybrids:
> Red Deer-Sylvan Lake, Red Deer-Innisfail, Red Deer-Blackfalds, Red
> Deer-Lacombe (dashed blue lines). Because the approximate shapes inherit
> 2019 boundaries where Tier A rules apply, the inner-city partition here
> matches the majority's; the differentiation is in naming and in how rural
> territory is attached to a Red Deer-named ED versus a regional ED.
> Approximate 2026 geometry -- shapefiles not yet released by Elections
> Alberta.

**Reader cue:** the map shows full brown coverage because both plans cover
the frame. What varies is the internal partition -- count the solid-orange
internal lines (3 cuts: N/S city + Lacombe-Clearwater + Sylvan Lake-Innisfail)
vs the dashed-navy internal lines (4 cuts: the four Red Deer-* hybrids).

**Caveats specific to this figure:**
* Red Deer-Innisfail and Red Deer-Blackfalds (minority) inherit their
  shapes from the 2019 Red Deer-North / Red Deer-South cores, because
  Tier A inheritance in the approximate gpkg doesn't yet capture the
  minority's larger hybrid claims in rural territory. This is a known
  limitation of the approximate shape stack; the caption text explains this
  explicitly so the reader doesn't misread the brown as "identical plans".

### 3. Airdrie

**File:** `maps/article/overlay_airdrie.png`
**Frame:** 44 km across (half-width 22 km) centred on Airdrie (51.2917 N,
-114.0167 W)
**Visible EDs:** 20 majority (incl. Tier C proxies), 12 minority, 0 Tier C

> **The Airdrie area.** Orange = majority-only; blue = minority-only;
> brown = both plans agree. The minority (blue) splits this commuter shed
> four ways: Airdrie East, Chestermere-Strathmore, Olds-Three
> Hills-Didsbury, Canmore-Kananaskis all reach into this frame. The
> majority (orange, partly proxied from 2019 for Tier C Airdrie-East /
> Airdrie-West / Cochrane-Springbank) keeps an Airdrie-named pair but folds
> the rural fringe into regional EDs. Approximate 2026 geometry --
> shapefiles not yet released by Elections Alberta. 2019 baseline shown as
> dashed grey. Minority shapes use v5 refinement (improved Tier C shapes
> for De Winton, Calgary-South, Windermere).

**Reader cue:** the majority draws 2 Airdrie-named EDs splitting the
commuter shed east / west. The minority draws 1 Airdrie-named ED
(Airdrie East) and folds western territory into Canmore-Kananaskis, Olds-Three
Hills-Didsbury, and Chestermere-Strathmore -- so you get 4 non-trivially
distinct dashed-navy partition shards touching Airdrie territory.

**Caveats specific to this figure:**
* Majority Airdrie-East / Airdrie-West / Cochrane-Springbank / Canmore-Banff
  are proxied from 2019 Airdrie-East / Airdrie-Cochrane / Banff-Kananaskis.
  The proxy captures the rough footprint but not the fine-grained majority
  hybrid cuts.

### 4. Lethbridge

**File:** `maps/article/overlay_lethbridge.png`
**Frame:** 60 km across (half-width 30 km) centred on Lethbridge
(49.6956 N, -112.8333 W)
**Visible EDs:** 5 majority (incl. Tier C proxies), 2 minority, 0 Tier C

> **The Lethbridge area -- the symmetric counter-test case.** Orange =
> majority-only; blue = minority-only; brown = both plans agree. The
> minority (blue) draws two Lethbridge hybrids (Lethbridge-Cardston,
> Lethbridge-Little Bow), each pulling rural territory into a Lethbridge-
> named ED; the majority (orange, proxied from 2019 for Tier C
> Lethbridge-East / Lethbridge-West / Taber-Cardston) keeps two compact
> Lethbridge city EDs and pushes rural area into Livingstone-Macleod.
> Approximate 2026 geometry -- shapefiles not yet released by Elections
> Alberta. 2019 baseline shown as dashed grey. Minority shapes use v5
> refinement (improved Tier C shapes for De Winton, Calgary-South,
> Windermere).

**Reader cue:** the two compact orange-only Lethbridge-East / Lethbridge-West
blobs (majority keeps 2019 city footprints) are surrounded by a far larger
dashed-navy perimeter -- those are the minority's two Lethbridge hybrids
absorbing the rural ring that the majority assigns to Livingstone-Macleod
and Taber-Cardston. The 2-vs-4 "asymmetric counter-test" story shows up as
the mismatch between the compact orange Lethbridge city blobs and the
wide-reaching dashed-navy perimeter.

**Caveats specific to this figure:**
* Lethbridge-East, Lethbridge-West, and Taber-Cardston (majority) are
  proxied from 2019 Lethbridge-East, Lethbridge-West, and the union of
  Taber-Warner + Cardston-Siksika respectively. These proxies capture the
  correct urban footprint but not the exact hybrid cuts the majority plan
  draws.

## Reproducibility

```
cd alberta_audit
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_build_overlay_figures.py
```

Outputs are deterministic given the input gpkgs; no random seeds involved.

## Known limitations (all figures)

1. **Approximate geometry.** None of the 2026 shapes are official. Elections
   Alberta has not released shapefiles for the commission proposals.
2. **Tier C majority proxies.** Where the majority gpkg lacks a Tier C
   polygon, we use the 2019 polygon of the most direct-lineage 2019 ED. For
   hybrids that genuinely cross old 2019 boundaries (e.g.,
   Calgary-Nose Creek, High River-Vulcan-Siksika) the proxy is a rough
   placeholder. The captions surface this.
3. **Tier C minority shapes.** Calgary-De Winton, Calgary-South, and
   Edmonton-Windermere in the minority plan are visually transcribed from
   commission thumbnails and are sub-shapefile-grade. They are flagged with
   a heavy dashed black outline whenever visible in a frame.
4. **2019 inheritance artefacts.** Where both plans inherit 2019 Tier A
   EDs identically, the overlay shows unbroken brown even when the plans
   disagree on naming -- the readable signal in those frames is the
   difference between the solid-orange and dashed-navy partition lines,
   not the fill colour.
