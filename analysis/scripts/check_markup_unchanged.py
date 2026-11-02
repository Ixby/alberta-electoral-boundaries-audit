# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
check_markup_unchanged.py
-------------------------

Companion to check_numbers_unchanged.py for voice-only rewrites (style guide
§4): links, markup, placeholders and code must survive the rewrite untouched.
Compares each file at a git ref with the working tree, as multisets:

  link targets     markdown ](target) and href= / src= values
  tags             HTML/Svelte tag names, opening and closing
  placeholders     %s, __BASE__, {expressions}, ${...}
  code             `inline code` spans and fenced code blocks
  headings         markdown heading lines (anchors depend on them)

Any difference FAILS. Usage
  python analysis/scripts/check_markup_unchanged.py --base REF FILE [FILE ...]
"""
import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

PATTERNS = {
    "link targets": re.compile(r"\]\(([^)\s]+)\)|\b(?:href|src)=\\?[\"']([^\"'\\]+)"),
    "tags": re.compile(r"</?([a-zA-Z][a-zA-Z0-9:-]*)\b"),
    "placeholders": re.compile(r"%s|__BASE__|\$\{[^}]*\}|(?<![\\$])\{[^{}\n]{1,80}\}"),
    "code": re.compile(r"```.*?```|`[^`\n]+`", re.S),
}


def grab(text, path):
    out = {}
    for name, rx in PATTERNS.items():
        if name == "code" and path.endswith(".ts"):
            continue  # template literals in .ts are code, not markdown code spans
        vals = []
        for m in rx.finditer(text):
            vals.append(next((g for g in m.groups() if g), m.group(0)) if m.groups() else m.group(0))
        out[name] = Counter(vals)
    if path.endswith(".md"):
        out["headings"] = Counter(l.strip() for l in text.splitlines() if re.match(r"^#{1,6} ", l))
    return out


def main(a):
    failed = False
    for f in a.files:
        r = subprocess.run(["git", "show", f"{a.base}:{f}"], capture_output=True, text=True)
        if r.returncode:
            print(f"SKIP {f}: not in {a.base}")
            continue
        old, new = grab(r.stdout, f), grab(Path(f).read_text(encoding="utf-8"), f)
        bad = []
        for k in old:
            lost, gained = old[k] - new[k], new[k] - old[k]
            if lost or gained:
                bad.append(f"   {k}: removed {dict(lost)} added {dict(gained)}"[:600])
        if bad:
            failed = True
            print(f"FAIL {f}")
            print("\n".join(bad))
        else:
            print(f"ok   {f}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/master")
    ap.add_argument("files", nargs="+")
    main(ap.parse_args())
