# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
map_diff.py
-----------

How far one district map departs from another, district by district.

SUPPLEMENTARY. Not a registered November test. Intended uses: the advisory
panel's map against the committee's map (how much the committee changed),
and the committee's map against the commission's majority and minority maps.

For every district of map B: the district of map A it takes the most
population from, the share of B's population that comes from it, and the
share of that A district's population that B keeps. A B district is
"unchanged" from its A match when both shares are at least 99%, the rule
Amendment 5, Part 13 uses for X1 (a) and (b). Population is the VA-level 2021 census
overlay (graph attribute pop_2021); VAs are attributed by representative
point, as in score_x1.py.

Usage
  python analysis/scripts/map_diff.py --a PATH --b PATH
         [--a-col COL] [--b-col COL] [--a-label NAME] [--b-label NAME]
         [--out diff.csv]
  Either map may instead be a CSV with columns node, district.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))
import mcmc_ensemble as me  # noqa: E402
import s15_2_criteria as s152  # noqa: E402

SAME = 0.99


def labels(path, col, va, nodes):
    if str(path).lower().endswith(".csv"):
        asg = pd.read_csv(path, dtype={"district": str}).set_index("node")["district"]
        return asg.reindex(nodes).fillna("__unassigned__")
    pts = va.loc[nodes, ["geometry"]].to_crs(s152.WORK)
    pts["geometry"] = pts.geometry.representative_point()
    return s152.assign(pts, path, col)


def diff(la, lb, pop):
    df = pd.DataFrame({"a": la.to_numpy(), "b": lb.to_numpy(), "pop": pop.to_numpy()})
    cross = df.groupby(["b", "a"])["pop"].sum()
    b_tot, a_tot = df.groupby("b")["pop"].sum(), df.groupby("a")["pop"].sum()
    rows = []
    for b, g in cross.groupby(level=0):
        g = g.droplevel(0).sort_values(ascending=False)
        a, p = g.index[0], g.iloc[0]
        from_a, kept = p / b_tot[b], p / a_tot[a]
        rows.append({"district_b": b, "pop_b": round(b_tot[b]), "best_match_a": a,
                     "share_of_b_from_match": round(from_a, 4), "share_of_match_kept": round(kept, 4),
                     "unchanged": bool(from_a >= SAME and kept >= SAME), "a_districts_drawn_from": int((g > 0).sum())})
    out = pd.DataFrame(rows).sort_values(["unchanged", "share_of_b_from_match"]).reset_index(drop=True)
    # share of all people whose district (matched B to A) is the same
    same_pop = sum(cross.get((r.district_b, r.best_match_a), 0) for r in out.itertuples())
    return out, same_pop / df["pop"].sum()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--a-col", default="EDName2025")
    ap.add_argument("--b-col", default="EDName2025")
    ap.add_argument("--a-label", default="A")
    ap.add_argument("--b-label", default="B")
    ap.add_argument("--out")
    a = ap.parse_args()
    va, graph = me.build_va_graph(verbose=False)
    nodes = sorted(graph.nodes())
    pop = pd.Series({n: graph.nodes[n]["pop_2021"] for n in nodes})
    out, kept = diff(labels(a.a, a.a_col, va, nodes), labels(a.b, a.b_col, va, nodes), pop)
    n_same = int(out.unchanged.sum())
    print(f"{a.b_label} vs {a.a_label} (SUPPLEMENTARY, descriptive): {len(out)} districts in {a.b_label}; "
          f"{n_same} unchanged (>= 99% both ways); {100 * kept:.1f}% of people are in the part of their district drawn from its largest source")
    for r in out[~out.unchanged].itertuples():
        print(f"  {r.district_b:42s} <- {r.best_match_a:42s} {100 * r.share_of_b_from_match:5.1f}% from it, "
              f"keeps {100 * r.share_of_match_kept:5.1f}% of it, draws on {r.a_districts_drawn_from}")
    if a.out:
        out.to_csv(a.out, index=False)
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
