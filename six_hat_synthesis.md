# Six Thinking Hats — Synthesis of Three Passes
## Alberta Electoral Boundary Audit

*This document synthesizes findings from three independent six-hat analyses: Pass 1 (project integrity and evidentiary weight), Pass 2 (scientific validity and methodological trustworthiness), Pass 3 (strategic impact and the road to November 2026). Where the passes converge, the finding is robust. Where they diverge, the tension is noted.*

---

## WHITE HAT — The Consolidated Factual Record

### What exists and is verified

**The maps:** Two competing 89-seat commission recommendations (majority: chair + 2 opposition-appointed; minority: 2 government-appointed) plus the 2019 87-seat baseline. Government rejected majority on April 16, 2026. Lunty MLA committee now draws the operative 91-seat map, expected November 2, 2026.

**The data (all public):** 1,973 election polls (2023), 87 ridings, Statistics Canada 2021 Census DAs, official Elections Alberta shapefiles (received May 6, 2026), 1,252 machine-parseable public submissions, 77-snapshot 338Canada polling series.

**Structural findings — vote-independent, survive all stress tests:**

| Metric | Majority | Minority | Delta |
|--------|----------|----------|-------|
| MAD from provincial average (54,929) | 3,180 | 4,707 | +48% |
| Ridings >+10% deviation | 5 | 15 | +10 |
| Ridings >+15% deviation | 0 | 5 | +5 |
| Max positive deviation | +14.28% | +24.06% | +9.78 pp |
| Calgary zone gap (NE/central vs S/W) | +0.36% | +12.20% | +11.84 pp |
| Airdrie municipal splits | 2 EDs | 4 EDs | 2× |
| Municipal boundary anchoring | 71.0% | 14.5% | 4.9× |
| Cartographic anomalies (chair-flagged) | 0 | 3 | — |

**Partisan-bias findings — vote-dependent, method-sensitive:**

| Metric | Majority | Minority | Direction |
|--------|----------|----------|-----------|
| Efficiency Gap (crosswalk, w=0.85) | −0.40% | −1.81% | Minority UCP-favorable |
| EG sensitivity range (asymmetry) | — | — | −0.51 to −1.52 pp |
| Mean-Median Gap | 2.1% | 3.5% | Minority UCP-favorable |
| Seats@50/50 (CI) | 43–46 | 41–47 | Overlapping — no difference |
| Declination | −0.021 | −0.015 | **Minority least UCP-favorable** |
| MCMC EG p-rank (ESS-adjusted) | p92.66 | p98.76 | Minority outlier |
| 338Canada April 2026 | — | +1 NDP seat | **Direction reversal** |
| Monte Carlo directional confidence | — | 90.5% | 95% CI crosses zero |

**Pre-registration:** OSF w2s8k, r3zm7, qsgy8, 6pt83; AsPredicted #289449, #289451, #289455. 17-test scoring grid committed for November 2026 Lunty map. 72-hour window from release.

**Red-team resolution:** 4 CRITICAL identified and addressed (p100→p98.76 ESS correction; "2h 24m separation" retracted; canonical shapefile recompute triggered). 8 HIGH disclosed but not all corrected (family-wise error rate, E2 reformulation, Canadian base-rate circularity, uniform-swing violation).

**What is definitively unknown:** Intentionality. The 7% EG judicial threshold (never adopted in Canada). What the Lunty map will show. Whether independent academic replication will confirm core results.

---

## RED HAT — Consolidated Emotional and Intuitive Read

All three passes converge on the same emotional terrain. The synthesis:

**The project exceeds its container.** A 234-node dependency DAG, eight-stage geometry pipeline, pre-registered falsifiability gates, and a self-commissioned science red-team is not undergraduate work in form. The gap between the institutional setting (one student, no funding, no lab) and the methodological ambition is striking and deserves recognition.

**The April 16 pivot feels wrong.** Across all three passes this reaction is consistent and strong. A government rejecting an independent commission's majority report and substituting its own MLA committee is not how the process is supposed to work. The intuitive alarm this produces is appropriate and should not be reasoned away.

**The visual anomalies are more persuasive than the statistics.** The Airdrie 4-way split, the lasso-shaped corridor reaching across the Bow River valley, the park extension through uninhabited national park — these do not require statistical literacy to produce concern. They look like what they look like.

**The 1.41 pp EG asymmetry feels like a real signal but not a smoking gun.** It is consistent, directional, and meaningful. It is also far below any threshold that would compel a legal or political remedy on its own. The emotional tension between "this matters" and "this will move people" is real and should inform how findings are communicated publicly.

