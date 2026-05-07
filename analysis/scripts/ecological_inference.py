"""
Ecological Inference (EI) Stub
------------------------------
Estimates voting patterns by demographic group using Bayesian methods
or King's Ecological Inference model. This is heavily used in Voting
Rights Act (VRA) Section 2 compliance tests to prove Racially Polarized
Voting (RPV).

Note: Full implementation requires PyMC or specialized R libraries.
This provides the deterministic Duncan & Davis bounds for the test suite.
"""

import numpy as np


def run_ei_bounds(
    demographic_fraction: np.ndarray, party_vote_fraction: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes Duncan & Davis bounds (the absolute mathematical limits)
    for ecological inference.

    X = fraction of population that is in the demographic group.
    Y = fraction of total vote received by the party.

    Returns (lower_bounds, upper_bounds) for the demographic group's
    support for the party.
    """
    X = np.asarray(demographic_fraction)
    Y = np.asarray(party_vote_fraction)

    # Avoid division by zero
    X_safe = np.where(X > 0, X, 1.0)

    # Lower bound: max(0, (Y - (1 - X)) / X)
    lower = np.maximum(0.0, (Y - (1.0 - X)) / X_safe)

    # Upper bound: min(1, Y / X)
    upper = np.minimum(1.0, Y / X_safe)

    # If X == 0, the bounds are technically undefined/meaningless. We return 0.
    lower = np.where(X == 0, 0.0, lower)
    upper = np.where(X == 0, 0.0, upper)

    return lower, upper
