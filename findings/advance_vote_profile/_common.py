"""Shared loaders and output helpers for findings/advance_vote_profile (exploratory, not registered).

Reads only. Large files may be LFS pointers in a worktree; set AVP_DATA_ROOT to
a checkout that holds the real files, or the loader walks up to find one.

Every output goes through write_json / write_csv, which add a `meta` block to
JSON (entry stamp in Alberta time, script, seed, inputs with SHA-256) and
refuse keys or headers that are not snake_case.
"""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_PROBE = "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
# Entry stamps name the model and effort that made the entry (author's rule,
# 2026-11-09). They come from the environment of the session that runs the
# script: set STAMP_MODEL (e.g. claude-opus-5-5) and STAMP_EFFORT (e.g. medium).
ALBERTA = __import__("datetime").timezone(__import__("datetime").timedelta(hours=-6), "UTC-6")


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
INPUTS = HERE / "inputs"  # tracked; files the results depend on
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)
INPUTS.mkdir(exist_ok=True)

WORKBOOK_2023 = DATA_ROOT / "data/raw/2023_results.xlsx"
WORKBOOK_2015 = DATA_ROOT / "data/raw/2015_results.xlsx"
VA_EDAY = DATA_ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
VA_M0 = DATA_ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
VA_P = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_p.gpkg"
VA_POP = DATA_ROOT / "data/va_pop_from_das.csv"
M0_SHA256 = "c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72"  # Amendment 12, Part 1


# ---------------------------------------------------------------- output helpers

def stamp():
    """Entry stamp: the system clock in Alberta time (UTC-6, fixed offset, so it
    does not depend on the platform's time-zone database), plus the model and
    effort of the session running the script. Never estimated, never defaulted."""
    import datetime
    model, effort = os.environ.get("STAMP_MODEL"), os.environ.get("STAMP_EFFORT")
    if not model or not effort:
        raise RuntimeError("set STAMP_MODEL and STAMP_EFFORT to the running session's model and effort")
    t = datetime.datetime.now(ALBERTA).strftime("%Y-%m-%d %H:%M")
    return f"{t} Alberta time · {model} · {effort}"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rel(path):
    path = Path(path).resolve()
    for base in (ROOT, DATA_ROOT):
        try:
            return str(path.relative_to(base.resolve()))
        except ValueError:
            pass
    return str(path)


_SNAKE = re.compile(r"^[a-z0-9_]+$")


def _check_keys(o, where="root"):
    if isinstance(o, dict):
        for k, v in o.items():
            if not isinstance(k, str) or not _SNAKE.match(k):
                raise ValueError(f"JSON key not snake_case at {where}: {k!r}")
            _check_keys(v, f"{where}.{k}")
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            _check_keys(v, f"{where}[{i}]")


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, float) and np.isnan(o):
        return None
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def meta(script, inputs, seed=None, extra=None):
    m = {"entry": stamp(), "script": rel(script), "status": "exploratory, not registered",
         "inputs": [{"path": rel(p), "sha256": sha256(p)} for p in inputs]}
    if seed is not None:
        m["seed"] = seed
    if extra:
        m.update(extra)
    return m


def write_json(name, payload, script, inputs, seed=None, extra=None):
    out = {"meta": meta(script, inputs, seed, extra), **payload}
    out = _clean(out)
    _check_keys(out)
    (OUT / name).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return OUT / name


def write_csv(df, name, index=False):
    df = df.reset_index() if index else df
    bad = [c for c in df.columns if not _SNAKE.match(str(c))]
    if bad:
        raise ValueError(f"{name}: headers not snake_case: {bad}")
    df.to_csv(OUT / name, index=False)
    return OUT / name


# ---------------------------------------------------------------- loaders

def load_2023_rows():
    """Every poll row of the 2023 workbook: one row per station or advance location.

    valid: valid ballots; total: total ballots cast (valid + declined + rejected), i.e. people who voted there;
    electors: "Names on List" (election-day stations only).
    """
    import openpyxl
    wb = openpyxl.load_workbook(WORKBOOK_2023, read_only=True, data_only=True)
    rows = []
    for sn in wb.sheetnames:
        it = list(wb[sn].iter_rows(values_only=True))
        hdr = [str(h).strip() if h else "" for h in it[0]]
        nl, vb, tb = hdr.index("Names on List"), hdr.index("Valid Ballots Cast"), hdr.index("Total Ballots Cast")
        cands = list(range(4, nl))
        party = [str(it[0][i]).split("\n")[-1].strip() for i in cands]
        for r in it[1:]:
            if r[2] is None:
                continue
            v = [r[i] or 0 for i in cands]
            ndp = sum(x for x, p in zip(v, party) if p == "NDP")
            ucp = sum(x for x, p in zip(v, party) if p == "UCP")
            rows.append(dict(ed=sn, letter=r[0], name=str(r[1]).strip(), type=r[2], vas=r[3], ndp=ndp, ucp=ucp,
                             other=sum(v) - ndp - ucp, valid=r[vb], total=r[tb], electors=r[nl]))
    raw = pd.DataFrame(rows)
    raw["kind"] = raw["type"]
    raw.loc[raw.name.str.contains("Vote Anywhere", case=False), "kind"] = "Vote Anywhere"
    return raw


def load_va(path=VA_EDAY):
    """VA polygons in the committed row order (election-day votes, equal split within a station)."""
    import geopandas as gpd
    g = gpd.read_file(path)
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

    e_n, e_u, e_o  election-day NDP / UCP / other votes (the audit's equal split of each station's count)
    electors       the station's "Names on List" split equally over its voting areas
    eday_total     the station's election-day total ballots cast, same split
    gap            electors minus election-day total ballots, same split (people on the list who did not
                   vote on election day). Negative where a station is already over 100% on election day.
    """
    g = load_va() if g is None else g
    raw = load_2023_rows() if raw is None else raw
    rows = []
    for r in raw[raw.kind == "Election Day"].itertuples():
        vs = [x.strip().zfill(3) for x in str(r.vas).split(",") if x.strip()]
        for x in vs:
            k = len(vs)
            rows.append((r.ed, x, r.ed + str(r.letter), k, r.electors / k, (r.electors - r.total) / k,
                         r.valid / k, r.total / k))
    st = pd.DataFrame(rows, columns=["ed", "v", "station", "n_vas", "electors", "gap", "eday_valid", "eday_total"])
    t = pd.DataFrame({"ed": g.ed.values, "v": g.v.values, "name": g.parent_ed_2019.values,
                      "e_n": g.va_ndp.values.astype(float), "e_u": g.va_ucp.values.astype(float),
                      "e_o": g.va_other.values.astype(float)})
    t = t.merge(st, on=["ed", "v"], how="left", validate="one_to_one")
    assert len(t) == len(g)
    return t


def division_totals(raw, kinds=("Advance", "Vote Anywhere", "Mobile", "Special Ballot")):
    """Non-election-day totals per division: ndp, ucp, other (valid) and total ballots cast."""
    non = raw[raw.kind.isin(kinds)]
    return non.groupby("ed")[["ndp", "ucp", "other", "valid", "total"]].sum()


def logit(p):
    p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def expit(x):
    return 1 / (1 + np.exp(-np.asarray(x, float)))
