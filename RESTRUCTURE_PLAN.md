# Restructure Plan — Alberta Audit Repository

*Planning document. Delete after execution is complete.*
*Drafted 2026-05-13. Grounded 2026-05-13 (all file paths verified). Status: APPROVED — not yet executed.*

---

## Principles

1. **Every directory name is a sentence fragment** that tells a reader what kind of thing is inside.
2. **Every file name is self-describing** without opening the file: concept first, document type last.
3. **No internal codes as identifiers**: `s15_2_`, `ch1_`, `tier_c_`, `v0_1_`, `phase4c_`, `red_team_` all belong to the working process, not the published research.
4. **Script output files keep their current names** — scripts reference these by exact path. Only human-written docs get renamed.
5. **All code must execute and output to the same locations after restructure.**

---

## Naming Convention

```
concept_description.md          ← human-readable analysis or methodology doc
concept_description.csv/.json   ← script output (name frozen; scripts write here)
```

---

## Target Root Structure

```
alberta_audit/
│
├── README.md
├── CONTRIBUTING.md
├── TODO.md
├── TREE.md
├── config.yaml
├── pyproject.toml
├── requirements.txt
├── run_audit.py
├── run_master_qa.py
│
├── preregistration/        ← "what we committed to before testing"
├── data/                   ← "the evidence" (unchanged internally)
├── analysis/               ← "how we tested it"
├── findings/               ← "what the tests found"  [was: analysis/reports/]
├── reports/                ← "what we published"     [was: outputs/]
├── tests/                  ← "automated verification"
└── archive/                ← "historical record"
    └── dpg/
```

---

## Tier 1 — Structure (no code changes)

### New: `preregistration/` at root

Move from `analysis/methodology/`:

| Old name | New name | Note |
|---|---|---|
| `null_hypothesis_and_exoneration_criteria.md` | `null_hypotheses.md` | |
| `threshold_provenance.md` | `thresholds.md` | |
| `preregistration_salt_audit_trail.md` | `seed_commitments.md` | |
| `issue14_seed_commitment.md` | `seed_issue14.md` | |
| `robustness_rerun_seed_commitment.md` | `seed_robustness_rerun.md` | |
| `retraction_pathway.md` | `retraction_conditions.md` | |
| `terms_of_reference_verbatim.md` | `terms_of_reference.md` | |

---

### New: `archive/provisional_geometries/` at root

`git mv dpg archive/provisional_geometries`

"DPG" is internal jargon. "provisional_geometries" is the plain-English expansion:
boundary tracings made from PDF thumbnails before official shapefiles arrived.
An external auditor reading the directory name should immediately understand what is inside.
DPG-era version prefixes within the directory are appropriate (they are part of the historical record).

Also move into `archive/provisional_geometries/` from `analysis/methodology/`:

- `mcmc_100k_and_full_coverage.md` → `archive/provisional_geometries/mcmc_100k_and_full_coverage.md`
  Documents the DPG-era 100k MCMC run with full-crosswalk fallback details; crosswalk configuration exists nowhere else. Archive, do not delete.

**Archive README** — Write `archive/README.md` on execution day noting:
- Date of restructure
- What `provisional_geometries/` contains and why it is archived (not deprecated)
- Logic delta: DPG files used different sign conventions and polygon provenance than canonical-era analysis; any DPG-era metric deviates from current findings by the margin documented in `provisional_geometries/analysis/dpg_perturbation_consolidated.md`

---

### `analysis/red_team/` → `analysis/review/`

`git mv analysis/red_team analysis/review`

File renames within `analysis/review/`:

