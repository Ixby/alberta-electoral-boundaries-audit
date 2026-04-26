# Legal-standard red-team framework

**Directive:** red-team every file in the repo to a standard defensible in a court of law (2026-04-23).

**Scope:** all files under `alberta_audit/` excluding `deprecated/` and `.temp/`. Approximately 150+ files across primary outputs, analysis documents, data artifacts, scripts, and reproducibility infrastructure.

**Posture:** this framework treats the audit as evidence that could be tendered in (a) a Charter-based boundary-drawing challenge, (b) a defamation proceeding arising from any adverse characterisation of a named commissioner / MLA / premier, (c) expert-witness testimony before a parliamentary committee, or (d) a journalistic defamation action responding to magazine publication. The standard is not "convincing on the face" but "survivable under hostile cross-examination."

---

## Legal-defensibility dimensions (ten)

Every file is evaluated against the ten dimensions below. Each finding is classified CRITICAL / HIGH / MEDIUM / LOW by dimension and severity.

### D1 — Evidentiary chain (primary source + archive)

Every substantive claim must trace to a primary source (public record, statutory text, census table, commission report, statement of vote, etc.) with a live URL AND an immutable archive snapshot (Wayback Machine or archive.ph). A claim citing a drifted URL with no archive is a **CRITICAL** evidentiary gap. A claim with a URL but no archive is **HIGH** until `FROZEN_MANIFEST.md` is updated. A claim with an archive but no author-verified retrieval date is **MEDIUM**.

### D2 — Attribution accuracy (verbatim quotations)

Every quoted string attributed to a named person or document must match the source verbatim, including punctuation and capitalisation. Paraphrases presented as quotations are **CRITICAL**. Quotations where the source is cited but the text differs even by a word are **HIGH**. Quotations without a page/line anchor are **MEDIUM**.

### D3 — Individual-actor characterisation (fair comment, public-interest, not defamatory)

Named individuals (commissioners, MLAs, premier, chair, addendum authors) may only be characterised in ways that (a) relate to their public conduct in a public role, (b) rest on publicly-documented evidence cited inline, and (c) distinguish fact from opinion. Characterisations imputing improper motive, dishonesty, or bad faith without documented evidence are **CRITICAL** (defamation exposure). Characterisations that reasonable readers could read as imputing motive without the text explicitly saying so are **HIGH** (innuendo risk). Unclear fact/opinion boundaries are **MEDIUM**.

### D4 — Methodology reproducibility

Any statistical / geometric / textual finding must be reproducible by a third party using only the files in the repo plus the archived primary sources. Missing scripts are **CRITICAL**. Scripts that run but depend on unarchived external URLs are **HIGH**. Scripts that run but produce numerically different results than reported are **CRITICAL**. Stochastic scripts without a pinned seed are **HIGH**.

### D5 — Data provenance (every CSV/GPKG/JSON → documented source)

Every data artifact must have a documented provenance chain: source URL → retrieval date → transformation script → output artifact. Artifacts with no documented source are **CRITICAL**. Artifacts whose documented source does not match the actual contents (e.g., a "2023 results" file that contains 2019 data) are **CRITICAL**. Artifacts with partial documentation are **HIGH**.

### D6 — Privilege / scope (fact vs. opinion vs. allegation)

Every adverse statement about an identifiable actor must be labelled as fact (with citation), opinion (with basis), or allegation (with source). Assertions stated as fact but resting on inference are **HIGH**. Opinions labelled as findings are **HIGH**. Allegations not traced to a named source are **CRITICAL**.

### D7 — Conflict of interest (author's standing)

The author's political affiliations, financial interests, prior employment related to the subject matter, and any personal involvement in the 2026 redistribution process must be disclosed somewhere discoverable in the repo (typically the author bio or a dedicated disclosure section). Missing disclosure is **HIGH** (credibility exposure; does not meet evidentiary bar but undermines witness standing).

### D8 — Copyright / fair dealing

Third-party quotations and image reproductions must fall within Canadian fair-dealing (s.29 Copyright Act) purposes (research, private study, criticism, review, news reporting, education, satire, parody) AND include attribution with source. Reproductions exceeding the fair-dealing threshold are **CRITICAL**. Attribution gaps are **HIGH**.

