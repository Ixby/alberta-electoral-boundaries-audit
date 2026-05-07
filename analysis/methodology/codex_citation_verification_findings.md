# Codex: Citation Verification Findings

Date: 2026-05-06  
Target: `alberta_audit/analysis/methodology/academic_literature_review.md`  
Scope: read-only verification of citation metadata, content fit, and local consistency. The target file was not edited.

## Step 1 - Local Inventory

I reread the current `academic_literature_review.md` with line numbers before writing this note. The current file has already absorbed several earlier fixes: Stephanopoulos and McGhee is now 2015 / 82(2); the unverifiable Pal UTLJ/CJLJ entries were removed; Sancton is now a 2008 book; the neighbour-drain status and drand seed scope are clearer; and the section numbering is fixed.

Remaining audit focus is therefore not the older hallucination set, but the smaller current-state set: exact titles/pages, source-to-claim fit, and places where the review should distinguish "literature says" from "audit inference."

## Step 2 - Metadata Verification

| Line(s) | Citation | Finding | Resolution |
| --- | --- | --- | --- |
| 13, 191 | Stephanopoulos and McGhee 2015, "Partisan Gerrymandering and the Efficiency Gap" | Verified. Year, journal, volume/issue, and pages match U. Chicago Law Review. Content supports efficiency gap / wasted votes / packing and cracking. | Keep. |
| 14 | McDonald and Best 2015 | Metadata partly wrong. The verified title is "Unfair Partisan Gerrymanders in Politics and Law: A Diagnostic Applied to Six Cases," not "An Assessment of Partisan Asymmetry." Volume/pages are right. | Fix title; keep mean-median content. |
| 15, 30 | Warrington 2018 and 2019 | Verified. 2018 paper introduces vote-distribution/declination approach; 2019 paper compares measures and includes EG/mean-median/declination divergence. | Keep. |
| 19 | Grofman 1983 | Metadata appears correct: "Measures of Bias and Proportionality in Seats-Votes Relationships," Political Methodology 9(3):295-327. Public verification found it through later scholarly references/JSTOR stable ID, not a publisher landing page. | Keep; library/publisher confirmation preferred for final bibliography. |
| 20 | King and Browning 1987 | Verified. APSR 81(4):1251-1273. Content supports seats-votes partisan bias. | Keep. |
| 21 | Gelman and King 1994 | Verified. AJPS 38(2):514-554. Content supports seats-votes/redistricting evaluation and uncertainty. | Keep. |
| 22, 192 | Chen and Rodden 2013 | Verified. QJPS 8(3):239-269. Content supports natural political-geography bias from concentrated urban voters. | Keep, but mark Alberta EG interpretation as audit inference. |
| 23 | Rodden 2019 | Verified. *Why Cities Lose*, Basic Books, 2019. Content supports urban-rural/density-based electoral disadvantage. | Keep, but avoid "inevitable" language. |
| 24 | Chen 2017 | Metadata incomplete. Full verified title is "The Impact of Political Geography on Wisconsin Redistricting: An Analysis of Wisconsin's Act 43 Assembly Districting Plan," Election Law Journal 16(4):443-452. | Use full title. |
| 25 | DeFord, Duchin, Solomon 2021 | ReCom citation verified. The content claim "Introduces the GEO metric" is not verified and appears wrong; GEO is introduced by Campisi, Ratliff, Somersille, and Veomett 2022. | Cite DeFord/Duchin/Solomon only for ReCom/GerryChain-style ensemble chains; remove GEO claim or add separate GEO citation. |
| 26 | Stephanopoulos and McGhee 2018 | Verified. "The Measure of a Metric," Stanford Law Review 70(5):1503-1568. | Keep. |
| 31 | Katz, King, Rosenblatt 2020 | Verified. APSR 114(1):164-178. Content supports partisan fairness foundations and critique of single unexamined measures. "Argues for measure ensembles" is a little too strong. | Rephrase to "supports separating fairness quantities from metrics and using multiple perspectives/diagnostics." |
| 35 | Herschlag et al. 2020 | Verified. Statistics and Public Policy 7(1):30-38. Content supports ensemble/outlier analysis and packing/cracking visual diagnostics. | Keep. |
| 48 | Alberta EBCA | Verified against the Alberta King's Printer PDF linked from Elections Alberta. The consolidation is current as of December 5, 2024; sections 13-15 support 89 EDs, effective-representation considerations, the +/-25% band, and the up-to-four ED exception down to -50% with the listed criteria. | Keep; cite the King's Printer PDF rather than only a secondary or archived copy. |
| 43, 110 | *Reference re Provincial Electoral Boundaries (Saskatchewan)* | Verified. [1991] 2 SCR 158; effective representation use is correct. | Keep. |
| 49 | Courtney 2001 | Verified. *Commissioned Ridings* is the foundational Canadian boundary-commission source. Content fit is strong. | Keep; add chapter/page pincites. |
| 50 | Courtney 2004 | Verified as UBC Press *Elections*; hardcover 2004, paperback 2005. Content covers electoral districts among Canadian electoral-regime building blocks. | Keep, cite edition used. |
| 51, 136, 154, 275 | Pal 2015 | Source verified as Michael Pal, "The Fractured Right to Vote..." (2015) 61:2 McGill LJ 231. McGill gives the start-page cite; Erudit gives the full range as 231-274. The review's 231-287 range is wrong. | Change 231-287 to 231-274, or cite start page only as "(2015) 61:2 McGill LJ 231." |
| 53 | Smith, *Canada's Deep Crown* | Metadata is wrong. Verified work is *Canada's Deep Crown: Beyond Elizabeth II, The Crown's Continuing Canadian Complexion*, by David E. Smith, Christopher McCreery, and Jonathan Shanks, University of Toronto Press, 2022. No representation/provincial redistribution chapter claim was verified. | Remove or replace with a directly relevant representation/boundaries source. Do not cite as 2010 single-author authority. |
| 54 | Sancton 2008 | Verified as a 2008 MQUP book. Relevance to municipal/community-of-interest framing is plausible. | Keep with scoped claim. |
| 55 | Carty | Metadata wrong: UBC Press lists *Big Tent Politics* as 2015, not 2017. Content claim is weak/wrong: chapter 5 is "The Life of the Party," not a representation/electoral-systems chapter, and the book is about Liberal Party organization. | Remove from boundary-commission literature or repurpose only for party-politics context; fix year if retained. |
| 61 | Archer 1992 | Citation real; page range found as 109-136. | Replace xxx-xxx with 109-136. |
| 63 | Stewart and Archer 2000 | Metadata verified. Content supports Alberta party/leadership context, not WRP/UCP evolution directly. | Keep only for PC-era leadership selection; avoid WRP/UCP claim. |
| 64 | Wiseman 2020 | Metadata verified. I found no Alberta chapter; table of contents is national/federal party history. | Do not claim "Alberta chapter" unless the text is checked; use for broad party-system context only. |
| 65 | *Orange Chinook* | Verified. Correct editors: Bratt, Brownsey, Sutherland, Taras. Strong fit for 2015 Alberta NDP and PC/UCP transition context. | Keep. |
| 70 | Ladner 2003 | Citation real; page range found as 167-196 in secondary syllabus/reference sources. | Fill page range as 167-196 if confirmed against book. |
| 72 | Papillon and [co-author] 2021 | Not verified as written. Search did not locate this title. | Do not cite in final form. Replace with a verified Indigenous representation/electoral-system source or leave as "source to locate." |
| 86-89 | Polsby/Popper, Reock, Young, Barnes/Solomon | Verified. Minor detail: Reock title is commonly "A Note: Measuring Compactness..." | Keep; optionally add "A Note:" to Reock title. |
| 101 | Altman and McDonald 2014 | Citation exists, but page range appears wrong: HICSS listing gives 2063-2072, not 2032-2041. Content claim overreaches: it is public participation GIS, not a formal basis for the audit's 70/30 blend. | Fix pages. If supporting redistricting software/modeling, cite Altman and McDonald 2011 BARD instead or alongside it. |
| 102 | Fifield, Imai, Kawahara, Kenny 2020 | Verified. Statistics and Public Policy 7(1):52-68. Content supports empirical validation of redistricting simulations. | Keep. |
| 114 | *Rucho v. Common Cause* | Verified for political-question holding and judicial-manageability discussion. Content fit is fine as US context, but "direct intellectual motivator" is the audit's inference. | Keep but phrase as interpretive context, not source fact. |
| 115 | *Figueroa* | Verified as [2003] 1 SCR 912; supports meaningful participation under s.3. Content fit is indirect, not boundary-specific. | Keep with narrowed claim. |
| 116 | *Frank* | Verified as 2019 SCC 1, [2019] 1 SCR 3. It is a s.3 voting-rights case, not an effective-representation boundary case. | Keep only for broad s.3 context; avoid "reinforces effective representation standard" unless tied back carefully. |
| 117 | *Haig* | Verified as [1993] 2 SCR 995. It concerns referendums and limits of s.3. | Keep only if the point is s.3 scope; do not imply direct boundary relevance. |
| 193 | McGann, Smith, Latner, Keena 2016 | Verified. Cambridge book exists and covers partisan bias/gerrymandering. | Keep; add page/chapter pin if using for packing+cracking case studies. |
| 229 | Nosek et al. 2018 | Verified. PNAS 115(11):2600-2606. | Keep. |
| 230 | Uhlmann et al. 2019 | Metadata wrong. Verified title is "Scientific Utopia III: Crowdsourcing Science," Perspectives on Psychological Science 14(5):711-733. It is not 14(3):375-395. AsPredicted-platform claim was not verified from the source. | Fix metadata; use only for crowdsourcing/transparency/replication unless AsPredicted support is specifically sourced elsewhere. |
| 231 | van 't Veer and Giner-Sorolla 2016 | Metadata/title/pages wrong. Verified title is "Pre-registration in social psychology-A discussion and suggested template," JESP 67:2-12. It proposes a template; it did not design the AsPredicted template. | Fix title/pages and remove AsPredicted-template claim. |
| 232 | OSF / AsPredicted links | User clarified that the OSF and AsPredicted registrations are intentionally not public yet. Treat the current external non-verifiability as a privacy/release-status issue, not as a failed source. | Do not describe these as public records until release. Phrase as private preregistrations or pending public release, or omit the URLs from public-facing text until they are public. |
| 238-241 | drand rounds | Local consistency mostly verified: `drand_seed.py` uses round 5500000; `report_academic.md` uses round 6062459 for future November work. | Keep current distinction. |
| 245 | Stark 2010 | Verified. USENIX EVT/WOTE 2010 paper. Public randomness analogy is reasonable but should stay analogy-level. | Keep. |
| 263 | Gill v. Whitford / US methodology note | Gill is real and relevant to EG history. The claim that Alberta law has looked to US methodology was not verified in this pass. | Add Alberta/legal support or remove the "Alberta law has looked to US methodology" clause. |

