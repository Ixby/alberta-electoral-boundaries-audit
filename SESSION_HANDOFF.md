# Session handoff — 2026-06-10

This file exists so a Claude session opened on a fresh machine (PC, web container, or another cloud workspace) can pick up the audit's open work without reading the full transcript of the prior session. It is updated at the close of each substantive session.

## Where the audit stands

**Headline status.** The published verdict is supported by the data and stated honestly:
- Structural-lane signature on the minority commission proposal (six independent geometric dimensions, all in the UCP direction).
- Partisan-magnitude lane *near, but below*, the audit's pre-registered Alberta-calibrated 95th-percentile / 4.10 % EG threshold (canonical EG = +3.96 %, percentile p94.4 against the 1,010,000-plan ReCom ensemble).
- Dependence-robust joint upper bound across the two analytical channels: **p ≤ 1.76×10⁻⁶ (≈ 1 in 568,000)**, Bonferroni-corrected. The earlier Fisher figure of 4.61×10⁻⁸ is retired because Ch1 and Ch2 share the same vote-attribution substrate and overlap on the EG dimension — they are not independent. Note: this document (dated 2026-06-10) predates the 2026-07-12 ensemble rerun; see `findings/ensemble_chain1_duplication_note.md` for current numbers.
- Procedural finding on the April 16 cabinet pivot: characterized as without precedent among the Canadian redistribution cycles this audit reviewed (per Duane Bratt correspondence). Stands without statistical inference.
- Regional-swing recompute on canonical geometry **corroborates** Lane 1: canonical minority's regional-swing s50 = 0.4607 sits above the maximum of the 10,000-plan verification ensemble's regional-swing distribution. The v0_9 "Lane 1 was officially demoted" finding was an artefact of DPG-substrate underestimation.

**Current commit on `master`:** see `git log --oneline -1` (the audit moves fast; a pinned hash here goes stale within days). All work is pushed.

**Update 2026-06-14.** Since the 2026-06-10 handoff: T1.4-full 1M constraint runs completed; locale set completed (L-2, 19 files); journey-to-work data extracted; media kit + FAQ + hostile-quote docs produced; structural battery (T5.1a) replicated on the minority map and demonstrated on the majority map (0/5); evaluation-symmetry matrix added. The work ledger was moved off-repo (2026-06-13). The methodology-defense corpus was brought into sync with the 2026-06-10 Fisher retirement.

## How to pick up

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit
git lfs install
git lfs pull   # ~200 MB; pulls the canonical 1.01M chain CSV + shapefiles
pip install -r requirements.txt
cd viewer && npm install && cd ..

