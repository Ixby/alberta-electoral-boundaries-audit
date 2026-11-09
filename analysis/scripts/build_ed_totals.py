# Per-ED vote totals for the map explorer's ED tooltip and the text explorer's
# district directory.
#
# Output: viewer/static/mapdata/ed_totals.json
#   { "minority": {ed_name: {"total": n, "anywhere": true}},
#     "majority": {...},
#     "2019":     {...} }
#
# Every total counts all 2023 ballots (Amendment 12's substrate,
# data/shapefiles/derived/va_polygons_with_all_2023_ballots.gpkg, columns
# va_{ucp,ndp,other}_all). Elections Alberta reports advance, mobile, special
# and Vote Anywhere ballots only by 2019 division; that file spreads them over
# each division's voting areas in proportion to the election-day votes each area
# cast, so 2019 division totals match the official results by design and the
# split across the new proposal districts is an estimate. anywhere=true on every
# row (the explorer then labels the figure as the district's total vote).
#
# The voting areas are assigned to districts by the explorer's own labels
# (valabels_<map>.json, parallel-indexed to va_props.json and to the gpkg rows;
# the script checks that alignment against the election-day votes).
import json, collections
from pathlib import Path
import pyogrio

REPO = Path(__file__).resolve().parents[2]
MAPDATA = REPO / "viewer" / "static" / "mapdata"
VA_ALL = REPO / "data" / "shapefiles" / "derived" / "va_polygons_with_all_2023_ballots.gpkg"
OFFICIAL_TOTAL_VALID = 1_764_915  # data/reference/alberta_2023_results.csv, total_valid_votes summed

va_props = json.loads((MAPDATA / "va_props.json").read_text(encoding="utf-8"))
va = pyogrio.read_dataframe(VA_ALL, read_geometry=False)
assert len(va) == len(va_props), (len(va), len(va_props))
eday = (va["va_ucp"] + va["va_ndp"] + va["va_other"]).round().astype(int)
bad = [i for i, p in enumerate(va_props) if abs(int(p.get("votes", 0)) - int(eday[i])) > 1]
assert not bad, f"va_props and {VA_ALL.name} rows are not aligned: {bad[:5]}"
all_ballots = (va["va_ucp_all"] + va["va_ndp_all"] + va["va_other_all"]).tolist()


def totals_by_ed(label_file: str) -> dict:
    labels = json.loads((MAPDATA / label_file).read_text(encoding="utf-8"))
    tot = collections.defaultdict(float)
    for i, ed in enumerate(labels):
        if ed:
            tot[ed] += all_ballots[i]
    return {n: {"total": int(round(v)), "anywhere": True} for n, v in tot.items()}


out = {k: totals_by_ed(f"valabels_{k}.json") for k in ("minority", "majority", "2019")}
for k, v in out.items():
    s = sum(r["total"] for r in v.values())
    assert abs(s - OFFICIAL_TOTAL_VALID) <= len(v), f"{k}: {s:,} against the official {OFFICIAL_TOTAL_VALID:,}"

(MAPDATA / "ed_totals.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print(f"[build_ed_totals] wrote ed_totals.json (all ballots) - "
      + ", ".join(f"{k} {len(v)} EDs, {sum(r['total'] for r in v.values()):,} votes" for k, v in out.items()))
