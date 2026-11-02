"""Diagnostic only (not a registered set): set D harness on the status-reading table; save the assignment every SPACE steps after BURN."""
import json, sys, hashlib
from pathlib import Path
sys.path.insert(0, "/tmp/claude-0/-home-user-alberta-electoral-boundaries-audit/9af3a5a2-4682-51b8-9140-74f10ed8aad4/scratchpad/calib")
import cse_s152 as cse
idx, k, outd, burn, space, n = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
outd.mkdir(parents=True, exist_ok=True)
cse.S152_PATH = Path("/home/user/alberta-electoral-boundaries-audit/data/outputs/s15_2_va_criteria_status.csv")
cse.OPTS.update(proposal_epsilon=0.5, muni_surcharge=0.0, s152=hashlib.sha256(cse.S152_PATH.read_bytes()).hexdigest())
orig = cse._write_ckpt
def hook(ckpt, payload):
    orig(ckpt, payload)
    d = payload["done"]
    if d >= burn and (d - burn) % space == 0:
        (outd / f"plan_{idx}_{d}.json").write_text(json.dumps(payload["assignment"]))
cse._write_ckpt = hook
cse.run("nk", idx, burn + space * (n - 1), 500, outd / f"chain{idx}.csv", "", k)
