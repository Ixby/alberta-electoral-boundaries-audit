# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
check_provenance.py — verify committed files against data/provenance_manifest.json.

For every entry in the manifest, hash the file and compare with the recorded
SHA-256. A mismatch fails. A file that is listed but absent also fails: every
entry in the manifest is committed (directly or as an LFS pointer), so absence means it was
deleted or renamed. Pass --allow-missing to downgrade absence to a warning. A
file that is present only as an un-pulled Git LFS pointer is reported and
skipped, not failed.

Scope. The manifest covers six derived outputs under data/outputs/ and the raw
inputs behind the headline numbers: the 2023 Statement of Vote workbook, the
results CSV, the poll-level CSV, the two printed-report population tables,
va_pop_from_das.csv (both copies), the census DA profile, and four Git LFS
boundary and vote files (the two canonical 2026 maps and the two voting-area
vote files). The 14 census API extracts listed in
data/census_2021/api_extracts_SHA256SUMS are not committed and not covered.
The canonical 2026 boundary files are also pinned in
analysis/utils/canonical_manifest.py. The hashes show that the files have not
changed since they were recorded; they cannot show that the boundary files are
the bytes Elections Alberta delivered, because the delivered package is not
archived.

Backward:
  data/provenance_manifest.json and the files it lists
Forward:
  .github/workflows/tests.yml (the "Verify data provenance" step)
"""
import json
import hashlib
import argparse
from pathlib import Path


# Text extensions hashed in the repo's canonical LF form. .gitattributes
# declares `* text=auto eol=lf`, so the bytes git stores are always LF — but
# scripts regenerating these outputs on Windows write CRLF to the working
# tree, and hashing raw working-tree bytes bakes the platform into the
# manifest. That exact drift broke the CI provenance gate on 2026-07-09:
# local (CRLF) hashes PASSed while the Linux checkout (LF) FAILed.
# Normalizing CRLF -> LF before hashing makes the manifest describe the
# content, not the checkout.
_TEXT_EXTENSIONS = {".csv", ".json", ".md", ".txt", ".yaml", ".yml"}


def compute_sha256(filepath):
    filepath = Path(filepath)
    hash_sha256 = hashlib.sha256()
    if filepath.suffix.lower() in _TEXT_EXTENSIONS:
        hash_sha256.update(filepath.read_bytes().replace(b"\r\n", b"\n"))
        return hash_sha256.hexdigest()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def is_lfs_pointer(filepath) -> bool:
    with open(filepath, "rb") as f:
        return f.read(64).startswith(b"version https://git-lfs")


def verify_provenance(manifest_path, allow_missing=False):
    """Check every manifest entry. Returns True if all pass; exits 1 otherwise."""
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    data_dir = Path(manifest_path).parent
    failed = False

    for filename, meta in manifest.items():
        filepath = data_dir / filename
        if not filepath.exists():
            if allow_missing:
                print(f"[WARN] File missing from local disk: {filename}")
            else:
                print(f"[FAIL] Listed file is missing: {filename} "
                      f"(pass --allow-missing to downgrade to a warning)")
                failed = True
            continue
        if is_lfs_pointer(filepath):
            print(f"[SKIP] {filename} is an un-pulled Git LFS pointer; not checked")
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
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print("[INFO] Wrote computed hashes back to manifest.")

    if failed:
        import sys

        sys.exit(1)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--allow-missing", action="store_true",
                        help="Treat a listed file that is absent as a warning, not a failure.")
    args = parser.parse_args()
    verify_provenance(args.manifest, allow_missing=args.allow_missing)
