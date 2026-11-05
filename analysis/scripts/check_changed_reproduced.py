# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
check_changed_reproduced.py
---------------------------

Pre-scoring check: does a map's geometry agree with the panel's own population table about which
districts it changed?

Amendment 7, Step A (findings/iap_unchanged_districts.md) splits the panel's 91 districts into 56
unchanged (name and stated population equal to a commission-majority district) and 35 changed. A map
being scored should agree:

  FAIL  a district Step A calls changed holds exactly the voting areas of a majority district, and the
        stated populations differ by at least MIN_PEOPLE (the change was not reproduced; the 2026-11-04
        Step C run found Edmonton-Meadows this way, 3,562 people, only after scoring)
  FAIL  a district Step A calls unchanged does not hold exactly its majority district's voting areas
  NOTE  a changed district whose stated difference is below MIN_PEOPLE and whose voting areas equal the
        majority's (Calgary-Acadia and Red Deer-South differ by 2 people; no voting area is that small)

Voting areas are assigned by representative point, the rule territory_null.territory() uses to decide
which districts are fixed. MIN_PEOPLE is half the mean voting-area population (4,888,723 / 4,765 / 2).

Exits 1 on any FAIL that a person has not acknowledged by name with --ack. An acknowledged FAIL is
still printed and written as a FAIL, marked acknowledged; the check never clears it itself.
Writes the full table to --out.

Usage: python -W ignore analysis/scripts/check_changed_reproduced.py --map GPKG [--name-col EDName2025] --out JSON
       [--ack DISTRICT ...]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
VA = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
MAJ = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
UNCHANGED = ROOT / "analysis/a8/unchanged_56.json"
STEP_A = ROOT / "findings/iap_unchanged_districts.md"
MIN_PEOPLE = 4_888_723 / 4_765 / 2


def norm(s):
    return s.replace("’", "'").strip()


def va_sets(va, gpkg, col):
    pts = va[["geometry"]].copy()
    pts["geometry"] = pts.geometry.representative_point()
    g = gpd.read_file(gpkg).to_crs(va.crs)
    j = gpd.sjoin(pts, g[[col, "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    if j[col].isna().any():
        sys.exit(f"{int(j[col].isna().sum())} voting areas fall outside every district of {gpkg}")
    sets = {}
    for oid, d in zip(va.OBJECTID, j[col]):
        sets.setdefault(norm(d), set()).add(int(oid))
    return {d: frozenset(v) for d, v in sets.items()}


def step_a_changed():
    """Changed districts and their stated difference from the same-name majority district (None if no such name)."""
    out = {}
    for line in STEP_A.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| \d+ \| ([^|]+) \| [\d,]+ \| [^|]+ \| (.+) \|$", line)
        if not m or "commission ED" not in m.group(2) and "not in the commission" not in m.group(2):
            continue
        d = re.search(r"difference (-?[\d,]+)", m.group(2))
        out[norm(m.group(1))] = int(d.group(1).replace(",", "")) if d else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--name-col", default="EDName2025")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ack", nargs="+", default=[])
    a = ap.parse_args()

    va = gpd.read_file(VA)
    maj = va_sets(va, MAJ, "EDName2025")
    new = va_sets(va, a.map, a.name_col)
    maj_by_set = {v: d for d, v in maj.items()}
    unchanged = {norm(n) for n in json.loads(UNCHANGED.read_text(encoding="utf-8"))["districts"]}
    changed = step_a_changed()
    assert len(unchanged) == 56 and len(changed) == 35, (len(unchanged), len(changed))
    missing = (unchanged | set(changed)) - set(new)
    if missing:
        sys.exit(f"districts in Step A but not in the map: {sorted(missing)}")

    rows, fails = [], 0
    for d in sorted(new):
        same_as = maj_by_set.get(new[d])
        if d in unchanged:
            ok = same_as == d
            status = "ok" if ok else "FAIL: Step A says unchanged; voting areas differ from the majority's"
        else:
            diff = changed.get(d)
            if same_as is None:
                status = "ok"
            elif diff is not None and abs(diff) < MIN_PEOPLE:
                status = f"NOTE: same voting areas as majority {same_as}; stated difference {diff} people"
            else:
                status = f"FAIL: Step A says changed (stated difference {diff}); voting areas equal majority {same_as}"
        acked = status.startswith("FAIL") and d in a.ack
        fails += status.startswith("FAIL") and not acked
        rows.append({"district": d, "step_a": "unchanged" if d in unchanged else "changed",
                     "same_vas_as_majority": same_as, "n_vas": len(new[d]), "status": status, "acknowledged": acked})
    bad_ack = sorted(set(a.ack) - {r["district"] for r in rows if r["acknowledged"]})
    if bad_ack:
        sys.exit(f"--ack names districts that do not fail: {bad_ack}")
    res = {"map": a.map, "min_people": round(MIN_PEOPLE, 1), "n_fail_unacknowledged": fails,
           "acknowledged": a.ack, "districts": rows}
    Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8", newline="\n")
    for r in rows:
        if r["status"] != "ok":
            print(f"{r['district']}: {r['status']}{' [acknowledged]' if r['acknowledged'] else ''}")
    n_ack = sum(r["acknowledged"] for r in rows)
    print(f"{'FAIL' if fails else 'PASS'}: {fails} unacknowledged and {n_ack} acknowledged of {len(rows)} districts "
          f"disagree with Step A; table in {a.out}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
