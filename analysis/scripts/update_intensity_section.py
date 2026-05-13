"""
update_intensity_section.py

Updates §5.9.4.6 in report_academic.md with the finalized
intensity-weighted net sentiment table.

Replaces the placeholder note with the LLM-scored intensity-weighted
net rankings from intensity_summary_table.csv.

Backward:
  # REVIEW: verify inputs before publication
Forward:
  # REVIEW: verify outputs before publication
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SUMMARY_CSV = ROOT / "data" / "outputs" / "intensity_summary_table.csv"
REPORT_PATH = ROOT / "outputs" / "academic_report" / "report_academic.md"

def main():
    if not SUMMARY_CSV.exists():
        print(f"ERROR: {SUMMARY_CSV} not found. Run aggregate_sentiment_intensity.py first.")
        sys.exit(1)
    
    # Load the summary data
    rows = []
    with SUMMARY_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "config": row["configuration"],
                "weighted_net": int(row["weighted_net"]),
                "direction": row["direction"],
            })
    
    # Build markdown table
    table_lines = [
        "",
        "| Configuration | Intensity-weighted net | Direction |",
        "|---|---|---|",
    ]
    
    for row in rows:
        table_lines.append(f"| {row['config']} | {row['weighted_net']} | {row['direction']} |")
    
    table_md = "\n".join(table_lines) + "\n"
    
    # Read report
    with REPORT_PATH.open(encoding="utf-8") as f:
        report_text = f.read()
    
    # Find and replace the placeholder section
    old_note = (
        "*Note: the rule-based intensity proxy is not highly discriminating — 91% of active rows score at the middle tier (2) because "
        "the LLM's reasoning text uses standardized language (\"explicitly argues\") regardless of underlying passion. "
        "A second-pass LLM intensity scoring run (`sentiment_intensity_score.py`) is in progress; "
        "the weighted-net ranking above will be updated when it completes.*"
    )
    
    new_note = (
        "*Note: the LLM intensity scoring run completed with 459 active rows classified on a 1–3 scale. "
        "The weighted-net scores reflect the intensity-weighted balance (support_sum − opposition_sum) across all submissions, "
        "where intensity 1 = mentioned in passing, 2 = clear position among several substantive points, "
        "3 = primary focus or emphatic language. A configuration's direction is determined by whether support or opposition "
        "has the larger weighted sum.*"
    )
    
    if old_note in report_text:
        print(f"Found placeholder note. Updating...")
        
        # Replace the old table (if it exists) with new table
        # The old table is right before the note
        import re
        
        # Pattern: a markdown table followed by the old note
        pattern = (
            r"(\| Configuration \| Intensity-weighted net \| Direction \|\n"
            r"\|\-{3}\|\-{3}\|\-{3}\|.*?\n(?:\|.*?\|.*?\|.*?\|\n)*)"
        )
        
        replacement = table_md + "\n"
        updated_report = re.sub(pattern, replacement, report_text, flags=re.DOTALL)
        
        # Replace the note
        updated_report = updated_report.replace(old_note, new_note)
        
        # Write back
        with REPORT_PATH.open("w", encoding="utf-8") as f:
            f.write(updated_report)
        
        print(f"✓ Updated §5.9.4.6 with LLM-scored intensity-weighted net table")
        print(f"✓ Replaced placeholder note with completion message")
        print(f"✓ Changes written to {REPORT_PATH}")
    else:
        print("WARNING: Could not find placeholder note in report.")
        print("The section may have already been updated or the note text may have changed.")

if __name__ == "__main__":
    main()
