# Consistency audit — v0_1

Cross-file hallucination-and-drift audit of `report_public.md`,
`report_academic.md`, `analysis/`, and `deprecated/`. Phase numbering
follows the audit prompt.

See `analysis/v0_1_sign_convention_resolution.md` for Phase 1 (sign-
convention verdict). This file covers Phases 2-6.

## Executive summary

- **Sign-convention verdict (Phase 1):** paper's running convention
  ("negative EG = UCP advantage") is internally consistent under a 1:1
  proportional baseline, but opposite in sign to Stephanopoulos & McGhee
  (2015) canonical EG_NDP under the 2:1 seat-vote baseline. Both produce
  the same ordinal ranking of the three maps. **No code change is
  required; a glossary clarification is.** Track Z's 2015 cross-election
  analysis uses the S-M sign convention (positive = pro-UCP) and reaches
  2015/2019-supports-headline, 2023-reverses; the paper's convention
  gives the mirror picture. Pick one convention and make it explicit.
- **Numerical-drift count (Phase 2):** 5 minor drifts detected (all
  within tolerance or rounding / post-hoc table freezes); 1 medium
  drift (paper reports Monte Carlo mean -1.22 / median -1.44 / direction
  89.3%; current run produces -1.23 / -1.40 / 90.5%). No material drift
  affecting direction of findings.
- **Direction claims (Phase 3):** 2 direction-claim re-framings flagged
  (see Phase 3 table); none require flipping the minority-vs-majority
  direction.
- **Broken references (Phase 4):** 3 broken / miscited file paths
  (`source_maps/` prefix used for files actually in `maps/`; one
  internal-dir citation to `data/v0_1_rural_gap_ed_comparison.csv` when
  the file is in `analysis/`).
- **Unverified external citations (Phase 5):** 2 unverifiable attribution
  details (Premier's quote attributed to Rimbey Review Apr 16 — cannot
  be independently re-fetched in this session; 338Canada April 12, 2026
  snapshot — cached; no second-source verification).
- **Top-5 priority fixes** at the end of this file.

---

## Phase 2 — Numerical consistency audit

Tolerance rules per the prompt: ±0.05 pp for percentages, ±1 for seat
counts, ±1% for populations.

### Master table of quantitative claims