**The red-team honesty produces trust; the CRITICAL errors produce caution.** The willingness to find, report, and correct p100→p98.76 and the P/C/E specification timing error is admirable and rare. But the fact that these errors existed — that the audit initially overclaimed tail precision and misstated its own specification timeline — should make any reader appropriately cautious about uncorrected HIGH issues.

**The 338Canada direction reversal produces genuine unease.** Three passes, same reaction. A finding that contradicts the structural direction under a plausible future vote environment is not a footnote. It is a substantive problem that the emotional radar correctly flags as unresolved.

**The silence around the project is uncomfortable.** Published. On GitHub. Methodologically substantial. No documented uptake. No news coverage. No academic co-author. The project is doing the work of a civic institution without one.

---

## BLACK HAT — Consolidated Risks and Vulnerabilities

All three passes identified overlapping vulnerabilities. Ranked by severity across the synthesis:

### Tier 1: Vulnerabilities that constrain what can be claimed

**1. Family-wise error rate uncorrected (HIGH, S2-03)**
21 tests, no Bonferroni or Benjamini-Hochberg correction. Per-test α at Bonferroni: 0.0024. Multiple findings that appear significant at α=0.05 may not survive correction. This is disclosed but not fixed. Individual test statistics in the paper are potentially misleading. This is the most persistent unresolved methodological flaw.

**2. Directional disagreement between partisan-bias metrics**
EG and Mean-Median: minority is most UCP-favorable. Declination: minority is *least* UCP-favorable. 338Canada polling: minority produces +1 NDP seat. Three metrics pointing in one direction and two pointing in another is not a clean directional finding. The correct characterization is "majority of methods show a consistent pattern, with documented exceptions." Any simpler statement overstates.

**3. Monte Carlo CI crosses zero**
90.5% directional confidence is meaningful. The 95% CI on EG asymmetry [−3.04, +0.76] pp crossing zero means the directional claim fails at classical significance. Re-labeling "sensitivity interval" is methodologically correct but does not change the statistical reality.

### Tier 2: Vulnerabilities that limit the P/C/E framework

**4. P/C/E criteria are retrospective, not pre-registered**
Same commit, same session. Relabeled correctly as "retrospectively-defined." Cannot carry confirmatory evidential weight. These are exploratory findings — valuable, but structurally equivalent to post-hoc rationalization regardless of labeling.

**5. E2 reformulation fits the optional-stopping pattern**
Criterion reformulated mid-audit after initial version failed to detect the target. Disclosed. Still a problem. The E2 result is the one that detects what the researcher suspected was there, not the criterion that was specified first.

**6. Counter-tests held from formal count in same pass as signatures**
Lethbridge and Red Deer 4-way splits were detected in the same analytical pass and held. The basis for holding them is documented. The selection is still researcher-determined. The three formal signatures are the detected patterns the researcher chose to count, out of more detected patterns.

### Tier 3: Strategic vulnerabilities

**7. Partisan capture risk**
The moment the NDP amplifies the audit before academic validation occurs, the government can dismiss it as opposition research. This risk is external to the methodology but may be more practically damaging than any methodological weakness.

**8. Government may simply proceed regardless**
A government that replaced an independent commission with its own committee is unlikely to be moved by a statistical audit. The Lunty map may be tabled, debated briefly, and enacted. The audit becomes part of the record but not a lever.

**9. Solo author, no institutional replication**
All code and methodology are public. No independent third-party replication has been conducted. The code audit was by AI, not a human statistician. An undetected systemic bug could invalidate findings in ways the dependency DAG would not catch.

**10. The 338Canada direction reversal is unexplained**
The mechanism by which the minority map produces +1 NDP seats under April 2026 polling while showing UCP-favorable EG under 2023 results is not quantified. The audit notes vote-distribution dependence but does not establish which electoral environment is more representative. If the answer is "April 2026 polling," the framing of the entire partisan-bias section requires revision.

---

## YELLOW HAT — Consolidated Strengths and Value

All three passes converge on these genuine strengths:

### The structural findings are the project's bedrock

MAD, Calgary zone gap, Airdrie split count, municipal anchoring percentage — none of these depend on votes, attribution methods, election cycles, or parameter choices. They are direct measurements from the commission's own maps using the commission's own methodology as the standard. They cannot be reversed by a methodological objection. They are the finding the public report should lead with and the finding that will survive the longest.

### The April 16 procedural finding stands independently

