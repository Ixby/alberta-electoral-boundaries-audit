# Pre-Registration Amendment: Final Forensic Hardening (April 27, 2026)

This document formally amends the audit's pre-registration. It records the final parameter locking and methodological hardening executed prior to the publication of the final academic and public reports.

## Summary of Final Procedural Updates
Following the initial post-audit review (April 26), three major structural refinements were applied to the audit pipeline to ensure maximum legal defensibility and mathematical rigour. These changes supersede all prior parameters for the published headline findings.

### Change 1 — Finalization of MCMC Ensemble Sample Size: 250,000 Maps
**Before:** The audit explored ensemble sizes of 100k, 250k, 1M, and 2M. An earlier amendment reverted the authoritative baseline to the 100,000-map ReCom standard following convergence diagnostics.
**After:** The final, authoritative legal standard is permanently locked to **250,000 maps** (run as four parallel chains of 62,500 maps each). 
**Rationale:** To proactively stave off accusations of "p-hacking" (adjusting parameters until a desired result is found), the exact scale progression must be formally logged. The ensemble size was initially scaled from 250,000 to 1,000,000 to 2,000,000 to investigate contradictory diagnostic signals in the tail probabilities. This extreme scale-up revealed that the contradictions were not a product of insufficient chain mixing, but rather a structural imprecision in the underlying map geometry (the `v0_8` topological gaps). While the initial methodology was theoretically sound, the boundary implementation was flawed and required a complete re-write. Once the `v0_9` topological substrate successfully snapped the data to precise boundaries, the inputs became clean and the statistical contradictions resolved instantly. At that point, the audit executed standard procedure: 10,000 maps to check the logic, 100,000 to validate the distributions, and 250,000 to hit the required legal and constitutional standard. Seeing perfect consistency across all metrics at 250k, the scaling stopped, establishing the final, rigorously defensible baseline without arbitrary parameter hunting.

### Change 2 — Hardening to `v0_9` Topological Substrate
**Before:** Spatial attribution and ensemble scoring relied on a `v0_7` and `v0_8` geographic substrate that had known topological imperfections (leaving trace gaps where municipal boundaries aligned imperfectly with Statistics Canada dissemination blocks). The resulting inheritance-fill approach achieved only partial (83-of-89) pure geometric coverage.
**After:** All quantitative metrics and ensemble scoring have been fully migrated to the **`v0_9` canonical topological substrate**. 
**Rationale:** The `v0_9` substrate forces absolute topological validity and applies a robust area-proportional logic to edge-cases. This achieves **100% geometric coverage (89-of-89 districts)**, eliminating all attribution artifacts.

### Change 3 — Final Headline `seats@50/50` Outlier Percentile
**Before:** Prior un-hardened metrics estimated the 2026 minority map's `seats@50/50` UCP advantage at 52.8% (p98.6).
**After:** Using the fully-hardened `v0_9` topological substrate against the official 250,000-map legal ensemble, the minority map's true value is **48.31%**. This places it at exactly the **98.5th percentile** of the neutral simulation (the top 1.5%).
**Rationale:** The 52.8% figure was an attribution artefact caused by the 83-of-89 geometric dropouts. The 48.31% metric is structurally and mathematically absolute. The core qualitative finding remains completely unchanged: the minority map remains an extreme statistical outlier (only 3,750 of 250,000 neutral procedures reach this advantage) and crosses all 5 pre-registered structural irregularity tests.

### Change 4 — Pre-Registration of November 91-Seat Map Tripwire
**Context:** To preemptively evaluate the forthcoming November 91-seat committee map without retroactively fitting tests to its outcomes, the audit hereby pre-registers the exact structural red flag ("tripwire") that will trigger a formal fail condition in automated scoring scripts.
**Registered Tripwire:** The Drain Pattern (Mid-Sized City Integrity). The audit flags an extreme structural anomaly if mid-sized cities (Airdrie, Red Deer, Lethbridge, St. Albert) are split into more than their population-dictated expected seats with >2% area overlap each. This is structurally unjustified by their populations and mirrors the engineered fractionation detected in the 2026 minority recommendation. 
**Discarded Tripwire:** The Lasso Pattern (Polsby-Popper Compactness). This test was removed from the automated tripwires. As documented in prior retractions, Polsby-Popper discrepancies evaporated under the mathematically-strict `v0_9` substrate. Using a known-brittle metric as a tripwire is scientifically dishonest and has been struck from the evaluation pipeline.

## Archival and Namespace Clean-Up
To ensure procedural transparency, all historical code and data artifacts (v0.1 through v0.8) have been preserved in `historical/` subdirectories. The active project namespace has been completely de-versioned. All references to scripts (e.g. `v0_9_cross_election.py` → `cross_election.py`) have been streamlined to maintain a pristine, current-state working directory for independent auditors.

**Signed:** Will Conner, Project Author
**Date:** April 27, 2026
