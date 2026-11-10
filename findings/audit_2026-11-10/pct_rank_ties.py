#!/usr/bin/env python3
"""pct_rank_ties.py -- the percentile-rank float-parsing bug, and tie-aware midranks.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

The bug. The pipeline ranks a map's value x in an ensemble with a midrank:
    100 * (count(values < x) + 0.5 * count(values == x)) / N        (mcmc_ensemble.py pct_rank)
The ensemble values are read back from CSV with pandas' default float parser, which is fast
but not exactly rounding: for some decimal strings it returns the neighbouring float. Seats at
50/50 is a fraction k/n, so many plans share one value. If the string for k/n parses one step
off, `values == x` is false for every tied plan and they all count as below (or above) the map.

What this script does:
  1. For every k/87, k/89, k/91 (k = 0..n), writes the value the way the chain files hold it
     (shortest round-trip repr) and the way the pooled file holds it (%.17g), reads it back with
     the default parser and with float_precision="round_trip", and lists every k that mis-parses.
  2. Recomputes every published canonical percentile (2019, majority, minority) both ways.
  3. Does the same for the forest-ReCom run and for the one committed 89-district chain.
  4. If the branch origin/amendment17-local-runs is reachable in this clone, streams the
     89-district size-matched chains from it with `git show` (nothing is checked out) and
     checks the size-matched placements of both commission maps the same way.

Output: findings/audit_2026-11-10/pct_rank_ties.json
Run   : python findings/audit_2026-11-10/pct_rank_ties.py    (no network, no randomness)
Note  : which strings mis-parse is a property of the pandas C parser; versions are recorded.
"""
import gzip
import io
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().with_suffix(".json")
SIDE_BRANCH = "origin/amendment17-local-runs"
PARTISAN = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
ALL7 = PARTISAN + ["population_mad", "reock_proxy_median", "reock_proxy_pct_below_030"]


def midrank(values, x, tol=0.0):
    """Midrank percentile. tol = 0 is the pipeline's exact comparison; tol > 0 counts near-ties."""
    v = np.asarray(values, float)
    if tol:
        eq = np.abs(v - x) <= tol
        below = (v < x) & ~eq
    else:
        eq = v == x
        below = v < x
    return 100.0 * (below.sum() + 0.5 * eq.sum()) / len(v), int(below.sum()), int(eq.sum())


def parse_test(n):
    ks = np.arange(n + 1)
    true = ks / n
    res = {}
    for fmt_name, strings in (("repr", [repr(float(t)) for t in true]), ("%.17g", ["%.17g" % t for t in true])):
        text = "x\n" + "\n".join(strings) + "\n"
        default = pd.read_csv(io.StringIO(text))["x"].values.astype(float)
        exact = pd.read_csv(io.StringIO(text), float_precision="round_trip")["x"].values
        assert (exact == true).all()
        bad = ks[default != true]
        res[fmt_name] = {
            "n_misparsed": int(len(bad)),
            "of": int(n + 1),
            "k_misparsed": [int(k) for k in bad],
            "direction": {str(int(k)): ("parsed_low" if default[k] < true[k] else "parsed_high") for k in bad},
        }
    return res


def compare(values_default, values_exact, maps, metrics, tol=1e-12):
    rows = []
    for m in metrics:
        if m not in values_default:
            continue
        vd, ve = values_default[m].values, values_exact[m].values
        for name, sc in maps.items():
            x = sc.get(m)
            if x is None or (isinstance(x, float) and np.isnan(x)):
                continue
            p_pipe, _, eq_pipe = midrank(vd, x)
            p_exact, below, eq = midrank(ve, x)
            p_tol, _, eq_tol = midrank(vd, x, tol)
            rows.append({
                "map": name, "metric": m, "value": x,
                "percentile_as_pipeline_computes_it": round(p_pipe, 4),
                "tie_aware_midrank": round(p_exact, 4),
                "tie_aware_midrank_by_tolerance": round(p_tol, 4),
                "plans_strictly_below": below, "plans_tied": eq,
                "plans_tied_as_pipeline_sees_them": eq_pipe,
                "share_strictly_below_pct": round(100.0 * below / len(ve), 4),
                "share_at_or_below_pct": round(100.0 * (below + eq) / len(ve), 4),
                "changes": bool(abs(p_pipe - p_exact) > 1e-9),
            })
    return rows


def read_both(src, cols):
    """src: path or bytes. Returns (default-parsed, exactly-parsed) frames."""
    def rd(**kw):
        s = io.BytesIO(src) if isinstance(src, bytes) else src
        head = pd.read_csv(io.BytesIO(src) if isinstance(src, bytes) else src, nrows=0).columns
        return pd.read_csv(s, usecols=[c for c in cols if c in head], **kw)
    return rd(), rd(float_precision="round_trip")


