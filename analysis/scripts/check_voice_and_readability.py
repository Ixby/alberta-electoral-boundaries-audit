"""
Voice and readability checker for audit reports.

Reports Flesch-Kincaid grade level against house-voice targets (advisory only —
scores outside target range print WARN but do not fail CI):
  public report   → grade 13–18 (post-secondary to advanced professional)
  academic report → grade ≤ 13

Usage:
  python analysis/scripts/check_voice_and_readability.py
  python analysis/scripts/check_voice_and_readability.py --report academic
  python analysis/scripts/check_voice_and_readability.py --report public
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import textstat
except ImportError:
    sys.exit("textstat not installed — run: pip install textstat==0.7.13")

ROOT = Path(__file__).resolve().parent.parent.parent

REPORTS = {
    "public": {
        "path": ROOT / "reports" / "public" / "report_public.md",
        "min_grade": 13,
        "max_grade": 18,
        "label": "Public report",
    },
    "academic": {
        "path": ROOT / "reports" / "academic" / "report_academic.md",
        "max_grade": 13,
        "label": "Academic report",
    },
}


def strip_markdown(text: str) -> str:
    """Remove Markdown markup so grade calculation operates on prose only."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def check_report(name: str, cfg: dict) -> None:
    path = cfg["path"]
    min_grade = cfg.get("min_grade")
    max_grade = cfg.get("max_grade")
    label = cfg["label"]

    if not path.exists():
        print(f"  SKIP  {label}: not found at {path.relative_to(ROOT)}")
        return

    prose = strip_markdown(path.read_text(encoding="utf-8"))
    fk = textstat.flesch_kincaid_grade(prose)
    flesch = textstat.flesch_reading_ease(prose)
    words = textstat.lexicon_count(prose)

    if min_grade is not None and max_grade is not None:
        target_str = f"{min_grade}-{max_grade}"
        in_range = min_grade <= fk <= max_grade
    elif max_grade is not None:
        target_str = f"<={max_grade}"
        in_range = fk <= max_grade
    else:
        target_str = "unset"
        in_range = True

    status = "OK  " if in_range else "WARN"
    print(
        f"  {status}  {label}: FK grade {fk:.1f} (target {target_str})"
        f"  |  Flesch ease {flesch:.1f}  |  {words:,} words"
    )


def main():
    parser = argparse.ArgumentParser(description="Check report readability (advisory).")
    parser.add_argument(
        "--report",
        choices=list(REPORTS) + ["all"],
        default="all",
        help="Which report to check (default: all)",
    )
    args = parser.parse_args()

    targets = REPORTS if args.report == "all" else {args.report: REPORTS[args.report]}

    print("=" * 60)
    print("  Voice & Readability Check  [advisory - does not fail CI]")
    print("=" * 60)

    for name, cfg in targets.items():
        check_report(name, cfg)

    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
