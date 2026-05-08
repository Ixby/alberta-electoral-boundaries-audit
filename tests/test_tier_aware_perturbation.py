import pytest
import numpy as np

def simulate_tier_aware_perturbation(polygons, iterations=100):
    """
    Simulates perturbing boundaries based on their provenance tier.
    Tier A (2019 parent): 0m uncertainty
    Tier B (Calibrated sweep/osm): 50m uncertainty
    Tier C (Visual v7): 300m uncertainty
    """
    np.random.seed(42) # Determinism for test
    results = []
    for _ in range(iterations):
        total_bias_shift = 0
        for poly in polygons:
            if poly["tier"] == "A":
                shift = np.random.normal(0, 0)
            elif poly["tier"] == "B":
                shift = np.random.normal(0, 50)
            elif poly["tier"] == "C":
                shift = np.random.normal(0, 300)
            total_bias_shift += shift * poly["voter_density"]
        results.append(total_bias_shift)
    return np.percentile(results, [5, 95])

def test_tier_aware_bounds():
    polygons = [
        {"id": 1, "tier": "A", "voter_density": 0.1},
        {"id": 2, "tier": "B", "voter_density": 0.5},
        {"id": 3, "tier": "C", "voter_density": 0.2},
    ]
    ci_lower, ci_upper = simulate_tier_aware_perturbation(polygons, 500)
    # The bounds should be tight since the heaviest density is in a calibrated tier
    assert ci_upper - ci_lower < 500 
