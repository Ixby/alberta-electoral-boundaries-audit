---
name: Duane Bratt outreach email
description: Draft email to Dr. Duane Bratt, Professor of Political Science at Mount Royal University, introducing the audit, asking about informal advising interest, and asking whether he could facilitate Elections Alberta shapefile access. Same-institution collegial framing.
forward_dependencies:
  - PO review / send from PO's Mount Royal email
  - Possible introduction to Elections Alberta via Bratt's contacts
  - Possible methodological review / co-authorship path if Bratt is interested
backward_dependencies:
  - analysis/v0_1_elections_alberta_shapefile_request.md (the cold-email version; Bratt route is warmer)
  - report_academic.md (the subject-matter)
  - analysis/v0_1_approximate_shape_analysis.md (current state of the geometry gap)
---

# Draft email — Dr. Duane Bratt

**Status:** Draft. PO review required before sending.

**Recipient:** Dr. Duane Bratt, Professor, Department of Economics, Justice, and Policy Studies, Mount Royal University. Email via Mount Royal faculty directory (`https://www.mtroyal.ca/ProgramsCourses/FacultiesSchoolsCentres/Arts/Departments/EconomicsJusticePolicyStudies/Faculty/DuaneBratt/index.htm` or `dbratt@mtroyal.ca`).

**Why Bratt specifically:**
- Same institution — Will Conner is a Mount Royal 4th-year BSc student. Collegial within-institution approach.
- Active public commentator on Alberta provincial politics; has been quoted in coverage of the 2025–26 commission and the April 16 motion.
- Long publication record on Alberta policy and UCP-era governance.
- Potential facilitator for Elections Alberta GIS team outreach via existing academic networks.
- Potential informal advisor on methodological choices (political science norms for the kinds of tests the audit runs).

**Recommended send:** Friday or weekend is fine for outreach; Monday morning preferred for reply-odds.

---

## Email draft

**Subject:** Mount Royal student — non-partisan audit of the 2026 electoral boundary proposals, seeking a quick conversation

Dear Dr. Bratt,

My name is Will Conner. I am a fourth-year Mount Royal BSc student in Computer Information Systems, and for the last several weeks I have been running a non-partisan audit of the 2025-26 Electoral Boundaries Commission's two recommended maps. The work is a personal interest project, not a course assignment.

I am writing for two reasons.

**One, I would value a brief conversation** if you have the bandwidth. My background is not political science, and the audit has pushed me into methodological choices (efficiency gap, declination, Monte Carlo sensitivity, Chen and Rodden natural-packing tests, community-of-interest coding) where a second set of eyes from someone who teaches this material would help me catch errors I cannot see. I am not asking for formal supervision or co-authorship — just whether you have 30 minutes in the next two or three weeks where I can walk through the methodology and findings, and where you can tell me what I have missed. If the work holds up under that conversation, I would like to know what the next step toward academic publication would look like. If it does not hold up, I would like to know that too, before anything goes public.

**Two, I have a specific logistical request**: I am trying to obtain the polygon shapefiles for the Commission's majority and minority 2026 proposals from Elections Alberta. The 2019 boundaries and 2023 voting-area files are already publicly posted, but the 2026 proposal shapefiles have not been released. Several of the most diagnostic tests — Polsby-Popper and Reock compactness, Chen-Rodden-style neutral-ensemble MCMC comparisons, precise voting-area attribution — require actual polygon geometry rather than the approximations I have built from the 2019 boundaries and the Commission's JPG maps. I have drafted a research-access request to Elections Alberta and am weighing an informal email to their GIS team against a formal FOIP request. If you have existing contacts at Elections Alberta or on the Commission who might respond to an introduction from a faculty member, that route would be much faster than a cold submission. If not, no worries — I will pursue the formal channel.

