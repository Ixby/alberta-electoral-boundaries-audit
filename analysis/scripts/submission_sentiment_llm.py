"""
submission_sentiment_llm.py

Reads the submission_search_dataset.csv to find which submissions mentioned
specific configurations. Loads the full text for those submissions and runs
a zero-shot classification via the Claude Code CLI (claude --print) so that
no API key setup is required — authentication is handled by Claude Code.

Extracts a direct quote justifying the classification and cross-verifies that
the quote exists in the source text. This provides direct forensic evidence
to counter the "Ontological Gap" critique regarding community support.

Requirements:
  - Claude Code CLI installed and authenticated (claude --version should work)

Usage:
  python analysis/scripts/submission_sentiment_llm.py
"""

import csv
import json
import sys
import logging
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "utils"))
from sentiment_config import DATA_DIR, TEXT_DIR, CONFIGS
from quote_verifier import verify_quote
from claude_client import CLAUDE_CMD, call_claude

logger = logging.getLogger(__name__)

# ── Path setup ───────────────────────────────────────────────────────────────

INPUT_CSV  = DATA_DIR / "submission_search_dataset.csv"
OUTPUT_CSV = DATA_DIR / "submission_sentiment_llm_results.csv"

# ── Configuration columns → human descriptions ────────────────────────────────
# The search dataset uses column names prefixed with "mentions_"; map those to
# the shared CONFIGS descriptions using the shared key suffixes.
CONFIG_NAMES = {
    "mentions_airdrie_4way_split":        CONFIGS["airdrie_4way_split"],
    "mentions_nolan_hill_cochrane":        CONFIGS["nolan_hill_cochrane"],
    "mentions_rmh_banff_park":            CONFIGS["rmh_banff_park"],
    "mentions_olds_three_hills_didsbury":  CONFIGS["olds_three_hills_didsbury"],
    "mentions_chestermere_split":          CONFIGS["chestermere_split"],
    "mentions_red_deer_hybrids":           CONFIGS["red_deer_hybrids"],
    "mentions_st_albert_sturgeon":         CONFIGS["st_albert_sturgeon"],
}

# ── JSON schema enforced by Claude Code ──────────────────────────────────────
# This is the single-config schema (one classification per call), distinct from
# the shared 7-config JSON_SCHEMA in sentiment_config. Keep it local.
JSON_SCHEMA_LOCAL = json.dumps({
    "type": "object",
    "properties": {
        "classification": {
            "type": "string",
            "enum": ["Active Support", "Active Opposition", "Neutral/Contextual", "Unrelated"]
        },
        "reasoning": {
            "type": "string",
            "description": "One sentence explaining the classification."
        },
        "exact_quote": {
            "type": "string",
            "description": "A direct 10-40 word verbatim substring from the text proving the classification. Empty string if Unrelated."
        }
    },
    "required": ["classification", "reasoning", "exact_quote"]
})

SYSTEM_PROMPT = (
    "You are an objective forensic auditor reading community submissions submitted to "
    "an Electoral Boundaries Commission. You will be given the full text of a submission "
    "and asked to evaluate its stance on a specific proposed boundary configuration.\n\n"
    "Classification definitions:\n"
    "- Active Support: The author explicitly requests, endorses, or advocates for the "
    "specified boundary configuration or alignment.\n"
    "- Active Opposition: The author explicitly opposes, rejects, or argues against the "
    "specified boundary configuration.\n"
    "- Neutral/Contextual: The author discusses the geographic areas involved but does "
    "not advocate for or against the specific configuration.\n"
    "- Unrelated: The text does not discuss the configuration at all.\n\n"
    "CRITICAL: exact_quote must be a verbatim substring of the submission text — "
    "copy it exactly, character for character.\n\n"
    "OUTPUT FORMAT:\n"
    "You must output ONLY valid JSON matching the schema. Do not include any conversational text or markdown formatting."
)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} not found. Run submission_search.py first.")
        sys.exit(1)

    # Collect tasks from the keyword-hit dataset
    tasks = []
    with INPUT_CSV.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["submission_id"] == "__SUMMARY__":
                continue
            for col, desc in CONFIG_NAMES.items():
                if row.get(col, "False") == "True":
                    tasks.append({
                        "submission_id": row["submission_id"],
                        "config_col": col,
                        "config_desc": desc,
                    })

    print(f"Found {len(tasks)} configuration mentions to classify.")

    results = []
    errors  = 0

    for i, task in enumerate(tasks):
        sub_id    = task["submission_id"]
        text_file = TEXT_DIR / f"{sub_id}.txt"

        if not text_file.exists():
            print(f"  [{i+1}/{len(tasks)}] SKIP {sub_id} — text file missing")
            continue

        text = text_file.read_text(encoding="utf-8", errors="replace")

        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] [{i+1}/{len(tasks)}] {sub_id}  ->  {task['config_desc'][:55]}...")

        prompt_instruction = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Evaluate the author's stance on this boundary configuration: {task['config_desc']}"
        )
        r = call_claude(text, prompt_instruction, JSON_SCHEMA_LOCAL, timeout=120)

        if not r or r.get("classification") == "Error":
            errors += 1

        quote = r.get("exact_quote", "") if r else ""
        vr = verify_quote(quote, text)

        results.append({
            "submission_id":  sub_id,
            "configuration":  task["config_desc"],
            "classification": r.get("classification", "Unknown") if r else "Unknown",
            "reasoning":      r.get("reasoning", "") if r else "",
            "exact_quote":    vr.quote,
            "quote_verified": vr.status,
        })

        # Respect rate limits
        time.sleep(0.5)

        # Write results incrementally to avoid data loss on crash/interrupt
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        fields = ["submission_id", "configuration", "classification",
                  "reasoning", "exact_quote", "quote_verified"]
        with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()
            csv.DictWriter(f, fieldnames=fields).writerows(results)

    print(f"\nDone. {len(results)} rows written -> {OUTPUT_CSV}")
    if errors:
        print(f"  WARNING: {errors} API errors — review rows where classification='Error'")

    # Quick summary to stdout
    by_config: dict[str, Counter] = {}
    for r in results:
        by_config.setdefault(r["configuration"], Counter())[r["classification"]] += 1

    print("\n── Summary ──────────────────────────────────────────────────────────────")
    for cfg, counts in sorted(by_config.items()):
        sup = counts.get("Active Support", 0)
        opp = counts.get("Active Opposition", 0)
        neu = counts.get("Neutral/Contextual", 0)
        print(f"  {cfg[:60]:<60}  Support={sup}  Oppose={opp}  Neutral={neu}")


if __name__ == "__main__":
    main()
