# Evaluation-only: loads official geometry, filtered to the 22 tuning EDs IMMEDIATELY.
from pathlib import Path
import geopandas as gpd, pandas as pd
REPO = Path(__file__).resolve().parents[2]
TUNING=[3,5,7,9,12,15,16,17,19,20,21,23,24,25,29,30,32,37,38,43,65,88]
_P=str(REPO / "data/shapefiles/canonical") + "/"
def load():
    s=pd.read_csv(REPO / "data/iap/iap_app7_populations.csv")
    s=s[s.ed_number.isin(TUNING)]
    g=gpd.read_file(_P+"ea_majority_2026_eds.gpkg")
    g=g[g.EDName2025.isin(s.district)].copy()
    assert len(g)==22
    g=g.merge(s[['district','ed_number','area_km2']],left_on='EDName2025',right_on='district')
    return g.set_index('ed_number').sort_index()
