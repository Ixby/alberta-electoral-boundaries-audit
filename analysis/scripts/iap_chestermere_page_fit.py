# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
iap_chestermere_page_fit.py
---------------------------

Post-registration check (2026-11-05), unregistered. Chestermere-Strathmore (ED 57) was copied
from the majority map because its stated population equals the commission's, so the registered
run never placed its page. Its stated area (1,025 km2) is not the official 1,019.72 km2, so the
panel changed it.

This places the page's red outline (PDF p272) on the ground with the inset fit of a10_inset.py
(similarity transform, trimmed ICP), using the majority's Chestermere-Strathmore as the target
and 100 m sampling, then lists every piece over 0.1 km2 where the placed page differs from the
majority district and from the v2 map. The Version 4 pipeline cannot place this page ("no page
layer matches a reference").

Reads   evidence/legislature/iap_report_2026_hires.pdf (through a9_stepb_reconstruct_v2.extract_page)
        data/shapefiles/canonical/ea_majority_2026_eds.gpkg, va_2023_election_day_votes.gpkg
        data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg
Writes  findings/iap_reconstruction_check/chestermere_page_fit.json

Usage: python -W ignore analysis/scripts/iap_chestermere_page_fit.py
"""
import json
import sys
from pathlib import Path

import geopandas as gpd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a10_inset as I  # noqa: E402
import a9_stepb_reconstruct_v2 as R2  # noqa: E402

ROOT = HERE.parents[1]
MAJ = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
V2 = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg"
VAS = ROOT / "data/shapefiles/canonical/va_2023_election_day_votes.gpkg"
OUT = ROOT / "findings/iap_reconstruction_check/chestermere_page_fit.json"
NAME = "Chestermere-Strathmore"


def iou(a, b):
    return a.intersection(b).area / a.union(b).area


def pieces(geom, P, M, G):
    out = []
    for q in gpd.GeoSeries([geom], crs=3400).explode(index_parts=False):
        if q.area < 1e5:
            continue
        rp = q.representative_point()
        out.append({"km2": round(q.area / 1e6, 3), "mean_width_m": round(2 * q.area / q.length),
                    "bounds_km": [round(v / 1000, 1) for v in q.bounds],
                    "majority_holder": [n for n in M.index if M.loc[n].geometry.contains(rp)],
                    "v2_holder": [n for n in G.index if G[n].contains(rp)],
                    "va_points": int(P.within(q).sum())})
    return out


def main():
    M = gpd.read_file(MAJ).set_index("EDName2025")
    G = gpd.read_file(V2).set_index("district").geometry
    V = gpd.read_file(VAS)
    P = V.representative_point()
    poly = R2.V1._evenodd_polygon(R2.extract_page(57)[0])
    I.SAMPLE_M = 100.0
    f = I.fit(poly, M.loc[NAME].geometry, trim=0.85)
    page = I.to_ground(poly, f)
    maj, v2 = M.loc[NAME].geometry, G[NAME]
    out = {"fit": {"median_m": round(f["med_m"], 1), "p90_m": round(f["p90_m"]), "max_m": round(f["max_m"])},
           "area_km2": {"stated": 1025, "page": round(page.area / 1e6, 2), "majority": round(maj.area / 1e6, 2),
                        "v2": round(v2.area / 1e6, 2)},
           "iou": {"page_vs_majority": round(iou(page, maj), 5), "page_vs_v2": round(iou(page, v2), 5)},
           "page_not_majority": pieces(page.difference(maj), P, M, G),
           "majority_not_page": pieces(maj.difference(page), P, M, G),
           "page_not_v2": pieces(page.difference(v2), P, M, G),
           "v2_not_page": pieces(v2.difference(page), P, M, G)}
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
