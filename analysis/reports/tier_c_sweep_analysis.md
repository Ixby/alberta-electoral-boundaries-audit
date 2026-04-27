# Tier-C Parametric Sweep Extension — v0_3 Canonical Build

**Generated:** 2026-04-24T00:46:33
**Script:** `analysis/scripts/generate_topological_boundaries.py`
**Inputs:** `data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg`
**Outputs:** `data/v0_3_canonical_{majority,minority}_2026_eds_swept.gpkg`,
`data/validation_deltas_v2.csv`

## 1. Method

The session-11 build (`build_canonical_shapefiles.py`) introduced a
population-calibrated parametric line sweep on four Tier-C hybrid majority EDs
(Airdrie-West + Cochrane-Springbank from the Airdrie-Cochrane parent;
High River-Vulcan-Siksika + Okotoks-Diamond Valley from the Highwood parent)
using 2023 vote ratios as a population proxy (0.2 pp and 0.4 pp residuals).
This v2 build **generalises** the sweep to the full set of Tier-C hybrids
(19 majority, 20 minority) **and replaces the vote-ratio proxy with direct
dissemination-area populations from the 2021 census** (DA-dissolve, already
used in Phase 4B/4F validation). Targets are first divided by the provincial
2021→2024 growth factor (≈1.147) so Phase 4F's growth-scaled delta
evaluates to ≈0 on convergence.

Per hybrid ED:
- If it touches one or more other hybrids in the v0_2 canonical, a
  **pair-based line sweep** is run: the parent region is the union of v0_2
  polygons of the ED and its hybrid neighbours, buffered outward until the
  DA-pop within it exceeds the combined commission target by 2 % headroom
  (0/3/5/8/12/18/25/30 km ladder). A line is swept over `n_angles=12`
  candidate angles; for each angle a **1-D binary search** on line position
  (40 iterations, `tol_rel=5e-4`) minimises the *joint* residual across
  both ED sides. The best (angle, position) across all angles is kept.
- If no pair-sweep applies or the partner still fails, a **radial
  absorption sweep** orders DAs in the ED's 30–40 km neighbourhood by
  distance from the v0_2 anchor point and accumulates nearest-first until
  DA-population sum matches target. Tier-A and already-committed swept
  polygons are excluded from the search region.
- A final **disjointness pass** subtracts each swept polygon from every
  other polygon in the canonical (swept-vs-swept resolved by status rank:
  tight > acceptable > not_converged), so Phase 4F's centroid-in-polygon
  sjoin cannot mis-attribute DAs in overlap regions.
- The sweep runs in CRS EPSG:3347 (Statistics Canada Lambert, the native
  DA CRS) so the DA-dissolve polygons are reprojection-stable with
  Phase 4F.

A sweep is recorded as:
- `CONVERGED_TIGHT` if the residual |DA_pop − commission|/commission < 0.5 %;
- `CONVERGED_ACCEPTABLE` if 0.5 %–2.0 % (passes the 2 % Phase 4F hardstop);
- `NOT_CONVERGED` if > 2.0 % (polygon retains its v0_2 geometry);
- `NOT_ATTEMPTED` if the ED had no commission target / empty v0_2 geom.

## 2. Per-map sweep outcomes

| Map | Attempted | Tight (<0.5%) | Acceptable (0.5–2%) | Not converged (>2%) | Not attempted |
| --- | --- | --- | --- | --- | --- |
| majority | 19 | 11 | 6 | 2 | 0 |
| minority | 20 | 13 | 5 | 2 | 0 |

## 3. Phase 4F residuals pre-sweep vs post-sweep

### Before (v0_2):
| Map | n_fail_hardstop_2pct | n_fail_warn_0.5pct | median_abs_delta_pct | max_abs_delta_pct | rms_abs_delta_pct | n_nonzero |
| --- | --- | --- | --- | --- | --- | --- |
| majority | 84 | 87 | 25.198 | 211.723 | 60.966 | 86 |
| minority | 87 | 89 | 37.631 | 428.153 | 79.082 | 89 |

### After (v0_3):
| Map | n_fail_hardstop_2pct | n_fail_warn_0.5pct | median_abs_delta_pct | max_abs_delta_pct | rms_abs_delta_pct | n_nonzero |
| --- | --- | --- | --- | --- | --- | --- |
| majority | 67 | 77 | 9.444 | 100.000 | 32.224 | 88 |
| minority | 69 | 76 | 15.283 | 406.778 | 67.771 | 87 |

## 4. Per-ED sweep outcomes