| Old name | New name |
|---|---|
| `red_team_assertions.md` | `assertions.md` |
| `red_team_code.md` | `code_review.md` |
| `red_team_code_fixes.md` | `code_fixes_deferred.md` |
| `red_team_conclusions.md` | `conclusions.md` |
| `red_team_latent_bias.md` | `latent_bias.md` |
| `science_red_team_framework.md` | `science_review_framework.md` |
| `science_red_team_design_and_stats.md` | `science_review_design_stats.md` |
| `science_red_team_data_priorart_peerreview.md` | `science_review_data_literature.md` |
| `science_red_team_reproducibility_and_falsifiability.md` | `science_review_reproducibility.md` |
| `legal_red_team_framework.md` | `legal_review_framework.md` |
| `legal_red_team_report_academic.md` | `legal_review_academic_report.md` |
| `legal_red_team_report_public.md` | `legal_review_public_report.md` |
| `legal_red_team_data_artifacts.md` | `legal_review_data_artifacts.md` |
| `legal_red_team_scripts.md` | `legal_review_scripts.md` |
| `external_code_audit_findings_gemini_2026-04-26.md` | `external_audit_gemini.md` |
| `external_code_audit_findings_meridian.md` | `external_audit_meridian.md` |
| `peer_review_canadian.md` | unchanged |
| `peer_review_legal.md` | unchanged |
| `peer_review_methods.md` | unchanged |
| `editor_synthesis.md` | unchanged |
| `design_critique.md` | unchanged |
| `public_report_editor_writer_critique.md` | `public_report_critique.md` |
| `quote_verification_log.md` | unchanged |

Remove from `analysis/review/` (process artifacts):

- `academic_reorganization_log.md`
- `archival_submission_queue.md`

---

### `analysis/methodology/` — flatten core, two subdirs for support material

Test design and defense docs stay at `methodology/` root — they are the core of this
directory and should be immediately visible. Only `provenance/` and `reference/` move
to subdirs (genuinely distinct content types). Remove ~30 process artifacts.

**`analysis/methodology/` root — test design docs** (renamed where needed)

| Old name | New name |
|---|---|
| `szat_methodology.md` | unchanged |
| `mcmc_ensemble.md` | unchanged |
| `test_selection_rationale.md` | unchanged |
| `sign_convention_resolution.md` | unchanged |
| `s15_2_reaudit.md` | `population_deviation_reaudit.md` |
| `ch1_comp_intermap_permutation.md` | `intermap_permutation_design.md` |
| `drain_v2_plan.md` | `neighbour_drain_design.md` |

**`analysis/methodology/` root — defense docs**

`test_apparatus_defense.md`, `warrington_declination_defense.md`, and
`urban_weight_defense.md` are **consolidated into `methodological_defenses.md`**
as named sections — they are anticipated objections to methodology choices, which
is exactly what that file is for. Do not keep them as standalone files.

**Internal link breakage (grounded 2026-05-13):** The following files reference the
three source docs with section-level pointers. All must be updated during merge:

| File | Reference | Action |
|---|---|---|
| `outputs/academic_report/report_academic.md` (×5) | `test_apparatus_defense.md §2.5`, bare paths at lines 559, 694, 2393, 2396, 2397 | Update links; use `methodological_defenses.md#test-apparatus-defense` etc. |
| `README.md` | `test_apparatus_defense.md` (hyperlink) | Update to `analysis/methodology/methodological_defenses.md#test-apparatus-defense` |
| `analysis/methodology/null_hypothesis_and_exoneration_criteria.md` | `test_apparatus_defense.md §1.3` | Update to anchor in consolidated file |
| `analysis/scripts/dependency_graph_build.py` | `test_apparatus_defense.md section 3` (docstring only) | Update docstring |

**Merge requirement:** When writing each section into `methodological_defenses.md`,
add a heading that produces the correct anchor, e.g.:

```markdown
## Test Apparatus Defense {#test-apparatus-defense}
## Warrington Declination Defense {#warrington-declination-defense}
## Urban Weight Defense {#urban-weight-defense}
```

`attribution_sensitivity_robustness.md` moves to `provenance/` — it is about data
handling, not test design.

