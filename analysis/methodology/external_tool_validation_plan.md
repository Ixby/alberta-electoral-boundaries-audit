---
name: External-tool validation plan
description: Step-by-step instructions for cross-validating the Alberta Electoral Boundaries Audit using R (the `redist` package), QGIS (visual polygon inspection), and ArcGIS (publication-grade figure polish). Written for someone who has never used these packages before. Each phase is independent; you can do Phase 1 alone and skip the rest, or do them in sequence.
type: methodology
---

# External-tool validation plan

This document walks through cross-validating the audit using three tools the university has access to. The plan is sequenced from highest-value to optional polish:

| Phase | Tool | What it adds | Time | Cost |
|---|---|---|---|---|
| **1** | **R + `redist` package** | Independent algorithm in a different language reproduces the headline `seats@50/50` finding | 1 evening setup + ~90 min run | Free |
| **2** | **QGIS** *or* **ArcGIS Pro via MRU vLab** | Visual inspection of the v0_8 polygon reconstructions against commission map images | 2 hours setup + 1 afternoon inspection | Free; MRU is an Esri campus, ArcGIS Pro is the supported standard via the vLab |
| **3** | **ArcGIS Pro** for figures | Polished publication-grade figures for journal submission (optional) | 1 hour setup + 1 day work | Free via MRU vLab (Apporto) |

**Note on Maptitude.** Mount Royal University does not have institutional access to Maptitude for Redistricting (Caliper Corporation), confirmed via the MRU software directory. MRU is an Esri-stack campus: the supported GIS tools through the MRU vLab (powered by Apporto) are ArcGIS Pro and ArcGIS Online, plus ENVI, geoScout, and CS Land for adjacent specialties. **Caliper does offer a 14-day free trial of Maptitude for Redistricting**, which is enough time for a focused measurement-cross-validation pass (Phase 2.5 below). The free trial is the practical way to add Maptitude as a validator without acquiring the licence.

You can stop after Phase 1 and the audit gains a meaningful credibility boost. Phase 2 is high-value but requires more domain knowledge of the geography. Phase 3 is only worth doing if you decide to submit the work to an academic journal.

---

## Phase 1 — R `redist` cross-validation

**Goal:** independently reproduce the audit's `seats@50/50` percentile placement using the Harvard `redist` package (Imai, Kenny, et al.), a completely separate codebase from the Python `gerrychain` library the audit currently uses. If both produce the same answer within ±0.5 percentile points, that's the strongest possible validation that the result isn't an artefact of `gerrychain`.

**What you need to know going in:** R is a programming language, similar to Python in concept. RStudio is the standard editor. You write code in the editor, hit a "Run" button, and see results in a console. You don't need to know R programming — you'll copy-paste a single script.

### Step 1.1 — Install R and RStudio (one time, ~10 minutes)

1. Download R from <https://cran.r-project.org/bin/windows/base/> — click the big download link, run the installer, accept defaults
2. Download RStudio Desktop (free version) from <https://posit.co/download/rstudio-desktop/> — run the installer, accept defaults
3. Open RStudio. You'll see a four-pane window. The bottom-left pane is the "Console" — that's where you'll see output. The top-left is empty until you open a script.

### Step 1.2 — Install the required R packages (one time, ~5 minutes)

In RStudio's Console pane (bottom-left), paste this block and press Enter:

```r
install.packages(c("redist", "sf", "dplyr", "ggplot2", "tigris"))
```

A bunch of text will scroll past as packages download and install. Wait until you see the `>` prompt return on a fresh line. If any package fails, RStudio will tell you which — usually it's because of a missing system dependency (Windows usually handles this; Mac sometimes needs Homebrew).

Verify the install worked by typing in the Console:

```r
library(redist)
packageVersion("redist")
```

You should see something like `[1] '4.2.0'` (or whatever the current version is). Anything ≥ 4.0 is fine.

