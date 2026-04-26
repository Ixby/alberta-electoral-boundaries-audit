---
name: Canadian inter-map EG asymmetry base rate (proxy computation)
description: Track V deliverable. Acquires a Canadian benchmark for inter-map partisan-asymmetry magnitude against which to calibrate the Alberta 2025-26 audit's 0.5-1.6 pp efficiency-gap asymmetry finding. Uses a seat-share-asymmetry proxy for the efficiency-gap asymmetry when both commission reports (interim and final) are scored against the same election's votes. Covers Alberta 2010, Alberta 2017, Federal 2022 (Alberta sub-commission), British Columbia 2023, Saskatchewan 2022, Manitoba 2018, and Alberta 2025-26 as the anchor; Nova Scotia 2019 is excluded as not structurally comparable. Produces a benchmark distribution and positions Alberta 2025-26 against it. Recalibrated 2026-04-23 (§7A) to remove the circularity flagged by Gemini Phase E.2 — Alberta 2025-26 excluded from the comparator distribution; see §7A for the corrected positioning (Approach A: 67th percentile n=6; Approach B: ordinal ranking among non-zero cycles, recommended primary framing).
forward_dependencies:
  - analysis/v0_1_fortification_c1_c10.md — §C4 (base-rate gap discussion; this file closes the gap)
  - data/v0_1_canadian_redistribution_base_rate.csv — updated with quantified rows
  - report_academic.md (§3.3 can cite this file if parent chooses; §5.2.1 consumes the §7A recalibration)
