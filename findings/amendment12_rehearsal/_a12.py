"""Shared setup for the Amendment 12 rehearsal wrappers (rehearsal, provisional, not a registered result).
Paths, the all-ballots VA file (SHA-256 checked), and a no-op for the audit logger."""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "findings" / "amendment12_rehearsal"
VA_ALL = ROOT / "data/shapefiles/derived/va_polygons_all_2023_ballots_primary.gpkg"
VA_ALL_SHA = "c9e21ac90fb97b9ee4a7e4da7c80d44922e5849842fc283344f724bb2711be72"
MAP = ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled.gpkg"
P1_ALL = 0.01394
S5_ALL = 0.0019398

for p in (ROOT / "analysis/scripts", ROOT / "analysis/utils", ROOT):
    sys.path.insert(0, str(p))


def check_va():
    h = hashlib.sha256(VA_ALL.read_bytes()).hexdigest()
    assert h == VA_ALL_SHA, f"all-ballots VA file changed: {h}"


def default_va_to_all_ballots():
    """Make mcmc_ensemble.build_va_graph default to the all-ballots file (its own va_path argument)."""
    check_va()
    import mcmc_ensemble as me
    orig = me.build_va_graph

    def patched(verbose=True, va_path=None):
        return orig(verbose=verbose, va_path=va_path if va_path is not None else VA_ALL)

    me.build_va_graph = patched
    return me


def noop_logger(mod):
    """The registered scripts append to data/outputs/script_run_audit.jsonl, an existing file; not touched here."""
    if hasattr(mod, "_log_run"):
        mod._log_run = lambda *a, **k: None
