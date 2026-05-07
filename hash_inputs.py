import hashlib, os, json, pathlib

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

SKIP_FILES = {
    "data/raw/98-401-X2021024_English_CSV_data.csv",
}
SKIP_DIRS = {
    ".git", ".temp", "__pycache__",
    "simulation_checkpoints_canonical",
    "simulation_checkpoints_partial_2m_killed",
    "simulation_checkpoints_250k_v0_8_buggy",
    "mcmc_checkpoints_canonical",
    "_perfecter_checkpoints",
    "source_checks",
}
SIZE_LIMIT = 50_000_000

results = {}
for root, dirs, files in os.walk("data/"):
    dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
    for f in sorted(files):
        path = pathlib.Path(root) / f
        rel = str(path).replace("\\", "/")
        if rel in SKIP_FILES:
            continue
        size = path.stat().st_size
        if size > SIZE_LIMIT:
            print(f"SKIP ({size/1e6:.0f}MB)  {rel}")
            continue
        h = sha256(path)
        results[rel] = {"sha256": h, "size_bytes": size}
        print(f"{h[:16]}...  {size:>10,}  {rel}")

print(f"\nTotal: {len(results)} files hashed")
with open("data/input_hashes.json", "w") as out:
    json.dump(results, out, indent=2)
print("Written: data/input_hashes.json")