backward_dependencies:
  - analysis/scripts/canadian_base_rate_compute.py (the original n=7 computation)
  - analysis/scripts/canadian_base_rate_recalibrate.py (the 2026-04-23 recalibration)
  - analysis/scripts/v0_2_packing_cracking_analysis.py (EG formula used in audit)
  - data/v0_1_338canada_reallocated_majority.csv, data/v0_1_338canada_reallocated_minority.csv (audit's Alberta 2025-26 anchor)
---

# Canadian inter-map EG asymmetry base rate — Track V

## 1. The base-rate gap this file closes

The v0.1 fortification document (C4) concedes a data gap: the audit
reports Alberta 2025-26's commission majority-vs-minority efficiency-gap
asymmetry as 0.5-1.6 pp but does not benchmark this against other
Canadian redistribution cycles. Without a base rate, a 0.5 pp EG
asymmetry and 1-seat shift could be large or small relative to normal
Canadian redistribution variance. The red-team's C4 attack lands
directly on this gap.

Full crosswalks for seven candidate Canadian cycles, as the fortification
document budgets them, run at 4-8 hours per cycle. That work cannot be
done inside this session's budget. This file builds the base rate via a
**seat-share-asymmetry proxy** instead, grounded on the closed-form EG
identity.

## 2. Method

### 2.1 The proxy identity

The Stephanopoulos-McGhee (2015) closed-form efficiency gap is:

    EG = (seat_share − 0.5) − 2 × (vote_share − 0.5)

When the same election's votes are scored against two different maps
(interim map A, final map B), the vote_share term cancels:

    EG_B − EG_A = seat_share_B − seat_share_A
               = Δseats / n_seats

This is a first-order identity: the efficiency-gap asymmetry between two
maps equals the seat-share asymmetry, provided both maps are scored on
the same election's ballots. The identity is exact at the closed-form
level and approximately correct (within a small-multiplier compression)
under the full wasted-vote formula that the audit actually uses.

### 2.2 Empirical calibration of the compression factor

The audit's Alberta 2025-26 finding gives the empirical mapping between
seat-share asymmetry and wasted-vote EG asymmetry:

- Seat-share asymmetry: 1 seat / 89 seats × 100 = **1.12 pp**
- Audit's reported EG asymmetry: **0.51 pp**
- Empirical compression ratio: 0.51 / 1.12 = **0.455**

This compression reflects that some flipped seats involve narrow margins
where the wasted-vote bolus is not a full (half-district) reallocation.
We treat the 0.455 compression factor as calibrated from the audit's own
cycle and apply it uniformly to other Canadian cycles for consistency.
Sensitivity: the compression factor is plausibly bounded in [0.4, 0.6]
across small-Δs regimes. Reporting both the seat-share-asymmetry (exact
closed-form EG delta) and the compressed EG-asymmetry gives a readable
band.

### 2.3 Per-cycle input: the seat-flip count

For each cycle, `Δseats` is the number of projected-partisan-winner
flips between the interim and final maps, scored against the most recent
provincial or federal election's vote totals. Published news coverage
and commission reports identify which ridings changed boundary between
interim and final; under the previous election's votes, we identify
which of those changes would cross a projected-winner threshold.

This is a proxy. A full crosswalk would compute EG per map directly. The
proxy provides order-of-magnitude accuracy because:

1. Most interim-to-final changes are intra-partisan-zone swaps
   (e.g., Federal-Alberta 2022's Chestermere move between two CPC-
   dominant suburban ridings). These do not flip projected winners.
2. The inter-map differences that matter for EG are exactly the flipped
   seats — the identity above shows this explicitly.
3. Upper-bound cases (Δseats_high) are given where residual boundary
   uncertainty in competitive seats could plausibly move one more seat.

Where interim-to-final changes redistribute communities of similar
partisan lean (the modal Canadian case), the proxy reports Δs = 0 and
EG asymmetry ≈ 0 — which is itself the falsifiable claim against which
Alberta 2025-26 is benchmarked.

## 3. Per-cycle results

### 3.1 Results table

| Cycle | Seats | Δs best estimate | Δs bound | Seat-share asym. (pp) | EG asym. proxy (pp) | Status |
|-------|------:|-----------------:|:--------|----------------------:|--------------------:|:-------|
| **Alberta 2025-26** (audit anchor) | 89 | 1 | 1-3 | 1.12 | **0.51** (0.51-1.60 headline) | measured_this_audit |
| Canada_federal_AB 2022 | 37 | 0 | 0-1 | 0.00 | 0.00 (bound 0.00-1.23) | proxy |
| British Columbia 2023 | 93 | 0 | 0-1 | 0.00 | 0.00 (bound 0.00-0.49) | proxy |
| Saskatchewan 2022 | 61 | 0 | 0-1 | 0.00 | 0.00 (bound 0.00-0.75) | proxy |
| Alberta 2017 | 87 | 1 | 0-2 | 1.15 | 0.52 (bound 0.00-1.05) | proxy |
| Alberta 2010 | 87 | 0 | 0-2 | 0.00 | 0.00 (bound 0.00-1.05) | proxy |
| Manitoba 2018 | 57 | 1 | 0-2 | 1.75 | 0.80 (bound 0.00-1.60) | proxy |
| Nova Scotia 2019 | 55 | NA | NA | NA | NA | **not comparable** — menu-of-four-alternatives structure |

### 3.2 Per-cycle evidence summary

**Alberta 2025-26 (anchor).** Audit measurement. 1-seat majority-minority
asymmetry under 2023 actual vote and April 2026 polling (both inputs
agree). EG asymmetry 0.51 pp (low-end) to 1.60 pp (high-end under
two-party collapse and weight sensitivity). Method-match with the
proxy's compression factor is by construction.

**Federal 2022 (Alberta sub-commission).** The commission made changes
to all but one of 37 electoral districts between its June 2022 proposal
and February 2023 final. However, partisan composition is invariant:
the two NDP-competitive Edmonton seats (Griesbach, Strathcona) retain
their NDP-competitive character under both configurations. The three
new Alberta seats all project Conservative under 2021 votes in both
maps. Changes concentrated on intra-Conservative-zone swaps
(Chestermere moved between Airdrie-Chestermere/Bow River; Sherwood Park
boundaries reshuffled; Spruce Grove area reconfigured). No projected
winner flips between proposal and final.
Source: Federal Electoral Boundaries Commission for Alberta (2023).

**British Columbia 2023.** Preliminary report (Oct 2022) and final
report (Apr 2023) both recommend 93 seats with six new seats in the
same six cities (Vancouver, Burnaby, Langley, Surrey, Kelowna,
Langford). News coverage characterises the final as "much the same"
as the preliminary, with tweaks to ~71-72 existing boundaries. Final
adopted unanimously by Legislative Assembly (Apr 6 2023). No identified
inter-map seat flip in public coverage. Under 2020 NDP landslide
(57/87 seats on 47.7% vote), the competitive-margin seat set is small
and located in suburban growth zones that do not change between
preliminary and final.
Source: British Columbia Electoral Boundaries Commission (2023).

**Saskatchewan 2022.** Interim (Jul 2022) and final (Oct 2022). All 59
southern boundaries adjusted for population. Partisan-relevant changes
concentrate in growing urban centres (Warman, Martensville,
Saskatoon-Stonebridge). Under 2020 SaskParty landslide (48/61 seats on
60.7% vote), the competitive-margin seat count is low (Regina NDP-
leaning seats). No public coverage identifies a specific interim-to-
final projected-winner flip.
Source: Saskatchewan Constituency Boundaries Commission (2022).

**Alberta 2017.** Interim (May 2017) and final (Oct 2017). Two documented
interim-to-final changes: Beaumont reunified into a single ED (interim
split it across two); Lesser Slave Lake restored as a distinct riding
(interim had merged it). The Lesser Slave Lake restoration
redistributes ~20k rural voters. Under 2015 NDP-wave vote (40.6%),
this shift is at the margin of projected-winner change. Best estimate
1 seat flip (corresponding to the reinstated Lesser Slave Lake seat's
projected PC/UCP winner vs the merged-northern-ED projected NDP winner
under the interim configuration). Upper bound 2 for Calgary/Edmonton
new-seat location adjustments.
Source: Alberta Electoral Boundaries Commission (2017).

**Alberta 2010.** Interim (Feb 2010) and final (Jul 2010). Final dropped
interim's Edmonton-west three-new-division proposal but retained the
interim net +4 seats (2 Calgary + 1 Edmonton + 1 Fort McMurray). Under
2008 PC landslide (72/83 seats), competitive seats were the 4 Liberal
Edmonton ridings plus a small additional competitive set. The
Edmonton-west change redistributed PC-zone voters; no documented
Liberal-to-PC or PC-to-Liberal projected flip across interim-to-final.
Source: Alberta Electoral Boundaries Commission (2010).

**Manitoba 2018.** Commission amended 56 of 57 boundaries between
preliminary and final. Key composition change: Winnipeg gained one seat
from rural Manitoba (Headingley and West St. Paul rural municipalities
moved into city ridings). Under 2016 PC-wave vote (53.1%, 40/57 PC),
the rural-to-Winnipeg seat reallocation creates a marginal NDP-
competitive seat and removes a PC-held rural seat. Best estimate 1
seat projected flip between interim and final.
Source: Manitoba Electoral Divisions Boundaries Commission (2018).

**Nova Scotia 2019 — not comparable.** The interim report (Nov 2018)
presented FOUR alternatives: 51 with adjusted boundaries; 55 with
restored Acadian/Preston districts; 55 with dual-member Inverness; 56
with an exceptional district. The final report (Apr 2019) corresponds
to Alternative 2. This is a menu-of-options structure, not an
interim-to-final single-map pair. The Alberta 2025-26 comparison —
two commissioners in the majority and two in the dissent producing
complete alternative maps — is not structurally the same as picking
one of four menu items after public feedback. Excluded from the
benchmark.
Source: Nova Scotia Electoral Boundaries Commission (2019).

## 4. Canadian benchmark distribution

Descriptive statistics over the n=7 comparable cycles (including Alberta
2025-26 anchor):

| Statistic | ΔEG_proxy (pp) | Seat-share asymmetry (pp) |
|-----------|---------------:|--------------------------:|
| Mean | 0.262 | 0.574 |
| Median | 0.000 | 0.000 |
| Min | 0.000 | 0.000 |
| Max | 0.798 | 1.754 |
| Std dev (population) | 0.314 | 0.690 |

Excluding Alberta 2025-26 anchor (n=6):

| Statistic | ΔEG_proxy (pp) | Seat-share asymmetry (pp) |
|-----------|---------------:|--------------------------:|
| Mean | 0.220 | 0.483 |
| Median | 0.000 | 0.000 |
| Max | 0.798 | 1.754 |

**The median Canadian interim-to-final inter-map EG asymmetry is
approximately zero pp.** More than half of the sampled cycles produce
no projected-winner seat flip between the interim and final commission
reports under the relevant election's vote baseline.

The distribution is right-skewed: most cycles cluster at zero or near-
zero asymmetry; Manitoba 2018, Alberta 2017, and Alberta 2025-26 are
the three cycles where a projected-winner flip occurs between the two
maps under the proxy method.

## 5. Alberta 2025-26 against the Canadian benchmark

### 5.1 Point estimate

Alberta 2025-26's 0.51 pp EG asymmetry sits at the **71st percentile** of
the n=7 distribution — i.e., 5 of 7 sampled cycles (including Alberta
2025-26 itself) fall at or below 0.51 pp. Of the three cycles with
non-zero estimates (Alberta 2017: 0.52; Alberta 2025-26: 0.51; Manitoba
2018: 0.80), Alberta 2025-26 falls in the middle.

### 5.2 High-end estimate

Under the audit's high-end figure of 1.60 pp EG asymmetry (which
corresponds to the two-party-collapsed weight sensitivity and the
three-seat asymmetry under certain polling inputs), Alberta 2025-26
**exceeds all other cycles in the Canadian sample.** The highest non-
Alberta-2026 estimate is Manitoba 2018's 0.80 pp; Alberta 2025-26's
high-end is double that.

