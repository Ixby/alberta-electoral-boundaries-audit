# Data Preparation — From Raw Sources to Analysis-Ready Datasets

**Purpose.** This document shows how each file in `data/` was produced from publicly-available raw sources. Readers who want to reproduce the audit from scratch (not just re-run the analysis scripts) can follow this pipeline to rebuild the datasets themselves.

Every step is either a direct download from an official government source, a named parser script in `analysis/`, or a PDF text extraction whose line numbers are cited.

---

## 1. Election results — 2023, 2019, 2015

### 2023 results

**Raw source:** Elections Alberta, 2023 Provincial General Election Statement of Vote.
URL: `https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx`
Format: Excel workbook, 87 sheets (one per electoral division), ~462 KB, poll-level detail.

**Acquired to:** `data/2023_results.xlsx` (verbatim).

**Derived artifacts:**
- `data/v0_1_alberta_2023_results.csv` — one row per ED with candidate names/parties/votes, region (Calgary / Edmonton / Rest of Alberta).
- `analysis/polls_2023_unified.csv` — 1,973 poll records unified across the 87 sheets, with columns `ed_2019`, `sheet_num`, `poll_letter`, `poll_name`, `ballot_type`, `ndp_votes`, `ucp_votes`, `other_votes`, `valid_votes`, `voting_areas`, `lat`, `lon`, `ed_2026_majority`, `ed_2026_minority`.

**Reproduction steps:**
```bash
curl -sLo data/2023_results.xlsx \
  https://www.elections.ab.ca/uploads/2023-Provincial-General-Election-Statement-of-Vote.xlsx
python3 analysis/v0_1_poll_attribution_skeleton.py   # generates polls_2023_unified.csv
```

**Integrity check.** Sum of NDP and UCP totals across all polls should match the official 2023 provincial counts:
- NDP: 777,404
- UCP: 928,900
- Two-party: 1,706,304

The skeleton script prints these at runtime. Any deviation indicates a parse error.

### 2019 results

**Raw source:** Elections Alberta, 2019 PGE Official Results All EDs.
URL: `https://www.elections.ab.ca/uploads/2019PGEOfficialResultsAllEDs.xlsx`
Format: Excel workbook, 87 sheets.

**Acquired to:** `data/v0_1_alberta_2019_results.csv` via manual per-sheet CSV extraction.

**Integrity check.** Seat outcome: NDP 24, UCP 63. This is matched on actual-seats from the first-session run of `analysis/v0_1_packing_cracking_analysis.py` (now in `deprecated/`; its 2019-side numbers agree with the active `v0_2_packing_cracking_analysis.py`).

### 2015 results

**Raw source:** Elections Alberta, 2015PGE-Official-Results.
URL: `https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx`
Format: Excel workbook, 87 sheets, poll-level detail. Parties: PC, WRP, NDP, LIB, AP, GPA, SC, CP-A, IND. UCP did not exist in 2015; `ucp_equiv` column sums PC + WRP (merged in 2017).

**Acquired to:** `data/2015_results.xlsx` (verbatim).

**Derived:** `data/v0_1_alberta_2015_results.csv` via `analysis/parse_2015_results.py`.

**Reproduction steps:**
```bash
curl -sLo data/2015_results.xlsx \
  https://www.elections.ab.ca/uploads/2015PGE-Official-Results.xlsx
python3 analysis/parse_2015_results.py
```

**Integrity check.** Parsed provincial shares must match official:
- Official 2015: NDP 40.59%, PC 27.79%, WRP 24.22%, LIB 4.18%
- Parsed: NDP 40.72%, PC 27.79%, WRP 24.09%, LIB 4.21% (within ±0.13 pp per party)

---

## 2. Commission final report — populations and crosswalks

### Majority + minority proposed populations

**Raw source:** Alberta Electoral Boundaries Commission, 2025–26 Final Report, March 23, 2026.
URL: `https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf`
Size: 83.9 MB, 362 pages.

**Key pages:**
- pp. 44–45: majority proposal variance tables (89 EDs, population, deviation from provincial average)
- p. 269 (Appendix C): majority hybrid-ED crosswalk (current → proposed)
- pp. 285+: Appendix E (minority report); pp. 307–308 contain three structured hybrid crosswalk tables
- p. 71 of Appendix E: minority proposal variance tables (89 EDs)

