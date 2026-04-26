# Reproducing this audit

This document is the entry point for anyone who wants to **audit the audit**: re-run the analyses, verify the headline numbers, or extend the methodology with their own checks. The audit is designed to be reproducible from a clean clone of the repository on a modern laptop. If anything below doesn't work as described, that's a bug — please open a GitHub issue.

---

## What you can verify, and how long it takes

| Verification | Wall time | Hardware |
|---|---|---|
| Forensic spot-check (10,000 maps with full assignments) | ~2 min | any laptop |
| Full 2,000,000-map MCMC ensemble | ~60 min | 4-core, 16 GB |
| Targeted-gerrymander short-bursts test (UCP + NDP directions) | ~12 min | any laptop |
| Rural-protection comparative analysis | <30 s | any laptop |
| Magazine PDF rebuild | ~30 s | any laptop |

Total time to reproduce every quantitative claim in `report_public.pdf` from a clean clone: **about 90 minutes**.

---

## Step 1 — Clone and set up

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit.git
cd alberta-electoral-boundaries-audit

# Git LFS is required for the 2M MCMC metric record (~237 MB)
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
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_mcmc_verification_subset.py
```

Expected output: `data/v0_1_mcmc_verification_metrics.csv` (10,000 rows of metrics) + `data/v0_1_mcmc_verification_assignments.npz` (compressed int8 array of 10,000 partition vectors).

To verify a specific partition:

```python
import numpy as np
import pandas as pd

# Load the pre-committed verification artefacts
m = pd.read_csv("data/v0_1_mcmc_verification_metrics.csv")
d = np.load("data/v0_1_mcmc_verification_assignments.npz")
assignments = d["assignments"]
va_ids = d["va_ids"]

# Pick step 5000 as an example
step_idx = 5000
saved_metrics = m.iloc[step_idx]
saved_assignment = assignments[step_idx]   # shape (n_va,) int8 array

# Recompute metrics from scratch using the saved assignment
# (see analysis/scripts/v0_1_mcmc_ensemble.py:seat_results for the formula)
# ... your independent reimplementation here ...

# Confirm match
print(saved_metrics)
```

If your independent reimplementation produces the same `efficiency_gap`, `seats_at_50_50`, `mean_median`, and `declination` as `saved_metrics`, the audit's procedure on this map is verified.

---

## Step 3 — Reproduce the headline 2M MCMC ensemble

This is the audit's authoritative simulation. Outputs all five files the article cites.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_mcmc_ensemble_250k_v0_8.py \
    --n-steps 2000000 --n-chains 4 --chunk-size 5000 --seed 88
```

Expected wall time: ~60 min on a 13th-gen i7-1360P. Outputs:

- `data/v0_1_mcmc_ensemble_percentiles_250k_v0_8.csv` — percentile placements for the three real maps
- `data/v0_1_mcmc_real_map_scores_250k_v0_8.json` — real-map metric scores
- `data/v0_1_mcmc_convergence_diagnostics_250k_v0_8.json` — ESS, autocorrelation by metric
- `data/mcmc_checkpoints_250k_v0_8/chain{0..3}_samples.csv` — per-chain metric record (these are the LFS-tracked artefacts; ~237 MB total)
- `analysis/reports/v0_1_mcmc_2M_v0_8_full.log` — full run log

Headline finding to verify: the simulation's `seats@50/50` ceiling holds at **51.72%** (45 of 87 simulated seats). No map in 2,000,000 reaches the minority commission map's 52.8% value. The reproduction is bit-identical if you used the pinned `gerrychain==0.3.2`.

---

## Step 4 — Reproduce the targeted-gerrymander short-bursts test

This is the symmetry test that confirms a non-neutral procedure can reach the minority's territory while the majority sits comfortably inside the neutral range.

```bash
# UCP-maximizing direction: confirms a non-neutral procedure can reach 52.87% (within rounding of the minority's 52.8%)
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_targeted_gerrymander_burst.py

# NDP-maximizing direction (symmetric mirror): confirms targeted procedures can drive seats@50/50 down to 37.93% (well below the majority's 43.7%)
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_targeted_gerrymander_burst_ndp.py
```

