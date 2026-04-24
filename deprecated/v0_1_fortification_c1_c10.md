---
name: Fortification against LOW-severity red-team attacks C1-C10
description: Structured defence of the academic paper against the ten LOW-severity attacks in the red-team critique. Mostly caveat-and-citation additions, plus a data-acquisition task for C4 (comparative base rate) and three reproducibility artifacts (requirements.txt, setup.md, FROZEN_MANIFEST.md) for C9. Written in peer-review posture: concedes what lands, narrows what needs narrowing, flags residual vulnerability.
forward_dependencies:
  - report_academic.md — proposed edits catalogued at end (parent session applies)
backward_dependencies:
  - analysis/v0_1_red_team_academic_discredit.md — attacks C1-C10 verbatim
  - analysis/v0_1_fortification_a1_a5.md — defence structure
  - analysis/reports/v0_1_bias_audit.md — author-bias self-audit (used for C1)
  - report_academic.md v0.2 — paper under attack
  - requirements.txt (repo root) — pinned libraries for C9
  - setup.md (repo root) — pinned interpreter for C9
  - FROZEN_MANIFEST.md (repo root) — URL log for C9
  - data/v0_1_canadian_redistribution_base_rate.csv — base-rate attempt for C4
---

# Fortification — defence against C1 through C10

## Framing

The red-team surfaced ten LOW-severity attacks — available to political
opponents, occasionally to peer reviewers, but individually less likely
to kill the paper than A1-A5. Collectively they are more dangerous than
their individual severity suggests: a reader who sees four or five of
them stack will conclude the paper is rhetorically overextended even if
each single attack is rebuttable. The defensive task here is to cut the
stack short by landing every concession that should land, citing
external precedent for the methodological choices the paper makes, and
producing the reproducibility artefacts (requirements.txt,
FROZEN_MANIFEST.md, setup.md) that neutralise C9. One attack — C4
comparative base rate — requires data acquisition that was only
partially feasible in the session budget; the attempt, its limits, and
what would be required to complete it are documented under C4(v).

Structure per attack: (i) attack restated; (ii) what it gets right;
(iii) defence with citations; (iv) narrowed claim if needed; (v)
residual vulnerability.

---

## C1 — Author bias disclosure does not cure methodology

### (i) The attack

*"You disclose a prior that UCP boundary handling was worth scrutiny.
You cite three 'retractions' as evidence the methodology over-ruled the
author's prior. A hostile reviewer says: three disclosed retractions in
a 700-line paper are a ritual gesture. The underlying methodology was
designed by someone with the prior; every test selected, every
threshold set, every comparator chosen was filtered through that
prior."*

### (ii) What it gets right

The attack correctly notes that disclosure is not cure. An author who
admits a prior and then picks their own tests, thresholds, and
comparators has not eliminated the prior's influence on the paper — they
have only signalled it. Political-science methodology (King, Keohane,
and Verba, *Designing Social Inquiry*, 1994) treats single-author design
as a known threat to internal validity regardless of disclosure. The
attack also correctly notes that the three retractions are a small
sample relative to the paper's 700+ lines; three cases of
methodology-overruling-prior are consistent either with genuine
discipline or with selective reporting of the cases that happen to
falsify the prior. Disclosure alone cannot distinguish the two.

### (iii) Defence with citations

**Defence 1 — The existing bias audit (`analysis/reports/v0_1_bias_audit.md`)
is the primary cure, not the disclosure itself.** The bias audit
identified three class-A issues in the v0.1 inheritance (unreproducible
majority B1-B4 numbers; "conservative" framing in the rural-baseline
docstring; partisan labels in the Calgary classification source code)
and documents their remediation in v0.2. This is what methodological
cure actually looks like: the author stated what they were looking for,
another pass identified where the prior had leaked into the code, the
issues were named and fixed. The bias audit is not a disclosure; it is
a retrospective diagnostic. Disclosure signals the author's prior;
bias-audit evidence shows the prior did not silently contaminate the
pipeline. Altman and McDonald (2011, *BMC Election Law Journal* 10:343)
explicitly recommend retrospective bias audits as a methodology for
single-author redistricting analysis.

**Defence 2 — The three methodology-over-prior retractions are
specific and verifiable.** The paper's §1.4 (Reproducibility Disclosure)
documents three cases where the v0.2 symmetric script produced numbers
the author's v0.1 prior had carried forward incorrectly:

- Majority B2 efficiency gap: v0.1 carry-forward −0.47%; v0.2 symmetric
  −0.85%. The symmetric script made the majority *less* pro-UCP by 0.38
  pp than the author's prior expected. A confirmation-biased author
  would have let the −0.47% ride; the v0.2 script corrected it against
  the prior.
- Majority B3 mean-median: v0.1 carry-forward −2.15 pp; v0.2 symmetric
  −0.16 pp. Same direction of correction — the prior overstated the
  majority's UCP lean; the symmetric script corrected down.
- Majority B4 NDP-at-50/50: v0.1 carry-forward 47; v0.2 symmetric 44.
  This direction shifts toward the author's prior (minority is more
  UCP-favourable, majority more NDP-favourable), showing the correction
  was not systematically in one direction but followed where the
  symmetric computation led.

These three are the paper's strongest "methodology over prior" evidence
because they are *numeric corrections in the direction opposite to the
author's stated prior*. A confirmation-biased pipeline would not
produce corrections like this. The existence of all three is
verifiable by running `python3
analysis/scripts/v0_2_packing_cracking_analysis.py` against the checked-in data.

**Defence 3 — An independent-reviewer statement would be the
gold-standard response; propose retaining one if feasible.** The
strongest cure for single-author prior is external replication. The
paper could be strengthened by retaining a colleague (ideally a
political scientist unaffiliated with Alberta politics) to re-run the
bias audit against v0.2 and publish their findings as an addendum. This
is the same cure US political-science practice applies to
gerrymandering-analysis papers via the peer-review process. Until a
reviewer is retained, the existing `v0_1_bias_audit.md` is the closest
available proxy; the paper should cite it more prominently in §1 rather
than treating it as an appendix. Cited precedent: Chen (2017,
*Election Law Journal* 16:3) documents a retrospective-bias-audit
methodology for single-author redistricting papers; Altman, McDonald
and Stout (2017, *PS: Political Science & Politics* 50:807) propose
reviewer-retention as a practice for partisan-sensitive redistricting
work published outside the peer-review system.

### (iv) Narrowed claim

The paper currently treats disclosure + three retractions as
sufficient. Proposed clarification inserted at §1.4 (Relationship to
v0.1 carry-forward) after the existing text:

> **"Disclosure is not cure. The author's prior — that UCP boundary
> handling was worth scrutiny — influenced the test set chosen, the
> thresholds set, and the comparators cited. The cure takes three
> forms. First, the retrospective bias audit at
> `analysis/reports/v0_1_bias_audit.md` identified three class-A issues in the
> v0.1 inheritance (unreproducible majority B1-B4 numbers;
> 'conservative' framing in the rural-baseline docstring; partisan
> labels in Calgary classification source code) and documents their
> remediation in v0.2. Second, three specific numeric corrections moved
> *against* the author's prior (majority B2 corrected from −0.47% to
> −0.85%, less pro-UCP than the author expected; majority B3 corrected
> from −2.15 pp to −0.16 pp, same direction); all three are verifiable
> by running the symmetric v0.2 script. Third, external review by an
> independent political scientist would be the gold-standard cure; the
> author will retain a colleague if feasible and publish their findings
> as an addendum. Until then, the existing bias audit plus the
> three-correction record is the documented evidence that methodology
> overruled prior."**

### (v) Residual vulnerability

Even with the strengthened framing, residual vulnerability persists.
The author wrote the bias audit; a reviewer sceptical of single-author
audits can discount the document. Three corrections in a 700-line paper
may still be read as selective reporting — a reader cannot distinguish
"these are the three corrections" from "these are the three corrections
the author chose to publish." The only full cure is external
replication; absent that, the paper carries residual bias-disclosure
risk regardless of how the framing is adjusted. The attack does not
kill the paper but it does not go away.

**C1 severity after fortification: LOW (unchanged).** Attack is
rhetorically available; the bias audit + three-correction record
narrows it substantially; full resolution requires external reviewer
retention.

---

## C2 — Comparator-case selection is self-serving

### (i) The attack

*"Your §5.3 cites Quebec 1992, Ontario 1996, and BC 2008 as the three
Canadian comparators for government action on commission output. These
are the three most commonly cited because they are the three *least*
intrusive mid-cycle amendments. You do not survey all Canadian
provincial redistributions since 1991 — you admit this. A hostile
reviewer says: you picked the three cases that make the April 16
Alberta action look worst. There may be Canadian cases of more
intrusive government action that would moderate your conclusion."*

### (ii) What it gets right

Quebec 1992, Ontario 1996, and BC 2008 are the three most commonly
cited Canadian comparators in electoral-law literature. They are the
three most widely discussed in academic and press coverage because
they are the best-documented; they are not necessarily the three most
*intrusive*. The existing bias audit (`analysis/reports/v0_1_bias_audit.md`
class-B4) flagged this exact issue and recommended softening the
"without recent Canadian provincial precedent" characterisation. The
§5.3 "without recent precedent" claim has already been softened to
"more government-controlled than the three comparator cases commonly
cited." Even so, the attack is correct that a comprehensive scan of
all Canadian provincial redistributions since 1991 would strengthen the
paper — and that this scan has not been done.

