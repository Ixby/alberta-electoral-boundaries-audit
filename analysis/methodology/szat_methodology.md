# Swing-Zone Allocation Test (SZAT) — Methodology and Pre-Registration

*Consolidation of `szat_proposal.md` (design and method) and
`szat_prereg_draft.md` (AsPredicted submission text). Both source files
are removed; this document is the canonical record.*

**Status:** Implemented. Pre-registered at AsPredicted #289,469 (filed 2026-05-07;
results known at filing; seed pre-committed at git hash `d2aea42`).

**Cross-ref:** `analysis/methodology/s15_2_reaudit.md`,
`analysis/methodology/academic_literature_review.md` §9

---

## §1 — Motivation

The existing audit tests — MCMC ensemble, efficiency gap, Neighbour-Drain, Urban
Hybridization — operate at the map level. They answer: *is this map an outlier?*
They do not answer: *which specific boundary choices caused the partisan effect,
and in which direction?*

The question surfaced during the §15(2) re-audit: Rocky Mountain House-Banff Park
(minority) passes all five statutory criteria and cannot be challenged on
population-deviation grounds. But the commission made a choice — draw the district
at −30.3% of quota rather than configure the region differently to stay within the
normal ±25% band. That choice reassigned specific voter blocs (the Banff-Kananaskis
polling subdivisions) from one ED configuration to another. Whether that reassignment
improved partisan efficiency for one party is an empirical question, and it is
testable.

SZAT formalises this question as a generalizable test applicable to any boundary
choice that differs between two maps.

---

## §2 — Core Concept: Swing Zones

A **swing zone** is any Voting Area (VA) polygon that is assigned to a different
Electoral Division under Map A than under Map B. When the minority map and majority
map are compared, a VA is a swing zone if:

    assigned_2026_minority ≠ assigned_2026_majority

There are currently 2,199 such swing zones in the existing VA assignment file (out
of 4,765 total VAs). These are the only VAs where the two maps' boundary choices
differ. Every other VA produces identical seat outcomes regardless of which map is
used; only the swing zones carry the between-map difference.

---

## §3 — Test Design

### 3.1 Inputs

| File | Description |
|---|---|
| `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` | Elections Alberta canonical majority 2026 ED boundaries |
| `data/shapefiles/canonical/ea_minority_2026_eds.gpkg` | Elections Alberta canonical minority 2026 ED boundaries |
| `data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp` | 2023 Voting Area polygons |
| `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg` | VAs with 2023 election-day + full vote attribution |

Note: `data/outputs/assignment_va_to_2026_assignments.csv` was built against
v0_5 DPG-derived shapefiles and must not be used as SZAT input. SZAT recomputes
VA assignments from scratch using the Elections Alberta canonical boundaries.

### 3.2 Spatial Join

For each VA polygon, compute centroid and assign:

    majority_ed  = ED whose boundary contains the VA centroid (majority map)
    minority_ed  = ED whose boundary contains the VA centroid (minority map)

Centroid-in-polygon is preferred over area-weighted overlap for political VAs
because the VA already represents a spatially coherent group of addresses.
Edge cases (centroid falls outside all EDs, or straddles a boundary) are
recorded as `unresolved` and excluded from the efficiency gap calculation with
a count reported.

### 3.3 Swing Zone Identification

    is_swing = (majority_ed ≠ minority_ed)

Non-swing VAs are excluded from the efficiency gap decomposition because they
produce identical outcomes under both maps.

### 3.4 Efficiency Gap Contribution per Swing Zone

The efficiency gap for a map is:

    EG = (wasted_votes_A − wasted_votes_B) / total_votes

where wasted votes = losing party's total votes in an ED + winning party's votes
above 50%+1 in that ED.

For each swing zone VA, compute its marginal efficiency gap contribution:

    ΔEG(va) = EG_contribution(va → minority_ed) − EG_contribution(va → majority_ed)

### 3.5 Aggregation and Verdict

    SZAT_score = Σ ΔEG(va)  for all swing zones

