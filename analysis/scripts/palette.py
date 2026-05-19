"""
palette.py — canonical colour palette for the Alberta Electoral Boundary Audit.

Convention
----------
  MINORITY_*  →  minority 2026 commission map  (purple family)
  MAJORITY_*  →  majority 2026 commission map  (teal family)

Import this module; do not redeclare these constants in individual scripts.
The palette is the single source of truth for all audit visualisations and
the HTML report.  It is not user-facing; values propagate at build/render time.
"""

# ---------------------------------------------------------------------------
# Primary map-identity colours
# ---------------------------------------------------------------------------
MINORITY_PURPLE       = "#6B35A7"   # minority 2026 — medium dark purple
MINORITY_PURPLE_LIGHT = "#EDE3F7"   # light fill for minority zones / callouts
MAJORITY_TEAL         = "#1A7A6E"   # majority 2026 — dark teal (complementary)
MAJORITY_TEAL_LIGHT   = "#D0EEEA"   # light fill for majority zones / callouts

# ---------------------------------------------------------------------------
# Segment palettes — categorical shades within each map (city-split charts)
# ---------------------------------------------------------------------------
MINORITY_SEGMENT_COLORS = ("#6B35A7", "#8F55C9", "#4D2080", "#B48CD9")
MAJORITY_SEGMENT_COLORS = ("#1A7A6E", "#2EA594", "#115249", "#5CBDB0")

# ---------------------------------------------------------------------------
# Party reference colours — do not use for map identity
# ---------------------------------------------------------------------------
NDP_ORANGE = "#EA7414"
UCP_BLUE   = "#225D9E"

# ---------------------------------------------------------------------------
# Structural / neutral colours
# ---------------------------------------------------------------------------
NEUTRAL_2019  = "#666666"
RULE_GREY     = "#888888"
TEXT_DARK     = "#1A1A1A"
THRESHOLD_RED = "#7B2D3E"   # Alberta-calibrated p95 threshold line
NORM_BAND     = "#D8D4E8"   # neutral ensemble norm band (muted lavender-grey)
