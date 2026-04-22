# v0_1 — Significance of Public Support for Minority Configurations

**Purpose.** The chair asserted in Appendix C that the dissenting minority's disputed configurations had "no public support" in the written submissions. A prior keyword-search pass (`submission_search_findings.md`) refuted that claim *precisely* on several configurations — at least some supporting submissions exist. This document asks the next question: **was the chair's characterization also *effectively* wrong — i.e., a material misrepresentation of what the public record shows — or merely technically defeated by a handful of outliers?**

All per-submission data is from `data/submission_search_dataset.csv`, which captures 70 hits across 1,252 machine-extractable submissions (93.4% of ~1,340 total; see caveats in the findings document).

---

## 1. Framework

A simple logical refutation ("one supporter exists, therefore 'no support' is false") is satisfying in debate but is not always the right standard for an *audit*. An audit concerned with whether a decision-maker fairly represented the record should measure not just the existence of counter-evidence, but its weight. We adopt three independent axes.

### 1.1 Engagement ratio
**Definition.** Supporting submissions ÷ total submissions that mention the configuration.
**Intuition.** Among citizens who cared enough to engage with this specific boundary question, what share backed the minority's direction? A high ratio means engaged public opinion on the question tilts toward the minority.
**Caveat.** The denominator is "engaged" citizens, not all citizens. Configurations with very small denominators produce unstable ratios.

### 1.2 Net support
**Definition.** Supporting − opposing submissions (neutrals excluded).
**Intuition.** Among those who took a side, does the minority's direction have more friends than enemies?
**Caveat.** A single well-argued opposing brief and a single short supporting letter both count equally here; use with absolute-count context.

### 1.3 Absolute support count
**Definition.** Raw count of supporting submissions.
**Intuition.** Does the minority's direction reach a critical mass of independent citizen voices? One detailed policy paper from a credible source may outweigh many form letters; conversely, three independent supports from different geographies is stronger evidence than one.
**Caveat.** Does not weight by quality; the narrative below annotates quality where relevant.

### 1.4 Thresholds (see §5 for rationale)

| Axis | Significant | Marginal | Negligible |
|---|---|---|---|
| Engagement ratio | ≥ 20% | 10–20% | < 10% |
| Absolute support | ≥ 3 | 1–2 | 0 |
| Net support | > 0 | = 0 | < 0 |

**Verdict mapping.** A configuration is:
- **Precisely + effectively wrong** if it meets the "significant" bar on *at least two of three* axes.
- **Precisely wrong only** if it has ≥ 1 supporting submission but fails the bar on ≥ 2 axes (existence refutes "no support" but the support is not material).
- **Chair's claim effectively stands** if supporting count is 0.
- **Insufficient data** if the configuration's denominator is near-zero and effective support cannot be assessed.

---

## 2. Per-configuration verdict table

Counts from `submission_search_dataset.csv` (automatic classification, with manual overrides preserved in the `(manual)` suffix). Raw counts include all position-labelled rows; "supporting" aggregates `supporting` and `supporting (manual)`.

| # | Configuration | Total hits | Supporting | Opposing | Neutral/ambig | Engagement ratio | Net support | Absolute support | **Verdict** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Airdrie 4-way split | 4 | 1\* | 1 | 2 | 25%\* | 0 | 1\* | **Precisely wrong only** (see note) |
| 2 | Calgary–Nolan Hill–Cochrane | 0 | 0 | 0 | 0 | n/a | n/a | 0 | **Chair's claim effectively stands** |
| 3 | Rocky Mountain House–Banff park (s.15(2)) | 20 | 5 | 1 | 14 | 25% | +4 | 5 | **Precisely + effectively wrong** |
| 4 | Olds–Three-Hills–Didsbury (preserve rural unit) | 5 | 3\*\* | 1 | 1 | 60% | +2 | 3\*\* | **Precisely + effectively wrong** |
| 5 | Chestermere (preserve separately) | 13 | 3 | 1 | 9 | 23% | +2 | 3 | **Precisely + effectively wrong** |
| 6 | Red Deer hybrids | 23 | 4 | 4 | 15 | 17% | 0 | 4 | **Precisely wrong; effectively ambiguous** |
| 7 | St. Albert–Sturgeon (minority alternative) | 11 | 2\*\*\* | 0 | 9 | 18% | +2 | 2\*\*\* | **Precisely wrong only** |

