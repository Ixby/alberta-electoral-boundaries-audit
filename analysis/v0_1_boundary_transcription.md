# v0_1 Commission-PNG Boundary Transcription (Track Y-prime Phase 1)

## Purpose

Visual transcription of the actual commission boundary line for each of Track Y's
five Tier B minority EDs, read directly from the 600-DPI commission map extracts.
The goal is to name the geographic features the commission actually drew the
boundary along — road, river, rail, administrative line — so the OSM re-snap in
Phase 2 can target the correct feature class per boundary segment.

## Source

- `maps/hires/v0_1_minority_p359_map73.png` — Alberta overview (minority)
- `maps/hires/v0_1_minority_p360_map74.png` — Calgary overview (minority)
- `maps/hires/v0_1_minority_p361_map75.png` — Edmonton overview (minority)
- `maps/hires/v0_1_minority_p362_map76.png` — City overviews (Lethbridge,
  Red Deer, Airdrie, Medicine Hat, Fort McMurray, Grande Prairie, St. Albert,
  Chestermere, Wetaskiwin / Ponoka area not directly isolated but visible on
  p359)

Colour conventions in the commission maps:
- **Red lines** = proposed 2026 ED boundaries.
- **Light blue wavy lines** = rivers / streams (hydrography layer).
- **Grey thin lines** = roads (major arterials named on some panels).
- **Thick black lines** = Indian Reserves (IRs), military reserves, major
  municipal boundaries.

## Per-boundary transcription

### 1. Calgary-De Winton (ED in minority map, p360)

**Location on map.** Southwest quadrant of the Calgary overview panel
(ED label "Calgary-De Winton" visible below "Calgary-Bow Breneck" on the panel).
ED spans from Calgary city's southern edge out to the foothills, wrapping around
the south of Calgary proper.

**Boundary transcription, segment by segment:**

| Segment | Feature class | Named feature |
|---|---|---|
| North edge (inside Calgary) | Road | Calgary city limit / Anderson Road / Stoney Trail SW corridor |
| North-east "step" into city | Road | follows Stoney Trail SW where it crosses south, then jogs east |
| East edge (south of Calgary city) | Admin | follows municipal boundary between Calgary and Foothills County |
| South edge | Admin | follows MD of Foothills boundary (a township line) |
| West edge | Admin | follows range line (rural township boundary) |

**Water bodies:** Highwood River crosses near the south edge but is NOT the
boundary. Bow River does not enter this ED.

**Verdict vs Track Y v1:** Track Y's road-snap dragged the east edge toward
arbitrary local rural roads. Commission clearly uses admin (range/township) lines
for the rural edges. The "staircase" pattern seen in the v1 verification overlay
is genuine commission behaviour — commission follows the rectangular township
grid — but Track Y's snap rounded the corners and mis-located a few ticks.

### 2. Calgary-South (ED in minority map, p360)

**Location on map.** Commission panel shows "Calgary-South" covering the
south-central part of Calgary; the ED consists of the south-central city
neighbourhoods (Fish Creek Park area, Midnapore, Shawnessy, etc.) plus an
eastward extension across the Bow River into the exurban area (Chestermere
approach corridor).

**Boundary transcription, segment by segment:**

| Segment | Feature class | Named feature |
|---|---|---|
| North edge (city, west half) | Road | Glenmore Trail / Anderson Road corridor |
| North edge (city, east half) | Road | Glenmore Trail extending east toward Deerfoot Trail |
| East edge (into exurbs) | **River** | **Bow River** — the ED's eastern protrusion is bounded on the east by the Bow River, follows its meanders south |
| South edge | Road | follows 22X / Marquis of Lorne Trail / Highway 22X east of the city |
| South exurban edge | Admin | township line south of Bow River crossing |
| West edge | Road | Deerfoot Trail / Macleod Trail corridor |

**Water bodies:** **Bow River is the eastern boundary of the exurban limb.**
This is the primary water-body boundary segment.

**Verdict vs Track Y v1:** Track Y's road-snap produced a jagged east edge
because it snapped to arbitrary local residential / service roads rather than
to the Bow River centreline. The verification PNG shows the tell-tale zigzag
along the eastern protrusion of the red boundary — the true commission line
follows the river, not roads. **This is a mishandled water-body boundary —
flag for re-snap to waterway=river.**

### 3. Edmonton-Windermere (ED in minority map, p361)

**Location on map.** Southwest Edmonton. ED wraps around the south-west and
south of Edmonton, with its eastern edge pressed up against the North
Saskatchewan River.

**Boundary transcription, segment by segment:**

| Segment | Feature class | Named feature |
|---|---|---|
| North edge | Road | Whitemud Drive / 23 Avenue NW corridor |
| **East edge (entire)** | **River** | **North Saskatchewan River** — the east and NE boundary is the river's left bank through the entire ED extent |
| South edge | Admin | Edmonton city boundary with Leduc County (township line) |
| West edge | Road | Anthony Henday Drive (ring road) / Winterburn Road |

