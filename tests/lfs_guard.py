"""Skip helper for data-backed tests.

Forward dependencies: none
Backward dependencies: test_pipeline_integration.py, test_published_numbers.py
"""
from __future__ import annotations

from pathlib import Path


def unavailable_reason(path) -> str | None:
    """Why a committed data file cannot be read, or None if it can.

    A file is unavailable when it is absent, or when it is still a Git LFS
    pointer (a ~130-byte text stub starting 'version https://git-lfs') because
    the clone did not run `git lfs pull`. Data-backed tests call this and skip
    with the returned message instead of failing on a pointer.
    """
    path = Path(path)
    if not path.exists():
        return f"{path} is not present"
    with open(path, "rb") as fh:
        head = fh.read(64)
    if head.startswith(b"version https://git-lfs"):
        return f"{path} is an un-pulled Git LFS pointer (run `git lfs pull`)"
    return None


def first_unavailable(*paths) -> str | None:
    """The first unavailable_reason among paths, or None if all can be read."""
    for p in paths:
        r = unavailable_reason(p)
        if r:
            return r
    return None
