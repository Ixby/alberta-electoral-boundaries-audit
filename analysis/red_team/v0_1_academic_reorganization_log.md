# Academic paper reorganization — log

**Date:** 2026-04-23
**Target file:** `report_academic.md`
**Original length:** 1,060 lines; 181,391 chars post-reorg (1,120 lines).
**Gate status:** house-voice PASS; Flesch-Kincaid grade 12.9 (textstat), target ≤ 13.0 — **PASS**. Pre-reorg baseline grade was also 12.9.

## What changed

The paper moved from the v0.1 ad-hoc structure (title, misplaced "Tools Used" and "Stress-Test Preamble" before the abstract, 11 body sections with parallel A/B/C/D/4/5 track labels, math formalism mid-paper, data provenance buried as §6) to a standard IMRAD-adjacent academic paper structure: Abstract → Author Disclosure → Introduction → Background and Prior Work → Data → Methods → Results → Discussion → Limitations and Falsifiability → Conclusion → References → Appendices A–F.

No substantive prose was cut. New prose was written for the Introduction (absorbing the old Stress-Test Preamble and the "Defensible synthesis" paragraph), the Background and Prior Work section (brief literature synthesis using already-cited works), the Data section (consolidating FROZEN_MANIFEST anchors plus the "Note on population-data provenance" summary), the §4 Methods opening paragraph, the §5 Results opening paragraph, the §6 Discussion opening paragraph, and the §8 Conclusion. Every number, citation, table, and argument from the original paper appears in the new structure; only the surrounding section labels were renumbered.

## Before / after section mapping

