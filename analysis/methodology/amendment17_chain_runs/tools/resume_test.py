"""Resume-equivalence test for close_seats_ensemble.py nk mode.

A: one unbroken run.  B: same run killed after its 2nd checkpoint (mid chunk 3),
then restarted with --resume.  Pass = A and B CSVs are byte-identical.
"""
import filecmp, json, subprocess, sys, time
from pathlib import Path

REPO, PY, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
K, IDX, STEPS, CHUNK = "91", "221", "3000", "500"
SCRIPT = str(REPO / "analysis" / "scripts" / "close_seats_ensemble.py")
OUT.mkdir(parents=True, exist_ok=True)


def cmd(out, *extra):
    return [PY, "-W", "ignore", SCRIPT, "nk", "--k", K, "--idx", IDX, "--steps", STEPS,
            "--chunk", CHUNK, "--out", str(out), *extra]


a, b = OUT / "A.csv", OUT / "B.csv"
for f in OUT.glob("*"):
    f.unlink()

t = time.time()
r = subprocess.run(cmd(a), cwd=REPO, capture_output=True, text=True)
print("A exit", r.returncode, f"{time.time()-t:.0f}s", r.stdout.strip().splitlines()[-1:], flush=True)

p = subprocess.Popen(cmd(b, "--resume"), cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
ck = OUT / "B.csv.ckpt.json"
while True:
    if ck.exists():
        try:
            if json.loads(ck.read_text())["done"] >= 1500:
                break
        except Exception:
            pass
    if p.poll() is not None:
        sys.exit("B finished before it could be killed; raise STEPS")
    time.sleep(0.2)
p.kill(); p.wait()
rows_at_kill = sum(1 for _ in open(b)) - 1
print("B killed; checkpoint done>=1500, csv rows at kill =", rows_at_kill, flush=True)

r = subprocess.run(cmd(b, "--resume"), cwd=REPO, capture_output=True, text=True)
print("B resume exit", r.returncode, r.stdout.strip().splitlines(), flush=True)
same = filecmp.cmp(a, b, shallow=False)
print("A rows", sum(1 for _ in open(a)) - 1, "B rows", sum(1 for _ in open(b)) - 1)
print("RESULT:", "IDENTICAL" if same else "DIFFERENT")
