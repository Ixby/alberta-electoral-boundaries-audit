"""Cycle dataclass for comparing EG asymmetry across Canadian redistribution cycles.

Situates Alberta 2026 against comparable provincial redistribution cycles. The
proxy EG-asymmetry applies a 0.455x deflator to the seat-share asymmetry,
calibrated to the measured 0.51 pp EG asymmetry for the Alberta 2026 cycle.

No file I/O: pure dataclass, takes constructor arguments only.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cycle:
    """One redistribution cycle comparison."""

    jurisdiction: str
    cycle_year: str
    map_a_label: str
    map_b_label: str
    seats_total: int
    seat_flips_estimate: Optional[float]
    seat_flips_low: Optional[float] = None
    seat_flips_high: Optional[float] = None

    @property
    def seat_share_asymmetry_pp(self) -> Optional[float]:
        """seat_flips / seats_total * 100, or None if estimate is absent."""
        if self.seat_flips_estimate is None:
            return None
        return self.seat_flips_estimate / self.seats_total * 100

    @property
    def eg_asymmetry_proxy_pp(self) -> Optional[float]:
        """seat_share_asymmetry_pp * 0.455 deflator, or None."""
        if self.seat_flips_estimate is None:
            return None
        return self.seat_share_asymmetry_pp * 0.455

    @property
    def eg_asymmetry_low_pp(self) -> Optional[float]:
        """Lower-bound EG proxy using seat_flips_low, or None."""
        if self.seat_flips_low is None:
            return None
        return self.seat_flips_low / self.seats_total * 100 * 0.455

    @property
    def eg_asymmetry_high_pp(self) -> Optional[float]:
        """Upper-bound EG proxy using seat_flips_high, or None."""
        if self.seat_flips_high is None:
            return None
        return self.seat_flips_high / self.seats_total * 100 * 0.455
