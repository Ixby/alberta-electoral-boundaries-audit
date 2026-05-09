"""One-shot script to add NaN contracts and logger calls to 23 sites."""
from pathlib import Path

FIXES = {}

# ── assignment_prep.py ──────────────────────────────────────────────────────
FIXES["analysis/scripts/assignment_prep.py"] = [
    (
        '    return abs(a - b) / b * 100 if b else float("nan")',
        '    # NaN contract: returns float("nan") if b == 0.\n    return abs(a - b) / b * 100 if b else float("nan")',
    ),
]

# ── neighbour_drain_adjacency.py ──────────────────────────────────────────────
FIXES["analysis/scripts/neighbour_drain_adjacency.py"] = [
    (
        '    return a / b if b else float("nan")',
        '    # NaN contract: returns float("nan") if b == 0.\n    return a / b if b else float("nan")',
    ),
]

# ── compactness_metrics.py ────────────────────────────────────────────────────
FIXES["analysis/scripts/compactness_metrics.py"] = [
    (
        '    if geom is None or geom.is_empty:\n        return float("nan")\n    try:\n        mbc = geom.minimum_bounding_circle()',
        '    # NaN contract: returns float("nan") if geometry is None, empty, or MBC fails.\n    if geom is None or geom.is_empty:\n        return float("nan")\n    try:\n        mbc = geom.minimum_bounding_circle()',
    ),
    (
        '        if mbc is None or mbc.is_empty or mbc.area == 0:\n            return float("nan")',
        '        # NaN contract: returns float("nan") if MBC is degenerate.\n        if mbc is None or mbc.is_empty or mbc.area == 0:\n            return float("nan")',
    ),
    (
        '    if geom is None or geom.is_empty:\n        return float("nan")\n    hull = geom.convex_hull',
        '    # NaN contract: returns float("nan") if geometry is None or empty.\n    if geom is None or geom.is_empty:\n        return float("nan")\n    hull = geom.convex_hull',
    ),
    (
        '    if hull is None or hull.area == 0:\n        return float("nan")',
        '    # NaN contract: returns float("nan") if convex hull has zero area.\n    if hull is None or hull.area == 0:\n        return float("nan")',
    ),
    (
        '    if perimeter_m <= 0 or area_m2 <= 0:\n        return float("nan")',
        '    # NaN contract: returns float("nan") if geometry measurements are non-positive.\n    if perimeter_m <= 0 or area_m2 <= 0:\n        return float("nan")',
    ),
]

# ── polsby_popper.py ──────────────────────────────────────────────────────────
FIXES["analysis/scripts/polsby_popper.py"] = [
    (
        'def polsby_popper(geom) -> float:\n    if geom is None or geom.is_empty:\n        return float("nan")',
        'def polsby_popper(geom) -> float:\n    # NaN contract: returns float("nan") if geometry is None, empty, or has zero perimeter.\n    if geom is None or geom.is_empty:\n        return float("nan")',
    ),
    (
        '    if perim == 0:\n        return float("nan")',
        '    # NaN contract: returns float("nan") if perimeter is zero.\n    if perim == 0:\n        return float("nan")',
    ),
]

# ── reock.py ──────────────────────────────────────────────────────────────────
FIXES["analysis/scripts/reock.py"] = [
    (
        '    if circle is None or circle.is_empty:\n        return float("nan")',
        '    # NaN contract: returns float("nan") if minimum bounding circle is degenerate.\n    if circle is None or circle.is_empty:\n        return float("nan")',
    ),
    (
        '    if geom is None or geom.is_empty:\n        return float("nan")\n    pts: list[tuple[float, float]] = []',
        '    # NaN contract: returns float("nan") if geometry is None or empty.\n    if geom is None or geom.is_empty:\n        return float("nan")\n    pts: list[tuple[float, float]] = []',
    ),
    (
        '    pts = list({p for p in pts})\n    if not pts:\n        return float("nan")',
        '    pts = list({p for p in pts})\n    # NaN contract: returns float("nan") if no valid coordinate points.\n    if not pts:\n        return float("nan")',
    ),
    (
        '    c = welzl(pts, [], len(pts))\n    if c is None:\n        return float("nan")',
        '    c = welzl(pts, [], len(pts))\n    # NaN contract: returns float("nan") if Welzl algorithm fails.\n    if c is None:\n        return float("nan")',
    ),
    (
        '    if geom is None or geom.is_empty:\n        return float("nan"), float("nan")\n    d = bounding_circle_diameter(geom)',
        '    # NaN contract: returns (float("nan"), float("nan")) if geometry is invalid or circle diameter is zero.\n    if geom is None or geom.is_empty:\n        return float("nan"), float("nan")\n    d = bounding_circle_diameter(geom)',
    ),
    (
        '    if not d or math.isnan(d) or d <= 0:\n        return float("nan"), float("nan")',
        '    # NaN contract: returns (float("nan"), float("nan")) if bounding diameter is zero or NaN.\n    if not d or math.isnan(d) or d <= 0:\n        return float("nan"), float("nan")',
    ),
]