## Step 3 - Content-Claim Findings

1. The strongest remaining content risk is not fabrication; it is overclaiming. Chen and Rodden/Rodden support natural geography, but the Alberta-specific claim that the 2019 -2.64% EG is "likely substantially natural packing" is the audit's inference and should be labelled that way.

2. DeFord/Duchin/Solomon should not be credited with introducing GEO. The verified GEO introduction is Campisi, Ratliff, Somersille, and Veomett, "Geography and Election Outcome Metric: An Introduction," Election Law Journal 21(3), 2022.

3. The Canadian literature section is much improved by verified Pal 2015, but Smith, Carty, Wiseman, and Papillon still need cleanup. Courtney and Pal are the defensible legal/boundary backbone; the others should not be allowed to carry boundary-commission claims unless rechecked with pages.

4. The legal cases are real, but only Saskatchewan is directly a boundary case. Figueroa, Frank, and Haig are broader s.3/scope context. Rucho/Gill are US context. The review should keep these lanes visibly separate.

5. The open-science section needs metadata fixes. Nosek is solid; Uhlmann and van 't Veer are currently mis-cited and overused for AsPredicted-specific claims.

## Step 4 - Local Consistency Findings

1. Neighbour-Drain status in the review now matches the local report better than before: v1 adjacency analysis exists, with Drain Phase B label-shuffle/null work still pending.

