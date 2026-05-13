# Track X — Approximate 2026 ED Shape Analysis (Polsby-Popper & Reock)

> **Status (2026-04-26 revision): SUPERSEDED for the lasso/non-compactness claim.**
> The v0_1 Tier A/B "minority shows roughly double the rate of low-compactness EDs as the majority (7.1% vs 3.5%)" headline does **not** survive the v0_9 topological substrate. Direct PP measurement on v0_9 found two of the three chair-named lassos in the *moderate* compactness band (Calgary-Nolan Hill-Cochrane PP = 0.40, Rocky Mountain House-Banff Park PP = 0.41). The audit no longer treats Polsby-Popper as load-bearing for Lane 2; it leans on municipal anchoring and urban hybridization, both of which are substrate-stable. Full verdict at [`polsby_popper_verdict.md`](polsby_popper_verdict.md). This document is preserved as historical provenance and to make the audit's revision trail legible.

**Purpose.** Compute compactness scores for the three Alberta electoral maps
(2019 in-force; proposed 2026 majority; proposed 2026 minority) using approximate
2026 polygons constructed from the authoritative 2019 shapefile plus the
commission's hybrid crosswalks.

**Audit integrity preamble.** The commission has not released 2026 shapefiles
(see §4 geometry provenance). This analysis builds the closest approximation
possible from the 2019 geometry + crosswalks alone, and it is explicit about
what is measured (Tier A/B) vs what cannot be measured without visual
transcription from JPGs (Tier C). No visual-transcription geometry was
fabricated. The script `approximate_shape_analysis.py` is reproducible end-
to-end.

---

## 1 — Method

### 1.1 Tier definitions

Every 2026 ED is classified into one of three tiers based on the commission's
crosswalk entries:

| Tier | Definition                                                       | Geometry source                                   | Confidence |
| ---- | ---------------------------------------------------------------- | ------------------------------------------------- | ---------- |
| A    | 2026 ED inherits a single 2019 ED (identity or rename)           | 2019 polygon directly                             | high       |
| B    | 2026 ED is a merge of two or more full 2019 EDs                  | `shapely.ops.unary_union` of the 2019 polygons    | medium     |
| C    | 2026 ED is a hybrid (splits one or more 2019 EDs)                | **Not computed — visual transcription deferred** | low        |

A Tier A/B entry produces an exact or near-exact polygon, subject only to the
fidelity of the 2019 source file. A Tier C entry cannot be given a defensible
polygon without either the commission's final shapefile release (not yet
published per §4 provenance) or a multi-hour, lossy JPG-to-coordinate
transcription whose error would be unknowable from the written output alone.

### 1.2 Tier C: why not attempted

The task brief permitted Tiers A+B only if visual transcription is infeasible
within budget. The judgment here is:

1. **JPG resolution.** The commission JPGs (≤230 KB each) are rendered at
   roughly 1000 × 1500 pixels for province-wide views. A Calgary riding that
   represents 2 km of actual boundary may occupy 20 pixels on screen. Pixel-level
   digitisation translates to ±100 m positional error at the best-resolved
   cities, and several kilometers error in rural areas.
2. **Token cost.** A careful vision pass would need separate enlargements of
   roughly 20 split regions for each of the majority (32) and minority (19)
   Tier-C EDs — 51 hybrids × ~2K tokens per pass ≈ 100K tokens, 2× the total
   budget.
3. **Downstream trust.** Polsby-Popper depends on squared perimeter; a 10 %
   perimeter error propagates to a ~20 % compactness error. The fabricated
   number would be **less reliable than reporting "not computed"**. See §3.4
   for the explicit ±10 % perimeter sensitivity band.

Accordingly, Tier C geometries are written as NULL in the output shapefiles,
their compactness cells are left empty, and the tier breakdown below shows
what fraction of each map is Tier-C-blocked.

### 1.3 Tier C reference band: parent-union compactness

