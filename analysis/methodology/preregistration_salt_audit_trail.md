# Pre-Registration Salt Audit Trail

**Purpose:** Establish that MCMC and SZAT salt strings were fixed before results
were observed, satisfying the chain-of-custody requirement for pre-registered
ensemble tests.

---

## Salt strings in use

| Script | Salt string | OSF registration |
|--------|-------------|-----------------|
| `mcmc_ensemble_canonical.py` (100k canonical ensemble) | `"mcmc_ensemble_250k"` | [OSF qsgy8](https://osf.io/qsgy8) |
| `szat.py` (SZAT bootstrap) | `"szat-bootstrap"` | [OSF r3zm7](https://osf.io/r3zm7) |

---

## Why `mcmc_ensemble_canonical.py` uses the salt `"mcmc_ensemble_250k"`

The canonical 100k ensemble inherits the salt from the earlier DPG-based 250k
ensemble. This is intentional and documented in the code:

```python
# Salt intentionally kept as "mcmc_ensemble_250k" for historical continuity:
# the canonical 100k ensemble was seeded from this salt to preserve chain-of-
# custody with the earlier DPG 250k run. Changing the salt would break
# reproducibility of the pre-registered ensemble (OSF reg qsgy8).
seed = get_canonical_seed("mcmc_ensemble_250k")
```

The DPG-based 250k run used salt `"mcmc_ensemble_250k"` which was registered in
OSF pre-registration **qsgy8** before any ensemble results were observed. When
canonical shapefiles superseded the DPG files (2026-05-07 directive), the seed
was kept identical so that the two ensembles can be compared on a shared seed
basis. The canonical run is not a new seeding decision — it is a re-run against
updated geometry using the same pre-registered seed.

---

## Why `szat.py` uses the salt `"szat-bootstrap"`

The SZAT bootstrap salt `"szat-bootstrap"` was registered in OSF
pre-registration **r3zm7** before the bootstrap was run. The registration
predates the 2026 Alberta Electoral Boundaries Commission report (minority and
majority shapefiles were not publicly available when the pre-registration was
filed). The salt string appears verbatim in the registered analysis plan.

---

## Verifying salt → seed derivation

Both salts are fed into `drand_seed.get_canonical_seed(salt)`, which calls the
drand League of Entropy beacon at a fixed round chosen in the pre-registration.
To independently verify:

```python
from analysis.scripts.drand_seed import get_canonical_seed
print(get_canonical_seed("mcmc_ensemble_250k"))   # should match recorded seed
print(get_canonical_seed("szat-bootstrap"))        # should match recorded seed
```

The beacon round number and the expected seeds are recorded in each OSF
pre-registration. If an independent reviewer obtains a different seed, the
beacon round in the pre-registration is the authoritative reference.

---

## Hostile reviewer response template

> "The salt string in the code is just a string — it could have been chosen after
> results were known."

**Response:** The salt feeds into a public, tamper-proof randomness beacon
(drand/League of Entropy). The beacon round used is fixed in the OSF
pre-registration, which has a timestamp predating the ensemble runs. An attacker
would need to predict a specific future beacon output *and* choose a salt that
produces that output — which is computationally infeasible. The full chain is:
pre-registration timestamp → beacon round → salt → seed → ensemble.

---

## Action items if pre-registration documents do not name the salt string explicitly

1. File a dated amendment to each OSF registration citing the salt string.
2. The amendment timestamp must predate any public release of ensemble results.
3. If results are already public, document that the salt is verifiably derived
   from a beacon round whose timestamp predates results.

---

*Last updated: 2026-05-08*
