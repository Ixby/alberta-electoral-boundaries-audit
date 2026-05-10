"""
submission_sentiment_llm_full.py

Full-corpus scan: runs LLM classification over all 1,252 EBC submissions (not just
the keyword-flagged 70). One API call per submission classifies all 7 configurations
simultaneously. Returns "Unrelated" for configs not discussed; emits a row only for
non-Unrelated results, keeping output compatible with submission_sentiment_llm_results.csv.

This closes the keyword-gap critique: the claim that certain configurations had no public
support can now be grounded in every submission, not just keyword-flagged ones.

Usage:
    python analysis/scripts/submission_sentiment_llm_full.py

Output:
    data/outputs/submission_sentiment_llm_full_results.csv
        columns: submission_id, configuration, classification, reasoning, exact_quote,
                 quote_verified, scan_type
    data/outputs/submission_sentiment_llm_full_progress.csv
        running tally of completed submission IDs (enables resume)

Resume: re-running the script skips submissions already in the progress file.

Cost estimate: ~1,252 submissions × $0.13/call ≈ $163 USD at sonnet pricing.
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

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from data_loader import _resolve_path
DATA_DIR = _resolve_path("data")

TEXT_DIR    = ROOT / ".temp" / "submissions" / "text"
OUTPUT_CSV  = DATA_DIR / "outputs" / "submission_sentiment_llm_full_results.csv"
PROGRESS_CSV = DATA_DIR / "outputs" / "submission_sentiment_llm_full_progress.csv"

OUTPUT_FIELDS = [
    "submission_id", "configuration", "classification",
    "reasoning", "exact_quote", "quote_verified", "scan_type",
]

# ── Configuration map ─────────────────────────────────────────────────────────
CONFIGS = {
    "airdrie_4way_split":        "Airdrie 4-way split",
    "nolan_hill_cochrane":       "Calgary-Nolan Hill-Cochrane hybrid",
    "rmh_banff_park":            "Rocky Mountain House-Banff Park hybrid",
    "olds_three_hills_didsbury": "Olds-Three Hills-Didsbury extending to Airdrie",
    "chestermere_split":         "Chestermere merging with Calgary",
    "red_deer_hybrids":          "Red Deer hybrid ridings (Blackfalds, Sylvan Lake, Innisfail)",
    "st_albert_sturgeon":        "St. Albert merging with Sturgeon County",
}

STANCE_ENUM = ["Active Support", "Active Opposition", "Neutral/Contextual", "Unrelated"]

# ── Claude CLI path ───────────────────────────────────────────────────────────
def _resolve_claude() -> str:
    if sys.platform == "win32":
        npm_bin = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd"
        if npm_bin.exists():
            return str(npm_bin)
    return shutil.which("claude") or shutil.which("claude.cmd") or "claude"

CLAUDE_CMD = _resolve_claude()

# ── JSON schema: one object with 7 config keys ────────────────────────────────
_CONFIG_SCHEMA = {
    key: {
        "type": "object",
        "properties": {
            "classification": {
                "type": "string",
                "enum": STANCE_ENUM,
            },
            "reasoning": {
                "type": "string",
                "description": "One sentence. Empty string if Unrelated.",
            },
            "exact_quote": {
                "type": "string",
                "description": (
                    "Verbatim 10-40 word substring from the text proving the stance. "
                    "Empty string if Unrelated or Neutral/Contextual."
                ),
            },
        },
        "required": ["classification", "reasoning", "exact_quote"],
    }
    for key in CONFIGS
}

JSON_SCHEMA = json.dumps({
    "type": "object",
    "properties": _CONFIG_SCHEMA,
    "required": list(CONFIGS.keys()),
})

# ── Prompt ────────────────────────────────────────────────────────────────────
_CONFIG_LIST = "\n".join(
    f'  "{key}": {desc}' for key, desc in CONFIGS.items()
)

SYSTEM_PROMPT = f"""\
You are an objective forensic auditor reading community submissions to an Electoral \
Boundaries Commission. Classify the author's stance on each of the following 7 boundary \
configurations. Use "Unrelated" when the configuration is not discussed.

Configurations (JSON key: human description):
{_CONFIG_LIST}

Stance definitions:
- Active Support: author explicitly requests, endorses, or advocates for the configuration.
- Active Opposition: author explicitly opposes or argues against the configuration.
- Neutral/Contextual: author discusses the geographic area but takes no position.
- Unrelated: the configuration is not discussed at all.