| Old section | Old label | New location | New label |
|---|---|---|---|
| Pre-abstract "Tools Used" | (out-of-band) | Author disclosure block | merged + acknowledgements |
| Pre-abstract "Stress-Test Preamble" | (out-of-band) | §1 Introduction | body |
| Abstract | ## Abstract | Abstract | unchanged |
| §1 Methodology and Integrity Framework | ## 1. | §4 Methods | |
| §1.1 Symmetry requirement | ### 1.1 | §4.1.1 | |
| §1.2 Falsifiability gates | ### 1.2 | §4.1.2 | |
| §1.3 What does not enter | ### 1.3 | §4.1.3 | |
| §1.4 Author disclosure | ### 1.4 | Author disclosure | (front-matter, pre-§1) |
| §2 Population Equality (Section A) | ## 2. | §5.1 | Population equality |
| §2.1 Distribution variance (A1) | ### 2.1 | §5.1.1 | |
| §2.2 Calgary geographic-zone (A2) | ### 2.2 | §5.1.2 | |
| §2.3 Urban–rural (A2b) | ### 2.3 | §5.1.3 | |
| §2.4 s.15(2) eligibility (A3) | ### 2.4 | §5.1.4 | |
| §3 Partisan Bias Metrics (Section B) | ## 3. | §5.2 | Partisan bias |
| §3.1 Methodology | ### 3.1 | §4.2 (vote-attribution pipeline) | |
| §3.2 Tests | ### 3.2 | §4.3 (test battery) | |
| §3.3 Results | ### 3.3 | §5.2.1 | Results |
| §3.4 Sensitivity (G5) | ### 3.4 | §5.2.2 | |
| §3.5 Falsifiability gate: asymmetry direction | ### 3.5 | §5.2.3 | |
| §3.5.1 Cross-metric weighting | ### 3.5.1 | §5.2.4 | |
| §3.6 Natural-packing context | ### 3.6 | §5.2.5 | |
| §3.7 Packing signatures | ### 3.7 | §5.3.1 | |
| §3.8 Cracking signatures | ### 3.8 | §5.3.2 | |
| §3.9 Engineered-boundary signatures | ### 3.9 | §5.3.3 | |
| §3.10 Signatures summary | ### 3.10 | §5.3.4 | |
| §3.11 MCMC neutral-ensemble baseline | ### 3.11 | §5.4 | |
| §3.12 Pre-registered checklist | ### 3.12 | §5.5 | |
| §3.13 Symmetry-of-test-selection | ### 3.13 | §5.6 | |
| §3.14 Stress-test grades mini-audit | ### 3.14 | §5.7 | |
| §4 Geographic Coherence (Section C) | ## 4. | §5.8 | Geographic coherence |
| §4.1 Visual spatial audit | ### 4.1 | §5.8.1 | |
| §4.2 Chair-flagged boundaries (C3) | ### 4.2 | §5.8.2 | |
| §4.3 Majority hybrids symmetric check | ### 4.3 | §5.8.3 | |
| §4.4 Community-of-interest splits (C4) | ### 4.4 | §5.8.4 | |
| §5 Procedural Audit (Section D) | ## 5. | §5.9 | Procedural findings |
| §5.1 Commission operation | ### 5.1 | §5.9.1 | |
| §5.2 April 16, 2026 government action | ### 5.2 | §5.9.2 | |
| §5.3 Comparator cases | ### 5.3 | §5.9.3 | |
| §5.4 Public submission record (D2) | ### 5.4 | §5.9.4 | |
| §5.4.1 through §5.4.5 | #### | §5.9.4.1 through §5.9.4.5 (5-deep) | |
| §5.5 Constitutional backdrop | ### 5.5 | §5.9.5 | |
| §6 Geometric Data Provenance (Section 4) | ## 6. | Appendix E | moved |
| §6.1 4A (direct shapefiles) | ### 6.1 | § E.1 | |
| §6.2 4B (DA dissolve) | ### 6.2 | § E.2 | |
| §6.3 4C (VA-polygon attribution) | ### 6.3 | § E.3 | |
| §6.4 4D/4E | ### 6.4 | § E.4 | |
| §6.5 4F validation | ### 6.5 | § E.5 | |
| §6.6 Technical Data Statement | ### 6.6 | § E.6 | |
| §6.7 Approximate 2026 geometry | ### 6.7 | § E.7 | |
| §7 Synthesis — Six-Dimensional Finding | ## 7. | §6 Discussion | |
| §8 Mathematical Formalism | ## 8. | Appendix D | moved |
| §8.1 Efficiency Gap | ### 8.1 | § D.1 | |
| §8.2 Mean-Median Gap | ### 8.2 | § D.2 | |
| §8.3 Polsby-Popper | ### 8.3 | § D.3 | |
| §8.4 Reock | ### 8.4 | § D.4 | |
| §9 Missing Evidence and Scope Limits | ## 9. | §7.1 | |
| §10 Falsifiability Statement | ## 10. | §7.2 | |
| §11 Legal Interpretive Note | ## 11. | Appendix F | moved |
| Note on population-data provenance | (unnumbered) | § E.8 | moved + summarised at §3.3 |
| Appendix C (2021-census baseline) | ## Appendix C | Appendix C | unchanged |
| Appendix A (Reproducibility) | ## Appendix A | Appendix A | unchanged |
| Appendix B (Section Documents) | ## Appendix B | Appendix B — Supporting Analysis Documents | renamed |
| References | ## References | References | unchanged |

## Content moved to appendices

| Source in v0.1 | Destination |
|---|---|
| §6 Geometric Data Provenance (+ sub-sections) | Appendix E with E.1–E.7 headings |
| §8 Mathematical Formalism (+ 8.1–8.4) | Appendix D with D.1–D.4 headings |
| §11 Legal Interpretive Note | Appendix F (unchanged prose) |
| "Note on population-data provenance and cycle-lag robustness" (unnumbered block at L863–L879 of v0.1) | § E.8 (with cycle-lag headline summarised at §3.3) |

## New prose (only)

