# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | Statistics Canada 2021 Census (Open Licence)
"""
implied_w.py

preregistration/city_weight_calibration_2026-11-07.md, "Inference": each map's implied city-boundary
weight W, by linear interpolation of its split ratio R on the calibration curve for its number of
districts. A map outside the curve's range is reported as below 0 or above 1, not extrapolated.
Curves: this folder's calibration_{a,b,c}.jsonl (indices 280-299) and the earlier Amendment 17 runs
(alberta_audit/analysis/methodology/amendment17_chain_runs: muni_calibration_10k.jsonl and the 6,000-step
k=91 rows of its README table). Where a W has both, the 10,000-step value is used.

Usage: python findings/city_weight/implied_w.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A17 = HERE.parents[2] / "alberta_audit/analysis/methodology/amendment17_chain_runs"
K91_6K = {0.0: 0.388, 0.10: 0.338, 0.25: 0.279, 1.0: 0.065}  # README table, 6,000 steps
COMMISSION = ("2003_commission", "2010_commission", "2017_commission", "2026_majority")


def curves():
    c = {}
    for k, pts in ((91, K91_6K),):
        for w, r in pts.items():
            c.setdefault(k, {})[w] = (r, "A17 README, 6,000 steps")
    files = [A17 / "muni_calibration_10k.jsonl"] + sorted(HERE.glob("calibration_*.jsonl"))
    for f in files:
        for line in f.read_text().splitlines():
            d = json.loads(line)
            c.setdefault(d["k"], {})[d["W"]] = (d["mean_second_half"], f"{f.name} idx {d['idx']}, {d['steps']:,} steps")
    return {k: dict(sorted(v.items())) for k, v in c.items()}


def implied(curve, R):
    ws = list(curve)
    rs = [curve[w][0] for w in ws]
    if R > rs[0]:
        return "below 0"
    if R < rs[-1]:
        return "above 1"
    for (w0, r0), (w1, r1) in zip(zip(ws, rs), zip(ws[1:], rs[1:])):
        if r1 <= R <= r0 and r0 != r1:
            return round(w0 + (w1 - w0) * (r0 - R) / (r0 - r1), 3)
    return "curve not monotone at R"


def main():
    C = curves()
    real = json.loads((HERE / "real_ratios.json").read_text())
    out = {"curves": {k: {str(w): {"R": r, "source": s} for w, (r, s) in v.items()} for k, v in C.items()}, "maps": {}}
    for name, v in real.items():
        if not isinstance(v, dict) or name.endswith(("_EA_file", "_GoA_layer")):
            continue
        k = v["k"]
        out["maps"][name] = {"k": k, "R": round(v["R"], 4), "implied_W": implied(C[k], v["R"]),
                             "sets_range": name in COMMISSION}
    ws = [out["maps"][m]["implied_W"] for m in COMMISSION]
    out["commission_range"] = {"min": min(ws), "max": max(ws)} if all(isinstance(w, float) for w in ws) else "not numeric"
    (HERE / "implied_w.json").write_text(json.dumps(out, indent=1), encoding="utf8")
    for k, v in C.items():
        print(k, {w: r for w, (r, _) in v.items()})
    for m, v in out["maps"].items():
        print(m, v)
    print("commission range", out["commission_range"])


if __name__ == "__main__":
    main()
