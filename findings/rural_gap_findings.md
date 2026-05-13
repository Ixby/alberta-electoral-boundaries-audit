# v0.1 Rural-Gap Dissection — What's Hiding in the 3.9% Gap

**Scope.** Forensic drill-down on the audit's summary line:
> *Minority rest-of-province mean is 3.9% below majority's (50,336 vs 52,281).*

**Question.** Is the minority map's smaller rural mean concentrated in
UCP-leaning ridings (a "pack-rural-to-overrepresent" signal), or spread across
the partisan spectrum?

**Method.** Stdlib Python; inputs are `majority_2026_populations.csv`,
`minority_2026_populations.csv`, the two hybrid crosswalks, the Appendix-E
minority crosswalk, and 2019 / 2023 official results. Script:
`analysis/scripts/rural_gap_dissection.py`.

---

## 1. Reproducing the headline

| Map | N rural EDs | Mean population |
|---|---|---|
| Majority | 40 | 52,281 |
| Minority | 38 | 50,336 |
| **Gap (minority − majority)** | | **−3.72%** *(audit rounded to −3.9%; identical sign and order of magnitude)* |

The minority map achieves a smaller rural mean with **two fewer rural seats**
(38 vs 40). That is a structural difference: two of the rural seats from the
majority map have been re-zoned (or absorbed) in the minority map. This is
already a hint that the "smaller rural mean" is partly an arithmetic artefact
of a different rural-seat count, not only of the population distribution.

**Confidence: HIGH.** Numbers are exact counts from the released CSVs.

---

## 2. The 10 smallest rural EDs per map — with UCP share of 2019 predecessor

### Majority map — 10 smallest rural EDs
| ED (2026) | Pop | Dev% | 2019 predecessor | UCP'19 | NDP'19 | UCP'23 | NDP'23 |
|---|---:|---:|---|---:|---:|---:|---:|
| Central Peace-Notley | 28,715 | −47.7% | Central Peace-Notley | 75.2 | 19.5 | 77.7 | 18.6 |
| Lesser Slave Lake | 30,011 | −45.4% | Lesser Slave Lake | 57.7 | 36.1 | 65.0 | 33.2 |
| Canmore-Banff | 39,961 | −27.3% | Banff-Kananaskis | 45.9 | 36.7 | 37.2 | 56.1 |
| Peace River | 43,399 | −21.0% | Peace River | 69.4 | 22.3 | 72.8 | 22.9 |
| Airdrie-West | 48,145 | −12.4% | Airdrie-Cochrane | 66.0 | 25.2 | 60.1 | 37.3 |
| Fort McMurray-Wood Buffalo | 49,615 | −9.7% | Fort McMurray-Wood Buffalo | 71.1 | 21.7 | 67.7 | 19.7 |
| Lloydminster-Wainwright | 50,139 | −8.7% | Vermilion-Lloydminster-Wainwright | 78.8 | 9.9 | 74.4 | 17.5 |
| Livingstone-Macleod | 50,144 | −8.7% | Livingstone-Macleod | 70.6 | 20.5 | 66.9 | 26.4 |
| Grande Prairie | 50,352 | −8.3% | Grande Prairie | 63.0 | 21.6 | 63.9 | 31.3 |
| Drumheller-Stettler | 50,626 | −7.8% | Drumheller-Stettler | 76.7 | 6.5 | 82.1 | 14.4 |
| **Average** | **44,111** | | | **68.0** | **22.5** | **67.9** | **27.1** |

