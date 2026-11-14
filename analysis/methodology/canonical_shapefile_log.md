---
name: Canonical shapefile log
description: Provenance of official Elections Alberta shapefiles, a summary of what was requested and received, and reconciliation of which findings have been recomputed on canonical geometry vs. DPG-era estimates.
type: reference
---

> **Backward:**
> - Elections Alberta (files received on request, 2026-05-06) — source of canonical shapefiles
> - `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`, `ea_minority_2026_eds.gpkg`, `va_2023_election_day_votes.gpkg` — files documented here
> - `data/provenance_manifest.json` — provenance manifest
>
> **Forward:**
> - `analysis/scripts/mcmc_ensemble_canonical.py`, `joint_outlier_score_canonical.py`, `szat.py` — consume canonical shapefiles
> - `reports/academic/report_academic.md` §4.1.4, §7 (Acknowledgments) — cites the shapefile receipt

# Canonical Shapefile Log

## 1. Shapefile receipt

Official Elections Alberta shapefiles were received from Elections Alberta on request on **2026-05-06**. The package contained:

**CRS provenance correction (re-verified 2026-06-12 per T1.7 R2 Ref #10 against pyproj/EPSG registry directly):**

| EPSG | Name (per EPSG/pyproj) | k₀ | False easting | False northing |
|---|---|---|---|---|
| 3400 | NAD83 / Alberta 10-TM (**Forest**) | 0.9992 | 500,000 m | 0 m |
| 3401 | NAD83 / Alberta 10-TM (**Resource**) | 0.9992 | 0 m | 0 m |
| 3775–3778 | NAD83 / Alberta 3TM (four-zone, ref merid 111° / 114° / 117° / 120° W) | 0.9999 | varies | varies |

Round-1 of this correction (2026-06-12 morning) labeled EPSG:3400 as "Resource" and EPSG:3401 as "Forest" — **the Forest/Resource labels were swapped**. Round-1 also claimed k₀=0.9999 belongs to 3401 — wrong; 3400 and 3401 both have **k₀=0.9992** identically (the 0.9999 belongs to the 3TM family, EPSG:3775–3778). Round-1's "~0.07–0.14% area/perimeter difference between 3400 and 3401" was therefore **fictitious**: because the two CRSs share scale factor and projection family, areas and perimeters computed in either coordinate system are identical to within float-precision noise. The real hazard is a **500 km easting shift if coordinates are ever mixed un-reprojected in an sjoin** (the false easting differs by exactly 500,000 m). Compactness scripts (`compactness_metrics.py`, `polsby_popper.py`, `reock.py`) that reproject to 3401 while the pipeline default is 3400 will get identical area/perimeter, just translated; the sjoin hazard remains the operative concern. A pipeline-wide single-CRS constant + per-sjoin CRS-equality assertion is queued as T4.10-CRS.

Also corrected: `report_academic.md:121` still claims "Alberta 3TM, EPSG:3776" — neither label is in any current script; pipeline default is 3400 (10-TM Forest). To be fixed in the §4.x rewrite under T1.7 R2 sweep.

| File | CRS | Districts | Notes |
|---|---|---|---|
| `ea_majority_2026_eds.gpkg` | EPSG:3400 (Alberta 10-TM Forest) | 89 | Commission majority map |
| `ea_minority_2026_eds.gpkg` | EPSG:3400 (Alberta 10-TM Forest) | 89 | Commission minority map |
| `va_2023_election_day_votes.gpkg` | EPSG:3400 | 4,765 VAs | 2023 VA polygons with election-day vote columns |

Files are stored at `data/shapefiles/canonical/`. They are tracked via Git LFS. `data/provenance_manifest.json` covers derived outputs only. The shapefiles' SHA-256 hashes are in §2.1 below; the two commission-map files are also pinned in `analysis/utils/canonical_manifest.py`.

The §4.1.4 sunset clause was triggered on receipt and resolved in two stages:

- **2026-05-18 (day 12, inside the two-week window).** Headline-recompute obligation closed with the Phase 4C canonical re-run (`packing_cracking_analysis.py` against the canonical EA shapefiles).
- **2026-05-23 (day 17, three days over the two-week window).** Full canonical integration closed: R `redist` SMC canonical cross-check (2026-05-18), §5.3.5 neighbour-drain canonical re-run (2026-05-23), DPG-mess pruning (DPG-era findings moved to `archive/dpg_era/`), scripts purged of DPG-era constants, repo-wide `Backward:`/`Forward:` dependency-declaration convention added. The three-day overshoot is disclosed in `findings/methods_paper_draft.md` §6 + §7.1 Stage 12 and in `findings/pre_registration_amendment_log.md`.

The sunset-clause window itself was originally posted as 48 hours and relaxed to two weeks on 2026-04-26 (recorded in Amendment 5, Part 2); the disclosed reason (solo researcher without monitoring automation) is in the replaced entry's text at commit `ca539bc4` of `findings/pre_registration_amendment_log.md`. The clause is **in-repo discipline, not externally pre-registered** — the four OSF dossiers contain `dpg2_experiment_plan.md` + `drain_v2_plan.md`; neither specifies a timeline.

The committee gave the panel's report to the Assembly on 2026-11-02. No official shapefile of the panel's map has been posted, so the November scoring so far uses the audit's reconstruction and is provisional (`findings/a10_stepc/README.md`). Per OSF [qsgy8](https://osf.io/qsgy8/) / AsPredicted #289,455, the **scorecard methodology** is externally pre-registered and locked; the internal operational standard for applying it is 72 hours from map release (the earlier Bucket C wording is superseded; see Amendment 5, Part 11).

---

## 2. Elections Alberta correspondence (summary)

The correspondence itself is private and is not reproduced here. This section records only what was asked, what was received, and what the audit relies on.

### 2.1 Request and receipt

- **Requested.** The author asked Elections Alberta for the digital boundary files of the commission's majority and minority maps.
- **Received, 2026-05-06.** Elections Alberta's geomatics staff replied on that date with both boundary files, and asked to be sent the findings when complete. The files were received from Elections Alberta on request. They are not posted on Elections Alberta's maps page, so this repository's copies cannot be checked against a public download.
- **Files and hashes (SHA-256, as committed):**

| File | SHA-256 |
|---|---|
| `ea_majority_2026_eds.gpkg` | `5dcd4c6f931bdd04286bdeb17b183f673ca8d59f4f805ab27c70138b00f1a160` |
| `ea_minority_2026_eds.gpkg` | `82e29a719e96c7880b54355b5f18487a1912c1152479577b4c9b90862779e897` |
| `va_2023_election_day_votes.gpkg` | `9d9a08a0f9b99f07d158dcc7a14a57445ff32be065088587acd6713e5d7f51a5` |

The hashes are of the committed `.gpkg` files (their Git LFS object ids; the two commission-map files are also pinned in `analysis/utils/canonical_manifest.py`). The package as delivered was not archived, so the hashes show the committed files are unchanged since commit, not that they are the delivered bytes.

Receipt of the files does not imply that Elections Alberta endorses any finding.

### 2.2 Technical questions, 2026-05-07

On 2026-05-07 the author put four technical questions to Elections Alberta's geomatics staff and received answers the same day. In summary:

1. **Voting areas for the 2026 boundaries.** None exist yet, because the boundaries were under review by the Select Special Committee. The audit therefore assigns the 2023 voting areas (`va_2023_election_day_votes.gpkg`) to the 2026 divisions by centroid. No official dataset exists to check that assignment against.
2. **2023 results.** The source is Elections Alberta's published general-election reports, the Statement of Vote the audit already uses.
3. **Population data.** Elections Alberta did not supply the commission's population data. The audit uses 2021 dissemination-area populations (`data/va_pop_from_das.csv`). Elections Alberta has not confirmed the audit's computed values and has not endorsed its method.
4. **Municipal boundaries and communities of interest.** Elections Alberta's municipal boundaries come from the Alberta open-data municipal boundary dataset, the same public source the audit's anchoring analysis uses (`score_anchoring.py`). No GIS dataset of communities of interest was named. The audit draws no conclusion about how the commission worked from this exchange.

A further exchange from 2026-05-11 to 2026-05-13 concerned the population figure used for Airdrie in the commission's reports. The author resolved the question from public sources.

---

## 3. Finding reconciliation — canonical vs. DPG

The table below records which findings have been recomputed on official EA shapefiles (marked **[C]**) and which remain on DPG-derived geometry (marked **[DPG]**). DPG findings are retained in the historical record per pre-registration obligation and are superseded where a [C] equivalent exists.

| Finding | §§ | Substrate | Status |
|---|---|---|---|
| Efficiency gap (B1) | 5.2 | Phase 4C canonical | **[C]** majority +0.10%, minority +4.02% |
| Mean-median (B2) | 5.2 | Phase 4C canonical | **[C]** majority −3.62 pp, minority +1.04 pp |
| Declination (B3) | 5.2 | Phase 4C canonical | **[C]** majority +0.027, minority −0.077 *(swapped-operand signs from before Amendment 5, Part 9, as logged at the time; corrected convention per Amendment 5, Part 9 (sign fixed 2026-06-12): majority −0.027, minority +0.077 — see report §5.4.9)* |
| Seats@50/50 (B4) | 5.2 | Phase 4C canonical | **[C]** majority 48 NDP, minority 43 NDP |
| Population MAD (A1) | 5.1 | Commission per-ED tables | **[C]** independent of shapefile geometry |
| NE/central Calgary zone asymmetry (A2) *(zone label corrected 2026-07-08; previously logged as "NW" — the classified zone is NE/central per `findings/population_equality.md` §A2)* | 5.1 | Canonical EA shapefiles | **[C]** majority +2.8%, minority +11.5% |
| Airdrie split count | 5.3 | Canonical EA shapefiles | **[C]** majority 2 EDs, minority 4 EDs |
| MCMC ensemble (B5) | 5.4.9 | Canonical EA shapefiles | **[C]** 1,010,000 plans, 4 chains × 252,500 steps |
| SZAT (Ch2) | 5.2.10 | Canonical EA shapefiles | **[C]** p=0.0024 on the i.i.d. null, one-tailed; exploratory only, p=0.19 on the component-block null (`findings/szat_block_permutation.md`) |
| Mahalanobis D² (Ch1) | 5.4.9 | Canonical EA shapefiles | **[C]** p < 0.00001 |
| Fisher combination | 5.5 | Both canonical | **[C]** p=4.61×10⁻⁸ (later retired 2026-06-10) |
| Population MAD ensemble | 5.4.9 | Canonical EA shapefiles | **[C]** minority p99.1, majority p15.8 |
| Reock compactness | 5.4.9 | Canonical EA shapefiles | **[C]** null — both maps p100 |
| Municipal anchoring | 5.8.5 | Canonical EA shapefiles | **[C]** null — minority 71.8%, majority 80.0% |
| Polsby-Popper (C2) | 5.4 | DPG + canonical April 27 run | **[C]** values in `data/outputs/polsby_popper_per_district.csv` |
| Chair-anomaly analysis (§C3) | 5.3 | Canonical + commission text | **[C]** 3 minority anomalies, 0 majority |
| Sentiment analysis §5.9 | 5.9 | Commission submission text | Independent of shapefile geometry |

**DPG-era results** for B1–B4 are preserved in §5.4.1–§5.4.8 and superseded by the canonical Phase 4C values above. Per pre-registration obligation, no DPG finding is silently removed; superseded values are noted in the DOCUMENTED CORRECTIONS block.

---

## 4. VA polygon overlap warnings

When building the GerryChain adjacency graph from the canonical VA layer, the following 35 polygon-pair overlaps are detected by GerryChain's adjacency builder (reproducible from `b5_variant_run.err`):

```
(39,640), (39,2376), (39,2631), (39,2717), (39,4508),
(49,1087), (172,2370), (172,2890), (180,444), (180,1414),
(180,4615), (180,4637), (260,616), (260,2492), (444,4615),
(510,1087), (510,2191), (905,4255), (905,4637), (970,3032),
(1015,2499), (1045,3836), (1045,4435), (1087,1494),
(1087,2495), (1087,3245), (1087,4212), (1414,3840),
(1414,4615), (2154,2499), (3032,4764), (4056,4152),
(4056,4762), (4152,4762), (4255,4637)
```

These are slivers in the official EA VA layer — sub-pixel topology artefacts common in any large polygon dataset. GerryChain detects them as overlaps and logs a warning, but uses the topological adjacency information correctly. The centroid-in-polygon spatial join in Phase 4C is unaffected: centroids are points and a point cannot be inside two polygons unless they genuinely overlap by more than a sliver. The 99.20% centroid-in-declared-parent pass rate (gate S3b) is the relevant integrity measure. These overlaps do not affect any reported finding.
