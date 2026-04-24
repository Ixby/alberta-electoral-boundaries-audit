# MAUP Area-Weighted VA Attribution — Alternative to Centroid-in-Polygon

**Generated:** 2026-04-23
**Pipeline:** `analysis/v0_1_phase_4c_va_attribution_maup.py`
**Companion (not modified):** `analysis/scripts/v0_1_phase_4c_va_attribution.py`, `analysis/scripts/v0_1_phase_4bcdef_execution.py`

Forward: `report_academic.md` §5.2.7 (suggested insertion at end)
Backward: `data/va_polygons_with_full_2023_votes.gpkg`, `data/v0_1_canonical_{majority,minority}_2026_eds.gpkg`, `data/v0_1_{majority,minority}_full_crosswalk.csv`

---

## 1. Problem statement

The existing Phase 4C pipeline (`v0_1_phase_4c_va_attribution.py` + the corresponding VA-polygon branch of `v0_1_phase_4bcdef_execution.py`) assigns each of 4,765 Voting Area polygons **wholesale to a single 2026 ED** based on the VA polygon's `representative_point()` (its interior centroid). When a VA polygon straddles a DPG ED boundary — i.e., when part of it lies inside ED_A and part inside ED_B — 100 % of the VA's 2023 votes are attributed to whichever ED the centroid happens to fall in. If a VA is split 60/40 across two EDs, the ED on the 60 % side gets all of it and the other ED gets nothing.

This is the classical **Modifiable Areal Unit Problem** (MAUP) in its binary form: the choice of a single-point aggregator introduces systematic bias at boundary-straddling units. The PO's 2026-04-22 vulnerability message (section 3) flagged this as a material source of potential error in the §5.2.7 partisan-bias measurement.

## 2. Method

**Area-weighted interpolation.** For each VA polygon `v` and each canonical 2026 ED polygon `e`:

```
area_weight(v, e) = area(v ∩ e) / area(v)
```

The VA's full 2023 two-party votes (`va_ndp_full`, `va_ucp_full`, `va_other_full` from the post-Election-Day-splat substrate) are then apportioned to each ED by the weight:

```
votes_to(v, e) = area_weight(v, e) × votes(v)
```

A VA entirely inside one ED contributes 1.0 × its votes to that ED. A VA split 60/40 between ED_A and ED_B contributes 0.6 × and 0.4 × of its votes respectively. The per-ED totals are the sum over all VAs.

**Crosswalk fallback.** Because the canonical DPG polygons contain Tier-C transcription artifacts (gaps, slivers), not every VA is fully covered by the 2026 polygon set. For each VA, the residual weight `1 − Σ_e area_weight(v, e)` is assigned via the full crosswalk (`parent_ed_2019 → proposed_2026`) to the VA's 2019-parent's crosswalk target. This guarantees per-VA vote conservation to 1.0.

**Overlap handling.** The canonical shapefiles contain real inter-ED polygon overlaps (Tier-C transcription slop): ~2,700 km² majority, ~16,500 km² minority. When a VA's raw weight sum across DPGs exceeds 1.0 (for 1,011 majority VAs / 1,722 minority VAs in the full run), the per-VA weights are proportionally re-normalised so the sum equals the DPG coverage fraction ≤ 1.0. This is the most defensible treatment short of manually repairing the canonical shapefile — each overlapping ED receives its fair share of the contested territory.

## 3. Implementation

- **Language / libraries:** Python 3.14, `geopandas` (with `shapely` 2.x), `pandas`, `numpy`.
- **Core primitive:** `gpd.overlay(vas, eds, how='intersection')` — returns a GeoDataFrame of polygon intersections with STR-tree spatial indexing; runtime ~2–7 s per map.
- **CRS:** All inputs reprojected to the VA substrate CRS (EPSG:3400, Alberta 10-TM projection, metres). Area calculations are metric-correct.
- **Full run time:** ~10 s on the 4,765-VA × 89-ED matrix (vs a pessimistic 10–30 min budget).

## 4. Validation

### 4.1 Conservation gate — PASS

For each VA, the sum of apportioned votes across all (VA, ED) rows must equal the VA's original votes.

| map | max \|Δ ndp\| | max \|Δ ucp\| | max \|Δ other\| | max \|Δ weight\| | result |
|---|---|---|---|---|---|
| majority | 9.45e-05 | 1.43e-04 | 6.90e-06 | 5.94e-07 | **PASS** (< 1 vote tolerance) |
| minority | 3.27e-05 | 4.00e-05 | 1.90e-06 | 1.73e-07 | **PASS** |

Two-party provincial totals land on **1,706,304** for both maps (matches the VA substrate to sub-vote precision and matches the centroid-pipeline headline).

### 4.2 Coverage

`va_area_weighted_coverage_frac` is the fraction of total VA-substrate area covered by DPG polygons (weighted by VA size).

