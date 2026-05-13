"""
hansard_sentiment_llm.py

Runs LLM sentiment classification over the EBC Public Meeting Hansard transcripts
(Round 1 and Round 2). Parses each transcript into speaker turns, retains only
turns by community participants (not Commission members asking questions), filters
to turns mentioning any of the 7 boundary configurations, and classifies each
relevant turn using the same 7-config JSON schema as submission_sentiment_llm_full.py.

Output is appended to data/outputs/submission_sentiment_llm_full_results.csv
with scan_type = "hansard_r1" or "hansard_r2", integrating directly with the
full-corpus submission results.

Source files expected at:
    .temp/submissions/text/hansard_r1.txt
    .temp/submissions/text/hansard_r2.txt

Usage:
    python analysis/scripts/hansard_sentiment_llm.py [--dry-run]

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

from __future__ import annotations

import csv
import json
import re
import sys
import logging
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from sentiment_config import (CONFIGS, CONFIG_KEYWORDS, COMMISSION_SPEAKERS,
    JSON_SCHEMA, OUTPUT_FIELDS, OUTPUTS_DIR, TEXT_DIR, DATA_DIR)
from source_loader import SourceLoader
from quote_verifier import verify_quote
from claude_client import CLAUDE_CMD, call_claude

OUTPUT_CSV   = OUTPUTS_DIR / "submission_sentiment_llm_full_results.csv"
PROGRESS_CSV = OUTPUTS_DIR / "hansard_sentiment_progress.csv"

loader = SourceLoader()

_CONFIG_LIST = "\n".join(f'  "{k}": {v}' for k, v in CONFIGS.items())

SYSTEM_PROMPT = f"""\
You are an objective forensic auditor reading a spoken testimony transcript from an \
Electoral Boundaries Commission public hearing. The text below is one community \
participant's testimony — it may include the speaker name followed by their statement. \
Classify the speaker's stance on each of the following 7 boundary configurations. \
Use "Unrelated" when the configuration is not discussed.

Configurations (JSON key: human description):
{_CONFIG_LIST}

Stance definitions:
- Active Support: speaker explicitly requests, endorses, or advocates for the configuration.
- Active Opposition: speaker explicitly opposes or argues against the configuration.
- Neutral/Contextual: speaker discusses the geographic area but takes no position.
- Unrelated: the configuration is not discussed at all.

