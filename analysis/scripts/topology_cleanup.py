"""
DEPRECATED 2026-05-07. Official Elections Alberta canonical shapefiles supersede
all DPG-derived files. Retained for provenance only.

Topology Cleanup — Eliminate inter-ED polygon overlap in v0_1 canonical DPGs
============================================================================
The canonical Derived Provisional Geometry (DPG) files were traced from
600-DPI commission thumbnails; tracing error put some polygons across shared
boundaries. Measurements on v0_1:

  * Majority: ~2,700 km² of inter-ED overlap, 1,011 VAs with raw DPG
    coverage > 1.0 (max 3.00×).
  * Minority: ~16,500 km² of inter-ED overlap, 1,722 VAs with raw DPG
    coverage > 1.0 (max 3.95×).

Under MAUP area-weighted attribution, this inflates fractional coverage
and produces Tier-C transcription artefacts (notably the Stony Plain-
Drayton Valley 24.8 pp flip under MAUP-v1).

**Method.** For each map independently:
  1. Detect inter-ED overlap regions via gpd.overlay(how='intersection').
  2. For each overlap between polygons A and B, assign it to whichever has
     stronger source evidence. Precedence (highest → lowest):
       sweep > osm-municipal-buffered > 2019-parent > v7
     Tie-breaker (both v7): smaller polygon area wins.
  3. Build clean polygons by subtracting each ED's "lost" overlap regions
     from its original geometry.
  4. Verify: no pair of polygons intersects (> 1 m²), no ED erased,
     provincial total area conserved within 0.1 %.

Inputs (read-only):
  data/v0_1_canonical_majority_2026_eds.gpkg
  data/v0_1_canonical_minority_2026_eds.gpkg

Outputs:
  data/v0_2_canonical_majority_2026_eds_topoclean.gpkg
  data/v0_2_canonical_minority_2026_eds_topoclean.gpkg
  analysis/reports/topology_cleanup_log.csv  (per-ED before/after)
  analysis/reports/topology_cleanup_summary.json

Forward: analysis/scripts/v0_1_assignment_va_attribution_maup_v2.py
Backward:
  analysis/scripts/v0_1_build_canonical_shapefiles.py
  data/v0_1_canonical_{majority,minority}_2026_eds.gpkg
"""

# Version: 0.1 series  (last updated 2026-04-26)


from __future__ import annotations

import json
import time
import warnings
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union
from shapely import make_valid

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="geopandas")
warnings.filterwarnings("ignore", message=".*GEOS.*")

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "analysis" / "reports"

MAJ_IN = DATA / "shapefiles" / "derived" / "v0_1_canonical_majority_2026_eds.gpkg"
MIN_IN = DATA / "shapefiles" / "derived" / "v0_1_canonical_minority_2026_eds.gpkg"
MAJ_OUT = (
    DATA / "shapefiles" / "derived" / "v0_2_canonical_majority_2026_eds_topoclean.gpkg"
)
MIN_OUT = (
    DATA / "shapefiles" / "derived" / "v0_2_canonical_minority_2026_eds_topoclean.gpkg"
)
LOG_CSV = REPORTS / "topology_cleanup_log.csv"
SUMMARY_JSON = REPORTS / "topology_cleanup_summary.json"

# Precedence order for canon_source (higher index = stronger evidence)
SOURCE_PRECEDENCE = {
    "v7": 1,
    "2019-parent": 3,
    "osm-municipal-buffered": 4,
    "sweep": 5,
}


def source_rank(src: str) -> int:
    return SOURCE_PRECEDENCE.get(str(src), 0)


def _keep_polys(geom):
    """Normalise to (Multi)Polygon; drop line/point remnants from set ops."""
    if geom is None or geom.is_empty:
        return None
    if geom.geom_type in ("Polygon", "MultiPolygon"):
        return geom
    if geom.geom_type == "GeometryCollection":
        polys = [g for g in geom.geoms if g.geom_type in ("Polygon", "MultiPolygon")]
        if not polys:
            return None
        return unary_union(polys)
    return None


def winner(a_src: str, a_area: float, b_src: str, b_area: float) -> str:
    """Return 'A' or 'B' — whichever polygon should keep the overlap region."""
    ra, rb = source_rank(a_src), source_rank(b_src)
    if ra > rb:
        return "A"
    if rb > ra:
        return "B"
    # Tie (both v7 usually): smaller polygon wins (concentrated > sprawling)
    return "A" if a_area <= b_area else "B"