### Step 1.3 — Get the audit's input data into R

The audit's input data lives in the GitHub repository. You'll need three files:

- The 2019 enacted Alberta shapefile: `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`
- The voting-area polygons with 2023 votes: `data/shapefiles/derived/va_polygons_with_2023_votes.gpkg`
- The audit's reconstructed v0_8 minority and majority maps:
  - `data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg`
  - `data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg`

If you cloned the repo with `git lfs pull`, all four are already on your disk. Open RStudio and set the working directory to the repo root using the menu **Session → Set Working Directory → Choose Directory…** and pick the `alberta_audit` folder.

### Step 1.4 — Save the cross-validation script

In RStudio, **File → New File → R Script**. Paste the entire block below into the empty top-left pane and save it as `analysis/scripts/redist_crossvalidation.R`.

```r
# ============================================================
# Alberta Electoral Boundaries Audit — R cross-validation
# Independent reproduction of the seats@50/50 finding using the
# Harvard `redist` package. If this gives the same answer as the
# Python `gerrychain` ensemble, the audit's headline finding is
# algorithm-independent.
# ============================================================

library(redist)
library(sf)
library(dplyr)

# ----- Step A: Load the input data -----
# These are the same input files the Python pipeline uses.

va <- st_read("data/shapefiles/derived/va_polygons_with_2023_votes.gpkg")
cat("Loaded", nrow(va), "voting areas\n")
cat("Column names:", paste(names(va), collapse = ", "), "\n")

# Sanity-check: total votes should be ~932,000 across the province
total_ucp <- sum(va$va_ucp, na.rm = TRUE)
total_ndp <- sum(va$va_ndp, na.rm = TRUE)
cat("Total UCP votes:", total_ucp, "\n")
cat("Total NDP votes:", total_ndp, "\n")
cat("UCP share:", round(total_ucp / (total_ucp + total_ndp) * 100, 2), "%\n")

# ----- Step B: Build the adjacency graph -----
# `redist` needs to know which voting areas border which others.
# This is the same graph the Python pipeline computes.

adj <- redist.adjacency(va)
cat("Built adjacency: ", length(adj), " nodes, ",
    sum(sapply(adj, length)) / 2, " edges\n", sep = "")

# ----- Step C: Set up the redistricting problem -----
# Population proxy: total votes per VA (same as the Python pipeline)
va$pop <- va$va_ucp + va$va_ndp + va$va_other
n_districts <- 87  # 2019 substrate count, matching the Python ensemble

# `redist`'s map object bundles geography + population + adjacency
map <- redist_map(
  va,
  pop_tol = 0.25,           # ±25% population tolerance, matching Python
  ndists  = n_districts,
  adj     = adj,
  pop_col = "pop"
)

# ----- Step D: Run the ReCom ensemble (this is the slow step) -----
# The Python pipeline runs 2,000,000 maps. For cross-validation,
# 50,000 is enough — the percentile placements should agree to
# within ±0.5pp at this sample size.
#
# Wall time on a 4-core laptop: ~30-45 minutes for 50,000 maps.

set.seed(88)  # same seed used by the Python pipeline's authoritative run
ensemble <- redist_smc(
  map,
  nsims = 50000,            # change to 500000 for a tighter check
  resample = TRUE,
  pop_temper = 0.05,
  ref_name = "audit_replication"
)

# ----- Step E: Compute seats@50/50 for each ensemble plan -----
# For each random plan, calculate UCP seats at provincial 50/50 votes
# under uniform partisan swing — exactly what the Python pipeline does.

ucp_share_per_district <- function(plan_assignment, va_data) {
  ucp <- tapply(va_data$va_ucp, plan_assignment, sum)
  ndp <- tapply(va_data$va_ndp, plan_assignment, sum)
  ucp / (ucp + ndp)
}

seats_at_50_50 <- function(plan_assignment, va_data) {
  shares <- ucp_share_per_district(plan_assignment, va_data)
  global_share <- sum(va_data$va_ucp) / sum(va_data$va_ucp + va_data$va_ndp)
  shift <- 0.5 - global_share
  shifted_shares <- pmin(pmax(shares + shift, 0), 1)
  mean(shifted_shares > 0.5)
}

cat("Computing seats@50/50 across all", ncol(ensemble), "ensemble plans...\n")
s50_values <- numeric(ncol(ensemble))
for (i in seq_len(ncol(ensemble))) {
  s50_values[i] <- seats_at_50_50(ensemble$plans[, i], va)
}

# ----- Step F: Report -----
# These should match the Python pipeline's reported values.

cat("\n========================================\n")
cat("  R cross-validation result\n")
cat("========================================\n")
cat("Ensemble size:", length(s50_values), "\n")
cat("seats@50/50 distribution across ensemble:\n")
cat("  median:    ", round(median(s50_values), 4), "\n")
cat("  p5:        ", round(quantile(s50_values, 0.05), 4), "\n")
cat("  p95:       ", round(quantile(s50_values, 0.95), 4), "\n")
cat("  max:       ", round(max(s50_values), 4), "\n")
cat("\n")
cat("Python ensemble published values (for comparison):\n")
cat("  median: 0.4483, p5: 0.4253, p95: 0.4828, max: 0.5172\n")
cat("\n")
cat("If the R values match within ±0.5 percentile points, the\n")
cat("audit's headline finding is algorithm-independent.\n")

# Save outputs for the audit's record
saveRDS(s50_values, file = "data/smc_crossvalidation_s50.rds")
write.csv(
  data.frame(seats_at_50_50 = s50_values),
  file = "data/redist_crossvalidation_s50.csv",
  row.names = FALSE
)
cat("Wrote data/redist_crossvalidation_s50.csv\n")
```

