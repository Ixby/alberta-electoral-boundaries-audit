# AI Onboarding & Context Guide

Welcome. If you are reading this, you are assisting with the **Alberta 2026 Electoral Boundary Forensic Audit**. 

This repository contains the data, mathematical models, and final reports used to forensically audit the proposed electoral maps for partisan bias, geometric gerrymandering, and population equality.

## 1. Core Context & The "Phase Shift"
You must understand the repository's timeline to understand its structure:
*   **The Blocked Phase (Provisional):** Prior to May 6, 2026, the official shapefiles were withheld. The audit relied on mathematically derived "Derived Provisional Geometries" (DPGs) denoted as `v0_1` through `v0_10`.
*   **The Canonical Phase (Current):** On May 6, official shapefiles were released. **All DPGs and their associated validation pipelines are now deprecated.** 
*   *Crucial Rule:* Never use any file in the `historical/` directory for active analysis. All current forensics must run against the `_canonical` shapefiles.

## 2. Directory Structure
The repository has just undergone a massive reorganization to become "Pitch Ready":
*   `outputs/`: The final, public-facing deliverables (`report_academic.md`, infographics, presentations).
*   `analysis/scripts/`: The ~60 active Python scripts running the statistical forensics (Polsby-Popper, MCMC ensembles, Packing/Cracking).
*   `data/`: Tiered into `raw/` (immutable shapefiles), `processed/` (cleaned data), and `outputs/` (generated metrics).
*   `historical/`: The graveyard. Contains all deprecated `dpg_archive/` build scripts and old `v0_10` geometries. 

## 3. The Portability Refactor (In Progress)
We are currently in the middle of a massive codebase refactor to ensure these scripts can be run on *any* machine against *any* arbitrary maps. 
*   **Strict Rule:** No absolute paths are allowed.
*   **Strict Rule:** Scripts are being migrated away from hardcoded `ROOT / "data"` calls and instead must rely on a central `config.yaml` to locate shapefiles and demographic data.
*   **Strict Rule:** Core logic (like `packing_cracking_analysis.py`) should accept generic GeoDataFrames and dynamic column names (e.g., `va_ndp`) rather than hardcoding "Alberta UCP vs NDP" logic.

## 4. Execution & Testing
*   `run_master_qa.py`: Executes the full PyTest mathematical suite AND the topological data integrity audit (`run_audit.py`).
*   `analysis/scripts/mcmc_ensemble_canonical.py`: The massive Markov Chain Monte Carlo (MCMC) engine that generates the 250,000-step baseline for partisan symmetry.

When you take the wheel, refer to the `tandem.md` file in the root directory for any immediate handoff notes from the previous agent. Good luck.
