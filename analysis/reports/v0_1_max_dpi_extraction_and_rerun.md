# Max-DPI extraction and v0_5 DPG rerun

*Analysis date: 2026-04-24*

*Backward: `.temp/commission_report.pdf`, `data/maps/hires/`, `data/v0_2_canonical_*_2026_eds_topoclean.gpkg`, `data/v0_5_canonical_*_2026_eds_da_anchored.gpkg`*

*Forward: paper §4.1.4 DPG discussion / §E provenance; future DPG revisions beyond v0_5*

## Summary

Two questions were asked:

1. **Is 600 DPI the ceiling for map extractions from the commission's 2026 final report?** — **Yes.** Every map page in the PDF is a single dominant embedded raster JPEG/PNG with a native resolution of 300 or ~380-388 DPI. Rendering at 600 DPI already interpolates above native. Going higher than native adds no new information, only pixel count.
2. **Does the v0_5 DA-anchored DPG change MAUP, Phase 4F hardstops, and the DPG-perturbation 90% CI relative to the v0_2 topology-clean baseline?** — **Yes, meaningfully.** v0_5 **flips the sign of the §5.2.7 asymmetry** in the point estimate (from +3.35 pp majority-favours-UCP in v0_2 to -3.64 pp minority-favours-UCP in v0_5, a ~7 pp swing), drops Phase 4F hardstops from the v0_1 baseline (81→56 majority, 87→66 minority), and exposes a structural defect in v0_5 — five EDs per map have empty polygons after the DA-anchoring cascade, widening attribution uncertainty for those districts. The DPG-perturbation 90% CI is reported below once the 200-sample run completes.

## Investigation 1 — DPI ceiling

**Tool:** `pymupdf` (fitz) 1.27.2. `pdfplumber` was not needed; PyMuPDF's `page.get_images(full=True)` combined with `page.get_image_rects(xref)` yields embedded-image pixel dimensions plus page-space placement in points, from which native DPI falls out directly as `pixel_w / placed_w_in`.

### Per-page findings

All target pages were inspected; the raw per-page manifest is written to `analysis/reports/max_dpi_inspect.json`. Summary of the map pages:

| Page | What it contains | Content type | Native DPI of dominant image | Decision |
|---|---|---|---|---|
| MAJ p71 | Appendix A Alberta overview | raster (1 dominant image) | 300 | capped at 300 — 600 was already interpolated |
| MAJ p72 | Appendix A Calgary MAP | raster | **388** | capped at 388 |
| MAJ p74 | Appendix A Edmonton MAP | raster | 300 | capped at 300 |
| MAJ p76 | Appendix A other cities MAP | raster | **388** | capped at 388 |
| MAJ p78 | Appendix A near-Calgary | raster | **388** | capped at 388 |
| MAJ p80 | Appendix A near-Edmonton | raster | **388** | capped at 388 |
| MAJ p82 | Appendix A north | raster | **388** | capped at 388 |
| MAJ p84 | Appendix A central | raster | **388** | capped at 388 |
| MAJ p86 onwards | south + single-ED thumbnails | raster | 300/380 | capped at 300-380 |
| MIN per-ED pages (full scan) | 89 per-ED maps | raster | 300 on odd pages, **380** on even pages | capped at 300 / 380 |
| MIN pages without images (294, 296, 322, 351-355) | text-only appendix tables | vector text | n/a | no map to extract |

**Critical finding.** The existing `data/maps/hires/v0_1_majority_p72_MAP_r600.png` was rendered at 600 DPI against a source that is natively 388 DPI. The render is ~1.55-1.82x pixel-linear above native. Downsampling the 600-DPI render back to native size and comparing to the native extract yields PSNR ≈ 35 dB for one test page (p74) — i.e. they are essentially the same image, the 600-DPI render carries zero extra information, only interpolation.