**Notes on starred rows:**

\* **Airdrie 4-way — disputed support.** The CSV codes `EBC-2025-1-0139` (City of Airdrie) as "supporting" because it proposes *some* form of Airdrie restructuring. The findings document's manual review found that none of Airdrie's three scenarios match the minority's specific 4-way split; the submission supports Airdrie getting more than one seat, not the minority's particular carve. Under a strict read, absolute support = 0 and the chair's claim effectively stands. Under the generous CSV classification, there is 1 supporter but a matching opposer (`EBC-2025-2-1017` opposes any division of Airdrie). Either read yields a verdict between "chair's claim effectively stands" and "precisely wrong only." **No read supports effectively wrong.**

\*\* **Olds–Three-Hills–Didsbury — generous coding.** `EBC-2025-1-0139` also appears here; manual inspection of its quote confirms it discusses rural/urban hybrid configurations generally and can reasonably count. The two Beiseker submissions (`EBC-2025-2-0161`, `EBC-2025-2-0209`) are unambiguous explicit supports for preserving a rural Olds-Didsbury-Three Hills anchor. Even dropping 1-0139 to neutral leaves 2 supporters vs. 1 opposer, which still meets net > 0 and approaches the absolute-count bar. Verdict holds.

\*\*\* **St. Albert–Sturgeon — classification ambiguity.** "St. Albert–Sturgeon" is the *majority's* name; submissions using that name may be supporting the majority's proposal, not the minority's alternative. The findings document notes the minority's alternative configuration name is not present in any submission. The 2 "supporting" rows here (`EBC-2025-2-0582`, `EBC-2025-2-0974`) appear to be supporting *some* St. Albert–area hybrid but not specifically the minority's variant. Treat this verdict as soft.

---

## 3. Interpretive guidance: gotcha versus material

A refutation of "no public support" can be cosmetic (gotcha) or substantive (material). The difference matters for the audit's procedural critique (§D2).

**Gotcha refutation.** The chair says "no public support"; we find 1 marginal supporter out of 5 engaged citizens who mention the configuration. Logically the chair is wrong, but the characterization — "the public record does not meaningfully back this direction" — is essentially accurate. A reasonable reader would feel the chair oversold slightly, not misrepresented.

Example in this dataset: **Airdrie 4-way** (row 1). Engagement ratio is 25% only under a generous coding; absolute support is 0–1. The chair who said "no public support for a 4-way split" is technically vulnerable if we count `EBC-2025-1-0139` as supporting, but the submission does not actually propose a 4-way split. A fact-checker would likely rule the chair's statement "mostly true."

**Material refutation.** The chair says "no public support"; we find that the configuration was *proposed by* citizens in the public record, not imposed *despite* them. A reasonable reader would now perceive the chair as having mischaracterized the record itself.

Example in this dataset: **RMH–Banff park** (row 3). `EBC-2025-2-0619` is a detailed position paper titled "Appropriate Political Representation for Alpine Alberta" that explicitly recommends, by name and boundary, exactly the minority's s.15(2)-invoking configuration. Four additional submissions (0091, 0095, 0555, 1029) back the same direction. Opposing submissions number one. A chair telling the commission's readers that this configuration had "no public support" is presenting the record exactly backwards: the minority did not invent this district; they adopted it from engaged public voices. This is material.

**Rule of thumb.** If you can point to an explicit, self-identified proposal of the configuration by a credible public voice *and* majority-positive net support among those who engaged, the chair was effectively wrong. If you can only point to tangentially aligned opposition to the majority's proposal (without any citizen actually proposing the minority's alternative), the refutation is technical.

Applied to this dataset: RMH–Banff, ODH, and Chestermere meet the "citizens proposed this, chair said they didn't" standard. Red Deer hybrids meet it weakly (net zero; proposals exist but opposition is equally represented). Airdrie 4-way, Nolan-Hill–Cochrane, and St. Albert do not meet it.

---

## 4. Summary for the academic report (<300 words)

The commission chair's Appendix C assertion that the dissenting minority's disputed hybrid configurations had "no public support" in the written submissions is not uniformly defensible. Systematic keyword search of 1,252 extractable public submissions (93% of ~1,340 total) finds that the chair's characterization ranges from effectively sound to materially misleading depending on the configuration.

