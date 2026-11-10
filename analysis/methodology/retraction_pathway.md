---
name: Retraction pathway — per-finding retraction conditions
description: Named conditions under which each active audit finding retracts, plus a record of findings already retracted under the H1-H10 stress-test protocol.
type: methodology
---

> **Backward:**
> - `preregistration/retraction_conditions.md` — pre-committed retraction conditions
> - `analysis/scripts/electoral_forensics_population.py` — produces A1/A2 findings tracked here
> - `analysis/scripts/szat.py`, `mcmc_ensemble_canonical.py`, `joint_outlier_score_canonical.py` — produce findings tracked here
>
> **Forward:**
> - `reports/academic/report_academic.md` §1 (introduction), §5 — cites retraction commitments
> - (leaf — retraction record / commitment ledger)

# Retraction pathway

Each active finding in this audit has a named retraction condition committed before the finding was published. A finding retracts — meaning it is moved from the active findings section to the DOCUMENTED CORRECTIONS box — when the condition is empirically met. The audit's operating rule is to act on a retraction condition within 48 hours of the evidence becoming known. The rule is kept in the repository and is not pre-registered outside it (`preregistration/retraction_conditions.md` §0).

This document is the canonical lookup. Cross-references point to the primary source for each condition.

---

## Active findings and retraction conditions

| Finding | Current status | Retraction condition | Primary source |
|---|---|---|---|
| Population MAD 48% wider (minority 4,707 vs majority 3,180, commission population tables; the official-shapefile-substrate pair is 3,938 vs 2,827 — a 39% gap — which is the value carrying the ensemble p99.13 percentile) | **Active** | An authoritative alternative population source (Elections Alberta official tables) produces a minority-majority MAD gap below 10% | §5.1; commission per-ED population tables |
| Calgary zone asymmetry (12.2% minority vs 0.4% majority on the committed zone lists; on a literal reading of the stated Bow River/Deerfoot rule the minority's gap is 5.3% to 5.7% and the majority's −2.6% to −3.1%, `findings/audit_2026-11-10/calgary_zone_recode.json`) | **Active** | An alternative geographic classification rule — independently derived, not post-hoc — produces a minority-majority asymmetry ≤ 1% while the current Bow River/Deerfoot rule produces >10%; tested with two rules in `electoral_forensics_population.py:a2_robustness_check()`; both rules agree on direction | §5.2.3; `findings/geographic_coherence.md` |
| Fisher combined p = 4.61×10⁻⁸ (Ch1 + Ch2) | **RETIRED 2026-06-10** (see note below) | Either Ch1 (Mahalanobis) or Ch2 (SZAT) p-value is corrected above α = 0.05 upon methodological review | §5.5; `findings/joint_outlier_score_summary.md` |
| SZAT Ch2 p = 0.0024 (boundary-choice partisan bias; i.i.d. null, one-tailed) | **Exploratory only since 2026-06-13**: the i.i.d. null is invalid because neighbouring areas vote alike, and the component-level block test (p ≈ 0.19) has one effective block and cannot reject. Not used in any headline (`findings/szat_block_permutation.md`) | The swing-zone definition is changed such that fewer than 200 VAs qualify as swing zones, making the bootstrap distribution degenerate; or an arithmetic error in the SZAT score is identified | §5.2.10; `analysis/scripts/szat.py` |
| Minority seats@50/50 at ensemble p99.99 | **Active** | An identified arithmetic error in `mcmc_ensemble_canonical.py:seat_results()` inflating the minority's seats@50/50; or official corrected canonical EA shapefiles materially altering the minority's ED boundaries and, on MCMC re-run, placing the minority below the ensemble p95 threshold. (Phase 4C canonical re-run confirms the direction: minority NDP@50/50 = 43 vs majority 48 on the same canonical geometry, 2026-05-17 — Phase 4C is not a retraction trigger for this finding.) | §5.4.9; H5 in §7; `data/outputs/regional_swing_canonical_ed.json` |
| Chair-flagged anomaly count (minority 3 vs majority 0) | **Active** | Majority-map imagery reveals ≥ 3 geometric anomalies of comparable severity (lasso, corridor, or COI-splitting shape) flagged by the commission chair or identified independently | §5.8.2, §5.9.4; chair's published majority report annotations |
| Airdrie split: four divisions by territory, three by people (≥2% of the city), against the majority's two | **Active** | The minority map's Airdrie split configuration is matched by an equally-fragmented treatment of a comparable Alberta city in the majority map | §5.3.2; §5.8 |
| Rationale tests on the six contested configurations. Counting only reasons the minority stated: none fails and four are partly supported. Counting the audit's own population-necessity arithmetic, which tests a claim the minority did not make: four fail | **Active** | Internal commission documents — pre-dating the final report — are published showing the disputed configurations were derived from documented community submissions rather than drafting discretion; or an independent analyst shows that no constraint-legal map can satisfy the minority's stated COI rationales while achieving ≥ 60% CSD/DA edge alignment (Amendment 5, Part 22; a successful counter-map would strengthen the finding) | §5.9.4; §6.2.6 condition 1 |
| Minority EG at ensemble p94.54 | **Withdrawn flag** | Flag already retracted: 1M canonical run places minority EG at p94.54, below the p95 threshold. EG is directional evidence only; the outlier-flag is not asserted | §5.4.9 |