# ── chen_rodden_alberta.py ────────────────────────────────────────────────────
FIXES["analysis/scripts/chen_rodden_alberta.py"] = [
    (
        '    if denominator == 0:\n        return float("nan"), -1.0 / (n - 1)',
        '    if denominator == 0:\n        logger.debug("morans_i: zero variance (n=%d), returning NaN", n)\n        return float("nan"), -1.0 / (n - 1)',
    ),
    (
        '    if total == 0:\n        return float("nan")\n    ndp_wasted = ucp_wasted = 0',
        '    if total == 0:\n        logger.debug("efficiency_gap: zero total votes, returning NaN")\n        return float("nan")\n    ndp_wasted = ucp_wasted = 0',
    ),
    (
        '    if not shares:\n        return float("nan")\n    return statistics.mean(shares) - statistics.median(shares)',
        '    if not shares:\n        logger.debug("mean_median: no valid districts, returning NaN")\n        return float("nan")\n    return statistics.mean(shares) - statistics.median(shares)',
    ),
]

# ── extended_partisan_metrics.py ──────────────────────────────────────────────
FIXES["analysis/scripts/extended_partisan_metrics.py"] = [
    (
        '    if len(ucp_wins) < 3 or len(ndp_wins) < 3:\n        return float("nan"), float("nan")',
        '    if len(ucp_wins) < 3 or len(ndp_wins) < 3:\n        logger.debug("lopsided_margins: insufficient wins (ucp=%d ndp=%d)", len(ucp_wins), len(ndp_wins))\n        return float("nan"), float("nan")',
    ),
    (
        '    if len(arr) == 0:\n        return float("nan")\n    less = (arr < val - 1e-9).sum()',
        '    if len(arr) == 0:\n        logger.debug("pct_rank: empty array, returning NaN")\n        return float("nan")\n    less = (arr < val - 1e-9).sum()',
    ),
]

# ── cross_election.py ─────────────────────────────────────────────────────────
FIXES["analysis/scripts/cross_election.py"] = [
    (
        '    if math.isnan(value):\n        return float("nan")\n    return float((ensemble_values < value).mean() * 100.0)',
        '    # NaN contract: propagates NaN input — if value is NaN, percentile is undefined.\n    if math.isnan(value):\n        return float("nan")\n    return float((ensemble_values < value).mean() * 100.0)',
    ),
]

# ── mcmc_ensemble.py ──────────────────────────────────────────────────────────
FIXES["analysis/scripts/mcmc_ensemble.py"] = [
    (
        '    if len(values) == 0 or np.isnan(x):\n        return float("nan")\n    below = np.sum(values < x)',
        '    # NaN contract: returns float("nan") if values array is empty or x is NaN.\n    if len(values) == 0 or np.isnan(x):\n        return float("nan")\n    below = np.sum(values < x)',
    ),
]

# ── canadian_base_rate_recalibrate.py ─────────────────────────────────────────
FIXES["analysis/scripts/canadian_base_rate_recalibrate.py"] = [
    (
        '    n = len(sample)\n    if n == 0:\n        return float("nan")',
        '    n = len(sample)\n    if n == 0:\n        logger.debug("percentile_score: empty sample, returning NaN")\n        return float("nan")',
    ),
]

# ── Execute ────────────────────────────────────────────────────────────────────
for path_str, fixes in FIXES.items():
    p = Path(path_str)
    if not p.exists():
        print(f"MISSING: {path_str}")
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    for old, new in fixes:
        if old in text:
            text = text.replace(old, new, 1)
        else:
            print(f"  MISS in {p.name}: {repr(old[:80])}")
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"OK: {p.name}")
    else:
        print(f"NO CHANGE: {p.name}")
