# Issue #14 Feasibility Check — Manual QGIS Inspection

## Quick Start

1. Open `data/issue14_feasibility_qgis.gpkg` in QGIS
2. Inspect the 3 worst-anchoring minority EDs
3. Answer the questions below (10-15 minutes)

## The 3 Worst EDs and Current Anchoring

| ED | Anchoring % | Perimeter (km) | Anchored (km) |
|---|---|---|---|
| Peace River | 7.4% | 1693.3 | 125.3 |
| Cold Lake-Bonnyville-St. Paul | 12.73% | 687.0 | 87.5 |
| Canmore-Kananaskis | 16.01% | 1211.4 | 193.9 |

**Goal:** Can we redraw these EDs to reach ≥60% anchoring while preserving Tier A COIs?

## Layer Guide in QGIS

- **ED_worst** (light blue polygons): The 3 worst EDs outlined
- **VA_in_worst** (small yellow polygons): Individual voting areas inside those EDs
- **CSD_reference** (thin gray boundaries): StatsCan Census Subdivisions (the anchoring target)
- **COI_reference** (red circles): Tier A COI constraint locations:
  - Airdrie-Calgary: Airdrie city centre (must preserve ED adjacency to Calgary EDs)
  - Tsuut'ina-Calgary: Tsuut'ina Nation centre (must stay in same ED or adjacent ED group)
  - Red Deer hub: Red Deer city centre (must not split across >3 EDs)

## Inspection Checklist

For **Peace River** (current 7.4%):
- [ ] Are there large runs of ED boundary that avoid CSD edges but could easily follow them?
- [ ] Which VAs on the ED perimeter are causing the low anchoring?
- [ ] If you merged those boundary-adjacent VAs into adjacent EDs, would the COI constraints break?

For **Cold Lake-Bonnyville-St. Paul** (current 12.73%):
- [ ] Same analysis as above

For **Canmore-Kananaskis** (current 16.01%):
- [ ] Same analysis as above

## Success Criteria

**Feasible**: You identify a plausible VA reassignment that could push anchoring from current level to ≥50% (even if not ≥60%) while keeping COI reference points in viable positions.

**Infeasible**: The ED perimeter is locked by COI constraints and cannot be redrawn to follow CSDs without breaking multiple Tier A claims.

## What To Do Next

- If **Feasible**: Proceed to Phase 3b (--demo mode) and Phase 4 (full 100k run with CSD-weight search)
- If **Infeasible**: Issue #14 is geometrically impossible; document and move to next priority

---

*Inspection takes 10-15 minutes. If you have GIS experience, you can spot the feasibility boundary visually without running a full model.*
