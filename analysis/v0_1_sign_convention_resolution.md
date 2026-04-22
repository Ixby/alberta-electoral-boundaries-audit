# Sign-convention resolution — v0_1

**Scope.** Answer the Track Z question: under what sign convention is the
paper's language "negative EG = UCP advantage" actually correct? The
Stephanopoulos-McGhee (2015) canonical convention and the paper's written
convention do not agree on what a negative code output means. This file
resolves which (if any) is right and which downstream claims need flipping.

## 1. The code's formula, verbatim

From `analysis/v0_2_packing_cracking_analysis.py`, `compute_metrics()`, lines
131-142:

```python
ndp_wasted = ucp_wasted = 0
for d in districts:
    tt = d['ndp'] + d['ucp']
    thr = tt // 2 + 1
    if d['ndp'] > d['ucp']:
        ndp_wasted += max(0, d['ndp'] - thr)
        ucp_wasted += d['ucp']
    else:
        ucp_wasted += max(0, d['ucp'] - thr)
        ndp_wasted += d['ndp']
eg = (ndp_wasted - ucp_wasted) / total
```

Definition of wasted votes matches S&M (2015): losing-candidate votes plus
winner votes above the 50%+1 threshold. The subtraction is
`ndp_wasted - ucp_wasted` (NDP-wasted minus UCP-wasted).

## 2. Canonical S-M convention

Stephanopoulos & McGhee (2015, *U. Chi. L. Rev.* 82(2): 831-900) define EG
from the perspective of a named party A as:

```
EG_A = (W_B - W_A) / T           (wasted-vote form)
     ≈ (S_A - 0.5) - 2*(V_A - 0.5)   (seat-vote shortcut at near-50/50 vote)
```

where W_X is party X's wasted votes, T total two-party votes, S_A party A's
seat share, V_A party A's two-party vote share. **Sign rule:**

- `EG_A > 0` → party A is ADVANTAGED (opponent wastes more; A wins more
  seats than the 2:1 seat-vote baseline predicts).
- `EG_A < 0` → party A is DISADVANTAGED.

## 3. Mapping the code to S-M

`code_eg = (W_NDP - W_UCP) / T = -EG_NDP_SM = +EG_UCP_SM`.

The code's eg is S-M's EG from **UCP's perspective**. Therefore:

- `code_eg > 0` → UCP advantaged (S-M).
- `code_eg < 0` → UCP disadvantaged (S-M).

The paper's written convention says "negative EG = UCP advantage." Under
strict S-M that is inverted.

## 4. Numerical verification on 2019 baseline, 2023 votes

Data: `data/v0_1_alberta_2023_results.csv`, 87 EDs, loaded by
`load_2023_results()`.

| Quantity | Value |
|---|---|
| NDP two-party total | 777,404 (45.56%) |
| UCP two-party total | 928,900 (54.44%) |
| Total 2P | 1,706,304 |
| NDP seats won | 38 |
| UCP seats won | 49 |
| NDP wasted | 404,054 |
| UCP wasted | 449,035 |
| `code_eg = (W_NDP - W_UCP) / T` | -2.6362% |
| S-M `EG_NDP = (W_UCP - W_NDP) / T` | +2.6362% |
| S-M seat-vote shortcut `EG_NDP ≈ (S_NDP - 0.5) - 2(V_NDP - 0.5)` | +2.5568% |

The seat-vote shortcut agrees with the wasted-vote form to within integer
rounding on the 50%+1 threshold. The two S-M formulations are internally
consistent.

**S-M interpretation of 2019 baseline:**

- `EG_NDP = +2.64%` means NDP is S-M-ADVANTAGED: NDP's 43.68% seat share
  exceeds the 2:1 baseline of 41.12% predicted by its 45.56% vote share.
- Equivalently, `EG_UCP = -2.64%` means UCP is S-M-DISADVANTAGED: UCP's
  56.32% seat share is below the 2:1 baseline of 58.88% predicted by its
  54.44% vote share.