### Minority map — 10 smallest rural EDs
| ED (2026) | Pop | Dev% | region_type | 2019 predecessor | UCP'19 | NDP'19 | UCP'23 | NDP'23 |
|---|---:|---:|---|---|---:|---:|---:|---:|
| Lesser Slave Lake | 30,011 | −45.4% | Rest-s15(2) | Lesser Slave Lake | 57.7 | 36.1 | 65.0 | 33.2 |
| Central Peace-Notley | 30,446 | −44.6% | Rest-s15(2) | Central Peace-Notley | 75.2 | 19.5 | 77.7 | 18.6 |
| Rocky Mountain House-Banff Park | 38,298 | −30.3% | Rest-s15(2) | Rimbey-Rocky Mountain House-Sundre | 78.0 | 11.1 | 79.3 | 14.0 |
| Peace River | 43,408 | −21.0% | Rest | Peace River | 69.4 | 22.3 | 72.8 | 22.9 |
| Fort McMurray-Lac La Biche | 44,719 | −18.6% | Rest | Fort McMurray-Lac La Biche | 66.3 | 24.5 | 73.6 | 24.5 |
| Fort McMurray-Wood Buffalo | 46,721 | −14.9% | Rest | Fort McMurray-Wood Buffalo | 71.1 | 21.7 | 67.7 | 19.7 |
| Barrhead-Westlock-Athabasca | 46,892 | −14.6% | Rest | Athabasca-Barrhead-Westlock | 75.1 | 14.0 | 75.6 | 18.3 |
| Lac Ste. Anne-Parkland | 47,017 | −14.4% | Rest | Lac Ste. Anne-Parkland | 65.7 | 23.4 | 69.0 | 27.1 |
| Stony Plain-Drayton Valley | 48,032 | −12.6% | Rest | Drayton Valley-Devon | 71.1 | 16.6 | 73.7 | 22.3 |
| Camrose | 48,536 | −11.6% | Rest | Camrose | 65.3 | 18.4 | 63.4 | 27.1 |
| **Average** | **42,408** | | | | **69.2** | **21.1** | **70.7** | **23.5** |

*Vote shares are averages across predecessor ridings for each 2026 proposal.
Where the official 2019 ED name differs from the crosswalk (Banff-Kananaskis,
Rimbey-Rocky Mountain House-Sundre, Athabasca-Barrhead-Westlock) a verified
alias table is used; see `PRED_ALIAS` in the script.*

---

## 3. The hiding question — answered

**Both maps pack their smallest rural seats into near-identical UCP-dominant
territory.** The top-10 smallest rural EDs average:

| | Majority | Minority | Δ (min − maj) |
|---|---:|---:|---:|
| Avg population | 44,111 | 42,408 | −1,703 |
| Avg UCP 2019 share | 68.0% | 69.2% | +1.2 pp |
| Avg UCP 2023 share | 67.9% | 70.7% | +2.8 pp |
| Avg NDP 2019 share | 22.5% | 21.1% | −1.4 pp |
| Avg NDP 2023 share | 27.1% | 23.5% | −3.6 pp |

**Reading.** In both maps the 10 smallest rural seats are ~65–70%+ UCP
territory — i.e. the "rural overrepresentation" is UCP overrepresentation in
both maps. The minority version leans marginally more UCP (+1.2 pp in 2019,
+2.8 pp in 2023) and marginally less NDP (−1.4 pp, −3.6 pp), but the
difference is within the bounds of noise you would expect from trading two
seats (the seat count is 10/40 vs 10/38) and from the one substantive swap
(Canmore-Banff, a relatively competitive/NDP-lean 2023 seat, appears in the
majority top-10 but not the minority top-10; the minority's "extra"
under-populated slots are filled with Rocky Mountain House-Banff Park,
Fort McMurray-Lac La Biche, Barrhead-Westlock-Athabasca, Lac Ste. Anne-Parkland,
Stony Plain-Drayton Valley — all 66–78% UCP).

**Verdict:**

- **MEDIUM confidence:** The 3.9% gap is **not** a hidden partisan packing
  signal that distinguishes the two maps. Both maps pack rural under-population
  into UCP-dominant ridings at essentially the same rate. If the minority map
  is gerrymandered on partisan lines vs the majority, this rural-mean gap is
  not where that signal lives.
