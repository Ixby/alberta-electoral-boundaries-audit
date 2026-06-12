---
title: T1.7 Round 2 — 18-Referee Verification Review (results)
date: 2026-06-12
status: COMPLETE — triage published; round-3 remediation queued
commit_reviewed: ea38b1c
review_model: claude-fable-5 (18 parallel adversarial agents, verification round)
predecessor: analysis/review/t1_7_18_referee_results_2026_06_12.md (round 1)
---

# T1.7 Round 2 — 18-Referee Verification Review

Same 18 specialties re-dispatched against HEAD `ea38b1c` after the round-1 remediation (commits `c9a9fbd`..`ea38b1c`). Mandate: verify round-1 fixes landed, find errors the remediation itself introduced, find anything missed.

**Headline: the core fixes are verified clean, but the remediation introduced ~18 new errors and left ~25 stale sites unswept.** The declination code fix, chain-CSV flip, and published percentiles reproduce exactly (Ref #5: PASS). The BH table arithmetic is hand-verified correct (Refs #1, #6). But the remediation pattern was "fix the flagged site, miss the siblings" — and several correction notes contain errors of their own.

## Class 1 — Errors INTRODUCED by the round-1 remediation

| # | Refs | Where | What went wrong |
|---|---|---|---|
| N1 | 18, 4, 15 | `preregistration/november_2026_scoring_spec.md:98` | **Self-invalidating hash pin.** SHA-256 `34097af2…` was recorded *inside the file being hashed*, then the file was edited again same session (§1 fix). Current hash `759ccc9c…`. A self-referential pin can never verify. Worse: §6 claims a `seed_commitments.md` entry that was never created, cites "Amendment 11" that has no log entry, and misattributes all three commit hashes (true chain per `git log --follow`: 2cd4b21 → 4781c70 → c12c7c8 → d9c3520). |
| N2 | 4, 15 | `data/simulation_checkpoints_canonical/chain*_samples.csv` @ c9a9fbd | **Lossy unscripted migration.** The Amendment 10 flip silently truncated EVERY float column from 17 to ~15-16 significant digits (pandas default repr round-trip) across 1.01M rows, while the commit message and amendment log claim only declination changed. No migration script committed; no pre/post SHA-256 manifest. Old 44MB blobs remain packed (+33MB repo bloat). |
| N3 | 2 | `data/outputs/simulated_ensemble_raw_samples_canonical.csv`, `data/outputs/simulation_real_map_scores_canonical.json` | **Migration incomplete at the data layer.** Two other canonical declination stores were never flipped (pooled CSV mean −0.00246 = old sign; real-map JSON still −0.0770). `joint_outlier_score.json` still records old-sign values. Any consumer mixing the flipped chains with the unflipped stores gets direction-inverted percentiles (p0.92 vs p98.79). `cross_election.py:178` is a duplicate unfixed declination implementation. |
| N4 | 2, 5, 15 | `analysis/scripts/mcmc_ensemble.py:216-220` | **Double-flip landmine.** The new comment says historical chain CSVs "must be negated downstream" — false at birth, since the same commit negated them in place. A maintainer obeying the comment double-flips. |
| N5 | 6, 14, 16, 17 | `report_academic.md:269, 642, 906, 1628, 1780`; `report_public.md:271, 273, 275` | **"4-of-4" conflates direction with tail.** Amendment 10 licenses "all four agree on direction"; EG sits at p94.4, below the p95 flag line, so tail/flag agreement is 3-of-4. §6.2.1:2421 says so itself. RT7's "Flagged pass on 4 of 4" is the worst instance. |
| N6 | 6 | `report_academic.md:1102, 1109` (§5.2.9) | **Proportionality Deviation row fabricated.** The values I wrote (+0.0079/+0.0058/+0.0064) match neither the canonical JSON (0.0237/0.0271/0.0252) nor any source; my ranking sentence is wrong — minority is largest, not 2019. |
| N7 | 11 | `report_academic.md:1197` (C3) | **C3 correction arithmetically wrong twice.** "24.7%" should be 25.0%; and the vintage ladder fails at both ends — Airdrie 74,100 (2021) > 68,661 ceiling so it's 2-district minimum at EVERY vintage (not "single-district feasible at 2021"); 3-way at 2025 (30,015 each) is below the 41,197 floor so "three-district-permissible" is wrong. C1 one bullet up states the correct fact — the fix created an internal contradiction. |
| N8 | 10 | `analysis/methodology/canonical_shapefile_log.md:22-28` | **CRS correction wrong in every particular** (verified via pyproj): 3400 = 10-TM *Forest*, 3401 = 10-TM *Resource* (the correction swapped them); both k₀=0.9992 (the claimed 0.9999 belongs to 3TM); the two differ only by false easting, so the asserted "~0.07–0.14% area difference" is fictitious. Real hazard (500 km easting shift on un-reprojected mixing) unstated. Also "three-zone 3775-3777" → four zones 3775-3778; `report_academic.md:121` still claims "Alberta 3TM, EPSG:3776". |
| N9 | 13 | `report_academic.md:370` | **Growth correction wrong for its endpoint.** "~10%" is the 2021→Q2-2024 figure; the sentence's endpoint says mid-2025, which is ~13% (5.02M / 4,442,879). |
| N10 | 12 | `report_academic.md:2063` | **Sentiment "182/1,252" overcorrection.** The progress CSV shows 1,254 unique submission IDs processed (silence ≠ unprocessed; rows only emitted for non-Unrelated). The round-1 fix propagated the completion report's unsupported "CRITICAL GAP" claim, converting a true coverage claim into a false one. The completion report is the unreliable artifact. |
| N11 | 8 | `report_academic.md:3027` | **New fabricated style of cause:** "*Carter v. Saskatchewan* [1991] 2 SCR 158" — no such case; it's *Reference re Prov. Electoral Boundaries (Sask.)*. Plus broken "§2.x" placeholder cross-ref. |
| N12 | 8 | `report_academic.md:318` | **"Kelen J." unverified** — may repeat the Heneghan error (referee's recollection: Shore J.; no reachable source confirms). Delete the named-judge parenthetical. |
| N13 | 9 | `report_academic.md:302` | **Rucho rewrite introduced two errors:** "139 S. Ct. 2484 was the slip-opinion reporter" is false (it's West's Supreme Court Reporter, a valid parallel cite); and *Whitford* plaintiffs lost on Article III standing (Gill), not "threshold justiciability" — conflated with Rucho. |
| N14 | 9 | `report_academic.md:927` | **White Burgess case name mangled:** "*White Burgess v. Halifax Regional Municipality*" → correct: *White Burgess Langille Inman v. Abbott and Haliburton Co.*, 2015 SCC 23 (line 3018 of same file has it right). |
| N15 | 2 | `findings/pre_registration_amendment_log.md:404` | **Amendment 10's 2019-enacted row splices substrates:** −0.034 sits at old-p18.46; the p8.95 belongs to the canonical JSON value −0.04509 (correct corrected row: +0.0451 at p91.05). Minority/majority rows verified exact. |
| N16 | 1 | `TODO_REMEDIATION.md:424, 443` (T1.9) | **T1.9's empirical-floor claim statistically wrong:** (b+1)/(B+1) over 1.01M autocorrelated draws requires exchangeability; honest ESS-bounded floor ≈ 6.7×10⁻⁴, which cannot "dominate" the parametric 1.4×10⁻⁶. |
| N17 | 10 | `report_academic.md:254` | **"Well wider than any reasonable contiguity-filter correction" indefensible:** minority margin to the 70% floor is 2.0 pp; the filter is monotone-decreasing and nothing in-repo bounds the correction below 2 pp. Asserted, never computed. |
| N18 | 2 | `report_academic.md:1304` + TODO | "Queued as T1.4-eps" — dangling reference; the actual queue item is T1.11. Also "every proposal already satisfies ±12.5%" overstated: the initial partition is built at full ε, so 12.5–25% districts persist until redrawn (asymptotic, not absolute). |

## Class 2 — Round-1 fixes incompletely swept (stale siblings)

| # | Refs | Where | Stale content |
|---|---|---|---|
| S1 | 1, 5, 16 | `report_academic.md:1567-1655, 2378, 2421, 2549, 2896-2916 (App D.3), 1339, 1415, 1684` | **Pre-Amendment-10 declination throughout the authoritative §5.4.9/5.4.10 tables, §6.2 verdict text, and Appendix D.3** — which §4.1.4 explicitly cites as the convention documentation and which asserts "there is NO sign-flip relative to Warrington." The asymmetric-packing narrative builds on NDP-tail declination while §1.2 claims UCP-tail: opposite signs of the same metric in one document. |
| S2 | 17 | `report_academic.md:1775` (RT2) | RT2 still says "B6 declination opposes… 3-of-4 mixed" — Amendment 10 upgrades it to 4-of-4 same sign. Selective refresh: RT3/RT7 regraded, RT2 left stale. |
| S3 | 1, 14, 17 | `report_academic.md:240, 304, 491, 518, 553, 555, 567, 2356, 2360`; `report_public.md:281`; `SESSION_HANDOFF.md:8`; dependency-graph dot/json/svg | "Independent" survives at 10+ sites including line 553 ("m = 11 independent tests") directly contradicting line 538 in the same subsection, and §4.4's Fisher endorsement via the ρ=−0.0014 check that §4.3.2 itself declares invalid. |
| S4 | 3 | `report_academic.md:271, 400, 646` (§1.2 caveat 3 / §3.3 / gate 4) | **Cross-election claims still v0_8-based and contradicted by the audit's own canonical Option C** (§5.2.8: 2019 EGs Majority −1.32% / Minority −0.49%, both NDP-favourable). "Neither map's EG sign flips under 2019" is false on canonical data; gate 4's "caveat is retracted" must itself be retracted. |
| S5 | 3 | `report_academic.md:1776` (RT3 row — my round-1 regrade) | My regrade cites the retracted v0_7 "+0.30/+0.90%" values and falsely claims "no canonical 2019 ensemble computed" — Option C IS one (100k canonical, seed 3562959107, Maj p48.3 / Min p70.4). |
| S6 | 7 | ~10 sites incl. `report_academic.md:752, 1222, 1306`; scripts | Phantom file `s15_2_reaudit.md` still cited (real: `population_deviation_reaudit.md`); §5.1.5 now cites the correct name while §5.1.4 cites the phantom — same doc, two names. Plus a new dangle: `minority_rationales_validation.md` missing its `reference/` path segment. |
| S7 | 7, 11 | `report_academic.md:750/766/786/1218 + 1210/1216/1236/1847` | W4: criterion (b) borderline (~143–145 km < 150 strict nearest-boundary per the audit's own reaudit §7) still suppressed in "5/5" headline. W5/E2: line 1210 still opens "**Detected.**"; "three formal signatures" not demoted at 3 sites; line 1847 counts E2 unqualified. |
| S8 | 11 | `report_academic.md:2389` | §6 still claims "the ±25% band permits a single-ED draw" for Airdrie (1.56× quota — illegal). Contradicts corrected C3. |
| S9 | 13 | `report_academic.md:378, 388`; `findings/cycle_lag_analysis.md` | Retracted 14.69% survives twice; Peerless Trout comparison reverses when annualized; Plan B flip counts (5/87, 0/89, 5/89) embed the ~4.2 pp universe artifact; Plan B still non-reproducible (missing script/files). |
| S10 | 12 | `report_public.md:44`; `november_2026_scoring_spec.md:93` | Bratt "cabinet" mischaracterization persists in public report (Assembly Motion 19, 44–36 — academic report has it right). |
| S11 | 8, 12 | `report_academic.md:2152, 2156-2162, 2737` | Cassista unbannered at 2 of 4 sites; Quebec "holdings" still styled as holdings with posture-based inferences; April 22+6 days date inconsistency. |
| S12 | 9 | `report_academic.md:310, 963, 1065, 1329, 1337, 1474, 2413, 2751` | "MGGG lawsuit-grade" at 3 more sites; "Chen-Rodden (2013) identity" at 963; line 310's "S-M proposed a 7% threshold" contradicts corrected §5.2.8; Best et al. 2018 cited with no bibliography entry; Rucho reference entry lacks the U.S. parallel cite. |
| S13 | 4 | `findings/t3_2_majority_rural_isolation.md:11, 41` + `analysis/scripts/t3_2_majority_rural_isolation.py:43` | T3.2 result file still says "pre-committed design" (no exploratory banner); the design doc's amended Airdrie classifier was never executed — the script still has hyphen-sensitive `"Airdrie-"`, so the frozen design misdescribes the published run. |
| S14 | 5 | `docs/report_academic.html`, `docs/report_public.html`, `docs/index.html`, `docs/REPRODUCING.md:124` | Public HTML builds and REPRODUCING.md all pre-Amendment-10 (serve p1.21 NDP-tail; reproducer following REPRODUCING.md "fails" to reproduce). |
| S15 | 6 | `report_public.md:156, 264, 273` | Stale "5 of 5 structural" claims survive the anchoring retraction (correct: 4 of 5). |
| S16 | 17 | `report_academic.md:2356, 2363` | §6 "None individually crosses a statistical significance threshold" now false post-canonical (MM p99.98, Decl p98.79, s50 p99.99 all > p95). |
| S17 | 16 | `report_academic.md:2454, 2471` (§6.2.4/§6.2.5) | Verdict text still framed on retired Readings A/B and superseded v0_8 numbers (EG +9.21% p100) that line 1628 itself marks superseded. |
| S18 | 14 | `report_public.md:216, 235` | Round-1 carry-overs never fixed: "strategically… engineers the exact structural firewall" (intent assertion) and "systematically dismantles the standard alternative defenses" (litigation rhetoric). |
| S19 | 1, 16 | `report_academic.md:533 vs 865/1646` | BH row 8 majority MM p0.85 vs canonical p0.92 — value drift across sections. |
| S20 | 4 | `report_academic.md:76` (abstract) | Abstract still lists 6pt83 + #289,469 as "prospective pre-registered" — contradicted by §4.3.2's own disclosure (6pt83 post-dates the shapefile commit; #289,469 filed with results known). |
| S21 | 17 | `TODO_REMEDIATION.md:29` (T1.1) | The original "wider than" arithmetic error survives in the T1.1 caveat — fixed in the findings doc, not the queue. |
| S22 | 12 | `report_academic.md:2106, 2068` | Published sentiment row breakdown (271/85/96) doesn't match the canonical CSV (263/85/103 + 1 blank); 292 vs 182 vs 1,254 coverage unreconciled. |
| S23 | 16 | `report_academic.md:56, 2421, 2460, 2473` | Screening/confirmatory firewall relabeled but not enforced: p ≤ 2.80×10⁻⁶ deployed verdict-bearing in §6.2 and abstract without exploratory qualifiers. |
| S24 | 16 | `report_academic.md:1590-1606, 2430, 2443-2445` | Severity asymmetry (round-1 D25) untouched: commission-constraint auxiliary excuses majority outliers but is never applied to minority tails. T1.17 queued but §6.2.3 "majority crosses no threshold" contradicts §6.2.2's own bolded majority MM outlier. |
| S25 | 10 | `report_academic.md:1883, 1909, 2941-2949` | §5.8.5 + footnote still claim the ≥1 km contiguity filter is implemented; Appendix D.4/D.5 still present retired v0_7 compactness tables as live (including the retracted Enoch-Devon 0.0652), with canonical direction *reversed*. |

## Verified clean (no action)

- Declination code fix + chain-CSV flip + three published percentiles reproduce exactly (Ref #5).
- §1.1 BH table arithmetic, monotone step-up, dependence disclosure (Refs #1, #6 — independently hand-verified).
- §5.2.1 advance-vote footnote; MC-error caveat; Lopsided directional caveat (Ref #6).
- FINDINGS_BRIEF chair-verdict fix; P(data|neutral) public rewrite (Refs #14, #16).
- §5.1.5 verbatim s.15(2) text; 2017 Bielby attribution (Ref #7).
- §5.8.4 Enoch-Devon rewrite vs canonical PP (Ref #10).
- Raîche holding substance at both sites (Ref #8 — judge attribution excepted).
- §5.2.8 EG-threshold provenance; LWV v PA cite (Ref #9).
- Amendments 5-7 reconciliation entry (Ref #4).
- Public-report Airdrie "constraint minimum: 2" already correct (Ref #11).

## Round-3 priority ordering

1. **N1-N4 (provenance/data-layer)** — the self-invalidating spec pin, the lossy CSV migration, the unflipped sibling stores, and the double-flip comment are the audit's worst current exposure: they are exactly the "silent data manipulation" profile a hostile reviewer alleges, and they're fully fixable: regenerate CSVs from c9a9fbd^ blobs at full precision via a checked-in script, flip the two sibling stores, regenerate joint_outlier_score.json, fix the comment, author Amendment 11 properly, re-pin the spec hash *externally* (seed_commitments.md).
2. **S1 (Amendment 10 sweep)** — one systematic pass over every declination site: §5.4.9/5.4.10 tables, §6.2, Appendix D.3, RT2, line 1415, docs/ HTML rebuild, REPRODUCING.md, cross_election.py, methodology docs.
3. **N5 + S15/S16/S17 (verdict-surface consistency)** — settle the "direction 4/4, tail 3/4" formula everywhere; §6.2.5 onto canonical numbers.
4. **N6-N17 (point corrections)** — each is a one-site fix.
5. **S4/S5 (cross-election)** — rewrite §1.2 caveat 3, §3.3, gate 4 and RT3 from Option C canonical.
6. **Remaining S-items** — mechanical sweeps.