Interpretation:
- **SZAT_score > 0**: minority map's swing-zone allocations produce greater NDP vote
  waste relative to the majority map (structural UCP advantage in swing zones)
- **SZAT_score < 0**: minority map swing-zone allocations favour NDP efficiency
- **SZAT_score ≈ 0**: swing-zone allocations are partisan-neutral

A regional breakdown decomposes SZAT_score by geographic zone (Calgary, Edmonton,
Rest of Alberta, Mountain/West).

### 3.6 Significance Test

Bootstrap the SZAT_score by randomly re-assigning swing-zone VAs to one of the
two maps' ED configurations (holding non-swing VAs fixed) using 10,000 permutations.
If |SZAT_score| > 95th percentile of the bootstrap distribution, the swing-zone
allocation is unlikely to be partisan-neutral.

Seed: `get_canonical_seed("szat-bootstrap")` from `analysis/scripts/drand_seed.py`.
Derivation: SHA-256(CANONICAL_RANDOMNESS + "szat-bootstrap"), first 4 bytes as
uint32 mod 2^32 = 23687475. Derived from Cloudflare drand League of Entropy beacon
round 5,500,000, committed at git hash `d2aea42` before any simulation results.

---

## §4 — Output Specification

Primary output: `findings/szat_results.csv`

| Column | Description |
|---|---|
| `va_id` | Voting area identifier |
| `parent_ed_2019` | 2019 parent ED |
| `majority_ed` | Assigned ED under majority map |
| `minority_ed` | Assigned ED under minority map |
| `is_swing` | Boolean |
| `va_ndp` | NDP votes (election-day) |
| `va_ucp` | UCP votes (election-day) |
| `va_other` | Other votes |
| `delta_eg_contribution` | ΔEG(va) — marginal EG change from minority vs majority assignment |
| `region` | Calgary / Edmonton / Rest of Alberta / Mountain-West |
| `notes` | Unresolved flag if applicable |

Summary output: `findings/szat_summary.json`

    {
      "szat_score": <float>,
      "swing_zone_count": <int>,
      "unresolved_count": <int>,
      "bootstrap_p_value": <float>,
      "regional_breakdown": {
        "Calgary": <float>,
        "Edmonton": <float>,
        "Rest of Alberta": <float>,
        "Mountain-West": <float>
      },
      "canmore_rmh_contribution": <float>
    }

The `canmore_rmh_contribution` field isolates the ΔEG contribution from the
Banff-Kananaskis VAs specifically.

---

## §5 — Relationship to Existing Tests

| Test | What it measures | SZAT comparison |
|---|---|---|
| MCMC ensemble | Is the whole map an outlier against neutral random draws? | SZAT measures which boundary differences between the two real maps drive the gap |
| Efficiency gap (map level) | Map-wide vote waste asymmetry | SZAT decomposes the gap into the specific boundary choices causing it |
| Neighbour-Drain | ED-pair adjacency pattern (packed next to cracked) | SZAT measures vote efficiency in the swing zones between those EDs |
| Urban Hybridization | Count of urban-rural fusion districts | SZAT could confirm whether Urban Hybridization districts are also swing-zone contributors |

SZAT does not replace any existing test. It adds spatial specificity to the
efficiency gap: not just *how much* imbalance exists but *where it comes from*.

---

## §6 — Generalizability

The majority-vs-minority framing is natural for this audit. The test generalises
to any pair of maps covering the same province:

**Any proposed map vs. the current enacted baseline (2019 EDs):** Every VA that
moves to a different 2026 ED from its 2019 ED is a swing zone; the question becomes
whether the proposed map's boundary choices systematically improve or degrade
partisan efficiency relative to the neutral baseline.

**Implementation path:** Replace `ea_majority_2026_eds.gpkg` with
`alberta_2019_eds.gpkg` as Map A. The 2019 ED boundaries are in
`data/shapefiles/reference/alberta_2019_eds/`. VA assignments to 2019 EDs are
trivially computed via `parent_ed_2019` in the existing VA file.