| Old name | New name | Action |
|---|---|---|
| `plain_language_defense.md` | unchanged | keep standalone |
| `methodological_defenses.md` | unchanged | absorbs 3 files below |
| `test_apparatus_defense.md` | — | merge into methodological_defenses.md |
| `warrington_declination_defense.md` | — | merge into methodological_defenses.md |
| `urban_weight_defense.md` | — | merge into methodological_defenses.md |
| `fisher_combination_defense.md` | unchanged | keep standalone — specific statistical argument, cited directly |
| `uncertainty_and_shapefile_impact.md` | `shapefile_uncertainty_analysis.md` | keep standalone |
| `novel_contributions.md` | unchanged | keep standalone |

**`analysis/methodology/` root — script-written files (cannot move)**

- `fisher_independence_defense.md` ← `validate_fisher_independence.py` appends results
- `audit_dependency_graph.json` ← `dependency_graph_build.py` reads/writes
- `audit_dependency_graph.dot` ← `dependency_graph_render.py` reads/writes
- `submission_search_log.md` ← `submission_search.py` writes here
- `audit_dependency_graph_readme.md` ← companion to the above; keep with them

**`analysis/methodology/provenance/`** — data chain of custody

| Old name | New name |
|---|---|
| `canonical_shapefile_log.md` | `shapefile_changelog.md` |
| `commission_source_provenance.md` | `source_document_provenance.md` |
| `shapefile_redteam_report.md` | `shapefile_audit.md` |
| `boundary_transcription.md` | unchanged |
| `canonical_shapefile_methodology.md` | `shapefile_integration_method.md` |
| `attribution_sensitivity_robustness.md` | `vote_attribution_provenance.md` |

**`analysis/methodology/reference/`** — literature, law, geographic facts

| Old name | New name |
|---|---|
| `academic_literature_review.md` | unchanged |
| `appendix_c_legal_baseline.md` | `legal_baseline.md` |
| `airdrie_quadrant_demographic_comparison.md` | unchanged |
| `banff_extension_population_check.md` | unchanged |
| `lethbridge_federal_boundary_check.md` | unchanged |
| `red_deer_sylvan_lake_school_age_magnitude.md` | unchanged |
| `st_albert_sturgeon_constraint_search.md` | unchanged |
| `cochrane_journey_to_work.md` | unchanged |
| `school_division_coherence.md` | unchanged |
| `csd_community_splits.md` | unchanged |
| `chen_rodden_alberta_validation.md` | unchanged |
| `external_tool_validation_plan.md` | `external_tool_validation.md` |
| `external_code_audit_brief.md` | `external_code_audit_scope.md` |
| `minority_rationales_inventory.md` | unchanged |
| `minority_rationales_validation.md` | unchanged |
| `338canada_historical.md` | `polling_data_338canada_historical.md` |
| `338canada_integration.md` | `polling_data_338canada_integration.md` |
| `338canada_riding_level.md` | `polling_data_338canada_riding_level.md` |
| `alberta_government_databases_survey.md` | unchanged |
| `codex_citation_verification_findings.md` | `citation_verification.md` |
| `changedetection_setup.md` | unchanged |

**Remove from `analysis/methodology/`** (process/planning artifacts — 10 files confirmed to exist):

- `assignment_execution_log.md`
- `assignment_runbook.md`
- `restructure_inventory.md`
- `scripts_inventory.md`
- `master_plan.md`
- `build_overlay_figures.md`
- `overlay_figures_v2.md`
- `shape_refinement.md`
- `composite_shapefiles_log.md`
- `self_check_protocol.md`

*(Note: `mcmc_100k_and_full_coverage.md` moves to `archive/dpg/` — see above. `pre_registration_platform_analysis.md` does not exist.)*

---

### `analysis/methodology/` README update

Rewrite `analysis/methodology/README.md` to serve as a navigation index for the four subdirectories plus the three root-level files scripts write to.

---

## Tier 2 — Renames requiring script path updates

### `analysis/reports/` → `findings/` at root

`git mv analysis/reports findings`

