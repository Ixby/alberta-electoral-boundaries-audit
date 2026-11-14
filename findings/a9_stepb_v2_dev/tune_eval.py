# Usage: python findings/a9_stepb_v2_dev/tune_eval.py OUT.json ED [ED ...]
# v2 development evaluation: tuning districts (official geometry) and changed pages (no geometry).
import sys, json, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis/scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import geopandas as gpd, numpy as np
import a9_stepb_reconstruct_v2 as R2
from truth import load, TUNING
CHANGED=[1,4,22,28,33,40,42,45,46,48,49,52,53,54,58,60,61,62,63,67,68,69,71,72,73,74,76,79,80,81,84,85,87,90,91]
eds=[int(a) for a in sys.argv[2:]]; out=sys.argv[1]
T=load(); res={}
for n in eds:
    assert n not in R2.SAMPLE
    t0=time.time()
    try:
        g=R2.reconstruct(n); r={k:v for k,v in R2.last_info.items() if k in ("inlier30","area_ratio","wide_z","s","theta_deg","n_road_pts","n_muni_pts","n_candidates","runner_up_inlier30")}
        if n in TUNING:
            tr=T.loc[n].geometry; r.update(iou=g.intersection(tr).area/g.union(tr).area, haus_km=g.hausdorff_distance(tr)/1000)
    except Exception as e:
        r={"error":repr(e)[:200]}
    r["sec"]=round(time.time()-t0,1); res[n]=r; print(n, {k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()}, flush=True)
json.dump(res, open(out,"w"), indent=1)
