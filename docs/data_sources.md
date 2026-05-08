# Data Sources

## Files excluded from automated SHA256 verification (`hash_inputs.py`)

The following input files exceed the 50 MB size limit used by `hash_inputs.py` and are
therefore excluded from the automated hash check. Their integrity is documented here
instead and should be verified manually before any re-run.

---

### Statistics Canada Census 2021 Profile — Dissemination Area level

| Field | Value |
|---|---|
| **Filename** | `data/raw/98-401-X2021024_English_CSV_data.csv` |
| **StatCan product** | 98-401-X, Table 2021024 |
| **Description** | Census Profile, 2021 Census of Population — Dissemination Area (DA) level, English CSV |
| **Source** | Statistics Canada Open Data — search product 98-401-X2021024 at www150.statcan.gc.ca |
| **File size** | 197.9 MB |
| **SHA256** | `a82348fed1a043764f1d543a30f79533237a03d82ede4c10452f940f9b24895e` |
| **Verified** | 2026-05-07 |

To re-verify: `python -c "import hashlib; h=hashlib.sha256(); [h.update(c) for c in iter(lambda: open('data/raw/98-401-X2021024_English_CSV_data.csv','rb').read(65536), b'')]; print(h.hexdigest())"`