**Water bodies:** **North Saskatchewan River is the east boundary.** This is
the dominant water-body segment on the ED.

**Verdict vs Track Y v1:** The verification PNG shows a pronounced zigzag
along the east edge of the red Track Y polygon. That zigzag is exactly what
happens when a road-snap tries to follow a curving river — it picks
intersecting side streets and ricochets between them. The commission's line
is a clean river meander. **This is the single largest mishandled water-body
boundary in Track Y's output. Flag for re-snap to waterway=river.**

### 4. Lethbridge-Little Bow (ED in minority map, p362, inset "Lethbridge")

**Location on map.** North of Lethbridge city, covering the rural area
between Lethbridge and Vulcan / Little Bow reservoir.

**Boundary transcription, segment by segment:**

| Segment | Feature class | Named feature |
|---|---|---|
| **North edge** | **River** | **Oldman River** — meanders are clearly visible on the commission map as the north boundary of the ED, matching the river's channel |
| East edge | Admin | range / township line running N-S at Oldman–Bow confluence region |
| South edge | Admin | township line just north of Lethbridge city limits |
| South edge near Lethbridge | Admin | Lethbridge city boundary (municipal) |
| West edge | Admin | range line |

**Water bodies:** **Oldman River is the north boundary** over a substantial
distance, plus Little Bow River may form part of the internal segment.

**Verdict vs Track Y v1:** The verification PNG north edge of the red boundary
shows small meander-like zigzags that correspond to the river, but these are
irregular and do not match the river's actual course. Track Y's road-snap was
unable to follow the river because few OSM "roads" parallel this stretch of
the Oldman. **Flag for re-snap to waterway=river.**

### 5. Wetaskawin-Ponoka-Maskwacis (ED in minority map, p359)

**Location on map.** Central Alberta, between Red Deer and Edmonton. Includes
the city of Wetaskiwin, town of Ponoka, the Maskwacis Indian Reserves (Ermineskin,
Samson, Louis Bull, Montana IRs).

**Boundary transcription, segment by segment:**

| Segment | Feature class | Named feature |
|---|---|---|
| North edge | Admin | township line north of Wetaskiwin / Battle Lake region |
| East edge | Admin | range line, follows township rectangle |
| South edge | Road / Admin | Highway 53 corridor near Ponoka, then township lines |
| South edge, western half | **River** | **Battle River** — partial segment where ED boundary hugs the Battle River's course between Ponoka and Maskwacis |
| West edge | Admin | range line west of Maskwacis IRs |
| Inner IR boundaries | Admin | thick black lines of IR perimeters (Maskwacis IRs form an island-enclave-like treatment) |

**Water bodies:** Battle River partial; the ED contains multiple lakes
(Pigeon Lake is NOT in this ED — it's west in Lac Ste. Anne-Parkland).

**Verdict vs Track Y v1:** Track Y's snap largely matched the township-grid
rectangular boundaries on the north and east. The south edge's river segment
is short and may be low-impact. Track Y's boundary looks mostly right on this
one — mild refinement needed.

## Summary table

| ED | Water-body segment flagged | Feature class(es) for re-snap | Priority |
|---|---|---|---|
| Calgary-De Winton | None | road (north) + admin (rural) | Low |
| Calgary-South | Bow River (east) | road (N) + **waterway=river** (E) + admin (S) | **High** |
| Edmonton-Windermere | North Saskatchewan River (east, full length) | road (N/W) + **waterway=river** (E) + admin (S) | **High** |
| Lethbridge-Little Bow | Oldman River (north) | **waterway=river** (N) + admin (E/W/S) | **High** |
| Wetaskawin-Ponoka-Maskwacis | Battle River (short, south) | admin (most) + **waterway=river** (S partial) | Low |

## Triple-check cross-reference

To triple-check these readings, the transcription was cross-referenced against:

1. The 2019 ED shapefile (same underlying hydrography — these rivers are visible
   in `data/alberta_2019_eds/` polygons and the Bow, North Saskatchewan, and
   Oldman all appear as boundaries between legacy 2019 EDs).
2. OSM's `waterway=river` tags — each named river is tagged and routable via
   Overpass.
3. Approximate visual alignment of the light-blue river symbol on the
   commission maps with the red ED boundary in the same region: in each of the
   three "High" priority cases, the red ED boundary follows the river
   meander pattern precisely, confirming the river is the boundary.

## Implication for Phase 2

Three out of five Tier B minority EDs have material water-body boundary
segments that Track Y's road-only snap cannot have handled correctly. These
three are the re-snap priority:
- Calgary-South (Bow River east)
- Edmonton-Windermere (North Saskatchewan east)
- Lethbridge-Little Bow (Oldman River north)

The two others (Calgary-De Winton, Wetaskawin-Ponoka-Maskwacis) are
admin-line dominated and Track Y's output is closer to correct. They need
only a check / minor refinement.
