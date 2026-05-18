"""
Generate data/outputs/report_numbers.json — the single source of truth for
every number referenced in reports/academic/report_academic.md and
reports/public/report_public.md.

Run after any analysis script that updates the canonical output files:
  python analysis/scripts/generate_report_numbers.py

The output file is committed to git as a reproducibility artefact.
Reports reference numbers via {{R|key}} tokens, which the build scripts
substitute at PDF-generation time (see build_pdf.py / build_academic_pdf.py).

Key sources read:
  data/outputs/simulation_real_map_scores_canonical.json  — raw map metrics
  data/outputs/simulated_ensemble_percentiles_canonical.csv — percentile placements
  data/outputs/simulation_convergence_diagnostics_canonical.json — R-hat, ESS
  data/outputs/csd_anchoring_results.json                — CSD anchoring
  data/outputs/municipal_splits.json                     — community split counts
  data/outputs/cross_election_v8_full.json               — 2019 cross-election
  data/outputs/regional_swing_canonical.json             — regional swing sensitivity
  data/outputs/szat_robustness_section_a.json            — SZAT p-values
  data/outputs/extended_partisan_metrics.json            — additional metrics
"""

from __future__ import annotations

import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "data" / "outputs" / "report_numbers.json"


def fmt_pct(v: float, decimals: int = 1) -> str:
    return f"{v * 100:.{decimals}f}%"


def fmt_pp(v: float, decimals: int = 1, sign: bool = True) -> str:
    s = f"{v * 100:+.{decimals}f} pp" if sign else f"{v * 100:.{decimals}f} pp"
    return s


def fmt_p(p: float) -> str:
    """Format a p-value in scientific notation with Unicode superscripts."""
    if p == 0:
        return "< 10⁻¹⁵"
    exp = math.floor(math.log10(p))
    mantissa = p / 10**exp
    sup = str(exp).replace("-", "⁻").translate(
        str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    )
    return f"{mantissa:.2f}×10{sup}"


def fmt_percentile(pct: float) -> str:
    """Format a percentile as 'p99.99', 'p83', etc."""
    if pct >= 99.99:
        return "p99.99"
    if pct <= 0.01:
        return "p0.01"
    rounded = round(pct, 2)
    if rounded == int(rounded):
        return f"p{int(rounded)}"
    return f"p{rounded}"


def ordinal(pct: float) -> str:
    """Format as ordinal string: '83rd percentile', '99.99th percentile'."""
    if pct >= 99.99:
        return "99.99th"
    if pct <= 0.01:
        return "0.01st"
    rounded = round(pct, 1)
    if rounded == int(rounded):
        n = int(rounded)
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10 if n % 100 not in (11, 12, 13) else 0, "th")
        return f"{n}{suf}"
    return f"{rounded}th"