2. The two drand rounds are now correctly scoped in the literature review: round 5500000 for current simulation infrastructure and round 6062459 for future November/Lunty pre-commitment.

3. OSF / AsPredicted status is now clarified by the user: these records are not public yet. That resolves the external lookup problem as an intentional privacy state, but it conflicts with any wording in the review or worklog that calls them a "public" or "parallel public" record before release.

## Step 5 - Recommended Fix Queue

High priority before publication:

- Fix McDonald and Best title.
- Fix or shorten Pal page range; safest final citation is "(2015) 61:2 McGill LJ 231" unless end page is confirmed.
- Remove or replace Smith 2010; it is not verified as cited.
- Fix/remove Carty 2017 and the chapter 5 representation claim.
- Remove Papillon 2021 placeholder unless exact citation is found.
- Fix Altman/McDonald HICSS pages and stop using it as support for the 70/30 blend.
- Fix Uhlmann and van 't Veer metadata and remove unsupported AsPredicted-specific claims.
- Mark OSF and AsPredicted preregistrations as private/pending public release until the records are actually public.

Medium priority:

- Add page/chapter pincites for Courtney, McGann et al., Archer, Ladner, and any Canadian comparator claims.
- Rephrase Alberta-specific natural-packing conclusions as audit inference built on Chen/Rodden, not direct literature claims.
- Narrow Frank, Figueroa, Haig, Rucho, and Gill to their proper legal lanes.
- Add separate Campisi et al. 2022 if the GEO metric remains in the review.