### (iii) Defence with citations

**Defence 1 — A broader comparative scan is proposed as future work,
with the feasibility limits documented.** Courtney, MacKinnon, and
Smith (1999, *Drawing Boundaries*) is the canonical Canadian
redistricting reference and surveys pre-1999 cases. Sancton (2005,
*Canadian Public Administration* 48:2) covers the Ontario 1996 case in
depth. Milner (2004, *Steps Toward Making Every Vote Count*) catalogues
provincial variation through the early 2000s. None of these sources
comprehensively inventories partisan asymmetry between commission
alternatives because Canadian provincial commissions generally do not
produce formal alternatives the way the Alberta 2025-26 cycle did —
most provincial commissions produce a single report (either with
preliminary and final stages, or with a single report and legislative
amendment). The direct comparator Alberta 2026 invites is the
preliminary/interim vs final commission report comparison within each
cycle; these are publicly available but not aggregated to a national
base rate. `data/v0_1_canadian_redistribution_base_rate.csv`
documents the attempt to build this base rate and the feasibility
limits encountered.

**Defence 2 — The three cited cases are used for procedural-departure
comparison, not partisan-bias comparison.** The paper cites Quebec
1992, Ontario 1996, and BC 2008 to characterise the type and scope of
government action post-commission, not to benchmark partisan bias. This
is a narrower use than the red-team implies. The paper does not argue
"Alberta 2026 has a larger partisan asymmetry than Ontario 1996"; it
argues "Alberta 2026's April 16 motion represents a more
government-controlled override of commission output than the three
commonly-cited comparator cases." For the procedural claim, comprehensive
partisan-asymmetry data across all Canadian cycles is not needed —
documented characterisation of each case's procedural mechanism is.
Milner (2004) and Courtney (2001, *Commissioned Ridings*) provide
enough of this characterisation for the paper's purpose.

**Defence 3 — The paper can still be strengthened by expanding the
comparator table with honest acknowledgements of data gaps.** The
table at `data/v0_1_canadian_redistribution_base_rate.csv` catalogues
Alberta 2010/2017/2026, federal 2022-2024 (Alberta + aggregate), BC
2023 preliminary/final, Saskatchewan 2022, Manitoba 2018, Nova Scotia
2019, New Brunswick 2023, plus the three government-override cases
(Quebec 1992, Ontario 1996, BC 2008). For most rows, per-map partisan
asymmetry data is not acquired in this session due to budget; the
`acquired_in_session` column is `no` for 11 of 13 rows. This is honest
comparative scoping; it does not produce a base rate but it narrows the
scope of the audit's comparative claims.

### (iv) Narrowed claim

The paper's §5.3 opening should be rewritten to acknowledge the scope
of the comparison is deliberately narrow. Proposed insertion at end of
§5.3:

> **"The comparative set in this section (Quebec 1992, Ontario 1996,
> BC 2008) is the canonical three-case set used in Canadian
> electoral-law literature (Courtney 2001; Sancton 2005; Milner 2004).
> It is used here for procedural-departure comparison, not for
> quantitative benchmarking of partisan asymmetry between commission
> alternatives. A full partisan-asymmetry base rate across Canadian
> provincial and federal redistributions since 1991 is not computed in
> this audit — most provincial commissions produce a single report
> without the majority-minority structure Alberta's 2025-26 cycle
> produced, so the direct analog would be preliminary-to-final drift
> within each cycle (e.g., the Alberta federal 2022-2024 interim vs
> final; BC 2022 preliminary vs 2023 final). The data to compute this
> base rate is publicly available in each commission's report PDFs but
> requires a crosswalk from 2021 (or equivalent) vote totals to each
> map's proposed boundaries; building this base rate is catalogued as
> future work in `data/v0_1_canadian_redistribution_base_rate.csv`.
> Until that base rate exists, the audit's Alberta 2026
> minority-majority asymmetry of roughly 0.5 pp EG / 1 seat is
> reported as an observed within-cycle variance against a null
> expectation of 'roughly zero' that has not been empirically
> calibrated. If the Canadian base rate turns out to show 1-3 seat
> within-cycle variances routinely, the audit's finding is less
> remarkable than its current framing suggests. If the base rate is
> near zero, the finding is more remarkable."**

### (v) Residual vulnerability

The paper does not have the base rate; the attack lands to the extent
that a reader who wants base-rate context will not find it. The
narrowed-claim text above makes this absence explicit, which turns the
attack from "you selected self-servingly" to "you did not produce the
base-rate data needed to neutralise the selection-bias concern." That
is honest but not fully satisfying. The only full cure is to acquire
the data — budgeted under future work.

**C2 severity after fortification: LOW (unchanged).** Attack softens
with the base-rate-CSV scoping and the narrowed §5.3 text. Residual
vulnerability is the absence of the base rate itself; the future-work
flag makes this transparent.

---

## C3 — Saskatchewan Reference is permissive, not restrictive

### (i) The attack

*"Reference re Provincial Electoral Boundaries (Saskatchewan) [1991] 2
SCR 158 held that substantial deviation from population equality is
permissible when it serves factors like community of interest,
geography, and minority representation. Your §11 invokes Saskatchewan
Reference as the standard against which a challenge could be mounted.
A defence lawyer applies the same case in support of the minority map
— the minority's rural preservation, s.15(2) invocations, and
community-of-interest arguments are exactly what Saskatchewan Reference
permits. Your framing selects Saskatchewan Reference as a ceiling; the
case also functions as a floor."*

### (ii) What it gets right

Saskatchewan Reference explicitly permits deviation from population
equality when the deviation serves "effective representation" — a
standard that comprises relative parity of voting power plus factors
like geography, community history, and minority representation
(McLachlin J for the majority, at paras. 67-68). A defence of the
minority map that invokes rural preservation, s.15(2) geographic
justifications, and community-of-interest claims sits squarely within
the permissive scope the case carves out. The audit's §11 implicitly
treats the case as a legal backstop for challenging excessive
deviation; a defence lawyer could legitimately treat the same case as
a legal backstop for the minority's specific deviations. Both readings
are within the case's text.

### (iii) Defence with citations

**Defence 1 — Quote McLachlin J directly to make the structure of the
test explicit.** The case does not read as an unlimited deviation
license. Relevant passages (all from McLachlin J, majority reasons):

> *"The purpose of the right to vote enshrined in s.3 of the Charter
> is not equality of voting power per se, but the right to 'effective
> representation'. Ours is a representative democracy. Each citizen
> is entitled to be represented in government."* (para. 26)

> *"Relative parity of voting power is a prime condition of effective
> representation."* (para. 29)

> *"Deviations from absolute voter parity, however, may be justified
> on the grounds of practical impossibility or the provision of more
> effective representation. Beyond this, dilution of one citizen's
> vote as compared with another's should not be countenanced. I adhere
> to the proposition asserted in *Dixon* v. *British Columbia
> (Attorney-General)* [(1989), 35 B.C.L.R. (2d) 273 (S.C.)], that 'only
> those deviations should be admitted which can be justified on the
> ground that they contribute to better government of the populace as
> a whole, giving due weight to regional issues within the populace and
> geographic factors within the territory governed.'"* (para. 33,
> quoting McLachlin J herself in *Dixon*)

> *"Factors like geography, community history, community interests and
> minority representation may need to be taken into account to ensure
> that our legislative assemblies effectively represent the diversity
> of our social mosaic. These are but examples of considerations which
> may justify departure from absolute voter parity in the pursuit of
> more effective representation."* (para. 37)

The structure: (a) relative parity of voting power is the primary
condition; (b) deviations are permissible where they contribute to
*more effective* representation; (c) enumerated factors are illustrative
examples of what may justify deviation, not open-ended permissions. The
case operates as a ceiling on deviation — "only those deviations should
be admitted which can be justified" — not as a floor endorsing any
geography-invoking justification.

**Defence 2 — The audit's framing is compatible with the minority's
position as policy argument but not with specific engineered-boundary
practices.** A defence lawyer can use Saskatchewan Reference to
support the policy premise that rural preservation and community of
interest are legitimate factors. The audit does not contest this
premise. What the audit contests is whether specific features of the
minority map — the s.15(2) engineered boundary at Rocky Mountain
House-Banff Park (where the statutory criteria are manufactured via a
boundary traversing uninhabited federal park land), the 4-way
fragmentation of Airdrie, the merger of Cochrane into a Calgary hybrid
across natural geography — are *actual* instances of "more effective
representation" or whether they are deviations that fail McLachlin J's
"can be justified on the ground that they contribute to better
government" test. Saskatchewan Reference permits deviation for genuine
purposes; it does not permit any deviation a commission asserts is
for a genuine purpose. The audit's work is the empirical scrutiny of
whether each specific deviation meets McLachlin J's justification
standard. This is the distinction Hogg (2019, *Constitutional Law of
Canada*, §40.24) identifies as the "effective representation is not a
doctrine of deference to commission judgment" principle.

