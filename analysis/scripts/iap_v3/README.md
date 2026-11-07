# v3 of the assembled 91-district map: line fit and finish (2026-11-05)

Post-registration, unregistered, sensitivity only. See `findings/iap_reconstruction_check/README.md`, section "v3".

Run in order from the repo root with the audit venv (`python -W ignore <step>`). Intermediate files go to `C:/tmp/` as named in each step.

| Step | Reads | Writes | Does |
|---|---|---|---|
| `step1_known_first.py` | v2 gpkg, majority, VAs, pages | `C:/tmp/iap_v3_candidate.gpkg` | Copied districts get official geometry; changed districts lose any overlap with them; clipped to the province |
| `step2_rebuild_coverage.py` | candidate | `C:/tmp/iap_v3_rebuilt.gpkg` | Nodes every boundary, polygonizes, and gives each face to its owner: an official district holding over half of it, else the changed district holding most; gaps and slivers go to the changed neighbour with the longest contact |
| `step3_page_claims.py` | rebuilt, pages, Chestermere page fit | `C:/tmp/iap_v3_claims.gpkg` | Land one page claims and the holder's own page does not, thicker than the calibrated trace error (30.7 m), goes to the claimant. Refused if it holds a VA point |
| `step4_rebuild_coverage.py` | claims | `C:/tmp/iap_v3_final.gpkg` (= `iap_2026_assembled_v3.gpkg`) | Step 2 again |
| `check_finish.py <gpkg>` | any map | stdout | Overlaps, holes, gaps and land outside the province, parts, invalid geometries, VAs moved against v2 |
| `step5_calibrate_traces.py` | final, pages | `C:/tmp/fit_samples.pkl` | Page trace against official line for the copied districts' pages (where the truth is known) |
| `step6_flag_lines.py` | final, pages, samples | `C:/tmp/line_flags_final.csv` | Every line touching a changed district, sampled every 25 m, against the nearest of its two references; flags stretches beyond the bar |
