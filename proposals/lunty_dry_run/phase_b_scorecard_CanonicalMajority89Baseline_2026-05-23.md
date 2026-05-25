# Phase B Scorecard — CanonicalMajority89Baseline

Date: 2026-05-23  
Shapefile: `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`  
Tripwires fired: **2 of 4**

## MO #1 — Drain Pattern (city cracking) — 🔴 **FIRED**

1 cities exceed the 1.5x district-split threshold

```json
{
  "flagged_cities": [
    {
      "city": "Lethbridge",
      "population_2021": 98406,
      "districts_in_city": 4,
      "justified_districts": 2,
      "split_ratio": 2.0
    }
  ],
  "threshold_ratio": 1.5
}
```

## MO #2 — Lasso (surgical non-compactness) — ⚪ clean

no districts hit both bottom-decile PP AND mixed urban-rural

```json
{
  "pp_threshold_p10": 0.2630372072265831,
  "flagged_districts": []
}
```

## MO #3 — Municipal de-anchoring — 🔴 **FIRED**

municipal anchoring = 36.1% (Canadian norm threshold 70%)

```json
{
  "anchored_fraction": 0.3611193361171811,
  "threshold": 0.7
}
```

## MO #4 — Sampler divergence — ⚪ clean

map seats@50/50 = 0.4607 → ReCom percentile 77.8, SMC percentile 95.2, divergence -17.4pp (threshold 25pp)

```json
{
  "recom_percentile": 77.81,
  "smc_percentile": 95.2083846074142,
  "divergence_pp": -17.3983846074142,
  "threshold_pp": 25
}
```

---

Pre-registered tripwire thresholds:

- MO #1 drain ratio threshold: 1.5x population-justified
- MO #2 Polsby-Popper percentile threshold: bottom 10%
- MO #3 anchoring threshold: 70%
- MO #4 sampler divergence threshold: 25pp