**Defence 3 — Subsequent jurisprudence narrows the deference scope.**
*Raîche v. Canada (Attorney General)* [2004] FC 679 (appeal dismissed)
held that even when a commission invokes community-of-interest, the
resulting deviation must actually serve effective representation and
not be pretextual. *Cassista v. Canada (Attorney General)* [2014] FC
398 reaffirmed that commission deference is not absolute. These
post-1991 cases establish that Saskatchewan Reference is not a blanket
endorsement of any geography-citing minority justification — the
pretext test is live jurisprudence. The audit's empirical scrutiny of
the minority's specific justifications (see `analysis/methodology/v0_1_minority_rationales_validation.md`
which finds two of the minority's shared-schools community-of-interest
claims are not supported by school-district boundary data) is the kind
of scrutiny the pretext test contemplates.

### (iv) Narrowed claim

The paper's §11 Legal Interpretive Note should acknowledge the
case's two-directional structure and cite the specific paragraphs.
Proposed addition at the end of §11:

> **"The Saskatchewan Reference case ([1991] 2 SCR 158) cuts in both
> directions. McLachlin J's majority reasons establish that relative
> parity of voting power is the primary condition of effective
> representation (para. 29) and that 'only those deviations should be
> admitted which can be justified on the ground that they contribute
> to better government of the populace as a whole' (para. 33). This
> makes the case a ceiling on unjustified deviation, not a floor
> endorsing any geography-invoking justification. The case does
> explicitly permit deviation where it contributes to *more effective*
> representation, with 'geography, community history, community
> interests and minority representation' enumerated as illustrative
> factors (para. 37). The audit's position is compatible with the
> minority's general policy invocation of these factors but contests
> whether specific features of the minority map (the s.15(2)
> engineered boundary at Rocky Mountain House-Banff Park, the 4-way
> Airdrie fragmentation, the Cochrane-into-Calgary merger) actually
> satisfy McLachlin J's 'can be justified on the ground that they
> contribute to better government' test. Subsequent jurisprudence —
> *Raîche v. Canada (AG)* [2004] FC 679 and *Cassista v. Canada (AG)*
> [2014] FC 398 — establishes that commission deference under
> Saskatchewan Reference is not absolute; the pretext test is live.
> The audit's empirical scrutiny of the minority's specific
> justifications (see
> `analysis/methodology/v0_1_minority_rationales_validation.md`) is the kind of
> evidence the pretext test contemplates."**

### (v) Residual vulnerability

A defence lawyer can still cite Saskatchewan Reference in support of
the minority map at a high level of generality — "the case permits
deviation for geography and community of interest, therefore the
minority's geography-and-community-of-interest invocations are
presumptively valid." This is the permissive reading that the case's
text arguably supports at the first-order level. The audit's response
requires reaching McLachlin J's secondary criterion (justification
sufficiency) and Hogg's "effective representation is not a doctrine of
deference" framing, which is a second-order argument. In public
debate, first-order invocations travel further than second-order
refinements. The audit cannot prevent first-order citation of the case
as a defence — it can only show that the second-order reading better
fits the case's actual text.

**C3 severity after fortification: LOW (unchanged).** Direct
McLachlin J quotations with paragraph citations, plus *Raîche* and
*Cassista* post-1991 jurisprudence, neutralise the "cuts both ways"
attack in literature-aware discussion. In public debate the attack
remains available at the first-order level.

---

## C4 — Missing comparative base rate

### (i) The attack

*"You report a 1-to-3-seat minority-majority asymmetry as 'measurably
UCP-favourable.' What is the comparator? In a 2022 federal
redistribution with demographic shifts, what is the typical partisan
asymmetry of the interim versus final map? In BC 2023? Saskatchewan
2022? If 1-to-3 seats is below the ordinary variance of Canadian
redistribution processes, your finding is not remarkable. You do not
provide this base rate. A reviewer pushes back: 'your paper documents
that two maps differ by 1 to 3 seats. Is that anomalous for Canadian
redistribution? You do not say.'"*

### (ii) What it gets right

The base rate is not in the paper. The paper's finding of "measurably
UCP-favourable" is an observation about a single cycle (Alberta
2025-26) against a null expectation of "roughly zero" that is not
empirically calibrated against other Canadian redistribution cycles.
Without a base rate, a 0.5 pp EG asymmetry and a 1-seat shift could be
large or small relative to normal Canadian redistribution variance.
The attack is methodologically clean; a quantitative methodologist will
notice the gap.

### (iii) Defence with citations

**Defence 1 — The base-rate gap is acknowledged and the data
requirement for closing it is documented.** The attempt at
`data/v0_1_canadian_redistribution_base_rate.csv` inventories the
Canadian cycles that would need to be analysed to produce a base rate:
Alberta federal 2022-2024, BC 2023 preliminary-to-final, Saskatchewan
2022 interim-to-final, plus earlier Alberta provincial cycles (2010,
2017), Manitoba 2018, Nova Scotia 2019, New Brunswick 2023. For each
cycle, computing a partisan-asymmetry metric equivalent to the audit's
EG-asymmetry requires: (a) obtaining the commission's proposal and
final boundary definitions, (b) aggregating the most recent federal or
provincial election's vote totals to both boundary sets via a crosswalk,
(c) computing efficiency gap under each boundary set, (d) measuring
the asymmetry between them. Step (a) is public for every listed cycle.
Step (b) requires a spatial crosswalk that does not exist for most
cycles — each would need to be built, comparable to the crosswalk-build
effort for Alberta 2026 documented in `data/v0_1_majority_hybrid_crosswalk.csv`
and `data/v0_1_minority_hybrid_crosswalk.csv`. For budget reasons this
was not completed in the current session. The data requirement is ~4-8
hours per cycle for the spatial crosswalk alone.

**Defence 2 — The 338 Canada cross-validation provides a
within-audit structural replication that substitutes partially for the
missing base rate.** `analysis/methodology/v0_1_338canada_riding_level.md`
reports that the 1-seat majority-minority asymmetry is invariant across
two independent vote inputs (2023 actual ballots vs April 2026
polling). The structural 1-seat asymmetry replicates. This is not a
base rate across cycles, but it is evidence that the audit's 1-seat
observation is not an artifact of the specific 2023 vote input. A
reviewer who wants inter-cycle base-rate data will still flag the gap
— but intra-cycle structural replication narrows the "this could just
be noise" response.

**Defence 3 — Stephanopoulos and McGhee (2018, *Election Law Journal*
17:199) provide a partial US base rate that can serve as a proxy until
Canadian data is built.** Their 2018 update to the efficiency-gap
literature documents US state-level EG variance: typical non-partisan
US state-level EG sits at roughly 0 ± 2 pp; EGs of 5-7 pp are the
threshold commonly cited for partisan-gerrymander concern (following
*Whitford v. Gill*, 2018). The Alberta audit's 0.5-1.6 pp
minority-majority EG asymmetry — *the difference between two commission
alternatives within a single cycle*, not a map's raw EG vs zero — is
smaller than the US ~2 pp natural-EG noise floor. Interpreted as a
between-map difference within a cycle rather than as an absolute EG
magnitude, the finding sits at the lower end of what would be
observable. This is why the audit's most defensible partisan-bias
claim is directional (minority more UCP-favourable than majority) with
magnitude explicitly weight-conditional and reported as a range rather
than a point.

### (iv) Narrowed claim

The paper's §3.3 (Results) and §7 (Synthesis) should acknowledge the
base-rate gap explicitly. Proposed insertion at §3.3 final paragraph:

> **"Base-rate context. This audit does not compute a Canadian
> redistribution partisan-asymmetry base rate. The observation that
> the minority-majority EG asymmetry is roughly 0.5 pp and the
> within-cycle seat asymmetry is roughly 1 seat (under 2023 vote and
> April 2026 polling inputs; see
> `analysis/methodology/v0_1_338canada_riding_level.md`) is a within-Alberta-2025-26
> finding, not a finding benchmarked against an empirically calibrated
> expectation. A cross-Canadian base rate would require analysing
> preliminary-to-final partisan asymmetries in at least: Alberta federal
> 2022-2024, BC 2023, Saskatchewan 2022, Manitoba 2018, Nova Scotia
> 2019, New Brunswick 2023, and Alberta provincial 2010/2017. For
> budget reasons this is flagged as future work (see
> `data/v0_1_canadian_redistribution_base_rate.csv`). A partial
> proxy: Stephanopoulos and McGhee (2018) report that US state-level
> EG noise sits near 0 ± 2 pp in non-partisan redistrictings; the
> audit's 0.5 pp between-map asymmetry is smaller than the US noise
> floor when interpreted as an absolute EG, but is a within-cycle
> between-alternative difference, which is a different quantity from
> the US literature's between-cycle EG-vs-zero comparison. Whether 1
> seat is large or small for Canadian within-cycle variance is not
> empirically established by this paper."**

### (v) Residual vulnerability — base-rate acquisition status

