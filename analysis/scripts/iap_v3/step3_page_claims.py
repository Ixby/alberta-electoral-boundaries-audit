import geopandas as gpd, numpy as np, shapely, json
BAR=30.7
R=gpd.read_file("C:/tmp/iap_v3_rebuilt.gpkg").set_index("district")
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg").set_index("EDName2025")
V=gpd.read_file("data/shapefiles/canonical/va_2023_election_day_votes.gpkg"); P=V.representative_point().values
known=[n for n in R.index if R.loc[n,"source"]=="known" and n!="Chestermere-Strathmore"]
pages={n:gpd.read_file(f"C:/tmp/a10reg/pages/ed{int(R.loc[n,'ed']):02d}.gpkg").to_crs(3400).union_all() for n in R.index if R.loc[n,"source"]=="placed"}
pages["Chestermere-Strathmore"]=gpd.read_file("C:/tmp/a10test/ed57_page_fit.gpkg").union_all()
geo=R.geometry.copy(); moves=[]
names=[n for n in pages]
for a in R.index:
    if a in known: continue
    for b in names:
        if b==a: continue
        x=geo[a].intersection(pages[b])
        if a in pages: x=x.difference(pages[a])
        x=x.difference(shapely.union_all([M.loc[k].geometry for k in known if M.loc[k].geometry.intersects(x)])) if not x.is_empty else x
        for q in shapely.get_parts(x):
            if q.geom_type!="Polygon" or q.area<100: continue
            if q.buffer(-BAR/2).is_empty: continue   # thinner than the calibrated trace error: leave the snapped line
            if not geo[b].distance(q)<0.5: continue
            nva=int(shapely.within(P,q).sum())
            moves.append({"from":a,"to":b,"m2":round(q.area),"VA_points":nva,"at":[round(c) for c in q.centroid.coords[0]]})
            if nva==0:
                geo[a]=geo[a].difference(q); geo[b]=geo[b].union(q)
print(json.dumps(moves,indent=0))
R2=R.copy(); R2["geometry"]=geo; gpd.GeoDataFrame(R2.reset_index(),geometry="geometry",crs=3400).to_file("C:/tmp/iap_v3_claims.gpkg",driver="GPKG")