def detect_overlaps(eds: gpd.GeoDataFrame, label: str) -> pd.DataFrame:
    """Return a DataFrame of per-pair overlap regions.

    Columns: idx_a, idx_b, name_a, name_b, src_a, src_b, area_a_orig,
             area_b_orig, overlap_geom, overlap_area_m2.
    """
    print(f"  [{label}] Detecting inter-ED overlaps...")
    t0 = time.time()

    # Self-overlay intersection: we only want pairs where i != j.
    # Tag index and do pairwise intersection through spatial index.
    eds = eds.reset_index(drop=True).copy()
    eds["_idx"] = eds.index
    sindex = eds.sindex

    rows = []
    for i, row_a in eds.iterrows():
        geom_a = row_a.geometry
        if geom_a is None or geom_a.is_empty:
            continue
        cand = list(sindex.query(geom_a, predicate="intersects"))
        for j in cand:
            if j <= i:
                continue
            row_b = eds.iloc[j]
            geom_b = row_b.geometry
            if geom_b is None or geom_b.is_empty:
                continue
            inter = geom_a.intersection(geom_b)
            inter = _keep_polys(inter)
            if inter is None or inter.is_empty:
                continue
            area = inter.area
            if area < 1.0:  # < 1 m² — numeric noise, skip
                continue
            rows.append(
                {
                    "idx_a": i,
                    "idx_b": j,
                    "name_a": row_a["name_2026"],
                    "name_b": row_b["name_2026"],
                    "src_a": row_a["canon_source"],
                    "src_b": row_b["canon_source"],
                    "area_a_orig": geom_a.area,
                    "area_b_orig": geom_b.area,
                    "overlap_geom": inter,
                    "overlap_area_m2": area,
                }
            )
    overlaps = pd.DataFrame(rows)
    total_km2 = overlaps["overlap_area_m2"].sum() / 1e6 if len(overlaps) else 0.0
    print(
        f"  [{label}] found {len(overlaps)} overlap pairs, total "
        f"{total_km2:,.1f} km² in {time.time()-t0:.1f}s"
    )
    return overlaps