Low priority:

- Add "A Note:" to Reock's title.
- Use full title for Chen 2017.
- Cite the exact edition for Courtney 2004/2005.

## Step 6 - Follow-Up Source Checks (2026-05-06)

I checked the remaining high-risk citations against official or publisher pages where possible, and folded the OSF/AsPredicted privacy clarification into the audit.

| Citation / claim | Source-check result | Resolution |
| --- | --- | --- |
| Alberta *Electoral Boundaries Commission Act* | Verified from Elections Alberta's legislation link to the Alberta King's Printer PDF. The PDF is an office consolidation, RSA 2000 c E-3, current as of December 5, 2024. It confirms 89 proposed EDs in s.13; effective-representation and communities-of-interest considerations in s.14; the +/-25% rule in s.15(1); and the up-to-four -50% exception plus criteria in s.15(2)-(3). | Keep. Use the King's Printer PDF as the primary source. |
| McDonald and Best 2015 | Publisher page confirms the title is "Unfair Partisan Gerrymanders in Politics and Law: A Diagnostic Applied to Six Cases." The abstract supports mean-median comparison as the key diagnostic. | Fix the title; content use is fine for mean-median. |
| Pal 2015 | McGill Law Journal page confirms title, author, volume/issue, and start page. Erudit confirms full page range 231-274. | Replace 231-287 with 231-274. |
| Chen 2017 | SAGE page confirms full title: "The Impact of Political Geography on Wisconsin Redistricting: An Analysis of Wisconsin's Act 43 Assembly Districting Plan," ELJ 16(4):443-452. | Use full title. |
| DeFord / Duchin / Solomon 2021 and GEO | HDSR source confirms ReCom as a family of Markov chains. Separate SAGE source confirms Campisi, Ratliff, Somersille, and Veomett 2022 introduces the GEO metric. | Do not credit GEO to DeFord/Duchin/Solomon. Cite ReCom and GEO separately. |
| Altman and McDonald | JSS source confirms the better fit for redistricting software is Altman and McDonald 2011, "BARD: Better Automated Redistricting," 42(4):1-28. The HICSS public-participation GIS cite does not justify the audit's 70/30 vote blend. | Cite BARD for software/modeling; do not use either source as formal support for the 70/30 blend unless the methodology text is narrowed. |
| Carty 2015 | UBC Press confirms *Big Tent Politics* is 2015, not 2017. Contents list chapter 5 as "The Life of the Party"; the book is Liberal Party organization/political-history context. | Remove from boundary-commission literature, or retain only as party-politics background with corrected year. |
| Smith / *Canada's Deep Crown* | De Gruyter/UTP page confirms the work is *Canada's Deep Crown* by David E. Smith, Christopher McCreery, and Jonathan Shanks, eBook published December 2, 2021 / print-era 2022. It is Crown/monarchy/government context, not verified redistribution authority. | Remove or replace with a directly relevant representation/boundaries source. |
| Orange Chinook | University of Calgary/JSTOR sources confirm title, 2019 date, editors Duane Bratt, Keith Brownsey, Richard Sutherland, and David Taras, and relevance to 2015 Alberta NDP / PC transition. | Keep. |
| Uhlmann et al. 2019 | SAGE confirms "Scientific Utopia III: Crowdsourcing Science," *Perspectives on Psychological Science* 14(5):711-733. It supports crowdsourcing/transparency, not an AsPredicted-platform claim. | Fix title, issue, and pages; narrow content claim. |
| van 't Veer and Giner-Sorolla 2016 | ScienceDirect confirms "Pre-registration in social psychology-A discussion and suggested template," JESP 67:2-12. It proposes a preregistration template; it does not establish the AsPredicted template used by this audit. | Fix title/pages; remove "designed the AsPredicted question template" claim. |
| OSF and AsPredicted registration links | User clarified these records are intentionally not public yet. Public automated checks cannot validate their contents until release, and that is expected. | Mark as private/pending public release. Do not call them public records yet. |
| Papillon 2021 placeholder | Targeted searches still did not locate the title as written. | Remove before publication unless exact bibliographic data is found. |
| Wiseman 2020 "Alberta chapter" | Source metadata is real, but no Alberta-specific chapter was verified. | Use only for broad party-system context unless the chapter/page claim is manually confirmed. |
| Gill / Alberta-law methodology claim | Gill is real and relevant to US EG history. No source found for "Alberta law has looked to US methodology." | Remove that clause unless a Canadian/Alberta authority is located. |

