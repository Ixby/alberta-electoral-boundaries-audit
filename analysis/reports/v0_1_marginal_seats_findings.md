# Marginal Seats and Uniform-Swing Analysis — v0.1

**Purpose.** The audit's partisan-shift range is abstract (roughly
0.5–1.6 pp in efficiency gap, 1–3 seats in a tied election). This
document translates that range into specific Alberta ridings and
specific past elections, so a general reader can see whether that kind
of shift is the kind that matters.

**Inputs.** `data/v0_1_alberta_{2015,2019,2023}_results.csv`.
**Script.** `analysis/scripts/v0_1_marginal_seats_analysis.py`.

**Method.** For each election, compute each ED's two-party NDP share
(NDP ÷ (NDP + UCP); for 2015, PC+WRP stands in for UCP). Signed margin
= NDP share − 50%. A "uniform swing of X pp toward UCP" subtracts X pp
from every ED's NDP share. Seats where the sign of the margin changes
are counted as flips. Non-two-party candidates (Liberal, AP, Green,
independents) are excluded from the share calculation — a simplifying
assumption that matches the audit's own two-party framing but
understates real-world fluidity in a handful of ridings where third
parties polled above a couple of points.

---

## What a 3 percentage point swing means in practice

Ridings decided by less than 3 pp of two-party margin:

| Election | Boundaries | Marginal (<3 pp) | Razor-thin (<1 pp) | <5 pp |
| --- | --- | --- | --- | --- |
| **2023** | current (post-2017) | **14 of 87** | 7 | 18 |
| **2019** | current (post-2017) | 7 of 87 | 3 | 13 |
| **2015** | pre-2017 (87 EDs) | 8 of 87 | 2 | 10 |

2023 stands out. It had roughly twice as many ridings in the flip-zone
as either 2019 or 2015. This is consistent with the broader picture of
2023 as Alberta's first genuinely competitive provincial election in
recent memory — and almost all of that concentration sits in Calgary.

Under the minority vs majority 2026 map difference, the audit's A2
analysis flags Calgary NDP-leaning districts as packed in the minority
proposal. Those are precisely the districts sitting in the flip zone
right now: in 2023, seven of fourteen Calgary ridings the NDP won
were inside a 3-pp margin.

---

## What a 1.5 pp swing (midpoint of the audit's estimate) actually does

A 1.5 pp uniform swing is the middle of the audit's stated
map-sensitivity range. Applied retrospectively:

### 2023 — 1.5 pp toward UCP flips 6 seats (all Calgary plus Banff-Kananaskis)

| ED | Prior winner | Prior margin |
| --- | --- | --- |
| Calgary-Acadia | NDP | +0.05 pp |
| Calgary-Glenmore | NDP | +0.09 pp |
| Calgary-Foothills | NDP | +0.60 pp |
| Calgary-Edgemont | NDP | +0.62 pp |
| Banff-Kananaskis | NDP | +0.66 pp |
| Calgary-Beddington | NDP | +1.36 pp |

### 2023 — 1.5 pp toward NDP flips 4 seats

| ED | Prior winner | Prior margin |
| --- | --- | --- |
| Calgary-North West | UCP | −0.30 pp |
| Calgary-North | UCP | −0.41 pp |
| Calgary-Bow | UCP | −1.21 pp |
| Lethbridge-East | UCP | −1.49 pp |

### 2019 — 1.5 pp toward UCP flips 1 seat; toward NDP flips 2

2019 was a blowout (UCP 63 / NDP 24 on two-party). The flip-zone is
small; a 1.5 pp swing moves only one or two ridings in either
direction.

### 2015 — 1.5 pp toward UCP-equivalent flips 2; toward NDP flips 1

2015 is on **pre-2017 boundaries** — the map that was replaced by the
current one. Individual ED names from this era cannot be one-to-one
compared to 2019/2023, and PC+WRP is a counterfactual stand-in for UCP
rather than the actual ballot. Numbers here are order-of-magnitude
only. The pattern, though, is consistent with 2019: a decisive
election has few seats in the flip zone.

---

## Seats to watch in 2027

Sorted by 2023 two-party margin, the most vulnerable ridings are:

