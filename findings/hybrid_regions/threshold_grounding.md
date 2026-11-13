# Grounding the "unusual" threshold in the literature (2026-11-07)

**Unregistered.** This replaces no registered threshold. It sets out what the published methods literature supports for calling a map an outlier against neutral maps, and re-reads this session's unregistered results against it. Sources are listed at the end; each is described only as far as its abstract or the cited search result states.

## What the literature uses

**1. Global outlier against an ensemble** (Herschlag et al. 2020, *Statistics and Public Policy*). A plan is compared with an ensemble of nonpartisan plans that satisfy the legal criteria. The enacted North Carolina plans were reported as "extreme outliers" and the judges' plan as not extreme. The approach was central to *Common Cause v. Lewis* (N.C. Super. 2019).
- The abstract gives no fixed percentile line. The practice is to show where the plan falls in the full distribution.
- Mattingly's 2019 rebuttal frames the comparison as what would have happened "if partisanship had not been explicitly considered", which is what this audit's ensembles do.

**2. A rigorous local test** (Chikina, Frieze and Pegden 2017, *PNAS*). Start a random walk from the plan itself. If the plan is in the most extreme fraction ε of the states that walk visits, that is significant at p = √(2ε), with no assumption that the chain has mixed.
- For p < 0.05, ε must be at most 0.00125: the plan is more extreme than 99.875% of the walk.
- Cho and Rubinstein-Salzedo (2019) show this identifies local outliers. A map can be a local outlier and still have a typical fairness value, so this test is separate from a global outlier test. Chikina et al. agree the two are different tests.

**3. A fixed efficiency-gap line** (Stephanopoulos and McGhee 2015, *U. Chi. L. Rev.*). They propose |EG| ≥ 8% for state-house plans, and two seats for congressional plans, as a presumptive threshold, and only where the imbalance is likely to last the decade.

**4. Choice of measure matters most.** In a power study of the Chikina test, the bias metric chosen had the largest effect on whether a biased map was caught (Clark et al. 2025, arXiv, not peer-reviewed).

**5. Multiple tests.** Neither paper above sets a rule for many regions tested at once. The standard correction (Bonferroni) divides the error rate by the number of tests.

## What that means for this session's thresholds

The plan's rule, beyond the 95th percentile or below the 5th, is a conventional 5%-per-tail global-outlier line. It is weaker than all three published standards:
- **No multiplicity correction:** it was applied across at least ten informative tests.
- **Lower bar than the case work:** it is far below the "extreme outlier" standard of the North Carolina analyses.
- **Wrong test for Chikina's bound:** these chains start from random plans, not from the map, so Chikina's bound does not apply.

| Standard | Line | Lethbridge, city-aware (4 pieces in 0.9% of plans; NDP votes in lopsided losses at p93) | St. Albert, city-blind (p97) |
|---|---|---|---|
| Plan's rule (5% per tail) | beyond p95 | no (p93) | yes |
| Bonferroni, at least 10 tests | beyond p99.75 or stricter | no | no |
| Chikina et al., if a walk from the map gave the same ε | ε ≤ 0.00125 | no (ε ≈ 0.009 gives p ≈ 0.13; ε ≈ 0.07 gives p ≈ 0.37) | no (ε ≈ 0.03 gives p ≈ 0.25) |
| Stephanopoulos-McGhee | \|EG\| ≥ 8% | not a regional measure | not a regional measure |

The Chikina row is illustrative only. The ε values come from chains that did not start at the map, so the p-values are what the bound would give if a walk from the map produced the same fractions.

**Province-wide efficiency gaps against the 8% line.** All ballots:

| Map | Efficiency gap |
|---|---|
| Panel | −1.66% |
| ¶167 | −2.19% |
| Commission majority | −2.70% |
| Commission minority | +2.55% |

On election-day votes the minority is +4.02%. No map comes near 8%. The registered P1 line (+1.39% on all ballots, Amendment 12) is the audit's own ensemble calibration, not a legal line, and is much stricter than the published proposal.

## Reading

- Under every standard the literature supports, nothing in this session's regional or packing results is a statistically significant outlier.
- The Lethbridge four-way split is the closest: rare (0.9% of city-aware plans), but not significant once multiple tests or Chikina's bound are applied.
- St. Albert's single flag does not survive any correction. It is as rare as one result among this many comparisons would be against nonpartisan alternatives.

## A test that applies properly (run: `README.md`, Chikina-Frieze-Pegden section)

The Chikina et al. test for Lethbridge walks from the panel's own southern configuration and asks whether it is extreme among the plans visited. On the voting-area graph two of the panel's districts are not contiguous (signal F's deviation). The walks did not repair the plan; they let each district have no more pieces than it has in the panel's plan, a disclosed deviation. On all four walks of 1,000,000 steps every p is at least 0.89: the configuration is not a local outlier. By Cho and Rubinstein-Salzedo, that answers the local question, not the global one.

## Sources
- Herschlag, G. J., et al. (2020). Quantifying gerrymandering in North Carolina. *Statistics and Public Policy*. https://consensus.app/papers/details/9533278654a85506a53b8e0383ac6c8f/
- Chikina, M., Frieze, A., & Pegden, W. (2017). Assessing significance in a Markov chain without mixing. *PNAS*. https://consensus.app/papers/details/dbdd7cf87aa15193a255d188025e42b1/
- Cho, W. K. T., & Rubinstein-Salzedo, S. (2019). Understanding significance tests from a non-mixing Markov chain for partisan gerrymandering claims. *Statistics and Public Policy*. https://consensus.app/papers/details/bf63d7b4a733560f97d969d8ab5e5aa6/
- Chikina, M., Frieze, A., & Pegden, W. (2019). Understanding our Markov chain significance test: a reply. *Statistics and Public Policy*. https://consensus.app/papers/details/58fe50f6427a58e1b3ff84030f35ab7f/
- Clark, R. A., et al. (2025). Empirical power analysis of a statistical test to quantify gerrymandering. arXiv. https://consensus.app/papers/details/7a9ee7a031e45720979c69265cec0417/
- Stephanopoulos, N., & McGhee, E. (2015). Partisan gerrymandering and the efficiency gap. *University of Chicago Law Review* 82, 831. Threshold as described in https://arxiv.org/pdf/1705.10812 and https://arxiv.org/pdf/1805.12572.
- Mattingly, J. C. (2019). Rebuttal report, *Common Cause v. Lewis*. https://sites.duke.edu/quantifyinggerrymandering/files/2019/09/Rebuttal.pdf
