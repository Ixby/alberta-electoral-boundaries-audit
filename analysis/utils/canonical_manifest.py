"""
canonical_manifest.py — SHA-256 manifest for canonical data files.

Every file listed here must match its recorded hash before any analysis
script uses it. Call verify_canonical_files() at the top of scripts that
load these files; it raises CanonicalFileError on mismatch.

Hashes were recorded on 2026-05-08 against Elections Alberta canonical
shapefiles (ea_*_2026_eds.gpkg) and the derived VA polygon file.

Forward dependencies: none
Backward dependencies: szat.py, mcmc_ensemble_canonical.py,
    joint_outlier_score_canonical.py (all call verify_canonical_files)
"""
from __future__ import annotations

import hashlib
from pathlib import Path

# ── Registry ──────────────────────────────────────────────────────────────────

# Maps each relative path (from repo root) to its expected SHA-256 hex digest.
# Add new canonical files here as they are locked in.
CANONICAL_HASHES: dict[str, str] = {
    "data/shapefiles/canonical/ea_majority_2026_eds.gpkg":
        "5dcd4c6f931bdd04286bdeb17b183f673ca8d59f4f805ab27c70138b00f1a160",
    "data/shapefiles/canonical/ea_minority_2026_eds.gpkg":
        "82e29a719e96c7880b54355b5f18487a1912c1152479577b4c9b90862779e897",
    "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg":
        "0ca9d3995db011bb66021392b305c781c870e287a48097654aceca7ff2f9ab4c",
}

# File sizes (bytes) — used for fast pre-check before full hash computation.
CANONICAL_SIZES: dict[str, int] = {
    "data/shapefiles/canonical/ea_majority_2026_eds.gpkg": 4_882_432,
    "data/shapefiles/canonical/ea_minority_2026_eds.gpkg": 4_907_008,
    "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg": 22_147_072,
}

# ── Exception ─────────────────────────────────────────────────────────────────


class CanonicalFileError(RuntimeError):
    """Raised when a canonical file is missing or has an unexpected hash."""


# ── Helpers ───────────────────────────────────────────────────────────────────


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


# ── Public API ────────────────────────────────────────────────────────────────


def verify_file(rel_path: str, *, strict: bool = True) -> bool:
    """
    Verify one canonical file by relative path.

    Parameters
    ----------
    rel_path : str
        Path relative to repo root (use forward slashes).
    strict : bool
        If True (default), raise CanonicalFileError on any mismatch.
        If False, return False instead of raising.

    Returns
    -------
    bool
        True if the file matches; False only when strict=False and mismatch found.
    """
    root = _repo_root()
    path = root / rel_path

    if not path.exists():
        msg = f"Canonical file missing: {path}"
        if strict:
            raise CanonicalFileError(msg)
        return False

    expected_hash = CANONICAL_HASHES.get(rel_path)
    if expected_hash is None:
        msg = f"No registered hash for {rel_path!r}. Add it to canonical_manifest.py."
        if strict:
            raise CanonicalFileError(msg)
        return False

    # Fast size pre-check — avoids reading 20+ MB if size is obviously wrong.
    expected_size = CANONICAL_SIZES.get(rel_path)
    actual_size = path.stat().st_size
    if expected_size is not None and actual_size != expected_size:
        msg = (
            f"Canonical file size mismatch: {rel_path}\n"
            f"  expected {expected_size:,} bytes, got {actual_size:,} bytes.\n"
            "Update this file's entry in canonical_manifest.py if the data changed."
        )
        if strict:
            raise CanonicalFileError(msg)
        return False

    actual_hash = _sha256(path)
    if actual_hash != expected_hash:
        msg = (
            f"Canonical file hash mismatch: {rel_path}\n"
            f"  expected {expected_hash}\n"
            f"  got      {actual_hash}\n"
            "If the data file was intentionally updated, re-run:\n"
            "  python -c \"import hashlib,pathlib; p=pathlib.Path('{rel_path}'); "
            "print(hashlib.sha256(p.read_bytes()).hexdigest())\"\n"
            "and update CANONICAL_HASHES in canonical_manifest.py."
        )
        if strict:
            raise CanonicalFileError(msg)
        return False

    return True


def verify_canonical_files(
    paths: list[str] | None = None,
    *,
    strict: bool = True,
) -> dict[str, bool]:
    """
    Verify all registered canonical files (or a subset).

    Parameters
    ----------
    paths : list[str] | None
        Relative paths to verify. Defaults to all keys in CANONICAL_HASHES.
    strict : bool
        Passed through to verify_file().

    Returns
    -------
    dict[str, bool]
        Maps each path to True (ok) / False (mismatch, only when strict=False).
    """
    if paths is None:
        paths = list(CANONICAL_HASHES)
    return {p: verify_file(p, strict=strict) for p in paths}


def print_manifest_status() -> None:
    """Print a one-line status for each registered canonical file."""
    root = _repo_root()
    for rel_path, expected in CANONICAL_HASHES.items():
        path = root / rel_path
        if not path.exists():
            print(f"  MISSING  {rel_path}")
            continue
        ok = verify_file(rel_path, strict=False)
        status = "OK      " if ok else "MISMATCH"
        print(f"  {status}  {rel_path}")


if __name__ == "__main__":
    print("Canonical file manifest check:")
    print_manifest_status()
