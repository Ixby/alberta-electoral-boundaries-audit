import pytest

def decompose_bias(eg_actual, eg_neutral_median):
    """
    Decomposes the absolute partisan lean into geography and drawing components.
    """
    draw_component = eg_actual - eg_neutral_median
    return {
        "geography": eg_neutral_median,
        "drawing": draw_component
    }

def test_absolute_level_decomposition():
    eg_actual_minority = -0.027  # -2.7%
    eg_neutral_median = -0.020   # -2.0%
    
    decomp = decompose_bias(eg_actual_minority, eg_neutral_median)
    
    assert decomp["geography"] == -0.020
    assert pytest.approx(decomp["drawing"]) == -0.007  # The drawing tips the scales by an additional -0.7%
