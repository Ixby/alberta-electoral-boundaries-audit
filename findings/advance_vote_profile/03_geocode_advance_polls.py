"""Geocode the named 2023 advance-poll locations (exploratory, not registered).

Each 2023 division sheet lists its advance polls by place name with their own
counts. This looks each name up in OpenStreetMap Nominatim, restricted to the
bounding box of the division. Only public polling-place names are sent.
Results are cached in inputs/advance_poll_geocodes.csv; a rerun reuses them.

Usage: python findings/advance_vote_profile/03_geocode_advance_polls.py
"""
import json
import time
import urllib.parse
import urllib.request

import pandas as pd

from _common import INPUTS, load_2023_rows, load_va

OUTF = INPUTS / "advance_poll_geocodes.csv"
UA = "research-client/1.0"


def query(q, box):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        dict(q=q, format="json", limit=1, countrycodes="ca", viewbox=",".join(f"{x:.5f}" for x in box), bounded=1))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main():
    raw = load_2023_rows()
    adv = raw[(raw.kind == "Advance")].copy()
    g = load_va()
    b = g.dissolve("ed").to_crs(4326).bounds  # minx miny maxx maxy
    cols = ["ed", "name", "lat", "lon", "display", "query"]
    done = pd.read_csv(OUTF, dtype={"ed": str}) if OUTF.exists() else pd.DataFrame(columns=cols)
    seen = set(zip(done.ed, done.name))
    rows = done.to_dict("records")
    for r in adv.itertuples():
        if (r.ed, r.name) in seen:
            continue
        bb = b.loc[r.ed]
        box = (bb.minx - 0.02, bb.maxy + 0.02, bb.maxx + 0.02, bb.miny - 0.02)
        cands = [r.name]
        if " - " in r.name:  # "Returning Office - X" names the place after the dash
            cands.append(r.name.split(" - ", 1)[1])
        if "," in r.name:  # "A, B" lists two buildings
            cands.append(r.name.split(",")[0])
        hit, failed = None, False
        for q in cands:
            try:
                res = query(q, box)
            except Exception as e:  # rate limit or network trouble: do not cache, retry on the next run
                failed = True
                print("ERR", r.ed, q, e, flush=True)
                time.sleep(30)
                break
            time.sleep(1.5)
            if res:
                hit = (res[0]["lat"], res[0]["lon"], res[0]["display_name"], q)
                break
        if failed:
            continue
        rows.append(dict(ed=r.ed, name=r.name, lat=hit[0] if hit else None, lon=hit[1] if hit else None,
                         display=hit[2] if hit else None, query=hit[3] if hit else None))
        pd.DataFrame(rows, columns=cols).to_csv(OUTF, index=False)
    d = pd.DataFrame(rows, columns=cols)
    print(len(d), "advance locations;", d.lat.notna().sum(), "geocoded", flush=True)


if __name__ == "__main__":
    main()