### D9 — PII / confidentiality

No personal data about private individuals (voters, witnesses, minor children of public figures, non-public contact information) must appear in any artifact. Leaked PII is **CRITICAL**. Data that could be used to re-identify individuals via combination with external data is **HIGH**.

### D10 — Time-stamped / falsifiable claims

Predictions (e.g., "the November 2026 MLA committee map will likely…") must be labelled as predictions with a falsifiability condition. Undated prospective claims are **HIGH**. Retrospective claims presented as unchanged-since-X without the X date are **MEDIUM**.

---

## Severity classification

- **CRITICAL** — would likely lose in cross-examination; blocks release.
- **HIGH** — defensible but weak; should be tightened before release.
- **MEDIUM** — defensible with context; note in the findings log for future revision.
- **LOW** — stylistic or housekeeping; no release impact.

## File-class triage order

1. **Primary public-facing outputs** (highest defamation + scrutiny risk)
   - `report_public.md`
   - `report_public.pdf`
   - `report_academic.md`
2. **Reproducibility manifests**
   - `FROZEN_MANIFEST.md`
   - `requirements.txt`
   - `setup.md`
3. **Analysis documents underpinning named-actor characterisations**
   - `analysis/methodology/v0_1_minority_rationales_validation.md`
   - `analysis/methodology/v0_1_school_division_coherence.md`
   - `analysis/reports/v0_1_section_C_geographic_coherence.md`
   - `analysis/reports/v0_1_bias_audit.md`
   - `analysis/reports/v0_1_design_critique.md`
4. **Scripts producing numerical claims in the reports**
   - `analysis/scripts/v0_2_packing_cracking_analysis.py`
   - `analysis/scripts/v0_3_monte_carlo_ci.py`
   - `analysis/scripts/338canada_scraper.py`
   - `analysis/scripts/338canada_reallocate.py`
   - `analysis/scripts/mcmc_ensemble.py`
   - `analysis/scripts/mcmc_full_coverage_rescore.py`
5. **Data artifacts**
   - `data/*.gpkg`, `data/*.csv` (each must trace to a source in `FROZEN_MANIFEST.md`)
6. **Remaining analysis documents, scripts, and auxiliary files**
7. **Scope exclusions** — `deprecated/`, `.temp/`, and any file with `deprecated_` prefix are reviewed only to confirm they are not cited in primary outputs.

## Findings output

Each file class produces a red-team findings file:

- `analysis/red_team/v0_1_legal_red_team_report_public.md`
- `analysis/red_team/v0_1_legal_red_team_report_academic.md`
- `analysis/red_team/v0_1_legal_red_team_frozen_manifest.md`
- `analysis/red_team/v0_1_legal_red_team_analysis_docs.md`
- `analysis/red_team/v0_1_legal_red_team_scripts.md`
- `analysis/red_team/v0_1_legal_red_team_data_artifacts.md`

Each findings file follows the template:

```
## Finding ID [D-dimension-NN]
**Severity:** CRITICAL | HIGH | MED | LOW
**Dimension:** D1–D10
**File:** path
**Line / region:** line number or section
**Claim under review:** verbatim from file
**Concern:** one-sentence cross-examination question this claim would face
**Evidence status:** sourced / unsourced / partially sourced
**Recommendation:** specific fix (tighten, add citation, retract, rephrase, move to opinion)
```

## Cross-referencing

- Existing red-team files (`v0_1_red_team_*.md`) address code, assertions, references, conclusions, and latent bias. Their findings are the starting point; this legal pass extends them to the court-admissibility standard above.
- Findings marked CRITICAL in earlier passes but deferred are re-examined here against the ten dimensions.

## Parallelisation plan (for 4:30am agent restart)

Once agent rate limits reset, six agents run in parallel, one per findings file, each scoped to its file class. Each agent produces its findings file and a summary table. A seventh agent (conductor role) consolidates all six into a single release-readiness score and blocks release on any outstanding CRITICAL.

Until then, this framework document and the `report_public.md` first-pass findings below are the serial-execution deliverables.
