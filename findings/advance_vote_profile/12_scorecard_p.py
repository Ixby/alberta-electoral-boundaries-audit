"""The registered scorecard restated under rule P (Amendment 14, Part 6), beside Amendment 12's rule.

Maps: the panel reconstruction (v3), the commission majority, the commission minority, the ¶167 map.

What is computed here, and from where
- Partisan lane P1-P4 (spec §3; verdict_synthesis.py's flag rule, applied as written):
    rule P: values and canonical-ensemble percentiles from outputs/ensemble_ranks_p.json (the replayed
    canonical chains that passed, 1,010,000 plans); P1's line from outputs/thresholds_p.json (+2.15%).
    Amendment 12: the panel from findings/amendment12_rehearsal/joint_outlier_allballots.json (registered
    joint_outlier_score_canonical.run_candidate on the M0 canonical ensemble; v3 has the same votes by
    construction, findings/iap_v3_two_lane/README.md); the commission maps from
    findings/allballots_ranking/canonical_ranking.json; the ¶167 map's P1 value from
    findings/iap_para167/real_maps_all_ballots.json. P1's line +1.394%.
    The ¶167 map's P2-P4 under Amendment 12 need the M0 canonical chains, which are not in this checkout:
    not computed.
- Structural lane S1-S6 (spec §3, midpoint rule, 3 of 5): S1-S3 and S6 use no votes and are read from
    the filed battery outputs. S5 is recomputed here for every map on both vote files with
    run_structural_battery.compute_S5_drain (imported, not edited). Amendment 12: flag below 0.0019398.
    Rule P: set aside (Amendment 14, Part 3): no flag; drain and midpoint reported beside it.
- Size-matched competitive seats (Amendment 5, Part 17: flag if close4 <= the set's 5th percentile):
    Amendment 12 from the filed all-ballots runs. Rule P: ensemble_ranks_p.json gives a midrank percentile
    and the median, not the 5th percentile, so the flag is not computed.
- R1/R2 (Amendment 8): the panel's from outputs/territory_null_p.json (both rules).

Writes outputs/scorecard_p.json. Run from the repository root:
  STAMP_MODEL=... STAMP_EFFORT=... python -I -W ignore findings/advance_vote_profile/12_scorecard_p.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import M0_SHA256, OUT, ROOT, VA_M0, VA_P, sha256, write_json  # noqa: E402

P_SHA256 = "bf9b27226e457ddb4b8c2feaa77f7402d1c3d1284657c821d208f6597b8f73bd"  # Amendment 14, Part 2
P1_A12 = 0.01394       # Amendment 12, Part 3
S5_A12 = 0.0019398     # Amendment 12, Part 3
PCT_LINE = 95.0        # P2-P4: p95 or more in the UCP direction
P3_LOW = 5.0           # P3's NDP-direction tail: reported, not counted (verdict_synthesis.py)

F = {
    "ranks_p": OUT / "ensemble_ranks_p.json",
    "thresholds_p": OUT / "thresholds_p.json",
    "territory_p": OUT / "territory_null_p.json",
    "joint_a12_panel": ROOT / "findings/amendment12_rehearsal/joint_outlier_allballots.json",
    "canonical_a12": ROOT / "findings/allballots_ranking/canonical_ranking.json",
    "para167_a12": ROOT / "findings/iap_para167/real_maps_all_ballots.json",
    "para167_cmp": ROOT / "findings/iap_para167/comparison.json",
    "size_matched_a12": ROOT / "findings/amendment12_rehearsal/size_matched_allballots.json",
    "struct_panel": ROOT / "findings/amendment12_checks/structural_panel_v3_allballots.json",
    "struct_majority": ROOT / "findings/amendment12_checks/structural_majority_allballots.json",
    "struct_minority": ROOT / "findings/amendment12_checks/structural_minority_allballots.json",
    "struct_para167": ROOT / "findings/iap_para167/structural.json",
}
SHP = {
    "panel_v3_91": ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg",
    "majority_89": ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
    "minority_89": ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
    "para167_91": ROOT / "findings/iap_para167/para167_map.gpkg",
}
STRUCT = {"panel_v3_91": "struct_panel", "majority_89": "struct_majority",
          "minority_89": "struct_minority", "para167_91": "struct_para167"}
MAPS = list(SHP)
N_DIST = {"panel_v3_91": 91, "majority_89": 89, "minority_89": 89, "para167_91": 91}
STATS = {"p1": "efficiency_gap", "p2": "mean_median", "p3": "declination", "p4": "seats_at_50_50"}


def load(k):
    return json.loads(F[k].read_text(encoding="utf-8"))


def partisan_p(ranks, line):
    canon = next(s for s in ranks["sets"] if s["set"] == "canonical")
    assert canon["chains_used"] == [0, 1, 2, 3] and canon["plans"] == 1_010_000
    get = {(r["map"], r["statistic"]): r for r in canon["ranks"]}
    out = {}
    for m in MAPS:
        tests = {}
        for t, st in STATS.items():
            r = get[(m, st)]
            e = {"value": r["value_p"], "percentile": r["percentile"]}
            if t == "p1":
                e.update(line=line, flag=r["value_p"] >= line)
            else:
                e.update(line="p95", flag=r["percentile"] >= PCT_LINE)
            if t == "p3":
                e["ndp_tail_reported_not_counted"] = r["percentile"] <= P3_LOW
            tests[t] = e
        out[m] = tests
    # The ranks are midrank percentiles (mcmc_ensemble.pct_rank); the registered rule counts plans at or
    # below. They differ only on ties. Seats at 50/50 is k/n: an 89- or 91-district value cannot equal any
    # k/87, so for these four maps there are no ties on P4.
    for m in MAPS:
        v = out[m]["p4"]["value"]
        assert all(abs(v - k / 87) > 1e-9 for k in range(88)), m
    return out


def partisan_a12():
    j = load("joint_a12_panel")["maps"]["candidate"]["marginals"]
    c = load("canonical_a12")
    p167 = load("para167_a12")["para167_map"]
    src = {"majority_89": "majority_2026", "minority_89": "minority_2026"}
    out = {}
    for m in MAPS:
        tests = {}
        for t, st in STATS.items():
            if m == "panel_v3_91":
                val, pct = j[st]["observed"], round(100 * j[st]["ucp_direction_percentile"], 2)
            elif m in src:
                x = c[src[m]][st]["all_ballots"]
                val, pct = x["value"], x["pct"]
            else:
                val, pct = p167[st], None
            if t == "p1":
                e = {"value": val, "percentile": pct, "line": P1_A12, "flag": val >= P1_A12}
            elif pct is None:
                e = {"value": val, "percentile": None, "line": "p95", "flag": None,
                     "not_computed": "needs the M0 canonical ensemble (data/simulation_checkpoints_allballots), "
                                     "not in this checkout; no canonical rank of this map on M0 is filed"}
            else:
                e = {"value": val, "percentile": pct, "line": "p95", "flag": pct >= PCT_LINE}
            if t == "p3" and pct is not None:
                e["ndp_tail_reported_not_counted"] = pct <= P3_LOW
            tests[t] = e
        out[m] = tests
    return out


def structural(thr_p):
    sys.path.insert(0, str(ROOT / "analysis/scripts"))
    import run_structural_battery as rsb
    if hasattr(rsb, "_log_run"):
        rsb._log_run = lambda *a, **k: None
    out = {}
    for m in MAPS:
        s = load(STRUCT[m])["metrics"]
        fixed = {
            "s1": {"value": s["S1_population_mad"]["value"], "line": 3382.5, "flag": s["S1_population_mad"]["flag"]},
            "s2": {"value": s["S2_municipal_split_count"]["value"], "line": 26.5, "flag": s["S2_municipal_split_count"]["flag"]},
            "s3": {"value": s["S3_anchoring_score"]["value"], "line": 0.7601, "flag": s["S3_anchoring_score"]["flag"]},
            "s6": {"value": s["S6_chair_flag_replication"].get("patterns_count_discriminating"), "line": 2.5,
                   "flag": s["S6_chair_flag_replication"]["flag"]},
        }
        d = {}
        for rule, va in (("a12", VA_M0), ("p", VA_P)):
            r = rsb.compute_S5_drain(SHP[m], va)
            if r.get("drain_score") is None or str(r.get("_note", "")).startswith("STUB"):
                raise SystemExit(f"S5 did not execute for {m} on {rule}: {r}")
            d[rule] = float(r["drain_score"])
        out[m] = {"fixed": fixed, "drain": d}
    # Cross-checks against the filed values.
    a12f = {"panel_v3_91": "struct_panel", "majority_89": "struct_majority", "minority_89": "struct_minority"}
    for m, k in a12f.items():
        assert abs(out[m]["drain"]["a12"] - load(k)["metrics"]["S5_drain_score"]["drain_score"]) < 1e-12, m
    assert abs(out["majority_89"]["drain"]["p"] - thr_p["s5_line"]["majority_drain"]) < 1e-12
    assert abs(out["minority_89"]["drain"]["p"] - thr_p["s5_line"]["minority_drain"]) < 1e-12
    return out


def main():
    assert sha256(VA_P) == P_SHA256, "P vote file hash"
    assert sha256(VA_M0) == M0_SHA256, "M0 vote file hash"
    thr = load("thresholds_p")
    ranks = load("ranks_p")
    p1_p = thr["p1_line"]["value"]
    s5_mid_p = thr["s5_line"]["value"]
    assert round(p1_p, 4) == 0.0215

    part_p = partisan_p(ranks, p1_p)
    part_a = partisan_a12()
    st = structural(thr)

    # Size-matched competitive seats (close4).
    sm = load("size_matched_a12")["results"]
    cmp167 = load("para167_cmp")["all_ballots"]["ranks_set_D"]["close4"]
    sets_p = {s["set"]: s for s in ranks["sets"] if "ranks" in s}
    comp = {}
    for m in MAPS:
        a12 = {}
        if m == "panel_v3_91":
            for k, v in sm.items():
                c = v["measures"]["close4"]
                a12[k[0].lower()] = {"value": c["iap_2026_assembled"]["value"], "percentile": c["iap_2026_assembled"]["pct"],
                             "q05": c["q05"], "flag": c["iap_2026_assembled"]["flag"]}
        elif m == "para167_91":
            a12["d"] = {"value": cmp167["para167_map"]["value"], "percentile": cmp167["para167_map"]["pct"],
                        "q05": cmp167["q05"], "flag": cmp167["para167_map"]["value"] <= cmp167["q05"],
                        "note": "set D only; sets A to C not placed for this map on M0"}
        else:
            a12["not_computed"] = "no 89-district all-ballots size-matched run is filed (amendment12_rehearsal README, failure 5)"
        p = {}
        for name, s in sets_p.items():
            if name == "canonical" or not name.endswith(str(N_DIST[m])):
                continue
            r = next((x for x in s["ranks"] if x["map"] == m and x["statistic"] == "close4"), None)
            if r:
                p[name[0].lower()] = {"value": r["value_p"], "percentile_midrank": r["percentile"], "ensemble_p50": r["ensemble_p50"],
                              "flag": None, "not_computed": "Part 17 flags at or below the set's 5th percentile; "
                                                            "ensemble_ranks_p.json gives no 5th percentile"}
        comp[m] = {"a12": a12, "p": p}
    comp["minority_89"]["p_note"] = "minority close4 is 8 to 9 across the lean range under P (9 at lean 1.0, ranked)"

    terr = load("territory_p")
    redraw = {
        "panel_v3_91": {rule: {"r1_efficiency_gap": {"value": terr[k]["eg"]["observed"], "p_two_sided": terr[k]["eg"]["p_two_sided"],
                                                     "flag": terr[k]["eg"]["p_two_sided"] < 0.05},
                               "r2_drain": {"value": terr[k]["drain"]["observed"], "p_two_sided": terr[k]["drain"]["p_two_sided"],
                                            "flag": terr[k]["drain"]["p_two_sided"] < 0.05}}
                        for rule, k in (("a12", "m0"), ("p", "p"))},
        "majority_89": "not applicable: R1 and R2 test the November map's changes against the majority map",
        "minority_89": "not applicable: R1 and R2 test the November map's changes against the majority map",
        "para167_91": "not computed: no redraw-test null has been run for this map",
    }
    redraw["panel_v3_91"]["note"] = ("scored on iap_2026_assembled.gpkg (Step C); v3 moves no voting area's representative "
                                     "point, so its votes per district are the same")

    maps = {}
    for m in MAPS:
        s = st[m]
        struct_a = {**s["fixed"], "s5": {"value": s["drain"]["a12"], "line": S5_A12, "flag": s["drain"]["a12"] < S5_A12}}
        struct_p = {**s["fixed"], "s5": {"value": s["drain"]["p"], "line": s5_mid_p, "flag": False, "set_aside": True,
                                         "below_midpoint_reported_only": s["drain"]["p"] < s5_mid_p}}
        n_sa = sum(bool(v["flag"]) for v in struct_a.values())
        n_sp = sum(bool(v["flag"]) for v in struct_p.values())
        n_pa = sum(1 for v in part_a[m].values() if v["flag"])
        nc_pa = [t for t, v in part_a[m].items() if v["flag"] is None]
        n_pp = sum(1 for v in part_p[m].values() if v["flag"])
        maps[m] = {
            "structural": {"a12": struct_a, "p": struct_p},
            "partisan": {"a12": part_a[m], "p": part_p[m]},
            "counts": {
                "a12": {"structural_flags": n_sa, "of": 5, "structural": "replicated" if n_sa >= 3 else "not replicated",
                        "partisan_flags": n_pa, "partisan_of": 4 - len(nc_pa), "partisan_not_computed": nc_pa,
                        "partisan": ("present" if n_pa >= 2 else ("absent" if not nc_pa else "not determined"))},
                "p": {"structural_flags": n_sp, "of": 5, "structural": "replicated" if n_sp >= 3 else "not replicated",
                      "partisan_flags": n_pp, "partisan_of": 4, "partisan_not_computed": [],
                      "partisan": "present" if n_pp >= 2 else "absent"},
            },
            "competitive_seats": comp[m],
            "redraw_tests": redraw[m],
        }

    payload = {
        "what": "Registered scorecard (spec §3 two lanes, plus the other vote-based tests) under rule P and Amendment 12's rule",
        "rules": {
            "a12": {"vote_file_sha256": M0_SHA256, "p1_line": P1_A12, "s5_line": S5_A12, "s5_flag": "below the line"},
            "p": {"vote_file_sha256": P_SHA256, "p1_line": p1_p, "s5_midpoint": s5_mid_p,
                  "s5": "set aside on this file (Amendment 14, Part 3): no flag, counts as not flagged"},
            "p2_to_p4": "p95 or more in the UCP direction against the 87-district canonical ensemble; P3's p5 tail reported, not counted",
            "structural_count": "3 or more of S1, S2, S3, S5, S6 = replicated; S4 measured, not counted",
            "partisan_count": "2 or more of P1 to P4 = present",
            "percentiles": "rule P: midrank (mcmc_ensemble.pct_rank), from ensemble_ranks_p.json; Amendment 12: share of plans at or "
                           "below. They differ only on ties; P4 cannot tie for these maps (checked). Rule-P values in that file are "
                           "rounded to 5 significant decimals from headline_table.csv (lean 1.0)",
        },
        "maps": maps,
        "unchanged_no_votes": ["S1", "S2", "S3", "S4", "S6", "X1", "towns over-divided", "city versus rest"],
        "not_restated": ["qsgy8 tripwires: run on election-day seats at 50/50 as filed (amendment12_rehearsal README, item 6)"],
    }
    inputs = [VA_P, VA_M0, *F.values(), *SHP.values()]
    write_json("scorecard_p.json", payload, __file__, inputs)
    for m in MAPS:
        print(m, json.dumps(maps[m]["counts"]))


if __name__ == "__main__":
    main()
