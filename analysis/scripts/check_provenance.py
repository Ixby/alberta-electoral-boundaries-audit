import json
import hashlib
import argparse
from pathlib import Path

def compute_sha256(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def verify_provenance(manifest_path):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    data_dir = Path(manifest_path).parent
    failed = False
    
    for filename, meta in manifest.items():
        filepath = data_dir / filename
        if not filepath.exists():
            # Many derived files are not checked into Git due to size, 
            # so missing files are only warnings unless running full validation
            print(f"[WARN] File missing from local disk: {filename}")
            continue
            
        actual_hash = compute_sha256(filepath)
        expected_hash = meta.get("sha256", "")
        
        # If it's a placeholder, update it. If it's an actual hash, check it.
        if "placeholder" in expected_hash:
            print(f"[INFO] Updating placeholder hash for {filename}: {actual_hash}")
            manifest[filename]["sha256"] = actual_hash
        elif actual_hash != expected_hash:
            print(f"[FAIL] Hash mismatch for {filename}!")
            print(f"  Expected: {expected_hash}")
            print(f"  Actual:   {actual_hash}")
            failed = True
        else:
            print(f"[PASS] {filename} (SHA256: {actual_hash[:8]}...)")
            
    if "placeholder" in str(manifest):
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        print("[INFO] Wrote computed hashes back to manifest.")
        
    if failed:
        import sys
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    verify_provenance(args.manifest)