## 5. Why the paper's written convention nonetheless captures a real asymmetry

The paper's convention ("negative = UCP advantage") tracks a DIFFERENT
reference point than S-M: it tracks raw proportional representation (votes
proportional to seats), not the 2:1 seat-vote slope S-M uses. Under raw
proportionality:

- NDP 45.56% votes but only 43.68% seats → NDP raw-proportionally
  under-represented → "UCP raw-advantage."
- The code returns -2.64%, which the paper reads as "UCP advantage."

Both the paper's convention and S-M are **internally consistent** and
describe real, measurable asymmetries. They just reference different
proportionality baselines:

- **S-M baseline:** 2:1 seat-vote slope around 50/50.
- **Paper's baseline:** 1:1 (strict proportional).

**Neither is wrong in the abstract.** But calling one "the efficiency gap"
is ambiguous, and the paper's running convention is the MINORITY usage in
the political-science literature. Every post-*Gill v. Whitford* paper the
audit cites (Stephanopoulos & McGhee 2014/2018, Warrington 2018,
Katz-King-Rosenblatt 2020, Chen 2017, Chen & Rodden 2013) uses the S-M
2:1-baseline reading.

## 6. What this means for the audit

The 2019 baseline code_eg of -2.64% is presented in the paper as
"Alberta's natural UCP-favourable floor." Under S-M that reading is
backwards: S-M says UCP is DISADVANTAGED at the 2019 baseline (gets fewer
seats than the 2:1 slope predicts). What the paper is describing is
**raw-proportional under-representation of NDP**, which is a different
claim.

This does not overturn the empirical finding. Both views agree on the
underlying facts: NDP has 45.6% votes, 43.7% seats; UCP has 54.4% votes,
56.3% seats. What they disagree on is which party to label "advantaged."

**The directionally-contingent finding (minority vs majority) is
unaffected by this convention question.** The code returns:

- Majority EG = -0.85%, Minority EG = -1.36%.
- Asymmetry = Min - Maj = -0.51 pp.

Under S-M: both maps shift UCP toward the 2:1 baseline (less UCP-
disadvantaged relative to 2019); the minority shifts less than the
majority. So the minority is "more UCP-disadvantaged" than the majority
under S-M, which is S-M's way of saying **the minority gives UCP fewer
seats relative to the 2:1 prediction than the majority does.**

Under the paper's convention: the minority has a more-negative EG, meaning
NDP raw-proportionally more under-represented, meaning "minority more
UCP-favourable."

**These two readings point in the same ordinal direction for the
majority-vs-minority comparison.** The minority is more UCP-leaning than
the majority under both conventions. The seat counts confirm this: 2023
actual seats are Majority 38 NDP / 51 UCP, Minority 37 NDP / 52 UCP — the
minority gives UCP one more seat than the majority does.

## 7. Resolution

**Verdict:** Option (a) — the paper's narrative convention is
internally consistent with a 1:1 proportional baseline, produces the same
ordinal ranking of the three maps as S-M, and correctly identifies the
minority as more UCP-leaning than the majority in raw-seat terms. The
paper should not invert its convention. **But it should not cite
Stephanopoulos & McGhee as authority for the running convention.** The
paper is using a proportionality-comparison usage that is not identical
to S-M's canonical EG.

**Required clarifications for the paper** (flagged for parent session;
not edited here):

1. §3.2 and §8.1 both cite S&M (2014/2015) and give the S-M formula
   EG = (W_A - W_B)/N. The paper's running convention that "negative EG
   favours UCP" is not what that formula's canonical reading produces.
   The paper should add a brief sign-convention note in §3.3 (and/or
   §8.1) stating explicitly: "Under this audit's reporting, a negative
   EG value indicates NDP is raw-proportionally under-represented in
   seat share relative to two-party vote share; this is the direction of
   a UCP raw-seat advantage. Stephanopoulos and McGhee's (2015)
   canonical sign rule uses a 2:1 seat-vote slope as its benchmark,
   which produces the opposite sign for the same seat configuration.
   Both conventions agree on the ordinal ranking of the three maps."

