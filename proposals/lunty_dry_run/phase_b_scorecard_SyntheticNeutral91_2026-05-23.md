# Phase B Scorecard — SyntheticNeutral91

Date: 2026-05-23  
Shapefile: `proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg`  
Tripwires fired: **2 of 3**

## MO #1 — Drain Pattern (city cracking) — 🔴 **FIRED**

2 cities exceed the 1.5x district-split threshold

```json
{
  "flagged_cities": [
    {
      "city": "Lethbridge",
      "population_2021": 98406,
      "districts_in_city": 3,
      "justified_districts": 2,
      "split_ratio": 1.5
    },
    {
      "city": "St. Albert",
      "population_2021": 68232,
      "districts_in_city": 3,
      "justified_districts": 2,
      "split_ratio": 1.5
    }
  ],
  "threshold_ratio": 1.5
}
```

## MO #2 — Lasso (surgical non-compactness) — ⚪ clean

no districts hit both bottom-decile PP AND mixed urban-rural

```json
{
  "pp_threshold_p10": 0.14902986112828515,
  "flagged_districts": []
}
```

## MO #3 — Municipal de-anchoring — 🔴 **FIRED**

municipal anchoring = 19.0% (Canadian norm threshold 70%)

```json
{
  "anchored_fraction": 0.1897484352668329,
  "threshold": 0.7
}
```

---

Pre-registered tripwire thresholds:

- MO #1 drain ratio threshold: 1.5x population-justified
- MO #2 Polsby-Popper percentile threshold: bottom 10%
- MO #3 anchoring threshold: 70%
- MO #4 sampler divergence threshold: 25pp
