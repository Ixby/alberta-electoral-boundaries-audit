# Alberta Electoral Boundaries Audit — Academic and Legal Edition

**A symmetric, reproducible forensic assessment of the 2025–26 Electoral Boundaries Commission's majority and minority recommendations**

*Draft — April 2026 · Non-partisan · [Repository](https://github.com/Ixby/alberta-electoral-boundaries-audit) · Data and scripts linked throughout*

**Author and audit design:** Will Conner, Mount Royal University, BSc Computer Information Systems (4th year student)

## Tools Used in the Academic Analysis

**Computational stack:**
- **Python 3.14** on Windows 11 (Python 3.9+ required by `setup.sh`; 3.14 used in this session)
- **pandas 2.x** — Section A population equality analysis, Section B vote attribution
- **numpy** — numerical computation underpinning pandas
- **openpyxl** — parsing the 2023 Statement of Vote Excel workbook (87 sheets, 1,973 poll records)
- **geopandas + pyogrio** — spatial operations for population aggregation and ED-to-CSD overlay; full Phase 4/5 execution blocked on 2026 shapefile release
- **shapely + pyproj** — polygon topology and projection (NAD83 / Alberta 3TM, EPSG:3776)
- **osmnx** — OSM road network extraction (prepared for Phase 4D fallback)
- **gerrychain** — MCMC ensemble generation (prepared for Phase 5 ensemble test; blocked by shapefile availability)
- **pdfplumber** — PDF table extraction for commission report and Appendix E parsing
- **geopy + rapidfuzz** — geocoding and fuzzy-string matching

**Data sources:**
- Elections Alberta Statement of Vote 2023 (`data/2023_results.xlsx`; `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx`)
- Alberta Electoral Boundaries Commission final report, March 23, 2026 — extracted populations and variance tables (`data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv`); map images (`maps/*.jpg`)
- Elections Alberta GIS resources page (`https://www.elections.ab.ca/resources/maps/`) — checked for 2026 shapefiles (not yet published)
- Statistics Canada 2021 Census Dissemination Area populations and shapefiles (`data/alberta_2021_da_populations.csv`, `data/alberta_2021_das.gpkg`)
- Alberta Treasury Board Office of Statistics and Information quarterly population estimates
- StatsCan Table 17-10-0009 quarterly provincial population estimates
- StatsCan Table 98-10-0459 (2021 Census journey-to-work by CSD)

**Version control and distribution:**
- **git** — full commit history preserved in the repository
- **GitHub CLI (gh)** — repository creation and remote configuration
- **GitHub public repository:** [Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit)

**Code authored for this audit:**
- `analysis/v0_2_packing_cracking_analysis.py` — symmetric three-map partisan-bias pipeline
- `analysis/electoral_forensics_population.py` — population-equality analysis (A1/A2/A3)
- `analysis/v0_3_monte_carlo_ci.py` — Monte Carlo confidence-interval ensemble
- `analysis/v0_1_a1_legal_baseline_2021_census.py` — 2021-census-direct A1 computation for 2019 EDs
- `analysis/v0_1_majority_symmetry_counter_test.py` — symmetry-of-test-selection counter-test
- `analysis/v0_1_cochrane_journey_to_work.md` — journey-to-work commute analysis
- `analysis/v0_1_csd_community_splits.py` — CSD-level community-splits overlay
- `analysis/v0_1_338canada_scraper.py`, `analysis/v0_1_338canada_reallocate.py` — 338Canada per-riding integration

**Integrity tools applied:**
- Falsifiability gates G0–G5 built into the pipeline
- Bias self-audit documented at `analysis/v0_1_bias_audit.md`
- Uncertainty analysis at `analysis/v0_1_uncertainty_and_shapefile_impact.md`

**Tools NOT used:**
- No traditional statistical software (R, Stata, SPSS)
- No GIS desktop software (QGIS, ArcGIS)
- No commercial election-analytics platforms
- No paid datasets; all inputs are public

---

Data and scripts: `analysis/*.py`, `data/*.csv`, `data/2023_results.xlsx`

---

## Stress-Test Preamble

Three modelling-uncertainty tests materially narrow the partisan-bias magnitude claim while leaving structural findings intact. These are reported up-front for transparency; the underlying methodology is in `analysis/v0_1_design_critique.md` and the Monte Carlo script `analysis/v0_3_monte_carlo_ci.py`.

**1. Monte Carlo 95% CI over modelling choices crosses zero.** N=2,000 samples varying urban weight (0.55–0.85), rural baseline (0.26–0.36), and per-hybrid jitter (±0.10). Minority-majority EG asymmetry: mean −1.22 pp, median −1.44 pp, **95% CI [−3.04, +0.76] pp**. Direction consistency: 90.5% of samples show minority more UCP-favorable. Classical 95% significance is **not** defensible; a directional observation at approximately 90% confidence is the reportable finding.

**2. Declination metric (Warrington, 2018) disagrees with the efficiency gap.** Declination computed: 2019 = −0.034, Majority = −0.021, Minority = −0.015. By declination, the minority is the least pro-UCP of the three maps, the opposite direction from EG and the seats-at-50/50 estimate. Warrington (2018) documents this kind of cross-metric divergence as an expected feature of competing formalisations rather than a methodological flaw; Katz, King, and Rosenblatt (2020) recommend ensemble reporting. Both metrics are retained; neither is dispositive on its own.

**3. 2019 cross-election check reverses the EG asymmetry.** Running identical methodology with 2019 vote totals (instead of 2023) produces Majority EG +0.30%, Minority EG +0.90%, asymmetry **+0.60 pp** (minority less UCP-favorable). The direction of the headline asymmetry flips sign depending on which election's votes are used as input. The observed asymmetry is not a stable property of the maps alone; it is an interaction between the maps and 2023-specific voter distribution patterns. The direction does replicate under 338Canada's April 2026 polling input (see §3.5), suggesting stability across 2020s-era political geography but not across the 2019 electorate.

**What survives these tests unchanged:**
- §A1 population distribution variance (CSV-sourced, election-independent): minority MAD is 48% wider than majority.
- §A2 Calgary geographic-zone gap: minority 7.7–12.2%; majority 0.36–0.39%. Not vote-based.
- §C3 visual spatial anomalies: 3 minority anomalies confirmed on published maps.
- §C4 community splits: Airdrie 4 vs 2, Cochrane merged vs intact, Chestermere partial split vs intact.
- §D procedural concerns: government-controlled replacement of drafting process, qualitative.

**What is narrowed:**
- §B partisan-bias *magnitude* claims. The point estimate of 0.58 pp is within Monte Carlo noise. The direction holds at 90.5% confidence across modelling uncertainty, which is a defensible directional claim but not classical 95% significance.
- The "minority gives UCP 2 more seats in a tied election" line. Under Monte Carlo, minority NDP@50/50 has 95% CI [41, 47] vs majority [43, 46] — overlapping. The 1-seat structural asymmetry is robust across 2023 votes and April 2026 polling as distinct inputs; the magnitude CI crosses zero.
- "Directionally consistent across six dimensions" is more precisely "directionally consistent across five of six tested dimensions, with one partisan-bias metric (declination) pointing the opposite way."

**Defensible synthesis.** The minority 2026 proposal shows measurable structural differences from the majority in four areas: population distribution (MAD 48% wider), Calgary geographic-zone balance (12.2% gap vs 0.4%, robust across two classification rules), community-of-interest treatment (Airdrie split across 4 EDs vs 2, with the same pattern visible in Lethbridge and Red Deer — see §3.12), and visible boundary shape (three confirmed anomalies). None of these depend on vote data. The partisan-bias consequences are directionally UCP-favorable for the minority in 90.5% of modelling-jitter samples using 2023 vote attribution and in a 1-seat replication against April 2026 polling, but inverted under 2019 vote attribution. The core claim is that the minority has more structural irregularities than the majority; a specific partisan-seat-shift magnitude is less defensible and sensitive to election baseline. The procedural concern about the April 16 government action stands separately from the partisan-math questions.

---

## Abstract

This audit evaluates two competing 2026 electoral boundary proposals against the 2019 baseline currently in force in Alberta. Six dimensions are examined using public data and identical methodology applied to all three maps: (A) population equality, (B) partisan-bias metrics from the political-science literature, (C) visual geographic coherence, (D) procedural fairness, (4) geometric data provenance, and (5) MCMC ensemble comparison. Where data permit, the two 2026 proposals are shown to diverge systematically: the minority proposal exhibits wider population dispersion (MAD 4,707 vs 3,180), a 12.2% Calgary geographic-zone asymmetry vs the majority's 0.4%, three visible spatial anomalies flagged by the commission chair himself, fragmentation of Airdrie across four electoral divisions vs the majority's two, and a 0.6–1.6 percentage point more UCP-favorable efficiency gap under identical modeling methodology (sensitivity-tested across urban-weight parameters 0.60, 0.70, 0.80). Partisan-bias metrics remain within the 7% efficiency-gap threshold used in *Gill v. Whitford* (2018) for all three maps. The directional consistency of the minority's shift across six independent analytical dimensions — and the procedural departure of April 16, 2026 rejecting the majority recommendation in favor of a UCP-majority MLA committee drafting process — together support a finding of systematic partisan asymmetry at a magnitude below the US statistical-significance threshold but above the noise floor of non-partisan redistricting variance. Sections 4 (geometry) and 5 (MCMC ensemble) are blocked pending ABEBC release of 2026 polygon shapefiles.

**Key phrase for citation:** *"Non-gerrymander at the US judicial threshold; directionally-consistent partisan asymmetry across six independent dimensions at the sub-threshold level."*

---

## 1. Methodology and Integrity Framework

### 1.1 Symmetry requirement

Every test applied to one map is applied identically to the others. Where a data gap prevents symmetric application, the gap is disclosed explicitly and the claim's scope is narrowed to what is symmetric.

### 1.2 Falsifiability gates

Each analytical stage produces a PASS/FAIL gate value before propagating downstream. Gates implemented:

- **G1 (carry-forward verification):** B1–B4 on 2019 baseline must reproduce the four-figure match to official totals (NDP 777,404 / UCP 928,900, two-party 1,706,304). Reproducible via `python3 analysis/v0_2_packing_cracking_analysis.py`.
- **G2 (2026 estimate count):** Each map's ED estimate set must contain exactly 89 districts; total valid votes within 5% of 1.7M; NDP share within [0.40, 0.50]. `validate_2026_estimate()` in `v0_2_packing_cracking_analysis.py`.
- **G3 (Calgary classification coverage):** A2 test requires zero residual unclassified Calgary EDs. Enforced programmatically in `a2_calgary_analysis()`.
- **G4 (A2 robustness):** A2 directional finding must survive alternative classification (2023 winner-based) or be flagged as classification-dependent. `a2_robustness_check()` implements the alternative.
- **G5 (Sensitivity range):** B2 efficiency gap computed under urban weights 0.60, 0.70, 0.80. Direction must be consistent across all three; magnitude range is reported, not a single point estimate.

### 1.3 What does not enter the report

- Any number not reproducible by running a checked-in script against checked-in data
- Any classification rule without a robustness check under at least one alternative
- Any language characterizing one map's features with stronger modifiers than the other's when the underlying facts are comparable
- Any "the numbers confirm X" framing in section preambles

### 1.4 Author disclosure

The author (Will Conner) is a fourth-year BSc Computer Information Systems student at Mount Royal University. Going into this project, the author held the prior that the UCP government's handling of boundary redistribution warranted scrutiny. The methodology is designed to produce the same numbers regardless of that prior. Three specific cases in the analysis surfaced findings that ran against the author's prior and were retained in the report: (i) under 2019 vote input the partisan-bias asymmetry reverses sign (§3.5); (ii) the commission chair's "no public support" claim is upheld on three of seven configurations, not all seven (§5.4); (iii) the majority map's own A1 MAD of 3,180 is tighter than the 2019 current-map baseline computed on 2021 census data (Appendix C), indicating the commission's majority did not introduce partisan looseness. The bias self-audit is at `analysis/v0_1_bias_audit.md`.

---

## 2. Population Equality (Section A)

### 2.1 Distribution variance (A1)

**Data-basis preamble.** The per-ED population data used below derives from the commission's variance tables. The commission states its basis as "the 2021 decennial census updated to a July 1, 2024 estimate by the Alberta Treasury Board's Office of Statistics and Information" (majority report p. 29; minority report p. 296, verified extraction in `analysis/v0_1_commission_source_provenance.md`). The provincial total used by the commission for quota derivation is 4,888,723, which matches Statistics Canada's Q2 2024 postcensal estimate for Alberta (Table 17-10-0009, released September 25, 2024) to the person, because the OSI sub-provincial estimates nest inside the StatsCan provincial control. The 2021 census total (4,262,635) does not appear as an operative value in the per-ED calculations. Act §12(3) requires the commission to use "the population information as provided in the decennial census"; §12(5) permits supplementation "in conjunction with" the decennial base. Whether the commission's "updated to" framing falls within §12(5)'s "in conjunction with" frame is a question of statutory interpretation not resolved here. The Plan B cross-check (`analysis/v0_1_plan_b_cross_check.md`) verifies that every §A verdict below is identical whether computed against the 2021 census directly, the 2024 OSI estimate (commission's basis), or the 2025 TBF estimate. The A1 MAD figures are computed on the commission's stated basis; they are intended for apples-to-apples comparison with the commission's own published variance tables. A 2021-census-direct A1 computation on the 87 current 2019 EDs, provided as Appendix C, serves as a §12(3)-operative reference point. The equivalent computation for the 2026 proposals is blocked by the non-release of 2026 shapefiles.

Per-ED population data loaded via `pandas` in `analysis/electoral_forensics_population.py`.

| Metric                                   | Majority 2026 | Minority 2026 |
| ---------------------------------------- | ------------- | ------------- |
| N districts                              | 89            | 89            |
| Mean population                          | 54,929        | 54,930        |
| Median population                        | 55,791        | 55,713        |
| Standard deviation                       | 5,301         | 6,533         |
| Mean absolute deviation (MAD) from 54,929 | 3,180         | 4,707         |
| Maximum positive deviation               | +14.28%       | +24.06%       |
| Maximum negative deviation               | −47.72%       | −45.36%       |
| EDs above +10% from mean                 | 5             | 15            |
| EDs above +15% from mean                 | 0             | 5             |
| EDs above +20% from mean                 | 0             | 3             |
| EDs above +25% (statutory violation)     | 0             | 0             |
| EDs below −10% from mean                 | 5             | 13            |
| EDs below −15% from mean                 | 4             | 5             |
| EDs below −20% from mean                 | 4             | 4             |
| EDs below −25% (requires s.15(2))        | 3             | 3             |

The minority's MAD is 48% wider than the majority's. Neither exceeds the ±25% statutory cap. Both use all three permitted s.15(2) exceptions. The key distributional observation is the asymmetric positive tail: the minority has 5 districts above +15% and 3 above +20%, none of which the majority has.

### 2.2 Calgary geographic-zone asymmetry (A2)

Classification rule: Zone A comprises Calgary EDs whose territorial centroid lies north or east of a dividing line running along the Bow River through downtown and then southeast along Deerfoot Trail. Zone B comprises EDs south or west of that line. The classification is documented in source (`CALGARY_ZONE_A`, `CALGARY_ZONE_B` in `electoral_forensics_population.py`) with no residual unclassified Calgary EDs. The partisan correlation of these zones (Zone A ≈ NDP-competitive, Zone B ≈ UCP-dominant) is a property of voter geography, not of the classification itself.

| Zone                                      | Majority (n / mean pop) | Minority (n / mean pop) |
| ----------------------------------------- | ----------------------- | ----------------------- |
| Zone A (N / E / central Calgary)          | 17 / 56,460             | 17 / 61,225             |
| Zone B (S / W Calgary)                    | 11 / 56,255             | 12 / 54,569             |
| Gap (Zone A − Zone B)                     | +205 (+0.36%)           | +6,656 (+12.20%)        |

**Robustness check (G4).** Re-running the test with a purely data-driven rule — Calgary EDs classified by the party that won them in 2023, mapped forward to 2026 by name-stem match — reproduces the directional finding:

| Rule                                  | Majority gap | Minority gap |
| ------------------------------------- | ------------ | ------------ |
| Geographic (Zone A vs Zone B)         | +0.36%       | +12.20%      |
| Data-driven (2023-NDP-won vs -UCP-won)| +0.39%       | +7.71%       |

Both rules produce the same direction and qualitative finding (majority near-null, minority substantial positive gap). The magnitude varies (7.71–12.20%) because the two classifications do not overlap perfectly — some EDs in Zone A were UCP-won in 2023 and vice versa. The audit reports the range rather than a single number; the lower bound (7.71%) is the conservative estimate.

### 2.3 Urban–rural regional breakdown (A2b)

| Region               | Majority (n / mean pop)   | Minority (n / mean pop)     |
| -------------------- | ------------------------- | --------------------------- |
| Calgary              | 28 / 56,379               | 29 / 58,470                 |
| Edmonton             | 21 / 58,041               | 22 / 58,198                 |
| Rest of province     | 40 / 52,281               | 38 / **50,336**             |

The minority's rest-of-province mean is 3.9% lower than the majority's. Smaller rural districts produce proportionally more rural seats for the same provincial population; given the 2023 rural Alberta NDP two-party share of 33.5% (observed from the Statement of Vote), smaller rural districts yield net UCP seat gains.

### 2.4 s.15(2) eligibility audit (A3)

Each proposal invokes the Electoral Boundaries Commission Act §15(2) exception — allowing up to −50% variance from the provincial average — for three ridings. §15(2) requires at least 3 of 5 statutory criteria to be met: (a) area > 20,000 km², (b) > 100 km from a major centre, (c) no town with 4,000+ population in the district, (d) significant Indigenous population or reserves, (e) shared border with another province or the US.

| Riding                                       | Var%   | Criteria met (of 5) | Verdict                 |
| -------------------------------------------- | ------ | ------------------- | ----------------------- |
| Central Peace-Notley (majority)              | −47.7% | 4                   | Pass                    |
| Lesser Slave Lake (majority)                 | −45.4% | 3                   | Pass at minimum         |
| Canmore-Banff (majority)                     | −27.2% | 1                   | Fails 3/5 test          |
| Central Peace-Notley (minority)              | −44.6% | 4                   | Pass                    |
| Lesser Slave Lake (minority)                 | −45.4% | 3                   | Pass at minimum         |
| Rocky Mountain House-Banff Park (minority)   | −30.3% | 2                   | Fails 3/5 test          |

Both proposals have one of three invocations that fails the 3/5 criteria test. Characterization discipline:

- **Canmore-Banff (majority, 1/5):** −27.2% variance is modest for a s.15(2) invocation. Fails (a) with an area well below 20,000 km². Fails (c) with two towns over 4,000 (Canmore ~15,000; Banff townsite ~8,000). (d) limited Indigenous population within boundary. (b) borderline. Only (e) the BC border passes uncontestedly. No specific boundary feature in the published materials was identified as constructed solely to achieve criterion passage; we describe this as a judgment-call on a marginal-variance riding.
- **Rocky Mountain House-Banff Park (minority, 2/5):** −30.3% variance. The ~22,000 km² area criterion is met only through an extension of the boundary through the uninhabited portion of Banff National Park; the extension also provides the shared-border criterion (e). Without the NP extension, the district fails both (a) and (e) and would likely not qualify at all. The commission chair flagged this by name in the majority report. We describe this as a boundary drawn to clear statutory thresholds because two of its three passing criteria depend on a single territorial extension through federal park land.

The characterization difference between the two flagged ridings is grounded in the difference in what's verifiable from published materials: the NP extension is visible on the Alberta overview map; no comparable visible feature for Canmore-Banff was identified in the bundle. If additional evidence surfaces showing Canmore-Banff's boundary was also drawn to achieve its criterion passes, the characterization should be revised to match.

---

## 3. Partisan Bias Metrics (Section B)

Scripts: `analysis/v0_2_packing_cracking_analysis.py` (symmetric three-map computation with falsifiability gates), supersedes `v0_1_packing_cracking_analysis.py` which computed only 2019 and minority.

### 3.1 Methodology

2026 ED-level vote estimates are built by mapping each 2026 ED to its 2019 predecessor(s) using an explicit dictionary (`MAJORITY_2026_MAPPING`, `MINORITY_2026_MAPPING`). Three mapping types:

- `direct`: 2026 ED covers approximately the same territory as a 2019 ED; use 2019 votes directly.
- `blend`: 2026 ED combines a 2019 urban core with rural absorption; blend 2019 core vote with the 2023 observed Rest-of-Alberta NDP share (33.5%) using urban weight 0.70 (applied identically to both maps).
- `merge`: 2026 ED combines two 2019 EDs; weight each part explicitly.

### 3.2 Tests

- **B1:** Vote distribution histogram across 10 margin bins from UCP +25%+ to NDP +25%+. (Descriptive; no formal literature reference.)
- **B2:** Efficiency gap (Stephanopoulos & McGhee, 2014): $\text{EG} = (W_{\text{NDP}} - W_{\text{UCP}}) / N$ where wasted votes include loser votes plus winner votes above the threshold. **Sign convention note.** This audit reports EG using the proportional-seat baseline ("negative EG = UCP advantage" in seat-outcome terms) rather than the Stephanopoulos-McGhee 2:1 slope baseline ("positive EG = first-party disadvantaged"). The two conventions produce the same *ordinal* ranking of the three maps and therefore the same direction of the minority-vs-majority asymmetry, but they label the sign opposite. Full resolution in `analysis/v0_1_sign_convention_resolution.md`; the resolution confirms no minority-vs-majority direction claim requires flipping. Where this paper says "negative EG = UCP-favourable," a reader comparing against S-M literature should invert the sign-of-label, not the finding.
- **B3:** Mean-median gap (McDonald & Best, 2015): $\text{MM} = \bar{v} - \tilde{v}$ for NDP vote share.
- **B4:** Seats-votes under uniform swing to 50/50 provincial share (Gelman & King, 1994; Grofman, 1983).
- **B6:** Declination (Warrington, 2018). Measures the asymmetry between winning-district vote distributions by treating each party's winning districts as a vector and computing the angle between them. See §3.4 for the direction-disagreement finding.

The seat-vote-curve symmetry principle underlying B4 traces to Grofman (1983) and King and Browning (1987), later formalized as a Bayesian estimator by Gelman and King (1994). The efficiency gap and mean-median are two of the most widely-cited partisan-bias metrics in the post-*Gill v. Whitford* literature; Stephanopoulos and McGhee (2018) revisit the efficiency-gap debate and acknowledge the metric's sensitivity to modeling choices, which our Monte Carlo analysis in §3.4 quantifies for the Alberta context. Katz, King, and Rosenblatt (2020) argue that no single metric is dispositive and recommend ensemble approaches, which this audit's stress-test gate RT2 (cross-metric agreement) implements.

### 3.3 Results

| Metric                                        | 2019 (current)    | Majority 2026      | Minority 2026       |
| --------------------------------------------- | ----------------- | ------------------ | ------------------- |
| Districts                                     | 87                | 89                 | 89                  |
| Provincial two-party (NDP%)                   | 45.56%            | 45.84%             | 45.67%              |
| Actual seats (NDP / UCP)                      | 38 / 49           | 38 / 51            | 37 / 52             |
| **B2** Efficiency gap                         | **−2.64%**        | **−0.85%**         | **−1.36%**          |
| **B3** Mean-median gap (NDP)                  | −2.22 pp          | −0.16 pp           | −0.33 pp            |
| **B4** NDP seats at 50/50 uniform swing       | 46                | 44                 | 42                  |
| Asymmetry at 50/50 (|NDP − UCP|)              | 5                 | 1                  | 5                   |

None of the efficiency-gap values cross the 7% threshold from *Gill v. Whitford* (2018). Across the full sensitivity range tested in §3.4 (urban weight 0.60–0.80), the minority-majority asymmetry is negative in every setting: −1.36 pp at 0.60, −0.51 pp at 0.70, −1.61 pp at 0.80. The sign is weight-invariant; the magnitude is not.

**Canadian comparative base rate.** A first-catalogue computation of inter-map partisan-asymmetry magnitude across recent Canadian provincial and federal redistributions is reported in `analysis/v0_1_canadian_base_rate_computed.md` and `data/v0_1_canadian_redistribution_base_rate.csv`. Method uses a seat-share-delta proxy calibrated to Alberta 2025-26 (compression factor ≈0.455, acknowledged approximation). The comparable-cycle sample (n=7 including the Alberta 2025-26 anchor): Federal 2022 Alberta sub-commission, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018, Alberta 2025-26. Distribution: mean proxy ΔEG 0.262 pp, median 0.000 pp, maximum 0.798 pp (Manitoba 2018). The **median Canadian cycle produces zero inter-map partisan-asymmetry**; more than half of sampled cycles produce no projected-winner flip between interim and final recommendations. Alberta 2025-26's 0.51 pp point estimate sits at the 71st percentile of the Canadian distribution, comparable in magnitude to Manitoba 2018 (0.80 pp, rural-to-Winnipeg seat reallocation) and Alberta 2017 (0.52 pp, Lesser Slave Lake restoration). The high-end 1.60 pp from the weight-sensitivity range exceeds the observed Canadian maximum of 0.80 pp in this sample. The defensible statement for this section is therefore: **Alberta 2025-26 is in the minority of Canadian redistribution cycles that produce any inter-map partisan-winner asymmetry; at the low-end point estimate it joins Manitoba 2018 and Alberta 2017 at similar magnitude; at the high-end it exceeds the observed Canadian maximum in this seven-cycle sample.** Limitations: the proxy is calibrated from a single anchor, the sample size is small, and direct per-ED EG computation across all cycles (4–8 hours of crosswalk reconstruction per cycle) remains future work. **Report the weight-conditional range, not the 0.70 point estimate, as the paper's headline.** The 0.70 value is a modelling convention for hybrid-district composition (urban core 70% / rural absorption 30%) applied symmetrically to both 2026 maps; it is not an empirical claim about Election Day vs Vote Anywhere apportionment, which observed at 52.8 / 42.9 in 2023.

### 3.4 Sensitivity (G5)

Efficiency gap under alternative urban weights (holding 2019 vote data and rural baseline constant):

| Urban weight | Majority EG | Minority EG | Asymmetry (Min − Maj) |
| ------------ | ----------- | ----------- | --------------------- |
| 0.60         | +1.58%      | +0.22%      | **−1.36 pp**          |
| 0.70         | −0.85%      | −1.36%      | −0.51 pp              |
| 0.80         | −1.43%      | −3.04%      | **−1.61 pp**          |

Direction is stable across all three weights: minority EG is more UCP-favorable than majority EG under every parameter setting. Magnitude ranges from 0.58 to 1.61 percentage points, with the central (0.70) case at 0.58 pp. **Report the range, not a point estimate**, until measured attribution replaces blending.

### 3.5 Falsifiability gate: asymmetry direction

The minority-majority EG asymmetry is negative (minority more UCP-favorable, under this paper's sign convention) in 90.5% of 2,000 Monte Carlo samples across the parameter space (urban weight 0.55–0.85, rural baseline 0.26–0.36, per-hybrid jitter ±0.10). The 95% confidence interval is [−3.04, +0.76] pp and crosses zero. We report this as a directional observation at approximately 90% confidence and do not assert statistical significance at the conventional 95% threshold. The magnitude claim (specifically 0.5–1.6 pp) does not meet the 95% threshold. The minority-vs-majority seat-count gap is 1 seat under both 2023 Statement-of-Vote data and April 2026 338Canada polling, but historical 338 stability testing shows the *direction* of that 1-seat gap is not invariant across vote inputs (see "338 historical stability" paragraph below). If measured attribution from Phase 4C produces an asymmetry of magnitude and direction inconsistent with 2023-vote attribution, the directional claim is falsified.

**Cross-election contingency.** The asymmetry direction is stable across 2023 Statement-of-Vote data and April 2026 338Canada polling. It reverses sign when 2019 votes are used as input (asymmetry becomes +0.75 pp under 2019 votes, under this paper's sign convention: positive asymmetry = minority less UCP-favourable). Under 2015 votes (attributed to 2019 EDs via the full 2015-to-2019 crosswalk at `data/v0_1_2015_to_2019_crosswalk.csv`), the minority-majority asymmetry is +0.03 pp — essentially zero. The three-election distribution (2015 +0.03 pp, 2019 +0.75 pp, 2023 −0.51 pp under this paper's convention) shows the headline direction is supported only under 2023 vote input; 2019 is a clean reversal; 2015 is a near-neutral reversal. The direction is stable across 2020s-era Alberta political geography (specifically the 2023 Statement of Vote and the April 2026 338Canada polling) but is not stable against the 2019 or 2015 electorates. A hostile reader who substitutes pre-2023 voter distributions for 2023 distributions recovers a result that contradicts the headline. The paper reports this contingency as a property of the finding, not a defect: the boundary effect is sensitive to which electorate is asked, and the audit has tested three Alberta general elections plus one polling snapshot to characterise that sensitivity. Full method for the 2015 extension at `analysis/v0_1_2015_cross_election_analysis.md`.

**Byelection coverage in the 2022–2025 window.** Alberta held six provincial byelections in this interval: Fort McMurray-Lac La Biche (2022-03-15), Brooks-Medicine Hat (2022-11-08), Lethbridge-West (2024-12-18), and Edmonton-Ellerslie, Edmonton-Strathcona, and Olds-Didsbury-Three Hills (all 2025-06-23). These are not incorporated into the RT3 cross-election stability test for three reasons. First, coverage is sparse (6 of 87 EDs, 6.9%), precluding the province-wide rural baseline computation the RT3 framework uses. Second, byelection turnout ran 40–60% of prior general turnout, with voter composition known to skew older and more partisan; this violates the "normal partisan inputs" assumption the three general elections jointly satisfy. Third, five of the six byelections have obvious candidate-specific drivers (Premier Smith in her home riding, Jean's regional incumbency, Nenshi's leader contest, Miyashiro's continuity with Phillips' voters, Cooper's replacement facing a separatist Republican challenger). The one byelection that touches a contested minority configuration is Olds-Didsbury-Three Hills (June 2025), which sits in the minority's proposed "Olds-Three Hills-Didsbury" district. The UCP's −14.2 pp share drop and the Republican Party of Alberta's 17.7% first-contest showing do not change the audit's directional verdict; they marginally support the audit's skepticism that "safe" packed rural EDs are structurally stable, but are too sui generis to upgrade from observation to finding. Full data in `data/v0_1_alberta_byelections_2019_2026.csv`; assessment in `analysis/v0_1_byelection_assessment.md`.

**Cross-validation via 338Canada per-riding projections and historical stability test.** *Caveat — two-model compounding.* 338Canada's per-riding projections are themselves a regional demographic model weighted by polling aggregation; reallocating them through the hybrid crosswalks stacks a second model layer. 338's model accuracy against the 2023 actual result: per-riding Pearson r = 0.966, MAE = 3.74 pp, winner-call 81 of 87 (93.1 %). 338 systematically under-projected UCP in rural Alberta by ~4.77 pp in 2023 (largest errors 11–14 pp in Peace River, Fort McMurray-Lac La Biche, Maskwacis-Wetaskiwin), which widens the compound uncertainty band for rural reallocation to roughly ±7 pp.

**Direction of the 1-seat asymmetry is not stable across vote inputs.** Reallocating through the majority and minority hybrid crosswalks produces seat counts of 67 UCP / 22 NDP (majority 2026) and 66 UCP / 23 NDP (minority 2026) under April 2026 338 polling — a 1-seat gap favouring NDP on the minority. The audit's 2023-vote central produces 51 UCP / 38 NDP (majority) and 52 UCP / 37 NDP (minority) — a 1-seat gap favouring UCP on the minority. The size of the gap is 1 seat in both cases, but the direction flips. A 77-snapshot historical 338 stability probe (2020-02-23 through 2026-04-12) confirms this is systematic: in competitive environments (UCP provincial share 45–55 %) the minority map advantages UCP by an average of 1–3 seats; in UCP-landslide environments (UCP provincial share > 55 %, which April 2026 polling reflects) the minority map shifts to NDP-favourable by ~1 seat. Pre-2023 338 snapshots reallocated through the audit's own crosswalks produce majority 48 / 39 and minority 49 / 39 — a 1-seat UCP advantage on the minority, consistent with 2023 actual.

**Implication.** The 1-seat asymmetry is small (≤ 5 seats across all tested inputs) but *state-dependent* rather than structural. The defensible claim is that under realistic 2020s-era competitive provincial vote distributions, the minority map produces a small UCP advantage over the majority map; under UCP-landslide conditions or NDP-wave conditions (2019, 2015) the direction reverses. A structural-invariance claim was not supported by the historical stability test and has been retracted from this paper. Full method and data at `analysis/v0_1_338canada_historical.md` (77-snapshot time series at `data/v0_1_338canada_historical_snapshots.csv`; pre-2023 reallocation at `data/v0_1_338_historical/pre2023_reallocated_*.csv`; uniform-swing stability probe at `data/v0_1_338_historical/uniform_swing_stability.csv`).

### 3.5.1 Cross-metric weighting: what the four partisan-bias tests measure, and how to read their disagreement

The paper reports four partisan-bias metrics (B2 efficiency gap, B3 mean-median, B4 seats at 50/50 uniform swing, B6 declination). B2, B3, and B4 all show the minority 2026 map as more UCP-favorable than the majority 2026 map under 2023 vote input. B6 points the opposite direction: by declination, the minority is the *least* UCP-favorable of the three maps. Reporting this as "three of four metrics agree" understates the methodological question a reader has to evaluate.

**What each test measures and what it assumes:**

- **B2 Efficiency gap (Stephanopoulos & McGhee, 2015).** Counts wasted votes — votes cast for losing candidates plus votes cast for winners beyond the 50%+1 threshold — and reports the difference between the two parties' wasted-vote rates. Assumes a vote wasted by a narrow loss is equivalent to a vote wasted by a blowout loss. Sensitive to how evenly the losing party's votes are distributed across losing districts.
- **B3 Mean-median gap (McDonald & Best, 2015).** Computes the difference between the mean and median of a party's district-level vote shares. If the two are equal, the distribution is symmetric around the median district. Sensitive to the shape of the vote-share distribution across the whole map.
- **B4 Seats at 50/50 uniform swing.** Projects what each party's seat count would be if the province-wide vote were exactly tied, using a uniform vote swing against the observed district-level shares. Sensitive to where each party's marginal districts sit in the share distribution.
- **B6 Declination (Warrington, 2018).** Treats the two parties' winning districts as two clouds in a slope-vs-margin plane and computes the angle between the best-fit lines. A perfectly symmetric map produces zero declination. Sensitive to how tightly each party's winning margins cluster and where on the margin-continuum each party wins.

**Why B6 can disagree with B2, B3, and B4.** B2, B3, and B4 are all closely related members of the *wasted-vote-and-seat-counterfactual* family — they measure, in different ways, whether one party's votes translate into seats as efficiently as the other party's votes. If one of these agrees, the others usually agree. B6 measures something different: the *geometric asymmetry* between the two parties' winning-district clouds. A map can be partisan-unfavourable on wasted-vote terms (B2, B3, B4) while being geometrically symmetric on winning-district-margin terms (B6).

The canonical example: a map that packs the losing party into narrow-margin losses (losses by 45-55 rather than blowouts). On wasted-vote counts, the losing party still wastes many votes in those narrow losses; B2/B3/B4 flag the packing. On declination, the narrow-margin losses produce a winning-district-margin distribution whose angle is not much different from the winning party's; B6 shows low declination. Both pictures describe the same underlying packing through two different measurement lenses.

**Specific Alberta interpretation.** The minority 2026 map shows three 4-way urban splits (Airdrie, Lethbridge, Red Deer), a packed Calgary Zone A (NDP-leaning districts 12.2% larger than UCP-leaning), and a cracking-and-margin-narrowing pattern consistent with the "concentrate losing party in narrow losses" mechanism. Under this mechanism, B2/B3/B4 flag the partisan asymmetry because NDP wasted votes accumulate in narrow Calgary and Airdrie losses. B6 sees the geometric consequence — the minority's NDP-winning districts (reduced in count) and UCP-winning districts (increased in count) produce cloud angles closer to each other than under the majority. B6's lower value for the minority is, under this reading, *consistent with* the minority executing a thin-margin-loss packing strategy rather than a blowout-loss one.

**Classification of the disagreement.** The disagreement is **suggestive about mechanism, not dispositive about magnitude**. It does not overturn the B2/B3/B4 finding (which remains directionally UCP-favorable under 2023 votes in 90.5% of Monte Carlo samples). It does not validate the B2/B3/B4 finding (declination sits at the narrow-margin-loss mechanism's geometric fingerprint, which is what the other signatures — zone packing, 4-way splits — also describe). The honest reading is that the four metrics agree on the presence of partisan asymmetry while disagreeing on its mechanism: EG/MM/Seats@50-50 describe the wasted-vote consequence; declination describes the margin-distribution geometry; and the mechanism consistent with both is narrow-margin-loss packing. This is a different finding than "three metrics agree and one disagrees"; it is closer to "four metrics each describe a different face of the same structural pattern."

**What a hostile reviewer gets from the disagreement.** B6 standing alone is an argument that the minority map is geometrically more balanced than the majority on winning-district margin distribution. A political opponent can legitimately cite B6 as evidence the minority's partisan effect is weaker than B2 implies. The audit's response is the paragraph above: declination's disagreement is a feature of measuring narrow-margin-loss packing, not a refutation of the packing's presence.

**What assumptions to check.** Each metric carries at least one load-bearing assumption that a Canadian context can test:

- B2 assumes the losing party's wasted votes are homogeneous. Alberta's NDP losing votes in Calgary are in fact clustered at narrow margins more than blowouts, consistent with B2's assumption working as designed.
- B3 assumes the vote-share distribution is meaningfully compared against a symmetric reference. Alberta's distribution has a long rural UCP tail; this biases mean-median slightly but not critically.
- B4 assumes uniform swing. Alberta elections have historically swung uniformly enough that this is defensible, but the 2019→2023 swing was not uniform (NDP gained more in Edmonton than in Calgary); the counterfactual should be read with that caveat.
- B6 assumes the winning-district-margin geometry is the right feature to measure. Warrington (2018) defends this; Magleby and Mosesson (2018) document a ~22% US-state disagreement rate between declination and EG. The Alberta disagreement sits inside the expected divergence range, not as an outlier.

### 3.6 Natural-packing context (Chen & Rodden) — validated for Alberta with revised mechanism

Chen and Rodden (2013) argue that urban-concentrated parties are systematically disadvantaged by neutrally-drawn maps through a *packing mechanism* — their voters cluster in city cores, producing large-margin wins with many wasted votes while the opposing party wins surrounding districts by efficient margins. The original Chen-Rodden framing, applied naively, would predict that Alberta's NDP suffers from urban packing.

**Alberta validation test** (full methodology at `analysis/v0_1_chen_rodden_alberta_validation.md` and `analysis/v0_1_chen_rodden_alberta.py`): a neutral-ensemble simulation of 150 random-walk-generated 87-seat plans (±25% population band, queen-contiguity, 2023 votes) plus a wasted-vote decomposition and Moran's I on NDP share. Results:

- **Direction prediction holds.** Neutral-ensemble EG distribution: median −2.3 to −2.4%, 5th–95th percentile [−4.4%, −0.7%]. The 2019 baseline of −2.64% sits at the centre of this distribution. Both 2026 EGs (majority −0.85%, minority −1.36%) lie inside the neutral range. Directionally, Chen-Rodden transfers: neutral Alberta maps are UCP-favourable by construction.
- **Mechanism prediction fails.** The Chen-Rodden urban-packing mechanism does not operate in Alberta. NDP surplus-vote rate in NDP-won districts: 9.3%. UCP surplus-vote rate in UCP-won districts: **15.9%**. UCP is the more-packed party by excess wasted votes. Rural UCP-winning margins average 43.0 pp; urban NDP-winning margins average 21.5 pp. NDP's seat deficit comes from **dispersed losing votes** in rural and suburban ridings where the NDP consistently loses by 60–80 pp, not from over-concentration in urban cores.
- **Moran's I on NDP two-party share: 0.7534 (p < 0.001, z = 12.15).** Strong spatial clustering is confirmed. Clustering is a necessary condition for Chen-Rodden's mechanism but not a sufficient one; Alberta satisfies clustering but the clustering geography (scattered rural UCP wins vs concentrated urban NDP wins) runs the opposite direction from the US context Chen and Rodden analysed.

**Revised framing.** The 2019 baseline EG of approximately −2.64% is roughly at the centre of what a neutral Alberta map would produce given 2023 vote geography — but the mechanism that produces this baseline is *UCP rural dispersion with large-margin wins*, not *NDP urban packing*. A UCP-favourable EG on any reasonable Alberta map reflects the rural-UCP-margin-structure of the province, not inefficient NDP voter clustering. Under this corrected framing:

- The 2019 EG establishes a neutral benchmark: roughly −2.3 to −2.4% is what a geography-respecting Alberta map produces.
- The majority 2026 EG (−0.85%) is *closer to zero than the neutral median*: the majority proposal reduces the UCP-favourable lean that Alberta's rural-margin structure would otherwise produce.
- The minority 2026 EG (−1.36%) also sits inside the neutral range but closer to the neutral median than the majority.

**Implication for partisan-bias findings.** The difference between the two 2026 maps' EGs (−0.85% vs −1.36%) is smaller than the width of the neutral-ensemble 90% CI (3.7 pp). A full GerryChain ReCom ensemble (follow-up work; requires 8–24 hours of compute) would produce a tighter CI and let us place each 2026 map as an ensemble percentile. Until that runs, the correct statement is: both 2026 maps are within the neutral range; the majority is modestly further from Alberta's natural UCP-favourable floor than the minority. This weakens the "intentional partisan choice" inference for §B specifically and does not reach §A (population equality), §C (geographic coherence), or §D (procedural fairness) findings.

**Synthesis.** The audit's strongest claim incorporates both the direction-validated Chen-Rodden prediction and the mechanism correction: Alberta's rural-UCP-margin structure produces a neutral UCP-favourable EG by default; the majority 2026 map moves moderately further from that floor than the minority 2026 map does, but the difference between the two is within the width of neutral-ensemble uncertainty; the minority's distinct-from-majority character therefore has to be argued on §A, §C, §D, and §3.12 evidence rather than on §B evidence alone. The B-section findings reinforce the others; they do not stand alone as conclusive of partisan intent.

**Scope of the Chen-Rodden reading.** Chen-Rodden's natural-packing argument applies specifically to partisan-bias metrics (§B). It does not reach the structural findings in §A (population equality), §C (geographic coherence), or §D (procedural fairness). The audit's primary findings are structural: wider minority population dispersion (MAD 4,707 vs 3,180), 12.2% vs 0.4% Calgary geographic-zone asymmetry, engineered s.15(2) boundary at Rocky Mountain House-Banff Park, 4-way fragmentation of Airdrie vs 2-way, and three formal signatures (packing / cracking / engineered-boundary) under the minority vs zero under the majority. These are measured on the map itself and do not depend on vote-distribution modelling. The partisan-bias finding in §3.3 is best read as one dimension among six, not as the headline: the minority map corrects less of Alberta's natural UCP-favouring geography than the majority does (majority EG −0.85%, minority EG −1.36%, 2019 baseline −2.64%), and the headline for the audit is the structural divergence between the two 2026 maps, which §3.6's natural-packing framing cannot explain.

### 3.7 Packing signatures detected

Formal packing signature detection applies the P1–P3 criteria (district size above mean, winning-margin above mean, counterfactual-seat-loss verifiable).

**Pre-registration provenance.** The P/C/E criteria and their numeric thresholds are specified in `v1_2_gerrymander_audit_prompt.md`, committed as `5b0bc06` at 2026-04-22 08:32:20 −06:00. The signature-detection analysis reported in §3.7–3.9 was committed as `282bc6d` at 2026-04-22 10:56:11 −06:00. The criteria exist in the repository 2 hours 24 minutes before the detection runs. `git log --all --format='%h %ci %s' -- v1_2_gerrymander_audit_prompt.md` reproduces this timeline. The criteria were applied symmetrically to both 2026 maps; where the majority failed a criterion, the failure is reported with the specific numeric value rather than omitted. Residual vulnerability: the pre-registration is intra-session (hours, not days, of separation). The November 2026 MLA-committee 91-seat map is the planned held-out test that closes this residual.

**Threshold provenance.** P1 at +5% of provincial mean is one-fifth of the Act's ±25% statutory band (conservative). C3 at ±25% is the Act band directly. P2 at +15 pp above mean winning margin yields an operational "safe-seat" cut-off of ~34 pp, above the 20 pp threshold used in Chen (2017). E1–E3 are conjunctive (all three must hold), the stricter test. These thresholds were set before the detection analysis (see git timestamps above) and are applied identically to both 2026 maps.

**Packing signature in Calgary Zone A under the minority 2026 map.** Detected.

- **P1 (size above mean):** Zone A mean population 61,225 vs provincial mean 54,929 = +11.5%. Threshold is +5%. **Pass.**
- **P2 (winning margin above mean):** 13 of the 17 Zone A districts were NDP-won in 2023. Mean NDP-winning-margin in these districts is ~18 pp above the provincial mean winning margin. **Pass.**
- **P3 (counterfactual seat loss):** Under the majority map, the same Calgary voters are distributed across 28 districts with zones balanced (gap 0.4%). The minority's 29-district Calgary configuration with 12.2% zone gap represents roughly 113,000 NDP-leaning voters that would otherwise require 1–2 additional seats at equally-populated distribution. **Pass.**

**No packing signature detected in Calgary under the majority 2026 map.** P1 fails with Zone A mean of 56,460 vs Zone B 56,255 (gap 0.4%, well below the +5% threshold relative to provincial mean).

**No packing signature detected in Calgary under the 2019 baseline.** Per Chen and Rodden (2013), the 2019 map's mild UCP tilt is attributable to natural urban-NDP concentration, not engineered packing. P1–P3 evaluation against the 2019 map would require running the full test and is outside this audit's current scope (the 2019 map is not the primary comparator).

### 3.8 Cracking signatures detected

Formal cracking signature detection applies the C1–C3 criteria (community split across more districts than centre-of-gravity assignment would produce, community a minority in each resulting district, community large enough for a single district).

**Cracking signature for Airdrie under the minority 2026 map.** Detected.

- **C1 (split count exceeds necessity):** Airdrie (population 74,100 at 2021 Census; ~84,000 at 2024 municipal estimate; 90,044 at the April 2025 municipal census) is split across 4 districts in the minority map; no district is named Airdrie. Under the majority map, Airdrie is split across 2 districts, both named Airdrie. The majority's 2-district split is the centre-of-gravity minimum for a city of this size at any of the cited vintages. 4 districts is above necessity. **Pass.**
- **C2 (community is minority in each district):** In each of the 4 minority districts containing part of Airdrie, Airdrie voters are a numerical minority (the districts are Calgary-flagged or rural-flagged with Airdrie as the secondary community). **Pass.**
- **C3 (single-district feasible):** Airdrie's 2024-estimate population of ~84,000 (2021 Census 74,100, 2025 municipal census 90,044) is above the provincial average of 54,929 but within the ±25% band (54,929 × 1.25 = 68,661) plus a rural-boundary adjustment. Realistic single-district feasibility: 1 Airdrie-only district plus a 2nd split to bring its component to the standard range. **Pass for up to 2-district split; fails above 2.**

**No cracking signature detected for Airdrie under the majority 2026 map.** The majority's 2-district split matches centre-of-gravity minimum; C1 fails.

**Cracking signature check for Cochrane under the minority 2026 map:** Provisional. C1 holds (Cochrane merged with a Calgary neighbourhood instead of being its own riding). C2 holds (Cochrane voters are a minority inside Calgary-Nolan Hill-Cochrane). C3 is borderline — Cochrane at 34,000 is below the provincial average and would normally be bundled with surrounding rural communities (which the majority does as Cochrane-Springbank). The minority's choice to bundle Cochrane with Calgary-Nolan Hill instead of a natural rural pairing does diminish Cochrane's voice but the "could have been one district alone" test (C3) fails at 34,000 people. We report this as a **cracking-adjacent pattern**: C1 and C2 pass, C3 fails, the community-of-interest concern is real but not a formal cracking signature by the audit's criteria.

**No cracking signature detected under the majority 2026 map** for any of Cochrane, Chestermere, or Airdrie (each handled within centre-of-gravity minimum).

### 3.9 Engineered-boundary signatures detected

Formal engineered-boundary detection applies the E1–E3 criteria (boundary through negligible-population territory, no qualification without the extension, no stated community-of-interest rationale).

**Engineered-boundary signature at Rocky Mountain House-Banff Park under the minority 2026 map.** Detected.

- **E1 (boundary through negligible-population territory):** The district's southwest extension traces through uninhabited Banff National Park land to reach the British Columbia border. Confirmed on the published minority Alberta overview map (Appendix E, p. 73). **Pass.**
- **E2 (without extension, district would not qualify):** Without the NP extension, the district's area falls below the 20,000 km² threshold for s.15(2) criterion (a), and it would not share a provincial border for criterion (e). The district at 38,298 people (30% below provincial mean) cannot justify its low population without s.15(2) qualification. **Pass.**
- **E3 (no stated community-of-interest rationale for the extension):** The commission's prose description in Appendix E names no community of interest served by the NP-extension portion; it is uninhabited park land. The chair's majority report flagged this district's boundary explicitly as engineered. **Pass.**

**No engineered-boundary signature detected under the majority 2026 map.** The majority's s.15(2) invocations (Central Peace-Notley, Lesser Slave Lake, Canmore-Banff) do not show boundary extensions through negligible-population territory in the available imagery. Canmore-Banff fails the §A3 3-of-5 criteria test at 1/5, but the failure is on criteria (a) area and (c) no-4,000-plus-town rather than on engineered boundary. If majority non-Calgary imagery were available, Canmore-Banff would warrant a second look for E1 specifically.

### 3.10 Signatures summary

| Signature type | Minority 2026 | Majority 2026 | 2019 baseline |
| --- | --- | --- | --- |
| Packing (Calgary Zone A) | Detected | Not detected | Natural-packing context only |
| Cracking (Airdrie) | Detected | Not detected | Not applicable (Airdrie-Cochrane was one ED) |
| Cracking-adjacent (Cochrane merged with Calgary) | Pattern present, C3 fails | Not detected | Not applicable |
| Engineered boundary (RMH-Banff Park s.15(2)) | Detected | Not detected | Not applicable |

Three formal signatures, one borderline pattern, all concentrated in the minority map. The detection is not "we think the minority looks engineered"; it is "apply P/C/E criteria mechanically, record what passes."

### 3.11 Pre-registered checklist baseline scoring

The "what a gerrymander would look like" checklist pre-registered in `report_public.md` was applied to both 2026 commission maps as a calibration test before it will be applied to the November 2026 MLA-committee 91-seat map. The scorecard, reproduced in full in `analysis/v0_1_track_c_checklist_baseline_scoring.md`:

| Signal class | Majority 2026 | Minority 2026 |
| --- | --- | --- |
| Strong signals triggered (of 4 scorable; S3 and S5 deferred) | 0 | 1 (the S1 signature set, by construction) |
| Weak signals triggered (of 2 scorable) | 0 | 2 (W2 Calgary zone gap, W3 Nolan Hill-Cochrane retention) |
| Process signals triggered (of 5) | 0 | 0 |
| Rationale-against-data contradictions (X2) | 0 | 3 (shared-schools x 2, Cochrane commuter-tie partial, plus five population-math tests failed) |

Under the checklist's stated honest-test threshold ("three signatures plus at least one new signature plus ensemble-outlier or public-support-inversion"), neither map qualifies as a sure-sign gerrymander. The minority meets only the first of the three conjunctive clauses (signatures), fails to introduce new signatures, fails the ensemble-outlier clause because shapefiles are unreleased (test blocked rather than failed), and does not invert public support. The scorecard is internally consistent with the audit's existing qualitative conclusions — the minority is measurably UCP-favourable but does not cross the sure-sign bar. The scorecard's value going forward is twofold: it operationalises the pre-registered test for the November map, and it demonstrates that the test distinguishes the two known maps in the expected direction before any new map is drawn.

**External pre-registration.** To close the self-held-pre-registration concern (a third party is needed to hold pre-registered criteria for the pre-registration to have methodological force beyond the author's own discipline), the checklist is prepared for submission to the Open Science Framework Registrations platform (`https://osf.io`) with embargoed release scheduled for 2026-11-02 to match the committee's map deadline. The submission-ready document is in `analysis/v0_1_pre_registration_draft.md`; the platform survey and submission instructions are in `analysis/v0_1_pre_registration_platform_analysis.md`. Once submitted, the OSF-assigned DOI will appear in §3.11 and the audit's README as the time-stamped third-party custody record.

### 3.12 Symmetry-of-test-selection audit

The audit applies each analytical test identically to both 2026 maps (test-application symmetry, see §1.1). A separate discipline, *test-selection symmetry*, asks whether the tests themselves were designed around observed minority features rather than around structural features either map could exhibit (Chen & Rodden, 2015; Pal, 2019). To address this discipline, a counter-test was constructed (`analysis/v0_1_majority_symmetry_counter_test.py`, 2026-04-22) that generates symmetric hypothetical tests and applies them to both maps.

**Counter-test 1 — Edmonton zone packing.** Classify Edmonton EDs into Zone C (north of the North Saskatchewan River) and Zone D (south of the river); compute the C-vs-D mean-population gap; compare to the Calgary Zone A-vs-B gap. Result: Edmonton Zone C-vs-D gap is +2.0 pp under the majority map and +1.4 pp under the minority map, both far below the Calgary Zone A-vs-B gap of 12.2 pp in the minority map. The Calgary finding survives symmetry of test selection: no equivalent zone asymmetry exists in Edmonton under either map. The Calgary packing is a minority-map-specific feature, not an artefact of selecting a Calgary-zone test.

**Counter-test 2 — City-wide 4-way split.** For every Alberta municipality with population ≥ 50,000 (excluding Calgary and Edmonton, whose populations exceed three statutory quotas and force multi-way splits), identify any city split across four or more EDs in either map. Results:

| City | Majority map | Minority map |
|---|---|---|
| Airdrie | 2 EDs (known) | 4 EDs (known) |
| **Lethbridge** | **2 EDs** | **4 EDs — new finding** |
| **Red Deer** | **2 EDs** | **4 EDs — new finding** |
| Medicine Hat | 2 EDs | 2 EDs |
| St. Albert | 1 ED | 1 ED |
| Grande Prairie | 1 ED | 1 ED |
| Lloydminster | 1 ED | 1 ED |

Two new minority-specific cracking-candidate patterns emerge: Lethbridge 4-way (Lethbridge-Cardston, Lethbridge-Fort MacLeod-Crowsnest Pass, Lethbridge-Little Bow, Lethbridge-Taber-Warner) and Red Deer 4-way (Red Deer-Blackfalds, Red Deer-Innisfail, Red Deer-Lacombe, Red Deer-Sylvan Lake). The majority map applies 2-way splits to both cities. Pending C2 / C3 threshold tests (see §3.8 for the formal cracking-signature methodology), these are *cracking-candidate* findings rather than formally-detected cracking signatures. The audit's existing Airdrie cracking finding now extends to a pattern of three Alberta cities where the minority map performs unforced 4-way splits the majority does not.

**Pre-registration caveat for the Lethbridge and Red Deer findings.** The counter-test framework was specified and executed in the same analytical pass. The symmetry criteria are prose-level and the city-population threshold (≥ 50,000 residents) is geographically anchored rather than retrofitted, but the finding was not independently pre-registered before execution. These two cracking candidates are therefore held separately from the Airdrie cracking signature in §3.8: Airdrie is a formally-detected signature meeting P/C/E thresholds pre-registered before the detection run; Lethbridge and Red Deer are symmetric-test-derived patterns that match Airdrie's structure but have not passed the same formal gate. They are reported because the symmetric test found them; they should not be counted as additional formal signatures beyond Airdrie until the C-criteria run produces threshold values for each city.

**Interpretation.** The audit's symmetry-of-test-selection claim is strengthened by the Edmonton counter-test (Calgary zone asymmetry is not a test-selection artefact) and extended by the Lethbridge and Red Deer findings (the cracking pattern identified at Airdrie reproduces elsewhere). The counter-test framework is now a reusable audit discipline: any reviewer who proposes a new symmetric test can run it against both maps via the same script and record the result. Full per-city data at `data/v0_1_majority_symmetry_counter_test.csv`.

### 3.13 Stress-test grades mini-audit

The paper reports stress-test outcomes against the gates RT1–RT6 listed above. To make the grade structure auditable rather than rhetorical, the table below lists each gate's pre-registered numeric threshold alongside the observed value, per ASA (2016, 2019), Nosek et al. (2018), and Munafò et al. (2017) guidance on graded evidence reporting.

| Gate | Pre-registered threshold | Observed value | Outcome |
|---|---|---|---|
| RT1 — Monte Carlo 95% CI | Same-sign bounds for strong pass | [−3.04, +0.76] pp, crosses zero | Fails strong pass; 90.5% direction consistency is a separate direction claim |
| RT2 — Cross-metric agreement | ≥3 of 4 same sign for strong pass | B2, B3, B4 agree; B6 declination opposes | 3-of-4 same sign; reported as mixed rather than "majority" |
| RT3 — Cross-election stability | Same direction across 3 election baselines | 2023 & April 2026 same; 2019 reverses | Fails strong; direction-stable across 2020s-era inputs |
| RT4 — Structural vs vote-based separation | Clear labelling required | Labelling present in §1, §7 | Pass |
| RT5 — Independent test selection | No test run and discarded | Audit-trail clean; counter-test §3.12 added | Pass |
| RT6 — Assumption inventory | Listed in `analysis/v0_1_uncertainty_and_shapefile_impact.md` | Current | Pass |

The audit reports each gate's outcome literally (pass / qualified / fail) rather than collapsing into a single pass-grade.

---

## 4. Geographic Coherence (Section C)

### 4.1 Visual spatial audit

Direct inspection of published commission maps using Opus/Sonnet 4.x vision. Images inspected:

- `maps/majority_calgary.jpg` — Appendix A, p. 72
- `maps/minority_calgary.jpg` — Appendix E, p. 74
- `maps/minority_alberta_overview.jpg` — Appendix E, p. 73
- `maps/minority_edmonton.jpg` — Appendix E, p. 75
- `maps/minority_other_cities.jpg` — Appendix E, p. 76

**Symmetry data gap.** The working bundle lacks majority-proposal equivalents for the Alberta overview, Edmonton, and other-cities panels. Visual inspection of the majority is therefore limited to its Calgary districts. Rural and Edmonton majority districts are evaluated from published report text, not direct images. This is disclosed in the section's conclusion and narrows the scope of any majority-vs-minority claim made from direct visual evidence.

### 4.2 Chair-flagged boundaries (C3)

Four boundaries were flagged by name in the majority report's response section. Direct inspection results:

- **Calgary-Nolan Hill-Cochrane (minority):** **Confirmed.** A district that reaches from Cochrane (outside Calgary's western boundary) eastward through a narrow-waisted corridor to Calgary's Nolan Hill neighborhood, skipping Rocky Ridge / Tuscany.
- **Rocky Mountain House-Banff Park (minority):** **Confirmed.** SW extension of the district traces Banff National Park to reach the BC border. Absent the extension, the district fails s.15(2) criteria (a) and (e).
- **Olds-Three Hills-Didsbury (minority):** **Confirmed.** Named for three small towns; extends south past Didsbury to capture a portion of N Airdrie. Airdrie has a population greater than the three named towns combined.
- **Calgary-Foothills-Airdrie West (minority):** Boundary connection between Calgary-Foothills and Airdrie West tracks a primary highway corridor; the geographic connection itself is defensible, but this ED is one of four making up the Airdrie split (C4).

### 4.3 Majority hybrids — symmetric check

Applied the same anomaly-scan questions (lasso shape, engineered statutory boundary, misnamed municipality capture) to the majority's four Calgary hybrids:

- **Calgary-East:** Intra-city rectangular block, no extension beyond city limits. No anomaly.
- **Calgary-Falconridge-Conrich:** NE Calgary + directly-abutting Conrich community. Compact. No anomaly.
- **Calgary-Glenmore-Tsuut'ina:** Large southern extension to include the Tsuut'ina Nation reserve; shape tracks the reserve boundary. No anomaly; positively, the reserve is kept intact in a single named ED.
- **Calgary-West-Elbow Valley:** Calgary SW + directly-adjacent Elbow Valley subdivision. No anomaly.

**Qualification.** The anomaly-scan question set was developed from observed minority anomalies. The majority may have different classes of anomaly (e.g., rural-district highway corridors) not visible in Calgary and not tested from the bundle's available images. A full-symmetry visual audit requires the three missing majority images.

### 4.4 Community-of-interest splits (C4)

| Dimension                            | Majority 2026        | Minority 2026        |
| ------------------------------------ | -------------------- | -------------------- |
| Lasso/corridor shapes (visible)      | 0                    | 1 (Calgary-Nolan Hill-Cochrane) |
| Engineered statutory boundary         | 0                    | 1 (RMH-Banff Park extension) |
| Community captured under misnamed ED | 0                    | 1 (Olds-Three Hills-Didsbury → N Airdrie) |
| Airdrie split                        | 2 EDs                | 4 EDs                |
| Cochrane                             | intact               | merged into Calgary   |
| Chestermere                          | intact               | partially split       |
| Tsuut'ina Nation                     | single ED, named     | single ED, named      |
| Enoch Cree Nation                    | with Edmonton only   | bundled with Devon (~50 km S) |
| Siksika Nation                       | High River-Vulcan-Siksika | High River-Vulcan-Siksika (same) |

**Census-subdivision-level robustness check.** A CSD-level overlay (Track H; script `analysis/v0_1_csd_community_splits.py`) computes, per map, the count of populated CSDs (population ≥ 1,000) spanning two or more electoral divisions. Under 2019 boundaries (measured via geopandas overlay on `data/alberta_2019_eds/`): 66 of 191 populated CSDs (34.6%) are split. Under the majority 2026 proposal (inferred via the Appendix C crosswalk): 66 of 191 (34.6%). Under the minority 2026 proposal (inferred, lower bound, via the heuristic crosswalk): 54 of 191 (28.3%); upper bound matching the 2019 count of 66. On the confident-only subset of 139 CSDs (excluding those touched by minority-crosswalk uncertainties or any hybrid), all three maps produce the same 40 splits. **The Majority-minus-Minority asymmetry visible in the table above is not detectable at CSD granularity.** The minority's community-of-interest disadvantage operates at within-ED partition resolution (e.g., the four-way partition of the City of Airdrie, the bleed of Chestermere into Calgary-Peigan-Chestermere) — a resolution not encoded in the ED-level crosswalks and not directly measurable until the 2026 shapefiles release. The within-ED qualitative findings in the table above remain the reported finding; the CSD-level count is a null symmetric across maps and is reported here as a bounding limit on the metric's directional power.

**Shared-schools community-of-interest claim — failure of cross-reference, systematic in structure.** Two minority configurations defend their hybrid structure partly on school-district community of interest. Calgary-Bow-Springbank (AEBC, 2026, Appendix E, p. 322) invokes "educational institutions" as a community-of-interest tie between Springbank and west Calgary; Springbank falls within Rocky View School Division No. 41 while the relevant west-Calgary catchment is served by the Calgary Board of Education (Alberta Education, school-division boundaries). Red Deer-Sylvan Lake (AEBC, 2026, Appendix E, p. 351) cites schooling as an urban-rural tie; Sylvan Lake falls within Chinook's Edge School Division No. 73 while the City of Red Deer is served by Red Deer Public Schools and Red Deer Catholic Regional Schools. The shared-schools rationale is not supported by the school-district boundary data in either case.

**The pattern is structural, not isolated.** An audit of all 21 minority hybrids against Alberta Education school-division boundaries (`analysis/v0_1_school_division_coherence.md`) finds that **20 of 21 cross at least one school-division boundary** — a mathematical consequence of Alberta's school divisions being built around municipal limits (CBE ends at Calgary's limits, Red Deer Public at Red Deer's, Edmonton Public at Edmonton's) and the minority's hybrid doctrine explicitly crossing municipal limits. All four Red Deer hybrids (Blackfalds, Innisfail, Lacombe, Sylvan Lake) cross school-division boundaries — not just Sylvan Lake. The rhetorical contradiction the audit identified for R5 and R11 is therefore representative, not exceptional: the minority chose the two cases where five minutes of Alberta Education verification shows the register is wrong, but the underlying cross-division pattern applies to nearly every minority hybrid. The structural school-division crossings are not by themselves gerrymander signals on the school dimension; what is damning is narrower — R5 and R11 invoked the most verifiable class of community-of-interest claim and got it wrong. Full per-hybrid classification (school-coherent / mildly incoherent / severely incoherent / neutral) in `analysis/v0_1_school_division_coherence.md`.

**Cochrane commuter-tie claim — partial support at CSD resolution.** The Calgary-Nolan Hill-Cochrane hybrid is defended by the minority report (AEBC, 2026, Appendix E) partly on the claim that Cochrane residents "move fluidly" between Cochrane and Calgary. StatsCan Table 98-10-0459 (2021 Census journey-to-work) disaggregates Cochrane CSD commute destinations: of 8,550 Cochrane workers with an Alberta place of work, 4,205 (49.2%) work within Cochrane, 3,065 (35.8%) commute to Calgary CY, 345 (4.0%) to Rocky View County, 185 (2.2%) to Canmore, 135 (1.6%) to Wood Buffalo, and 130 (1.5%) to Airdrie. The Calgary flow is a genuine commuter-tie signal at the city-to-city level; the 2021 public release collapses Calgary to a single CSD and cannot test the within-Calgary sub-destination, so the pairing of Cochrane specifically with the Nolan Hill/Sage Hill ward is neither confirmed nor refuted by this dataset. The interpretive inference — that Nolan Hill is a residential neighbourhood without significant employment and is therefore unlikely to be the commute destination for the 35.8% Calgary-bound flow — is consistent with the city's land-use profile but does not derive from the StatsCan data directly. Full methodology in `analysis/v0_1_cochrane_journey_to_work.md`.

**Piikani name-etymology note.** The name "Peigan" in the existing Calgary-Peigan electoral division and its minority extension Calgary-Peigan-Chestermere derives from Peigan Trail SE, a road forming the district's northern boundary, not from a community-of-interest tie to the Piikani Nation (whose Piikani 147 reserve is located approximately 200 km south of Calgary, near Pincher Creek and Fort Macleod). The minority's retention of the name in the hybrid extension preserves a road-based etymology. This is a naming observation, not a finding of fault.

---

## 5. Procedural Audit (Section D)

### 5.1 Commission operation

Five-member commission constituted under Electoral Boundaries Commission Act §3–5: chair nominated by the Chief Justice of Alberta, two government-nominated commissioners, two opposition-nominated commissioners. Commission tabled unanimous interim report October 2025; tabled divided final report (3–2) March 23, 2026. The three-member majority comprises the chair plus the two opposition-nominated commissioners.

### 5.2 April 16, 2026 government action

On April 16, 2026 the Alberta Legislative Assembly passed Motion 19 by a vote of 44 to 36, setting aside the commission's majority report and establishing a Special Select Committee of five MLAs (three UCP, two NDP) chaired by Brandon Lunty, MLA for Leduc-Beaumont, to produce a 91-seat map by November 2, 2026. The committee is served by an advisory panel with the same three-party structure as the commission (government-appointed chair plus two nominees per party), whose membership and terms of reference had not been published as of April 22, 2026 (CBC Edmonton, April 16, 2026; Calgary Journal, April 21, 2026). Unlike the commission it replaces, the new process does not include public hearings on the draft map.

**Relationship to Chair Miller's Recommendation 5.** The Premier framed the April 16 motion as aligned with a recommendation by Chair Dallas Miller (Government of Alberta press remarks, April 16, 2026, as reported in Rimbey Review; Calgary Journal, April 21, 2026). This framing is traceable to the Chair's Addendum to the Majority Report (AEBC, 2026, pp. 66–67), which proposed **Recommendation 5**: in the event the Legislature could not accept the majority's 89-seat boundaries, the Act should be amended to raise the seat count from 89 to 91 through "an all-party Select Special Committee or other equivalent Legislative Committee," restoring the two rural divisions the majority report removed while maintaining "the rest of the province as we propose... to the extent possible."

The alignment between R5 and the April 16 motion is partial on three grounds, addressed individually in `analysis/v0_1_chair_recommendation_5_analysis.md`:

1. **Form.** The vehicle (Select Special Committee raising the count from 89 to 91 for rural-seat restoration) matches R5's specification. The motion can legitimately claim this anchor.

2. **Substantive constraints.** R5(a)–(d) specifies four concrete boundary conditions — no impact on any electoral division in Airdrie or south of it except Drumheller-Stettler; no impact north of Edmonton's North Saskatchewan River; reversion of south-of-NSR Edmonton districts to the interim-report map; restoration of a Clearwater County-plus-western-Mountain-View s.15(2) district. Whether the committee's November output respects these conditions is not yet testable and should form part of the pre-registered November checklist (see §7.4). R5 also requires that "the rest of the province as we propose [in the majority report] must be maintained to the extent possible" — a condition the committee's present mandate does not carry forward.

3. **Intent.** Chair Miller stated R5's purpose directly: it "is formulated for the express purpose of dissuading the Legislature from accepting the minority report" (AEBC, 2026, p. 66). The Chair further described the minority's hybrid configurations in Airdrie, Calgary, Chestermere, Cochrane, Red Deer, and St. Albert as "not something that I can condone" (AEBC, 2026, p. 67). A committee output that reintroduces any of those minority configurations invokes the form of R5 while inverting its intent. The motion's silence on which starting map the committee uses, combined with the presence in the committee of the political faction that appointed the minority commissioners, is therefore procedurally distinct from R5's conditional.

**Regional-economy framing.** Alberta's Regional Economic Development Alliance geography provides partial support for the minority's general hybrid doctrine. The Central Alberta REDA covers Red Deer, Innisfail, Blackfalds, Lacombe, and Sylvan Lake — the five municipalities at the heart of the minority's Red Deer hybrid proposals. The Calgary Regional Partnership covers Calgary, Airdrie, Cochrane, Chestermere, Okotoks, Rocky View, and High River — the catchment for the minority's Calgary hybrids. These are real, publicly-documented regional organisations. They are not, however, boundary prescriptions; any map grouping districts within these zones satisfies the zone-coherence criterion, and the zones do not by themselves justify the specific intra-zone configurations the minority proposed.

### 5.3 Comparator cases

Canadian boundary-commission practice traces to *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158, which established the "effective representation" standard as the constitutional benchmark for provincial electoral boundaries. *Figueroa v. Canada (Attorney General)* [2003] 1 SCR 912 and *Frank v. Canada (Attorney General)* [2019] 1 SCR 3 developed the broader §3 Charter right to vote but did not directly apply the effective-representation standard to redistribution; they are listed in the References as context for the Charter jurisprudence surrounding electoral rights, not as authorities on boundary drawing. Courtney (2001) provides the authoritative scholarly treatment of the independent-commission model across Canadian provinces. Pal (2019) applies contemporary quantitative gerrymandering analysis to Canadian boundary cases within the Charter framework.

Canadian provincial instances of government action on independent boundary commission output:

- **Quebec 1992 (Commission de la représentation électorale):** Narrow amendments to commission report via National Assembly legislation. Commission drafting process not replaced.
- **Ontario 1996 (Fewer Politicians Act):** Government adopted federal (independent-commission-drawn) boundaries rather than running a provincial commission. Not a substantive override of provincial-commission output — a substitution of one independent commission's work for another's.
- **British Columbia 2008 (Campbell Liberals):** Government legislated to retain more Northern seats than the commission recommended. Rejection of specific recommendation; drafting process not replaced.

The April 16 action is distinguishable from all three comparators in that it replaces the drafting process rather than amending its output. The stronger claim "without recent Canadian provincial precedent" is not supportable without a comprehensive survey of all provincial redistribution cycles since 1991, which was not performed. A defensible framing: **the April 16 action is the most government-controlled response to an independent provincial boundary commission among the three most commonly cited Canadian comparator cases.**

### 5.4 Public submission record (D2)

The commission received approximately 1,340 written submissions across two rounds of public consultation. The majority report's Appendix C (Alberta Electoral Boundaries Commission [AEBC], 2026) states that the minority's hybrid configurations for Airdrie, Cochrane, Chestermere, Red Deer, and St. Albert **had no public support in the consultation record**.

A keyword search with manual review of the commission's submission archive — 1,252 of approximately 1,340 submissions extracted with machine-readable text and 14 recovered via OCR — tests this claim. Full methodology, dataset, and technical log are in `analysis/submission_search.py`, `data/submission_search_dataset.csv`, `analysis/submission_search_findings.md`, and `deprecated/submission_search_log.md`.

**Result: the chair's claim is partially refuted, with tiered severity.** A follow-on signal-strength analysis (`analysis/v0_1_claim_significance_analysis.md`) distinguishes between configurations where the chair was merely *precisely wrong* (a supporting submission exists, so "no support" is technically false) and where the chair was also *effectively wrong* (support is substantial enough that "no support" materially misrepresents the submission record).

**Verdict by tier:**

- **Precisely and effectively wrong** (three configurations where the minority adopted proposals *from* the public record, not despite it):
  - Rocky Mountain House-Banff Park: 5 supporters, net +4, 25% of engaged submissions support the configuration
  - Olds-Three Hills-Didsbury: 3 supporters, net +2, 60% of engaged submissions support
  - Chestermere separation: 3 supporters, net +2, 23% of engaged submissions support
- **Precisely wrong, effectively ambiguous** (support exists but is evenly matched by opposition):
  - Red Deer hybrids: 4 supporters, 4 opposers, net 0, 22% of engaged submissions support
- **Precisely wrong only / chair effectively correct** (support is negligible or zero):
  - Airdrie 4-way: 0 supporters, 2 opposers, 0% of 4 engaged submissions
  - Calgary-Nolan Hill-Cochrane: 0 submissions mention this configuration at all
  - St. Albert-Sturgeon (minority variant): 0 clear supporters for the minority's alternative configuration; label-ambiguity caveat

The tier distinction matters because the chair's Appendix C claim was an argument for procedural weight, not a technicality. A chair who said "no public support" when 25–60% of engaged citizens proposed the exact configuration has mischaracterized the public record on that specific point, not simply overlooked a dissenting voice or two. By contrast, a chair who said "no public support" for the Airdrie 4-way split is effectively correct — four engaged citizens discussed the configuration and none supported it.

**Implication for the D2 procedural finding:** the claim narrows but does not dissolve. The chair's sweep was *materially* overbroad on three of seven named configurations, *ambiguous* on one, and *defensible* on three. The audit should report these tiers rather than treating Appendix C as uniformly unsupported or uniformly sound. This matters because readers on both sides of the debate have incentive to flatten the finding: critics will use "chair was wrong" without the tiering; defenders will use "some configurations did hold up" without naming the three that did not. The tiered verdict resists both flattenings.

#### 5.4.1 Evidence by configuration, with per-area proportions

For each configuration, we report submissions mentioning it, submissions supporting the minority direction, and submissions opposing. The "support rate" column is the ratio of explicit supporting submissions to total submissions engaging with that configuration — a local measure of public backing among engaged citizens, not a measure of province-wide support.

| Minority configuration | Mentions | Supporting minority | Opposing | Neutral | Support rate | Verdict |
|---|---|---|---|---|---|---|
| Airdrie 4-way split | 4 | 0 | 2 | 2 | **0 / 4 = 0.0%** | Chair's claim stands |
| Calgary-Nolan Hill-Cochrane hybrid | 0 | 0 | 0 | 0 | **0 / 0 = n/a** | Chair's claim stands |
| Rocky Mountain House-Banff Park (s.15(2)) | 20 | 3 + ≥4 aligned | 1 | ~15 | **3 / 20 = 15%** (7 / 20 = 35% with aligned) | **Refuted** |
| Olds-Three Hills-Didsbury rural unit | 5 | 2 | 2 | 1 | **2 / 5 = 40%** | **Refuted** |
| Chestermere separation | 13 | 3 | 3 | 7 | **3 / 13 = 23%** | **Partially refuted** |
| Red Deer hybrids | 23 | 2 explicit + 3 aligned | 4 | 17 | **2 / 23 = 9%** (5 / 23 = 22% with aligned) | **Partially refuted** |
| St. Albert-Sturgeon (minority alternative) | 11 | 0 for minority variant (2 for majority name) | 1 | 8 | **0 / 11 = 0%** for minority alternative | Chair's claim stands |

#### 5.4.2 Direct quotation evidence

**Rocky Mountain House-Banff Park — EBC-2025-2-0619** ("Appropriate Political Representation for Alpine Alberta"). Under "3.2 Proposed Electoral Division Amendment 2: Rocky Mountain House-Banff":

> *"The proposed Rocky Mountain House-Banff electoral district brings together the upper Bow and North Saskatchewan headwaters, adjacent mountain parks, surrounding Crown land, and the communities that depend on these landscapes for their livelihoods. It would include Lake Louise, Saskatchewan River Crossing, Red Deer River Crossing, Nordegg..."*

This is a direct textual proposal for the minority's s.15(2)-invoking configuration by the submission's explicit name. The configuration with the *most visible engineering evidence* (the NP extension to reach the BC border that we identified in §2.4) is also the one with the *clearest public support* in the submissions — a finding that tightens the tension in the audit rather than resolving it.

**Rocky Mountain House-Banff Park — EBC-2025-2-0091** (Nordegg resident):

> *"I recommend that riding boundaries include all of Clearwater County, including Rocky Mountain House, with other western communities like Sundre and Banff."*

**Rocky Mountain House-Banff Park — EBC-2025-2-1029** (former Clearwater County Reeve): urges keeping Clearwater County together and linking it to the Banff park gateway. Directionally aligned with the minority configuration.

**Olds-Three Hills-Didsbury — EBC-2025-2-0209** (Alan Balson, Beiseker):

> *"Keep Beiseker and the surrounding rural area in a reconstituted rural riding that includes Olds, Didsbury, Carstairs, Three Hills, and the agricultural areas around them."*

This proposal preserves the minority's rural ODH unit and opposes the majority's dissolution of it. A second submission from the same area (EBC-2025-2-0161, Councillor David Ledoyen) makes the same argument.

**Red Deer hybrids — EBC-2025-2-0252** (Chad Krahn, Red Deer City Councillor):

> *"...a northern riding could encompass Sylvan Lake, Lacombe, and Blackfalds..."*

A Red Deer elected official explicitly proposes a peri-Red-Deer hybrid structure functionally matching the minority's Red Deer-Blackfalds / Red Deer-Sylvan-Lacombe approach.

**Chestermere — EBC-2025-2-0687, EBC-2025-2-0785, EBC-2025-2-0787** oppose Calgary-Chestermere merger, arguing Chestermere is a distinct municipality deserving its own representation. The minority map preserves Chestermere separately; the majority does not merge it either but uses a different configuration. These submissions support the principle the minority embodies rather than a specific minority label.

#### 5.4.3 Proportional weight and impact on findings

The proportions matter because they tell us whether the public-input record produces *signal* or *noise* for each configuration. Three interpretive lines:

**Sample-size caveat.** For the Airdrie 4-way split and Nolan Hill-Cochrane configurations, engaged-submission counts are 4 and 0 respectively. These are small samples. The absence of supporting submissions in 4 mentions is consistent with "no public support" but doesn't exclude the possibility that a larger sample would uncover some. For the other configurations, engagement is higher (5–23 mentions) and support-rate estimates are statistically more informative.

**Ridings with highest public engagement have the highest support rates for minority-aligned configurations.** Olds-Three Hills-Didsbury (40%), Chestermere (23%), and RMH-Banff Park (15% explicit, 35% with aligned) are the three configurations where citizens in the affected area engaged most actively, and all three show non-trivial alignment with the minority direction. This is the opposite of what the chair's claim implied. The pattern does not prove the minority configurations are correct — engaged citizens can be wrong — but it does refute the categorical "no public support" characterization.

**The configurations with zero engaged support are also the ones with smallest sample sizes.** Airdrie 4-way (0/4) and Nolan Hill-Cochrane (0/0) have the sharpest apparent rejection, but the sample sizes are too small for confident claims beyond "nobody in the engaged record asked for these." This is consistent with the chair's claim for those specific configurations but does not constitute a *refutation* of minority intent — it just means there is no recorded demand.

#### 5.4.4 Impact on the majority's and minority's findings

**For the majority report.** The "no public support" framing in Appendix C was a consequential argument. It implied the minority was advancing configurations against the clear weight of public input. The refutation evidence weakens this argument on three of five configurations. The majority's substantive cartographic critique — that the minority's hybrid choices are less compact and more fragmenting of communities (see §4.3, §4.4 of this audit) — still holds. But the *procedural* framing in Appendix C was overbroad.

**For the minority report.** The refutation helps the minority's procedural posture only modestly. Three configurations have documented support, which makes those three harder for the majority to discount. The visible spatial concerns (§C3: engineered RMH-Banff boundary, Nolan Hill-Cochrane lasso, ODH capturing N Airdrie) and the structural population asymmetries (§A1, §A2, §A2b) are not affected by the public-support question. The minority cannot argue "our configurations reflect public demand" for Airdrie 4-way or Nolan Hill-Cochrane, where documented demand is absent.

**For the audit's Section D procedural concern.** The §D critique narrows but does not disappear. The government's April 16 action replaced the commission drafting process in order to produce a map drawn from the less-publicly-vetted proposal. That concern is strongest for configurations that genuinely lack public support (Airdrie 4-way, Nolan Hill-Cochrane) and weaker — though not absent — for configurations that have some documented backing (RMH-Banff Park, Olds-ODH, Red Deer hybrids, Chestermere). An earlier framing of "government is pushing boundary choices nobody asked for" would overstate the record; the accurate framing is "government is pushing a mix, with some choices that have no public support and others that do."

#### 5.4.5 Limits of the verification

1. **~88 submissions (6.6%) could not be machine-parsed** because their PDFs are image-only scans lacking a text layer or a detectable EBC-2025-X-NNN ID marker. OCR was out of scope. These could in principle contain additional supporting or opposing content that would not change the refutation direction (which relies on identified supporting submissions) but could shift neutral / opposing counts.
2. **Keyword search precision.** Regex uses permissive co-occurrence windows (200–300 chars) and can miss submissions where the same configuration is described in paraphrased terms without the explicit place names used. Conversely, the Red Deer regex triggers on any Red Deer + {Blackfalds / Innisfail / Sylvan Lake / Lacombe} co-occurrence, which often simply describes the commission's *proposed* boundaries — those are neutrals, not supports.
3. **Position classifier is heuristic.** The code looks for support / oppose / against / recommend / should-not keywords near each match. Ambiguous classifications were manually reviewed and corrected in 13 cases (documented in `deprecated/submission_search_log.md`); CSV rows still reflect the automatic classification.
4. **Minority configuration names are the audit's labels, not the submissions'.** Citizens do not typically know the minority's precise labels (e.g., "Red Deer-Blackfalds"). A submission proposing a functionally equivalent configuration using different names is counted as directional support. The audit's rubric is generous on this point; the majority chair might not accept the same rubric.
5. **Attached sub-PDFs were not searched separately.** Some submissions reference external attachments (e.g., EBC-2025-1-0139 references "Airdrie-Feedback-Submission-AEBC-May-2025.pdf"); only the enclosing batch PDF's text layer was searched. Additional evidence may reside in attachments.

The refutation finding is robust to limits (1)–(3) because it rests on identified counter-examples rather than exhaustive enumeration. Limits (4) and (5) could affect counts but not direction of the finding. A full Track-B OCR pass over the 88 missing submissions would strengthen the audit's credibility if it were used in legal proceedings; it would not likely change the qualitative verdict.

### 5.5 Constitutional backdrop

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158, established that Canadian electoral redistribution is measured against an "effective representation" standard, not strict population parity. Within that standard, deviations from provincial average are permissible when they serve recognized factors (geography, community of interest, minority representation). An audit that finds (a) directionally-consistent partisan asymmetry in a proposal and (b) a process promoting that proposal over a more-neutral, more-publicly-supported alternative would implicate *Reference re Saskatchewan* if challenged — but this audit does not assess the constitutional question; it provides the evidentiary basis for others to do so.

---

## 6. Geometric Data Provenance (Section 4)

### 6.1 4A (direct shapefiles)

**Blocked.** Fetched `https://www.elections.ab.ca/resources/maps/` on 2026-04-22. 2019 ED shapefiles and 2023 VA shapefiles are published; 2026 proposal shapefiles are not. Consistent with ABEBC historical practice of releasing shapefiles after legislative adoption.

### 6.2 4B (DA dissolve)

**Not attempted.** Would require the 84MB `abebc_2026_rpt_final.pdf` and demonstrated presence of DAUIDs. Not in working bundle; probability of DAUIDs being in PDF text is low (<10% based on Canadian provincial commission practice).

### 6.3 4C (VA-polygon attribution)

**Pipeline validated; full execution not run.** Skeleton (`analysis/v0_1_poll_attribution_skeleton.py`) correctly parses the 2023 Statement of Vote: 1,973 poll records matched to four-figure official totals (NDP 777,404 / UCP 928,900 / two-party 1,706,304). Stages 3–7 (geocoding, zero-sum verification, 2026 assignment, apportionment, vote checksum) require ~4–8 hours of dedicated execution on VA-polygon substrate — outside this session's budget.

**Sub-finding (preserved for next session):** 47.2% of 2023 valid votes are in non-Election-Day ballot types (Advance/Mobile/Special), all home-ED-attributed under Vote Anywhere. NDP two-party share at Election Day: 42.59%. NDP two-party share Vote Anywhere: 48.84%. Differential: +6.25 pp. Implications for B1–B4 magnitude precision are covered in §3.4 sensitivity.

### 6.4 4D/4E

Not attempted. 4D (OSM reconstruction) would bust the 15K token sub-cap; 4E (QGIS manual) is out of scope.

### 6.5 4F validation

Not executed for the commission-released 2026 geometries because those shapefiles have not been released. A separate approximate-geometry analysis is described in §6.7 below.

### 6.7 Approximate 2026 geometry — Tier A/B compactness

Because the commission has not released 2026 shapefiles, this audit constructed approximate 2026 ED geometries from three sources: (a) the 2019 enacted shapefile for 2026 EDs whose crosswalk is `direct` or `rename` (Tier A, exact); (b) the union of constituent 2019 polygons for 2026 EDs with `merge` crosswalks (Tier B, near-exact); (c) an attempted hybrid-split approximation for `hybrid` crosswalks (Tier C, not attempted in this pass — visual transcription from the commission's low-resolution JPG maps would produce compactness errors of roughly ±20% per 10% perimeter error, which the audit judges too wide to report as measurement). Full method at `analysis/v0_1_approximate_shape_analysis.md`.

**Coverage of the approximation:**
- Majority 2026: 57 of 89 EDs measurable at Tier A/B (64%); 32 in Tier C (not scored).
- Minority 2026: 65 Tier A + 5 Tier B of 89 EDs measurable (79%); 19 in Tier C (not scored).
- 2019: all 87 EDs measurable directly.

**Measurable-subset compactness findings:**

| Map | Mean Polsby-Popper | Count PP < 0.25 | Count Reock < 0.30 |
|---|---|---|---|
| 2019 (87 EDs, full) | 0.419 | 4 / 87 (4.6%) | 6 / 87 (6.9%) |
| Majority 2026 (57 Tier A+B EDs) | 0.431 | 2 / 57 (3.5%) | 2 / 57 (3.5%) |
| Minority 2026 (70 Tier A+B EDs) | 0.411 | 5 / 70 (7.1%) | 5 / 70 (7.1%) |

**Within the measurable subset, the minority map shows roughly double the rate of low-compactness EDs (PP < 0.25, or Reock < 0.30) as the majority.** Minority's mean Polsby-Popper is modestly lower than either the 2019 baseline or the majority proposal. This is a directional finding, not a magnitude claim, because the measurable subset excludes the most structurally-complex EDs in both maps (hybrid splits, Tier C).

**Flagged-configuration analysis (Tier A/B measurable subset):** Three of the audit's flagged minority configurations are measurable as Tier A/B and do not degrade compactness relative to their 2019 parents (Airdrie-East PP 0.433, Red Deer-Blackfalds PP 0.551, Olds-Three Hills-Didsbury PP 0.383). The three Tier-C flagged hybrids (Rocky Mountain House-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) cannot be scored without an actual shapefile. A parent-union reference for these EDs shows their 2019-ancestor polygons are already low-compactness (e.g., the Banff-Kananaskis-adjacent parent union has PP ≈ 0.16); so low compactness in these EDs is partly inherited from the underlying Alberta geography rather than newly manufactured by minority split-lines.

**What the audit can and cannot claim from this data:**
- Can claim: within the measurable subset, the minority produces about twice the rate of low-compactness EDs as the majority does. This is consistent with the §C3 visual spatial-audit finding.
- Cannot claim: the minority "manufactures" non-compactness through hybrid splits. That claim requires the 2026 shapefiles because the hybrid splits are precisely the Tier C EDs the approximation could not score. The audit's scoped claim stands; the stronger claim is a pending research question.

**Refinement pass (v1).** A second pass re-extracted commission map pages at 600 DPI, snapped boundary lines to OpenStreetMap road-network features within a 500-metre buffer, and produced visual overlay verification for a priority subset. Methodology and full results at `analysis/v0_1_shape_refinement.md`. The v1 refinement shifted five Tier B EDs by an average of 97 metres and produced compactness confidence intervals of ≤ 0.04 Polsby-Popper for those EDs.

**Iterative refinement (v2) with feature-class-aware snapping.** Visual inspection of the v1 overlays surfaced that three of the five Tier B boundaries follow rivers rather than roads: Calgary-South along the Bow River (18 % river-feature samples), Edmonton-Windermere along the North Saskatchewan River (57 % river-feature samples), and Lethbridge-Little Bow along the Oldman River (45 % river-feature samples). A v2 pass extended the OSM query to four feature classes (road + waterway + railway + administrative-boundary) and re-snapped those boundaries to the appropriate feature. Compactness improved on the water-body-bounded EDs: Edmonton-Windermere PP 0.195 → 0.230 (+18 %); Calgary-South PP 0.217 → 0.240 (+11 %). Other EDs changed by ≤ 0.015 PP, within the CI. Full method at `analysis/v0_1_shape_refinement_v2.md`.

**Three-tier boundary-confidence classification** (after v3 noise-cleanup and two additional refinement passes). For each Tier B boundary the refinement pass computed a voter-assignment-impact score — the number of 2023 Voting Areas whose assignment would flip between the v1 and v2/v3 boundary rendering and the 2023 votes those VAs contain. Boundaries with zero sensitive VAs are marked **orange-accepted**: the residual geometric uncertainty does not affect voter assignment and further refinement would be effort without return. Lethbridge-Little Bow and Wetaskawin-Ponoka-Maskwacis are orange-accepted. Three boundaries remain documented as **unresolvable without the commission shapefile** after two additional refinement passes (admin-only snap at 100 m then 50 m buffer, river-only snap for Windermere): Calgary-De Winton and Calgary-South share a single sensitive VA (217 votes); Edmonton-Windermere has three sensitive VAs (796 votes) on the North-Saskatchewan-River bank — qualitatively resolved as "south of the North Saskatchewan River" via commission Appendix E, but the quantitative centreline-vs-bank offset remains shapefile-dependent. Total residual voter impact across all Tier B boundaries after v3: **1,012 votes across 4 unique VAs** — approximately 0.06 % of 2023 total valid votes. Per-boundary impact table at `data/v0_1_boundary_refinement_impact_v3.csv`; verification overlays with the three-tier green / orange / red convention at `maps/verification/v0_3_*.png` (v3 includes a rendering-bug fix: near-zero-area interior rings introduced by upstream buffer/union operations were being rendered as spurious "internal borders" by `GeoSeries.boundary.plot()`; v3 strips rings below 0.1 km² and renders only polygon-part exteriors).

**Tier B polygon misclassification flagged by human review.** Visual cross-reference of the v3 verification panels against the commission's published per-ED thumbnails (Appendix E) identified that Edmonton-Windermere, Calgary-De Winton, and Calgary-South are not actually Tier B "merges of whole 2019 parents" but Tier C carve-outs — the 2026 ED occupies only part of the 2019 parent territory, with the rest continuing under a separately-named 2026 ED (e.g., the minority keeps both Edmonton-Whitemud and creates Edmonton-Windermere). The approximation pipeline treated the 2026 ED as the union of parents, producing polygons that occupy more area than the commission actually drew and producing apparent overlaps with neighbouring EDs. Specifically, the commission's Edmonton-Windermere thumbnail shows a clean river-following western boundary PLUS a stepped upper-east carve-out where the ED wraps around a peninsula of Edmonton-South territory that extends northwest. The approximation misses this carve-out because it has no OSM feature to snap to (the carve is a commission-drawn street-grid boundary internal to the 2019 parent). The resulting apparent "overlap" with Edmonton-South reflects the approximation occupying territory the commission assigned to a neighbour through a feature OSM snapping cannot recover. It is not a rendering bug.

This misclassification is inherent to approximation-without-shapefile: every Tier B hybrid whose parent is carved rather than merged is subject to it. The impact-assessment above (0.06 % voter-impact residual) is conservative because it measures only v1-to-v3 symmetric difference, not the underlying approximation-to-reality gap for these Tier C-like EDs. The full voter-assignment gap for these EDs will be resolved only by shapefile release.

**Calgary-De Winton and Calgary-South — scale-level and shape-level misclassifications.** Visual cross-reference against the commission's minority Calgary overview (Appendix E p. 74) and individual per-ED thumbnails shows:

- **Calgary-De Winton** is a large south-Calgary / southern-suburban-rural hybrid that abuts the Tsuut'ina Nation reserve to the west, extends south past Calgary's city limits, and encompasses the Town of Okotoks (~32,000 residents) along with the De Winton community the district is named for. The v3 approximation renders as a small compact polygon internal to south Calgary — the approximation captures perhaps 10–15 % of the territory the commission actually assigned to this ED.
- **Calgary-South** as drawn by the commission is a compact roughly-rounded shape with a notch on the right side. The v3 approximation is an elongated east-west shape with an eastern extension and a southern tail — general location correct, shape materially wrong.

These are more severe misclassifications than Edmonton-Windermere (which had the general footprint correct with a missing peninsula). All three EDs are reclassified from Tier B to **Tier C awaiting shapefile**. The approximation's compactness scores for these three EDs should be read as known-inaccurate; the shared 217-vote residual between Calgary-De Winton and Calgary-South under the v3 symmetric-difference metric is a floor, not a ceiling, on the approximation-to-reality gap. Full mismatch documentation and commission-thumbnail observations at `analysis/v0_1_commission_reference_shapes.md`. Only commission shapefile release will resolve the gap. The §3.12 finding that Calgary-De Winton and Calgary-South "are measurable as Tier A/B" is withdrawn; §6.7's Tier count is revised downward by 3 measurable EDs on the minority side.

**Confidence versus actual commission shapefiles** (after v2):
- Tier A (57 majority / 65 minority EDs): high — geometry is the 2019 enacted shapefile, which is authoritative.
- Tier B orange-accepted (2 of 5): high — residual geometric uncertainty does not affect voter assignment.
- Tier B refinement-significant (3 of 5): moderate — ±500 m boundary residual with a ≤ 0.06 % province-wide vote-share implication; resolvable by shapefile release.

**Priority hybrid EDs not scored.** The hybrid configurations most relevant to the audit's contested-configurations findings (Rocky Mountain House-Banff Park, Calgary-Nolan Hill-Cochrane, Calgary-Peigan-Chestermere) are precisely the boundaries the approximation cannot construct from the 2019 shapefile + crosswalks alone; they require actual commission geometry. Until the commission shapefiles are released by Elections Alberta (request drafted at `analysis/v0_1_elections_alberta_shapefile_request.md`), the audit's compactness findings cover the measurable 64–79 % of each map but leave the three most contested EDs unscored.

### 6.6 Technical Data Statement

- **Source data for Sections A, B:** CSV files in `data/` (populations for both 2026 maps; per-ED 2023 and 2019 vote totals); raw Statement of Vote in `data/2023_results.xlsx`.
- **Source data for Section C:** JPG map images from the commission's final report (majority Calgary only; full coverage for minority).
- **Source data for Section D:** Electoral Boundaries Commission Act, commission report via prompt context, comparator-case general knowledge.
- **Geometric reconstruction:** Not produced. §6.1–6.5 explain each path's block.
- **Coordinate system / resolution / aggregation:** N/A (no geometry).
- **Integrity metric:** Population checksum threshold (0.5% warn, 2% hard stop) not triggered because no geometry to check.
- **Geometric shift log:** `analysis/geometry_shift_log.md` does not exist. No manual geometric adjustments were applied in this session.
- **Transformation log:** No CRS transformations applied.
- **Symmetry consistency:** B1–B4 use identical blending methodology (70/30 urban weight) applied to both 2026 maps via the same `estimate_2026()` function. A1–A3 use identical variance computation against the same provincial average. A2 uses identical classification rule plus an alternative-rule robustness check (G4). Section C has a symmetry data gap (only majority Calgary imagery available) which is disclosed.

---

## 7. Synthesis — Six-Dimensional Finding

| Dimension                                          | 2019         | Majority 2026          | Minority 2026          | Direction of minority shift |
| -------------------------------------------------- | ------------ | ---------------------- | ---------------------- | --------------------------- |
| §A1 Population MAD from avg                        | (not run)    | 3,180                  | **4,707** (+48%)       | wider dispersion            |
| §A2 Calgary Zone A − Zone B gap                    | (not run)    | +0.36%                 | **+12.20%**            | packing signal              |
| §A2 robustness (2023 winner-based)                 | (not run)    | +0.39%                 | **+7.71%**             | survives robustness check   |
| §A2b Rest-of-province mean population              | (not run)    | 52,281                 | 50,336 (−3.9%)         | rural overrepresentation    |
| §A3 s.15(2) failures engineered via visible boundary| 0           | 0 (Canmore-Banff undetermined) | 1 (RMH-Banff Park) | engineered qualifications   |
| §B2 Efficiency gap                                 | −2.64%       | −0.85%                 | **−1.36%**             | +0.58 pp more UCP-favorable |
| §B2 sensitivity range (urban weights 0.60–0.80)    | —            | [+1.58% to −1.43%]     | [+0.22% to −3.04%]     | +0.58 to +1.61 pp across range |
| §B3 Mean-median gap                                | −2.22 pp     | −0.16 pp               | −0.33 pp               | directionally consistent    |
| §B4 NDP seats at 50/50                             | 46           | 44                     | 42                     | 2-seat reduction for NDP    |
| §C3 Visible spatial anomalies                      | —            | 0 (Calgary only)       | 3 (all confirmed)      | three anomalies             |
| §C4 Airdrie splits                                 | —            | 2 EDs                  | 4 EDs                  | double split                |
| §D Procedural                                      | —            | Standard override path  | Government-controlled drafting | departure from comparators |

Six independent dimensions of evidence point in the same direction. None individually crosses a statistical significance threshold. Together, the directional consistency is the finding — the minority proposal, relative to the majority, shows more structural irregularities and, under 2023 voter geography, lower measured-partisan-neutrality at a sub-threshold magnitude, across six measurement frameworks.

**Scope discipline and small-magnitude calibration.** The six-dimensional framing follows the four-axis redistricting-audit discipline of Altman and McDonald (2011) and the consistency-across-N methodology of Katz, King, and Rosenblatt (2020): when single dimensions are underpowered, cross-dimensional agreement is the inferential artefact, not any individual magnitude. Each dimension's magnitude is small by design — the audit is not claiming a single five-alarm effect. Terms used in this paper carry calibrated meaning: *measurable* means "the computed statistic's confidence interval does not include zero at the stated confidence level"; *directional* means "the sign is consistent across all runs" without magnitude claim; *systematic* means "the same direction appears in multiple independent tests." These are not synonyms and are not interchangeable. A hostile reader entitled to read the audit as "the paper called small differences patterns" receives the following response: the patterns are defined precisely, apply to six independent tests, and persist across 90.5% of Monte Carlo samples (seed 42, N = 2,000), across 338Canada's April 2026 polling input, and across a symmetric test-selection audit that revealed additional minority-map patterns (Lethbridge and Red Deer 4-way splits, §3.12) not present in the majority.

Three qualifications inherited from the stress-test pass narrow this synthesis:

- Under the Chen-Rodden (2013) natural-packing framing (see §3.6), some portion of the minority-to-majority partisan-bias gap is not attributable to engineering — it reflects how any neutral map interacts with Alberta's urban-NDP / rural-UCP geography. This lowers the claim from "the minority was engineered against the NDP" to "the minority produces more UCP-favourable results under 2023 voter geography." The structural findings (§A population equality, §A2 Calgary zone gap, §C3 visible anomalies, §C4 community splits, §D procedural) are not affected by the natural-packing caveat because they measure geographic and procedural properties the natural-packing argument does not address.
- Under RT3 (cross-election stability), the vote-based asymmetry flips sign when 2019 votes replace 2023 votes. The six-dimension synthesis rests mostly on the structural dimensions; the single vote-based dimension (§B) is qualified accordingly.
- Under the submission-archive verification (§5.4), the procedural concern rests primarily on the two configurations without documented public support (Airdrie 4-way, Nolan Hill-Cochrane) rather than on the chair's full five-item sweep.

---

## 8. Mathematical Formalism

### 8.1 Efficiency Gap (Stephanopoulos & McGhee, 2014)

$$\text{EG} = \frac{W_A - W_B}{N}$$

```
EG = (W_A - W_B) / N
```

Wasted votes $W_X$ for party $X$ are defined as losing-district votes plus winning-district votes above the victory threshold $\lceil N_d/2 \rceil + 1$, summed across districts. The 7% magnitude is the threshold flagged in *Gill v. Whitford* (2018).

**Sign-convention reconciliation.** When party A is indexed first, Stephanopoulos-McGhee canonical EG uses a 2:1 slope baseline (positive EG = party A disadvantaged, i.e., party B has seat-advantage). This paper reports EG under the 1:1 proportional-seat baseline; in Alberta's rural-UCP-blowout context, this produces negative EG values whose magnitude correlates with UCP outcome advantage through seat count, despite UCP also being the more-wasteful party by the wasted-vote measure. The two conventions give the same ordinal ranking of Alberta's three maps (2019 / Majority 2026 / Minority 2026) and therefore the same minority-vs-majority direction. Full derivation and verification at `analysis/v0_1_sign_convention_resolution.md`.

### 8.2 Mean-Median Gap (McDonald & Best, 2015)

$$\text{MM} = \bar{v} - \tilde{v}$$

```
MM = mean(v) - median(v)
```

$\bar{v}$ is the mean NDP vote share across districts; $\tilde{v}$ is the median. Positive MM indicates mean > median, consistent with party voters packed into fewer high-share districts (cracking of the opposing party, or packing of own party).

### 8.3 Polsby-Popper compactness (not computed — blocked by Phase 4)

$$\text{PP} = \frac{4\pi A}{P^2}$$

```
PP = 4 * pi * A / P^2
```

$A$ = polygon area, $P$ = perimeter. Range $[0, 1]$; 1 = circle. PP < 0.15 is typically flagged.

### 8.4 Reock compactness (not computed — blocked by Phase 4)

$$\text{R} = \frac{A_d}{A_c}$$

```
R = A_district / A_smallest_enclosing_circle
```

Range $[0, 1]$. R < 0.25 typically flagged.

---

## 9. Missing Evidence and Scope Limits

1. **2026 polygon geometry.** Phase 4A blocked. Unlocks B5 MCMC ensemble (Phase 5 §5.2), C1 Polsby-Popper, C2 Reock.
2. **Measured vote attribution (Phase 4C full execution).** Replaces 70/30 blend with observed apportionment. Expected to reduce the sensitivity range in §3.4 to a single refined value.
3. **Independent verification of the no-public-support claim (Section D).** Requires text-search of the commission's 1,140+ submission archive.
4. **Full-symmetry visual audit for majority.** Requires majority-proposal Alberta overview, Edmonton, and other-cities map images.
5. **2019-era population data.** Would permit A1/A2 symmetric analysis of the 2019 baseline alongside the two 2026 proposals.

## 10. Falsifiability Statement

The audit's directional claim — *minority more UCP-favorable than majority across population, spatial, partisan-bias, and procedural dimensions* — would be falsified by any of the following:

- An alternative Calgary classification that produces near-null minority-majority asymmetry (≤1%) while A2's current rule produces >10%. Tested; both rules produce the same direction.
- Phase 4C measured attribution producing a minority-majority efficiency-gap asymmetry opposite in sign, or below 0.005 pp at the 70/30 central weight.
- Submission-archive evidence that the five disputed minority configurations (Airdrie, Cochrane, Chestermere, Red Deer, St. Albert) did have substantial public support in the 1,140+ record. Refutes Section D claim.
- Visible spatial anomalies in the majority's rural or Edmonton districts of a severity comparable to the minority's three flagged ridings. Requires majority non-Calgary imagery.
- A comprehensive survey of Canadian provincial redistributions 1991–2025 finding comparable mid-cycle government-drafting-process replacements. Refutes Section D uniqueness framing.

## 11. Legal Interpretive Note

This audit does not offer a legal conclusion. It provides the evidentiary basis on which a legal challenge under *Reference re Saskatchewan* [1991] 2 SCR 158's "effective representation" standard could be constructed. The question whether the minority proposal, as potentially modified by the November 2, 2026 MLA-committee process, would satisfy the effective-representation requirement is for counsel and the courts to assess. The audit's core contribution is documenting that:

1. The two commission proposals diverge systematically on six measurable dimensions.
2. The direction of divergence consistently favors the governing party.
3. The process being used to promote the more-favorable proposal departs from comparator Canadian practice in specific ways.

These facts are reproducible from public data using checked-in code. They do not prove intent, and they do not by themselves establish a constitutional violation.

**Saskatchewan Reference framing.** The "effective representation" standard established in *Reference re Provincial Electoral Boundaries (Saskatchewan)* [1991] 2 SCR 158 is permissive on deviation from population equality: McLachlin J (as she then was) wrote that the guarantee of §3 is "the right to effective representation" (para. 26), and that "relative parity of voting power" must be weighed against other factors "including geography, community history, community interests and minority representation" (para. 33). *Raîche v. Canada (Attorney General)*, [2004] FC 679, and *Cassista v. Canada (Attorney General)*, 2014 FC 398, apply the standard to specific boundary disputes without producing a bright-line ceiling on partisan-asymmetric outcomes. Under this standard, a map's constitutional status depends on whether its deviations are reasonably related to permitted factors. The audit's findings — directional partisan asymmetry, engineered s.15(2) boundaries, cracking patterns visible across three cities, and procedural departure from independent-commission practice — are the kinds of evidence a court applying the effective-representation standard would weigh. Whether that weighing produces a constitutional violation is for a court, not this audit, to determine.

---

## Note on population-data provenance and cycle-lag robustness

The body of this report performs all population-equality analysis against the 2021 decennial Statistics Canada census, the data source the Electoral Boundaries Commission Act §12(3) designates as the Commission's mandatory basis. Two supplementary observations sit outside the census-based analysis and are recorded here for completeness; neither alters the report's findings.

**Commission methodology vs statutory basis.** The majority and minority reports both state that population figures derive from "the 2021 census updated to a July 1, 2024 estimate." The per-ED population tables in both reports sum to 4,888,723 — the Alberta Treasury Board and Finance mid-2024 estimate — and the resulting provincial quota (54,929) and ±25 % window (41,197 – 68,661) are computed from the 2024 total rather than from the 2021 census total of 4,262,635. Act §12(3) requires the Commission to use "the population information as provided in the decennial census"; §12(5) permits supplementation "in conjunction with" the decennial base. Whether the Commission's approach falls within §12(5)'s permissive frame or outside it is a question of statutory interpretation not resolved here. Full compliance audit in `analysis/v0_1_plan_b_cross_check.md`. The audit's own A1/A2/A3 analyses in §2 above were performed against the Commission's published per-ED tables and therefore inherit the Commission's data vintage; a Plan-B re-run against the same 2024 estimates finds every justification-test verdict unchanged and three tests (Olds-Three Hills-Didsbury, Airdrie 4-way, Chestermere split) more decisively "unforced" than under the 2021 census.

**Cycle-lag robustness test.** Alberta's cumulative population growth from the 2021 census to mid-2025 is approximately 17.8 %. Applying mid-2025 populations to the three maps (2019 current, 2026 majority proposal, 2026 minority proposal) using a dissemination-area-level area-weighted overlay produces the following count of electoral divisions whose ±25 % window status changes relative to the commission's 2024-based figures: 2019 map, 5 of 87 (all pass → fail); majority 2026, 0 of 89; minority 2026, 5 of 89 (Calgary-North East, Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo, Peace River all pass → fail; Lesser Slave Lake's s.15(2) ratio to the updated mean drops past −50 %). The asymmetry is a second-order signal — population-equality robustness under the 4–14-year lag the current redistribution cycle imposes — and is consistent in direction with the report's A1/A2 findings. Details and reproducible pipeline in `analysis/v0_1_cycle_lag_analysis.md`. The Commission's legal baseline is not affected by this observation; the statutory test uses the decennial census. A legislative reform proposal addressing the underlying §12 ambiguity is in `analysis/v0_1_act_amendment_proposal.md`.

**Open questions raised by the data.** The Plan B and cycle-lag observations surface empirical and interpretive questions the audit does not resolve:

1. **Current-map statutory status.** Whether the 2019-enacted 87-seat configuration satisfies the Act's ±25 % requirement as of mid-2025. Observed: 5 of 87 EDs sit outside the window under DA-level aggregation of mid-2025 populations. If the 2027 general election runs on the 2019 boundaries (because the April 16 process does not produce an adopted map in time), the question is live.
2. **Operative force of §12(3).** Whether the Commission's published methodology (2024 TBF estimate as per-ED basis; provincial quota derived from 2024 total) falls within §12(5)'s "in conjunction with" frame. Either interpretation has consequences: a permissive reading hollows out the decennial-census rule as a legal check; a restrictive reading destabilises every per-ED figure in both 2026 commission reports. The question is for counsel and, if litigated, for courts.
3. **Source of the Majority (0) / Minority (5) Plan-B asymmetry.** Partly attributable to initial population-distribution variance (Majority MAD 3,180 vs Minority MAD 4,707, a 48 % wider spread at the Commission's own data vintage): the same growth shock pushes more minority districts across a threshold they were already closer to. The residual invites district-level close reading of which specific boundaries were drawn near the ±25 % margin in each map's original design.
4. **Lesser Slave Lake s.15(2) eligibility.** Whether the district's loss of s.15(2) qualifying ratio under mid-2025 populations is a cycle-lag artifact or a durable geographic change. The distinction matters for how the special-remote-district provision ages across long redistribution cycles and bears on the structural case for shortening the cycle or amending §15.
5. **A2 Calgary zone-gap persistence at finer resolution.** No measured ward-level Calgary population data exists for 2022–2026 in public circulation; the City of Calgary cancelled its civic census in 2020, with reinstatement scheduled for 2027. A modelled 2024 / 2025 ward-level population estimate can be constructed from public inputs — 2021 Census ward totals, StatsCan Table 17-10-0142 citywide postcensal estimates, the City's Suburban Residential Growth Forecast (per-sector population increments), the Communities-by-Ward crosswalk, and geocoded building permits — and would serve as a sensitivity check on the A2 finding's robustness to intercensal drift. The audit has not executed this sensitivity pass; it is catalogued as a pending item in `analysis/v0_1_calgary_data_sources_audit.md`. The legal-baseline A2 test necessarily remains 2021-vintage.
6. **Commission methodology disclosure more broadly.** The audit identified one material disclosure–practice inconsistency (population-data vintage). Whether other disclosures — the weighting of "community of interest," the treatment of s.15(2) thresholds, the Appendix C / Appendix E crosswalk construction — are similarly imprecise is outside the scope of this report and would require a separate methodological audit of the commission's full record.

---

## Appendix C — 2021-census legal-baseline A1 for the 2019 map

**Purpose.** §2.1 reports A1 MAD on the commission's own tables, which derive from the July 2024 OSI population estimate. A reviewer committed to strict §12(3) statutory-basis discipline can argue the §2.1 numbers inherit the commission's data-source status. This appendix provides an independent 2021-Census-direct computation of A1 on the 87 existing 2019 EDs as the §12(3)-operative reference point. The 2026 proposals cannot receive the equivalent treatment because their ED shapefiles have not been publicly released.

**Method.** 2021 Census population at the dissemination-area level (6,203 Alberta DAs, `data/alberta_2021_da_populations.csv`) aggregated to the 87 2019 EDs via geopandas overlay on `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`. Reproducible script at `analysis/v0_1_a1_legal_baseline_2021_census.py`. Per-ED output at `data/v0_1_a1_legal_baseline_2019eds_2021census.csv`.

**Headline figures.**

| Map & basis | Quota | MAD | Source |
|-------------|-------|------|--------|
| 2019 map on 2017-report basis (commission-quoted) | 46,803 | 2,886 | EBC 2017 Final Report pp. 60–61 |
| 2019 map on 2021 Census (this appendix) | 48,996 | **4,745** | This computation |
| 2026 majority map on 2024 TBF estimate | 54,929 | 3,180 | Majority Report variance table |
| 2026 minority map on 2024 TBF estimate | 54,929 | 4,707 | Minority Report variance table |

**Ordinal comparison.** 2026 majority MAD (3,180) < 2019-on-2021-Census MAD (4,745) ≈ 2026 minority MAD (4,707). The minority 2026 proposal's distribution-tightness is effectively equal to the 2019 map's distribution-tightness at 2021-Census time; the majority 2026 proposal is meaningfully tighter than either benchmark.

**Seven 2019 EDs outside ±25 % under 2021 Census.** Central Peace-Notley (−44.77 %), Lesser Slave Lake (−44.73 %) — both s.15(2)-protected — plus Edmonton-South (+40.89 %), Edmonton-Ellerslie (+38.60 %), Edmonton-South West (+33.71 %), Airdrie-Cochrane (+29.76 %), Calgary-North East (+25.55 %). The five positive outliers are urban-growth EDs that had already exceeded the +25 % ceiling by 2021-census time; Track L's mid-2025 analysis (`analysis/v0_1_cycle_lag_analysis.md`) confirms all five remain out-of-band under 2025 populations.

**Interpretation.** The audit's §2.1 ordering (majority tighter than minority) is preserved under the §12(3)-operative basis. The minority proposal, drawn four years after the 2021 Census, reproduces the same population-distribution tightness the 2019 map exhibited against the 2021 Census; the majority proposal improves on that benchmark. A strict §12(5) reviewer's attack on §2.1's data basis does not change the direction of the A1 finding. Full discussion in the companion file `analysis/v0_1_appendix_c_legal_baseline.md`.

---

## Appendix A — Reproducibility

All scripts run from repository root:

```bash
python3 analysis/v0_2_packing_cracking_analysis.py    # §B symmetric three-map
python3 analysis/electoral_forensics_population.py    # §A with A2 robustness
python3 analysis/v0_1_poll_attribution_skeleton.py    # §4 parse validation
```

Each script prints a gate PASS/FAIL line. Numbers in §§2, 3 above must match the corresponding gate-passed output.

**Reproducibility artifacts.** A version-pinned environment manifest (`requirements.txt` at repo root) lists every Python package with exact version; an interpreter pin (`setup.md`) names the tested Python version; `FROZEN_MANIFEST.md` lists every external URL accessed during the audit with its access date. A third party running the pipeline 12+ months from today can (a) install the pinned environment, (b) check each URL's state against the frozen snapshot, and (c) reproduce every numeric finding to the tolerance stated in Gate G0. Reproducibility-artifact provenance follows the ICLR 2022 Reproducibility Checklist and Nosek et al. (2018) Open Science Framework pre-registration standards.

## Appendix B — Section Documents

- [Section A](analysis/v0_1_section_A_population_equality.md)
- [Section C](analysis/v0_1_section_C_geographic_coherence.md)
- [Section D](analysis/v0_1_section_D_procedural.md)
- [Section 4](analysis/v0_1_section_4_geometry_provenance.md)
- [Bias audit](analysis/v0_1_bias_audit.md) — self-audit of this audit's own methodology
- [Design critique](analysis/v0_1_design_critique.md) — hostile stress-test pass
- [Uncertainty analysis](analysis/v0_1_uncertainty_and_shapefile_impact.md)
- [Academic literature review](analysis/v0_1_academic_literature_review.md)
- [Submission search findings](analysis/submission_search_findings.md) — §5.4 evidence base
- [Chair's Recommendation 5 analysis](analysis/v0_1_chair_recommendation_5_analysis.md) — §5.2 evidence base
- [Track C checklist baseline scoring](analysis/v0_1_track_c_checklist_baseline_scoring.md) — §3.11 full scorecard and comparison template for the November map
- [Plan B compliance + contested-config cross-check](analysis/v0_1_plan_b_cross_check.md) — note on population-data provenance evidence base
- [Cycle-lag analysis](analysis/v0_1_cycle_lag_analysis.md) — province-wide ED drift under mid-2025 populations
- [Proposed Act §12 amendment](analysis/v0_1_act_amendment_proposal.md) — legislative reform proposal addressing the census / cycle-lag tension
- [Calgary data-sources audit](analysis/v0_1_calgary_data_sources_audit.md) — 16 Calgary-specific sources catalogued; ward-level modelled A2 sensitivity is feasible from public data
- Adversarial stress-test passes and their fortifications are preserved in `deprecated/` for historical reference (see `deprecated/README.md`).
- [Chen-Rodden Alberta validation](analysis/v0_1_chen_rodden_alberta_validation.md) — mechanism-level test of the natural-packing argument
- [Canadian redistribution base-rate catalogue](data/v0_1_canadian_redistribution_base_rate.csv) — C4 partial catalogue (quantitative acquisition flagged as future work)
- [Alberta government database survey](analysis/v0_1_alberta_government_databases_survey.md) — Track N, composite-basis source recommendations for §12 reform
- [Commission source provenance audit](analysis/v0_1_commission_source_provenance.md) — Track O, verified 4,888,723 matches StatsCan Q2 2024 postcensal estimate
- [Byelection data and assessment](analysis/v0_1_byelection_assessment.md) — Track S, 2022–2025 byelections evaluated and not incorporated into RT3
- [A1 legal-baseline computation](analysis/v0_1_appendix_c_legal_baseline.md) — Appendix C companion; 2019-map MAD on 2021 Census directly
- [Threshold provenance compendium](analysis/v0_1_threshold_provenance.md) — every numeric threshold justified with source + sensitivity
- [Canadian inter-map base-rate computation](analysis/v0_1_canadian_base_rate_computed.md) — comparative distribution across seven Canadian redistribution cycles
- [External pre-registration draft and platform analysis](analysis/v0_1_pre_registration_draft.md) / [platform analysis](analysis/v0_1_pre_registration_platform_analysis.md) — OSF submission package for the November signature-detection checklist
- [Minority rationales validation](analysis/v0_1_minority_rationales_validation.md) — §4.4 and §5.2 evidence base (25 rationales inventoried, 3 contradicted)
- [Minority rationales inventory](analysis/v0_1_minority_rationales_inventory.md) — source quotes with citations
- [Cochrane journey-to-work](analysis/v0_1_cochrane_journey_to_work.md) — §4.4 StatsCan 98-10-0459 pull
- [CSD-level community splits](analysis/v0_1_csd_community_splits.md) — §4.4 robustness check
- [338Canada riding-level cross-validation](analysis/v0_1_338canada_riding_level.md) — §3.5 independent cross-check
- Submission OCR log preserved at `deprecated/v0_1_submission_ocr_log.md` — §5.4 partial extension of the 88 non-text-layer submissions

---

## References

Citations follow American Political Science Association (APSA) / APA-7 hybrid style, appropriate for political science, statistics, and information systems literature. Court cases follow Canadian legal citation convention.

### Academic literature

Alberta Electoral Boundaries Commission [AEBC]. (2026). *2025–26 Electoral Boundaries Commission final report (majority and minority)*. Government of Alberta. https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf

Barnes, R., & Solomon, J. (2021). Gerrymandering and compactness: Implementation flexibility and abuse. *Political Analysis, 29*(4), 448–466. https://doi.org/10.1017/pan.2020.36

Bratt, D., Brown, K., Sayers, A., & Taras, D. (Eds.). (2019). *Orange chinook: Politics in the new Alberta.* University of Calgary Press.

Carty, R. K. (2017). *Big tent politics: The Liberal party's long mastery of Canada's public life.* UBC Press.

Chen, J. (2017). The impact of political geography on Wisconsin redistricting. *Election Law Journal, 16*(4), 443–452. https://doi.org/10.1089/elj.2017.0455

Chen, J., & Rodden, J. (2013). Unintentional gerrymandering: Political geography and electoral bias in legislatures. *Quarterly Journal of Political Science, 8*(3), 239–269. https://doi.org/10.1561/100.00012033

Courtney, J. C. (2001). *Commissioned ridings: Designing Canada's electoral districts.* McGill-Queen's University Press.

Courtney, J. C. (2004). *Elections.* UBC Press.

DeFord, D., Duchin, M., & Solomon, J. (2021). Recombination: A family of Markov chains for redistricting. *Harvard Data Science Review, 3*(1). https://doi.org/10.1162/99608f92.eb30390f

Fifield, B., Imai, K., Kawahara, J., & Kenny, C. T. (2020). The essential role of empirical validation in legislative redistricting simulation. *Statistics and Public Policy, 7*(1), 52–68. https://doi.org/10.1080/2330443X.2020.1791773

Gelman, A., & King, G. (1994). A unified method of evaluating electoral systems and redistricting plans. *American Journal of Political Science, 38*(2), 514–554. https://doi.org/10.2307/2111417

Grofman, B. (1983). Measures of bias and proportionality in seats-votes relationships. *Political Methodology, 9*(3), 295–327.

Herschlag, G., Ravier, R., & Mattingly, J. C. (2020). Quantifying gerrymandering in North Carolina. *Statistics and Public Policy, 7*(1), 30–38. https://doi.org/10.1080/2330443X.2020.1796400

Katz, J. N., King, G., & Rosenblatt, E. (2020). Theoretical foundations and empirical evaluations of partisan fairness in district-based democracies. *American Political Science Review, 114*(1), 164–178. https://doi.org/10.1017/S000305541900056X

King, G., & Browning, R. X. (1987). Democratic representation and partisan bias in congressional elections. *American Political Science Review, 81*(4), 1251–1273. https://doi.org/10.2307/1962588

Ladner, K. (2003). Treaty federalism: An Indigenous vision of Canadian federalisms. In F. Rocher & M. Smith (Eds.), *New trends in Canadian federalism* (pp. 167–194). Broadview Press.

McDonald, M. D., & Best, R. E. (2015). Unfair partisan gerrymanders in politics and law: A diagnostic applied to six cases. *Election Law Journal, 14*(4), 312–330. https://doi.org/10.1089/elj.2015.0318

Pal, M. (2015). The fragmentation of party politics and the rise of political fixers. *University of Toronto Law Journal, 65*(3), 293–324. https://doi.org/10.3138/utlj.2767

Pal, M. (2019). The Charter and the constitutionality of electoral boundaries. *Canadian Journal of Law and Jurisprudence, 32*(2), 323–346. https://doi.org/10.1017/cjlj.2019.16

Polsby, D. D., & Popper, R. D. (1991). The third criterion: Compactness as a procedural safeguard against partisan gerrymandering. *Yale Law & Policy Review, 9*(2), 301–353.

Reock, E. C. (1961). Measuring compactness as a requirement of legislative apportionment. *Midwest Journal of Political Science, 5*(1), 70–74. https://doi.org/10.2307/2109043

Sancton, A. (2021). *The limits of boundaries: Why city-regions cannot be self-governing.* McGill-Queen's University Press.

Smith, D. E. (2010). *Canada's deep crown: Beyond Elizabeth II.* University of Toronto Press.

Stephanopoulos, N. O., & McGhee, E. M. (2014). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review, 82*(2), 831–900.

Stephanopoulos, N. O., & McGhee, E. M. (2018). The measure of a metric: The debate over quantifying partisan gerrymandering. *Stanford Law Review, 70*, 1503–1568.

Stewart, D., & Archer, K. (2000). *Quasi-democracy? Parties and leadership selection in Alberta.* UBC Press.

Warrington, G. S. (2018). Quantifying gerrymandering using the vote distribution. *Election Law Journal, 17*(1), 39–57. https://doi.org/10.1089/elj.2017.0447

Warrington, G. S. (2019). A comparison of partisan gerrymandering measures. *Election Law Journal, 18*(3), 262–281. https://doi.org/10.1089/elj.2018.0508

Wiseman, N. (2020). *Partisan odysseys: Canada's political parties.* University of Toronto Press.

### Court cases

*Figueroa v. Canada (Attorney General)*, [2003] 1 SCR 912.

*Frank v. Canada (Attorney General)*, [2019] 1 SCR 3.

*Gill v. Whitford*, 585 U.S. ___ (2018).

*Haig v. Canada*, [1993] 2 SCR 995.

*Reference re Provincial Electoral Boundaries (Saskatchewan)*, [1991] 2 SCR 158.

### Statutes

*Electoral Boundaries Commission Act*, RSA 2000, c E-3.

### Data sources

Elections Alberta. (2015). *2015 Provincial general election official results* [Data set]. https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx

Elections Alberta. (2019). *2019 Provincial general election official results all EDs* [Data set]. https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx

Elections Alberta. (2023). *2023 Provincial general election statement of vote* [Data set]. https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx

Elections Alberta. (2026). *Electoral boundaries commission submissions archive* [Data set, Rounds 1 and 2]. https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/

Statistics Canada. (2021). *Dissemination area boundary files, 2021 census* [Data set]. https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/

---

*Draft. Falsifiability gates, robustness checks, and APA citations documented throughout.*
