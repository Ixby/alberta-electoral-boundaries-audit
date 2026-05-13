# Seed Commitment — Issue #14 Counter-Map Challenge

**Date:** 2026-05-10
**Purpose:** Pre-commit the random seed for the Issue #14 Trade-off Frontier counter-map run before any analysis is executed.

---

## Drand Beacon

| Field | Value |
| --- | --- |
| Chain | Cloudflare drand (default) |
| Round | 6099799 |
| Randomness | `d77d5fcb462447e3f0b13f16ea9693c8eb28318d8fba1a71631d9501d1fffab1` |
| Signature | `852c3fc3b5c7bc2b122aa9c2fda23f3fcd41725ac9bbe2f10f55971034c21d0878b6c632beb651c873b4287cb208013a076ba5ca3a1311b4624fe029d661526f4b17105f32b07d5f706211bae23845ccd5f8d2e337f5f2b35612bc9c97ec4b08` |
| Fetched | 2026-05-10, before OSF submission, before any runs |

Verification: `curl https://drand.cloudflare.com/public/6099799`

---

## Derivation Protocol

```python
import hashlib

randomness = "d77d5fcb462447e3f0b13f16ea9693c8eb28318d8fba1a71631d9501d1fffab1"

h = hashlib.sha256(f"alberta-audit-issue14-countermap:{randomness}".encode()).hexdigest()
issue14_seed = int(h[:8], 16)
```

---

## Derived Seed

| Field | Value |
| --- | --- |
| Salt | `alberta-audit-issue14-countermap` |
| SHA-256 hash | `f66ea63337f3cc08e93fd1a25fcb6d72a1b8468b2fcd28abe2d261d6e730f2c4` |
| **issue14_seed** | **4134446643** |

---

## Run Parameters (committed before execution)

| Parameter | Value |
| --- | --- |
| N_CHAINS | 2 |
| N_STEPS_PER_CHAIN | 50,000 (100,000 total) |
| CHECKPOINT_INTERVAL | 1,000 steps |
| CSD_WEIGHT | TBD — to be committed after Phase 3b hyperparameter tuning (2.0 / 5.0 / 10.0 grid search) |
| POP_DEVIATION | 0.25 (±25%) |
| ANCHORING_STORE_THRESHOLD | 0.50 |
| ANCHORING_SUCCESS_THRESHOLD | 0.60 |

CSD_WEIGHT will be committed to this file after the tuning pass and before the full run begins.

---

## Success Criteria (pre-committed)

| Outcome | Condition | Disposition |
| --- | --- | --- |
| Success | Best plan anchoring ≥60% AND all Tier A COI constraints pass | §5.8.5 retracted under condition B |
| Partial | Best plan anchoring 45–59% AND all Tier A COI constraints pass | §5.8.5 weakened, not retracted; reported as "material improvement, below majority-equivalence" |
| Null | Best plan anchoring <45% OR any Tier A COI constraint fails | §5.8.5 null stands; reported as "100k-plan CSD-biased search did not produce a Pareto-better map" |

---

## Order of Operations

1. Beacon fetched — 2026-05-10 ✓
2. Seed derived and committed to git — 2026-05-10 ✓
3. OSF pre-registration submitted — **pending**
4. Phase 3b demo + hyperparameter tuning — **pending**
5. CSD_WEIGHT committed to this file — **pending**
6. Full run executed — **pending**
