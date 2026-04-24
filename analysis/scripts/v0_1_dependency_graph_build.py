"""Build the Alberta audit dependency DAG.

This script produces the machine-readable directed acyclic graph of the
Alberta audit specified in ``analysis/methodology/v0_1_test_apparatus_defense.md``
section 3 and the PO synthesis ("Novel Combined Test: The Dependency Graph").

Nodes are organized into four layers:

* **L0 Raw:** primary data sources (enumerated from ``FROZEN_MANIFEST.md``).
* **L1 Constructed:** derived data products under ``data/``.
* **L2 Measurement:** Python scripts under ``analysis/scripts/``.
* **L3 Inference:** findings as stated in ``report_academic.md`` sections 5.1 through 5.9.

Edges are typed ``required`` (target cannot exist without source),
``corroborating`` (target has other independent paths), or ``validating``
(source is a validation/gate for target). Edges from L0/L1 into L2 and
from L2 into L1/L3 are discovered by parsing ``Forward:`` / ``Backward:``
docstring headers where present; the L0 set and the L3 finding set are
hand-encoded from ``FROZEN_MANIFEST.md`` and ``report_academic.md``
respectively.

Outputs:

* ``analysis/methodology/audit_dependency_graph.json`` — the DAG.
* ``analysis/methodology/audit_dependency_graph.dot`` — Graphviz DOT source.

Run ``dot -Tsvg analysis/methodology/audit_dependency_graph.dot -o
maps/audit_dependency_graph.svg`` to render.

Forward: analysis/methodology/audit_dependency_graph.json
Forward: analysis/methodology/audit_dependency_graph.dot
Backward:
  FROZEN_MANIFEST.md
  report_academic.md
  analysis/scripts/*.py  (Forward/Backward headers where present)
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
SCRIPTS = ROOT / "analysis" / "scripts"
METHODOLOGY = ROOT / "analysis" / "methodology"

OUT_JSON = METHODOLOGY / "audit_dependency_graph.json"
OUT_DOT = METHODOLOGY / "audit_dependency_graph.dot"

SCHEMA_VERSION = "v0_1"


# ---------------------------------------------------------------------------
# L0 — Raw data nodes (from FROZEN_MANIFEST.md)
# ---------------------------------------------------------------------------

L0_NODES: List[Dict[str, Any]] = [
    # Primary election and commission sources
    {
        "id": "L0:data.2023_statement_of_vote",
        "layer": "L0",
        "name": "2023 Statement of Vote",
        "type": "raw_data",
        "path": "data/2023_results.xlsx",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / 2023 Statement of Vote",
    },
    {
        "id": "L0:data.2015_statement_of_vote",
        "layer": "L0",
        "name": "2015 Statement of Vote",
        "type": "raw_data",
        "path": "data/2015_results.xlsx",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / 2015 Statement of Vote",
    },
    {
        "id": "L0:data.commission_final_report_2026",
        "layer": "L0",
        "name": "2026 commission final report (majority + minority + chair addendum)",
        "type": "raw_data",
        "path": "(external 80 MB PDF — archived on Wayback)",
        "provenance": "Alberta Electoral Boundaries Commission",
        "frozen_manifest_row": "Primary / 2026 commission final report",
    },
    {
        "id": "L0:data.commission_final_report_2017",
        "layer": "L0",
        "name": "2017 commission final report",
        "type": "raw_data",
        "path": "(external 36.5 MB PDF — archived on Wayback)",
        "provenance": "Alberta Electoral Boundaries Commission",
        "frozen_manifest_row": "Primary / 2017 commission final report",
    },
    {
        "id": "L0:data.commission_map_pngs",
        "layer": "L0",
        "name": "Commission map PNGs (majority + minority, Calgary/Edmonton/overview/other cities)",
        "type": "raw_data",
        "path": "maps/majority_calgary.jpg, maps/minority_*.jpg",
        "provenance": "Extracted from 2026 commission final report",
        "frozen_manifest_row": "Primary / commission final report (page extractions)",
    },
    {
        "id": "L0:data.2019_ed_shapefile",
        "layer": "L0",
        "name": "2019 Alberta electoral-division shapefile (87 EDs, Bill 33 enacted)",
        "type": "raw_data",
        "path": "data/alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / 2019 ED shapefiles",
    },
    {
        "id": "L0:data.2023_va_shapefile",
        "layer": "L0",
        "name": "2023 Voting-Area polygon shapefile (4,765 VAs)",
        "type": "raw_data",
        "path": "data/alberta_2023_vas/EA_Voting_Area_Boundaries_2023.shp",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / 2023 VA shapefiles",
    },
    # StatsCan sources
    {
        "id": "L0:data.2021_das_gpkg",
        "layer": "L0",
        "name": "2021 Dissemination-Area cartographic boundaries",
        "type": "raw_data",
        "path": "data/alberta_2021_das.gpkg",
        "provenance": "Statistics Canada (98-401-X2021006 geometry)",
        "frozen_manifest_row": "StatsCan / 2021 DA cartographic boundaries",
    },
    {
        "id": "L0:data.2021_csds_gpkg",
        "layer": "L0",
        "name": "2021 Census Sub-Division cartographic boundaries",
        "type": "raw_data",
        "path": "data/alberta_2021_csds.gpkg",
        "provenance": "Statistics Canada (98-401-X2021005 geometry)",
        "frozen_manifest_row": "StatsCan / 2021 CSD cartographic boundaries",
    },
    {
        "id": "L0:data.2021_da_populations",
        "layer": "L0",
        "name": "2021 DA populations (98-401-X2021006)",
        "type": "raw_data",
        "path": "data/alberta_2021_da_populations.csv",
        "provenance": "Statistics Canada",
        "frozen_manifest_row": "StatsCan / 98-401-X2021006 DA population",
    },
    {
        "id": "L0:data.2021_csd_populations",
        "layer": "L0",
        "name": "2021 CSD populations (98-401-X2021005)",
        "type": "raw_data",
        "path": "data/alberta_2021_csd_populations.csv",
        "provenance": "Statistics Canada",
        "frozen_manifest_row": "StatsCan / 98-401-X2021005 CSD population",
    },
    {
        "id": "L0:data.statscan_1710000901",
        "layer": "L0",
        "name": "StatsCan Table 17-10-0009 quarterly population estimates",
        "type": "raw_data",
        "path": "(external CSV — archived on Wayback)",
        "provenance": "Statistics Canada",
        "frozen_manifest_row": "StatsCan / Table 17-10-0009",
    },
    {
        "id": "L0:data.cochrane_journey_to_work",
        "layer": "L0",
        "name": "StatsCan Table 98-10-0459 journey-to-work (Cochrane CSD)",
        "type": "raw_data",
        "path": "data/v0_1_cochrane_journey_to_work.csv",
        "provenance": "Statistics Canada",
        "frozen_manifest_row": "StatsCan / Journey-to-work STC98-10-0459",
    },
    # Alberta Treasury Board
    {
        "id": "L0:data.tbf_population_estimates",
        "layer": "L0",
        "name": "Alberta TBF / Economic Dashboard population estimates",
        "type": "raw_data",
        "path": "(external dashboard; frozen into Plan-B CSVs)",
        "provenance": "Alberta Treasury Board & Finance",
        "frozen_manifest_row": "ATBF / Economic Dashboard Population",
    },
    # Projection / polling
    {
        "id": "L0:data.338canada_snapshots",
        "layer": "L0",
        "name": "338Canada Alberta per-riding projections (87-seat) + historical snapshots",
        "type": "raw_data",
        "path": "data/v0_1_338canada_per_riding_87seat.csv, data/v0_1_338canada_historical_snapshots.csv, data/v0_1_338_historical/",
        "provenance": "338Canada",
        "frozen_manifest_row": "Projections / 338Canada per-riding + historical",
    },
    # City of Calgary
    {
        "id": "L0:data.calgary_wards_geojson",
        "layer": "L0",
        "name": "Calgary wards GeoJSON (14 ward polygons)",
        "type": "raw_data",
        "path": "data/calgary_wards.geojson",
        "provenance": "City of Calgary open data",
        "frozen_manifest_row": "Calgary / wards GeoJSON",
    },
    # Submission archive
    {
        "id": "L0:data.submission_archive",
        "layer": "L0",
        "name": "Commission public submissions archive (~1,340 submissions)",
        "type": "raw_data",
        "path": "data/submission_search_dataset.csv",
        "provenance": "Alberta Electoral Boundaries Commission public consultation record",
        "frozen_manifest_row": "Commission / submission archive (not in manifest; bundled as CSV)",
    },
    # Commission text-extracted artifacts
    {
        "id": "L0:data.commission_published_populations",
        "layer": "L0",
        "name": "Commission-published per-ED populations (majority App A + minority App E)",
        "type": "raw_data",
        "path": "data/v0_1_majority_2026_populations.csv, data/v0_1_minority_2026_populations.csv, data/v0_1_minority_2026_populations_appendixE.csv",
        "provenance": "Commission final report, variance tables",
        "frozen_manifest_row": "Primary / 2026 commission final report (Appendix A/E tables)",
    },
    {
        "id": "L0:data.commission_rationales",
        "layer": "L0",
        "name": "Commission minority rationale text (Appendix E prose)",
        "type": "raw_data",
        "path": "data/v0_1_minority_rationales.csv",
        "provenance": "Commission final report Appendix E",
        "frozen_manifest_row": "Primary / 2026 commission final report (Appendix E rationales)",
    },
    {
        "id": "L0:data.2019_ed_populations",
        "layer": "L0",
        "name": "2019 ED populations (Appendix C legal baseline)",
        "type": "raw_data",
        "path": "data/v0_1_alberta_2019_populations.csv, data/v0_1_a1_legal_baseline_2019eds_2021census.csv",
        "provenance": "Commission 2017 final report + 2021 Census DA roll-up",
        "frozen_manifest_row": "Primary / 2017 commission final report + StatsCan DA populations",
    },
    {
        "id": "L0:data.2019_election_results",
        "layer": "L0",
        "name": "2019 Alberta provincial election results (attributed to 2019 EDs)",
        "type": "raw_data",
        "path": "data/v0_1_alberta_2019_results.csv",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / Elections Alberta prior-cycle results",
    },
    {
        "id": "L0:data.2015_election_results",
        "layer": "L0",
        "name": "2015 Alberta provincial election results",
        "type": "raw_data",
        "path": "data/v0_1_alberta_2015_results.csv",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / 2015 Statement of Vote (parsed)",
    },
    {
        "id": "L0:data.byelections_2019_2026",
        "layer": "L0",
        "name": "Alberta byelections 2019-2026",
        "type": "raw_data",
        "path": "data/v0_1_alberta_byelections_2019_2026.csv",
        "provenance": "Elections Alberta",
        "frozen_manifest_row": "Primary / Elections Alberta byelection records",
    },
    {
        "id": "L0:data.commission_rationales_text",
        "layer": "L0",
        "name": "2015-to-2019 boundary crosswalk (partial)",
        "type": "raw_data",
        "path": "data/v0_1_2015_to_2019_crosswalk.csv, data/v0_1_2015_to_2019_crosswalk_partial.csv",
        "provenance": "Commission 2017 final report text",
        "frozen_manifest_row": "Primary / 2017 commission final report",
    },
    {
        "id": "L0:data.commission_r5_addendum",
        "layer": "L0",
        "name": "Chair Miller's Recommendation 5 (Majority Report addendum)",
        "type": "raw_data",
        "path": "(extracted from commission final report pp. 66-67)",
        "provenance": "Commission final report, chair addendum",
        "frozen_manifest_row": "Primary / 2026 commission final report (chair addendum)",
    },
    {
        "id": "L0:data.news_coverage_april_2026",
        "layer": "L0",
        "name": "News coverage of April 16, 2026 government action (CBC / Calgary Journal / Rimbey)",
        "type": "raw_data",
        "path": "(external; Wayback + archive.ph snapshots)",
        "provenance": "CBC Edmonton, Calgary Journal, Rimbey Review",
        "frozen_manifest_row": "News / April 2026 coverage (§5.9.2)",
    },
    {
        "id": "L0:data.ref_saskatchewan_1991",
        "layer": "L0",
        "name": "Reference re Provincial Electoral Boundaries (Saskatchewan) [1991] 2 SCR 158",
        "type": "legal_source",
        "path": "(case law — cited not checked in)",
        "provenance": "Supreme Court of Canada",
        "frozen_manifest_row": "Legal / effective-representation doctrine",
    },
    {
        "id": "L0:data.electoral_boundaries_act",
        "layer": "L0",
        "name": "Alberta Electoral Boundaries Commission Act (s.12, s.15, s.21)",
        "type": "legal_source",
        "path": "(statute — cited not checked in)",
        "provenance": "Province of Alberta",
        "frozen_manifest_row": "Legal / Alberta EBC Act",
    },
    {
        "id": "L0:data.rizzo_rizzo_1998",
        "layer": "L0",
        "name": "Rizzo & Rizzo Shoes Ltd. (Re) [1998] 1 SCR 27 (purposive interpretation)",
        "type": "legal_source",
        "path": "(case law — cited not checked in)",
        "provenance": "Supreme Court of Canada",
        "frozen_manifest_row": "Legal / statutory interpretation",
    },
    # Historical projection artefacts
    {
        "id": "L0:data.338_historical_snapshots_dir",
        "layer": "L0",
        "name": "338Canada pre-2023 reallocated snapshot CSVs",
        "type": "raw_data",
        "path": "data/v0_1_338_historical/",
        "provenance": "338Canada (frozen snapshots)",
        "frozen_manifest_row": "Projections / 338Canada historical snapshot directory",
    },
    # Derived from commission published rationales
    {
        "id": "L0:data.school_division_boundaries",
        "layer": "L0",
        "name": "Alberta Education school-division boundaries (R5 / R11 cross-reference)",
        "type": "raw_data",
        "path": "(referenced in methodology only)",
        "provenance": "Alberta Education",
        "frozen_manifest_row": "Alberta Education / school division shapefiles",
    },
    # Frozen URL manifest artifact itself (source of truth for L0)
    {
        "id": "L0:doc.frozen_manifest",
        "layer": "L0",
        "name": "FROZEN_MANIFEST.md (reproducibility manifest)",
        "type": "documentation",
        "path": "FROZEN_MANIFEST.md",
        "provenance": "Audit",
        "frozen_manifest_row": "(self-reference)",
    },
]


# ---------------------------------------------------------------------------
# L1 — Constructed data products
# ---------------------------------------------------------------------------

L1_NODES: List[Dict[str, Any]] = [
    # DPG topology chain (v0_1 -> v0_2 -> v0_3 -> v0_4 -> v0_5)
    {
        "id": "L1:constructed.dpg_v0_1_canonical",
        "layer": "L1",
        "name": "v0_1 canonical DPGs (majority + minority, tier-A/B/C hybrid)",
        "type": "derived_geometry",
        "path": "data/v0_1_canonical_{majority,minority}_2026_eds.gpkg",
        "notes": "Original canonical DPG pre topology-cleanup; contains residual overlap.",
    },
    {
        "id": "L1:constructed.dpg_v0_2_topoclean",
        "layer": "L1",
        "name": "v0_2 topology-cleaned DPGs",
        "type": "derived_geometry",
        "path": "data/v0_2_canonical_{majority,minority}_2026_eds_topoclean.gpkg",
        "notes": "Precedence-resolved overlap cleanup (2,754 km² / 16,734 km² claimed).",
    },
    {
        "id": "L1:constructed.dpg_v0_3_swept",
        "layer": "L1",
        "name": "v0_3 pop-swept DPGs",
        "type": "derived_geometry",
        "path": "data/v0_3_canonical_{majority,minority}_2026_eds_swept.gpkg",
    },
    {
        "id": "L1:constructed.dpg_v0_4_municipal",
        "layer": "L1",
        "name": "v0_4 municipal-anchored DPGs",
        "type": "derived_geometry",
        "path": "data/v0_4_canonical_{majority,minority}_2026_eds_anchored.gpkg",
    },
    {
        "id": "L1:constructed.dpg_v0_5_da_anchored",
        "layer": "L1",
        "name": "v0_5 DA-anchored DPGs",
        "type": "derived_geometry",
        "path": "data/v0_5_canonical_{majority,minority}_2026_eds_da_anchored.gpkg",
        "notes": "Survey-grade snap to StatsCan DA edges. Known defect: empty polygons for 5 EDs per map.",
    },
    # Intermediate refinement shapes
    {
        "id": "L1:constructed.approximate_eds",
        "layer": "L1",
        "name": "Approximate majority / minority 2026 EDs (direct-polygon tier)",
        "type": "derived_geometry",
        "path": "data/v0_1_approximate_{majority,minority}_2026_eds.gpkg",
    },
    {
        "id": "L1:constructed.refined_eds_v6",
        "layer": "L1",
        "name": "Refined v6 majority / minority polygons (shape refinement chain)",
        "type": "derived_geometry",
        "path": "data/v0_1_refined_v6_{majority,minority}_2026_eds.gpkg",
    },
    {
        "id": "L1:constructed.derived_v7_eds",
        "layer": "L1",
        "name": "Derived v7 minority / majority 2026 ED polygons",
        "type": "derived_geometry",
        "path": "data/v0_1_derived_v7_{majority,minority}_2026_eds.gpkg",
    },
    {
        "id": "L1:constructed.composite_eds",
        "layer": "L1",
        "name": "Composite majority / minority polygons (v0_1 workflow precursor)",
        "type": "derived_geometry",
        "path": "data/v0_1_composite_{majority,minority}_2026_eds.gpkg",
    },
    # Crosswalks
    {
        "id": "L1:constructed.crosswalk_majority_full",
        "layer": "L1",
        "name": "Majority 88-row full crosswalk (2019 → 2026 EDs)",
        "type": "crosswalk",
        "path": "data/v0_1_majority_full_crosswalk.csv",
    },
    {
        "id": "L1:constructed.crosswalk_minority_full",
        "layer": "L1",
        "name": "Minority 88-row full crosswalk (2019 → 2026 EDs)",
        "type": "crosswalk",
        "path": "data/v0_1_minority_full_crosswalk.csv",
    },
    {
        "id": "L1:constructed.crosswalk_majority_hybrid",
        "layer": "L1",
        "name": "Majority hybrid crosswalk (urban-weighted blend)",
        "type": "crosswalk",
        "path": "data/v0_1_majority_hybrid_crosswalk.csv",
    },
    {
        "id": "L1:constructed.crosswalk_minority_hybrid",
        "layer": "L1",
        "name": "Minority hybrid crosswalk (urban-weighted blend)",
        "type": "crosswalk",
        "path": "data/v0_1_minority_hybrid_crosswalk.csv, data/v0_1_minority_hybrid_crosswalk_appendixE.csv",
    },
    # VA-level substrates
    {
        "id": "L1:constructed.va_substrate_elecday",
        "layer": "L1",
        "name": "VA vote substrate — Election-Day-only (pre-splat)",
        "type": "vote_substrate",
        "path": "data/va_polygons_with_2023_votes.gpkg",
    },
    {
        "id": "L1:constructed.va_substrate_full",
        "layer": "L1",
        "name": "VA vote substrate — full (election-day + advance-vote splatted)",
        "type": "vote_substrate",
        "path": "data/va_polygons_with_full_2023_votes.gpkg",
    },
    {
        "id": "L1:constructed.va_pop_from_das",
        "layer": "L1",
        "name": "VA-level 2021 DA-weighted population",
        "type": "vote_substrate",
        "path": "data/va_pop_from_das.csv",
    },
    {
        "id": "L1:constructed.polls_2023_unified",
        "layer": "L1",
        "name": "2023 polls unified (per-poll vote totals)",
        "type": "derived_data",
        "path": "analysis/polls_2023_unified.csv",
    },
    {
        "id": "L1:constructed.advance_vote_diag",
        "layer": "L1",
        "name": "Advance-vote splat diagnostics",
        "type": "derived_data",
        "path": "analysis/v0_1_advance_vote_splat_diagnostics.csv",
    },
    # MCMC ensemble artefacts
    {
        "id": "L1:constructed.mcmc_ensemble_10k",
        "layer": "L1",
        "name": "10k preliminary ReCom ensemble samples",
        "type": "mcmc_ensemble",
        "path": "data/v0_1_mcmc_ensemble_samples.csv, data/v0_1_mcmc_ensemble_percentiles.csv",
    },
    {
        "id": "L1:constructed.mcmc_ensemble_100k",
        "layer": "L1",
        "name": "100k publication-grade ReCom ensemble samples + percentiles",
        "type": "mcmc_ensemble",
        "path": "data/v0_1_mcmc_ensemble_samples_100k.csv, data/v0_1_mcmc_ensemble_percentiles_100k.csv, data/v0_1_mcmc_ensemble_percentiles_full_100k.csv, data/v0_1_mcmc_convergence_diagnostics_100k.json",
    },
    {
        "id": "L1:constructed.mcmc_real_map_scores",
        "layer": "L1",
        "name": "Real-map scores under ensemble baselines (v0_1/v2/full/full_100k)",
        "type": "mcmc_artifact",
        "path": "data/v0_1_mcmc_real_map_scores*.json",
    },
    {
        "id": "L1:constructed.mcmc_multichain",
        "layer": "L1",
        "name": "3-chain ReCom multi-seed ensemble + R-hat diagnostic",
        "type": "mcmc_ensemble",
        "path": "data/v0_1_mcmc_multichain_samples.csv, data/v0_1_mcmc_multichain_pooled.csv, data/v0_1_mcmc_multichain_rhat.json, data/v0_1_mcmc_multichain_summary.md",
    },
    # Phase 4B / 4C outputs
    {
        "id": "L1:constructed.phase4b_pops",
        "layer": "L1",
        "name": "Phase 4B per-2026-ED 2021 census populations (majority + minority)",
        "type": "phase4_output",
        "path": "data/v0_1_phase4b_{majority,minority}_2021_populations.csv",
    },
    {
        "id": "L1:constructed.phase4c_votes",
        "layer": "L1",
        "name": "Phase 4C per-2026-ED 2023 vote totals (centroid)",
        "type": "phase4_output",
        "path": "data/v0_1_phase4c_{majority,minority}_2023_votes.csv",
    },
    {
        "id": "L1:constructed.phase4c_votes_maup_v1",
        "layer": "L1",
        "name": "Phase 4C MAUP-v1 area-weighted vote totals (v0_1 DPG)",
        "type": "phase4_output",
        "path": "data/v0_1_phase4c_{majority,minority}_2023_votes_maup.csv",
    },
    {
        "id": "L1:constructed.phase4c_votes_maup_v2",
        "layer": "L1",
        "name": "Phase 4C MAUP-v2 vote totals (on v0_2 topology-clean DPG)",
        "type": "phase4_output",
        "path": "data/v0_2_phase4c_{majority,minority}_2023_votes_maup.csv",
    },
    {
        "id": "L1:constructed.phase4c_votes_maup_v05",
        "layer": "L1",
        "name": "Phase 4C MAUP-v3 vote totals (on v0_5 DA-anchored DPG)",
        "type": "phase4_output",
        "path": "data/v0_5_phase4c_{majority,minority}_2023_votes_maup.csv",
    },
    {
        "id": "L1:constructed.phase4b_v05_pops",
        "layer": "L1",
        "name": "Phase 4B v0_5 populations (DA-anchored DPG)",
        "type": "phase4_output",
        "path": "data/v0_5_phase4b_{majority,minority}_2021_populations.csv",
    },
    {
        "id": "L1:constructed.phase4f_validation",
        "layer": "L1",
        "name": "Phase 4F validation deltas (commission vs Phase 4B)",
        "type": "validation_gate",
        "path": "data/v0_1_phase4f_validation_deltas.csv, data/v0_1_phase4f_validation_deltas_v2.csv, data/v0_5_phase4f_validation_deltas.csv",
    },
    {
        "id": "L1:constructed.phase4bcdef_summary",
        "layer": "L1",
        "name": "Phase 4B/C/D/E/F execution summary JSON",
        "type": "phase4_output",
        "path": "data/v0_1_phase_4bcdef_summary.json",
    },
    {
        "id": "L1:constructed.va_to_2026_assignments",
        "layer": "L1",
        "name": "VA-to-2026-ED assignments (centroid + MAUP)",
        "type": "phase4_output",
        "path": "analysis/phase_4c_va_to_2026_assignments.csv, analysis/reports/phase_4c_va_to_2026_assignments_maup.csv, analysis/reports/phase_4c_va_to_2026_assignments_maup_v2.csv, analysis/reports/v0_5_phase4c_va_to_2026_assignments_maup.csv",
    },
    {
        "id": "L1:constructed.phase4c_maup_summary",
        "layer": "L1",
        "name": "Phase 4C MAUP summary JSON (v0_1/v0_2/v0_5)",
        "type": "phase4_output",
        "path": "analysis/reports/v0_1_phase4c_maup_summary.json, analysis/reports/v0_2_phase4c_maup_summary.json, analysis/reports/v0_5_phase4c_maup_summary.json",
    },
    # Anchoring summaries
    {
        "id": "L1:constructed.municipal_anchoring_summary",
        "layer": "L1",
        "name": "Municipal anchoring summary (v0_4)",
        "type": "anchoring_output",
        "path": "data/v0_1_municipal_anchoring_summary.json, analysis/reports/v0_1_municipal_anchoring_log.csv",
    },
    {
        "id": "L1:constructed.da_anchoring_summary",
        "layer": "L1",
        "name": "DA boundary anchoring summary (v0_5)",
        "type": "anchoring_output",
        "path": "data/v0_1_da_anchoring_summary.json, analysis/reports/v0_1_da_anchoring_log.csv",
    },
    {
        "id": "L1:constructed.topology_cleanup_log",
        "layer": "L1",
        "name": "Topology cleanup log (v0_1 → v0_2)",
        "type": "anchoring_output",
        "path": "data/v0_1_tier_c_sweep_summary.json, analysis/reports/v0_1_topology_cleanup_summary.json, analysis/reports/v0_1_topology_cleanup_log.csv",
    },
    # Perturbation samples
    {
        "id": "L1:constructed.dpg_perturbation_flat",
        "layer": "L1",
        "name": "DPG perturbation samples (flat ±500m)",
        "type": "perturbation_output",
        "path": "data/v0_1_dpg_perturbation_samples.csv, data/v0_1_dpg_perturbation_summary.json",
    },
    {
        "id": "L1:constructed.dpg_perturbation_tiered",
        "layer": "L1",
        "name": "DPG perturbation samples (tier-aware)",
        "type": "perturbation_output",
        "path": "data/v0_1_dpg_perturbation_samples_v2_tiered.csv, data/v0_1_dpg_perturbation_summary_v2_tiered.json",
    },
    {
        "id": "L1:constructed.dpg_perturbation_tight",
        "layer": "L1",
        "name": "DPG perturbation samples (tight tier-aware)",
        "type": "perturbation_output",
        "path": "data/v0_1_dpg_perturbation_samples_v3_tight.csv, data/v0_1_dpg_perturbation_summary_v3_tight.json",
    },
    {
        "id": "L1:constructed.dpg_perturbation_v05",
        "layer": "L1",
        "name": "DPG perturbation samples (v0_5 DA-anchored substrate)",
        "type": "perturbation_output",
        "path": "data/v0_5_dpg_perturbation_samples.csv, data/v0_5_dpg_perturbation_summary.json",
    },
    # Other derived products
    {
        "id": "L1:constructed.compactness_scores",
        "layer": "L1",
        "name": "Polsby-Popper compactness scores (v0_1 + refined)",
        "type": "derived_metric",
        "path": "data/v0_1_compactness_scores.csv, data/v0_1_compactness_scores_refined.csv",
    },
    {
        "id": "L1:constructed.chen_rodden",
        "layer": "L1",
        "name": "Chen-Rodden decomposition (pairwise + absolute)",
        "type": "derived_metric",
        "path": "data/v0_1_chen_rodden_decomposition.csv, data/v0_1_chen_rodden_decomposition.json, data/v0_1_chen_rodden_absolute_decomposition.json, data/v0_1_chen_rodden_simulation.csv, data/v0_1_chen_rodden_summary.json",
    },
    {
        "id": "L1:constructed.cross_election_asymmetry",
        "layer": "L1",
        "name": "Cross-election asymmetry tables (3-way 2015/2019/2023)",
        "type": "derived_metric",
        "path": "data/v0_1_cross_election_asymmetry_3way.csv, data/v0_1_2015_cross_election_summary.csv, data/v0_1_province_wide_drift_*.csv",
    },
    {
        "id": "L1:constructed.rural_gap_summary",
        "layer": "L1",
        "name": "Rural gap dissection — smallest-10 majority/minority EDs",
        "type": "derived_metric",
        "path": "analysis/v0_1_rural_gap_summary.json, analysis/v0_1_rural_gap_ed_comparison.csv, analysis/v0_1_rural_gap_smallest10_majority.csv, analysis/v0_1_rural_gap_smallest10_minority.csv",
    },
    {
        "id": "L1:constructed.symmetry_counter_test",
        "layer": "L1",
        "name": "Majority-symmetry counter-test (Edmonton zones + 4-way city splits)",
        "type": "derived_metric",
        "path": "data/v0_1_majority_symmetry_counter_test.csv",
    },
    {
        "id": "L1:constructed.csd_splits",
        "layer": "L1",
        "name": "CSD community-of-interest splits",
        "type": "derived_metric",
        "path": "data/v0_1_csd_splits_summary.csv",
    },
    {
        "id": "L1:constructed.submission_search_results",
        "layer": "L1",
        "name": "Submission archive keyword-search dataset + findings",
        "type": "derived_data",
        "path": "data/submission_search_dataset.csv, analysis/reports/submission_search_findings.md",
    },
    {
        "id": "L1:constructed.boundary_refinement_impact",
        "layer": "L1",
        "name": "Boundary refinement impact CSVs (v2–v6)",
        "type": "derived_data",
        "path": "data/v0_1_boundary_refinement_impact*.csv",
    },
    {
        "id": "L1:constructed.338canada_reallocated",
        "layer": "L1",
        "name": "338Canada reallocated to 2026 EDs (majority + minority)",
        "type": "derived_data",
        "path": "data/v0_1_338canada_reallocated_majority.csv, data/v0_1_338canada_reallocated_minority.csv, data/v0_1_338canada_ridings_index.csv",
    },
    {
        "id": "L1:constructed.canadian_base_rate",
        "layer": "L1",
        "name": "Canadian redistribution base-rate comparator (n=6)",
        "type": "derived_data",
        "path": "data/v0_1_canadian_redistribution_base_rate.csv",
    },
    {
        "id": "L1:constructed.marginal_seats",
        "layer": "L1",
        "name": "Marginal-seats per-ED margins + uniform-swing flips",
        "type": "derived_data",
        "path": "data/v0_1_justification_test_inputs.csv",
    },
    {
        "id": "L1:constructed.hybrid_adjacency",
        "layer": "L1",
        "name": "Hybrid adjacent VAs (inter-ED boundary VA mapping)",
        "type": "derived_data",
        "path": "data/hybrid_adjacent_vas.csv",
    },
    {
        "id": "L1:constructed.tier_c_reference",
        "layer": "L1",
        "name": "Tier-C parent-union reference + sweep summary",
        "type": "derived_data",
        "path": "data/v0_1_tierC_parent_union_reference.csv, data/v0_1_tier_c_sweep_summary.json",
    },
    {
        "id": "L1:constructed.max_dpi_extract",
        "layer": "L1",
        "name": "Max-DPI commission-map extractions (bottleneck audit)",
        "type": "derived_data",
        "path": "analysis/reports/v0_1_max_dpi_extract.json, analysis/reports/v0_1_max_dpi_inspect.json",
    },
]


# ---------------------------------------------------------------------------
# L2 — Measurement scripts (enriched from Forward/Backward headers)
# ---------------------------------------------------------------------------

# Canonical script manifest with explicit layer metadata. Scripts not on this
# list that are found in analysis/scripts/ are still added, just without a
# curated dependency map.

L2_MANIFEST: List[Dict[str, Any]] = [
    # Geometry construction
    {
        "path": "analysis/scripts/v0_1_build_canonical_shapefiles.py",
        "name": "Build canonical shapefiles (v0_1 canonical DPGs)",
        "role": "Produces L1:dpg_v0_1_canonical from approximate + refined + derived EDs.",
    },
    {
        "path": "analysis/scripts/v0_1_build_canonical_shapefiles_v2.py",
        "name": "Build canonical shapefiles v2 (post-shape-refinement)",
        "role": "Second-pass canonical shapefile builder.",
    },
    {
        "path": "analysis/scripts/v0_1_build_composite_shapefiles.py",
        "name": "Build composite shapefiles",
        "role": "Assembles composite polygons from tier-A/B/C inputs.",
    },
    {
        "path": "analysis/scripts/v0_1_build_full_crosswalks.py",
        "name": "Build 88-row full crosswalks",
        "role": "Produces majority/minority full crosswalk CSVs.",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement.py",
        "name": "Shape refinement v1",
        "role": "Polygon refinement pass (v1).",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v2.py",
        "name": "Shape refinement v2",
        "role": "Polygon refinement pass (v2).",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v3.py",
        "name": "Shape refinement v3",
        "role": "Polygon refinement pass (v3).",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v4.py",
        "name": "Shape refinement v4",
        "role": "Polygon refinement pass (v4).",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v5.py",
        "name": "Shape refinement v5",
        "role": "Polygon refinement pass (v5).",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v6.py",
        "name": "Shape refinement v6",
        "role": "Polygon refinement pass (v6) — minority v6 canonical source.",
    },
    {
        "path": "analysis/v0_1_shape_derivation_v7.py",
        "name": "Shape derivation v7 (minority 89-ED derived set)",
        "role": "Produces derived v7 minority polygon set.",
    },
    {
        "path": "analysis/scripts/v0_1_topology_cleanup.py",
        "name": "Topology cleanup (v0_1 → v0_2)",
        "role": "Precedence-resolved overlap cleanup producing v0_2 DPG.",
    },
    {
        "path": "analysis/scripts/v0_1_municipal_anchoring.py",
        "name": "Municipal-boundary anchoring (v0_2 → v0_4)",
        "role": "Snaps DPG perimeters to CSD municipal boundaries.",
    },
    {
        "path": "analysis/scripts/v0_1_da_boundary_anchoring.py",
        "name": "DA-boundary anchoring (v0_4 → v0_5)",
        "role": "Snaps residual perimeters to StatsCan DA edges.",
    },
    # VA vote substrate
    {
        "path": "analysis/scripts/v0_1_advance_vote_splat.py",
        "name": "Advance-vote splat (apportion Vote-Anywhere to VAs)",
        "role": "Produces full-VA substrate from Election-Day-only.",
    },
    {
        "path": "analysis/scripts/v0_1_poll_attribution_skeleton.py",
        "name": "Poll-to-VA attribution skeleton",
        "role": "Polls aggregated into VAs for vote conservation.",
    },
    {
        "path": "analysis/scripts/parse_2015_results.py",
        "name": "Parse 2015 Statement of Vote",
        "role": "2015 xlsx → CSV per-ED results.",
    },
    # Phase 4
    {
        "path": "analysis/scripts/phase_4c_prep.py",
        "name": "Phase 4C preparation",
        "role": "Builds VA substrates for Phase 4C.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4c_va_attribution.py",
        "name": "Phase 4C centroid-in-polygon attribution",
        "role": "Centroid-based 2023-vote assignment to 2026 EDs.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4c_va_attribution_maup.py",
        "name": "Phase 4C MAUP-v1 area-weighted attribution",
        "role": "Area-weighted VA → 2026-ED assignment on v0_1 DPG.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4c_va_attribution_maup_v2.py",
        "name": "Phase 4C MAUP-v2 on v0_2 topology-clean DPG",
        "role": "Area-weighted attribution on cleaned geometry.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4c_va_attribution_maup_v3_v05.py",
        "name": "Phase 4C MAUP-v3 on v0_5 DA-anchored DPG",
        "role": "Area-weighted attribution on DA-anchored geometry.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4bcdef_execution.py",
        "name": "Phase 4B/C/D/E/F execution pipeline",
        "role": "Primary Phase-4 driver producing per-ED pop + vote totals + validation.",
    },
    {
        "path": "analysis/scripts/v0_1_phase_4bf_v05.py",
        "name": "Phase 4B+4F execution on v0_5 DA-anchored substrate",
        "role": "Parallel Phase-4 driver on v0_5 DPG.",
    },
    # Population / A-family
    {
        "path": "analysis/scripts/electoral_forensics_population.py",
        "name": "Electoral forensics — population equality (A1/A2/A2b)",
        "role": "MAD, Calgary zone gap, urban/rural regional breakdown.",
    },
    {
        "path": "analysis/scripts/v0_1_a1_legal_baseline_2021_census.py",
        "name": "A1 legal-baseline against 2019 EDs + 2021 census",
        "role": "Appendix C legal-baseline A1 reference.",
    },
    {
        "path": "analysis/scripts/v0_1_plan_b_rerun.py",
        "name": "Plan-B population rerun (2021 census / 2024 OSI / 2025 TBF)",
        "role": "Cross-basis robustness for A-family verdicts.",
    },
    {
        "path": "analysis/scripts/v0_1_rural_gap_dissection.py",
        "name": "Rural gap dissection",
        "role": "Smallest-10 majority/minority rural ED comparison.",
    },
    # B-family (partisan bias) core
    {
        "path": "analysis/scripts/v0_2_packing_cracking_analysis.py",
        "name": "v0_2 packing/cracking analysis (symmetric 3-map B2/B3/B4)",
        "role": "Efficiency gap, mean-median, seats@50/50, and declination on three maps.",
    },
    {
        "path": "analysis/scripts/v0_3_monte_carlo_ci.py",
        "name": "v0_3 Monte Carlo CI (B-family 2000-sample sensitivity)",
        "role": "Urban-weight + rural-baseline + per-hybrid jitter Monte Carlo CI.",
    },
    {
        "path": "analysis/scripts/v0_1_majority_symmetry_counter_test.py",
        "name": "Majority-symmetry counter-test",
        "role": "Edmonton zone + city-wide 4-way split counter-tests.",
    },
    {
        "path": "analysis/scripts/v0_1_marginal_seats_analysis.py",
        "name": "Marginal-seats + uniform-swing analysis",
        "role": "Per-ED margin + seat-flip enumeration.",
    },
    {
        "path": "analysis/scripts/v0_1_2015_cross_election.py",
        "name": "2015 cross-election extension",
        "role": "Extends RT3 to 2015 election via 2015-to-2019 crosswalk.",
    },
    {
        "path": "analysis/scripts/v0_1_cross_election_rural_baseline.py",
        "name": "Cross-election rural-baseline drift",
        "role": "Province-wide drift calibration across 2015/2019/2023.",
    },
    {
        "path": "analysis/scripts/v0_1_justification_tests.py",
        "name": "Justification tests (blended-crosswalk sanity)",
        "role": "Blended-crosswalk mechanical checks on B-family metrics.",
    },
    # MCMC
    {
        "path": "analysis/scripts/v0_1_mcmc_ensemble.py",
        "name": "10k ReCom ensemble (preliminary)",
        "role": "First MCMC ensemble run — 10,000 samples.",
    },
    {
        "path": "analysis/scripts/v0_1_mcmc_ensemble_100k.py",
        "name": "100k ReCom ensemble (publication-grade)",
        "role": "Primary 100k-sample ensemble.",
    },
    {
        "path": "analysis/scripts/v0_1_mcmc_full_coverage_rescore.py",
        "name": "Full-coverage MCMC rescore",
        "role": "Real-map scoring under 88-row crosswalk + polygon fallback.",
    },
    {
        "path": "analysis/scripts/v0_1_mcmc_full_coverage_rescore_100k.py",
        "name": "Full-coverage MCMC rescore (100k)",
        "role": "Rescore against 100k-sample ensemble.",
    },
    {
        "path": "analysis/scripts/v0_1_mcmc_full_coverage_rescore_v2.py",
        "name": "Full-coverage MCMC rescore v2 (spatial substrate)",
        "role": "Rescore using full-VA substrate and canonical DPGs.",
    },
    {
        "path": "analysis/scripts/v0_1_mcmc_multichain_ensemble.py",
        "name": "Multi-chain MCMC (3-seed R-hat)",
        "role": "Three independently-seeded ReCom chains + pooled + R-hat.",
    },
    # Chen-Rodden
    {
        "path": "analysis/scripts/v0_1_chen_rodden_alberta.py",
        "name": "Chen-Rodden Alberta validation (neutral-ensemble decomposition)",
        "role": "Validates Chen-Rodden direction prediction; reports mechanism correction.",
    },
    {
        "path": "analysis/scripts/v0_1_chen_rodden_decomposition.py",
        "name": "Chen-Rodden pairwise + absolute decomposition",
        "role": "Geography-vs-drawing decomposition against 100k ensemble.",
    },
    # Perturbation sensitivity
    {
        "path": "analysis/scripts/v0_1_dpg_perturbation_sensitivity.py",
        "name": "DPG perturbation sensitivity (flat ±500m)",
        "role": "Fifth-layer CI from DPG tracing uncertainty.",
    },
    {
        "path": "analysis/scripts/v0_1_dpg_perturbation_sensitivity_v2.py",
        "name": "DPG perturbation sensitivity (tier-aware)",
        "role": "Sixth-layer CI, tier-aware σ per canon_source.",
    },
    {
        "path": "analysis/scripts/v0_1_dpg_perturbation_sensitivity_v05.py",
        "name": "DPG perturbation sensitivity (v0_5 DA-anchored)",
        "role": "Seventh-layer CI on v0_5 DA-anchored DPG substrate.",
    },
    {
        "path": "analysis/scripts/v0_1_dpg_perturbation_writeup.py",
        "name": "DPG perturbation writeup generator",
        "role": "Writes up perturbation CI findings.",
    },
    # Compactness / geography
    {
        "path": "analysis/scripts/v0_1_csd_community_splits.py",
        "name": "CSD community-of-interest split analysis",
        "role": "Per-map CSD-level community-split counts.",
    },
    # 338 integration
    {
        "path": "analysis/scripts/v0_1_338canada_historical.py",
        "name": "338Canada historical-snapshot reallocation",
        "role": "77-snapshot historical stability probe.",
    },
    {
        "path": "analysis/scripts/v0_1_338canada_reallocate.py",
        "name": "338Canada reallocation (majority + minority)",
        "role": "338 per-riding scores mapped to 2026 EDs.",
    },
    {
        "path": "analysis/scripts/v0_1_338canada_scraper.py",
        "name": "338Canada scraper (87-seat per-riding)",
        "role": "Builds 338Canada per-riding frozen CSV.",
    },
    {
        "path": "analysis/scripts/v0_1_canadian_base_rate_compute.py",
        "name": "Canadian base-rate comparator compute",
        "role": "n=6 Canadian redistribution cycle asymmetry comparator.",
    },
    {
        "path": "analysis/scripts/v0_1_canadian_base_rate_recalibrate.py",
        "name": "Canadian base-rate recalibration (circular-inclusion fix)",
        "role": "Removes Alberta 2025-26 from its own comparator distribution.",
    },
    # Overlay + visuals + auxiliary
    {
        "path": "analysis/scripts/v0_1_build_overlay_figures.py",
        "name": "Overlay figures v1",
        "role": "Commission-vs-canonical overlay figure generation.",
    },
    {
        "path": "analysis/scripts/v0_1_build_overlay_figures_v2.py",
        "name": "Overlay figures v2",
        "role": "Revised overlay figure set.",
    },
    {
        "path": "analysis/scripts/v0_1_build_article_figures_v3.py",
        "name": "Article figures v3",
        "role": "Report-grade figure assembly.",
    },
    {
        "path": "analysis/scripts/v0_1_approximate_shape_analysis.py",
        "name": "Approximate shape analysis",
        "role": "Scores approximate majority polygons against commission reference.",
    },
    {
        "path": "analysis/scripts/v0_1_max_dpi_extract.py",
        "name": "Max-DPI extraction from commission PDF",
        "role": "Native-DPI extraction of commission map rasters.",
    },
    {
        "path": "analysis/scripts/v0_1_max_dpi_inspect.py",
        "name": "Max-DPI inspection",
        "role": "Inspects bit-depth + raster provenance of extracted images.",
    },
    {
        "path": "analysis/scripts/v0_1_tier_c_crops.py",
        "name": "Tier-C crop generation",
        "role": "Commission PDF → Tier-C crop images for transcription.",
    },
    {
        "path": "analysis/scripts/v0_1_track_l_drift.py",
        "name": "Track-L population-drift analysis",
        "role": "Population drift within audit window.",
    },
    {
        "path": "analysis/scripts/v0_1_url_archival.py",
        "name": "URL archival (Wayback + archive.ph)",
        "role": "Produces FROZEN_MANIFEST Wayback columns.",
    },
    {
        "path": "analysis/scripts/v0_1_airdrie_overlap_diagnostic.py",
        "name": "Airdrie overlap diagnostic",
        "role": "Per-ED Airdrie split diagnostics.",
    },
    {
        "path": "analysis/scripts/v0_1_edmonton_beaumont_polygon.py",
        "name": "Edmonton-Beaumont polygon trace",
        "role": "Manual polygon trace for Edmonton-Beaumont.",
    },
    {
        "path": "analysis/scripts/v0_1_edmonton_beaumont_split.py",
        "name": "Edmonton-Beaumont split",
        "role": "Splits Beaumont CSD from Edmonton core.",
    },
    {
        "path": "analysis/scripts/v0_1_overlap_zone_diagnostic.py",
        "name": "Overlap-zone diagnostic",
        "role": "Per-pair overlap diagnostic for topology cleanup.",
    },
    {
        "path": "analysis/scripts/v0_1_submission_ocr.py",
        "name": "Submission OCR",
        "role": "OCR of 88 image-only submission PDFs.",
    },
    {
        "path": "analysis/scripts/v0_1_submission_ocr_analyze.py",
        "name": "Submission OCR analyze",
        "role": "Post-OCR keyword extraction.",
    },
    {
        "path": "analysis/scripts/submission_search.py",
        "name": "Submission archive keyword search",
        "role": "Produces submission_search_dataset.csv with per-configuration counts.",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v6_processors.py",
        "name": "Shape refinement v6 processors",
        "role": "v6 processing helpers.",
    },
    {
        "path": "analysis/scripts/v0_1_shape_refinement_v6_writer.py",
        "name": "Shape refinement v6 writer",
        "role": "v6 GPKG writer.",
    },
    # Report build
    {
        "path": "analysis/scripts/build_academic_html.py",
        "name": "Build academic HTML",
        "role": "Renders report_academic.md to HTML.",
    },
    {
        "path": "analysis/scripts/build_cover.py",
        "name": "Build cover page",
        "role": "Cover art assembly.",
    },
    {
        "path": "analysis/scripts/build_pdf.py",
        "name": "Build PDF",
        "role": "PDF assembly from academic HTML.",
    },
    {
        "path": "analysis/scripts/check_voice_and_readability.py",
        "name": "Voice and readability checker",
        "role": "Editorial-pass automation.",
    },
]


# ---------------------------------------------------------------------------
# L3 — Inference / finding nodes (from report_academic.md §5.1–§5.9)
# ---------------------------------------------------------------------------

# Each L3 node lists its evidentiary upstream nodes as `evidence` (IDs of any
# layer). The edge `type` is "required" if removing the upstream node
# eliminates the finding; "corroborating" if the finding has another independent
# path; "validating" if the upstream is a gate. Each edge may carry a
# `sensitivity` note.

L3_FINDINGS: List[Dict[str, Any]] = [
    # §5.1 Population equality
    {
        "id": "L3:finding.a1_mad_majority_3180",
        "report_section": "5.1.1",
        "name": "A1 — Majority 2026 MAD = 3,180",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "population value from commission variance tables"),
            ("L2:electoral_forensics_population", "required", "computes MAD from commission populations"),
        ],
    },
    {
        "id": "L3:finding.a1_mad_minority_4707",
        "report_section": "5.1.1",
        "name": "A1 — Minority 2026 MAD = 4,707 (48% wider than majority)",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "population value from commission variance tables"),
            ("L2:electoral_forensics_population", "required", "computes MAD from commission populations"),
        ],
    },
    {
        "id": "L3:finding.a1_positive_tail_minority",
        "report_section": "5.1.1",
        "name": "A1 — Minority has 5 EDs above +15% from mean (majority has 0)",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "variance tables"),
            ("L2:electoral_forensics_population", "required", "positive-tail counts"),
        ],
    },
    {
        "id": "L3:finding.a1_plan_b_robustness",
        "report_section": "5.1.1",
        "name": "A1 — All §5.1 verdicts identical under 2021 census / 2024 OSI / 2025 TBF bases",
        "evidence": [
            ("L0:data.2021_da_populations", "corroborating", "direct 2021 census path"),
            ("L0:data.tbf_population_estimates", "corroborating", "2025 TBF estimate path"),
            ("L0:data.statscan_1710000901", "corroborating", "Table 17-10-0009 path"),
            ("L2:v0_1_plan_b_rerun", "required", "cross-basis robustness check"),
        ],
    },
    {
        "id": "L3:finding.a2_calgary_majority_0_36",
        "report_section": "5.1.2",
        "name": "A2 — Majority Calgary Zone A-vs-B gap = +0.36%",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "per-ED population"),
            ("L2:electoral_forensics_population", "required", "zone classifier"),
        ],
    },
    {
        "id": "L3:finding.a2_calgary_minority_12_20",
        "report_section": "5.1.2",
        "name": "A2 — Minority Calgary Zone A-vs-B gap = +12.20%",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "per-ED population"),
            ("L2:electoral_forensics_population", "required", "zone classifier"),
        ],
    },
    {
        "id": "L3:finding.a2_calgary_minority_robustness_7_71",
        "report_section": "5.1.2",
        "name": "A2 — Minority Calgary gap 7.71% under 2023-winner-based rule (G4 robustness)",
        "evidence": [
            ("L0:data.commission_published_populations", "corroborating", "geographic-rule path"),
            ("L0:data.2023_statement_of_vote", "required", "2023 winners per ED"),
            ("L2:electoral_forensics_population", "required", "dual-rule classifier"),
        ],
    },
    {
        "id": "L3:finding.a2b_rural_minority_smaller",
        "report_section": "5.1.3",
        "name": "A2b — Minority rest-of-province mean 50,336 (3.9% lower than majority)",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "regional breakdown"),
            ("L2:electoral_forensics_population", "required", "urban-rural classifier"),
        ],
    },
    {
        "id": "L3:finding.a3_s15_2_all_pass",
        "report_section": "5.1.4",
        "name": "A3 — All 6 s.15(2) invocations pass the 3-of-5 statutory threshold under corrected thresholds",
        "evidence": [
            ("L0:data.electoral_boundaries_act", "required", "statutory criteria"),
            ("L0:data.commission_final_report_2026", "required", "invocation claims"),
            ("L0:data.2021_csd_populations", "corroborating", "town population check"),
        ],
    },
    {
        "id": "L3:finding.a3_rmh_banff_engineered",
        "report_section": "5.1.4/5.3.3",
        "name": "Engineered-boundary signature: RMH-Banff Park (park extension chosen over populated alternatives)",
        "evidence": [
            ("L0:data.commission_map_pngs", "required", "visible park-land extension"),
            ("L0:data.commission_final_report_2026", "required", "chair p. 352 rationale"),
            ("L0:data.rizzo_rizzo_1998", "validating", "purposive interpretation frame"),
        ],
    },
    # §5.2 Partisan bias
    {
        "id": "L3:finding.b2_eg_2019_minus_2_64",
        "report_section": "5.2.1",
        "name": "B2 — 2019 baseline efficiency gap = −2.64%",
        "evidence": [
            ("L0:data.2019_election_results", "required", "2019 vote data + 87-seat attribution substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "EG computation"),
        ],
    },
    {
        "id": "L3:finding.b2_eg_majority_minus_1_29",
        "report_section": "5.2.1",
        "name": "B2 — Majority 2026 efficiency gap = −1.29% (central w=0.85)",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_majority_hybrid", "required", "blended crosswalk substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "EG computation"),
        ],
    },
    {
        "id": "L3:finding.b2_eg_minority_minus_2_71",
        "report_section": "5.2.1",
        "name": "B2 — Minority 2026 efficiency gap = −2.71% (central w=0.85)",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "blended crosswalk substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "EG computation"),
        ],
    },
    {
        "id": "L3:finding.b2_asymmetry_minus_1_42",
        "report_section": "5.2.1",
        "name": "B2 — Minority-majority EG asymmetry = −1.42 pp at central weight (crosswalk reading)",
        "evidence": [
            ("L1:constructed.crosswalk_majority_hybrid", "required", "majority substrate"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "minority substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "asymmetry calc"),
        ],
    },
    {
        "id": "L3:finding.b2_eg_sensitivity_range_0_49_1_50",
        "report_section": "5.2.2",
        "name": "B2 — Sensitivity range 0.49–1.50 pp across urban weights 0.60-0.90",
        "evidence": [
            ("L2:v0_3_monte_carlo_ci", "required", "weight sweep"),
            ("L1:constructed.crosswalk_majority_hybrid", "required", "majority substrate"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "minority substrate"),
        ],
    },
    {
        "id": "L3:finding.b2_canadian_base_rate_67th",
        "report_section": "5.2.1",
        "name": "Canadian redistribution base-rate — Alberta 2025-26 at 67th percentile of n=6 comparator",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "Alberta 2025-26 is one of the comparator cycles (from commission final report)"),
            ("L1:constructed.canadian_base_rate", "required", "comparator distribution"),
            ("L2:v0_1_canadian_base_rate_recalibrate", "required", "circular-inclusion fix"),
        ],
    },
    {
        "id": "L3:finding.b3_mean_median_majority",
        "report_section": "5.2.1",
        "name": "B3 — Majority 2026 mean-median gap = −0.16 pp",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_majority_hybrid", "required", "substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "MM computation"),
        ],
    },
    {
        "id": "L3:finding.b3_mean_median_minority",
        "report_section": "5.2.1",
        "name": "B3 — Minority 2026 mean-median gap = −0.34 pp",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "MM computation"),
        ],
    },
    {
        "id": "L3:finding.b4_seats_at_50_majority",
        "report_section": "5.2.1",
        "name": "B4 — Majority 2026 NDP seats at 50/50 uniform swing = 44",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_majority_hybrid", "required", "substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "uniform-swing calc"),
        ],
    },
    {
        "id": "L3:finding.b4_seats_at_50_minority",
        "report_section": "5.2.1",
        "name": "B4 — Minority 2026 NDP seats at 50/50 = 42",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "uniform-swing calc"),
        ],
    },
    {
        "id": "L3:finding.b6_declination_minority_lowest",
        "report_section": "5.2.4",
        "name": "B6 — Declination shows minority is least UCP-favourable (disagrees with B2/B3/B4)",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote data"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "declination calc"),
        ],
    },
    {
        "id": "L3:finding.b2_monte_carlo_ci_crosses_zero",
        "report_section": "5.2.3",
        "name": "B2 — 95% Monte Carlo CI [−3.04, +0.76] pp (crosses zero); 90.5% same sign",
        "evidence": [
            ("L2:v0_3_monte_carlo_ci", "required", "2000-sample sweep"),
            ("L1:constructed.crosswalk_majority_hybrid", "required", "substrate"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "substrate"),
        ],
    },
    {
        "id": "L3:finding.b2_reversal_2019_votes",
        "report_section": "5.2.3",
        "name": "B2 — Direction flips to +0.75 pp under 2019 votes; near-zero under 2015 votes",
        "evidence": [
            ("L0:data.2019_election_results", "required", "2019 attribution"),
            ("L0:data.2015_election_results", "required", "2015 attribution"),
            ("L0:data.commission_rationales_text", "required", "2015-to-2019 crosswalk (for 2015 extension)"),
            ("L2:v0_1_2015_cross_election", "required", "2015 extension"),
        ],
    },
    {
        "id": "L3:finding.b_338_direction_state_dependent",
        "report_section": "5.2.3",
        "name": "B-family — 1-seat gap direction is state-dependent (UCP-landslide flips it)",
        "evidence": [
            ("L0:data.338canada_snapshots", "required", "77-snapshot time series"),
            ("L0:data.338_historical_snapshots_dir", "required", "pre-2023 reallocation"),
            ("L2:v0_1_338canada_historical", "required", "reallocation pipeline"),
            ("L1:constructed.338canada_reallocated", "required", "reallocated scores"),
        ],
    },
    {
        "id": "L3:finding.b_byelection_assessment",
        "report_section": "5.2.3",
        "name": "B — Byelection coverage too sparse + candidate-specific to enter RT3 (6 of 87 EDs)",
        "evidence": [
            ("L0:data.byelections_2019_2026", "required", "byelection results"),
        ],
    },
    {
        "id": "L3:finding.b2_chen_rodden_direction_validated",
        "report_section": "5.2.5",
        "name": "Chen-Rodden direction prediction validates for Alberta (2019 baseline at centre of neutral distribution)",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "vote substrate"),
            ("L2:v0_1_chen_rodden_alberta", "required", "validation simulation"),
            ("L1:constructed.mcmc_ensemble_100k", "corroborating", "alternate neutral-ensemble path"),
        ],
    },
    {
        "id": "L3:finding.b2_chen_rodden_mechanism_fails",
        "report_section": "5.2.5",
        "name": "Chen-Rodden mechanism prediction fails: UCP is the more-packed party (15.9% vs 9.3% surplus)",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "per-ED vote data"),
            ("L2:v0_1_chen_rodden_alberta", "required", "decomposition"),
        ],
    },
    {
        "id": "L3:finding.b2_chen_rodden_pairwise_100_drawing",
        "report_section": "5.2.5",
        "name": "Chen-Rodden pairwise decomposition — minority-vs-majority gap is 100% drawing, 0% geography",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble median baseline"),
            ("L1:constructed.mcmc_real_map_scores", "required", "real-map scores"),
            ("L2:v0_1_chen_rodden_decomposition", "required", "decomposition script"),
        ],
    },
    {
        "id": "L3:finding.b2_chen_rodden_absolute_draw_components",
        "report_section": "5.2.5",
        "name": "Absolute Chen-Rodden EG drawing components: 2019 −4.12, Majority −3.81, Minority +0.34 pp",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble median"),
            ("L1:constructed.mcmc_real_map_scores", "required", "real-map scores"),
            ("L2:v0_1_chen_rodden_decomposition", "required", "absolute decomposition"),
            ("L1:constructed.chen_rodden", "required", "absolute decomposition JSON output"),
        ],
    },
    {
        "id": "L3:finding.b2_chen_rodden_minority_seats_5_75",
        "report_section": "5.2.5",
        "name": "Minority adds +5.75 pp NDP responsiveness at 50/50 via asymmetric drawing",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble baseline"),
            ("L2:v0_1_chen_rodden_decomposition", "required", "seats-at-50 drawing component"),
        ],
    },
    {
        "id": "L3:finding.b_marginal_seats_1_5pp_swing",
        "report_section": "5.2.6",
        "name": "1.5 pp uniform swing flips 6 seats toward UCP + 4 toward NDP on 2023 results",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "per-ED margins"),
            ("L2:v0_1_marginal_seats_analysis", "required", "uniform-swing enumeration"),
            ("L1:constructed.marginal_seats", "required", "marginal-seats outputs"),
        ],
    },
    {
        "id": "L3:finding.b_marginal_seats_14_of_87",
        "report_section": "5.2.6",
        "name": "14 of 87 ridings within 3 pp two-party margin in 2023",
        "evidence": [
            ("L0:data.2023_statement_of_vote", "required", "per-ED margins"),
            ("L2:v0_1_marginal_seats_analysis", "required", "enumeration"),
        ],
    },
    # §5.2.7 multi-layer sensitivity
    {
        "id": "L3:finding.b2_crosswalk_reading",
        "report_section": "5.2.7",
        "name": "Crosswalk reading — minority-majority asymmetry = −1.42 pp (minority more UCP-favourable)",
        "evidence": [
            ("L1:constructed.crosswalk_majority_hybrid", "required", "majority substrate"),
            ("L1:constructed.crosswalk_minority_hybrid", "required", "minority substrate"),
            ("L2:v0_2_packing_cracking_analysis", "required", "metric compute"),
        ],
    },
    {
        "id": "L3:finding.b2_spatial_reading_positive_4_15",
        "report_section": "5.2.7",
        "name": "High-resolution spatial reading — asymmetry = +4.15 pp (minority more NDP-favourable)",
        "evidence": [
            ("L1:constructed.dpg_v0_1_canonical", "required", "DPG geometry"),
            ("L1:constructed.va_substrate_full", "required", "full-VA substrate"),
            ("L2:v0_1_mcmc_full_coverage_rescore_v2", "required", "spatial rescore"),
        ],
    },
    {
        "id": "L3:finding.b2_maup_v1_topology_artefact",
        "report_section": "5.2.7",
        "name": "MAUP-v1 −1.12 pp → +3.35 pp under topology cleanup (artefact exposed)",
        "evidence": [
            ("L1:constructed.phase4c_votes_maup_v1", "required", "MAUP-v1 substrate"),
            ("L1:constructed.phase4c_votes_maup_v2", "required", "MAUP-v2 substrate"),
            ("L2:v0_1_topology_cleanup", "required", "cleanup"),
            ("L2:v0_1_phase_4c_va_attribution_maup_v2", "required", "re-run"),
        ],
    },
    {
        "id": "L3:finding.b2_topology_cleanup_overlap_km2",
        "report_section": "5.2.7",
        "name": "Topology cleanup — 2,754 km² majority / 16,734 km² minority inter-ED overlap (96 pairs)",
        "evidence": [
            ("L0:data.commission_map_pngs", "required", "source PNGs traced into v0_1 DPG"),
            ("L1:constructed.dpg_v0_1_canonical", "required", "input DPG"),
            ("L1:constructed.topology_cleanup_log", "required", "overlap log"),
            ("L2:v0_1_topology_cleanup", "required", "detection"),
        ],
    },
    {
        "id": "L3:finding.b2_perturbation_flat_ci",
        "report_section": "5.2.7",
        "name": "DPG perturbation flat-±500m 90% CI [+1.69, +7.67] pp (200/200 positive)",
        "evidence": [
            ("L1:constructed.dpg_v0_2_topoclean", "required", "substrate"),
            ("L1:constructed.dpg_perturbation_flat", "required", "perturbation samples"),
            ("L2:v0_1_dpg_perturbation_sensitivity", "required", "flat-σ pipeline"),
        ],
    },
    {
        "id": "L3:finding.b2_perturbation_tiered_ci",
        "report_section": "5.2.7",
        "name": "DPG perturbation tier-aware 90% CI [+2.76, +7.62] pp (200/200 positive)",
        "evidence": [
            ("L1:constructed.dpg_v0_2_topoclean", "required", "substrate"),
            ("L1:constructed.dpg_perturbation_tiered", "required", "tiered samples"),
            ("L2:v0_1_dpg_perturbation_sensitivity_v2", "required", "tiered-σ pipeline"),
        ],
    },
    {
        "id": "L3:finding.b2_perturbation_tight_ci",
        "report_section": "5.2.7",
        "name": "DPG perturbation tight tier-aware 90% CI [+2.89, +6.48] pp",
        "evidence": [
            ("L1:constructed.dpg_perturbation_tight", "required", "tight samples"),
            ("L2:v0_1_dpg_perturbation_sensitivity_v2", "required", "tight-σ run"),
        ],
    },
    {
        "id": "L3:finding.b2_v05_signflip",
        "report_section": "5.2.7",
        "name": "v0_5 DA-anchored MAUP rerun — sign flip to −3.64 pp (DPG-construction dominant)",
        "evidence": [
            ("L1:constructed.dpg_v0_5_da_anchored", "required", "v0_5 DPG"),
            ("L1:constructed.phase4c_votes_maup_v05", "required", "v0_5 substrate"),
            ("L1:constructed.dpg_perturbation_v05", "corroborating", "v0_5 perturbation"),
            ("L2:v0_1_phase_4c_va_attribution_maup_v3_v05", "required", "rerun pipeline"),
            ("L2:v0_1_dpg_perturbation_sensitivity_v05", "required", "v0_5 CI"),
        ],
    },
    {
        "id": "L3:finding.b2_dpi_ceiling",
        "report_section": "5.2.7",
        "name": "Commission-map DPI ceiling — native 300-388 DPI is bottleneck, not scan resolution",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "PDF raster analysis"),
            ("L1:constructed.max_dpi_extract", "required", "extraction audit"),
            ("L2:v0_1_max_dpi_extract", "required", "extraction"),
            ("L2:v0_1_max_dpi_inspect", "required", "inspection"),
        ],
    },
    {
        "id": "L3:finding.b2_core_margin_insulation",
        "report_section": "5.2.7",
        "name": "Core-vs-Margin insulation test — disagreement is systematic, not a swing-VA artefact",
        "evidence": [
            ("L1:constructed.va_substrate_full", "required", "VA substrate"),
            ("L1:constructed.dpg_v0_1_canonical", "required", "DPG"),
            ("L2:v0_1_mcmc_full_coverage_rescore_v2", "required", "Core/Margin tabulation"),
        ],
    },
    # §5.3 signature detection
    {
        "id": "L3:finding.packing_minority_calgary_zone_a",
        "report_section": "5.3.1",
        "name": "Packing signature detected — Minority Calgary Zone A (P1/P2/P3 pass)",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "population sizes"),
            ("L0:data.2023_statement_of_vote", "required", "NDP winners + margins"),
            ("L2:electoral_forensics_population", "required", "zone classifier"),
            ("L2:v0_2_packing_cracking_analysis", "required", "P-criteria application"),
        ],
    },
    {
        "id": "L3:finding.packing_not_majority_calgary",
        "report_section": "5.3.1",
        "name": "Packing signature NOT detected on majority Calgary (P1 fails)",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "population sizes"),
            ("L2:electoral_forensics_population", "required", "zone classifier"),
            ("L2:v0_2_packing_cracking_analysis", "required", "P-criteria application"),
        ],
    },
    {
        "id": "L3:finding.cracking_minority_airdrie",
        "report_section": "5.3.2",
        "name": "Cracking signature detected — Minority Airdrie 4-way split (C1/C2/C3 pass)",
        "evidence": [
            ("L0:data.commission_map_pngs", "required", "4-district split visually"),
            ("L0:data.commission_final_report_2026", "required", "4-district naming"),
            ("L0:data.2021_csd_populations", "required", "Airdrie population"),
            ("L2:v0_2_packing_cracking_analysis", "required", "C-criteria application"),
        ],
    },
    {
        "id": "L3:finding.cracking_cochrane_c3_fails",
        "report_section": "5.3.2",
        "name": "Cochrane cracking-adjacent: C1/C2 pass, C3 fails (pattern but not formal signature)",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "Cochrane-Calgary pairing"),
            ("L0:data.2021_csd_populations", "required", "Cochrane population"),
            ("L2:v0_2_packing_cracking_analysis", "required", "C-criteria application"),
        ],
    },
    {
        "id": "L3:finding.signatures_summary_three_minority",
        "report_section": "5.3.4",
        "name": "Three formal signatures, all concentrated in minority map (majority detects zero)",
        "evidence": [
            ("L3:finding.packing_minority_calgary_zone_a", "required", "packing signature"),
            ("L3:finding.cracking_minority_airdrie", "required", "cracking signature"),
            ("L3:finding.a3_rmh_banff_engineered", "required", "engineered-boundary signature"),
        ],
    },
    # §5.4 MCMC
    {
        "id": "L3:finding.mcmc_minority_mean_median_p95",
        "report_section": "5.4",
        "name": "Minority 2026 at p95.35 on mean-median (UCP-favoured tail, ESS-downgraded)",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble distribution"),
            ("L1:constructed.mcmc_real_map_scores", "required", "real-map scores"),
            ("L1:constructed.crosswalk_minority_full", "required", "crosswalk fallback"),
            ("L2:v0_1_mcmc_full_coverage_rescore_100k", "required", "rescore"),
        ],
    },
    {
        "id": "L3:finding.mcmc_minority_declination_p1_6",
        "report_section": "5.4",
        "name": "Minority 2026 at p1.6 on declination (NDP-favoured tail)",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble distribution"),
            ("L1:constructed.mcmc_real_map_scores", "required", "real-map scores"),
            ("L2:v0_1_mcmc_full_coverage_rescore_100k", "required", "rescore"),
        ],
    },
    {
        "id": "L3:finding.mcmc_structural_floor",
        "report_section": "5.4",
        "name": "Ensemble median mean-median = −0.019, seats-at-50/50 = 0.448 — structural UCP floor",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "ensemble distribution"),
            ("L2:v0_1_mcmc_ensemble_100k", "required", "ensemble generation"),
        ],
    },
    {
        "id": "L3:finding.mcmc_multichain_rhat",
        "report_section": "5.4",
        "name": "Multi-chain R-hat < 1.01 on 3/4 metrics, 1.0099 on mean-median (strict publication-grade)",
        "evidence": [
            ("L1:constructed.mcmc_multichain", "required", "R-hat JSON"),
            ("L2:v0_1_mcmc_multichain_ensemble", "required", "3-chain run"),
        ],
    },
    {
        "id": "L3:finding.mcmc_ess_150_downgrade",
        "report_section": "5.4",
        "name": "Tail claims downgraded — ESS ~150 per metric bounds p100/p1.6 to p95.35/p2.5",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_100k", "required", "convergence diagnostics"),
            ("L2:v0_1_mcmc_ensemble_100k", "required", "ensemble"),
        ],
    },
    {
        "id": "L3:finding.mcmc_10k_flag_retraction",
        "report_section": "5.4",
        "name": "10k-era 2019 mean-median + Majority seats-at-50/50 flags retracted under full-coverage rescore",
        "evidence": [
            ("L1:constructed.mcmc_ensemble_10k", "required", "preliminary baseline"),
            ("L1:constructed.mcmc_ensemble_100k", "required", "full-coverage ensemble"),
            ("L2:v0_1_mcmc_full_coverage_rescore_100k", "validating", "re-run retraction gate"),
        ],
    },
    # §5.5 pre-registered checklist
    {
        "id": "L3:finding.checklist_minority_3_sig_plus_mcmc",
        "report_section": "5.5",
        "name": "Pre-registered checklist — minority has 3 signatures + MCMC outlier; majority has 0",
        "evidence": [
            ("L3:finding.signatures_summary_three_minority", "required", "3 formal signatures"),
            ("L3:finding.mcmc_minority_mean_median_p95", "required", "MCMC outlier flag"),
            ("L3:finding.mcmc_minority_declination_p1_6", "required", "MCMC outlier flag"),
        ],
    },
    {
        "id": "L3:finding.checklist_neither_crosses_sure_sign",
        "report_section": "5.5",
        "name": "Neither 2026 map crosses the sure-sign-gerrymander bar",
        "evidence": [
            ("L3:finding.signatures_summary_three_minority", "required", "signature count"),
            ("L3:finding.mcmc_minority_declination_p1_6", "corroborating", "outlier"),
        ],
    },
    # §5.6 symmetry-of-test-selection
    {
        "id": "L3:finding.symmetry_edmonton_no_zone_gap",
        "report_section": "5.6",
        "name": "Symmetry counter-test 1 — Edmonton zone gap (+2.0 pp maj / +1.4 pp min) << Calgary 12.2 pp",
        "evidence": [
            ("L0:data.commission_published_populations", "required", "zone populations"),
            ("L1:constructed.symmetry_counter_test", "required", "counter-test CSV"),
            ("L2:v0_1_majority_symmetry_counter_test", "required", "counter-test script"),
        ],
    },
    {
        "id": "L3:finding.symmetry_lethbridge_red_deer_4way",
        "report_section": "5.6",
        "name": "Symmetry counter-test 2 — Lethbridge + Red Deer 4-way splits found in minority, 2-way in majority",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "city-to-ED bindings"),
            ("L0:data.2021_csd_populations", "required", "city population threshold"),
            ("L1:constructed.symmetry_counter_test", "required", "counter-test CSV"),
            ("L2:v0_1_majority_symmetry_counter_test", "required", "counter-test script"),
        ],
    },
    # §5.7 stress-test
    {
        "id": "L3:finding.rt2_b_family_three_of_four",
        "report_section": "5.7",
        "name": "RT2 — B2/B3/B4 agree on direction; B6 declination opposes (mixed pass)",
        "evidence": [
            ("L3:finding.b2_eg_asymmetry_minus_1_42", "corroborating", "B2"),
            ("L3:finding.b3_mean_median_minority", "corroborating", "B3"),
            ("L3:finding.b4_seats_at_50_minority", "corroborating", "B4"),
            ("L3:finding.b6_declination_minority_lowest", "corroborating", "B6"),
        ],
    },
    {
        "id": "L3:finding.rt7_flag_pass_minority_only",
        "report_section": "5.7",
        "name": "RT7 — MCMC outlier flag-pass on minority only",
        "evidence": [
            ("L3:finding.mcmc_minority_mean_median_p95", "required", "MCMC flag"),
            ("L3:finding.mcmc_minority_declination_p1_6", "required", "MCMC flag"),
        ],
    },
    # §5.8 geographic coherence
    {
        "id": "L3:finding.c_visual_three_anomalies_minority",
        "report_section": "5.8.1/5.8.2",
        "name": "Three visible spatial anomalies on minority (Nolan-Hill-Cochrane, RMH-Banff Park, Olds-TH-D)",
        "evidence": [
            ("L0:data.commission_map_pngs", "required", "visual inspection"),
            ("L0:data.commission_final_report_2026", "corroborating", "chair-flagged list"),
        ],
    },
    {
        "id": "L3:finding.c_majority_calgary_symmetric",
        "report_section": "5.8.3",
        "name": "Majority Calgary hybrids — no visible anomaly (symmetric check)",
        "evidence": [
            ("L0:data.commission_map_pngs", "required", "majority Calgary image"),
        ],
    },
    {
        "id": "L3:finding.c4_csd_splits_null_symmetric",
        "report_section": "5.8.4",
        "name": "CSD-level split count — null symmetric across three maps (40-66 splits each)",
        "evidence": [
            ("L0:data.2021_csds_gpkg", "required", "CSD geometry"),
            ("L0:data.2019_ed_shapefile", "required", "2019 overlay"),
            ("L1:constructed.csd_splits", "required", "split summary"),
            ("L2:v0_1_csd_community_splits", "required", "overlay script"),
        ],
    },
    {
        "id": "L3:finding.c5_municipal_anchoring_asymmetry",
        "report_section": "5.8.5",
        "name": "Municipal-anchoring — majority 71.0% vs minority 14.5% (4.9× asymmetry)",
        "evidence": [
            ("L0:data.2021_csds_gpkg", "required", "CSD reference"),
            ("L1:constructed.dpg_v0_2_topoclean", "required", "input DPG"),
            ("L1:constructed.dpg_v0_4_municipal", "required", "anchored DPG"),
            ("L1:constructed.municipal_anchoring_summary", "required", "anchoring summary"),
            ("L2:v0_1_municipal_anchoring", "required", "anchoring pipeline"),
        ],
    },
    {
        "id": "L3:finding.c5_da_anchoring_extension",
        "report_section": "5.8.5",
        "name": "DA-anchoring extension — combined 79.6% majority vs 16.5% minority (5.1× asymmetry preserved)",
        "evidence": [
            ("L0:data.2021_das_gpkg", "required", "DA reference"),
            ("L1:constructed.dpg_v0_4_municipal", "required", "municipal-anchored input"),
            ("L1:constructed.dpg_v0_5_da_anchored", "required", "DA-anchored DPG"),
            ("L1:constructed.da_anchoring_summary", "required", "anchoring summary"),
            ("L2:v0_1_da_boundary_anchoring", "required", "pipeline"),
        ],
    },
    {
        "id": "L3:finding.c_shared_schools_refuted",
        "report_section": "5.8.5",
        "name": "Shared-schools community-of-interest claim refuted (R5 + R11); 20 of 21 minority hybrids cross school-division boundaries",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "rationale text"),
            ("L0:data.school_division_boundaries", "required", "school-district reference"),
        ],
    },
    {
        "id": "L3:finding.c_cochrane_commuter_partial",
        "report_section": "5.8.5",
        "name": "Cochrane commuter-tie — partial support (35.8% commute to Calgary CY; sub-neighbourhood not testable)",
        "evidence": [
            ("L0:data.cochrane_journey_to_work", "required", "STC98-10-0459"),
        ],
    },
    # §5.9 procedural
    {
        "id": "L3:finding.d_commission_3_2_split",
        "report_section": "5.9.1",
        "name": "Commission tabled divided final report (3-2, chair + opposition-nominated majority)",
        "evidence": [
            ("L0:data.commission_final_report_2026", "required", "commission record"),
        ],
    },
    {
        "id": "L3:finding.d_motion_19_passed",
        "report_section": "5.9.2",
        "name": "Motion 19 passed 44-36 on April 16, 2026 — Select Committee established, no public hearings on draft",
        "evidence": [
            ("L0:data.news_coverage_april_2026", "required", "news record"),
        ],
    },
    {
        "id": "L3:finding.d_r5_chair_only_not_majority",
        "report_section": "5.9.2",
        "name": "R5 is chair Miller's personal recommendation, not commission-majority collective",
        "evidence": [
            ("L0:data.commission_r5_addendum", "required", "R5 text"),
            ("L0:data.news_coverage_april_2026", "corroborating", "Clark social-media confirmation"),
        ],
    },
    {
        "id": "L3:finding.d_motion_19_most_gov_controlled",
        "report_section": "5.9.3",
        "name": "April 16 action is most government-controlled among 3 Canadian comparator cases",
        "evidence": [
            ("L0:data.news_coverage_april_2026", "required", "April 16 description"),
            ("L0:data.commission_final_report_2026", "required", "commission vs government framing"),
        ],
    },
    {
        "id": "L3:finding.d2_chair_claim_partially_refuted",
        "report_section": "5.9.4",
        "name": "Chair's 'no public support' Appendix C claim partially refuted (RMH-Banff, ODH, Chestermere)",
        "evidence": [
            ("L0:data.submission_archive", "required", "submission text"),
            ("L1:constructed.submission_search_results", "required", "search dataset"),
            ("L0:data.commission_final_report_2026", "required", "chair Appendix C claim"),
        ],
    },
    {
        "id": "L3:finding.d2_airdrie_nolan_hill_no_support",
        "report_section": "5.9.4",
        "name": "Chair claim stands for Airdrie 4-way + Nolan-Hill-Cochrane (no public support)",
        "evidence": [
            ("L0:data.submission_archive", "required", "submission text"),
            ("L1:constructed.submission_search_results", "required", "search dataset"),
        ],
    },
    {
        "id": "L3:finding.d5_effective_representation_not_adjudicated",
        "report_section": "5.9.5",
        "name": "Reference re Saskatchewan effective-representation frame set out but not adjudicated",
        "evidence": [
            ("L0:data.ref_saskatchewan_1991", "required", "case law"),
        ],
    },
    # Cross-cutting synthesis
    {
        "id": "L3:finding.synthesis_six_dimensions",
        "report_section": "6",
        "name": "Synthesis — six independent dimensions point same direction (minority more UCP-favorable)",
        "evidence": [
            ("L3:finding.a1_mad_minority_4707", "corroborating", "population MAD"),
            ("L3:finding.a2_calgary_minority_12_20", "corroborating", "Calgary zone"),
            ("L3:finding.a2b_rural_minority_smaller", "corroborating", "rural mean"),
            ("L3:finding.b2_asymmetry_minus_1_42", "corroborating", "partisan bias (crosswalk)"),
            ("L3:finding.signatures_summary_three_minority", "corroborating", "signature detection"),
            ("L3:finding.c_visual_three_anomalies_minority", "corroborating", "spatial anomalies"),
            ("L3:finding.c5_municipal_anchoring_asymmetry", "corroborating", "municipal anchoring"),
            ("L3:finding.d_motion_19_most_gov_controlled", "corroborating", "procedural"),
        ],
    },
]


# ---------------------------------------------------------------------------
# Script header parsing
# ---------------------------------------------------------------------------

_GLOB_RE = re.compile(r"\{[^}]*\}")


def _expand_braces(path: str) -> List[str]:
    """Expand ``foo_{a,b}.csv`` into two strings."""
    match = _GLOB_RE.search(path)
    if not match:
        return [path]
    inner = match.group(0)[1:-1]
    parts = [p.strip() for p in inner.split(",")]
    prefix, suffix = path[: match.start()], path[match.end() :]
    out: List[str] = []
    for p in parts:
        out.extend(_expand_braces(prefix + p + suffix))
    return out


def parse_headers(script_path: Path) -> Tuple[List[str], List[str]]:
    """Extract Forward / Backward listings from a script docstring.

    Returns ``(forwards, backwards)``. Each entry is a path string relative
    to the repo root (``{...}`` braces expanded). Comments on the line (after
    two spaces) are stripped.
    """
    try:
        text = script_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ([], [])
    # Find the first docstring — loose but adequate for the audit's scripts.
    m = re.search(r'"""(.+?)"""', text, re.DOTALL)
    if not m:
        return ([], [])
    doc = m.group(1)
    forwards: List[str] = []
    backwards: List[str] = []
    mode: str | None = None
    for raw_line in doc.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("Forward:"):
            mode = "forward"
            rest = stripped[len("Forward:") :].strip()
            if rest:
                forwards.extend(_expand_braces(_strip_comment(rest)))
        elif stripped.startswith("Backward:"):
            mode = "backward"
            rest = stripped[len("Backward:") :].strip()
            if rest:
                backwards.extend(_expand_braces(_strip_comment(rest)))
        elif mode and line.startswith(("  ", "\t")) and stripped and not stripped.startswith("#"):
            cleaned = _strip_comment(stripped)
            if cleaned:
                target = forwards if mode == "forward" else backwards
                target.extend(_expand_braces(cleaned))
        elif mode and (not stripped or not line.startswith((" ", "\t"))):
            mode = None
    return (forwards, backwards)


def _strip_comment(s: str) -> str:
    # Strip trailing parenthetical commentary like "  (StatsCan ...)".
    s = re.sub(r"\s{2,}\(.*$", "", s)
    s = re.sub(r"\s{2,}#.*$", "", s)
    return s.strip()


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------

def _norm_path(p: str) -> str:
    return p.replace("\\", "/").strip().rstrip(",;")


# Map known constructed-data paths back to L1 IDs. The mapping tolerates
# brace-expanded variants.

PATH_TO_ID: Dict[str, str] = {}


def _register_path(node_id: str, path_field: str) -> None:
    # The path_field may carry multiple comma-separated paths AND brace
    # expansions; split on commas/whitespace first, then expand braces.
    for raw in re.split(r",\s*", path_field):
        raw = raw.strip()
        if not raw or "(" in raw or "=" in raw:
            continue
        for expanded in _expand_braces(raw):
            PATH_TO_ID.setdefault(_norm_path(expanded), node_id)


def build_path_lookup() -> None:
    for node in L0_NODES:
        if "path" in node:
            _register_path(node["id"], node["path"])
    for node in L1_NODES:
        if "path" in node:
            _register_path(node["id"], node["path"])
    # Manually alias variants that scripts reference without a dedicated node.
    aliases = [
        # _full.gpkg variants route to their non-_full canonical.
        ("data/v0_1_approximate_majority_2026_eds_full.gpkg", "L1:constructed.approximate_eds"),
        ("data/v0_1_approximate_minority_2026_eds.gpkg", "L1:constructed.approximate_eds"),
        ("data/v0_1_refined_v6_minority_2026_eds_full.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_majority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_minority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v2_majority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v2_minority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v3_majority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v3_minority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v4_minority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_refined_v5_minority_2026_eds.gpkg", "L1:constructed.refined_eds_v6"),
        ("data/v0_1_derived_v7_majority_2026_eds.gpkg", "L1:constructed.derived_v7_eds"),
        ("data/v0_1_derived_v7_minority_2026_eds.gpkg", "L1:constructed.derived_v7_eds"),
        ("report_academic.md", "L0:doc.frozen_manifest"),
        ("FROZEN_MANIFEST.md", "L0:doc.frozen_manifest"),
    ]
    for path, node_id in aliases:
        PATH_TO_ID.setdefault(_norm_path(path), node_id)


def find_l2_id(script_rel_path: str) -> str:
    base = _norm_path(script_rel_path)
    stem = Path(base).stem
    return f"L2:{stem}"


def resolve_dependency(path_str: str) -> str | None:
    """Map a dependency path to an existing node ID or create a fallback."""
    norm = _norm_path(path_str)
    if not norm:
        return None
    # Strip leading repo segments.
    if norm.startswith("./"):
        norm = norm[2:]
    # Direct lookup first.
    if norm in PATH_TO_ID:
        return PATH_TO_ID[norm]
    # Tolerate paths that appear in manifest with extra basenames.
    for key, node_id in PATH_TO_ID.items():
        if norm == key or norm.endswith("/" + key) or key.endswith("/" + norm):
            return node_id
    # Script path?
    if norm.startswith("analysis/scripts/") and norm.endswith(".py"):
        return find_l2_id(norm)
    if norm.startswith("analysis/") and norm.endswith(".py"):
        return find_l2_id(norm)
    # Report output markdown: treat as a Forward artefact (L1-style doc).
    # We won't create a node for each markdown output; instead ignore them
    # unless they are analysis/reports under explicit tracking.
    return None


def build_nodes_and_edges() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    judgment_calls: List[str] = []

    # Copy L0 + L1 nodes.
    for n in L0_NODES + L1_NODES:
        nodes.append(dict(n))

    # L2 nodes — union of L2_MANIFEST and any scripts with F/B headers.
    manifest_by_path = {_norm_path(m["path"]): m for m in L2_MANIFEST}

    # Exclude graph-meta scripts from the L2 node set — they operate on the
    # DAG itself, not on the audit's evidentiary chain.
    meta_skip = {
        "analysis/scripts/v0_1_dependency_graph_build.py",
        "analysis/scripts/v0_1_dependency_graph_render.py",
        "analysis/scripts/v0_1_dependency_query.py",
    }

    header_scripts: Set[str] = set()
    for script_path in sorted(SCRIPTS.glob("*.py")):
        rel = script_path.relative_to(ROOT).as_posix()
        if rel in meta_skip:
            continue
        fwds, bkwds = parse_headers(script_path)
        if fwds or bkwds:
            header_scripts.add(rel)

    # Also capture analysis/v0_1_shape_derivation_v7.py (not in scripts/).
    derivation = ROOT / "analysis" / "v0_1_shape_derivation_v7.py"
    if derivation.exists():
        rel = derivation.relative_to(ROOT).as_posix()
        fwds, bkwds = parse_headers(derivation)
        if fwds or bkwds:
            header_scripts.add(rel)

    all_l2_paths: Set[str] = set(manifest_by_path.keys()) | header_scripts

    l2_entries: List[Dict[str, Any]] = []
    for path in sorted(all_l2_paths):
        manifest = manifest_by_path.get(path, {})
        node_id = find_l2_id(path)
        entry = {
            "id": node_id,
            "layer": "L2",
            "name": manifest.get("name", Path(path).stem),
            "type": "measurement_script",
            "path": path,
            "role": manifest.get("role", ""),
            "has_header": path in header_scripts,
        }
        l2_entries.append(entry)
        nodes.append(entry)

    # Parse headers → edges for each header-bearing script.
    for entry in l2_entries:
        if not entry["has_header"]:
            continue
        script_full = ROOT / entry["path"]
        fwds, bkwds = parse_headers(script_full)
        for fwd in fwds:
            target = resolve_dependency(fwd)
            if target is None:
                judgment_calls.append(
                    f"Forward target unresolved in {entry['path']}: {fwd!r}"
                )
                continue
            edges.append(
                {
                    "source": entry["id"],
                    "target": target,
                    "type": "required",
                    "sensitivity": "script Forward: header",
                }
            )
        for bkwd in bkwds:
            source = resolve_dependency(bkwd)
            if source is None:
                judgment_calls.append(
                    f"Backward source unresolved in {entry['path']}: {bkwd!r}"
                )
                continue
            edges.append(
                {
                    "source": source,
                    "target": entry["id"],
                    "type": "required",
                    "sensitivity": "script Backward: header",
                }
            )

    # Add curated L2 role-based edges for scripts without F/B headers but in
    # the manifest — these capture the obvious "consumes X, produces Y" link
    # inferred from the role field. We only add edges we can justify from
    # path names already present in L1.
    curated_l2_edges: List[Tuple[str, str, str, str]] = [
        # (script_stem, target_id, direction, sensitivity)
        ("electoral_forensics_population", "L0:data.commission_published_populations", "in", "consumes per-ED population table"),
        ("v0_2_packing_cracking_analysis", "L0:data.2023_statement_of_vote", "in", "consumes 2023 vote data"),
        ("v0_2_packing_cracking_analysis", "L1:constructed.crosswalk_majority_hybrid", "in", "consumes majority hybrid crosswalk"),
        ("v0_2_packing_cracking_analysis", "L1:constructed.crosswalk_minority_hybrid", "in", "consumes minority hybrid crosswalk"),
        ("v0_3_monte_carlo_ci", "L0:data.2023_statement_of_vote", "in", "consumes 2023 vote data"),
        ("v0_3_monte_carlo_ci", "L1:constructed.crosswalk_majority_hybrid", "in", "consumes majority hybrid crosswalk"),
        ("v0_3_monte_carlo_ci", "L1:constructed.crosswalk_minority_hybrid", "in", "consumes minority hybrid crosswalk"),
        ("v0_1_mcmc_ensemble", "L0:data.2023_va_shapefile", "in", "VA substrate"),
        ("v0_1_mcmc_ensemble", "L1:constructed.va_pop_from_das", "in", "DA-derived VA population"),
        ("v0_1_mcmc_ensemble", "L1:constructed.mcmc_ensemble_10k", "out", "produces 10k ensemble"),
        ("v0_1_mcmc_ensemble_100k", "L0:data.2023_va_shapefile", "in", "VA substrate"),
        ("v0_1_mcmc_ensemble_100k", "L1:constructed.va_pop_from_das", "in", "DA-derived VA population"),
        ("v0_1_mcmc_ensemble_100k", "L1:constructed.mcmc_ensemble_100k", "out", "produces 100k ensemble"),
        ("v0_1_mcmc_full_coverage_rescore_100k", "L1:constructed.mcmc_ensemble_100k", "in", "consumes 100k ensemble"),
        ("v0_1_mcmc_full_coverage_rescore_100k", "L1:constructed.crosswalk_majority_full", "in", "fallback crosswalk"),
        ("v0_1_mcmc_full_coverage_rescore_100k", "L1:constructed.crosswalk_minority_full", "in", "fallback crosswalk"),
        ("v0_1_mcmc_full_coverage_rescore_100k", "L1:constructed.mcmc_real_map_scores", "out", "produces real-map scores"),
        ("v0_1_advance_vote_splat", "L0:data.2023_statement_of_vote", "in", "Election-Day + Vote-Anywhere rows"),
        ("v0_1_advance_vote_splat", "L1:constructed.va_substrate_elecday", "in", "Election-Day substrate input"),
        ("v0_1_advance_vote_splat", "L1:constructed.va_substrate_full", "out", "produces splatted full-VA substrate"),
        ("v0_1_advance_vote_splat", "L1:constructed.advance_vote_diag", "out", "diagnostics CSV"),
        ("parse_2015_results", "L0:data.2015_statement_of_vote", "in", "parse 2015 xlsx"),
        ("parse_2015_results", "L0:data.2015_election_results", "out", "per-ED 2015 results"),
        ("phase_4c_prep", "L0:data.2023_statement_of_vote", "in", "raw votes"),
        ("phase_4c_prep", "L0:data.2023_va_shapefile", "in", "VA geometry"),
        ("phase_4c_prep", "L1:constructed.va_substrate_elecday", "out", "election-day VA substrate"),
        ("phase_4c_prep", "L1:constructed.polls_2023_unified", "out", "unified polls"),
        ("v0_1_chen_rodden_alberta", "L0:data.2023_statement_of_vote", "in", "vote substrate"),
        ("v0_1_chen_rodden_alberta", "L0:data.2019_ed_shapefile", "in", "87-seat baseline geometry"),
        ("v0_1_chen_rodden_alberta", "L1:constructed.chen_rodden", "out", "Chen-Rodden outputs"),
        ("v0_1_csd_community_splits", "L0:data.2021_csds_gpkg", "in", "CSD geometry"),
        ("v0_1_csd_community_splits", "L0:data.2019_ed_shapefile", "in", "2019 baseline"),
        ("v0_1_csd_community_splits", "L1:constructed.dpg_v0_1_canonical", "in", "DPG substrates"),
        ("v0_1_csd_community_splits", "L1:constructed.csd_splits", "out", "CSD splits summary"),
        ("v0_1_338canada_historical", "L0:data.338_historical_snapshots_dir", "in", "historical snapshots"),
        ("v0_1_338canada_historical", "L0:data.338canada_snapshots", "in", "77-snapshot series"),
        ("v0_1_338canada_reallocate", "L0:data.338canada_snapshots", "in", "current 338 data"),
        ("v0_1_338canada_reallocate", "L1:constructed.crosswalk_majority_hybrid", "in", "majority crosswalk"),
        ("v0_1_338canada_reallocate", "L1:constructed.crosswalk_minority_hybrid", "in", "minority crosswalk"),
        ("v0_1_338canada_reallocate", "L1:constructed.338canada_reallocated", "out", "reallocated scores"),
        ("v0_1_canadian_base_rate_compute", "L1:constructed.canadian_base_rate", "out", "base-rate CSV"),
        ("v0_1_canadian_base_rate_recalibrate", "L1:constructed.canadian_base_rate", "out", "recalibrated base-rate"),
        ("v0_1_marginal_seats_analysis", "L0:data.2023_statement_of_vote", "in", "2023 margins"),
        ("v0_1_marginal_seats_analysis", "L0:data.2019_election_results", "in", "2019 margins"),
        ("v0_1_marginal_seats_analysis", "L0:data.2015_election_results", "in", "2015 margins"),
        ("v0_1_marginal_seats_analysis", "L1:constructed.marginal_seats", "out", "margin table"),
        ("v0_1_2015_cross_election", "L0:data.2015_election_results", "in", "2015 results"),
        ("v0_1_2015_cross_election", "L0:data.commission_rationales_text", "in", "2015-to-2019 crosswalk"),
        ("v0_1_2015_cross_election", "L1:constructed.cross_election_asymmetry", "out", "3-way asymmetry"),
        ("v0_1_a1_legal_baseline_2021_census", "L0:data.2021_da_populations", "in", "DA populations"),
        ("v0_1_a1_legal_baseline_2021_census", "L0:data.2019_ed_shapefile", "in", "2019 ED geometry"),
        ("v0_1_a1_legal_baseline_2021_census", "L0:data.2019_ed_populations", "out", "legal-baseline A1"),
        ("v0_1_plan_b_rerun", "L0:data.2021_da_populations", "in", "2021 census basis"),
        ("v0_1_plan_b_rerun", "L0:data.tbf_population_estimates", "in", "TBF basis"),
        ("v0_1_plan_b_rerun", "L0:data.statscan_1710000901", "in", "Table 17-10-0009 basis"),
        ("v0_1_rural_gap_dissection", "L0:data.commission_published_populations", "in", "per-ED population"),
        ("v0_1_rural_gap_dissection", "L1:constructed.rural_gap_summary", "out", "rural gap summary"),
        ("v0_1_majority_symmetry_counter_test", "L0:data.commission_published_populations", "in", "per-ED population"),
        ("v0_1_majority_symmetry_counter_test", "L0:data.2021_csd_populations", "in", "CSD population threshold"),
        ("v0_1_majority_symmetry_counter_test", "L1:constructed.symmetry_counter_test", "out", "counter-test CSV"),
        ("submission_search", "L0:data.submission_archive", "in", "raw submissions"),
        ("submission_search", "L1:constructed.submission_search_results", "out", "keyword-search results"),
        ("v0_1_url_archival", "L0:doc.frozen_manifest", "out", "updates Wayback columns"),
        ("v0_1_max_dpi_extract", "L0:data.commission_final_report_2026", "in", "commission PDF"),
        ("v0_1_max_dpi_extract", "L1:constructed.max_dpi_extract", "out", "extraction JSON"),
        ("v0_1_max_dpi_inspect", "L1:constructed.max_dpi_extract", "in", "extraction JSON"),
        ("v0_1_build_canonical_shapefiles", "L1:constructed.approximate_eds", "in", "majority approximate source"),
        ("v0_1_build_canonical_shapefiles", "L1:constructed.refined_eds_v6", "in", "minority v6 source"),
        ("v0_1_build_canonical_shapefiles", "L1:constructed.derived_v7_eds", "in", "v7 derived source"),
        ("v0_1_build_canonical_shapefiles", "L1:constructed.dpg_v0_1_canonical", "out", "canonical DPG"),
        ("v0_1_build_full_crosswalks", "L0:data.2019_ed_shapefile", "in", "2019 parents"),
        ("v0_1_build_full_crosswalks", "L1:constructed.dpg_v0_1_canonical", "in", "DPG"),
        ("v0_1_build_full_crosswalks", "L1:constructed.crosswalk_majority_full", "out", "majority full crosswalk"),
        ("v0_1_build_full_crosswalks", "L1:constructed.crosswalk_minority_full", "out", "minority full crosswalk"),
        # Hybrid crosswalks are authored from commission Appendix E descriptions
        # + 2019 ED shapefile; they are not produced by a standalone script but
        # rather committed to the repo as hand-edited CSVs. Link them to the
        # commission final report as their evidentiary parent so invalidating
        # upstream L0 correctly cascades.
        ("v0_1_build_full_crosswalks", "L1:constructed.crosswalk_majority_hybrid", "in", "feeds into full crosswalk build"),
        ("v0_1_build_full_crosswalks", "L1:constructed.crosswalk_minority_hybrid", "in", "feeds into full crosswalk build"),
        # Shape refinement chain (v1 -> v6)
        ("v0_1_shape_refinement", "L1:constructed.approximate_eds", "in", "approximate ED inputs"),
        ("v0_1_shape_refinement", "L1:constructed.boundary_refinement_impact", "out", "per-pass impact CSV"),
        ("v0_1_shape_refinement_v2", "L1:constructed.boundary_refinement_impact", "out", "v2 impact CSV"),
        ("v0_1_shape_refinement_v3", "L1:constructed.boundary_refinement_impact", "out", "v3 impact CSV"),
        ("v0_1_shape_refinement_v4", "L1:constructed.boundary_refinement_impact", "out", "v4 impact CSV"),
        ("v0_1_shape_refinement_v5", "L1:constructed.boundary_refinement_impact", "out", "v5 impact CSV"),
        ("v0_1_shape_refinement_v6", "L1:constructed.refined_eds_v6", "out", "v6 refined polygon set"),
        ("v0_1_shape_refinement_v6", "L1:constructed.boundary_refinement_impact", "out", "v6 impact CSV"),
        ("v0_1_shape_refinement_v6_processors", "L1:constructed.refined_eds_v6", "out", "v6 processors helper"),
        ("v0_1_shape_refinement_v6_writer", "L1:constructed.refined_eds_v6", "out", "v6 GPKG writer"),
        ("v0_1_shape_derivation_v7", "L1:constructed.refined_eds_v6", "in", "v6 input"),
        ("v0_1_shape_derivation_v7", "L1:constructed.derived_v7_eds", "out", "v7 derived polygons"),
        # Build pipeline and auxiliary
        ("v0_1_build_composite_shapefiles", "L1:constructed.approximate_eds", "in", "approximate input"),
        ("v0_1_build_composite_shapefiles", "L1:constructed.refined_eds_v6", "in", "refined v6 input"),
        ("v0_1_build_composite_shapefiles", "L1:constructed.composite_eds", "out", "composite polygons"),
        # 338Canada scraper → snapshots
        ("v0_1_338canada_scraper", "L0:data.338canada_snapshots", "out", "scrapes 338 per-riding projections"),
        # Diagnostic scripts
        ("v0_1_airdrie_overlap_diagnostic", "L1:constructed.dpg_v0_1_canonical", "in", "DPG input for overlap diagnostic"),
        ("v0_1_airdrie_overlap_diagnostic", "L1:constructed.hybrid_adjacency", "out", "hybrid-adjacent VAs"),
        ("v0_1_overlap_zone_diagnostic", "L1:constructed.dpg_v0_1_canonical", "in", "DPG input"),
        ("v0_1_overlap_zone_diagnostic", "L1:constructed.topology_cleanup_log", "out", "diagnostic for cleanup"),
        ("v0_1_edmonton_beaumont_polygon", "L0:data.commission_map_pngs", "in", "manual Edmonton-Beaumont trace"),
        ("v0_1_edmonton_beaumont_polygon", "L1:constructed.derived_v7_eds", "out", "contributes to v7 polygon set"),
        ("v0_1_edmonton_beaumont_split", "L0:data.2021_csds_gpkg", "in", "Beaumont CSD"),
        ("v0_1_edmonton_beaumont_split", "L1:constructed.derived_v7_eds", "out", "split output"),
        ("v0_1_approximate_shape_analysis", "L1:constructed.approximate_eds", "in", "approximate polygons"),
        ("v0_1_approximate_shape_analysis", "L0:data.commission_map_pngs", "in", "commission reference images"),
        ("v0_1_tier_c_crops", "L0:data.commission_final_report_2026", "in", "source PDF"),
        ("v0_1_tier_c_crops", "L1:constructed.tier_c_reference", "out", "tier-C reference"),
        ("v0_1_track_l_drift", "L0:data.tbf_population_estimates", "in", "TBF quarterly"),
        ("v0_1_track_l_drift", "L0:data.statscan_1710000901", "in", "StatsCan quarterly"),
        ("v0_1_cross_election_rural_baseline", "L0:data.2015_election_results", "in", "2015 rural baseline"),
        ("v0_1_cross_election_rural_baseline", "L0:data.2019_election_results", "in", "2019 rural baseline"),
        ("v0_1_cross_election_rural_baseline", "L0:data.2023_statement_of_vote", "in", "2023 rural baseline"),
        ("v0_1_cross_election_rural_baseline", "L1:constructed.cross_election_asymmetry", "out", "province-wide drift CSVs"),
        ("v0_1_justification_tests", "L0:data.2023_statement_of_vote", "in", "vote data"),
        ("v0_1_justification_tests", "L1:constructed.marginal_seats", "out", "justification test inputs"),
        ("v0_1_poll_attribution_skeleton", "L0:data.2023_statement_of_vote", "in", "poll-level rows"),
        ("v0_1_poll_attribution_skeleton", "L1:constructed.polls_2023_unified", "out", "unified polls"),
        ("v0_1_mcmc_full_coverage_rescore", "L1:constructed.mcmc_ensemble_10k", "in", "10k ensemble"),
        ("v0_1_mcmc_full_coverage_rescore", "L1:constructed.mcmc_real_map_scores", "out", "10k rescore scores"),
        ("v0_1_submission_ocr", "L0:data.submission_archive", "in", "image-only submission PDFs"),
        ("v0_1_submission_ocr", "L1:constructed.submission_search_results", "out", "OCR-augmented search dataset"),
        ("v0_1_submission_ocr_analyze", "L1:constructed.submission_search_results", "in", "OCR keyword pass"),
        ("v0_1_build_overlay_figures", "L1:constructed.dpg_v0_1_canonical", "in", "DPG for overlay"),
        ("v0_1_build_overlay_figures_v2", "L1:constructed.dpg_v0_1_canonical", "in", "DPG for overlay v2"),
        ("v0_1_build_article_figures_v3", "L1:constructed.dpg_v0_1_canonical", "in", "DPG"),
        ("v0_1_dpg_perturbation_writeup", "L1:constructed.dpg_perturbation_flat", "in", "flat samples"),
        ("v0_1_dpg_perturbation_writeup", "L1:constructed.dpg_perturbation_tiered", "in", "tiered samples"),
        ("v0_1_phase_4bcdef_execution", "L1:constructed.phase4bcdef_summary", "out", "summary JSON"),
        ("v0_1_phase_4c_va_attribution_maup", "L1:constructed.phase4c_maup_summary", "out", "MAUP summary"),
        ("v0_1_phase_4c_va_attribution_maup_v2", "L1:constructed.phase4c_maup_summary", "out", "MAUP v2 summary"),
        ("v0_1_phase_4c_va_attribution_maup_v3_v05", "L1:constructed.phase4c_maup_summary", "out", "MAUP v0_5 summary"),
        ("v0_1_phase_4c_va_attribution_maup", "L1:constructed.va_to_2026_assignments", "out", "VA-to-2026-ED assignments"),
        ("v0_1_phase_4c_va_attribution_maup_v2", "L1:constructed.va_to_2026_assignments", "out", "VA-to-2026-ED assignments v2"),
        ("v0_1_phase_4c_va_attribution_maup_v3_v05", "L1:constructed.va_to_2026_assignments", "out", "VA-to-2026-ED assignments v0_5"),
        ("v0_1_phase_4bf_v05", "L1:constructed.phase4b_v05_pops", "out", "v0_5 Phase 4B pops"),
        # Polsby-Popper compactness
        ("v0_1_approximate_shape_analysis", "L1:constructed.compactness_scores", "out", "compactness scores"),
        # DPG v0_3 swept (intermediate constructed product produced by build_canonical_shapefiles_v2 per Issue #3)
        ("v0_1_municipal_anchoring", "L1:constructed.dpg_v0_3_swept", "in", "prefers v0_3 swept DPG over v0_2 where present"),
        ("v0_1_build_canonical_shapefiles_v2", "L1:constructed.dpg_v0_3_swept", "out", "produces v0_3 pop-swept DPG (Issue #3)"),
        ("v0_1_build_canonical_shapefiles_v2", "L1:constructed.dpg_v0_2_topoclean", "in", "cleaned topology input"),
        # Report-build scripts: consume report_academic.md (doc) and emit HTML/PDF.
        # We don't model these as L0/L3 artefacts but they still need an edge
        # to avoid orphan status — attach to FROZEN_MANIFEST as consuming the
        # repository doc-set.
        ("build_academic_html", "L0:doc.frozen_manifest", "in", "reads published report"),
        ("build_cover", "L0:doc.frozen_manifest", "in", "reads cover art"),
        ("build_pdf", "L0:doc.frozen_manifest", "in", "reads HTML/Markdown"),
        ("check_voice_and_readability", "L0:doc.frozen_manifest", "in", "reads editorial-pass files"),
    ]

    l2_ids = {e["id"] for e in l2_entries}
    for stem, node_id, direction, sensitivity in curated_l2_edges:
        script_id = f"L2:{stem}"
        if script_id not in l2_ids:
            # Script may not exist in repo — skip silently.
            continue
        if direction == "in":
            edges.append({
                "source": node_id,
                "target": script_id,
                "type": "required",
                "sensitivity": sensitivity,
            })
        else:
            edges.append({
                "source": script_id,
                "target": node_id,
                "type": "required",
                "sensitivity": sensitivity,
            })

    # L3 findings + their evidentiary edges.
    for finding in L3_FINDINGS:
        finding_node = {
            "id": finding["id"],
            "layer": "L3",
            "name": finding["name"],
            "type": "finding",
            "report_section": finding["report_section"],
        }
        nodes.append(finding_node)
        for src_id, edge_type, sensitivity in finding["evidence"]:
            edges.append({
                "source": src_id,
                "target": finding["id"],
                "type": edge_type,
                "sensitivity": sensitivity,
            })

    # Authored-artefact provenance: some L1 nodes are hand-curated CSVs
    # authored from commission Appendix E descriptions or external polling
    # sources. Link them back to their evidentiary parents so invalidation
    # cascades correctly.
    authored_links: List[Tuple[str, str, str, str]] = [
        ("L0:data.commission_final_report_2026", "L1:constructed.crosswalk_majority_hybrid", "required", "authored from commission Appendix C + 2019 shapefile"),
        ("L0:data.2019_ed_shapefile", "L1:constructed.crosswalk_majority_hybrid", "required", "2019 parents for crosswalk rows"),
        ("L0:data.commission_final_report_2026", "L1:constructed.crosswalk_minority_hybrid", "required", "authored from commission Appendix E + 2019 shapefile"),
        ("L0:data.2019_ed_shapefile", "L1:constructed.crosswalk_minority_hybrid", "required", "2019 parents for crosswalk rows"),
        ("L0:data.commission_final_report_2026", "L1:constructed.approximate_eds", "required", "transcribed from commission maps + rationales"),
        ("L0:data.commission_map_pngs", "L1:constructed.approximate_eds", "required", "traced from commission map rasters"),
        ("L0:data.2019_ed_shapefile", "L1:constructed.approximate_eds", "required", "Tier-A identity shapes"),
        ("L0:data.commission_final_report_2026", "L1:constructed.refined_eds_v6", "required", "refinement guided by commission text"),
        ("L0:data.commission_map_pngs", "L1:constructed.refined_eds_v6", "required", "refinement guided by commission maps"),
        ("L0:data.commission_final_report_2026", "L1:constructed.derived_v7_eds", "required", "derived from commission text"),
        ("L0:data.commission_map_pngs", "L1:constructed.derived_v7_eds", "required", "derived from commission maps"),
        ("L0:data.2023_statement_of_vote", "L1:constructed.va_substrate_elecday", "required", "Election-Day rows"),
        ("L0:data.2023_va_shapefile", "L1:constructed.va_substrate_elecday", "required", "VA polygons"),
        ("L0:data.2023_statement_of_vote", "L1:constructed.va_substrate_full", "required", "Vote-Anywhere rows"),
        ("L0:data.2023_va_shapefile", "L1:constructed.va_substrate_full", "required", "VA polygons"),
        ("L0:data.2021_da_populations", "L1:constructed.va_pop_from_das", "required", "DA populations for VA weighting"),
        ("L0:data.2021_das_gpkg", "L1:constructed.va_pop_from_das", "required", "DA polygons"),
        ("L0:data.2023_va_shapefile", "L1:constructed.va_pop_from_das", "required", "VA polygons"),
        # commission-published populations have upstream from commission final report
        ("L0:data.commission_final_report_2026", "L0:data.commission_published_populations", "required", "extracted from Appendix A + E tables"),
        ("L0:data.commission_final_report_2026", "L0:data.commission_rationales", "required", "extracted from Appendix E rationale prose"),
        ("L0:data.commission_final_report_2026", "L0:data.commission_r5_addendum", "required", "chair addendum within final report"),
        ("L0:data.commission_final_report_2017", "L0:data.2019_ed_populations", "required", "2019-era populations per 2017 commission"),
        ("L0:data.2021_da_populations", "L0:data.2019_ed_populations", "corroborating", "DA-aggregated cross-check"),
        ("L0:data.2015_statement_of_vote", "L0:data.2015_election_results", "required", "parsed from 2015 SoV"),
        # 338canada snapshots subset
        ("L0:data.338canada_snapshots", "L0:data.338_historical_snapshots_dir", "corroborating", "historical slice of same projection data"),
    ]
    for src, tgt, etype, sensitivity in authored_links:
        edges.append({
            "source": src,
            "target": tgt,
            "type": etype,
            "sensitivity": sensitivity,
        })

    # Add a validating edge from Phase 4F to Phase 4B/C outputs.
    for target in (
        "L1:constructed.phase4b_pops",
        "L1:constructed.phase4c_votes",
    ):
        edges.append({
            "source": "L1:constructed.phase4f_validation",
            "target": target,
            "type": "validating",
            "sensitivity": "Phase 4F validates commission-vs-derived populations (hardstop gate)",
        })

    # Add validating edges for FROZEN_MANIFEST → all L0 non-doc nodes.
    for n in L0_NODES:
        if n["id"] == "L0:doc.frozen_manifest":
            continue
        edges.append({
            "source": "L0:doc.frozen_manifest",
            "target": n["id"],
            "type": "validating",
            "sensitivity": "FROZEN_MANIFEST pins the source URL + snapshot",
        })

    # Deduplicate edges.
    seen: Set[Tuple[str, str, str]] = set()
    unique_edges: List[Dict[str, Any]] = []
    node_ids: Set[str] = {n["id"] for n in nodes}
    for e in edges:
        key = (e["source"], e["target"], e["type"])
        if key in seen:
            continue
        if e["source"] not in node_ids or e["target"] not in node_ids:
            judgment_calls.append(
                f"Dropping edge with missing endpoint: {e['source']} -> {e['target']}"
            )
            continue
        if e["source"] == e["target"]:
            continue
        seen.add(key)
        unique_edges.append(e)

    return nodes, unique_edges, judgment_calls


# ---------------------------------------------------------------------------
# DOT rendering
# ---------------------------------------------------------------------------

LAYER_COLORS = {
    "L0": "#d0e8f2",  # light blue — raw data
    "L1": "#ddebbd",  # light green — constructed
    "L2": "#fce4a7",  # light amber — scripts
    "L3": "#f2c6c6",  # light red — findings
}

EDGE_STYLES = {
    "required": "solid",
    "corroborating": "dashed",
    "validating": "dotted",
}


def _dot_id(raw_id: str) -> str:
    return '"' + raw_id.replace('"', '\\"') + '"'


def _dot_label(node: Dict[str, Any]) -> str:
    name = node.get("name", node["id"])
    section = node.get("report_section")
    if section:
        name = f"§{section}\\n{name}"
    # Wrap long names at ~36 chars on spaces.
    words = name.split(" ")
    lines: List[str] = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 > 42:
            lines.append(current)
            current = w
        else:
            current = (current + " " + w).strip() if current else w
    if current:
        lines.append(current)
    joined = "\\n".join(lines)
    return joined.replace('"', '\\"')


def emit_dot(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("digraph audit_dependency_graph {")
    lines.append('  rankdir=TB;')
    lines.append('  splines=true;')
    lines.append('  overlap=false;')
    lines.append('  ranksep=1.2;')
    lines.append('  nodesep=0.35;')
    lines.append('  node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=9];')
    lines.append('  edge [fontname="Helvetica", fontsize=7];')

    for layer in ("L0", "L1", "L2", "L3"):
        lines.append(f'  subgraph cluster_{layer} {{')
        lines.append(f'    label="Layer {layer[1]} — {_layer_title(layer)}";')
        lines.append(f'    style="rounded,filled"; color="{LAYER_COLORS[layer]}88"; fillcolor="{LAYER_COLORS[layer]}22";')
        for n in nodes:
            if n["layer"] != layer:
                continue
            color = LAYER_COLORS[layer]
            lines.append(
                f'    {_dot_id(n["id"])} [label="{_dot_label(n)}", fillcolor="{color}"];'
            )
        lines.append('  }')

    for e in edges:
        style = EDGE_STYLES.get(e["type"], "solid")
        color = {
            "required": "#333333",
            "corroborating": "#2a7f2a",
            "validating": "#774a00",
        }.get(e["type"], "#555555")
        lines.append(
            f'  {_dot_id(e["source"])} -> {_dot_id(e["target"])} '
            f'[style={style}, color="{color}"];'
        )

    lines.append("}")
    return "\n".join(lines) + "\n"


def _layer_title(layer: str) -> str:
    return {
        "L0": "Raw data",
        "L1": "Constructed data",
        "L2": "Measurement scripts",
        "L3": "Findings",
    }[layer]


# ---------------------------------------------------------------------------
# Validation — topological sort + orphan detection
# ---------------------------------------------------------------------------

def topological_sort(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> Tuple[bool, List[str]]:
    indeg: Dict[str, int] = {n["id"]: 0 for n in nodes}
    out_adj: Dict[str, List[str]] = defaultdict(list)
    for e in edges:
        if e["target"] in indeg and e["source"] in indeg:
            indeg[e["target"]] += 1
            out_adj[e["source"]].append(e["target"])
    q = deque([nid for nid, d in indeg.items() if d == 0])
    order: List[str] = []
    while q:
        nid = q.popleft()
        order.append(nid)
        for nxt in out_adj[nid]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return (len(order) == len(nodes), order)


def find_orphans(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> List[str]:
    touched: Set[str] = set()
    for e in edges:
        touched.add(e["source"])
        touched.add(e["target"])
    return sorted(n["id"] for n in nodes if n["id"] not in touched)


def findings_reachable_to_L0(
    nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    back_adj: Dict[str, List[str]] = defaultdict(list)
    for e in edges:
        back_adj[e["target"]].append(e["source"])
    node_layer = {n["id"]: n["layer"] for n in nodes}
    findings = [n["id"] for n in nodes if n["layer"] == "L3"]
    reaches: List[str] = []
    orphan: List[str] = []
    for f in findings:
        seen: Set[str] = {f}
        stack = [f]
        hit_l0 = False
        while stack:
            cur = stack.pop()
            if node_layer.get(cur) == "L0":
                hit_l0 = True
                break
            for p in back_adj[cur]:
                if p not in seen:
                    seen.add(p)
                    stack.append(p)
        if hit_l0:
            reaches.append(f)
        else:
            orphan.append(f)
    return reaches, orphan


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _git_head() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            text=True,
        ).strip()
        return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> int:
    build_path_lookup()
    nodes, edges, judgment_calls = build_nodes_and_edges()

    acyclic, order = topological_sort(nodes, edges)
    orphans = find_orphans(nodes, edges)
    _, findings_without_l0 = findings_reachable_to_L0(nodes, edges)

    # Most-depended-on nodes (high in-degree).
    indeg: Dict[str, int] = defaultdict(int)
    outdeg: Dict[str, int] = defaultdict(int)
    for e in edges:
        indeg[e["target"]] += 1
        outdeg[e["source"]] += 1

    graph = {
        "meta": {
            "schema_version": SCHEMA_VERSION,
            "date_built": _dt.date.today().isoformat(),
            "commit": _git_head(),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "acyclic": acyclic,
            "orphan_nodes": orphans,
            "findings_without_l0_path": findings_without_l0,
            "judgment_calls": judgment_calls,
            "counts_per_layer": {
                layer: sum(1 for n in nodes if n["layer"] == layer)
                for layer in ("L0", "L1", "L2", "L3")
            },
            "edge_counts_per_type": {
                t: sum(1 for e in edges if e["type"] == t)
                for t in ("required", "corroborating", "validating")
            },
            "top5_indegree": sorted(indeg.items(), key=lambda kv: -kv[1])[:5],
            "top5_outdegree_l3sources": sorted(
                (
                    (nid, d)
                    for nid, d in outdeg.items()
                    if any(n["id"] == nid and n["layer"] != "L3" for n in nodes)
                ),
                key=lambda kv: -kv[1],
            )[:5],
        },
        "nodes": nodes,
        "edges": edges,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    dot = emit_dot(nodes, edges)
    OUT_DOT.write_text(dot, encoding="utf-8")

    # Print summary.
    meta = graph["meta"]
    print(f"Nodes: {meta['node_count']} (L0={meta['counts_per_layer']['L0']}, L1={meta['counts_per_layer']['L1']}, L2={meta['counts_per_layer']['L2']}, L3={meta['counts_per_layer']['L3']})")
    print(f"Edges: {meta['edge_count']} (required={meta['edge_counts_per_type']['required']}, corroborating={meta['edge_counts_per_type']['corroborating']}, validating={meta['edge_counts_per_type']['validating']})")
    print(f"Acyclic: {meta['acyclic']}")
    print(f"Orphan nodes: {len(orphans)}")
    print(f"Findings with no L0 path: {len(findings_without_l0)}")
    print(f"Judgment-call items: {len(judgment_calls)}")
    print("Top-5 in-degree:")
    for nid, d in meta["top5_indegree"]:
        print(f"  {d:4d}  {nid}")
    print("Top-5 out-degree (non-L3 sources):")
    for nid, d in meta["top5_outdegree_l3sources"]:
        print(f"  {d:4d}  {nid}")
    if judgment_calls:
        print("Judgment calls (up to first 10):")
        for j in judgment_calls[:10]:
            print(f"  - {j}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