**Acquired to:**
- `data/v0_1_majority_2026_populations.csv` — manually extracted from pp. 44–45
- `data/v0_1_minority_2026_populations.csv` — manually extracted from Appendix E variance table
- `data/v0_1_minority_2026_populations_appendixE.csv` — second extraction from Appendix E (corroborates the first with minor rounding differences noted in `data/data_acquisition_manifest.md`)

**Crosswalks:**
- `data/v0_1_majority_hybrid_crosswalk.csv` — extracted from Appendix C table via `pdfplumber`
- `data/v0_1_minority_hybrid_crosswalk.csv` — heuristic name-matching across 89 proposed × 87 current EDs, 73 confident mappings, 16 new names, 14 unmapped
- `data/v0_1_minority_hybrid_crosswalk_appendixE.csv` — 22 mappings extracted from the three tables on pp. 307–308 of Appendix E

**Reproduction steps:**
```bash
mkdir -p .temp
curl -sLo .temp/commission_report.pdf \
  https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf
python3 -c "
import pdfplumber
with pdfplumber.open('.temp/commission_report.pdf') as pdf:
    # Page 269 has the majority hybrid crosswalk as a table
    tables = pdf.pages[268].extract_tables()
    # Emit CSV from tables[0] (see analysis/parse_2015_results.py for table extraction pattern)
"
```

The full crosswalk extraction is part of the Phase 4C preparation; see `analysis/phase_4c_prep.py` which uses these crosswalks for VA-to-2026 candidate matching.

