# Chikina-Frieze-Pegden test of the panel's southern configuration (written before any walk)

> Written 2026-11-07, about 9:00 AM Alberta Time (UTC−6), before any walk has run. Unregistered and **not blind**: the regional ensemble results are known (`findings/hybrid_regions/`). Requested by the author ("sure", 2026-11-07). GitHub only; no OSF filing. Nothing here says whether any map is a gerrymander. As Cho and Rubinstein-Salzedo (2019) show, a significant result would mean the configuration is a **local** outlier: unusually extreme compared with small changes to itself. It would not show the configuration is unusual among all neutral maps.

## The test

Chikina, Frieze and Pegden (2017, *PNAS*) prove the following for a reversible Markov chain. Take a walk of any length starting from the presented state. If that state's value is in the most extreme fraction ε of the values along the walk, the null hypothesis that it was drawn from the chain's stationary distribution is rejected at p = √(2ε).

## The chain (reversible, as the theorem requires)

ReCom is not reversible, so it is not used. Instead:

- **States:** assignments of the panel's southern group's voting areas to its 8 districts.
  - Each district must be contiguous under queen adjacency (voting areas that touch, corners included).
  - Each district's 2021 population must be within ±25% of the region mean.
  - Every other division is held fixed.
  - Queen adjacency is a deviation from the rook adjacency used elsewhere. It is made so that the panel's districts are contiguous as drawn, without repairing them.
- **The move:** choose uniformly one of the pairs (a voting area, a different district it touches) and propose moving that area into that district. Accept with probability min(1, B / B′), where B and B′ are the numbers of such pairs before and after. This Metropolis-Hastings correction makes the chain reversible with respect to the uniform distribution over valid states. A rejected or invalid move leaves the state unchanged and still counts as a step.
- **Pinned areas:** any voting area that cannot reach the rest of the region under queen adjacency is held in its district and not moved.

## Values tested (all ballots)

1. **V1:** the share of Lethbridge's NDP two-party votes in seats the NDP loses by 10 points or more. Larger means more of the cracking pattern.
2. **V2:** the number of districts holding at least 2% of Lethbridge's 2021 population. Larger means more split.

ε is the fraction of states along the walk whose value is at least the panel's value, counting ties as at least as extreme (the conservative choice). One-sided, in the direction of more cracking. The test is reported for each value separately, and Bonferroni across the two: significant at 0.05 if p < 0.025.

## Walks

- **Length:** four independent walks of 1,000,000 steps, each from the panel's configuration.
- **Seeds:** drand, salt `cfp_lethbridge_<walk>`.
- **Reporting:** each walk's ε and p, plus how far the walk moved from the start (the share of voting areas reassigned at the end).

The theorem holds for any walk length. Short walks have low power, so a non-significant result does not show the configuration is typical.

**Signed:** Claude (acting as session agent), directed by Will Conner
