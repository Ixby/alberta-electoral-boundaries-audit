"""
quote_verify_and_clean.py
--------------------------
Verify extracted quotes against source submission text files and produce a
cleaned sentiment dataset.

For each row in the full sentiment results CSV that has an exact_quote:
  1. Load the source submission text from .temp/submissions/text/{submission_id}.txt
  2. Normalize both quote and source to lowercase stripped ASCII
  3. Check for literal substring match (VERIFIED)
  4. If not literal, check difflib sequence ratio >= 0.85 (NEAR_MATCH)
  5. Otherwise flag as UNVERIFIED

Rows without an exact_quote keep their existing quote_verified value.

Outputs:
    data/outputs/quotes_verified.csv  -- full dataset with updated quote_verified column
    data/outputs/quote_verification_summary.json -- counts by verification status

Usage:
    python analysis/scripts/quote_verify_and_clean.py

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""
from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TEXT_DIR = ROOT / ".temp" / "submissions" / "text"
INPUT_CSV = ROOT / "data/outputs/submission_sentiment_llm_full_results.csv"
OUTPUT_CSV = ROOT / "data/outputs/quotes_verified.csv"
SUMMARY_JSON = ROOT / "data/outputs/quote_verification_summary.json"

NEAR_MATCH_THRESHOLD = 0.85


def normalize(text: str) -> str:
    """Normalize text for fuzzy matching: lowercase, strip accents, collapse whitespace."""
    if not isinstance(text, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[\"'‘’“”`]", "'", ascii_text)
    ascii_text = re.sub(r"\s+", " ", ascii_text).strip().lower()
    return ascii_text


def load_source_text(submission_id: str) -> str:
    """Load and return the full text of a submission, or empty string if missing."""
    path = TEXT_DIR / f"{submission_id}.txt"
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def verify_quote(quote: str, source_text: str) -> str:
    """Return verification status: VERIFIED, NEAR_MATCH, or UNVERIFIED."""
    if not quote or not source_text:
        return "UNVERIFIED"

    norm_quote = normalize(quote)
    norm_source = normalize(source_text)

    if not norm_quote:
        return "UNVERIFIED"

    # Literal match
    if norm_quote in norm_source:
        return "VERIFIED"

    # Fuzzy match — use the longest possible window from the source
    # to avoid O(n²) SequenceMatcher on the full document.
    window = len(norm_quote) * 2
    best_ratio = 0.0
    for start in range(0, max(1, len(norm_source) - len(norm_quote) + 1), max(1, len(norm_quote) // 2)):
        chunk = norm_source[start : start + window]
        ratio = SequenceMatcher(None, norm_quote, chunk[:len(norm_quote) + 20]).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
        if best_ratio >= NEAR_MATCH_THRESHOLD:
            break

    if best_ratio >= NEAR_MATCH_THRESHOLD:
        return f"NEAR_MATCH ({best_ratio:.2f})"

    return "UNVERIFIED"


def main():
    print(f"Loading sentiment results from {INPUT_CSV.name}...")
    df = pd.read_csv(INPUT_CSV, on_bad_lines="skip")
    print(f"  {len(df)} rows loaded.")

    has_quote = df["exact_quote"].notna() & (df["exact_quote"].str.strip().str.len() > 0)
    print(f"  {has_quote.sum()} rows have an exact_quote to verify.")

    # Cache source texts to avoid repeated disk reads
    source_cache: dict[str, str] = {}

    results = []
    verified_count = 0
    near_match_count = 0
    unverified_count = 0
    no_quote_count = 0

    for _, row in df.iterrows():
        new_row = row.to_dict()

        if not has_quote.loc[row.name]:
            no_quote_count += 1
            results.append(new_row)
            continue

        sid = str(row["submission_id"])
        if sid not in source_cache:
            source_cache[sid] = load_source_text(sid)

        status = verify_quote(str(row["exact_quote"]), source_cache[sid])
        new_row["quote_verified"] = status

        if "VERIFIED" in status and "NEAR" not in status:
            verified_count += 1
        elif "NEAR_MATCH" in status:
            near_match_count += 1
        else:
            unverified_count += 1

        results.append(new_row)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)

    summary = {
        "total_rows": len(df),
        "rows_with_quote": int(has_quote.sum()),
        "verified": verified_count,
        "near_match": near_match_count,
        "unverified": unverified_count,
        "no_quote": no_quote_count,
        "verification_rate": round(
            (verified_count + near_match_count) / max(1, has_quote.sum()), 3
        ),
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2)

    print("\nVerification Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print(f"\nOutput: {OUTPUT_CSV.relative_to(ROOT)}")
    print(f"Summary: {SUMMARY_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
