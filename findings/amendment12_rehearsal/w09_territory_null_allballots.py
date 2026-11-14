"""w09: Amendment 12, Part 2 replay of the territory null, all-ballots form. WRITTEN FOR THE OFFICIAL RUN; NOT LAUNCHED IN THE REHEARSAL.
territory_null.py has no --va-file; its only vote-bearing call is me.build_va_graph(verbose=False), and the sampler reads no votes.
This wrapper defaults that call to the all-ballots VA file and runs the module's own main(), so a replay is literal.
Usage (from ../wt-a8, detached by WMI + pythonw, like the filed run):
  PY w09_territory_null_allballots.py --idx N --enacted <map.gpkg> --stated-low K --out DIR   [--steps 100000 --thin 250]"""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
A8 = ROOT.parent / "wt-a8"
VA_ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
# same substrate check as _a12.check_va / w07 (inline: importing _a12 would put wt-osf's modules ahead of wt-a8's)
assert hashlib.sha256(VA_ALL.read_bytes()).hexdigest() == "c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72",     "all-ballots VA file changed"
sys.path.insert(0, str(A8 / "analysis/utils"))
sys.path.insert(0, str(A8 / "analysis/scripts"))
import mcmc_ensemble as me  # noqa: E402

_orig = me.build_va_graph
me.build_va_graph = lambda verbose=True, va_path=None: _orig(verbose=verbose, va_path=va_path if va_path is not None else VA_ALL)
import territory_null as tn  # noqa: E402

tn.main()