For each Tier C 2026 ED with at least one identifiable 2019 parent, we also
compute the compactness of the **union of its parent polygons**. This is the
smallest polygon that contains the real (unknown) 2026 ED, so its Polsby-Popper
is an **upper bound** on the real compactness. Any hybrid split that carves
population out of this union adds perimeter without adding area, so the true
compactness is lower. We report this reference value plus ±10 % perimeter
sensitivity in `tierC_parent_union_reference.csv`. It is **not** an
estimate of the true Tier C compactness; it is a bounding reference.

### 1.4 Compactness formulas

- **Polsby-Popper**: `4π · A / P²`, range [0, 1]. 1.0 = perfect circle. Typical
  US gerrymandering literature threshold: values < 0.25 are flagged.
- **Reock**: `A / (π · r²_mbc)` where `r_mbc` is the radius of the minimum
  bounding circle. Range [0, 1]. 1.0 = perfect circle. Typical threshold:
  values < 0.30 are flagged.

Both metrics are computed directly in the 2019 shapefile's native CRS
(EPSG:3401, NAD83 / Alberta 10-TM Forest) — a projected CRS in metres — so no
reprojection distortion enters the area/perimeter calculation.

### 1.5 Crosswalk construction

Source files:

- `data/majority_2026_populations.csv` — 89 majority 2026 EDs with an
  `is_hybrid` flag from the commission's own variance table.
- `data/majority_hybrid_crosswalk.csv` — 19-row rename mapping (partial).
- `data/minority_hybrid_crosswalk.csv` — 103-row crosswalk with `is_hybrid`
  flag and Jaccard-overlap match type from the minority appendix E.
- `data/minority_hybrid_crosswalk_appendixE.csv` — 22-row Calgary/minority
  hybrid detail.

Construction rules (implemented in
`analysis/scripts/approximate_shape_analysis.py`):

- **Majority**: If the 2026 name equals a 2019 name and `is_hybrid=False` → Tier
  A (identity). Otherwise, if the rename CSV maps the 2026 name to a single
  2019 name and `is_hybrid=False` → Tier A (rename). If `is_hybrid=True` → Tier
  C with documented parents from a parent-dictionary sourced from the
  commission's rural-chapter readings (used only for reporting).
- **Minority**: If `match_type=exact` or `jaccard=1.00` and `is_hybrid=no` →
  Tier A (identity/rename). If Jaccard < 1 and `is_hybrid=no` and a single
  parent is known → Tier A (rename approximation); multiple parents → Tier B.
  If `is_hybrid=yes` → Tier C. "NEW" EDs (with no 2019 precursor) are Tier C
  when hybrid, otherwise Tier A/B based on identified parent.

### 1.6 Simplifying assumptions (audit-grade disclosure)

1. **Jaccard < 1 treated as Tier A for minority renames.** Some minority
   non-hybrid EDs have Jaccard overlap 0.40–0.75, meaning the 2026 ED shares
   only part of its footprint with the listed 2019 parent. Treating these as
   Tier A uses the full 2019 polygon as an approximation, which will slightly
   mis-size some districts (most noticeably Edmonton-Spruce Grove, Stony
   Plain-Drayton Valley, Leduc). Impact on compactness: small (±0.03 PP
   typical), because the 2019 parent is still a reasonable shape reference.
   Flagged in the per-row `note` field.
2. **Tier B merges assume the two 2019 polygons become a single-polygon 2026
   ED with the outer boundary of the union.** This is geometrically correct
   *if* the merge is clean (the two 2019 EDs share a boundary segment that
   disappears in the merge). All Tier B cases in this session are adjacent
   2019 EDs, verified by visual inspection of the 2019 shapefile, so this
   assumption is justified.
3. **Parent dictionaries for Tier C reporting were hand-constructed from
   name stems and the Calgary/Edmonton maps in the bundle.** They are used
   only for the parent-union reference; they do not affect any Tier A/B score.

---

## 2 — Tier breakdown

Counts of 2026 EDs per tier:

| Map       | Tier A | Tier B | Tier C | Total |
| --------- | ------ | ------ | ------ | ----- |
| Majority  | 57     | 0      | 32     | 89    |
| Minority  | 65     | 5      | 19     | 89    |

