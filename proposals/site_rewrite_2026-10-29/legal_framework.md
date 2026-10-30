# Legal framework for Alberta electoral districts and redistricting: what is required and what is not

Research memo for the site rewrite. Prepared 2026-10-29. Not legal advice.

**How this was sourced.** I read the repo first. After that I relied on WebSearch only. WebFetch is blocked in this session: `decisions.courts.ns.ca` failed with a network-policy error, so I fetched nothing else. **No judgment text was read directly this session.** As a result:

- **VERIFIED-PRIMARY** is used only for statute or Charter text quoted verbatim in the repo. That means the EBCA extracts in `preregistration/terms_of_reference.md` and `findings/terms_of_reference_audit.md`, taken from the King's Printer consolidation of 2024-12-05 and the commission report. I did not re-check that text against King's Printer this session.
- **VERIFIED-SECONDARY** means a reliable secondary source seen in search results this session (law-firm or court summaries, the CBA National Magazine, news, Assembly web pages). Where the only source was Wikipedia or a single search summary, the status says "(weak)".
- **UNVERIFIED** means memory, or a repo claim I could not confirm. A gap stays a gap.

**Pending counsel review (SESSION_HANDOFF.md, item T6).** These citations were already flagged before this session: Pal & Choudhry 2011; *Cassista v. Canada*, 2014 FC 398; the Parks Act citation; the Saskatchewan Reference pinpoints (para. 26 and 33; para. 98 not found); the Cannon year; the KKR attribution. This session's status: Cassista is still not found by search and should be dropped. The pinpoints are still unverified. The other four are outside the legal scope here and were not checked.

---

## 0. The findings that matter most

1. **The site says the 2026 move has "no recorded precedent". Alberta itself is the precedent.**
   - By May 1992 Alberta's commission was deadlocked over hybrid "rurban" ridings. Its final report was "thrown out" in July 1992.
   - The job was handed to a four-MLA Select Special Committee chaired by Bob Bogle (Motion 24, July 2, 1992). The opposition refused to take part, so the committee was all PC MLAs.
   - The committee's map was enacted as the *Electoral Divisions Statutes Amendment Act, 1993* and used in the June 1993 election.
   - On October 24, 1994 the Alberta Court of Appeal found the boundaries consistent with the Charter. It also criticized the process, because committee members could not give a sufficient rationale for several boundaries. It said a proper review was needed within the term of the sitting Legislature.
   - Status: VERIFIED-SECONDARY, from Alberta Views and Wikipedia; the judgment itself was not seen. This contradicts `en.ts` `anomalous_p2`, academic §5.9.3 and `procedural_analysis.md` D4.
2. **NS 2017 holding (2017 NSCA 10).** A five-judge panel advised that the 2012 enactment abolishing the protected Acadian ridings violated Charter s.3.
   - The Attorney General had rejected the commission's interim report and directed it to conform to the ±25% terms of reference. Per a secondary source quoting the court, this "forced the commission to sign a final report with electoral boundaries that did not represent the commission's authentic view of effective representation."
   - The court also noted that the government could have redrawn the map through the legislature. Those prospects, it said, "do not justify stifling the independent commission's view."
   - So the case is about **interference with a commission that the government chose to use**. It does not hold that a legislature must adopt a commission's map.
   - Status: VERIFIED-SECONDARY; paragraph numbers not seen.
3. **The Quebec case is now decided, and the repo is out of date.** The case is *Quebec (AG) v. Lalande*, 2026 SCC 13.
   - Oral judgment came on April 22, 2026, 7–2; written reasons on May 1, 2026. Kasirer J. wrote for the majority; Côté and Rowe JJ. dissented.
   - A statute pausing Quebec's independent commission infringed s.3 and was not saved by s.1. It failed minimal impairment because Quebec could have protected the Gaspésie ridings temporarily while letting the commission finish elsewhere. Unanimous passage did not shield it.
   - On June 12, 2026 Quebec's National Assembly then passed its own act setting a new map and raising the seat count from 125 to 127 to keep the two ridings.
   - Status: VERIFIED-SECONDARY. The academic report still says the reasons are "pending" and names the case "*Coalition de l'Outaouais*". The site's "Quebec contrast" (`quebec_p1`) now misdescribes Quebec.
4. **The /law page cites the wrong section.** It says "Section 12 of the Act also permits referring a commission's recommendations to a legislative committee." Section 12 is the population-data rule (VERIFIED-PRIMARY). Nothing in the repo's verbatim EBCA text provides for referral to a committee. The committee is a creature of an Assembly motion, not of the Act.
5. **The basic process facts on the site need re-checking.**
   - The Assembly's committee page says the committee was "established by Government Motion 37, passed by the Assembly on April 21, 2026". It lists **6 members**: Lunty (chair), de Jonge, Sawyer and Wiebe (UCP), and Ganley and Gray (NDP).
   - The site says "Motion 19", April 16, "five MLAs, three UCP, two NDP".
   - I found no source for a separate Motion 19. The 44–36 count appears only in a GDELT event entry dated April 22.
   - Status: VERIFIED-SECONDARY.
6. **The core gap.** The EBCA's rules bind "the Commission", not the Legislature. The commission rules are: hearings (s.7), deadlines (ss.6 and 8), the ±25% band (s.15(1)) and the s.15(2) exception. When MLAs pass an Electoral Divisions Act, the only hard limit is the Charter, mainly s.3. Section 33 cannot override s.3.

---

## A. What the Constitution requires

### A1. For the districts themselves

| Requirement | Authority | Status |
|---|---|---|
| Every citizen has the right to vote in provincial elections: "Every citizen of Canada has the right to vote in an election of members of the House of Commons or of a legislative assembly and to be qualified for membership therein." | Charter s.3. Quoted verbatim in the commission report; repo `preregistration/terms_of_reference.md` §3 | VERIFIED-PRIMARY (via repo) |
| s.3 protects **effective representation**, not strict equality of voting power. | *Reference re Provincial Electoral Boundaries (Sask.)*, [1991] 2 SCR 158 ("Carter"), McLachlin J. for a 6–3 majority. Cory J., Lamer C.J. and L'Heureux-Dubé J. dissented. | VERIFIED-SECONDARY |
| "Relative parity of voting power is a prime condition of effective representation." | Carter, as quoted in commentary | VERIFIED-SECONDARY (wording seen quoted; no pinpoint) |
| Departures from parity "may be justified on the grounds of practical impossibility or the provision of more effective representation". Factors include geography, community history, community interests and minority representation. Undue dilution of one citizen's vote compared with another's "should not be countenanced". | Carter | VERIFIED-SECONDARY |
| Deviations must be justified as contributing to "better government of the [populace as a whole]" | Carter | UNVERIFIED (the snippet seen was cut off at "better government of the") |
| There is no bright-line numeric tolerance in the Constitution. ±25% is a statutory choice, not a constitutional rule. | Carter, as summarized in repo §2 and Wikipedia; the Alberta and Saskatchewan statutes set ±25% | VERIFIED-SECONDARY |
| The review standard is deferential. Per the Federal Court's summary of Carter, a commission does not contravene s.3 unless "reasonable persons applying the appropriate principles … could not have set the electoral boundaries as they exist." | Raîche v. Canada, 2004 FC 679, summarizing Carter | VERIFIED-SECONDARY |
| A s.3 breach can be justified under s.1 (the Oakes test). In practice Carter justifies deviations inside s.3 itself. Section 1 is reached when a law is found to infringe. | Dixon (BCSC 1989): not saved by s.1. Lalande 2026 SCC 13: failed minimal impairment. Working Families 2025 SCC 5: not saved | VERIFIED-SECONDARY |
| **Section 33 cannot override s.3.** The notwithstanding clause reaches only s.2 and ss.7–15. | Charter s.33, per Justice Canada's Charterpedia. Confirmed in *Ontario (AG) v. Working Families Coalition (Canada) Inc.*, 2025 SCC 5 (5–4), where s.33 had been invoked but could not shield a s.3 breach | VERIFIED-SECONDARY |
| Section 45 of the Constitution Act, 1982 says "Subject to section 41, the legislature of each province may exclusively make laws amending the constitution of the province." This is not a route around the Charter. A province changes its electoral districts by ordinary statute, and the Charter is part of the Constitution of Canada, which s.45 does not reach. I found no case applying s.45 to provincial redistribution. | Constitution Act, 1982 s.45, per a Wikisource text snippet and constitutionalstudies.ca | Text: VERIFIED-SECONDARY. The application is my analysis; no authority was found. |

