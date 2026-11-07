# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
ledger.py

One list of every percentile-ranked comparison made in the unregistered analyses since Step C
(2026-11-04 to 2026-11-07), read from their saved outputs, with a multiple-testing reading across
the whole family. Every percentile is turned into a two-sided p = 2 x min(pct, 100 - pct) / 100.
Benjamini-Hochberg (false discovery rate 5%) and Bonferroni are applied across all of them.
Chikina-Frieze-Pegden p-values enter as reported. Nothing is dropped. Unregistered.

Usage: python -W ignore findings/test_ledger/ledger.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = HERE.parent
rows = []


def add(analysis, plan, comparison, measure, map_, pct=None, p=None, note=""):
    if p is None:
        p = min(1.0, 2 * min(pct, 100 - pct) / 100)
    rows.append({"analysis": analysis, "plan": plan, "comparison": comparison, "measure": measure, "map": map_,
                 "percentile": pct, "p_two_sided": round(p, 6), "note": note})


def main():
    c = json.loads((F / "iap_para167/comparison.json").read_text())
    for b in ("all_ballots", "election_day"):
        for m, v in c[b]["ranks_set_D"].items():
            if m in ("ucp_seats", "efficiency_gap", "mean_median", "declination", "seats_at_50_50"):
                for k, lab in (("iap_2026_assembled_v3", "panel"), ("para167_map", "para167")):
                    add("para167 comparison", "5eb63b34", f"set D (91), {b}", m, lab, v[k]["pct"])
    for b in ("all_ballots", "election_day"):
        s = json.loads((F / f"packing_cracking/sorted_vs_neutral_{b}.json").read_text())
        for k in ("panel", "para167"):
            for m in ("seats_40_to_50", "seats_under_30", "ndp_seats"):
                add("packing and cracking, part 2", "c2f1a710", f"set D sorted (91), {b}", m, k, s[k][m]["pct"])
    r = json.loads((F / "six_signals/regional_south.json").read_text())
    for m in ("leth_far_all", "leth_pieces", "ndp_seats_all"):
        for k in ("panel", "para167"):
            add("six signals F, south city-blind", "0610a3a9", "regional ReCom, city-blind", m, k, r["measures"][m][k]["pct"])
    h = json.loads((F / "hybrid_regions/summary.json").read_text())
    for reg, blk in h["regions"].items():
        for v, vb in blk["variants"].items():
            if reg == "Lethbridge" and v == "blind":
                continue  # same chains as signal F
            for m in ("city_far_all", "city_pieces"):
                add("hybrid regions", "d2c1353e", f"regional ReCom, {v}", f"{reg}: {m}", "panel", vb[m]["panel"]["pct"])
    cfp = json.loads((F / "hybrid_regions/cfp_lethbridge.json").read_text())
    for w, rr in cfp["walks"].items():
        for k in ("V1", "V2"):
            add("Chikina-Frieze-Pegden", "f9bb45da", f"local walk {w}", k, "panel", p=rr[k]["p"], note="p as reported, one-sided")
    m = len(rows)
    order = sorted(range(m), key=lambda i: rows[i]["p_two_sided"])
    bh_max = 0
    for rank, i in enumerate(order, 1):
        if rows[i]["p_two_sided"] <= 0.05 * rank / m:
            bh_max = rank
    for rank, i in enumerate(order, 1):
        rows[i]["bh_significant"] = rank <= bh_max
        rows[i]["bonferroni_significant"] = rows[i]["p_two_sided"] <= 0.05 / m
        rows[i]["nominal_flag_5pct_tail"] = rows[i]["percentile"] is not None and (rows[i]["percentile"] >= 95 or rows[i]["percentile"] <= 5)
    out = {"n_tests": m, "bh_discoveries": bh_max, "bonferroni_discoveries": sum(r["bonferroni_significant"] for r in rows),
           "nominal_flags": sum(r["nominal_flag_5pct_tail"] for r in rows), "rows": sorted(rows, key=lambda r: r["p_two_sided"])}
    (HERE / "ledger.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    print({k: out[k] for k in ("n_tests", "nominal_flags", "bh_discoveries", "bonferroni_discoveries")})
    for r in out["rows"][:16]:
        print(f"{r['p_two_sided']:.4f} {r['percentile']} {r['map']:8s} {r['comparison']:34s} {r['measure']} {'BH' if r['bh_significant'] else ''}")


if __name__ == "__main__":
    main()
