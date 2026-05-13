# Plain-Language Defense — One-Page Synthesis

**Source:** `analysis/methodology/plain_language_defense.md` (215 assertions, §§1–8, all appendices)
**Purpose:** Quick-reference answers to the six objections most likely to arise from reviewers, journalists, and institutional readers.

---

## 1. "You're calling this a gerrymander."

The audit does not. A gerrymander is a legal conclusion about intent — that a map was deliberately drawn to entrench one party's power. This audit makes no claim about intent and draws no legal conclusion. What it does is narrower: it measures whether the minority map's boundary choices fall within the range you would expect from a fair, neutral process. That is a question numbers can answer. Whether the measured divergence rises to the level of a gerrymander is a question for courts, not a statistical audit.

---

## 2. "Your tests are designed to find what you were looking for."

Three things make that impossible. First, every test was publicly declared — on the Open Science Framework, a public academic registry — before the data were examined. The test criteria, pass thresholds, and predicted outcomes are in a dated public record you can check right now. Second, every test was run on both maps identically. There is no test in this audit that applies to the minority map but not the majority. Third, three findings came out against the researcher's stated prior expectations and are reported in full anyway: the partisan-bias direction reverses under a different set of election results; the commission chair's claim about public opposition was upheld on some configurations but not all; and the majority map actually has tighter population distribution than the 2019 baseline. A process designed to confirm a predetermined conclusion would have quietly dropped those three results. They are in the paper.

---

## 3. "A computer simulation of a million fake maps proves nothing about a real one."

The simulation does not draw arbitrary fake maps. It draws random maps subject to the same legal rules the commission was required to follow: districts must be connected, roughly equal in population, and satisfy the same geographic constraints. The result is a reference band — the range of outcomes a fair, unbiased process would normally produce. When the minority map's scores fall outside that band, it means they are more extreme than nearly every one of the million randomly drawn neutral maps. The randomness itself is auditable: all random seeds come from a public cryptographic timestamp service (operated by Cloudflare), committed to git before the analysis ran. No seed was chosen after the results were seen. As a check, a second run with a completely different seed reproduced the same results within normal statistical variation.

---

## 4. "You picked a threshold that makes the minority map fail."

The threshold — 4.10% efficiency gap — was not chosen by the researcher. It is the value that 95% of the million randomly drawn neutral Alberta maps fall below, computed from the same 2023 election that produced these maps. It is Alberta's own ceiling for what a neutral process normally produces, not a number imported from another context. As a further check, the same computation was run using vote data from the 2019 and 2015 elections. The resulting ceilings were 1.01% (2019, a one-sided Conservative landslide) and 9.71% (2015, a one-sided NDP sweep). The minority map falls below the ceiling under 2019 and 2023 conditions; it exceeds the ceiling only under 2015 conditions — the most unfavorable historical context. The majority map falls below the ceiling in all three. The US academic reference threshold of 7% sits in the middle of that range; both maps pass under that standard too. The 2023 ceiling of 4.10% is actually stricter than the US reference, not weaker.

---

## 5. "You used AI tools — the analysis isn't reliable."

AI tools were used the way a researcher might use a spell-checker or a search engine — to help draft text, catch inconsistencies, and suggest approaches. No AI tool ran any analysis, accessed any data file, or produced any number that appears in the report. Every number was verified by the researcher against the original source files and script outputs. All code is publicly available Python; all input data comes from Elections Alberta and Statistics Canada. Anyone with a standard computer can re-run every script against the same publicly available data and reproduce every number independently.

---

## 6. "You hid a finding that didn't work out."

The opposite happened. Municipal-boundary anchoring — whether the map's district lines follow city and town boundaries — was one of five tests announced in advance on the public registry. Early analysis, done before Elections Alberta released its official boundary files, showed a large gap between the two maps. When the official files arrived and the test was rerun on them, both maps turned out to respect city and town boundaries at rates that are normal for Canadian redistricting (72% and 80%, within the typical 70–85% range). The finding collapsed. It is reported explicitly in the paper under a "RETRACTED FINDING" label that explains why it failed. It does not appear in any headline result. The audit's other findings do not depend on it.

---

*Full entry-by-entry record: `analysis/methodology/plain_language_defense.md`*
