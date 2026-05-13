# Science-standard red-team framework

**Directive:** red-team every file in the repo to a standard defensible under peer review (2026-04-23).

**Scope:** all files under `alberta_audit/` excluding `historical/` and `.temp/`. Companion to `analysis/red_team/legal_red_team_framework.md`. Where the legal framework asks "would this survive cross-examination?", the science framework asks "would this survive a methods-paper peer review?"

**Posture:** the audit is evaluated as if being submitted as a methods paper to a peer-reviewed political-science / statistics journal (candidate venues: *Election Law Journal*, *Statistics and Public Policy*, *Journal of Quantitative Description*, *PNAS Nexus*). Reviewers will hunt for the same pathologies they hunt for in any social-science paper: pre-registration, researcher degrees of freedom, cherry-picked metrics, confounder control, statistical power, prior-literature engagement, and calibration of claim strength to evidence.

---

## Science-defensibility dimensions (ten)

### S1 — Experimental design (pre-specified vs. post-hoc)

Every test reported must have been specified *before* the data were examined (pre-registered) or clearly labelled as exploratory. The audit's signature framework (P1–P3 packing, C1–C3 cracking, E1–E3 engineered-boundary) was specified ahead of detection — this is the model. Any test that was added or reshaped *after* looking at the data is HIGH S1 unless the reshaping is disclosed (as §3.9 discloses for E2). Post-hoc tests presented as if pre-registered are CRITICAL S1.

### S2 — Statistical validity (tests, power, multiple-comparisons)

Standard checks: did the audit use tests appropriate to the data scale (Likert vs. continuous vs. count); does the sample size support the claimed effect size; has the family-wise error rate been controlled when multiple tests are run on the same data; are confidence intervals reported rather than point estimates alone. The four partisan-bias metrics (B2 EG, B3 MM, B4 S@50/50, B6 declination) plus the 21-hybrid school-division audit plus the 77-snapshot 338 stability probe plus the MCMC ensemble together constitute ~10 distinct statistical tests on overlapping data. No family-wise correction is reported. HIGH S2.

### S3 — Reproducibility (computational + conceptual)

Computational: every numeric claim must be reproducible from the committed repo with the pinned environment. Conceptual: a second team using the same data but different tools should reach the same qualitative conclusion. Computational is largely covered by the legal-framework D4; conceptual reproducibility is science-specific — does the audit's conclusion survive if a reviewer substitutes a different metric for EG, a different compactness definition, a different ensemble seed, a different crosswalk weight?

### S4 — Null hypothesis + falsifiability framing

Every claim needs a null it's rejecting and a concrete falsification condition. The audit's §3.5 falsifiability gate plus §3.14 RT1–RT7 stress-test table is the model; the checklist's 3/4 coverage is MED S4. Any claim presented as a finding without a null hypothesis statement is HIGH S4.

### S5 — Confounder control

For every purported effect, what confounders were considered and excluded? Two confounders the audit must address:
1. **Natural geographic packing** (Chen & Rodden 2015) — UCP voters spread across rural Alberta would produce a UCP-favourable EG under *any* map that respects population equality. §3.6 engages this; verify engagement is complete.
2. **Alberta's UCP-heavy 2023 electorate** — the minority's UCP-favourability reverses under 2019 votes. §3.4 engages this via cross-election stability. Verify that the reported "direction is weight-invariant" is the right framing given one confounder (the electorate itself) can flip the sign.

Any partisan-bias claim that does not explicitly address both confounders is HIGH S5.

### S6 — Prior-art engagement (literature review completeness)

A methods paper must locate itself in the extant literature. The audit cites Stephanopoulos & McGhee (2014/2015), Warrington (2018), McDonald & Best (2015), Chen & Rodden (2015), Altman & McDonald (2011), Gelman & King (1994), Tufte (1973), Katz & King & Rosenblatt (2020), Grant v. Torstar (SCC 2009), Rizzo v. Rizzo Shoes (SCC 1998). Two gaps a peer reviewer will flag:
1. **Pildes & Stephanopoulos on measurement** — the EG-vs-PS debate in the 2015–2019 literature bears on whether 7% is a sensible threshold.
2. **Canadian-specific redistribution literature** — Carty, Pal, Courtney — whose framings differ from the US-centric literature the audit leans on.

Any major claim that rests on US-only literature without Canadian-context engagement is MED S6.

### S7 — Data quality (coverage, selection bias, measurement error)

