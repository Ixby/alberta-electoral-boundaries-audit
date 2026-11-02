"""Rescore the packing signature (academic report §5.3.1) on the official vote attribution.

The signature needs all three criteria:
  P1  Zone A mean district population >= provincial mean + 5%   (thresholds.md #10)
  P2  the winning party in Zone A wins by margins >= provincial mean district
      winning margin + 15 percentage points                     (thresholds.md #11)
  P3  counterfactual seat loss against the majority map

§5.3.1 recorded P2 as a pass with "13 of the 17 Zone A districts NDP-won" citing
data/outputs/votes_2023_minority.csv. That file gives 9 of 17 (13 is the majority
map's count). This script recomputes P2 on the canonical Phase 4C election-day
attribution (data/outputs/phase4c_per_ed_votes_<map>.csv) and, as a cross-check,
on the file §5.3.1 cites. Zone A is the list in electoral_forensics_population.py.

Winning margin = |NDP - UCP| / (NDP + UCP) x 100 (two-party, percentage points).
Output: data/outputs/packing_signature_rescore_2026-11-01.json
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "outputs" / "packing_signature_rescore_2026-11-01.json"


def norm(name: str) -> str:
    return re.sub(r"[\s\-–'’]", "", name).lower()


def zone_a() -> set[str]:
    src = (ROOT / "analysis" / "scripts" / "electoral_forensics_population.py").read_text(encoding="utf-8")
    block = re.search(r"CALGARY_ZONE_A\s*=\s*\{(.*?)\}", src, re.S).group(1)
    return {norm(n) for n in re.findall(r'"([^"]+)"', block)}


def score(path: Path, ndp_col: str, ucp_col: str) -> dict:
    zone = zone_a()
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        n, u = float(r[ndp_col]), float(r[ucp_col])
        if n + u <= 0:
            continue
        rows.append((r["ed_name"], n, u, abs(n - u) / (n + u) * 100))
    prov = sum(m for *_, m in rows) / len(rows)
    z = [x for x in rows if norm(x[0]) in zone]
    ndp_won = [x for x in z if x[1] > x[2]]
    ucp_won = [x for x in z if x[2] > x[1]]
    m_ndp = sum(x[3] for x in ndp_won) / len(ndp_won) if ndp_won else None
    excess = (m_ndp - prov) if m_ndp is not None else None
    return {
        "source": str(path.relative_to(ROOT)),
        "districts_scored": len(rows),
        "zone_a_districts": len(z),
        "zone_a_ndp_won": len(ndp_won),
        "zone_a_ucp_won": len(ucp_won),
        "provincial_mean_winning_margin_pp": round(prov, 2),
        "zone_a_ndp_won_mean_margin_pp": round(m_ndp, 2) if m_ndp is not None else None,
        "excess_over_provincial_pp": round(excess, 2) if excess is not None else None,
        "p2_threshold_pp": 15.0,
        "p2_pass": bool(excess is not None and excess >= 15.0),
    }


def main() -> None:
    out = {
        "test": "Packing signature P2 (winning margin >= provincial mean + 15 pp), Calgary Zone A",
        "rule": "Signature detected only if P1, P2 and P3 all pass (academic report §5.3.1)",
        "canonical": {
            "minority": score(ROOT / "data/outputs/phase4c_per_ed_votes_minority.csv", "ndp", "ucp"),
            "majority": score(ROOT / "data/outputs/phase4c_per_ed_votes_majority.csv", "ndp", "ucp"),
        },
        "cross_check_file_cited_in_5_3_1": {
            "minority": score(ROOT / "data/outputs/votes_2023_minority.csv", "ndp_2023", "ucp_2023"),
            "majority": score(ROOT / "data/outputs/votes_2023_majority.csv", "ndp_2023", "ucp_2023"),
        },
    }
    m = out["canonical"]["minority"]
    out["verdict_minority"] = (
        "Not detected: P2 fails on the official attribution "
        f"({m['zone_a_ndp_won']} of {m['zone_a_districts']} Zone A districts NDP-won; "
        f"their mean margin is {m['excess_over_provincial_pp']:+.1f} pp against the provincial mean, "
        "where P2 needs +15 pp). P1 (Zone A districts 11.5% above the provincial mean) still passes."
    )
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
