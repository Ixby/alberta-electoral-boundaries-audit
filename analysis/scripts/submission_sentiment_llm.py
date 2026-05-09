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
import subprocess
import sys
import logging
import time
from datetime import datetime
from pathlib import Path

# ── Path setup ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)

try:
    sys.path.insert(0, str(ROOT / "analysis" / "utils"))
    import data_loader
    DATA_DIR = data_loader._resolve_path("data")
except Exception as e:
    logger.warning("data_loader unavailable, falling back to ROOT/data: %s", e)
    DATA_DIR = ROOT / "data"

TEXT_DIR  = ROOT / ".temp" / "submissions" / "text"
INPUT_CSV = DATA_DIR / "submission_search_dataset.csv"
OUTPUT_CSV = DATA_DIR / "submission_sentiment_llm_results.csv"

# ── Configuration columns → human descriptions ────────────────────────────────
CONFIG_NAMES = {
    "mentions_airdrie_4way_split":        "Airdrie 4-way split",
    "mentions_nolan_hill_cochrane":        "Calgary-Nolan Hill-Cochrane hybrid",
    "mentions_rmh_banff_park":            "Rocky Mountain House-Banff Park hybrid",
    "mentions_olds_three_hills_didsbury":  "Olds-Three Hills-Didsbury extending to Airdrie",
    "mentions_chestermere_split":          "Chestermere merging with Calgary",
    "mentions_red_deer_hybrids":           "Red Deer hybrid ridings (Blackfalds, Sylvan Lake, Innisfail)",
    "mentions_st_albert_sturgeon":         "St. Albert merging with Sturgeon County",
}

# ── JSON schema enforced by Claude Code ──────────────────────────────────────
JSON_SCHEMA = json.dumps({
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

# ── Claude Code CLI call ──────────────────────────────────────────────────────
def call_claude(text: str, config_desc: str) -> dict:
    prompt_instruction = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Evaluate the author's stance on this boundary configuration: {config_desc}"
    )

    cmd = [
        "claude",
        "--print",
        "--model", "sonnet",
        "--output-format", "json",
        "--json-schema", JSON_SCHEMA,
        "--no-session-persistence",
        prompt_instruction,
    ]

    try:
        result = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
        if result.returncode != 0:
            print(f"  CLI error: {result.stderr[:200]}")
            return {"classification": "Error", "reasoning": result.stderr[:100], "exact_quote": ""}

        try:
            import re
            outer = json.loads(result.stdout)
            inner = outer.get("result") or outer.get("text") or outer
            
            if isinstance(inner, str):
                # Try to extract JSON from a markdown block if present
                match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', inner, re.DOTALL)
                if match:
                    inner = match.group(1)
                
                try:
                    inner = json.loads(inner)
                except json.JSONDecodeError:
                    # Fallback to regex extraction if Claude completely ignored JSON format
                    c_match = re.search(r'(Active Support|Active Opposition|Neutral/Contextual|Unrelated)', inner, re.IGNORECASE)
                    c = c_match.group(1) if c_match else "Unknown"
                    # Map back to exact enum casing
                    c_map = {
                        "active support": "Active Support",
                        "active opposition": "Active Opposition",
                        "neutral/contextual": "Neutral/Contextual",
                        "unrelated": "Unrelated"
                    }
                    c_final = c_map.get(c.lower(), "Unknown")
                    return {"classification": c_final, "reasoning": inner[:200].strip(), "exact_quote": ""}
            
            if not isinstance(inner, dict):
                inner = {}
            return inner
            
        except json.JSONDecodeError:
            print(f"  JSON decode error. Raw output: {result.stdout[:200]}")
            return {"classification": "Error", "reasoning": "JSON decode error", "exact_quote": ""}

    except subprocess.TimeoutExpired:
        return {"classification": "Error", "reasoning": "Timeout", "exact_quote": ""}
    except Exception as e:
        print(f"  Unexpected error: {e}")
        return {"classification": "Error", "reasoning": str(e)[:100], "exact_quote": ""}


# ── Quote verification ────────────────────────────────────────────────────────
def verify_quote(quote: str, source_text: str) -> str:
    if not quote:
        return "N/A"
    if quote in source_text:
        return "True"
    # Allow for normalised whitespace (PDF extraction can insert newlines)
    if " ".join(quote.split()) in " ".join(source_text.split()):
        return "True (Normalized)"
    return "False"


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
        r = call_claude(text, task["config_desc"])

        if r.get("classification") == "Error":
            errors += 1

        quote = r.get("exact_quote", "")
        results.append({
            "submission_id":  sub_id,
            "configuration":  task["config_desc"],
            "classification": r.get("classification", "Unknown"),
            "reasoning":      r.get("reasoning", ""),
            "exact_quote":    quote,
            "quote_verified": verify_quote(quote, text),
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
        print(f"  ⚠  {errors} API errors — review rows where classification='Error'")

    # Quick summary to stdout
    from collections import Counter
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
