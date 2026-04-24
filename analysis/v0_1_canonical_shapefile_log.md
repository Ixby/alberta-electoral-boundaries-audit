# Canonical shapefile build log
Date: 2026-04-23T19:22:04.027237


## Majority overlap pair resolution

  Resolving Airdrie-Cochrane -> ['Airdrie-West', 'Cochrane-Springbank']
    VAs: 82, target_ratio(A): 0.460
    sweep: best_score=0.0018, achieved_ratio=0.462, target=0.460, angle=75° pos=0.36
    road-snap: found road at 720 m, extended to crossing line (direction -134°)
    Sensitivity: {'n_in_envelope': 7, 'ratio_min': np.float64(0.43483301888313736), 'ratio_max': np.float64(0.4995500943350588), 'ratio_mean': np.float64(0.457932000433089)}

  Resolving Highwood -> ['High River-Vulcan-Siksika', 'Okotoks-Diamond Valley']
    VAs: 71, target_ratio(A): 0.491
    Using town-cluster approach
    High River-Vulcan-Siksika: 47 VAs, achieved_ratio=0.681
    Okotoks-Diamond Valley: 24 VAs, achieved_ratio=0.319
    sweep: best_score=0.0347, achieved_ratio=0.526, target=0.491, angle=112° pos=0.51
    Parametric sweep (validation): score=0.0347, ratio=0.526
    Sweep wins (score 0.0347 < cluster 0.1900); falling back to sweep
    sweep: best_score=0.0036, achieved_ratio=0.495, target=0.491, angle=165° pos=0.48
    road-snap: found road at 475 m, extended to crossing line (direction -144°)
    Sensitivity: {'n_in_envelope': 2, 'ratio_min': np.float64(0.449858454519103), 'ratio_max': np.float64(0.5257767120038849), 'ratio_mean': np.float64(0.48781758326149394)}

## Building majority canonical

## Building minority canonical

### Majority summary
  Total EDs: 89, null geometry: 0
  v7: 67
  2019-parent: 18
  sweep: 4
  tier A: 57
  tier C-2019-direct: 16
  tier C-v6-pixel-exact: 6
  tier C-null: 4
  tier C-sweep: 4
  tier C-2019-blend: 2

### Minority summary
  Total EDs: 89, null geometry: 0
  v7: 84
  2019-parent: 5
  tier A: 65
  tier unknown: 14
  tier C-v6-pixel-exact: 3
  tier C-2019-blend: 3
  tier B: 2
  tier C-2019-split: 1
  tier C-2019-direct: 1

## Overlap check (majority)
  Airdrie-West ∩ Cochrane-Springbank: 0.00 km²
  Airdrie-West ∩ High River-Vulcan-Siksika: 0.00 km²
  Airdrie-West ∩ Okotoks-Diamond Valley: 0.00 km²
  Cochrane-Springbank ∩ High River-Vulcan-Siksika: 0.00 km²
  Cochrane-Springbank ∩ Okotoks-Diamond Valley: 0.00 km²
  High River-Vulcan-Siksika ∩ Okotoks-Diamond Valley: 0.00 km²