The substitution of a government-controlled MLA committee for an independent commission majority recommendation has no precedent in recent Canadian redistricting history (BC 2008, Quebec 1992, Ontario 1996 all handled differently). This finding requires no statistical literacy. It is a factual observation about a democratic norm. It is the most legally and politically durable finding in the audit.

### The pre-registration for the Lunty map is the project's most credible contribution

The 17-test scoring grid is committed. The 72-hour window is specified. Numeric thresholds are fixed. The map does not yet exist. When it does, the audit will be the first rigorous public analysis available, with unimpeachable pre-registration. If the committee map shows anomalies, the pre-registered finding will carry significantly more evidentiary weight than everything in the retrospective audit combined. If it does not, the audit will say so. Either outcome is a civic contribution.

### The dependency DAG is an original methodological contribution

No Canadian redistricting audit has published a directed acyclic graph of analytical dependencies with explicit orphaning conditions. This makes the audit uniquely interrogable and uniquely honest about what depends on what. It is a civic technology contribution independent of the partisan-bias findings.

### The red-team correction process demonstrates scientific integrity

The CRITICAL corrections — p100→p98.76, P/C/E specification timing retraction, canonical shapefile recompute — were found, corrected, and documented publicly. This is rare. It is the strongest possible evidence that the author's commitment is to accuracy rather than to a predetermined conclusion.

### The Act amendment proposal is constructive and actionable

90-day public comment minimum, paired population tables, written deviation explanations — these translate findings into a draft bill. They give the opposition MLAs something to table. They give future commissions a procedural framework. This is how audit findings become durable policy change.

### The Enoch Cree Nation dimension has the broadest coalition potential

Minority map: Enoch Cree Nation paired with distant Devon. Majority map: paired with adjacent Edmonton. This is a community-of-interest finding with s.35 constitutional dimensions. It is the one finding that connects to Indigenous rights law, federal Crown obligations, and UNDRIP in ways that far exceed the audit's current framing. It is underdeveloped and should not remain so.

---

## GREEN HAT — Consolidated Priority Actions

All three passes generated creative directions. Consolidated by feasibility and impact:

### Highest priority (do before November 2026)

