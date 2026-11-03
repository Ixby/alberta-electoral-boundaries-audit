# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a9_stepb_calibrate.py
---------------------

Amendment 9: the single second calibration run. It scores version 2 of the
reconstruction procedure (a9_stepb_reconstruct_v2.py) on the same fixed
34-district sample, under exactly the Amendment 7 gates and the rules of
findings/a7_stepb_calibration_protocol.md. It reuses the frozen scorer
a7_stepb_calibrate.py unchanged and substitutes only the procedure.

Usage: python analysis/scripts/a9_stepb_calibrate.py --out findings/a9_stepb_calibration.json
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ["STEPB_V2_CALIBRATION_RUN"] = "1"

import a9_stepb_reconstruct_v2 as V2  # noqa: E402  (imports the real version 1 for its helpers)

sys.modules["a7_stepb_reconstruct"] = V2  # the frozen scorer imports the procedure by this name
import a7_stepb_calibrate as C  # noqa: E402

if __name__ == "__main__":
    C.main()
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    d = json.loads(out.read_text(encoding="utf-8"))
    d["procedure"] = "analysis/scripts/a9_stepb_reconstruct_v2.py (Amendment 9; scorer a7_stepb_calibrate.py, unchanged)"
    out.write_text(json.dumps(d, indent=1, default=float), encoding="utf-8")
