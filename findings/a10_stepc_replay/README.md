# Step C replay through run_stepc.py (2026-11-05)

A check of the tooling, not a new result. `analysis/scripts/run_stepc.py` was run on the same input as the provisional Step C (`findings/a10_stepb_run/districts_real_map.gpkg`, `--name-col district`, `--snap-dir C:/tmp/a10reg/fixed`), ingesting to a separate path so the committed scoring copy was not touched. That ingested copy was deleted afterwards; its bytes differ from the committed copy's (file metadata), and every score below matches.

**Pre-check.** `check_changed_reproduced.py` failed on Edmonton-Meadows (Step A: changed, stated −3,562; the reconstruction holds exactly the majority's voting areas) and the runner stopped, as designed. The failure was not acknowledged. The replay continued with `--from assignment` because its purpose is to compare against a run already made; the failure stands in `check_changed_reproduced.json`.

**Comparison with `findings/a10_stepc/`** (timestamps and file paths ignored):

| Output | Result |
|---|---|
| partisan lane (`iap_2026_assembled_phase4c.json`, `joint_outlier.json`) | identical |
| structural lane, verdict, X1 | identical |
| size-matched (`size_matched.json`) | identical |
| qsgy8 scorecard | identical |
| cut-VA sensitivity (corrected script) | identical |
| voting areas cut, marked | identical |
| rules check | one value differs: Rocky Mountain House-Sundre on the overlay, −31.4% → −32.5% |

The one difference is VA 875 (498 people on the overlay). Step C's rules check used the registered reconstruction's assignment, which puts it in Rocky Mountain House-Sundre; the runner uses one representative-point assignment for every step, which puts it in Lacombe-Sylvan Lake, as the partisan and structural steps already did. The stated-population figure (−41.3%) and every band are unchanged.

Step 7 (R1/R2) is not part of the runner (detached, hours); its fixed scorer was checked separately and reproduces Step C's `scores.csv` and `calibration.json` byte for byte (branch `a8-territory-null`, commit `569250cd`).

**Hashes in `manifest.json`.** The manifest was written on Windows. For some text files its SHA-256 is of the file with CRLF line endings, while the repository stores LF, so those hashes do not match on Linux until the file is converted to CRLF; every one of them then reproduces against the files as they stood when the replay ran (the two scripts it hashes, `joint_outlier_score_canonical.py` and `run_structural_battery.py`, have been edited since). The manifest also hashes the replay's ingested copy, `data/shapefiles/iap_assembled_replay/iap_2026_assembled.gpkg`, which was deleted after the run and is not in the repository.