### Step 1.5 — Run the script

Click the **Source** button at the top of the script editor (or press Ctrl+Shift+S). The script will start running. You'll see output appear in the Console pane below. Wait until the script finishes — about 30-45 minutes for 50,000 maps on a typical laptop.

### Step 1.6 — Interpret the result

The script prints the R-computed median, p5, p95, and max for `seats@50/50`, followed by the Python-published values. Compare them line by line.

**Pass criterion:** all four R values within ±0.005 (0.5 percentage points) of the published Python values.

| Metric | Python published | R reproduction | Pass? |
|---|---|---|---|
| median | 0.4483 | (your R value) | ✓ if within 0.4433-0.4533 |
| p5 | 0.4253 | (your R value) | ✓ if within 0.4203-0.4303 |
| p95 | 0.4828 | (your R value) | ✓ if within 0.4778-0.4878 |
| max | 0.5172 | (your R value) | ✓ if within 0.5122-0.5222 |

If all four pass, the validation is successful. Open a GitHub issue at `https://github.com/Ixby/alberta-electoral-boundaries-audit/issues` titled "R cross-validation passed" with your R values copy-pasted, and reference the date and your hardware. That single issue is the public evidence of independent algorithm validation.

If any value fails by more than 0.5pp, **stop** and post the discrepancy as an issue without claiming the validation passed. The most likely cause is a small methodology difference between the two libraries' default settings (e.g., `redist_smc` uses Sequential Monte Carlo by default; `redist_mergesplit` is closer to gerrychain's ReCom).

---

## Phase 2 — QGIS visual inspection

**Goal:** open the audit's reconstructed v0_8 polygons in a GIS viewer alongside the commission's published map images and visually confirm the polygons match the boundaries shown in the images. Catches the kind of error that code-level checks can't detect.

### Step 2.1 — Install QGIS (one time, ~10 minutes)