Rules:
- exact_quote must be a verbatim substring copied character-for-character from the text.
- exact_quote must be empty string for Unrelated or Neutral/Contextual entries.
- reasoning must be one sentence; empty string for Unrelated entries.
- Output ONLY valid JSON matching the schema. No markdown, no conversational text.\
"""

# ── Quote verification ────────────────────────────────────────────────────────
def verify_quote(quote: str, source_text: str) -> str:
    if not quote:
        return "N/A"
    if quote in source_text:
        return "True"
    if " ".join(quote.split()) in " ".join(source_text.split()):
        return "True (Normalized)"
    return "False"

# ── Claude call ───────────────────────────────────────────────────────────────
def call_claude(text: str) -> dict:
    cmd = [
        CLAUDE_CMD,
        "--print",
        "--model", "sonnet",
        "--output-format", "json",
        "--json-schema", JSON_SCHEMA,
        "--no-session-persistence",
        SYSTEM_PROMPT,
    ]
    try:
        result = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
        )
        if result.returncode != 0:
            logger.warning("CLI error: %s", result.stderr[:200])
            return {}

        outer = json.loads(result.stdout)

        # --json-schema validated output lands in structured_output
        structured = outer.get("structured_output")
        if isinstance(structured, dict):
            return structured

        # Fallback: try result field
        inner = outer.get("result", "")
        if isinstance(inner, str) and inner.strip().startswith("{"):
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                pass

        return {}

    except subprocess.TimeoutExpired:
        logger.warning("Timeout on submission")
        return {}
    except Exception as e:
        logger.warning("Unexpected error: %s", e)
        return {}

# ── Resume: load already-completed IDs ───────────────────────────────────────
def load_completed() -> set[str]:
    if not PROGRESS_CSV.exists():
        return set()
    with PROGRESS_CSV.open(encoding="utf-8") as f:
        return {row["submission_id"] for row in csv.DictReader(f)}

# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    text_files = sorted(
        f for f in TEXT_DIR.glob("*.txt")
        if not f.stem.startswith("hansard_")
    )
    if not text_files:
        print(f"ERROR: no text files found in {TEXT_DIR}")
        sys.exit(1)

    completed = load_completed()
    pending = [f for f in text_files if f.stem not in completed]

    print(f"Corpus: {len(text_files)} submissions total")
    print(f"Already done: {len(completed)}")
    print(f"Remaining: {len(pending)}")
    print(f"Claude: {CLAUDE_CMD}")
    print()

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Open output in append mode so resume works
    out_mode = "w" if not OUTPUT_CSV.exists() else "a"
    out_fh = OUTPUT_CSV.open(out_mode, newline="", encoding="utf-8")
    out_writer = csv.DictWriter(out_fh, fieldnames=OUTPUT_FIELDS)
    if out_mode == "w":
        out_writer.writeheader()

    prog_mode = "w" if not PROGRESS_CSV.exists() else "a"
    prog_fh = PROGRESS_CSV.open(prog_mode, newline="", encoding="utf-8")
    prog_writer = csv.DictWriter(prog_fh, fieldnames=["submission_id", "timestamp", "rows_emitted"])
    if prog_mode == "w":
        prog_writer.writeheader()

    errors = 0
    total_rows = 0

    for i, tf in enumerate(pending):
        sub_id = tf.stem
        text = tf.read_text(encoding="utf-8", errors="replace")

        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{i+1}/{len(pending)}] {sub_id} ({len(text):,} chars)", end=" ... ", flush=True)

        result = call_claude(text)

        if not result:
            errors += 1
            print("ERROR")
        else:
            rows_emitted = 0
            for key, desc in CONFIGS.items():
                cfg_result = result.get(key, {})
                if not isinstance(cfg_result, dict):
                    continue
                classification = cfg_result.get("classification", "Unrelated")
                if classification == "Unrelated":
                    continue  # skip — only emit non-Unrelated rows
                quote = cfg_result.get("exact_quote", "")
                out_writer.writerow({
                    "submission_id":  sub_id,
                    "configuration":  desc,
                    "classification": classification,
                    "reasoning":      cfg_result.get("reasoning", ""),
                    "exact_quote":    quote,
                    "quote_verified": verify_quote(quote, text),
                    "scan_type":      "full_corpus",
                })
                rows_emitted += 1
                total_rows += 1

            print(f"{rows_emitted} non-Unrelated results")

        # Mark complete and flush
        prog_writer.writerow({
            "submission_id": sub_id,
            "timestamp": datetime.now().isoformat(),
            "rows_emitted": rows_emitted if result else 0,
        })
        out_fh.flush()
        prog_fh.flush()

        time.sleep(0.3)

    out_fh.close()
    prog_fh.close()

    print(f"\nDone. {len(pending)} submissions processed, {total_rows} non-Unrelated rows written.")
    if errors:
        print(f"  {errors} API errors — check progress CSV for gaps.")

    # Summary by configuration
    if OUTPUT_CSV.exists():
        from collections import Counter
        by_cfg: dict[str, Counter] = {}
        with OUTPUT_CSV.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("scan_type") != "full_corpus":
                    continue
                by_cfg.setdefault(row["configuration"], Counter())[row["classification"]] += 1

        if by_cfg:
            print("\n-- Full-corpus summary ----------------------------------------------------------")
            for cfg, counts in sorted(by_cfg.items()):
                print(
                    f"  {cfg[:60]:<60}  "
                    f"Support={counts.get('Active Support',0)}  "
                    f"Oppose={counts.get('Active Opposition',0)}  "
                    f"Neutral={counts.get('Neutral/Contextual',0)}"
                )


if __name__ == "__main__":
    main()