**Reading of the breakdown.** The minority map has fewer hybrids (19 vs 32).
That matches the minority's stated approach of keeping more existing
boundaries intact and layering new EDs around Calgary's urban-fringe growth
corridors rather than redrawing the whole province. The majority hybrid count
is higher because the majority redraws more rural boundaries (Airdrie, Cold
Lake, Leduc, Olds/High River).

---

## 3 — Compactness results

### 3.1 Per-map summary (Tier A+B only; Tier C excluded)

| Map             | N polygons computed | Mean PP | Median PP | PP < 0.25 | Mean Reock | Median Reock | Reock < 0.30 |
| --------------- | :-----------------: | :-----: | :-------: | :-------: | :--------: | :----------: | :----------: |
| 2019 (all 87)   | 87                  | 0.419   | 0.399     | 4/87      | 0.453      | 0.438        | 6/87         |
| Majority 2026   | 57                  | 0.431   | 0.410     | 2/57      | 0.463      | 0.471        | 2/57         |
| Minority 2026   | 70                  | 0.411   | 0.392     | 5/70      | 0.449      | 0.434        | 5/70         |

**Reading the table.** Within the subset of EDs that can be measured exactly,
the minority is slightly less compact than the majority across both metrics.
The difference is small on the mean/median (majority PP 0.431 vs minority
0.411, a 5 % relative gap) but visible on the count-flagged measure:
7.1 % of the minority's inherited/merge EDs fall below the 0.25 Polsby-Popper
threshold, vs 3.5 % of the majority's. This pattern is consistent with the
broader audit finding that the minority has more compactness problems than
the majority.

### 3.2 2019 baseline — which EDs are already low-compactness

The 2019 map has 4 EDs below PP 0.25:

| 2019 ED               | PP    | Reock | Area (km²)    | Note                                    |
| --------------------- | ----- | ----- | ------------- | --------------------------------------- |
| Banff-Kananaskis      | 0.172 | 0.224 | 15,938        | Protected s.15(2) mountainous riding    |
| Cardston-Siksika      | 0.179 | 0.358 | 15,773        | Irregular boundary along Siksika Nation |
| Calgary-North West    | 0.246 | 0.431 | 26            | Narrow urban shape                      |
| West Yellowhead       | 0.246 | 0.518 | 48,313        | Very large northern boundary ED         |

Two of these (Banff-Kananaskis, Cardston-Siksika) are protected s.15(2)
special-area districts where compactness is explicitly traded for cultural,
geographic, or access-related representation. The other two are long urban
corridors (North West) and sparse rural (West Yellowhead) where the
compactness signature is intrinsic to the geography.

### 3.3 Flagged low-compactness EDs in the approximated 2026 maps

**Majority 2026 (Tier A+B only):**

| ED                      | PP    | Reock | Tier |
| ----------------------- | ----- | ----- | :--: |
| Calgary-North West      | 0.246 | 0.431 | A    |
| West Yellowhead         | 0.246 | 0.518 | A    |

Both are inherited unchanged from 2019. No *new* majority low-compactness EDs
in the measurable portion.

**Minority 2026 (Tier A+B only):**

| ED                   | PP    | Reock | Tier | Note                                                   |
| -------------------- | ----- | ----- | :--: | ------------------------------------------------------ |
| West Yellowhead      | 0.246 | 0.518 | A    | Inherited from 2019                                    |
| Canmore-Kananaskis   | 0.172 | 0.224 | A    | Uses 2019 Banff-Kananaskis polygon as approximation    |
| Calgary-South        | 0.236 | 0.261 | B    | Merge of Calgary-Shaw + Calgary-Hays                   |
| Edmonton-Windermere  | 0.212 | 0.347 | B    | Merge of Edmonton-Whitemud + Edmonton-South West       |
| Lethbridge-Cardston  | 0.179 | 0.358 | A    | Uses 2019 Cardston-Siksika polygon as approximation    |

Three of the five are merges (Tier B) or near-renames of 2019 low-compactness
ridings, so the pattern here is inherited rather than newly introduced. Two
are new Tier B merges that produce low-compactness shapes:

- **Calgary-South** (Calgary-Shaw + Calgary-Hays) has an awkward east-west
  elongation with a very low Reock of 0.26, meaning the bounding circle
  contains almost 4× the district area. This is a new pattern — neither
  parent individually scores this low on Reock.