### 5.3 Verdict

**Alberta 2025-26's 0.5 pp point-estimate EG asymmetry is within the
upper half of the Canadian interim-to-final range but not outside it.
Alberta 2025-26's 1.6 pp high-end estimate exceeds the highest observed
Canadian cycle in the benchmark sample.**

The honest reading: the *low-end* audit headline (0.5 pp) is consistent
with ordinary Canadian redistribution variance (Manitoba 2018 showed
the same order of magnitude). The *high-end* headline (1.6 pp) is not
consistent with ordinary Canadian redistribution variance and sits
above the sampled benchmark.

This benchmark sample is n=7 and includes only the most recent
preliminary-vs-final cycles for which evidence was reachable in the
session budget. It does not include pre-2010 cycles, and it relies on
a seat-share-asymmetry proxy rather than direct per-ED EG computation.
Expansion to the full historical record is a future-work item.

## 6. Implications for the audit's §3.3 acknowledgement

The audit's proposed §3.3 insertion (per fortification document C4)
acknowledges the base-rate gap and notes that Stephanopoulos-McGhee
(2018) show US state-level EG noise at ~0±2 pp. This file now permits a
**Canadian** anchor:

> "A proxy base rate across six comparable Canadian interim-to-final
> commission cycles (Alberta 2010, 2017; Federal-Alberta 2022; British
> Columbia 2023; Saskatchewan 2022; Manitoba 2018) yields a median
> inter-map EG asymmetry of 0.0 pp and a maximum of 0.8 pp
> (Manitoba 2018, where a rural-to-Winnipeg seat reallocation produced
> a one-seat projected flip). Alberta 2025-26's point-estimate EG
> asymmetry of 0.5 pp is within the Canadian range; Alberta 2025-26's
> high-end estimate of 1.6 pp is above it. Method:
> `analysis/methodology/v0_1_canadian_base_rate_computed.md` and
> `analysis/scripts/canadian_base_rate_compute.py`."