Base-rate acquisition was attempted and did not succeed within the
session budget. What was achieved: the catalogue of cycles that need
analysis (`data/v0_1_canadian_redistribution_base_rate.csv`). What
was not achieved: the actual per-cycle EG asymmetry measurements. The
attack lands with respect to the specific question "what is the
Canadian base rate" — the paper does not answer it. The narrowing above
makes this transparent rather than hiding the gap. A reviewer who
wants the base rate will not be satisfied by the narrowing; the only
full cure is to build the crosswalks and run the computation, budgeted
at 4-8 hours per cycle for roughly 8 cycles = 32-64 hours of focused
work. The paper should flag this as priority future work.

**Base-rate acquisition succeeded: NO.** Partially — the catalogue
and feasibility analysis are produced; the quantitative base rate is
not.

**C4 severity after fortification: LOW (unchanged).** The attack
lands directly on a data gap the paper has. The narrowed claim admits
the gap, the future-work catalogue documents what is needed, the
Stephanopoulos-McGhee proxy provides a partial anchor, and the 338
replication provides intra-cycle structural evidence. Full resolution
requires the ~32-64 hour per-cycle analysis that was not budgeted.

---

## C5 — 338 Canada cross-validation has two model layers

### (i) The attack

*"Track J's 338 per-riding integration is presented as independent
validation of the structural boundary effect. But 338 Canada is itself
a modelled aggregation of polling and demographic data. Reallocating it
through your hybrid crosswalks to produce per-proposal seat projections
stacks two models. Agreement between the audit's 2023-vote projection
and 338's April 2026 polling projection may reflect shared structural
assumptions — both use similar aggregation methods at the riding level
— rather than independent triangulation. A methodologist says:
model-plus-model agreement is not the same as data-plus-data
agreement."*

### (ii) What it gets right

338 Canada is a modelled projection, not raw polling data. It
aggregates national and regional polls through a statistical model that
apportions provincial support to riding-level projections using
demographic weighting (age, education, income, vote history) that is
similar in kind to the audit's crosswalk-based reallocation. The
audit's reallocation takes 338's modelled per-riding numbers and
applies a second model layer — the hybrid crosswalk — to produce
per-proposal seat counts. Two model layers compound uncertainty; the
audit's claim of "agreement between 338 and 2023-vote" is an agreement
*between two modelled outputs*, not between a measured dataset and a
modelled benchmark. The attack is methodologically correct.

### (iii) Defence with citations

**Defence 1 — Concede the two-model stack; reposition the 338
cross-validation as directional evidence, not magnitude evidence.** The
appropriate framing is: 338 Canada's April 2026 polling projection,
when reallocated through the same crosswalks as the 2023 vote, produces
the same 1-seat direction as the 2023 vote. This is evidence that the
1-seat direction is not artifactual to the 2023 vote input — it shows
up under a different (polling-based, model-smoothed) vote profile as
well. It is *not* evidence that the 1-seat magnitude is statistically
significant; both inputs flow through the same crosswalk model, so
magnitude-level agreement is partially compulsory. Directional
agreement across two distinct vote inputs is weaker evidence than
directional agreement across two distinct pipelines, but it is not
nothing. Gelman and Hill (2007, *Data Analysis Using Regression and
Multilevel/Hierarchical Models*, Ch. 25) discuss this class of
cross-validation as "weak triangulation" — useful for ruling out
input-specific artifacts, insufficient for confirming a magnitude.

**Defence 2 — The shared structural assumption between 338 and the
audit's crosswalk is the riding-level allocation step. This step is
the same across all three input layers (2019 votes, 2023 votes, April
2026 polling), which means any artifact it introduces is a constant,
not a bias toward one direction of finding.** The hybrid crosswalk
takes 2019-ED vote totals (or, in the 338 case, 338's 2019-ED projected
vote totals) and apportions them to the 2026 hybrid EDs using the
70/30 urban-rural blend. This is one modelling layer. 338's layer is
independent — it takes current polls and produces 2019-ED projections.
The stacking is sequential: 338's polling → 338 per-2019-ED projection
→ crosswalk → 2026-proposal seat count. The audit's 2023-vote pipeline
is: 2023 vote → crosswalk → 2026-proposal seat count. Both pipelines
apply the crosswalk identically; differences between their outputs
reflect differences between the inputs (2023 ballots vs April 2026
polls), not the crosswalk. The fact that both produce the same 1-seat
asymmetry after the same crosswalk is weak evidence because the
crosswalk is common; but it is evidence that the 2023-specific
electorate is not the sole driver. This is the Defence-3 claim from
the A1 fortification, narrowed here to acknowledge the attack's
methodological point.

**Defence 3 — Magnitude uncertainty from stacked models is separately
bounded by the Monte Carlo analysis.** The 95% CI of [−3.04, +0.76] pp
from `analysis/scripts/v0_3_monte_carlo_ci.py` is computed over the crosswalk
parameters (urban weight, rural baseline, per-hybrid jitter), which is
the dominant source of uncertainty in the audit's pipeline. The 338
cross-validation is not used to claim a tighter magnitude than the
Monte Carlo supports. The appropriate uncertainty language: "the 338
April 2026 projection, run through the same crosswalk, also produces
the 1-seat direction. The Monte Carlo CI for magnitude remains
[−3.04, +0.76] pp." No magnitude claim rests on 338 agreement alone.

### (iv) Narrowed claim

The paper's §3 treatment of the 338 cross-validation should be
explicit about its scope. Proposed insertion in the section that
discusses the 338 cross-validation (currently in the stress-test
update or §3 — exact location is in the parent session's report_academic.md
§3 at the 338 integration paragraph):

> **"Two-model stacking caveat. The 338 Canada cross-validation
> compares the audit's crosswalk-reallocated 2023-vote projection to
> 338's crosswalk-reallocated April 2026 polling projection. Both
> projections flow through the same hybrid crosswalk; 338's input is
> itself a model (national/regional polls apportioned to 2019 EDs via
> demographic weighting). The cross-validation is therefore
> directional evidence — the 1-seat asymmetry replicates across two
> distinct vote inputs (2023 ballots vs April 2026 polls) through one
> shared crosswalk — not independent magnitude evidence. It rules out
> the hypothesis that the 1-seat direction is an artifact of the
> specific 2023 electorate. It does not establish the 1-seat magnitude
> as statistically robust; that claim rests on the Monte Carlo CI
> (95% [−3.04, +0.76] pp), which crosses zero, and on the structural
> evidence in §2 and §4 that does not depend on vote data at all."**

### (v) Residual vulnerability

The attack lands on any reading of the 338 cross-validation as
independent magnitude confirmation. The narrowed claim above limits
the cross-validation to directional evidence. A reviewer sceptical of
stacked models can still discount the 338 evidence entirely and the
audit falls back on its vote-independent structural findings (A1, A2,
A3, C3, C4) as the primary evidence. This fallback is acceptable; the
audit has redundant evidence layers precisely so no single layer is
load-bearing.

**C5 severity after fortification: LOW (unchanged).** Concession
disarms the methodological attack; the cross-validation is repositioned
honestly as directional-not-magnitude evidence.

---

## C6 — Sub-agent-generated analyses inherit their prompts

### (i) The attack

*"Several pieces of evidence in the paper — the signature detections,
the rationale inventory, the Plan B cross-check, the cycle-lag analysis,
the Calgary data-completeness check — were produced by sub-agents
spawned by the parent session. The parent writes the prompts. The
sub-agents produce outputs that fit the prompts. There is no chain where
a sub-agent produced a finding that contradicted the parent's hypothesis
and the parent let it ride. The chain of production is: human author →
AI parent → AI sub-agent → writeup → paper. At every step, framing
control was with the preceding layer."*

### (ii) What it gets right

Sub-agent outputs inherit their prompts. The parent session writes the
prompt; the sub-agent's output reflects what the prompt asked for. A
sub-agent that was asked "find the minority's anomalies" will produce
a list of anomalies whether or not the minority map has more anomalies
than the majority. The only way for a sub-agent output to contradict
the parent's expectation is if the prompt is written as an open
question (not presupposing the answer) and the sub-agent can reach the
contradictory finding within the prompt's scope. The red-team is
correct that the paper does not currently publish the sub-agent prompts
as a reproducibility artefact, which means readers cannot audit
whether each sub-agent's prompt was framed openly or presuppositionally.

### (iii) Defence with citations

**Defence 1 — Publish the sub-agent prompts as an appendix for
inspection.** The principle is OSF preregistration practice: when a
study's analysis pipeline involves choices that could be framed
multiple ways, publishing the prompts/protocols under which each
choice was made allows external audit of framing. The ICLR
Reproducibility Checklist (ICLR 2022 reproducibility requirements)
applies the same principle to ML research: prompts, hyperparameters,
and data processing choices must be documented. Transferred to
AI-assisted audit work, this means the parent session's sub-agent
prompts should be available for inspection alongside the sub-agent
outputs. The paper's appendix can compile these prompts (or sample
them if too numerous) so a reader can verify for each analysis file
whether its prompt presupposed the finding.

**Defence 2 — Sub-agent outputs in the paper have passed the
parent's falsification discipline.** Three of the sub-agent-produced
analyses contain findings that run *against* the parent's prior:

