# Alberta Electoral Boundary Audit: Plain-Language Findings Brief

**May 2026 — Phase 4C canonical results**

---

## Background

In 2025–26, Alberta's Electoral Boundary Commission produced two competing maps for the province's 89 electoral districts. Three commissioners signed the majority map; two signed the alternative (minority) map. On April 16, 2026, the provincial government set both maps aside and assigned the redrawing task to a five-member committee of MLAs — three from the governing United Conservative Party. This audit measured both commission maps using identical statistical methods applied symmetrically. All analysis uses official Elections Alberta shapefiles.

---

## What the Audit Found

**The two maps differ on six measurable structural properties, and the differences consistently point in the same direction.**

### 1. Population equality

Every electoral district should contain close to the same number of people. The tighter the spread, the more equal each citizen's vote. Under the majority map, the average district deviates from the provincial mean by approximately **3,180 people**. Under the minority map, that figure is **4,707 people — 48% wider** than under the majority map.

### 2. Seat allocation at a tied vote

The most direct test: hold the provincial vote at exactly 50% for each party and ask how many seats each map awards. At a perfect tie, the majority map produces approximately **48 NDP seats** (53.9%) out of 89. The minority map produces approximately **43 NDP seats** (48.3%) — a **5-seat swing to the UCP** relative to the majority map, without changing a single vote.

This was tested against a computer simulation of 1,010,000 independently drawn neutral Alberta maps using the same population rules. The majority map's result sits inside the normal range (83rd percentile). The minority map's result is reached by fewer than 100 of 1,010,000 neutral draws.

### 3. Vote-to-seat translation imbalance

In any election, some votes are "wasted" — cast for a losing candidate, or piled onto a winner who didn't need them. When one party's votes are systematically wasted at a higher rate, the map gives the other party's votes more seat-earning power per ballot. This analysis measures that imbalance across all 89 districts.

Under the **majority map**, the gap in wasted votes between the two parties amounts to roughly **881 votes** out of 896,644 partisan ballots cast — about 0.1% of the total. Under the **minority map**, the same calculation yields a gap of roughly **36,000 votes** — about 4.0% of all ballots cast. The minority map's structural vote-to-seat imbalance is approximately **41 times larger** than the majority map's. Both gaps favour the UCP.

### 4. Calgary and Airdrie district structure

The minority map splits the City of Airdrie into **four separate districts**, each attached to a different rural or Calgary-edge constituency, where the majority map uses two. The minority map over-represents Calgary's northwest quadrant — a predominantly UCP area — by **11.5% above the provincial average**, compared to **2.8%** under the majority map.

---

## What This Audit Does Not Claim

This audit does not conclude that either map constitutes a gerrymander in any legal sense. Canada has no statute or common-law rule that defines redistricting manipulation as a legal wrong by that name. The applicable legal standards in Canada are the *Electoral Boundaries Commission Act* (EBCA), which governs the commission's process, and section 3 of the *Canadian Charter of Rights and Freedoms*, which guarantees the right to effective representation. Whether the statistical patterns documented here rise to a violation of either standard is a question for courts, legislators, and legal scholars — not this audit.

This audit also does not establish intent. Statistical asymmetry is consistent with deliberate manipulation, with geographic sorting of voters, or with coincidence. The audit measures effect, not motive.

---

## Methodology Note

All results use the official Elections Alberta shapefiles (GeoPackage format, Phase 4C release). Vote attribution is computed by centroid-in-polygon spatial join of 4,765 voting areas to the proposed district boundaries. The simulation ensemble consists of 1,010,000 neutral maps generated via Markov-chain redistricting (ReCom algorithm) under the same population-equality rules that governed the commission. Analysis is pre-registered on the Open Science Framework (OSF:6pt83, AsPredicted:#289,469, AsPredicted:#289,451). Full methodology is in the academic report.

---

## Disclosure

The author is a student at Mount Royal University. This research was conducted independently and was not commissioned as coursework. The views expressed are the author's own and do not represent Mount Royal University. The author has no employment, contractual, or advisory relationship with Elections Alberta, the Electoral Boundaries Commission, or any provincial political party. The author has in the past donated to and volunteered for the NDP; this is disclosed because it is a potential source of motivated reasoning. The methodology — symmetric measurement of both maps, pre-registration of all tests before examining results, and open publication of all data and code — is the structural safeguard against that bias. This research received no external funding.

---

*Full reports: `reports/academic/report_academic.md` (technical monograph) and `reports/public/report_public.md` (plain-language).*
*Data and code: [github.com/Ixby/alberta-electoral-boundaries-audit](https://github.com/Ixby/alberta-electoral-boundaries-audit)*
