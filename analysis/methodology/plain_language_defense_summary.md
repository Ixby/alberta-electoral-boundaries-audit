# Plain-Language Defense — One-Page Synthesis

**Source:** `analysis/methodology/plain_language_defense.md` (215 assertions, §§1–8, all appendices)
**Purpose:** Quick-reference for reviewers, journalists, and institutional readers. Organized by the six challenge categories most likely to arise.

---

## 1. "You're calling this a gerrymander."

The audit does not. It asks a narrower empirical question: do the measurable properties of the minority map fall within the range that Canadian law and neutral random processes would produce? That is a question data can answer. Whether the deviation constitutes an illegal gerrymander is a legal judgment for courts. The audit's formal claim is that the minority map's boundary choices exceed the discretion space that Canadian independent-commission practice normally occupies — not that unlawful intent existed.

---

## 2. "Your statistical tests are rigged to find what you were looking for."

Three safeguards rule this out. First, every test was pre-registered on a public registry (OSF) before the data were examined — the null hypotheses, pass/fail thresholds, and predicted directions are locked in a dated public record. Second, the same tests were applied symmetrically to both maps; the majority map passes every threshold the minority map fails. Third, three findings ran *against* the researcher's stated prior and were retained: the partisan-bias sign reverses under 2019 vote inputs; the chair's "no public support" claim holds on three of seven configurations, not all seven; and the majority map's own population dispersion is tighter than the 2019 baseline. A rigged process would have dropped these.

---

## 3. "A computer simulation that drew a million fake maps proves nothing about a real one."

The simulation does not draw arbitrary fake maps — it draws random maps that satisfy the same legal constraints the commission faced: equal population within statutory tolerance, geographically contiguous districts, same number of seats. All random seeds come from a public cryptographic randomness beacon (Cloudflare drand) committed to git before execution, so no seed was chosen after results were seen. The simulation ran long enough that four independent chains converged (Gelman-Rubin R̂ < 1.1 on all metrics). An independent seed re-run with a separately derived key confirmed the canonical results within sampling variation.

---

## 4. "Your threshold is arbitrary — you picked a number that makes the minority map fail."

The 4.10% efficiency-gap threshold is the 95th percentile of over one million randomly drawn neutral Alberta maps under 2023 vote shares — the same election in which the minority map was drawn. It is the jurisdiction-specific ceiling, not a number imported from another context. As a cross-check, two additional ensembles were run using 2019 and 2015 vote shares: the resulting p95 values were 1.01% (UCP landslide) and 9.71% (NDP wave), producing a jurisdiction-normed range of 1.01%–9.71%. The minority map falls below the threshold in the two more recent electoral contexts and above it only under 2015 conditions — the most UCP-unfavorable election in modern Alberta history. The majority map falls below the threshold in all three contexts. The US academic reference threshold of 7% (Stephanopoulos & McGhee) sits in the middle of that range; both maps are below 7%, and the Alberta 4.10% threshold is stricter than the US reference.

---

## 5. "You used AI tools — the analysis isn't reliable."

AI tools were used as drafting and consistency-checking assistants, not as analytical decision-makers. No AI tool executed code, accessed data files, or computed a number that appears in the report. Every number was verified by the researcher against the original data files and script outputs. All code is open-source Python; all inputs are publicly available data from Elections Alberta and Statistics Canada. Any reader with a standard computer can re-run every script against the same inputs and reproduce every number in the report.

---

## 6. "You hid a failed finding."

The opposite occurred. Municipal-boundary anchoring was one of five pre-registered dimensions. Earlier analysis using approximate boundary tracings (from PDF images, before official shapefiles were available) showed a large asymmetry between the two maps. When the official Elections Alberta shapefiles arrived and the measurement was rerun on the exact files, both maps fell within the 70–85% Canadian comparator norm (72% and 80% respectively). The finding collapsed. The audit reports this explicitly in §5.8.5 under a "RETRACTED FINDING" label, explains why it failed, and removes it from the Fisher combination. It does not appear in any headline result.

---

*Full entry-by-entry record: `analysis/methodology/plain_language_defense.md`*
