---
name: Hardcoded-values audit of the Phase B scorecard pipeline
description: "Inventory of every hardcoded literal in the scorecard + dry-run pipeline, classified by necessity (pre-registered, methodology, external data, drift hazard, or actual inconsistency). Surfaces one real bug-or-intentional-asymmetry between mo1's 10-city dict and mo2's 8-city big_city_codes set in phase_b_scorecard.py, and drafts a runtime consistency check that would catch any future drift. Status: PREP COMPLETE — the consistency check is not committed to live code because resolving the discrepancy requires a methodology decision (which city set is correct for the urban-share half of MO #2) that needs PI authorization."
type: methodology
---

> **Backward:**
> - `analysis/scripts/phase_b_scorecard.py` — the live scorecard this audits
> - `analysis/scripts/neighbour_drain_adjacency.py` — drain test touched by the same code-review pass
> - `proposals/lunty_dry_run/` — synthetic 91-district generators that test the scorecard
> - `preregistration/null_hypotheses.md` — the pre-registration that pins the MO #1–#4 thresholds
>
> **Forward:**
> - `analysis/scripts/phase_b_scorecard.py` — would gain a `_assert_city_sets_consistent()` runtime check (or a unit test) if authorized
> - (leaf — methodology audit, not consumed by any script)

# Hardcoded-values audit — Phase B scorecard pipeline

**Status as of 2026-05-24: PREP COMPLETE, NOT AUTHORIZED.** This file inventories hardcoded literals in the pipeline touched by the 2026-05-24 code-review pass (commits 220287d, a4ac32b, e5932e5, 854a80e). One real inconsistency is documented below; the proposed runtime check is **not** committed to live code because resolving the discrepancy requires a methodology decision rather than a defensive patch.

## Method

`grep`-walk every numeric, string, and dict literal in:

- `analysis/scripts/phase_b_scorecard.py` (live scorecard)
- `analysis/scripts/neighbour_drain_adjacency.py` (drain test)
- `analysis/scripts/score_anchoring.py` (anchoring scorer)
- `analysis/scripts/municipal_anchoring_2019_baseline.py` (2019 comparator)
- `proposals/lunty_dry_run/generate_synthetic_91.py`
- `proposals/lunty_dry_run/generate_realistic_91.py`

Classify each value by whether removing it (or moving it to a file / making it parametric) would meaningfully reduce risk.

## Classification

### A — Necessary by pre-registration

These values were committed in writing **before** the Lunty committee began its work; the whole point is that they are unchangeable from the script's runtime context. Moving them to a config file would weaken the audit's pre-registration discipline (a config file is editable post-hoc; a literal in committed code is not). **Do not touch.**

| Value | File:line | Pre-reg source |
|---|---|---|
| `MO1_DRAIN_TRIPWIRE_FACTOR = 1.5` | phase_b_scorecard.py:104 | committed 2026-04-24 |
| `MO2_PP_PERCENTILE_THRESHOLD = 10` | phase_b_scorecard.py:110 | committed 2026-04-24 |
| `MO3_ANCHORING_THRESHOLD = 0.70` | phase_b_scorecard.py:111 | Canadian-norm threshold, pre-registered |
| `MO4_SAMPLER_DIVERGENCE_PP = 25` | phase_b_scorecard.py:112 | committed 2026-04-24 |
| `S_THRESHOLD = 0.15`, `M_THRESHOLD = 0.05` | neighbour_drain_adjacency.py:89-90 | directive-specified |
| `SENSITIVITY_GRID = [(0.10, 0.08), (0.15, 0.05), (0.20, 0.03)]` | neighbour_drain_adjacency.py:115 | directive-specified |

### B — Necessary as methodology constants

Held identical across the canonical and DPG-era runs so the metric is substrate-agnostic. Moving them to a config would invite per-run tuning, which would invalidate the methodology-parity guarantee with the 2019 baseline. **Do not touch.**

| Value | File:line | Why fixed |
|---|---|---|
| `SNAP_TOL_M = 500.0` | score_anchoring.py:106, municipal_anchoring_2019_baseline.py:119 | EBCA ±500m error budget; matches headline runs |
| `VERTEX_DENSIFY_M = 50.0` | score_anchoring.py:107, municipal_anchoring_2019_baseline.py:122 | matches headline runs |
| `ADJACENCY_BUFFER_M = 600.0` | neighbour_drain_adjacency.py:103 | substrate-gap tolerance; rationale documented in-file |
| `K_FALLBACK = 3` | neighbour_drain_adjacency.py:112 | substrate-gap fallback for rural isolates |
| `POP_TOLERANCE = 0.25` | generate_synthetic_91.py:61 | EBCA standard |
| `N_DISTRICTS = 91` | generate_synthetic_91.py:60 | Lunty committee seat count |