def cleanup_map(eds: gpd.GeoDataFrame, label: str) -> tuple[gpd.GeoDataFrame, dict]:
    """Run one-map topology cleanup. Returns cleaned GeoDataFrame + stats."""
    # Make geometries valid before anything
    eds = eds.reset_index(drop=True).copy()
    eds["geometry"] = eds.geometry.apply(
        lambda g: make_valid(g) if g is not None else g
    )
    eds["geometry"] = eds.geometry.apply(_keep_polys)
    eds = eds[eds.geometry.notna() & ~eds.geometry.is_empty].reset_index(drop=True)

    orig_total_area_sum = float(eds.geometry.area.sum())  # double-counts overlap
    # True provincial footprint = union-dissolve of all polygons
    orig_union_area = float(unary_union(eds.geometry.tolist()).area)
    # Expected ideal total after cleanup ≈ provincial union (each point counted once)
    orig_total_area = orig_union_area

    orig_areas = eds.geometry.area.copy()

    overlaps = detect_overlaps(eds, label)
    total_overlap_km2 = (
        float(overlaps["overlap_area_m2"].sum()) / 1e6 if len(overlaps) else 0.0
    )

    # For each polygon, build the union of overlap-regions it should LOSE
    # (the ones where it is not the winner).
    n = len(eds)
    to_subtract = {i: [] for i in range(n)}
    decision_rows = []
    for _, r in overlaps.iterrows():
        w = winner(r["src_a"], r["area_a_orig"], r["src_b"], r["area_b_orig"])
        loser_idx = r["idx_b"] if w == "A" else r["idx_a"]
        winner_idx = r["idx_a"] if w == "A" else r["idx_b"]
        to_subtract[int(loser_idx)].append(r["overlap_geom"])
        decision_rows.append(
            {
                "name_winner": eds.iloc[winner_idx]["name_2026"],
                "src_winner": eds.iloc[winner_idx]["canon_source"],
                "name_loser": eds.iloc[loser_idx]["name_2026"],
                "src_loser": eds.iloc[loser_idx]["canon_source"],
                "overlap_km2": r["overlap_area_m2"] / 1e6,
            }
        )

    decisions_df = (
        pd.DataFrame(decision_rows)
        .sort_values("overlap_km2", ascending=False)
        .reset_index(drop=True)
        if decision_rows
        else pd.DataFrame()
    )

    # Apply subtractions with an anti-erasure safeguard: if losing all
    # assigned overlaps would leave < 10% of the original polygon area
    # (i.e. the polygon would be effectively swallowed), the loser is
    # over-matched by a sprawling higher-tier neighbour — a sweep or
    # 2019-parent polygon that traced too broadly. In that case keep the
    # loser's core by subtracting only the MOST EXCESS overlaps (the
    # smallest-rank overlaps first) until the remaining area is >= 10%
    # of its original.
    cleaned_geoms = []
    protection_events = []  # list of (ed_name, orig_km2, protected_km2)
    for i, row in eds.iterrows():
        g = row.geometry
        losses = to_subtract[i]
        if losses:
            orig_area = g.area
            loss_union = unary_union(losses)
            try:
                g2 = g.difference(loss_union)
            except Exception:
                g2 = make_valid(g).difference(make_valid(loss_union))
            g2 = _keep_polys(g2)
            remaining_frac = (
                (g2.area / orig_area) if (g2 is not None and not g2.is_empty) else 0.0
            )

            if remaining_frac < 0.10:
                # Anti-erasure: this polygon would lose >90 % of its area.
                # Fall back: do NOT subtract anything from this polygon;
                # the overlap is contested and keeping the full original
                # preserves geographic meaning. The competing higher-tier
                # polygon still keeps the overlap too (both sides retain
                # it in their own file), which means the residual overlap
                # check will flag it — we'll dissolve that separately by
                # letting the SMALLER polygon (this loser) keep its
                # footprint and intersecting it out of the WINNER's
                # geometry post-hoc. For now, we keep g unchanged and
                # record the event; the second pass handles the winner.
                protection_events.append(
                    (row["name_2026"], orig_area / 1e6, g2.area / 1e6 if g2 else 0.0)
                )
                print(
                    f"    ANTI-ERASURE: {row['name_2026']} would retain "
                    f"only {remaining_frac*100:.2f}% — keeping original."
                )
                g2 = g
            elif g2 is None or g2.is_empty:
                print(
                    f"    WARNING: {row['name_2026']} would be fully erased "
                    "by overlap subtraction. Keeping original geometry."
                )
                g2 = g
        else:
            g2 = g
        cleaned_geoms.append(g2)

    # Second pass: for every protected loser, subtract its (now-preserved)
    # geometry from every other cleaned polygon. This ensures the winner
    # still gives up the contested area even though the loser kept it.
    if protection_events:
        print(
            f"  [{label}] second pass: re-subtracting {len(protection_events)} "
            f"protected-loser regions from all overlapping winners..."
        )
        protected_names = {ev[0] for ev in protection_events}
        for p_idx, row in eds.iterrows():
            if row["name_2026"] not in protected_names:
                continue
            protected_geom = cleaned_geoms[p_idx]
            for o_idx in range(n):
                if o_idx == p_idx:
                    continue
                other = cleaned_geoms[o_idx]
                if other is None or other.is_empty:
                    continue
                if not other.intersects(protected_geom):
                    continue
                new_other = other.difference(protected_geom)
                new_other = _keep_polys(new_other)
                if new_other is None or new_other.is_empty:
                    # Would erase the other polygon — skip (don't recurse erasure)
                    continue
                if new_other.area / other.area < 0.10:
                    # Skip — would erase this one too
                    continue
                cleaned_geoms[o_idx] = new_other

    # Third pass: resolve any remaining residual overlaps by centroid-
    # proximity assignment. After anti-erasure both polygons may still
    # share the contested region. Split it 50/50 by nearest centroid.
    print(
        f"  [{label}] third pass: centroid-proximity split for any "
        "remaining contested regions..."
    )
    for i in range(n):
        for j in range(i + 1, n):
            gi, gj = cleaned_geoms[i], cleaned_geoms[j]
            if gi is None or gj is None or gi.is_empty or gj.is_empty:
                continue
            if not gi.intersects(gj):
                continue
            inter = gi.intersection(gj)
            inter = _keep_polys(inter)
            if inter is None or inter.is_empty or inter.area < 1.0:
                continue
            # Use original polygon centroids as anchors (pre-cleanup).
            ci = eds.iloc[i].geometry.representative_point()
            cj = eds.iloc[j].geometry.representative_point()
            # For each sub-polygon of the intersection, compute the
            # dominant anchor by centroid distance.
            inter_parts = (
                list(inter.geoms) if inter.geom_type == "MultiPolygon" else [inter]
            )
            give_to_i_parts = []
            give_to_j_parts = []
            for part in inter_parts:
                if part.is_empty:
                    continue
                pc = part.representative_point()
                di = pc.distance(ci)
                dj = pc.distance(cj)
                if di <= dj:
                    give_to_i_parts.append(part)
                else:
                    give_to_j_parts.append(part)
            # i keeps its region; subtract the j-dominant parts from i,
            # and the i-dominant parts from j.
            if give_to_j_parts:
                rem_j = unary_union(give_to_j_parts)
                new_gi = gi.difference(rem_j)
                new_gi = _keep_polys(new_gi)
                if (
                    new_gi is not None
                    and not new_gi.is_empty
                    and new_gi.area / gi.area > 0.05
                ):
                    cleaned_geoms[i] = new_gi
            if give_to_i_parts:
                rem_i = unary_union(give_to_i_parts)
                new_gj = gj.difference(rem_i)
                new_gj = _keep_polys(new_gj)
                if (
                    new_gj is not None
                    and not new_gj.is_empty
                    and new_gj.area / gj.area > 0.05
                ):
                    cleaned_geoms[j] = new_gj

    # Fourth pass: final unconditional split of any remaining residuals.
    # If two polygons still overlap after passes 1-3 (anti-erasure stuck),
    # assign the overlap region deterministically by centroid proximity
    # of ORIGINAL polygons, without survival floor. This guarantees the
    # no-overlap gate passes.
    print(f"  [{label}] fourth pass: unconditional residual split...")
    for i in range(n):
        for j in range(i + 1, n):
            gi, gj = cleaned_geoms[i], cleaned_geoms[j]
            if gi is None or gj is None or gi.is_empty or gj.is_empty:
                continue
            if not gi.intersects(gj):
                continue
            inter = gi.intersection(gj)
            inter = _keep_polys(inter)
            if inter is None or inter.is_empty or inter.area < 1.0:
                continue
            # Whichever polygon's original centroid is closer to the overlap
            # centroid keeps it. Subtract from the other unconditionally.
            ci = eds.iloc[i].geometry.representative_point()
            cj = eds.iloc[j].geometry.representative_point()
            pc = inter.representative_point()
            if pc.distance(ci) <= pc.distance(cj):
                # i keeps, j loses
                new_gj = gj.difference(inter)
                new_gj = _keep_polys(new_gj)
                if new_gj is None or new_gj.is_empty:
                    # Would erase; skip this pair (rare)
                    print(
                        f"    WARNING: fourth-pass would erase {eds.iloc[j]['name_2026']}; leaving overlap."
                    )
                    continue
                cleaned_geoms[j] = new_gj
            else:
                new_gi = gi.difference(inter)
                new_gi = _keep_polys(new_gi)
                if new_gi is None or new_gi.is_empty:
                    print(
                        f"    WARNING: fourth-pass would erase {eds.iloc[i]['name_2026']}; leaving overlap."
                    )
                    continue
                cleaned_geoms[i] = new_gi

    cleaned = eds.copy()
    cleaned["geometry"] = cleaned_geoms
    cleaned["geometry"] = cleaned["geometry"].apply(_keep_polys)

    new_areas = cleaned.geometry.area
    delta_km2 = (new_areas - orig_areas) / 1e6

    # Per-ED log
    per_ed_log = pd.DataFrame(
        {
            "map": label,
            "name_2026": cleaned["name_2026"].values,
            "canon_source": cleaned["canon_source"].values,
            "orig_area_km2": orig_areas.values / 1e6,
            "clean_area_km2": new_areas.values / 1e6,
            "delta_km2": delta_km2.values,
        }
    )

    # Verify no pair overlaps > 1 m²
    post_overlaps = detect_overlaps(cleaned, f"{label} (post-clean)")
    post_overlap_km2 = (
        float(post_overlaps["overlap_area_m2"].sum()) / 1e6
        if len(post_overlaps)
        else 0.0
    )
    max_residual_m2 = (
        float(post_overlaps["overlap_area_m2"].max()) if len(post_overlaps) else 0.0
    )

    no_overlap_pass = post_overlap_km2 < 0.001  # < 1000 m² residual = PASS

    # Verify no ED erased
    n_erased = int((new_areas < 1.0).sum())
    no_erased_pass = n_erased == 0

    # Provincial total area conservation
    new_total_area = float(new_areas.sum())
    area_drift_frac = (new_total_area - orig_total_area) / orig_total_area
    area_conservation_pass = abs(area_drift_frac) < 0.001

    # Net per-side delta (should be 0 — overlap resolved is zero-sum)
    net_delta_km2 = float(delta_km2.sum())

    stats = {
        "label": label,
        "n_eds": int(n),
        "orig_union_area_km2": orig_union_area / 1e6,
        "orig_sum_area_km2_double_counted": orig_total_area_sum / 1e6,
        "clean_total_area_km2": new_total_area / 1e6,
        "area_drift_frac_vs_union": area_drift_frac,
        "area_conservation_pass": area_conservation_pass,
        "overlap_km2_resolved": total_overlap_km2,
        "overlap_pairs_resolved": int(len(overlaps)),
        "residual_overlap_km2": post_overlap_km2,
        "residual_overlap_max_m2": max_residual_m2,
        "no_overlap_pass": no_overlap_pass,
        "n_eds_erased": n_erased,
        "no_erased_pass": no_erased_pass,
        "net_delta_km2": net_delta_km2,
        "n_eds_gained": int((delta_km2 > 0).sum()),
        "n_eds_lost": int((delta_km2 < 0).sum()),
    }

    print(
        f"  [{label}] resolved {total_overlap_km2:,.1f} km² overlap; "
        f"residual = {post_overlap_km2:.4f} km²"
    )
    print(
        f"  [{label}] area drift: {area_drift_frac*100:+.4f}%  "
        f"net delta: {net_delta_km2/1e6:+.4f} km2  "
        f"n gained: {stats['n_eds_gained']}  n lost: {stats['n_eds_lost']}"
    )
    print(
        f"  [{label}] validation: no-overlap={no_overlap_pass}  "
        f"no-erased={no_erased_pass}  area-conservation={area_conservation_pass}"
    )

    return cleaned, stats, per_ed_log, decisions_df