### A2. For the process that draws them

| Point | Authority | Status |
|---|---|---|
| **The Constitution does not require an independent commission.** I found no authority requiring one, and Carter upheld a scheme in which the legislature itself fixed the urban/rural/northern seat split that the commission had to work within. | Carter. Facts: 29 urban, 35 rural, 2 northern seats, with ±25% south and ±50% north | VERIFIED-SECONDARY (facts per Wikipedia and vLex snippets). "No requirement" = absence of authority found. |
| **If government uses an independent commission, executive interference with that commission's independent view can make the resulting map violate s.3.** | *Reference re the Final Report of the Electoral Boundaries Commission*, 2017 NSCA 10 (Jan. 24, 2017). The reference question asked whether s.1 of c.61, Acts of N.S. 2012 (which enacted the Final Report) violated s.3. The answer was yes. The AG's direction "forced the commission to sign a final report with electoral boundaries that did not represent the commission's authentic view of effective representation." The legislature could have redrawn the map itself, but "those prospects do not justify stifling the independent commission's view of effective representation." | VERIFIED-SECONDARY (Global News/CP, Formac, vLex summary, search summary of the court page). The full judgment was not read. |
| **Legislation that halts or derails the commission process is reviewable under s.3 and s.1. Unanimous passage does not shield it.** Courts will not police the detailed mechanics of map-drawing, but legislatures cannot adopt disproportionate measures. | *Quebec (AG) v. Lalande*, 2026 SCC 13 (Kasirer J.) | VERIFIED-SECONDARY (Torys, CBA National Magazine, Jurist, SCC Case in Brief, Elections Québec) |
| **A failure to create a minority-protecting district can itself breach s.3.** In Nova Scotia (Chéticamp), the court declared the House of Assembly Act provision invalid, suspended the declaration, and allowed about 20 months for a fix. | N.S. Supreme Court, Muise J., Nov. 2024. Neutral citation not found. | VERIFIED-SECONDARY (CBC; N.S. government release). Citation UNVERIFIED. |
| **Courts do not review the law-making process before a law is enacted. They review the law once it is passed.** | *Mikisew Cree First Nation v. Canada (Governor General in Council)*, 2018 SCC 40. Courts should rarely scrutinize law-making (separation of powers, parliamentary sovereignty, privilege). A post-enactment challenge can be determined by the courts. | VERIFIED-SECONDARY (SCC Case in Brief, Canadian Lawyer). Applying it to an Assembly committee is analogy, my analysis. |
| Courts generally will not set a legislature's timetable for a fix. | Later Dixon proceedings (Meredith J.): the court "cannot dictate to a Legislature the time frame" | VERIFIED-SECONDARY (weak: Canadian Parliamentary Review via search summary) |
| A constitutional floor on election frequency exists (Charter s.4, five-year maximum). It was not researched further. | Charter s.4 | UNVERIFIED (memory) |

---

## B. What Alberta statute requires

All EBCA text below is VERIFIED-PRIMARY, quoted verbatim in the repo files `preregistration/terms_of_reference.md` and `findings/terms_of_reference_audit.md` §1. **Every one of these rules is addressed to "the Commission".**

### B1. Districts (Part 2, Redistribution Rules)

- **s.12 Population data.** Default is the decennial census (s.12(3)). It is displaced by a more recent province-wide census (s.12(4)). The Commission "may, as it considers appropriate, use more recent information … in conjunction with" either (s.12(5)).
- **s.13 Number.** "The Commission shall divide Alberta into 89 proposed electoral divisions." The marginal note reads 2024 c17 s3.
- **s.14 Factors.** The Commission "shall take into consideration the requirement for effective representation as guaranteed by the Canadian Charter of Rights and Freedoms, and in doing so may take into consideration":
  - (a) sparsity, density and rate of growth of the population;
  - (b) communities of interest, including municipalities, regional and rural communities, Indian reserves and Metis settlements;
  - (c) geographical features;
  - (d) communication and transportation;
  - (e) understandable and clear boundaries;
  - (f) any other factors.
  - Compactness and contiguity are **not** listed.
- **s.15(1) Band.** No division may be more than 25% above or below the average.
- **s.15(2) Exception.** For "no more than 4" divisions, if "the Commission is of the opinion that at least 3" of these criteria exist, the division may be "as much as 50% below" the average:
  - (a) area over 20,000 km², or total surveyed area over 15,000 km²;
  - (b) more than 150 km from the Legislature Building in Edmonton to the nearest boundary, by the most direct highway route;
  - (c) no town over 8,000 people;
  - (d) contains an Indian reserve or Metis settlement;
  - (e) part of the boundary is coterminous with the provincial boundary.
  - It is permissive ("may") and gated by opinion. It allows deviation **below** the average only.
- **s.15(3).** Crowsnest Pass is not a "town" for the purpose of s.15(2)(c).

### B2. Process

- **s.2(1) Composition.**
  - Chair: appointed by the Lieutenant Governor in Council. Must be the Ethics Commissioner, the Auditor General, a post-secondary president, a judge or retired judge, or a person of similar stature.
  - Two members nominated by the Leader of the Opposition, in consultation with other opposition leaders.
  - Two members nominated by the Premier ("President of the Executive Council").
  - The four members are appointed by the Speaker. They must not be MLAs.
  - The **Chief Justice has no role.**
- **s.2(2).** The Chief Electoral Officer provides advice, information and assistance.
- **s.5 Timing.** A commission is appointed in the first session after every second general election, no sooner than 8 and no later than 10 years after the last one.
- **s.6(1).** Interim report to the Speaker within 7 months of appointment.
- **s.7(1).** The Commission "must hold public hearings both (a) before its report is submitted to the Speaker, and (b) after its report has been made public."
- **s.8(1).** The Commission "may … within 5 months" submit a final report.
- **s.9.** "If there is more than one report … the report of a majority of the members of the Commission is the report of the Commission, but if there is no majority, the report of the chair is the report of the Commission."
- **s.10 "Report to Assembly".** The heading is VERIFIED-SECONDARY (a table-of-contents snippet of the 2024 consolidation hosted by parliamentum.org). The **operative text is UNVERIFIED.**
- **How a report becomes law.** It has no legal effect by itself. Earlier commission transcripts (1995–96 and 2009) say the Assembly decides by resolution whether to "approve or approve with alterations" the proposals and then introduces a bill establishing the new divisions, which comes into force on proclamation. Status: VERIFIED-SECONDARY (historical). The current section number and wording are UNVERIFIED.

### B3. Electoral Divisions Act and the seat-count changes