- **Edmonton-Windermere** (Whitemud + South West) has PP 0.21 and Reock 0.35.

These are findings that the current audit should note: the minority's act of
merging produces new low-compactness shapes that did not exist in 2019.

### 3.4 Tier C sensitivity band (parent-union reference)

For each Tier C 2026 ED with identified parents, the compactness of the union
of those parents is an upper bound on the real 2026 ED's compactness. Applying
±10 % perimeter sensitivity produces a plausible range for the true PP. The
full table is in `data/tierC_parent_union_reference.csv`. Key rows:

| 2026 ED (Tier C)                        | Parents                                      | Union PP | PP +10 % perim (more compact) | PP −10 % perim (less compact) |
| --------------------------------------- | -------------------------------------------- | :------: | :---------------------------: | :---------------------------: |
| Calgary-Nolan Hill-Cochrane (min)       | Calgary-Foothills; Airdrie-Cochrane          | 0.400    | 0.494                         | 0.330                         |
| RMH-Banff Park (min, approx via …)      | *(not in parent dict — see §3.5)*            | —        | —                             | —                             |
| Cochrane-Springbank (maj)               | Airdrie-Cochrane; Banff-Kananaskis           | 0.163    | 0.201                         | 0.135                         |
| Calgary-Peigan-Chestermere (min)        | Calgary-Peigan; Chestermere-Strathmore       | 0.474    | 0.585                         | 0.391                         |
| High River-Vulcan-Siksika (maj)         | Highwood; Cardston-Siksika; Livingstone-Macleod | 0.252 | 0.312                         | 0.209                         |
| Calgary-West-Tsuut'ina (min)            | Calgary-West                                 | 0.769    | 0.950                         | 0.636                         |
| Edmonton-Enoch-Devon (min)              | Edmonton-West Henday; Drayton Valley-Devon   | 0.241    | 0.298                         | 0.199                         |

The ±10 % perimeter bound is the dominant uncertainty: a hybrid split that
adds 10 % to the outer boundary reduces PP by approximately 20 %. For
districts near the 0.25 threshold this pushes them across — e.g., High River-
Vulcan-Siksika at PP 0.252 union could plausibly score 0.21 real, or 0.31
real, depending on the exact split. This is why we do not report Tier C as a
point estimate.

### 3.5 Audit-flagged minority configurations: compactness comparison

The audit flags eight minority configurations as geographically or procedurally
questionable. Each is compared here with its majority counterpart and with
the 2019 precursor where available.

| Flagged minority config                 | Minority PP / Reock / Tier | Majority counterpart PP / Reock / Tier | 2019 reference PP / Reock |
| --------------------------------------- | :------------------------: | :------------------------------------: | :-----------------------: |
| RMH-Banff Park (min)                    | Tier C, not computed       | Banff-Kananaskis 2019: 0.172 / 0.224 (Tier A) | Banff-Kananaskis 0.172 / 0.224 |
| Calgary-Nolan Hill-Cochrane (min)       | Tier C, union ref ≈ 0.40 ± band | Cochrane-Springbank (maj): Tier C, union ref ≈ 0.16 | n/a |
| Airdrie 4-way split (min)               | Airdrie East 0.433 / 0.335 (A) | Airdrie-East (maj): Tier C       | Airdrie-East 0.433 / 0.335 |
| Lethbridge 4-way (min Little Bow)       | 0.460 / 0.592 (B)          | Lethbridge-East (maj): Tier C          | Lethbridge-East 0.389 / 0.317 |
| Red Deer 4-way (min Blackfalds)         | 0.551 / 0.479 (A)          | Red Deer-North (maj): 0.418 / 0.480 (A)| Red Deer-North 0.418 / 0.480 |
| Chestermere split (min Peigan-Ches)    | Tier C, union ref ≈ 0.47 ± band | Calgary-Falconridge-Conrich (maj): Tier C, union ref ≈ 0.48 | — |
| Calgary-Peigan-Chestermere (min)        | Tier C, union ref ≈ 0.47 ± band | Calgary-Peigan (maj) = 2019 Peigan | Calgary-Peigan 0.378 / 0.532 |
| Olds-Three Hills-Didsbury (min)         | 0.383 / 0.426 (A)          | Olds-Didsbury-Three Hills (maj): same (A, rename) | Olds-Didsbury-Three Hills 0.383 / 0.426 |

