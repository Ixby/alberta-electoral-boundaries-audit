# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
rules_check.py
--------------

Descriptive check of a district map against the EBCA population rules:
s.15(1) (within 25% of the average) and s.15(2) (up to 4 divisions as much
as 50% below the average, each meeting at least 3 of criteria (a)-(e)).

SUPPLEMENTARY. Not a registered November test (those are in
preregistration/november_2026_scoring_spec.md and Amendment 5, Parts 13-17). It
reports what the map does against the Act's numbers; it gives no verdict.
The Act's s.15 rules are addressed to the Commission; whether they bind a
legislative committee depends on the motion that created it.

Population basis. Deviations use the VA-level 2021 census overlay the
ensembles use (graph attribute pop_2021), with VAs attributed by
representative point, as in score_x1.py and s15_2_criteria.py. That overlay
is not the official count a commission or committee publishes. If the map's
own stated populations are given (--stated), both deviations are reported
and a district is listed as outside a band only when both put it there;
on the overlay alone it is listed as "overlay only".

Criteria. (a)-(e) are scored with s15_2_criteria.criteria() on the per-VA
table given by --table (default data/outputs/s15_2_va_criteria.csv). The
table in force for set D is the Amendment 5, Part 15 table, SHA-256 48c928b8...2fafc;
any other table is reported as such.

Usage
  python analysis/scripts/rules_check.py --map PATH [--name-col COL]
  python analysis/scripts/rules_check.py --assignment CSV  (columns: node, district)
         [--table CSV] [--stated CSV (columns: district, population)]
         [--label NAME] [--out results.json]