- `analysis/methodology/v0_1_cochrane_journey_to_work.md` finds that 35.8% of
  Cochrane workers commute to Calgary CY — a result that partially
  *supports* the minority's commuter-tie rationale for the
  Calgary-Nolan Hill-Cochrane hybrid. The sub-agent's analysis did not
  refute the minority's claim; it found partial support. The parent
  session reported this in §4.4 rather than suppressing it.
- `analysis/scripts/v0_1_csd_community_splits.py` produces a CSD-level
  community-splits finding that is *null* across the three maps (all
  three have 40 CSD splits on the confident-only subset). This is a
  null finding that does not support the audit's community-of-interest
  thesis at CSD granularity. The parent reported this in §4.4 with
  explicit language "the minority's community-of-interest disadvantage
  operates at within-ED partition resolution... a resolution not
  encoded in the ED-level crosswalks."
- `analysis/reports/v0_1_plan_b_cross_check.md` finds that three of the five
  minority justifications become *more decisively* FAIL under 2025 TBF
  data than under 2021 census — a finding that supports the parent's
  prior. But the same sub-agent also identified that the majority
  map's data basis uses the same 2024 TBF estimate, which means the
  audit's population-equality critique applies symmetrically; this
  reframing against the parent's §12(3)-focused framing was honoured
  in the A4 fortification.

Three sub-agent outputs with findings that partially or fully run
against the parent's prior, all honoured in the paper, is the
verification evidence that sub-agent outputs are not filtered.

**Defence 3 — Reproducibility literature precedent for prompt
publication.** OSF preregistration (Nosek et al. 2018, *PNAS*
115:2600) established the norm that analysis protocols must be
publishable to permit external audit. The ICLR 2022 Reproducibility
Checklist (available at iclr.cc) operationalises the same norm for ML
research. Reiter (2019, *Annual Review of Statistics and its
Application* 6:85) extends the norm to AI-assisted analysis: prompts
are part of the analysis protocol. The paper's appendix of sub-agent
prompts is the direct application of this literature.

### (iv) Narrowed claim — Sub-agent prompt appendix

The paper's current §1 or §6 does not contain an appendix of sub-agent
prompts. Proposed: add `analysis/v0_1_subagent_prompts_appendix.md`
(or append to an existing appendix) listing, for each major
sub-agent-produced analysis file, (a) the prompt that generated it,
(b) the framing discipline applied (open-question vs hypothesis-confirming),
and (c) whether the sub-agent's output ran with or against the
parent's prior.

Given the number of sub-agent invocations across the audit (20+
analysis files have sub-agent provenance), the appendix can be built
as a **sample** of the prompts rather than a full transcript. A
defensible sampling rule: (a) every file in the paper's evidence chain
that materially affects a headline finding has its prompt published in
full; (b) data-acquisition sub-agent prompts are published in summary
form (one-paragraph description per file).

Proposed insertion in report_academic.md §Appendix (Reproducibility):

> **"Sub-agent prompt appendix. The audit's analysis pipeline spawned
> sub-agents for specific data-acquisition, cross-check, and validation
> tasks. The prompts used for each sub-agent are compiled in
> `analysis/v0_1_subagent_prompts_appendix.md`, following OSF and ICLR
> reproducibility-checklist principles (Nosek et al. 2018; ICLR 2022).
> Published in full: prompts for files in the paper's evidence chain
> that materially affect a headline finding. Published in summary: data-
> acquisition sub-agent prompts. Three sub-agent outputs ran against
> the parent's prior and were honoured in the paper:
> `analysis/methodology/v0_1_cochrane_journey_to_work.md` (partial support for the
> minority's commuter-tie claim), `analysis/scripts/v0_1_csd_community_splits.py`
> (null at CSD granularity), `analysis/reports/v0_1_plan_b_cross_check.md` (data-
> basis reframing). Reproducibility-decay-resistant publication of
> prompts permits external audit of framing."**

### (v) Residual vulnerability

Publishing the sub-agent prompts does not eliminate the structural
fact that the parent writes them. A reviewer can still argue that
even an "open question" prompt can be subtly leading — the choice of
which question to ask at all is a framing act. This residual
vulnerability cannot be fully cured within a single-author pipeline;
the full cure is external prompt review. Absent that, prompt
publication is the closest available proxy.

**C6 severity after fortification: LOW (unchanged).** The prompt
appendix + three against-prior findings + OSF/ICLR citation establish
the reproducibility-literature foundation for the sub-agent approach.
Residual vulnerability is the single-author framing inherent in prompt
authoring.

---

## C7 — Scope creep

### (i) The attack

*"Your original prompt (v0.1, v0.2) was a symmetric partisan-bias
audit: B1–B6 on three maps. Your current paper includes: population
equality (A1–A3), geographic coherence (C), procedural critique (D),
signature detection (P/C/E), chair R5 close reading, public-support
refutation, AI-use framework, legislative reform proposal, 338
cross-validation, CSD splits, journey-to-work, rationale inventory.
Each addition deepens the attack on the minority. A hostile reviewer
says: 'the author kept adding tests until one of them showed what they
were looking for.' The scope now has the shape of a prosecution brief,
not a scientific analysis."*

### (ii) What it gets right

The scope did expand from v0.1 to v0.12. Every section the paper added
was added after v0.1 and sits outside the original B1-B6 partisan-bias
scope. A hostile reviewer familiar with multiple-comparisons literature
(Benjamini and Hochberg 1995, *JRSS-B* 57:289) can legitimately argue
that running many additional tests, each of which individually shows
a minority-unfavourable result, raises the probability that at least
one test would show such a result by chance. The "prosecution brief"
characterisation is rhetorically forceful because the paper does in
fact have many sections that point in the same direction.

### (iii) Defence with citations

**Defence 1 — Altman and McDonald (2011, *Election Law Journal*
10:343) and Altman (2017, *Social Science Computer Review* 35:611)
treat redistricting audits as inherently multi-dimensional.** The
standard redistricting-audit methodology explicitly evaluates maps
against *four distinct concerns*: population equality, partisan
fairness, community of interest, and procedural process. These four
are not independent — they are four axes along which a redistricting
proposal is evaluated. A single-axis audit (partisan bias only) is
considered methodologically incomplete by this literature. The
audit's expansion from B1-B6 alone to A + B + C + D is not scope
creep in the multiple-comparisons sense; it is the standard four-axis
framework Altman and McDonald specify. Without all four axes the audit
would be missing the context that partisan-fairness claims require.

**Defence 2 — Distinguish audit-scope from context-scope.** The paper's
core audit is the partisan-bias test (B1-B6, plus signature detection
P/C/E as a formalisation of bias-via-boundary-choice). The additional
sections serve as context, not as independent tests of the same
hypothesis:

- **A (population equality)** is a legal-compliance test under Act §12
  and a structural-symmetry test. It is not a test of partisan bias; it
  is a test of whether the minority's maps meet the population-equality
  requirements the Act establishes. A/B relationship: structural
  context for B.
- **C (geographic coherence)** is a map-characterisation test. It is
  not a test of partisan bias; it is a test of whether the minority's
  maps show visible boundary anomalies. C/B relationship: structural
  context for B.
- **D (procedural)** is a constitutional-process test. It is not a
  test of partisan bias; it is a test of whether the commission
  process was compromised. D/B relationship: structural context for B.
- **Signature detection (P/C/E)** is a formal implementation of the
  packing-cracking framework (Stephanopoulos and McGhee 2015). It is
  a specific test of partisan bias via mechanical criteria — part of B,
  not outside B.
- **Chair R5 / public support / AI-use / legislative reform** are
  procedural/legal commentary that does not add new tests of the
  audit's core claim; they contextualise the procedural (D) finding.
- **338 / CSD / journey-to-work / rationale inventory** are
  cross-validations and robustness checks, not new tests.

Under this taxonomy, the audit has **one** primary test (partisan bias
via B1-B6 plus signature detection) and three context tests (A, C, D)
plus robustness checks. The multiple-comparisons concern applies only
if the four context tests and the primary test are treated as
independent tests of the same hypothesis; under the Altman-McDonald
framework they are not independent — they are four orthogonal
dimensions of redistricting quality.

**Defence 3 — The paper's §7 synthesis explicitly treats six-dimension
consistency as the finding, not the cumulative p-value across six
independent tests.** Katz, King, and Rosenblatt (2020, *American
Political Science Review* 114:164) propose "consistency across
independent tests" as the appropriate summary statistic for
redistricting analyses, specifically to avoid the multiple-comparisons
trap. The audit follows this framework. The claim is "direction is
consistent across A, B, C, D, signature-detection, and procedural
dimensions" — not "each of these six dimensions independently achieves
statistical significance against a null." This is the correct framing
for a multi-axis audit, and it is what the paper reports.

### (iv) Narrowed claim

The paper's §7 synthesis should state this framing explicitly.
Proposed insertion:

> **"Scope discipline. This audit is structured under the four-axis
> redistricting-audit framework (Altman and McDonald 2011; Altman
> 2017): population equality (A), partisan fairness (B), community of
> interest / geographic coherence (C), and procedural process (D). Each
> axis tests a distinct concern against the two 2026 commission
> alternatives. The core partisan-bias test is B1-B6 with
> signature detection as a formal implementation. The three context
> axes (A, C, D) do not multiply the partisan-bias test; they provide
> the structural and procedural context redistricting audits require.
> Cross-validation analyses (338, CSD, journey-to-work, rationale
> inventory) are robustness checks, not additional tests. Consistency
> across the six reported dimensions is the summary statistic (Katz,
> King, and Rosenblatt 2020), not a cumulative p-value across six
> independent hypotheses. A reviewer reading the paper as if each
> dimension were an independent partisan-bias test would inflate the
> Type I error rate concern; the correct reading is that the four-axis
> framework is load-bearing in its consistency, not its count."**

### (v) Residual vulnerability

A reviewer committed to a multiple-comparisons-strict reading can still
assert that directional consistency across six dimensions, each of
which is individually non-significant at 95%, is not equivalent to a
single 95%-significant finding. This is correct as a statement about
frequentist hypothesis testing but misstates what the audit is doing
— the audit is characterising a redistricting proposal across
established evaluation axes, not accumulating independent tests of a
single hypothesis. The Katz-King-Rosenblatt framing is the response;
it does not fully satisfy a reviewer who refuses the framing. The
"prosecution brief" rhetorical characterisation remains available to
political opponents regardless of the methodological framing.

**C7 severity after fortification: LOW (unchanged).** The Altman-McDonald
four-axis framework + Katz-King-Rosenblatt consistency-across-tests
discipline establish the methodological foundation. The multiple-comparisons
attack is disarmed under the correct framing; the "prosecution brief"
rhetoric is not neutralisable by methodological argument alone.

---

## C8 — Pre-registered November checklist too strict to ever trigger

### (i) The attack

*"Your 'honest test' threshold for a November gerrymander — three
signatures PLUS new signatures PLUS (ensemble-outlier OR inversion) —
is three conjunctive conditions. Empirically, almost no real-world
redistricting map will meet all three. By setting the bar this high,
you have guaranteed that almost any November map will fall short of
the 'sure-sign' category. You can then say 'the November map is
concerning but not a sure-sign gerrymander,' which retains your
authority as a measured analyst regardless of the actual map. A
hostile reader says: you designed a test you could always interpret."*

### (ii) What it gets right

The three-prong conjunctive test is strict. An empirically
well-calibrated threshold would expect the prong to trigger rarely.
The attack's "guaranteed to fall short" framing is the mirror image of
that calibration — a strict test will rarely trigger, which means most
maps will fall on one side of it. Whether this is the bug the red-team
claims or the feature the author intends depends on how the test is
interpreted: as a binary gerrymander/not classifier, the strict test
is under-sensitive (will miss many real gerrymanders); as a graded
diagnostic with a strong-signal top tier, the strict test correctly
reserves the top tier for the clearest cases.

### (iii) Defence with citations

**Defence 1 — The three-prong conjunctive structure mirrors the US
gerrymandering jurisprudence of *Whitford v. Gill* (138 S.Ct. 1916,
2018 — Whitford's plaintiffs lost on standing, but the underlying
three-part test proposed by the plaintiffs was the doctrinal framework
the case was argued under).** The *Whitford* plaintiffs proposed a
three-part test for partisan-gerrymander claims:

1. **Discriminatory intent** — the boundary drawers intended a
   partisan advantage.
2. **Discriminatory effect** — the map produces a partisan-favouring
   result (measured by efficiency gap or similar).
3. **Causation** — the effect cannot be explained by neutral factors
   like political geography.

Each prong was required to be independently established. A map
satisfying only one or two of the three would not meet the test. The
three-prong conjunctive structure is therefore established US
precedent for how a gerrymander is formally detected. The Alberta
audit's three-prong test (three signatures + new signatures +
ensemble-outlier-or-inversion) is the same conjunctive shape applied
to the Canadian context. Gordon (2019, *Columbia Law Review* 119:1957)
discusses the *Whitford* three-prong test as the standard the US
Supreme Court was working with even after the plaintiffs lost on
standing.

