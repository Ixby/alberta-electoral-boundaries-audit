# Evidence: source documents the audit relies on

Each file is an unaltered copy of a public document, kept so a reader can check every quotation against the original. Times are Alberta time (MDT). Hashes are SHA-256 of the file as committed.

| File | What it is | Source | Retrieved |
|---|---|---|---|
| `legislation/electoral_boundaries_commission_act_RSA2000_cE-3_current_2026-05-14.pdf` | Electoral Boundaries Commission Act, office consolidation current as of 2026-05-14 | https://kings-printer.alberta.ca/documents/Acts/E03.pdf | 2026-10-31 10:14 |
| `legislation/interpretation_act_RSA2000_cI-8_current_2025-09-01.pdf` | Interpretation Act, current as of 2025-09-01 | https://kings-printer.alberta.ca/documents/Acts/I08.pdf | 2026-10-31 10:14 |
| `legislation/municipal_government_act_RSA2000_cM-26_current_2026-09-01.pdf` | Municipal Government Act, current as of 2026-09-01 | https://kings-printer.alberta.ca/documents/Acts/m26.pdf | 2026-10-31 10:14 |
| `hansard/alberta_hansard_1990-12-10_evening.pdf` | Alberta Hansard, 1990-12-10 evening sitting, pp. 2749–2751 (committee debate on the Crowsnest Pass clause) | https://docs.assembly.ab.ca/LADDAR_files/docs/hansards/han/legislature_22/session_2/19901210_2000_01_han.pdf | 2026-10-31 10:15 |
| `commission_reports/abebc_2026_rpt_final.pdf` | 2025–26 Electoral Boundaries Commission final report: majority report, with the minority report and maps as Appendix E (p. 285 on); 362 pages; PDF created 2026-03-16 | https://www.elections.ab.ca/uploads/abebc_2026_rpt_final.pdf | 2026-10-31 10:15 |
| `commission_reports/abebc_2003_rpt_final.pdf` | 2002–03 Electoral Boundaries Commission final report, 92 pages | https://www.elections.ab.ca/uploads/abebc_2003_rpt_final.pdf | 2026-10-31 10:16 |
| `legislature/assembly_committee_page_ceb_2026-10-31.html` | Legislative Assembly of Alberta page for the Select Special Committee on Electoral Boundaries, as served | https://www.assembly.ab.ca/assembly-business/committees/ceb | 2026-10-31 15:01 |
| `legislature/standing_orders_alberta_effective_2026-03-16.pdf` | Standing Orders of the Legislative Assembly of Alberta, effective March 16, 2026 | https://www.assembly.ab.ca/docs/default-source/reference/assembly-documents/StandingOrders.pdf | 2026-10-31 19:40 |
| `legislature/assembly_news_ebc_appointed_2025-03-28.html` | Legislative Assembly of Alberta notice "Electoral Boundaries Commission to soon begin consultations", March 28, 2025, as served | https://www.assembly.ab.ca/about/news-and-announcements/2025/03/28/electoral-boundaries-commission-to-soon-begin-consultations | 2026-11-01 |
| `legislature/ceb_transcript_2026-10-28.pdf` | Transcript of the Select Special Committee on Electoral Boundaries, meeting of October 28, 2026, pp. CEB-65 to CEB-78; 20 pages | https://docs.assembly.ab.ca/LADDAR_files/docs/committees/ceb/legislature_31/session_2/20261028_1030_01_ceb.pdf | 2026-11-01 |

Full hashes:

