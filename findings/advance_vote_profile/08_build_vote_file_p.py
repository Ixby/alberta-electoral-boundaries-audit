"""Build the all-ballots voting-area file under rule P (exploratory, not registered).

The registered all-ballots file (Amendment 12, Part 1) is
  data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg
built by analysis/scripts/vote_anywhere_splat.py --primary: the election-day file
(va_polygons_with_2023_votes.gpkg, same rows and geometry) with va_ndp, va_ucp and va_other
replaced by all-ballots values placed under M0.

This script writes the same file under P:
  data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg
the election-day file with va_ndp, va_ucp and va_other replaced by election-day votes plus early
votes placed under P (_models.allocate_p, beta = 1.0, lam = 1). Same rows, same order, same
columns, same geometry, so any script that takes --va-file can read it.

Stops unless: every 2019 division's NDP, UCP and other totals equal the official totals in the
2023 workbook (to half a vote, as vote_anywhere_splat.py checks, and in fact to 1e-6); the province
totals equal the registered file's; rows and geometry match the election-day file.

Writes the gpkg and outputs/vote_file_p.json (size, SHA-256, checks).
Usage: python findings/advance_vote_profile/08_build_vote_file_p.py
"""
import os
import subprocess

import geopandas as gpd
import numpy as np
import pandas as pd

import _models as M
from _common import M0_SHA256, ROOT, VA_EDAY, VA_M0, VA_P, WORKBOOK_2023, build_va_table, division_totals, load_2023_rows, load_va, rel, sha256, write_json


def lfs(path):
    """Whether .gitattributes routes the path through Git LFS, and whether git lfs lists it as tracked."""
    r = subprocess.run(["git", "check-attr", "filter", "--", rel(path)], cwd=ROOT, capture_output=True, text=True).stdout
    listed = subprocess.run(["git", "lfs", "ls-files", "-n"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return {"lfs_pattern": r.strip().endswith(": lfs"), "lfs_tracked": rel(path) in listed}


def main():
    raw = load_2023_rows()
    g = load_va()
    t = build_va_table(g, raw)
    tot = division_totals(raw)
    a = M.allocate_p(t, tot, M.BETA_P)
    official = raw.groupby("ed")[["ndp", "ucp", "other"]].sum()
    got = pd.DataFrame({"ed": t.ed, "ndp": a["ndp"], "ucp": a["ucp"], "other": a["other"]}).groupby("ed").sum()
    err = float((got - official.loc[got.index]).abs().max().max())
    assert len(got) == 87 and err < 1e-6, err
    assert sha256(VA_M0) == M0_SHA256
    m0 = gpd.read_file(VA_M0)
    ed = gpd.read_file(VA_EDAY)
    assert (ed.OBJECTID.values == g.OBJECTID.values).all() and (m0.OBJECTID.values == ed.OBJECTID.values).all()
    prov = {c: float(a[c].sum()) for c in ("ndp", "ucp", "other")}
    prov_m0 = {c: float(m0[f"va_{c}"].sum()) for c in ("ndp", "ucp", "other")}
    assert all(abs(prov[c] - prov_m0[c]) < 1e-3 for c in prov), (prov, prov_m0)
    out = ed.copy()
    for c in ("ndp", "ucp", "other"):
        out[f"va_{c}"] = a[c]
    assert list(out.columns) == list(m0.columns)
    assert out.geometry.geom_equals_exact(m0.geometry, 0).all()
    VA_P.unlink(missing_ok=True)
    os.environ["OGR_CURRENT_DATE"] = "2023-05-29T00:00:00.000Z"  # fixed timestamp inside the GeoPackage, so a rebuild is byte-identical
    out.to_file(VA_P, driver="GPKG")
    back = gpd.read_file(VA_P)
    for c in ("ndp", "ucp", "other"):
        assert np.allclose(back[f"va_{c}"].values, a[c], rtol=0, atol=1e-9)
    by19 = back.groupby("parent_ed_2019")[["va_ndp", "va_ucp", "va_other"]].sum()
    moved = float(np.abs(back.va_ndp.values - m0.va_ndp.values).sum() + np.abs(back.va_ucp.values - m0.va_ucp.values).sum()) / 2
    res = {"file": rel(VA_P), "bytes": VA_P.stat().st_size, "sha256": sha256(VA_P), "rule": {"name": "P", "beta": M.BETA_P, "lam": M.LAM_P},
           "rows": int(len(back)), "columns": list(back.columns),
           "province_totals": {k: round(v, 3) for k, v in prov.items()},
           "checks": {"division_totals_equal_official_max_abs_votes": err, "divisions": 87,
                      "province_totals_equal_registered_file": True, "rows_and_geometry_equal_election_day_file": True,
                      "parent_ed_2019_groups": int(len(by19))},
           "two_party_votes_placed_differently_from_m0": round(moved, 1),
           "sibling": {"file": rel(VA_M0), "sha256": M0_SHA256, **lfs(VA_M0)},
           "git_lfs": lfs(VA_P)}
    write_json("vote_file_p.json", res, __file__, [WORKBOOK_2023, VA_EDAY, VA_M0])
    print(res)


if __name__ == "__main__":
    main()
