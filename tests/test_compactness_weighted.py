import pytest
import math
from shapely.geometry import Polygon

def calculate_compactness_weighted_eg(ed_results, ed_shapes):
    """
    Weights each ED's contribution to Efficiency Gap by its irregularity.
    """
    w_sum = 0
    eg_sum = 0
    
    # Assume median PP is 0.5 for this mock
    median_pp = 0.5
    
    for ed in ed_results:
        name = ed["ed"]
        shape = ed_shapes.get(name)
        if not shape: continue
        
        # Polsby-Popper = 4 * pi * Area / Perimeter^2
        pp = (4 * math.pi * shape.area) / (shape.length ** 2)
        
        # Weight = 1 - (PP / median_pp), bounded [0, 1]
        w = max(0, min(1, 1 - (pp / median_pp)))
        
        # Mock EG contribution
        # Wasted votes calculation
        total = ed["ndp"] + ed["ucp"]
        if ed["ndp"] > ed["ucp"]:
            wasted_ndp = ed["ndp"] - (total / 2)
            wasted_ucp = ed["ucp"]
        else:
            wasted_ucp = ed["ucp"] - (total / 2)
            wasted_ndp = ed["ndp"]
            
        # negative = UCP advantage, positive = NDP advantage
        eg_i = (wasted_ucp - wasted_ndp) / total
        
        w_sum += w
        eg_sum += w * eg_i
        
    return eg_sum / w_sum if w_sum > 0 else 0

def test_compactness_weighted_bias():
    ed_results = [
        {"ed": "ED_REGULAR", "ndp": 60, "ucp": 40}, # NDP win
        {"ed": "ED_IRREGULAR", "ndp": 48, "ucp": 52} # UCP win
    ]
    ed_shapes = {
        "ED_REGULAR": Polygon([(0, 0), (0, 10), (10, 10), (10, 0)]), # Square, high PP
        "ED_IRREGULAR": Polygon([(0, 0), (0, 10), (2, 10), (2, 2), (10, 2), (10, 0)]) # L-shape, low PP
    }
    
    cw_eg = calculate_compactness_weighted_eg(ed_results, ed_shapes)
    # Irregular ED should dominate the weighted EG
    assert cw_eg < 0 # UCP favored in the irregular ED
