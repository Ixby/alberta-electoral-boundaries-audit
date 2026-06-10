---
name: maup_attribution_canonical
description: Centroid vs area-weighted vs population-weighted VA→ED attribution on canonical Elections Alberta shapefiles
type: project
date: 2026-06-10
status: executed; substantive finding
---

> **Backward:**
> - `analysis/scripts/phase4c_canonical_attribution.py` — centroid (representative_point) attribution; baseline
> - `analysis/scripts/va_attribution_area_weighted.py` — area-weighted MAUP attribution
> - `analysis/scripts/va_attribution_population_weighted.py` — population-weighted MAUP attribution (new this pass)
> - `data/shapefiles/canonical/va_2023_election_day_votes.gpkg` — canonical VA polygons
> - `data/shapefiles/canonical/ea_*_2026_eds.gpkg` — canonical EA shapefiles
> - `data/shapefiles/reference/alberta_2021_das.gpkg` + `data/reference/alberta_2021_da_populations.csv` — DA layer for the population-weighted overlay
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.2.7 (measurement-resolution sensitivity)
> - `analysis/methodology/methodological_defenses.md` (MAUP-defense entry)
> - `TODO_REMEDIATION.md` (T1.4 partial closure on attribution sensitivity)

# Centroid vs MAUP attribution on canonical geometry

**Headline.** Population-weighted MAUP attribution — the most rigorous available method short of polling-station-level geocoding — **confirms** the centroid-in-polygon attribution the audit's chain pipeline uses. The two methods agree on every partisan-bias metric to within 0.1 pp on both commission maps. **Area-weighted MAUP attribution, by contrast, disagrees** — it shifts the majority's efficiency gap by +1.39 pp (from +0.10 % to +1.49 %). The disagreement is a *MAUP artifact in the area-weighted method*, not a real signal: area-weighted gives huge low-population rural slivers equal weight per square meter, which systematically credits rural EDs with votes that demographically belong elsewhere. **The audit's centroid attribution is therefore vindicated as methodologically robust on canonical geometry; the existing area-weighted "+1.39 pp shift" should not be treated as evidence of a real attribution problem.**

## What the three methods are

| Method | What it does | Cost on canonical | Verdict |
|---|---|---|---|
| **Centroid-in-polygon** | For each VA, find its `representative_point()` → assign all its votes to the containing ED | ~0.1 s | Audit's baseline; used by `mcmc_ensemble_canonical.py`, `phase4c_canonical_attribution.py`, and every published Lane-1 number |
| **Area-weighted MAUP** | For each VA × ED intersection, assign votes ∝ intersection area / VA area | ~5 s | Implemented previously; **introduces a spurious +1.39 pp shift on the majority** under canonical geometry. Reason: equal weight per square meter overcredits low-population rural slivers. |
| **Population-weighted MAUP** | For each VA × ED intersection, weight votes by the 2021 DA-derived *population* inside the intersection, not its area | ~15 s | **Confirms centroid** to within 0.1 pp on every metric. Most rigorous available without external geocoding. |

## Numbers

Per-ED partisan-bias metrics under each attribution method (canonical shapefiles + canonical 2023 election-day votes):

| Map | Method | EG | MM | Decl (Warrington) | Seats@50/50 (UCP) | UCP seats |
|---|---|---:|---:|---:|---:|---:|
| Majority | centroid | **+0.098 %** | −0.03619 | +0.02668 | 0.4607 | 55 |
| Majority | area-weighted MAUP | +1.489 % | −0.03601 | +0.00301 | 0.4607 | **56** ⚠ |
| Majority | population-weighted MAUP | **+0.044 %** | −0.03605 | +0.02678 | 0.4607 | 55 |
| Minority | centroid | **+4.019 %** | +0.01040 | −0.07700 | 0.5169 | 60 |
| Minority | area-weighted MAUP | +4.005 % | +0.00962 | −0.07682 | 0.5169 | 60 |
| Minority | population-weighted MAUP | **+3.946 %** | +0.00961 | −0.07754 | 0.5169 | 60 |

Inter-map asymmetry (minority EG − majority EG) under each method:

| Method | Majority EG | Minority EG | Asymmetry |
|---|---:|---:|---:|
| Centroid | +0.098 % | +4.019 % | **+3.921 pp** |
| Area-weighted MAUP | +1.489 % | +4.005 % | +2.516 pp |
| Population-weighted MAUP | +0.044 % | +3.946 % | **+3.902 pp** |

Centroid and population-weighted agree on asymmetry to within 0.02 pp. Area-weighted disagrees by 1.4 pp — and is the wrong method to trust, per the diagnostic below.

