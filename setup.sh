#!/usr/bin/env bash
# setup.sh — Install Python dependencies for Phases 4–5
# Idempotent — safe to re-run

set -e

echo "Alberta Boundaries Audit — dependency setup"
echo "==========================================="

python3 -c "import sys; assert sys.version_info >= (3, 9), 'Python 3.9+ required'" || {
    echo "ERROR: Python 3.9 or higher required for geopandas."
    exit 1
}

INSTALL() {
    pip install --quiet --break-system-packages "$@" 2>/dev/null || \
    pip install --quiet "$@"
}

echo "Installing core scientific stack..."
INSTALL pandas numpy openpyxl

echo "Installing GIS stack (Phase 4)..."
INSTALL geopandas shapely fiona pyproj

echo "Installing geocoding (Phase 4C poll-location attribution)..."
INSTALL geopy rapidfuzz

echo "Installing OSM network tools (Phase 4D fallback)..."
INSTALL osmnx

echo "Installing PDF extraction tools (Phase 4B PDF text parsing)..."
INSTALL pdfplumber pypdf

echo "Installing MCMC ensemble tools (Phase 5)..."
INSTALL gerrychain || {
    echo "WARN: gerrychain install failed. Phase 5 (B5 ensemble) will be blocked."
    echo "      You can fall back to R's redist package via MRU lab software."
}

echo ""
echo "Verifying critical imports..."
python3 << 'PYEOF'
checks = [
    ('pandas', 'core'),
    ('numpy', 'core'),
    ('openpyxl', 'Phase 4C Statement of Vote parsing'),
    ('geopandas', 'Phase 4 GIS'),
    ('geopy', 'Phase 4C geocoding (Nominatim fallback)'),
    ('rapidfuzz', 'Phase 4C landmark dictionary fuzzy matching'),
    ('osmnx', 'Phase 4D street network'),
    ('pdfplumber', 'Phase 4B PDF parsing'),
    ('gerrychain', 'Phase 5 MCMC ensemble'),
]
for mod, purpose in checks:
    try:
        __import__(mod)
        print(f"  {mod:12s} OK ({purpose})")
    except ImportError:
        print(f"  {mod:12s} MISSING — {purpose} disabled")
PYEOF

echo ""
echo "Setup complete. Next: launch Claude Code with 'claude --effort xhigh'"
echo "Claude Code will read CLAUDE.md and follow v0_8_gerrymander_audit_prompt.md"
