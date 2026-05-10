"""
sentiment_config.py

Single source of truth for all sentiment analysis constants shared across:
  submission_sentiment_llm.py, submission_sentiment_llm_full.py,
  hansard_sentiment_llm.py, quote_verify_and_clean.py,
  validation_sample.py, compute_kappa.py, cross_reference_submitters.py

Dependencies:
  Forward:  (consumed by all sentiment scripts)
  Backward: analysis/utils/data_loader.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# ── Project paths ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent

try:
    _utils = str(ROOT / "analysis" / "utils")
    if _utils not in sys.path:
        sys.path.insert(0, _utils)
    import data_loader
    DATA_DIR = data_loader._resolve_path("data")
except Exception:
    DATA_DIR = ROOT / "data"

TEXT_DIR    = ROOT / ".temp" / "submissions" / "text"
OUTPUTS_DIR = DATA_DIR / "outputs"

# ── Configuration map — 7 boundary configurations under analysis ───────────────
CONFIGS: dict[str, str] = {
    "airdrie_4way_split":        "Airdrie 4-way split",
    "nolan_hill_cochrane":       "Calgary-Nolan Hill-Cochrane hybrid",
    "rmh_banff_park":            "Rocky Mountain House-Banff Park hybrid",
    "olds_three_hills_didsbury": "Olds-Three Hills-Didsbury extending to Airdrie",
    "chestermere_split":         "Chestermere merging with Calgary",
    "red_deer_hybrids":          "Red Deer hybrid ridings (Blackfalds, Sylvan Lake, Innisfail)",
    "st_albert_sturgeon":        "St. Albert merging with Sturgeon County",
}

# Ordered for output/schema consistency
CONFIG_KEYS: list[str] = list(CONFIGS.keys())

STANCE_ENUM: list[str] = [
    "Active Support",
    "Active Opposition",
    "Neutral/Contextual",
    "Unrelated",
]

# Keywords that trigger inclusion of a Hansard turn in classification
CONFIG_KEYWORDS: dict[str, list[str]] = {
    "airdrie_4way_split":        ["airdrie"],
    "nolan_hill_cochrane":       ["nolan hill", "cochrane"],
    "rmh_banff_park":            ["rocky mountain house", "banff"],
    "olds_three_hills_didsbury": ["olds", "three hills", "didsbury"],
    "chestermere_split":         ["chestermere"],
    "red_deer_hybrids":          ["blackfalds", "sylvan lake", "innisfail", "red deer"],
    "st_albert_sturgeon":        ["st. albert", "st albert", "sturgeon"],
}

# ── EBC Commission panel — complete roster; never community participants ────────
# Source: Hansard front matter, all sessions R1 and R2
COMMISSION_SPEAKERS: frozenset[str] = frozenset({
    "The Chair",
    "Chair",
    "Justice Miller",    # Dallas K. Miller — Chair
    "Mr. Clark",         # Greg Clark — Commissioner
    "Mr. Evans",         # John D. Evans KC — Commissioner
    "Dr. Martin",        # Julian Martin — Commissioner
    "Mrs. Samson",       # Susan Samson — Commissioner
    "Ms. Samson",
    "Mr. Roth",          # Aaron Roth — Administrator (support staff)
    "Ms. Dean",          # Shannon Dean KC — Clerk
    "Mr. Massolin",      # Philip Massolin — Clerk Assistant and Executive Director
})

# ── Standard output columns ────────────────────────────────────────────────────
OUTPUT_FIELDS: list[str] = [
    "submission_id",
    "configuration",
    "classification",
    "reasoning",
    "exact_quote",
    "quote_verified",
    "scan_type",
]

# ── Shared JSON schema: one object with 7 config keys ─────────────────────────
def build_json_schema() -> str:
    """Return JSON string of the 7-config schema used in all Claude calls."""
    per_config = {
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
        for key in CONFIG_KEYS
    }
    return json.dumps({
        "type": "object",
        "properties": per_config,
        "required": CONFIG_KEYS,
    })


JSON_SCHEMA: str = build_json_schema()
