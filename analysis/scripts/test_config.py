

import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent / "utils"))
    import data_loader

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = data_loader._resolve_path("data")

# Common source of truth for all test harnesses
MAP_PLANS = [
    {
        "name": "Minority 2026 (Canonical)",
        "path": DATA_DIR / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg",
        "id_col": "EDName2025"
    },
    {
        "name": "Majority 2026 (Canonical)",
        "path": DATA_DIR / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg",
        "id_col": "EDName2025"
    },
    {
        "name": "2019 Baseline",
        "path": DATA_DIR / "shapefiles" / "reference" / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp",
        "id_col": "EDName2017"
    }
]