Every data artifact needs its coverage, selection bias, and measurement error characterised.
- **2023 Statement of Vote coverage** — should be near-100%; verify.
- **Submission search coverage** — 1,252 of 1,345 (93%). What systematic pattern is in the missing 93? Possibly OCR failure on handwritten / low-quality submissions; possibly files with no text layer. HIGH S7 unless characterised.
- **VA-to-ED assignment error** — centroid-in-polygon introduces ~0.5% rounding on border VAs. Acceptable; already noted in MCMC report.
- **MCMC full-coverage caveat** — the 57/70 polygon coverage in the 10k run (now being remedied via crosswalk fallback) is HIGH S7 until the 100k run with full crosswalk closes it.
- **2026 commission shapefiles** — NOT released as of 2026-04-22. All Tier B/C polygon work is approximation. This is the single largest S7 gap.

### S8 — Cherry-picking / researcher degrees of freedom

Have metrics been chosen *after* looking at which ones produce the desired result? Four checks:
1. **Metric selection**: four partisan-bias metrics chosen; three agree on direction, one (declination) disagrees. §3.5.1 addresses this openly — GOOD. No cherry-picking flagged.
2. **Threshold selection**: §15(2)'s 3/5 threshold is statutory, not chosen. Compactness's Polsby-Popper cutoff is standard. GOOD.
3. **Signature threshold**: "three signatures plus new signature plus ensemble outlier" (pre-registered checklist) — the threshold was set before the data, and the current scorecard does NOT cross it. GOOD — evidence against cherry-picking.
4. **Geographic scope**: audit focuses on Calgary, Edmonton, Red Deer, Lethbridge, Airdrie, St. Albert, RMH-Banff. Are there other EDs where the minority/majority differ that were excluded? Verify completeness by running the differ-by-polygon test against all 89 EDs.

### S9 — Claim calibration (magnitude language vs evidence)

The public report's "one to three seats at a tied vote, with a 95-percent confidence interval that crosses zero" is well-calibrated. The academic paper's "directional consistency across six dimensions" is appropriately hedged. The strongest language in the report is "three formal signatures detected in the minority" — this needs the evidence bar to clearly support "formal."

### S10 — Peer-review-readiness

Structural: does the paper have the sections a methods reviewer expects (abstract / intro / data / methods / results / limitations / conclusion)? The academic paper has approximate parallels but uses section names the audit invented (A/B/C/D "tracks"). Retranslating the audit's structure onto the IMRAD template is a MEDIUM S10 finding — good for submission, not required for defensibility.

Transparency: is the code + data + preregistration openly available? Repo is committed; preregistration is planned for OSF submission (per §3.12). GOOD.

Limitations: does the paper have a dedicated limitations section? Yes (§7 in academic, THE LIMITS in public). GOOD.

---

## Severity classification

- **CRITICAL** — would trigger a reject decision from a careful reviewer; blocks submission.
- **HIGH** — would trigger a major revision request; should be fixed before release.
- **MEDIUM** — would prompt a comment in a peer review; note for future revision.
- **LOW** — stylistic or housekeeping; no release impact.

## File-class triage order

1. **Academic paper** (`report_academic.md`) — highest-stakes science venue
2. **Analysis docs producing statistical claims** (MCMC, packing-cracking, compactness, sensitivity, stability probe)
3. **Scripts producing the numbers in the reports**
4. **Public report** — less science-review exposure, but must not contradict the academic
5. **Data artifacts** — cross-checked against claims
6. **Pre-registration + falsifiability docs** (`track_c_checklist_baseline_scoring.md`, `pre_registration_draft.md`)

## Findings output

Three findings files, one per agent:
- `analysis/red_team/science_red_team_design_and_stats.md` — S1, S2, S9
- `analysis/red_team/science_red_team_reproducibility_and_falsifiability.md` — S3, S4, S5, S8
- `analysis/red_team/science_red_team_data_priorart_peerreview.md` — S6, S7, S10

Each findings file follows the template:

```
## Finding [S-dimension-NN]
**Severity:** CRITICAL | HIGH | MED | LOW
**Dimension:** S1–S10
**File / section:** path and section
**Claim under review:** verbatim
**Reviewer objection:** one-sentence objection a peer reviewer would raise
**Evidence status:** supported / partially supported / unsupported
**Recommendation:** specific fix
```

## How this relates to the legal framework

- The legal framework asks "does this evidence survive cross-examination?" The science framework asks "does this analysis survive peer review?"
- D4 (legal reproducibility) ≈ S3 (science reproducibility). Same checks, same finding IDs can be shared.
- D10 (legal time-stamping) ≈ S4 (science falsifiability). Related but different — legal is about dated predictions; science is about formal null-hypothesis framing.
- Several dimensions are unique to science: S1 pre-registration, S2 statistical validity, S5 confounder control, S6 prior art, S8 cherry-picking, S7 data quality at science-paper depth.

A finding triggered by both frameworks gets both severity labels — e.g., "HIGH D2 / CRITICAL S1" if a quote was paraphrased (legal) and a post-hoc test was presented as pre-registered (science).
