"""
v0_1_v8_overlap_diagnostic.py

Inspect every residual overlap pair in the v0_8 canonical GPKGs and print
them sorted by overlap area. Companion to v0_1_dpg_perfecter.py — the
perfecter only logs the first 3 overlaps; this gives the full ranked list
so we know which need refinement.

Outputs:
  data/v0_1_v8_overlap_pairs_<plan>.csv  (sorted by area DESC)
  Console table

Dependencies:
  Forward:  data/shapefiles/derived/v0_8_canonical_*_2026_eds.gpkg
  Backward: data/v0_1_v8_overlap_pairs_*.csv
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _perf_utils import Timer, ts  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
DERIVED = DATA / "shapefiles" / "derived"


def diagnose(plan: str) -> pd.DataFrame:
    src = DERIVED / f"v0_8_canonical_{plan}_2026_eds.gpkg"
    if not src.exists():
        print(f"  [skip] {src.name} not found")
        return pd.DataFrame()

    with Timer(f"[{plan}] diagnose") as t:
        g = gpd.read_file(src)
        name_col = "name_2026" if "name_2026" in g.columns else g.columns[0]
        geoms = g.geometry.values
        names = g[name_col].astype(str).values
        n = len(g)

        print(f"\n=== {plan} 2026 ===  ({n} EDs, CRS={g.crs})")
        sindex = g.sindex
        rows = []
        for i in range(n):
            candidates = list(sindex.intersection(geoms[i].bounds))
            for j in candidates:
                if j <= i:
                    continue
                try:
                    inter = geoms[i].intersection(geoms[j])
                except Exception:
                    continue
                a = inter.area
                if a > 1.0:  # square metres in EPSG:3401
                    rows.append(
                        {
                            "ed_a": names[i],
                            "ed_b": names[j],
                            "overlap_km2": a / 1e6,
                            "ed_a_km2": geoms[i].area / 1e6,
                            "ed_b_km2": geoms[j].area / 1e6,
                            "frac_of_smaller": a / min(geoms[i].area, geoms[j].area),
                        }
                    )

        if not rows:
            print("  no overlaps > 1 m²")
            t.note = f"{n} EDs, 0 overlap pairs"
            return pd.DataFrame()

        df = pd.DataFrame(rows).sort_values("overlap_km2", ascending=False)
        out = DATA / f"v0_1_v8_overlap_pairs_{plan}.csv"
        df.to_csv(out, index=False)
        print(f"  {len(df)} pairs with overlap > 1 m²")
        print(f"  total overlap area: {df['overlap_km2'].sum():.4f} km²")
        print(f"  largest 10:")
        for _, r in df.head(10).iterrows():
            print(
                f"    {r['overlap_km2']:>10.4f} km²  {r['ed_a']:<35s} ∩ {r['ed_b']:<35s}  "
                f"frac_of_smaller={r['frac_of_smaller']:.4f}"
            )
        print(f"  wrote {out.name}")
        t.note = (
            f"{n} EDs, {len(df)} overlap pairs, {df['overlap_km2'].sum():.2f} km² total"
        )
    return df


def main() -> int:
    with Timer("[v0_8 overlap diagnostic]"):
        for plan in ("majority", "minority"):
            diagnose(plan)
    return 0


if __name__ == "__main__":
    sys.exit(main())
