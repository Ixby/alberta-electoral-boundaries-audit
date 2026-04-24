#!/usr/bin/env bash
# setup.sh — Install Python dependencies for the Alberta Electoral
# Boundaries Audit pipeline. Idempotent — safe to re-run.

set -e

echo "Alberta Electoral Boundaries Audit — dependency setup"
echo "======================================================"

python3 -c "import sys; assert sys.version_info >= (3, 11), 'Python 3.11+ required'" || {
    echo "ERROR: Python 3.11 or higher required."
    exit 1
}

INSTALL() {
    pip install --quiet --break-system-packages "$@" 2>/dev/null || \
    pip install --quiet "$@"
}

echo "Installing core scientific stack..."
INSTALL pandas numpy openpyxl

echo "Installing GIS stack (Phase 4, Stage 2/3)..."
# Modern geopandas uses pyogrio as default backend; fiona not required.
INSTALL geopandas pyogrio shapely pyproj

echo "Installing geocoding + fuzzy matching (Phase 4C poll attribution)..."
INSTALL geopy rapidfuzz

echo "Installing OSM network tools (Phase 4D fallback)..."
INSTALL osmnx

echo "Installing PDF extraction tools (Appendix B/C/E parsing)..."
INSTALL pdfplumber pypdf

echo "Installing MCMC ensemble tools (Phase 5)..."
INSTALL gerrychain || {
    echo "WARN: gerrychain install failed. Phase 5 (B5 ensemble) will be blocked."
}

echo "Installing publication gate tools (readability + voice checks)..."
INSTALL textstat

echo ""
echo "Verifying critical imports..."
python3 << 'PYEOF'
checks = [
    ('pandas', 'core'),
    ('numpy', 'core'),
    ('openpyxl', 'Phase 4C Statement of Vote parsing'),
    ('geopandas', 'Phase 4 GIS'),
    ('pyogrio', 'Phase 4 GIS IO backend'),
    ('geopy', 'Phase 4C geocoding'),
    ('rapidfuzz', 'Phase 4C landmark matching'),
    ('osmnx', 'Phase 4D OSM reconstruction'),
    ('pdfplumber', 'Appendix B/C/E parsing'),
    ('gerrychain', 'Phase 5 MCMC ensemble'),
    ('textstat', 'Publication gate PR2 readability'),
]
for mod, purpose in checks:
    try:
        __import__(mod)
        print(f"  {mod:12s} OK ({purpose})")
    except ImportError:
        print(f"  {mod:12s} MISSING — {purpose} disabled")
PYEOF

echo ""
echo "Reproducibility check — running five baseline scripts:"
echo ""

for script in \
    analysis/scripts/v0_2_packing_cracking_analysis.py \
    analysis/scripts/electoral_forensics_population.py \
    analysis/scripts/v0_3_monte_carlo_ci.py \
    analysis/scripts/v0_1_cross_election_rural_baseline.py \
    analysis/scripts/check_voice_and_readability.py
do
    echo "  $script"
done

echo ""
echo "Setup complete. Next steps:"
echo "  1. PYTHONIOENCODING=utf-8 python3 analysis/scripts/v0_2_packing_cracking_analysis.py"
echo "  2. Verify output matches v1_2_gerrymander_audit_prompt.md carry-forward table."
echo "  3. If matched, proceed with the stage pipeline in v1_2."
echo "  4. If not matched, investigate drift before running downstream stages."