**Implementation approach: route through `config.yaml`, not a bulk string replace.**

Rather than replacing the hardcoded path constant in 9 scripts, add a key to `config.yaml`
and update `data_loader.py` to expose it. This means future directory renames require
one edit in one file, not 9 script edits.

```yaml
# config.yaml — add under paths:
paths:
  findings_dir: findings    # was analysis/reports
```

```python
# data_loader.py — add accessor (alongside existing CONFIG dict):
FINDINGS = ROOT / CONFIG["paths"]["findings_dir"]
```

```python
# Each affected script — replace hardcoded constant:
# Before
REPORTS = ROOT / "analysis" / "reports"

# After
from analysis.scripts.utils.data_loader import FINDINGS as REPORTS
```

The `REPORTS` alias preserves all downstream references within each script unchanged.

Affected scripts (9 total — grounded 2026-05-13):

| Script | Variable name |
|---|---|
| `intermap_permutation_test.py` | `REPORTS` |
| `joint_outlier_score_canonical.py` | `REPORTS` |
| `joint_outlier_score.py` | `REPORTS` |
| `population_consistency.py` | `REPORTS` |
| `szat_2019_baseline.py` | `REPORTS` |
| `szat_validate.py` | `REPORTS` |
| `szat.py` | `REPORTS` |
| `drain_label_shuffle_null.py` | `out_reports` (different variable name, same path string) |

Also update: `dependency_graph_build.py` — embeds `analysis/reports/` as string data inside JSON output. Update string data separately from the `REPORTS=` bulk replace.

**File renames within `findings/`** — human-written docs only (script outputs keep their names):

| Old name | New name | Note |
|---|---|---|
| `section_A_population_equality.md` | `population_equality.md` | |
| `section_C_geographic_coherence.md` | `geographic_coherence.md` | |
| `section_D_procedural.md` | `procedural_analysis.md` | |
| `section_4_geometry_provenance.md` | `geometry_provenance.md` | |
| `bias_audit.md` | `partisan_bias_summary.md` | |
| `sensitivity_report.md` | `sensitivity_analysis.md` | |
| `tier_c_sweep_analysis.md` | `boundary_sweep_analysis.md` | `tier_c` is internal jargon |
| `2015_cross_election_analysis.md` | `cross_election_2015.md` | |
| `ndp_burst_symmetry.md` | `burst_symmetry_analysis.md` | |
| `byelection_assessment.md` | unchanged | |
| `marginal_seats_findings.md` | unchanged | |
| `joint_outlier_score_summary.md` | unchanged | script writes here |
| `neighbour_drain_analysis.md` | unchanged | script writes here |
| `municipal_anchoring_analysis.md` | unchanged | script writes here |

Move to `archive/dpg/` (DPG-era outputs that landed in analysis/reports/):

- `approximate_shape_analysis.md`
- `build_v7_log.csv`
- `build_v7_summary.json`
- `max_dpi_extract.json`
- `max_dpi_inspect.json`

Remove from `findings/` (D-category — superseded or process artifacts):

- `article_figures_v3.md`
- `plan_b_cross_check.md`
- `wayback_spn2_request.md`

Archive to `archive/` (analytical content, not current but not disposable):

- `consistency_audit.md` → `archive/consistency_audit.md` — phases 2-6 of sign-convention resolution; phase 1 is in `sign_convention_resolution.md` but 2-6 are not captured elsewhere

Keep and rename in `findings/`:

| Old name | New name | Reason to keep |
|---|---|---|
| `91_seat_preliminary.md` | `lunty_91_seat_preliminary.md` | Phase 2 groundwork — Lunty map pre-registered for evaluation Nov 2026 |
| `methods_paper_draft.md` | unchanged | Legitimate scholarly output goal — draft of standalone SZAT/ensemble methods paper |
| `track_c_checklist_baseline_scoring.md` | `checklist_baseline_scoring.md` | Pre-registered Phase 2 baseline — forward dependency on Lunty evaluation; `track_c_` prefix is internal jargon |