### 6.1 Does the base rate support or weaken the audit's headline?

**Mixed.** The low-end headline (0.5 pp) is supported in the sense that
it is not alone — Manitoba 2018 reached a similar magnitude, and
Alberta 2017's restoration of Lesser Slave Lake reached the same scale.
The median Canadian cycle produces no projected flip at all, so
Alberta 2025-26 joins a minority of cycles with any inter-map
asymmetry — this is mild **evidence for** the audit's finding being
real rather than noise.

The high-end headline (1.6 pp) is above the observed Canadian maximum
in this sample (Manitoba 2018 at 0.8 pp). Under that reading, Alberta
2025-26 is the **Canadian outlier** in the sampled window. This is a
stronger **evidence for** the audit's finding being anomalous.

Either way, the claim "0.5-1.6 pp is within ordinary Canadian variance"
is **not** supported by this benchmark. The median is 0.0 pp, not
0.5 pp. Any non-zero inter-map EG asymmetry places a cycle in the
upper tail of the distribution. The more defensible framing after this
benchmark is: "Alberta 2025-26 is in the minority of Canadian cycles
that produce any inter-map partisan-winner asymmetry, and at the high-
end interpretation exceeds the observed Canadian maximum in this
seven-cycle sample."

## 7. Limitations

1. **Proxy, not direct EG.** The 0.455 compression factor is calibrated
   from Alberta 2025-26 alone. Direct per-ED EG computation on all
   cycles would either confirm or refine this factor.
