---
name: Commission reference shapes — human cross-check vs approximation
description: Documents specific mismatches between the audit's Tier B approximate shapefiles and the commission's published per-ED thumbnails for Edmonton-Windermere, Calgary-De Winton, and Calgary-South. The commission thumbnails were visually cross-referenced from Appendix E (minority) during session 10 and the mismatches are recorded here so readers of the verification panels understand which approximations are known-inaccurate relative to the actual commission geometry.
forward_dependencies:
  - report_academic.md §6.7 (cites this file for the Tier B → Tier C reclassification)
  - Elections Alberta shapefile release (will close the gap)
backward_dependencies:
  - maps/verification/v0_3_*.png (the approximations the reader sees)
  - maps/minority_calgary.jpg, maps/hires/v0_1_minority_p360_map74.png (source thumbnails)
  - analysis/methodology/shape_refinement_v3.md (the refinement pass whose approximations are reclassified)
---

# Commission reference shapes — human cross-check

## Status note (session 10 close)

**v4 improved territorial fidelity substantially for all three EDs but remains materially off for Calgary-De Winton and Calgary-South.** The v4 pass (`analysis/methodology/shape_refinement_v4.md`) closed an estimated 90 % of the thumbnail-legible gap under its own error bands, but a further PO-provided reference on 2026-04-23 — a hand-painted overlay showing the commission's actual Calgary-De Winton (purple) and Calgary-South (green) shapes against the minority overview — establishes that v4's per-segment error bands were themselves too narrow:

- **Calgary-De Winton.** The commission's shape is roughly the full quadrant south of Calgary's southern city limit plus east of a north-south line near the Tsuut'ina reserve's east boundary, extending south well past the named Calgary ridings with a serrated rural southern boundary. v4 at 835 km² is likely less than 60 % of the true territorial footprint; the true footprint is more in the 1,400–1,700 km² range. Specific v4 gaps: the west edge should step further west, the north edge has a stepped indentation where Tsuut'ina Nation 145 notches into the ED, and the south edge extends materially further south than v4 placed it. **Correction to v4's Okotoks treatment (PO, 2026-04-23):** Okotoks is *inside* Calgary-De Winton at the ED's south-east-most edge, not subtracted from it as v4 assumed. This matches the original reference observation in §Calgary-De Winton below ("encompasses the Town of Okotoks") and contradicts v4's "subtract Okotoks town boundary" step. v5 refinement must keep Okotoks inside the De Winton polygon.
- **Calgary-South.** The commission's shape sits east of Calgary-Fish Creek (labelled ED 13) as a compact-to-medium urban block with a curved northwest edge where it abuts Fish Creek. v4 at 9 km² is approximately half the true size; the true footprint is likely 15–25 km². The general location is correct (south-east Calgary urban); the size is too small.
- **Edmonton-Windermere.** A second PO-painted reference on 2026-04-23 (the Edmonton-Windermere / Edmonton-South overview) establishes that v4 is also too small here. The commission's Windermere has (i) a main vertical lobe in south-west Edmonton following the North Saskatchewan River on its west side with a stepped/notched north edge along the river, and (ii) a distinctive rectangular *eastern arm* extending horizontally east from partway up the main body into what would otherwise be Edmonton-South territory. v4's simple "east cut at ~141 Street" does not capture the arm. The main body's south edge also extends further south than v4's Anthony Henday cut. v4 at 36.76 km² is probably 50–60 % of the true footprint; the true footprint is likely 55–70 km². Edmonton-South (ED 46) sits immediately east of the arm and inherits the inverse shape.

The observations above and below remain the canonical textual record of what the commission thumbnails show and what approximations miss. v4 remains the current best-effort approximation for all three EDs; the gaps listed here should be closed either by a v5 refinement pass (using the three 2026-04-23 PO-painted references as additional anchors) or by the commission shapefile release. Reference image sources: PO-painted overlays on the minority Calgary overview (De Winton purple + Calgary-South green) and the Edmonton-Windermere / Edmonton-South panel (Windermere orange/yellow), both 2026-04-23.

## Purpose

The v3 verification panels in `maps/verification/` show approximate polygon boundaries for the minority 2026 electoral divisions. Three of those approximations do not match the shapes the commission actually published in its minority-report thumbnails. This file documents the specific mismatches so a reader of the verification panels knows which approximations are faithful and which are not.

The three affected EDs are Edmonton-Windermere, Calgary-De Winton, and Calgary-South. All three were classified as Tier B (merge of 2019 parents) during the approximation pipeline. All three are actually Tier C (carve-out of 2019 parents) in the commission's real map. The approximation cannot recover a carve boundary without an OSM feature class to snap to, and the commission's carves in these three cases do not follow any standard OSM feature type (road, waterway, railway, admin boundary).