After this step, the unresolved checks are narrow: Courtney chapter/page pincites, McGann chapter/page pincites, physical-book confirmation for Ladner and Archer page ranges if strict bibliography standards are required, and public recheck of OSF/AsPredicted after release.

## Step 7 - Chapter and Page Targets for Full-Text Checks (2026-05-06)

These are the specific chapters/pages to obtain or inspect if the goal is to move from metadata verification to content-level certification.

| Source | Chapters/pages to check | Use in the literature review |
| --- | --- | --- |
| Courtney 2001, *Commissioned Ridings* | Ch. 2, "Electoral Districts in a Federal State," pp. 9-34; Ch. 3, "Institutional Role-Modelling: Canada's First Provincial Electoral Boundaries Commissions," pp. 35-56; Ch. 5, "Drawing the Maps," pp. 74-93; Ch. 6, "Professional and Independent Commissions," pp. 94-121; Ch. 8, "\"A Full and Generous Construction\": The Courts and Redistribution," pp. 151-171; Ch. 9, "Life With Carter: Commissioned Ridings in the 1990s," pp. 172-203; Ch. 10, "Community of Interest and Effective Representation," pp. 204-234. | Canadian boundary-commission model, independent commissions, provincial/federal practice, courts, effective representation, community of interest. |
| Courtney 2004/2005, *Elections* | Ch. 3, "From Gerrymandering to Independence: Territorially-Based Districts," pp. 45-76. Optional audit framing: Ch. 7, "Auditing Canada's Electoral System," pp. 160-177. | Shorter Canadian Democratic Audit treatment of redistribution/electoral districts; use as secondary overview, not replacement for *Commissioned Ridings*. |
| Archer 1992 | "Voting Behaviour and Political Dominance in Alberta, 1971-1991," in *Government and Politics in Alberta*, pp. 109-136. | Alberta electoral geography and one-party-dominance context. |
| Ladner 2003 | Ch. 7, "Treaty Federalism: An Indigenous Vision of Canadian Federalisms," in *New Trends in Canadian Federalism*, pp. 167-196. Some scholarly references cite 167-194, likely excluding notes; full chapter appears to run until Ch. 8 begins at p. 197. | Indigenous constitutional/federalism context. Use carefully: it supports Indigenous governance/treaty-federalism framing, not a specific electoral-boundary rule by itself. |
| McGann, Smith, Latner, Keena 2016, *Gerrymandering in America* | Ch. 3, "Measuring Partisan Bias," pp. 56-96, especially "Partisan Gerrymandering and How to Measure It," pp. 58-69; Ch. 4, "Geographic Explanations for Partisan Bias," pp. 97-145, especially "The Urban Concentration Hypothesis," pp. 100-121; Ch. 5, "Political Explanations of Partisan Bias," pp. 146-176. | Partisan symmetry/bias, distinguishing geography from political map-drawing, and US case-study context. |
| Wiseman 2020, *Partisan Odysseys* | No Alberta chapter verified. If retained at all, relevant broad-context chapters are Ch. 8, "Division and Reconfiguration," pp. 115-128; Ch. 9, "Conservatism: Old and New," pp. 129-143; and Conclusion, pp. 144-160. | Broad Canadian party-system / Conservative realignment context only. Do not cite as "Alberta chapter." |
| Sancton 2008, *The Limits of Boundaries* | Introduction, pp. 3-8; Ch. 1, "Focusing on Cities," pp. 9-32; Ch. 3, "Boundaries for Municipal Corporations," pp. 56-77; Conclusion, pp. 131-138. | Municipal-boundary and city-region boundary theory. Use only as analogy/context for community-of-interest or municipal anchoring; it is not an electoral-district source. |
| Papillon placeholder | No chapter/page target. The exact title in the review was not found. | Remove unless exact source appears. Possible replacement for Indigenous electoral participation, not boundary design: Dabin, Daoust, and Papillon 2019, "Indigenous Peoples and Affinity Voting in Canada," *CJPS* 52(1):39-53. |
| Altman and McDonald | If retained for software/modeling, use Altman and McDonald 2011, "BARD: Better Automated Redistricting," *Journal of Statistical Software* 42(4):1-28. The HICSS 2014 public-participation GIS paper is pp. 2063-2072. | Neither source should be used as direct support for the audit's 70/30 vote blend unless the text says the blend is an audit assumption. |