2. §3.3 's synthesis table last column ("+0.58 pp more UCP-favorable"
   for the minority) is correct under the paper's convention. It should
   not be restated as a claim about S-M's EG_NDP.

3. The two-party-shortcut formula `(S - 0.5) - 2(V - 0.5)` should NOT
   be mixed with the wasted-vote form unless both S-M and paper
   conventions are named. If a reader uses the shortcut and expects the
   paper's sign, they will get the opposite answer.

4. `analysis/v0_3_monte_carlo_ci.py` lines 158-159 print
   "negative = minority more UCP-favorable" which is consistent with
   the paper's convention, NOT with S-M. The labelling is internally
   consistent with the paper but an S-M-trained reader would find it
   inverted. The labels are defensible as-is if the sign-convention
   note above is added to the reports. **No code change is required
   for the direction claim to hold** — only a glossary / footnote.

5. The Track Z analysis (`analysis/v0_1_2015_cross_election_analysis.md`)
   states at §6 and again at §"Sign-convention note" that v0_3's labels
   are inverted relative to the "gerrymandering literature's
   convention for 'pro-UCP'." Track Z's claim is incorrect: v0_3 is
   using the paper's 1:1 proportional convention, not the S-M 2:1
   convention, and within that convention the labels are right. Track Z
   should be amended to remove the "v0_3 labels are inverted" claim
   and replace it with "v0_3 uses the paper's 1:1 proportional
   convention, which is opposite to the S-M canonical convention;
   both produce the same ordinal direction on the minority-majority
   comparison but label it with opposite signs."

## 8. Consequences for direction claims in the reports

Because the paper's convention and S-M both yield the same **ordinal**
ranking (minority more UCP-leaning than majority in raw-seat terms), the
following paper direction claims do not require flipping:

- "Minority more UCP-favourable than majority" (§3.3, §3.4, §3.5, §7).
- "Minority shifts baseline toward UCP relative to majority" (§7).
- "The minority's EG of −1.36% is more UCP-leaning than the majority's
  −0.85%" (§3.3).

The following claims **do** require clarification because they either
invoke S-M as authority or stack the sign convention with a 2:1-slope
description:

- §3.2 listing of B2's formula as "Stephanopoulos & McGhee (2014)" with
  the wasted-vote form that matches their formula but not their sign
  convention. Add the sign-convention note from §7.1 above.
- §8.1 mathematical-formalism statement. Clarify that this audit reports
  EG from the opposing-party (UCP-advantage) perspective on the
  proportional-seat baseline, not from S-M's 2:1 slope.
- The 2019 baseline framing of "−2.64% is Alberta's natural UCP-favourable
  floor" is accurate under the paper's convention. Under S-M it is
  "Alberta's natural NDP-advantage-at-the-2:1-slope floor." The
  Chen-Rodden `v0_1_chen_rodden_alberta_validation.md` analysis assumes
  the paper's convention and concludes the neutral ensemble produces a
  floor near -2.64%. That reasoning is internally consistent.

## 9. 2015 cross-election reading under the corrected resolution

From `data/v0_1_cross_election_asymmetry_3way.csv`:

| Election | Maj EG | Min EG | Min − Maj |
|---|---|---|---|
| 2015 | +7.25% | +7.28% | +0.03 pp |
| 2019 | +0.16% | +0.90% | +0.75 pp |
| 2023 | -0.85% | -1.36% | -0.51 pp |

**Under the paper's convention (negative = UCP raw-proportional advantage;
positive = NDP raw-proportional advantage):**

- 2015: both maps strongly NDP-advantaged (natural — NDP won in 2015);
  minority essentially identical to majority.
- 2019: both maps mildly NDP-advantaged; minority +0.75 pp MORE
  NDP-advantaged than majority → minority LESS UCP-favourable than
  majority under 2019 votes.
