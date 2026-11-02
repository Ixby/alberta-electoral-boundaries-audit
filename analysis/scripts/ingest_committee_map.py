# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
ingest_committee_map.py
-----------------------

Step 0 of the November 2 runbook: take the published district file, check it,
and write the one file every later step reads.

The later steps do not all handle names the same way. run_structural_battery.py
has no --name-col; if a map has no EDName2025 column it silently takes the
first column as district names. This writes the map with its name column copied
to EDName2025, so every step reads the same names and no step needs --name-col.

Checks (a blocking failure exits 1 and names each problem; nothing is fixed
silently):
  - the file has a coordinate system;
  - the name column exists, and every name is present and unique;
  - every geometry is valid and non-empty;
  - districts overlapping by more than 0.1 km2;
  - every district receives at least one voting area (VA), and the share of
    the province's 2021 population left outside every district is under 0.5%
    (VAs are placed by representative point, as in score_x1.py and
    rules_check.py);
  - district count: 87, 89 or 91 have neutral-map sets; any other count is
    reported, so the size-matched step's error is expected, not a surprise.
Warnings (exit 0) are listed too.

Writes OUT (default data/shapefiles/lunty/lunty_2026_eds.gpkg) and
OUT.ingest.json: source path, URL, download time, SHA-256 of every source
file, the name column used, district names, and every check result.

Usage
  python analysis/scripts/ingest_committee_map.py --src PATH [--name-col COL]
         [--url URL] [--downloaded "2026-11-02 10:15 MST"] [--dissolve] [--out PATH]
  PATH may be .gpkg, .shp, .geojson, .kml or a .zip holding one of these.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import mcmc_ensemble as me  # noqa: E402
import s15_2_criteria as s152  # noqa: E402

SETS = {87, 89, 91}
OVERLAP_KM2, UNASSIGNED_MAX = 0.1, 0.005
NAME_GUESSES = ("EDName2025", "ED_NAME", "EDName", "ED_Name", "Name", "NAME", "name", "ENGLISH_NAME", "ED")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(src):
    p = Path(src)
    if p.suffix.lower() == ".zip":
        return gpd.read_file(f"zip://{p.resolve().as_posix()}"), [p]
    sidecars = [p] + ([q for q in p.parent.glob(p.stem + ".*") if q != p] if p.suffix.lower() == ".shp" else [])
    return gpd.read_file(p), sidecars


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--name-col")
    ap.add_argument("--url")
    ap.add_argument("--downloaded")
    ap.add_argument("--dissolve", action="store_true",
                    help="merge rows that share a district name into one (multi-part districts); reported in the log")
    ap.add_argument("--out", default=str(REPO / "data/shapefiles/lunty/lunty_2026_eds.gpkg"))
    a = ap.parse_args()

    g, files = read(a.src)
    block, warn = [], []
    col = a.name_col or next((c for c in NAME_GUESSES if c in g.columns), None)
    if col is None or col not in g.columns:
        sys.exit(f"name column not found; columns are {list(g.columns)}. Pass --name-col.")
    if a.dissolve:
        n0 = len(g)
        g = g.dissolve(by=col, as_index=False)
        warn.append(f"--dissolve: {n0} rows merged into {len(g)} districts by {col!r}")
    if not a.name_col:
        warn.append(f"name column guessed as {col!r}; columns are {list(g.columns)}")

    if g.crs is None:
        block.append("the file has no coordinate system")
    names = g[col]
    if names.isna().any() or (names.astype(str).str.strip() == "").any():
        block.append(f"{int(names.isna().sum() + (names.astype(str).str.strip() == '').sum())} district(s) without a name")
    dup = names[names.duplicated(keep=False)].astype(str).unique().tolist()
    if dup:
        block.append(f"duplicate names (several polygons per district? rerun with --dissolve): {dup}")
    bad = g[~g.geometry.is_valid | g.geometry.is_empty][col].astype(str).tolist()
    if bad:
        block.append(f"invalid or empty geometry: {bad}")
    k = names.nunique()
    if k not in SETS:
        warn.append(f"{k} districts: no size-matched neutral-map set exists for this count (only {sorted(SETS)}); "
                    "runbook step 3b will stop with an error by design. The 87-district canonical comparison still runs.")

    if g.crs is not None and not bad:
        w = g.to_crs(s152.WORK)
        sidx = w.sindex
        over = []
        for i, j in zip(*sidx.query(w.geometry, predicate="intersects")):
            if i < j:
                area = w.geometry.iloc[i].intersection(w.geometry.iloc[j]).area / 1e6
                if area > OVERLAP_KM2:
                    over.append(f"{w[col].iloc[i]} / {w[col].iloc[j]} ({area:.2f} km2)")
        if over:
            block.append(f"overlapping districts: {over}")

        va, graph = me.build_va_graph(verbose=False)
        nodes = sorted(graph.nodes())
        pop = pd.Series({n: graph.nodes[n]["pop_2021"] for n in nodes})
        pts = va.loc[nodes, ["geometry"]].to_crs(s152.WORK)
        pts["geometry"] = pts.geometry.representative_point()
        tmp = Path(a.out).with_suffix(".check.gpkg")
        w[[col, "geometry"]].to_file(tmp, driver="GPKG")
        lab = s152.assign(pts, tmp, col)
        tmp.unlink()
        share = float(pop[lab.to_numpy() == "__unassigned__"].sum() / pop.sum())
        empty = sorted(set(names.astype(str)) - set(lab.astype(str)))
        if empty:
            block.append(f"districts that receive no voting area: {empty}")
        msg = f"{100 * share:.2f}% of the 2021 population falls outside every district"
        if share > 0:
            (block if share >= UNASSIGNED_MAX else warn).append(msg)
        per = pop.groupby(lab.to_numpy()).sum().drop("__unassigned__", errors="ignore")
        dev = per / per.mean() - 1
        warn.append(f"overlay deviation range {100 * dev.min():+.1f}% ({dev.idxmin()}) to "
                    f"{100 * dev.max():+.1f}% ({dev.idxmax()}); the overlay is not the official count")

    out = Path(a.out)
    log = {"source": str(Path(a.src).resolve()), "url": a.url, "downloaded": a.downloaded,
           "source_sha256": {f.name: sha256(f) for f in files}, "name_col": col, "districts": int(k),
           "names": sorted(names.astype(str).tolist()), "crs": str(g.crs), "blocking": block, "warnings": warn}
    for w_ in warn:
        print("WARN   " + w_)
    for b in block:
        print("BLOCK  " + b)
    if block:
        print(f"NOT INGESTED: {len(block)} blocking problem(s); {out} not written")
        Path(str(out) + ".ingest.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
        sys.exit(1)
    g = g.copy()
    if col != "EDName2025":
        if "EDName2025" in g.columns:
            g = g.rename(columns={"EDName2025": "EDName2025_original"})
        g["EDName2025"] = g[col].astype(str)
    out.parent.mkdir(parents=True, exist_ok=True)
    g.to_file(out, driver="GPKG")
    log["out_sha256"] = sha256(out)
    Path(str(out) + ".ingest.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"INGESTED: {k} districts, names from {col!r} -> EDName2025; wrote {out} and {out}.ingest.json")


if __name__ == "__main__":
    main()
