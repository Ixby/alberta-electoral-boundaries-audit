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

- Criteria inputs built: `analysis/scripts/s152_criteria.py` → `data/outputs/s152_va_criteria.csv`
  (area_km2, road_km, big_town, reserve_or_metis, border per VA). Sources: VA layer (EPSG:3400),
  2021 CSDs, GoA Metis Settlement polygons, NRCan CLSS Aboriginal Lands (152 AB polygons), OSM highways
  (336,855-vertex network), Legislature 53.533694, −113.506611.
- Validation vs `population_deviation_reaudit.md`: CPN (both maps), Canmore-Banff, RMH-Banff Park match
  criterion-by-criterion. Lesser Slave Lake (b): literal nearest-boundary distance 113 km straight /
  134 km road < 150 → fails (b); commission/re-audit say P. Independently confirmed by Audit (133.9 km);
  registered as a disclosed difference; LSL still 3/5.
- Bug found: gerrychain `boundary_node` includes lake-hole VAs → (e) uses exterior rings only.
- Audit registers its own `s15_2_criteria.py` (different thresholds) as THE implementation for set D
  (Amendment 21: "one spec, one implementation"); this build becomes the independent cross-check.
- Mechanism constraints found in gerrychain 0.3.2: recom → epsilon_tree_bipartition →
  bipartition_tree(balance_edge_fn=find_balanced_edge_cuts_memoization); epsilon_tree_bipartition
  re-checks the cut side against pop_target(1±epsilon) (PopulationBalanceError); run_ensemble's
  chain constraint is `alberta_statutory_population_constraint`, no hook to replace it.

## 3. Specify  (GATE — draft, awaiting owner)

**S1 Split rule.** In s.15(2) mode a ReCom split of a merged pair is valid when each side is either
(i) within ±25% of the average, or (ii) 25–50% below average AND meets ≥ 3 of (a)–(e) under the
registered predicates. Implemented as a custom balance-edge function (same root choice, same
spanning tree draw as gerrychain's memoization function, one extra aggregate pass for the criteria
sums/counts per subtree); `epsilon` passed to recom = 0.5 only so gerrychain's post-check admits a
−50% side — the real band is enforced by the balance function.
**S2 Chain constraint.** Every plan: all divisions within ±25%, except ≤ 4 that are 25–50% below and
meet ≥ 3 criteria. Installed by replacing the MarkovChain constraints in nk s.15(2) mode.
**S3 Opinion gate.** Criteria met ⇒ permitted, never required (owner-approved reading 1).
**S4 Seed.** As today (±25% recursive_tree_part); the chain may then create s.15(2) divisions.
**S5 Predicates.** Use the registered Audit implementation (`s15_2_criteria.py`) when it lands; this
repo's `s152_criteria.py` is the cross-check. Disagreements reported with the rule that caused them.
**S6 Fast-fail** widened: a pair is infeasible only if no (normal|s.15(2)) × (normal|s.15(2)) side
combination can hold its total.

**Acceptance criteria.**
AC1 Every sampled plan satisfies S2 (checked by an independent post-hoc checker over a test run).
AC2 s.15(2) divisions occur (count > 0) in a 10,000-step test run, and never more than 4 per plan.
AC3 With s.15(2) mode off, output is byte/content-identical to the current code (regression hash).
AC4 Kill-and-resume identity holds in s.15(2) mode.
AC5 The criteria predicates reproduce the real maps' s.15(2) districts as validated in Discover
    (5/6 exact; LSL (b) the disclosed difference).
AC6 Throughput: a 500-step chunk ≤ 60 s on this machine under load (so 252,500 steps < ~9 h).

**Non-goals.** s.14 factors; changing max_attempts; the 15,000 km² surveyed-area limb (no data).

**GATE PASSED 2026-10-29 ~21:35 — owner: "Go".**

## 4. Plan  (folded into the Specify approval — logged deviation)

The owner's "Go" answered a spec whose S1–S6 already fix the implementation route, and the owner has
consistently directed momentum; the plan below is recorded rather than separately gated. Rollback:
the mode is behind `--s152`; with it off, AC3 requires identical output.
1. Implement S1/S2/S6 in close_seats_ensemble.py (`find_balanced_edge_cuts_s152`,
   `s152_constraint`, `s152_pair_infeasible`, `--s152 PATH`, checkpointed SHA of the table).
2. `tools/test_s152.py`: in-process chain recording every plan + independent pandas check (AC1, AC2, AC6).
3. AC3 regression hash; AC4 kill-and-resume in s.15(2) mode.
4. Swap in Audit's registered `s15_2_criteria.py` table when it lands (adapter if columns differ);
   cross-check report; then production 250s / 150s.

Implementation note: run_ensemble reseeds any state with a district beyond `pop_deviation`, so s.15(2)
mode passes pop_deviation 0.5 (its constraint is replaced by `s152_constraint` via RecordingChain and
the proposal epsilon is passed explicitly as 0.5; the real bands live in the balance function).

## 5. Execute

- ~21:40 Step 1 done (uncommitted). Step 2 test running: k=91 idx 250, 3,000 steps.
- ~21:45 **Amendment 21 signed by Audit** (c75b9baf on ccr-7082dbd7-sqy3h2, this branch merged in).
  **Owner ruling recorded (given to Audit directly): s.15(2)(c) purposive reading** — a "town" is a city
  or town (CSD CY, T) or the urban service area of a specialized municipality (Sherwood Park,
  Fort McMurray), Crowsnest Pass excluded (s.15(3)); counted when the division holds ≥ 2% of its 2021
  population. This REPLACES the T-only reading approved at the Question gate. Reason given: T-only
  would make Calgary-Glenmore-Tsuut'ina, Calgary-West-Tsuut'ina and both Medicine Hat districts eligible
  to sit 50% under quota.
- Registered criteria table for set D: `data/outputs/s15_2_va_criteria.csv` (SHA-256 01f70a86…8f47)
  from Audit's `s15_2_criteria.py`: (a) area > 20,000 km²; (b) OSM highway distance to the nearest node
  within 1 km, division min > 150 km; (c) as above; (d) division holds ≥ 10% of a reserve's (NRCan IR)
  or Metis settlement's area; (e) ≥ 1 km shared with the provincial boundary. `load_s152` reads both
  table formats; this repo's `s152_criteria.py` table (T-only, any-overlap, ≥ 100 m) is the cross-check.
- First acceptance run (own table, k=91 idx 259 — idx 250 failed to seed, retired): 3,000 plans,
  AC1 0 violations, AC2 s.15(2) divisions in 97.3% of plans (max 4 in 46%), AC6 13.5 s / 500 steps.
  AC3 regression content hash unchanged (66e00fa2…67cf). AC4 kill-and-resume in s.15(2) mode IDENTICAL.
- Rerunning on the registered table, with an independent per-plan score by Audit's own `criteria()`
  and explicit constraint-rejection checks (> +25%, < −50%, −30% with < 3 criteria, 5 qualifying).

## 6. Verify
## 7. Decide
## 8. Baseline
## 9. Operate
## 10. Learn

(§5 cont.) 2026-10-30 01:14 — registered-table acceptance PASSED (AC1 0/600, AC2 95.3% / max 4,
constraint checks PASS, AC6 7.1 s median per 500). 01:15 production launched: k=91 idx 251–254,
k=89 idx 150–151. Full numbers in amendment17_chain_runs/README.md.
