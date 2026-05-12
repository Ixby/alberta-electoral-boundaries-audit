# Reproducing this audit

This document is the entry point for anyone who wants to **audit the audit**: re-run the analyses, verify the headline numbers, or extend the methodology with their own checks. The audit is designed to be reproducible from a clean clone of the repository on a modern laptop. If anything below doesn't work as described, that's a bug — please open a GitHub issue.

---

## What you can verify, and how long it takes

| Verification | Wall time | Hardware |
|---|---|---|
| Forensic spot-check (10,000 maps with full assignments) | ~2 min | any laptop |
| Canonical 1M MCMC ensemble (4 × 252,500 continuous chains) | ~6–8 h | 4-core, 16 GB |
| Targeted-gerrymander short-bursts test (UCP + NDP directions) | ~12 min | any laptop |
| Rural-protection comparative analysis | <30 s | any laptop |
| Magazine PDF rebuild | ~30 s | any laptop |

Total time to reproduce every quantitative claim in `report_public.pdf` from a clean clone: **about 30 minutes**.

---

## Step 1 — Clone and set up

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit

# Git LFS is required for the 250k MCMC metric record (~30 MB)
git lfs install
git lfs pull

# Python 3.11+ recommended (3.14 verified)
python -m venv .venv
source .venv/bin/activate         # bash; on PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Pinned versions matter.** The audit's deterministic results require `gerrychain==0.3.2` (and the rest of `requirements.txt`). Newer gerrychain releases may change ReCom proposal behaviour; you'll get *similar* numbers but not bit-identical ones. If you want bit-identical reproduction, use the pinned versions.

---

## Step 2 — Verify the forensic spot-check (the fastest check)

This is the cleanest single verification: 10,000 ReCom steps with full per-step partition assignments serialized to disk. You can pick any of the 10,000 saved partitions, recompute its metrics from scratch, and confirm they match what the audit reports.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/mcmc_verification_subset.py
```

Expected output: `data/simulation_verification_metrics.csv` (10,000 rows of metrics) + `data/verification_assignments_raw.npz` (compressed int8 array of 10,000 partition vectors).

To verify a specific partition:

```python
import numpy as np
import pandas as pd

# Load the pre-committed verification artefacts
m = pd.read_csv("data/simulation_verification_metrics.csv")
d = np.load("data/verification_assignments_raw.npz")
assignments = d["assignments"]
va_ids = d["va_ids"]

# Pick step 5000 as an example
step_idx = 5000
saved_metrics = m.iloc[step_idx]
saved_assignment = assignments[step_idx]   # shape (n_va,) int8 array

# Recompute metrics from scratch using the saved assignment
# (see analysis/scripts/mcmc_ensemble.py:seat_results for the formula)
# ... your independent reimplementation here ...

# Confirm match
print(saved_metrics)
```

If your independent reimplementation produces the same `efficiency_gap`, `seats_at_50_50`, `mean_median`, and `declination` as `saved_metrics`, the audit's procedure on this map is verified.

---

## Step 3 — Reproduce the canonical 1M MCMC ensemble

> **CANONICAL ENSEMBLE:** All published results use the 1,010,000-plan canonical run described here.
> Base seed: 1,432,864,451 (drand round, salt "mcmc_ensemble_250k", OSF registration qsgy8).
> The per-chain checkpoint CSVs are committed under `data/simulation_checkpoints_canonical/`
> (4 files, ~1 GB total — stored via Git LFS). Running the script from scratch reproduces
> the same ensemble because the seed is deterministic from the drand beacon.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/mcmc_ensemble_canonical.py --n-steps 250000
```

Expected wall time: ~6–8 h total (4 chains parallelised on a 4-core machine). The canonical artefacts are already committed:

- `data/simulation_checkpoints_canonical/chain{0..3}_samples.csv` — 252,500 rows each, 4 chains, 1,010,000 total plans. Columns: `efficiency_gap`, `mean_median`, `declination`, `seats_at_50_50`, `chain`, and compactness proxies.
- `data/outputs/simulated_ensemble_percentiles_canonical.csv` — per-metric percentile rankings for all three maps
- `data/outputs/simulation_convergence_diagnostics_canonical.json` — ESS, rho_lag1, Gelman-Rubin per chain

Headline findings to verify (all against the 1M canonical ensemble):

- The minority map's mean-median difference sits at the **p99.98** of the neutral ensemble.
- The minority map's `seats@50/50` value (p99.99) — only ~66 of 1,010,000 neutral plans reach this level of UCP seat advantage at an even vote split.
- The minority map's declination sits at **p1.21** (NDP tail — extreme concentration of NDP votes).
- The minority map's efficiency gap sits at **p94.4** — below the individual 95th-percentile flag threshold.
- The majority map sits within the neutral null on all four metrics.

---

## Step 4 — Reproduce the targeted-gerrymander short-bursts test

This is the symmetry test that confirms a non-neutral procedure can reach the minority's territory while the majority sits comfortably inside the neutral range.

```bash
# UCP-maximizing direction: confirms a non-neutral procedure can reach 52.87% (which encompasses the minority's 51.69%)
PYTHONIOENCODING=utf-8 python analysis/scripts/targeted_gerrymander_burst.py

# NDP-maximizing direction (symmetric mirror): confirms targeted procedures can drive seats@50/50 down to 37.93% (well below the majority's 43.7%)
PYTHONIOENCODING=utf-8 python analysis/scripts/targeted_gerrymander_burst_ndp.py
```