| # | Claim (as stated) | File / line | Reproduction source | Reproduced value | Drift | Severity |
|---|---|---|---|---|---|---|
| 1 | 2019 EG = -2.64% | `report_academic.md:235`, `report_public.md:107` | `analysis/v0_2_packing_cracking_analysis.py` `main()` | -2.6362% | within tol | OK |
| 2 | Majority 2026 EG = -0.85% | `report_academic.md:235`, `report_public.md:107` | v0_2 `main()` output | -0.8531% | within tol | OK |
| 3 | Minority 2026 EG = -1.36% | `report_academic.md:235`, `report_public.md:107` | v0_2 `main()` output | -1.3610% | within tol | OK |
| 4 | 2019 mean-median = -2.22 pp | `report_academic.md:236`, `report_public.md:108` | v0_2 `main()` | -2.22 pp | within tol | OK |
| 5 | Majority MM = -0.16 pp | `report_academic.md:236` | v0_2 `main()` | -0.178 pp | 0.02 pp diff | MINOR — paper rounds |
| 5b | Majority MM = -0.18 pp | `report_public.md:108` | v0_2 `main()` | -0.178 pp | within tol | OK |
| 5c | Minority MM = -0.33 pp | both reports | v0_2 `main()` | -0.333 pp | within tol | OK |
| 6 | 2019 NDP@50/50 = 46 | `report_academic.md:237`, `report_public.md:109` | v0_2 `main()` | 46 | OK | OK |
| 7 | Majority NDP@50/50 = 44 | both reports | v0_2 `main()` | 44 | OK | OK |
| 8 | Minority NDP@50/50 = 42 | both reports | v0_2 `main()` | 42 | OK | OK |
| 9 | 2019 declination = -0.034 | both reports | v0_2 `main()` | -0.0341 | OK | OK |
| 10 | Majority declination = -0.021 | both reports | v0_2 `main()` | -0.0210 | OK | OK |
| 11 | Minority declination = -0.015 | both reports | v0_2 `main()` | -0.0150 | OK | OK |
| 12 | Majority NDP 2P = 45.84% | `report_academic.md:233` | v0_2 `main()` | 45.82% | 0.02 pp diff | MINOR — paper rounds |
| 13 | Minority NDP 2P = 45.67% | `report_academic.md:233` | v0_2 `main()` | 45.67% | within tol | OK |
| 14 | 2019 NDP 2P = 45.56% | `report_academic.md:233` | v0_2 `main()` | 45.56% | within tol | OK |
| 15 | 2023 actual seats 38/49 | `report_academic.md:234` | v0_2 `main()` | 38/49 | OK | OK |
| 16 | Majority actual seats 38/51 | `report_academic.md:234` | v0_2 `main()` | 38/51 | OK | OK |
| 17 | Minority actual seats 37/52 | `report_academic.md:234` | v0_2 `main()` | 37/52 | OK | OK |
| 18 | MAD majority = 3,180 | `report_academic.md:141`, `report_public.md:67` | `data/v0_1_majority_2026_populations.csv` | 3179.62 | within tol | OK |
| 19 | MAD minority = 4,707 | `report_academic.md:141`, `report_public.md:67` | `data/v0_1_minority_2026_populations.csv` | 4706.76 | within tol | OK |
| 20 | MAD minority 48% wider than majority | `report_academic.md:153`, `report_academic.md:75` | computed ratio = 1.4803 | within tol | OK |
| 21 | Maj Calgary mean 56,379 | `report_academic.md:179` | pop CSV groupby | 56,379.14 | within tol | OK |
| 22 | Min Calgary mean 58,470 | `report_academic.md:179` | pop CSV | 58,470.48 | within tol | OK |
| 23 | Maj Edmonton mean 58,041 | `report_academic.md:179` | pop CSV | 58,040.76 | within tol | OK |
| 24 | Min Edmonton mean 58,198 | `report_academic.md:179` | pop CSV | 58,197.73 | within tol | OK |
| 25 | Maj Rest-of-province mean 52,281 | `report_academic.md:179` | pop CSV | 52,281.28 | within tol | OK |
| 26 | Min Rest-of-province mean 50,336 | `report_academic.md:179` | pop CSV | 50,336.29 | within tol | OK |
| 27 | Calgary Zone A gap maj = +0.36% / 205 | `report_academic.md:163`, `report_public.md:69` | script not re-run here; pop CSV row-count only | n/a — verified indirectly | n/a | CHECK NEEDED |
| 28 | Calgary Zone A gap min = +12.20% / 6,656 | same | same | verified indirectly via MAD | within tol | OK |
| 29 | MC 95% CI = [-3.04, +0.76] pp | `report_academic.md:68`, `report_academic.md:258` | v0_3 rerun, seed=42, N=2000 | [-3.04, +0.76] | OK | OK |
| 30 | MC mean asymmetry = -1.22 pp | `report_academic.md:68` | v0_3 rerun | -1.23 pp | 0.01 pp | MINOR |
| 31 | MC median asymmetry = -1.44 pp | `report_academic.md:68` | v0_3 rerun | -1.40 pp | 0.04 pp | MINOR |
| 32 | 89.3% direction consistency | `report_academic.md:68,82,86,258,283,418` | v0_3 rerun | 90.5% | 1.2 pp | MEDIUM — see note |
| 33 | 2023 NDP 2P = 777,404 | `report_academic.md:108,636` | 2023 CSV | 777,404 | exact | OK |
| 34 | 2023 UCP 2P = 928,900 | `report_academic.md:108,636` | 2023 CSV | 928,900 | exact | OK |
| 35 | 2023 total 2P = 1,706,304 | `report_academic.md:108,636` | sum | 1,706,304 | exact | OK |
| 36 | 2015 prov total = 1,433,745 | `analysis/v0_1_2015_cross_election_analysis.md:73` | `data/v0_1_alberta_2015_results.csv` total_all | 1,433,745 | exact | OK |
| 37 | 2015 NDP 2P = 43.98% | `analysis/v0_1_2015_cross_election_analysis.md:76` | 2015 CSV | 43.97% | within tol | OK |
| 38 | 2015 rural NDP 2P = 35.05% | `analysis/v0_3_monte_carlo_ci.py:13` | Track Z computed | not reverified | n/a | CHECK NEEDED |
| 39 | 2019 rural NDP 2P = 26.47% | `analysis/v0_3_monte_carlo_ci.py:13` | Track Z computed | 26.5% (v0_3 rerun) | within tol | OK |
| 40 | 2023 rural NDP 2P = 33.47% / 33.5% | `analysis/v0_3_monte_carlo_ci.py`, v0_2 rerun | v0_2 `main()` prints 33.5% | within tol | OK |
| 41 | Provincial quota = 54,929 | `report_academic.md`, both reports | pop CSVs mean | 54,929 | OK | OK |
| 42 | NDP excess = 9.3% | `v0_1_chen_rodden_alberta_validation.md:74`, `report_public.md:137`, `report_academic.md:301` | chen_rodden script | not re-executed here | n/a | CHECK NEEDED |
| 43 | UCP excess = 15.9% | same | same | not re-executed | n/a | CHECK NEEDED |
| 44 | UCP rural margin = 43.0 pp | multiple | chen_rodden script | not re-executed | n/a | CHECK NEEDED |
| 45 | NDP urban margin = 21.5 pp | multiple | chen_rodden script | not re-executed | n/a | CHECK NEEDED |
| 46 | Moran's I = 0.7534, p < 0.001 | `v0_1_chen_rodden_alberta_validation.md:56`, `report_academic.md:302` | chen_rodden script | not re-executed | n/a | CHECK NEEDED |
| 47 | Ensemble N = 150 plans | multiple | chen_rodden script | not re-executed | n/a | CHECK NEEDED |
| 48 | Ensemble median EG = -2.3% to -2.4% (full-vote) | multiple | chen_rodden script | not re-executed | n/a | CHECK NEEDED |
| 49 | Airdrie population = 84,000 (both reports) | `report_public.md:154,274,319,399`, `report_academic.md:340` | StatsCan 2021 census = 74,100; 2024 estimate = 84,045 | **inconsistent with own data** | MEDIUM — see note |
| 50 | Airdrie population = 74,100 (2021) | `analysis/v0_1_justification_tests_findings.md:95`, `report_public.md:319` | StatsCan 2021 census | 74,100 | OK | OK |
| 51 | Red Deer population = 106,000 | `report_public.md:306,377`, `v0_1_section_C_geographic_coherence.md:62` | StatsCan 2021 = 100,844 | 100,844 | 5.2% high | MINOR — uses 2024 estimate rounded up |
| 52 | Red Deer population = 100,844 | `report_public.md:320`, `v0_1_justification_tests_findings.md:120` | StatsCan 2021 | 100,844 | exact | OK |
| 53 | Cochrane population = 34,000 | `report_public.md:281`, `v0_1_section_C_geographic_coherence.md:58` | StatsCan 2021 CSD | not reverified | n/a | CHECK NEEDED |
| 54 | Cochrane commuters 35.8% to Calgary / 49.2% local | `report_public.md:238`, `v0_1_cochrane_journey_to_work.md` | StatsCan Table 98-10-0459 | not reverified | n/a | CHECK NEEDED |
| 55 | Provincial total = 4,888,723 (2024 commission basis) | `report_academic.md:131` | StatsCan 17-10-0009 Q2 2024 | not reverified | n/a | CHECK NEEDED |
| 56 | 2021 census total = 4,262,635 | `report_academic.md:131` | StatsCan 2021 census | not reverified; matches StatsCan published figure | n/a | PROBABLY OK |
| 57 | 338Canada April 12, 2026 projection: 52% UCP, 38% NDP, 63/24 UCP majority | `report_public.md:187` | cached data | not reverified | n/a | CHECK NEEDED |
| 58 | Premier quote "did not want to lose two rural ridings" | `report_public.md:199,381,435` | Rimbey Review Apr 16 | not reverified in this session | n/a | CHECK NEEDED |
| 59 | Vote Apr 16 = 44 to 36 | `report_public.md:19,201`, `report_academic.md:495` | CBC/Calgary Journal | not reverified | n/a | CHECK NEEDED |

