# Pending Recompute — Known Stale Values

**Status as of:** 2026-05-10  
**Gate G2: COMPLETE** — canonical values from `simulated_ensemble_percentiles_canonical.csv` propagated to §5.4.9, §5.5, §6.2.1, and §6.2.2 on 2026-05-10.  
**Scope decision:** Only official Elections Alberta geometry is authoritative for MCMC scoring.  
**Official EA shapefiles received:** 2026-05-06 (Raymond Mok)

---

## The situation

All MCMC real-map scoring results currently in `report_academic.md` §5.4 were produced against **Derived Provisional Geometries (DPGs)** — the audit's own reconstructed boundary polygons. These runs predate the official EA shapefile delivery.

| Run | Geometry | Status |
| --- | --- | --- |
| Run #1/2 (10k preliminary) | v0_6 partial-coverage DPG | Historical — superseded |
| Run #3 (250k full) | v0_6 full-coverage DPG | Historical — superseded |
| Run #4 (250k v0_8) | v0_8 full-coverage DPG | Historical — superseded |
| Run #5 (1M v0_8) | v0_8 full-coverage DPG | Historical — superseded |
| Multichain (3×150k) | canonical DPG | Historical — superseded |
| **G2 target run** | **Official EA shapefiles** | **Not yet run — this is what G2 produces** |

The ensemble distribution (the neutral random-walk plans) does not need to be re-run: it is generated from the 4,765 VA polygon substrate, which is independent of the real-map boundaries. Only the **real-map scoring** changes — assigning VAs to EDs using official EA polygons instead of DPGs.

---

## What G2 requires

1. Run real-map scoring for the three maps (2019 enacted, majority 2026, minority 2026) using official EA boundary shapefiles against the existing 250k+ neutral ensemble.
2. Output to `data/simulated_ensemble_percentiles_full_100k.csv` (or equivalent; name TBD).
3. Propagate official-geometry percentiles into §5.4 headline prose and summary tables.
4. Retain DPG run values in the §5.4 run-comparison tables as **historical record** — clearly labelled "DPG-based, pre-official-shapefile."

---

## Values expected to change

The following §5.4 headline values are DPG-based and will be replaced by G2 output. They are not errors — they are the best available numbers before official shapefiles arrived. Do not treat discrepancies between these values and the official-geometry run as suspicious.

| Metric | Current report value (DPG-based) | Run source | Will change to |
| --- | --- | --- | --- |
| Minority EG | p100.0 | Run #5 v0_8 | TBD — official geometry |
| Minority mean-median | p87.4 / p95.35 (ESS-downgraded) | Run #5 / Run #3 | TBD |
| Minority declination | p3.0 | Run #5 | TBD |
| Minority seats@50/50 | p100.0 | Run #5 | TBD |
| Majority EG | p99.93 | Run #5 | TBD |
| Majority mean-median | p53.5 | Run #5 | TBD |
| Majority declination | p41.5 | Run #5 | TBD |
| Majority seats@50/50 | p21.6 | Run #5 | TBD |

The "TBD" cells cannot be filled until the official-geometry run completes.

---

## What does NOT change at G2

- The ensemble distribution itself (neutral draws from the VA substrate)
- The Fisher combination test (Ch1 + Ch2), which does not depend on MCMC percentile values
- The structural findings (§5.1 population equality, §5.8 geographic coherence, §5.9 procedural)
- The SZAT bootstrap (§5.3)
- The Mahalanobis joint-tail test (§5.5)

The MCMC percentiles are one input to the §6.2 verdict. They are not the load-bearing signal.

---

## Do not update §5.4 manually before G2 runs

Editing individual percentile numbers without re-running the official-geometry scoring would create an internally inconsistent document. Wait for G2.
