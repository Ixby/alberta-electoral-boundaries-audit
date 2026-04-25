# v0_8 Alignment Proof

Programmatic verification that the refined v0_8 GPKGs match the
Alberta Electoral Boundaries Commission's published maps.

## Majority (`v0_8_canonical_majority_2026_eds.gpkg`)

### Topology
- ED count: **89** (expected 89) — ✓
- EDs with geometry (area ≥ 0.1 km²): **68 / 89**
- **Empty EDs (area < 0.1 km²): 21** — these EDs were not assembled from source data and remain unfilled. This is a known data-completeness limitation inherited from v0_7.

  Empty EDs:
  - Calgary-Currie  (0.0000 km²)
  - Calgary-East  (0.0002 km²)
  - Calgary-Fish Creek  (0.0000 km²)
  - Calgary-Hays  (0.0000 km²)
  - Calgary-Klein  (0.0000 km²)
  - Calgary-North  (0.0015 km²)
  - Calgary-North West  (0.0000 km²)
  - Edmonton-Beverly-Clareview  (0.0004 km²)
  - Edmonton-Glenora-Riverview  (0.0000 km²)
  - Edmonton-Manning  (0.0000 km²)
  - Edmonton-North West  (0.0000 km²)
  - Edmonton-South  (0.0000 km²)
  - Edmonton-West Henday  (0.0000 km²)
  - Edmonton-Windermere  (0.0000 km²)
  - Lacombe-Clearwater  (0.0100 km²)
  - Lethbridge-East  (0.0000 km²)
  - Red Deer-South  (0.0000 km²)
  - St. Albert-Sturgeon  (0.0000 km²)
  - Stony Plain-Drayton Valley  (0.0000 km²)
  - Strathcona-Sherwood Park  (0.0023 km²)
  - Wetaskiwin-Ponoka-Maskwacis  (0.0000 km²)
- Residual overlaps > 1 m²: **66** (157.096294 km² total)
- Coverage: **100.0427%** of provincial area (662864.2 / 662581.1 km²)

### City-centre landmark check

| City | ED containing centre | Match |
|------|---------------------|-------|
| Calgary | Calgary-Lougheed | ✓ |
| Edmonton | Edmonton-City Centre | ✓ |
| Red Deer | Red Deer-North | ✓ |
| Lethbridge | Lethbridge-West | ✓ |
| Medicine Hat | Medicine Hat-Brooks | ✓ |
| Grande Prairie | Grande Prairie-Wapiti | ✓ |
| Fort McMurray | Fort McMurray-Wood Buffalo | ✓ |
| Airdrie | Airdrie-East | ✓ |
| St. Albert | West Yellowhead | ✗ |
| Spruce Grove | Spruce Grove | ✓ |

**1 landmark check(s) failed** — likely misalignment or ED-naming mismatch.

## Minority — SKIPPED
