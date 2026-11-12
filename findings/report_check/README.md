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
- Several CBC pages and the CCLA page returned 403, so those checks rest on search summaries. The research files say which.
- The Quebec assent date (June 12, 2026) comes from a summary of the Assemblée nationale page.

**Links to check:**
- The CBC "May 2026" link is the "seeks judicial chair" story and does not name O'Ferrall. The link was removed from his name and kept in the sources list.
- The CBC November 2025 notwithstanding-clause link could not be found in search.

**Conflicts and gaps in the record:**
- **Retraction timing:** the public report and `preregistration/retraction_conditions.md` said 48 hours; academic §6.2.6 said 30 days. Resolved 2026-11-12: the author chose 30 days, and every document and all 18 site languages now say 30 days.
- **Appendix E** does not exist (D goes to F). Nothing links to it.
- **The site's text** (`viewer/src/lib/i18n/locales/en.ts`) was not fact-checked separately. Only the Finding 15 and minority-quote fixes were carried over. One known difference: the report's corrected sweep says 49.2% and 1.6 points. The English site text matches it (`d4b5c735`); most translated locales still say 49.7% and 4 points.
- **The title** was changed by the author on 2026-11-07, from "Two Maps, Then None" to "Two Paths, One Map".