def main():
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "versions": {"pandas": pd.__version__, "numpy": np.__version__},
        "parse_test": {},
    }
    for n in (87, 89, 91):
        out["parse_test"]["k/%d" % n] = parse_test(n)

    # ---- canonical ensemble: the four chain files (the authoritative copy) -------------------
    real = json.loads((ROOT / "data/outputs/simulation_real_map_scores_canonical.json").read_text())
    maps = {k: real[k] for k in ("2019_enacted", "majority_2026", "minority_2026")}
    parts = [read_both(ROOT / f"data/simulation_checkpoints_canonical/chain{i}_samples.csv", ALL7) for i in range(4)]
    d_def = pd.concat([p[0] for p in parts], ignore_index=True)
    d_ex = pd.concat([p[1] for p in parts], ignore_index=True)
    rows = compare(d_def, d_ex, maps, ALL7)
    pub = pd.read_csv(ROOT / "data/outputs/simulated_ensemble_percentiles_canonical.csv")
    label = {"2019 enacted": "2019_enacted", "majority 2026 canonical": "majority_2026", "minority 2026 canonical": "minority_2026"}
    pubd = {(label[r.map], r.metric): r.percentile for r in pub.itertuples() if r.percentile == r.percentile}
    for r in rows:
        p = pubd.get((r["map"], r["metric"]))
        r["published_percentile"] = None if p is None else round(float(p), 4)
        r["pipeline_value_reproduces_published"] = None if p is None else bool(abs(p - r["percentile_as_pipeline_computes_it"]) < 5e-4)
    n_misparsed_values = int((d_def["seats_at_50_50"].values != d_ex["seats_at_50_50"].values).sum())
    out["canonical"] = {
        "n_plans": int(len(d_ex)),
        "seats_values_parsed_one_step_off": n_misparsed_values,
        "seats_at_50_50_distribution_k_of_87": {
            str(int(k)): int(c) for k, c in
            pd.Series(np.round(d_ex["seats_at_50_50"].values * 87).astype(int)).value_counts().sort_index().items()},
        "rows": rows,
        "rows_that_change": [r for r in rows if r["changes"]],
    }

    # ---- forest-ReCom run (percentiles published in forest_recom_percentiles_phaseA.csv) -----
    fr = json.loads((ROOT / "data/outputs/forest_recom_real_map_scores_phaseA.json").read_text())
    f_def, f_ex = read_both(ROOT / "data/outputs/forest_recom_raw_samples_phaseA.csv", PARTISAN + ["chunk"])
    keep = f_ex["chunk"].values >= 1  # the published forest percentiles drop chunk 0 of each chain
    rows = compare(f_def[keep], f_ex[keep], {k: fr[k] for k in ("majority_2026", "minority_2026")}, PARTISAN)
    fpub = pd.read_csv(ROOT / "data/outputs/forest_recom_percentiles_phaseA.csv")
    fpubd = {(r.map, r.metric): r.percentile for r in fpub.itertuples()}
    for r in rows:
        p = fpubd.get((r["map"], r["metric"]))
        r["published_percentile"] = None if p is None else round(float(p), 4)
        r["pipeline_value_reproduces_published"] = None if p is None else bool(abs(p - r["percentile_as_pipeline_computes_it"]) < 5e-4)
    out["forest_recom"] = {"n_plans": int(keep.sum()), "rows": rows, "rows_that_change": [r for r in rows if r["changes"]]}

    # ---- 89-district size-matched sets -------------------------------------------------------
    sm = json.loads((ROOT / "data/outputs/size_matched_results_2026-10-30.json").read_text())
    k89 = {"majority_2026": maps["majority_2026"], "minority_2026": maps["minority_2026"]}
    have_branch = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", "--quiet", SIDE_BRANCH],
                                 capture_output=True).returncode == 0
    folder = {"A_k89": "data/simulation_checkpoints_k89", "B_k89": "data/simulation_checkpoints_k89_eps25",
              "C_k89": "data/simulation_checkpoints_k89_muni", "D_k89": "data/simulation_checkpoints_k89_s152a23"}
    size = {"side_branch": SIDE_BRANCH, "side_branch_reachable": have_branch, "sets": {}}
    for key in sorted(k for k in sm if k.endswith("_k89")):
        dd, de, missing = [], [], []
        for ch in sm[key]["chains"]:
            local = ROOT / folder[key] / f"chain{ch}_samples.csv"
            if local.exists():
                a, b = read_both(local, PARTISAN)
            elif have_branch:
                blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{SIDE_BRANCH}:{folder[key]}/chain{ch}_samples.csv.gz"],
                                      capture_output=True)
                if blob.returncode != 0:
                    missing.append(ch)
                    continue
                a, b = read_both(gzip.decompress(blob.stdout), PARTISAN)
            else:
                missing.append(ch)
                continue
            dd.append(a)
            de.append(b)
        if missing or not dd:
            size["sets"][key] = {"computed": False, "chains_missing": missing,
                                 "why": "chains are not on this branch and the side branch is not reachable"}
            continue
        a, b = pd.concat(dd, ignore_index=True), pd.concat(de, ignore_index=True)
        rows = compare(a, b, k89, PARTISAN)
        for r in rows:
            p = sm[key]["measures"].get(r["metric"], {}).get(r["map"], {}).get("pct")
            r["published_percentile"] = p
            r["pipeline_value_reproduces_published"] = None if p is None else bool(abs(p - r["percentile_as_pipeline_computes_it"]) < 0.006)
        size["sets"][key] = {
            "computed": True, "chains": sm[key]["chains"], "n_plans": int(len(b)),
            "seats_values_parsed_one_step_off": int((a["seats_at_50_50"].values != b["seats_at_50_50"].values).sum()),
            "rows": rows, "rows_that_change": [r for r in rows if r["changes"]],
        }
    out["size_matched_89"] = size

    # ---- summary -----------------------------------------------------------------------------
    changed = [("canonical", r) for r in out["canonical"]["rows_that_change"]]
    changed += [("forest_recom", r) for r in out["forest_recom"]["rows_that_change"]]
    for key, s in size["sets"].items():
        if s.get("computed"):
            changed += [(key, r) for r in s["rows_that_change"]]
    y19 = next(r for r in out["canonical"]["rows"] if r["map"] == "2019_enacted" and r["metric"] == "seats_at_50_50")
    published_k = {"2019 map 40/87": (40, 87), "majority 41/89": (41, 89), "minority 46/89": (46, 89),
                   "2019 all ballots 41/87": (41, 87), "majority all ballots 42/89": (42, 89),
                   "panel election-day 44/91": (44, 91), "panel all ballots 45/91": (45, 91),
                   "para-167 election-day 43/91": (43, 91), "para-167 all ballots 44/91": (44, 91)}
    out["summary"] = {
        "misparsed_counts_repr": {k: v["repr"]["n_misparsed"] for k, v in out["parse_test"].items()},
        "published_seat_values_and_whether_their_string_misparses": {
            name: bool(k in out["parse_test"]["k/%d" % n]["repr"]["k_misparsed"]) for name, (k, n) in published_k.items()},
        "published_percentiles_that_change": [
            {"ensemble": e, "map": r["map"], "metric": r["metric"],
             "as_published": r["percentile_as_pipeline_computes_it"], "tie_aware_midrank": r["tie_aware_midrank"],
             "plans_tied": r["plans_tied"]} for e, r in changed],
        "only_2019_seats_changes": bool(len(changed) == 1 and changed[0][0] == "canonical"
                                        and changed[0][1]["map"] == "2019_enacted"
                                        and changed[0][1]["metric"] == "seats_at_50_50"),
        "seats_2019_as_published": y19["percentile_as_pipeline_computes_it"],
        "seats_2019_tie_aware_midrank": y19["tie_aware_midrank"],
        "seats_2019_share_strictly_below": y19["share_strictly_below_pct"],
        "seats_2019_share_at_or_below": y19["share_at_or_below_pct"],
        "seats_2019_plans_tied": y19["plans_tied"],
        "not_checked": [
            "All-ballots percentiles (findings/allballots_ranking/canonical_ranking.json): the all-ballots chains are not committed. "
            "The 2019 map's all-ballots seats value is 41/87, whose string mis-parses, so its published 74.08 is very likely "
            "the share at or below, not a midrank; it cannot be recomputed here.",
            "91-district sets (the panel's map): not recomputed here; of the panel's values only 45/91 (all ballots) was checked for parsing.",
        ],
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    s = out["summary"]
    print(json.dumps({k: s[k] for k in ("misparsed_counts_repr", "only_2019_seats_changes", "seats_2019_as_published",
                                         "seats_2019_tie_aware_midrank", "published_percentiles_that_change")}, indent=1))
    print(json.dumps(s["published_seat_values_and_whether_their_string_misparses"]))


if __name__ == "__main__":
    main()
