# Swing-Zone Allocation Test (SZAT) — Methodology Proposal

**Status:** Proposed. Canonical shapefiles ingested 2026-05-06. Ready for implementation.
**Date drafted:** 2026-05-06
**Cross-ref:** `analysis/methodology/s15_2_reaudit.md`, `analysis/methodology/academic_literature_review.md` §9

---

## 1. Motivation

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

## 2. Core concept: swing zones

A **swing zone** is any Voting Area (VA) polygon that is assigned to a different
Electoral Division under Map A than under Map B. When the minority map and majority
map are compared, a VA is a swing zone if:

    assigned_2026_minority ≠ assigned_2026_majority

There are currently 2,199 such swing zones in the existing VA assignment file (out
of 4,765 total VAs). These are the only VAs where the two maps' boundary choices
differ. Every other VA produces identical seat outcomes regardless of which map is
used; only the swing zones carry the between-map difference.

---

## 3. Test design

### 3.1 Inputs

| File | Description |
| --- | --- |
| `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` | Elections Alberta canonical majority 2026 ED boundaries (**see §7**) |
| `data/shapefiles/canonical/ea_minority_2026_eds.gpkg` | Elections Alberta canonical minority 2026 ED boundaries (**see §7**) |
| `data/shapefiles/reference/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp` | 2023 Voting Area polygons (Elections Alberta) |
| `data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg` | VAs with 2023 election-day + full vote attribution |

Note: the existing `data/outputs/assignment_va_to_2026_assignments.csv` was built
against v0_5 DPG-derived shapefiles and uses mixed assignment methods (spatial,
crosswalk, nearest_ed). It is **not** used as an input to SZAT. SZAT recomputes
VA assignments from scratch using the Elections Alberta canonical boundaries via
a clean spatial join.

### 3.2 Spatial join

For each VA polygon, compute centroid and assign:

    majority_ed  = ED whose boundary contains the VA centroid (majority map)
    minority_ed  = ED whose boundary contains the VA centroid (minority map)

Centroid-in-polygon is preferred over area-weighted overlap for political VAs
because the VA already represents a spatially coherent group of addresses; the
centroid reliably falls inside the correct ED for all but narrow boundary-crossing
edge cases. Edge cases (centroid falls outside all EDs, or straddles a boundary)
are recorded as `unresolved` and excluded from the efficiency gap calculation with
a count reported.

### 3.3 Swing zone identification

    is_swing = (majority_ed ≠ minority_ed)

Swing zones carry the between-map difference. Non-swing VAs are excluded from
the efficiency gap decomposition because they produce identical outcomes under
both maps.

### 3.4 Efficiency gap contribution per swing zone

The efficiency gap for a map is:

    EG = (wasted_votes_A − wasted_votes_B) / total_votes

where wasted votes = losing party's total votes in an ED + winning party's votes
above 50%+1 in that ED.

For each swing zone VA, compute its **marginal efficiency gap contribution** —
the change in EG produced by assigning it to the minority map's ED rather than
the majority map's ED:

    ΔEG(va) = EG_contribution(va → minority_ed) − EG_contribution(va → majority_ed)

This requires knowing the total vote margin in each ED (to determine whether
the VA's votes are going into a winning or losing seat, and whether they are
above or below the 50%+1 threshold). ED-level totals are computed from the full
VA spatial join in the same run.

### 3.5 Aggregation and verdict

Sum ΔEG across all swing zones:

    SZAT_score = Σ ΔEG(va)  for all swing zones

Interpretation:

- **SZAT_score > 0**: swing-zone allocations under the minority map produce
  greater NDP vote waste relative to the majority map (minority map is less
  efficient for NDP / more efficient for UCP in the swing zones)
- **SZAT_score < 0**: minority map swing-zone allocations favour NDP efficiency
- **SZAT_score ≈ 0**: swing-zone allocations are partisan-neutral

A regional breakdown is produced in addition to the map-wide sum, decomposing
SZAT_score by geographic zone (Calgary, Edmonton, Rest of Alberta, Mountain/West)
to identify which regions drive the between-map difference.

### 3.6 Significance test

Bootstrap the SZAT_score by randomly re-assigning the swing-zone VAs to one of
the two maps' ED configurations (holding the non-swing VAs fixed) and computing
SZAT_score under each random re-assignment. If the observed SZAT_score falls
outside the 95th percentile of the bootstrap distribution, the swing-zone
allocation is unlikely to be partisan-neutral.

Seed: `get_canonical_seed("szat-bootstrap")` from `analysis/scripts/drand_seed.py`.

---

## 4. Output specification

Primary output: `analysis/reports/szat_results.csv`

| Column | Description |
| --- | --- |
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

