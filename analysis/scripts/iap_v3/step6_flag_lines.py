import geopandas as gpd, numpy as np, pandas as pd, shapely, os, pickle
cal,_=pickle.load(open("C:/tmp/fit_samples.pkl","rb"))
good=cal[~cal.ed.isin([86,82])]
for u,g in good.groupby("urban"): print("calibration good pages urban" if u else "calibration good pages rural",{p:round(g.d.quantile(p),1) for p in (.5,.95,.99,.999)},"max",round(g.d.max(),1))
BAR=round(good.d.quantile(.999),1); print("BAR (calibration p99.9) =",BAR,"m")
R=gpd.read_file("C:/tmp/iap_v3_final.gpkg").set_index("district")
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg").set_index("EDName2025")
V=gpd.read_file("data/shapefiles/canonical/va_2023_election_day_votes.gpkg"); V["votes"]=V.va_ndp+V.va_ucp+V.va_other
P=gpd.GeoDataFrame(V[["votes"]],geometry=V.representative_point(),crs=3400)
known=[n for n in R.index if R.loc[n,"source"]=="known" and n!="Chestermere-Strathmore"]
pages={n:gpd.read_file(f"C:/tmp/a10reg/pages/ed{int(R.loc[n,'ed']):02d}.gpkg").to_crs(3400).union_all() for n in R.index if R.loc[n,"source"]=="placed"}
# add the Chestermere page fit
pages["Chestermere-Strathmore"]=gpd.read_file("C:/tmp/a10test/ed57_page_fit.gpkg").union_all()
prov=shapely.boundary(shapely.union_all(M.geometry.values))
tree=shapely.STRtree(R.geometry.values); names=list(R.index); rows=[]
for i,a in enumerate(names):
    for j in tree.query(R.loc[a].geometry.buffer(1)):
        b=names[j]
        if j<=i: continue
        if a in known and b in known: continue
        ln=shapely.intersection(shapely.boundary(R.loc[a].geometry),R.loc[b].geometry.buffer(0.01))
        ln=shapely.line_merge(shapely.union_all([x for x in shapely.get_parts(ln) if x.geom_type in("LineString","MultiLineString")])) if not ln.is_empty else ln
        if ln.is_empty or ln.length<50: continue
        pts=np.array([p for part in shapely.get_parts(ln) if part.length>1 for p in shapely.line_interpolate_point(part,np.arange(0,part.length,25))])
        refs=[]
        for n in (a,b):
            if n in known: refs.append(shapely.boundary(M.loc[n].geometry))
            elif n in pages: refs.append(shapely.boundary(pages[n]))
        if not refs: rows.append({"a":a,"b":b,"km":ln.length/1e3,"unsupported_km":np.nan,"note":"no reference"}); continue
        d=np.minimum.reduce([shapely.distance(pts,r) for r in refs])
        bad=d>BAR
        band=shapely.union_all([shapely.buffer(pt,float(dd)) for pt,dd in zip(pts[bad],d[bad])]) if bad.any() else None
        vin=P[P.within(band)] if band is not None else P.iloc[:0]
        rows.append({"a":a,"b":b,"km":round(ln.length/1e3,2),"refs":len(refs),"unsupported_km":round(bad.sum()*0.025,2),"max_m":round(d.max(),1),"VAs_in_band":len(vin),"votes_in_band":round(vin.votes.sum())})
D=pd.DataFrame(rows); D.to_csv("C:/tmp/line_flags_final.csv",index=False)
pd.set_option("display.width",220)
print("lines checked",len(D),"total km",round(D.km.sum()),"; lines with unsupported stretches",(D.unsupported_km>0).sum(),"; unsupported km",round(D.unsupported_km.sum(),1))
print(D[D.unsupported_km>0].sort_values("votes_in_band",ascending=False).to_string(index=False))
print(D[D.note.notna()] if "note" in D else "")
