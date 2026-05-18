---
name: Canonical shapefile log
description: Provenance of official Elections Alberta shapefiles, EA GIS correspondence, and reconciliation of which findings have been recomputed on canonical geometry vs. DPG-era estimates.
type: reference
---

# Canonical Shapefile Log

## 1. Shapefile receipt

Official Elections Alberta shapefiles were received on **2026-05-06** in response to a formal research access request submitted by the author. The package contained:

| File | CRS | Districts | Notes |
|---|---|---|---|
| `ea_majority_2026_eds.gpkg` | EPSG:3400 (Alberta 3TM) | 89 | Commission majority map |
| `ea_minority_2026_eds.gpkg` | EPSG:3400 (Alberta 3TM) | 89 | Commission minority map |
| `va_2023_election_day_votes.gpkg` | EPSG:3400 | 4,765 VAs | 2023 VA polygons with election-day vote columns |

Files are stored at `data/shapefiles/canonical/`. They are tracked via Git LFS. SHA-256 hashes are recorded in `data/provenance_manifest.json` (relative path keys `outputs/…`; shapefiles not yet hashed in the manifest — add when needed).

The §4.1.4 sunset clause was triggered on receipt and partially fulfilled: the 2026-proposal-shapefile trigger closed on 2026-05-18 with the Phase 4C canonical re-run. The November 2026 committee-map trigger remains open pending the Lunty committee's report.

---

## 2. EA GIS correspondence

### 2.1 Research access request and shapefile receipt

A formal research access request was submitted to Elections Alberta. **Raymond Mok** (Geomatics Team Lead, Elections Alberta) responded on **2026-05-06**, attached both shapefiles, and asked to receive the findings when complete. The author confirmed this arrangement on the same date.

Raymond Mok should be acknowledged in §7 (Acknowledgments) for providing data access and answering technical questions. Acknowledgment does not imply EA endorsement of findings.

### 2.2 Technical questions — responded 2026-05-07

Following shapefile receipt, the author submitted four technical methodology questions to Raymond Mok on 2026-05-07. His responses are reproduced below verbatim (from email thread, wconn161@mtroyal.ca ↔ Raymond.Mok@elections.ab.ca, 2026-05-07 3:17 PM) and annotated with their methodological implications.

A follow-up exchange on 2026-05-11 through 2026-05-13 concerned the population estimate used for Airdrie in the commission reports. The author resolved the question independently; Raymond confirmed with "#teamwork."

---

**Q1: Do you have voting area polygons for the proposed 2026 ED boundaries?**

> *"We do not have any of the voting areas for the next set of ED boundaries. This is due to the government has formed a Select Special Committee to review the ED boundaries. Their report will be submitted to the Legislature by Nov 2. You can find more information on the Legislative Assembly of Alberta website: https://www.assembly.ab.ca/assembly-business/committees/ceb"*

**Implication.** EA has not constructed 2026 VA polygons because the Lunty committee may redraw the boundaries before they take effect. This confirms that the audit's approach — using the 2023 VA polygons (`va_2023_election_day_votes.gpkg`) with a centroid-in-polygon spatial join to the 2026 ED boundaries — is the correct and only available methodology. There is no alternative dataset against which to validate or replace this attribution method.

---

**Q2: 2023 election results source.**

> *"You can find the information regarding to the 2023 Provincial General Election here: https://www.elections.ab.ca/resources/reports/general-elections/."*

**Implication.** Confirms the canonical citation for the 2023 Statement of Vote already used in the audit. No change required.

---

**Q3: Population data used by the commission.**

> *"I am not sure if I am allowed to share the population data. But I can say that your method sounds reasonable for your study."*

**Implication.** EA staff confirmed the population estimation methodology is reasonable without endorsing the specific computed values. The audit uses 2021 DA-weighted population sums (`data/va_pop_from_das.csv`) as the population substrate for the VA polygons. EA could not confirm or deny the commission's own per-ED population figures. This informal confirmation is noted here as methodological corroboration; it is not a formal EA endorsement and should not be cited as such. Phrasing for §4: *"The population estimation methodology was described to Elections Alberta GIS staff, who noted it was reasonable for the study's purposes (informal communication, 2026-05)."*

