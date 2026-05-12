# Contributing to the Alberta Electoral Boundary Audit

Thank you for your interest in contributing! This project is an open, reproducible forensic audit. We welcome scrutiny, corrections, and new methodological approaches.

## Getting Started

1. Check the **Quickstart** in the `README.md` to get your local environment running.
2. Read **`REPRODUCING.md`** for detailed instructions on the data pipeline, expected outputs, and how to trigger the MCMC ensembles.

## How to Contribute

### 1. Challenging a Finding
This is the most valuable form of contribution. 
* Every load-bearing finding has a public retraction condition documented in `analysis/methodology/retraction_pathway.md`. 
* If you have data or an argument that triggers one of these conditions, please **open an Issue** detailing the finding number (e.g., §5.8.5) and your evidence.

### 2. Code and Data Corrections
If you spot a bug in a script, an error in a crosswalk file, or a typo in the documentation:
* Fork the repository.
* Create a branch (e.g., `fix-v09-anchoring-bug`).
* Submit a Pull Request.

### 3. Proposing New Metrics
If you want to add a new structural or partisan test:
* Please include a **pre-registration artifact** in your PR description: state your null hypothesis, the pass/fail threshold, and your predicted direction *before* you run the test. This matches the discipline used throughout the audit.

## Coding Standards
* The codebase is functional and script-based by design (~87 Python scripts in `analysis/scripts/`).
* **Do not over-abstract.** Avoid creating deep inheritance hierarchies or global config files unless absolutely necessary. The current DAG (Directed Acyclic Graph) of scripts ensures that each analytical step is atomic and independently verifiable.
* Python code should be compatible with Python 3.11+.

## AI Tooling Attribution Policy
This audit was produced with AI assistance from **Claude Opus 4.7** (Anthropic), **Google Gemini 3.1 Pro**, and **OpenAI Codex** (adversarial commentary). We maintain a strict dual-attribution policy:
* If an AI tool originated a finding or wrote substantial portions of a script, it must be credited in the commit message via `Co-Authored-By` trailers.
* The human author retains final editorial and methodological responsibility for all committed code.
* AI tools did not execute code or access external data independently; all script runs and data access were performed by the author.

Thank you for helping us keep this audit rigorous and transparent!