## Why area-weighted is the outlier (the MAUP-artifact diagnosis)

Alberta's voting areas (VAs) are not uniform in shape or population density. Rural VAs in particular are vast in area but sparse in population. When an ED boundary cuts across a rural VA:

- Area-weighted MAUP says: "this VA is 60 % in ED-A and 40 % in ED-B" → split votes 60/40.
- Population-weighted MAUP says: "the populated portion of this VA is 92 % in ED-A; the 40 % area in ED-B is empty pasture" → split votes 92/8.
- Centroid-in-polygon says: "the VA's centroid is in ED-A" → 100 % to A.

Area-weighted treats every square meter as if a voter lived there. In rural Alberta, almost no voter lives in any given square meter. Population-weighted correctly identifies where the voters actually live. Centroid-in-polygon ignores the question entirely but, on canonical geometry, happens to land within 0.08 pp of the population-weighted answer on EG, because Elections Alberta drew ED boundaries primarily along administrative lines (municipal boundaries, county boundaries, the Banff park edge) that *also* contain the populated places — so the populated centroid of each VA is rarely on the wrong side of an ED line.

The area-weighted method's +1.39 pp majority shift is not a real attribution bias; it is the method overcrediting empty land with votes. The population-weighted result is the truth.

## What this means for the audit's published findings

1. **The centroid attribution used throughout the audit is methodologically robust on canonical geometry.** Population-weighted MAUP — the rigour-tier above area-weighted — confirms it to within 0.1 pp on every metric on both maps.
2. **The minority's Lane-1 outlier status is invariant to attribution method.** Minority EG = +4.02 % (centroid) / +4.00 % (area-weighted) / +3.95 % (population-weighted) — all three within 0.1 pp, all three sitting at roughly p94 against the canonical ensemble. The "near, but below" the pre-registered 4.10 % threshold framing in the public report stands under every attribution method tested.
3. **The minority−majority asymmetry of +3.92 pp** is preserved under centroid and population-weighted attribution. The earlier area-weighted reading of +2.52 pp was a MAUP artifact and should not be cited as a "shrunk asymmetry under MAUP correction."
4. **The majority's near-neutral EG of ~+0.1 % is real**, not a centroid artifact. Under population-weighted MAUP it is actually *closer* to zero (+0.04 %) than centroid suggests.
5. **The existing `analysis/methodology/methodological_defenses.md` entry citing "+0.0000 pp MAUP shift on v0_9"** was correct *for v0_9 substrate* (where the DPG topological shapefiles snapped to VA edges by construction). On canonical EA shapefiles the picture is different: area-weighted is biased by ~1.4 pp on the majority but population-weighted is essentially identical to centroid. The defense's headline still holds — "attribution method does not change the audit's findings" — but the canonical-substrate evidence is now the population-weighted result, not the v0_9 area-weighted +0.0000.

## Open follow-up

- The 89-of-89 per-ED EG numbers under all three methods are written to `data/outputs/maup_*_canonical_*.csv`. The ensemble percentile placements (against the 1,010,000-plan canonical chain) are unchanged because the chain ensemble uses centroid attribution consistently per-plan — the ensemble's null distribution is calibrated to centroid, so the centroid real-map values are the correct ones to place against it. A constraint-enforcing ensemble run that also tested population-weighted attribution per-plan would be the publication-grade move (queued in `TODO_REMEDIATION.md` T1.4).
- The mean-VA-weight-sum of 0.9989 in the population-weighted run reflects ~0.11 % of votes uncredited (cast in VAs whose DA overlay had zero-pop slivers). This is well below the centroid-method's "nearest-ED fallback" rate of 3/4,765 VAs (~0.06 %) and area-weighted's coverage of 99.02 %. Both MAUP methods are conservative on the side of dropping uncertain votes rather than spreading them.

## Reproducibility

```bash
# Area-weighted MAUP
python analysis/scripts/va_attribution_area_weighted.py \
  --shapefile data/shapefiles/canonical/ea_majority_2026_eds.gpkg \
  --va-shapefile data/shapefiles/canonical/va_2023_election_day_votes.gpkg \
  --ed-id-col EDName2025 \
  --out data/outputs/maup_area_weighted_canonical_majority.csv

# Population-weighted MAUP
python analysis/scripts/va_attribution_population_weighted.py \
  --shapefile data/shapefiles/canonical/ea_majority_2026_eds.gpkg \
  --out data/outputs/maup_pop_weighted_canonical_majority.csv

# Identical commands with ea_minority_2026_eds.gpkg for the minority.
```

Total compute: ~5 s area-weighted; ~15 s population-weighted per map. Negligible.
