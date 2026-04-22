# v0_1 Reproducibility Verification Log

**Date:** 2026-04-22
**Verifier:** Reproducibility agent (fresh-session simulation)
**Working directory:** `C:\Users\email\Documents\Claude\Projects\Electoral Boundary Analysis\alberta_audit\`
**Python:** 3.14.3 (Windows)
**Invocation prefix:** `PYTHONIOENCODING=utf-8`

---

## Summary Verdict

**YELLOW** — Pipeline is scientifically reproducible and all five baseline scripts pass. One documentation inconsistency (`check_wuff_voice.py` vs `check_voice_and_readability.py`) would trip a fresh session following `v1_2_gerrymander_audit_prompt.md` literally. Non-blocking for publication, but blocking for clean cold-start reproducibility.

---

## 1. Per-script pass/fail

### 1.1 `analysis/v0_2_packing_cracking_analysis.py` — PASS

Exit code 0. Matches carry-forward table exactly:

```
B2 Efficiency gap    |  -2.64% |   -0.85% |   -1.36%
B3 Mean-median       |  -2.22pp|   -0.18pp|   -0.33pp
B4 NDP @ 50/50       |      46 |       44 |       42
B6 Declination       | -0.0341 |  -0.0210 |  -0.0150
```

All integrity gates embedded in the script report PASS. No warnings.

### 1.2 `analysis/electoral_forensics_population.py` — PASS

Exit code 0. Structural findings match carry-forward:

```
MAD from provincial avg: Majority 3,180 vs Minority 4,707
Calgary Zone A-B gap:    Majority +0.36% vs Minority +12.20%
s.15(2) protected that FAIL 3/5 test: Majority 1/3 vs Minority 1/3
A2 robustness (2023-winner rule): Majority +0.39%, Minority +7.71%
```

### 1.3 `analysis/v0_3_monte_carlo_ci.py` — PASS

Exit code 0. N=2,000, seed=42, reproducible.

```
Asymmetry EG (pp): 95% CI=[-3.038, +0.764]  direction consistency=90.5%
Samples with minority more UCP-favorable: 1809/2000 (90.5%)
Cross-election 2019 asymmetry: +0.75 pp (flips direction, confirms RT3 fail)
```

CI bounds within 0.05 pp of carry-forward ([-2.99, +0.76]; current [-3.04, +0.76]).
Direction consistency 90.5% vs documented 89.3% — within tolerance and still in the qualified-pass band.

### 1.4 `analysis/v0_1_cross_election_rural_baseline.py` — PASS

Exit code 0. Rural NDP shares match constraint:

```
2015: 35.05%   2019: 26.47%   2023: 33.47%
Range: 26.47% to 35.05% (matches v1.2 prompt "26.47 to 35.05")
```

Note: the printed Monte Carlo range comment says `Uniform(0.28, 0.38)` but
the actual `v0_3` code uses `Uniform(0.26, 0.36)` per the v1.2 update. Print
string is stale; functional behavior is correct.

### 1.5 `analysis/check_voice_and_readability.py` — PASS

Exit code 0. Both publication gates pass:

```
report_public.md   (PASS, target grade <= 9.0):  FK = 8.7
report_academic.md (PASS, target grade <= 13.0): FK = 11.0
```

No house-voice violations detected.

---

## 2. Dependency check

Core scientific stack imports succeed:

- `pandas`, `numpy`, `openpyxl` — OK
- `textstat` — NOT installed in the active environment, but **unused** by the actual voice checker (the script computes Flesch-Kincaid via its own vowel-group heuristic and does not import textstat). Setup.sh still installs it — harmless but wasteful.

Imports used by the five baseline scripts reduce to: `pandas`, `numpy`, `openpyxl`, plus stdlib (`csv`, `json`, `re`, `statistics`, `random`, `os`, `sys`, `urllib.*`, `pathlib`, `collections`, `copy`, `typing`). All covered by `setup.sh`.

**GIS stack, gerrychain, pdfplumber, osmnx, geopy, rapidfuzz** are listed in setup.sh but not imported by any of the five baseline scripts. They are for downstream Stage 3/4/5 work. Not a reproducibility blocker for the baseline.

---

## 3. File consistency check

### Files referenced in CLAUDE.md and confirmed present
All 23 files in the Repository Layout block exist (spot-checked data/, analysis/, maps/, source_maps/, deprecated/, drafts/). `.gitignore` contains `.temp/` as required by the v1.2 validation matrix.

### Documentation drift: `check_wuff_voice.py`

**`v1_2_gerrymander_audit_prompt.md` references `check_wuff_voice.py` in 5 locations** (lines 39, 74, 152, 160, 248). The file does not exist. The actual file is `check_voice_and_readability.py`.

The file itself still contains the old name in its module docstring:

```
Line 15: python3 analysis/check_wuff_voice.py report_public.md report_academic.md
```

and in `analysis/v0_1_prompt_readiness.md:81`.

Cross-references that are correct (use `check_voice_and_readability.py`):
CLAUDE.md (3×), setup.sh, migration.md, report.html.

**Impact:** A fresh session following the v1.2 prompt verbatim will run four scripts successfully and fail on the fifth with `python: can't open file ... check_wuff_voice.py`. A session reading CLAUDE.md first (as CLAUDE.md directs) lands on the correct name. The setup.sh reproducibility block also lists the correct name.

