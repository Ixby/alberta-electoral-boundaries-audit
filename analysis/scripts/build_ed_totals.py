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
# The voting areas are assigned to the 2026 districts by the explorer's own
# labels (valabels_<map>.json, parallel-indexed to va_props.json and to the gpkg
# rows; the script checks that alignment against the election-day votes). For
# the 2019 map the division comes from the gpkg's ED_NAME, written with the
# explorer's spelling of each name: three voting areas (Maskwacis-Wetaskiwin
# 004, Fort McMurray-Lac La Biche 023, Calgary-Buffalo 008) carry a
# neighbouring division's label in valabels_2019.json, which moved 142 to 312
# votes between three pairs of divisions. With ED_NAME every 2019 total equals
# the official result, and the script checks that.
#
# Rounding: each map's district totals are rounded by largest remainder, so
# they sum exactly to the province total (1,764,915), not just within one vote
# per district.
import csv, json, collections, math
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


def largest_remainder(tot: dict) -> dict:
    """Round {name: float} to integers that sum to round(sum of the floats)."""
    target = int(round(sum(tot.values())))
    floors = {n: math.floor(v) for n, v in tot.items()}
    short = target - sum(floors.values())
    for n in sorted(tot, key=lambda n: tot[n] - floors[n], reverse=True)[:short]:
        floors[n] += 1
    return floors


def labels_for(map_key: str) -> list:
    labels = json.loads((MAPDATA / f"valabels_{map_key}.json").read_text(encoding="utf-8"))
    if map_key != "2019":
        return labels
    # 2019: the division each VA belongs to (ED_NAME), in the explorer's spelling
    # (the majority label among that division's VAs).
    spelling = collections.defaultdict(collections.Counter)
    for i, ed in enumerate(va["ED_NAME"]):
        if labels[i]:
            spelling[ed][labels[i]] += 1
    name = {ed: c.most_common(1)[0][0] for ed, c in spelling.items()}
    assert len(set(name.values())) == len(name) == 87, "2019 division names do not map one-to-one"
    return [name[ed] for ed in va["ED_NAME"]]


def totals_by_ed(map_key: str) -> dict:
    labels = labels_for(map_key)
    tot = collections.defaultdict(float)
    for i, ed in enumerate(labels):
        if ed:
            tot[ed] += all_ballots[i]
    return {n: {"total": t, "anywhere": True} for n, t in largest_remainder(tot).items()}


out = {k: totals_by_ed(k) for k in ("minority", "majority", "2019")}
for k, v in out.items():
    s = sum(r["total"] for r in v.values())
    assert s == OFFICIAL_TOTAL_VALID, f"{k}: {s:,} against the official {OFFICIAL_TOTAL_VALID:,}"

# 2019: every division equals its official total (the McCall division is
# spelled Calgary-Bhullar-McCall in the results file).
with open(REPO / "data" / "reference" / "alberta_2023_results.csv", encoding="utf-8") as fh:
    official = {r["ed_name"]: int(r["total_valid_votes"]) for r in csv.DictReader(fh)}
official.setdefault("Calgary-McCall", official.get("Calgary-Bhullar-McCall"))
off_2019 = {n: r["total"] - official.get(n, -10**9) for n, r in out["2019"].items()}
assert all(abs(d) <= 1 for d in off_2019.values()), {n: d for n, d in off_2019.items() if abs(d) > 1}

(MAPDATA / "ed_totals.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print(f"[build_ed_totals] wrote ed_totals.json (all ballots) - "
      + ", ".join(f"{k} {len(v)} EDs, {sum(r['total'] for r in v.values()):,} votes" for k, v in out.items()))
