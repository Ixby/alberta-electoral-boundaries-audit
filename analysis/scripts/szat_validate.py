"""
szat_validate.py -- Two validation checks for szat.py results.

Check 3: Attribution integrity
  Verify that sum(delta_eg, all VAs) == szat_score.
  Also check: swing-only sum vs non-swing contribution.
  Expected: non-swing VAs have nonzero delta_eg because their ED context
  shifts when swing zones move between maps; total attribution covers full score.

Check 2: Bootstrap approximation fidelity
  szat.py uses the full-recompute procedure (pre-registered null):
    For each permutation, each swing-zone VA is randomly assigned to either
    its majority_ed or minority_ed (Bernoulli 0.5). Non-swing VAs keep their
    shared ED. EG is recomputed from scratch.
    SZAT_perm = EG(perm_minority_map) - EG(majority_map_fixed).

  This check compares that full-recompute null against the older additive-delta
  approximation (sum of delta_eg for flipped swing VAs) to verify that both
  produce qualitatively similar p-values. The additive approximation captures
  only direct swing-zone effects (~55% of the score); the full-recompute null
  is the pre-registered method used in szat.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")
REPORTS = ROOT / "analysis" / "reports"

RESULTS_CSV  = REPORTS / "szat_results.csv"
SUMMARY_JSON = REPORTS / "szat_summary.json"

N_FULL_RECOMPUTE = 500


# ── EG helpers (identical to szat.py) ─────────────────────────────────────────

def _ed_waste(ndp: float, ucp: float) -> tuple[float, float]:
    total = ndp + ucp
    if total == 0:
        return 0.0, 0.0
    threshold = total / 2
    if ndp >= ucp:
        return max(0.0, ndp - threshold), ucp
    return ndp, max(0.0, ucp - threshold)


def compute_eg(ed_votes: pd.DataFrame) -> float:
    total_prov = (ed_votes["ndp"] + ed_votes["ucp"]).sum()
    if total_prov == 0:
        return 0.0
    wn = wu = 0.0
    for _, row in ed_votes.iterrows():
        dn, du = _ed_waste(row["ndp"], row["ucp"])
        wn += dn
        wu += du
    return (wn - wu) / total_prov


# ── Check 3: Attribution integrity ────────────────────────────────────────────

def check_attribution(summary: dict, va: pd.DataFrame) -> bool:
    print("=" * 60)
    print("CHECK 3 -- Attribution integrity")
    print("=" * 60)

    szat_score = summary["szat_score"]
    swing      = va[va["is_swing"] == 1]
    non_swing  = va[va["is_swing"] == 0]

    delta_swing    = swing["delta_eg"].sum()
    delta_nonswing = non_swing["delta_eg"].sum()
    delta_all      = va["delta_eg"].sum()

    print(f"  szat_score (summary.json):       {szat_score:+.6f}")
    print(f"  sum delta_eg  swing only:        {delta_swing:+.6f}")
    print(f"  sum delta_eg  non-swing only:    {delta_nonswing:+.6f}")
    print(f"  sum delta_eg  all VAs:           {delta_all:+.6f}")
    print()

    # All-VA sum should equal szat_score within 6-digit rounding (4765 * 5e-7 ~ 0.0024 max)
    all_match = abs(delta_all - szat_score) < 0.001
    # Non-swing being nonzero is EXPECTED (indirect effects); report magnitude
    nonswing_pct = 100.0 * abs(delta_nonswing) / abs(szat_score) if szat_score else 0

    print(f"  sum(all) ~= szat_score:          {'PASS' if all_match else f'FAIL  diff={delta_all - szat_score:.4f}'}")
    print(f"  Non-swing indirect effect:       {delta_nonswing:+.6f}  ({nonswing_pct:.1f}% of szat_score) -- EXPECTED nonzero")
    print(f"  Direct swing effect:             {delta_swing:+.6f}  ({100-nonswing_pct:.1f}% of szat_score)")
    print()

    # Cross-check EG values
    eg_maj_rep = summary["eg_majority"]
    eg_min_rep = summary["eg_minority"]
    maj_t = va.groupby("majority_ed", as_index=False).agg(
        ndp=("va_ndp", "sum"), ucp=("va_ucp", "sum")
    ).rename(columns={"majority_ed": "ed_name"})
    min_t = va.groupby("minority_ed", as_index=False).agg(
        ndp=("va_ndp", "sum"), ucp=("va_ucp", "sum")
    ).rename(columns={"minority_ed": "ed_name"})
    eg_maj_recomp = compute_eg(maj_t)
    eg_min_recomp = compute_eg(min_t)

    print(f"  EG majority  reported: {eg_maj_rep:+.6f}  recomputed: {eg_maj_recomp:+.6f}  {'PASS' if abs(eg_maj_recomp - eg_maj_rep) < 1e-5 else 'FAIL'}")
    print(f"  EG minority  reported: {eg_min_rep:+.6f}  recomputed: {eg_min_recomp:+.6f}  {'PASS' if abs(eg_min_recomp - eg_min_rep) < 1e-5 else 'FAIL'}")

    return all_match


# ── Check 2: Bootstrap approximation fidelity ─────────────────────────────────

def check_bootstrap_approximation(summary: dict, va: pd.DataFrame) -> None:
    print()
    print("=" * 60)
    print("CHECK 2 -- Bootstrap approximation fidelity")
    print(f"  ({N_FULL_RECOMPUTE} permutations, same canonical seed)")
    print("=" * 60)

    szat_score = summary["szat_score"]

    sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
    try:
        from drand_seed import get_canonical_seed
        seed = get_canonical_seed("szat-bootstrap")
        print(f"  Seed: {seed} (drand_seed)")
    except Exception as _e:
        # szat.py hard-fails when drand_seed is unavailable; validate matches that
        # behaviour so both scripts use the same seed source.
        raise RuntimeError(
            "drand_seed.get_canonical_seed unavailable — cannot reproduce the "
            "pre-registered bootstrap. Ensure drand_seed.py is on sys.path."
        ) from _e

    swing_mask   = va["is_swing"].values.astype(bool)
    swing_va     = va[swing_mask].reset_index(drop=True)
    non_swing_va = va[~swing_mask].reset_index(drop=True)
    n_swing      = len(swing_va)

    swing_deltas = swing_va["delta_eg"].values

    # Majority map ED totals -- fixed reference for full-recompute null
    all_ndp = np.concatenate([swing_va["va_ndp"].values, non_swing_va["va_ndp"].values])
    all_ucp = np.concatenate([swing_va["va_ucp"].values, non_swing_va["va_ucp"].values])
    all_maj_ed = np.concatenate([swing_va["majority_ed"].values, non_swing_va["majority_ed"].values])
    maj_df = pd.DataFrame({"ed": all_maj_ed, "ndp": all_ndp, "ucp": all_ucp})
    maj_totals = maj_df.groupby("ed", as_index=False).agg(
        ndp=("ndp", "sum"), ucp=("ucp", "sum")
    ).rename(columns={"ed": "ed_name"})
    eg_maj_fixed = compute_eg(maj_totals)

    print(f"  EG majority (fixed reference):   {eg_maj_fixed:+.6f}")
    print(f"  SZAT observed:                   {szat_score:+.6f}")
    print()

    sw_maj_ed  = swing_va["majority_ed"].values
    sw_min_ed  = swing_va["minority_ed"].values
    sw_ndp     = swing_va["va_ndp"].values
    sw_ucp     = swing_va["va_ucp"].values
    nsw_ed     = non_swing_va["majority_ed"].values
    nsw_ndp    = non_swing_va["va_ndp"].values
    nsw_ucp    = non_swing_va["va_ucp"].values

    # Additive approximation (same logic as szat.py)
    rng_approx = np.random.default_rng(seed)
    approx_scores = np.array([
        swing_deltas[rng_approx.random(n_swing) < 0.5].sum()
        for _ in range(N_FULL_RECOMPUTE)
    ])

    # Full-recompute null (pre-registered procedure)
    rng_full = np.random.default_rng(seed)
    full_scores = np.empty(N_FULL_RECOMPUTE)
    for i in range(N_FULL_RECOMPUTE):
        flip = rng_full.random(n_swing) < 0.5   # True = use minority_ed
        perm_ed = np.where(flip, sw_min_ed, sw_maj_ed)

        # Permuted minority map: swing VAs take perm_ed; non-swing keep majority_ed
        eds  = np.concatenate([perm_ed,  nsw_ed])
        ndps = np.concatenate([sw_ndp,   nsw_ndp])
        ucps = np.concatenate([sw_ucp,   nsw_ucp])
        perm_df = pd.DataFrame({"ed": eds, "ndp": ndps, "ucp": ucps})
        perm_totals = perm_df.groupby("ed", as_index=False).agg(
            ndp=("ndp", "sum"), ucp=("ucp", "sum")
        ).rename(columns={"ed": "ed_name"})
        full_scores[i] = compute_eg(perm_totals) - eg_maj_fixed

    fmt = "{:<35}  {:>+16.6f}  {:>+16.6f}  {:>+10.6f}"
    hdr = "{:<35}  {:>16}  {:>16}  {:>10}"
    print(hdr.format("Metric", "Additive approx", "Full recompute", "Diff"))
    print(hdr.format("-" * 35, "-" * 16, "-" * 16, "-" * 10))

    metrics = [
        ("Mean",
            float(np.mean(approx_scores)),         float(np.mean(full_scores))),
        ("Std dev",
            float(np.std(approx_scores)),           float(np.std(full_scores))),
        ("2.5th pct",
            float(np.percentile(approx_scores,  2.5)), float(np.percentile(full_scores,  2.5))),
        ("97.5th pct",
            float(np.percentile(approx_scores, 97.5)), float(np.percentile(full_scores, 97.5))),
        ("p-val (two-tailed vs szat_score)",
            float(np.mean(np.abs(approx_scores) >= abs(szat_score))),
            float(np.mean(np.abs(full_scores)   >= abs(szat_score)))),
    ]
    for label, a, f in metrics:
        print(fmt.format(label, a, f, a - f))

    approx_p = float(np.mean(np.abs(approx_scores) >= abs(szat_score)))
    full_p   = float(np.mean(np.abs(full_scores)   >= abs(szat_score)))
    both_sig = approx_p < 0.05 and full_p < 0.05
    qualitative_agree = both_sig or (approx_p >= 0.05 and full_p >= 0.05)

    print()
    print(f"  Qualitative agreement (a=0.05):  {'PASS' if qualitative_agree else 'FAIL'}")
    print()
    print("  NOTE: Additive approx null ~ direct swing effects only (mean ~ szat/2).")
    print("        Full-recompute null ~ EG(perm_minority) - EG(majority_fixed).")
    print("        Both compare against szat_score which includes direct + indirect effects.")


# ── Check 4: Unconstrained null — population MAD sensitivity (O2 defense) ─────

N_POP_SENSITIVITY = 500
PROV_POP = 4_262_635  # Alberta 2021 census population used in audit


def check_unconstrained_null_population(summary: dict, va: pd.DataFrame) -> bool:
    """
    Adversarial-audit O2 defense: verify that the Bernoulli(0.5) unconstrained
    null does not produce wildly imbalanced maps, making the unconstrained null
    empirically defensible for the actual swing-zone geography.

    For each of N_POP_SENSITIVITY bootstrap permutations (same seed as main boot):
      - compute the population of each resulting ED in the permuted minority map
      - record population MAD from the provincial per-ED average

    If >=95% of permutations have population MAD <= 2× the real minority map's
    population MAD, the unconstrained null is empirically defensible.

    Uses VA-level population (va_pop column if present; falls back to uniform
    scaling from vote totals as a proxy — votes ∝ population in this dataset).
    """
    print()
    print("=" * 60)
    print("CHECK 4 -- Unconstrained null population balance (O2 defense)")
    print(f"  ({N_POP_SENSITIVITY} permutations, same canonical seed)")
    print("=" * 60)

    # Prefer va_pop if present; otherwise scale votes as population proxy
    if "va_pop" in va.columns:
        va = va.copy()
        pop_col = "va_pop"
    else:
        va = va.copy()
        va["va_pop"] = va["va_ndp"] + va["va_ucp"]
        pop_col = "va_pop"
        print("  NOTE: va_pop column absent — using vote total as population proxy")

    swing_mask   = va["is_swing"].values.astype(bool)
    swing_va     = va[swing_mask].reset_index(drop=True)
    non_swing_va = va[~swing_mask].reset_index(drop=True)

    sw_maj_ed  = swing_va["majority_ed"].values
    sw_min_ed  = swing_va["minority_ed"].values
    sw_pop     = swing_va[pop_col].values
    nsw_ed     = non_swing_va["majority_ed"].values
    nsw_pop    = non_swing_va[pop_col].values

    # Real minority map population MAD
    real_min_df = pd.DataFrame({
        "ed":  np.concatenate([swing_va["minority_ed"].values, nsw_ed]),
        "pop": np.concatenate([sw_pop, nsw_pop]),
    })
    real_ed_pops = real_min_df.groupby("ed")["pop"].sum()
    n_eds = len(real_ed_pops)
    avg_pop = real_ed_pops.mean()
    real_mad = float(np.mean(np.abs(real_ed_pops.values - avg_pop)))

    print(f"  Real minority map:  n_EDs={n_eds}  avg_pop={avg_pop:,.0f}  MAD={real_mad:,.0f}")
    print(f"  Threshold (2× real MAD): {2 * real_mad:,.0f}")

    try:
        sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
        from drand_seed import get_canonical_seed
        seed = get_canonical_seed("szat-bootstrap")
    except Exception as _e:
        raise RuntimeError("drand_seed unavailable — cannot reproduce seed") from _e

    rng = np.random.default_rng(seed)
    perm_mads = np.empty(N_POP_SENSITIVITY)
    for i in range(N_POP_SENSITIVITY):
        flip = rng.random(len(sw_maj_ed)) < 0.5
        perm_ed  = np.where(flip, sw_min_ed, sw_maj_ed)
        eds  = np.concatenate([perm_ed, nsw_ed])
        pops = np.concatenate([sw_pop, nsw_pop])
        ed_pops = pd.Series(pops).groupby(pd.Series(eds)).sum()
        perm_mads[i] = float(np.mean(np.abs(ed_pops.values - avg_pop)))

    pct_within = float(np.mean(perm_mads <= 2 * real_mad))
    median_perm_mad = float(np.median(perm_mads))
    max_perm_mad    = float(np.max(perm_mads))

    print(f"  Permutation MAD:    median={median_perm_mad:,.0f}  max={max_perm_mad:,.0f}")
    print(f"  Within 2× real MAD: {pct_within:.1%} of {N_POP_SENSITIVITY} permutations")
    print()

    passed = pct_within >= 0.95
    print(f"  O2 defense (>=95% within 2× real MAD):  {'PASS' if passed else 'FAIL'}")
    if not passed:
        print("  WARNING: Unconstrained null produces population imbalance in many")
        print("  permutations. Consider a constrained null for the SZAT bootstrap.")
    else:
        print("  Interpretation: Bernoulli(0.5) swing-zone shuffle preserves near-")
        print("  balance in >=95% of draws — unconstrained null is defensible here.")
    return passed


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Loading results...")
    va = pd.read_csv(RESULTS_CSV)
    with open(SUMMARY_JSON) as f:
        summary = json.load(f)
    print(f"  {len(va)} VAs ({int(va['is_swing'].sum())} swing)")
    print()

    ok3 = check_attribution(summary, va)
    check_bootstrap_approximation(summary, va)
    ok4 = check_unconstrained_null_population(summary, va)

    print()
    print("=" * 60)
    print(f"Summary: {'Attribution PASS' if ok3 else 'Attribution FAIL'} | "
          f"{'Pop-balance PASS' if ok4 else 'Pop-balance FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