The work to date is public at `https://github.com/Ixby/alberta-electoral-boundaries-audit`. The quickest overview is the draft public-facing report (`report_public.md` in the repo) which walks the findings in plain language. The technical detail is in `report_academic.md` and the analysis files. Headline: the minority map shows measurable structural differences from the majority on population equality, Calgary geographic-zone balance, community-of-interest treatment (Airdrie, Lethbridge, and Red Deer all split four ways in the minority, two ways in the majority — this is a new finding that came out of a symmetric counter-test), and at least one engineered s.15(2) boundary (Rocky Mountain House-Banff Park). The partisan-bias metrics are directionally UCP-favourable for the minority at about 90% confidence against 2023 votes — not statistically significant at the conventional 95% threshold, and the direction reverses when 2019 votes are used as input. A red-team pass on the draft has surfaced some real vulnerabilities I am still working through. The procedural analysis of the April 16 motion is the part I feel most sure-footed on; the partisan-math claims are where I most want a methodological second opinion.

If a conversation is feasible I am flexible on format (in-person at campus, phone, email thread, anything). If not, a brief email response indicating "not right now" or "try so-and-so instead" is equally welcome.

Thank you for your time. I am aware this is a cold email from an undergraduate to a senior faculty member, and I appreciate the consideration.

Best,

Will Conner  
BSc Computer Information Systems, 4th year  
Mount Royal University  
[email address]  
[phone, optional]

GitHub: `https://github.com/Ixby/alberta-electoral-boundaries-audit`

---

## Reasoning notes (for PO, not to be sent)

**Tone calibrations:**
- Opens with "personal interest" to signal this is not a course assignment demanding academic obligation.
- Uses "quick conversation" as the entry ask, not "full supervision" or "co-authorship" — lower cost to Bratt's inbox.
- Surfaces the methodological uncertainty *openly* ("red-team pass has surfaced some real vulnerabilities I am still working through") — signals maturity rather than defensiveness; more likely to trigger a helpful response than a guarded one.
- Explicitly names the partisan-math claims as "where I most want a methodological second opinion" — not overclaiming; asking for help where help is needed.
- Flags the procedural analysis as the sure-footed part — signals the audit has a defensible core.
- Lethbridge / Red Deer 4-way finding mentioned because it is new and concrete and will catch a political scientist's attention.

**What the email does NOT do:**
- Does not ask Bratt to promote the work or share it politically.
- Does not name-drop.
- Does not pitch the audit as journalism-ready or action-ready.
- Does not reference the red-team as a selling point — mentions it as evidence that the audit has been stress-tested, not as a framing device.
- Does not ask for Bratt's public endorsement.

**Anticipated response scenarios:**
1. **Positive, "sure, send me a time":** best case. Brief the PO on how to prep for the meeting (5-minute opener, specific methodology questions, bring the one-page summary, offer to demo the code).
2. **Positive, "forward to a colleague":** also good. Bratt may route to someone working on Canadian redistricting directly (e.g., a PhD student or post-doc) with more time.
3. **Positive, "here's an Elections Alberta contact":** solves the shapefile question without Bratt taking on advising role.
4. **Polite decline:** totally OK; no loss. The cold email to Elections Alberta still runs.
5. **No response within 2 weeks:** one gentle follow-up email ("just checking this hadn't gone to junk"), then drop it.

**What to have ready if Bratt says yes:**
- One-page executive summary (can be extracted from `report_public.md` opening section).
- The five clearest quantitative findings with source citations.
- The two to three methodological choices where the audit is most vulnerable (cross-election reversal, Monte Carlo CI crossing zero, threshold pre-registration caveats).
- A clean map of the audit's file structure so Bratt can review at his own pace.
- Questions for Bratt: what is the Canadian political-science consensus on efficiency gap vs declination? Has anyone done Chen-Rodden for Alberta before? Is there a published paper on the 2017 Alberta commission's boundary-math outcomes?

**What to NOT do:**
- Don't follow up more than once.
- Don't forward the email to others ("Dr. Bratt and three other faculty") — that signals spam.
- Don't pitch this as political writing. Bratt is an academic first; political commentary is a side activity.
- Don't mention the red-team by label ("attack A1 through A5 now fortified"). Keep the stress-testing framing inside-baseball.
