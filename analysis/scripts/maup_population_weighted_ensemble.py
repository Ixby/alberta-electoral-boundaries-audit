# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta + StatsCan (public domain) | https://ixby.github.io
"""
maup_population_weighted_ensemble.py — T1.4a population-weighted attribution
placement against the canonical 1.01M ensemble.
===============================================================================

Key methodological point (the reason this is tractable without a per-plan
assignment archive): the canonical ReCom ensemble assigns *atomic VAs* to
districts. A VA is never split across its own assigned district, so the
ensemble's partisan-metric distribution is INVARIANT to the VA->ED attribution
method (centroid vs population-weighted). Attribution can only move a *real-map*
value. T1.4a therefore reduces to: score both commission maps under centroid and
under population-weighted attribution from the same VA basis, and re-place each
against the (invariant) ensemble distribution.

Acceptance (TODO_REMEDIATION T1.4a): if the centroid and population-weighted
percentile placements agree within +/-2 percentile points, the published
percentile claims survive a publication-grade attribution audit.

Outputs:
  findings/maup_population_weighted_ensemble.md
  data/outputs/maup_population_weighted_ensemble.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from mcmc_ensemble import build_va_graph, score_exogenous_map, seat_results  # noqa: E402
from va_attribution_population_weighted import population_weighted_attribution  # noqa: E402

MAJ = ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg"
MIN = ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg"
DAS = ROOT / "data/shapefiles/reference/alberta_2021_das.gpkg"
NAMECOL = "EDName2025"
METRICS = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]
CHAIN_DIR = ROOT / "data/simulation_checkpoints_canonical"
OUT_MD = ROOT / "findings/maup_population_weighted_ensemble.md"
OUT_JSON = ROOT / "data/outputs/maup_population_weighted_ensemble.json"


def load_ensemble() -> pd.DataFrame:
    frames = [pd.read_csv(CHAIN_DIR / f"chain{i}_samples.csv", usecols=METRICS) for i in range(4)]
    return pd.concat(frames, ignore_index=True)


def pct(dist: np.ndarray, val: float) -> float:
    return float(np.mean(dist <= val) * 100.0)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("[T1.4a] building VA graph (canonical votes + pop)...", flush=True)
    va, _ = build_va_graph(verbose=False)
    das = gpd.read_file(DAS)
    # DA shapefile is DAUID-keyed with no population column; join 2021 DA pops
    # from the reference CSV (same logic as va_attribution_population_weighted.main).
    if "pop_2021" not in das.columns:
        ref_csv = ROOT / "data/reference/alberta_2021_da_populations.csv"
        pop_df = pd.read_csv(ref_csv, dtype={"DAUID": str})
        pop_col = [c for c in pop_df.columns if "pop" in c.lower()][0]
        pop_df = pop_df.rename(columns={pop_col: "pop_2021"})
        das["DAUID"] = das["DAUID"].astype(str)
        das = das.merge(pop_df[["DAUID", "pop_2021"]], on="DAUID", how="left")
        das["pop_2021"] = das["pop_2021"].fillna(0.0)
        print(f"  joined DA pop from {ref_csv.name} "
              f"(total {das['pop_2021'].sum():,.0f})", flush=True)

    ens = load_ensemble()
    print(f"  ensemble n = {len(ens):,}", flush=True)

    results = {}
    for label, path in [("majority_2026", MAJ), ("minority_2026", MIN)]:
        print(f"\n=== {label} ===", flush=True)
        # Centroid attribution (current canonical method)
        m_cent = score_exogenous_map(va, path, id_col=NAMECOL)
        # Population-weighted attribution (VA x ED x DA three-way overlay)
        eds = gpd.read_file(path)
        per_ed, stats = population_weighted_attribution(
            va, eds, das, ed_id_col=NAMECOL, da_pop_col="pop_2021", verbose=True
        )
        m_pw = seat_results(per_ed["ucp"].values, per_ed["ndp"].values)

        rows = {}
        for mk in METRICS:
            dist = ens[mk].dropna().values
            cv, pv = float(m_cent[mk]), float(m_pw[mk])
            cp, pp = pct(dist, cv), pct(dist, pv)
            rows[mk] = {
                "centroid_value": cv, "centroid_pctile": cp,
                "popweighted_value": pv, "popweighted_pctile": pp,
                "value_shift": pv - cv, "pctile_shift": pp - cp,
            }
            print(f"  {mk:<16} centroid {cv:+.4f}@p{cp:6.2f}  "
                  f"popwt {pv:+.4f}@p{pp:6.2f}  Δpctile {pp-cp:+.2f}", flush=True)
        results[label] = {"metrics": rows, "attribution_drift": stats}

    max_shift = max(abs(r["pctile_shift"])
                    for lab in results for r in results[lab]["metrics"].values())
    verdict = "SURVIVES" if max_shift <= 2.0 else "EXCEEDS 2pp — investigate"

    payload = {
        "test": "T1.4a population-weighted attribution placement vs canonical 1.01M ensemble",
        "ensemble_n": int(len(ens)),
        "ensemble_attribution_invariant": True,
        "note": "Ensemble assigns atomic VAs; a VA never straddles its assigned district, "
                "so the ensemble distribution is identical under centroid and population-weighted "
                "attribution. Only real-map values can shift.",
        "max_abs_pctile_shift": max_shift,
        "verdict": verdict,
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=float), encoding="utf-8")

    md = [
        "---",
        "title: Population-weighted attribution placement vs canonical ensemble (T1.4a)",
        "status: COMPLETE",
        "---",
        "",
        "# T1.4a — Population-weighted attribution placement",
        "",
        "**Why no per-plan assignment archive is needed.** The canonical ReCom ensemble "
        "assigns *atomic VAs* to districts; a VA is never split across its own assigned "
        "district, so the ensemble's partisan-metric distribution is invariant to the "
        "VA→ED attribution method. Attribution can only move a *real-map* value. T1.4a "
        "therefore reduces to scoring both commission maps under centroid and under "
        "population-weighted (VA × ED × 2021-DA three-way overlay) attribution from the "
        "same VA basis, and re-placing each against the invariant 1,010,000-plan ensemble.",
        "",
        f"**Verdict: the published percentile claims {verdict}** "
        f"(max |percentile shift| = {max_shift:.2f} pp across all metrics and both maps; "
        f"acceptance threshold ±2 pp).",
        "",
    ]
    for label in ("minority_2026", "majority_2026"):
        md += [f"## {label}", "",
               "| Metric | Centroid value @ pctile | Pop-weighted value @ pctile | Δ pctile |",
               "|---|---|---|---|"]
        for mk in METRICS:
            r = results[label]["metrics"][mk]
            md.append(f"| {mk} | {r['centroid_value']:+.4f} @ p{r['centroid_pctile']:.2f} "
                      f"| {r['popweighted_value']:+.4f} @ p{r['popweighted_pctile']:.2f} "
                      f"| {r['pctile_shift']:+.2f} |")
        md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"\nVerdict: {verdict} (max |Δpctile| = {max_shift:.2f} pp)", flush=True)
    print(f"Wrote {OUT_MD} and {OUT_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
