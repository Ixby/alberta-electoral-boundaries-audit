Project-level documentation and operational records.

| File | Description |
|---|---|
| `FROZEN_MANIFEST.md` | Canonical inventory of every primary data source with checksums and archive URLs. The authoritative list of what the audit depends on. |
| `REPRODUCING.md` | Step-by-step instructions for reproducing the full audit pipeline from scratch |
| `COMPLETED_LOG.md` | Chronological log of completed work items with outcome notes |
| `setup.md` | Environment setup: Python version, dependency installation, data directory layout |
| `data_sources.md` | Narrative description of each primary data source and how it was obtained |
| `ai_use_recommendations_for_committee.md` | AI-use recommendations for the Lunty committee: seven principles, technical guidance, and a 9-item public disclosure checklist |
| `act_amendment_proposal.md` | Proposed amendments to the Electoral Boundaries Commission Act based on audit findings |
| `changedetection_setup.md` | Configuration for Elections Alberta webpage monitoring (change-detection alerts) |
| `external_tool_validation.md` | Validation notes for third-party tools used in the audit (GerryChain, geopandas, etc.) |

`FROZEN_MANIFEST.md` is load-bearing: any finding that cites a primary source must trace to an entry in this file.
