# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
ledger.py

One list of the percentile-ranked comparisons read below from the saved outputs of the unregistered
analyses since Step C (2026-11-04 to 2026-11-07), with a multiple-testing reading across them.
Every percentile is turned into a two-sided p = 2 x min(pct, 100 - pct) / 100.
Benjamini-Hochberg (false discovery rate 5%) and Bonferroni are applied across all of them.
Chikina-Frieze-Pegden p-values enter as reported. Unregistered. Not every percentile the analyses
report is read: for example packing_cracking's Lethbridge lopsided-loss rows, six signals F's
election-day rows and set D's close4 are not.
A map beyond every plan has no percentile p of 0: where the chains' n_eff is known, p is floored at
2 / (n_eff + 1); a percentile of 0 or 100 without an n_eff is an error.

Usage: python -W ignore findings/test_ledger/ledger.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = HERE.parent
rows = []


def add(analysis, plan, comparison, measure, map_, pct=None, p=None, note="", n_eff=None):
    if p is None:
        p = min(1.0, 2 * min(pct, 100 - pct) / 100)
        if n_eff is not None:
            p = max(p, 2 / (n_eff + 1))
        assert p > 0, f"percentile {pct} with no n_eff: {analysis} {measure}"
    rows.append({"analysis": analysis, "plan": plan, "comparison": comparison, "measure": measure, "map": map_,
                 "percentile": pct, "p_two_sided": round(p, 6), "n_eff": n_eff, "note": note})


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
    lt = F / "local_targeting/local_targeting.json"
    if lt.exists():
        t = json.loads(lt.read_text())
        for k in ("competitive_vs_safe", "ndp_won_vs_ucp_won"):
            add("local targeting A", "399a489a", "Fisher exact, majority divisions changed", k, "panel", p=t["A"][k]["p_fisher_two_sided"])
        if t["B"]["p_sign_two_sided"] is not None:
            add("local targeting B", "399a489a", "sign test, close changed pairs", "margin shift direction", "panel", p=t["B"]["p_sign_two_sided"])
    cd = F / "changed_districts/summary.json"
    if cd.exists():
        # ucp_packed is left out: in a fixed region it equals ndp_packed less a constant (scaled), so it ranks identically
        for grp, blk in json.loads(cd.read_text())["groups"].items():
            for mp, mb in blk["maps"].items():
                for v, vb in mb["variants"].items():
                    for m_ in ("ndp_seats_all", "ndp_packed_all", "ndp_near_all", "ndp_far_all"):
                        add("changed districts", "3c501006", f"regional ReCom k{mb['k']}, {v}", f"{grp}: {m_}",
                            "majority" if mp == "majority" else "panel", vb[m_]["pct"], n_eff=vb[m_]["n_eff"])
    lw = F / "city_weight/lethbridge_at_w.json"
    if lw.exists():
        for w, vb in json.loads(lw.read_text())["weights"].items():
            if w == "0.5" or isinstance(vb, str):
                continue  # W = 0.5 is the hybrid-regions row already counted
            for m_ in ("city_far_all", "city_pieces"):
                add("city weight", "5dc4a0dd", f"regional ReCom, city-aware W={w}", f"Lethbridge: {m_}", "panel", vb[m_]["panel"]["pct"])
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