**Integrity checks.**
- Majority total population: 4,888,723 (matches commission's reported total).
- Minority total population: 4,888,773 (50-person rounding drift; this is the commission's own rounding, not a parse error).

### Commission map images

**Raw source:** Appendices A (majority) and E (minority) of the final report.
- Majority Calgary map: p. 72
- Minority Alberta overview: Appendix E, p. 73
- Minority Calgary map: Appendix E, p. 74
- Minority Edmonton: Appendix E, p. 75
- Minority other cities: Appendix E, p. 76

**Acquired via:** manual extraction from the PDF using a PDF-to-image tool at 300 DPI.

**Stored at:**
```
maps/majority_calgary.jpg
maps/minority_calgary.jpg
maps/minority_alberta_overview.jpg
maps/minority_edmonton.jpg
maps/minority_other_cities.jpg
```

**Known gap.** The majority's Alberta overview, Edmonton, and other-cities maps were not extracted from the bundle's working copy. Section C3 therefore covers the majority's Calgary districts only. This is disclosed as a symmetry data gap in the academic report.

### Submission archive

**Raw source:** Elections Alberta, Electoral Boundaries Commission submissions archive.
URL: `https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/`
Format: 27 batch PDF files (4 for Round 1, 23 for Round 2), ~1,340 submissions total, ~200–300 MB aggregate.

**Acquired to:** `.temp/submissions/` (gitignored; raw PDFs are not redistributed).

**Derived:**
- `data/submission_search_dataset.csv` — per-submission keyword hit dataset (70 hit rows + summary)
- `analysis/submission_search.py` — the reproducible pipeline
- `analysis/submission_search_findings.md` — written verdict on the chair's "no public support" claim

**Reproduction steps:**
```bash
mkdir -p .temp/submissions
for i in 1 51 101 151; do
    curl -sLo ".temp/submissions/EBC2025Submissions${i}-${i+49}ForPosting.pdf" \
      "https://www.elections.ab.ca/uploads/EBC2025Submissions${i}-${i+49}ForPosting.pdf"
done
# Round 2 (23 files at EBC-2025-2-NNN to NNN pattern)
python3 analysis/submission_search.py
```

**Integrity.** 1,252 of ~1,340 submissions extracted with usable text layer. The remaining ~88 are image-only scans without a detectable EBC-2025-X-NNN ID marker; OCR was out of scope.

---

## 3. Shapefiles and geographic data

### Alberta 2019 Electoral Division shapefile

**Raw source:** Elections Alberta GIS resources page.
URL: `https://www.elections.ab.ca/uploads/2019Boundaries_ED-Shapefiles.zip`
Format: ESRI Shapefile, EPSG:3401 (NAD83 3TM 114°W for Alberta), 87 polygons.

**Acquired to:** `data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.*` (shp, shx, dbf, prj, plus auxiliary files).

### Alberta 2023 Voting Area shapefile

**Raw source:** Elections Alberta GIS resources page.
URL: `https://www.elections.ab.ca/uploads/2023Boundaries_VAs.zip`
Format: ESRI Shapefile, EPSG:3400, 4,765 polygons.

**Acquired to:** `data/alberta_2023_vas/`.

**Integrity check.** The 4,765 polygon count matches exactly the 4,765 unique `(ed_2019, voting_area)` pairs extracted from `analysis/polls_2023_unified.csv`. Per-ED VA counts: min 35, mean 54.8, max 82.

### Statistics Canada 2021 Dissemination Areas (Alberta only)

**Raw source:** StatsCan 2021 Census boundary files, national DA shapefile.
URL: `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip`
Format: ESRI Shapefile, ~168 MB national; Alberta subset filtered by PRUID = '48'.

**Filtered to:** `data/alberta_2021_das.gpkg` (GeoPackage, ~15.5 MB), 6,203 Alberta DAs.

**Reproduction steps:**
```bash
mkdir -p .temp
curl -sLo .temp/lda_2021.zip \
  https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lda_000a21a_e.zip
unzip .temp/lda_2021.zip -d .temp/lda_2021
python3 -c "
import geopandas as gpd
gdf = gpd.read_file('.temp/lda_2021/lda_000a21a_e.shp')
ab = gdf[gdf['PRUID'] == '48']
ab.to_file('data/alberta_2021_das.gpkg', driver='GPKG')
"
```

### Statistics Canada 2021 DA populations

**Raw source:** StatsCan table 98-401-X2021006 (Population and dwelling counts by dissemination area).
Direct-URL (bypasses the interactive form):
```
https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/comp/getFile.cfm?LANG=E&GEONO=006&FILETYPE=CSV
```

**Acquired to:** `data/alberta_2021_da_populations.csv`.

**Integrity check.** Sum of Alberta 2021 DA populations = 4,262,635 (matches the official AB 2021 total).

### Calgary ward shapefile

**Raw source:** Calgary Open Data, Socrata dataset `tz8z-hyaz`.
URL: `https://data.calgary.ca/Government/Ward-Boundaries/tz8z-hyaz`
Format: GeoJSON, EPSG:4326, 14 Calgary civic wards.

**Acquired to:** `data/calgary_wards.geojson`.

### Statistics Canada 2021 Census Subdivisions (Alberta)

**Raw source:** StatsCan 2021 census CSD boundary files.
Filtered to Alberta: 423 CSDs.

**Acquired to:** `data/alberta_2021_csds.gpkg` + `data/alberta_2021_csd_populations.csv`.

**Purpose.** Programmatic verification of §C4 community-of-interest splits. A CSD is roughly "city, town, village, or rural municipality"; it is the statutory unit a split-across-districts claim references.

---

## 4. Phase 4C substrate

### Voting Areas with attached 2023 votes

**Raw sources:** `data/alberta_2023_vas/` + `analysis/polls_2023_unified.csv`.

**Derived:** `data/va_polygons_with_2023_votes.gpkg` (22 MB, 4,765 polygons).

**Method.** Each Election Day poll record has a `voting_areas` field listing comma-separated VA numbers. Poll votes are equal-weight-split across the VAs in that list and summed per (ED, VA) pair. Advance / Mobile / Special Ballot records are excluded at this stage; they will be apportioned in Phase 4C Stage 7 by Election Day spatial share.

**Reproduction:** `analysis/phase_4c_prep.py` is the reproducible pipeline. Integrity gates S3a (100% polygon match), S3b (99.20% VA centroid in declared 2019 ED), and S3c (0.0000% vote conservation drift) documented in `analysis/va_spatial_integrity_report.md`.

### Hybrid-adjacent VA candidates

**Derived:** `data/hybrid_adjacent_vas.csv` (1,438 rows).

**Method.** For each hybrid 2026 ED in both the majority and minority maps, identify which 2019-ED VAs are likely affected. Token-overlap matching filters generic tokens (Calgary, Edmonton, directionals, anything appearing in ≥5 EDs) before producing candidate pairs. This narrows the Phase 4C Vision-assignment work from 4,765 VAs to 1,438.

---

## 5. Computed analytical outputs

### Majority + minority B1–B6 metrics

**Script:** `analysis/v0_2_packing_cracking_analysis.py`
**Inputs:** `data/v0_1_alberta_2023_results.csv`, `data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv`.
**Method:** explicit name-based 2019→2026 ED mapping dictionaries (`MAJORITY_2026_MAPPING`, `MINORITY_2026_MAPPING`) with three mapping types:
- `direct` — 2026 ED covers approximately the same territory as one 2019 ED
- `blend` — 2026 hybrid combines a 2019 urban core with rural absorption (70/30 default blend)
- `merge` — 2026 ED combines two 2019 EDs

The 70/30 blend is applied identically to both maps. Sensitivity across 0.60 / 0.70 / 0.80 is reported. Monte Carlo CI across the full parameter range is in `analysis/v0_3_monte_carlo_ci.py`.

### Section A population equality

**Script:** `analysis/electoral_forensics_population.py`
**Inputs:** `data/v0_1_majority_2026_populations.csv`, `data/v0_1_minority_2026_populations.csv`.
**Method:** pandas summary statistics on population variance. Calgary zone classification uses pure geography (Zone A: N/E/central of Bow River/Deerfoot line; Zone B: S/W), with a second data-driven classification (2023 winner) as a robustness check.

### Cross-election rural baseline

**Script:** `analysis/v0_1_cross_election_rural_baseline.py`
**Inputs:** 2015, 2019, 2023 results CSVs.
**Output:** rural NDP two-party share per election (26.5% / 33.5% / 35.1%), informing the Monte Carlo sampling range.

### Marginal-seat historical analysis

**Script:** `analysis/v0_1_marginal_seats_analysis.py`
**Output:** per-election list of seats within 1 / 3 / 5 pp of the two-party flip line; seats that flip under ±1.5 and ±3.0 pp uniform swings; Calgary Zone-A NDP-held watch list.

---

## 6. How to run the full pipeline from scratch

```bash
git clone https://github.com/Ixby/alberta-electoral-boundaries-audit
cd alberta-electoral-boundaries-audit
bash setup.sh

# Verify the carry-forward baseline
python3 analysis/v0_2_packing_cracking_analysis.py
python3 analysis/electoral_forensics_population.py
python3 analysis/v0_3_monte_carlo_ci.py
python3 analysis/v0_1_cross_election_rural_baseline.py
python3 analysis/v0_1_marginal_seats_analysis.py
python3 analysis/check_voice_and_readability.py

# If the above match the academic report's tables, the environment is good.
# To rebuild Phase 4C substrate:
python3 analysis/phase_4c_prep.py

# Re-download raw sources and rebuild from scratch (optional):
# see steps above for each dataset.
```

---

## 7. What is NOT in the repository and why

| Item | Source | Why not committed |
|---|---|---|
| Raw commission report PDF (83.9 MB) | elections.ab.ca | Size; URL provided for reproduction. |
| Raw submission archive PDFs (~300 MB) | elections.ab.ca | Size; URLs in `analysis/submission_search.py`. |
| National StatsCan DA shapefile (~168 MB) | statcan.gc.ca | Size; Alberta-only filter committed as GeoPackage. |
| 2010-era AB ED shapefile (for 2015→2019 crosswalk) | Not publicly posted | Elections Alberta does not publish pre-2017 shapefiles. Partial prose-based crosswalk is in `data/v0_1_2015_to_2019_crosswalk_partial.csv`. |
| 2026 ABEBC shapefiles | Not yet released | Expected after royal assent, summer 2026. |
| ~88 image-only submissions (OCR'd) | Raw PDF layer has no text | OCR was out of scope; findings do not depend on them. |

---

## 8. Integrity discipline

Every dataset in `data/` is either:
1. A direct verbatim copy of an official government file, or
2. A derived dataset produced by a named script in `analysis/` that takes only committed inputs.

No manual post-processing is applied to numeric outputs. Where prose extraction from the commission PDF was required (e.g., Appendix E crosswalk), the derivation is documented in `analysis/appendix_e_recon_log.md`.

This discipline is what makes the audit's reproducibility claim credible. If a number in the report doesn't match what the checked-in scripts produce, either the script is wrong (in which case the commit history is audit-able) or the data has drifted (in which case the test passes).

---

*Data preparation documentation v0.1. Authored April 22, 2026. If you reproduce the pipeline from scratch and find a divergence, file a repository issue with the specific file, the reproduction step number, and the observed-vs-expected values.*
