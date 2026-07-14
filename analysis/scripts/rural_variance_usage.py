# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Rural variance-usage test — the minority's second charge, executed.

MOTIVATION. The minority report (p. 356) charges that the ±25% population
variance "is a deliberate instruction," that the majority's approach
"privilege[s] population parity," and that "to decline to use that range,
particularly in rural Alberta, diminishes one of the Act's central
safeguards." The measurable claim: the majority under-uses the permitted
below-average variance for rural divisions relative to the minority.

STATUS: EXPLORATORY (in-session, same standard as rural_division_count.py).

HYPOTHESES — FROZEN IN THIS HEADER BEFORE FIRST EXECUTION (2026-07-14):
  H-charge (the minority's prediction): rural-anchored divisions sit closer
    to the provincial mean on the majority map than on the minority map —
    i.e. the majority's mean rural deviation is nearer zero and its rural
    divisions make less use of the permitted negative range.
  H-null: rural deviation profiles are similar across the two maps.
  Descriptive output; no invented threshold; reported whichever way it cuts.

METHOD. Commission-published per-ED populations (the same tables both
reports print) joined to the rural/urban name classifier from
rural_division_count.py (both variants). For each map: mean and minimum
deviation-from-provincial-mean among rural-anchored divisions, the count
below −10% (meaningful use of the range), and the count of s.15(2)-scale
(≤ −25%) divisions.

Backward:
  data/reference/majority_2026_populations.csv, data/reference/minority_2026_populations.csv
  analysis/scripts/rural_division_count.py — classifier
Forward:
  findings/rural_variance_usage.md (results recorded in
  findings/rural_division_count.md's companion section if merged)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
from rural_division_count import is_rural, is_rural_corrected  # noqa: E402

FILES = {
    "majority_2026": ROOT / "data/reference/majority_2026_populations.csv",
    "minority_2026": ROOT / "data/reference/minority_2026_populations.csv",
}


def analyse(path: Path, rule) -> dict:
    df = pd.read_csv(path)
    name_col = next(c for c in df.columns if "name" in c.lower() or "district" in c.lower() or "division" in c.lower())
    pop_col = next(c for c in df.columns if "pop" in c.lower())
    mean_pop = df[pop_col].mean()
    df["dev_pct"] = (df[pop_col] - mean_pop) / mean_pop * 100
    rural = df[df[name_col].map(rule)]
    return {
        "n_rural": int(len(rural)),
        "mean_rural_dev_pct": round(float(rural["dev_pct"].mean()), 2),
        "min_rural_dev_pct": round(float(rural["dev_pct"].min()), 2),
        "rural_below_minus10": int((rural["dev_pct"] < -10).sum()),
        "rural_below_minus25": int((rural["dev_pct"] <= -25).sum()),
        "mean_abs_rural_dev_pct": round(float(rural["dev_pct"].abs().mean()), 2),
    }


def main() -> None:
    out = {}
    for rule_name, rule in (("frozen_rule", is_rural), ("corrected_rule", is_rural_corrected)):
        out[rule_name] = {k: analyse(p, rule) for k, p in FILES.items()}
    dest = ROOT / "findings" / "rural_variance_usage.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    for rule_name, block in out.items():
        print(f"==== {rule_name} ====")
        for k, r in block.items():
            print(f"{k}: n_rural={r['n_rural']} mean_dev={r['mean_rural_dev_pct']}% "
                  f"min={r['min_rural_dev_pct']}% below-10%={r['rural_below_minus10']} "
                  f"below-25%={r['rural_below_minus25']} mean_abs={r['mean_abs_rural_dev_pct']}%")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