**1. Complete the counter-map challenge (Issue #14)**
Produce an alternative map achieving the minority's stated representational objectives with majority-level municipal boundary anchoring. If it can be done — and it almost certainly can — the unavoidability defense collapses entirely. This is the single most powerful piece of evidence available. It requires no statistical literacy to understand. "Here is what those boundaries could have looked like" is a sentence anyone can follow.

**2. Apply Bonferroni/BH correction and propagate**
One to two days of analytical work. Report both corrected and uncorrected p-values. Note which findings survive correction. This closes the most persistent documented HIGH issue before the November scorecard runs.

**3. Run the 338Canada 77-snapshot sensitivity**
Automate EG and MM calculation across all 77 historical polling snapshots. If the EG asymmetry is consistently directional across most snapshots, the vote-distribution-dependence concern is substantially reduced. If it reverses frequently, the finding is fragile and should be relabeled. Either answer is useful.

**4. Pre-brief 2–3 academics before November**
Duane Bratt (MRU, follow up on April 23 outreach) plus one or two others. Academics who have read and understood the methodology before the committee map drops can comment for media within 24–48 hours of publication. That window is what distinguishes "independent civic analysis" from "partisan attack" in news coverage.

### High priority (June–September 2026)

**5. Submit the methods paper to a statistical methods journal**
The DPG framework documentation is publishable independently of the Alberta controversy. "Constructing Provincial Electoral Geometries Without Official Shapefiles" solves a real problem with broad applicability. A methods paper under review before November establishes academic standing.

**6. Submit audit preprint to SSRN/OSF**
Low effort, immediate legitimacy signal. A preprint with a stated journal submission is meaningfully different from a GitHub repo in how journalists and academics perceive it.

**7. Run the 2019-seeded MCMC ensemble (Issue #13)**
The historically-enacted null hypothesis is more legally relevant than the random-draw null. Seeding from the 2019 map asks "how far does this proposal deviate from what Alberta voters have lived under?" — a more grounded framing.

**8. Expand the Indigenous dimension**
Commission a section on Enoch Cree Nation, s.15(2) eligibility criteria, and any other affected First Nations communities. Engage an Indigenous legal scholar or First Nations organization as co-reviewer. This broadens the coalition, strengthens the analysis, and connects to constitutional dimensions the current audit does not reach.

### Strategic actions (before November)

**9. Build the November scorecard dashboard**
A simple GitHub Pages dashboard showing the 17 tests with pass/fail status as results are computed — linked to OSF pre-registration and individual methodology documentation — makes the pre-registration concrete for non-statisticians. No hosting cost. Built once, ready to populate.

**10. Prepare the media kit**
One-page explainer, five-bullet summary, three publishable graphics, FAQ on common objections. Prepared before November. Ready to distribute the moment the scorecard is published. Journalists on deadline will not read the monograph.

**11. Approach the Globe and Mail data desk with a pre-November briefing**
The Globe's data journalism team has covered redistricting before. An advance briefing — "here is the pre-registered methodology; when the map drops on November 2, this is what we will report within 72 hours" — is a compelling pitch. Highest-reach single media placement available.

---

## BLUE HAT — Process Synthesis and Consolidated Direction

### What three passes have established

The three analyses converge on a consistent and coherent picture:

**The project is scientifically honest and methodologically ambitious.** It has real findings, real limitations, and a genuine commitment to transparency that is rare in public-interest research. The CRITICAL errors were caught, corrected, and documented. The HIGH issues are disclosed. The retraction conditions are specified. The dependency graph is public.

**The structural findings are the foundation; the partisan-bias findings are the superstructure.** The structural findings (MAD, zone gap, Airdrie, anchoring) do not need the partisan-bias analysis to matter. They stand on their own. The partisan-bias findings add important context — consistent direction, MCMC outlier status — but are appropriately characterized as sub-threshold in magnitude with documented directional exceptions.

**The project's greatest strength is ahead of it, not behind it.** The retrospective audit of the 2026 commission maps is complete and published. The prospective pre-registered audit of the November 2026 Lunty committee map is the project's most credible and most strategically significant contribution. Everything done between now and November 2 is preparation for that moment.

**The project's greatest vulnerability is not methodological — it is isolation.** One author, no institutional home, no documented academic engagement, no media coverage, no community organization co-signatories. The methodology can sustain attack. The isolation cannot. The five months before November are an opportunity to address this.

### The consolidated claim the evidence supports

> "The minority commission recommendation departs from the majority recommendation on five structural dimensions independent of vote data, all running in the same direction. Partisan-bias metrics show a consistent but sub-threshold directional pattern across most analytical methods and election cycles, with documented exceptions including a direction reversal under April 2026 polling. The April 16 government decision to substitute a government-controlled MLA committee for the independent commission majority has no recent Canadian precedent. A pre-registered 17-test audit of the forthcoming committee map will be published within 72 hours of its release."

This claim is fully supported by the evidence. It is the right claim level for public communication. It does not overstate. It does not use the word "gerrymander" as a verdict. It lets readers draw their own conclusions from documented facts.

### The consolidated priority list

| Priority | Action | Timeline | Impact |
|----------|--------|----------|--------|
| 1 | Counter-map challenge (Issue #14) | June 2026 | Highest — collapses unavoidability defense |
| 2 | Bonferroni/BH correction | May 2026 | High — closes primary unresolved HIGH issue |
| 3 | 338Canada 77-snapshot sensitivity | June 2026 | High — resolves direction-reversal concern |
| 4 | Follow up with Duane Bratt; pre-brief 2 more academics | May–July 2026 | High — establishes academic standing before November |
| 5 | Methods paper submission | July 2026 | Medium — long-term academic contribution |
| 6 | SSRN/OSF preprint | June 2026 | Medium — immediate legitimacy signal |
| 7 | 2019-seeded MCMC ensemble | July–August 2026 | Medium — stronger null hypothesis |
| 8 | Indigenous dimension expansion | July 2026 | Medium — broadest coalition potential |
| 9 | November scorecard dashboard | September 2026 | Medium — public communication |
| 10 | Media prep kit | October 2026 | Medium — ready for 72-hour window |
| 11 | Globe and Mail data desk pitch | October 2026 | High if successful — reach |

### What the project is not, and should not claim to be

- Not a finding of intentional partisan manipulation
- Not evidence of legal gerrymandering under any Canadian judicial standard
- Not a pre-registered confirmatory study for the retrospective findings (correctly labeled exploratory)
- Not a claim that the minority map produces worse election outcomes under all vote environments

### What the project is

A rigorous, pre-registered, fully reproducible independent civic audit of a provincial redistricting process, produced at a standard of methodological transparency that exceeds most academic research in this space — and the only such audit that will exist when the November 2026 committee map is released.

---

*Synthesis of Passes 1, 2, and 3 — complete*
