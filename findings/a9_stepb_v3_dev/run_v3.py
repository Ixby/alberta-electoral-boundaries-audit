# Usage: python findings/a9_stepb_v3_dev/run_v3.py OUT.json ED [ED ...]
# Development run of the repository's version 3 module (georeference only; acceptance rule reported, not applied).
import sys, json, time
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis/scripts"))
sys.path.insert(0, str(REPO / "findings/a9_stepb_v2_dev"))
import a9_stepb_reconstruct_v3 as V3, geopandas as gpd, numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
from truth import load, TUNING
T=load(); out=sys.argv[1]; R={}
for n in [int(a) for a in sys.argv[2:]]:
    assert n not in V3.SAMPLE
    t0=time.time()
    try:
        poly,p,c,i=V3.georeference(n); V1=V3.V1
        geoms=[poly] if poly.geom_type=='Polygon' else list(poly.geoms)
        g=unary_union([Polygon(V1._apply(np.array(x.exterior.coords),p[0],p[1],p[2:],c),[V1._apply(np.array(h.coords),p[0],p[1],p[2:],c) for h in x.interiors]).buffer(0) for x in geoms])
        gpd.GeoDataFrame({'ed':[n]},geometry=[g],crs=3400).to_file(Path(out).with_name(f'ed{n}.gpkg'))
        if n in TUNING:
            tr=T.loc[n].geometry; i.update(iou=g.intersection(tr).area/g.union(tr).area, haus_km=g.hausdorff_distance(tr)/1000)
    except Exception as e: i={"error":repr(e)[:300]}
    i['sec']=round(time.time()-t0,1); R[n]=i
    print(n,json.dumps(i,default=lambda v: round(float(v),3)),flush=True)
    json.dump(R,open(out,'w'),indent=1,default=float)
