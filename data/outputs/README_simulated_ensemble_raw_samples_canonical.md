# `simulated_ensemble_raw_samples_canonical.csv`

The pooled cache of the canonical ensemble: the four chain CSVs at
`data/simulation_checkpoints_canonical/chain{0,1,2,3}_samples.csv`, concatenated
in order (4 × 252,500 = 1,010,000 rows). It is LFS-tracked (oid `cb09ae5693…`,
about 170 MB). It matches the chain CSVs value for value. Its declination column
uses the sign set in Amendment 5, Part 9; the mean is +0.00142.

`analysis/scripts/joint_outlier_score_canonical.py` and
`analysis/scripts/verify_joint_empirical_bound.py` read it.

The chain CSVs are authoritative; the pool is a regenerable duplicate. To rebuild
it from them:

```python
import pandas as pd
from pathlib import Path
parts = [pd.read_csv(p) for p in sorted(Path('data/simulation_checkpoints_canonical').glob('chain*_samples.csv'))]
pooled = pd.concat(parts, ignore_index=True)
pooled.to_csv('data/outputs/simulated_ensemble_raw_samples_canonical.csv',
              index=False, float_format='%.17g')
```

See `findings/pre_registration_amendment_log.md` Amendment 5, Part 9 for the
declination sign.