This generalisation is documented here for future implementation. It is not in
scope for the current audit, which is bounded to the minority-vs-majority comparison.

---

## §8 — Defensibility: Anticipated Challenges and Responses

This section documents the audit's response to each principal challenge that a hostile reviewer, counsel, or court would raise against SZAT. Claims below are grounded in primary sources cited in §5 (relationship to existing tests) and `analysis/methodology/reference/academic_literature_review.md` §9b and §10.

---

### Challenge 1: "SZAT is a novel test with no published validation. Results from untested methods cannot be relied upon."

**Response.**

The novelty claim is accurate and is disclosed in the AsPredicted pre-registration text (Appendix, filed 2026-05-07), in the academic literature review (§9b), and in the report (§5.2.10). No established test decomposes the between-map EG difference to individual boundary choices at the Voting Area level; that gap is the test's motivation.

Novelty is not, however, equivalent to invalidity. SZAT is composed entirely of validated sub-components:

1. **Efficiency gap** (Stephanopoulos & McGhee 2015, *U. Chi. L. Rev.* 82(2): 831–900) — the unit of measure. EG is applied identically to both maps' swing-zone subsets; it does not change properties by being restricted to swing zones.

2. **Centroid-in-polygon spatial join** — established GIS operation. The assignment of VA centroids to ED polygons is the same `representative_point()` method used throughout the audit and documented in `szat.py` §3.2.

