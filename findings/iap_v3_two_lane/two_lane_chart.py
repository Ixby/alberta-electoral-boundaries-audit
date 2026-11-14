# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
two_lane_chart.py

The two-lane scorecard chart with the panel's map beside the two commission maps, on the
registered November battery (spec v1.2 §3: S1-S6 midpoint flags, P1-P4), not on Act I's
April battery that the public chart (article_figures.build_bias_structure_matrix) uses. Act I's
tests were set by comparing the two commission maps and have no rule for scoring a third map;
§3's midpoint rule was written for exactly that. On §3 the minority is 5 of 5 (anchoring counts
there: 71.8% against a 76.0% midpoint), where Act I counts it 4 of 5.

Unregistered sensitivity; the panel's map is the v3 reconstruction, not an official shapefile.
Draft only: not wired into the report or the viewer.

Reads   findings/iap_v3_two_lane/structural.json, structural_majority_rerun.json,
        structural_minority_rerun.json, structural_2019_rerun.json, joint_outlier.json
        data/outputs/simulated_ensemble_percentiles_canonical.csv
Writes  findings/iap_v3_two_lane/two_lane_chart.svg (+ .png)

Usage: python findings/iap_v3_two_lane/two_lane_chart.py
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis/scripts"))
from palette import MAJORITY_TEAL, MINORITY_PURPLE, NEUTRAL_2019, NDP_ORANGE, UCP_BLUE, TEXT_DARK, INK_SUBTLE, PAPER_BG  # noqa: E402

PANEL = "#8A6D1F"  # ochre: a third map, outside both commission palettes


def flags(f):
    return json.loads((HERE / f).read_text())["structural_lane_flags"]


def p_flags(pct):
    """P1 EG >= +4.10%; P2, P4 >= p95 UCP direction; P3 declination in either tail (spec §3)."""
    return int(pct["eg"] >= 0.041) + int(pct["mm"] >= 95) + int(pct["decl"] >= 95 or pct["decl"] <= 5) + int(pct["s50"] >= 95)