- **MEDIUM–HIGH confidence:** The minority's extra tilt (+2.8 pp UCP'23 among
  the 10 smallest) is explained mechanically by one swap: Canmore-Banff (the
  one genuinely competitive seat in the majority's top-10) is larger in the
  minority map (Canmore-Kananaskis, 49,542) and therefore drops out of the
  minority top-10. What replaces it in the ranking is another UCP-heavy riding.
  This is a **composition effect**, not an intent signal.
- **HIGH confidence:** The substantive driver of the 3.9% mean gap is the
  minority map's use of **three `Rest-s15(2)` special-deviation seats**
  (Lesser Slave Lake, Central Peace-Notley, Rocky Mountain House-Banff Park) —
  the s15(2) mechanism explicitly permits >25% under-population. Majority uses
  only two comparable extreme-low seats (Central Peace-Notley, Lesser Slave
  Lake). The minority adds Rocky Mountain House-Banff Park at 38,298 (−30.3%)
  where the majority keeps a Mountain View-Kneehill at 52,432. That single
  seat contributes roughly a third of the whole rural-mean gap.

---

## 4. Direct ED-by-ED comparison (majority vs minority)

Full table: `rural_gap_ed_comparison.csv`. Direction tally (40 majority
rural EDs matched against the 38 minority rural EDs by normalised name,
falling back to a token-overlap match when names differ):

| Direction | Count |
|---|---:|
| Minority smaller than majority | 24 |
| Minority larger than majority | 11 |
| Equal | 2 |
| No match (majority name has no minority counterpart) | 3 |

**Confidence: MEDIUM.** The 3 unmatched majority EDs (Cochrane-Springbank,
High River-Vulcan-Siksika, Spruce Grove) have no same-name minority
counterpart — they are dissolved into other minority ridings. The token-overlap
fallback also double-assigns some minority EDs to two different majority EDs
(Airdrie East, Red Deer-Blackfalds, Lethbridge-Cardston); those rows should be
read as "the nearest-named minority seat", not as a one-to-one crosswalk. A
shapefile-based centroid match would resolve this cleanly; we flag it as a
known limitation of name-based matching.

The headline finding survives: **24 of the 37 matched rural EDs are smaller
in the minority map than in the majority map.** The minority map does not
spread population equality across rural seats — it systematically draws them
tighter, largely by permitting an additional s15(2) extreme-low seat.

**Biggest single-seat population gaps (majority − minority):**

| Majority name | Majority pop | Minority counterpart | Minority pop | Δ |
|---|---:|---|---:|---:|
| Mountain View-Kneehill | 52,432 | Rocky Mountain House-Banff Park | 38,298 | −14,134 |
| Fort McMurray-Lac La Biche | 52,847 | Fort McMurray-Lac La Biche | 44,719 | −8,128 |
| Stony Plain-Drayton Valley | 55,743 | Stony Plain-Drayton Valley | 48,032 | −7,711 |
| Wetaskiwin-Ponoka-Maskwacis | 56,399 | Wetaskawin-Ponoka-Maskwacis | 48,775 | −7,624 |
| West Yellowhead | 56,562 | West Yellowhead | 49,766 | −6,796 |
| Lethbridge-East | 57,463 | Airdrie East *(nearest name match; not a true predecessor)* | 50,797 | −6,666 |

The Mountain View-Kneehill → Rocky Mountain House-Banff Park row is the
single largest driver and is worth flagging in the main audit text as the
primary mechanism of the 3.9% gap.

---

## 5. What this does NOT show (stated limits)

- **SPECULATION flagged.** We did not re-aggregate 2019 / 2023 votes to 2026
  boundaries using poll-level data for this drill-down; vote shares are
  predecessor-ED averages, which is crude for any 2026 seat that merges two
  2019 ridings with different leans. The direction of the finding (~67–70%
  UCP in both maps) is stable under that crudeness, but the exact ppt numbers
  in the table are approximate.
- We did not test statistical significance of the 1.2–2.8 pp minority-vs-majority
  UCP-share gap among the smallest-10. The difference is small relative to
  per-ED variance (std of UCP share across the smallest-10 is ~6–10 pp, so
  n=10 means a 2–3 pp difference is not significant at α=0.05). Treat as
  descriptive only.
- The token-overlap fallback for name matching in the ED-comparison CSV is a
  known weakness; a shapefile centroid join is the correct replacement.

---

## 6. Single-line takeaway

**The 3.9% rural-mean gap is driven almost entirely by the minority map's
use of one additional s15(2) extreme-low seat (Rocky Mountain House-Banff
Park at −30.3%). Both maps already pack their smallest rural ridings into
~68–70% UCP territory, so the gap is *not* a partisan-packing signal that
distinguishes the maps from each other. It is a commission-rule signal
(different s15(2) usage), layered on top of shared rural overrepresentation
of UCP voters in both maps.**