Summary output: `analysis/reports/szat_summary.json`

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
Banff-Kananaskis VAs specifically, since those are the swing zones whose
partisan direction motivated this test.

---

## 5. Relationship to existing tests

| Test | What it measures | SZAT comparison |
| --- | --- | --- |
| MCMC ensemble | Is the whole map an outlier against neutral random draws? | SZAT measures which boundary *differences between the two real maps* drive the gap |
| Efficiency gap (map level) | Map-wide vote waste asymmetry | SZAT decomposes the gap into the specific boundary choices causing it |
| Neighbour-Drain | ED-pair adjacency pattern (packed next to cracked) | SZAT measures vote efficiency in the swing zones between those EDs |
| Urban Hybridization | Count of urban-rural fusion districts | SZAT could confirm whether Urban Hybridization districts are also swing-zone contributors |

SZAT does not replace any existing test. It adds spatial specificity to the
efficiency gap: not just *how much* imbalance exists but *where it comes from*.

---

## 6. Generalizability (question for later)

The majority-vs-minority framing is natural for this audit because both maps are
real proposals from the same commission under identical constraints. But the test
generalises to any pair of maps covering the same province:

**Any proposed map vs. the current enacted baseline (2019 EDs):**
The same swing-zone logic applies. Every VA that moves to a different 2026 ED
from its 2019 ED is a swing zone; the question becomes whether the proposed map's
boundary choices systematically improve or degrade partisan efficiency relative
to the neutral baseline. This is potentially more useful to the field because:

- Courts and commissions care whether a *new* map is an improvement or a step
  backward relative to the prior plan, not just how two competing proposals
  compare to each other
- A map that scores well on majority-vs-minority SZAT could still score poorly
  on proposed-vs-baseline SZAT if both proposals share a partisan structure that
  the 2019 map did not have

**Implementation path:**
Replace `ea_majority_2026_eds.gpkg` with `alberta_2019_eds.gpkg` as Map A.
The 2019 ED boundaries are already in `data/shapefiles/reference/alberta_2019_eds/`.
VA assignments to 2019 EDs are trivially computed (the 2023 VA file was built
against 2019 EDs, so `parent_ed_2019` already provides this). This means the
proposed-vs-2019 variant requires only the minority spatial join as new computation.

This generalisation is documented here for future implementation. It is not
in scope for the current audit, which is bounded to the minority-vs-majority
comparison.

---

## 7. Canonical shapefile policy

**Effective 2026-05-06:** Elections Alberta shapefiles are the canonical boundary
source for all forward analysis. All DPG-derived shapefiles are deprecated.

| Deprecated file | Status |
| --- | --- |
| `data/shapefiles/derived/v11_majority_2026_eds.gpkg` | Deprecated — DPG-derived |
| `data/shapefiles/derived/v11_minority_2026_eds.gpkg` | Deprecated — DPG-derived |
| `data/shapefiles/derived/v0_10_topological_*.gpkg` | Deprecated — DPG-derived |
| `data/shapefiles/derived/v0_9_topological_*.gpkg` | Deprecated — DPG-derived |

Canonical paths (to be populated when shapefiles are received):

| File | Description |
| --- | --- |
| `data/shapefiles/canonical/ea_majority_2026_eds.gpkg` | Elections Alberta majority 2026 boundaries |
| `data/shapefiles/canonical/ea_minority_2026_eds.gpkg` | Elections Alberta minority 2026 boundaries |

The `data/shapefiles/canonical/` directory does not yet exist. It should be
created and populated before SZAT or any updated pipeline run is executed.
All scripts that currently reference `v11_` or `v0_10_` paths should be updated
to reference `canonical/` paths before their next execution.

**The existing `data/outputs/assignment_va_to_2026_assignments.csv` was built
against deprecated shapefiles.** It remains valid as a provenance record but
must not be used as the spatial-join input for SZAT or any downstream analysis
that requires canonical boundary accuracy.

---

## 8. Implementation checklist

- [ ] Receive Elections Alberta shapefiles and place at canonical paths
- [ ] Create `data/shapefiles/canonical/` directory
- [ ] Write `analysis/scripts/szat.py` implementing §3.1–3.6
- [ ] Register `get_canonical_seed("szat-bootstrap")` in `drand_seed.py`
- [ ] Add SZAT to `audit_dependency_graph.json`
- [ ] Run and review `szat_results.csv` — check Canmore/RMH contribution specifically
- [ ] Update `academic_literature_review.md` §9 with SZAT as a novel test
- [x] Pre-register bootstrap null — AsPredicted #289,469 (filed 2026-05-07; results known at filing; seed pre-committed at d2aea42)

---

Document version: 1.0 — 2026-05-06
