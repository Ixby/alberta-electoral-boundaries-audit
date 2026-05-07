"""Pytest suite for geometric compactness metrics.

Tests Polsby-Popper, Reock, Convex Hull, and Schwartzberg calculations
against known geometric shapes (circles, squares, rectangles) to ensure
the math produces the expected textbook answers, and verifies edge-case handling.

Run from the repo root:
    python -m pytest tests/test_compactness.py -v
"""

import sys
import math
from pathlib import Path

import pytest
from shapely.geometry import Polygon, Point

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from polsby_popper import polsby_popper
from reock import reock
from compactness_metrics import convex_hull_ratio, schwartzberg_score

# ============================================================
# Compactness metric tests
# ============================================================


def test_polsby_popper_circle():
    """A perfect circle should have a Polsby-Popper score of 1.0."""
    circle = Point(0, 0).buffer(1.0, quad_segs=256)
    pp = polsby_popper(circle)
    assert 0.99 < pp <= 1.001


def test_polsby_popper_square(standard_shapes):
    """A square has an area of 4 and perimeter of 8.
    PP = 4 * pi * 4 / (8^2) = ~0.785.
    """
    square = standard_shapes["square"]
    pp = polsby_popper(square)
    assert math.isclose(pp, math.pi / 4, rel_tol=1e-3)


def test_polsby_popper_bacon_strip():
    """A thin 10x1 rectangle (bacon strip gerrymander).
    Area = 10, Perimeter = 22. PP = 40pi / 484 = ~0.259.
    """
    strip = Polygon([(0, 0), (10, 0), (10, 1), (0, 1)])
    pp = polsby_popper(strip)
    assert math.isclose(pp, (40 * math.pi) / 484, rel_tol=1e-3)


def test_reock_circle():
    """A perfect circle should have a Reock score of 1.0."""
    circle = Point(0, 0).buffer(1.0, quad_segs=256)
    d, r = reock(circle)
    assert math.isclose(d, 2.0, rel_tol=1e-2)
    assert 0.99 < r <= 1.001


def test_reock_rectangle(standard_shapes):
    """A 4x2 rectangle has bounding circle diameter sqrt(20).
    Reock = 4 * 8 / (pi * 20) = ~0.509.
    """
    rect = standard_shapes["rectangle"]
    d, r = reock(rect)
    assert math.isclose(d, math.sqrt(20), rel_tol=1e-2)
    assert math.isclose(r, 1.6 / math.pi, rel_tol=1e-2)


def test_convex_hull_ratio(standard_shapes):
    """A convex shape (like a square) is its own convex hull -> score 1.0.
    A concave shape (like a crescent or L-shape) has a score < 1.0.
    """
    square = standard_shapes["square"]
    assert math.isclose(convex_hull_ratio(square), 1.0, rel_tol=1e-5)

    # L-shape: Area = 12
    l_shape = standard_shapes["l_shape"]
    # Convex hull is the 4x4 square missing a 2x2 triangle.
    # Area of hull = 16 - (0.5 * 2 * 2) = 14.
    # Score = 12 / 14 = 6/7 ~= 0.857
    assert math.isclose(convex_hull_ratio(l_shape), 12.0 / 14.0, rel_tol=1e-3)


def test_schwartzberg_score(standard_shapes):
    """Ratio of perimeter to circumference of equal-area circle.
    Circle -> 1.0
    Square -> Area=4, equiv radius=sqrt(4/pi)=~1.128
              Circumference = 2*pi*1.128 = ~7.089
              Perimeter = 8
              Score = 7.089 / 8 = ~0.886
    """
    circle = Point(0, 0).buffer(1.0, quad_segs=256)
    assert 0.99 < schwartzberg_score(circle.area, circle.length) <= 1.001

    square = standard_shapes["square"]
    equiv_circ = 2 * math.pi * math.sqrt(4 / math.pi)
    expected = equiv_circ / 8.0
    assert math.isclose(
        schwartzberg_score(square.area, square.length), expected, rel_tol=1e-3
    )


def test_empty_geometries():
    """Metrics should gracefully handle empty or invalid geometries."""
    empty_poly = Polygon()
    assert math.isnan(polsby_popper(empty_poly))

    d, r = reock(empty_poly)
    assert math.isnan(d) and math.isnan(r)
    assert math.isnan(convex_hull_ratio(empty_poly))
    assert math.isnan(schwartzberg_score(0, 0))
