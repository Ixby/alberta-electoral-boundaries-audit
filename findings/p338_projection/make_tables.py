"""make_tables.py -- turns out/results.json and out/districts_*.csv into the markdown tables used in
README.md (written to out/tables.md). Run after simulate_338.py: python3 -I make_tables.py"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
r = json.loads((OUT / "results.json").read_text())
LAB = {"map2019": "2019 enacted (87)", "majority": "Commission majority (89)", "minority": "Commission minority (89)",
       "panel": "Advisory panel, reconstructed (91)", "para167": "Panel minority ¶167, reconstructed (91)"}
AUD = {"map2019": "2019_enacted", "majority": "majority_2026", "minority": "minority_2026", "panel": "iap_2026_assembled",
       "para167": "para167_map"}
pct = lambda x: f"{100 * x:.0f}%"


def sg(x, nd=0):
    """Signed number with a real minus sign and no negative zero."""
    v = round(float(x), nd)
    if v == 0:
        return "0"
    t = f"{abs(v):.{nd}f}"
    return ("+" if v > 0 else "\u2212") + t


L = []

# 2023 check
L.append("### 2023 check (all ballots)\n\n| Map | UCP seats, audit | UCP seats, here | Within 2 / 4 pts, audit | here | Seats at 50/50, audit | here |\n|---|---:|---:|---:|---:|---:|---:|")
for k, v in r["check_2023"].items():
    a, o = v["audit"], v["ours"]
    L.append(f"| {LAB[k]} | {a['ucp_seats']} | {o['ucp']} | {a['close2']} / {a['close4']} | {o['close2']} / {o['close4']} | "
             f"{a['seats_at_50_50']:.4f} | {o['seats_at_50_50_share']:.4f} |")

# point projection
L.append("\n### Point projection\n\n| Map | Seats | Majority needs | UCP | NDP | Tied | UCP / NDP seat share | Within 4 pts | Within 2 pts | Within 1 pt | Result |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
for k, v in r["point"].items():
    t = v["proportional"]
    d = pd.read_csv(OUT / f"districts_{k}.csv")
    c1 = int((d.ucp_minus_ndp_pts_twoparty.abs() <= 1).sum())
    res = "UCP majority" if t["ucp"] >= t["need"] else "NDP majority" if t["ndp"] >= t["need"] else "hung"
    L.append(f"| {LAB[k]} | {t['n']} | {t['need']} | {t['ucp']} | {t['ndp']} | {t['tie']} | {pct(t['ucp'] / t['n'])} / {pct(t['ndp'] / t['n'])} | "
             f"{t['close4']} | {t['close2']} | {c1} | {res} |")

# MC per map
m = r["mc"]["main"]["maps"]
L.append("\n### Monte Carlo, 5,000 draws\n\n| Map | UCP seats, median (5th–95th) | NDP seats, median (5th–95th) | P(UCP majority) | P(NDP majority) | P(hung) |\n|---|---:|---:|---:|---:|---:|")
for k, v in m.items():
    L.append(f"| {LAB[k]} | {v['ucp_median']:.0f} ({v['ucp_p05_p95'][0]:.0f}–{v['ucp_p05_p95'][1]:.0f}) | "
             f"{v['ndp_median']:.0f} ({v['ndp_p05_p95'][0]:.0f}–{v['ndp_p05_p95'][1]:.0f}) | {pct(v['p_ucp_majority'])} | "
             f"{pct(v['p_ndp_majority'])} | {pct(v['p_hung'])} |")

# lead needed and 50/50
L.append("\n### What it takes\n\n| Map | UCP lead needed for a UCP majority (pts) | UCP seats at a 50/50 vote, this projection | Same, audit (2023 all ballots) |\n|---|---:|---:|---:|")
for k, v in r["lead_needed"].items():
    t = r["point"][k]["proportional"]
    a = r["check_2023"][k]["ours"]
    L.append(f"| {LAB[k]} | {sg(v['ucp_majority_from_lead_pts'], 1)} | {t['seats_at_50_50_ucp']:.0f} of {t['n']} ({pct(t['seats_at_50_50_share'])}) | "
             f"{a['seats_at_50_50_ucp']:.0f} of {a['n']} ({pct(a['seats_at_50_50_share'])}) |")

# pairs
P = r["mc"]["main"]["pairs"]
order = [("panel", "majority"), ("panel", "map2019"), ("minority", "majority"), ("para167", "panel"),
         ("majority", "map2019"), ("minority", "map2019"), ("minority", "panel"), ("para167", "majority"), ("para167", "map2019"),
         ("minority", "para167")]


def pair(a, b):
    key, sgn = (f"{a}_vs_{b}", 1) if f"{a}_vs_{b}" in P else (f"{b}_vs_{a}", -1)
    p = P[key]
    q = lambda med, rng: (sgn * med, sorted([sgn * rng[0], sgn * rng[1]]))
    du, ru = q(p["ucp_seat_diff_median"], p["ucp_seat_diff_p05_p95"])
    dl, rl = q(p["ucp_lead_diff_median"], p["ucp_lead_diff_p05_p95"])
    a_only = p["p_ucp_maj_on_first_only"] if sgn == 1 else p["p_ucp_maj_on_second_only"]
    b_only = p["p_ucp_maj_on_second_only"] if sgn == 1 else p["p_ucp_maj_on_first_only"]
    return du, ru, dl, rl, p["p_government_differs"], a_only, b_only


short = {"map2019": "2019", "majority": "majority", "minority": "minority", "panel": "panel", "para167": "¶167"}
L.append("\n### Map against map, same draws (first map minus second)\n\n| Comparison | UCP seats: median (5th–95th) | UCP seat lead over NDP: median (5th–95th) | Draws with a different government | of which UCP majority only on first / only on second |\n|---|---:|---:|---:|---:|")
for a, b in order:
    du, ru, dl, rl, f, ao, bo = pair(a, b)
    L.append(f"| {short[a]} − {short[b]} | {sg(du)} ({sg(ru[0])} to {sg(ru[1])}) | {sg(dl)} ({sg(rl[0])} to {sg(rl[1])}) | "
             f"{100 * f:.1f}% | {100 * ao:.1f}% / {100 * bo:.1f}% |")

# robustness
L.append("\n### Robustness: same draws, different assumptions\n\n| Variant | P(UCP maj.) 2019 | majority | minority | panel | ¶167 | Different govt: panel vs majority | panel vs 2019 | minority vs majority |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|")
names = {"main": "Main (proportional swing)", "additive_swing": "Additive swing", "no_riding_noise": "No riding noise",
         "riding_noise_x1.5": "Riding noise × 1.5", "ranges_as_95pct": "338 ranges read as 95% intervals",
         "riding_noise_x0.5": "Riding noise × 0.5"}
for v, x in r["mc"].items():
    mm, pp = x["maps"], x["pairs"]
    L.append(f"| {names[v]} | " + " | ".join(pct(mm[k]["p_ucp_majority"]) for k in LAB) + " | "
             + " | ".join(f"{100 * pp[k]['p_government_differs']:.1f}%" for k in ("majority_vs_panel", "map2019_vs_panel", "majority_vs_minority")) + " |")
d = r["mc"]["main"]["diagnostics"]
L.append(f"\nMain run: provincial lead s.d. {d['sd_prov_lead_pts']:.2f} pts; riding s.d. median {d['sd_riding_lead_pts_median']:.2f} "
         f"(range {d['sd_riding_lead_pts_range'][0]:.2f}–{d['sd_riding_lead_pts_range'][1]:.2f}); provincial UCP lead across draws "
         f"5th/50th/95th: {sg(d['provincial_lead_pct']['5'], 1)} / {sg(d['provincial_lead_pct']['50'], 1)} / {sg(d['provincial_lead_pct']['95'], 1)}; "
         f"third-party seat wins: {d['other_party_wins']}; riding targets clipped: {d['riding_targets_clipped_share']:.4f}.")
(OUT / "tables.md").write_text("\n".join(L) + "\n", encoding="utf8")
print("\n".join(L))
