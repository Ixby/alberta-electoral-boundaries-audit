---
name: Pre-registration amendment — 2026-04-23
description: Documents five changes made to v0_1_pre_registration_draft.md after the initial OSF upload (06:22 PM MT, 2026-04-23). Submitted alongside the updated file to provide a transparent change record.
type: project
---

# Pre-registration amendment — 2026-04-23

**Registration:** Pre-registered signature-detection checklist for the Alberta MLA Special Select Committee's 91-seat electoral boundary map.  
**Author:** Will Conner.  
**Original upload:** 2026-04-23, 06:22 PM MT.  
**This amendment filed:** 2026-04-23.  
**Reason for amendment:** Five corrections and additions identified after initial upload. No thresholds or hypotheses were altered. Changes 1–4 correct stale weight parameters that were not updated when the central urban-weight estimate was revised from 0.70 to 0.85 earlier in the analysis session. Change 5 adds a toolstack disclosure that should have been present at initial submission.

---

## Change 1 — §11 Indices, B2 formula: central weight and sensitivity range

**Location:** §11 Indices and derived variables, B2 — Efficiency gap (EG), final sentence.

**Before:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.70; sensitivity range 0.60–0.80).

**After:**
> For hybrid EDs, vote totals are estimated by blending the urban-core and rural-absorption portions at the specified urban weight (central estimate 0.85; sensitivity range 0.60–0.90).

**Reason:** The central urban-weight estimate was updated from 0.70 to 0.85 based on Calgary DA-level population density analysis conducted prior to registration. The sensitivity range was extended from 0.60–0.80 to 0.60–0.90 to cover the full parameter space tested in the analysis scripts. The initial upload retained the old values. This correction brings the pre-registration into alignment with the actual parameters used in `analysis/v0_2_packing_cracking_analysis.py` and reported in both audit reports.

---

## Change 2 — §9 Manipulated variables: sensitivity sweep values

**Location:** §9 Manipulated variables, second paragraph.

**Before:**
> The urban-weight parameter used in hybrid-district vote attribution (tested at 0.60, 0.70, and 0.80) is a modelling sensitivity parameter...

**After:**
> The urban-weight parameter used in hybrid-district vote attribution (tested at 0.60, 0.70, 0.80, 0.85, and 0.90) is a modelling sensitivity parameter...

**Reason:** Same as Change 1. The three-value list was carried forward from an earlier draft; the actual analysis tests five values. Corrected to match the scripts.

---

## Change 3 — §2 Study design, Component 2: parameter count and values

**Location:** §2 Study type, causal interpretation, and design — Component 2 paragraph.

**Before:**
> Sensitivity is tested across three urban-weight parameters (0.60, 0.70, 0.80) and three election cycles...

**After:**
> Sensitivity is tested across five urban-weight parameters (0.60, 0.70, 0.80, 0.85, 0.90) and three election cycles...

**Reason:** Same as Changes 1–2. Corrected to match actual analysis.

---

## Change 4 — §3 Pre-registered tests, S4: sensitivity range

**Location:** §3 Pre-registered tests, S4 — Efficiency gap crosses the US 7% threshold, threshold description.

**Before:**
> ...using the audit's pre-existing 85/15 urban/rural weighting (w=0.85, the central blending convention applied identically to both 2026 commission maps; sensitivity range 0.60–0.80 also reported)...

**After:**
> ...using the audit's pre-existing 85/15 urban/rural weighting (w=0.85, the central blending convention applied identically to both 2026 commission maps; sensitivity range 0.60–0.90 also reported)...

**Reason:** The sensitivity range stated here must match the range stated in the Indices section (Change 1). Corrected from 0.60–0.80 to 0.60–0.90 for consistency.

---

## Change 5 — §15 Context: declared toolstack added

**Location:** §15 Context and additional information — new paragraph appended after the Timeline entry.

**Added:**
> **Declared toolstack.** This audit was produced using the following tools: Python 3.11 (pandas, numpy, geopandas/pyogrio, shapely, pyproj, GerryChain 0.3.2, textstat, pdfplumber, rapidfuzz, osmnx); Elections Alberta GIS data; Statistics Canada DA shapefiles; pdfplumber for commission report extraction; and Claude (Anthropic), a large language model used as an analytical and writing assistant throughout the project. Claude's role included: drafting and revising report text, proposing analysis structure and section outlines, identifying consistency gaps between documents, and surfacing edge cases in the methodology (e.g., the Vote Anywhere apportionment issue and the pre-registration disclosure requirement). All substantive analytical claims — metric values, thresholds, data provenance, and code outputs — were verified against primary sources and script outputs by the author. Claude did not execute code or access external data independently; all script runs were performed by the author in a local Python environment. The use of an AI assistant is disclosed here and in both the public and academic reports in accordance with emerging norms for AI-assisted research.

**Reason:** AI use disclosure was omitted from the initial upload. Emerging norms for research involving large language model assistance (see e.g. Nature portfolio policies, 2023; ICMJE recommendations update, 2023) require disclosure of AI tools used in analysis and writing. The disclosure is additive — it documents what tools were used; it does not change any finding, threshold, or hypothesis.

---

## Summary

| # | Section | Nature | Effect on findings |
|---|---|---|---|
| 1 | §11 B2 formula | Correction — weight values | None; aligns text with scripts |
| 2 | §9 Manipulated variables | Correction — parameter list | None; aligns text with scripts |
| 3 | §2 Study design | Correction — parameter count and list | None; aligns text with scripts |
| 4 | §3 S4 threshold | Correction — sensitivity range | None; aligns text with §11 |
| 5 | §15 Toolstack | Addition — AI use disclosure | None; additive disclosure only |

No hypotheses, thresholds, research questions, scoring rules, or data inclusion/exclusion criteria were changed. The pre-registered 7% EG threshold (S4), the 10% zone-gap threshold (S1/RQ1), the four-division Airdrie threshold (S1/RQ2), and the p95 ensemble threshold (RQ5) are unchanged.