2. **Seat-flip inference from news coverage.** For cycles with
   publicly-invisible boundary adjustment detail (Saskatchewan 2022
   is the worst case), Δs = 0 is an educated inference rather than a
   direct measurement. Upper-bound columns reflect this uncertainty.
3. **Small n.** Seven cycles is a narrow benchmark. Pre-2010 cycles,
   federal 2002 redistribution, Quebec 2017, Ontario 2013 would expand
   the sample.
4. **Nova Scotia 2019 exclusion.** The menu-of-four structure is not
   comparable to Alberta 2025-26's majority-vs-minority structure.
   Including it would require a different comparison (e.g., final vs
   alternative-3) and is out of scope here.
5. **Government-override cycles.** Ontario 1996, Quebec 1992, BC 2008
   are all government-legislated departures from a single commission
   report, not interim-vs-final commission comparisons. They remain in
   the catalogue but outside this benchmark.
6. **Future federal sub-commissions.** Building similar proxy estimates
   for the other nine provincial federal commissions in the 2022 cycle
   would expand the federal anchor from n=1 (Alberta) to n=10.

## 7A. Recalibration (2026-04-23) — circularity fix

### 7A.1 The circularity

The §5.1 claim above — "Alberta 2025-26's 0.51 pp EG asymmetry sits at
the 71st percentile of the n=7 distribution" — is circular. Alberta
2025-26 is the anchor case the audit is evaluating, and it is a member
of the n=7 distribution used to rank it. A reviewer can legitimately
say: "you scored Alberta 2026 at p71 on a distribution that contains
Alberta 2026 as one of seven data points, and you calibrated the
compression factor (0.455) from Alberta 2026." Both operations
contaminate the benchmark. Gemini's red-team Phase E.2 flagged this.

Two independent issues:

1. **Inclusion.** The comparator distribution used to place Alberta
   2025-26 should not itself contain Alberta 2025-26.
2. **Compression calibration.** The 0.455 deflator that maps
   seat-share asymmetry to EG-proxy was fit from Alberta 2025-26
   alone. Other cycles' EG-proxy values (0.52 for Alberta 2017, 0.80
   for Manitoba 2018) inherit that calibration. We mitigate by
   reporting the raw seat-share asymmetry (factor-free, closed-form
   exact under constant votes) alongside the compressed EG-proxy.

This section supersedes §5.1's percentile claim. The original n=7
computation is retained above as historical record; the numbers below
are the corrected positioning.

### 7A.2 Approach A — exclude Alberta 2025-26 from the distribution

Computing the comparator distribution over the six OTHER cycles
(Federal-AB 2022, BC 2023, Saskatchewan 2022, Alberta 2017, Alberta
2010, Manitoba 2018) and placing Alberta 2025-26's 0.51 pp against it:

| Statistic    | EG-proxy pp (n=6) | Seat-share asymmetry pp (n=6) |
| ------------ | ----------------: | ----------------------------: |
| Mean         |             0.220 |                         0.483 |
| Median       |             0.000 |                         0.000 |
| Min          |             0.000 |                         0.000 |
| Max          |             0.800 |                         1.754 |
| Population σ |             0.321 |                         0.705 |

Sorted EG-proxy comparator: `[0.00, 0.00, 0.00, 0.00, 0.52, 0.80]`.

**Alberta 2025-26 (0.51 pp) against this n=6 comparator:**

- Weak percentile: **66.7%** (4 of 6 comparator cycles fall strictly
  below; the two non-zero cycles Alberta 2017 and Manitoba 2018 fall
  strictly above).
- High-end (1.60 pp): **100%** (exceeds Manitoba 2018's 0.80 pp
  maximum in the comparator).
- Seat-share asymmetry (1.12 pp, factor-free): **66.7%** against the
  n=6 seat-share distribution (4 below, 2 above).

The revised point-estimate percentile is 67% rather than 71%. This is
**not a material change** — the anchor remains in the upper third of
the Canadian distribution under either framing, and the high-end
headline (1.60 pp exceeds the Canadian maximum) is unchanged. But the
new number is defensible against the circularity objection.

