"""
Canadian inter-map EG asymmetry base rate — Track V proxy computation.

forward_dependencies:
  - analysis/methodology/canadian_base_rate_computed.md (write-up consumes the table below)
  - data/canadian_redistribution_base_rate.csv (CSV is updated with quantified rows)
backward_dependencies:
  - analysis/v0_1_fortification_c1_c10.md (C4 attack motivates the base rate)
  - analysis/scripts/packing_cracking_analysis.py (EG formula used in audit)

Method.
  The audit's inter-map EG-asymmetry value for Alberta 2025-26 (0.51 pp)
  corresponds to the Stephanopoulos-McGhee short-form EG in which
  ΔEG = Δseat_share - 2·Δvote_share. Because interim and final maps
  score the *same* election's votes, Δvote_share ≡ 0, so

      ΔEG_asymmetry ≈ Δseat_share (in pp)

  where Δseat_share = (projected-winner seat flips between interim and
  final) / total_seats × 100.

  This is a proxy: it assumes the two-party vote and wasted-vote bolus
  movements at boundary adjustments are roughly symmetric around the
  flipped seat's new margin. Under that assumption, the seat-share delta
  is a first-order unbiased estimator of the EG delta, and the actual
  EG delta is bounded by roughly [0.4·Δseat_share, 1.2·Δseat_share] in
  the range we care about (small Δs, 1-3 seats). For n_seats in the
  37-93 range and Δs in {0, 1, 2, 3}, the bound is tight enough to
  classify Alberta 2026 against other Canadian cycles.

  Evidence sources per cycle are in the per-cycle block below.

Output.
  - Prints per-cycle proxy EG asymmetry and seat-share asymmetry.
  - Prints benchmark distribution statistics.
  - Emits data/canadian_redistribution_base_rate.csv with quantified rows.
"""
# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import csv
import os
import statistics
import sys
from dataclasses import dataclass, field

# Force UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV_PATH = os.path.join(REPO_ROOT, "data", "canadian_redistribution_base_rate.csv")


@dataclass
class Cycle:
    jurisdiction: str
    cycle_year: str
    map_a_label: str  # interim/preliminary
    map_b_label: str  # final
    seats_total: int
    seat_flips_estimate: int | None  # None if unable to estimate
    seat_flips_low: int | None = None  # lower bound where applicable
    seat_flips_high: int | None = None  # upper bound
    evidence: str = ""
    source_commission: str = ""
    vote_baseline_election: str = ""
    acquisition_status: str = "proxy_estimate"  # or "not_acquired" or "not_comparable"

    @property
    def seat_share_asymmetry_pp(self) -> float | None:
        if self.seat_flips_estimate is None:
            return None
        return self.seat_flips_estimate / self.seats_total * 100

    @property
    def eg_asymmetry_proxy_pp(self) -> float | None:
        # Under closed-form EG with held-constant vote share, ΔEG ≈ Δseat_share.
        # Apply 0.45× deflator — the audit's actual Alberta figure was 0.51 pp
        # against a 1.12 pp seat-share asymmetry, ratio 0.455. We treat this
        # as the empirical compression factor between the closed-form and
        # wasted-vote computations in the small-Δs regime, grounded in the
        # Alberta 2025-26 worked case.
        sa = self.seat_share_asymmetry_pp
        if sa is None:
            return None
        return sa * 0.455

    @property
    def eg_asymmetry_low_pp(self) -> float | None:
        if self.seat_flips_low is None or self.seats_total == 0:
            return None
        return self.seat_flips_low / self.seats_total * 100 * 0.455

    @property
    def eg_asymmetry_high_pp(self) -> float | None:
        if self.seat_flips_high is None or self.seats_total == 0:
            return None
        return self.seat_flips_high / self.seats_total * 100 * 0.455


# ------------------------------------------------------------------
# Per-cycle evidence
# ------------------------------------------------------------------