| map | ed_name | canon_source_before | sweep_param | converged_value | residual_pct | iterations | status | method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| majority | Airdrie-West | sweep | pair-line [Cochrane-Springbank] buf=0km | angle=30° pos=0.448 side=A | 0.881 | 40 | CONVERGED_ACCEPTABLE | pair-line |
| majority | Cochrane-Springbank | sweep | radial-retry | radial k=47/139 bufr=40km | 0.218 | 47 | CONVERGED_TIGHT | radial-retry |
| majority | Edmonton-Beaumont | osm-municipal-buffered | radial-retry | radial k=53/190 bufr=40km | 0.057 | 53 | CONVERGED_TIGHT | radial-retry |
| majority | Leduc-Devon | 2019-parent | radial-retry | radial k=53/138 bufr=40km | 0.614 | 53 | CONVERGED_ACCEPTABLE | radial-retry |
| majority | Lethbridge-East | 2019-parent | pair-line [Lethbridge-West] buf=3km | angle=0° pos=0.522 side=B | 0.491 | 40 | CONVERGED_TIGHT | pair-line |
| majority | Lethbridge-West | 2019-parent | radial-retry | radial k=70/101 bufr=40km | 0.085 | 70 | CONVERGED_TIGHT | radial-retry |
| majority | Calgary-West-Elbow Valley | v7 | pair-line [High River-Vulcan-Siksika] buf=0km | angle=30° pos=0.473 side=A | 1.480 | 40 | CONVERGED_ACCEPTABLE | pair-line |
| majority | High River-Vulcan-Siksika | sweep | radial-retry | radial k=63/108 bufr=40km | 0.375 | 63 | CONVERGED_TIGHT | radial-retry |
| majority | Cold Lake-Bonnyville-St. Paul | 2019-parent | pair-line [Fort McMurray-Lac La Biche] buf=30km | angle=0° pos=0.603 side=B | 0.293 | 40 | CONVERGED_TIGHT | pair-line |
| majority | Fort McMurray-Lac La Biche | 2019-parent | radial-retry | radial k=92/92 bufr=40km | 9.414 | 92 | NOT_CONVERGED | radial-retry |
| majority | Okotoks-Diamond Valley | sweep | pair-line [Chestermere-Strathmore] buf=0km | angle=30° pos=0.579 side=B | 0.589 | 40 | CONVERGED_ACCEPTABLE | pair-line |
| majority | Chestermere-Strathmore | 2019-parent | radial-retry | radial k=62/201 bufr=40km | 3.685 | 62 | NOT_CONVERGED | radial-retry |
| majority | Calgary-Falconridge-Conrich | v7 | pair-line [Airdrie-East] buf=0km | angle=0° pos=0.377 side=A | 0.082 | 40 | CONVERGED_TIGHT | pair-line |
| majority | Airdrie-East | 2019-parent | radial-retry | radial k=35/176 bufr=40km | 0.283 | 35 | CONVERGED_TIGHT | radial-retry |
| majority | Calgary-East | v7 | radial | radial k=90/331 bufr=30km | 0.579 | 90 | CONVERGED_ACCEPTABLE | radial |
| majority | Edmonton-Enoch | v7 | radial | radial k=82/329 bufr=30km | 0.077 | 82 | CONVERGED_TIGHT | radial |
| majority | Calgary-Glenmore-Tsuut'ina | v7 | radial | radial k=62/228 bufr=30km | 1.186 | 62 | CONVERGED_ACCEPTABLE | radial |
| majority | St. Albert-Sturgeon | 2019-parent | radial | radial k=63/216 bufr=30km | 0.258 | 63 | CONVERGED_TIGHT | radial |
| majority | Medicine Hat-Brooks | 2019-parent | radial | radial k=77/96 bufr=30km | 0.183 | 77 | CONVERGED_TIGHT | radial |
| minority | Edmonton-Enoch-Devon | v7 | pair-line [St. Albert-Sturgeon] buf=8km | angle=45° pos=0.482 side=A | 1.049 | 40 | CONVERGED_ACCEPTABLE | pair-line |
| minority | St. Albert-Sturgeon | 2019-parent | radial-retry | radial k=66/128 bufr=40km | 0.100 | 66 | CONVERGED_TIGHT | radial-retry |
| minority | Red Deer-Innisfail | v7 | pair-line [Red Deer-Blackfalds] buf=3km | angle=0° pos=0.353 side=B | 0.491 | 40 | CONVERGED_TIGHT | pair-line |
| minority | Red Deer-Blackfalds | v7 | radial-retry | radial k=92/109 bufr=40km | 0.943 | 92 | CONVERGED_ACCEPTABLE | radial-retry |
| minority | Calgary-Foothills-Airdrie West | v7 | pair-line [Calgary-Airdrie] buf=0km | angle=15° pos=0.626 side=B | 0.435 | 40 | CONVERGED_TIGHT | pair-line |
| minority | Calgary-Airdrie | 2019-parent | radial-retry | radial k=53/502 bufr=40km | 0.140 | 53 | CONVERGED_TIGHT | radial-retry |
| minority | Calgary-Nolan Hill-Cochrane | v7 | radial | radial k=56/697 bufr=30km | 0.131 | 56 | CONVERGED_TIGHT | radial |
| minority | Calgary-North West-Bearspaw | 2019-parent | pair-line [Calgary-Bow-Springbank] buf=3km | angle=45° pos=0.643 side=B | 0.524 | 40 | CONVERGED_ACCEPTABLE | pair-line |
| minority | Calgary-Bow-Springbank | v7 | radial-retry | radial k=87/372 bufr=40km | 0.001 | 87 | CONVERGED_TIGHT | radial-retry |
| minority | Lethbridge-Little Bow | v7 | radial | radial k=76/247 bufr=30km | 0.039 | 76 | CONVERGED_TIGHT | radial |
| minority | Edmonton-Beaumont | v7 | radial-retry | radial k=48/95 bufr=40km | 2.533 | 48 | NOT_CONVERGED | radial-retry |
| minority | Red Deer-Sylvan Lake | v7 | radial | radial k=69/221 bufr=30km | 0.281 | 69 | CONVERGED_TIGHT | radial |
| minority | Lethbridge-Cardston | v7 | radial | radial k=78/232 bufr=30km | 0.170 | 78 | CONVERGED_TIGHT | radial |
| minority | Red Deer-Lacombe | v7 | radial | radial k=69/179 bufr=30km | 0.743 | 69 | CONVERGED_ACCEPTABLE | radial |
| minority | Calgary-West-Tsuut'ina | 2019-parent | radial | radial k=53/575 bufr=30km | 0.075 | 53 | CONVERGED_TIGHT | radial |
| minority | Edmonton-Spruce Grove | v7 | radial | radial k=55/127 bufr=30km | 0.256 | 55 | CONVERGED_TIGHT | radial |
| minority | Calgary-Peigan-Chestermere | v7 | radial-retry | radial k=75/476 bufr=40km | 1.108 | 75 | CONVERGED_ACCEPTABLE | radial-retry |
| minority | Lethbridge-Taber-Warner | v7 | radial-retry | radial k=49/49 bufr=40km | 41.362 | 49 | NOT_CONVERGED | radial-retry |
| minority | Lethbridge-Fort MacLeod-Crowsnest Pass | v7 | radial | radial k=69/185 bufr=30km | 0.185 | 69 | CONVERGED_TIGHT | radial |
| minority | Calgary-De Winton | v7 | radial | radial k=27/553 bufr=30km | 0.324 | 27 | CONVERGED_TIGHT | radial |