### 7A.3 Approach B — ordinal ranking among non-zero cycles

Three of the seven cycles produce non-zero inter-map asymmetry under
the proxy method (Alberta 2017, Alberta 2025-26, Manitoba 2018). The
other four (Federal-AB 2022, BC 2023, Saskatchewan 2022, Alberta 2010)
are estimated at zero.

Ranked by EG-proxy magnitude, the three non-zero cycles are:

| Rank | Cycle                    | EG-proxy pp | Seat-share asym. pp |
| ---: | ------------------------ | ----------: | ------------------: |
|    1 | Alberta 2025-26 (anchor) |        0.51 |                1.12 |
|    2 | Alberta 2017             |        0.52 |                1.15 |
|    3 | Manitoba 2018            |        0.80 |                1.75 |

Framing: "Alberta 2025-26 is one of three Canadian redistribution
cycles in the sample that produced any inter-map projected-winner
asymmetry. Its magnitude (0.51 pp / 1.12 pp seat-share) is
approximately equal to Alberta 2017's (0.52 pp / 1.15 pp seat-share,
Lesser Slave Lake restoration) and below Manitoba 2018's (0.80 pp /
1.75 pp seat-share, rural-to-Winnipeg reallocation)."

No percentile claim. Defensible in a small-sample setting where
n=6 does not really support percentile arithmetic to two decimal
places.

### 7A.4 Recommended primary framing

**Approach B (ordinal) should be the primary framing in the paper.**
Reasoning:

1. n=6 is too small to support meaningful percentile claims;
   quartile-scale resolution is what a 6-point sample can deliver.
2. Both non-zero non-anchor cycles are documented single-seat
   commission changes (rural seat restored, rural-to-urban seat
   reallocated). Alberta 2025-26 is also a single-seat change under
   the point estimate. The ordinal framing surfaces this structural
   similarity — all three cycles are "single-seat commission
   changes" — which the percentile framing obscures.
3. The compression-factor calibration problem (0.455 from Alberta
   2026 alone) contaminates the EG-proxy ordering less than it
   contaminates the EG-proxy percentile. Ordering of 0.51 vs 0.52 vs
   0.80 survives any reasonable compression factor; percentile
   precision does not.

Approach A is retained as a sensitivity: if a reviewer demands a
numerical percentile, 67th percentile (n=6 excluding the anchor) is
the defensible number. The original 71st percentile should not be
used.

### 7A.5 Why n=6 is the practical ceiling

Possible extensions and why they weren't added in this pass:

- **Nova Scotia 2019.** Remains excluded as menu-of-four-alternatives;
  not structurally comparable. Including it would require a different
  comparison (e.g., final vs. alternative-3) and a different method
  design, not a drop-in extension.
- **Federal 2022 other nine provinces.** Feasible in principle —
  transposition of 2021 votes onto proposal and final maps is in the
  Elections Canada crosswalk. But 4–8 hours per province to reconstruct
  seat flips; ten provinces' worth of that is the kind of work the
  original computation document deferred as out of scope. Would expand
  the federal anchor from n=1 (Alberta) to n=10.
- **Pre-2010 provincial cycles.** Public commission reports exist but
  interim-vs-final diffs are harder to recover from archival material;
  most news coverage does not preserve the interim map. Feasible with
  archival research, not feasible in the current session.
- **Government-override cycles (Ontario 1996, Quebec 1992, BC 2008,
  Manitoba 1989).** Already flagged in the catalogue as "not
  interim-vs-final commission comparisons." A separate comparator
  class that cannot be folded into this one without a second method
  design.
- **New Brunswick 2023.** In the catalogue but not acquired in the
  original pass. Could plausibly be added with comparable effort to
  Saskatchewan 2022. Would take the comparator from n=6 to n=7.

For this recalibration, we accept n=6 as the practical ceiling and
report Approach B (ordinal) as primary.

### 7A.6 Suggested replacement paragraph for report_academic.md §5.2.1

The existing "Canadian comparative base rate" paragraph in §5.2.1
reports the circular p71 claim. The replacement paragraph below
incorporates §7A.1–§7A.4 and should be substituted for the existing
paragraph. Word count ~285.

