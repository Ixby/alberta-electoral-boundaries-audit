# Fact-check of the public report (2026-11-07)

`reports/public/report_public.md` was checked at commit `2d47e0b6`. Every checkable claim (number, quote, citation and fact) was tested against the repo's data and saved sources. The report was then corrected in four commits: `ac190790`, `a7b5570e`, `fecaafaf` and the legal-research commit that follows them.

## First pass: six section checks

| Section (lines at `2d47e0b6`) | Claims | Verified | Mismatch | Stale | Unverifiable | Opinion |
|---|---:|---:|---:|---:|---:|---:|
| 1–76, opening | 46 | 37 | 1 | 0 | 3 | 5 |
| 77–167, Act I | 94 | 66 | 7 | 0 | 5 | 16 |
| 168–266, Act II | 100 | 76 | 4 | 1 | 5 | 14 |
| 267–372, Act III | 99 | 78 | 2 | 0 | 13 | 6 |
| 373–465, Scorecard and Author's View | 80 | 57 | 1 | 6 | 9 | 7 |
| 466–end, appendices | 114 | 84 | 1 | 0 | 8 | 21 |
| **Total** | **533** | **398** | **16** | **7** | **43** | **69** |

Files: `section_*.json`, one record per claim (line, claim, status, source, value found).

**How each result was handled:**
- **Every mismatch** was re-checked against its source before the report was edited. Fifteen were fixed. The sixteenth, a "dangling sentence" in Appendix B, was a false report: the checking agent's tool had cut the line short, and the sentence is complete. Two further corrections came out of checking the Finding 15 mismatch: the 4.5× ratio (14,199 against 3,152) and the panel's 53,722 average.
- **Stale items** (the November statements, and the efficiency-gap line under Amendment 12) are updated. A new section, "November: the panel's map, checked", carries the results.

## Second pass: research on the unverifiable claims

Per the author ("anything marked can't verify gets researched"), all 43 were researched in three groups. Files: `research_legal.json`, `research_alberta.json` and `research_methods_internal.json`, each with a source, a quote or number, and a suggested rewording.

| Group | Entries | Supported | Partly | Contradicted | Still unverified |
|---|---:|---:|---:|---:|---:|
| Legal and history | 16 | 8 | 6 | 0 | 2 |
| Alberta politics and records | 11 | 5 | 6 | 0 | 0 |
| Methods and internal | 17 | 5 | 8 | 3 | 1 |

**Partly supported or contradicted:** the claim was narrowed or reworded in the report. Examples:
- "found no" in place of "has never";
- Bill 20's powers as passed;
- the Nova Scotia court's own words;
- Quebec's June 2026 law;
- the mechanism test described as the compactness test it was;
- the ledger's "only score" sentence corrected;
- retraction conditions 4 and 5 labelled as not yet registered.

Two clauses with no support were removed:
- "many from the Indigenous communities" (Lesser Slave Lake submissions);
- "five commissioners, five reports" (1992).

**Still unverified (3).** All three are hedged absence claims, kept with their hedge:
- no Canadian decision striking a map for splitting a city;
- no Canadian court weighing ensemble evidence;
- no Canadian body using the efficiency gap.

## Left for the author

**Sources to re-read by hand:**
- Several CBC pages and the CCLA page returned 403 at the time, so those checks rested on search summaries. **Re-checked 2026-11-12** with a browser user agent; every cited page loads and its title matches the claim it backs:
  - CBC 9.7172743 (April 2026): "MLA committee to review Alberta electoral boundaries after report is set aside".
  - CBC 9.7187435 (published 2026-05-05): "All-party committee seeks judicial chair to lead effort to redraw Alberta electoral boundaries".
  - CBC 9.7167110: "Alberta wants to set aside commission report, strike MLA committee to look at 91-seat legislature".
  - CBC 9.7169185: "Another try to redraw electoral boundaries would create challenging timeline: Elections Alberta".
  - CBC 1.6678407: "Alberta passes Sovereignty Act, but first strips out sweeping powers for cabinet".
  - CBC 1.7185346 (April 2024; redirects to a new slug): "Alberta government wants power to remove municipal councillors, repeal bylaws it doesn't like".
  - CBC lite 1.7383348: "N.S. Supreme Court rules Chéticamp should have protected Acadian electoral district".
  - CBC lite 1.7374605: "Alberta to get 2 new provincial electoral ridings for next election".
  - CCLA, "CCLA Sounds the Alarm Over the Politicization of Alberta's Electoral Map", published 2026-04-20. The live page sits behind a bot challenge; it was read from the Wayback Machine copy of 2026-11-02 (`web.archive.org/web/20261102130530/...`).
- The Quebec assent date (June 12, 2026) comes from a summary of the Assemblée nationale page.

**Links to check:**
- The CBC "May 2026" link is the "seeks judicial chair" story and does not name O'Ferrall. The link was removed from his name and kept in the sources list.
- The CBC November 2025 notwithstanding-clause link (9.6983786) exists: "Alberta to invoke notwithstanding clause to shield 3 transgender bills from court challenges", published 2025-11-18. It supports the bill. The bill's passage on December 11, 2025 and the injunction's end come from the Egale timeline cited beside it. **Resolved 2026-11-12.**

**Conflicts and gaps in the record:**
- **Retraction timing:** the public report and `preregistration/retraction_conditions.md` said 48 hours; academic §6.2.6 said 30 days. Resolved 2026-11-12: the author chose 30 days, and every document and all 18 site languages now say 30 days.
- **Appendix E** does not exist (D goes to F). Nothing links to it.
- **The site's text** (`viewer/src/lib/i18n/locales/en.ts`) was not fact-checked separately. Only the Finding 15 and minority-quote fixes were carried over. One known difference: the report's corrected sweep says 49.2% and 1.6 points. The English site text matches it (`d4b5c735`); most translated locales still say 49.7% and 4 points.
- **The title** was changed by the author on 2026-11-07, from "Two Maps, Then None" to "Two Paths, One Map".