Each takes ~6 min. Outputs at `data/v0_1_targeted_burst_*.json` and `_trace.csv`.

Method: Cannon, Goldbloom-Helzner, Gupta, Matthews, Suwal (2022) short-bursts hill-climbing. 800 bursts × 50 ReCom steps each, accept the most-favourable partition from each burst as the seed for the next.

---

## Step 5 — Reproduce the rural-protection comparative analysis

Computes per-voter representation weight for rural vs urban districts under all three maps; counts hybrid EDs and s.15(2) declarations.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_rural_protection_test.py
```

Wall time: <30 seconds. Headline numbers to verify:

- **2019 enacted:** rural voters carry 4.4% more weight than urban
- **2026 majority:** 11.9% more weight; 3 EDs declared under s.15(2) (Canmore-Banff, Central Peace-Notley, Lesser Slave Lake)
- **2026 minority:** 22.9% more weight; 0 s.15(2) declarations; 25 hybrid EDs (vs majority's 9)

---

## Step 6 — Reproduce the fuzzing analysis on missing-ED attribution

Tests how sensitive the seats@50/50 finding is to different attribution choices for the 6 minority-map districts that don't catch a 2023 voting-area centroid.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/v0_1_fuzz_missing_eds.py
```

Wall time: ~30 seconds. Headline numbers to verify:

- Inheritance-2019 (most defensible): 52.8%
- Worst case (all 6 missing assumed strongly NDP): 51.7%
- Best case (all 6 missing assumed strongly UCP): 57.3%
- Random-resample (10,000 trials): 88.9% of trials place minority above the simulation's 51.72% ceiling

---

## Step 7 — Rebuild the magazine PDF

Regenerates `report_public.pdf` from `report_public.md` + cover art.

```bash
PYTHONIOENCODING=utf-8 python analysis/scripts/build_cover.py
```

Wall time: ~30 seconds. The intermediate `article.pdf` and `article.html` are written to `.temp/` (gitignored). The final merged `report_public.pdf` is what most readers see.

---

## What's preserved for byte-verifiable forensic verification

| Artefact | Storage | What it proves |
|---|---|---|
| 4× per-chain metric CSVs (~237 MB) | Git LFS | Every step in the 2M ensemble's metric record |
| 10k forensic verification subset | Git regular (1.84 MB compressed) | Byte-verifiable spot-check: pick any saved partition, recompute, confirm |
| Targeted-burst trace + best.json | Git regular | The Cannon et al. short-bursts hill-climb result |
| Pre-registration draft + amendments | Git regular | The discipline chain: what was promised, what changed, when |
| Methodology files (`analysis/methodology/`) | Git regular | Per-claim evidence trail with primary-source citations |

**Reproducibility is the audit's first-line defense against any "you didn't actually do this" critique.** All artefacts above survive a fresh clone; nothing depends on any author-only resource.

---

## When the official Elections Alberta shapefiles are released

Run the wrapper:

```bash
bash analysis/scripts/recompute_against_official_shapefiles.sh \
    /path/to/official_majority_2026.gpkg \
    /path/to/official_minority_2026.gpkg
```

This snapshots the current outputs to `archive/recompute_<timestamp>/`, stages the official files, re-runs the audit pipeline (90 min), computes deltas vs published values, generates a stub pre-registration amendment file, and rebuilds `report_public.pdf`. The maintainer then reviews the deltas and prose-updates as needed. See the script's docstring for full detail.

If you want continuous monitoring of Elections Alberta for shapefile releases, see `analysis/automation/changedetection_setup.md` for the ChangeDetection.io + GitHub Actions trigger pipeline.

---

## Open issues / honest gaps

The "where this audit falls short" honest self-assessment is in the public report's "Behind the audit" section. The single biggest gap is **external replication**: the audit is reproducible by design but has not yet been independently re-run by anyone outside the project. If you reproduce the audit using this document, please open a GitHub issue confirming what you ran, what you got, and where (if anywhere) the numbers differed. That feedback is the most valuable possible contribution.

---

## Contact

Will Conner — `wconn161@mtroyal.ca` (project author). For methodology questions, open a GitHub issue at <https://github.com/Ixby/alberta-electoral-boundaries-audit/issues>.