Move out of `findings/` — policy documents, not test findings:

| Old path | New path | Reason |
|---|---|---|
| `analysis/reports/act_amendment_proposal.md` | `docs/act_amendment_proposal.md` | Legislative proposal; `findings/` is for test results |
| `analysis/reports/ai_use_recommendations_for_committee.md` | `docs/ai_use_recommendations_for_committee.md` | Policy recommendation; same reason |

Move out of `analysis/methodology/reference/` — operational/planning documents:

| Old path | New path | Reason |
|---|---|---|
| `analysis/methodology/changedetection_setup.md` | `docs/changedetection_setup.md` | Service setup instructions; not research methodology |
| `analysis/methodology/external_tool_validation_plan.md` (→ `external_tool_validation.md`) | `docs/external_tool_validation.md` | Validation plan; live task tracked in TODO.md; move to docs once runs complete |

---

### `outputs/` → `reports/` at root

`git mv outputs reports`

Rename subdirectories:

- `reports/academic_report/` → `reports/academic/`
- `reports/public_report/` → `reports/public/`

**Build script path fix (grounded 2026-05-13):** Both build scripts currently reference
`SRC_MD = REPO_ROOT / "report_academic.md"` (root-level) — a pre-existing bug; those files
do not exist at root, they live in `outputs/academic_report/` and `outputs/public_report/`.
Fix both as part of the restructure:

```python
# build_academic_pdf.py — before (broken path)
SRC_MD = REPO_ROOT / "report_academic.md"

# After
SRC_MD = REPO_ROOT / "reports" / "academic" / "report_academic.md"
```

```python
# build_pdf.py — before (broken path)
SRC_MD = REPO_ROOT / "report_public.md"

# After
SRC_MD = REPO_ROOT / "reports" / "public" / "report_public.md"
```

---

## README Convention

GitHub renders `README.md` automatically at any directory level. Every directory
a reader might land in cold gets one. Write these as part of the execution pass —
do not leave a directory without a README after restructuring it.

| Directory | README content |
|---|---|
| `/` | Project overview — findings, quickstart, citation (already exists; update paths) |
| `preregistration/` | What each file commits to, OSF registration IDs, filing dates |
| `analysis/methodology/` | Index of test design + defense docs; what provenance/ and reference/ contain; which 5 files scripts write to and why they can't move |
| `analysis/methodology/provenance/` | What each file documents and which script or process produced the data it describes |
| `analysis/methodology/reference/` | What each file covers; which are literature, which are geographic fact-checks, which are legal sources |
| `analysis/review/` | What kind of scrutiny each file represents (science, legal, peer, external code audit) |
| `findings/` | Which files are script outputs (never edit by hand) vs. human-written summaries; how to re-generate script outputs |
| `reports/` | How to rebuild both PDFs; dependency on pandoc version |
| `archive/` | Date and rationale for restructure; logic delta (DPG vs. canonical-era); how to read archived files |
| `archive/provisional_geometries/` | What provisional geometries were, why archived not deprecated, what verification images show, logic delta vs current findings |

---

## Execution Day Prerequisites

Before the first `git mv`:

1. **Clean working directory.** `git status` must show nothing staged or modified. A dirty tree means `git reset --hard HEAD` is NOT a safe undo — it would destroy uncommitted work. Stash or commit everything first.
2. **Dedicated branch.** `git checkout -b feat/restructure` — do not work on `main`. The restructure is one atomic operation that merges after full verification, not a series of incremental commits to main.
3. **Code freeze.** Declare no other branches should merge during execution. The restructure touches paths that active development branches may also be editing. Estimated window: 4 hours.

**If anything goes wrong mid-execution:** `git reset --hard HEAD && git clean -fd` returns to the exact pre-restructure state — but only if the working directory was clean when you started.

---

## Execution Order