- **The map in force today has 87 divisions.** It was enacted in December 2017 and used in 2019 and 2023 (VERIFIED-SECONDARY, Government of Alberta open-data pages). The citation SA 2017 c E-4.1 is UNVERIFIED, because sources name the statute inconsistently. If no new Electoral Divisions Act is enacted and proclaimed, the 87-seat Act governs the next election. That last point is my analysis; it is consistent with Wikipedia's note that new boundaries apply only "if the legislature implements" them.
- **The move from 87 to 89 was a 2024 amendment to the EBCA, not a 2025 change to the EDA.** This corrects the brief's premise. The amendment came through Bill 31, the *Justice Statutes Amendment Act, 2024* (introduced Nov. 5, 2024; marginal note 2024 c17 s3).
  - It also added "rate of growth" to s.14(a).
  - Per Wikipedia (weak), it removed the earlier consideration of municipal boundaries "wherever possible" and of community boundaries within Edmonton and Calgary.
  - Status: VERIFIED-SECONDARY (Alberta fact sheet, CBC, CTV); the "removed" details are weak.
- **Bill 32, *Electoral Boundaries Commission Amendment Act, 2026*.**
  - Introduced April 23, 2026 by Justice Minister Mickey Amery.
  - Section 13 is "amended by striking out '89 proposed electoral divisions' and substituting '91 proposed electoral divisions'" (first-reading text; assent line blank).
  - It was at Committee of the Whole as of the May 12–13, 2026 ABmunis update. The spring sitting was due to end about May 14, and the fall sitting starts October 27.
  - **I found no evidence of third reading or Royal Assent. Status unknown; it is a gap.**
  - Note (my analysis): Bill 32 changes the Commission's mandate. A 91-seat Electoral Divisions Act would fix the number by itself, whatever s.13 says.

### B4. What binds the Lunty committee and the advisory panel

- **Instrument: Government Motion 37.** Introduced April 16, 2026 and passed April 21, 2026 (Assembly committee page; ABmunis; Calgary Journal/CP). The April 20 Order Paper text, per the search summary, says the review is to be "expedited" and "would not require public hearings". The motion urges the government to introduce a bill amending s.13 to 91. Clause C(d) provides for engaging independent advisors. Per the UCP caucus and search summaries, the panel is to divide Alberta into 91 divisions and incorporate Recommendation 5 "subject to any modifications the independent advisory panel considers necessary". Status: VERIFIED-SECONDARY; the full motion text was not seen.
- **Deadlines.** The panel reports to the committee by Oct. 22, 2026. The committee reports to the Assembly by Nov. 2, 2026. Status: VERIFIED-SECONDARY (committee page; CTV). I found no report of delivery.
- **Members.** Six: Lunty (chair), de Jonge, Sawyer and Wiebe (UCP); Ganley and Gray (NDP). Rowswell has substituted for Sawyer. Status: VERIFIED-SECONDARY (Assembly committee page and transcripts via search).
- **Panel chair.**
  - Acting Chief Justice Dawn Pentelechuk declined the committee's May 4 request to circulate a call for a judicial chair, citing "the irregularity of this process". The CBA Alberta branch and the Law Society of Alberta also declined to take part.
  - Retired justice Brian O'Ferrall was later named chair. The NDP has questioned his UCP donations.
  - Status: VERIFIED-SECONDARY (Southern Alberta Newspapers/Bow Island Commentator; CTV).
- **What binds them legally.**
  - The EBCA's process rules (ss.2 and 5–9) and redistribution rules (ss.12–15) are addressed to "the Commission". They do not bind an Assembly committee or its advisors unless the motion adopts them. Whether GM37 incorporates Part 2 is **unknown; it is a gap.**
  - The committee works under the Assembly's own rules and the motion.
  - Only the eventual Electoral Divisions Act is reviewable, under s.3 (Mikisew, by analogy).
- **The 18-month readiness point is not a legal rule.** Elections Alberta says it needs "at least 1 1/2 years" to implement new ridings (VERIFIED-SECONDARY, CTV). The election is fixed for Oct. 18, 2027 (VERIFIED-SECONDARY, weak: Wikipedia). From a Nov. 2, 2026 report plus a bill, the window is about 11 months. Missing the readiness target creates no breach by itself.

---

## C. What courts have said (Alberta first)

1. **The 1991 Alberta Court of Appeal reference.**
   - Name and citation: *Reference re: Order in Council O.C. 91/91 in Respect of the Electoral Boundaries Commission Act*, 1991 ABCA 317 (CanLII). Status: VERIFIED-SECONDARY (as cited by ABlawg, Fluker, April 13, 2026). The reporter citation "(1991), 86 DLR (4th) 447" is UNVERIFIED.
   - Holding: **unresolved.** Wikipedia says the court found the proposed boundaries consistent with the Charter and with Carter, and that the government then scrapped the report and amended the Electoral Divisions Act in early 1991 to "Charter-proof" it. A search summary of ABlawg says the court "declined to make declarations on the Charter compliance" in these 1990s references. The sources conflict, so do not state a holding until the judgment is read.
