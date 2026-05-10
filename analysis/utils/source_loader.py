"""
source_loader.py — Repository pattern for submission and Hansard text files.

Abstracts file I/O and caching so callers never deal with path logic or
the "is this a Hansard turn or a submission?" distinction.

Cached at instance level. For scripts that create one SourceLoader and reuse
it across many rows, the 2.7 MB Hansard files are loaded once per process.

Dependencies:
  Forward:  (consumed by sentiment scripts)
  Backward: analysis/utils/sentiment_config.py
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    from sentiment_config import TEXT_DIR as _DEFAULT_TEXT_DIR
except ImportError:
    import sys
    from pathlib import Path as _P
    _root = _P(__file__).resolve().parent.parent.parent
    _DEFAULT_TEXT_DIR = _root / ".temp" / "submissions" / "text"

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


class SourceLoader:
    """
    Repository for EBC submission and Hansard source texts.

    Key contract: get_text() always returns a verbatim copy of the file
    on disk. No transformation is applied. This guarantees that any quote
    extracted from the returned text is a verbatim substring of the
    original source document.
    """

    def __init__(self, text_dir: Path | None = None) -> None:
        self._text_dir: Path = text_dir or _DEFAULT_TEXT_DIR
        self._text_cache:     dict[str, str]        = {}
        self._sentence_cache: dict[str, list[str]]  = {}

    # ── Internal key resolution ────────────────────────────────────────────────

    def _key(self, submission_id: str) -> str:
        """Map a submission_id to its file stem.

        Hansard turns share a single large file; individual submissions
        each have their own file. The key is the file stem (without .txt).
        """
        if submission_id.startswith("hansard_r1"):
            return "hansard_r1"
        if submission_id.startswith("hansard_r2"):
            return "hansard_r2"
        return submission_id

    # ── Public interface ───────────────────────────────────────────────────────

    def get_text(self, submission_id: str) -> tuple[str, bool]:
        """Return (text, found).

        text is the verbatim file contents, or "" if the file does not exist.
        found is False when the file is missing.
        """
        key = self._key(submission_id)
        if key not in self._text_cache:
            path = self._text_dir / f"{key}.txt"
            self._text_cache[key] = (
                path.read_text(encoding="utf-8", errors="replace")
                if path.exists()
                else ""
            )
        text = self._text_cache[key]
        return text, bool(text)

    def get_sentences(self, submission_id: str) -> list[str]:
        """Return a sentence-split list of the source text, cached per file."""
        key = self._key(submission_id)
        if key not in self._sentence_cache:
            text, found = self.get_text(submission_id)
            self._sentence_cache[key] = (
                _SENTENCE_RE.split(text) if found else []
            )
        return self._sentence_cache[key]

    def source_key(self, submission_id: str) -> str:
        """Expose the resolved key, useful for external cache lookups."""
        return self._key(submission_id)
