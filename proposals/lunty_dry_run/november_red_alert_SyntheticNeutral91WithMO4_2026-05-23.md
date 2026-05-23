# November Red Alert Scorecard — SyntheticNeutral91WithMO4

Date: 2026-05-23  
Shapefile: `proposals/lunty_dry_run/synthetic_neutral_91_test_input.gpkg`  
Tripwires fired: **2 of 4**

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

## MO #4 — Sampler divergence — ⚪ clean

map seats@50/50 = 0.4505 → ReCom percentile 51.6, SMC percentile 55.6, divergence -4.0pp (threshold 25pp)

```json
{
  "recom_percentile": 51.623069306930695,
  "smc_percentile": 55.612148830223276,
  "divergence_pp": -3.989079523292581,
  "threshold_pp": 25
}
```

---

Pre-registered tripwire thresholds:

- MO #1 drain ratio threshold: 1.5x population-justified
- MO #2 Polsby-Popper percentile threshold: bottom 10%
- MO #3 anchoring threshold: 70%
- MO #4 sampler divergence threshold: 25pp
