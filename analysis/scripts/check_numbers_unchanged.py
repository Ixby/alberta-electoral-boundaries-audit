# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
check_numbers_unchanged.py
--------------------------

Guard for voice-only rewrites (VOICE.md): every number in a file must survive
the rewrite. Compares each file at a git ref with the working tree.

  numerals      every numeric token (1,234 / 4.10% / −0.0072 / 2026), commas
                and sign variants normalised; any difference FAILS
  number words  zero to twenty, hundred, thousand, million, half, twice;
                differences are reported as WARN (a rewrite may spell out
                "3" as "three"), to be checked by hand

Usage
  python analysis/scripts/check_numbers_unchanged.py --base origin/master FILE [FILE ...]
Exit status 1 if any file's numerals changed.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

NUM = re.compile(r"(?<![\w.])[-+−–]?\d[\d,]*(?:\.\d+)?%?")
WORDS = re.compile(r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
                   r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|hundred|thousand|million|half|twice)\b", re.I)


def numerals(text):
    out = Counter()
    for m in NUM.findall(text):
        t = m.replace(",", "").replace("−", "-").replace("–", "-").lstrip("+")
        out[t.lstrip("-") if t.startswith("-") and not re.match(r"-\d", t) else t] += 1
    return out


def words(text):
    return Counter(w.lower() for w in WORDS.findall(text))


def at_ref(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main(a):
    failed = False
    for f in a.files:
        old = at_ref(a.base, f)
        if old is None:
            print(f"SKIP {f}: not in {a.base}")
            continue
        new = Path(f).read_text(encoding="utf-8")
        on, nn = numerals(old), numerals(new)
        lost, gained = on - nn, nn - on
        if lost or gained:
            failed = True
            print(f"FAIL {f}")
            if lost:
                print("   removed: " + ", ".join(f"{k}×{v}" for k, v in sorted(lost.items())))
            if gained:
                print("   added:   " + ", ".join(f"{k}×{v}" for k, v in sorted(gained.items())))
        else:
            print(f"ok   {f} ({sum(on.values())} numerals unchanged)")
        ow, nw = words(old), words(new)
        if ow != nw:
            d = {k: nw[k] - ow[k] for k in set(ow) | set(nw) if nw[k] != ow[k]}
            print("   WARN number words changed: " + ", ".join(f"{k} {v:+d}" for k, v in sorted(d.items())))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/master")
    ap.add_argument("files", nargs="+")
    main(ap.parse_args())
