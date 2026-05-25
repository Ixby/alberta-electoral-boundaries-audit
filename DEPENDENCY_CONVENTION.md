---
name: Dependency Convention
description: How every script and document in this repo declares its upstream and downstream so the dependency graph stays accurate without a separate map that rots.
type: project
---

# Dependency Convention

**Tree maps rot. We put the mapping in the files themselves.**

Every script and document in this repository declares — in its own header — what it reads from (`Backward:`) and what reads from it (`Forward:`). When a file is edited and its inputs or outputs change, the declaration moves with it. There is no central dependency map to keep in sync.

This file is the rule. It is itself a leaf: it has no upstream, and its downstream is "every contributor and reviewer who reads it before opening a file."

---

## The format

Two grep-able keys, indented two spaces, one path per line. Comment after `—` if useful.

```
Backward:
  path/to/input.csv                              — what this file reads in
  analysis/scripts/upstream_script.py            — produces this file's input

Forward:
  path/to/output.json                            — what this file writes out
  findings/some_consumer.md                      — narrative consumer of the output
  (terminal — leaf node, reviewer-facing only)   — when there are no programmatic consumers
```

**Why this format:**

- `Backward:` / `Forward:` matches the convention already in use across 95 of the repository's 102 Python scripts (as of 2026-05-23). Choosing it over `Upstream:` / `Downstream:` avoided 95 edits.
- Two-space indent + bare path lets `grep -A20 "Backward:" file` return the entire block cleanly. No need for a parser.
- Inline `— comment` is optional and ignored by grep targeting paths.

---

## Where the block goes

### Python files

Inside the module docstring, at the bottom. Existing convention:

```python
"""
script_name.py — short description
=====================================
...module-level prose explaining what it does...

Backward:
  data/inputs/foo.gpkg
  analysis/scripts/upstream.py

Forward:
  data/outputs/bar.csv
  findings/consumer_analysis.md
"""
```

### Markdown files

Below the YAML frontmatter (if present), above the H1 title, inside a top-of-file block. Pattern:

```markdown
---
name: Analysis title
description: ...
type: project
---

> **Backward:**
> - `analysis/scripts/companion.py` — produces this file's headline numbers
> - `data/outputs/companion_output.csv` — per-row data summarized below
>
> **Forward:**
> - `reports/academic/report_academic.md` §5.8.X — incorporates this finding
> - `findings/cross_reference.md` — discusses the implications

# Analysis title
```

---

## Leaf nodes (terminal files)

Files with no programmatic downstream — public reports, infographics, README, the technical monograph — declare themselves as **leaves**:

```
Forward:
  (leaf — reviewer-facing / external consumers only)
```

This is **not** the same as omitting the `Forward:` block. A leaf is a deliberate terminal classification; an omitted block is undocumented and a defect. `grep -L "Forward:"` finds defects.

---

## Special cases

**Utility modules (`palette.py`, helper libraries).** Backward is usually `(none — utility module / constants)`. Forward is the list of importers, or `(any script in analysis/scripts/)` if it's broadly imported. Example:

```python
"""
palette.py — colour constants used by report-figure scripts.

Backward:
  (none — utility module, no data inputs)

Forward:
  (any analysis/scripts/*.py that builds figures; broad utility import)
"""
```

**Narrative-only `.md` files (retrospectives, Q&A docs, status reports).** Still get a `Backward:` / `Forward:` block. Their backward is "the analyses they discuss"; their forward is usually "(leaf — narrative / human reader)". Even pure narratives declare, because the goal is "I can move up and down the chain from any file."

**Retraction logs, changelogs.** Backward is "the files documenting the retracted findings"; forward is "(leaf — retraction record)".

---

## When the convention is violated

If a file edits change what it reads or writes:

1. Update the file's own `Backward:` / `Forward:` block.
2. Update the block in each file appearing in the changed direction (i.e., if you added a new output, the consumer of that output gets a new `Backward:` entry).
3. No central map to update.

If a file is renamed or moved, every other file referencing it needs its declaration updated. `grep -rln "old/path/name"` finds them.

---

## How this audit was conducted

The repository's dependency-declaration coverage was audited on 2026-05-23:

- **Python:** 95 / 102 scripts already declared dependencies. The 7 outliers were small utilities (`palette.py`, `check_voice_and_readability.py`, etc.) that have since been given dependency blocks for completeness, even where the block is `(none — utility module)`.
- **Markdown:** 42 / 162 declared dependencies. The remaining 120 were brought into compliance in a documentation pass, with most acquiring `Forward: (leaf — narrative)` or `Forward: (leaf — reviewer-facing)`.

After that pass, `grep -rL "Backward:" analysis/scripts/*.py` and the equivalent for `.md` files should return nothing. If they do, the convention has drifted.

---

Backward:
  (none — this file is the convention; it depends on nothing)

Forward:
  (leaf — read by every contributor and external reviewer; not consumed by any script)
