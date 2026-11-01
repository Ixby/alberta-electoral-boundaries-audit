# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
calibration_sample_plans.py
---------------------------

Save neutral plans for the lane calibration
(analysis/methodology/structural_lane_calibration_design.md).

Runs the sampler the size-matched sets ran: close_seats_ensemble.py at
amendment17-local-runs@2994113c (SHA-256 2e75ca75...4316), passed as --sampler,
loaded with only its repository path changed. After BURN steps it writes the
chain's assignment every SPACE steps, NPLANS plans in all, beside the chain's
CSV of per-step metrics.

  kernel s152       set D: s.15(2) mode with the Amendment 23 criteria table
                    (production set-D options)
  kernel canonical  the registered ensemble's kernel: half-band proposal, no
                    s.15(2) mode

Usage
  git show 2994113c:analysis/scripts/close_seats_ensemble.py > /tmp/cse_2994113c.py
  python analysis/scripts/calibration_sample_plans.py --sampler /tmp/cse_2994113c.py \\
         --idx 290 --out DIR [--burn 10000] [--space 2500] [--nplans 50] [--k 91] [--kernel s152]
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SAMPLER_SHA = "2e75ca758a3071bf713084912d93188b48b89ef6d667476d4a4a84ec2a014316"


def load_sampler(path):
    src = Path(path).read_text(encoding="utf-8")
    if hashlib.sha256(src.encode()).hexdigest() != SAMPLER_SHA:
        print(f"note: {path} is not close_seats_ensemble.py@2994113c", flush=True)
    src = src.replace("REPO = Path(__file__).resolve().parents[2]", f"REPO = Path({str(REPO)!r})", 1)
    spec = importlib.util.spec_from_loader("cse_calibration", loader=None)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cse_calibration"] = mod
    exec(compile(src, str(path), "exec"), mod.__dict__)
    return mod


def main(a):
    cse = load_sampler(a.sampler)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.kernel == "s152":
        cse.S152_PATH = REPO / "data/outputs/s15_2_va_criteria.csv"
        cse.OPTS.update(proposal_epsilon=0.5, muni_surcharge=0.0,
                        s152=hashlib.sha256(cse.S152_PATH.read_bytes()).hexdigest())
    else:
        cse.S152_PATH = None
        cse.OPTS.update(proposal_epsilon=None, muni_surcharge=0.0, s152=None)
    orig = cse._write_ckpt

    def hook(ckpt, payload):
        orig(ckpt, payload)
        done = payload["done"]
        if done >= a.burn and (done - a.burn) % a.space == 0:
            (out / f"plan_{a.idx}_{done}.json").write_text(json.dumps(payload["assignment"]), encoding="utf-8")

    cse._write_ckpt = hook
    cse.run("nk", a.idx, a.burn + a.space * (a.nplans - 1), 500, out / f"chain{a.idx}.csv", "", a.k)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sampler", required=True)
    ap.add_argument("--idx", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--burn", type=int, default=10000)
    ap.add_argument("--space", type=int, default=2500)
    ap.add_argument("--nplans", type=int, default=50)
    ap.add_argument("--k", type=int, default=91)
    ap.add_argument("--kernel", choices=["s152", "canonical"], default="s152")
    main(ap.parse_args())
