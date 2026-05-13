# v0_8 Alignment Proof

Programmatic verification that the refined v0_8 GPKGs match the
Alberta Electoral Boundaries Commission's published maps.

## Majority (`v0_8_full_refined_majority_2026_eds.gpkg`)

### Topology
- ED count: **89** (expected 89) — ✓
- EDs with geometry (area ≥ 0.1 km²): **89 / 89**
- Residual overlaps > 1 m²: **0** (0.000000 km² total)
- Coverage: **100.0427%** of provincial area (662864.2 / 662581.1 km²)

### City-centre landmark check

| City | ED containing centre | Match |
|------|---------------------|-------|
| Calgary | Calgary-Klein | ✓ |
| Edmonton | Edmonton-Glenora-Riverview | ✓ |
| Red Deer | Red Deer-North | ✓ |
| Lethbridge | Lethbridge-West | ✓ |
| Medicine Hat | Medicine Hat-Brooks | ✓ |
| Grande Prairie | Grande Prairie-Wapiti | ✓ |
| Fort McMurray | Fort McMurray-Wood Buffalo | ✓ |
| Airdrie | Airdrie-East | ✓ |
| St. Albert | West Yellowhead | ✗ |
| Spruce Grove | Spruce Grove | ✓ |

**1 landmark check(s) failed** — likely misalignment or ED-naming mismatch.

## Minority (`v0_8_full_refined_minority_2026_eds.gpkg`)

### Topology
- ED count: **89** (expected 89) — ✓
- EDs with geometry (area ≥ 0.1 km²): **89 / 89**
- Residual overlaps > 1 m²: **0** (0.000000 km² total)
- Coverage: **100.0004%** of provincial area (662583.5 / 662581.1 km²)

### City-centre landmark check

| City | ED containing centre | Match |
|------|---------------------|-------|
| Calgary | Peace River | ✗ |
| Edmonton | Edmonton-Beverly-Clareview | ✓ |
| Red Deer | Peace River | ✗ |
| Lethbridge | Peace River | ✗ |
| Medicine Hat | Peace River | ✗ |
| Grande Prairie | Grande Prairie-Wapiti | ✓ |
| Fort McMurray | Peace River | ✗ |
| Airdrie | Airdrie East | ✓ |
| St. Albert | Peace River | ✗ |
| Spruce Grove | Edmonton-Spruce Grove | ✓ |

**6 landmark check(s) failed** — likely misalignment or ED-naming mismatch.

## Cross-plan consistency
- Majority area: 662864.21 km²
- Minority area: 662583.47 km²
- Absolute diff: 280.7376 km² (0.0424%)
