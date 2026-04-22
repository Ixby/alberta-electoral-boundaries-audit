"""
Monte Carlo Confidence Interval over Modeling Choices
======================================================
v0.3 — fortification of v0.2 pointwise sensitivity

Answers the critic's question: "How do you know the 0.58 pp asymmetry
is distinguishable from zero, given your modeling uncertainty?"

Samples:
  - urban_weight ~ Uniform(0.55, 0.85)
  - rural_ndp_share ~ Uniform(0.26, 0.36)  (empirical range of rural
    Alberta NDP two-party share across 2015, 2019, 2023 elections.
    Observed: 26.47% (2019), 33.47% (2023), 35.05% (2015).
    See analysis/v0_1_cross_election_rural_baseline.py.)
  - per-hybrid jitter: each hybrid's urban_weight independently
    sampled from Uniform(urban_weight - 0.10, urban_weight + 0.10),
    clipped to [0.40, 0.95]

For each sample:
  1. Build majority and minority estimates using per-hybrid jittered weights
  2. Compute B2 efficiency gap for each map
  3. Record the minority - majority EG asymmetry

After N = 2,000 samples, report:
  - Mean asymmetry
  - 95% CI (2.5th and 97.5th percentiles)
  - Fraction of runs with same-sign asymmetry (directional consistency)

A directional claim is defensible if the 95% CI does not cross zero.
"""
from __future__ import annotations
import random
import statistics
from copy import deepcopy

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from v0_2_packing_cracking_analysis import (
    load_2023_results, compute_metrics,
    MAJORITY_2026_MAPPING, MINORITY_2026_MAPPING,
    estimate_2026,
)


def jittered_mapping(mapping: dict, base_weight: float, jitter: float, rng: random.Random) -> dict:
    """Return a copy of mapping with each 'blend' entry's urban weight jittered."""
    out = {}
    for new_ed, spec in mapping.items():
        if spec[0] == 'blend':
            w = max(0.40, min(0.95, base_weight + rng.uniform(-jitter, jitter)))
            out[new_ed] = ('blend', spec[1], w)
        elif spec[0] == 'split':
            w = max(0.40, min(0.95, base_weight + rng.uniform(-jitter, jitter)))
            out[new_ed] = ('split', spec[1], w, spec[3])
        else:
            out[new_ed] = spec
    return out


def run_monte_carlo(n_samples: int = 2000, seed: int = 42) -> dict:
    rng = random.Random(seed)
    dists_2019 = load_2023_results()

    results = {
        'maj_eg': [],
        'min_eg': [],
        'asymmetry': [],
        'maj_ndp50': [],
        'min_ndp50': [],
        'maj_dec': [],
        'min_dec': [],
    }

    for i in range(n_samples):
        base_w = rng.uniform(0.55, 0.85)
        rural = rng.uniform(0.26, 0.36)
        jitter = 0.10

        maj_map = jittered_mapping(MAJORITY_2026_MAPPING, base_w, jitter, rng)
        min_map = jittered_mapping(MINORITY_2026_MAPPING, base_w, jitter, rng)

        maj = estimate_2026(dists_2019, maj_map, rural)
        minr = estimate_2026(dists_2019, min_map, rural)

        if len(maj) != 89 or len(minr) != 89:
            continue  # skip invalid sample

        m_maj = compute_metrics(maj, 'maj', verbose=False)
        m_min = compute_metrics(minr, 'min', verbose=False)

        results['maj_eg'].append(m_maj['eg'] * 100)
        results['min_eg'].append(m_min['eg'] * 100)
        results['asymmetry'].append((m_min['eg'] - m_maj['eg']) * 100)
        results['maj_ndp50'].append(m_maj['ndp_at_50'])
        results['min_ndp50'].append(m_min['ndp_at_50'])
        if m_maj['declination'] == m_maj['declination']:
            results['maj_dec'].append(m_maj['declination'])
        if m_min['declination'] == m_min['declination']:
            results['min_dec'].append(m_min['declination'])

    return results


def summarize(label: str, values: list):
    if not values:
        print(f"  {label:<30s} : no samples")
        return
    values_sorted = sorted(values)
    n = len(values_sorted)
    p025 = values_sorted[int(n * 0.025)]
    p50  = values_sorted[int(n * 0.500)]
    p975 = values_sorted[int(n * 0.975)]
    mn = statistics.mean(values)
    same_sign = sum(1 for v in values if (v > 0) == (mn > 0)) / n * 100
    print(f"  {label:<30s} : mean={mn:+.3f}  median={p50:+.3f}  "
          f"95% CI=[{p025:+.3f}, {p975:+.3f}]  "
          f"direction consistency={same_sign:.1f}%")