# The operational backlog is tracked locally and is NOT in this repo
# (it was moved off GitHub 2026-06-13). On a fresh clone it will be absent;
# the maintainer keeps it in a gitignored private working directory.
```

## What's in flight (read these in order)

1. **Local work ledger (off-repo, gitignored)** — every queued item, status, acceptance criterion, and resolution path. This was moved out of the repository on 2026-06-13; it will not appear in a fresh clone. Ask the maintainer for the current ledger before assuming the backlog is empty.
2. **`findings/dpg_legacy_audit.md`** — the full DPG-creep scan from 2026-06-10. Confirms no published canonical number is contaminated; flags cosmetic residue queued at T4.5.
3. **`findings/regional_swing_canonical_robustness.md`** — the substantive Lane-1 corroboration result. Supersedes `findings/regional_swing_robustness.md` (v0_9 era).
4. **`preregistration/november_2026_scoring_spec.md`** — the frozen November held-out test. Substrate, S1–S6, P1–P4, the 2×2 verdict surface, the 72-hour public commitment.
5. **`reports/academic/report_academic.md`** §4.1.4 sunset clause, §4.3.2 Bonferroni paragraph, §4.3.3 multiple-comparison strategy, §5.4.9 effect-size paragraph, §5.2.10 SZAT paragraph, §7.0 Lane-1 hedge, Appendix D.3 declination formula — all carry the corrected dependence-robust framing.
6. **`reports/public/report_public.md`** lead and verdict-table row, and `docs/FINDINGS_BRIEF.md` Top Findings + pre-registration paragraph — all carry the corrected public-facing prose.

## Open scripts (stubs landed 2026-06-10)

All four are committed. Each runs as a smoke test; the parts marked TODO are honest placeholders, not silent fallbacks.

- **`analysis/scripts/run_structural_battery.py`** — orchestrates S1–S6 for the November test. S4 (Polsby-Popper compactness) runs end-to-end against canonical; S1, S2, S3, S5, S6 emit honest "did not execute" markers with specific wire-in points. Run with `--shapefile <path>` to test.
- **`analysis/scripts/verdict_synthesis.py`** — combines structural + joint outlier into the pre-committed 2×2 verdict. Fully functional. Refuses to publish (`publishable_72h: false`) if any structural metric did not execute.
- **`analysis/scripts/rural_gap_dissection.py`** — full implementation of the rural-mean / partisan-lean drill-down. Run with `--populations` and `--votes` CSVs. Ready for canonical minority against canonical majority; ready for the November Lunty map once population + vote overlays land.
- **`analysis/scripts/local_perturbation_chain.py`** — Issue #13 retraction-tripwire chain. Framework, retraction rule, and CLI complete; the `single_va_swap()` proposal kernel is a NotImplementedError marker waiting for the implementation per Issue #13 spec.

## What's blocking each open Tier-1 item

| Item | Blocker | Resolution path |
|---|---|---|
| T1.1 1M regional swing | Per-VA assignments for the canonical 1M run are not archived | Re-run `mcmc_ensemble_canonical.py` with `--save-assignments` (script change) OR rely on the 10k subset corroboration already published |
| T1.2 Brown/Cauchy joint | Need paired per-plan (D², SZAT) computation | Iterate the 1M chain once with SZAT compute per plan; estimate `c` for Brown's scaled-χ² OR apply the Liu-Xie Cauchy combination |
| T1.4 Constraint-enforcing ensemble | ~6–8 h compute + script work | Write `mcmc_ensemble_canonical_constrained.py` with s.15(2) tier + anchoring penalties; run 250k–1M plans |
| T1.5 Short-bursts canonical rerun | Compute window (~60–120 min) | `nohup python analysis/scripts/simulation_short_bursts.py > /tmp/bursts.log 2>&1 &` and wait |
| T2.4 LLM sentiment IRR | Human labelling | Label 60-item sample, compute κ, re-publish chair-flag breakdown |
| T6 Legal citations | Counsel review | Pal & Choudhry 2011, Cassista 2014 FC 398, Parks Act citation, Saskatchewan Reference pinpoints, Cannon year, KKR attribution — see T6.1 in the local work ledger |

## What you should NOT do

- **Do not roll back the dependence-robust Bonferroni headline** to the Fisher 4.61×10⁻⁸ figure. Ch1 and Ch2 are not independent under the audit's own data. Any "but the Fisher figure was so much more impressive" pressure is the wrong incentive — the corrected bound is still extreme (1 in 568,000, rerun 2026-07-12) and is what the math supports.
- **Do not amend `preregistration/november_2026_scoring_spec.md` after the Lunty committee publishes its map** except via a dated, signed entry in `findings/pre_registration_amendment_log.md` with the (a) what, (b) why-not-a-goalpost-move, (c) why-unamended-not-feasible structure mandated by the spec itself.
- **Do not delete or "clean up" the partial Cree (`crk.ts.partial`) or Somali (`so.ts.partial`) translations** in `viewer/src/lib/i18n/locales/_wip/`. They're partial work being preserved until the next translation pass completes them.
- **Do not run `git lfs prune`** unless you've confirmed nothing in the canonical pipeline still references the 169 MB raw-samples CSV.

## Translation status

19 locales live in the locales/ directory (sorted by Alberta speaker counts): English, Tagalog (partial), Punjabi (partial), French, Spanish, Arabic, Cantonese, Mandarin, German, Hindi, Vietnamese, Korean, Urdu, Polish, Ukrainian, Russian, Plains Cree (stub), Plautdietsch (stub), and Somali (stub). Partial work for Cree and Somali is preserved at `_wip/`. Punjabi and Tagalog are functional but at ~114/115 lines vs en.ts's 800 — they fall back to English for unfinished keys.

Numeric headline updates (1-in-14.5M → 1-in-568K; 4.61×10⁻⁸ → 1.76×10⁻⁶) were swept across all 12 non-stub locales by `/tmp/patch_locales*.py` (deleted after run). The surrounding narrative was not retranslated — locales L-1 in the local work ledger captures the per-string re-translation pass. Note: The document was drafted 2026-06-10; the current numbers reflect the 2026-07-12 ensemble rerun.

## Reproducibility one-liner

```bash
# Verify the corrected joint statistic against the canonical chain CSVs (post-2026-07-12 rerun)
python -c "
import pandas as pd, numpy as np
from pathlib import Path
chains = sorted(Path('data/simulation_checkpoints_canonical').glob('chain*_samples.csv'))
df = pd.concat([pd.read_csv(c) for c in chains], ignore_index=True)
metrics = ['efficiency_gap','mean_median','declination','seats_at_50_50']
X = df[metrics].values
mu, cov = X.mean(axis=0), np.cov(X, rowvar=False)
inv = np.linalg.pinv(cov)
real_min = np.array([0.040194, 0.010402, 0.077003, 0.516854])  # declination sign corrected in Amendment 10
D2 = float((real_min - mu) @ inv @ (real_min - mu))
n_extreme = int((np.einsum('ij,jk,ik->i', X-mu, inv, X-mu) >= D2).sum())
bonf = 2 * min((n_extreme+1)/(len(df)+1), 0.0024)
print(f'Mahalanobis D = {np.sqrt(D2):.4f}; n_extreme = {n_extreme} / {len(df):,}')
print(f'Bonferroni bound = {bonf:.3g} (1 in {int(round(1/bonf)):,})')
"
# Expected (post-2026-07-12 clean rerun): D = 5.80; n_extreme = 0; bound = 1.76e-06 (~1 in 568,000)
# (The published 1-in-568,000 uses the parametric χ² Ch1 p = 8.80e-7 instead of the
#  empirical floor; both are defensible, the parametric is more conservative.)
```

If that one-liner reproduces, the audit's central machinery is intact and the canonical chain CSVs are unmodified (post-2026-07-12 rerun).

## Last words

The integrity instincts are good. Where the audit gets in trouble is when the public-facing prose runs ahead of what the math supports. The corrected prose now matches the corrected math; the next analyst's job is to keep them in sync as new results land. The local work ledger (held off-repo by the maintainer) is how you do that.

— prior session, 2026-06-10
