# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_run.py
----------

Amendment 10: the registered run, in order, in one command.

  1. a10_reconstruct_pages.py PAGES_DIR ED...  version 3 on every page that is not a
                                               known district (skipped per page when its
                                               json exists, so a stopped run resumes)
  2. a10_neighbours.py PAGES_DIR               neighbour numbers, city labels and drawn
                                               neighbour boundaries of every page
  3. a10_inset.py fit PAGES_DIR                the locator insets carried to ground
  4. a10_stepb_calibrate.py --pages PAGES_DIR  assemble -> snap/assign -> gates and sanity
     --out OUT_JSON

Each step runs in the same Python as this script and must exit 0; the run stops at the
first failure. Steps 2-4 always run in full. Python 3.12.13 with PyMuPDF 2.1 (the scorer
refuses any other).

Usage: python -W ignore analysis/scripts/a10_run.py PAGES_DIR OUT_JSON [--skip-pages]
  --skip-pages  steps 2-4 only, on page outputs already in PAGES_DIR
"""
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TUNING = [3, 5, 7, 9, 12, 15, 16, 17, 19, 20, 21, 23, 24, 25, 29, 30, 32, 37, 38, 43, 65, 88]


def pages_to_run():
    sample = json.loads((REPO / "findings/a7_stepb_sample.json").read_text(encoding="utf-8"))["sample"]
    s = json.loads((REPO / "findings/a7_stepb_sample.json").read_text(encoding="utf-8"))
    changed = s.get("changed")
    eds = sorted(set(int(x) for x in sample) | set(int(x) for x in changed))
    assert len(eds) == 69 and not set(eds) & set(TUNING), eds
    return eds


def step(name, args):
    t0 = time.time()
    print(f"== {name}: {' '.join(str(a) for a in args)}", flush=True)
    r = subprocess.run([sys.executable, "-W", "ignore", *map(str, args)], cwd=REPO)
    print(f"== {name}: exit {r.returncode}, {time.time() - t0:.0f} s", flush=True)
    if r.returncode != 0:
        sys.exit(f"{name} failed (exit {r.returncode})")


def main():
    pages, out = Path(sys.argv[1]), Path(sys.argv[2])
    pages.mkdir(parents=True, exist_ok=True)
    if "--skip-pages" not in sys.argv:
        step("pages", [HERE / "a10_reconstruct_pages.py", pages, *pages_to_run()])
    step("neighbours", [HERE / "a10_neighbours.py", pages])
    step("inset", [HERE / "a10_inset.py", "fit", pages])
    step("score", [HERE / "a10_stepb_calibrate.py", "--pages", pages, "--out", out])


if __name__ == "__main__":
    main()
