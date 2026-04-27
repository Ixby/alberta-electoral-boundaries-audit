import os
import re

def preview_refactor():
    patterns_to_strip = [
        r"^v0_\d+_",
        r"_v0_\d+$"
    ]
    
    # We will only look at these directories
    target_dirs = ["analysis/scripts", "analysis/reports", "analysis/methodology", "data", "."]
    ignore_dirs = [".git", "shapefiles", "deprecated", "archive", "tests", "__pycache__", ".pytest_cache", ".mypy_cache", "maps", "cache", "logs", "emails"]

    renames = []
    
    for d in target_dirs:
        for root, dirs, files in os.walk(d):
            # Prune ignore_dirs
            dirs[:] = [dir for dir in dirs if dir not in ignore_dirs and not dir.startswith(".")]
            
            for file in files:
                if file.endswith(".py") or file.endswith(".md") or file.endswith(".csv") or file.endswith(".json") or file.endswith(".sh"):
                    original_name = file
                    new_name = original_name
                    
                    # Apply strip patterns
                    for p in patterns_to_strip:
                        new_name = re.sub(p, "", new_name)
                    
                    # Special cases like `_v0_9.py` or `.csv`
                    new_name = re.sub(r"_v0_\d+\.py$", ".py", new_name)
                    new_name = re.sub(r"_v0_\d+\.csv$", ".csv", new_name)
                    new_name = re.sub(r"_v0_\d+\.json$", ".json", new_name)
                    
                    if new_name != original_name:
                        old_path = os.path.join(root, original_name)
                        new_path = os.path.join(root, new_name)
                        renames.append((old_path, new_path, original_name, new_name))
                        
    print(f"Found {len(renames)} files to rename.")
    for old, new, old_n, new_n in sorted(renames)[:50]:
        print(f"REN: {old_n} -> {new_n}")

if __name__ == "__main__":
    preview_refactor()