## Step 8 - Uploaded `source_checks` Inventory (2026-05-06)

The uploaded folder covers most of the full-text targets, but not all.

| Target | Upload status | Note |
| --- | --- | --- |
| Courtney 2001, *Commissioned Ridings* | Missing for content-check purposes | The uploaded `commissioned-ridings-...337p-dollar7500...pdf` appears to be a book review or journal item about the book, not Courtney's actual chapters. It is not enough to verify Ch. 2, 3, 5, 6, 8, 9, or 10. |
| Courtney 2004/2005, *Elections* | Present, but needs visual/OCR confirmation | `John_Courtney_Elections_The_Ca.PDF` is present. Local tools could not extract reliable OCR from it, so confirm it includes Ch. 3 pp. 45-76, and optionally Ch. 7 pp. 160-177. |
| Archer 1992 | Present | `Government_and_Politics_in_Alberta_----_(5_Voting_Behaviour_and_Political_Dominance_in_Alberta,_1971-1991).pdf` is the target chapter. |
| Ladner 2003 | Missing if Ladner remains cited | I did not see `Treaty Federalism` / *New Trends in Canadian Federalism*. The Dabin/Daoust/Papillon article is useful as a replacement source, but it does not verify Ladner. |
| McGann et al. 2016 | Present | Cambridge zip contains Ch. 3 pp. 56-96, Ch. 4 pp. 97-145, and Ch. 5 pp. 146-176. |
| Wiseman 2020 | Present, with duplicate | De Gruyter PDFs `...-009`, `...-010`, `...-011` are present; `...-010` appears twice. These cover the broad-context chapters identified earlier. |
| Sancton 2008 | Present | Introduction, Ch. 1, Ch. 3, and Conclusion PDFs are present. |
| Papillon placeholder / replacement | Replacement present | `indigenous-peoples-and-affinity-voting-in-canada.pdf` is present and can replace the unverifiable Papillon placeholder for Indigenous electoral participation, not boundary design. |
| Altman and McDonald | Uploaded source is not the requested one | `altman-mcdonald-2017-redistricting-by-formula-an-ohio-reform-experiment.pdf` is present, but it is not BARD 2011 and not the HICSS 2014 public-participation GIS paper. Keep it only if the review adds a distinct Ohio reform / formula-redistricting point. |

Net missing items at this point: Courtney 2001 Ch. 10 pp. 204-234 and the rest of Ch. 9 pp. 186-203 if those claims remain; Ladner 2003 if retained; Altman and McDonald 2014 HICSS only if that exact citation remains; and public OSF/AsPredicted checks after release. Altman and McDonald 2011 BARD is now present as `v42i04.pdf`.

## Step 9 - Courtney *Elections* Chapter 3 Screenshot Check (2026-05-06)

The user supplied screenshots of Courtney 2004/2005, *Elections*, Ch. 3, "From Gerrymandering to Independence: Territorially-Based Districts," pp. 45-76. This is the correct Courtney *Elections* source for the review's redistribution/electoral-district overview.

Useful pincites from the screenshots:

- pp. 45-46: chapter framing; why boundary drawing matters for participation, responsiveness, inclusiveness, equality, public trust, effective representation, and capacity to ensure accountability.
- pp. 47-50: pre-reform gerrymandering and malapportionment examples, including Quebec and interprovincial district-size problems.
- pp. 53-58: "Designing Districts" and "Canada Adopts Independent Boundary Commissions"; provincial/federal adoption of arm's-length commissions, nonpartisan design, and Manitoba as an institutional model.
- pp. 58-60: elements of federal and provincial boundary readjustment schemes, including separate commissions, population deviation limits, exceptional circumstances, community of interest / community identity / historical pattern, and public opportunity to make representations.
- pp. 60-61: examples of commissions considering community of interest and minority representation, including Acadian and African-Nova Scotian examples.
- pp. 61-63: "The Courts and Redistribution"; s.3 Charter framing and *Reference re Provincial Electoral Boundaries (Saskatchewan)*, including relative parity and factors that may justify departure from absolute parity.
- pp. 63-67: "Aboriginal Electoral Districts"; relevant to Indigenous representation context, but still broader than Alberta EBCA s.15(2)(d).
- pp. 67-69: public participation in redistribution.
- pp. 69-75: equity/equality trends in district populations, Gini-index discussion, and concluding assessment.
- p. 76: chapter summary box: nonpartisan commissions now determine district boundaries; community of interest incorporates social, regional, and ethnic considerations; effective representation is an ambiguous term open to differing interpretations.

Resolved by this upload: Courtney 2004/2005, Ch. 3 pp. 45-76. Still missing for Courtney: the *Commissioned Ridings* 2001 chapters, especially Ch. 5, Ch. 6, Ch. 8, and Ch. 10.

## Step 10 - Updated `source_checks` Inventory After Courtney Uploads (2026-05-06)

New Courtney 2001 files were added:

- `Commissioned_Ridings_..._(Pages_1_to_25).pdf`
- `Commissioned_Ridings_..._(Pages_26_to_50).pdf`
- `Commissioned_Ridings_..._(Pages_51_to_75).pdf`
- `Commissioned_Ridings_..._(Pages_76_to_100).pdf`
- `Commissioned_Ridings_..._(Pages_101_to_125).pdf`
- `2615327_commissioned-ridings-p151-171,172-185.pdf`

This resolves most of the Courtney 2001 coverage:

- Ch. 2 pp. 9-34: present across pp. 1-25 and 26-50 files.
- Ch. 3 pp. 35-56: present across pp. 26-50 and 51-75 files.
- Ch. 5 pp. 74-93: present across pp. 51-75 and 76-100 files.
- Ch. 6 pp. 94-121: present across pp. 76-100 and 101-125 files.
- Ch. 8 pp. 151-171: present in `2615327_commissioned-ridings-p151-171,172-185.pdf`.
- Ch. 9 pp. 172-203: partially present for pp. 172-185 only.
- Ch. 10 pp. 204-234: still missing.

Remaining Courtney pull if the review uses community-of-interest/effective-representation claims from *Commissioned Ridings*: Ch. 10 pp. 204-234. If using "Life With Carter" / 1990s commission practice, also pull Ch. 9 pp. 186-203.

## Step 11 - Updated `source_checks` Inventory After BARD Upload (2026-05-06)

New file added: `v42i04.pdf`.

This appears to be Altman and McDonald 2011, "BARD: Better Automated Redistricting," *Journal of Statistical Software* 42(4):1-28. That resolves the BARD source request for redistricting software/modeling context.

Still not present: Altman and McDonald 2014 HICSS, "Public Participation GIS: The Case of Redistricting," pp. 2063-2072. This only matters if the literature review keeps the HICSS citation specifically. The cleaner fix is to cite BARD 2011 for redistricting software/modeling and describe the audit's 70/30 blend as an audit assumption, not as a literature-derived method.

## Source Ledger

Key external sources used in this verification pass:

- Alberta King's Printer, *Electoral Boundaries Commission Act* PDF: https://www.qp.alberta.ca/documents/Acts/E03.pdf
- Elections Alberta electoral-boundaries commission page linking the Act: https://www.elections.ab.ca/resources/reports/electoral-boundaries-commission/
- Stephanopoulos and McGhee 2015, University of Chicago Law Review: https://lawreview.uchicago.edu/online-archive/partisan-gerrymandering-and-efficiency-gap
- McDonald and Best 2015, Election Law Journal: https://journals.sagepub.com/doi/10.1089/elj.2015.0358
- Warrington 2018: https://journals.sagepub.com/doi/10.1089/elj.2017.0447
- Warrington 2019: https://journals.sagepub.com/doi/abs/10.1089/elj.2018.0508
- Chen and Rodden 2013: https://www.nowpublishers.com/article/Details/QJPS-12033
- Chen 2017: https://journals.sagepub.com/doi/full/10.1089/elj.2017.0455
- Gelman and King 1994: https://gking.harvard.edu/files/abs/writeit-abs.shtml
- King and Browning 1987: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/DFCCA480550B89B09281AB9266090701/S0003055400204437a.pdf/democratic-representation-and-partisan-bias-in-congressional-elections.pdf
- Katz, King, Rosenblatt 2020: https://www.cambridge.org/core/journals/american-political-science-review/article/theoretical-foundations-and-empirical-evaluations-of-partisan-fairness-in-districtbased-democracies/86DAD2FE5F86E72D75A9704DFD7D192E
- Herschlag et al. 2020: https://ideas.repec.org/a/taf/usppxx/v7y2020i1p30-38.html
- DeFord, Duchin, Solomon 2021, HDSR ReCom: https://hdsr.mitpress.mit.edu/pub/1ds8ptxu
- Campisi, Ratliff, Somersille, Veomett 2022 GEO metric: https://journals.sagepub.com/doi/full/10.1089/elj.2021.0054
- Barnes and Solomon 2021: https://www.cambridge.org/core/journals/political-analysis/article/gerrymandering-and-compactness-implementation-flexibility-and-abuse/433FB3A0D12E5851C1A43C8B29264E01
- Pal 2015, McGill Law Journal: https://lawjournal.mcgill.ca/article/the-fractured-right-to-vote-democracy-discretion-and-designing-electoral-districts/
- Pal 2015, Erudit PDF / DOI record: https://www.erudit.org/en/journals/mlj/2015-v61-n2-mlj02616/1037248ar.pdf
- Courtney 2001, MQUP: https://www.mqup.ca/commissioned-ridings-products-9780773522657.php
- Courtney 2001, De Gruyter table of contents: https://www.degruyterbrill.com/document/doi/10.1515/9780773569430-009/html
- Courtney 2004/2005, UBC Press: https://www.ubcpress.ca/elections
- Courtney 2004/2005, De Gruyter table of contents: https://www.degruyterbrill.com/document/doi/10.59962/9780774850889-007/html
- Carty 2015, UBC Press: https://www.ubcpress.ca/big-tent-politics
- Sancton 2008, MQUP/De Gruyter: https://www.degruyterbrill.com/document/doi/10.1515/9780773574267/html
- Sancton 2008, De Gruyter table of contents: https://www.degruyterbrill.com/document/doi/10.1515/9780773574977/html
- Smith, McCreery, Shanks 2022: https://www.degruyterbrill.com/document/doi/10.3138/9781487540777/html
- Orange Chinook: https://www.degruyterbrill.com/document/doi/10.1515/9781773850276/html
- Archer 1992 page-range corroboration: https://ojs.unbc.ca/index.php/cpsr/article/download/19/150/455
- Ladner 2003 page-range corroboration: https://www.encyclopedia.com/social-sciences/applied-and-social-sciences-magazines/treaty-federalism
- McGann et al. 2016 Cambridge table of contents: https://assets.cambridge.org/97811071/43258/toc/9781107143258_toc.pdf
- Wiseman 2020, De Gruyter table of contents: https://www.degruyterbrill.com/document/doi/10.3138/9781487536947/html
- Dabin, Daoust, Papillon 2019: https://www.cambridge.org/core/journals/canadian-journal-of-political-science-revue-canadienne-de-science-politique/article/indigenous-peoples-and-affinity-voting-in-canada/C406B5C0145941FD03D57AD863894239
- Altman and McDonald 2011 BARD: https://www.jstatsoft.org/v42/i04/
- HICSS 2014 listing for "Public Participation GIS": https://researchr.org/publication/hicss-2014
- Fifield et al. 2020: https://imai.fas.harvard.edu/research/enumerate.html
- Rucho: https://supreme.justia.com/cases/federal/us/588/18-422/
- Gill: https://supreme.justia.com/cases/federal/us/585/16-1161/
- Nosek et al. 2018: https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/
- Uhlmann et al. 2019: https://journals.sagepub.com/doi/10.1177/1745691619850561
- van 't Veer and Giner-Sorolla 2016: https://www.sciencedirect.com/science/article/pii/S0022103116301925
- Stark 2010: https://www.usenix.org/conference/evtwote-10/super-simple-simultaneous-single-ballot-risk-limiting-audits
- drand background: https://www.drand.love/about/
