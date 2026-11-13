"""w03: run_structural_battery.main with S5_MIDPOINT = 0.0019398 (Amendment 12, Part 3) and --votes the all-ballots file."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402
import run_structural_battery as r  # noqa: E402

_a12.check_va()
r.S5_MIDPOINT = _a12.S5_ALL
_a12.noop_logger(r)
args = sys.argv[1:] or ["--shapefile", str(_a12.MAP), "--votes", str(_a12.VA_ALL),
                        "--output", str(_a12.OUT / "structural_allballots.json"), "--label", "iap_2026_assembled"]
rc = r.main(args)
# compute_S5_drain returns a STUB dict on any exception; that is a failure, not a result (run sheet, step 2).
import json  # noqa: E402
out = Path(args[args.index("--output") + 1]) if "--output" in args else None
if rc in (0, None) and out is not None:
    s5 = json.loads(out.read_text())["metrics"]["S5_drain_score"]
    if s5.get("flag") is None or str(s5.get("_note", "")).startswith("STUB"):
        sys.exit(f"S5 did not execute: {s5}")
sys.exit(rc)
