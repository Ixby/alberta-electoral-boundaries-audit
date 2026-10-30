"""Check the s152_criteria predicates against the repo's own s.15(2) re-audit
(analysis/methodology/population_deviation_reaudit.md §3-4) for the real maps' s.15(2) EDs."""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(sys.argv[1])
sys.path[:0] = [str(REPO / "analysis/scripts"), str(REPO / "analysis/utils")]
import mcmc_ensemble as me  # noqa: E402
from s152_criteria import OUT, district_criteria  # noqa: E402

# expected per re-audit (P=True / F=False); None = re-audit gives no single call
EXPECT = {
    ("majority", "Central Peace-Notley"): dict(a_area=True, b_far=True, c_no_big_town=True, d_reserve_metis=True, e_border=True),
    ("majority", "Lesser Slave Lake"): dict(a_area=True, b_far=True, c_no_big_town=True, d_reserve_metis=True, e_border=False),
    ("majority", "Canmore-Banff"): dict(a_area=False, b_far=True, c_no_big_town=False, d_reserve_metis=True, e_border=True),
    ("minority", "Central Peace-Notley"): dict(a_area=True, b_far=True, c_no_big_town=True, d_reserve_metis=True, e_border=True),
    ("minority", "Lesser Slave Lake"): dict(a_area=True, b_far=True, c_no_big_town=True, d_reserve_metis=True, e_border=False),
    ("minority", "Rocky Mountain House-Banff Park"): dict(a_area=True, b_far=True, c_no_big_town=True, d_reserve_metis=True, e_border=True),
}
EXPECT_N = {("majority", "Lesser Slave Lake"): 4, ("minority", "Lesser Slave Lake"): 4}

df = pd.read_csv(OUT, index_col="node")
va, graph = me.build_va_graph(verbose=False)
nodes = sorted(graph.nodes())
pts = va.loc[nodes].copy(); pts["geometry"] = pts.geometry.representative_point()
total = sum(graph.nodes[n]["pop_2021"] for n in nodes)
bad = 0
for m in ("majority", "minority"):
    eds = gpd.read_file(REPO / f"data/shapefiles/canonical/ea_{m}_2026_eds.gpkg").to_crs(pts.crs)
    j = gpd.sjoin(pts[["geometry"]], eds[["EDName2025", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    avg = total / eds["EDName2025"].nunique()
    for (mm, name), exp in EXPECT.items():
        if mm != m:
            continue
        mask = (j["EDName2025"] == name).reindex(df.index).fillna(False)
        if not mask.any():
            print(f"{m:8s} {name}: NOT FOUND in map"); bad += 1; continue
        c = district_criteria(df, mask)
        pop = sum(graph.nodes[n]["pop_2021"] for n in df.index[mask])
        diffs = [k for k, v in exp.items() if v is not None and c[k] != v]
        if (m, name) in EXPECT_N and c["n_met"] != EXPECT_N[(m, name)]:
            diffs.append(f"n_met {c['n_met']}!={EXPECT_N[(m, name)]}")
        sub = df[mask]
        print(f"{m:8s} {name:34s} var {pop/avg-1:+.1%}  met {c['n_met']}/5  "
              f"area {sub['area_km2'].sum():,.0f} km2  road_min {sub['road_km'].min():.0f} km  "
              f"towns>8k [{';'.join(sorted(set(sub.loc[sub['big_town'], 'town_name'])))}]  "
              f"{'OK' if not diffs else 'MISMATCH ' + ','.join(diffs)}")
        bad += bool(diffs)
print("RESULT:", "ALL MATCH" if not bad else f"{bad} mismatch(es)")
