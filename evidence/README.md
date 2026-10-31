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

Full hashes:

```
e34f13093c7fdcb8b815ea5c7aba18d5943398689cc4215bc3dc0f8047bcdb85  electoral_boundaries_commission_act_RSA2000_cE-3_current_2026-05-14.pdf
eca9fc7dcf80aea7023794657578b7c493ed7657394542ddbee0a7908844caa9  interpretation_act_RSA2000_cI-8_current_2025-09-01.pdf
fa0c134755325fa37839512c27472fd78fc28c007db5174c0ce3333cf277b7b4  municipal_government_act_RSA2000_cM-26_current_2026-09-01.pdf
63abb96a382144b6afaf5d1612156b62e32b0c1054afe2683258210aaf43c8e2  alberta_hansard_1990-12-10_evening.pdf
7236cd0aaa611f5198f88856f677a2028f9a442dccdc0359725b4995a2d0247e  abebc_2026_rpt_final.pdf
a3555d34175901deac78706820d7778c3adf5e37128020879fccaaa1feedc5f0  abebc_2003_rpt_final.pdf
```

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

The documents support both readings. Read as written, "town" is a legal status that a city does not have, and the Act uses "city" separately where it means city. The 1990 justification for the Crowsnest Pass clause turned on density and settlement pattern, which supports reading (c) as a test of whether a district holds an urban centre. Amendment 25 (proposed, not yet signed) would run set D under both readings.