**For three of seven configurations — Rocky Mountain House–Banff Park, Olds–Three-Hills–Didsbury, and Chestermere — the chair is both precisely and effectively wrong.** Engaged public submissions explicitly *proposed* these directions, with net positive support and absolute supporter counts of 3–5 each. The most striking is RMH–Banff Park: a detailed position paper (EBC-2025-2-0619) and four aligned submissions propose the minority's s.15(2)-invoking alpine district by name and boundary. The minority adopted this configuration from the public record, not in spite of it. Characterizing it as having "no public support" is a material misrepresentation.

**For one configuration (Red Deer hybrids), the chair is precisely wrong but the public record is genuinely divided**: four supporters and four opposers on the hybrid direction. The audit should note the split rather than claim refutation.

**For three configurations (Airdrie 4-way split, Calgary–Nolan-Hill–Cochrane, St. Albert–Sturgeon minority alternative), the chair's claim effectively stands**: no citizen submission explicitly proposes the minority's specific carve, and Nolan-Hill–Cochrane has zero matching submissions in the record.

**Implication for the D2 procedural finding.** The audit's procedural critique narrows but does not dissolve. The chair overstated the sweep of his Appendix C dismissal. Three of seven configurations materially misrepresent the public record; one is ambiguous; three are defensible. A revised finding should distinguish these tiers rather than treat Appendix C as uniformly unsupported or uniformly sound.

---

## 5. Methodology notes

### 5.1 Threshold rationale

- **Engagement ratio ≥ 20% as "significant."** Among citizens engaged enough to submit on a specific boundary question, one-in-five backing a direction constitutes a meaningful minority voice in participatory-input terms. Below 10% is essentially noise given the small denominators involved (5–23 submissions per configuration).
- **Absolute count ≥ 3 as "critical mass."** Three independent submissions from different authors/geographies distinguish a genuine public-input signal from a single advocate or a coincidental reference. Below 3, claims about "the public" are always contestable.
- **Net support > 0.** The minimum bar for "public opinion on this question leans toward the minority" rather than "the public is split" or "the public leans against."

These thresholds are conservative-for-the-audit: they make it *harder* to conclude the chair was effectively wrong. A more aggressive framework (e.g., engagement ratio ≥ 15%) would flip the Red Deer verdict to "effectively wrong" as well.

### 5.2 Ambiguity resolutions

- **EBC-2025-1-0139 (City of Airdrie) counted in 3 configurations.** CSV codes it as supporting across Airdrie-4way, Olds-Three-Hills-Didsbury, and Red Deer hybrids. The findings document's manual review concludes it does not actually match the minority's 4-way Airdrie carve. Resolution: retain the generous CSV classification in the table, but annotate the Airdrie row as disputed (note \* in §2). Verdict does not change under either read.
- **St. Albert–Sturgeon ambiguity.** The majority and minority both propose St. Albert–area hybrids under different configurations; submissions typically do not distinguish which variant they back. Resolution: verdict held soft ("precisely wrong only") pending a more targeted re-read that classifies by specific boundary rather than by riding name.
- **Red Deer net-zero.** Four supporters vs. four opposers produces net = 0 (marginal). Two of three axes (engagement ratio 17%, absolute ≥ 3) meet or approach the significant bar; net support does not. Resolution: verdict "precisely wrong; effectively ambiguous" — below the effective-wrong threshold on our 2-of-3 rule, but close. Audit should describe the split honestly rather than claim clean refutation.

### 5.3 Inherited caveats from the keyword search

1. ~88 submissions (6.6%) are image-only PDFs that were not OCR'd. These are not known to contain supports; they are simply not machine-searchable. Would affect opposing and neutral totals more than supporting totals (which came primarily from manual review of hits).
2. Keyword co-occurrence windows (200–300 chars) may miss paraphrased proposals.
3. Position classifier is heuristic; manually corrected for clear cases, but borderline rows retain automatic labels.
4. Submission authors generally do not know the minority's specific configuration names, so directional matches (not label matches) are counted as support.

No caveat changes the headline finding: RMH–Banff, ODH, and Chestermere cannot be characterized as having "no public support" without materially misrepresenting the submission record.