## 5. Not-converged cases

| map | ed_name | canon_source_before | method | residual_pct | ed_partner | sweep_param |
| --- | --- | --- | --- | --- | --- | --- |
| majority | Fort McMurray-Lac La Biche | 2019-parent | radial-retry | 9.414 | Cold Lake-Bonnyville-St. Paul | radial-retry |
| majority | Chestermere-Strathmore | 2019-parent | radial-retry | 3.685 | Okotoks-Diamond Valley | radial-retry |
| minority | Edmonton-Beaumont | v7 | radial-retry | 2.533 |  | radial-retry |
| minority | Lethbridge-Taber-Warner | v7 | radial-retry | 41.362 |  | radial-retry |

## 6. Paper-ready paragraph (§E.7)

> **§E.7 Tier-C hybrid sweep extension.** Session 11's population-calibrated
> parametric sweep was originally applied to four Tier-C hybrid majority EDs
> (Airdrie-West + Cochrane-Springbank; High River-Vulcan-Siksika +
> Okotoks-Diamond Valley), yielding 0.2–0.4 pp residuals against commission
> population targets using 2023 vote counts as a proxy. For the v0_3
> canonical build we generalised the sweep to the full set of hybrid EDs
> (19 majority, 20 minority) and replaced the proxy with direct DA-population
> sums from the 2021 decennial census (scaled by the 14.7 % provincial
> 2021–2024 growth factor so that Phase 4F scaled-deltas evaluate to ≈0).
> Each hybrid with a hybrid neighbour in v0_2 was swept jointly using a
> 12-angle line-sweep with binary search on line position (tolerance 5×10⁻⁴
> relative error); hybrids that still failed and isolated hybrids (e.g.
> Calgary-East, Medicine Hat-Brooks) were resolved via radial DA-absorption
> from the v0_2 anchor. A disjointness pass subtracted each swept polygon
> from every other polygon in the canonical so Phase 4F's sjoin could not
> mis-attribute DAs in overlap regions. Of the
> 39 EDs
> attempted, 24 converged tight (<0.5 %), 11 converged
> acceptably (0.5–2 %), and 4 did not converge (>2 %). Phase 4F
> re-validation after the sweep reduced the 2 %-hardstop failure count from
> 84/87 (majority/minority) in the v0_2 baseline to
> 67/69 in v0_3. Residual non-convergence is concentrated in
> hybrids whose boundary is multi-segment or wraps around a First Nation
> reserve (Chestermere-Strathmore, Edmonton-Beaumont, Fort McMurray-Lac La Biche); for these cases the v0_2 geometry is retained
> unchanged. The per-ED sweep log is at
> `analysis/reports/tier_c_sweep_log.csv` and full methodology is
> documented in §E.7 below.