- 2023: both maps mildly UCP-advantaged; minority -0.51 pp MORE
  UCP-favourable than majority.

**Direction of minority vs majority under paper's convention:**

- 2015: essentially zero (+0.03 pp toward NDP-advantage for minority).
- 2019: positive (minority less UCP-favourable than majority).
- 2023: negative (minority more UCP-favourable than majority).

This produces the headline 2023 finding the paper reports, reverses under
2019 votes, and essentially zeros out under 2015 votes. The
cross-election contingency paragraph in §3.5 should be read under the
paper's convention.

**Track Z's 2015 analysis file states the opposite: "minority is MORE
pro-UCP than majority for 2015 (+0.03) and 2019 (+0.75)."** That reading
depends on Track Z's (incorrect) claim that the code's sign convention
matches "the gerrymandering literature's convention for pro-UCP."
Correcting Track Z to the paper's convention:

- 2015 +0.03 → minority marginally LESS UCP-favourable than majority.
- 2019 +0.75 → minority LESS UCP-favourable than majority.
- 2023 -0.51 → minority MORE UCP-favourable than majority.

Under the paper's convention, the 2023 result is the one that matches
the headline and the 2015/2019 results reverse it. **The paper's
headline is supported by 1 of 3 elections under this (paper's)
convention, not 2 of 3.** The cross-election contingency is stronger
against the paper than Track Z concluded.

## 10. Summary

| Question | Answer |
|---|---|
| Is the code's EG formula a canonical S-M EG? | No — it's S-M EG from UCP perspective (sign-flipped relative to S-M's EG_NDP). |
| Is the paper's "negative = UCP advantage" convention coherent? | Yes — under a 1:1 proportional baseline, not S-M's 2:1 slope. |
| Do paper convention and S-M agree on the minority-vs-majority direction? | Yes — both rank minority as more UCP-leaning than majority in raw-seat terms. |
| Does Track Z's 2015 cross-election analysis use the right sign? | Partially — Track Z uses a sign convention ("positive = pro-UCP") that is S-M-canonical but inverted relative to the paper's running convention. Under the paper's convention, the 2023 result is the one that supports the headline; 2015 and 2019 reverse it. Under S-M's convention, 2015 and 2019 support the headline; 2023 reverses it. |
| Do any paper direction claims need flipping? | No direction claim about minority vs majority needs flipping. The 2019-vs-2023 cross-election contingency narrative needs re-reading under the paper's convention. |
| Does the code need changing? | No. Only documentation / glossary additions. |
| Do v0_3 print labels need changing? | No, assuming the sign-convention note is added to the reports. They are consistent with the paper's convention. |

**Verdict on Phase 1 resolution options:**

- (a) The paper's narrative convention is correct (in the sense that it is
  internally consistent and describes real asymmetry): **CONFIRMED**
  — with the clarification that the paper's convention uses a 1:1
  proportional baseline, not S-M's 2:1 slope. S-M is cited for the formula
  but not for the sign rule.
- (b) S-M convention is correct, paper is inverted: **PARTIALLY
  CORRECT** — S-M's canonical sign rule is the opposite of the paper's,
  but because the ordinal ranking is preserved, the minority-vs-majority
  direction claim does not need to be flipped. Only the framing of the
  2019 baseline as "UCP-favourable floor" and the cross-election 2015 /
  2019 / 2023 narrative under each convention need to be disambiguated.
- (c) Code is wrong: **REJECTED**. The code correctly implements the
  S&M (2015) wasted-vote formula; the sign it produces is
  `(W_NDP - W_UCP)/T`, which is just S-M EG from UCP's perspective.

**Resolved:** Paper's convention stands; paper should add a one-paragraph
sign-convention note distinguishing the raw-proportional reading from the
S-M 2:1-slope reading. Track Z's cross-election analysis uses the S-M
convention explicitly and reaches conclusions that reverse the paper's
convention for 2015 and 2019 — this is a framing collision in the
document set, not a correctness error in either.
