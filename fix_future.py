import os
from pathlib import Path

scripts_dir = Path("analysis/scripts")

def fix_future_import(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "from __future__ import annotations" not in content:
        return
        
    lines = content.split('\n')
    future_idx = -1
    for i, line in enumerate(lines):
        if line.strip() == "from __future__ import annotations":
            future_idx = i
            break
            
    if future_idx == -1:
        return
        
    # Check if there are any real statements before it
    # We will just pull the future import out and place it after the docstring or at the very top
    
    # Remove the future import from its current location
    lines.pop(future_idx)
    
    # Find where to put it (after module docstring if exists)
    insert_idx = 0
    in_docstring = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and (stripped.startswith('\"\"\"') or stripped.startswith("'''")):
            in_docstring = True
            if len(stripped) >= 6 and (stripped.endswith('\"\"\"') or stripped.endswith("'''")):
                in_docstring = False
                insert_idx = i + 1
                break
            continue
            
        if in_docstring:
            if stripped.endswith('\"\"\"') or stripped.endswith("'''") or stripped.startswith('\"\"\"') or stripped.startswith("'''"):
                in_docstring = False
                insert_idx = i + 1
                break
        else:
            if stripped and not stripped.startswith('#'):
                insert_idx = i
                break
                
    lines.insert(insert_idx, "from __future__ import annotations")
    
    new_content = '\n'.join(lines)
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed __future__ import in {filepath}")

for root, _, files in os.walk(scripts_dir):
    for f in files:
        if f.endswith(".py"):
            fix_future_import(Path(root) / f)