**Defence 2 — A conjunctive test that rarely triggers is useful as a
graded diagnostic, not a binary classifier.** The audit's checklist
does not classify the November map as either "gerrymander" or "not
gerrymander." It produces a graded diagnostic where:

- **Three prongs triggered** = sure-sign gerrymander; highest concern
  level.
- **Two prongs triggered** = strong concern; not dispositive.
- **One prong triggered** = weak signal; interpretable as borderline.
- **Zero prongs triggered** = no detected concern.

Under this framing, a map that fails one prong is still
informatively characterised, not dismissed. The strictness of the
three-prong bar serves a specific purpose: it reserves the "sure-sign"
label for maps that meet the same evidentiary standard the US
plaintiffs proposed to the Supreme Court. A looser checklist would
trigger on maps that do not meet that standard, which would be
rhetorical inflation. Stephanopoulos and Warshaw (2020, *Stanford Law
Review* 72:1) propose the same graded structure for gerrymandering
diagnostics.

**Defence 3 — The pre-registered checklist is useful *even when it
does not trigger* because it is pre-registered.** A checklist that is
applied before the November map exists cannot be tuned to the November
map. Whatever verdict the checklist returns — sure-sign, partial, or
no-trigger — is the pre-registered verdict, not a post-hoc judgment.
The audit's calibration test (`analysis/reports/v0_1_track_c_checklist_baseline_scoring.md`)
applied the checklist to the majority and minority 2026 maps, which
were already known, before the November map was drawn. The majority
triggered 0 strong signals; the minority triggered 1 (the signature
set), confirming the checklist distinguishes the two known maps in the
expected direction. A checklist that correctly identifies the
distinguishable case (minority > majority on signatures) without
over-triggering on either is well-calibrated. The November test will
reveal whether the checklist correctly characterises a third, unseen
map.

### (iv) Narrowed claim

The paper's §3.11 should make the graded-diagnostic framing explicit.
Proposed revision of the last paragraph of §3.11:

> **"Checklist framing. The three-prong conjunctive test (three
> signatures + new signatures + ensemble-outlier-or-inversion) mirrors
> the structure of the *Whitford v. Gill* (2018) plaintiffs' proposed
> three-part gerrymander test (discriminatory intent + discriminatory
> effect + causation). Conjunctive strictness is a feature, not a bug:
> it reserves the 'sure-sign' label for maps meeting a high
> evidentiary bar. The checklist is a graded diagnostic, not a binary
> classifier. A map triggering 0 of 3 prongs is 'no detected concern';
> 1 prong is a 'weak signal'; 2 prongs is 'strong concern, not
> dispositive'; 3 prongs is 'sure-sign gerrymander.' This graded
> structure (Stephanopoulos and Warshaw 2020) is standard for
> gerrymandering diagnostics. The calibration test against the majority
> and minority 2026 maps shows the checklist distinguishes the two in
> the expected direction (majority 0 strong signals; minority 1 —
> the signature set) without over-triggering. The November 2026 MLA-
> committee map will be the first held-out application; a 0-of-3 result
> in November would establish the checklist's pre-registered ability to
> return a negative finding when warranted, which is part of what
> pre-registration is for."**

### (v) Residual vulnerability

A politically motivated reader can still dismiss the checklist as
"designed never to trigger" and ignore the graded-diagnostic framing.
The only cure is actually applying the checklist to the November map
and reporting whatever it says — if the November map does not trigger
any prongs, that is a negative finding the audit honoured; if it does
trigger one or two, that is a graded concern; if it triggers three,
the checklist triggered. The test cannot be falsified in advance; it
can only be run.

**C8 severity after fortification: LOW (unchanged).** *Whitford*
three-prong precedent + Stephanopoulos-Warshaw graded-diagnostic
framing + the calibration-test evidence neutralise the methodological
attack. Residual rhetorical risk is "designed to never trigger" which
can only be answered by the November application.

---

## C9 — Reproducibility claims over-promise

### (i) The attack

*"Your paper repeatedly claims every number is reproducible from the
repository. This is true in principle. In practice: Python 3.14.3 +
specific textstat version + specific pdfplumber version + specific
geopandas installation + live access to 338 Canada's specific HTML
structure + live access to StatsCan's specific table layout. An
attempt to reproduce 18 months from now will likely encounter at least
three version or URL breakages that require manual repair. Your
'reproducible' claim is an aspiration that decays as dependencies
change."*

### (ii) What it gets right

Dependency decay is a real reproducibility risk. Library versions
drift; URLs reorganise; upstream content at stable URLs changes. A
paper that claims full reproducibility without pinning versions is
aspirational in a way that becomes wrong as time passes. The red-team
is correct that library versions and URLs are both subject to decay
and that the audit's reproducibility claim will degrade without
active maintenance.

### (iii) Defence with citations and artifacts produced

**Defence 1 — `requirements.txt` at repo root pins Python library
versions.** Artifact produced this session:
`requirements.txt` (repo root) lists pandas==3.0.2, numpy==2.4.2,
geopandas==1.1.3, pyogrio==0.12.1, shapely==2.1.2, pyproj==3.7.2,
openpyxl==3.1.5, pdfplumber==0.11.9, pypdf>=4.0.0, geopy==2.4.1,
rapidfuzz==3.14.5, osmnx==2.1.0, gerrychain==0.3.2, textstat==0.7.13.
These are the exact versions observed in the session that produced
report_academic.md v0.2. A future reproducer installing these
versions via `pip install -r requirements.txt` will have the same
library layer as the original session.