> **Canadian comparative base rate.** A first-catalogue computation
> of inter-map partisan-asymmetry magnitude across recent Canadian
> provincial and federal redistributions is reported in
> `analysis/methodology/v0_1_canadian_base_rate_computed.md` and
> `data/v0_1_canadian_redistribution_base_rate.csv`. The method uses
> a seat-share-delta proxy calibrated to Alberta 2025-26 (compression
> factor ≈0.455, acknowledged approximation). Seven comparable
> cycles were scored: Federal 2022 Alberta sub-commission, BC 2023,
> Saskatchewan 2022, Alberta 2017, Alberta 2010, Manitoba 2018, and
> Alberta 2025-26. Because Alberta 2025-26 is both the case under
> audit and the cycle from which the compression factor is fit, it
> is excluded from the comparator distribution used to position it
> (an earlier version of this paper reported a "71st percentile"
> placement against an n=7 distribution that included Alberta
> 2025-26; that claim was circular and has been retracted). Against
> the n=6 comparator, four cycles (Federal-AB 2022, BC 2023,
> Saskatchewan 2022, Alberta 2010) produce zero inter-map
> projected-winner asymmetry; two produce non-zero asymmetry —
> Alberta 2017 at 0.52 pp (Lesser Slave Lake restoration) and
> Manitoba 2018 at 0.80 pp (rural-to-Winnipeg seat reallocation).
> Alberta 2025-26's 0.51 pp point-estimate is ordinally equivalent
> to Alberta 2017 and below Manitoba 2018; the high-end 1.52 pp from
> the weight-sensitivity range exceeds the observed Canadian maximum
> in this sample. The defensible statement is therefore: **Alberta
> 2025-26 is one of three Canadian redistribution cycles (of seven
> sampled) that produced any inter-map projected-winner asymmetry;
> at the low-end point estimate it is ordinally equivalent to
> Alberta 2017 and below Manitoba 2018; at the high-end it exceeds
> the observed Canadian maximum in this sample.** If a quantitative
> placement is required, Alberta 2025-26 sits at the 67th percentile
> of the n=6 comparator. Method details and the full recalibration
> at §7A of the computation document. The sample is small and
> proxy-based; direct per-ED EG computation remains future work.

## 8. References

Alberta Electoral Boundaries Commission. (2010). *Final Report to the
Speaker of the Legislative Assembly of Alberta*. Edmonton: Legislative
Assembly of Alberta.

Alberta Electoral Boundaries Commission. (2017). *Final Report to the
Speaker of the Legislative Assembly of Alberta*. Edmonton: Legislative
Assembly of Alberta.
https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf

British Columbia Electoral Boundaries Commission. (2023). *Final
Report*. Victoria: Legislative Assembly of British Columbia.
https://bcebc.ca/final-report/

Elections Canada. (2023). *Transposition of Votes from the 44th General
Election to the 2023 Representation Orders*. Ottawa: Office of the
Chief Electoral Officer.
https://www.elections.ca/content.aspx?section=res&dir=rep/tra/2023rep&document=index&lang=e

Federal Electoral Boundaries Commission for Alberta. (2023). *Report of
the Federal Electoral Boundaries Commission for the Province of
Alberta*. Ottawa: Office of the Chief Electoral Officer.
https://redecoupage-redistribution-2022.ca/com/ab/rprt/index_e.aspx

Manitoba Electoral Divisions Boundaries Commission. (2018). *Final
Report*. Winnipeg: Elections Manitoba.
https://www.electionsmanitoba.ca/en/resources/maps

Nova Scotia Electoral Boundaries Commission. (2019). *Final Report*.
Halifax: Nova Scotia Legislature.
https://nselectoralboundaries.ca/

Saskatchewan Constituency Boundaries Commission. (2022). *Final
Report*. Regina: Saskatchewan Legislative Assembly.
https://www.saskboundaries.ca/reports/

Stephanopoulos, N. O., & McGhee, E. M. (2015). Partisan gerrymandering
and the efficiency gap. *University of Chicago Law Review*, 82(2),
831-900.

Stephanopoulos, N. O., & McGhee, E. M. (2018). The measure of a metric:
The debate over quantifying partisan gerrymandering. *Election Law
Journal*, 17(4), 198-222.
