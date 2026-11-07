"""w08: findings/a10_stepc/cut_va_sensitivity_stepc.py with mcmc_ensemble.build_va_graph defaulted to the all-ballots VA file.
Run with A10_STEPC=1, as filed. Rehearsal, provisional, not a registered result."""
import runpy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _a12  # noqa: E402

_a12.default_va_to_all_ballots()
sys.path.insert(0, str(_a12.ROOT / "findings/a10_dev"))
sys.argv[0] = str(_a12.ROOT / "findings/a10_stepc/cut_va_sensitivity_stepc.py")
runpy.run_path(sys.argv[0], run_name="__main__")
