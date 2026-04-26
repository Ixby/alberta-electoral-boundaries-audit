# Setup — pinned interpreter and build environment

This file pins the Python interpreter and OS environment used to produce
the numbers in `report_academic.md` v0.2 (committed 2026-04-22). It
complements `requirements.txt` (library versions) and
`FROZEN_MANIFEST.md` (external URLs).

## Interpreter

- **Python 3.14.3** (CPython, 64-bit)
- **Platform:** Windows 11 Education, build 26100

Python 3.11 is the minimum declared in `setup.sh`; 3.14.3 is what the
author's session actually ran. If a future reproduction uses 3.12 or
3.13, note the divergence in the run log — floating-point behaviour and
`statistics` module internals are stable across these versions but
library wheel availability is not.

## Install

```bash
# from the repository root:
python -m pip install -r requirements.txt
```

If `gerrychain` fails to install on a given platform, Phase 5 (B5 MCMC
ensemble) will be blocked but all other sections remain reproducible.

## Verification

A minimal smoke-test on install:

```bash
python -c "import pandas, numpy, geopandas, shapely, pyproj; print('OK')"
python3 analysis/scripts/v0_2_packing_cracking_analysis.py | head -5
```

Expected final digits on 2019-baseline B1-B4 (from the same Python 3.14.3
run the report was generated on):

```
2019 BOUNDARIES: EG -2.64%, MM -2.22pp, NDP@50/50 46, sim 38/49
```

If these differ, investigate before trusting any downstream number.

## Reproducibility expectations

Pinned versions in `requirements.txt` cover the Python library layer.
Three additional layers of reproducibility-decay risk are documented in
`FROZEN_MANIFEST.md`:

1. **External URL drift** — Elections Alberta, Statistics Canada, and
   338Canada may reorganise their URL structures.
2. **Shapefile release** — the 2026 ED shapefiles were not released at
   time of analysis; phases dependent on them are blocked regardless of
   library versioning.
3. **Commission PDF content** — the commission's report PDF
   (`abebc_2026_rpt_final.pdf`) is treated as immutable by SHA-256 for
   the life of the audit; URL may drift.

See `FROZEN_MANIFEST.md` for dates of last successful access.