Rules:
- exact_quote must be a verbatim substring copied character-for-character from the text.
- exact_quote must be empty string for Unrelated or Neutral/Contextual entries.
- reasoning must be one sentence; empty string for Unrelated entries.
- Output ONLY valid JSON matching the schema. No markdown, no conversational text.\
"""


# ── Hansard parser ────────────────────────────────────────────────────────────

# Session header — "Public Participants" block followed by date line
PARTICIPANTS_RE = re.compile(
    r"Public Participants\s*\n(.*?)(?=(?:January|February|March|April|May|June|July|"
    r"August|September|October|November|December)\s+\d+,?\s+\d{4})",
    re.DOTALL,
)

# Match session title line to identify session boundaries in the main text
SESSION_TITLE_RE = re.compile(r"Title:\s+(.+?)\s+\[", re.MULTILINE)

# Speaker turn: a proper honorific-led or multi-word proper name followed by ": "
# Requires at least one of:
#   - Honorific prefix (Mr., Mrs., Ms., Dr., Justice, etc.)
#   - Two-word proper name  (catches "Craig Burrows-Johnson:" style)
# This intentionally excludes single words like "West:", "Edge:", riding names.
SPEAKER_RE = re.compile(
    r"(?:^|\n)"
    r"("
    r"(?:The Chair|The\s+\w+)"                             # "The Chair", "The Member"
    r"|(?:Mr\.|Mrs\.|Ms\.|Dr\.|Justice|Chief|Mayor|Reeve|Deputy|Honourable)\s+\S+"  # honorifics
    r"|[A-Z][a-z]+(?:\s+[A-Z][a-zA-Z'\-]+){1,4}"          # two+ word proper name (Craig Burrows-Johnson)
    r")"
    r":\s+",
    re.MULTILINE,
)


def _extract_last_name(full_name: str) -> str:
    """Extract last name token from 'Firstname Lastname, Title, ...' format."""
    name_part = full_name.split(",")[0].strip()
    tokens = name_part.split()
    return tokens[-1].lower() if tokens else ""


def _build_participant_index(text: str) -> dict[tuple[int, int], set[str]]:
    """
    Returns a mapping from (start_offset, end_offset) session ranges to
    sets of participant last names (lowercased) for that session.
    Used to identify community speakers vs Commission members.
    """
    # Parse participant blocks
    participant_blocks: list[tuple[int, set[str]]] = []
    for m in PARTICIPANTS_RE.finditer(text):
        raw_names = [l.strip() for l in m.group(1).split("\n") if l.strip()]
        last_names: set[str] = set()
        for name in raw_names:
            ln = _extract_last_name(name)
            if ln:
                last_names.add(ln)
        participant_blocks.append((m.start(), last_names))

    # Build ranges (each block lasts until the next block starts)
    index: dict[tuple[int, int], set[str]] = {}
    for i, (start, lnames) in enumerate(participant_blocks):
        end = participant_blocks[i + 1][0] if i + 1 < len(participant_blocks) else len(text)
        index[(start, end)] = lnames

    return index


def _session_participants(offset: int, index: dict[tuple[int, int], set[str]]) -> set[str]:
    for (start, end), lnames in index.items():
        if start <= offset < end:
            return lnames
    return set()


def _is_community_speaker(speaker: str, offset: int,
                          participant_index: dict[tuple[int, int], set[str]]) -> bool:
    """Return True if this speaker is a community participant (not Commission panel)."""
    # Always exclude known Commission members
    if speaker in COMMISSION_SPEAKERS:
        return False
    # "The Chair" pattern
    if speaker.startswith("The "):
        return False

    # Extract last name from speaker string ("Mrs. Miyanaga" → "miyanaga")
    tokens = speaker.split()
    # Strip honorific if present
    honorifics = {"Mr.", "Mrs.", "Ms.", "Dr.", "Justice", "Chief", "Mayor", "Reeve", "Deputy"}
    speaker_tokens = [t for t in tokens if t not in honorifics]
    if not speaker_tokens:
        return False
    speaker_last = speaker_tokens[-1].lower().rstrip(".,")

    # Check against session participant list
    participants = _session_participants(offset, participant_index)
    if participants:
        return speaker_last in participants

    # If no participant list available for this session, include any honourific-led speaker
    # that is not a known Commission member (conservative fallback)
    return True


def parse_community_turns(text: str) -> list[dict]:
    """
    Parse the Hansard into community participant speaker turns only.
    Returns list of {session, speaker, turn_num, text}.
    """
    participant_index = _build_participant_index(text)

    # Session titles for labelling
    session_titles: list[tuple[int, str]] = [
        (m.start(), m.group(1).strip()) for m in SESSION_TITLE_RE.finditer(text)
    ]
    def _session_label(offset: int) -> str:
        label = "Unknown"
        for (pos, title) in session_titles:
            if pos <= offset:
                label = title
        return label

    matches = list(SPEAKER_RE.finditer(text))
    turns = []
    turn_num = 0

    for i, m in enumerate(matches):
        speaker = m.group(1).strip()
        turn_start = m.end()
        turn_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        turn_text = text[turn_start:turn_end].strip()

        if not turn_text:
            continue

        if not _is_community_speaker(speaker, m.start(), participant_index):
            continue

        turns.append({
            "session":   _session_label(m.start()),
            "speaker":   speaker,
            "turn_num":  turn_num,
            "text":      turn_text,
        })
        turn_num += 1

    return turns


def turn_mentions_config(turn_text: str) -> list[str]:
    lower = turn_text.lower()
    return [key for key, kws in CONFIG_KEYWORDS.items() if any(kw in lower for kw in kws)]


# ── Progress tracking ─────────────────────────────────────────────────────────
def load_completed() -> set[str]:
    if not PROGRESS_CSV.exists():
        return set()
    with PROGRESS_CSV.open(encoding="utf-8") as f:
        return {row["turn_id"] for row in csv.DictReader(f)}


# ── Main ─────────────────────────────────────────────────────────────────────
def main(dry_run: bool = False) -> None:
    hansard_files = [
        ("hansard_r1", "hansard_r1"),
        ("hansard_r2", "hansard_r2"),
    ]

    completed = load_completed()
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    out_mode = "a" if OUTPUT_CSV.exists() else "w"
    out_fh = OUTPUT_CSV.open(out_mode, newline="", encoding="utf-8")
    out_writer = csv.DictWriter(out_fh, fieldnames=OUTPUT_FIELDS)
    if out_mode == "w":
        out_writer.writeheader()

    prog_mode = "a" if PROGRESS_CSV.exists() else "w"
    prog_fh = PROGRESS_CSV.open(prog_mode, newline="", encoding="utf-8")
    prog_writer = csv.DictWriter(prog_fh, fieldnames=["turn_id", "timestamp", "rows_emitted"])
    if prog_mode == "w":
        prog_writer.writeheader()

    total_turns = 0
    total_rows  = 0
    errors      = 0

    for scan_type, stem in hansard_files:
        txt_path = TEXT_DIR / f"{stem}.txt"
        if not txt_path.exists():
            print(f"WARNING: {txt_path} not found -- skipping")
            continue

        print(f"\n=== {stem} ({txt_path.stat().st_size // 1024:,} KB) ===")
        text = txt_path.read_text(encoding="utf-8", errors="replace")

        community_turns = parse_community_turns(text)
        print(f"  Community participant turns: {len(community_turns):,}")

        relevant = [(t, turn_mentions_config(t["text"])) for t in community_turns]
        relevant = [(t, keys) for t, keys in relevant if keys]
        print(f"  Turns mentioning configuration keywords: {len(relevant):,}")

        if dry_run:
            print("  Sample (first 5):")
            for t, keys in relevant[:5]:
                s  = t['session'][:40].encode('ascii', errors='replace').decode()
                sp = t['speaker'].encode('ascii', errors='replace').decode()
                tx = t['text'][:80].encode('ascii', errors='replace').decode()
                print(f"    [{s}] {sp}: {tx}...")
                print(f"      configs: {keys}")
            print(f"  [dry-run] would classify {len(relevant)} turns")
            continue

        for i, (turn, _hit_keys) in enumerate(relevant):
            turn_id = f"{scan_type}-{turn['turn_num']:05d}"
            if turn_id in completed:
                continue

            now = datetime.now().strftime("%H:%M:%S")
            label = f"{turn['speaker'][:28]} @ {turn['session'][:28]}"
            safe_label = label.encode("ascii", errors="replace").decode("ascii")
            print(f"[{now}] [{i+1}/{len(relevant)}] {safe_label}", end=" ... ", flush=True)

            result = call_claude(turn["text"], system_prompt=SYSTEM_PROMPT, json_schema=JSON_SCHEMA)
            total_turns += 1

            if not result:
                errors += 1
                print("ERROR")
                rows_emitted = 0
            else:
                rows_emitted = 0
                full_text = f"{turn['speaker']}: {turn['text']}"
                for key, desc in CONFIGS.items():
                    cfg = result.get(key, {})
                    if not isinstance(cfg, dict):
                        continue
                    classification = cfg.get("classification", "Unrelated")
                    if classification == "Unrelated":
                        continue
                    quote = cfg.get("exact_quote", "")
                    vr = verify_quote(quote, full_text, reasoning=cfg.get("reasoning", ""))
                    quote = vr.quote
                    quote_verified = vr.status
                    out_writer.writerow({
                        "submission_id":  turn_id,
                        "configuration":  desc,
                        "classification": classification,
                        "reasoning":      cfg.get("reasoning", ""),
                        "exact_quote":    quote,
                        "quote_verified": quote_verified,
                        "scan_type":      scan_type,
                    })
                    rows_emitted += 1
                    total_rows += 1
                print(f"{rows_emitted} results")

            prog_writer.writerow({
                "turn_id":      turn_id,
                "timestamp":    datetime.now().isoformat(),
                "rows_emitted": rows_emitted,
            })
            out_fh.flush()
            prog_fh.flush()
            time.sleep(0.3)

    out_fh.close()
    prog_fh.close()

    print(f"\nDone. {total_turns} turns classified, {total_rows} non-Unrelated rows written.")
    if errors:
        print(f"  {errors} errors.")

    if not dry_run and OUTPUT_CSV.exists():
        from collections import Counter
        by_cfg: dict[str, Counter] = {}
        with OUTPUT_CSV.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("scan_type") not in ("hansard_r1", "hansard_r2"):
                    continue
                by_cfg.setdefault(row["configuration"], Counter())[row["classification"]] += 1
        if by_cfg:
            print("\n--- Hansard summary ---")
            for cfg, counts in sorted(by_cfg.items()):
                print(
                    f"  {cfg[:60]:<60}  "
                    f"Support={counts.get('Active Support', 0)}  "
                    f"Oppose={counts.get('Active Opposition', 0)}  "
                    f"Neutral={counts.get('Neutral/Contextual', 0)}"
                )


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN --- no files will be written")
    main(dry_run=dry_run)