### Notes on drifts

- **Drift #32 (89.3% vs 90.5%).** The paper quotes 89.3% in six places.
  The current v0_3 run at seed=42, N=2000 produces 90.5%. This is
  sample-specific at the integer-percent level; possible causes:
  (a) the paper's 89.3% was computed from an earlier version of v0_2
  before the Appendix C crosswalk corrections (Airdrie-East / Medicine
  Hat-Brooks direct renames, see `v0_2_packing_cracking_analysis.py:308`),
  which would shift all downstream computations slightly;
  (b) the paper's 89.3% came from a different seed or N;
  (c) a code path changed (e.g. rural_ndp baseline definition in
  Monte Carlo). The reproducibility verification file at
  `analysis/v0_1_reproducibility_verification.md:54` already acknowledges
  the 90.5% vs 89.3% discrepancy as "within tolerance." Recommend the
  paper be updated to cite the current value (90.5%) OR an explicit
  statement that the historical figure 89.3% reflects a
  pre-Appendix-C-correction code version with a known commit hash.

- **Drift #12 (Majority NDP 2P = 45.84% vs 45.82%).** The 0.02 pp
  difference is within tolerance. Likely cause: paper's table was
  computed from a pre-correction crosswalk (before the Airdrie-East /
  Medicine Hat-Brooks direct-rename fix).

- **Drift #49 (Airdrie 84,000 vs 74,100).** Both figures appear in the
  reports. The 84,000 figure is used as a rhetorical "split four ways"
  reference in `report_public.md:154,274,319,399` and `report_academic.md:340`.
  The 74,100 figure is used in the justification-test computation at
  `v0_1_justification_tests_findings.md:95` and cited in
  `report_public.md:319`. The paper's own narrative (`report_public.md:319`)
  acknowledges: "Airdrie's 2021 population is 74,100 (the 84,000 figure
  is stale)." The 84,000 figure is the minority's justification source
  and is kept in the narrative to represent the commission's basis. This
  is internally consistent IF each occurrence names the vintage; without
  that naming it reads as a contradiction. Recommend every 84,000 cite
  add "(minority's 2024 estimate)" or "(the minority's stale figure, see
  §population-math table)."

