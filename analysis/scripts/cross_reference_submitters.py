"""
Cross-reference EBC written submitters against Hansard public hearing participants.

Purpose:
    Identify people who both submitted a written submission to the EBC AND testified
    at a public hearing (appeared in the Hansard). Dual contributors are stronger
    signals of community engagement and can be weighted higher in sentiment analysis.

Outputs:
    data/outputs/cross_reference_submitters.csv
    data/outputs/hansard_participants_full.csv

CLI:
    python cross_reference_submitters.py [--dry-run]

Dependencies:
    Forward: data/outputs/cross_reference_submitters.csv,
             data/outputs/hansard_participants_full.csv
    Backward: analysis/utils/sentiment_config.py, analysis/utils/source_loader.py,
              .temp/submissions/text/hansard_r1.txt,
              .temp/submissions/text/hansard_r2.txt, .temp/submissions/text/*.txt
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from sentiment_config import DATA_DIR, TEXT_DIR, OUTPUTS_DIR
from source_loader import SourceLoader

loader = SourceLoader()

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

PARTICIPANTS_RE = re.compile(
    r"Public Participants\s*\n(.*?)(?=(?:January|February|March|April|May|June|July|"
    r"August|September|October|November|December)\s+\d+,?\s+\d{4})",
    re.DOTALL,
)

# For session header extraction (city + date)
SESSION_HEADER_RE = re.compile(
    r"Electoral Boundaries Commission Public Hearings\s*[–-]\s*([^\n]+)\s*\n"
    r"Public Participants"
)

NAME_HEURISTICS = [
    re.compile(r"(?:My name is|I am|I'm|I,)\s+([A-Z][a-z]+\s+[A-Z][a-zA-Z'\-]+)"),
    re.compile(r"(?:Submitted by|From:|Sincerely,|Regards,|Respectfully,)\s*\n?\s*([A-Z][a-z]+\s+[A-Z][a-zA-Z'\-]+)"),
]
NAME_FIRST_LINE_RE = re.compile(r"^([A-Z][a-z]+\s+[A-Z][a-zA-Z'\-]+)\s*\n")


# ---------------------------------------------------------------------------
# Step 1: Parse Hansard participant lists
# ---------------------------------------------------------------------------

def _extract_session_label(text: str, match_start: int) -> str:
    """Find the nearest session header before the Public Participants block."""
    preceding = text[:match_start]
    headers = list(SESSION_HEADER_RE.finditer(preceding))
    if headers:
        return headers[-1].group(1).strip()
    return "Unknown"


def parse_hansard(hansard_round: int) -> list[dict]:
    """
    Parse a Hansard file and return a list of participant records.

    Each record has:
        name, last_name, is_mla, hansard_round, session
    """
    text, found = loader.get_text(f"hansard_r{hansard_round}")
    if not found:
        print(f"WARNING: Hansard file not found for round {hansard_round}")
        return []

    records: list[dict] = []

    for m in PARTICIPANTS_RE.finditer(text):
        block = m.group(1)
        session = _extract_session_label(text, m.start())

        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            # Skip lines that look like dates or header fragments
            if re.match(
                r"^(?:January|February|March|April|May|June|July|August|"
                r"September|October|November|December)\s+\d",
                line,
            ):
                continue
            if re.match(r"^\d{1,2}:\d{2}", line):
                continue

            # Detect MLA marker before stripping roles
            is_mla = bool(re.search(r"\bMLA\b", line))

            # Strip role/title suffix: take only the part before the first comma
            name_part = line.split(",")[0].strip()

            # Must look like "Firstname Lastname" (at least two words)
            parts = name_part.split()
            if len(parts) < 2:
                continue

            last_name = parts[-1]

            records.append(
                {
                    "name": name_part,
                    "last_name": last_name,
                    "is_mla": is_mla,
                    "hansard_round": hansard_round,
                    "session": session,
                }
            )

    return records


def build_participant_list() -> list[dict]:
    r1 = parse_hansard(1)
    r2 = parse_hansard(2)
    return r1 + r2


# ---------------------------------------------------------------------------
# Step 2: Extract submitter names from text files
# ---------------------------------------------------------------------------

def extract_name_from_text(text: str) -> str:
    """
    Try three heuristics in order; return 'Unknown' if none match.
    """
    # Heuristic 1 & 3 (as per spec order — heuristic 2 requires first 500 chars)
    for pat in NAME_HEURISTICS[:1]:  # "My name is / I am / I'm / I,"
        m = pat.search(text)
        if m:
            return m.group(1).strip()

    # Heuristic 2: name at very start of text (first 500 chars)
    snippet = text[:500]
    m = NAME_FIRST_LINE_RE.search(snippet)
    if m:
        return m.group(1).strip()

    # Heuristic 3: closing salutation / attribution
    m = NAME_HEURISTICS[1].search(text)
    if m:
        return m.group(1).strip()

    return "Unknown"


def build_submitter_list() -> list[dict]:
    """
    Scan all .txt files in TEXT_DIR (skip hansard_*.txt) and extract names.
    """
    records: list[dict] = []
    for fpath in sorted(TEXT_DIR.glob("*.txt")):
        if fpath.name.startswith("hansard_"):
            continue
        submission_id = fpath.stem  # e.g. EBC-2025-1-0012
        text = fpath.read_text(encoding="utf-8", errors="replace")
        name = extract_name_from_text(text)
        parts = name.split() if name != "Unknown" else []
        last_name = parts[-1] if len(parts) >= 2 else ""
        records.append(
            {
                "submission_id": submission_id,
                "name": name,
                "last_name": last_name,
            }
        )
    return records


# ---------------------------------------------------------------------------
# Step 3: Cross-reference by last name
# ---------------------------------------------------------------------------

def _first_initial(name: str) -> str:
    """Return the first letter of the first word, lowercased. Empty string if unavailable."""
    parts = name.strip().split()
    if parts:
        return parts[0][0].lower()
    return ""


def cross_reference(
    submitters: list[dict],
    participants: list[dict],
) -> list[dict]:
    """
    Match submitters against Hansard participants by last name.

    Returns a list of cross-reference hit records.
    """
    # Build a lookup: lowercase last_name -> list of participant records
    participant_index: dict[str, list[dict]] = {}
    for p in participants:
        key = p["last_name"].lower()
        if key:
            participant_index.setdefault(key, []).append(p)

    hits: list[dict] = []

    for sub in submitters:
        sub_last = sub["last_name"].lower()
        if not sub_last:
            continue

        # Exact match
        matched_participants = participant_index.get(sub_last, [])

        # Partial / substring match (Low confidence)
        partial_participants: list[dict] = []
        if not matched_participants and len(sub_last) >= 4:
            for p_last, p_list in participant_index.items():
                if len(p_last) >= 4 and (
                    sub_last in p_last or p_last in sub_last
                ) and p_last != sub_last:
                    partial_participants.extend(p_list)

        for p in matched_participants:
            # Determine confidence
            sub_init = _first_initial(sub["name"])
            p_init = _first_initial(p["name"])
            if sub_init and p_init and sub_init == p_init:
                confidence = "High"
            else:
                confidence = "Medium"

            hits.append(
                {
                    "submission_id": sub["submission_id"],
                    "submitter_name": sub["name"],
                    "hansard_round": p["hansard_round"],
                    "hansard_session": p["session"],
                    "participant_name": p["name"],
                    "is_mla": p["is_mla"],
                    "match_confidence": confidence,
                }
            )

        for p in partial_participants:
            hits.append(
                {
                    "submission_id": sub["submission_id"],
                    "submitter_name": sub["name"],
                    "hansard_round": p["hansard_round"],
                    "hansard_session": p["session"],
                    "participant_name": p["name"],
                    "is_mla": p["is_mla"],
                    "match_confidence": "Low",
                }
            )

    return hits


# ---------------------------------------------------------------------------
# Step 4: Output
# ---------------------------------------------------------------------------

XREF_FIELDS = [
    "submission_id",
    "submitter_name",
    "hansard_round",
    "hansard_session",
    "participant_name",
    "is_mla",
    "match_confidence",
]

PARTICIPANT_FIELDS = [
    "name",
    "last_name",
    "is_mla",
    "hansard_round",
    "session",
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    submitters: list[dict],
    participants: list[dict],
    hits: list[dict],
) -> None:
    total_subs = len(submitters)
    named_subs = sum(1 for s in submitters if s["name"] != "Unknown")

    high = [h for h in hits if h["match_confidence"] == "High"]
    medium = [h for h in hits if h["match_confidence"] == "Medium"]
    low = [h for h in hits if h["match_confidence"] == "Low"]

    print(f"Submitters with extractable names: {named_subs} / {total_subs}")
    print(f"Total Hansard participants: {len(participants)}")
    print()
    print(f"Cross-reference hits by confidence:")
    print(f"  High   (last name + first initial match): {len(high)}")
    print(f"  Medium (last name only):                  {len(medium)}")
    print(f"  Low    (partial last name):               {len(low)}")
    print()

    if high or medium:
        print("High and Medium confidence matches:")
        for h in sorted(high + medium, key=lambda x: x["match_confidence"]):
            mla_tag = " [MLA]" if h["is_mla"] else ""
            print(
                f"  [{h['match_confidence']}] {h['submission_id']} | "
                f"Submitter: {h['submitter_name']} | "
                f"Participant: {h['participant_name']}{mla_tag} | "
                f"R{h['hansard_round']} {h['hansard_session']}"
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cross-reference EBC submitters against Hansard participants."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without writing output files.",
    )
    args = parser.parse_args()

    print("Step 1: Parsing Hansard participant lists...")
    participants = build_participant_list()
    print(f"  Found {len(participants)} participant records across both rounds.")

    print("Step 2: Extracting submitter names from submission text files...")
    submitters = build_submitter_list()
    print(f"  Scanned {len(submitters)} submission files.")

    print("Step 3: Cross-referencing by last name...")
    hits = cross_reference(submitters, participants)
    print(f"  Found {len(hits)} cross-reference hits.")

    print()
    print_summary(submitters, participants, hits)

    if args.dry_run:
        print()
        print("Dry run: no output files written.")
        return

    xref_path = OUTPUTS_DIR / "cross_reference_submitters.csv"
    write_csv(xref_path, XREF_FIELDS, hits)
    print(f"Wrote: {xref_path}")

    participants_path = OUTPUTS_DIR / "hansard_participants_full.csv"
    write_csv(participants_path, PARTICIPANT_FIELDS, participants)
    print(f"Wrote: {participants_path}")


if __name__ == "__main__":
    main()