- §1 Introduction opener (context paragraphs + three-question framing): ~220 words NEW; drew the three stress-test numbered paragraphs and the "Defensible synthesis" paragraph verbatim from the v0.1 "Stress-Test Preamble".
- §1 Contribution + Scope closers: ~300 words NEW.
- §2 Background and Prior Work: ~680 words NEW; all citations already present in v0.1 References.
- §3 Data: ~450 words NEW (primary-sources table derived from v0.1's pre-abstract "Tools Used" block, coverage-caveats and cycle-lag subsections synthesised from v0.1 §6.1, §5.5, and the "Note on population-data provenance" block).
- §4 Methods opening paragraph: ~80 words NEW (transitional).
- §4.5 What this audit does not claim: ~130 words NEW.
- §5 Results opening paragraph: ~170 words NEW (TOC + pointer to reorganization log).
- §5.1–§5.9 sub-section headers: NEW wrappers around unchanged v0.1 prose.
- §6 Discussion opening paragraph: ~45 words NEW.
- §8 Conclusion: ~480 words NEW.
- Author disclosure block opening + acknowledgements paragraph: v0.1 §1.4 prose preserved + a new acknowledgements paragraph that folds in the v0.1 pre-abstract "Tools Used" block content.

Every other word of prose in the reorganized file is v0.1 prose with its heading renumbered.

## Cross-references updated

### Inside `report_academic.md`

All v0.1 §-references were rewritten systematically:

- `§1.1` (Symmetry requirement) → `§4.1.1`
- `§2.1` / `§2.4` → `§5.1.1` / `§5.1.4`
- `§3.3` / `§3.4` / `§3.5` / `§3.5.1` / `§3.6` / `§3.7` / `§3.8` / `§3.9` / `§3.10` / `§3.11` / `§3.12` / `§3.13` / `§3.14` → `§5.2.1` / `§5.2.2` / `§5.2.3` / `§5.2.4` / `§5.2.5` / `§5.3.1` / `§5.3.2` / `§5.3.3` / `§5.3.4` / `§5.4` / `§5.5` / `§5.6` / `§5.7`
- `§4.3` / `§4.4` → `§5.8.3` / `§5.8.4`
- `§5.2` / `§5.4` (old procedural) → `§5.9.2` / `§5.9.4`
- `§A`, `§A1`, `§A2`, `§A2b`, `§A3` → `§5.1`, `§5.1.1`, `§5.1.2`, `§5.1.3`, `§5.1.4`
- `§B`, `§B2`, `§B3`, `§B4` → `§5.2`, `§5.2.1`, `§5.2.1`, `§5.2.1`
- `§C`, `§C3`, `§C4` → `§5.8`, `§5.8.2`, `§5.8.4`
- `§D` → `§5.9`
- `§6` (geometric provenance) → `Appendix E` (or `§ E.1`–`§ E.7`)
- `§7.4` → `§7.2` (Falsifiability Statement in the Limitations section)

Three rounds of substitution were needed because the automated pass over the prose produced cascading false positives when a substring like `§5.2` appeared inside a replacement target. Eleven cases (mostly inside the new Introduction block) were fixed surgically after the automated pass.

### Inside `analysis/red_team/` files

The red-team files are historical critiques written against v0.1 with specific L-number references (e.g., "ACA-01 L92, L243, L794, L840"). Those L-numbers are embedded in the critiques' evidence chains and updating them would require re-running the red-team passes, not a mechanical rewrite. The red-team §-references describe where findings sit in the critiqued document; they are historical artifacts of that pass rather than living documentation. Left unchanged by this reorganization; a future red-team pass against the reorganized paper will produce fresh L-numbers and fresh §-references tied to the new structure.

## Voice + readability gate

```
$ python3 analysis/check_voice_and_readability.py report_academic.md
report_academic.md (PASS, target grade <= 13.0):
  [info] Flesch-Kincaid Grade: 12.9  [method=textstat]
```

Both the house-voice rules (no "not X — Y" mirror reversals, no templated triads, no emoji, no editorialising reactions) and the FK ≤ 13.0 target pass.

## Edits summary

- **Sections renumbered or moved:** 37 (14 top-level headings, 23 sub-headings).
- **New prose blocks written:** 9 (Introduction, Background, Data, Methods opener + §4.5, Results opener, Discussion opener, Conclusion, Author-disclosure opener + acknowledgements).
- **Cross-references updated:** ~45 distinct old→new mappings, applied across ~180 occurrences inside the paper.
- **Total edits touching the source file:** 1 complete rewrite via `scripts/tmp_reorganize.py` (removed after run) + 17 surgical Edit-tool fixes for cascading-substitution residues and two appendix-level renumbering details.

## Content cut for coherence

None. Every table, code block, citation, and prose paragraph of v0.1 appears in the reorganized paper. The "Tools Used in the Academic Analysis" block that sat between the title and the abstract was absorbed into the Author Disclosure + Acknowledgements block and the §3 Data section's primary-sources table; its individual bullet points were preserved in the acknowledgements paragraph.