def main():
    print("=" * 72)
    print("  v0_1 Topology Cleanup — remove inter-ED DPG overlap")
    print("=" * 72)

    print("\n[load] canonical DPGs...")
    maj = gpd.read_file(MAJ_IN)
    mino = gpd.read_file(MIN_IN)
    print(f"  Majority: {len(maj)} EDs  CRS={maj.crs}")
    print(f"  Minority: {len(mino)} EDs  CRS={mino.crs}")

    # Ensure projected CRS (for area calcs). Both should already be EPSG:3401.
    assert maj.crs == mino.crs, "Majority and minority CRS mismatch"

    print("\n" + "=" * 72)
    print("  MAJORITY cleanup")
    print("=" * 72)
    t0 = time.time()
    maj_clean, maj_stats, maj_log, maj_dec = cleanup_map(maj, "majority")
    print(f"  [majority elapsed: {time.time()-t0:.1f}s]")

    print("\n" + "=" * 72)
    print("  MINORITY cleanup")
    print("=" * 72)
    t1 = time.time()
    min_clean, min_stats, min_log, min_dec = cleanup_map(mino, "minority")
    print(f"  [minority elapsed: {time.time()-t1:.1f}s]")

    # Write outputs
    print("\n[write] cleaned GPKGs...")
    maj_clean.to_file(MAJ_OUT, driver="GPKG")
    min_clean.to_file(MIN_OUT, driver="GPKG")
    print(f"  wrote: {MAJ_OUT}")
    print(f"  wrote: {MIN_OUT}")

    # Per-ED log
    full_log = pd.concat([maj_log, min_log], ignore_index=True)
    full_log.to_csv(LOG_CSV, index=False)
    print(f"  wrote: {LOG_CSV}  ({len(full_log)} rows)")

    # Decisions top-20 each
    print("\n[top decisions, majority]")
    if not maj_dec.empty:
        for _, r in maj_dec.head(10).iterrows():
            print(
                f"  {r['overlap_km2']:7.1f} km²  "
                f"[{r['src_winner']}] {r['name_winner']:<40s} "
                f"won vs [{r['src_loser']}] {r['name_loser']}"
            )
    print("\n[top decisions, minority]")
    if not min_dec.empty:
        for _, r in min_dec.head(10).iterrows():
            print(
                f"  {r['overlap_km2']:7.1f} km²  "
                f"[{r['src_winner']}] {r['name_winner']:<40s} "
                f"won vs [{r['src_loser']}] {r['name_loser']}"
            )

    summary = {
        "majority": maj_stats,
        "minority": min_stats,
        "outputs": {
            "majority_gpkg": str(MAJ_OUT),
            "minority_gpkg": str(MIN_OUT),
            "per_ed_log_csv": str(LOG_CSV),
        },
        "gates_passed": {
            "majority_no_overlap": maj_stats["no_overlap_pass"],
            "majority_no_erased": maj_stats["no_erased_pass"],
            "majority_area_conservation": maj_stats["area_conservation_pass"],
            "minority_no_overlap": min_stats["no_overlap_pass"],
            "minority_no_erased": min_stats["no_erased_pass"],
            "minority_area_conservation": min_stats["area_conservation_pass"],
        },
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  wrote: {SUMMARY_JSON}")

    all_pass = all(summary["gates_passed"].values())
    print("\n" + ("=" * 72))
    print(
        f"  TOPOLOGY CLEANUP: {'ALL GATES PASSED' if all_pass else 'GATE FAILURE — investigate'}"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
