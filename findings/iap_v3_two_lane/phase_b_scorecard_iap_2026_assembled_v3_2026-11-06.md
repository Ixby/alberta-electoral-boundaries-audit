# Phase B Scorecard — iap_2026_assembled_v3

Date: 2026-11-06  
Shapefile: `data\shapefiles\iap_assembled\iap_2026_assembled_v3.gpkg`  
Tripwires fired: **1 of 4**

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
  "pp_threshold_p10": 0.26827340344131534,
  "flagged_districts": []
}
```

## MO #3 — Municipal de-anchoring — ⚪ clean

municipal anchoring = 74.3% (Canadian norm threshold 70%)

```json
{
  "anchored_fraction": 0.7429422716216431,
  "threshold": 0.7,
  "methodology": "score_anchoring.py (tier-ordered snap, SNAP_TOL_M=500, VERTEX_DENSIFY_M=50)"
}
```

## MO #4 — Sampler divergence — ⚪ clean

map seats@50/50 = 0.4835 → ReCom percentile 98.8, SMC percentile 100.0, divergence -1.2pp (threshold 25pp)

```json
{
  "recom_percentile": 98.80287128712871,
  "smc_percentile": 99.98838424500975,
  "divergence_pp": -1.1855129578810448,
  "threshold_pp": 25
}
```

---

Pre-registered tripwire thresholds:

- MO #1 drain ratio threshold: 1.5x population-justified
- MO #2 Polsby-Popper percentile threshold: bottom 10%
- MO #3 anchoring threshold: 70%
- MO #4 sampler divergence threshold: 25pp