def main():
    c = pd.read_csv(ROOT / "data/outputs/simulated_ensemble_percentiles_canonical.csv")
    rows = {}
    for key, name in (("2019 enacted", "2019 enacted"), ("majority 2026 canonical", "Majority 2026"),
                      ("minority 2026 canonical", "Minority 2026")):
        g = c[c["map"] == key].set_index("metric")
        rows[name] = {"eg": g.loc["efficiency_gap", "value"], "mm": g.loc["mean_median", "percentile"],
                      "decl": g.loc["declination", "percentile"], "s50": g.loc["seats_at_50_50", "percentile"]}
    m = json.loads((HERE / "joint_outlier.json").read_text())["maps"]["candidate"]["marginals"]
    rows["Panel's map (reconstructed)"] = {
        "eg": m["efficiency_gap"]["observed"], "mm": 100 * m["mean_median"]["ucp_direction_percentile"],
        "decl": 100 * m["declination"]["ucp_direction_percentile"],
        "s50": 100 * m["seats_at_50_50"]["ucp_direction_percentile"]}
    rows["2019 enacted"]["s"] = flags("structural_2019_rerun.json")
    rows["Majority 2026"]["s"] = flags("structural_majority_rerun.json")
    rows["Minority 2026"]["s"] = flags("structural_minority_rerun.json")
    rows["Panel's map (reconstructed)"]["s"] = flags("structural.json")
    for n, r in rows.items():
        r["p"] = p_flags(r)
        print(f"{n}: EG {100 * r['eg']:+.2f}%  structural {r['s']} of 5  partisan {r['p']} of 4")

    plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                         "font.sans-serif": ["Arial", "DejaVu Sans"], "figure.facecolor": PAPER_BG,
                         "axes.facecolor": "none", "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(7.2, 5.6), dpi=300)
    fig.subplots_adjust(top=0.82, bottom=0.17, left=0.13, right=0.97)
    XMIN, XMAX, YMIN, YMAX = -7, 7, -0.6, 5.7
    ax.axvline(4.10, color="#777777", lw=1.1, ls="--", zorder=1)
    ax.axhline(2.5, color="#777777", lw=1.1, ls="--", zorder=1)
    ax.text(4.25, 1.4, "P1 line, +4.10%:\nabout 1 in 20 of the\naudit's neutral\nsimulations tilts\nfurther (an audit\n"
            "calibration, not\na legal line)", color="#555555", fontsize=7, style="italic", ha="left", va="top")
    ax.text(XMIN + 0.12, 2.58, "3 of 5 = structural signature replicated (registered rule, spec §3)",
            color="#555555", fontsize=7, style="italic", ha="left", va="bottom")

    style = {"2019 enacted": (NEUTRAL_2019, (3.7, 0.45), "right"),
             "Majority 2026": (MAJORITY_TEAL, (-0.5, 0.45), "right"),
             "Minority 2026": (MINORITY_PURPLE, (3.3, 3.3), "right"),
             "Panel's map (reconstructed)": (PANEL, (-0.6, 3.25), "right")}
    for n, r in rows.items():
        col, xy, ha = style[n]
        x, y = 100 * r["eg"], r["s"]
        hollow = n.startswith("Panel")
        ax.scatter(x, y, s=320, c="white", edgecolors="white", linewidths=2.5, zorder=3)
        ax.scatter(x, y, s=240, c="white" if hollow else col, edgecolors=col if hollow else TEXT_DARK,
                   linewidths=2.2 if hollow else 1.4, zorder=4)
        ax.annotate(f"{n}\n{x:+.1f}% / {y} of 5 structural\n{r['p']} of 4 partisan flags",
                    xy=(x, y), xytext=xy, fontsize=8.5, fontweight="bold", color=col, ha=ha, va="bottom",
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.9, shrinkA=0, shrinkB=7), zorder=5)

    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_xticks(range(-6, 7, 2))
    ax.set_xticklabels([f"{v:+d}%" if v else "0%" for v in range(-6, 7, 2)], fontsize=8.5)
    ax.set_yticks(range(6))
    ax.set_xlabel("Partisan tilt: the efficiency gap\nfurther right = the map favours the UCP more",
                  fontsize=9.5, color=TEXT_DARK, labelpad=8)
    ax.set_ylabel("Structural flags, out of 5 (S1-S3, S5, S6)\nhigher = closer to the minority map",
                  fontsize=9.5, color=TEXT_DARK, labelpad=8)
    ax.spines["bottom"].set_visible(False)
    bx = ax.get_xaxis_transform()
    ax.plot([XMIN, 0], [0, 0], transform=bx, color=NDP_ORANGE, lw=1.2, clip_on=False, zorder=10)
    ax.plot([0, XMAX], [0, 0], transform=bx, color=UCP_BLUE, lw=1.2, clip_on=False, zorder=10)
    ax.set_title("The panel's map beside the 2019 map and the commission maps, on the registered two lanes",
                 fontsize=12, fontweight="bold", loc="left", color=TEXT_DARK, pad=50)
    ax.text(0.0, 1.03, "November scoring spec §3: each structural flag fires on the minority's side of the midpoint\n"
            "between the commission maps. These are the audit's tests, not Recommendation 5. Dashed lines are its own\n"
            "calibrations, not legal thresholds.",
            transform=ax.transAxes, fontsize=8, color="#555555", ha="left", va="bottom")
    ax.text(0.0, -0.17, "Hollow point: the panel's map is reconstructed from its report's pages (v3), not an official "
            "shapefile; provisional,\nunregistered sensitivity. Its seats at 50/50 is ranked against 87-district plans, "
            "as registered.\n2019 fires S3 and S5 here (0 of 5 on the public chart's April tests); these midpoints were set between "
            "the 2026 maps, and S6 asks about\n2026 patterns only.", transform=ax.transAxes, fontsize=7, color=INK_SUBTLE, style="italic", ha="left", va="top")
    for ext in ("svg", "png"):
        fig.savefig(HERE / f"two_lane_chart.{ext}", dpi=200 if ext == "png" else 300, facecolor=PAPER_BG,
                    bbox_inches="tight", pad_inches=0.1)


if __name__ == "__main__":
    main()