1. Calgary-Acadia (NDP +0.05 pp)
2. Calgary-Glenmore (NDP +0.09 pp)
3. Calgary-North West (UCP −0.30 pp)
4. Calgary-North (UCP −0.41 pp)
5. Calgary-Foothills (NDP +0.60 pp)
6. Calgary-Edgemont (NDP +0.62 pp)
7. Banff-Kananaskis (NDP +0.66 pp)
8. Calgary-Bow (UCP −1.21 pp)
9. Calgary-Beddington (NDP +1.36 pp)
10. Lethbridge-East (UCP −1.49 pp)
11. Calgary-Elbow (NDP +1.57 pp)
12. Calgary-Cross (UCP −1.77 pp)
13. Calgary-Klein (NDP +2.14 pp)
14. Calgary-East (UCP −2.58 pp)

**Twelve of the fourteen razor-thin 2023 seats are in Calgary.** Using
a Zone-A heuristic — Calgary + 2023 NDP-held — seven of the fourteen
NDP-held Calgary ridings sit inside a 3-pp margin. These are the seats
the A2 packing analysis implicates in the minority-map scenario.

**Plain warning for the reader:** in these specific seats — Calgary-
Acadia, Calgary-Glenmore, Calgary-Edgemont, Calgary-Foothills,
Calgary-Beddington, Calgary-North West, Calgary-North, Calgary-Bow —
a 1-3 percentage-point map-driven shift is not hypothetical headroom.
It is the same size as the gap that decided the seat in 2023.

---

## Historical perspective

The 2023 result was UCP 49 / NDP 38 — an 11-seat gap. A 1-3 seat
map-driven flip would not have changed which party formed government.
**State that plainly:** the audit's finding is not "the map stole the
2023 election." It did not.

What the finding addresses is the next election, and any election
close to tied. In 2023, UCP won 49% of the two-party vote and the
legislature's majority. In a genuine coin-flip election, 1-3 seats is
exactly the width that decides who governs. The 1985 Ontario election
(minority PC / Liberal-NDP accord) was decided by four seats; BC 2017
was decided by a single seat flipping the Horgan NDP into a confidence-
and-supply arrangement; Quebec 2012 produced a PQ minority of four
seats over the Liberals. In each case a 1-3 pp swing in the map or
in the vote would have changed the outcome.

Alberta has not had an election in the modern era that close. The
audit's argument is not that it has — it is that the *map being
considered for 2027 biases the floor for the next one*, and the 2023
marginal landscape is where that bias lands.

---

## Caveats

- **Two-party simplification.** The uniform-swing model ignores
  Liberal, Alberta Party, Green, and independent vote share. In a few
  ridings (Lethbridge-West, Calgary-Currie) these parties polled
  non-trivially in 2023 and a real-world swing would be distributed
  unevenly among them. The direction of the flip-zone finding is
  robust; the exact number of seats at each threshold has ±1 seat of
  noise.
- **Uniform swing is uniform.** Real partisan shifts are regionally
  heterogeneous. Calgary and Edmonton often move in opposite
  directions. The flip-count numbers here assume every ED moves by the
  same amount, which is a stress test of the map's geometry, not a
  forecast.
- **2015 boundaries ≠ 2019/2023 boundaries.** Individual 2015 ED
  names should not be quoted as "Lesser Slave Lake would have flipped"
  because the riding no longer exists in the same form. Use 2015
  numbers only at the aggregate (`< 3 pp = 8 seats`) level.
- **Zone-A heuristic is name-based.** The "Calgary NDP-held" list is
  a proxy for the A2 packed-district set, not a spatial join. Use the
  A2 analysis's own district list for any claim that requires
  one-to-one correspondence.

---

## Summary (<200 words)

In 2023, **14 of 87** Alberta ridings were decided by a two-party
margin under 3 percentage points; in 2019, 7; in 2015, 8 (2015 on
older boundaries — not directly comparable). A uniform **1.5 pp
shift** — the midpoint of the audit's estimated map-driven swing
range — would have flipped **6 seats** in 2023 (all Calgary except
Banff-Kananaskis), 1 in 2019, and 2 in 2015. A 3.0 pp shift in 2023
would flip **8 seats**.

The 2023 result (UCP 49 / NDP 38, 11-seat gap) was too lopsided for a
1–3 seat map effect to change which party formed government. But in a
tied or near-tied election — the scenario the audit's efficiency-gap
language addresses — those marginal Calgary seats are exactly where a
1–3 pp map-driven shift decides the outcome. The concrete reading: a
3.9% population deviation is not numerically huge, but on the 2023
marginal landscape it is the same order of magnitude as the gap
separating several individual Calgary ridings from flipping. A shift
of that size would not have flipped 2023. It is the right size to
flip a tied 2027.