**[SUPERSEDED 2026-06-10 — see `reports/academic/report_academic.md` §4.3.3 and §5.5.]** The Fisher combination of Ch1 and Ch2 (T = 39.87, p = 4.61×10⁻⁸) is retired: it assumed channel independence the two channels do not have (they share the 2023 vote substrate; Brown 1975), and Ch2 (SZAT) does not survive a contiguity-respecting block-permutation null (p ≈ 0.19). The operative joint figure is Ch1 alone (Mahalanobis p ≈ 8.84×10⁻⁷) doubled as a conservative allowance for the two channels then examined (p ≈ 1.77×10⁻⁶). That is one model's estimate on election-day ballots, not a bound: under other defensible choices the figure runs from about 1 in 20,000 to about 1 in 570,000 (`findings/audit_2026-11-10/joint_sensitivity.json`), and no all-ballots version exists. The map is far out in the tail on every version. The Fisher figure here is preserved as historical record. (Updated 2026-07-12 post-ensemble rerun.)

---

## Findings retracted under H1-H10 stress-test protocol

These findings were held during the DPG-era analysis, were stress-tested in the H1-H10 hypothesis battery (§7 hypothesis tests), and did not survive. They are recorded here, not deleted, per the DOCUMENTED CORRECTIONS convention.

| Hypothesis | Retracted claim | What falsified it |
|---|---|---|
| H1 | 2M-step MCMC ensemble, minority seats@50/50 at p100 (no neutral plan reaches it) | The chain orchestration silently re-seeded from the 2019 baseline at every 20k-step chunk boundary; the "2M-step run" was structurally 100 independent 20k-step bursts. Bug fixed in commit `73544a3`. Canonical ensemble replaces this result. |
| H2 | Minority seats@50/50 = 52.8% (published headline) | VA-dissolve coverage was 83/89 districts, not 89/89; 6 districts were effectively unscored. Corrected value is 51.69% for the UCP, 46 of 89 seats (the NDP's share is 48.3%; commit `7cf47a4`). |
| H4 | Municipal anchoring: minority 14.5%, majority 71.0%, 4.9× asymmetry | Did not survive canonical recomputation against official Elections Alberta shapefiles. Canonical: minority 71.8%, majority 80.0%; both within the 70–85% Canadian comparator norm. Retracted per the §4.1.4 DPG sunset clause. Full reconciliation in §5.8.5. |

---

## Provisional findings under active replication

These findings are directional observations that have not been pre-registered and have not been independently replicated. They are reported as exploratory evidence but should not be cited as confirmed findings.

| Finding | Status | What would confirm it |
|---|---|---|
| Minority seats@50/50 at p65–70 under regional swing (vs p99.99 under uniform) | Exploratory (H5) | Independent replication using a different regional-swing parameterisation reaching the same range |
| SZAT 2019→minority score = +0.016 (p=0.053, marginally outside null) | Exploratory | Replication against the panel's 91-seat map, tabled 2026-11-02 (OSF:qsgy8); SZAT's null must be repaired first |
| Submission-archive support-inversion on 3 of 7 minority configurations | **Withdrawn pending recode.** The support/oppose labels behind it are unreliable and the classification is being redone (`findings/submissions_recode/`) | A completed recode with validated labels |

---

## Source

§7.2 (Falsifiability statement); §6.2.6 (What would change the author's verdict); H1-H10 hypothesis battery (§7 hypothesis tests).
