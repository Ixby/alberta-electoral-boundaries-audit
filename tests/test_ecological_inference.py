"""Pytest suite for Ecological Inference / VRA Compliance metrics.

Tests the deterministic bounds (Duncan & Davis) used to establish limits
on racially polarized voting estimates.

Run from the repo root:
    python -m pytest tests/test_ecological_inference.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pytest
import math

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from ecological_inference import run_ei_bounds

# ============================================================
# Ecological Inference bounds tests
# ============================================================


def test_ei_bounds(demographic_blocks):
    """Test Duncan & Davis deterministic bounds for EI."""
    # Convert demographic_blocks fixture into X (demographic fraction) and Y (vote fraction)
    # block 0: pop 1000, target 800 (80%), ndp 750 (75%)
    # block 1: pop 1000, target 100 (10%), ndp 300 (30%)
    
    # We will test the existing explicit vectors as they precisely test mathematical bounds
    # but we can structure them using the fixture data concept.
    
    # District 1: Demographic is 80% of pop, Party gets 90% of vote.
    # Min support = (0.9 - 0.2)/0.8 = 0.875
    # Max support = 0.9/0.8 -> capped at 1.0

    # District 2: Demographic is 20% of pop, Party gets 10% of vote.
    # Min support = (0.1 - 0.8)/0.2 = <0 -> capped at 0.0
    # Max support = 0.1/0.2 = 0.5

    X = np.array([0.8, 0.2])
    Y = np.array([0.9, 0.1])

    lower, upper = run_ei_bounds(X, Y)

    assert math.isclose(lower[0], 0.875, abs_tol=1e-5)
    assert math.isclose(upper[0], 1.0, abs_tol=1e-5)

    assert math.isclose(lower[1], 0.0, abs_tol=1e-5)
    assert math.isclose(upper[1], 0.5, abs_tol=1e-5)


def test_ei_bounds_edge_cases():
    """Test empty/zero populations."""
    X = np.array([0.0, 1.0])
    Y = np.array([0.5, 0.5])

    lower, upper = run_ei_bounds(X, Y)

    # Where X=0, bounds are meaningless, function returns 0
    assert lower[0] == 0.0
    assert upper[0] == 0.0

    # Where X=1, bounds should perfectly match Y
    assert math.isclose(lower[1], 0.5, abs_tol=1e-5)
    assert math.isclose(upper[1], 0.5, abs_tol=1e-5)