2. **The 1994 Alberta Court of Appeal reference on the *Electoral Divisions Statutes Amendment Act, 1993*** (Bill 55, which enacted the Bogle committee map).
   - Judgment date: Oct. 24, 1994.
   - What it found: the boundaries complied with the Charter, but the court identified problems with the process. Committee members could not give a sufficient rationale for several boundaries and populations. The court noted that one of the smallest divisions was the one Bogle himself represented. It said a proper review was needed within the term of the sitting Legislature, which expired in 1997.
   - Status: VERIFIED-SECONDARY (weak: Wikipedia's Taber-Warner and Alberta-districts pages; Alberta Views opening).
   - The phrase "there is no permissible variation if there is no justification", attributed to Alberta Views in one search summary, is **UNVERIFIED**: an exact-phrase search failed. The citation "(1994) 119 DLR (4th) 1 (Alta CA)" (repo academic §2 and references) is **UNVERIFIED**.
   - Aftermath: Bill 20 (1995) introduced the present appointment model, a chair appointed by cabinet from a list that includes judges (VERIFIED-SECONDARY). A new commission reported in 1996.
3. **Carter (SCC 1991).** See A1. The SCC allowed the appeal from the Saskatchewan Court of Appeal, which had found a breach.
4. ***Dixon v. British Columbia (AG)* (1989), 59 DLR (4th) 247 (BCSC), McLachlin C.J.S.C.**
   - BC's distribution, with different bases for mainland and island and urban/rural/remote categories, violated s.3 and was not saved by s.1. The government did not appeal.
   - The often-quoted "±25% would probably resist challenge" comes only from Alberta committee transcripts (weak).
   - Status: VERIFIED-SECONDARY (vLex appendix; Canadian Parliamentary Review). The exact wording is not seen.
5. **2017 NSCA 10 (Nova Scotia).** See A2. This is the closest analogue on process: interference with an independent commission.
   - How it differs from Alberta 2026: in NS the executive directed a sitting commission mid-process. In Alberta 2026 the commission finished, both reports were tabled intact, and the Legislature declined to proceed with them and created a different body.
   - The NSCA said a legislature redrawing the map itself remained possible. So the case is not authority that Motion/GM37 is unconstitutional. It is authority that, where the state relies on an "independent" body, stifling that body's view can taint the enacted map under s.3.
   - Status of the comparison: my analysis.
   - Aftermath (VERIFIED-SECONDARY): the government accepted the opinion, but the 2017 election ran on the 2012 map. A later commission restored minority districts.
6. ***Raîche v. Canada (AG)*, 2004 FC 679, Shore J. (May 11, 2004).**
   - The court set aside the federal commission's decision moving Allardville and parts of Saumarez and Bathurst from Acadie–Bathurst to Miramichi, and suspended the declaration of invalidity for one year. It found **no** s.3 violation.
   - Defect: the commission applied the federal Act narrowly. It kept variance under 10% but did not weigh community of interest.
   - The fix came through an Inquiries Act commission and then Parliament's Bill C-36 (2005).
   - Status: VERIFIED-SECONDARY (vLex, Federal Court Reports headnote, House PROC report, Senate report). The repo's claim that the court found Official Languages Act Part VII violations is UNVERIFIED (seen only in a Senate committee finding).
   - It is a trial-level decision under a federal statute: persuasive, not binding.
7. **N.S. Supreme Court, Chéticamp (Nov. 2024).** See A2. A court can find that a *missing* protected district breaches s.3.
8. ***Quebec (AG) v. Lalande*, 2026 SCC 13.** See §0 item 3 and A2.
   - Sequence: the Superior Court found an infringement but justified it (May 29, 2025). The Court of Appeal struck the law down (Dec. 1, 2025). The SCC dismissed the appeal.
   - Alberta's Attorney General filed an intervener factum (April 10, 2026). Its content was not seen.
   - Status: VERIFIED-SECONDARY.
9. ***Ontario (AG) v. Working Families*, 2025 SCC 5.** s.3 includes an informed vote, and s.33 cannot shield a s.3 breach. VERIFIED-SECONDARY.
10. ***Mikisew Cree*, 2018 SCC 40.** No pre-enactment judicial supervision of law-making. VERIFIED-SECONDARY.
11. ***Cassista v. Canada*, 2014 FC 398.** Not found in any search this session either. Recommend deleting it, not just banner-flagging it. Status: UNVERIFIED (T6).
12. ***Deschênes*, 2025 FC 343.** A challenge to the federal commission's elimination of a Quebec riding. Existence only; the outcome was not seen. VERIFIED-SECONDARY (existence).

---

## D. What the law does NOT require, item by item against the 2026 process

| # | Gap (not required) | Basis | 2026 process | What still applies |
|---|---|---|---|---|
| 1 | The Assembly does not have to adopt a commission report. | EBCA: a report takes effect only through an Electoral Divisions Act (B2) | Both commission maps were set aside: lawful. | The current 87-seat Act stays in force until replaced. |
| 2 | A commission does not have to draw the enacted map. The Legislature may legislate its own. | NSCA 2017 noted this. Alberta 1992–93 did it. Quebec did it in June 2026 (127 seats). | A committee and advisory panel is a lawful vehicle. | s.3 review of whatever is enacted (ABCA 1994 reviewed a committee-drawn map). |
| 3 | No public hearings are required of an Assembly committee. | EBCA s.7 binds only the Commission. GM37 says hearings are not required. | No hearings on the 91-seat map. | Hearings are not a legal condition, but without them the record the committee can later rely on is thinner (analysis). |
| 4 | No independence requirement applies to a legislative committee. | No authority requires it. EBCA s.2 binds the Commission. | 4 UCP to 2 NDP committee; a panel styled "independent" by motion. The acting Chief Justice declined, citing "irregularity". | NSCA 2017: where the state relies on an independent body, stifling its view can taint the map under s.3. If the panel is directed, its "independence" is a fact question (analysis). |
| 5 | No constitutional seat number. | Carter; EBCA s.13 is ordinary statute. | 91 seats: a policy choice. Bill 32's status is unknown. | Each district's deviation must still be justifiable. |
| 6 | The ±25% band and s.15(2) do not bind the Legislature or a committee. | EBCA ss.15(1)–(2) are addressed to "the Commission". | Whether GM37 imports them is unknown (gap). | Carter justification. The 1994 ABCA criticized unexplained populations even in a map it upheld. |
| 7 | No statutory duty to give reasons for an enacted map. | No provision found. | The committee report's content is unknown. | Practically decisive: the 1994 ABCA faulted the absence of rationale. Under Carter the state must justify deviations if challenged. |
| 8 | Recommendation 5 binds no one. | It is a chair-only addendum (repo p. 66), and GM37 lets the panel modify. | The government cited R5 as its basis. | Only as a fidelity test (audit X1), not law. See §H. |
| 9 | No legal 18-month deadline. | It is Elections Alberta guidance. | About 11 months remain from Nov. 2, 2026. | If nothing passes, 2027 runs on the 2017 map. Whether an outdated map raises a Lalande-type s.3 issue is untested (analysis, not a holding). |
| 10 | No "gerrymandering" test and no partisan-intent element. | No Canadian test found. s.3 asks about effective representation. | Partisan effect is evidence only. | Carter / Raîche reasonableness. |
| 11 | No pre-enactment court review of the committee. | Mikisew 2018 SCC 40 (analogy). | The committee's process is shielded while ongoing. | A challenge after enactment is available. |
| 12 | (Not a gap) s.33 cannot be used. | Charter s.33; Working Families. | n/a | s.3 is always reviewable. |

---

## E. Where the site's current legal copy is wrong, outdated, overstated, or missing something

**/law page:** `viewer/src/routes/law/+page.svelte`

| Lines | Problem | Fix | Severity |
|---|---|---|---|
| 183–185 | "Section 12 of the Act also permits referring a commission's recommendations to a legislative committee … That is the door the government used on April 16" | **Wrong.** s.12 is population data. The committee came from Government Motion 37 (passed April 21 per the Assembly page), not from the EBCA. | High |
| 180–182 | "Most provinces make a commission's map effective unless the legislature actively overrides it." | **Unsupported or overstated.** Nova Scotia requires legislation (verified). Manitoba appears automatic (verified, weak). Quebec's commission sets the map, but the National Assembly legislated its own in June 2026. BC and Saskatchewan were not checked. Say "some jurisdictions" and name them. | Medium |
| 104–112 | Raîche: "remedy was referral back to the commission, not boundaries struck down"; "'reasonable commission' review" | **Imprecise.** The court set aside the commission's decision and suspended invalidity for a year. The fix came via an Inquiries Act commission and then Parliament (Bill C-36). Replace "reasonable commission" with Carter's test: "could reasonable people, applying the right principles, have drawn the lines this way?" | Medium |
| 83–84 | "McLachlin J. explained (at para. 33)" | The pinpoint is pending T6. Drop the paragraph number until verified. | Low |
| whole page | **Missing:** Alberta's own 1991 and 1994 references and the 1992 committee precedent; NSCA 2017; Lalande 2026; s.33 cannot override s.3; EBCA rules bind the Commission, not the Legislature; Mikisew. | Add (see §F). | High |

**`viewer/src/lib/i18n/locales/en.ts`**

| Key (line) | Problem | Fix | Severity |
|---|---|---|---|
| `anomalous_p2` (653) | "no recorded precedent in post-Confederation redistricting … No other Canadian province has transferred redistricting authority … to a government-controlled legislative committee" | **Wrong.** In Alberta in 1992 the commission report was thrown out and a PC-only committee of MLAs drew the 1993 map. Rewrite as "the first time since Alberta's 1992 committee, which the Court of Appeal criticized in 1994". | High |
| `anomalous_p1` (651) | "settled on a single model"; "Other Canadian jurisdictions take the opposite default" | Overstated. Same fix as /law lines 180–182. | Medium |
| `framework_p1` (656) | "Population parity is the primary consideration" | Carter: relative parity is "a prime condition" of effective representation, and deviations need justification. Keep the quote "not equality of voting power per se" only after checking it against the judgment (the repo text matches; not independently seen). | Low |
| `framework_p2` (658) | "systematic impairment of one identifiable group's ability to elect proportionate representation is the pattern that s.3 challenges target" | **Misstates s.3.** No proportional or group-outcome right was found. Carter's concern is undue dilution of votes without justification. Raîche is "the leading Canadian authority": overstated (trial level, federal statute, no s.3 breach). | High |
| `framework_p3` (660) | Says only that the EBCA does not prohibit a parallel body. | Incomplete. Add: (a) EBCA rules bind the Commission only; (b) NSCA 2017; (c) Lalande; (d) the 1994 ABCA faulted a committee map for missing rationale; (e) review comes after enactment. | Medium |
| `intro` (633) / `intro_b` (635) | "Motion 19 … April 16 … five MLAs — three UCP, two NDP"; "Panel … under Government Motion 37" | **Conflicts with the Assembly page:** GM37 created the committee (passed April 21), with six members (4 UCP, 2 NDP). Check Votes and Proceedings for April 16 and 21 before keeping "Motion 19" or "44–36". Also: "the panel draws on submissions the original commission gathered" is unverified. | High |
| `quebec_p1`/`quebec_p2` (663–665) | "the independent body has the last word"; "cannot be … bypassed" | **Outdated.** In 2024 Quebec's legislature suspended the CRE (struck down: Lalande, 2026 SCC 13). In June 2026 it legislated its own 127-seat map. The contrast now cuts both ways. | High |
| `r5_test` (648) | "must meet all four conditions … Failing any one means …" | Condition (d) is "consider restoring", not "restore". See §H. | Medium |

**Repo documents (not site copy, but sources for it)**

| File / line | Problem | Severity |
|---|---|---|
| `reports/academic/report_academic.md` §5.9.1 (1996); `findings/procedural_analysis.md` D1 (16, 27) | "chair nominated by the Chief Justice", "ss. 3–5". Per s.2(1)(a) the chair is appointed by the Lieutenant Governor in Council. Already flagged in `terms_of_reference_audit.md` §2.1 but never fixed in these files. | High |
| `procedural_analysis.md` D1 (37) | "section 15 of the Act allows the Legislative Assembly to amend the commission's proposals". s.15 is the variance rule. | High |
| `procedural_analysis.md` D4 (66) | "Ontario 1996 … The Supreme Court upheld the approach". No source found. UNVERIFIED: remove or verify. | Medium |
| `procedural_analysis.md` D4 (76); academic §5.9.3 (2032) | "first instance" / "No Canadian provincial redistribution cycle … involves the government both rejecting a completed commission product and reassigning the drafting authority". Contradicted by Alberta 1992. | High |
| academic §5.9.2 (2001) | "five MLAs (three UCP, two NDP)". The Assembly page lists 6 (4 UCP, 2 NDP). | Medium |
| academic §5.9.3 / §5.9.5 (2032–2243) | SCC reasons "pending"; "*Coalition de l'Outaouais*"; "doctrinal implication 1" says legislatures "cannot block … even when justified on regional-protection grounds". Outdated and overstated: Lalande turned on minimal impairment and pointed to a narrower regional protection as acceptable. Quebec then legislated 127 seats. | High |
| academic App. F (3154) | Names the minority commissioners "Sela Clark, Nadia Samson, Sandra Evans, David Martin". The real names are Greg Clark, Susan Samson, John Evans KC and Dr. Julian Martin (report p. 1, in repo). The minority is two people, and Clark is a majority member. This is an accuracy and defamation-posture (D3) problem. | High |
| academic §2 (322) and references (2848) | Cassista is still unlocated; drop it. The 1994 ABCA citation "119 DLR (4th) 1" is unverified. | Medium |
| `findings/ebc_s15_selective_application.md` §1 (25), §9 (132) | The s.15(2) "quote" is not the statutory text (compare `terms_of_reference.md` §3d). "s.35 Charter" should be s.35 of the Constitution Act, 1982. | Medium |
| `docs/act_amendment_proposal.md` §1.2 (131–141) | "variances inside ±25% … presumptively compliant with s. 3" is overstated: Carter set no presumption. "*Friends of Democracy v Canada*, 2003 ABQB" is UNVERIFIED. "1991 ABCA 317" is consistent with ABlawg. | Medium |
| `findings/checklist_baseline_scoring.md` X1 (158–161); academic X1 (1765) | "R5 binds the November committee"; "(d) Restore Clearwater … district". R5 binds no one, and (d) says "consider". | Medium |

---

## F. Plain-language draft (about 700 words)

> **What the law requires — and what it doesn't**
>
> **The Constitution.** Section 3 of the Charter gives every citizen the right to vote. The Supreme Court of Canada has said this means more than casting a ballot. It means "effective representation."
>
> Voters in different districts should have roughly equal voting power. That is the starting point. It is not a strict rule of one person, one vote. A district can be smaller or larger for a good reason, such as geography, community history, shared local interests, or giving a minority community a real voice. The reason has to be real, and the gap cannot be larger than the reason supports.
>
> Courts use a generous test. They ask whether reasonable people, applying these principles, could have drawn the lines this way. Courts rarely strike down maps.
>
> No government can switch this right off. The Charter's notwithstanding clause does not cover section 3.
>
> Courts also look at how a map gets made. In 2017, Nova Scotia's Court of Appeal found a map unconstitutional. The government had pushed an independent commission to change its recommendations, and the court said the final map did not reflect the commission's own view. In 2026, the Supreme Court of Canada struck down a Quebec law that paused Quebec's commission to save rural ridings. It said Quebec could have protected those ridings in a narrower way. A unanimous vote did not save the law.
>
> **Alberta's law.** The *Electoral Boundaries Commission Act* sets the rules for Alberta's commission:
>
> - **Who sits on it.** A chair appointed by cabinet from a short list that includes judges. Two members nominated by the Premier and two by the Opposition, all appointed by the Speaker.
> - **Hearings.** Public hearings before and after a draft map.
> - **Deadlines.** A draft within seven months. A final report within five months after that.
> - **Seats.** 89 seats. A bill to raise this to 91 was introduced in April 2026.
> - **Population.** Every district within 25 per cent of the average. Up to four remote districts can go as low as 50 per cent below, if they meet three of five tests.
> - **Effective representation.** The commission must consider it, and it may weigh other factors.
>
> The 2025–26 commission followed these rules. Both of its maps fit inside them.
>
> **What the law doesn't require.** Much of this rulebook binds only the commission.
>
> - The Legislature does not have to adopt the commission's map. A commission report becomes law only if MLAs pass a bill.
> - The hearings, the deadlines and the 25 per cent band apply to the commission. When MLAs pass their own boundaries law, the only hard limit is the Charter.
> - A committee of MLAs does not have to hold public hearings. The motion that created the Lunty committee says its review is expedited and does not require them.
> - Nothing requires the committee to be independent, to publish a draft, or to explain its choices.
> - The chair's Recommendation 5, which the government cited, binds no one.
> - Elections Alberta says it needs about 18 months to prepare new ridings. That is a planning need, not a legal deadline.
> - Courts do not step into the Legislature's work while it is under way. A challenge can come only after a law passes.
>
> **This has happened before.** In 1992, Alberta's commission deadlocked over mixed urban–rural ridings. The government set its report aside and gave the job to a committee of MLAs. The Opposition refused to take part. That committee's map was used in the 1993 election.
>
> In 1994, the Court of Appeal let that map stand. It also criticized the committee for failing to explain several of its boundaries, and said a proper review was needed before long. Alberta then rewrote its law to create the commission system used today.
>
> **What this means in November.** Lawful does not mean beyond challenge. The committee's map will face the same test as any map: does it give voters effective representation, and are its gaps in population justified?
>
> Reasons matter. A map that comes with clear explanations is easier to defend. A map without them leaves the government to explain itself later, in court.
>
> This audit will score the map and the process against these standards. It will not decide whether the map is constitutional. That is a job for the courts.

**Sentences resting only on secondary or weak sources.** Check these before publishing:

- the 1992–94 paragraph (Wikipedia and Alberta Views; the 1994 judgment was not read);
- "the final map did not reflect the commission's own view" (NSCA, via a secondary quote);
- "does not require them [hearings]" (Order Paper, via search summary);
- the description of Lalande (law-firm and CBA summaries; the SCC reasons were not read).

---

## G. Citation table

Repo paths are relative to `/home/user/alberta-electoral-boundaries-audit/`.

| # | Authority | Claim supported | Source | Status |
|---|---|---|---|---|
| 1 | Charter s.3 | Text of the right to vote | `preregistration/terms_of_reference.md` §3 (commission report p. 15) | VERIFIED-PRIMARY (via repo) |
| 2 | Charter s.33 | Override limited to s.2 and ss.7–15 | https://www.justice.gc.ca/eng/csj-sjc/rfc-dlc/ccrf-ccdl/check/art33.html | VERIFIED-SECONDARY |
| 3 | Constitution Act, 1982 s.45 | Text; no link to redistribution found | https://en.wikisource.org/wiki/Constitution_Act,_1982/Part_V ; https://www.constitutionalstudies.ca/2021/08/provincial-constitutions-what-are-they-and-how-do-we-amend-them/ | VERIFIED-SECONDARY (text); application UNVERIFIED |
| 4 | Charter s.4 | Five-year maximum | memory | UNVERIFIED |
| 5 | *Reference re Prov. Electoral Boundaries (Sask.)*, [1991] 2 SCR 158 | Effective representation; 6–3; factors; scheme fixed by legislature upheld | https://en.wikipedia.org/wiki/Reference_re_Provincial_Electoral_Boundaries_(Sask) ; https://www.constitutionalstudies.ca/?p=8563 ; https://ca.vlex.com/vid/ref-re-prov-electoral-680566509 | VERIFIED-SECONDARY |
| 6 | Same | "Relative parity … prime condition"; "practical impossibility or the provision of more effective representation" | https://redecoupage-redistribution-2022.ca/com/on/phrg/othaut/northon/getCmt_e.aspx?cmt=cmt182 ; Wikipedia (above) | VERIFIED-SECONDARY (quoted wording) |
| 7 | Same | "better government of the …" | https://parliamentum.org/wp-content/uploads/2024/09/3.-nova-scotias-proposal.pdf (truncated) | UNVERIFIED (incomplete) |
| 8 | Same, para. 26 / 33 pinpoints | Used on /law and in academic App. F | repo only | UNVERIFIED (T6) |
| 9 | Same | "not equality of voting power per se, but … 'effective representation'" | `docs/act_amendment_proposal.md` §1.2; `en.ts` framework_p1 | UNVERIFIED as exact wording (substance VERIFIED-SECONDARY) |
| 10 | *Dixon v. BC (AG)* (1989), 59 DLR (4th) 247 (BCSC) | s.3 breach, not saved by s.1; McLachlin C.J.S.C. | https://ca.vlex.com/vid/appendix-3-fundamamental-jurisprudence-869049315 ; https://revparl.ca/english/issue_param_129_art_817.html | VERIFIED-SECONDARY |
| 11 | Dixon (later, Meredith J.) | Court cannot dictate legislative time frame | https://revparl.ca/english/issue_param_129_art_817.html | VERIFIED-SECONDARY (weak) |
| 12 | Dixon | "±25% would probably resist challenge" | Alberta committee transcripts (docs.assembly.ab.ca eb89) | UNVERIFIED (transcript paraphrase only) |
| 13 | *Reference re: O.C. 91/91 … EBCA*, 1991 ABCA 317 | Name and neutral citation | https://ablawg.ca/?p=15049 | VERIFIED-SECONDARY |
| 14 | Same | Holding (consistent with Charter vs. declined declarations) | https://en.wikipedia.org/wiki/List_of_Alberta_provincial_electoral_districts ; ABlawg | UNVERIFIED (sources conflict) |
| 15 | Same, (1991) 86 DLR (4th) 447 | Reporter citation | memory | UNVERIFIED |
| 16 | 1994 ABCA reference, *Electoral Divisions Statutes Amendment Act, 1993* | Oct. 24, 1994; upheld; process criticized; no rationale; review needed by 1997 | https://en.wikipedia.org/wiki/Taber-Warner ; https://albertaviews.ca/knowing-draw-line/ ; Wikipedia list (above) | VERIFIED-SECONDARY (weak) |
| 17 | Same, (1994) 119 DLR (4th) 1 | Reporter citation | `reports/academic/report_academic.md` §2, refs | UNVERIFIED |
| 18 | Same | "no permissible variation if there is no justification" | one search summary of Alberta Views; exact-phrase search failed | UNVERIFIED |
| 19 | Alberta 1992 Select Special Committee (Motion 24, July 2, 1992; Bogle) | Commission report thrown out; 4 PC MLAs; opposition boycott; map used in 1993 | https://albertaviews.ca/knowing-draw-line/ ; https://en.wikipedia.org/wiki/Taber-Warner | VERIFIED-SECONDARY |
| 20 | Bill 55 (1993), *Electoral Divisions Statutes Amendment Act, 1993* | Enacted committee map; "effective representation" stated aim | https://docs.assembly.ab.ca/LADDAR_files/docs/bills/bill/legislature_22/session_4/19920319_bill-055.pdf ; Hansard https://docs.assembly.ab.ca/LADDAR_files/docs/hansards/han/legislature_22/session_4/19930126_2000_01_han.pdf | VERIFIED-SECONDARY |
| 21 | Bill 20 (1995) EBCA amendment | Chair appointed by LGIC from a list incl. judges | https://docs.assembly.ab.ca/LADDAR_files/docs/bills/bill/legislature_23/session_3/19950213_bill-020.pdf | VERIFIED-SECONDARY |
| 22 | *Reference re Final Report of the EBC*, 2017 NSCA 10 | s.3 breach; AG interference with "authentic view"; legislature could redraw; reference question re s.1 c.61 2012 | https://ca.vlex.com/vid/nova-scotia-691127873 ; https://www.formac.ca/starrspoint/?p=2664 ; https://globalnews.ca/news/3202760/nova-scotia-acadians-win-key-court-battle-over-french-speaking-ridings/ ; https://amp.cbc.ca/news/canada/nova-scotia/commission-electoral-boundaries-court-acadian-african-nova-scotian-1.4091075 ; court page (not fetched) https://decisions.courts.ns.ca/nsc/nsca/en/230165/1/document.do | VERIFIED-SECONDARY |
| 23 | N.S. Supreme Court (Muise J.), Nov. 2024, Chéticamp | Missing protected district breached s.3; suspended declaration; ~20 months | https://www.cbc.ca/lite/story/1.7383348 ; https://news.novascotia.ca/en/2025/02/18/province-appoint-special-electoral-boundaries-commission-cheticamp | VERIFIED-SECONDARY (citation UNVERIFIED) |
| 24 | *Raîche v. Canada (AG)*, 2004 FC 679 (Shore J.) | Set aside; one-year suspension; no s.3 breach; Carter test wording; Bill C-36 follow-up | https://ca.vlex.com/vid/681460337 ; https://recueil.cmf-fja.gc.ca/fja-cmf/j/en/331633/1/document.do ; https://ourcommons.ca/documentviewer/en/38-1/PROC/report-19 ; https://sencanada.ca/Content/SEN/Committee/381/lega/rep/rep05feb05-e.htm | VERIFIED-SECONDARY |
| 25 | Raîche | Official Languages Act Part VII violation found by the court | `report_academic.md` §2 | UNVERIFIED (Senate report only) |
| 26 | *Quebec (AG) v. Lalande*, 2026 SCC 13 | 7–2; s.3 breach; failed minimal impairment; unanimity no shield; Kasirer J.; reasons May 1 | https://www.torys.com/en/our-latest-thinking/publications/2026/05/quebec-v-lalande ; https://nationalmagazine.ca/en-ca/articles/hot-topics-in-law/2026/supreme-court-quashes-quebec-legislature-s-plan-to-delay-electoral-boundary-redistribution ; https://www.jurist.org/news/2026/05/canada-high-court-finds-quebec-suspension-of-independent-electoral-map-review-unconstitutional/ ; https://scc-csc.ca/judgments-jugements/cb/2026/42152/ | VERIFIED-SECONDARY |
| 27 | Quebec act of June 12, 2026 | New map; 125 → 127 seats | https://www.electionsquebec.qc.ca/en/electoral-maps/review-of-quebecs-electoral-map/ | VERIFIED-SECONDARY |
| 28 | AG Alberta intervener factum, SCC 42152 | Alberta intervened in Lalande | https://www.scc-csc.ca/pdf/case-documents/42152/FM050_Intervener_Attorney-General-of-Alberta.pdf | VERIFIED-SECONDARY (existence; content not seen) |
| 29 | *Ontario (AG) v. Working Families*, 2025 SCC 5 | s.3 informed vote; s.33 unavailable; 5–4 | https://www.torys.com/en/our-latest-thinking/publications/2025/03/spending-limits-on-third-party-political-advertising-violate-the-charter ; https://www.yorku.ca/osgoode/thecourt/2025/08/05/the-right-to-know-scc-strikes-down-election-spending-limits-for-third-parties-in-working-families/ | VERIFIED-SECONDARY |
| 30 | *Mikisew Cree*, 2018 SCC 40 | No pre-enactment review of law-making; post-enactment challenge possible | https://scc-csc.ca/judgments-jugements/cb/2018/37441/ ; https://www.canadianlawyermag.com/legalfeeds/author/elizabeth-raymer/parliament-has-no-duty-to-consult-first-nations-in-making-laws-scc-16329/ | VERIFIED-SECONDARY |
| 31 | *Cassista v. Canada*, 2014 FC 398 | (none; not found) | search this session; T6 | UNVERIFIED |
| 32 | *Deschênes*, 2025 FC 343 | Existence of a 2025 federal boundary challenge | https://decisions.fct-cf.gc.ca/fc-cf/decisions/en/527573/1/document.do | VERIFIED-SECONDARY (existence) |
| 33 | EBCA s.2(1), 2(2) | Composition; CEO support | `findings/terms_of_reference_audit.md` §1 | VERIFIED-PRIMARY (via repo) |
| 34 | EBCA s.5, 6(1), 7(1), 8(1), 9 | Timing; hearings; reports; majority rule | same | VERIFIED-PRIMARY (via repo) |
| 35 | EBCA s.10 | Heading "Report to Assembly" | https://parliamentum.org/wp-content/uploads/2026/04/electoral-boundaries-commission-act-2024-r.s.a.-2000-c.e-3.pdf (ToC snippet) | Heading VERIFIED-SECONDARY; text UNVERIFIED |
| 36 | EBCA (legislative step) | Assembly "approve or approve with alterations" by resolution, then a bill | https://docs.assembly.ab.ca/LADDAR_files/docs/committees/ebc9596/legislature_23/session_4/19960423_1200_01_ebc9596.pdf ; https://docs.assembly.ab.ca/LADDAR_files/docs/committees/ebc09/legislature_27/session_2/20090922_1503_01_ebc09.pdf | VERIFIED-SECONDARY (historical); current text UNVERIFIED |
| 37 | EBCA s.12 | Population data (not committee referral) | `preregistration/terms_of_reference.md` §4 | VERIFIED-PRIMARY (via repo) |
| 38 | EBCA s.13, 14, 15(1)–(3) | 89 seats; factors; ±25%; s.15(2) criteria; Crowsnest | `preregistration/terms_of_reference.md` §3a–3e | VERIFIED-PRIMARY (via repo) |
| 39 | SA 2024 c17 (Bill 31, *Justice Statutes Amendment Act, 2024*) | 87 → 89; growth rate added | https://www.alberta.ca/system/files/jus-fact-sheet-bill-31-justice-statutes-amendment-act.pdf ; https://www.cbc.ca/lite/story/1.7374605 | VERIFIED-SECONDARY |
| 40 | Same | Removed municipal / city-community boundary considerations | https://en.wikipedia.org/wiki/2026_Alberta_electoral_redistribution | VERIFIED-SECONDARY (weak) |
| 41 | Electoral Divisions Act (2017; 87 divisions) | Map in force; used 2019 and 2023 | https://open.alberta.ca/opendata/electoral-division | VERIFIED-SECONDARY; citation "SA 2017 c E-4.1" UNVERIFIED |
| 42 | Bill 32 (2026), *EBC Amendment Act, 2026* | s.13 89 → 91; introduced April 23 by Amery; Committee of the Whole as of May 12–13 | https://docs.assembly.ab.ca/LADDAR_files/docs/bills/bill/legislature_31/session_2/20251023_bill-032.pdf ; https://www.alberta.ca/system/files/news-updating-electoral-boundaries-20260423-langes.pdf ; https://www.abmunis.ca/news/update-legislature-may-13-2026 | VERIFIED-SECONDARY; passage/assent UNVERIFIED |
| 43 | Government Motion 37 (2026) | Committee established April 21; expedited; no hearings required; urge 91-seat bill; panel clause C(d) | https://www.assembly.ab.ca/assembly-business/committees/ceb ; https://docs.assembly.ab.ca/LADDAR_files/docs/houserecords/op/legislature_31/session_2/20260420_1200_01_op.pdf ; https://www.abmunis.ca/news/update-legislature-april-22-2026 ; https://calgaryjournal.ca/2026/04/21/government-motion-passes-to-take-second-run-at-redrawing-albertas-electoral-ridings/ | VERIFIED-SECONDARY (full text not seen) |
| 44 | GM37 | Panel to incorporate R5 "subject to any modifications the independent advisory panel considers necessary" | https://unitedconservativecaucus.ca/statement-on-the-electoral-boundaries-commission-report-2/ ; search summary | VERIFIED-SECONDARY (partisan source; exact text not seen) |
| 45 | "Motion 19", April 16, 44–36 | Repo/site claim | `findings/hansard_april16_motion19.md`; `en.ts` intro; only corroboration https://gdeltcloud.com/events/veto-in-edmonton--cameoplus_b11b5bf3 | UNVERIFIED (conflicts with item 43) |
| 46 | Committee membership (6) | Lunty, de Jonge, Sawyer, Wiebe (UCP); Ganley, Gray (NDP) | https://www.assembly.ab.ca/assembly-business/committees/ceb ; CEB transcripts e.g. https://docs.assembly.ab.ca/LADDAR_files/docs/committees/CEB/legislature_31/session_2/20260504_0930_01_ceb.pdf | VERIFIED-SECONDARY |
| 47 | Panel appointments (June 9, 2026) | Two Premier, two Opposition nominees | https://www.assembly.ab.ca/about/news-and-announcements/2026/06/09/committee-appoints-members-to-electoral-boundaries-advisory-panel | VERIFIED-SECONDARY |
| 48 | Pentelechuk letter; CBA/LSA declined; O'Ferrall chair | "irregularity of this process" | https://bowislandcommentator.com/news/2026/05/28/chief-justice-cites-integrity-issues-refuses-to-suggest-electoral-boundaries-chair/ ; https://www.ctvnews.ca/edmonton/article/former-alberta-judge-tapped-to-chair-panel-re-drawing-electoral-boundaries/ | VERIFIED-SECONDARY |
| 49 | Panel due Oct. 22; committee due Nov. 2 | Deadlines | https://www.assembly.ab.ca/assembly-business/committees/CEB ; CTV (above) | VERIFIED-SECONDARY |
| 50 | Elections Alberta readiness | "at least 1 1/2 years" | https://www.ctvnews.ca/calgary/article/redraw-of-electoral-boundaries-would-present-challenging-timeline-elections-alberta/ | VERIFIED-SECONDARY |
| 51 | Fixed election date Oct. 18, 2027 | Timeline | https://en.wikipedia.org/wiki/32nd_Alberta_general_election | VERIFIED-SECONDARY (weak) |
| 52 | Manitoba automatic effect; N.S. requires legislation | Comparative default | https://www.mysteinbach.ca/news/?p=2948 ; https://news.novascotia.ca/en/2012/10/25/province-implements-electoral-boundaries-report | VERIFIED-SECONDARY (BC/SK UNVERIFIED) |
| 53 | Recommendation 5 text (a)–(d) | "should … d) consider restoring …" | `findings/chair_recommendation_5_analysis.md` (report pp. 66–67) | VERIFIED-PRIMARY (via repo) |
| 54 | *Baker v. Canada*, [1999] 2 SCR 817, para. 75 | "alert, alive and sensitive"; not determinative; reasons show whether considered | https://legallibrary.crin.org/mavis-baker-v-canada-minister-of-citizenship-and-immigration/ ; https://meurrensonimmigration.com/the-best-interests-of-a-child/ | VERIFIED-SECONDARY (pinpoint per secondary) |
| 55 | *Legault*, 2002 FCA 125 | Weight is for the decision-maker | cited in a secondary source; citation from memory | UNVERIFIED (citation) |
| 56 | *Canada (MCI) v. Vavilov*, 2019 SCC 65, para. 128 | Failure to "meaningfully grapple" with key issues; no duty to address every argument | https://meurrensonimmigration.com/the-supreme-court-of-canada-decision-in-vavilov/ ; https://www.lerners.ca/?p=19057 | VERIFIED-SECONDARY |
| 57 | Ontario *Planning Act* "have regard to" vs "be consistent with" | Gradient of adherence | https://archives.york.ca/councilcommitteearchives/pdf/-9.pdf ; https://administrativelawblog.harpergrey.com/tag/have-regard-to/ | VERIFIED-SECONDARY (professional view, not a holding) |
| 58 | General proposition "consider = genuine weighing, not adoption" as a cross-context rule | §H | no single leading case verified | UNVERIFIED (Baker/Vavilov are analogues) |

---

## H. How Canadian law reads a duty to "consider", and how to score Recommendation 5(d)

**The text** (VERIFIED-PRIMARY, via `findings/chair_recommendation_5_analysis.md`). "…restoration of the two electoral divisions **should**: a) have no impact on … b) have no impact on … c) result in … reverting … and d) **consider restoring** an electoral division mostly consisting of Clearwater County and western Mountain View County as an electoral division with s. 15(2) status under the Act."

The main clause separately asks the Assembly to "restore the two electoral divisions that this Commission has removed" and keep "the rest of the province as we propose … to the extent possible."

**H1. Plain meaning.** "Should … consider restoring" asks for consideration. It does not ask for a result. The thing that "should" happen in (d) is that the option is weighed. Items (a)–(c) describe outcomes. Item (d) describes a step of thought. In ordinary English, you can consider something and decline it.

**H2. Interpretive reading.** Canadian drafting uses a gradient of verbs:

- "shall / must [do]" requires the result;
- "be consistent with" requires close adherence;
- "shall have regard to / take into account / consider" requires the matter to be weighed;
- "may consider" permits it.

The EBCA itself uses this structure. The Commission "**shall** take into consideration the requirement for effective representation … and … **may** take into consideration" factors (a)–(f) (s.14; VERIFIED-PRIMARY). Ontario planning practice treats "have regard to" as requiring less adherence than "be consistent with" (VERIFIED-SECONDARY; a professional view, not a holding).

In administrative law, a duty to consider a matter means the decision-maker must be "alert, alive and sensitive" to it and examine it with real attention. The matter is not determinative, and its weight is for the decision-maker (*Baker*, para. 75: VERIFIED-SECONDARY; the weight point via *Legault*, citation UNVERIFIED). Courts find the evidence in the reasons:

- *Baker* was unreasonable because its reasons did not show the officer was alive to the children's interests (VERIFIED-SECONDARY).
- A failure to "meaningfully grapple" with a key issue may show the decision-maker was not alert to it, but reasons need not address everything (*Vavilov*, para. 128: VERIFIED-SECONDARY).

I could not verify a single leading case stating "consider = genuine good-faith weighing, not adoption" as a general rule across contexts. *Baker* and *Vavilov* are the strongest verified analogues (UNVERIFIED as a general proposition).

Three caveats:

1. These are judicial-review standards for statutory decision-makers. R5 is a recommendation in a commission addendum, not law.
2. The committee and panel act under an Assembly motion, inside the legislative process, which courts do not supervise before enactment (*Mikisew*, by analogy). So X1 is a **fidelity test**: did the government deliver what it cited? It is not a legal-compliance test.
3. GM37 reportedly lets the panel make "any modifications [it] considers necessary" (VERIFIED-SECONDARY). Even (a)–(c) do not bind the panel. They remain fair conditions for testing fidelity to the proposal the government cited.

Two further points (my analysis):

- "s. 15(2) status" is, under the Act, a matter of "the Commission['s] opinion". Whether the panel can confer it depends on the motion's terms, which is a gap.
- A Clearwater-based division within ±25% would need no s.15(2) status at all. Scoring should treat a division "mostly consisting of" Clearwater County and western Mountain View County, given s.15(2) status or an equivalent sub-25% protection, as adoption.

**H3. Evidence that would show genuine consideration.** Strongest first:

1. **Adoption.** The map contains the division.
2. **Express treatment with a reason.** The committee or panel report names the Clearwater / western Mountain View option and gives a reason for adopting it or declining it, tied to the Act's factors. Examples: population and variance, how many s.15(2) criteria it meets, community of interest, or the knock-on effects on (a)–(c).
3. **Supporting analysis.** A population table, variance figure or criteria count for the option, even if the option was rejected.
4. **Public record of deliberation.** CEB committee transcripts, which are public, or panel minutes showing the option was discussed with reasons.

These are **not sufficient**:

- boilerplate such as "all recommendations were carefully considered";
- naming the option with no reason;
- silence.

**H4. Which scoring rule.**

- **Strict** (no Clearwater s.15(2) seat = fail). This rewrites "consider restoring" as "restore". It misreads the text the audit says it is testing, and it would mark as unfaithful a committee that weighed the option openly and declined it for stated reasons. Academic §7 X1 (line 1765) and `checklist_baseline_scoring.md` (line 161) already say "restored". That wording overstates R5.
- **Lenient** (any consideration = pass). This cannot be falsified. Deliberations are private, and anyone can say they considered something. It would make (d) meaningless.
- **Evidenced consideration** (pass only if the report shows the option was weighed and gives a reason; adoption is an automatic pass). **This is the most defensible rule.** It matches the plain text, and it matches how Canadian law checks a duty to consider: through reasons (*Baker*; *Vavilov*). It is falsifiable from public documents. It applies the same way whatever the outcome. It also connects to the legal point in §D row 7: reasons are what a map's defenders will need.

**Recommended implementation.**

1. Score (d) in three states: **ADOPTED / CONSIDERED-WITH-REASONS / NOT SHOWN**.
2. X1 passes only if (a)–(c) pass and (d) is ADOPTED or CONSIDERED-WITH-REASONS.
3. Report the strict-reading result alongside, as a sensitivity line.
4. Today is 2026-10-29, before the Nov. 2 release. Per `SESSION_HANDOFF.md`, change the spec only through a dated entry in `findings/pre_registration_amendment_log.md`, using its required what / why-not-a-goalpost-move / why-unamended-not-feasible structure, and **before** the map lands.
5. At the same time, fix `r5_test` in `en.ts`, academic X1, and `checklist_baseline_scoring.md` X1 ("R5 binds the November committee" becomes "R5 binds no one; it is the yardstick the government cited").
