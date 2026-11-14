# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Statistics Canada, National Road Network, Alberta, edition 17.0 (Open Government Licence - Canada)
"""Build data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg, the road reference of the Step B
reconstruction (versions 2 and 3).

Source: nrn_rrn_ab_GPKG.zip from Statistics Canada (SHA-256 0dfd3afc...acf9a), unzipped;
layer NRN_AB_17_0_ROADSEG of NRN_AB_17_0_GPKG_en.gpkg. Keeps ROADCLASS and RTNUMBER1 and
reprojects to EPSG:3400. Run with the pinned environment (findings/a9_stepb_v3_dev/environment.txt).

Usage: python analysis/scripts/build_nrn_extract.py PATH/TO/NRN_AB_17_0_GPKG_en.gpkg
"""
import sys
from pathlib import Path

import geopandas as gpd

OUT = Path(__file__).resolve().parents[2] / "data/reference/nrn/nrn_ab_17_0_roadseg_3400.gpkg"

if __name__ == "__main__":
    g = gpd.read_file(sys.argv[1], layer="NRN_AB_17_0_ROADSEG", columns=["ROADCLASS", "RTNUMBER1"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    g.to_crs(3400).to_file(OUT, driver="GPKG")
    print(len(g), OUT)