```
e34f13093c7fdcb8b815ea5c7aba18d5943398689cc4215bc3dc0f8047bcdb85  electoral_boundaries_commission_act_RSA2000_cE-3_current_2026-05-14.pdf
eca9fc7dcf80aea7023794657578b7c493ed7657394542ddbee0a7908844caa9  interpretation_act_RSA2000_cI-8_current_2025-09-01.pdf
fa0c134755325fa37839512c27472fd78fc28c007db5174c0ce3333cf277b7b4  municipal_government_act_RSA2000_cM-26_current_2026-09-01.pdf
63abb96a382144b6afaf5d1612156b62e32b0c1054afe2683258210aaf43c8e2  alberta_hansard_1990-12-10_evening.pdf
7236cd0aaa611f5198f88856f677a2028f9a442dccdc0359725b4995a2d0247e  abebc_2026_rpt_final.pdf
a3555d34175901deac78706820d7778c3adf5e37128020879fccaaa1feedc5f0  abebc_2003_rpt_final.pdf
5520241bf9d35f3efb90fa2dff019a6993fe70ad1e01b9b8ed3872e0ce58d4a3  assembly_committee_page_ceb_2026-10-31.html
46c4825da82f5e6483404f1eb5b1968f5a424cff18cd91898cb468d19e4a7972  standing_orders_alberta_effective_2026-03-16.pdf
64b9986d5b7ec9c99df1c227773005128e37acd5fedc229e2937acf54fa9db4f  assembly_news_ebc_appointed_2025-03-28.html
a9b70c7737e169cb8bd1e9dbc17c7d97e81015dec63214baf4b95b010c49a141  ceb_transcript_2026-10-28.pdf
```

The Assembly's news page is built on each request, so a fresh download will not match the hash above byte for byte; the committed copy is the page as served on 2026-11-01. The transcript PDF downloaded again on 2026-11-01 matched its hash exactly.

The audit used the 2026 final report earlier (`data/meta/data_acquisition_manifest.md`, as `commission_report.pdf`), but no hash was recorded then, so this copy cannot be shown to be byte-identical to that one.

## What each is relied on for: the meaning of "town" in s.15(2)(c)

Checked 2026-10-31 against the files above.

- **The Act defines no "town".** Its only definition is s.1: "In this Act, 'Commission' means an Electoral Boundaries Commission appointed pursuant to section 2."
- **The Act says "city" where it means city.** s.2(3) and (4): of each pair of appointees, "one must be resident in a city and the other resident outside a city".
- **s.15(2)(c)** reads "there is no town in the proposed electoral division that has a population exceeding 8000 people". **s.15(3)** reads "For the purpose of subsection (2)(c), The Municipality of Crowsnest Pass is not a town." The history note is "RSA 2000 cE-13 s15;2009 c19 s5".
- **The figure was 4,000 before 2009.** The 2003 report quotes "(c) there is no town in the proposed electoral division that has a population exceeding 4,000 people" and the Crowsnest Pass clause. The only amendment to s.15 since the 2000 revision is 2009 c19 s5, so the change to 8,000 came then. That is an inference from the history note; the 2009 amending Act itself is not in this folder.
- **The Interpretation Act lists towns and cities as separate kinds of municipality** and defines neither. s.28(1)(kk): "'municipality' means a city, town, village, municipal district, specialized municipality, improvement district or special area". s.3(1) applies the Act "to the interpretation of every enactment except to the extent that a contrary intention appears".
- **The Municipal Government Act makes town and city separate legal statuses.** s.77 lists the types of municipality that may be formed, including "(d) town; (e) city". s.91 treats changing a town to a city as a change of status. The old population rules for each status (ss.78–84) were repealed in 2022 (2022 c16 s9(15)), so today a town is a municipality with town status, whatever its size.
- **The 1990 debate (Hansard pp. 2749–2751).** The bill's criterion was "you cannot have a town greater than 4,000 in population". An opposition member asked why Crowsnest Pass, which "has a population of more than 4,000", was exempted. The Member for Pincher Creek-Crowsnest (Mr. Bradley) answered: "a town, or not a town: that is the question. The municipality of Crowsnest Pass ... was not created under the Municipal Government Act of Alberta. It was created by a special Act". He then argued from its function: lowest density "of any of what are considered to be urban municipalities", five settlements spread along Highway 3; "It's more than a town; it is a collection of towns."
- **Commission practice.** Neither the 2003 nor the 2026 report says how it read "town". The 2026 majority gave Canmore-Banff s.15(2) protection for "its distance from the Legislature, the high Indigenous population, the border with British Columbia", not for criterion (c).

The documents support both readings. Read as written, "town" is a legal status that a city does not have, and the Act uses "city" separately where it means city. The 1990 justification for the Crowsnest Pass clause turned on density and settlement pattern, which supports reading (c) as a test of whether a district holds an urban centre. A draft amendment that would have run set D under both readings was withdrawn unsigned and is not carried into Amendment 5: the audit keeps the reading in Amendment 5, Part 15, which follows commission practice (see the amendment log).

