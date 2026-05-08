import os
import re
from pathlib import Path

scripts_dir = Path("analysis/scripts")

IMPORT_STATEMENT = """
import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    _p = Path(__file__).resolve().parent
    sys.path.insert(0, str(_p / "utils") if _p.name == "scripts" else str(_p.parent / "utils"))
    import data_loader
"""

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Standardize the data paths to use config
    if 'ROOT / "data"' in content or "ROOT / 'data'" in content:
        # Inject import if not present
        if "import data_loader" not in content:
            # Insert after the first few imports
            lines = content.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    insert_idx = i
                    break
            
            # If no imports found, insert at the top
            content = '\n'.join(lines[:insert_idx]) + "\n" + IMPORT_STATEMENT + "\n" + '\n'.join(lines[insert_idx:])
        
        # Replace common hardcoded data directory assignments
        content = content.replace('ROOT / "data"', 'data_loader._resolve_path("data")')
        content = content.replace("ROOT / 'data'", "data_loader._resolve_path('data')")
        
        # Replace shapefile canonical hardcoding
        content = content.replace('data_loader._resolve_path("data") / "shapefiles" / "canonical"', 'data_loader._resolve_path(data_loader.CONFIG["data"]["canonical_dir"])')

    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Refactored paths in {filepath}")

if __name__ == "__main__":
    count = 0
    for root, _, files in os.walk(scripts_dir):
        if "utils" in root:
            continue # skip the loader itself
        for f in files:
            if f.endswith(".py"):
                process_file(Path(root) / f)
                count += 1
    print(f"Sweep complete. Processed {count} scripts.")
