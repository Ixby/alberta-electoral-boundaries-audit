# `simulated_ensemble_raw_samples_canonical.csv` — substrate-stale (2026-06-12)

The LFS-tracked version of this file (oid `eef920b85e…`, size ~170 MB) was
committed *before* Amendment 10 (the declination sign-convention correction,
2026-06-12). Its declination column carries the pre-Amendment-10 sign
(mean ≈ −0.00246 instead of the corrected +0.00246).

**Do not consume the LFS-tracked version directly.** Either:

1. **Regenerate locally from canonical chain CSVs** (preferred):
   ```python
   import pandas as pd
   from pathlib import Path
   parts = [pd.read_csv(p) for p in sorted(Path('data/simulation_checkpoints_canonical').glob('chain*_samples.csv'))]
   pooled = pd.concat(parts, ignore_index=True)
   pooled.to_csv('data/outputs/simulated_ensemble_raw_samples_canonical.csv',
                 index=False, float_format='%.17g')
   ```

2. **Use the canonical chain CSVs directly** — every consumer of this file
   can equivalently iterate over the 4 chain CSVs at
   `data/simulation_checkpoints_canonical/chain{0,1,2,3}_samples.csv`.
   That is the canonical source.

The pooled cache is retained as an LFS pointer for repository-size reasons
(the LFS server cannot accept the post-flip blob in the current proxy
configuration). The chain CSVs are authoritative; the pool is a regenerable
duplicate.

See `findings/pre_registration_amendment_log.md` Amendment 10 for the full
sign-correction record.
