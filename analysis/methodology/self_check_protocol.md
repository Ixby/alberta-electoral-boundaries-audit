# Self-Check Protocol — Alberta Electoral Boundaries Audit

This document defines the quality-control checks the user can trigger at any point in the audit. Type the phrase exactly as listed; Claude will execute the corresponding checklist.

---

## Trigger phrases

| Phrase | Scope | Purpose |
| --- | --- | --- |
| `check task` | Last completed unit of work | Verify the change did what was intended and left no loose ends |
| `check project` | Full audit state | Broad consistency pass — open items, blockers, structural debt |
| `check pre-reg` | Pre-registration chain | Confirm code, seeds, and registration text are mutually consistent |
| `check lit` | Literature reviews | Cross-check academic and draft-paper lit reviews for divergence |
| `check deps` | Dependency graph | Confirm `audit_dependency_graph.json` is current; flag stale paths |

---

## `check task` — task-level verification

Run after any commit or completed unit of work.

1. Read the last two git commit messages (`git log --oneline -2`). Do they match what was actually changed (`git diff HEAD~1`)?
2. Check for new lint warnings in files touched by the last commit.
3. **If a `.md` file changed:** grep for cross-references (AsPredicted numbers, OSF URLs, file paths) and confirm each still resolves.
4. **If a `.py` script changed:** confirm imports don't break — `python -c "import sys; sys.path.insert(0, 'analysis/scripts'); import <module>"`.
5. **If a `data/outputs/` file changed:** confirm the producing script and any worklog entry (`dpg_validation/dpg2_worklog.md` or `analysis/methodology/`) are updated to match.
6. **If a pre-registration document changed:** check that every AsPredicted number and OSF URL in the file appears consistently in `dpg_validation/dpg2_worklog.md` §Pre-registration table.
7. **If files were moved:** confirm no remaining references to the old path exist in tracked files (`grep -r "<old_path>" --include="*.py" --include="*.md"`).

Report: pass/fail per item; any action needed.

---

## `check project` — project-level state

Run at the start of a new session after a gap, or when the user asks for a status summary.

1. `git log --oneline -10` — what changed in the last ten commits?
2. Read `private_notes/live_tasks.md` — any open items that appear overdue?
3. Read `dpg_validation/dpg2_worklog.md` — what phase is active, what is blocked?
4. Read `analysis/methodology/academic_literature_review.md` §7 priority table — any **High** items with Status "Not yet incorporated"?
5. Read `analysis/red_team/red_team_conclusions.md` — any CRITICAL or HIGH findings without a documented resolution?
6. Check `analysis/meta/FROZEN_MANIFEST.md` — are any URLs marked "unarchived" that may now be archivable?
7. Check for structural debt:
   - Any `*_backup.md` files at the repo root? (`ls *.md | grep backup`)
   - Any `v0_1_`-prefixed files outside `historical/`? (`find . -name "v0_1_*" ! -path "*/historical/*" ! -path "*/private_notes/*"`)
   - Any science red-team docs in `analysis/methodology/` rather than `analysis/red_team/`? (`ls analysis/methodology/ | grep "red_team\|science_red"`)
8. Check dependency graph currency: does `analysis/methodology/audit_dependency_graph.json` reflect current script names? (Key stale paths to watch: `v0_1_dpg_perturbation_sensitivity.py`, `v0_1_assignment_va_attribution.py` — these were renamed and the graph needs a rebuild.)

Summarise: open items, blockers, recommended next action.

---

## `check pre-reg` — pre-registration chain

Run any time the pre-registration record is touched or before any simulation result is cited.

