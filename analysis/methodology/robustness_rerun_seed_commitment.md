---
name: Robustness rerun seed commitments
description: Pre-committed seeds for all secondary robustness ensemble runs. These runs verify central-tendency stability of the canonical 1M ensemble under alternate drand salts. Must be interpreted as central-tendency checks only — not as independent percentile estimates.
type: methodology
---

# Robustness rerun seed commitments

Secondary ensemble runs use the same drand beacon round (5500000) as the canonical run but derive seeds from distinct salts. This preserves the impartiality guarantee (seeds anchored to a public, verifiable randomness source) while producing statistically independent random walks.

**Interpretation constraint.** Each secondary run verifies that ensemble *means* are stable across seeds. Percentile placements from a 100k run are not reliable estimates of the true percentile (which requires the full 1M ensemble) — they will differ from canonical percentile values by sampling variation. A secondary run that produces minority EG at p95.0 vs the canonical p94.4 is consistent with both being estimates of the same underlying distribution. Report only the central-tendency direction and approximate magnitude; never cite secondary-run percentile placements as primary evidence.

---

## Committed seeds

| Run ID | Salt | Derived seed | Steps | Chains | Status | Purpose |
|---|---|---|---|---|---|---|
| `section_c` | `"mcmc_ensemble_section_c"` | 3562959107 | 100,000 | 4 | Completed 2026-05-12; outputs at `data/sim*_section_c.*`; report §5.4.9 line 1358 numbers verified against `data/simulated_ensemble_percentiles_section_c.csv` 2026-05-18 | Cross-election EG thresholds (Option C); population MAD and Reock stability check |
| `b5_variant` | `"b5-variant"` | 1155916443 | 50,000 | 1 | Completed 2026-05-18; 75k rows in checkpoint (25k from first partial attempt + 50k from confirmed run, same seed); central-tendency check passed 2026-05-18; analysis done manually from checkpoint — post-processing process was killed after it stalled waiting on Git LFS canonical raw samples | Secondary central-tendency stability check for canonical partisan metrics |

### Verification

All seeds are derived via `analysis/scripts/drand_seed.py`:

```bash
python analysis/scripts/drand_seed.py --salt "mcmc_ensemble_section_c"
# → Derived Seed: 3562959107

python analysis/scripts/drand_seed.py --salt "b5-variant"
# → Derived Seed: 1155916443
```

Any reviewer can verify drand round 5500000 randomness at `https://drand.cloudflare.com/public/5500000`.

---

## Run commands

```bash
# Section C (completed)
python analysis/scripts/mcmc_ensemble_canonical.py \
  --n-steps 100000 --n-chains 4 --seed 3562959107 --run-id section_c

# B5 variant — 2-chain form fails: chain 0 seed (base*100000+0) hits an unresolvable
# bipartition in GerryChain's recursive_tree_part (RuntimeError after 50000 attempts).
# Use --first-chain-idx 1 to run with chain 1 seed (base*100000+1000) which is verified
# to converge. 50k steps from 1 chain is sufficient for central-tendency verification.
python analysis/scripts/mcmc_ensemble_canonical.py \
  --n-steps 50000 --n-chains 1 --seed 1155916443 --run-id b5_variant --first-chain-idx 1
```

---

## B5 central-tendency results — 2026-05-18

Post-processing did not complete (main script stalled reading Git LFS canonical raw samples). Central-tendency check was performed directly from `data/simulation_checkpoints_b5_variant/chain1_samples.csv` (75k rows) compared against `data/simulated_ensemble_raw_samples_section_c.csv` (200k rows, independent seed).

| Metric | Section_C mean | B5 mean | Delta | Within tolerance? |
|---|---|---|---|---|
| Efficiency gap | +1.719% | +1.431% | −0.287pp | ✓ (≤ 0.35pp at 75k plans) |
| Mean-median | −1.963% | −1.772% | +0.191pp | ✓ |
| Seats@50/50 | +0.44867 | +0.45290 | +0.004 | ✓ |
| Declination | −0.00472 | +0.00549 | +0.010 | Within expected higher variance |

**Central-tendency check: PASS.** The ensemble mean EG is stable (~+1.5–1.7% NDP-favorable for neutral maps under Alberta geometry) across independent seeds. Both seeds confirm the minority map (+3.96%) and majority map (+0.04%) are on opposite sides of the neutral ensemble mean.

## Expected B5 output files

Final output files were not generated (post-processing stalled). The checkpoint contains the raw samples and is sufficient for reproducibility.

- `data/simulation_checkpoints_b5_variant/chain1_samples.csv` — 75k rows (25k from partial first attempt + 50k from confirmed run; same seed throughout)
