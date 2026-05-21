"""Add per-district efficiency-gap contribution to the three ed_hover_*.json files.

EG contribution (district i):
  threshold_i  = (ucp_i + ndp_i) / 2
  wasted_ndp_i = ndp_i  if UCP wins, else ndp_i - threshold_i
  wasted_ucp_i = ucp_i  if NDP wins, else ucp_i - threshold_i
  eg_i         = (wasted_ndp_i - wasted_ucp_i) / V_province

Positive eg_i → UCP-favoured district.  Negative → NDP-favoured.

Output field: "eg" (float, 4 decimal places, units = fraction of province vote).
Existing fields are preserved; file is rewritten in-place.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
HOVER_DIR = REPO / "docs" / "data"

FILES = {
    "minority": HOVER_DIR / "ed_hover_minority.json",
    "majority": HOVER_DIR / "ed_hover_majority.json",
    "2019":     HOVER_DIR / "ed_hover_2019.json",
}


def compute_eg(records: list[dict]) -> list[dict]:
    # Province total (2-party only — standard Stephanopoulos-McGhee)
    V = sum(r["ucp_votes"] + r["ndp_votes"] for r in records)
    if V == 0:
        return records

    out = []
    for r in records:
        ucp, ndp = r["ucp_votes"], r["ndp_votes"]
        total = ucp + ndp
        threshold = total / 2

        if ucp >= ndp:          # UCP wins
            wasted_ucp = ucp - threshold
            wasted_ndp = float(ndp)
        else:                   # NDP wins
            wasted_ndp = ndp - threshold
            wasted_ucp = float(ucp)

        eg = (wasted_ndp - wasted_ucp) / V
        out.append({**r, "eg": round(eg, 4)})
    return out


def main() -> None:
    for key, path in FILES.items():
        if not path.exists():
            print(f"SKIP {key}: {path} not found")
            continue
        records = json.loads(path.read_text(encoding="utf-8"))
        enriched = compute_eg(records)
        path.write_text(json.dumps(enriched, ensure_ascii=False, separators=(",", ":")),
                        encoding="utf-8")
        total_eg = sum(r["eg"] for r in enriched)
        print(f"{key}: {len(enriched)} districts, sum_EG = {total_eg:.4f}")


if __name__ == "__main__":
    main()
