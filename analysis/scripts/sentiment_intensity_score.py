"""
sentiment_intensity_score.py

Second-pass LLM scoring: adds an intensity (1-3) field to each already-classified
Active Opposition / Active Support row in submission_sentiment_llm_full_results.csv.

Intensity scale:
  1 = Mentioned in passing; one clause among many unrelated points
  2 = Clear position taken; one of several substantive points in the text
  3 = Primary focus or emphatic; the configuration dominates the passage or the
      language is notably strong (demands, urges, calls it unacceptable, etc.)

One API call per row (passes the exact_quote + reasoning already extracted).
Skips Neutral/Contextual and Unrelated rows. Resumes from progress file.

Output:
    data/outputs/sentiment_intensity_scores.csv
        columns: row_key, submission_id, configuration, scan_type,
                 classification, intensity, intensity_reasoning
    data/outputs/sentiment_intensity_progress.csv
        running tally of completed row_keys

Usage:
    python analysis/scripts/sentiment_intensity_score.py [--dry-run]

Cost estimate: ~459 active rows × $0.03/call ≈ $14 USD at sonnet pricing.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import sys
import logging
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = ROOT / "data"

INPUT_CSV    = DATA_DIR / "outputs" / "submission_sentiment_llm_full_results.csv"
OUTPUT_CSV   = DATA_DIR / "outputs" / "sentiment_intensity_scores.csv"
PROGRESS_CSV = DATA_DIR / "outputs" / "sentiment_intensity_progress.csv"

OUTPUT_FIELDS = [
    "row_key", "submission_id", "configuration", "scan_type",
    "classification", "intensity", "intensity_reasoning",
]

INTENSITY_ENUM = [1, 2, 3]

JSON_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "intensity": {
            "type": "integer",
            "enum": INTENSITY_ENUM,
            "description": (
                "1 = mentioned in passing; "
                "2 = clear position, one of several substantive points; "
                "3 = primary focus or emphatically stated"
            ),
        },
        "intensity_reasoning": {
            "type": "string",
            "description": "One sentence explaining why this intensity level was chosen.",
        },
    },
    "required": ["intensity", "intensity_reasoning"],
})

SYSTEM_PROMPT = """\
You are scoring the INTENSITY of a stated position in a community submission to an \
Electoral Boundaries Commission. You are given:
  - classification: the stance already determined (Active Support or Active Opposition)
  - exact_quote: a verbatim excerpt proving the stance
  - reasoning: a one-sentence summary of why that stance was assigned

Score intensity on this scale:
  1 = Mentioned in passing. The configuration appears as a brief aside or single clause \
among many unrelated topics. Language is mild or indirect.
  2 = Clear position taken. The commenter explicitly states their view and gives at least \
one reason. This is one substantive point among several in the passage.
  3 = Primary focus or emphatic. The configuration is the dominant subject of the passage, \
OR the language is notably strong: demands, urges, calls it unacceptable/outrageous, \
devotes most of the text to it, repeats the concern multiple times.