"""
import argparse
import difflib
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

A23_SHA = "48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc"
BAND, LOW, CAP, MIN_CRITERIA = 0.25, 0.50, 4, 3


def reserve_areas():
    """Total area (km2) of each reserve and Metis settlement, as s15_2_criteria.reserves() computes it."""
    r = gpd.read_file(s152.RESERVES).to_crs(s152.WORK)
    r = r[r["distributionType"] == "IR"][["adminAreaNameEng", "geometry"]].rename(columns={"adminAreaNameEng": "name"})
    m = gpd.read_file(s152.METIS).to_crs(s152.WORK)[["METIS_NAME", "geometry"]].rename(columns={"METIS_NAME": "name"})
    m["name"] = m["name"] + " (Metis settlement)"
    r = pd.concat([r, m], ignore_index=True).dissolve(by="name").reset_index()
    return (r.set_index("name").geometry.area / 1e6).to_dict()


def load_table(path, nodes, pop):
    tab = pd.read_csv(path, index_col="node", keep_default_na=False).loc[nodes]
    tab["pop"] = pop.to_numpy()
    for col in ("road_km", "area_km2", "border_km"):
        tab[col] = tab[col].astype(float)
    tab["reserves"] = [json.loads(r) if r else None for r in tab["reserves"]]
    return tab


def labels_for(va, nodes, a):
    if a.assignment:
        asg = pd.read_csv(a.assignment, dtype={"district": str}).set_index("node")["district"]
        return asg.reindex(nodes).fillna("__unassigned__").to_numpy()
    pts = va.loc[nodes, ["geometry"]].to_crs(s152.WORK)
    pts["geometry"] = pts.geometry.representative_point()
    return s152.assign(pts, a.map, a.name_col).to_numpy()


def _norm(name):
    return "".join(ch for ch in str(name).casefold() if ch.isalnum())


def match_names(stated, districts):
    """Map each stated name to a map district: exact, then ignoring case/punctuation/spaces,
    then a close spelling (difflib >= 0.9). Every non-exact match is reported for a human to check."""
    norm = {_norm(d): d for d in districts}
    out, notes, unmatched = {}, [], []
    for n in stated.index:
        if n in districts:
            out[n] = n
        elif _norm(n) in norm:
            out[n] = norm[_norm(n)]
            notes.append(f"{n} -> {out[n]}")
        else:
            close = difflib.get_close_matches(_norm(n), list(norm), n=1, cutoff=0.9)
            if close:
                out[n] = norm[close[0]]
                notes.append(f"{n} -> {out[n]} (close spelling)")
            else:
                unmatched.append(n)
    return out, notes, unmatched


def check(labels, tab, res_area, stated=None):
    crit = s152.criteria(tab, labels, None, res_area)
    unassigned = crit.pop("__unassigned__", None)
    k = len(crit)
    avg = sum(v["pop"] for v in crit.values()) / k
    st_dev, notes, unmatched = {}, [], []
    if stated is not None:
        names, notes, unmatched = match_names(stated, list(crit))
        st_avg = float(stated.sum()) / len(stated)  # the map's own average: its total over its district count
        st_dev = {names[n]: float(p) / st_avg - 1 for n, p in stated.items() if n in names}
    rows = []
    for d, v in crit.items():
        dev = v["pop"] / avg - 1
        sdev = st_dev.get(d)
        def band(x):
            if x is None:
                return None
            return "above +25%" if x > BAND else "below -50%" if x < -LOW else "below -25%" if x < -BAND else "within"
        b_ov, b_st = band(dev), band(sdev)
        rows.append({"district": d, "pop_overlay": round(v["pop"]), "dev_overlay_pct": round(100 * dev, 1),
                     "dev_stated_pct": None if sdev is None else round(100 * sdev, 1),
                     "band_overlay": b_ov, "band_stated": b_st,
                     "basis": "both" if b_st is not None else "overlay only",
                     **{c: v[c] for c in "abcde"}, "criteria_met": v["n"],
                     "area_km2": v["area_km2"], "road_km": v["road_km"], "border_km": v["border_km"],
                     "towns_over_8000": v["towns_over_8000"], "reserves_held": v["reserves_held"]})
    df = pd.DataFrame(rows).sort_values("dev_overlay_pct").reset_index(drop=True)

    def side(x):
        return x if x in ("above +25%", "below -25%", "below -50%") else None

    # outside a band only when both bases agree; where they disagree, listed separately
    df["band"] = [b_o if b_s is None else (b_o if side(b_o) == side(b_s) else "bases disagree")
                  for b_o, b_s in zip(df.band_overlay, df.band_stated)]
    low = df[df.band.isin(["below -25%", "below -50%"])]
    disagree = df[df.band == "bases disagree"]
    summary = {
        "districts": k, "average_pop_overlay": round(avg), "stated_populations": bool(st_dev),
        "stated_name_matches_not_exact": notes, "stated_names_unmatched": unmatched,
        "map_districts_without_stated": [d for d in crit if st_dev and d not in st_dev],
        "unassigned_pop_overlay": round(unassigned["pop"]) if unassigned else 0,
        "above_plus25": df[df.band == "above +25%"].district.tolist(),
        "below_minus50": df[df.band == "below -50%"].district.tolist(),
        "below_minus25": [{"district": r.district, "dev_overlay_pct": r.dev_overlay_pct,
                           "dev_stated_pct": r.dev_stated_pct, "basis": r.basis, "criteria_met": r.criteria_met,
                           "criteria": "".join(c for c in "abcde" if getattr(r, c)),
                           "meets_3_of_5": bool(r.criteria_met >= MIN_CRITERIA)} for r in low.itertuples()],
        "below_minus25_count": len(low), "s15_2_cap": CAP,
        "over_cap": len(low) > CAP,
        "below_minus25_without_3_criteria": low[low.criteria_met < MIN_CRITERIA].district.tolist(),
        "bases_disagree": [{"district": r.district, "dev_overlay_pct": r.dev_overlay_pct,
                            "dev_stated_pct": r.dev_stated_pct} for r in disagree.itertuples()],
        "dev_range_overlay_pct": [float(df.dev_overlay_pct.min()), float(df.dev_overlay_pct.max())],
        "dev_range_stated_pct": ([float(df.dev_stated_pct.min()), float(df.dev_stated_pct.max())]
                                 if st_dev else None),
    }
    return summary, df


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--map", help="district polygons (.gpkg/.shp)")
    src.add_argument("--assignment", help="CSV with columns node, district")
    ap.add_argument("--name-col", default="EDName2025")
    ap.add_argument("--table", default=str(REPO / "data/outputs/s15_2_va_criteria.csv"))
    ap.add_argument("--stated", help="CSV with columns district, population (the map's own figures)")
    ap.add_argument("--label", default="map")
    ap.add_argument("--out")
    a = ap.parse_args()

    sha = hashlib.sha256(Path(a.table).read_bytes()).hexdigest()
    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    pop = pd.Series({n: graph.nodes[n]["pop_2021"] for n in nodes})
    tab = load_table(a.table, nodes, pop)
    stated = None
    if a.stated:
        stated = pd.read_csv(a.stated, dtype={"district": str}).set_index("district")["population"].astype(float)
    summary, df = check(labels_for(va, nodes, a), tab, reserve_areas(), stated)
    summary = {"label": a.label, "table": a.table, "table_sha256": sha, "table_is_a23": sha == A23_SHA,
               "status": "SUPPLEMENTARY - descriptive, not a registered test", **summary}

    print(f"{a.label}: {summary['districts']} districts, overlay average {summary['average_pop_overlay']:,}; "
          f"deviation {summary['dev_range_overlay_pct'][0]:+.1f}% to {summary['dev_range_overlay_pct'][1]:+.1f}% (overlay)")
    print(f"criteria table {sha[:12]}{'' if summary['table_is_a23'] else '  (NOT the Amendment 5, Part 15 table)'}; "
          f"population basis: {'overlay and stated' if summary['stated_populations'] else 'overlay only'}")
    if summary["stated_populations"]:
        lo, hi = summary["dev_range_stated_pct"]
        print(f"deviation {lo:+.1f}% to {hi:+.1f}% (stated)")
        for n in summary["stated_name_matches_not_exact"]:
            print(f"  name matched: {n}")
        for n in summary["stated_names_unmatched"] + summary["map_districts_without_stated"]:
            print(f"  NO MATCH (overlay only for this district): {n}")
    if summary["unassigned_pop_overlay"]:
        print(f"unassigned VA population: {summary['unassigned_pop_overlay']:,}")
    print(f"above +25%: {summary['above_plus25'] or 'none'}")
    print(f"below -50%: {summary['below_minus50'] or 'none'}")
    print(f"below -25%: {summary['below_minus25_count']} (s.15(2) allows up to {CAP})")
    for r in summary["below_minus25"]:
        st = "" if r["dev_stated_pct"] is None else f" (stated {r['dev_stated_pct']:+.1f}%)"
        print(f"  {r['district']:42s} {r['dev_overlay_pct']:+6.1f}%{st}  {r['criteria_met']}/5 [{r['criteria']}]"
              f"{'' if r['meets_3_of_5'] else '  fewer than 3 criteria'}")
    for r in summary["bases_disagree"]:
        print(f"  bases disagree, not counted: {r['district']} overlay {r['dev_overlay_pct']:+.1f}%, "
              f"stated {r['dev_stated_pct']:+.1f}%")
    if a.out:
        out = Path(a.out)
        out.write_text(json.dumps(summary, indent=1, default=str))
        df.to_csv(out.with_suffix(".csv"), index=False)
        print(f"wrote {out} and {out.with_suffix('.csv')}")


if __name__ == "__main__":
    main()
