#!/usr/bin/env python3
"""polls_338.py -- the four polls 338Canada listed, their simple average, and 338's projection.

EXPLORATORY. Computed after the fact for the 2026-11-10 audit. Not a registered test.

Input : evidence/projections/338canada_2026-10-19/provincial_summary.txt
Output: findings/audit_2026-11-10/polls_338.json
Run   : python findings/audit_2026-11-10/polls_338.py   (from anywhere; no network, no randomness)

The input is the text of 338Canada's Alberta page as fetched on 2026-11-09. It prints each
poll as: firm, date, then two or three bare numbers with NO party labels. This script reads
the first number as UCP and the second as NDP. That order is the order of the page's own
projection block lower in the same file (UCP first, NDP second) and of the page's table
header as the auditors re-read it (UCP, NDP, ...); the header itself is not in the committed
file. A third number, when present, is another party and is kept unlabelled.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "evidence/projections/338canada_2026-10-19/provincial_summary.txt"
OUT = Path(__file__).resolve().with_suffix(".json")


def main():
    lines = [ln.strip() for ln in SRC.read_text(encoding="utf-8").splitlines() if ln.strip()]
    start = lines.index("Latest Alberta Polls") + 1
    end = next(i for i, ln in enumerate(lines) if ln.startswith("©"))
    polls, cur = [], None
    for ln in lines[start:end]:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", ln):
            cur["date"] = ln
        elif re.fullmatch(r"\d+(\.\d+)?", ln):
            cur["numbers_as_printed"].append(float(ln) if "." in ln else int(ln))
        else:
            cur = {"firm": ln, "date": None, "numbers_as_printed": []}
            polls.append(cur)
    for p in polls:
        n = p["numbers_as_printed"]
        assert len(n) >= 2 and p["date"], p
        p["ucp_pct"], p["ndp_pct"] = n[0], n[1]
        p["ucp_lead_pts"] = n[0] - n[1]
        p["third_number_unlabelled"] = n[2] if len(n) > 2 else None
    assert len(polls) == 4, polls

    # 338's projection block: three numbers (low, high, point) before "± 5%" and the party name.
    proj = {}
    for party in ("UCP", "NDP"):
        i = max(j for j, ln in enumerate(lines) if ln == party)
        assert lines[i - 1].startswith("±"), lines[i - 4:i + 1]
        low, high, point = (int(lines[i - k].rstrip("%")) for k in (4, 3, 2))
        proj[party] = {"point_pct": point, "low_pct": low, "high_pct": high, "band": lines[i - 1]}
    update = next(ln for ln in lines if ln.startswith("Latest update:")).split(":", 1)[1].strip()

    n = len(polls)
    avg_ucp = sum(p["ucp_pct"] for p in polls) / n
    avg_ndp = sum(p["ndp_pct"] for p in polls) / n
    out = {
        "status": "EXPLORATORY - computed after the fact for the 2026-11-10 audit; not a registered test",
        "source": str(SRC.relative_to(ROOT)),
        "party_order_note": (
            "The committed file has no party labels on the poll numbers. First number is read as UCP, "
            "second as NDP (the order of the projection block in the same file, and of the page's table "
            "header as re-read by the auditors on 2026-11-10; the header is not in the repository)."
        ),
        "polls": polls,
        "polls_simple_average": {
            "n_polls": n,
            "ucp_pct": round(avg_ucp, 2),
            "ndp_pct": round(avg_ndp, 2),
            "ucp_lead_pts": round(avg_ucp - avg_ndp, 2),
            "date_range": [min(p["date"] for p in polls), max(p["date"] for p in polls)],
            "method": "unweighted mean of the four listed polls; no weighting by date, sample size or firm",
        },
        "projection_338": {
            "latest_update": update,
            "ucp": proj["UCP"],
            "ndp": proj["NDP"],
            "ucp_lead_pts": proj["UCP"]["point_pct"] - proj["NDP"]["point_pct"],
            "what_it_is": "338Canada's modelled popular-vote projection, not a poll and not a poll average",
        },
        "projection_minus_poll_average": {
            "ucp_pts": round(proj["UCP"]["point_pct"] - avg_ucp, 2),
            "ndp_pts": round(proj["NDP"]["point_pct"] - avg_ndp, 2),
            "lead_pts": round((proj["UCP"]["point_pct"] - proj["NDP"]["point_pct"]) - (avg_ucp - avg_ndp), 2),
        },
        "polls_with_ndp_ahead_or_tied": [p["firm"] for p in polls if p["ndp_pct"] >= p["ucp_pct"]],
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out["polls_simple_average"]), json.dumps(out["projection_338"]["ucp_lead_pts"]))


if __name__ == "__main__":
    main()
