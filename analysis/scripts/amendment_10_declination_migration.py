"""
amendment_10_declination_migration.py — Authoritative migration script for
the Amendment 10 declination sign-correction (T1.7 referee #5; Warrington 2018
sign convention restored at analysis/scripts/mcmc_ensemble.py:215).

Round 2 (T1.7 R2 Refs #2, #4, #15) caught three failures in the original
in-session migration at commit c9a9fbd:

  1. The original flip used pandas read_csv/to_csv with default float repr,
     which truncated every numeric column from 17 to ~15-16 significant
     digits across 1.01M rows — not just declination. This script restores
     full repr precision on every non-declination column from the pre-flip
     blobs at c9a9fbd^ (= fc5aae1) and negates declination from those
     blobs as the only edit.

  2. Two sibling declination stores were never migrated:
       - data/outputs/simulated_ensemble_raw_samples_canonical.csv
       - data/outputs/simulation_real_map_scores_canonical.json
     This script handles them too.

  3. No migration script and no pre/post SHA-256 manifest existed. This
     script IS the checked-in migration; it writes a manifest at
     findings/amendment_10_migration_manifest.json with pre/post SHA-256
     for every touched file.

Usage:
  python analysis/scripts/amendment_10_declination_migration.py [--dry-run] [--from-blobs]

  --from-blobs    Source the pre-flip CSVs from `git show fc5aae1:<path>`
                  rather than the on-disk (already-flipped) versions.
                  This is the correct mode for a fresh re-migration.

  --dry-run       Print what would change; touch nothing.

Idempotency: if a CSV's declination column mean is already small-positive
(post-flip), this script REFUSES to flip it again (prevents double-flip).
Override with --force if you really mean it.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent

# Files that carry a declination column requiring negation
CHAIN_CSVS = [
    Path("data/simulation_checkpoints_canonical/chain0_samples.csv"),
    Path("data/simulation_checkpoints_canonical/chain1_samples.csv"),
    Path("data/simulation_checkpoints_canonical/chain2_samples.csv"),
    Path("data/simulation_checkpoints_canonical/chain3_samples.csv"),
]
POOLED_CSV = Path("data/outputs/simulated_ensemble_raw_samples_canonical.csv")
REAL_MAP_JSON = Path("data/outputs/simulation_real_map_scores_canonical.json")

PRE_FLIP_COMMIT = "fc5aae1"  # c9a9fbd^, the last pre-Amendment-10 commit

MANIFEST_PATH = ROOT / "findings" / "amendment_10_migration_manifest.json"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes())


def git_show_bytes(commit: str, repo_path: str) -> bytes:
    """Read the file content from a git blob at <commit>:<repo_path>."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{repo_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return result.stdout


def negate_csv_declination_full_repr(in_bytes: bytes) -> bytes:
    """Read a CSV from bytes, negate the `declination` column, and write
    back with full float repr (Python's default `repr` round-trips float64
    exactly). Preserves every other column byte-for-byte where possible by
    using the maximum-precision text representation."""
    df = pd.read_csv(io.BytesIO(in_bytes))
    if "declination" not in df.columns:
        raise RuntimeError("declination column missing")
    df["declination"] = -df["declination"]
    # Use float_format that round-trips: %.17g is sufficient for IEEE 754
    # double precision. Pandas' default is %.12g, which loses precision.
    buf = io.StringIO()
    df.to_csv(buf, index=False, float_format="%.17g")
    return buf.getvalue().encode("utf-8")


def col_means(b: bytes) -> Dict[str, float]:
    df = pd.read_csv(io.BytesIO(b))
    return {c: float(df[c].mean()) for c in df.columns if pd.api.types.is_numeric_dtype(df[c])}


def check_idempotency(b: bytes, label: str, force: bool) -> None:
    """Refuse to flip a CSV whose declination column is already small-positive."""
    df = pd.read_csv(io.BytesIO(b))
    mean = float(df["declination"].mean())
    if mean > 0 and abs(mean) < 0.01 and not force:
        raise RuntimeError(
            f"{label}: declination column mean is already small-positive ({mean:+.5f}). "
            "Refusing to flip — this would double-flip back to old sign. "
            "Pass --force if you have verified this is what you want."
        )


def migrate_chain_csv(path: Path, source_bytes: bytes, dry: bool, force: bool) -> Dict:
    """Migrate a single chain CSV. source_bytes is the PRE-flip content."""
    check_idempotency(source_bytes, str(path), force)
    pre_sha = sha256(source_bytes)
    pre_means = col_means(source_bytes)
    flipped = negate_csv_declination_full_repr(source_bytes)
    post_sha = sha256(flipped)
    post_means = col_means(flipped)
    if not dry:
        path.write_bytes(flipped)
    return {
        "path": str(path),
        "pre_sha256": pre_sha,
        "post_sha256": post_sha,
        "pre_declination_mean": pre_means.get("declination"),
        "post_declination_mean": post_means.get("declination"),
        "all_pre_means": pre_means,
        "all_post_means": post_means,
        "edited_columns": ["declination"],
    }


