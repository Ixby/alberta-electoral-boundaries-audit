---
name: Retraction pathway — per-finding retraction conditions
description: Named conditions under which each active audit finding retracts, plus a record of findings already retracted under the H1-H10 stress-test protocol.
type: methodology
---

# Retraction pathway

Each active finding in this audit has a named retraction condition committed before the finding was published. A finding retracts — meaning it is moved from the active findings section to the DOCUMENTED CORRECTIONS box — when the condition is empirically met. The audit's pre-registration (§1 introduction) commits to publishing any retraction within 30 days of receiving the falsifying evidence.

This document is the canonical lookup. Cross-references point to the primary source for each condition.

---

## Active findings and retraction conditions

| Finding | Current status | Retraction condition | Primary source |
|---|---|---|---|
| Population MAD 48% wider (minority MAD 3,938 vs majority 2,827) | **Active** | An authoritative alternative population source (Elections Alberta official tables) produces a minority-majority MAD gap below 10% | §5.1; commission per-ED population tables |
| Calgary zone asymmetry (12.2% minority vs 0.4% majority) | **Active** | An alternative geographic classification rule — independently derived, not post-hoc — produces a minority-majority asymmetry ≤ 1% while the current Bow River/Deerfoot rule produces >10%; tested with two rules in `electoral_forensics_population.py:run_alternative_classification()`; both rules agree on direction | §5.2.3; `findings/geographic_coherence.md` |
| Fisher combined p = 6.87×10⁻⁸ (Ch1 + Ch2) | **Active** | Either Ch1 (Mahalanobis) or Ch2 (SZAT) p-value is corrected above α = 0.05 upon methodological review | §5.5; `findings/joint_outlier_score_summary.md` |
| SZAT Ch2 p = 0.0024 (boundary-choice partisan bias) | **Active** | The swing-zone definition is changed such that fewer than 200 VAs qualify as swing zones, making the bootstrap distribution degenerate; or an arithmetic error in the SZAT score is identified | §5.2.10; `analysis/scripts/szat.py` |
| Minority seats@50/50 at ensemble p99.99 | **Active** | Phase 4C measured vote attribution (replacing 70/30 blend with observed apportionment) produces a minority-majority seats@50/50 gap opposite in sign, or below 0.005 percentage points at the 70/30 central weight | §5.4.9; H5 in §7; `data/outputs/regional_swing_canonical_ed.json` |
| Chair-flagged anomaly count (minority 3 vs majority 0) | **Active** | Majority-map imagery reveals ≥ 3 geometric anomalies of comparable severity (lasso, corridor, or COI-splitting shape) flagged by the commission chair or identified independently | §5.8.2, §5.9.4; chair's published majority report annotations |
| Airdrie 4-way vs 2-way split | **Active** | The minority map's Airdrie split configuration is matched by an equally-fragmented treatment of a comparable Alberta city in the majority map | §5.3.2; §5.8 |
| Rationale-failure rate (5 of 6 contested configurations) | **Active** | Internal commission documents — pre-dating the final report — are published showing the disputed configurations were derived from documented community submissions rather than drafting discretion; or an independent analyst constructs a constraint-legal counter-map satisfying the minority's stated COI rationales while achieving ≥ 60% CSD/DA edge alignment | §5.9.4; §6.2.6 condition 1 |
| Minority EG at ensemble p94.4 | **Withdrawn flag** | Flag already retracted: 1M canonical run places minority EG at p94.4, below the p95 threshold. EG is directional evidence only; the outlier-flag is not asserted | §5.4.9 |

---

## Findings retracted under H1-H10 stress-test protocol

These findings were held during the DPG-era analysis, were stress-tested in the H1-H10 hypothesis battery (§7 hypothesis tests), and did not survive. They are recorded here, not deleted, per the DOCUMENTED CORRECTIONS convention.

| Hypothesis | Retracted claim | What falsified it |
|---|---|---|
| H1 | 2M-step MCMC ensemble, minority seats@50/50 at p100 (no neutral plan reaches it) | The chain orchestration silently re-seeded from the 2019 baseline at every 20k-step chunk boundary; the "2M-step run" was structurally 100 independent 20k-step bursts. Bug fixed in commit `73544a3`. Canonical ensemble replaces this result. |
| H2 | Minority seats@50/50 = 52.8% (published headline) | VA-dissolve coverage was 83/89 districts, not 89/89; 6 districts were effectively unscored. Corrected value is 48.3% (commit `7cf47a4`). |
| H4 | Municipal anchoring: minority 14.5%, majority 71.0%, 4.9× asymmetry | Did not survive canonical recomputation against official Elections Alberta shapefiles. Canonical: minority 72.0%, majority 80.0%; both within the 70–85% Canadian comparator norm. Retracted per the §4.1.4 DPG sunset clause. Full reconciliation in §5.8.5. |

---

## Provisional findings under active replication

These findings are directional observations that have not been pre-registered and have not been independently replicated. They are reported as exploratory evidence but should not be cited as confirmed findings.

| Finding | Status | What would confirm it |
|---|---|---|
| Minority seats@50/50 at p65–70 under regional swing (vs p99.99 under uniform) | Exploratory (H5) | Independent replication using a different regional-swing parameterisation reaching the same range |
| SZAT 2019→minority score = +0.016 (p=0.053, marginally outside null) | Exploratory | Pre-registered replication against November 2026 Lunty-committee map (OSF:qsgy8) |
| Submission-archive support-inversion on 3 of 7 minority configurations | Exploratory | IRR validation at κ ≥ 0.60 on 60 stratified samples (blocked pending human annotation) |

---

## Source

§7.2 (Falsifiability statement); §6.2.6 (What would change the author's verdict); H1-H10 hypothesis battery (§7 hypothesis tests).