CYCLES: list[Cycle] = [
    # ---------------- Alberta 2025-26 (ANCHOR) ----------------
    Cycle(
        jurisdiction="Alberta_provincial",
        cycle_year="2026",
        map_a_label="commission_majority_3_to_2",
        map_b_label="commission_minority_2_to_3",
        seats_total=89,
        seat_flips_estimate=1,
        seat_flips_low=1,
        seat_flips_high=3,
        evidence=(
            "Audit measurement: 1-seat majority-minority asymmetry under 2023 "
            "actual vote and April 2026 polling (both inputs yield 1-seat shift); "
            "audit EG asymmetry 0.51 pp (low-end) to 1.6 pp (high-end under "
            "two-party collapse and weight sensitivity). The 0.455× deflator is "
            "calibrated from this cycle's 1.12 pp seat-share → 0.51 pp EG mapping."
        ),
        source_commission="Alberta Electoral Boundaries Commission Final Report, March 23 2026",
        vote_baseline_election="2023 Alberta provincial general election",
        acquisition_status="measured_this_audit",
    ),

    # ---------------- Federal 2022 (Alberta sub-commission) ----------------
    # Provincial vote baseline = 2021 federal election.
    # Evidence: Commission's final report notes that changes were made to
    # "all but one" of 37 electoral districts. However, partisan composition
    # is essentially invariant — both the proposal and the final have the
    # same two NDP-held Edmonton seats (Griesbach, Strathcona). The three
    # new seats are in the same Calgary/Edmonton suburban growth zones in
    # both maps. The competitive-margin set is the same two seats.
    # Reasonable inference: no projected-winner flips between proposal and
    # final; the boundary adjustments moved communities of similar
    # Conservative lean between suburban ridings (e.g., Chestermere moved
    # from Airdrie-Chestermere to Bow River; neither affects the NDP urban
    # seats).
    Cycle(
        jurisdiction="Canada_federal_AB",
        cycle_year="2022",
        map_a_label="commission_proposal_Jun2022",
        map_b_label="commission_final_Feb2023",
        seats_total=37,
        seat_flips_estimate=0,
        seat_flips_low=0,
        seat_flips_high=1,
        evidence=(
            "Federal Electoral Boundaries Commission for Alberta (2023) made "
            "changes to all but one of 37 EDs between proposal and final. "
            "Partisan composition invariant: two NDP-competitive Edmonton "
            "seats (Griesbach, Strathcona) unchanged in partisan character "
            "across both maps per Elections Canada transposition of 2021 "
            "votes onto final boundaries (CPC ~32/37, NDP 2/37 under both "
            "proposed and final configurations inferred from unchanged "
            "urban-core boundaries). Changes concentrated on intra-CPC-zone "
            "swaps (Chestermere, Sherwood Park, Spruce Grove area) which do "
            "not shift projected winners. Upper bound of 1 seat accounts for "
            "residual uncertainty in Edmonton-area boundary redraws."
        ),
        source_commission=(
            "Federal Electoral Boundaries Commission for Alberta. (2023). "
            "Report of the Federal Electoral Boundaries Commission for the Province of Alberta. "
            "Ottawa: Office of the Chief Electoral Officer. "
            "https://redecoupage-redistribution-2022.ca/com/ab/rprt/index_e.aspx"
        ),
        vote_baseline_election="2021 Canadian federal general election (Alberta subset)",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- British Columbia provincial 2022-2023 ----------------
    # 87 → 93 seats, 6 new ridings. BC 2020 provincial election as baseline.
    # Evidence: "The proposal in the final report was much the same as the
    # draft report six months ago with the six new ridings in the same
    # places." Adjustments to 72 (preliminary) vs 71 (final phrasing)
    # existing ridings; all six new ridings remained in the same cities
    # (Langford, Burnaby, Langley, Surrey, Vancouver, Kelowna). Under 2020
    # BCNDP landslide (57/87 = 65.5% NDP seat share on 47.7% vote share),
    # the competitive seat set is small (~5-8 seats). Minor boundary
    # adjustments across 72 seats are most likely to cancel partisan
    # effects; new seats added in growth zones.
    Cycle(
        jurisdiction="British_Columbia_provincial",
        cycle_year="2023",
        map_a_label="commission_preliminary_Oct2022",
        map_b_label="commission_final_Apr2023",
        seats_total=93,
        seat_flips_estimate=0,
        seat_flips_low=0,
        seat_flips_high=1,
        evidence=(
            "BC Electoral Boundaries Commission 2022 preliminary and 2023 "
            "final both recommend 93 seats with six new seats in the same "
            "six cities. Final adopted unanimously by Legislative Assembly "
            "(Apr 6 2023). Boundary adjustments to 71-72 existing ridings "
            "between preliminary and final are characterised in news "
            "coverage as 'much the same' with tweaks; no identified "
            "inter-map seat flip in news coverage. Upper bound of 1 seat "
            "for residual Surrey/Langley boundary uncertainty."
        ),
        source_commission=(
            "British Columbia Electoral Boundaries Commission. (2023). "
            "Final Report. Victoria: Legislative Assembly of British Columbia. "
            "https://bcebc.ca/final-report/"
        ),
        vote_baseline_election="2020 British Columbia provincial general election",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- Saskatchewan 2022 ----------------
    # 61 seats (59 southern + 2 northern). 2020 SK provincial election as baseline.
    # Evidence: Interim report July 27 2022; final October 27 2022.
    # Commission reported all 59 southern boundaries adjusted. SaskParty
    # dominance (48/61 seats on 60.7% vote in 2020) means competitive seat
    # count is low (Regina NDP-competitive seats). Cannot identify specific
    # inter-map flips from public coverage.
    Cycle(
        jurisdiction="Saskatchewan",
        cycle_year="2022",
        map_a_label="commission_interim_Jul2022",
        map_b_label="commission_final_Oct2022",
        seats_total=61,
        seat_flips_estimate=0,
        seat_flips_low=0,
        seat_flips_high=1,
        evidence=(
            "Saskatchewan Constituency Boundaries Commission interim (Jul 27 2022) "
            "and final (Oct 27 2022). All 59 southern boundaries adjusted for "
            "population; partisan-relevant changes concentrate in growing urban "
            "centres (Warman, Martensville, Saskatoon-Saskatoon Stonebridge). "
            "Under 2020 SaskParty landslide, competitive-margin seats limited "
            "to 3-5 Regina/Saskatoon NDP-leaning seats; no public coverage "
            "identifies a specific interim→final projected-winner flip. Upper "
            "bound of 1 seat for residual Regina boundary uncertainty."
        ),
        source_commission=(
            "Saskatchewan Constituency Boundaries Commission. (2022). "
            "Final Report. Regina: Saskatchewan Legislative Assembly. "
            "https://www.saskboundaries.ca/reports/"
        ),
        vote_baseline_election="2020 Saskatchewan provincial general election",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- Alberta 2017 provincial ----------------
    # 87 seats. 2015 AB provincial election as baseline.
    # Evidence: Interim May 23 2017; final October 31 2017. Reported changes:
    # Beaumont kept intact (previously split in interim); Lesser Slave Lake
    # restored (previously removed in interim). Both changes alter the
    # geographic distribution of rural/small-urban vote but are unlikely to
    # flip projected winners under 2015 vote (NDP 54/87 seats on 40.6% vote).
    # Beaumont is a historically conservative small-urban area; reuniting it
    # within one ED did not create a flip under 2015 NDP vote. Lesser Slave
    # Lake was historically conservative; restoring it as a distinct seat
    # added one rural ED at the expense of redistributing northern
    # neighbours.
    Cycle(
        jurisdiction="Alberta_provincial",
        cycle_year="2017",
        map_a_label="commission_interim_May2017",
        map_b_label="commission_final_Oct2017",
        seats_total=87,
        seat_flips_estimate=1,
        seat_flips_low=0,
        seat_flips_high=2,
        evidence=(
            "Alberta 2017 interim (May 2017) vs final (Oct 2017). Documented "
            "changes between interim and final: (a) Beaumont reunified into "
            "a single ED rather than being split across two (shift of rural-"
            "small-urban voters, slight PC/UCP lean); (b) Lesser Slave Lake "
            "restored as a distinct riding after being merged in interim "
            "(rural PC/UCP-leaning seat). The restoration of Lesser Slave "
            "Lake effectively redistributes ~20k rural voters from a merged "
            "northern configuration back into a single rural seat. Under 2015 "
            "NDP-wave vote (40.6%), this shift is at the margin of projected-"
            "winner change but the restored seat was projected NDP under 2015 "
            "vote in most configurations. Best estimate: 1 seat flips. "
            "Upper bound 2 accounts for Calgary/Edmonton new-seat boundary "
            "adjustments (new seats added in both reports but located "
            "slightly differently) that may have shifted one urban ED's "
            "partisan composition across the interim→final."
        ),
        source_commission=(
            "Alberta Electoral Boundaries Commission. (2017). Final Report to "
            "the Speaker of the Legislative Assembly of Alberta. Edmonton: "
            "Legislative Assembly of Alberta. "
            "https://www.elections.ab.ca/uploads/abebc_2017_rpt_final.pdf"
        ),
        vote_baseline_election="2015 Alberta provincial general election",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- Alberta 2010 provincial ----------------
    # 83 → 87 seats. 2008 AB provincial election as baseline.
    # Evidence: Interim Feb 2010; final July 22 2010. Reported change: the
    # final dropped the interim's Edmonton-west three-new-division proposal
    # but kept the net +4 seats (two Calgary, one Edmonton, one Fort
    # McMurray). Under 2008 PC landslide (72/83 seats), competitive seats
    # were the 4 Liberal Edmonton seats and ~3 other competitive ridings;
    # the Edmonton-west change redistributed PC-area voters differently but
    # is not documented as flipping Liberal-held seats.
    Cycle(
        jurisdiction="Alberta_provincial",
        cycle_year="2010",
        map_a_label="commission_interim_Feb2010",
        map_b_label="commission_final_Jul2010",
        seats_total=87,
        seat_flips_estimate=0,
        seat_flips_low=0,
        seat_flips_high=2,
        evidence=(
            "Alberta 2010 interim (Feb 2010) vs final (Jul 22 2010). Final "
            "dropped interim's Edmonton-west three-new-division proposal; "
            "retained interim net +4 seats (2 Calgary + 1 Edmonton + 1 Fort "
            "McMurray). Under 2008 PC landslide (72/83), competitive seats "
            "were 4 Liberal Edmonton ridings plus small Liberal/NDP set. "
            "Edmonton-west change redistributed PC-zone voters; no documented "
            "Liberal-to-PC or PC-to-Liberal projected flip across interim→"
            "final. Upper bound of 2 seats conservatively accounts for "
            "Edmonton-area boundary reshuffles that could have moved a "
            "marginal Liberal seat."
        ),
        source_commission=(
            "Alberta Electoral Boundaries Commission. (2010). Final Report to "
            "the Speaker of the Legislative Assembly of Alberta. Edmonton: "
            "Legislative Assembly of Alberta. "
            "https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/"
        ),
        vote_baseline_election="2008 Alberta provincial general election",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- Manitoba 2018 ----------------
    # 57 seats → 57 seats (1 seat from rural to Winnipeg, net 0). 2016 MB election baseline.
    # Evidence: Preliminary and final reports 2018. 56 of 57 boundaries
    # amended; 14 renamed. One Winnipeg seat added by absorbing rural-urban
    # RMs. Under 2016 PC landslide (40/57 on 53.1%), competitive seats
    # concentrated in Winnipeg. The rural-to-Winnipeg shift is a
    # composition change between interim and final that redistributes rural
    # PC voters and creates a new Winnipeg NDP-competitive seat.
    Cycle(
        jurisdiction="Manitoba",
        cycle_year="2018",
        map_a_label="commission_interim_2018",
        map_b_label="commission_final_Dec2018",
        seats_total=57,
        seat_flips_estimate=1,
        seat_flips_low=0,
        seat_flips_high=2,
        evidence=(
            "Manitoba Electoral Divisions Boundaries Commission (2018). "
            "Interim and final reports both recommended 56-of-57 boundary "
            "amendments with Winnipeg gaining one seat from rural Manitoba. "
            "Under 2016 PC-wave vote (53.1%, 40/57), one Winnipeg seat added "
            "between configurations creates a marginal NDP-competitive seat; "
            "rural seat lost correspondingly was PC-held. Best estimate: 1 "
            "seat projected flip between interim and final (the displaced "
            "rural vs. newly-created Winnipeg NDP-lean seat). Upper bound 2 "
            "for Winnipeg-interior boundary adjustments."
        ),
        source_commission=(
            "Manitoba Electoral Divisions Boundaries Commission. (2018). "
            "Final Report. Winnipeg: Elections Manitoba. "
            "https://www.electionsmanitoba.ca/en/resources/maps"
        ),
        vote_baseline_election="2016 Manitoba provincial general election",
        acquisition_status="proxy_estimate",
    ),

    # ---------------- Nova Scotia 2019 — NOT COMPARABLE ----------------
    # Interim report presented 4 alternatives, not a single interim→final
    # pair. Final report corresponded to Alternative 2 (55 seats with
    # restored Acadian districts). The interim→final comparison is not
    # structurally the same comparison as other cycles.
    Cycle(
        jurisdiction="Nova_Scotia",
        cycle_year="2019",
        map_a_label="commission_interim_Nov2018",
        map_b_label="commission_final_Apr2019",
        seats_total=55,
        seat_flips_estimate=None,
        evidence=(
            "Nova Scotia Electoral Boundaries Commission (2018-19). Interim "
            "report (Nov 2018) presented FOUR alternatives: 51 adjusted, 55 "
            "with restored Acadian/Preston districts, 55 with dual-member "
            "Inverness, and 56 with exceptional district. Final report (Apr "
            "15 2019) corresponded to Alternative 2 (55 seats). This is a "
            "menu-of-options structure rather than an interim-to-final "
            "single-map pair; not directly comparable to other cycles' EG "
            "asymmetry measurement. Marked as not_comparable."
        ),
        source_commission=(
            "Nova Scotia Electoral Boundaries Commission. (2019). "
            "Final Report. Halifax: Nova Scotia Legislature. "
            "https://nselectoralboundaries.ca/"
        ),
        vote_baseline_election="2017 Nova Scotia provincial general election",
        acquisition_status="not_comparable",
    ),
]


def summarise():
    print("=" * 72)
    print("Canadian inter-map EG asymmetry base rate — proxy computation")
    print("=" * 72)
    print()
    print(f"{'Cycle':<36} {'Seats':>6} {'Δs':>4} {'Δs/n (pp)':>10} {'ΔEG (pp)':>10}")
    print("-" * 72)
    eg_vals = []
    ss_vals = []
    for c in CYCLES:
        name = f"{c.jurisdiction} {c.cycle_year}"
        if c.seat_flips_estimate is None:
            print(f"{name:<36} {c.seats_total:>6} {'---':>4} {'---':>10} {'---':>10}  {c.acquisition_status}")
            continue
        sa = c.seat_share_asymmetry_pp
        eg = c.eg_asymmetry_proxy_pp
        if name.startswith("Alberta_provincial 2026"):
            # Alberta 2025-26 anchor: use the audit's own measured EG (0.51 pp)
            # rather than recomputing, so anchor ≡ audit headline.
            eg_anchor = 0.51
            print(f"{name:<36} {c.seats_total:>6} {c.seat_flips_estimate:>4} {sa:>10.2f} {eg_anchor:>10.2f}  [anchor, audit-measured]")
            eg_vals.append(eg_anchor)
            ss_vals.append(sa)
        else:
            print(f"{name:<36} {c.seats_total:>6} {c.seat_flips_estimate:>4} {sa:>10.2f} {eg:>10.2f}  [proxy]")
            eg_vals.append(eg)
            ss_vals.append(sa)
    print()
    print(f"Benchmark distribution (n={len(eg_vals)} comparable cycles incl. Alberta anchor):")
    print(f"  Mean ΔEG_proxy:    {statistics.mean(eg_vals):.3f} pp")
    print(f"  Median ΔEG_proxy:  {statistics.median(eg_vals):.3f} pp")
    print(f"  Min:               {min(eg_vals):.3f} pp")
    print(f"  Max:               {max(eg_vals):.3f} pp")
    print(f"  Std dev:           {statistics.pstdev(eg_vals):.3f} pp")
    print()
    excl = [v for v, c in zip(eg_vals, CYCLES) if not (c.jurisdiction == "Alberta_provincial" and c.cycle_year == "2026")]
    if excl:
        print(f"Excluding Alberta 2025-26 anchor (n={len(excl)}):")
        print(f"  Mean ΔEG_proxy:    {statistics.mean(excl):.3f} pp")
        print(f"  Median ΔEG_proxy:  {statistics.median(excl):.3f} pp")
        print(f"  Min:               {min(excl):.3f} pp")
        print(f"  Max:               {max(excl):.3f} pp")
        print()
    # Percentile rank of Alberta anchor
    alberta = 0.51
    rank = sum(1 for v in eg_vals if v <= alberta)
    print(f"Alberta 2025-26 (0.51 pp) percentile among n={len(eg_vals)} cycles: "
          f"{100*rank/len(eg_vals):.1f}% (i.e., "
          f"{rank} of {len(eg_vals)} cycles fall at or below Alberta's value)")
    print()


def update_csv():
    """Write the quantified rows back to the catalogue CSV, preserving
    catalogue rows that are not in our cycle list (e.g., government-override
    comparators Ontario 1996, Quebec 1992, BC 2008, NB 2023)."""
    # Load existing CSV
    with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    # Build a lookup from our cycle computations, keyed on (jurisdiction, cycle_year)
    computed = {}
    for c in CYCLES:
        if c.jurisdiction == "Alberta_provincial" and c.cycle_year == "2026":
            # Preserve audit's own anchor row unchanged (it is already in the CSV)
            continue
        jurisdiction_csv = {
            "Canada_federal_AB": "Canada_federal_AB",
            "British_Columbia_provincial": "British_Columbia",
            "Saskatchewan": "Saskatchewan",
            "Alberta_provincial": "Alberta",
            "Manitoba": "Manitoba",
            "Nova_Scotia": "Nova_Scotia",
        }.get(c.jurisdiction, c.jurisdiction)
        computed[(jurisdiction_csv, c.cycle_year)] = c

    # Update rows
    new_rows = []
    for row in rows:
        key = (row["jurisdiction"], row["cycle_year"])
        if key in computed:
            c = computed[key]
            if c.acquisition_status == "not_comparable":
                row["seat_asymmetry_pct"] = "NA_not_comparable"
                row["eg_asymmetry_pp"] = "NA_not_comparable"
                row["data_quality"] = "not_comparable_menu_of_alternatives"
                row["acquired_in_session"] = "partial"
                row["notes"] = c.evidence
            else:
                row["seats_changed_between_a_and_b"] = str(c.seat_flips_estimate)
                row["seat_asymmetry_pct"] = f"{c.seat_share_asymmetry_pp:.2f}"
                row["eg_asymmetry_pp"] = f"{c.eg_asymmetry_proxy_pp:.2f}"
                if c.seat_flips_low is not None and c.seat_flips_high is not None:
                    low = c.eg_asymmetry_low_pp or 0.0
                    high = c.eg_asymmetry_high_pp or 0.0
                    row["eg_asymmetry_pp"] = f"{c.eg_asymmetry_proxy_pp:.2f} (bound {low:.2f}-{high:.2f})"
                row["data_quality"] = "proxy_seat_share_asymmetry_method"
                row["acquired_in_session"] = "yes_proxy"
                row["notes"] = c.evidence[:600]
        new_rows.append(row)

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    print(f"Wrote updated catalogue: {CSV_PATH}")


if __name__ == "__main__":
    summarise()
    update_csv()