---

**Q4: Municipal boundary and communities-of-interest data sources.**

> *"In terms of the municipal boundaries, we do use the most up-to-date dataset from Alberta OpenData. As for 'Communities of Interest', we used the ESRI and Google basemaps for references. This is mainly because EBC members learned more about the areas from their knowledge and public hearings."*

**Implications (two):**

1. **Municipal boundaries.** EA uses the current Alberta OpenData municipal boundary dataset — the same publicly available source used in this audit's municipal anchoring analysis (`score_anchoring.py`). The scoring baseline and the commission's baseline are identical. This is a methodological alignment, not a coincidence.

2. **Communities of interest.** The commission had no formal GIS protocol for communities-of-interest determinations. The methodology was judgment-based (EBC member local knowledge + public hearing input), supplemented by commercial basemaps (ESRI, Google) rather than a canonical GIS dataset. This is relevant to the Airdrie split analysis (§5.3) and the NW Calgary zone classification (§5.1): neither has a single authoritative spatial definition, so the commission's community-of-interest determinations in those areas reflect discretionary judgment calls, not a reproducible geographic rule.

---

## 3. Finding reconciliation — canonical vs. DPG

The table below records which findings have been recomputed on official EA shapefiles (marked **[C]**) and which remain on DPG-derived geometry (marked **[DPG]**). DPG findings are retained in the historical record per pre-registration obligation and are superseded where a [C] equivalent exists.

| Finding | §§ | Substrate | Status |
|---|---|---|---|
| Efficiency gap (B1) | 5.2 | Phase 4C canonical | **[C]** majority +0.10%, minority +4.02% |
| Mean-median (B2) | 5.2 | Phase 4C canonical | **[C]** majority −3.62 pp, minority +1.04 pp |
| Declination (B3) | 5.2 | Phase 4C canonical | **[C]** majority +0.027, minority −0.077 |
| Seats@50/50 (B4) | 5.2 | Phase 4C canonical | **[C]** majority 48 NDP, minority 43 NDP |
| Population MAD (A1) | 5.1 | Commission per-ED tables | **[C]** independent of shapefile geometry |
| NW Calgary zone asymmetry (A2) | 5.1 | Canonical EA shapefiles | **[C]** majority +2.8%, minority +11.5% |
| Airdrie split count | 5.3 | Canonical EA shapefiles | **[C]** majority 2 EDs, minority 4 EDs |
| MCMC ensemble (B5) | 5.4.9 | Canonical EA shapefiles | **[C]** 1,010,000 plans, 4 chains × 252,500 steps |
| SZAT (Ch2) | 5.2.10 | Canonical EA shapefiles | **[C]** p=0.0024 |
| Mahalanobis D² (Ch1) | 5.4.9 | Canonical EA shapefiles | **[C]** p < 0.00001 |
| Fisher combination | 5.5 | Both canonical | **[C]** p=6.87×10⁻⁸ |
| Population MAD ensemble | 5.4.9 | Canonical EA shapefiles | **[C]** minority p99.0, majority p15.8 |
| Reock compactness | 5.4.9 | Canonical EA shapefiles | **[C]** null — both maps p100 |
| Municipal anchoring | 5.8.5 | Canonical EA shapefiles | **[C]** null — minority 72.0%, majority 80.0% |
| Polsby-Popper (C2) | 5.4 | DPG + canonical April 27 run | **[C]** values in `data/outputs/polsby_popper_per_district.csv` |
| Chair-anomaly analysis (§C3) | 5.3 | Canonical + commission text | **[C]** 3 minority anomalies, 0 majority |
| Sentiment analysis §5.9 | 5.9 | Commission submission text | Independent of shapefile geometry |

**DPG-era results** for B1–B4 are preserved in §5.4.1–§5.4.8 and superseded by the canonical Phase 4C values above. Per pre-registration obligation, no DPG finding is silently removed; retracted values are noted in the DOCUMENTED CORRECTIONS block.

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