## Edmonton-Windermere (minority ED 51)

**Commission thumbnail (Appendix E).** The ED has a river-following western boundary along the North Saskatchewan River, a stepped / street-grid northern edge, a relatively clean southern edge, and a distinctive **upper-east carve-out** where the ED wraps around a peninsula of territory assigned to Edmonton-South. The peninsula extends northwest from Edmonton-South's main body into what would otherwise be Windermere territory.

**v3 approximation.** The west edge is correctly river-snapped (this is the one part the refinement captured). The upper-east carve-out is missing — the approximation occupies the peninsula territory that the commission assigned to Edmonton-South. This produces a ~119,000 m² apparent "overlap" with Edmonton-South across ~100 sliver regions, which is the approximation-to-reality gap, not a rendering bug.

**Residual voter impact (v3 symmetric-difference only).** 3 sensitive VAs, 796 votes on the river bank (left-right ambiguity) and the carve-out margin. True voter impact is larger and unquantifiable without the shapefile, because the approximation occupies wrong territory, not merely the wrong boundary.

## Calgary-De Winton (minority ED 6 or adjacent; numbering hard to read at thumbnail resolution)

**Commission thumbnail (Appendix E; minority Calgary overview p. 74).** A **large south-Calgary / southern-suburban-rural hybrid** that:
- Abuts the Tsuut'ina Nation reserve to the west (does not cross it)
- Extends south past Calgary's city limits
- Encompasses the Town of Okotoks (~25 km south of Calgary)
- Includes the De Winton community after which the ED is named

**v3 approximation.** A small compact polygon internal to south Calgary. Structurally wrong in scale — the approximation captures maybe 10–15 % of the territory the commission actually assigned to Calgary-De Winton. Okotoks is not in the approximation. The reserve-abutment is not reflected.

**Residual voter impact.** 1 sensitive VA, 217 votes under the v3 symmetric-difference metric. The true voter impact is much larger — Okotoks alone is ~32,000 people — but the impact cannot be computed under the current approximation because the approximation does not span the correct territory. This ED should be classified Tier C awaiting shapefile release; the Tier B classification applied during approximation was an error.

## Calgary-South (minority ED 26)

**Commission thumbnail (Appendix E; minority Calgary overview p. 74).** A compact roughly-rounded shape with a notch on the right side. Not especially elongated. Not sprawling.

**v3 approximation.** An elongated east-west shape with a distinct eastern extension and a southern tail. Wider and more spread than the commission's actual ED. The general location is correct (south Calgary); the shape is wrong.

**Residual voter impact.** 1 sensitive VA (shared with Calgary-De Winton), 217 votes under the v3 symmetric-difference metric. Like De Winton, the true voter impact is larger because the approximation occupies partly wrong territory rather than merely producing a misaligned boundary.

## Reclassification

Per these three mismatches, the §6.7 classification is updated:

- **Tier A (exact 2019 inheritance):** 57 majority + 65 minority EDs. Unchanged; the 2019 shapefile is authoritative.
- **Tier B orange-accepted (voter-neutral residual):** Lethbridge-Little Bow, Wetaskawin-Ponoka-Maskwacis. Unchanged.
- **Tier C awaiting shapefile (previously misclassified as Tier B refinement-significant):** Edmonton-Windermere, Calgary-De Winton, Calgary-South. These are explicitly marked as known-inaccurate approximations; the v3 panels should be read with this caveat.

The §6.7 residual voter impact of 1,012 votes on 4 VAs is the v1-to-v3 symmetric-difference measure — it is the floor, not the ceiling, of the approximation-to-reality gap. The true gap will be resolved only by commission shapefile release.

## Verification panel caption updates

Each v3 verification panel for the three EDs above should carry a header caveat noting:

> **Known-inaccurate approximation.** The commission's published thumbnail for this ED (Appendix E) shows a boundary the approximation pipeline cannot reconstruct from OSM features. The polygon rendered here is Tier C in substance despite its Tier B label. See `analysis/methodology/commission_reference_shapes.md`.

This caveat has been added to `maps/verification/v0_3_minority_edmonton_windermere.png`, `..._calgary_de_winton.png`, and `..._calgary_south.png` in the next rendering pass. Until that pass completes, this file is the canonical record of the mismatch.

## Source of the commission reference observations

The commission thumbnails were visually inspected from:
- `maps/minority_calgary.jpg` — Appendix E p. 74 (minority Calgary overview)
- `maps/hires/v0_1_minority_p360_map74.png` — 600-DPI re-extraction of the same page
- Individual per-ED thumbnails in the commission report's Appendix E

Specific shape descriptions above are from the PO's human review of the commission report, cross-referenced against the audit's approximation polygons in `maps/verification/v0_3_*.png`.
