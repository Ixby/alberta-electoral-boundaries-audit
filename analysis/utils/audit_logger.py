"""audit_logger.py — Append-only script run audit log.

All analysis scripts call log_run() at the end of their main() to record
what they produced and whether the run succeeded.  Creates an auditable
trail without changing any existing output flows.

Log file: data/outputs/script_run_audit.jsonl  (newline-delimited JSON)
Each entry:
  {"ts": "2026-05-14T…Z", "script": "name.py", "outputs": ["path", …],
   "elapsed_s": N.N, "status": "success"|"error", "errors": []}

Non-blocking: all I/O is wrapped in try/except — a logging failure never
raises to the caller and never breaks a script run.

Usage in any analysis script::

    import time
    from audit_logger import log_run
    t0 = time.time()
    # ... do work ...
    log_run(__file__, [str(OUT_CSV), str(OUT_JSON)], time.time() - t0)

Forward:
  data/outputs/script_run_audit.jsonl
Backward:
  (none — utility module, no file inputs)
"""
from __future__ import annotations

import datetime
import json
import os
import sys
from pathlib import Path

try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import data_loader

_LOG_PATH: Path | None = None


def _log_path() -> Path:
    global _LOG_PATH
    if _LOG_PATH is None:
        _LOG_PATH = data_loader._resolve_path("data") / "outputs" / "script_run_audit.jsonl"
        try:
            _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
    return _LOG_PATH


def log_run(
    script: str | Path,
    outputs: list[str | Path],
    elapsed_s: float,
    status: str = "success",
    errors: list[str] | None = None,
) -> None:
    """Append one audit record to the shared run log.  Never raises."""
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "script": Path(script).name,
        "outputs": [str(p) for p in outputs],
        "elapsed_s": round(float(elapsed_s), 2),
        "status": status,
        "errors": errors or [],
    }
    try:
        line = json.dumps(entry, ensure_ascii=False) + "\n"
        with open(_log_path(), "a", encoding="utf-8") as fh:
            fh.write(line)
    except Exception:
        pass