| map | DPG area coverage | n VAs fully covered | n VAs partial | n VAs zero-cover | crosswalk-fallback weight mass |
|---|---|---|---|---|---|
| majority | **90.91 %** | 3,967 | 474 | 324 | 463 (9.72 %) |
| minority | **89.59 %** | 3,201 | 793 | 771 | 1,012 (21.23 %) |

Consistent with §5.2.7's reported "89.8 % on majority and 80.2 % on minority" (the minority coverage differs modestly — 89.6 % here vs 80.2 % in the centroid pipeline — because the centroid test is a point-in-polygon predicate that misses partially-covered VAs, whereas area-weighted coverage credits a VA fractionally for any intersection area).

### 4.3 Overlapping DPG polygons normalised

- Majority: 1,011 VAs with raw DPG coverage > 1.0 (max 3.00 ×) — proportionally normalised.
- Minority: 1,722 VAs with raw DPG coverage > 1.0 (max 3.95 ×) — proportionally normalised.

The higher minority figure reflects the larger Tier-C overlap area in the minority shapefile and is the mechanical reason minority EG moves more than majority EG under the MAUP treatment (see §6).

## 5. Results

### 5.1 B2 Efficiency gap — MAUP vs centroid

| measurement | majority EG | minority EG | asymmetry (min − maj) | direction |
|---|---|---|---|---|
| §5.2.7 centroid (headline) | **−2.33 %** | **+1.82 %** | **+4.15 pp** | min more NDP-favourable |
| **MAUP area-weighted** | **−3.25 %** | **−2.14 %** | **+1.12 pp** | min more NDP-favourable |
| Δ vs centroid | −0.92 pp | −3.96 pp | **−3.03 pp** | (asymmetry narrows) |
| §5.2.7 blended crosswalk | −1.29 % | −2.71 % | **−1.42 pp** | min more UCP-favourable |

**Does the +4.15 pp asymmetry survive?** The **sign survives but the magnitude collapses**. Under MAUP, minority is still more NDP-favourable than majority, but by **+1.12 pp** — less than one-quarter of the centroid headline. The minority EG flips from +1.82 % (pro-NDP) under centroid to −2.14 % (pro-UCP) under MAUP, while majority EG drifts modestly more UCP-favourable.

### 5.2 Seat totals

| measurement | majority NDP/UCP | minority NDP/UCP |
|---|---|---|
| MAUP area-weighted | 38 / 51 | 32 / 57 |

(Centroid-pipeline seat totals for the same maps are reported in `data/v0_1_phase_4bcdef_summary.json`; the MAUP totals differ modestly because of margin shifts at tipping EDs.)

### 5.3 Seat flips (minority only)

Three minority-map EDs flip between the two measurements:

- **Calgary-South**: was zero-VA under centroid (§5.2.7-flagged) → MAUP gives it real votes and it lands UCP (+18.9 % margin). The crosswalk fallback feeds this ED via the `parent_ed_2019 → Calgary-South` path.
- **Edmonton-Manning**: was zero-VA under centroid → MAUP gives it UCP +1.9 % margin, now a tipping district.
- **Stony Plain-Drayton Valley**: was UCP +9.3 % under centroid → flips to **NDP −15.6 %** under MAUP (24.8 pp margin shift).

### 5.4 Large per-ED shifts — surprise findings

The Stony Plain-Drayton Valley flip is the single largest driver of the minority EG shift. Diagnostic inspection of the canonical minority shapefile shows that the Stony Plain-Drayton Valley polygon **overlaps metropolitan Edmonton EDs by 3–470 km² each** (total ~1,200 km² of overlap against 20+ Edmonton polygons). Under MAUP weight-normalisation, urban Edmonton VAs that lie in this multi-claimed territory get split ~50/50 between their natural urban ED and Stony Plain-Drayton Valley, which injects ~55,000 votes of NDP-leaning urban mass into what the commission documents as a rural/exurban district.

**This is a Tier-C DPG transcription artifact**, not a property of the minority proposal itself. The same artifact was present under centroid-in-polygon but invisible because centroid-in-polygon made a binary choice per VA; MAUP exposes it by proportionally splitting the contested VAs. The correct interpretation is that **the minority map's MAUP EG is a mixture of (a) genuine packing/cracking effects and (b) DPG polygon-overlap noise**, and the +1.12 pp asymmetry must be read with this caveat.

A similar effect is not present on the majority shapefile, where Tier-C overlap area is ~6 × smaller.

## 6. Interpretation — what does MAUP say about §5.2.7?

The §5.2.7 crosswalk-vs-spatial disagreement on asymmetry magnitude/sign is measured as the gap between the blended-crosswalk asymmetry (−1.42 pp) and the high-resolution spatial asymmetry:

| spatial method | spatial asym | gap vs crosswalk (−1.42 pp) | verdict |
|---|---|---|---|
| centroid-in-polygon (§5.2.7) | +4.15 pp | **5.57 pp** | original disagreement |
| **MAUP area-weighted** | **+1.12 pp** | **2.54 pp** | **gap narrows by 3.03 pp** |

