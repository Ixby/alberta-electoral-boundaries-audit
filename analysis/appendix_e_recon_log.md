# Appendix E Reconnaissance Log

Purpose: document what Appendix E of the 2025-2026 EBC Final Report contains, and what was (and was not) extractable.

## Contents of Appendix E (pages 285-362 of 362-page report)

| Section | Pages | Content |
|---------|-------|---------|
| Title page | 285 | "APPENDIX E: Minority Report and Maps" |
| Executive Summary | 287-288 | Narrative recommendations: 89 EDs (up from 87), 2 new seats to Edmonton and Calgary, 11 Calgary hybrid EDs, 4 each RD/Lethbridge hybrids, 6→5 Edmonton urban consolidation, 3 special rural districts (Central Peace-Notley, Lesser Slave Lake, Rocky Mountain House-Banff Park) |
| Introduction / legal basis | 289-294 | Commission composition, Act, redistribution rules |
| Process / principles | 295-306 | Narrative on effective representation, hybrid rationale, population variance rules |
| Macro-level decisions | 307-310 | Narrative — 11 Calgary hybrids, 4 Red Deer, 4 Lethbridge, Edmonton consolidation, Spruce Grove split |
| Individual ED recommendations | 311-355 | Narrative for each proposed ED: boundary description, rationale, map reference |
| Population table | 357-360 | **Table of 89 proposed EDs with populations** (the only machine-extractable table) |
| Closing / maps | 361-362 | Maps (not machine-extractable) |

## What was extracted

### `data/v0_1_minority_2026_populations_appendixE.csv`

89 rows, columns: `num, proposed_2026, population`.

Examples:
```
1, Calgary-Acadia, 53346
2, Calgary-Airdrie, 58820
...
89, Wetaskawin-Ponoka-Maskwacis, 48775
```

**Cross-check vs pre-existing `data/v0_1_minority_2026_populations.csv`** (unknown provenance, but already in the repo): populations agree for the first 7 rows spot-checked. Names match. This re-extraction corroborates the earlier file.

### `data/v0_1_minority_hybrid_crosswalk.csv`

**Schema mirrors `data/v0_1_majority_hybrid_crosswalk.csv`** (`current_2019, proposed_2026`) plus added columns:
- `is_hybrid` — heuristic ("yes" if the proposed name combines a major-city token with a rural-marker token, or has 3+ hyphen-separated components)
- `minority_pop_2026` — from Appendix E table
- `match_type` — `exact` / `jaccard=X.XX` / `new` / `unmapped`

Counts:
- 73 rows with `match_type = exact` or `jaccard ≥ 0.4` (confident current→proposed mapping)
- 16 rows with `match_type = new` — minority-proposed EDs with no clear 2019 counterpart (likely new hybrids: Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere, Calgary-Okotoks-De Winton, etc.)
- 14 rows with `match_type = unmapped` — 2019 EDs with no clear minority counterpart (likely merged into hybrid names)

### Caveats — DO NOT use uncritically

1. **The heuristic hybrid flag is not authoritative.** It was derived from name morphology, not from the commission's own classification. The minority's own prose (page 307) explicitly names 11 Calgary hybrids, 4 Red Deer, 4 Lethbridge, + some Edmonton capital-region hybrids (Spruce Grove etc.). To use the hybrid flag in statistical claims, a manual review against the pp. 311-355 narrative is required.

2. **The `current_2019 → proposed_2026` mapping is many-to-many in practice.** The minority's recommendations redraw most EDs; a single 2019 ED may have its population redistributed across 3+ proposed 2026 EDs. The crosswalk CSV picks a single best-token-match, which is useful for name-change tracking but **not for population flow analysis**. For Phase 4B dissolves, use the shapefile + DA-level spatial join instead of the name crosswalk.

3. **Unmapped rows**: 14 current EDs + 16 new proposed EDs suggest ~15% structural turnover, which is consistent with the minority's net +2 seat proposal plus hybrid creation. Do not interpret "unmapped" as "ED eliminated"; the area is always assigned somewhere.

## What was NOT in Appendix E

- **No tabular current→proposed crosswalk** — the majority's Appendix C does contain one (which is `data/v0_1_majority_hybrid_crosswalk.csv`, 19 rows covering only the hybrid/renamed EDs). The minority's text does not have an analogous table.
- **No population-by-DA or population-by-VA breakdown** — the minority gives only ED-level totals, same as the majority.
- **No machine-readable polygon data** — maps in the PDF are raster images. Producing a shapefile of the minority's proposed boundaries would require digitizing from those images, which is out of scope for this session.

## Recommendations for next analyst

1. If the audit requires an authoritative minority hybrid list, **manually enumerate** from the minority narrative (pp. 287-288 executive summary + pp. 307-310 macro-level) and overwrite the `is_hybrid` column in the crosswalk.
2. If Phase 4B requires dissolving 2019 VAs into proposed 2026 minority EDs, **the minority's boundaries exist only as raster maps in the PDF**. Options: (a) request the shapefile from the commission if it exists, (b) digitize from maps, (c) proxy with the majority's Appendix D boundaries where they overlap with minority recommendations. Without (a), quantitative analysis of the minority's boundaries is fundamentally limited to name-level claims.
3. For cross-validation of the 89-ED population total: sum in `data/v0_1_minority_2026_populations_appendixE.csv` should equal provincial population. Quick sanity check possible against `v0_1_alberta_2019_populations.csv` aggregate × growth factor.