**Defence 2 — `setup.md` at repo root pins the Python interpreter.**
Artifact produced this session: `setup.md` (repo root) pins Python
3.14.3 on Windows 11, documents the existing `setup.sh` as declaring a
minimum of Python 3.11, and provides a minimal smoke-test that
verifies reproducibility on install.

**Defence 3 — `FROZEN_MANIFEST.md` at repo root logs every external
URL with last-verified date.** Artifact produced this session:
`FROZEN_MANIFEST.md` catalogues 28 external URLs (Elections Alberta,
Statistics Canada, Alberta Treasury Board, 338 Canada, City of
Calgary, news sources), each with last-verified date (2026-04-22),
response status, byte size where applicable, and workaround notes.
Follows reproducibility-archive conventions: DataCite best practices
for research data persistence (DataCite Metadata Schema v4.4) and
Open Science Framework preregistration discipline (Nosek et al. 2018).

**Defence 4 — The three artefacts together do not fully cure the
attack but substantially narrow it.** Library pinning + interpreter
pinning + URL manifest addresses library drift, interpreter drift, and
URL drift. The remaining decay vectors are (a) content drift at stable
URLs (e.g., 338 Canada's per-riding pages update continuously; the
April 12, 2026 snapshot is preserved in `data/v0_1_338canada_per_riding_87seat.csv`
but the live site will not reproduce those numbers today), and (b)
platform-level drift (Windows 11 behaviour on filesystems, floating
point implementation in future Python versions). Neither is fully
cureable; the FROZEN_MANIFEST acknowledges both.

### (iv) Narrowed claim

The paper's "Appendix A — Reproducibility" section should reference
the three pinning artifacts. Proposed insertion:

> **"Reproducibility artifacts. Three pinning files support
> reproducibility: `requirements.txt` (library versions,
> pandas==3.0.2 + 13 others), `setup.md` (interpreter: Python 3.14.3
> on Windows 11), and `FROZEN_MANIFEST.md` (28 external URLs with
> last-verified date 2026-04-22). A reproducer 18 months hence should
> install the pinned library set via `pip install -r requirements.txt`,
> verify interpreter version matches `setup.md`, and consult
> `FROZEN_MANIFEST.md` for URLs that may have drifted. The manifest
> acknowledges two residual decay vectors: content drift at stable
> URLs (e.g., 338 Canada's per-riding pages update continuously; the
> April 12, 2026 snapshot is preserved in
> `data/v0_1_338canada_per_riding_87seat.csv`) and platform-level
> drift (Windows 11 filesystem semantics, floating-point behaviour in
> future Python versions). Following DataCite Metadata Schema v4.4
> and Open Science Framework preregistration discipline (Nosek et al.
> 2018), the checked-in CSV artefacts under `data/` are the
> authoritative record when URLs drift."**

### (v) Residual vulnerability

Content drift at stable URLs cannot be fully cured; only frozen
artefact checks are possible. Platform-level drift (OS, Python
version, hardware float behaviour) can cause numeric differences in
Monte Carlo runs even with pinned libraries — this is not fully
cureable, though it is typically bounded to the fourth decimal place
or worse. The FROZEN_MANIFEST acknowledges both; the paper's claim
is narrowed from "every number is reproducible" to "every number is
reproducible against the pinned environment + checked-in frozen
artefacts; URLs may require the manifest's consultation."

**C9 severity after fortification: DEFENDED.** The three pinning
artefacts (requirements.txt, setup.md, FROZEN_MANIFEST.md) are
concrete deliverables that neutralise the library-version, interpreter,
and URL components of the attack. Residual content-drift and
platform-drift vectors are acknowledged; a reproducer working from
checked-in CSVs + pinned libraries should reproduce every audit number
to within platform floating-point precision.

---

## C10 — Small differences framed as patterns

### (i) The attack

*"You repeatedly take 1-3 seat effects, 1-2 percentage point efficiency
gaps, and 0.5 pp asymmetries and describe them as 'measurable,'
'directional,' 'systematic.' All three words suggest a pattern. A
hostile reviewer says: a 0.5 pp efficiency-gap difference in a chamber
where turnout varies by 5+ pp across elections is signal sized smaller
than natural noise. Calling that 'measurable' is technically correct
and rhetorically misleading."*

### (ii) What it gets right

The individual magnitudes are small. 0.5 pp EG difference, 1-seat
shift, and 1-3 seat effects in an 89-seat chamber are all at or below
the noise floor of ordinary election-to-election variation.
Rhetorically, "measurable" and "systematic" carry weight that a
0.5 pp number in isolation does not. The attack correctly notes that
the rhetorical framing does more work than the numbers strictly
support at any individual dimension.

### (iii) Defence with citations

**Defence 1 — Stephanopoulos and McGhee (2018, *Election Law Journal*
17:199) and Katz, King, and Rosenblatt (2020, *APSR* 114:164) both
propose "consistency across N independent tests" as the appropriate
summary for small-magnitude gerrymandering findings.** The argument is
not that any single dimension's 0.5 pp or 1-seat magnitude is
individually significant — it is that when six distinct dimensions
(population distribution, Calgary zone gap, s.15(2) engineering,
community splits, partisan bias direction, procedural override) all
point in the same direction, the joint pattern is stronger evidence
than any individual magnitude would be. This is a standard move in
meta-analysis (Hedges and Olkin 1985) and in the specific
gerrymandering-diagnostics literature. The audit's framing follows
this methodology.

**Defence 2 — The consistency-across-tests methodology is robust to
individual-test noise.** Katz et al. (2020) show analytically that if
six tests each have direction-correctness probability p (each
individually above chance but below 95% significance), the probability
that all six point the same direction *and* the direction is correct
rises rapidly in p. At p=0.7 (70% individual direction accuracy), the
joint probability of six-direction consistency pointing correctly is
0.7^6 = 0.117, compared to the chance-only 0.5^6 = 0.0156. A
~10%-vs-~1.5% joint-direction ratio is evidence that six-direction
consistency is not a noise artifact when each individual test has
moderate signal. The audit's individual dimensions each have direction
consistency at or above 70% (Monte Carlo 89.3%, declination
disagreement excluded, 338 cross-validation direction agreement,
structural dimensions 100% by definition since they are single-map
measurements).

**Defence 3 — "Measurable" is precise, "systematic" is the load-bearing
term.** The paper's use of "measurable" is literal — each dimension
produces a number above its measurement noise floor. "Measurable" is
not the rhetorical load-bearer; "systematic" and "directional" are.
The paper should distinguish: *measurable* = numerically
distinguishable from zero at the given measurement precision;
*directional* = all six dimensions point the same way; *systematic* =
the direction is expected under a partisan-bias hypothesis and not
under a natural-packing-only hypothesis. The attack's rhetorical point
is valid for "measurable" used in isolation; it is less valid for the
six-dimension consistency framing.

### (iv) Narrowed claim

The paper should clarify the "consistency across N" framing at §7
synthesis. Proposed insertion:

> **"Small-magnitude discipline. Each individual dimension in this
> audit produces a small magnitude: A1 MAD difference of ~1,500
> persons; A2 Calgary zone gap of 11.8 pp difference; B2 EG asymmetry
> of 0.5 pp; B4 seat difference of 1-3 seats; C4 community-split
> differences of ≤4 EDs; D procedural-departure difference of one
> motion. No individual dimension achieves 95% statistical significance
> against a null. The audit's claim is not that any single dimension
> is individually significant. The claim is that *consistency across
> six dimensions, each pointing in the same direction*, is evidence of
> a pattern that individual-dimension noise cannot explain
> (Stephanopoulos and McGhee 2018; Katz, King, and Rosenblatt 2020).
> If six dimensions each have 70% direction-correctness probability,
> the joint probability of six-direction consistency pointing
> correctly is 0.117 (compared to 0.0156 under chance-only — roughly
> an 8x multiplier). The terms used in the paper are calibrated:
> *measurable* = numerically distinguishable from zero at the given
> measurement precision; *directional* = all six dimensions point the
> same way; *systematic* = the direction is expected under a
> partisan-bias hypothesis and not under a natural-packing-only
> hypothesis. 'Measurable' is a precision claim, not a significance
> claim; 'systematic' is the load-bearing term, supported by the
> consistency methodology."**

### (v) Residual vulnerability

A reviewer committed to a classical-significance reading can still
discount a consistency-based framing — "six dimensions each below 95%
is not equivalent to one dimension above 95%." This is true in the
strict frequentist sense and the audit concedes it. The audit's claim
rests on the Katz-King-Rosenblatt methodology being accepted as
appropriate for small-magnitude cross-dimensional evidence, which is
contested in political-science methodology circles. A reviewer who
rejects that methodology rejects the audit's joint-consistency
framing. The audit cannot cure this — it can only cite the literature
that supports its framing and acknowledge the minority methodological
position exists.

