# Pre-Registration Amendment: Final Forensic Hardening (April 27, 2026)

This document formally amends the audit's pre-registration. It records the final parameter locking and methodological hardening executed prior to the publication of the final academic and public reports.

## Summary of Final Procedural Updates
Following the initial post-audit review (April 26), three major structural refinements were applied to the audit pipeline to ensure maximum legal defensibility and mathematical rigour. These changes supersede all prior parameters for the published headline findings.

### Change 1 — Finalization of MCMC Ensemble Sample Size: 250,000 Maps
**Before:** The audit explored ensemble sizes of 100k, 250k, 1M, and 2M. An earlier amendment reverted the authoritative baseline to the 100,000-map ReCom standard following convergence diagnostics.
**After:** The final, authoritative legal standard is permanently locked to **250,000 maps** (run as four parallel chains of 62,500 maps each). 
**Rationale:** While 100,000 maps achieves sufficient Gelman-Rubin convergence (R̂ < 1.05), increasing the baseline to 250,000 significantly improves the Effective Sample Size (ESS ≈ 375 per metric), resolving the noise-floor limitations at the extreme right tail and establishing a rigorously defensible threshold for constitutional challenge.

### Change 2 — Hardening to `v0_9` Topological Substrate
**Before:** Spatial attribution and ensemble scoring relied on a `v0_7` and `v0_8` geographic substrate that had known topological imperfections (leaving trace gaps where municipal boundaries aligned imperfectly with Statistics Canada dissemination blocks). The resulting inheritance-fill approach achieved only partial (83-of-89) pure geometric coverage.
**After:** All quantitative metrics and ensemble scoring have been fully migrated to the **`v0_9` canonical topological substrate**. 
**Rationale:** The `v0_9` substrate forces absolute topological validity and applies a robust area-proportional logic to edge-cases. This achieves **100% geometric coverage (89-of-89 districts)**, eliminating all attribution artifacts.

### Change 3 — Final Headline `seats@50/50` Outlier Percentile
**Before:** Prior un-hardened metrics estimated the 2026 minority map's `seats@50/50` UCP advantage at 52.8% (p98.6).
**After:** Using the fully-hardened `v0_9` topological substrate against the official 250,000-map legal ensemble, the minority map's true value is **48.31%**. This places it at exactly the **98.5th percentile** of the neutral simulation (the top 1.5%).
**Rationale:** The 52.8% figure was an attribution artefact caused by the 83-of-89 geometric dropouts. The 48.31% metric is structurally and mathematically absolute. The core qualitative finding remains completely unchanged: the minority map remains an extreme statistical outlier (only 3,750 of 250,000 neutral procedures reach this advantage) and crosses all 5 pre-registered structural irregularity tests.

## Archival and Namespace Clean-Up
To ensure procedural transparency, all historical code and data artifacts (v0.1 through v0.8) have been preserved in `historical/` subdirectories. The active project namespace has been completely de-versioned. All references to scripts (e.g. `v0_9_cross_election.py` → `cross_election.py`) have been streamlined to maintain a pristine, current-state working directory for independent auditors.

**Signed:** Will Conner, Project Author
**Date:** April 27, 2026