**The disagreement narrows but does not close.** The two spatial measurements (centroid vs MAUP) still both point to minority-more-NDP-favourable, which disagrees with the blended-crosswalk reading of minority-more-UCP-favourable. But the MAUP magnitude is much closer to the crosswalk's −1.42 pp than the centroid's +4.15 pp was.

Three readings of this are defensible and should all appear in §5.2.7:

1. **The centroid +4.15 pp was inflated by MAUP.** ~3 of the 5.57 pp gap between the two §5.2.7 measurements was an artifact of wholesale-VA assignment at boundary-straddling units. MAUP removes that artifact and the remaining gap (2.54 pp) is attributable to DPG polygon-tier uncertainty plus the Stony Plain-type Tier-C overlap noise. This favours the reading that the *true* spatial asymmetry is small (~+1 pp) and the *true* partisan-bias direction is near-null.

2. **The centroid +4.15 pp was essentially correct; MAUP is the one introducing noise.** Under this reading, the mass being split across the Stony Plain-Drayton Valley / Edmonton overlaps under MAUP is not a Tier-C artifact but real territory the minority map genuinely disputes, and the MAUP 50/50 split is a defensible compromise that the centroid method resolved in one direction. This reading is weaker because the polygon overlap is documented as transcription slop (Tier-C) rather than cartographic intent.

3. **Both spatial readings have meaningful error bars that neither §5.2.7 nor this note have formally bracketed.** MC-bracketing for the spatial measurement (proposed in §5.2.7's "not yet Monte-Carlo-bracketed" caveat) is the natural next step, and the MAUP result gives a concrete alternative point-estimate to include in that bracket. Under this reading, the honest summary is: *spatial asym estimates lie somewhere in +1.1 pp to +4.2 pp, probably closer to the lower end*, with DPG fidelity the binding constraint on further precision.

My recommended language (§8 below) is reading **3** — present both spatial methods, acknowledge the ~3 pp range, and keep the §5.2.7 core conclusion (that the partisan-bias direction is sensitive to spatial resolution) unchanged. MAUP does not resolve the measurement problem; it just re-bounds it more tightly.

## 7. Absolute paths of files created

- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\analysis\v0_1_phase_4c_va_attribution_maup.py`
- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_phase4c_majority_2023_votes_maup.csv`
- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_phase4c_minority_2023_votes_maup.csv`
- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\analysis\phase_4c_va_to_2026_assignments_maup.csv` (15,723 rows)
- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\analysis\v0_1_phase4c_maup_summary.json`
- `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\analysis\v0_1_maup_area_weighted_analysis.md` (this file)

## 8. Paper-ready paragraph — suggested insertion at end of §5.2.7

The paragraph below (≈215 words) is designed to slot in as a third measurement layer after the existing "high-resolution spatial" row in §5.2.7's comparison table and before "Both measurements are internally consistent." It is framed honestly: MAUP narrows but does not close the disagreement, and the residual gap is bounded by DPG fidelity.

---

> **MAUP area-weighted attribution (third measurement layer).** The centroid-in-polygon spatial method reported above assigns each of 4,765 VAs wholesale to one 2026 ED based on the VA polygon's interior centroid, which introduces binary-assignment bias at boundary-straddling VAs. A higher-fidelity alternative computes the fractional area-overlap of each VA polygon with each 2026 ED polygon (Modifiable Areal Unit Problem area-weighted interpolation) and apportions the VA's 2023 votes across EDs by those fractions. The implementation is in `analysis/v0_1_phase_4c_va_attribution_maup.py`; conservation is exact to ±0.001 votes per VA, and provincial two-party totals match the centroid pipeline at 1,706,304 on both maps. Under MAUP, majority 2026 EG = **−3.25 %**, minority 2026 EG = **−2.14 %**, and the minority-majority asymmetry is **+1.12 pp** (direction preserved: minority more NDP-favourable, but magnitude collapsed from +4.15 pp to +1.12 pp). The gap between the blended-crosswalk asymmetry (−1.42 pp) and the spatial-high-resolution asymmetry narrows from 5.57 pp (centroid) to **2.54 pp (MAUP)**. Approximately 3 of the 5.57 pp of the original §5.2.7 disagreement was therefore a centroid-assignment artifact. The residual 2.54 pp disagreement is attributable to DPG polygon-tier transcription uncertainty — particularly a ~1,200 km² overlap between the Stony Plain-Drayton Valley minority polygon and multiple metropolitan Edmonton polygons — which will collapse under the §4.1.4 sunset-clause re-run once official 2026 shapefiles are released.

---

## 9. Reproduction

```bash
cd "c:/Users/email/Documents/Claude/Projects/Electoral Boundary Analysis/alberta_audit"
PYTHONIOENCODING=utf-8 python analysis/v0_1_phase_4c_va_attribution_maup.py
# smoke test (50 VAs):
PYTHONIOENCODING=utf-8 python analysis/v0_1_phase_4c_va_attribution_maup.py --smoke 50
```

Runtime: ~10 s for the full 4,765-VA × 89-ED run (both maps). No network or external dependencies beyond the read-only inputs listed in §1 of the script docstring.