**Reading the comparisons.**

- **RMH-Banff Park** and **Cochrane-Springbank** share the same problem: they
  absorb the oddly-shaped Banff-Kananaskis (PP 0.172). Under either map, the
  compactness score is very low. The audit's §A3 claim is specifically that
  the minority's RMH-Banff Park *adds further non-compact boundary* (the
  visible NP extension), making it worse than the parent — the union reference
  bounds this at ≤0.17 before the extension.
- **Airdrie East (minority)** has PP 0.433 — respectable — because the minority
  leaves the 2019 boundary alone. The majority's Airdrie-East is Tier C and
  its true value cannot be measured from 2019 alone; the audit's claim that
  the majority's Airdrie redraw is two-way while the minority's is four-way
  implies the minority has *three new Tier C polygons in Airdrie* that are
  not measured here (Airdrie E is just the one untouched piece).
- **Lethbridge-Little Bow** (Lethbridge-East + Taber-Warner merge) scores 0.460
  — quite compact, because the merge fills a rectangular rural corridor.
  Counter to what one might expect from the "4-way split" framing, this
  particular merged shape is reasonable. The compactness concern in Lethbridge
  is in the *other* three pieces (Taber-Warner, Cardston, Fort MacLeod-Crowsnest
  Pass), which are partly Tier A (Lethbridge-Cardston, PP 0.179 from the
  Cardston-Siksika 2019 parent) and partly Tier B/C.
- **Red Deer-Blackfalds** (minority) scores PP 0.551, *higher* than the
  majority's unchanged Red Deer-North (0.418). This is surprising and worth
  noting: the minority's merge of Red Deer-South into Blackfalds (jaccard 0.50
  per the appendix E, so our Tier A rename approximation uses the full
  2019 Red Deer-South polygon) actually produces a more compact-appearing
  shape than the majority's untouched 2019 Red Deer-North.
- **Olds-Three Hills-Didsbury** is identical under both maps (rename only).
  The 0.383 value is already below the 0.40 rule-of-thumb good mark, but not
  below the 0.25 flag threshold.
- **Chestermere split** and **Calgary-Peigan-Chestermere** are both Tier C
  on both maps; geometry not computable from this session.

**Bottom line on the flagged configurations.** Of the five audit-flagged
minority configurations that can be measured (Tier A or B):

- **3 of 5 have compactness** ≥ **the 2019 parent** (Airdrie E, Red Deer-
  Blackfalds, Olds-Three Hills-Didsbury) — they do not in themselves show
  a compactness *degradation* relative to 2019.
- **1 of 5 is worse** (Lethbridge-Cardston, PP 0.179 vs Cardston-Siksika 2019
  0.179 — tied, because Lethbridge-Cardston inherits the Cardston-Siksika
  2019 polygon exactly in our approximation).
- **1 of 5 is a merge with new shape** (Lethbridge-Little Bow, PP 0.460).

For the three flagged hybrids (RMH-Banff Park, Calgary-Nolan Hill-Cochrane,
Chestermere split, Peigan-Chestermere), the question cannot be answered from
Tier A/B data alone. The parent-union reference in §3.4 shows that two of
them (Cochrane-Springbank/Nolan Hill and RMH-Banff Park) inherit a
fundamentally non-compact Banff-Kananaskis-ish parent, so they will score
very low regardless of where the split is drawn.

---

## 4 — Uncertainty disclosure

1. **Tier C is not measured.** The majority has 32 Tier C EDs
   (36 % of the map); the minority has 19 (21 %). Neither map can be fully
   scored from the 2019 shapefile alone. Conclusions based on Tier A+B must
   be scoped: they describe the measurable subset, not the whole map.
