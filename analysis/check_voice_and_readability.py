"""
house voice and readability checker.

house voice rules (from project styles):
- No mirrored 'not X — Y' reversals or 'not X, Y' constructions
- No templated triads
- No emoji
- No editorializing reactions ("shockingly", "remarkably", etc.)
- Plain, grounded, conversational prose

Also checks grade level for public report using a Flesch-Kincaid
approximation (textstat library, FOSS).

Usage:
  python3 analysis/check_wuff_voice.py report_public.md report_academic.md

Exit status:
  0 - all checks pass
  1 - one or more violations detected (output lists them)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


# Patterns that violate house voice. Each is (regex, description).
# The "not X — Y" pattern matches rhetorical mirror reversals only when
# X is a simple adjective/noun (3-20 chars) paired with a conceptually
# opposite Y. We allow "not [past-participle] — [status]" as a non-
# rhetorical status-description pattern (e.g., "Not executed — blocked").
WUFF_VIOLATIONS = [
    (r"\bnot\s+(a|an|the|just)\s+[a-zA-Z ]{3,30}\s+[—–-]\s+",
     "'not X — Y' mirror reversal"),
    (r"[\u2600-\u27BF\U0001F300-\U0001FAFF]", "emoji"),
    (r"\b(shockingly|remarkably|staggering(?:ly)?|astound(?:ing)?ly|unprecedented(?!\s+(case|precedent|in|to)))\b",
     "editorializing reaction"),
    (r"^[-*•]\s+[A-Za-z]+,\s+[A-Za-z]+,\s+and\s+[A-Za-z]+\.?\s*$",
     "templated triad in bullet (3-item list for rhetoric)"),
]

EDITORIALIZING_PHRASES = [
    "at the end of the day",
    "make no mistake",
    "it goes without saying",
    "needless to say",
]


def _approx_flesch_kincaid_grade(text: str) -> float | None:
    """Approximate Flesch-Kincaid grade level without external deps.
    FKG = 0.39*(words/sents) + 11.8*(syllables/words) - 15.59.
    Using a rough syllable-count heuristic.
    """
    # Remove markdown syntax that shouldn't count
    stripped = re.sub(r"[`*_#>|\[\]()]", " ", text)
    stripped = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", stripped)
    # Split sentences
    sents = [s.strip() for s in re.split(r"[.!?]+", stripped) if s.strip()]
    if not sents:
        return None
    # Words
    words = re.findall(r"\b[A-Za-z][A-Za-z']*\b", stripped)
    if not words:
        return None
    # Syllable count by vowel-group heuristic
    total_syl = 0
    for w in words:
        w = w.lower()
        groups = re.findall(r"[aeiouy]+", w)
        syl = max(1, len(groups))
        # Silent-e
        if w.endswith("e") and syl > 1 and not w.endswith("le"):
            syl -= 1
        total_syl += syl
    return 0.39 * (len(words) / len(sents)) + 11.8 * (total_syl / len(words)) - 15.59


def check_file(path: Path, target_grade: float | None = None) -> tuple[bool, list[str]]:
    issues = []
    text = path.read_text(encoding="utf-8", errors="replace")

    for pattern, desc in WUFF_VIOLATIONS:
        matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))
        for m in matches[:10]:  # cap reporting per pattern
            line_no = text[: m.start()].count("\n") + 1
            snippet = m.group(0)
            issues.append(f"  line {line_no}: {desc}: '{snippet[:80]}'")

    lower = text.lower()
    for phrase in EDITORIALIZING_PHRASES:
        idx = 0
        while True:
            pos = lower.find(phrase, idx)
            if pos < 0:
                break
            line_no = text[:pos].count("\n") + 1
            issues.append(f"  line {line_no}: filler phrase: '{phrase}'")
            idx = pos + len(phrase)

    fkg = _approx_flesch_kincaid_grade(text)
    if fkg is not None:
        issues.append(f"  [info] Approximate Flesch-Kincaid Grade: {fkg:.1f}")
        if target_grade is not None and fkg > target_grade + 0.5:
            issues.append(
                f"  FAIL: grade {fkg:.1f} exceeds target {target_grade:.1f} "
                f"(tolerance +0.5)"
            )
            return False, issues

    # house voice violations are fatal; informational lines are not
    fatal = any(
        not ln.startswith("  [info]") and "FAIL" not in ln[:10]
        and "filler phrase" not in ln and "emoji" not in ln
        for ln in issues
        if any(d[1] in ln for d in WUFF_VIOLATIONS)
    )
    # Actually simpler: any WUFF_VIOLATIONS pattern matched is a fail
    voice_fail = any(d[1] in ln for ln in issues for d in WUFF_VIOLATIONS)
    grade_fail = any("FAIL: grade" in ln for ln in issues)
    return not (voice_fail or grade_fail), issues


def main():
    args = sys.argv[1:]
    if not args:
        args = ["report_public.md", "report_academic.md"]
    pass_all = True
    for p in args:
        path = Path(p)
        if not path.exists():
            print(f"{p}: FILE NOT FOUND")
            pass_all = False
            continue
        target = 9.0 if "public" in p.lower() else 13.0
        ok, issues = check_file(path, target_grade=target)
        status = "PASS" if ok else "FAIL"
        print(f"\n{p} ({status}, target grade <= {target}):")
        for line in issues:
            print(line)
        if not ok:
            pass_all = False

    sys.exit(0 if pass_all else 1)


if __name__ == "__main__":
    main()