0. **Pre-move hash capture + grep sweep.**
   ```powershell
   # Capture current FROZEN_MANIFEST hash as pre-restructure baseline
   python -c "import hashlib, json, pathlib; [print(p, hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]) for p in sorted(pathlib.Path('findings').rglob('*')) if pathlib.Path(p).is_file()]" > pre_restructure_hashes.txt
   ```
   *(Run after `findings/` exists, i.e. after Step 5 — or against `analysis/reports/` before the move.)*

   Grep sweep — catches .py, .md, .yaml, .json:
   ```powershell
   grep -r "analysis.reports\|analysis/reports" --include="*.py" --include="*.md" --include="*.yaml" --include="*.json" -l
   grep -r "warrington_declination_defense\|test_apparatus_defense\|urban_weight_defense" -l
   ```
   Resolve any surprises before proceeding.

1. Remove all identified files (`git rm`) — reduces index noise before renames
2. Merge defense docs into `methodological_defenses.md`:
   - Add named sections with explicit anchors: `## Test Apparatus Defense {#test-apparatus-defense}` etc.
   - Each merged section opens with a standard metadata block:
     ```
     **Status:** [Pre-registered date or "Post-hoc defense"]
     **Target objection:** [one sentence — what criticism this answers]
     **Key evidence:** [pointer to the primary supporting file or section]
     ```
   - Update all 4 files with broken links (report_academic.md ×5, README.md, null_hypothesis…, dependency_graph_build.py docstring)
   - Then `git rm` the 3 source files
3. Create new directories (`preregistration/`, `archive/`, `analysis/methodology/provenance/`, `analysis/methodology/reference/`, `analysis/review/`)
4. Tier 1 moves (`git mv`) — zero code deps
5. Tier 2 moves (`git mv analysis/reports findings`, `git mv outputs reports`)
6. Add `findings_dir` key to `config.yaml`; add `FINDINGS` accessor to `data_loader.py`; update 9 scripts to import it
7. Build script `SRC_MD` path fix (`build_pdf.py` and `build_academic_pdf.py`)
8. Write READMEs for all 9 directories in the table above
9. Add OSF registration links and "Date Registered" headers to all 7 files in `preregistration/`
10. Update root `README.md`: add note that `data/outputs/district_patterns/` is the machine-readable geographic record of packing/cracking/draining patterns (visualization code sunsetted; underlying spatial evidence preserved)
11. Run broken-link check:
    ```powershell
    # Check all markdown cross-references resolve
    markdown-link-check --quiet (Get-ChildItem -Recurse -Filter "*.md" | Select -ExpandProperty FullName)
    # Or if not installed: grep for .md links and spot-check
    grep -r "\](analysis/methodology/\|analysis/red_team/\|analysis/reports/" --include="*.md"
    ```
12. Run verification:
    ```
    python -m pytest tests/ -x -q
    python run_audit.py
    python analysis/scripts/build_pdf.py --dry-run
    ```
    Two additions to make to `run_audit.py` before execution day:

    **a. `--path-check` flag:** loops over every `Path.open()` call, does `path.exists()` only,
    no GeoPackage loading. Catches missing paths in ~2 seconds instead of waiting for the
    full 10-check suite to crash mid-run.

    **b. Dirty-check guard:** before any script writes to a known machine-output file, check
    `git status --porcelain <filepath>`. If the file has uncommitted manual changes, abort:
    *"Manual changes detected in machine-output file. Commit or stash before running audit."*
    This prevents a script from silently overwriting a human fix.

    **c. Stale-output purge:** each script deletes its target output file before writing.
    Prevents the failure mode where a script finds an old version of the file at a legacy
    path and silently "succeeds" without actually running.

13. Post-restructure hash comparison:
    ```powershell
    python -c "import hashlib, json, pathlib; [print(p, hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()[:12]) for p in sorted(pathlib.Path('findings').rglob('*')) if pathlib.Path(p).is_file()]" > post_restructure_hashes.txt
    diff pre_restructure_hashes.txt post_restructure_hashes.txt
    ```
    Expected diff: file paths change (analysis/reports/ → findings/); hashes are identical.
    Any hash change means a script wrote different output — investigate before committing.