def migrate_real_map_json(path: Path, dry: bool, force: bool) -> Dict:
    """Negate declination values in the real-map scores JSON. Idempotent:
    refuses to flip if the minority value is already positive."""
    raw = path.read_bytes()
    pre_sha = sha256(raw)
    data = json.loads(raw.decode("utf-8"))
    # Inspect each map's declination
    edits: List[Tuple[str, float, float]] = []
    for key in ("majority", "minority", "enacted_2019", "majority_2026", "minority_2026", "2019_enacted"):
        if key not in data:
            continue
        entry = data[key]
        if not isinstance(entry, dict):
            continue
        for sub in ("declination", "declination_canonical", "Warrington_declination"):
            if sub in entry and isinstance(entry[sub], (int, float)):
                old = float(entry[sub])
                if key == "minority" and old > 0 and not force:
                    raise RuntimeError(
                        f"{path}: {key}.{sub} = {old:+.5f} is already positive. "
                        "Refusing to flip (would double-flip). Use --force to override."
                    )
                new = -old
                entry[sub] = new
                edits.append((f"{key}.{sub}", old, new))
    new_raw = json.dumps(data, indent=2).encode("utf-8")
    post_sha = sha256(new_raw)
    if not dry:
        path.write_bytes(new_raw)
    return {
        "path": str(path),
        "pre_sha256": pre_sha,
        "post_sha256": post_sha,
        "edits": [{"key": k, "pre": p, "post": q} for k, p, q in edits],
    }


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print intended changes without touching anything")
    ap.add_argument("--from-blobs", action="store_true",
                    help="Source pre-flip CSVs from git show fc5aae1:<path> "
                         "rather than from disk (use this for a fresh, lossless re-migration)")
    ap.add_argument("--force", action="store_true",
                    help="Override idempotency check (DANGEROUS — can double-flip)")
    args = ap.parse_args(argv)

    manifest: Dict = {
        "amendment": 10,
        "title": "Declination sign-convention correction (Warrington 2018)",
        "source": f"git blobs at {PRE_FLIP_COMMIT} (= c9a9fbd^)" if args.from_blobs else "on-disk current files",
        "script": __file__,
        "dry_run": args.dry_run,
        "force": args.force,
        "entries": [],
    }

    for rel in CHAIN_CSVS:
        abspath = ROOT / rel
        if args.from_blobs:
            print(f"  reading git blob {PRE_FLIP_COMMIT}:{rel} …", flush=True)
            source = git_show_bytes(PRE_FLIP_COMMIT, str(rel))
        else:
            source = abspath.read_bytes()
        entry = migrate_chain_csv(abspath, source, args.dry_run, args.force)
        manifest["entries"].append(entry)
        print(f"  {rel.name}: pre-decl_mean={entry['pre_declination_mean']:+.5f} "
              f"→ post-decl_mean={entry['post_declination_mean']:+.5f}",
              flush=True)

    # Pooled CSV: ALWAYS source from disk because it is LFS-tracked at
    # pre-flip commits (`git show <commit>:<path>` returns an LFS pointer,
    # not the actual data). Disk content is whatever the local LFS smudge
    # left there.
    if (ROOT / POOLED_CSV).exists():
        source = (ROOT / POOLED_CSV).read_bytes()
        # Detect LFS pointer (the literal text "version https://git-lfs.github.com")
        if source[:60].startswith(b"version https://git-lfs"):
            print(f"  {POOLED_CSV} is an LFS pointer on disk — skipping (run `git lfs pull` first)", flush=True)
        else:
            entry = migrate_chain_csv(ROOT / POOLED_CSV, source, args.dry_run, args.force)
            manifest["entries"].append(entry)
            print(f"  {POOLED_CSV.name}: pre-decl_mean={entry['pre_declination_mean']:+.5f} "
                  f"→ post-decl_mean={entry['post_declination_mean']:+.5f}", flush=True)

    if (ROOT / REAL_MAP_JSON).exists():
        entry = migrate_real_map_json(ROOT / REAL_MAP_JSON, args.dry_run, args.force)
        manifest["entries"].append(entry)
        for e in entry["edits"]:
            print(f"  {REAL_MAP_JSON.name}: {e['key']} {e['pre']:+.5f} → {e['post']:+.5f}", flush=True)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not args.dry_run:
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\nmanifest -> {MANIFEST_PATH}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