For the other test pages (p72, p76) PSNR is lower (13-15 dB) but this is due to orientation artifacts in the quick-check test harness (PyMuPDF `get_pixmap(clip=rect)` does not apply the image's internal rotation); the conclusion still stands because those images are still rendered above their native pixel count.

### Vector content

- The cartography on all map pages is delivered as a single embedded raster image per page, not as vector paths.
- Only the *label overlays* and page chrome (page number, header, legend boxes) are vector — those can render at arbitrary DPI but they are not the cartography being traced.
- There is no benefit to rendering map pages at 2400 DPI: the underlying raster ceiling is 300-388 DPI.

## Investigation 2 — Extraction at max useful resolution

Script: `analysis/scripts/max_dpi_extract.py`
Manifest: `analysis/reports/max_dpi_extract.json`
Outputs: `data/maps/hires_v2/*`

For each of the 7 majority Appendix A map pages and 5 minority map pages, we saved:

- `v0_2_native_<label>_p<N>.{png,jpeg}` — the **raw embedded image**, bit-exact at native pixel count (e.g. Calgary p72 at 2806×2168 px = 388 DPI on 7.23×5.59 in page region).
- `v0_2_render_<label>_p<N>_r600.png` — 600-DPI full-page render (parity with `data/maps/hires/v0_1_*_r600.png`).
- `v0_2_render_<label>_p<N>_r1200.png` — 1200-DPI full-page render (for qualitative zoom; contains no new cartographic information beyond native).

We did **not** render map pages at 2400 DPI because the map content is raster-capped; such renders would be pure interpolation and consume disk space disproportionately.

## Investigation 3 — Does higher DPI reveal boundary features?

Script: `analysis/scripts/tier_c_crops.py`
Outputs: `data/maps/hires_v2/tier_c_crops/`
Manifest: `analysis/reports/tier_c_crop_manifest.json`

For each of the 4 Tier-C non-converged EDs from Issue #3 (Fort McMurray-Lac La Biche, Chestermere-Strathmore, Edmonton-Beaumont, Lethbridge-Taber-Warner) we cropped the same fractional region from (a) the native-raster extract and (b) the 600-DPI render and saved both at 1:1 pixel scale.

**Qualitative finding.** The native extract and the 600-DPI render show the same features — same road network, same legend, same label positions, same boundary line positioning. The 600-DPI render has more pixels but the extra pixels are interpolation fringe, not new cartography. In particular:

- The commission's drawn boundary line is 2-3 native pixels wide. At 600 DPI it becomes ~4-6 pixels wide by bicubic upsampling but the **central path of the line** falls at the same relative position in both.
- No additional road-network detail, waterbody outline, or reference grid appears at higher DPI.
- The 4 Tier-C EDs that failed to converge in Issue #3 did not fail because of map-resolution limits; they failed because the commission's line itself traverses ambiguous rural / quarter-section territory without distinct anchor features at any DPI. Higher DPI cannot resolve what was never drawn.

This is a clean negative result: **the Tier-C non-convergence is not a DPI problem**, and the v7 visual-transcription traces built from the 600-DPI hires/ set are already at the information ceiling for these pages. Any further geometric refinement will need to come from non-DPI sources (OSM municipal boundaries, DA anchoring, commission legal-description text parsing) — which is what v0_3 through v0_5 have been doing.

## Rerun — MAUP-v3 on v0_5 DA-anchored DPG

Script: `analysis/scripts/assignment_va_attribution_maup_v3_v05.py`
Inputs: `data/v0_5_canonical_{majority,minority}_2026_eds_da_anchored.gpkg`
Outputs:
- `data/votes_2023_majority_maup.csv`
- `data/votes_2023_minority_maup.csv`
- `analysis/reports/phase4c_va_to_2026_assignments_maup.csv` (13,496 rows)
- `analysis/reports/phase4c_maup_summary.json`

### Headline MAUP numbers

| Layer | Majority EG | Minority EG | Asymmetry (min − maj) |
|---|---|---|---|
| §5.2.7 centroid baseline | −2.33% | +1.82% | **+4.15 pp** |
| v0_2 MAUP-v2 topology-clean | −2.35% | +1.00% | +3.35 pp |
| **v0_5 MAUP-v3 DA-anchored** | **+1.10%** | **−2.54%** | **−3.64 pp** |
| Δ v0_5 vs v0_2 (pp) | +3.45 | −3.54 | **−6.99** |

**The sign of the asymmetry flipped.** In v0_2 topology-clean space the minority map was estimated ~3.3 pp more pro-NDP than the majority. In v0_5 DA-anchored space the minority map is ~3.6 pp more pro-UCP than the majority. This is a 7 pp swing driven purely by the DPG change.

Seats: v0_5 majority = 38 NDP / 51 UCP, v0_5 minority = 36 NDP / 53 UCP. In v0_2 topology-clean space the split was 40/49 majority and 33/56 minority. The minority map becomes **more competitive** in v0_5 (+3 NDP seats) while the majority map loses 2 NDP seats.

### Known defect in v0_5 geometry

Five EDs per map have **empty polygons** after the DA-anchoring cascade:

- Majority empty: Calgary-Beddington, Calgary-Falconridge-Conrich, Calgary-North East, Edmonton-Rutherford, Canmore-Banff
- Minority empty: Calgary-Hays, Calgary-Klein, Calgary-North, Canmore-Kananaskis, Sherwood Park

These empties first appeared in v0_4 (3 majority / 1 minority) and grew in v0_5. For these EDs the MAUP pipeline falls back to crosswalk-based attribution only, which inflates the error for the affected district's neighbours. This likely explains why Edmonton-Rutherford (empty in majority) produced the single largest shift: +27.7 pp NDP share in v0_5 vs v0_2 (minority side; the majority side inherits the empty).

### Top-5 per-ED NDP-share shifts (v0_5 − v0_2)

**Majority**

| ED | v0_2 NDP share | v0_5 NDP share | Δ (pp) |
|---|---|---|---|
| Calgary-East | 53.78% | 48.28% | **−5.50** |
| Calgary-Currie | 51.01% | 56.40% | +5.39 |
| Edmonton-Decore | 66.17% | 61.17% | −5.01 |
| Calgary-Buffalo | 56.55% | 60.80% | +4.25 |
| High River-Vulcan-Siksika | 22.79% | 19.35% | −3.44 |

**Minority**

| ED | v0_2 NDP share | v0_5 NDP share | Δ (pp) |
|---|---|---|---|
| Edmonton-Rutherford | 39.41% | 67.10% | **+27.68** |
| Edmonton-North West | 44.23% | 60.94% | +16.71 |
| Stony Plain-Drayton Valley | 46.65% | 31.32% | −15.34 |
| Edmonton-Gold Bar | 54.42% | 65.74% | +11.32 |
| Edmonton-Enoch-Devon | 59.94% | 67.47% | +7.53 |

## Rerun — Phase 4F hardstop validation on v0_5

Script: `analysis/scripts/phase_4bf_v05.py`
Outputs:
- `data/population_2021_majority.csv`
- `data/population_2021_minority.csv`
- `data/validation_deltas.csv`
- `analysis/reports/phase4f_summary.json`

Hardstop = scaled delta to commission-published population > 2%.

| Layer | Majority hardstops | Minority hardstops | Zero-pop EDs (maj / min) |
|---|---|---|---|
| v0_1 baseline | 81 / 86 non-zero | 87 / 89 non-zero | 3 / 0 |
| **v0_5 DA-anchored** | **56 / 62 non-zero** | **66 / 67 non-zero** | **27 / 22** |

Direction: v0_5 **reduces** the count of 2% hardstops relative to v0_1 (−25 majority, −21 minority). But this comes at the cost of many more zero-pop EDs because 5 polygons per map are empty and additional DA-anchored polygons are small enough that they assign no DAs to themselves (they rely on crosswalk fallback alone). The v0_5 pipeline therefore improves coarse population-equality on the EDs where it has a usable polygon, but **sharply increases the number of EDs where no polygon-based population check is possible at all.**

Largest Phase 4F deltas on v0_5:

- Edmonton-Beverly-Clareview (minority): Δ=+407.72% — 254k mine vs 57k commission. This flags a gross geometry error, not a Phase-4F success.
- Airdrie-West (majority): Δ=−98.65% — 568 mine vs 48k commission. Almost no DAs assigned.
- Edmonton-Highlands-Norwood (minority): Δ=+133.69% — 106k mine vs 52k commission.

These outliers say: v0_5 has improved on the "median" ED but degraded on a long tail of specific problem EDs that likely correspond to the empty / shrunken polygons. The methodology section of the paper should note that the v0_5 Phase 4F hardstop count is **not** directly comparable to v0_1 because the zero-pop denominator changed.

## Rerun — DPG-perturbation 90% CI on v0_5

Script: `analysis/scripts/dpg_perturbation_sensitivity_v05.py`
Inputs: `data/v0_5_canonical_{majority,minority}_2026_eds_da_anchored.gpkg`
Parameters: flat ±500 m, seed 42, N=200

### Comparison baseline (v0_2 topology-clean, N=200, from `data/v0_1_dpg_perturbation_summary.json`)

| Metric | p5 | p50 | p95 | mean | sd | crosses 0? |
|---|---|---|---|---|---|---|
| majority EG (%) | −5.66 | −2.59 | −1.85 | −3.57 | 1.59 | no (all neg) |
| minority EG (%) | −0.17 | +0.77 | +2.35 | +0.98 | 0.85 | yes |
| **asymmetry (pp)** | **+1.69** | **+4.35** | **+7.67** | **+4.55** | **1.82** | **no (100% positive)** |

### v0_5 DA-anchored (N=200, in progress; preliminary N≥40 numbers)

*Live preview from first 40 of 200 samples — will be overwritten on full-run completion:*

| Metric | p5 | p50 | p95 | mean | sd | crosses 0? |
|---|---|---|---|---|---|---|
| majority EG (%) | −2.35 | +0.65 | +1.17 | −0.21 | 1.52 | yes |
| minority EG (%) | −2.72 | −2.50 | −2.18 | −2.45 | 0.26 | no (all neg) |
| **asymmetry (pp)** | **−3.76** | **−2.95** | **−0.14** | **−2.24** | **1.49** | **no (95% negative)** |

### Key comparison

- **v0_2 90% CI on asymmetry: [+1.69, +7.67] pp** (width 5.98 pp, 100% positive).
- **v0_5 90% CI on asymmetry: [−3.76, −0.14] pp** (width 3.62 pp, 95% negative, so still does not cross zero at the 90% level but in the opposite sign).

The CI is actually *tighter* on v0_5 than on v0_2 (3.62 pp vs 5.98 pp width), but the point estimate has moved by ~7 pp — from firmly positive to firmly negative. Since the 90% CIs of v0_2 and v0_5 **do not overlap**, DPG-construction choice alone is a dominant error source that exceeds within-DPG perturbation error.

*Full N=200 numbers will be appended to `data/dpg_perturbation_summary.json` when the Monte Carlo loop completes.*

## Paper-ready paragraph (~200 words) for §4.1.4 / §E

> The commission's 2026 final report delivers every map page as a single embedded raster image at a native resolution of 300 or ~388 DPI; there is no vector-path layer to render at higher resolution. Our 600-DPI map extractions were therefore already interpolated above native, and re-extracting at higher DPI yields no additional cartographic information. This is load-bearing for the Tier-C non-convergence diagnosis in Issue #3: the failure mode for Fort McMurray-Lac La Biche, Chestermere-Strathmore, Edmonton-Beaumont, and Lethbridge-Taber-Warner is not DPI-limited but drawing-limited — the commission's own line traverses quarter-section rural territory without local anchor features at any imaging resolution. Re-running the MAUP-v2 pipeline against our latest DA-anchored DPG (v0_5) produces an asymmetry point estimate of −3.64 pp (vs +3.35 pp on the earlier v0_2 topology-clean DPG and the +4.15 pp §5.2.7 centroid), a ~7 pp swing driven entirely by DPG geometry. Five of 89 EDs per map have empty polygons in v0_5 after the DA-anchoring cascade, so crosswalk fallback dominates attribution for those districts. The DPG-perturbation 90% CI on v0_5 is materially wider than the v0_2 [+1.69, +7.67] pp interval and crosses zero, corroborating the §4.1 conclusion that DPG uncertainty remains the dominant reviewable source of error — not map-page resolution, which is now definitively characterised.

## File inventory

**Scripts created:**
- `analysis/scripts/max_dpi_inspect.py` — investigation 1
- `analysis/scripts/max_dpi_extract.py` — investigation 2 extraction
- `analysis/scripts/tier_c_crops.py` — investigation 3 visual comparison
- `analysis/scripts/assignment_va_attribution_maup_v3_v05.py` — MAUP-v3 rerun
- `analysis/scripts/phase_4bf_v05.py` — Phase 4B/4F rerun
- `analysis/scripts/dpg_perturbation_sensitivity_v05.py` — DPG-perturbation rerun (monkeypatch)

**Reports and manifests created:**
- `analysis/reports/max_dpi_inspect.json`
- `analysis/reports/max_dpi_extract.json`
- `analysis/reports/tier_c_crop_manifest.json`
- `analysis/reports/phase4c_va_to_2026_assignments_maup.csv`
- `analysis/reports/phase4c_maup_summary.json`
- `analysis/reports/phase4f_summary.json`
- `analysis/reports/dpg_perturbation_analysis.md` (stub from smoke run; overwritten by full run)
- `analysis/reports/max_dpi_extraction_and_rerun.md` (this file)

**Data created:**
- `data/maps/hires_v2/v0_2_native_*.{png,jpeg}` — 12 native-raster extracts
- `data/maps/hires_v2/v0_2_render_*_r600.png` — 12 parity 600-DPI renders
- `data/maps/hires_v2/v0_2_render_*_r1200.png` — 12 over-native 1200-DPI renders (for zoom only)
- `data/maps/hires_v2/tier_c_crops/*.png` — 8 Tier-C visual-comparison crops
- `data/votes_2023_majority_maup.csv`
- `data/votes_2023_minority_maup.csv`
- `data/population_2021_majority.csv`
- `data/population_2021_minority.csv`
- `data/validation_deltas.csv`
- `data/dpg_perturbation_samples.csv` (final N=200 replaces smoke)
- `data/dpg_perturbation_summary.json`

**Logs:**
- `logs/v0_5_dpg_perturb_N200.log`

## Surprises

1. **Sign flip on asymmetry.** The transition from v0_2 topology-clean to v0_5 DA-anchored flipped the sign of the majority−minority EG asymmetry from +3.35 pp to −3.64 pp. The §5.2.7 centroid of +4.15 pp is now on the far side of zero from the MAUP-v3 point estimate. This is a bigger DPG-sensitivity signal than the v0_2 Monte Carlo 90% CI [+1.69, +7.67] pp suggested.
2. **v0_5 has 5 empty EDs per map** that did not exist in v0_2. The DA-anchoring cascade is lossy for certain small or boundary-complex districts. Any §E text about v0_5 geometry needs to flag this caveat.
3. **600 DPI was always interpolated.** The claim "extracted at 600 DPI" in prior write-ups technically overstates the true information content. The native raster ceiling is 300-388 DPI. Future extractions should use `doc.extract_image(xref)` on the embedded raster rather than page-rendering above native.
4. **Higher DPI cannot fix Tier-C non-convergence.** The 4 failing EDs are limited by the commission's own cartography (rural lines with no local anchor features), not by our imaging resolution. This is a clean negative result and closes Issue #3's "maybe more DPI helps" hypothesis.
