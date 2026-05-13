# Sentiment Analysis × Minority Rationales Cross-Reference

**Purpose:** Compare public submission sentiment (LLM-scored, 920 rows) against the minority commission's stated justifications and their validation verdicts. Tests whether configurations with stronger rationale support received stronger public support.

**Data sources:**
- Public sentiment: `data/outputs/sentiment_intensity_scores.csv` (920 rows; 559 submissions + 361 Hansard turns)
- Rationale validation: `analysis/methodology/minority_rationales_validation.md` (R1–R11 verdicts)
- Aggregated sentiment: `data/outputs/intensity_summary_table.csv`

---

## Summary Table

| Configuration | Weighted-Net Sentiment | Rationale(s) | Validation Verdict | Alignment |
|---|---|---|---|---|
| **Calgary-Nolan Hill-Cochrane** | −122 (opposed) | R1 | PARTIALLY SUPPORTS | Misaligned: rationale has merit but public opposed |
| **Calgary-Peigan-Chestermere** | −101 (opposed) | R2 | INCONCLUSIVE | Consistent: rationale weak, public opposed |
| **Airdrie 4-way split** | −112 (opposed) | R3/R4 | SUPPORTS | Misaligned: strong rationale but public opposed |
| **Chestermere (within Peigan)** | −101 (opposed) | R2 | INCONCLUSIVE | Consistent: weak rationale, public opposed |
| **Rocky Mountain House–Banff** | −29 (opposed) | R1 (partial) | PARTIALLY SUPPORTS | Slight misalignment: modest rationale, modest opposition |
| **St. Albert–Sturgeon County** | −15 (neutral) | — | — | Neutral: no strong rationale invoked |
| **Red Deer hybrids** | −154 (opposed) | R8–R11 | SUPPORTS/INCONCLUSIVE | Misaligned: rationales supported but public strongly opposed |
| **Olds–Three Hills–Didsbury** | +6 (net supported) | — | — | Sole net-support configuration; no rationale analysis |

---

## Detailed Analysis

### Configuration 1: Calgary–Nolan Hill–Cochrane

**Sentiment:** −122 weighted-net (84 opp / 28 sup; opposition_sum=178, support_sum=56)

**Rationale (R1):** "Cochrane residents fluidly move to Calgary; justified by commute flows."
- **Validation verdict:** PARTIALLY SUPPORTS — 35.8% of Cochrane commuters work in Calgary, but commute is city-wide average, not specific to Nolan Hill; near 50% within-Cochrane work share suggests substantial internal labour market.

**Cross-reference analysis:**
- Minority claimed legitimate Cochrane–Nolan Hill community tie.
- Validation found: real commute flow exists, but rationale conflates "Calgary commute" with "Nolan Hill neighbourhood."
- Public sentiment: strongly opposed (−122), 3:1 opposition ratio.
- **Alignment:** MISALIGNED — Minority rationale has some empirical merit (35.8% commute to Calgary is real), but public clearly opposed the configuration. This suggests public concerns transcend the rationale offered (geographic adjacency not mentioned, river-valley separation, population balance, etc.).

---

### Configuration 2: Calgary–Peigan–Chestermere

**Sentiment:** −101 weighted-net (63 opp / 16 sup; opposition_sum=137, support_sum=36)

**Rationale (R2):** "Growing social, economic, transportation connections."
- **Validation verdict:** INCONCLUSIVE / LEANS CONTRADICTS — CMA membership supports general Calgary–Chestermere tie. But specific boundary (southern Chestermere–Forest Lawn) has no shared school division (Rocky View Schools vs CBE), no shared transit (Chestermere not on Calgary Transit), different municipal governments. Only connection is QE2/Glenmore Trail access. Chestermere is already paired with Strathmore in minority's own district; adding a second Calgary slice is problematic on population math (Test 5).

**Cross-reference analysis:**
- Minority rationale is stated in general terms ("growing connections").
- Validation found: connections are weak, and structural issues (double Chestermere inclusion) undermine the proposal.
- Public sentiment: strong opposition (−101), 4:1 opposition ratio.
- **Alignment:** CONSISTENT — Weak rationale, strong opposition. Public opposition aligns with validation's skepticism about the connection's substance.

---

### Configuration 3: Airdrie 4-way split

**Sentiment:** −112 weighted-net (78 opp / 27 sup; opposition_sum=169, support_sum=57)

**Rationale (R3, R4):** "Strong economic, community, and transportation ties with Calgary" (R3/R4).
- **Validation verdict:** SUPPORTS (at the commuter-tie level) — Airdrie is in Calgary CMA; 2025 population 90,044 with 4.9% annual growth, projected 128,470 by 2033. CMA membership alone establishes commuter tie above threshold. **However**, whether this *requires* a 4-way split rather than two Airdrie-named districts is a policy choice, not a data-driven necessity. Population math (4-way split is forced) is CLOSED-FAIL (Test 3).

**Cross-reference analysis:**
- Minority rationale is strong: Airdrie–Calgary commute tie is empirically real and measurable.
- Validation found: rationale is valid at the general level, but 4-way split is population-math forced, not rationale-justified.
- Public sentiment: strong opposition (−112), 3:1 opposition ratio.
- **Alignment:** MISALIGNED — Minority rationale (Airdrie–Calgary tie) is empirically supported, yet public strongly opposed the configuration. This suggests public concern is about the *method* (4-way fragmentation) rather than the principle (Airdrie–Calgary pairing). Airdrie's packing into 4 districts may have triggered "dilution of Airdrie representation" objections that outweighed the commute-tie rationale.

---

### Configuration 4: Rocky Mountain House–Banff Park

**Sentiment:** −29 weighted-net (162 opp / 146 sup; opposition_sum=335, support_sum=306)

