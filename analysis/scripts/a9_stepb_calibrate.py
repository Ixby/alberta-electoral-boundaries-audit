# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a9_stepb_calibrate.py
---------------------

Amendment 9: the single second calibration run. It scores version 3 of the
reconstruction procedure (a9_stepb_reconstruct_v3.py) on the same fixed
34-district sample, under exactly the Amendment 7 gates and the rules of
findings/a7_stepb_calibration_protocol.md. It reuses the frozen scorer
a7_stepb_calibrate.py unchanged and substitutes only the procedure. It also
records version 3's own fit diagnostics for each district, which the frozen
scorer does not copy.

Environment: Python 3.12.13 with PyMuPDF 2.1 (findings/a9_stepb_v3_dev/environment.txt).
It refuses to run under another PyMuPDF version.

Usage: python analysis/scripts/a9_stepb_calibrate.py --out findings/a9_stepb_calibration.json
"""
import json
import os
import sys
from pathlib import Path

import pymupdf

if pymupdf.__version__ != "2.1":
    sys.exit(f"PyMuPDF {pymupdf.__version__}: the registered run needs PyMuPDF 2.1")

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ["STEPB_V3_CALIBRATION_RUN"] = "1"

import a9_stepb_reconstruct_v3 as V3  # noqa: E402

diagnostics = {}
_reconstruct = V3.reconstruct


def _recording(ed):
    V3.last_info = {}
    try:
        return _reconstruct(ed)
    finally:
        diagnostics[int(ed)] = {k: v for k, v in V3.last_info.items() if k != "layers"}


V3.reconstruct = _recording
sys.modules["a7_stepb_reconstruct"] = V3  # the frozen scorer imports the procedure by this name
import a7_stepb_calibrate as C  # noqa: E402

if __name__ == "__main__":
    C.main()
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    d = json.loads(out.read_text(encoding="utf-8"))
    d["procedure"] = "analysis/scripts/a9_stepb_reconstruct_v3.py (Amendment 9; scorer a7_stepb_calibrate.py, unchanged)"
    d["environment"] = {"python": sys.version.split()[0], "pymupdf": pymupdf.__version__}
    d["v3_diagnostics"] = {str(k): v for k, v in sorted(diagnostics.items())}
    out.write_text(json.dumps(d, indent=1, default=float), encoding="utf-8")