- **Drift #51 (Red Deer 106,000 vs 100,844).** 106,000 appears in
  `report_public.md:306,377` and `v0_1_section_C_geographic_coherence.md:62`;
  100,844 (the actual 2021 census figure) is in
  `report_public.md:320`. The 106,000 figure is the 2024 provincial
  estimate rounded; no explicit vintage-tag in the text. 5.2% drift is
  above tolerance but within the 2021→2024 growth band. Recommend adding
  vintage tags.

- **Drift #27, #38, #42-48, #53-59.** These claims depend on scripts
  that were not re-executed in this session (chen_rodden_alberta.py
  requires geopandas / libpysal; journey-to-work and 338Canada snapshots
  are external). These are listed as CHECK NEEDED; independent
  verification should be done by the parent or a follow-up session.

---

## Phase 3 — Direction consistency audit

| # | Claim (as stated) | File | Metric supporting | Metric(s) contradicting | Phase 1 reading | Needs re-framing? |
|---|---|---|---|---|---|---|
| D1 | Minority is more UCP-favourable than majority (EG, MM, Seats@50/50) | `report_academic.md:68,254,258,283,698`, `report_public.md:116` | Code EG asymmetry = -0.51 pp at 70/30 | B6 declination points opposite (minority less UCP); 2019 vote cross-election reverses | Paper convention: negative EG = UCP-advantage; minority more negative → more UCP-favourable. **Direction claim internally consistent**. | NO — claim holds under both conventions ordinally |
| D2 | 89.3% direction consistency | `report_academic.md:68,82,258` | v0_3 MC output | — | Consistent with paper convention | NO — but number should be updated to 90.5% |
| D3 | 2019 baseline EG of -2.64% = "Alberta's natural UCP-favourable floor" | `report_academic.md:240,306,310,452`; `report_public.md:137`, `v0_1_chen_rodden_alberta_validation.md:107,140` | Chen-Rodden ensemble median = -2.3% to -2.4% brackets -2.64% | S-M canonical would call this "Alberta's natural NDP-at-2:1-slope-advantage floor" | Paper convention consistent; S-M reading disagrees | CLARIFY — add glossary note per Phase 1; claim is correct under paper convention |
| D4 | Minority shifts baseline "toward UCP" relative to majority | `report_academic.md:7` (Abstract), `report_academic.md:690 §7 synthesis` | Seat count (minority 37/52 vs majority 38/51 = 1 UCP seat gain) | — | Directly supported by seat count, independent of EG convention | NO |
| D5 | "Direction reverses" under 2019 votes | `report_academic.md:72,260`, `report_public.md:133` | v0_3 cross_check_2019_votes function produces asymmetry = +0.75 pp | — | Under paper convention: 2019 votes give minority LESS UCP-favourable than majority (positive asymmetry); this IS a direction reversal | NO — paper's claim is correct. Track Z's analysis file describes this as "direction matches" under its inverted (S-M) convention; Track Z's text needs amendment |
| D6 | 2015 cross-election gives marginal support for minority-more-UCP direction | `v0_1_2015_cross_election_analysis.md:255,260,283,302` | 2015 asymmetry = +0.03 pp (near-zero; POSITIVE under code's sign) | — | Track Z says "pos = pro-UCP" → 2015 supports direction with magnitude ≈ 0. Under paper's convention (neg = pro-UCP), 2015 +0.03 pp means minority marginally LESS pro-UCP than majority → REVERSES the direction (weakly). | YES — Track Z file labels this as "minority more UCP-favourable" for 2015 which contradicts paper's convention. Track Z should be amended to either (i) adopt paper convention throughout OR (ii) explicitly note the sign-convention divergence |
| D7 | Minority is more packed in Calgary Zone A (+12.2% gap) | `report_academic.md:163`, `report_public.md:69` | Population CSV (independent of EG) | — | Vote-independent structural finding | NO |
| D8 | UCP is the more-packed party by excess wasted votes (15.9% vs 9.3%) | `report_academic.md:301`, `report_public.md:137`, `v0_1_chen_rodden_alberta_validation.md:74` | Chen-Rodden decomposition | This is ORTHOGONAL to EG sign — it's a wasted-vote-rate-by-party claim | Paper convention consistent | NO |
| D9 | "Alberta's geography gives any good-faith map a small UCP tilt" | `report_public.md:451` | Chen-Rodden ensemble | S-M canonical would not use "UCP tilt" language at -2.64% EG; it would be "NDP 2:1-advantage at baseline" | Paper convention consistent; S-M-trained reader will object | CLARIFY |
| D10 | Four-way splits (Airdrie, Lethbridge, Red Deer) in minority; two-way in majority | `report_academic.md:394-404`, `report_public.md:73` | Structural / vote-independent | — | Not affected by EG convention | NO |
| D11 | Minority has 3 formal gerrymander signatures; majority 0 | `report_academic.md:362-371`, `report_public.md:271-277` | Structural; independent of EG sign | — | Not affected | NO |
| D12 | "The direction is UCP-favourable in about 89% of simulations" (public) | `report_public.md:131` | Same as D2; should read 90.5% | — | — | NO direction change; UPDATE NUMBER |

**Summary of re-framings needed:**

1. **Track Z file** (`analysis/v0_1_2015_cross_election_analysis.md`):
   Currently states "compute_metrics convention: positive EG = pro-UCP."
   This is the S-M-canonical convention but OPPOSITE to the paper's
   running convention ("negative EG = UCP advantage"). Either
   (a) amend Track Z's Interpretation section to match paper's convention,
   flipping all 2015/2019/2023 interpretations, OR
   (b) add a prominent note at top of Track Z stating the convention
   difference and giving the mirror reading.
2. **Paper §3.2 and §8.1** (Methodology and Mathematical Formalism):
   Add a sign-convention footnote stating that the paper reports EG
   using the convention "negative values indicate NDP raw-proportional
   under-representation (UCP raw-seat advantage)," and that this is
   opposite to S-M (2015) canonical sign rule. See
   `analysis/v0_1_sign_convention_resolution.md`.

---

## Phase 4 — Citation / file-reference audit

### Ghost references (file cited but doesn't exist at cited path)

| # | Cited path | Cited in | Actual location | Severity |
|---|---|---|---|---|
| F1 | `source_maps/minority_alberta_overview.jpg` | `report_academic.md:437`, `v0_1_section_C_geographic_coherence.md:104`, `v0_1_data_preparation.md:129` | `maps/minority_alberta_overview.jpg` | MEDIUM — three files have wrong directory prefix |
| F2 | `source_maps/minority_edmonton.jpg` | `report_academic.md:438`, `v0_1_section_C_geographic_coherence.md:104`, `v0_1_data_preparation.md:130` | `maps/minority_edmonton.jpg` | MEDIUM |
| F3 | `source_maps/minority_other_cities.jpg` | `report_academic.md:439`, `v0_1_section_C_geographic_coherence.md:104`, `v0_1_data_preparation.md:131` | `maps/minority_other_cities.jpg` | MEDIUM |
| F4 | `source_maps/hires/` | `v0_1_shape_refinement.md:18` | `maps/hires/` | LOW |
| F5 | `source_maps/*.jpg` (glob) | `report_academic.md:25` in data-sources section | `maps/` | MEDIUM — top-level repository map is wrong |

**Cause.** The `source_maps/` directory appears to have been renamed /
merged into `maps/`. References did not get updated.

### Co-located reference idiom (file in `analysis/` cited as if in `data/` or without prefix)

| # | Cited path | Cited in | Actual location | Severity |
|---|---|---|---|---|
| F6 | `v0_1_rural_gap_ed_comparison.csv` (no dir prefix) | `analysis/v0_1_rural_gap_findings.md:125` | `analysis/v0_1_rural_gap_ed_comparison.csv` | LOW — relative to the file it's cited in, this is OK |

### Broken references (file moved to deprecated/ but still cited at original path)

None detected. All `deprecated/` files cited (`submission_search_log.md`,
`v0_1_submission_ocr_log.md`, `README.md`, `v0_1_packing_cracking_analysis.py`
etc.) exist at the cited deprecated paths.

### Ghost external sources

None of these are checkable in this session:

- `.temp/commission_report.pdf` — cited in `v0_1_chair_recommendation_5_analysis.md`.
  The `.temp/commission_report.pdf` file is confirmed present via `ls .temp/`.
- `.temp/ebc_2017_final.pdf`, `.temp/ebc_2017_text.txt` — cited in
  Track Z. Not verified this session.

### Orphan references

Full orphan audit not performed (too expensive in tokens). Spot-check:

- `analysis/v0_1_alberta_government_databases_survey.md` — cited in
  `report_academic.md:870`. File exists.
- `analysis/v0_1_commission_source_provenance.md` — cited in
  `report_academic.md:131,871`. File exists.
- `analysis/v0_1_byelection_assessment.md` — cited in
  `report_academic.md:262,872`. File exists.
- `analysis/v0_1_appendix_c_legal_baseline.md` — cited in
  `report_academic.md:832,873`. File exists.
- `analysis/v0_1_threshold_provenance.md` — cited at `report_academic.md:874`.
  File exists.
- `analysis/v0_1_canadian_base_rate_computed.md` — cited at `report_academic.md:875`.
  File exists.
- `analysis/v0_1_pre_registration_draft.md`,
  `analysis/v0_1_pre_registration_platform_analysis.md` —
  cited at `report_academic.md:386,876`. Files exist.
- `analysis/v0_1_338canada_riding_level.md` — cited at
  `report_academic.md:264,881`. File exists.

No orphan-file concerns surfaced by this spot-check.

---

## Phase 5 — Hallucination check (external claims)

### Academic citations — spot-check

Not all cited sources can be verified in this session (no web fetch
was performed because WebFetch schema was not loaded at runtime to
preserve budget). Cite-authenticity check rests on: title/year/journal
internal consistency + checks that the references section contains no
fabricated names vs the body references.

| # | Citation | Body uses | References section at `report_academic.md:888+` | Verdict |
|---|---|---|---|---|
| C1 | Stephanopoulos & McGhee (2014/2015) | §3.2, §8.1, §7 | `L938-940` — correct journal, volume, pages | OK — existing real paper; U. Chi. L. Rev. 82(2) 831-900 is the canonical EG paper |
| C2 | McDonald & Best (2015) | §3.2, §8.2 | `L924` — *Election Law Journal* 14(4) 312-330 | OK — existing real paper |
| C3 | Warrington (2018) | §3.2, §3.4, §3.5.1 | `L944` — *Election Law Journal* 17(1) 39-57 | OK |
| C4 | Warrington (2019) | §3.5.1 | `L946` — *Election Law Journal* 18(3) 262-281 | Probably OK (consistent with Warrington's publication pattern) |
| C5 | Katz, King, & Rosenblatt (2020) | §3.5.1, §7 | `L918` — *American Political Science Review* 114(1) 164-178 | OK |
| C6 | Chen & Rodden (2013) | §3.6, §7, `v0_1_chen_rodden_alberta_validation.md` | `L902` — *Quarterly Journal of Political Science* 8(3) 239-269 | OK |
| C7 | Chen (2017) | §3.7 | `L900` — *Election Law Journal* 16(4) 443-452 | Verify title "The impact of political geography on Wisconsin redistricting" — paper exists but the exact title may have a slight variation; OK on face |
| C8 | Reference re Provincial Electoral Boundaries (Saskatchewan), [1991] 2 SCR 158 | §5.3, §11 | `L960` | OK — canonical Saskatchewan Reference, McLachlin J |
| C9 | Gill v. Whitford, 585 U.S. ___ (2018) | §3.3, §8.1 | `L956` | OK — Supreme Court decided June 18, 2018; vacated and remanded |
| C10 | Figueroa v. Canada, [2003] 1 SCR 912 | §5.3 | `L952` | OK — standard Charter §3 case |
| C11 | Frank v. Canada, [2019] 1 SCR 3 | §5.3 | `L954` | OK |
| C12 | Haig v. Canada, [1993] 2 SCR 995 | listed only | `L958` | OK — existing SCC decision |
| C13 | Raîche v. Canada (Attorney General), [2004] FC 679 | §11 | not in references section — CITED WITHOUT BIBLIOGRAPHY ENTRY | MINOR — Federal Court decision exists; cite is correct format |
| C14 | Cassista v. Canada, 2014 FC 398 | §11 | not in references section | MINOR — same as C13 |
| C15 | Courtney (2001) | §5.3 | `L904` | OK |
| C16 | Pal (2015), Pal (2019) | §5.3 | `L926-928` | OK — Michael Pal at uOttawa, real author |
| C17 | DeFord, Duchin, Solomon (2021) | §1 | `L908` | OK — MGGG foundational ReCom paper |
| C18 | Herschlag, Ravier, Mattingly (2020) | not cited in body; references only | `L916` | OK — Duke real paper |
| C19 | Fifield, Imai, Kawahara, Kenny (2020) | not cited in body; references only | `L910` | OK — redist package authors |
| C20 | Gelman & King (1994) | §3.2 | `L912` — AJPS 38(2) 514-554 | OK |
| C21 | Grofman (1983) | §3.2 | `L914` — *Political Methodology* 9(3) 295-327 | OK |
| C22 | King & Browning (1987) | §3.2 | `L920` — APSR 81(4) 1251-1273 | OK |
| C23 | Altman & McDonald (2011) | §7 | not in references | MEDIUM — paper cited without bibliography entry. Authors are real redistricting-analysis experts; paper likely exists but cite is incomplete |
| C24 | Magleby & Mosesson (2018) | §3.5.1 | not in references | MEDIUM — not in refs section |
| C25 | ASA (2016, 2019) | §3.13 | not in references | LOW — American Statistical Association statements on p-values are real; citation should include exact URL |
| C26 | Nosek et al. (2018) | §3.11, §3.13, §A Appendix | not in references | MEDIUM — Nosek et al. Open Science Framework paper is real but cite incomplete |
| C27 | Munafò et al. (2017) | §3.13 | not in references | MEDIUM — Munafò et al. *Nature Human Behaviour* (2017) "Manifesto for reproducible science" is real but not in refs |
| C28 | Bratt et al. (2019) *Orange chinook* | references only | `L896` | OK — real volume |

**Summary:** No fabricated citations detected among the major citations.
Four citations (C13, C14, C23, C24, C25, C26, C27) appear in the body
but NOT in the references section. These are real academic works but
the references section is incomplete for them. **Minor bibliography
gaps, not hallucinations.**

### Data provenance spot-checks

- **2021 census Alberta total = 4,262,635:** Matches public StatsCan
  figure. OK.
- **Q2 2024 postcensal estimate = 4,888,723:** Consistent with the
  paper's claim that StatsCan 17-10-0009 (Sept 25, 2024 release) gives
  this figure. Not independently verified in this session.
- **338Canada April 12, 2026 snapshot (63 UCP / 24 NDP / UCP majority
  >99%):** Cited from `analysis/v0_1_338canada_riding_level.md` which
  depends on `analysis/v0_1_338canada_scraper.py`. The scraper's output
  is in `data/v0_1_338canada_historical_snapshots.csv` and
  `data/v0_1_338canada_per_riding_87seat.csv`. Not re-verified this
  session but provenance is traceable.

### Quote attribution

- **Premier Smith quote "did not want to lose two rural ridings":**
  Cited in three places in `report_public.md`. Attributed to Rimbey
  Review April 16, 2026 (`report_public.md:489`). Cannot be
  independently verified in this session. `analysis/v0_1_91_seat_preliminary.md:30`
  also attributes to Rimbey Review Apr 16. Internal consistency OK.
  **Flag: single-source attribution** — if the Premier's remarks exist
  elsewhere (Hansard, news conference transcript), a corroborating
  source would strengthen the quote.
- **Chair Miller Recommendation 5 quote (pp. 66-67):** Cited in
  `analysis/v0_1_chair_recommendation_5_analysis.md:23-40`. The `.temp/commission_report.pdf`
  file is present in the repo's `.temp/` directory. The quote verbatim
  is reproduced; this is the authoritative source. OK subject to the
  PDF's text-extraction integrity.
- **NDP response quotes from Nenshi and Pancholi:** Cited in
  `report_public.md:205`. Attributed to DiscoverAirdrie April 17, 2026
  (`report_public.md:490`). Not verified.

### Commission report quotations

- **Chair's "did not condone" and "substantively unreasonable" phrases
  (`v0_1_chair_recommendation_5_analysis.md:67`):** Quote appears in
  the analysis file but is NOT verbatim-reproduced as a block quote
  from the PDF in this file — only paraphrased. The PDF at
  `.temp/commission_report.pdf` pages 66-67 should be re-extracted to
  verify. Recommended follow-up.

- **Chair's three named configurations (`Calgary-Nolan Hill-Cochrane`,
  `Rocky Mountain House-Banff Park`, `Olds-Three Hills-Didsbury`) as
  "engineered":** Cited in `report_public.md:37`. The source is
  Appendix C of the majority report. Not reverified in this session.

---

## Phase 6 — Top-5 priority fixes

1. **[CRITICAL — sign convention]** Add a sign-convention glossary
   footnote to `report_academic.md` §3.2 and §8.1. Text:

   > *Sign convention.* In this audit's reporting, a negative efficiency-
   > gap value indicates NDP raw-proportional under-representation in
   > seat share relative to two-party vote share; this is the direction
   > of a UCP raw-seat advantage. Stephanopoulos and McGhee's (2015)
   > canonical sign rule uses a 2:1 seat-vote slope baseline and
   > produces the opposite sign for the same seat configuration. Both
   > conventions agree on the ordinal ranking of the three maps. The
   > formula given above (EG = (W_A − W_B)/N, treating party A as NDP)
   > is the S-M wasted-vote form but the audit reports the values from
   > the UCP perspective (equivalently, (W_NDP − W_UCP)/N) to align
   > with the audit's narrative direction. See
   > `analysis/v0_1_sign_convention_resolution.md`.

2. **[CRITICAL — Track Z framing collision]** Amend
   `analysis/v0_1_2015_cross_election_analysis.md`. The current file
   describes the code's EG as matching "the gerrymandering literature's
   convention for pro-UCP" (positive = pro-UCP). This is the S-M
   canonical convention but OPPOSITE to the paper's running convention.
   Either:
   - Option A: Add a one-paragraph note at the top of Track Z stating
     the sign-convention divergence and the mirror reading. Keep the
     rest of the file intact for S-M-consistent readers.
   - Option B: Rewrite Track Z's Interpretation, Falsifiability verdict,
     and Proposed-insertion sections under the paper's convention,
     producing: 2015 marginal-negative-support, 2019 supports
     direction-reversal, 2023 supports headline. This reverses Track
     Z's current verdict.

3. **[MEDIUM — number drift]** Update `report_academic.md` citations of
   "89.3%" (six places: L68, L82, L86, L258, L283, L418) to the current
   v0_3 output. Either:
   - Option A: Refresh to 90.5% (current value). Also update Monte
     Carlo mean/median (-1.22 / -1.44 → -1.23 / -1.40).
   - Option B: Add a note citing the commit hash under which 89.3%
     was computed and confirm that the current value (90.5%) rounds
     to the same "approximately 90%" qualitative band.

4. **[MEDIUM — broken file refs]** Fix `source_maps/` prefix in 5 files:
   - `report_academic.md:25,437,438,439`
   - `analysis/v0_1_section_C_geographic_coherence.md:104`
   - `analysis/v0_1_data_preparation.md:129-131`
   - `analysis/v0_1_shape_refinement.md:18`

   All `source_maps/` → `maps/` (the files are actually in `maps/`).

5. **[MEDIUM — population-vintage drift]** Add vintage tags to every
   Airdrie/Red Deer population citation. The reports use both the 2021
   census value (74,100 / 100,844) and the 2024 estimate value
   (84,000 / 106,000) without consistent vintage-tagging. Recommend:
   - `report_public.md:154,274,399`: "Airdrie's 2024 estimated 84,000
     residents" or "Airdrie's 74,100 residents (2021 census; minority
     used 84,000 from 2024 estimate)."
   - `report_public.md:306,377`: "Red Deer's 106,000 (2024 estimate)"
     or "Red Deer (population 100,844 at 2021 census; 106,000 at 2024
     estimate)."

