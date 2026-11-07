import geopandas as gpd, numpy as np, shapely, time, json
t0=time.time()
C=gpd.read_file("C:/tmp/iap_v3_claims.gpkg").set_index("district")
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg").set_index("EDName2025")
known=[n for n in C.index if C.loc[n,"source"]=="known" and n!="Chestermere-Strathmore"]
prov=shapely.union_all(M.geometry.values)
geo={n:(M.loc[n].geometry if n in known else C.loc[n].geometry) for n in C.index}
lines=shapely.union_all([shapely.boundary(g) for g in geo.values()]+[shapely.boundary(prov)])
faces=np.array(list(shapely.get_parts(shapely.polygonize(shapely.get_parts(lines)))))
print("faces",len(faces),round(time.time()-t0),"s",flush=True)
names=list(geo); tree=shapely.STRtree(np.array([geo[n] for n in names]))
fa=shapely.area(faces)
inside_prov=shapely.area(shapely.intersection(faces,prov))>0.5*fa
owner=np.full(len(faces),-1)
kidx=[names.index(n) for n in known]
for fi in np.where(inside_prov)[0]:
    cand=tree.query(faces[fi],predicate="intersects")
    ov={c:shapely.intersection(geo[names[c]],faces[fi]).area for c in cand}
    ks=[c for c in ov if c in kidx and ov[c]>0.5*fa[fi]]
    if ks: owner[fi]=ks[0]; continue
    chg={c:a for c,a in ov.items() if c not in kidx}
    if chg and max(chg.values())>0.5*fa[fi]: owner[fi]=max(chg,key=chg.get)
print("unowned faces inside province:",int(((owner<0)&inside_prov).sum()),flush=True)
ftree=shapely.STRtree(faces)
def contact(fi,fj): return shapely.length(shapely.intersection(shapely.boundary(faces[fi]),shapely.boundary(faces[fj])))
for it in range(5):
    todo=np.where((owner<0)&inside_prov)[0]
    if not len(todo): break
    for fi in todo:
        nb=[j for j in ftree.query(faces[fi].buffer(0.01)) if j!=fi and owner[j]>=0]
        ch=[j for j in nb if owner[j] not in kidx] or nb
        if ch: owner[fi]=owner[max(ch,key=lambda j:contact(fi,j))]
out={}
for k,n in enumerate(names):
    fs=faces[owner==k]; out[n]=shapely.union_all(fs) if len(fs) else shapely.Polygon()
# sliver parts of changed districts -> changed neighbour by longest contact
V=gpd.read_file("data/shapefiles/canonical/va_2023_election_day_votes.gpkg"); P=V.representative_point().values
kept=[]
for n in names:
    if n in known: continue
    parts=sorted(shapely.get_parts(out[n]),key=lambda g:-g.area)
    for p in parts[1:]:
        if shapely.within(P,p).any(): kept.append((n,"VA",round(p.area,3))); continue
        nb=[m for m in names if m!=n and m not in known and shapely.length(shapely.intersection(shapely.boundary(out[m]),p.buffer(0.01)))>0]
        if nb:
            m=max(nb,key=lambda m:shapely.length(shapely.intersection(shapely.boundary(out[m]),p.buffer(0.01))))
            out[m]=shapely.union_all([out[m],p]); out[n]=shapely.difference(out[n],p)
        else: kept.append((n,"only official neighbours",round(p.area,3)))
R=C.copy(); R["geometry"]=[out[n] for n in C.index]; R=gpd.GeoDataFrame(R.reset_index(),geometry="geometry",crs=3400)
R.to_file("C:/tmp/iap_v3_final.gpkg",driver="GPKG")
print("kept secondary parts:",kept[:20],len(kept))
print("official districts identical (area diff m2):",max(abs(out[n].area-M.loc[n].geometry.area) for n in known), "sym diff max m2", max(shapely.symmetric_difference(out[n],M.loc[n].geometry).area for n in known))
print("done",round(time.time()-t0),"s")
# leftover uncovered province land (faces whose point fell on a line) -> touching changed district
U=shapely.union_all(list(out.values())); left=[p for p in shapely.get_parts(shapely.difference(prov,U)) if p.area>0]
unres=[]
for p in left:
    nb=[m for m in names if m not in known and shapely.distance(out[m],p)<0.01]
    if nb:
        m=max(nb,key=lambda m:shapely.length(shapely.intersection(shapely.boundary(out[m]),p.buffer(0.01))))
        out[m]=shapely.union_all([out[m],p])
    else: unres.append(round(p.area,4))
print("leftover pieces",len(left),"total m2",round(sum(p.area for p in left),4),"unresolved (official-only neighbours)",len(unres),sum(unres))
R=C.copy(); R["geometry"]=[out[n] for n in C.index]; R=gpd.GeoDataFrame(R.reset_index(),geometry="geometry",crs=3400)
R.to_file("C:/tmp/iap_v3_final.gpkg",driver="GPKG")
