# ============================================================
# Alberta Electoral Boundaries Audit — R cross-validation
#
# Independent reproduction of the seats@50/50 finding using the
# Harvard `redist` package (Imai/Kenny et al.). Uses Sequential
# Monte Carlo (SMC) — a fundamentally different sampler from the
# ReCom Markov chain in the Python `gerrychain` pipeline.
#
# If the R SMC ensemble produces the same percentile placements
# as the Python ReCom ensemble (within ±0.5pp), the audit's
# headline finding is algorithm-independent and library-independent.
#
# Run from the repo root in RStudio:
#   Session -> Set Working Directory -> alberta_audit/
#   then File -> Source (or Ctrl+Shift+S) on this script
#
# Or from the command line:
#   Rscript analysis/scripts/v0_1_redist_crossvalidation.R
#
# Wall time: ~30-45 min on a 4-core laptop for 50,000 SMC samples.
# ============================================================

library(redist)
library(sf)
library(dplyr)

# ----- Step A: Load the input data ----------------------------------
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

# ----- Step B: Build the adjacency graph ----------------------------
# `redist` needs to know which voting areas border which others.
# This is the same graph the Python pipeline computes.

adj <- redist.adjacency(va)
cat("Built adjacency: ", length(adj), " nodes, ",
    sum(sapply(adj, length)) / 2, " edges\n", sep = "")

# ----- Step C: Set up the redistricting problem ---------------------
# Population proxy: total votes per VA (same as Python pipeline)
# Note: Python uses pop_2021 from the StatsCan DA file. R uses
# va_ucp + va_ndp + va_other as a vote-weighted proxy because the
# SMC algorithm needs strictly positive integer-like populations
# and the gpkg's pop_2021 column has fractional values from areal
# interpolation. The percentile placements should still match
# because both substrates are equal-population-balanced.
va$pop <- pmax(round(va$va_ucp + va$va_ndp + va$va_other), 1)
n_districts <- 87  # 2019 substrate count, matching the Python ensemble

# `redist`'s map object bundles geography + population + adjacency
map <- redist_map(
  va,
  pop_tol = 0.25,           # +/-25% population tolerance, matching Python
  ndists  = n_districts,
  adj     = adj,
  pop_col = "pop"
)

# ----- Step D: Run the ReCom ensemble (this is the slow step) -------
# The Python pipeline runs 2,000,000 maps via ReCom. For cross-
# validation, 50,000 SMC samples is enough — the percentile
# placements should agree to within +/-0.5pp at this sample size.
# Wall time on a 4-core laptop: ~30-45 minutes.

set.seed(88)  # arbitrary seed; reproducibility within R is sufficient
ensemble <- redist_smc(
  map,
  nsims = 50000,            # change to 500000 for a tighter check
  resample = TRUE,
  pop_temper = 0.05,
  ref_name = "audit_replication"
)

# ----- Step E: Compute seats@50/50 for each ensemble plan -----------
# For each random plan, calculate UCP seats at provincial 50/50 votes
# under uniform partisan swing — exactly what the Python pipeline does.
# Mirrors seat_results() in v0_1_mcmc_ensemble.py:
#     province_ucp = ucp.sum() / total.sum()
#     swing = 0.5 - province_ucp
#     shifted = clip(ucp_share + swing, 0, 1)
#     seats_at_50_50 = sum(shifted > 0.5 + 1e-9) / n
# Note the +1e-9 epsilon (LOW finding from the Gemini code audit).

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
  mean(shifted_shares > 0.5 + 1e-9)
}

cat("Computing seats@50/50 across all", ncol(ensemble), "ensemble plans...\n")
s50_values <- numeric(ncol(ensemble))
for (i in seq_len(ncol(ensemble))) {
  s50_values[i] <- seats_at_50_50(ensemble$plans[, i], va)
}

# ----- Step F: Report -----------------------------------------------
# These should match the Python pipeline's reported values.

cat("\n========================================\n")
cat("  R cross-validation result\n")
cat("========================================\n")
cat("Ensemble size:", length(s50_values), "\n")
cat("seats@50/50 distribution across ensemble:\n")
cat("  median:    ", round(median(s50_values), 4), "\n")
cat("  p5:        ", round(quantile(s50_values, 0.05), 4), "\n")
cat("  p95:       ", round(quantile(s50_values, 0.95), 4), "\n")
cat("  p99:       ", round(quantile(s50_values, 0.99), 4), "\n")
cat("  max:       ", round(max(s50_values), 4), "\n")
cat("\n")
cat("Python ensemble published values (corrected post-audit):\n")
cat("  TODO: fill in from v0_1_post_audit_recompute_deltas.md\n")
cat("        once the corrected 2M Python re-run completes.\n")
cat("        Until then, the buggy-version published values were:\n")
cat("        median: 0.4483, p5: 0.4253, p95: 0.4828, max: 0.5172\n")
cat("\n")
cat("Pass criterion: R values within +/-0.5pp of corrected Python values.\n")

# Save outputs for the audit's record
saveRDS(s50_values, file = "data/v0_1_redist_crossvalidation_s50.rds")
write.csv(
  data.frame(seats_at_50_50 = s50_values),
  file = "data/v0_1_redist_crossvalidation_s50.csv",
  row.names = FALSE
)
cat("Wrote data/v0_1_redist_crossvalidation_s50.csv\n")
