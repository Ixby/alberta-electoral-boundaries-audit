# Governance log — EBCA s.15(2) in the Amendment 17 nk chains

Started 2026-10-29 ~20:20 MT. Mode: interactive. Owner: Wuff (Will).
Owner rulings carried in: "we want to be as strict as the statue, no more, no less";
"i rather see what we can see than have not bothered to look"; s.15(2) = "Build it".
Statute text source: repo VERIFIED-PRIMARY extracts (proposals/site_rewrite_2026-10-29/legal_framework.md §B,
preregistration/terms_of_reference.md). Not re-checked against King's Printer this session.

## 1. Question  (GATE — awaiting owner)

**Testable outcome.** A `--s152` option for close_seats_ensemble.py nk chains such that, on a test run:
1. every sampled plan has all divisions within ±25% of average except at most 4, each of which is
   25–50% *below* average and meets ≥3 of the 5 s.15(2) criteria under documented predicates;
2. the chain actually reaches such plans (s.15(2) divisions observed in the test run, count > 0);
3. the criteria predicates reproduce the repo's own criterion-by-criterion assessment of the real
   maps' s.15(2) divisions (analysis/methodology/population_deviation_reaudit.md) — any mismatch is
   explained or fixed;
4. resume is still byte-identical; the default path (no flag) is still byte-identical to today.

**Constraints.** Pins unchanged (gerrychain 0.3.2 etc.). Nothing committed/pushed (Audit session lands it).
Pre-registration: design logged in the amendment log before any ensemble-vs-real-map comparison.
Deadline Monday 2026-11-02 morning.

**Out of scope.** s.14 factors (permissive "may"); the municipality-aware set is a separate sensitivity.
Changing the canonical 1.01M ensemble.

**Interpretations needing the owner (statute is literal; these are where literal is ambiguous):**
- Opinion gate ("if the Commission is of the opinion that at least 3 ... exist"): model as
  criteria-met ⇒ permitted (never required).
- (c) "no town ... exceeding 8,000": literal = municipal status *town* (CSD type T), not cities;
  s.15(3) excluding Crowsnest Pass (a specialized municipality) supports the municipal-status reading.
  Whole-town population, town counted if any part lies in the division.
- (a) only the 20,000 km² area limb is computable; the 15,000 km² surveyed-area limb is not (no data).
- (b) "most direct highway route" to the nearest boundary point: approximated as OSM road-network
  distance from the Legislature Building to the division's nearest VA.
- (d) reserves from CSD types IRI/S-É; Metis settlements are NOT in the CSD layer. RESOLVED
  2026-10-30 (owner: "lookup metis boundaries"): official GoA "Metis Settlement" polygons (all 8),
  data/shapefiles/reference/metis_settlements_dl/ + SOURCE.md (URL, retrieval time, licence).
- (e) VA boundary shares length with the provincial boundary.

**Known unknowns.** Split-rule cost (criteria evaluated per candidate cut); whether chains mix well
with the wider band; OSM network completeness for (b); Metis settlement source.

**Proportionality.** Full lifecycle warranted: it changes the null model that a public audit claim
rests on, and the criteria predicates are interpretive. Scaled: Plan + Baseline kept short.

**GATE PASSED 2026-10-29 ~20:25 — owner: "go"** (approves the testable outcome, full-lifecycle
proportionality, and the six readings as written; (d) since resolved with official Metis data).

## 2. Discover
## 3. Specify
## 4. Plan
## 5. Execute
## 6. Verify
## 7. Decide
## 8. Baseline
## 9. Operate
## 10. Learn
