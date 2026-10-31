# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
size_matched_results.py
-----------------------

Distributions of the Amendment 17/20/21/23 neutral-map sets, their effective
sample sizes, and the two 2026 commission maps placed against the 89-district
sets.

  Sets      A  ±12.5% proposal band (Amendment 17); B  statute band (Amendment 20,
            set 1); C  municipality-aware, W = 0.5 (Amendment 20 set 2, Amendment
            21); D  s.15(2), Amendment 23 rule (Amendment 20 set 3). The first
            set D run (Amendment 21 table) is superseded and not read.
  n_eff     Geyer initial positive sequence, per chain, by the canonical
            estimator (simulation_multichain_ensemble.autocorrelation_ess),
            summed over chains. A result is final when pooled n_eff >= 400 and
            no chain's lag cap bound (Amendment 21 item 2(a)); otherwise it is
            provisional and n_eff is an upper bound where the cap bound.
  Flags     Amendment 17: towns split and the city-versus-rest gap flag at or
            above the set's 95th percentile; competitive seats (close4) flag at
            or below its 5th percentile.
  Placement midrank percentile, as mcmc_ensemble.pct_rank.

The commission maps have 89 districts, so they are placed against the k = 89
sets only. These placements are baselines; the registered test is the
November map's.

Usage
  python analysis/scripts/size_matched_results.py --root DIR --real real_maps.json
         [--out-json PATH] [--out-md PATH]
  DIR holds data/simulation_checkpoints_*/chainNNN_samples.csv[.gz]; chains
  also present under the repo's data/ are read from there.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
from mcmc_ensemble import pct_rank  # noqa: E402

_src = (REPO / "analysis/scripts/simulation_multichain_ensemble.py").read_text()
_ns = {"np": np}
exec(_src[_src.index("def autocorrelation_ess"):_src.index("\ndef ", _src.index("def autocorrelation_ess") + 10)], _ns)
autocorrelation_ess = _ns["autocorrelation_ess"]

SETS = {
    "A": ("", "±12.5% proposal band (Amendment 17)"),
    "B": ("_eps25", "statute band, ±25% (Amendment 20, set 1)"),
    "C": ("_muni", "municipality-aware, W = 0.5 (Amendment 20 set 2; Amendment 21)"),
    "D": ("_s152a23", "s.15(2), Amendment 23 rule (Amendment 20 set 3)"),
}
REGISTERED = {"towns_flagged": "upper", "city_gap_pct": "upper", "close4": "lower"}
REPORTED = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50", "population_mad", "ucp_seats"]
NEFF_FINAL = 400


def load_chains(roots, k, suffix):
    found = {}
    for root in roots:
        d = Path(root) / "data" / f"simulation_checkpoints_k{k}{suffix}"
        for f in sorted(d.glob("chain*_samples.csv*")) if d.exists() else []:
            idx = int(re.search(r"chain(\d+)_", f.name).group(1))
            found.setdefault(idx, f)
    return {i: pd.read_csv(f, usecols=lambda c: c in set(REGISTERED) | set(REPORTED)) for i, f in sorted(found.items())}


