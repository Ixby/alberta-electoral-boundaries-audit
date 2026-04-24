# Edmonton-Beaumont polygon + red-team validation log
Date: 2026-04-23T20:28:14.382964

Edmonton-Beaumont polygon generator + red-team validation
======================================================================
Loading canonical majority: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_canonical_majority_2026_eds.gpkg
Loading canonical minority: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_canonical_minority_2026_eds.gpkg

Existing Edmonton-Beaumont polygon:
  Tier: C-osm-construct
  Area: 807.2 km2
  Centroid (EPSG:3401): (104853, 5910596)
Loading Leduc-Beaumont VAs from VA polygon file...
  Leduc-Beaumont VAs: 60
  Leduc-Beaumont total Election-Day votes: 12,642
  Trying OSM query: 'Beaumont, Leduc County, Alberta, Canada'
  Query failed: Nominatim geocoder returned 0 results for query 'Beaumont, Leduc County, Alberta, Canada'.
  Trying OSM query: 'Beaumont, Alberta, Canada'
  City of Beaumont: 24.2 km2
  OSM Beaumont area: 24.2 km2
  Applying 2000m edge buffer for immediate suburbs...
  Final polygon area: 76.6 km2
  VAs inside Edmonton-Beaumont polygon: 21
  Captured votes: 4,621

Updating canonical majority shapefile...
  Replacing existing Edmonton-Beaumont polygon (was: C-osm-construct)

======================================================================
RED-TEAM VALIDATION
======================================================================

--- MAJORITY (89 EDs) ---
  [OK] ED count: 89
  [OK] No null geometries
  [OK] CRS: EPSG:3401
  [OK] Column 'name_2026' present
  [OK] Column 'canon_tier' present
  [OK] 'map' column: all rows = 'majority'
  [OK] No duplicate ED names
  Tier distribution:
    A                        :  57  [high]
    C-2019-direct            :  16  [lower]
    C-v6-pixel-exact         :   5  [medium]
    C-null                   :   4  [lower]
    C-sweep                  :   4  [medium]
    C-2019-blend             :   2  [lower]
    C-osm-construct          :   1  [lower]
  Area range: 10.6 – 109222.0 km2
  Checking pairwise overlaps (full NxN)...
  [WARN] 81 overlapping pairs found

--- MINORITY (89 EDs) ---
  [OK] ED count: 89
  [OK] No null geometries
  [OK] CRS: EPSG:3401
  [OK] Column 'name_2026' present
  [OK] Column 'canon_tier' present
  [OK] 'map' column: all rows = 'minority'
  [OK] No duplicate ED names
  Tier distribution:
    A                        :  65  [high]
    unknown                  :  14  [lower]
    C-v6-pixel-exact         :   3  [medium]
    C-2019-blend             :   3  [lower]
    B                        :   2  [high]
    C-2019-split             :   1  [lower]
    C-2019-direct            :   1  [lower]
  Area range: 12.2 – 104403.5 km2
  Checking pairwise overlaps (full NxN)...
  [WARN] 95 overlapping pairs found
  [NOTE] Edmonton-Beaumont exists in minority file too (check if correctly named)

  Crosswalk sanity check:
  [OK] Edmonton-Beaumont -> Leduc-Beaumont (correct)

======================================================================
VALIDATION SUMMARY: 0 error(s), 2 warning(s)
WARNINGS:
  [WARN] MAJORITY: 81 overlapping polygon pairs:
  Calgary-Acadia x Calgary-Confluence: 4.11 km2
  Calgary-Acadia x Calgary-East: 77.30 km2
  Calgary-Beddington x Calgary-Nose Creek: 15.91 km2
  Calgary-Bhullar-McCall x Calgary-Falconridge-Conrich: 62.83 km2
  Calgary-Bhullar-McCall x Calgary-Nose Creek: 0.10 km2
  Calgary-Bhullar-McCall x Airdrie-East: 2.48 km2
  Calgary-Bhullar-McCall x Chestermere-Strathmore: 2.89 km2
  Calgary-Bow x Calgary-Varsity: 14.98 km2
  Calgary-Bow x Cochrane-Springbank: 0.21 km2
  Calgary-Buffalo x Calgary-Confluence: 4.41 km2
  [WARN] MINORITY: 95 overlapping polygon pairs:
  Calgary-Airdrie x Calgary-Bow-Springbank: 23.76 km2
  Calgary-Airdrie x Calgary-Falconridge: 23.88 km2
  Calgary-Airdrie x Calgary-Foothills-Airdrie West: 70.65 km2
  Calgary-Airdrie x Calgary-Lougheed: 0.19 km2
  Calgary-Airdrie x Calgary-Nolan Hill-Cochrane: 264.11 km2
  Calgary-Airdrie x Olds-Three Hills-Didsbury: 197.43 km2
  Calgary-Beddington x Calgary-North East: 5.15 km2
  Calgary-Bow-Springbank x Calgary-North West-Bearspaw: 23.68 km2
  Calgary-Buffalo x Calgary-Cross: 0.01 km2
  Calgary-Cross x Calgary-East: 13.09 km2
======================================================================

Saving updated canonical files...
  Saved: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_canonical_majority_2026_eds.gpkg
  Saved: C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\data\v0_1_canonical_minority_2026_eds.gpkg
