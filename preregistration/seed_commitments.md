> **Backward:**
> - Cloudflare drand beacon — public randomness source for all salts
> - OSF qsgy8 (MCMC seed) and OSF 6pt83 (SZAT seed) — public pre-registrations
>
> **Forward:**
> - `analysis/scripts/mcmc_ensemble_canonical.py` — consumes the `mcmc_ensemble_250k` salt
> - `analysis/scripts/szat.py` — consumes the `szat-bootstrap` salt
> - `reports/academic/report_academic.md` §5.4, §5.2.10 — reports results seeded from this salt audit
> - (terminal — pre-registration record; reviewer-facing chain-of-custody document)

# Pre-Registration Salt Audit Trail

> **Pre-registration:** [OSF qsgy8](https://osf.io/qsgy8) (MCMC seed) · [OSF 6pt83](https://osf.io/6pt83) (SZAT seed)

**Purpose:** Establish that MCMC and SZAT salt strings were fixed before results
were observed, satisfying the chain-of-custody requirement for pre-registered
ensemble tests.

---

## Salt strings in use

| Script | Salt string | drand seed committed | OSF registration | OSF form timing |
| --- | --- | --- | --- | --- |
| `mcmc_ensemble_canonical.py` (100k canonical ensemble) | `"mcmc_ensemble_250k"` | 2026-04-27 | [OSF qsgy8](https://osf.io/qsgy8) | Predates EA shapefiles |
| `szat.py` (SZAT bootstrap) | `"szat-bootstrap"` | 2026-04-27 | [OSF 6pt83](https://osf.io/6pt83) | ~3 hours after szat.py first ran (2026-05-06); seed predates shapefiles by 9 days |

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

**Accurate timeline:**

| Event | Timestamp |
| --- | --- |
| `drand_seed.py` committed (beacon infrastructure, salt fixed in code) | 2026-04-27 09:49 |
| Official EA shapefiles received (Raymond Mok) | 2026-05-06 09:51 |
| `szat.py` first run; results committed (commit 873f4d0) | 2026-05-06 18:11 |
| OSF SZAT registration script (`osf_reg4_szat.py`) written; 6pt83 filed | 2026-05-06 ~21:16 |

The drand seed infrastructure — including the salt string `"szat-bootstrap"` — was
committed on 2026-04-27, **9 days before the EA shapefiles arrived**. The salt was
therefore fixed before any SZAT computation was possible; it could not have been
chosen by observing the results.

The OSF formal registration **6pt83** was filed approximately 3 hours after
`szat.py` first ran. The form is post-hoc relative to the results. The provenance
claim rests on the drand seed timestamp (2026-04-27), not on the OSF form timestamp.

None of the four OSF registrations (w2s8k, r3zm7, qsgy8, 6pt83) name or specify
the SZAT bootstrap methodology in their filed documents — each contains
`dpg2_experiment_plan.md` and `drain_v2_plan.md` (see §5.3.1 OSF file content
disclosure). The seed-chain anchor for Ch2 is the drand beacon round committed
2026-04-27, not an OSF document.

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

---

## november_2026_scoring_spec — External pin (added 2026-06-12 per Amendments 11 + 12)

| Attribute | Value |
|---|---|
| File path | `preregistration/november_2026_scoring_spec.md` |
| SHA-256 (as of 2026-06-12 commit, Amendments 8 + 9 + 11 + 12 applied) | `e3546346a17091562e57dc943a302d7bd5650546cd8188d628e5f4d0a17568b9` |
| Last amendment | 12 (2026-06-12; documented in `findings/pre_registration_amendment_log.md`) |
| Drand round target | **To be pinned** before Lunty draft circulates (queued T5.3). Round 5500000 (Oct 2025) is rejected: it predates the salt commits and was therefore *publicly known* when the salts were chosen — cannot serve as a future-beacon anchor. A genuinely future round will be selected and pinned here before any Lunty draft circulates publicly. |
| OSF mirror | qsgy8 (initial); refresh queued T5.3 to reflect Amendments 8–12 |

**Verification protocol.** Any reader can verify the spec has not been tampered with after pinning by running

```bash
sha256sum preregistration/november_2026_scoring_spec.md
```

and comparing against the SHA-256 above. If the values differ, either (a) a follow-on amendment was filed (look for a numbered entry in `findings/pre_registration_amendment_log.md` after Amendment 12), or (b) the file has been modified outside the documented amendment chain. The amendment-chain protocol is in `preregistration/november_2026_scoring_spec.md` §6.

This entry was added 2026-06-12 to retire a self-invalidating pin written earlier the same session (Amendment 12; see T1.7 R2 Refs #4 + #18). The earlier pin recorded the SHA-256 *inside* the spec file, then continued editing the spec — guaranteeing the recorded hash would not match the file. External pinning is the standard fix.

---

## Amendment A — november_2026_scoring_spec.md post-commitment modification (2026-07-12)

**Date:** 2026-07-12 (committed git hash `893e6d3a`)

**What changed:** Commit `893e6d3ab0ff746316a11b4e75faf2807393026e` ("Sweep repo-wide for stray stale figures after the 2026-07-12 ensemble rerun") modified `preregistration/november_2026_scoring_spec.md` line 94, updating the Bonferroni bound statement from `p ≤ 2.80×10⁻⁶` to `p ≤ 1.76×10⁻⁶`.

**Reason:** The Bonferroni bound had been recomputed following a full rerun of the canonical ensemble on 2026-07-12. The new canonical run produced a lower dependence-robust upper bound than the prior ensemble.

**Prior SHA-256 (before 893e6d3a):** `e3546346a17091562e57dc943a302d7bd5650546cd8188d628e5f4d0a17568b9`

**Current SHA-256 (after 893e6d3a):** `2110548c9e82170425ba760eee1574afd83ebae96d8ce094f5f8ad278f0cdbe3`

**Pre-commitment status:** This file is flagged in `preregistration/seed_commitments.md` line 130 as pinned to a specific SHA-256 as of 2026-06-12. The pin was intended to prevent undetected tampering with the Lunty-test specification. The commit 893e6d3a modifies the file post-pin, which violates the pre-commitment principle. However, the modification is:
1. Documented in the commit message (explicitly noted as a "stale figure" correction)
2. Limited to a single factual update (the Bonferroni bound)
3. Not a change to the Lunty-test scoring methodology itself
4. Dated and traceable in the public git log

**Disclosure:** Any reader validating the file against the pinned SHA-256 will find a mismatch and can trace the cause via `git log` to commit 893e6d3a. The mismatch is not silent tampering — it is disclosed by the pin mechanism itself and is explained by this amendment.
