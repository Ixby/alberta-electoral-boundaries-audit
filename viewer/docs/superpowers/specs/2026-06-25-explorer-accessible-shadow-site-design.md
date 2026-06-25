# Accessible Shadow Site for the Map Explorer — Design

**Date:** 2026-06-25
**Status:** Approved (brainstorm) — ready for implementation plan
**Goal:** Give blind / screen-reader users equivalent access to the *information* the deck.gl map explorer conveys, via a dedicated, navigable text page.

## Problem

The explorer is a WebGL `<canvas>` — a single opaque element to assistive tech. ARIA on the canvas cannot expose its content. A blind user currently gets nothing from the visualization.

## Decisions (from brainstorm)

1. **Target experience:** an accessible **content layer** — read/explore the audit's substance non-visually. *Not* making the canvas keyboard-operable.
2. **Placement:** a **dedicated accessible route** `/explorer/text` — a standalone, complete, static representation independent of canvas state ("embedded shadow site").
3. **Structure:** **anomaly-first** — lead with the flagged boundaries (each EBC '26 annotation as its own section), then a full district directory.

## Architecture

- New prerendered SvelteKit route `/explorer/text` (adapter-static), real HTML document.
- i18n via the existing `t()` system: first-class **en + fr** (fr is human-reviewed), other locales fall back to English.
- No WebGL, no map-state coupling, no live regions — fully static, robust.
- Landmarks: `<header>`, `<nav>` (in-page TOC), `<main>`, `<footer>`. Descriptive `<title>`; correct `lang`.

## Discoverability

- On `/explorer`, the **first focusable element** is a visually-hidden-until-focused link: "Open the accessible text version of this map." Plus a visible link in the control panel.
- The canvas gets `role="img"` + a concise `aria-label` summary pointing to the text version.
- Reciprocal links: text page ↔ interactive map ↔ full report.

## Heading hierarchy

```
h1   Alberta Electoral Boundary Audit — map, text version
       intro + links (interactive map, full report)
nav  "On this page" — in-page TOC (jump links)
h2   Flagged boundaries (EBC '26 Annotations)
   h3  <one per flagged boundary>
         · what the map shows here
         · why it's flagged (annotation explanation, reused from locale keys)
         · version(s) & district(s) affected
h2   District directory
   <table> all 89 districts (see "Table semantics")
h2   How to read this / methodology note + links back
```

## Table semantics

- Real `<table>` + `<caption>`; `<th scope="col">` column headers; `<th scope="row">` district name per row.
- **Default: one combined table** — district rows × version-grouped columns (lets a blind user compare a district across the three maps in one row). *Open to switching to three per-version tables if preferred.*
- Sorted alphabetically (predictable); **flag status as a column** so flagged districts are findable.

## Reuse, not rewrite

- Annotation explanations: reuse the existing POI/tooltip locale keys (single source of truth, gets fr free).
- District names per version: reuse the explorer's label data.
- **Default: link to the report's narrative findings, do not re-summarize** them here (avoid duplication; the annotation sections carry the spatial substance). *Open to a short summary if preferred.*

## Data dependency (resolve in plan)

Per-district **numeric** data (votes/percentile per version): annotation text + district names are available; per-district vote figures are rendered at VA level and aggregated on hover. **Verify** whether a clean ED-level dataset exists. If not cheap to produce, the directory scopes to **name + flag status + link to the report's data tables** — structure is unchanged either way.

## Non-goals

- Canvas keyboard operability; live-sync to map state; data export.

## Verification

- Conformance: axe / Lighthouse snapshot (target 100), heading-order + landmark checks, manual structural review.
- **Conformance ≠ usefulness.** Final gate is a real screen-reader pass (NVDA / VoiceOver), ideally by a blind user or a project reviewer. Build to verified-conformant; state plainly that the human AT pass is the sign-off.