### C — Necessary as external-data literals (drift-monitored)

Values transcribed from external sources (StatsCan 2021 census, Elections Alberta). Drift hazard exists but is low. The 80.0 / 72.0 canonical-anchoring case was the worst of this class and was addressed in commit 854a80e (`_resolve_canonical_anchoring()` reads `data/outputs/canonical_anchoring_summary.json` when present, falls back to literals with a loud WARN otherwise).

Remaining literals in this class that have **not** been wrapped in a resolver:

| Value | File:line | Source | Drift hazard |
|---|---|---|---|
| `avg_pop_per_district = 53_722` (= `floor(4,888,723 / 91)`) | phase_b_scorecard.py:131 | TBF-adjusted 2021 population ÷ Lunty seat count | Drifts if either input is restated. The literal hides both inputs from the maintainer. |
| 10-city per-city populations: Calgary 1,306,784 … Leduc 34,094 | phase_b_scorecard.py:134–144 | 2021 census | Drifts if census is restated (rare) or if the audit expands the list |
| 10-city CSD codes inside `cities` dict | phase_b_scorecard.py:134–144 | StatsCan 2021 CSD reference | Static; CSD codes are persistent identifiers |
| `_CANONICAL_MAJORITY_PCT_FALLBACK = 80.0`, `_CANONICAL_MINORITY_PCT_FALLBACK = 72.0` | municipal_anchoring_2019_baseline.py:131–132 | methods-paper §7.1 Stage 9 | **Already wrapped** by `_resolve_canonical_anchoring()` in commit 854a80e |

**Recommendation:** rewrite `avg_pop_per_district = 53_722` as `_TBF_POPULATION_2021 = 4_888_723; _LUNTY_SEAT_COUNT = 91; avg_pop_per_district = _TBF_POPULATION_2021 // _LUNTY_SEAT_COUNT`. Same value today; named inputs visible to the maintainer; trivially auditable if either changes. Could be done as a follow-up commit without methodology implications.

### D — Magic numbers that should be named constants (cosmetic)

| Value | File:line | What it is |
|---|---|---|
| `100.0` (shared-boundary threshold) | neighbour_drain_adjacency.py:238 | minimum shared-edge length for strict adjacency |
| `0.40 <= ed_urban <= 0.60` (mid-urban-rural band) | phase_b_scorecard.py:257 | MO #2 lasso-urban-mix band |
| `b"version https://git-lfs"` (LFS pointer sentinel) | phase_b_scorecard.py:424 etc | Git LFS spec |

Cosmetic. No behaviour change from naming them. Worth doing in a future cleanup pass.

### E — Actual inconsistency (real finding)

The notable finding from this audit:

**`phase_b_scorecard.py` maintains two separately-defined city lists that overlap but are not identical.**

`cities` dict in `mo1_drain_pattern` (lines 134–144) contains **10** cities with their populations and CSD codes:

```
Calgary, Edmonton, Red Deer, Lethbridge, St. Albert,
Medicine Hat, Grande Prairie, Airdrie, Spruce Grove, Leduc
```

`big_city_codes` set in `mo2_lasso_compactness` (lines 227–235) contains only **8** CSD codes:

```
4806016 Calgary, 4811062 Edmonton, 4806036 Red Deer,
4802012 Lethbridge, 4811049 St. Albert, 4801006 Medicine Hat,
4819030 Grande Prairie, 4806008 Airdrie
```

**Missing from mo2: 4811053 Spruce Grove and 4811028 Leduc.**

The two lists are defined ~90 lines apart with no cross-reference, no shared constant, and no comment explaining the asymmetry. There are two equally-plausible interpretations:

1. **Intentional asymmetry.** mo1's `cities` dict counts the 10 named cities for population-justified district-split scrutiny (mid-sized cities like Spruce Grove with 37k pop still warrant the split-ratio check). mo2's `big_city_codes` defines the urban-share denominator for the lasso check — and may have deliberately excluded Spruce Grove and Leduc as Edmonton-satellite communities whose VA centroids are mostly inside their parent metro area's commute shed rather than acting as independent urban cores.

2. **Bug / drift.** One list was extended (Spruce Grove + Leduc added to `cities`) without updating the other (`big_city_codes` was not extended in sync). The two literals drifted because nothing in the code or tests enforces consistency.

The pre-registration document does not appear to specify which city set mo2 should use, so the runtime evidence is ambiguous. **Resolution requires a PI methodology decision**, not a defensive code patch.

## Proposed verification check (NOT YET AUTHORIZED)