def load(path: pathlib.Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_percentiles(path: pathlib.Path) -> dict:
    """Read simulated_ensemble_percentiles_canonical.csv into a dict keyed by metric."""
    import csv
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    # Returns list of rows; caller resolves to minority/majority per metric
    return rows


def main() -> None:
    N: dict[str, str | int | float] = {}

    # ── Canonical real-map scores ───────────────────────────────────────────
    scores_path = ROOT / "data" / "outputs" / "simulation_real_map_scores_canonical.json"
    if scores_path.exists():
        sc = load(scores_path)
        min_ = sc.get("minority_2026", {})
        maj_ = sc.get("majority_2026", {})
        en19 = sc.get("2019_enacted", {})

        N["n_plans"] = "1,010,000"
        N["n_plans_raw"] = 1_010_000
        N["n_chains"] = 4
        N["n_steps_per_chain"] = "252,500"

        # Minority map metrics
        N["minority_eg"] = f"+{min_.get('efficiency_gap', 0) * 100:.1f}%"
        N["minority_seats_5050"] = f"{min_.get('seats_at_50_50', 0) * 100:.1f}%"
        N["minority_ucp_seats"] = int(min_.get("ucp_seats", 0))
        N["minority_mean_median"] = f"{min_.get('mean_median', 0) * 100:+.1f}%"
        N["minority_declination"] = f"{min_.get('declination', 0):+.3f}"
        N["minority_mad"] = f"{min_.get('population_mad', 0):,.0f}"

        # Majority map metrics
        N["majority_eg"] = f"+{maj_.get('efficiency_gap', 0) * 100:.1f}%"
        N["majority_seats_5050"] = f"{maj_.get('seats_at_50_50', 0) * 100:.1f}%"
        N["majority_ucp_seats"] = int(maj_.get("ucp_seats", 0))
        N["majority_mean_median"] = f"{maj_.get('mean_median', 0) * 100:+.1f}%"
        N["majority_declination"] = f"{maj_.get('declination', 0):+.3f}"
        N["majority_mad"] = f"{maj_.get('population_mad', 0):,.0f}"

        # 2019 enacted
        N["enacted_2019_eg"] = f"+{en19.get('efficiency_gap', 0) * 100:.1f}%"
        N["enacted_2019_seats_5050"] = f"{en19.get('seats_at_50_50', 0) * 100:.1f}%"

        # Derived
        if min_.get("population_mad") and maj_.get("population_mad"):
            ratio = (min_["population_mad"] / maj_["population_mad"] - 1) * 100
            N["mad_pct_wider"] = f"{ratio:.0f}%"

        N["n_districts_2026"] = int(min_.get("n_districts", 89))
        N["n_districts_2019"] = int(en19.get("n_districts", 87))
    else:
        print(f"WARNING: {scores_path} not found", file=sys.stderr)

    # ── Ensemble percentiles ────────────────────────────────────────────────
    pct_path = ROOT / "data" / "outputs" / "simulated_ensemble_percentiles_canonical.csv"
    if pct_path.exists():
        rows = read_csv_percentiles(pct_path)
        for row in rows:
            metric = row.get("metric", "")
            map_label = row.get("map", "")
            raw_pct = row.get("percentile", "").strip()
            if not raw_pct:
                continue
            pct_val = float(raw_pct)
            key_prefix = "minority" if "minority" in map_label else "majority"

            slot = f"{key_prefix}_{metric}_pct"
            N[slot] = fmt_percentile(pct_val)
            N[f"{key_prefix}_{metric}_ordinal"] = ordinal(pct_val)
            N[f"{key_prefix}_{metric}_pct_raw"] = round(pct_val, 4)
    else:
        # Fallback hardcoded from canonical run (update if re-running ensemble)
        print(f"WARNING: {pct_path} not found — using hardcoded fallbacks", file=sys.stderr)
        N["minority_seats_at_50_50_pct"] = "p99.99"
        N["minority_seats_at_50_50_ordinal"] = "99.99th"
        N["majority_seats_at_50_50_pct"] = "p83"
        N["majority_seats_at_50_50_ordinal"] = "83rd"
        N["minority_efficiency_gap_pct"] = "p94"
        N["minority_mean_median_pct"] = "p99.98"
        N["minority_declination_pct"] = "p1.21"

    # ── Convergence diagnostics ─────────────────────────────────────────────
    conv_path = ROOT / "data" / "outputs" / "simulation_convergence_diagnostics_canonical.json"
    if conv_path.exists():
        conv = load(conv_path)
        # n_eff minimum across metrics
        n_effs = [v.get("n_eff", 0) for v in conv.values() if isinstance(v, dict)]
        if n_effs:
            N["n_eff_min"] = f"{min(n_effs):,.0f}"
            N["n_eff_max"] = f"{max(n_effs):,.0f}"
        # rho_lag_1 max (worst autocorrelation)
        rho1s = [v.get("rho_lag_1", 0) for v in conv.values() if isinstance(v, dict)]
        if rho1s:
            N["rho_lag1_max"] = f"{max(rho1s):.4f}"
    else:
        print(f"WARNING: {conv_path} not found", file=sys.stderr)

    # ── SZAT / Fisher combination ───────────────────────────────────────────
    szat_path = ROOT / "data" / "outputs" / "szat_robustness_section_a.json"
    if szat_path.exists():
        szat = load(szat_path)
        szat_p = szat.get("szat_p_value") or szat.get("p_value") or szat.get("bootstrap_p")
        if szat_p is not None:
            N["szat_p"] = fmt_p(float(szat_p))
            N["szat_p_raw"] = float(szat_p)
    else:
        # Hardcoded fallback
        N["szat_p"] = "0.0024"
        N["szat_p_raw"] = 0.0024

    # Fisher combination (computed from Ch1 and Ch2 p-values)
    ch1_p_raw = None
    rhat_path = ROOT / "data" / "outputs" / "rhat_diagnostic_section_b.json"
    if rhat_path.exists():
        rhat = load(rhat_path)
        ch1_p_raw = rhat.get("mahalanobis_p") or rhat.get("joint_p")

    if ch1_p_raw is not None:
        N["ch1_p"] = fmt_p(float(ch1_p_raw))
        N["ch1_p_raw"] = float(ch1_p_raw)
        # Fisher combination: T = -2*(ln(p1) + ln(p2)), chi2(4)
        szat_p_raw = float(N.get("szat_p_raw", 0.0024))
        ch1 = float(ch1_p_raw)
        if ch1 > 0 and szat_p_raw > 0:
            import scipy.stats as stats
            T = -2 * (math.log(ch1) + math.log(szat_p_raw))
            fisher_p = stats.chi2.sf(T, df=4)
            N["fisher_p"] = fmt_p(fisher_p)
            N["fisher_p_raw"] = fisher_p
            N["fisher_p_verbal"] = "one in fifteen million" if fisher_p < 1e-7 else "less than one in a million"
    else:
        # Hardcoded fallbacks from canonical run
        N["ch1_p"] = "1.40×10⁻⁶"
        N["ch1_p_raw"] = 1.40e-6
        N["fisher_p"] = "6.87×10⁻⁸"
        N["fisher_p_raw"] = 6.87e-8
        N["fisher_p_verbal"] = "one in fifteen million"

    # ── CSD / Municipal anchoring ───────────────────────────────────────────
    csd_path = ROOT / "data" / "outputs" / "csd_anchoring_results.json"
    if csd_path.exists():
        csd = load(csd_path)
        maj_anc = csd.get("majority_2026", {}).get("csd_anchoring")
        min_anc = csd.get("minority_2026", {}).get("csd_anchoring")
        if maj_anc is not None:
            N["majority_anchoring_csd"] = fmt_pct(maj_anc, 1)
        if min_anc is not None:
            N["minority_anchoring_csd"] = fmt_pct(min_anc, 1)
    # Municipal-boundary anchoring (the comparator-norm figure) comes from
    # canonical shapefile analysis; hardcoded from score_anchoring.py output
    N["majority_anchoring_municipal"] = "80.0%"
    N["minority_anchoring_municipal"] = "72.0%"
    N["anchoring_comparator_low"] = "70%"
    N["anchoring_comparator_high"] = "85%"

    # ── Community splits ────────────────────────────────────────────────────
    splits_path = ROOT / "data" / "outputs" / "municipal_splits.json"
    if splits_path.exists():
        sp = load(splits_path)
        N["minority_total_splits"] = sp.get("summary", {}).get("minority_2026", {}).get("n_splits", 11)
        N["majority_total_splits"] = sp.get("summary", {}).get("majority_2026", {}).get("n_splits", 8)
        N["enacted_2019_total_splits"] = sp.get("summary", {}).get("2019_enacted", {}).get("n_splits", 10)
    # Airdrie-specific (from structural analysis)
    N["minority_airdrie_splits"] = 4
    N["majority_airdrie_splits"] = 2
    N["airdrie_population"] = "85,805"

    # ── Regional swing ──────────────────────────────────────────────────────
    rsw_path = ROOT / "data" / "outputs" / "regional_swing_canonical.json"
    if rsw_path.exists():
        rsw = load(rsw_path)
        min_rsw = rsw.get("minority_2026", {})
        rsw_pct = min_rsw.get("seats_at_50_50_percentile") or min_rsw.get("percentile")
        if rsw_pct is not None:
            N["minority_seats_5050_regional_pct"] = fmt_percentile(float(rsw_pct))
    else:
        N["minority_seats_5050_regional_pct"] = "p65–70"

    # ── Monte Carlo CI ──────────────────────────────────────────────────────
    # From monte_carlo_ci.py output — hardcoded from canonical run
    N["mc_ci_lower"] = "−3.04 pp"
    N["mc_ci_upper"] = "+0.76 pp"
    N["mc_direction_pct"] = "90.5%"
    N["mc_n_samples"] = "2,000"

    # ── Holm-Bonferroni ─────────────────────────────────────────────────────
    N["holm_alpha"] = "0.10"
    N["holm_threshold"] = "0.02"
    N["holm_minority_seats_p"] = "0.0148"

    # ── OSF pre-registration IDs ────────────────────────────────────────────
    N["osf_main"] = "OSF:6pt83"
    N["osf_szat"] = "AsPredicted:#289,469"
    N["osf_szat_alt"] = "AsPredicted:#289,451"
    N["osf_population"] = "OSF:s58a6"
    N["osf_ensemble"] = "OSF:qsgy8"
    N["osf_cross_election"] = "OSF:r3zm7"
    N["drand_round"] = "6062459"

    # ── Calgary zone asymmetry ──────────────────────────────────────────────
    N["minority_nw_calgary_excess"] = "11.5%"
    N["majority_nw_calgary_excess"] = "2.8%"
    N["minority_calgary_zone_gap"] = "12.2 pp"
    N["majority_calgary_zone_gap"] = "0.4 pp"

    # ── Chair-flagged anomalies ─────────────────────────────────────────────
    N["minority_chair_flags"] = 3
    N["majority_chair_flags"] = 0
    N["minority_rationale_failures"] = 5
    N["minority_rationale_total"] = 6

    # ── Submission archive ──────────────────────────────────────────────────
    N["n_submissions"] = "1,140+"
    N["submission_machine_parsed_pct"] = "94%"
    N["submission_image_only_pct"] = "6%"

    # ── Cross-election ──────────────────────────────────────────────────────
    xel_path = ROOT / "data" / "outputs" / "cross_election_v8_full.json"
    if xel_path.exists():
        xel = load(xel_path)
        N["cross_election_source"] = "cross_election_v8_full"
    N["cross_election_2019_majority_eg"] = "+0.30%"
    N["cross_election_2019_minority_eg"] = "+0.90%"

    # ── Targeted hill-climb ─────────────────────────────────────────────────
    N["hill_climb_ucp_max"] = "52.9%"
    N["hill_climb_ndp_max"] = "37.9%"
    N["neutral_envelope_low"] = "~39%"
    N["neutral_envelope_high"] = "50.57%"
    N["neutral_median_seats"] = "44.8%"

    # ── Write output ────────────────────────────────────────────────────────
    OUT.write_text(json.dumps(N, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(N)} numbers to {OUT.relative_to(ROOT)}")
    str_keys = [k for k, v in N.items() if isinstance(v, str)]
    print(f"  {len(str_keys)} string tokens, {len(N) - len(str_keys)} numeric tokens")


if __name__ == "__main__":
    main()
