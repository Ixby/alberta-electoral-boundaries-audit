"""
T3.2 — Majority rural-isolation counter-test.

Pre-registered at:
  preregistration/t3_2_majority_rural_isolation_design.md

Closes TODO_REMEDIATION T3.2 ("one majority-anomaly counter-test"). Mirror-tests
the minority-derived neighbour-drain finding by asking whether the majority's
anomalously low drain score (z = -2.915 vs canonical ensemble) reflects engineered
rural isolation or natural Alberta geography.

Three metrics on each of {majority, minority, 2019 enacted}:
  R1  median Polsby-Popper across rural-anchored EDs (lower = more elongated)
  R2  mean count of urban-anchored neighbors per rural ED (lower = less contact)
  R3  fraction of rural EDs with zero urban-anchored neighbors (higher = more isolation)

Symmetric verdict per the design's §5 decision rule.

Backward:
  data/shapefiles/canonical/ea_majority_2026_eds.gpkg
  data/shapefiles/canonical/ea_minority_2026_eds.gpkg
  data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp
Forward:
  findings/t3_2_majority_rural_isolation.json
  findings/t3_2_majority_rural_isolation.md
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from statistics import median, mean
from typing import Sequence

import geopandas as gpd

ROOT = Path(__file__).resolve().parent.parent.parent

URBAN_PREFIXES: tuple[str, ...] = (
    "Calgary-", "Edmonton-", "Airdrie", "Lethbridge-", "Red Deer-",
    "Medicine Hat-", "St. Albert-", "Sherwood Park-",
    "Fort McMurray-", "Grande Prairie-", "Spruce Grove-",
)
# "Airdrie" (no hyphen) matches both "Airdrie-East" (majority, hyphen) and
# "Airdrie East" (minority, space); amended 2026-06-13 per T1.7 R2 S13.

CANONICAL_CRS = "EPSG:3400"

MAPS = {
    "majority_2026": {
        "path": ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg",
        "name_col": "EDName2025",
    },
    "minority_2026": {
        "path": ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg",
        "name_col": "EDName2025",
    },
    "enacted_2019": {
        "path": ROOT / "data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp",
        "name_col": "EDName2017",
    },
}


def is_rural(name: str) -> bool:
    return not any(name.startswith(p) for p in URBAN_PREFIXES)


def polsby_popper(area: float, perimeter: float) -> float:
    if perimeter <= 0:
        return float("nan")
    return (4 * math.pi * area) / (perimeter * perimeter)


def build_adjacency(gdf: gpd.GeoDataFrame, name_col: str) -> dict[str, set[str]]:
    """Queen contiguity: any non-zero shared boundary."""
    sindex = gdf.sindex
    adj: dict[str, set[str]] = {n: set() for n in gdf[name_col]}
    geoms = gdf.geometry.values
    names = gdf[name_col].values
    for i, g in enumerate(geoms):
        candidates = list(sindex.intersection(g.bounds))
        for j in candidates:
            if j <= i:
                continue
            if g.touches(geoms[j]) or g.intersects(geoms[j]):
                inter = g.intersection(geoms[j])
                if not inter.is_empty and inter.length > 0:
                    adj[names[i]].add(names[j])
                    adj[names[j]].add(names[i])
    return adj


def score_map(label: str, spec: dict) -> dict:
    gdf = gpd.read_file(spec["path"])
    if gdf.crs is None:
        raise RuntimeError(f"{label}: shapefile has no CRS")
    gdf = gdf.to_crs(CANONICAL_CRS)
    name_col = spec["name_col"]

    gdf["__is_rural"] = gdf[name_col].apply(is_rural)
    gdf["__area_m2"] = gdf.geometry.area
    gdf["__perim_m"] = gdf.geometry.length
    gdf["__pp"] = [polsby_popper(a, p) for a, p in zip(gdf["__area_m2"], gdf["__perim_m"])]

    adjacency = build_adjacency(gdf, name_col)
    rural_names = set(gdf.loc[gdf["__is_rural"], name_col])
    urban_names = set(gdf.loc[~gdf["__is_rural"], name_col])

    rural_rows = gdf[gdf["__is_rural"]].copy()
    n_rural = len(rural_rows)

    pp_rural = [v for v in rural_rows["__pp"].tolist() if not math.isnan(v)]
    r1_median_pp = median(pp_rural) if pp_rural else float("nan")

    urban_nbr_counts: list[int] = []
    rural_with_zero_urban = 0
    for name in rural_rows[name_col]:
        nbrs = adjacency[name]
        urban_nbrs = nbrs & urban_names
        urban_nbr_counts.append(len(urban_nbrs))
        if len(urban_nbrs) == 0:
            rural_with_zero_urban += 1

    r2_mean_urban_nbrs = mean(urban_nbr_counts) if urban_nbr_counts else float("nan")
    r3_zero_urban_frac = (rural_with_zero_urban / n_rural) if n_rural else float("nan")

    return {
        "label": label,
        "n_eds_total": int(len(gdf)),
        "n_rural_eds": int(n_rural),
        "n_urban_eds": int(len(urban_names)),
        "R1_median_pp_rural": round(r1_median_pp, 6),
        "R2_mean_urban_neighbors_per_rural_ed": round(r2_mean_urban_nbrs, 4),
        "R3_fraction_rural_with_zero_urban_neighbors": round(r3_zero_urban_frac, 4),
        "rural_eds": sorted(rural_names),
        "rural_urban_neighbor_counts": dict(zip(rural_rows[name_col].tolist(), urban_nbr_counts)),
    }


def rank_maps(scores: dict[str, dict]) -> dict:
    """Rank 1 = most isolated.

    R1 (median PP): lower = more isolated → ascending rank
    R2 (mean urban nbrs): lower = more isolated → ascending rank
    R3 (zero-urban-nbr fraction): higher = more isolated → descending rank
    """
    labels = list(scores.keys())

    def asc_rank(values: Sequence[float]) -> list[int]:
        order = sorted(range(len(values)), key=lambda i: values[i])
        ranks = [0] * len(values)
        for r, i in enumerate(order):
            ranks[i] = r + 1
        return ranks

    def desc_rank(values: Sequence[float]) -> list[int]:
        order = sorted(range(len(values)), key=lambda i: -values[i])
        ranks = [0] * len(values)
        for r, i in enumerate(order):
            ranks[i] = r + 1
        return ranks

    r1_vals = [scores[l]["R1_median_pp_rural"] for l in labels]
    r2_vals = [scores[l]["R2_mean_urban_neighbors_per_rural_ed"] for l in labels]
    r3_vals = [scores[l]["R3_fraction_rural_with_zero_urban_neighbors"] for l in labels]

    r1_ranks = asc_rank(r1_vals)
    r2_ranks = asc_rank(r2_vals)
    r3_ranks = desc_rank(r3_vals)

    table = {}
    for i, l in enumerate(labels):
        table[l] = {
            "R1_rank": r1_ranks[i],
            "R2_rank": r2_ranks[i],
            "R3_rank": r3_ranks[i],
            "mean_rank": round((r1_ranks[i] + r2_ranks[i] + r3_ranks[i]) / 3.0, 4),
        }
    return table


def verdict(scores: dict[str, dict], ranks: dict[str, dict]) -> dict:
    maj = "majority_2026"
    most_isolated_overall = min(ranks, key=lambda l: ranks[l]["mean_rank"])
    metrics_majority_first = sum(
        1
        for axis in ("R1_rank", "R2_rank", "R3_rank")
        if ranks[maj][axis] == 1
    )
    if most_isolated_overall == maj and metrics_majority_first >= 2:
        v = "H1_supported"
        narrative = (
            "Majority shows the most-isolated rural pattern overall and on "
            f"{metrics_majority_first} of 3 metrics. The drain anomaly is "
            "consistent with engineered rural isolation — a symmetric structural "
            "anomaly to the minority's drain/anchoring signature."
        )
    elif metrics_majority_first <= 1 and most_isolated_overall != maj:
        v = "H0_supported"
        narrative = (
            f"Majority is most-isolated on only {metrics_majority_first} of 3 "
            f"metrics and is not the most isolated map overall ({most_isolated_overall} is). "
            "The drain anomaly is consistent with natural Alberta rural geography, "
            "not engineered isolation."
        )
    else:
        v = "mixed"
        narrative = (
            f"Mixed result: majority is most-isolated on {metrics_majority_first} of 3 "
            f"metrics; overall most-isolated = {most_isolated_overall}. The drain "
            "anomaly remains partially characterized."
        )
    return {
        "decision": v,
        "majority_metrics_first_count": metrics_majority_first,
        "overall_most_isolated_map": most_isolated_overall,
        "narrative": narrative,
    }


def script_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def write_markdown(out_md: Path, scores: dict, ranks: dict, v: dict, commit: str) -> None:
    rows = ["majority_2026", "minority_2026", "enacted_2019"]
    lines = [
        "---",
        "name: t3_2_majority_rural_isolation",
        "date: 2026-06-11",
        "preregistration: preregistration/t3_2_majority_rural_isolation_design.md",
        "type: counter-test",
        "verdict: " + v["decision"],
        f"script_commit: {commit}",
        "---",
        "",
        "> **Backward:**",
        "> - `preregistration/t3_2_majority_rural_isolation_design.md` — pre-committed design",
        "> - `analysis/scripts/t3_2_majority_rural_isolation.py` — this analysis",
        "> - `findings/joint_outlier_score.json` — source of the majority drain anomaly motivating the test",
        ">",
        "> **Forward:**",
        "> - `reports/academic/report_academic.md` §5.6 — symmetry-of-test-selection audit (extend with this entry)",
        "> - `findings/README.md` — index",
        "",
        "# T3.2 — Majority rural-isolation counter-test (result)",
        "",
        "## Summary",
        "",
        v["narrative"],
        "",
        "## Per-map metric values",
        "",
        "| Map | n EDs | n rural | R1 median PP (rural) | R2 mean urban-nbrs/rural ED | R3 frac rural with 0 urban nbrs |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        s = scores[r]
        lines.append(
            f"| {r} | {s['n_eds_total']} | {s['n_rural_eds']} | "
            f"{s['R1_median_pp_rural']:.4f} | "
            f"{s['R2_mean_urban_neighbors_per_rural_ed']:.3f} | "
            f"{s['R3_fraction_rural_with_zero_urban_neighbors']:.3f} |"
        )
    lines += [
        "",
        "## Rank table (1 = most rural-isolated on the axis)",
        "",
        "| Map | R1 (median PP↓) | R2 (urban-nbrs↓) | R3 (zero-urban frac↑) | Mean rank |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        rk = ranks[r]
        lines.append(
            f"| {r} | {rk['R1_rank']} | {rk['R2_rank']} | {rk['R3_rank']} | {rk['mean_rank']:.3f} |"
        )
    lines += [
        "",
        "## Decision (per §5 of the pre-registered design)",
        "",
        f"- **Verdict:** `{v['decision']}`",
        f"- **Majority is rank-1 on:** {v['majority_metrics_first_count']} of 3 metrics",
        f"- **Overall most-isolated map:** {v['overall_most_isolated_map']}",
        "",
        v["narrative"],
        "",
        "## Reproducibility",
        "",
        "```bash",
        "python analysis/scripts/t3_2_majority_rural_isolation.py \\",
        "  --output-json findings/t3_2_majority_rural_isolation.json \\",
        "  --output-md   findings/t3_2_majority_rural_isolation.md",
        "```",
        "",
        f"Script commit: `{commit}`",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--output-json",
        type=Path,
        default=ROOT / "findings/t3_2_majority_rural_isolation.json",
    )
    ap.add_argument(
        "--output-md",
        type=Path,
        default=ROOT / "findings/t3_2_majority_rural_isolation.md",
    )
    args = ap.parse_args(argv)

    scores = {label: score_map(label, spec) for label, spec in MAPS.items()}
    ranks = rank_maps(scores)
    v = verdict(scores, ranks)
    commit = script_commit()

    payload = {
        "test": "T3.2 majority rural-isolation counter-test",
        "preregistration": "preregistration/t3_2_majority_rural_isolation_design.md",
        "script_commit": commit,
        "salt_string": "t3_2_majority_rural_isolation_counter_test",
        "scores": scores,
        "ranks": ranks,
        "verdict": v,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(args.output_md, scores, ranks, v, commit)
    print(f"verdict: {v['decision']}")
    print(f"narrative: {v['narrative']}")
    print(f"json -> {args.output_json}")
    print(f"md   -> {args.output_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