## What each is relied on for: the November committee

Checked 2026-10-31 against the committee page above (correction C37 in the academic report).

- **Who sits on it.** "Committee Members (6)": Brandon Lunty (Chair, UC, Leduc-Beaumont), Chantelle de Jonge (UC), Kathleen Ganley (NDP), Christina Gray (NDP), Tara Sawyer (UC) and Ron Wiebe (UC). Four UCP, two NDP.
- **What created it, and when.** The committee "was established by Government Motion 37, passed by the Assembly on April 21, 2026, to oversee an independent review of the electoral boundaries of Alberta", and "is directed to engage independent advisors in accordance with clause C.(d)" of that motion.
- **The vote.** CBC News, "MLA committee to review Alberta electoral boundaries after report is set aside" (Michelle Bellefontaine, posted April 21, 2026, https://www.cbc.ca/news/canada/edmonton/alberta-boundaries-committee-motion-9.7172743, read 2026-10-31 15:05): "MLAs voted 44-36 in favour of the measure following a highly charged debate Tuesday afternoon." April 21, 2026 was a Tuesday. The article is not copied here because it is a copyrighted news story; the quotation and link are the record.
- **Committee voting.** The Standing Orders cap a special committee at 11 members (SO 56(1)) and give the Speaker a casting vote in the Assembly (SO 11(3)); no rule on whether a committee chair votes on every question or only to break a tie was found (searched 2026-10-31). Amendment 5, Part 25 relies on that absence.

## What each is relied on for: the October 28 committee votes

Checked 2026-11-01 against the committee transcript above.

- **Attendance.** "Rowswell, Garth, Vermilion-Lloydminster-Wainwright (UC)* ... * substitution for Tara Sawyer." The chair, Brandon Lunty, did not vote in either recorded vote below.
- **The report's arrival.** "The report was provided to committee members on October 22, 2026, in accordance with clause C(e)(iv) of Government Motion 37" (p. CEB-65).
- **Motion 1, ending the review (moved by Mr. Wiebe, pp. CEB-66 to CEB-67).** That the committee "(a) acknowledge that the independent advisory panel has submitted its report in accordance with Government Motion 37, thereby concluding its mandate, and (b) conclude its review of the report of the independent advisory panel."
- **First 3–2 vote, carried (p. CEB-72).** "For the motion: de Jonge, Rowswell, Wiebe. Against the motion: Gray, Ganley. Totals: For – 3, Against – 2. The Chair: All right. That motion has been carried."
- **Motion 17, payments (moved by Ms Gray, pp. CEB-73 to CEB-74).** That the committee "include in its report to the Legislative Assembly the following: (a) all records of payments made to the chair and members of the independent advisory panel, (b) a list of payments made to all external experts, consultants, contractors, and legal advisers engaged by the independent advisory panel."
- **Second 3–2 vote, defeated (p. CEB-74).** "For the motion: Gray, Ganley. Against the motion: de Jonge, Rowswell, Wiebe. Totals: Against – 3, For – 2. The Chair: All right. Thank you. That motion is defeated."
- **No observations.** Ms Gray: "There were no observations made because the government members passed a motion that would stop the making of observations and observation motions" (p. CEB-73).

## What each is relied on for: who nominated the commissioners

Checked 2026-11-01 against the Assembly notice above.

- **The chair.** "The Honourable Justice Dallas K. Miller was appointed on March 19, 2025, by the Lieutenant Governor in Council to chair the Commission."
- **The four commissioners.** "Working with Justice Miller are the following four individuals, appointed by Speaker Cooper. Dr. Julian Martin (Sherwood Park) Nominated by the President of Executive Council John D. Evans, KC (City of Lethbridge) Nominated by the President of Executive Council Greg Clark (City of Calgary) Nominated by the Leader of His Majesty’s Loyal Opposition Susan Samson (Sylvan Lake) Nominated by the Leader of His Majesty’s Loyal Opposition."
- **The minority report is Martin's and Evans's.** It is signed "John Evans, K.C. Dr. Julian Martin, Commissioners" (final report, Appendix E, `commission_reports/abebc_2026_rpt_final.pdf`).
