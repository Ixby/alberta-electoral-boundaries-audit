# Per-ED vote totals for the map explorer's ED tooltip.
#
# Output: viewer/static/mapdata/ed_totals.json
#   { "minority": {ed_name: {"total": n, "anywhere": false}},
#     "majority": {...},
#     "2019":     {ed_name: {"total": n, "anywhere": true}} }
#
# Attribution honesty:
#  - 2026 proposal EDs (minority/majority): "total" is the ELECTION-DAY
#    (in-person) total only — the sum of the ED's voting-area votes. Advance /
#    Vote Anywhere / Special / Mobile ballots are reported by Elections Alberta
#    only at the 2019-ED level and have no voting-area geometry, so they cannot
#    be attributed to the new proposal districts. anywhere=false.
#  - 2019 enacted EDs: every ballot is attributable (each poll carries its
#    ed_2019), so "total" is the FULL count across all ballot types.
#    anywhere=true.
#
# In-person per-ED totals come from the same VA data the explorer renders
# (va_props.json + valabels_<map>.json), so the ED total equals the sum of the
# poll figures shown in the tooltip. The 2019 all-ballot total comes from
# data/outputs/polls_2023_unified.csv (ed_2019 column).
import json, collections
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
MAPDATA = REPO / "viewer" / "static" / "mapdata"

va_props = json.loads((MAPDATA / "va_props.json").read_text(encoding="utf-8"))

def inperson_by_ed(label_file: str) -> dict:
    labels = json.loads((MAPDATA / label_file).read_text(encoding="utf-8"))
    tot = collections.defaultdict(int)
    for i, ed in enumerate(labels):
        if ed:
            p = va_props[i]
            tot[ed] += int(p.get("votes", 0)) if isinstance(p, dict) else 0
    return dict(tot)

out = {
    "minority": {n: {"total": v, "anywhere": False} for n, v in inperson_by_ed("valabels_minority.json").items()},
    "majority": {n: {"total": v, "anywhere": False} for n, v in inperson_by_ed("valabels_majority.json").items()},
}

# 2019: full all-ballot total per ed_2019 from the unified polls file.
polls = pd.read_csv(REPO / "data" / "outputs" / "polls_2023_unified.csv", encoding="latin-1")
full_2019 = polls.groupby("ed_2019")["valid_votes"].sum().astype(int).to_dict()
ip_2019 = inperson_by_ed("valabels_2019.json")
ed19 = {}
for n in ip_2019:
    if n in full_2019:
        ed19[n] = {"total": int(full_2019[n]), "anywhere": True}
    else:
        # name not in the polls file (e.g. a spelling variant) — fall back to the
        # in-person sum so the ED still shows a grounded number, flagged honestly.
        ed19[n] = {"total": int(ip_2019[n]), "anywhere": False}
        print(f"[build_ed_totals] 2019 ED '{n}' absent from polls ed_2019; using in-person total only")
out["2019"] = ed19

(MAPDATA / "ed_totals.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
print(f"[build_ed_totals] wrote ed_totals.json — minority {len(out['minority'])}, majority {len(out['majority'])}, 2019 {len(out['2019'])} EDs")
