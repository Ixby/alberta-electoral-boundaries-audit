"""Shared loaders for findings/advance_vote_profile (exploratory, not registered).

Reads only. Large files may be LFS pointers in a worktree; set AVP_DATA_ROOT to
a checkout that holds the real files, or the loader walks up to find one.
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_PROBE = "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"


def _data_root():
    env = os.environ.get("AVP_DATA_ROOT")
    if env:
        return Path(env)
    for p in [ROOT, *ROOT.parents]:
        f = p / _PROBE
        if f.exists() and f.stat().st_size > 10_000:
            return p
    return ROOT


DATA_ROOT = _data_root()
CACHE = HERE / "cache"  # git-ignored; only re-downloadable federal files go here
INPUTS = HERE / "inputs"  # tracked; files the results depend on
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)
INPUTS.mkdir(exist_ok=True)


def load_2023_rows():
    """Every poll row of the 2023 workbook: one row per station or advance location."""
    import openpyxl
    wb = openpyxl.load_workbook(DATA_ROOT / "data/raw/2023_results.xlsx", read_only=True, data_only=True)
    rows = []
    for sn in wb.sheetnames:
        it = list(wb[sn].iter_rows(values_only=True))
        hdr = it[0]
        nl = [i for i, h in enumerate(hdr) if h and str(h).strip() == "Names on List"][0]
        vb = [i for i, h in enumerate(hdr) if h and str(h).strip() == "Valid Ballots Cast"][0]
        cands = list(range(4, nl))
        party = [str(hdr[i]).split("\n")[-1].strip() for i in cands]
        for r in it[1:]:
            if r[2] is None:
                continue
            v = [r[i] or 0 for i in cands]
            ndp = sum(x for x, p in zip(v, party) if p == "NDP")
            ucp = sum(x for x, p in zip(v, party) if p == "UCP")
            rows.append(dict(ed=sn, letter=r[0], name=str(r[1]).strip(), type=r[2], vas=r[3], ndp=ndp, ucp=ucp,
                             other=sum(v) - ndp - ucp, valid=r[vb], electors=r[nl]))
    raw = pd.DataFrame(rows)
    raw["kind"] = raw["type"]
    raw.loc[raw.name.str.contains("Vote Anywhere", case=False), "kind"] = "Vote Anywhere"
    return raw


def load_va():
    """VA polygons in the committed row order (election-day votes, equal split within a station)."""
    import geopandas as gpd
    g = gpd.read_file(DATA_ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg")
    g["ed"] = g.ED_NUM.astype(int).astype(str).str.zfill(2)
    g["v"] = g.VA_NUMBER.astype(int).astype(str).str.zfill(3)
    return g


def region_of(name):
    if name.startswith("Calgary-"):
        return "Calgary"
    if name.startswith("Edmonton-"):
        return "Edmonton"
    small = ("Lethbridge", "Red Deer", "Medicine Hat", "Grande Prairie", "Fort McMurray", "St. Albert",
             "Sherwood Park", "Airdrie", "Spruce Grove", "Leduc", "Strathcona", "Brooks-Medicine Hat",
             "Cypress-Medicine Hat", "Morinville-St. Albert", "Fort Saskatchewan")
    if name.startswith(small):
        return "Smaller cities and suburbs"
    return "Rural"


def build_va_table(g=None, raw=None):
    """One row per voting area, in the committed file's row order.

    e_n, e_u   election-day NDP / UCP votes (the audit's equal split of each station's count)
    electors   the station's "Names on List" split equally over its voting areas
    gap        electors minus election-day valid ballots, same split (people who did not vote on election day)
    """
    g = load_va() if g is None else g
    raw = load_2023_rows() if raw is None else raw
    rows = []
    for r in raw[raw.kind == "Election Day"].itertuples():
        vs = [x.strip().zfill(3) for x in str(r.vas).split(",") if x.strip()]
        for x in vs:
            rows.append((r.ed, x, r.ed + str(r.letter), len(vs), r.electors / len(vs), (r.electors - r.valid) / len(vs),
                         r.valid / len(vs), r.ndp, r.ucp))
    st = pd.DataFrame(rows, columns=["ed", "v", "station", "n_vas", "electors", "gap", "eday_valid", "st_ndp", "st_ucp"])
    t = pd.DataFrame({"ed": g.ed.values, "v": g.v.values, "name": g.parent_ed_2019.values,
                      "e_n": g.va_ndp.values.astype(float), "e_u": g.va_ucp.values.astype(float)})
    t = t.merge(st, on=["ed", "v"], how="left", validate="one_to_one")
    pop = pd.read_csv(DATA_ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx").pop_2021
    t["pop"] = t.index.map(pop).fillna(0.0)
    assert len(t) == len(g)
    return t


def division_totals(raw, kinds=("Advance", "Vote Anywhere", "Mobile", "Special Ballot")):
    non = raw[raw.kind.isin(kinds)]
    return non.groupby("ed")[["ndp", "ucp"]].sum()


def logit(p):
    p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def expit(x):
    return 1 / (1 + np.exp(-np.asarray(x, float)))