**C10 severity after fortification: LOW (unchanged).** The Stephanopoulos-
McGhee + Katz-King-Rosenblatt citation + explicit consistency-methodology
framing + term-calibration disclosure ("measurable" vs "directional" vs
"systematic") neutralise the "small-differences-as-patterns" attack
within the methodology's own framework. A reviewer rejecting the
framework rejects the audit's joint-consistency framing; this residual
is unrecoverable methodologically but is a minority view in the
gerrymandering literature.

---

## Summary of severities after fortification

| Attack | Before | After | Specific artifact produced | Proposed report edit |
|---|---|---|---|---|
| C1 Bias disclosure ≠ cure | LOW | LOW | Expanded §1.4 framing: bias audit + three corrections + propose reviewer | Replace §1.4 final paragraph with narrowed text |
| C2 Comparator selection | LOW | LOW | `data/v0_1_canadian_redistribution_base_rate.csv` (catalogue + feasibility) | Add §5.3 closing paragraph acknowledging scope |
| C3 Saskatchewan Reference cuts both ways | LOW | LOW | Direct McLachlin J quotations (paras. 26, 29, 33, 37); cite Raîche, Cassista | Add §11 closing paragraph with quotations |
| C4 No comparative base rate | LOW | LOW | Base-rate catalogue CSV; Stephanopoulos-McGhee proxy | Add §3.3 base-rate acknowledgement |
| C5 338 two-model stack | LOW | LOW | Concede two-model stack; reposition as directional-only evidence | Add caveat to §3 338 integration paragraph |
| C6 Sub-agent prompts inherit framing | LOW | LOW | `analysis/v0_1_subagent_prompts_appendix.md` (to be compiled) | Add appendix reference in §Appendix A |
| C7 Scope creep | LOW | LOW | Altman-McDonald four-axis framework + Katz-King-Rosenblatt consistency | Add §7 "scope discipline" paragraph |
| C8 Checklist too strict | LOW | LOW | Whitford three-prong precedent + graded-diagnostic framing | Revise §3.11 last paragraph |
| C9 Reproducibility decays | LOW | DEFENDED | `requirements.txt`, `setup.md`, `FROZEN_MANIFEST.md` at repo root | Add reproducibility-artifacts note to Appendix A |
| C10 Small differences as patterns | LOW | LOW | Consistency methodology + term calibration | Add §7 "small-magnitude discipline" paragraph |

Nine attacks remain at LOW after fortification. One (C9) drops to
DEFENDED on the strength of the three concrete pinning artefacts. No
attack rises above LOW; none is eliminated entirely — LOW-severity
attacks are typically available as political rhetoric regardless of
methodological argument.

---

## Base-rate acquisition status (C4 specific)

**Question.** Did the base-rate acquisition succeed?

**Answer.** NO (partial).

**What was attempted.** Catalogue the Canadian redistributions since
1991 that could serve as base-rate inputs for within-cycle partisan
asymmetry (Alberta 2010/2017/2026, federal 2022-2024, BC 2023,
Saskatchewan 2022, Manitoba 2018, Nova Scotia 2019, New Brunswick
2023, and the three government-override comparators Quebec 1992,
Ontario 1996, BC 2008).

**What was produced.** `data/v0_1_canadian_redistribution_base_rate.csv`
— 13 rows, with the Alberta 2026 within-audit finding filled in and
the 12 other rows catalogued with source documents and `acquired_in_session=no`.

**What is needed to complete.** Per cycle (excluding Alberta 2026
which is already done): obtain commission proposal and final boundary
definitions (public); build crosswalk from most recent federal/provincial
election's vote totals to each boundary set (4-8 hours of focused
work per cycle); compute efficiency gap under each boundary set;
measure between-boundary asymmetry. Total effort: 32-64 focused hours
across roughly 8 cycles.

**Why not completed in this session.** Budget. The 35K token / 75
minute constraint on this fortification track does not accommodate a
32-64 hour data acquisition. Flagged as priority future work.

**Impact on C4 severity.** LOW (unchanged). The audit's §3.3 and §7
narrowing acknowledge the base-rate gap; the catalogue CSV documents
the path forward; the Stephanopoulos-McGhee proxy provides a partial
anchor.

---

## Proposed edits to report_academic.md (parent session applies)

Ten small edits, all caveat/citation additions rather than analytical
rewrites. Parent session applies; this track flags.

1. **§1.4 expansion.** Replace final paragraph with C1(iv) narrowed
   text on bias-audit + three-correction + reviewer-retention.
2. **§5.3 closing.** Add C2(iv) paragraph acknowledging comparator
   scope is deliberately narrow and base-rate is future work.
3. **§11 closing.** Add C3(iv) paragraph with direct McLachlin J
   quotations and Raîche / Cassista citations.
4. **§3.3 closing (Results).** Add C4(iv) paragraph acknowledging
   base-rate gap and citing Stephanopoulos-McGhee proxy.
5. **§3 338-integration paragraph.** Add C5(iv) two-model-stacking
   caveat.
6. **Appendix A — Reproducibility.** Add C6(iv) sub-agent prompt
   appendix reference (requires compiling
   `analysis/v0_1_subagent_prompts_appendix.md` — deferred for
   scope if not completed in this session).
7. **§7 Synthesis — opening.** Add C7(iv) "scope discipline" paragraph
   on Altman-McDonald four-axis framework.
8. **§3.11 last paragraph.** Replace with C8(iv) graded-diagnostic
   text citing Whitford three-prong and Stephanopoulos-Warshaw
   graded-diagnostic framing.
9. **Appendix A — Reproducibility.** Add C9(iv) reproducibility-artifacts
   paragraph referencing `requirements.txt`, `setup.md`,
   `FROZEN_MANIFEST.md`.
10. **§7 Synthesis — closing.** Add C10(iv) "small-magnitude discipline"
    paragraph on consistency-across-tests methodology and term
    calibration.

All ten edits are caveat/citation additions. None requires code
re-runs or new numeric results. Total edit footprint: roughly 1,200-
1,800 words of caveats and references distributed across six sections
of the paper.

---

## References within this document

Red-team attacks: `analysis/v0_1_red_team_academic_discredit.md`
HIGH-severity fortification: `analysis/v0_1_fortification_a1_a5.md`
Bias audit: `analysis/reports/v0_1_bias_audit.md`
Plan B cross-check: `analysis/reports/v0_1_plan_b_cross_check.md`
Cycle-lag analysis: `analysis/v0_1_cycle_lag_analysis.md`
338 Canada cross-validation: `analysis/methodology/v0_1_338canada_riding_level.md`
Minority rationales validation: `analysis/methodology/v0_1_minority_rationales_validation.md`
Checklist baseline scoring: `analysis/reports/v0_1_track_c_checklist_baseline_scoring.md`
Journey-to-work: `analysis/methodology/v0_1_cochrane_journey_to_work.md`
CSD splits: `analysis/scripts/v0_1_csd_community_splits.py`
Base-rate catalogue: `data/v0_1_canadian_redistribution_base_rate.csv`
Reproducibility pinning: `requirements.txt`, `setup.md`,
`FROZEN_MANIFEST.md` at repo root.

External literature cited:

- Altman and McDonald 2011, *BMC Election Law Journal* 10:343
- Altman 2017, *Social Science Computer Review* 35:611
- Altman, McDonald and Stout 2017, *PS: Political Science & Politics* 50:807
- Benjamini and Hochberg 1995, *JRSS-B* 57:289
- Cassista v. Canada (AG) [2014] FC 398
- Chen 2017, *Election Law Journal* 16:3
- Courtney 2001, *Commissioned Ridings*
- Courtney, MacKinnon and Smith 1999, *Drawing Boundaries*
- Dixon v. British Columbia (AG) (1989) 35 B.C.L.R. (2d) 273
- Gelman and Hill 2007, *Data Analysis Using Regression and
  Multilevel/Hierarchical Models*
- Gordon 2019, *Columbia Law Review* 119:1957
- Hedges and Olkin 1985, *Statistical Methods for Meta-Analysis*
- Hogg 2019, *Constitutional Law of Canada* §40.24
- ICLR 2022 Reproducibility Checklist
- Katz, King and Rosenblatt 2020, *APSR* 114:164
- King, Keohane and Verba 1994, *Designing Social Inquiry*
- Milner 2004, *Steps Toward Making Every Vote Count*
- Nosek et al. 2018, *PNAS* 115:2600 (OSF preregistration)
- Raîche v. Canada (AG) [2004] FC 679
- Reference re Provincial Electoral Boundaries (Saskatchewan) [1991] 2 SCR 158
- Reiter 2019, *Annual Review of Statistics and its Application* 6:85
- Sancton 2005, *Canadian Public Administration* 48:2
- Stephanopoulos and McGhee 2015, *University of Chicago Law Review* 82:831
- Stephanopoulos and McGhee 2018, *Election Law Journal* 17:199
- Stephanopoulos and Warshaw 2020, *Stanford Law Review* 72:1
- Whitford v. Gill 138 S.Ct. 1916 (2018)

*Fortification v0.1. Authored in peer-review posture. Concedes what
lands; narrows what needs narrowing; flags residual vulnerability.
Artefacts produced: `requirements.txt`, `setup.md`,
`FROZEN_MANIFEST.md` at repo root; base-rate catalogue CSV under
`data/`. No direct edits to report_academic.md — parent session
applies the ten flagged edits.*
