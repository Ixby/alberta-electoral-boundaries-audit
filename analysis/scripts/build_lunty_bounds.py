# Alberta Electoral Boundary Audit — Lunty-scaffold highlight bounds
#
# Builds viewer/static/mapdata/lunty_bounds.json: the APPROXIMATE region the
# commission chair (Justice Dallas Miller) named in his Addendum Recommendation 5
# (commission final report pp. 66-67) as where one of the two restored rural
# electoral divisions should go — "an electoral division mostly consisting of
# Clearwater County and western Mountain View County" with s.15(2) status.
#
# This is an APPROXIMATE highlight from county boundaries, NOT the chair's exact
# lines (the addendum gave constraints + a named area, not a drawn boundary). The
# second restored seat's bounds are not geographically specified in the addendum.
# Reprojected to EPSG:3401 and origin-shifted to the explorer's coordinate space.
import json
from pathlib import Path
import geopandas as gpd
from shapely.ops import unary_union

REPO = Path(__file__).resolve().parents[2]
meta = json.loads((REPO / "docs" / "data" / "map_meta.json").read_text())
ox, oy = meta["origin_x"], meta["origin_y"]

g = gpd.read_file(REPO / "data" / "shapefiles" / "reference" / "alberta_2021_csds.gpkg").to_crs(3401)
sel = g[g["CSDNAME"].isin(["Clearwater County", "Mountain View County"])]
geom = unary_union(list(sel.geometry)).simplify(150)


def rings(gm):
    polys = list(gm.geoms) if gm.geom_type == "MultiPolygon" else [gm]
    return [[[round(x - ox, 1), round(y - oy, 1)] for x, y in p.exterior.coords] for p in polys]


data = {
    "zones": [
        {
            "id": "lunty-rmh-clearwater",
            "name": "Clearwater + W. Mountain View County",
            "note": "Approximate — chair's Addendum Rec 5(d) restoration zone (s.15(2)); not exact lines.",
            "rings": rings(geom),
        }
    ]
}
out = REPO / "viewer" / "static" / "mapdata" / "lunty_bounds.json"
out.write_text(json.dumps(data))
print(f"Wrote {out}: {sum(len(r) for r in data['zones'][0]['rings'])} points")
