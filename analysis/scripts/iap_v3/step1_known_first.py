import geopandas as gpd, numpy as np, pandas as pd, shapely, os, json
from shapely import STRtree
G=gpd.read_file("data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg").set_index("district")
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg").set_index("EDName2025")
V=gpd.read_file("data/shapefiles/canonical/va_2023_election_day_votes.gpkg"); P=gpd.GeoDataFrame(V[["OBJECTID"]],geometry=V.representative_point(),crs=3400)
prov=shapely.union_all(M.geometry.values)
known=[n for n in G.index if G.loc[n,"source"]=="known" and n!="Chestermere-Strathmore"]
geo=G.geometry.copy()
for n in known: geo[n]=M.loc[n].geometry
KU=shapely.union_all([geo[n] for n in known])
changed=[n for n in G.index if n not in known]
pages={}
for n in changed:
    f=f"C:/tmp/a10reg/pages/ed{int(G.loc[n,'ed']):02d}.gpkg"
    if os.path.exists(f) and G.loc[n,"source"]=="placed": pages[n]=gpd.read_file(f).to_crs(3400).union_all()
def poly(g):
    ps=[x for x in shapely.get_parts(g) if x.geom_type in ("Polygon","MultiPolygon")]
    return shapely.union_all(ps) if ps else shapely.Polygon()
log={"overlap_to":[], "holes_to":[], "slivers_to":[]}
# 1 known wins; clip to province
for n in changed: geo[n]=poly(geo[n].difference(KU).intersection(prov))
# 2 overlaps between changed districts
ch=list(changed)
for i,a in enumerate(ch):
    for b in ch[i+1:]:
        x=geo[a].intersection(geo[b])
        if x.area<0.01: continue
        sa=pages[a].intersection(x).area if a in pages else 0; sb=pages[b].intersection(x).area if b in pages else 0
        win,lose=(a,b) if sa>=sb else (b,a)
        geo[lose]=poly(geo[lose].difference(x)); log["overlap_to"].append([win,lose,round(x.area,1)])
def assign(piece,cands,key):
    best=max(cands,key=lambda n:geo[n].boundary.intersection(piece.buffer(0.5)).length)
    geo[best]=poly(geo[best].union(piece)); log[key].append([best,round(piece.area,1)])
# 3 holes / uncovered province land -> changed neighbour with longest contact
for it in range(3):
    U=shapely.union_all(list(geo.values)); miss=poly(prov.difference(U))
    ps=[p for p in shapely.get_parts(miss) if p.area>0.01]
    if not ps: break
    for p in ps:
        c=[n for n in changed if geo[n].distance(p)<0.5]
        if c: assign(p,c,"holes_to")
# 4 slivers: secondary parts with no VA point -> neighbour with longest contact
for n in changed:
    parts=sorted(shapely.get_parts(geo[n]),key=lambda g:-g.area)
    if len(parts)<2: continue
    keep=parts[0]
    for p in parts[1:]:
        if P.within(p).any(): keep=keep.union(p); log["slivers_to"].append([n,"KEPT (holds VA)",round(p.area,1)]); continue
        c=[m for m in G.index if m!=n and geo[m].distance(p)<0.5]
        if not c: keep=keep.union(p); continue
        best=max(c,key=lambda m:geo[m].boundary.intersection(p.buffer(0.5)).length)
        if best in known:  # never alter an official district: keep sliver in the changed district? give to a changed neighbour if any
            cc=[m for m in c if m not in known]
            if cc: best=max(cc,key=lambda m:geo[m].boundary.intersection(p.buffer(0.5)).length)
            else: keep=keep.union(p); log["slivers_to"].append([n,"KEPT (only official neighbours)",round(p.area,1)]); continue
        geo[best]=geo[best].union(p); log["slivers_to"].append([best,n,round(p.area,1)])
    geo[n]=keep
geo=geo.apply(lambda g:shapely.make_valid(g) if not g.is_valid else g)
v3=G.copy(); v3["geometry"]=geo; v3=gpd.GeoDataFrame(v3.reset_index(),geometry="geometry",crs=3400)
# checks
g=v3.geometry.values; U=shapely.union_all(g)
over=sum(g.area)-U.area; gap=prov.difference(U).area; extra=U.difference(prov).area
parts=int(sum(len(shapely.get_parts(x)) for x in g))
b=gpd.sjoin(P,gpd.read_file("data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg")[["district","geometry"]],predicate="within").groupby("OBJECTID").district.first()
a=gpd.sjoin(P,v3[["district","geometry"]],predicate="within").groupby("OBJECTID").district.first()
moved=int((b!=a.reindex(b.index)).sum()); unass=int(len(P)-len(a))
off=[n for n in known if not v3.set_index("district").loc[n].geometry.equals(M.loc[n].geometry)]
print(f"v3: overlap {over:.2f} m2, gap {gap:.2f} m2, outside province {extra:.2f} m2, parts {parts}, invalid {int((~shapely.is_valid(g)).sum())}, VAs moved {moved}, unassigned {unass}, official districts altered {off}")
print({k:len(v) for k,v in log.items()}, "kept slivers:",[r for r in log["slivers_to"] if "KEPT" in str(r[1])][:10])
print("overlap moves >1000 m2:",[r for r in log["overlap_to"] if r[2]>1000])
print("hole fills >1000 m2:",[r for r in log["holes_to"] if r[1]>1000])
if moved==0 and unass==0:
    v3.to_file("C:/tmp/iap_v3_candidate.gpkg",driver="GPKG"); json.dump(log,open("C:/tmp/iap_v3_log.json","w"),indent=0)