def main():
    print("=" * 70)
    print("  Monte Carlo Confidence Intervals — Modeling Uncertainty")
    print("=" * 70)
    print()
    print("Sampling:")
    print("  base urban_weight ~ Uniform(0.55, 0.85)")
    print("  rural_ndp_share ~ Uniform(0.26, 0.36)  [from 2015/2019/2023 observed]")
    print("  per-hybrid jitter ~ Uniform(-0.10, +0.10)")
    print("  N = 2,000 samples; seed = 42 (reproducible)")
    print()

    results = run_monte_carlo(n_samples=2000, seed=42)

    print(f"Samples collected: {len(results['asymmetry'])}")
    print()
    print("Per-map metrics:")
    summarize("Majority EG (%)", results['maj_eg'])
    summarize("Minority EG (%)", results['min_eg'])
    summarize("Majority NDP@50/50", results['maj_ndp50'])
    summarize("Minority NDP@50/50", results['min_ndp50'])
    summarize("Majority declination", results['maj_dec'])
    summarize("Minority declination", results['min_dec'])
    print()
    print("Minority - Majority asymmetry (the audit's headline claim):")
    summarize("Asymmetry EG (pp)", results['asymmetry'])

    # Directional consistency test
    asym = results['asymmetry']
    neg = sum(1 for v in asym if v < 0)
    pos = sum(1 for v in asym if v > 0)
    zero_cross = sum(1 for v in asym if -0.05 < v < 0.05)

    print()
    print("=" * 70)
    print("  FALSIFIABILITY OUTCOME")
    print("=" * 70)
    print(f"  Samples with minority more UCP-favorable (negative): {neg}/{len(asym)} ({neg/len(asym)*100:.1f}%)")
    print(f"  Samples with minority less UCP-favorable (positive): {pos}/{len(asym)} ({pos/len(asym)*100:.1f}%)")
    print(f"  Samples within +/- 0.05 pp of zero:                  {zero_cross}/{len(asym)} ({zero_cross/len(asym)*100:.1f}%)")
    if asym:
        ci_lo = sorted(asym)[int(len(asym) * 0.025)]
        ci_hi = sorted(asym)[int(len(asym) * 0.975)]
        if ci_lo < 0 and ci_hi < 0:
            print(f"  VERDICT: 95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}] pp is entirely negative.")
            print(f"           Directional claim DEFENSIBLE under modeling uncertainty.")
        elif ci_lo > 0 and ci_hi > 0:
            print(f"  VERDICT: 95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}] pp is entirely positive.")
            print(f"           Directional claim reversed.")
        else:
            print(f"  VERDICT: 95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}] pp crosses zero.")
            print(f"           Directional claim NOT defensible under full modeling uncertainty.")


def cross_check_2019_votes():
    """Apply same methodology using 2019 votes as input (instead of 2023)
    to check whether the asymmetry direction is election-specific or
    stable across elections.
    """
    import csv, os
    here = os.path.dirname(os.path.abspath(__file__))
    path_2019 = os.path.join(here, '..', 'data', 'v0_1_alberta_2019_results.csv')

    # Load 2019 per-ED NDP/UCP totals
    dists_2019_votes = []
    with open(path_2019) as f:
        for r in csv.DictReader(f):
            ndp = ucp = 0
            for i in range(1, 9):
                cand = r.get(f'cand_{i}', '') or ''
                votes_s = r.get(f'votes_{i}', '') or ''
                if not cand or not votes_s:
                    continue
                try:
                    v = int(votes_s)
                except ValueError:
                    continue
                if cand.endswith('(NDP)'):
                    ndp = v
                elif cand.endswith('(UCP)'):
                    ucp = v
            if ndp + ucp == 0:
                continue
            dists_2019_votes.append({
                'ed': r['ed_name'], 'region': r['region'],
                'ndp': ndp, 'ucp': ucp,
            })

    print("=" * 70)
    print("  CROSS-CHECK: Same methodology with 2019 votes as input")
    print("=" * 70)
    print(f"  Loaded {len(dists_2019_votes)} districts from 2019 results")

    # Compute 2019-vote rural baseline
    rural = [d for d in dists_2019_votes if d['region'] == 'Rest of Alberta']
    rural_ndp_2019 = sum(d['ndp'] for d in rural) / sum(d['ndp']+d['ucp'] for d in rural)
    print(f"  Rural NDP share in 2019: {rural_ndp_2019*100:.1f}%")
    print(f"  (2023 rural NDP share was 33.5% — 2019 likely higher given NDP won in 2015)")
    print()

    # Estimate 2026 maps using 2019 votes
    from v0_2_packing_cracking_analysis import estimate_2026, compute_metrics
    maj = estimate_2026(dists_2019_votes, MAJORITY_2026_MAPPING, rural_ndp_2019)
    minr = estimate_2026(dists_2019_votes, MINORITY_2026_MAPPING, rural_ndp_2019)

    print("  2019-vote metrics:")
    m_2019 = compute_metrics(dists_2019_votes, "2019 map, 2019 votes", verbose=False)
    m_maj = compute_metrics(maj, "Majority 2026, 2019 votes", verbose=False)
    m_min = compute_metrics(minr, "Minority 2026, 2019 votes", verbose=False)

    print(f"    2019 map (actual):  NDP {m_2019['ndp_seats']}/UCP {m_2019['ucp_seats']}, EG {m_2019['eg']*100:+.2f}%, MM {m_2019['mm_gap']*100:+.2f}pp")
    print(f"    Majority 2026 (est): NDP {m_maj['ndp_seats']}/UCP {m_maj['ucp_seats']}, EG {m_maj['eg']*100:+.2f}%, MM {m_maj['mm_gap']*100:+.2f}pp")
    print(f"    Minority 2026 (est): NDP {m_min['ndp_seats']}/UCP {m_min['ucp_seats']}, EG {m_min['eg']*100:+.2f}%, MM {m_min['mm_gap']*100:+.2f}pp")
    asym_2019 = (m_min['eg'] - m_maj['eg']) * 100
    print()
    print(f"  Minority-Majority EG asymmetry under 2019 votes: {asym_2019:+.2f} pp")
    print(f"  (2023 votes produced asymmetry of -0.58 pp at 70/30 weight)")
    print()
    if asym_2019 < 0:
        print(f"  CROSS-ELECTION CONSISTENCY: Direction matches across 2019 and 2023.")
    else:
        print(f"  CROSS-ELECTION INCONSISTENCY: Direction flips between 2019 and 2023.")


if __name__ == '__main__':
    main()
    print()
    cross_check_2019_votes()