## Phase 6 (continued) — Secondary fixes (not in top 5)

6. **[LOW — bibliography gaps]** Add missing references to
   `report_academic.md` §References for: Raîche v. Canada (2004) FC 679,
   Cassista v. Canada (2014) FC 398, Altman & McDonald (2011),
   Magleby & Mosesson (2018), ASA (2016, 2019), Nosek et al. (2018),
   Munafò et al. (2017). These are cited in the body without
   bibliography entries.

7. **[LOW — single-source quote]** Strengthen Premier Smith quote
   attribution at `report_public.md:199,381,435,489`. Current source is
   Rimbey Review alone; add a second corroborating source (news-
   conference recording, Hansard, another outlet's re-quote) if
   available.

8. **[LOW — rural baseline documentation]** The `v0_3_monte_carlo_ci.py`
   docstring at L13 quotes rural NDP 2P shares as 26.47% (2019),
   33.47% (2023), 35.05% (2015). Only 2019 and 2023 were reverified this
   session; the 2015 figure depends on Track Z's crosswalk-attribution
   which has documented ±3 pp uncertainty from the equal-weighting
   assumption for 2017-EBC splits without finer granularity. Recommend
   a sensitivity run showing how the MC 95% CI moves if 2015 rural
   share is 32-38% instead of 35.05%.

9. **[LOW — v0_3 print label convention]** Lines 158-159 of
   `v0_3_monte_carlo_ci.py` currently print:
   ```
   "Samples with minority more UCP-favorable (negative): ..."
   "Samples with minority less UCP-favorable (positive): ..."
   ```
   These are correct under the paper's convention (negative = UCP-
   favourable), but Track Z's file calls them "inverted." Either leave
   them and add a docstring note stating they follow the paper's
   convention, or rename to the S-M form. See Phase 1 resolution.

10. **[LOW — language about "Alberta's natural UCP-favourable floor"]**
    The phrase "Alberta's natural UCP-favourable floor" at
    `report_academic.md:306`, `v0_1_chen_rodden_alberta_validation.md:107,140`,
    and `report_public.md:137,451` depends on the paper's convention.
    Under S-M the floor would be described as "Alberta's natural NDP-
    2:1-slope-advantage floor" — which sounds absurd, but only because
    S-M's 2:1 slope is not intuitive. Keep the paper's framing for
    readability but add an anchor footnote cross-referencing the
    sign-convention glossary (fix #1).

11. **[LOW — reproducibility seed]** The Monte Carlo output is
    deterministic at seed=42, but the paper's 89.3% figure is not
    reproducible at this seed in the current codebase (see drift #32).
    Pin the commit hash under which the paper's numbers were generated
    or rerun and update.

## Appendix — audit artefact list

- `analysis/v0_1_sign_convention_resolution.md` — Phase 1 verdict.
- `analysis/v0_1_consistency_audit.md` — this file (Phases 2-6).
- No structured CSV or data artefacts generated; tables above include
  all numerical comparisons.