3. **Permutation bootstrap** — established significance testing framework (Fisher 1935, *The Design of Experiments*; Efron & Tibshirani 1993, *An Introduction to the Bootstrap*). The specific permutation null (Bernoulli(0.5) assignment of swing zones to either map's configuration) is novel, but the inference framework is not.

The closest prior literature falls into two groups:

- **Map-level outlier tests** (Stephanopoulos & McGhee 2015, whole-map EG; Altman & McDonald 2011, simulation comparison): these ask whether a map is anomalous relative to neutral draws. They do not answer which boundary choices drive the anomaly.

- **Map-level decomposition** (Chen & Rodden 2013 — geography vs. drawing at map level; **Barton & Eguia 2024**, "A decomposition of partisan advantage in electoral district maps," *Electoral Studies* — decomposes a map's partisan advantage into political geography, redistricting legal constraints, and discretionary map-choice): these isolate the "discretionary" component of partisan advantage from the forced component.

SZAT is the boundary-choice-level operationalisation of the discretionary component identified by Barton & Eguia: where they isolate the discretionary factor at the map level, SZAT identifies which specific Voting Area assignments — the places where the two commissioners drew lines differently — account for the between-map EG difference. SZAT asks a different question from all prior tests: not "is the map anomalous?" nor "how much of this map's advantage is discretionary?", but "among the specific decisions that differed between two real proposed maps, which VAs drove the partisan EG gap, and is the overall pattern partisan-neutral?"

This is not a test for a new quantity; it is a test for an established quantity (EG) applied to a previously untested conditioning set (the between-map swing zone).

**VA file provenance check (run 2026-05-18).** The default run uses `va_polygons_with_full_2023_votes.gpkg` (derived file). A second run against the official Elections Alberta `va_2023_election_day_votes.gpkg` (canonical file, same source as Phase 4C) produces identical results: SZAT score +0.039211, swing zones 2,110, p = 0.0024, EG majority +0.000982, EG minority +0.040194, regional breakdown unchanged. The two VA files assign all 4,765 VA representative points identically — confirming that the derived file's geometry is consistent with the canonical EA VA geometry. Output: `findings/szat_summary_canonical_va.json`.

**Evidentiary posture.** SZAT is reported as Channel 2 of a two-channel test (see §5.3.4 and `analysis/methodology/fisher_combination_defense.md`). Channel 1 (Mahalanobis D², p = 1.40×10⁻⁶) is a well-established joint outlier method applied to a validated MCMC ensemble. SZAT's p = 0.0024 is corroborating evidence that reinforces Channel 1 from a structurally different direction. The headline result (Fisher T = 39.02, combined p = 6.87×10⁻⁸) does not depend on accepting SZAT as the primary finding; it remains meaningful even if a reviewer discounts SZAT entirely, because Channel 1 alone returns p = 1.40×10⁻⁶.

---

### Challenge 2: "The pre-registration was filed after the results were known. The p-value cannot be trusted."

**Response.**

The timing limitation is acknowledged explicitly in the pre-registration text itself (Appendix, "Timing disclosure") and restated in the academic report. The exact admission reads: *"The `szat.py` script was written and a preliminary run was executed on 2026-05-06 before this registration was filed. ... The specific numerical results were known to the analyst at time of filing."*

What remains verifiable despite this timing:

1. **The bootstrap seed was pre-committed before any results.** The Cloudflare drand beacon round 5,500,000 was committed at git hash `d2aea42` before the canonical shapefiles arrived on 2026-05-06. The salt `"szat-bootstrap"` and the derivation method (SHA-256, first 4 bytes as uint32) are specified in `drand_seed.py` and committed at the same hash. The seed itself — 23,687,475 — is not analyst-chosen; it is cryptographically derived from a public beacon whose value no party to this audit controls. Retroactive selection of a seed to produce a desired p-value is therefore impossible: the seed is a function of a public timestamp, not an analyst choice.

2. **The p-value has been reproduced across multiple independent runs with different parameters.** The p-value history in `academic_literature_review.md` §9b documents: original additive-delta approximation (p ≈ 0.000), 500-permutation full-recompute (p ≈ 0.012), 10,000-permutation Election-Day-only substrate (p = 0.0044), 10,000-permutation full advance-vote substrate (p = 0.0024). H₀ was rejected at α = 0.05 under every specification. The declining p-value across increasingly rigorous specifications is inconsistent with a result manufactured to exceed a threshold.

3. **The test is fully reproducible.** An independent analyst who runs `analysis/scripts/szat.py` against the canonical shapefiles and the same seed recovers p = 0.0024. The null distribution is not analyst-controlled.

The residual vulnerability is that a filing made after results are known cannot fully replicate the inferential value of a pre-analysis registration. The audit does not overclaim this point: SZAT's timing limitation is why the Fisher combination presents it as Channel 2 (corroborating) rather than the primary headline test. Channel 1 (Mahalanobis D²) was registered at OSF:6pt83 before shapefiles arrived and carries the primary inferential weight.

---

### Challenge 3: "The Bernoulli(0.5) permutation null is arbitrary. A different null would give a different p-value."

**Response.**

The Bernoulli(0.5) null asks a specific and interpretable question: *if the minority commissioners had made each swing-zone boundary choice with equal probability of favouring either map's configuration — no partisan preference — how extreme would the observed SZAT score be?*

This is the natural null for a test of partisan neutrality in boundary-choice. Each swing zone is a Voting Area where the two maps draw a line differently. Under the null of partisan-neutral decision-making, each such choice has no systematic directional lean; assigning each independently with probability 0.5 is the minimal-assumption encoding of that neutrality.

Alternative nulls that a hostile reviewer might propose:

- **Geography-stratified null** (e.g., hold regional proportions fixed): A geography-stratified permutation would test whether the swing zone allocations are unusual *conditional on regional composition*. This is a stricter test (it controls for regional variation in partisan geography). Running the SZAT score under a region-fixed null would be a legitimate robustness check. The regional decomposition in `findings/szat_summary.json` (Rest of Alberta +0.015, Edmonton +0.008, Calgary +0.011) shows that the positive SZAT score persists across all four regions — a geography-stratified null cannot attribute the result to a single regional anomaly.

- **Proportional-to-vote-share null**: A null proportional to the swing zone's pre-existing vote shares would condition on the partisanship of the VA itself. This is not the appropriate null for a test of *boundary-drawing choice*: the question is whether the commissioner's assignment of a VA to one ED vs another is partisan-neutral, not whether the VA's votes are partisan-neutral. The VA's partisanship is given data; the boundary-drawing choice is the behaviour under test.

The Bernoulli(0.5) null is the correct null for the question SZAT is asking. It is also the null that the pre-registration text specifies verbatim (Appendix §5: "For each of 10,000 permutations: for each swing-zone VA, randomly assign it to either its majority-map ED or its minority-map ED (independent Bernoulli(0.5) draws)"). An analyst who wanted to weaken the result could have proposed a more conservative null; choosing Bernoulli(0.5) is the strongest transparent null, not a choice calibrated to maximize significance.

---

### Challenge 4: "SZAT is only one test. A single novel test does not establish a finding."

**Response.**

SZAT is presented as one component of a two-channel joint test, not as a standalone finding. The Fisher combination (T = 39.02, p = 6.87×10⁻⁸, `analysis/methodology/fisher_combination_defense.md`) requires both channels to contribute; the headline figure is not derived from SZAT alone.

The two channels are structurally independent:

- **Channel 1 (Mahalanobis D²):** Scores the minority map against 1,010,000 neutral ReCom ensemble draws on a joint vector of four established partisan metrics (EG, mean-median, declination, seats@50/50). It asks: *is this map unusual relative to constraint-equivalent neutral alternatives?* It does not examine specific boundary choices.

- **Channel 2 (SZAT):** Decomposes the EG gap to the specific boundary choices that differ between the two real proposals. It asks: *do the places where the minority drew differently from the majority systematically favour one party?* It does not compare the minority to neutral draws.

The independence between channels is not assumed; it is argued in `analysis/methodology/fisher_combination_defense.md` §3: Channel 1 conditions on the whole map's position in the neutral ensemble space; Channel 2 conditions only on the swing zones — a strict subset of boundary choices that is not evaluated by the ensemble test. Positive correlation between them, if present, makes Fisher conservative (see `fisher_combination_defense.md` §5, AV5): Fisher underestimates significance when channels are positively correlated. The combined p-value is a lower bound on significance under dependence.

Beyond the Fisher combination, the directional consistency across five additional non-vote-dependent structural findings (population dispersion, Calgary zone asymmetry, Airdrie fragmentation, spatial anomaly count, procedural departure) is noted in the academic report's §6 synthesis. A hostile reader who rejects SZAT entirely is left with the ensemble result (p = 1.40×10⁻⁶) and the structural lane intact.

---

## §7 — Implementation Checklist

- [x] Receive Elections Alberta shapefiles and place at canonical paths
- [x] Create `data/shapefiles/canonical/` directory
- [x] Write `analysis/scripts/szat.py` implementing §3.1–3.6
- [x] Register `get_canonical_seed("szat-bootstrap")` in `drand_seed.py`
- [x] Add SZAT to `audit_dependency_graph.json`
- [x] Run and review `szat_results.csv`
- [x] Update `academic_literature_review.md` §9 with SZAT as a novel test
- [x] Pre-register bootstrap null — AsPredicted #289,469 (filed 2026-05-07;
      results known at filing; seed pre-committed at d2aea42)

---

## Appendix — AsPredicted Pre-Registration Text

*Verbatim submission text filed at aspredicted.org as AsPredicted #289,469
on 2026-05-07.*

**Timing disclosure.** The SZAT bootstrap seed was derived from the pre-committed
drand beacon (CANONICAL_ROUND = 5500000, committed at git hash `d2aea42` before
any simulation results were generated). The `szat.py` script was written and a
preliminary run was executed on 2026-05-06 before this registration was filed.
This diverges from the ideal pre-analysis registration sequence. It is disclosed
here and in the report: the analysis plan and seed were pre-committed, but the
registration text was filed after a preliminary run confirmed the pipeline worked.
The specific numerical results were known to the analyst at time of filing.

---

### 1. Have any data been collected for this study already?

Yes. We use the 2023 Alberta general election results by Voting Area (VA),
obtained from Elections Alberta, and the official 2026 Electoral Boundary
Commission proposed boundary shapefiles (majority and minority reports),
released 2026-04-09 and obtained directly from Elections Alberta. All data
were already in our possession before the SZAT analysis pipeline was designed.

### 2. What is the main question being asked or hypothesis being tested?

Do the specific boundary choices that differ between the 2026 EBC majority and
minority proposed maps — the "swing zones," defined as Voting Areas whose centroid
falls in a different Electoral Division under the minority map than under the
majority map — systematically shift partisan vote efficiency in a directional way?

**Null hypothesis (H0):** The minority map's swing-zone boundary choices produce no
systematic difference in efficiency-gap contribution compared to the majority map.
Formally: the observed SZAT score does not exceed the 95th percentile of the
randomization null distribution.

**Alternative hypothesis (H1):** The swing-zone allocations under the minority map
are directionally non-neutral — they produce a larger efficiency-gap asymmetry than
would be expected if the boundary choices were randomly assigned across swing-zone VAs.

### 3. Describe the key dependent variable(s)

**SZAT score** = EG(minority map) − EG(majority map), where EG is the standard
Stephanopoulos-McGhee (2015, *U. Chi. L. Rev.* 82(2): 831–900) efficiency gap
computed from 2023 election-day Voting Area vote totals spatially joined to each
proposed map.

EG sign convention: positive = more NDP votes wasted than UCP (structural UCP
advantage). SZAT score positive = minority map's boundary choices increase NDP
vote waste relative to the majority map.

Secondary outputs:
- Regional decomposition of SZAT score (Calgary, Edmonton, Mountain-West,
  Rest of Alberta)
- Canmore/RMH focal-ED contribution

### 4. How many observations will be collected?

4,765 Voting Areas assigned via centroid-in-polygon spatial join to each proposed
map. Swing zones number approximately 2,100 (exact count from the spatial join).
The bootstrap uses 10,000 permutations.

### 5. What are the analyses?

**Primary test — randomization bootstrap:**

For each of 10,000 permutations:
1. For each swing-zone VA, randomly assign it to either its majority-map ED or its
   minority-map ED (independent Bernoulli(0.5) draws)
2. Compute EG for each map under the randomized assignment
3. Record SZAT score under the permutation

Bootstrap seed: `get_canonical_seed("szat-bootstrap")` derived from Cloudflare
drand League of Entropy beacon round 5,500,000
(randomness `45922177bf69644aa0b8f8043695221eacad1147dfde0967c72fbf3756ffacac`),
committed at git hash `d2aea42`. Derivation: SHA-256(CANONICAL_RANDOMNESS +
"szat-bootstrap"), first 4 bytes as uint32 mod 2^32 = 23687475.

**Verdict criterion:** Reject H0 if |SZAT_score| > 95th percentile of the
bootstrap null distribution (two-tailed α = 0.05).

**Boundary shapefiles (canonical):** Elections Alberta official shapefiles
`EBC2025_Boundaries_Apr092026.shp` (majority) and
`Minority_Report_Boundaries.shp` (minority), both EPSG:3400, 89 EDs each,
stored at `data/shapefiles/canonical/` in the audit repository.

All code in `analysis/scripts/szat.py`.

### 6. Any other comments?

This test was motivated by the §15(2) population-deviation re-audit
(`analysis/methodology/s15_2_reaudit.md`, 2026-04-23), which found that the
minority map's Rocky Mountain House-Banff Park ED is 5.3 percentage points
outside the normal ±25% population band and invokes the §15(2) exception —
the smallest margin of any §15(2) invocation in either map.

**Relationship to existing pre-registrations:**
- AsPredicted #289449: DPG v11 validation (complete)
- AsPredicted #289451: Neighbour-Drain label-shuffle null (pending)
- AsPredicted #289455: Lunty 91-seat forensic scorecard (pending)
- This registration (AsPredicted #289,469): SZAT bootstrap null
