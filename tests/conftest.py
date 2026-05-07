"""Pytest Configuration and Shared Fixtures.

This file defines centralized input data and shared testing resources
so they can be defined in one spot and injected into any test across 
the entire test suite.
"""

import pytest
from shapely.geometry import Polygon

@pytest.fixture
def sample_ed_results():
    """Provides a standard set of Electoral District vote results.
    
    Useful for partisan symmetry, marginal seats, and threshold testing.
    """
    return [
        {"ed": "ED_NDP_SAFE", "region": "Urban", "ndp": 70, "ucp": 30},
        {"ed": "ED_NDP_MARGINAL", "region": "Urban", "ndp": 52, "ucp": 48},
        {"ed": "ED_UCP_MARGINAL", "region": "Rural", "ndp": 48, "ucp": 52},
        {"ed": "ED_UCP_SAFE", "region": "Rural", "ndp": 20, "ucp": 80},
    ]

@pytest.fixture
def standard_shapes():
    """Provides geometrically exact test shapes.
    
    Useful for compactness, convexity, and structural tests.
    """
    return {
        "square": Polygon([(0, 0), (0, 2), (2, 2), (2, 0)]),  # Area 4, Perimeter 8
        "rectangle": Polygon([(0, 0), (0, 2), (4, 2), (4, 0)]), # Area 8, Perimeter 12
        "l_shape": Polygon([(0, 0), (0, 4), (2, 4), (2, 2), (4, 2), (4, 0)]) # Area 12, Perimeter 16
    }

@pytest.fixture
def demographic_blocks():
    """Provides standardized census block allocations for Ecological Inference."""
    return [
        {"va": "VA_1", "pop_total": 1000, "pop_target": 800, "ndp_votes": 750, "ucp_votes": 50},
        {"va": "VA_2", "pop_total": 1000, "pop_target": 100, "ndp_votes": 300, "ucp_votes": 600},
    ]