1. Download QGIS Long-Term Release from <https://qgis.org/en/site/forusers/download.html> — click the Windows installer, run it, accept defaults
2. Open QGIS (it's called "QGIS Desktop"). You'll see a complex window with map canvas in the centre, layer list on the left, and a toolbar.

### Step 2.2 — Load the audit's polygons

In QGIS:

1. **Layer → Add Layer → Add Vector Layer…**
2. Source type: File. Browse to `data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg`. Click **Add**, then **Close**.
3. Repeat for `v0_8_full_refined_majority_2026_eds.gpkg`.
4. Both maps now appear in the Layers pane on the left.
5. Right-click the minority layer → **Properties → Symbology**. Change "Single Symbol" to "Categorized" and choose `name_2026` as the category column. Click **Classify**, then **OK**. Each district gets a different colour.

### Step 2.3 — Load the commission's published map images as overlays

The commission's published maps are in the audit's `maps/hires/` folder as 600-DPI PNG/JPG files.

1. **Layer → Add Layer → Add Raster Layer…**
2. Browse to `maps/hires/minority_alberta_overview.jpg` (or any of the others)
3. The image loads but with no spatial reference — it appears at coordinates (0,0).
4. **Right-click the layer → Georeferencer**. (Or: Raster menu → Georeferencer → open the image.) The georeferencer window opens.
5. Add 4-6 ground-control points where the image's known landmarks (city centres, prominent intersections) match real-world coordinates. Click a point on the image, then click the corresponding point on the QGIS map canvas.
6. Set transformation type to **Polynomial 2** (good for low-distortion maps). Click **Start Georeferencing**. Save the georeferenced image as a GeoTIFF.

This is the slowest part — about 20-30 minutes per commission image. For the visual inspection workflow, you only need to georeference the **Calgary detail map** and the **Edmonton detail map** at minimum. The province overview is too low-resolution to verify boundaries.

### Step 2.4 — Visual inspection workflow

For each of the audit's six contested EDs, do this:

| ED to inspect | What to check |
|---|---|
| Calgary-Airdrie | Does the v0_8 polygon match the commission's published Airdrie boundary? |
| Calgary-Nolan-Hill-Cochrane | Does the lasso shape connecting Cochrane to NW Calgary match the published image? |
| Rocky Mountain House-Banff Park | How far into Banff National Park does the published boundary extend? Does v0_8 match? |
| Olds-Three-Hills-Didsbury | Does the North-Airdrie reach in v0_8 match the published boundary? |
| Lethbridge-Taber-Warner | Does the Lethbridge city split in v0_8 match the published boundary? |
| Edmonton-Spruce-Grove | Does the Spruce-Grove inclusion in v0_8 match the published image? |

For each ED:

1. In QGIS, **Layer panel → click the eye icon** to show only the relevant minority polygon and the commission overlay
2. Zoom in to the ED's boundary at city/town scale
3. **Visually trace the published boundary** with the cursor; compare to the v0_8 polygon outline
4. **Document findings** in a per-ED entry: "Boundary aligns within visual tolerance" / "Boundary deviates 200m at northwest edge" / "Boundary differs significantly — needs investigation"

Save the findings as `analysis/methodology/v0_1_qgis_visual_inspection_findings.md`. Each ED gets a short paragraph; include screenshots cropped from QGIS for any deviation.

### Step 2.5 — Pass criterion

For the audit to be considered "visually validated":

- 4 of 6 EDs must align within visual tolerance (~500 m)
- For any ED that deviates significantly, the deviation is documented in `data/INTEGRITY_STATUS.md` and the audit's findings citing that ED carry the deviation as a caveat

If 5 or 6 EDs align within tolerance, the visual inspection is a clean pass. If only 4 align, document the two that don't. If 3 or fewer align, **stop** and investigate the geometry pipeline — there's a systematic bug.

---

## Phase 2.5 — Maptitude measurement cross-validation (free-trial scope)

**Goal:** independently re-measure the audit's three real maps (2019 enacted, 2026 majority, 2026 minority) in Maptitude for Redistricting — the industry-standard commercial tool — and confirm the measurements match the audit's published values. This cross-validates the **measurement layer** (efficiency gap, compactness, anchoring percentages, voter-equality scores) using a completely different toolchain. It does NOT cross-validate the simulation ensemble (Maptitude doesn't generate ensembles); R `redist` is the right tool for that.

**Why this is worth doing if you have access:** Maptitude is what US redistricting commissions actually use. A hostile expert reviewing the audit can no longer say "you only used academic-research tools" if the headline measurements come out the same in Maptitude as in the audit's Python pipeline.

**Scope (sized to fit a 14-day free trial):** measurement re-run only. Do NOT use the trial to build counter-maps, run plan-evaluation suites, or explore Maptitude's interactive drawing features. The narrow scope keeps the work to one focused 4-hour session.

### Step 2.5.1 — Get the free trial

1. Visit <https://www.caliper.com/maptovu.htm> and click "Try Maptitude for Redistricting Free."
2. Fill out the request form (Caliper requires a brief description of intended use — "academic cross-validation of an electoral-audit project, scope: measurement of three pre-existing maps" is the honest description and what they expect).
3. Wait for the download link (typically arrives within 1 business day).
4. Install on Windows. Plan ~30 minutes for the install + initial setup.

### Step 2.5.2 — Load the audit's three maps

In Maptitude, **File → Open** the GeoPackage files:

- 2019 enacted: `data/shapefiles/reference/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp`
- 2026 majority: `data/shapefiles/derived/v0_8_full_refined_majority_2026_eds.gpkg`
- 2026 minority: `data/shapefiles/derived/v0_8_full_refined_minority_2026_eds.gpkg`

Maptitude will treat each one as a separate redistricting plan. Set the population layer to the StatsCan 2021 DA file (`data/shapefiles/reference/alberta_2021_das.gpkg`).

### Step 2.5.3 — Run Maptitude's built-in measurement tools

For each plan:

1. **Population deviation report:** Maptitude → Districting → Population Statistics. Compare to the audit's published values (majority within ±7%; minority within ±12.7%).
2. **Compactness report:** Maptitude → Districting → Compactness Measures. Maptitude reports Polsby-Popper, Reock, Schwartzberg by default. Compare per-district scores against the audit's `analysis/scripts/v0_1_compactness.py` outputs (run that script first if you don't already have the values).
3. **Partisan-bias report:** Load 2023 vote data via Maptitude's Election Data import. Run the built-in efficiency-gap and seats-votes-curve reports. Compare to the audit's published efficiency gap (majority +6.4%, minority +9.2%).

### Step 2.5.4 — Pass criterion + write-up

For each metric on each map, the Maptitude value should be within ±0.5pp of the audit's published value. Document the comparison as `analysis/methodology/v0_1_maptitude_cross_validation.md` with:

- Maptitude version and trial period dates
- Per-metric, per-map comparison table
- Any deviation > 0.5pp flagged with a maintainer-investigation note
- Screenshots of the Maptitude reports for archival

If everything matches: the measurement layer is independently validated by the industry-standard tool. Open a GitHub issue at `https://github.com/Ixby/alberta-electoral-boundaries-audit/issues` with the comparison table.

If anything materially diverges: the most likely cause is a methodology difference (e.g., Maptitude's default efficiency gap may use the Stephanopoulos-McGhee 2014 formula vs. the modified Cover-McGhee 2019 update). Document the difference; investigate; do not silently update the audit.

---

## Phase 3 — ArcGIS publication-grade figures (optional)

**Goal:** if and when the audit is submitted to an academic journal (target: *Canadian Journal of Political Science* or *Election Law Journal*), produce the map figures using ArcGIS rather than matplotlib. Journal referees respond better to ArcGIS-quality cartography. This is purely cosmetic — the underlying data is identical.

### Step 3.1 — Get ArcGIS access through MRU

1. Visit Mount Royal's IT Services page on software access. ArcGIS Pro is the current desktop product; ArcGIS Online is the web version.
2. Faculty or student licence depending on your status. As a student you typically get an annual ArcGIS Online + ArcGIS Pro Desktop bundle through the university.
3. Install ArcGIS Pro (Windows-only). The installer is large (~3 GB). Allow ~30 minutes for download + install.

### Step 3.2 — Reproduce the verdict-quadrant figure in ArcGIS

The verdict quadrant doesn't really need ArcGIS (it's a scatter plot, matplotlib handles it fine). The figures that benefit from ArcGIS treatment are the **map figures** for a journal version.

1. **Add Data → file** → load the v0_8 polygons
2. **Symbology → Unique Values** by `name_2026`
3. Apply a journal-grade colour palette (Cynthia Brewer's ColorBrewer 2.0 palettes are standard; ArcGIS has them built in)
4. Add a north arrow, scale bar, legend, and title
5. **Export Map** as 300-DPI PNG or PDF for journal submission

ArcGIS Pro's "Layout" view is what produces publication figures. Tutorials at <https://learn.arcgis.com/en/projects/get-started-with-arcgis-pro/> walk through this for total beginners.

### Step 3.3 — Optional: cross-validation via ArcGIS spatial-join

ArcGIS has a built-in "Spatial Join" tool that can do voting-area-centroid → ED-polygon attribution as an independent check on the audit's Python `geopandas.sjoin` output.

1. **Geoprocessing → Spatial Join**
2. Target features: the v0_8 ED polygons
3. Join features: voting-area centroids
4. Join operation: One-to-one, sum the `va_ucp` and `va_ndp` fields
5. Output a new feature class with per-ED vote totals
6. Export as CSV and `diff` against the audit's Python output

This is a purely cosmetic-credibility addition — the Python `sjoin` is correct, but having the same numbers come out of ArcGIS's internal tool is a third independent confirmation.

---

## What to do if any phase fails

Each phase is designed to either pass with high confidence or fail in a documented way. If something fails:

1. **Don't claim the validation passed.** The honest reporting is: "Phase X attempted; results did not match published values within tolerance; investigation pending."
2. **Open a GitHub issue** at `https://github.com/Ixby/alberta-electoral-boundaries-audit/issues` documenting the discrepancy with your hardware, software versions, and the exact values you got
3. **Tag the issue with `validation-failure`** so future readers can find it
4. **Update the public report's "Honest gaps" section** in `report_public.md` to reflect the failed validation (the section currently lists "external replication" as the biggest gap; if a replication attempt produces a discrepancy, that's a different and more important gap)

A failed validation is more valuable than no validation. Both increase the audit's credibility — successful validation by confirming the result, failed validation by surfacing problems honestly.

---

## Suggested sequencing for first-time users

If you've never used any of these tools, do them in this order:

| Week | Task | Hours |
|---|---|---|
| 1 | Install R + RStudio + redist; run a `library(redist)` smoke test | 0.5 |
| 1 | Skim the redist documentation: <https://alarm-redist.org/redist/> | 0.5 |
| 1 | Run the Phase 1 script overnight | 0.5 (active) + ~45 min (passive) |
| 1 | Compare Phase 1 results to Python; open GitHub issue | 0.5 |
| 2 | Install QGIS; complete Module 1 of the QGIS Training Manual | 2 |
| 2 | Load audit polygons + georeference one commission image | 1.5 |
| 2 | Visual inspection of 6 contested EDs; write findings | 4 |
| 3 (optional, journal-only) | Install ArcGIS Pro; complete the "Get Started" tutorial | 2 |
| 3 (optional) | Reproduce the verdict-quadrant or one map figure in ArcGIS | 4 |

A motivated first-time user can complete Phase 1 in a single evening (3-4 hours including reading) and Phase 2 over a weekend.
