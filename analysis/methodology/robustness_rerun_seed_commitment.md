# Seed Commitment — Robustness, Diagnostics, and Pending Channels

**Date:** 2026-05-10
**Purpose:** Pre-commit all random seeds for the three-section robustness/rerun registration before any analyses are executed.

---

## Drand Beacon

| Field | Value |
|---|---|
| Chain | Cloudflare drand (default) |
| Round | 6099592 |
| Randomness | `5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8` |
| Signature | `8a193647eedd3f423d261f05b3e4603702634486fae82ee032e35f5cf57c93c69b77d8897d5506b889d0dc0b29fbcbf413e098028bc77e69c59a1e8a6fee29b20465ef3dfd3b193deb55446b211d195fff17b0447e7d46f28c13c559520265ab` |
| Fetched | 2026-05-10, before OSF submission, before any runs |

Verification: `curl https://drand.cloudflare.com/public/6099592`

---

## Derivation Protocol

```python
import hashlib

randomness = "5b893b864ba71c70cfd0d0bb3b5549730eaeb282ea1140cf3d72a3167934a9a8"

# Section A: 10 SZAT robustness seeds
for i in range(10):
    h = hashlib.sha256(f"alberta-audit-robustness-szat-seed-{i}:{randomness}".encode()).hexdigest()
    seed = int(h[:8], 16)

# Section C: MCMC rerun base seed
h_c = hashlib.sha256(f"alberta-audit-mcmc-rerun-base:{randomness}".encode()).hexdigest()
base_seed = int(h_c[:8], 16)
```

---

## Section A — SZAT Multi-Seed Robustness Seeds

Post-hoc relative to OSF 6pt83 (primary result p=0.0024, seed committed 2026-04-27).
All 10 seeds fixed here before execution. Results reported regardless of direction.

| Index | Seed |
|---|---|
| seed_00 | 1225431167 |
| seed_01 | 2380378561 |
| seed_02 | 2351904413 |
| seed_03 | 768926600 |
| seed_04 | 156365611 |
| seed_05 | 1841997680 |
| seed_06 | 3405372638 |
| seed_07 | 1541506898 |
| seed_08 | 536299629 |
| seed_09 | 4096160843 |

---

## Section B — R-hat Convergence Diagnostic

No seed required. Deterministic computation on existing chain outputs:
`analysis/data/simulated_ensemble_raw_samples_canonical.csv` (250,000 draws, 2 chains × 125k).
Pass criterion: Gelman-Rubin R̂ < 1.1 on all four metrics (EG, MM, declination, seats@50/50).

---

## Section C — MCMC Rerun Base Seed

Prospective analysis; primary result unknown. Channels: population MAD ratio, Reock asymmetry, municipal anchoring departure.

| Field | Value |
|---|---|
| base_seed | 3562959107 |
| chains | 2 |
| plans per chain | 50,000 (100,000 total) |
| Additional outputs | per-plan population MAD, per-plan mean Reock, per-plan municipal anchor count |

---

## Order of Operations

1. Beacon fetched — 2026-05-10 ✓
2. Seeds derived and committed to git — 2026-05-10 ✓
3. OSF form submitted — **pending**
4. Analyses executed — **not yet run**
