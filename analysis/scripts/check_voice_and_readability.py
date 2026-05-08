"""
House voice and readability checker.

House voice rules (from project styles):
- No mirrored 'not X — Y' reversals
- No templated triads
- No emoji
- No editorializing reactions ("shockingly", "remarkably", etc.)
- Plain, grounded, conversational prose

Also checks grade level for public report using Flesch-Kincaid.
Prefers the textstat library (installed via setup.sh) when available;
falls back to a local approximation otherwise.

Usage:
  python3 analysis/scripts/check_voice_and_readability.py report_public.md report_academic.md

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
# HIGH-09: broadened the 'not X — Y' detector to catch bare-adjective
# and bare-noun forms ("not partisan — structural", "not gerrymandering
# — redistribution"). The previous pattern required a leading
# 'a/an/the/just' and missed the most common house-voice violation.
#
# Rhetorical-mirror shape: exactly one word between `not` and the dash.
# We also allow the optional determiner prefix (a/an/the/just) from
# the original rule. Status-description patterns ("Not executed —
# blocked", "not computed — blocked by", "not attempted in this pass
# — …") naturally fail the "one word only before dash" requirement
# when extra clause material is present; for bare status participles
# that do fit the shape, we stop-list the common ones.
_NOT_MIRROR_STOP = (
    r"(?:executed|blocked|applied|installed|registered|activated"
    r"|scheduled|staged|posted|merged|computed|attempted|tested"
    r"|verified|submitted|configured|assigned|deployed|available"
    r"|absent|present|required|covered|included|excluded|reported"
    r"|known|shown|given|listed|addressed|observed|recorded)"
)
# Prepositions / conjunctions that signal Y is a multi-word
# parenthetical rather than a single mirror term.
_Y_STOP_PREFIX = (
    r"(?:for|in|on|at|to|with|from|as|by|of|if|though|but|and"
    r"|or|because|since|while|when|where|although|however)"
)
WUFF_VIOLATIONS = [
    # Determiner form: retained from v0 for backward coverage of
    # "not a bug — feature" style (X may include spaces).
    (
        r"\bnot\s+(a|an|the|just)\s+[a-zA-Z ]{3,30}\s+[—–-]\s+",
        "'not X — Y' mirror reversal",
    ),
    # Bare form: single word between `not` and the dash, followed
    # by a non-preposition word on the Y side. Catches the common
    # audit-voice violations ("not partisan — structural", "not
    # gerrymandering — redistribution") the determiner form missed.
    # Prepositions on the Y side lead parentheticals ("not absent
    # — for configurations that…") rather than mirror terms;
    # status-participle stoplist filters procedural prose.
    (
        r"\bnot\s+"
        r"(?!" + _NOT_MIRROR_STOP + r"\b)"
        r"[A-Za-z]{3,30}\s+[—–-]\s+"
        r"(?!" + _Y_STOP_PREFIX + r"\b)"
        r"[A-Za-z]",
        "'not X — Y' mirror reversal",
    ),
    (r"[\u2600-\u27BF\U0001F300-\U0001FAFF]", "emoji"),
    (
        r"\b(shockingly|remarkably|staggering(?:ly)?|astound(?:ing)?ly|unprecedented(?!\s+(case|precedent|in|to)))\b",
        "editorializing reaction",
    ),
    (
        r"^[-*•]\s+[A-Za-z]+,\s+[A-Za-z]+,\s+and\s+[A-Za-z]+\.?\s*$",
        "templated triad in bullet (3-item list for rhetoric)",
    ),
]

EDITORIALIZING_PHRASES = [
    "at the end of the day",
    "make no mistake",
    "it goes without saying",
    "needless to say",
]


def _flesch_kincaid_grade(text: str) -> tuple[float | None, str]:
    """Compute Flesch-Kincaid grade level.

    Returns (grade, method) where method is 'textstat' if the peer-
    reviewed library was used, or 'approx' if the local fallback
    approximation was used. Markdown syntax is stripped before scoring.
    """
    stripped = re.sub(r"[`*_#>|\[\]()]", " ", text)
    stripped = re.sub(r"!?\[[^\]]*\]\([^)]*\)", "", stripped)

    try:
        import textstat as _ts

        return float(_ts.flesch_kincaid_grade(stripped)), "textstat"
    except ImportError:
        pass

    sents = [s.strip() for s in re.split(r"[.!?]+", stripped) if s.strip()]
    if not sents:
        return None, "approx"
    words = re.findall(r"\b[A-Za-z][A-Za-z']*\b", stripped)
    if not words:
        return None, "approx"
    total_syl = 0
    for w in words:
        w = w.lower()
        groups = re.findall(r"[aeiouy]+", w)
        syl = max(1, len(groups))
        if w.endswith("e") and syl > 1 and not w.endswith("le"):
            syl -= 1
        total_syl += syl
    return (
        0.39 * (len(words) / len(sents)) + 11.8 * (total_syl / len(words)) - 15.59,
        "approx",
    )


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

    fkg, method = _flesch_kincaid_grade(text)
    if fkg is not None:
        label = (
            "Flesch-Kincaid Grade"
            if method == "textstat"
            else "Approximate Flesch-Kincaid Grade"
        )
        issues.append(f"  [info] {label}: {fkg:.1f}  [method={method}]")
        # HIGH-10: only treat the grade as gate-blocking when computed
        # by textstat. The local vowel-group approximation can differ
        # from textstat by +/-2 grade levels on typical prose; failing
        # the gate on that approximation produced false FAIL verdicts
        # on machines without textstat installed. Under 'approx' we
        # still emit the informational line but let the gate pass.
        if (
            target_grade is not None
            and method == "textstat"
            and fkg > target_grade + 0.5
        ):
            issues.append(
                f"  FAIL: grade {fkg:.1f} exceeds target {target_grade:.1f} "
                f"(tolerance +0.5)"
            )
            return False, issues
        elif (
            target_grade is not None and method == "approx" and fkg > target_grade + 0.5
        ):
            # Downgraded to informational so reviewers without textstat
            # do not get spurious FAIL output.
            issues.append(
                f"  [info] approximation reports grade {fkg:.1f} above "
                f"target {target_grade:.1f} — install textstat to gate."
            )

    # house voice violations are fatal; informational lines are not
    fatal = any(
        not ln.startswith("  [info]")
        and "FAIL" not in ln[:10]
        and "filler phrase" not in ln
        and "emoji" not in ln
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
        # Public report targets undergrad reading level (Alberta Views
        # audience); academic report sits a notch higher.
        target = 12.0 if "public" in p.lower() else 13.0
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
