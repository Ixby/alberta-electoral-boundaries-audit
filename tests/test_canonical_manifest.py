"""
Tests for analysis/utils/canonical_manifest.py.

Forward dependencies: none
Backward dependencies: canonical_manifest.verify_file, verify_canonical_files
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

# Ensure utils is importable
_utils = Path(__file__).resolve().parent.parent / "analysis" / "utils"
if str(_utils) not in sys.path:
    sys.path.insert(0, str(_utils))

import canonical_manifest as cm


# ── Helpers ───────────────────────────────────────────────────────────────────

def _write_file(tmp_path: Path, rel: str, content: bytes) -> tuple[str, str, int]:
    """Write bytes to tmp_path/rel; return (rel, sha256_hex, size)."""
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest()
    return rel, digest, len(content)


def _patch(monkeypatch, tmp_path: Path, hashes: dict, sizes: dict) -> None:
    monkeypatch.setattr(cm, "CANONICAL_HASHES", hashes)
    monkeypatch.setattr(cm, "CANONICAL_SIZES", sizes)
    monkeypatch.setattr(cm, "_repo_root", lambda: tmp_path)


# ── verify_file — missing file ────────────────────────────────────────────────

@pytest.mark.parametrize("strict", [True, False])
def test_missing_file_strict_false_returns_false(tmp_path, monkeypatch, strict):
    rel = "data/file.gpkg"
    _patch(monkeypatch, tmp_path, {rel: "abc123"}, {rel: 10})
    if strict:
        with pytest.raises(cm.CanonicalFileError, match="missing"):
            cm.verify_file(rel, strict=True)
    else:
        assert cm.verify_file(rel, strict=False) is False


# ── verify_file — unregistered path ──────────────────────────────────────────

def test_unregistered_path_strict_raises(tmp_path, monkeypatch):
    _patch(monkeypatch, tmp_path, {}, {})
    p = tmp_path / "unknown.gpkg"
    p.write_bytes(b"data")
    with pytest.raises(cm.CanonicalFileError, match="No registered hash"):
        cm.verify_file("unknown.gpkg", strict=True)


def test_unregistered_path_permissive_returns_false(tmp_path, monkeypatch):
    _patch(monkeypatch, tmp_path, {}, {})
    p = tmp_path / "unknown.gpkg"
    p.write_bytes(b"data")
    assert cm.verify_file("unknown.gpkg", strict=False) is False


# ── verify_file — size mismatch ───────────────────────────────────────────────

@pytest.mark.parametrize("strict", [True, False])
def test_size_mismatch(tmp_path, monkeypatch, strict):
    rel, digest, size = _write_file(tmp_path, "f.gpkg", b"hello")
    _patch(monkeypatch, tmp_path, {rel: digest}, {rel: size + 999})
    if strict:
        with pytest.raises(cm.CanonicalFileError, match="size mismatch"):
            cm.verify_file(rel, strict=True)
    else:
        assert cm.verify_file(rel, strict=False) is False


# ── verify_file — hash mismatch ───────────────────────────────────────────────

@pytest.mark.parametrize("strict", [True, False])
def test_hash_mismatch(tmp_path, monkeypatch, strict):
    rel, _, size = _write_file(tmp_path, "f.gpkg", b"hello")
    _patch(monkeypatch, tmp_path, {rel: "0" * 64}, {rel: size})
    if strict:
        with pytest.raises(cm.CanonicalFileError, match="hash mismatch"):
            cm.verify_file(rel, strict=True)
    else:
        assert cm.verify_file(rel, strict=False) is False


# ── verify_file — passing ─────────────────────────────────────────────────────

def test_verify_file_pass(tmp_path, monkeypatch):
    rel, digest, size = _write_file(tmp_path, "canonical/ea.gpkg", b"real content here")
    _patch(monkeypatch, tmp_path, {rel: digest}, {rel: size})
    assert cm.verify_file(rel) is True


def test_verify_file_pass_no_size_entry(tmp_path, monkeypatch):
    """Files without a CANONICAL_SIZES entry skip the size pre-check."""
    rel, digest, _ = _write_file(tmp_path, "f.gpkg", b"abc")
    _patch(monkeypatch, tmp_path, {rel: digest}, {})
    assert cm.verify_file(rel) is True


# ── verify_canonical_files ────────────────────────────────────────────────────

def test_verify_canonical_files_returns_dict(tmp_path, monkeypatch):
    rel_a, dig_a, sz_a = _write_file(tmp_path, "a.gpkg", b"aaa")
    rel_b, dig_b, sz_b = _write_file(tmp_path, "b.gpkg", b"bbb")
    _patch(monkeypatch, tmp_path,
           {rel_a: dig_a, rel_b: dig_b},
           {rel_a: sz_a, rel_b: sz_b})
    result = cm.verify_canonical_files(strict=False)
    assert result == {rel_a: True, rel_b: True}


def test_verify_canonical_files_subset(tmp_path, monkeypatch):
    rel_a, dig_a, sz_a = _write_file(tmp_path, "a.gpkg", b"aaa")
    rel_b, dig_b, sz_b = _write_file(tmp_path, "b.gpkg", b"bbb")
    _patch(monkeypatch, tmp_path,
           {rel_a: dig_a, rel_b: dig_b},
           {rel_a: sz_a, rel_b: sz_b})
    result = cm.verify_canonical_files(paths=[rel_a], strict=False)
    assert list(result.keys()) == [rel_a]
    assert result[rel_a] is True


def test_verify_canonical_files_mismatch_strict_raises(tmp_path, monkeypatch):
    rel, _, size = _write_file(tmp_path, "bad.gpkg", b"content")
    _patch(monkeypatch, tmp_path, {rel: "0" * 64}, {rel: size})
    with pytest.raises(cm.CanonicalFileError):
        cm.verify_canonical_files(strict=True)


def test_verify_canonical_files_defaults_to_all_hashes(tmp_path, monkeypatch):
    """When paths=None, all keys in CANONICAL_HASHES are checked."""
    rel_a, dig_a, sz_a = _write_file(tmp_path, "a.gpkg", b"a")
    rel_b, dig_b, sz_b = _write_file(tmp_path, "b.gpkg", b"b")
    _patch(monkeypatch, tmp_path,
           {rel_a: dig_a, rel_b: dig_b},
           {rel_a: sz_a, rel_b: sz_b})
    result = cm.verify_canonical_files(paths=None, strict=False)
    assert set(result.keys()) == {rel_a, rel_b}
