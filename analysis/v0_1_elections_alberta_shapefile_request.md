---
name: Elections Alberta shapefile request email
description: Draft request to Elections Alberta asking for early release or research access to the 2026 majority and minority electoral-division shapefiles for academic analysis. Non-partisan, educational-use framing.
forward_dependencies:
  - PO review / send
  - Shapefile release would unblock Phase 4/5 (measured vote attribution, Polsby-Popper, Reock, GerryChain ensemble)
backward_dependencies:
  - analysis/v0_1_approximate_shape_analysis.md (Track X — documents the gap the shapefiles would fill)
  - analysis/v0_1_uncertainty_and_shapefile_impact.md (what the audit cannot do without shapefiles)
---

# Elections Alberta shapefile request — email draft

**Status:** Draft. PO review required before sending.

**Recipient options (in order of likely effectiveness):**
1. **Chief Electoral Officer of Alberta** — Gordon McClure, via `elections.alberta@gov.ab.ca` or the Elections Alberta general contact form at `https://www.elections.ab.ca/contact/`
2. **GIS and Data Coordination team, Elections Alberta** — the team that produced the 2019 and 2023 shapefiles currently published at `https://www.elections.ab.ca/resources/maps/`. Staff credited in the Alberta Electoral Boundaries Commission 2025-26 final report (pp. iv–v): Raymond Mok, Sarah Cirka, and Meghan Pittman (Technologists).
3. **Alberta Electoral Boundaries Commission** (via the commission secretariat, if still staffed)
4. **Access to Information and Privacy Coordinator** (as a formal FOIP request if informal channels decline)

**Recommended first approach:** informal email to Elections Alberta GIS team (option 2), cc Chief Electoral Officer (option 1). Professional, narrow ask, non-partisan framing. If no response within 2 weeks, escalate to formal FOIP request.

---

## Email draft

**Subject:** Research access request — 2026 Electoral Boundaries Commission shapefiles (majority and minority recommendations)

Dear Elections Alberta GIS and Data Coordination team, and Chief Electoral Officer McClure:

I am Will Conner, a fourth-year Bachelor of Science (Computer Information Systems) student at Mount Royal University. I am writing to request research access to the electoral-division shapefiles associated with the 2025-26 Electoral Boundaries Commission's majority and minority recommendations.

I am conducting a non-partisan academic audit of the Commission's two recommended maps using public data, reproducible code, and the symmetric-methodology discipline described in the political-science gerrymandering literature (Stephanopoulos & McGhee 2015; Warrington 2018; Chen & Rodden 2013, 2015). The audit's public repository, reports, and reproducible pipeline are at `https://github.com/Ixby/alberta-electoral-boundaries-audit`.

Several analytical tools that are standard in modern redistricting scholarship require the actual polygon geometries for the proposed electoral divisions, not just the population tables from the Commission's published variance tables. These include:

1. **Polsby-Popper and Reock compactness scores** — measures how regularly-shaped each district is. Low scores flag unusual boundary shapes that may warrant additional scrutiny.
2. **Markov Chain Monte Carlo neutral-ensemble analysis** (Chen & Rodden 2015; Magleby & Mosesson 2018) — generates thousands of alternative rule-respecting districting plans and places each commission proposal as a percentile against the neutral distribution. This is the standard tool modern US courts and academics use to distinguish engineered partisan maps from natural voter-geography effects.
3. **Precise voting-area-to-electoral-division attribution** — currently the audit uses hybrid-level crosswalks extracted from the Commission's Appendix C (majority) and heuristic name-matching (minority). Precise shapefile-based attribution would remove this approximation.

Without the polygon shapefiles, the audit has instead produced approximate district boundaries by combining the 2019 published shapefile, the Commission's hybrid crosswalks, and visual interpretation of the Commission map JPGs. These approximations carry documented uncertainty (see `analysis/v0_1_approximate_shape_analysis.md` in the repository). Precise shapefiles would let the audit replace these approximations with measured results.

The audit is non-partisan and has been designed to be applied identically to the majority and the minority map. The code is public. Any party receiving the shapefiles for the same research purpose would reach the same numerical results.

I am aware that Elections Alberta may not have a standing policy for releasing commission-proposed-but-not-yet-legislated boundaries. If the request is not appropriate under current protocols, I would welcome guidance on either:

- A research-access arrangement with reasonable terms (e.g., non-redistribution, academic-use-only, acknowledgement in any derivative work, deletion on request)
- A formal Freedom of Information and Protection of Privacy (FOIP) request procedure, if that is the correct channel
- Any alternative data format that would serve the same analytical purpose (geo-referenced PDF; GeoJSON; shapefile, preferably in NAD83 / Alberta 3TM, EPSG:3776)

The audit will cite Elections Alberta as the data source on any analysis that uses the shapefiles, and will publish full methodology and results in the public repository above. I am happy to provide further information about the audit's scope, a summary of intended analyses, or a preview of the reports currently in draft form if that would help.

Thank you for considering this request. I understand Elections Alberta receives many inquiries and appreciate the time.

Sincerely,

Will Conner  
Bachelor of Science — Computer Information Systems (4th year)  
Mount Royal University  
[email address]  
[phone, optional]

Repository: `https://github.com/Ixby/alberta-electoral-boundaries-audit`

---

## Reasoning notes (for PO, not to be sent)

**What to watch for in the response:**

- **Yes, with conditions:** likely a non-redistribution clause, acknowledgement-in-output requirement, and maybe a non-partisan-use affirmation. All acceptable.
- **Yes, via FOIP:** standard process; 30-day response window; possibly a small fee. Worth pursuing if informal is declined.
- **Not yet released, come back when legislated:** most likely polite decline. Response is to thank them and note the audit will proceed on approximations until legislation.
- **No access under any timeline:** unlikely, but if so the FOIP route becomes the formal escalation.

**What the PO should consider before sending:**
- Whether to use the PO's personal email or the Mount Royal institutional email (latter may carry more weight).
- Whether to attach a one-page summary of the audit's methodology and findings to date.
- Whether to cc a Mount Royal faculty sponsor, if one is available — would strengthen the research-access framing.
- Whether to time the send for a weekday morning (slightly higher open-rate than Friday afternoon).

**If shapefiles arrive:** the repository's existing pipeline is ready to ingest them. Specifically, `analysis/v0_1_a1_legal_baseline_2021_census.py` already demonstrates DA-level overlay against 2019 shapefiles; the same pipeline extended to the 2026 shapefiles would produce measured-rather-than-approximated results within 2–4 hours of compute.

**Escalation path if declined:**
1. Informal email to commission secretariat (different team, same underlying data).
2. FOIP request with narrow scope ("polygon geometries for the 89 proposed electoral divisions in the majority report and the 89 proposed electoral divisions in the minority report, in any standard GIS format").
3. Contact political-science faculty at University of Alberta, University of Calgary, or Mount Royal with active redistricting research — they may have existing Elections Alberta relationships.
4. Journalistic-use-based request via a reporter covering the file (the commission report has received substantial media attention; a newsroom with existing FOIP workflows could pursue on a faster timeline).
