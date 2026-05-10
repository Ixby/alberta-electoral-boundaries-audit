"""
quote_verifier.py — Strategy-pattern quote verification for sentiment analysis.

Implements a tiered pipeline. Each tier is a strategy that either confirms
the quote or passes to the next tier:

  Tier 1 — ExactMatch:       quote is a verbatim substring of source_text
  Tier 2 — NormalizedMatch:  quote matches after whitespace normalisation
  Tier 3 — ProgramExtracted: find best-matching sentence via content words
  Tier 4 — Hallucinated:     no match found; quote must be cleared

The pipeline is invoked via verify_quote(). Callers receive a
VerificationResult with the (possibly replaced) quote and a status string.

Dependencies:
  Forward:  (consumed by quote_verify_and_clean.py, sentiment scripts)
  Backward: (stdlib only)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ── Stopwords ─────────────────────────────────────────────────────────────────

STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "not", "we", "i", "you",
    "they", "it", "he", "she", "this", "that", "which", "who", "what",
    "when", "where", "how", "as", "so", "if", "our", "their", "its", "my",
    "his", "her", "your", "us", "them", "very", "also", "more", "than",
    "then", "these", "those", "about", "into", "out", "up", "down",
    "there", "here", "all", "some", "any", "other", "such", "each",
    "can", "just", "now", "only", "over", "after", "before", "between",
    "through",
})

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_TOKEN_RE    = re.compile(r"\b\w+\b")


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class VerificationResult:
    """Outcome of a quote verification pass.

    quote:     Verbatim text to use as the quote (may be "" if unverifiable).
               When non-empty this is always an exact substring of source_text.
    status:    One of the canonical status strings (see STATUS_* constants).
    downgrade: True when the classification should be marked unverifiable
               because no supporting quote could be confirmed.
    """
    quote:     str
    status:    str
    downgrade: bool = field(default=False)


# Canonical status values
STATUS_NA         = "N/A"
STATUS_TRUE       = "True"
STATUS_NORMALIZED = "True (Normalized)"
STATUS_EXTRACTED  = "True (Extracted)"
STATUS_WEAK       = "Weak-match (Manual Review)"
STATUS_HALLUCINATED = "Hallucinated"
STATUS_MISSING    = "Source Missing"

PRIMARY_STATUSES = frozenset({STATUS_TRUE, STATUS_NORMALIZED, STATUS_EXTRACTED})


# ── Internal helpers ──────────────────────────────────────────────────────────

def _significant_words(text: str) -> set[str]:
    """Non-stopword tokens of length > 3 (lowercased)."""
    return {
        t for t in _TOKEN_RE.findall(text.lower())
        if t not in STOPWORDS and len(t) > 3
    }


def _score_candidate(candidate: str, sig_words: set[str]) -> int:
    """Count how many significant words appear in candidate (lowercased)."""
    lower = candidate.lower()
    return sum(1 for w in sig_words if w in lower)


# ── Verification strategies ───────────────────────────────────────────────────

class _ExactMatchStrategy:
    def verify(self, quote: str, source_text: str, **_) -> VerificationResult | None:
        if quote in source_text:
            return VerificationResult(quote=quote, status=STATUS_TRUE)
        return None


class _NormalizedMatchStrategy:
    def verify(self, quote: str, source_text: str, **_) -> VerificationResult | None:
        if " ".join(quote.split()) in " ".join(source_text.split()):
            return VerificationResult(quote=quote, status=STATUS_NORMALIZED)
        return None


class _ProgramExtractStrategy:
    """Search source_text for the sentence(s) with highest content-word overlap
    with the claimed quote + reasoning hint. Returns an Extracted result only
    when the candidate is a confirmed exact substring of source_text."""

    def verify(
        self,
        quote: str,
        source_text: str,
        reasoning: str = "",
        sentences: list[str] | None = None,
    ) -> VerificationResult | None:
        sig_words = _significant_words(quote) | _significant_words(reasoning)
        if not sig_words:
            return None

        sents = sentences if sentences is not None else _SENTENCE_RE.split(source_text)

        best_score = 0
        best_candidate = ""

        # Score individual sentences
        for sent in sents:
            score = _score_candidate(sent, sig_words)
            if score > best_score:
                best_score = score
                best_candidate = sent.strip()

        # Score consecutive sentence pairs (content can span a boundary)
        for i in range(len(sents) - 1):
            pair = sents[i].strip() + " " + sents[i + 1].strip()
            score = _score_candidate(pair, sig_words)
            if score > best_score:
                best_score = score
                best_candidate = pair

        if not best_candidate:
            return None

        # Require the candidate to be a verbatim substring — this is the
        # forensic guarantee that the quote is unaltered.
        if best_score >= 3 and best_candidate in source_text:
            return VerificationResult(quote=best_candidate, status=STATUS_EXTRACTED)

        if best_score >= 2:
            return VerificationResult(quote="", status=STATUS_WEAK)

        return None


# ── Public API ────────────────────────────────────────────────────────────────

_PIPELINE: list = [
    _ExactMatchStrategy(),
    _NormalizedMatchStrategy(),
    _ProgramExtractStrategy(),
]


def verify_quote(
    quote:       str,
    source_text: str,
    reasoning:   str  = "",
    sentences:   list[str] | None = None,
) -> VerificationResult:
    """Run the full verification pipeline on a claimed quote.

    Args:
        quote:       The quote string returned by the LLM. May be hallucinated.
        source_text: The verbatim source document text.
        reasoning:   The LLM's one-sentence reasoning (used as a hint for
                     content-word extraction when the quote fails exact match).
        sentences:   Pre-split sentence list (pass when available to avoid
                     re-splitting large Hansard files on every call).

    Returns:
        VerificationResult with a verified, verbatim quote (or "" if
        unverifiable) and a canonical status string.
    """
    # No quote needed for these cases
    if not quote:
        return VerificationResult(quote="", status=STATUS_NA)

    for strategy in _PIPELINE:
        kwargs: dict = {"quote": quote, "source_text": source_text,
                        "reasoning": reasoning, "sentences": sentences}
        result = strategy.verify(**kwargs)
        if result is not None:
            return result

    # Nothing found in any tier — hallucination confirmed
    return VerificationResult(quote="", status=STATUS_HALLUCINATED, downgrade=True)
