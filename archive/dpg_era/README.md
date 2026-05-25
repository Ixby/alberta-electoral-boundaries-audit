---
name: DPG-era archive — orientation
description: "One-paragraph landing for archive/dpg_era/. You probably do not need to read anything in this directory. The audit's live claims, current numbers, and active methodology are all in findings/, reports/, analysis/methodology/, and the top-level README.md. This directory exists for trail-of-work transparency and as the methods-paper worked example."
type: archive
---

> **Backward:**
> - `README.md` (top-level) — points here in §"What the audit finds" for the retraction history
> - `findings/methods_paper_draft.md` §7.1 Stage 9 — uses the contents of this directory as the canonical worked example for the DPG-framework + sunset-clause methodology
> - `analysis/methodology/retraction_pathway.md` — the formal retraction log; refers here for full DPG-era analyses
>
> **Forward:**
> - (leaf — historical archive; not consumed by any live analysis. Skip unless you specifically need the retraction history or the methods-paper case study.)

# DPG-era archive

**You probably don't need to read this directory.** The audit's current claims, current numbers, and active methodology are in:

- `README.md` (top-level) — public summary and headline findings
- `findings/` — live analyses
- `reports/academic/report_academic.md` — full technical monograph
- `reports/public/report_public.md` — plain-language public report
- `analysis/methodology/` — live methodology rationale and defenses

**What's here.** Three analyses whose substantive claims were retracted on canonical recomputation against official Elections Alberta shapefiles (2026-05-06), plus one extracted document preserving the pre-canonical sampler-cross-validation framing. They are kept intact for two reasons: (i) trail-of-work transparency — the audit publicly records what was previously claimed and why it was withdrawn rather than rewriting history; (ii) the methods paper (`findings/methods_paper_draft.md`) uses this directory as its worked example for the Derived Provisional Geometry framework + 48-hour-sunset-clause contribution.

**The files.**

- `municipal_anchoring_analysis.md` — DPG-era municipal-anchoring headline (majority 71.0% / minority 14.5%, a 4.9× asymmetry). Canonical recomputation: majority 80.0% / minority 72.0%, both within the 70–85% Canadian comparator norm. The DPG-era 4.9× gap is retracted.
- `da_anchoring_analysis.md` — DA-edge extension of the municipal analysis. Carried the same DPG substrate; the v0_5 totals (majority 79.6% / minority 16.5%) did not survive canonical recomputation either.
- `natural_anchoring_secondary_check.md` — DPG-era counterfactual asking whether the minority's 14.5% anchoring inverts under highways/rivers. Verdict was INVERTS on DPG (40.2 / 38.4 / 40.1 across 2019-enacted / majority / minority). Moot on canonical geometry because the underlying 14.5% headline did not survive.
- `redist_pre_canonical_history.md` — extracted on 2026-05-23 from `findings/redist_python_comparison.md`. Preserves the pre-canonical setup table, distribution-shape comparison, v0_9 minority placement (0.4831 at ReCom p98.6 vs SMC near-median), stability-caveat triple-run, and the surgical-fortification framing that was withdrawn when the canonical recomputation showed the disagreement was substrate-driven.

**If you are a reviewer:** the live sampler cross-validation is at `findings/redist_python_comparison.md`. The substrate-invariant compactness-mechanism falsification (Test #2, Welch p = 7.7×10⁻²³⁴) lives there, not here. The live Lane-2 case rests on urban hybridization, Airdrie city-splitting, and chair-flagged cartographic anomalies — all unaffected by the DPG → canonical transition.

**If you are auditing the methods paper:** this is the case study. `findings/methods_paper_draft.md` §7.1 Stages 1–10 walks through the development arc; the per-stage anchoring numbers and metric values are reproducible from the files in this directory.

**If you are reading for retraction history:** the formal retraction log is `analysis/methodology/retraction_pathway.md`. This directory is the artifact-level record.
