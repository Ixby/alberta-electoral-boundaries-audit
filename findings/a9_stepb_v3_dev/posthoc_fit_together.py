# Post-hoc (the sample is spent): would a "pieces must mate" check have caught the run's errors?
# For each placed sample reconstruction: share of its area overlapping (a) official geometry of the 22
# non-sample tuning districts, (b) other placed sample reconstructions.
import sys, json, os, numpy as np, geopandas as gpd, pandas as pd
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "analysis/scripts"))
os.environ["STEPB_V3_CALIBRATION_RUN"]="1"
import a9_stepb_reconstruct_v3 as V3, a7_stepb_calibrate as C
from shapely.geometry import Polygon
from shapely.ops import unary_union
V1=V3.V1
d=json.load(open(str(__import__("pathlib").Path(__file__).resolve().parents[2] / "findings/a9_stepb_calibration.json"),encoding="utf-8"))
app7=pd.read_csv(C.APP7).set_index("ed_number")
maj=gpd.read_file(C.MAJ).to_crs(3400); maj["key"]=maj.EDName2025.map(C.norm)
tun=maj[maj.key.isin({C.norm(app7.loc[n,"district"]) for n in V3.TUNING})]
tu=unary_union(list(tun.geometry))
rec={}
for r in d["districts"]:
    if "iou" not in r: continue
    v=d["v3_diagnostics"][str(r["ed"])]; p=v["p"]; c=np.array(v["c"])
    outline,*_=V3.R2.extract_page(r["ed"]); poly=V1._evenodd_polygon(outline)
    gs=[poly] if poly.geom_type=='Polygon' else list(poly.geoms)
    rec[r["ed"]]=(r,unary_union([Polygon(V1._apply(np.array(x.exterior.coords),p[0],p[1],p[2:],c),[V1._apply(np.array(h.coords),p[0],p[1],p[2:],c) for h in x.interiors]).buffer(0) for x in gs]))
for n,(r,g) in sorted(rec.items()):
    a=g.intersection(tu).area/g.area
    o=unary_union([h for m,(_,h) in rec.items() if m!=n]); b=g.intersection(o).area/g.area
    print(f"{n:3d} {r['district'][:28]:28s} IoU {r['iou']:.4f} | overlaps tuning districts {a:7.3%} | overlaps other reconstructions {b:7.3%}", flush=True)
