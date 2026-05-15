# Adapting this audit to other jurisdictions

This document is for the next researcher — whether running Alberta 2031, BC 2028, Saskatchewan 2029, or a federal redistribution cycle — who wants to apply this methodology without starting from scratch. The audit was designed with portability in mind: the statistical pipeline is jurisdiction-agnostic, and the configuration layer separates jurisdiction-specific parameters from the analysis code.

**What transfers directly.** The MCMC neutral-ensemble framework (GerryChain ReCom), SZAT boundary-choice test, Mahalanobis D² joint outlier score, Fisher combination, population-equality tests, and pre-registration discipline all work on any two-party plurality system with geographically nested electoral districts. Canadian federal ridings, Quebec MNAs, and BC MLAs all fit.

**What requires adaptation.** Party labels, shapefile paths, column names, and geographic calibration constants are jurisdiction-specific. This document tells you exactly what to change and where.

---

## 1. What you need (minimum data requirements)

| Data | Format | Notes |
|---|---|---|
| Official electoral district boundaries for both candidate maps | GeoPackage or Shapefile, projected CRS (not WGS84) | Elections Alberta used EPSG:3400; Elections BC uses EPSG:3005 |
| Voting-area-level election results from at least one recent election | CSV or GeoPackage with polygon geometries and per-party vote totals | The VA layer is the spatial join substrate. Statistics Canada Voting Areas (SVPs) work for federal; provincial VAs differ by province |
| Population data by electoral district (commission's own tables) | CSV | Usually published in the commission's appendices |
| Reference boundary from the previous cycle (enacted baseline) | Same format as candidate maps | Used to establish the neutral-ensemble starting point and SZAT swing-zone definition |

**Nice to have but not blocking:** DA-level population boundaries (for anchoring analysis), CSD municipal boundaries (for community-of-interest anchoring), and 338Canada-style polling projections for historical stability probes.

---

## 2. What to change — the adaptation checklist

### `config.yaml`

This is the single-file adaptation point. Every jurisdiction-specific value lives here.

```yaml
# Step 1: Update map paths and ID columns
maps:
  map_a:                          # rename from "majority" or the "preferred" map
    path: "data/shapefiles/canonical/<your_map_a>.gpkg"
    id_col: "<your_ed_name_column>"
  map_b:                          # rename from "minority" or the "alternative" map
    path: "data/shapefiles/canonical/<your_map_b>.gpkg"
    id_col: "<your_ed_name_column>"
  reference:
    path: "data/shapefiles/reference/<previous_cycle>.shp"
    id_col: "<previous_ed_name_column>"

# Step 2: Update substrate column names
substrate:
  path: "data/shapefiles/derived/<your_va_layer>.gpkg"
  columns:
    party_1_votes: "<incumbent_party_va_column>"   # votes for the governing party
    party_2_votes: "<opposition_party_va_column>"  # votes for the main opposition
    other_votes: "<other_votes_column>"
    population: "<population_column>"
    geographic_id: "<va_unique_id_column>"

# Step 3: Update party labels and roles (when Track F is implemented)
parties:
  incumbent: "<GovernmentPartyAbbreviation>"       # e.g., "Liberal", "NDP", "UCP"
  opposition: "<OppositionPartyAbbreviation>"
  incumbent_historical: "<HistoricalLabel>"        # for cross-election data spanning a party name change

# Step 4: Update election metadata (when Track G is implemented)
elections:
  current_year: <most_recent_election_year>
  boundary_year: <year_new_boundaries_take_effect>
  baseline_years: [<previous_election_1>, <previous_election_2>]

# Step 5: Update audit constants
audit:
  expected_districts: <number_of_seats>
  expected_total_votes: <total_two_party_votes>
  crs_epsg: <your_projected_crs>
```

### `analysis/scripts/electoral_forensics_population.py`

Replace the Calgary geographic zone constants with your jurisdiction's metropolitan zones:

- `CALGARY_ZONE_A` → replace with your urban-core zone definition (use a geographic feature as the dividing line — a river, a transit corridor, or a census metropolitan boundary)
- `CALGARY_ZONE_B` → replace with your suburban-ring zone definition
- The `run_alternative_classification()` function should implement an independently-derived second rule to verify the zone asymmetry finding is not classifier-dependent

### `analysis/scripts/packing_cracking_analysis.py`

- The `MAJORITY_2026_MAPPING` / `MINORITY_2026_MAPPING` dictionaries contain the 2026-specific ED-to-predecessor crosswalk. Replace with your jurisdiction's ED mapping.
- `URBAN_WEIGHT_DEFAULT = 0.85` is calibrated to Calgary's 2021 DA-level population density. For other cities, re-derive this by computing the fraction of urban-hybrid ED population that falls within the dense census metropolitan boundary.

### `analysis/scripts/mcmc_ensemble_canonical.py`

- `POPULATION_TOLERANCE` is currently set to 0.25 (Alberta EBCA §15 ±25%). Change to match your jurisdiction's statutory tolerance (federal Canada also uses ±25% with 15% for specified areas; some provinces differ).
- `BASE_SEED` is derived from a Cloudflare drand beacon round. For a new jurisdiction, compute a new seed from a drand round that occurs before you first examine the official shapefiles.

---

## 3. What stays the same (no changes needed)

| Component | Why it transfers |
|---|---|
| `mcmc_ensemble_canonical.py` (GerryChain ReCom algorithm) | ReCom is geometry-agnostic; it operates on any contiguous graph of electoral districts with population constraints |
| `szat.py` (SZAT boundary-choice test) | The swing-zone definition and bootstrap null are computed from the two candidate maps; no jurisdiction-specific parameters |
| `joint_outlier_score_canonical.py` (Mahalanobis D²) | Uses the ensemble-derived covariance matrix; adapts automatically |
| `historical_eg_baseline.py` (efficiency-gap computation) | Pure computation on vote counts; no geography |
| Pre-registration template (OSF) | See §4 below for blank template |
| Gelman-Rubin convergence diagnostics | Same threshold (R̂ < 1.05) regardless of jurisdiction |
| Fisher combination and Holm-Bonferroni correction | Same formulae |
| `tests/` pytest suite | Tests cover computation logic, not jurisdiction-specific constants; all pass with updated column names |

---

## 4. Pre-registration template

Before examining official shapefiles, register the following on OSF:

```
Jurisdiction: [PROVINCE/FEDERAL/OTHER] [ELECTION_YEAR] Electoral Boundary Redistribution

Research question: Do the [COMMISSION_NAME]'s two candidate maps (Map A and Map B) differ on 
measurable partisan-fairness dimensions relative to a neutral redistricting baseline?

Statistical tests (pre-committed before shapefile receipt):
1. MCMC neutral ensemble: [N]-plan ReCom under ±[TOLERANCE]% population constraint.
   Base seed: SHA-256(salt:[YOUR_SALT]:randomness:[DRAND_ROUND_RANDOMNESS])
   Outlier threshold: p95 (one-tailed).
2. SZAT boundary-choice test: bootstrap permutation test on swing VAs (n=10,000 permutations).
   Outlier threshold: p < 0.05.
3. Fisher combination of tests 1 and 2 (independence check required first).
4. Population MAD comparison: Map A vs Map B Median Absolute Deviation from quota.
5. [JURISDICTION-SPECIFIC structural test, e.g., municipal anchoring, compactness].

Party labels: [INCUMBENT_PARTY] as "party_1", [OPPOSITION_PARTY] as "party_2".
Election data: [ELECTION_YEAR] [SOURCE].

Prediction: Map B's outlier percentile > Map A's on at least 3 of 4 partisan-bias metrics.
Direction: Map B more [INCUMBENT]-favourable than Map A.
```

---

## 5. Expected compute requirements

Wall time on a 4-core laptop with 16 GB RAM:

| Seat count | MCMC 1M plans | 250k plans | Forensic spot-check |
|---|---|---|---|
| 89 seats (Alberta) | ~6–8 h | ~1.5–2 h | ~2 min |
| ~125 seats (federal Alberta sub-commission) | ~15–20 h | ~4–5 h | ~5 min |
| 338 seats (full federal Canada) | ~40–60 h | ~10–15 h | ~20 min |

MCMC wall time scales roughly as O(n_seats × n_steps). Multi-chain runs (4 chains × 252,500 steps) are independently parallelisable: run each chain on a separate core. The GerryChain `checkpointing` feature saves chain state every 500 steps; runs interrupted mid-way resume from the last checkpoint without loss.

---

## 6. Known failure modes

**Near-equal populations.** If all districts are within 2–3% of the quota, the ReCom chain mixes very slowly (almost no valid proposals are accepted). This is unlikely in practice but can occur in small, densely uniform provinces. Fix: widen the population tolerance parameter temporarily for mixing; report the final ensemble at the statutory tolerance.

**Three-party elections.** The two-party (incumbent/opposition) framing in EG and SZAT is correct for plurality systems with one dominant two-party contest per district. If a third party is competitive in ≥ 20% of districts, the EG computation understates wasted votes. The Alberta script discards third-party votes and computes EG on the two-party share; this is documented and appropriate when the third party is small. For genuinely three-party systems (federal NDP competitive), consider computing multi-party EG or restricting analysis to the pairwise contest that generates the marginal seat.

**No comparable previous-cycle baseline.** SZAT requires a reference partition (the enacted baseline) to define swing VAs. If this is the first commission in a jurisdiction's history, or if the seat count changes substantially between cycles, the SZAT baseline is less meaningful. In this case, use the MCMC ensemble result (Ch1 Mahalanobis) as the primary test and SZAT as supplementary.

**Incumbent-protection clauses.** Some jurisdictions freeze specific districts under s.15(2)-style statutory protection (federal Canada protects Northern Quebec ridings). The `mcmc_ensemble_canonical.py` script has a commented-out freeze mechanism for this; see the `s15(2) freeze attempt` note in commit `972b04a` and the limitation documented there (freezing reduces ensemble diversity and makes outlier percentiles more conservative, not less).

---

## How to get help

- Open a GitHub issue at the audit repository with the `jurisdictions` label.
- The methods paper (`findings/methods_paper_draft.md`) documents the DPG geometry-reconstruction pipeline for cases where official shapefiles are unavailable.
- For questions about the Canadian constitutional framework (*Saskatchewan Reference*, effective representation standard), see the academic report §4.1 and Appendix F.
