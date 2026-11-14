import geopandas as gpd, shapely, sys, numpy as np
f=sys.argv[1]
G=gpd.read_file(f); g=G.geometry.values; U=shapely.union_all(g)
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg"); prov=shapely.union_all(M.geometry.values)
holes=[shapely.Polygon(r) for p in shapely.get_parts(U) for r in p.interiors]
t=shapely.STRtree(g); ov=0; n=0
for i in range(len(g)):
    for j in t.query(g[i]):
        if j>i:
            a=g[i].intersection(g[j]).area
            if a>1e-6: ov+=a; n+=1
V=gpd.read_file("data/shapefiles/canonical/va_2023_election_day_votes.gpkg"); P=gpd.GeoDataFrame(V[["OBJECTID"]],geometry=V.representative_point(),crs=3400)
b=gpd.sjoin(P,gpd.read_file("data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg")[["district","geometry"]],predicate="within").groupby("OBJECTID").district.first()
a=gpd.sjoin(P,G[[G.columns[[c in ("district","EDName2025") for c in G.columns]][0],"geometry"]].rename(columns={"EDName2025":"district"}),predicate="within").groupby("OBJECTID").district.first()
print(f.split('/')[-1],"overlap m2",round(ov,4),"pairs",n,"holes",len(holes),round(sum(h.area for h in holes),4),"m2; gap vs province",round(prov.difference(U).area,4),"outside",round(U.difference(prov).area,4),"parts",sum(len(shapely.get_parts(x)) for x in g),"invalid",int((~shapely.is_valid(g)).sum()),"VAs moved",int((b!=a.reindex(b.index)).sum()),"unassigned",len(P)-len(a))
