"""
_perf_utils.py — shared observability helpers for the audit pipeline.

Two utilities, both intentionally minimal:

    ts() -> str
        Wall-clock HH:MM:SS string for prefixing log lines.

    Timer(label, *, note="")
        Context manager. On enter, prints `[HH:MM:SS] {label} start`.
        On exit, prints `[HH:MM:SS] {label} done in X.Xs[ — {note}]`.
        The `note` attribute can be mutated inside the with-block to
        attach a context-specific summary that the exit message will
        append (e.g. "67 pairs resolved", "16955 gaps assigned").

Usage:

    from _perf_utils import Timer, ts

    with Timer(f"[{label}] Phase 1") as t:
        result = do_work()
        t.note = f"{result.count} items processed"

To make this importable from sibling scripts in the same directory,
each consumer adds:

    HERE = Path(__file__).resolve().parent
    sys.path.insert(0, str(HERE))
    from _perf_utils import Timer, ts

This keeps the helper opt-in: scripts that don't import it are
unaffected and the pre-existing inline `_ts()` lambdas continue to work.

Forward:  any analysis script that wants consistent observability
Backward: stdlib only (time)
"""
from __future__ import annotations

import time


def ts() -> str:
    """Wall-clock HH:MM:SS for log prefixes."""
    return time.strftime("%H:%M:%S")


class Timer:
    """Context manager that logs start + done-with-elapsed.

    The `note` attribute (string) can be set inside the with-block to
    append a context-specific summary to the done line.
    """

    __slots__ = ("label", "note", "_t0")

    def __init__(self, label: str, *, note: str = ""):
        self.label = label
        self.note = note
        self._t0 = 0.0

    def __enter__(self):
        self._t0 = time.time()
        print(f"[{ts()}] {self.label} start", flush=True)
        return self

    def __exit__(self, *exc) -> None:
        elapsed = time.time() - self._t0
        suffix = f" — {self.note}" if self.note else ""
        print(f"[{ts()}] {self.label} done in {elapsed:.1f}s{suffix}", flush=True)