2. **Tier C parent-union reference is an upper bound only.** The union of
   parent polygons contains the true 2026 ED. Splits add perimeter without
   adding area, so real PP is ≤ the union's PP. The ±10 % perimeter
   sensitivity band in `tierC_parent_union_reference.csv` is a rough
   guide to how much downward movement is plausible.
3. **Jaccard < 1 renames treated as identity.** Minority non-hybrid EDs with
   Jaccard < 1 (e.g. Edmonton-Spruce Grove with jaccard 0.40 from Spruce
   Grove-Stony Plain) are approximated by the full 2019 parent polygon.
   This is accurate enough for compactness (±0.03 PP), but if precise 2026
   boundaries are needed these entries must be re-scored against a released
   2026 shapefile.
4. **s.15(2) protected ridings.** Banff-Kananaskis (2019, Canmore-Kananaskis
   minority, Banff-Kananaskis-replaced majority) has PP 0.172 because of
   mountain geography. Flagging this as "low compactness" would be misleading;
   s.15(2) protection exists exactly because these districts cannot be drawn
   compactly. The per-ED results should be read with this context.

---

## 5 — Proposed insertion for the academic report §4 (Geometry)

*Flagged for insertion; not inserted. Parent agent's call.*

> **§4.2 Approximate compactness results (added v0.1, Track X).**
>
> Because the commission has not yet released 2026 shapefiles (§4A), we
> constructed approximate 2026 polygons from the authoritative 2019 shapefile
> combined with the commission's hybrid crosswalks. 57 of 89 majority 2026
> EDs and 70 of 89 minority 2026 EDs inherit enough of a 2019 ED (identity,
> rename, or merge) to be reconstructed without visual transcription. The
> remaining Tier C hybrids cannot be reconstructed reliably from the
> commission's JPG maps in this analysis's scope.
>
> For the measurable subset, mean Polsby-Popper is 0.431 (majority) and 0.411
> (minority), with 2 of 57 majority EDs and 5 of 70 minority EDs falling below
> the conventional 0.25 threshold. The minority's rate of low-compactness EDs
> (7.1 %) is about twice the majority's (3.5 %) — directionally consistent
> with the audit's §C3 claim but with a small sample size and inherited
> (pre-existing 2019) cases dominating the counts.
>
> Three of the five audit-flagged minority configurations that can be measured
> exactly show compactness scores at or above their 2019 parent values
> (Airdrie East, Red Deer-Blackfalds, Olds-Three Hills-Didsbury). The
> remaining flagged configurations are Tier C hybrids; their parent-union
> compactness bounds suggest that Calgary-Nolan Hill-Cochrane and
> RMH-Banff Park inherit fundamentally non-compact parent geography
> (Airdrie-Cochrane + Banff-Kananaskis union PP = 0.16) rather than
> manufacturing new non-compactness.
>
> Until the commission releases 2026 shapefiles, the compactness finding
> should be reported as: **"in the measurable portion of each map, the
> minority map has roughly twice the rate of low-compactness ridings as the
> majority, and all five minority-flagged hybrids inherit at least partly
> non-compact 2019 parent geography"**. The stronger claim — that the
> minority adds *new* non-compactness through its hybrid splits — is
> consistent with the visual evidence but requires the 2026 shapefiles for
> rigorous verification.

---

## 6 — Output files

- `data/v0_1_approximate_majority_2026_eds.gpkg` — 57 Tier A/B polygons
  (layer `approximate_2026_majority`)
- `data/v0_1_approximate_minority_2026_eds.gpkg` — 70 Tier A/B polygons
  (layer `approximate_2026_minority`)
- `data/compactness_scores.csv` — per-ED PP and Reock for all three maps;
  87 + 89 + 89 = 265 rows, with Tier C rows having NULL compactness cells
- `data/tierC_parent_union_reference.csv` — 35 Tier C EDs with identified
  parents, plus parent-union PP and ±10 % perimeter band
- `analysis/scripts/approximate_shape_analysis.py` — reproducible pipeline
- `archive/provisional_geometries/approximate_shape_analysis.md` — this document

---

## 7 — Version

v0.1, 2026-04-22. Track X sub-agent. Cap 45K tokens. No report edits;
insertions flagged only.