14. **TREE.md path lint.** Parse `TREE.md` for any file path strings (lines matching
    ` ├── ` or ` └── ` that contain a `.` extension or path separator) and call
    `os.path.exists()` on each. Any annotation that points to a non-existent file is a
    curation lag — fix before committing. This is the validation that the curated navigation
    document matches the actual post-restructure state.
    ```python
    # Quick manual check:
    python -c "
    import re, os
    for line in open('TREE.md'):
        m = re.search(r'[├└]── ([\w/.-]+\.\w+)', line)
        if m and not os.path.exists(m.group(1)):
            print('MISSING:', m.group(1))
    "
    ```

15. Commit in one clean commit; delete `RESTRUCTURE_PLAN.md`, `pre_restructure_hashes.txt`, `post_restructure_hashes.txt`; merge `feat/restructure` to `main`

---

---

## Remove: `interactive_proofs/`

The React/TypeScript web app has never been deployed and adds maintenance debt with
no analytical value. Remove the entire directory.

**Before removing**, extract these two data assets to `data/outputs/district_patterns/`:

| Source | Destination | What it is |
|---|---|---|
| `interactive_proofs/public/data/*.geojson` (36 files) | `data/outputs/district_patterns/` | Geographic boundaries of every identified packing, cracking, and draining district for both maps — 2019 and 2026 versions with dot files |
| `interactive_proofs/public/data/events.json` | `data/outputs/district_patterns/packing_cracking_events.json` | Per-district vote statistics (UCP/NDP %, margins, safety classification, voter impact) for each boundary change event — the metadata layer for the GeoJSON files |

These are the only copies of this data in the repo. The React app wrapper has no value;
the underlying data does.

Add `data/outputs/district_patterns/` to the `findings/` README as a note that this
directory contains the machine-readable geographic record of identified packing,
cracking, and draining patterns.

Add step to execution order: extract data assets before `git rm -r interactive_proofs/`.

---

## Post-Execution Hardening

Once the restructure commits are merged, add these guards to prevent the structure from drifting:

**1. Protected-files pre-commit hook.** Maintain a `.protected_files` list at repo root:
```
findings/szat_summary.json
findings/szat_summary_full_votes.json
findings/szat_2019_baseline.json
findings/neighbour_drain_analysis.md
findings/municipal_anchoring_analysis.md
findings/joint_outlier_score_summary.md
findings/joint_outlier_score.json
findings/intermap_permutation_test_results.json
analysis/methodology/audit_dependency_graph.json
analysis/methodology/audit_dependency_graph.dot
analysis/methodology/fisher_independence_defense.md
analysis/methodology/submission_search_log.md
```
A pre-commit hook checks whether any staged change touches a listed file and aborts
if the `RUNNING_FROM_SCRIPT` environment variable is unset. The dirty-check guard in
`run_audit.py` (Step 12b) sets this variable before writing.

**2. TREE.md path linter.** The Step 14 script above can be run as a pre-commit hook too:
blocks any commit that leaves `TREE.md` pointing at non-existent paths.
This ensures curation stays accurate without automating the content.

**3. `findings/README.md` machine-output list.** Explicitly enumerate every file in
`findings/` that is machine-generated and must not be hand-edited; state which script
generates each one and how to regenerate it.

---

## Do Not Touch

- `data/` directory name or internal structure — config.yaml and every script uses `data/` paths
- `tests/` — pytest discovers by convention
- CSV/JSON files in `findings/` (was `analysis/reports/`) that scripts write to — keep exact names
- `data/outputs/` contents — dozens of hardcoded output paths
- `interactive_proofs/` — Vite build has its own path conventions
- `analysis/scripts/` — imports and test discovery depend on location
