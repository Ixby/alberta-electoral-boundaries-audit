# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
palette.py — canonical colour palette for the Alberta Electoral Boundary Audit.

Convention
----------
  MINORITY_*  →  minority 2026 commission map  (purple family)
  MAJORITY_*  →  majority 2026 commission map  (teal family)

Import this module; do not redeclare these constants in individual scripts.
The palette is the single source of truth for all audit visualisations and
the HTML report.  It is not user-facing; values propagate at build/render time.

Backward:
  (none — utility module / constants; no data inputs)

Forward:
  (any analysis/scripts/*.py that builds figures or maps; broad utility import.
   Concrete importers found by `grep -rln "from .*palette import\\|palette\\." analysis/scripts/`.
   Renaming a constant here requires checking that grep first.)
"""

# ---------------------------------------------------------------------------
# Primary map-identity colours
# ---------------------------------------------------------------------------
MINORITY_PURPLE       = "#6B35A7"   # minority 2026 — medium dark purple
MINORITY_PURPLE_LIGHT = "#EDE3F7"   # light fill for minority zones / callouts
# MAJORITY_TEAL raised from #1A7A6E on 2026-07-08: the old value sat below the
# chroma floor in the dataviz six-check validator (OKLCh C 0.086 < 0.1 — reads
# gray-ish); #0F8A78 passes all checks and keeps CVD separation vs the purple
# at deltaE 52 (deutan). Same teal family — "teal" references remain accurate.
MAJORITY_TEAL         = "#0F8A78"   # majority 2026 — teal (complementary)
MAJORITY_TEAL_LIGHT   = "#D0EEEA"   # light fill for majority zones / callouts

# ---------------------------------------------------------------------------
# Segment palettes — categorical shades within each map (city-split charts)
# ---------------------------------------------------------------------------
MINORITY_SEGMENT_COLORS = ("#6B35A7", "#8F55C9", "#4D2080", "#B48CD9")
MAJORITY_SEGMENT_COLORS = ("#0F8A78", "#2EA594", "#115249", "#5CBDB0")

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

# ---------------------------------------------------------------------------
# Site-integration tokens (added 2026-07-13) — published figures inherit the
# viewer's design language instead of matplotlib's. Values mirror the CSS
# tokens in viewer/src/routes/+page.svelte (:root, light theme); keep in sync.
# ---------------------------------------------------------------------------
PAPER_BG   = "#f9f7f2"  # viewer --bg (light): the warm paper the page sits on
INK_TEXT   = "#1a1a1a"  # viewer --text
INK_MUTED  = "#444444"  # viewer --text-muted
INK_SUBTLE = "#666666"  # viewer --text-subtle

# The site's font stacks, written into the SVGs so figure text is rendered by
# the reader's browser in the same faces as the surrounding page. Figures are
# laid out with a metrically-similar local face (Arial ~ Segoe UI) and saved
# with svg.fonttype='none' so text stays live text rather than outlined paths.
SITE_SANS_STACK  = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
SITE_SERIF_STACK = "'Palatino Linotype', Palatino, Georgia, 'Times New Roman', serif"

# Local layout faces matplotlib may resolve and write into the SVG; the
# harmonizer rewrites each to the corresponding site stack. Serif faces are
# handled first so multi-word names never partially match a sans pass.
_SERIF_LAYOUT_FACES = ("Palatino Linotype", "Playfair Display", "Source Serif 4",
                       "Georgia", "Lora", "DejaVu Serif", "Times New Roman")
_SANS_LAYOUT_FACES  = ("Source Sans 3", "Source Sans Pro", "DejaVu Sans",
                       "Helvetica", "Arial")


def harmonize_svg(path) -> None:
    """Rewrite an SVG's font-family declarations to the site's stacks.

    matplotlib (svg.fonttype='none') writes the resolved local font name into
    each text element's style attribute (e.g. ``font: 700 9.5px 'Arial'``);
    this swaps those names for the viewer's full CSS stacks so the browser
    renders figure text in the page's own faces, with graceful fallback.
    """
    from pathlib import Path as _P
    p = _P(path)
    svg = p.read_text(encoding="utf-8")
    # Two-phase substitution via sentinels: the site stacks themselves contain
    # face names from the layout lists ('Times New Roman', Arial), so direct
    # replacement would recursively re-expand text just inserted.
    SERIF_TOK, SANS_TOK = "\x00SERIF\x00", "\x00SANS\x00"
    for face in _SERIF_LAYOUT_FACES:
        svg = svg.replace(f"'{face}'", SERIF_TOK)
    for face in _SANS_LAYOUT_FACES:
        svg = svg.replace(f"'{face}'", SANS_TOK)
    # Collapse fallback lists (e.g. TOK, TOK, sans-serif) to one token, then
    # drop the now-redundant trailing generic.
    for tok, generic in ((SERIF_TOK, "serif"), (SANS_TOK, "sans-serif")):
        while f"{tok}, {tok}" in svg:
            svg = svg.replace(f"{tok}, {tok}", tok)
        svg = svg.replace(f"{tok}, {generic}", tok)
    svg = svg.replace(SERIF_TOK, SITE_SERIF_STACK).replace(SANS_TOK, SITE_SANS_STACK)
    p.write_text(svg, encoding="utf-8")


def save_fig(fig, out_path, facecolor: str = PAPER_BG, pad_inches: float = 0.10,
             tight: bool = True):
    """House savefig: paper background, live site-font text, optional tight bbox.

    ``tight=False`` preserves a figure's full composed canvas (schematics laid
    out on fixed geometry). Also writes a PNG preview alongside when the
    AUDIT_FIG_PNG_PREVIEW env var names a directory — visual QA without
    committing raster copies.
    """
    import os
    from pathlib import Path as _P
    out_path = _P(out_path)
    kw = dict(dpi=300, facecolor=facecolor)
    if tight:
        kw.update(bbox_inches="tight", pad_inches=pad_inches)
    fig.savefig(out_path, **kw)
    if out_path.suffix.lower() == ".svg":
        harmonize_svg(out_path)
    preview_dir = os.environ.get("AUDIT_FIG_PNG_PREVIEW")
    if preview_dir:
        _P(preview_dir).mkdir(parents=True, exist_ok=True)
        kw["dpi"] = 150
        fig.savefig(_P(preview_dir) / (out_path.stem + ".png"), **kw)
    return out_path
