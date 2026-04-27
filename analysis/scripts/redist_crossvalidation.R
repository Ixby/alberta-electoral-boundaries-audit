# Version: 0.1 series  (last updated 2026-04-26)

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

# Add the user library path on Windows so the redist/sf/dplyr we installed
# without admin elevation are visible. Harmless on other platforms (the
# resulting path either exists or is silently ignored).
user_lib <- file.path(Sys.getenv("USERPROFILE"), "R", "win-library", "4.6")
if (dir.exists(user_lib)) {
  .libPaths(c(user_lib, .libPaths()))
}

library(redist)
library(redistmetrics)
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

# Note: Python uses pop_2021 from the StatsCan DA file. R previously used
# a vote-weighted proxy but now correctly uses rounded pop_2021 to properly
# validate population-balanced maps rather than vote-balanced maps,
# resolving Bug E from the code audit.
# Load population from the Python-generated cache
pop_cache <- read.csv("data/va_pop_from_das.csv")
va$pop_2021 <- pop_cache$pop_2021[match(seq_len(nrow(va)) - 1, pop_cache$va_row_idx)]
va$pop <- pmax(round(va$pop_2021), 1)
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
# Notes on parameter choices:
# - nsims = 5000: 10k previously collapsed to 3 unique plans during
#   resampling at the late SMC iterations because of low resampling
#   efficiency. 5k gives the particle filter more headroom; if that
#   still collapses we drop pop_temper and/or relax pop_tol.
# - resample = FALSE: returns the un-resampled particle population,
#   which avoids the variance-of-weights collapse that crashed the
#   prior run. Each plan carries an importance weight; we use the
#   weights when computing percentiles below.
# - pop_temper = 0: tempering was the warning's primary suspect; turn
#   it off to keep the importance weights bounded.
ensemble <- redist_smc(
  map,
  nsims = 5000,
  resample = FALSE,
  pop_temper = 0,
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

# `redist_plans` objects expose their assignment matrix via as.matrix().
# Columns are plans, rows are units (one row per VA). Importance weights
# (when resample = FALSE) are accessible via attr(ensemble, "wgt").
plan_matrix <- as.matrix(ensemble)
n_plans <- ncol(plan_matrix)
cat("Computing seats@50/50 across all", n_plans, "ensemble plans...\n")
s50_values <- numeric(n_plans)
for (i in seq_len(n_plans)) {
  s50_values[i] <- seats_at_50_50(plan_matrix[, i], va)
}

# Pull importance weights for the un-resampled particle population so
# the percentiles below reflect the true target distribution rather
# than the proposal distribution.
weights <- attr(ensemble, "wgt")
if (is.null(weights)) {
  weights <- rep(1.0 / n_plans, n_plans)
}
# Normalise just in case
weights <- weights / sum(weights)

# ----- Step F: Report -----------------------------------------------
# These should match the Python pipeline's reported values.

# Weighted quantile for un-resampled particle population. Sort by value,
# build cumulative weight, find the smallest value where cumweight >= q.
weighted_quantile <- function(x, w, q) {
  ord <- order(x)
  xs <- x[ord]
  ws <- w[ord]
  cw <- cumsum(ws) / sum(ws)
  vapply(q, function(qq) {
    idx <- which(cw >= qq)[1]
    if (is.na(idx)) tail(xs, 1) else xs[idx]
  }, numeric(1))
}

cat("\n========================================\n")
cat("  R cross-validation result\n")
cat("========================================\n")
cat("Ensemble size:", length(s50_values), "plans (weighted)\n")
cat("Effective sample size (importance-weighted):",
    round(1 / sum(weights^2)), "\n")
qs <- weighted_quantile(s50_values, weights, c(0.05, 0.50, 0.95, 0.99))
cat("seats@50/50 distribution across ensemble (weighted):\n")
cat("  median:    ", round(qs[2], 4), "\n")
cat("  p5:        ", round(qs[1], 4), "\n")
cat("  p95:       ", round(qs[3], 4), "\n")
cat("  p99:       ", round(qs[4], 4), "\n")
cat("  max:       ", round(max(s50_values), 4), "\n")
cat("  weighted % >= 0.4831 (v0_9 minority): ",
    round(100 * sum(weights[s50_values >= 0.4831]) / sum(weights), 2), "%\n")
cat("\n")
cat("Python ensemble published values (post-audit reference):\n")
cat("  See analysis/reports/v0_1_post_audit_recompute_deltas.md for the\n")
cat("  corrected percentile placements from the 100k pre-registered\n")
cat("  baseline ensemble. The earlier 2M exploratory enlargement was\n")
cat("  cancelled in favour of the standard 100k after diagnostics\n")
cat("  confirmed gold-standard convergence at much smaller sample sizes.\n")
cat("\n")
cat("  Buggy pre-audit 2M values, archived for delta comparison only:\n")
cat("    median: 0.4483, p5: 0.4253, p95: 0.4828, max: 0.5172\n")
cat("\n")
cat("Pass criterion: R values within +/-0.5pp of corrected Python values.\n")

# Compute Polsby-Popper compactness per plan for the falsification tests
# proposed by the PO ("the mechanism is the geometry"). Mean PP across the
# plan's districts is the per-plan summary; we keep the full per-district
# values too so distributions can be inspected later.
cat("Computing Polsby-Popper compactness across all plans...\n")
# redistmetrics::comp_polsby returns one value per (plan, district) pair
# in a long vector. Pass plans as the matrix and shp as the sf object.
pp_long <- redistmetrics::comp_polsby(plans = plan_matrix, shp = va)
# Reshape to (n_districts x n_plans) and average per plan.
pp_matrix <- matrix(pp_long, nrow = n_districts, ncol = n_plans)
mean_pp_per_plan <- colMeans(pp_matrix)
cat("Polsby-Popper distribution across plans:\n")
cat("  median: ", round(median(mean_pp_per_plan), 4), "\n")
cat("  p5:     ", round(quantile(mean_pp_per_plan, 0.05), 4), "\n")
cat("  p95:    ", round(quantile(mean_pp_per_plan, 0.95), 4), "\n")

# FALSIFICATION TESTS (PO design):
# Test #2: do the SMC plans that reach the minority's 0.4831 seats@50/50
# have systematically lower compactness than the rest?
# Test #4: how do the SMC compactness distribution and the Python ReCom
# compactness distribution compare? (Python comparison done in a separate
# script.)
high_ucp_mask <- s50_values >= 0.4831
if (sum(high_ucp_mask) > 0) {
  high_pp <- mean_pp_per_plan[high_ucp_mask]
  low_pp  <- mean_pp_per_plan[!high_ucp_mask]
  cat("Falsification Test #2 — does high-UCP-advantage need non-compact geometry?\n")
  cat(sprintf("  N high-UCP plans (s50 >= 0.4831): %d\n", sum(high_ucp_mask)))
  cat(sprintf("  Mean PP, high-UCP plans:  %.4f (lower = less compact)\n",
              mean(high_pp)))
  cat(sprintf("  Mean PP, other plans:     %.4f\n", mean(low_pp)))
  cat(sprintf("  Difference: %.4f  (negative => high-UCP plans ARE less compact)\n",
              mean(high_pp) - mean(low_pp)))
  if (length(low_pp) > 0 && length(high_pp) > 0) {
    t_test <- t.test(high_pp, low_pp)
    cat(sprintf("  Welch t-test p-value: %.4g\n", t_test$p.value))
  }
}

# Save outputs for the audit's record
saveRDS(list(s50 = s50_values, weights = weights, pp = mean_pp_per_plan),
        file = "data/v0_1_redist_crossvalidation_s50.rds")
write.csv(
  data.frame(seats_at_50_50 = s50_values, weight = weights,
             polsby_popper = mean_pp_per_plan),
  file = "data/v0_1_redist_crossvalidation_s50.csv",
  row.names = FALSE
)
cat("Wrote data/v0_1_redist_crossvalidation_s50.csv\n")
