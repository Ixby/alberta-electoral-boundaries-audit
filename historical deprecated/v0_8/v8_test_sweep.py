"""
v0_1_v8_test_sweep.py

Run the full v0_8 test suite in parallel via subprocess.Popen, so eight
independent scripts saturate cores instead of running one-at-a-time.

Each test script writes its own outputs (CSVs, JSONs, MD reports) to its
canonical path; this wrapper just orchestrates the parallel launch and
streams a per-script summary line as each finishes.

Order of completion is non-deterministic. Failures of one script do not
abort the others — failures are reported in the final summary table.

Run:
    PYTHONIOENCODING=utf-8 python alberta_audit/analysis/scripts/v0_1_v8_test_sweep.py

Dependencies:
  Forward:  individual test scripts (v0_1_compactness_metrics.py,
            v0_1_extended_partisan_metrics.py, etc.)
  Backward: this wrapper does not produce its own data artefacts; it is
            an orchestrator.
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

# Each tuple: (script_filename, args, label, est_minutes)
# Ordered by decreasing expected wall time so the slowest start first
# (LPT scheduling — minimises total wall-clock for given concurrency).
TESTS = [
    ("v0_1_extended_partisan_metrics.py", [], "Extended partisan metrics", 5),
    ("v0_1_gerrymetrics_comparison.py", [], "Gerrymetrics comparison", 4),
    ("v0_1_compactness_metrics.py", [], "Compactness metrics", 3),
    ("v0_1_v8_alignment_proof.py", [], "v0_8 alignment proof", 2),
    ("v0_1_v8_overlap_diagnostic.py", [], "v0_8 overlap diagnostic", 1),
    ("v0_1_contiguity_check.py", [], "Contiguity check", 1),
    ("v0_1_majority_symmetry_counter_test.py", [], "Symmetry counter test", 1),
    ("v0_1_justification_tests.py", [], "Justification tests", 1),
]


def run_one(script: str, args: list[str], label: str) -> dict:
    cmd = [sys.executable, str(HERE / script)] + args
    t0 = time.time()
    print(f"  ▶ START   {label:<30s}  ({script})", flush=True)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"},
            cwd=ROOT,
        )
        elapsed = time.time() - t0
        if result.returncode == 0:
            print(f"  ✓ DONE    {label:<30s}  ({elapsed:.0f}s)", flush=True)
            return {
                "label": label,
                "script": script,
                "ok": True,
                "elapsed": elapsed,
                "stdout_tail": result.stdout[-400:],
            }
        else:
            print(
                f"  ✗ FAILED  {label:<30s}  exit={result.returncode}  ({elapsed:.0f}s)",
                flush=True,
            )
            return {
                "label": label,
                "script": script,
                "ok": False,
                "elapsed": elapsed,
                "exit_code": result.returncode,
                "stderr_tail": result.stderr[-400:],
            }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        print(f"  ⏰ TIMEOUT {label:<30s}  ({elapsed:.0f}s)", flush=True)
        return {
            "label": label,
            "script": script,
            "ok": False,
            "elapsed": elapsed,
            "exit_code": "timeout",
        }
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  ! ERROR   {label:<30s}  {e}", flush=True)
        return {
            "label": label,
            "script": script,
            "ok": False,
            "elapsed": elapsed,
            "exit_code": str(e),
        }


def main() -> int:
    n_workers = min(8, len(TESTS), os.cpu_count() or 4)
    print(
        f"[v0_8 test sweep] launching {len(TESTS)} test scripts with "
        f"{n_workers} parallel workers",
        flush=True,
    )
    print(f"  scripts directory: {HERE}", flush=True)
    print(f"  working directory: {ROOT}", flush=True)
    t_start = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=n_workers) as ex:
        futures = {ex.submit(run_one, s, a, l): (s, l) for s, a, l, _ in TESTS}
        for f in as_completed(futures):
            results.append(f.result())

    print(
        f"\n[v0_8 test sweep] all {len(results)} scripts complete in "
        f"{time.time()-t_start:.0f}s",
        flush=True,
    )
    print("\n=== SUMMARY ===")
    print(f"  {'STATUS':<10}{'ELAPSED':<10}LABEL")
    print(f"  {'-'*10}{'-'*10}{'-'*30}")
    for r in sorted(results, key=lambda x: -x["elapsed"]):
        status = "✓ pass" if r["ok"] else "✗ fail"
        print(f"  {status:<10}{r['elapsed']:>6.0f}s  {r['label']}")

    failures = [r for r in results if not r["ok"]]
    if failures:
        print(f"\n  {len(failures)} script(s) failed — full stderr tails:")
        for r in failures:
            print(f"\n  --- {r['label']} ({r['script']}) ---")
            tail = r.get("stderr_tail") or r.get("exit_code") or ""
            print(f"    exit={r.get('exit_code')}")
            for line in str(tail).splitlines()[-10:]:
                print(f"    {line}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