A drop-in module-level assertion that would catch any future drift in either direction. **Pinning it to ten cities would lock in interpretation #1; pinning it to eight would lock in interpretation #2.** A diagnostic-only version (warn-and-continue if the lists diverge) avoids forcing the methodology question while still surfacing future drift.

```python
# Add near the top of analysis/scripts/phase_b_scorecard.py,
# after the cities dict is defined (lifted out of mo1 to module scope):

_CITIES_FOR_MO1 = {
    "Calgary":        {"pop": 1_306_784, "csd_code": 4806016},
    "Edmonton":       {"pop": 1_010_899, "csd_code": 4811062},
    "Red Deer":       {"pop":   100_844, "csd_code": 4806036},
    "Lethbridge":     {"pop":    98_406, "csd_code": 4802012},
    "St. Albert":     {"pop":    68_232, "csd_code": 4811049},
    "Medicine Hat":   {"pop":    63_271, "csd_code": 4801006},
    "Grande Prairie": {"pop":    64_141, "csd_code": 4819030},
    "Airdrie":        {"pop":    74_100, "csd_code": 4806008},
    "Spruce Grove":   {"pop":    37_645, "csd_code": 4811053},
    "Leduc":          {"pop":    34_094, "csd_code": 4811028},
}

# MO #2's urban-share denominator. Currently the eight non-satellite
# cities from _CITIES_FOR_MO1; Spruce Grove and Leduc are excluded as
# Edmonton-satellite communities. Pin explicitly so future drift in
# either direction is forced through a methodology amendment, not a
# silent edit.
_BIG_CITY_CODES_FOR_MO2 = {
    4806016, 4811062, 4806036, 4802012,
    4811049, 4801006, 4819030, 4806008,
}

# Consistency check: every code in _BIG_CITY_CODES_FOR_MO2 must appear
# in _CITIES_FOR_MO1, and the asymmetry (Spruce Grove + Leduc dropped)
# must remain exactly as committed. Fires at import time so drift is
# caught before any scorecard is written.
def _assert_city_sets_consistent() -> None:
    mo1_codes = {c["csd_code"] for c in _CITIES_FOR_MO1.values()}
    if not _BIG_CITY_CODES_FOR_MO2.issubset(mo1_codes):
        extra = _BIG_CITY_CODES_FOR_MO2 - mo1_codes
        raise RuntimeError(
            f"MO #2 big_city_codes contains CSDs not in MO #1 cities: "
            f"{sorted(extra)}. The two lists must remain in sync or "
            f"the methodology asymmetry must be amended in the pre-reg."
        )
    expected_dropped = {4811053, 4811028}  # Spruce Grove, Leduc
    actual_dropped = mo1_codes - _BIG_CITY_CODES_FOR_MO2
    if actual_dropped != expected_dropped:
        raise RuntimeError(
            f"MO #2 / MO #1 city-set asymmetry has changed. Expected "
            f"MO #2 to drop {sorted(expected_dropped)} relative to MO #1; "
            f"actually drops {sorted(actual_dropped)}. Update both lists "
            f"and the pre-registration if the change is intentional."
        )

_assert_city_sets_consistent()
```

The check freezes the current state as "this is what the audit committed to," and forces any future change through both lists. It does not silently fix the discrepancy — it makes the discrepancy load-bearing and visible.

## Decision the PI must make before authorising the check

1. Is the 8-vs-10 asymmetry intentional? If yes, the check above is the right shape and should be merged. The pre-registration should be amended to explicitly name the asymmetry and the rationale.
2. Or is the asymmetry a bug? If yes, the fix is to add `4811053` and `4811028` to `_BIG_CITY_CODES_FOR_MO2`, re-run the scorecard against the live and dry-run inputs, and disclose any output change in a transparent retraction note (the same way the canonical-anchoring DPG retraction was handled).

Either resolution is publishable. The current state — two undocumented divergent lists with no consistency enforcement — is not.

## Estimated effort if authorised

- Move both lists to module scope: 10 minutes
- Add the consistency check: 10 minutes
- Re-run the scorecard against the committed dry-run inputs and diff outputs: 10 minutes (once LFS is pulled)
- If outputs differ, write a retraction-style note in the dry-run report: 30 minutes

Total: under 1 hour. Trivial compared to the methodology question.

## Authorization checklist

Before any code in this proposal lands:

- [ ] Principal investigator decides whether the 8-vs-10 city-set asymmetry is intentional or a bug
- [ ] If intentional, the rationale is added to `preregistration/null_hypotheses.md` § MO #2
- [ ] If a bug, the eight-city set is extended to ten, the scorecard is re-run, and any output change is disclosed in `proposals/lunty_dry_run/dry_run_report.md`
- [ ] The consistency-check function above (or its corrected variant) is added to `phase_b_scorecard.py` and runs at import time
