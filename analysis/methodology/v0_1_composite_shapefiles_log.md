# Composite shapefile build log
Date: 2026-04-23T17:03:44.632720

Builds best-available 89-ED GeoPackages from v7 + 2019 parent fallbacks.


=== Majority ===
  Total EDs: 89
  From v7 (primary): 67
  From v6 minority: 0
  From 2019 parent: 22
  Unresolvable: 0
  Calgary-Confluence: resolved from 2019 (2019 parent: Calgary-Buffalo (direct))
  Calgary-Nose Creek: resolved from 2019 (2019 parent: Calgary-Beddington (direct))
  Edmonton-Windermere: resolved from 2019 (2019 parent: Edmonton-South West (direct))
  Airdrie-East: resolved from 2019 (2019 parent: Airdrie-East (direct))
  Airdrie-West: resolved from 2019 (2019 parent: Airdrie-Cochrane (blend))
  Barrhead-Westlock-Athabasca: resolved from 2019 (2019 parent: Athabasca-Barrhead-Westlock (direct))
  Canmore-Banff: resolved from 2019 (2019 parent: Banff-Kananaskis (direct))
  Chestermere-Strathmore: resolved from 2019 (2019 parent: Chestermere-Strathmore (direct))
  Cochrane-Springbank: resolved from 2019 (2019 parent: Airdrie-Cochrane (blend))
  Cold Lake-Bonnyville-St. Paul: resolved from 2019 (2019 parent: Bonnyville-Cold Lake-St. Paul (direct))
  Fort McMurray-Lac La Biche: resolved from 2019 (2019 parent: Fort McMurray-Lac La Biche (direct))
  High River-Vulcan-Siksika: resolved from 2019 (2019 parent: Highwood (blend))
  Leduc-Devon: resolved from 2019 (2019 parent: Leduc-Beaumont (blend))
  Lethbridge-East: resolved from 2019 (2019 parent: Lethbridge-East (blend))
  Lethbridge-West: resolved from 2019 (2019 parent: Lethbridge-West (blend))
  Medicine Hat-Brooks: resolved from 2019 (2019 parent: Brooks-Medicine Hat (direct))
  Mountain View-Kneehill: resolved from 2019 (2019 parent: Olds-Didsbury-Three Hills (direct))
  Okotoks-Diamond Valley: resolved from 2019 (2019 parent: Highwood (blend))
  St. Albert-Sturgeon: resolved from 2019 (2019 parent: Morinville-St. Albert (blend))
  Stony Plain-Drayton Valley: resolved from 2019 (2019 parent: Drayton Valley-Devon (direct))
  Sylvan Lake-Innisfail: resolved from 2019 (2019 parent: Innisfail-Sylvan Lake (direct))
  Taber-Cardston: resolved from 2019 (2019 parent: Taber-Warner (direct))

--- Majority summary ---
  Null geometries remaining: 0
  v7: 67
  2019-parent: 22
  tier A: 57
  tier C-fallback-2019-direct: 14
  tier C-fallback-2019-blend: 8
  tier C-v6-pixel-exact: 6
  tier C-null: 4

Output: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_composite_majority_2026_eds.gpkg

=== Minority ===
  Total EDs: 89
  From v7 (primary): 84
  From v6 minority: 0
  From 2019 parent: 5
  Unresolvable: 0
  Calgary-Airdrie: resolved from 2019 (2019 parent: Airdrie-Cochrane (split))
  Calgary-McCall-Bhullar: resolved from 2019 (2019 parent: Calgary-McCall (direct))
  Calgary-North West-Bearspaw: resolved from 2019 (2019 parent: Calgary-North West (blend))
  Calgary-West-Tsuut'ina: resolved from 2019 (2019 parent: Calgary-West (blend))
  St. Albert-Sturgeon: resolved from 2019 (2019 parent: Morinville-St. Albert (blend))

--- Minority summary ---
  Null geometries remaining: 0
  v7: 84
  2019-parent: 5
  tier A: 65
  tier : 14
  tier C-v6-pixel-exact: 3
  tier C-fallback-2019-blend: 3
  tier B: 2
  tier C-fallback-2019-split: 1
  tier C-fallback-2019-direct: 1

Output: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_composite_minority_2026_eds.gpkg