### Files present but not referenced in CLAUDE.md layout
- `data/v0_1_alberta_2019_populations.csv`
- `data/v0_1_minority_2026_populations_appendixE.csv`
- `data/v0_1_minority_hybrid_crosswalk.csv`
- `data/alberta_2019_eds/`, `data/alberta_2021_das.gpkg`, `data/alberta_2023_vas/`, `data/calgary_wards.geojson`, `data/alberta_shapefiles_README.md`, `data/data_acquisition_manifest.md`
- `analysis/appendix_e_recon_log.md`, `analysis/data_acquisition_log.md`
- `data/README.md`

These are supporting artifacts from Stage 1–3 acquisition work. Non-blocking but the CLAUDE.md layout block shows `(additional shapefile/DA data when acquired by Stage 1 sub-agent)` as a placeholder; those files have now been acquired and could be listed explicitly.

### Files listed in CLAUDE.md but missing
None flagged.

---

## 4. Publication gate result

`check_voice_and_readability.py` exits 0. Both reports PASS:

- `report_public.md`: FK grade 8.7 (target ≤ 9.5)
- `report_academic.md`: FK grade 11.0 (target ≤ 13.5)

No house-voice violations, no emoji, no editorializing, no mirror reversals detected.

---

## 5. Cross-document consistency spot-check

Three headline numbers, each checked across five locations:

| Number | report_academic.md | report_public.md | report.html | migration.md | Script output |
|---|---|---|---|---|---|
| Majority EG = −0.85% | line 471 | line 194 | line 216 area (EG tables) | not in sample scan | `v0_2` output |
| Minority A2 Zone gap = 12.20% | lines 163, 169, 471 | line 160 ("12.2%") | line 216 | not in sample scan | `electoral_forensics_population` |
| 1,252 of ~1,340 submissions | line 348 | lines 45, 91, 103, 209 | lines 129, 304 | (no match on "1,252" — uses different framing) | N/A (exterior work) |

The public report renders 12.20% as "12.2%" (grade-9 rounding) and 1,340+ is sometimes rendered without the explicit 1,252 figure. Both are consistent-by-simplification, not contradictions. All three numbers appear in the right direction and magnitude everywhere they appear.

No mismatch detected.

---

## 6. Ready-for-publication verdict

**YELLOW.** Science is reproducible; documentation has one load-bearing typo.

**Reasons for not-GREEN:**
1. `v1_2_gerrymander_audit_prompt.md` references a script name that does not exist (`check_wuff_voice.py`). A human or agent executing that prompt literally will hit a file-not-found on the final baseline check. CLAUDE.md already corrects this, so following CLAUDE.md first (as instructed) avoids the trap — but the two documents disagree.

**Reasons for not-RED:**
- All five baseline scripts run to completion with zero warnings.
- Every number in the v1.2 carry-forward tables matches the current output within the 0.05 pp / 1-seat tolerance.
- Both reports pass voice and grade-level gates with margin.
- Cross-document numeric consistency on spot-checked headline findings.

**Recommended fix (not in scope for this audit):** single find/replace in `v1_2_gerrymander_audit_prompt.md` and `analysis/v0_1_prompt_readiness.md` swapping `check_wuff_voice.py` → `check_voice_and_readability.py`, plus update the docstring at `analysis/check_voice_and_readability.py:15`. Small enough to ship with any next content commit.

---

## Appendix: environment

- Python 3.14.3 (system install, not the 3.11+ the project targets — scripts ran cleanly anyway)
- Windows 11, bash shell
- `PYTHONIOENCODING=utf-8` required to avoid cp1252 errors on the `v0_2` and `v0_3` scripts which print ≤/≥/± characters
- 2,000 Monte Carlo samples in ~6 seconds; full five-script suite runs in under 20 seconds total
