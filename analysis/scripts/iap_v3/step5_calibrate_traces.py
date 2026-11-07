import geopandas as gpd, numpy as np, pandas as pd, shapely, os, pickle
R=gpd.read_file("C:/tmp/iap_v3_final.gpkg").set_index("ed")
M=gpd.read_file("data/shapefiles/canonical/ea_majority_2026_eds.gpkg"); M["k"]=M.EDName2025
prov=shapely.union_all(M.geometry.values); pb=shapely.boundary(prov)
app7=pd.read_csv("data/iap/iap_app7_populations.csv").set_index("ed_number")
def samp(line,step=50):
    pts=[]
    for part in shapely.get_parts(line):
        if part.length>1: pts+=list(shapely.line_interpolate_point(part,np.arange(0,part.length,step)))
    return np.array(pts)
cal=[];rows=[]
for ed in R.index:
    f=f"C:/tmp/a10reg/pages/ed{ed:02d}.gpkg"
    if not os.path.exists(f): continue
    pg=gpd.read_file(f).to_crs(3400).union_all()
    nm=app7.loc[ed,"district"]; src=R.loc[ed,"source"]
    pts=samp(shapely.difference(shapely.boundary(pg),pb.buffer(200)))
    if not len(pts): continue
    urban=R.loc[ed].geometry.area<300e6
    if src=="known":
        tru=M[M.k==nm].geometry
        if len(tru):
            d=shapely.distance(pts,shapely.boundary(tru.iloc[0])); cal.append(pd.DataFrame({"ed":ed,"urban":urban,"d":d}))
    else:
        d=shapely.distance(pts,shapely.boundary(R.loc[ed].geometry))
        rows.append(pd.DataFrame({"ed":ed,"district":nm,"src":src,"urban":urban,"d":d}))
cal=pd.concat(cal); ch=pd.concat(rows)
q=lambda s:pd.Series({"n":len(s),"p50":s.quantile(.5),"p90":s.quantile(.9),"p95":s.quantile(.95),"p99":s.quantile(.99),"max":s.max()}).round(1)
print("CALIBRATION: page trace vs official line, unchanged districts (", cal.ed.nunique(),"pages)");print(cal.groupby("urban").d.apply(q).unstack())
print("v3 line vs own page trace, placed districts");print(ch.groupby("urban").d.apply(q).unstack())
pickle.dump((cal,ch),open("C:/tmp/fit_samples.pkl","wb"))
