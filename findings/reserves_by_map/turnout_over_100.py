# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
turnout_over_100.py
-------------------
Every 2026 referendum election-day voting area whose ballots exceed its electors on the list, in all
87 divisions (inputs/referendum2026_q10_ed*.xlsx, Question 10). Each case is placed in one of three
kinds, tested in this order:

- combined count: Elections Alberta reports that at 14 locations the voting areas' ballots could not be
  separated, so the whole place's ballots sit under the first area and the others show zero. A case
  is this kind when another area at the same place shows electors and zero ballots.
- same place, areas mixed: the place has several areas and its turnout over all of them is at or
  under 100%.
- the whole place over 100%: the place's ballots exceed its electors on the list.

Ballots = valid + spoiled + declined + rejected. Descriptive, exploratory, not registered.
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _xlsx import rows  # noqa: E402


def num(x):
    return float(x) if x not in ("", None) else 0.0


def main():
    n_areas, cases = 0, []
    for f in sorted(HERE.glob("inputs/referendum2026_q10_ed*.xlsx"), key=lambda p: int(re.search(r"ed(\d+)", p.name).group(1))):
        allrows = list(rows(f))
        ed = allrows[2][0]
        areas = [r for r in allrows if len(r) >= 11 and r[2] == "Election Day"]
        n_areas += len(areas)
        byplace = collections.defaultdict(list)
        for r in areas:
            byplace[r[1]].append(r)
        for place, rs in byplace.items():
            cast = {r[0]: num(r[6]) + num(r[7]) + num(r[8]) + num(r[9]) for r in rs}
            el = {r[0]: num(r[3]) for r in rs}
            place_turnout = 100 * sum(cast.values()) / sum(el.values()) if sum(el.values()) else None
            zero = [a for a in el if el[a] > 0 and cast[a] == 0]
            for r in rs:
                a = r[0]
                if el[a] > 0 and cast[a] > el[a]:
                    kind = ("combined count" if zero else
                            "same place, areas mixed" if len(rs) > 1 and place_turnout <= 100 else
                            "the whole place over 100%")
                    o1, o2 = num(r[4]), num(r[5])
                    cases.append({"division": ed, "voting_area": a, "voting_place": place.strip(), "electors_on_list": int(el[a]),
                                  "ballots": int(cast[a]), "turnout_pct": round(100 * cast[a] / el[a], 1),
                                  "place_areas": len(rs), "place_turnout_pct": round(place_turnout, 1),
                                  "zero_ballot_areas_at_place": zero, "kind": kind,
                                  "remain_pct": round(100 * o1 / (o1 + o2), 1) if o1 + o2 else None})
    out = {"election_day_voting_areas": n_areas, "over_100": len(cases),
           "by_kind": dict(collections.Counter(c["kind"] for c in cases)),
           "cases": sorted(cases, key=lambda c: (c["kind"], -c["turnout_pct"]))}
    (HERE / "turnout_over_100.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("election_day_voting_areas", "over_100", "by_kind")}))
    for c in out["cases"]:
        print(c["kind"], "|", c["division"], c["voting_area"], c["voting_place"], c["turnout_pct"], "place", c["place_turnout_pct"], "remain", c["remain_pct"])


if __name__ == "__main__":
    main()
