# Aboriginal Lands of Canada Legislative Boundaries (Alberta) — provenance

- Publisher: Natural Resources Canada, Canada Lands Survey System (CLSS), "Aboriginal Lands of Canada
  Legislative Boundaries", https://open.canada.ca/data/en/dataset/522b07b9-78e2-4819-b736-ad9208eb1067
  (Open Government Licence – Canada).
- Retrieved 2026-10-30T02:39Z from the ArcGIS REST layer
  https://proxyinternet.nrcan-rncan.gc.ca/arcgis/rest/services/CLSS-SATC/CLSS_Administrative_Boundaries/MapServer/0/query
  (envelope -120.1,48.9,-109.9,60.1 EPSG:4326, outFields=*, outSR=4326, f=geojson, two pages of 500; 577 features),
  then filtered to jurisdictionEng == "Alberta" → 152 polygons.
- File: aboriginal_lands_alberta.geojson, SHA-256 f87795a16204bdc88d465b31cae6c7727417146c6b95eb63f51d1a683d89b8d0.
  layer_meta.json = the layer's ?f=pjson description at retrieval.
- Caveat: copies of this national layer carry the note that it "is not to be used for defining boundaries";
  used here only to test whether a division contains a reserve (EBCA s.15(2)(d)).
- Approved: owner "i agree with cloud" (2026-10-29 ~21:05 MT), the Audit session having proposed this fetch.
- Why: the 2021 CSD layer lists 86 reserve/settlement CSDs (IRI, S-É); uninhabited reserves can be missing
  from it, which would make (d) stricter than the statute.