Output ONLY valid JSON. No markdown, no explanation outside the JSON.\
"""




def _resolve_claude() -> str:
    if sys.platform == "win32":
        npm_bin = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd"
        if npm_bin.exists():
            return str(npm_bin)
    return shutil.which("claude") or shutil.which("claude.cmd") or "claude"


CLAUDE_CMD = _resolve_claude()


def call_claude(prompt_text: str) -> dict:
    # Embed system prompt in user message
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt_text}"

    cmd = [
        CLAUDE_CMD,
        "--print",
        "--model", "haiku",
        "--output-format", "json",
        "--json-schema", JSON_SCHEMA,
        "--no-session-persistence",
    ]
    try:
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60,
        )
        if result.returncode != 0:
            logger.warning("CLI error: %s", result.stderr[:200])
            return {}
        raw = result.stdout.strip()
        if not raw:
            return {}
        parsed = json.loads(raw)
        # Claude CLI returns structured output in the structured_output field
        if isinstance(parsed, dict) and "structured_output" in parsed:
            return parsed["structured_output"]
        # Fallback for older format or non-schema responses
        if isinstance(parsed, dict) and "result" in parsed:
            inner = parsed["result"]
            if isinstance(inner, str):
                # Result may be wrapped in markdown code blocks
                inner = inner.strip()
                if inner.startswith("```json"):
                    inner = inner[7:]  # Remove ```json
                if inner.startswith("```"):
                    inner = inner[3:]  # Remove ```
                if inner.endswith("```"):
                    inner = inner[:-3]  # Remove trailing ```
                inner = inner.strip()
                if inner:
                    return json.loads(inner)
            return inner
        return parsed
    except json.JSONDecodeError as e:
        logger.warning("JSON parse error: %s (raw: %s)", e, raw[:200] if 'raw' in locals() else "")
        return {}
    except Exception as e:
        logger.warning("call_claude error: %s", e)
        return {}


def load_completed() -> set[str]:
    if not PROGRESS_CSV.exists():
        return set()
    completed = set()
    with PROGRESS_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "row_key" not in reader.fieldnames:
            # File exists but has no proper header; treat as empty
            return set()
        for row in reader:
            if row.get("row_key"):
                completed.add(row["row_key"])
    return completed


def make_row_key(row: dict) -> str:
    return f"{row['submission_id']}|{row['configuration']}|{row['scan_type']}"


def main(dry_run: bool = False) -> None:
    if not INPUT_CSV.exists():
        print(f"ERROR: input file not found: {INPUT_CSV}")
        sys.exit(1)

    rows = []
    with INPUT_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("classification") in ("Active Opposition", "Active Support"):
                rows.append(r)

    print(f"Active rows to score: {len(rows)}")

    completed = load_completed()
    todo = [r for r in rows if make_row_key(r) not in completed]
    print(f"Already scored: {len(completed)}  Remaining: {len(todo)}")

    if dry_run:
        print("\n[dry-run] Sample prompts (first 3):")
        for r in todo[:3]:
            prompt = _build_prompt(r)
            print(f"  [{make_row_key(r)}]")
            print(f"  {prompt[:200]}")
            print()
        return

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_mode = "a" if OUTPUT_CSV.exists() else "w"
    out_fh = OUTPUT_CSV.open(out_mode, newline="", encoding="utf-8")
    out_writer = csv.DictWriter(out_fh, fieldnames=OUTPUT_FIELDS)
    if out_mode == "w":
        out_writer.writeheader()

    prog_mode = "a" if PROGRESS_CSV.exists() else "w"
    prog_fh = PROGRESS_CSV.open(prog_mode, newline="", encoding="utf-8")
    prog_writer = csv.DictWriter(prog_fh, fieldnames=["row_key", "timestamp"])
    if prog_mode == "w":
        prog_writer.writeheader()

    errors = 0
    for i, row in enumerate(todo):
        key = make_row_key(row)
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{i+1}/{len(todo)}] {key[:70]}", end=" ... ", flush=True)

        prompt = _build_prompt(row)
        result = call_claude(prompt)

        if not result or "intensity" not in result:
            errors += 1
            print("ERROR")
            time.sleep(2)
            continue

        intensity = int(result["intensity"])
        out_writer.writerow({
            "row_key":             key,
            "submission_id":       row["submission_id"],
            "configuration":       row["configuration"],
            "scan_type":           row["scan_type"],
            "classification":      row["classification"],
            "intensity":           intensity,
            "intensity_reasoning": result.get("intensity_reasoning", ""),
        })
        out_fh.flush()

        prog_writer.writerow({
            "row_key":   key,
            "timestamp": datetime.now().isoformat(),
        })
        prog_fh.flush()

        print(f"intensity={intensity}")

    out_fh.close()
    prog_fh.close()
    print(f"\nDone. {len(todo) - errors} scored, {errors} errors.")

    if OUTPUT_CSV.exists():
        _print_summary()


def _build_prompt(row: dict) -> str:
    return (
        f"classification: {row['classification']}\n"
        f"exact_quote: {row.get('exact_quote','').strip()}\n"
        f"reasoning: {row.get('reasoning','').strip()}"
    )


def _print_summary() -> None:
    import collections
    rows = []
    with OUTPUT_CSV.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    valid = [r for r in rows if r.get("intensity")]
    null_count = len(rows) - len(valid)
    print(f"\n=== Intensity summary ({len(rows)} rows, {null_count} null skipped) ===")
    by_intensity: dict = collections.Counter(int(r["intensity"]) for r in valid)
    for k in sorted(by_intensity):
        print(f"  intensity={k}: {by_intensity[k]}")
    print()
    by_config: dict = collections.defaultdict(lambda: {"n": 0, "sum": 0, "opp": 0, "sup": 0})
    for r in valid:
        cfg = r["configuration"]
        intensity = int(r["intensity"])
        by_config[cfg]["n"] += 1
        by_config[cfg]["sum"] += intensity
        if r["classification"] == "Active Opposition":
            by_config[cfg]["opp"] += intensity
        else:
            by_config[cfg]["sup"] += intensity
    print(f"{'Configuration':<55} {'n':>4} {'mean':>5} {'net_w':>6}")
    for cfg, d in sorted(by_config.items(), key=lambda x: x[1]["opp"]-x[1]["sup"], reverse=True):
        mean = d["sum"] / d["n"]
        net  = d["sup"] - d["opp"]
        print(f"{cfg:<55} {d['n']:>4} {mean:>5.2f} {net:>6}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
