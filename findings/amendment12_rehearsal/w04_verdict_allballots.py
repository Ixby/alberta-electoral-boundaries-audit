"""w04: verdict_synthesis.main with P1_EG_THRESHOLD = 0.01394 (Amendment 12, Part 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402
import verdict_synthesis as v  # noqa: E402

v.P1_EG_THRESHOLD = _a12.P1_ALL
sys.exit(v.main(["--structural", str(_a12.OUT / "structural_allballots.json"),
                 "--joint", str(_a12.OUT / "joint_outlier_allballots.json"),
                 "--output", str(_a12.OUT / "verdict_allballots.json")]))