1. Read `dpg_validation/dpg2_worklog.md` §Pre-registration. Confirm the AsPredicted table has four rows: #289449 (DPG v11, complete), #289451 (Neighbour-Drain, pending), ~~#289452~~ (superseded), #289455 (Lunty 91-seat, pending).
2. Read `analysis/scripts/drand_seed.py`. Confirm `CANONICAL_ROUND = 5500000` and `CANONICAL_RANDOMNESS` match the value at `drand.cloudflare.com/public/5500000`.
3. Confirm `analysis/scripts/november_red_alert_scorecard.py` contains `BOOTSTRAP_SEED: int = get_canonical_seed("lunty-bootstrap")`.
4. Confirm `analysis/scripts/drain_label_shuffle_null.py` uses `get_canonical_seed("drain-label-shuffle")` (or per-map salts derived from it).
5. Confirm OSF registration URLs in `analysis/methodology/academic_literature_review.md` §12 table match the `dpg_validation/dpg2_worklog.md` OSF column (w2s8k, r3zm7, qsgy8).
6. Confirm git commit `d2aea42` exists and predates any simulation output files (`git show d2aea42 --stat`).

Report: any mismatch between registered text and committed code.

---

## `check lit` — literature review consistency

Run after any edit to either literature review document.

1. Read `analysis/methodology/academic_literature_review.md` §7 priority table. Note any item marked **High** with Status other than "incorporated" or cross-referenced.
2. Read `private/draft_papers/novel_tests_lit_review.md` (gitignored; exists locally). Check §2.1 for Neighbour-Drain cross-reference and §8 pre-registration table.
3. Confirm the following are consistent across both documents:
   - Rodden 2019 *Why Cities Lose* cited with full reference
   - Chen & Rodden 2013 cited (QJPS 8, 239)
   - Rucho v. Common Cause 588 U.S. 684 (2019) cited in the academic review §5
   - Neighbour-Drain intensity formula and AsPredicted #289,451 reference appear in both
4. Confirm `academic_literature_review.md` §2 still has the ⚠ S6-01/S6-02 citation flags on Pal (2015) and Pal (2019). These must not be silently removed.
5. Confirm all citations in `academic_literature_review.md` use APSA style: Author Last, First. Year. "Title." *Venue* Volume(Issue): Pages. (See §10 of this protocol for APSA format reference.)

Report: any divergence or missing cross-references.

---

## `check deps` — dependency graph currency

Run after significant script additions or renames.

1. Run `python analysis/scripts/dependency_query.py --list-scripts` (or equivalent) to list what the graph currently knows.
2. Compare against `ls analysis/scripts/*.py` — any scripts present on disk but not in the graph?
3. Check for stale paths: grep the graph JSON for `v0_1_dpg_perturbation_sensitivity`, `v0_1_assignment_va_attribution`, `v0_1_shape_refinement` — these were renamed and should now reference their `historical/` locations.
4. If the graph is stale, run `python analysis/scripts/dependency_graph_build.py` to rebuild, then commit the updated `analysis/methodology/audit_dependency_graph.json`.

---

## Section 10 — APSA citation format reference

All citations in `academic_literature_review.md` and draft papers use APSA (American Political Science Association) format:

**Journal article:**
Author Last, First. Year. "Article Title." *Journal Name* Volume(Issue): Pages.
> Chen, Jowei, and Jonathan Rodden. 2013. "Unintentional Gerrymandering: Political Geography and Electoral Bias in Legislatures." *Quarterly Journal of Political Science* 8(3): 239–269.

**Book:**
Author Last, First. Year. *Book Title*. Place: Publisher.
> Rodden, Jonathan. 2019. *Why Cities Lose: The Deep Roots of the Urban-Rural Political Divide*. New York: Basic Books.

**Court case (legal citation, not APSA per se):**
*Case Name*, Volume Reporter Page (Court Year).
> *Rucho v. Common Cause*, 588 U.S. 684 (2019).

**Pre-registration / dataset:**
Author Last, First. Year. "Title." Platform. URL.
> Conner, Will. 2026. "Alberta 2026 Electoral Boundary Audit — DPG v11 Validation." AsPredicted #289449. https://aspredicted.org/289449.pdf

---

*Protocol version: 2026-05-06. Update this document when trigger phrases or checklist items change.*
