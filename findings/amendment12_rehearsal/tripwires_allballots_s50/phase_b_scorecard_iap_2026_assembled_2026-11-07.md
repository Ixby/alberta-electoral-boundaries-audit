# Phase B Scorecard — iap_2026_assembled

Date: 2026-11-07  
Shapefile: `data\shapefiles\iap_assembled\iap_2026_assembled.gpkg`  
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
  "pp_threshold_p10": 0.26795641039660306,
  "flagged_districts": []
}
```

## MO #3 — Municipal de-anchoring — ⚪ clean

municipal anchoring = 74.1% (Canadian norm threshold 70%)

```json
{
  "anchored_fraction": 0.7405816237272229,
  "threshold": 0.7,
  "methodology": "score_anchoring.py (tier-ordered snap, SNAP_TOL_M=500, VERTEX_DENSIFY_M=50)"
}
```

## MO #4 — Sampler divergence — ⚪ clean

map seats@50/50 = 0.4945 → ReCom percentile 99.8, SMC percentile 100.0, divergence -0.2pp (threshold 25pp)

```json
{
  "recom_percentile": 99.8080198019802,
  "smc_percentile": 99.99999999999987,
  "divergence_pp": -0.19198019801967803,
  "threshold_pp": 25
}
```

---

Pre-registered tripwire thresholds:

- MO #1 drain ratio threshold: 1.5x population-justified
- MO #2 Polsby-Popper percentile threshold: bottom 10%
- MO #3 anchoring threshold: 70%
- MO #4 sampler divergence threshold: 25pp