def neff_uncapped(x):
    """Diagnostic only, not the registered estimator: the same first-non-positive truncation
    with no lag cap (FFT autocorrelation, lags up to n/4)."""
    x = x[~np.isnan(x)]
    n = len(x)
    x = x - x.mean()
    v = x @ x / n
    if v == 0:
        return float("nan")
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[: n // 4] / n / v
    nonpos = np.where(acf[1:] <= 0)[0]
    lag = nonpos[0] if len(nonpos) else len(acf) - 1
    return n / (1 + 2 * acf[1: lag + 1].sum())


def ess(chains, col):
    per, capped = [], False
    for df in chains.values():
        x = df[col].to_numpy(float)
        r = autocorrelation_ess(x)
        cap = min(len(x[~np.isnan(x)]) // 4, 2000)
        capped |= r["max_lag_used"] >= cap
        per.append(r["n_eff"])
    tot = float(np.nansum(per))
    return tot, bool(capped), per


def summarize(chains, real):
    out = {}
    for col in list(REGISTERED) + REPORTED:
        if not chains or col not in next(iter(chains.values())):
            continue
        v = np.concatenate([df[col].to_numpy(float) for df in chains.values()])
        v = v[~np.isnan(v)]
        neff, capped, per = ess(chains, col)
        q05, q50, q95 = np.quantile(v, [0.05, 0.5, 0.95])
        diag = float(sum(neff_uncapped(df[col].to_numpy(float)) for df in chains.values()))
        row = {"n_plans": int(len(v)), "n_chains": len(chains), "n_eff": round(neff, 1),
               "n_eff_uncapped_diagnostic": round(diag, 1),
               "n_eff_per_chain": [round(x, 1) for x in per], "lag_cap_bound": capped,
               "status": "final" if neff >= NEFF_FINAL and not capped else "provisional",
               "q05": float(q05), "q50": float(q50), "q95": float(q95)}
        for m, rv in (real or {}).items():
            x = rv.get(col)
            if x is None:
                continue
            p = pct_rank(v, float(x))
            entry = {"value": float(x), "pct": round(float(p), 2)}
            if col in REGISTERED:
                entry["flag"] = bool(x >= q95) if REGISTERED[col] == "upper" else bool(x <= q05)
            row[m] = entry
        out[col] = row
    return out


def main(a):
    roots = [a.root, REPO]
    real = json.loads(Path(a.real).read_text())
    commission = {m: real[m] for m in ("majority_2026", "minority_2026")}
    res = {}
    for key, (suffix, label) in SETS.items():
        for k in (89, 91):
            chains = load_chains(roots, k, suffix)
            if not chains:
                continue
            res[f"{key}_k{k}"] = {"set": key, "label": label, "k": k, "chains": sorted(chains),
                                  "measures": summarize(chains, commission if k == 89 else None)}
            print(f"{key} k={k}: chains {sorted(chains)}", flush=True)
    if a.out_json:
        Path(a.out_json).write_text(json.dumps(res, indent=1))
    if a.out_md:
        Path(a.out_md).write_text(render(res))
    return res


def fmt(x, col):
    if col in ("efficiency_gap", "mean_median", "declination"):
        return f"{x:+.4f}"
    if col == "seats_at_50_50":
        return f"{100 * x:.2f}%"
    if col in ("city_gap_pct",):
        return f"{x:+.1f}%"
    if col == "population_mad":
        return f"{x:,.0f}"
    return f"{x:g}"


def render(res):
    lines = []
    for name, r in res.items():
        lines.append(f"### Set {r['set']}, {r['k']} districts: {r['label']}\n")
        lines.append(f"Chains {', '.join(map(str, r['chains']))}.\n")
        cols = "| Measure | Plans | n_eff | Status | n_eff, no cap (diagnostic) | 5th | Median | 95th |"
        sep = "|---|---|---|---|---|---|---|---|"
        if r["k"] == 89:
            cols += " Majority | Minority |"
            sep += "---|---|"
        lines += [cols, sep]
        for col, m in r["measures"].items():
            neff = f"{m['n_eff']:,.0f}" + (" (cap)" if m["lag_cap_bound"] else "")
            row = f"| {col} | {m['n_plans']:,} | {neff} | {m['status']} | {m['n_eff_uncapped_diagnostic']:,.0f} | {fmt(m['q05'], col)} | {fmt(m['q50'], col)} | {fmt(m['q95'], col)} |"
            if r["k"] == 89:
                for mp in ("majority_2026", "minority_2026"):
                    e = m.get(mp)
                    if e:
                        flag = " **flag**" if e.get("flag") else ""
                        row += f" {fmt(e['value'], col)} (p{e['pct']:.1f}){flag} |"
                    else:
                        row += " — |"
            lines.append(row)
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--real", required=True)
    ap.add_argument("--out-json")
    ap.add_argument("--out-md")
    main(ap.parse_args())