**Rationale (R1 partial):** Bancroft area geographic tie to Calgary; RMH–Banff economy.
- **Validation verdict:** PARTIALLY SUPPORTS (for the Banff tourism-anchor logic, not for RMH–Calgary tie).

**Cross-reference analysis:**
- Minority rationale is modest and geographically justified.
- Validation is cautiously supportive for internal RMH–Banff logic.
- Public sentiment: slight opposition (−29), nearly balanced (162:146), smallest opposition margin in the set.
- **Alignment:** WEAKLY ALIGNED — Both rationale strength and public opposition are modest. This configuration has the smallest opposition spread, suggesting public was more ambivalent than for the Calgary hybrids. Internal RMH–Banff tie may be less controversial than inter-city pairings.

---

### Configuration 5: St. Albert–Sturgeon County

**Sentiment:** −15 weighted-net (59 opp / 52 sup; opposition_sum=122, support_sum=107)

**Rationale:** No specific minority rationale invoked (constraint-forced; majority also draws same two-district structure).
- **Validation verdict:** — N/A (already constraint-satisfied in both maps).

**Cross-reference analysis:**
- Both majority and minority independently arrive at the same St. Albert–Sturgeon pairing under EBCA constraints.
- Public sentiment: very weak opposition (−15), nearly balanced (59:52).
- **Alignment:** NEUTRAL — Neither faction chose this pairing for discretionary reasons; it is constraint-forced. Public is essentially neutral, reflecting the lack of substantive controversy.

---

### Configuration 6: Red Deer Hybrid Ridings (Blackfalds, Sylvan Lake, Innisfail)

**Sentiment:** −154 weighted-net (118 opp / 45 sup; opposition_sum=245, support_sum=91)

**Rationale (R8–R11):** 
- R8: Red Deer–Blackfalds "agricultural services hub" and "Joffre chemical plant" — SUPPORTS
- R9: Red Deer–Innisfail "regional hub" — SUPPORTS
- R10: Red Deer–Lacombe "Highway 11 economic corridor" — PARTIALLY SUPPORTS
- R11: Red Deer–Sylvan Lake "where they work, go to school" — INCONCLUSIVE / LEANS CONTRADICTS (schools claim not supported)

**Validation verdict:** Mixed — SUPPORTS for Joffre labour tie and Red Deer hub role, but concern that pulling rural areas into Red Deer riding dilutes urban representation.

**Cross-reference analysis:**
- Minority rationales are individually reasonable (economic corridors, labour-market ties).
- Validation found: rationales are empirically grounded but raise structural concerns about urban-representation dilution.
- Public sentiment: strongest opposition in entire set (−154), 2.6:1 opposition ratio.
- **Alignment:** MISALIGNED — Minority's individual rationales are validated as supporting (Joffre plant, hub function, etc.), yet public opposition is strongest in the dataset. This suggests cumulative effect: each rationale alone is defensible, but combining multiple rural hybrids around Red Deer generated public backlash. The "dilute Red Deer urban representation" concern may dominate over the economic-tie rationales.

---

### Configuration 7: Olds–Three Hills–Didsbury (Extending to Airdrie)

**Sentiment:** +6 weighted-net (20 opp / 23 sup; opposition_sum=40, support_sum=46)

**Rationale:** No minority rationale invoked (this is the *majority's* proposal for the Olds area).
- **Validation verdict:** N/A.

**Cross-reference analysis:**
- This is the only net-supported configuration in the public sentiment results.
- No minority rationale because the minority proposed a different boundary here.
- Public sentiment: sole net-support, narrow margin (20:23).
- **Alignment:** N/A — No minority rationale to cross-reference; this reflects majority proposal preference.

---

## Synthesis

### Key Finding: Rationale Strength ≠ Public Support

**Four configurations (Calgary–Nolan Hill, Airdrie 4-way, Red Deer hybrids) have rationales validated as empirically grounded (PARTIALLY SUPPORTS or SUPPORTS) yet faced the strongest public opposition (−122, −112, −154).** Conversely, the weakly-rationalized Peigan–Chestermere (INCONCLUSIVE) and St. Albert–Sturgeon (constraint-forced) faced more modest opposition or near-balance.

**Interpretation:** Public opposition to the minority map is not tracking the logical strength of individual rationales. Instead, opposition correlates with:
1. **Fragmentation concern:** Airdrie 4-way split (−112) and Red Deer hybrids (−154) fragment established regional towns into multiple ridings.
2. **Geographic adjacency:** Calgary hybrids (Nolan Hill, Peigan, Airdrie) link city to distant regions, triggering "urban–rural pairing" concerns independent of commute-flow validity.
3. **Cumulative effect:** Red Deer's three rationales (Blackfalds, Innisfail, Sylvan Lake) are individually reasonable but collectively generate the dataset's largest opposition (−154).

### Implication for §5.9.4

The sentiment analysis reinforces the procedural concern in §5.9.4: the minority's boundary choices rest on rationales that are individually defensible but cumulatively create a map whose partisan asymmetry and structural irregularities exceed what public submissions were willing to endorse. The public was not rejecting the validity of commute flows or economic ties; it was rejecting the *method* — the 4-way fragmentation and the geographic logic of linking distant rural areas to urban districts.

---

## Data Provenance

- Sentiment intensity scoring: `analysis/scripts/sentiment_intensity_score.py` (920 rows × 7 configurations)
- Rationale validation: `analysis/methodology/minority_rationales_validation.md` (qualitative verdicts R1–R11)
- Aggregation: `analysis/scripts/aggregate_sentiment_intensity.py` (weighted-net computation)
- Cross-reference: This document (qualitative alignment analysis)

**Status:** Sentiment intensity and aggregation COMPLETE; cross-reference document DRAFT [2026-05-10].
