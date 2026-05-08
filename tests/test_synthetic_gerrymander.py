import pytest

def detect_synthetic_gerrymander(map_results, baseline_median=-0.02):
    """
    Validates that the test battery correctly flags a known synthetic gerrymander
    by checking if its EG significantly deviates from the constraint-bound median.
    """
    eg = map_results["eg"]
    if eg < baseline_median - 0.03: # Arbitrary threshold for synthetic flag
        return "GERRYMANDER_UCP"
    elif eg > baseline_median + 0.03:
        return "GERRYMANDER_NDP"
    return "NEUTRAL"

def test_synthetic_detection():
    # We feed the detector a map we specifically drew to pack/crack
    synthetic_gerrymander = {"eg": -0.06} 
    neutral_map = {"eg": -0.022}
    
    assert detect_synthetic_gerrymander(synthetic_gerrymander) == "GERRYMANDER_UCP"
    assert detect_synthetic_gerrymander(neutral_map) == "NEUTRAL"