Each takes ~6 min. Outputs at `data/v0_1_targeted_burst_*.json` and `_trace.csv`.

Method: Cannon, Goldbloom-Helzner, Gupta, Matthews, Suwal (2022) short-bursts hill-climbing. 800 bursts × 50 ReCom steps each, accept the most-favourable partition from each burst as the seed for the next.

---

## Step 5 — Reproduce the rural-protection comparative analysis

Computes per-voter representation weight for rural vs urban districts under all three maps; counts hybrid EDs and s.15(2) declarations.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/rural_protection_test.py
```

Wall time: <30 seconds. Headline numbers to verify:

- **2019 enacted:** rural voters carry 4.4% more weight than urban
- **2026 majority:** 11.9% more weight; 3 EDs declared under s.15(2) (Canmore-Banff, Central Peace-Notley, Lesser Slave Lake)
- **2026 minority:** 22.9% more weight; 0 s.15(2) declarations; 17 hybrid EDs under the operational area-share rule (vs majority's 14, vs 2019 baseline 8). The narrative manual count published in earlier drafts (25 vs 9) was not reproducible by an automated rule and has been superseded — see `analysis/reports/dangerzone_metric_definitions.md`.

---

## Step 6 — Rebuild the magazine PDF

Regenerates `report_public.pdf` from `report_public.md` + cover art.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py
```

Wall time: ~30 seconds. The intermediate `article.pdf` and `article.html` are written to `.temp/` (gitignored). The final merged `report_public.pdf` is what most readers see.

---

## What's preserved for byte-verifiable forensic verification

| Artefact | Storage | What it proves |
|---|---|---|
| `data/simulation_checkpoints_canonical/chain{0..3}_samples.csv` (4 chains, ~1 GB) | Git LFS | Every step in the canonical 1M ensemble; `chain` column enables Gelman-Rubin |
| `data/outputs/simulated_ensemble_percentiles_canonical.csv` | Git regular | Per-metric percentile rankings for all three maps against the 1M ensemble |
| 10k forensic verification subset | Git regular (1.84 MB compressed) | Byte-verifiable spot-check: pick any saved partition, recompute, confirm |
| Targeted-burst trace + best.json | Git regular | The Cannon et al. short-bursts hill-climb result |
| Pre-registration draft + amendments | Git regular | The discipline chain: what was promised, what changed, when |
| Methodology files (`analysis/methodology/`) | Git regular | Per-claim evidence trail with primary-source citations |

**Reproducibility is the audit's first-line defense against any "you didn't actually do this" critique.** All artefacts above survive a fresh clone; nothing depends on any author-only resource.

---

## Official Elections Alberta shapefiles (received 2026-05-06)

Elections Alberta released official vector shapefiles on 2026-05-06 (commit `873f4d0`). All analysis uses these canonical files:

- `data/shapefiles/canonical/ea_majority_2026_eds.gpkg`
- `data/shapefiles/canonical/ea_minority_2026_eds.gpkg`

The Derived Provisional Geometries (DPG) reconstruction pipeline is preserved in `analysis/methodology/` for audit-trail completeness but is no longer used in any published claim. Any DPG-era value that differs from the canonical results is documented in `analysis/methodology/canonical_shapefile_log.md`.

---

## Open issues / honest gaps

The "where this audit falls short" honest self-assessment is in the public report's "Behind the audit" section. The single biggest gap is **external replication**: the audit is reproducible by design but has not yet been independently re-run by anyone outside the project. If you reproduce the audit using this document, please open a GitHub issue confirming what you ran, what you got, and where (if anywhere) the numbers differed. That feedback is the most valuable possible contribution.

---

## Contributors and AI-tooling attribution

This is a single-author audit (Will Conner, project author) executed with substantial assistance from two AI systems acting as adversarial collaborators:

- **Claude Opus 4.7 (Anthropic)** — primary co-author for code, prose, hypothesis-tracker maintenance, and editorial work. Authored most commits; runs as the operating shell during analysis sessions.
- **Google Gemini 3.1 Pro** — adversarial code reviewer and red-team author. Identified the Gemini-9 code audit findings (commit `73544a3`); authored the v0_9 topological VA-dissolve substrate (`analysis/scripts/topological_shape_resolution.py`); identified the Two-Party share + s15(2) freeze methodological flaws and implemented the initial fixes (commit `972b04a`); authored the methodological-defenses appendix (`analysis/methodology/methodological_defenses.md`).

**Attribution policy.** Every commit in this repo records its substantive co-author via `Co-Authored-By:` trailers. When a finding originated with one of the AI collaborators, the trailer names them — *not* as a deflection of authorial responsibility (the project author signs off on every change) but so a future reader can trace the provenance of any specific number, fix, or framing back to its source. This audit treats the AI tools as named external collaborators rather than invisible production infrastructure, in keeping with the audit's general transparency standard.

The PO retains final editorial and methodological responsibility for everything in this repository.

---

## Contact

Will Conner — `wconn161@mtroyal.ca` (project author). For methodology questions, open a GitHub issue at <https://github.com/Ixby/alberta-electoral-boundaries-audit/issues>.
